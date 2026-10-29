# Security & Post-Quantum Readiness Audit Report

**Project:** zcash-android-wallet-sdk @ a95780ac00e0 · Electric Coin Company (Zcash) — public repository (passive review)
| | |
|---|---|
| Organization | QSI |
| Report date | 2026-10-28 13:02 UTC |
| Report version | 1 |
| Audit run | 3ef13c60-5290-4ae1-a145-078ea2850fe4 (Document audit) |
| Analyzer engine | qsi-engine 1.2.0 |
| Risk profile | Small technology company |
| Content SHA-256 | `d2c9af625f49db5cb717298783cbe2869e143e524920ee5efa91cd94399bd0e6` |
| Signature key (Ed25519, SHA-256 fingerprint; the signature is the separate file report.sig.json) | `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e` |
> This report presents automated and documented analysis results for the stated scope. It is not a legal opinion, a certification or an attestation of compliance with any standard.

## 1. Executive summary

- Critical: **0**
- High: **0**
- Medium: **6**
- Low: **21**
- Info: **6**

- Confirmed technical vulnerability: 0
- Known vulnerable component: 26
- Confirmed configuration error: 0
- Potential cryptographic risk: 1
- Long-term post-quantum risk: 1
- Improvement recommendation: 4
- Insufficient data: 1

Mosca's inequality (x + y > z): x = 5, y = 3, z = 12 → time available under this scenario. _z is a planning assumption chosen per risk profile, not a prediction. A cryptographically relevant quantum computer is not publicly known to exist today._

Analyst review: 1 confirmed, 0 not applicable, 0 dismissed as false positives.

**Post-quantum maturity: Level 0 of 4 — no post-quantum cryptography.** Next step: Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

## 2. Scope and boundaries

Mode: Document audit

Repository: <https://github.com/zcash/zcash-android-wallet-sdk> @ `a95780ac00e0198c111c6e701126e6688f64a12a` — evidence links open the lines at this commit.

350 files, 2611173 bytes in total, 0 redaction(s); the per-file SHA-256 list is in appendix C.

## 3. Methodology

| Area | Status | Count | Examples |
|---|---|---|---|
| dependencies | checked | 4 | backend-lib/Cargo.lock: 712 dependencies parsed (712 pinned); backend-lib/Cargo.toml: 51 dependencies parsed (1 pinned); build-conventions/buildscript-gradle.lockfile: 27 dependencies parsed (27 pinned) |
| source_code | checked | 338 | backend-lib/build.gradle.kts: 268 lines scanned with 16 rule patterns and 122 registry patterns; backend-lib/build.rs: 101 lines scanned with 16 rule patterns and 122 registry patterns; backend-lib/src/main/java/cash/z/ecc/android/sdk/internal/Backend.kt: 409 lines scanned with 16 rule patterns and 122 registry patterns |
| certificates_and_keys | checked | 1 | responsible_disclosure.md: certificates/keys parsed |
| osv_advisories | checked | 1 | 918 pinned packages queried at OSV.dev; 29 affected (14 of them only in development or build dependencies) |

_Long lists are grouped here; the full per-file list is in the JSON report, signed with the same key._

## 4. Assets examined and not examined

- None

## 5. Architecture overview

Static review of the source tree zcash-android-wallet-sdk at a95780ac00e0198c111c6e701126e6688f64a12a. 350 files analysed; of 2062 files, 261 are test, fuzzing, benchmark or example code and were left out, 1451 are not read by any analyzer, 0 exceed the per-file limit and 0 did not fit the total limit. No requests were sent to the owner's systems.

## 6. Overall security posture

- Indicative posture index: **51** / 100 — _Derived from findings in scope (confirmed and potential issues weighted by severity). Indicative only; not comparable across differently scoped audits._
- Quantum-vulnerable share of inventory: 14.3%

## 7. Detailed findings

### QSI-2026-05179 — SHA-1 used in backend-lib/src/main/java/cash/z/ecc/android/sdk/internal/ext/FileExt.kt

- Severity: **Medium** · Classification: Potential cryptographic risk · Confidence: Medium
> **Analyst review (QSI review, 2026-10-23): confirmed by the analyst.** The finding anchors at the helper, File.getSha1Hash() in backend-lib/src/main/java/cash/z/ecc/android/sdk/internal/ext/FileExt.kt; the use that matters is SaplingParamTool, which downloads the Sapling spend and output parameters from download.z.cash and verifies them against two hard-coded SHA-1 digests (SPEND_PARAM_FILE_SHA1_HASH, OUTPUT_PARAM_FILE_SHA1_HASH). Stated precisely: the property relied on here is second-preimage resistance, which SHA-1 still has — only its collision resistance is broken, and that is not what this check uses. So this is not exploitable as it stands and must not be described as such. It is still the wrong primitive for an integrity check on security-critical cryptographic material, and it is directly relevant to post-quantum readiness: Grover halves preimage security, taking SHA-1 from 160 bits to about 80, below any acceptable margin for parameters with this lifetime. SHA-256 is the correct replacement.
- Affected asset: `file:backend-lib/src/main/java/cash/z/ecc/android/sdk/internal/ext/FileExt.kt`
- Data source: backend-lib/src/main/java/cash/z/ecc/android/sdk/internal/ext/FileExt.kt
- Detection method: Regular-expression matching of language-specific API patterns.
- Analyzer: source_code 1.2.0 · 2026-10-28 13:02 UTC
- Priority score: 38.2 / 100
- CVSS v3.1: not applicable

1 call site(s) of SHA-1 (first at line 50).

**Potential impact.** If used for signatures, password storage, integrity against attackers or token generation, collisions/preimages may be exploitable. Non-security checksums are acceptable.

**Reproduction steps.**

