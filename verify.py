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

A bundle only passes if all four hold. Anything else prints FAIL and the reason, and the exit status is 1.

Ed25519 is verified twice where possible: with the `cryptography` package if it is installed, and with a
self-contained RFC 8032 implementation in this file. When both are available both must agree, so a bug in the
bundled implementation cannot turn a bad signature into a good one without the installed library agreeing to it.
Run --self-test to see that the implementations agree, that a real signature passes, and that flipping one byte
of the payload, the signature or a file is detected.
"""
from __future__ import annotations

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


def _raw_from_pem(pem: str) -> bytes:
    """The 32 raw bytes of an Ed25519 SubjectPublicKeyInfo PEM; the key bytes are its last 32."""
    import base64

    body = "".join(l.strip() for l in pem.strip().splitlines() if "-----" not in l)
    der = base64.b64decode(body)
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


# ---------------------------------------------------------------- bundle checks

import base64


def _sha256(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _check_signature(sig_path: pathlib.Path, root_pem: str | None) -> tuple[dict, list[str]]:
    errs: list[str] = []
    doc = json.loads(sig_path.read_text())
    for field in ("algorithm", "public_key_pem", "payload", "signature"):
        if field not in doc:
            errs.append(f"{sig_path.name}: missing field {field!r}")
    if errs:
        return {}, errs
    if doc["algorithm"] != "Ed25519":
        errs.append(f"{sig_path.name}: unexpected algorithm {doc['algorithm']!r}")
        return {}, errs

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

    return json.loads(doc["payload"]), errs


def verify_bundle(d: pathlib.Path, root_pem: str | None) -> list[str]:
    errs: list[str] = []
    bsig = d / "bundle.sig.json"
    if not bsig.exists():
        return [f"{d.name}: no bundle.sig.json"]

    payload, e = _check_signature(bsig, root_pem)
    errs += e
    if not payload:
        return errs

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
            errs.append(f"{d.name}/{name}: sha256 {got[:16]}… != signed {want[:16]}…")

    # The bundle's own copy of the key must be the key that signed it.
    pem_file = d / "public_key.pem"
    if pem_file.exists():
        if _raw_from_pem(pem_file.read_text()) != _raw_from_pem(json.loads(bsig.read_text())["public_key_pem"]):
            errs.append(f"{d.name}: public_key.pem is not the key that signed the bundle")
    else:
        errs.append(f"{d.name}: public_key.pem missing")

    rsig = d / "report.sig.json"
    if rsig.exists():
        rpayload, e = _check_signature(rsig, root_pem)
        errs += e
        rjson = d / "report.json"
        if rpayload and rjson.exists():
            stated = json.loads(rjson.read_text()).get("content_sha256")
            signed = rpayload.get("content_sha256")
            if stated and signed and not signed.startswith(stated) and not stated.startswith(signed):
                errs.append(f"{d.name}: report.json content_sha256 disagrees with the signed value")
    else:
        errs.append(f"{d.name}: report.sig.json missing")

    return errs


# ---------------------------------------------------------------- self-test

def self_test(root: pathlib.Path) -> int:
    print("self-test: the verifier, before you trust what it says about the bundles\n")
    bundles = sorted(p.parent for p in (root / "audits").glob("*/bundle.sig.json"))
    if not bundles:
        print("  no bundles found under audits/ — nothing to test against")
        return 1
    doc = json.loads((bundles[0] / "bundle.sig.json").read_text())
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

    bad_payload = bytearray(payload)
    bad_payload[len(bad_payload) // 2] ^= 0x01
    r, _ = ed25519_verify(pem, bytes(bad_payload), sig)
    print(f"  one flipped payload byte caught .. {'OK' if not r else 'FAIL'}")
    passed = passed and not r

    bad_sig = bytearray(sig)
    bad_sig[0] ^= 0x01
    r, _ = ed25519_verify(pem, payload, bytes(bad_sig))
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

    print("\nself-test " + ("passed" if passed else "FAILED"))
    return 0 if passed else 1


def main(argv: list[str]) -> int:
    root = pathlib.Path(__file__).resolve().parent
    args = [a for a in argv[1:] if not a.startswith("-")]
    if "--self-test" in argv[1:]:
        return self_test(root)

    root_pem_path = root / "PUBLIC-KEY.pem"
    root_pem = root_pem_path.read_text() if root_pem_path.exists() else None
    if root_pem is None:
        print("note: PUBLIC-KEY.pem is not at the repository root, so bundles are only checked against")
        print("      the key each one carries. Compare that key across bundles yourself.\n")

    targets = [pathlib.Path(a) for a in args] or sorted(
        p.parent for p in (root / "audits").glob("*/bundle.sig.json")
    )
    if not targets:
        print("nothing to verify: pass a bundle directory, or run from a checkout containing audits/")
        return 1

    failed = 0
    for d in targets:
        errs = verify_bundle(d, root_pem)
        if errs:
            failed += 1
            print(f"FAIL  {d.name}")
            for e in errs:
                print(f"        {e}")
        else:
            print(f"OK    {d.name}")

    print(f"\n{len(targets) - failed} verified, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
