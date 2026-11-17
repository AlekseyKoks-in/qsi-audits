#!/usr/bin/env python3
"""Verify the signed audit bundles in this repository. No dependencies, no network, no trust in the publisher.

    python3 verify.py                 # verify every bundle under audits/
    python3 verify.py audits/secp256k1
    python3 verify.py --self-test     # check the verifier itself before you trust its "OK"

What is checked, per bundle:

  1. bundle.sig.json carries an Ed25519 signature over a canonical JSON payload. The signature is verified
     against the public key embedded in that same file.
  2. That embedded key is compared byte for byte with public_key.pem in the bundle, and with PUBLIC-KEY.pem at
     the repository root, so one substituted key cannot quietly re-sign one bundle.
  3. Every file named in the payload's files_sha256 is re-hashed and compared.
  4. report.sig.json is verified the same way, and its content_sha256 is compared with the value inside
     report.json, which is where the report states its own digest.
  5. Where the payload names an ML-DSA-65 key (pq_key_id; bundles signed from 13 November 2026 on), the
     post-quantum co-signature over the same payload is verified too (FIPS 204, with the payload's schema as the
     context string), its key must be the one the payload names, and it must equal public_key_mldsa.pem in the
     bundle and PUBLIC-KEY-MLDSA.pem at the repository root where those exist. A payload that names a key whose
     signature is missing, or a post-quantum signature that the payload does not name, fails.

A bundle only passes if all of these hold. Anything else prints FAIL and the reason, and the exit status is 1.
Bundles signed before the post-quantum co-signature existed carry Ed25519 alone and pass on checks 1-4.

Both signature schemes are verified twice where possible: with the `cryptography` package if it is installed
(ML-DSA needs cryptography 48 or later built with OpenSSL 3.5), and with a self-contained implementation in this file
(RFC 8032 for Ed25519, FIPS 204 for ML-DSA-65). When both are available both must agree, so a bug in the bundled
implementation cannot turn a bad signature into a good one without the installed library agreeing to it.
Run --self-test to see that the implementations agree, that real signatures and NIST's ML-DSA test vectors
(mldsa65-kat.json, from the ACVP server) give the expected answers, and that one flipped byte is detected.
"""
from __future__ import annotations

import base64
import hashlib
import json
import pathlib
import sys

# ---------------------------------------------------------------- Ed25519, RFC 8032, self-contained

_P = 2**255 - 19
_L = 2**252 + 27742317777372353535851937790883648493
_D = -121665 * pow(121666, _P - 2, _P) % _P


def _inv(x: int) -> int:
    return pow(x, _P - 2, _P)


def _add(P, Q):
    x1, y1 = P
    x2, y2 = Q
    k = _D * x1 * x2 * y1 * y2 % _P
    x3 = (x1 * y2 + x2 * y1) * _inv(1 + k) % _P
    y3 = (y1 * y2 + x1 * x2) * _inv(1 - k) % _P
    return (x3, y3)


def _mul(P, n: int):
    R = (0, 1)
    while n:
        if n & 1:
            R = _add(R, P)
        P = _add(P, P)
        n >>= 1
    return R


_BY = 4 * _inv(5) % _P