```
Open line 50 in the supplied file backend-lib/src/main/java/cash/z/ecc/android/sdk/internal/ext/FileExt.kt and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [backend-lib/src/main/java/cash/z/ecc/android/sdk/internal/ext/FileExt.kt](https://github.com/zcash/zcash-android-wallet-sdk/blob/a95780ac00e0198c111c6e701126e6688f64a12a/backend-lib/src/main/java/cash/z/ecc/android/sdk/internal/ext/FileExt.kt#L50) · line 50 · SHA-256 a736d03fcbd7dd715bdb2f63c218c283d7c40b13eb7322a475012f339243a37e_

```
   48 | suspend fun File.getSha1Hash(): String {
   49 |     return withContext(Dispatchers.IO) {
   50 |         val messageDigest = MessageDigest.getInstance("SHA-1")
   51 |         inputStreamSuspend().use { fis ->
   52 |             DigestInputStream(fis, messageDigest).use { dis ->
```

**Limitations of the check.** Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Replace with SHA-256/SHA-3 (or Argon2/bcrypt for passwords) where security-relevant.

**Retest procedure.** Re-scan the source and review the call sites listed in the evidence.

### QSI-2026-05184 — block-buffer 0.10.4 is affected by GHSA-qwgh-2vcv-g2f7

- Severity: **Medium** · Classification: Known vulnerable component · Confidence: Low
- Affected asset: `dependency:crates.io/block-buffer@0.10.4`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 13:02 UTC
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

### QSI-2026-05185 — block-buffer 0.11.0-rc.3 is affected by GHSA-qwgh-2vcv-g2f7

- Severity: **Medium** · Classification: Known vulnerable component · Confidence: Low
- Affected asset: `dependency:crates.io/block-buffer@0.11.0-rc.3`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 13:02 UTC
- Priority score: 33.1 / 100
- CVSS v3.1: not applicable

OSV.dev reports GHSA-qwgh-2vcv-g2f7 for crates.io package block-buffer at version 0.11.0-rc.3: block_buffer: panic corrupts inline buffer position. The advisory names no affected functions, so reachability was not determined.

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

### QSI-2026-05189 — rsa 0.9.10 is affected by RUSTSEC-2023-0071 (CVE-2023-49092)

- Severity: **Medium** · Classification: Known vulnerable component · Confidence: Low
- Affected asset: `dependency:crates.io/rsa@0.9.10`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 13:02 UTC
- Priority score: 33.1 / 100
- CVSS v3.1: 5.9 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:N/A:N`)

OSV.dev reports RUSTSEC-2023-0071 (CVE-2023-49092) for crates.io package rsa at version 0.9.10: Marvin Attack: potential key recovery through timing sidechannels. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2023-0071
```

**Evidence.**

_tool_output · [OSV.dev RUSTSEC-2023-0071](https://osv.dev/vulnerability/RUSTSEC-2023-0071) · manifest · SHA-256 6fcc27a80e8a30342b68a229087947db7a952d0facf3cc8d6edbd7abfd150c53_

```
{"id": "RUSTSEC-2023-0071", "aliases": ["CVE-2023-49092", "GHSA-4grx-2x9w-596c", "GHSA-c38w-74pg-36hr"], "modified": "2026-09-14T09:45:02.996132556Z", "summary": "Marvin Attack: potential key recovery through timing sidechannels", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:N/A:N"}], "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (none published yet; see the advisory for mitigations).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-05190 — rustls 0.23.43 is affected by GHSA-2mjx-qc3c-rqvc (RUSTSEC-2026-0285)

- Severity: **Medium** · Classification: Known vulnerable component · Confidence: Low
- Affected asset: `dependency:crates.io/rustls@0.23.43`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 13:02 UTC
- Priority score: 33.1 / 100
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

### QSI-2026-05191 — rustls 0.23.43 is affected by GHSA-c8m5-c952-6cm4 (RUSTSEC-2026-0346)

- Severity: **Medium** · Classification: Known vulnerable component · Confidence: Low
- Affected asset: `dependency:crates.io/rustls@0.23.43`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 13:02 UTC
- Priority score: 33.1 / 100
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

### QSI-2026-05180 — Quantum-vulnerable RSA key (2048-bit) in responsible_disclosure.md

- Severity: **Low** · Classification: Long-term post-quantum risk · Confidence: High
- Affected asset: `file:responsible_disclosure.md#line 11`
- Data source: responsible_disclosure.md
- Detection method: Public key parsing.
- Analyzer: certificates 1.2.0 · 2026-10-28 13:02 UTC
- Priority score: 36.2 / 100
- CVSS v3.1: not applicable

A RSA 2048-bit public key was found (line 11).

**Potential impact.** Long-term risk once a CRQC exists; for key exchange, recorded traffic could be decrypted retroactively.

**Reproduction steps.**

```
Open line 11 in the supplied file responsible_disclosure.md and inspect the quoted lines (see evidence).
```

**Evidence.**

_key · responsible_disclosure.md · line 11 · SHA-256 99f8a76d7955bc1cad612c6fe14ee442ba2c3ba5655096eda02d83c54d97d810_

```
OpenPGP primary key: algorithm ID 1 (RSA) 2048-bit
```

_key · responsible_disclosure.md · line 11 · SHA-256 a744425426415d58dbeef862a6f1d8bcf6b00820639c8784270363d0b6330969_

```
OpenPGP subkey: algorithm ID 1 (RSA) 2048-bit
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability.

**Recommendation.** Inventory and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it..

**Retest procedure.** Re-audit after migration.

### QSI-2026-05193 — rustls 0.23.43 is affected by GHSA-w44r-93j7-qv28 (RUSTSEC-2026-0349)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low
- Affected asset: `dependency:crates.io/rustls@0.23.43`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 13:02 UTC
- Priority score: 28.6 / 100
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

### QSI-2026-05192 — rustls 0.23.43 is affected by GHSA-h2v8-394m-p7vv (RUSTSEC-2026-0348)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/rustls@0.23.43`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 13:02 UTC
- Priority score: 24.3 / 100
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

### QSI-2026-05186 — crypto-bigint 0.5.5 is affected by RUSTSEC-2026-0387 (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/crypto-bigint@0.5.5`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 13:02 UTC
- Priority score: 20.2 / 100
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

### QSI-2026-05187 — h2 0.4.15 is affected by RUSTSEC-2026-0258 (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/h2@0.4.15`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 13:02 UTC
- Priority score: 20.2 / 100
- CVSS v3.1: not applicable

OSV.dev reports RUSTSEC-2026-0258 for crates.io package h2 at version 0.4.15: h2 unbounded empty DATA frames. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0258
```

**Evidence.**

_tool_output · [OSV.dev RUSTSEC-2026-0258](https://osv.dev/vulnerability/RUSTSEC-2026-0258) · manifest · SHA-256 d8694780e4da4b8ee995c62dbd89ea4aef9579bf2c51b2a4b677a2231b8d4edc_

```
{"id": "RUSTSEC-2026-0258", "aliases": ["GHSA-q83h-524g-xf6h"], "modified": "2026-10-12T18:00:10.934581734Z", "summary": "h2 unbounded empty DATA frames", "severity": null, "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Triage the advisory; upgrade to a fixed version (0.4.16) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-05194 — rustls-webpki 0.103.13 is affected by RUSTSEC-2026-0382 (CVE-2026-111943) (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/rustls-webpki@0.103.13`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 13:02 UTC
- Priority score: 20.2 / 100
- CVSS v3.1: not applicable

OSV.dev reports RUSTSEC-2026-0382 (CVE-2026-111943) for crates.io package rustls-webpki at version 0.103.13: Certificate verification may accept distrusted intermediates. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. The advisory names no affected functions, so reachability was not determined.

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

### QSI-2026-05195 — tokio 1.53.1 is affected by RUSTSEC-2026-0386 (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/tokio@1.53.1`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 13:02 UTC
- Priority score: 20.2 / 100
- CVSS v3.1: not applicable

OSV.dev reports RUSTSEC-2026-0386 for crates.io package tokio at version 1.53.1: `AsyncFd::new` and related constructors violate I/O safety. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. The audited code does not name the affected functions (tokio::io::unix::AsyncFd::new, tokio::io::unix::AsyncFd::try_new, tokio::io::unix::AsyncFd::try_with_interest, tokio::io::unix::AsyncFd::with_interest); tokio comes in through other dependencies, which may still call them.

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0386
```

**Evidence.**

_tool_output · [OSV.dev RUSTSEC-2026-0386](https://osv.dev/vulnerability/RUSTSEC-2026-0386) · manifest · SHA-256 f73073a3500a8c1b126e0070756badd87c6af0a88d357d6a1e083bf4f9f96021_

```
{"id": "RUSTSEC-2026-0386", "aliases": [], "modified": "2026-10-23T14:45:03.847864944Z", "summary": "`AsyncFd::new` and related constructors violate I/O safety", "severity": null, "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Triage the advisory; upgrade to a fixed version (1.51.6, 1.53.3) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-05196 — webpki-roots 1.0.9 is affected by RUSTSEC-2026-0381 (CVE-2026-111943) (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/webpki-roots@1.0.9`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 13:02 UTC
- Priority score: 20.2 / 100
- CVSS v3.1: not applicable

OSV.dev reports RUSTSEC-2026-0381 (CVE-2026-111943) for crates.io package webpki-roots at version 1.0.9: Bundled root certificates allow trust in distrusted emSign intermediates. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0381
```

**Evidence.**

_tool_output · [OSV.dev RUSTSEC-2026-0381](https://osv.dev/vulnerability/RUSTSEC-2026-0381) · manifest · SHA-256 a97aff76592b60902cd4b16acc1ea2e7be27cd23fb1cd59575028f4953d51114_

```
{"id": "RUSTSEC-2026-0381", "aliases": ["CVE-2026-111943", "GO-2026-6809", "RUSTSEC-2026-0382", "RUSTSEC-2026-0383"], "modified": "2026-10-21T06:30:02.818201920Z", "summary": "Bundled root certificates allow trust in distrusted emSign intermediates", "severity": null, "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Triage the advisory; upgrade to a fixed version (0.26.11, 1.0.10) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-05197 — zstd 0.13.3 is affected by RUSTSEC-2026-0391 (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/zstd@0.13.3`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 13:02 UTC
- Priority score: 20.2 / 100
- CVSS v3.1: not applicable

OSV.dev reports RUSTSEC-2026-0391 for crates.io package zstd at version 0.13.3: Data from an abandoned stream leaks into the next stream on a reused context. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. The audited code does not name the affected functions (zstd::stream::raw::Decoder::with_context, zstd::stream::raw::Encoder::with_context); zstd comes in through other dependencies, which may still call them.

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0391
```

**Evidence.**

_tool_output · [OSV.dev RUSTSEC-2026-0391](https://osv.dev/vulnerability/RUSTSEC-2026-0391) · manifest · SHA-256 c5a6274e5a4cfb8793fcf3f343ddadadd6d41a200d24a392d8f363faa59b0e78_

```
{"id": "RUSTSEC-2026-0391", "aliases": [], "modified": "2026-10-26T14:00:04.269245609Z", "summary": "Data from an abandoned stream leaks into the next stream on a reused context", "severity": null, "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Triage the advisory; upgrade to a fixed version (0.14.3) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-05198 — zstd-safe 7.2.4 is affected by RUSTSEC-2026-0395 (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/zstd-safe@7.2.4`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 13:02 UTC
- Priority score: 20.2 / 100
- CVSS v3.1: not applicable

OSV.dev reports RUSTSEC-2026-0395 for crates.io package zstd-safe at version 7.2.4: Use-after-free with `CParameter::StableInBuffer`. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. The audited code does not name the affected functions (zstd_safe::CCtx::set_parameter); zstd-safe comes in through other dependencies, which may still call them.

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0395
```

**Evidence.**

_tool_output · [OSV.dev RUSTSEC-2026-0395](https://osv.dev/vulnerability/RUSTSEC-2026-0395) · manifest · SHA-256 cf314e3df3f714ad17083f648e4d6822839805759c13c152cf2b2edcfbba9cdb_

```
{"id": "RUSTSEC-2026-0395", "aliases": [], "modified": "2026-10-26T14:00:06.388344282Z", "summary": "Use-after-free with `CParameter::StableInBuffer`", "severity": null, "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Triage the advisory; upgrade to a fixed version (8.2.0) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-05199 — zstd-safe 7.2.4 is affected by RUSTSEC-2026-0396 (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/zstd-safe@7.2.4`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 13:02 UTC
- Priority score: 20.2 / 100
- CVSS v3.1: not applicable

OSV.dev reports RUSTSEC-2026-0396 for crates.io package zstd-safe at version 7.2.4: `Seekable` reads a NULL or out-of-bounds seek table. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. The audited code does not name the affected functions (zstd_safe::seekable::SeekTable::frame_decompressed_size, zstd_safe::seekable::Seekable::decompress, zstd_safe::seekable::Seekable::decompress_frame, zstd_safe::seekable::Seekable::frame_decompressed_size, zstd_safe::seekable::Seekable::offset_to_frame_index); zstd-safe comes in through other dependencies, which may still call them.

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0396
```

**Evidence.**

_tool_output · [OSV.dev RUSTSEC-2026-0396](https://osv.dev/vulnerability/RUSTSEC-2026-0396) · manifest · SHA-256 46019c3c1c8cc1772c03fcccbfa90a2b7502cdb744481795fef991bd88bf8e23_

```
{"id": "RUSTSEC-2026-0396", "aliases": [], "modified": "2026-10-26T14:00:05.789682118Z", "summary": "`Seekable` reads a NULL or out-of-bounds seek table", "severity": null, "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Triage the advisory; upgrade to a fixed version (8.2.0) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-05200 — zstd-safe 7.2.4 is affected by RUSTSEC-2026-0397 (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/zstd-safe@7.2.4`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 13:02 UTC
- Priority score: 20.2 / 100
- CVSS v3.1: not applicable

OSV.dev reports RUSTSEC-2026-0397 for crates.io package zstd-safe at version 7.2.4: `OutBuffer::around_pos` exposes uninitialized memory. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. The audited code does not name the affected functions (zstd_safe::OutBuffer::around_pos); zstd-safe comes in through other dependencies, which may still call them.

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0397
```

**Evidence.**

_tool_output · [OSV.dev RUSTSEC-2026-0397](https://osv.dev/vulnerability/RUSTSEC-2026-0397) · manifest · SHA-256 e1cc2d6a8e69a560eb15d719dcb988b36e18b940b8913145ec52a73efd0b9fcc_

```
{"id": "RUSTSEC-2026-0397", "aliases": [], "modified": "2026-10-26T14:00:05.089587004Z", "summary": "`OutBuffer::around_pos` exposes uninitialized memory", "severity": null, "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Triage the advisory; upgrade to a fixed version (8.2.0) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-05201 — zstd-safe 7.2.4 is affected by RUSTSEC-2026-0398 (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/zstd-safe@7.2.4`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 13:02 UTC
- Priority score: 20.2 / 100
- CVSS v3.1: not applicable

OSV.dev reports RUSTSEC-2026-0398 for crates.io package zstd-safe at version 7.2.4: `Seekable::decompress` sets a `Vec` length beyond its capacity for offsets past the end. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. The audited code does not name the affected functions (zstd_safe::seekable::AdvancedSeekable::decompress, zstd_safe::seekable::Seekable::decompress); zstd-safe comes in through other dependencies, which may still call them.

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0398
```

**Evidence.**

_tool_output · [OSV.dev RUSTSEC-2026-0398](https://osv.dev/vulnerability/RUSTSEC-2026-0398) · manifest · SHA-256 01887ac4409fe66647c178d3ac91c674dafafb9134960f58c0f4ffcaa080acda_

```
{"id": "RUSTSEC-2026-0398", "aliases": [], "modified": "2026-10-26T14:00:05.092082939Z", "summary": "`Seekable::decompress` sets a `Vec` length beyond its capacity for offsets past the end", "severity": null, "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Triage the advisory; upgrade to a fixed version (8.2.0) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-05202 — zstd-safe 7.2.4 is affected by RUSTSEC-2026-0399 (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/zstd-safe@7.2.4`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 13:02 UTC
- Priority score: 20.2 / 100
- CVSS v3.1: not applicable

OSV.dev reports RUSTSEC-2026-0399 for crates.io package zstd-safe at version 7.2.4: Use-after-free through `init_using_cdict` and `init_using_ddict`. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. The audited code does not name the affected functions (zstd_safe::CCtx::init_using_cdict, zstd_safe::DCtx::init_using_ddict); zstd-safe comes in through other dependencies, which may still call them.

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0399
```

**Evidence.**

_tool_output · [OSV.dev RUSTSEC-2026-0399](https://osv.dev/vulnerability/RUSTSEC-2026-0399) · manifest · SHA-256 dde7c9d1fcd35a89a4e462b7b42373ae75187190ebfffa3876d9e2bba20e386a_

```
{"id": "RUSTSEC-2026-0399", "aliases": [], "modified": "2026-10-26T14:00:05.792431051Z", "summary": "Use-after-free through `init_using_cdict` and `init_using_ddict`", "severity": null, "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Triage the advisory; upgrade to a fixed version (8.2.0) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-05203 — zstd-safe 7.2.4 is affected by RUSTSEC-2026-0400 (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/zstd-safe@7.2.4`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 13:02 UTC
- Priority score: 20.2 / 100
- CVSS v3.1: not applicable

OSV.dev reports RUSTSEC-2026-0400 for crates.io package zstd-safe at version 7.2.4: Use-after-free of a dictionary after a one-shot call on a context with an open stream. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. The audited code does not name the affected functions (zstd_safe::DCtx::decompress, zstd_safe::DCtx::decompress_using_ddict, zstd_safe::DCtx::decompress_using_dict); zstd-safe comes in through other dependencies, which may still call them.

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0400
```

**Evidence.**

_tool_output · [OSV.dev RUSTSEC-2026-0400](https://osv.dev/vulnerability/RUSTSEC-2026-0400) · manifest · SHA-256 12a31cd97694259b60fd13de0204d4257a30facebdbf5eb19bc091d2b54c85f6_

```
{"id": "RUSTSEC-2026-0400", "aliases": [], "modified": "2026-10-26T14:00:05.692077560Z", "summary": "Use-after-free of a dictionary after a one-shot call on a context with an open stream", "severity": null, "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Triage the advisory; upgrade to a fixed version (8.2.0) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-05204 — zstd-safe 7.2.4 is affected by RUSTSEC-2026-0401 (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/zstd-safe@7.2.4`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 13:02 UTC
- Priority score: 20.2 / 100
- CVSS v3.1: not applicable

OSV.dev reports RUSTSEC-2026-0401 for crates.io package zstd-safe at version 7.2.4: Out-of-bounds read in `train_from_buffer` when sample sizes overflow. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. The audited code does not name the affected functions (zstd_safe::train_from_buffer); zstd-safe comes in through other dependencies, which may still call them.

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0401
```

**Evidence.**

_tool_output · [OSV.dev RUSTSEC-2026-0401](https://osv.dev/vulnerability/RUSTSEC-2026-0401) · manifest · SHA-256 8f606743a027e187f8815975be52f1a4018a22a8d8cacc5d66407f974573c3a0_

```
{"id": "RUSTSEC-2026-0401", "aliases": [], "modified": "2026-10-26T14:00:04.231502512Z", "summary": "Out-of-bounds read in `train_from_buffer` when sample sizes overflow", "severity": null, "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Triage the advisory; upgrade to a fixed version (8.2.0) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-05205 — zstd-safe 7.2.4 is affected by RUSTSEC-2026-0402 (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/zstd-safe@7.2.4`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 13:02 UTC
- Priority score: 20.2 / 100
- CVSS v3.1: not applicable

OSV.dev reports RUSTSEC-2026-0402 for crates.io package zstd-safe at version 7.2.4: Heap buffer overflow in `CCtx::try_clone` on a multithreaded context. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. The audited code does not name the affected functions (zstd_safe::CCtx::try_clone); zstd-safe comes in through other dependencies, which may still call them.

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0402
```

**Evidence.**

_tool_output · [OSV.dev RUSTSEC-2026-0402](https://osv.dev/vulnerability/RUSTSEC-2026-0402) · manifest · SHA-256 1659ee65665b5ae755a87f2715370efa327fc3064514c61888dd4fa3a3f32642_

```
{"id": "RUSTSEC-2026-0402", "aliases": [], "modified": "2026-10-26T14:00:05.685817733Z", "summary": "Heap buffer overflow in `CCtx::try_clone` on a multithreaded context", "severity": null, "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Triage the advisory; upgrade to a fixed version (8.2.0) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-05206 — zstd-safe 7.2.4 is affected by RUSTSEC-2026-0403 (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/zstd-safe@7.2.4`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 13:02 UTC
- Priority score: 20.2 / 100
- CVSS v3.1: not applicable

OSV.dev reports RUSTSEC-2026-0403 for crates.io package zstd-safe at version 7.2.4: Uninitialized memory exposed when streaming decompression of a legacy frame fails. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. The audited code does not name the affected functions (zstd_safe::DCtx::decompress_stream); zstd-safe comes in through other dependencies, which may still call them.

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0403
```

**Evidence.**

_tool_output · [OSV.dev RUSTSEC-2026-0403](https://osv.dev/vulnerability/RUSTSEC-2026-0403) · manifest · SHA-256 b1d1701270f636af5d21f2b55cbd122bcd0df90ce4dce6793aa9263b377caddb_

```
{"id": "RUSTSEC-2026-0403", "aliases": [], "modified": "2026-10-26T14:00:05.787441176Z", "summary": "Uninitialized memory exposed when streaming decompression of a legacy frame fails", "severity": null, "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Triage the advisory; upgrade to a fixed version (8.2.0) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-05207 — zstd-safe 7.2.4 is affected by RUSTSEC-2026-0404 (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/zstd-safe@7.2.4`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 13:02 UTC
- Priority score: 20.2 / 100
- CVSS v3.1: not applicable

OSV.dev reports RUSTSEC-2026-0404 for crates.io package zstd-safe at version 7.2.4: Double free in `DCtx::try_clone`. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. The audited code does not name the affected functions (zstd_safe::DCtx::try_clone); zstd-safe comes in through other dependencies, which may still call them.

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0404
```

**Evidence.**

_tool_output · [OSV.dev RUSTSEC-2026-0404](https://osv.dev/vulnerability/RUSTSEC-2026-0404) · manifest · SHA-256 7c25f3932e55150f3788cd8fcee7738d3c905758f825a562b19f78d7e041b0b2_

```
{"id": "RUSTSEC-2026-0404", "aliases": [], "modified": "2026-10-26T14:00:05.092817237Z", "summary": "Double free in `DCtx::try_clone`", "severity": null, "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Triage the advisory; upgrade to a fixed version (8.2.0) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-05208 — zstd-safe 7.2.4 is affected by RUSTSEC-2026-0405 (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/zstd-safe@7.2.4`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 13:02 UTC
- Priority score: 20.2 / 100
- CVSS v3.1: not applicable

OSV.dev reports RUSTSEC-2026-0405 for crates.io package zstd-safe at version 7.2.4: Out-of-bounds read with an out-of-range `InBuffer::pos`. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. The audited code does not name the affected functions (zstd_safe::seekable::SeekableCStream::compress_stream); zstd-safe comes in through other dependencies, which may still call them.

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0405
```

**Evidence.**

_tool_output · [OSV.dev RUSTSEC-2026-0405](https://osv.dev/vulnerability/RUSTSEC-2026-0405) · manifest · SHA-256 aa7a0dd1f301f7767bcd2d2a354fda77b1e2ed887669efac9bdd2bc66db5be81_

```
{"id": "RUSTSEC-2026-0405", "aliases": [], "modified": "2026-10-26T14:00:05.680942523Z", "summary": "Out-of-bounds read with an out-of-range `InBuffer::pos`", "severity": null, "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Triage the advisory; upgrade to a fixed version (8.2.0) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-05209 — zstd-safe 7.2.4 is affected by RUSTSEC-2026-0406 (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/zstd-safe@7.2.4`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 13:02 UTC
- Priority score: 20.2 / 100
- CVSS v3.1: not applicable

OSV.dev reports RUSTSEC-2026-0406 for crates.io package zstd-safe at version 7.2.4: Use-after-free when changing a multithreaded context with an unfinished frame. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. The audited code does not name the affected functions (zstd_safe::CCtx::disable_dictionary, zstd_safe::CCtx::init, zstd_safe::CCtx::load_dictionary, zstd_safe::CCtx::ref_cdict, zstd_safe::CCtx::ref_prefix, zstd_safe::CCtx::reset …); zstd-safe comes in through other dependencies, which may still call them.

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0406
```

**Evidence.**

_tool_output · [OSV.dev RUSTSEC-2026-0406](https://osv.dev/vulnerability/RUSTSEC-2026-0406) · manifest · SHA-256 deca0b7103bdc0c3ed051bcdb0dbd3d63e215fecdbdba6a7f24f9fb8c2e93ecd_

```
{"id": "RUSTSEC-2026-0406", "aliases": [], "modified": "2026-10-26T14:00:05.095427051Z", "summary": "Use-after-free when changing a multithreaded context with an unfinished frame", "severity": null, "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Triage the advisory; upgrade to a fixed version (8.2.0) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-05210 — zstd-sys 2.0.16+zstd.1.5.7 is affected by RUSTSEC-2026-0410 (no severity rating)

- Severity: **Info** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/zstd-sys@2.0.16+zstd.1.5.7`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 13:02 UTC
- Priority score: 17.1 / 100
- CVSS v3.1: not applicable

OSV.dev reports RUSTSEC-2026-0410 for crates.io package zstd-sys at version 2.0.16+zstd.1.5.7: WebAssembly allocator shim corrupts memory on allocation failure. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. The advisory affects only wasm32 targets; the repository declares the Rust targets armv7-linux-androideabi, aarch64-linux-android, i686-linux-android, x86_64-linux-android.

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0410
```

**Evidence.**

_tool_output · [OSV.dev RUSTSEC-2026-0410](https://osv.dev/vulnerability/RUSTSEC-2026-0410) · manifest · SHA-256 1e892df4ce7c9911f01547e4a80d1fb3ea5a27b8c1c89c0514917e08bbf3bdc5_

```
{"id": "RUSTSEC-2026-0410", "aliases": [], "modified": "2026-10-26T14:00:05.788985783Z", "summary": "WebAssembly allocator shim corrupts memory on allocation failure", "severity": null, "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Triage the advisory; upgrade to a fixed version (2.1.2) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-05211 — 50 advisories in 14 development or build-only Maven package(s)

- Severity: **Info** · Classification: Improvement recommendation · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `dependencies:Maven:non-runtime`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch lookup of exact versions; scope from devDependencies, package-lock.json dev flags, pnpm importers sections, the Cargo.lock graph rooted at the Cargo.toml tables, and — for yarn.lock, which records no scope — the lock graph walked from package.json. Where a runtime requirement cannot be resolved in a lock, that lock is left unclassified rather than risking a package being set aside wrongly.
- Analyzer: dependencies 1.2.0 · 2026-10-28 13:02 UTC
- Priority score: 16.0 / 100
- CVSS v3.1: not applicable

OSV.dev lists 50 advisories (22 rated high or critical) for 14 Maven package(s) that only development or build tooling pulls in (build-conventions/buildscript-gradle.lockfile, build-conventions/gradle.lockfile): e.g. com.google.guava:guava@33.3.1-jre [build]: GHSA-xxph-c9ww-hj94; io.netty:netty-codec@4.1.110.Final [build]: GHSA-3p8m-j85q-pgmj, GHSA-558v-64gr-wgg4, GHSA-mj4r-2hfc-f8p6; io.netty:netty-codec-http@4.1.110.Final [build]: GHSA-38f8-5428-x5cv, GHSA-4mp9-239f-g9hg, GHSA-57rv-r2g8-2cj3, GHSA-6cqp-g7gg-8hr5, GHSA-6jqx-86gh-f27w, GHSA-84h7-rjj3-6jx4, GHSA-8c42-7qj2-3j46, GHSA-f6hv-jmp6-3vwv, GHSA-fghv-69vj-qj49, GHSA-gcjf-9mgh-3p7g, GHSA-hvcg-qmg6-jm4c, GHSA-jppx-w49h-x2qq, GHSA-m4cv-j2px-7723, GHSA-mvh2-crg5-v77c, GHSA-pwqr-wmgm-9rr8, GHSA-q4f6-jm68-57ww, GHSA-v8h7-rr48-vmmv, GHSA-xxqh-mfjm-7mv9; io.netty:netty-codec-http2@4.1.110.Final [build]: GHSA-563q-j3cm-6jxm, GHSA-5x3r-wrvg-rp6q, GHSA-93wv-jw9v-4972, GHSA-c2gf-v879-257j, GHSA-c69g-56f8-xwqj, GHSA-f6hv-jmp6-3vwv, GHSA-prj3-ccx8-p6x4, GHSA-w9fj-cfpg-grvv; io.netty:netty-common@4.1.110.Final [build]: GHSA-389x-839f-4rhx, GHSA-xq3w-v528-46rv. The manifests mark them as such (devDependencies, "dev": true in package-lock.json, pnpm importers sections, [dev-dependencies]/[build-dependencies] reached through Cargo.lock, or — for yarn.lock, which records no scope at all — package.json reached through the lock graph), so they are not part of what ships.

**Potential impact.** They do not reach users of the product. They can affect developer machines and CI (supply chain): a compromised or vulnerable tool can tamper with builds.

**Reproduction steps.**

```
Look the packages listed in the evidence up at https://osv.dev and check their scope in build-conventions/buildscript-gradle.lockfile, build-conventions/gradle.lockfile.
```

**Evidence.**

_tool_output · [OSV.dev (Maven)](https://osv.dev/) · build-conventions/buildscript-gradle.lockfile · SHA-256 dd2231187ca8623fbd0e45b8665e110ab75a9371136018756f17cfa2192b838f_

```
com.google.guava:guava@33.3.1-jre [build]: GHSA-xxph-c9ww-hj94
io.netty:netty-codec@4.1.110.Final [build]: GHSA-3p8m-j85q-pgmj, GHSA-558v-64gr-wgg4, GHSA-mj4r-2hfc-f8p6
io.netty:netty-codec-http@4.1.110.Final [build]: GHSA-38f8-5428-x5cv, GHSA-4mp9-239f-g9hg, GHSA-57rv-r2g8-2cj3, GHSA-6cqp-g7gg-8hr5, GHSA-6jqx-86gh-f27w, GHSA-84h7-rjj3-6jx4, GHSA-8c42-7qj2-3j46, GHSA-f6hv-jmp6-3vwv, GHSA-fghv-69vj-qj49, GHSA-gcjf-9mgh-3p7g, GHSA-hvcg-qmg6-jm4c, GHSA-jppx-w49h-x2qq, GHSA-m4cv-j2px-7723, GHSA-mvh2-crg5-v77c, GHSA-pwqr-wmgm-9rr8, GHSA-q4f6-jm68-57ww, GHSA-v8h7-rr48-vmmv, GHSA-xxqh-mfjm-7mv9
io.netty:netty-codec-http2@4.1.110.Final [build]: GHSA-563q-j3cm-6jxm, GHSA-5x3r-wrvg-rp6q, GHSA-93wv-jw9v-4972, GHSA-c2gf-v879-257j, GHSA-c69g-56f8-xwqj, GHSA-f6hv-jmp6-3vwv, GHSA-prj3-ccx8-p6x4, GHSA-w9fj-cfpg-grvv
io.netty:netty-common@4.1.110.Final [build]: GHSA-389x-839f-4rhx, GHSA-xq3w-v528-46rv
io.netty:netty-handler@4.1.110.Final [build]: GHSA-3qp7-7mw8-wx86, GHSA-4g8c-wm8x-jfhw, GHSA-c4c3-7fpv-j4q5, GHSA-c653-97m9-rcg9, GHSA-fccg-mwvh-qqg4, GHSA-x4gw-5cx5-pgmh
io.netty:netty-handler-proxy@4.1.110.Final [build]: GHSA-45q3-82m4-75jr
org.apache.commons:commons-compress@1.21 [build]: GHSA-4265-ccf5-phj5, GHSA-4g9r-vxhx-9pgx
org.bitbucket.b_c:jose4j@0.9.5 [build]: GHSA-3677-xxcr-wjqv
org.bouncycastle:bcpkix-jdk18on@1.79 [build]: GHSA-wg6q-6289-32hp
org.bouncycastle:bcprov-jdk18on@1.79 [build]: GHSA-574f-3g2m-x479, GHSA-9pwp-9qqc-pr26, GHSA-c3fc-8qff-9hwx, GHSA-qp49-qgx5-5m26
org.jdom:jdom2@2.0.6 [build]: GHSA-2363-cqg2-863c
org.jetbrains.kotlin:kotlin-gradle-plugin@2.0.21 [build]: GHSA-r937-wjx7-w2jp
org.jetbrains.kotlin:kotlin-gradle-plugin@2.3.20 [build]: GHSA-r937-wjx7-w2jp
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Scopes come from the manifests; a registry crate's own build dependencies cannot be told apart in Cargo.lock, so the runtime set may be larger than reality, never smaller.

**Recommendation.** Update the tooling during routine maintenance; prioritise packages that run in CI with secrets or that produce release artefacts.

**Retest procedure.** Re-run the dependency scan after updating.

### QSI-2026-05181 — No post-quantum capable cryptographic library detected

- Severity: **Info** · Classification: Insufficient data · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `dependencies`
- Data source: dependency manifests
- Detection method: Dependency name matching.
- Analyzer: dependencies 1.2.0 · 2026-10-28 13:02 UTC
- Priority score: 13.4 / 100
- CVSS v3.1: not applicable

Across 4 dependency manifests, QSI found crypto libraries (curve25519-dalek, ecdsa, ed25519-dalek, org.bouncycastle:bcprov-jdk18on, p256, p384, ring, rsa, rustls, secp256k1, x25519-dalek) but none from its PQC-capable list.

**Potential impact.** Readiness indicator only: PQC support may come from the platform (OpenSSL, OS, cloud KMS) rather than application dependencies.

**Reproduction steps.**

```
Review the dependency manifests listed in the evidence.
```

**Evidence.**

_dependency · backend-lib/Cargo.lock, backend-lib/Cargo.toml, build-conventions/buildscript-gradle.lockfile, build-conventions/gradle.lockfile · SHA-256 b16155e20a6433988988e592d8e856f3848ee7d0b22ea93a3da6a11e40efeaed_

```
Crypto libraries: curve25519-dalek, ecdsa, ed25519-dalek, org.bouncycastle:bcprov-jdk18on, p256, p384, ring, rsa, rustls, secp256k1, x25519-dalek. PQC support depends on the version for: org.bouncycastle:bcprov-jdk18on
```

**Limitations of the check.** Absence of evidence is not evidence of absence: system libraries and transitive dependencies may not be listed.

**Recommendation.** Confirm where PQC support will come from (TLS terminator, KMS/HSM, library upgrade).

**Retest procedure.** Re-scan after upgrades.

### QSI-2026-05182 — atomic-polyfill 1.0.3: informational advisory RUSTSEC-2023-0089 (unmaintained)

- Severity: **Info** · Classification: Improvement recommendation · Confidence: Low
- Affected asset: `dependency:crates.io/atomic-polyfill@1.0.3`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 13:02 UTC
- Priority score: 12.3 / 100
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

### QSI-2026-05183 — bincode 2.0.1: informational advisory RUSTSEC-2025-0141 (unmaintained)

- Severity: **Info** · Classification: Improvement recommendation · Confidence: Low
- Affected asset: `dependency:crates.io/bincode@2.0.1`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 13:02 UTC
- Priority score: 12.3 / 100
- CVSS v3.1: not applicable

OSV.dev lists RUSTSEC-2025-0141 for crates.io package bincode at version 2.0.1 as informational (unmaintained): Bincode is unmaintained. It reports no vulnerability; an unmaintained package will not receive fixes for future ones.

**Potential impact.** No known vulnerability. Future security fixes may not be released.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2025-0141
```

**Evidence.**

_tool_output · [OSV.dev RUSTSEC-2025-0141](https://osv.dev/vulnerability/RUSTSEC-2025-0141) · manifest · SHA-256 532525d6fd3f2cb4701cae8133e80ff6557554f82b919c38fb8a089b03cf57f5_

```
{"id": "RUSTSEC-2025-0141", "aliases": [], "modified": "2026-01-16T11:07:28.867553Z", "summary": "Bincode is unmaintained", "severity": null, "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time.

**Recommendation.** Plan a move to a maintained alternative, or record the decision to keep it.

**Retest procedure.** Re-run the dependency scan after the change.

### QSI-2026-05188 — paste 1.0.15: informational advisory RUSTSEC-2024-0436 (unmaintained)

- Severity: **Info** · Classification: Improvement recommendation · Confidence: Low
- Affected asset: `dependency:crates.io/paste@1.0.15`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 13:02 UTC
- Priority score: 12.3 / 100
- CVSS v3.1: not applicable

OSV.dev lists RUSTSEC-2024-0436 for crates.io package paste at version 1.0.15 as informational (unmaintained): paste - no longer maintained. It reports no vulnerability; an unmaintained package will not receive fixes for future ones.

**Potential impact.** No known vulnerability. Future security fixes may not be released.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2024-0436
```

**Evidence.**

_tool_output · [OSV.dev RUSTSEC-2024-0436](https://osv.dev/vulnerability/RUSTSEC-2024-0436) · manifest · SHA-256 ea867adb8ba26c96c3779becf55b3de25d46f37f23ab55131e09c98a8b0b9975_

```
{"id": "RUSTSEC-2024-0436", "aliases": [], "modified": "2026-01-27T22:03:15.694766Z", "summary": "paste - no longer maintained", "severity": null, "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time.

**Recommendation.** Plan a move to a maintained alternative, or record the decision to keep it.

**Retest procedure.** Re-run the dependency scan after the change.


## 8. Post-quantum assessment

| | Key establishment (x = how long data must stay confidential; harvest now, decrypt later) | Signatures (x = how long signatures/keys must stay trusted) |
|---|---|---|
| Data/key lifetime x | 5 | 5 |
| Migration time y | 3 | 3 |
| Assumed years to CRQC z | 12 (central) | 12 |
| x + y − z | -4 → time available under this scenario | -4 → time available under this scenario |
_No signature lifetime is set for the project; the data lifetime is used as an assumption._
#### Where z comes from

Averaged expert likelihood that a CRQC exists within each horizon, from the annual survey published by the author of this inequality. Likelihood estimates, not predictions of a date.

| Within | Likelihood | The report's wording |
|---|---|---|
| 5 years | ~15% | averaged estimate |
| 10 years | 28-49% | quite possible |
| 15 years | 51-70% | likely |

**Why this scenario (central, z = 12):** Between the 10-year band (28-49%) and the 15-year band (51-70%): roughly where the experts' averaged likelihood crosses one half. More than half of the respondents (13 of 26) already put the likelihood at 50% or more for some horizon.
_Planning assumptions: x for key establishment, x for signatures, y are the defaults of the risk profile “Small technology company”, not the client's figures; with the client's actual lifetimes the verdict can change._

### Post-quantum maturity: Level 0 of 4 — no post-quantum cryptography


**Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

_Levels: 0 none; 1 present, not wired; 2 in use outside the critical paths; 3 hybrid in a critical path; 4 post-quantum by default in the critical paths (root of trust, key wrapping, channel key exchange). Judged from code and manifests._
No readiness questionnaire was completed for this project.

### Quantum algorithms relevant to this inventory

| Quantum algorithm | Effect | Attack model | Inventoried algorithms (rows) | What it means for this audit |
|---|---|---|---|---|
| Shor's algorithm — factoring | breaks | Q1 | RSA (2) | Breaks RSA at every key length: a longer modulus only raises the cost polynomially. Plan migration to ML-KEM (or a hybrid) for key establishment and ML-DSA / SLH-DSA for signatures; start with keys protecting data that must stay confidential for years (harvest now, decrypt later) and with long-lived signatures. |
| Grover's algorithm — key search and preimages | weakens (larger keys restore the margin) | Q1 | SHA-1 (1) | Not a break. 256-bit keys (AES-256, ChaCha20) keep a comfortable margin; AES-128 meets NIST category 1, while some authorities ask for 256-bit keys in quantum-resistant contexts (see the AES-128 entry). Prefer 256-bit keys for long-lived data; 256-bit hashes need no change for preimage resistance. |
| Brassard–Høyer–Tapp — collision search | weakens (larger keys restore the margin) | Q1 | SHA-1 (1) | 256-bit hashes (SHA-256, SHA3-256) remain adequate for collision resistance; 160-bit hashes are already weak classically (SHA-1 collisions are practical). Use 384/512-bit hashes where NIST categories 4–5 are required. |

_Effects: breaks — replace the algorithm; weakens — larger keys or outputs restore the margin; included in standard parameters — no action at standard parameter sets; only with superposition queries — not applicable to ordinary deployments._


## 9. Limitations and assumptions

- This report presents automated and documented analysis results for the stated scope. It is not a legal opinion, a certification or an attestation of compliance with any standard.
- z is a planning assumption chosen per risk profile, not a prediction. A cryptographically relevant quantum computer is not publicly known to exist today.

## 10. Remediation plan / Priorities for 30, 60 and 90 days

### 30 days

| Priority | ID | Action | Type | Closure criteria |
|---|---|---|---|---|
| P2 | QSI-2026-05184 | Upgrade block-buffer to a fixed version (none published yet; see the advisory for mitigations). | root-cause fix | Dependency scan no longer reports GHSA-qwgh-2vcv-g2f7. |
| P2 | QSI-2026-05185 | Upgrade block-buffer to a fixed version (none published yet; see the advisory for mitigations). | root-cause fix | Dependency scan no longer reports GHSA-qwgh-2vcv-g2f7. |
| P2 | QSI-2026-05189 | Upgrade rsa to a fixed version (none published yet; see the advisory for mitigations). | root-cause fix | Dependency scan no longer reports RUSTSEC-2023-0071 (CVE-2023-49092). |
| P2 | QSI-2026-05190 | Upgrade rustls to a fixed version (0.23.45). | root-cause fix | Dependency scan no longer reports GHSA-2mjx-qc3c-rqvc (RUSTSEC-2026-0285). |
| P2 | QSI-2026-05191 | Upgrade rustls to a fixed version (0.23.46, 0.24.0-dev.2). | root-cause fix | Dependency scan no longer reports GHSA-c8m5-c952-6cm4 (RUSTSEC-2026-0346). |
| P2 | QSI-2026-05193 | Upgrade rustls to a fixed version (0.23.46, 0.24.0-dev.2). | root-cause fix | Dependency scan no longer reports GHSA-w44r-93j7-qv28 (RUSTSEC-2026-0349). |
| P2 | QSI-2026-05192 | Upgrade rustls to a fixed version (0.23.46, 0.24.0-dev.2). | root-cause fix | Dependency scan no longer reports GHSA-h2v8-394m-p7vv (RUSTSEC-2026-0348). |
### 60 days

| Priority | ID | Action | Type | Closure criteria |
|---|---|---|---|---|
| P3 | QSI-2026-05179 | Review each SHA-1 call site in backend-lib/src/main/java/cash/z/ecc/android/sdk/internal/ext/FileExt.kt; replace security-relevant ones with SHA-256 or a password hash. | root-cause fix | No security-relevant SHA-1 usage remains. |
| P3 | QSI-2026-05186 | Triage RUSTSEC-2026-0387; upgrade crypto-bigint to a fixed version (0.7.6) if it applies. | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0387, or the triage is recorded. |
| P3 | QSI-2026-05187 | Triage RUSTSEC-2026-0258; upgrade h2 to a fixed version (0.4.16) if it applies. | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0258, or the triage is recorded. |
| P3 | QSI-2026-05194 | Triage RUSTSEC-2026-0382 (CVE-2026-111943); upgrade rustls-webpki to a fixed version (0.103.16, 0.104.0-alpha.8) if it applies. | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0382 (CVE-2026-111943), or the triage is recorded. |
| P3 | QSI-2026-05195 | Triage RUSTSEC-2026-0386; upgrade tokio to a fixed version (1.51.6, 1.53.3) if it applies. | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0386, or the triage is recorded. |
| P3 | QSI-2026-05196 | Triage RUSTSEC-2026-0381 (CVE-2026-111943); upgrade webpki-roots to a fixed version (0.26.11, 1.0.10) if it applies. | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0381 (CVE-2026-111943), or the triage is recorded. |
| P3 | QSI-2026-05197 | Triage RUSTSEC-2026-0391; upgrade zstd to a fixed version (0.14.3) if it applies. | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0391, or the triage is recorded. |
| P3 | QSI-2026-05198 | Triage RUSTSEC-2026-0395; upgrade zstd-safe to a fixed version (8.2.0) if it applies. | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0395, or the triage is recorded. |
| P3 | QSI-2026-05199 | Triage RUSTSEC-2026-0396; upgrade zstd-safe to a fixed version (8.2.0) if it applies. | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0396, or the triage is recorded. |
| P3 | QSI-2026-05200 | Triage RUSTSEC-2026-0397; upgrade zstd-safe to a fixed version (8.2.0) if it applies. | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0397, or the triage is recorded. |
| P3 | QSI-2026-05201 | Triage RUSTSEC-2026-0398; upgrade zstd-safe to a fixed version (8.2.0) if it applies. | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0398, or the triage is recorded. |
| P3 | QSI-2026-05202 | Triage RUSTSEC-2026-0399; upgrade zstd-safe to a fixed version (8.2.0) if it applies. | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0399, or the triage is recorded. |
| P3 | QSI-2026-05203 | Triage RUSTSEC-2026-0400; upgrade zstd-safe to a fixed version (8.2.0) if it applies. | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0400, or the triage is recorded. |
| P3 | QSI-2026-05204 | Triage RUSTSEC-2026-0401; upgrade zstd-safe to a fixed version (8.2.0) if it applies. | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0401, or the triage is recorded. |
| P3 | QSI-2026-05205 | Triage RUSTSEC-2026-0402; upgrade zstd-safe to a fixed version (8.2.0) if it applies. | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0402, or the triage is recorded. |
| P3 | QSI-2026-05206 | Triage RUSTSEC-2026-0403; upgrade zstd-safe to a fixed version (8.2.0) if it applies. | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0403, or the triage is recorded. |
| P3 | QSI-2026-05207 | Triage RUSTSEC-2026-0404; upgrade zstd-safe to a fixed version (8.2.0) if it applies. | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0404, or the triage is recorded. |
| P3 | QSI-2026-05208 | Triage RUSTSEC-2026-0405; upgrade zstd-safe to a fixed version (8.2.0) if it applies. | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0405, or the triage is recorded. |
| P3 | QSI-2026-05209 | Triage RUSTSEC-2026-0406; upgrade zstd-safe to a fixed version (8.2.0) if it applies. | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0406, or the triage is recorded. |
| P3 | QSI-2026-05210 | Triage RUSTSEC-2026-0410; upgrade zstd-sys to a fixed version (2.1.2) if it applies. | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0410, or the triage is recorded. |
### 90 days

| Priority | ID | Action | Type | Closure criteria |
|---|---|---|---|---|
| P3 | QSI-2026-05180 | Add RSA usages at file:responsible_disclosure.md to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P4 | QSI-2026-05180 | Plan migration of RSA to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. or a hybrid scheme in use. |
| P4 | QSI-2026-05211 | Update the development and build dependencies listed in the evidence. | root-cause fix | The dependency scan reports no advisories for tooling packages, or the remaining ones are recorded. |
| P4 | QSI-2026-05182 | Replace atomic-polyfill with a maintained alternative or record why it stays. | root-cause fix | atomic-polyfill replaced, or the decision recorded. |
| P4 | QSI-2026-05183 | Replace bincode with a maintained alternative or record why it stays. | root-cause fix | bincode replaced, or the decision recorded. |
| P4 | QSI-2026-05188 | Replace paste with a maintained alternative or record why it stays. | root-cause fix | paste replaced, or the decision recorded. |

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
2. C. Gidney — How to factor 2048 bit RSA integers with less than a million noisy qubits (arXiv:2505.15917) — arXiv. <https://arxiv.org/abs/2505.15917> (preprint (2025-05-21): < 1 million noisy qubits, < 1 week, 0.1% gate error, 1 µs surface-code cycle)
3. C. Gidney, M. Ekerå — How to factor 2048 bit RSA integers in 8 hours using 20 million noisy qubits (Quantum 5, 433) — Quantum. <https://doi.org/10.22331/q-2021-04-15-433> (peer-reviewed article (2021): 10^-3 gate error, 1 µs cycle, 10 µs reaction time)
4. C. Zalka — Grover's quantum searching algorithm is optimal (Phys. Rev. A 60, 2746, 1999; arXiv:quant-ph/9711070) — APS. <https://doi.org/10.1103/PhysRevA.60.2746> (peer-reviewed article: optimal for any success probability; parallel search gains no more than splitting the space)
5. Common Vulnerability Scoring System v3.1: Specification Document — FIRST. <https://www.first.org/cvss/v3.1/specification-document> (final)
6. D. J. Bernstein — Cost analysis of hash collisions: Will quantum computers make SHARCS obsolete? (2009) — cr.yp.to. <https://cr.yp.to/hash/collisioncost-20090823.pdf> (paper dated 2009-08-23)
7. FIPS 203 — Module-Lattice-Based Key-Encapsulation Mechanism Standard (ML-KEM) — NIST. <https://csrc.nist.gov/pubs/fips/203/final> (final (August 2024))
8. FIPS 204 — Module-Lattice-Based Digital Signature Standard (ML-DSA) — NIST. <https://csrc.nist.gov/pubs/fips/204/final> (final (August 2024))
9. FIPS 205 — Stateless Hash-Based Digital Signature Standard (SLH-DSA) — NIST. <https://csrc.nist.gov/pubs/fips/205/final> (final (August 2024))
10. G. Brassard, P. Høyer, A. Tapp — Quantum Algorithm for the Collision Problem (LATIN '98; arXiv:quant-ph/9705002) — Springer / arXiv. <https://arxiv.org/abs/quant-ph/9705002> (peer-reviewed article: collisions of r-to-one functions in O((N/r)^{1/3}) expected evaluations)
11. L. K. Grover — A fast quantum mechanical algorithm for database search (STOC 1996) — ACM. <https://doi.org/10.1145/237814.237866> (peer-reviewed article)
12. M. Amy et al. — Estimating the cost of generic quantum pre-image attacks on SHA-2 and SHA-3 (SAC 2016; arXiv:1603.09383) — Springer / arXiv. <https://arxiv.org/abs/1603.09383> (peer-reviewed article: SHA-256 about 2^153.8 surface-code cycles on 2^12.6 logical qubits; SHA3-256 about 2^146.5 cycles on 2^20)
13. M. Cain et al. — Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits (arXiv:2603.28627) — arXiv. <https://arxiv.org/abs/2603.28627> (preprint (2026-03-30): P-256 in a few days with 26,000 physical neutral-atom qubits; RSA-2048 one to two orders of magnitude longer)
14. M. Mosca — Cybersecurity in an Era with Quantum Computers: Will We Be Ready? (IEEE Security & Privacy, 2018) — IEEE. <https://doi.org/10.1109/MSP.2018.3761723> (peer-reviewed article; source of the x + y > z migration inequality)
15. NIST IR 8547 — Transition to Post-Quantum Cryptography Standards — NIST. <https://csrc.nist.gov/pubs/ir/8547/ipd> (initial public draft (November 2024); proposes deprecating quantum-vulnerable public-key algorithms after 2030 and disallowing them after 2035 — dates may change in the final version)
16. NIST SP 800-131A Rev. 2 — Transitioning the Use of Cryptographic Algorithms and Key Lengths — NIST. <https://csrc.nist.gov/pubs/sp/800/131/a/r2/final> (final (2019))
17. NIST — Post-Quantum Cryptography Standardization: Evaluation Criteria, Security (Call for Proposals, Section 4.A.5) — NIST. <https://csrc.nist.gov/Projects/Post-Quantum-Cryptography/Post-Quantum-Cryptography-Standardization/Evaluation-Criteria/Security-(Evaluation-Criteria)> (security categories: AES-128 key search 2^170/MAXDEPTH quantum gates, AES-192 2^233/MAXDEPTH, AES-256 2^298/MAXDEPTH; MAXDEPTH 2^40–2^96)
18. OSV advisory GHSA-2mjx-qc3c-rqvc — OSV.dev. <https://osv.dev/vulnerability/GHSA-2mjx-qc3c-rqvc> (modified 2026-10-27T15:30:05.509305490Z)
19. OSV advisory GHSA-c8m5-c952-6cm4 — OSV.dev. <https://osv.dev/vulnerability/GHSA-c8m5-c952-6cm4> (modified 2026-10-27T16:15:05.354395696Z)
20. OSV advisory GHSA-h2v8-394m-p7vv — OSV.dev. <https://osv.dev/vulnerability/GHSA-h2v8-394m-p7vv> (modified 2026-10-27T16:15:05.337819489Z)
21. OSV advisory GHSA-qwgh-2vcv-g2f7 — OSV.dev. <https://osv.dev/vulnerability/GHSA-qwgh-2vcv-g2f7> (modified 2026-08-19T19:30:06.686866977Z)
22. OSV advisory GHSA-w44r-93j7-qv28 — OSV.dev. <https://osv.dev/vulnerability/GHSA-w44r-93j7-qv28> (modified 2026-10-27T16:15:05.340347056Z)
23. OSV advisory RUSTSEC-2023-0071 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2023-0071> (modified 2026-09-14T09:45:02.996132556Z)
24. OSV advisory RUSTSEC-2023-0089 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2023-0089> (modified 2025-04-29T08:31:10Z)
25. OSV advisory RUSTSEC-2024-0436 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2024-0436> (modified 2026-01-27T22:03:15.694766Z)
26. OSV advisory RUSTSEC-2025-0141 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2025-0141> (modified 2026-01-16T11:07:28.867553Z)
27. OSV advisory RUSTSEC-2026-0258 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0258> (modified 2026-10-12T18:00:10.934581734Z)
28. OSV advisory RUSTSEC-2026-0381 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0381> (modified 2026-10-21T06:30:02.818201920Z)
29. OSV advisory RUSTSEC-2026-0382 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0382> (modified 2026-10-21T00:55:56.763143468Z)
30. OSV advisory RUSTSEC-2026-0386 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0386> (modified 2026-10-23T14:45:03.847864944Z)
31. OSV advisory RUSTSEC-2026-0387 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0387> (modified 2026-10-24T03:45:02.365137418Z)
32. OSV advisory RUSTSEC-2026-0391 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0391> (modified 2026-10-26T14:00:04.269245609Z)
33. OSV advisory RUSTSEC-2026-0395 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0395> (modified 2026-10-26T14:00:06.388344282Z)
34. OSV advisory RUSTSEC-2026-0396 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0396> (modified 2026-10-26T14:00:05.789682118Z)
35. OSV advisory RUSTSEC-2026-0397 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0397> (modified 2026-10-26T14:00:05.089587004Z)
36. OSV advisory RUSTSEC-2026-0398 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0398> (modified 2026-10-26T14:00:05.092082939Z)
37. OSV advisory RUSTSEC-2026-0399 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0399> (modified 2026-10-26T14:00:05.792431051Z)
38. OSV advisory RUSTSEC-2026-0400 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0400> (modified 2026-10-26T14:00:05.692077560Z)
39. OSV advisory RUSTSEC-2026-0401 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0401> (modified 2026-10-26T14:00:04.231502512Z)
40. OSV advisory RUSTSEC-2026-0402 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0402> (modified 2026-10-26T14:00:05.685817733Z)
41. OSV advisory RUSTSEC-2026-0403 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0403> (modified 2026-10-26T14:00:05.787441176Z)
42. OSV advisory RUSTSEC-2026-0404 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0404> (modified 2026-10-26T14:00:05.092817237Z)
43. OSV advisory RUSTSEC-2026-0405 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0405> (modified 2026-10-26T14:00:05.680942523Z)
44. OSV advisory RUSTSEC-2026-0406 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0406> (modified 2026-10-26T14:00:05.095427051Z)
45. OSV advisory RUSTSEC-2026-0410 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0410> (modified 2026-10-26T14:00:05.788985783Z)
46. OSV.dev — open-source vulnerability database and API — Open Source Security Foundation. <https://osv.dev/> (the database QSI queries for each exactly pinned version; every advisory id in a finding resolves at https://osv.dev/vulnerability/<id>)
47. P. W. Shor — Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms on a Quantum Computer (SIAM J. Comput., 1997) — SIAM. <https://doi.org/10.1137/S0097539795293172> (peer-reviewed article)
48. S. Jaques, M. Naehrig, M. Roetteler, F. Virdia — Implementing Grover oracles for quantum key search on AES and LowMC (EUROCRYPT 2020; arXiv:1910.01700) — Springer / arXiv. <https://arxiv.org/abs/1910.01700> (peer-reviewed article: lower cost estimates for the AES key searches that define the NIST categories)

## Appendices: Cryptographic inventory

| Algorithm | Parameter | Library | Location | Quantum status | Classical status |
|---|---|---|---|---|---|
| SHA-1 | SHA-1 |  | backend-lib/src/main/java/cash/z/ecc/android/sdk/internal/ext/FileExt.kt:50 | weak classically | deprecated |
| Crypto library | 0.13.1 | p384 (RustCrypto elliptic curves) | backend-lib/Cargo.lock | n/a | acceptable |
| Crypto library | 0.13.2 | p256 (RustCrypto elliptic curves) | backend-lib/Cargo.lock | n/a | acceptable |
| Crypto library | 0.16.9 | ecdsa (python-ecdsa) | backend-lib/Cargo.lock | n/a | acceptable |
| Crypto library | 0.17.14 | ring (ring (Rust)) | backend-lib/Cargo.lock | n/a | acceptable |
| Crypto library | 0.23.43 | rustls (rustls) | backend-lib/Cargo.lock | n/a | acceptable |
| Crypto library | 0.29.1 | secp256k1 (secp256k1 bindings) | backend-lib/Cargo.lock | n/a | acceptable |
| Crypto library | 0.9.10 | rsa (RustCrypto rsa) | backend-lib/Cargo.lock | n/a | acceptable |
| Crypto library | 2.0.1 | x25519-dalek (ed25519-dalek) | backend-lib/Cargo.lock | n/a | acceptable |
| Crypto library | 2.2.0 | ed25519-dalek (ed25519-dalek) | backend-lib/Cargo.lock | n/a | acceptable |
| Crypto library | 4.1.3 | curve25519-dalek (ed25519-dalek) | backend-lib/Cargo.lock | n/a | acceptable |
| Crypto library | 1.79 | org.bouncycastle:bcprov-jdk18on (Bouncy Castle) | build-conventions/gradle.lockfile:122 | n/a | acceptable |
| RSA | 2048-bit |  | responsible_disclosure.md (line 11) | vulnerable (Shor) | acceptable |
| RSA | 2048-bit |  | responsible_disclosure.md (line 11) | vulnerable (Shor) | acceptable |

## Appendices: Input files

| File | Size | SHA-256 | Redactions |
|---|---|---|---|
| backend-lib/Cargo.lock | 191175 | `324795f089d68678845da85bb94f9ef2a1b25e15241514c945f7e75cdfee9211` | 0 |
| backend-lib/Cargo.toml | 10336 | `623c2c278bc8f09f654f6691ba4013f1b0bd744a1aca71b9c06f19f6031bda3a` | 0 |
| backend-lib/build.gradle.kts | 9491 | `d9bf273ace25507c9373292d63ead4e2a861f4606f32b0c1d71c32aaac16210d` | 0 |
| backend-lib/build.rs | 4343 | `698d6538c4b7c8007f028a7c214b31e17b01f7287075b594e64d8d7aa147c3be` | 0 |
| backend-lib/src/main/java/cash/z/ecc/android/sdk/internal/Backend.kt | 13853 | `f377eff292b0ada797b2f5f093ac712a006fb081e946d63952184ae2fdaba436` | 0 |
| backend-lib/src/main/java/cash/z/ecc/android/sdk/internal/Derivation.kt | 3932 | `544fbd8fb0d5979d067366c5dc3bfd193c809f647697aac8a955793847a11144` | 0 |
| backend-lib/src/main/java/cash/z/ecc/android/sdk/internal/Eip681.kt | 1091 | `d8952dada0779117452e04a04fc2bc875cc0dd3df12a6de6d98f7b4aeffadbe4` | 0 |
| backend-lib/src/main/java/cash/z/ecc/android/sdk/internal/SdkDispatchers.kt | 1852 | `9c9994e6ff6fe71fa8a90c46e9e99ecd8cb03b0f8873677072ac27551482f798` | 0 |
| backend-lib/src/main/java/cash/z/ecc/android/sdk/internal/ext/FileExt.kt | 2420 | `f6d81a7cb9cd4f097025cb53b0dc3de8f21fefaedc82e0ec2f763998e3e9fee3` | 0 |
| backend-lib/src/main/java/cash/z/ecc/android/sdk/internal/ext/NumberExt.kt | 171 | `52d76c25bcc5ba21fb3cb2c4ae7c44153584fc3c4101a61330950c5c8139110c` | 0 |
| backend-lib/src/main/java/cash/z/ecc/android/sdk/internal/jni/FakeRustBackend.kt | 8928 | `a2179352e6be5d1073fdcf9c1467b8abc585b4803ae62063510e639a07616a5f` | 0 |
| backend-lib/src/main/java/cash/z/ecc/android/sdk/internal/jni/JniConstants.kt | 2748 | `2809c14841ac3504cc39f336d77d8b4c2165cb9169261a74b3cd7cfcc54473ed` | 0 |
| backend-lib/src/main/java/cash/z/ecc/android/sdk/internal/jni/MigrationRustBackend.kt | 38522 | `fb4ceefc077a428d1994a06d3c18a47e61f30742563a70e7406c84d34607a483` | 0 |
| backend-lib/src/main/java/cash/z/ecc/android/sdk/internal/jni/NativeLibraryLoader.kt | 1782 | `858888f649b87520fc5b9ef3c1153a2bbf40d9b2399a003a45f9b4391265604f` | 0 |
| backend-lib/src/main/java/cash/z/ecc/android/sdk/internal/jni/RustBackend.kt | 30085 | `e29835f691c61f536c870cca39ff8136e80b861e0a30c1e7dda6fc5bddb98b5b` | 0 |
| backend-lib/src/main/java/cash/z/ecc/android/sdk/internal/jni/RustDerivationTool.kt | 4803 | `f10010c92548a4c539d3e24197f3e35e50a984fbad012d5871b2535cd9110d11` | 0 |
| backend-lib/src/main/java/cash/z/ecc/android/sdk/internal/jni/RustEip681Tool.kt | 981 | `b893b44e155ab97404bb8aaa35eb516d9b199a279b4cda12c036f884f5f1e4c1` | 0 |
| backend-lib/src/main/java/cash/z/ecc/android/sdk/internal/jni/VotingRustBackend.kt | 53538 | `8e39d67fd026e6adb52bd72a1c132c91686ccfda6fedad5f83c030a102bae9f4` | 0 |
| backend-lib/src/main/java/cash/z/ecc/android/sdk/internal/model/CombinedWalletClientImpl.kt | 8739 | `c1388b3ce88f40f710c283ebe829054d1915fb04f334bfe3d4d7e7ed78027bdd` | 0 |
| backend-lib/src/main/java/cash/z/ecc/android/sdk/internal/model/IsolatedTorWalletClient.kt | 2286 | `6c867eca268644a6b3779a75c403659c15a64b7d4c37b3c0d077120bae345d68` | 0 |
| backend-lib/src/main/java/cash/z/ecc/android/sdk/internal/model/JniAccount.kt | 1449 | `3926e1be2c9d50c30cd071d48b8ffb9ca35c3a5f08ed6641f325abefa8746b6e` | 0 |
| backend-lib/src/main/java/cash/z/ecc/android/sdk/internal/model/JniAccountBalance.kt | 5384 | `2c837474065ffc275b191acb0ce5312406db3ab3b41163ca4d4582e50839ce14` | 0 |
| backend-lib/src/main/java/cash/z/ecc/android/sdk/internal/model/JniAccountUsk.kt | 1525 | `da76d5c1b7beaf19a89a307f888cb4c18ed569c42305ff81e2f37ff5f01a317f` | 0 |
| backend-lib/src/main/java/cash/z/ecc/android/sdk/internal/model/JniAddressCheckResult.kt | 343 | `d8cc5e241c1ef8b60b899ab911fcf5188202202ff8b548ac118378734b4328dc` | 0 |
| backend-lib/src/main/java/cash/z/ecc/android/sdk/internal/model/JniBlockMeta.kt | 1864 | `80327f75d6c1faa122ba59091872522afd2fb76324311f66cdddc7340df78415` | 0 |
| backend-lib/src/main/java/cash/z/ecc/android/sdk/internal/model/JniEip681TransactionRequest.kt | 2675 | `bf8fa27496e10af1bcb54c902acde43b846a0ecd9df00d71f11829aaca1aceea` | 0 |
| backend-lib/src/main/java/cash/z/ecc/android/sdk/internal/model/JniHttpHeader.kt | 183 | `9ee890d1ff68ac20f41021ab633bd8c029e4456a42e27755557f355b458288dd` | 0 |
| backend-lib/src/main/java/cash/z/ecc/android/sdk/internal/model/JniHttpResponseBytes.kt | 451 | `3a9fe347545f4938d962a7a2569eda248511df707d17259941fe7967d8e5ea8c` | 0 |
| backend-lib/src/main/java/cash/z/ecc/android/sdk/internal/model/JniMetadataKey.kt | 841 | `e83773adfe0f94df5464564f606b49d25f75b46dd07a5b4f3462163d54f143e7` | 0 |
| backend-lib/src/main/java/cash/z/ecc/android/sdk/internal/model/JniRewindResult.kt | 1338 | `2a162bb7fd7269840f5c480cc274feb8d155277e425fb836db5f81d30ae1cddd` | 0 |
| backend-lib/src/main/java/cash/z/ecc/android/sdk/internal/model/JniScanRange.kt | 1344 | `2d3918e3a16d3d49773a4439fd506f425ad926be0b93892dc1882a31dac241e2` | 0 |
| backend-lib/src/main/java/cash/z/ecc/android/sdk/internal/model/JniScanSummary.kt | 1531 | `7091d6f437258a207138059c85ba6001d69d40398921b5ca75110671a558457e` | 0 |
| backend-lib/src/main/java/cash/z/ecc/android/sdk/internal/model/JniSingleUseTransparentAddress.kt | 914 | `8bad606ba577fdfca88ea1289118f7cf4652bb1755bcbbf761cebacef14f8d0b` | 0 |
| backend-lib/src/main/java/cash/z/ecc/android/sdk/internal/model/JniSubtreeRoot.kt | 1088 | `a11404298b79bc691dc5f5a74c874b4a21b505031b94162e5764101204174d11` | 0 |
| backend-lib/src/main/java/cash/z/ecc/android/sdk/internal/model/JniTransaction.kt | 349 | `f581c7b599fab7664a3902eca9e3458cea21b9af1e004cd7c704c0e834fd007e` | 0 |
| backend-lib/src/main/java/cash/z/ecc/android/sdk/internal/model/JniTransactionDataRequest.kt | 2292 | `9beb38a08eb2613ff2448c2d6e627b6f41e12e94c9fb6d37b06d5b551fc1915e` | 0 |
| backend-lib/src/main/java/cash/z/ecc/android/sdk/internal/model/JniUnifiedSpendingKey.kt | 1161 | `faf40d78d53dfb495a5a511a52ba7c5473f1edb363d3125ba877616304af1076` | 0 |
| backend-lib/src/main/java/cash/z/ecc/android/sdk/internal/model/JniWalletSummary.kt | 5027 | `36c646ef59390e9bbc23d60f3d9091a6c2f5548c8ae0c17b5a963643fe8a79ad` | 0 |
| backend-lib/src/main/java/cash/z/ecc/android/sdk/internal/model/LazyTorClient.kt | 2168 | `8a4e8efe4e94f05e55d5208bf00518939388dcfb430ad6b81bf38eba2bc16b1e` | 0 |
| backend-lib/src/main/java/cash/z/ecc/android/sdk/internal/model/ProposalUnsafe.kt | 2751 | `dad1059735d866c5e9b453ba5aa6841162af5b92c0a388864c3ccde3dce941f2` | 0 |
| backend-lib/src/main/java/cash/z/ecc/android/sdk/internal/model/RustLogging.kt | 1075 | `a103fa1cc51d753e0ff392dd0676d4eecca771b77dacc57d811bf84d491d5af8` | 0 |
| backend-lib/src/main/java/cash/z/ecc/android/sdk/internal/model/TorClient.kt | 8550 | `20cea253ac84b90d59d8d753af07d5ec184a3b2b27418123cba12bc79d8b48a6` | 0 |
| backend-lib/src/main/java/cash/z/ecc/android/sdk/internal/model/TorHttp.kt | 663 | `387678a8a09314ecfb750abfb385cda42c41f26e4d3b1b9a98fd6d70cfcc1283` | 0 |
| backend-lib/src/main/java/cash/z/ecc/android/sdk/internal/model/TorHttpConfig.kt | 471 | `9d1223c6d77a59dfb8cbba6dceed694126bbe5b18b8229a7393caf25c99075f8` | 0 |
| backend-lib/src/main/java/cash/z/ecc/android/sdk/internal/model/TorHttpEngine.kt | 3966 | `c635491810b3f0472be23f89bed0e2c143c7c77297b22ed6edee81badd4dd0b5` | 0 |
| backend-lib/src/main/java/cash/z/ecc/android/sdk/internal/model/TorWalletClient.kt | 7914 | `21db8f7a869a8d33505b1dcc6af6b2875313e188712a2d043309ec23dd91ad11` | 0 |
| backend-lib/src/main/java/cash/z/ecc/android/sdk/internal/model/ZcashProtocol.kt | 1410 | `40839e81077a4773f6c93c0603a5ba839609fc0cf05bc0f5a220b3f9e60e0470` | 0 |
| backend-lib/src/main/java/cash/z/ecc/android/sdk/internal/model/migration/JniMigrationModels.kt | 10525 | `08ffc3c5381ccd021395b779781cdbc2fab01468f939a9fb80f7202bc00412bd` | 0 |
| backend-lib/src/main/java/cash/z/ecc/android/sdk/internal/model/voting/JniVotingModels.kt | 25751 | `c825df4bf9368354d04aed2876089c04205ac971025504345b23532787ac2913` | 0 |
| backend-lib/src/main/proto/proposal.proto | 7648 | `7bbc79e731eb5345124351794ca8ce7b01fdff570646af889076be1a46d46cf9` | 0 |
| backend-lib/src/main/rust/eip681.rs | 10750 | `cba69bba70c2f0cff4acd4a2019763a7dc86b7adfaa7a2b49d141190b962ae7d` | 0 |
| backend-lib/src/main/rust/lib.rs | 153798 | `ee51888c9bd93c8e645b608f4d4dbd109dba246d64fea1b1d5ad0d07204a6936` | 0 |
| backend-lib/src/main/rust/migration.rs | 369853 | `21c573ddfe9fd73af8350aabf5cf296746bdf82aa3f5e49d505e840bd84b3af3` | 0 |
| backend-lib/src/main/rust/migration_engine.rs | 19232 | `6653594423c7d3c424b0bda96d6bbdf31bc5389f42b7dd34647177605d7a78ae` | 0 |
| backend-lib/src/main/rust/migration_keystone.rs | 27694 | `689c3586f23e752474e9025bfb9e1eb199bcbe16ce985bb91d44034f12771575` | 0 |
| backend-lib/src/main/rust/migration_plan_cache.rs | 5152 | `a497abf84062def1a0955433450e963e52a1e349df2484403d13242258e3b676` | 0 |
| backend-lib/src/main/rust/migration_send_max.rs | 6898 | `47976e4ce8d4d17476d9bd8267cdac51939d4042b851b27223ca4fc4503e55d4` | 0 |
| backend-lib/src/main/rust/tor.rs | 9844 | `48b77fae67e39a0ca2f409da8bfffc148d8cae08075ba1a4682d7b64db28c9fd` | 0 |
| backend-lib/src/main/rust/utils/exception.rs | 4607 | `73307da924d7154f72fc2aec7138c53eee1041e315eb72e2cef4ae56e4b65fea` | 0 |
| backend-lib/src/main/rust/utils/target_ndk.rs | 1767 | `c0f9ace4fb5a2db9c56be76b1bfe78895dde27b87ca57bdb5cb26a18390e12fd` | 0 |
| backend-lib/src/main/rust/utils/trace.rs | 2460 | `6aea8946ba52f7cd8124ae37627a4cf2b52be4189870ba1cac660acf01000b55` | 0 |
| backend-lib/src/main/rust/utils.rs | 4501 | `69c5f7cc4466f392752950d1cd007988ee18eca6f25f176daa6aea6ae0f8fc80` | 0 |
| backend-lib/src/main/rust/voting/db.rs | 6276 | `ba134fa18dd4527bad29747d10cf8cf5477830279619cdb6a24fb2a838e83841` | 0 |
| backend-lib/src/main/rust/voting/delegation.rs | 44417 | `778c92134dafd2bec7f5ecdc9641eb235081e09f348885bbc4c03ae1f2027c88` | 0 |
| backend-lib/src/main/rust/voting/helpers.rs | 67845 | `74a03dff530384ac024266b31c66620115a2f0496e15a113e295c1a290150cef` | 0 |
| backend-lib/src/main/rust/voting/notes.rs | 13979 | `6f5c3470bb15b364f93080ca784ad68f650d024c769553b885f43ff8cafbe5d7` | 0 |
| backend-lib/src/main/rust/voting/progress.rs | 1618 | `cf170ec349ad1db650d512a879b306d3d1410fc5fd49dfccd28151d408146ee8` | 0 |
| backend-lib/src/main/rust/voting/recovery.rs | 23825 | `7b483f68c26e11e1373aaf4bdf893a6b870636fc53690661a39518515886ea2c` | 0 |
| backend-lib/src/main/rust/voting/rounds.rs | 8276 | `59744670390906f947b1a87172a3417c25ef89f084a8983596a54aa09e15b466` | 0 |
| backend-lib/src/main/rust/voting/share_tracking.rs | 2723 | `ff435e306a99bf83e65bfee977af3887ea25bd2b6e0aabce7aff2d5715cbba00` | 0 |
| backend-lib/src/main/rust/voting/tree.rs | 3161 | `ab53503ea351032f323eeeef37559c270c1508e7bf9d16fc85c8fbfac6bd16b7` | 0 |
| backend-lib/src/main/rust/voting/util.rs | 10422 | `6fae74dc805141f6649c3a97fc1b53dbd0ed2d9d3155d33588fd4d80b2f4453e` | 0 |
| backend-lib/src/main/rust/voting/vote.rs | 6007 | `a5655e6c343a8866d052f977d7fb07ba9282dff9bbaeab8ff11aa70b27ee85a4` | 0 |
| backend-lib/src/main/rust/voting.rs | 1300 | `9d65d28f1afcad5fdbc653ffbef511f71fa78e172f810c2b03507f0c2b2e1484` | 0 |
| build-conventions/build.gradle.kts | 2221 | `bfe40a64aa7ef58586d1bf142ea8165b1b7726858b0285082381dabc77621696` | 0 |
| build-conventions/buildscript-gradle.lockfile | 1818 | `5a50547c8e75c67c90d4661ddb6374d2e1b9c937c43107ac5fcfe392a85e653b` | 0 |
| build-conventions/gradle.lockfile | 20074 | `21af30ec686cf74ab65ffcc17b10f2b98c879c2aee72f99aa80451cae7ff25c4` | 0 |
| build-conventions/settings.gradle.kts | 648 | `3648741d5278b36ab973b9e739bf75ef5a21288d402d2bd2dfc980aeba27bcf6` | 0 |
| build-conventions/src/main/kotlin/AgentDirectories.kt | 1364 | `1d85d943c42ab6ad0844451f3809187832cd31b1481a37c16b1e1ab2ea6eee32` | 0 |
| build-conventions/src/main/kotlin/zcash-sdk.android-conventions.gradle.kts | 8195 | `705902814ddff1e11e396fe32bf0171fe569a0411a0823383edcc6de1670e7cd` | 0 |
| build-conventions/src/main/kotlin/zcash-sdk.dependency-conventions.gradle.kts | 882 | `897944473c2768c4e02ea259822001d32d361039fda528a1e7a55b8e01a5f2bd` | 0 |
| build-conventions/src/main/kotlin/zcash-sdk.detekt-conventions.gradle.kts | 1327 | `b7c10d8b318e918ac1f47dff50dc3dc56d5986efd71783d9cc2402bc0509d51f` | 0 |
| build-conventions/src/main/kotlin/zcash-sdk.emulator-wtf-conventions.gradle.kts | 1240 | `f08664e0efda03fd0b05c92bd1b95f49e324b09fd30d2b18564c215bf23e0c42` | 0 |
| build-conventions/src/main/kotlin/zcash-sdk.ktlint-conventions.gradle.kts | 1380 | `e9ca58586fd146ad7187ededff9e082b90c4163d27e25e06fa1f1e97d22da475` | 0 |
| build-conventions/src/main/kotlin/zcash-sdk.publishing-conventions.gradle.kts | 3506 | `aee17c375d894b2b3d00e64de6ca7a05a48c76fea3aa7bb46ef1199a7e23da74` | 0 |
| build-conventions/src/main/kotlin/zcash-sdk.rosetta-conventions.gradle.kts | 1463 | `57d28a87672a1c2abed373c9ff0992116d5e7ccf8f0b5d51fa26ebd5797d8088` | 0 |
| build.gradle.kts | 4567 | `600e91d311bd4dcd1f0e9d7e43f3caeaeea58bbe78270ae39b0091fc318052fd` | 0 |
| darkside-test-lib/build.gradle.kts | 1022 | `d227e2ca21d81e4ea33fe52cedcba24a01f2a8400919d16c0a169243a52dea96` | 0 |
| darkside-test-lib/src/androidTest/java/cash/z/ecc/android/sdk/ext/LightWalletDarksideEndpointDefaultExt.kt | 725 | `1889ee89686e15e9cccd2f80201f39eab8fff9e6fe45332dd25a49609d9cb6a3` | 0 |
| lightwallet-client-lib/build.gradle.kts | 4522 | `ebeaf8fa9c274e1dde5c07226c0e868cbfa831c713ad460cae1970817c74ce45` | 0 |
| lightwallet-client-lib/lightwallet-protocol/walletrpc/compact_formats.proto | 6490 | `d8d0c8aaa5ceec7d5dcc188ef25b04011df2ec0254901620fce982fc13aeb32d` | 0 |
| lightwallet-client-lib/lightwallet-protocol/walletrpc/service.proto | 15236 | `6fbfa974081fb02366a3118a25764af289bdbb86688978f5ff2bae661dfa346a` | 0 |
| lightwallet-client-lib/src/androidTest/java/co/electriccoin/lightwallet/client/fixture/StatusExceptionFixture.kt | 232 | `8d3a9d32c601be002349d41fa5a75387f7497d90c2ce0e553f7602c75951e2ad` | 0 |
| lightwallet-client-lib/src/main/java/co/electriccoin/lightwallet/client/CombinedWalletClient.kt | 6009 | `a5f610dbb2ae803d010be25900717e72d68c89faafa5d048a32549dd06c08746` | 0 |
| lightwallet-client-lib/src/main/java/co/electriccoin/lightwallet/client/LightWalletClient.kt | 988 | `e787c6184019eb322cf755fd716e0be0c7577583123c4ad2a804a60d5d6c9990` | 0 |
| lightwallet-client-lib/src/main/java/co/electriccoin/lightwallet/client/PartialTorWalletClient.kt | 428 | `dcc06dc9559bb98aabe43ff421678ac3513bd810c589e467b7a2f4d7d3157314` | 0 |
| lightwallet-client-lib/src/main/java/co/electriccoin/lightwallet/client/PartialWalletClient.kt | 1236 | `e4cad47f9f821ba404bd6ff94d50baeddb921c3b3192399049a7b7625a59f343` | 0 |
| lightwallet-client-lib/src/main/java/co/electriccoin/lightwallet/client/WalletClient.kt | 3371 | `75e3d0abd59bc65451132830a321a8ddc9a255321c3a772ad7f3494f42b28d53` | 0 |
| lightwallet-client-lib/src/main/java/co/electriccoin/lightwallet/client/ext/BenchmarkingExt.kt | 276 | `5563b0cc6198055c8b87d888a61f7191adb05ad96c3004d8aab0e6844caf7a6a` | 0 |
| lightwallet-client-lib/src/main/java/co/electriccoin/lightwallet/client/fixture/BenchmarkingBlockRangeFixture.kt | 923 | `7c2da8dbbc8fcad826ed88059a4840e9096da8bfba003c29085022694c9692bb` | 0 |
| lightwallet-client-lib/src/main/java/co/electriccoin/lightwallet/client/fixture/FileBlockRangeFixture.kt | 673 | `89e1a977e91d43ca35c52d2a7f778b059ef701331707450fed92cdb0cfddae9d` | 0 |
| lightwallet-client-lib/src/main/java/co/electriccoin/lightwallet/client/fixture/ListOfCompactBlocksFixture.kt | 1253 | `e3a994cd26f650b6dfbcec90d89a45096e48a95c73e8824d66ae5b6de35fb6c8` | 0 |
| lightwallet-client-lib/src/main/java/co/electriccoin/lightwallet/client/fixture/SingleCompactBlockFixture.kt | 2114 | `87da4b33db7106f39419623b5f5cb68572a372062e08f0a471508fce2175c6c7` | 0 |
| lightwallet-client-lib/src/main/java/co/electriccoin/lightwallet/client/internal/ApiStatusResolver.kt | 333 | `a34b7bbbc303e3ad558243ed53dc4a979bc28d2f0f98b524d48a493cf12d4713` | 0 |
| lightwallet-client-lib/src/main/java/co/electriccoin/lightwallet/client/internal/ChannelFactory.kt | 957 | `25ec51abc167c623ff5e63399eb74aefc4b2b152daae092a685aa1b5db342380` | 0 |
| lightwallet-client-lib/src/main/java/co/electriccoin/lightwallet/client/internal/Constants.kt | 390 | `0e1a34c68f449df83cd38bee1862e51f838f2afb4cba99741a4866788f22fe45` | 0 |
| lightwallet-client-lib/src/main/java/co/electriccoin/lightwallet/client/internal/DarksideApi.kt | 6674 | `b2154b2a3708d58e54ced2278565700978d6b67c11a17aeebea538503c025ab1` | 0 |
| lightwallet-client-lib/src/main/java/co/electriccoin/lightwallet/client/internal/GrpcStatusResolver.kt | 2923 | `59af08bab087839a577f8bb3139bcb944b03c9531128a7d5f38e5ddaedc37681` | 0 |
| lightwallet-client-lib/src/main/java/co/electriccoin/lightwallet/client/internal/LightWalletClientImpl.kt | 15701 | `9e36aa7a66bac76cb2316f5632fcb3e55b4f0edf6a476c0b7e1b2a8e31f02e05` | 0 |
| lightwallet-client-lib/src/main/java/co/electriccoin/lightwallet/client/model/BlockHeightUnsafe.kt | 591 | `46864afb8e1460815188db80a78ff17fdf012f4fe3b068be49d3c900ba0457f8` | 0 |
| lightwallet-client-lib/src/main/java/co/electriccoin/lightwallet/client/model/BlockIDUnsafe.kt | 1193 | `a2952c5a892072e941f8cce649f72d00ae34e3684a0cbe4d6e7d253d3001e344` | 0 |
| lightwallet-client-lib/src/main/java/co/electriccoin/lightwallet/client/model/CompactBlockUnsafe.kt | 2476 | `92bd2df66b59e3cf70ee40be10dd9720aca0be81f4ca459b07deb523f34e4e02` | 0 |
| lightwallet-client-lib/src/main/java/co/electriccoin/lightwallet/client/model/GetAddressUtxosReplyUnsafe.kt | 809 | `9e5d567531372670d61bd452a7cfb05b13a9ceae5ae7fb19fa0191465dbbb2d3` | 0 |
| lightwallet-client-lib/src/main/java/co/electriccoin/lightwallet/client/model/LightWalletEndpoint.kt | 176 | `3056b3bbe27ac9b59d7c84f809e8bb5b8619096db7b0c9832da1a39875d9a3f9` | 0 |
| lightwallet-client-lib/src/main/java/co/electriccoin/lightwallet/client/model/LightWalletEndpointInfoUnsafe.kt | 1278 | `c4a57e857f2540cad66e72f793996446ffa29ccd84f6335ba83d8feee34a47ff` | 0 |
| lightwallet-client-lib/src/main/java/co/electriccoin/lightwallet/client/model/RawTransactionUnsafe.kt | 1855 | `c98515e41911449272ad21f515b0fc66bdf10694eb328f38fe1629892cc8414f` | 0 |
| lightwallet-client-lib/src/main/java/co/electriccoin/lightwallet/client/model/Response.kt | 4990 | `ded6c58a3940334a8971c73818449afeeb668b98f0babd292ac0de2ca9f639a9` | 0 |
| lightwallet-client-lib/src/main/java/co/electriccoin/lightwallet/client/model/ResponseException.kt | 281 | `6294b5f73ad2696397d80925cb114d456b61201b5ae39dc74a6130dc82a2faf0` | 0 |
| lightwallet-client-lib/src/main/java/co/electriccoin/lightwallet/client/model/SendResponseUnsafe.kt | 742 | `e331fdc41fafd59329e55faf17d057a750d3b01f4bfa722d1a4af1ff4b52165d` | 0 |
| lightwallet-client-lib/src/main/java/co/electriccoin/lightwallet/client/model/ShieldedProtocolEnum.kt | 392 | `78baf9340a3f070f7a878a8eadb70d44f1d30250cb0965a82527e56450dd2f67` | 0 |
| lightwallet-client-lib/src/main/java/co/electriccoin/lightwallet/client/model/SubtreeRootUnsafe.kt | 1102 | `c59d7f77c76e730edb0457ac10ece7e314f91a5701369c86f91e71ed8c168ba0` | 0 |
| lightwallet-client-lib/src/main/java/co/electriccoin/lightwallet/client/model/TreeStateUnsafe.kt | 998 | `688654d557d917c7cf0937149810ffe7d56038b77493b0bce422152bb856898d` | 0 |
| lightwallet-client-lib/src/main/java/co/electriccoin/lightwallet/client/model/UninitializedTorClientException.kt | 138 | `904c6bd7a8a99b428eb1db09648dbdc9005d14d6acc6156acf8e261701179682` | 0 |
| lightwallet-client-lib/src/main/java/co/electriccoin/lightwallet/client/util/Disposable.kt | 1314 | `cf5a4f6aab7836c735a1f20a1ebfd5d3b2d8855302e7ddd0886e32a29c0abb41` | 0 |
| lightwallet-client-lib/src/main/proto/compact_formats.proto | 7148 | `37782e3d3451b9a78be7405e52fd0b99f05c50195990929388cba80bff3dfe2e` | 0 |
| lightwallet-client-lib/src/main/proto/darkside.proto | 6361 | `e25b7b16975e91a1ece189f6bb3361c5c204054e6f9a260d3e307607db1a475c` | 0 |
| lightwallet-client-lib/src/main/proto/service.proto | 15626 | `5a63333cb338e9f5c98479166f5876b18574ca7ed5d93b7ca50c62ac40c81370` | 0 |
| responsible_disclosure.md | 4651 | `90670bffbab9deec2a1a4bada177134e528d7e797718d0f1bd3dcf8821d1e191` | 0 |
| rust-toolchain.toml | 288 | `49028d2b650057f65c4482b5c1ff79e1e941825aaeb75da3b04a773686ea6d6e` | 0 |
| sdk-incubator-lib/build.gradle.kts | 2512 | `c7a1d0f5eeb7a88b90c4e0343ba485992401c952883d57cbbc9d5b7eef22a8fa` | 0 |
| sdk-incubator-lib/src/androidTest/kotlin/cash/z/ecc/android/sdk/Global.kt | 637 | `21167fc9f46488b13cd60c53fd374f832af00258d594bcdf61866d6df3018058` | 0 |
| sdk-incubator-lib/src/androidTest/kotlin/cash/z/ecc/android/sdk/Iterator.kt | 173 | `c05de87d66ca3dc0a581ff12f90737f6e530b9f33ec1066d7c7c5ec166b06a80` | 0 |
| sdk-incubator-lib/src/androidTest/kotlin/cash/z/ecc/android/sdk/fixture/CurrencyConversionFixture.kt | 407 | `ca9838c26b5a22cef84d77a6cbe6ab16f65ca409653e2a537125286a42897a63` | 0 |
| sdk-incubator-lib/src/androidTest/kotlin/cash/z/ecc/android/sdk/fixture/FiatCurrencyFixture.kt | 201 | `0548a11e3f69a00d79f96395d1de9fef5560e746e99d969c8646b27395198d93` | 0 |
| sdk-incubator-lib/src/androidTest/kotlin/cash/z/ecc/android/sdk/fixture/LocaleFixture.kt | 365 | `c5d3c1071079980b1251e5643f1c1b178aa4b37c6fa06d2e3aecdd34148ca2c8` | 0 |
| sdk-incubator-lib/src/androidTest/kotlin/cash/z/ecc/android/sdk/fixture/MemoFixture.kt | 218 | `1245d59c5222002d405338569ab2364f24b8f801bd0f72190286e5f000f68a1c` | 0 |
| sdk-incubator-lib/src/androidTest/kotlin/cash/z/ecc/android/sdk/fixture/MonetarySeparatorsFixture.kt | 369 | `bd29f611e6dc90625a2651d63935171cb38af8ecf5c4885e4fd2b818d8170327` | 0 |
| sdk-incubator-lib/src/androidTest/kotlin/cash/z/ecc/android/sdk/fixture/PersistableWalletFixture.kt | 1342 | `eb0053f6551937d2e4697077329d54261b93038fe9dfce50da940bb5bcf91f3f` | 0 |
| sdk-incubator-lib/src/androidTest/kotlin/cash/z/ecc/android/sdk/fixture/SeedPhraseFixture.kt | 411 | `56cf644437fc1d72361bb70abf1670d8b423ced0b759f599476bc5b51f8cacad` | 0 |
| sdk-incubator-lib/src/androidTest/kotlin/cash/z/ecc/android/sdk/fixture/ZatoshiFixture.kt | 238 | `0fa55d426432c2bca7def96ee6244cf161899ebc38ea4e659c0ca1493f45a148` | 0 |
| sdk-incubator-lib/src/androidTest/kotlin/cash/z/ecc/android/sdk/fixture/ZecSendFixture.kt | 780 | `9bf2f448dc2569c9c83bccc9667eca2d1fc58e77f41295edd3e861772befaa17` | 0 |
| sdk-incubator-lib/src/main/java/cash/z/ecc/android/sdk/WalletCoordinator.kt | 10258 | `68e106fee3e5d91f434d9cf15d341f753a3e364bd4d7af5d877b09846ff62e72` | 0 |
| sdk-incubator-lib/src/main/java/cash/z/ecc/android/sdk/fixture/AccountBalanceFixture.kt | 976 | `05e92ad8bb0e567d38d78b20170827157f888a1ae2812548a3dfcd37a76cb00f` | 0 |
| sdk-incubator-lib/src/main/java/cash/z/ecc/android/sdk/fixture/WalletAddressFixture.kt | 914 | `aa28d836e1599e478da5530f4bf8120f970729eef549f1d8b19feff46c2d38dd` | 0 |
| sdk-incubator-lib/src/main/java/cash/z/ecc/android/sdk/fixture/WalletAddressesFixture.kt | 588 | `8336d1289e261c78cab02339d3877c7c24be5f7c88137d25c9fbcea7897f8e82` | 0 |
| sdk-incubator-lib/src/main/java/cash/z/ecc/android/sdk/fixture/WalletFixture.kt | 5261 | `530461089860a0db9972b942de1d7867b4ccbd28dfa3c5edf2d113c438504d97` | 0 |
| sdk-incubator-lib/src/main/java/cash/z/ecc/android/sdk/internal/StringExt.kt | 219 | `96ec01a54de6c193389b55bb14025adb388cd6269f6c784078491bad6da2df52` | 0 |
| sdk-incubator-lib/src/main/java/cash/z/ecc/android/sdk/model/FiatCurrencyConversionExt.kt | 461 | `68cb4ba6e357b7aebd7793f9ed158c02f460fd894ff52ad0c853cb8f654478f8` | 0 |
| sdk-incubator-lib/src/main/java/cash/z/ecc/android/sdk/model/FiatCurrencyConversionRateState.kt | 1435 | `f802f2e8501ab5233ba57f8ecf6504184a91ae37ad4f9063cdca26f1c3404afc` | 0 |
| sdk-incubator-lib/src/main/java/cash/z/ecc/android/sdk/model/Locale.kt | 983 | `50b5503ff2c0b607ebb7a22a0e683a5da5aa96eef3d8f1785007d9d5cbeb4456` | 0 |
| sdk-incubator-lib/src/main/java/cash/z/ecc/android/sdk/model/Memo.kt | 768 | `c2b226e48e7fc0734aa2d0e4ade0c8ca8f78fb029d178547d7b9d94d66459aa0` | 0 |
| sdk-incubator-lib/src/main/java/cash/z/ecc/android/sdk/model/PersistableWallet.kt | 9299 | `52120b7396ba66a10487a510603faf277df7432f7d9be8049fc767297a1f9be7` | 0 |
| sdk-incubator-lib/src/main/java/cash/z/ecc/android/sdk/model/SeedPhrase.kt | 979 | `52bfdfe001ea202202e5a8e7861d076b3709f6dba1c01b30091c72788f7f6a1c` | 0 |
| sdk-incubator-lib/src/main/java/cash/z/ecc/android/sdk/model/WalletAddress.kt | 2132 | `4c986602ae28be9c5d95325beea8da9006395be852302b3b948c0b68e7027c1b` | 0 |
| sdk-incubator-lib/src/main/java/cash/z/ecc/android/sdk/model/WalletAddresses.kt | 1151 | `8aea782603eefe5c7c88df0640f56327f730c25238813e56ea3b27205718e5d3` | 0 |
| sdk-incubator-lib/src/main/java/cash/z/ecc/android/sdk/model/ZatoshiExt.kt | 3021 | `b894c509562e466a6649503c2d370195141a654a190866be1ecc0ea492cb71e4` | 0 |
| sdk-incubator-lib/src/main/java/cash/z/ecc/android/sdk/model/ZecSend.kt | 872 | `9a8d47d42a35ba23bba98dc1236c402f9ca6f8f9dce89c9e5d221e8b9be7316b` | 0 |
| sdk-incubator-lib/src/main/java/cash/z/ecc/android/sdk/model/ZecSendExt.kt | 1644 | `4366884b3d8fb77f1618db850e6c922253e3e73600cfe95ab42473f41218e31f` | 0 |
| sdk-incubator-lib/src/main/java/cash/z/ecc/android/sdk/model/ZecString.kt | 5384 | `37f99fe5d1f030ea82e9cf663b6ce13fa83f6f69397e894ba63d2648f3d5e477` | 0 |
| sdk-incubator-lib/src/main/java/cash/z/ecc/android/sdk/model/ZecStringExt.kt | 2684 | `4d59403bc33e930367e60500b975fceeebf3f859fb562a490e01a87b56639bdd` | 0 |
| sdk-lib/build.gradle.kts | 5236 | `10e88243c22e3a11bb56b40e9fc620a2f3b7ee381b1111182afb1e6dcab32fe3` | 0 |
| sdk-lib/src/androidTest/java/cash/z/ecc/android/sdk/ext/TestExtensions.kt | 4430 | `e9594465622927d50d33632c8a136b674814ae3f91f18a6630f1bd9357fdfa7a` | 0 |
| sdk-lib/src/androidTest/java/cash/z/ecc/android/sdk/fixture/LightWalletEndpointFixture.kt | 1128 | `654d8bfbe6cf8f88862fba75d216c1573f9d41fc70a3d4f4ab4d42f0d84d50e7` | 0 |
| sdk-lib/src/androidTest/java/cash/z/ecc/android/sdk/fixture/WalletFixture.kt | 1255 | `3a20a91da9facd8040c4f87d2ab1851f43117afa43fb024aa6d4c53622b2c62c` | 0 |
| sdk-lib/src/androidTest/java/cash/z/ecc/android/sdk/util/AddressGeneratorUtil.kt | 1571 | `0ce2c4323fff93889d52c30a386bb39a18ac932ba99a378ab248f2ad6b3ee4f1` | 0 |
| sdk-lib/src/androidTest/java/cash/z/ecc/android/sdk/util/BalancePrinterUtil.kt | 6442 | `6eef910860daf705c815a1d495a0553fff7e9f7790efb368897bfba5d1568564` | 0 |
| sdk-lib/src/androidTest/java/cash/z/ecc/android/sdk/util/DataDbScannerUtil.kt | 5516 | `0be2ff3ade94dee8a5a9c68d2c02f21a894fb6d6278fc4aebc97c4bbbd83073e` | 0 |
| sdk-lib/src/androidTest/java/cash/z/ecc/android/sdk/util/SimpleMnemonics.kt | 1110 | `41dfb4995d9767038bbe572724173f6f0a84e450bdc444acff937f4655ab97ad` | 0 |
| sdk-lib/src/androidTest/java/cash/z/ecc/android/sdk/util/TestWallet.kt | 8178 | `7c48cfccc8bf26ee4150a1d00ee7d40bd3aea607f35f477abc55af4cdc56f022` | 0 |
| sdk-lib/src/androidTest/java/cash/z/ecc/android/sdk/util/TransactionCounterUtil.kt | 3313 | `0fe9deb916b32f684699585ae9c52d9b55e427a5ae2f60010d053ed96eabf82b` | 0 |
| sdk-lib/src/androidTest/java/cash/z/ecc/fixture/CheckpointFixture.kt | 3398 | `93e668639877448462d7798796338eadabc782ea1f74c1fb216686e188b21913` | 0 |
| sdk-lib/src/androidTest/java/cash/z/ecc/fixture/DatabaseCacheFilesRootFixture.kt | 688 | `dc2f4c8927620286ce19219173be5864dbd1a766f8d0f634e66a884018554762` | 0 |
| sdk-lib/src/androidTest/java/cash/z/ecc/fixture/DatabaseNameFixture.kt | 1212 | `f4f7095a70e615b2522c8fd665416a33b42600b5285c3ed535343657b5408eb1` | 0 |
| sdk-lib/src/androidTest/java/cash/z/ecc/fixture/DatabasePathFixture.kt | 1341 | `0a0b2381fc620873065046b36e45ea5c08b50b561dc6a1467633fc986d625aaa` | 0 |
| sdk-lib/src/androidTest/java/cash/z/ecc/fixture/FakeRustBackendFixture.kt | 506 | `1933a335c42bded361c4410e347f50807d5ce2d06ced9d2d16492101e1dc14d6` | 0 |
| sdk-lib/src/androidTest/java/cash/z/ecc/fixture/FilePathFixture.kt | 528 | `de2de09fc4c01bac1879dd31d47f8bf6047e1ca28a837d43b727c46fa1c085d4` | 0 |
| sdk-lib/src/androidTest/java/cash/z/ecc/fixture/SaplingParamToolFixture.kt | 1421 | `de623d79d5937c575aeb4ca01135fae52013737387a5ff23b58eb5eb41c779ea` | 0 |
| sdk-lib/src/androidTest/java/cash/z/ecc/fixture/SaplingParamsFixture.kt | 2217 | `c1bd509eb5f532aa911d12f77aed581ed2b4428033ebb5ffbd71fd50a21d4ff8` | 0 |
| sdk-lib/src/androidTest/java/cash/z/ecc/preference/MockPreferenceProvider.kt | 1098 | `f6ad193c1f8a472a349b2269064eaaf0aa1f3bfc2a1daad14cba6b742ec963a2` | 0 |
| sdk-lib/src/androidTest/java/cash/z/ecc/preference/fixture/BooleanPreferenceDefaultFixture.kt | 438 | `ac781af353613f3b6c53a225a49131e1126b56fa9e5f000aa4b7cc3b1b99b6ff` | 0 |
| sdk-lib/src/androidTest/java/cash/z/ecc/preference/fixture/IntegerPreferenceDefaultFixture.kt | 483 | `724a0d6c687d80693e91fb447cc6378fba39627d3b47804ee7a01fa6a9ff8a4d` | 0 |
| sdk-lib/src/androidTest/java/cash/z/ecc/preference/fixture/StringDefaultPreferenceFixture.kt | 512 | `f3ea58b0cc8e3f5a25ff5c5df769b6bba4037f3af436129cac2a4b00e6d09e43` | 0 |
| sdk-lib/src/debug/java/cash/z/ecc/android/sdk/annotation/OpenForTesting.kt | 588 | `c07c7a84990483414a5973cd00b877bb62d12f7e0f1348e3e73148c4a4441289` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/Broadcaster.kt | 1721 | `c3f97a5fcaaaf17421d5339daa222a9df75950952acf8e58b21abb41bc3e8f8e` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/MigrationSdk.kt | 58806 | `22aa7fe2a677005ba296f9d363a4f495c83e222bffbd4e186ccfb5810d138dc0` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/SdkSynchronizer.kt | 59105 | `7c28ecbd3405b2dac884d8e0092ec07608bdfaedf96a6f3b8d7ec1d6ec94ae03` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/Synchronizer.kt | 61009 | `32958fd3979af8f75e08bcdf3521c590d61c67f0c0f139698575ef42a82f1933` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/VotingSdk.kt | 14094 | `7178feaa09781c21c6bbf11aa423873013f81ab666ea9f626a27586606015bbb` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/block/processor/CompactBlockProcessor.kt | 138070 | `a40f7456677c4f4c5fd36ca539f88e31d6e21a166f79660ffcc78b0cb6d3dcde` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/block/processor/model/BatchSyncProgress.kt | 503 | `813e2e02077de3d698b77b0507a3e726b829b96b8d8684e190458b95a8632302` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/block/processor/model/GetMaxScannedHeightResult.kt | 469 | `bcb67d8bd1a2fe4e2b97bd0f597812b0979ea59fc2f926de1224b3a0ec4002a1` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/block/processor/model/GetSubtreeRootsResult.kt | 770 | `cac5f3bf9bd9b267e8dd536d9fd7c9363973f1db766039399383e9c7e4e0fdc7` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/block/processor/model/GetWalletSummaryResult.kt | 776 | `e984f53da67ba93dd7b772d36f976560c43cfe6f290358cd60ea7bb7aabd5c4a` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/block/processor/model/PutSaplingSubtreeRootsResult.kt | 427 | `86b9c1bd7af4d0e284feee425dc25335ea5afbfa995e2643b4e91430436a0e1e` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/block/processor/model/SbSPreparationResult.kt | 956 | `8884ab10f010e00d0439bdd99ad778b13b4b9e67ddfb0ff2669fe2fe5fb3bb4c` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/block/processor/model/SuggestScanRangesResult.kt | 510 | `b852bb0eed50a19f30ff38379b2c8b1e4c3e736911226b7941fd7961670a6d21` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/block/processor/model/SyncStageResult.kt | 340 | `6e12936a4d29d3f5e5cfd5e1c8b6f387ed64cbb3c2ee381f6152c7fe98d77799` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/block/processor/model/SyncingResult.kt | 2746 | `6c0f6577a92549b3df465b23831593eac2cc9bc96f5845ac4113837001216d4f` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/block/processor/model/UpdateChainTipResult.kt | 437 | `6c158ebe7a32d23630423dd6ef76559427bf10b07e1893210c4a8b7df4149492` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/block/processor/model/VerifySuggestedScanRange.kt | 396 | `c7fe8e8a9b855fde88ead2914cdfce81afbd53d5c6900404842b1843ba30299c` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/exception/Exceptions.kt | 22201 | `0a9c088049ae1277680f5c87d6489bfeac4f4988aa02ca107747839350e3cca2` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/exception/TorInitializationErrorException.kt | 168 | `394d603ce4e119b810f859afef3f90a2ed4ae798d2d8d8a258b94d41192370f3` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/ext/BatchMetrics.kt | 1575 | `1b2d458cec217f82c4cf350a35dae670cd3da480110fffd64ee381cc01aab72b` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/ext/BlockExt.kt | 948 | `42cecab37632370cb082bef25c032de68e6b43641d21c83184f5d3214e02fe49` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/ext/ConsensusBranchId.kt | 1557 | `2cb2c9bdb73ce6ec56b2a3e120825de53393eb762eb81475cb5b4448726bcb8a` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/ext/CurrencyFormatter.kt | 15899 | `c9c3f58d26f34d46da8cca6104e5f332b1334dd5da7d0b223a9d744717f10c37` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/ext/Flow.kt | 1983 | `6feaf3ebb5e94db71264b55d56955d4061675235644eb6655b6980436be2cebf` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/ext/ZcashSdk.kt | 2592 | `a30062764147f9a29d49be7a036788f31293af4a4d289bfceb36a837aa1079a4` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/fixture/AccountCreateSetupFixture.kt | 831 | `ab4d7363d4d62ec01dd7403f2e265a2d375e45b0b38427f6e404f881a6ad1a20` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/fixture/AccountFixture.kt | 2458 | `f5e032a0a2a801044ed50d60ef18e227cea4e4758c4a268667e4ef8837ef1386` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/fixture/TransactionOverviewFixture.kt | 3324 | `23642553eef31a7f8acbf8e37b68fe7333d975cd1a0e026b8d72c771a50fe56b` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/fixture/WalletBalanceFixture.kt | 896 | `54a8b18cb3dd9cb5ace483d6503799f2a2af9282c9909b5d5de304b2bb151fee` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/AndroidApiVersion.kt | 1586 | `b7c3d865c28a613b1474b57cda766f5101cf4238cce1ff050992bae3b7ac21e7` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/ChainTipEstimator.kt | 6247 | `1156a4c4fce93f85bc4619044080d4838cf64d95d342d59773e5ad1f2adf3862` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/DerivationToolExt.kt | 2627 | `2e96a597a7abb721298cdd1d067f02f6e184356316a0b841d3917e10ce127fc0` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/FastestServerFetcher.kt | 11091 | `b8ccd3e3853bb744db63741043d18ffc0d727e9ccfe362f893e15ad453d58174` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/Files.kt | 1939 | `b676d313e21caed72b906707eafe55781751f7c10229ce05b5009437cd45ecd8` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/ImportAccountErrors.kt | 1067 | `ed5349d0f554ef888eb068eb044ab9b9c301f7a722d6a071005e87664c1d91a3` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/LazyWithArgument.kt | 1002 | `fedf00159aea09b8b1722b38ddf86d4a897096eba1d3025c817d30d1403db211` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/NoBackupContextWrapper.kt | 1606 | `02de36958958ed26a525b7caeecac91a80748443483dd233cdef18dc411a55f8` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/OrchardMigrationSdkImpl.kt | 94617 | `ba525aa40dc494721d6369adc270da6e3610b872c2e6a8c224626c1371520263` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/SaplingParamFetcher.kt | 2416 | `8bf2693842a150bfec8cf76f856b29b145cd3d48d21d2b22e6e5bd327cb8caf0` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/SaplingParamTool.kt | 16328 | `bd1e5e2072153e41bdc2dd68ec44fabbef5e1d066679dc5a0a5107c4d1083735` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/SuspendingLazy.kt | 747 | `25cf4ca6d476b7cc01aac278dba436a468d9fb3fcb0f378e5637bc2fe4c6353e` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/Twig.kt | 6122 | `06803b49e24f03ca81c04783803d9bc36f67f3fa7b6eeed9778eeb3acd97cdaa` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/TypesafeBackend.kt | 11290 | `a56c54c20144c6b7eaa404147d05c5992a907b3de7c94c3394ccbaec6bae50b7` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/TypesafeBackendImpl.kt | 14715 | `d4d3f915b3b938ff8927474ae0a28f3dd9c0df45a8464d1a16949ea34956ec59` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/TypesafeDerivationToolImpl.kt | 2708 | `370b0f1e354bd203a793b5e20c245179b004401b68967e2769344944b54ff161` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/TypesafeMigrationBackend.kt | 12380 | `4ff7b5f1b2c2c31071d3068d2860729f13110d6fdf63cbaaf38207a2dc1e7183` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/TypesafeMigrationBackendImpl.kt | 12063 | `f9d6d7fb8c550bff90922e942373d8df6fcdf4e33404cf6297db14b1cad37395` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/TypesafeVotingBackend.kt | 22477 | `4f22dcb372b4cf45fd20ebcd376bee9c3cd8a4e1c92d070dc79cdbbf16975184` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/TypesafeVotingBackendImpl.kt | 49983 | `3e60aaca6aaba9cadcf131c0b75312c44fa87cf60a234082b5c7ad3c95fcd9b9` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/VotingNoteInfoMapper.kt | 840 | `b67ecc3750760a2cf912b0596cf2740fbb4b304319130215e7373a83ad2176a0` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/VotingSdkDelegationMappers.kt | 3535 | `a1cfff3ccce87796b682422ff4e46bb175e4d1102a4860a67e3de86aa5fefb58` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/VotingSdkImpl.kt | 16226 | `00e484870e1ceef4ce7800645b6dd3b02ee620bcdfbc0af2fcbbcf19930e58a1` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/VotingSdkNoteMappers.kt | 3862 | `446a8e8caada197b4da93c470b25d994e6e6afa744e7ed1d7594a1fbe17a6579` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/VotingSdkRoundMappers.kt | 3021 | `09493218690f27ae3fa15f2596dbd1ec95f4d93bc3c566ef99e1df46a0005413` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/VotingSdkVoteMappers.kt | 3363 | `c7334ba9014e6ee44a9ae0c4a914fa0ab56c329cfed65c5ff928d29c85af7593` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/block/CompactBlockDownloader.kt | 11972 | `3bdbebd4aa4e8ce04522d110bf55e4fa05b7f15fb7d630e68bfd68909be6178d` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/db/CursorParser.kt | 634 | `7aa79d653e46f5aafb5c1bfaa04bb8263aa470e02cb449a7f8557fcd83c083f1` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/db/DatabaseCoordinator.kt | 16623 | `8bf7ecb7f38a1d87723adef30a2ce7e2519a246cc29b0d0bf6dd0ee6de54a41d` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/db/ReadOnlySqliteOpenHelper.kt | 1541 | `56993339efb8ecb3560ee5d53dfd3360967403b5de12f8b0c3c6f98fa3e60336` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/db/ReadOnlySupportSqliteOpenHelper.kt | 2096 | `fc5065c278d2a6fcc26cee401f1b94478251d1531fdad2598ade963a7753847a` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/db/SQLiteDatabaseExt.kt | 3787 | `941f990f944bb1f5769c6af89345c440629d836ef73af8e3d3740c4ef3378c18` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/db/derived/AllTransactionView.kt | 13314 | `1047158e12454a429abbf92c6ab9892727063149ca7cbf6ce5b659e554a6ee7e` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/db/derived/BlockTable.kt | 4075 | `76244faafd65b81aa3244bd83c3dc5e06468b1e379da7efbb2ab81d42b0c96d8` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/db/derived/DbDerivedDataRepository.kt | 4441 | `0d91651d665300a303ee8957dacff23a1704b648baf0036e5235ee65ccfbc867` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/db/derived/DerivedDataDb.kt | 7025 | `e94b99fffe12526fbd23c30de0fdb8bfa87a813ac0a5552e48b05f77efb80eaf` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/db/derived/TransactionTable.kt | 5209 | `83118710169ebb1bf5d15a013822d7fcbe24bfd73fac23b18a4bfb35778c4152` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/db/derived/TxOutputsView.kt | 8307 | `a083fcfc478f890b4f7c6b17d28ef9a4bbac9b2d4a7d4e137279424b94f822cf` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/exchange/UsdExchangeRateFetcher.kt | 2229 | `bf30d5b5ca87c086df9325a23d825fd80b9e3b3c673afb5bd8baf76b4ff12d6b` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/ext/BlockExt.kt | 460 | `476b87e99414743ca51cb87de2140d0dd7544e55301bf5e9b787325b73313504` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/ext/ClosedRangeExt.kt | 570 | `542fcaf7d08111686d07dd23c3e6a054283a873eaa31bda3d4cb5cbc31ea3542` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/ext/ContextExt.kt | 789 | `4b3aefe607b541e94ffb0f9f493b4c2b64626d387dd4ad2e27588acde7444c53` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/ext/ExceptionExt.kt | 2575 | `996fe9cc15c92016df407864738f3685dad247470599c91a56ac072279cf6cc9` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/ext/Placeholders.kt | 4539 | `5c2560b85c1fb1f79d9f38f5e9477cd0ad0478b8f743ec226cafb2ddebceebbf` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/ext/WalletService.kt | 5046 | `746d500073709fd7a75334b63abdaa6b6397ec4ca2af155c73dd4c5590cd5ec9` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/metrics/TraceScope.kt | 1274 | `969486dee0af293a0b1eb7af7f2a9c0b55e31c92e8cd67013569c2212bbc936a` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/model/BlockBatch.kt | 430 | `d363cfede9c4fa040e0f63ef1cd97b4907caf26c638d3f1aa8d9f2912174785d` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/model/Checkpoint.kt | 1567 | `400213030402749e2914e714d20eed613b5bfa8b3378a6dc11c0a000751bb963` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/model/DbBlock.kt | 284 | `1600661f959c9e7cca795f9efb6e21afa87334a93046fef25f1fcc1e426b33a8` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/model/DbTransactionOverview.kt | 1169 | `093119c3e9b7d77e7afc87c5df613a51b1e3f03c44691f4823939e08ab8d337c` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/model/EncodedTransaction.kt | 473 | `2ecddd155c753b2ebc67654ad5bbcddaebda3dca298b84ba9650f4f595cb3305` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/model/OutputProperties.kt | 696 | `d4f563f890fddcf42a49d4a0c8aa10642d119398bd8ad2fa7788bbc3e254238b` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/model/Progress.kt | 618 | `87220a4e155bda1454c97b9679c33d4bfacd77edb0575f5a1ccf78bff038b3cc` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/model/RecoveryProgress.kt | 683 | `ca30b3b71a897b14acb7cb16c3c54840e035ef92af4ba86fd369ef9eb82412ac` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/model/RewindResult.kt | 1036 | `8cdf149a3d69ced85a411f5a3fb52fa07db868de1f22614e8ffefc3f82b3d959` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/model/ScanProgress.kt | 559 | `233315f5b556c404a88227c0058ae8603a4ce8439a7bac53a0e49342c23bec43` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/model/ScanRange.kt | 1935 | `579d63a3f1ab29e4cbbb802ec47e5de61c1ef1830f6dd6bd961880f1d1201a5b` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/model/ScanSummary.kt | 831 | `dea370ab7713e3bc65f428d499c81b96d99f77435ccdeddd58c4161406a65cc9` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/model/SubtreeRoot.kt | 1421 | `60be555a85faef436a5e638a2f0af77ae8735a9a90c9e3f12bb44a372857db22` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/model/TransactionDataRequest.kt | 8140 | `a3b21fd908d94fecb13a72eae97ba22819756084f8e37a24082424a811d1b583` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/model/TransactionStatus.kt | 672 | `9dae56875f3c24508e8ceccb445628747a4deebe006606c5e02183782df34659` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/model/TreeState.kt | 844 | `532ae7a2640eb72994b4245dbacd108e7992ec30b39e7d2cca691049f8201607` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/model/WalletSummary.kt | 1416 | `c98a9dbc4714defc194a85266102ea935932dc9f8234b7cc2f90f1f68e23780d` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/model/ext/BlockHeightUnsafeExt.kt | 350 | `787b22ef6757efd04ed4aa7c54dac80c08ee9f945a316e5771b452cbd6fa3fa9` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/model/ext/CheckpointExt.kt | 3266 | `fb75c04af14c2c882cd250b899053d8a75ff51203bc352f03c8bbd6ab5fec74b` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/model/ext/RawTransactionUnsafeExt.kt | 712 | `371f96eeeb75fa1a0b370a59e759f80d547ff645d50a6544dea0d37e35e22ce4` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/repository/CompactBlockRepository.kt | 2132 | `89d2f6a2f0ac253ad60391963c1f53f7e967edda971654d9ceaee5f0e94e9e03` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/repository/DerivedDataRepository.kt | 5413 | `fad04b2375650e514f7977249197ff6be107414a8d199c791443ecd24d58b05e` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/storage/block/FileCompactBlockRepository.kt | 7532 | `6cc46b8af6df2bbb7c7c5190f6bd48e278e8b32cbeb4172f33bf4ac48ec8b2ae` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/storage/preference/AndroidPreferenceProvider.kt | 5066 | `5a8bbf0efe10365ee6935abf76f8d6c64ca1b62070973da065b2e088fc959f96` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/storage/preference/EncryptedPreferenceProvider.kt | 489 | `f4d0fb48eb3a8557d2043906861a6b3aa761abbd924e2a57577c52890eb421f6` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/storage/preference/PreferenceHolder.kt | 870 | `6fddc8e6863777ecbf27059fd63ea660fd5c79a10db46fff35154bacea3af9b5` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/storage/preference/StandardPreferenceProvider.kt | 477 | `3a7014432ae7a8d37e22e2b3a81b29525cf6b220b1a511564d098b64d5cddd05` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/storage/preference/api/PreferenceProvider.kt | 728 | `4d8654ade9e5a9a4dfee4fd30161f20f3d2b39c2b94e4f4c00c169f27c8ec56f` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/storage/preference/keys/EncryptedPreferenceKeys.kt | 2814 | `d245ae0749a738fdeef28b26b0da4be59f1f1a8a0780676dfc9f8abea0771a57` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/storage/preference/keys/StandardPreferenceKeys.kt | 484 | `cc5aa95d99846ed423019bd41c8981c0662acc1115de83df938346958d125776` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/storage/preference/model/entry/BooleanPreferenceDefault.kt | 1011 | `25a36ea055fa204958b804f843ef8e49d6ea5a1187e638f37986e61e8c15f01b` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/storage/preference/model/entry/IntegerPreferenceDefault.kt | 950 | `a0f26ad0903cae0e3408fc787d96e1af8d45e2519ed59f69cffcfd3c6f65f111` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/storage/preference/model/entry/PreferenceDefault.kt | 2183 | `5d60a0b8e798cf1c6920764b26e733472e1f98eeeb6a71e83c69061e74e366b8` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/storage/preference/model/entry/PreferenceKey.kt | 1133 | `6ff7c424c2bb6112b5a10590efee11582a02f784483cddb56b0a13dc6e3cd1b6` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/storage/preference/model/entry/StringPreferenceDefault.kt | 619 | `235f63ec897b50c479bee6a061ab925fe3ea88ab93e92190ab1c595edfc2f9fa` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/transaction/CreatedTransactionExt.kt | 336 | `b1000a9a2c55e9f392202209182827ef236fa3407f5a88455bb72dd560fc97ae` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/transaction/OutboundTransactionManager.kt | 5923 | `c7ced5f973cee37bdc755f5450387a4364597d724aac85eba2c5bd50194babf0` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/transaction/OutboundTransactionManagerImpl.kt | 4107 | `dcfdac512e040f1b6628580f8277f1df1cd88bbafa7b37e20f6f6c2d1f3b27b0` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/transaction/PendingSubmitPlanCodec.kt | 3667 | `7293cafede86aa6db9c4484c0bde7de70db32b7830b63caf3f5bcc3a53c33f41` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/transaction/PendingSubmitPlanStore.kt | 6760 | `2bcef01aee55180b30a2837a68ee5d6e6e6e73512ef7c2a8825860343e10ce72` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/transaction/SdkBroadcaster.kt | 5893 | `7a938e03748a03aac031fb50fd408c40b1ff84d094c058d3bcbfc563232b8aa2` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/transaction/SubmitPlanExecutor.kt | 778 | `7c89f80d38627a6ccb701fee1f5e1040c1480cab75113ac16790e2e2c2cdc940` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/transaction/SubmitTransaction.kt | 3740 | `71ac10bade79c775d054c3a1eb957b70511d4059b74634e61438936af7922610` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/transaction/TransactionEncoder.kt | 6108 | `af7ca847a2dce14092047131b2be8c94e6dafea7b29675ec588bbbb0998eced0` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/transaction/TransactionEncoderImpl.kt | 11825 | `bbb2803ef94d19b1478c927a2bfcf221c760ffa6cf2ab0202e3686af8cfbe60e` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/internal/transaction/TransactionSubmitPlan.kt | 359 | `fae5415927cbf3075b4a523319a841aa9e2f97bedf53a50030791c5bf8389df3` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/model/Account.kt | 4936 | `3aefcf680071e990fcb546cfd863274a6ae194ed3e4bc8f9a62a422e160eb2a7` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/model/AccountBalance.kt | 1570 | `91b08f121849502cb494ab64f3d2c07ed6d1156f1320699fdac24a29557629c2` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/model/AccountCreateSetup.kt | 808 | `0c7484d25cda6adf5dca945b39de87caef3060accb645bde1ad3e6da601dfbd0` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/model/AccountImportSetup.kt | 1129 | `6a22bd63b1747b2e5b54475302c0176e91352a2997cd6ef9d707a5ad3574d959` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/model/AccountMetadataKey.kt | 2625 | `536aec740fd4b4de22a011e669a1f0338254d7eb0d67b12ca1b5f6b033827bba` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/model/AccountPurpose.kt | 1001 | `39282822ebd448a8f9e7413163fdc9e20d12a74df81603504e7144a56e64ecb0` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/model/AccountUsk.kt | 1126 | `6697b11f5035e2e2c1378de8222b1fa4943755c465bfd9386e079c23b06cf258` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/model/AccountUuid.kt | 847 | `5ab0a58247960a5ae597158b6c59d182e87da32ea1ca936b82d6071d223c9716` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/model/BlockHeight.kt | 2507 | `db7c2698edd55f3f6b38534a902605d19b7491c6c41c62985a1cc9b32cb0ba82` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/model/CreatedTransaction.kt | 545 | `89f2a80b506dcf7e5b34bd336ef8a65020b7bb90caffde581db6382df936832e` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/model/FastestServersResult.kt | 631 | `deb67f285bf0d740028ebabdb2244547e92b7d196a4f71c6d059e7db360ce1dd` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/model/FetchFiatCurrencyResult.kt | 360 | `43680e376ed36061a26d63ef5cbdf7408cd1e9fb8f702c63f7d03e6595584580` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/model/FiatCurrency.kt | 995 | `2f7871c1684ce09b6e969b02a5b81ea44688d3bc8b3200949b489f24b084fb38` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/model/FiatCurrencyConversion.kt | 778 | `5b820d20c97aab01558f7b9ff9479539856f15d20fb6ccd3250c166550ac37a6` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/model/FirstClassByteArray.kt | 528 | `56e8ab9e8a9b61e1c855472ccddf68536c9fa4916a3c3746e6b80a7230780833` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/model/MemoContent.kt | 8663 | `9b306a57ce3cf940a1e7229137ae86c342cfc9cb81d19320ffce6e6a66338969` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/model/ObserveFiatCurrencyResult.kt | 174 | `73051b717627cf0200159cac055b1b78266c7c9cf8966d95bad2fa96746e7ac3` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/model/Pczt.kt | 446 | `4be9eec2c44831c5a932a81e59c23af64e07a98c5828a2378d7d782fa785620d` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/model/PendingTransaction.kt | 5482 | `cd9208ef994f1124e99a90373d8ff3feed075d7a2431940518091b9af452a42d` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/model/PercentDecimal.kt | 882 | `fcc6e0aa7dbfe2938990d1d89faf1e83843a6caa22f9cce2d050688f7eb288fb` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/model/Proposal.kt | 2292 | `4cf55b39f5b7468fec1cb896d92adf2952d92329aa6decf633491e874bae4a80` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/model/RawTransaction.kt | 1661 | `272552de6720669df5b3a10c11d46ade7a2dd2a9f92ac4275f86cc5463faa0b2` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/model/SdkFlags.kt | 464 | `7fbe1f2c16010788c0ae68e4114440255cfc4f19f887609ce83025c00be663ad` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/model/SingleUseTransparentAddress.kt | 958 | `4c5e33a3b0831031fd3bd21faef3278cb72a980eb77f12c37d1c478c2e45a646` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/model/TransactionId.kt | 2013 | `a680d2ddaa3f4bb8dfcb2f8e789cb3fe3be148133e27998c633d10be1a12b630` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/model/TransactionOutput.kt | 189 | `cab97a36aeeaf2d2af727c14f5c895754a1dfec47e3230be8bd0ce5475d7e5e7` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/model/TransactionOverview.kt | 6714 | `6a521c8ec82e2500f2f128f0e7c313d6f915d6ba3741650f3f5bfd201b196a4e` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/model/TransactionSubmitResult.kt | 1992 | `01d6fb49fced00c39aeb5eac156dd9cda926c0900b6169ced1354b04859d9f91` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/model/UnifiedAddressRequest.kt | 1069 | `095a7f2ce546f5c6f12a9b8b211f775719b7f0a5d18320afa22ebbb213242004` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/model/UnifiedFullViewingKey.kt | 440 | `c8dc3d1238197a395e79f3d92ed5abd34fce4b6dfb5fb2682d5797e2a73da9ee` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/model/UnifiedSpendingKey.kt | 2506 | `6d166e98ea45daec368fdc087e6c0ad2461e438fa57ff7f05e302398196d5677` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/model/WalletBalance.kt | 2165 | `7adc1bbbd6923848cc954a23f07587fbbb2d2d63b03124895a3e9ac0ef525cb5` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/model/Zatoshi.kt | 1163 | `946f9695a267d2e07e211199fe8df9709a1cc872cc532e1fa9251c89f8cd2991` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/model/ZcashNetwork.kt | 1461 | `962a2f02a08b5aed201b3f5b2aed78f183d2f090b9c9b75dfe5a3d4fcd90bdbc` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/model/Zip318Kind.kt | 2079 | `4ab35d5506d38cff129994b5e9f07bb194eb51a971b863adc1eac78d307a783c` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/model/Zip32AccountIndex.kt | 558 | `00aea12278ca7a4ce4d72f069318bf82a70280668b6cc255460a60f14b2c2c8d` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/model/voting/VotingModels.kt | 17280 | `8665a5117a282e9fe754516ec93b2dc143f2a52e3d12609908a74949e503aab6` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/tool/CheckpointTool.kt | 12623 | `d3fc4ad8378f2065e3ad4e1fbc82c15779cc5ce09c5ac6bc08433ceb9a031ae1` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/tool/DerivationTool.kt | 6701 | `328f4d6a59432fd7ab0742c33b63aca8627086b376b4784def114468090a53ac` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/type/AddressType.kt | 1305 | `2fe46fdd9c496943c3ebb4cf2306fc39a19c4c1dc7a3990d970159fbdead7f41` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/type/ConsensusMatchType.kt | 2272 | `8abfbe498b521c2b255ca4be7108cb150871be4b0fd723c7214177d8b695e93e` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/type/ServerValidation.kt | 328 | `6f0bb359aa8c6b709423b48348b6a0b1f682cc0ac868b95b10d41b9a4172b86e` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/type/WalletTypes.kt | 324 | `024b322b920107bdcde5e3b83f86fe6ebda28a7df73338789cb78991b996a87f` | 0 |
| sdk-lib/src/main/java/cash/z/ecc/android/sdk/util/WalletClientFactory.kt | 1604 | `d2ccdcd1f2bcd3047c374625474b3537bf854d3f48bc8f950e64089a80e00c97` | 0 |
| sdk-lib/src/release/java/cash/z/ecc/android/sdk/annotation/OpenForTesting.kt | 579 | `7411e0ad18d1946c30823762ba8891c0254f0e3a2fb1b0039ef94b88925f7496` | 0 |
| settings.gradle.kts | 16977 | `55e67069d951e3d1ddd39cf66c50363096f8f7b12a1a78c4bec8a6898917800b` | 0 |
