# Security & Post-Quantum Readiness Audit Report

**Project:** cairo @ 68a61f6c6251 · StarkWare — public repository (passive review)
| | |
|---|---|
| Organization | QSI |
| Report date | 2026-10-28 12:22 UTC |
| Report version | 1 |
| Audit run | 3ee51131-9f40-4430-8d6c-442a9bdfd05e (Document audit) |
| Analyzer engine | qsi-engine 1.2.0 |
| Risk profile | Web3 project |
| Content SHA-256 | `18d87b68c3d7d5ee5324566405f8f401703b54def1529b72cf769a0cbf89aa4a` |
| Signature key (Ed25519, SHA-256 fingerprint; the signature is the separate file report.sig.json) | `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e` |
> This report presents automated and documented analysis results for the stated scope. It is not a legal opinion, a certification or an attestation of compliance with any standard.

## 1. Executive summary

- Critical: **1**
- High: **4**
- Medium: **5**
- Low: **10**
- Info: **4**

- Confirmed technical vulnerability: 0
- Known vulnerable component: 19
- Confirmed configuration error: 0
- Potential cryptographic risk: 0
- Long-term post-quantum risk: 2
- Improvement recommendation: 2
- Insufficient data: 1

Mosca's inequality (x + y > z): x = 5, y = 5, z = 12 → tight margin. _z is a planning assumption chosen per risk profile, not a prediction. A cryptographically relevant quantum computer is not publicly known to exist today._

**Post-quantum maturity: Level 0 of 4 — no post-quantum cryptography.** Next step: Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

## 2. Scope and boundaries

Mode: Document audit

Repository: <https://github.com/starkware-libs/cairo> @ `68a61f6c6251900e0080e09c812ffaeb37fd358e` — evidence links open the lines at this commit.

567 files, 8154078 bytes in total, 0 redaction(s); the per-file SHA-256 list is in appendix C.

## 3. Methodology

| Area | Status | Count | Examples |
|---|---|---|---|
| dependencies | checked | 50 | Cargo.lock: 453 dependencies parsed (453 pinned); Cargo.toml: 63 dependencies parsed (1 pinned); crates/bin/cairo-compile/Cargo.toml: 9 dependencies parsed (3 pinned) |
| source_code | checked | 516 | crates/bin/cairo-compile/src/main.rs: 86 lines scanned with 16 rule patterns and 122 registry patterns; crates/bin/cairo-execute/src/main.rs: 452 lines scanned with 16 rule patterns and 122 registry patterns; crates/bin/cairo-format/src/main.rs: 232 lines scanned with 16 rule patterns and 122 registry patterns |
| osv_advisories | checked | 1 | 485 pinned packages queried at OSV.dev; 13 affected |

_Long lists are grouped here; the full per-file list is in the JSON report, signed with the same key._

## 4. Assets examined and not examined

- None

## 5. Architecture overview

Static review of the source tree cairo at 68a61f6c6251900e0080e09c812ffaeb37fd358e. 567 files analysed; of 1762 files, 855 are test, fuzzing, benchmark or example code and were left out, 340 are not read by any analyzer, 0 exceed the per-file limit and 0 did not fit the total limit. No requests were sent to the owner's systems.

## 6. Overall security posture

- Indicative posture index: **2** / 100 — _Derived from findings in scope (confirmed and potential issues weighted by severity). Indicative only; not comparable across differently scoped audits._
- Quantum-vulnerable share of inventory: 55.6%

## 7. Detailed findings

### QSI-2026-04420 — zip 0.6.6 is affected by RUSTSEC-2026-0369

- Severity: **Critical** · Classification: Known vulnerable component · Confidence: Low
- Affected asset: `dependency:crates.io/zip@0.6.6`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 12:22 UTC
- Priority score: 40.5 / 100
- CVSS v3.1: 9.1 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H`)

OSV.dev reports RUSTSEC-2026-0369 for crates.io package zip at version 0.6.6: ZipStreamReader::extract() and ZipArchive::extract() apply Unix permissions through symlinks without confining the target. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0369
```

**Evidence.**

