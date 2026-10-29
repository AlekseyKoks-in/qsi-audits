# Security & Post-Quantum Readiness Audit Report

**Project:** monero @ 3fd0f88c20f5 · Monero — public repository (passive review)
| | |
|---|---|
| Organization | QSI |
| Report date | 2026-10-28 16:45 UTC |
| Report version | 1 |
| Audit run | 21c01b41-ab43-493f-81ae-7028dfa36d92 (Document audit) |
| Analyzer engine | qsi-engine 1.2.0 |
| Risk profile | Crypto exchange, custodian or wallet |
| Content SHA-256 | `c640f43c1f7c8aeef4a0c7208351c7fb5f0d46ab7c3a0401b7c2139ece61dd32` |
| Signature key (Ed25519, SHA-256 fingerprint; the signature is the separate file report.sig.json) | `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e` |
> This report presents automated and documented analysis results for the stated scope. It is not a legal opinion, a certification or an attestation of compliance with any standard.

## 1. Executive summary

- Critical: **0**
- High: **0**
- Medium: **5**
- Low: **2**
- Info: **1**

- Confirmed technical vulnerability: 0
- Known vulnerable component: 3
- Confirmed configuration error: 0
- Potential cryptographic risk: 0
- Long-term post-quantum risk: 4
- Improvement recommendation: 0
- Insufficient data: 1

Mosca's inequality (x + y > z): x = 10, y = 5, z = 8 → migration would finish too late under this scenario. _z is a planning assumption chosen per risk profile, not a prediction. A cryptographically relevant quantum computer is not publicly known to exist today._

**Post-quantum maturity: Level 0 of 4 — no post-quantum cryptography.** Next step: Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

## 2. Scope and boundaries

Mode: Document audit

Repository: <https://github.com/monero-project/monero> @ `3fd0f88c20f559839cafb20911cb13cb45eba7bd` — evidence links open the lines at this commit.

580 files, 7979041 bytes in total, 0 redaction(s); the per-file SHA-256 list is in appendix C.

## 3. Methodology

