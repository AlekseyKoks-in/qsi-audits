# XRP Ledger: what still signs or encrypts on elliptic curves, read from the code (2026-11-21)

XRPL-Standards [discussion 295](https://github.com/XRPLF/XRPL-Standards/discussions/295) proposes a `dilithium` key
type (ML-DSA-44, FIPS 204) under a `Quantum` amendment. A summary of this inventory was posted there on 21 November
2026; this report is the evidence behind it. The eight signed bundles (report, CycloneDX CBOM, SARIF) are in
`studies/xrpl/<name>/`, kept apart from the portfolio totals in the README, and verifiable offline:

```
python3 verify.py studies/xrpl/*
```

All eight carry the Ed25519 signature and the ML-DSA-65 co-signature of the keys at the repository root.

This is not a vulnerability report. It answers one question at pinned commits: which parts of the XRP Ledger stack
rely on cryptography that a quantum computer breaks, and what the proposal does not cover yet.

## The bundles

| Bundle | Repository @ commit | Files | Inventory rows | Shor-breakable | Post-quantum | Findings: crit / high / med / low / info |
|---|---|---:|---:|---:|---:|---|
| `xrpl-rippled` | XRPLF/rippled `develop` @ `82217fb` | 1246 | 37 | 36 | 0 | 0 / 0 / 5 / 2 / 0 |
| `xrpl-rippled-quantum` | XRPLF/rippled `xrplf/quantum` @ `816e5b6` | 1258 | 51 | 37 | 13 | 0 / 0 / 5 / 2 / 0 |
| `xrpl-js` | XRPLF/xrpl.js @ `1261682` | 377 | 44 | 29 | 0 | 0 / 0 / 4 / 3 / 2 |
| `xrpl-py` | XRPLF/xrpl-py @ `d15d5a0` | 295 | 38 | 32 | 0 | 0 / 0 / 3 / 4 / 1 |
| `xrpl4j` | XRPLF/xrpl4j @ `bbbd620` | 645 | 22 | 16 | 0 | 0 / 0 / 5 / 1 / 1 |
| `xrpl-go` | XRPLF/xrpl-go @ `23275f0` | 514 | 39 | 30 | 0 | 0 / 0 / 4 / 4 / 2 |
| `xrpl-validator-keys-tool` | ripple/validator-keys-tool @ `4c0fb75` | 4 | 2 | 2 | 0 | 0 / 0 / 2 / 0 / 0 |
| `xrpl-ledger-app-xrp` | LedgerHQ/app-xrp @ `7b5185f` | 61 | 8 | 8 | 0 | 0 / 0 / 4 / 0 / 0 |
| **Total** | | **4,400** | **241** | **190** | **13** | 0 / 0 / 32 / 16 / 6 |

Nothing here is critical or high. The medium findings are quantum-vulnerable signatures (ECDSA, Ed25519) and
Pedersen commitments, grouped by the role QSI infers from the surrounding code, and preliminary until read. Of the
16 low ones, 12 are EC-ElGamal, 2 are the RSA key rippled generates for its TLS context
(`src/libxrpl/basics/make_SSLContext.cpp`, `RSA_generate_key_ex`), and 2 are listed under "Other findings" below.
The info ones say that no post-quantum capable library was detected (four SDKs) or sum up advisories in
development-only packages (two). A bundle's inventory also counts dependency manifests and vendored third-party code
(tests are excluded), so it is slightly larger than the production-only figures further down.

## What the code shows

1. **Confidential MPTs stay exposed after the signature migration.** XLS-0096 (Final) keeps each holder's balance,
   the issuer's mirror and an optional auditor's copy on the ledger as EC-ElGamal ciphertexts on secp256k1 (66
   bytes each), next to 33-byte encryption keys. Whoever first recovers one of those secret keys with a quantum
   computer can decrypt every amount ever encrypted to it, so ciphertexts written today are readable later, and
   moving account and validator signatures to ML-DSA does not change that. The code is already in rippled `develop`
   (`src/libxrpl/protocol/ConfidentialTransfer.cpp`, `secp256k1_elgamal_add`) and in all four SDKs through
   mpt-crypto: cffi in xrpl-py (`xrpl/ext/confidential/`), cgo in xrpl-go (`confidential/mptcrypto/`), JNA in
   xrpl4j (`crypto/confidential/util/jna/`) and WebAssembly in xrpl.js (`packages/mpt-crypto/`). No NIST
   post-quantum standard covers additively homomorphic encryption, so this needs its own answer, at least a note in
   XLS-0096 that the confidentiality is time-limited, rather than a new key type. The Pedersen commitments beside
   the ciphertexts are a different case: they are perfectly hiding, so a quantum computer learns nothing from the
   ones already on the ledger; what it breaks is their binding, which matters for proofs made once it exists.
2. **Validator tooling.** On `xrplf/quantum`, rippled's `validation_create` accepts `KeyType::Dilithium`
   (`src/xrpld/rpc/handlers/admin/keygen/ValidationCreate.cpp:49`), but validator-keys-tool, which operators use for
   master keys and manifests, creates
   master keys as Ed25519 (`src/ValidatorKeysTool.cpp:64`, `ValidatorKeys const keys(KeyType::Ed25519);`) and tokens
   as secp256k1 by default (`src/ValidatorKeys.h:104`), and has no Dilithium key type.
3. **Clients.** At these commits xrpl-py, xrpl4j and xrpl-go have no post-quantum signer. ML-DSA-44 exists only on
   xrpl.js's `xrplf/quantum` branch (`ac94989`, measured below but not bundled), through `@noble/post-quantum`'s
   `ml_dsa44`. Ledger's XRP app signs with secp256k1 or Ed25519 through the BOLOS SDK
   (`src/apdu/messages/sign_transaction.c:110` `cx_ecdsa_sign_no_throw`, `:115` `cx_eddsa_sign_no_throw`), so
   hardware signing also depends on support in the device, not only in the app.
4. **The post-quantum branch.** The 13 post-quantum rows of `xrpl-rippled-quantum` are the ML-DSA code behind
   `KeyType::Dilithium` (`include/xrpl/protocol/KeyType.h`, `STValidation.h`, `src/libxrpl/protocol/PublicKey.cpp`),
   built as ML-DSA-44 (`DILITHIUM_MODE=2`, `pqcrystals_dilithium2_ref_*`) from the FIPS 204 reference code:
   `cmake/deps/dilithium.cmake` pins Transia-RnD/dilithium `3032292` and states that it is pq-crystals/dilithium
   `444cdcc` plus one commit that touches only `ref/Makefile`. The older Transia-RnD/rippled `quantum` branch
   (`8666c9a`) pins pq-crystals `v3.1` instead (`9dddb2a`, 23 February 2021): round-3 Dilithium, whose signatures
   do not verify as ML-DSA-44 although the sizes match. quantova-inc reported that branch in the same
   discussion on 9 November; this confirms it from the build files. The implementation links in the proposal's
   header (`XRPLF/rippled/tree/dilithium-full`, `XRPLF/xrpl.js/tree/dilithium`, `XRPLF/xrpld-publisher/tree/quantum`)
   did not resolve on 21 November.

## Production code only, before and after QSI learned the XRP Ledger's vocabulary

The first measurement missed half of this cryptography. A scanner with no word for a primitive reports it as absent
(see "does your scanner have a word for this cryptography?" in the README), and QSI lacked several:

- rippled's key types as libxrpl spells them after the `xrpl::` rename, `KeyType::Secp256k1` and `KeyType::Ed25519`:
  validator-keys-tool measured 0 rows, rippled 17;
- Ledger's BOLOS API (`cx_ecdsa_sign_no_throw`, `cx_eddsa_sign_no_throw`, `CX_CURVE_256K1`, `CX_CURVE_Ed25519`):
  the XRP app measured 0 rows;
- noble v2's import paths with a `.js` suffix (`'@noble/curves/ed25519.js'`, usually renamed): xrpl.js's default
  Ed25519 signer was not found, and the same applies to every JavaScript project on noble v2;
- the CRYSTALS reference API (`pqcrystals_dilithium{2,3,5}_*`) and `KeyType::Dilithium`: the post-quantum code on
  the `quantum` branches was invisible. QSI's ML-DSA entry now also warns that round-3 Dilithium is not ML-DSA;
- EC-ElGamal as an entry of its own: Confidential MPT ciphertexts had been filed under prime-field ElGamal with
  OpenPGP's deprecation note (RFC 9580), which was wrong. The entry now names the curve, the harvest-now-decrypt-later
  exposure and mpt-crypto's API (`mpt_encrypt_amount`, `secp256k1_elgamal_add`, ...), and Pedersen commitments
  (`mpt_get_pedersen_commitment`, `getPedersenCommitment`) are recognised;
- one false row removed: the pattern `[.:]idea\b` matched `'.idea/'`, JetBrains' folder in an ESLint
  configuration, so three xrpl.js packages "used the IDEA cipher".

Measured on production code (tests, examples and vendored libraries left out) of eleven repositories:

| Repository | Commit | Rows before → after | Shor-breakable before → after | Post-quantum after |
|---|---|---:|---:|---:|
| rippled (`develop`) | `82217fb` | 17 → 35 | 16 → 34 | 0 |
| rippled (`xrplf/quantum`) | `816e5b6` | 19 → 49 | 18 → 35 | 13 (ML-DSA-44) |
| xrpl.js | `1261682` | 14 → 26 | 10 → 25 | 0 |
| xrpl.js (`xrplf/quantum`), not bundled | `ac94989` | 15 → 27 | 10 → 25 | 1 (ML-DSA-44) |
| xrpl-py | `d15d5a0` | 28 → 35 | 25 → 32 | 0 |
| xrpl4j | `bbbd620` | 14 → 20 | 10 → 16 | 0 |
| xrpl-go | `23275f0` | 24 → 26 | 19 → 21 | 0 |
| validator-keys-tool | `4c0fb75` | 0 → 2 | 0 → 2 | 0 |
| Ledger app-xrp | `7b5185f` | 0 → 8 | 0 → 8 | 0 |
| Xaman, not published here | `cf63acd` | 15 → 15 | 10 → 10 | 0 |
| GemWallet, not published here | `fe27ea9` | 4 → 4 | 4 → 4 | 0 |
| **Total** | | **150 → 247** | **122 → 212** | **1 → 14** |

The nine mainline repositories (the two `xrplf/quantum` branches share most of their code with `develop` and
`main`) hold 171 rows, 152 of them Shor-breakable: 68 secp256k1 ECDSA, 29 EC-ElGamal (in five repositories), 21
Ed25519 (in eight), 19 Pedersen commitments, 12 ECDSA with no curve named, 2 RSA and 1 P-256. None is post-quantum.
The two wallets were measured for the discussion and are not part of this publication, so those two rows cannot be
checked against a bundle here.

## Other findings

- `xrpl-js`: a 4096-bit RSA OpenPGP key committed in `packages/ripple-keypairs/SECURITY.md` (low), the key for
  vulnerability reports; it is in the inventory as an OpenPGP primary key and subkey, not as code. Also 23
  advisories in six development or build-only npm packages (info).
- `xrpl-go`: `golang.org/x/crypto` v0.56.0 is affected by GO-2026-5932 (low, no severity rating): the
  `golang.org/x/crypto/openpgp` package is unmaintained; the advisory names no affected functions, so reachability
  was not determined. Also one advisory in a development-only npm package (info).

## False findings removed before publication

The first issue of these bundles (QSI engine 1.8.0) carried false findings. Each was fixed in QSI with a test, and
the bundles here were issued again with engine 1.8.1: configuration names in rippled (`kValidatorToken`,
`kAdminPassword`, `kPassword`) and the result code `tesSUCCESS` had been reported as secrets, and an advisory in
`webpack-dev-middleware`, used only by xrpl-go's documentation site, had been reported against the library.

## Limits

- Static analysis of the source at the commits named; nothing was sent to anyone's systems, no network was probed,
  and reachability is not analysed.
- Roles are inferred from the code around each call, and the findings say "preliminary" until read. Pedersen
  commitments carry the role "threshold signing and MPC protocols", the nearest QSI has; in XLS-0096 they commit
  to confidential amounts.
- Seven EC-ElGamal mentions are still written as plain "ElGamal" (five in `xrpl-py`, two in `xrpl-go`): docstrings
  of the models, error texts, and a Go file named `elgamal.go` (`confidential/elgamal/`), in files that make no
  EC-ElGamal call. By meaning they are XLS-0096's EC-ElGamal.
- Recall outside these repositories is not measured.

To list every EC-ElGamal row of one bundle with nothing but Python:

```
python3 -c "import json,sys; [print(r['algorithm'], r['location']) for r in json.load(open(sys.argv[1]))['inventory'] if 'ElGamal' in r['algorithm']]" studies/xrpl/xrpl-rippled/report.json
```
