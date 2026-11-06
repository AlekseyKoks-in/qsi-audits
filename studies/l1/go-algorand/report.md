# Security & Post-Quantum Readiness Audit Report

**Project:** go-algorand @ e46aea5466a1 · Algorand Foundation — public repository (passive review)
| | |
|---|---|
| Organization | QSI |
| Report date | 2026-11-06 16:16 UTC |
| Report version | 1 |
| Audit run | 96d950eb-cb91-4272-91ed-00709f332206 (Document audit) |
| Analyzer engine | qsi-engine 1.3.0 |
| Risk profile | Crypto exchange, custodian or wallet |
| Content SHA-256 | `6d145d52c9c066144e055074447ebfbd4d0fe3daaa4654cbf36de67ea6eb5165` |
| Signature key (Ed25519, SHA-256 fingerprint; the signature is the separate file report.sig.json) | `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e` |
> This report presents automated and documented analysis results for the stated scope. It is not a legal opinion, a certification or an attestation of compliance with any standard.

## 1. Executive summary

- Critical: **0**
- High: **1**
- Medium: **11**
- Low: **3**
- Info: **7**

- Confirmed technical vulnerability: 0
- Known vulnerable component: 14
- Confirmed configuration error: 1
- Potential cryptographic risk: 0
- Long-term post-quantum risk: 7
- Improvement recommendation: 0
- Insufficient data: 0

Mosca's inequality (x + y > z): x = 10, y = 5, z = 8 → migration would finish too late under this scenario. _z is a planning assumption chosen per risk profile, not a prediction. A cryptographically relevant quantum computer is not publicly known to exist today._

**Post-quantum maturity: Level 2 of 4 — post-quantum in use outside the critical paths.** Next step: Extend post-quantum protection to the critical roles that stay classical, starting with what can be recorded today (wrapped keys, channel key exchange).

## 2. Scope and boundaries

Mode: Document audit

Repository: <https://github.com/algorand/go-algorand> @ `e46aea5466a1152af6e08f83555ed16cfcd89f49` — evidence links open the lines at this commit.

1160 files, 10256158 bytes in total, 1 redaction(s); the per-file SHA-256 list is in appendix C.

## 3. Methodology

| Area | Status | Count | Examples |
|---|---|---|---|
| source_code | checked | 1152 | agreement/abstractions.go: 335 lines scanned with 16 rule patterns and 267 registry patterns; agreement/actions.go: 569 lines scanned with 16 rule patterns and 267 registry patterns; agreement/actiontype_string.go: 39 lines scanned with 16 rule patterns and 267 registry patterns |
| dependencies | checked | 6 | cmd/partitiontest_linter/go.mod: 4 dependencies parsed (4 pinned); go.mod: 185 dependencies parsed (185 pinned); tools/block-generator/go.mod: 166 dependencies parsed (166 pinned) |
| certificates_and_keys | checked | 1 | installer/rpm/RPM-GPG-KEY-Algorand: certificates/keys parsed |
| entropy | checked | 1 | random-number generation: 1152 code files read with 537 macro definitions from the tree; 0 ineffective guard(s), 0 weak random-bytes provider(s), 0 weak key-generation site(s) |
| osv_advisories | checked | 1 | 193 pinned packages queried at OSV.dev; 10 affected |

_Long lists are grouped here; the full per-file list is in the JSON report, signed with the same key._

## 4. Assets examined and not examined

- None

## 5. Architecture overview

Static review of the source tree go-algorand at e46aea5466a1152af6e08f83555ed16cfcd89f49. 1160 files analysed; of 3096 files, 1393 are test, fuzzing, benchmark or example code and were left out, 542 are not read by any analyzer, 1 exceed the per-file limit and 0 did not fit the total limit. Files no analyzer reads include: .aptly.conf, .claude/skills/combine-dependabot-prs/SKILL.md, .claude/skills/promote-vfuture/SKILL.md, .claude/skills/spec-consensus-param/SKILL.md, .codecov.yml. 64 files in build-output or dependency-cache directories (.git, .hg, .venv, __pycache__, build, dist, node_modules, target, vendor, venv) were not read. No requests were sent to the owner's systems.

## 6. Overall security posture

- Indicative posture index: **70** / 100 — _Derived from findings in scope (confirmed and potential issues weighted by severity). Indicative only; not comparable across differently scoped audits._
- Quantum-vulnerable share of inventory: 33.4%

## 7. Detailed findings

### QSI-2026-19631 — Possible hard-coded secret in logging/telemetryConfig.go

- Severity: **High** · Classification: Confirmed configuration error · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `file:logging/telemetryConfig.go`
- Data source: logging/telemetryConfig.go
- Detection method: Regular-expression matching of language-specific API patterns.
- Analyzer: source_code 1.3.0 · 2026-11-06 16:16 UTC
- Priority score: 47.1 / 100
- CVSS v3.1: not applicable

1 secret-like value(s) of type generic_assignment (first at line 35). Values were redacted by QSI.

**Potential impact.** Credentials in source code leak through repositories, builds and logs.

**Reproduction steps.**

```
Open line 35 in the supplied file logging/telemetryConfig.go and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [logging/telemetryConfig.go](https://github.com/algorand/go-algorand/blob/e46aea5466a1152af6e08f83555ed16cfcd89f49/logging/telemetryConfig.go#L35) · line 35 · SHA-256 7b816d3ae2740f85ab1dd0753c2d64809d1455a1106315eb63dafd6064cb1fb2_

```
   35 | var defaultTelemetryPassword = "[REDACTED]"
```

**Limitations of the check.** Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Move secrets to a secrets manager/environment; rotate the exposed values.

**Retest procedure.** Re-scan the source and review the call sites listed in the evidence.

### QSI-2026-19630 — Quantum-vulnerable RSA key (2048-bit) in installer/rpm/RPM-GPG-KEY-Algorand

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: High
- Affected asset: `file:installer/rpm/RPM-GPG-KEY-Algorand#line 1`
- Data source: installer/rpm/RPM-GPG-KEY-Algorand
- Detection method: Public key parsing.
- Analyzer: certificates 1.3.0 · 2026-11-06 16:16 UTC
- Priority score: 50.3 / 100
- CVSS v3.1: not applicable

A RSA 2048-bit public key was found (line 1).

**Potential impact.** Long-term risk once a CRQC exists; for key exchange, recorded traffic could be decrypted retroactively.

**Reproduction steps.**

```
Open line 1 in the supplied file installer/rpm/RPM-GPG-KEY-Algorand and inspect the quoted lines (see evidence).
```

**Evidence.**

_key · installer/rpm/RPM-GPG-KEY-Algorand · line 1 · SHA-256 99f8a76d7955bc1cad612c6fe14ee442ba2c3ba5655096eda02d83c54d97d810_

```
OpenPGP primary key: algorithm ID 1 (RSA) 2048-bit
```

_key · installer/rpm/RPM-GPG-KEY-Algorand · line 1 · SHA-256 a744425426415d58dbeef862a6f1d8bcf6b00820639c8784270363d0b6330969_

```
OpenPGP subkey: algorithm ID 1 (RSA) 2048-bit
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability.

**Recommendation.** Inventory and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it..

**Retest procedure.** Re-audit after migration.

### QSI-2026-19635 — github.com/labstack/echo/v4 v4.16.1 is affected by GHSA-246p-cpwv-v3jq (CVE-2026-118653, GO-2026-6872)

- Severity: **Medium** · Classification: Known vulnerable component · Confidence: Medium
- Affected asset: `dependency:Go/github.com/labstack/echo/v4@v4.16.1`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 16:16 UTC
- Priority score: 44.2 / 100
- CVSS v3.1: 5.3 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:N`)

