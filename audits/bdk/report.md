# Security & Post-Quantum Readiness Audit Report

**Project:** bdk @ f2528da88b10 · Bitcoin Dev Kit — public repository (passive review)
| | |
|---|---|
| Organization | QSI |
| Report date | 2026-10-28 19:24 UTC |
| Report version | 1 |
| Audit run | 2b50b8d0-5f83-4b6a-8343-16d2e8f4851e (Document audit) |
| Analyzer engine | qsi-engine 1.2.0 |
| Risk profile | Crypto exchange, custodian or wallet |
| Content SHA-256 | `17cf808163d3356c7d53bcdb7c9e634e4a9e6400eb6e18601bfc81fadd83aba5` |
| Signature key (Ed25519, SHA-256 fingerprint; the signature is the separate file report.sig.json) | `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e` |
> This report presents automated and documented analysis results for the stated scope. It is not a legal opinion, a certification or an attestation of compliance with any standard.

## 1. Executive summary

- Critical: **0**
- High: **0**
- Medium: **1**
- Low: **0**
- Info: **0**

- Confirmed technical vulnerability: 0
- Known vulnerable component: 0
- Confirmed configuration error: 0
- Potential cryptographic risk: 0
- Long-term post-quantum risk: 1
- Improvement recommendation: 0
- Insufficient data: 0

Mosca's inequality (x + y > z): x = 10, y = 5, z = 8 → migration would finish too late under this scenario. _z is a planning assumption chosen per risk profile, not a prediction. A cryptographically relevant quantum computer is not publicly known to exist today._

**Post-quantum maturity: Level 0 of 4 — no post-quantum cryptography.** Next step: Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

## 2. Scope and boundaries

Mode: Document audit

Repository: <https://github.com/bitcoindevkit/bdk> @ `f2528da88b1041bdddf547d677511aea19ad3573` — evidence links open the lines at this commit.

45 files, 592207 bytes in total, 0 redaction(s); the per-file SHA-256 list is in appendix C.

## 3. Methodology

| Area | Status | Count | Examples |
|---|---|---|---|
| dependencies | checked | 7 | crates/bitcoind_rpc/Cargo.toml: 4 dependencies parsed (0 pinned); crates/chain/Cargo.toml: 9 dependencies parsed (0 pinned); crates/core/Cargo.toml: 5 dependencies parsed (0 pinned) |
| source_code | checked | 38 | crates/bitcoind_rpc/src/bip158.rs: 197 lines scanned with 16 rule patterns and 122 registry patterns; crates/bitcoind_rpc/src/lib.rs: 627 lines scanned with 16 rule patterns and 122 registry patterns; 137 lines in #[cfg(test)] modules ignored; crates/chain/src/balance.rs: 105 lines scanned with 16 rule patterns and 122 registry patterns; 38 lines in #[cfg(test)] modules ignored |
| osv_advisories | not checked | 1 | no exactly pinned versions to query |

_Long lists are grouped here; the full per-file list is in the JSON report, signed with the same key._

## 4. Assets examined and not examined

- osv_advisories — not checked: no exactly pinned versions to query

## 5. Architecture overview

Static review of the source tree bdk at f2528da88b1041bdddf547d677511aea19ad3573. 45 files analysed; of 89 files, 30 are test, fuzzing, benchmark or example code and were left out, 14 are not read by any analyzer, 0 exceed the per-file limit and 0 did not fit the total limit. No requests were sent to the owner's systems.

## 6. Overall security posture

- Indicative posture index: **100** / 100 — _Derived from findings in scope (confirmed and potential issues weighted by severity). Indicative only; not comparable across differently scoped audits._
- Quantum-vulnerable share of inventory: 100.0%

## 7. Detailed findings

### QSI-2026-06106 — Quantum-vulnerable ECDSA: transaction and message signing (1 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:ECDSA:transaction_signing`
- Data source: crates/chain/src/spk_iter.rs
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.2.0 · 2026-10-28 19:24 UTC
- Priority score: 35.6 / 100
- CVSS v3.1: not applicable

