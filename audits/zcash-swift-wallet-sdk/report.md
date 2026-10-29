# Security & Post-Quantum Readiness Audit Report

**Project:** zcash-swift-wallet-sdk @ 4895ee058da9 · Electric Coin Company (Zcash) — public repository (passive review)
| | |
|---|---|
| Organization | QSI |
| Report date | 2026-10-28 13:03 UTC |
| Report version | 1 |
| Audit run | 92a48a9c-2953-4dff-9139-91cd1aa708d4 (Document audit) |
| Analyzer engine | qsi-engine 1.2.0 |
| Risk profile | Small technology company |
| Content SHA-256 | `3f9395ecdc760e1d1fbe874a5b0e9954a776e0a678451db32e9a30253ad81a7f` |
| Signature key (Ed25519, SHA-256 fingerprint; the signature is the separate file report.sig.json) | `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e` |
> This report presents automated and documented analysis results for the stated scope. It is not a legal opinion, a certification or an attestation of compliance with any standard.

## 1. Executive summary

- Critical: **0**
- High: **0**
- Medium: **7**
- Low: **21**
- Info: **4**

- Confirmed technical vulnerability: 0
- Known vulnerable component: 27
- Confirmed configuration error: 0
- Potential cryptographic risk: 0
- Long-term post-quantum risk: 1
- Improvement recommendation: 3
- Insufficient data: 1

Mosca's inequality (x + y > z): x = 5, y = 3, z = 12 → time available under this scenario. _z is a planning assumption chosen per risk profile, not a prediction. A cryptographically relevant quantum computer is not publicly known to exist today._

**Post-quantum maturity: Level 0 of 4 — no post-quantum cryptography.** Next step: Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

## 2. Scope and boundaries

Mode: Document audit

Repository: <https://github.com/zcash/zcash-swift-wallet-sdk> @ `4895ee058da99971057cceb80f36b8909656a8a9` — evidence links open the lines at this commit.

205 files, 3130631 bytes in total, 0 redaction(s); the per-file SHA-256 list is in appendix C.

## 3. Methodology

| Area | Status | Count | Examples |
|---|---|---|---|
| source_code | checked | 198 | .claude/skills/update-checkpoints/scripts/checkmate.py: 73 lines scanned with 16 rule patterns and 122 registry patterns; .claude/skills/update-checkpoints/scripts/fetch_checkpoints.py: 164 lines scanned with 16 rule patterns and 122 registry patterns; .claude/skills/update-checkpoints/scripts/verify_checkpoints.py: 199 lines scanned with 16 rule patterns and 122 registry patterns |
| dependencies | checked | 3 | Cargo.lock: 679 dependencies parsed (679 pinned); Cargo.toml: 57 dependencies parsed (1 pinned); Package.resolved: 21 dependencies parsed (21 pinned) |
| certificates_and_keys | checked | 1 | responsible_disclosure.md: certificates/keys parsed |
| osv_advisories | checked | 1 | 679 pinned packages queried at OSV.dev; 16 affected |

_Long lists are grouped here; the full per-file list is in the JSON report, signed with the same key._

## 4. Assets examined and not examined

- None

## 5. Architecture overview

Static review of the source tree zcash-swift-wallet-sdk at 4895ee058da99971057cceb80f36b8909656a8a9. 205 files analysed; of 1623 files, 178 are test, fuzzing, benchmark or example code and were left out, 1240 are not read by any analyzer, 0 exceed the per-file limit and 0 did not fit the total limit. No requests were sent to the owner's systems.

## 6. Overall security posture

- Indicative posture index: **48** / 100 — _Derived from findings in scope (confirmed and potential issues weighted by severity). Indicative only; not comparable across differently scoped audits._
- Quantum-vulnerable share of inventory: 16.7%

## 7. Detailed findings

### QSI-2026-05216 — block-buffer 0.10.4 is affected by GHSA-qwgh-2vcv-g2f7

- Severity: **Medium** · Classification: Known vulnerable component · Confidence: Low
- Affected asset: `dependency:crates.io/block-buffer@0.10.4`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 13:03 UTC
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

### QSI-2026-05217 — block-buffer 0.11.0-rc.3 is affected by GHSA-qwgh-2vcv-g2f7

- Severity: **Medium** · Classification: Known vulnerable component · Confidence: Low
- Affected asset: `dependency:crates.io/block-buffer@0.11.0-rc.3`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 13:03 UTC
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

### QSI-2026-05222 — rsa 0.9.10 is affected by RUSTSEC-2023-0071 (CVE-2023-49092)

- Severity: **Medium** · Classification: Known vulnerable component · Confidence: Low
- Affected asset: `dependency:crates.io/rsa@0.9.10`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 13:03 UTC
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

### QSI-2026-05223 — rustls 0.23.42 is affected by GHSA-2mjx-qc3c-rqvc (RUSTSEC-2026-0285)

- Severity: **Medium** · Classification: Known vulnerable component · Confidence: Low
- Affected asset: `dependency:crates.io/rustls@0.23.42`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 13:03 UTC
- Priority score: 33.1 / 100
- CVSS v3.1: 5.3 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N`)

OSV.dev reports GHSA-2mjx-qc3c-rqvc (RUSTSEC-2026-0285) for crates.io package rustls at version 0.23.42: Rustls: TLS 1.3 handshake messages incorrectly accepted across encryption level boundaries. The advisory names no affected functions, so reachability was not determined.

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

### QSI-2026-05224 — rustls 0.23.42 is affected by GHSA-c8m5-c952-6cm4 (RUSTSEC-2026-0346)

- Severity: **Medium** · Classification: Known vulnerable component · Confidence: Low
- Affected asset: `dependency:crates.io/rustls@0.23.42`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 13:03 UTC
- Priority score: 33.1 / 100
- CVSS v3.1: 4.0 (`CVSS:3.1/AV:L/AC:H/PR:H/UI:R/S:U/C:H/I:N/A:N`)

OSV.dev reports GHSA-c8m5-c952-6cm4 (RUSTSEC-2026-0346) for crates.io package rustls at version 0.23.42: Rustls: Session Debug formatting exposes TLS master secrets and resumption PSKs. The advisory names no affected functions, so reachability was not determined.

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

### QSI-2026-05227 — serde_with 3.17.0 is affected by GHSA-7gcf-g7xr-8hxj

- Severity: **Medium** · Classification: Known vulnerable component · Confidence: Low
- Affected asset: `dependency:crates.io/serde_with@3.17.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 13:03 UTC
- Priority score: 33.1 / 100
- CVSS v3.1: not applicable

