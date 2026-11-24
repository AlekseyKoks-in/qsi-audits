# Security & Post-Quantum Readiness Audit Report

**Project:** xrpl-ledger-app-xrp @ 7b5185ff09b4 · Ledger — public repository (passive review)
| | |
|---|---|
| Organization | QSI |
| Report date | 2026-11-24 12:24 UTC |
| Report version | 1 |
| Audit run | 345343e9-2f64-4950-8036-ec23bda5c312 (Document audit) |
| Analyzer engine | qsi-engine 1.20.0 |
| Risk profile | Web3 project |
| Content SHA-256 | `c3c6c789c3ff7b1075a42f180b251360901495f96c10be48a1093ee80df39b36` |
| Signature key (Ed25519 SHA-256 fingerprint, then the ML-DSA-65 one where it co-signs; the signature is the separate file report.sig.json) | `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e · ML-DSA-65 dbd4e297b3213d1d7577a565e76de14cc5ad0e409f1dc68291c67266fc95066a` |
> This report presents automated and documented analysis results for the stated scope. It is not a legal opinion, a certification or an attestation of compliance with any standard.

## 1. Executive summary

- Critical: **0**
- High: **0**
- Medium: **4**
- Low: **0**
- Info: **0**

- Confirmed technical vulnerability: 0
- Known vulnerable component: 0
- Confirmed configuration error: 0
- Potential cryptographic risk: 0
- Long-term post-quantum risk: 4
- Improvement recommendation: 0
- Insufficient data: 0

Mosca's inequality (x + y > z): x = 5, y = 5, z = 12 → tight margin. _z is a planning assumption chosen per risk profile, not a prediction. A cryptographically relevant quantum computer is not publicly known to exist today._

**Post-quantum maturity: Level 0 of 4 — no post-quantum cryptography.** Next step: Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

## 2. Scope and boundaries

Mode: Document audit

Repository: <https://github.com/LedgerHQ/app-xrp> @ `7b5185ff09b4b3d15df242b156a6aaadfc99f555` — evidence links open the lines at this commit.

61 files, 190607 bytes in total, 0 redaction(s); the per-file SHA-256 list is in appendix C.

## 3. Methodology

| Area | Status | Count | Examples |
|---|---|---|---|
| source_code | checked | 60 | src/apdu/constants.h: 42 lines scanned with 17 rule patterns and 340 registry patterns; src/apdu/entry.c: 57 lines scanned with 17 rule patterns and 340 registry patterns; src/apdu/entry.h: 24 lines scanned with 17 rule patterns and 340 registry patterns |
| entropy | checked | 1 | random-number generation: 60 code files read with 271 macro definitions from the tree; 0 ineffective guard(s), 0 weak random-bytes provider(s), 0 weak key-generation site(s) |

_Long lists are grouped here; the full per-file list is in the JSON report, signed with the same key._

## 4. Assets examined and not examined

- None

## 5. Architecture overview

Static review of the source tree xrpl-ledger-app-xrp at 7b5185ff09b4b3d15df242b156a6aaadfc99f555. 61 files analysed; of 6763 files, 6662 are test, fuzzing, benchmark or example code and were left out, 40 are not read by any analyzer, 0 exceed the per-file limit and 0 did not fit the total limit. Files no analyzer reads include: .clang-format, .clusterfuzzlite/Dockerfile, .clusterfuzzlite/build.sh, .clusterfuzzlite/project.yaml, .git-blame-ignore-revs. 30 files in build-output or dependency-cache directories (.git, .hg, .venv, __pycache__, build, dist, node_modules, target, vendor, venv) were not read. No requests were sent to the owner's systems.

## 6. Overall security posture

- Indicative posture index: **100** / 100 — _Derived from findings in scope (confirmed and potential issues weighted by severity). Indicative only; not comparable across differently scoped audits._
- Quantum-vulnerable share of inventory: 100.0%

## 7. Detailed findings

