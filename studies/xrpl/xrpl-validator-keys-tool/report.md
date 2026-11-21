# Security & Post-Quantum Readiness Audit Report

**Project:** xrpl-validator-keys-tool @ 4c0fb75eec96 · Ripple — public repository (passive review)
| | |
|---|---|
| Organization | QSI |
| Report date | 2026-11-21 10:24 UTC |
| Report version | 1 |
| Audit run | a9bad12b-a5d9-4c48-87f2-b83026b08b85 (Document audit) |
| Analyzer engine | qsi-engine 1.8.1 |
| Risk profile | Web3 project |
| Content SHA-256 | `b85785e63f890a58ff95dd6422534423caf8411033ded5511e5803a9181a099c` |
| Signature key (Ed25519 SHA-256 fingerprint, then the ML-DSA-65 one where it co-signs; the signature is the separate file report.sig.json) | `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e · ML-DSA-65 dbd4e297b3213d1d7577a565e76de14cc5ad0e409f1dc68291c67266fc95066a` |
> This report presents automated and documented analysis results for the stated scope. It is not a legal opinion, a certification or an attestation of compliance with any standard.

## 1. Executive summary

- Critical: **0**
- High: **0**
- Medium: **2**
- Low: **0**
- Info: **0**

- Confirmed technical vulnerability: 0
- Known vulnerable component: 0
- Confirmed configuration error: 0
- Potential cryptographic risk: 0
- Long-term post-quantum risk: 2
- Improvement recommendation: 0
- Insufficient data: 0

Mosca's inequality (x + y > z): x = 5, y = 5, z = 12 → tight margin. _z is a planning assumption chosen per risk profile, not a prediction. A cryptographically relevant quantum computer is not publicly known to exist today._

**Post-quantum maturity: Level 0 of 4 — no post-quantum cryptography.** Next step: Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

## 2. Scope and boundaries

Mode: Document audit

Repository: <https://github.com/ripple/validator-keys-tool> @ `4c0fb75eec9601c711645998c904507e87e910ae` — evidence links open the lines at this commit.

| File | Size | SHA-256 | Redactions |
|---|---|---|---|
| src/ValidatorKeys.cpp | 8755 | `a2a51292625a283541d247f1435005851b59ce6836f209b07d9c1440a6350f1f` | 0 |
| src/ValidatorKeys.h | 3553 | `b8e33d80d5dddff750403e1d67fe2d574118e1cce4ab873b15ecea825e4122d1` | 0 |
| src/ValidatorKeysTool.cpp | 13448 | `94c1bfc7b5ca715e1a6c0cc14dc5b0f9319dadb3b5a963ad4b37289e311e779f` | 0 |
| src/ValidatorKeysTool.h | 567 | `c8314e8fa8b8bbcffee8b678b60cfc7625b63c1ce84dec93aec73b57cbd43997` | 0 |

## 3. Methodology

| Area | Status | Detail |
|---|---|---|
| source_code | checked | src/ValidatorKeys.cpp: 294 lines scanned with 16 rule patterns and 313 registry patterns |
| source_code | checked | src/ValidatorKeys.h: 162 lines scanned with 16 rule patterns and 313 registry patterns |
| source_code | checked | src/ValidatorKeysTool.cpp: 471 lines scanned with 16 rule patterns and 313 registry patterns |
| source_code | checked | src/ValidatorKeysTool.h: 30 lines scanned with 16 rule patterns and 313 registry patterns |
| entropy | checked | random-number generation: 4 code files read with 0 macro definitions from the tree; 0 ineffective guard(s), 0 weak random-bytes provider(s), 0 weak key-generation site(s) |

## 4. Assets examined and not examined

- None

## 5. Architecture overview

Static review of the source tree xrpl-validator-keys-tool at 4c0fb75eec9601c711645998c904507e87e910ae. 4 files analysed; of 20 files, 3 are test, fuzzing, benchmark or example code and were left out, 13 are not read by any analyzer, 0 exceed the per-file limit and 0 did not fit the total limit. Files no analyzer reads include: .clang-format, .git-blame-ignore-revs, .github/workflows/clang-format.yml, .gitignore, CMakeLists.txt. 30 files in build-output or dependency-cache directories (.git, .hg, .venv, __pycache__, build, dist, node_modules, target, vendor, venv) were not read. No requests were sent to the owner's systems.

## 6. Overall security posture

