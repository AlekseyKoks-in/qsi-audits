# Security & Post-Quantum Readiness Audit Report

**Project:** xrpl-py @ d15d5a0f42b2 · XRPL Foundation — public repository (passive review)
| | |
|---|---|
| Organization | QSI |
| Report date | 2026-11-23 14:07 UTC |
| Report version | 1 |
| Audit run | bee15ec0-32dd-4874-98ca-03c5eb8c1790 (Document audit) |
| Analyzer engine | qsi-engine 1.16.2 |
| Risk profile | Web3 project |
| Content SHA-256 | `e10b7694243366a25db9dcb7510f8bdb2f6b4f4877941eef9ce81fc845fc1320` |
| Signature key (Ed25519 SHA-256 fingerprint, then the ML-DSA-65 one where it co-signs; the signature is the separate file report.sig.json) | `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e · ML-DSA-65 dbd4e297b3213d1d7577a565e76de14cc5ad0e409f1dc68291c67266fc95066a` |
> This report presents automated and documented analysis results for the stated scope. It is not a legal opinion, a certification or an attestation of compliance with any standard.

## 1. Executive summary

- Critical: **0**
- High: **0**
- Medium: **3**
- Low: **4**
- Info: **1**

- Confirmed technical vulnerability: 0
- Known vulnerable component: 0
- Confirmed configuration error: 0
- Potential cryptographic risk: 0
- Long-term post-quantum risk: 7
- Improvement recommendation: 0
- Insufficient data: 1

Mosca's inequality (x + y > z): x = 5, y = 5, z = 12 → tight margin. _z is a planning assumption chosen per risk profile, not a prediction. A cryptographically relevant quantum computer is not publicly known to exist today._

**Post-quantum maturity: Level 0 of 4 — no post-quantum cryptography.** Next step: Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

## 2. Scope and boundaries

Mode: Document audit

Repository: <https://github.com/XRPLF/xrpl-py> @ `d15d5a0f42b2c57a800dc8ad2c802ec3a899450f` — evidence links open the lines at this commit.

295 files, 1325114 bytes in total, 0 redaction(s); the per-file SHA-256 list is in appendix C.

## 3. Methodology

| Area | Status | Count | Examples |
|---|---|---|---|
| source_code | checked | 292 | docs/conf.py: 60 lines scanned with 16 rule patterns and 340 registry patterns; packaging/confidential/setup.py: 14 lines scanned with 16 rule patterns and 340 registry patterns; tools/generate_definitions.py: 376 lines scanned with 16 rule patterns and 340 registry patterns |
| dependencies | checked | 3 | packaging/confidential/pyproject.toml: 2 dependencies parsed (0 pinned); poetry.lock: 73 dependencies parsed (73 pinned); pyproject.toml: 8 dependencies parsed (0 pinned) |
| tls_key_exchange_groups | Insufficient data | 73 | poetry.lock line 9: not in the algorithm registry, not assessed: ["dev"]; poetry.lock line 24: not in the algorithm registry, not assessed: ["dev"]; poetry.lock line 36: not in the algorithm registry, not assessed: ["main"] |
| tls_configuration | checked | 1 | poetry.lock: openssl TLS directives parsed |
| entropy | checked | 1 | random-number generation: 292 code files read with 37 macro definitions from the tree; 0 ineffective guard(s), 0 weak random-bytes provider(s), 0 weak key-generation site(s) |
| crediting | checked | 1 | payment crediting: 56 file(s) read incoming transfers on TON, the XRP Ledger (Xaman sign requests included), Tron or an EVM chain, 0 credit from a Tron or EVM node; 0 lead(s). A wait for confirmations or finality is recognised by its words, not traced; reorganisations and duplicate crediting are not checked |
| osv_advisories | checked | 1 | 73 pinned packages queried at OSV.dev; 0 affected |

_Long lists are grouped here; the full per-file list is in the JSON report, signed with the same key._

## 4. Assets examined and not examined

- tls_key_exchange_groups — Insufficient data: 73 (examples: poetry.lock line 9: not in the algorithm registry, not assessed: ["dev"]; poetry.lock line 24: not in the algorithm registry, not assessed: ["dev"]; poetry.lock line 36: not in the algorithm registry, not assessed: ["main"])

## 5. Architecture overview

Static review of the source tree xrpl-py at d15d5a0f42b2c57a800dc8ad2c802ec3a899450f. 295 files analysed; of 664 files, 275 are test, fuzzing, benchmark or example code and were left out, 94 are not read by any analyzer, 0 exceed the per-file limit and 0 did not fit the total limit. Files no analyzer reads include: .claude/skills/batch-deps-upgrade/README.md, .claude/skills/batch-deps-upgrade/SKILL.md, .coderabbit.yaml, .flake8, .github/dependabot.yml. 30 files in build-output or dependency-cache directories (.git, .hg, .venv, __pycache__, build, dist, node_modules, target, vendor, venv) were not read. No requests were sent to the owner's systems.

## 6. Overall security posture

- Indicative posture index: **100** / 100 — _Derived from findings in scope (confirmed and potential issues weighted by severity). Indicative only; not comparable across differently scoped audits._
- Quantum-vulnerable share of inventory: 84.2%

## 7. Detailed findings

### QSI-2026-44390 — Quantum-vulnerable ECDSA: transaction and message signing (5 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:ECDSA:transaction_signing`
- Data source: xrpl/core/keypairs/secp256k1.py
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.16.2 · 2026-11-23 14:07 UTC
- Priority score: 33.0 / 100
- CVSS v3.1: not applicable