OSV.dev reports GHSA-246p-cpwv-v3jq (CVE-2026-118653, GO-2026-6872) for Go package github.com/labstack/echo/v4 at version v4.16.1: Echo has Rate Limiter Bypass via Spoofed X-Forwarded-For Header in Default Configuration. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-246p-cpwv-v3jq
```

**Evidence.**

_tool_output · [OSV.dev GHSA-246p-cpwv-v3jq](https://osv.dev/vulnerability/GHSA-246p-cpwv-v3jq) · line 37 · SHA-256 155528c0a1c25237da1ea48e611838aaeb8218a372fcee25c536b78078c5363e_

```
{"id": "GHSA-246p-cpwv-v3jq", "aliases": ["CVE-2026-118653", "GO-2026-6872"], "modified": "2026-11-05T23:26:14.796992232Z", "summary": "Echo has Rate Limiter Bypass via Spoofed X-Forwarded-For Header in Default Configuration", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:N"}], "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed. A Go function counts only in a file that also names its package (a method: its type); unexported functions only through the exported ones.

**Recommendation.** Upgrade to a fixed version (none published yet; see the advisory for mitigations).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-19636 — github.com/labstack/echo/v4 v4.16.1 is affected by GHSA-99jh-6h7p-pp36 (CVE-2026-118651, GO-2026-6875)

- Severity: **Medium** · Classification: Known vulnerable component · Confidence: Medium
- Affected asset: `dependency:Go/github.com/labstack/echo/v4@v4.16.1`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 16:16 UTC
- Priority score: 44.2 / 100
- CVSS v3.1: 5.3 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:N`)

OSV.dev reports GHSA-99jh-6h7p-pp36 (CVE-2026-118651, GO-2026-6875) for Go package github.com/labstack/echo/v4 at version v4.16.1: Echo: Reverse Proxy Forwards Attacker-Supplied X-Real-IP to Upstream by Default. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-99jh-6h7p-pp36
```

**Evidence.**

_tool_output · [OSV.dev GHSA-99jh-6h7p-pp36](https://osv.dev/vulnerability/GHSA-99jh-6h7p-pp36) · line 37 · SHA-256 e73925195a680d3902a1a2e7fe897faa454885abde43edcb5242caee51ca5540_

```
{"id": "GHSA-99jh-6h7p-pp36", "aliases": ["CVE-2026-118651", "GO-2026-6875"], "modified": "2026-11-05T23:25:35.191121662Z", "summary": "Echo: Reverse Proxy Forwards Attacker-Supplied X-Real-IP to Upstream by Default", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:N"}], "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed. A Go function counts only in a file that also names its package (a method: its type); unexported functions only through the exported ones.

**Recommendation.** Upgrade to a fixed version (none published yet; see the advisory for mitigations).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-19642 — github.com/pion/dtls/v2 v2.2.12 is affected by GHSA-9f3f-wv7r-qc8r (CVE-2026-26014, GO-2026-4479)

- Severity: **Medium** · Classification: Known vulnerable component · Confidence: Medium
- Affected asset: `dependency:Go/github.com/pion/dtls/v2@v2.2.12`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 16:16 UTC
- Priority score: 44.2 / 100
- CVSS v3.1: 5.9 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:N/A:N`)

OSV.dev reports GHSA-9f3f-wv7r-qc8r (CVE-2026-26014, GO-2026-4479) for Go package github.com/pion/dtls/v2 at version v2.2.12: Pion DTLS's usage of random nonce generation with AES GCM ciphers risks leaking the authentication key. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-9f3f-wv7r-qc8r
```

**Evidence.**

_tool_output · [OSV.dev GHSA-9f3f-wv7r-qc8r](https://osv.dev/vulnerability/GHSA-9f3f-wv7r-qc8r) · line 141 · SHA-256 7eb37c2b6ca00b8aa0dcef0d206b61e27e7a6d7ba19c535510643573c31d6b5e_

```
{"id": "GHSA-9f3f-wv7r-qc8r", "aliases": ["CVE-2026-26014", "GO-2026-4479"], "modified": "2026-09-10T03:50:34.689023565Z", "summary": "Pion DTLS's usage of random nonce generation with AES GCM ciphers risks leaking the authentication key", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:N/A:N"}], "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed. A Go function counts only in a file that also names its package (a method: its type); unexported functions only through the exported ones.

**Recommendation.** Upgrade to a fixed version (none published yet; see the advisory for mitigations).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-19643 — github.com/pion/stun v0.6.1 is affected by GHSA-34rh-wp3j-6cxc (CVE-2026-54909)

- Severity: **Medium** · Classification: Known vulnerable component · Confidence: Medium
- Affected asset: `dependency:Go/github.com/pion/stun@v0.6.1`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 16:16 UTC
- Priority score: 44.2 / 100
- CVSS v3.1: 5.3 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L`)

OSV.dev reports GHSA-34rh-wp3j-6cxc (CVE-2026-54909) for Go package github.com/pion/stun at version v0.6.1: Pion STUN vulnerable to remote denial of service via panic while parsing a malformed XOR-MAPPED-ADDRESS attribute. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-34rh-wp3j-6cxc
```

**Evidence.**

_tool_output · [OSV.dev GHSA-34rh-wp3j-6cxc](https://osv.dev/vulnerability/GHSA-34rh-wp3j-6cxc) · line 153 · SHA-256 25b88eee7863898f5def9a554b94bf4f6ddbae56da03d4abd189bf9ea0cea347_

```
{"id": "GHSA-34rh-wp3j-6cxc", "aliases": ["CVE-2026-54909", "GO-2026-6163"], "modified": "2026-09-10T03:50:51.344851444Z", "summary": "Pion STUN vulnerable to remote denial of service via panic while parsing a malformed XOR-MAPPED-ADDRESS attribute", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L"}], "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed. A Go function counts only in a file that also names its package (a method: its type); unexported functions only through the exported ones.

**Recommendation.** Upgrade to a fixed version (none published yet; see the advisory for mitigations).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-19627 — Quantum-vulnerable X25519: key wrapping and data encryption at rest (1 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:X25519:key_wrapping`
- Data source: crypto/libsodium-fork/src/libsodium/crypto_box/crypto_box_seal.c
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.3.0 · 2026-11-06 16:16 UTC
- Priority score: 36.9 / 100
- CVSS v3.1: not applicable

1 reference(s) to X25519 across 1 file(s), e.g. crypto/libsodium-fork/src/libsodium/crypto_box/crypto_box_seal.c:32. Role, judged from paths, function names and nearby code: key wrapping and data encryption at rest. Keys or data encrypted to these public keys are stored: anyone who copies them now decrypts them once a CRQC exists (harvest now, decrypt later).

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open crypto/libsodium-fork/src/libsodium/crypto_box/crypto_box_seal.c:32 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [crypto/libsodium-fork/src/libsodium/crypto_box/crypto_box_seal.c](https://github.com/algorand/go-algorand/blob/e46aea5466a1152af6e08f83555ed16cfcd89f49/crypto/libsodium-fork/src/libsodium/crypto_box/crypto_box_seal.c#L32) · line 32 · SHA-256 7639098c5e359f826c9a3a9916473df34aeaeacbae782ff962a91a2774a1d37e_

```
   31 | 
   32 |     if (crypto_box_keypair(epk, esk) != 0) {
   33 |         return -1; /* LCOV_EXCL_LINE */
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Wrap keys with ML-KEM or a hybrid KEM (X25519 + ML-KEM-768) and re-wrap the stored keys; data that may already have been copied needs its own assessment.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-19628 — Quantum-vulnerable ECDSA: transaction and message signing (26 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:ECDSA:transaction_signing`
- Data source: crypto/secp256k1/curve.go
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.3.0 · 2026-11-06 16:16 UTC
- Priority score: 35.6 / 100
- CVSS v3.1: not applicable

96 reference(s) to ECDSA across 26 file(s), e.g. crypto/secp256k1/curve.go:33. Role, judged from paths, function names and nearby code: transaction and message signing. A CRQC derives the private key from a public key that is already known (on chain after the first spend, in reused addresses): funds and approvals controlled by these keys need a migration path.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open crypto/secp256k1/curve.go:33 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [crypto/secp256k1/curve.go](https://github.com/algorand/go-algorand/blob/e46aea5466a1152af6e08f83555ed16cfcd89f49/crypto/secp256k1/curve.go#L33) · line 33 · SHA-256 0efb6d1753fc3c985dc73870733075bc0601bec436a8c4ba906dee7e7605d63d_

```
   32 | 
   33 | package secp256k1
   34 | 
```

_file_excerpt · [crypto/secp256k1/dummy.go](https://github.com/algorand/go-algorand/blob/e46aea5466a1152af6e08f83555ed16cfcd89f49/crypto/secp256k1/dummy.go#L14) · line 14 · SHA-256 a93bed01956bdb2d2574be6d038986d6fb6c1ff3f632d0d1036a9d81c78cee74_

```
   13 | 
   14 | package secp256k1
   15 | 
```

_file_excerpt · [crypto/secp256k1/dummy.go](https://github.com/algorand/go-algorand/blob/e46aea5466a1152af6e08f83555ed16cfcd89f49/crypto/secp256k1/dummy.go#L17) · line 17 · SHA-256 ad5aa81a776fd75d6e130c0cd9e86f0b320496ff3156c30801f6ad3010389529_

```
   16 | import (
   17 | 	_ "github.com/algorand/go-algorand/crypto/secp256k1/libsecp256k1/include"
   18 | 	_ "github.com/algorand/go-algorand/crypto/secp256k1/libsecp256k1/src"
```

_file_excerpt · [crypto/secp256k1/dummy.go](https://github.com/algorand/go-algorand/blob/e46aea5466a1152af6e08f83555ed16cfcd89f49/crypto/secp256k1/dummy.go#L18) · line 18 · SHA-256 30eca17768087ba85bf85824b1323b4173075618dad12bf4edb7ae4c4ab9706f_

```
   17 | 	_ "github.com/algorand/go-algorand/crypto/secp256k1/libsecp256k1/include"
   18 | 	_ "github.com/algorand/go-algorand/crypto/secp256k1/libsecp256k1/src"
   19 | 	_ "github.com/algorand/go-algorand/crypto/secp256k1/libsecp256k1/src/modules/recovery"
```

_file_excerpt · [crypto/secp256k1/ext.h](https://github.com/algorand/go-algorand/blob/e46aea5466a1152af6e08f83555ed16cfcd89f49/crypto/secp256k1/ext.h#L53) · line 53 · SHA-256 051aeb46545f89d7e8f0c1bbb9a3520d04efa2a9f1f9f72ddaa5ec232c1b1cd2_

```
   52 | ) {
   53 | 	secp256k1_ecdsa_signature sig;
   54 | 	secp256k1_pubkey pubkey;
```

_file_excerpt · [crypto/secp256k1/ext.h](https://github.com/algorand/go-algorand/blob/e46aea5466a1152af6e08f83555ed16cfcd89f49/crypto/secp256k1/ext.h#L56) · line 56 · SHA-256 b6c5991701d9a948b642bc9c59b3ea64395decd9753d88bf512c1f1f4aff3cf3_

```
   55 | 
   56 | 	if (!secp256k1_ecdsa_signature_parse_compact(ctx, &sig, sigdata)) {
   57 | 		return 0;
```

_file_excerpt · [crypto/secp256k1/ext.h](https://github.com/algorand/go-algorand/blob/e46aea5466a1152af6e08f83555ed16cfcd89f49/crypto/secp256k1/ext.h#L62) · line 62 · SHA-256 4304b95e08cf7b885d19684c7c080b3924f2ce38be0b7f423b127c01ad545652_

```
   61 | 	}
   62 | 	return secp256k1_ecdsa_verify(ctx, &sig, msgdata, &pubkey);
   63 | }
```

_file_excerpt · [crypto/secp256k1/libsecp256k1/contrib/lax_der_parsing.c](https://github.com/algorand/go-algorand/blob/e46aea5466a1152af6e08f83555ed16cfcd89f49/crypto/secp256k1/libsecp256k1/contrib/lax_der_parsing.c#L8) · line 8 · SHA-256 d8fa0de7aecc6613c84d2ca894169b7de7607d7849fe578dca238a068ae402f2_

```
    7 | #include <string.h>
    8 | #include <secp256k1.h>
    9 | 
```

_file_excerpt · [crypto/secp256k1/libsecp256k1/contrib/lax_der_parsing.c](https://github.com/algorand/go-algorand/blob/e46aea5466a1152af6e08f83555ed16cfcd89f49/crypto/secp256k1/libsecp256k1/contrib/lax_der_parsing.c#L12) · line 12 · SHA-256 f7cc1f35d372c550d69cc9ae6dbeaef5c715147934a596093393ff5a3d554126_

```
   11 | 
   12 | int ecdsa_signature_parse_der_lax(const secp256k1_context* ctx, secp256k1_ecdsa_signature* sig, const unsigned char *input, size_t inputlen) {
   13 |     size_t rpos, rlen, spos, slen;
```

_file_excerpt · [crypto/secp256k1/libsecp256k1/contrib/lax_der_parsing.c](https://github.com/algorand/go-algorand/blob/e46aea5466a1152af6e08f83555ed16cfcd89f49/crypto/secp256k1/libsecp256k1/contrib/lax_der_parsing.c#L20) · line 20 · SHA-256 d8262388bcb8acbc6152fed7b7d97a4b161dc411e4574e9fcfb7f1e6b3707835_

```
   19 |     /* Hack to initialize sig with a correctly-parsed but invalid signature. */
   20 |     secp256k1_ecdsa_signature_parse_compact(ctx, sig, tmpsig);
   21 | 
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains adopt them.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-19625 — Quantum-vulnerable Ed25519: role not determined (19 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:Ed25519:general`
- Data source: crypto/batchverifier.c
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.3.0 · 2026-11-06 16:16 UTC
- Priority score: 34.2 / 100
- CVSS v3.1: not applicable

253 reference(s) to Ed25519 across 19 file(s), e.g. crypto/batchverifier.c:16. Role, judged from paths, function names and nearby code: role not determined. The code does not show what the keys protect; review decides the priority.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open crypto/batchverifier.c:16 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [crypto/batchverifier.c](https://github.com/algorand/go-algorand/blob/e46aea5466a1152af6e08f83555ed16cfcd89f49/crypto/batchverifier.c#L16) · line 16 · SHA-256 7fbf57fc364fb19eb48e721897377a04950422f3d574e94e5ff3a1857e00a688_

```
   15 |         mpos += mlen[i];
   16 |         publicKeys2D[i] = &publicKeys1D[i*crypto_sign_ed25519_PUBLICKEYBYTES];
   17 |         signatures2D[i] = &signatures1D[i*crypto_sign_ed25519_BYTES];
```

_file_excerpt · [crypto/batchverifier.c](https://github.com/algorand/go-algorand/blob/e46aea5466a1152af6e08f83555ed16cfcd89f49/crypto/batchverifier.c#L17) · line 17 · SHA-256 4cd9d116a43d62adec6c381495333af76ead39f89d22ed041c970d8c3b4c068d_

```
   16 |         publicKeys2D[i] = &publicKeys1D[i*crypto_sign_ed25519_PUBLICKEYBYTES];
   17 |         signatures2D[i] = &signatures1D[i*crypto_sign_ed25519_BYTES];
   18 |     }
```

_file_excerpt · [crypto/batchverifier.c](https://github.com/algorand/go-algorand/blob/e46aea5466a1152af6e08f83555ed16cfcd89f49/crypto/batchverifier.c#L19) · line 19 · SHA-256 344fa4a497b1d60ae81e5280a14389035441d40a200529fe47aaf25add3978e1_

```
   18 |     }
   19 |     return crypto_sign_ed25519_open_batch(messages2D, mlen, publicKeys2D, signatures2D, num, valid);
   20 | }
```

_file_excerpt · [crypto/batchverifier.go](https://github.com/algorand/go-algorand/blob/e46aea5466a1152af6e08f83555ed16cfcd89f49/crypto/batchverifier.go#L190) · line 190 · SHA-256 ea7b3f3856f686d87f900664c6a29a955a057c21c978ddf5c2041bdd93488298_

```
  189 | 	for i := range b.messages {
  190 | 		failed[i] = !ed25519Verify(ed25519PublicKey(b.publicKeys[i]), HashRep(b.messages[i]), ed25519Signature(b.signatures[i]))
  191 | 		if failed[i] {
```

_file_excerpt · [crypto/curve25519.go](https://github.com/algorand/go-algorand/blob/e46aea5466a1152af6e08f83555ed16cfcd89f49/crypto/curve25519.go#L69) · line 69 · SHA-256 afa83fc8ebb8e5135433796dea825b5c4b8b2870b5130df75ad84cd6540f1670_

```
   68 | 	// Check sizes of structs
   69 | 	_ = [C.crypto_sign_ed25519_BYTES]byte(ed25519Signature{})
   70 | 	_ = [C.crypto_sign_ed25519_PUBLICKEYBYTES]byte(ed25519PublicKey{})
```

_file_excerpt · [crypto/curve25519.go](https://github.com/algorand/go-algorand/blob/e46aea5466a1152af6e08f83555ed16cfcd89f49/crypto/curve25519.go#L70) · line 70 · SHA-256 018e47a51afd81189b3c00e21ce83960e6c346043742c6ccb5480cda19b9a82e_

```
   69 | 	_ = [C.crypto_sign_ed25519_BYTES]byte(ed25519Signature{})
   70 | 	_ = [C.crypto_sign_ed25519_PUBLICKEYBYTES]byte(ed25519PublicKey{})
   71 | 	_ = [C.crypto_sign_ed25519_SECRETKEYBYTES]byte(ed25519PrivateKey{})
```

_file_excerpt · [crypto/curve25519.go](https://github.com/algorand/go-algorand/blob/e46aea5466a1152af6e08f83555ed16cfcd89f49/crypto/curve25519.go#L71) · line 71 · SHA-256 fc27b1df9511398d88f72d691b2ea37f60117fb5676662d56714c0ddaccd471e_

```
   70 | 	_ = [C.crypto_sign_ed25519_PUBLICKEYBYTES]byte(ed25519PublicKey{})
   71 | 	_ = [C.crypto_sign_ed25519_SECRETKEYBYTES]byte(ed25519PrivateKey{})
   72 | 	_ = [C.crypto_sign_ed25519_SEEDBYTES]byte(ed25519Seed{})
```

_file_excerpt · [crypto/include/sodium.h](https://github.com/algorand/go-algorand/blob/e46aea5466a1152af6e08f83555ed16cfcd89f49/crypto/include/sodium.h#L42) · line 42 · SHA-256 d7fb5f017dd4fc7fac7bb375353fafd5c14911dcd8f590f64eba84fb28389161_

```
   41 | #include "sodium/crypto_sign.h"
   42 | #include "sodium/crypto_sign_ed25519.h"
   43 | #include "sodium/crypto_stream.h"
```

_file_excerpt · [crypto/include/sodium/crypto_sign.h](https://github.com/algorand/go-algorand/blob/e46aea5466a1152af6e08f83555ed16cfcd89f49/crypto/include/sodium/crypto_sign.h#L13) · line 13 · SHA-256 2c5c152c49d891d97fb78d1f37f1dba5780476cbd4fc91abbc771658776237b2_

```
   12 | 
   13 | #include "crypto_sign_ed25519.h"
   14 | #include "export.h"
```

_file_excerpt · [crypto/include/sodium/crypto_sign.h](https://github.com/algorand/go-algorand/blob/e46aea5466a1152af6e08f83555ed16cfcd89f49/crypto/include/sodium/crypto_sign.h#L28) · line 28 · SHA-256 758b21d19d70a17bfeead26b376bb0046d245252bc35354d6b239f7c7941d3ee_

```
   27 | 
   28 | #define crypto_sign_BYTES crypto_sign_ed25519_BYTES
   29 | SODIUM_EXPORT
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it; introduce an abstraction layer for crypto-agility.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-19626 — Quantum-vulnerable X25519: role not determined (12 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:X25519:general`
- Data source: crypto/include/sodium.h
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.3.0 · 2026-11-06 16:16 UTC
- Priority score: 34.2 / 100
- CVSS v3.1: not applicable

21 reference(s) to X25519 across 12 file(s), e.g. crypto/include/sodium.h:34. Role, judged from paths, function names and nearby code: role not determined. The code does not show what the keys protect; review decides the priority.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open crypto/include/sodium.h:34 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [crypto/include/sodium.h](https://github.com/algorand/go-algorand/blob/e46aea5466a1152af6e08f83555ed16cfcd89f49/crypto/include/sodium.h#L34) · line 34 · SHA-256 1309d78496f4478e5aad9c0b0a2ff383888c6e5db2568d5c032018177c4220d9_

```
   33 | #include "sodium/crypto_pwhash_argon2i.h"
   34 | #include "sodium/crypto_scalarmult.h"
   35 | #include "sodium/crypto_scalarmult_curve25519.h"
```

_file_excerpt · [crypto/include/sodium/crypto_box.h](https://github.com/algorand/go-algorand/blob/e46aea5466a1152af6e08f83555ed16cfcd89f49/crypto/include/sodium/crypto_box.h#L57) · line 57 · SHA-256 1e27fc2ee2b495c03ffc60eb0aec55dd21579565e536b07d5739843e21d2005d_

```
   56 | SODIUM_EXPORT
   57 | int crypto_box_keypair(unsigned char *pk, unsigned char *sk)
   58 |             __attribute__ ((nonnull));
```

_file_excerpt · [crypto/include/sodium/crypto_kx.h](https://github.com/algorand/go-algorand/blob/e46aea5466a1152af6e08f83555ed16cfcd89f49/crypto/include/sodium/crypto_kx.h#L42) · line 42 · SHA-256 293662ab6df380d996d32badde3bebe43c337a3b9eccbe4ef68ea677f3df6206_

```
   41 | SODIUM_EXPORT
   42 | int crypto_kx_keypair(unsigned char pk[crypto_kx_PUBLICKEYBYTES],
   43 |                       unsigned char sk[crypto_kx_SECRETKEYBYTES])
```

_file_excerpt · [crypto/include/sodium/crypto_scalarmult.h](https://github.com/algorand/go-algorand/blob/e46aea5466a1152af6e08f83555ed16cfcd89f49/crypto/include/sodium/crypto_scalarmult.h#L26) · line 26 · SHA-256 8745fe4e6cb7f4eb08a32034eccd5d299356701aff7f413232ceb84898886639_

```
   25 | SODIUM_EXPORT
   26 | int crypto_scalarmult_base(unsigned char *q, const unsigned char *n)
   27 |             __attribute__ ((nonnull));
```

_file_excerpt · [crypto/include/sodium/crypto_scalarmult.h](https://github.com/algorand/go-algorand/blob/e46aea5466a1152af6e08f83555ed16cfcd89f49/crypto/include/sodium/crypto_scalarmult.h#L38) · line 38 · SHA-256 c96703b3a6085f03abf077edaa807e6258886f4a50e0078d268cd8ae799789a1_

```
   37 | SODIUM_EXPORT
   38 | int crypto_scalarmult(unsigned char *q, const unsigned char *n,
   39 |                       const unsigned char *p)
```

_file_excerpt · [crypto/libsodium-fork/src/libsodium/crypto_box/crypto_box.c](https://github.com/algorand/go-algorand/blob/e46aea5466a1152af6e08f83555ed16cfcd89f49/crypto/libsodium-fork/src/libsodium/crypto_box/crypto_box.c#L72) · line 72 · SHA-256 c0013e4cf7927fd70e25378a8286496ad969d4b79b00df8c55a6e5409c688412_

```
   71 | int
   72 | crypto_box_keypair(unsigned char *pk, unsigned char *sk)
   73 | {
```

_file_excerpt · [crypto/libsodium-fork/src/libsodium/crypto_kx/crypto_kx.c](https://github.com/algorand/go-algorand/blob/e46aea5466a1152af6e08f83555ed16cfcd89f49/crypto/libsodium-fork/src/libsodium/crypto_kx/crypto_kx.c#L7) · line 7 · SHA-256 b83e11b5df3ca6749d82125bb5fd506677971c2838c5fa944770caa7bf54b093_

```
    6 | #include "crypto_kx.h"
    7 | #include "crypto_scalarmult.h"
    8 | #include "private/common.h"
```

_file_excerpt · [crypto/libsodium-fork/src/libsodium/crypto_kx/crypto_kx.c](https://github.com/algorand/go-algorand/blob/e46aea5466a1152af6e08f83555ed16cfcd89f49/crypto/libsodium-fork/src/libsodium/crypto_kx/crypto_kx.c#L19) · line 19 · SHA-256 e7a0f139312c3eacae72fffe977326fc3f794ebf892a4122f800b74e7814c806_

```
   18 |                        seed, crypto_kx_SEEDBYTES, NULL, 0);
   19 |     return crypto_scalarmult_base(pk, sk);
   20 | }
```

_file_excerpt · [crypto/libsodium-fork/src/libsodium/crypto_kx/crypto_kx.c](https://github.com/algorand/go-algorand/blob/e46aea5466a1152af6e08f83555ed16cfcd89f49/crypto/libsodium-fork/src/libsodium/crypto_kx/crypto_kx.c#L23) · line 23 · SHA-256 5383dc5a21d6f55f1471d2781d4cf72a3ddd9273156da5e2c116be73263793ca_

```
   22 | int
   23 | crypto_kx_keypair(unsigned char pk[crypto_kx_PUBLICKEYBYTES],
   24 |                   unsigned char sk[crypto_kx_SECRETKEYBYTES])
```

_file_excerpt · [crypto/libsodium-fork/src/libsodium/crypto_scalarmult/crypto_scalarmult.c](https://github.com/algorand/go-algorand/blob/e46aea5466a1152af6e08f83555ed16cfcd89f49/crypto/libsodium-fork/src/libsodium/crypto_scalarmult/crypto_scalarmult.c#L2) · line 2 · SHA-256 9e041e272488a8a0e015c3ed4d2f88cc794e4a4624edd654c3479fd30584e19e_

```
    1 | 
    2 | #include "crypto_scalarmult.h"
    3 | 
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Classify each usage, record data lifetimes, and plan migration to Hybrid key establishment with ML-KEM (FIPS 203), e.g. X25519MLKEM768 in TLS 1.3 or mlkem768x25519-sha256 in SSH; introduce an abstraction layer for crypto-agility.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-19629 — Quantum-vulnerable ECDH: role not determined (4 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:ECDH:general`
- Data source: crypto/secp256k1/libsecp256k1/include/secp256k1_ecdh.h
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.3.0 · 2026-11-06 16:16 UTC
- Priority score: 34.2 / 100
- CVSS v3.1: not applicable

7 reference(s) to ECDH across 4 file(s), e.g. crypto/secp256k1/libsecp256k1/include/secp256k1_ecdh.h:20. Role, judged from paths, function names and nearby code: role not determined. The code does not show what the keys protect; review decides the priority.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open crypto/secp256k1/libsecp256k1/include/secp256k1_ecdh.h:20 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [crypto/secp256k1/libsecp256k1/include/secp256k1_ecdh.h](https://github.com/algorand/go-algorand/blob/e46aea5466a1152af6e08f83555ed16cfcd89f49/crypto/secp256k1/libsecp256k1/include/secp256k1_ecdh.h#L20) · line 20 · SHA-256 7bd6ded8d3e8bdd26a80745ab082f8e2b2bc76aba765e7c5371b4a7b62856859_

```
   19 |  */
   20 | SECP256K1_API SECP256K1_WARN_UNUSED_RESULT int secp256k1_ecdh(
   21 |   const secp256k1_context* ctx,
```

_file_excerpt · [crypto/secp256k1/libsecp256k1/src/java/org/bitcoin/NativeSecp256k1.java](https://github.com/algorand/go-algorand/blob/e46aea5466a1152af6e08f83555ed16cfcd89f49/crypto/secp256k1/libsecp256k1/src/java/org/bitcoin/NativeSecp256k1.java#L381) · line 381 · SHA-256 4a76b0ce27748a15ca0e3e6b2cb0a15274c7f0223f35a07f4f936d6223fe487f_

```
  380 |         try {
  381 |           retByteArray = secp256k1_ecdh(byteBuff, Secp256k1Context.getContext(), pubkey.length);
  382 |         } finally {
```

_file_excerpt · [crypto/secp256k1/libsecp256k1/src/java/org/bitcoin/NativeSecp256k1.java](https://github.com/algorand/go-algorand/blob/e46aea5466a1152af6e08f83555ed16cfcd89f49/crypto/secp256k1/libsecp256k1/src/java/org/bitcoin/NativeSecp256k1.java#L444) · line 444 · SHA-256 52bb0a81453030eb358a05efe7baf739a9f100114325d74964bb5de4a37e3238_

```
  443 | 
  444 |     private static native byte[][] secp256k1_ecdh(ByteBuffer byteBuff, long context, int inputLen);
  445 | 
```

_file_excerpt · [crypto/secp256k1/libsecp256k1/src/java/org_bitcoin_NativeSecp256k1.c](https://github.com/algorand/go-algorand/blob/e46aea5466a1152af6e08f83555ed16cfcd89f49/crypto/secp256k1/libsecp256k1/src/java/org_bitcoin_NativeSecp256k1.c#L6) · line 6 · SHA-256 784f99e7ba1dbc2b27f568c918afd301e67b538fc3a902c7c7bb361b48f08f61_

```
    5 | #include "include/secp256k1.h"
    6 | #include "include/secp256k1_ecdh.h"
    7 | #include "include/secp256k1_recovery.h"
```

_file_excerpt · [crypto/secp256k1/libsecp256k1/src/java/org_bitcoin_NativeSecp256k1.c](https://github.com/algorand/go-algorand/blob/e46aea5466a1152af6e08f83555ed16cfcd89f49/crypto/secp256k1/libsecp256k1/src/java/org_bitcoin_NativeSecp256k1.c#L352) · line 352 · SHA-256 02bddc556cf14d4de17abde58b6d40be5bea351f497d70f02d7e8d6b7614dbbf_

```
  351 |   if (ret) {
  352 |     ret = secp256k1_ecdh(
  353 |       ctx,
```

_file_excerpt · [crypto/secp256k1/libsecp256k1/src/modules/ecdh/main_impl.h](https://github.com/algorand/go-algorand/blob/e46aea5466a1152af6e08f83555ed16cfcd89f49/crypto/secp256k1/libsecp256k1/src/modules/ecdh/main_impl.h#L10) · line 10 · SHA-256 4f4e28aaaf190882449bce7f9351d198fc68226dc29e2747a0e7042951b20ccf_

```
    9 | 
   10 | #include "include/secp256k1_ecdh.h"
   11 | #include "ecmult_const_impl.h"
```

_file_excerpt · [crypto/secp256k1/libsecp256k1/src/modules/ecdh/main_impl.h](https://github.com/algorand/go-algorand/blob/e46aea5466a1152af6e08f83555ed16cfcd89f49/crypto/secp256k1/libsecp256k1/src/modules/ecdh/main_impl.h#L13) · line 13 · SHA-256 f443a95be4ed06fa46d362a64da496bd6eac33c4572a5ae8c109407103db4bee_

```
   12 | 
   13 | int secp256k1_ecdh(const secp256k1_context* ctx, unsigned char *result, const secp256k1_pubkey *point, const unsigned char *scalar) {
   14 |     int ret = 0;
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Classify each usage, record data lifetimes, and plan migration to Hybrid key establishment with ML-KEM (FIPS 203), e.g. X25519MLKEM768 in TLS 1.3 or mlkem768x25519-sha256 in SSH; introduce an abstraction layer for crypto-agility.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-19632 — Quantum-vulnerable RSA: role not determined (1 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:RSA:general`
- Data source: tools/network/dnssec/testHarness.go
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.3.0 · 2026-11-06 16:16 UTC
- Priority score: 34.2 / 100
- CVSS v3.1: not applicable

1 reference(s) to RSA across 1 file(s), e.g. tools/network/dnssec/testHarness.go:22. Role, judged from paths, function names and nearby code: role not determined. The code does not show what the keys protect; review decides the priority.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open tools/network/dnssec/testHarness.go:22 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [tools/network/dnssec/testHarness.go](https://github.com/algorand/go-algorand/blob/e46aea5466a1152af6e08f83555ed16cfcd89f49/tools/network/dnssec/testHarness.go#L22) · line 22 · SHA-256 824218641afe5125959cff6bf8001fa964d81c801cf155ea4e59777074ca1197_

```
   21 | 	"crypto"
   22 | 	"crypto/rsa"
   23 | 	"fmt"
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it; introduce an abstraction layer for crypto-agility.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-19637 — github.com/libp2p/go-libp2p-kad-dht v0.38.0 is affected by GO-2024-3218 (CVE-2023-26248) (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:Go/github.com/libp2p/go-libp2p-kad-dht@v0.38.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 16:16 UTC
- Priority score: 20.3 / 100
- CVSS v3.1: not applicable

OSV.dev reports GO-2024-3218 (CVE-2023-26248) for Go package github.com/libp2p/go-libp2p-kad-dht at version v0.38.0: Content Censorship in the InterPlanetary File System (IPFS) via Kademlia DHT abuse in github.com/libp2p/go-libp2p-kad-dht. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2024-3218
```

**Evidence.**

_tool_output · [OSV.dev GO-2024-3218](https://osv.dev/vulnerability/GO-2024-3218) · line 39 · SHA-256 78f9da1b356c08bee7ef24aa1bfb035506cd473a70773029d64f3f7a072166bc_

```
{"id": "GO-2024-3218", "aliases": ["CVE-2023-26248", "GHSA-mqr9-hjr8-2m9w"], "modified": "2026-07-01T14:59:24.616695200Z", "summary": "Content Censorship in the InterPlanetary File System (IPFS) via Kademlia DHT abuse in github.com/libp2p/go-libp2p-kad-dht", "severity": null, "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed. A Go function counts only in a file that also names its package (a method: its type); unexported functions only through the exported ones.

**Recommendation.** Triage the advisory; upgrade to a fixed version (none published yet; see the advisory for mitigations) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-19638 — golang.org/x/crypto v0.57.0 is affected by GO-2026-5932 (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:Go/golang.org/x/crypto@v0.57.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 16:16 UTC
- Priority score: 20.3 / 100
- CVSS v3.1: not applicable

OSV.dev reports GO-2026-5932 for Go package golang.org/x/crypto at version v0.57.0: The golang.org/x/crypto/openpgp package is unmaintained, unsafe by design, and has known security issues. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-5932
```

**Evidence.**

_tool_output · [OSV.dev GO-2026-5932](https://osv.dev/vulnerability/GO-2026-5932) · line 59 · SHA-256 79b7a13fb7767fbace049b5199d913b96ffabce881fc497fd2222d40644da151_

```
{"id": "GO-2026-5932", "aliases": [], "modified": "2026-11-02T22:15:06.677088389Z", "summary": "The golang.org/x/crypto/openpgp package is unmaintained, unsafe by design, and has known security issues", "severity": null, "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed. A Go function counts only in a file that also names its package (a method: its type); unexported functions only through the exported ones.

**Recommendation.** Triage the advisory; upgrade to a fixed version (0.58.1-0.20261009181718-2f1f834330b2) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-19644 — golang.org/x/net v0.60.0 is affected by GO-2026-6860 (CVE-2026-78661) (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:Go/golang.org/x/net@v0.60.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 16:16 UTC
- Priority score: 20.3 / 100
- CVSS v3.1: not applicable

OSV.dev reports GO-2026-6860 (CVE-2026-78661) for Go package golang.org/x/net at version v0.60.0: Avoid quadratic complexity when coalescing text nodes in html in golang.org/x/net. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. The audited code names golang.org/x/net/html.Parse: the affected code may be reachable.

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-6860
```

**Evidence.**

_tool_output · [OSV.dev GO-2026-6860](https://osv.dev/vulnerability/GO-2026-6860) · line 187 · SHA-256 1f106c45371219bac0158f7ce44e57c439f50f0c32898616d1563f14cadb1b28_

```
{"id": "GO-2026-6860", "aliases": ["CVE-2026-78661"], "modified": "2026-10-27T21:30:04.890809062Z", "summary": "Avoid quadratic complexity when coalescing text nodes in html in golang.org/x/net", "severity": null, "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed. A Go function counts only in a file that also names its package (a method: its type); unexported functions only through the exported ones.

**Recommendation.** Triage the advisory; upgrade to a fixed version (0.62.0) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-19639 — github.com/ipld/go-ipld-prime v0.22.0 is affected by GHSA-w239-58x2-q8p5 (CVE-2026-42328, GO-2026-5684)

- Severity: **Info** · Classification: Known vulnerable component · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `dependency:Go/github.com/ipld/go-ipld-prime@v0.22.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 16:16 UTC
- Priority score: 29.9 / 100
- CVSS v3.1: 6.2 (`CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev reports GHSA-w239-58x2-q8p5 (CVE-2026-42328, GO-2026-5684) for Go package github.com/ipld/go-ipld-prime at version v0.22.0: go-ipld-prime's DAG-CBOR and DAG-JSON decoders have unbounded recursion depth. None of the affected functions (github.com/ipld/go-ipld-prime/codec/dagcbor.Decode, github.com/ipld/go-ipld-prime/codec/dagjson.Decode) is named in the audited code: the advisory does not apply unless they are reached indirectly (traits, macros, other dependencies).

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-w239-58x2-q8p5
```

**Evidence.**

_tool_output · [OSV.dev GHSA-w239-58x2-q8p5](https://osv.dev/vulnerability/GHSA-w239-58x2-q8p5) · line 98 · SHA-256 b44ed07f6b64987651ff3895cb0a445f799c9895da4ab3dbb4b4672babf473f4_

```
{"id": "GHSA-w239-58x2-q8p5", "aliases": ["CVE-2026-42328", "GO-2026-5684"], "modified": "2026-09-10T03:51:07.104837244Z", "summary": "go-ipld-prime's DAG-CBOR and DAG-JSON decoders have unbounded recursion depth", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed. A Go function counts only in a file that also names its package (a method: its type); unexported functions only through the exported ones.

**Recommendation.** Upgrade to a fixed version (0.23.0).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-19640 — github.com/klauspost/compress v1.18.0 is affected by GHSA-259r-337f-4rfw (CVE-2026-63209, GO-2026-5841)

- Severity: **Info** · Classification: Known vulnerable component · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `dependency:Go/github.com/klauspost/compress@v1.18.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 16:16 UTC
- Priority score: 29.9 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev reports GHSA-259r-337f-4rfw (CVE-2026-63209, GO-2026-5841) for Go package github.com/klauspost/compress at version v1.18.0: Compress/s2: Integer Overflow or Wraparound and Out-of-bounds Write in compress. None of the affected functions (github.com/klauspost/compress/s2.NewDict) is named in the audited code: the advisory does not apply unless they are reached indirectly (traits, macros, other dependencies).

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-259r-337f-4rfw
```

**Evidence.**

_tool_output · [OSV.dev GHSA-259r-337f-4rfw](https://osv.dev/vulnerability/GHSA-259r-337f-4rfw) · line 104 · SHA-256 b415f1a2f3e954680bf032db6b47454a035b6a2af6b7a5a152588cc24bafce59_

```
{"id": "GHSA-259r-337f-4rfw", "aliases": ["CVE-2026-63209", "GO-2026-5841"], "modified": "2026-10-20T14:45:03.782718646Z", "summary": "Compress/s2: Integer Overflow or Wraparound and Out-of-bounds Write in compress", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed. A Go function counts only in a file that also names its package (a method: its type); unexported functions only through the exported ones.

**Recommendation.** Upgrade to a fixed version (1.18.7).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-19633 — github.com/aws/aws-sdk-go v1.34.0 is affected by GO-2022-0635 (CVE-2020-8912) (no severity rating)

- Severity: **Info** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:Go/github.com/aws/aws-sdk-go@v1.34.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 16:16 UTC
- Priority score: 17.8 / 100
- CVSS v3.1: not applicable

OSV.dev reports GO-2022-0635 (CVE-2020-8912) for Go package github.com/aws/aws-sdk-go at version v1.34.0: In-band key negotiation issue in AWS S3 Crypto SDK for golang in github.com/aws/aws-sdk-go. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. None of the affected functions (github.com/aws/aws-sdk-go/service/s3/s3crypto.NewDecryptionClient, github.com/aws/aws-sdk-go/service/s3/s3crypto.NewEncryptionClient) is named in the audited code: the advisory does not apply unless they are reached indirectly (traits, macros, other dependencies).

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2022-0635
```

**Evidence.**

_tool_output · [OSV.dev GO-2022-0635](https://osv.dev/vulnerability/GO-2022-0635) · line 19 · SHA-256 d352230690501c3365a82d0d1228c54072b67fb8cd2c7dcb18f30e6095515321_

```
{"id": "GO-2022-0635", "aliases": ["CVE-2020-8912", "GHSA-7f33-f4f5-xwgw"], "modified": "2026-02-04T02:41:58.893164Z", "summary": "In-band key negotiation issue in AWS S3 Crypto SDK for golang in github.com/aws/aws-sdk-go", "severity": null, "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed. A Go function counts only in a file that also names its package (a method: its type); unexported functions only through the exported ones.

**Recommendation.** Triage the advisory; upgrade to a fixed version (none published yet; see the advisory for mitigations) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-19634 — github.com/aws/aws-sdk-go v1.34.0 is affected by GO-2022-0646 (CVE-2020-8911) (no severity rating)

- Severity: **Info** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:Go/github.com/aws/aws-sdk-go@v1.34.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 16:16 UTC
- Priority score: 17.8 / 100
- CVSS v3.1: not applicable

OSV.dev reports GO-2022-0646 (CVE-2020-8911) for Go package github.com/aws/aws-sdk-go at version v1.34.0: CBC padding oracle issue in AWS S3 Crypto SDK for golang in github.com/aws/aws-sdk-go. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. None of the affected functions (github.com/aws/aws-sdk-go/service/s3/s3crypto.NewDecryptionClient, github.com/aws/aws-sdk-go/service/s3/s3crypto.NewEncryptionClient) is named in the audited code: the advisory does not apply unless they are reached indirectly (traits, macros, other dependencies).

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2022-0646
```

**Evidence.**

_tool_output · [OSV.dev GO-2022-0646](https://osv.dev/vulnerability/GO-2022-0646) · line 19 · SHA-256 0b50371b3e3532b7898cbcffed92e00b995bf8a26a80eb19412cc904ad3ef99e_

```
{"id": "GO-2022-0646", "aliases": ["CVE-2020-8911", "GHSA-f5pg-7wfw-84q9"], "modified": "2026-02-04T02:16:32.066930Z", "summary": "CBC padding oracle issue in AWS S3 Crypto SDK for golang in github.com/aws/aws-sdk-go", "severity": null, "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed. A Go function counts only in a file that also names its package (a method: its type); unexported functions only through the exported ones.

**Recommendation.** Triage the advisory; upgrade to a fixed version (none published yet; see the advisory for mitigations) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-19641 — github.com/klauspost/compress v1.18.0 is affected by GO-2026-6865 (CVE-2026-116591) (no severity rating)

- Severity: **Info** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:Go/github.com/klauspost/compress@v1.18.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 16:16 UTC
- Priority score: 17.8 / 100
- CVSS v3.1: not applicable

OSV.dev reports GO-2026-6865 (CVE-2026-116591) for Go package github.com/klauspost/compress at version v1.18.0: Panic on two-block frames in github.com/klauspost/compress. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. None of the affected functions (github.com/klauspost/compress/fse.Compress, github.com/klauspost/compress/fse.Decompress, github.com/klauspost/compress/fse.Scratch.readNCount, github.com/klauspost/compress/fse.Scratch.validateNorm, github.com/klauspost/compress/huff0.Compress1X, github.com/klauspost/compress/huff0.Compress4X …) is named in the audited code: the advisory does not apply unless they are reached indirectly (traits, macros, other dependencies).

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-6865
```

**Evidence.**

_tool_output · [OSV.dev GO-2026-6865](https://osv.dev/vulnerability/GO-2026-6865) · line 104 · SHA-256 0b28910de38174fa37f4effdc4bf67a0c4fde17b0041a6b33f42cfa03de9b455_

```
{"id": "GO-2026-6865", "aliases": ["CVE-2026-116591", "GHSA-fpmh-frq8-7rj8"], "modified": "2026-11-05T23:15:14.472777299Z", "summary": "Panic on two-block frames in github.com/klauspost/compress", "severity": null, "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed. A Go function counts only in a file that also names its package (a method: its type); unexported functions only through the exported ones.

**Recommendation.** Triage the advisory; upgrade to a fixed version (1.20.2) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-19645 — golang.org/x/net v0.60.0 is affected by GO-2026-6866 (CVE-2026-97045) (no severity rating)

- Severity: **Info** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:Go/golang.org/x/net@v0.60.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 16:16 UTC
- Priority score: 17.8 / 100
- CVSS v3.1: not applicable

OSV.dev reports GO-2026-6866 (CVE-2026-97045) for Go package golang.org/x/net at version v0.60.0: Check all ancestor namespace transitions when rendering raw text in html in golang.org/x/net. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. None of the affected functions (golang.org/x/net/html.Render, golang.org/x/net/html.childTextNodesAreLiteral) is named in the audited code: the advisory does not apply unless they are reached indirectly (traits, macros, other dependencies).

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-6866
```

**Evidence.**

_tool_output · [OSV.dev GO-2026-6866](https://osv.dev/vulnerability/GO-2026-6866) · line 187 · SHA-256 102267a016bc5eef7979a90b1ddd2288ff36b09ab6fa040c808e62f3b55c1f42_

```
{"id": "GO-2026-6866", "aliases": ["CVE-2026-97045"], "modified": "2026-10-27T21:45:08.978077289Z", "summary": "Check all ancestor namespace transitions when rendering raw text in html in golang.org/x/net", "severity": null, "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed. A Go function counts only in a file that also names its package (a method: its type); unexported functions only through the exported ones.

**Recommendation.** Triage the advisory; upgrade to a fixed version (0.62.0) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-19646 — github.com/klauspost/compress v1.18.7 is affected by GO-2026-6865 (CVE-2026-116591) (no severity rating)

- Severity: **Info** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:Go/github.com/klauspost/compress@v1.18.7`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 16:16 UTC
- Priority score: 17.8 / 100
- CVSS v3.1: not applicable

OSV.dev reports GO-2026-6865 (CVE-2026-116591) for Go package github.com/klauspost/compress at version v1.18.7: Panic on two-block frames in github.com/klauspost/compress. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. None of the affected functions (github.com/klauspost/compress/fse.Compress, github.com/klauspost/compress/fse.Decompress, github.com/klauspost/compress/fse.Scratch.readNCount, github.com/klauspost/compress/fse.Scratch.validateNorm, github.com/klauspost/compress/huff0.Compress1X, github.com/klauspost/compress/huff0.Compress4X …) is named in the audited code: the advisory does not apply unless they are reached indirectly (traits, macros, other dependencies).

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-6865
```

**Evidence.**

_tool_output · [OSV.dev GO-2026-6865](https://osv.dev/vulnerability/GO-2026-6865) · line 11 · SHA-256 0b28910de38174fa37f4effdc4bf67a0c4fde17b0041a6b33f42cfa03de9b455_

```
{"id": "GO-2026-6865", "aliases": ["CVE-2026-116591", "GHSA-fpmh-frq8-7rj8"], "modified": "2026-11-05T23:15:14.472777299Z", "summary": "Panic on two-block frames in github.com/klauspost/compress", "severity": null, "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed. A Go function counts only in a file that also names its package (a method: its type); unexported functions only through the exported ones.

**Recommendation.** Triage the advisory; upgrade to a fixed version (1.20.2) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.


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

### Post-quantum maturity: Level 2 of 4 — post-quantum in use outside the critical paths

- In use: FN-DSA — data/transactions/logic/doc.go
- In use: FN-DSA — data/transactions/logic/opcodes.go
- Present, not wired: FN-DSA — crypto/falconWrapper.go
- Classical only — key wrapping and data encryption at rest: X25519 (1 file(s))

**Next step:** Extend post-quantum protection to the critical roles that stay classical, starting with what can be recorded today (wrapped keys, channel key exchange).

_Levels: 0 none; 1 present, not wired; 2 in use outside the critical paths; 3 hybrid in a critical path; 4 post-quantum by default in the critical paths (root of trust, key wrapping, channel key exchange). Judged from code and manifests._

### What the quantum-vulnerable algorithms do

| Role | Algorithms (files) | ID | First step |
|---|---|---|---|
| **key wrapping and data encryption at rest** | X25519 (1) | QSI-2026-19627 | Wrap keys with ML-KEM or a hybrid KEM (X25519 + ML-KEM-768) and re-wrap the stored keys; data that may already have been copied needs its own assessment |
| **transaction and message signing** | ECDSA (26) | QSI-2026-19628 | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains adopt them |
| **role not determined** | Ed25519 (19), X25519 (12), ECDH (4), RSA (1) | QSI-2026-19625, QSI-2026-19626, QSI-2026-19629, QSI-2026-19632 | Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it; introduce an abstraction layer for crypto-agility |

_Roles are judged from file paths, function names and the code around each match; review confirms them. Root-of-trust keys and wrapped keys come first: they are hard to replace or can be recorded today._
No readiness questionnaire was completed for this project.

### Quantum algorithms relevant to this inventory

| Quantum algorithm | Effect | Attack model | Inventoried algorithms (rows) | What it means for this audit |
|---|---|---|---|---|
| Shor's algorithm — factoring | breaks | Q1 | RSA (3) | Breaks RSA at every key length: a longer modulus only raises the cost polynomially. Plan migration to ML-KEM (or a hybrid) for key establishment and ML-DSA / SLH-DSA for signatures; start with keys protecting data that must stay confidential for years (harvest now, decrypt later) and with long-lived signatures. |
| Shor's algorithm — elliptic-curve discrete logarithms | breaks | Q1 | ECDH (4), ECDSA (41), Ed25519 (32), X25519 (22) | Elliptic-curve keys are expected to fall before RSA keys of comparable classical strength. On blockchains, coins whose public key is already on chain (reused addresses, pay-to-public-key and Taproot outputs) are exposed first; plan the move to post-quantum signatures and avoid key reuse in the meantime. |
| Grover's algorithm — key search and preimages | weakens (larger keys restore the margin) | Q1 | AES-256 (3), Argon2 (21), BLAKE2 (33), ChaCha20-Poly1305 (28), HKDF (1), HMAC (6), Keccak-256 (2), PBKDF2 (2), Poly1305 (21), Poseidon (5), SHA-2 (25), SHA-3 (2), SHAKE (1), XSalsa20-Poly1305 (43), scrypt (4) | Not a break. 256-bit keys (AES-256, ChaCha20) keep a comfortable margin; AES-128 meets NIST category 1, while some authorities ask for 256-bit keys in quantum-resistant contexts (see the AES-128 entry). Prefer 256-bit keys for long-lived data; 256-bit hashes need no change for preimage resistance. |
| Brassard–Høyer–Tapp — collision search | weakens (larger keys restore the margin) | Q1 | BLAKE2 (33), Keccak-256 (2), Poseidon (5), SHA-2 (25), SHA-3 (2), SHAKE (1) | 256-bit hashes (SHA-256, SHA3-256) remain adequate for collision resistance; 160-bit hashes are already weak classically (SHA-1 collisions are practical). Use 384/512-bit hashes where NIST categories 4–5 are required. |
| Quantum lattice sieving | included in standard parameters | Q1 | FN-DSA (3) | No change for ML-KEM or ML-DSA at the standard parameter sets. A 2024 claim of a polynomial-time quantum LWE algorithm was withdrawn after a bug was found (see claims). |

_Effects: breaks — replace the algorithm; weakens — larger keys or outputs restore the margin; included in standard parameters — no action at standard parameter sets; only with superposition queries — not applicable to ordinary deployments._


## 9. Limitations and assumptions

- This report presents automated and documented analysis results for the stated scope. It is not a legal opinion, a certification or an attestation of compliance with any standard.
- z is a planning assumption chosen per risk profile, not a prediction. A cryptographically relevant quantum computer is not publicly known to exist today.

## 10. Remediation plan / Priorities for 30, 60 and 90 days

### 30 days

| Priority | ID | Action | Type | Closure criteria |
|---|---|---|---|---|
| P1 | QSI-2026-19631 | Rotate and remove secrets found in logging/telemetryConfig.go. | root-cause fix | Secret scanner reports no secrets; old values revoked. |
| P2 | QSI-2026-19635 | Upgrade github.com/labstack/echo/v4 to a fixed version (none published yet; see the advisory for mitigations). | root-cause fix | Dependency scan no longer reports GHSA-246p-cpwv-v3jq (CVE-2026-118653, GO-2026-6872). |
| P2 | QSI-2026-19636 | Upgrade github.com/labstack/echo/v4 to a fixed version (none published yet; see the advisory for mitigations). | root-cause fix | Dependency scan no longer reports GHSA-99jh-6h7p-pp36 (CVE-2026-118651, GO-2026-6875). |
| P2 | QSI-2026-19642 | Upgrade github.com/pion/dtls/v2 to a fixed version (none published yet; see the advisory for mitigations). | root-cause fix | Dependency scan no longer reports GHSA-9f3f-wv7r-qc8r (CVE-2026-26014, GO-2026-4479). |
| P2 | QSI-2026-19643 | Upgrade github.com/pion/stun to a fixed version (none published yet; see the advisory for mitigations). | root-cause fix | Dependency scan no longer reports GHSA-34rh-wp3j-6cxc (CVE-2026-54909). |
| P2 | QSI-2026-19639 | Upgrade github.com/ipld/go-ipld-prime to a fixed version (0.23.0). | root-cause fix | Dependency scan no longer reports GHSA-w239-58x2-q8p5 (CVE-2026-42328, GO-2026-5684). |
| P2 | QSI-2026-19640 | Upgrade github.com/klauspost/compress to a fixed version (1.18.7). | root-cause fix | Dependency scan no longer reports GHSA-259r-337f-4rfw (CVE-2026-63209, GO-2026-5841). |
### 60 days

| Priority | ID | Action | Type | Closure criteria |
|---|---|---|---|---|
| P3 | QSI-2026-19637 | Triage GO-2024-3218 (CVE-2023-26248); upgrade github.com/libp2p/go-libp2p-kad-dht to a fixed version (none published yet; see the advisory for mitigations) if it applies. | root-cause fix | Dependency scan no longer reports GO-2024-3218 (CVE-2023-26248), or the triage is recorded. |
| P3 | QSI-2026-19638 | Triage GO-2026-5932; upgrade golang.org/x/crypto to a fixed version (0.58.1-0.20261009181718-2f1f834330b2) if it applies. | root-cause fix | Dependency scan no longer reports GO-2026-5932, or the triage is recorded. |
| P3 | QSI-2026-19644 | Triage GO-2026-6860 (CVE-2026-78661); upgrade golang.org/x/net to a fixed version (0.62.0) if it applies. | root-cause fix | Dependency scan no longer reports GO-2026-6860 (CVE-2026-78661), or the triage is recorded. |
| P3 | QSI-2026-19633 | Triage GO-2022-0635 (CVE-2020-8912); upgrade github.com/aws/aws-sdk-go to a fixed version (none published yet; see the advisory for mitigations) if it applies. | root-cause fix | Dependency scan no longer reports GO-2022-0635 (CVE-2020-8912), or the triage is recorded. |
| P3 | QSI-2026-19634 | Triage GO-2022-0646 (CVE-2020-8911); upgrade github.com/aws/aws-sdk-go to a fixed version (none published yet; see the advisory for mitigations) if it applies. | root-cause fix | Dependency scan no longer reports GO-2022-0646 (CVE-2020-8911), or the triage is recorded. |
| P3 | QSI-2026-19641 | Triage GO-2026-6865 (CVE-2026-116591); upgrade github.com/klauspost/compress to a fixed version (1.20.2) if it applies. | root-cause fix | Dependency scan no longer reports GO-2026-6865 (CVE-2026-116591), or the triage is recorded. |
| P3 | QSI-2026-19645 | Triage GO-2026-6866 (CVE-2026-97045); upgrade golang.org/x/net to a fixed version (0.62.0) if it applies. | root-cause fix | Dependency scan no longer reports GO-2026-6866 (CVE-2026-97045), or the triage is recorded. |
| P3 | QSI-2026-19646 | Triage GO-2026-6865 (CVE-2026-116591); upgrade github.com/klauspost/compress to a fixed version (1.20.2) if it applies. | root-cause fix | Dependency scan no longer reports GO-2026-6865 (CVE-2026-116591), or the triage is recorded. |
### 90 days

| Priority | ID | Action | Type | Closure criteria |
|---|---|---|---|---|
| P3 | QSI-2026-19630 | Add RSA usages at file:installer/rpm/RPM-GPG-KEY-Algorand to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-19627 | Add X25519 usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-19628 | Add ECDSA usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-19625 | Add Ed25519 usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-19626 | Add X25519 usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-19629 | Add ECDH usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-19632 | Add RSA usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P4 | QSI-2026-19630 | Plan migration of RSA to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. or a hybrid scheme in use. |
| P4 | QSI-2026-19627 | Plan migration of X25519 to Hybrid key establishment with ML-KEM (FIPS 203), e.g. X25519MLKEM768 in TLS 1.3 or mlkem768x25519-sha256 in SSH (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows Hybrid key establishment with ML-KEM (FIPS 203), e.g. X25519MLKEM768 in TLS 1.3 or mlkem768x25519-sha256 in SSH or a hybrid scheme in use. |
| P4 | QSI-2026-19628 | Plan migration of ECDSA to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-19625 | Plan migration of Ed25519 to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-19626 | Plan migration of X25519 to Hybrid key establishment with ML-KEM (FIPS 203), e.g. X25519MLKEM768 in TLS 1.3 or mlkem768x25519-sha256 in SSH (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows Hybrid key establishment with ML-KEM (FIPS 203), e.g. X25519MLKEM768 in TLS 1.3 or mlkem768x25519-sha256 in SSH or a hybrid scheme in use. |
| P4 | QSI-2026-19629 | Plan migration of ECDH to Hybrid key establishment with ML-KEM (FIPS 203), e.g. X25519MLKEM768 in TLS 1.3 or mlkem768x25519-sha256 in SSH (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows Hybrid key establishment with ML-KEM (FIPS 203), e.g. X25519MLKEM768 in TLS 1.3 or mlkem768x25519-sha256 in SSH or a hybrid scheme in use. |
| P4 | QSI-2026-19632 | Plan migration of RSA to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |

## 11. Tools used

- blockchain 1.0.0
- certificates 1.2.0
- chain_map 1.0.0
- configs 1.1.0
- dependencies 1.3.0
- inventory_document 1.1.0
- solidity 1.3.0
- source_code 1.4.0
- tls_code 1.1.0
- tls_live 1.0.0
- qsi-engine 1.3.0
- OSV.dev API v1

## 12. Sources and normative documents

1. A. Becker, L. Ducas, N. Gama, T. Laarhoven — New directions in nearest neighbor searching with applications to lattice sieving (SODA 2016; IACR ePrint 2015/1128) — IACR ePrint. <https://eprint.iacr.org/2015/1128> (peer-reviewed article: classical sieving in 2^{0.292n + o(n)})
2. A. Chailloux, J. Loyer — Lattice sieving via quantum random walks (ASIACRYPT 2021; IACR ePrint 2021/570) — IACR ePrint. <https://eprint.iacr.org/2021/570> (peer-reviewed article: 2^{0.2570d + o(d)}, previously 2^{0.2653d + o(d)} (Laarhoven))
3. A. Chailloux, M. Naya-Plasencia, A. Schrottenloher — An Efficient Quantum Collision Search Algorithm and Implications on Symmetric Cryptography (ASIACRYPT 2017; IACR ePrint 2017/847) — IACR ePrint. <https://eprint.iacr.org/2017/847> (peer-reviewed article: Õ(2^{2n/5}) time, O(n) qubits, Õ(2^{n/5}) classical memory)
4. C. Chevignard, P.-A. Fouque, A. Schrottenloher — Reducing the Number of Qubits in Quantum Discrete Logarithms on Elliptic Curves (IACR ePrint 2026/280) — IACR ePrint. <https://eprint.iacr.org/2026/280> (revision of a EUROCRYPT 2026 paper: 3.12n + o(n) qubits; for n = 256, 1193 qubits and 22 runs of 2^38.98 Toffoli gates)
5. C. Gidney — How to factor 2048 bit RSA integers with less than a million noisy qubits (arXiv:2505.15917) — arXiv. <https://arxiv.org/abs/2505.15917> (preprint (2025-05-21): < 1 million noisy qubits, < 1 week, 0.1% gate error, 1 µs surface-code cycle)
6. C. Gidney, M. Ekerå — How to factor 2048 bit RSA integers in 8 hours using 20 million noisy qubits (Quantum 5, 433) — Quantum. <https://doi.org/10.22331/q-2021-04-15-433> (peer-reviewed article (2021): 10^-3 gate error, 1 µs cycle, 10 µs reaction time)
7. C. Zalka — Grover's quantum searching algorithm is optimal (Phys. Rev. A 60, 2746, 1999; arXiv:quant-ph/9711070) — APS. <https://doi.org/10.1103/PhysRevA.60.2746> (peer-reviewed article: optimal for any success probability; parallel search gains no more than splitting the space)
8. CRYSTALS-Kyber — Algorithm Specifications and Supporting Documentation (round 3, 2021-08-04) — CRYSTALS team. <https://pq-crystals.org/kyber/data/kyber-specification-round3-20210804.pdf> (NIST round-3 submission: core-SVP cost 2^{0.292β} classical, 2^{0.265β} quantum; Kyber768 166 quantum bits)
9. Common Vulnerability Scoring System v3.1: Specification Document — FIRST. <https://www.first.org/cvss/v3.1/specification-document> (final)
10. D. J. Bernstein — Cost analysis of hash collisions: Will quantum computers make SHARCS obsolete? (2009) — cr.yp.to. <https://cr.yp.to/hash/collisioncost-20090823.pdf> (paper dated 2009-08-23)
11. D. Litinski — How to compute a 256-bit elliptic curve private key with only 50 million Toffoli gates (arXiv:2306.08585) — arXiv. <https://arxiv.org/abs/2306.08585> (preprint (2023-06-14): 6000 modules × 1152 physical qubits, one key per 10 minutes under its architecture assumptions)
12. FIPS 203 — Module-Lattice-Based Key-Encapsulation Mechanism Standard (ML-KEM) — NIST. <https://csrc.nist.gov/pubs/fips/203/final> (final (August 2024))
13. FIPS 204 — Module-Lattice-Based Digital Signature Standard (ML-DSA) — NIST. <https://csrc.nist.gov/pubs/fips/204/final> (final (August 2024))
14. FIPS 205 — Stateless Hash-Based Digital Signature Standard (SLH-DSA) — NIST. <https://csrc.nist.gov/pubs/fips/205/final> (final (August 2024))
15. G. Brassard, P. Høyer, A. Tapp — Quantum Algorithm for the Collision Problem (LATIN '98; arXiv:quant-ph/9705002) — Springer / arXiv. <https://arxiv.org/abs/quant-ph/9705002> (peer-reviewed article: collisions of r-to-one functions in O((N/r)^{1/3}) expected evaluations)
16. J. Proos, C. Zalka — Shor's discrete logarithm quantum algorithm for elliptic curves (Quantum Inf. Comput. 3(4), 2003; arXiv:quant-ph/0301141) — Quantum Information & Computation. <https://doi.org/10.26421/QIC3.4-3> (peer-reviewed article)
17. L. K. Grover — A fast quantum mechanical algorithm for database search (STOC 1996) — ACM. <https://doi.org/10.1145/237814.237866> (peer-reviewed article)
18. M. Amy et al. — Estimating the cost of generic quantum pre-image attacks on SHA-2 and SHA-3 (SAC 2016; arXiv:1603.09383) — Springer / arXiv. <https://arxiv.org/abs/1603.09383> (peer-reviewed article: SHA-256 about 2^153.8 surface-code cycles on 2^12.6 logical qubits; SHA3-256 about 2^146.5 cycles on 2^20)
19. M. Cain et al. — Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits (arXiv:2603.28627) — arXiv. <https://arxiv.org/abs/2603.28627> (preprint (2026-03-30): P-256 in a few days with 26,000 physical neutral-atom qubits; RSA-2048 one to two orders of magnitude longer)
20. M. Mosca — Cybersecurity in an Era with Quantum Computers: Will We Be Ready? (IEEE Security & Privacy, 2018) — IEEE. <https://doi.org/10.1109/MSP.2018.3761723> (peer-reviewed article; source of the x + y > z migration inequality)
21. M. Roetteler, M. Naehrig, K. Svore, K. Lauter — Quantum resource estimates for computing elliptic curve discrete logarithms (ASIACRYPT 2017) — IACR / arXiv. <https://arxiv.org/abs/1706.06752> (peer-reviewed article: at most 9n + 2⌈log2 n⌉ + 10 qubits and 448 n^3 log2 n + 4090 n^3 Toffoli gates)
22. NIST IR 8547 — Transition to Post-Quantum Cryptography Standards — NIST. <https://csrc.nist.gov/pubs/ir/8547/final> (final (2026-10-27; the initial public draft of November 2024 is obsoleted). Tables 2 and 4: ECDSA, EdDSA and RSA signatures, finite-field and elliptic-curve DH and MQV, and RSA key establishment are deprecated after 2030 and disallowed after 2035 at every key size — the draft deprecated only the 112-bit level. A composite (hybrid) key establishment stays FIPS 140-validatable while one input comes from an approved scheme. Repeats the federal deadlines of OMB M-26-15: post-quantum key establishment by 2030-12-31 and signatures by 2031-12-31 for high value assets and high impact systems)
23. NIST — Post-Quantum Cryptography Standardization: Evaluation Criteria, Security (Call for Proposals, Section 4.A.5) — NIST. <https://csrc.nist.gov/Projects/Post-Quantum-Cryptography/Post-Quantum-Cryptography-Standardization/Evaluation-Criteria/Security-(Evaluation-Criteria)> (security categories: AES-128 key search 2^170/MAXDEPTH quantum gates, AES-192 2^233/MAXDEPTH, AES-256 2^298/MAXDEPTH; MAXDEPTH 2^40–2^96)
24. OSV advisory GHSA-246p-cpwv-v3jq — OSV.dev. <https://osv.dev/vulnerability/GHSA-246p-cpwv-v3jq> (modified 2026-11-05T23:26:14.796992232Z)
25. OSV advisory GHSA-259r-337f-4rfw — OSV.dev. <https://osv.dev/vulnerability/GHSA-259r-337f-4rfw> (modified 2026-10-20T14:45:03.782718646Z)
26. OSV advisory GHSA-34rh-wp3j-6cxc — OSV.dev. <https://osv.dev/vulnerability/GHSA-34rh-wp3j-6cxc> (modified 2026-09-10T03:50:51.344851444Z)
27. OSV advisory GHSA-99jh-6h7p-pp36 — OSV.dev. <https://osv.dev/vulnerability/GHSA-99jh-6h7p-pp36> (modified 2026-11-05T23:25:35.191121662Z)
28. OSV advisory GHSA-9f3f-wv7r-qc8r — OSV.dev. <https://osv.dev/vulnerability/GHSA-9f3f-wv7r-qc8r> (modified 2026-09-10T03:50:34.689023565Z)
29. OSV advisory GHSA-w239-58x2-q8p5 — OSV.dev. <https://osv.dev/vulnerability/GHSA-w239-58x2-q8p5> (modified 2026-09-10T03:51:07.104837244Z)
30. OSV advisory GO-2022-0635 — OSV.dev. <https://osv.dev/vulnerability/GO-2022-0635> (modified 2026-02-04T02:41:58.893164Z)
31. OSV advisory GO-2022-0646 — OSV.dev. <https://osv.dev/vulnerability/GO-2022-0646> (modified 2026-02-04T02:16:32.066930Z)
32. OSV advisory GO-2024-3218 — OSV.dev. <https://osv.dev/vulnerability/GO-2024-3218> (modified 2026-07-01T14:59:24.616695200Z)
33. OSV advisory GO-2026-5932 — OSV.dev. <https://osv.dev/vulnerability/GO-2026-5932> (modified 2026-11-02T22:15:06.677088389Z)
34. OSV advisory GO-2026-6860 — OSV.dev. <https://osv.dev/vulnerability/GO-2026-6860> (modified 2026-10-27T21:30:04.890809062Z)
35. OSV advisory GO-2026-6865 — OSV.dev. <https://osv.dev/vulnerability/GO-2026-6865> (modified 2026-11-05T23:15:14.472777299Z)
36. OSV advisory GO-2026-6866 — OSV.dev. <https://osv.dev/vulnerability/GO-2026-6866> (modified 2026-10-27T21:45:08.978077289Z)
37. OWASP Application Security Verification Standard — OWASP. <https://owasp.org/www-project-application-security-verification-standard/> (living standard — check the project page for the current version)
38. P. W. Shor — Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms on a Quantum Computer (SIAM J. Comput., 1997) — SIAM. <https://doi.org/10.1137/S0097539795293172> (peer-reviewed article)
39. R. Babbush et al. — Securing Elliptic Curve Cryptocurrencies against Quantum Vulnerabilities: Resource Estimates and Mitigations (arXiv:2603.28846) — arXiv. <https://arxiv.org/abs/2603.28846> (preprint (2026-03-30, v2 2026-04-15): 256-bit ECDLP with < 1200 logical qubits and < 90 M Toffoli gates (or < 1450 and < 70 M); < 500,000 physical qubits at 10^-3 error, minutes)
40. S. Jaques, M. Naehrig, M. Roetteler, F. Virdia — Implementing Grover oracles for quantum key search on AES and LowMC (EUROCRYPT 2020; arXiv:1910.01700) — Springer / arXiv. <https://arxiv.org/abs/1910.01700> (peer-reviewed article: lower cost estimates for the AES key searches that define the NIST categories)

## Appendices: Cryptographic inventory

By origin: dependency manifests 3 (0 Shor-breakable) · own code 93 (26 Shor-breakable) · third-party code in the tree 209 (76 Shor-breakable).

| Algorithm | Parameter | Library | Quantum status | Classical status | Count | Locations | Examples |
|---|---|---|---|---|---|---|---|
| AES-256 |  |  | reduced margin (Grover), approved | acceptable | 3 | 3 | crypto/include/sodium/crypto_aead_aes256gcm.h; crypto/libsodium-fork/src/libsodium/crypto_aead/aes256gcm/aesni/aead_aes256gcm_aesni.c; crypto/libsodium-fork/src/libsodium/include/sodium/crypto_aead_aes256gcm.h |
| Argon2 |  |  | reduced margin (Grover), approved | acceptable | 21 | 21 | crypto/include/sodium.h:32; crypto/include/sodium/crypto_pwhash.h:104; crypto/include/sodium/crypto_pwhash_argon2i.h |
| ChaCha20-Poly1305 | ChaCha20-Poly1305 |  | reduced margin (Grover), approved | acceptable | 11 | 11 | crypto/include/sodium.h:9; crypto/include/sodium/crypto_aead_chacha20poly1305.h:1; crypto/include/sodium/crypto_aead_xchacha20poly1305.h:1 |
| ChaCha20-Poly1305 |  |  | reduced margin (Grover), approved | acceptable | 17 | 17 | crypto/include/sodium/crypto_secretbox_xchacha20poly1305.h; crypto/include/sodium/crypto_stream_chacha20.h; crypto/include/sodium/crypto_stream_xchacha20.h |
| HKDF |  |  | reduced margin (Grover), approved | acceptable | 1 | 1 | daemon/kmd/wallet/driver/sqlite_crypto.go:241 |
| HMAC | HMAC-SHA-256 |  | reduced margin (Grover), approved | acceptable | 3 | 3 | crypto/include/sodium/crypto_auth_hmacsha256.h; crypto/libsodium-fork/src/libsodium/crypto_auth/hmacsha256/auth_hmacsha256.c; crypto/libsodium-fork/src/libsodium/include/sodium/crypto_auth_hmacsha256.h |
| HMAC | HMAC-SHA-512 |  | reduced margin (Grover), approved | acceptable | 3 | 3 | crypto/include/sodium/crypto_auth_hmacsha512.h; crypto/libsodium-fork/src/libsodium/crypto_auth/hmacsha512/auth_hmacsha512.c; crypto/libsodium-fork/src/libsodium/include/sodium/crypto_auth_hmacsha512.h |
| PBKDF2 |  |  | reduced margin (Grover), approved | acceptable | 2 | 2 | crypto/libsodium-fork/src/libsodium/crypto_pwhash/scryptsalsa208sha256/pbkdf2-sha256.c; crypto/libsodium-fork/src/libsodium/crypto_pwhash/scryptsalsa208sha256/pbkdf2-sha256.h |
| Poly1305 |  |  | reduced margin (Grover), approved | acceptable | 21 | 21 | crypto/include/sodium.h:31; crypto/include/sodium/crypto_onetimeauth.h:6; crypto/include/sodium/crypto_onetimeauth_poly1305.h:1 |
| SHA-2 | SHA-512 |  | reduced margin (Grover), approved | acceptable | 12 | 12 | cmd/goal/application.go:21; crypto/hashes.go:21; crypto/include/sodium/crypto_hash_sha512.h |
| XSalsa20-Poly1305 | XSalsa20-Poly1305 |  | reduced margin (Grover), approved | acceptable | 26 | 26 | crypto/include/sodium.h:36; crypto/include/sodium/crypto_box_curve25519xsalsa20poly1305.h:5; crypto/include/sodium/crypto_secretbox.h:1 |
| XSalsa20-Poly1305 |  |  | reduced margin (Grover), approved | acceptable | 17 | 17 | crypto/include/sodium/crypto_core_salsa20.h; crypto/include/sodium/crypto_stream_salsa20.h; crypto/include/sodium/randombytes_salsa20_random.h |
| scrypt |  |  | reduced margin (Grover), approved | acceptable | 4 | 4 | crypto/libsodium-fork/src/libsodium/crypto_pwhash/scryptsalsa208sha256/crypto_scrypt-common.c; crypto/libsodium-fork/src/libsodium/crypto_pwhash/scryptsalsa208sha256/crypto_scrypt.h; crypto/libsodium-fork/src/libsodium/crypto_pwhash/scryptsalsa208sha256/scrypt_platform.c |
| BLAKE2 |  |  | Grover: acceptable to NIST, below ECCG/ANSSI guidance | acceptable | 33 | 33 | crypto/include/sodium.h:22; crypto/include/sodium/crypto_generichash.h:54; crypto/include/sodium/crypto_generichash_blake2b.h |
| Keccak-256 | Keccak-256 |  | Grover: acceptable to NIST, below ECCG/ANSSI guidance | acceptable | 2 | 2 | data/transactions/logic/crypto.go:142; data/transactions/logic/doc.go:44 |
| Poseidon |  |  | Grover: acceptable to NIST, below ECCG/ANSSI guidance | acceptable | 5 | 5 | data/transactions/logic/crypto.go:32; data/transactions/logic/doc.go:73; data/transactions/logic/fields.go:932 |
| SHA-2 | SHA-256 |  | Grover: acceptable to NIST, below ECCG/ANSSI guidance | acceptable | 13 | 13 | crypto/hashes.go:20; crypto/include/sodium/crypto_hash_sha256.h; crypto/libsodium-fork/src/libsodium/crypto_hash/sha256/cp/hash_sha256_cp.c:61 |
| SHA-3 |  |  | Grover: acceptable to NIST, below ECCG/ANSSI guidance | acceptable | 2 | 2 | crypto/stateproof/coinGenerator.go:23; data/transactions/logic/crypto.go:24 |
| SHAKE |  |  | Grover: acceptable to NIST, below ECCG/ANSSI guidance | acceptable | 1 | 1 | crypto/stateproof/coinGenerator.go:78 |
| Crypto library | v0.57.0 | golang.org/x/crypto (Go x/crypto) | n/a | acceptable | 3 | 3 | go.mod:59; tools/block-generator/go.mod:166; tools/debug/algodump/go.mod:145 |
| FN-DSA |  |  | post-quantum | acceptable | 3 | 3 | crypto/falconWrapper.go:22; data/transactions/logic/doc.go:50; data/transactions/logic/opcodes.go:860 |
| ECDH |  |  | vulnerable (Shor) | acceptable | 4 | 4 | crypto/secp256k1/libsecp256k1/include/secp256k1_ecdh.h:20; crypto/secp256k1/libsecp256k1/src/java/org/bitcoin/NativeSecp256k1.java:381; crypto/secp256k1/libsecp256k1/src/java/org_bitcoin_NativeSecp256k1.c:6 |
| ECDSA | secp256k1 |  | vulnerable (Shor) | acceptable | 21 | 21 | crypto/secp256k1/curve.go:33; crypto/secp256k1/dummy.go:14; crypto/secp256k1/libsecp256k1/contrib/lax_der_parsing.c:8 |
| ECDSA |  |  | vulnerable (Shor) | acceptable | 17 | 17 | crypto/secp256k1/ext.h:53; crypto/secp256k1/libsecp256k1/contrib/lax_der_parsing.c:12; crypto/secp256k1/libsecp256k1/contrib/lax_der_parsing.h:82 |
| ECDSA | P-256 |  | vulnerable (Shor) | acceptable | 3 | 3 | data/transactions/logic/crypto.go:363; data/transactions/logic/fields.go:769; data/transactions/logic/opcodes.go:69 |
| Ed25519 | Ed25519 |  | vulnerable (Shor) | acceptable | 32 | 32 | crypto/batchverifier.c:16; crypto/batchverifier.go:190; crypto/curve25519.go:69 |
| RSA | 2048-bit |  | vulnerable (Shor) | acceptable | 2 | 2 | installer/rpm/RPM-GPG-KEY-Algorand (line 1) |
| RSA |  |  | vulnerable (Shor) | acceptable | 1 | 1 | tools/network/dnssec/testHarness.go:22 |
| X25519 |  |  | vulnerable (Shor) | acceptable | 7 | 7 | crypto/curve25519.go; crypto/include/sodium/crypto_scalarmult_curve25519.h; crypto/libsodium-fork/src/libsodium/crypto_scalarmult/curve25519/sandy2x/curve25519_sandy2x.c |
| X25519 | X25519 |  | vulnerable (Shor) | acceptable | 15 | 15 | crypto/include/sodium.h:34; crypto/include/sodium/crypto_box.h:57; crypto/include/sodium/crypto_kx.h:42 |

_Long lists are grouped here; the full per-file list is in the JSON report, signed with the same key._

## Appendices: Input files

| File | Size | SHA-256 | Redactions |
|---|---|---|---|
| agreement/abstractions.go | 13820 | `1b1550948621a587563fa9f64b9a89261a631e14b3bc11188d0d8cf17675a0c8` | 0 |
| agreement/actions.go | 17401 | `51a5d195e2a9848249c06b09929e878d0bee8924c6ec965fd150290877e9aba5` | 0 |
| agreement/actiontype_string.go | 1126 | `fac0b616090792ec426f2d1e525f65614c3a6da88af3474513236df3e9f45274` | 0 |
| agreement/actor.go | 4330 | `7ef6665a9e6e9b564c0c37fb172fe7ce17ac3d6df9200776741eda78523ae7e9` | 0 |
| agreement/agreeInstall.go | 1052 | `f23a492c0622bc473cbebe3243e8f5029ff3ed79d6d5df166652ccbcaeb703fd` | 0 |
| agreement/agreementtest/keyManager.go | 2130 | `7f0c82235ba4ead401aae79343cdd7a6a108a55944c344376b85ddbb3284a8d3` | 0 |
| agreement/agreementtest/simulate.go | 5162 | `d0521b338f0f73c4a99bef572befbca8ceff69de55cffa176893dd2f561d8e2b` | 0 |
| agreement/asyncVoteVerifier.go | 7382 | `3fc5534ea06ae1040a15211caff80c0e03dedc6c217ace1bc76d23ad430bc887` | 0 |
| agreement/autopsy.go | 12956 | `006dff76c5e7cd455c1b9b37793d86df0abbeaec4294df3087a6cb2ecf31e3de` | 0 |
| agreement/bundle.go | 10740 | `4d60f2b0a57dd3e280aa843b58a625a1ed3fc544f88968004d5467a194bbc058` | 0 |
| agreement/cadaver.go | 4957 | `c85cf3ab5ecb12bee1487d2a6d46217190715b790ea9393ca15c3bb6e44ecc01` | 0 |
| agreement/certificate.go | 2563 | `d4cefbe49774f94fa73dff6162c71d4b04e8d0876b22d391b1ffcb15be223b80` | 0 |
| agreement/coservice.go | 2125 | `b8de70aa739533a2ae2808c065787b7c94b5f1f03f8a65a890ed02a344fb3dd2` | 0 |
| agreement/coservicetype_string.go | 972 | `2f7ae2fd053f3ad175b4ed3a8db53b9a4e614a0dbc3e67932650225a20e9597f` | 0 |
| agreement/credentialArrivalHistory.go | 2669 | `a1987d520b4a99c0f591e6ddc24c75d762f6073350c1002e2c943a51f2f0e3bf` | 0 |
| agreement/cryptoRequestContext.go | 5364 | `a1b5650ac27bce38ab3de61225b2aa0ba0331b82f802df27ffdfc2a0fbfd58e0` | 0 |
| agreement/cryptoVerifier.go | 12870 | `2854e9d325d85ca041da1211e41aabfca11f3e7a706eafd6d6ccae0763c3b7ff` | 0 |
| agreement/demux.go | 15519 | `638df6ee6517c5adc5a5be69cbfcc4dee439d991aaf8faf7e39fdbb7c5630671` | 0 |
| agreement/doc.go | 2026 | `49efaf893e51d40a4106082a095e38ba0eb13639e0923596dedf1e22980c45e0` | 0 |
| agreement/dynamicFilterTimeoutParams.go | 2118 | `95fe5f23ae9be5d3a8c78a8ead9bf026e8eae1616590c3ac1d950ac0394b0808` | 0 |
| agreement/errors.go | 1613 | `d24d791681af1ce042e9c8d04376b6e48ba524692638e756ed1b45df70a3d009` | 0 |
| agreement/events.go | 30191 | `3cbf3b9bb4b84529ce994bc3bcab3ea1e4ea7501346bf0356e9a09f8455341af` | 0 |
| agreement/eventtype_string.go | 2359 | `f198833b6643f64eaa899ae1a3206d13069eca92c5542aebb59b5d6770274fbc` | 0 |
| agreement/gossip/network.go | 6312 | `11eefe549a42dc38d86825097910689df33a493a9e256c9e539606eca56102ca` | 0 |
| agreement/listener.go | 2547 | `ca252257205e05033dc4591d7377fd25d6f42fa0f7ceeafa727b3374c2a0db03` | 0 |
| agreement/message.go | 3647 | `862476d9ee78b722f305a14dc5895373c11c2c49e0fb03e9dc0cb4ddd4d15e24` | 0 |
| agreement/msgp_gen.go | 297170 | `1f06b6bf747a8fff86f4eb01416f152e1ec3b6d0fd7fcd331ed0f6490b83790d` | 0 |
| agreement/params.go | 1025 | `09358375a8545bd5d4552d2d3d2e79e9abc69d2fb2e194c8a246d9bbc7cb3eb7` | 0 |
| agreement/persistence.go | 12397 | `9b9243129b1cdf9d090db4ffddceb32d086443c89610583e78ace9648053dc87` | 0 |
| agreement/player.go | 28876 | `e1c6f0ad5fca758c81ffc6c3bf1fa0c749ddb5907f9d31f559869393581b3dda` | 0 |
| agreement/playerContract.go | 3081 | `de4f0d4ca1c632675d19bec6bc1248f5a81d70b9c4a964b0aefab6da3cf1aa12` | 0 |
| agreement/proposal.go | 13400 | `139e69cbb11bcf962617dcbec247642df917297b0fe87e34d661595725ae48f7` | 0 |
| agreement/proposalManager.go | 12500 | `72ff01cafb98b2bf8e505d3db9326610ac985e5f804e3bba2f726786cec11b41` | 0 |
| agreement/proposalManagerContract.go | 1723 | `706e46846f2be0d40056098b96672ab99bc4880294531475302ef7c9cbefc1c0` | 0 |
| agreement/proposalStore.go | 14688 | `8f4d00157543cb3655d5963d4d90fbc4d0e222f098fc3c8ead2f9cb6ed257a5b` | 0 |
| agreement/proposalStoreContract.go | 984 | `6d0a356cad41d56f53b1ba4667522e4de3816ceac15b833fc51abf5009ba4303` | 0 |
| agreement/proposalTable.go | 1493 | `7b6eb3ec188c5b11f519481da62f99dbfbbd4568e3638688ee0c7103e6a60c49` | 0 |
| agreement/proposalTracker.go | 9220 | `dd5c6f8c088db3c43d1d2f23a8f99719c07bafc98e6bca9771011344d8977a65` | 0 |
| agreement/proposalTrackerContract.go | 5067 | `c2bcca9fb29ebf56f5701c03eaf248ad4d4dc9f71cef15980970c4c93eed2a0b` | 0 |
| agreement/pseudonode.go | 22377 | `68c1e90741fdc7b2ed461b89709ff22ef954c329dda8447f2835b58de943104a` | 0 |
| agreement/router.go | 11430 | `d94ad156aea7a656066a04f305d349080439329a232e40aef3b8d016d6c3334d` | 0 |
| agreement/selector.go | 3542 | `ad5be0ba02e57f5f35ea147dcb340a7f46b053548a59b417c5ab02334823b0b5` | 0 |
| agreement/service.go | 9353 | `6661731350d476fa7060cfe16f361c76c5cd69830ce2882ae74e1d80b4e00f59` | 0 |
| agreement/sort.go | 3219 | `a1a7e60e733fc3c1fa380681f0303a1ad44c74d0943640eacedd44c2351e4847` | 0 |
| agreement/statemachinetag_string.go | 1062 | `3a5ad08ec9b1f228ef555f78a6711676576dfa3de53a946758331dafdfbfbe9e` | 0 |
| agreement/trace.go | 17381 | `29864d10fa08971dcabaecdd8663985d4bf564aeae2a7339e3a9c38f68f5751c` | 0 |
| agreement/traceTime.go | 8313 | `d2bd10d8a957fedaddbd569291e230a030464f9575b8cd35abdcd16a95ce4677` | 0 |
| agreement/types.go | 5287 | `a0390b1d48016dd547b309acbbf89e64e2823abf4bf63710930b3dc37e7d5409` | 0 |
| agreement/vote.go | 10531 | `c104578980fc2c6d13e68fc183a96c1e86a7cbb6640d0900f6fad73c78c1ce98` | 0 |
| agreement/voteAggregator.go | 11525 | `f4a4161f604356ede37f8fc63e538763af4f95b0e31cef4ae199b71fe35a0308` | 0 |
| agreement/voteAggregatorContract.go | 2239 | `28c911b84d6d371349f470397efe8c05a70a7b69e28d6b6da2260ddfc0250215` | 0 |
| agreement/voteAuxiliary.go | 6541 | `5fdb764c3839edeb3ab7d75dd8ea54588aeac89308ae020b59da130e3b4e8104` | 0 |
| agreement/voteAuxiliaryContract.go | 1306 | `e6d48875e85a90e900cb31d9289be8fb82683f13516653a60a2d2a47cf4376c5` | 0 |
| agreement/voteTracker.go | 13995 | `25cf918c15647ad689dd2e749451d0bcb9364d1ebd2e28d911f905d71d84097d` | 0 |
| agreement/voteTrackerContract.go | 4617 | `b6f797372f218dff68992262295b823360dccbaa9b43c4750d5ba42814f2f8dd` | 0 |
| catchup/catchpointService.go | 34534 | `c1034353cb53880c809037590cfe7208cdccba8581fbb0dc40fe650bfdc0ce75` | 0 |
| catchup/classBasedPeerSelector.go | 6176 | `ac9df7ef4c2bde7ad26cdc19316e6d572747f4eb836603ac3d7957945b0b49cb` | 0 |
| catchup/ledgerFetcher.go | 8451 | `548c8c6edaff25d28deed0166714fd4b64fd187dc2a89f1f924a2810e86bf43d` | 0 |
| catchup/peerSelector.go | 22469 | `2fbad12a7d5d646ec22e007748fe13e8766ff696aea57da45d6883ea257ed047` | 0 |
| catchup/service.go | 39149 | `c8c1fa245284c940173a3880e9d2df97466c7105c43978366bc05a3ada511731` | 0 |
| catchup/universalFetcher.go | 13039 | `6f9ff9cfb2cf3265b3f0e47fd3ed300c6ddba7dd5071e163cae2acc6610a10f0` | 0 |
| cmd/algocfg/getCommand.go | 2148 | `752985ed26559a4a15e0e19311841b11f6efc0ebcb1b986f52dbef250eeac7f9` | 0 |
| cmd/algocfg/main.go | 1388 | `4e23af7bfdfdd896a8381e7909416d87136a9a87b56f8043640ed578f28ce9d7` | 0 |
| cmd/algocfg/profileCommand.go | 8479 | `53485a2283b3d90711944b5fea950ed578f0946537166780250317d132d06319` | 0 |
| cmd/algocfg/report.go | 1084 | `6702ac8ad269dcd38d86f21b9683f107918b03cdb0d49f1e4181f4a60c840b77` | 0 |
| cmd/algocfg/resetCommand.go | 2760 | `e0b45b8fd39563b6a64a6a218ab88757117b6d4683127123e5c25187a27de0fb` | 0 |
| cmd/algocfg/setCommand.go | 3754 | `5c7de87f8b43607d6a974a3c9e4299f500ddbc0a39c129641b26a99e8599e691` | 0 |
| cmd/algod/main.go | 17243 | `3b598b502a42ae4a77dcbfdab5efc1029f5cd1ca5c7c337397b2eb8609f28b0e` | 0 |
| cmd/algofix/deadlock.go | 2242 | `33f880b1c6fce5476e99a659a592e14e47f5c169121e3045a0f2feaa750d5d2f` | 0 |
| cmd/algofix/doc.go | 1426 | `a0a8131a9d77fa4273df0608cd1a4f7e7e89ba1cb14fac8dee2febf3dcddb1af` | 0 |
| cmd/algofix/fix.go | 12835 | `fab15ef63cbd9870b9884894a181ed1cea281c009e59e981a077853a71ed4e2c` | 0 |
| cmd/algofix/main.go | 5886 | `79d868771d380065689e38e25cea544dbec76f5815ba6637fb8bd3e90a48d405` | 0 |
| cmd/algoh/blockWatcher.go | 4432 | `2d2802152f660786545cb325f0ce94d800f44201b020549554524cde351836a4` | 0 |
| cmd/algoh/blockstats.go | 2367 | `290a2268863b8ce266b984741a181664bce319842e47f812e21562616a488341` | 0 |
| cmd/algoh/client.go | 1161 | `af3f41f119356e4feb8cf44b453bc1565ea6fda814b372f6b4f49831508ceb23` | 0 |
| cmd/algoh/deadman.go | 4177 | `bdd3f98ce5fddc8449358259d20ca5d8b599d6bb37e21c0168defcb1cb96f0fc` | 0 |
| cmd/algoh/eventsender.go | 1021 | `0f6673c67b4cd4acfa2f76ba0e1e830bcb0725a4f21e4731c86799f1b9dbfeaf` | 0 |
| cmd/algoh/main.go | 13915 | `2b5b01190a90f2c9a25733c685f8a537b5f21de44026eecb5f2d4830713783e0` | 0 |
| cmd/algoh/mockClient.go | 3458 | `e81b0d56ce52b1f2f78e73398ec28c326adda2d12aee49ff4a4490bb5ca37fec` | 0 |
| cmd/algokey/common.go | 3738 | `45851572dd57f009871f5f4a0ce6eae57dd86dc37516a8f84f87af5a4e83ee55` | 0 |
| cmd/algokey/export.go | 1775 | `609e5f4636d8d08559eab22845a53f6af3c7204f00aab409e32850cb81237f1a` | 0 |
| cmd/algokey/generate.go | 1817 | `1a2d9bd599fdba8307adc94d507ec1160da482b0cc32521b6aa699f95a57087e` | 0 |
| cmd/algokey/import.go | 1685 | `0f8b49d83e779dc216867174d3bbdff46e1af2b858a707c319d537d261b79b4f` | 0 |
| cmd/algokey/keyreg.go | 9082 | `36d8f3fccdf0ae89c68833670ed885a58b0972dd7b431e1f6f5a6fa6a35a8baa` | 0 |
| cmd/algokey/main.go | 1968 | `b2644062abb594f442b95dc93a0dd576f4b57aa7f09f3449416783de726ebdf0` | 0 |
| cmd/algokey/msgp_gen.go | 6512 | `3c8f004483ee2364332a0b30e9885ce38bc21187fdb6394acecdd67bd6ea6c6b` | 0 |
| cmd/algokey/multisig.go | 6126 | `346b9c060f28412299100d1797bfee0dc2388f68385a6881fd1fffcaf403eda7` | 0 |
| cmd/algokey/part.go | 6957 | `46fc9e21b15cb6320d5afc257c74a38798a9ac79b714cc592cd9cf6542f5e163` | 0 |
| cmd/algokey/salted.go | 15013 | `2f414774253e92425a8ce51ad4ce44f6c7370e04e0ca055109ff18d81d8c04d4` | 0 |
| cmd/algokey/salted_key.go | 3682 | `22caed4572f0c1b8ab70928c31b10987b39bdae85385857d89cb32ae799eb25c` | 0 |
| cmd/algokey/salted_scheme.go | 7409 | `93f80c8b3c1528084472308be07274529963a14d2f06a4e4542c9c894c6f732b` | 0 |
| cmd/algokey/sign.go | 2690 | `f190dd847f22ae44418bfac31d54c3b43c8624bd05d7bb1bb89e4e4baa056f77` | 0 |
| cmd/algons/commands.go | 1212 | `57fcbb7040fa0a2a29c7a0f273844b10d73414fe45a8bd27b92adafcb2b2ab04` | 0 |
| cmd/algons/dnsCmd.go | 16087 | `0bc8fd171c43bdce49fa5476885de1de1188fc85d3f66103c9e4ab0ecd3074aa` | 0 |
| cmd/algons/dnsaddrCmd.go | 6822 | `ff81a9bced1709109334b896b37503d67b50fe456c705e59daa4200451985c74` | 0 |
| cmd/algorelay/commands.go | 1640 | `99384a266a0db3b37e6d22961fb45c8995939ffd64b1b0735d51e4074a9c8d31` | 0 |
| cmd/algorelay/eb/eb.go | 1111 | `d76c884ffd099167d5ed884c96592d693fb4c3be799686b8a201d13cb19b2a83` | 0 |
| cmd/algorelay/relayCmd.go | 19496 | `5709bb3b4820ecf9dfb6457080137f8c94d868e47f572ecabefb03053630b74f` | 0 |
| cmd/buildtools/commands.go | 1486 | `d28e34aa588d8c5e655688085107d921a88a050989fc2090be8ba315a82ce9c9` | 0 |
| cmd/buildtools/genesis.go | 9759 | `4395cb1d16e91b6b833d99b60ef014aafa642f2c761144f8ad1e7dff809b7f3d` | 0 |
| cmd/catchpointdump/commands.go | 3333 | `f490c1fa1294f97b8e293cfec752677fc6500ee8c5aedff6c6fcd39f031cdb0b` | 0 |
| cmd/catchpointdump/database.go | 6906 | `c8b1589519d8e68d300bc4fdc97bc6bc82baec0b60013763a90b0526b58e870f` | 0 |
| cmd/catchpointdump/file.go | 26885 | `a1bdb458bb7324492ad9c3ad771ad407626f66a1d79924138bee3e4cd0fa03fb` | 0 |
| cmd/catchpointdump/info.go | 9664 | `a6c530e41680da76e077261a85386ee61de51bc0f10fac664b353d85f38feee6` | 0 |
| cmd/catchpointdump/net.go | 12519 | `12bfe2f5cd52055d365b502ecb74b83178a14301a0f5d6d829727e04ed0d98a4` | 0 |
| cmd/catchupsrv/download.go | 6266 | `1db3102951d5dec2864c56606362a513cdb36072c59b282abad81241bae3c36f` | 0 |
| cmd/catchupsrv/main.go | 4162 | `edac94439d7fbe4eeb9edf4cf5e8ae53419190acb96f4e9083e932e79669f49b` | 0 |
| cmd/catchupsrv/tarblocks.go | 5403 | `58380dd435b474c14a022e18a1663afa2f46fecbf6f2ed38fdfbcdf69b243340` | 0 |
| cmd/dbgen/main.go | 2573 | `b79fd472329fbfa831a19ec37be841d89e85a8c6c8d68b191e4058f5049aea4d` | 0 |
| cmd/diagcfg/main.go | 1429 | `3e01323d714cad0aa513d87ec1fb53bc5f56db5783550644b73f7e3d3c9d2ac2` | 0 |
| cmd/diagcfg/messages.go | 1520 | `d094fe754536a61f1852f5fd4f3694ce9b12a0e95d37ed87b5ed7f1f40fa5e1e` | 0 |
| cmd/diagcfg/metric.go | 3613 | `d8bfdea52cd7a29c0bbd24af0be9de52944984a02b4a7d68cb749beac27a091f` | 0 |
| cmd/diagcfg/telemetry.go | 5642 | `7f9e576ee1de5d234d828311d856deeeeb09efcef40a6e6c919ead8697070346` | 0 |
| cmd/dispenser/server.go | 6432 | `e9ea7e573a273e71b8bf59c0c0bf0b0a7817cb5bb298830d870147c03b16776e` | 0 |
| cmd/genesis/newgenesis.go | 2242 | `09e8359babb6f8578a810cd5c48679a2fff1c10e331bc9d007d30d4910c9b872` | 0 |
| cmd/goal/account.go | 61819 | `f43c6b298eb75aa7cdc555955be64dd72af72fed74da2c78abf8af4f280a924b` | 0 |
| cmd/goal/accountsList.go | 7803 | `82d2ee00666b6c35effb2d5e0015387cc1e76d2ef0a1718763a4df304c501098` | 0 |
| cmd/goal/application.go | 55358 | `166313aafdc25fbc3f91424486fc980ca51f1c5255f561abe1182ec56f7319c1` | 0 |
| cmd/goal/asset.go | 29760 | `503087ffde87373b3eed8b89ec019242ca87db57dfde9d29a02603730ca01ace` | 0 |
| cmd/goal/box.go | 5287 | `009c362d0565596119166ecd4a9e7ffc55525459876b2938d31fd1330056f872` | 0 |
| cmd/goal/bundledGenesisInject.go | 77754 | `c05ab12b7922194eef355a9dc3031889ff3f96bb423da9d67ee4f8aae5b015f0` | 0 |
| cmd/goal/clerk.go | 46423 | `812cb2c650c3d05c1ed0844551a7a310a11ee7cd088c24195736d7279e882d3c` | 0 |
| cmd/goal/commands.go | 15572 | `f02bd777b2d4745bf9c30b96525f4806243ed87a0bd7e2dd8e92e3da2b7a2046` | 0 |
| cmd/goal/common.go | 3466 | `bda3b9ad4def95fd62cd023b3d71732280897511a771213fe0b6f36e0e8eee5d` | 0 |
| cmd/goal/completion.go | 1620 | `306f241272c0800f821d1b685989b1bf4bed6ad8b9233ffd17304376451f608a` | 0 |
| cmd/goal/formatting.go | 5301 | `9c9d02473917821cb69c2786ae7d1f30f0724c2e914dc4779cb896d833989b72` | 0 |
| cmd/goal/inspect.go | 5663 | `0a4909cd8c70114adc79719b4c184f6e683541563a8cf5b0ca014197e1c771d3` | 0 |
| cmd/goal/kmd.go | 3106 | `efdc23b52c86dae8289c3c53ef4bff9e8325f87f685d1417d91d3bd9526a7007` | 0 |
| cmd/goal/ledger.go | 3854 | `b30ec97b18eb2ad3031cd06e29e10f5097a1ce858a38e8f99cdf2d0ad1d98396` | 0 |
| cmd/goal/messages.go | 14950 | `0dd028adbdbdde5da54c1e7744f2793c10234078e748f706ad735710d3cb58c4` | 0 |
| cmd/goal/multisig.go | 11972 | `4e74e6613e10fed650c2993594024fe18ef16cddb79c2220b69ecc0278db9ed5` | 0 |
| cmd/goal/network.go | 12075 | `858a3875a325960bb79a8a580eee73d12049b0e3d02ff40ec61c8b78ea9c5465` | 0 |
| cmd/goal/node.go | 23849 | `0e09d24d216ad4e1e5e87ab450409816a7e163529f3dea22538109e040e910b9` | 0 |
| cmd/goal/p2pid.go | 2242 | `9be82fd3cadeed8271738928835bc33754fec23594976a97975f6a2c9eb16819` | 0 |
| cmd/goal/tealsign.go | 7971 | `9ad98f63e89de1ad0ef5467d894450303ee9d97fb598a8cda043b3a9857c9c71` | 0 |
| cmd/goal/wallet.go | 8316 | `56b17730b7f6db396b0cb3efc13e6eb47ccaee474c5af86338553841e2803efc` | 0 |
| cmd/incorporate/incorporate.go | 7721 | `cdba7033ab5a585027276355497db9a3b9b44ddff613398302855e885ade4714` | 0 |
| cmd/kmd/codes/codes.go | 1109 | `fef14b0c3fa8a6f3669cd93cdc568ef73f923557a0c17541c0e9af48031f6ddd` | 0 |
| cmd/kmd/main.go | 4079 | `f79844ee6423a53a7717e6fff5ecbbfc8edd464aef8bcebea73542712b7cb1f3` | 0 |
| cmd/kmd/mlock_darwin.go | 919 | `9b5f78ec6f6ab2091401f64f02fa85978ad3c63664bd467c0859f90693d97ae9` | 0 |
| cmd/kmd/mlock_linux.go | 1126 | `1a30e990b12668720266ffdeea188b797d60b09376ebce15e74e7afbf115016e` | 0 |
| cmd/kmd/mlock_windows.go | 1167 | `a57d6943db8a230d24cd8c771c87b8452d673c7e687f422b6b290968f9bdc81a` | 0 |
| cmd/loadgenerator/config.go | 2560 | `0dfa5a2c1450da23337d326125b3b6d73b3ae7fb7ba4c1f8c45b32af247c916c` | 0 |
| cmd/loadgenerator/main.go | 9176 | `a4618d67482cd481b32236c02345adfe7f9e0a397b7a3658b9e4c919a500a8e7` | 0 |
| cmd/msgpacktool/main.go | 2758 | `a21977e153e6e71c817bc0ee9213fb2cfb87ab772c9adbe15656796bbbb4ff1e` | 0 |
| cmd/netdummy/main.go | 1825 | `fa5883ed00f6a9b914ecd050d434440bac90e541b1ed47c380366918252de9a0` | 0 |
| cmd/netgoal/commands.go | 1789 | `da2276492bea7480fd3c51ce815a7b0af226fdc285d00cd35112afa987f7349a` | 0 |
| cmd/netgoal/generate.go | 18976 | `78cd257ed54a1274f887b7be8529ea044501b3a43fb3579223e6789c8fc74345` | 0 |
| cmd/netgoal/messages.go | 980 | `ddc63b57e0e05cafee7212f2c48fbbd4c50f673fb87fb41015ff9b01e95d8db1` | 0 |
| cmd/netgoal/network.go | 7891 | `9bdf7a15fc1bf665e2db18ea02bcf1642d27b507ca12d58d3fccd552a1b3ed13` | 0 |
| cmd/netgoal/recipe.go | 950 | `e32c8c67906294f7e7c5ff5dca07e2cbd21842c7a91746be9bee4bbe420f0e5c` | 0 |
| cmd/nodecfg/apply.go | 5441 | `ddc378a059ca80824b6b18298568b50eb0eb80bfae3bf03268a080c85d270bef` | 0 |
| cmd/nodecfg/commands.go | 1719 | `fd0d1e554244ebdbd2cdf5ea4cecf0e55f2d524e84a63735c8b30a69b8f7383a` | 0 |
| cmd/nodecfg/download.go | 2594 | `1588fd5f2a0e7350f8f2fb02340a5d0741346e23afa552d664052e437e885ad5` | 0 |
| cmd/nodecfg/get.go | 2481 | `1685c86a188f72dd0d6f11f95f40ea5e104a56260be47c7772d7e230b9a174a4` | 0 |
| cmd/nodecfg/untar.go | 3538 | `d8c7e611d6962774fd3cead2b6c58b591f1ab449be543c039933a66e751e9921` | 0 |
| cmd/opdoc/opdoc.go | 18051 | `fbe713e20f16714568ec0aee21a9609a4a596d32fd8ca65de7ace27881d3d7fc` | 0 |
| cmd/opdoc/tmLanguage.go | 7185 | `20cc4ad97970fe705b7362e475bf8331899b0b2d14dcbc5be71c7d7de418934a` | 0 |
| cmd/partitiontest_linter/go.mod | 277 | `9d3f529cd8bc1354e89448e5d92dadf7c3d9b48a1b72a08f744363c059de0c24` | 0 |
| cmd/partitiontest_linter/linter.go | 4745 | `7a836c5e54c052d3606cd2127149ae8f20a989e48dbd13671f128a6a2f40d884` | 0 |
| cmd/pingpong/commands.go | 1139 | `caee55f6719cc4bbcee1c70faff75a38f6c2a5ca2a470678b1e11d380a0eb4d0` | 0 |
| cmd/pingpong/runCmd.go | 17291 | `cda9cd0b4b8ba248d1ba60f03f780a96a22976887799eda2a4d738b49e758f92` | 0 |
| cmd/pingpong/teal_programs.go | 3604 | `e9af3d34d64107f76bfc97107285953450fae6f82e6da2a07ffc5b143ebd0e5c` | 0 |
| cmd/updater/commands.go | 1453 | `4b64a13afe7c73164ccad750c2aa43b4e7cd0e83f2148b2bcba1706553e073d9` | 0 |
| cmd/updater/sendCmd.go | 1951 | `696fdedd961d73455d120031edc4ac44fbf6c52308bf551be4cbe033d8645659` | 0 |
| cmd/updater/toolsCmd.go | 2390 | `d77c5692fd3e482b5181d4e3713e61ec36feb9c4456af71a175c67c4f13e99fe` | 0 |
| cmd/updater/util.go | 896 | `3e572a018992b20a5bc9ccf7dcb595de2c056870f8ded9463022e28209a6f6df` | 0 |
| cmd/updater/versionCmd.go | 4305 | `e3e44617d1194d3f7b3d8ac30aaf1f9ce9778d093fd9462877122635ea543f3a` | 0 |
| cmd/util/cmd.go | 4075 | `6ca5adacd6c29f760c5d0a7c0d35af21d3177eef688baf847df208b302e97997` | 0 |
| cmd/util/datadir/datadir.go | 2764 | `4a546820eed493effa229775694716ea822616670fb2c54118e501512ed353e3` | 0 |
| cmd/util/datadir/messages.go | 1063 | `47d7cbd0c4e4cc0dcd3ab595e82ef99a03b15c5f864a86a4b761c54f9104d067` | 0 |
| cmd/util/datadir/report.go | 1209 | `eb1c321c7807945bc51e7166f45717a58346a96da9efa444ae685a7f78595df0` | 0 |
| config/bounds/bounds.go | 6946 | `67ae12682638a050467b8e3aa083ad5964b7b601fe65c185a4932ebdf4c29e7a` | 0 |
| config/buildvars.go | 1716 | `92e65fe77f59a348cad22819da17db123e10fe06b721fc242a4db166cf01a9b2` | 0 |
| config/config.go | 13885 | `99dd6f813d087fcc081ae922828fd553f52fe047e3706d71b3aacdb389912648` | 0 |
| config/consensus.go | 66799 | `5bf3f6a4d45f8a0a16e077a926ff5076800bff41441f30890dd1febbde897051` | 0 |
| config/defaultsGenerator/defaultsGenerator.go | 6866 | `550038bbf55b4f66950cca1078706edb32ddc6aafdc8aa943c2c8fadcdd4cbb0` | 0 |
| config/dnsbootstrap.go | 6440 | `efcb3756109ff29cd03668ce321ce01b8366e1ebf17e05d60aa2cb699eb2f4d0` | 0 |
| config/keyfile.go | 3700 | `944393304285b3860d416e0e329356be6693532d97502a5c904719a3d1f903dc` | 0 |
| config/localTemplate.go | 59403 | `edb46e8303c6e2ff6c98b8fe5859d6565de1e9206e25b3c6755aa97fa9bc26af` | 0 |
| config/local_defaults.go | 8748 | `53a2153bbe799e88ef033b74b347e7b52faf3fc90298173c9fd23f66a22c1bf4` | 0 |
| config/migrate.go | 11168 | `473dbdd29e877c96424cec94fedf8b6b9e2ab910cf15ef96c8c8c8b638f672e0` | 0 |
| config/version.go | 3871 | `a83495addfe80c4480a80c8526ad7aed0210d69c8ca1c1740a9557c2a6f40c62` | 0 |
| crypto/batchverifier.c | 991 | `749e07446e090ef31ef2370343a8384274938d59be70a2bfe4431c3791cd016d` | 0 |
| crypto/batchverifier.go | 8708 | `7430c9479111eed282ba68ba6551678f8d39d42717fd21b57d9dcfbdb0355163` | 0 |
| crypto/cryptoerror.go | 1396 | `2de90212164d64d5f1d5c83b03a61882c4ee8d503a2129d5534a78c455a0e710` | 0 |
| crypto/curve25519.go | 11276 | `4af08e9988afd9575d5d69faac5727ab3649531dfd923ecbb28ff71dd3606f41` | 0 |
| crypto/digest.go | 1476 | `15fbd5f0a14deb4e952caf042c933004cdb9a9fc1d9d1eac58ab270dfeea5f7d` | 0 |
| crypto/falconWrapper.go | 11123 | `4b8df2f298a7f1b90158056e50d28548f69da83e36740279d9109c266db6e54a` | 0 |
| crypto/gobatchverifier.go | 7019 | `208ff6fb1547cff0901629b3e6baf4c79560866221b1fcbe3aa5d4aa7d030938` | 0 |
| crypto/hashes.go | 4445 | `8c0661b5004bda25bb3ba27f939417eb2a5a77892401499b8f16814a550d27a8` | 0 |
| crypto/include/sodium.h | 2582 | `02fe3eddf4b03ec47415ecb8e0a502e603c323fbacddb2c2025576cd59a10e45` | 0 |
| crypto/include/sodium/core.h | 391 | `692c9a03eb49591a3ccacbef293f473c619cc86ef5dd4776a6e2e4321426fb07` | 0 |
| crypto/include/sodium/crypto_aead_aes256gcm.h | 7980 | `b45d4a101a1b08db991ecfac2c19d2c5c404667e65a2337487b8d8580e70200e` | 0 |
| crypto/include/sodium/crypto_aead_chacha20poly1305.h | 8782 | `829054e89c68f98c660c5f5cc65318e2fda345a888a0c337534a338bc96ee757` | 0 |
| crypto/include/sodium/crypto_aead_xchacha20poly1305.h | 4848 | `2e3467ee81b0a4a2edd36eafa2efe68f6d92562fba5871381c574b1195b54d73` | 0 |
| crypto/include/sodium/crypto_auth.h | 1131 | `18e3b4387bf3ef4683020e67272ea0af0e85be8b904e8b9ea1a6471baa539b55` | 0 |
| crypto/include/sodium/crypto_auth_hmacsha256.h | 2121 | `a583c3ec325ef74cbcaa3d472521c47f7ee34193a0313a22b3cc8170659928aa` | 0 |
| crypto/include/sodium/crypto_auth_hmacsha512.h | 2108 | `48115502c7ab894af5731820a130ebca95005e24a7a5bb25cd20b680d3a3a9f4` | 0 |
| crypto/include/sodium/crypto_auth_hmacsha512256.h | 2031 | `13537acc947f539a36a005c306164b164287be4937352a42330f969bfeaa1124` | 0 |
| crypto/include/sodium/crypto_box.h | 6763 | `dbb765369328122ad2e4bbe58d9bc0df705481e17369f4fdfb339ed0cdf13fe8` | 0 |
| crypto/include/sodium/crypto_box_curve25519xchacha20poly1305.h | 7903 | `b344debbbde7e9027bd7667c90ad2bab38522db4d5fb8db30d916bcb6e0f1de9` | 0 |
| crypto/include/sodium/crypto_box_curve25519xsalsa20poly1305.h | 4676 | `df8ec2022c04b2959482e2a1838503443a8432f65a5ddd700ec1bff7cb45af70` | 0 |
| crypto/include/sodium/crypto_core_ed25519.h | 2372 | `895b552e30c5585705a16868cb4f71660c4931e4cb79b7ee902dc3389709afb0` | 0 |
| crypto/include/sodium/crypto_core_hchacha20.h | 816 | `d2a265946fab3fddb8ee4b7ee6b3fb34b6526efa6ba45c6609c7e395ed302fc1` | 0 |
| crypto/include/sodium/crypto_core_hsalsa20.h | 804 | `5f9d48c0cdfcb8ce86a0e65cfa490cac0e9cacbca4aa864926593c691f69be63` | 0 |
| crypto/include/sodium/crypto_core_salsa20.h | 792 | `614992c472e5c2bad2ba8d90a4b6d9023db3774847e3541d5c87ad4cb59d69d0` | 0 |
| crypto/include/sodium/crypto_core_salsa2012.h | 816 | `1fce6f1b2a28c7764ba7ed99fefabefa2cbca688ce86e2574cc08ae235c8c3fd` | 0 |
| crypto/include/sodium/crypto_core_salsa208.h | 968 | `f5f40276f7f06f3478750037c56b8e29b1717588b75bd1a3769ccc54f73a709a` | 0 |
| crypto/include/sodium/crypto_generichash.h | 2492 | `89326c1af0eb23640509d4a63856a90a6cc34f36ad7d5e65ecf962a0a51782f7` | 0 |
| crypto/include/sodium/crypto_generichash_blake2b.h | 3960 | `85ee5ceb160ca0ccb12a33cb67811de37a987ce07b0e65b890a174979f564b8e` | 0 |
| crypto/include/sodium/crypto_hash.h | 898 | `4e3a0ca71f173dd56a6b114201c7f481a7094d381be6997fa1e0443b9fe02395` | 0 |
| crypto/include/sodium/crypto_hash_sha256.h | 1486 | `c2e01ef92d04de38d817599f0f25189cea06e6f9d094c02b60b5dac6e3f02970` | 0 |
| crypto/include/sodium/crypto_hash_sha512.h | 1490 | `51f5abaa6e44006ee59e3ef94aba28263f103e10da76b106ad8f7d10ff3dd7fe` | 0 |
| crypto/include/sodium/crypto_kdf.h | 1308 | `09901e619b1909e1802ace8f1e8b9ceb2218fd49c4ee430126802df7ff402525` | 0 |
| crypto/include/sodium/crypto_kdf_blake2b.h | 1071 | `2f0739ea610fb5c9ad8c453d84fac1d09e187f67096c70887f22c32a750e922b` | 0 |
| crypto/include/sodium/crypto_kx.h | 2201 | `b590d661674331aba7dade467ee902e1b61d0fe875bfc3780bd41b9e91dce316` | 0 |
| crypto/include/sodium/crypto_onetimeauth.h | 1897 | `dc60366896142461c994a8a72896ac8a10999fa2b58ccfdbcd0fc465f07a96c5` | 0 |
| crypto/include/sodium/crypto_onetimeauth_poly1305.h | 2183 | `d93ebefda0df2d67fdab0200910d7fed970c20a710b0c221a1843722b3e99878` | 0 |
| crypto/include/sodium/crypto_pwhash.h | 4966 | `e529cb84849008caf0dd2f3f1bac6808a0be9c963f9d2814f59badeda85d0c5b` | 0 |
| crypto/include/sodium/crypto_pwhash_argon2i.h | 3919 | `50a6b40ea240dd5f3b01198437ab56afabd050733ffa4d3dae5a90367e2e30ca` | 0 |
| crypto/include/sodium/crypto_pwhash_argon2id.h | 3981 | `15fe59b3b5b7ef6562b446f39d28ec4d97de06c662005f0d9aad6788d61b8155` | 0 |
| crypto/include/sodium/crypto_pwhash_scryptsalsa208sha256.h | 4688 | `5104ba3a227b676f0f8d3f0978d882b9d7ac683bf43c1d8995d6003e2ffe8e1f` | 0 |
| crypto/include/sodium/crypto_scalarmult.h | 1167 | `d71e80d4492e5e92ccc9208557aee63b86363bc2de1eed056b01c0ae0ea7fd29` | 0 |
| crypto/include/sodium/crypto_scalarmult_curve25519.h | 1081 | `f36d70d3691c358d3624b166b74071c79873a44d1115363c28af604d1dd1eb0a` | 0 |
| crypto/include/sodium/crypto_scalarmult_ed25519.h | 1389 | `ad50ed9c3a66304d5c2585935ac2bc9b2236345e314027d187c7b0a15d6f42dd` | 0 |
| crypto/include/sodium/crypto_secretbox.h | 3286 | `5871a0f6da4264f36d610170bf4304d8837d9ca54e85b3586f7b33a3856f3f40` | 0 |
| crypto/include/sodium/crypto_secretbox_xchacha20poly1305.h | 2832 | `bfc3f3ac1dc931b5c65a5ae29857a8343b7597ac4e36bdad017b5034ecc3dd2e` | 0 |
| crypto/include/sodium/crypto_secretbox_xsalsa20poly1305.h | 2410 | `a54a6ca892819f3a8baa91fa847685bf4cf2259a9467f1117ac7ae3268ca9b00` | 0 |
| crypto/include/sodium/crypto_secretstream_xchacha20poly1305.h | 3832 | `84f514317b7feb33b644b2c3fc45b9f012dd5cbda98aeb8086ec8f6d7029851f` | 0 |
| crypto/include/sodium/crypto_shorthash.h | 954 | `9a555d7608952c028e9fcbd3b959949c959b1aa22309e7f94c358603469bc2a9` | 0 |
| crypto/include/sodium/crypto_shorthash_siphash24.h | 1224 | `ab9cdc35b0077ae108c926aa57f6221d47fd2ce0f0b2cb87665d0ee885d2d7ff` | 0 |
| crypto/include/sodium/crypto_sign.h | 3350 | `3b93f7a9edeec30e8ff7256a1d73638fc3a44f53478cfe7306bf9c01ac61ea65` | 0 |
| crypto/include/sodium/crypto_sign_ed25519.h | 4300 | `5ec51cce0b8082e0af4c5bea491ab4dcaeba5650f59305649944e048a5dc4817` | 0 |
| crypto/include/sodium/crypto_sign_edwards25519sha512batch.h | 2056 | `0d4e4b174a6f09a41e0c8bd23009cf5c2bb81af304cfced2d8fbf00b553816d3` | 0 |
| crypto/include/sodium/crypto_stream.h | 1606 | `ae8d27cabc066b6e369e0a4d04f0aea1aced45145d8e176a21bdcf359c4001a0` | 0 |
| crypto/include/sodium/crypto_stream_chacha20.h | 3672 | `e6f0ef6cb1199bac25096f715fd9290e073c8a9e0fc03066699fed0fb800612b` | 0 |
| crypto/include/sodium/crypto_stream_salsa20.h | 1836 | `cf1c051d837eaea3b102c63683394e415d2d9ee2f885ba105312af7e13db03b8` | 0 |
| crypto/include/sodium/crypto_stream_salsa2012.h | 1532 | `bc65adc00270a7e18bd5acf3141c252bddb82a4628388299349ab94f9784bd8e` | 0 |
| crypto/include/sodium/crypto_stream_salsa208.h | 1731 | `5430b7f5a934a75ee4f5c8e9ed9ddc3cec7dd1032ac8bec35c7188da5d738fa2` | 0 |
| crypto/include/sodium/crypto_stream_xchacha20.h | 1875 | `dcaafd5679d02460b24fe877946458ff454f4e9d35c8e1f8f1f1b48d54c96698` | 0 |
| crypto/include/sodium/crypto_stream_xsalsa20.h | 1856 | `de812c7463a2ca0f4db6c6edb671277777f0aaccff85d86a471c7da932a09b0c` | 0 |
| crypto/include/sodium/crypto_verify_16.h | 419 | `d3b4fbea4b6d2bf23a9a079939a181625be76a006af129732af86bf4b544456c` | 0 |
| crypto/include/sodium/crypto_verify_32.h | 419 | `6ea1ea855b691a2b08510afe74f893d4ff44e40b14501d774d1a73dd79ad4e73` | 0 |
| crypto/include/sodium/crypto_verify_64.h | 419 | `9736126e6d38864b7c2aa0edf0075e3f6b1fe485a060067ce8c06afb340171a8` | 0 |
| crypto/include/sodium/crypto_vrf.h | 2132 | `644222b198d4e3565a750c4fa522bf3ca0800c8313def00fbcb4fd5a1db6e945` | 0 |
| crypto/include/sodium/crypto_vrf_ietfdraft03.h | 4200 | `b966fef7b111eb6fd061c3c20426b62b52189114ba098351c0e975cefbda69cf` | 0 |
| crypto/include/sodium/export.h | 1347 | `acc6ee537f831d535b0607be90f05150103765b7ca82170fd61a85bd5e6f73ff` | 0 |
| crypto/include/sodium/randombytes.h | 1847 | `41bf6745f8343b39a48861e9128bbff39ddd7f784d3e8c59a8fcbc55c6511c05` | 0 |
| crypto/include/sodium/randombytes_salsa20_random.h | 290 | `9d4dc30d99085bd9057fc01dd568e1bd1e7699d5dfa185bf630cd8f43e0ed921` | 0 |
| crypto/include/sodium/randombytes_sysrandom.h | 282 | `cdcc193ee76bb69626b7cb63b105db2f83796b7c365c9f4e42193fa9e654bfb6` | 0 |
| crypto/include/sodium/runtime.h | 889 | `5f618794bfa316c338bc166ffd21f00e5711a0ebf94aaa19440c88b0c94be023` | 0 |
| crypto/include/sodium/utils.h | 6316 | `d2aa29188313663ee4a6864b41023a22985024a520b9addbdafb453023a67145` | 0 |
| crypto/include/sodium/version.h | 509 | `1b6524c23b8580157dce7ecc1e339f6cefd4e8b0c00c4265a5bd6ae8357c99b1` | 0 |
| crypto/libsodium-fork/builds/msvc/resource.h | 387 | `564ceb99be50ffe51b1189e56c1f79fd2b2425ee07eefcee078e72e8944d2acc` | 0 |
| crypto/libsodium-fork/builds/msvc/version.h | 508 | `9bc31dd330e3e9619fcab1c051d855139adce2bcdab1669a981b7fb3e04e6199` | 0 |
| crypto/libsodium-fork/packaging/dotnet-core/prepare.py | 9485 | `76866e81b048e6b6262e973461a833baef2ef93ed087b3372f2b8c47bf7d312a` | 0 |
| crypto/libsodium-fork/regen-msvc/regen-msvc.py | 4843 | `8bd509609e111b135a62e3f477066aa6c851c28de9d5bd8509f57cd932525b41` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_aead/aes256gcm/aesni/aead_aes256gcm_aesni.c | 41636 | `e93e067e60b6e65e3b516a179515decbfcf86d6b0af905688d071fe8b24c3360` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_aead/chacha20poly1305/sodium/aead_chacha20poly1305.c | 14254 | `1d88a62bd4c28dd9d36974dc13981a2c19978ccaa7add04cfb486cc86ca3e494` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_aead/xchacha20poly1305/sodium/aead_xchacha20poly1305.c | 9406 | `26b35c0c0d49676817b3935cadc30e9f9e2c814f16916ea177767e78e5b1ea0d` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_auth/crypto_auth.c | 775 | `0949551db403830e60d0526a2074a12c9cdfc4772ea9706a6ed1e205b676d40c` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_auth/hmacsha256/auth_hmacsha256.c | 2947 | `b4074f8ee81ad6a3fe98ae144ecd6c68f61706ae297c2f78470c519a162fd9cd` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_auth/hmacsha512/auth_hmacsha512.c | 2953 | `804e3d9bf2e20d7d866a3fa1213fecf07c526a1d2a3d0adc0e94e546019e9b75` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_auth/hmacsha512256/auth_hmacsha512256.c | 2523 | `fd57c37bd05aa9f188e87ac30bdef3b267d3698887c40ee16f0f949646331125` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_box/crypto_box.c | 2383 | `8741972f4f816baaf1b7409cd6412b06f85b8d02ee9aef9161522f5591b50911` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_box/crypto_box_easy.c | 3676 | `a71a822831333a2c8a1780ad224861e0aa4bf665520c9e9428f323adfc90b0a8` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_box/crypto_box_seal.c | 1973 | `c9bed6c747a4c6446813a1a82edf3f4a995e11a8f9bf59c38a055d55200dd9d8` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_box/curve25519xchacha20poly1305/box_curve25519xchacha20poly1305.c | 6514 | `f7933b5b3d45003d6e1d3aac14b5eef62f8fa044d1819153937eaf70562583f0` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_box/curve25519xchacha20poly1305/box_seal_curve25519xchacha20poly1305.c | 3052 | `d72af55e9f5003a372b5d2bfa8dfe3ad76bc595ea683f6243d8f45b29ff48be1` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_box/curve25519xsalsa20poly1305/box_curve25519xsalsa20poly1305.c | 4576 | `64cec48c8189d560eb1400eedbaf591c2f40b31be258d6e4c3db09283deb1a70` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_core/ed25519/core_ed25519.c | 5513 | `2a9992c98b30c165a74680a03b1ce7b3bf1793b3b67e9ef819c3286b92bb94ca` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_core/ed25519/ref10/ed25519_ref10.c | 77395 | `3a050a80c509aab6d4f8339015a93e58a38156ded42f83c857f55d67196a96e0` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_core/ed25519/ref10/fe_25_5/base.h | 85502 | `4b55044010ee8b7270b5b58f3d064e1a5798966f3ecd317f287cb2ff61751fbc` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_core/ed25519/ref10/fe_25_5/base2.h | 2579 | `2ee371b7a19b20d076a93b47e06b0d8d7305a6e4501b7002ae16572aa19a258f` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_core/ed25519/ref10/fe_25_5/base_ge25519.h | 454 | `a829687160df579095392f286dcdfa1cbb84787f52a64fe63c9232d8aa9c9ea9` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_core/ed25519/ref10/fe_25_5/constants.h | 702 | `2ca8e949a77cc004cb618c50de87c35d8b72907283e4c87d885ac75a808032ed` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_core/ed25519/ref10/fe_25_5/fe.h | 5787 | `6fde442ea8b8a6f252948168ceb9f203abfd48f4e00c3cdd4070e26a4e28ef9e` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_core/ed25519/ref10/fe_51/base.h | 75894 | `ed3ae74d98c89ac5a3aebada53e7ddb22d00c1968b7838d04a10665b4e651869` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_core/ed25519/ref10/fe_51/base2.h | 2280 | `0e6cecfa1747abd6f7a09d6119b33cd435fb4b88ed3811bc002d81ccccfbd29c` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_core/ed25519/ref10/fe_51/base_ge25519.h | 396 | `a1cb63ed860fb9df7ca1de754c67f29a01d24d90d7962e59c47bf70748dc9b87` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_core/ed25519/ref10/fe_51/constants.h | 648 | `b690418b3a630d8fc2f2f3c3c471ea7bbcbaad13dd32aa3af3bd150fbc847058` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_core/ed25519/ref10/fe_51/fe.h | 2473 | `a96a476b0a0615636b5867e8a80f1f18c1084fd6d59a7967203a54bf090082fd` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_core/hchacha20/core_hchacha20.c | 2232 | `9c891c646f9e6ec20d0597464d5d987512697a3d5b00051ad9ed67501ebdecc9` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_core/hsalsa20/core_hsalsa20.c | 408 | `ecb3514e479cc993366542f9efe71de9aafd8f439cf9223f4ab0d97e9b97625a` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_core/hsalsa20/ref2/core_hsalsa20_ref2.c | 2571 | `d9fdd18eeaaf6964ecb30eee30314a32abd10360c660af253cdab83826026a13` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_core/salsa/ref/core_salsa_ref.c | 4812 | `64335b1e24b96e48b7b7791c2bb3165aa366e47da9d0f74f846c491b5b70989f` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_generichash/blake2b/generichash_blake2.c | 1216 | `dc60a6a9b7f2f668853596a547282ca47eb6b1a978a8906d93ce4d103e6bad44` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_generichash/blake2b/ref/blake2.h | 4543 | `cea6d217a1abb7058dbbafcf931fa65fe41a0a688d4b6b3a4e10ec972988f965` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_generichash/blake2b/ref/blake2b-compress-avx2.c | 1160 | `14a070b5b301f7dd023075c2929fb88697b83a438eedbdab11ec136994156343` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_generichash/blake2b/ref/blake2b-compress-avx2.h | 6103 | `d37dfeaf843ff7b264390dae4138cc8f976d859740b65cfed62ec5b604e53596` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_generichash/blake2b/ref/blake2b-compress-ref.c | 3002 | `7fd2ce5d123c9fdd71decb105156d69f91ceaff7437bcd81486a5b3f9ce7d1db` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_generichash/blake2b/ref/blake2b-compress-sse41.c | 2593 | `4f3de0b056a86ef2090ebf5a1db98238df56c607fa7cfaee8aa4f3359e6cb644` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_generichash/blake2b/ref/blake2b-compress-sse41.h | 6719 | `5a020c1492aef02727826f64056cf8725f79c30cd8aa7fb43f287ce1578f11f4` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_generichash/blake2b/ref/blake2b-compress-ssse3.c | 2930 | `2507623162b653296bca9feff58d4c0e67c8f2d3fda7babf6698beb0eb9fad43` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_generichash/blake2b/ref/blake2b-compress-ssse3.h | 6718 | `09c9c525c9505247fc2425d0cbe10d32805c91e06c3d4309f76be2f89a63482b` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_generichash/blake2b/ref/blake2b-load-avx2.h | 12895 | `d610f6ded2f16d9832ec71ba9bfd2954a779cb9117d1e5a4510436d8ff1c4400` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_generichash/blake2b/ref/blake2b-load-sse2.h | 5594 | `daa18d55dfaf3c9a29e7bf390ea0f92aaf291aa0d315d912ae0082fd61e0fe3f` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_generichash/blake2b/ref/blake2b-load-sse41.h | 10060 | `89a96cf99ea570e450f608c509c52f11cb9775de17d201ab0cc57805202a3ac2` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_generichash/blake2b/ref/blake2b-ref.c | 11817 | `b712bc4f00a81ecec8fef02825506334983fa99e549107dc175ff1f48e3b17f6` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_generichash/blake2b/ref/generichash_blake2b.c | 3977 | `6c6bb63b0c9944c215af776e7325489c087e49bc513bccf8e1a518db0b7fedde` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_generichash/crypto_generichash.c | 2037 | `dc974ba3ab8ffcbd2684df7a842ad79d641a3c47e6f3a033fc4876fe12f1fbce` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_hash/crypto_hash.c | 323 | `bdc3db640637230f93fa859bc2715ec5905d911d32817b2fdf3bbf787b98d293` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_hash/sha256/cp/hash_sha256_cp.c | 7939 | `1835e9e6e071d2d82a80d33359f3c90ab3a24bfd633e96f1b1536e3780838ee4` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_hash/sha256/hash_sha256.c | 205 | `27966cb51a4f2ccf00d226bbed169dca16246cbbed82fbfc2ca18f9b99829526` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_hash/sha512/cp/hash_sha512_cp.c | 9407 | `60f428ee3d3b124b45055b31aa93c2a71f86dcc37110f7fd103baa276fc7eef9` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_hash/sha512/hash_sha512.c | 205 | `fca3b25c288cff440005ac36c4247f8df5ff3d38117e260eae8366d78178b641` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_kdf/blake2b/kdf_blake2b.c | 1635 | `802fe22def270bacd8166a17a99259cb538c5e24a90efde0c266c487b3e83c95` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_kdf/crypto_kdf.c | 931 | `0279ed40772be2c0f8c03e134026ccd8da2d1c3f756e9cab4d978d68dfaca283` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_kx/crypto_kx.c | 4379 | `c48d3aceab62c58ce5f8a9e57c347d698b65e0181ad026dd75c279d4a02b3f15` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_onetimeauth/crypto_onetimeauth.c | 1691 | `f9ccd6b3801c5819855a24bc3a0ad3ed4a9f397d59286fd4b9cff2063051711e` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_onetimeauth/poly1305/donna/poly1305_donna.c | 3494 | `ccbfba9202f7f7e318043bc9eb518277fadd171082202f85676a8f800287bf32` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_onetimeauth/poly1305/donna/poly1305_donna.h | 293 | `fe81733c21c22b47b8217627d40709e0d2f96fbfa385f2346ce697b7cebdd89b` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_onetimeauth/poly1305/donna/poly1305_donna32.h | 6729 | `40536f083dfaa6c969e71cb941669e863b7c6a34321b1804421fea8b1af646bd` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_onetimeauth/poly1305/donna/poly1305_donna64.h | 5235 | `03f93315a9a06be40cf8da8845f4d11595521481b1ff757344b1c2e5336ca7b2` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_onetimeauth/poly1305/onetimeauth_poly1305.c | 2464 | `0bbd1eec53c47abe43246962c8e655f7c159d152205b107c09d189e8d92792ad` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_onetimeauth/poly1305/onetimeauth_poly1305.h | 1016 | `7481732850bbe2cfbf6034581dfb8ab17b9005d2d22afdb030319072d637d1d3` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_onetimeauth/poly1305/sse2/poly1305_sse2.c | 31319 | `058d06d9dac94916e76c70f8d34e2a2deab17056fa237a39bea530b81785e731` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_onetimeauth/poly1305/sse2/poly1305_sse2.h | 289 | `689ac732de5fbf2f1552306e76e2edaa55057512599a3e1dce32b84ebfb6defa` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_pwhash/argon2/argon2-core.c | 15615 | `6fff070f8f439e386f4a5d62065131b91dea3205bf217f610c2b73f242c69a0c` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_pwhash/argon2/argon2-core.h | 10216 | `de8d5f5a2c0fd3c57f941ed72bf625f2d54afb3db09a6fe19ba1120c27656893` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_pwhash/argon2/argon2-encoding.c | 10254 | `9cee75b62668cab99398f595b9a571d3136fd6bc35e60679d9cfba25ccad25f2` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_pwhash/argon2/argon2-encoding.h | 1064 | `932ff34acb1861ba418b85ad69c66a214b2cb62bf941cf9eb8220b8f9aaa1e4e` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_pwhash/argon2/argon2-fill-block-avx2.c | 8023 | `8192730e7e3c335d3a1924893b832e83832a3e87c7a26615bd4ae964d4509036` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_pwhash/argon2/argon2-fill-block-avx512f.c | 8208 | `1ee75ff725441be5c6f493f14ab3e14e427fd2bd33c27a2ac2bc3e84c80caacb` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_pwhash/argon2/argon2-fill-block-ref.c | 8576 | `5fbbace0055d92056cdcd7621a9694de1ef7046542f710e1a478c04b0ab423ba` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_pwhash/argon2/argon2-fill-block-ssse3.c | 7943 | `b57e67f3c976bbfec062815b1ce0b3afc796c1bd80fea3868c60119c083408f7` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_pwhash/argon2/argon2.c | 8063 | `3621714cd3677ecd346819a1e2e8b3e446a1465a5f35c2a8da1a5deae43587d3` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_pwhash/argon2/argon2.h | 11085 | `ffc82383ad8ad1aaff540975379dbba370e7bd40c23cdf3260aab8cb4922d41a` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_pwhash/argon2/blake2b-long.c | 3137 | `37f1b01973dd484e009346bc46d7eb16e74d2f9b5186c29f2d8df4a1d286ef2d` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_pwhash/argon2/blake2b-long.h | 151 | `541220c3cd78acb15a80398a4b732e3ed7cf4b8fac531fb99c574b97ef826557` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_pwhash/argon2/blamka-round-avx2.h | 5847 | `abcfd03ed9a4d26ca96fe493925019f21cd44fb22738385e09aa554ba3d21ff5` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_pwhash/argon2/blamka-round-avx512f.h | 4569 | `256cd0cad160e7c30ee9243a5e796566645a708f8ae1e52d32fa24efc78d0fa6` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_pwhash/argon2/blamka-round-ref.h | 1555 | `619594355542219396a9545b4ee4afbb7eae8493784fb9aca01a72e3cd9021a3` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_pwhash/argon2/blamka-round-ssse3.h | 5451 | `60b0f267e9b16ae6af9017b1d1ce6977eecaef7b8894444fadd0b670d1624f00` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_pwhash/argon2/pwhash_argon2i.c | 7970 | `3bd2226d68477e867c3c955c7673a9db9d643f202b48cf01ed589a37485bf395` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_pwhash/argon2/pwhash_argon2id.c | 6382 | `378829c702b6d957e3ee0c694e62e623e98840e2925f3c3e0289402f4f3a3187` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_pwhash/crypto_pwhash.c | 4779 | `318a2d22a9f50f16fffccb7c61b61a578a7f608ea49cd87baa8ab5013fde795d` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_pwhash/scryptsalsa208sha256/crypto_scrypt-common.c | 7069 | `93de04c2711f75a886ad362ed6867782c4cfce611f468b71fb779ac377d563e2` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_pwhash/scryptsalsa208sha256/crypto_scrypt.h | 4130 | `6de9449b535cd5ee647138178c6e0b26f18052bc1061dd0861efc1614cc6db62` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_pwhash/scryptsalsa208sha256/nosse/pwhash_scryptsalsa208sha256_nosse.c | 10502 | `8893227b3aee1407b2b21614b162f484ad565c65ecb8b6c3d9e11041c1019140` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_pwhash/scryptsalsa208sha256/pbkdf2-sha256.c | 3534 | `21a4267540c36c52ddada2dbd733e361f566ff41eca2594311b87f56bc93ffed` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_pwhash/scryptsalsa208sha256/pbkdf2-sha256.h | 1870 | `98e99b1ac7599d8acde7cc2a76f6b342ac1803278ddc65850100c2a13fd58142` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_pwhash/scryptsalsa208sha256/pwhash_scryptsalsa208sha256.c | 8658 | `2c5df00871269c03c01f765d55b7c26fa3cc4af958668af9534ab2f97e12a8a2` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_pwhash/scryptsalsa208sha256/scrypt_platform.c | 2862 | `2e6822a7217899484f1c7d02d35568696818daddbfc8c82f905a9ce551f58f6a` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_pwhash/scryptsalsa208sha256/sse/pwhash_scryptsalsa208sha256_sse.c | 12450 | `cfc8111717193a4d450220753e2a44674b2465691d21d3afb0c45b98dd619dd0` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_scalarmult/crypto_scalarmult.c | 579 | `3aa1ce5272c4d77a0b03791becff2949a82db8c590dc10a423802984cbc08e99` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_scalarmult/curve25519/ref10/x25519_ref10.c | 5809 | `43c5c77e287775cc576a6ef64a6f669169ef8aecf8fb4fff791e5607137c611a` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_scalarmult/curve25519/ref10/x25519_ref10.h | 249 | `b9d6e13c9065f7f6f5d9fbff21f28bbc4956967b9bde802df172194702a05a9f` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_scalarmult/curve25519/sandy2x/consts_namespace.h | 906 | `7d2dd849708eafd885e6b72f38094a78bb75b13fbf581663b4882399b61ea5d6` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_scalarmult/curve25519/sandy2x/curve25519_sandy2x.c | 2555 | `b71a538b73766b07313cf982af1fefdec0be8592b993624d872d21d74fa8dce9` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_scalarmult/curve25519/sandy2x/curve25519_sandy2x.h | 225 | `3cd4f3ecc9f202e64c88a134452e4a23d1ce67b404935b73ed50280b32865859` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_scalarmult/curve25519/sandy2x/fe.h | 550 | `2274ea02748ade547d39084c2f5b41cd7f068ec2b648d2bf7dd6a55b07299a96` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_scalarmult/curve25519/sandy2x/fe51.h | 614 | `034410eea5c360bdb5ed5e2258e4d260363cececf00bbdad78369ca0e4463561` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_scalarmult/curve25519/sandy2x/fe51_invert.c | 1482 | `572e6a03f0f172c6d3f78ae9ad8df4e3b28215074220bf146fd707db3acaba57` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_scalarmult/curve25519/sandy2x/fe51_namespace.h | 753 | `74b2538f5ce69a87716264c763de047f31308a6e5a7cd912925b6ecd1b619ac6` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_scalarmult/curve25519/sandy2x/fe_frombytes_sandy2x.c | 1790 | `5bc870db6fcd8b2f52bde8b0a5a47e799ca361b1eaac98190c0258c81a5b108d` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_scalarmult/curve25519/sandy2x/ladder.h | 231 | `d4fddfc1d132c0b00ae8b50624c74de133e156dc498628eedcdb87a2c1c18fe1` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_scalarmult/curve25519/sandy2x/ladder_base.h | 256 | `4fb8a727d842fd44a660e677d9487045c6f0a1bd07f8d117c55c3b9a57e90e67` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_scalarmult/curve25519/sandy2x/ladder_base_namespace.h | 253 | `5d81a455988ec7b3ba673de0f027db4d5a54b634416dcb7df96a707898ed427c` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_scalarmult/curve25519/sandy2x/ladder_namespace.h | 218 | `3389364a25ea0a948f0fabe97635aff03cdb5f9d59fc21a1ae1c55c18aa968c3` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_scalarmult/curve25519/scalarmult_curve25519.c | 1427 | `64f473f5069dcb892b196019475f31f571ba46ac79ba31047010c2c506dafb87` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_scalarmult/curve25519/scalarmult_curve25519.h | 341 | `c887fe855f943cb70a0967bba811f9ac97d254f213930d96e9fb2ffdc71015e1` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_scalarmult/ed25519/ref10/scalarmult_ed25519_ref10.c | 2721 | `813a32242f69796468f434b3bca15d8abb8c2406f426945651ffbaec6b1cf717` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_secretbox/crypto_secretbox.c | 1295 | `7c9a3e3a11e709094c3c5fbdf0851810427dbca514c69bb22aabd97c148731a3` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_secretbox/crypto_secretbox_easy.c | 4915 | `6ff8e9d9420c898c99631d484a562abc5042c7ef6b5559e6765097449200f2c2` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_secretbox/xchacha20poly1305/secretbox_xchacha20poly1305.c | 6343 | `495923b6fc551cc10e667ebf031776a1ae3744d1445e1ffac0dfa767b4fd1a63` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_secretbox/xsalsa20poly1305/secretbox_xsalsa20poly1305.c | 2252 | `58d45fe808876822dd31820190dfe94da3a0c17d7451c1e66190d321f0d2abc9` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_secretstream/xchacha20poly1305/secretstream_xchacha20poly1305.c | 11380 | `b9bd13b46d0d0332c69069d3f829fcf30d267e584a998a6379f8a89b9b3ffb22` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_shorthash/crypto_shorthash.c | 629 | `b4f5e2bd83496b9ef0c5334c104f9c6a4e2dc1b8f46dc12a5de01c3de3900fc0` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_shorthash/siphash24/ref/shorthash_siphash24_ref.c | 1697 | `04f3d382837c2589d3959ff44351b716e55c16a886297aefcda0b77b272d5796` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_shorthash/siphash24/ref/shorthash_siphash_ref.h | 606 | `51548a9d39274f75b1a0054d8b0318cd5f1ecb6d24b58e1e3a0c2fcf248b7f0a` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_shorthash/siphash24/ref/shorthash_siphashx24_ref.c | 1781 | `3df5a0a7b46d0f69be027879c8fa3ffb0be0b6b54e687fb24d2ef1b0121f2d25` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_shorthash/siphash24/shorthash_siphash24.c | 238 | `72465eaaa527e9d42b2d6dd645069b64e30402de973cc972f114688c85ef7c83` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_shorthash/siphash24/shorthash_siphashx24.c | 242 | `48cb227728cdae63b7dfe0246f8c6d7e998f4dfe57f53fd492a4157ffbca1f27` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_sign/crypto_sign.c | 3040 | `a00bb94a7a5e64b4c921a6c26925a613c88617c4cf8e888896a825b9f03b03ce` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_sign/ed25519/ref10/batch.c | 9715 | `9a2f278687786ef804509eb43702f366ee6fefed5039f23da2e1e1b5bbd6e09d` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_sign/ed25519/ref10/keypair.c | 1978 | `ef0d2cde816c39e4fd6d61a37e33fbbcd7192c78430477a763dada8822a319aa` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_sign/ed25519/ref10/obsolete.c | 3432 | `3bb6cf66cb5fde743980aeba0c1acbfd12c178168df68d804c5b49839c00841e` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_sign/ed25519/ref10/open.c | 2638 | `2b345bf78695844262832eb14d0655da3a815024db0d437791142ee3b34b062d` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_sign/ed25519/ref10/open_bv_compat.c | 3477 | `c2c3e9f3b936efb008f6dcb0082856776e6c8a3133f1935e44b7c7e7a5195b89` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_sign/ed25519/ref10/sign.c | 4356 | `39333c0e1652f3990c3e1e578a3c01d6d1d555e21458c4acb8b71accb2b1b940` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_sign/ed25519/ref10/sign_ed25519_ref10.h | 1584 | `b25e3c08b5ff1cfae1e93c33aa13dac240f950f9715ef7dc05050f96b65b4426` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_sign/ed25519/sign_ed25519.c | 2663 | `a0403685845114f8e84c0196cdd42699477e07121cd916d2f35472a2c70a69fc` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_stream/chacha20/dolbeau/chacha20_dolbeau-avx2.c | 4615 | `c35913b69aab652192e7f5a5fb05e01c6b86ce0432e3bc3aabfc9714308994a3` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_stream/chacha20/dolbeau/chacha20_dolbeau-avx2.h | 199 | `4bc87ed826dbf7beadd2b41c01bf6e7fb846ff941cd6e1c8da870310ec8aaab7` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_stream/chacha20/dolbeau/chacha20_dolbeau-ssse3.c | 4423 | `729df4cd33f1b6c54d420084c4bc8cac39da500a14651936a7b593c9c69e41cc` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_stream/chacha20/dolbeau/chacha20_dolbeau-ssse3.h | 200 | `26c77341fe9573788065f4ac77a2bd92bc55bab093c61518728ddc4abfd388a3` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_stream/chacha20/dolbeau/u0.h | 2872 | `19cf10cdd56122220d38647df58b5f7e331a75a00e2fa4d178225184b3fd7dd2` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_stream/chacha20/dolbeau/u1.h | 3168 | `455c1d8d854e274488f7b5b7659ad13c9ca5c3f28bad3f16e9be646abaf1d309` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_stream/chacha20/dolbeau/u4.h | 6574 | `b073331f5da9350214bcc6cd0905315b6af6a94245244cc628195f7ca43056c7` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_stream/chacha20/dolbeau/u8.h | 18061 | `020fda6dff06db8646bd973fd8d6c7a66b78af1774fbe1639b20b01225dcabb9` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_stream/chacha20/ref/chacha20_ref.c | 8466 | `a93ebb4cc15c590798cb095d48ed39eb5d8929fda7904ce148908485e38914c3` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_stream/chacha20/ref/chacha20_ref.h | 190 | `04942a791be36ecd42568d9ee34b751f4ff8a02d919fa8b16e1a6e604d246726` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_stream/chacha20/stream_chacha20.c | 5623 | `119f02db875d0b293631b3756884f659fb3c80754ac79857876e8d0cecff9c38` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_stream/chacha20/stream_chacha20.h | 947 | `91848ca3f4b7badcf29aa8b03d3179a20e4ff4d4662f64d42612a2b0a9a367b3` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_stream/crypto_stream.c | 919 | `c22d3728361f741eb89c220d0f2289168e1cf4ccc129f4bf6f6858dc209184f3` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_stream/salsa20/ref/salsa20_ref.c | 2665 | `e47d9a29430d6ee4d2f7789e309984bf98997b3e5e7665f4efb006b705d50fc2` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_stream/salsa20/ref/salsa20_ref.h | 186 | `6ae5115492511b18007b3561562d83b09248a8f34f86318813ced358ee7622fb` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_stream/salsa20/stream_salsa20.c | 2770 | `3c61a4a21512fca10a7555acb99c76d2e1992777994930fd8bd49265935ba84c` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_stream/salsa20/stream_salsa20.h | 532 | `c726237642e7c269fabbc2442f2ce008b0de9a2cf90469758853d78f27a1eee6` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_stream/salsa20/xmm6/salsa20_xmm6.c | 852 | `c3c8230ca99c8b79182ef706d22b32f9b47656884a80cd5e92effb6569dddefe` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_stream/salsa20/xmm6/salsa20_xmm6.h | 187 | `b56e570bfa5e15910a3b2c4fcc5999b7b8ac5f754e5f70bcb9ed938c211ac09d` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_stream/salsa20/xmm6int/salsa20_xmm6int-avx2.c | 3296 | `ca3783de60a965a6f41b2c4759a9218864a01ba3585dfe345343924e255644da` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_stream/salsa20/xmm6int/salsa20_xmm6int-avx2.h | 195 | `bfbc9a2d6513fdab5ede6dc8cec1f2f6a555a08aefef7e0b1b18c1017793c72a` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_stream/salsa20/xmm6int/salsa20_xmm6int-sse2.c | 3023 | `51a4af9211dcb908ca1b0368e54c0b3bdda4b1076f672d5f06773961c0b05d57` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_stream/salsa20/xmm6int/salsa20_xmm6int-sse2.h | 195 | `839d059a0ba385066a969bf582e1f9d9969d825b5d8debe778937de4e5de8bc3` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_stream/salsa20/xmm6int/u0.h | 6879 | `5d0f8743a38dee11ff160fc6a2f30c976548edb7479c17040d0e43865b8f10ed` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_stream/salsa20/xmm6int/u1.h | 6814 | `f35de0b5967c7f1ce03700f4f2d23783b34441216036aa745b9707305d4e6eae` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_stream/salsa20/xmm6int/u4.h | 19408 | `3bf51e537e7fa8ffe3db2dedf87c990ae7d6e90cfc1aa1ca666807ba7a65493b` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_stream/salsa20/xmm6int/u8.h | 18674 | `f06f540318841dcf94483aabf2511da791ba1d6a68d1f42665ced9a54d9d6715` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_stream/salsa2012/ref/stream_salsa2012_ref.c | 2370 | `20cc0512f97f70bcf65561e9bef9f0b042ab49640c443d7e9d454d2401ca166a` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_stream/salsa2012/stream_salsa2012.c | 520 | `2aaba5e9e9c6db319ff14e5dea314e911cfb10298430d202d66cea3f33b484dd` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_stream/salsa208/ref/stream_salsa208_ref.c | 2359 | `b9cddcf73aaef798b5c5359d7e629b1859fd8885ddd5b7889977ab17af74b923` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_stream/salsa208/stream_salsa208.c | 510 | `0e8ff1ff21298538da4ec94d6edfdd541f7ee97a421956a8323eafb5ba85e662` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_stream/xchacha20/stream_xchacha20.c | 1969 | `db04ab9c17b43330c0c109ca8c545e7cc9cae106b6313ca6b04cf80c113558b1` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_stream/xsalsa20/stream_xsalsa20.c | 1692 | `0c3d8b9b45ee606ac9b7a4b651347e72b2f629e6d17e513c7a7aa161058c4aec` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_verify/sodium/verify.c | 2296 | `2af44fcbde7abb7aacba6629689d19fea98b8dda19fd7d53c3186c077ee97e86` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_vrf/crypto_vrf.c | 1725 | `46a3714d0cacb35ca103795be060844805305bf4af46073fd7f2383b0423205a` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_vrf/ietfdraft03/convert.c | 4374 | `0c5f5aa53637c8cdfc46eff6998bf11f1497238013414f17eef97b0302e6c8c4` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_vrf/ietfdraft03/keypair.c | 1401 | `a4af749c3c5bade4d249e37673a9461b5f7e556986fa6a4d1921f401aa879404` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_vrf/ietfdraft03/prove.c | 6366 | `d173b9b8b14baca3d6228fe34b6f1f54dd2df647ad54a3b8479157fcbcfa5b46` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_vrf/ietfdraft03/verify.c | 7732 | `2d23eff2ec13d93cc3de6478f9d99b2f50b5bf59b6d0db9fc29ec04f47b060be` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_vrf/ietfdraft03/vrf.c | 1605 | `999f0301c08eee4d3e12e0faf4d52969d9eea5e6df58865252f029239b26c877` | 0 |
| crypto/libsodium-fork/src/libsodium/crypto_vrf/ietfdraft03/vrf_ietfdraft03.h | 1903 | `793c9fc7251173a25928eff2cf3cce58ded524b79741e67ae972f0002d2f5db9` | 0 |
| crypto/libsodium-fork/src/libsodium/include/sodium.h | 2582 | `02fe3eddf4b03ec47415ecb8e0a502e603c323fbacddb2c2025576cd59a10e45` | 0 |
| crypto/libsodium-fork/src/libsodium/include/sodium/core.h | 391 | `692c9a03eb49591a3ccacbef293f473c619cc86ef5dd4776a6e2e4321426fb07` | 0 |
| crypto/libsodium-fork/src/libsodium/include/sodium/crypto_aead_aes256gcm.h | 7980 | `b45d4a101a1b08db991ecfac2c19d2c5c404667e65a2337487b8d8580e70200e` | 0 |
| crypto/libsodium-fork/src/libsodium/include/sodium/crypto_aead_chacha20poly1305.h | 8782 | `829054e89c68f98c660c5f5cc65318e2fda345a888a0c337534a338bc96ee757` | 0 |
| crypto/libsodium-fork/src/libsodium/include/sodium/crypto_aead_xchacha20poly1305.h | 4848 | `2e3467ee81b0a4a2edd36eafa2efe68f6d92562fba5871381c574b1195b54d73` | 0 |
| crypto/libsodium-fork/src/libsodium/include/sodium/crypto_auth.h | 1131 | `18e3b4387bf3ef4683020e67272ea0af0e85be8b904e8b9ea1a6471baa539b55` | 0 |
| crypto/libsodium-fork/src/libsodium/include/sodium/crypto_auth_hmacsha256.h | 2121 | `a583c3ec325ef74cbcaa3d472521c47f7ee34193a0313a22b3cc8170659928aa` | 0 |
| crypto/libsodium-fork/src/libsodium/include/sodium/crypto_auth_hmacsha512.h | 2108 | `48115502c7ab894af5731820a130ebca95005e24a7a5bb25cd20b680d3a3a9f4` | 0 |
| crypto/libsodium-fork/src/libsodium/include/sodium/crypto_auth_hmacsha512256.h | 2031 | `13537acc947f539a36a005c306164b164287be4937352a42330f969bfeaa1124` | 0 |
| crypto/libsodium-fork/src/libsodium/include/sodium/crypto_box.h | 6763 | `dbb765369328122ad2e4bbe58d9bc0df705481e17369f4fdfb339ed0cdf13fe8` | 0 |
| crypto/libsodium-fork/src/libsodium/include/sodium/crypto_box_curve25519xchacha20poly1305.h | 7903 | `b344debbbde7e9027bd7667c90ad2bab38522db4d5fb8db30d916bcb6e0f1de9` | 0 |
| crypto/libsodium-fork/src/libsodium/include/sodium/crypto_box_curve25519xsalsa20poly1305.h | 4676 | `df8ec2022c04b2959482e2a1838503443a8432f65a5ddd700ec1bff7cb45af70` | 0 |
| crypto/libsodium-fork/src/libsodium/include/sodium/crypto_core_ed25519.h | 2372 | `895b552e30c5585705a16868cb4f71660c4931e4cb79b7ee902dc3389709afb0` | 0 |
| crypto/libsodium-fork/src/libsodium/include/sodium/crypto_core_hchacha20.h | 816 | `d2a265946fab3fddb8ee4b7ee6b3fb34b6526efa6ba45c6609c7e395ed302fc1` | 0 |
| crypto/libsodium-fork/src/libsodium/include/sodium/crypto_core_hsalsa20.h | 804 | `5f9d48c0cdfcb8ce86a0e65cfa490cac0e9cacbca4aa864926593c691f69be63` | 0 |
| crypto/libsodium-fork/src/libsodium/include/sodium/crypto_core_salsa20.h | 792 | `614992c472e5c2bad2ba8d90a4b6d9023db3774847e3541d5c87ad4cb59d69d0` | 0 |
| crypto/libsodium-fork/src/libsodium/include/sodium/crypto_core_salsa2012.h | 816 | `1fce6f1b2a28c7764ba7ed99fefabefa2cbca688ce86e2574cc08ae235c8c3fd` | 0 |
| crypto/libsodium-fork/src/libsodium/include/sodium/crypto_core_salsa208.h | 968 | `f5f40276f7f06f3478750037c56b8e29b1717588b75bd1a3769ccc54f73a709a` | 0 |
| crypto/libsodium-fork/src/libsodium/include/sodium/crypto_generichash.h | 2492 | `89326c1af0eb23640509d4a63856a90a6cc34f36ad7d5e65ecf962a0a51782f7` | 0 |
| crypto/libsodium-fork/src/libsodium/include/sodium/crypto_generichash_blake2b.h | 3960 | `85ee5ceb160ca0ccb12a33cb67811de37a987ce07b0e65b890a174979f564b8e` | 0 |
| crypto/libsodium-fork/src/libsodium/include/sodium/crypto_hash.h | 898 | `4e3a0ca71f173dd56a6b114201c7f481a7094d381be6997fa1e0443b9fe02395` | 0 |
| crypto/libsodium-fork/src/libsodium/include/sodium/crypto_hash_sha256.h | 1486 | `c2e01ef92d04de38d817599f0f25189cea06e6f9d094c02b60b5dac6e3f02970` | 0 |
| crypto/libsodium-fork/src/libsodium/include/sodium/crypto_hash_sha512.h | 1490 | `51f5abaa6e44006ee59e3ef94aba28263f103e10da76b106ad8f7d10ff3dd7fe` | 0 |
| crypto/libsodium-fork/src/libsodium/include/sodium/crypto_kdf.h | 1308 | `09901e619b1909e1802ace8f1e8b9ceb2218fd49c4ee430126802df7ff402525` | 0 |
| crypto/libsodium-fork/src/libsodium/include/sodium/crypto_kdf_blake2b.h | 1071 | `2f0739ea610fb5c9ad8c453d84fac1d09e187f67096c70887f22c32a750e922b` | 0 |
| crypto/libsodium-fork/src/libsodium/include/sodium/crypto_kx.h | 2201 | `b590d661674331aba7dade467ee902e1b61d0fe875bfc3780bd41b9e91dce316` | 0 |
| crypto/libsodium-fork/src/libsodium/include/sodium/crypto_onetimeauth.h | 1897 | `dc60366896142461c994a8a72896ac8a10999fa2b58ccfdbcd0fc465f07a96c5` | 0 |
| crypto/libsodium-fork/src/libsodium/include/sodium/crypto_onetimeauth_poly1305.h | 2183 | `d93ebefda0df2d67fdab0200910d7fed970c20a710b0c221a1843722b3e99878` | 0 |
| crypto/libsodium-fork/src/libsodium/include/sodium/crypto_pwhash.h | 4966 | `e529cb84849008caf0dd2f3f1bac6808a0be9c963f9d2814f59badeda85d0c5b` | 0 |
| crypto/libsodium-fork/src/libsodium/include/sodium/crypto_pwhash_argon2i.h | 3919 | `50a6b40ea240dd5f3b01198437ab56afabd050733ffa4d3dae5a90367e2e30ca` | 0 |
| crypto/libsodium-fork/src/libsodium/include/sodium/crypto_pwhash_argon2id.h | 3981 | `15fe59b3b5b7ef6562b446f39d28ec4d97de06c662005f0d9aad6788d61b8155` | 0 |
| crypto/libsodium-fork/src/libsodium/include/sodium/crypto_pwhash_scryptsalsa208sha256.h | 4688 | `5104ba3a227b676f0f8d3f0978d882b9d7ac683bf43c1d8995d6003e2ffe8e1f` | 0 |
| crypto/libsodium-fork/src/libsodium/include/sodium/crypto_scalarmult.h | 1167 | `d71e80d4492e5e92ccc9208557aee63b86363bc2de1eed056b01c0ae0ea7fd29` | 0 |
| crypto/libsodium-fork/src/libsodium/include/sodium/crypto_scalarmult_curve25519.h | 1081 | `f36d70d3691c358d3624b166b74071c79873a44d1115363c28af604d1dd1eb0a` | 0 |
| crypto/libsodium-fork/src/libsodium/include/sodium/crypto_scalarmult_ed25519.h | 1389 | `ad50ed9c3a66304d5c2585935ac2bc9b2236345e314027d187c7b0a15d6f42dd` | 0 |
| crypto/libsodium-fork/src/libsodium/include/sodium/crypto_secretbox.h | 3286 | `5871a0f6da4264f36d610170bf4304d8837d9ca54e85b3586f7b33a3856f3f40` | 0 |
| crypto/libsodium-fork/src/libsodium/include/sodium/crypto_secretbox_xchacha20poly1305.h | 2832 | `bfc3f3ac1dc931b5c65a5ae29857a8343b7597ac4e36bdad017b5034ecc3dd2e` | 0 |
| crypto/libsodium-fork/src/libsodium/include/sodium/crypto_secretbox_xsalsa20poly1305.h | 2410 | `a54a6ca892819f3a8baa91fa847685bf4cf2259a9467f1117ac7ae3268ca9b00` | 0 |
| crypto/libsodium-fork/src/libsodium/include/sodium/crypto_secretstream_xchacha20poly1305.h | 3832 | `84f514317b7feb33b644b2c3fc45b9f012dd5cbda98aeb8086ec8f6d7029851f` | 0 |
| crypto/libsodium-fork/src/libsodium/include/sodium/crypto_shorthash.h | 954 | `9a555d7608952c028e9fcbd3b959949c959b1aa22309e7f94c358603469bc2a9` | 0 |
| crypto/libsodium-fork/src/libsodium/include/sodium/crypto_shorthash_siphash24.h | 1224 | `ab9cdc35b0077ae108c926aa57f6221d47fd2ce0f0b2cb87665d0ee885d2d7ff` | 0 |
| crypto/libsodium-fork/src/libsodium/include/sodium/crypto_sign.h | 4441 | `4738fecec706dc70d2ec2b3b95523c1f3671e860a8dc81872e88a4cfd8ebb23e` | 0 |
| crypto/libsodium-fork/src/libsodium/include/sodium/crypto_sign_ed25519.h | 4948 | `351489c2d0f7be7b0f132a820be6b7768b6d62eb9dcee834f973c33dd5c0dcd0` | 0 |
| crypto/libsodium-fork/src/libsodium/include/sodium/crypto_sign_edwards25519sha512batch.h | 2056 | `0d4e4b174a6f09a41e0c8bd23009cf5c2bb81af304cfced2d8fbf00b553816d3` | 0 |
| crypto/libsodium-fork/src/libsodium/include/sodium/crypto_stream.h | 1606 | `ae8d27cabc066b6e369e0a4d04f0aea1aced45145d8e176a21bdcf359c4001a0` | 0 |
| crypto/libsodium-fork/src/libsodium/include/sodium/crypto_stream_chacha20.h | 3672 | `e6f0ef6cb1199bac25096f715fd9290e073c8a9e0fc03066699fed0fb800612b` | 0 |
| crypto/libsodium-fork/src/libsodium/include/sodium/crypto_stream_salsa20.h | 1836 | `cf1c051d837eaea3b102c63683394e415d2d9ee2f885ba105312af7e13db03b8` | 0 |
| crypto/libsodium-fork/src/libsodium/include/sodium/crypto_stream_salsa2012.h | 1532 | `bc65adc00270a7e18bd5acf3141c252bddb82a4628388299349ab94f9784bd8e` | 0 |
| crypto/libsodium-fork/src/libsodium/include/sodium/crypto_stream_salsa208.h | 1731 | `5430b7f5a934a75ee4f5c8e9ed9ddc3cec7dd1032ac8bec35c7188da5d738fa2` | 0 |
| crypto/libsodium-fork/src/libsodium/include/sodium/crypto_stream_xchacha20.h | 1875 | `dcaafd5679d02460b24fe877946458ff454f4e9d35c8e1f8f1f1b48d54c96698` | 0 |
| crypto/libsodium-fork/src/libsodium/include/sodium/crypto_stream_xsalsa20.h | 1856 | `de812c7463a2ca0f4db6c6edb671277777f0aaccff85d86a471c7da932a09b0c` | 0 |
| crypto/libsodium-fork/src/libsodium/include/sodium/crypto_verify_16.h | 419 | `d3b4fbea4b6d2bf23a9a079939a181625be76a006af129732af86bf4b544456c` | 0 |
| crypto/libsodium-fork/src/libsodium/include/sodium/crypto_verify_32.h | 419 | `6ea1ea855b691a2b08510afe74f893d4ff44e40b14501d774d1a73dd79ad4e73` | 0 |
| crypto/libsodium-fork/src/libsodium/include/sodium/crypto_verify_64.h | 419 | `9736126e6d38864b7c2aa0edf0075e3f6b1fe485a060067ce8c06afb340171a8` | 0 |
| crypto/libsodium-fork/src/libsodium/include/sodium/crypto_vrf.h | 2132 | `644222b198d4e3565a750c4fa522bf3ca0800c8313def00fbcb4fd5a1db6e945` | 0 |
| crypto/libsodium-fork/src/libsodium/include/sodium/crypto_vrf_ietfdraft03.h | 4200 | `b966fef7b111eb6fd061c3c20426b62b52189114ba098351c0e975cefbda69cf` | 0 |
| crypto/libsodium-fork/src/libsodium/include/sodium/export.h | 1347 | `acc6ee537f831d535b0607be90f05150103765b7ca82170fd61a85bd5e6f73ff` | 0 |
| crypto/libsodium-fork/src/libsodium/include/sodium/private/chacha20_ietf_ext.h | 632 | `116e6f97313959c5c45eadeb1722b52f5ec0f38ad57ef1177b3eae4d57d3fa3f` | 0 |
| crypto/libsodium-fork/src/libsodium/include/sodium/private/common.h | 6202 | `605781eed060b01d418c24605cda664a6e3139d6541ec2536dfd5ba3d1360afa` | 0 |
| crypto/libsodium-fork/src/libsodium/include/sodium/private/ed25519_ref10.h | 3876 | `53feea7573f8cf747460be2304366c7195ba578726289ae3cbd9d4c69e131e0f` | 0 |
| crypto/libsodium-fork/src/libsodium/include/sodium/private/ed25519_ref10_fe_25_5.h | 30154 | `7f1522d3286253add4d09c61df2fb4e96d4b4b8bc50db57c5ecadc0c10dae36a` | 0 |
| crypto/libsodium-fork/src/libsodium/include/sodium/private/ed25519_ref10_fe_51.h | 10968 | `4b9c0513603135de0f8f9a64632bb71f9dd4cb6a0cdf82907c8bcdc9e3398ed4` | 0 |
| crypto/libsodium-fork/src/libsodium/include/sodium/private/ed25519_ref10_sc_25_5.h | 19587 | `dcb600432bd1c9d7d33c9740702d6746645cab04f5d7f8dd8bf11eabe2ba3e1d` | 0 |
| crypto/libsodium-fork/src/libsodium/include/sodium/private/ed25519_ref10_sc_51.h | 13608 | `74ca64251b2406f84f23d04418e376eb7cab69a89648d99171f9e78d2d5bf061` | 0 |
| crypto/libsodium-fork/src/libsodium/include/sodium/private/implementations.h | 433 | `c97f3bed15f648a925023527d25d4130774d0a15354cfb5184b20dbc5f7e328c` | 0 |
| crypto/libsodium-fork/src/libsodium/include/sodium/private/mutex.h | 115 | `ee045978cbd074c695e8e0b4ec074b84e768c9557c8b4d69ebccc0710bbc422c` | 0 |
| crypto/libsodium-fork/src/libsodium/include/sodium/private/sse2_64_32.h | 1119 | `cb456bfe3b22c8bf1062a8e579ed1f15bdff724a23c8313531a1a46dd2a2843b` | 0 |
| crypto/libsodium-fork/src/libsodium/include/sodium/randombytes.h | 1847 | `41bf6745f8343b39a48861e9128bbff39ddd7f784d3e8c59a8fcbc55c6511c05` | 0 |
| crypto/libsodium-fork/src/libsodium/include/sodium/randombytes_nativeclient.h | 331 | `5294db1b305c72be8d3ba604cf3539c3a5f6fe3c390dcec4603a83d55c258c23` | 0 |
| crypto/libsodium-fork/src/libsodium/include/sodium/randombytes_salsa20_random.h | 290 | `9d4dc30d99085bd9057fc01dd568e1bd1e7699d5dfa185bf630cd8f43e0ed921` | 0 |
| crypto/libsodium-fork/src/libsodium/include/sodium/randombytes_sysrandom.h | 282 | `cdcc193ee76bb69626b7cb63b105db2f83796b7c365c9f4e42193fa9e654bfb6` | 0 |
| crypto/libsodium-fork/src/libsodium/include/sodium/runtime.h | 889 | `5f618794bfa316c338bc166ffd21f00e5711a0ebf94aaa19440c88b0c94be023` | 0 |
| crypto/libsodium-fork/src/libsodium/include/sodium/utils.h | 6316 | `d2aa29188313663ee4a6864b41023a22985024a520b9addbdafb453023a67145` | 0 |
| crypto/libsodium-fork/src/libsodium/randombytes/nativeclient/randombytes_nativeclient.c | 1497 | `82f30aa6a82f766140c99e9a56e575094ee8fd3a2daf26300d08e5a88a6ec1a4` | 0 |
| crypto/libsodium-fork/src/libsodium/randombytes/randombytes.c | 5068 | `004a69a257dc7acfb3c6fca839337e5f08da5bd864d9968ccc9a4768ca7baaac` | 0 |
| crypto/libsodium-fork/src/libsodium/randombytes/salsa20/randombytes_salsa20_random.c | 13791 | `5567c7f0ecd8b0718740ea31ccf01c4d6e5fabe3eafe055553a9d94462000360` | 0 |
| crypto/libsodium-fork/src/libsodium/randombytes/sysrandom/randombytes_sysrandom.c | 9563 | `4af43eb1a171a90a1d984d3ce0e5586cd3a9a22c6192f04686455aa665a2db7a` | 0 |
| crypto/libsodium-fork/src/libsodium/sodium/codecs.c | 9296 | `f2d9d92e607a47209199e29358d20179982ea64a3ef130caf0b8cefd0f98fd43` | 0 |
| crypto/libsodium-fork/src/libsodium/sodium/core.c | 4119 | `69d7126c668759b332bee5d504b7e70008a7c900edd36e299bbcb9002a407e93` | 0 |
| crypto/libsodium-fork/src/libsodium/sodium/runtime.c | 7561 | `42f94fc144cec1dd2019f8dc3db10460d38c60a11bc62c0f518719ea698a5df7` | 0 |
| crypto/libsodium-fork/src/libsodium/sodium/utils.c | 20621 | `69a8c1cb091bb658fb21b8bd701b3b07f71a2bbf24d18a10d6ad61a3171f1bc5` | 0 |
| crypto/libsodium-fork/src/libsodium/sodium/version.c | 381 | `f156b71249e77d49a3d31b8cd76fe8251da2df20a851c2e2ba91978847893823` | 0 |
| crypto/memcpy_chk_windows.c | 1168 | `e90507b20f22f1a159865b0e7887da046fd925f4bee91b5f78fb2b4e38895638` | 0 |
| crypto/merklearray/array.go | 1482 | `eaca58c72e404afb1989370087e3a83dcc30c184541404fb188cb304e30b5ea6` | 0 |
| crypto/merklearray/layer.go | 2409 | `85a4fb1c6b6b727ef3e6e71f4db0c84d6e2463b2b528826ee473705e8b41fa4a` | 0 |
| crypto/merklearray/merkle.go | 12005 | `0e2aafa981b0be02c8abc17e034b88826dc0726cacf21c142c9f9b3a0bd3dafb` | 0 |
| crypto/merklearray/msgp_gen.go | 16950 | `41f3f33d7c61ac54b4731fed5dec516e889e65e971f1165b0884f9b60a032fe9` | 0 |
| crypto/merklearray/partial.go | 3536 | `b15b715ae726e2f70ec51c271d550b4dd2a50bb86f8e456f3c3c9d3a405d7098` | 0 |
| crypto/merklearray/proof.go | 6947 | `269950e9e8feb23e31655a1f0050af5bea3137e6fce9c41f082e822da5364743` | 0 |
| crypto/merklearray/vectorCommitmentArray.go | 2781 | `6263cdb47990c092c56d943f7db8728ec42aa32b38c28c0365599c0c820f90eb` | 0 |
| crypto/merklearray/worker.go | 3019 | `310ba10587426de36afe4f28b664120ce09c2de77b6461f3c6ea142b02c3fdac` | 0 |
| crypto/merklesignature/committablePublicKeys.go | 3241 | `4f39b507f32dcdd3be423157b543c579a8a5f72cadac40af5b3be201bb04bdea` | 0 |
| crypto/merklesignature/const.go | 1973 | `75b1a36c8413da45f310942c853de55f78029bc1949394e62569c1294fb3e836` | 0 |
| crypto/merklesignature/keysBuilder.go | 2788 | `f6e7530011cdec65272987f1a8f7a1d8788445103f62131c1060379e4082b1e6` | 0 |
| crypto/merklesignature/merkleSignatureScheme.go | 11316 | `08e4aa43d5dd8be562e6a66fda314b75c454742f16cadc1257a5655af1f4d5c8` | 0 |
| crypto/merklesignature/msgp_gen.go | 19578 | `517f8261510462dbd411efdf38a1a80444a1047d5dae856511fa46ee549098f2` | 0 |
| crypto/merklesignature/persistentMerkleSignatureScheme.go | 5656 | `00a27d902c39edb60ec8b0b1c3f3bdd6cc6df16761470402777b06ef019894fe` | 0 |
| crypto/merklesignature/posdivs.go | 1888 | `a1ae3da6b74ccd009e7521ff0851b6e43dcee0262c80fc950768a0611181d5d2` | 0 |
| crypto/merkletrie/bitset.go | 1548 | `99df01fce905cc2a1c7df00cec683d04e08706ea4ef3b0625f8f535c3c3f23a1` | 0 |
| crypto/merkletrie/cache.go | 27892 | `931378d2dba9fcea7e9f1b5a8311c349c04eef4d98d7e76a08847bfe03371871` | 0 |
| crypto/merkletrie/committer.go | 1810 | `573e0e9da6be1cd73087bb6c936129ce70477b8f24859eeaea640036a9e31f37` | 0 |
| crypto/merkletrie/node.go | 12338 | `68bdbfc46560d5786d6fb3c5f6ae676f381b73c7edde8fb1c22787331d00616b` | 0 |
| crypto/merkletrie/trie.go | 9488 | `6c6f834ac570420942a5c2677f04b2fd69428931283bd40a0f6c4eb7447d995d` | 0 |
| crypto/msgp_gen.go | 115932 | `ba99f6f3ce4be0ff5b06f50827e443ce850a93c710d9e2bf5eff69bd70f7828d` | 0 |
| crypto/multisig.go | 10705 | `cfb4fb885d69fd7d79f9e10479031685f2175cfed9c34935c9f5f8fda4a42465` | 0 |
| crypto/onetimesig.go | 18316 | `cf2cacfdcaa47f1c7ce6bac0aa160315d6a08acc93fd5f72b9da198984c907e7` | 0 |
| crypto/onetimesigpersist.go | 6503 | `34ec6ad0b10f32096919536511f7979f190694ee509df014c850ab99a735ef7e` | 0 |
| crypto/passphrase/errors.go | 1021 | `12e79a6a94ce327df882b14cac881d450ea80935d6f3b03232139a7ede83e1ac` | 0 |
| crypto/passphrase/passphrase.go | 5780 | `47314d9fcdb40fb2ee95d527405ad9566c5ba8e1e43a35cc76cc950d35507048` | 0 |
| crypto/passphrase/wordlist.go | 14385 | `66585b146537e9d7519e847e0363286723d5b1f5baea37620f9df6ebab6ecf42` | 0 |
| crypto/rand.go | 2814 | `713d5b688ff5d075f82680d66bff13f06b57925450ae5e1449e2703b9dc11a27` | 0 |
| crypto/secp256k1/curve.go | 9853 | `b063240f68384b1866a94eb3ab2e538b359ef82b4e23cac6cc653d0c037e7214` | 0 |
| crypto/secp256k1/dummy.go | 795 | `862d31d1bfb603b50f926137d2628dc78ee90ca49c0004a16ba616489be6f832` | 0 |
| crypto/secp256k1/ext.h | 4944 | `78e5c31f2095b51c15939229f16e37c4ce91f01b5c107914d16a5084b5dd0a8a` | 0 |
| crypto/secp256k1/libsecp256k1/contrib/dummy.go | 222 | `16f550b65021d0c6152ead9c3fa5856a88051c7f0763db608a7c0bd91d0049df` | 0 |
| crypto/secp256k1/libsecp256k1/contrib/lax_der_parsing.c | 3610 | `2a1cdc8e8f30fd064e1a619505d6d53c130462a40bf2da95575791b91e641608` | 0 |
| crypto/secp256k1/libsecp256k1/contrib/lax_der_parsing.h | 3909 | `87ccaf0a5afa711e4e52dcd5345473172531a6ab30c926822c4aa7afffdde2ef` | 0 |
| crypto/secp256k1/libsecp256k1/contrib/lax_der_privatekey_parsing.c | 5114 | `8677deadbd09d46deb4778751424f9e87b6ad24730e2dc3ec1f9bd681e13bf31` | 0 |
| crypto/secp256k1/libsecp256k1/contrib/lax_der_privatekey_parsing.h | 3724 | `a4d226896ac58aa8820f1b2e0a59809bf9d677c991398947b0479d898354ebf5` | 0 |
| crypto/secp256k1/libsecp256k1/dummy.go | 227 | `cdb4abf1a72d78c8c3693b7c082a2ad337f47ff6a1cdda53bbec2101d550ac88` | 0 |
| crypto/secp256k1/libsecp256k1/include/dummy.go | 222 | `b99aae51ae07e09b9fc71e4a23e280f29dab7e0cfbde6b5a90274213500d3cea` | 0 |
| crypto/secp256k1/libsecp256k1/include/secp256k1.h | 25517 | `72d78cac2a6879f5f02728dcd25d3ac1e0844681a3a6d7c5d63192fcf49f32ea` | 0 |
| crypto/secp256k1/libsecp256k1/include/secp256k1_ecdh.h | 1014 | `ff74451e3e574dd144ba97f1ee3a13453a6e748ad61ae7c33f52bc856d3ad642` | 0 |
| crypto/secp256k1/libsecp256k1/include/secp256k1_recovery.h | 4700 | `2bc4be0ea9862c81e4ad750c3c378e31b4cc7ac3f0d792a6f9b360f252a165ab` | 0 |
| crypto/secp256k1/libsecp256k1/src/basic-config.h | 944 | `5d04f98036331e50780355edb2918f5670d185e1ae1d48fb99a59ffb66c79b0a` | 0 |
| crypto/secp256k1/libsecp256k1/src/dummy.go | 218 | `6dceb0ba565e9a40ae1db7d5c3c73e3173465443738f068d91cbcc64175d1d1d` | 0 |
| crypto/secp256k1/libsecp256k1/src/ecdsa.h | 1172 | `c2793ab52944a53bf3b757044b82284188cce3dbabb0a2caabbbd2703a1c1e11` | 0 |
| crypto/secp256k1/libsecp256k1/src/ecdsa_impl.h | 10391 | `51fc7601310420e0ce45a3288b9da75e2c836952fda7e8a4e846766a4cf303f7` | 0 |
| crypto/secp256k1/libsecp256k1/src/eckey.h | 1208 | `c6d283eb8dc8ea1605a575cc3a5b260503cb5eb38dfb827a44460c458592d404` | 0 |
| crypto/secp256k1/libsecp256k1/src/eckey_impl.h | 3178 | `dccf81e7bbea7d0fcd8c9e0ccb67a8f3f4f367d99dae77f051f07ce833e4fa4d` | 0 |
| crypto/secp256k1/libsecp256k1/src/ecmult.h | 1481 | `b51aa0fc049aebb3551237a7f3319fb2243db69ceebfec13dddc8cf6052c4f15` | 0 |
| crypto/secp256k1/libsecp256k1/src/ecmult_const.h | 581 | `d0dd163e84cb20622011cd101fa6c86ac14fda3b7a3e876b269843da1412de2e` | 0 |
| crypto/secp256k1/libsecp256k1/src/ecmult_const_impl.h | 8952 | `50daaa382564652294204450a768a2069b979551dd763495fe2db455bf8288dc` | 0 |
| crypto/secp256k1/libsecp256k1/src/ecmult_gen.h | 2277 | `f86ab1735935c4afce8624c76f5d992957c8402c7be9462518d54138925bc684` | 0 |
| crypto/secp256k1/libsecp256k1/src/ecmult_gen_impl.h | 8359 | `583ab67aeb185053f9c8e03fdbb7a35bc4a824fa9bd48b135fdb4d8207000b44` | 0 |
| crypto/secp256k1/libsecp256k1/src/ecmult_impl.h | 14095 | `5aae6a84dc4377eb29918d22d79f58128e71dda40462cb8a54d400adfa04921a` | 0 |
| crypto/secp256k1/libsecp256k1/src/field.h | 6436 | `78cb7e3926533c1a283350de00c4e6746cf14e83254bfbc48accf5e0ecfa160a` | 0 |
| crypto/secp256k1/libsecp256k1/src/field_10x26.h | 1909 | `20f5aac948d71f7cd3ba4995bf8a89169dd8da6d8f3e66bc32d182b76b3e1a23` | 0 |
| crypto/secp256k1/libsecp256k1/src/field_10x26_impl.h | 45369 | `2ef5eb5ecf0a077007f55b4f36cbda9518c0b4d9b43ba7932f291ea782216017` | 0 |
| crypto/secp256k1/libsecp256k1/src/field_5x52.h | 1711 | `38fa9dd9652ec5984f6058553ed8e8787c1b09632fc0ec15ce0fe194aa5acca6` | 0 |
| crypto/secp256k1/libsecp256k1/src/field_5x52_asm_impl.h | 13127 | `a4f00e3724a687ac3bcb3d355fe7c40b0b5d010ee41527614bfe49365fa894e7` | 0 |
| crypto/secp256k1/libsecp256k1/src/field_5x52_impl.h | 14622 | `5c84d099502ebebd984df35702aecbca14101ba7185e136029a12d27b7516396` | 0 |
| crypto/secp256k1/libsecp256k1/src/field_5x52_int128_impl.h | 9190 | `ad30ee7c7094b09aba014194a17a31e4b6f85caf54919850c9b840b32421d30c` | 0 |
| crypto/secp256k1/libsecp256k1/src/field_impl.h | 8758 | `564ca40bfb3a31d8cd8a8af283785d60de32edfe96e316d9f2547b00f6f4fa3d` | 0 |
| crypto/secp256k1/libsecp256k1/src/gen_context.c | 2356 | `e963c01c681fefed967f48975a7b5391b15beec428a845c490985fcf433678b3` | 0 |
| crypto/secp256k1/libsecp256k1/src/group.h | 7862 | `c79a73b99d94faea040c6e4b7b75c8875fcc6388df90de9ffcc208cb404d2d6c` | 0 |
| crypto/secp256k1/libsecp256k1/src/group_impl.h | 27525 | `4f5dfb6b1132d574acdebc64b827abc69c3940ea8cb14935bf33be783b63e638` | 0 |
| crypto/secp256k1/libsecp256k1/src/hash.h | 1712 | `ec9eb940dc53db3fa04e504c69858afa52d803de7c1f2861a62798d6c1e431f8` | 0 |
| crypto/secp256k1/libsecp256k1/src/hash_impl.h | 12674 | `9c1f484cb00e95d0cc4377be8df02827569037c6ff7ec16434c041b480103559` | 0 |
| crypto/secp256k1/libsecp256k1/src/java/org/bitcoin/NativeSecp256k1.java | 15756 | `62319d94a74ee487cdffad7d64807bdcad349ce9ef1c615065cc5ab5ef9f681c` | 0 |
| crypto/secp256k1/libsecp256k1/src/java/org/bitcoin/NativeSecp256k1Util.java | 1543 | `cdf53b4214a284c2f370e4e79442a2ea38c05b968e30c036f2ec717157e60b4e` | 0 |
| crypto/secp256k1/libsecp256k1/src/java/org/bitcoin/Secp256k1Context.java | 1551 | `361eae8a47d1c1906eb9dc90e1196cc9a0f9841caca95ad2e133a5cafe596a10` | 0 |
| crypto/secp256k1/libsecp256k1/src/java/org_bitcoin_NativeSecp256k1.c | 12137 | `ccae1fb58044f0509367b42bd2017f04b28e871e9e65b24288d4369658ff0086` | 0 |
| crypto/secp256k1/libsecp256k1/src/java/org_bitcoin_NativeSecp256k1.h | 3733 | `b7f97adade72e1a87e5f8e1caa6b0c6bd08456ccd27074d5fe0d7930296e161e` | 0 |
| crypto/secp256k1/libsecp256k1/src/java/org_bitcoin_Secp256k1Context.c | 404 | `05bf610a3f3a7ccf8a4b066e83454dee40c2a33fe18d3e615bdbc636bba24309` | 0 |
| crypto/secp256k1/libsecp256k1/src/java/org_bitcoin_Secp256k1Context.h | 538 | `46286b5df55c15a8506adb3ae002a5d4f86e74f359f89dd2038588c7b7ae5b5c` | 0 |
| crypto/secp256k1/libsecp256k1/src/modules/dummy.go | 221 | `d994866892f4824b8a03cfc9450a230decebcea4c145ea3f4e9aadcbd74d0c02` | 0 |
| crypto/secp256k1/libsecp256k1/src/modules/ecdh/dummy.go | 219 | `4c94be241bcb1292c3bd99b5a019f40361856a0cbcb4b943e0d587f685ccbc78` | 0 |
| crypto/secp256k1/libsecp256k1/src/modules/ecdh/main_impl.h | 1893 | `e4fcec40b57ce3bb847afd359a3b6745a829f6aa4063a89cb00202e7846c5c81` | 0 |
| crypto/secp256k1/libsecp256k1/src/modules/recovery/dummy.go | 223 | `946a3d88ff5cb66ea762088a46589ad5390d036e7da42390df0611a311192456` | 0 |
| crypto/secp256k1/libsecp256k1/src/modules/recovery/main_impl.h | 7194 | `462f8fb1995505a759fe5c89f9df0007ad568101a6b881383694ba3a5a355b57` | 0 |
| crypto/secp256k1/libsecp256k1/src/num.h | 2788 | `94351cc1bc831d9acb2ef2c832408890d71ec0c5fb74a944bc119e4055935d84` | 0 |
| crypto/secp256k1/libsecp256k1/src/num_gmp.h | 599 | `a4d8ab9abd0454447201476e87a104c2780c02485ef0a36270edd8cde01fe747` | 0 |
| crypto/secp256k1/libsecp256k1/src/num_gmp_impl.h | 8376 | `3862a06bfd520676ae15b32355a5638b07f4f7c0208e0c3c2ad5ee9e6031598d` | 0 |
| crypto/secp256k1/libsecp256k1/src/num_impl.h | 667 | `6d5dd7469f03c6f07b10f5fb1e48f5c0e62cd650e6861853ad796ea0ebb71ccd` | 0 |
| crypto/secp256k1/libsecp256k1/src/scalar.h | 4763 | `01ca47e9a3282f408c348359869b875f8911f95ced20a6be426dd972159aca56` | 0 |
| crypto/secp256k1/libsecp256k1/src/scalar_4x64.h | 766 | `b46b7c8c57e7eddd53116832cc2476f130474423abd23ecfe775cb166888ad8a` | 0 |
| crypto/secp256k1/libsecp256k1/src/scalar_4x64_impl.h | 30690 | `bf640aaab778b3218c2f62bfcbe952ef57d1e0227367ca9a99df007f4087b702` | 0 |
| crypto/secp256k1/libsecp256k1/src/scalar_8x32.h | 690 | `7b94e8e4c7f1d3303a90dfe52ceb5367bc54daf12c7ee5209e875e85cc0417f2` | 0 |
| crypto/secp256k1/libsecp256k1/src/scalar_8x32_impl.h | 26859 | `fbfc380e50f71b2bcc55b72060b4e05dac656b28ace208630dd242c530198f95` | 0 |
| crypto/secp256k1/libsecp256k1/src/scalar_impl.h | 13142 | `5f7b5be78ccf84d1d3b8a17d098705dc81c1f7b34cda3f4854302b3f68924011` | 0 |
| crypto/secp256k1/libsecp256k1/src/scalar_low.h | 554 | `9158754d4b9a55e0eab6b8e47d548489e2ba580e7058d875ab2c5c6d65a6d5c7` | 0 |
| crypto/secp256k1/libsecp256k1/src/scalar_low_impl.h | 3719 | `a3baf7ac8b87a81f0d4ad950e9254419293760c992e8a47ff3893db0b12550b9` | 0 |
| crypto/secp256k1/libsecp256k1/src/secp256k1.c | 18950 | `802d66def212632f417606012d69a64d1afed2ad2828dab92211c9667ff3923d` | 0 |
| crypto/secp256k1/libsecp256k1/src/util.h | 2870 | `807dd2dffa646cf7b780769c69df2aba2c1462e48301fc00b61738743d0853b1` | 0 |
| crypto/secp256k1/panic_cb.go | 643 | `7ecfb8748933b0a208b21ef1f3427e18cf6045a1bcabce66a6b3095d94022eab` | 0 |
| crypto/secp256k1/scalar_mult_cgo.go | 1441 | `02878eb3f9025efa2f697ca6e2bfa4647a332416517cd773c2c4422bde785d8a` | 0 |
| crypto/secp256k1/scalar_mult_nocgo.go | 424 | `e4e9da8a93e85fdbb2f064baff88d7373907b7062cf1e3e79ee9cc04243ed8b3` | 0 |
| crypto/secp256k1/secp256.go | 5746 | `92062d35457868c143478b46419083079dcff1c3a462093d4b1e445ea338a3ee` | 0 |
| crypto/sig_scheme.go | 3537 | `5942b04a8d7a8323107714e66b02005e0cc3a021f30a503afc48c059e5c0b63d` | 0 |
| crypto/stateproof/coinGenerator.go | 4735 | `5f7fb2801d9c4fc68c13182267fb73e941d0c50055cb39e2d0de3d0adb1db50f` | 0 |
| crypto/stateproof/committableSignatureSlot.go | 3749 | `f08b2ab8b76e3fa1bc3e206de29a0132e0c0b402758daf7a57a74c29859c6349` | 0 |
| crypto/stateproof/const.go | 1862 | `5f582473d246551f27ca005eb946af9fa88fec96b1cf3e91ede5286d09406e5d` | 0 |
| crypto/stateproof/msgp_gen.go | 32473 | `22aa837d7ae6497e72e33419d000371f1de629d8d41ae393d4196d432165b2a5` | 0 |
| crypto/stateproof/prover.go | 8395 | `562afe0a595c2f228ae7bab142379779564f43ab1c6cd5e8d444443d2347b8dd` | 0 |
| crypto/stateproof/structs.go | 3757 | `1df713a6067276c01170f363239a978fbe11cb0d3f0badd17c97ff43ec527914` | 0 |
| crypto/stateproof/verifier.go | 6331 | `eb152039a947f552af189f2f177b13f92d5a0db182d5df36aa5322f2307a4498` | 0 |
| crypto/stateproof/weights.go | 6934 | `03c13257bf553c33f9a7ac5bfd3a011ad0ad531eaec7f5ce0232612dc3fba1ef` | 0 |
| crypto/statetrie/nibbles/nibbles.go | 4443 | `0a1e3d5fa8df4bfc8ac876fdcc156f6902e6128d548c10786ff9e532ca0de34b` | 0 |
| crypto/util.go | 3507 | `6ed01eff1ce79b24b964c51d5a6d24839a324bfdd087003dcfcd5f803da0013e` | 0 |
| crypto/vrf.go | 5954 | `7197b1fa7f9c8f5dc8c9a01d9b53b1bf98d58fd4863ae50aa901cb70f29aacee` | 0 |
| daemon/algod/api/client/encoding.go | 1377 | `5b38b47e6b244e943b4cd3945e32cbd0fde29a9d2d495b1e381494ff36ce0a14` | 0 |
| daemon/algod/api/client/restClient.go | 35171 | `d9266846cbeff427159d384cee93d053a7a21ee11d47c8e964429c3065c2a30b` | 0 |
| daemon/algod/api/jsoncanon.py | 126 | `a148a8af0bc6fc66b68dcac58a2f8f1dcf4e322911d33e9ae8d55f3926352522` | 0 |
| daemon/algod/api/server/common/handlers.go | 6106 | `ed74f9227593f98d3aa017ce94883c75c537d9c79dcb8cac939de2ff96c6887f` | 0 |
| daemon/algod/api/server/common/metrics.go | 1787 | `a0313d52fea997d63d4fa3eb260613abd117d6a9292ae71bd20ab5d1134bcb5e` | 0 |
| daemon/algod/api/server/common/responses.go | 1206 | `f6c75123b27a9c14624accbe845f1cae597b52c9edcef0be20eeb0f67ed1db2c` | 0 |
| daemon/algod/api/server/common/routes.go | 1611 | `033632126fdb16bf6e99b35d0c7246338fe2543e896e07da414e32986a6acfca` | 0 |
| daemon/algod/api/server/json.go | 2040 | `3e7006098749070b4e7ea1ab87a5e2a1ed87532cdf1fe6587f2871bea0220761` | 0 |
| daemon/algod/api/server/lib/common.go | 2176 | `c1b8f8945929c320a6cb66bc77061186a921c28b714702569bdacfaccfc0f06f` | 0 |
| daemon/algod/api/server/lib/middlewares/auth.go | 3620 | `504849e742664c98c0f9d530733c4ac8637937cd33b094848090a2c7d0ea1fb5` | 0 |
| daemon/algod/api/server/lib/middlewares/connectionLimiter.go | 1495 | `2d182cbd1e09b4245a157295358ffd51e622523d9396e70b26664decf9280ec5` | 0 |
| daemon/algod/api/server/lib/middlewares/cors.go | 1692 | `38d7fb621e663ff3bac30a5c666f32ecc4eee34b8bdc70ce9a4da89f72beee65` | 0 |
| daemon/algod/api/server/lib/middlewares/logger.go | 1913 | `cbd7810891c558e858b68c3600f229b481bb40910c0fc9a3116db6869d5afb46` | 0 |
| daemon/algod/api/server/router.go | 6479 | `467323ebf6a1dde071b201e4159ea6a36932af81ef8e1068e91cbb616710b3ca` | 0 |
| daemon/algod/api/server/v1/handlers/errors.go | 867 | `089bd83bb6f5398c62d59b8c2d7d80ddfc9aa20f41c630a2664b586a963212e4` | 0 |
| daemon/algod/api/server/v1/handlers/handlers.go | 1166 | `552012c03a8a9377c2ab7a8fa0d2e75b9304109a288ed875fe7494ad97b99e57` | 0 |
| daemon/algod/api/server/v1/routes/routes.go | 3510 | `d0985f88bbc6a138534d73a66cb0365c747fe509eb5c950de16e50fb350b377e` | 0 |
| daemon/algod/api/server/v2/account.go | 16523 | `373616572a16598182249659c37e6237313672e2e30afff5103496563e90c739` | 0 |
| daemon/algod/api/server/v2/errors.go | 3705 | `379954b2bd69377a9d0c652d692eed631b195b3d3f970a9e6351052553177c82` | 0 |
| daemon/algod/api/server/v2/generated/data/routes.go | 3884 | `5a34ddffc2ed77825faaa62f8eaa0942efd00b698ed10ccea0d5c1bf34f93e69` | 0 |
| daemon/algod/api/server/v2/generated/experimental/routes.go | 3756 | `0c4b210467e2c1965162aabcabdb81e997098bd879c6b2027bb46313e58fe16d` | 0 |
| daemon/algod/api/server/v2/generated/model/types.go | 75515 | `3624709af89d89063ecd024aaef04974229aa48540d89be3556d29a5b180b502` | 0 |
| daemon/algod/api/server/v2/generated/nonparticipating/private/routes.go | 8063 | `4c9b13080edbd30cdf9d64a6618b5422259a2a1d50a3174b863e68b9dbcf068b` | 0 |
| daemon/algod/api/server/v2/generated/nonparticipating/public/routes.go | 41075 | `de98ef2aa12ef3fec97c7c056018087f5a4fa6034b5d226af89944474bfe9bdb` | 0 |
| daemon/algod/api/server/v2/generated/participating/private/routes.go | 10416 | `e51a3a7f88192a6dd503f449d30423d3ab653373d9623bd58355a9189d6a0bff` | 0 |
| daemon/algod/api/server/v2/generated/participating/public/routes.go | 8260 | `5aff7e1d88ab06afb8fd7f0341afba2c1b05d072df7cd6f033c210406dfb0072` | 0 |
| daemon/algod/api/server/v2/handlers.go | 91719 | `c9a9e8e22f1421a55860e8e7ef783b72534becee08e81f59169cf1dd931d6a4c` | 0 |
| daemon/algod/api/server/v2/utils.go | 21289 | `40c7adb1426da23158f167f5adf9beac67932a2e1417bb708f2df9e5c5dc115b` | 0 |
| daemon/algod/api/swagger.go | 1008 | `a1c856c574407875fb75fca467275a1587ad742cebc267b0d152df58e9064532` | 0 |
| daemon/algod/deadlockLogger.go | 2992 | `f13d257345dc1264e0d2d66c3fa5cb4a620f11772288df24e7a26cf9428c1532` | 0 |
| daemon/algod/server.go | 15896 | `f0afbff322a53c89f9095dc868bab960d8c50b6d6337f31fac6b07d740152ff7` | 0 |
| daemon/kmd/api/api.go | 5871 | `da2ff74e1f4f1abc6b24967e1df9ddb2ed4887e725dba5268fd9fceec56cb602` | 0 |
| daemon/kmd/api/cors.go | 2452 | `0a0795fda3bb15892bbb635a1d8e8ace87edfbda26f91ac3a4a35c0d32171102` | 0 |
| daemon/kmd/api/v1/auth.go | 1883 | `c464b079ea4f8d65157980c17029b4b47a5a9451b0cd8db2e8f882ac1b102b9c` | 0 |
| daemon/kmd/api/v1/errors.go | 1052 | `0b38ac9c61cb5a8aa360e8d149d85b507b2470d5d5a4a858a5e1c8595d7e486b` | 0 |
| daemon/kmd/api/v1/handlers.go | 40012 | `94fe5b7d87568f346e9ae7af145a2ca70a334cc03f9b025089df646afe9f85fc` | 0 |
| daemon/kmd/client/client.go | 1391 | `6434f0b3044d0e7f7bfd26723343cf4147fafe8476e7ec53f19fb12ca6b8f8b2` | 0 |
| daemon/kmd/client/requests.go | 4218 | `db9b860e205a0d2268f34a918214bebee8901cabe223f42fcd8c81954ccdda29` | 0 |
| daemon/kmd/client/wrappers.go | 8693 | `4d512162291f7a49e8a9e998198215f97dff8329c07efa74e021a24bf4fc4e61` | 0 |
| daemon/kmd/config/config.go | 4542 | `9c60106bbd2f097170818dd288b52e340a829d2200d5127b2399021fcb2cd73e` | 0 |
| daemon/kmd/config/errors.go | 975 | `10a5b77f4ddc41dbacf1ef1cadb1f5910d1b233f744cea4df2adc38b3635628f` | 0 |
| daemon/kmd/kmd.go | 3058 | `2ca24fa0b762283cccc52b8307d3730ca97d08141f3b2a3ff0cc162e8cd1244f` | 0 |
| daemon/kmd/lib/kmdapi/bundledSpecInject.go | 317723 | `3132c5d23736771c5161cb0db1c6369e7be579f7d0659b693ee302999fe1a9b3` | 0 |
| daemon/kmd/lib/kmdapi/common.go | 2160 | `30cb1b98d4a9a4f1ffcc7e491753110d7bc9889d4406ed19f617aeb3eb03fd58` | 0 |
| daemon/kmd/lib/kmdapi/genSwaggerWrappers.py | 1605 | `fffc946a2c2b2334b6787b8198bf49ebc1a55bc8ffc76a8716deb4b04fc18f70` | 0 |
| daemon/kmd/lib/kmdapi/requests.go | 9080 | `9ed5663de3f1a99cb9b70ca06c61be0abed67a25feeb9f018f6062a25353e47e` | 0 |
| daemon/kmd/lib/kmdapi/responses.go | 10204 | `ca01a98acbbdcb6b25055596ae3e8375c012cc582b2b298263906992d31b8afc` | 0 |
| daemon/kmd/server/errors.go | 1361 | `be0b9462b8425625d533fe19400b6f7c132100221be4fc341281c2813a895866` | 0 |
| daemon/kmd/server/server.go | 8028 | `187817b6bafb472ceb1c2be6a5b18e89d63065de582bf9cc3b893e3d7149944c` | 0 |
| daemon/kmd/session/auth.go | 7114 | `80b8aeb8adfedce73602a8a6f58ecc4d0cab20d07606519147e4c68028e16903` | 0 |
| daemon/kmd/session/session.go | 2019 | `28c55ca33a59a23fe014f07bd1cc0384d1a4f4bce3d019935f553c865f9d1dc5` | 0 |
| daemon/kmd/wallet/driver/driver.go | 3744 | `f8311c7fb2aaeed7ff3081d9416e52d60e2c889942af6513cdc52c602ee6f3ae` | 0 |
| daemon/kmd/wallet/driver/ledger.go | 15027 | `d9761feec00fce265e6d5a6cdd33cf8ef57748b3b648380c9b2e5d086c7b4df4` | 0 |
| daemon/kmd/wallet/driver/ledger_errors.go | 862 | `66d0e497394fab8d937bbf307e7e32d2c1e077e2acf85032a2dba4bd55f85621` | 0 |
| daemon/kmd/wallet/driver/ledger_hid.go | 6061 | `c763f5c87facc799b512062aa8658dfef825812893da2e8ee2ac339f0e24eda6` | 0 |
| daemon/kmd/wallet/driver/ledger_hid_darwin.go | 1852 | `073541eeb3cd3d4ead3ef45dac2a8f9ccb4062061d2291181d1e9d1bf52fc9ba` | 0 |
| daemon/kmd/wallet/driver/ledger_hid_other.go | 1093 | `41913deeec5ca0cffa801b8f5da59f0b1a3e6ff808d4d23ea1f5300c6111a112` | 0 |
| daemon/kmd/wallet/driver/sqlite.go | 38438 | `5513cab28950ab0348cea2d4d34f78acc7a051a180fdfb8496689fde52aac54a` | 0 |
| daemon/kmd/wallet/driver/sqlite_crypto.go | 7700 | `44294523c9c099b672a6a58d0fdd6541b87adf0dd0e75c0a5dabee218ba2e64a` | 0 |
| daemon/kmd/wallet/driver/sqlite_errors.go | 2735 | `7f152efddddf23f3f654f23e3dec043b4f6afda48d97834ac702eb88069ad70d` | 0 |
| daemon/kmd/wallet/driver/util.go | 927 | `a13165cf5353a69a27f0619cf6e9c28ae919f67a8ee26607caae8d612c630a4f` | 0 |
| daemon/kmd/wallet/wallet.go | 3032 | `5ecade542e2793231258492f04f28d9f3942303502973fc81aa8c64d0e90e68f` | 0 |
| data/account/account.go | 6236 | `e757cf11815708789ef0e1bdf4c96f71b61785e05eacac4412f3866be418be45` | 0 |
| data/account/msgp_gen.go | 7881 | `eb96e1d26609e9c324a477c8c7f098f57b551d1f31f542886806eba5aa3fec0e` | 0 |
| data/account/partInstall.go | 3504 | `e27a2671c5055c3571a046733039504aa354f79cb7e70744ed458b8365cd2424` | 0 |
| data/account/participation.go | 11610 | `ee4bb7f2260180d48333edb10ab1379a934bb2a86704fd581a8b7aa3b6162a38` | 0 |
| data/account/participationRegistry.go | 45264 | `6772924540f1e939a2a108451c3313e09e591e957cd2d1b71bbfdfeccc39faab` | 0 |
| data/account/registeryDbOps.go | 8519 | `95e7fd46295be4e7d8857af89d910bb70e973b38b9aa410195ed8a90a70a0467` | 0 |
| data/account/rootInstall.go | 1065 | `f608742efacd1481a80874aa8e458b960bf0f2cb496f41b99c2baed369a053f1` | 0 |
| data/account/votingRows.go | 13725 | `75fd53d081921bdcfe5fd9b819aab41d66dd5642fccd16013060cc14a4a778ae` | 0 |
| data/accountManager.go | 8004 | `70eb604f48cdf98a02a5f865ab594582ae672397eb50c48d4c57f879404d70e5` | 0 |
| data/appRateLimiter.go | 11575 | `e3bd6ccafbd9348bdd8bf0701ed5d46c1acdcdac27817b3320c1e18b3089d087` | 0 |
| data/basics/address.go | 3968 | `65df2c36dd59fc3c390f5d236765e3ae1abc820fc0bfc6c06ee77bdf9f6d8893` | 0 |
| data/basics/fraction.go | 2207 | `5852768828d9d17896490dc85d43aa1353d8a0c36aed8f4d10975ca51a91c28b` | 0 |
| data/basics/msgp_gen.go | 121493 | `bc18c81473da65eb5fe422166ea8ef07569e1d0d1f14894b2c72d449ff4dc736` | 0 |
| data/basics/overflow.go | 8375 | `42e1e64458df8bd5f4ca098c8b059023ea7e5f470320dc677fac04755d66bdd7` | 0 |
| data/basics/salted_address.go | 3211 | `3d56909ccfe03e41e2ec51497a129983a0e7acd752ce6dae040b63a52a447921` | 0 |
| data/basics/serr.go | 4511 | `580d9c27f9ca6db67813e0d17e81650bf1cb58d7541de52e5b10141b25e26da7` | 0 |
| data/basics/sort.go | 2762 | `a019064f5b772b22167e3c8b553a19d6347c5cd91c66744781c0a56bfc1ca188` | 0 |
| data/basics/stateProofParticipant.go | 3366 | `fc8b229a08471522a60e9553797768f60b9da2bf9dc0ee3b9624c783d1bff2ee` | 0 |
| data/basics/teal.go | 6588 | `74330d98f25e2bbf60fe111b36eea09cc31ba7317f300d7dc5fe9bf75a58f4bf` | 0 |
| data/basics/units.go | 7015 | `cd0ca652f3e5baaf47a940f9d7116b19761afa0d50bcfbd688890a8f41353a6f` | 0 |
| data/basics/userBalance.go | 25306 | `ed3b9d19d0c3ee2c3aa725013a2095ae87717c09b330909573af795d3ea699ba` | 0 |
| data/bookkeeping/block.go | 38675 | `107d9d868be1d70cde10d5625229d950765e984fb759b51d685a6e593a423a8f` | 0 |
| data/bookkeeping/genesis.go | 10268 | `687d41ae67852df4f49004be7fd739c6fede86ca1a5f77890ffb7de079a6391a` | 0 |
| data/bookkeeping/lightBlockHeader.go | 3453 | `bf28bd1671897b9da6ebb9cd8409412fc15c682e5a2c79346feb0f4014911105` | 0 |
| data/bookkeeping/msgp_gen.go | 100355 | `926131f073e89d3aca52321f8e0a9d7a96baa22e53a0d363d0bf3c306f55c575` | 0 |
| data/bookkeeping/prettyprinting.go | 1535 | `05657932d50de6f47c01d9bd4fdf8eed142a0e817a5f80573c77b7c90f23406f` | 0 |
| data/bookkeeping/txn_merkle.go | 4907 | `05d6a71f062d705a492719a9c1022c5e9b0f35ed6738e2cf55e5ee91eae41004` | 0 |
| data/committee/committee.go | 2221 | `4af886d15c8a0559617df8bf0b13cd5fd46d3ba706aa8c8c369be0f4caf8bbc5` | 0 |
| data/committee/credential.go | 8198 | `d741b2c3e42c1b5f52751b8120afca5207a1388d46b44d0b4f41240e73a04a78` | 0 |
| data/committee/msgp_gen.go | 12658 | `e75508092b4a4d188e092dff26fb006c128ae1e9c6f0cc8cb9bd34caf9a8d5dc` | 0 |
| data/datatest/fabricateLedger.go | 2125 | `9c2605be3f5a6304adadf496f23436064a84e78a27d1248132bc81184e856aad` | 0 |
| data/datatest/impls.go | 4993 | `cf0d584db79509249408089d85fb1b2b4d1434ba681b9a7c37dfee146ba5ddc3` | 0 |
| data/hashable/message.go | 1163 | `853c5686d8d510c4a30a06b979f2da30e46f96d21289d91fcc9a53760b3bd3b4` | 0 |
| data/hashable/msgp_gen.go | 2740 | `033958012557c6b50422690a4d256fa452a25c23858f0efa72dd58a807dfd916` | 0 |
| data/ledger.go | 13133 | `ad480ff2916ba2be03ddb57b5f3b6ee87460dcf63db8a2bd3e37a97c62f745e1` | 0 |
| data/pools/errors.go | 7705 | `afb8442593fcd80e6fd507b3e8be6904690e406f633cf74bce6265cea8002fd0` | 0 |
| data/pools/statusCache.go | 2217 | `8461981c7f6cab4f58ef113c9971fa1dd0cb6380f5fb670588e90b0e6ac29f5f` | 0 |
| data/pools/transactionPool.go | 41184 | `4a15cec4ae43c6c7995204bba425981aa8e54641e593115bfb7bc27f74eb814c` | 0 |
| data/stateproofmsg/message.go | 2278 | `e019ae7e1d0d8e720ac8cb9869f0270fd00914b33da87766d158b277453b9044` | 0 |
| data/stateproofmsg/msgp_gen.go | 5472 | `196f79cf70be515055c3bdcfadd810948048fd4c8b398df24ecb77a03e143a9b` | 0 |
| data/transactions/application.go | 26378 | `d25846a40dc794882e9bc9004628fda4717877a2042a635256e9d59f23637c32` | 0 |
| data/transactions/application_string.go | 883 | `a686a5a767423dac8a9b5178f06defe2bcebe9f62aa49fb0a49657b38e8ef741` | 0 |
| data/transactions/asset.go | 4300 | `4f9bd7d04249bc258cc0b76758b75a30791324aa560a45b8f64246eef33723a7` | 0 |
| data/transactions/checks.go | 9428 | `bca8fcf3a8701afb7b5069a596a52749c7133c4aa4ff1743758ea66b876c87a5` | 0 |
| data/transactions/heartbeat.go | 4887 | `77c7986dd3ba3aed8eb7567c7aa3787701d4d75578ca4a146334e10c0781be76` | 0 |
| data/transactions/keyreg.go | 6391 | `d6297005bb56c390306bb3e4e4cb88924da3bf85dc27bcaf840cd8db865a818f` | 0 |
| data/transactions/logic/assembler.go | 107202 | `ec9dd4fc282464473f0323cb9088322a103f35a0feb98fd5fe87c9ad6bb859f1` | 0 |
| data/transactions/logic/box.go | 19970 | `888b2ac0afa1678a03301c6f8ccbfa5019b865573438c825faf93dc824a28530` | 0 |
| data/transactions/logic/crypto.go | 17037 | `3d0f69f78a9888dd12b3b60606895f8d0351b1b1d25f6f41907c157ff6debf46` | 0 |
| data/transactions/logic/doc.go | 49832 | `3a027136d302e14e8974789e57d8106bcbc8166fc7712c39204cc8c5c86ca8f0` | 0 |
| data/transactions/logic/eval.go | 207464 | `bfbdb22b2b975164663f6403976fbfae6328a6a958dabd6e0cb756a6490a7dfd` | 0 |
| data/transactions/logic/fields.go | 68272 | `44fce5b36596a0b2f73e10e6ed7498de45893807e581c92b63f424ab7848b5aa` | 0 |
| data/transactions/logic/fields_string.go | 18109 | `ff964861ae7dab5b8a9ab576fc0b82cb4da1ee3b2107bd839d60d3266c075832` | 0 |
| data/transactions/logic/frames.go | 3489 | `0e05aece96cdc45676374d88b6cceb13e450cfbeda60cebc2cdab058713cb241` | 0 |
| data/transactions/logic/mocktracer/scenarios.go | 28798 | `e24de14156d3b3bd010aa4c171f0a989c1e20283ecf679ef7e326dc3ba8826db` | 0 |
| data/transactions/logic/mocktracer/tracer.go | 9724 | `85d0c36c194830ecef6ccac6ac7512ffe58ba3a9e2c0f368ef2c4a6f13d0df76` | 0 |
| data/transactions/logic/opcodeExplain.go | 10499 | `ef9102a1527d2ce72b571a55f0440d25778d89b2b8c7b5be805b9bc5a389b75f` | 0 |
| data/transactions/logic/opcodes.go | 51240 | `ea62ce062d0872e946a476830e5c9e79173d2bb4ce472e73e0a39ba14ea0c5a3` | 0 |
| data/transactions/logic/pairing.go | 25724 | `a68addb5de9768a360558b3574296c32f5bf4a51620f63063d49b21facd3647f` | 0 |
| data/transactions/logic/program.go | 2525 | `aa7214412c696a66d656256d698cef60af44a9e98948c8fea694bdaeca975b02` | 0 |
| data/transactions/logic/resources.go | 16013 | `ca6ca0a0f9dec004d431dd645310b76760aecaaf672a62de62cb3124b8bfbd60` | 0 |
| data/transactions/logic/sourcemap.go | 2951 | `e723eb5a268cf6fb0ba11e1309e2b6be504bce2d28cc17ded35196b26eab43bb` | 0 |
| data/transactions/logic/tlhc.py | 1984 | `ca8b3c235757a6351af25f1c20e6a68fd66fb3278dde55a1a5aa1769bdb9904f` | 0 |
| data/transactions/logic/tracer.go | 13356 | `c0047648385919a4d34cfaebe88c5b0513092be4e1022ac2d046706a7f84fd12` | 0 |
| data/transactions/logicsig.go | 5851 | `98acf931772f6962e65fc30abf147a4479866657bef731027c9b0081a91fe328` | 0 |
| data/transactions/msgp_gen.go | 180830 | `1637887a15dc329f8225de89955e1893f82832eea147a1ea1a214e41a4a2ea88` | 0 |
| data/transactions/payment.go | 2281 | `329527018b8930021f157f4095f2e4b91a1078b174b7a779c0ff73a6f1eb16ca` | 0 |
| data/transactions/payset.go | 2254 | `b007154f96f8de45f8aceb1fd45bab98c161e4b4665756b76a5dbd06a7e52aef` | 0 |
| data/transactions/sig_scheme.go | 6075 | `d57b0b4e27edb49d3e520a8985a534037e3cffaab0163b42eeb87db3282e91d7` | 0 |
| data/transactions/signedtxn.go | 8634 | `6b99b684588088b4ff9f7888c9ba1e182a5b6c2459170ee49b28c27b00f0e93c` | 0 |
| data/transactions/sksig.go | 8498 | `9e128defc22a160b76cea9f43f5e7f47d724d3b6ca669a5e0bf505b14ed79bea` | 0 |
| data/transactions/sort.go | 1528 | `132bad70da172d42c71b509730e1710c1b56b3c5cdca55ecac157b0e917f45bc` | 0 |
| data/transactions/stateproof.go | 3338 | `d9e7a5ff6f06348e5b04c7c4e26e4c4968b82640bca0b3a85ff38b9cc4de029e` | 0 |
| data/transactions/teal.go | 3725 | `a7570ab2b9189efa34ea3906587f126994b105f6aa9c1089b566b5a5afe47c06` | 0 |
| data/transactions/testhelpers.go | 1105 | `f5f48073b95ec4e810f067ed8525f7d21b94e9e8315a6a49605eaf87de4dd37d` | 0 |
| data/transactions/transaction.go | 20068 | `0d44874905c0edee1acc67222bdddb312320b3d01a6fb8835cd7bce146879d15` | 0 |
| data/transactions/verify/txn.go | 30135 | `cc4cfa53c3f39a5789a7a2695cd96fe258e33dad149fceca67eac7d791ab5d94` | 0 |
| data/transactions/verify/txnBatch.go | 13520 | `4fd9d37a3875f63e7830e1176eac6cb953a661443011b4690abc93e89b47e5e2` | 0 |
| data/transactions/verify/verifiedTxnCache.go | 14488 | `15855d83986af297cae3fc9589240d47b2e0067d1186e4ab39f4a2097b07e157` | 0 |
| data/txDupCache.go | 6741 | `0bd1e401fa707b3a18ae84fe2bc0bc581b740fb64c273982870102afd498c3e3` | 0 |
| data/txHandler.go | 38267 | `fd49f8e573515031000ebcc105a4da88fbd775d8d8c5eed50d625c94de4bcf8a` | 0 |
| data/txntest/defi.go | 13125 | `a8cdd79dd1f41a835eca5daf357688124d1371d319d0eb55065120da5d519598` | 0 |
| data/txntest/program.go | 2726 | `8dd88329f58d0bd2ce47a14f468fe9b9214fa2a5753983fc020ae68bea61e6ec` | 0 |
| data/txntest/txn.go | 12032 | `df4f605889d90d6325fa4a6668c80e995013f9a6e74920e248dc6458df0946c5` | 0 |
| gen/generate.go | 13792 | `37bc8020333d5ac7c52058ce00cd8336f76af814b7108b6c8816a0c0cb022124` | 0 |
| gen/walletData.go | 2220 | `8620308de30cf6e395ad74b5fcc0e75282c9b0baafd7640bc5362cf8e97cd5b3` | 0 |
| go.mod | 8844 | `1d6aeae0e10e6c258510a5117d641d6399abd7750d6388613b3c32d8a51dc819` | 0 |
| heartbeat/abstractions.go | 2326 | `6199cecb2edb70015f3c7186899d327d6790d9313541510f54e943818f29fafc` | 0 |
| heartbeat/service.go | 7755 | `f60b3d5b701fa374535231946ccb28cf31bea324323848dc6db947ab673134bc` | 0 |
| installer/rpm/RPM-GPG-KEY-Algorand | 1757 | `da73bea9d17be7360eb43478e572dadb8d200648bd6625475b1c20a5288d2e44` | 0 |
| internal/rapidgen/rapidgenerators.go | 3599 | `2e6719505c8206a148fb5fecca0997f0e521e69421a6f9210ede7bd738284102` | 0 |
| internal/rapidgen/tld.go | 10913 | `6a1055f0d703b3ff32e0c536a6545417d5aa5ada7716febed5c6c72a3018cdb3` | 0 |
| ledger/acctdeltas.go | 43731 | `12a85cbd25909259f81b45e409a69e16c001d75e84f90491def59fccb2b2931c` | 0 |
| ledger/acctonline.go | 42310 | `ce629d942badf0297ec57c8c0d5bcdbe0d03fe6576ba0a36f3f9943ec47aab55` | 0 |
| ledger/acctonlineexp.go | 2049 | `fb2bbe3585ef47e518264cd35d3a9b2e7d81ccaff45361b6854041516f33cc89` | 0 |
| ledger/acctupdates.go | 89450 | `1d8f6d2d2d549fb7a309d8c86f11ae0eef712bccc3e98cdce5386a0e1f68d0d5` | 0 |
| ledger/apply/application.go | 16707 | `742cee7d6c4d818270b4e69ff71655a939b222246992415f9fa4144526a7d8de` | 0 |
| ledger/apply/apply.go | 6737 | `48bedee5dcfc663bbb9733a586dbb8412925a52cc741aa1116bfcf7d53a79fff` | 0 |
| ledger/apply/asset.go | 13644 | `bc14a3b8376f5fa4c29ae2068b24c78a5d7af4eb7f8c551c23a93b4d98b2b53a` | 0 |
| ledger/apply/challenge.go | 4108 | `e16f4e98db1d482866371b6d15b9eaf3c2eeb332ca71be6cce28dd7928069010` | 0 |
| ledger/apply/heartbeat.go | 4829 | `a9a6d400666e80d81bbf453793e9fd268388766c6910e0f8259823d9aefe003b` | 0 |
| ledger/apply/keyreg.go | 3607 | `61e1fe52376d21a00227579f054915512127cdd12ac0eaac3f018a5aca1c5226` | 0 |
| ledger/apply/payment.go | 5416 | `a2a5ba054bc62a4b23389b12db542cc18e0d6b44274441114c5436500257ba09` | 0 |
| ledger/apply/stateproof.go | 3822 | `6dc4ff33b8a3974809c82f43437cc1010b3b2b7f46c004a4696561b46ccff2ec` | 0 |
| ledger/blockqueue.go | 11146 | `f422345c340fd87c8a902face0025eec2a17d813733d30aa9bf046263d542c80` | 0 |
| ledger/bulletin.go | 4289 | `ee7dd9b6c4a5699e5c375c5e6a42a16e4bb54b8a3a6de79337e1fdc40868b844` | 0 |
| ledger/catchpointfileheader.go | 2029 | `f9853b1ecb9aa09343b6f59545d399fc18cb86189bfd15163e390820dc521fbc` | 0 |
| ledger/catchpointfilewriter.go | 22177 | `23d5b595a700ba4e9b5a4a1743e9a00981220f62ebcd06ceb7606074e8a4e1dc` | 0 |
| ledger/catchpointtracker.go | 64110 | `238309f820fd551afcef102cf9856a5145e665fa3112a1822f41046b29f70d5f` | 0 |
| ledger/catchupaccessor.go | 52628 | `d4c845641682df179a4e1e9c3a5174dd93eaa5b9ed7affaaf2412b71adf23b7b` | 0 |
| ledger/encoded/msgp_gen.go | 20396 | `b5102bd2a891de249a2519676052dbd022d3dfc7dd154e40dd0e85b3af46e13c` | 0 |
| ledger/encoded/recordsV5.go | 1157 | `6093e56b806108154f99fc90e554daeb7956a71b649449f55802abf5a77f495b` | 0 |
| ledger/encoded/recordsV6.go | 3940 | `ee86e3987c6f065ce59f14db7e9f740e8ecc83f175f1acaa97895a27e3d87f67` | 0 |
| ledger/eval/appcow.go | 25262 | `678105baf8c752334d0f1a04a9d0f41976e0776d4092f9d8e4307403819fa74b` | 0 |
| ledger/eval/applications.go | 12383 | `4dd3ddf419ae4cea588eb23ffeb912171e50171f967c5efc756228a528d70c1f` | 0 |
| ledger/eval/assetcow.go | 1507 | `78407f32a7b9ae38fdaaf828b6a8052dedad9bb44eeb11e967d27d55b2e5fc8e` | 0 |
| ledger/eval/cow.go | 15466 | `a29036bd10ff11245673e8ba4dad651b7067c1f34c25b7ef39fffecf22cbbb0e` | 0 |
| ledger/eval/cow_creatables.go | 8071 | `9b8bc58cc9c86072cd87165a3f2e230a2a92da52509999c1b792fa2ce4e23853` | 0 |
| ledger/eval/eval.go | 88377 | `91a4deeece55b8fbffe294d56eef2fe45333aa84a95428af2565911bc2796405` | 0 |
| ledger/eval/evalindexer.go | 1830 | `80bceea9f31aa8c1aaf4a823fabd39cbff1e6217500d2e317f8e072d5bd3165e` | 0 |
| ledger/eval/prefetcher/prefetcher.go | 25169 | `21f970ff6604a65f0772e930255e317d4bd09f8cd60b6996ee0ee10d7dbe115e` | 0 |
| ledger/eval/txntracer.go | 6303 | `2164d8822f1f37eee35de04cc3d02f79ea51ecae24c0df7e266eaefd13b7e288` | 0 |
| ledger/ledger.go | 39695 | `ac49689e5438c31fad74df4339386fe3c4f74c07eb4f04ae1519c9a99484870d` | 0 |
| ledger/ledgercore/accountdata.go | 8169 | `71553cb2d4b481ba1af80c4e074b5bf67955ad0e3c64890e34a0bd02de9b3a9b` | 0 |
| ledger/ledgercore/accountresource.go | 3670 | `ec26a98b48cb3c0c5e75f470d3d3b1cb26e6c28a67886186d3e1628a2246b63a` | 0 |
| ledger/ledgercore/catchpointlabel.go | 6865 | `593ac5b9a05c4426095e13d632e9425ad4a7629b5356ae3742ec9adb46334fde` | 0 |
| ledger/ledgercore/error.go | 8052 | `87385f333f1a227b6b9b8225fbd124044dac9750f327e29256aa911f866a5bba` | 0 |
| ledger/ledgercore/misc.go | 1288 | `75ccd00e69c0ed9d220ef4ae128da827d682b7a53bd3dc278b8874e4fd65e239` | 0 |
| ledger/ledgercore/msgp_gen.go | 20465 | `ca4dbb5851ca9f32392603dd8f5c24f6cf4a878f9dbc4674e7ec045a7eac1e0a` | 0 |
| ledger/ledgercore/onlineacct.go | 1496 | `2b14b2e79484ccc9d5fe4f58e1ab2ac770f5d2c498a0ae133d5fe7c4f9485091` | 0 |
| ledger/ledgercore/statedelta.go | 28860 | `145065075ebd9d63100d8aa43c0cb0b168dd0f26bc47b995b794f81a5c09d3ee` | 0 |
| ledger/ledgercore/stateproofverification.go | 2365 | `9bb6f7222c50b47f42bcf72172fb5da6701bb8be7e2f3ff124cba3b27d156cef` | 0 |
| ledger/ledgercore/totals.go | 5085 | `c60ed2be9a977db62bd1ff467c381a1a823df5e6e498142be8a12e0b38776736` | 0 |
| ledger/ledgercore/validatedBlock.go | 3611 | `0dfb23da2d2e9c0756558501a03a8719fde9f85533f3af385c17c551c7b2bf79` | 0 |
| ledger/ledgercore/votersForRound.go | 7704 | `2328222d15d4a47014f318fb50d225a840476a7091db8101c291dc8e756598bc` | 0 |
| ledger/lruaccts.go | 6417 | `a0f2d8970ca07d68ba51edf9d5ad96f80d7a454909d5dfe1be2998088b0fd1f3` | 0 |
| ledger/lrukv.go | 5025 | `deb5cfb084b4af0ff383787601fc0c714245efeac24981415639a5d53113a964` | 0 |
| ledger/lruonlineaccts.go | 5395 | `c7340858b05d78ab3f268609973be32618d44b21bd2542bb403e6139805bfc21` | 0 |
| ledger/lruresources.go | 7531 | `56b0666738298272ad630dde4e4c61522a3714f5e433bc285a94204a8b802b27` | 0 |
| ledger/metrics.go | 3346 | `e77406c7965fc9d7790bcfa27d50ef096fc336ecf7f84d3458a5ba6d11810355` | 0 |
| ledger/msgp_gen.go | 27097 | `2271d04ae02bb7cbf0d56e3169173eac54a343880dda395e074f1dada77588c4` | 0 |
| ledger/notifier.go | 3444 | `7aa3b0012a96d97427ce0f685d41fee4a6b71066ca06b1e66238f7dec0b0efb2` | 0 |
| ledger/onlineaccountscache.go | 4653 | `f99b9a1f97f34ceca6b9c2b7d62ba0ec1d3aa83f926070b4976b219c5c237c9f` | 0 |
| ledger/onlinetopheap.go | 1981 | `d18ae89c89c9290c260a573864898afb7aace6023ada149bda6e644347c07385` | 0 |
| ledger/simulation/initialStates.go | 6406 | `2e7d899d6aa910ad1b25f63d66396a4210aec3b2df10f2a7b79547052a458d30` | 0 |
| ledger/simulation/resources.go | 27694 | `a4e58872beacd1b532ba57ef8febcb74551cb1ed81f07d9ad15293f3e7323d0d` | 0 |
| ledger/simulation/simulator.go | 18855 | `2c6bf0db66d5adce6979287b8a506d04921bd5bcfecea92cbd31c799bc89a91f` | 0 |
| ledger/simulation/trace.go | 14215 | `dabb6e6d47f3d7fba1503a3f80da627485f882ca63febac7d14f580967a621b7` | 0 |
| ledger/simulation/tracer.go | 22001 | `a3002e73d77562006100a67e5b1e0ccb01972f7b5da668e8921994db6547f584` | 0 |
| ledger/spverificationtracker.go | 11202 | `05df37a4898592cbd745aa750a33ee2fad06b967d85b2913f0bc7a690a3a2f04` | 0 |
| ledger/store/blockdb/blockdb.go | 9172 | `be0e3f6bad1946b63e9f33f51bb149ddd30976213ff10ffb353833356b97454f` | 0 |
| ledger/store/trackerdb/catchpoint.go | 9484 | `341e7af2ac09848a48eed2f5c3dc51c046b20035fe7b353948ea053db6359e1b` | 0 |
| ledger/store/trackerdb/data.go | 34128 | `63ecb965f1af8ffafb1ac0d99f6d6bd14464cf42bae31f2f3b6a4acd029f602a` | 0 |
| ledger/store/trackerdb/dualdriver/accounts_reader.go | 7389 | `33df90eeaa96aeb721d40f31bbe8250978c47c0584572397ec3180c46e26c86d` | 0 |
| ledger/store/trackerdb/dualdriver/accounts_reader_ext.go | 12422 | `ec8a925b00cefdb04069a8224a066959dbe91e933268cc0716383ec2190c8639` | 0 |
| ledger/store/trackerdb/dualdriver/accounts_writer.go | 6383 | `b70e295ad06efa3a77f71eb2087520d31a691ad08ed7674110bfdd65e89ff6f6` | 0 |
| ledger/store/trackerdb/dualdriver/accounts_writer_ext.go | 4215 | `de5ca7809d023ba000415c11cf9ca5db2b343cbb56a7ac78069d723002e64be8` | 0 |
| ledger/store/trackerdb/dualdriver/dualdriver.go | 17111 | `4ae09311527d3b338205c264eea1709a721332d95345f5476c5b9b3dc06bd54d` | 0 |
| ledger/store/trackerdb/dualdriver/online_accounts_reader.go | 3603 | `f0cfa47eb4816037691e7c8dab66c80233e6db1a01f99e77bab0b812acc5e498` | 0 |
| ledger/store/trackerdb/dualdriver/online_accounts_writer.go | 1866 | `4323f8ae548e53fd061aaa6c6a69628c9d5ba7effedda8adc4e430f7df12bf29` | 0 |
| ledger/store/trackerdb/dualdriver/stateproof_reader.go | 2917 | `bd4ba571500bc7f5540e30bf6393d609660cd8208f67ad8cce8158d91093ecea` | 0 |
| ledger/store/trackerdb/dualdriver/stateproof_writer.go | 2296 | `097e65b700a337bda78b734d032d4b640e78119f606c86886e4fab0f8d436f02` | 0 |
| ledger/store/trackerdb/dualdriver/transaction_for_testing.go | 2416 | `5db9852d07b4e69c2ce36ebb3e2d67889dbceee01f410d6aaddddac88a9277d9` | 0 |
| ledger/store/trackerdb/generickv/accounts_ext_reader.go | 14528 | `9cdcfa4240c6f74e7106f9bce1cbbe74322d885816ae65c3e759e96961574849` | 0 |
| ledger/store/trackerdb/generickv/accounts_ext_writer.go | 7539 | `4e5fb2b904f9f979f6a16a857350782c0f2efc54ae9d47bf019065a92f009b40` | 0 |
| ledger/store/trackerdb/generickv/accounts_reader.go | 9932 | `20e0e445914c103b0d1e6d470440ba2287a45ebb78f692f6c55c1efa2a74928c` | 0 |
| ledger/store/trackerdb/generickv/accounts_writer.go | 5350 | `73a7ccb918c94d1c73fa33a6d930101f9c1faea5b0e970fb34815ec4472b957c` | 0 |
| ledger/store/trackerdb/generickv/catchpoint.go | 1694 | `697cbc44c8bb7491ce99d658d3f64129e071b6dfe9102c3f65e12f1448d2e05e` | 0 |
| ledger/store/trackerdb/generickv/init_accounts.go | 2161 | `6dd555f667960f04c90c79f8d967de6aa4fa2858b77306fe710560bf76df29cb` | 0 |
| ledger/store/trackerdb/generickv/migrations.go | 5681 | `fc321ab33f4f52a72eddc675f5bca15268357a853ca709a913db250301b27e7e` | 0 |
| ledger/store/trackerdb/generickv/msgp_gen.go | 3499 | `6eb08dde0424767e6768ce4b3100803f7eaacf6eda930af5a7c2a9ba8f0eadad` | 0 |
| ledger/store/trackerdb/generickv/onlineaccounts_reader.go | 4108 | `54757059c01a2980684053dbd87dd297e8a9eddf010e40d6988e884d1e2f65cd` | 0 |
| ledger/store/trackerdb/generickv/onlineaccounts_writer.go | 2283 | `d323f171c8c6d2d0cb98b3b622a379112fec1fb778b0e851c48131bf73ee16fb` | 0 |
| ledger/store/trackerdb/generickv/reader.go | 3243 | `56b2e4f4b57f59e5f2ca84b8e325a490c2e609b86c9c76a22318300889449331` | 0 |
| ledger/store/trackerdb/generickv/schema.go | 11338 | `eb2ab3d2a3cf50275406fd8738eb5a560199275f1b6b9ecd44dfd9542356d48b` | 0 |
| ledger/store/trackerdb/generickv/stateproof_reader.go | 3034 | `39f0ece567d0d924ba5e27efe7fc396bd0ff103c967c937c3bd98142ccc454d9` | 0 |
| ledger/store/trackerdb/generickv/stateproof_writer.go | 2513 | `be681b4dc8e8fc50d6a85d7a42359f1293839a4034fe62022d23a186738da1a9` | 0 |
| ledger/store/trackerdb/generickv/writer.go | 3294 | `2f4ec6858e8c92ecd2d2e555e91b03c149b9da02e10f08e8e9e1237ad9f244e8` | 0 |
| ledger/store/trackerdb/hashing.go | 5011 | `9046117b478bd00178c27a41dcaedc4123d6a5587c417590157ebfd3688d11f3` | 0 |
| ledger/store/trackerdb/hashkind_string.go | 688 | `a2970aea2eae1414091a4a5ee181f9a4089f9895677011f4fddd9591598f45c1` | 0 |
| ledger/store/trackerdb/interface.go | 13543 | `1382401aa1aac9cc4caf3b65a9710991627ccbfe85457a7e56e21979e679f62c` | 0 |
| ledger/store/trackerdb/msgp_gen.go | 63167 | `e8590af45e041bdaa1de07a7910ce7c47914650a2d7c112c524e1555f6d1c2fa` | 0 |
| ledger/store/trackerdb/params.go | 1394 | `29d5ea7fcb61d853dc90f74bcffd7a3c578463ab008e95ad35fac0b1518eeb50` | 0 |
| ledger/store/trackerdb/pebbledbdriver/pebbledriver.go | 18947 | `bd71701b8cb2e18a65958840c3235fb9074beee20f025002bdc26ce13e9aa698` | 0 |
| ledger/store/trackerdb/pebbledbdriver/pebbledriver_arm.go | 1153 | `d8bfb47c212e24e1cb49d98e8d00b87e85108d701d2ddfc0e07d07124f15dd6a` | 0 |
| ledger/store/trackerdb/pebbledbdriver/testing.go | 1501 | `d3a6cf6a9eb6a143c332df8439eca7996fe5c0a710bcc93a1d1da9695e566891` | 0 |
| ledger/store/trackerdb/sqlitedriver/accountsV2.go | 29153 | `c5db723ea86412353774d497963286d09ad5949e531b5ea4f5997a3297877c3d` | 0 |
| ledger/store/trackerdb/sqlitedriver/catchpoint.go | 21973 | `6f2e40c3dd8d090e557049a4a16b8b2d1587a46958864b2c2ea83927634ae80a` | 0 |
| ledger/store/trackerdb/sqlitedriver/catchpointPendingHashesIter.go | 2524 | `7cfa59961efb1aae6af13dce19f4fc244cd47d9bf09a29c87ae0164705844820` | 0 |
| ledger/store/trackerdb/sqlitedriver/encodedAccountsIter.go | 5727 | `501b9b104bca8eee1dd067b8419d621e60109a60a168bb8a8a04aef6db6ef4a0` | 0 |
| ledger/store/trackerdb/sqlitedriver/kvsIter.go | 8225 | `3cf7f60788fbb6e4d14fc0190af88d43e0ad769be0139f608bfeb8c23b8621c3` | 0 |
| ledger/store/trackerdb/sqlitedriver/merkle_committer.go | 2533 | `c095e7bae9a42b584f2d9c4526a627c3ac100d752803d3501a582ee4e4144657` | 0 |
| ledger/store/trackerdb/sqlitedriver/orderedAccountsIter.go | 14864 | `899551980e28fc03a276ad360c260280f91f8ae16e8a49115f8fb3485b521e10` | 0 |
| ledger/store/trackerdb/sqlitedriver/schema.go | 32002 | `2115fb8409a9ebfadf6e867410494aaa6ac97906dba8cc5e4ca00b7f5a97bb2b` | 0 |
| ledger/store/trackerdb/sqlitedriver/spVerificationAccessor.go | 6054 | `2991a441bca33a7becc59d57885891bf3cab31de1c2db4c7ce525dc7a240ce89` | 0 |
| ledger/store/trackerdb/sqlitedriver/sql.go | 32045 | `08689aab8fb3d10aeed06e7298fc74cef5c84e6d0b4fd225ed1abe95f64d469b` | 0 |
| ledger/store/trackerdb/sqlitedriver/sqlitedriver.go | 13328 | `eb2f32a66c04c456a72669ba86b928649b718232cfad7608aa5f41741b20662c` | 0 |
| ledger/store/trackerdb/sqlitedriver/testing.go | 5299 | `b84f40af83bf8cfeebdbda880554c12e7daea4f7cc9144cc139751e06a7a8d30` | 0 |
| ledger/store/trackerdb/sqlitedriver/trackerdbV2.go | 20792 | `50533185d897295a94e74ff02984ca77cc0245829dacf12660a3377c9876b5df` | 0 |
| ledger/store/trackerdb/store.go | 6418 | `d657560b7ce880051729eaf78daf225129e39a16dbeafd333a5f2cba13ed5d7b` | 0 |
| ledger/store/trackerdb/testdb/testdb.go | 1494 | `6de45f4949ae0b38b07c04548aa5baf10207952f864d347b8d03a31a65248f9c` | 0 |
| ledger/store/trackerdb/testinterface.go | 2040 | `acc1623369de5bbde159d54e1ead8d7b4e14571c08a38373d81b05dbd975134c` | 0 |
| ledger/store/trackerdb/utils.go | 1673 | `4b9872a7c74a8b6ca34b8f748152372505a2f669c8dc00d8fe7cd3ad5ca4588e` | 0 |
| ledger/store/trackerdb/version.go | 1063 | `cb76a2af45387cb386ec4d233882259d9a69c7f966ae26d94b6ba34ea9235484` | 0 |
| ledger/tracker.go | 39178 | `3b0880be17047083f206ff1055bbf32e02f2c5743ffccde56135e7f44b83ff6e` | 0 |
| ledger/trackerdb.go | 2771 | `8b5f901d153733b0ec1321e04ec7908684822a159f85a1b4a56c71f3d7b6226c` | 0 |
| ledger/txtail.go | 14887 | `fa55d81899f962f6f45c7191ad90eb2518f25f2fc751e04d343b2004c48fe550` | 0 |
| ledger/voters.go | 13114 | `d4512a05452dac1172e9f786f999dc88c02f5b5028520cb5dd9daf6211a784bd` | 0 |
| libgoal/accounts.go | 1262 | `2643b1610f5bb9c621af54d851020465e061c1275b2ad0e2b869436787b30e17` | 0 |
| libgoal/error.go | 972 | `9a590b9f20f5c868b3cffde77433717380bc7ccdd761435c214379230c7346b3` | 0 |
| libgoal/libgoal.go | 38483 | `1a60790653e2a225a5409098e0acd7fa78c3058feae8536fa758a2f57d0cb501` | 0 |
| libgoal/lockedFile.go | 2419 | `7854b2f52a43f1ebf373c6833c3c256f8c83b96123ea6052d05e2583f2314eff` | 0 |
| libgoal/lockedFileLinux.go | 2667 | `7cac9f902a9dac649b20659d06c02c872440a4fd5603611694ca9bdcf511c1b0` | 0 |
| libgoal/lockedFileUnix.go | 2300 | `11903316a0f3e71516bbba52ac6cdf7b43fd3f8fdf374fbe8fa99beca6a0e75b` | 0 |
| libgoal/lockedFileWindows.go | 3021 | `6cfd20a499014e32e124460333eeb3e5eaf8a206d0dce528d7c625d2cee7487d` | 0 |
| libgoal/participation.go | 3122 | `8b520751d45a6c524696cfd1cf5d4ca23cee9bc38eb2214af5f3f6806ad0bd9c` | 0 |
| libgoal/participation/participation.go | 3277 | `38a3c8ff027849128bb1f7a67c3180430bbd0f0c8214978dfc3e796bfad38a3f` | 0 |
| libgoal/system.go | 2658 | `98152826bc70f7643c0eb969bca50c1aa2d659eb06cbb77e54886cd080b10e1d` | 0 |
| libgoal/teal.go | 1267 | `221c2c97c418b7c3d5ccfa0a0b84f81cae45f888600d77db9d2aef9a3ea0ba9b` | 0 |
| libgoal/transactions.go | 34841 | `209584c9397777d791a76dc4071536b94b995b4764efb2c0f14675583286c28c` | 0 |
| libgoal/unencryptedWallet.go | 3339 | `e499bce62d083350c9cb7a7978f72c5f5bc8ea6d8e58fdfbf0915229b39ed8de` | 0 |
| libgoal/walletHandles.go | 2494 | `e8bf6d3d3da760434535bc5312839f966bebc532e3df9bf173e2f00073d87b10` | 0 |
| libgoal/wallets.go | 6242 | `1a63cad4a71d1da91a0fb7621b54811303eb1989db8e346902d1e06a20fd845b` | 0 |
| logging/collector.go | 3893 | `bb2f8a57fc0176563222ecf576c8ecadfd54e0bb299fe72067a0c3c7a4361346` | 0 |
| logging/cyclicWriter.go | 6492 | `44cf0f47cd6a194eaea306a6c5f0cf43f7356235500b6629945fc3dda672a1a8` | 0 |
| logging/log.go | 11570 | `701f95c8f985b4ed8026b5ebca5ea60e48367f08a790eea8c06bbd3e225710f4` | 0 |
| logging/logBuffer.go | 2630 | `8bbcb2813335e562b46f18d33e2418a95c236e7ad512f0d12cd4732fb70d0153` | 0 |
| logging/logspec/agreement.go | 7031 | `a6d7f916a708bacd7d0e3782878937d67599d2a83d6e12f1a11c7e753ec4b991` | 0 |
| logging/logspec/agreementtype_string.go | 1797 | `2fd25113f4ada1180fc2fd79ceeb68c44bfe637f6a8d9962f451931a25a6fff7` | 0 |
| logging/logspec/component_string.go | 775 | `f95b52ee21de5781dcfcf79390c8e5f2a2ecbf22db2405f1138aed83e34238d2` | 0 |
| logging/logspec/ledger.go | 2180 | `3817a5b19ee30c18de991628da5a200424ce4d90a087c2ee3f3d7d3c65db086d` | 0 |
| logging/logspec/ledgertype_string.go | 673 | `ac61751324093ce9d06e585d627386f68bec030cc38d3918893c1044986ba571` | 0 |
| logging/logspec/root.go | 2552 | `7a2b2dd99d35678e43e6bc20f03d88638ff9704bf3b06f1abfc2fd358e833fc1` | 0 |
| logging/telemetry.go | 8006 | `1256b7997030ec2a404d7269117fcd9f68d4a122d023fc1498de06a1e19f1ef8` | 0 |
| logging/telemetryCommon.go | 2786 | `08835f3c2bf18d01e426fadc84d3f16786aa5f765c136f97e42748c8be84b824` | 0 |
| logging/telemetryConfig.go | 5720 | `f596ff0f741d638f1f7740795f4e0cc6c09480d197cde07c4ffcc442176041fd` | 1 |
| logging/telemetryFilteredHook.go | 3302 | `d20d9ad73feda8cdf47f1e34d1b4ad6dedea116c94fdece6fd844294e9973dc4` | 0 |
| logging/telemetryhook.go | 9021 | `f56da8418e2cb9f1e196c80583fe933dc71bf59eaf74209aee48a6188cbdbeb4` | 0 |
| logging/telemetryspec/category.go | 1426 | `97abb344fe6d64b227af9f362dad7ec37cd538bea86c5c1361dea173722c072a` | 0 |
| logging/telemetryspec/event.go | 12758 | `a397bc13df809b420cde388fa5c705ba56a74c4adea3568024f9e02dffecd8eb` | 0 |
| logging/telemetryspec/eventTiming.go | 1886 | `4a831cb392b38a8b64b5ece679adc40a12c8e3a19cd09172391413a138c48ff2` | 0 |
| logging/telemetryspec/metric.go | 12734 | `849becd1ce0c8f318dc3ddeb2c13adc9b298215804cd92c53b6e29e2bce33a5c` | 0 |
| logging/testingLogger.go | 2234 | `3823a326b9edff3ebeee15710e935741fb776f62ac4718b9c9f030ab2b04591b` | 0 |
| logging/usage.go | 2115 | `d0c84d3785200aea314db16c45801c3ca0f4a5c96c42afb4705dd4a095e9d08d` | 0 |
| netdeploy/network.go | 16307 | `1951aa66d9cbbcc9084d948c5b4ae458555879f6051423b360abc03ffd02844a` | 0 |
| netdeploy/networkTemplate.go | 11745 | `90d485ad7ae5611ba6b460f802338f686a827ccd89ddd70630b8f4a647adc19b` | 0 |
| netdeploy/remote/bootstrappedNetwork.go | 1717 | `020c26d13d9bde6e555c8ab6f860bfb03f51720957befc94de00fe19a2281115` | 0 |
| netdeploy/remote/buildConfig.go | 1697 | `d3def4af532b72f24aadcd41f08101577e82b7f56ee15671d3e89c3450e13d34` | 0 |
| netdeploy/remote/deployedNetwork.go | 35001 | `57989efdc6caddb9d27f6d5c2bb823014e2edb336916102f07daf88d82d2694a` | 0 |
| netdeploy/remote/hostConfig.go | 917 | `a5cbbda7251833174331b0a9fd914921d8d5470f405666ad3619b2f032be9c42` | 0 |
| netdeploy/remote/hostTemplate.go | 1957 | `c47aceb7436f6a3cccaa86bce41972608f321ca90849731dea44529f3a37c0f3` | 0 |
| netdeploy/remote/nodeConfig.go | 3617 | `2324fdf24b8b7c7cff3fd532246730035e075c84785640534f65594243500dbc` | 0 |
| netdeploy/remote/nodeWalletData.go | 918 | `a3f46fe10c9902a7924595fe9d331b386ac8faf2416a8fea58154493531cf579` | 0 |
| netdeploy/remote/nodecfg/nodeConfigurator.go | 11483 | `33b52ee82a675b45f4282b66f4d0fb9bd2872554b3295992f15be090f17a486e` | 0 |
| netdeploy/remote/nodecfg/nodeDir.go | 12573 | `b151e1c7b79a9ffb6d5ef931a9e639ef018bbde19610e4f21b322204b85aa83a` | 0 |
| netdeploy/remote/topology.go | 1140 | `ab86b2fe037e4e6f3c95f0126ec74a5d05c5c5be39cf7ff8d2374ee90091323d` | 0 |
| network/addr.go | 1442 | `237b6b6d23fd37120e60b23b33a8c88a0266825f4f41e268d6300c0643a26ecd` | 0 |
| network/addr/addr.go | 3469 | `4b75a7fd788e22e6b70f68351e68900048ead8ca5c4577803c920085a8326385` | 0 |
| network/connPerfMon.go | 21418 | `a725c48dc30b88e4d13c00e929bf83e3fb3e740888eae55012d0ea25013b17eb` | 0 |
| network/gossipNode.go | 12213 | `522e46436f03b1c8a78cb38e50e79092aa276d2d66ab23eddf4b77073ea58e9f` | 0 |
| network/hybridNetwork.go | 9423 | `41ecb1d4549c43cabc2f331e0108100f11fad0439d73cc8c1872319a79ea19ca` | 0 |
| network/limitcaller/dialer.go | 3110 | `ce2b1ce8d8535ee95aaef70743b1caa7b2346ccc9b5ffe81e3d10265d5e21d81` | 0 |
| network/limitcaller/rateLimitingTransport.go | 4468 | `1b113d0f1723cf128e90a13f470c5a69e5e8404cc7e3bffb5eb236776d6c2ad0` | 0 |
| network/limited_reader_slurper.go | 5611 | `0a7d1290de122e51272ce8c8825e09be65c5cac8333f1fc5c9e05730942bae3a` | 0 |
| network/limitlistener/rejectingLimitListener.go | 2262 | `24f3ecf126f47a2817d1cb10aa59c8ea93e7b01cc3afcaa222cfa5c0a6ef43ce` | 0 |
| network/mesh.go | 8609 | `550b4479b1fa295a42f0c44f61242e2fcebdad2edc09737900980d740da60f32` | 0 |
| network/messageFilter.go | 3618 | `2446f5849dd92ef063067889681478d5714ea6b9d7907da5a859f7622d63b523` | 0 |
| network/messagetracer/graphtrace.go | 2187 | `793eabf2bb9a54aed287722cacccfb51ba419cf2bd6e93bcb5898c54bdbbfeb0` | 0 |
| network/messagetracer/interface.go | 1944 | `b19f41c6d49a2fdeffe1c5cf65451ea0c15813c0252d3f75bd2784ccc0351e0b` | 0 |
| network/metrics.go | 16231 | `c7082c7e6e03dfbf5bb488af323aeae726fe54960a001bef30bbc5b69ca25544` | 0 |
| network/msgCompressor.go | 11910 | `56e849c968f02d06fd4ddffb9479cb4431576badf13f78018ad3b4bc0fbf41d2` | 0 |
| network/msgOfInterest.go | 3523 | `cacbcb01784e7610e2fbb07a4f1e244b3d0c20f8798fea5eb85f67719ec51486` | 0 |
| network/msgp_gen.go | 32640 | `9e8a5de574e047f45e1ece14545bef4b785d9ca3056ed2c46843ead8252fdcad` | 0 |
| network/multiplexer.go | 4800 | `38666ff419e710fb1738dfb70016426d206004b7e998c023add4e942cdb08ebf` | 0 |
| network/netidentity.go | 21927 | `dd923ecd9019e6b2566a61152a230970275d2bfa94e9923c0ef15849a452ae50` | 0 |
| network/netprio.go | 4149 | `9d852184eacd8cf9fdbe24fe07fe657d560c86e8f46c69a222f2365be7478bca` | 0 |
| network/p2p/capabilities.go | 7424 | `2deae7475503a9920d2af6a71d34171e7a175b20c81dd2674eeb4b617e3a538c` | 0 |
| network/p2p/dht/dht.go | 3148 | `0cdcca8f4ddf548e7a5a17d72da93445c51ea371265e646de31cd86c20b5b999` | 0 |
| network/p2p/dnsaddr/resolve.go | 3124 | `57ea796bfd2280f3870b50ae248c24d54b01103d9cf9bc38a520f714523dc157` | 0 |
| network/p2p/dnsaddr/resolveController.go | 3302 | `6ad901db36a76f7bf57e21df4e184f444959912c7eb4563867247e4faf443d27` | 0 |
| network/p2p/http.go | 9063 | `0ab7d1e93e14797b26af6bea1679ecc570bf4513a538d65b5a3766e24caa6d2a` | 0 |
| network/p2p/logger.go | 3863 | `b3d33326f0f431126c870e0e0bd4f7191e7681853ba2974f8f0232d25b1a9b18` | 0 |
| network/p2p/p2p.go | 17880 | `91a47228229cd35428719b0d2410d2fb62c96112d44f8cdd70149270e767617f` | 0 |
| network/p2p/peerID.go | 5912 | `379de8be07b41b02b6a0d0432e19714541e1fbbf8d37e58dd590470cc8ab4b39` | 0 |
| network/p2p/peerstore/peerstore.go | 13068 | `89c2fb7d05b149b0fdaf40292682aacef20640399a2a078c20b173237bca50cf` | 0 |
| network/p2p/peerstore/utils.go | 2343 | `04044fa3d344eecafaa21c046e4baf70d4f042d3f4bb9c610aed9150600e9dbd` | 0 |
| network/p2p/pubsub.go | 8692 | `0aa60c720f6bdf811e26a83ff836fb7fd44e633ff768e2985b5ec0e2c65a3c68` | 0 |
| network/p2p/streams.go | 13581 | `8024404e8c2ee2865836996f00c1195b52d42095842971f470dbd207232a3a6a` | 0 |
| network/p2pMetainfo.go | 4266 | `347be539f2aa49939652a0a50016ca9c07c9d3c931d5912ee14800faaf3f770b` | 0 |
| network/p2pNetwork.go | 43398 | `187688f81191ae93db6af02be4ce09b2f679af68979829698b4c9ca83ee6d417` | 0 |
| network/p2pPeer.go | 2853 | `39a5e66428f56f30ba7aa4e615c19a317928d59288dc682bc1b5e867fb6ebd06` | 0 |
| network/peersheap.go | 2184 | `ff68a22fa6a9bac28692ed876466a7869956680f9461017ff3d466295d5ca171` | 0 |
| network/phonebook/phonebook.go | 14126 | `d38a660a0ba830b6ef17645cd4d6b82f7cb40127c60a7c689e6523b300923404` | 0 |
| network/requestLogger.go | 4263 | `583ff514dfa738247eac9f2b02564d00228a454036fb553515bece80baec6ac0` | 0 |
| network/requestTracker.go | 22827 | `ce2991f0b769c13a81766c4f76542df30ac869b1cde05100fc878670b8e758ca` | 0 |
| network/topics.go | 4222 | `19cae5c887dab0e0ad47b22745171aa92d53a300863d0ab00d731efc790f518f` | 0 |
| network/vpack/dynamic_vpack.go | 17476 | `123998e7f52f78060cbc4283aa825371416629c15f0755c55e7c1bc407ef3df6` | 0 |
| network/vpack/lru_table.go | 5077 | `5ba6af055e8ef80ce6db074706a4d2c6c596706d04fd81ab253216c3a970afbf` | 0 |
| network/vpack/msgp.go | 5634 | `4eb7c5dabb922e26af07b7a5c494fb780b51f5571131d520b1190e6a7d6a212a` | 0 |
| network/vpack/parse.go | 7455 | `567d03dedcd6aa09a8ccc16a2f7b0443288740db490bf561e8305e8b9dc5f6bb` | 0 |
| network/vpack/proposal_window.go | 3954 | `6d2ee04e0d3ea8b2bfc233b7ebc1be1381c102b446b074dc4e4da82bab725f9a` | 0 |
| network/vpack/vpack.go | 13700 | `6bb117aaf4c49d7bb4510ae6df2949c9b38507ed682a46fe47b3dc130880c2d5` | 0 |
| network/wsNetwork.go | 96583 | `275283601b6ba69cc9435d37813d568dbb82c90736e6954e45f904340a0ffb5e` | 0 |
| network/wsPeer.go | 43958 | `831b4aa44e413d431b6bf4b258113b22aa866840775825284395c485be0b296a` | 0 |
| node/error.go | 2909 | `ccaa513e1df558ff83f5d3060f749036aef3f5179142ca5cb67e4e738c3416cb` | 0 |
| node/follower_node.go | 18454 | `9d305853963ed03fae67625b6e4afa244a1696a688c0172ddf532506eb0f1fcd` | 0 |
| node/impls.go | 5011 | `18dfad208b821cce5b3ad7ec97ca7b4850c3c4d9065b19220303986cc7f45567` | 0 |
| node/msgp_gen.go | 8831 | `3ec85bad46e06f511eef4ab28ba3025ec437185158e6a3ee1b16b6f6f568cadb` | 0 |
| node/netprio.go | 4332 | `8eb64e59a57e53311eecc116468264d41ce99819fd3ad9ac54b90de980b7c966` | 0 |
| node/node.go | 56386 | `c0ae63906fb8bd9bcfefd2d8b35496dada4c4ec5411de3e80b6abdda25ff10ad` | 0 |
| nodecontrol/LaggedStdIo.go | 3185 | `d69a2b6eaa033c29e0b696aae945ebbc6b86a9852a958fddb942a28af291f732` | 0 |
| nodecontrol/NodeController.go | 5361 | `fea9dae71f217579d88993cae50869e233ec000166b7879921e0b689c7459790` | 0 |
| nodecontrol/algodControl.go | 13919 | `0510a4deee885907f39e3b8152d8b9162c9d269f929871ea53bb55c5d4bf4141` | 0 |
| nodecontrol/kmdControl.go | 9054 | `3c1d95d0e1a00ae76957b9da315aa7371fd774857f6de258dcbcf4b75c679c2c` | 0 |
| nodecontrol/kmdControl_common.go | 1155 | `e59e49366bf8004ca0126e0a6d94df1b4eebc35d06e60940abdda2828449599f` | 0 |
| nodecontrol/kmdControl_windows.go | 874 | `a46b8ef1ee34f70a2ae16611a6e3b66404f079bbb7c1c63c5f5d8b6dfee5a826` | 0 |
| nodecontrol/nodeControlErrors.go | 1309 | `4fa948c41a879b51f4b6486f91fbcaa0e665379985612c18fde9d7aa17e363ff` | 0 |
| protocol/codec.go | 10000 | `f46582ba50e048f60cd0bb9e1deb1acc261a9f6ff9fd15067caec396c8abcff7` | 0 |
| protocol/codec_tester.go | 17370 | `28a6168b3e226206076c64ef3691f7acbd3b5e2119037523351ec4b8ed4fffe8` | 0 |
| protocol/consensus.go | 12542 | `66a6c27e865757012102f6ed64919512c7727449468ff50e28e362b0ac2a556b` | 0 |
| protocol/hash.go | 3505 | `66729f84386e0ffbe4ef00c341fe90dc7b7ee340b70141c759431806252f016b` | 0 |
| protocol/msgp_gen.go | 14310 | `39c31b9464fd1dd6d9e3c8c3844136b752e85e83070a097e5e37aca2463742a7` | 0 |
| protocol/networks.go | 877 | `89cd79e0bcc1cc7492176086440555a46e002887f4cd7e1d27141851ba7becba` | 0 |
| protocol/sig_scheme.go | 1845 | `efc04f874f9bfba80196e478766313ba61398423ee0b44b78cef3ed561b147e8` | 0 |
| protocol/stateproof.go | 1854 | `7d096608f6b87dcd8ea9690942cad499c4dac01965ac668c72c503f5c15fc4dd` | 0 |
| protocol/tags.go | 6867 | `e1a0e7feae5a4d0c0f05db8f5e2390a3a301aa61715572cad5fc2348a5088219` | 0 |
| protocol/transcode/core.go | 7358 | `93b7cca938ec1c59535b540c6f2152895ece174654f48587dc228af482dcbd51` | 0 |
| protocol/txntype.go | 2020 | `29a4977a36212d706601b280bb8a97b53513024f58251d94509b6e4ee08cf714` | 0 |
| rpcs/blockService.go | 17890 | `7e71456ff7aafdf497cd8ad40a40cec95d9fa35d4a8ea3f8a12e552c211035de` | 0 |
| rpcs/healthService.go | 1353 | `ec0480b00e43b4ee5834ff2f88fa350ff0df4e60aa5ae546f3a1d9af316fa4b7` | 0 |
| rpcs/httpTxSync.go | 7101 | `e2bf4a741706fc779b028e00c5fc0610fa54c404b4a8ebdeae1e4061213aea82` | 0 |
| rpcs/ledgerService.go | 9887 | `9dad4cafcd3af53e01ac92aad001da633cf8c2a4e96f92a331560f4460e3be55` | 0 |
| rpcs/msgp_gen.go | 8351 | `ac35fafb215558d2180b2f3dca79cab0d38c713d32868ab8e999c757d01458a6` | 0 |
| rpcs/registrar.go | 1342 | `6dbb70a88fd31352f645fb5178e3f52a755a029e2ecde3f9afe162df3fcd167c` | 0 |
| rpcs/txService.go | 7496 | `9b05f4cca2db049d44aef49843614e0c7b72e8afcbd4468fd5d5b6c97e5de462` | 0 |
| rpcs/txSyncer.go | 5543 | `a5ec8acc17282f2aa97dbfefed33dc3234a3e32e4b692089caa9392cb416a2a7` | 0 |
| scripts/buildnumber.py | 424 | `de7237a7e28d63f6117ecc142f9eedab8838b4aa5858fb0afedd3df81ca4647f` | 0 |
| scripts/export_sdk_types.py | 13092 | `c3062e3066781aad90357a7fa7012e5c9d3c9035b31477de7e69718babb27ce1` | 0 |
| scripts/get_current_installers.py | 1428 | `727f046da4a063946d8ad683ea8fec43d53170d6eb71a8ec8ee814795fc41402` | 0 |
| scripts/httpd.py | 597 | `0d17e1a7ec6a9e2da71843d3422961c37a12fcf533785c333f9133898f04b6d8` | 0 |
| scripts/release/README.md | 9195 | `5f1af25056003ae5886e44848ff963f7ecfaf537a6899f589fac6fa0a54abf9b` | 0 |
| scripts/release/archive/get_latest_go.py | 3593 | `72002e8ef41c865eaf43ce92795fa1bc50e73c47e1cf9b6ec4ecc7a38f7a28b3` | 0 |
| scripts/release/mule/deploy/releases_page/generate_releases_page.py | 10393 | `52c050f27c07d67e6ca2fb180cfc902df2a4b07baa7c9f60dfe1cc0761d1f5f2` | 0 |
| scripts/retrieve_logs_from_testnet_s3_today.py | 565 | `d37e41b68a6ac7b64e66badfc32771426b861b04e4fd3774db4780c63e16495d` | 0 |
| shared/algoh/config.go | 2696 | `f3b16046f1e7f70e3a46e4618b3e126b1b79b0b1e9dc9696e0aaa004223eb6bd` | 0 |
| shared/pingpong/accounts.go | 28123 | `a2fc6a5cd57051c57236b3074a573e2048ce17478b1df0f844b97161a33e2c37` | 0 |
| shared/pingpong/config.go | 6156 | `506e6b1fede2b54067ee5c1047b0ce3303d926296f8105b4edeef7a804483e41` | 0 |
| shared/pingpong/pingpong.go | 42167 | `447cfaa1338106bc8e91637d4d3233f6af6d614f2224b7e56e51e02f965995bf` | 0 |
| stateproof/abstractions.go | 2542 | `64c12323946b7f9e60fa74906863993cf11a3d900cd4ae7f25d4d92c8d50543d` | 0 |
| stateproof/builder.go | 25336 | `0e04b6edefdd8039be686be3fad869eba2e1f3ccf1d47a9c9bb096b1e6cfe86b` | 0 |
| stateproof/db.go | 7771 | `79b0267bfaaddcd4aa637374462a0931f784719fbe80ed9c05fe22f1a7dff422` | 0 |
| stateproof/msgp_gen.go | 9749 | `616fbb769fff359457d5b758e19da9b039e1c23860d005869650f26ee514981a` | 0 |
| stateproof/recovery.go | 1783 | `63b71ded3d38cfb7e6e605ff4a75bd1e0607457a13b4937ae75a4d896ae5ebb4` | 0 |
| stateproof/signer.go | 5670 | `6778078d1cbf29be6ef19f58221a751c7c4c0d2e4e2b9d76a851521623840918` | 0 |
| stateproof/stateproofMessageGenerator.go | 5782 | `92b1f47f0402b8e744b7727b8c582a7f46b1c251e19d7f01e65ca6e3931d8bfe` | 0 |
| stateproof/verify/stateproof.go | 7865 | `408a74a4a97d96306d71d19e65b397a5c1b33c9157d63730a2e5b1d68de6cb2b` | 0 |
| stateproof/worker.go | 5228 | `e31422d23ef184ebcaf0231097a55dd969595d453a988ccff3f32f6f8ba2f734` | 0 |
| tools/block-generator/core/commands.go | 1284 | `246fbf4b38994ce33f50cd5f2b39094b2aab927bbaba664a544620c49670869d` | 0 |
| tools/block-generator/generator/config.go | 11351 | `1dee5de36a9bb26ff1a4ef526ab3356cf32279aad345efff69bba7bc2869cd56` | 0 |
| tools/block-generator/generator/daemon.go | 1708 | `990f18ebca827679610a9036bf3fee28bd347f92791de96755726fcabb1b51b5` | 0 |
| tools/block-generator/generator/generate.go | 28528 | `f1e742d9153f1cd81d4b68541f63ac51502b6950233e28a79550a4c0719d4e82` | 0 |
| tools/block-generator/generator/generate_apps.go | 9914 | `ef93263265718d37a49711ac08994610becd611af778459d17ead7818381b4cb` | 0 |
| tools/block-generator/generator/generator_ledger.go | 11868 | `bd7c24c96e477554715b935479c5d6228cc9b3ec992a0de8e73f8cdce5b6f2ee` | 0 |
| tools/block-generator/generator/generator_types.go | 5528 | `6801a7b60ef88f58ade9fc43fb58d6c872b4801d11c25cb930f79f3ec2184a9d` | 0 |
| tools/block-generator/generator/make_transactions.go | 7481 | `a3527eb59bc4ee0a4ff0195f7657048e39631dcf0a75df3e4c863dd83eb21ed1` | 0 |
| tools/block-generator/generator/server.go | 5736 | `dea87faab336bbe77c2a574643cc2a23f286bbfb8501bf8b82266b739923b0c1` | 0 |
| tools/block-generator/generator/utils.go | 2590 | `b169cf0e6f1fae593be5ff6e04a495d5aff43a9ba2b9c1ab8ad266fe6fc1c4ac` | 0 |
| tools/block-generator/go.mod | 8609 | `1400e07bdb3bac6f73f41b41e33c9593068e3a95cc4406125fe118d15ceb0fb4` | 0 |
| tools/block-generator/main.go | 927 | `6adea2980ee7d698f690c68d2b8cf35296d6b08048dad27a2f026b986cd97310` | 0 |
| tools/block-generator/requirements.txt | 15 | `3f19161bb168b095466cd45f787e64b3318f69f7a29f01a178146f99250ea422` | 0 |
| tools/block-generator/runner/metrics_collector.go | 2974 | `fe1f4caf82f99665412bf8537ad00554c2b3a09a9a8fdc246ba52866590f35fe` | 0 |
| tools/block-generator/runner/run.go | 17975 | `b50f7b0458542cfbb7f261c04ecc803b609f1583178a904f8dcd2f052777565e` | 0 |
| tools/block-generator/runner/runner.go | 4392 | `520c37ce88775ba0c7110d7a2a65e512e13f156d6539b2f9ea9cf3d5ab8a6282` | 0 |
| tools/block-generator/scripts/print_tps.py | 1907 | `8846c3d6429efd614ef5331fbb8bbd09274cdc8c947e0165d96403d316d7ce52` | 0 |
| tools/block-generator/util/util.go | 2621 | `44e90a3d3ef1fa456302b87fb968ebf56aca89baed6cde77165a7cf2d7422604` | 0 |
| tools/boxkey/convertBoxKey.go | 1453 | `1d905a803699bced29a0ccbb97f7587c307b513718317a146b1a53d238a401df` | 0 |
| tools/debug/algodump/compress.go | 20099 | `a55db36936f893333b9636d1bb7f4058935661b01643fb47f5022c33e8051038` | 0 |
| tools/debug/algodump/go.mod | 7635 | `9a2c47543d3c5996eb7013e4276ac1f0fd67ed5631e15a901c4d6cad84c6d10f` | 0 |
| tools/debug/algodump/main.go | 11897 | `489dc01707bc6bc8f220894356bc04ab4a04c35cac9c6f6134df126d32f2102d` | 0 |
| tools/debug/carpenter/main.go | 11307 | `620dbe0e9f323da6bcf480cec7e4024d776592db34bec7038f4ca666ad1e4f6b` | 0 |
| tools/debug/chopper/main.go | 6597 | `6aada1af2b0d06c259fc2ee115e6fe0e0432e1c28e3669d33c8c3a0e7273e945` | 0 |
| tools/debug/coroner/main.go | 3590 | `a445a34ad83094da101f52c9b0896df8499ff51d97faa968b6bc98cb35d38f54` | 0 |
| tools/debug/determaccount/main.go | 1409 | `70cde8205fb49039f8f398eda22db00e85f3c367378e74e3d1fcdce6035f2562` | 0 |
| tools/debug/dumpblocks/main.go | 3122 | `070efd5f80615d24dc1f1f1a908a98e4cf95a45e893f4deaf5bb80748d134480` | 0 |
| tools/debug/logfilter/main.go | 4385 | `39cbeddb1e32ea7fe6c73ace965299b789958df0b5c1000e5ba21cd4d001f864` | 0 |
| tools/debug/net.py | 1346 | `a57c98997a99fdcee74a556f928550d56fde27692df33e21938adf4c57c0228d` | 0 |
| tools/debug/showchains.py | 2190 | `96fbc87e7b26676427e17771eef643378295c2af244fca5536682375743100af` | 0 |
| tools/debug/transplanter/main.go | 14095 | `13ba896d8fdd6a85a3f38436e4f1d68dec0d73bb82fc8853eeb7df5b26ebd129` | 0 |
| tools/misc/convertAddress.go | 1491 | `e577605861a1f0c5ee2be26bc299ff7c68d635eba8cf8f7280769e6c7c49270c` | 0 |
| tools/network/bootstrap.go | 4465 | `2f8fa849de61ee94e7e9ab0f614228ede8c83bba52abf1fe114a3d4a6c7e69a7` | 0 |
| tools/network/cloudflare/cloudflare.go | 13556 | `aad43e6257c289a23667eddb60c1c190cb4a0fb3490d35fcdb39839d96c20314` | 0 |
| tools/network/cloudflare/createRecord.go | 6045 | `4e9b512d5fbcf8912aa73623e591e2ccdabcb40293305a887793ff61935a740b` | 0 |
| tools/network/cloudflare/deleteRecord.go | 2331 | `b096e3c53e68240a8a744ebe2841f5f953104d105f6a586440a854870f81c440` | 0 |
| tools/network/cloudflare/helpers.go | 976 | `a476806a188c34bad12bd970352f8a0ab6b4dc5f31b678b8d05541ccf52e50ad` | 0 |
| tools/network/cloudflare/listRecords.go | 4202 | `f44ceaca848edadbd6ea79031966163490911db67cc80dcd71786074fcad17ec` | 0 |
| tools/network/cloudflare/updateRecord.go | 3153 | `64e06a44383129f363025561d044b8472426244ce48dbc0a38e94c216e911cb6` | 0 |
| tools/network/cloudflare/zones.go | 3302 | `c6b06b562d21e395c2a9e1b132305a9a22f89f177b5000a316f75d94174ec9f6` | 0 |
| tools/network/dnssec/anchor.go | 2434 | `b8a2ceb4f660d8acfe9c672c38c613ca7742b7cae2ea463c373fb84f19debbcd` | 0 |
| tools/network/dnssec/client.go | 8652 | `259c8afba83a29ab3a66303877f93bc12d00beceffda21f7caefc33d8c518f3d` | 0 |
| tools/network/dnssec/config.go | 1824 | `7c19d0b4b560f850297caef0d3504eb656198df8beafa18b531a72aebfe92324` | 0 |
| tools/network/dnssec/config_unix.go | 1809 | `a307b94662a77f0d17cdbc2117171217be964640c44809c5d81e7d23621a68f9` | 0 |
| tools/network/dnssec/config_windows.go | 4364 | `12b03fd67bb135952fd6c6aace5689f83f9b21fd87aa4a2058ed623c7c63db38` | 0 |
| tools/network/dnssec/dialer.go | 2950 | `5757bb2f770ebcc2fdd84732cdce3776f51f47ed6f4679d437a2f9ed097dd7d5` | 0 |
| tools/network/dnssec/relay-check/main.go | 2233 | `41bef0a0bcba9e62951b7bcc8b65c714fdb497cc3ba5b0f998e7cbda125aafa3` | 0 |
| tools/network/dnssec/resolver.go | 9633 | `a0463d1bc5d791f9c9bb31e60b6e7190792757d34ff5795d0c38cc84f888aeee` | 0 |
| tools/network/dnssec/sort.go | 2237 | `1cd87cf39db5879df63f8825bd5aded4ffd469d6353379314267fef7ba9b9386` | 0 |
| tools/network/dnssec/testHarness.go | 15528 | `05775c6dd3d524fce09560fb888696597b0cca3d8a1a279934adff74277339da` | 0 |
| tools/network/dnssec/trustchain.go | 7176 | `ddce20c50c2c3596c3b75d14e63164bf1bd2d5efb88ca11163ca0c50c8146f3b` | 0 |
| tools/network/dnssec/trustedzone.go | 7387 | `1e86b5916a69721cf48db864fd761d7b4ea5dac418d355204bd0d6b9b8324270` | 0 |
| tools/network/dnssec/util.go | 1590 | `c59972a9b1ca2560b5b57e9f2a29e3cafa9ff4ab17b416d52fb5ba1d3ad13da3` | 0 |
| tools/network/externalIP.go | 1242 | `3a00a3ee3df19541e104787db4eeae253987fd78570c4b1c340502bc3d5608f8` | 0 |
| tools/network/resolveController.go | 4123 | `7f8556b5e42716906e9d22fd3db62dc497a8cf0a07111001e9689ee7ae307148` | 0 |
| tools/network/resolver.go | 5152 | `dbeff1b232653adf8411068f3418c32f0cc53aba209ab17d32ed42e7e491aaec` | 0 |
| tools/network/telemetryURIUpdateService.go | 5116 | `27ac4850e3958dad464cd977272b7cdde697b0e84b0630b763bb265f6afd2f0b` | 0 |
| tools/teal/algotmpl/extract.go | 2518 | `04256c2d0a5b2e59c567c1ac0411680485bba621ef8cf7b5df27cd7649834423` | 0 |
| tools/teal/algotmpl/main.go | 4618 | `093c95fd89b0822b6eb2d767d497b6b895d1b6b0ea56e114fcb75d37960b037b` | 0 |
| tools/teal/dkey/dsign/main.go | 3046 | `dcb2cbee1b3603afff48fadd21d337cbd728bff7d09df6723f544522f1954468` | 0 |
| tools/x-repo-types/go.mod | 507 | `822ef0a0e4b3a9eeef4b68c9ba5dc4cd600041612f5747733f1a7de7b1bae739` | 0 |
| tools/x-repo-types/typeAnalyzer/main.go | 2575 | `44bb0195086d161ba82720aafedc30f7094409ae17db4ef890ba7004dfb0b61e` | 0 |
| tools/x-repo-types/typeAnalyzer/typeAnalyzer.go | 19590 | `c318336452f8375b9a5567e5aabcdd423ff4cbf9c845b9365f32954b6781a95b` | 0 |
| tools/x-repo-types/typeAnalyzer/unreleased.go | 1811 | `c22c20024074b6e8b5066a28c716984fa8dab2cb94f01a8dba722d5d5ead1ef1` | 0 |
| tools/x-repo-types/xrt.go | 8809 | `a600f03f2e27307c86ee229037c3b053a300d5db95d888220dac817baf06885f` | 0 |
| util/bloom/bloom.go | 5140 | `3fa383ae79a98a9165eb1bb6439498048306fa681d9fd07913622ba741b15d52` | 0 |
| util/cmdUtils.go | 1455 | `cc30a1549d3041e5dd7925706798c39c847485703a70b3b266cfc71486c1b230` | 0 |
| util/codecs/json.go | 5558 | `7eece80707570537173fe1a7da6b0b5db1964d28d50dc6ac4c49a91284b4e849` | 0 |
| util/condvar/timedwait.go | 1736 | `8ff826900819a8f0ea4cf8f7a251f83268b4d36ab92a37254211186c75c5dbe4` | 0 |
| util/db/dbpair.go | 1747 | `75dd89978dc5ff5ef145c1d33754c7b778b08bec468e4a784446a35365b706c1` | 0 |
| util/db/dbutil.go | 19503 | `5822a853a2f1e1d35bcda02f739f9b2715121c1f810e2086bcac3da922ea4c16` | 0 |
| util/db/fullfsync_darwin.go | 933 | `714b989a36ff209b4de893bac85cd1c3ad22ba56303976411f85e1a00856c568` | 0 |
| util/db/initialize.go | 4395 | `0118f13764762f3c8f1f442d0c0f32291ea3719579f7bce8161bf016c98a7489` | 0 |
| util/db/interfaces.go | 1883 | `ad1e7fdd7e70fa479a655ebd05e7a840a1e7f60f0e95cf6e969e7777cf3b5cb9` | 0 |
| util/db/versioning.go | 2118 | `3a1134be0676433f63cbe72136f40996b33d44be0d80566db4f472af87295d3e` | 0 |
| util/db/walerase.go | 12681 | `37d7a830528d347702c710f9736e9d0175bd14cf5e47991bc5fd52c466d36916` | 0 |
| util/execpool/backlog.go | 4054 | `292ce615d29b3883837dddde62455235de7f55c64a92b120508877dda09a5bf0` | 0 |
| util/execpool/pool.go | 4542 | `8772be6302e54256294d8070a3c59a8bf04f735f7b2d3bdb718b5fa056389502` | 0 |
| util/execpool/stream.go | 7637 | `41639c5810b1dc7a9a83bfb7cab88ed4f9aa1faeecdff8bcf64906bfa9ad274c` | 0 |
| util/fn.go | 1710 | `69f589c1c5774002b606c228e18599427359c36871f27ae8642a3f4d714e4ed5` | 0 |
| util/io.go | 6811 | `6baba77d9f1987ef7d548706f65f9b1f1aa208d4902bf188ed0ac4d89e0ba83b` | 0 |
| util/list.go | 3937 | `71e208a9b7e5b75dfa590ab1023c0c66df6f8a485a6584c255d797f88f560d58` | 0 |
| util/metrics/couge.go | 5521 | `49489bfd8e53c0cd097c19d5a8669206273211233bd47c14a4a6331ac5d896c8` | 0 |
| util/metrics/counter.go | 3604 | `e0447ebf6ee42f2415c65ab85712dc642feb5cec05b389bd858de44cae534657` | 0 |
| util/metrics/gauge.go | 2856 | `846abbec6d4feac5e450db92591aa1f901e2482c186fe74261972f04897db646` | 0 |
| util/metrics/metrics.go | 17921 | `47365b9b69f5d3bcd623cb01539a62ab324a2c6b421129363b0d69291a5ecd61` | 0 |
| util/metrics/netdev_common.go | 2699 | `faa1fa4d55d6b25c6a3cd669abc022a13f5b7dafa80fa7fd979003da5a3bd6db` | 0 |
| util/metrics/netdev_darwin.go | 2708 | `130b36702208b2ed0b5ba4b5e5830b8c9061469efe75326729d5a75aa37b3799` | 0 |
| util/metrics/netdev_linux.go | 1818 | `d0fc59f4774eb024237ae61184ab6e40fef4ff4698c32c89bd9e502f0d81928e` | 0 |
| util/metrics/netdev_noop.go | 923 | `57bab95d909738176d59f5acaa2cc90ccd37f5a830e0d6b2499fe877c1363f72` | 0 |
| util/metrics/otel.go | 2725 | `53bbf3a02c397cc94118c8b4f9fc0f4b8de3ea4d51b17e507cc87502dc9904c1` | 0 |
| util/metrics/prometheus.go | 7781 | `ba938d072654fdedc9249adfeb7f0557939cd7f02b88da3569a21022ee7a8431` | 0 |
| util/metrics/registry.go | 2416 | `25b3d2a055afe96557e6b6ec015aa950437759d62bd82b2b67e90d6c37cac825` | 0 |
| util/metrics/registryCommon.go | 2020 | `ac6aa2851a9f5dc1b6e67b6ce5c80e73aed0e234d7d2dee49fb5364016624540` | 0 |
| util/metrics/reporter.go | 9096 | `ec52524995637183fc7fc114e78849b59b40d34d24e5cde0a2a52440523a1adf` | 0 |
| util/metrics/runtime.go | 4230 | `2ad8b21ef456188c40c005012781658cfc3f9be5903ba84157ca2843a89dc094` | 0 |
| util/metrics/service.go | 2788 | `ae7b74c6e6dc15d0a67f5d1d6e32cc5f938ff3ae36c26a8efe0c3f92408081e1` | 0 |
| util/metrics/serviceCommon.go | 1710 | `3724a2fd525021650ce6fda7357414e4c6eaa19327bdeb0ad694c6b05d664bbb` | 0 |
| util/metrics/tagcounter.go | 5042 | `64f9a50dfff08f43205258bda05fed397afb4e1de2b6577b4e94c74ef6fca7b9` | 0 |
| util/pagedqueue.go | 5490 | `d2f85b761670c71cfc46bd8e4a99c57d372fcd268d55c183a098c916bd20eb41` | 0 |
| util/process.go | 2161 | `40c13d476bc3abf6e04f548fc46d393b6f4e3d37487bf3e9dd510c3867d19b6e` | 0 |
| util/process_common.go | 1084 | `b21684a4cebd684cbd1c4be323b2db18a2bc02a5013ba77ae42bee9045d5d1c8` | 0 |
| util/process_windows.go | 4357 | `a8a4c2e3eaabc9f81f40f5cc12c20259aec4398226d58999b00a0490992e647d` | 0 |
| util/rateLimit.go | 19424 | `706c77e2e00f4c491d95680763bfc2d7b3b7f4944adce8bfa753d309193715a0` | 0 |
| util/s3/fileIterator.go | 2081 | `fdaed3ba359b46eedd4455715d6094464a3a161bb5da2aa258ca91dd021fb630` | 0 |
| util/s3/s3Helper.go | 8853 | `1f37f3c6b35d031b882a8d68a00bbbef4c9265c052572b07b8f35c1eba655b50` | 0 |
| util/set.go | 2545 | `13fb7b9ba1fda566a2bf59e7d33da514dd9c5a2f6e10bc5180e260b03adcdd70` | 0 |
| util/sleep.go | 1086 | `4fe80adb166bac76ef82c62a60a3d8f74f22e5bdc9072f0bd96fa16fb68c0bc7` | 0 |
| util/sleep_linux.go | 1571 | `136d55b50b6c46da6611b6c950221b0c65e518872a52b4a7e9988698ef9c3eb8` | 0 |
| util/sleep_linux_32.go | 1143 | `55d386bfba8ab87d3bd4f6f72a337e4c12c9b82163fab01cd01cf12bbbd6b9b4` | 0 |
| util/sleep_linux_64.go | 1130 | `5926b38447616bfe0fc74473b27b6eb508f9a4f357b126cac4607b84d04aae2b` | 0 |
| util/tcpinfo.go | 2998 | `b2a1b0225e09b53d3ac372dfceb301aa78c22ca4114e3d46db2cdc7435a84010` | 0 |
| util/tcpinfo_darwin.go | 1581 | `bae50ca51406cdca1c96df4ea4195f3cda1948a01afe60c30c8b7909f5422714` | 0 |
| util/tcpinfo_linux.go | 3266 | `73c173c1ce50295255ac71bd0a69085fce2f97c099a48b68bf1734622c4b50d4` | 0 |
| util/tcpinfo_noop.go | 918 | `4ddb131291afc792542bf07d575c2fa04cd09165bc2c6c5bc90de84c7a0ea478` | 0 |
| util/timers/frozen.go | 1907 | `5fb9720c2b415a23a5018f85d4ba54998132e4fcdacc83300c0069e74a894e4e` | 0 |
| util/timers/interface.go | 2042 | `7529bc2085c9c9996da0501373de42183b027dd50867f891d79608ab20ffe8e2` | 0 |
| util/timers/monotonic.go | 3068 | `4251c1067bfaa7e2e97bb15d5406e10be038026c4719f3a52f65ed09fcc7a241` | 0 |
| util/tokens/tokens.go | 3904 | `9e75e8c6fe7be57d20252f6dcf081b82c421df2484e3d6be163fd3e02c4e3fc9` | 0 |
| util/util.go | 2747 | `758ab276b25ec2c25e004bb0a916f7a9589ea52d2a3ba8d487b94565006fe8df` | 0 |
| util/util_darwin.go | 1009 | `2efc9b308fb4999f0b15880ca9aa6e86ecf5b218c6375d872dd081ca453d989a` | 0 |
| util/util_linux.go | 1011 | `bab4a55bfcc9ab964c1b4c13f6b1033b18e11776607db7ff7cab93e16adbe7c1` | 0 |
| util/util_windows.go | 3174 | `76530e44cdab4fe8913c1055bb9e183ecf237bff8d3acbc6241b5efb7b48978b` | 0 |
| util/uuid/uuid.go | 1444 | `74276424b95b251d7e41ef30a3d995421c0988175acb0fd489277bb659a20e93` | 0 |
| util/watchdogStreamReader.go | 7206 | `e495e95276c1659a13493c5e54eec389fbfb86c31f345e1db41d105916d58535` | 0 |