def _recover_x(y: int, sign: int):
    if y >= _P:
        return None
    xx = (y * y - 1) * _inv(_D * y * y + 1) % _P
    if xx == 0:
        return None if sign else 0
    x = pow(xx, (_P + 3) // 8, _P)
    if (x * x - xx) % _P != 0:
        x = x * pow(2, (_P - 1) // 4, _P) % _P
    if (x * x - xx) % _P != 0:
        return None
    if x & 1 != sign:
        x = _P - x
    return x


_B = (_recover_x(_BY, 0), _BY)


def _decode_point(b: bytes):
    if len(b) != 32:
        return None
    y = int.from_bytes(b, "little")
    sign = (y >> 255) & 1
    y &= (1 << 255) - 1
    x = _recover_x(y, sign)
    return None if x is None else (x, y)


def _ed25519_verify_pure(pub32: bytes, msg: bytes, sig: bytes) -> bool:
    if len(sig) != 64 or len(pub32) != 32:
        return False
    A = _decode_point(pub32)
    R = _decode_point(sig[:32])
    if A is None or R is None:
        return False
    S = int.from_bytes(sig[32:], "little")
    if S >= _L:
        return False
    h = int.from_bytes(hashlib.sha512(sig[:32] + pub32 + msg).digest(), "little") % _L
    return _mul(_B, S) == _add(R, _mul(A, h))


def _ed25519_verify_library(pub_pem: str, msg: bytes, sig: bytes):
    """True/False with the installed `cryptography`, or None when it is not available."""
    try:
        from cryptography.exceptions import InvalidSignature
        from cryptography.hazmat.primitives.serialization import load_pem_public_key
    except Exception:
        return None
    try:
        key = load_pem_public_key(pub_pem.encode())
    except Exception:
        return False
    try:
        key.verify(sig, msg)
        return True
    except InvalidSignature:
        return False
    except Exception:
        return False


def _pem_der(pem: str) -> bytes:
    body = "".join(l.strip() for l in pem.strip().splitlines() if "-----" not in l)
    return base64.b64decode(body)


def _raw_from_pem(pem: str) -> bytes:
    """The 32 raw bytes of an Ed25519 SubjectPublicKeyInfo PEM; the key bytes are its last 32."""
    der = _pem_der(pem)
    if len(der) < 32:
        raise ValueError("public key too short")
    return der[-32:]


def ed25519_verify(pub_pem: str, msg: bytes, sig: bytes) -> tuple[bool, str]:
    pure = _ed25519_verify_pure(_raw_from_pem(pub_pem), msg, sig)
    lib = _ed25519_verify_library(pub_pem, msg, sig)
    if lib is None:
        return pure, "built-in"
    if lib != pure:
        return False, f"IMPLEMENTATIONS DISAGREE (built-in={pure}, cryptography={lib})"
    return pure, "built-in + cryptography"


# ---------------------------------------------------------------- ML-DSA-65, FIPS 204, self-contained (verification)
#
# Only what verification needs: unpacking the public key and the signature, ExpandA, SampleInBall, the NTT, and
# UseHint. Section and algorithm numbers are those of FIPS 204 (August 2024).

_Q = 8380417
_K, _LCOLS = 6, 5            # ML-DSA-65: a k x l matrix
_TAU, _BETA = 49, 196        # beta = tau * eta, eta = 4
_GAMMA1 = 1 << 19
_GAMMA2 = (_Q - 1) // 32
_OMEGA = 55
_CTILDE = 48                 # lambda / 4 bytes, lambda = 192
_PK_LEN = 32 + 32 * _K * 10  # 1952
_SIG_LEN = _CTILDE + _LCOLS * 32 * 20 + _OMEGA + _K  # 3309
_ZETAS = [pow(1753, int(format(i, "08b")[::-1], 2), _Q) for i in range(256)]
_N_INV = pow(256, _Q - 2, _Q)  # 8347681
# SubjectPublicKeyInfo of an ML-DSA-65 key: AlgorithmIdentifier with OID 2.16.840.1.101.3.4.3.18, then the raw key.
_MLDSA65_SPKI = bytes.fromhex("308207b2300b0609608648016503040312038207a100")


def _ntt(a: list[int]) -> list[int]:
    """Algorithm 41."""
    a = list(a)
    m, length = 0, 128
    while length >= 1:
        for start in range(0, 256, 2 * length):
            m += 1
            z = _ZETAS[m]
            for j in range(start, start + length):
                t = z * a[j + length] % _Q
                a[j + length] = (a[j] - t) % _Q
                a[j] = (a[j] + t) % _Q
        length //= 2
    return a


def _intt(a: list[int]) -> list[int]:
    """Algorithm 42."""
    a = list(a)
    m, length = 256, 1
    while length < 256:
        for start in range(0, 256, 2 * length):
            m -= 1
            z = -_ZETAS[m] % _Q
            for j in range(start, start + length):
                t = a[j]
                a[j] = (t + a[j + length]) % _Q
                a[j + length] = z * (t - a[j + length]) % _Q
        length *= 2
    return [x * _N_INV % _Q for x in a]


def _unpack(data: bytes, bits: int) -> list[int]:
    """SimpleBitUnpack: 256 coefficients of ``bits`` bits each, packed little-endian (Algorithm 18)."""
    v = int.from_bytes(data, "little")
    mask = (1 << bits) - 1
    return [(v >> (i * bits)) & mask for i in range(256)]


def _rej_ntt_poly(seed: bytes) -> list[int]:
    """Algorithm 30: a polynomial in the NTT domain sampled from SHAKE128 by rejection."""
    n = 3 * 280
    while True:
        stream = hashlib.shake_128(seed).digest(n)
        out = []
        for i in range(0, n - 2, 3):
            z = stream[i] | (stream[i + 1] << 8) | ((stream[i + 2] & 0x7F) << 16)
            if z < _Q:
                out.append(z)
                if len(out) == 256:
                    return out
        n += 3 * 64  # rare: the first bytes did not give 256 coefficients; the SHAKE stream continues


def _sample_in_ball(seed: bytes) -> list[int]:
    """Algorithm 29: the challenge polynomial with tau coefficients +-1, from SHAKE256 of c-tilde."""
    n = 8 + 256
    while True:
        stream = hashlib.shake_256(seed).digest(n)
        signs = int.from_bytes(stream[:8], "little")
        c = [0] * 256
        pos = 8
        for i in range(256 - _TAU, 256):
            while pos < n and stream[pos] > i:
                pos += 1
            if pos >= n:
                break
            j = stream[pos]
            pos += 1
            c[i] = c[j]
            c[j] = -1 if (signs >> (i + _TAU - 256)) & 1 else 1
        else:
            return c
        n += 256


def _use_hint(h: int, r: int) -> int:
    """Algorithms 36 and 40 for gamma2 = (q - 1) / 32."""
    r %= _Q
    r0 = r % (2 * _GAMMA2)
    if r0 > _GAMMA2:
        r0 -= 2 * _GAMMA2
    if r - r0 == _Q - 1:
        r1, r0 = 0, r0 - 1
    else:
        r1 = (r - r0) // (2 * _GAMMA2)
    if not h:
        return r1
    return (r1 + 1) % 16 if r0 > 0 else (r1 - 1) % 16


def _hint_unpack(y: bytes):
    """Algorithm 21; None when the encoding is malformed."""
    h = [[0] * 256 for _ in range(_K)]
    index = 0
    for i in range(_K):
        end = y[_OMEGA + i]
        if end < index or end > _OMEGA:
            return None
        first = index
        while index < end:
            if index > first and y[index - 1] >= y[index]:
                return None
            h[i][y[index]] = 1
            index += 1
    if any(y[i] for i in range(index, _OMEGA)):
        return None
    return h


def _mldsa65_verify_internal(pk: bytes, m_prime: bytes, sig: bytes) -> bool:
    """Algorithm 8, ML-DSA.Verify_internal, for ML-DSA-65."""
    if len(pk) != _PK_LEN or len(sig) != _SIG_LEN:
        return False
    rho = pk[:32]
    t1 = [_unpack(pk[32 + 320 * i:32 + 320 * (i + 1)], 10) for i in range(_K)]
    c_tilde = sig[:_CTILDE]
    z = [[_GAMMA1 - v for v in _unpack(sig[_CTILDE + 640 * s:_CTILDE + 640 * (s + 1)], 20)] for s in range(_LCOLS)]
    h = _hint_unpack(sig[_CTILDE + 640 * _LCOLS:])
    if h is None:
        return False
    if max(abs(v) for poly in z for v in poly) >= _GAMMA1 - _BETA:
        return False
    mu = hashlib.shake_256(hashlib.shake_256(pk).digest(64) + m_prime).digest(64)
    c_hat = _ntt([x % _Q for x in _sample_in_ball(c_tilde)])
    z_hat = [_ntt([x % _Q for x in poly]) for poly in z]
    w1 = bytearray()
    for r in range(_K):
        t1_hat = _ntt([(x << 13) % _Q for x in t1[r]])
        acc = [0] * 256
        for s in range(_LCOLS):
            a = _rej_ntt_poly(rho + bytes([s, r]))  # ExpandA, Algorithm 32: row r, column s
            zs = z_hat[s]
            for i in range(256):
                acc[i] += a[i] * zs[i]
        w = _intt([(acc[i] - c_hat[i] * t1_hat[i]) % _Q for i in range(256)])
        packed = 0
        for i in range(256):
            packed |= _use_hint(h[r][i], w[i]) << (4 * i)
        w1 += packed.to_bytes(128, "little")  # w1Encode, Algorithm 28
    return hashlib.shake_256(mu + bytes(w1)).digest(_CTILDE) == c_tilde


def mldsa65_verify_pure(pk: bytes, msg: bytes, sig: bytes, ctx: bytes = b"") -> bool:
    """Algorithm 3, ML-DSA.Verify (pure ML-DSA, with a context string of at most 255 bytes)."""
    if len(ctx) > 255:
        return False
    return _mldsa65_verify_internal(pk, bytes([0, len(ctx)]) + ctx + msg, sig)


def _mldsa_raw_from_pem(pem: str) -> bytes:
    der = _pem_der(pem)
    if len(der) != len(_MLDSA65_SPKI) + _PK_LEN or not der.startswith(_MLDSA65_SPKI):
        raise ValueError("not an ML-DSA-65 public key")
    return der[len(_MLDSA65_SPKI):]


def _mldsa65_verify_library(pub_pem: str, msg: bytes, sig: bytes, ctx: bytes):
    """True/False with the installed `cryptography`, or None when it has no ML-DSA."""
    try:
        from cryptography.exceptions import InvalidSignature, UnsupportedAlgorithm
        from cryptography.hazmat.primitives.asymmetric.mldsa import MLDSA65PublicKey
        from cryptography.hazmat.primitives.serialization import load_pem_public_key
    except Exception:
        return None
    try:
        key = load_pem_public_key(pub_pem.encode())
    except UnsupportedAlgorithm:
        return None
    except Exception:
        return False
    if not isinstance(key, MLDSA65PublicKey):
        return False
    try:
        key.verify(sig, msg, ctx)
        return True
    except InvalidSignature:
        return False
    except UnsupportedAlgorithm:
        return None
    except Exception:
        return False


def mldsa65_verify(pub_pem: str, msg: bytes, sig: bytes, ctx: bytes) -> tuple[bool, str]:
    pure = mldsa65_verify_pure(_mldsa_raw_from_pem(pub_pem), msg, sig, ctx)
    lib = _mldsa65_verify_library(pub_pem, msg, sig, ctx)
    if lib is None:
        return pure, "built-in"
    if lib != pure:
        return False, f"IMPLEMENTATIONS DISAGREE (built-in={pure}, cryptography={lib})"
    return pure, "built-in + cryptography"


# ---------------------------------------------------------------- bundle checks


def _sha256(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _only_line_endings(path: pathlib.Path, want: str) -> bool:
    """The file hashes to the signed value once CRLF is turned back into LF: a checkout rewrote its line endings."""
    data = path.read_bytes()
    return b"\r\n" in data and hashlib.sha256(data.replace(b"\r\n", b"\n")).hexdigest() == want


CRLF_HINT = ("only its line endings differ: this checkout turned LF into CRLF (Git's core.autocrlf). Clone again with "
             "the repository's .gitattributes in effect, or with: git clone -c core.autocrlf=false ...")


def _check_pq(name: str, doc: dict, payload: dict, root_pq_pem: str | None) -> list[str]:
    """The ML-DSA-65 co-signature of a signature file whose payload names a post-quantum key, or carries one."""
    named, pq = payload.get("pq_key_id"), doc.get("pq")
    if named and not isinstance(pq, dict):
        return [f"{name}: the payload names ML-DSA-65 key {named}, but the post-quantum signature is missing"]
    if not named:
        return [f"{name}: a post-quantum signature that the signed payload does not name (no pq_key_id)"]
    if pq.get("algorithm") != "ML-DSA-65":
        return [f"{name}: unexpected post-quantum algorithm {pq.get('algorithm')!r}"]
    errs: list[str] = []
    schema = payload.get("schema", "")
    if pq.get("context") != schema:
        errs.append(f"{name}: the ML-DSA-65 signature was made for {pq.get('context')!r}, not {schema!r}")
    try:
        raw = _mldsa_raw_from_pem(pq.get("public_key_pem", ""))
    except Exception as exc:
        return errs + [f"{name}: post-quantum key: {exc}"]
    fp = hashlib.sha256(raw).hexdigest()
    if fp[:16] != named:
        errs.append(f"{name}: the ML-DSA-65 key is not the one the payload names ({fp[:16]} != {named})")
    if pq.get("key_fingerprint_sha256") and pq["key_fingerprint_sha256"] != fp:
        errs.append(f"{name}: the ML-DSA-65 key_fingerprint_sha256 does not match the embedded key")
    if root_pq_pem is not None and raw != _mldsa_raw_from_pem(root_pq_pem):
        errs.append(f"{name}: co-signed with a different ML-DSA-65 key than PUBLIC-KEY-MLDSA.pem at the repository root")
    try:
        sig = base64.b64decode(pq.get("signature", ""))
    except Exception:
        return errs + [f"{name}: the ML-DSA-65 signature is not base64"]
    ok, how = mldsa65_verify(pq["public_key_pem"], doc["payload"].encode(), sig, schema.encode())
    if not ok:
        errs.append(f"{name}: ML-DSA-65 signature does NOT verify ({how})")
    return errs


def _check_signature(sig_path: pathlib.Path, root_pem: str | None,
                     root_pq_pem: str | None = None) -> tuple[dict, list[str], bool]:
    """(payload, problems, whether an ML-DSA-65 co-signature was checked)."""
    errs: list[str] = []
    doc = json.loads(sig_path.read_text(encoding="utf-8"))
    for field in ("algorithm", "public_key_pem", "payload", "signature"):
        if field not in doc:
            errs.append(f"{sig_path.name}: missing field {field!r}")
    if errs:
        return {}, errs, False
    if doc["algorithm"] != "Ed25519":
        errs.append(f"{sig_path.name}: unexpected algorithm {doc['algorithm']!r}")
        return {}, errs, False

    ok, how = ed25519_verify(doc["public_key_pem"], doc["payload"].encode(), base64.b64decode(doc["signature"]))
    if not ok:
        errs.append(f"{sig_path.name}: signature does NOT verify ({how})")

    # The fingerprint the file states must be the key the file carries.
    want = doc.get("key_fingerprint_sha256")
    got = hashlib.sha256(_raw_from_pem(doc["public_key_pem"])).hexdigest()
    if want and want != got:
        errs.append(f"{sig_path.name}: key_fingerprint_sha256 does not match the embedded key")

    if root_pem is not None and _raw_from_pem(doc["public_key_pem"]) != _raw_from_pem(root_pem):
        errs.append(f"{sig_path.name}: signed with a different key than PUBLIC-KEY.pem at the repository root")

    payload = json.loads(doc["payload"])
    pq = bool(payload.get("pq_key_id") or doc.get("pq"))
    if pq:
        errs += _check_pq(sig_path.name, doc, payload, root_pq_pem)
    return payload, errs, pq


def verify_bundle(d: pathlib.Path, root_pem: str | None, root_pq_pem: str | None = None) -> tuple[list[str], bool]:
    """(problems, whether both signature files carry a verified ML-DSA-65 co-signature)."""
    errs: list[str] = []
    bsig = d / "bundle.sig.json"
    if not bsig.exists():
        return [f"{d.name}: no bundle.sig.json"], False

    payload, e, bundle_pq = _check_signature(bsig, root_pem, root_pq_pem)
    errs += e
    if not payload:
        return errs, False

    files = payload.get("files_sha256") or {}
    if not files:
        errs.append(f"{d.name}: the signed payload lists no files")
    for name, want in sorted(files.items()):
        f = d / name
        if not f.exists():
            errs.append(f"{d.name}/{name}: listed in the signature but missing")
            continue
        got = _sha256(f)
        if got != want:
            hint = f" — {CRLF_HINT}" if _only_line_endings(f, want) else ""
            errs.append(f"{d.name}/{name}: sha256 {got[:16]}… != signed {want[:16]}…{hint}")

    # The bundle's own copy of the key must be the key that signed it.
    pem_file = d / "public_key.pem"
    if pem_file.exists():
        if _raw_from_pem(pem_file.read_text(encoding="utf-8")) != _raw_from_pem(json.loads(bsig.read_text(encoding="utf-8"))["public_key_pem"]):
            errs.append(f"{d.name}: public_key.pem is not the key that signed the bundle")
    else:
        errs.append(f"{d.name}: public_key.pem missing")

    pq_file = d / "public_key_mldsa.pem"
    if pq_file.exists():
        block = json.loads(bsig.read_text(encoding="utf-8")).get("pq") or {}
        try:
            same = _mldsa_raw_from_pem(pq_file.read_text(encoding="utf-8")) == _mldsa_raw_from_pem(block.get("public_key_pem", ""))
        except Exception:
            same = False
        if not same:
            errs.append(f"{d.name}: public_key_mldsa.pem is not the ML-DSA-65 key that co-signed the bundle")

    report_pq = False
    rsig = d / "report.sig.json"
    if rsig.exists():
        rpayload, e, report_pq = _check_signature(rsig, root_pem, root_pq_pem)
        errs += e
        rjson = d / "report.json"
        if rpayload and rjson.exists():
            stated = json.loads(rjson.read_text(encoding="utf-8")).get("content_sha256")
            signed = rpayload.get("content_sha256")
            if stated and signed and not signed.startswith(stated) and not stated.startswith(signed):
                errs.append(f"{d.name}: report.json content_sha256 disagrees with the signed value")
    else:
        errs.append(f"{d.name}: report.sig.json missing")

    return errs, bundle_pq and report_pq and not errs


# ---------------------------------------------------------------- self-test

def _flip(b: bytes, at: int) -> bytes:
    out = bytearray(b)
    out[at] ^= 0x01
    return bytes(out)


def _self_test_mldsa(root: pathlib.Path, bundles: list[pathlib.Path]) -> bool:
    passed = True
    kat = root / "mldsa65-kat.json"
    if kat.exists():
        vectors = json.loads(kat.read_text(encoding="utf-8"))["tests"]
        right = [mldsa65_verify_pure(bytes.fromhex(t["pk"]), bytes.fromhex(t["message"]), bytes.fromhex(t["signature"]),
                                     bytes.fromhex(t["context"])) == t["testPassed"] for t in vectors]
        good = sum(t["testPassed"] for t in vectors)
        print(f"  ML-DSA-65: NIST test vectors ..... {'OK' if all(right) else 'FAIL'}   "
              f"({sum(right)} of {len(vectors)} give the expected answer: {good} valid, {len(vectors) - good} tampered)")
        passed = passed and all(right)
    else:
        print("  ML-DSA-65: NIST test vectors ..... skipped, mldsa65-kat.json is not next to verify.py")

    try:
        from cryptography.hazmat.primitives import serialization
        from cryptography.hazmat.primitives.asymmetric.mldsa import MLDSA65PrivateKey

        key = MLDSA65PrivateKey.generate()
        msg, ctx = b"qsi verify.py self-test", b"qsi.bundle-signature/1"
        sig = key.sign(msg, ctx)
        pem = key.public_key().public_bytes(serialization.Encoding.PEM,
                                            serialization.PublicFormat.SubjectPublicKeyInfo).decode()
    except Exception:
        print("  ML-DSA-65: cross-check ........... skipped, `cryptography` with ML-DSA is not installed")
    else:
        ok, how = mldsa65_verify(pem, msg, sig, ctx)
        print(f"  ML-DSA-65: a fresh signature ..... {'OK' if ok else 'FAIL'}   ({how})")
        passed = passed and ok and how == "built-in + cryptography"
        caught = not any(mldsa65_verify(pem, m, s, c)[0] for m, s, c in
                         ((_flip(msg, 3), sig, ctx), (msg, _flip(sig, 0), ctx), (msg, _flip(sig, 2000), ctx),
                          (msg, sig, b"qsi.report-signature/1")))
        print(f"  ML-DSA-65: tampering caught ...... {'OK' if caught else 'FAIL'}   (message, c-tilde, z, context)")
        passed = passed and caught

    real = [b for b in bundles if "pq" in json.loads((b / "bundle.sig.json").read_text(encoding="utf-8"))]
    if real:
        doc = json.loads((real[0] / "bundle.sig.json").read_text(encoding="utf-8"))
        ok, how = mldsa65_verify(doc["pq"]["public_key_pem"], doc["payload"].encode(),
                                 base64.b64decode(doc["pq"]["signature"]), json.loads(doc["payload"])["schema"].encode())
        print(f"  ML-DSA-65: a real co-signature ... {'OK' if ok else 'FAIL'}   ({real[0].name}, {how})")
        passed = passed and ok
    else:
        print("  ML-DSA-65: a real co-signature ... none yet among the bundles here (all were signed before 13 November 2026)")
    return passed


def self_test(root: pathlib.Path) -> int:
    print("self-test: the verifier, before you trust what it says about the bundles\n")
    bundles = sorted(p.parent for p in (root / "audits").glob("*/bundle.sig.json"))
    if not bundles:
        print("  no bundles found under audits/ — nothing to test against")
        return 1
    doc = json.loads((bundles[0] / "bundle.sig.json").read_text(encoding="utf-8"))
    pem, payload, sig = doc["public_key_pem"], doc["payload"].encode(), base64.b64decode(doc["signature"])

    ok, how = ed25519_verify(pem, payload, sig)
    print(f"  a real signature verifies ........ {'OK' if ok else 'FAIL'}   ({how})")
    passed = ok

    lib = _ed25519_verify_library(pem, payload, sig)
    if lib is None:
        print("  cross-check ...................... skipped, `cryptography` is not installed")
    else:
        agree = lib == _ed25519_verify_pure(_raw_from_pem(pem), payload, sig)
        print(f"  both implementations agree ....... {'OK' if agree else 'FAIL'}")
        passed = passed and agree

    r, _ = ed25519_verify(pem, _flip(payload, len(payload) // 2), sig)
    print(f"  one flipped payload byte caught .. {'OK' if not r else 'FAIL'}")
    passed = passed and not r

    r, _ = ed25519_verify(pem, payload, _flip(sig, 0))
    print(f"  one flipped signature byte caught  {'OK' if not r else 'FAIL'}")
    passed = passed and not r

    other = base64.b64decode(
        "".join(l for l in """-----BEGIN PUBLIC KEY-----
MCowBQYDK2VwAyEA11qYAYKxCrfVS/7TyWQHOg7hcvPapiMlrwIaaPcHURo=
-----END PUBLIC KEY-----""".splitlines() if "-----" not in l)
    )
    r = _ed25519_verify_pure(other[-32:], payload, sig)
    print(f"  a different key is rejected ...... {'OK' if not r else 'FAIL'}")
    passed = passed and not r

    passed = _self_test_mldsa(root, bundles) and passed

    print("\nself-test " + ("passed" if passed else "FAILED"))
    return 0 if passed else 1


def main(argv: list[str]) -> int:
    root = pathlib.Path(__file__).resolve().parent
    args = [a for a in argv[1:] if not a.startswith("-")]
    if "--self-test" in argv[1:]:
        return self_test(root)

    root_pem_path = root / "PUBLIC-KEY.pem"
    root_pem = root_pem_path.read_text(encoding="utf-8") if root_pem_path.exists() else None
    if root_pem is None:
        print("note: PUBLIC-KEY.pem is not at the repository root, so bundles are only checked against")
        print("      the key each one carries. Compare that key across bundles yourself.\n")
    root_pq_path = root / "PUBLIC-KEY-MLDSA.pem"
    root_pq_pem = root_pq_path.read_text(encoding="utf-8") if root_pq_path.exists() else None

    targets = [pathlib.Path(a) for a in args] or sorted(
        p.parent for p in (root / "audits").glob("*/bundle.sig.json")
    )
    if not targets:
        print("nothing to verify: pass a bundle directory, or run from a checkout containing audits/")
        return 1

    failed = pq = 0
    for d in targets:
        errs, co_signed = verify_bundle(d, root_pem, root_pq_pem)
        if errs:
            failed += 1
            print(f"FAIL  {d.name}")
            for e in errs:
                print(f"        {e}")
        else:
            pq += co_signed
            print(f"OK    {d.name}" + ("   [+ ML-DSA-65]" if co_signed else ""))

    print(f"\n{len(targets) - failed} verified, {failed} failed")
    if pq:
        print(f"{pq} of them also carry a verified ML-DSA-65 co-signature"
              + ("" if root_pq_pem else " (no PUBLIC-KEY-MLDSA.pem at the root: checked against the key each one names)"))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