### QSI-2026-50300 — Quantum-vulnerable ECDSA: transaction and message signing (3 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:ECDSA:transaction_signing`
- Data source: src/apdu/messages/sign_transaction.c
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.20.0 · 2026-11-24 12:24 UTC
- Priority score: 33.0 / 100
- CVSS v3.1: not applicable

5 reference(s) to ECDSA across 3 file(s), e.g. src/apdu/messages/sign_transaction.c:100. Role, judged from paths, function names and nearby code: transaction and message signing. A CRQC derives the private key from a public key that is already known (on chain after the first spend, in reused addresses): funds and approvals controlled by these keys need a migration path.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open src/apdu/messages/sign_transaction.c:100 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [src/apdu/messages/sign_transaction.c](https://github.com/LedgerHQ/app-xrp/blob/7b5185ff09b4b3d15df242b156a6aaadfc99f555/src/apdu/messages/sign_transaction.c#L100) · line 100 · SHA-256 e30b6d6f765da2a317b8c538f6acbc075fe3008965877e6ad47f4f3cd7f9fd1d_

```
   99 | 
  100 |     if (tmp_ctx.transaction_context.curve == CX_CURVE_256K1) {
  101 |         cx_sha512_t hash;
```

_file_excerpt · [src/apdu/messages/sign_transaction.c](https://github.com/LedgerHQ/app-xrp/blob/7b5185ff09b4b3d15df242b156a6aaadfc99f555/src/apdu/messages/sign_transaction.c#L110) · line 110 · SHA-256 e213ba5ab23f8c8337d14a9f602f9e765f35f3cdad14a2f5ac5e7c96368edae7_

```
  109 |         tx = sizeof(G_io_apdu_buffer);
  110 |         CX_CHECK(cx_ecdsa_sign_no_throw(&private_key, CX_RND_RFC6979 | CX_LAST,
  111 |                                         CX_SHA256, key_buffer, 32,
```

_file_excerpt · [src/apdu/messages/sign_transaction.c](https://github.com/LedgerHQ/app-xrp/blob/7b5185ff09b4b3d15df242b156a6aaadfc99f555/src/apdu/messages/sign_transaction.c#L204) · line 204 · SHA-256 f662e2c23a17326ab8694984f0e078cd6a1df3477de3ecae1888ef7ab0f873cc_

```
  203 |     tmp_ctx.transaction_context.curve =
  204 |         (((p2 & P2_ED25519) != 0) ? CX_CURVE_Ed25519 : CX_CURVE_256K1);
  205 | 
```

_file_excerpt · [src/swap/handle_check_address.c](https://github.com/LedgerHQ/app-xrp/blob/7b5185ff09b4b3d15df242b156a6aaadfc99f555/src/swap/handle_check_address.c#L37) · line 37 · SHA-256 b42cd54e3d915d64c83513a541abf3eb6a99ba953a16bae0da9ddd12cde6928a_

```
   36 |     int error =
   37 |         get_public_key(CX_CURVE_256K1, bip32_path_ptr, bip32_path_length,
   38 |                        params_length, &public_key, NULL);
```

_file_excerpt · [src/xrp/xrp_helpers.c](https://github.com/LedgerHQ/app-xrp/blob/7b5185ff09b4b3d15df242b156a6aaadfc99f555/src/xrp/xrp_helpers.c#L147) · line 147 · SHA-256 b6b0de7721dd5c84793ac3eed115e6eb427a038acf2cf397641c8719a202f338_

```
  146 |                              xrp_pubkey_t* out) {
  147 |     if (public_key->curve == CX_CURVE_256K1) {
  148 |         out->buf[0] = ((public_key->W[64] & 1u) ? 0x03 : 0x02);
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains adopt them.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-50301 — Quantum-vulnerable Ed25519: transaction and message signing (2 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:Ed25519:transaction_signing`
- Data source: src/apdu/messages/sign_transaction.c
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.20.0 · 2026-11-24 12:24 UTC
- Priority score: 33.0 / 100
- CVSS v3.1: not applicable

3 reference(s) to Ed25519 across 2 file(s), e.g. src/apdu/messages/sign_transaction.c:115. Role, judged from paths, function names and nearby code: transaction and message signing. A CRQC derives the private key from a public key that is already known (on chain after the first spend, in reused addresses): funds and approvals controlled by these keys need a migration path.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open src/apdu/messages/sign_transaction.c:115 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [src/apdu/messages/sign_transaction.c](https://github.com/LedgerHQ/app-xrp/blob/7b5185ff09b4b3d15df242b156a6aaadfc99f555/src/apdu/messages/sign_transaction.c#L115) · line 115 · SHA-256 97a23e7186d26d562e8847491e95dcf5e8346ab9f4b06f0cdc213820be2bc9b4_

```
  114 |         size_t size;
  115 |         CX_CHECK(cx_eddsa_sign_no_throw(
  116 |             &private_key, CX_SHA512, tmp_ctx.transaction_context.raw_tx,
```

_file_excerpt · [src/apdu/messages/sign_transaction.c](https://github.com/LedgerHQ/app-xrp/blob/7b5185ff09b4b3d15df242b156a6aaadfc99f555/src/apdu/messages/sign_transaction.c#L204) · line 204 · SHA-256 f662e2c23a17326ab8694984f0e078cd6a1df3477de3ecae1888ef7ab0f873cc_

```
  203 |     tmp_ctx.transaction_context.curve =
  204 |         (((p2 & P2_ED25519) != 0) ? CX_CURVE_Ed25519 : CX_CURVE_256K1);
  205 | 
```

_file_excerpt · [src/xrp/xrp_pub_key.c](https://github.com/LedgerHQ/app-xrp/blob/7b5185ff09b4b3d15df242b156a6aaadfc99f555/src/xrp/xrp_pub_key.c#L24) · line 24 · SHA-256 4ab90166a46856aa933359078db80f2e0997f0a524ef683b6cdb658190d93ee0_

```
   23 |     // other supported value.
   24 |     cx_md_t pubkey_hash = (curve == CX_CURVE_Ed25519) ? CX_SHA512 : CX_SHA256;
   25 | 
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains adopt them.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-50298 — Quantum-vulnerable ECDSA: role not determined (1 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:ECDSA:general`
- Data source: src/apdu/messages/get_public_key.c
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.20.0 · 2026-11-24 12:24 UTC
- Priority score: 31.7 / 100
- CVSS v3.1: not applicable

1 reference(s) to ECDSA across 1 file(s), e.g. src/apdu/messages/get_public_key.c:106. Role, judged from paths, function names and nearby code: role not determined. The code does not show what the keys protect; review decides the priority.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open src/apdu/messages/get_public_key.c:106 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [src/apdu/messages/get_public_key.c](https://github.com/LedgerHQ/app-xrp/blob/7b5185ff09b4b3d15df242b156a6aaadfc99f555/src/apdu/messages/get_public_key.c#L106) · line 106 · SHA-256 56a3c0e14de6cef079997dd89749383db6b8d97d9e5471b2f4d9e69d0c71cc10_

```
  105 | 
  106 |     curve = (((p2 & P2_ED25519) != 0) ? CX_CURVE_Ed25519 : CX_CURVE_256K1);
  107 |     memset(&pending_pubkey_ctx, 0, sizeof(pending_pubkey_ctx));
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it; introduce an abstraction layer for crypto-agility.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-50299 — Quantum-vulnerable Ed25519: role not determined (1 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:Ed25519:general`
- Data source: src/apdu/messages/get_public_key.c
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.20.0 · 2026-11-24 12:24 UTC
- Priority score: 31.7 / 100
- CVSS v3.1: not applicable

1 reference(s) to Ed25519 across 1 file(s), e.g. src/apdu/messages/get_public_key.c:106. Role, judged from paths, function names and nearby code: role not determined. The code does not show what the keys protect; review decides the priority.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open src/apdu/messages/get_public_key.c:106 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [src/apdu/messages/get_public_key.c](https://github.com/LedgerHQ/app-xrp/blob/7b5185ff09b4b3d15df242b156a6aaadfc99f555/src/apdu/messages/get_public_key.c#L106) · line 106 · SHA-256 56a3c0e14de6cef079997dd89749383db6b8d97d9e5471b2f4d9e69d0c71cc10_

```
  105 | 
  106 |     curve = (((p2 & P2_ED25519) != 0) ? CX_CURVE_Ed25519 : CX_CURVE_256K1);
  107 |     memset(&pending_pubkey_ctx, 0, sizeof(pending_pubkey_ctx));
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it; introduce an abstraction layer for crypto-agility.

**Retest procedure.** Re-run the inventory after refactoring.


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


**Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

_Levels: 0 none; 1 present, not wired; 2 in use outside the critical paths; 3 hybrid in a critical path; 4 post-quantum by default in the critical paths (root of trust, key wrapping, channel key exchange). Judged from code and manifests._

### What the quantum-vulnerable algorithms do

| Role | Algorithms (files) | ID | First step |
|---|---|---|---|
| **transaction and message signing** | ECDSA (3), Ed25519 (2) | QSI-2026-50300, QSI-2026-50301 | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains adopt them |
| **role not determined** | ECDSA (1), Ed25519 (1) | QSI-2026-50298, QSI-2026-50299 | Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it; introduce an abstraction layer for crypto-agility |

_Roles are judged from file paths, function names and the code around each match; review confirms them. Root-of-trust keys and wrapped keys come first: they are hard to replace or can be recorded today._
No readiness questionnaire was completed for this project.

### Quantum algorithms relevant to this inventory

| Quantum algorithm | Effect | Attack model | Inventoried algorithms (rows) | What it means for this audit |
|---|---|---|---|---|
| Shor's algorithm — elliptic-curve discrete logarithms | breaks | Q1 | ECDSA (5), Ed25519 (3) | Elliptic-curve keys are expected to fall before RSA keys of comparable classical strength. On blockchains, coins whose public key is already on chain (reused addresses, pay-to-public-key and Taproot outputs) are exposed first; plan the move to post-quantum signatures and avoid key reuse in the meantime. |

_Effects: breaks — replace the algorithm; weakens — larger keys or outputs restore the margin; included in standard parameters — no action at standard parameter sets; only with superposition queries — not applicable to ordinary deployments._


## 9. Limitations and assumptions

- This report presents automated and documented analysis results for the stated scope. It is not a legal opinion, a certification or an attestation of compliance with any standard.
- z is a planning assumption chosen per risk profile, not a prediction. A cryptographically relevant quantum computer is not publicly known to exist today.

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
| P3 | QSI-2026-50300 | Add ECDSA usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-50301 | Add Ed25519 usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-50298 | Add ECDSA usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-50299 | Add Ed25519 usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P4 | QSI-2026-50300 | Plan migration of ECDSA to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-50301 | Plan migration of Ed25519 to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-50298 | Plan migration of ECDSA to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-50299 | Plan migration of Ed25519 to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |

## 11. Tools used

- blockchain 1.0.0
- certificates 1.2.0
- chain_map 1.0.0
- configs 1.1.0
- crediting 1.4.0
- dependencies 1.6.0
- hndl 1.0.0
- inventory_document 1.1.0
- key_storage 1.0.0
- mpc 1.0.0
- solidity 1.8.1
- source_code 1.11.0
- tls_code 1.1.0
- tls_live 1.0.0
- ton_contracts 1.0.0
- validator_keys 1.2.0
- wallet_login 1.0.0
- qsi-engine 1.20.0
- OSV.dev API v1

## 12. Sources and normative documents

1. C. Chevignard, P.-A. Fouque, A. Schrottenloher — Reducing the Number of Qubits in Quantum Discrete Logarithms on Elliptic Curves (IACR ePrint 2026/280) — IACR ePrint. <https://eprint.iacr.org/2026/280> (revision of a EUROCRYPT 2026 paper: 3.12n + o(n) qubits; for n = 256, 1193 qubits and 22 runs of 2^38.98 Toffoli gates)
2. Common Vulnerability Scoring System v3.1: Specification Document — FIRST. <https://www.first.org/cvss/v3.1/specification-document> (final)
3. D. Litinski — How to compute a 256-bit elliptic curve private key with only 50 million Toffoli gates (arXiv:2306.08585) — arXiv. <https://arxiv.org/abs/2306.08585> (preprint (2023-06-14): 6000 modules × 1152 physical qubits, one key per 10 minutes under its architecture assumptions)
4. FIPS 203 — Module-Lattice-Based Key-Encapsulation Mechanism Standard (ML-KEM) — NIST. <https://csrc.nist.gov/pubs/fips/203/final> (final (August 2024))
5. FIPS 204 — Module-Lattice-Based Digital Signature Standard (ML-DSA) — NIST. <https://csrc.nist.gov/pubs/fips/204/final> (final (August 2024))
6. FIPS 205 — Stateless Hash-Based Digital Signature Standard (SLH-DSA) — NIST. <https://csrc.nist.gov/pubs/fips/205/final> (final (August 2024))
7. J. Proos, C. Zalka — Shor's discrete logarithm quantum algorithm for elliptic curves (Quantum Inf. Comput. 3(4), 2003; arXiv:quant-ph/0301141) — Quantum Information & Computation. <https://doi.org/10.26421/QIC3.4-3> (peer-reviewed article)
8. M. Cain et al. — Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits (arXiv:2603.28627) — arXiv. <https://arxiv.org/abs/2603.28627> (preprint (2026-03-30): P-256 in a few days with 26,000 physical neutral-atom qubits; RSA-2048 one to two orders of magnitude longer)
9. M. Mosca — Cybersecurity in an Era with Quantum Computers: Will We Be Ready? (IEEE Security & Privacy, 2018) — IEEE. <https://doi.org/10.1109/MSP.2018.3761723> (peer-reviewed article; source of the x + y > z migration inequality)
10. M. Roetteler, M. Naehrig, K. Svore, K. Lauter — Quantum resource estimates for computing elliptic curve discrete logarithms (ASIACRYPT 2017) — IACR / arXiv. <https://arxiv.org/abs/1706.06752> (peer-reviewed article: at most 9n + 2⌈log2 n⌉ + 10 qubits and 448 n^3 log2 n + 4090 n^3 Toffoli gates)
11. NIST IR 8547 — Transition to Post-Quantum Cryptography Standards — NIST. <https://csrc.nist.gov/pubs/ir/8547/final> (final (2026-10-27; the initial public draft of November 2024 is obsoleted). Tables 2 and 4: ECDSA, EdDSA and RSA signatures, finite-field and elliptic-curve DH and MQV, and RSA key establishment are deprecated after 2030 and disallowed after 2035 at every key size — the draft deprecated only the 112-bit level. A composite (hybrid) key establishment stays FIPS 140-validatable while one input comes from an approved scheme. Repeats the federal deadlines of OMB M-26-15: post-quantum key establishment by 2030-12-31 and signatures by 2031-12-31 for high value assets and high impact systems)
12. P. W. Shor — Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms on a Quantum Computer (SIAM J. Comput., 1997) — SIAM. <https://doi.org/10.1137/S0097539795293172> (peer-reviewed article)
13. R. Babbush et al. — Securing Elliptic Curve Cryptocurrencies against Quantum Vulnerabilities: Resource Estimates and Mitigations (arXiv:2603.28846) — arXiv. <https://arxiv.org/abs/2603.28846> (preprint (2026-03-30, v2 2026-04-15): 256-bit ECDLP with < 1200 logical qubits and < 90 M Toffoli gates (or < 1450 and < 70 M); < 500,000 physical qubits at 10^-3 error, minutes)

## Appendices: Cryptographic inventory

By origin: own code 8 (8 Shor-breakable).

| Algorithm | Parameter | Library | Location | Quantum status | Classical status |
|---|---|---|---|---|---|
| ECDSA | secp256k1 |  | src/apdu/messages/get_public_key.c:106 | vulnerable (Shor) | acceptable |
| ECDSA | secp256k1 |  | src/apdu/messages/sign_transaction.c:100 | vulnerable (Shor) | acceptable |
| ECDSA |  |  | src/apdu/messages/sign_transaction.c:110 | vulnerable (Shor) | acceptable |
| ECDSA | secp256k1 |  | src/swap/handle_check_address.c:37 | vulnerable (Shor) | acceptable |
| ECDSA | secp256k1 |  | src/xrp/xrp_helpers.c:147 | vulnerable (Shor) | acceptable |
| Ed25519 | Ed25519 |  | src/apdu/messages/get_public_key.c:106 | vulnerable (Shor) | acceptable |
| Ed25519 | Ed25519 |  | src/apdu/messages/sign_transaction.c:115 | vulnerable (Shor) | acceptable |
| Ed25519 | Ed25519 |  | src/xrp/xrp_pub_key.c:24 | vulnerable (Shor) | acceptable |

## Appendices: Input files

| File | Size | SHA-256 | Redactions |
|---|---|---|---|
| doc/xrpapp.asc | 13599 | `0cb0fc700954bd614cfdf749365bfe55ce40b34c169c21e9faf3e699aa465e08` | 0 |
| src/apdu/constants.h | 1514 | `1c948301cd3c09c04b70635977cc4676f912b89747e29c56f7dbd65d14219c0b` | 0 |
| src/apdu/entry.c | 1909 | `238babd6201129cf5c71f6c5f6077e923fab2ac1ecfef577c9bd73dcfd521cf1` | 0 |
| src/apdu/entry.h | 914 | `449c63baef9e9a870060460db08439cfcf96b5bff3954c799d3dd35742b7332e` | 0 |
| src/apdu/global.c | 1238 | `fe1f9068f0f47bab3ea7c041d2e49a3d8ec7a83adb1f4be9208d71dad6f06ec7` | 0 |
| src/apdu/global.h | 2306 | `e65e3e41ca97d056077f670ad9cc5bb4ecd33d63d60bf77afc2b45408cf61348` | 0 |
| src/apdu/messages/get_app_configuration.c | 1116 | `34d989d87b3fbb24d829a6a1cbec13895d5af4cc721a56359e7df3ac5a771c78` | 0 |
| src/apdu/messages/get_app_configuration.h | 990 | `54bd7b663303b355d1476f926f50699b0574ee89fac05d5bd2d9f8eb72604898` | 0 |
| src/apdu/messages/get_public_key.c | 4924 | `49c0d00a12b961419c83066ea4d940bbbebeb4e7b000f473a7a075c4fdb0a526` | 0 |
| src/apdu/messages/get_public_key.h | 1028 | `bd5ddbb3d93adff5a024e8d4eeeacc2033f3745246287545c202b70618897b00` | 0 |
| src/apdu/messages/sign_transaction.c | 9253 | `d064e7e8518fcd28cf2c09acf1cd5fbef192b1dc4c14d75784fcfdc61822c6a0` | 0 |
| src/apdu/messages/sign_transaction.h | 1119 | `2d8d5d0adcfce85c7c75c837b04b2b3ceb31ad8efc11bb1d76302f711bbcd0d9` | 0 |
| src/app_main.c | 2362 | `723e36f359c0dfd693fb60959d0f33c5d2a4d0015e7662c9cb7ece7db29f3f46` | 0 |
| src/common.h | 901 | `92d0dce40e1aa61e20654845541d8bf31d47ae0402001e45240be642161a9973` | 0 |
| src/globals.h | 485 | `0aec6e34e1b2f441bba11429df801d46b14f95b8267fa3237a615f09cc2322b9` | 0 |
| src/limitations.h | 1393 | `5708eb66e5ea433968d28d60a3f3b22abf30f63d6d22131660bf78486c7ca950` | 0 |
| src/swap/handle_check_address.c | 1507 | `71c6a7d2f196bd5f49a4539e38a0fa381e953573de81e839cec28d21d0372651` | 0 |
| src/swap/handle_get_printable_amount.c | 565 | `8986b87e5867c39c29bfeb23dc1bc6278500a02ff46358df126fae8b28078391` | 0 |
| src/swap/handle_swap_sign_transaction.c | 1832 | `d611223451d97886c9b5aad745a0739802d2dd70b402eba201441f2852870100` | 0 |
| src/swap/handle_swap_sign_transaction.h | 241 | `ac7402499cd10a0ccce6e9a32910b5d21a0e4e465623841bb69734c24ada2839` | 0 |
| src/transaction/transaction.c | 6594 | `94cc2274ad568853771783b01b75cc61b0fc3d6760d76de1aad65c56d508bc03` | 0 |
| src/transaction/transaction.h | 1169 | `85d9a6c8808f4eb30be9047c2777131a62347a82e75a88a684bb5217cde66c0f` | 0 |
| src/ui/address/address_ui.h | 1222 | `f4e519feb6e85eb0ba56549e37b319f2df4c5fc190ca26aa9a0dad5c5d35b02e` | 0 |
| src/ui/address/address_ui_nbgl.c | 2023 | `cb29680a01e7d1eaf7aa71e5c98de27a4e65d2b3130150412df004239bb18d4d` | 0 |
| src/ui/main/idle_menu.h | 867 | `0e26d294e13e0b57fdd03eb20205794ce5f8a292dbf6b970f3eb22c4639afdd1` | 0 |
| src/ui/main/idle_menu_nbgl.c | 3999 | `5d8717a3066c127870a6a8bf40b8079dd5922aad613810f14cb5d3b789198289` | 0 |
| src/ui/other/blind_signing.c | 950 | `e15fad37eaff0c0d6e982be9d88cad2d291f8e01f64051d3fd92bed0fe26db2f` | 0 |
| src/ui/other/blind_signing.h | 60 | `4df97dd2ce4f17301b2a4b81db0deba0db120984c521ffe3aa9c578537d78548` | 0 |
| src/ui/transaction/review_menu.h | 1062 | `625b33a291b3b6ab71d84cbbf7a917e1c405e0b1dd107bfe83df6d516015dc70` | 0 |
| src/ui/transaction/review_menu_nbgl.c | 4475 | `6581e829c55f772792e9d6a8bbb572e886db76bbf8308aabc47ab68fb347a318` | 0 |
| src/ui/ui.h | 1246 | `ed68e2e52e071ec64bd69eb65b70b8d9cf8715b66ad2ca876c55f813f5b4541a` | 0 |
| src/xrp/amount.c | 9400 | `9f0398cdd99e174ef69071e7d22609054d48f479130e84817c8f35779473aa67` | 0 |
| src/xrp/amount.h | 1277 | `036bfc07a7f8ec3ba371fa03b4876c3496d074fd20c0276d60ccd15b567e2863` | 0 |
| src/xrp/array.h | 927 | `4898659d98034f5deeb527e5482eec332b80fd565b7ae50fa72aae2b6a406764` | 0 |
| src/xrp/ascii_strings.c | 1347 | `1d1e3f6f81c97db7ab0f49e23eb061e928ede5779a4f20c61ac7ede4addc2e4f` | 0 |
| src/xrp/ascii_strings.h | 114 | `f2190a080e316f101ac6d7b75523414ee587b31e3d5d688d01cb0b683a91342e` | 0 |
| src/xrp/field_sort.c | 1932 | `4909485c67b8185f334417c18951c7716879ededa14183129d59aa6c0a6c3b9a` | 0 |
| src/xrp/field_sort.h | 947 | `48325fb4c56f0f2d893f4fda6c1cfa90547d04c0513a04810ac50e92b0354c87` | 0 |
| src/xrp/fields.c | 9543 | `e3d49dc82dcff55afc45c4232442ffa6bb1b72bfdfb30d262d618010436b8a74` | 0 |
| src/xrp/fields.h | 8157 | `3755cda8a10f2b9101c541ded6c73a2af01e8200aa4ee250c6b20345d453c1eb` | 0 |
| src/xrp/flags.c | 16559 | `4bbb78921e29fd2d13387c7a11e9067dba0d2dbe3a9c58b38b8ea47032ab4162` | 0 |
| src/xrp/flags.h | 1218 | `90c439e572e7fad08ef1df3a649ac45a92397862a361399c4d555dd41e4df66c` | 0 |
| src/xrp/fmt.c | 2421 | `2d54aee7630ceca45b4f4d43deed69aedb01f7d0d8b98c35ae2c4097e26bc565` | 0 |
| src/xrp/fmt.h | 90 | `2bd09cd700a846019debd7f6777c0dd27a7c1015c9915ca16ecbce59c729ebb3` | 0 |
| src/xrp/general.c | 8162 | `067e5fb0c0159665282e81998ac8fcc0f6feb3d278ee2993147cc059be2b5a0f` | 0 |
| src/xrp/general.h | 1454 | `7a707749af9b4ed6c8d5b576a0ea7dc27ef449d13598f30a7bd44cad51ae48c0` | 0 |
| src/xrp/number_helpers.c | 925 | `5a439c3b1426c2b66663a945a3f473ff5d4ade33c0e1552083bf9142968be4c7` | 0 |
| src/xrp/number_helpers.h | 848 | `e68166af8e6bd1d736f11b4e198f8f92a6c21052235ab4187a0ec44036de70a5` | 0 |
| src/xrp/percentage.c | 3115 | `9c8f45f161bb43675db8b98f0887e3adf33ca9843fd924b595d4cb7f1b23f0b3` | 0 |
| src/xrp/percentage.h | 1023 | `96d835d105573a50efc0ad93086caf4b79a0464eb8c43bf286ec3b9454d650b5` | 0 |
| src/xrp/readers.c | 1430 | `633c2e3d87c498978557222338abf23a8c31d78415389cfd644ab7213fc1f32c` | 0 |
| src/xrp/readers.h | 990 | `da91db49867ec38abf7d152cc193fd4b3a1730606a5df624dac2183faa57b34e` | 0 |
| src/xrp/time.c | 4356 | `262c9b0f15c0bc722b5cfcb480579beb60ccb4c78858e4f119693549c4486e07` | 0 |
| src/xrp/time.h | 1089 | `78750c1cd52c1b2f49122b1a73aaeb80fd06087de3b23f206924792fbbfba176` | 0 |
| src/xrp/transaction_types.h | 2616 | `f918fb14fa915064b69d5f1fdcdd5c9aa96450f54e5f4383e55cb038a2102033` | 0 |
| src/xrp/xrp_helpers.c | 9106 | `033ee7cc78dada40f0b133de8eaa5e9dd627675807468ffe3ecb0ade8b1b6dc6` | 0 |
| src/xrp/xrp_helpers.h | 1898 | `24c0fb770bfc2fe3e75c010ccb836f1094a13b5f763d0abf4cd4eaece1aa1ed0` | 0 |
| src/xrp/xrp_parse.c | 23969 | `c78835d4ac4268988eab15b64af1dbcd7f628bbbbf20e88698ac90245407b887` | 0 |
| src/xrp/xrp_parse.h | 1428 | `2e13e37ea18ade2f2cadda54fb31072f9f90a4e720dffc3c6ae59d4af9320de5` | 0 |
| src/xrp/xrp_pub_key.c | 1115 | `318eb2967a6a895fd2890c851f5e91dbf6224218e567d0ea3ad298559b9bc9bf` | 0 |
| src/xrp/xrp_pub_key.h | 288 | `6ee5b72f81c8ee9b3954105b2a2b560ea94b9a7e6e3400f33fa5c1b37268bc12` | 0 |