OSV.dev reports GHSA-7gcf-g7xr-8hxj for crates.io package serde_with at version 3.17.0: serde_with: KeyValueMap serialization panics on empty sequence or map entries. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-7gcf-g7xr-8hxj
```

**Evidence.**

_tool_output · [OSV.dev GHSA-7gcf-g7xr-8hxj](https://osv.dev/vulnerability/GHSA-7gcf-g7xr-8hxj) · manifest · SHA-256 9a6efbdf7670d9ead9898fb39da9d141ceec2380712ba7d56de6b7ec07c98051_

```
{"id": "GHSA-7gcf-g7xr-8hxj", "aliases": [], "modified": "2026-09-10T03:51:10.897685062Z", "summary": "serde_with: KeyValueMap serialization panics on empty sequence or map entries", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (3.21.0).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-05228 — time 0.3.37 is affected by GHSA-r6v5-fh4h-64xc (CVE-2026-25727, RUSTSEC-2026-0009)

- Severity: **Medium** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/time@0.3.37`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 13:03 UTC
- Priority score: 28.1 / 100
- CVSS v3.1: not applicable

OSV.dev reports GHSA-r6v5-fh4h-64xc (CVE-2026-25727, RUSTSEC-2026-0009) for crates.io package time at version 0.3.37: time vulnerable to stack exhaustion Denial of Service attack. The audited code does not name the affected functions (time::Date::parse, time::OffsetDateTime::parse, time::PrimitiveDateTime::parse, time::Time::parse, time::UtcDateTime::parse, time::UtcOffset::parse …); time comes in through other dependencies, which may still call them.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-r6v5-fh4h-64xc
```

**Evidence.**

_tool_output · [OSV.dev GHSA-r6v5-fh4h-64xc](https://osv.dev/vulnerability/GHSA-r6v5-fh4h-64xc) · manifest · SHA-256 47bed44226c6f8f5c94bfd27c3dd67ade62aa708c5d61bcca37c2b8bbe9b577d_

```
{"id": "GHSA-r6v5-fh4h-64xc", "aliases": ["CVE-2026-25727", "RUSTSEC-2026-0009"], "modified": "2026-09-10T03:50:35.583241382Z", "summary": "time vulnerable to stack exhaustion Denial of Service attack", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:H/AT:N/PR:L/UI:A/VC:N/VI:N/VA:H/SC:N/SI:N/SA:H"}], "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (0.3.47).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-05212 — Quantum-vulnerable RSA key (2048-bit) in responsible_disclosure.md

- Severity: **Low** · Classification: Long-term post-quantum risk · Confidence: High
- Affected asset: `file:responsible_disclosure.md#line 11`
- Data source: responsible_disclosure.md
- Detection method: Public key parsing.
- Analyzer: certificates 1.2.0 · 2026-10-28 13:03 UTC
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

### QSI-2026-05226 — rustls 0.23.42 is affected by GHSA-w44r-93j7-qv28 (RUSTSEC-2026-0349)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low
- Affected asset: `dependency:crates.io/rustls@0.23.42`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 13:03 UTC
- Priority score: 28.6 / 100
- CVSS v3.1: 3.7 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N`)

OSV.dev reports GHSA-w44r-93j7-qv28 (RUSTSEC-2026-0349) for crates.io package rustls at version 0.23.42: rustls: An unauthenticated ServerHello poisons the per-name key-exchange record, so later ClientHellos carry only a classical X25519 share. The advisory names no affected functions, so reachability was not determined.

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

### QSI-2026-05225 — rustls 0.23.42 is affected by GHSA-h2v8-394m-p7vv (RUSTSEC-2026-0348)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/rustls@0.23.42`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 13:03 UTC
- Priority score: 24.3 / 100
- CVSS v3.1: 3.7 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:N/A:L`)

OSV.dev reports GHSA-h2v8-394m-p7vv (RUSTSEC-2026-0348) for crates.io package rustls at version 0.23.42: Rustls: Brotli certificate decompression can allocate an attacker-controlled amount of memory up to 1 GiB before authentication. The affected code sits behind the `brotli` Cargo feature, off by default, which no audited manifest enables: the advisory does not apply unless another dependency enables it.

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

### QSI-2026-05218 — crypto-bigint 0.5.5 is affected by RUSTSEC-2026-0387 (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/crypto-bigint@0.5.5`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 13:03 UTC
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

### QSI-2026-05219 — event-listener 5.4.1 is affected by RUSTSEC-2026-0221 (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/event-listener@5.4.1`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 13:03 UTC
- Priority score: 20.2 / 100
- CVSS v3.1: not applicable

OSV.dev reports RUSTSEC-2026-0221 for crates.io package event-listener at version 5.4.1: `event-listener` allows `!Send` tags to cross thread boundaries via `StackSlot`. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0221
```

**Evidence.**

_tool_output · [OSV.dev RUSTSEC-2026-0221](https://osv.dev/vulnerability/RUSTSEC-2026-0221) · manifest · SHA-256 984b4e4e87b4e2cc5992a06daf6b6466ee08279d927a38dca105b75fa8546f7c_

```
{"id": "RUSTSEC-2026-0221", "aliases": [], "modified": "2026-07-31T12:15:04.629484145Z", "summary": "`event-listener` allows `!Send` tags to cross thread boundaries via `StackSlot`", "severity": null, "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Triage the advisory; upgrade to a fixed version (5.4.2) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-05220 — h2 0.4.15 is affected by RUSTSEC-2026-0258 (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/h2@0.4.15`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 13:03 UTC
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

### QSI-2026-05229 — tokio 1.53.1 is affected by RUSTSEC-2026-0386 (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/tokio@1.53.1`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 13:03 UTC
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

### QSI-2026-05230 — zstd 0.13.3 is affected by RUSTSEC-2026-0391 (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/zstd@0.13.3`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 13:03 UTC
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

### QSI-2026-05231 — zstd-safe 7.2.4 is affected by RUSTSEC-2026-0395 (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/zstd-safe@7.2.4`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 13:03 UTC
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

### QSI-2026-05232 — zstd-safe 7.2.4 is affected by RUSTSEC-2026-0396 (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/zstd-safe@7.2.4`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 13:03 UTC
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

### QSI-2026-05233 — zstd-safe 7.2.4 is affected by RUSTSEC-2026-0397 (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/zstd-safe@7.2.4`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 13:03 UTC
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

### QSI-2026-05234 — zstd-safe 7.2.4 is affected by RUSTSEC-2026-0398 (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/zstd-safe@7.2.4`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 13:03 UTC
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

### QSI-2026-05235 — zstd-safe 7.2.4 is affected by RUSTSEC-2026-0399 (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/zstd-safe@7.2.4`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 13:03 UTC
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

### QSI-2026-05236 — zstd-safe 7.2.4 is affected by RUSTSEC-2026-0400 (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/zstd-safe@7.2.4`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 13:03 UTC
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

### QSI-2026-05237 — zstd-safe 7.2.4 is affected by RUSTSEC-2026-0401 (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/zstd-safe@7.2.4`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 13:03 UTC
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

### QSI-2026-05238 — zstd-safe 7.2.4 is affected by RUSTSEC-2026-0402 (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/zstd-safe@7.2.4`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 13:03 UTC
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

### QSI-2026-05239 — zstd-safe 7.2.4 is affected by RUSTSEC-2026-0403 (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/zstd-safe@7.2.4`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 13:03 UTC
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

### QSI-2026-05240 — zstd-safe 7.2.4 is affected by RUSTSEC-2026-0404 (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/zstd-safe@7.2.4`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 13:03 UTC
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

### QSI-2026-05241 — zstd-safe 7.2.4 is affected by RUSTSEC-2026-0405 (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/zstd-safe@7.2.4`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 13:03 UTC
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

### QSI-2026-05242 — zstd-safe 7.2.4 is affected by RUSTSEC-2026-0406 (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/zstd-safe@7.2.4`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 13:03 UTC
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

### QSI-2026-05243 — zstd-sys 2.0.16+zstd.1.5.7 is affected by RUSTSEC-2026-0410 (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/zstd-sys@2.0.16+zstd.1.5.7`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 13:03 UTC
- Priority score: 20.2 / 100
- CVSS v3.1: not applicable

OSV.dev reports RUSTSEC-2026-0410 for crates.io package zstd-sys at version 2.0.16+zstd.1.5.7: WebAssembly allocator shim corrupts memory on allocation failure. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. The advisory names no affected functions, so reachability was not determined. It affects only wasm32 targets.

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

### QSI-2026-05213 — No post-quantum capable cryptographic library detected

- Severity: **Info** · Classification: Insufficient data · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `dependencies`
- Data source: dependency manifests
- Detection method: Dependency name matching.
- Analyzer: dependencies 1.2.0 · 2026-10-28 13:03 UTC
- Priority score: 13.4 / 100
- CVSS v3.1: not applicable

Across 3 dependency manifests, QSI found crypto libraries (curve25519-dalek, ecdsa, ed25519-dalek, p256, p384, ring, rsa, rustls, secp256k1, x25519-dalek) but none from its PQC-capable list.

**Potential impact.** Readiness indicator only: PQC support may come from the platform (OpenSSL, OS, cloud KMS) rather than application dependencies.

**Reproduction steps.**

```
Review the dependency manifests listed in the evidence.
```

**Evidence.**

_dependency · Cargo.lock, Cargo.toml, Package.resolved · SHA-256 afaf41cc18f45737a6066d3670aa5870ee2ce9f1e082d771b281af998ce72df3_

```
Crypto libraries: curve25519-dalek, ecdsa, ed25519-dalek, p256, p384, ring, rsa, rustls, secp256k1, x25519-dalek
```

**Limitations of the check.** Absence of evidence is not evidence of absence: system libraries and transitive dependencies may not be listed.

**Recommendation.** Confirm where PQC support will come from (TLS terminator, KMS/HSM, library upgrade).

**Retest procedure.** Re-scan after upgrades.

### QSI-2026-05214 — atomic-polyfill 1.0.3: informational advisory RUSTSEC-2023-0089 (unmaintained)

- Severity: **Info** · Classification: Improvement recommendation · Confidence: Low
- Affected asset: `dependency:crates.io/atomic-polyfill@1.0.3`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 13:03 UTC
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

### QSI-2026-05215 — bincode 2.0.1: informational advisory RUSTSEC-2025-0141 (unmaintained)

- Severity: **Info** · Classification: Improvement recommendation · Confidence: Low
- Affected asset: `dependency:crates.io/bincode@2.0.1`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 13:03 UTC
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

### QSI-2026-05221 — paste 1.0.15: informational advisory RUSTSEC-2024-0436 (unmaintained)

- Severity: **Info** · Classification: Improvement recommendation · Confidence: Low
- Affected asset: `dependency:crates.io/paste@1.0.15`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 13:03 UTC
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

_Effects: breaks — replace the algorithm; weakens — larger keys or outputs restore the margin; included in standard parameters — no action at standard parameter sets; only with superposition queries — not applicable to ordinary deployments._


## 9. Limitations and assumptions

- This report presents automated and documented analysis results for the stated scope. It is not a legal opinion, a certification or an attestation of compliance with any standard.
- z is a planning assumption chosen per risk profile, not a prediction. A cryptographically relevant quantum computer is not publicly known to exist today.

## 10. Remediation plan / Priorities for 30, 60 and 90 days

### 30 days

| Priority | ID | Action | Type | Closure criteria |
|---|---|---|---|---|
| P2 | QSI-2026-05216 | Upgrade block-buffer to a fixed version (none published yet; see the advisory for mitigations). | root-cause fix | Dependency scan no longer reports GHSA-qwgh-2vcv-g2f7. |
| P2 | QSI-2026-05217 | Upgrade block-buffer to a fixed version (none published yet; see the advisory for mitigations). | root-cause fix | Dependency scan no longer reports GHSA-qwgh-2vcv-g2f7. |
| P2 | QSI-2026-05222 | Upgrade rsa to a fixed version (none published yet; see the advisory for mitigations). | root-cause fix | Dependency scan no longer reports RUSTSEC-2023-0071 (CVE-2023-49092). |
| P2 | QSI-2026-05223 | Upgrade rustls to a fixed version (0.23.45). | root-cause fix | Dependency scan no longer reports GHSA-2mjx-qc3c-rqvc (RUSTSEC-2026-0285). |
| P2 | QSI-2026-05224 | Upgrade rustls to a fixed version (0.23.46, 0.24.0-dev.2). | root-cause fix | Dependency scan no longer reports GHSA-c8m5-c952-6cm4 (RUSTSEC-2026-0346). |
| P2 | QSI-2026-05227 | Upgrade serde_with to a fixed version (3.21.0). | root-cause fix | Dependency scan no longer reports GHSA-7gcf-g7xr-8hxj. |
| P2 | QSI-2026-05228 | Upgrade time to a fixed version (0.3.47). | root-cause fix | Dependency scan no longer reports GHSA-r6v5-fh4h-64xc (CVE-2026-25727, RUSTSEC-2026-0009). |
| P2 | QSI-2026-05226 | Upgrade rustls to a fixed version (0.23.46, 0.24.0-dev.2). | root-cause fix | Dependency scan no longer reports GHSA-w44r-93j7-qv28 (RUSTSEC-2026-0349). |
| P2 | QSI-2026-05225 | Upgrade rustls to a fixed version (0.23.46, 0.24.0-dev.2). | root-cause fix | Dependency scan no longer reports GHSA-h2v8-394m-p7vv (RUSTSEC-2026-0348). |
### 60 days

| Priority | ID | Action | Type | Closure criteria |
|---|---|---|---|---|
| P3 | QSI-2026-05218 | Triage RUSTSEC-2026-0387; upgrade crypto-bigint to a fixed version (0.7.6) if it applies. | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0387, or the triage is recorded. |
| P3 | QSI-2026-05219 | Triage RUSTSEC-2026-0221; upgrade event-listener to a fixed version (5.4.2) if it applies. | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0221, or the triage is recorded. |
| P3 | QSI-2026-05220 | Triage RUSTSEC-2026-0258; upgrade h2 to a fixed version (0.4.16) if it applies. | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0258, or the triage is recorded. |
| P3 | QSI-2026-05229 | Triage RUSTSEC-2026-0386; upgrade tokio to a fixed version (1.51.6, 1.53.3) if it applies. | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0386, or the triage is recorded. |
| P3 | QSI-2026-05230 | Triage RUSTSEC-2026-0391; upgrade zstd to a fixed version (0.14.3) if it applies. | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0391, or the triage is recorded. |
| P3 | QSI-2026-05231 | Triage RUSTSEC-2026-0395; upgrade zstd-safe to a fixed version (8.2.0) if it applies. | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0395, or the triage is recorded. |
| P3 | QSI-2026-05232 | Triage RUSTSEC-2026-0396; upgrade zstd-safe to a fixed version (8.2.0) if it applies. | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0396, or the triage is recorded. |
| P3 | QSI-2026-05233 | Triage RUSTSEC-2026-0397; upgrade zstd-safe to a fixed version (8.2.0) if it applies. | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0397, or the triage is recorded. |
| P3 | QSI-2026-05234 | Triage RUSTSEC-2026-0398; upgrade zstd-safe to a fixed version (8.2.0) if it applies. | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0398, or the triage is recorded. |
| P3 | QSI-2026-05235 | Triage RUSTSEC-2026-0399; upgrade zstd-safe to a fixed version (8.2.0) if it applies. | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0399, or the triage is recorded. |
| P3 | QSI-2026-05236 | Triage RUSTSEC-2026-0400; upgrade zstd-safe to a fixed version (8.2.0) if it applies. | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0400, or the triage is recorded. |
| P3 | QSI-2026-05237 | Triage RUSTSEC-2026-0401; upgrade zstd-safe to a fixed version (8.2.0) if it applies. | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0401, or the triage is recorded. |
| P3 | QSI-2026-05238 | Triage RUSTSEC-2026-0402; upgrade zstd-safe to a fixed version (8.2.0) if it applies. | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0402, or the triage is recorded. |
| P3 | QSI-2026-05239 | Triage RUSTSEC-2026-0403; upgrade zstd-safe to a fixed version (8.2.0) if it applies. | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0403, or the triage is recorded. |
| P3 | QSI-2026-05240 | Triage RUSTSEC-2026-0404; upgrade zstd-safe to a fixed version (8.2.0) if it applies. | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0404, or the triage is recorded. |
| P3 | QSI-2026-05241 | Triage RUSTSEC-2026-0405; upgrade zstd-safe to a fixed version (8.2.0) if it applies. | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0405, or the triage is recorded. |
| P3 | QSI-2026-05242 | Triage RUSTSEC-2026-0406; upgrade zstd-safe to a fixed version (8.2.0) if it applies. | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0406, or the triage is recorded. |
| P3 | QSI-2026-05243 | Triage RUSTSEC-2026-0410; upgrade zstd-sys to a fixed version (2.1.2) if it applies. | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0410, or the triage is recorded. |
### 90 days

| Priority | ID | Action | Type | Closure criteria |
|---|---|---|---|---|
| P3 | QSI-2026-05212 | Add RSA usages at file:responsible_disclosure.md to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P4 | QSI-2026-05212 | Plan migration of RSA to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. or a hybrid scheme in use. |
| P4 | QSI-2026-05214 | Replace atomic-polyfill with a maintained alternative or record why it stays. | root-cause fix | atomic-polyfill replaced, or the decision recorded. |
| P4 | QSI-2026-05215 | Replace bincode with a maintained alternative or record why it stays. | root-cause fix | bincode replaced, or the decision recorded. |
| P4 | QSI-2026-05221 | Replace paste with a maintained alternative or record why it stays. | root-cause fix | paste replaced, or the decision recorded. |

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

1. C. Gidney — How to factor 2048 bit RSA integers with less than a million noisy qubits (arXiv:2505.15917) — arXiv. <https://arxiv.org/abs/2505.15917> (preprint (2025-05-21): < 1 million noisy qubits, < 1 week, 0.1% gate error, 1 µs surface-code cycle)
2. C. Gidney, M. Ekerå — How to factor 2048 bit RSA integers in 8 hours using 20 million noisy qubits (Quantum 5, 433) — Quantum. <https://doi.org/10.22331/q-2021-04-15-433> (peer-reviewed article (2021): 10^-3 gate error, 1 µs cycle, 10 µs reaction time)
3. Common Vulnerability Scoring System v3.1: Specification Document — FIRST. <https://www.first.org/cvss/v3.1/specification-document> (final)
4. FIPS 203 — Module-Lattice-Based Key-Encapsulation Mechanism Standard (ML-KEM) — NIST. <https://csrc.nist.gov/pubs/fips/203/final> (final (August 2024))
5. FIPS 204 — Module-Lattice-Based Digital Signature Standard (ML-DSA) — NIST. <https://csrc.nist.gov/pubs/fips/204/final> (final (August 2024))
6. FIPS 205 — Stateless Hash-Based Digital Signature Standard (SLH-DSA) — NIST. <https://csrc.nist.gov/pubs/fips/205/final> (final (August 2024))
7. M. Cain et al. — Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits (arXiv:2603.28627) — arXiv. <https://arxiv.org/abs/2603.28627> (preprint (2026-03-30): P-256 in a few days with 26,000 physical neutral-atom qubits; RSA-2048 one to two orders of magnitude longer)
8. M. Mosca — Cybersecurity in an Era with Quantum Computers: Will We Be Ready? (IEEE Security & Privacy, 2018) — IEEE. <https://doi.org/10.1109/MSP.2018.3761723> (peer-reviewed article; source of the x + y > z migration inequality)
9. NIST IR 8547 — Transition to Post-Quantum Cryptography Standards — NIST. <https://csrc.nist.gov/pubs/ir/8547/ipd> (initial public draft (November 2024); proposes deprecating quantum-vulnerable public-key algorithms after 2030 and disallowing them after 2035 — dates may change in the final version)
10. OSV advisory GHSA-2mjx-qc3c-rqvc — OSV.dev. <https://osv.dev/vulnerability/GHSA-2mjx-qc3c-rqvc> (modified 2026-10-27T15:30:05.509305490Z)
11. OSV advisory GHSA-7gcf-g7xr-8hxj — OSV.dev. <https://osv.dev/vulnerability/GHSA-7gcf-g7xr-8hxj> (modified 2026-09-10T03:51:10.897685062Z)
12. OSV advisory GHSA-c8m5-c952-6cm4 — OSV.dev. <https://osv.dev/vulnerability/GHSA-c8m5-c952-6cm4> (modified 2026-10-27T16:15:05.354395696Z)
13. OSV advisory GHSA-h2v8-394m-p7vv — OSV.dev. <https://osv.dev/vulnerability/GHSA-h2v8-394m-p7vv> (modified 2026-10-27T16:15:05.337819489Z)
14. OSV advisory GHSA-qwgh-2vcv-g2f7 — OSV.dev. <https://osv.dev/vulnerability/GHSA-qwgh-2vcv-g2f7> (modified 2026-08-19T19:30:06.686866977Z)
15. OSV advisory GHSA-r6v5-fh4h-64xc — OSV.dev. <https://osv.dev/vulnerability/GHSA-r6v5-fh4h-64xc> (modified 2026-09-10T03:50:35.583241382Z)
16. OSV advisory GHSA-w44r-93j7-qv28 — OSV.dev. <https://osv.dev/vulnerability/GHSA-w44r-93j7-qv28> (modified 2026-10-27T16:15:05.340347056Z)
17. OSV advisory RUSTSEC-2023-0071 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2023-0071> (modified 2026-09-14T09:45:02.996132556Z)
18. OSV advisory RUSTSEC-2023-0089 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2023-0089> (modified 2025-04-29T08:31:10Z)
19. OSV advisory RUSTSEC-2024-0436 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2024-0436> (modified 2026-01-27T22:03:15.694766Z)
20. OSV advisory RUSTSEC-2025-0141 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2025-0141> (modified 2026-01-16T11:07:28.867553Z)
21. OSV advisory RUSTSEC-2026-0221 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0221> (modified 2026-07-31T12:15:04.629484145Z)
22. OSV advisory RUSTSEC-2026-0258 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0258> (modified 2026-10-12T18:00:10.934581734Z)
23. OSV advisory RUSTSEC-2026-0386 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0386> (modified 2026-10-23T14:45:03.847864944Z)
24. OSV advisory RUSTSEC-2026-0387 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0387> (modified 2026-10-24T03:45:02.365137418Z)
25. OSV advisory RUSTSEC-2026-0391 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0391> (modified 2026-10-26T14:00:04.269245609Z)
26. OSV advisory RUSTSEC-2026-0395 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0395> (modified 2026-10-26T14:00:06.388344282Z)
27. OSV advisory RUSTSEC-2026-0396 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0396> (modified 2026-10-26T14:00:05.789682118Z)
28. OSV advisory RUSTSEC-2026-0397 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0397> (modified 2026-10-26T14:00:05.089587004Z)
29. OSV advisory RUSTSEC-2026-0398 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0398> (modified 2026-10-26T14:00:05.092082939Z)
30. OSV advisory RUSTSEC-2026-0399 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0399> (modified 2026-10-26T14:00:05.792431051Z)
31. OSV advisory RUSTSEC-2026-0400 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0400> (modified 2026-10-26T14:00:05.692077560Z)
32. OSV advisory RUSTSEC-2026-0401 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0401> (modified 2026-10-26T14:00:04.231502512Z)
33. OSV advisory RUSTSEC-2026-0402 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0402> (modified 2026-10-26T14:00:05.685817733Z)
34. OSV advisory RUSTSEC-2026-0403 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0403> (modified 2026-10-26T14:00:05.787441176Z)
35. OSV advisory RUSTSEC-2026-0404 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0404> (modified 2026-10-26T14:00:05.092817237Z)
36. OSV advisory RUSTSEC-2026-0405 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0405> (modified 2026-10-26T14:00:05.680942523Z)
37. OSV advisory RUSTSEC-2026-0406 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0406> (modified 2026-10-26T14:00:05.095427051Z)
38. OSV advisory RUSTSEC-2026-0410 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0410> (modified 2026-10-26T14:00:05.788985783Z)
39. P. W. Shor — Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms on a Quantum Computer (SIAM J. Comput., 1997) — SIAM. <https://doi.org/10.1137/S0097539795293172> (peer-reviewed article)

## Appendices: Cryptographic inventory

| Algorithm | Parameter | Library | Location | Quantum status | Classical status |
|---|---|---|---|---|---|
| Crypto library | 0.13.1 | p384 (RustCrypto elliptic curves) | Cargo.lock | n/a | acceptable |
| Crypto library | 0.13.2 | p256 (RustCrypto elliptic curves) | Cargo.lock | n/a | acceptable |
| Crypto library | 0.16.9 | ecdsa (python-ecdsa) | Cargo.lock | n/a | acceptable |
| Crypto library | 0.17.14 | ring (ring (Rust)) | Cargo.lock | n/a | acceptable |
| Crypto library | 0.23.42 | rustls (rustls) | Cargo.lock | n/a | acceptable |
| Crypto library | 0.29.1 | secp256k1 (secp256k1 bindings) | Cargo.lock | n/a | acceptable |
| Crypto library | 0.9.10 | rsa (RustCrypto rsa) | Cargo.lock | n/a | acceptable |
| Crypto library | 2.0.1 | x25519-dalek (ed25519-dalek) | Cargo.lock | n/a | acceptable |
| Crypto library | 2.2.0 | ed25519-dalek (ed25519-dalek) | Cargo.lock | n/a | acceptable |
| Crypto library | 4.1.3 | curve25519-dalek (ed25519-dalek) | Cargo.lock | n/a | acceptable |
| RSA | 2048-bit |  | responsible_disclosure.md (line 11) | vulnerable (Shor) | acceptable |
| RSA | 2048-bit |  | responsible_disclosure.md (line 11) | vulnerable (Shor) | acceptable |

## Appendices: Input files

| File | Size | SHA-256 | Redactions |
|---|---|---|---|
| .claude/skills/update-checkpoints/scripts/checkmate.py | 2829 | `9064ba49433d036798a3ff0601c4a0a8ee6528abcd30de90412d76e818a33c94` | 0 |
| .claude/skills/update-checkpoints/scripts/fetch_checkpoints.py | 6046 | `b792994b0a8546d09b69d45b82512a8b8864b228e6a04fb7c420b0d3e694cd0c` | 0 |
| .claude/skills/update-checkpoints/scripts/verify_checkpoints.py | 7311 | `e01fa8090e45e71807fa82a4dd75939ed8d431749f0d57401cfa0f5880be1968` | 0 |
| BuildSupport/LocalPackages-Package.swift | 317 | `0e49f104f66bc8be8e6dabf0541c40b01eff03eaccc6644f5f7faac82b513198` | 0 |
| Cargo.lock | 182765 | `e887fa176f4fb05d93832601600c95f2734a5d33fd333e8f502953dc6652dbfb` | 0 |
| Cargo.toml | 5314 | `8c6d2e956f0fb11c0cadeb45a7260d1c9b126badea7765debabff425c7dbb746` | 0 |
| Package.resolved | 5862 | `af670ce8cfa12d4edce82ed22f18c4f427c1e8e6f1f8332d7bc711c2ac93ecbb` | 0 |
| Package.swift | 3662 | `207fe4fdcc59b524ee286eed72082220db145331446380eecfe8a1b0b0f5615f` | 0 |
| Sources/ZcashLightClientKit/Account/Account.swift | 1291 | `dd238a58214cbb697b9bb7cea1c28c239b216819fe5e0bf0b17e7da09ab031ff` | 0 |
| Sources/ZcashLightClientKit/Account/AccountMetadataKey.swift | 3632 | `30236e32cdd7b763ec3246801becd59cfb3602de4cf47e7c86570dc58cd5c61f` | 0 |
| Sources/ZcashLightClientKit/Block/Actions/Action.swift | 4128 | `aca74001ab99eb9f29aeec4ace6a4061f5480d2d8085846d8e163fc2efc89375` | 0 |
| Sources/ZcashLightClientKit/Block/Actions/ClearAlreadyScannedBlocksAction.swift | 1006 | `9c00b4075c953564abd514ed7da81c29518794c04eabfe0d76b16b7073a6467d` | 0 |
| Sources/ZcashLightClientKit/Block/Actions/ClearCacheAction.swift | 673 | `e282b20cda6c60da38ede4b3dd25fa18359cc324fcdf5fb12eb9c7a1e0f2e0f1` | 0 |
| Sources/ZcashLightClientKit/Block/Actions/DownloadAction.swift | 2670 | `35d8bb856313f2996e2cc012f3b6bdac87c7582ad575368d6f418c1d0dba8d54` | 0 |
| Sources/ZcashLightClientKit/Block/Actions/EnhanceAction.swift | 4219 | `ce8049f08dab0a7ae44d1980f435e3cef3aef33bcb55cc0e83a3f158d636fcbc` | 0 |
| Sources/ZcashLightClientKit/Block/Actions/FetchUTXOsAction.swift | 833 | `3ec4d2e5c866a705b8f8997e07e01a25049ac6788c2b35767b8f31cc671eb958` | 0 |
| Sources/ZcashLightClientKit/Block/Actions/MigrateLegacyCacheDBAction.swift | 2726 | `7884a9b9a68b8d2ea8cb1ecf706ee3e7dab14de0d242452e5592047b24643919` | 0 |
| Sources/ZcashLightClientKit/Block/Actions/ProcessSuggestedScanRangesAction.swift | 2479 | `326268a1e39a5cb9287f5b59d109b46b3da6309c2b2ab78c0d9ad3618a9dd615` | 0 |
| Sources/ZcashLightClientKit/Block/Actions/RewindAction.swift | 2082 | `3e61c61311854f75c0e44127fc9bcd89f112e1e9d98b79cc43eb747105249553` | 0 |
| Sources/ZcashLightClientKit/Block/Actions/SaplingParamsAction.swift | 861 | `767c1e82f7cd94f76d67d6e885f7ef6ec42fbde847a76de1fe2f37d4a2caacae` | 0 |
| Sources/ZcashLightClientKit/Block/Actions/ScanAction.swift | 5672 | `d19bb0070a28b9951e186f918d10fef4fb2084acb0b582d8be323bb00fc2a6c3` | 0 |
| Sources/ZcashLightClientKit/Block/Actions/TxResubmissionAction.swift | 1466 | `25af971034cd9b9180baab2b58ffffc7825d00c5e274280844b376de8180af95` | 0 |
| Sources/ZcashLightClientKit/Block/Actions/UpdateChainTipAction.swift | 2243 | `8ce2a04f7bc9209337cc5e90b4851bbed90f265005e34ad5c9726802657c4295` | 0 |
| Sources/ZcashLightClientKit/Block/Actions/UpdateSubtreeRootsAction.swift | 5904 | `b00e0a7f7f83e46fccdccf1facc0c4cff23f3046450eb5ef31ebf42aee3d9c23` | 0 |
| Sources/ZcashLightClientKit/Block/Actions/ValidateServerAction.swift | 4671 | `0d967779a6db14a40d3452fa43402108c5a375a90ee856d8e5619ea8b6466b05` | 0 |
| Sources/ZcashLightClientKit/Block/CompactBlockProcessor.swift | 39273 | `bec5308a69c1c8a66995f9355608dcf0622ffc8f95dc91c0da854245041533f1` | 0 |
| Sources/ZcashLightClientKit/Block/DatabaseStorage/ConnectorProvider.swift | 722 | `9eebb126d3d60afc091651d29b0152ab85a03e69bd37fffa3d8396607bef1532` | 0 |
| Sources/ZcashLightClientKit/Block/DatabaseStorage/DatabaseStorageError.swift | 455 | `20a3c91b11822600aeaab38a2bdccb1f69963b9cf5366ba8a1cd128cfe7460d2` | 0 |
| Sources/ZcashLightClientKit/Block/DatabaseStorage/SimpleConnectionProvider.swift | 3406 | `f44730872ecddecfa37ed153692ff87b0f3d873ee173abbca7f304bf3a7b556f` | 0 |
| Sources/ZcashLightClientKit/Block/Download/BlockDownloader.swift | 11889 | `37bc2503c65ca380198c0df1a73f44d759acacf99813277eb016f4a309db0b93` | 0 |
| Sources/ZcashLightClientKit/Block/Download/BlockDownloaderService.swift | 4482 | `c3eca659f8fd2881f4ae8e1dace0308491d23e03df8662a6b13b960877d7cb45` | 0 |
| Sources/ZcashLightClientKit/Block/Enhance/BlockEnhancer.swift | 13436 | `1a57e784a044c8653432ff9aacb4b1c0ea63c3a41c8f6f7fd630d431ea553182` | 0 |
| Sources/ZcashLightClientKit/Block/FetchUnspentTxOutputs/UTXOFetcher.swift | 2834 | `b3ce6a778fca90b6cc94812e7f98f9d4575dfb99b434e1e4301d35656402fcc7` | 0 |
| Sources/ZcashLightClientKit/Block/FilesystemStorage/FSCompactBlockRepository.swift | 15448 | `aa13e8916038b152884a54ff33432c1658e9abf1d11d3eadddaa8b8e1dc8fd34` | 0 |
| Sources/ZcashLightClientKit/Block/SaplingParameters/SaplingParametersHandler.swift | 2444 | `52a6c08e9e3499f32dd9b47a693d8a08f959a1fb19513b14e3650557651246c7` | 0 |
| Sources/ZcashLightClientKit/Block/Scan/BlockScanner.swift | 3062 | `5a576ac007cc4c2078108c656ad9cc5f12311028bbc2035a931d9981569d373b` | 0 |
| Sources/ZcashLightClientKit/Block/Utils/AfterSyncHooksManager.swift | 2160 | `fd2c477acb8ec000c6a8155ccc7bd297016b42f8c13636cd08a12e2b045b7fb8` | 0 |
| Sources/ZcashLightClientKit/Block/Utils/CompactBlockProgress.swift | 559 | `42cd85a623286ec50fde3f3b336ad8cda68bd568196f80df46283417e9e909c7` | 0 |
| Sources/ZcashLightClientKit/Block/Utils/SyncControlData.swift | 589 | `97dc49f6395bd7e45fb1dac95523e4ce00f27434ff45505d073d3c329294d54a` | 0 |
| Sources/ZcashLightClientKit/Broadcaster.swift | 8934 | `a9c90d36349069aedc6c09bb25ccdf316493722af5733c9bd9326bd6eadfd628` | 0 |
| Sources/ZcashLightClientKit/Checkpoint/BundleCheckpointSource.swift | 6147 | `27a20b0f64d8593bdec27b9dc950719398d96c3a8cc66d35fa6d38601d7cb883` | 0 |
| Sources/ZcashLightClientKit/Checkpoint/BundleCheckpointURLProvider.swift | 2238 | `05b5054d777b197ceb3b49e0a216e9e1e10b793aebdf8345a5ecbb64e4f9e298` | 0 |
| Sources/ZcashLightClientKit/Checkpoint/Checkpoint+helpers.swift | 2464 | `0e1ae9a2bb15dc21b09f7611b81d7b2b174634c8a8a1245f2b53c94e1ca7a620` | 0 |
| Sources/ZcashLightClientKit/Checkpoint/Checkpoint.swift | 4876 | `60be32515d02262ca1b665ad0b57bede6baaef4a1e07971aaa1ce7107cafc8b1` | 0 |
| Sources/ZcashLightClientKit/Checkpoint/CheckpointSource.swift | 1828 | `e8c7c6798447da3f494a1aa80a87e042ae7e79ea2ad4b29f64b449f054132919` | 0 |
| Sources/ZcashLightClientKit/Checkpoint/CheckpointSourceFactory.swift | 818 | `84ca45d590c041ab71e38eba66e9d01c9db90aebf4837838cae9a414d5949543` | 0 |
| Sources/ZcashLightClientKit/Checkpoint/RegtestCheckpointSource.swift | 1099 | `850f94df1c76dee9c445e9feedb5b8327cb7ffd44a8cce5aaa095bf4081cdd28` | 0 |
| Sources/ZcashLightClientKit/ClosureSynchronizer.swift | 8156 | `050fd7734e41c17ce48ff3f3419f53592bbd46be441c76a8459690e282bd0cc6` | 0 |
| Sources/ZcashLightClientKit/CombineSynchronizer.swift | 7281 | `65bca8ccb2f7393ceac92fc6dc6d2ade8220c3491a3a1b4bb90717eb7e209a02` | 0 |
| Sources/ZcashLightClientKit/Constants/Checkpoint+mainnet.swift | 532 | `d27f749b7f67a77258be9f26ddddbb1802b4666d297a76e3ada46aa17cc4dc7c` | 0 |
| Sources/ZcashLightClientKit/Constants/Checkpoint+regtest.swift | 1257 | `ad340ab28960be4ac703dc47fbf208381d16f9f205d9995a9ebc6a8c1918f83c` | 0 |
| Sources/ZcashLightClientKit/Constants/Checkpoint+testnet.swift | 532 | `601a64089864c342856d316a6053391bdd52ecc4a7ea763cfa03ad0482958722` | 0 |
| Sources/ZcashLightClientKit/Constants/NetworkActivationHeights.swift | 2487 | `83e0ee9f355aa052d3bbc5f5c510789b55b1d0fdbad31c0c0dc4d2b4d0e4fd96` | 0 |
| Sources/ZcashLightClientKit/Constants/ZcashSDK.swift | 13626 | `b1d35ac25870e8bbdd60b06303acbf3bd96ffc2475c6f480545e63105f90ddce` | 0 |
| Sources/ZcashLightClientKit/DAO/BlockDao.swift | 1748 | `fbee478f7449cec48559f950717b545e0b5cc76d8a8bb212c2cea05c2a524dd0` | 0 |
| Sources/ZcashLightClientKit/DAO/PagedTransactionDao.swift | 1492 | `0542b318832e05a348deca61a0f146beea9c7544261ae46e268ae711a4bf14b2` | 0 |
| Sources/ZcashLightClientKit/DAO/TransactionDao.swift | 12008 | `18e4a09bfeaf6033a1a3d6b3518645a4981c249ee50c09dfff502197cc31d816` | 0 |
| Sources/ZcashLightClientKit/DAO/UnspentTransactionOutputDao.swift | 635 | `b7e3f335be438aac77db47f51c296becf6d9afd34287edb5c00a29494c646d02` | 0 |
| Sources/ZcashLightClientKit/Entity/AccountEntity.swift | 723 | `8ee353170e9233875bca24f925b31a5d70ac5c2996f51c59eb308a7fce2783e6` | 0 |
| Sources/ZcashLightClientKit/Entity/EncodedTransactionEntity.swift | 791 | `0ec9e9549aafb9f42544bf19547f351c96742c9d20c46807a287e7d1415f957f` | 0 |
| Sources/ZcashLightClientKit/Entity/Pczt.swift | 141 | `877dd4b79ba5f9724e68c305bcd0138dcd3078474861e10a44394fb773301c37` | 0 |
| Sources/ZcashLightClientKit/Entity/SentNoteEntity.swift | 1269 | `6134527e624041a5f2287c1f01e6bd99bd8ac322c03e2e7404be5d92f567ad58` | 0 |
| Sources/ZcashLightClientKit/Entity/TransactionEntity.swift | 14779 | `8e30d9a85b1c80dff22f818865d44ceb517750f73de3da55a81208f7a995aa64` | 0 |
| Sources/ZcashLightClientKit/Entity/UnspentTransactionOutputEntity.swift | 461 | `814534999f4e781f85b89f747de7b7841657cd4320ad646ac656eee53ff11175` | 0 |
| Sources/ZcashLightClientKit/Entity/ZcashCompactBlock.swift | 2499 | `d4e8a979294bde4f58fac37427635c9010036f2fe3f478fe569347a34d50dcfa` | 0 |
| Sources/ZcashLightClientKit/Error/RedactedRustError.swift | 2841 | `44c31a888d8d45394c02bc652f0aa178deddd7768106de281c5d62ed2aafe348` | 0 |
| Sources/ZcashLightClientKit/Error/ZcashError+LocalizedError.swift | 868 | `2de2073c1c2b2c06457b73e9f2759218bd20df428e60d18e8058c084d7eae674` | 0 |
| Sources/ZcashLightClientKit/Error/ZcashError.swift | 113143 | `4d26aa96365a0e1afbfc5d88d8cfc83622f178377681fc8fae1891ba5c7b596b` | 0 |
| Sources/ZcashLightClientKit/Error/ZcashErrorCode.swift | 36713 | `58e5c17e5f78f1d8c5dad03fe6081accf9d4feaa243c4babb20ad71d6f37033a` | 0 |
| Sources/ZcashLightClientKit/Error/ZcashErrorCodeDefinition.swift | 62228 | `673843ad6989c419a2a3392da2f42df97512d367d8510bae0bace6d91794c344` | 0 |
| Sources/ZcashLightClientKit/Extensions/Bool+ToData.swift | 232 | `7477a8c9c1a0fd07afa761900d99a070db2d049903c462741034aba44e09cdf3` | 0 |
| Sources/ZcashLightClientKit/Extensions/Data+ToOtherTypes.swift | 315 | `2245c26abfd213913cdaca6f9e0f15b0cc20b5c77d2b7cd68f52486896d30310` | 0 |
| Sources/ZcashLightClientKit/Extensions/Data+Zcash.swift | 318 | `c73be1f32d422578cf0ab4268b4b7c0536fe9172ba49c276159aa887453d9063` | 0 |
| Sources/ZcashLightClientKit/Extensions/Data+internal.swift | 829 | `42e49dd728f25168916eb2dc8c799ccfaa3f6c0227831ebcaeabc0f8b296b825` | 0 |
| Sources/ZcashLightClientKit/Extensions/Error+ZcashError.swift | 327 | `07cd99a9d4b0c343e6b7093c44de9fb31547c797d84630bbbcbb49483324546a` | 0 |
| Sources/ZcashLightClientKit/Extensions/HexEncode.swift | 1089 | `f6f0577b66c57157328d274b31e071cff9b1aa99331f4f1d32f30ebe373241e7` | 0 |
| Sources/ZcashLightClientKit/Extensions/Int+ToData.swift | 230 | `49e0803165c672f5863c80361fa7b9bea7b2d2b560b83306f4fe9d642a49a3b3` | 0 |
| Sources/ZcashLightClientKit/Extensions/NumberFormatter+Zcash.swift | 494 | `b734a64597772eb746f2198699bf182e431a7217a660bf550d0cbd1b520ae765` | 0 |
| Sources/ZcashLightClientKit/Extensions/URL+UpdateWithAlias.swift | 1205 | `8b0f707b7eaf3d6cbaab842a53d5fba098e45c59522b66d187e8e3c4390e8041` | 0 |
| Sources/ZcashLightClientKit/Extensions/Undescribable.swift | 468 | `45d87808ec737d87efbb6d75ff43ad58caa8cf21f27178da6621262a017b7d8a` | 0 |
| Sources/ZcashLightClientKit/Extensions/Zatoshi+SQLite.swift | 371 | `ef166b3e558b92e3295d85ae226c6b63ef15fca1d245fb558fed2bde809dee01` | 0 |
| Sources/ZcashLightClientKit/Extensions/ZcashRust+Utils.swift | 572 | `c0e3df592399b991bba7ac6004395ee0f349752b778b6dbf3e37210e590c6d56` | 0 |
| Sources/ZcashLightClientKit/Extensions/ZcashSDK+extensions.swift | 712 | `06024bc269dab0d136d5e810aef7a8037aa2752384506b1797e925bbcca3bd92` | 0 |
| Sources/ZcashLightClientKit/Initializer.swift | 30378 | `d75d5a550d2ab35aa89e4cf176eaf41d79756dbf33678083946e4dff81b847e7` | 0 |
| Sources/ZcashLightClientKit/Metrics/SDKMetrics.swift | 4025 | `57f9aca61e2ed784d046ebf9be2f890a4c31ece66e862f3a70784309f6b21a91` | 0 |
| Sources/ZcashLightClientKit/Migration/ChainTipEstimator.swift | 8153 | `776c8a8a1cd65e41ace07c3e3a7da2dc84077beb59ed20b4fa7fe44548a959fe` | 0 |
| Sources/ZcashLightClientKit/Migration/MigrationBroadcaster.swift | 16552 | `6cf565c17fb698a5f3064e852a5ce7f9bb4797be6df2364289b3799514b99eb9` | 0 |
| Sources/ZcashLightClientKit/Migration/MigrationSyncGate.swift | 31420 | `57d9dd39e1fa300c3872876cb1117aaf35d465b8e5b64734011fa914ddef823b` | 0 |
| Sources/ZcashLightClientKit/Migration/OrchardMigration.swift | 60958 | `e68ac1df68baf5edb6d12b954ca568c4f25e1ea502eb9d37718a08d6f3825efd` | 0 |
| Sources/ZcashLightClientKit/Migration/OrchardMigrationHost.swift | 23083 | `d23badd6f0c51ac17591803cc1db794ed005d02e128fff6277d52280e8ecc1f1` | 0 |
| Sources/ZcashLightClientKit/Model/Eip681TransactionRequest.swift | 3303 | `637f8c908cd53e6255bc6ad164008c8e31ccc7899b47aa1572d1ae313c105b95` | 0 |
| Sources/ZcashLightClientKit/Model/FiatCurrencyResult.swift | 855 | `0c1f06732b991506ec4f3348325f9bcae4cd931d5e431141ccc6b5d798dd10ac` | 0 |
| Sources/ZcashLightClientKit/Model/Memo.swift | 7451 | `02f957adb460e31aeda9ad3342c3c495db4b93b6d63fe7da507dca961aabec4d` | 0 |
| Sources/ZcashLightClientKit/Model/MigrationModels.swift | 55867 | `8e3276e5332626f092963cb5a11aa1ea2d223e9d740769c66949a13acf2439e4` | 0 |
| Sources/ZcashLightClientKit/Model/Proposal.swift | 3197 | `c3fe134d36260332b53ff091b8c38739a58548d1446aaa7ca5aba0537e4323ff` | 0 |
| Sources/ZcashLightClientKit/Model/ScanRange.swift | 649 | `3e4c12357a315466f8102ab2ed6456cb574a24a4f4d674f693280c31fd696d4e` | 0 |
| Sources/ZcashLightClientKit/Model/ScanSummary.swift | 249 | `1ace1980a3ade8ba4453112b0aa08b64bf3f5384fd0e37693b6fa76b43745bd7` | 0 |
| Sources/ZcashLightClientKit/Model/SingleUseTransparentAddress.swift | 753 | `74b64c9d727ac3c44573ff711e5ecf57f56fe88a050e05acbd0cea4e15924e0a` | 0 |
| Sources/ZcashLightClientKit/Model/TransactionDataRequest.swift | 5860 | `0145e5057ccccba6b3399c2b9bfb4f4c77d99007486abfe9b40ba8702590cd6b` | 0 |
| Sources/ZcashLightClientKit/Model/TxId.swift | 1109 | `8eace1b6514da999e863880b33354c6c8ea613129409c17c231fed8cf61f653f` | 0 |
| Sources/ZcashLightClientKit/Model/WalletSummary.swift | 5105 | `0cf316c85a8a5874b205e6d2e9585c3fc9092692f32d578fe18cb4ba2345d8e8` | 0 |
| Sources/ZcashLightClientKit/Model/WalletTypes.swift | 13313 | `a17a16bfc6aaba6ff82614e6822b0f330f005f2e6d6d9c79d8822fdf9123e789` | 0 |
| Sources/ZcashLightClientKit/Model/Zatoshi.swift | 3612 | `e33fcb56c1eef083e4630a5862ce2141036f7c31d317261cce08cdd58fbfeee3` | 0 |
| Sources/ZcashLightClientKit/Model/ZcashNetwork+IronwoodActivation.swift | 948 | `6cae091ccb36991feb925d4cb98cc92ee73e4b0b47eb42f7a64cbeff0a431ed4` | 0 |
| Sources/ZcashLightClientKit/Modules/Service/GRPC/LightWalletGRPCService.swift | 19524 | `05d82c9f367124a1e016422a33e1ecd52e480501591f26b79c71c2744b4a1d9f` | 0 |
| Sources/ZcashLightClientKit/Modules/Service/GRPC/ProtoBuf/Extensions/Protocolbuffer+Extensions.swift | 1186 | `3660372f3445c8e4e8d6c111f167f86f7ac28d78d2c46fdf58a01f3cd6095bec` | 0 |
| Sources/ZcashLightClientKit/Modules/Service/GRPC/ProtoBuf/compact_formats.pb.swift | 26494 | `eb9dde3d35346413ccc4fc42c2b2f2b0671e3887ca4b3ec5dae1d380fca68c5a` | 0 |
| Sources/ZcashLightClientKit/Modules/Service/GRPC/ProtoBuf/proposal.pb.swift | 42510 | `c0c382edc742c6ea6ad6f51dfce6fc4a7ae01fce7bc09c8f210217ad24fe297b` | 0 |
| Sources/ZcashLightClientKit/Modules/Service/GRPC/ProtoBuf/proto/proposal.proto | 7647 | `cda75853804c312b481762111b3ffda0ff4442c7b5b03ecfc47a55e4f660c139` | 0 |
| Sources/ZcashLightClientKit/Modules/Service/GRPC/ProtoBuf/service.grpc.swift | 98144 | `10bdbec52293277f5266890813d23e26fadabd40c1f48d95bbad7c91b1cc238a` | 0 |
| Sources/ZcashLightClientKit/Modules/Service/GRPC/ProtoBuf/service.pb.swift | 62950 | `b70e743d5476ec9bea9e023763242d99fb693f5c58d193b391bb3f12d90b74e7` | 0 |
| Sources/ZcashLightClientKit/Modules/Service/LightWalletService.swift | 8594 | `7769934f501a7b0353628e1264362f17bca500dcea07f7635d7d906619957358` | 0 |
| Sources/ZcashLightClientKit/Modules/Service/Tor/LightWalletGRPCServiceOverTor.swift | 8850 | `c55b2ebe17a7dc3028b16cbfc8d52930cad4499c866d438d49c4858c18239ae5` | 0 |
| Sources/ZcashLightClientKit/Providers/LatestBlocksDataProvider.swift | 2474 | `ee355c7e4cae9fdfe460345c346768651b999e8e87b2e4ba17003c5d1f07f7f5` | 0 |
| Sources/ZcashLightClientKit/Providers/ResourceProvider.swift | 2590 | `b5ad7c7f2d7b86cb7629b547fcecd140623f38ab56062ca2bed60e5e5cef58f4` | 0 |
| Sources/ZcashLightClientKit/Repository/BlockRepository.swift | 268 | `b26f26c679fc1b19807d40c41286f895d684e78a263e5ba82c4664c34e3570b3` | 0 |
| Sources/ZcashLightClientKit/Repository/CompactBlockRepository.swift | 1359 | `7e307357687ec777cae926f008e6eef47296a859f40eb58ad9c9dcd4e278994e` | 0 |
| Sources/ZcashLightClientKit/Repository/NotesRepository.swift | 318 | `149ccef7d0ccd94c91e712003ac03c547ee6e7d530d83744c88e8763c3b21965` | 0 |
| Sources/ZcashLightClientKit/Repository/PaginatedTransactionRepository.swift | 739 | `009198d5cf21edd9c424aabd46c529aeef1ce2ab8f40a1aabcfc70d7a1f99025` | 0 |
| Sources/ZcashLightClientKit/Repository/TransactionRepository.swift | 1694 | `f869e5163567db178bd56cb8dfb167008690c3cc2cd750b9c8316306ec5ac313` | 0 |
| Sources/ZcashLightClientKit/Repository/TransactionRepositoryBuilder.swift | 801 | `3821bbc61dc4c199f78dacb55f887e477e76a2993dcb6eea8628f3540ca44621` | 0 |
| Sources/ZcashLightClientKit/Rust/Voting/PirSnapshotResolver.swift | 11053 | `770885b159979c08633e299de9b06072c19a5e8fb662351e8744b4a8e03c2ea2` | 0 |
| Sources/ZcashLightClientKit/Rust/Voting/VotingConstants.swift | 765 | `d908bc9b4fc904fe3dc730b73a2ac360c87f9a5ed5f0a1d1eb0a8fe7b0471439` | 0 |
| Sources/ZcashLightClientKit/Rust/Voting/VotingKeyTypes.swift | 5423 | `cd18af1a0a8617ff28680f3f36f50b1b311fdd775c4888d4e3d746487f41adf7` | 0 |
| Sources/ZcashLightClientKit/Rust/Voting/VotingRustBackend.swift | 86726 | `6f96ef9d20b4a99b6eec105c7a00ccab7ac16e7d3ca82abf2312e377469be846` | 0 |
| Sources/ZcashLightClientKit/Rust/Voting/VotingTypes.swift | 23705 | `2e6e66edc27fcf79e6e48ed2bfaf5b0d0d905d0d6a1da7c2924db359f17e53fc` | 0 |
| Sources/ZcashLightClientKit/Rust/WalletSummary+FFI.swift | 4739 | `a24dde9852350ad21ac491012674367eb957b7b6eba7473f97c5590bfa0a56a0` | 0 |
| Sources/ZcashLightClientKit/Rust/ZcashEip681Backend.swift | 10121 | `78c66400d88cefc9bee774aca23d1a2b300f6352161fdcf69b18c3dbb810d5d2` | 0 |
| Sources/ZcashLightClientKit/Rust/ZcashKeyDerivationBackend.swift | 9483 | `1519ec9c5c228dd35112837a5381355c837891b933d2ccaaa6dc1060f459d761` | 0 |
| Sources/ZcashLightClientKit/Rust/ZcashKeyDerivationBackendWelding.swift | 6186 | `f8093a864248e30e6baa2a8243a56c6b20ad972ff47d363b59a67cb25de3002a` | 0 |
| Sources/ZcashLightClientKit/Rust/ZcashRustBackend.swift | 132298 | `38a33feabbdb9e8582d5a5e534e8cb4136198c08eff9ace8aaec7bef3a086c1e` | 0 |
| Sources/ZcashLightClientKit/Rust/ZcashRustBackendWelding.swift | 54802 | `28b7a1c0a670fe465be318f953ebe042493e468f62f636842ff30d3379287cde` | 0 |
| Sources/ZcashLightClientKit/Synchronizer/ClosureSDKSynchronizer.swift | 11863 | `9f7ec07ee3b7d5d1332e1807969bd6d70dd1548c8ac7ee5e31d59760a06d1313` | 0 |
| Sources/ZcashLightClientKit/Synchronizer/CombineSDKSynchronizer.swift | 11147 | `37d73afbe787719085f8ce32ba33fae21cd8f19cec331ff56bed6d12f6cbd119` | 0 |
| Sources/ZcashLightClientKit/Synchronizer/Dependencies.swift | 10448 | `de55bf712b05843abfa762de4151f23d60a40140a0dbb57446444f7c8b59fb6c` | 0 |
| Sources/ZcashLightClientKit/Synchronizer/SDKBroadcaster.swift | 7785 | `09e6eee11a4568367ba62a90b188354ed1b42324b4f273f528466f300b82f1af` | 0 |
| Sources/ZcashLightClientKit/Synchronizer/SDKSynchronizer.swift | 66783 | `f69a0d0de236f53869c831111a71281bff3f8ddf8c1bc3261162c51619412e2a` | 0 |
| Sources/ZcashLightClientKit/Synchronizer.swift | 104332 | `007180ca59b48c4faaa3ce9d70901fb9645c302573e6370d84cb7de53bedfaac` | 0 |
| Sources/ZcashLightClientKit/Tool/DerivationTool.swift | 13683 | `95034aa99c12335a9270b713b2e6fd62639389995bdc40170501b1c0c3eb2104` | 0 |
| Sources/ZcashLightClientKit/Tor/TorClient.swift | 18296 | `1004871c74d77bb58fd18878cce2710aff6989dbf1b23e155d4512a1490d527a` | 0 |
| Sources/ZcashLightClientKit/Transaction/EndpointSubmitter.swift | 2521 | `399533ac3047859c8ea1be5a3ad1a110a358f75de7f2620e8ef29e71e0466632` | 0 |
| Sources/ZcashLightClientKit/Transaction/MultiEndpointSubmitter.swift | 10497 | `1bf2cecd3556dc3c2626fe853348ac863d0a6bf717cb1f293f8d9ed25dc2f952` | 0 |
| Sources/ZcashLightClientKit/Transaction/SubmitPlanExecutor.swift | 1562 | `d873f4e0d6119570bed282774fe51d5747701093aeeb7fd1809f31e5edde8e99` | 0 |
| Sources/ZcashLightClientKit/Transaction/SubmitPlanStore.swift | 9508 | `b047f7a733c38e607edef2634b07f30fecf72cf9b271d280ad7e1bbb1876d318` | 0 |
| Sources/ZcashLightClientKit/Transaction/TransactionEncoder.swift | 5775 | `1bf2c67169c73c0a044d52489827d977cc8cfb8ad01b4d18cb3322397ccffa75` | 0 |
| Sources/ZcashLightClientKit/Transaction/TxResubmitter.swift | 7646 | `11275db58936a43b265d4a06fa57d0676923a88d6d8fa22598409d34d983c48f` | 0 |
| Sources/ZcashLightClientKit/Transaction/WalletTransactionEncoder.swift | 6871 | `196c0dddef314b75fd85074ab510961814032a12ec757aff2a94bd6eb3d5de9f` | 0 |
| Sources/ZcashLightClientKit/Utils/AsyncToClosureGateway.swift | 1202 | `f55b5a89f87592c52a7f2c5bd2a8f2742c94f46a26a95be43f1bea6a6e5da958` | 0 |
| Sources/ZcashLightClientKit/Utils/AsyncToCombineGateway.swift | 1745 | `e52fb4a5a2f9824802271c760e263ae98279de3cffd9f313112281103315576e` | 0 |
| Sources/ZcashLightClientKit/Utils/BackupExcludedStorage.swift | 2096 | `6db3a8e743b6eee80e30d8ac58f150f4a2179695dc99627fbc7b96869db72d9a` | 0 |
| Sources/ZcashLightClientKit/Utils/Clamped.swift | 830 | `dc6a809c931a610571c437fa7c7a8e5bee788201ce4bdb5b196be5b7d8919729` | 0 |
| Sources/ZcashLightClientKit/Utils/DBActor.swift | 1954 | `ef887ae70511e578c31db5be07203fbaab8c378188d3c819b9d18d23d96ecd75` | 0 |
| Sources/ZcashLightClientKit/Utils/DIContainer.swift | 3597 | `c84be42acee48cab2b6f019ee6d20e00bb0661b095903226a67d6acf5141cf72` | 0 |
| Sources/ZcashLightClientKit/Utils/GenericActor.swift | 314 | `bbef7ff013f54f44e7fe154ab6ae3c54810653a830cad13032d2b984de769f97` | 0 |
| Sources/ZcashLightClientKit/Utils/LoggingProxy.swift | 2657 | `80c7dd801ce029ed0c45c6bc68a325cbfbf9588ed99094cbd81a75433cfd2b78` | 0 |
| Sources/ZcashLightClientKit/Utils/OSLogger.swift | 4116 | `869f8adcf08e0c50ee1d0bc8a0542fb865039f4463a88fa63b87eb8c8f3eaec5` | 0 |
| Sources/ZcashLightClientKit/Utils/SDKFlags.swift | 3277 | `01677794ab1124d031580d649df173db77b7f4c025070f943e13787179061171` | 0 |
| Sources/ZcashLightClientKit/Utils/SaplingParameterDownloader.swift | 7297 | `366ee712d90ee3f619b4ddb5f08b038e97b4085a2bcc013f985f3c7bc8ea0e40` | 0 |
| Sources/ZcashLightClientKit/Utils/SpecificCombineTypes.swift | 454 | `11c5643fa1ad93bd6ce285294d5150a8c7a3fbd105f72ee8a0081854f8f15ba1` | 0 |
| Sources/ZcashLightClientKit/Utils/SyncSessionIDGenerator.swift | 755 | `98c8dec0a158cc87f40fa2128a6f5a205603d4c8abaf258ae27d29430e56cbac` | 0 |
| Sources/ZcashLightClientKit/Utils/Task+sleep.swift | 294 | `b4eae0f182fd4857cdef2c030c81139a8e5a5fb8a4b2a2e867c8b2717f3e7b66` | 0 |
| Sources/ZcashLightClientKit/Utils/UsedAliasesChecker.swift | 1512 | `b72f3fd2231a8c59ea97e2e469f8eabc23ae2911beda691752bac3f4da0a9590` | 0 |
| Sources/ZcashLightClientKit/Utils/WitnessesFixGate.swift | 6465 | `4d89bcef152ce849dbced991bda192e00c162caf628d56b086949173894f6a48` | 0 |
| Sources/ZcashLightClientKit/Utils/ZcashFileManager.swift | 325 | `c309049dd20537366c31e46a0831503c8d093f337c53e7d48e09f29d4efc2a5f` | 0 |
| lightwallet-protocol/walletrpc/compact_formats.proto | 6490 | `d8d0c8aaa5ceec7d5dcc188ef25b04011df2ec0254901620fce982fc13aeb32d` | 0 |
| lightwallet-protocol/walletrpc/service.proto | 15236 | `6fbfa974081fb02366a3118a25764af289bdbb86688978f5ff2bae661dfa346a` | 0 |
| responsible_disclosure.md | 4648 | `b22c1c8a1dad5e09a915455a9111014624ba559bbea9c7b08f2dd4e1df0782f2` | 0 |
| rust/build.rs | 3528 | `b6ceacf11198555804bd255be6ce8b0e507b9b35e4532da1056cb8026f6eecf9` | 0 |
| rust/src/derivation.rs | 31382 | `37ae450b8c1a65ed189d48ae04adb2baee7c494c3f55346ee68616f9ba5467c6` | 0 |
| rust/src/eip681.rs | 17307 | `1ffdce28a5180709863f6055cfa9b1da2e2d5a8541440bb1845c035b4079f3f6` | 0 |
| rust/src/error_report.rs | 22607 | `3300906616d2bd81f3e098d1564c7c3976a0add7d2b1332b52b8130bbf82034f` | 0 |
| rust/src/ext_schema.rs | 2703 | `78c735696386d4f577fdea09b3c28686c8ad40f8472f1ccf37c9667ae9925af9` | 0 |
| rust/src/ffi/sys.rs | 119 | `16c6b95133b0dd82837ec3d098e637bcae957aab180bebe37c697ad42a88c66f` | 0 |
| rust/src/ffi.rs | 49683 | `3cfcb04dfabb39544f28faba641523b7028e521da82ec11dfa3b8184df26c8eb` | 0 |
| rust/src/lib.rs | 208268 | `afc4b32a0843665f4022b976de0b9664f0e020c159692503976fc2b5e0088bfd` | 0 |
| rust/src/migration.rs | 532046 | `e614bf9f2de830fe338a26ae55c9be82ead182ff0dfd7d35be8da41af9ac7663` | 0 |
| rust/src/migration_engine.rs | 7679 | `6f486536fcb33419ed2c2a1692ad4042f54e76d24c7ae1fb7f4e9ac68b5c05f1` | 0 |
| rust/src/migration_finalize.rs | 12826 | `f12370cdd2d684918463c5a6b2f4aa3e906bb12bb00d22e69daab2c60b33ef22` | 0 |
| rust/src/migration_keystone.rs | 27554 | `3745f20c7ad10878b32a7bf8285b9a562a0b5c02605f9e62418c862fd7fb1ec8` | 0 |
| rust/src/migration_plan_cache.rs | 6391 | `dab3c8fe290705fc52b8be473a1f4d774e3d53734eb2194b30ebb94b7b49789b` | 0 |
| rust/src/migration_turnstile.rs | 4462 | `cc33f903018993bfd8618ba94f7cceabadd3f0045d5c82f56626fedf15ef63d2` | 0 |
| rust/src/os_log/layer.rs | 871 | `bdb7e530c379bf4f3c0b134fe20c34c29553467a10c0d211c34fa1d441c06acf` | 0 |
| rust/src/os_log/signpost.rs | 2643 | `d2c814fafdea8dba57fde91b32b4728ca404db9bd1a792234728ac8a1431b087` | 0 |
| rust/src/os_log/writer.rs | 2215 | `f7f85b1e75b6f34bb9653a71f75ed79a21d773a7fa8eaa97f8a115bfd134f6ef` | 0 |
| rust/src/os_log.rs | 2216 | `e1f1be0bf4d4b1cbfa6c5c4ab3a1da082a7f27e6d41251882213648ddcddedbd` | 0 |
| rust/src/tor.rs | 9927 | `b4fb708571b1779bc2b9bdaddc640204f26e50de99e6bf7aba4db02b1d335bd4` | 0 |
| rust/src/voting/confirmation.rs | 2756 | `663e7c0a08585a1f755ed4f60a2f085a07a6587266186b15172cb6e5b2a005d4` | 0 |
| rust/src/voting/constants.rs | 2100 | `9577388b6831849edae435d202303b7140873d05be3d5122467dcccb09cdda18` | 0 |
| rust/src/voting/db.rs | 7533 | `0b8d71ed8e6802d2add5a166890f9ae81033d707daf7ae7a709a581d18f1c80e` | 0 |
| rust/src/voting/delegation.rs | 70957 | `e87f24b8c0a799f6577b20c04a8fd8934a574358c3cdda49ae5dd76f53b8f2e6` | 0 |
| rust/src/voting/ffi_types.rs | 6328 | `184ea90611e9f9e690bb8f6b6618219b45b7ba700f526d388bb197c64546b024` | 0 |
| rust/src/voting/helpers.rs | 8945 | `f7ceda1fd8a2a2c04b75a026904213bee0426d69fc7e87af69f8d4153d8ed103` | 0 |
| rust/src/voting/json.rs | 6696 | `85078385184c23a71456e2929878204274f7addef125dc283f2354cc308225cd` | 0 |
| rust/src/voting/notes.rs | 9619 | `7b2561686ba60d26bbfb8629aa5ceba086c94c31b42ae2b356bd30c3703a8341` | 0 |
| rust/src/voting/progress.rs | 1516 | `732e388c0c58cd6eb68493094388a97beb33371e3a644c73b141f4829eec1a80` | 0 |
| rust/src/voting/recovery.rs | 25607 | `a972e84fb3cf28e348b780df4587ddb33df391bd6e6c5ffaa3961b821952b14a` | 0 |
| rust/src/voting/rounds.rs | 17983 | `6c9ae05545c889923962d8ba1f6162cd4159cbea12437157dc3fc38b94fc76e8` | 0 |
| rust/src/voting/share_tracking.rs | 19735 | `74942bcf7842203b28da6e69c097286f11a188c0174e6d5a9c788565e230dccf` | 0 |
| rust/src/voting/signing.rs | 18168 | `b6a69b6fcf2df3ba81dcff8f5601373ce0646d0393cb5b9b427b809d941527fe` | 0 |
| rust/src/voting/tree.rs | 3800 | `d4409c4a543592d6c1fd2ae4bff8ecd9b0407639038bd021fc2f015b6728a666` | 0 |
| rust/src/voting/util.rs | 24536 | `905651b85dc1fa229641b84226bf1a388aea577723ea1763e6a881c181e7110c` | 0 |
| rust/src/voting/vote.rs | 12732 | `745787066754dc8eed0680b92d1c1e03acd2d01f81c69f6b095c4b5ba2936570` | 0 |
| rust/src/voting.rs | 784 | `fda5fcd11bfa1c705e1151f4fce52474bd35ddfee4e08025aa11df1b28e43c5b` | 0 |
| rust/wrapper.c | 573 | `36ae07d00d702e2db37417af79637dc86964657d730a9b200040e91d4ac61768` | 0 |
| rust/wrapper.h | 375 | `449d05440894d5e11a82bc7c010a6021146edc440a981fb90522b8e9f5dd2791` | 0 |