| Area | Status | Count | Examples |
|---|---|---|---|
| source_code | checked | 572 | src/blockchain_db/blockchain_db.cpp: 507 lines scanned with 16 rule patterns and 122 registry patterns; src/blockchain_db/blockchain_db.h: 1920 lines scanned with 16 rule patterns and 122 registry patterns; src/blockchain_db/lmdb/db_lmdb.cpp: 5817 lines scanned with 16 rule patterns and 122 registry patterns |
| certificates | error (not checked) | 1 | src/common/dns_utils.cpp line 79: certificate could not be parsed (ValueError) |
| certificates_and_keys | checked | 1 | src/common/dns_utils.cpp: certificates/keys parsed |
| chain_map | checked | 1 | src/device_trezor/trezor/protob/messages-monero.proto: Monero |
| dependencies | checked | 2 | src/fcmp_pp/fcmp_pp_rust/Cargo.lock: 79 dependencies parsed (79 pinned); src/fcmp_pp/fcmp_pp_rust/Cargo.toml: 7 dependencies parsed (0 pinned) |
| tls_key_exchange_groups | Insufficient data | 1 | src/ringct/multiexp.cc line 555: not in the algorithm registry, not assessed: (groups |
| tls_configuration | checked | 1 | src/ringct/multiexp.cc: openssl TLS directives parsed |
| osv_advisories | checked | 1 | 79 pinned packages queried at OSV.dev; 3 affected |

_Long lists are grouped here; the full per-file list is in the JSON report, signed with the same key._

## 4. Assets examined and not examined

- certificates — error (not checked): src/common/dns_utils.cpp line 79: certificate could not be parsed (ValueError)
- tls_key_exchange_groups — Insufficient data: src/ringct/multiexp.cc line 555: not in the algorithm registry, not assessed: (groups

## 5. Architecture overview

Static review of the source tree monero at 3fd0f88c20f559839cafb20911cb13cb45eba7bd. 580 files analysed; of 663 files, 1 are test, fuzzing, benchmark or example code and were left out, 82 are not read by any analyzer, 0 exceed the per-file limit and 0 did not fit the total limit. No requests were sent to the owner's systems.

## 6. Overall security posture

- Indicative posture index: **93** / 100 — _Derived from findings in scope (confirmed and potential issues weighted by severity). Indicative only; not comparable across differently scoped audits._
- Quantum-vulnerable share of inventory: 41.2%

## 7. Detailed findings

### QSI-2026-05417 — Transaction signing for 1 chain(s) relies on elliptic-curve signatures

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: High
- Affected asset: `chain-map`
- Data source: src/device_trezor/trezor/protob/messages-monero.proto
- Detection method: Message definitions (.proto) matched to QSI's table of chain signature schemes.
- Analyzer: chain_map 1.2.0 · 2026-10-28 16:45 UTC
- Priority score: 56.8 / 100
- CVSS v3.1: not applicable

The wallet's message definitions cover Monero. These chains authorize transactions with Ed25519, which Shor's algorithm breaks on a cryptographically relevant quantum computer. A wallet cannot move a chain to post-quantum signatures on its own: the chain has to adopt a scheme first.

**Potential impact.** Once a CRQC exists, an attacker who sees an account's public key could derive the private key and move funds; how soon keys are exposed depends on each chain (address reuse, account model).

**Reproduction steps.**

```
Open the .proto files named in the evidence.
```

**Evidence.**

_file_excerpt · [src/device_trezor/trezor/protob/messages-monero.proto](https://github.com/monero-project/monero/blob/3fd0f88c20f559839cafb20911cb13cb45eba7bd/src/device_trezor/trezor/protob/messages-monero.proto#L2) · line 2 · SHA-256 2a60fdbae9c4da472daabb0e85b95bb7592b561df57b5344c02f5d168a37c8d9_

```
package hw.trezor.messages.monero;
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Chains are recognized from the names of the message definitions (.proto files and packages); the schemes are the chains' documented account signatures, not an analysis of the wallet's signing code.

**Recommendation.** Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains adopt them. Keep the signing layer crypto-agile per chain (algorithm identifiers in messages and storage, room for larger keys and signatures) and track each chain's post-quantum proposals, so that a new scheme can be added when a chain activates it.

**Retest procedure.** Re-run when a chain activates a post-quantum signature scheme or the wallet adds one.

### QSI-2026-05414 — Quantum-vulnerable Ed25519: role not determined (4 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:Ed25519:general`
- Data source: src/crypto/crypto_ops_builder/crypto_sign.h
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.2.0 · 2026-10-28 16:45 UTC
- Priority score: 34.2 / 100
- CVSS v3.1: not applicable

4 reference(s) to Ed25519 across 4 file(s), e.g. src/crypto/crypto_ops_builder/crypto_sign.h:10. Role, judged from paths, function names and nearby code: role not determined. The code does not show what the keys protect; review decides the priority.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open src/crypto/crypto_ops_builder/crypto_sign.h:10 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [src/crypto/crypto_ops_builder/crypto_sign.h](https://github.com/monero-project/monero/blob/3fd0f88c20f559839cafb20911cb13cb45eba7bd/src/crypto/crypto_ops_builder/crypto_sign.h#L10) · line 10 · SHA-256 1633a67376543975d71960dfc141c8df6517fb680e0f0bafa39f3e8693ce6069_

```
    9 | extern int crypto_sign_open(unsigned char *,unsigned long long *,const unsigned char *,unsigned long long,const unsigned char *);
   10 | extern int crypto_sign_keypair(unsigned char *,unsigned char *);
   11 | extern int crypto_sign_publickey(unsigned char *pk, unsigned char *sk, unsigned char *seed);
```

_file_excerpt · [src/crypto/crypto_ops_builder/include/sodium.h](https://github.com/monero-project/monero/blob/3fd0f88c20f559839cafb20911cb13cb45eba7bd/src/crypto/crypto_ops_builder/include/sodium.h#L32) · line 32 · SHA-256 e44ffcfd2c36c50a32623005fa4fc3a6955d56c815105774ac58780b1b801d0f_

```
   31 | #include "sodium/crypto_sign.h"
   32 | #include "sodium/crypto_sign_ed25519.h"
   33 | #include "sodium/crypto_stream.h"
```

_file_excerpt · [src/crypto/crypto_ops_builder/ref10/keypair.c](https://github.com/monero-project/monero/blob/3fd0f88c20f559839cafb20911cb13cb45eba7bd/src/crypto/crypto_ops_builder/ref10/keypair.c#L7) · line 7 · SHA-256 7463cfd8d788a4394462333e573eb707e802d719f8151ef9326694b265e43610_

```
    6 | 
    7 | int crypto_sign_keypair(unsigned char *pk,unsigned char *sk)
    8 | {
```

_file_excerpt · [src/crypto/crypto_ops_builder/ref10CommentedCombined/keypair.c](https://github.com/monero-project/monero/blob/3fd0f88c20f559839cafb20911cb13cb45eba7bd/src/crypto/crypto_ops_builder/ref10CommentedCombined/keypair.c#L7) · line 7 · SHA-256 7463cfd8d788a4394462333e573eb707e802d719f8151ef9326694b265e43610_

```
    6 | 
    7 | int crypto_sign_keypair(unsigned char *pk,unsigned char *sk)
    8 | {
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it; introduce an abstraction layer for crypto-agility.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-05415 — Quantum-vulnerable X25519: role not determined (2 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:X25519:general`
- Data source: src/crypto/crypto_ops_builder/include/sodium.h
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.2.0 · 2026-10-28 16:45 UTC
- Priority score: 34.2 / 100
- CVSS v3.1: not applicable

2 reference(s) to X25519 across 2 file(s), e.g. src/crypto/crypto_ops_builder/include/sodium.h:25. Role, judged from paths, function names and nearby code: role not determined. The code does not show what the keys protect; review decides the priority.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open src/crypto/crypto_ops_builder/include/sodium.h:25 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [src/crypto/crypto_ops_builder/include/sodium.h](https://github.com/monero-project/monero/blob/3fd0f88c20f559839cafb20911cb13cb45eba7bd/src/crypto/crypto_ops_builder/include/sodium.h#L25) · line 25 · SHA-256 e2d333bff28206bff3400c47b5c6881b1ec65e0ebd19b05659e42ceb45f51547_

```
   24 | #include "sodium/crypto_pwhash_scryptsalsa208sha256.h"
   25 | #include "sodium/crypto_scalarmult.h"
   26 | #include "sodium/crypto_scalarmult_curve25519.h"
```

_file_excerpt · [src/crypto/x25519.cpp](https://github.com/monero-project/monero/blob/3fd0f88c20f559839cafb20911cb13cb45eba7bd/src/crypto/x25519.cpp#L30) · line 30 · SHA-256 bce348264cf8220651dfc34ba2a085d131c4931555ecc9701059e13aff64c093_

```
   29 | //paired header
   30 | #include "x25519.h"
   31 | 
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Classify each usage, record data lifetimes, and plan migration to Hybrid key establishment with ML-KEM (FIPS 203), e.g. X25519MLKEM768 in TLS 1.3 or mlkem768x25519-sha256 in SSH; introduce an abstraction layer for crypto-agility.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-05416 — Quantum-vulnerable ECDH: role not determined (2 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:ECDH:general`
- Data source: src/device_trezor/trezor/protocol.cpp
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.2.0 · 2026-10-28 16:45 UTC
- Priority score: 34.2 / 100
- CVSS v3.1: not applicable

3 reference(s) to ECDH across 2 file(s), e.g. src/device_trezor/trezor/protocol.cpp:699. Role, judged from paths, function names and nearby code: role not determined. The code does not show what the keys protect; review decides the priority.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open src/device_trezor/trezor/protocol.cpp:699 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [src/device_trezor/trezor/protocol.cpp](https://github.com/monero-project/monero/blob/3fd0f88c20f559839cafb20911cb13cb45eba7bd/src/device_trezor/trezor/protocol.cpp#L699) · line 699 · SHA-256 7160937a79a3a95f9c7a63fe81b770c6ed8c34318e8970a8856144860de7c98b_

```
  698 |     } else {
  699 |       CHECK_AND_ASSERT_THROW_MES(8 == ack->ecdh_info().size(), "Invalid ECDH.amount size");
  700 |       memcpy(ecdh.amount.bytes, ack->ecdh_info().data(), 8);
```

_file_excerpt · [src/ringct/rctSigs.cpp](https://github.com/monero-project/monero/blob/3fd0f88c20f559839cafb20911cb13cb45eba7bd/src/ringct/rctSigs.cpp#L1573) · line 1573 · SHA-256 457fe6b06c26b300f98003a4b0493c6e84abdfae48a650dac0be78ba805af4c5_

```
 1572 |         key Ctmp;
 1573 |         CHECK_AND_ASSERT_THROW_MES(sc_check(mask.bytes) == 0, "warning, bad ECDH mask");
 1574 |         CHECK_AND_ASSERT_THROW_MES(sc_check(amount.bytes) == 0, "warning, bad ECDH amount");
```

_file_excerpt · [src/ringct/rctSigs.cpp](https://github.com/monero-project/monero/blob/3fd0f88c20f559839cafb20911cb13cb45eba7bd/src/ringct/rctSigs.cpp#L1574) · line 1574 · SHA-256 85f3eb7fcdfb06e0bff054a2e92336f11459a212c26b5ea7770cc9bcd8a4ee1d_

```
 1573 |         CHECK_AND_ASSERT_THROW_MES(sc_check(mask.bytes) == 0, "warning, bad ECDH mask");
 1574 |         CHECK_AND_ASSERT_THROW_MES(sc_check(amount.bytes) == 0, "warning, bad ECDH amount");
 1575 |         addKeys2(Ctmp, mask, amount, H);
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Classify each usage, record data lifetimes, and plan migration to Hybrid key establishment with ML-KEM (FIPS 203), e.g. X25519MLKEM768 in TLS 1.3 or mlkem768x25519-sha256 in SSH; introduce an abstraction layer for crypto-agility.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-05419 — block-buffer 0.10.4 is affected by GHSA-qwgh-2vcv-g2f7

- Severity: **Medium** · Classification: Known vulnerable component · Confidence: Low
- Affected asset: `dependency:crates.io/block-buffer@0.10.4`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 16:45 UTC
- Priority score: 33.1 / 100
- CVSS v3.1: not applicable

OSV.dev reports GHSA-qwgh-2vcv-g2f7 for crates.io package block-buffer at version 0.10.4: block_buffer: panic corrupts inline buffer position. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-qwgh-2vcv-g2f7
```

**Evidence.**

_tool_output · [OSV.dev GHSA-qwgh-2vcv-g2f7](https://osv.dev/vulnerability/GHSA-qwgh-2vcv-g2f7) · manifest · SHA-256 ac22c9ee6301d8c1e4b09ca6951303d71527ccba2df30c96af92531d8efbb71e_

```
{"id": "GHSA-qwgh-2vcv-g2f7", "aliases": [], "modified": "2026-08-19T19:30:06.686866977Z", "summary": "block_buffer: panic corrupts inline buffer position", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:L/VI:L/VA:N/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (none published yet; see the advisory for mitigations).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-05421 — keccak 0.1.5 is affected by GHSA-3288-p39f-rqpv (RUSTSEC-2026-0012)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/keccak@0.1.5`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 16:45 UTC
- Priority score: 25.0 / 100
- CVSS v3.1: not applicable

OSV.dev reports GHSA-3288-p39f-rqpv (RUSTSEC-2026-0012) for crates.io package keccak at version 0.1.5: Unsoundness in opt-in ARMv8 assembly backend for `keccak`. The affected code sits behind the `asm` Cargo feature, off by default, which no audited manifest enables: the advisory does not apply unless another dependency enables it.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-3288-p39f-rqpv
```

**Evidence.**

_tool_output · [OSV.dev GHSA-3288-p39f-rqpv](https://osv.dev/vulnerability/GHSA-3288-p39f-rqpv) · manifest · SHA-256 d5a8f5565101ab9d60521142f31c54583db5b87e9a59fc99e1fa93d6c2e5f782_

```
{"id": "GHSA-3288-p39f-rqpv", "aliases": ["RUSTSEC-2026-0012"], "modified": "2026-09-10T03:50:59.332505686Z", "summary": "Unsoundness in opt-in ARMv8 assembly backend for `keccak`", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:L/AC:H/AT:P/PR:N/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N/E:U"}], "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (0.1.6).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-05420 — crypto-bigint 0.5.5 is affected by RUSTSEC-2026-0387 (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/crypto-bigint@0.5.5`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 16:45 UTC
- Priority score: 20.3 / 100
- CVSS v3.1: not applicable

OSV.dev reports RUSTSEC-2026-0387 for crates.io package crypto-bigint at version 0.5.5: Multiple timing variability issues in operations intended to be constant-time. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0387
```

**Evidence.**

_tool_output · [OSV.dev RUSTSEC-2026-0387](https://osv.dev/vulnerability/RUSTSEC-2026-0387) · manifest · SHA-256 eab63427da988e95becf061fd8169abcb9634f743aeeb7567dfa2ba2667b05a5_

```
{"id": "RUSTSEC-2026-0387", "aliases": [], "modified": "2026-10-24T03:45:02.365137418Z", "summary": "Multiple timing variability issues in operations intended to be constant-time", "severity": null, "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Triage the advisory; upgrade to a fixed version (0.7.6) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-05418 — No post-quantum capable cryptographic library detected

- Severity: **Info** · Classification: Insufficient data · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `dependencies`
- Data source: dependency manifests
- Detection method: Dependency name matching.
- Analyzer: dependencies 1.2.0 · 2026-10-28 16:45 UTC
- Priority score: 13.3 / 100
- CVSS v3.1: not applicable

Across 2 dependency manifests, QSI found crypto libraries (curve25519-dalek, ecdsa, k256, p256) but none from its PQC-capable list.

**Potential impact.** Readiness indicator only: PQC support may come from the platform (OpenSSL, OS, cloud KMS) rather than application dependencies.

**Reproduction steps.**

```
Review the dependency manifests listed in the evidence.
```

**Evidence.**

_dependency · src/fcmp_pp/fcmp_pp_rust/Cargo.lock, src/fcmp_pp/fcmp_pp_rust/Cargo.toml · SHA-256 db5d4da5ee6bd5304400a63ce961218e4d81bf3dc595a99c76e75ace171c646c_

```
Crypto libraries: curve25519-dalek, ecdsa, k256, p256
```

**Limitations of the check.** Absence of evidence is not evidence of absence: system libraries and transitive dependencies may not be listed.

**Recommendation.** Confirm where PQC support will come from (TLS terminator, KMS/HSM, library upgrade).

**Retest procedure.** Re-scan after upgrades.


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
| **transaction and message signing** | Ed25519 (1) | QSI-2026-05417 | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains adopt them |
| **role not determined** | Ed25519 (4), ECDH (2), X25519 (2) | QSI-2026-05414, QSI-2026-05415, QSI-2026-05416 | Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it; introduce an abstraction layer for crypto-agility |

_Roles are judged from file paths, function names and the code around each match; review confirms them. Root-of-trust keys and wrapped keys come first: they are hard to replace or can be recorded today._
No readiness questionnaire was completed for this project.

### Quantum algorithms relevant to this inventory

| Quantum algorithm | Effect | Attack model | Inventoried algorithms (rows) | What it means for this audit |
|---|---|---|---|---|
| Shor's algorithm — elliptic-curve discrete logarithms | breaks | Q1 | Bulletproofs (4), ECDH (2), Ed25519 (5), X25519 (3) | Elliptic-curve keys are expected to fall before RSA keys of comparable classical strength. On blockchains, coins whose public key is already on chain (reused addresses, pay-to-public-key and Taproot outputs) are exposed first; plan the move to post-quantum signatures and avoid key reuse in the meantime. |
| Grover's algorithm — key search and preimages | weakens (larger keys restore the margin) | Q1 | AES-128 (1), BLAKE2 (3), ChaCha20-Poly1305 (3), HMAC (2), PBKDF2 (2), SHA-2 (4), SHA-3 (1) | Not a break. 256-bit keys (AES-256, ChaCha20) keep a comfortable margin; AES-128 meets NIST category 1, while some authorities ask for 256-bit keys in quantum-resistant contexts (see the AES-128 entry). Prefer 256-bit keys for long-lived data; 256-bit hashes need no change for preimage resistance. |
| Brassard–Høyer–Tapp — collision search | weakens (larger keys restore the margin) | Q1 | BLAKE2 (3), SHA-2 (4), SHA-3 (1) | 256-bit hashes (SHA-256, SHA3-256) remain adequate for collision resistance; 160-bit hashes are already weak classically (SHA-1 collisions are practical). Use 384/512-bit hashes where NIST categories 4–5 are required. |

_Effects: breaks — replace the algorithm; weakens — larger keys or outputs restore the margin; included in standard parameters — no action at standard parameter sets; only with superposition queries — not applicable to ordinary deployments._


## 9. Limitations and assumptions

- This report presents automated and documented analysis results for the stated scope. It is not a legal opinion, a certification or an attestation of compliance with any standard.
- z is a planning assumption chosen per risk profile, not a prediction. A cryptographically relevant quantum computer is not publicly known to exist today.
- certificates: src/common/dns_utils.cpp line 79: certificate could not be parsed (ValueError)
- tls_key_exchange_groups: src/ringct/multiexp.cc line 555: not in the algorithm registry, not assessed: (groups

## 10. Remediation plan / Priorities for 30, 60 and 90 days

### 30 days

| Priority | ID | Action | Type | Closure criteria |
|---|---|---|---|---|
| P2 | QSI-2026-05419 | Upgrade block-buffer to a fixed version (none published yet; see the advisory for mitigations). | root-cause fix | Dependency scan no longer reports GHSA-qwgh-2vcv-g2f7. |
| P2 | QSI-2026-05421 | Upgrade keccak to a fixed version (0.1.6). | root-cause fix | Dependency scan no longer reports GHSA-3288-p39f-rqpv (RUSTSEC-2026-0012). |
### 60 days

| Priority | ID | Action | Type | Closure criteria |
|---|---|---|---|---|
| P3 | QSI-2026-05420 | Triage RUSTSEC-2026-0387; upgrade crypto-bigint to a fixed version (0.7.6) if it applies. | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0387, or the triage is recorded. |
### 90 days

| Priority | ID | Action | Type | Closure criteria |
|---|---|---|---|---|
| P3 | QSI-2026-05417 | Add Ed25519 usages at the wallet's transaction signing to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-05414 | Add Ed25519 usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-05415 | Add X25519 usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-05416 | Add ECDH usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P4 | QSI-2026-05417 | Plan migration of Ed25519 to ? (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ? or a hybrid scheme in use. |
| P4 | QSI-2026-05414 | Plan migration of Ed25519 to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-05415 | Plan migration of X25519 to Hybrid key establishment with ML-KEM (FIPS 203), e.g. X25519MLKEM768 in TLS 1.3 or mlkem768x25519-sha256 in SSH (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows Hybrid key establishment with ML-KEM (FIPS 203), e.g. X25519MLKEM768 in TLS 1.3 or mlkem768x25519-sha256 in SSH or a hybrid scheme in use. |
| P4 | QSI-2026-05416 | Plan migration of ECDH to Hybrid key establishment with ML-KEM (FIPS 203), e.g. X25519MLKEM768 in TLS 1.3 or mlkem768x25519-sha256 in SSH (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows Hybrid key establishment with ML-KEM (FIPS 203), e.g. X25519MLKEM768 in TLS 1.3 or mlkem768x25519-sha256 in SSH or a hybrid scheme in use. |

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

1. A. Chailloux, M. Naya-Plasencia, A. Schrottenloher — An Efficient Quantum Collision Search Algorithm and Implications on Symmetric Cryptography (ASIACRYPT 2017; IACR ePrint 2017/847) — IACR ePrint. <https://eprint.iacr.org/2017/847> (peer-reviewed article: Õ(2^{2n/5}) time, O(n) qubits, Õ(2^{n/5}) classical memory)
2. C. Chevignard, P.-A. Fouque, A. Schrottenloher — Reducing the Number of Qubits in Quantum Discrete Logarithms on Elliptic Curves (IACR ePrint 2026/280) — IACR ePrint. <https://eprint.iacr.org/2026/280> (revision of a EUROCRYPT 2026 paper: 3.12n + o(n) qubits; for n = 256, 1193 qubits and 22 runs of 2^38.98 Toffoli gates)
3. C. Zalka — Grover's quantum searching algorithm is optimal (Phys. Rev. A 60, 2746, 1999; arXiv:quant-ph/9711070) — APS. <https://doi.org/10.1103/PhysRevA.60.2746> (peer-reviewed article: optimal for any success probability; parallel search gains no more than splitting the space)
4. Common Vulnerability Scoring System v3.1: Specification Document — FIRST. <https://www.first.org/cvss/v3.1/specification-document> (final)
5. D. J. Bernstein — Cost analysis of hash collisions: Will quantum computers make SHARCS obsolete? (2009) — cr.yp.to. <https://cr.yp.to/hash/collisioncost-20090823.pdf> (paper dated 2009-08-23)
6. D. Litinski — How to compute a 256-bit elliptic curve private key with only 50 million Toffoli gates (arXiv:2306.08585) — arXiv. <https://arxiv.org/abs/2306.08585> (preprint (2023-06-14): 6000 modules × 1152 physical qubits, one key per 10 minutes under its architecture assumptions)
7. FIPS 203 — Module-Lattice-Based Key-Encapsulation Mechanism Standard (ML-KEM) — NIST. <https://csrc.nist.gov/pubs/fips/203/final> (final (August 2024))
8. FIPS 204 — Module-Lattice-Based Digital Signature Standard (ML-DSA) — NIST. <https://csrc.nist.gov/pubs/fips/204/final> (final (August 2024))
9. FIPS 205 — Stateless Hash-Based Digital Signature Standard (SLH-DSA) — NIST. <https://csrc.nist.gov/pubs/fips/205/final> (final (August 2024))
10. G. Brassard, P. Høyer, A. Tapp — Quantum Algorithm for the Collision Problem (LATIN '98; arXiv:quant-ph/9705002) — Springer / arXiv. <https://arxiv.org/abs/quant-ph/9705002> (peer-reviewed article: collisions of r-to-one functions in O((N/r)^{1/3}) expected evaluations)
11. J. Proos, C. Zalka — Shor's discrete logarithm quantum algorithm for elliptic curves (Quantum Inf. Comput. 3(4), 2003; arXiv:quant-ph/0301141) — Quantum Information & Computation. <https://doi.org/10.26421/QIC3.4-3> (peer-reviewed article)
12. L. K. Grover — A fast quantum mechanical algorithm for database search (STOC 1996) — ACM. <https://doi.org/10.1145/237814.237866> (peer-reviewed article)
13. M. Amy et al. — Estimating the cost of generic quantum pre-image attacks on SHA-2 and SHA-3 (SAC 2016; arXiv:1603.09383) — Springer / arXiv. <https://arxiv.org/abs/1603.09383> (peer-reviewed article: SHA-256 about 2^153.8 surface-code cycles on 2^12.6 logical qubits; SHA3-256 about 2^146.5 cycles on 2^20)
14. M. Cain et al. — Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits (arXiv:2603.28627) — arXiv. <https://arxiv.org/abs/2603.28627> (preprint (2026-03-30): P-256 in a few days with 26,000 physical neutral-atom qubits; RSA-2048 one to two orders of magnitude longer)
15. M. Mosca — Cybersecurity in an Era with Quantum Computers: Will We Be Ready? (IEEE Security & Privacy, 2018) — IEEE. <https://doi.org/10.1109/MSP.2018.3761723> (peer-reviewed article; source of the x + y > z migration inequality)
16. M. Roetteler, M. Naehrig, K. Svore, K. Lauter — Quantum resource estimates for computing elliptic curve discrete logarithms (ASIACRYPT 2017) — IACR / arXiv. <https://arxiv.org/abs/1706.06752> (peer-reviewed article: at most 9n + 2⌈log2 n⌉ + 10 qubits and 448 n^3 log2 n + 4090 n^3 Toffoli gates)
17. NIST IR 8547 — Transition to Post-Quantum Cryptography Standards — NIST. <https://csrc.nist.gov/pubs/ir/8547/ipd> (initial public draft (November 2024); proposes deprecating quantum-vulnerable public-key algorithms after 2030 and disallowing them after 2035 — dates may change in the final version)
18. NIST — Post-Quantum Cryptography Standardization: Evaluation Criteria, Security (Call for Proposals, Section 4.A.5) — NIST. <https://csrc.nist.gov/Projects/Post-Quantum-Cryptography/Post-Quantum-Cryptography-Standardization/Evaluation-Criteria/Security-(Evaluation-Criteria)> (security categories: AES-128 key search 2^170/MAXDEPTH quantum gates, AES-192 2^233/MAXDEPTH, AES-256 2^298/MAXDEPTH; MAXDEPTH 2^40–2^96)
19. OSV advisory GHSA-3288-p39f-rqpv — OSV.dev. <https://osv.dev/vulnerability/GHSA-3288-p39f-rqpv> (modified 2026-09-10T03:50:59.332505686Z)
20. OSV advisory GHSA-qwgh-2vcv-g2f7 — OSV.dev. <https://osv.dev/vulnerability/GHSA-qwgh-2vcv-g2f7> (modified 2026-08-19T19:30:06.686866977Z)
21. OSV advisory RUSTSEC-2026-0387 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0387> (modified 2026-10-24T03:45:02.365137418Z)
22. P. W. Shor — Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms on a Quantum Computer (SIAM J. Comput., 1997) — SIAM. <https://doi.org/10.1137/S0097539795293172> (peer-reviewed article)
23. R. Babbush et al. — Securing Elliptic Curve Cryptocurrencies against Quantum Vulnerabilities: Resource Estimates and Mitigations (arXiv:2603.28846) — arXiv. <https://arxiv.org/abs/2603.28846> (preprint (2026-03-30, v2 2026-04-15): 256-bit ECDLP with < 1200 logical qubits and < 90 M Toffoli gates (or < 1450 and < 70 M); < 500,000 physical qubits at 10^-3 error, minutes)
24. S. Jaques, M. Naehrig, M. Roetteler, F. Virdia — Implementing Grover oracles for quantum key search on AES and LowMC (EUROCRYPT 2020; arXiv:1910.01700) — Springer / arXiv. <https://arxiv.org/abs/1910.01700> (peer-reviewed article: lower cost estimates for the AES key searches that define the NIST categories)

## Appendices: Cryptographic inventory

| Algorithm | Parameter | Library | Quantum status | Classical status | Count | Locations | Examples |
|---|---|---|---|---|---|---|---|
| ChaCha20-Poly1305 | ChaCha20-Poly1305 |  | reduced margin (Grover), approved | acceptable | 3 | 3 | src/crypto/crypto_ops_builder/include/sodium.h:6; src/device_trezor/trezor/protocol.cpp:45; src/device_trezor/trezor/protocol.hpp:95 |
| HMAC |  |  | reduced margin (Grover), approved | acceptable | 2 | 2 | src/crypto/hmac-keccak.c; src/crypto/hmac-keccak.h |
| PBKDF2 |  |  | reduced margin (Grover), approved | acceptable | 2 | 2 | src/mnemonics/polyseed/pbkdf2.c; src/mnemonics/polyseed/pbkdf2.h |
| SHA-2 | SHA-512 |  | reduced margin (Grover), approved | acceptable | 3 | 3 | src/crypto/crypto_ops_builder/sha512-blocks.c; src/crypto/crypto_ops_builder/sha512-hash.c; src/crypto/crypto_ops_builder/sha512.h |
| AES-128 | AES-128 |  | Grover: acceptable to NIST, below ECCG/ANSSI guidance | acceptable | 1 | 1 | src/gen_ssl_cert/gen_ssl_cert.cpp:191 |
| BLAKE2 |  |  | Grover: acceptable to NIST, below ECCG/ANSSI guidance | acceptable | 3 | 3 | src/crypto/blake2b.c; src/crypto/blake2b.h; src/crypto/crypto_ops_builder/include/sodium.h:17 |
| SHA-2 |  |  | Grover: acceptable to NIST, below ECCG/ANSSI guidance | acceptable | 1 | 1 | src/common/util.cpp:688 |
| SHA-3 |  |  | Grover: acceptable to NIST, below ECCG/ANSSI guidance | acceptable | 1 | 1 | src/net/tor_address.cpp:297 |
| Crypto library | 0.13.2 | p256 (RustCrypto elliptic curves) | n/a | acceptable | 1 | 1 | src/fcmp_pp/fcmp_pp_rust/Cargo.lock |
| Crypto library | 0.13.4 | k256 (RustCrypto elliptic curves) | n/a | acceptable | 1 | 1 | src/fcmp_pp/fcmp_pp_rust/Cargo.lock |
| Crypto library | 0.16.9 | ecdsa (python-ecdsa) | n/a | acceptable | 1 | 1 | src/fcmp_pp/fcmp_pp_rust/Cargo.lock |
| Crypto library | 4.1.3 | curve25519-dalek (ed25519-dalek) | n/a | acceptable | 1 | 1 | src/fcmp_pp/fcmp_pp_rust/Cargo.lock |
| Bulletproofs |  |  | vulnerable (Shor) | acceptable | 4 | 4 | src/ringct/bulletproofs.cc; src/ringct/bulletproofs.h; src/ringct/bulletproofs_plus.cc |
| ECDH |  |  | vulnerable (Shor) | acceptable | 2 | 2 | src/device_trezor/trezor/protocol.cpp:699; src/ringct/rctSigs.cpp:1573 |
| Ed25519 | Ed25519 |  | vulnerable (Shor) | acceptable | 4 | 4 | src/crypto/crypto_ops_builder/crypto_sign.h:10; src/crypto/crypto_ops_builder/include/sodium.h:32; src/crypto/crypto_ops_builder/ref10/keypair.c:7 |
| Ed25519 | CLSAG ring signatures on the Ed25519 curve |  | vulnerable (Shor) | acceptable | 1 | 1 | src/device_trezor/trezor/protob/messages-monero.proto:2 |
| X25519 | X25519 |  | vulnerable (Shor) | acceptable | 3 | 3 | src/crypto/crypto_ops_builder/include/sodium.h:25; src/crypto/x25519.cpp:30; src/crypto/x25519.h |

_Long lists are grouped here; the full per-file list is in the JSON report, signed with the same key._

## Appendices: Input files

| File | Size | SHA-256 | Redactions |
|---|---|---|---|
| src/blockchain_db/blockchain_db.cpp | 14998 | `890ecabf5b5b3046efc36767bebb115654e662633df252af4c5c94dbf8fa7ab0` | 0 |
| src/blockchain_db/blockchain_db.h | 65455 | `9f95afd9ba80177d01c5ce2a38559cf8056ea2062c0971374b0e4cbcc902a1cd` | 0 |
| src/blockchain_db/lmdb/db_lmdb.cpp | 199577 | `ddb3f55db39b117b77fae106977c1f953cc7f294ec0015cc4547a1836431181b` | 0 |
| src/blockchain_db/lmdb/db_lmdb.h | 19787 | `2bbc80cd3f0eac0542dbf314cafc7748c93e86d3dda39ff5e891fee33563a6fc` | 0 |
| src/blockchain_db/locked_txn.h | 2725 | `b951cbb91e2ce9822ddd1b79efdbc6101786b27ceb8f307d50eb7db49b88e185` | 0 |
| src/blockchain_db/testdb.h | 14991 | `c994d82bfcd68fc243efcc9d4bc3af0444bf4aefbb7a06dd3115305cd55d608a` | 0 |
| src/blockchain_utilities/blockchain_ancestry.cpp | 25111 | `1be8151d216744856a96fcd757c9abe9edbcd38ed498ea05edafc6d8f42f3e80` | 0 |
| src/blockchain_utilities/blockchain_depth.cpp | 12179 | `f312d133720dbba014b68f432f5e52e48bcf336cd6612560ee3fabd037f00774` | 0 |
| src/blockchain_utilities/blockchain_export.cpp | 7117 | `09d63a1b7df2f44f5ce82a3ebd039feb5c7ea9705ae535150077cfc0ac8e5304` | 0 |
| src/blockchain_utilities/blockchain_import.cpp | 25490 | `0cc04b1128dc6914e55472b56391404439eb4d0540acd0d431f72eaebe1d1617` | 0 |
| src/blockchain_utilities/blockchain_prune.cpp | 28434 | `c86e11a72f5411d087c465fd8e03955b206a6fe75d065a52e756727fbff70bb8` | 0 |
| src/blockchain_utilities/blockchain_prune_known_spent_data.cpp | 9632 | `590311cbf7bcf1b43fad9bb16f017373774bc516238363544ad02e2677ad62ad` | 0 |
| src/blockchain_utilities/blockchain_stats.cpp | 13527 | `e0590a2821af17c404e7acaee96361ad1893a0bb07f3010941a1148a9288eb29` | 0 |
| src/blockchain_utilities/blockchain_usage.cpp | 8669 | `69d8fb3002050900298e5b033cf62fbdec9133c3a4935703fbab39e500cf45ce` | 0 |
| src/blockchain_utilities/blockchain_utilities.h | 1878 | `ec9af7520b77f351f2fb14054802d5ad3ab14f6199e7b673cfaa12d3059d1813` | 0 |
| src/blockchain_utilities/blocksdat_file.cpp | 6325 | `d1ec96224cfb317ba72eb593a9f42dc38d7e2ec6d2cd967ee60465e28332e9c2` | 0 |
| src/blockchain_utilities/blocksdat_file.h | 2851 | `9b832d52d85361da3210a24988920eb5469ff44fb4b25be0a2b02743ca976b33` | 0 |
| src/blockchain_utilities/bootstrap_file.cpp | 20694 | `936637ad87c6e09aa232c0dbc335b9422c6b341809115479b75ebec2db4decec` | 0 |
| src/blockchain_utilities/bootstrap_file.h | 3632 | `7b827ae0f6668b504315db0df26855abf765763b16d58b96fe4e792a27df558a` | 0 |
| src/blockchain_utilities/bootstrap_serialization.h | 3253 | `563c0471b16361bdf72e242a9624ad2c07da7398c17c0f55411db33f7e0fc887` | 0 |
| src/blocks/blocks.cpp | 953 | `c7a8210a3988eceb40614e11d709b89309c928bb03b36038e22f11cc658ea5dd` | 0 |
| src/blocks/blocks.h | 261 | `516a7d0c3eca2ba098e870799fadf336b0fd5fc7b05ae1749e47ef2fe0b6d874` | 0 |
| src/checkpoints/checkpoints.cpp | 18539 | `0aed431c9dae90fea54352ad178e36a0c4de9691854b611664b487f17f0d3a37` | 0 |
| src/checkpoints/checkpoints.h | 7925 | `3885e86d412d43ba1760d7906d3bca1d1513e776fa88b7b708f6d44c379d859c` | 0 |
| src/common/aligned.c | 4016 | `43b5fe181d2b96dee9b93f6ca28e53e4939a9bf7e2d0c55c4713389442ff4dcf` | 0 |
| src/common/aligned.h | 1897 | `7542430220ae4323f0b9ff95c9a8fa5c22f99fe01f65690329e633dce65e20d3` | 0 |
| src/common/apply_permutation.h | 3139 | `5e4df1872cdb736f7779073982f4f243912914943f73e4d21c5c8636cfe32f18` | 0 |
| src/common/base58.cpp | 8837 | `c8fe6a65c896ed0cb0cf15da636aecaba91dbae74d4c46d8d238f5a7ee9b9677` | 0 |
| src/common/base58.h | 2041 | `d1e4aa494afcfa1f3a8c7db7ab954c1e627f7e39a393c3476a7a2c8743a225b2` | 0 |
| src/common/combinator.cpp | 1960 | `080cb5468b083aefb5adad0b79dbd5c77d1b4c0e2339d2449a39cdfa32f0313a` | 0 |
| src/common/combinator.h | 2933 | `f551c2c9f06e7339185ffad5ab8e47ae2de98b6225b7dd776403a752205ed9be` | 0 |
| src/common/command_line.cpp | 2814 | `66c5c1c2068e42f121e3b7832cd2f4de9b48859acf52c9647365db549b500ed4` | 0 |
| src/common/command_line.h | 9584 | `3c28f210b54126bb49d20f79de04691b35dfa9af7cbdc5f997217f82513cfb3a` | 0 |
| src/common/common_fwd.h | 1823 | `9af357568cefeef0716c0595b7d6ac4d1756a86899e8656cd3d47b2071df3daf` | 0 |
| src/common/container_helpers.h | 6318 | `d48485d9ecb19c8dffa6945265003ee61905c49df6e29cd71a07aaa5fc8e2c49` | 0 |
| src/common/dns_utils.cpp | 18122 | `901dc39605a1abe1cfbdfdc099db215b0fbdcc5d4a74caab8be6b8962cf851a4` | 0 |
| src/common/dns_utils.h | 6858 | `5e61a2c1f7623e14da75973333085470b5d2eff7c3f87a79ed21fb9cb214960a` | 0 |
| src/common/download.cpp | 12535 | `d85190aee67a61f17aea6d816511cf0605ec4e7d433df9263948ecc06220cf5f` | 0 |
| src/common/download.h | 2576 | `c2cf51c93cb04cf065a0658fe5e20cd00c579aba413463e584d6d814ada8ea71` | 0 |
| src/common/error.cpp | 2997 | `55e30474dfcf316a11e00851e1d77ab45382caedd016ab052836cca0ba17c8f7` | 0 |
| src/common/error.h | 2170 | `557d3b8d8972a0aef0845fe0c1860eca9358bbecfb9feb50e0271d4f63feb655` | 0 |
| src/common/expect.cpp | 2780 | `ebc611bd15a0ea473e52ed4e600efeb8fae9ee1128dbb42ba70b0cef8090863e` | 0 |
| src/common/expect.h | 15578 | `06987bba9651a493267083e57232dcccb01165bbc5c8ae9b7f6060f360bf2bc1` | 0 |
| src/common/hash_combine.h | 1925 | `99ebe9023c690ae314928bb2e7785f058fb2db0a73aa46cf19e9a6b43b884f42` | 0 |
| src/common/http_connection.h | 2387 | `02967080463dffb770a210c7286c98565ad6beaeac37bf2f8843103b940445d5` | 0 |
| src/common/i18n.h | 1764 | `ffc4ba21b5730841063ab9c28d81ee447ab9658dc49ca30decadb600f642218e` | 0 |
| src/common/json_util.h | 2266 | `f72581d610f82053c7849fea6ddf471a290c887288c393888895da487efc85a6` | 0 |
| src/common/notify.cpp | 3095 | `6f8b2d581f3574bb066309e1de4599a568c0da1a02ac446b92210882d4f962bb` | 0 |
| src/common/notify.h | 1998 | `8ce1eaaf309623a589f1422c70b23f4fe32bc690e7fb21ff2d3d0cab2c8369be` | 0 |
| src/common/password.cpp | 7761 | `b7b1e1c2e7110f2ae3602aecb7b91e4c75ea5bdda8bfbfa1cd772331b0b961b6` | 0 |
| src/common/password.h | 3912 | `dcfd038b0ca8d6cd316e81368de633678ccbd8f6480229c2b23299b30cdec2b4` | 0 |
| src/common/perf_timer.cpp | 5978 | `66201160bab1cf6c9c5bfebfdda8a7cda1a7fed888c97265b9705393d7cd1bde` | 0 |
| src/common/perf_timer.h | 3242 | `5b9d780468eacfe5cfeadbab956f60caf69c333cbc86f45c261e903924680249` | 0 |
| src/common/powerof.h | 353 | `4669eb750178448dd9775a91708540996538c2e90f7894ba8b4c41e1a74b86b3` | 0 |
| src/common/pruning.cpp | 5637 | `5ca6dbfd1955cc20652340f38a09bde3095a25dfb009b767138a7bd5b60240bd` | 0 |
| src/common/pruning.h | 2890 | `99b109af93885f5d25df1eec6dc73bb92b816bef51bde5760f833d56c21e6bfb` | 0 |
| src/common/rpc_client.h | 4273 | `e60fe2835eed2eb8f7cb6105a414068b9170e7d177e2bd9f73e91440b3b8b892` | 0 |
| src/common/scoped_message_writer.h | 4377 | `8794aa8d232a721826938cc4f36890fee7898030e0b00a2f0e85ecad4a62c61a` | 0 |
| src/common/sfinae_helpers.h | 5127 | `57881b5a5a96b742c30d9d7a0a23b2e9b7c89e882db3b4c224544a38cc2be549` | 0 |
| src/common/spawn.cpp | 4216 | `576fb7ef7f6a79cb386bf3f557775a47eefd8f9cad63c8733049a27a26077c42` | 0 |
| src/common/spawn.h | 1748 | `a48847020b18a58cb752775e3ad67874ad274919c8aac56577588385972a4eb8` | 0 |
| src/common/stack_trace.cpp | 5655 | `cc3a10a9287929dc7170469bb09059ef42a8c209f43369b024bbf0c8d6309319` | 0 |
| src/common/stack_trace.h | 1736 | `09257cfdac0924837ea5ff22d0ba3542a93983feb775dfa31f1229ffd8bb2ef8` | 0 |
| src/common/threadpool.cpp | 5094 | `f1d905daeb44a8212ceea81e697144abb79f16f0e7e4283a615356f69d717e1e` | 0 |
| src/common/threadpool.h | 3546 | `7293c96684cda10ba3d620d30d94396cfd20e6998e24f8b8a86bb8d1c852b858` | 0 |
| src/common/timings.cc | 4265 | `25b7cca7c8fd78d170ce437ef0b1568ca22f1f1fa6f727ac1cc8d3c8f9cd3472` | 0 |
| src/common/timings.h | 687 | `d05dcb2f54d461991268b4f6ec018d8b3faff602e84a5a036051e947ad644428` | 0 |
| src/common/unordered_containers_boost_serialization.h | 4474 | `282c8091c7cb455f85ecaec302cfad06c5e14b2b3e43a444f8e79fa5d2daf075` | 0 |
| src/common/updates.cpp | 4443 | `40c2c39f8978779647adf830064992a53697b9657d4d34ce38107803bea4e4c0` | 0 |
| src/common/updates.h | 1921 | `294ade0f86f9fdfff401118853a04d31690cb0e720507ca7439065456a485fb9` | 0 |
| src/common/utf8.h | 3844 | `584f39c455b3693c6ad5870e5ec4e1ddc065497d86a6ecd18569c388498305e9` | 0 |
| src/common/util.cpp | 34509 | `9be89e62f530d6f487df8a54c501ee44698fcb167543f08a2f2fa628dc90042f` | 0 |
| src/common/util.h | 8431 | `cf67beb2f899e754198d25b6592ae24c315fb8a9716f1300012cc8fc487a1572` | 0 |
| src/common/va_args.h | 1868 | `b15e986afe97d30cf756892ec561ce5305cf59829d947c515da8d8d999bddfdb` | 0 |
| src/common/varint.h | 5200 | `5db99e352da835800079fd971fee46d9369c30f73488d0a49f7ada812018868f` | 0 |
| src/crypto/CryptonightR_JIT.c | 3327 | `dff68e134c9eb3fa01769260354e63abc77ce890ffca278b0e4663974e0bbeb3` | 0 |
| src/crypto/CryptonightR_JIT.h | 853 | `a062cdfda3df5f5f9d23a23440930811281b8045b6d202ed4fcaa6f57a896e9a` | 0 |
| src/crypto/CryptonightR_template.h | 45536 | `a10ec27257974333a662c19193babd2708ad165428bae2ed83f8cdfba3460627` | 0 |
| src/crypto/aesb.c | 7200 | `fec400edc936046855faf8cb3dc2508451588ee37fee7423ebbd95ee931d0150` | 0 |
| src/crypto/blake256.c | 11334 | `e97b22ff7c9022b41eba55cedf185431dffbf355f333ab12bbe68af065370f92` | 0 |
| src/crypto/blake256.h | 2884 | `6550d57620c3a3a6d2ed59353655b984b8463d020e77ab41a12ce8ee46b51462` | 0 |
| src/crypto/blake2b.c | 16682 | `cc7fd489f410caf9db9f24d8d43d1ab8bd7cefd239f44e284940a63e30522ebb` | 0 |
| src/crypto/blake2b.h | 4363 | `1ac31a0e76721d1be876d0162da58ccd35d5dd7576ea90889990c1e66af9d5e8` | 0 |
| src/crypto/c_threads.h | 3814 | `14cfa2506e924ba0c8c532df55ef1721f858d085befbbb12713f4d077ae8af47` | 0 |
| src/crypto/chacha.c | 5152 | `39217bce7447a4e7aa7df9e827068f91bc085bf67001a8fbed8abd3c1ce6fd93` | 0 |
| src/crypto/chacha.h | 4329 | `67afe061305907098f1562c3758e24a3bff08b3bfc0184557345f3ddc24fe218` | 0 |
| src/crypto/crypto-ops-data.c | 89586 | `94bee88043845662892a6f489347ad2b4f37744ff6b21c47a1aa0f3e52aed985` | 0 |
| src/crypto/crypto-ops.c | 119401 | `7da995bedd791475d85c9f7f1fde32c2b287a64d7184a294abacad53c0ca64ed` | 0 |
| src/crypto/crypto-ops.h | 8021 | `9b2d2e0bbfd9c8061607ca596f21e4d2ddb0b25d0225fd88590feb07eaeab5e9` | 0 |
| src/crypto/crypto.cpp | 28177 | `4262aaf44304788f07660abc7c75df0d0042aa280ba064d0244c5f075b0c5859` | 0 |
| src/crypto/crypto.h | 17990 | `875e5755a556cb4d6a1ae4d03850985a9d558f9951633a51519fb2f78b332faf` | 0 |
| src/crypto/crypto_ops_builder/api.h | 54 | `964817f8bb5b69762a52352a9a37d4e1ef4edf06f40c8c063891ffe83762bc72` | 0 |
| src/crypto/crypto_ops_builder/crypto-ops-data.c | 88295 | `d3d062b58f7f217a2ff3bb2e0c40c4592d7ecb771069bf1aa1154e6a4423efff` | 0 |
| src/crypto/crypto_ops_builder/crypto-ops-old.c | 88461 | `e81ec67482514e89f91885fa1d6458b809db932f98d66a9bb4b6a27ca21703f3` | 0 |
| src/crypto/crypto_ops_builder/crypto-ops.h | 4248 | `8bfd65dc841ff9db62578ca879b00703603b2477c45a4cbe40119f05d4098cf6` | 0 |
| src/crypto/crypto_ops_builder/crypto_int32.h | 81 | `238803073441714ec17cd8b5f499f697f3dced53951daec0746eb79be45693d7` | 0 |
| src/crypto/crypto_ops_builder/crypto_sign.h | 593 | `37bae804bf4516a7150f53b9ce93cc8afeea6ea0f7844e8cf1a8afe9bfcdd928` | 0 |
| src/crypto/crypto_ops_builder/crypto_uint32.h | 93 | `13f943899ccdbaf3b50fdab4658a1ca67d59abdb17c08a6be6ed31a30378556d` | 0 |
| src/crypto/crypto_ops_builder/crypto_verify_32.h | 175 | `bf7159913d5daf6d43841b41d48a95162137b7a76061f4d6f93d58bc003db903` | 0 |
| src/crypto/crypto_ops_builder/include/sodium/crypto_int32.h | 106 | `7466cd927cf8d488429f07f67d5ab4e7b44d5f03255854f5ce94e90d31f22591` | 0 |
| src/crypto/crypto_ops_builder/include/sodium/crypto_int64.h | 106 | `84789af2e9d29ee05909fbfd4fca6e53066a99b170494d56bf40d0322f98aa67` | 0 |
| src/crypto/crypto_ops_builder/include/sodium/crypto_uint16.h | 110 | `72c0ee8769c0be4cebed882b7daf429364be15acd3345eb489a5cefdc49a61c6` | 0 |
| src/crypto/crypto_ops_builder/include/sodium/crypto_uint32.h | 110 | `95ade98289486611bc56e1b11e0e99a4c3df02973048dc40275e60350ecbce8b` | 0 |
| src/crypto/crypto_ops_builder/include/sodium/crypto_uint64.h | 110 | `039abc368ad01d76295be0bbea2b64ccb449a76444a001b476fbc05a91c1d742` | 0 |
| src/crypto/crypto_ops_builder/include/sodium/crypto_uint8.h | 106 | `dedaa634cd59ebc5db41be8ae0536114652f601df95938c96e3865d7240d81e4` | 0 |
| src/crypto/crypto_ops_builder/include/sodium/crypto_verify_32.h | 344 | `c0027cf769c1f6a01c2df6a58cac045157f5da304974efdcecd8f000d72f422b` | 0 |
| src/crypto/crypto_ops_builder/include/sodium/randombytes.h | 1362 | `e17ffd7744c59d66844cf0db1fdc3eb271a92b6eca82e219b3ae6e81fdf5f922` | 0 |
| src/crypto/crypto_ops_builder/include/sodium.h | 1814 | `010e58c066e38efea63848b024903cfdc5f659a8495bdc7f1c3f4a45f366dcb9` | 0 |
| src/crypto/crypto_ops_builder/randombytes.c | 1011 | `2f91ccc384c1f86077f1e5cea9152b23458cd4304433a8097e49c92e9af2f23c` | 0 |
| src/crypto/crypto_ops_builder/ref10/api.h | 121 | `9d7cfd2c451dcf8ca38837dd602c8915ec246ed461a355c218a2bf9edd48ea6c` | 0 |
| src/crypto/crypto_ops_builder/ref10/base.h | 76457 | `dac873e5965b34e29a14b56bc63f9434fbba16b3513daf53c7b0b2d07b614ac0` | 0 |
| src/crypto/crypto_ops_builder/ref10/base.py | 1343 | `83148d97984e2812d79eddfb06942217db284a7ab6077d05e309e6fff66314af` | 0 |
| src/crypto/crypto_ops_builder/ref10/base2.h | 2388 | `1dbe1b61a3b7689d840eec4be7569261d719e67cf9ed5ad1b51c5e34583bec94` | 0 |
| src/crypto/crypto_ops_builder/ref10/base2.py | 1231 | `59566c7896508e4adcad02b37410703d10f5cac0726c60f3b81944809468022f` | 0 |
| src/crypto/crypto_ops_builder/ref10/d.h | 91 | `4729f3315d4815f5f3cb47d3f176ad0e907471aa3a9afc8d80484d2da98723a2` | 0 |
| src/crypto/crypto_ops_builder/ref10/d.py | 565 | `6c9277207d8537153653f936d51e8fac47203e78d9c341e2bccb919619e7d440` | 0 |
| src/crypto/crypto_ops_builder/ref10/d2.h | 90 | `0248fcb39acf255d78e0d19d6d605275a1939a7f61001f58f376569ecc0c5256` | 0 |
| src/crypto/crypto_ops_builder/ref10/d2.py | 567 | `e3aff85dcca7c5706e8a94d045e3246f8786c834074edf1d3ee41bc983e10156` | 0 |
| src/crypto/crypto_ops_builder/ref10/fe.h | 1939 | `37c8cf172c190b37134e6c9f9bf61f12c790126ecedc2abd6ecddffa71a4fd92` | 0 |
| src/crypto/crypto_ops_builder/ref10/fe_0.c | 170 | `825fc6d85b392d15c9b26c26ad2ccfb664a1c09658d8e2d26c54e37ac6e8b509` | 0 |
| src/crypto/crypto_ops_builder/ref10/fe_1.c | 170 | `a7ab32148848f7c44bc78b1e6d53c7bd633f629694b3b2dc075cc06d5eb17054` | 0 |
| src/crypto/crypto_ops_builder/ref10/fe_add.c | 1255 | `f838729610a80bb3a988fdfe1a8a9e9ab01648006492adf1ff35b544a38cf398` | 0 |
| src/crypto/crypto_ops_builder/ref10/fe_cmov.c | 1283 | `dc5f5993f3268ee20a333407e2d4b7a26a38ce1f8be7ce20b11c7d8f05efe03d` | 0 |
| src/crypto/crypto_ops_builder/ref10/fe_copy.c | 454 | `0f91f42eac64053f508537fff726561d2e21cd88f5f7fa304f34f419545a9121` | 0 |
| src/crypto/crypto_ops_builder/ref10/fe_frombytes.c | 2222 | `ae43a9b293d0950e4a87b5fdeaf59fbb9374aaa910f7aa295ee9e9521cec9a8a` | 0 |
| src/crypto/crypto_ops_builder/ref10/fe_invert.c | 135 | `504b694c38ab523f9514164a6f19dfa2987e5561525e4ebb1964c33028b0a6fb` | 0 |
| src/crypto/crypto_ops_builder/ref10/fe_isnegative.c | 266 | `c15116f89c80c6d393e6aa2e8ef6ad8b164e7b61f04bd208064f61e70f394697` | 0 |
| src/crypto/crypto_ops_builder/ref10/fe_isnonzero.c | 315 | `d39c476ead289b2cb93d11588afe13f24ba824af81e45ee935930f4d02587443` | 0 |
| src/crypto/crypto_ops_builder/ref10/fe_mul.c | 10744 | `77a67c16eebaa095e171caca018ceee1646a737eb314cebe72f05fff8a7d6b14` | 0 |
| src/crypto/crypto_ops_builder/ref10/fe_neg.c | 855 | `3ce85c334bbe9fa2e7e231d2319ec3d29cd03781c7b3108570635348652732c5` | 0 |
| src/crypto/crypto_ops_builder/ref10/fe_pow22523.c | 127 | `c6fca170f96ae1decbf89b9a0eef5e3973e3332fb064d8a39da20535148fdbc7` | 0 |
| src/crypto/crypto_ops_builder/ref10/fe_sq.c | 5980 | `a35384fbebe43092b465a2abd12abbf2ae1b2f337a711688c5487c06ce0dc56e` | 0 |
| src/crypto/crypto_ops_builder/ref10/fe_sq2.c | 6106 | `2abf4c6b3ed21ed8a805f2c0be1b9db4d88cdde9a0c710f24d070c5f2d01e076` | 0 |
| src/crypto/crypto_ops_builder/ref10/fe_sub.c | 1255 | `1a2afa4c5fc5fcec3dfd1344dbb41ba3b1c93acea47f74b413216b9c8f374c11` | 0 |
| src/crypto/crypto_ops_builder/ref10/fe_tobytes.c | 3189 | `678b10c1f49937ceccabddbaebe0982dea91a2620bdd81e29207178a959d97aa` | 0 |
| src/crypto/crypto_ops_builder/ref10/ge.h | 2869 | `827267cd894408c3e10443a51c257ce5dfc93ad032eff178a101d12cc9d1ace7` | 0 |
| src/crypto/crypto_ops_builder/ref10/ge_add.c | 125 | `cc236e58ad907a18671f2b5782ff9f4d2383a9848bc589b9fda83b3ecc55c05a` | 0 |
| src/crypto/crypto_ops_builder/ref10/ge_add.h | 2080 | `ac78e776b39f2eb09cb6588bb86f34f3cf970f81d124136920bf8ba5c3e8b3b8` | 0 |
| src/crypto/crypto_ops_builder/ref10/ge_double_scalarmult.c | 2371 | `225189d7203c85950c21a0a19120919bcc2cf91b50fa6c7453106321b362c463` | 0 |
| src/crypto/crypto_ops_builder/ref10/ge_frombytes.c | 987 | `6e65ae1c056f1dc11da16b2bd4aabad151db3abcd5ab7fbfaca7e784c18496d1` | 0 |
| src/crypto/crypto_ops_builder/ref10/ge_madd.c | 128 | `daf288d47d4d7356821912391ad2279a7ae5696a28bde7830b1660672ab5e6b4` | 0 |
| src/crypto/crypto_ops_builder/ref10/ge_madd.h | 1900 | `a39615f652006291a3fb0299728243191937b98e0e91fc8bf8196f96075a8d60` | 0 |
| src/crypto/crypto_ops_builder/ref10/ge_msub.c | 128 | `a7e060f539ad7a19428491fce2328ab2d5a6b5e1967a41e24bea8c80fe526a15` | 0 |
| src/crypto/crypto_ops_builder/ref10/ge_msub.h | 1900 | `ee0e1ecc451b7b30ea9ba9c71035d371414ce26267ca94523b12877a01c84e82` | 0 |
| src/crypto/crypto_ops_builder/ref10/ge_p1p1_to_p2.c | 165 | `be6e9b143c304c652534eea0fa9c92031005db7c83b824e7cf95581c093f9983` | 0 |
| src/crypto/crypto_ops_builder/ref10/ge_p1p1_to_p3.c | 191 | `ce67bc193d4d9c81ff18532ab5c1e74ccf519e8349ed19ff112feb22df27a3d2` | 0 |
| src/crypto/crypto_ops_builder/ref10/ge_p2_0.c | 86 | `1277df80612424d2eeb17e6700687b6fa24bfb5549f774c2112bc20fc39ebcfb` | 0 |
| src/crypto/crypto_ops_builder/ref10/ge_p2_dbl.c | 112 | `3d6aba9a349542b8350c5bbc8f69252d463b14605ad65d35241e89812482e780` | 0 |
| src/crypto/crypto_ops_builder/ref10/ge_p2_dbl.h | 1476 | `68aece7c0d6d99f8c6a91b4708d85336f060f9dfe171c1484097c4e380d1f884` | 0 |
| src/crypto/crypto_ops_builder/ref10/ge_p3_0.c | 100 | `e11b72f763151ef2ce652a0bf7991673b01e6ce74f15e90fd4af28cde505a52b` | 0 |
| src/crypto/crypto_ops_builder/ref10/ge_p3_dbl.c | 131 | `343ec8eddef9d91d130e3bbf443cdd64d226cd129530fede2126a837e31aab49` | 0 |
| src/crypto/crypto_ops_builder/ref10/ge_p3_to_cached.c | 246 | `7fb03b81ba8d513990c3ed90128fcb8bbff1012d8a4e7573fb50a0c0c6af0fcf` | 0 |
| src/crypto/crypto_ops_builder/ref10/ge_p3_to_p2.c | 149 | `1a29bfa686815c7c694d6cd2c660314f00e2bc53278478b7d8d51ede5133c34d` | 0 |
| src/crypto/crypto_ops_builder/ref10/ge_p3_tobytes.c | 228 | `232f48e92a096e1a9c5c18ce2bc80583d42236740501bff7d57eb9b9cc6310f4` | 0 |
| src/crypto/crypto_ops_builder/ref10/ge_precomp_0.c | 110 | `602db7879544d2084b3a6b21b33950b2b6974fabc36a8c867ad7207ac7a7b115` | 0 |
| src/crypto/crypto_ops_builder/ref10/ge_scalarmult_base.c | 2477 | `08d424c208d9f52a0dce884720413dc37449bee2ea6997e0d1cc5061433ff445` | 0 |
| src/crypto/crypto_ops_builder/ref10/ge_sub.c | 125 | `b1efea5ffb664ce1302099db84073cd959a4f9754f62ea73a1c58aac47e8f2df` | 0 |
| src/crypto/crypto_ops_builder/ref10/ge_sub.h | 2080 | `ee9a421a8a9778518748c93c1e9e7a08032601bfea0b5a7ecf266d1fc1b6a95d` | 0 |
| src/crypto/crypto_ops_builder/ref10/ge_tobytes.c | 225 | `6a54bfa8dbe907892fdb5b8f11581e3c6afaca1d9bf8f452ba9d6af3ea72ec6b` | 0 |
| src/crypto/crypto_ops_builder/ref10/keypair.c | 415 | `a2fdd7099b1a4aaa2deee29991b032b1d5dc9744dc87152b1a76d3783b5e602d` | 0 |
| src/crypto/crypto_ops_builder/ref10/open.c | 1036 | `9fd51699dde7bc7362c52fb98831b79b6355611fe21cfe132ff6ee4f3c9cecfc` | 0 |
| src/crypto/crypto_ops_builder/ref10/pow22523.h | 5518 | `32a9c7273c98fe428c7e1349f940e346960e84219b2d3c3cd0ada753e305fd86` | 0 |
| src/crypto/crypto_ops_builder/ref10/pow225521.h | 5527 | `7ab9170e5237fa676da2acd90cfe72a0357852114aeb937e210dc7dd6b9ff3df` | 0 |
| src/crypto/crypto_ops_builder/ref10/sc.h | 382 | `8ca4cb1ddc03571b62d668853f652b6116a8a93c439e32a529924bc0acc16c9d` | 0 |
| src/crypto/crypto_ops_builder/ref10/sc_muladd.c | 12494 | `5970a794d5e3691abee3514fe7a51c100bafcd1ef6053109a252ed7a6635194a` | 0 |
| src/crypto/crypto_ops_builder/ref10/sc_reduce.c | 8139 | `957ca57f09db9b46e6f25d530c2d913765893a7be36d34dfbcd3dc4524546299` | 0 |
| src/crypto/crypto_ops_builder/ref10/sign.c | 817 | `d71fce453b41ccd285fb4f9b8843e06e352b537be96519c595b438de9c840709` | 0 |
| src/crypto/crypto_ops_builder/ref10/sqrtm1.h | 87 | `eb5c2da31ae65159d3a2aa590dcac6594a384a731f918828c6e0d99fc1844b86` | 0 |
| src/crypto/crypto_ops_builder/ref10/sqrtm1.py | 563 | `fcfd6bd207bd9a0d34cef97bb6166691f720e8c52c6a48ed4e032edb26511c11` | 0 |
| src/crypto/crypto_ops_builder/ref10CommentedCombined/MakeCryptoOps.py | 9683 | `4d5cc2faa31dd389927ed392e52f203c33111973a53d2d70b4e6897ea4e1b9ec` | 0 |
| src/crypto/crypto_ops_builder/ref10CommentedCombined/api.h | 121 | `9d7cfd2c451dcf8ca38837dd602c8915ec246ed461a355c218a2bf9edd48ea6c` | 0 |
| src/crypto/crypto_ops_builder/ref10CommentedCombined/base.h | 76457 | `dac873e5965b34e29a14b56bc63f9434fbba16b3513daf53c7b0b2d07b614ac0` | 0 |
| src/crypto/crypto_ops_builder/ref10CommentedCombined/base.py | 1343 | `83148d97984e2812d79eddfb06942217db284a7ab6077d05e309e6fff66314af` | 0 |
| src/crypto/crypto_ops_builder/ref10CommentedCombined/base2.h | 2388 | `1dbe1b61a3b7689d840eec4be7569261d719e67cf9ed5ad1b51c5e34583bec94` | 0 |
| src/crypto/crypto_ops_builder/ref10CommentedCombined/base2.py | 1231 | `59566c7896508e4adcad02b37410703d10f5cac0726c60f3b81944809468022f` | 0 |
| src/crypto/crypto_ops_builder/ref10CommentedCombined/crypto-ops.h | 4188 | `d0cb06f9d36ae77217103dcce693f31e088101b616c617b42706cc76578abd55` | 0 |
| src/crypto/crypto_ops_builder/ref10CommentedCombined/d.h | 91 | `4729f3315d4815f5f3cb47d3f176ad0e907471aa3a9afc8d80484d2da98723a2` | 0 |
| src/crypto/crypto_ops_builder/ref10CommentedCombined/d.py | 565 | `6c9277207d8537153653f936d51e8fac47203e78d9c341e2bccb919619e7d440` | 0 |
| src/crypto/crypto_ops_builder/ref10CommentedCombined/d2.h | 90 | `0248fcb39acf255d78e0d19d6d605275a1939a7f61001f58f376569ecc0c5256` | 0 |
| src/crypto/crypto_ops_builder/ref10CommentedCombined/d2.py | 567 | `e3aff85dcca7c5706e8a94d045e3246f8786c834074edf1d3ee41bc983e10156` | 0 |
| src/crypto/crypto_ops_builder/ref10CommentedCombined/fe.h | 1939 | `37c8cf172c190b37134e6c9f9bf61f12c790126ecedc2abd6ecddffa71a4fd92` | 0 |
| src/crypto/crypto_ops_builder/ref10CommentedCombined/fe_0.c | 170 | `825fc6d85b392d15c9b26c26ad2ccfb664a1c09658d8e2d26c54e37ac6e8b509` | 0 |
| src/crypto/crypto_ops_builder/ref10CommentedCombined/fe_1.c | 170 | `a7ab32148848f7c44bc78b1e6d53c7bd633f629694b3b2dc075cc06d5eb17054` | 0 |
| src/crypto/crypto_ops_builder/ref10CommentedCombined/fe_add.c | 1255 | `f838729610a80bb3a988fdfe1a8a9e9ab01648006492adf1ff35b544a38cf398` | 0 |
| src/crypto/crypto_ops_builder/ref10CommentedCombined/fe_cmov.c | 1283 | `dc5f5993f3268ee20a333407e2d4b7a26a38ce1f8be7ce20b11c7d8f05efe03d` | 0 |
| src/crypto/crypto_ops_builder/ref10CommentedCombined/fe_copy.c | 454 | `0f91f42eac64053f508537fff726561d2e21cd88f5f7fa304f34f419545a9121` | 0 |
| src/crypto/crypto_ops_builder/ref10CommentedCombined/fe_frombytes.c | 2222 | `ae43a9b293d0950e4a87b5fdeaf59fbb9374aaa910f7aa295ee9e9521cec9a8a` | 0 |
| src/crypto/crypto_ops_builder/ref10CommentedCombined/fe_invert.c | 135 | `504b694c38ab523f9514164a6f19dfa2987e5561525e4ebb1964c33028b0a6fb` | 0 |
| src/crypto/crypto_ops_builder/ref10CommentedCombined/fe_isnegative.c | 266 | `c15116f89c80c6d393e6aa2e8ef6ad8b164e7b61f04bd208064f61e70f394697` | 0 |
| src/crypto/crypto_ops_builder/ref10CommentedCombined/fe_isnonzero.c | 315 | `d39c476ead289b2cb93d11588afe13f24ba824af81e45ee935930f4d02587443` | 0 |
| src/crypto/crypto_ops_builder/ref10CommentedCombined/fe_mul.c | 10744 | `77a67c16eebaa095e171caca018ceee1646a737eb314cebe72f05fff8a7d6b14` | 0 |
| src/crypto/crypto_ops_builder/ref10CommentedCombined/fe_neg.c | 855 | `3ce85c334bbe9fa2e7e231d2319ec3d29cd03781c7b3108570635348652732c5` | 0 |
| src/crypto/crypto_ops_builder/ref10CommentedCombined/fe_pow22523.c | 127 | `c6fca170f96ae1decbf89b9a0eef5e3973e3332fb064d8a39da20535148fdbc7` | 0 |
| src/crypto/crypto_ops_builder/ref10CommentedCombined/fe_sq.c | 5980 | `a35384fbebe43092b465a2abd12abbf2ae1b2f337a711688c5487c06ce0dc56e` | 0 |
| src/crypto/crypto_ops_builder/ref10CommentedCombined/fe_sq2.c | 6106 | `2abf4c6b3ed21ed8a805f2c0be1b9db4d88cdde9a0c710f24d070c5f2d01e076` | 0 |
| src/crypto/crypto_ops_builder/ref10CommentedCombined/fe_sub.c | 1255 | `1a2afa4c5fc5fcec3dfd1344dbb41ba3b1c93acea47f74b413216b9c8f374c11` | 0 |
| src/crypto/crypto_ops_builder/ref10CommentedCombined/fe_tobytes.c | 3189 | `678b10c1f49937ceccabddbaebe0982dea91a2620bdd81e29207178a959d97aa` | 0 |
| src/crypto/crypto_ops_builder/ref10CommentedCombined/ge.h | 2869 | `827267cd894408c3e10443a51c257ce5dfc93ad032eff178a101d12cc9d1ace7` | 0 |
| src/crypto/crypto_ops_builder/ref10CommentedCombined/ge_add.c | 125 | `cc236e58ad907a18671f2b5782ff9f4d2383a9848bc589b9fda83b3ecc55c05a` | 0 |
| src/crypto/crypto_ops_builder/ref10CommentedCombined/ge_add.h | 2080 | `ac78e776b39f2eb09cb6588bb86f34f3cf970f81d124136920bf8ba5c3e8b3b8` | 0 |
| src/crypto/crypto_ops_builder/ref10CommentedCombined/ge_double_scalarmult.c | 2371 | `225189d7203c85950c21a0a19120919bcc2cf91b50fa6c7453106321b362c463` | 0 |
| src/crypto/crypto_ops_builder/ref10CommentedCombined/ge_frombytes.c | 987 | `6e65ae1c056f1dc11da16b2bd4aabad151db3abcd5ab7fbfaca7e784c18496d1` | 0 |
| src/crypto/crypto_ops_builder/ref10CommentedCombined/ge_madd.c | 128 | `daf288d47d4d7356821912391ad2279a7ae5696a28bde7830b1660672ab5e6b4` | 0 |
| src/crypto/crypto_ops_builder/ref10CommentedCombined/ge_madd.h | 1900 | `a39615f652006291a3fb0299728243191937b98e0e91fc8bf8196f96075a8d60` | 0 |
| src/crypto/crypto_ops_builder/ref10CommentedCombined/ge_msub.c | 128 | `a7e060f539ad7a19428491fce2328ab2d5a6b5e1967a41e24bea8c80fe526a15` | 0 |
| src/crypto/crypto_ops_builder/ref10CommentedCombined/ge_msub.h | 1900 | `ee0e1ecc451b7b30ea9ba9c71035d371414ce26267ca94523b12877a01c84e82` | 0 |
| src/crypto/crypto_ops_builder/ref10CommentedCombined/ge_p1p1_to_p2.c | 165 | `be6e9b143c304c652534eea0fa9c92031005db7c83b824e7cf95581c093f9983` | 0 |
| src/crypto/crypto_ops_builder/ref10CommentedCombined/ge_p1p1_to_p3.c | 191 | `ce67bc193d4d9c81ff18532ab5c1e74ccf519e8349ed19ff112feb22df27a3d2` | 0 |
| src/crypto/crypto_ops_builder/ref10CommentedCombined/ge_p2_0.c | 86 | `1277df80612424d2eeb17e6700687b6fa24bfb5549f774c2112bc20fc39ebcfb` | 0 |
| src/crypto/crypto_ops_builder/ref10CommentedCombined/ge_p2_dbl.c | 112 | `3d6aba9a349542b8350c5bbc8f69252d463b14605ad65d35241e89812482e780` | 0 |
| src/crypto/crypto_ops_builder/ref10CommentedCombined/ge_p2_dbl.h | 1476 | `68aece7c0d6d99f8c6a91b4708d85336f060f9dfe171c1484097c4e380d1f884` | 0 |
| src/crypto/crypto_ops_builder/ref10CommentedCombined/ge_p3_0.c | 100 | `e11b72f763151ef2ce652a0bf7991673b01e6ce74f15e90fd4af28cde505a52b` | 0 |
| src/crypto/crypto_ops_builder/ref10CommentedCombined/ge_p3_dbl.c | 131 | `343ec8eddef9d91d130e3bbf443cdd64d226cd129530fede2126a837e31aab49` | 0 |
| src/crypto/crypto_ops_builder/ref10CommentedCombined/ge_p3_to_cached.c | 246 | `7fb03b81ba8d513990c3ed90128fcb8bbff1012d8a4e7573fb50a0c0c6af0fcf` | 0 |
| src/crypto/crypto_ops_builder/ref10CommentedCombined/ge_p3_to_p2.c | 149 | `1a29bfa686815c7c694d6cd2c660314f00e2bc53278478b7d8d51ede5133c34d` | 0 |
| src/crypto/crypto_ops_builder/ref10CommentedCombined/ge_p3_tobytes.c | 228 | `232f48e92a096e1a9c5c18ce2bc80583d42236740501bff7d57eb9b9cc6310f4` | 0 |
| src/crypto/crypto_ops_builder/ref10CommentedCombined/ge_precomp_0.c | 110 | `602db7879544d2084b3a6b21b33950b2b6974fabc36a8c867ad7207ac7a7b115` | 0 |
| src/crypto/crypto_ops_builder/ref10CommentedCombined/ge_scalarmult_base.c | 2477 | `08d424c208d9f52a0dce884720413dc37449bee2ea6997e0d1cc5061433ff445` | 0 |
| src/crypto/crypto_ops_builder/ref10CommentedCombined/ge_sub.c | 125 | `b1efea5ffb664ce1302099db84073cd959a4f9754f62ea73a1c58aac47e8f2df` | 0 |
| src/crypto/crypto_ops_builder/ref10CommentedCombined/ge_sub.h | 2080 | `ee9a421a8a9778518748c93c1e9e7a08032601bfea0b5a7ecf266d1fc1b6a95d` | 0 |
| src/crypto/crypto_ops_builder/ref10CommentedCombined/ge_tobytes.c | 225 | `6a54bfa8dbe907892fdb5b8f11581e3c6afaca1d9bf8f452ba9d6af3ea72ec6b` | 0 |
| src/crypto/crypto_ops_builder/ref10CommentedCombined/keypair.c | 415 | `a2fdd7099b1a4aaa2deee29991b032b1d5dc9744dc87152b1a76d3783b5e602d` | 0 |
| src/crypto/crypto_ops_builder/ref10CommentedCombined/open.c | 1036 | `9fd51699dde7bc7362c52fb98831b79b6355611fe21cfe132ff6ee4f3c9cecfc` | 0 |
| src/crypto/crypto_ops_builder/ref10CommentedCombined/pow22523.h | 5518 | `32a9c7273c98fe428c7e1349f940e346960e84219b2d3c3cd0ada753e305fd86` | 0 |
| src/crypto/crypto_ops_builder/ref10CommentedCombined/pow225521.h | 5527 | `7ab9170e5237fa676da2acd90cfe72a0357852114aeb937e210dc7dd6b9ff3df` | 0 |
| src/crypto/crypto_ops_builder/ref10CommentedCombined/sc.h | 382 | `8ca4cb1ddc03571b62d668853f652b6116a8a93c439e32a529924bc0acc16c9d` | 0 |
| src/crypto/crypto_ops_builder/ref10CommentedCombined/sc_muladd.c | 12494 | `5970a794d5e3691abee3514fe7a51c100bafcd1ef6053109a252ed7a6635194a` | 0 |
| src/crypto/crypto_ops_builder/ref10CommentedCombined/sc_reduce.c | 8139 | `957ca57f09db9b46e6f25d530c2d913765893a7be36d34dfbcd3dc4524546299` | 0 |
| src/crypto/crypto_ops_builder/ref10CommentedCombined/sc_sub.xmr.c | 16943 | `c0feab4474da4f2d5023d61c2b7c8973e54042e0d5fb9d32047b39c7d763050c` | 0 |
| src/crypto/crypto_ops_builder/ref10CommentedCombined/sign.c | 817 | `d71fce453b41ccd285fb4f9b8843e06e352b537be96519c595b438de9c840709` | 0 |
| src/crypto/crypto_ops_builder/ref10CommentedCombined/sqrtm1.h | 87 | `eb5c2da31ae65159d3a2aa590dcac6594a384a731f918828c6e0d99fc1844b86` | 0 |
| src/crypto/crypto_ops_builder/ref10CommentedCombined/sqrtm1.py | 563 | `fcfd6bd207bd9a0d34cef97bb6166691f720e8c52c6a48ed4e032edb26511c11` | 0 |
| src/crypto/crypto_ops_builder/ref10CommentedCombined/xmrSpecificOld.c | 22902 | `6a4ebfa9e017a1cfe125add6444f55aec1f5d1f152da21cda6dd02a02088927b` | 0 |
| src/crypto/crypto_ops_builder/sha512-blocks.c | 6437 | `6a651d1d0a5e3ee0af98fd180b750097f646913be3725bf2ff683f116f75e8e1` | 0 |
| src/crypto/crypto_ops_builder/sha512-hash.c | 1804 | `66d6e138a4ebb147d2581af487115bd3265cf81069ee5c7fb2d0307865930906` | 0 |
| src/crypto/crypto_ops_builder/sha512.h | 243 | `48a0f71abcada8dbc6f2fa7272c2d8cdbe6f1e871bfd4ed9d6b3d64f20906b04` | 0 |
| src/crypto/crypto_ops_builder/verify.c | 473 | `9cbbc9a8d5fd0599365d8cfde7f3f8b1c94fc80272a4a1e0bd38e0c31c2c7289` | 0 |
| src/crypto/duration.h | 3040 | `cfb2430d8c207c61b65200f02a38144e37cfcbffb1c523616cfee2508a384ea2` | 0 |
| src/crypto/generators.cpp | 14212 | `62520504016a2ee95c7b0dcbac93e4b39aac7b245e0b193b66e2f7fe2d5ef39b` | 0 |
| src/crypto/generators.h | 2133 | `f035faafe63a192dabe9cadef9ac125981cb1ad5e7a4eee4671c2a94986fa493` | 0 |
| src/crypto/generic-ops.h | 4018 | `d24614c94eb59017554b9349be8b3ee277388b3281979626aa09b72aa664460a` | 0 |
| src/crypto/groestl.c | 11960 | `542ccf2655689086d6369115b318deab977060e354d0d5d2aa8e8f1688c4bfb4` | 0 |
| src/crypto/groestl.h | 3103 | `464fbe8356ec602a2fbb3e3fbd034c5c9f7f453d4e71fb4134b8a0cedf54d703` | 0 |
| src/crypto/groestl_tables.h | 14083 | `e8e33e6f9b97f72e197b4dfdcd85289b5e93973e16cd66205646cedf4dfe5f4c` | 0 |
| src/crypto/hash-def.h | 1675 | `f09795fb08fa68acd88957b551bbbcd81c896b4ab319c9aad45a2f3b08b5f994` | 0 |
| src/crypto/hash-extra-blake.c | 1865 | `56fb87bbea92024e67bec636b59d92cad8ee9788e2ac6463d806f79ae4beb622` | 0 |
| src/crypto/hash-extra-groestl.c | 1885 | `6109ee3af549187f181334158875f629ee5936b887a1f0f3d6cfb080e7d34859` | 0 |
| src/crypto/hash-extra-jh.c | 2070 | `8c5ccd706c6cfab5ffb570673b11c47ed9c11080141f2a2bd6a17c406cc6ef18` | 0 |
| src/crypto/hash-extra-skein.c | 2048 | `4d104ea4a63736a3cb595164eeaa3b3a017a7176e9a96959fad56f5adba78c6e` | 0 |
| src/crypto/hash-ops.h | 4481 | `6340b58874b4645cc90d6cf97f87c157b8c8605421aafebcb8fd0bfc7424920a` | 0 |
| src/crypto/hash.c | 2338 | `56a62dc76510b7d9c5e4fd4f7fdcf09aa86a68d0e0e98b002bb8ab22277f112c` | 0 |
| src/crypto/hash.cpp | 3957 | `3214ca89b4b885357294958b18d0d78d9e223df56358b651f3492475522ead72` | 0 |
| src/crypto/hash.h | 3121 | `89fee28ecd6b8c7d71ad3df58e28205551fb2709ae7dc1a98a5af961d581688b` | 0 |
| src/crypto/hmac-keccak.c | 2989 | `e67a1afa52bab3adef2a6a0d8c3bb99c558d3e94f23748b114c7543efb710e99` | 0 |
| src/crypto/hmac-keccak.h | 2356 | `e2fc2dd3a89cbd454b98b45cff6432dba19138774dbc1e6bdcb56260b07ea11a` | 0 |
| src/crypto/initializer.h | 2768 | `735dca21f7181d4be1fb08450297ec264f904d55137298990e20b634bc362801` | 0 |
| src/crypto/jh.c | 25452 | `f6c6b6983e67da79371d195e857e8f3c9f419ca84c5b77063862ce6222a04073` | 0 |
| src/crypto/jh.h | 828 | `ca4f3570ce36a46bdc24e749ad1d60f9216ee708076d61fd9f1a1ed336626178` | 0 |
| src/crypto/keccak.c | 6738 | `56aec12b01d0b85dfff97f8d32e9dbe1bdf4f5cc76a4a97a93af73aa05c98b39` | 0 |
| src/crypto/keccak.h | 993 | `dde2bdb591a893b8ca5890b7e3d5be906812d4b3977e9006b5434e1cf35d3be7` | 0 |
| src/crypto/oaes_lib.c | 8292 | `e81aea08da377b8831ce937ee2c18c5a1fb423c566caef0f608b6d717a1fbef5` | 0 |
| src/crypto/oaes_lib.h | 3397 | `1aff1cfc2bd5102e518827247b21c2c07666c2f24b5dce11cb34a7a7c50fb99c` | 0 |
| src/crypto/random.c | 6281 | `a600a0a54df08eff9be89335daea5299d961fa43dc024c488eceb5a610ec93c6` | 0 |
| src/crypto/random.h | 2070 | `cfcb0a4b9dc5472dbadb1f018e50e72b25c5ed1007c8dc293de0b7aade440e16` | 0 |
| src/crypto/rx-slow-hash.c | 15956 | `1e8ecab05829bd0e2607c5d677629c3e9d4908f8e7754baf0a37dabfdc2af427` | 0 |
| src/crypto/skein.c | 84748 | `96bdda389bcb9b87811f52c33b74840bd38f4900f8dc163ed358704e32a805c2` | 0 |
| src/crypto/skein.h | 1910 | `9f1d7fd31d8d9776974af1e33441da6caa33a3e08c0ad5b86e5f1215af7a2fec` | 0 |
| src/crypto/skein_port.h | 8334 | `741a2fda82c22b29865ebe1c640e65a48d5c4935a8f8ec16f68eccc379ef79d2` | 0 |
| src/crypto/slow-hash.c | 57460 | `886ae10164b0593e35df7419cd5834ce66a6db5a5f54a623a5364804f868fd83` | 0 |
| src/crypto/tree-hash.c | 8235 | `1869b24e5cf1f9c36b23d743d251ddbcd6227f5d1c781cb60f800cb1e0ce5cb1` | 0 |
| src/crypto/variant2_int_sqrt.h | 7769 | `680314b217892f7ef62d30386a69854ceb607cfd1d4d946fdbe5344259f156cf` | 0 |
| src/crypto/variant4_random_math.h | 13674 | `52423d93368918c7dc17d793ad5c1d9c3f152a03849b43d2182bf0a6eba92448` | 0 |
| src/crypto/wallet/crypto.h | 2547 | `020a41b52135f2ce48977ea7077354f182f3748819f348bb8c965b73394db99a` | 0 |
| src/crypto/wire.h | 1883 | `a1748e10504d14cb6202f86b048016e518752ca96b81ca61bb4fc3b4827222d8` | 0 |
| src/crypto/x25519.cpp | 4237 | `aa9696357248dfaa733e4a512a1c6b4eff6c6e9cd4787ec7914f13cd7d3a78f9` | 0 |
| src/crypto/x25519.h | 3330 | `752f814403b6ac65e071b794c670ff4c1befe28f6f1a4072f2205bab3ef06483` | 0 |
| src/cryptonote_basic/account.cpp | 13581 | `bc0220f0efe219365058dd9771060c44cf6571521fb906eacfe89e749572df07` | 0 |
| src/cryptonote_basic/account.h | 7943 | `d9d5dc7dbb2ce3ada4a72c70e2e0de982f77adbdf5a828a0f55c6bf487b83355` | 0 |
| src/cryptonote_basic/account_boost_serialization.h | 2294 | `9e407789747d9be7f9fbd6ec6ed61e92edf6e682cb2f749aad892a33d9037091` | 0 |
| src/cryptonote_basic/blobdatatype.h | 1877 | `c1924f5ad550f030970046354d3ba7a85e909da013f1c6abe6467d144492f0e7` | 0 |
| src/cryptonote_basic/connection_context.cpp | 3938 | `52b3b29894003d821229e60b4197304fa1a6513f4809020a91eb5c4cadf078f6` | 0 |
| src/cryptonote_basic/connection_context.h | 6139 | `da57dcfc2429ccaedc22849dd5897f05fc591f3066ab891e6421ce45fde11939` | 0 |
| src/cryptonote_basic/cryptonote_basic.h | 23702 | `204962967bb9f093b577b3ba014d9d742ec9a706137b16e20128e44b1102745c` | 0 |
| src/cryptonote_basic/cryptonote_basic_impl.cpp | 12627 | `9ad62ed4650dbdc338826869f0a42e7bdf1d74c153059d1d55e47b99ac5b7366` | 0 |
| src/cryptonote_basic/cryptonote_basic_impl.h | 6531 | `d38a12c2b89d894b9fd8349d62c1145c83fcc160dd8076f3014a3f206b9f1d7c` | 0 |
| src/cryptonote_basic/cryptonote_boost_serialization.h | 12987 | `5f284bf26ed20e1134d62929734111e25a3867e2e40f3acdd1ce77b7b273e0ba` | 0 |
| src/cryptonote_basic/cryptonote_format_utils.cpp | 75265 | `065a550a474b7eb3bd3a3a5e08c190294883c0e84496336e15d4d86edf67c9a7` | 0 |
| src/cryptonote_basic/cryptonote_format_utils.h | 16704 | `6b3be1845d396921c65ff3e13e83f860c3991fb2d07884bd4b8bb1ae4e9e3d9e` | 0 |
| src/cryptonote_basic/cryptonote_format_utils_basic.cpp | 2195 | `ef8ad44714feff9ab34babe75c982448820fee8f807f4b39f7207eb2c93dab1b` | 0 |
| src/cryptonote_basic/difficulty.cpp | 9281 | `96f4776d7b624f952df85220630100e57de469f40b5ff4af15ed56489d0e465c` | 0 |
| src/cryptonote_basic/difficulty.h | 2910 | `c5f1674bf6ed674c3682259628a2c81e87e8b9150198bd443691feba14772965` | 0 |
| src/cryptonote_basic/events.h | 2153 | `d4880274f21fa3a2845818056230fda5ae47c6e3b81e801aa4695b0512e8bede` | 0 |
| src/cryptonote_basic/fwd.h | 1727 | `2d23b2b8da870c54d4db7f305a5bc9b8ccc65a867e826848295eaa7c2944f3ce` | 0 |
| src/cryptonote_basic/hardfork.cpp | 12424 | `67e76b5140de6b799b1479e4dcd917bb906e0a8e49dbee8fa14e6880c3291b94` | 0 |
| src/cryptonote_basic/hardfork.h | 9987 | `e28a84dc295baacd4cbc4f1dfaf597065058afc34fe1683283a5e8c72c9f1229` | 0 |
| src/cryptonote_basic/merge_mining.cpp | 3385 | `537857dc323d1debc7a7bcea0cbb4e21d4c7438b9485d1f8675f53b6a48bd823` | 0 |
| src/cryptonote_basic/merge_mining.h | 1915 | `919bbc1eda13d8f329233e9b22d5160ca2facb746b32a60bd59efa939943c186` | 0 |
| src/cryptonote_basic/miner.cpp | 45038 | `467207ed6b4b1dc693cab2a81fdbeda8a7cb120c515ee885ed012b8790a67682` | 0 |
| src/cryptonote_basic/miner.h | 8222 | `9cac6b0a6329e48ffbf9e969c76a435430555ff4fd288726375d6e98364efbbe` | 0 |
| src/cryptonote_basic/subaddress_index.h | 3393 | `e155a9aa113048064186d8cd52a9c04ccc749e2565b93ec700b65f1f86971208` | 0 |
| src/cryptonote_basic/tx_extra.h | 6059 | `ae91d15d11be1ac887ecd658ca9a2c78d4d5ccb1d072e24b31ab6268efd97e68` | 0 |
| src/cryptonote_basic/verification_context.h | 3521 | `e81b2a8d69421e19d43b1905601563e13bb7f13fade10fd3f222f42cd460c054` | 0 |
| src/cryptonote_config.h | 19904 | `61d6d6a85ad582ac87aa22011e25417dc437871f460e90adec5697eff17224fc` | 0 |
| src/cryptonote_core/blockchain.cpp | 216305 | `23ad915e0df0e46bb0ae614076e4095edb513b6e325f44152716abe15d9b542f` | 0 |
| src/cryptonote_core/blockchain.h | 70469 | `768071da3a2c8e8a55d9630ed84d236054b610da4d50a4dfc459107fa413ed57` | 0 |
| src/cryptonote_core/blockchain_and_pool.h | 2399 | `e9231c8881f356315f9a1d20eabb64525083468771422a72fb25883bb822d9ef` | 0 |
| src/cryptonote_core/cryptonote_core.cpp | 79945 | `21098bf0ef9e97e85af2da82af446352f6d2ebc9e3e08f77d92e49b7c79c906d` | 0 |
| src/cryptonote_core/cryptonote_core.h | 40658 | `0db747916552178b45bd42afeb0fa141c7af7b9882b023b1bc31e38d0da9da9b` | 0 |
| src/cryptonote_core/cryptonote_tx_utils.cpp | 32529 | `8e5bef1af8b1dc4d9c1c20bdbb3d794956a015fc4f40204913815297a09190f6` | 0 |
| src/cryptonote_core/cryptonote_tx_utils.h | 9935 | `03dc4e38355d5cd5a7dccc92fc427483169fcae4c6357de025c26116c8924b34` | 0 |
| src/cryptonote_core/i_core_events.h | 2032 | `7604bb4c8bfecf6d660950177851b203f93414f6c5b9c4ff14174e8731112058` | 0 |
| src/cryptonote_core/tx_pool.cpp | 81184 | `df1ffcaf62938ac348c940e632e82440fc0c402c9434913c0c1b65e9949c6df6` | 0 |
| src/cryptonote_core/tx_pool.h | 27949 | `b5ecd519b2885f9c5639168023009f26c5a832fd7532469c48bbef14409c08a7` | 0 |
| src/cryptonote_core/tx_sanity_check.cpp | 3764 | `0f9ac93798074919e4185ecee1ce7fba5215a4ac634f57d750758625131f592d` | 0 |
| src/cryptonote_core/tx_sanity_check.h | 1876 | `e18a475346ca5c3e028c549f0b6f446a71102d9c5b800ead24a0191f482128e6` | 0 |
| src/cryptonote_core/tx_verification_utils.cpp | 19093 | `7ef9f66ffff4ef0da57814c87ed2da241b3c88bd94842d01a60e7f78eec11a8d` | 0 |
| src/cryptonote_core/tx_verification_utils.h | 7508 | `4ce264c92b4477f3f06d1553a27ebe8297a11a14e251b6d5adcffd012ae288a4` | 0 |
| src/cryptonote_protocol/block_entry_utils.h | 6026 | `fabd51964c431ee5ca92b21e5cb96c8dbd8919d64c2fa893f7f376187977c9db` | 0 |
| src/cryptonote_protocol/block_queue.cpp | 18400 | `71c884b4dfe5c58c651d52ac0feb45523754aa518b2fffab3711e8f52910b4b9` | 0 |
| src/cryptonote_protocol/block_queue.h | 6522 | `68f509fc085855cb156e1aa81f2e0f824e16a900e1387b3df4f9b923866f948d` | 0 |
| src/cryptonote_protocol/cryptonote_protocol_defs.h | 11991 | `4459e0d2186d3d16ed7d70d3291f6612cd92f1f37774cf9a24decf9fba0b6b9f` | 0 |
| src/cryptonote_protocol/cryptonote_protocol_handler-base.cpp | 5183 | `8e4d2a5aaf4f837ddd53ea4920939be76494828b61bb46809c983a6975d9c5d6` | 0 |
| src/cryptonote_protocol/cryptonote_protocol_handler.h | 12513 | `d3004caf4394207bde153782668053d22c833d5ee20ae7e187e8ad5395304d01` | 0 |
| src/cryptonote_protocol/cryptonote_protocol_handler_common.h | 3360 | `ac282102baff1b289cb56f1157d607ef91d45e235926e4ece931889861edcd69` | 0 |
| src/cryptonote_protocol/enums.h | 2176 | `1ed7d02504dc98b9f291071cde570f4953294710baa930fb8be201ef60272b49` | 0 |
| src/cryptonote_protocol/fwd.h | 1704 | `aa1e77275411e986363a96a62ad789f248b3449763a0c78514bb541cc4b7812d` | 0 |
| src/cryptonote_protocol/levin_notify.cpp | 35623 | `18e10ce8b9b512bf4a244327d8a8bc98c830eb48736c186e0c3014c8c77e47dd` | 0 |
| src/cryptonote_protocol/levin_notify.h | 4879 | `d833a6870a9d14389d5c4bb1e5f3fda9331a7c086060e1cc295a7c170bf57eca` | 0 |
| src/daemon/command_line_args.h | 6299 | `80b157c96eb7d7d526404c448c1f5e325faf374795fc6e22051d1f213c1141ce` | 0 |
| src/daemon/command_parser_executor.cpp | 31960 | `451a849f130ed6776801a9ef5061c4152a606375984a5c729348d2ae711c1914` | 0 |
| src/daemon/command_parser_executor.h | 5200 | `b1eece0b4902f79065483aa4a71e06b2a4fedc05fd549b5624a303b665573aa1` | 0 |
| src/daemon/command_server.cpp | 15651 | `afb861a09efe150dbee664fe7840d7bbb1c0a8aa845a7b5f5be8a2415109a290` | 0 |
| src/daemon/command_server.h | 2733 | `155a4b80d9fb8da517ac1de41f83c870eb1186f61b0a17956b34cbf8d1468f25` | 0 |
| src/daemon/core.h | 3941 | `43ce7f59d00e5067186dacd521e85d844cef81a462987ee3e183132ce9376905` | 0 |
| src/daemon/daemon.cpp | 12131 | `e4ac6c5273b1e56e0269cc1002df6fc79726300a4a4e2846feebf2ccbf1a6925` | 0 |
| src/daemon/daemon.h | 2262 | `b4a843b991536194f4126feb6668a6f71cea6b11ffcf2790ec65912f2abb49e5` | 0 |
| src/daemon/executor.cpp | 2695 | `dbadf166b9642c7c0c291d0ad649a1e0c6c6e288626a75ee187ebf61274d3dcc` | 0 |
| src/daemon/executor.h | 2557 | `10eca95089cffc28bf3a0d12629994a0e9496495dcdbe5dcecefa6fc8389d857` | 0 |
| src/daemon/main.cpp | 14632 | `e03b76b68743cbf45ac4556776088a6bb0bf34867026a8278b0c571688d4a94a` | 0 |
| src/daemon/p2p.h | 3194 | `c89da42f7e346582845cc34003ab6e879552c69e2ec85f88e81cd920b2f74748` | 0 |
| src/daemon/protocol.h | 2993 | `83e3026ace1589e223c16ef99fbfb5b12843b64e4efff14fcab89d843dcfcc7f` | 0 |
| src/daemon/rpc.h | 3606 | `13092e9c708e74b0fc4a01a3ddc5e370c7a94499f5f851eca5c4196257d788bf` | 0 |
| src/daemon/rpc_command_executor.cpp | 81552 | `123748c3026078d8030887a697640d49ed124fc8f6f319dac46af38954877cde` | 0 |
| src/daemon/rpc_command_executor.h | 4959 | `510b1e255dec37b63608ef629b65c416d188d81b19e9ceec36f97557a300c205` | 0 |
| src/daemonizer/daemonizer.h | 2888 | `a7a8f317f5cc7ac23a16154c11e136e8c6c27973972598f1ac38b83b9a5b790c` | 0 |
| src/daemonizer/posix_fork.cpp | 4955 | `b31b452441c3222219f179abdf0985136cb18cff35a0a090c5a937bb034f2539` | 0 |
| src/daemonizer/posix_fork.h | 1703 | `5af6e0a3922c65baef730c2e2b148f6c2fdb58bab30d21b1cebfccbeeed0edd7` | 0 |
| src/daemonizer/windows_service.cpp | 8747 | `c866149846c9a36d6ef359ddec3f2c3dd0fbebbf4aeb7f85e78bccc5c02de418` | 0 |
| src/daemonizer/windows_service.h | 2138 | `8ba0b57e991bf896851459efc39ddbfca8ac43764ac4a18ef2f96c3460109ae8` | 0 |
| src/daemonizer/windows_service_runner.h | 5199 | `ffcccc98a2c47cf1db69d76341d8002d9eb59c606d16bdf58e97267a6f3a6ef4` | 0 |
| src/debug_utilities/cn_deserialize.cpp | 7653 | `ce2a7fbbf26f426f512e310f096998b27855cd9b233324630052d86c1b913718` | 0 |
| src/debug_utilities/dns_checks.cpp | 5527 | `ce18f66bd59d07280694b75b877eb4abf073cb5b0dbae30489ab791f8f2e0f15` | 0 |
| src/debug_utilities/object_sizes.cpp | 4337 | `7bceb8a710b12782a5402f1dab4ef3293c716cc09ede6385020e00366470f26e` | 0 |
| src/device/device.cpp | 4122 | `4b26053f49c5f63c49e9a9aa63ec0c3e96152164e72ddde6079f6af2bc0ca032` | 0 |
| src/device/device.hpp | 14868 | `ceb92cdf2fa18db1839a9599bcd089ff400fa1e0a28ba261629fc9c232c9fff0` | 0 |
| src/device/device_cold.hpp | 6499 | `687982f119dd95475e765ed866b08fd93e3bcf1e81e31e640688a5df8d525675` | 0 |
| src/device/device_default.cpp | 22758 | `b01708afb69af47cd85de6ed0c1125005920bb7b060bb736ef7932f7a7fd184f` | 0 |
| src/device/device_default.hpp | 10608 | `f4680e7f86ea2ebf3aba361760105d68f39be2045279110b4493237a73cf081b` | 0 |
| src/device/device_io.hpp | 2100 | `04e13668eadbc57e51736a94ac7ddc125777b134ccdbc545abf464c2eb5c85d1` | 0 |
| src/device/device_io_hid.cpp | 13867 | `5f66c743b1edc5bec3acc6f60686c47126d5b13b82c212a055674f713b054c75` | 0 |
| src/device/device_io_hid.hpp | 4193 | `56b98eee55009fbe3e61efe3847593ff6f7031cedb2d20c96d6dbad481b4b8c6` | 0 |
| src/device/device_ledger.cpp | 95324 | `e9be6b96becd58617dc99a8ab3996174a59303bfb431f44fc3a6aa8e0c7a9089` | 0 |
| src/device/device_ledger.hpp | 16651 | `4540240c76aefc04267af721a3227b43c347d310186cb1027a1e7c530bc8da72` | 0 |
| src/device/log.cpp | 5787 | `d5a58ef9ec6c318bebafa3d76fbaaf9bba43cc036e47d4c62b29145a105af034` | 0 |
| src/device/log.hpp | 3803 | `a33cb58b12101b78b1c07f85352ed52b78075e4f5dd7888c9cc99ec93127824b` | 0 |
| src/device_trezor/device_trezor.cpp | 30321 | `a3284befdac91e9bb837475888aab9d3d47fa684a59777e4e2f420061fe72a69` | 0 |
| src/device_trezor/device_trezor.hpp | 9128 | `70c9dda60b84e55becb5111c900dced7f94d4ca3d30a43ab223335ef002ed83d` | 0 |
| src/device_trezor/device_trezor_base.cpp | 20027 | `70484771a0f9da8a52a111f70dccfa9f84b8be564f94a380c14e0542e0052f71` | 0 |
| src/device_trezor/device_trezor_base.hpp | 12846 | `df347e26bbe4130b99ba4ca36459fa751b8f06fb76978c6c9d90403e84c0ea4c` | 0 |
| src/device_trezor/trezor/debug_link.cpp | 3123 | `1517dca749b900495fe00be101c6246fafdcfd1fbd9731b437f67d5c7a5c645c` | 0 |
| src/device_trezor/trezor/debug_link.hpp | 3461 | `b0b35f56d320b19547e271e0889f7dbbd1d893835e7af05a469075dca0a14e1c` | 0 |
| src/device_trezor/trezor/exceptions.hpp | 7206 | `941f49d6f71b0c7e2183bfa416cb86d7fdf8541fb72ccc398ea01724efcc9f0d` | 0 |
| src/device_trezor/trezor/messages_map.cpp | 5399 | `82f0a9e90f76baf7eea73a056faff80931d6b3cbca757e9f800e0cc9369e5691` | 0 |
| src/device_trezor/trezor/messages_map.hpp | 3921 | `a2d63ae5bf68cbf4579e8a7e27c009ab22633b63c9151a1e20ad310f8b31a0f9` | 0 |
| src/device_trezor/trezor/protob/messages-common.proto | 6918 | `cff96d8dc8c6e3943afc8d14ac3e0aaaf2b609d387766bc5f889f7ab861be24d` | 0 |
| src/device_trezor/trezor/protob/messages-debug.proto | 10196 | `b4226439d34ea46d6b706a7d2f010f6f10c92d83db93743bac3039a41ae64d17` | 0 |
| src/device_trezor/trezor/protob/messages-management.proto | 30030 | `81391eedb4a960a5332e5f3d40b1f316ac635ebb0e471f8e6d4233d5a670d6aa` | 0 |
| src/device_trezor/trezor/protob/messages-monero.proto | 15967 | `b5b5d9b971f5834db8b41901cf6e89fcfa491e6ac3e8bc26287465b8881ee4d2` | 0 |
| src/device_trezor/trezor/protob/messages.proto | 24596 | `60d5a9fe9fc43f3c131beb51f677b78037830cc2860bcd288b4db031cb671dd8` | 0 |
| src/device_trezor/trezor/protob/options.proto | 3772 | `91cdd9232d1e08fef809b9814e33ab07a5a0e4885ea10ee71a1f9785106d27a7` | 0 |
| src/device_trezor/trezor/protocol.cpp | 44357 | `208d62420b9807b1f6031655fc422468a2c306e1523276a27ee7c216ad559b19` | 0 |
| src/device_trezor/trezor/protocol.hpp | 14674 | `f06aaedb3060f23e0a937e0b8d051f8544046e7228337bf4700eefd28a5f919e` | 0 |
| src/device_trezor/trezor/transport.cpp | 41677 | `d15b58f2d40646c9a6a8222cd6da75dc38304be0faff784307783511f13d8709` | 0 |
| src/device_trezor/trezor/transport.hpp | 14295 | `bda32b96a4853236b1dde3a36a41fc2a12eaa7473d406c2ccd4dc3edec2ee6c0` | 0 |
| src/device_trezor/trezor/trezor_defs.hpp | 2711 | `bb3cfb5dca576a61c599d5498e6caab1ef96b114f5ff9b5a7305e2aec4fef2dd` | 0 |
| src/device_trezor/trezor.hpp | 1990 | `aa0be0f4131eb22e9201a899db73253851d0b1e26bfeb2d5e1d661ef2072230c` | 0 |
| src/fcmp_pp/curve_trees.cpp | 49581 | `481bbba5852dfe401c5ae5146e5e12881d276fcf7f91f3fb7f3c1cc52fddc11c` | 0 |
| src/fcmp_pp/curve_trees.h | 10640 | `4cd9e819ed3917feb9a33ef416223bb7e68a6539f2e5c9d46a4b9daf162b849f` | 0 |
| src/fcmp_pp/fcmp_pp_crypto.cpp | 4714 | `75bf9d17c712e5ff6238745c0ca66723d0f2b2084afdac4fabc129a2aef97c34` | 0 |
| src/fcmp_pp/fcmp_pp_crypto.h | 4276 | `a9d1ef69e8ff60c018c25791ce1e27ecbd3573489827d0f23ddd1d99f3e31132` | 0 |
| src/fcmp_pp/fcmp_pp_rust/Cargo.lock | 20760 | `b69c300c2ce402e4050ef2a7015a852cb584bf55060af2722bd6b107a300be5a` | 0 |
| src/fcmp_pp/fcmp_pp_rust/Cargo.toml | 1224 | `92b9f088f56eaf892c4bec7fcc387d3fb3a33624254989105e3a0481e8374703` | 0 |
| src/fcmp_pp/fcmp_pp_rust/fcmp++.h | 6477 | `54796b3106fef176fe83cff2a26bbd1aca64e7b40ebe32c5024ae0bc9399d3d0` | 0 |
| src/fcmp_pp/fcmp_pp_rust/src/lib.rs | 7054 | `c716dc4002996f66097051550f143ccc1805aac29ed8f36af769565e978af0ac` | 0 |
| src/fcmp_pp/fcmp_pp_types.cpp | 4921 | `316e306c4c59294d1afafaa56384779bddfadd250eddc2e650f1cff31d2c9ffa` | 0 |
| src/fcmp_pp/fcmp_pp_types.h | 7831 | `b74e86f5dd23fa696158b071c0a9395b6bdd67c26923fceaf52ad63468555252` | 0 |
| src/fcmp_pp/ffi_api_c_compat.c | 46 | `bdfe5cf8538074b03e4577bcbf357106195c04dd0430766d7ce0f7c03c9a0caf` | 0 |
| src/fcmp_pp/tower_cycle.cpp | 8817 | `1cfb35096882577b273c9c3a22b18f36f72f94227bc9ceae595bfc6a2e6454d2` | 0 |
| src/fcmp_pp/tower_cycle.h | 5976 | `bf021c24bfee6238902561814fe775aa0daa7f9eebd1336c64e867850a71964e` | 0 |
| src/gen_multisig/gen_multisig.cpp | 9435 | `9c53df5c2003ca158cba7d8c2296c7e235d4919f7a6b35f8f26800b7f43ecd84` | 0 |
| src/gen_ssl_cert/gen_ssl_cert.cpp | 9041 | `08c54d396e000b26e47d25fcee42a0441fb57b192a3560fc08b9f0b307567eb0` | 0 |
| src/hardforks/hardforks.cpp | 5804 | `919ce96a538abc81e2af0971a38765c4d4f2be64b5bdd00e3868fdb8ece72182` | 0 |
| src/hardforks/hardforks.h | 2273 | `a75869264df3a069f9f0391b1827da70411f9edf052557bce29d1cec39633520` | 0 |
| src/lmdb/database.cpp | 5839 | `18a7c471dc7fcba5c2b4480dbf809e2395e37c9c03daa7b28012b838ba261a16` | 0 |
| src/lmdb/database.h | 5006 | `a1aef2ee4e3e46a3c9da582dc11fbdeb1dc09b52499fed4345f6c0bc8eedcc6d` | 0 |
| src/lmdb/error.cpp | 3812 | `364cc360f8e673a18e9857109c90780e33f467101cdb5d4ea45b34d483edd6b8` | 0 |
| src/lmdb/error.h | 2494 | `1a00589f4a11055a1963ffd19d426c6bb82cce352156b271ff973f764d40a30b` | 0 |
| src/lmdb/key_stream.h | 9725 | `7000b76657e6a5dcc2106c457c710b9d744acf8a4f311ad0e6ae24a661bfe6e8` | 0 |
| src/lmdb/table.cpp | 2110 | `8c3ecbd7e101b3dc629b896ba4c655c894d9c2137a8214b0813aa816d4c6fe56` | 0 |
| src/lmdb/table.h | 4182 | `79b3a675ddf9a3f433189dd62ee2d0516859f079b9261c545f34181bec847dc9` | 0 |
| src/lmdb/transaction.h | 3471 | `6af112d7e57063a2354853c3ba1e69f20b5bdde0610b28d69b499be48e2d93f4` | 0 |
| src/lmdb/util.h | 6252 | `99a8b89464ad04b7a49e500509a9b2af976f2734baac7f4a5784bb55d8afe415` | 0 |
| src/lmdb/value_stream.cpp | 2993 | `003f3c6b1f3a3658192bacb1f29760ec503358757007b24fb6196ec0b4da54e6` | 0 |
| src/lmdb/value_stream.h | 11217 | `ba0f1e108df3068be7730839d006623babb47e101250ccab7b08e379ba76dbde` | 0 |
| src/mnemonics/chinese_simplified.h | 26291 | `4a38fbe7279616aa78aa11dbcf425d0ba5305fd2089cb4421d544f2c540d50fd` | 0 |
| src/mnemonics/dutch.h | 34414 | `775d05f737f453d6798876d99961bb3bcfc49d47cb57860d3c0b2a03b9a64822` | 0 |
| src/mnemonics/electrum-words.cpp | 25437 | `41b2b72db444e4893c6abd6dac9a34d54c929e2b9394988ec22d758146625163` | 0 |
| src/mnemonics/electrum-words.h | 8880 | `eff1c41ae6935091ee40b57bd3044b053e8700ffe0b1a049926a90981c591020` | 0 |
| src/mnemonics/english.h | 33172 | `9bd756d29e689aae0e6e7f8b1196c4f35df350225c4668d4f6f41842f05fc2ca` | 0 |
| src/mnemonics/english_old.h | 32389 | `20c9090994c5b441f2e550cddbf266d604b64e495d9b172e45a8031e1aa5d578` | 0 |
| src/mnemonics/esperanto.h | 30916 | `382d9f9bfcf293e4dc9f156042fe5a3f2a151191bae368a494eaf53c77e16043` | 0 |
| src/mnemonics/french.h | 30898 | `f4e42ab4eb9824a2cd829f132e33dfc46ae31c5788a37c9726d393e7cc809a82` | 0 |
| src/mnemonics/german.h | 34100 | `7b910a96bc94d19eb3e4edd8179db383a68b03a7608396bbee0fdc46a7d4e88e` | 0 |
| src/mnemonics/italian.h | 34533 | `d02956b528db827646a1f6f78c1a19716b9334985cb893eb09409834a04045db` | 0 |
| src/mnemonics/japanese.h | 42380 | `3701f067006b60e95e266e7a385b472c5bddeb6f476e737eed6d3b7febefe6d5` | 0 |
| src/mnemonics/language_base.h | 7885 | `2bc256f01c6904af914cb7c6526254267ed463882e216fd0eb1d9bbdf4bf5bb4` | 0 |
| src/mnemonics/lojban.h | 28601 | `6c84dedd2609060f30368b92b5e377207e28afcda5401b5060d57c633e623a04` | 0 |
| src/mnemonics/polyseed/pbkdf2.c | 3257 | `f03848974bafc867280a7f8d25551b0832c61993b71d6f78bc8a178a73f41557` | 0 |
| src/mnemonics/polyseed/pbkdf2.h | 1748 | `6d3ab3e361a1a868b9dc84d8aca1be1c067f8fab2b507f65411c4fcb8420fb97` | 0 |
| src/mnemonics/polyseed/polyseed.cpp | 11144 | `314b882bc71f3862021c6261f90cfffb457217cff71ae87244e1558a8778dd03` | 0 |
| src/mnemonics/polyseed/polyseed.hpp | 4641 | `2a7332bf708f96b3d0d202a29d1c79caa65e99b7a832bdede62c58a53ab57748` | 0 |
| src/mnemonics/portuguese.h | 36110 | `0a6b191930a29f1ae827c1f5f8905548035bac5e5b41386f0978cf39e4adcfa1` | 0 |
| src/mnemonics/russian.h | 42516 | `2d3f282d11e917fcdd6248b87002f5b982b6abaa773e9676d21886b6a50a4762` | 0 |
| src/mnemonics/singleton.h | 2277 | `f540c185cd745a39e6780916163e3710ea20e8e97569e842b5b15e80adfb2256` | 0 |
| src/mnemonics/spanish.h | 33863 | `994a941260f53e066753204f4b92c20bb1d830b58e76ff89c2caa71c34d546ef` | 0 |
| src/multisig/multisig.cpp | 6813 | `8945675dc70155c253622cb497b32094da82790c725f4cd283ba48d3376fad50` | 0 |
| src/multisig/multisig.h | 3375 | `f0a8feffa4fd4e211b2804cc4ca1375d28ce31f56389f31093b7ad49a1b74d40` | 0 |
| src/multisig/multisig_account.cpp | 11230 | `8b7e6a0ecd4286d79873e8e6f0d5a994d75deaef3e1665c6ac3c9c274a14eead` | 0 |
| src/multisig/multisig_account.h | 16041 | `1f1c17870645d04ff57edc7b6f63c9cbf00d1322356fb37e8e8ec1e13443356f` | 0 |
| src/multisig/multisig_account_kex_impl.cpp | 47621 | `427206dd22bff7c9575b99c0ebb87f51b3cd734baec11182bd9b44bbc6b3eb3f` | 0 |
| src/multisig/multisig_clsag_context.cpp | 10109 | `9102b7d879bf7509300576470235dff5f876fefd967df2d9f8733565b84cc3cc` | 0 |
| src/multisig/multisig_clsag_context.h | 5567 | `93409100d656e65a685419273e2b349571b7e0a9c058a09e88d647cf942f14aa` | 0 |
| src/multisig/multisig_kex_msg.cpp | 12502 | `9b7e993aeb21688019500f8c5cbe06f2339a811cbfa9b9a67a3a014276a5bf80` | 0 |
| src/multisig/multisig_kex_msg.h | 4168 | `e083328e759d04437e637f685dcead17f1908f502242b2ff95b43e942e81b3b4` | 0 |
| src/multisig/multisig_kex_msg_serialization.h | 2767 | `c9dbf4b439bf85f5eeb910635ac422dd7dc23f8d30cdd5db27052ef0f0f94388` | 0 |
| src/multisig/multisig_tx_builder_ringct.cpp | 39982 | `4c40b206bf31cff470430dbb4d96f86c0721e7b803785b6cdd58084a4b01a306` | 0 |
| src/multisig/multisig_tx_builder_ringct.h | 4240 | `8fdff6a9a7ed02e4ce8735860c3476357e37116cdba7ab1738d6065ba62886da` | 0 |
| src/net/dandelionpp.cpp | 7824 | `c84e34bd2f4c07ae978c0fff1088819fa38182e05712ba2936467e874e4c9f56` | 0 |
| src/net/dandelionpp.h | 4401 | `3e0c264071eacef26a8bfca377d7399bf10c4e04a8dd344aa5d6c4879203562e` | 0 |
| src/net/error.cpp | 4202 | `5ea382659487e8d5f477063455ff3b790050eff92d619676783603a43c9a6d9b` | 0 |
| src/net/error.h | 3013 | `5c03072aabf37eaf4ef9ec06ef8f25c12c7869eec7e28f00b9721c302add3eb6` | 0 |
| src/net/fwd.h | 2063 | `16fc122d1533629bd11ed91292e1089b5342cc5ab2d30e8a405d212de8a52ad4` | 0 |
| src/net/host.h | 421 | `14c6638f26638196a5c8cc4b3d1b7c247fcb38aad9b376c1ba9101cfe6d9db2c` | 0 |
| src/net/http.cpp | 2394 | `89dd0289cb99021303a8776f8428f827036120be567ec4bf4a2ac5f51b4eedb3` | 0 |
| src/net/http.h | 2005 | `f4a1d1e8fefad0ee1cc3b9b3d8bf9293f84e685c78d34fe893bae426e5c8f35c` | 0 |
| src/net/i2p_address.cpp | 7988 | `5cba903bc483d465a6d6a3ee28c22beac00a387cfb81be98cd24fbb23616c78b` | 0 |
| src/net/i2p_address.h | 5719 | `498c7c51fe36515749456fe78676a381962d868ba65de2f457bdca1b8be04a98` | 0 |
| src/net/parse.cpp | 11308 | `e16650484fcc7da2bc706172a3e5388ceaecc9e75b9adcdcd9dc4ce5f7e7bac8` | 0 |
| src/net/parse.h | 6115 | `3a7ec9c7c24d10428ebb769bc39c7d6c9e8f14c70bd2d7fabb9a60531c5b0805` | 0 |
| src/net/resolve.cpp | 2879 | `63b2b4bc6e36c132eee48a9696eddd1ff3ddbf81896826795f9ffa26e8a548e2` | 0 |
| src/net/resolve.h | 2089 | `9e3cc2dee49244ede22cf692b74aa38ef4ddb7ef6bf4b7387ded5758fa48ae27` | 0 |
| src/net/socks.cpp | 31196 | `dc433b90f1c17b5a8a8876d8506e13f8a5aa931cf7d5a1a6372bad8c9715c307` | 0 |
| src/net/socks.h | 9933 | `a341282e8e66cd78395090d42f828c42a3e4fd8fae65d5cce3b0ce18c65cdafd` | 0 |
| src/net/socks_connect.cpp | 4667 | `ceddfa10494c10a4f9f61f0a2c7429afa6962e7a821efb594265ec9e90167b60` | 0 |
| src/net/socks_connect.h | 2482 | `8b25ac4cfd50e6b8afa1706163db471e9715948fd8e16598f78fa00cbf4c6ddf` | 0 |
| src/net/tor_address.cpp | 10522 | `6492bc6fc1d706e971562d54bb300aec45ba8773907a8e1a675b8b2981df78a8` | 0 |
| src/net/tor_address.h | 6165 | `f7184774ef446ce1e5d8c96e93064d210099b8db7ac45b909df6dda55015c75d` | 0 |
| src/net/zmq.cpp | 7475 | `e69f6e7d9c4b61e1a4cc22d2a2ee2855a0301797fd3c70879dae9db913a99471` | 0 |
| src/net/zmq.h | 7329 | `11af387364c308f22df269bf963e944c2fffc051f370d78d8a536908b7d18a84` | 0 |
| src/p2p/net_node.cpp | 18599 | `8043503fe66baa6a8de6dcdab44cbb25fbf2a5e3e9e28b8847fea8c9b49f4f68` | 0 |
| src/p2p/net_node.h | 25038 | `6f193237b58e21129bb23b009acaf8b35be7e07deed6fe0e042098fde1470088` | 0 |
| src/p2p/net_node_common.h | 6168 | `fe637f24443629c0adb49c69df97b16349e063c28e8b131457aa83ea2f12a5fa` | 0 |
| src/p2p/net_peerlist.cpp | 9447 | `38ec2dd134027947eeb6260414d8bc16293a35719611261197cab76160eb0523` | 0 |
| src/p2p/net_peerlist.h | 19467 | `dd2d8fb66cd268cfea188f27e030dcf43529f3f3a1b0d3c48a711b014b6cd67d` | 0 |
| src/p2p/net_peerlist_boost_serialization.h | 8245 | `3660393ce76a6ac7f66c922f1665fa2562f9f49b6a940a87059e25095da05f3b` | 0 |
| src/p2p/p2p_protocol_defs.h | 9435 | `91a1374000110f9526c7812890a6902dbf990a187f07f9b47317ee8e545332b8` | 0 |
| src/ringct/bulletproofs.cc | 37126 | `fe61080cfbe7710847a97ea49e8463928cc4ae83eab439e623eda070b9dd17b0` | 0 |
| src/ringct/bulletproofs.h | 2240 | `e36c28a84778076d333fcf6011fb986058f75d8238855fa0d0aa796923c6e2bd` | 0 |
| src/ringct/bulletproofs_plus.cc | 44785 | `3b77634f01a1d5e7f007c5fcf8b6bad0eab0689ad277a18a825f17fee4a43d20` | 0 |
| src/ringct/bulletproofs_plus.h | 2266 | `64d3dc95fe1da6fd48c29ff14664a10f1148b4101e48efadda1922e14a92745d` | 0 |
| src/ringct/multiexp.cc | 19998 | `8d2499a1785fff85d4a870abedfbf1fa97bb9895276a57a4443a50483fd36f67` | 0 |
| src/ringct/multiexp.h | 3476 | `d6ad8b749e21e776d68e0f8d22d3b0f90d00222778cb381ef5ef0a046be36408` | 0 |
| src/ringct/rctCryptoOps.c | 6408 | `e89a3c4e7c1fced6d8472c5a74a6c2f419171ed73cfe7d928a0adddc740d41ce` | 0 |
| src/ringct/rctCryptoOps.h | 1813 | `6c66a5eed0a9181461f4561b3ea4dd1c067901403a8561c4d78cc4429ec72da8` | 0 |
| src/ringct/rctOps.cpp | 58439 | `0cd3cbb185c4053e8b17b3a6279d02bfe18b6f48a61e0e334f7baa3a2cd46d77` | 0 |
| src/ringct/rctOps.h | 8520 | `dc34e9a64653c2f16a479228e4c0e3df907ecfacade80fce17b4808458a1dc10` | 0 |
| src/ringct/rctSigs.cpp | 67411 | `2d45e11f8f8aecb5bcec1570b8fbbf26e6e4133b1652f02cec1826deb0b83436` | 0 |
| src/ringct/rctSigs.h | 8303 | `60dd8268f5c8c9c2ba00e59db1f2f819e37530ad00aedb09719728dd8c10a9f3` | 0 |
| src/ringct/rctTypes.cpp | 9912 | `5585d9e05295e7ec46c7b22e11b7a3f8d2c1980d954415956a3a441e7a322c40` | 0 |
| src/ringct/rctTypes.h | 42153 | `fbeb5fb765342f26b4a8e0c1aba8070d4fa6a171491b57c9dfa7eb7958e8cecb` | 0 |
| src/rpc/core_rpc_server.cpp | 130669 | `6104917c5d74e04be25cb72404cf7ed55fbdf8988fbfb51988be79f251b00aa9` | 0 |
| src/rpc/core_rpc_server.h | 26168 | `b69205bc80e986f8677bc1752545af2431673838480c0cc5e0c2f29b32a2066e` | 0 |
| src/rpc/core_rpc_server_commands_defs.h | 72176 | `cbaabb92c9d7800e3121e3223025bf2377a07fabca4122bc3e247089968371ca` | 0 |
| src/rpc/core_rpc_server_error_codes.h | 4553 | `835573f857415bb8826b85b0f904fafaeb82b6775b0d15168e8688c196752584` | 0 |
| src/rpc/daemon_handler.cpp | 36748 | `8134593b61b146499bfa1ddb9b422f16bc0c6146799bcdbc63a0e6d4d2b49084` | 0 |
| src/rpc/daemon_handler.h | 5877 | `4f2a096abeb9f5909a13789db801b2c6dcffa9930444631308bd161b97aa8fd9` | 0 |
| src/rpc/daemon_messages.cpp | 21374 | `324a3fd990590449a395933be969cec02b6078daf36f33b97c58b03a52f941b8` | 0 |
| src/rpc/daemon_messages.h | 14433 | `68ed4f29b73532bba7c4fc81acbbb834a30019bbbc9c937ea88bda72a5fe9574` | 0 |
| src/rpc/daemon_rpc_version.h | 1945 | `365e180895864fda01f9eb1bfc7bc3b79a0790851304807586593f4dac21782f` | 0 |
| src/rpc/fwd.h | 1673 | `f48796f8a3dbd0bc2f9fed9b7a0787cc4a9b5d1027b9b2fbcc7232f3d551d170` | 0 |
| src/rpc/instantiations.cpp | 2056 | `403c4b15fe1329fb840d96ff0e2f4ede834f7377fcaa4e2611c857b04cd8deac` | 0 |
| src/rpc/message.cpp | 7564 | `82af36d64276c6ee3586b2e0591abff23d4e4617c98311ef21e241620d6ccb89` | 0 |
| src/rpc/message.h | 3720 | `9027947d8286545de72d581d27f4cc56bfa99ac5f76fd43b6ea2bb2c24b58657` | 0 |
| src/rpc/message_data_structs.h | 5495 | `59ef19412e9b1ecd65ccc31e2ab1c19096091d144e892e61ca8c008b2cd193ca` | 0 |
| src/rpc/rpc_args.cpp | 13133 | `47810f5b5f0b92df27e74efaa8c77d3b643b475771e6c3ecb495fe30b7af2796` | 0 |
| src/rpc/rpc_args.h | 4784 | `266f0893c0f0bc715173f4b7fde56d2db7d3e9f5fb46537fa0bc6bc3bc7c29c6` | 0 |
| src/rpc/rpc_handler.cpp | 4487 | `cb0a82c82cd700649e95ed34f1385804e4bf5e0f6bdd9db6ed35f5211984817c` | 0 |
| src/rpc/rpc_handler.h | 2464 | `733a9e379e388e189cb1416f1f631226f13c29260ab889c60d9b5259542ff38f` | 0 |
| src/rpc/rpc_version_str.cpp | 2218 | `f3b13f68444e3b73ca5a4b3060389aac7dfa50d247fc74a28a5404a5825960c2` | 0 |
| src/rpc/rpc_version_str.h | 1763 | `0224dcb09772c566dbbeac2e510384f0f1e2d8873e82d13c7ef63473aea1679f` | 0 |
| src/rpc/zmq_pub.cpp | 19989 | `4d040ea7ad84b4118624d046f1ba25d06ffaf4273a880a9c3bd604275382aed2` | 0 |
| src/rpc/zmq_pub.h | 5430 | `1a0e31639042737a13295f3983093390c6dda94e6396c2f034fc29e8435b9faa` | 0 |
| src/rpc/zmq_restricted_methods.cpp | 2676 | `0eedbcc6a248edd55f73d30f11994372043365c08fc5d8efc22e134d8b2c0374` | 0 |
| src/rpc/zmq_restricted_methods.h | 2036 | `f02234a6da5874b2c91a4328f1bf72269515f32d9cafc75f2d30425ab82ac0af` | 0 |
| src/rpc/zmq_server.cpp | 9208 | `5ad4d5414b6805b53efec1b5355c55e9e24b6f20df693d3f79d62571374517d4` | 0 |
| src/rpc/zmq_server.h | 2684 | `e84186df7a45fcc4cbbab3152d6ded743c8b326a66eb6eabe3e2239d7b8bcef7` | 0 |
| src/serialization/binary_archive.h | 7238 | `f5578514503217162d9549f62800577b18a6551069e0963924c7a870e23306d9` | 0 |
| src/serialization/binary_utils.h | 2418 | `d67f591fb9d6eec08880a00f2c75c2ca39ede484217c5a67074b83cbd151a927` | 0 |
| src/serialization/container.h | 6196 | `d9f43b3db3d753e201aef43658d2951e691d1d51980a1939139a309747fdeeee` | 0 |
| src/serialization/containers.h | 3231 | `24ccc6633b49998c48f4333d16ff24f56b0335d41897c88f94e3901039a0c0d8` | 0 |
| src/serialization/crypto.h | 3535 | `33693773359fc7a4e2dabab7adcbace55ea830cf15ce597182c79ea1d531f39d` | 0 |
| src/serialization/debug_archive.h | 2297 | `c5387d2d6df5fa388617ae1c5bf5576c022abe766fe44dad62704df32cb76203` | 0 |
| src/serialization/difficulty_type.h | 2425 | `6db74c550326d3b4afd35d2e9ebfa12946ee9ef6943b5f53febf415f0546da39` | 0 |
| src/serialization/json_archive.h | 5018 | `ef16b6f19ee88e77439fe7927acf8592c36bf48d7c586d9082c629f6807e8999` | 0 |
| src/serialization/json_object.cpp | 45554 | `c75a5f2fad1d8db94c3345b5637dd63761bf1e6e1330cbacea077b8f41735211` | 0 |
| src/serialization/json_object.h | 16656 | `782630f3c7d52c5b2a3e4863e692054efd404a537a0bc9f4c1afda847ddb0908` | 0 |
| src/serialization/pair.h | 3646 | `bdff05396b383bdc3b5e5c21455befccb91838d0cb307178b57af31ed19db65a` | 0 |
| src/serialization/serialization.h | 12136 | `ea7a0f0575c0407d05ac5df5474dee7ac4b16bd7d277182f17c0d857f09e27c6` | 0 |
| src/serialization/string.h | 2422 | `db41c1e3bd30f7c4c264ce48bbbb3cd68853e4894a94186f4a956cefd6a90e40` | 0 |
| src/serialization/tuple.h | 4044 | `cd05dc5475aaf4c1ea3ef00f6cdb7e0c8ef196f6640c5d280ee15ac53b77f658` | 0 |
| src/serialization/variant.h | 4854 | `c6d14557694e9a91948917d250f350e761a028cc23d3df422ec13ec96ba68ba4` | 0 |
| src/simplewallet/simplewallet.cpp | 439466 | `8408b5260efed6c903fac16f4ed653f39dc704be7bc08d9feba7f05596792b87` | 0 |
| src/simplewallet/simplewallet.h | 26770 | `b44752ac31624450fbb3693a1be39cb515193e6bc73f3f7506ecfc646519a1de` | 0 |
| src/version.h | 237 | `f2a50f491b82cd557c6ab2e52bb5292933746508f79ba9c97112ee33b01ce47b` | 0 |
| src/wallet/api/address_book.cpp | 5503 | `8f7816d631901826c40568b929c564cb1cd5e786bff5a972074ee7f568c187af` | 0 |
| src/wallet/api/address_book.h | 2752 | `a8fd7a7681cc75cecd9c252c39a4abae0df00c5840230fd364b2ce41042b2159` | 0 |
| src/wallet/api/common_defines.h | 104 | `bd3a70e86ead51a12a8a0646674c115eed928961ee78fbf4d492fcb53fa76f56` | 0 |
| src/wallet/api/pending_transaction.cpp | 8772 | `08386a626d0cf11f3acaa2381ef0b1d43f375f568029c7c15f0d9155e1ec5d43` | 0 |
| src/wallet/api/pending_transaction.h | 2963 | `b1f2f83b73beb550bf00c5fa45193c96ac1a9befec9247d4c72daf73a9f6a9df` | 0 |
| src/wallet/api/subaddress.cpp | 2995 | `648aa61c6319120b678b4d8ccb52868d682b6e03bde5a6ce55bd2249f91efa35` | 0 |
| src/wallet/api/subaddress.h | 2248 | `b5360cec6bc3f1e553407fa67a8c80f6cc5bbeec510cef84a23116b948b3d4f7` | 0 |
| src/wallet/api/subaddress_account.cpp | 3019 | `b5fc0a33c0b1b8c1aa011ee7cad8034095884043519c43e4157330f671add8fd` | 0 |
| src/wallet/api/subaddress_account.h | 2187 | `3bdc62f5b1db06ec19e73074cf1bcebf410eee0a6708f1557a2981a7fc827499` | 0 |
| src/wallet/api/transaction_history.cpp | 11485 | `979337f589537bb7f87208ce21cae70d6c05196d988986e5e0dc93cc274609b6` | 0 |
| src/wallet/api/transaction_history.h | 2468 | `d789f1599434b319122b851324d85dcecdce5cd1653ec3cbb99302a5a9e2fe54` | 0 |
| src/wallet/api/transaction_info.cpp | 3635 | `f27d2819ad6999a2f3187052df0b2e5465fdad904d7ba9ccf39cdc5368875e0c` | 0 |
| src/wallet/api/transaction_info.h | 3521 | `9aefb2062a19c7f041bf6e85987e1192421223e33f3a77fd725e66f19b0580d4` | 0 |
| src/wallet/api/unsigned_transaction.cpp | 12018 | `1f932509abb26e5c2da91ff45ca8de2f9d3365aaac42005ce64844b5a7702367` | 0 |
| src/wallet/api/unsigned_transaction.h | 3066 | `4b44e743463c6d17d677d035efe3f9c843710bf54475dfb3654c519b25594f86` | 0 |
| src/wallet/api/utils.cpp | 2171 | `139d92ecb5e71fc5dbc642221cf241af9ee61021b7fcb1115abba5ac19ff12e0` | 0 |
| src/wallet/api/wallet.cpp | 96145 | `0353531b4e43c35185a653377c97b07449ddabec1741f9b62f945d6c51a3b8ee` | 0 |
| src/wallet/api/wallet.h | 18377 | `73603b335637795155fc4f961b977adfe6f4b0430e2c511fbb8bc69dc838e310` | 0 |
| src/wallet/api/wallet2_api.h | 63491 | `de9d0144b609ca866c73b5d90a2c672d0eba827abfc5c17f13bfb4ef6cc0977a` | 0 |
| src/wallet/api/wallet_manager.cpp | 16075 | `88fe910cd2873128934d14456efeb618c57007fcbafeeac55dbb81f0e0cdfe89` | 0 |
| src/wallet/api/wallet_manager.h | 6823 | `c28aed7b9286c506774c8481b2dbe68e2eb0e5c0ff0f544729a507bc4eb7eab5` | 0 |
| src/wallet/fee_algorithm.h | 1967 | `ad9b73a35956c10a8ce15fc174915a432eb9cb66c990eacfaaa61fa79567d8c0` | 0 |
| src/wallet/fee_priority.cpp | 1787 | `fb8c0b71eff89d5a497f4521dede3e69c7cb0ef4024f8418e963d9ac94a6fcad` | 0 |
| src/wallet/fee_priority.h | 5320 | `b154a17e5ec795c5448f75620f6cc49d0dcf23f35f7336a92eec1250c9e0c08b` | 0 |
| src/wallet/message_store.cpp | 54341 | `949969fb6dfda898fe682a123e10c7726ebdb1bde8adb20f0b42551d97c6bb8c` | 0 |
| src/wallet/message_store.h | 16239 | `e1a370f5ce11d037e5b230bcf3cc34e2a23cc6984fdc8f4af5097adfd7664f1d` | 0 |
| src/wallet/message_transporter.cpp | 15090 | `91f40cac1a3baa2bd25703ebda083d0f5134d285b28417a96c393db153c1dfbf` | 0 |
| src/wallet/message_transporter.h | 4581 | `713cc11cc94acb41710b465bc7de93ec8ce07cfde3333f35803d525f9f42ff03` | 0 |
| src/wallet/node_rpc_proxy.cpp | 13146 | `4574a3ba7586086461d02b96accd462b32ebbc248f839e19ecff299a58f6cccd` | 0 |
| src/wallet/node_rpc_proxy.h | 4078 | `8b7d0d436bab9f44d0860359a5fc5cf9e4c3b9c5bafc847cbc3e14529c1a9f2c` | 0 |
| src/wallet/pending_tx_validation.cpp | 45079 | `e538b7002dde58ad082b194322967db74d947e2e248c7968f072735d6147117a` | 0 |
| src/wallet/pending_tx_validation.h | 5701 | `c8e6f75396e5406f8c60140ceed76e2f7a7f62c7940a47f64de1769d81199cbf` | 0 |
| src/wallet/ringdb.cpp | 16960 | `7881b0d0d1386e8a54025ec60c4683397ee4b662c6b57b9f8715e63101a7c02d` | 0 |
| src/wallet/ringdb.h | 2878 | `b0b1d61f1c4714e4eef9e7dd6f6bfb00d882bb887fe3d39a88e14267bcbbd4f1` | 0 |
| src/wallet/wallet2.cpp | 719577 | `d20f537fc704b3b817864a69091f88d3f022b86de92b0b97bf2a3f460274ce4f` | 0 |
| src/wallet/wallet2.h | 106674 | `1384e76292999719948e24bf9616a55a7f18ae553ec07f24c38d3fabc9ada810` | 0 |
| src/wallet/wallet2_basic/wallet2_boost_serialization.h | 11638 | `eef05b8051025b896a55e2f33ac8f101f8b38f2d040cd3c46a35dddfab89f256` | 0 |
| src/wallet/wallet2_basic/wallet2_serialization.h | 5052 | `c182e4c10aaec6d133562d18ef0fb6b0296c3b32c608639a5f7e31a01171c6c7` | 0 |
| src/wallet/wallet2_basic/wallet2_types.h | 10600 | `41705780b5375e30107056fb901f2585b1b190f99c73b4835e4faaf780babeeb` | 0 |
| src/wallet/wallet_args.cpp | 9005 | `df1c9f26258bb12a70256f5afa398b6bcca588f6b3df27cb6a24b36ec9d803b4` | 0 |
| src/wallet/wallet_args.h | 2998 | `a51e954c2a06819f07bb27c29e34c57e01083756ea01b61496fc39a974e94131` | 0 |
| src/wallet/wallet_errors.h | 41867 | `bcb75a8b3a8c0aba60eddbef9d3c25baa3e11659236924c83b6ec1004c014b17` | 0 |
| src/wallet/wallet_rpc_server.cpp | 216932 | `f7245a8568f45c8528feb1900c83bdc50dfaeddd8d3c665590e9171716ebab34` | 0 |
| src/wallet/wallet_rpc_server.h | 36202 | `639ba5dfd09c9147564cc653760eb7a5bfc7832973e1b115308cffc3825ba75a` | 0 |
| src/wallet/wallet_rpc_server_commands_defs.h | 71893 | `5994ba58923241d36314d624ace92f5c7f6f97d833806f5bcd11b28c3549a299` | 0 |
| src/wallet/wallet_rpc_server_error_codes.h | 4733 | `79ebbf54396c0792be4beaf969587677be77cb76a33d9033f3adc6cc08d87a91` | 0 |