2 reference(s) to ECDSA across 1 file(s), e.g. crates/chain/src/spk_iter.rs:2. Role, judged from paths, function names and nearby code: transaction and message signing. A CRQC derives the private key from a public key that is already known (on chain after the first spend, in reused addresses): funds and approvals controlled by these keys need a migration path.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open crates/chain/src/spk_iter.rs:2 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [crates/chain/src/spk_iter.rs](https://github.com/bitcoindevkit/bdk/blob/f2528da88b1041bdddf547d677511aea19ad3573/crates/chain/src/spk_iter.rs#L2) · line 2 · SHA-256 58953e8cd27684683f75e8c61ebc1f8b6d9c286a2f5983b56e89a0ae255886b5_

```
    1 | use crate::{
    2 |     bitcoin::{secp256k1::Secp256k1, ScriptBuf},
    3 |     miniscript::{Descriptor, DescriptorPublicKey},
```

_file_excerpt · [crates/chain/src/spk_iter.rs](https://github.com/bitcoindevkit/bdk/blob/f2528da88b1041bdddf547d677511aea19ad3573/crates/chain/src/spk_iter.rs#L40) · line 40 · SHA-256 2100b069271cc49191876e6a859414230e335185aeb5ec18d55ed509e55d5e14_

```
   39 |     descriptor: D,
   40 |     secp: Secp256k1<bitcoin::secp256k1::VerifyOnly>,
   41 | }
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains adopt them.

**Retest procedure.** Re-run the inventory after refactoring.


## 8. Post-quantum assessment

| | Key establishment (x = how long data must stay confidential; harvest now, decrypt later) | Signatures (x = how long signatures/keys must stay trusted) |
|---|---|---|
| Data/key lifetime x | 10 | 10 |
| Migration time y | 5 | 5 |
| Assumed years to CRQC z | 8 (early) | 8 |
| x + y − z | 7 → migration would finish too late under this scenario | 7 → migration would finish too late under this scenario |
#### Where z comes from

Averaged expert likelihood that a CRQC exists within each horizon, from the annual survey published by the author of this inequality. Likelihood estimates, not predictions of a date.

| Within | Likelihood | The report's wording |
|---|---|---|
| 5 years | ~15% | averaged estimate |
| 10 years | 28-49% | quite possible |
| 15 years | 51-70% | likely |

**Why this scenario (early, z = 8):** Inside the 10-year horizon the survey puts at 28-49% ('quite possible'), and consistent with the BSI estimate of 15 years that 'could shrink to 10 or even less'. Use it for data that must stay confidential for decades, where being wrong is expensive.
_Planning assumptions: x for key establishment, x for signatures, y are the defaults of the risk profile “Crypto exchange, custodian or wallet”, not the client's figures; with the client's actual lifetimes the verdict can change._

### Post-quantum maturity: Level 0 of 4 — no post-quantum cryptography


**Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

_Levels: 0 none; 1 present, not wired; 2 in use outside the critical paths; 3 hybrid in a critical path; 4 post-quantum by default in the critical paths (root of trust, key wrapping, channel key exchange). Judged from code and manifests._

### What the quantum-vulnerable algorithms do

| Role | Algorithms (files) | ID | First step |
|---|---|---|---|
| **transaction and message signing** | ECDSA (1) | QSI-2026-06106 | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains adopt them |

_Roles are judged from file paths, function names and the code around each match; review confirms them. Root-of-trust keys and wrapped keys come first: they are hard to replace or can be recorded today._
No readiness questionnaire was completed for this project.

### Quantum algorithms relevant to this inventory

| Quantum algorithm | Effect | Attack model | Inventoried algorithms (rows) | What it means for this audit |
|---|---|---|---|---|
| Shor's algorithm — elliptic-curve discrete logarithms | breaks | Q1 | ECDSA (1) | Elliptic-curve keys are expected to fall before RSA keys of comparable classical strength. On blockchains, coins whose public key is already on chain (reused addresses, pay-to-public-key and Taproot outputs) are exposed first; plan the move to post-quantum signatures and avoid key reuse in the meantime. |

_Effects: breaks — replace the algorithm; weakens — larger keys or outputs restore the margin; included in standard parameters — no action at standard parameter sets; only with superposition queries — not applicable to ordinary deployments._


## 9. Limitations and assumptions

- This report presents automated and documented analysis results for the stated scope. It is not a legal opinion, a certification or an attestation of compliance with any standard.
- z is a planning assumption chosen per risk profile, not a prediction. A cryptographically relevant quantum computer is not publicly known to exist today.
- osv_advisories: no exactly pinned versions to query

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
| P3 | QSI-2026-06106 | Add ECDSA usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P4 | QSI-2026-06106 | Plan migration of ECDSA to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |

## 11. Tools used

- blockchain 1.0.0
- certificates 1.1.0
- chain_map 1.0.0
- configs 1.1.0
- dependencies 1.2.0
- inventory_document 1.1.0
- solidity 1.2.0
- source_code 1.3.0
- tls_code 1.1.0
- tls_live 1.0.0
- qsi-engine 1.2.0
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
11. NIST IR 8547 — Transition to Post-Quantum Cryptography Standards — NIST. <https://csrc.nist.gov/pubs/ir/8547/ipd> (initial public draft (November 2024); proposes deprecating quantum-vulnerable public-key algorithms after 2030 and disallowing them after 2035 — dates may change in the final version)
12. P. W. Shor — Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms on a Quantum Computer (SIAM J. Comput., 1997) — SIAM. <https://doi.org/10.1137/S0097539795293172> (peer-reviewed article)
13. R. Babbush et al. — Securing Elliptic Curve Cryptocurrencies against Quantum Vulnerabilities: Resource Estimates and Mitigations (arXiv:2603.28846) — arXiv. <https://arxiv.org/abs/2603.28846> (preprint (2026-03-30, v2 2026-04-15): 256-bit ECDLP with < 1200 logical qubits and < 90 M Toffoli gates (or < 1450 and < 70 M); < 500,000 physical qubits at 10^-3 error, minutes)

## Appendices: Cryptographic inventory

| Algorithm | Parameter | Library | Location | Quantum status | Classical status |
|---|---|---|---|---|---|
| ECDSA | secp256k1 |  | crates/chain/src/spk_iter.rs:2 | vulnerable (Shor) | acceptable |

## Appendices: Input files

| File | Size | SHA-256 | Redactions |
|---|---|---|---|
| crates/bitcoind_rpc/Cargo.toml | 1205 | `83b91c7a3e4ca359834c618240fa8f3a0a5e758f6732d666046c41a11bf49d1e` | 0 |
| crates/bitcoind_rpc/src/bip158.rs | 6761 | `b34cdc094a2395ce3336c503df9bcc0ee29f344f741ab25a3392d80020c1f06e` | 0 |
| crates/bitcoind_rpc/src/lib.rs | 24629 | `baf69cb786789de4b5f1b9357cd496200656552d93bf3ae8958180b289c7d41e` | 0 |
| crates/chain/Cargo.toml | 1488 | `0a170fa2a682fa7b5dd32a1a18d3c923136b75e44bf0bbc6497a6a565d8b38b3` | 0 |
| crates/chain/src/balance.rs | 3239 | `c4722689b26a97489acec069808665f2d99f21756d149dd98526a622fb596188` | 0 |
| crates/chain/src/canonical.rs | 28704 | `6d3081611bb7099213687c0ec0225ace91dd7662cdd20161b30cd37d16c34022` | 0 |
| crates/chain/src/canonical_task.rs | 19546 | `a774ade1336130608faff6ce1ecca7b07b9665c1a4c00eeb6a29fa0691d525ef` | 0 |
| crates/chain/src/canonical_view_task.rs | 8775 | `f60cac7e957c47be21c1e66c8a75230b8f1bea954d6784716a24ca05c9afcb32` | 0 |
| crates/chain/src/chain_data.rs | 13411 | `770bdca6ee7e8706a14a4ab08f93fb094d2c7ba5149452d23f75d71f3adf64c7` | 0 |
| crates/chain/src/descriptor_ext.rs | 1395 | `c046997e44f8ebdf762a39d259763091cd70ec1897e22cc7e6ac253705bdf837` | 0 |
| crates/chain/src/example_utils.rs | 2544 | `8f76a44443ebc40cceff4833b82898a1eda21784774582649e4a3edd2d80c710` | 0 |
| crates/chain/src/indexed_tx_graph.rs | 20256 | `9d90f8c1ce2109d50a351f4c8c9f7e360bde210957cfc95f825ffedc509226ad` | 0 |
| crates/chain/src/indexer/keychain_txout.rs | 55225 | `13f5011338a01c5776262b07538efd04338f13c9ad33349a06c925b5d38a8539` | 0 |
| crates/chain/src/indexer/spk_txout.rs | 19747 | `3f60ae8ee0ec261ba9a93407ef2d9e232787526bf4fad22daf6877e9ca1f1820` | 0 |
| crates/chain/src/indexer.rs | 2332 | `2745f08c61b5c64bad7768ae5a5f5cd94bbf608120f62df8ff0fead96b227653` | 0 |
| crates/chain/src/lib.rs | 2931 | `90a0f842b2b47069220959344f84c0aa4c8ecfc1344bff8572dd2e307e176d9e` | 0 |
| crates/chain/src/local_chain.rs | 35484 | `81ff161a87ed2621837edac91ef5f4b44e01d8ad2cdb2fcd2a7e71c64b69fc1f` | 0 |
| crates/chain/src/rusqlite_impl.rs | 31001 | `f0d1ee07c37b7463e0d6d51509518fb765da6a043a0f80ef5253d8dd7e39a8da` | 0 |
| crates/chain/src/spk_iter.rs | 11496 | `5df96d8c7921b3306d986d117a4348e9afe98be7c27c94b1ef8fe1ab13c2f7b9` | 0 |
| crates/chain/src/tx_data_traits.rs | 3937 | `3955c21e9df3f266e015156de68802b855c4eff8b4248dcb2beba6ccf3ca9748` | 0 |
| crates/chain/src/tx_graph.rs | 54561 | `6e99486950e6e752f1451b68fef0df8f2b365c4c816c33aac9b263e6a75bf317` | 0 |
| crates/core/Cargo.toml | 967 | `b7d7c5845ff0fe6681193d2de326a75c076e01201a1a7ee345dda16980f1cb28` | 0 |
| crates/core/src/block_id.rs | 1431 | `9b95ef3640317298b5a38d6fa7b89fdac18edc53aac55292b7a85f0f4f850619` | 0 |
| crates/core/src/chain_query.rs | 1659 | `369fb027368651a610f09a66bce4adaf2fc7774eeff122ab6a368a3b0471ac6b` | 0 |
| crates/core/src/checkpoint.rs | 26783 | `fbb0c2a3f0d13941adc50f6d8ba9f84cd703d1505f51a098dd4fa011acc01f4f` | 0 |
| crates/core/src/checkpoint_entry.rs | 5428 | `6864fd17b358f33675409d53e65ff00d83cd929d507c600bf1dbfb1f80c7cb76` | 0 |
| crates/core/src/lib.rs | 2986 | `70bd648e7f01758a128bd04cce0251d5194bd1e84b9ae4a9ac90a0e6d9f5e327` | 0 |
| crates/core/src/merge.rs | 2522 | `a7d01b0607e0b525e9841d59a2d011bd2e8d2edb807a888634db7400922b5c49` | 0 |
| crates/core/src/spk_client.rs | 26500 | `b36f7eac9ea9faef7ca22e2604d857d218ed1b1aa47a2657edb659e5a501b91d` | 0 |
| crates/core/src/tx_update.rs | 4343 | `4fa8a8f174889198258acc3293f726142d6c1882c41468be839c4db8077e2af7` | 0 |
| crates/electrum/Cargo.toml | 984 | `71d66c3d4f5fad2b279c8ce0d48ada975679f93668f9425670e14d1fe19b0200` | 0 |
| crates/electrum/src/bdk_electrum_client.rs | 36790 | `e390a2b8437c83a9d14daeb3f923b19797efea2fb50e6a11fb8f79f58b12f53b` | 0 |
| crates/electrum/src/lib.rs | 1100 | `bbbeb08934d653c218be80344abe9f46b62085154b47ca29fe0b704f1370d3c0` | 0 |
| crates/esplora/Cargo.toml | 1748 | `1daccf1d0415e843e617673ccedabfb49813555855b01c80f8cf9b3853a2acda` | 0 |
| crates/esplora/src/async_ext.rs | 28886 | `c2fb578219b5fc719a943f6529f68b25857c9191c866752f283b005c31698aed` | 0 |
| crates/esplora/src/blocking_ext.rs | 35556 | `dd5711d633b794f71c5b5ce84767028799dd1f8d9f61cc01d1b995a0f15a27e0` | 0 |
| crates/esplora/src/lib.rs | 2777 | `69cd2fb696e1b267c0891e57eadac8ada2f1a27fe96305e6889930569f9580ff` | 0 |
| crates/file_store/Cargo.toml | 761 | `afcf61e36799750107cce36d0333badc52cbaaf3803d7eca9ec35e164de765d4` | 0 |
| crates/file_store/src/entry_iter.rs | 2635 | `00cb247c7ca63d3ae44317c2abbaffdd5b36a49bfbbf99ff5fca9c79234a299b` | 0 |
| crates/file_store/src/lib.rs | 1714 | `1010d865adab4b312801b24b93f4f851d6da991ba31e449907aba70aad735550` | 0 |
| crates/file_store/src/store.rs | 23655 | `9390058ea9f9ab92fe1ca6732e3dbf06fd99822533b48b5a91d5a98ae46fcfce` | 0 |
| crates/testenv/Cargo.toml | 1067 | `1595b83bbd626078abc111bd7ac9233df0406f944473aa8d0e1a956de0dc4845` | 0 |
| crates/testenv/src/lib.rs | 21293 | `16bd1975ff6ead0e1f8bb86c65f33bec630835b2f21f48ff6c61e4dde0ea97aa` | 0 |
| crates/testenv/src/persist_test_utils.rs | 6370 | `fcfef6b7701ba51df6048b7ddd9ace6402ff9fe29cd7b8e0eacf16b77d8e554f` | 0 |
| crates/testenv/src/utils.rs | 5585 | `50b9ebfe246c3d0be4e277d2acd16773aabe06d1bfff2ee1e87f38efe851b894` | 0 |