- Indicative posture index: **100** / 100 — _Derived from findings in scope (confirmed and potential issues weighted by severity). Indicative only; not comparable across differently scoped audits._
- Quantum-vulnerable share of inventory: 100.0%

## 7. Detailed findings

### QSI-2026-34934 — Quantum-vulnerable ECDSA: role not determined (1 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:ECDSA:general`
- Data source: src/ValidatorKeys.h
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.8.1 · 2026-11-21 10:24 UTC
- Priority score: 31.7 / 100
- CVSS v3.1: not applicable

1 reference(s) to ECDSA across 1 file(s), e.g. src/ValidatorKeys.h:104. Role, judged from paths, function names and nearby code: role not determined. The code does not show what the keys protect; review decides the priority.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open src/ValidatorKeys.h:104 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [src/ValidatorKeys.h](https://github.com/ripple/validator-keys-tool/blob/4c0fb75eec9601c711645998c904507e87e910ae/src/ValidatorKeys.h#L104) · line 104 · SHA-256 ab49ca1c1a19a77ad484a2f6f8163e3ec955f2808563d6eb9730ce952409ce0a_

```
  103 |     boost::optional<ValidatorToken>
  104 |     createValidatorToken(KeyType const& keyType = KeyType::Secp256k1);
  105 | 
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it; introduce an abstraction layer for crypto-agility.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-34935 — Quantum-vulnerable Ed25519: role not determined (1 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:Ed25519:general`
- Data source: src/ValidatorKeysTool.cpp
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.8.1 · 2026-11-21 10:24 UTC
- Priority score: 31.7 / 100
- CVSS v3.1: not applicable

1 reference(s) to Ed25519 across 1 file(s), e.g. src/ValidatorKeysTool.cpp:64. Role, judged from paths, function names and nearby code: role not determined. The code does not show what the keys protect; review decides the priority.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open src/ValidatorKeysTool.cpp:64 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [src/ValidatorKeysTool.cpp](https://github.com/ripple/validator-keys-tool/blob/4c0fb75eec9601c711645998c904507e87e910ae/src/ValidatorKeysTool.cpp#L64) · line 64 · SHA-256 4ccde58448819ac88692327683451e95a08012e9a680e95a3b808e111d60afad_

```
   63 | 
   64 |     ValidatorKeys const keys(KeyType::Ed25519);
   65 |     keys.writeToFile(keyFile);
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
| **role not determined** | ECDSA (1), Ed25519 (1) | QSI-2026-34934, QSI-2026-34935 | Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it; introduce an abstraction layer for crypto-agility |

_Roles are judged from file paths, function names and the code around each match; review confirms them. Root-of-trust keys and wrapped keys come first: they are hard to replace or can be recorded today._
No readiness questionnaire was completed for this project.

### Quantum algorithms relevant to this inventory

| Quantum algorithm | Effect | Attack model | Inventoried algorithms (rows) | What it means for this audit |
|---|---|---|---|---|
| Shor's algorithm — elliptic-curve discrete logarithms | breaks | Q1 | ECDSA (1), Ed25519 (1) | Elliptic-curve keys are expected to fall before RSA keys of comparable classical strength. On blockchains, coins whose public key is already on chain (reused addresses, pay-to-public-key and Taproot outputs) are exposed first; plan the move to post-quantum signatures and avoid key reuse in the meantime. |

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
| P3 | QSI-2026-34934 | Add ECDSA usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-34935 | Add Ed25519 usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P4 | QSI-2026-34934 | Plan migration of ECDSA to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-34935 | Plan migration of Ed25519 to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |

## 11. Tools used

- blockchain 1.0.0
- certificates 1.2.0
- chain_map 1.0.0
- configs 1.1.0
- crediting 1.1.0
- dependencies 1.4.3
- hndl 1.0.0
- inventory_document 1.1.0
- mpc 1.0.0
- solidity 1.5.2
- source_code 1.7.1
- tls_code 1.1.0
- tls_live 1.0.0
- ton_contracts 1.0.0
- validator_keys 1.2.0
- wallet_login 1.0.0
- qsi-engine 1.8.1
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

By origin: own code 2 (2 Shor-breakable).

| Algorithm | Parameter | Library | Location | Quantum status | Classical status |
|---|---|---|---|---|---|
| ECDSA | secp256k1 |  | src/ValidatorKeys.h:104 | vulnerable (Shor) | acceptable |
| Ed25519 | Ed25519 |  | src/ValidatorKeysTool.cpp:64 | vulnerable (Shor) | acceptable |