_tool_output · [OSV.dev RUSTSEC-2026-0369](https://osv.dev/vulnerability/RUSTSEC-2026-0369) · manifest · SHA-256 889fd754651c2317ee1367e6b79afa5c8dc85363614c3ddf017e6e7118c949ce_

```
{"id": "RUSTSEC-2026-0369", "aliases": ["GHSA-4684-h2q9-2vcp"], "modified": "2026-10-16T23:30:02.387698467Z", "summary": "ZipStreamReader::extract() and ZipArchive::extract() apply Unix permissions through symlinks without confining the target", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H"}], "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (9.0.0).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-04406 — pulldown-cmark 0.13.4 is affected by RUSTSEC-2026-0414

- Severity: **High** · Classification: Known vulnerable component · Confidence: Medium
- Affected asset: `dependency:crates.io/pulldown-cmark@0.13.4`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 12:22 UTC
- Priority score: 49.2 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev reports RUSTSEC-2026-0414 for crates.io package pulldown-cmark at version 0.13.4: Exponential event growth with `ENABLE_WIKILINKS`. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0414
```

**Evidence.**

_tool_output · [OSV.dev RUSTSEC-2026-0414](https://osv.dev/vulnerability/RUSTSEC-2026-0414) · manifest · SHA-256 84141280a223372225a976433f4a051a0f151b4a2d3daaa5d454b3808029c61e_

```
{"id": "RUSTSEC-2026-0414", "aliases": [], "modified": "2026-10-28T09:00:02.341043798Z", "summary": "Exponential event growth with `ENABLE_WIKILINKS`", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (0.13.5).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-04408 — quinn-proto 0.11.17 is affected by RUSTSEC-2026-0340

- Severity: **High** · Classification: Known vulnerable component · Confidence: Low
- Affected asset: `dependency:crates.io/quinn-proto@0.11.17`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 12:22 UTC
- Priority score: 36.9 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev reports RUSTSEC-2026-0340 for crates.io package quinn-proto at version 0.11.17: Peer minimum ACK delay can panic quinn-proto when ACK_FREQUENCY transmission is enabled. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0340
```

**Evidence.**

_tool_output · [OSV.dev RUSTSEC-2026-0340](https://osv.dev/vulnerability/RUSTSEC-2026-0340) · manifest · SHA-256 20321fd13a708b936ab6ccc115a6ed97f9b78eb43a4e76d134ec1664a5fc8feb_

```
{"id": "RUSTSEC-2026-0340", "aliases": ["GHSA-3g6h-r5qx-f6hq"], "modified": "2026-10-12T18:15:01.975478256Z", "summary": "Peer minimum ACK delay can panic quinn-proto when ACK_FREQUENCY transmission is enabled", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (0.11.18).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-04409 — quinn-proto 0.11.17 is affected by RUSTSEC-2026-0343

- Severity: **High** · Classification: Known vulnerable component · Confidence: Low
- Affected asset: `dependency:crates.io/quinn-proto@0.11.17`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 12:22 UTC
- Priority score: 36.9 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev reports RUSTSEC-2026-0343 for crates.io package quinn-proto at version 0.11.17: Outgoing datagram buffer accounting can panic the sender in quinn-proto. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0343
```

**Evidence.**

_tool_output · [OSV.dev RUSTSEC-2026-0343](https://osv.dev/vulnerability/RUSTSEC-2026-0343) · manifest · SHA-256 8038e96bc82cf763be522e034a1baf7a01bd0b6523ae60faa215d96e1fd3adc3_

```
{"id": "RUSTSEC-2026-0343", "aliases": ["GHSA-ppcp-v39w-8jq2"], "modified": "2026-10-12T18:15:01.961745820Z", "summary": "Outgoing datagram buffer accounting can panic the sender in quinn-proto", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (0.11.18).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-04418 — zip 0.6.6 is affected by RUSTSEC-2026-0367

- Severity: **High** · Classification: Known vulnerable component · Confidence: Low
- Affected asset: `dependency:crates.io/zip@0.6.6`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 12:22 UTC
- Priority score: 36.9 / 100
- CVSS v3.1: 7.3 (`CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H`)

OSV.dev reports RUSTSEC-2026-0367 for crates.io package zip at version 0.6.6: Insecure Preservation of SUID/SGID Bits during ZIP Extraction Leading to Potential Privilege Escalation. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0367
```

**Evidence.**

_tool_output · [OSV.dev RUSTSEC-2026-0367](https://osv.dev/vulnerability/RUSTSEC-2026-0367) · manifest · SHA-256 db37f0f24f5796f64e8d2e96846b7cf21dd61e1b0a4c7de21b8268aa1a29a3c7_

```
{"id": "RUSTSEC-2026-0367", "aliases": ["GHSA-vv5m-jxxh-4627"], "modified": "2026-10-16T23:30:02.392172556Z", "summary": " Insecure Preservation of SUID/SGID Bits during ZIP Extraction Leading to Potential Privilege Escalation", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H"}], "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (9.0.0).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-04398 — Quantum-vulnerable ECDSA: transaction and message signing (2 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:ECDSA:transaction_signing`
- Data source: crates/cairo-lang-sierra/src/extensions/modules/starknet/mod.rs
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.2.0 · 2026-10-28 12:22 UTC
- Priority score: 33.0 / 100
- CVSS v3.1: not applicable

3 reference(s) to ECDSA across 2 file(s), e.g. crates/cairo-lang-sierra/src/extensions/modules/starknet/mod.rs:24. Role, judged from paths, function names and nearby code: transaction and message signing. A CRQC derives the private key from a public key that is already known (on chain after the first spend, in reused addresses): funds and approvals controlled by these keys need a migration path.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open crates/cairo-lang-sierra/src/extensions/modules/starknet/mod.rs:24 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [crates/cairo-lang-sierra/src/extensions/modules/starknet/mod.rs](https://github.com/starkware-libs/cairo/blob/68a61f6c6251900e0080e09c812ffaeb37fd358e/crates/cairo-lang-sierra/src/extensions/modules/starknet/mod.rs#L24) · line 24 · SHA-256 114a4f0ae1d810207edaf43599b7cc9c2dd4f7800eb06b14137002a53c4d3aaa_

```
   23 | use secp256::{Secp256Libfunc, Secp256PointType};
   24 | pub mod secp256k1;
   25 | pub mod secp256r1;
```

_file_excerpt · [crates/cairo-lang-sierra/src/extensions/modules/starknet/mod.rs](https://github.com/starkware-libs/cairo/blob/68a61f6c6251900e0080e09c812ffaeb37fd358e/crates/cairo-lang-sierra/src/extensions/modules/starknet/mod.rs#L25) · line 25 · SHA-256 7e6e9c2b04ea6d156352d55791e4b83d960da30ac66655bad69061284c310fe7_

```
   24 | pub mod secp256k1;
   25 | pub mod secp256r1;
   26 | 
```

_file_excerpt · [crates/cairo-lang-sierra/src/extensions/modules/starknet/secp256k1.rs](https://github.com/starkware-libs/cairo/blob/68a61f6c6251900e0080e09c812ffaeb37fd358e/crates/cairo-lang-sierra/src/extensions/modules/starknet/secp256k1.rs#L24) · line 24 · SHA-256 ae5dfb6aa4a275c5330cd1255673964bbd5607c4d8f7d91a489d41672690d159_

```
   23 |     const TYPE_ID: GenericTypeId = Secp256k1PointType::ID;
   24 |     const TYPE_ID_STR: &'static str = "core::starknet::secp256k1::Secp256k1Point";
   25 | }
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains adopt them.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-04397 — Quantum-vulnerable ECDSA: role not determined (4 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:ECDSA:general`
- Data source: crates/cairo-lang-runner/src/casm_run/mod.rs
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.2.0 · 2026-10-28 12:22 UTC
- Priority score: 31.7 / 100
- CVSS v3.1: not applicable

7 reference(s) to ECDSA across 4 file(s), e.g. crates/cairo-lang-runner/src/casm_run/mod.rs:41. Role, judged from paths, function names and nearby code: role not determined. The code does not show what the keys protect; review decides the priority.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open crates/cairo-lang-runner/src/casm_run/mod.rs:41 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [crates/cairo-lang-runner/src/casm_run/mod.rs](https://github.com/starkware-libs/cairo/blob/68a61f6c6251900e0080e09c812ffaeb37fd358e/crates/cairo-lang-runner/src/casm_run/mod.rs#L41) · line 41 · SHA-256 0e71c46f74a3ab0591cba43edd9de9663e8a101e5386eebba48bc383848c95de_

```
   40 | use lambdaworks_math::cyclic_group::IsGroup;
   41 | use lambdaworks_math::elliptic_curve::short_weierstrass::curves::secp256k1::curve::Secp256k1Curve;
   42 | use lambdaworks_math::elliptic_curve::short_weierstrass::curves::secp256r1::curve::Secp256r1Curve;
```

_file_excerpt · [crates/cairo-lang-runner/src/casm_run/mod.rs](https://github.com/starkware-libs/cairo/blob/68a61f6c6251900e0080e09c812ffaeb37fd358e/crates/cairo-lang-runner/src/casm_run/mod.rs#L42) · line 42 · SHA-256 f4453e699fd83272c62133e0dd37b99331fbdec4356805860f334ca4b867a406_

```
   41 | use lambdaworks_math::elliptic_curve::short_weierstrass::curves::secp256k1::curve::Secp256k1Curve;
   42 | use lambdaworks_math::elliptic_curve::short_weierstrass::curves::secp256r1::curve::Secp256r1Curve;
   43 | use lambdaworks_math::elliptic_curve::short_weierstrass::point::ShortWeierstrassProjectivePoint;
```

_file_excerpt · [crates/cairo-lang-sierra/src/extensions/modules/starknet/secp256.rs](https://github.com/starkware-libs/cairo/blob/68a61f6c6251900e0080e09c812ffaeb37fd358e/crates/cairo-lang-sierra/src/extensions/modules/starknet/secp256.rs#L3) · line 3 · SHA-256 2c337fb5211b6a3336031a7e331caf1e52a0f93519608e9f0dd756fc0e3971ab_

```
    2 | 
    3 | use super::secp256k1::{Secp256k1, Secp256k1PointType};
    4 | use super::secp256r1::{Secp256r1, Secp256r1PointType};
```

_file_excerpt · [crates/cairo-lang-sierra/src/extensions/modules/starknet/secp256.rs](https://github.com/starkware-libs/cairo/blob/68a61f6c6251900e0080e09c812ffaeb37fd358e/crates/cairo-lang-sierra/src/extensions/modules/starknet/secp256.rs#L4) · line 4 · SHA-256 20087e0fcacf6d88cdd30d21dd6df4607503072361aee4392c24edb9a627733e_

```
    3 | use super::secp256k1::{Secp256k1, Secp256k1PointType};
    4 | use super::secp256r1::{Secp256r1, Secp256r1PointType};
    5 | use super::syscalls::SyscallGenericLibfunc;
```

_file_excerpt · [crates/cairo-lang-sierra/src/extensions/modules/starknet/secp256r1.rs](https://github.com/starkware-libs/cairo/blob/68a61f6c6251900e0080e09c812ffaeb37fd358e/crates/cairo-lang-sierra/src/extensions/modules/starknet/secp256r1.rs#L24) · line 24 · SHA-256 d4163de088e926b53c4c5dce2c77bb74aeba87048a8ec413c75a07e5fd0768e6_

```
   23 |     const TYPE_ID: GenericTypeId = Secp256r1PointType::ID;
   24 |     const TYPE_ID_STR: &'static str = "core::starknet::secp256r1::Secp256r1Point";
   25 | }
```

_file_excerpt · [crates/cairo-lang-starknet-classes/src/felt252_serde.rs](https://github.com/starkware-libs/cairo/blob/68a61f6c6251900e0080e09c812ffaeb37fd358e/crates/cairo-lang-starknet-classes/src/felt252_serde.rs#L11) · line 11 · SHA-256 1eb81a2d0feea5c6487b656df37086af50f29a08d0020b120d765748e7a7fcbd_

```
   10 | use cairo_lang_sierra::extensions::starknet::secp256::Secp256GetPointFromXLibfunc;
   11 | use cairo_lang_sierra::extensions::starknet::secp256k1::Secp256k1;
   12 | use cairo_lang_sierra::extensions::starknet::secp256r1::Secp256r1;
```

_file_excerpt · [crates/cairo-lang-starknet-classes/src/felt252_serde.rs](https://github.com/starkware-libs/cairo/blob/68a61f6c6251900e0080e09c812ffaeb37fd358e/crates/cairo-lang-starknet-classes/src/felt252_serde.rs#L12) · line 12 · SHA-256 f63ec86cc34d6c40745db6eb5255f177f151fe4b72c607f13e481d4acd9ce5d3_

```
   11 | use cairo_lang_sierra::extensions::starknet::secp256k1::Secp256k1;
   12 | use cairo_lang_sierra::extensions::starknet::secp256r1::Secp256r1;
   13 | use cairo_lang_sierra::extensions::starknet::storage::{
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it; introduce an abstraction layer for crypto-agility.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-04401 — block-buffer 0.10.4 is affected by GHSA-qwgh-2vcv-g2f7

- Severity: **Medium** · Classification: Known vulnerable component · Confidence: Low
- Affected asset: `dependency:crates.io/block-buffer@0.10.4`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 12:22 UTC
- Priority score: 31.5 / 100
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

### QSI-2026-04410 — rustls 0.23.43 is affected by GHSA-2mjx-qc3c-rqvc (RUSTSEC-2026-0285)

- Severity: **Medium** · Classification: Known vulnerable component · Confidence: Low
- Affected asset: `dependency:crates.io/rustls@0.23.43`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 12:22 UTC
- Priority score: 31.5 / 100
- CVSS v3.1: 5.3 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N`)

OSV.dev reports GHSA-2mjx-qc3c-rqvc (RUSTSEC-2026-0285) for crates.io package rustls at version 0.23.43: Rustls: TLS 1.3 handshake messages incorrectly accepted across encryption level boundaries. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-2mjx-qc3c-rqvc
```

**Evidence.**

_tool_output · [OSV.dev GHSA-2mjx-qc3c-rqvc](https://osv.dev/vulnerability/GHSA-2mjx-qc3c-rqvc) · manifest · SHA-256 f20e4b21c01d3d75460ac8d90a54d541a1a34187a4f05b501e4f46c27c564e86_

```
{"id": "GHSA-2mjx-qc3c-rqvc", "aliases": ["RUSTSEC-2026-0285"], "modified": "2026-10-27T15:30:05.509305490Z", "summary": "Rustls: TLS 1.3 handshake messages incorrectly accepted across encryption level boundaries", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N"}], "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (0.23.45).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-04411 — rustls 0.23.43 is affected by GHSA-c8m5-c952-6cm4 (RUSTSEC-2026-0346)

- Severity: **Medium** · Classification: Known vulnerable component · Confidence: Low
- Affected asset: `dependency:crates.io/rustls@0.23.43`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 12:22 UTC
- Priority score: 31.5 / 100
- CVSS v3.1: 4.0 (`CVSS:3.1/AV:L/AC:H/PR:H/UI:R/S:U/C:H/I:N/A:N`)

OSV.dev reports GHSA-c8m5-c952-6cm4 (RUSTSEC-2026-0346) for crates.io package rustls at version 0.23.43: Rustls: Session Debug formatting exposes TLS master secrets and resumption PSKs. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-c8m5-c952-6cm4
```

**Evidence.**

_tool_output · [OSV.dev GHSA-c8m5-c952-6cm4](https://osv.dev/vulnerability/GHSA-c8m5-c952-6cm4) · manifest · SHA-256 87554a0cce34470a221f04ad57566b2b512ff6299ad3ee95b190df659d646e3d_

```
{"id": "GHSA-c8m5-c952-6cm4", "aliases": ["RUSTSEC-2026-0346"], "modified": "2026-10-27T16:15:05.354395696Z", "summary": "Rustls: Session Debug formatting exposes TLS master secrets and resumption PSKs", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:L/AC:H/PR:H/UI:R/S:U/C:H/I:N/A:N"}], "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (0.23.46, 0.24.0-dev.2).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-04404 — lru 0.12.5 is affected by GHSA-rhfx-m35p-ff5j (RUSTSEC-2026-0002)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low
- Affected asset: `dependency:crates.io/lru@0.12.5`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 12:22 UTC
- Priority score: 27.0 / 100
- CVSS v3.1: not applicable

OSV.dev reports GHSA-rhfx-m35p-ff5j (RUSTSEC-2026-0002) for crates.io package lru at version 0.12.5: `IterMut` violates Stacked Borrows by invalidating internal pointer. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-rhfx-m35p-ff5j
```

**Evidence.**

_tool_output · [OSV.dev GHSA-rhfx-m35p-ff5j](https://osv.dev/vulnerability/GHSA-rhfx-m35p-ff5j) · manifest · SHA-256 74c3e26941575e818cf192f0511138a6719b2124292f8348b2d299a631095b03_

```
{"id": "GHSA-rhfx-m35p-ff5j", "aliases": ["RUSTSEC-2026-0002"], "modified": "2026-09-10T03:50:59.064354050Z", "summary": "`IterMut` violates Stacked Borrows by invalidating internal pointer", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N/E:U"}], "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (0.16.3).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-04413 — rustls 0.23.43 is affected by GHSA-w44r-93j7-qv28 (RUSTSEC-2026-0349)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low
- Affected asset: `dependency:crates.io/rustls@0.23.43`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 12:22 UTC
- Priority score: 27.0 / 100
- CVSS v3.1: 3.7 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N`)

OSV.dev reports GHSA-w44r-93j7-qv28 (RUSTSEC-2026-0349) for crates.io package rustls at version 0.23.43: rustls: An unauthenticated ServerHello poisons the per-name key-exchange record, so later ClientHellos carry only a classical X25519 share. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-w44r-93j7-qv28
```

**Evidence.**

_tool_output · [OSV.dev GHSA-w44r-93j7-qv28](https://osv.dev/vulnerability/GHSA-w44r-93j7-qv28) · manifest · SHA-256 f0fcaa2fa7a56e188458f39e55b23e999d0c7da6d3c1294c014c64ab37b33dee_

```
{"id": "GHSA-w44r-93j7-qv28", "aliases": ["RUSTSEC-2026-0349"], "modified": "2026-10-27T16:15:05.340347056Z", "summary": "rustls: An unauthenticated ServerHello poisons the per-name key-exchange record, so later ClientHellos carry only a classical X25519 share", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N"}], "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (0.23.46, 0.24.0-dev.2).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-04412 — rustls 0.23.43 is affected by GHSA-h2v8-394m-p7vv (RUSTSEC-2026-0348)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/rustls@0.23.43`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 12:22 UTC
- Priority score: 22.9 / 100
- CVSS v3.1: 3.7 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:N/A:L`)

OSV.dev reports GHSA-h2v8-394m-p7vv (RUSTSEC-2026-0348) for crates.io package rustls at version 0.23.43: Rustls: Brotli certificate decompression can allocate an attacker-controlled amount of memory up to 1 GiB before authentication. The affected code sits behind the `brotli` Cargo feature, off by default, which no audited manifest enables: the advisory does not apply unless another dependency enables it.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-h2v8-394m-p7vv
```

**Evidence.**

_tool_output · [OSV.dev GHSA-h2v8-394m-p7vv](https://osv.dev/vulnerability/GHSA-h2v8-394m-p7vv) · manifest · SHA-256 9118726d52fea7cee09a6b4a21a10d2a7bab860f9762fff4658cb78db0453744_

```
{"id": "GHSA-h2v8-394m-p7vv", "aliases": ["RUSTSEC-2026-0348"], "modified": "2026-10-27T16:15:05.337819489Z", "summary": "Rustls: Brotli certificate decompression can allocate an attacker-controlled amount of memory up to 1 GiB before authentication.", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:N/A:L"}], "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (0.23.46, 0.24.0-dev.2).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-04402 — crypto-bigint 0.5.5 is affected by RUSTSEC-2026-0387 (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/crypto-bigint@0.5.5`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 12:22 UTC
- Priority score: 18.4 / 100
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

### QSI-2026-04405 — lru 0.12.5 is affected by RUSTSEC-2026-0253 (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/lru@0.12.5`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 12:22 UTC
- Priority score: 18.4 / 100
- CVSS v3.1: not applicable

OSV.dev reports RUSTSEC-2026-0253 for crates.io package lru at version 0.12.5: Potential use-after-free due to lack of panic safety in `LruCache::pop()`. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0253
```

**Evidence.**

_tool_output · [OSV.dev RUSTSEC-2026-0253](https://osv.dev/vulnerability/RUSTSEC-2026-0253) · manifest · SHA-256 06df98c5350689983b2fda96297e3527fd26f472c5d474c041975b220e7ffc2c_

```
{"id": "RUSTSEC-2026-0253", "aliases": [], "modified": "2026-08-11T11:15:06.101553049Z", "summary": "Potential use-after-free due to lack of panic safety in `LruCache::pop()`", "severity": null, "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Triage the advisory; upgrade to a fixed version (0.18.2) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-04407 — quinn-proto 0.11.17 is affected by RUSTSEC-2026-0338 (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/quinn-proto@0.11.17`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 12:22 UTC
- Priority score: 18.4 / 100
- CVSS v3.1: not applicable

OSV.dev reports RUSTSEC-2026-0338 for crates.io package quinn-proto at version 0.11.17: Remote peer can panic quinn-proto with zero-length STREAM frames during unordered reads. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0338
```

**Evidence.**

_tool_output · [OSV.dev RUSTSEC-2026-0338](https://osv.dev/vulnerability/RUSTSEC-2026-0338) · manifest · SHA-256 2d8a96c1ccb5782dfd51ab6c6bfc548092df0a416eb5a7c29ca5b5ffdce603ea_

```
{"id": "RUSTSEC-2026-0338", "aliases": ["GHSA-465w-v9q3-7j98"], "modified": "2026-10-12T18:15:01.969514645Z", "summary": "Remote peer can panic quinn-proto with zero-length STREAM frames during unordered reads", "severity": null, "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Triage the advisory; upgrade to a fixed version (0.11.18) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-04414 — rustls-webpki 0.103.14 is affected by RUSTSEC-2026-0382 (CVE-2026-111943) (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/rustls-webpki@0.103.14`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 12:22 UTC
- Priority score: 18.4 / 100
- CVSS v3.1: not applicable

OSV.dev reports RUSTSEC-2026-0382 (CVE-2026-111943) for crates.io package rustls-webpki at version 0.103.14: Certificate verification may accept distrusted intermediates. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0382
```

**Evidence.**

_tool_output · [OSV.dev RUSTSEC-2026-0382](https://osv.dev/vulnerability/RUSTSEC-2026-0382) · manifest · SHA-256 9111e73d752392534752d5ea5c9da4ec9a422a29c088531d446d16b27a016fa8_

```
{"id": "RUSTSEC-2026-0382", "aliases": ["CVE-2026-111943", "GO-2026-6809", "RUSTSEC-2026-0381", "RUSTSEC-2026-0383"], "modified": "2026-10-21T00:55:56.763143468Z", "summary": "Certificate verification may accept distrusted intermediates", "severity": null, "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Triage the advisory; upgrade to a fixed version (0.103.16, 0.104.0-alpha.8) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-04415 — salsa 0.28.2 is affected by RUSTSEC-2026-0308 (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/salsa@0.28.2`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 12:22 UTC
- Priority score: 18.4 / 100
- CVSS v3.1: not applicable

OSV.dev reports RUSTSEC-2026-0308 for crates.io package salsa at version 0.28.2: Use-after-free in interned values and cached function results. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0308
```

**Evidence.**

_tool_output · [OSV.dev RUSTSEC-2026-0308](https://osv.dev/vulnerability/RUSTSEC-2026-0308) · manifest · SHA-256 580ef2afe3fb4006afc362c0b351c3c07e95f925e97e474f8909ed94a7cbe4b5_

```
{"id": "RUSTSEC-2026-0308", "aliases": ["GHSA-xc3w-55vh-cw3w"], "modified": "2026-09-24T14:45:04.873565398Z", "summary": "Use-after-free in interned values and cached function results", "severity": null, "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Triage the advisory; upgrade to a fixed version (0.28.5) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-04417 — webpki-root-certs 1.0.9 is affected by RUSTSEC-2026-0383 (CVE-2026-111943) (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/webpki-root-certs@1.0.9`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 12:22 UTC
- Priority score: 18.4 / 100
- CVSS v3.1: not applicable

OSV.dev reports RUSTSEC-2026-0383 (CVE-2026-111943) for crates.io package webpki-root-certs at version 1.0.9: Bundled root certificates allow trust in distrusted emSign intermediates. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0383
```

**Evidence.**

_tool_output · [OSV.dev RUSTSEC-2026-0383](https://osv.dev/vulnerability/RUSTSEC-2026-0383) · manifest · SHA-256 5020317ed72c7e0cbf2d22efcc385ee146b42c336ffbeb3bf453e64cec1e9d3d_

```
{"id": "RUSTSEC-2026-0383", "aliases": ["CVE-2026-111943", "GO-2026-6809", "RUSTSEC-2026-0381", "RUSTSEC-2026-0382"], "modified": "2026-10-21T06:30:02.691648061Z", "summary": "Bundled root certificates allow trust in distrusted emSign intermediates", "severity": null, "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Triage the advisory; upgrade to a fixed version (0.26.11, 1.0.10) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-04419 — zip 0.6.6 is affected by RUSTSEC-2026-0368 (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/zip@0.6.6`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 12:22 UTC
- Priority score: 18.4 / 100
- CVSS v3.1: not applicable

OSV.dev reports RUSTSEC-2026-0368 for crates.io package zip at version 0.6.6: zip: `ZipArchive::extract` creates symbolic links whose attacker-controlled targets are outside the destination directory. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0368
```

**Evidence.**

_tool_output · [OSV.dev RUSTSEC-2026-0368](https://osv.dev/vulnerability/RUSTSEC-2026-0368) · manifest · SHA-256 77cc28045dc809d16dfd7075061aa99e7aa21d64c6bf6d60981905302d10a02d_

```
{"id": "RUSTSEC-2026-0368", "aliases": ["GHSA-4v9h-p7m9-rh26"], "modified": "2026-10-16T23:30:02.383750571Z", "summary": "zip: `ZipArchive::extract` creates symbolic links whose attacker-controlled targets are outside the destination directory", "severity": null, "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Triage the advisory; upgrade to a fixed version (9.0.0) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-04403 — derivative 2.2.0: informational advisory RUSTSEC-2024-0388 (unmaintained)

- Severity: **Info** · Classification: Improvement recommendation · Confidence: High
- Affected asset: `dependency:crates.io/derivative@2.2.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 12:22 UTC
- Priority score: 18.7 / 100
- CVSS v3.1: not applicable

OSV.dev lists RUSTSEC-2024-0388 for crates.io package derivative at version 2.2.0 as informational (unmaintained): `derivative` is unmaintained; consider using an alternative. It reports no vulnerability; an unmaintained package will not receive fixes for future ones.

**Potential impact.** No known vulnerability. Future security fixes may not be released.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2024-0388
```

**Evidence.**

_tool_output · [OSV.dev RUSTSEC-2024-0388](https://osv.dev/vulnerability/RUSTSEC-2024-0388) · manifest · SHA-256 0624a2acbe96d2e8c44b2e7c9e0253aa4d99e8e969cd062a4b077f6a30749e57_

```
{"id": "RUSTSEC-2024-0388", "aliases": [], "modified": "2024-11-10T13:34:40Z", "summary": "`derivative` is unmaintained; consider using an alternative", "severity": null, "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time.

**Recommendation.** Plan a move to a maintained alternative, or record the decision to keep it.

**Retest procedure.** Re-run the dependency scan after the change.

### QSI-2026-04416 — tokio 1.53.1 is affected by RUSTSEC-2026-0386 (no severity rating)

- Severity: **Info** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/tokio@1.53.1`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 12:22 UTC
- Priority score: 15.3 / 100
- CVSS v3.1: not applicable

OSV.dev reports RUSTSEC-2026-0386 for crates.io package tokio at version 1.53.1: `AsyncFd::new` and related constructors violate I/O safety. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. None of the affected functions (tokio::io::unix::AsyncFd::new, tokio::io::unix::AsyncFd::try_new, tokio::io::unix::AsyncFd::try_with_interest, tokio::io::unix::AsyncFd::with_interest) is named in the audited code: the advisory does not apply unless they are reached indirectly (traits, macros, other dependencies).

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0386
```

**Evidence.**

_tool_output · [OSV.dev RUSTSEC-2026-0386](https://osv.dev/vulnerability/RUSTSEC-2026-0386) · manifest · SHA-256 1ebb594fd9923dc03209b41738d3f9cf8f324941e8844709473c643cd247e8b6_

```
{"id": "RUSTSEC-2026-0386", "aliases": [], "modified": "2026-10-23T14:45:03.847864944Z", "summary": "`AsyncFd::new` and related constructors violate I/O safety", "severity": null, "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Triage the advisory; upgrade to a fixed version (1.51.6, 1.53.3) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-04399 — No post-quantum capable cryptographic library detected

- Severity: **Info** · Classification: Insufficient data · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `dependencies`
- Data source: dependency manifests
- Detection method: Dependency name matching.
- Analyzer: dependencies 1.2.0 · 2026-10-28 12:22 UTC
- Priority score: 12.2 / 100
- CVSS v3.1: not applicable

Across 50 dependency manifests, QSI found crypto libraries (openssl, ring, rustls) but none from its PQC-capable list.

**Potential impact.** Readiness indicator only: PQC support may come from the platform (OpenSSL, OS, cloud KMS) rather than application dependencies.

**Reproduction steps.**

```
Review the dependency manifests listed in the evidence.
```

**Evidence.**

_dependency · Cargo.lock, Cargo.toml, crates/bin/cairo-compile/Cargo.toml, crates/bin/cairo-execute/Cargo.toml, crates/bin/cairo-format/Cargo.toml, crates/bin/cairo-run/Cargo.toml, crates/bin/cairo-size-profiler/Cargo.toml, crates/bin/generate-syntax/Cargo.toml, crates/bin/get-lowering/Cargo.toml, crates/bin/sierra-compile/Cargo.toml, crates/bin/starknet-compile/Cargo.toml, crates/bin/starknet-sierra-compile/Cargo.toml, crates/bin/starknet-sierra-extract-code/Cargo.toml, crates/bin/starknet-sierra-upgrade-val · SHA-256 1980ed6357825cc444a27bc1b98985b873318b59d5a5fa25de06c96d7c8ef037_

```
Crypto libraries: openssl, ring, rustls. PQC support depends on the version for: openssl
```

**Limitations of the check.** Absence of evidence is not evidence of absence: system libraries and transitive dependencies may not be listed.

**Recommendation.** Confirm where PQC support will come from (TLS terminator, KMS/HSM, library upgrade).

**Retest procedure.** Re-scan after upgrades.

### QSI-2026-04400 — atomic-polyfill 1.0.3: informational advisory RUSTSEC-2023-0089 (unmaintained)

- Severity: **Info** · Classification: Improvement recommendation · Confidence: Low
- Affected asset: `dependency:crates.io/atomic-polyfill@1.0.3`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 12:22 UTC
- Priority score: 11.2 / 100
- CVSS v3.1: not applicable

OSV.dev lists RUSTSEC-2023-0089 for crates.io package atomic-polyfill at version 1.0.3 as informational (unmaintained): atomic-polyfill is unmaintained. It reports no vulnerability; an unmaintained package will not receive fixes for future ones.

**Potential impact.** No known vulnerability. Future security fixes may not be released.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2023-0089
```

**Evidence.**

_tool_output · [OSV.dev RUSTSEC-2023-0089](https://osv.dev/vulnerability/RUSTSEC-2023-0089) · manifest · SHA-256 0fcfb6f26f61ecb982bc38b6d6f12db7c77d0fc40bf9353a089129368e765f0f_

```
{"id": "RUSTSEC-2023-0089", "aliases": [], "modified": "2025-04-29T08:31:10Z", "summary": "atomic-polyfill is unmaintained", "severity": null, "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time.

**Recommendation.** Plan a move to a maintained alternative, or record the decision to keep it.

**Retest procedure.** Re-run the dependency scan after the change.


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
| **transaction and message signing** | ECDSA (2) | QSI-2026-04398 | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains adopt them |
| **role not determined** | ECDSA (4) | QSI-2026-04397 | Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it; introduce an abstraction layer for crypto-agility |

_Roles are judged from file paths, function names and the code around each match; review confirms them. Root-of-trust keys and wrapped keys come first: they are hard to replace or can be recorded today._
No readiness questionnaire was completed for this project.

### Quantum algorithms relevant to this inventory

| Quantum algorithm | Effect | Attack model | Inventoried algorithms (rows) | What it means for this audit |
|---|---|---|---|---|
| Shor's algorithm — elliptic-curve discrete logarithms | breaks | Q1 | ECDSA (10) | Elliptic-curve keys are expected to fall before RSA keys of comparable classical strength. On blockchains, coins whose public key is already on chain (reused addresses, pay-to-public-key and Taproot outputs) are exposed first; plan the move to post-quantum signatures and avoid key reuse in the meantime. |
| Grover's algorithm — key search and preimages | weakens (larger keys restore the margin) | Q1 | Keccak-256 (3) | Not a break. 256-bit keys (AES-256, ChaCha20) keep a comfortable margin; AES-128 meets NIST category 1, while some authorities ask for 256-bit keys in quantum-resistant contexts (see the AES-128 entry). Prefer 256-bit keys for long-lived data; 256-bit hashes need no change for preimage resistance. |
| Brassard–Høyer–Tapp — collision search | weakens (larger keys restore the margin) | Q1 | Keccak-256 (3) | 256-bit hashes (SHA-256, SHA3-256) remain adequate for collision resistance; 160-bit hashes are already weak classically (SHA-1 collisions are practical). Use 384/512-bit hashes where NIST categories 4–5 are required. |

_Effects: breaks — replace the algorithm; weakens — larger keys or outputs restore the margin; included in standard parameters — no action at standard parameter sets; only with superposition queries — not applicable to ordinary deployments._


## 9. Limitations and assumptions

- This report presents automated and documented analysis results for the stated scope. It is not a legal opinion, a certification or an attestation of compliance with any standard.
- z is a planning assumption chosen per risk profile, not a prediction. A cryptographically relevant quantum computer is not publicly known to exist today.

## 10. Remediation plan / Priorities for 30, 60 and 90 days

### 30 days

| Priority | ID | Action | Type | Closure criteria |
|---|---|---|---|---|
| P2 | QSI-2026-04420 | Upgrade zip to a fixed version (9.0.0). | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0369. |
| P2 | QSI-2026-04406 | Upgrade pulldown-cmark to a fixed version (0.13.5). | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0414. |
| P2 | QSI-2026-04408 | Upgrade quinn-proto to a fixed version (0.11.18). | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0340. |
| P2 | QSI-2026-04409 | Upgrade quinn-proto to a fixed version (0.11.18). | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0343. |
| P2 | QSI-2026-04418 | Upgrade zip to a fixed version (9.0.0). | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0367. |
| P2 | QSI-2026-04401 | Upgrade block-buffer to a fixed version (none published yet; see the advisory for mitigations). | root-cause fix | Dependency scan no longer reports GHSA-qwgh-2vcv-g2f7. |
| P2 | QSI-2026-04410 | Upgrade rustls to a fixed version (0.23.45). | root-cause fix | Dependency scan no longer reports GHSA-2mjx-qc3c-rqvc (RUSTSEC-2026-0285). |
| P2 | QSI-2026-04411 | Upgrade rustls to a fixed version (0.23.46, 0.24.0-dev.2). | root-cause fix | Dependency scan no longer reports GHSA-c8m5-c952-6cm4 (RUSTSEC-2026-0346). |
| P2 | QSI-2026-04404 | Upgrade lru to a fixed version (0.16.3). | root-cause fix | Dependency scan no longer reports GHSA-rhfx-m35p-ff5j (RUSTSEC-2026-0002). |
| P2 | QSI-2026-04413 | Upgrade rustls to a fixed version (0.23.46, 0.24.0-dev.2). | root-cause fix | Dependency scan no longer reports GHSA-w44r-93j7-qv28 (RUSTSEC-2026-0349). |
| P2 | QSI-2026-04412 | Upgrade rustls to a fixed version (0.23.46, 0.24.0-dev.2). | root-cause fix | Dependency scan no longer reports GHSA-h2v8-394m-p7vv (RUSTSEC-2026-0348). |
### 60 days

| Priority | ID | Action | Type | Closure criteria |
|---|---|---|---|---|
| P3 | QSI-2026-04402 | Triage RUSTSEC-2026-0387; upgrade crypto-bigint to a fixed version (0.7.6) if it applies. | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0387, or the triage is recorded. |
| P3 | QSI-2026-04405 | Triage RUSTSEC-2026-0253; upgrade lru to a fixed version (0.18.2) if it applies. | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0253, or the triage is recorded. |
| P3 | QSI-2026-04407 | Triage RUSTSEC-2026-0338; upgrade quinn-proto to a fixed version (0.11.18) if it applies. | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0338, or the triage is recorded. |
| P3 | QSI-2026-04414 | Triage RUSTSEC-2026-0382 (CVE-2026-111943); upgrade rustls-webpki to a fixed version (0.103.16, 0.104.0-alpha.8) if it applies. | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0382 (CVE-2026-111943), or the triage is recorded. |
| P3 | QSI-2026-04415 | Triage RUSTSEC-2026-0308; upgrade salsa to a fixed version (0.28.5) if it applies. | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0308, or the triage is recorded. |
| P3 | QSI-2026-04417 | Triage RUSTSEC-2026-0383 (CVE-2026-111943); upgrade webpki-root-certs to a fixed version (0.26.11, 1.0.10) if it applies. | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0383 (CVE-2026-111943), or the triage is recorded. |
| P3 | QSI-2026-04419 | Triage RUSTSEC-2026-0368; upgrade zip to a fixed version (9.0.0) if it applies. | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0368, or the triage is recorded. |
| P3 | QSI-2026-04416 | Triage RUSTSEC-2026-0386; upgrade tokio to a fixed version (1.51.6, 1.53.3) if it applies. | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0386, or the triage is recorded. |
### 90 days

| Priority | ID | Action | Type | Closure criteria |
|---|---|---|---|---|
| P3 | QSI-2026-04398 | Add ECDSA usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-04397 | Add ECDSA usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P4 | QSI-2026-04398 | Plan migration of ECDSA to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-04397 | Plan migration of ECDSA to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-04403 | Replace derivative with a maintained alternative or record why it stays. | root-cause fix | derivative replaced, or the decision recorded. |
| P4 | QSI-2026-04400 | Replace atomic-polyfill with a maintained alternative or record why it stays. | root-cause fix | atomic-polyfill replaced, or the decision recorded. |

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
19. OSV advisory GHSA-2mjx-qc3c-rqvc — OSV.dev. <https://osv.dev/vulnerability/GHSA-2mjx-qc3c-rqvc> (modified 2026-10-27T15:30:05.509305490Z)
20. OSV advisory GHSA-c8m5-c952-6cm4 — OSV.dev. <https://osv.dev/vulnerability/GHSA-c8m5-c952-6cm4> (modified 2026-10-27T16:15:05.354395696Z)
21. OSV advisory GHSA-h2v8-394m-p7vv — OSV.dev. <https://osv.dev/vulnerability/GHSA-h2v8-394m-p7vv> (modified 2026-10-27T16:15:05.337819489Z)
22. OSV advisory GHSA-qwgh-2vcv-g2f7 — OSV.dev. <https://osv.dev/vulnerability/GHSA-qwgh-2vcv-g2f7> (modified 2026-08-19T19:30:06.686866977Z)
23. OSV advisory GHSA-rhfx-m35p-ff5j — OSV.dev. <https://osv.dev/vulnerability/GHSA-rhfx-m35p-ff5j> (modified 2026-09-10T03:50:59.064354050Z)
24. OSV advisory GHSA-w44r-93j7-qv28 — OSV.dev. <https://osv.dev/vulnerability/GHSA-w44r-93j7-qv28> (modified 2026-10-27T16:15:05.340347056Z)
25. OSV advisory RUSTSEC-2023-0089 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2023-0089> (modified 2025-04-29T08:31:10Z)
26. OSV advisory RUSTSEC-2024-0388 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2024-0388> (modified 2024-11-10T13:34:40Z)
27. OSV advisory RUSTSEC-2026-0253 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0253> (modified 2026-08-11T11:15:06.101553049Z)
28. OSV advisory RUSTSEC-2026-0308 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0308> (modified 2026-09-24T14:45:04.873565398Z)
29. OSV advisory RUSTSEC-2026-0338 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0338> (modified 2026-10-12T18:15:01.969514645Z)
30. OSV advisory RUSTSEC-2026-0340 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0340> (modified 2026-10-12T18:15:01.975478256Z)
31. OSV advisory RUSTSEC-2026-0343 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0343> (modified 2026-10-12T18:15:01.961745820Z)
32. OSV advisory RUSTSEC-2026-0367 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0367> (modified 2026-10-16T23:30:02.392172556Z)
33. OSV advisory RUSTSEC-2026-0368 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0368> (modified 2026-10-16T23:30:02.383750571Z)
34. OSV advisory RUSTSEC-2026-0369 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0369> (modified 2026-10-16T23:30:02.387698467Z)
35. OSV advisory RUSTSEC-2026-0382 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0382> (modified 2026-10-21T00:55:56.763143468Z)
36. OSV advisory RUSTSEC-2026-0383 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0383> (modified 2026-10-21T06:30:02.691648061Z)
37. OSV advisory RUSTSEC-2026-0386 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0386> (modified 2026-10-23T14:45:03.847864944Z)
38. OSV advisory RUSTSEC-2026-0387 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0387> (modified 2026-10-24T03:45:02.365137418Z)
39. OSV advisory RUSTSEC-2026-0414 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0414> (modified 2026-10-28T09:00:02.341043798Z)
40. P. W. Shor — Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms on a Quantum Computer (SIAM J. Comput., 1997) — SIAM. <https://doi.org/10.1137/S0097539795293172> (peer-reviewed article)
41. R. Babbush et al. — Securing Elliptic Curve Cryptocurrencies against Quantum Vulnerabilities: Resource Estimates and Mitigations (arXiv:2603.28846) — arXiv. <https://arxiv.org/abs/2603.28846> (preprint (2026-03-30, v2 2026-04-15): 256-bit ECDLP with < 1200 logical qubits and < 90 M Toffoli gates (or < 1450 and < 70 M); < 500,000 physical qubits at 10^-3 error, minutes)
42. S. Jaques, M. Naehrig, M. Roetteler, F. Virdia — Implementing Grover oracles for quantum key search on AES and LowMC (EUROCRYPT 2020; arXiv:1910.01700) — Springer / arXiv. <https://arxiv.org/abs/1910.01700> (peer-reviewed article: lower cost estimates for the AES key searches that define the NIST categories)

## Appendices: Cryptographic inventory

| Algorithm | Parameter | Library | Location | Quantum status | Classical status |
|---|---|---|---|---|---|
| Keccak-256 | Keccak-256 |  | crates/cairo-lang-semantic/src/types.rs:23 | Grover: acceptable to NIST, below ECCG/ANSSI guidance | acceptable |
| Keccak-256 | Keccak-256 |  | crates/cairo-lang-sierra/src/ids.rs:4 | Grover: acceptable to NIST, below ECCG/ANSSI guidance | acceptable |
| Keccak-256 | Keccak-256 |  | crates/cairo-lang-starknet-classes/src/keccak.rs:2 | Grover: acceptable to NIST, below ECCG/ANSSI guidance | acceptable |
| Crypto library | 0.10.81 | openssl (OpenSSL) | Cargo.lock | n/a | acceptable |
| Crypto library | 0.17.14 | ring (ring (Rust)) | Cargo.lock | n/a | acceptable |
| Crypto library | 0.23.43 | rustls (rustls) | Cargo.lock | n/a | acceptable |
| Crypto library | 0.10.73 | openssl (OpenSSL) | Cargo.toml | n/a | acceptable |
| Crypto library | workspace | openssl (OpenSSL) | crates/bin/starknet-sierra-upgrade-validate/Cargo.toml | n/a | acceptable |
| ECDSA | secp256k1 |  | crates/cairo-lang-runner/src/casm_run/mod.rs:41 | vulnerable (Shor) | acceptable |
| ECDSA | P-256 |  | crates/cairo-lang-runner/src/casm_run/mod.rs:42 | vulnerable (Shor) | acceptable |
| ECDSA | secp256k1 |  | crates/cairo-lang-sierra/src/extensions/modules/starknet/mod.rs:24 | vulnerable (Shor) | acceptable |
| ECDSA | P-256 |  | crates/cairo-lang-sierra/src/extensions/modules/starknet/mod.rs:25 | vulnerable (Shor) | acceptable |
| ECDSA | secp256k1 |  | crates/cairo-lang-sierra/src/extensions/modules/starknet/secp256.rs:3 | vulnerable (Shor) | acceptable |
| ECDSA | P-256 |  | crates/cairo-lang-sierra/src/extensions/modules/starknet/secp256.rs:4 | vulnerable (Shor) | acceptable |
| ECDSA | secp256k1 |  | crates/cairo-lang-sierra/src/extensions/modules/starknet/secp256k1.rs:24 | vulnerable (Shor) | acceptable |
| ECDSA | P-256 |  | crates/cairo-lang-sierra/src/extensions/modules/starknet/secp256r1.rs:24 | vulnerable (Shor) | acceptable |
| ECDSA | secp256k1 |  | crates/cairo-lang-starknet-classes/src/felt252_serde.rs:11 | vulnerable (Shor) | acceptable |
| ECDSA | P-256 |  | crates/cairo-lang-starknet-classes/src/felt252_serde.rs:12 | vulnerable (Shor) | acceptable |

## Appendices: Input files

| File | Size | SHA-256 | Redactions |
|---|---|---|---|
| Cargo.lock | 125405 | `afaf48f30a42c610b766e6dcb06e68203d45e43c2f339bb882e0c6a03c2895f3` | 0 |
| Cargo.toml | 5333 | `4df1342b05c0d893010469be852f60c02d3829234da4e047393f1a4a89c76a02` | 0 |
| crates/bin/cairo-compile/Cargo.toml | 745 | `824cbadd1ac84f537ec2daf506eb0d9f63385e33e051c26dd25190ed002eff7c` | 0 |
| crates/bin/cairo-compile/src/main.rs | 2696 | `030cf60d8a534d663a8ad398b94c636fd3dc7dddbd6205466a11858f604f0f3c` | 0 |
| crates/bin/cairo-execute/Cargo.toml | 1131 | `0b7a69d84c623c1ac8fec351caaaf6017c91ce06a10f51d3708af43e223d0346` | 0 |
| crates/bin/cairo-execute/src/main.rs | 18076 | `e219a06602c041ea9808603f6ab977ec8d8895fbf45c19c1f243e1edd4fb8782` | 0 |
| crates/bin/cairo-format/Cargo.toml | 625 | `4df498087b2446916e7acc7590a7e447785c26f8448b8283c0a33904b289fa8c` | 0 |
| crates/bin/cairo-format/src/main.rs | 7798 | `a57c37c2692016394a1fac7099d939af6bf40d382a62d262750978cebe720786` | 0 |
| crates/bin/cairo-run/Cargo.toml | 872 | `e57a13f381ca79ac62689fb9bf505f42d65d8d39985ac3c44f829250e192f4d2` | 0 |
| crates/bin/cairo-run/src/main.rs | 5709 | `682584923a2e7b6f0771600966da3ff4d777c58101a200665441aad59cb9ed71` | 0 |
| crates/bin/cairo-size-profiler/Cargo.toml | 1632 | `08cd0c5b2ba09157ce4dbce0d4ec7b7402c90a5e6900750cdeeba7fffb3b9caa` | 0 |
| crates/bin/cairo-size-profiler/src/main.rs | 10510 | `feb0d747a61fbea953b534dd837470676ef70b119d3fc1c3e3161a0127027688` | 0 |
| crates/bin/generate-syntax/Cargo.toml | 416 | `389238bb35848ac3dcc7a30674dc2392678f67a30a713d86f319eb37c21823b3` | 0 |
| crates/bin/generate-syntax/src/main.rs | 381 | `2beb19a7d0b697c788286ab8a660190de330f1ed9f195c1434fb4ef6ab0920c1` | 0 |
| crates/bin/get-lowering/Cargo.toml | 1310 | `ef9abc3b48e904666ecbeab399abdc333a8cb87b9253e64d886107f17d58c0f2` | 0 |
| crates/bin/get-lowering/src/main.rs | 12193 | `e0b74b87a0fb1d88d3da807a455afac6e223bba37fdc80b3bb3ebbe84accf5c2` | 0 |
| crates/bin/sierra-compile/Cargo.toml | 812 | `9f4acba2e68a2a2954656e8a1ed69da0944e25dbd9eac141c3faf8d5ddb623fc` | 0 |
| crates/bin/sierra-compile/src/main.rs | 1928 | `4bd96f8e455cd35580518555b93a212750a93497f97db3fb22b74896fdb01e4e` | 0 |
| crates/bin/starknet-compile/Cargo.toml | 720 | `52ec2ca0cfac91e682978cb181819244f8aac806e9725ca3c385ee24a0bffb73` | 0 |
| crates/bin/starknet-compile/src/main.rs | 2879 | `5674b13d82ad3318c72c7b24a4f8daa4e2e8559790c9c34198da0b56a45d4c69` | 0 |
| crates/bin/starknet-sierra-compile/Cargo.toml | 763 | `b245d1e68b405eaeb6dcb4b0f90e7facd069d8913a4a64b58b09d205c4c07039` | 0 |
| crates/bin/starknet-sierra-compile/src/main.rs | 3149 | `14b41282cdcb1c5001cc22d55e2aa33ed90180a995af09c44c8d8d8fa5f37f8d` | 0 |
| crates/bin/starknet-sierra-extract-code/Cargo.toml | 534 | `4fb45462968ab82d980b4cdd071e0143892cfd3ecfea04eb403131adec40a2c8` | 0 |
| crates/bin/starknet-sierra-extract-code/src/main.rs | 1255 | `b5965f0e1d93d9909213cc9bf8dae4106f5971bde672be9abbb4094cfec5f517` | 0 |
| crates/bin/starknet-sierra-upgrade-validate/Cargo.toml | 1043 | `e0fb965ff51f06756aa2469c4e0439ebbfa74e99c90edec8d211675dbbfca957` | 0 |
| crates/bin/starknet-sierra-upgrade-validate/src/main.rs | 24474 | `2de6e8071de90fbebda78e6911339ba98a1d4d3a73dbfe6550b880c44518a8f4` | 0 |
| crates/cairo-lang-casm/Cargo.toml | 1157 | `ea552c74e97678a83934c352d40d5f7fcc6d5c0fd57875e0059e49e322cde86c` | 0 |
| crates/cairo-lang-casm/src/ap_change.rs | 4402 | `22e27ef0a9837285073b7ef657118eac32d8f0e33bca9a3c7d6746c2b2e0cecb` | 0 |
| crates/cairo-lang-casm/src/assembler.rs | 11348 | `11b70ff281ebde844f6bc0ea0a4a20cd327aafe7980b10987a2639bf2d78aec9` | 0 |
| crates/cairo-lang-casm/src/builder.rs | 43291 | `760f1cd450f3581b9efa4e3b0d8302be6e987990b6b699a2006c7dabdadd62c6` | 0 |
| crates/cairo-lang-casm/src/cell_expression.rs | 5178 | `62eadf9d821f94a4237ef5c0de4deec5e14d06531090eaeb671ba8a74f33f22d` | 0 |
| crates/cairo-lang-casm/src/encoder.rs | 4308 | `3a847ebfe4e8915235a5fca1b07b22bd1a430ee23c2719b87bec1e597ae82d24` | 0 |
| crates/cairo-lang-casm/src/hints/mod.rs | 37691 | `b20a3bb3d29fdaf7388fae70ec6208af59e1f121bdd6c7fd8144b7638974a9b7` | 0 |
| crates/cairo-lang-casm/src/inline.rs | 13207 | `15ecd50d7b5017f36de351e134face2c34e4516a85d2d9c32cff34a312e50707` | 0 |
| crates/cairo-lang-casm/src/instructions.rs | 6975 | `20797f3124c1feb700e86affab285ae722ee587bc9a84c318a10aa633d486aa7` | 0 |
| crates/cairo-lang-casm/src/lib.rs | 360 | `82c4240add8e990d62cd458398f111331de26bc78be7d38bc0cf3904823ffcc5` | 0 |
| crates/cairo-lang-casm/src/operand.rs | 5392 | `b0ab13c05e4a3c55152dc171aa8c6c921fd4a0138c8ac4c1dc5efa64acfb3ec5` | 0 |
| crates/cairo-lang-compiler/Cargo.toml | 1352 | `210db0b4cacc6000381bb3ed13cdd2a36f0d6cef28eeb34e42070c1613b886fe` | 0 |
| crates/cairo-lang-compiler/src/db.rs | 8614 | `771bb1082ed2f9a2fe47149fc557c02e99cb9f5e023b33e8e805836cf57b7d00` | 0 |
| crates/cairo-lang-compiler/src/diagnostics.rs | 11142 | `63434f06c1ccd42694618825e105f3e341e33b4e7adaaf744515ca3e1cdf3b4e` | 0 |
| crates/cairo-lang-compiler/src/lib.rs | 16895 | `75a24dd98333f88a5f0968c50013f43d76c51292fbbe0c7d6d3d8f4c20308843` | 0 |
| crates/cairo-lang-compiler/src/project.rs | 6212 | `5f2cbd7bd3bf374e12d6ba0b1bdc4359b26940f769f2f7fe169a13f9f72e3b6b` | 0 |
| crates/cairo-lang-debug/Cargo.toml | 552 | `f179b3d54b6aed01a71b64d463c25e14d01fd69800beaa76c738caf2fa2e68d1` | 0 |
| crates/cairo-lang-debug/src/debug.rs | 8539 | `12f7b5efd57aad97277639ae83045d584ccb521d8bc64a37fe345dc08aa2128c` | 0 |
| crates/cairo-lang-debug/src/lib.rs | 134 | `6db717119bad90e961d428dbbf650470d6742d42f11c850907a0e878fa118ddb` | 0 |
| crates/cairo-lang-defs/Cargo.toml | 1231 | `62dc4a2baa7da766e30e4408e9a7e7234fbeb3b9abac4893141273001471f861` | 0 |
| crates/cairo-lang-defs/src/cache/mod.rs | 88814 | `e9b19f19fbffba645de83ee79949c52a863ea67dea14fa35015ce361baf23820` | 0 |
| crates/cairo-lang-defs/src/db.rs | 77856 | `dcda77a40d2de9381c0734cf867c1cf62bc7641da2c865cd7fd6bb46475978eb` | 0 |
| crates/cairo-lang-defs/src/diagnostic_utils.rs | 3231 | `6f25738e325116ed65aac3b3cef4467f1a5574a1a83a0438c024f2f5b2566aca` | 0 |
| crates/cairo-lang-defs/src/ids.rs | 57051 | `149574dd264f072bb6c3a75d2be69ac3c4cd7d304c9b4fbb622f835c3a22a3cb` | 0 |
| crates/cairo-lang-defs/src/lib.rs | 331 | `3a751df9731e19e9831cfca8fbce13736f158134ebbc8ca78cefcaf1b106776c` | 0 |
| crates/cairo-lang-defs/src/patcher.rs | 13336 | `41b671f2542bb802b0402485884f6edb18b60da8081412519127b6039bb07006` | 0 |
| crates/cairo-lang-defs/src/plugin.rs | 9361 | `f9ee397d4705da5eff87d4a5317599535d0835c9d6beec9ea148fba5de27ad17` | 0 |
| crates/cairo-lang-defs/src/plugin_utils.rs | 8562 | `7114978b10f5eb7fa29c04c27bed72eb3163c220564e5f2dc8b720e4fa757a87` | 0 |
| crates/cairo-lang-defs/src/stable_order.rs | 4454 | `22b1155e82f8b9a945a51930f8916a1ed68713f881d1e886e422d32c226edd65` | 0 |
| crates/cairo-lang-diagnostics/Cargo.toml | 812 | `60fdbfacb1903bea67d204675fbfedff4ba1c38ca6b4b1cadad84cfaf6c3e40c` | 0 |
| crates/cairo-lang-diagnostics/src/diagnostics.rs | 14320 | `04ce38d55b23cc16b209fba0f3d2329ec43abb71770f21e3ccc3bafccdc51948` | 0 |
| crates/cairo-lang-diagnostics/src/error_code.rs | 2342 | `ff3b0a2276aeea4c8ebed7194ed9ecd7380eff4be786e643941ab9e868023c03` | 0 |
| crates/cairo-lang-diagnostics/src/lib.rs | 493 | `f5ccf1a38ab4b5b45ced31bffef7beb9e52ff8148260e2a31bd5f3fee805e77c` | 0 |
| crates/cairo-lang-doc/Cargo.toml | 1292 | `2c6c33eb61fdac82273ccc975e443d120c6bf0f8e348fa95b0505d9aba791109` | 0 |
| crates/cairo-lang-doc/src/db.rs | 11610 | `d91930171b6254904fb8470e598174190ed149b617081c56606296c3f6ec2537` | 0 |
| crates/cairo-lang-doc/src/documentable_formatter.rs | 29966 | `225519d3aaba9fca3e13863c920ad92889dfc09967695b298f45c4c21ab9a7f4` | 0 |
| crates/cairo-lang-doc/src/documentable_item.rs | 2281 | `b5f008ac9dd2b77cc2240aa1e85a15e0c5fe184c3e9ee5c3a5f9f7bf423c6a99` | 0 |
| crates/cairo-lang-doc/src/helpers.rs | 26774 | `f8140b146a3c8cc3d62d8c3f8f38146e4d67d519ccccdfcc32f1d4f6585f83b2` | 0 |
| crates/cairo-lang-doc/src/lib.rs | 203 | `cf6fa016b5838f157783bb2835742595ff68104bc5385b3b40a027a5fd57e69b` | 0 |
| crates/cairo-lang-doc/src/location_links.rs | 6446 | `e28cc9bd0932e8fc0e1b06d7aa2d552bd4b317c3144d1e6b108e4bdcd5ac6aeb` | 0 |
| crates/cairo-lang-doc/src/parser.rs | 18328 | `5fd4580addf52c253243710f51db1882dee3198233b9fc41a6936733b1592c4c` | 0 |
| crates/cairo-lang-doc/src/signature_data.rs | 24761 | `59277adfe9e188f2d80fdab7a90a8507bc7f1a55de394b0117313531b4423545` | 0 |
| crates/cairo-lang-doc/src/signature_errors.rs | 1479 | `502b9ab7cdf3cd7dda501fd40e2410273f68bdf627fa1c4296962665c1c342e4` | 0 |
| crates/cairo-lang-eq-solver/Cargo.toml | 473 | `6497a4901045844f2596e6807dfebcf429bfa1dd357da105306d8cb33b5fffb0` | 0 |
| crates/cairo-lang-eq-solver/src/expr.rs | 2023 | `ee026898443d81881f9537402b1fc05ac4081e50497ee1fbae103a15a64280c6` | 0 |
| crates/cairo-lang-eq-solver/src/lib.rs | 4380 | `7f062f8b517c533bb1e665f6055948168f720856b88bf796ed2250ea78fcd1e8` | 0 |
| crates/cairo-lang-executable/Cargo.toml | 1772 | `d1531c4e88f054b937b9cb7e503af83125c65645691de6613d70f45ea4b51a50` | 0 |
| crates/cairo-lang-executable/src/compile.rs | 10178 | `04cbd281e177bb6a0abf6a0ad7f5967eddd40ba8646c507e7e5991b9360f5adc` | 0 |
| crates/cairo-lang-executable/src/debug_info.rs | 2341 | `cf9161042c88e723361772cfbaa765724d85c372eee3708286706c5ae4999405` | 0 |
| crates/cairo-lang-executable/src/executable.rs | 3255 | `f29282d4022b9bc221ec2977b0e5acf7326d79f8b082e667f00fa93d6605be4d` | 0 |
| crates/cairo-lang-executable/src/lib.rs | 78 | `f90f222945c23a9ed5cf6fa81e612514fe592b434b78bd6687354a7fd35f7be1` | 0 |
| crates/cairo-lang-executable-plugin/Cargo.toml | 1086 | `5658a87167a22cd18bc848be57f3c04ae851ec8a2cfb791fa93727f845575571` | 0 |
| crates/cairo-lang-executable-plugin/src/lib.rs | 9302 | `391107d0bca32107336a7988582cf84c70d9d580fc70548ea63d8774e343fe6c` | 0 |
| crates/cairo-lang-execute-utils/Cargo.toml | 643 | `ba24ec61910b15a0c6473ef3fd1d0498a277858ad3f2d85d3d79c15484c66232` | 0 |
| crates/cairo-lang-execute-utils/src/lib.rs | 2728 | `a3328710869fc4071cb96292eb220a134784af68e08c6e935ba182d2bb18f08b` | 0 |
| crates/cairo-lang-filesystem/Cargo.toml | 957 | `64c4de286eee1585a0677f5b4b5c71a3e523524a142a0f7cfd7ebc3fd9a97b7e` | 0 |
| crates/cairo-lang-filesystem/src/cfg.rs | 5922 | `5dfa893eca474663a9edce475cb420a4237c58ab9c11bea506282404903617ae` | 0 |
| crates/cairo-lang-filesystem/src/db.rs | 26180 | `e9560e660025d8519c749c8ca2e16a03b8382cde576fbaa8be8b3d428d3559db` | 0 |
| crates/cairo-lang-filesystem/src/detect.rs | 865 | `e0a29d2945ce78e3a663cc8c9d4d9a2c399ccf8706ccef896559db8b5e4a0c3c` | 0 |
| crates/cairo-lang-filesystem/src/flag.rs | 5722 | `041ee696f404c616b75a24bbf6ad7420bdcb58631b6e016d2adc6bfdf0a7a809` | 0 |
| crates/cairo-lang-filesystem/src/ids.rs | 19041 | `9803c7b29b7e9225479088c55212134263efd212965784bde9bf90167f7d8841` | 0 |
| crates/cairo-lang-filesystem/src/lib.rs | 162 | `c08f14e13a5556d9b910ac52e4512968a43dd89f48b08912936911c7e55d7eb2` | 0 |
| crates/cairo-lang-filesystem/src/location_marks.rs | 4360 | `503db8406bad9e467a22f2e56c1bc5a91be6102154bff43370603f04fc4e2b19` | 0 |
| crates/cairo-lang-filesystem/src/span.rs | 8540 | `a430cc45addeefa8d64a6aba8cc33456bff165f981106decce2cbe65cd2d2145` | 0 |
| crates/cairo-lang-formatter/Cargo.toml | 931 | `ba6979b9b6799a00aa16c4ad2af948e56431c7ce57512a7eac573e970714d608` | 0 |
| crates/cairo-lang-formatter/src/cairo_formatter.rs | 9087 | `540ac75b48a0e14a79173317e1d8065d5f664e22db0db9d788e3f9481f457723` | 0 |
| crates/cairo-lang-formatter/src/formatter_impl.rs | 66995 | `3400918b8a7acd3a297db9cede1e7d66c7f5b289369e0f87946dffd691b64663` | 0 |
| crates/cairo-lang-formatter/src/lib.rs | 6049 | `73c35422e63e80f7b215687cbea6b1b7f49cdad4ba282662af7416b9b6b855ea` | 0 |
| crates/cairo-lang-formatter/src/node_properties.rs | 50675 | `57e5af74d68de2d4baf795f1ab6ec1c380af8eafba426867f9b639e657602433` | 0 |
| crates/cairo-lang-lowering/Cargo.toml | 1736 | `107702ddb74605781441e73d27f4a2a44980a87edd1157542a21f8655a89fbb3` | 0 |
| crates/cairo-lang-lowering/src/add_withdraw_gas/mod.rs | 4841 | `d29fac5c4bd5a25ebdb37bf38c0e615cec0b9f7cb58a4a2f79384a90cf2811ba` | 0 |
| crates/cairo-lang-lowering/src/analysis/backward.rs | 8996 | `345420cb955a8fd475d95efd16a3efaf77e8da428abd03232a9c8dc72c21b219` | 0 |
| crates/cairo-lang-lowering/src/analysis/core.rs | 7631 | `36daa787393b670fc9ebb5c94b0bf7ed7ba8885160c99bb86edda607e11c12b7` | 0 |
| crates/cairo-lang-lowering/src/analysis/def_site.rs | 4250 | `76fde60eed2cac9f793f9fa5c3ad81207bfe490541722353bb10cc406022c0bd` | 0 |
| crates/cairo-lang-lowering/src/analysis/dominator.rs | 3090 | `9d7db76b93adf03691f0eb028426a88f4380d7f5afac59446b55a6fac867ae9d` | 0 |
| crates/cairo-lang-lowering/src/analysis/equality_analysis.rs | 43371 | `162c2d54105a66a8a26f5ba57766deaf020b553dc5c16f265c08fa1eb0f31fc7` | 0 |
| crates/cairo-lang-lowering/src/analysis/forward.rs | 5911 | `726dfa12e1e0fef5757efcd34bf289496eeaa1e8d96a465bf59db7063c6fbe83` | 0 |
| crates/cairo-lang-lowering/src/analysis/mod.rs | 3726 | `d5aea227fce022d21414051dbcda16e1a7daf85dfad0a968b0b87e48c47c01bb` | 0 |
| crates/cairo-lang-lowering/src/analysis/topological_order.rs | 1883 | `c8d0ed6a85140d261dd616101c79f36ab1bdd975f41daea9ba583e1a2ea87c4a` | 0 |
| crates/cairo-lang-lowering/src/analysis/use_sites.rs | 4194 | `a864e2433bcba8b874b1917a2ce19c09c4a55aec5c9e6bf66701d0c283005f4e` | 0 |
| crates/cairo-lang-lowering/src/borrow_check/demand.rs | 5583 | `4d3fe12453e1c8ba970b776b467e001322dacbff9f3e16c39b9f5d14e060d3fe` | 0 |
| crates/cairo-lang-lowering/src/borrow_check/mod.rs | 13215 | `8b4e1d40b93b9677bb8f4b8fce1b2ae859f7649b77511ee11dcc39f3e78aeb21` | 0 |
| crates/cairo-lang-lowering/src/cache/mod.rs | 47940 | `b19a1e05de005add7bf7c9def38c140c697c9d5f0e668d891b30de502a1dd159` | 0 |
| crates/cairo-lang-lowering/src/concretize/mod.rs | 3441 | `0c6eecbf3076c362dea7c2f9cd0d14791803bdb71c1ce594123ade83c351bab3` | 0 |
| crates/cairo-lang-lowering/src/db.rs | 34220 | `af066a3e5c236536aaddf33bd128bca08aa3a3b8ff15e36238b127df5e4acd62` | 0 |
| crates/cairo-lang-lowering/src/destructs.rs | 23205 | `d6e853d7aec164de87632aa6ce285e009d425336565af3e688521b2f5edc55c7` | 0 |
| crates/cairo-lang-lowering/src/diagnostic.rs | 11376 | `0b435713634379f819c4333bf2e2a923d13cec3a4b9264af689d5bff17b5b891` | 0 |
| crates/cairo-lang-lowering/src/fmt.rs | 12196 | `59a177f69e262b87cd93ec3704a3b575a357be619a77b7a7a5fd595e09609605` | 0 |
| crates/cairo-lang-lowering/src/graph_algorithms/concrete_function_node.rs | 1477 | `6a55cf331291d860b32c110549a8bdda5624a7bd65bb6ca67d74e0efe17f1620` | 0 |
| crates/cairo-lang-lowering/src/graph_algorithms/cycles.rs | 3455 | `7749745db5f2c4713674c4a0235979531a23904da3903436d35fde4015fea736` | 0 |
| crates/cairo-lang-lowering/src/graph_algorithms/feedback_set.rs | 1949 | `dbc0b6c5f448f4a518d66625da90b1cd64be3dd18df91cc35df0c8e5c0ebf52c` | 0 |
| crates/cairo-lang-lowering/src/graph_algorithms/mod.rs | 109 | `80071fcfac46f961acb7f6803895b2551247f79ca12d467346bea6e81b77e5c6` | 0 |
| crates/cairo-lang-lowering/src/graph_algorithms/strongly_connected_components.rs | 4711 | `6fabe78161fed54ff70673c392a4676cbdd6d32d40b91a64bd78163b239f45d1` | 0 |
| crates/cairo-lang-lowering/src/ids.rs | 29037 | `540602eaede9f37a6641cf292e25f8f70c93852d74f4e408fffe75a5d46bac5d` | 0 |
| crates/cairo-lang-lowering/src/implicits/mod.rs | 13596 | `14392c0bdb472a52e3a2377351489e0130b393a89c7251097a6bfd02706c9570` | 0 |
| crates/cairo-lang-lowering/src/inline/mod.rs | 14922 | `9216e210ede3060deb0dab0e58dfaa7cd4b5ddf9f038d38e47200366b1b89bb4` | 0 |
| crates/cairo-lang-lowering/src/inline/statements_weights.rs | 4140 | `9447c76cdeed14932ecd804da36dbf69a81c7ddeffe5ac935b7b4cc7a20fe9a2` | 0 |
| crates/cairo-lang-lowering/src/lib.rs | 594 | `b84d1165ba24e0c4ecfca2c39029a7907b253bafa3c3aed31a2edb850649af69` | 0 |
| crates/cairo-lang-lowering/src/lower/block_builder.rs | 24323 | `78e2e096e120a396c5627ec16349feedfcb40ee3bdb5194be6000de0cd64e729` | 0 |
| crates/cairo-lang-lowering/src/lower/context.rs | 20019 | `0132d0571e95ac27ebd8da8d276e79bdde2c8a1da1f10a1041d45756980c2e31` | 0 |
| crates/cairo-lang-lowering/src/lower/external.rs | 1904 | `113ba121828e68edc3b44818ce641a13b744c7a8ae238c8d8a1cb8e3b95c0bb6` | 0 |
| crates/cairo-lang-lowering/src/lower/flow_control/create_graph/cache.rs | 1341 | `f0de5627e4a05cac42c852a76fd370a7e9e81423940425554acd88cd6118a931` | 0 |
| crates/cairo-lang-lowering/src/lower/flow_control/create_graph/filtered_patterns.rs | 5881 | `dd755be7b3df06c042c0a8ab3211d29cbdcb7e950e58fad011927b360c697cb4` | 0 |
| crates/cairo-lang-lowering/src/lower/flow_control/create_graph/patterns.rs | 42185 | `7a91e3f2276a94e2ba28991076c6fae7ebd1f93bc78f0947f82c6fb028271288` | 0 |
| crates/cairo-lang-lowering/src/lower/flow_control/create_graph.rs | 10966 | `be3372a9795ced5aca33701e141978c3c4fba413500f6d4e2bea2ea4fcdb2b83` | 0 |
| crates/cairo-lang-lowering/src/lower/flow_control/graph.rs | 18163 | `358bc820ba4be18eb2517a6950813993e34f1976a7132afd34791a3dc9ad5ea6` | 0 |
| crates/cairo-lang-lowering/src/lower/flow_control/lower_graph/lower_node.rs | 25960 | `1ccf7d7eebb63b5a06231cd3369cce4f6330c111cfbec94e3a16273f680537a4` | 0 |
| crates/cairo-lang-lowering/src/lower/flow_control/lower_graph.rs | 11142 | `b8e1a4a2d10142014311eed4de567ca2fe706acb983cc7966ccb61bced1a59f0` | 0 |
| crates/cairo-lang-lowering/src/lower/flow_control/mod.rs | 84 | `f476c1199d0a460d721205320a51d0baf042da8fa17ce40094f1766f3e7290c4` | 0 |
| crates/cairo-lang-lowering/src/lower/generators.rs | 10428 | `10ed00c9417e32c382e41425f5e3f0aecef7027670899c6e5ff59cc097c18703` | 0 |
| crates/cairo-lang-lowering/src/lower/logical_op.rs | 3947 | `1e6c50dccd144076624233641b69ccb8a53af2f4c48e2da0be6ed0660d25d48b` | 0 |
| crates/cairo-lang-lowering/src/lower/lower_let_else.rs | 3781 | `a077e0507a2259c128af6eb31247d0723fba24a589713708ee92a16065701d3f` | 0 |
| crates/cairo-lang-lowering/src/lower/mod.rs | 93437 | `3a8d54ef9d1287bcc9dbe78595b290ebad631bf56a8e9d42db10a504011e8af7` | 0 |
| crates/cairo-lang-lowering/src/lower/refs.rs | 19875 | `e203fec60a9f53178234d222f64c257aeabd19ab7851df8fcbc433953e578fe1` | 0 |
| crates/cairo-lang-lowering/src/objects/blocks.rs | 4492 | `a54bd1e77c6720a7e753e7a6fe68c8ba15c2383d5a404da351ab3e5cc9c86fff` | 0 |
| crates/cairo-lang-lowering/src/objects.rs | 23944 | `e71434d45e4d5400ac352cef7b493ca4bd7e88894421fdfe68236e1c9bf83cb3` | 0 |
| crates/cairo-lang-lowering/src/optimizations/branch_inversion.rs | 2446 | `da9b78a2ada7d8a22b907011a650feb3195cc26d174360e0016caa5a5f7b88a8` | 0 |
| crates/cairo-lang-lowering/src/optimizations/config.rs | 4299 | `4cbb181749bffa80e954c8828d6ceb60a9973aee8cf58ae3daa9f8c33b88b2e6` | 0 |
| crates/cairo-lang-lowering/src/optimizations/const_folding.rs | 89030 | `f963183d32de175aff907ee71c5a7f1a55d99a8bb775faa15ca76002b5bee8ea` | 0 |
| crates/cairo-lang-lowering/src/optimizations/cse.rs | 8554 | `8f5f9ebde40b99c431f36090b11ab7f6425ad399ea2f4eaf92ca38f7c37937b0` | 0 |
| crates/cairo-lang-lowering/src/optimizations/dedup_blocks.rs | 13329 | `420052777a004cfa0c5a8187bc2d9b4c37a9d05be9409a6de7ec1d3102ee1c11` | 0 |
| crates/cairo-lang-lowering/src/optimizations/early_unsafe_panic.rs | 5924 | `52d9b2632f15cb6b4e2d9052e059fad3af68190aae7cc4d063757614fb899cec` | 0 |
| crates/cairo-lang-lowering/src/optimizations/gas_redeposit.rs | 6421 | `c196e3c0bd06d08810a557952bf4ab67583a28151ecb7a37772f1c72f1b98909` | 0 |
| crates/cairo-lang-lowering/src/optimizations/match_optimizer.rs | 26147 | `3bc67741ca9fefc6bbd2ee1cc88549682e1490ccf5356cc7cc2a8cfc682145c6` | 0 |
| crates/cairo-lang-lowering/src/optimizations/mod.rs | 825 | `ceeb9e8c4b3096e5f9576ce3a36f0ec74028eb7d65b39c438581d5937291eea2` | 0 |
| crates/cairo-lang-lowering/src/optimizations/reboxing.rs | 12366 | `8e2b466f50686363878e66dd7391bc46a23e44c1c4a28109ba3a03d9af96ee66` | 0 |
| crates/cairo-lang-lowering/src/optimizations/remappings.rs | 6065 | `6ee8c0899529a617e65bbd2a7bd7f8ceff72a970dfaf9a501b4775b872bed374` | 0 |
| crates/cairo-lang-lowering/src/optimizations/reorder_statements.rs | 7226 | `de86fe440ba7baa6c105d810230d8f7768dcf01637deb7b05c440ec84f78d87e` | 0 |
| crates/cairo-lang-lowering/src/optimizations/return_optimization.rs | 22739 | `850c997146705977a620ebbcd7374948b423a6433a4db7f3de1afcfa8483662d` | 0 |
| crates/cairo-lang-lowering/src/optimizations/scrub_units.rs | 1692 | `a10124a0defa610021319c981fe4bad9520279ca9a8964c022fb42b1b6221171` | 0 |
| crates/cairo-lang-lowering/src/optimizations/split_structs.rs | 14732 | `49a74015128e3cd7aac0772c699a0f4091a9e3937b79d7006ec6c7082379538e` | 0 |
| crates/cairo-lang-lowering/src/optimizations/strategy.rs | 11189 | `860728c9d8269e1b716474f595e2f85a889c2df2bd70597a50a529e3dd91e77e` | 0 |
| crates/cairo-lang-lowering/src/optimizations/trim_unreachable.rs | 2154 | `361f8c624b623dc8482d814fbdcea2cb9d2442d13e5d65c4bd7bf9ff246147f3` | 0 |
| crates/cairo-lang-lowering/src/optimizations/trim_unused_params.rs | 4944 | `647e3bd580b2671e235bf774d07c0ce07899cd6942ea283325b109485f5495a4` | 0 |
| crates/cairo-lang-lowering/src/optimizations/validate.rs | 6179 | `e4f34f8471a8235a77a2f89adc067d95cc39b4a7fa9b48e9cc3b9816dd35bab5` | 0 |
| crates/cairo-lang-lowering/src/optimizations/var_renamer.rs | 918 | `4c2a03c8851bd67107a675be487cba3e215a55c68f13ae1ba6966cf38b7142e7` | 0 |
| crates/cairo-lang-lowering/src/optimizations/variable_forwarding.rs | 17948 | `d250e0787b533301470676ad17bb8a26f4b1dfabd55790d2f1eda7de054366dc` | 0 |
| crates/cairo-lang-lowering/src/panic/mod.rs | 21240 | `0f3a6701ca47707828c44409dc985170c3a80c304fa09f7e7967819b047fa66b` | 0 |
| crates/cairo-lang-lowering/src/reorganize_blocks.rs | 7689 | `88adf4b47aedd29d8359a403df49f601b635f967d3c84c0df0e240c379815c7c` | 0 |
| crates/cairo-lang-lowering/src/scc/mod.rs | 1561 | `8f08018083244d298bc855405a993e9b1c46fc9dd7ebacd3575c69b712a8c35f` | 0 |
| crates/cairo-lang-lowering/src/specialization.rs | 15258 | `16f24c164cde153dfc910ab5adf9694e08bc1dafa627f19d525c3f81b2e1437e` | 0 |
| crates/cairo-lang-lowering/src/utils.rs | 9139 | `ed1ab606f286a95365f148c40f1d576c5270a63a772ba702581d53fcc1a64291` | 0 |
| crates/cairo-lang-parser/Cargo.toml | 1210 | `7b0e396f29d57b10e4e08f530473daa91c60a0ac62284040c5c54165b3a6ca22` | 0 |
| crates/cairo-lang-parser/src/colored_printer.rs | 5599 | `70f83bddc163ffe17a19a42a3e692920ec8f765b946120dcc30b80e9f248d70a` | 0 |
| crates/cairo-lang-parser/src/db.rs | 4956 | `91f1529a768976f5326e8605115c58b1f5cf9f08938ffd4d92c241cb8c747437` | 0 |
| crates/cairo-lang-parser/src/diagnostic.rs | 14620 | `36d7be6ff02bdc192c58ad06b0b79526d3ce939435d5a9b914926db8d81e3b70` | 0 |
| crates/cairo-lang-parser/src/lexer.rs | 18794 | `5d7a62104d7d151d39783c4be9f2794a9de2cb548a023d6e97d12c805ad0feff` | 0 |
| crates/cairo-lang-parser/src/lib.rs | 345 | `1e3e2962b7509b32b19ada12f5a2ce05fbef68a100dde9b63a0c605d149c7480` | 0 |
| crates/cairo-lang-parser/src/macro_helpers.rs | 5747 | `eadb6e26b0706911288793ad07c09d1e4878558065784bc55bc568042e7e4df2` | 0 |
| crates/cairo-lang-parser/src/operators.rs | 1605 | `ade5622a3bfeb02e7d8e9a5f3ebff7920c75e0a4d2c00f13c940f1a8e12f6ea1` | 0 |
| crates/cairo-lang-parser/src/parser.rs | 178412 | `f19287523a912436719202fa40a23f27d99457f02dbae36f88a28d6126dd2d94` | 0 |
| crates/cairo-lang-parser/src/printer.rs | 10308 | `9e61c1b2607b3ad3ae68d63cfccd918dd6dbd73777e16c8f2c1da26a350501d9` | 0 |
| crates/cairo-lang-parser/src/recovery.rs | 2409 | `af5246d49b6fdb6d0ae2bab50b059073be1af014badac8f24ccdb8d10bf28851` | 0 |
| crates/cairo-lang-parser/src/utils.rs | 7015 | `533efaff1a845c84988bae6c1ac1d465b44165d08ad7b9fa691d24f9d1ccc164` | 0 |
| crates/cairo-lang-parser/src/validation.rs | 5575 | `0f2efddc5d698410af4a2754844bb2b70c724d066562cf8094915dd2eb4d1681` | 0 |
| crates/cairo-lang-plugins/Cargo.toml | 1140 | `f6efde4f4a63f369332f42a755918c9cce2f63e3a4c9ce1f363ba3d66aa83db5` | 0 |
| crates/cairo-lang-plugins/src/lib.rs | 954 | `23705319b162a9884a2352a75cce43541db32fa65d253045dcee88af12ab920f` | 0 |
| crates/cairo-lang-plugins/src/plugins/compile_error.rs | 2397 | `59251a537ca9ad984ff0e61791e4628cbe896e4e69a3f6ac8316e1f8a3f1f4e0` | 0 |
| crates/cairo-lang-plugins/src/plugins/config.rs | 12869 | `b750cf21ac3542b109ba18ad18b00476e15d0482a259c165af46dca03441dcc1` | 0 |
| crates/cairo-lang-plugins/src/plugins/derive/clone.rs | 2449 | `8b1d71ba200bfebb1221fd6eb2b04ae48e8c8b568c452c3b7c4669ab16074471` | 0 |
| crates/cairo-lang-plugins/src/plugins/derive/debug.rs | 2718 | `3ab06055acbbc525d25a8de854eda46a4089f0b82d09eb1c7d5c55255ac52182` | 0 |
| crates/cairo-lang-plugins/src/plugins/derive/default.rs | 3932 | `38a3681310c0d4592f310d21c3d91f7542be3967646444ab9d044aaf18d9d788` | 0 |
| crates/cairo-lang-plugins/src/plugins/derive/destruct.rs | 1709 | `c3972013edba7e9e0ec9a9ffdde12d711d6dd948f3222dbec2f0046e06ea9f32` | 0 |
| crates/cairo-lang-plugins/src/plugins/derive/hash.rs | 4235 | `939a38280ad36fbf266478a25613b515baaf842a668ebe7445e9cd0cd8eb412a` | 0 |
| crates/cairo-lang-plugins/src/plugins/derive/mod.rs | 6031 | `4ed43f5138e2fd8b5c0e027709e155991f1e6eecb824b678a0af29d0fb2356c7` | 0 |
| crates/cairo-lang-plugins/src/plugins/derive/panic_destruct.rs | 1793 | `f99fc58ae6e6c2fe1e965675305dbaf513dbab0978a9387ce85d8acd8fa340ed` | 0 |
| crates/cairo-lang-plugins/src/plugins/derive/partial_eq.rs | 2551 | `c9f8566fdd6ea012176ebd63c73080df4d931741dff1bff9baea0c9755f2f01d` | 0 |
| crates/cairo-lang-plugins/src/plugins/derive/serde.rs | 4043 | `6c14d7ccad7269bee5397268f00bebaef7733eae7dd1bcc293794ff7d1a736af` | 0 |
| crates/cairo-lang-plugins/src/plugins/external_attributes_validation.rs | 4616 | `cb924f8e58aad5dc56c0e5acdd58da52b9c8c25965910fd904f815a9ddb0f4a1` | 0 |
| crates/cairo-lang-plugins/src/plugins/generate_trait.rs | 12129 | `cf831bcb4644e9eb022d2dcb3b87ba7be4decb47f5064a6f966e9c19cb6ada8d` | 0 |
| crates/cairo-lang-plugins/src/plugins/mod.rs | 286 | `e634eb1149fc731452891ce7d041d959d5fe7179d46f572cf6e9eab51415e60a` | 0 |
| crates/cairo-lang-plugins/src/plugins/panicable.rs | 8277 | `c8f7d0a1e79351377fa47cee4c0fa9d057a6dd3afe974eb8368bf515890e6856` | 0 |
| crates/cairo-lang-plugins/src/plugins/utils.rs | 7882 | `9b1fa829203d29a29be80c3826a7e9cb895a4e6ed987fc9507887d7bffabad7d` | 0 |
| crates/cairo-lang-primitive-token/Cargo.toml | 205 | `977928aaafb88ef97175a4dcb2bedd4c54d88bbf7ebd3673e476c9cf60425f5d` | 0 |
| crates/cairo-lang-primitive-token/src/lib.rs | 1180 | `2d89755333baf08480eaea6bc8ed1772af47b91f5ff8338a358d99425a1a47ce` | 0 |
| crates/cairo-lang-proc-macros/Cargo.toml | 675 | `89bb0e1f708c4addfc60dc0910bcb11a1430036f8c04867282d3a460364b7b54` | 0 |
| crates/cairo-lang-proc-macros/src/debug.rs | 7570 | `ea547fe0b755b62048fefd6cbf5d9776a4e9657cc31208025e6d6fdec81ff702` | 0 |
| crates/cairo-lang-proc-macros/src/heap_size.rs | 4997 | `488dff258ae7c7746522ac134cee41b80f0430eb089247f2e4252ceb5291392b` | 0 |
| crates/cairo-lang-proc-macros/src/lib.rs | 3864 | `7037ba8a301c548c5816e3b87e4ef51b19edb22457ca3a160060e3a51d572d6d` | 0 |
| crates/cairo-lang-proc-macros/src/rewriter.rs | 7262 | `ba4a8fd2144357d6f74c96cf11f46cb631c9dc2f3277679037d9a9e24b47e1c1` | 0 |
| crates/cairo-lang-project/Cargo.toml | 596 | `c2075895152be51e923eae844c011aacbda96759ca87c724ad8e1da1d8b6a584` | 0 |
| crates/cairo-lang-project/src/lib.rs | 2750 | `00bf838cc4f53a1c192edf71f401fdc5fc9335fd3cb71e02669c217e344323bd` | 0 |
| crates/cairo-lang-runnable-utils/Cargo.toml | 887 | `13160c5c05a0dc51141cea307b87f9392423c479774d9953a1034c7ffb62b0b8` | 0 |
| crates/cairo-lang-runnable-utils/src/builder.rs | 28440 | `c6788a664274e4fec80425a149fe3f345941f833d71005edefe8b1535d9e7079` | 0 |
| crates/cairo-lang-runnable-utils/src/lib.rs | 17 | `981eec34c62f5531f29016aaaa8de2d750f4bc73add348fd0ba0340c383b19c1` | 0 |
| crates/cairo-lang-runner/Cargo.toml | 1711 | `0ce7f20d1ccd919dbd42bbf3500decb8dc506cff9b0bf0ea9f5a42ecaf475d6c` | 0 |
| crates/cairo-lang-runner/src/casm_run/circuit.rs | 9578 | `a567d4070bd5f423bc606b806d92f44125e667d4f28e4c0c8f4fecb2ee310968` | 0 |
| crates/cairo-lang-runner/src/casm_run/contract_address.rs | 1138 | `87e8dddfd65133178d191a2a69216362bb43e07e82d2c24c3aeb451b0fbaaa0c` | 0 |
| crates/cairo-lang-runner/src/casm_run/dict_manager.rs | 5095 | `8b5de79ee35f38f9818bf9c4a8440613f1abc7f90e93abb48b5b4fbabc8d11f2` | 0 |
| crates/cairo-lang-runner/src/casm_run/mod.rs | 104550 | `95c92cb2bb92a68fe0a43ca323e96c1554fade18bffc6179bbc4d22075a3e6c4` | 0 |
| crates/cairo-lang-runner/src/clap.rs | 795 | `d3193d4e1c0872e6f5b28053ab2780222cbfb692e4cc5ca251c6e17f36eaef63` | 0 |
| crates/cairo-lang-runner/src/lib.rs | 22867 | `d4c16c1ecd0a4a4467f59e88fab0e2dd97fce6d9f132913990debdd01af16d22` | 0 |
| crates/cairo-lang-runner/src/profiling.rs | 33152 | `9a123aae121cfd69630e3f46df6cfa03117bc5939a23b56affcb9e60a2b4db9d` | 0 |
| crates/cairo-lang-runner/src/short_string.rs | 1865 | `e8b84b28ba08e5ced7f95959e5e6d5b2544bf0510d4726ca9df8f96358c72784` | 0 |
| crates/cairo-lang-semantic/Cargo.toml | 1840 | `36759e06904053a1b94385544de86766f0a24978e4168ea076e93c3348563e66` | 0 |
| crates/cairo-lang-semantic/src/cache/mod.rs | 75211 | `2657a935118c4ba86d00e269e35ad25ce77d30b453c60e8b8d2bba5af4ead191` | 0 |
| crates/cairo-lang-semantic/src/corelib.rs | 49941 | `c60235bee4c60235ce8a03e0b3b4fd70ddf7313babf89f17d6183c7c5ac1655e` | 0 |
| crates/cairo-lang-semantic/src/db.rs | 27798 | `7b2c59e8e9525f25f817f41b330be3e688f5109673cd19ca428df1c810d911b9` | 0 |
| crates/cairo-lang-semantic/src/diagnostic.rs | 98540 | `c7fb4d4bd18844371dec6bdc0f8dbb8f9a2d900fc5515a670aa3b4f5b3f07cc5` | 0 |
| crates/cairo-lang-semantic/src/expr/compute.rs | 216662 | `9eebf2350067bc86ba420d527c206657455cafde1a7a8455b4fe993b68979fee` | 0 |
| crates/cairo-lang-semantic/src/expr/fmt.rs | 1439 | `d4b19b1f258c95339a9decd384c286dc2ccb3307ce31c49a5073e4192920a3fa` | 0 |
| crates/cairo-lang-semantic/src/expr/inference/canonic.rs | 24736 | `fd01ec1cb77ab0fe9852687e9c185bdd5f02fda9a308ae01ca9521c736c9ea6f` | 0 |
| crates/cairo-lang-semantic/src/expr/inference/conform.rs | 38910 | `a18f97d20506855ead0224e909edb019022d2e8a8605cec38e356b13395540db` | 0 |
| crates/cairo-lang-semantic/src/expr/inference/infers.rs | 23418 | `d183dfe2cefc48ef7e75dd2aa3301f8a5dbea740eaccb98ae0e38b9f92653b26` | 0 |
| crates/cairo-lang-semantic/src/expr/inference/solver.rs | 40404 | `1ef34a75a622f8a8cbddc6382b136f88637ed76a1e31ef9212cb903657a19426` | 0 |
| crates/cairo-lang-semantic/src/expr/inference.rs | 79595 | `70307c92bd3a0d208eccecbac8a05a045c346f45ab69eb7267ba36c436293f3e` | 0 |
| crates/cairo-lang-semantic/src/expr/mod.rs | 199 | `ac6f699225cd3b8ad1fc1b95655e8f49e2039991b198a7572b7df928eff117a2` | 0 |
| crates/cairo-lang-semantic/src/expr/objects.rs | 21703 | `c62fcd0440687f6d25c0c6812f3eb1974ea5120cc835f39d23e73fe575d77b42` | 0 |
| crates/cairo-lang-semantic/src/expr/pattern.rs | 10217 | `b7ce9ec9bf8129a6a2aeceda0b20c64229e32bbcc3b9f96bb6a5c6ab31f6d965` | 0 |
| crates/cairo-lang-semantic/src/helper.rs | 3549 | `b24a13f800a0e549f12b7fdb7c02e2971610b7a9dd254e7fe538fd494e5f8de6` | 0 |
| crates/cairo-lang-semantic/src/ids.rs | 1446 | `18ae7f13c6985c573c777ed6be89a827edf84c31737b0510f06a64b5302f64ec` | 0 |
| crates/cairo-lang-semantic/src/inline_macros/array.rs | 3385 | `3ee861083eb4c0c0a711218599e4465baa25bc5ac16ed865ffbde20d549e7ee4` | 0 |
| crates/cairo-lang-semantic/src/inline_macros/assert.rs | 6560 | `38d8ed1f9e76137760ce93116d2224fd6192ffaab41a859c99b77b0e5ffdb08f` | 0 |
| crates/cairo-lang-semantic/src/inline_macros/consteval_int.rs | 8942 | `5d2b042f235b3cd27b17acde6d6034d9ff8ed120abea8ab2b83ec626eb09c0db` | 0 |
| crates/cairo-lang-semantic/src/inline_macros/expose.rs | 1749 | `0481a3e653e1760080beff1fd455e4231c81d665f207810b584cd56241c87bfc` | 0 |
| crates/cairo-lang-semantic/src/inline_macros/format.rs | 3325 | `eac7e9ce1a20944bf038947a84368d133a4bf2ed0e15b0e6bca2f50bb6e99dc2` | 0 |
| crates/cairo-lang-semantic/src/inline_macros/mod.rs | 1225 | `ce634d7a6160137504c99727d72ea0e8358411b5148102971a9f7c6b61dec3de` | 0 |
| crates/cairo-lang-semantic/src/inline_macros/panic.rs | 6342 | `850b79c362476df34d568967a037eb7dcaf86a9c2e839f84dac82d989333c260` | 0 |
| crates/cairo-lang-semantic/src/inline_macros/print.rs | 4424 | `68a12b5e6b26970e75e4281291cf16d6b72fc8147e1e27e552be0a0f5569564d` | 0 |
| crates/cairo-lang-semantic/src/inline_macros/write.rs | 25627 | `13e16309123611cb911de31d4f312b045b0f5dc738d4d99696af4d1f53bafa42` | 0 |
| crates/cairo-lang-semantic/src/items/attribute.rs | 6487 | `5ef8754feb279b1aebee83e4bc2f310fdf78dd7b7b82d38ce0f25dbd2d19ab76` | 0 |
| crates/cairo-lang-semantic/src/items/constant.rs | 67872 | `50c20d530433dc8ad088a545e41b9ced5770b04d1e34c05b9409f2337594d0ea` | 0 |
| crates/cairo-lang-semantic/src/items/enm.rs | 14966 | `1f1db7768ced681b5439a15a01570b5dac99e34578dbe8fb4f0600dac8015c9a` | 0 |
| crates/cairo-lang-semantic/src/items/extern_function.rs | 9077 | `297998289db4222cc3f7795cba60172c387bd9f1c25e8389b3c6aca41c3037ff` | 0 |
| crates/cairo-lang-semantic/src/items/extern_type.rs | 6287 | `598e31bc23ce12c4408700a029352acdf87d5f11e09da7617836feba7e10afb6` | 0 |
| crates/cairo-lang-semantic/src/items/feature_kind.rs | 12988 | `f6433830f2d60c7ab0732fc1f1036c53b6e5412753de7a68b3594ad1fbd8034e` | 0 |
| crates/cairo-lang-semantic/src/items/fmt.rs | 2578 | `ef07997681439a8a6fb734663a79e640d4210694a1524e958f2c7d34dc3ca66e` | 0 |
| crates/cairo-lang-semantic/src/items/free_function.rs | 11734 | `5f6ec03b4630fa207159ed7780b8bffa35e6527e37bfcbd0b33d2f1168fae461` | 0 |
| crates/cairo-lang-semantic/src/items/function_with_body.rs | 13887 | `6b76f944ea39f918db6affb9d0e173888fe717570892665f0ea406a4ba540f86` | 0 |
| crates/cairo-lang-semantic/src/items/functions.rs | 47159 | `0c82ffe27a78b4148eda3ce0e99ec74c443f216e3d3175644972cf12605ab01d` | 0 |
| crates/cairo-lang-semantic/src/items/generics.rs | 36592 | `7ce2164f0484d60f52beba435025b77078f4c1eb0c687ffcfdaf4e2d111ff56c` | 0 |
| crates/cairo-lang-semantic/src/items/imp.rs | 181339 | `013653447500757fa415d093c16879ea5b11df2086074d241567798be75e2998` | 0 |
| crates/cairo-lang-semantic/src/items/impl_alias.rs | 11604 | `1be3d28274260d86dea3904d1b3a3f852867bafb99f0171041d0a100af3925fb` | 0 |
| crates/cairo-lang-semantic/src/items/implization.rs | 2114 | `5a4e386921bd8ee76efd68b2aaa63b162c1fe991b9ca144d7c54e0ca6ca64773` | 0 |
| crates/cairo-lang-semantic/src/items/macro_call.rs | 16093 | `ce81f586fffad4620d7b9a0be7569cbcd0fe679e3c38b12f99d1f90f64e76bbd` | 0 |
| crates/cairo-lang-semantic/src/items/macro_declaration.rs | 39356 | `b851ccb16c7726191b35f25df9edf65666f4b19f0d35024f60621121641a25f0` | 0 |
| crates/cairo-lang-semantic/src/items/mod.rs | 3343 | `bd532ee08e7b83187278354c395f983fb7b5d5bff87fa40b36e44c53bc30f8f0` | 0 |
| crates/cairo-lang-semantic/src/items/modifiers.rs | 2569 | `c7f08264e3a65f93d7dca167369056c37364bc4ead99e9e0cd8c95174363eeb5` | 0 |
| crates/cairo-lang-semantic/src/items/module.rs | 16730 | `1ccb97699a0cb53b759f5111f8945b8412f46454ffb7d84a2782e45df232f3fd` | 0 |
| crates/cairo-lang-semantic/src/items/module_type_alias.rs | 6216 | `b193a6fb37e194d2bcdfcc237242cd942122978cf4ab923408b9345f5b9df1fd` | 0 |
| crates/cairo-lang-semantic/src/items/structure.rs | 13071 | `127230b6b2f54a9fb97e8e241d1261662f95fd2c89d2cb73c25b74a88885acc2` | 0 |
| crates/cairo-lang-semantic/src/items/trt.rs | 62808 | `0191eabf5313d704c0d99105625b5f3a5f6025d4a0ef180ab781d042dab581bd` | 0 |
| crates/cairo-lang-semantic/src/items/type_aliases.rs | 4372 | `f846fdc5385e74ac7b8370480f98a73248f9d1a0bef183c9c37c585e3301d1fd` | 0 |
| crates/cairo-lang-semantic/src/items/us.rs | 20936 | `67c6049db196a45ee9dd3f912a6e9d7570ed46e223af75e9c0afbd87024e197c` | 0 |
| crates/cairo-lang-semantic/src/items/visibility.rs | 2234 | `dbb9f224a29774307955ca4574ff02fd813ab7f8d336310f699b34c9784e9568` | 0 |
| crates/cairo-lang-semantic/src/keyword.rs | 464 | `4fe452dace02195a18cdc7d80440d91f1d95da065c8a43132b2e5aae011309ac` | 0 |
| crates/cairo-lang-semantic/src/lib.rs | 723 | `5ec4561c150bc8c1bd5683980bdd51bf99f6503c5e34ce75fa8a9f4fa9d975cd` | 0 |
| crates/cairo-lang-semantic/src/lookup_item.rs | 10066 | `19d17989d9c45ef5f7ab15317069f891f2b5472cce404527d1ae896d1d463d85` | 0 |
| crates/cairo-lang-semantic/src/lsp_helpers.rs | 26444 | `0a87f230614cfb047ff6dad8ac29b530fe6b7b680ee0cf9cd118f1a62181440e` | 0 |
| crates/cairo-lang-semantic/src/path.rs | 25472 | `26103632724448a8382de03f4ed8a1edbe1d22d6c9f70bed20f18205442ae2a9` | 0 |
| crates/cairo-lang-semantic/src/plugin.rs | 3650 | `a7296359f53d1057b5cf9043b22a9a7bae23ab64b4a1e68c165ce5f87152e37a` | 0 |
| crates/cairo-lang-semantic/src/resolve/item.rs | 7160 | `fed332ec2933a5120261a0e99eda76294a3f0b30db1ecf3552bfbb490eb3f115` | 0 |
| crates/cairo-lang-semantic/src/resolve/mod.rs | 115112 | `f90f6bd352b33bf9a98105d7e27b57197524dedc2d8c3aa3ea524c4e8a7e23c0` | 0 |
| crates/cairo-lang-semantic/src/semantic.rs | 4881 | `6bdf91fb77f41ae90b94d07c771915e16b80ebe428967d198bb673df90ad27cb` | 0 |
| crates/cairo-lang-semantic/src/stable_order.rs | 13497 | `74f9cc767182f9fb9dec27683be128cc990471b17a7bed214e3bb1f01439b418` | 0 |
| crates/cairo-lang-semantic/src/substitution.rs | 31195 | `9b91cc49df741a83a84b417ada612e98165e42a610a532ab3b4ca341b747b3a4` | 0 |
| crates/cairo-lang-semantic/src/types.rs | 60452 | `5dd49c5dc049efb3118d3939833e7b4d1b9c7e9d44fb6ed7a87c459aa1536536` | 0 |
| crates/cairo-lang-semantic/src/usage/mod.rs | 19323 | `78b5d62e717d7ae881238318284278c99c7aa085e6856c21e5bce08d912ef727` | 0 |
| crates/cairo-lang-sierra/Cargo.toml | 1245 | `6da6c0ad10e09b2fa3f650b9e064b6ee05f2ee169c78db55bc86ffae24f42cfe` | 0 |
| crates/cairo-lang-sierra/src/algorithm/mod.rs | 27 | `635616f226b407b7a76f148a524510171a12788a88881c22905148868311e535` | 0 |
| crates/cairo-lang-sierra/src/algorithm/topological_order.rs | 3750 | `9b68085c090bff1854fc79857629377c6a12c927ec14772506dc4354da9a93a6` | 0 |
| crates/cairo-lang-sierra/src/build.rs | 71 | `dfc95faf6971ef88db3bde5eec530a3c7300c0486db2eabc195f3bc4f43dc80e` | 0 |
| crates/cairo-lang-sierra/src/debug_info.rs | 8426 | `3b6d52aae041247085268ee052fe7a6ec5a911cda952a39b07f389aabb129814` | 0 |
| crates/cairo-lang-sierra/src/edit_state.rs | 2100 | `ef9b611aa1494bc5477dfd7e530285b41f14434ec4b1f65791aff84672959f18` | 0 |
| crates/cairo-lang-sierra/src/extensions/core.rs | 6180 | `12f0f150c7502f6a9e0d8a568c1ef119a27c3c730ec10f2bd54b82f741df7c9d` | 0 |
| crates/cairo-lang-sierra/src/extensions/error.rs | 1712 | `0c2dbdcbd896148ad49f322ea9b67da8559fad4fccdc1f9ce09931ef0f544fdb` | 0 |
| crates/cairo-lang-sierra/src/extensions/lib_func.rs | 25513 | `a0ce27d0d8152f7866332d2637d896dd74ce595206d2248c16bfdec142a7b35f` | 0 |
| crates/cairo-lang-sierra/src/extensions/mod.rs | 2768 | `e979a5cf79be22f1d3b8c51700e56cfca8bdaec63a46a03162cdbedb8e9ec924` | 0 |
| crates/cairo-lang-sierra/src/extensions/modules/ap_tracking.rs | 2382 | `3e32039a5d495c6834359dbd6547ea9cd93d7bc6fe841163851d6746fa0d6988` | 0 |
| crates/cairo-lang-sierra/src/extensions/modules/array.rs | 26205 | `58857c3f5c6e0287dea3dfbd80ab9a882449b65e07357d86a3c11dba27fd47e1` | 0 |
| crates/cairo-lang-sierra/src/extensions/modules/bitwise.rs | 429 | `2c065f36227f4da6bea2f9dfc4f3217a2a9ef54ea32b36687169968495939606` | 0 |
| crates/cairo-lang-sierra/src/extensions/modules/blake.rs | 4770 | `aa655fa86edbfb74f57c244dbf8baa978321eab2cb371fc4f074dd21ef6cfc64` | 0 |
| crates/cairo-lang-sierra/src/extensions/modules/boolean.rs | 3780 | `fcde0ca79f812dd763504a64825dd789c1e2a6b8c65ad699a143608d50d9dc42` | 0 |
| crates/cairo-lang-sierra/src/extensions/modules/bounded_int.rs | 27956 | `d975e9338bb20b577f68668e889834d8f0978b4187a8a096df70cb948c8528a1` | 0 |
| crates/cairo-lang-sierra/src/extensions/modules/boxing.rs | 5284 | `84f669b7bfa932e686586ca1b2c1b604c8de1834e150b48d100caf3b42f7c7ce` | 0 |
| crates/cairo-lang-sierra/src/extensions/modules/branch_align.rs | 743 | `f9093feda987fa961ce60a7f849766d234ab9f93f4ca3e7e4c48e306c7c4963e` | 0 |
| crates/cairo-lang-sierra/src/extensions/modules/bytes31.rs | 2490 | `5befd20c5c674587804b97520480c6339f0ab588b1cb44a96bdc4113174de58e` | 0 |
| crates/cairo-lang-sierra/src/extensions/modules/casts.rs | 7024 | `c74e099a84afdc29e5be387bb926054e43ad7f3de379dcd95d8c450112553e11` | 0 |
| crates/cairo-lang-sierra/src/extensions/modules/circuit.rs | 49281 | `2d7ec86291a5fade010a898144d272967c982423ffeb9f779953b6fe88d948c0` | 0 |
| crates/cairo-lang-sierra/src/extensions/modules/const_type.rs | 16095 | `620be418f673af06518e6d109e08ded63c27df92c43f6a9d6aaa00e4bf19b7f5` | 0 |
| crates/cairo-lang-sierra/src/extensions/modules/consts.rs | 2554 | `1f02ab96b7b81f22697b054c88cfc14546a8e1adf9e66f5a1af9237f40dbb855` | 0 |
| crates/cairo-lang-sierra/src/extensions/modules/coupon.rs | 5850 | `cd80877e7d0a39c7f42070a90f7497be533e3c277ef786424b0adee7a094823a` | 0 |
| crates/cairo-lang-sierra/src/extensions/modules/debug.rs | 1212 | `3867fe6c80209032d80cf22a74a99b879d6b7b04abe34899427e67d3efb66678` | 0 |
| crates/cairo-lang-sierra/src/extensions/modules/drop.rs | 1232 | `a3405fb27939b034641dd54649e2fa3f96fff749bc014efdff16c2bebe0143d3` | 0 |
| crates/cairo-lang-sierra/src/extensions/modules/duplicate.rs | 1278 | `7c838ab049544ce49b84574d8edf643909d34841073f203158724528b016ed55` | 0 |
| crates/cairo-lang-sierra/src/extensions/modules/ec.rs | 15537 | `e4a18cd51071a02258d67b928ecdd63e765bd67d6fd9c0effd96901871585108` | 0 |
| crates/cairo-lang-sierra/src/extensions/modules/enm.rs | 17169 | `5df91eec8e6c98e7e1631aff88b8738ba0cfda41c80cc4e7f1f08f0a07196021` | 0 |
| crates/cairo-lang-sierra/src/extensions/modules/felt252.rs | 10120 | `d662fd68648b4bd5a86b2e477bbb57111f0783221b040db1c95be9b71fb9fed2` | 0 |
| crates/cairo-lang-sierra/src/extensions/modules/felt252_dict.rs | 11355 | `283c07442e2ed388d80bb3780891547bf96d9a02085b6878d91b5ce3e23e4baf` | 0 |
| crates/cairo-lang-sierra/src/extensions/modules/function_call.rs | 6553 | `0e6d0eb128810df637cead6afcfe5d9f19247765aaddc3bd41f95c12c2675db8` | 0 |
| crates/cairo-lang-sierra/src/extensions/modules/gas.rs | 14216 | `172514245ccc478545ffb5a732fd7da0eb2243ff85438e6eac43d02522d68168` | 0 |
| crates/cairo-lang-sierra/src/extensions/modules/gas_reserve.rs | 4478 | `68db4423be4185a3c5cb4bec4df7bb1f535456b56960c17d0002e9fde767d0d9` | 0 |
| crates/cairo-lang-sierra/src/extensions/modules/int/mod.rs | 7599 | `9d7af18faf9766f7606b32d5cc33180f0775de041b0a126b1a1994a7b1b70e36` | 0 |
| crates/cairo-lang-sierra/src/extensions/modules/int/signed.rs | 11796 | `c082c8e36d63c71ed1bdb57d8cb027cfbd262e91f5d9d8ed26691939ad5c423a` | 0 |
| crates/cairo-lang-sierra/src/extensions/modules/int/signed128.rs | 1530 | `3ce148e0c3b1a40012678f28db2ba9bf3167eeff7bfd37514dd7c2ec6cf7acd5` | 0 |
| crates/cairo-lang-sierra/src/extensions/modules/int/unsigned.rs | 15201 | `2a75a977fc80d9a78df0edd65aee4766c309652fbc57abd3b833eb02e9dea4a3` | 0 |
| crates/cairo-lang-sierra/src/extensions/modules/int/unsigned128.rs | 8767 | `4775854d8f3ad67615b08ee902b3703efdaf0543fc37fa98d6c10cd95ab834b6` | 0 |
| crates/cairo-lang-sierra/src/extensions/modules/int/unsigned256.rs | 6796 | `ebafd86d50b98750940da6ce1bb6646bf5846ea5d17828a6a6b1b6588ba18296` | 0 |
| crates/cairo-lang-sierra/src/extensions/modules/int/unsigned512.rs | 2951 | `b9690b437bbd86f4b1b1899215f3821c4b9f4be5c32ec507b3b1db934b3d2748` | 0 |
| crates/cairo-lang-sierra/src/extensions/modules/is_zero.rs | 2055 | `e0ba001d8b5d00882db8531b12fcda3ae6809889189a0b91a4107281c939cd33` | 0 |
| crates/cairo-lang-sierra/src/extensions/modules/mem.rs | 5730 | `57b1216779b3956cccb893ad49c8eb5d802ab8e52bea6db6bcab59e28b452031` | 0 |
| crates/cairo-lang-sierra/src/extensions/modules/mod.rs | 2307 | `5c343d1bed023e3bfbedd528f516865d46c05e9b2213d601bf7d4c3f2e54c712` | 0 |
| crates/cairo-lang-sierra/src/extensions/modules/non_zero.rs | 2491 | `51ad34a10e5558c7a2dc943f73474090f579359899133b995e632cdecb26bbbe` | 0 |
| crates/cairo-lang-sierra/src/extensions/modules/nullable.rs | 6219 | `69ef87ec759089f92563da902949a59fe5c38f157935d9eac24b020f8c42a1cc` | 0 |
| crates/cairo-lang-sierra/src/extensions/modules/pedersen.rs | 2142 | `76d48e9980b9df519671b5816f345a6718c770d94bc59b932cb1a17888eddeef` | 0 |
| crates/cairo-lang-sierra/src/extensions/modules/poseidon.rs | 2402 | `64ce45d4428488b0d68ee1ccf3f66c0ae9baa41b9ee5bd100c103c29d0d354e3` | 0 |
| crates/cairo-lang-sierra/src/extensions/modules/qm31.rs | 10657 | `37b1898865b7c471c029a72d267887c2d42a0198fa658fc8f7d4bfa7022d5f72` | 0 |
| crates/cairo-lang-sierra/src/extensions/modules/range.rs | 6940 | `d77235507ced078517487df038448881356159582ba34284c4b83a42d54cd9e4` | 0 |
| crates/cairo-lang-sierra/src/extensions/modules/range_check.rs | 784 | `af4f9d0735fb8ffb1b68a280953d810bedde54ab9da44b4d3c0c60e38d5e7e5a` | 0 |
| crates/cairo-lang-sierra/src/extensions/modules/segment_arena.rs | 1094 | `709ed651bbafec9c427297d1d01ac3a6511372a99a3ab116feb7185b226dda21` | 0 |
| crates/cairo-lang-sierra/src/extensions/modules/snapshot.rs | 3174 | `06e8993661dbc615c40f1a2b3f43be703cd36a7f744808aa1cdfdce4f610545f` | 0 |
| crates/cairo-lang-sierra/src/extensions/modules/span.rs | 1151 | `d2f49a2faec4e3f8b327038338aa7fd1ddf842641ef11f150b003ccaa1ee9a41` | 0 |
| crates/cairo-lang-sierra/src/extensions/modules/squashed_felt252_dict.rs | 3361 | `c3504bfe2316a7042ff55882b594830803295cf3fdd65acda4817cb102641e55` | 0 |
| crates/cairo-lang-sierra/src/extensions/modules/starknet/emit_event.rs | 880 | `549e50cc6af3ef5cdd4f5666d92d900907a647bd911c645270c69c443644fe8e` | 0 |
| crates/cairo-lang-sierra/src/extensions/modules/starknet/getter.rs | 12948 | `08be307df3478990035bd150c89a492b4df5de3da5593343114a9d3c50b92482` | 0 |
| crates/cairo-lang-sierra/src/extensions/modules/starknet/interoperability.rs | 8705 | `b6aaf1652db2e6e03ea43565e3db3b6900efef6929634b8acace63f2511e23a7` | 0 |
| crates/cairo-lang-sierra/src/extensions/modules/starknet/mod.rs | 5652 | `74c57ba011fd1453e1b686f5d9dd36dcf7427f01dcc66443f11191d87739a611` | 0 |
| crates/cairo-lang-sierra/src/extensions/modules/starknet/secp256.rs | 6735 | `f82f3b08cb95fbe11b3b44b103e93b0fc66b2b7a64ea416213e1ca07ac07bfc3` | 0 |
| crates/cairo-lang-sierra/src/extensions/modules/starknet/secp256k1.rs | 1001 | `f70b17f0e1a3712c435d57454dafcc965c5ec630d25dfc4eb20eee65c69ba357` | 0 |
| crates/cairo-lang-sierra/src/extensions/modules/starknet/secp256r1.rs | 1001 | `ea55c773bb58e7acfcbceb07facbcc6bfa84c30ce09fe1f46e8b37ed5caf13f2` | 0 |
| crates/cairo-lang-sierra/src/extensions/modules/starknet/storage.rs | 8377 | `9b2f35658e7435a320bf653102690b7f8743d1f493b0e5bb2a47043a7e76bc6a` | 0 |
| crates/cairo-lang-sierra/src/extensions/modules/starknet/syscalls.rs | 14296 | `7afa8b0f441dd713716c42ee4ccccbcbed9bcb64e39c4f6812243eb108e95a56` | 0 |
| crates/cairo-lang-sierra/src/extensions/modules/structure.rs | 14362 | `1431e0fcec16fcfa80d47dda8d054867fd4556b99c41c04c7d7d009351175a7e` | 0 |
| crates/cairo-lang-sierra/src/extensions/modules/trace.rs | 1282 | `b799e19357f5b970d824f3c40173aec91ab60c2fbdaf200137b3b16de6c3109c` | 0 |
| crates/cairo-lang-sierra/src/extensions/modules/try_from_felt252.rs | 2479 | `ba43ddb6eb5a4716c1e5f27ee82838bb288e00fc5caed2c924658afca204fab8` | 0 |
| crates/cairo-lang-sierra/src/extensions/modules/unconditional_jump.rs | 813 | `6d6f93b0dd5be172a5ac2701344f7a6cde02d5d47c48964ac2c3c9ff03544a3a` | 0 |
| crates/cairo-lang-sierra/src/extensions/modules/uninitialized.rs | 1154 | `e6d3e7aa67958e2389be9f1de38b22a84638023f029c00d61c617d05dc8aec7f` | 0 |
| crates/cairo-lang-sierra/src/extensions/modules/unsafe_panic.rs | 706 | `27213b591fa1666788899d9c9d80bb06269b8b9f4817277f30aad07d0d65cab3` | 0 |
| crates/cairo-lang-sierra/src/extensions/modules/utils.rs | 6328 | `a7a62abfeb62c8c0d7f3078a821071a6653b1e578353417e8c726eaa15286e9d` | 0 |
| crates/cairo-lang-sierra/src/extensions/type_specialization_context.rs | 616 | `6eb6407ae435a7a68259420c00a806d4c062912345099b88ab90328d8f7ced21` | 0 |
| crates/cairo-lang-sierra/src/extensions/types.rs | 8638 | `d3c7e74495e5dc6326498aab23a6e1ae64f0ad9b62e3a2ec7fda9b5b3ab226e4` | 0 |
| crates/cairo-lang-sierra/src/fmt.rs | 7634 | `880f3d324f13c8720d5d624678915adc970fab53c016085dbfc8473b3e5ba824` | 0 |
| crates/cairo-lang-sierra/src/ids.rs | 4066 | `060c9c53bd269e24de6c90d317c3384b0b0db27ba4fd8c2fdc5146cd1d00f40a` | 0 |
| crates/cairo-lang-sierra/src/labeled_statement.rs | 3373 | `163976370406399e19804ef2253158fcc180e74625f658ec6210ceb8fd8c4d8d` | 0 |
| crates/cairo-lang-sierra/src/lib.rs | 1187 | `0e7f1d9b8c48089d879e2e333ad324e678dfc454253113b29e03eed0e4368ed4` | 0 |
| crates/cairo-lang-sierra/src/program.rs | 11121 | `a623d6eff63ed0994ac4fb5b4076d95880afc0e9156e5c60865e31398eb04bb6` | 0 |
| crates/cairo-lang-sierra/src/program_registry.rs | 17518 | `df1a6c14e19ff6d0c96e9985dfb5daa869afd60605c1388a3fcc290542c68a66` | 0 |
| crates/cairo-lang-sierra/src/simulation/core.rs | 33654 | `6674a9db10d3103dc87a89e46d25c4d0b80dbbb36e6a88b0bc2ea75336d45913` | 0 |
| crates/cairo-lang-sierra/src/simulation/mod.rs | 6015 | `1e742c8715edfe3b3111411209c8b02294e7c24b13100d18b64295909c611565` | 0 |
| crates/cairo-lang-sierra/src/simulation/value.rs | 734 | `3dc76e0ab0f29e0377dd547bbc1b604a42250fa316189baf768813f76cea1cfb` | 0 |
| crates/cairo-lang-sierra-ap-change/Cargo.toml | 764 | `c256bc01e51113db81d81a7c992770c596c5868e9e4c885dd74df2dbc8cd9268` | 0 |
| crates/cairo-lang-sierra-ap-change/src/ap_change_info.rs | 1108 | `6b60014bd489270fc85a15996accdd093b551614a1142118d2ae3143aeb19879` | 0 |
| crates/cairo-lang-sierra-ap-change/src/compute.rs | 14627 | `e821f794a050e9e2269ff4638e818f639a2a11a973f8211186310fcd594dee0e` | 0 |
| crates/cairo-lang-sierra-ap-change/src/core_libfunc_ap_change.rs | 28543 | `b177577c0c6dfcd9e5270c469952a60740138411084aaa0105f30191ffa23674` | 0 |
| crates/cairo-lang-sierra-ap-change/src/generate_equations.rs | 7565 | `bef7f8441314d81daffb80d695364b6da54ae2c3af3a0c364cbe7bce6e2dc8f1` | 0 |
| crates/cairo-lang-sierra-ap-change/src/lib.rs | 5075 | `47d6d60b61ae21a30a20b44da94269d5469a3eec1928bb5ac6dc62651e72fef0` | 0 |
| crates/cairo-lang-sierra-gas/Cargo.toml | 923 | `776cc01650253808ccc98e9ed1608f01a334d11b1428b557da709c54b5acce99` | 0 |
| crates/cairo-lang-sierra-gas/src/compute_costs.rs | 36226 | `10f38295ddf6515479a5e296f9fefcffce37fce1caad1e07487ccec421626c23` | 0 |
| crates/cairo-lang-sierra-gas/src/core_libfunc_cost.rs | 1993 | `f650dd5e2973da809018bfc7a9484eab8164326637aaadfb23429705bd7a5f3f` | 0 |
| crates/cairo-lang-sierra-gas/src/core_libfunc_cost_base.rs | 47737 | `38f0fb987f353da00e402943ee3d9700a86a59e06d20c7273ff1d904f2d6c0ab` | 0 |
| crates/cairo-lang-sierra-gas/src/core_libfunc_cost_expr.rs | 3068 | `f5224549eff968f358e87c21f030af438b0d6f5920b908d4737cb98d76b4d54d` | 0 |
| crates/cairo-lang-sierra-gas/src/cost_expr.rs | 971 | `70a854d5b5c545ae8bb22a9296f826605759bc57beabda29e8a1b2bbe2af1e49` | 0 |
| crates/cairo-lang-sierra-gas/src/gas_info.rs | 4793 | `3a8bf4e33b70532ba47de755759ae8618eba021b0710c85e4fc12acca36d07b2` | 0 |
| crates/cairo-lang-sierra-gas/src/generate_equations.rs | 4897 | `70f7904c4e67c38b816f489cf400a07e85cce85a4c399ba677cdeda334608b5b` | 0 |
| crates/cairo-lang-sierra-gas/src/lib.rs | 16437 | `4f8f46b37b13092382ffe15f93136da42ff43f0953c2f95c26c256bb6b701413` | 0 |
| crates/cairo-lang-sierra-gas/src/objects.rs | 5491 | `f9e472e895b22ab9c7222ddc962ade1133c1d73704847b216de30d0f79e3052d` | 0 |
| crates/cairo-lang-sierra-gas/src/starknet_libfunc_cost_base.rs | 4871 | `08ef9e2aa171bbeaebc229d784387a00f475155a690310bdeee9e0a869e9e053` | 0 |
| crates/cairo-lang-sierra-generator/Cargo.toml | 1907 | `2b139c3e1340cb3c0e78c8021cc432674a7e33498fea4a6ca37787bba2d8ac6d` | 0 |
| crates/cairo-lang-sierra-generator/src/ap_change.rs | 886 | `06770faa7c040d81cb929c80704e5173d4502a49b060e29a652477aa57550ad0` | 0 |
| crates/cairo-lang-sierra-generator/src/ap_tracking.rs | 6177 | `720c2e182891e8401115ea80872ad4c45caad28f93768fd15b86c4539283ec23` | 0 |
| crates/cairo-lang-sierra-generator/src/block_generator.rs | 31097 | `8ddbd2678b7a5330bb31fcfb360190e970a58cad4e5f1d8ed58748162d1b555e` | 0 |
| crates/cairo-lang-sierra-generator/src/canonical_id_replacer.rs | 2557 | `8a6c5d15b3f898ad9d23f9a887940ec915c45a884940f85b4ea05473f89b2ac4` | 0 |
| crates/cairo-lang-sierra-generator/src/db.rs | 20338 | `7855cb358f28f73beb12f6420266649c0b7a7c06655d43d15bef3789c455b8fc` | 0 |
| crates/cairo-lang-sierra-generator/src/debug_info/function_debug_info/serializable.rs | 2542 | `1822da65544d402d0a95b5a1c4767d7cc04593cc62d775ec31f0671579fbee53` | 0 |
| crates/cairo-lang-sierra-generator/src/debug_info/function_debug_info.rs | 23491 | `e5faa7ef511ff77c8398c0ec920457b80e6aaa619b7fbca4f224cc37ca01ded0` | 0 |
| crates/cairo-lang-sierra-generator/src/debug_info/mod.rs | 3116 | `a58306571f877f52c55d2b3359711eb716fa0b748e61eb8edd25c16d1bbdaa0e` | 0 |
| crates/cairo-lang-sierra-generator/src/debug_info/statements_locations/statements_code_locations.rs | 1327 | `9d7c37340f33502715e68fe85fd9ed29937cc771e3f5679777e34875ce838e9b` | 0 |
| crates/cairo-lang-sierra-generator/src/debug_info/statements_locations/statements_functions.rs | 7285 | `56bb45cf9e8e67cd4a8efb8bb848e3e95aa6b5e7a5efb40ccb59b79eda9b2544` | 0 |
| crates/cairo-lang-sierra-generator/src/debug_info/statements_locations.rs | 4898 | `b98770f292a5178a497c2c72f91913963a3185ef8a1dfe87d3e55037d4983914` | 0 |
| crates/cairo-lang-sierra-generator/src/debug_info/type_names.rs | 9028 | `1020d9f056137423deff4eade77c6993154be7a756e4acafa666f4864a115d7a` | 0 |
| crates/cairo-lang-sierra-generator/src/executables.rs | 4940 | `ddd4cbf099fcf21e66c1d55270e8f558420e265d473f09869d5392f71087fe34` | 0 |
| crates/cairo-lang-sierra-generator/src/expr_generator_context.rs | 9927 | `c564c130ae08b7d1c8660032c926dc6c5265ea002a7d5316fc1738d4e2718bab` | 0 |
| crates/cairo-lang-sierra-generator/src/extra_sierra_info.rs | 825 | `2ce4a506e83bc4589a43ce2cad0e792ec80c23b5a51299766e4f51818e8eff63` | 0 |
| crates/cairo-lang-sierra-generator/src/function_generator.rs | 8852 | `c273ebf8b59c9899860f8bdfcafc567c34585a3a8fc5989a4b6c7be7c6d629af` | 0 |
| crates/cairo-lang-sierra-generator/src/function_generator_test_utils.rs | 2081 | `f7ae0d5d27adcd4f88ce655b6d86b33bfc07659720398d511c57caa9c4370829` | 0 |
| crates/cairo-lang-sierra-generator/src/id_allocator.rs | 304 | `e0e8ef751ebc59bbf12ebbf8783b020b48c9d6cafba4435eb85a9211d876c009` | 0 |
| crates/cairo-lang-sierra-generator/src/lib.rs | 702 | `c5043b9ef18b32ec91085543a38e17e672ba1bd7ecb36f15ec2702e68ed59ed8` | 0 |
| crates/cairo-lang-sierra-generator/src/lifetime.rs | 10318 | `fd2afc2ec06d45113b72732e5cff2f7cfd4d5187904be23cfef0146e7a630cfc` | 0 |
| crates/cairo-lang-sierra-generator/src/local_variables.rs | 19715 | `edee41829621a172824da9795b5fb9679a0c2522625e13a41fced5cbe9161b9b` | 0 |
| crates/cairo-lang-sierra-generator/src/next_statement_index_fetch.rs | 1900 | `43bd8b05acb6781c9348963e6292f87f5b2cf0e5a97f02b1d381aebc2a3be2ca` | 0 |
| crates/cairo-lang-sierra-generator/src/pre_sierra.rs | 5826 | `1158fa380f4ae04d546ebdd3d95a2f95ef51993015ab6c0390f1edb336dfee1f` | 0 |
| crates/cairo-lang-sierra-generator/src/program_generator.rs | 18258 | `dba4aeaf736264f736d2b91f3264de5abe1c4b18eb553b632f349218a8d90a3b` | 0 |
| crates/cairo-lang-sierra-generator/src/replace_ids.rs | 8790 | `67df8f245c5a65cc484a1154d0ab6d8902864de6c007e936a65404ca2ab1af85` | 0 |
| crates/cairo-lang-sierra-generator/src/resolve_labels.rs | 4078 | `e744e0badaccc514d36bf9bdef6ed3466d9ec097ec888297c7b076e0d91b34cb` | 0 |
| crates/cairo-lang-sierra-generator/src/specialization_context.rs | 2235 | `9575217c3536ed0e1b8bfcfa93eaf4ceed8d264366d6a3461bc320f8882e484e` | 0 |
| crates/cairo-lang-sierra-generator/src/store_variables/known_stack.rs | 6986 | `ef9501a884d1ae60a22092d9eecd7abc27c9688d8d9c1487480ac084e9e3e378` | 0 |
| crates/cairo-lang-sierra-generator/src/store_variables/mod.rs | 25303 | `3b295e91b0571f98b89f0d2667c9c02ae7ef4eb4e58ef8cd3b7dc8a7a1946c53` | 0 |
| crates/cairo-lang-sierra-generator/src/store_variables/state.rs | 7846 | `e94c9d536cb09d5107d00c2e813c6e61e01a6ec384141aeee2e7c5a06463d203` | 0 |
| crates/cairo-lang-sierra-generator/src/types.rs | 11635 | `7f0d066312cbb9c4d674745adf2b2d571e66663fec4a773bffcfa2e1edb67915` | 0 |
| crates/cairo-lang-sierra-generator/src/utils.rs | 20935 | `d0bdd34307a0e9e353c2e13acf085ba0e5b51160da58af2f14432dea13a2927b` | 0 |
| crates/cairo-lang-sierra-to-casm/Cargo.toml | 1283 | `47b9bf575d4e324120770b608e0f2efe131a66dbddf161cd33a9708e0c69da1c` | 0 |
| crates/cairo-lang-sierra-to-casm/src/annotations.rs | 22289 | `06c81b0cafa2b83981c8e0a1f1e7e30bae6dd07fdb003f60484ae1730b2142fb` | 0 |
| crates/cairo-lang-sierra-to-casm/src/circuit.rs | 1229 | `fcffe45b5ef74d257a389035f1bf7ea4e57bd5eecd84d45dca09db53eef53544` | 0 |
| crates/cairo-lang-sierra-to-casm/src/compiler.rs | 30215 | `522cf0dbbd91b98908869825591bad9a6d018323f3216012098482174383a08d` | 0 |
| crates/cairo-lang-sierra-to-casm/src/environment/ap_tracking.rs | 616 | `2272a16ed69e1c5c46efe6d1f8513084d37be31a5979116fb2fd9805cc07a1d0` | 0 |
| crates/cairo-lang-sierra-to-casm/src/environment/frame_state.rs | 4596 | `0ab90267afa318932ebfa12d5f2ed21a21c458d37951d9b769677a7d127e79f6` | 0 |
| crates/cairo-lang-sierra-to-casm/src/environment/gas_wallet.rs | 2105 | `b6a75149eca42f911674f17b3a8d4777eb8fe3c3d02393203acaaff665685137` | 0 |
| crates/cairo-lang-sierra-to-casm/src/environment/mod.rs | 2584 | `0a911694273206a60eab82e02800137e8d5b4eb32727b5b67dbe9827fe753256` | 0 |
| crates/cairo-lang-sierra-to-casm/src/invocations/array.rs | 20140 | `4aea928916df27b75544bdf8e32024133ce0d19571afb7a0b351759c6a733acc` | 0 |
| crates/cairo-lang-sierra-to-casm/src/invocations/bitwise.rs | 1229 | `d51477ade4fce34c37bf3c9f5a4c245b15627a29bca94110fe59d969a6880e98` | 0 |
| crates/cairo-lang-sierra-to-casm/src/invocations/blake.rs | 1914 | `8aca5d84230addba16cd17de3a36390c8742003aaaef38d0c15665d0af670833` | 0 |
| crates/cairo-lang-sierra-to-casm/src/invocations/boolean.rs | 3251 | `775505bcc7867d91a2c3fc764f2a6cf05f6a1977c7fb43786d1cba93845c59d9` | 0 |
| crates/cairo-lang-sierra-to-casm/src/invocations/boxing.rs | 4097 | `8e54f54a8ebfdfde62f97418096eb4bf7c9a17773e0b40fb3296ac05d5868080` | 0 |
| crates/cairo-lang-sierra-to-casm/src/invocations/bytes31.rs | 940 | `9cdb770b0670b77c3364db2c824aece01ef9383455dc61e41f0d33525efa2955` | 0 |
| crates/cairo-lang-sierra-to-casm/src/invocations/casts.rs | 9079 | `c739825160e22ab33135211361cd9fc64944f89eccc31a56e4ced4fb3c201760` | 0 |
| crates/cairo-lang-sierra-to-casm/src/invocations/circuit.rs | 23950 | `436195e40b5b63e50a8e53ce03f6f20f55e7026173c8e998694482cd32f9e724` | 0 |
| crates/cairo-lang-sierra-to-casm/src/invocations/const_type.rs | 2512 | `ef1a24e051a0b694543b2a979ab2511a1cd459ca5ca819b4dd3782152bea1804` | 0 |
| crates/cairo-lang-sierra-to-casm/src/invocations/debug.rs | 1299 | `d35e3fe54d20b1bd69dc2644e9a7af5f716f3cbcc473a74779bea6a9e62702c9` | 0 |
| crates/cairo-lang-sierra-to-casm/src/invocations/ec.rs | 16612 | `a15f1d89b8045571643e2ff737b6c3fef5ac70f324c2d9cbffb482f852ddca72` | 0 |
| crates/cairo-lang-sierra-to-casm/src/invocations/enm.rs | 20273 | `9329d25f4d185b9117af3c35a5ce5c252cbaba3b5d47a3a8b8ddfd4865b79257` | 0 |
| crates/cairo-lang-sierra-to-casm/src/invocations/felt252.rs | 3992 | `ec63ad1f7cc35827639011f34cca26796cfc3d5c870274f75328558daed3b747` | 0 |
| crates/cairo-lang-sierra-to-casm/src/invocations/felt252_dict.rs | 34762 | `44d344bba719872a599fd73167947f9a5f299f515277286199266d22035faad8` | 0 |
| crates/cairo-lang-sierra-to-casm/src/invocations/function_call.rs | 1726 | `146f1bd5558bd7a16b73e2b64d36eedb829cab5c536fe51fb1a1455470c47a61` | 0 |
| crates/cairo-lang-sierra-to-casm/src/invocations/gas.rs | 12880 | `33683e857d4103801b3e52ae0844e2ccc805f42a1c6a326347045e8b0c8b208f` | 0 |
| crates/cairo-lang-sierra-to-casm/src/invocations/gas_reserve.rs | 1848 | `aa9244587acf95abe808d6b37cba1710338aa82dacfbac389c111cfbac065fbf` | 0 |
| crates/cairo-lang-sierra-to-casm/src/invocations/int/bounded.rs | 13336 | `10ea21047b19bed493e13c02ecd1c258813ce028ed8b218fae04c1fa040076e1` | 0 |
| crates/cairo-lang-sierra-to-casm/src/invocations/int/mod.rs | 5810 | `162f4afcc9dab40c0ee01f5c0dfa48be905bfdfa51e99279c06dfeb6c90d7c0b` | 0 |
| crates/cairo-lang-sierra-to-casm/src/invocations/int/signed.rs | 6707 | `e37e3610c8f846b872a899e3491b6240ce135d28b0c864ad6ce1e42fd9498272` | 0 |
| crates/cairo-lang-sierra-to-casm/src/invocations/int/signed128.rs | 1081 | `0e6d441c1f95af91ee11fca7eda31f01f8a2215fa11f5efa1c9d3f36d0ebe250` | 0 |
| crates/cairo-lang-sierra-to-casm/src/invocations/int/unsigned.rs | 6742 | `e34bc55fb3b0806ed0dc70b54e108505ccfc1388e4f2ba8b3a1e1f6e2c80cb30` | 0 |
| crates/cairo-lang-sierra-to-casm/src/invocations/int/unsigned128.rs | 16361 | `ebcbd7b7c0f00386ee8692c9b91377e79164390c611468762f5953d59f99ad3f` | 0 |
| crates/cairo-lang-sierra-to-casm/src/invocations/int/unsigned256.rs | 22425 | `cadf78a5c6351cc79cc7a14129990ef78a21e55b93651358ccab989ebf47b500` | 0 |
| crates/cairo-lang-sierra-to-casm/src/invocations/int/unsigned512.rs | 8351 | `9c671e0073fa695cd8841002e6c45aff7eb594f6f50b1f2803cebef1cb562441` | 0 |
| crates/cairo-lang-sierra-to-casm/src/invocations/mem.rs | 6406 | `b9a48d9e7bf8113819d43465bde6e8db5d4f9c842422c97bc5ec5b8945dc31d8` | 0 |
| crates/cairo-lang-sierra-to-casm/src/invocations/misc.rs | 11998 | `38b4d607e5034490df23fcb069a3d49cc2ae065e00d6f6a9b4f5847667894b78` | 0 |
| crates/cairo-lang-sierra-to-casm/src/invocations/mod.rs | 33234 | `627df5e90a44cd2c8ae5f826b2139db1c2b304b36598135f41513847d53f275e` | 0 |
| crates/cairo-lang-sierra-to-casm/src/invocations/nullable.rs | 2132 | `fff675671e7e1db055d6f044ba099386baffed86d49f21a809365de5065e1d75` | 0 |
| crates/cairo-lang-sierra-to-casm/src/invocations/pedersen.rs | 1374 | `c80ee865cc8aca9e24bcdc73c0aaa34dd75987c0941e44870f113de91c2cdc52` | 0 |
| crates/cairo-lang-sierra-to-casm/src/invocations/poseidon.rs | 1476 | `c8d3efa310a6e3a90b827a01a78ecb061993dfe928a4d41d8df95206e3477561` | 0 |
| crates/cairo-lang-sierra-to-casm/src/invocations/qm31.rs | 6768 | `cc48e6d879ceb7ec85cd69d19ac735bcc7d3cc6ed76b143fa567b4ff0e584416` | 0 |
| crates/cairo-lang-sierra-to-casm/src/invocations/range.rs | 3388 | `ad97da4048ea0c37ba113aed1f6cc196439c334a6e67f549dcd610954be937e1` | 0 |
| crates/cairo-lang-sierra-to-casm/src/invocations/range_reduction.rs | 4930 | `d5fcf66b9e18fbe2437b0dd28ac51be757964a8d928a4f30a681244114cb3da7` | 0 |
| crates/cairo-lang-sierra-to-casm/src/invocations/squashed_felt252_dict.rs | 541 | `b0660d114e0d9feec38c8d4b8bda36f6c1069984de64451d1dce85722a21dd76` | 0 |
| crates/cairo-lang-sierra-to-casm/src/invocations/starknet/mod.rs | 8819 | `6777a75df5be190a86110e9a38d138aa0c668766dae38dd6c194ba6e4cba7556` | 0 |
| crates/cairo-lang-sierra-to-casm/src/invocations/starknet/secp256.rs | 1966 | `0bae520e54dfa5e86c20df4cd3ebe6feb96be67c71fd89b0ce43cfc4547a20f3` | 0 |
| crates/cairo-lang-sierra-to-casm/src/invocations/starknet/storage.rs | 3021 | `149a0623dc70d52ac813f420759ce7b8f72405f39622629ace2a22a064fce9d4` | 0 |
| crates/cairo-lang-sierra-to-casm/src/invocations/structure.rs | 4193 | `80a8d0fa76c6938e69a94874754eb629ac953e4c561580c9ca7dfb7f4748adb1` | 0 |
| crates/cairo-lang-sierra-to-casm/src/invocations/trace.rs | 876 | `765e19ebf445c4a3e70739ff101746435b186a6e10063c85f05661f879139982` | 0 |
| crates/cairo-lang-sierra-to-casm/src/invocations/unsafe_panic.rs | 562 | `fd644ddc10b083c4b7a556baa3119daed4014bb163b5935db6594f8400983d5b` | 0 |
| crates/cairo-lang-sierra-to-casm/src/lib.rs | 317 | `3a6d2b2e4cdb08b80214a495270ffc17f8eeda8a980a73105238a037f078976f` | 0 |
| crates/cairo-lang-sierra-to-casm/src/metadata.rs | 6255 | `72e7d5a09bbcddf2836fd0f720cd0688cf99bb59bc885e58fefe764c50639e31` | 0 |
| crates/cairo-lang-sierra-to-casm/src/references.rs | 7424 | `72acc4d75f259468939f68df9cc79307e69ea6ba59866fa69eaf3a38e184729e` | 0 |
| crates/cairo-lang-sierra-to-casm/src/relocations.rs | 6266 | `c0ff6f1b2ffc92e74328d662a1d454d85e43252b72cd30d344eea3ee8636d180` | 0 |
| crates/cairo-lang-sierra-type-size/Cargo.toml | 366 | `240984359ba8a1e4f73a9305df42751d97ac326c34f45f4e64b39d356ad56d16` | 0 |
| crates/cairo-lang-sierra-type-size/src/lib.rs | 7592 | `db78a7ef6c705b0d45ba782b576550ff092be1b1094b93458b0967d6f09b6ac4` | 0 |
| crates/cairo-lang-starknet/Cargo.toml | 2142 | `6a1360c1cca1097b573b751d708918ff71fa8092c1b17dadb8ec8cfdfbef7ea5` | 0 |
| crates/cairo-lang-starknet/src/abi.rs | 41779 | `381a37251032046c995613128b75696940e06343ed8415a25fc2aca474ea86ad` | 0 |
| crates/cairo-lang-starknet/src/aliased.rs | 649 | `38da360be02f8e593caaf6b3e2fd9c120040cddfa7e43bdb5a0f95d73289b937` | 0 |
| crates/cairo-lang-starknet/src/analyzer.rs | 13388 | `9a9d9a06288c9beba04cb98460e8884a9432272cfebdefeb2b96aab758f13422` | 0 |
| crates/cairo-lang-starknet/src/compile.rs | 11380 | `9933fdb854db7fd63bb9d0f20bee87757b9b75a83dc0650e57f3d7b49b9ffcf5` | 0 |
| crates/cairo-lang-starknet/src/contract.rs | 16046 | `c3cd61b1b1cbebe22d82ed0c02c77019d468448157f6f9d98f4b06af2a4d542b` | 0 |
| crates/cairo-lang-starknet/src/inline_macros/get_dep_component.rs | 4687 | `81a782b89f8cf97f6354eaeff56c814f5dd65c2f2dac2f4d79af6d7f94268a1a` | 0 |
| crates/cairo-lang-starknet/src/inline_macros/mod.rs | 45 | `16fd1d759add691ed9c24b26dda646ad9eda79fb7240f14c752ac74bdedc7637` | 0 |
| crates/cairo-lang-starknet/src/inline_macros/selector.rs | 2307 | `cca3bf5b0a97993fc98aecea0036e6bf767fb0d7cefc0a202b3feca161240e31` | 0 |
| crates/cairo-lang-starknet/src/lib.rs | 1182 | `c348847751678d4de26eebd99d5123b4c25c071f36de8fd435981e9d09790e45` | 0 |
| crates/cairo-lang-starknet/src/plugin/aux_data.rs | 1541 | `81291dd720309acabb0c0a26222be996df1853eb058c5654b0fb0d9e3ee555a7` | 0 |
| crates/cairo-lang-starknet/src/plugin/consts.rs | 3802 | `3eaae97df33b2bfa30bb96e6c0123ff3433ac797db3af9670f636cce5acd8098` | 0 |
| crates/cairo-lang-starknet/src/plugin/derive/event.rs | 14301 | `e8647c159b45677bb7e46110bf9c597a7fbba459be52698dc8c93c525071d731` | 0 |
| crates/cairo-lang-starknet/src/plugin/derive/mod.rs | 2050 | `6227361b246cf3c4524c080c65512dc6cb06b8550e6c09785c7497b516249622` | 0 |
| crates/cairo-lang-starknet/src/plugin/derive/store.rs | 15777 | `a7eff76b3d88daa8b417f7b2e860a862866cdd1cdc5851a151705593b26b149a` | 0 |
| crates/cairo-lang-starknet/src/plugin/dispatcher.rs | 27474 | `7fdda5a7c96461c76447035b6e211e65b4822429a20dec4f13e0ee81b86fd3d2` | 0 |
| crates/cairo-lang-starknet/src/plugin/embeddable.rs | 9055 | `4d51e3fc753f7b0777881054db9c4d5b07d53c3c03517f0b1fadb75f43e45dc6` | 0 |
| crates/cairo-lang-starknet/src/plugin/entry_point.rs | 15108 | `3fc15ee6c59e2a4b0a798dd25a56eafd9063df17a2d3e205dab21d5ead226dca` | 0 |
| crates/cairo-lang-starknet/src/plugin/events.rs | 3925 | `454e0ffa68531a86d1f889feb387db5b20760a90728469cc9c21fbb87ae00c44` | 0 |
| crates/cairo-lang-starknet/src/plugin/mod.rs | 3736 | `91f056fae747fc9cef893b8d868fcef55fe17aee51094fc8aa037ea38ad07a0e` | 0 |
| crates/cairo-lang-starknet/src/plugin/starknet_module/component.rs | 18599 | `c6a336d75e0571f1ba9325648a680602e954f7906541e829fab22f1e61ab14b3` | 0 |
| crates/cairo-lang-starknet/src/plugin/starknet_module/contract.rs | 32103 | `c61fc50f0f6d6ca2a1ee5cf84081a722a503fe837c064ffe1c0a285152f45499` | 0 |
| crates/cairo-lang-starknet/src/plugin/starknet_module/generation_data.rs | 2813 | `c53524f10caaf387d871216808591c295f37b3126e131626479873ddb064653e` | 0 |
| crates/cairo-lang-starknet/src/plugin/starknet_module/mod.rs | 9931 | `6617015634a6f58154d3becfec6fe381409de9b325a8e3e637117ed337138c34` | 0 |
| crates/cairo-lang-starknet/src/plugin/storage.rs | 9473 | `6e1536d861dd31cef2eaeb8af42cab2972afaef82538fac551434b9b146f62d6` | 0 |
| crates/cairo-lang-starknet/src/plugin/storage_interfaces.rs | 36520 | `762e142ff07dee6f49a887c2c7e12f03683af522b5c263485fe3528693a20291` | 0 |
| crates/cairo-lang-starknet/src/plugin/utils.rs | 8745 | `8a48739b3844d3f6466d5daf32b0337e93856427ee94b4ebf371d948fe914ec6` | 0 |
| crates/cairo-lang-starknet-classes/Cargo.toml | 1430 | `dbaa0518f6a005070eccfeef8e20dc4703f55edd1d7bc2afb52009038f883d19` | 0 |
| crates/cairo-lang-starknet-classes/src/abi.rs | 6334 | `239701f9af14e798d7652ce509adb8c9663b16de1aba4087f2b0232910834a90` | 0 |
| crates/cairo-lang-starknet-classes/src/allowed_libfuncs.rs | 5759 | `f04ae3fa8baaff30672e1fe397b9c6c764b9e646d73efea19bfe381a9e9afaac` | 0 |
| crates/cairo-lang-starknet-classes/src/casm_contract_class.rs | 27208 | `bbf1f0e9d0cff5d47002a5efbea90b42d0933cc24a742895777423f9f2a53532` | 0 |
| crates/cairo-lang-starknet-classes/src/compiler_version.rs | 1496 | `47ed2a5b52f0e682d83edccdd06f78cda603fa2f754f16285739fd42c7cd4a74` | 0 |
| crates/cairo-lang-starknet-classes/src/contract_class.rs | 6618 | `126d7933e29c75ee15e9887cd6fe1904e2a7e5fbf38e624c105fcdb0fc3e3da1` | 0 |
| crates/cairo-lang-starknet-classes/src/contract_segmentation.rs | 7240 | `8fed6d566fc8b705c938cdf113af1f026f1c13d6b4db6fcca3121552550e4abf` | 0 |
| crates/cairo-lang-starknet-classes/src/felt252_serde.rs | 24171 | `4d25743988ab34f0859ca27de6c9cabbad4a446cd8be244119e0e1bf9dc65a9b` | 0 |
| crates/cairo-lang-starknet-classes/src/felt252_vec_compression.rs | 3910 | `7d5de620428ea451b8d3097003e25594c9db2a5edb6d7aab8369db8826d85c67` | 0 |
| crates/cairo-lang-starknet-classes/src/keccak.rs | 445 | `5c1f594e59fc02b0ed542f735856072afb4f72f139faa6b81fce5f295a5e6f84` | 0 |
| crates/cairo-lang-starknet-classes/src/lib.rs | 570 | `b521745e338003fb09016ab7de0cca3c78154897741907c2f751a6c5c187bc7f` | 0 |
| crates/cairo-lang-syntax/Cargo.toml | 1035 | `eda9a67c2b8c7ca4134d9c76b36546df594a16886a8302ac79dcc2c7f2f2d556` | 0 |
| crates/cairo-lang-syntax/src/attribute/consts.rs | 3199 | `ecc03a3bd97576d00dcf18379d29f6239ccda22ea79fd24c42798f43d82aa48f` | 0 |
| crates/cairo-lang-syntax/src/attribute/mod.rs | 36 | `6616808eb02f9517ce92123f6af2c82fb04de0badf90321190bc7961e22f9943` | 0 |
| crates/cairo-lang-syntax/src/attribute/structured.rs | 6238 | `b4159474031392ebf99a707cf828753c9b7a0a9cd58f70df4cf675405e189ab1` | 0 |
| crates/cairo-lang-syntax/src/lib.rs | 108 | `43b235fe8a4e879d568641754be85aca2fd01cfa85150dcc7a490e22c4432f4b` | 0 |
| crates/cairo-lang-syntax/src/node/ast.rs | 1587267 | `b26a1df700db9d3b96fb5a1ee10a1a16c174858a0807d4ff40bdc2d622a67234` | 0 |
| crates/cairo-lang-syntax/src/node/ast_ext.rs | 4359 | `3cf597a94388635e92cbb989a6422c59baec18ee1f5e9ea143251b22c5482fd3` | 0 |
| crates/cairo-lang-syntax/src/node/db.rs | 327 | `996b0488dd22cd764af7e68663e71d27795d8df3391ad1ffc3c1da68cacda1f2` | 0 |
| crates/cairo-lang-syntax/src/node/element_list.rs | 1800 | `14c40b5bcb89c7fa680ab2b6e893914d2b45c3b4dc299e7a81cdc108d440f61f` | 0 |
| crates/cairo-lang-syntax/src/node/green.rs | 1114 | `93d75c996ecfbce693e8e43229d4dc5afd9cc9bfe790693f4234df8de0fe0dc2` | 0 |
| crates/cairo-lang-syntax/src/node/helpers.rs | 44261 | `16994ab0212961a8cd6a4d8da6cdced7d9803aab3c5b45a0265a6a55153d1a91` | 0 |
| crates/cairo-lang-syntax/src/node/ids.rs | 2186 | `3689e50a47fbc539c418ff56e5e53b35df62ec324c410e5100c704fa0def6833` | 0 |
| crates/cairo-lang-syntax/src/node/iter.rs | 3789 | `76cf8662e61ad175f84201894f84b951fd79a4f49fae4070a2e8fdfa315ff1fe` | 0 |
| crates/cairo-lang-syntax/src/node/key_fields.rs | 16798 | `bf6d4796017cc958799a7ccc384356124a0a51abe0e892dc8073a40ed49fb2af` | 0 |
| crates/cairo-lang-syntax/src/node/kind.rs | 18270 | `aaf0845d07a0979fdb67be477255d41b1580b30b064d217baa4d8472ef48c661` | 0 |
| crates/cairo-lang-syntax/src/node/mod.rs | 36780 | `5397d59a3439cf29c5540c0d840c4785401e179a87aa30f3ffa541a872d3c766` | 0 |
| crates/cairo-lang-syntax/src/node/stable_ptr.rs | 962 | `c5bd56f99e85bcd2b0a503a1aaa82b2428a09543fea1ee722e927c13e755b3a9` | 0 |
| crates/cairo-lang-syntax/src/node/with_db.rs | 4853 | `3a56dca38c04674b5dfed9d43f512c9a907b25732da969313d5e255f3db33b7b` | 0 |
| crates/cairo-lang-syntax-codegen/Cargo.toml | 560 | `6465f50eb26d90b340b11173ddc19772a701df2c7e32dccdd43c33e2173f9f7d` | 0 |
| crates/cairo-lang-syntax-codegen/src/cairo_spec.rs | 51368 | `d679af4a2baf50c791a1d34c71935f63367c1f0cb059b2d5e6af4038b59900d8` | 0 |
| crates/cairo-lang-syntax-codegen/src/generator.rs | 31277 | `14a8766462d4ed9152b796a4cca8dcd5241b3128201ddd931814fd8db43b23aa` | 0 |
| crates/cairo-lang-syntax-codegen/src/lib.rs | 128 | `d8aa0047699da6e84a71b30f660d2f7333793f8d86250f1a93d3bf238f990ca2` | 0 |
| crates/cairo-lang-syntax-codegen/src/spec.rs | 7992 | `3338b1ad4c56675835596855e8eb055754652ec3b64a586b08d1e41751f769c0` | 0 |
| crates/cairo-lang-test-plugin/Cargo.toml | 1581 | `b1056e8fb5df40d95dbc246d3bb01613699f18993930fb4645718063a6296f15` | 0 |
| crates/cairo-lang-test-plugin/src/inline_macros/assert.rs | 10538 | `6e130200a84abf3ded29ccf89ee9a1783a3c0eb19b7d88a14af894b8b0dc9deb` | 0 |
| crates/cairo-lang-test-plugin/src/inline_macros/mod.rs | 16 | `f8d0c219a61c7f7865511f7b329744702d7cc68aaf1200449a0a86770386b4a7` | 0 |
| crates/cairo-lang-test-plugin/src/lib.rs | 12890 | `feba47115073e710f534246a8a24b6bc0b7d763fd90123f284299e37f3e2ee36` | 0 |
| crates/cairo-lang-test-plugin/src/plugin.rs | 1416 | `6a33d61d518943b7c36ad383dee8033219065edd9472a02ef8924ee43249269e` | 0 |
| crates/cairo-lang-test-runner/Cargo.toml | 1248 | `4d18dc8ff3511bff3818cea60b3832a0660095e6351518a99203a2eb41d59ebd` | 0 |
| crates/cairo-lang-test-runner/src/lib.rs | 19871 | `1c9cff406327f41db978a5671fa62f96380bc672c01e977c00c615f9306b4287` | 0 |
| crates/cairo-lang-test-utils/Cargo.toml | 1325 | `c3eb4b1d2ed4161cf9f3e06aed0e421921c876a2ac9bda8e10c9828966f8f152` | 0 |
| crates/cairo-lang-test-utils/src/lib.rs | 4970 | `459dbf11d40b74b139ef405df52e0df64d14cf67380224eb9cd36601ab4f9918` | 0 |
| crates/cairo-lang-test-utils/src/parse_test_file.rs | 17539 | `b3feee64aaa5083eed39d204000f3c4672f5966375e7352e19d2ba4b0bb57369` | 0 |
| crates/cairo-lang-utils/Cargo.toml | 1515 | `91662f18231120a839ea0b744f93bc4e79a5a4c28747b714fb2974f3705fed13` | 0 |
| crates/cairo-lang-utils/src/bigint.rs | 7681 | `467462418564a70118ddc9c606c09e9affc7ad32f47cda10dfe50660befadbe6` | 0 |
| crates/cairo-lang-utils/src/byte_array.rs | 197 | `2fea15a510ae3b46b4391ce7fd1da8dce1610112af8d035ce28a6662da4a80f6` | 0 |
| crates/cairo-lang-utils/src/casts.rs | 622 | `b2948700af813fd93db652fde0c5034059d0120103c7d212511646ec18629947` | 0 |
| crates/cairo-lang-utils/src/collection_arithmetics.rs | 4302 | `64b733f781074df0ef3b02fd311dd43741bccb30b850a7ed77625c79e7b61e82` | 0 |
| crates/cairo-lang-utils/src/deque.rs | 1794 | `2f186c8c526e45c1ab4800054ed09db02f426be213bbeed45a587d801756370e` | 0 |
| crates/cairo-lang-utils/src/extract_matches.rs | 1904 | `7d4d4287530787ae8fcc79f1b527a45e53fbc9870a77cb6b2fc30a67828a4510` | 0 |
| crates/cairo-lang-utils/src/graph_algos/feedback_set.rs | 4244 | `084b1a4c871046016b2d02296b7314da9855bb0a9fb9de6f3992a0614ed4c72f` | 0 |
| crates/cairo-lang-utils/src/graph_algos/graph_node.rs | 1219 | `84b31e1b638c821fd8b71c1b3fbb756a6245dcfb94e4c1636915fa611b3bcf32` | 0 |
| crates/cairo-lang-utils/src/graph_algos/mod.rs | 105 | `484aef560b14e85e56dbd6e4c46d4472cacd651c8a992ab9f7960552f40d6f01` | 0 |
| crates/cairo-lang-utils/src/graph_algos/scc_graph_node.rs | 849 | `b984f5b04f391a21fe3b560b30c6cff3616e35ee1fb3ff73bcc2ab8c9614ffd6` | 0 |
| crates/cairo-lang-utils/src/graph_algos/strongly_connected_components.rs | 4859 | `79e4e20fa47056c42537109a2480e78e300fc11ad73170c1470ab749edab606d` | 0 |
| crates/cairo-lang-utils/src/heap_size.rs | 10993 | `ed70e37d8e9b8a2c4980ae81204ec8edd638adc30b33a39866a89b1ea582024c` | 0 |
| crates/cairo-lang-utils/src/iterators.rs | 313 | `c451ca43774c3cb5df7eca24e63c8c9a7db96b955698f6b070ba28d277ce8883` | 0 |
| crates/cairo-lang-utils/src/lib.rs | 5081 | `903884ce4c523e5bca7b6f420a7f8bde0d82656665353f98d81f12c2925c29de` | 0 |
| crates/cairo-lang-utils/src/logging.rs | 2707 | `a485c2cd4cdb89964382a738d88923db53ebd6ce64cbdf12c398c0248d048295` | 0 |
| crates/cairo-lang-utils/src/ordered_hash_map.rs | 4850 | `80efafe352cc58037414acd1cfa8d0a1deb530e81d19a743ce90c9cf031de5c7` | 0 |
| crates/cairo-lang-utils/src/ordered_hash_set.rs | 3010 | `3d92b201071e5ffe2b5643fb24fb79660111db41814caaefc94cb185b7376922` | 0 |
| crates/cairo-lang-utils/src/small_ordered_map.rs | 2426 | `5e4383edcfe26ba4b9efa5ed60fc75492d210a4ec96f7c6ff21d8d8083c57ea6` | 0 |
| crates/cairo-lang-utils/src/unordered_hash_map.rs | 12795 | `5465e8f07fe63cad2291180063ebe136616753637689d4f3c7d6d109ffe924bc` | 0 |
| crates/cairo-lang-utils/src/unordered_hash_set.rs | 3763 | `68cb657c870203a100879692ed73b5fe90c36238bc1f38e32b096c7fbdfe60e3` | 0 |
| ensure-no_std/.cargo/config.toml | 42 | `285033faa15221410d801d5394381ae495890d37cc60b6c0aff0b7d08beda7b8` | 0 |
| ensure-no_std/Cargo.toml | 391 | `b476920fbefde741529a43a0f9fa7da09e070ff01b5385b9a625133c5f2d0bb0` | 0 |
| ensure-no_std/src/main.rs | 447 | `8cc2e4ea686f58cf1ae1db7029276784d5b9f107cb65197959896ca2d08ea1df` | 0 |
| scripts/check_comment_punctuation.py | 5854 | `57f582217517901ec58426679b422ac4261287ef27dbda3d058d5e77d37ce7c8` | 0 |