27 reference(s) to ECDSA across 5 file(s), e.g. xrpl/core/keypairs/secp256k1.py:1. Role, judged from paths, function names and nearby code: transaction and message signing. A CRQC derives the private key from a public key that is already known (on chain after the first spend, in reused addresses): funds and approvals controlled by these keys need a migration path.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open xrpl/core/keypairs/secp256k1.py:1 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [xrpl/core/keypairs/secp256k1.py](https://github.com/XRPLF/xrpl-py/blob/d15d5a0f42b2c57a800dc8ad2c802ec3a899450f/xrpl/core/keypairs/secp256k1.py#L1) · line 1 · SHA-256 ad17ce0087216bf5bd474b4e38f269553a5cb51c85184d951778526432e7b8b5_

```
    1 | """secp256k1 elliptic curve cryptography interface."""
    2 | 
```

_file_excerpt · [xrpl/core/keypairs/secp256k1.py](https://github.com/XRPLF/xrpl-py/blob/d15d5a0f42b2c57a800dc8ad2c802ec3a899450f/xrpl/core/keypairs/secp256k1.py#L21) · line 21 · SHA-256 816b4f2fc15a578f996488d0e4930970141d6563bc101134f6f6fdf917229edc_

```
   20 | 
   21 | _CURVE: Final[Curve] = Curve.get_curve("secp256k1")
   22 | _GROUP_ORDER: Final[int] = _CURVE.order
```

_file_excerpt · [xrpl/core/keypairs/secp256k1.py](https://github.com/XRPLF/xrpl-py/blob/d15d5a0f42b2c57a800dc8ad2c802ec3a899450f/xrpl/core/keypairs/secp256k1.py#L44) · line 44 · SHA-256 076fdde40abf3ebbbd87720a542b6a9e188e3499017afa0b07f73762b45b1ee2_

```
   43 |     """
   44 |     Methods for using the ECDSA cryptographic system with the secp256k1
   45 |     elliptic curve.
```

_file_excerpt · [xrpl/ext/confidential/include/secp256k1.h](https://github.com/XRPLF/xrpl-py/blob/d15d5a0f42b2c57a800dc8ad2c802ec3a899450f/xrpl/ext/confidential/include/secp256k1.h#L80) · line 80 · SHA-256 42167c95481f0ec667afe584926da67ba267ebabfdb19e05a7ad7e9be4e8fed6_

```
   79 |  */
   80 | typedef struct secp256k1_ecdsa_signature {
   81 |     unsigned char data[64];
```

_file_excerpt · [xrpl/ext/confidential/include/secp256k1.h](https://github.com/XRPLF/xrpl-py/blob/d15d5a0f42b2c57a800dc8ad2c802ec3a899450f/xrpl/ext/confidential/include/secp256k1.h#L82) · line 82 · SHA-256 cdc23e614da912f23027127abfb94599623f7f2a871a313ad6ed750216b9c3bf_

```
   81 |     unsigned char data[64];
   82 | } secp256k1_ecdsa_signature;
   83 | 
```

_file_excerpt · [xrpl/ext/confidential/include/secp256k1.h](https://github.com/XRPLF/xrpl-py/blob/d15d5a0f42b2c57a800dc8ad2c802ec3a899450f/xrpl/ext/confidential/include/secp256k1.h#L501) · line 501 · SHA-256 e6f24a8cc5a4511593d19ae7ed906bcd86fa9220a4b3e53183d5f428a55f9a7f_

```
  500 |  */
  501 | SECP256K1_API int secp256k1_ecdsa_signature_parse_compact(
  502 |     const secp256k1_context *ctx,
```

_file_excerpt · [xrpl/ext/confidential/include/secp256k1_mpt.h](https://github.com/XRPLF/xrpl-py/blob/d15d5a0f42b2c57a800dc8ad2c802ec3a899450f/xrpl/ext/confidential/include/secp256k1_mpt.h#L5) · line 5 · SHA-256 f6ef645d793b3aaed24e4d8730a5b857973e8dd66babfcc3739998ea5530bc25_

```
    4 | #include "mpt_protocol.h"
    5 | #include <secp256k1.h>
    6 | #include <stdint.h>
```

_file_excerpt · [xrpl/ext/confidential/transaction_builders.py](https://github.com/XRPLF/xrpl-py/blob/d15d5a0f42b2c57a800dc8ad2c802ec3a899450f/xrpl/ext/confidential/transaction_builders.py#L78) · line 78 · SHA-256 9b4acdedcd5c1ef2cb8ae58e692284757563158806be75f271aabf591e431141_

```
   77 | # ──────────────────────────────────────────────────────────────────────────────
   78 | _PUBKEY_HEX_LEN = 66  # 33-byte compressed secp256k1 public key
   79 | 
```

_file_excerpt · [xrpl/ext/confidential/transaction_builders.py](https://github.com/XRPLF/xrpl-py/blob/d15d5a0f42b2c57a800dc8ad2c802ec3a899450f/xrpl/ext/confidential/transaction_builders.py#L285) · line 285 · SHA-256 78460974ed6f685c3533cbb3c8b580e52fae8bab58fd80ea3e2d410701469d1d_

```
  284 |     Uses mpt_generate_blinding_factor, which validates the scalar against the
  285 |     secp256k1 curve order (unlike raw random bytes).
  286 | 
```

_file_excerpt · [xrpl/models/transactions/payment_channel_create.py](https://github.com/XRPLF/xrpl-py/blob/d15d5a0f42b2c57a800dc8ad2c802ec3a899450f/xrpl/models/transactions/payment_channel_create.py#L52) · line 52 · SHA-256 f29c5f0d80eeaa3228aa29af6ba699e9efd7d99d12cc28c85833bff806638662_

```
   51 |     claims against this  channel, as hexadecimal. This can be any valid
   52 |     secp256k1 or Ed25519 public key. This field is required.
   53 | 
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains adopt them.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-44392 — Quantum-vulnerable Pedersen commitment: threshold signing and MPC protocols (6 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:Pedersen commitment:threshold_mpc`
- Data source: xrpl/ext/confidential/build_mpt_crypto.py
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.16.2 · 2026-11-23 14:07 UTC
- Priority score: 33.0 / 100
- CVSS v3.1: not applicable

14 reference(s) to Pedersen commitment across 6 file(s), e.g. xrpl/ext/confidential/build_mpt_crypto.py:79. Role, judged from paths, function names and nearby code: threshold signing and MPC protocols. Paillier, Pedersen commitments and the discrete-logarithm proofs inside threshold ECDSA and EdDSA protocols all fall to Shor's algorithm; a post-quantum threshold scheme is a protocol change, not a parameter change.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open xrpl/ext/confidential/build_mpt_crypto.py:79 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [xrpl/ext/confidential/build_mpt_crypto.py](https://github.com/XRPLF/xrpl-py/blob/d15d5a0f42b2c57a800dc8ad2c802ec3a899450f/xrpl/ext/confidential/build_mpt_crypto.py#L79) · line 79 · SHA-256 1f3bdfa0d4a4b13a7bd043f12fab8ab7e74f2572df2aa81fed01e1d935891cfc_

```
   78 |     typedef struct {
   79 |         uint8_t pedersen_commitment[33];
   80 |         uint64_t amount;
```

_file_excerpt · [xrpl/ext/confidential/build_mpt_crypto.py](https://github.com/XRPLF/xrpl-py/blob/d15d5a0f42b2c57a800dc8ad2c802ec3a899450f/xrpl/ext/confidential/build_mpt_crypto.py#L119) · line 119 · SHA-256 2e21eae3911af7c5e54a3123b586138b37cb29ca03295ed7d3d44751af7602c6_

```
  118 |     );
  119 |     int mpt_get_pedersen_commitment(
  120 |         uint64_t amount,
```

_file_excerpt · [xrpl/ext/confidential/commitments.py](https://github.com/XRPLF/xrpl-py/blob/d15d5a0f42b2c57a800dc8ad2c802ec3a899450f/xrpl/ext/confidential/commitments.py#L22) · line 22 · SHA-256 8d238aa63ba4f324ee8e9052568301960e0ee80680e870493f492edadb488178_

```
   21 | 
   22 | def create_pedersen_commitment(amount: int, blinding_factor: str) -> str:
   23 |     """
```

_file_excerpt · [xrpl/ext/confidential/commitments.py](https://github.com/XRPLF/xrpl-py/blob/d15d5a0f42b2c57a800dc8ad2c802ec3a899450f/xrpl/ext/confidential/commitments.py#L40) · line 40 · SHA-256 b3634f4c5606c53512e130a7b308495f9674b00bd0324dfe55c78b796f60fb22_

```
   39 |     commitment = ffi.new("uint8_t[]", 33)
   40 |     result = lib.mpt_get_pedersen_commitment(amount, blinding_bytes, commitment)
   41 |     if result != 0:
```

_file_excerpt · [xrpl/ext/confidential/include/secp256k1_mpt.h](https://github.com/XRPLF/xrpl-py/blob/d15d5a0f42b2c57a800dc8ad2c802ec3a899450f/xrpl/ext/confidential/include/secp256k1_mpt.h#L231) · line 231 · SHA-256 d14025fc0f9047dce1e628444687577a59ac742a045f92182192614f0caf0e69_

```
  230 | int
  231 | secp256k1_mpt_pedersen_commit(
  232 |     secp256k1_context const* ctx,
```

_file_excerpt · [xrpl/ext/confidential/include/utility/mpt_utility.h](https://github.com/XRPLF/xrpl-py/blob/d15d5a0f42b2c57a800dc8ad2c802ec3a899450f/xrpl/ext/confidential/include/utility/mpt_utility.h#L54) · line 54 · SHA-256 e92263be3776aafe4d9bcfe1246553afc691e09d4dfcd504c1478e903b5b903a_

```
   53 | {
   54 |     uint8_t pedersen_commitment[kMPT_PEDERSEN_COMMIT_SIZE];
   55 |     uint64_t amount;
```

_file_excerpt · [xrpl/ext/confidential/include/utility/mpt_utility.h](https://github.com/XRPLF/xrpl-py/blob/d15d5a0f42b2c57a800dc8ad2c802ec3a899450f/xrpl/ext/confidential/include/utility/mpt_utility.h#L225) · line 225 · SHA-256 ee42899e04fd6668b6a7f270ecc73cd9b6b72c34ee1f8a26a9c452bf418793d1_

```
  224 | int
  225 | mpt_get_pedersen_commitment(
  226 |     uint64_t amount,
```

_file_excerpt · [xrpl/ext/confidential/main.py](https://github.com/XRPLF/xrpl-py/blob/d15d5a0f42b2c57a800dc8ad2c802ec3a899450f/xrpl/ext/confidential/main.py#L132) · line 132 · SHA-256 89b1bc0ff933312246133107fb4f385becb565f6d3967b359129a2fa93a62fc5_

```
  131 |     # Commitments and Bulletproofs
  132 |     def create_pedersen_commitment(
  133 |         self: Self, amount: int, blinding_factor: str
```

_file_excerpt · [xrpl/ext/confidential/main.py](https://github.com/XRPLF/xrpl-py/blob/d15d5a0f42b2c57a800dc8ad2c802ec3a899450f/xrpl/ext/confidential/main.py#L136) · line 136 · SHA-256 50c90f4b7835ae6299ebc2e2c9d1498155f13c893678aa6d08d05508aa6aa3d6_

```
  135 |         """Create a Pedersen commitment: PC = amount*G + blinding_factor*H"""
  136 |         return commitments.create_pedersen_commitment(amount, blinding_factor)
  137 | 
```

_file_excerpt · [xrpl/ext/confidential/main.py](https://github.com/XRPLF/xrpl-py/blob/d15d5a0f42b2c57a800dc8ad2c802ec3a899450f/xrpl/ext/confidential/main.py#L366) · line 366 · SHA-256 863df3efb124d3d395e94c4de9336a2feb1f3d8d00b3cb0a6b80aac253e503bb_

```
  365 |         ffi.memmove(
  366 |             balance_params.pedersen_commitment,
  367 |             _hex_to_fixed_bytes(balance_commitment, 33, "balance_commitment"),
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Track post-quantum threshold signatures (NIST IR 8214C) and keep the protocol layer ready to swap the signature scheme; record which keys and shares must stay valid for how long.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-44389 — Quantum-vulnerable ECDSA: role not determined (7 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:ECDSA:general`
- Data source: xrpl/constants.py
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.16.2 · 2026-11-23 14:07 UTC
- Priority score: 31.7 / 100
- CVSS v3.1: not applicable

8 reference(s) to ECDSA across 7 file(s), e.g. xrpl/constants.py:15. Role, judged from paths, function names and nearby code: role not determined. The code does not show what the keys protect; review decides the priority.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open xrpl/constants.py:15 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [xrpl/constants.py](https://github.com/XRPLF/xrpl-py/blob/d15d5a0f42b2c57a800dc8ad2c802ec3a899450f/xrpl/constants.py#L15) · line 15 · SHA-256 0476f98819d00936217e14afb5895ac5e8cda70ffc9d56bfcf178ad6338f4ee0_

```
   14 |     ED25519 = "ed25519"
   15 |     SECP256K1 = "secp256k1"
   16 | 
```

_file_excerpt · [xrpl/core/keypairs/main.py](https://github.com/XRPLF/xrpl-py/blob/d15d5a0f42b2c57a800dc8ad2c802ec3a899450f/xrpl/core/keypairs/main.py#L15) · line 15 · SHA-256 f6551be801defa68f608582f4f35a8344c9acd8ef313d52b36a772c2b255132e_

```
   14 | from xrpl.core.keypairs.helpers import get_account_id
   15 | from xrpl.core.keypairs.secp256k1 import SECP256K1
   16 | 
```

_file_excerpt · [xrpl/ext/confidential/build_mpt_crypto.py](https://github.com/XRPLF/xrpl-py/blob/d15d5a0f42b2c57a800dc8ad2c802ec3a899450f/xrpl/ext/confidential/build_mpt_crypto.py#L311) · line 311 · SHA-256 119d8ed595c2ec5bd15f9bcc0da41cfd88b266fb8999cd27ce60cbb86593ad19_

```
  310 |        against the actual library ABI. mpt_utility.h pulls in secp256k1_mpt.h,
  311 |        mpt_protocol.h, secp256k1.h, stdbool.h and stddef.h. */
  312 |     #include <stdint.h>
```

_file_excerpt · [xrpl/ext/confidential/commitments.py](https://github.com/XRPLF/xrpl-py/blob/d15d5a0f42b2c57a800dc8ad2c802ec3a899450f/xrpl/ext/confidential/commitments.py#L8) · line 8 · SHA-256 46e9d6d9844e2c6d8144b3269b0292f8f1a572aef0a51087e107c5947b4c5277_

```
    7 | create_bulletproof / verify_bulletproof are available on every platform:
    8 | mpt-crypto (including secp256k1) is statically linked into the extension, so
    9 | secp256k1_ec_pubkey_parse is bound directly everywhere (the old Windows DLL did
```

_file_excerpt · [xrpl/ext/confidential/crypto_bindings.py](https://github.com/XRPLF/xrpl-py/blob/d15d5a0f42b2c57a800dc8ad2c802ec3a899450f/xrpl/ext/confidential/crypto_bindings.py#L7) · line 7 · SHA-256 89faa6fb76e06804323efc16306d552c24566db17a6fb6425e0bc2b85293bf0d_

```
    6 | 
    7 | The mpt-crypto C code (with secp256k1 and OpenSSL) is statically linked INTO
    8 | the CFFI extension (_mpt_crypto) at build time, so the compiled extension is
```

_file_excerpt · [xrpl/ext/confidential/include/utility/mpt_utility.h](https://github.com/XRPLF/xrpl-py/blob/d15d5a0f42b2c57a800dc8ad2c802ec3a899450f/xrpl/ext/confidential/include/utility/mpt_utility.h#L5) · line 5 · SHA-256 308d3e70f8eba79c098cdc39235abd5d05a95f5718c61c02060e9faf7543c0cb_

```
    4 | #include <mpt_protocol.h>
    5 | #include <secp256k1.h>
    6 | #include <secp256k1_mpt.h>
```

_file_excerpt · [xrpl/ext/confidential/main.py](https://github.com/XRPLF/xrpl-py/blob/d15d5a0f42b2c57a800dc8ad2c802ec3a899450f/xrpl/ext/confidential/main.py#L73) · line 73 · SHA-256 8438a059ea62f124fd825162d3ed5588482761baf11ede88f3740eb307e93e57_

```
   72 |     def __init__(self: Self) -> None:
   73 |         """Initialize with mpt-crypto's globally shared secp256k1 context."""
   74 |         # Use the context owned by mpt-crypto rather than creating our own:
```

_file_excerpt · [xrpl/ext/confidential/main.py](https://github.com/XRPLF/xrpl-py/blob/d15d5a0f42b2c57a800dc8ad2c802ec3a899450f/xrpl/ext/confidential/main.py#L81) · line 81 · SHA-256 c487ff44a0b600ae8611b7afce30440380fffaf04367a4e33cb1dc4e00f164c6_

```
   80 |         if self.ctx == ffi.NULL:
   81 |             raise RuntimeError("Failed to obtain mpt-crypto secp256k1 context")
   82 | 
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it; introduce an abstraction layer for crypto-agility.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-44391 — Quantum-vulnerable EC-ElGamal: key wrapping and data encryption at rest (5 file(s))

- Severity: **Low** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:EC-ElGamal:key_wrapping`
- Data source: xrpl/ext/confidential/build_mpt_crypto.py
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.16.2 · 2026-11-23 14:07 UTC
- Priority score: 27.9 / 100
- CVSS v3.1: not applicable

43 reference(s) to EC-ElGamal across 5 file(s), e.g. xrpl/ext/confidential/build_mpt_crypto.py:63. Role, judged from paths, function names and nearby code: key wrapping and data encryption at rest. Keys or data encrypted to these public keys are stored: anyone who copies them now decrypts them once a CRQC exists (harvest now, decrypt later).

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open xrpl/ext/confidential/build_mpt_crypto.py:63 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [xrpl/ext/confidential/build_mpt_crypto.py](https://github.com/XRPLF/xrpl-py/blob/d15d5a0f42b2c57a800dc8ad2c802ec3a899450f/xrpl/ext/confidential/build_mpt_crypto.py#L63) · line 63 · SHA-256 a190cc938dc5874cf9439579c4eec258d9c9ea67657905b73d8b5ca6088a1ba6_

```
   62 |     );
   63 |     int secp256k1_mpt_get_generator_vector(
   64 |         const secp256k1_context* ctx,
```

_file_excerpt · [xrpl/ext/confidential/build_mpt_crypto.py](https://github.com/XRPLF/xrpl-py/blob/d15d5a0f42b2c57a800dc8ad2c802ec3a899450f/xrpl/ext/confidential/build_mpt_crypto.py#L104) · line 104 · SHA-256 72e4d7b80df678ca6ae5e8cb5066174424dad17098f5b5c4c1be34f4a2d7bf42_

```
  103 |     // ---- Keys / encryption / commitment ----
  104 |     int mpt_generate_keypair(uint8_t* out_privkey, uint8_t* out_pubkey);
  105 |     int mpt_generate_blinding_factor(uint8_t out_factor[32]);
```

_file_excerpt · [xrpl/ext/confidential/build_mpt_crypto.py](https://github.com/XRPLF/xrpl-py/blob/d15d5a0f42b2c57a800dc8ad2c802ec3a899450f/xrpl/ext/confidential/build_mpt_crypto.py#L106) · line 106 · SHA-256 8688f57ad9a7d96f0fc57d7761fa1f7d6a4582c2c28173197da1e77a6a6ae16d_

```
  105 |     int mpt_generate_blinding_factor(uint8_t out_factor[32]);
  106 |     int mpt_encrypt_amount(
  107 |         uint64_t amount,
```

_file_excerpt · [xrpl/ext/confidential/encryption.py](https://github.com/XRPLF/xrpl-py/blob/d15d5a0f42b2c57a800dc8ad2c802ec3a899450f/xrpl/ext/confidential/encryption.py#L2) · line 2 · SHA-256 25b870e010354969fdffcc2b627d16cd5274ea1e396dece2df5ae8cc4e7abe1f_

```
    1 | """
    2 | ElGamal encryption and decryption functions.
    3 | 
```

_file_excerpt · [xrpl/ext/confidential/encryption.py](https://github.com/XRPLF/xrpl-py/blob/d15d5a0f42b2c57a800dc8ad2c802ec3a899450f/xrpl/ext/confidential/encryption.py#L5) · line 5 · SHA-256 1e3b3f9946e2125116f2a6e96a221c4185e7b1496db6f9cc4c3d3f4eabf2d9f3_

```
    4 | This module provides functions for encrypting and decrypting amounts
    5 | using ElGamal encryption.
    6 | """
```

_file_excerpt · [xrpl/ext/confidential/encryption.py](https://github.com/XRPLF/xrpl-py/blob/d15d5a0f42b2c57a800dc8ad2c802ec3a899450f/xrpl/ext/confidential/encryption.py#L29) · line 29 · SHA-256 74511517b9c81de1a6e5e78453b1636abf8d6e39a893d4e023ecf48571ececbb_

```
   28 |     """
   29 |     Encrypt an amount using ElGamal encryption via the utility layer.
   30 | 
```

_file_excerpt · [xrpl/ext/confidential/homomorphic.py](https://github.com/XRPLF/xrpl-py/blob/d15d5a0f42b2c57a800dc8ad2c802ec3a899450f/xrpl/ext/confidential/homomorphic.py#L2) · line 2 · SHA-256 7b2a64b448bbf11ef1c5a8d9b6153917c6d260157edd7167d158e22ce924abd5_

```
    1 | """
    2 | Homomorphic operations on EC-ElGamal ciphertexts.
    3 | 
```

_file_excerpt · [xrpl/ext/confidential/homomorphic.py](https://github.com/XRPLF/xrpl-py/blob/d15d5a0f42b2c57a800dc8ad2c802ec3a899450f/xrpl/ext/confidential/homomorphic.py#L4) · line 4 · SHA-256 7f5fc24f1a5a3073aa3b34d7c69ddf1829a414874e6406f8fa03e2b6f9c03c4a_

```
    3 | 
    4 | ElGamal is additively homomorphic: ``Enc(a) +/- Enc(b) = Enc(a +/- b)`` when both
    5 | ciphertexts are encrypted under the same public key. These wrap mpt-crypto's
```

_file_excerpt · [xrpl/ext/confidential/homomorphic.py](https://github.com/XRPLF/xrpl-py/blob/d15d5a0f42b2c57a800dc8ad2c802ec3a899450f/xrpl/ext/confidential/homomorphic.py#L6) · line 6 · SHA-256 04bd5729da3dfdab9b423dafc6a5a78dd2463e4bf8b14710e518e83565795fb6_

```
    5 | ciphertexts are encrypted under the same public key. These wrap mpt-crypto's
    6 | ``secp256k1_elgamal_add`` / ``secp256k1_elgamal_subtract``.
    7 | 
```

_file_excerpt · [xrpl/ext/confidential/include/secp256k1_mpt.h](https://github.com/XRPLF/xrpl-py/blob/d15d5a0f42b2c57a800dc8ad2c802ec3a899450f/xrpl/ext/confidential/include/secp256k1_mpt.h#L16) · line 16 · SHA-256 2fe0678af4d255c60ea8a39b55985920c55d42ba3f09a6a4eb9f1088aa6016e5_

```
   15 | SECP256K1_API int
   16 | secp256k1_elgamal_generate_keypair(
   17 |     secp256k1_context const* ctx,
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Wrap keys with ML-KEM or a hybrid KEM (X25519 + ML-KEM-768) and re-wrap the stored keys; data that may already have been copied needs its own assessment.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-44394 — Quantum-vulnerable ElGamal: key wrapping and data encryption at rest (3 file(s))

- Severity: **Low** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:ElGamal:key_wrapping`
- Data source: xrpl/ext/confidential/main.py
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.16.2 · 2026-11-23 14:07 UTC
- Priority score: 27.9 / 100
- CVSS v3.1: not applicable

14 reference(s) to ElGamal across 3 file(s), e.g. xrpl/ext/confidential/main.py:85. Role, judged from paths, function names and nearby code: key wrapping and data encryption at rest. Keys or data encrypted to these public keys are stored: anyone who copies them now decrypts them once a CRQC exists (harvest now, decrypt later).

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open xrpl/ext/confidential/main.py:85 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [xrpl/ext/confidential/main.py](https://github.com/XRPLF/xrpl-py/blob/d15d5a0f42b2c57a800dc8ad2c802ec3a899450f/xrpl/ext/confidential/main.py#L85) · line 85 · SHA-256 0d0bd3bdd8639f549a3273f2d20f541de3fb61e674e02e49b75c296ddf0b153c_

```
   84 |     def generate_keypair(self: Self) -> Tuple[str, str]:
   85 |         """Generate an ElGamal keypair."""
   86 |         return keypair.generate_keypair()
```

_file_excerpt · [xrpl/ext/confidential/main.py](https://github.com/XRPLF/xrpl-py/blob/d15d5a0f42b2c57a800dc8ad2c802ec3a899450f/xrpl/ext/confidential/main.py#L91) · line 91 · SHA-256 846bc3e46c9c81631a230f42f99ffb71e9550933885c484db5809426830d4cce_

```
   90 |     ) -> Tuple[str, str, str]:
   91 |         """Generate an ElGamal keypair with a Schnorr proof of knowledge."""
   92 |         return keypair.generate_keypair_with_pok(context_id)
```

_file_excerpt · [xrpl/ext/confidential/main.py](https://github.com/XRPLF/xrpl-py/blob/d15d5a0f42b2c57a800dc8ad2c802ec3a899450f/xrpl/ext/confidential/main.py#L113) · line 113 · SHA-256 0b53c3aa6fe1d897640db31ed30125c438d5ac469ed32e86512171a68bbe1bd4_

```
  112 |     ) -> Tuple[str, str, str]:
  113 |         """Encrypt an amount using ElGamal encryption."""
  114 |         return encryption.encrypt(pubkey_uncompressed, amount, blinding_factor)
```

_file_excerpt · [xrpl/ext/confidential/transaction_builders.py](https://github.com/XRPLF/xrpl-py/blob/d15d5a0f42b2c57a800dc8ad2c802ec3a899450f/xrpl/ext/confidential/transaction_builders.py#L240) · line 240 · SHA-256 2675ea955a3c9c0b205530637d1e03fd1d2ad7f932a8485fd15a7af2a74f972b_

```
  239 | ) -> int:
  240 |     """Decrypt an on-ledger ElGamal balance blob to its plaintext amount.
  241 | 
```

_file_excerpt · [xrpl/ext/confidential/transaction_builders.py](https://github.com/XRPLF/xrpl-py/blob/d15d5a0f42b2c57a800dc8ad2c802ec3a899450f/xrpl/ext/confidential/transaction_builders.py#L253) · line 253 · SHA-256 f15d56d8b6c63560e6a2b65b025dda90273f53a95be682e852d30b6df7401935_

```
  252 |     Args:
  253 |         balance_hex: 132-char hex ElGamal ciphertext (``c1 || c2``). An empty
  254 |             string (no confidential balance yet) returns 0.
```

_file_excerpt · [xrpl/ext/confidential/transaction_builders.py](https://github.com/XRPLF/xrpl-py/blob/d15d5a0f42b2c57a800dc8ad2c802ec3a899450f/xrpl/ext/confidential/transaction_builders.py#L272) · line 272 · SHA-256 369b883dd8d14b41e577df5184512206c33de556329ac47d23575a5e9992891a_

```
  271 |             f"balance_hex must be {CIPHERTEXT_LENGTH} hex characters "
  272 |             f"({CIPHERTEXT_LENGTH // 2}-byte c1||c2 ElGamal ciphertext)"
  273 |         )
```

_file_excerpt · [xrpl/models/transactions/confidential_mpt_convert.py](https://github.com/XRPLF/xrpl-py/blob/d15d5a0f42b2c57a800dc8ad2c802ec3a899450f/xrpl/models/transactions/confidential_mpt_convert.py#L76) · line 76 · SHA-256 47b8909c810b7d192e1894124758d107f0cc35e56b2c34db97ef6c4ed4842223_

```
   75 |     holder_encrypted_amount: str = REQUIRED
   76 |     """ElGamal ciphertext credited to the holder's CB_IN."""
   77 | 
```

_file_excerpt · [xrpl/models/transactions/confidential_mpt_convert.py](https://github.com/XRPLF/xrpl-py/blob/d15d5a0f42b2c57a800dc8ad2c802ec3a899450f/xrpl/models/transactions/confidential_mpt_convert.py#L79) · line 79 · SHA-256 04a95027286e26ef4db072051f903a5f150ff65d57b4d3200e5169ff37c68409_

```
   78 |     issuer_encrypted_amount: str = REQUIRED
   79 |     """ElGamal ciphertext credited to the issuer's mirror balance."""
   80 | 
```

_file_excerpt · [xrpl/models/transactions/confidential_mpt_convert.py](https://github.com/XRPLF/xrpl-py/blob/d15d5a0f42b2c57a800dc8ad2c802ec3a899450f/xrpl/models/transactions/confidential_mpt_convert.py#L89) · line 89 · SHA-256 cae6d051ebd252b2295a7d354416b51d7ae6c6189a2dec52a27e822206a8330d_

```
   88 |     """
   89 |     The holder's ElGamal public key. Mandatory if the account has not yet
   90 |     registered a key (initialization). Forbidden if a key is already registered.
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Wrap keys with ML-KEM or a hybrid KEM (X25519 + ML-KEM-768) and re-wrap the stored keys; data that may already have been copied needs its own assessment.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-44393 — Quantum-vulnerable EC-ElGamal: role not determined (3 file(s))

- Severity: **Low** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:EC-ElGamal:general`
- Data source: xrpl/ext/confidential/commitments.py
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.16.2 · 2026-11-23 14:07 UTC
- Priority score: 25.2 / 100
- CVSS v3.1: not applicable

8 reference(s) to EC-ElGamal across 3 file(s), e.g. xrpl/ext/confidential/commitments.py:171. Role, judged from paths, function names and nearby code: role not determined. The code does not show what the keys protect; review decides the priority.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open xrpl/ext/confidential/commitments.py:171 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [xrpl/ext/confidential/commitments.py](https://github.com/XRPLF/xrpl-py/blob/d15d5a0f42b2c57a800dc8ad2c802ec3a899450f/xrpl/ext/confidential/commitments.py#L171) · line 171 · SHA-256 0eea2150fc41585b4881146be315699eb2766047119cc3b83bed5b867fb89304_

```
  170 | 
  171 |     result = lib.secp256k1_mpt_get_generator_vector(ctx, G_vec, n, b"G", 1)
  172 |     if result != 1:
```

_file_excerpt · [xrpl/ext/confidential/commitments.py](https://github.com/XRPLF/xrpl-py/blob/d15d5a0f42b2c57a800dc8ad2c802ec3a899450f/xrpl/ext/confidential/commitments.py#L175) · line 175 · SHA-256 01ec6df50b6217d3b5d03c1bdfb4613466317f5c783402db47c8dfc506f41c66_

```
  174 | 
  175 |     result = lib.secp256k1_mpt_get_generator_vector(ctx, H_vec, n, b"H", 1)
  176 |     if result != 1:
```

_file_excerpt · [xrpl/ext/confidential/keypair.py](https://github.com/XRPLF/xrpl-py/blob/d15d5a0f42b2c57a800dc8ad2c802ec3a899450f/xrpl/ext/confidential/keypair.py#L4) · line 4 · SHA-256 77051da554a2f18c492507b0e6f3427228396184330d3b80798075aff937b745_

```
    3 | 
    4 | This module provides functions for generating ElGamal keypairs and
    5 | creating/verifying Schnorr proofs of knowledge.
```

_file_excerpt · [xrpl/ext/confidential/keypair.py](https://github.com/XRPLF/xrpl-py/blob/d15d5a0f42b2c57a800dc8ad2c802ec3a899450f/xrpl/ext/confidential/keypair.py#L22) · line 22 · SHA-256 44d610e3560217d5e2ff4dcdb8d5491e4543ea54fa4d14188ae613ab7ab9216a_

```
   21 |     """
   22 |     Generate an ElGamal keypair using the utility layer.
   23 | 
```

_file_excerpt · [xrpl/ext/confidential/keypair.py](https://github.com/XRPLF/xrpl-py/blob/d15d5a0f42b2c57a800dc8ad2c802ec3a899450f/xrpl/ext/confidential/keypair.py#L33) · line 33 · SHA-256 791ce3b68dd48595a9d511ded3ab65c8956a4c8a0159390ef6a7b908617330d6_

```
   32 | 
   33 |     result = lib.mpt_generate_keypair(privkey, pubkey)
   34 |     if result != 0:
```

_file_excerpt · [xrpl/models/transactions/mptoken_issuance_set.py](https://github.com/XRPLF/xrpl-py/blob/d15d5a0f42b2c57a800dc8ad2c802ec3a899450f/xrpl/models/transactions/mptoken_issuance_set.py#L148) · line 148 · SHA-256 abd045428e6e337cf6ba59f6d5c4164eeae301007674feeeda2ad00343e2f380_

```
  147 |     """
  148 |     The 33-byte EC-ElGamal public key used for the issuer's mirror balances.
  149 |     """
```

_file_excerpt · [xrpl/models/transactions/mptoken_issuance_set.py](https://github.com/XRPLF/xrpl-py/blob/d15d5a0f42b2c57a800dc8ad2c802ec3a899450f/xrpl/models/transactions/mptoken_issuance_set.py#L153) · line 153 · SHA-256 10b9554e5a04c4ee9545565e1e3d2d65edd831b61e87b52cfe5f86a592dc30f6_

```
  152 |     """
  153 |     The 33-byte EC-ElGamal public key used for regulatory oversight (if applicable).
  154 |     """
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Classify each usage, record data lifetimes, and plan migration to NIST's post-quantum standards cover key encapsulation and signatures; none covers additively homomorphic encryption. Treat amounts encrypted this way as eventually public, and limit what a design must store on-ledger; lattice-based homomorphic schemes are the research direction; introduce an abstraction layer for crypto-agility.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-44395 — Quantum-vulnerable ElGamal: role not determined (2 file(s))

- Severity: **Low** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:ElGamal:general`
- Data source: xrpl/models/base_model.py
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.16.2 · 2026-11-23 14:07 UTC
- Priority score: 25.2 / 100
- CVSS v3.1: not applicable

2 reference(s) to ElGamal across 2 file(s), e.g. xrpl/models/base_model.py:41. Role, judged from paths, function names and nearby code: role not determined. The code does not show what the keys protect; review decides the priority.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open xrpl/models/base_model.py:41 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [xrpl/models/base_model.py](https://github.com/XRPLF/xrpl-py/blob/d15d5a0f42b2c57a800dc8ad2c802ec3a899450f/xrpl/models/base_model.py#L41) · line 41 · SHA-256 28031f663f883590dcfeb6f591ebf565599382a3647ee2e6d842bde6d59f3b5f_

```
   40 |     "did": "DID",
   41 |     "elgamal": "ElGamal",
   42 |     "id": "ID",
```

_file_excerpt · [xrpl/models/transactions/confidential_mpt_clawback.py](https://github.com/XRPLF/xrpl-py/blob/d15d5a0f42b2c57a800dc8ad2c802ec3a899450f/xrpl/models/transactions/confidential_mpt_clawback.py#L28) · line 28 · SHA-256 1e4e257f50c1659303ea51ba742faa7367f7657384dc43d49e1e5b3a82e0f626_

```
   27 |     account. This action is fundamentally incompatible with standard confidential
   28 |     transfers, as the issuer does not possess the holder's private ElGamal key
   29 |     and therefore cannot generate the required ZKPs for a normal ConfidentialSend.
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Classify each usage, record data lifetimes, and plan migration to Hybrid key establishment with ML-KEM (FIPS 203), e.g. X25519MLKEM768 in TLS 1.3 or mlkem768x25519-sha256 in SSH; introduce an abstraction layer for crypto-agility.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-44396 — No post-quantum capable cryptographic library detected

- Severity: **Info** · Classification: Insufficient data · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `dependencies`
- Data source: dependency manifests
- Detection method: Dependency name matching.
- Analyzer: dependencies 1.16.2 · 2026-11-23 14:07 UTC
- Priority score: 12.2 / 100
- CVSS v3.1: not applicable

Across 3 dependency manifests, QSI found crypto libraries (pycryptodome, xrpl-py) but none from its PQC-capable list.

**Potential impact.** Readiness indicator only: PQC support may come from the platform (OpenSSL, OS, cloud KMS) rather than application dependencies.

**Reproduction steps.**

```
Review the dependency manifests listed in the evidence.
```

**Evidence.**

_dependency · packaging/confidential/pyproject.toml, poetry.lock, pyproject.toml · SHA-256 571f5c3b2d3bb8455fa49046948cdad270089d6f96db814d36befd31e0c98df7_

```
Crypto libraries: pycryptodome, xrpl-py
```

**Limitations of the check.** Absence of evidence is not evidence of absence: system libraries and transitive dependencies may not be listed.

**Recommendation.** Confirm where PQC support will come from (TLS terminator, KMS/HSM, library upgrade).

**Retest procedure.** Re-scan after upgrades.


## 8. Post-quantum assessment

| | Key establishment (x = how long data must stay confidential; harvest now, decrypt later) | Signatures (x = how long signatures/keys must stay trusted) |
|---|---|---|
| Data/key lifetime x | 5 | 10 |
| Migration time y | 5 | 5 |
| Assumed years to CRQC z | 12 (central) | 12 |
| x + y − z | -2 → tight margin | 3 → migration would finish too late under this scenario |
#### Where z comes from

Averaged expert likelihood that a CRQC exists within each horizon, from the annual survey published by the author of this inequality. Likelihood estimates, not predictions of a date.

| Within | Likelihood | The report's wording |
|---|---|---|
| 5 years | ~15% | averaged estimate |
| 10 years | 28-49% | quite possible |
| 15 years | 51-70% | likely |

**Why this scenario (central, z = 12):** Between the 10-year band (28-49%) and the 15-year band (51-70%): roughly where the experts' averaged likelihood crosses one half. More than half of the respondents (13 of 26) already put the likelihood at 50% or more for some horizon.
_Planning assumptions: x for key establishment, x for signatures, y are the defaults of the risk profile “Web3 project”, not the client's figures; with the client's actual lifetimes the verdict can change._

### Post-quantum maturity: Level 0 of 4 — no post-quantum cryptography

- Classical only — key wrapping and data encryption at rest: EC-ElGamal, ElGamal (8 file(s))
- Classical only — threshold signing and MPC protocols: Pedersen commitment (6 file(s))

**Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

_Levels: 0 none; 1 present, not wired; 2 in use outside the critical paths; 3 hybrid in a critical path; 4 post-quantum by default in the critical paths (root of trust, key wrapping, channel key exchange). Judged from code and manifests._

### What the quantum-vulnerable algorithms do

| Role | Algorithms (files) | ID | First step |
|---|---|---|---|
| **key wrapping and data encryption at rest** | EC-ElGamal (5), ElGamal (3) | QSI-2026-44391, QSI-2026-44394 | Wrap keys with ML-KEM or a hybrid KEM (X25519 + ML-KEM-768) and re-wrap the stored keys; data that may already have been copied needs its own assessment |
| **threshold signing and MPC protocols** | Pedersen commitment (6) | QSI-2026-44392 | Track post-quantum threshold signatures (NIST IR 8214C) and keep the protocol layer ready to swap the signature scheme; record which keys and shares must stay valid for how long |
| **transaction and message signing** | ECDSA (5) | QSI-2026-44390 | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains adopt them |
| **role not determined** | ECDSA (7), EC-ElGamal (3), ElGamal (2) | QSI-2026-44389, QSI-2026-44393, QSI-2026-44395 | Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it; introduce an abstraction layer for crypto-agility |

_Roles are judged from file paths, function names and the code around each match; review confirms them. Root-of-trust keys and wrapped keys come first: they are hard to replace or can be recorded today._
No readiness questionnaire was completed for this project.

### Quantum algorithms relevant to this inventory

| Quantum algorithm | Effect | Attack model | Inventoried algorithms (rows) | What it means for this audit |
|---|---|---|---|---|
| Shor's algorithm — discrete logarithms in finite fields | breaks | Q1 | ElGamal (5) | Breaks finite-field Diffie–Hellman and DSA at every size. Move key establishment to ML-KEM (hybrid with X25519 or ECDH during the transition) and signatures to ML-DSA or SLH-DSA. |
| Shor's algorithm — elliptic-curve discrete logarithms | breaks | Q1 | EC-ElGamal (8), ECDSA (12), Ed25519 (1), Pedersen commitment (6) | Elliptic-curve keys are expected to fall before RSA keys of comparable classical strength. On blockchains, coins whose public key is already on chain (reused addresses, pay-to-public-key and Taproot outputs) are exposed first; plan the move to post-quantum signatures and avoid key reuse in the meantime. |
| Grover's algorithm — key search and preimages | weakens (larger keys restore the margin) | Q1 | RIPEMD-160 (1), SHA-2 (2) | Not a break. 256-bit keys (AES-256, ChaCha20) keep a comfortable margin; AES-128 meets NIST category 1, while some authorities ask for 256-bit keys in quantum-resistant contexts (see the AES-128 entry). Prefer 256-bit keys for long-lived data; 256-bit hashes need no change for preimage resistance. |
| Brassard–Høyer–Tapp — collision search | weakens (larger keys restore the margin) | Q1 | RIPEMD-160 (1), SHA-2 (2) | 256-bit hashes (SHA-256, SHA3-256) remain adequate for collision resistance; 160-bit hashes are already weak classically (SHA-1 collisions are practical). Use 384/512-bit hashes where NIST categories 4–5 are required. |

_Effects: breaks — replace the algorithm; weakens — larger keys or outputs restore the margin; included in standard parameters — no action at standard parameter sets; only with superposition queries — not applicable to ordinary deployments._


## 9. Limitations and assumptions

- This report presents automated and documented analysis results for the stated scope. It is not a legal opinion, a certification or an attestation of compliance with any standard.
- z is a planning assumption chosen per risk profile, not a prediction. A cryptographically relevant quantum computer is not publicly known to exist today.
- tls_key_exchange_groups: 73 (examples: poetry.lock line 9: not in the algorithm registry, not assessed: ["dev"]; poetry.lock line 24: not in the algorithm registry, not assessed: ["dev"]; poetry.lock line 36: not in the algorithm registry, not assessed: ["main"])

## 10. Remediation plan / Priorities for 30, 60 and 90 days

### 30 days

| Priority | ID | Action | Type | Closure criteria |
|---|---|---|---|---|
### 60 days

| Priority | ID | Action | Type | Closure criteria |
|---|---|---|---|---|
### 90 days

| Priority | ID | Action | Type | Closure criteria |
|---|---|---|---|---|
| P3 | QSI-2026-44390 | Add ECDSA usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-44392 | Add Pedersen commitment usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-44389 | Add ECDSA usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-44391 | Add EC-ElGamal usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-44394 | Add ElGamal usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-44393 | Add EC-ElGamal usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-44395 | Add ElGamal usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P4 | QSI-2026-44390 | Plan migration of ECDSA to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-44392 | Plan migration of Pedersen commitment to  (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows  or a hybrid scheme in use. |
| P4 | QSI-2026-44389 | Plan migration of ECDSA to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-44391 | Plan migration of EC-ElGamal to NIST's post-quantum standards cover key encapsulation and signatures; none covers additively homomorphic encryption. Treat amounts encrypted this way as eventually public, and limit what a design must store on-ledger; lattice-based homomorphic schemes are the research direction (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows NIST's post-quantum standards cover key encapsulation and signatures; none covers additively homomorphic encryption. Treat amounts encrypted this way as eventually public, and limit what a design must store on-ledger; lattice-based homomorphic schemes are the research direction or a hybrid scheme in use. |
| P4 | QSI-2026-44394 | Plan migration of ElGamal to Hybrid key establishment with ML-KEM (FIPS 203), e.g. X25519MLKEM768 in TLS 1.3 or mlkem768x25519-sha256 in SSH (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows Hybrid key establishment with ML-KEM (FIPS 203), e.g. X25519MLKEM768 in TLS 1.3 or mlkem768x25519-sha256 in SSH or a hybrid scheme in use. |
| P4 | QSI-2026-44393 | Plan migration of EC-ElGamal to NIST's post-quantum standards cover key encapsulation and signatures; none covers additively homomorphic encryption. Treat amounts encrypted this way as eventually public, and limit what a design must store on-ledger; lattice-based homomorphic schemes are the research direction (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows NIST's post-quantum standards cover key encapsulation and signatures; none covers additively homomorphic encryption. Treat amounts encrypted this way as eventually public, and limit what a design must store on-ledger; lattice-based homomorphic schemes are the research direction or a hybrid scheme in use. |
| P4 | QSI-2026-44395 | Plan migration of ElGamal to Hybrid key establishment with ML-KEM (FIPS 203), e.g. X25519MLKEM768 in TLS 1.3 or mlkem768x25519-sha256 in SSH (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows Hybrid key establishment with ML-KEM (FIPS 203), e.g. X25519MLKEM768 in TLS 1.3 or mlkem768x25519-sha256 in SSH or a hybrid scheme in use. |

## 11. Tools used

- blockchain 1.0.0
- certificates 1.2.0
- chain_map 1.0.0
- configs 1.1.0
- crediting 1.3.0
- dependencies 1.4.4
- hndl 1.0.0
- inventory_document 1.1.0
- mpc 1.0.0
- solidity 1.8.1
- source_code 1.10.2
- tls_code 1.1.0
- tls_live 1.0.0
- ton_contracts 1.0.0
- validator_keys 1.2.0
- wallet_login 1.0.0
- qsi-engine 1.16.2
- OSV.dev API v1

## 12. Sources and normative documents

1. A. Chailloux, M. Naya-Plasencia, A. Schrottenloher — An Efficient Quantum Collision Search Algorithm and Implications on Symmetric Cryptography (ASIACRYPT 2017; IACR ePrint 2017/847) — IACR ePrint. <https://eprint.iacr.org/2017/847> (peer-reviewed article: Õ(2^{2n/5}) time, O(n) qubits, Õ(2^{n/5}) classical memory)
2. C. Chevignard, P.-A. Fouque, A. Schrottenloher — Reducing the Number of Qubits in Quantum Discrete Logarithms on Elliptic Curves (IACR ePrint 2026/280) — IACR ePrint. <https://eprint.iacr.org/2026/280> (revision of a EUROCRYPT 2026 paper: 3.12n + o(n) qubits; for n = 256, 1193 qubits and 22 runs of 2^38.98 Toffoli gates)
3. C. Gidney, M. Ekerå — How to factor 2048 bit RSA integers in 8 hours using 20 million noisy qubits (Quantum 5, 433) — Quantum. <https://doi.org/10.22331/q-2021-04-15-433> (peer-reviewed article (2021): 10^-3 gate error, 1 µs cycle, 10 µs reaction time)
4. C. Zalka — Grover's quantum searching algorithm is optimal (Phys. Rev. A 60, 2746, 1999; arXiv:quant-ph/9711070) — APS. <https://doi.org/10.1103/PhysRevA.60.2746> (peer-reviewed article: optimal for any success probability; parallel search gains no more than splitting the space)
5. Common Vulnerability Scoring System v3.1: Specification Document — FIRST. <https://www.first.org/cvss/v3.1/specification-document> (final)
6. D. J. Bernstein — Cost analysis of hash collisions: Will quantum computers make SHARCS obsolete? (2009) — cr.yp.to. <https://cr.yp.to/hash/collisioncost-20090823.pdf> (paper dated 2009-08-23)
7. D. Litinski — How to compute a 256-bit elliptic curve private key with only 50 million Toffoli gates (arXiv:2306.08585) — arXiv. <https://arxiv.org/abs/2306.08585> (preprint (2023-06-14): 6000 modules × 1152 physical qubits, one key per 10 minutes under its architecture assumptions)
8. FIPS 203 — Module-Lattice-Based Key-Encapsulation Mechanism Standard (ML-KEM) — NIST. <https://csrc.nist.gov/pubs/fips/203/final> (final (August 2024))
9. FIPS 204 — Module-Lattice-Based Digital Signature Standard (ML-DSA) — NIST. <https://csrc.nist.gov/pubs/fips/204/final> (final (August 2024))
10. FIPS 205 — Stateless Hash-Based Digital Signature Standard (SLH-DSA) — NIST. <https://csrc.nist.gov/pubs/fips/205/final> (final (August 2024))
11. G. Brassard, P. Høyer, A. Tapp — Quantum Algorithm for the Collision Problem (LATIN '98; arXiv:quant-ph/9705002) — Springer / arXiv. <https://arxiv.org/abs/quant-ph/9705002> (peer-reviewed article: collisions of r-to-one functions in O((N/r)^{1/3}) expected evaluations)
12. J. Proos, C. Zalka — Shor's discrete logarithm quantum algorithm for elliptic curves (Quantum Inf. Comput. 3(4), 2003; arXiv:quant-ph/0301141) — Quantum Information & Computation. <https://doi.org/10.26421/QIC3.4-3> (peer-reviewed article)
13. L. K. Grover — A fast quantum mechanical algorithm for database search (STOC 1996) — ACM. <https://doi.org/10.1145/237814.237866> (peer-reviewed article)
14. M. Amy et al. — Estimating the cost of generic quantum pre-image attacks on SHA-2 and SHA-3 (SAC 2016; arXiv:1603.09383) — Springer / arXiv. <https://arxiv.org/abs/1603.09383> (peer-reviewed article: SHA-256 about 2^153.8 surface-code cycles on 2^12.6 logical qubits; SHA3-256 about 2^146.5 cycles on 2^20)
15. M. Cain et al. — Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits (arXiv:2603.28627) — arXiv. <https://arxiv.org/abs/2603.28627> (preprint (2026-03-30): P-256 in a few days with 26,000 physical neutral-atom qubits; RSA-2048 one to two orders of magnitude longer)
16. M. Ekerå, J. Gärtner — A high-level comparison of state-of-the-art quantum algorithms for breaking asymmetric cryptography (arXiv:2405.14381) — arXiv. <https://arxiv.org/abs/2405.14381> (preprint (2024-05-23): Regev-style algorithms show no overall advantage yet for cryptographic RSA and finite-field sizes)
17. M. Mosca — Cybersecurity in an Era with Quantum Computers: Will We Be Ready? (IEEE Security & Privacy, 2018) — IEEE. <https://doi.org/10.1109/MSP.2018.3761723> (peer-reviewed article; source of the x + y > z migration inequality)
18. M. Roetteler, M. Naehrig, K. Svore, K. Lauter — Quantum resource estimates for computing elliptic curve discrete logarithms (ASIACRYPT 2017) — IACR / arXiv. <https://arxiv.org/abs/1706.06752> (peer-reviewed article: at most 9n + 2⌈log2 n⌉ + 10 qubits and 448 n^3 log2 n + 4090 n^3 Toffoli gates)
19. NIST IR 8547 — Transition to Post-Quantum Cryptography Standards — NIST. <https://csrc.nist.gov/pubs/ir/8547/final> (final (2026-10-27; the initial public draft of November 2024 is obsoleted). Tables 2 and 4: ECDSA, EdDSA and RSA signatures, finite-field and elliptic-curve DH and MQV, and RSA key establishment are deprecated after 2030 and disallowed after 2035 at every key size — the draft deprecated only the 112-bit level. A composite (hybrid) key establishment stays FIPS 140-validatable while one input comes from an approved scheme. Repeats the federal deadlines of OMB M-26-15: post-quantum key establishment by 2030-12-31 and signatures by 2031-12-31 for high value assets and high impact systems)
20. NIST — Post-Quantum Cryptography Standardization: Evaluation Criteria, Security (Call for Proposals, Section 4.A.5) — NIST. <https://csrc.nist.gov/Projects/Post-Quantum-Cryptography/Post-Quantum-Cryptography-Standardization/Evaluation-Criteria/Security-(Evaluation-Criteria)> (security categories: AES-128 key search 2^170/MAXDEPTH quantum gates, AES-192 2^233/MAXDEPTH, AES-256 2^298/MAXDEPTH; MAXDEPTH 2^40–2^96)
21. P. W. Shor — Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms on a Quantum Computer (SIAM J. Comput., 1997) — SIAM. <https://doi.org/10.1137/S0097539795293172> (peer-reviewed article)
22. R. Babbush et al. — Securing Elliptic Curve Cryptocurrencies against Quantum Vulnerabilities: Resource Estimates and Mitigations (arXiv:2603.28846) — arXiv. <https://arxiv.org/abs/2603.28846> (preprint (2026-03-30, v2 2026-04-15): 256-bit ECDLP with < 1200 logical qubits and < 90 M Toffoli gates (or < 1450 and < 70 M); < 500,000 physical qubits at 10^-3 error, minutes)
23. S. Jaques, M. Naehrig, M. Roetteler, F. Virdia — Implementing Grover oracles for quantum key search on AES and LowMC (EUROCRYPT 2020; arXiv:1910.01700) — Springer / arXiv. <https://arxiv.org/abs/1910.01700> (peer-reviewed article: lower cost estimates for the AES key searches that define the NIST categories)

## Appendices: Cryptographic inventory

By origin: dependency manifests 3 (0 Shor-breakable) · own code 35 (32 Shor-breakable).

| Algorithm | Parameter | Library | Quantum status | Classical status | Count | Locations | Examples |
|---|---|---|---|---|---|---|---|
| RIPEMD-160 | RIPEMD-160 |  | weak classically | legacy | 1 | 1 | xrpl/core/keypairs/helpers.py:34 |
| SHA-2 | SHA-512 |  | reduced margin (Grover), approved | acceptable | 1 | 1 | xrpl/core/keypairs/helpers.py:18 |
| SHA-2 | SHA-256 |  | Grover: acceptable to NIST, below ECCG/ANSSI guidance | acceptable | 1 | 1 | xrpl/core/keypairs/helpers.py:33 |
| Crypto library | >=5.1.0 | xrpl-py (xrpl-py) | n/a | acceptable | 1 | 1 | packaging/confidential/pyproject.toml |
| Crypto library | 3.23.0 | pycryptodome (PyCryptodome) | n/a | acceptable | 1 | 1 | poetry.lock |
| Crypto library | ^3.23.0 | pycryptodome (PyCryptodome) | n/a | acceptable | 1 | 1 | pyproject.toml |
| EC-ElGamal |  |  | vulnerable (Shor) | acceptable | 8 | 8 | xrpl/ext/confidential/build_mpt_crypto.py:63; xrpl/ext/confidential/commitments.py:171; xrpl/ext/confidential/encryption.py:2 |
| ECDSA | secp256k1 |  | vulnerable (Shor) | acceptable | 11 | 11 | xrpl/constants.py:15; xrpl/core/keypairs/main.py:15; xrpl/core/keypairs/secp256k1.py:1 |
| ECDSA |  |  | vulnerable (Shor) | acceptable | 1 | 1 | xrpl/ext/confidential/include/secp256k1.h:80 |
| Ed25519 | Ed25519 |  | vulnerable (Shor) | acceptable | 1 | 1 | xrpl/core/keypairs/ed25519.py |
| ElGamal |  |  | vulnerable (Shor) | deprecated | 5 | 5 | xrpl/ext/confidential/main.py:85; xrpl/ext/confidential/transaction_builders.py:240; xrpl/models/base_model.py:41 |
| Pedersen commitment |  |  | vulnerable (Shor) | acceptable | 6 | 6 | xrpl/ext/confidential/build_mpt_crypto.py:79; xrpl/ext/confidential/commitments.py:22; xrpl/ext/confidential/include/secp256k1_mpt.h:231 |

_Long lists are grouped here; the full per-file list is in the JSON report, signed with the same key._

## Appendices: Input files

| File | Size | SHA-256 | Redactions |
|---|---|---|---|
| docs/conf.py | 2160 | `3a61fbc7a329ab45f04cd0bf26ced10b89b4b5c7a4054499fe1196a3433d4604` | 0 |
| packaging/confidential/pyproject.toml | 5878 | `1a1d8ced438e8bc61c6bd00a85800229ee21741b250820641dab4e98bd271efc` | 0 |
| packaging/confidential/setup.py | 678 | `0a62c746e4bb246d426e59cfe065412e0575961aca59fada41b8d3e1076154af` | 0 |
| poetry.lock | 206397 | `c7d3970c6602acdcc54ec1f3afa10387190504f2f94d8c7847fe2744d2e27050` | 0 |
| pyproject.toml | 3916 | `27663a9b4af74ed007e84f2899625c85d4090f82903a0ed2736b74f3280f8389` | 0 |
| tools/generate_definitions.py | 10185 | `511233a494c7fe4955b243d2e4a46426567f8ed2020d5d3df8d5d239fb89e42b` | 0 |
| tools/generate_tx_models.py | 6539 | `4ac763645f3fe578380969c04b77bb6fc9700eda5cd869e2d46009fd7353c087` | 0 |
| xrpl/__init__.py | 349 | `a478acb95090c23a979d2da2e68f3a2c0f14fbb96478d30fc6e5bf10ba5baaea` | 0 |
| xrpl/account/__init__.py | 394 | `3aec6546fdd668cdbe7cee7fddeb7a8432893b18e09b532f3daebf635fce756b` | 0 |
| xrpl/account/main.py | 3376 | `4167a7c34e1a05e31671555f169aa3d1ee4cd316ed8ae92ce20a720bc6844f52` | 0 |
| xrpl/account/transaction_history.py | 777 | `f755bccad6658903b65ea2d5cf89655bb7c6f245d5a669abcab3fc1e1136dfd1` | 0 |
| xrpl/asyncio/__init__.py | 190 | `18c11dd759e66adf52fd026e01ea79ef720a4144b631e31bf60c7edb48b37295` | 0 |
| xrpl/asyncio/account/__init__.py | 416 | `cd1934211e0c4bc4e16d103375db2ea8a6edf0e321450ac1fbd4b55ce4dfbdeb` | 0 |
| xrpl/asyncio/account/main.py | 4245 | `301b6e799957bcf66506283866901d605fbab9d2a8123f159b4171de38cd360f` | 0 |
| xrpl/asyncio/account/transaction_history.py | 1171 | `65f772b25ce737b36e56964a8d91d34f71c8f878cb52bb9d49c72e5364a3823d` | 0 |
| xrpl/asyncio/clients/__init__.py | 706 | `423e35b6ffb86bf42850676fa21a7f21fa1119f5c9407b7d5b6c12dfac954ce0` | 0 |
| xrpl/asyncio/clients/async_client.py | 722 | `6b671ce2420b1cc9c34ef33b1cff51a7725fe0a4d761eb5e7ed43f2276a87881` | 0 |
| xrpl/asyncio/clients/async_json_rpc_client.py | 316 | `77070bf9683a7fd69af62b03eb7e8828e0296af669f04a728ec19c484e5b0e25` | 0 |
| xrpl/asyncio/clients/async_websocket_client.py | 10432 | `cf5df65e4c30ae3f922380e15d37a519543ad3304356d8ba033b4489ee3743bc` | 0 |
| xrpl/asyncio/clients/client.py | 2522 | `d8c5b454ec97a96b56fc95dda9bbfc5f8c9b528dac56062e0612d6ae649004cb` | 0 |
| xrpl/asyncio/clients/exceptions.py | 1097 | `0da93b66301190faeba091ab056806c1bcdacf144142d0c397567e1e863a0944` | 0 |
| xrpl/asyncio/clients/json_rpc_base.py | 1757 | `f28973c54eaf45688b40208430ed765f6a1c0243cba4991de89d4534bfb6424c` | 0 |
| xrpl/asyncio/clients/utils.py | 3341 | `a35d6d5d863bfd7c70004ad7cd170e83d692ac9b4cf817170bcbb68c38377b86` | 0 |
| xrpl/asyncio/clients/websocket_base.py | 9209 | `61bb34b32c91f7c03fd085d9135a0d06746efd61af76fcfb3618b9a23d504d68` | 0 |
| xrpl/asyncio/ledger/__init__.py | 329 | `447f72bbfa11bd13b81fc482a424c69fd40bc73832dc3773996967e636f3380c` | 0 |
| xrpl/asyncio/ledger/main.py | 4465 | `b0b783cd92cf1174897aabbab03239ee3e29974ce0c3f06b53c3d8ff1c4d506c` | 0 |
| xrpl/asyncio/ledger/utils.py | 2353 | `7fd161e50988e73a9629181573240af57d62ad6321884a8d2a1d73f5951d3a75` | 0 |
| xrpl/asyncio/transaction/__init__.py | 684 | `60fd524c2a3dfbdc32bb1e8665945e51cac4a9b8aa495020953da27980af7eab` | 0 |
| xrpl/asyncio/transaction/main.py | 28958 | `9c7b602be5588bef91d2ca829eff020293bc2201c33834529847c784ea44eaf6` | 0 |
| xrpl/asyncio/transaction/reliable_submission.py | 9988 | `084e1f7f475017f77c41be696e094d495e5e17b46bb439aa40e67f6fd13f7c2b` | 0 |
| xrpl/asyncio/wallet/__init__.py | 220 | `575e4b869960b9b3e9401ac3af7ef2b0fff7d078e9d29d95eb1e24fdfca7778a` | 0 |
| xrpl/asyncio/wallet/wallet_generation.py | 9038 | `33d0c58a0ee6008283ce407f999101cba0d9f1e2677fb07da90dab327984f058` | 0 |
| xrpl/clients/__init__.py | 657 | `03b05e7a758768249691d47242b3b8112519a6e16ea8a531ed3da42e001745a6` | 0 |
| xrpl/clients/json_rpc_client.py | 296 | `255c7dd8108cd7cee84c4444880dffebf7483c67fbec38dd03612a62610b188f` | 0 |
| xrpl/clients/sync_client.py | 736 | `1393688493c2d35cfcec3b828e6e445df03c83e0fe0b532293955f97fa804e8c` | 0 |
| xrpl/clients/websocket_client.py | 8936 | `f70d50bc1ae558669595fa25c3dc9f416e546bad31df9a399b0dcf81342e6d01` | 0 |
| xrpl/constants.py | 1755 | `8ca50f0823ddf5fba6d4de092e8177a92031cba00b9fdf1e8e4ce723dadbad56` | 0 |
| xrpl/core/__init__.py | 172 | `2ae2dd5d80b684b284b0025ff5de584613a4b3e943da76a230d6790c0c0e18cb` | 0 |
| xrpl/core/addresscodec/__init__.py | 1132 | `3b7167d52311a1a2afb9483c1a457324390567c1ed566dc6cea56be58d8cc520` | 0 |
| xrpl/core/addresscodec/codec.py | 7175 | `0d7ea0ba013f58eb968ebcb8cde75e19b1ba6352da9c3b6b6d6fc0d25d75e2cc` | 0 |
| xrpl/core/addresscodec/exceptions.py | 195 | `ed9857809cb8ccfd0f66242c862814d3d4df1a9777bd0e42c952038c7b028b81` | 0 |
| xrpl/core/addresscodec/main.py | 5735 | `63c845b52f601f49b5a8f5c454ad7a649bf059aefde8bef07deeb650f5829a5f` | 0 |
| xrpl/core/addresscodec/utils.py | 238 | `c009904737284fcf9655ce363609339598290a119349e41e27c981915ec013b2` | 0 |
| xrpl/core/binarycodec/__init__.py | 855 | `7f85b5979191587b70c706e5fab84d2ab1b43f338f5c9563920249c0bb6ae209` | 0 |
| xrpl/core/binarycodec/binary_wrappers/__init__.py | 297 | `7878ed49c31893c817f3c33ff1608be4f7e4f365eeff587571c7a7bad9be03e3` | 0 |
| xrpl/core/binarycodec/binary_wrappers/binary_parser.py | 8941 | `61cac6c96bfacef279e0a2004fe80d9d5077e7eb0320016c036bafda932fd825` | 0 |
| xrpl/core/binarycodec/binary_wrappers/binary_serializer.py | 4596 | `d52d3f3d6443fbdb00216bcabae408899cf1a9290b19517a3ee23a60ae7cbc48` | 0 |
| xrpl/core/binarycodec/definitions/__init__.py | 1174 | `4747d801e2388ab46c25d3c48c099bb72c989d69156d1bea1754c0d79f1e56aa` | 0 |
| xrpl/core/binarycodec/definitions/definitions.py | 9973 | `147e6e79cef80a3254a47c30ce986953fcb1c1777089f5465912e04bcf7e2ba4` | 0 |
| xrpl/core/binarycodec/definitions/field_header.py | 2062 | `8787ba9eb970e65478c1f0783e8e05f0a284c1ce0e6be784e269b48c0bfac0f9` | 0 |
| xrpl/core/binarycodec/definitions/field_info.py | 1224 | `4a09a70f2a11ee5c637e46c2c2949018c718cd81d173bf61a234bf4986540f5e` | 0 |
| xrpl/core/binarycodec/definitions/field_instance.py | 1959 | `6275d5a80567585f11c3905ee8238b2415923eb8134d7c79725ca3b8612a01a9` | 0 |
| xrpl/core/binarycodec/exceptions.py | 192 | `2dab9a44d1c037e5236a44ab737b2b71881459e8cffbc5c031d5733702fe9c91` | 0 |
| xrpl/core/binarycodec/field_id_codec.py | 3942 | `f022f1aaeed1ab9df9ddee767b264acb27bde5aa69f656b2839ea33a996e5b8e` | 0 |
| xrpl/core/binarycodec/main.py | 8633 | `808cb19ff4cffd203e13e3794fbc3a39f6d2772122d8fe12f676da7c5afaf2ba` | 0 |
| xrpl/core/binarycodec/types/__init__.py | 1612 | `c910479619cfe71dfce27b5b333036dee6260fcdd3693c8834e2ad65524492f3` | 0 |
| xrpl/core/binarycodec/types/account_id.py | 2943 | `1c3b4f1ba4812fcfd97ac61d6bda5825684eec49c8f032801167cb30ab983840` | 0 |
| xrpl/core/binarycodec/types/amount.py | 17652 | `5168afb51b569fb0d0ea1f786094f522a424b90928c0c4e12bb81a3b02585d12` | 0 |
| xrpl/core/binarycodec/types/blob.py | 1987 | `d4e3139c4f0b3272bc01f529f134f21811a69982318b2851d9e0fba1be45bf17` | 0 |
| xrpl/core/binarycodec/types/currency.py | 4333 | `78ecd894d4aee6282feed0b9b4d3e856c7bfea99d7fa8d5d7c92e4e25d9250a0` | 0 |
| xrpl/core/binarycodec/types/hash.py | 2677 | `a466f2a1ba26446d7382d26fbcb2565f6846b968f7874b4afa266485b07c97a8` | 0 |
| xrpl/core/binarycodec/types/hash128.py | 1522 | `a545f460f06e06267832cee683fee54de4ed56a99d1752d768fb6c8068e8c980` | 0 |
| xrpl/core/binarycodec/types/hash160.py | 605 | `78492ecf2dea00bf88d2a1d8a2953d595329d928e7aa0e3688352b9dff3b6250` | 0 |
| xrpl/core/binarycodec/types/hash192.py | 625 | `cf2927b317ac0c2ed50e78c62a0f0bf4f29285a488c9e631d2e7185889396dbb` | 0 |
| xrpl/core/binarycodec/types/hash256.py | 606 | `e6af8fef248c700b2dfc7f2ad9bc11934d27caff51ec7b4c6cbd436b62899a8e` | 0 |
| xrpl/core/binarycodec/types/int.py | 691 | `683dc4f85abd629b1859077a907d0373d7b2ea0da02ce5c04d0a7a9423b55079` | 0 |
| xrpl/core/binarycodec/types/int32.py | 2533 | `133ef36e4a9135970a3280b16fcf50c94af54aca0d63b74511a52ed772748357` | 0 |
| xrpl/core/binarycodec/types/issue.py | 7113 | `7f54a3619784f0f327bf3a62f61b8c253e39f5c53652d7f1b4972aa0477de5ba` | 0 |
| xrpl/core/binarycodec/types/number.py | 13010 | `c7f29d441fce50907bed2b3098ce8bd7e2178ab07f9f266124b3b0cecd3a75e3` | 0 |
| xrpl/core/binarycodec/types/path_set.py | 9014 | `fa614722181f059a97317cc5558e89e61207fab3bfb50848a056a6fc4f9cc716` | 0 |
| xrpl/core/binarycodec/types/serialized_type.py | 2759 | `02b8c5581e298b8058c4f06e4f63e43aa920d83471ad603302d5f7352b645c2c` | 0 |
| xrpl/core/binarycodec/types/st_array.py | 3284 | `59b866f0662ae20fa3b7116dfcb893e2e6be7cd21947ebc5ae2b904d3952b514` | 0 |
| xrpl/core/binarycodec/types/st_object.py | 9207 | `65906016cc76223c28fbe6c4fb5d30cd4ae30b911ede632c62f2fb8e427ab9a6` | 0 |
| xrpl/core/binarycodec/types/uint.py | 3468 | `92713bc2017770f0c96b569ae977401d4984445c26dc856974d407ec3f73caa0` | 0 |
| xrpl/core/binarycodec/types/uint16.py | 2060 | `e6fed9017291853deb8bd08baf649b2c897173366246ccf4c5aa2ab5c28817ff` | 0 |
| xrpl/core/binarycodec/types/uint32.py | 2280 | `c0ff238f74f66c05caebec305bef3ce169741f6b461e08ef4d4644ce3b11f32c` | 0 |
| xrpl/core/binarycodec/types/uint64.py | 3493 | `05565bbd1ba6d4ec50c5073b9f39fe21170a4bd3b4f115a7f911cc95b3c1439d` | 0 |
| xrpl/core/binarycodec/types/uint8.py | 1996 | `fadfb82a72d5c10511931f68fcac1aaeace4ef4c6bb35907e9d4f4b1b65fadc6` | 0 |
| xrpl/core/binarycodec/types/vector256.py | 2877 | `9909323aa7551632c86881b183eda377a14893205987644cd258da3be99d6a8a` | 0 |
| xrpl/core/binarycodec/types/xchain_bridge.py | 3425 | `d829a37e6c4ed20a2224072286cccd605fa0e30ab1435f91095a8f3593690bd9` | 0 |
| xrpl/core/keypairs/__init__.py | 448 | `e85e61c9ba8764a9059200e955242129bdba69680323cc640decc4e26e49845a` | 0 |
| xrpl/core/keypairs/crypto_implementation.py | 1247 | `30581e7f2df3d1e8733c1a5a5d0b165518a42a7d6793aab85c1f286dfd780268` | 0 |
| xrpl/core/keypairs/ed25519.py | 3654 | `e317d61726aeac7c1bf1d7957c3dc8f5e00eb8e40d40741fb63151b3798b524d` | 0 |
| xrpl/core/keypairs/exceptions.py | 183 | `364fb2fbd40e32acc9711b7c1963a99ec9beb9f6cf3bb0cba593c82240e96d9b` | 0 |
| xrpl/core/keypairs/helpers.py | 894 | `5300f0e1b70f5a19c2c664e67605f24ba85344390ddcfdcd2b5f9a510613cb3b` | 0 |
| xrpl/core/keypairs/main.py | 4882 | `cbbf8a4720afe6bb2ea4f70ce5abc9383e53e38d64a170f01a55a17a51b080cd` | 0 |
| xrpl/core/keypairs/secp256k1.py | 7432 | `5c05922dc4ec7ba5bda6bd37c3b10ff047bf081a3842b5eb5fc404a71aae5af9` | 0 |
| xrpl/ext/confidential/__init__.py | 4560 | `7d747fe9cb85d038806c7c9acbcbd574c422edeab2eae0197f4dac9fd7f6af12` | 0 |
| xrpl/ext/confidential/build_mpt_crypto.py | 14268 | `484ad4b5ee8991339b0ca71b8e6d93bd1a1f9457a5b37b25602fb366ed69bcdd` | 0 |
| xrpl/ext/confidential/commitments.py | 6646 | `b0ff6cae2f70b730d9f9e477018e3cdc868fa3ccbaf151257bea1182f907f1bb` | 0 |
| xrpl/ext/confidential/context.py | 10887 | `e19eaf8925a77b7e217aa1994fe1afcdd5cd5dd390127f83e1339c5fb78c23c7` | 0 |
| xrpl/ext/confidential/crypto_bindings.py | 4186 | `07050fefaf3c229d0b0867bc4229ef4c96a0808e237b64f922cae7c8c219e346` | 0 |
| xrpl/ext/confidential/encryption.py | 4905 | `0b325bc3b9f6169ed22deca5781b4da2186cd2c13ef701f7fd72505a13b08af1` | 0 |
| xrpl/ext/confidential/homomorphic.py | 4676 | `fbcb34d5721f58b4e0b47c0063a49ef003ed1404b31e2fec0763b48d2735b7f1` | 0 |
| xrpl/ext/confidential/include/mpt_protocol.h | 1300 | `341b4dd4c9ac01d45bcbce7d5de4c9354773eb83ee5caf6a54bc8065f92dadc5` | 0 |
| xrpl/ext/confidential/include/secp256k1.h | 42764 | `8ba347fedd24e0a9df2cfe9c58aa68f82ccac6a8737a5053add13254c62ffe65` | 0 |
| xrpl/ext/confidential/include/secp256k1_mpt.h | 16209 | `ee1a061db0bae3c1b9259aee21a989ff2a5df3e15f5267eb8f54ff6eba054a03` | 0 |
| xrpl/ext/confidential/include/utility/mpt_utility.h | 18927 | `909a063bb3643ceef2ffdc988fc112a4b99d46e32223b865dd58302ffe413fc3` | 0 |
| xrpl/ext/confidential/keypair.py | 4236 | `f956be13be45e4eb7120b663de09083382bbc6e137a28a51c5cee477c7f61d27` | 0 |
| xrpl/ext/confidential/main.py | 21242 | `dbf2a9ab17518c61536f2c278fd64f5035a5300cf8da1250a299a73f93ca3ac1` | 0 |
| xrpl/ext/confidential/transaction_builders.py | 63365 | `3314d09109ce311b08c392c093145682f1f4c487c64cefbdf10b7e3dfe3beca8` | 0 |
| xrpl/ledger/__init__.py | 315 | `5971c3bd4eb7ae20cb9d96f60a253f73d9c07f7c6590e907229f5f5362b6b088` | 0 |
| xrpl/ledger/main.py | 2283 | `3884908d9c7d4c39e15f6ba615b5fb37f641c67c816f38c2f42ac8e5ea810430` | 0 |
| xrpl/models/__init__.py | 1124 | `09571198140246d378a93623a0b0b28186f29482a4f853ab669a3ecdac88b69b` | 0 |
| xrpl/models/amounts/__init__.py | 679 | `a6f80f1375b979553a83cfabed74439c7e6a3cfab7a4aa4e6a7e28f00957ffd7` | 0 |
| xrpl/models/amounts/amount.py | 2009 | `c0b08cd1d2d0a6bba41b4e74b5919fdc6ecb46c28deddc278719df57fc2aa361` | 0 |
| xrpl/models/amounts/clawback_amount.py | 464 | `a8c7f0163a0e44e2e91eeb08e639dee8d6e009b546d3ec21d13df9064059fa9c` | 0 |
| xrpl/models/amounts/issued_currency_amount.py | 1275 | `d427fb47e06aa492252a0a8eef0c6555514b77a1f2a9403dafd911342b1b46ed` | 0 |
| xrpl/models/amounts/mpt_amount.py | 1140 | `20b8f1cc33bc8353d3c96951ecf66b5f6e3bc384f57c626484760178117479f3` | 0 |
| xrpl/models/auth_account.py | 456 | `bfa4dcd453173ccaf2b2c29be26173fd69117305c225fc36011022066b0c22bc` | 0 |
| xrpl/models/base_model.py | 16298 | `621595716a19459f0f2d4ab6d7a7afe7f06e8c76d8554bbe04cd268d4a4cd46c` | 0 |
| xrpl/models/currencies/__init__.py | 458 | `a8bd15582dff27dd5feafd9900df06cc71f6402882ee033028cce7ce9519385b` | 0 |
| xrpl/models/currencies/currency.py | 393 | `f30e402ac0a6d22b96e3971474fe4712250a5a9f5d48e2ce8a18ff8e9a7a7e7b` | 0 |
| xrpl/models/currencies/issued_currency.py | 2159 | `02f77ae144a3eebc8e521f3973b8fcbc1a406a783ad03936442192f4ac3342b8` | 0 |
| xrpl/models/currencies/mpt_currency.py | 1770 | `af0e95cddb67cecb5b14877c8eeb653d847282a35183076ec147b2bd23171f74` | 0 |
| xrpl/models/currencies/xrp.py | 2897 | `543b3dbc66a3cb1e3ad3fa61a422ef711dd08f8857c37f8b34902820c03a0c92` | 0 |
| xrpl/models/exceptions.py | 172 | `e287cdc7cdf3e715ef84eebeeb20fa9118f5b672604456c3c84ca4038a9ac6f1` | 0 |
| xrpl/models/flags.py | 3958 | `92d662c63aed9d9462babdba9f5a6ad59e5427713e52933f23124808c136a076` | 0 |
| xrpl/models/mptoken_metadata.py | 3495 | `aad0743d8b31784e99beec8e4cb2380b8d3f132d98cd86abb54b06560c928363` | 0 |
| xrpl/models/nested_model.py | 2392 | `0189bb6e4e009d24cc25c1d986da82585c225b4151b4bfcdcd376b31774c82a9` | 0 |
| xrpl/models/path.py | 2045 | `48677fc62695b73d13a279cbbd5b256c3364c9232af3a8c22b24e2d24f4cfb1c` | 0 |
| xrpl/models/requests/__init__.py | 4215 | `ca44595cf252039253415111a4f00d4bfd1a4058c8031062f70031bfa4b0cbc1` | 0 |
| xrpl/models/requests/account_channels.py | 1471 | `e7cc3cf63e06ba83ce1f7915475a613211fc25d0323b299773ce4a3f63032219` | 0 |
| xrpl/models/requests/account_currencies.py | 1056 | `bf010412c73d5e937729696234e2a80c72ac938b1c00a57a525e6dcd8b0295b4` | 0 |
| xrpl/models/requests/account_info.py | 1010 | `e1c550abf031855bafd064f794389e313c39dd1b1e55f861e021fbe4b25296fd` | 0 |
| xrpl/models/requests/account_lines.py | 1245 | `9fe808b21469722695eaecb71ec8b2c33675d8671918a493e5601ced0bc90126` | 0 |
| xrpl/models/requests/account_nfts.py | 1138 | `5364e38d85ecb418a048cea170d3936c442c5ec016c78dd6db445658cbec9651` | 0 |
| xrpl/models/requests/account_objects.py | 2197 | `e981839650526e4e83dbc70f44839a3262a047138c5bc9d9a8c5ef66721f12f6` | 0 |
| xrpl/models/requests/account_offers.py | 1083 | `c7d747fed0577529e910654b617bada0a010957985fc9904d59a061e1b016043` | 0 |
| xrpl/models/requests/account_tx.py | 1129 | `40d5d06feeaa7e575adaceba328c496a39a2b7394135d79ecf177f0906e3e351` | 0 |
| xrpl/models/requests/amm_info.py | 1287 | `6ecbd96e4c36f9a9df01468f787f10185f461b53898a3c59bf71eecd0d6f190b` | 0 |
| xrpl/models/requests/book_offers.py | 963 | `b7801b8ed61a5b89c00e8abc8360ecf9960ee6c7b057410def6aa1422733495f` | 0 |
| xrpl/models/requests/channel_authorize.py | 2952 | `a03580bbb8f8b999f429532645118410262d58444d3bac98d03c8496a4cb3a66` | 0 |
| xrpl/models/requests/channel_verify.py | 1004 | `c2b9c5f9de2dc1e385683e447c0e8b8807924b0ef3f4c962f5d06eeca983cc29` | 0 |
| xrpl/models/requests/deposit_authorized.py | 1327 | `efbe3e33c462b850c21adeddeba72d29b92f4d1c0b52c1e721566df1360a401c` | 0 |
| xrpl/models/requests/feature.py | 542 | `b7da627453c882806a7c665e9fb2edef6311508dc1f9fb05fad48691a12bf8a2` | 0 |
| xrpl/models/requests/fee.py | 713 | `db38e997cb8c11c5c42767c19ae67b7f0f2cd3b8b265ae6c9c1def120585abcf` | 0 |
| xrpl/models/requests/gateway_balances.py | 998 | `e450e27453388f3698cc92c907c617468cf662a0b70beb5c4db88f5bf69c9c75` | 0 |
| xrpl/models/requests/generic_request.py | 3134 | `d9796f21e4a6a21b95c3a130ee73a6d3cd529116383d5611b802fce5bb5976c3` | 0 |
| xrpl/models/requests/get_aggregate_price.py | 1677 | `ed33544cdbb7d1ce2ae9b686451d857579ac8e521d48a263f873522db882688f` | 0 |
| xrpl/models/requests/ledger.py | 642 | `74d37f4269bb8fda952ff3203feb74ff5bd28b25f6fd0ebc0da7cd93f9169374` | 0 |
| xrpl/models/requests/ledger_closed.py | 608 | `6cb9d27208316d6f39596f789bf5519e2c94f2ecc232afa54aa81a845f952677` | 0 |
| xrpl/models/requests/ledger_current.py | 664 | `79ff353d8266a8574d7ec4fd60a095914b5aafb063252eb2d04db894488f041a` | 0 |
| xrpl/models/requests/ledger_data.py | 1128 | `5bb89bcef1ec01d3907914db1a2b814777b5faa0269afad92e4d0e9cc8425bb0` | 0 |
| xrpl/models/requests/ledger_entry.py | 10209 | `81e6138890b2a073cdfb4e0abfbdc905e0334281668691c7e3a553efb5e96293` | 0 |
| xrpl/models/requests/manifest.py | 775 | `547f39988a507d155b3ce8da121bfe10892010f308d594b0922406542e971866` | 0 |
| xrpl/models/requests/nft_buy_offers.py | 731 | `ef9fd3abcd6ed310419accd4adc670fc94949f0d94a665a97a8ccc10049b76b4` | 0 |
| xrpl/models/requests/nft_history.py | 1106 | `bf6bf984aa45e56fae5ea762df2ed2731954b9d6292d42664bc7fe5b56e0a221` | 0 |
| xrpl/models/requests/nft_info.py | 694 | `dcbda5ca89cab1d8c4f0aea847f1f9463962d789c7b544b526f1c0b87e158343` | 0 |
| xrpl/models/requests/nft_sell_offers.py | 738 | `8b9f8477c58861d073455145439492cecfc4a3b5c3c005e5390439fba74e0622` | 0 |
| xrpl/models/requests/nfts_by_issuer.py | 882 | `0a57a1a82a16a249d176c233764637bd6d983b7ec8e1e65db0f326c97d44d148` | 0 |
| xrpl/models/requests/no_ripple_check.py | 1352 | `9373fce4e3f83b169dcbbb504ea597cf38249a612880787b62c96df5791e362f` | 0 |
| xrpl/models/requests/path_find.py | 4254 | `978274eb65c28997301a28b1f0a1f936f7037b0cc95a1c26b55f0d46e2b9d662` | 0 |
| xrpl/models/requests/ping.py | 485 | `9a4f6848206d26baa41d73c1b09fc40e9d9b4edc400f560e86886e09839ea234` | 0 |
| xrpl/models/requests/random.py | 517 | `215b57258108f94fb8987a17c8ab3ead5b034f8e796da5cb28d20ae3fb846013` | 0 |
| xrpl/models/requests/request.py | 6957 | `35be4c3607da405d0c66e55c7f19f88742560423e845e629d38af91f28353ab2` | 0 |
| xrpl/models/requests/ripple_path_find.py | 2203 | `c661be8db0754f76b8dbd9e4e159cdf7a82eae357432cb9f787908e9f86f9f5d` | 0 |
| xrpl/models/requests/server_definitions.py | 630 | `eed3b31ac867503ba346927404a69ab9ce16f34d8288e864bd224699fb9f0f54` | 0 |
| xrpl/models/requests/server_info.py | 556 | `28a4c63d554a55b216ec47d885236612e1e76c9e103c192b271b954b5ca7d47f` | 0 |
| xrpl/models/requests/server_state.py | 1132 | `3b554ae9b5d56f81cc5bd49653044c0c42bc487bdaf8370ebcefe29378b80e09` | 0 |
| xrpl/models/requests/sign.py | 4106 | `2592c3f564c27af6e60ca069075addceb0a70ff1e06eac886b19b941c4aadb4b` | 0 |
| xrpl/models/requests/sign_and_submit.py | 5028 | `bac4e144be0cad86a2cccb8786bdfc81d9c73e30e7c676ddc13892c74a3ac47e` | 0 |
| xrpl/models/requests/sign_for.py | 3260 | `974befb94df4ae1d94a5f041198ac1517edc741e6a1fa74389d3c423c2ff90ef` | 0 |
| xrpl/models/requests/simulate.py | 3230 | `7bd606586a0efd9f9b4cf4cadcb49dabbb0a7cc77782f04e8be52bfa869c04bc` | 0 |
| xrpl/models/requests/submit.py | 3658 | `31aa70dd0a8029c960085cd9c85f374623465e8922e7b7194f1f4a6e6b3e9157` | 0 |
| xrpl/models/requests/submit_multisigned.py | 2361 | `672f3e9be5ab78452ff56cd6f56ab4709bd098d42b4e775821c3bcda4117e2b5` | 0 |
| xrpl/models/requests/submit_only.py | 2763 | `59732797e0159ba0fc882b5bbde15363127233504b89471d2c1f860453f7794d` | 0 |
| xrpl/models/requests/subscribe.py | 2016 | `7a26ad75e55eafeb84aada8ec53a72cb4cfb718edd3cdc1c49a9cde3c6e45016` | 0 |
| xrpl/models/requests/transaction_entry.py | 1121 | `1cf677cae565744e0242dd8cffd7a91248946d525d171edcb2fab82ce8df8640` | 0 |
| xrpl/models/requests/tx.py | 2604 | `93d3b55410e6a3f3e223cb874fe7eaeb2eb0b116d88139c520c6c5c5ea8211d0` | 0 |
| xrpl/models/requests/unsubscribe.py | 1491 | `02a0bc63e45cfc601ad95770c9dea43610226cd993f144e3278a3efc4e17f61b` | 0 |
| xrpl/models/requests/vault_info.py | 1683 | `204e0ae321e3d999a097a783325a0d2edeecb251ffc974dfed05da235a5af1cf` | 0 |
| xrpl/models/required.py | 288 | `97b2ff6cd4842f12c343067ad0372afbe5f9672e09bbadbe7fd98307df6a1ef3` | 0 |
| xrpl/models/response.py | 3571 | `7c5ca8ccb582675c8ff6cc73789348ee33ffae256b91247cd17916ea82c35702` | 0 |
| xrpl/models/transactions/__init__.py | 10227 | `8af29b14e3b5f05504c75a76c536a93cf0096f264babe7ef1949156d74cf83d0` | 0 |
| xrpl/models/transactions/account_delete.py | 1792 | `e10a997b978210eb51497b648b31bca0730e5ab89674770b10aed0d359f9fd44` | 0 |
| xrpl/models/transactions/account_set.py | 9845 | `230290a960815a0881609a9fc1043d11eaedadb221d3436ff44c392d4d6f4bab` | 0 |
| xrpl/models/transactions/amm_bid.py | 2798 | `247da70390666ae9576a495ae7906830f70e1322b9d4aaf22e7f9469f48f310b` | 0 |
| xrpl/models/transactions/amm_clawback.py | 3659 | `84dec014d7e6d2b3b61f1bba6945968ee7926fed0eaa200b3bd13801a17ccbcb` | 0 |
| xrpl/models/transactions/amm_create.py | 2672 | `954abc9bf6a04183fd295bba9a9592efee49b6c810e60debc4eec5311f6de4c2` | 0 |
| xrpl/models/transactions/amm_delete.py | 1552 | `6a2044ae1c0e5216f5d43d2ddb1d9b7367386b911157da65647d1f62d561f397` | 0 |
| xrpl/models/transactions/amm_deposit.py | 3271 | `5ef3e1d5c343bebd30d59039d13b3e8d8c6e5c9d4bee8f9607b2c77c8434440f` | 0 |
| xrpl/models/transactions/amm_vote.py | 1938 | `2125f28f095a6de10e4c351d7eb290466a6372f02e25bcf8b20b4eaf21b55d2d` | 0 |
| xrpl/models/transactions/amm_withdraw.py | 3015 | `6efbfb5d00028a839676dd299a808ca39dbfe16d521d230467fa40f4746f6ed9` | 0 |
| xrpl/models/transactions/batch.py | 6558 | `b4a4861547839fb8391cd71b121fa55b2258a9a89cd81e775f8d00ac5f5c22a2` | 0 |
| xrpl/models/transactions/check_cancel.py | 1023 | `79fb8037f0af4c84e8f3d56d5f57f9cd94ef12af83bf5560566638c5749ecc61` | 0 |
| xrpl/models/transactions/check_cash.py | 1948 | `48c3a6ad0f6824e92ef44f89906747f5ec17375c47e9fb3bcd082332579d73ea` | 0 |
| xrpl/models/transactions/check_create.py | 1840 | `3417702f977047a87912ec794241f4fa4244c2ebd963e0caf9fc6589ae58dcc8` | 0 |
| xrpl/models/transactions/clawback.py | 1947 | `1285a6e99e2928d532f81d0d635b17e1ea8607590d8d4ecf1418328ffc22d52d` | 0 |
| xrpl/models/transactions/confidential_mpt_clawback.py | 3539 | `23d05ef9071f23f1446cd04d438927442ee5bbb31358e4133d9d6a4067390b84` | 0 |
| xrpl/models/transactions/confidential_mpt_constants.py | 6198 | `c5359c8d7b8872a78d9de9afc6dc989ebec9a65998a1cbd978e4f585a066d2ce` | 0 |
| xrpl/models/transactions/confidential_mpt_convert.py | 7242 | `9d093c52de7c23dcc3401de8af658fa90c13eff5efdb913a04a9d8b56a082a4e` | 0 |
| xrpl/models/transactions/confidential_mpt_convert_back.py | 5554 | `278127bd04428d806d1513f7ddccdd71f0cf1729180bacc8cdfe828056dee00a` | 0 |
| xrpl/models/transactions/confidential_mpt_merge_inbox.py | 2011 | `03bde49c51f91afe35a7d03f3d68c38e4dd7f87d95ac643763acbe010c130dce` | 0 |
| xrpl/models/transactions/confidential_mpt_send.py | 6704 | `38824cee9ffa04fb2b64b76109fd6cd4878d7e3392b9f5166da91b1945dcc139` | 0 |
| xrpl/models/transactions/credential_accept.py | 1367 | `3a62cd36ceb6cb89a60fa4d0240f78f86e28d219ea38ca4505271de8aec37d36` | 0 |
| xrpl/models/transactions/credential_create.py | 2106 | `6df33b0dd75c15f24f752638b3532dd07e287ea378b8c9f1b8f9f722752e5dc7` | 0 |
| xrpl/models/transactions/credential_delete.py | 1529 | `f229bdce5cafc99aa6563232ab9bac73010465df37e9b11ef87ee7e2bf222038` | 0 |
| xrpl/models/transactions/delegate_set.py | 4420 | `4dbea8d53816945646412d24e6c53fb51e1d5b0e1a7e9b90a43dd79e2e9665a8` | 0 |
| xrpl/models/transactions/deposit_preauth.py | 4543 | `622d9347b26426980c0ac88bc2f11d8060e31192885bd4221012b61dce05d0af` | 0 |
| xrpl/models/transactions/did_delete.py | 477 | `61d6e20eca91a23f8701ff91c092f46c04cdd850e5ff7d5d2636c240bd3572a7` | 0 |
| xrpl/models/transactions/did_set.py | 2559 | `4e41a321c18f4aca622b0802455f6689d163c2e673d45e4e8c60a74ab3a964ae` | 0 |
| xrpl/models/transactions/escrow_cancel.py | 974 | `9ffffdb98024122495f5bd40b82f1bccb2c9382ec0e1496dc2623d7edef3642d` | 0 |
| xrpl/models/transactions/escrow_create.py | 2741 | `773a85a989bc6c82cf04d401baaf0d465ac47074751c58bdcad10e835eac88ca` | 0 |
| xrpl/models/transactions/escrow_finish.py | 2344 | `58904099353f1d62a3aaaae7b572da86f780c4475460006468f318d4be269e59` | 0 |
| xrpl/models/transactions/loan_broker_cover_clawback.py | 2156 | `f5d8d89b542fa37d3288790b44e0d36797fde0393761898858d28d714799d935` | 0 |
| xrpl/models/transactions/loan_broker_cover_deposit.py | 850 | `4ad15bb42bf0b44057dbcdcfb5535dc770c0a6d2e718699819f5f8960d81ee23` | 0 |
| xrpl/models/transactions/loan_broker_cover_withdraw.py | 1814 | `aae51d65e013f7462239532e7a7b890f484ddf9c82db6ba0eaeb832e3f73307d` | 0 |
| xrpl/models/transactions/loan_broker_delete.py | 705 | `db076c6c940bbcba88b3dcc6f00358cfefe547a305b007fed53f0c7b753318d0` | 0 |
| xrpl/models/transactions/loan_broker_set.py | 3800 | `7df3351356516bff46fdbce4d9c043fc7c805241f7ef542f62e38de29ca611e9` | 0 |
| xrpl/models/transactions/loan_delete.py | 677 | `a9febe2332c0f1da6457d908622d5a686273f00405a31a27a4912b76966a6eb0` | 0 |
| xrpl/models/transactions/loan_manage.py | 1528 | `39596842ee819b93f4c75179c313369c128cd333077e1024b6f4166a14c5645a` | 0 |
| xrpl/models/transactions/loan_pay.py | 2466 | `94463e316bb21c553e1b9417712b7e6358dce78f0ca44806fe5688c3539d136e` | 0 |
| xrpl/models/transactions/loan_set.py | 7535 | `ae56a4f798cd80e3f76839fee5e4863aeef7d8ce6edc1235bd9f244bcd293dbd` | 0 |
| xrpl/models/transactions/metadata.py | 3241 | `2956b5b5befc6b88bf42a4f91efc0dd905d85100a9dd88af41d544424fc2f5f7` | 0 |
| xrpl/models/transactions/mptoken_authorize.py | 2014 | `d82e3249af33e400ba55524bd11a1d22e1f4675bdb41098e36295c4920d7289d` | 0 |
| xrpl/models/transactions/mptoken_issuance_create.py | 8657 | `989fefd987b2b67826358379c39662d76553b7b08fdc60271a1c3d6bbd4c4f3a` | 0 |
| xrpl/models/transactions/mptoken_issuance_destroy.py | 1062 | `8fc0d80da5c91aaadd50bac9b787e9aa6423c6b29e13a97a475d369800e6be42` | 0 |
| xrpl/models/transactions/mptoken_issuance_set.py | 11296 | `87e63e92b1d3d989879e2f997b67436eb997605f2896eb7737ac1dc61945ed0f` | 0 |
| xrpl/models/transactions/nftoken_accept_offer.py | 4455 | `22b3cc43cf29644f5b01058aa5acd63dda94d0bf26038e2050742aad1b2137f6` | 0 |
| xrpl/models/transactions/nftoken_burn.py | 1674 | `7552c86b624a7acca064cf99eabb835316753cdf986258ff43cc9613fc38a250` | 0 |
| xrpl/models/transactions/nftoken_cancel_offer.py | 1945 | `4f00e912af153eba97c8ed87626a280609f90513b921cbefef159459117a609c` | 0 |
| xrpl/models/transactions/nftoken_create_offer.py | 4203 | `6d50d5c3ec206560fb73fda4e747c8705d401b960c047abf9b0b71a92b87f87e` | 0 |
| xrpl/models/transactions/nftoken_mint.py | 6507 | `e9b074321731a6c6b7cb17890403b03d4cee75dd15b77a6f76b8c5c6fe5d37e7` | 0 |
| xrpl/models/transactions/nftoken_modify.py | 2138 | `31ade5f7323e28240227152c5782214e169ca40d11407fd8d81badecb9888796` | 0 |
| xrpl/models/transactions/offer_cancel.py | 967 | `55f22eb958f3f57a99b73f08d94dd992839a5273cd4a01daf41da71f1a78b74b` | 0 |
| xrpl/models/transactions/offer_create.py | 4653 | `c054825eeb5d0e3d72a9c9acc09ac683d7e02b4b3f4f5dc383d34bcdb0cadb9b` | 0 |
| xrpl/models/transactions/oracle_delete.py | 746 | `16d35c949224ab39c49593b0f4951fefe2cd520611e7cda7d6dd6cd98a6e6e42` | 0 |
| xrpl/models/transactions/oracle_set.py | 6974 | `53910849a14125a08d2585946cc60b7fab42b23f0afb948829b7d2f9a90bd5fb` | 0 |
| xrpl/models/transactions/payment.py | 8519 | `d7db87740128a53ef486128c0b7c5af57427b34a7c46b57d05380583ba7008fa` | 0 |
| xrpl/models/transactions/payment_channel_claim.py | 4279 | `ad1244ab12b1e7aa4c3a56dc484da996bf042c002c15277fdd1cb69a14ccaa97` | 0 |
| xrpl/models/transactions/payment_channel_create.py | 2241 | `e5045ccea43196ef8ebb73af11db40f77b97e4bbf5a3645073be32765fac0e9c` | 0 |
| xrpl/models/transactions/payment_channel_fund.py | 1520 | `07d8850060b379bcfd425a97fd4a684a57d6d606f6134e62ebfe04acb55d50ba` | 0 |
| xrpl/models/transactions/permissioned_domain_delete.py | 1348 | `d71ac35e2a10a70c6f6a1a953b46e3527b24c8eb87325710fcd7dcbcc76a9d4e` | 0 |
| xrpl/models/transactions/permissioned_domain_set.py | 1939 | `4ee995726aedabd3c4c532d6a772dfb46890d7d8166a2c6a7768e23ede777355` | 0 |
| xrpl/models/transactions/pseudo_transactions/__init__.py | 576 | `9ba6a2b6e78f66f64d9fde8040c71f17d22ee6b829c3522086e6c5723eefa878` | 0 |
| xrpl/models/transactions/pseudo_transactions/enable_amendment.py | 3633 | `aeed8843d4ff70b9df2a00d793cee47bbfa7b03a04af2401084678fc03d21190` | 0 |
| xrpl/models/transactions/pseudo_transactions/pseudo_transaction.py | 1287 | `78772808687df90e483bd80f9ab2c4d0548063e6250e28eb5cb286c46da5c974` | 0 |
| xrpl/models/transactions/pseudo_transactions/set_fee.py | 2640 | `2114fe1732d3286d449a7437655ed473c4c178ade1558d35dba252aa59209522` | 0 |
| xrpl/models/transactions/pseudo_transactions/unl_modify.py | 2255 | `76173a8d88e9c32a3771c111f2959f9af02e4d9da864baf702b9ed891e43be25` | 0 |
| xrpl/models/transactions/set_regular_key.py | 897 | `8e2b677770faa77b1ac44dee961ae8fd980582f0d47d63d6fa2387f9f90172bf` | 0 |
| xrpl/models/transactions/signer_list_set.py | 4992 | `670577838adc562c29e929d6fe2ad94d86a90cff8ef1d5d16111162040b66390` | 0 |
| xrpl/models/transactions/sponsorship_set.py | 11188 | `700ccfc6aabea8c15778dfc71bdb842b88778df4345f8159e454fcfe384e60bc` | 0 |
| xrpl/models/transactions/sponsorship_transfer.py | 4897 | `913e1e94f4f0c489bfa48010d014709f27a776f3b2484e68c1e531f6a4994902` | 0 |
| xrpl/models/transactions/ticket_create.py | 880 | `a426f7346eac0d8502a747c7515b4fb2ee263f7cefc52407ae3ca3c205976af7` | 0 |
| xrpl/models/transactions/transaction.py | 25728 | `b4a8415bd183e16301c618fb7c3aaddb04d2ca116966a820586b6385afdcf1de` | 0 |
| xrpl/models/transactions/trust_set.py | 2692 | `49fbfc75e6601ddd57a99518e550d1d74766350bdb17862e9c1161f7e3ee0725` | 0 |
| xrpl/models/transactions/types/__init__.py | 275 | `41bf097e140f4cc75a157591d3a658818dd4d325f5aee58df7fac046be57694f` | 0 |
| xrpl/models/transactions/types/pseudo_transaction_type.py | 287 | `b9200262dd753a6cb3144358a0d446fc122db7b0471a99e087502a1bce14b7e1` | 0 |
| xrpl/models/transactions/types/transaction_type.py | 3300 | `1f7608825453f160c50a5fdd07757983fa96f4d8c1fecd2db9f6a022d03cb5db` | 0 |
| xrpl/models/transactions/vault_clawback.py | 1377 | `d84aeb2119f7fb7f0e53a3b182c14c4555223d520c659700d1a3a64cd320ca18` | 0 |
| xrpl/models/transactions/vault_create.py | 11305 | `87143e378d363a959135b6e63052a2ca5bb2290d65901a8b2c20ae3cc6a7c4ed` | 0 |
| xrpl/models/transactions/vault_delete.py | 1527 | `5d6e528cfb71aa1beba28c61eca080156bfafb094605fd302dab7dd9873a2744` | 0 |
| xrpl/models/transactions/vault_deposit.py | 745 | `da9c8f527afbe133fde0862c49385985cd927009aa2fcd50bb671bbf0f1b0fab` | 0 |
| xrpl/models/transactions/vault_set.py | 2132 | `de69c518fc482b49804fad75a6699c95683916af5d2675720fdea225c27191fa` | 0 |
| xrpl/models/transactions/vault_withdraw.py | 1984 | `389d4db1df5d264b7474a5ed84cca606636f7a99349fc0faa75b15522e38bf50` | 0 |
| xrpl/models/transactions/xchain_account_create_commit.py | 2124 | `83fe794c38e003ef360a2360523bc91f55a748884be4f830d5ce4585d1d8bce0` | 0 |
| xrpl/models/transactions/xchain_add_account_create_attestation.py | 3044 | `ea8ffca38fb82a50670ee23392bb5e4eee705460058bb22b4d4b257f3aa19eba` | 0 |
| xrpl/models/transactions/xchain_add_claim_attestation.py | 2804 | `878dad3c43968e5bb236650b990058e98f301d24c81656a28a49fbe6d765a253` | 0 |
| xrpl/models/transactions/xchain_claim.py | 2881 | `54a60b35579a9240c0483aeff97bd28541f68defdfb710d554316e75e86af124` | 0 |
| xrpl/models/transactions/xchain_commit.py | 2124 | `7acb7714b76bdb56b5c451d34e0559439a39af4f09d2e321e960dd98c97de9b3` | 0 |
| xrpl/models/transactions/xchain_create_bridge.py | 3160 | `ec006774860a86aa99e205affb77a950c3de11e5039b71393afaf05100d919b4` | 0 |
| xrpl/models/transactions/xchain_create_claim_id.py | 2081 | `38de1f4c935914a1766c59ed4bcb9b12b8a0b36cf63d3fe46e23b1c468f727e9` | 0 |
| xrpl/models/transactions/xchain_modify_bridge.py | 3519 | `97bf9bcc39392ea781cedfc2dde49f2a403ff03e25744bd9e11bd22ed95a6377` | 0 |
| xrpl/models/types.py | 750 | `c5e52f465f32e20958b13e040c8935513d4abf499ef19cab9705a80306144dbc` | 0 |
| xrpl/models/utils.py | 4163 | `5141d776c917b82d2d9661a303391022bbe31f165d8f61f4be77d98232922b77` | 0 |
| xrpl/models/xchain_bridge.py | 1034 | `07a5b3d2d0715fd747e8cfd5edba0e1d5582fe5ee71465cf204775514e0a5f7f` | 0 |
| xrpl/transaction/__init__.py | 1237 | `3dfaac084831b8643f870ed5d8af0464e6df28ec2f8c731fedd41b158296b786` | 0 |
| xrpl/transaction/batch_signers.py | 10063 | `3a499780057c707beaef86fe20333ea5bf782e981a25953dbfe2bbcd28f3d442` | 0 |
| xrpl/transaction/counterparty_signer.py | 11234 | `a1b9ad604bc54eabee357b4c1648caf7b36820cb84a7e396591d5a0df7f9785b` | 0 |
| xrpl/transaction/main.py | 5435 | `86e9c9606caafcb9e9e96fe2ace316ad3cc8ac075e7803352eca9b4e25c3e719` | 0 |
| xrpl/transaction/multisign.py | 1217 | `66ccf79841ee19f8a61b5579e17acfec04d6f230a95b5d33844acfa9e65c9d4a` | 0 |
| xrpl/transaction/reliable_submission.py | 2665 | `c2e818c184e9da77b61a01e72656e0500f6315e4368d14c50ed1f5eb43b5beb6` | 0 |
| xrpl/transaction/sponsor_signer.py | 13466 | `06f55880b99165d40a1c7969f1220bf926972727f179b708facbb21c76a98c0a` | 0 |
| xrpl/utils/__init__.py | 1313 | `29dd5b6b0b16156ad4c7b7f9979027e0e62722eb16f7190e57a3ce20e27328ae` | 0 |
| xrpl/utils/get_nftoken_id.py | 4328 | `d01fbf1ab31fe742ef465d9cc83819c46aa2332d9258a0c1a4f9f3d34e318f04` | 0 |
| xrpl/utils/get_xchain_claim_id.py | 1517 | `708e6e708c745a590102440abd92704ba4f2856badab7e6aaf8eb0329017078f` | 0 |
| xrpl/utils/mptoken_metadata.py | 13651 | `3bd99f8df7fb897d2849d6be2aa1aa68581b4c91f13ffb026b3250a4f3b7c3ef` | 0 |
| xrpl/utils/parse_nftoken_id.py | 3413 | `2e8b6dbcb8fad25ea7b7bc7e72f7ef6120ba2669f1e365d17cecc28e03b1a0d0` | 0 |
| xrpl/utils/str_conversions.py | 788 | `c5280b6ef70e6e0095bf7c8b0e99febb26f69be1d76b85e0e7af61e5e8be8423` | 0 |
| xrpl/utils/time_conversions.py | 4202 | `8ae306f2ab8dc32c716c62824de6c7dbf3ad01b8d15bb0aab9e0c97c3f9bfb7f` | 0 |
| xrpl/utils/txn_parser/__init__.py | 350 | `8f30dfd895bf9879ab8798ea3d63fbecf6eb8e5eab8eb7d42928829db96153d8` | 0 |
| xrpl/utils/txn_parser/get_balance_changes.py | 1791 | `32098f990057f235ea4778fb498af9ab112f10c09f683e14c23772058d36e541` | 0 |
| xrpl/utils/txn_parser/get_final_balances.py | 1446 | `54edf35b6d957333950eb82427810af13d29d4d14eecd5ac8ea76d33f0db2b9b` | 0 |
| xrpl/utils/txn_parser/get_order_book_changes.py | 641 | `b63f2cba4b20e063b1bcee8694d9eb91f73f90074f880503adc7b40deb220f24` | 0 |
| xrpl/utils/txn_parser/utils/__init__.py | 627 | `f0be8051b26e2a75632eafe3e86abe5a8e58a77acd4110c3a0b784595ea23b61` | 0 |
| xrpl/utils/txn_parser/utils/balance_parser.py | 5218 | `2d853fe583f2681729e1a777c3c4338f9acae2d2a47dbc2b402bc262cfdde726` | 0 |
| xrpl/utils/txn_parser/utils/nodes.py | 2519 | `3f35ab75d10d3c9366d00195816272b8cb076a9a8604bad9c044e134ddb0b44b` | 0 |
| xrpl/utils/txn_parser/utils/order_book_parser.py | 6192 | `6e7bce4519c42346b25d2fb8d2591dd8c7c80624883fa86dba398ca5cad30dd5` | 0 |
| xrpl/utils/txn_parser/utils/parser.py | 1192 | `9138bc2f692ca3c1213f1b064803ea5170885498079b341fda3877af42f25cee` | 0 |
| xrpl/utils/txn_parser/utils/types.py | 1404 | `0f0eed1c695b985d2e5e88d3a362362224ad964c6873f3d061a2b91fee75afdb` | 0 |
| xrpl/utils/xrp_conversions.py | 3473 | `0d9713627d1e008d81af671cfc74d69cf46c6ca50ec7033e36103ad08523dc4b` | 0 |
| xrpl/wallet/__init__.py | 270 | `f1815095880541a72a1a1cf9eecaf4fef5f559233ece9f74a4bdd0da58f94484` | 0 |
| xrpl/wallet/main.py | 10507 | `35cb9c7475c1773166bae4ecd15a74ca2c884bf5bf824376b9066d0c6320b064` | 0 |
| xrpl/wallet/wallet_generation.py | 1640 | `61c006dd7697d308fde18876e898b719d1296e4e7b7e9ee83dcd7fa3b51f7394` | 0 |
