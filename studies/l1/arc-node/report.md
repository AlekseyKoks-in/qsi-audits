# Security & Post-Quantum Readiness Audit Report

**Project:** arc-node @ 6e764023ee65 · Circle (Arc) — public repository (passive review)
| | |
|---|---|
| Organization | QSI |
| Report date | 2026-11-06 15:31 UTC |
| Report version | 1 |
| Audit run | a58a0714-a9d2-41d4-b96d-7e3809f2d534 (Document audit) |
| Analyzer engine | qsi-engine 1.3.0 |
| Risk profile | Crypto exchange, custodian or wallet |
| Content SHA-256 | `2cb1f259975c8af684ffa81af50b3a9c029ff2d5a6375299ede323d6502412cd` |
| Signature key (Ed25519, SHA-256 fingerprint; the signature is the separate file report.sig.json) | `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e` |
> This report presents automated and documented analysis results for the stated scope. It is not a legal opinion, a certification or an attestation of compliance with any standard.

## 1. Executive summary

- Critical: **0**
- High: **17**
- Medium: **20**
- Low: **31**
- Info: **61**

- Confirmed technical vulnerability: 0
- Known vulnerable component: 45
- Confirmed configuration error: 1
- Potential cryptographic risk: 6
- Long-term post-quantum risk: 4
- Improvement recommendation: 73
- Insufficient data: 0

Mosca's inequality (x + y > z): x = 10, y = 5, z = 8 → migration would finish too late under this scenario. _z is a planning assumption chosen per risk profile, not a prediction. A cryptographically relevant quantum computer is not publicly known to exist today._

**Post-quantum maturity: Level 2 of 4 — post-quantum in use outside the critical paths.** Next step: Extend post-quantum protection to the critical roles that stay classical, starting with what can be recorded today (wrapped keys, channel key exchange).

## 2. Scope and boundaries

Mode: Document audit

Repository: <https://github.com/circlefin/arc-node> @ `6e764023ee6515fe70573e123ed2db912a7207b4` — evidence links open the lines at this commit.

1135 files, 11126358 bytes in total, 78 redaction(s); the per-file SHA-256 list is in appendix C.

## 3. Methodology

| Area | Status | Count | Examples |
|---|---|---|---|
| dependencies | checked | 40 | Cargo.lock: 1276 dependencies parsed (1276 pinned); Cargo.toml: 216 dependencies parsed (3 pinned); crates/consensus-db/Cargo.toml: 20 dependencies parsed (0 pinned) |
| source_code | checked | 498 | assets/devnet/genesis.config.ts: 138 lines scanned with 16 rule patterns and 267 registry patterns; assets/localdev/genesis.config.ts: 182 lines scanned with 16 rule patterns and 267 registry patterns; assets/mainnet/genesis.config.ts: 177 lines scanned with 16 rule patterns and 267 registry patterns |
| secrets | checked | 66 | assets/mainnet/genesis.config.ts: 11 redacted value(s) not reported (comments, test modules, fixture declarations, placeholders, values the source annotates as published, or hex values not bound to a secret name); crates/eth-engine/src/abi_utils.rs: value(s) at line(s) 337 (test_corrupted_public_key_leaves_set_empty_and_errors) are declared inside a fixture and treated as test data, although the file itself is not test code; crates/eth-engine/src/abi_utils.rs: 1 redacted value(s) not reported (comments, test modules, fixture declarations, placeholders, values the source annotates as published, or hex values not bound to a secret name) |
| smart_contracts | checked | 590 | contracts/scripts/Addresses.sol: built-in Solidity pattern checks; contracts/scripts/ArtifactHelper.s.sol: built-in Solidity pattern checks; contracts/scripts/DenylistManagement.s.sol: built-in Solidity pattern checks |
| slither | not checked | 590 | slither is not installed on the server (pip install slither-analyzer + solc) |
| entropy | checked | 1 | random-number generation: 498 code files read with 0 macro definitions from the tree; 0 ineffective guard(s), 0 weak random-bytes provider(s), 0 weak key-generation site(s) |
| osv_advisories | not checked | 1 | 125 package(s) are built from git repositories (forks or unreleased code), so registry advisories were not looked up for them: arc-malachitebft-app, arc-malachitebft-app-channel, arc-malachitebft-codec, arc-malachitebft-config, arc-malachitebft-core-consensus, arc-malachitebft-core-driver, arc-malachitebft-core-state-machine, arc-malachitebft-core-types, arc-malachitebft-core-votekeeper, arc-malachitebft-discovery, arc-malachitebft-engine, arc-malachitebft-engine-byzantine … |
| osv_advisories | checked | 1 | 1000 pinned packages queried at OSV.dev; 33 affected (1 of them only in development or build dependencies) |

_Long lists are grouped here; the full per-file list is in the JSON report, signed with the same key._

## 4. Assets examined and not examined

- slither — not checked: 590 (examples: slither is not installed on the server (pip install slither-analyzer + solc))
- osv_advisories — not checked: 1 (examples: 125 package(s) are built from git repositories (forks or unreleased code), so registry advisories were not looked up for them: arc-malachitebft-app, arc-malachitebft-app-channel, arc-malachitebft-codec, arc-malachitebft-config, arc-malachitebft-core-consensus, arc-malachitebft-core-driver, arc-malachitebft-core-state-machine, arc-malachitebft-core-types, arc-malachitebft-core-votekeeper, arc-malachitebft-discovery, arc-malachitebft-engine, arc-malachitebft-engine-byzantine …)

## 5. Architecture overview

Static review of the source tree arc-node at 6e764023ee6515fe70573e123ed2db912a7207b4. 1135 files analysed; of 3265 files, 1461 are test, fuzzing, benchmark or example code and were left out, 669 are not read by any analyzer, 0 exceed the per-file limit and 0 did not fit the total limit. Files no analyzer reads include: .cargo/audit.toml, .config/nextest.toml, .dockerignore, .foundry-version, .github/CODEOWNERS. 685 files in build-output or dependency-cache directories (.git, .hg, .venv, __pycache__, build, dist, node_modules, target, vendor, venv) were not read. 750 files come from directories a .gitmodules pins and are read as shipped source rather than skipped as a dependency cache: contracts/lib/openzeppelin-contracts-upgradeable (459), contracts/lib/openzeppelin-contracts (291). No requests were sent to the owner's systems.

## 6. Overall security posture

- Indicative posture index: **0** / 100 — _Derived from findings in scope (confirmed and potential issues weighted by severity). Indicative only; not comparable across differently scoped audits._
- Quantum-vulnerable share of inventory: 7.2%

## 7. Detailed findings

### QSI-2026-19526 — rmcp 1.4.0 is affected by GHSA-33f5-2c5q-wgwj (CVE-2026-63127)

- Severity: **High** · Classification: Known vulnerable component · Confidence: Medium
- Affected asset: `dependency:crates.io/rmcp@1.4.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 50.2 / 100
- CVSS v3.1: 8.2 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:N`)

OSV.dev reports GHSA-33f5-2c5q-wgwj (CVE-2026-63127) for crates.io package rmcp at version 1.4.0: RMCP: Missing Resource Field Validation in OAuth Protected Resource Metadata Discovery. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-33f5-2c5q-wgwj
```

**Evidence.**

_tool_output · [OSV.dev GHSA-33f5-2c5q-wgwj](https://osv.dev/vulnerability/GHSA-33f5-2c5q-wgwj) · manifest · SHA-256 c1ab8acdb6fd448b36c50ff1155c2047fe250e3113423960512fb2d520af324a_

```
{"id": "GHSA-33f5-2c5q-wgwj", "aliases": ["CVE-2026-63127"], "modified": "2026-09-16T22:30:08.107391372Z", "summary": "RMCP: Missing Resource Field Validation in OAuth Protected Resource Metadata Discovery", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:N"}], "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (2.0.0).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-19528 — rmcp 1.4.0 is affected by GHSA-9pj6-vhgr-3mwh (CVE-2026-63128)

- Severity: **High** · Classification: Known vulnerable component · Confidence: Medium
- Affected asset: `dependency:crates.io/rmcp@1.4.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 50.2 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev reports GHSA-9pj6-vhgr-3mwh (CVE-2026-63128) for crates.io package rmcp at version 1.4.0: RMCP: Unauthenticated permanent session-table leak in rmcp Streamable HTTP server transport leads to remote denial-of-service. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-9pj6-vhgr-3mwh
```

**Evidence.**

_tool_output · [OSV.dev GHSA-9pj6-vhgr-3mwh](https://osv.dev/vulnerability/GHSA-9pj6-vhgr-3mwh) · manifest · SHA-256 8250eff4b4b607285a1b9fee7fddb2ffab54a7b41cbdff7fcb55c67bc51302ef_

```
{"id": "GHSA-9pj6-vhgr-3mwh", "aliases": ["CVE-2026-63128"], "modified": "2026-09-16T22:30:08.343637534Z", "summary": "RMCP: Unauthenticated permanent session-table leak in rmcp Streamable HTTP server transport leads to remote denial-of-service", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (2.0.0).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-19441 — Possible hard-coded secret in contracts/lib/openzeppelin-contracts-upgradeable/contracts/token/ERC6909/extensions/draft-ERC6909TokenSupplyUpgradeable.sol

- Severity: **High** · Classification: Confirmed configuration error · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `file:contracts/lib/openzeppelin-contracts-upgradeable/contracts/token/ERC6909/extensions/draft-ERC6909TokenSupplyUpgradeable.sol`
- Data source: contracts/lib/openzeppelin-contracts-upgradeable/contracts/token/ERC6909/extensions/draft-ERC6909TokenSupplyUpgradeable.sol
- Detection method: Regular-expression matching of language-specific API patterns.
- Analyzer: source_code 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 47.1 / 100
- CVSS v3.1: not applicable

1 secret-like value(s) of type hex_private_key_32b (first at line 21). Values were redacted by QSI.

**Potential impact.** Credentials in source code leak through repositories, builds and logs.

**Reproduction steps.**

```
Open line 21 in the supplied file contracts/lib/openzeppelin-contracts-upgradeable/contracts/token/ERC6909/extensions/draft-ERC6909TokenSupplyUpgradeable.sol and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/contracts/token/ERC6909/extensions/draft-ERC6909TokenSupplyUpgradeable.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/contracts/token/ERC6909/extensions/draft-ERC6909TokenSupplyUpgradeable.sol#L21) · line 21 · SHA-256 cf74f24f02484f76ae662f07905a00e2ce06c4da7fab82259bdd3c0ca92095c5_

```
   21 |     bytes32 private constant ERC6909TokenSupplyStorageLocation = [REDACTED];
```

**Limitations of the check.** Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Move secrets to a secrets manager/environment; rotate the exposed values.

**Retest procedure.** Re-scan the source and review the call sites listed in the evidence.

### QSI-2026-19499 — hickory-proto 0.25.2 is affected by GHSA-3v94-mw7p-v465 (RUSTSEC-2026-0118)

- Severity: **High** · Classification: Known vulnerable component · Confidence: Low
- Affected asset: `dependency:crates.io/hickory-proto@0.25.2`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 37.6 / 100
- CVSS v3.1: not applicable

OSV.dev reports GHSA-3v94-mw7p-v465 (RUSTSEC-2026-0118) for crates.io package hickory-proto at version 0.25.2: hickory-proto: NSEC3 closest-encloser proof validation enters unbounded loop on cross-zone responses. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-3v94-mw7p-v465
```

**Evidence.**

_tool_output · [OSV.dev GHSA-3v94-mw7p-v465](https://osv.dev/vulnerability/GHSA-3v94-mw7p-v465) · manifest · SHA-256 cc87bacaef206929b0a77fd5d147c04acf1d462eb4c797fbe2c86c8000270b12_

```
{"id": "GHSA-3v94-mw7p-v465", "aliases": ["RUSTSEC-2026-0118", "RUSTSEC-2026-0120"], "modified": "2026-09-10T03:50:45.304576252Z", "summary": "hickory-proto: NSEC3 closest-encloser proof validation enters unbounded loop on cross-zone responses", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (0.26.0-beta.1).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-19501 — hickory-resolver 0.25.2 is affected by GHSA-5j98-2g5x-46v6 (CVE-2026-93657)

- Severity: **High** · Classification: Known vulnerable component · Confidence: Low
- Affected asset: `dependency:crates.io/hickory-resolver@0.25.2`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 37.6 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N`)

OSV.dev reports GHSA-5j98-2g5x-46v6 (CVE-2026-93657) for crates.io package hickory-resolver at version 0.25.2: hickory-resolver: Resolver::lookup() and Resolver::lookup_ip() APIs obscure DNSSEC validation failures. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-5j98-2g5x-46v6
```

**Evidence.**

_tool_output · [OSV.dev GHSA-5j98-2g5x-46v6](https://osv.dev/vulnerability/GHSA-5j98-2g5x-46v6) · manifest · SHA-256 79e70d1c34645cde8da40aaafd922976090c6a7bf4412140fb5be85bf172da61_

```
{"id": "GHSA-5j98-2g5x-46v6", "aliases": ["CVE-2026-93657"], "modified": "2026-10-05T23:00:04.250222435Z", "summary": "hickory-resolver: Resolver::lookup() and Resolver::lookup_ip() APIs obscure DNSSEC validation failures", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N"}], "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (0.26.2).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-19505 — libp2p-quic 0.13.0 is affected by GHSA-5hq8-qhww-jm7q (CVE-2026-61544)

- Severity: **High** · Classification: Known vulnerable component · Confidence: Low
- Affected asset: `dependency:crates.io/libp2p-quic@0.13.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 37.6 / 100
- CVSS v3.1: not applicable

OSV.dev reports GHSA-5hq8-qhww-jm7q (CVE-2026-61544) for crates.io package libp2p-quic at version 0.13.0: libp2p-quic: Remote panic via certificate expiry race during QUIC handshake. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-5hq8-qhww-jm7q
```

**Evidence.**

_tool_output · [OSV.dev GHSA-5hq8-qhww-jm7q](https://osv.dev/vulnerability/GHSA-5hq8-qhww-jm7q) · manifest · SHA-256 6fc6dfa16c6ae300993cd42c604eebc708b32d1721334a87dfd3243b1492e36d_

```
{"id": "GHSA-5hq8-qhww-jm7q", "aliases": ["CVE-2026-61544"], "modified": "2026-09-15T20:15:04.814697144Z", "summary": "libp2p-quic: Remote panic via certificate expiry race during QUIC handshake", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (0.13.1).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-19508 — openssl 0.10.75 is affected by GHSA-8c75-8mhr-p7r9 (CVE-2026-41678)

- Severity: **High** · Classification: Known vulnerable component · Confidence: Low
- Affected asset: `dependency:crates.io/openssl@0.10.75`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 37.6 / 100
- CVSS v3.1: not applicable

OSV.dev reports GHSA-8c75-8mhr-p7r9 (CVE-2026-41678) for crates.io package openssl at version 0.10.75: rust-openssl has incorrect bounds assertion in aes key wrap. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-8c75-8mhr-p7r9
```

**Evidence.**

_tool_output · [OSV.dev GHSA-8c75-8mhr-p7r9](https://osv.dev/vulnerability/GHSA-8c75-8mhr-p7r9) · manifest · SHA-256 5512e9d3ae72f6abee111221f876c1b246e312eba6f58614ed6c529c5370e771_

```
{"id": "GHSA-8c75-8mhr-p7r9", "aliases": ["CVE-2026-41678"], "modified": "2026-09-10T03:50:43.807790048Z", "summary": "rust-openssl has incorrect bounds assertion in aes key wrap", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:U"}], "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (0.10.78).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-19509 — openssl 0.10.75 is affected by GHSA-ghm9-cr32-g9qj (CVE-2026-41681)

- Severity: **High** · Classification: Known vulnerable component · Confidence: Low
- Affected asset: `dependency:crates.io/openssl@0.10.75`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 37.6 / 100
- CVSS v3.1: not applicable

OSV.dev reports GHSA-ghm9-cr32-g9qj (CVE-2026-41681) for crates.io package openssl at version 0.10.75: rust-openssl: rustMdCtxRef::digest_final() writes past caller buffer with no length check. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-ghm9-cr32-g9qj
```

**Evidence.**

_tool_output · [OSV.dev GHSA-ghm9-cr32-g9qj](https://osv.dev/vulnerability/GHSA-ghm9-cr32-g9qj) · manifest · SHA-256 3ac28443d0eb144b47d2fac235169496b7bfe29b68e03d39d7ae436a1b524060_

```
{"id": "GHSA-ghm9-cr32-g9qj", "aliases": ["CVE-2026-41681"], "modified": "2026-09-10T03:51:01.732377930Z", "summary": "rust-openssl: rustMdCtxRef::digest_final() writes past caller buffer with no length check", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:U"}], "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (0.10.78).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-19510 — openssl 0.10.75 is affected by GHSA-hppc-g8h3-xhp3 (CVE-2026-41898)

- Severity: **High** · Classification: Known vulnerable component · Confidence: Low
- Affected asset: `dependency:crates.io/openssl@0.10.75`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 37.6 / 100
- CVSS v3.1: not applicable

OSV.dev reports GHSA-hppc-g8h3-xhp3 (CVE-2026-41898) for crates.io package openssl at version 0.10.75: rust-openssl: Unchecked callback length in PSK/cookie trampolines leaks adjacent memory to peer. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-hppc-g8h3-xhp3
```

**Evidence.**

_tool_output · [OSV.dev GHSA-hppc-g8h3-xhp3](https://osv.dev/vulnerability/GHSA-hppc-g8h3-xhp3) · manifest · SHA-256 ecd44622f7c4e92568c2f150d539347b861e949c26b396ede8004f6359338f5d_

```
{"id": "GHSA-hppc-g8h3-xhp3", "aliases": ["CVE-2026-41898"], "modified": "2026-09-10T03:51:02.103657748Z", "summary": "rust-openssl: Unchecked callback length in PSK/cookie trampolines leaks adjacent memory to peer", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:L/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (0.10.78).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-19512 — openssl 0.10.75 is affected by GHSA-pqf5-4pqq-29f5 (CVE-2026-41676)

- Severity: **High** · Classification: Known vulnerable component · Confidence: Low
- Affected asset: `dependency:crates.io/openssl@0.10.75`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 37.6 / 100
- CVSS v3.1: not applicable

OSV.dev reports GHSA-pqf5-4pqq-29f5 (CVE-2026-41676) for crates.io package openssl at version 0.10.75: rust-openssl: Deriver::derive and PkeyCtxRef::derive can overflow short buffers on OpenSSL 1.1.1. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-pqf5-4pqq-29f5
```

**Evidence.**

_tool_output · [OSV.dev GHSA-pqf5-4pqq-29f5](https://osv.dev/vulnerability/GHSA-pqf5-4pqq-29f5) · manifest · SHA-256 eb0d3f491496bc0f79c5140235d200f4b90826abb9f9aa80893e7a07d385bf1b_

```
{"id": "GHSA-pqf5-4pqq-29f5", "aliases": ["CVE-2026-41676"], "modified": "2026-09-10T03:51:02.503624598Z", "summary": "rust-openssl: Deriver::derive and PkeyCtxRef::derive can overflow short buffers on OpenSSL 1.1.1", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:U"}], "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (0.10.78).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-19514 — openssl 0.10.75 is affected by GHSA-xp3w-r5p5-63rr (CVE-2026-42327)

- Severity: **High** · Classification: Known vulnerable component · Confidence: Low
- Affected asset: `dependency:crates.io/openssl@0.10.75`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 37.6 / 100
- CVSS v3.1: not applicable

OSV.dev reports GHSA-xp3w-r5p5-63rr (CVE-2026-42327) for crates.io package openssl at version 0.10.75: rust-openssl has undefined behavior in X509Ref::ocsp_responders for certificates with non-UTF-8 OCSP URLs. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-xp3w-r5p5-63rr
```

**Evidence.**

_tool_output · [OSV.dev GHSA-xp3w-r5p5-63rr](https://osv.dev/vulnerability/GHSA-xp3w-r5p5-63rr) · manifest · SHA-256 44c3a538ee434a99967c48575139883b19bbe2279df4d3903051b5ad46ff99d7_

```
{"id": "GHSA-xp3w-r5p5-63rr", "aliases": ["CVE-2026-42327"], "modified": "2026-09-10T03:51:07.254489393Z", "summary": "rust-openssl has undefined behavior in X509Ref::ocsp_responders for certificates with non-UTF-8 OCSP URLs", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (0.10.79).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-19522 — quinn-proto 0.11.15 is affected by RUSTSEC-2026-0340

- Severity: **High** · Classification: Known vulnerable component · Confidence: Low
- Affected asset: `dependency:crates.io/quinn-proto@0.11.15`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 37.6 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev reports RUSTSEC-2026-0340 for crates.io package quinn-proto at version 0.11.15: Peer minimum ACK delay can panic quinn-proto when ACK_FREQUENCY transmission is enabled. The advisory names no affected functions, so reachability was not determined.

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

### QSI-2026-19523 — quinn-proto 0.11.15 is affected by RUSTSEC-2026-0341

- Severity: **High** · Classification: Known vulnerable component · Confidence: Low
- Affected asset: `dependency:crates.io/quinn-proto@0.11.15`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 37.6 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev reports RUSTSEC-2026-0341 for crates.io package quinn-proto at version 0.11.15: Stream reassembly memory-exhaustion guard in quinn-proto can be bypassed. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0341
```

**Evidence.**

_tool_output · [OSV.dev RUSTSEC-2026-0341](https://osv.dev/vulnerability/RUSTSEC-2026-0341) · manifest · SHA-256 843224ae2e1a0c898b003d66aa1610a8f10928c662ad0f000421250465a638ae_

```
{"id": "RUSTSEC-2026-0341", "aliases": ["GHSA-qfwj-vfxf-92j2"], "modified": "2026-10-12T18:15:01.969505433Z", "summary": "Stream reassembly memory-exhaustion guard in quinn-proto can be bypassed", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (0.11.17).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-19449 — delegatecall usage in contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/account/utils/draft-ERC7579Utils.sol

- Severity: **High** · Classification: Potential cryptographic risk · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `contract:contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/account/utils/draft-ERC7579Utils.sol`
- Data source: contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/account/utils/draft-ERC7579Utils.sol
- Detection method: Solidity source pattern analysis.
- Analyzer: solidity 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 36.5 / 100
- CVSS v3.1: not applicable

delegatecall at line 234. (related: SWC-112)

**Potential impact.** If the target is user-controlled, an attacker can execute arbitrary code in this contract's storage context.

**Reproduction steps.**

```
Open line 234 in the supplied file contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/account/utils/draft-ERC7579Utils.sol and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/account/utils/draft-ERC7579Utils.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/account/utils/draft-ERC7579Utils.sol#L234) · line 234 · SHA-256 42e274c73007a59a42e252b5a5a5cc7573d9d4823b920a60f52ffb2015e1419b_

```
  232 |         bytes calldata data
  233 |     ) private returns (bytes memory) {
  234 |         (bool success, bytes memory returndata) = (target == address(0) ? address(this) : target).delegatecall(data);
  235 |         return _validateExecutionMode(index, execType, success, returndata);
  236 |     }
```

**Limitations of the check.** Lightweight static pattern analysis of Solidity source without compilation or symbolic execution. It does not replace a full smart-contract audit; confirm manually or with dedicated tools (Slither, Foundry tests).

**Recommendation.** Restrict delegatecall targets to trusted, immutable implementations.

**Retest procedure.** Re-run static analysis and add a unit/fuzz test that exercises the pattern.

### QSI-2026-19465 — delegatecall usage in contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/Address.sol

- Severity: **High** · Classification: Potential cryptographic risk · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `contract:contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/Address.sol`
- Data source: contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/Address.sol
- Detection method: Solidity source pattern analysis.
- Analyzer: solidity 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 36.5 / 100
- CVSS v3.1: not applicable

delegatecall at line 97. (related: SWC-112)

**Potential impact.** If the target is user-controlled, an attacker can execute arbitrary code in this contract's storage context.

**Reproduction steps.**

```
Open line 97 in the supplied file contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/Address.sol and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/Address.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/Address.sol#L97) · line 97 · SHA-256 de90734492398d249f990996f44e7767a3e9ae43db2e357697f6ccfc0437f3af_

```
   95 |      */
   96 |     function functionDelegateCall(address target, bytes memory data) internal returns (bytes memory) {
   97 |         (bool success, bytes memory returndata) = target.delegatecall(data);
   98 |         return verifyCallResultFromTarget(target, success, returndata);
   99 |     }
```

**Limitations of the check.** Lightweight static pattern analysis of Solidity source without compilation or symbolic execution. It does not replace a full smart-contract audit; confirm manually or with dedicated tools (Slither, Foundry tests).

**Recommendation.** Restrict delegatecall targets to trusted, immutable implementations.

**Retest procedure.** Re-run static analysis and add a unit/fuzz test that exercises the pattern.

### QSI-2026-19472 — delegatecall usage in contracts/lib/openzeppelin-contracts/contracts/account/utils/draft-ERC7579Utils.sol

- Severity: **High** · Classification: Potential cryptographic risk · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `contract:contracts/lib/openzeppelin-contracts/contracts/account/utils/draft-ERC7579Utils.sol`
- Data source: contracts/lib/openzeppelin-contracts/contracts/account/utils/draft-ERC7579Utils.sol
- Detection method: Solidity source pattern analysis.
- Analyzer: solidity 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 36.5 / 100
- CVSS v3.1: not applicable

delegatecall at line 234. (related: SWC-112)

**Potential impact.** If the target is user-controlled, an attacker can execute arbitrary code in this contract's storage context.

**Reproduction steps.**

```
Open line 234 in the supplied file contracts/lib/openzeppelin-contracts/contracts/account/utils/draft-ERC7579Utils.sol and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [contracts/lib/openzeppelin-contracts/contracts/account/utils/draft-ERC7579Utils.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts/contracts/account/utils/draft-ERC7579Utils.sol#L234) · line 234 · SHA-256 42e274c73007a59a42e252b5a5a5cc7573d9d4823b920a60f52ffb2015e1419b_

```
  232 |         bytes calldata data
  233 |     ) private returns (bytes memory) {
  234 |         (bool success, bytes memory returndata) = (target == address(0) ? address(this) : target).delegatecall(data);
  235 |         return _validateExecutionMode(index, execType, success, returndata);
  236 |     }
```

**Limitations of the check.** Lightweight static pattern analysis of Solidity source without compilation or symbolic execution. It does not replace a full smart-contract audit; confirm manually or with dedicated tools (Slither, Foundry tests).

**Recommendation.** Restrict delegatecall targets to trusted, immutable implementations.

**Retest procedure.** Re-run static analysis and add a unit/fuzz test that exercises the pattern.

### QSI-2026-19484 — delegatecall usage in contracts/lib/openzeppelin-contracts/contracts/utils/Address.sol

- Severity: **High** · Classification: Potential cryptographic risk · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `contract:contracts/lib/openzeppelin-contracts/contracts/utils/Address.sol`
- Data source: contracts/lib/openzeppelin-contracts/contracts/utils/Address.sol
- Detection method: Solidity source pattern analysis.
- Analyzer: solidity 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 36.5 / 100
- CVSS v3.1: not applicable

delegatecall at line 97. (related: SWC-112)

**Potential impact.** If the target is user-controlled, an attacker can execute arbitrary code in this contract's storage context.

**Reproduction steps.**

```
Open line 97 in the supplied file contracts/lib/openzeppelin-contracts/contracts/utils/Address.sol and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [contracts/lib/openzeppelin-contracts/contracts/utils/Address.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts/contracts/utils/Address.sol#L97) · line 97 · SHA-256 de90734492398d249f990996f44e7767a3e9ae43db2e357697f6ccfc0437f3af_

```
   95 |      */
   96 |     function functionDelegateCall(address target, bytes memory data) internal returns (bytes memory) {
   97 |         (bool success, bytes memory returndata) = target.delegatecall(data);
   98 |         return verifyCallResultFromTarget(target, success, returndata);
   99 |     }
```

**Limitations of the check.** Lightweight static pattern analysis of Solidity source without compilation or symbolic execution. It does not replace a full smart-contract audit; confirm manually or with dedicated tools (Slither, Foundry tests).

**Recommendation.** Restrict delegatecall targets to trusted, immutable implementations.

**Retest procedure.** Re-run static analysis and add a unit/fuzz test that exercises the pattern.

### QSI-2026-19504 — jsonwebtoken 9.3.1 is affected by GHSA-h395-gr6q-cpjc (CVE-2026-25537)

- Severity: **Medium** · Classification: Known vulnerable component · Confidence: Medium
- Affected asset: `dependency:crates.io/jsonwebtoken@9.3.1`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 44.2 / 100
- CVSS v3.1: not applicable

OSV.dev reports GHSA-h395-gr6q-cpjc (CVE-2026-25537) for crates.io package jsonwebtoken at version 9.3.1: jsonwebtoken has Type Confusion that leads to potential authorization bypass. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-h395-gr6q-cpjc
```

**Evidence.**

_tool_output · [OSV.dev GHSA-h395-gr6q-cpjc](https://osv.dev/vulnerability/GHSA-h395-gr6q-cpjc) · manifest · SHA-256 5512edb8cb1bd9b3bd496f0eebe1107455f6b41bbce1ab22cc4c8ae28ef97c12_

```
{"id": "GHSA-h395-gr6q-cpjc", "aliases": ["CVE-2026-25537"], "modified": "2026-09-10T03:50:35.169824826Z", "summary": "jsonwebtoken has Type Confusion that leads to potential authorization bypass", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N/E:P"}], "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (10.3.0).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-19527 — rmcp 1.4.0 is affected by GHSA-9g45-5xwm-f3wc (CVE-2026-64684)

- Severity: **Medium** · Classification: Known vulnerable component · Confidence: Medium
- Affected asset: `dependency:crates.io/rmcp@1.4.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 44.2 / 100
- CVSS v3.1: 6.8 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:N/A:N`)

OSV.dev reports GHSA-9g45-5xwm-f3wc (CVE-2026-64684) for crates.io package rmcp at version 1.4.0: RMCP: Custom HTTP headers leak to cross-origin redirect targets. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-9g45-5xwm-f3wc
```

**Evidence.**

_tool_output · [OSV.dev GHSA-9g45-5xwm-f3wc](https://osv.dev/vulnerability/GHSA-9g45-5xwm-f3wc) · manifest · SHA-256 9ca385e2c811ca73c332b7dd793b1f1bd194d670c49ba6935d68745f9dd6c7cc_

```
{"id": "GHSA-9g45-5xwm-f3wc", "aliases": ["CVE-2026-64684"], "modified": "2026-09-17T16:45:06.215938994Z", "summary": "RMCP: Custom HTTP headers leak to cross-origin redirect targets", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:N/A:N"}], "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (2.1.0).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-19529 — rmcp 1.4.0 is affected by GHSA-c9xm-49cp-xcr9

- Severity: **Medium** · Classification: Known vulnerable component · Confidence: Medium
- Affected asset: `dependency:crates.io/rmcp@1.4.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 44.2 / 100
- CVSS v3.1: not applicable

OSV.dev reports GHSA-c9xm-49cp-xcr9 for crates.io package rmcp at version 1.4.0: rmcp OAuth client fetches server-controlled resource_metadata URLs. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-c9xm-49cp-xcr9
```

**Evidence.**

_tool_output · [OSV.dev GHSA-c9xm-49cp-xcr9](https://osv.dev/vulnerability/GHSA-c9xm-49cp-xcr9) · manifest · SHA-256 305b8c99a86ada5b92bf6013107220f46538f4a0eab77500146b85b0a410d5b4_

```
{"id": "GHSA-c9xm-49cp-xcr9", "aliases": [], "modified": "2026-10-02T16:30:07.619134114Z", "summary": "rmcp OAuth client fetches server-controlled resource_metadata URLs", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N"}], "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (2.0.0).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-19536 — serde_with 3.16.1 is affected by GHSA-7gcf-g7xr-8hxj

- Severity: **Medium** · Classification: Known vulnerable component · Confidence: Medium
- Affected asset: `dependency:crates.io/serde_with@3.16.1`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 44.2 / 100
- CVSS v3.1: not applicable

OSV.dev reports GHSA-7gcf-g7xr-8hxj for crates.io package serde_with at version 3.16.1: serde_with: KeyValueMap serialization panics on empty sequence or map entries. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-7gcf-g7xr-8hxj
```

**Evidence.**

_tool_output · [OSV.dev GHSA-7gcf-g7xr-8hxj](https://osv.dev/vulnerability/GHSA-7gcf-g7xr-8hxj) · manifest · SHA-256 b42c751004bfb387a1f24d4e9b23157ae70dc8f33fdb503f87f6d04255008aa3_

```
{"id": "GHSA-7gcf-g7xr-8hxj", "aliases": [], "modified": "2026-09-10T03:51:10.897685062Z", "summary": "serde_with: KeyValueMap serialization panics on empty sequence or map entries", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:N"}], "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (3.21.0).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-19537 — tar 0.4.45 is affected by GHSA-3pv8-6f4r-ffg2

- Severity: **Medium** · Classification: Known vulnerable component · Confidence: Medium
- Affected asset: `dependency:crates.io/tar@0.4.45`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 44.2 / 100
- CVSS v3.1: not applicable

OSV.dev reports GHSA-3pv8-6f4r-ffg2 for crates.io package tar at version 0.4.45: tar has a PAX header desynchronization issue. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-3pv8-6f4r-ffg2
```

**Evidence.**

_tool_output · [OSV.dev GHSA-3pv8-6f4r-ffg2](https://osv.dev/vulnerability/GHSA-3pv8-6f4r-ffg2) · manifest · SHA-256 ea380731f63af3a9d11d5db2269a81a3bb262ca10b6cbc95fecc4fef0221ee6f_

```
{"id": "GHSA-3pv8-6f4r-ffg2", "aliases": [], "modified": "2026-09-10T03:51:04.454810375Z", "summary": "tar has a PAX header desynchronization issue", "severity": null, "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (0.4.46).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-19466 — Raw ecrecover usage in contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/cryptography/ECDSA.sol

- Severity: **Medium** · Classification: Potential cryptographic risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `contract:contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/cryptography/ECDSA.sol`
- Data source: contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/cryptography/ECDSA.sol
- Detection method: Solidity source pattern analysis.
- Analyzer: solidity 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 43.6 / 100
- CVSS v3.1: not applicable

ecrecover at line 148. (related: SWC-117/SWC-121)

**Potential impact.** Without s-value/zero-address checks and nonces, signatures may be malleable or replayable. ecrecover relies on secp256k1 ECDSA (quantum-vulnerable long-term).

**Reproduction steps.**

```
Open line 148 in the supplied file contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/cryptography/ECDSA.sol and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/cryptography/ECDSA.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/cryptography/ECDSA.sol#L148) · line 148 · SHA-256 bbb05c626df7732576d2e3f08f6fcf908767b508ed20b71385b32c95794d893e_

```
  146 | 
  147 |         // If the signature is valid (and not malleable), return the signer address
  148 |         address signer = ecrecover(hash, v, r, s);
  149 |         if (signer == address(0)) {
  150 |             return (address(0), RecoverError.InvalidSignature, bytes32(0));
```

**Limitations of the check.** Lightweight static pattern analysis of Solidity source without compilation or symbolic execution. It does not replace a full smart-contract audit; confirm manually or with dedicated tools (Slither, Foundry tests).

**Recommendation.** Use OpenZeppelin ECDSA.recover with EIP-712 domain separation and nonces.

**Retest procedure.** Re-run static analysis and add a unit/fuzz test that exercises the pattern.

### QSI-2026-19485 — Raw ecrecover usage in contracts/lib/openzeppelin-contracts/contracts/utils/cryptography/ECDSA.sol

- Severity: **Medium** · Classification: Potential cryptographic risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `contract:contracts/lib/openzeppelin-contracts/contracts/utils/cryptography/ECDSA.sol`
- Data source: contracts/lib/openzeppelin-contracts/contracts/utils/cryptography/ECDSA.sol
- Detection method: Solidity source pattern analysis.
- Analyzer: solidity 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 43.6 / 100
- CVSS v3.1: not applicable

ecrecover at line 148. (related: SWC-117/SWC-121)

**Potential impact.** Without s-value/zero-address checks and nonces, signatures may be malleable or replayable. ecrecover relies on secp256k1 ECDSA (quantum-vulnerable long-term).

**Reproduction steps.**

```
Open line 148 in the supplied file contracts/lib/openzeppelin-contracts/contracts/utils/cryptography/ECDSA.sol and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [contracts/lib/openzeppelin-contracts/contracts/utils/cryptography/ECDSA.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts/contracts/utils/cryptography/ECDSA.sol#L148) · line 148 · SHA-256 bbb05c626df7732576d2e3f08f6fcf908767b508ed20b71385b32c95794d893e_

```
  146 | 
  147 |         // If the signature is valid (and not malleable), return the signer address
  148 |         address signer = ecrecover(hash, v, r, s);
  149 |         if (signer == address(0)) {
  150 |             return (address(0), RecoverError.InvalidSignature, bytes32(0));
```

**Limitations of the check.** Lightweight static pattern analysis of Solidity source without compilation or symbolic execution. It does not replace a full smart-contract audit; confirm manually or with dedicated tools (Slither, Foundry tests).

**Recommendation.** Use OpenZeppelin ECDSA.recover with EIP-712 domain separation and nonces.

**Retest procedure.** Re-run static analysis and add a unit/fuzz test that exercises the pattern.

### QSI-2026-19421 — Quantum-vulnerable Ed25519: transaction and message signing (1 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:Ed25519:transaction_signing`
- Data source: crates/signer/src/local.rs
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 35.6 / 100
- CVSS v3.1: not applicable

1 reference(s) to Ed25519 across 1 file(s), e.g. crates/signer/src/local.rs:26. Role, judged from paths, function names and nearby code: transaction and message signing. A CRQC derives the private key from a public key that is already known (on chain after the first spend, in reused addresses): funds and approvals controlled by these keys need a migration path.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open crates/signer/src/local.rs:26 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [crates/signer/src/local.rs](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/crates/signer/src/local.rs#L26) · line 26 · SHA-256 c2ce9e5fae650659e9da0a14bf5a52b1beb54d3f2818af84eb8c930954bb8f82_

```
   25 | 
   26 | pub use malachitebft_signing_ed25519::*;
   27 | 
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains adopt them.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-19422 — Quantum-vulnerable ECDSA: transaction and message signing (4 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:ECDSA:transaction_signing`
- Data source: crates/spammer/src/accounts.rs
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 35.6 / 100
- CVSS v3.1: not applicable

4 reference(s) to ECDSA across 4 file(s), e.g. crates/spammer/src/accounts.rs:20. Role, judged from paths, function names and nearby code: transaction and message signing. A CRQC derives the private key from a public key that is already known (on chain after the first spend, in reused addresses): funds and approvals controlled by these keys need a migration path.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open crates/spammer/src/accounts.rs:20 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [crates/spammer/src/accounts.rs](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/crates/spammer/src/accounts.rs#L20) · line 20 · SHA-256 0273a225b1be1776c71fa9c34290b74865b18d1d3c22d66e478e9ae1a3ed7f8c_

```
   19 | use color_eyre::eyre::{self, Context, Result};
   20 | use k256::ecdsa::SigningKey;
   21 | use serde::{Deserialize, Serialize};
```

_file_excerpt · [crates/spammer/src/generator.rs](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/crates/spammer/src/generator.rs#L23) · line 23 · SHA-256 dccd4934ba92819c55bd41fc3d651df59a8ec1356622025eab4d8d40e4b79789_

```
   22 | use color_eyre::eyre::{self, Result};
   23 | use k256::ecdsa::SigningKey;
   24 | use rand::Rng;
```

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/cryptography/ECDSA.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/cryptography/ECDSA.sol#L148) · line 148 · SHA-256 bbb05c626df7732576d2e3f08f6fcf908767b508ed20b71385b32c95794d893e_

```
  146 | 
  147 |         // If the signature is valid (and not malleable), return the signer address
  148 |         address signer = ecrecover(hash, v, r, s);
  149 |         if (signer == address(0)) {
  150 |             return (address(0), RecoverError.InvalidSignature, bytes32(0));
```

_file_excerpt · [contracts/lib/openzeppelin-contracts/contracts/utils/cryptography/ECDSA.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts/contracts/utils/cryptography/ECDSA.sol#L148) · line 148 · SHA-256 bbb05c626df7732576d2e3f08f6fcf908767b508ed20b71385b32c95794d893e_

```
  146 | 
  147 |         // If the signature is valid (and not malleable), return the signer address
  148 |         address signer = ecrecover(hash, v, r, s);
  149 |         if (signer == address(0)) {
  150 |             return (address(0), RecoverError.InvalidSignature, bytes32(0));
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains adopt them.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-19420 — Quantum-vulnerable ECDSA: role not determined (2 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:ECDSA:general`
- Data source: crates/quake/src/nodekey.rs
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 34.2 / 100
- CVSS v3.1: not applicable

3 reference(s) to ECDSA across 2 file(s), e.g. crates/quake/src/nodekey.rs:23. Role, judged from paths, function names and nearby code: role not determined. The code does not show what the keys protect; review decides the priority.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open crates/quake/src/nodekey.rs:23 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [crates/quake/src/nodekey.rs](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/crates/quake/src/nodekey.rs#L23) · line 23 · SHA-256 e12a2180b412a84ef180085d707eb0f0b4cc77bf22e34a02b0364a7cf0a70a0a_

```
   22 | use reth_network_peers::{pk2id, NodeRecord, PeerId};
   23 | use secp256k1::{SecretKey, SECP256K1};
   24 | use std::fs;
```

_file_excerpt · [crates/quake/src/nodekey.rs](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/crates/quake/src/nodekey.rs#L129) · line 129 · SHA-256 aa0bb537f284ae1e32e935520eff06631f8af6b5634e814d5992a7b73e88f9a8_

```
  128 |     SecretKey::from_slice(&bytes)
  129 |         .map_err(|e| eyre!("Invalid secp256k1 key in nodekey file {path:?}: {e}"))
  130 | }
```

_file_excerpt · [crates/quake/src/rpc/valset_manager.rs](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/crates/quake/src/rpc/valset_manager.rs#L25) · line 25 · SHA-256 e388969a4614dc2df4532973295425542dbc698331b43f40317547918e58d2ef_

```
   24 | use color_eyre::eyre::{eyre, Context, Result};
   25 | use k256::ecdsa::SigningKey;
   26 | use serde::{Deserialize, Serialize};
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it; introduce an abstraction layer for crypto-agility.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-19423 — Quantum-vulnerable Ed25519: role not determined (4 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:Ed25519:general`
- Data source: crates/types/src/codec/proto.rs
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 34.2 / 100
- CVSS v3.1: not applicable

4 reference(s) to Ed25519 across 4 file(s), e.g. crates/types/src/codec/proto.rs:28. Role, judged from paths, function names and nearby code: role not determined. The code does not show what the keys protect; review decides the priority.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open crates/types/src/codec/proto.rs:28 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [crates/types/src/codec/proto.rs](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/crates/types/src/codec/proto.rs#L28) · line 28 · SHA-256 4690a4677968e8bbb2e0ae3db50e5dcc1ed2093b4bcb5c88fcc46792a755eb20_

```
   27 | use malachitebft_proto::{Error as ProtoError, Protobuf};
   28 | use malachitebft_signing_ed25519::Signature;
   29 | use malachitebft_sync::{self as sync, PeerId};
```

_file_excerpt · [crates/types/src/proposal_part.rs](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/crates/types/src/proposal_part.rs#L26) · line 26 · SHA-256 8cade3a23b00481a217233938938416eae2a70b38ccb6b49462f9b2586c49496_

```
   25 | use malachitebft_proto::{self as proto, Error as ProtoError, Protobuf};
   26 | use malachitebft_signing_ed25519::Signature;
   27 | 
```

_file_excerpt · [crates/types/src/signing.rs](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/crates/types/src/signing.rs#L21) · line 21 · SHA-256 1969d2368ea84b5f938dab550dc744d6d6aa4ff1c28410833b90aee8f261367f_

```
   20 | };
   21 | pub use malachitebft_signing_ed25519::{Ed25519, PrivateKey, PublicKey, Signature};
   22 | 
```

_file_excerpt · [crates/types/src/ssz/v1/vote.rs](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/crates/types/src/ssz/v1/vote.rs#L21) · line 21 · SHA-256 2de65aa6e6820f63bf63741dd7857a7ee02a58a14c777940fb17366f65b41e3f_

```
   20 | use malachitebft_core_types::{SignedVote, VoteType};
   21 | use malachitebft_signing_ed25519::Signature;
   22 | 
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it; introduce an abstraction layer for crypto-agility.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-19490 — block-buffer 0.12.0 is affected by GHSA-qwgh-2vcv-g2f7

- Severity: **Medium** · Classification: Known vulnerable component · Confidence: Low
- Affected asset: `dependency:crates.io/block-buffer@0.12.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 33.1 / 100
- CVSS v3.1: not applicable

OSV.dev reports GHSA-qwgh-2vcv-g2f7 for crates.io package block-buffer at version 0.12.0: block_buffer: panic corrupts inline buffer position. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-qwgh-2vcv-g2f7
```

**Evidence.**

_tool_output · [OSV.dev GHSA-qwgh-2vcv-g2f7](https://osv.dev/vulnerability/GHSA-qwgh-2vcv-g2f7) · manifest · SHA-256 7591b0713b64478fa8ad16a5dd54163bfd64b0d142da6666684f3debae896c25_

```
{"id": "GHSA-qwgh-2vcv-g2f7", "aliases": [], "modified": "2026-10-30T15:45:11.580215361Z", "summary": "block_buffer: panic corrupts inline buffer position", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:L/VI:L/VA:N/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (none published yet; see the advisory for mitigations).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-19491 — cmov 0.5.2 is affected by GHSA-3rjw-m598-pq24 (CVE-2026-50185)

- Severity: **Medium** · Classification: Known vulnerable component · Confidence: Low
- Affected asset: `dependency:crates.io/cmov@0.5.2`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 33.1 / 100
- CVSS v3.1: not applicable

OSV.dev reports GHSA-3rjw-m598-pq24 (CVE-2026-50185) for crates.io package cmov at version 0.5.2: Cmov/CmovEq on aarch64 can produce wrong results if high-bits of registers are set. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-3rjw-m598-pq24
```

**Evidence.**

_tool_output · [OSV.dev GHSA-3rjw-m598-pq24](https://osv.dev/vulnerability/GHSA-3rjw-m598-pq24) · manifest · SHA-256 27176a365b98febca62de077da5905b32eccbb59430084dc5dbabfd3e69d6343_

```
{"id": "GHSA-3rjw-m598-pq24", "aliases": ["CVE-2026-50185"], "modified": "2026-09-10T03:51:10.250390903Z", "summary": "Cmov/CmovEq on aarch64 can produce wrong results if high-bits of registers are set ", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N/E:P"}], "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (0.5.4).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-19500 — hickory-proto 0.25.2 is affected by GHSA-q2qq-hmj6-3wpp (RUSTSEC-2026-0119)

- Severity: **Medium** · Classification: Known vulnerable component · Confidence: Low
- Affected asset: `dependency:crates.io/hickory-proto@0.25.2`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 33.1 / 100
- CVSS v3.1: not applicable

OSV.dev reports GHSA-q2qq-hmj6-3wpp (RUSTSEC-2026-0119) for crates.io package hickory-proto at version 0.25.2: hickory-proto vulnerable to CPU exhaustion during message encoding due to O(n²) name compression. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-q2qq-hmj6-3wpp
```

**Evidence.**

_tool_output · [OSV.dev GHSA-q2qq-hmj6-3wpp](https://osv.dev/vulnerability/GHSA-q2qq-hmj6-3wpp) · manifest · SHA-256 a1d335f000995ae746f9c3c12f06c15ff8c13707b954c076afe865b69d3a3b06_

```
{"id": "GHSA-q2qq-hmj6-3wpp", "aliases": ["RUSTSEC-2026-0119"], "modified": "2026-09-10T03:51:06.690531529Z", "summary": "hickory-proto vulnerable to CPU exhaustion during message encoding due to O(n²) name compression", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (0.26.1).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-19502 — hickory-resolver 0.25.2 is affected by GHSA-6f2x-v7q7-m7m5

- Severity: **Medium** · Classification: Known vulnerable component · Confidence: Low
- Affected asset: `dependency:crates.io/hickory-resolver@0.25.2`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 33.1 / 100
- CVSS v3.1: not applicable

OSV.dev reports GHSA-6f2x-v7q7-m7m5 for crates.io package hickory-resolver at version 0.25.2: hickory-resolver follows irrelevant CNAME records. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-6f2x-v7q7-m7m5
```

**Evidence.**

_tool_output · [OSV.dev GHSA-6f2x-v7q7-m7m5](https://osv.dev/vulnerability/GHSA-6f2x-v7q7-m7m5) · manifest · SHA-256 48a180207e8da293534f1ca0c2e4ae7cfb203bb592ece2f7b4ded90349914639_

```
{"id": "GHSA-6f2x-v7q7-m7m5", "aliases": [], "modified": "2026-10-05T23:15:03.987605025Z", "summary": "hickory-resolver follows irrelevant CNAME records", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (0.26.2).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-19511 — openssl 0.10.75 is affected by GHSA-phqj-4mhp-q6mq (CVE-2026-45784)

- Severity: **Medium** · Classification: Known vulnerable component · Confidence: Low
- Affected asset: `dependency:crates.io/openssl@0.10.75`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 33.1 / 100
- CVSS v3.1: not applicable

OSV.dev reports GHSA-phqj-4mhp-q6mq (CVE-2026-45784) for crates.io package openssl at version 0.10.75: rust-openssl: Potential out-of-bounds write in `CipherCtxRef::cipher_update_inplace` for AES-KW-PAD ciphers. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-phqj-4mhp-q6mq
```

**Evidence.**

_tool_output · [OSV.dev GHSA-phqj-4mhp-q6mq](https://osv.dev/vulnerability/GHSA-phqj-4mhp-q6mq) · manifest · SHA-256 883691705dc3dbcc2a7b246591b4e3a6c655ecd3f754bfe49c73ce1a27ee4377_

```
{"id": "GHSA-phqj-4mhp-q6mq", "aliases": ["CVE-2026-45784"], "modified": "2026-09-10T03:51:06.601254514Z", "summary": "rust-openssl: Potential out-of-bounds write in `CipherCtxRef::cipher_update_inplace` for AES-KW-PAD ciphers", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:N/VI:L/VA:L/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (0.10.80).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-19515 — openssl 0.10.75 is affected by GHSA-xv59-967r-8726 (CVE-2026-44662)

- Severity: **Medium** · Classification: Known vulnerable component · Confidence: Low
- Affected asset: `dependency:crates.io/openssl@0.10.75`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 33.1 / 100
- CVSS v3.1: not applicable

OSV.dev reports GHSA-xv59-967r-8726 (CVE-2026-44662) for crates.io package openssl at version 0.10.75: rust-openssl vulnerable to heap buffer overflow when encrypting with AES key-wrap-with-padding. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-xv59-967r-8726
```

**Evidence.**

_tool_output · [OSV.dev GHSA-xv59-967r-8726](https://osv.dev/vulnerability/GHSA-xv59-967r-8726) · manifest · SHA-256 65e7b83d8891d6cb32ae4f4bd6e80da5d770afea05f42c516e61973df0f9837a_

```
{"id": "GHSA-xv59-967r-8726", "aliases": ["CVE-2026-44662"], "modified": "2026-09-10T03:51:07.319185525Z", "summary": "rust-openssl vulnerable to heap buffer overflow when encrypting with AES key-wrap-with-padding", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:N/VI:L/VA:L/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (0.10.79).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-19516 — opentelemetry_sdk 0.31.0 is affected by GHSA-w9wp-h8wv-79jx (CVE-2026-48504)

- Severity: **Medium** · Classification: Known vulnerable component · Confidence: Low
- Affected asset: `dependency:crates.io/opentelemetry_sdk@0.31.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 33.1 / 100
- CVSS v3.1: 5.3 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L`)

OSV.dev reports GHSA-w9wp-h8wv-79jx (CVE-2026-48504) for crates.io package opentelemetry_sdk at version 0.31.0: opentelemetry_sdk has unbounded memory allocation in W3C Baggage propagation. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-w9wp-h8wv-79jx
```

**Evidence.**

_tool_output · [OSV.dev GHSA-w9wp-h8wv-79jx](https://osv.dev/vulnerability/GHSA-w9wp-h8wv-79jx) · manifest · SHA-256 813831dd003cedf6504e30c78f17b1892961288b94c8ca7a04d7c8da0bfb295a_

```
{"id": "GHSA-w9wp-h8wv-79jx", "aliases": ["CVE-2026-48504"], "modified": "2026-09-10T03:50:50.807599062Z", "summary": "opentelemetry_sdk has unbounded memory allocation in W3C Baggage propagation", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L"}], "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (0.32.1).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-19530 — rustls 0.23.36 is affected by GHSA-2mjx-qc3c-rqvc (RUSTSEC-2026-0285)

- Severity: **Medium** · Classification: Known vulnerable component · Confidence: Low
- Affected asset: `dependency:crates.io/rustls@0.23.36`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 33.1 / 100
- CVSS v3.1: 5.3 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N`)

OSV.dev reports GHSA-2mjx-qc3c-rqvc (RUSTSEC-2026-0285) for crates.io package rustls at version 0.23.36: Rustls: TLS 1.3 handshake messages incorrectly accepted across encryption level boundaries. The advisory names no affected functions, so reachability was not determined.

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

### QSI-2026-19531 — rustls 0.23.36 is affected by GHSA-c8m5-c952-6cm4 (RUSTSEC-2026-0346)

- Severity: **Medium** · Classification: Known vulnerable component · Confidence: Low
- Affected asset: `dependency:crates.io/rustls@0.23.36`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 33.1 / 100
- CVSS v3.1: 4.0 (`CVSS:3.1/AV:L/AC:H/PR:H/UI:R/S:U/C:H/I:N/A:N`)

OSV.dev reports GHSA-c8m5-c952-6cm4 (RUSTSEC-2026-0346) for crates.io package rustls at version 0.23.36: Rustls: Session Debug formatting exposes TLS master secrets and resumption PSKs. The advisory names no affected functions, so reachability was not determined.

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

### QSI-2026-19525 — rand 0.8.5 is affected by GHSA-cq8v-f236-94qc (RUSTSEC-2026-0097)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Medium
- Affected asset: `dependency:crates.io/rand@0.8.5`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 39.2 / 100
- CVSS v3.1: not applicable

OSV.dev reports GHSA-cq8v-f236-94qc (RUSTSEC-2026-0097) for crates.io package rand at version 0.8.5: Rand is unsound with a custom logger using rand::rng(). The audited code names rand::rng, rand::thread_rng: the affected code may be reachable.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-cq8v-f236-94qc
```

**Evidence.**

_tool_output · [OSV.dev GHSA-cq8v-f236-94qc](https://osv.dev/vulnerability/GHSA-cq8v-f236-94qc) · manifest · SHA-256 a61cde8ef254431f750cff43ce8ebe999ba61525990761c3c15b83d24b6124b6_

```
{"id": "GHSA-cq8v-f236-94qc", "aliases": ["RUSTSEC-2026-0097"], "modified": "2026-09-10T03:50:43.958966498Z", "summary": "Rand is unsound with a custom logger using rand::rng()", "severity": null, "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (0.10.1, 0.8.6, 0.9.3).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-19411 — Floating pragma (^0.8.29) in 29 file(s)

- Severity: **Low** · Classification: Improvement recommendation · Confidence: High
- Affected asset: `solidity:pragma:^0.8.29`
- Data source: contracts/scripts/Addresses.sol
- Detection method: Solidity source pattern analysis.
- Analyzer: solidity 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 34.8 / 100
- CVSS v3.1: not applicable

pragma ^0.8.29 in 29 file(s), first at contracts/scripts/Addresses.sol:17. (related: SWC-103)

**Potential impact.** Contracts may be deployed with untested compiler versions. The compiler actually used is set by the build configuration, which this check does not read.

**Reproduction steps.**

```
Open contracts/scripts/Addresses.sol:17 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [contracts/scripts/Addresses.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/scripts/Addresses.sol#L17) · line 17 · SHA-256 5c8ac17d5a976b0f9784507cbb9141142f04a4aade299887ce0ed620236d0ee9_

```
   15 | // limitations under the License.
   16 | 
   17 | pragma solidity ^0.8.29;
   18 | 
   19 | /**
```

_file_excerpt · [contracts/scripts/ArtifactHelper.s.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/scripts/ArtifactHelper.s.sol#L17) · line 17 · SHA-256 ef0692d8465f6899047b1bb52eb49cdf4761299252a363f448f00c78e1355394_

```
   15 | // limitations under the License.
   16 | 
   17 | pragma solidity ^0.8.29;
   18 | 
   19 | // ArtifactHelper — genesis builder entrypoint. Reads compiled contract bytecode and
```

_file_excerpt · [contracts/scripts/DenylistManagement.s.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/scripts/DenylistManagement.s.sol#L17) · line 17 · SHA-256 80b7cf5c4aec11e96887a954beb4331a83011a8dc7475bc12c456d83c24fdc92_

```
   15 | // limitations under the License.
   16 | 
   17 | pragma solidity ^0.8.29;
   18 | 
   19 | import {Script, console} from "forge-std/Script.sol";
```

_file_excerpt · [contracts/scripts/DeployGasGuzzler.s.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/scripts/DeployGasGuzzler.s.sol#L17) · line 17 · SHA-256 80b7cf5c4aec11e96887a954beb4331a83011a8dc7475bc12c456d83c24fdc92_

```
   15 | // limitations under the License.
   16 | 
   17 | pragma solidity ^0.8.29;
   18 | 
   19 | import {Script, console} from "forge-std/Script.sol";
```

_file_excerpt · [contracts/scripts/DeployMemo.s.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/scripts/DeployMemo.s.sol#L17) · line 17 · SHA-256 80b7cf5c4aec11e96887a954beb4331a83011a8dc7475bc12c456d83c24fdc92_

```
   15 | // limitations under the License.
   16 | 
   17 | pragma solidity ^0.8.29;
   18 | 
   19 | import {Script, console} from "forge-std/Script.sol";
```

_file_excerpt · [contracts/scripts/DeployMulticall3From.s.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/scripts/DeployMulticall3From.s.sol#L17) · line 17 · SHA-256 80b7cf5c4aec11e96887a954beb4331a83011a8dc7475bc12c456d83c24fdc92_

```
   15 | // limitations under the License.
   16 | 
   17 | pragma solidity ^0.8.29;
   18 | 
   19 | import {Script, console} from "forge-std/Script.sol";
```

_file_excerpt · [contracts/scripts/DeployPermissionedValidatorManager.s.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/scripts/DeployPermissionedValidatorManager.s.sol#L17) · line 17 · SHA-256 80b7cf5c4aec11e96887a954beb4331a83011a8dc7475bc12c456d83c24fdc92_

```
   15 | // limitations under the License.
   16 | 
   17 | pragma solidity ^0.8.29;
   18 | 
   19 | import {Script, console} from "forge-std/Script.sol";
```

_file_excerpt · [contracts/scripts/DeployProtocolConfig.s.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/scripts/DeployProtocolConfig.s.sol#L17) · line 17 · SHA-256 80b7cf5c4aec11e96887a954beb4331a83011a8dc7475bc12c456d83c24fdc92_

```
   15 | // limitations under the License.
   16 | 
   17 | pragma solidity ^0.8.29;
   18 | 
   19 | import {Script, console} from "forge-std/Script.sol";
```

_file_excerpt · [contracts/scripts/ProtocolConfigManagement.s.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/scripts/ProtocolConfigManagement.s.sol#L17) · line 17 · SHA-256 80b7cf5c4aec11e96887a954beb4331a83011a8dc7475bc12c456d83c24fdc92_

```
   15 | // limitations under the License.
   16 | 
   17 | pragma solidity ^0.8.29;
   18 | 
   19 | import {Script, console} from "forge-std/Script.sol";
```

_file_excerpt · [contracts/scripts/ProxyManagement.s.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/scripts/ProxyManagement.s.sol#L17) · line 17 · SHA-256 80b7cf5c4aec11e96887a954beb4331a83011a8dc7475bc12c456d83c24fdc92_

```
   15 | // limitations under the License.
   16 | 
   17 | pragma solidity ^0.8.29;
   18 | 
   19 | import {Script, console} from "forge-std/Script.sol";
```

**Limitations of the check.** Lightweight static pattern analysis of Solidity source without compilation or symbolic execution. It does not replace a full smart-contract audit; confirm manually or with dedicated tools (Slither, Foundry tests).

**Recommendation.** Pin the compiler version used in testing.

**Retest procedure.** Re-run static analysis and add a unit/fuzz test that exercises the pattern.

### QSI-2026-19424 — Floating pragma (^0.8.20) in 336 file(s)

- Severity: **Low** · Classification: Improvement recommendation · Confidence: High
- Affected asset: `solidity:pragma:^0.8.20`
- Data source: contracts/lib/openzeppelin-contracts-upgradeable/certora/harnesses/AccessControlDefaultAdminRulesHarness.sol
- Detection method: Solidity source pattern analysis.
- Analyzer: solidity 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 34.8 / 100
- CVSS v3.1: not applicable

pragma ^0.8.20 in 336 file(s), first at contracts/lib/openzeppelin-contracts-upgradeable/certora/harnesses/AccessControlDefaultAdminRulesHarness.sol:2. (related: SWC-103)

**Potential impact.** Contracts may be deployed with untested compiler versions. The compiler actually used is set by the build configuration, which this check does not read.

**Reproduction steps.**

```
Open contracts/lib/openzeppelin-contracts-upgradeable/certora/harnesses/AccessControlDefaultAdminRulesHarness.sol:2 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/certora/harnesses/AccessControlDefaultAdminRulesHarness.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/certora/harnesses/AccessControlDefaultAdminRulesHarness.sol#L2) · line 2 · SHA-256 756598f4bd85d94c54eb240ebeadf53780d19d71de6fe7a69ff53c1507742f21_

```
    1 | // SPDX-License-Identifier: MIT
    2 | pragma solidity ^0.8.20;
    3 | 
    4 | import {AccessControlDefaultAdminRules} from "../patched/access/extensions/AccessControlDefaultAdminRules.sol";
```

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/certora/harnesses/AccessControlHarness.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/certora/harnesses/AccessControlHarness.sol#L2) · line 2 · SHA-256 d3760e2e2e6b2de828a557f740f9904e637cc250bed6ea48140f2d7daef11453_

```
    1 | // SPDX-License-Identifier: MIT
    2 | pragma solidity ^0.8.20;
    3 | 
    4 | import {AccessControl} from "../patched/access/AccessControl.sol";
```

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/certora/harnesses/AccessManagedHarness.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/certora/harnesses/AccessManagedHarness.sol#L3) · line 3 · SHA-256 8b82af0296a3ec37e4e214190af0400128d0db4f5ee34af49eec871b38137797_

```
    1 | // SPDX-License-Identifier: MIT
    2 | 
    3 | pragma solidity ^0.8.20;
    4 | 
    5 | import "../patched/access/manager/IAccessManager.sol";
```

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/certora/harnesses/AccessManagerHarness.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/certora/harnesses/AccessManagerHarness.sol#L3) · line 3 · SHA-256 87d2bae8e69f1f7f97a6ba1e9699d0307d2dae27a7db50ac21f0dc2fb2cdf318_

```
    1 | // SPDX-License-Identifier: MIT
    2 | 
    3 | pragma solidity ^0.8.20;
    4 | 
    5 | import "../patched/access/manager/AccessManager.sol";
```

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/certora/harnesses/DoubleEndedQueueHarness.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/certora/harnesses/DoubleEndedQueueHarness.sol#L2) · line 2 · SHA-256 7465f9b8e6c53057c2d9dfbc88a2b83fb14b813ca1d865da45a12143ec796206_

```
    1 | // SPDX-License-Identifier: MIT
    2 | pragma solidity ^0.8.20;
    3 | 
    4 | import {DoubleEndedQueue} from "../patched/utils/structs/DoubleEndedQueue.sol";
```

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/certora/harnesses/ERC20FlashMintHarness.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/certora/harnesses/ERC20FlashMintHarness.sol#L3) · line 3 · SHA-256 d9268da21b039a53f3ffe15e3e1b64163968ef2adaabc61fb422f2327baf75d3_

```
    1 | // SPDX-License-Identifier: MIT
    2 | 
    3 | pragma solidity ^0.8.20;
    4 | 
    5 | import "../patched/token/ERC20/ERC20.sol";
```

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/certora/harnesses/ERC20PermitHarness.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/certora/harnesses/ERC20PermitHarness.sol#L2) · line 2 · SHA-256 fe79ecdbebdd3812b94f5edab6c9b7572be14d41aa4c9be552aa6706e1ac1d3d_

```
    1 | // SPDX-License-Identifier: MIT
    2 | pragma solidity ^0.8.20;
    3 | 
    4 | import {ERC20Permit, ERC20} from "../patched/token/ERC20/extensions/ERC20Permit.sol";
```

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/certora/harnesses/ERC20WrapperHarness.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/certora/harnesses/ERC20WrapperHarness.sol#L3) · line 3 · SHA-256 16d256728596f72ea22e19d41f979405a160b6d28721d44c83e4422d9017b2ce_

```
    1 | // SPDX-License-Identifier: MIT
    2 | 
    3 | pragma solidity ^0.8.20;
    4 | 
    5 | import {ERC20Permit} from "../patched/token/ERC20/extensions/ERC20Permit.sol";
```

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/certora/harnesses/ERC3156FlashBorrowerHarness.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/certora/harnesses/ERC3156FlashBorrowerHarness.sol#L5) · line 5 · SHA-256 c5389bf3b06d502da28d0c5a350b10b0fabe82e0ffba247a522ea005b5e3ad09_

```
    3 | import {IERC3156FlashBorrower} from "../patched/interfaces/IERC3156FlashBorrower.sol";
    4 | 
    5 | pragma solidity ^0.8.20;
    6 | 
    7 | contract ERC3156FlashBorrowerHarness is IERC3156FlashBorrower {
```

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/certora/harnesses/ERC721Harness.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/certora/harnesses/ERC721Harness.sol#L3) · line 3 · SHA-256 6f89bde0f57299ebcc2623cc87a97d97d48f0b4775ed243d802e69dc6d1fee44_

```
    1 | // SPDX-License-Identifier: MIT
    2 | 
    3 | pragma solidity ^0.8.20;
    4 | 
    5 | import {ERC721} from "../patched/token/ERC721/ERC721.sol";
```

**Limitations of the check.** Lightweight static pattern analysis of Solidity source without compilation or symbolic execution. It does not replace a full smart-contract audit; confirm manually or with dedicated tools (Slither, Foundry tests).

**Recommendation.** Pin the compiler version used in testing.

**Retest procedure.** Re-run static analysis and add a unit/fuzz test that exercises the pattern.

### QSI-2026-19429 — Floating pragma (^0.8.26) in 12 file(s)

- Severity: **Low** · Classification: Improvement recommendation · Confidence: High
- Affected asset: `solidity:pragma:^0.8.26`
- Data source: contracts/lib/openzeppelin-contracts-upgradeable/contracts/account/extensions/draft-AccountERC7579HookedUpgradeable.sol
- Detection method: Solidity source pattern analysis.
- Analyzer: solidity 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 34.8 / 100
- CVSS v3.1: not applicable

pragma ^0.8.26 in 12 file(s), first at contracts/lib/openzeppelin-contracts-upgradeable/contracts/account/extensions/draft-AccountERC7579HookedUpgradeable.sol:4. (related: SWC-103)

**Potential impact.** Contracts may be deployed with untested compiler versions. The compiler actually used is set by the build configuration, which this check does not read.

**Reproduction steps.**

```
Open contracts/lib/openzeppelin-contracts-upgradeable/contracts/account/extensions/draft-AccountERC7579HookedUpgradeable.sol:4 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/contracts/account/extensions/draft-AccountERC7579HookedUpgradeable.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/contracts/account/extensions/draft-AccountERC7579HookedUpgradeable.sol#L4) · line 4 · SHA-256 3b08fda64ef29f18684f1806c44e64f22faca5f8525d60a3a9a1a3b747c027ed_

```
    2 | // OpenZeppelin Contracts (last updated v5.4.0) (account/extensions/draft-AccountERC7579Hooked.sol)
    3 | 
    4 | pragma solidity ^0.8.26;
    5 | 
    6 | import {IERC7579Hook, MODULE_TYPE_HOOK} from "@openzeppelin/contracts/interfaces/draft-IERC7579.sol";
```

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/contracts/account/extensions/draft-AccountERC7579Upgradeable.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/contracts/account/extensions/draft-AccountERC7579Upgradeable.sol#L4) · line 4 · SHA-256 7607a3788222c36039abf8fb51e88ce162b507dd9e527653a35cb26e21afddd8_

```
    2 | // OpenZeppelin Contracts (last updated v5.4.0) (account/extensions/draft-AccountERC7579.sol)
    3 | 
    4 | pragma solidity ^0.8.26;
    5 | 
    6 | import {PackedUserOperation} from "@openzeppelin/contracts/interfaces/draft-IERC4337.sol";
```

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/contracts/utils/cryptography/signers/MultiSignerERC7913Upgradeable.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/contracts/utils/cryptography/signers/MultiSignerERC7913Upgradeable.sol#L4) · line 4 · SHA-256 ebad31ac47b9d001fd41ba60b7b910e2c14cd944f34a741e83436f8c611d7129_

```
    2 | // OpenZeppelin Contracts (last updated v5.4.0) (utils/cryptography/signers/MultiSignerERC7913.sol)
    3 | 
    4 | pragma solidity ^0.8.26;
    5 | 
    6 | import {AbstractSigner} from "@openzeppelin/contracts/utils/cryptography/signers/AbstractSigner.sol";
```

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/contracts/utils/cryptography/signers/MultiSignerERC7913WeightedUpgradeable.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/contracts/utils/cryptography/signers/MultiSignerERC7913WeightedUpgradeable.sol#L4) · line 4 · SHA-256 38605c25420c20a61081f0449f28b48153a67fc440f560e3edcaecc2dc0efc32_

```
    2 | // OpenZeppelin Contracts (last updated v5.4.0) (utils/cryptography/signers/MultiSignerERC7913Weighted.sol)
    3 | 
    4 | pragma solidity ^0.8.26;
    5 | 
    6 | import {SafeCast} from "@openzeppelin/contracts/utils/math/SafeCast.sol";
```

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/account/extensions/draft-AccountERC7579.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/account/extensions/draft-AccountERC7579.sol#L4) · line 4 · SHA-256 f79fee1651a2d42e4961cbb1a739af50a5586a657f5c10364b9acf44b2d464a9_

```
    2 | // OpenZeppelin Contracts (last updated v5.4.0) (account/extensions/draft-AccountERC7579.sol)
    3 | 
    4 | pragma solidity ^0.8.26;
    5 | 
    6 | import {PackedUserOperation} from "../../interfaces/draft-IERC4337.sol";
```

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/account/extensions/draft-AccountERC7579Hooked.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/account/extensions/draft-AccountERC7579Hooked.sol#L4) · line 4 · SHA-256 01723dd7b2303e85d3790f67f93582b89069cc3f52a69697048bbc3a3c1f690f_

```
    2 | // OpenZeppelin Contracts (last updated v5.4.0) (account/extensions/draft-AccountERC7579Hooked.sol)
    3 | 
    4 | pragma solidity ^0.8.26;
    5 | 
    6 | import {IERC7579Hook, MODULE_TYPE_HOOK} from "../../interfaces/draft-IERC7579.sol";
```

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/cryptography/signers/MultiSignerERC7913.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/cryptography/signers/MultiSignerERC7913.sol#L4) · line 4 · SHA-256 39d1e7d402496ad874c7f7438c101eada78e00c19094828271ca5a39e2292101_

```
    2 | // OpenZeppelin Contracts (last updated v5.4.0) (utils/cryptography/signers/MultiSignerERC7913.sol)
    3 | 
    4 | pragma solidity ^0.8.26;
    5 | 
    6 | import {AbstractSigner} from "./AbstractSigner.sol";
```

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/cryptography/signers/MultiSignerERC7913Weighted.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/cryptography/signers/MultiSignerERC7913Weighted.sol#L4) · line 4 · SHA-256 ce5d1947cf5df8a52ee84dcb0e16f460ab69a99c6fac70aab33165da22b19d0e_

```
    2 | // OpenZeppelin Contracts (last updated v5.4.0) (utils/cryptography/signers/MultiSignerERC7913Weighted.sol)
    3 | 
    4 | pragma solidity ^0.8.26;
    5 | 
    6 | import {SafeCast} from "../../math/SafeCast.sol";
```

_file_excerpt · [contracts/lib/openzeppelin-contracts/contracts/account/extensions/draft-AccountERC7579.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts/contracts/account/extensions/draft-AccountERC7579.sol#L4) · line 4 · SHA-256 f79fee1651a2d42e4961cbb1a739af50a5586a657f5c10364b9acf44b2d464a9_

```
    2 | // OpenZeppelin Contracts (last updated v5.4.0) (account/extensions/draft-AccountERC7579.sol)
    3 | 
    4 | pragma solidity ^0.8.26;
    5 | 
    6 | import {PackedUserOperation} from "../../interfaces/draft-IERC4337.sol";
```

_file_excerpt · [contracts/lib/openzeppelin-contracts/contracts/account/extensions/draft-AccountERC7579Hooked.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts/contracts/account/extensions/draft-AccountERC7579Hooked.sol#L4) · line 4 · SHA-256 01723dd7b2303e85d3790f67f93582b89069cc3f52a69697048bbc3a3c1f690f_

```
    2 | // OpenZeppelin Contracts (last updated v5.4.0) (account/extensions/draft-AccountERC7579Hooked.sol)
    3 | 
    4 | pragma solidity ^0.8.26;
    5 | 
    6 | import {IERC7579Hook, MODULE_TYPE_HOOK} from "../../interfaces/draft-IERC7579.sol";
```

**Limitations of the check.** Lightweight static pattern analysis of Solidity source without compilation or symbolic execution. It does not replace a full smart-contract audit; confirm manually or with dedicated tools (Slither, Foundry tests).

**Recommendation.** Pin the compiler version used in testing.

**Retest procedure.** Re-run static analysis and add a unit/fuzz test that exercises the pattern.

### QSI-2026-19430 — Floating pragma (^0.8.24) in 70 file(s)

- Severity: **Low** · Classification: Improvement recommendation · Confidence: High
- Affected asset: `solidity:pragma:^0.8.24`
- Data source: contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/GovernorUpgradeable.sol
- Detection method: Solidity source pattern analysis.
- Analyzer: solidity 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 34.8 / 100
- CVSS v3.1: not applicable

pragma ^0.8.24 in 70 file(s), first at contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/GovernorUpgradeable.sol:4. (related: SWC-103)

**Potential impact.** Contracts may be deployed with untested compiler versions. The compiler actually used is set by the build configuration, which this check does not read.

**Reproduction steps.**

```
Open contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/GovernorUpgradeable.sol:4 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/GovernorUpgradeable.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/GovernorUpgradeable.sol#L4) · line 4 · SHA-256 110868dcdf2d240b04a524ee36b745867c4c7b8f9f73ea04b005ce62e378a5c1_

```
    2 | // OpenZeppelin Contracts (last updated v5.4.0) (governance/Governor.sol)
    3 | 
    4 | pragma solidity ^0.8.24;
    5 | 
    6 | import {IERC721Receiver} from "@openzeppelin/contracts/token/ERC721/IERC721Receiver.sol";
```

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorCountingFractionalUpgradeable.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorCountingFractionalUpgradeable.sol#L4) · line 4 · SHA-256 86e0442c6fa16d0ac3bbb0ea2dd846de6b753aec4bba7182dd70e6507f542dcc_

```
    2 | // OpenZeppelin Contracts (last updated v5.4.0) (governance/extensions/GovernorCountingFractional.sol)
    3 | 
    4 | pragma solidity ^0.8.24;
    5 | 
    6 | import {IGovernor} from "@openzeppelin/contracts/governance/IGovernor.sol";
```

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorCountingOverridableUpgradeable.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorCountingOverridableUpgradeable.sol#L4) · line 4 · SHA-256 bdb8e6161a8909cfc35ed78a2d7d8a62880dc103d980aeaa0a9cfa227bb55692_

```
    2 | // OpenZeppelin Contracts (last updated v5.4.0) (governance/extensions/GovernorCountingOverridable.sol)
    3 | 
    4 | pragma solidity ^0.8.24;
    5 | 
    6 | import {SignatureChecker} from "@openzeppelin/contracts/utils/cryptography/SignatureChecker.sol";
```

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorCountingSimpleUpgradeable.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorCountingSimpleUpgradeable.sol#L4) · line 4 · SHA-256 4454a914a26988a27cc038e3fb2add0ee70857bb60dc9d0a835e3582c5d30f44_

```
    2 | // OpenZeppelin Contracts (last updated v5.4.0) (governance/extensions/GovernorCountingSimple.sol)
    3 | 
    4 | pragma solidity ^0.8.24;
    5 | 
    6 | import {IGovernor} from "@openzeppelin/contracts/governance/IGovernor.sol";
```

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorNoncesKeyedUpgradeable.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorNoncesKeyedUpgradeable.sol#L4) · line 4 · SHA-256 e536a2de91a5a3a8796e436e81a73ca8bca6b094b977528da71fb8b19a73e1d2_

```
    2 | // OpenZeppelin Contracts (last updated v5.4.0) (governance/extensions/GovernorNoncesKeyed.sol)
    3 | 
    4 | pragma solidity ^0.8.24;
    5 | 
    6 | import {GovernorUpgradeable} from "../GovernorUpgradeable.sol";
```

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorPreventLateQuorumUpgradeable.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorPreventLateQuorumUpgradeable.sol#L4) · line 4 · SHA-256 7c84de814498b9dd5ddf63879eca2a4f180bed285b11f59f877b7aff1be767ba_

```
    2 | // OpenZeppelin Contracts (last updated v5.4.0) (governance/extensions/GovernorPreventLateQuorum.sol)
    3 | 
    4 | pragma solidity ^0.8.24;
    5 | 
    6 | import {GovernorUpgradeable} from "../GovernorUpgradeable.sol";
```

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorProposalGuardianUpgradeable.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorProposalGuardianUpgradeable.sol#L3) · line 3 · SHA-256 dd5c48f694fa58ad35b341e11d88aa0e0b820cb4d7f2af6ed182f7fe3d250b55_

```
    1 | // SPDX-License-Identifier: MIT
    2 | // OpenZeppelin Contracts (last updated v5.4.0) (governance/extensions/GovernorProposalGuardian.sol)
    3 | pragma solidity ^0.8.24;
    4 | 
    5 | import {GovernorUpgradeable} from "../GovernorUpgradeable.sol";
```

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorSequentialProposalIdUpgradeable.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorSequentialProposalIdUpgradeable.sol#L4) · line 4 · SHA-256 eacd4e34333aea40ebe0b9c7f683f757699256000bf3a989dc43b3a0606d8357_

```
    2 | // OpenZeppelin Contracts (last updated v5.4.0) (governance/extensions/GovernorSequentialProposalId.sol)
    3 | 
    4 | pragma solidity ^0.8.24;
    5 | 
    6 | import {IGovernor} from "@openzeppelin/contracts/governance/IGovernor.sol";
```

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorSettingsUpgradeable.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorSettingsUpgradeable.sol#L4) · line 4 · SHA-256 ded858f835859b38a2d94267fe0f45d451e889e30d499fecb7067fe89fcffc93_

```
    2 | // OpenZeppelin Contracts (last updated v5.4.0) (governance/extensions/GovernorSettings.sol)
    3 | 
    4 | pragma solidity ^0.8.24;
    5 | 
    6 | import {IGovernor} from "@openzeppelin/contracts/governance/IGovernor.sol";
```

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorStorageUpgradeable.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorStorageUpgradeable.sol#L4) · line 4 · SHA-256 9289493ceb764442978e609362e8a9a11496799dc5be9368480ed4eb0c550659_

```
    2 | // OpenZeppelin Contracts (last updated v5.4.0) (governance/extensions/GovernorStorage.sol)
    3 | 
    4 | pragma solidity ^0.8.24;
    5 | 
    6 | import {GovernorUpgradeable} from "../GovernorUpgradeable.sol";
```

**Limitations of the check.** Lightweight static pattern analysis of Solidity source without compilation or symbolic execution. It does not replace a full smart-contract audit; confirm manually or with dedicated tools (Slither, Foundry tests).

**Recommendation.** Pin the compiler version used in testing.

**Retest procedure.** Re-run static analysis and add a unit/fuzz test that exercises the pattern.

### QSI-2026-19440 — Floating pragma (^0.8.22) in 11 file(s)

- Severity: **Low** · Classification: Improvement recommendation · Confidence: High
- Affected asset: `solidity:pragma:^0.8.22`
- Data source: contracts/lib/openzeppelin-contracts-upgradeable/contracts/proxy/utils/UUPSUpgradeable.sol
- Detection method: Solidity source pattern analysis.
- Analyzer: solidity 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 34.8 / 100
- CVSS v3.1: not applicable

pragma ^0.8.22 in 11 file(s), first at contracts/lib/openzeppelin-contracts-upgradeable/contracts/proxy/utils/UUPSUpgradeable.sol:4. (related: SWC-103)

**Potential impact.** Contracts may be deployed with untested compiler versions. The compiler actually used is set by the build configuration, which this check does not read.

**Reproduction steps.**

```
Open contracts/lib/openzeppelin-contracts-upgradeable/contracts/proxy/utils/UUPSUpgradeable.sol:4 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/contracts/proxy/utils/UUPSUpgradeable.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/contracts/proxy/utils/UUPSUpgradeable.sol#L4) · line 4 · SHA-256 51b7f93f2c4fd2c89014e27a01386d2091067d1c843ce40fba6d6ace7350852b_

```
    2 | // OpenZeppelin Contracts (last updated v5.3.0) (proxy/utils/UUPSUpgradeable.sol)
    3 | 
    4 | pragma solidity ^0.8.22;
    5 | 
    6 | import {IERC1822Proxiable} from "@openzeppelin/contracts/interfaces/draft-IERC1822.sol";
```

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/proxy/ERC1967/ERC1967Proxy.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/proxy/ERC1967/ERC1967Proxy.sol#L4) · line 4 · SHA-256 7adae15fedc454fe7d18b8e2fad3c5e4b48c1902d6b840073c1016836f6e537c_

```
    2 | // OpenZeppelin Contracts (last updated v5.2.0) (proxy/ERC1967/ERC1967Proxy.sol)
    3 | 
    4 | pragma solidity ^0.8.22;
    5 | 
    6 | import {Proxy} from "../Proxy.sol";
```

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/proxy/beacon/BeaconProxy.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/proxy/beacon/BeaconProxy.sol#L4) · line 4 · SHA-256 19558af72f040ec2c4617d6a8ed5ab34a59eafbbf9971b68169088c989dc6cac_

```
    2 | // OpenZeppelin Contracts (last updated v5.2.0) (proxy/beacon/BeaconProxy.sol)
    3 | 
    4 | pragma solidity ^0.8.22;
    5 | 
    6 | import {IBeacon} from "./IBeacon.sol";
```

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/proxy/transparent/ProxyAdmin.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/proxy/transparent/ProxyAdmin.sol#L4) · line 4 · SHA-256 052868c38d31aa073c450d64ff0715428866c19e8e32e2c525efb17bd7732a36_

```
    2 | // OpenZeppelin Contracts (last updated v5.2.0) (proxy/transparent/ProxyAdmin.sol)
    3 | 
    4 | pragma solidity ^0.8.22;
    5 | 
    6 | import {ITransparentUpgradeableProxy} from "./TransparentUpgradeableProxy.sol";
```

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/proxy/transparent/TransparentUpgradeableProxy.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/proxy/transparent/TransparentUpgradeableProxy.sol#L4) · line 4 · SHA-256 a0ab0b407fa84ebb917a03b4f1fffb4cae80fb281e64da12718de700b94381c6_

```
    2 | // OpenZeppelin Contracts (last updated v5.2.0) (proxy/transparent/TransparentUpgradeableProxy.sol)
    3 | 
    4 | pragma solidity ^0.8.22;
    5 | 
    6 | import {ERC1967Utils} from "../ERC1967/ERC1967Utils.sol";
```

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/proxy/utils/UUPSUpgradeable.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/proxy/utils/UUPSUpgradeable.sol#L4) · line 4 · SHA-256 48fa313b14c9a4efe40ece54c8b8e32bfe55583b5817314f68c73c5b85c8af69_

```
    2 | // OpenZeppelin Contracts (last updated v5.3.0) (proxy/utils/UUPSUpgradeable.sol)
    3 | 
    4 | pragma solidity ^0.8.22;
    5 | 
    6 | import {IERC1822Proxiable} from "../../interfaces/draft-IERC1822.sol";
```

_file_excerpt · [contracts/lib/openzeppelin-contracts/contracts/proxy/ERC1967/ERC1967Proxy.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts/contracts/proxy/ERC1967/ERC1967Proxy.sol#L4) · line 4 · SHA-256 7adae15fedc454fe7d18b8e2fad3c5e4b48c1902d6b840073c1016836f6e537c_

```
    2 | // OpenZeppelin Contracts (last updated v5.2.0) (proxy/ERC1967/ERC1967Proxy.sol)
    3 | 
    4 | pragma solidity ^0.8.22;
    5 | 
    6 | import {Proxy} from "../Proxy.sol";
```

_file_excerpt · [contracts/lib/openzeppelin-contracts/contracts/proxy/beacon/BeaconProxy.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts/contracts/proxy/beacon/BeaconProxy.sol#L4) · line 4 · SHA-256 19558af72f040ec2c4617d6a8ed5ab34a59eafbbf9971b68169088c989dc6cac_

```
    2 | // OpenZeppelin Contracts (last updated v5.2.0) (proxy/beacon/BeaconProxy.sol)
    3 | 
    4 | pragma solidity ^0.8.22;
    5 | 
    6 | import {IBeacon} from "./IBeacon.sol";
```

_file_excerpt · [contracts/lib/openzeppelin-contracts/contracts/proxy/transparent/ProxyAdmin.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts/contracts/proxy/transparent/ProxyAdmin.sol#L4) · line 4 · SHA-256 052868c38d31aa073c450d64ff0715428866c19e8e32e2c525efb17bd7732a36_

```
    2 | // OpenZeppelin Contracts (last updated v5.2.0) (proxy/transparent/ProxyAdmin.sol)
    3 | 
    4 | pragma solidity ^0.8.22;
    5 | 
    6 | import {ITransparentUpgradeableProxy} from "./TransparentUpgradeableProxy.sol";
```

_file_excerpt · [contracts/lib/openzeppelin-contracts/contracts/proxy/transparent/TransparentUpgradeableProxy.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts/contracts/proxy/transparent/TransparentUpgradeableProxy.sol#L4) · line 4 · SHA-256 a0ab0b407fa84ebb917a03b4f1fffb4cae80fb281e64da12718de700b94381c6_

```
    2 | // OpenZeppelin Contracts (last updated v5.2.0) (proxy/transparent/TransparentUpgradeableProxy.sol)
    3 | 
    4 | pragma solidity ^0.8.22;
    5 | 
    6 | import {ERC1967Utils} from "../ERC1967/ERC1967Utils.sol";
```

**Limitations of the check.** Lightweight static pattern analysis of Solidity source without compilation or symbolic execution. It does not replace a full smart-contract audit; confirm manually or with dedicated tools (Slither, Foundry tests).

**Recommendation.** Pin the compiler version used in testing.

**Retest procedure.** Re-run static analysis and add a unit/fuzz test that exercises the pattern.

### QSI-2026-19442 — Floating pragma (>=0.8.0 <0.9.0) in 6 file(s)

- Severity: **Low** · Classification: Improvement recommendation · Confidence: High
- Affected asset: `solidity:pragma:>=0.8.0 <0.9.0`
- Data source: contracts/lib/openzeppelin-contracts-upgradeable/lib/halmos-cheatcodes/src/SVM.sol
- Detection method: Solidity source pattern analysis.
- Analyzer: solidity 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 34.8 / 100
- CVSS v3.1: not applicable

pragma >=0.8.0 <0.9.0 in 6 file(s), first at contracts/lib/openzeppelin-contracts-upgradeable/lib/halmos-cheatcodes/src/SVM.sol:2. (related: SWC-103)

**Potential impact.** Contracts may be deployed with untested compiler versions. The compiler actually used is set by the build configuration, which this check does not read.

**Reproduction steps.**

```
Open contracts/lib/openzeppelin-contracts-upgradeable/lib/halmos-cheatcodes/src/SVM.sol:2 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/lib/halmos-cheatcodes/src/SVM.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/lib/halmos-cheatcodes/src/SVM.sol#L2) · line 2 · SHA-256 bd471efc2f4d7d423e928467267caaddb41788dd0f77dd12ceceaf88d979eed2_

```
    1 | // SPDX-License-Identifier: AGPL-3.0
    2 | pragma solidity >=0.8.0 <0.9.0;
    3 | 
    4 | /// @notice Symbolic Virtual Machine
```

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/lib/halmos-cheatcodes/src/SymTest.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/lib/halmos-cheatcodes/src/SymTest.sol#L2) · line 2 · SHA-256 97630b16a584af991c523a19d6304c66e9d3e30b64896278317489cf5453873b_

```
    1 | // SPDX-License-Identifier: AGPL-3.0
    2 | pragma solidity >=0.8.0 <0.9.0;
    3 | 
    4 | import {SVM} from "./SVM.sol";
```

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/lib/halmos-cheatcodes/src/SVM.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/lib/halmos-cheatcodes/src/SVM.sol#L2) · line 2 · SHA-256 bd471efc2f4d7d423e928467267caaddb41788dd0f77dd12ceceaf88d979eed2_

```
    1 | // SPDX-License-Identifier: AGPL-3.0
    2 | pragma solidity >=0.8.0 <0.9.0;
    3 | 
    4 | /// @notice Symbolic Virtual Machine
```

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/lib/halmos-cheatcodes/src/SymTest.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/lib/halmos-cheatcodes/src/SymTest.sol#L2) · line 2 · SHA-256 97630b16a584af991c523a19d6304c66e9d3e30b64896278317489cf5453873b_

```
    1 | // SPDX-License-Identifier: AGPL-3.0
    2 | pragma solidity >=0.8.0 <0.9.0;
    3 | 
    4 | import {SVM} from "./SVM.sol";
```

_file_excerpt · [contracts/lib/openzeppelin-contracts/lib/halmos-cheatcodes/src/SVM.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts/lib/halmos-cheatcodes/src/SVM.sol#L2) · line 2 · SHA-256 bd471efc2f4d7d423e928467267caaddb41788dd0f77dd12ceceaf88d979eed2_

```
    1 | // SPDX-License-Identifier: AGPL-3.0
    2 | pragma solidity >=0.8.0 <0.9.0;
    3 | 
    4 | /// @notice Symbolic Virtual Machine
```

_file_excerpt · [contracts/lib/openzeppelin-contracts/lib/halmos-cheatcodes/src/SymTest.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts/lib/halmos-cheatcodes/src/SymTest.sol#L2) · line 2 · SHA-256 97630b16a584af991c523a19d6304c66e9d3e30b64896278317489cf5453873b_

```
    1 | // SPDX-License-Identifier: AGPL-3.0
    2 | pragma solidity >=0.8.0 <0.9.0;
    3 | 
    4 | import {SVM} from "./SVM.sol";
```

**Limitations of the check.** Lightweight static pattern analysis of Solidity source without compilation or symbolic execution. It does not replace a full smart-contract audit; confirm manually or with dedicated tools (Slither, Foundry tests).

**Recommendation.** Pin the compiler version used in testing.

**Retest procedure.** Re-run static analysis and add a unit/fuzz test that exercises the pattern.

### QSI-2026-19445 — Floating pragma (>=0.8.4) in 22 file(s)

- Severity: **Low** · Classification: Improvement recommendation · Confidence: High
- Affected asset: `solidity:pragma:>=0.8.4`
- Data source: contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/access/IAccessControl.sol
- Detection method: Solidity source pattern analysis.
- Analyzer: solidity 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 34.8 / 100
- CVSS v3.1: not applicable

pragma >=0.8.4 in 22 file(s), first at contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/access/IAccessControl.sol:4. (related: SWC-103)

**Potential impact.** Contracts may be deployed with untested compiler versions. The compiler actually used is set by the build configuration, which this check does not read.

**Reproduction steps.**

```
Open contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/access/IAccessControl.sol:4 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/access/IAccessControl.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/access/IAccessControl.sol#L4) · line 4 · SHA-256 23e7d8c92d03f6bff5ad665a9628ccf99a1fbd2c8518315998d386ef1323efac_

```
    2 | // OpenZeppelin Contracts (last updated v5.4.0) (access/IAccessControl.sol)
    3 | 
    4 | pragma solidity >=0.8.4;
    5 | 
    6 | /**
```

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/access/extensions/IAccessControlDefaultAdminRules.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/access/extensions/IAccessControlDefaultAdminRules.sol#L4) · line 4 · SHA-256 96400a8a52df4007d6a7593b1b0be6dbc3f6a5abc698eca9ff7c53364c95d3cf_

```
    2 | // OpenZeppelin Contracts (last updated v5.4.0) (access/extensions/IAccessControlDefaultAdminRules.sol)
    3 | 
    4 | pragma solidity >=0.8.4;
    5 | 
    6 | import {IAccessControl} from "../IAccessControl.sol";
```

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/access/extensions/IAccessControlEnumerable.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/access/extensions/IAccessControlEnumerable.sol#L4) · line 4 · SHA-256 75556f8db0a186ce0a66b1b5240e24b517d812fb0b35aa13be728c34ec167058_

```
    2 | // OpenZeppelin Contracts (last updated v5.4.0) (access/extensions/IAccessControlEnumerable.sol)
    3 | 
    4 | pragma solidity >=0.8.4;
    5 | 
    6 | import {IAccessControl} from "../IAccessControl.sol";
```

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/access/manager/IAccessManaged.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/access/manager/IAccessManaged.sol#L4) · line 4 · SHA-256 9c08e8da31027518b308530215396f93af24a7d744c2a8e6e1a6d37d2f6765ca_

```
    2 | // OpenZeppelin Contracts (last updated v5.4.0) (access/manager/IAccessManaged.sol)
    3 | 
    4 | pragma solidity >=0.8.4;
    5 | 
    6 | interface IAccessManaged {
```

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/access/manager/IAccessManager.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/access/manager/IAccessManager.sol#L4) · line 4 · SHA-256 d28fa18895fb37d698e2114a3f9647ecb0fbac5b691a7721b42e907fa69616ef_

```
    2 | // OpenZeppelin Contracts (last updated v5.4.0) (access/manager/IAccessManager.sol)
    3 | 
    4 | pragma solidity >=0.8.4;
    5 | 
    6 | interface IAccessManager {
```

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/IGovernor.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/IGovernor.sol#L4) · line 4 · SHA-256 b81914f14753db894afe128eb575dd1b9fe9d5c46039a15c867534193abccc45_

```
    2 | // OpenZeppelin Contracts (last updated v5.4.0) (governance/IGovernor.sol)
    3 | 
    4 | pragma solidity >=0.8.4;
    5 | 
    6 | import {IERC165} from "../interfaces/IERC165.sol";
```

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/utils/IVotes.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/utils/IVotes.sol#L3) · line 3 · SHA-256 2d7fa19d01382e1f39025c59254c6e8b0b5ac5f674f664c7a8aba67121454811_

```
    1 | // SPDX-License-Identifier: MIT
    2 | // OpenZeppelin Contracts (last updated v5.4.0) (governance/utils/IVotes.sol)
    3 | pragma solidity >=0.8.4;
    4 | 
    5 | /**
```

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC5805.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC5805.sol#L4) · line 4 · SHA-256 3dc3349505a2b221ebeb2f6bf38d734f18a44cb5bcb9a7c8ba9ecad7e7a12cf7_

```
    2 | // OpenZeppelin Contracts (last updated v5.4.0) (interfaces/IERC5805.sol)
    3 | 
    4 | pragma solidity >=0.8.4;
    5 | 
    6 | import {IVotes} from "../governance/utils/IVotes.sol";
```

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/draft-IERC4337.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/draft-IERC4337.sol#L4) · line 4 · SHA-256 d17bdd715fea647ade8e58dbb8d6db44eabd38b83cfc07e6bd35a2aa6480d3c0_

```
    2 | // OpenZeppelin Contracts (last updated v5.4.0) (interfaces/draft-IERC4337.sol)
    3 | 
    4 | pragma solidity >=0.8.4;
    5 | 
    6 | /**
```

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/draft-IERC6093.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/draft-IERC6093.sol#L3) · line 3 · SHA-256 5d815c4a9d35069b852fa8680de4a927fad2efe4e16a06ba93d483ed3dbc31f8_

```
    1 | // SPDX-License-Identifier: MIT
    2 | // OpenZeppelin Contracts (last updated v5.4.0) (interfaces/draft-IERC6093.sol)
    3 | pragma solidity >=0.8.4;
    4 | 
    5 | /**
```

**Limitations of the check.** Lightweight static pattern analysis of Solidity source without compilation or symbolic execution. It does not replace a full smart-contract audit; confirm manually or with dedicated tools (Slither, Foundry tests).

**Recommendation.** Pin the compiler version used in testing.

**Retest procedure.** Re-run static analysis and add a unit/fuzz test that exercises the pattern.

### QSI-2026-19448 — Floating pragma (>=0.4.16) in 24 file(s)

- Severity: **Low** · Classification: Improvement recommendation · Confidence: High
- Affected asset: `solidity:pragma:>=0.4.16`
- Data source: contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/access/manager/IAuthority.sol
- Detection method: Solidity source pattern analysis.
- Analyzer: solidity 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 34.8 / 100
- CVSS v3.1: not applicable

pragma >=0.4.16 in 24 file(s), first at contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/access/manager/IAuthority.sol:4. (related: SWC-103)

**Potential impact.** Contracts may be deployed with untested compiler versions. The compiler actually used is set by the build configuration, which this check does not read.

**Reproduction steps.**

```
Open contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/access/manager/IAuthority.sol:4 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/access/manager/IAuthority.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/access/manager/IAuthority.sol#L4) · line 4 · SHA-256 4ccb3824a219e881342151d513fd570a985805e45f8134da6e03d4ec66c37aa1_

```
    2 | // OpenZeppelin Contracts (last updated v5.4.0) (access/manager/IAuthority.sol)
    3 | 
    4 | pragma solidity >=0.4.16;
    5 | 
    6 | /**
```

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC165.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC165.sol#L4) · line 4 · SHA-256 f9edce89b01b34aa894800ef3fa3073cc4b0436b50baa26e7d613240d8322a97_

```
    2 | // OpenZeppelin Contracts (last updated v5.4.0) (interfaces/IERC165.sol)
    3 | 
    4 | pragma solidity >=0.4.16;
    5 | 
    6 | import {IERC165} from "../utils/introspection/IERC165.sol";
```

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC1820Implementer.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC1820Implementer.sol#L4) · line 4 · SHA-256 90e19e192797c701ec2db43e0080d0ceb11bd31377f88720e2e76f082a487867_

```
    2 | // OpenZeppelin Contracts (last updated v5.4.0) (interfaces/IERC1820Implementer.sol)
    3 | 
    4 | pragma solidity >=0.4.16;
    5 | 
    6 | /**
```

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC20.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC20.sol#L4) · line 4 · SHA-256 10d1b8a3c3afc59652beebb8fe83afe9dc8fa660a61e100fd154a51dfe373155_

```
    2 | // OpenZeppelin Contracts (last updated v5.4.0) (interfaces/IERC20.sol)
    3 | 
    4 | pragma solidity >=0.4.16;
    5 | 
    6 | import {IERC20} from "../token/ERC20/IERC20.sol";
```

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC5267.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC5267.sol#L4) · line 4 · SHA-256 c945bb5ab2bfe8966a53c06a1d17e19411dfd30e0104a10be9a92f361a4c2ae7_

```
    2 | // OpenZeppelin Contracts (last updated v5.4.0) (interfaces/IERC5267.sol)
    3 | 
    4 | pragma solidity >=0.4.16;
    5 | 
    6 | interface IERC5267 {
```

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC5313.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC5313.sol#L4) · line 4 · SHA-256 aebdd32a48c284a91c895b97fb18d7df2ea1a686de935fb1670b601b62b5b4ce_

```
    2 | // OpenZeppelin Contracts (last updated v5.4.0) (interfaces/IERC5313.sol)
    3 | 
    4 | pragma solidity >=0.4.16;
    5 | 
    6 | /**
```

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC6372.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC6372.sol#L4) · line 4 · SHA-256 c672a1ab55a27f6b879faf23b7a896ea3031e4d2e3b4cf3cd2f4d704319e3ae1_

```
    2 | // OpenZeppelin Contracts (last updated v5.4.0) (interfaces/IERC6372.sol)
    3 | 
    4 | pragma solidity >=0.4.16;
    5 | 
    6 | interface IERC6372 {
```

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/draft-IERC1822.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/draft-IERC1822.sol#L4) · line 4 · SHA-256 a9c6cede38f2575457213411cfc96039b7839c78a25af87fe8b87c382625ba65_

```
    2 | // OpenZeppelin Contracts (last updated v5.4.0) (interfaces/draft-IERC1822.sol)
    3 | 
    4 | pragma solidity >=0.4.16;
    5 | 
    6 | /**
```

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/proxy/beacon/IBeacon.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/proxy/beacon/IBeacon.sol#L4) · line 4 · SHA-256 0ac512b6beb2e5185427fdefea7e79f7a825a2b52bb31b52762702152f2f3fde_

```
    2 | // OpenZeppelin Contracts (last updated v5.4.0) (proxy/beacon/IBeacon.sol)
    3 | 
    4 | pragma solidity >=0.4.16;
    5 | 
    6 | /**
```

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC20/IERC20.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC20/IERC20.sol#L4) · line 4 · SHA-256 2c0336249aad455845b2389e325e16bec0f3fe1cdbfe7217b1b74414ed4afc7f_

```
    2 | // OpenZeppelin Contracts (last updated v5.4.0) (token/ERC20/IERC20.sol)
    3 | 
    4 | pragma solidity >=0.4.16;
    5 | 
    6 | /**
```

**Limitations of the check.** Lightweight static pattern analysis of Solidity source without compilation or symbolic execution. It does not replace a full smart-contract audit; confirm manually or with dedicated tools (Slither, Foundry tests).

**Recommendation.** Pin the compiler version used in testing.

**Retest procedure.** Re-run static analysis and add a unit/fuzz test that exercises the pattern.

### QSI-2026-19459 — Floating pragma (>=0.6.2) in 44 file(s)

- Severity: **Low** · Classification: Improvement recommendation · Confidence: High
- Affected asset: `solidity:pragma:>=0.6.2`
- Data source: contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC1155.sol
- Detection method: Solidity source pattern analysis.
- Analyzer: solidity 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 34.8 / 100
- CVSS v3.1: not applicable

pragma >=0.6.2 in 44 file(s), first at contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC1155.sol:4. (related: SWC-103)

**Potential impact.** Contracts may be deployed with untested compiler versions. The compiler actually used is set by the build configuration, which this check does not read.

**Reproduction steps.**

```
Open contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC1155.sol:4 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC1155.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC1155.sol#L4) · line 4 · SHA-256 dfad9a7c3626bba385b5f4d08f81ed1d81cc36b4d1cb98982357a01cd7b3088d_

```
    2 | // OpenZeppelin Contracts (last updated v5.4.0) (interfaces/IERC1155.sol)
    3 | 
    4 | pragma solidity >=0.6.2;
    5 | 
    6 | import {IERC1155} from "../token/ERC1155/IERC1155.sol";
```

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC1155MetadataURI.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC1155MetadataURI.sol#L4) · line 4 · SHA-256 747195b68051040181c142d8dad51aa94d7ad2ac3b6c89f6b871d46901757a6a_

```
    2 | // OpenZeppelin Contracts (last updated v5.4.0) (interfaces/IERC1155MetadataURI.sol)
    3 | 
    4 | pragma solidity >=0.6.2;
    5 | 
    6 | import {IERC1155MetadataURI} from "../token/ERC1155/extensions/IERC1155MetadataURI.sol";
```

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC1155Receiver.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC1155Receiver.sol#L4) · line 4 · SHA-256 ba575cd74504fdd21e05902631f34f04ecdfc21f2dc21cd807519f1a9911c902_

```
    2 | // OpenZeppelin Contracts (last updated v5.4.0) (interfaces/IERC1155Receiver.sol)
    3 | 
    4 | pragma solidity >=0.6.2;
    5 | 
    6 | import {IERC1155Receiver} from "../token/ERC1155/IERC1155Receiver.sol";
```

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC1363.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC1363.sol#L4) · line 4 · SHA-256 0ae7b1530694970bb44b9fd90939bba9bcd218c633d3ea37a7666e31b93bfe82_

```
    2 | // OpenZeppelin Contracts (last updated v5.4.0) (interfaces/IERC1363.sol)
    3 | 
    4 | pragma solidity >=0.6.2;
    5 | 
    6 | import {IERC20} from "./IERC20.sol";
```

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC20Metadata.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC20Metadata.sol#L4) · line 4 · SHA-256 722abdc20b3aed62edb98224660ceda46fbeeec7ab1a0bd3df1bec08de9f6e10_

```
    2 | // OpenZeppelin Contracts (last updated v5.4.0) (interfaces/IERC20Metadata.sol)
    3 | 
    4 | pragma solidity >=0.6.2;
    5 | 
    6 | import {IERC20Metadata} from "../token/ERC20/extensions/IERC20Metadata.sol";
```

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC2612.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC2612.sol#L4) · line 4 · SHA-256 d6d9aefd47b64b6f1cc632539477a628f63b71a3511e725906c017dac6bb971f_

```
    2 | // OpenZeppelin Contracts (last updated v5.4.0) (interfaces/IERC2612.sol)
    3 | 
    4 | pragma solidity >=0.6.2;
    5 | 
    6 | import {IERC20Permit} from "../token/ERC20/extensions/IERC20Permit.sol";
```

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC2981.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC2981.sol#L4) · line 4 · SHA-256 53750e4f38b884d1d3c2bd7cb9abb36d887dfb103edc30fc4a61d0cc4de2d2ef_

```
    2 | // OpenZeppelin Contracts (last updated v5.4.0) (interfaces/IERC2981.sol)
    3 | 
    4 | pragma solidity >=0.6.2;
    5 | 
    6 | import {IERC165} from "../utils/introspection/IERC165.sol";
```

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC4626.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC4626.sol#L4) · line 4 · SHA-256 b3a2a0351e191c43fefae23dfed92b09f0bfc47b51e713f8bda036b93cec222b_

```
    2 | // OpenZeppelin Contracts (last updated v5.4.0) (interfaces/IERC4626.sol)
    3 | 
    4 | pragma solidity >=0.6.2;
    5 | 
    6 | import {IERC20} from "../token/ERC20/IERC20.sol";
```

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC4906.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC4906.sol#L4) · line 4 · SHA-256 e2ee6d31e713881f491922e294cf49bf7859c7eef1e473f395ebff9b80427c5d_

```
    2 | // OpenZeppelin Contracts (last updated v5.4.0) (interfaces/IERC4906.sol)
    3 | 
    4 | pragma solidity >=0.6.2;
    5 | 
    6 | import {IERC165} from "./IERC165.sol";
```

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC721.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC721.sol#L4) · line 4 · SHA-256 3975ec1ecd5890fa0f13a4faac39703402ec0af4aa99790db0a6c850d35408e7_

```
    2 | // OpenZeppelin Contracts (last updated v5.4.0) (interfaces/IERC721.sol)
    3 | 
    4 | pragma solidity >=0.6.2;
    5 | 
    6 | import {IERC721} from "../token/ERC721/IERC721.sol";
```

**Limitations of the check.** Lightweight static pattern analysis of Solidity source without compilation or symbolic execution. It does not replace a full smart-contract audit; confirm manually or with dedicated tools (Slither, Foundry tests).

**Recommendation.** Pin the compiler version used in testing.

**Retest procedure.** Re-run static analysis and add a unit/fuzz test that exercises the pattern.

### QSI-2026-19460 — Floating pragma (>=0.5.0) in 28 file(s)

- Severity: **Low** · Classification: Improvement recommendation · Confidence: High
- Affected asset: `solidity:pragma:>=0.5.0`
- Data source: contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC1271.sol
- Detection method: Solidity source pattern analysis.
- Analyzer: solidity 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 34.8 / 100
- CVSS v3.1: not applicable

pragma >=0.5.0 in 28 file(s), first at contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC1271.sol:4. (related: SWC-103)

**Potential impact.** Contracts may be deployed with untested compiler versions. The compiler actually used is set by the build configuration, which this check does not read.

**Reproduction steps.**

```
Open contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC1271.sol:4 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC1271.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC1271.sol#L4) · line 4 · SHA-256 f2bacab150c87c9cfea74e814ce65bae34fa0412ab6732e65f3e72e281f893b1_

```
    2 | // OpenZeppelin Contracts (last updated v5.4.0) (interfaces/IERC1271.sol)
    3 | 
    4 | pragma solidity >=0.5.0;
    5 | 
    6 | /**
```

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC1363Receiver.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC1363Receiver.sol#L4) · line 4 · SHA-256 4f068aab542c1592d906da9e43036d3f3db506836f9a00e1db63229bb49474c7_

```
    2 | // OpenZeppelin Contracts (last updated v5.4.0) (interfaces/IERC1363Receiver.sol)
    3 | 
    4 | pragma solidity >=0.5.0;
    5 | 
    6 | /**
```

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC1363Spender.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC1363Spender.sol#L4) · line 4 · SHA-256 485ea05476fc90f70bb54f0957581f5788b630d79b5ed81df81c453500715bad_

```
    2 | // OpenZeppelin Contracts (last updated v5.4.0) (interfaces/IERC1363Spender.sol)
    3 | 
    4 | pragma solidity >=0.5.0;
    5 | 
    6 | /**
```

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC1820Registry.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC1820Registry.sol#L4) · line 4 · SHA-256 40b939f3fb746c2c9b91ef40155d8878613d75843e609ae4f111033d35309fe7_

```
    2 | // OpenZeppelin Contracts (last updated v5.4.0) (interfaces/IERC1820Registry.sol)
    3 | 
    4 | pragma solidity >=0.5.0;
    5 | 
    6 | /**
```

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC3156.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC3156.sol#L4) · line 4 · SHA-256 0b8a00ecd164f2e583d806a567e9b10bc3ddecad59f491d31f25de3c14af4868_

```
    2 | // OpenZeppelin Contracts (last updated v5.4.0) (interfaces/IERC3156.sol)
    3 | 
    4 | pragma solidity >=0.5.0;
    5 | 
    6 | import {IERC3156FlashBorrower} from "./IERC3156FlashBorrower.sol";
```

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC3156FlashBorrower.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC3156FlashBorrower.sol#L4) · line 4 · SHA-256 b81bda4c830c16f632c80224092dacf0c06511c033b73ec4333ce4a0cad09f1a_

```
    2 | // OpenZeppelin Contracts (last updated v5.4.0) (interfaces/IERC3156FlashBorrower.sol)
    3 | 
    4 | pragma solidity >=0.5.0;
    5 | 
    6 | /**
```

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC3156FlashLender.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC3156FlashLender.sol#L4) · line 4 · SHA-256 dcb834116e3eee956960030ceb40fb2080f3c2905d07ea06936a7d08ad3251f8_

```
    2 | // OpenZeppelin Contracts (last updated v5.4.0) (interfaces/IERC3156FlashLender.sol)
    3 | 
    4 | pragma solidity >=0.5.0;
    5 | 
    6 | import {IERC3156FlashBorrower} from "./IERC3156FlashBorrower.sol";
```

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC721Receiver.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC721Receiver.sol#L4) · line 4 · SHA-256 cb571bbb05af940bb2c85ae627acf089fc7af97a1fe63c079f51147ad248cb8b_

```
    2 | // OpenZeppelin Contracts (last updated v5.4.0) (interfaces/IERC721Receiver.sol)
    3 | 
    4 | pragma solidity >=0.5.0;
    5 | 
    6 | import {IERC721Receiver} from "../token/ERC721/IERC721Receiver.sol";
```

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC777.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC777.sol#L4) · line 4 · SHA-256 42f670948a09c75454999975a10e63222a9923ac7c02a250bd51872822396913_

```
    2 | // OpenZeppelin Contracts (last updated v5.4.0) (interfaces/IERC777.sol)
    3 | 
    4 | pragma solidity >=0.5.0;
    5 | 
    6 | /**
```

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC777Recipient.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC777Recipient.sol#L4) · line 4 · SHA-256 ae2a8cb30d4432227b660192824f615f39fee4d56463f5d8ab1cd7a6c6d83210_

```
    2 | // OpenZeppelin Contracts (last updated v5.4.0) (interfaces/IERC777Recipient.sol)
    3 | 
    4 | pragma solidity >=0.5.0;
    5 | 
    6 | /**
```

**Limitations of the check.** Lightweight static pattern analysis of Solidity source without compilation or symbolic execution. It does not replace a full smart-contract audit; confirm manually or with dedicated tools (Slither, Foundry tests).

**Recommendation.** Pin the compiler version used in testing.

**Retest procedure.** Re-run static analysis and add a unit/fuzz test that exercises the pattern.

### QSI-2026-19461 — Floating pragma (>=0.4.11) in 4 file(s)

- Severity: **Low** · Classification: Improvement recommendation · Confidence: High
- Affected asset: `solidity:pragma:>=0.4.11`
- Data source: contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC1967.sol
- Detection method: Solidity source pattern analysis.
- Analyzer: solidity 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 34.8 / 100
- CVSS v3.1: not applicable

pragma >=0.4.11 in 4 file(s), first at contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC1967.sol:4. (related: SWC-103)

**Potential impact.** Contracts may be deployed with untested compiler versions. The compiler actually used is set by the build configuration, which this check does not read.

**Reproduction steps.**

```
Open contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC1967.sol:4 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC1967.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC1967.sol#L4) · line 4 · SHA-256 0fa068eab3436c2f8fe905a9533f3a048cdf431d277bf6e08be4b70a2ddda220_

```
    2 | // OpenZeppelin Contracts (last updated v5.4.0) (interfaces/IERC1967.sol)
    3 | 
    4 | pragma solidity >=0.4.11;
    5 | 
    6 | /**
```

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC2309.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC2309.sol#L4) · line 4 · SHA-256 67cd5ff60e6832d750865c0d8b2bb32e5bd44fb48883d5894a3c4b48ee6a29b4_

```
    2 | // OpenZeppelin Contracts (last updated v5.4.0) (interfaces/IERC2309.sol)
    3 | 
    4 | pragma solidity >=0.4.11;
    5 | 
    6 | /**
```

_file_excerpt · [contracts/lib/openzeppelin-contracts/contracts/interfaces/IERC1967.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts/contracts/interfaces/IERC1967.sol#L4) · line 4 · SHA-256 0fa068eab3436c2f8fe905a9533f3a048cdf431d277bf6e08be4b70a2ddda220_

```
    2 | // OpenZeppelin Contracts (last updated v5.4.0) (interfaces/IERC1967.sol)
    3 | 
    4 | pragma solidity >=0.4.11;
    5 | 
    6 | /**
```

_file_excerpt · [contracts/lib/openzeppelin-contracts/contracts/interfaces/IERC2309.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts/contracts/interfaces/IERC2309.sol#L4) · line 4 · SHA-256 67cd5ff60e6832d750865c0d8b2bb32e5bd44fb48883d5894a3c4b48ee6a29b4_

```
    2 | // OpenZeppelin Contracts (last updated v5.4.0) (interfaces/IERC2309.sol)
    3 | 
    4 | pragma solidity >=0.4.11;
    5 | 
    6 | /**
```

**Limitations of the check.** Lightweight static pattern analysis of Solidity source without compilation or symbolic execution. It does not replace a full smart-contract audit; confirm manually or with dedicated tools (Slither, Foundry tests).

**Recommendation.** Pin the compiler version used in testing.

**Retest procedure.** Re-run static analysis and add a unit/fuzz test that exercises the pattern.

### QSI-2026-19462 — Floating pragma (^0.8.21) in 2 file(s)

- Severity: **Low** · Classification: Improvement recommendation · Confidence: High
- Affected asset: `solidity:pragma:^0.8.21`
- Data source: contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/proxy/ERC1967/ERC1967Utils.sol
- Detection method: Solidity source pattern analysis.
- Analyzer: solidity 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 34.8 / 100
- CVSS v3.1: not applicable

pragma ^0.8.21 in 2 file(s), first at contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/proxy/ERC1967/ERC1967Utils.sol:4. (related: SWC-103)

**Potential impact.** Contracts may be deployed with untested compiler versions. The compiler actually used is set by the build configuration, which this check does not read.

**Reproduction steps.**

```
Open contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/proxy/ERC1967/ERC1967Utils.sol:4 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/proxy/ERC1967/ERC1967Utils.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/proxy/ERC1967/ERC1967Utils.sol#L4) · line 4 · SHA-256 e64a735b005a914c363744d11a5476987b5ff999b943817102880932e4781bc4_

```
    2 | // OpenZeppelin Contracts (last updated v5.4.0) (proxy/ERC1967/ERC1967Utils.sol)
    3 | 
    4 | pragma solidity ^0.8.21;
    5 | 
    6 | import {IBeacon} from "../beacon/IBeacon.sol";
```

_file_excerpt · [contracts/lib/openzeppelin-contracts/contracts/proxy/ERC1967/ERC1967Utils.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts/contracts/proxy/ERC1967/ERC1967Utils.sol#L4) · line 4 · SHA-256 e64a735b005a914c363744d11a5476987b5ff999b943817102880932e4781bc4_

```
    2 | // OpenZeppelin Contracts (last updated v5.4.0) (proxy/ERC1967/ERC1967Utils.sol)
    3 | 
    4 | pragma solidity ^0.8.21;
    5 | 
    6 | import {IBeacon} from "../beacon/IBeacon.sol";
```

**Limitations of the check.** Lightweight static pattern analysis of Solidity source without compilation or symbolic execution. It does not replace a full smart-contract audit; confirm manually or with dedicated tools (Slither, Foundry tests).

**Recommendation.** Pin the compiler version used in testing.

**Retest procedure.** Re-run static analysis and add a unit/fuzz test that exercises the pattern.

### QSI-2026-19467 — Floating pragma (>=0.6.9) in 2 file(s)

- Severity: **Low** · Classification: Improvement recommendation · Confidence: High
- Affected asset: `solidity:pragma:>=0.6.9`
- Data source: contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/vendor/compound/ICompoundTimelock.sol
- Detection method: Solidity source pattern analysis.
- Analyzer: solidity 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 34.8 / 100
- CVSS v3.1: not applicable

pragma >=0.6.9 in 2 file(s), first at contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/vendor/compound/ICompoundTimelock.sol:4. (related: SWC-103)

**Potential impact.** Contracts may be deployed with untested compiler versions. The compiler actually used is set by the build configuration, which this check does not read.

**Reproduction steps.**

```
Open contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/vendor/compound/ICompoundTimelock.sol:4 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/vendor/compound/ICompoundTimelock.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/vendor/compound/ICompoundTimelock.sol#L4) · line 4 · SHA-256 ffd60d39b3c4e53b95e2a718e2044ab5dd54c418f024748efc3c41a36c776e8d_

```
    2 | // OpenZeppelin Contracts (last updated v5.4.0) (vendor/compound/ICompoundTimelock.sol)
    3 | 
    4 | pragma solidity >=0.6.9;
    5 | 
    6 | /**
```

_file_excerpt · [contracts/lib/openzeppelin-contracts/contracts/vendor/compound/ICompoundTimelock.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts/contracts/vendor/compound/ICompoundTimelock.sol#L4) · line 4 · SHA-256 ffd60d39b3c4e53b95e2a718e2044ab5dd54c418f024748efc3c41a36c776e8d_

```
    2 | // OpenZeppelin Contracts (last updated v5.4.0) (vendor/compound/ICompoundTimelock.sol)
    3 | 
    4 | pragma solidity >=0.6.9;
    5 | 
    6 | /**
```

**Limitations of the check.** Lightweight static pattern analysis of Solidity source without compilation or symbolic execution. It does not replace a full smart-contract audit; confirm manually or with dedicated tools (Slither, Foundry tests).

**Recommendation.** Pin the compiler version used in testing.

**Retest procedure.** Re-run static analysis and add a unit/fuzz test that exercises the pattern.

### QSI-2026-19513 — openssl 0.10.75 is affected by GHSA-xmgf-hq76-4vx2 (CVE-2026-41677)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low
- Affected asset: `dependency:crates.io/openssl@0.10.75`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 29.4 / 100
- CVSS v3.1: not applicable

OSV.dev reports GHSA-xmgf-hq76-4vx2 (CVE-2026-41677) for crates.io package openssl at version 0.10.75: rust-opennssl has an Out-of-bounds read in PEM password callback when returning an oversized length. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-xmgf-hq76-4vx2
```

**Evidence.**

_tool_output · [OSV.dev GHSA-xmgf-hq76-4vx2](https://osv.dev/vulnerability/GHSA-xmgf-hq76-4vx2) · manifest · SHA-256 b6d4ab0e724d8f8f0247292f16da1b84ad084b001c95214604692899f6df5f58_

```
{"id": "GHSA-xmgf-hq76-4vx2", "aliases": ["CVE-2026-41677"], "modified": "2026-09-10T03:50:44.840710191Z", "summary": "rust-opennssl has an Out-of-bounds read in PEM password callback when returning an oversized length", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:L/VI:N/VA:L/SC:N/SI:N/SA:N/E:U"}], "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (0.10.78).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-19533 — rustls 0.23.36 is affected by GHSA-w44r-93j7-qv28 (RUSTSEC-2026-0349)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low
- Affected asset: `dependency:crates.io/rustls@0.23.36`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 29.4 / 100
- CVSS v3.1: 3.7 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N`)

OSV.dev reports GHSA-w44r-93j7-qv28 (RUSTSEC-2026-0349) for crates.io package rustls at version 0.23.36: rustls: An unauthenticated ServerHello poisons the per-name key-exchange record, so later ClientHellos carry only a classical X25519 share. The advisory names no affected functions, so reachability was not determined.

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

### QSI-2026-19532 — rustls 0.23.36 is affected by GHSA-h2v8-394m-p7vv (RUSTSEC-2026-0348)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/rustls@0.23.36`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 25.0 / 100
- CVSS v3.1: 3.7 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:N/A:L`)

OSV.dev reports GHSA-h2v8-394m-p7vv (RUSTSEC-2026-0348) for crates.io package rustls at version 0.23.36: Rustls: Brotli certificate decompression can allocate an attacker-controlled amount of memory up to 1 GiB before authentication. The affected code sits behind the `brotli` Cargo feature, off by default, which no audited manifest enables: the advisory does not apply unless another dependency enables it.

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

### QSI-2026-19486 — anyhow 1.0.102 is affected by RUSTSEC-2026-0190 (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/anyhow@1.0.102`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 20.3 / 100
- CVSS v3.1: not applicable

OSV.dev reports RUSTSEC-2026-0190 for crates.io package anyhow at version 1.0.102: Unsoundness in `Error::downcast_mut()`. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. The audited code does not name the affected functions (anyhow::Error::downcast_mut); anyhow comes in through other dependencies, which may still call them.

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0190
```

**Evidence.**

_tool_output · [OSV.dev RUSTSEC-2026-0190](https://osv.dev/vulnerability/RUSTSEC-2026-0190) · manifest · SHA-256 12d4b3eeb5a7dc67549bc112051813542621c4c3bb2d3ddfb353886e687f8013_

```
{"id": "RUSTSEC-2026-0190", "aliases": [], "modified": "2026-06-29T14:15:03.650725453Z", "summary": "Unsoundness in `Error::downcast_mut()`", "severity": null, "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Triage the advisory; upgrade to a fixed version (1.0.103) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-19488 — bitmaps 3.2.1 is affected by RUSTSEC-2025-0167 (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/bitmaps@3.2.1`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 20.3 / 100
- CVSS v3.1: not applicable

OSV.dev reports RUSTSEC-2025-0167 for crates.io package bitmaps at version 3.2.1: `Bitmap::try_from(&[u8])` can create invalid values. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2025-0167
```

**Evidence.**

_tool_output · [OSV.dev RUSTSEC-2025-0167](https://osv.dev/vulnerability/RUSTSEC-2025-0167) · manifest · SHA-256 03863e29642c4e63a545c7523f4282720a866033586991abde6afc0a8f4675cc_

```
{"id": "RUSTSEC-2025-0167", "aliases": [], "modified": "2026-08-10T19:45:04.530683607Z", "summary": "`Bitmap::try_from(&[u8])` can create invalid values", "severity": null, "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Triage the advisory; upgrade to a fixed version (none published yet; see the advisory for mitigations) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-19493 — crypto-bigint 0.5.5 is affected by RUSTSEC-2026-0387 (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/crypto-bigint@0.5.5`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 15:31 UTC
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

### QSI-2026-19494 — ctutils 0.4.0 is affected by RUSTSEC-2026-0385 (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/ctutils@0.4.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 20.3 / 100
- CVSS v3.1: not applicable

OSV.dev reports RUSTSEC-2026-0385 for crates.io package ctutils at version 0.4.0: Non-constant-time mask generation and `u128` comparisons. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0385
```

**Evidence.**

_tool_output · [OSV.dev RUSTSEC-2026-0385](https://osv.dev/vulnerability/RUSTSEC-2026-0385) · manifest · SHA-256 200470326c8a5ad19deb3639dff41d33749b1153097b6b87ef95e4beec747848_

```
{"id": "RUSTSEC-2026-0385", "aliases": [], "modified": "2026-10-23T08:30:02.389575143Z", "summary": "Non-constant-time mask generation and `u128` comparisons", "severity": null, "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Triage the advisory; upgrade to a fixed version (0.4.4) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-19496 — event-listener 5.4.1 is affected by RUSTSEC-2026-0221 (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/event-listener@5.4.1`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 20.3 / 100
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

### QSI-2026-19497 — git2 0.20.4 is affected by RUSTSEC-2026-0183 (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/git2@0.20.4`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 20.3 / 100
- CVSS v3.1: not applicable

OSV.dev reports RUSTSEC-2026-0183 for crates.io package git2 at version 0.20.4: Potential undefined behavior when calling Remote::list(). The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0183
```

**Evidence.**

_tool_output · [OSV.dev RUSTSEC-2026-0183](https://osv.dev/vulnerability/RUSTSEC-2026-0183) · manifest · SHA-256 10faba6c0849fd3be4082ba2701b3a701df0d48038fec8624f4d5771044fc51f_

```
{"id": "RUSTSEC-2026-0183", "aliases": [], "modified": "2026-06-17T13:00:04.696626611Z", "summary": "Potential undefined behavior when calling Remote::list()", "severity": null, "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Triage the advisory; upgrade to a fixed version (0.21.0) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-19498 — git2 0.20.4 is affected by RUSTSEC-2026-0184 (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/git2@0.20.4`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 20.3 / 100
- CVSS v3.1: not applicable

OSV.dev reports RUSTSEC-2026-0184 for crates.io package git2 at version 0.20.4: Potential undefined behavior with Signature from a buffer-created BlameHunk. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0184
```

**Evidence.**

_tool_output · [OSV.dev RUSTSEC-2026-0184](https://osv.dev/vulnerability/RUSTSEC-2026-0184) · manifest · SHA-256 bb3368926dab073cdb45cbcb12e78836e24537892ff222fd96327f747e605250_

```
{"id": "RUSTSEC-2026-0184", "aliases": [], "modified": "2026-06-17T14:00:05.672935662Z", "summary": "Potential undefined behavior with Signature from a buffer-created BlameHunk", "severity": null, "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Triage the advisory; upgrade to a fixed version (0.21.0) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-19503 — imbl-sized-chunks 0.1.3 is affected by RUSTSEC-2026-0292 (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/imbl-sized-chunks@0.1.3`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 20.3 / 100
- CVSS v3.1: not applicable

OSV.dev reports RUSTSEC-2026-0292 for crates.io package imbl-sized-chunks at version 0.1.3: Double free / use-after-free in `Chunk` and `InlineArray` removal methods when an element's `Drop` panics. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. The audited code does not name the affected functions (imbl_sized_chunks::inline_array::InlineArray::clear, imbl_sized_chunks::inline_array::InlineArray::truncate, imbl_sized_chunks::sized_chunk::Chunk::clear, imbl_sized_chunks::sized_chunk::Chunk::drop_left, imbl_sized_chunks::sized_chunk::Chunk::drop_right); imbl-sized-chunks comes in through other dependencies, which may still call them.

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0292
```

**Evidence.**

_tool_output · [OSV.dev RUSTSEC-2026-0292](https://osv.dev/vulnerability/RUSTSEC-2026-0292) · manifest · SHA-256 746e59e7a217deb325b0ab8f2f61c3aa99980400e09bc72ae0a048c06d833d42_

```
{"id": "RUSTSEC-2026-0292", "aliases": [], "modified": "2026-09-21T09:15:02.898993962Z", "summary": "Double free / use-after-free in `Chunk` and `InlineArray` removal methods when an element's `Drop` panics", "severity": null, "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Triage the advisory; upgrade to a fixed version (0.2.0) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-19506 — libz-sys 1.1.23 is affected by RUSTSEC-2026-0418 (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/libz-sys@1.1.23`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 20.3 / 100
- CVSS v3.1: not applicable

OSV.dev reports RUSTSEC-2026-0418 for crates.io package libz-sys at version 1.1.23: libz-sys build script leaks environment variables in the build directory. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0418
```

**Evidence.**

_tool_output · [OSV.dev RUSTSEC-2026-0418](https://osv.dev/vulnerability/RUSTSEC-2026-0418) · manifest · SHA-256 c5853994609eb6005df3fdabfd8d90722c9213a6b6ddc9f03b43ae0e4a747b57_

```
{"id": "RUSTSEC-2026-0418", "aliases": ["GHSA-8p3x-q3q3-q3v5"], "modified": "2026-10-29T14:15:02.333141406Z", "summary": "libz-sys build script leaks environment variables in the build directory", "severity": null, "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Triage the advisory; upgrade to a fixed version (1.1.31) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-19507 — lru 0.16.3 is affected by RUSTSEC-2026-0253 (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/lru@0.16.3`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 20.3 / 100
- CVSS v3.1: not applicable

OSV.dev reports RUSTSEC-2026-0253 for crates.io package lru at version 0.16.3: Potential use-after-free due to lack of panic safety in `LruCache::pop()`. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. The advisory names no affected functions, so reachability was not determined.

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

### QSI-2026-19520 — quinn-proto 0.11.15 is affected by RUSTSEC-2026-0338 (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/quinn-proto@0.11.15`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 20.3 / 100
- CVSS v3.1: not applicable

OSV.dev reports RUSTSEC-2026-0338 for crates.io package quinn-proto at version 0.11.15: Remote peer can panic quinn-proto with zero-length STREAM frames during unordered reads. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. The advisory names no affected functions, so reachability was not determined.

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

### QSI-2026-19521 — quinn-proto 0.11.15 is affected by RUSTSEC-2026-0339 (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/quinn-proto@0.11.15`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 20.3 / 100
- CVSS v3.1: not applicable

OSV.dev reports RUSTSEC-2026-0339 for crates.io package quinn-proto at version 0.11.15: Unbounded growth of pending connection ID retirements in quinn-proto. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0339
```

**Evidence.**

_tool_output · [OSV.dev RUSTSEC-2026-0339](https://osv.dev/vulnerability/RUSTSEC-2026-0339) · manifest · SHA-256 b5c8da254e3051004bc694e865ed6cf27e63c10cddc5641f13f42bd290bdb54a_

```
{"id": "RUSTSEC-2026-0339", "aliases": ["GHSA-hmxj-32vh-65vr"], "modified": "2026-10-12T18:15:01.956822776Z", "summary": "Unbounded growth of pending connection ID retirements in quinn-proto", "severity": null, "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Triage the advisory; upgrade to a fixed version (0.11.17) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-19524 — quinn-proto 0.11.15 is affected by RUSTSEC-2026-0342 (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/quinn-proto@0.11.15`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 20.3 / 100
- CVSS v3.1: not applicable

OSV.dev reports RUSTSEC-2026-0342 for crates.io package quinn-proto at version 0.11.15: Zero-length DATAGRAM frames bypass the receive buffer limit in quinn-proto. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0342
```

**Evidence.**

_tool_output · [OSV.dev RUSTSEC-2026-0342](https://osv.dev/vulnerability/RUSTSEC-2026-0342) · manifest · SHA-256 41dfd63166e25757cdb189c219a98c5e4b8d6b2e389f484cc583556a378073e4_

```
{"id": "RUSTSEC-2026-0342", "aliases": ["GHSA-2hv7-gw8g-gpq5"], "modified": "2026-10-12T18:15:01.956681478Z", "summary": "Zero-length DATAGRAM frames bypass the receive buffer limit in quinn-proto", "severity": null, "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Triage the advisory; upgrade to a fixed version (0.11.17) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-19535 — rustls-webpki 0.103.13 is affected by RUSTSEC-2026-0382 (CVE-2026-111943) (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/rustls-webpki@0.103.13`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 20.3 / 100
- CVSS v3.1: not applicable

OSV.dev reports RUSTSEC-2026-0382 (CVE-2026-111943) for crates.io package rustls-webpki at version 0.103.13: Certificate verification may accept distrusted intermediates. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0382
```

**Evidence.**

_tool_output · [OSV.dev RUSTSEC-2026-0382](https://osv.dev/vulnerability/RUSTSEC-2026-0382) · manifest · SHA-256 4c972eb1d77abf0d1c39f2b402c5fea32a5dacf7dbbeac638e7549ce780805d1_

```
{"id": "RUSTSEC-2026-0382", "aliases": ["BIT-golang-2026-111943", "CVE-2026-111943", "GO-2026-6809", "RUSTSEC-2026-0381", "RUSTSEC-2026-0383"], "modified": "2026-10-29T10:55:54.096394276Z", "summary": "Certificate verification may accept distrusted intermediates", "severity": null, "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Triage the advisory; upgrade to a fixed version (0.103.16, 0.104.0-alpha.8) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-19412 — Privileged administrative functions in contracts/src/Denylist.sol: addDenylister, removeDenylister

- Severity: **Info** · Classification: Improvement recommendation · Confidence: High
- Affected asset: `contract:contracts/src/Denylist.sol`
- Data source: contracts/src/Denylist.sol
- Detection method: Solidity source pattern analysis.
- Analyzer: solidity 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 37.0 / 100
- CVSS v3.1: not applicable

Functions guarded by owner/role modifiers: addDenylister, removeDenylister. (related: —)

**Potential impact.** Centralization risk: compromise of the admin key compromises the protocol.

**Reproduction steps.**

```
Open contract in the supplied file contracts/src/Denylist.sol and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [contracts/src/Denylist.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/src/Denylist.sol) · multiple · SHA-256 cadbbdb19e190130c437c5cd3c1bdd5bf5beba4ac520194ead25107990714e23_

```
Privileged functions: addDenylister, removeDenylister
```

**Limitations of the check.** Lightweight static pattern analysis of Solidity source without compilation or symbolic execution. It does not replace a full smart-contract audit; confirm manually or with dedicated tools (Slither, Foundry tests).

**Recommendation.** Use a multisig/timelock for admin roles and document them.

**Retest procedure.** Re-run static analysis and add a unit/fuzz test that exercises the pattern.

### QSI-2026-19413 — Privileged administrative functions in contracts/src/common/roles/Pausable.sol: updatePauser

- Severity: **Info** · Classification: Improvement recommendation · Confidence: High
- Affected asset: `contract:contracts/src/common/roles/Pausable.sol`
- Data source: contracts/src/common/roles/Pausable.sol
- Detection method: Solidity source pattern analysis.
- Analyzer: solidity 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 37.0 / 100
- CVSS v3.1: not applicable

Functions guarded by owner/role modifiers: updatePauser. (related: —)

**Potential impact.** Centralization risk: compromise of the admin key compromises the protocol.

**Reproduction steps.**

```
Open contract in the supplied file contracts/src/common/roles/Pausable.sol and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [contracts/src/common/roles/Pausable.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/src/common/roles/Pausable.sol) · multiple · SHA-256 bd451358b742bb99245bd4b702dca8520a5778e3c6052249a52d69b058d7e287_

```
Privileged functions: updatePauser
```

**Limitations of the check.** Lightweight static pattern analysis of Solidity source without compilation or symbolic execution. It does not replace a full smart-contract audit; confirm manually or with dedicated tools (Slither, Foundry tests).

**Recommendation.** Use a multisig/timelock for admin roles and document them.

**Retest procedure.** Re-run static analysis and add a unit/fuzz test that exercises the pattern.

### QSI-2026-19414 — Privileged administrative functions in contracts/src/protocol-config/roles/Controller.sol: updateController

- Severity: **Info** · Classification: Improvement recommendation · Confidence: High
- Affected asset: `contract:contracts/src/protocol-config/roles/Controller.sol`
- Data source: contracts/src/protocol-config/roles/Controller.sol
- Detection method: Solidity source pattern analysis.
- Analyzer: solidity 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 37.0 / 100
- CVSS v3.1: not applicable

Functions guarded by owner/role modifiers: updateController. (related: —)

**Potential impact.** Centralization risk: compromise of the admin key compromises the protocol.

**Reproduction steps.**

```
Open contract in the supplied file contracts/src/protocol-config/roles/Controller.sol and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [contracts/src/protocol-config/roles/Controller.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/src/protocol-config/roles/Controller.sol) · multiple · SHA-256 163e0107f6554559a2216f674f448926df9c7e2c7f9bbafff11a2dd4c71c44dd_

```
Privileged functions: updateController
```

**Limitations of the check.** Lightweight static pattern analysis of Solidity source without compilation or symbolic execution. It does not replace a full smart-contract audit; confirm manually or with dedicated tools (Slither, Foundry tests).

**Recommendation.** Use a multisig/timelock for admin roles and document them.

**Retest procedure.** Re-run static analysis and add a unit/fuzz test that exercises the pattern.

### QSI-2026-19415 — Privileged administrative functions in contracts/src/proxy/AdminUpgradeableProxy.sol: upgradeTo, upgradeToAndCall, changeAdmin

- Severity: **Info** · Classification: Improvement recommendation · Confidence: High
- Affected asset: `contract:contracts/src/proxy/AdminUpgradeableProxy.sol`
- Data source: contracts/src/proxy/AdminUpgradeableProxy.sol
- Detection method: Solidity source pattern analysis.
- Analyzer: solidity 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 37.0 / 100
- CVSS v3.1: not applicable

Functions guarded by owner/role modifiers: upgradeTo, upgradeToAndCall, changeAdmin. (related: —)

**Potential impact.** Centralization risk: compromise of the admin key compromises the protocol.

**Reproduction steps.**

```
Open contract in the supplied file contracts/src/proxy/AdminUpgradeableProxy.sol and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [contracts/src/proxy/AdminUpgradeableProxy.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/src/proxy/AdminUpgradeableProxy.sol) · multiple · SHA-256 cebcf7b9e5eb6647254a7b67be21e509d1481751443611294fc0f42bccfa0eb7_

```
Privileged functions: upgradeTo, upgradeToAndCall, changeAdmin
```

**Limitations of the check.** Lightweight static pattern analysis of Solidity source without compilation or symbolic execution. It does not replace a full smart-contract audit; confirm manually or with dedicated tools (Slither, Foundry tests).

**Recommendation.** Use a multisig/timelock for admin roles and document them.

**Retest procedure.** Re-run static analysis and add a unit/fuzz test that exercises the pattern.

### QSI-2026-19416 — Privileged administrative functions in contracts/src/validator-manager/PermissionedValidatorManager.sol: transferRegistryOwner, acceptRegistryOwnership

- Severity: **Info** · Classification: Improvement recommendation · Confidence: High
- Affected asset: `contract:contracts/src/validator-manager/PermissionedValidatorManager.sol`
- Data source: contracts/src/validator-manager/PermissionedValidatorManager.sol
- Detection method: Solidity source pattern analysis.
- Analyzer: solidity 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 37.0 / 100
- CVSS v3.1: not applicable

Functions guarded by owner/role modifiers: transferRegistryOwner, acceptRegistryOwnership. (related: —)

**Potential impact.** Centralization risk: compromise of the admin key compromises the protocol.

**Reproduction steps.**

```
Open contract in the supplied file contracts/src/validator-manager/PermissionedValidatorManager.sol and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [contracts/src/validator-manager/PermissionedValidatorManager.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/src/validator-manager/PermissionedValidatorManager.sol) · multiple · SHA-256 3931080fe35e77bc29d127415ae04b8c3218a8c5215a6e7af4e636bba2970151_

```
Privileged functions: transferRegistryOwner, acceptRegistryOwnership
```

**Limitations of the check.** Lightweight static pattern analysis of Solidity source without compilation or symbolic execution. It does not replace a full smart-contract audit; confirm manually or with dedicated tools (Slither, Foundry tests).

**Recommendation.** Use a multisig/timelock for admin roles and document them.

**Retest procedure.** Re-run static analysis and add a unit/fuzz test that exercises the pattern.

### QSI-2026-19417 — Privileged administrative functions in contracts/src/validator-manager/ValidatorRegistry.sol: registerValidator, activateValidator, removeValidator, updateValidatorVotingPower

- Severity: **Info** · Classification: Improvement recommendation · Confidence: High
- Affected asset: `contract:contracts/src/validator-manager/ValidatorRegistry.sol`
- Data source: contracts/src/validator-manager/ValidatorRegistry.sol
- Detection method: Solidity source pattern analysis.
- Analyzer: solidity 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 37.0 / 100
- CVSS v3.1: not applicable

Functions guarded by owner/role modifiers: registerValidator, activateValidator, removeValidator, updateValidatorVotingPower. (related: —)

**Potential impact.** Centralization risk: compromise of the admin key compromises the protocol.

**Reproduction steps.**

```
Open contract in the supplied file contracts/src/validator-manager/ValidatorRegistry.sol and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [contracts/src/validator-manager/ValidatorRegistry.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/src/validator-manager/ValidatorRegistry.sol) · multiple · SHA-256 bd1b2d0999172dce7804f3a5026567f30704da6702191f95c9cb5ffa2ad8f6d5_

```
Privileged functions: registerValidator, activateValidator, removeValidator, updateValidatorVotingPower
```

**Limitations of the check.** Lightweight static pattern analysis of Solidity source without compilation or symbolic execution. It does not replace a full smart-contract audit; confirm manually or with dedicated tools (Slither, Foundry tests).

**Recommendation.** Use a multisig/timelock for admin roles and document them.

**Retest procedure.** Re-run static analysis and add a unit/fuzz test that exercises the pattern.

### QSI-2026-19418 — Privileged administrative functions in contracts/src/validator-manager/roles/Controller.sol: configureController, removeController, updateVotingPowerLimit

- Severity: **Info** · Classification: Improvement recommendation · Confidence: High
- Affected asset: `contract:contracts/src/validator-manager/roles/Controller.sol`
- Data source: contracts/src/validator-manager/roles/Controller.sol
- Detection method: Solidity source pattern analysis.
- Analyzer: solidity 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 37.0 / 100
- CVSS v3.1: not applicable

Functions guarded by owner/role modifiers: configureController, removeController, updateVotingPowerLimit. (related: —)

**Potential impact.** Centralization risk: compromise of the admin key compromises the protocol.

**Reproduction steps.**

```
Open contract in the supplied file contracts/src/validator-manager/roles/Controller.sol and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [contracts/src/validator-manager/roles/Controller.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/src/validator-manager/roles/Controller.sol) · multiple · SHA-256 b34887a19bc168163054e80fca215b40e779ea813c2dd4166d91146c3325ef12_

```
Privileged functions: configureController, removeController, updateVotingPowerLimit
```

**Limitations of the check.** Lightweight static pattern analysis of Solidity source without compilation or symbolic execution. It does not replace a full smart-contract audit; confirm manually or with dedicated tools (Slither, Foundry tests).

**Recommendation.** Use a multisig/timelock for admin roles and document them.

**Retest procedure.** Re-run static analysis and add a unit/fuzz test that exercises the pattern.

### QSI-2026-19419 — Privileged administrative functions in contracts/src/validator-manager/roles/ValidatorRegisterer.sol: addValidatorRegisterer, removeValidatorRegisterer

- Severity: **Info** · Classification: Improvement recommendation · Confidence: High
- Affected asset: `contract:contracts/src/validator-manager/roles/ValidatorRegisterer.sol`
- Data source: contracts/src/validator-manager/roles/ValidatorRegisterer.sol
- Detection method: Solidity source pattern analysis.
- Analyzer: solidity 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 37.0 / 100
- CVSS v3.1: not applicable

Functions guarded by owner/role modifiers: addValidatorRegisterer, removeValidatorRegisterer. (related: —)

**Potential impact.** Centralization risk: compromise of the admin key compromises the protocol.

**Reproduction steps.**

```
Open contract in the supplied file contracts/src/validator-manager/roles/ValidatorRegisterer.sol and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [contracts/src/validator-manager/roles/ValidatorRegisterer.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/src/validator-manager/roles/ValidatorRegisterer.sol) · multiple · SHA-256 21761771f0d55baafbb802499b47d8acf890d4d9967eb4bbb342dbfa08af9f09_

```
Privileged functions: addValidatorRegisterer, removeValidatorRegisterer
```

**Limitations of the check.** Lightweight static pattern analysis of Solidity source without compilation or symbolic execution. It does not replace a full smart-contract audit; confirm manually or with dedicated tools (Slither, Foundry tests).

**Recommendation.** Use a multisig/timelock for admin roles and document them.

**Retest procedure.** Re-run static analysis and add a unit/fuzz test that exercises the pattern.

### QSI-2026-19425 — Privileged administrative functions in contracts/lib/openzeppelin-contracts-upgradeable/certora/harnesses/Ownable2StepHarness.sol: restricted

- Severity: **Info** · Classification: Improvement recommendation · Confidence: High
- Affected asset: `contract:contracts/lib/openzeppelin-contracts-upgradeable/certora/harnesses/Ownable2StepHarness.sol`
- Data source: contracts/lib/openzeppelin-contracts-upgradeable/certora/harnesses/Ownable2StepHarness.sol
- Detection method: Solidity source pattern analysis.
- Analyzer: solidity 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 37.0 / 100
- CVSS v3.1: not applicable

Functions guarded by owner/role modifiers: restricted. (related: —)

**Potential impact.** Centralization risk: compromise of the admin key compromises the protocol.

**Reproduction steps.**

```
Open contract in the supplied file contracts/lib/openzeppelin-contracts-upgradeable/certora/harnesses/Ownable2StepHarness.sol and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/certora/harnesses/Ownable2StepHarness.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/certora/harnesses/Ownable2StepHarness.sol) · multiple · SHA-256 36ed478689eb7537103955dd954f943862d16e4135ccd297de1e6c99b9b9e5e5_

```
Privileged functions: restricted
```

**Limitations of the check.** Lightweight static pattern analysis of Solidity source without compilation or symbolic execution. It does not replace a full smart-contract audit; confirm manually or with dedicated tools (Slither, Foundry tests).

**Recommendation.** Use a multisig/timelock for admin roles and document them.

**Retest procedure.** Re-run static analysis and add a unit/fuzz test that exercises the pattern.

### QSI-2026-19426 — Privileged administrative functions in contracts/lib/openzeppelin-contracts-upgradeable/certora/harnesses/OwnableHarness.sol: restricted

- Severity: **Info** · Classification: Improvement recommendation · Confidence: High
- Affected asset: `contract:contracts/lib/openzeppelin-contracts-upgradeable/certora/harnesses/OwnableHarness.sol`
- Data source: contracts/lib/openzeppelin-contracts-upgradeable/certora/harnesses/OwnableHarness.sol
- Detection method: Solidity source pattern analysis.
- Analyzer: solidity 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 37.0 / 100
- CVSS v3.1: not applicable

Functions guarded by owner/role modifiers: restricted. (related: —)

**Potential impact.** Centralization risk: compromise of the admin key compromises the protocol.

**Reproduction steps.**

```
Open contract in the supplied file contracts/lib/openzeppelin-contracts-upgradeable/certora/harnesses/OwnableHarness.sol and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/certora/harnesses/OwnableHarness.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/certora/harnesses/OwnableHarness.sol) · multiple · SHA-256 36ed478689eb7537103955dd954f943862d16e4135ccd297de1e6c99b9b9e5e5_

```
Privileged functions: restricted
```

**Limitations of the check.** Lightweight static pattern analysis of Solidity source without compilation or symbolic execution. It does not replace a full smart-contract audit; confirm manually or with dedicated tools (Slither, Foundry tests).

**Recommendation.** Use a multisig/timelock for admin roles and document them.

**Retest procedure.** Re-run static analysis and add a unit/fuzz test that exercises the pattern.

### QSI-2026-19427 — Privileged administrative functions in contracts/lib/openzeppelin-contracts-upgradeable/contracts/access/Ownable2StepUpgradeable.sol: transferOwnership

- Severity: **Info** · Classification: Improvement recommendation · Confidence: High
- Affected asset: `contract:contracts/lib/openzeppelin-contracts-upgradeable/contracts/access/Ownable2StepUpgradeable.sol`
- Data source: contracts/lib/openzeppelin-contracts-upgradeable/contracts/access/Ownable2StepUpgradeable.sol
- Detection method: Solidity source pattern analysis.
- Analyzer: solidity 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 37.0 / 100
- CVSS v3.1: not applicable

Functions guarded by owner/role modifiers: transferOwnership. (related: —)

**Potential impact.** Centralization risk: compromise of the admin key compromises the protocol.

**Reproduction steps.**

```
Open contract in the supplied file contracts/lib/openzeppelin-contracts-upgradeable/contracts/access/Ownable2StepUpgradeable.sol and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/contracts/access/Ownable2StepUpgradeable.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/contracts/access/Ownable2StepUpgradeable.sol) · multiple · SHA-256 3ef6a6924988649e26a7e42a450b6976f80844a318d3ab2418fc99e4bae2bcee_

```
Privileged functions: transferOwnership
```

**Limitations of the check.** Lightweight static pattern analysis of Solidity source without compilation or symbolic execution. It does not replace a full smart-contract audit; confirm manually or with dedicated tools (Slither, Foundry tests).

**Recommendation.** Use a multisig/timelock for admin roles and document them.

**Retest procedure.** Re-run static analysis and add a unit/fuzz test that exercises the pattern.

### QSI-2026-19428 — Privileged administrative functions in contracts/lib/openzeppelin-contracts-upgradeable/contracts/access/OwnableUpgradeable.sol: renounceOwnership, transferOwnership

- Severity: **Info** · Classification: Improvement recommendation · Confidence: High
- Affected asset: `contract:contracts/lib/openzeppelin-contracts-upgradeable/contracts/access/OwnableUpgradeable.sol`
- Data source: contracts/lib/openzeppelin-contracts-upgradeable/contracts/access/OwnableUpgradeable.sol
- Detection method: Solidity source pattern analysis.
- Analyzer: solidity 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 37.0 / 100
- CVSS v3.1: not applicable

Functions guarded by owner/role modifiers: renounceOwnership, transferOwnership. (related: —)

**Potential impact.** Centralization risk: compromise of the admin key compromises the protocol.

**Reproduction steps.**

```
Open contract in the supplied file contracts/lib/openzeppelin-contracts-upgradeable/contracts/access/OwnableUpgradeable.sol and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/contracts/access/OwnableUpgradeable.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/contracts/access/OwnableUpgradeable.sol) · multiple · SHA-256 c9178db25d8ef1b1a83ff9fe952090d86c1ef54a1f84a5a67cc0aac7fdd62bd6_

```
Privileged functions: renounceOwnership, transferOwnership
```

**Limitations of the check.** Lightweight static pattern analysis of Solidity source without compilation or symbolic execution. It does not replace a full smart-contract audit; confirm manually or with dedicated tools (Slither, Foundry tests).

**Recommendation.** Use a multisig/timelock for admin roles and document them.

**Retest procedure.** Re-run static analysis and add a unit/fuzz test that exercises the pattern.

### QSI-2026-19431 — Privileged administrative functions in contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/GovernorUpgradeable.sol: relay

- Severity: **Info** · Classification: Improvement recommendation · Confidence: High
- Affected asset: `contract:contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/GovernorUpgradeable.sol`
- Data source: contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/GovernorUpgradeable.sol
- Detection method: Solidity source pattern analysis.
- Analyzer: solidity 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 37.0 / 100
- CVSS v3.1: not applicable

Functions guarded by owner/role modifiers: relay. (related: —)

**Potential impact.** Centralization risk: compromise of the admin key compromises the protocol.

**Reproduction steps.**

```
Open contract in the supplied file contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/GovernorUpgradeable.sol and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/GovernorUpgradeable.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/GovernorUpgradeable.sol) · multiple · SHA-256 7ffca126961e19e9d9b0edb533fbaeacef6491d5098a94c1d9d5b988a15cb6ba_

```
Privileged functions: relay
```

**Limitations of the check.** Lightweight static pattern analysis of Solidity source without compilation or symbolic execution. It does not replace a full smart-contract audit; confirm manually or with dedicated tools (Slither, Foundry tests).

**Recommendation.** Use a multisig/timelock for admin roles and document them.

**Retest procedure.** Re-run static analysis and add a unit/fuzz test that exercises the pattern.

### QSI-2026-19432 — Privileged administrative functions in contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorPreventLateQuorumUpgradeable.sol: setLateQuorumVoteExtension

- Severity: **Info** · Classification: Improvement recommendation · Confidence: High
- Affected asset: `contract:contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorPreventLateQuorumUpgradeable.sol`
- Data source: contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorPreventLateQuorumUpgradeable.sol
- Detection method: Solidity source pattern analysis.
- Analyzer: solidity 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 37.0 / 100
- CVSS v3.1: not applicable

Functions guarded by owner/role modifiers: setLateQuorumVoteExtension. (related: —)

**Potential impact.** Centralization risk: compromise of the admin key compromises the protocol.

**Reproduction steps.**

```
Open contract in the supplied file contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorPreventLateQuorumUpgradeable.sol and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorPreventLateQuorumUpgradeable.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorPreventLateQuorumUpgradeable.sol) · multiple · SHA-256 514805472eac509275a6bf6ad6edb5f54cc24756ff9976c1eb00d142f771616d_

```
Privileged functions: setLateQuorumVoteExtension
```

**Limitations of the check.** Lightweight static pattern analysis of Solidity source without compilation or symbolic execution. It does not replace a full smart-contract audit; confirm manually or with dedicated tools (Slither, Foundry tests).

**Recommendation.** Use a multisig/timelock for admin roles and document them.

**Retest procedure.** Re-run static analysis and add a unit/fuzz test that exercises the pattern.

### QSI-2026-19433 — Privileged administrative functions in contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorProposalGuardianUpgradeable.sol: setProposalGuardian

- Severity: **Info** · Classification: Improvement recommendation · Confidence: High
- Affected asset: `contract:contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorProposalGuardianUpgradeable.sol`
- Data source: contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorProposalGuardianUpgradeable.sol
- Detection method: Solidity source pattern analysis.
- Analyzer: solidity 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 37.0 / 100
- CVSS v3.1: not applicable

Functions guarded by owner/role modifiers: setProposalGuardian. (related: —)

**Potential impact.** Centralization risk: compromise of the admin key compromises the protocol.

**Reproduction steps.**

```
Open contract in the supplied file contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorProposalGuardianUpgradeable.sol and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorProposalGuardianUpgradeable.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorProposalGuardianUpgradeable.sol) · multiple · SHA-256 07131118f6b2675894b2f4bfb84fe2a748fee242d9167f30d1ec33a4fc0f9f34_

```
Privileged functions: setProposalGuardian
```

**Limitations of the check.** Lightweight static pattern analysis of Solidity source without compilation or symbolic execution. It does not replace a full smart-contract audit; confirm manually or with dedicated tools (Slither, Foundry tests).

**Recommendation.** Use a multisig/timelock for admin roles and document them.

**Retest procedure.** Re-run static analysis and add a unit/fuzz test that exercises the pattern.

### QSI-2026-19434 — Privileged administrative functions in contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorSettingsUpgradeable.sol: setVotingDelay, setVotingPeriod, setProposalThreshold

- Severity: **Info** · Classification: Improvement recommendation · Confidence: High
- Affected asset: `contract:contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorSettingsUpgradeable.sol`
- Data source: contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorSettingsUpgradeable.sol
- Detection method: Solidity source pattern analysis.
- Analyzer: solidity 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 37.0 / 100
- CVSS v3.1: not applicable

Functions guarded by owner/role modifiers: setVotingDelay, setVotingPeriod, setProposalThreshold. (related: —)

**Potential impact.** Centralization risk: compromise of the admin key compromises the protocol.

**Reproduction steps.**

```
Open contract in the supplied file contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorSettingsUpgradeable.sol and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorSettingsUpgradeable.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorSettingsUpgradeable.sol) · multiple · SHA-256 86374e75349ee43fad2906180e81f23f3c94d19c2162c84a665cf6d22130b06e_

```
Privileged functions: setVotingDelay, setVotingPeriod, setProposalThreshold
```

**Limitations of the check.** Lightweight static pattern analysis of Solidity source without compilation or symbolic execution. It does not replace a full smart-contract audit; confirm manually or with dedicated tools (Slither, Foundry tests).

**Recommendation.** Use a multisig/timelock for admin roles and document them.

**Retest procedure.** Re-run static analysis and add a unit/fuzz test that exercises the pattern.

### QSI-2026-19435 — Privileged administrative functions in contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorTimelockAccessUpgradeable.sol: setBaseDelaySeconds, setAccessManagerIgnored

- Severity: **Info** · Classification: Improvement recommendation · Confidence: High
- Affected asset: `contract:contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorTimelockAccessUpgradeable.sol`
- Data source: contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorTimelockAccessUpgradeable.sol
- Detection method: Solidity source pattern analysis.
- Analyzer: solidity 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 37.0 / 100
- CVSS v3.1: not applicable

Functions guarded by owner/role modifiers: setBaseDelaySeconds, setAccessManagerIgnored. (related: —)

**Potential impact.** Centralization risk: compromise of the admin key compromises the protocol.

**Reproduction steps.**

```
Open contract in the supplied file contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorTimelockAccessUpgradeable.sol and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorTimelockAccessUpgradeable.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorTimelockAccessUpgradeable.sol) · multiple · SHA-256 f2f0ae2a1314268db485c56a4fe1f2d974856fd30405d8e1b223f1102f2a16d6_

```
Privileged functions: setBaseDelaySeconds, setAccessManagerIgnored
```

**Limitations of the check.** Lightweight static pattern analysis of Solidity source without compilation or symbolic execution. It does not replace a full smart-contract audit; confirm manually or with dedicated tools (Slither, Foundry tests).

**Recommendation.** Use a multisig/timelock for admin roles and document them.

**Retest procedure.** Re-run static analysis and add a unit/fuzz test that exercises the pattern.

### QSI-2026-19436 — Privileged administrative functions in contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorTimelockCompoundUpgradeable.sol: updateTimelock

- Severity: **Info** · Classification: Improvement recommendation · Confidence: High
- Affected asset: `contract:contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorTimelockCompoundUpgradeable.sol`
- Data source: contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorTimelockCompoundUpgradeable.sol
- Detection method: Solidity source pattern analysis.
- Analyzer: solidity 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 37.0 / 100
- CVSS v3.1: not applicable

Functions guarded by owner/role modifiers: updateTimelock. (related: —)

**Potential impact.** Centralization risk: compromise of the admin key compromises the protocol.

**Reproduction steps.**

```
Open contract in the supplied file contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorTimelockCompoundUpgradeable.sol and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorTimelockCompoundUpgradeable.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorTimelockCompoundUpgradeable.sol) · multiple · SHA-256 825de8a0266ca176b55c917fd9450222f4d40ce841c16a9f026715c5a07f3d75_

```
Privileged functions: updateTimelock
```

**Limitations of the check.** Lightweight static pattern analysis of Solidity source without compilation or symbolic execution. It does not replace a full smart-contract audit; confirm manually or with dedicated tools (Slither, Foundry tests).

**Recommendation.** Use a multisig/timelock for admin roles and document them.

**Retest procedure.** Re-run static analysis and add a unit/fuzz test that exercises the pattern.

### QSI-2026-19437 — Privileged administrative functions in contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorTimelockControlUpgradeable.sol: updateTimelock

- Severity: **Info** · Classification: Improvement recommendation · Confidence: High
- Affected asset: `contract:contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorTimelockControlUpgradeable.sol`
- Data source: contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorTimelockControlUpgradeable.sol
- Detection method: Solidity source pattern analysis.
- Analyzer: solidity 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 37.0 / 100
- CVSS v3.1: not applicable

Functions guarded by owner/role modifiers: updateTimelock. (related: —)

**Potential impact.** Centralization risk: compromise of the admin key compromises the protocol.

**Reproduction steps.**

```
Open contract in the supplied file contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorTimelockControlUpgradeable.sol and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorTimelockControlUpgradeable.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorTimelockControlUpgradeable.sol) · multiple · SHA-256 825de8a0266ca176b55c917fd9450222f4d40ce841c16a9f026715c5a07f3d75_

```
Privileged functions: updateTimelock
```

**Limitations of the check.** Lightweight static pattern analysis of Solidity source without compilation or symbolic execution. It does not replace a full smart-contract audit; confirm manually or with dedicated tools (Slither, Foundry tests).

**Recommendation.** Use a multisig/timelock for admin roles and document them.

**Retest procedure.** Re-run static analysis and add a unit/fuzz test that exercises the pattern.

### QSI-2026-19438 — Privileged administrative functions in contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorVotesQuorumFractionUpgradeable.sol: updateQuorumNumerator

- Severity: **Info** · Classification: Improvement recommendation · Confidence: High
- Affected asset: `contract:contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorVotesQuorumFractionUpgradeable.sol`
- Data source: contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorVotesQuorumFractionUpgradeable.sol
- Detection method: Solidity source pattern analysis.
- Analyzer: solidity 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 37.0 / 100
- CVSS v3.1: not applicable

Functions guarded by owner/role modifiers: updateQuorumNumerator. (related: —)

**Potential impact.** Centralization risk: compromise of the admin key compromises the protocol.

**Reproduction steps.**

```
Open contract in the supplied file contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorVotesQuorumFractionUpgradeable.sol and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorVotesQuorumFractionUpgradeable.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorVotesQuorumFractionUpgradeable.sol) · multiple · SHA-256 37d9e023fde908bbc2e9347f91ad2aa3006ddd93480c2ac0413f2847e2b727b4_

```
Privileged functions: updateQuorumNumerator
```

**Limitations of the check.** Lightweight static pattern analysis of Solidity source without compilation or symbolic execution. It does not replace a full smart-contract audit; confirm manually or with dedicated tools (Slither, Foundry tests).

**Recommendation.** Use a multisig/timelock for admin roles and document them.

**Retest procedure.** Re-run static analysis and add a unit/fuzz test that exercises the pattern.

### QSI-2026-19439 — Privileged administrative functions in contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorVotesSuperQuorumFractionUpgradeable.sol: updateSuperQuorumNumerator

- Severity: **Info** · Classification: Improvement recommendation · Confidence: High
- Affected asset: `contract:contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorVotesSuperQuorumFractionUpgradeable.sol`
- Data source: contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorVotesSuperQuorumFractionUpgradeable.sol
- Detection method: Solidity source pattern analysis.
- Analyzer: solidity 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 37.0 / 100
- CVSS v3.1: not applicable

Functions guarded by owner/role modifiers: updateSuperQuorumNumerator. (related: —)

**Potential impact.** Centralization risk: compromise of the admin key compromises the protocol.

**Reproduction steps.**

```
Open contract in the supplied file contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorVotesSuperQuorumFractionUpgradeable.sol and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorVotesSuperQuorumFractionUpgradeable.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorVotesSuperQuorumFractionUpgradeable.sol) · multiple · SHA-256 07f49116aa90ff89ec6b7b7d0820cc65a342e480d922ad1f7209983948f77120_

```
Privileged functions: updateSuperQuorumNumerator
```

**Limitations of the check.** Lightweight static pattern analysis of Solidity source without compilation or symbolic execution. It does not replace a full smart-contract audit; confirm manually or with dedicated tools (Slither, Foundry tests).

**Recommendation.** Use a multisig/timelock for admin roles and document them.

**Retest procedure.** Re-run static analysis and add a unit/fuzz test that exercises the pattern.

### QSI-2026-19443 — Privileged administrative functions in contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/certora/harnesses/Ownable2StepHarness.sol: restricted

- Severity: **Info** · Classification: Improvement recommendation · Confidence: High
- Affected asset: `contract:contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/certora/harnesses/Ownable2StepHarness.sol`
- Data source: contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/certora/harnesses/Ownable2StepHarness.sol
- Detection method: Solidity source pattern analysis.
- Analyzer: solidity 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 37.0 / 100
- CVSS v3.1: not applicable

Functions guarded by owner/role modifiers: restricted. (related: —)

**Potential impact.** Centralization risk: compromise of the admin key compromises the protocol.

**Reproduction steps.**

```
Open contract in the supplied file contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/certora/harnesses/Ownable2StepHarness.sol and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/certora/harnesses/Ownable2StepHarness.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/certora/harnesses/Ownable2StepHarness.sol) · multiple · SHA-256 36ed478689eb7537103955dd954f943862d16e4135ccd297de1e6c99b9b9e5e5_

```
Privileged functions: restricted
```

**Limitations of the check.** Lightweight static pattern analysis of Solidity source without compilation or symbolic execution. It does not replace a full smart-contract audit; confirm manually or with dedicated tools (Slither, Foundry tests).

**Recommendation.** Use a multisig/timelock for admin roles and document them.

**Retest procedure.** Re-run static analysis and add a unit/fuzz test that exercises the pattern.

### QSI-2026-19444 — Privileged administrative functions in contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/certora/harnesses/OwnableHarness.sol: restricted

- Severity: **Info** · Classification: Improvement recommendation · Confidence: High
- Affected asset: `contract:contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/certora/harnesses/OwnableHarness.sol`
- Data source: contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/certora/harnesses/OwnableHarness.sol
- Detection method: Solidity source pattern analysis.
- Analyzer: solidity 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 37.0 / 100
- CVSS v3.1: not applicable

Functions guarded by owner/role modifiers: restricted. (related: —)

**Potential impact.** Centralization risk: compromise of the admin key compromises the protocol.

**Reproduction steps.**

```
Open contract in the supplied file contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/certora/harnesses/OwnableHarness.sol and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/certora/harnesses/OwnableHarness.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/certora/harnesses/OwnableHarness.sol) · multiple · SHA-256 36ed478689eb7537103955dd954f943862d16e4135ccd297de1e6c99b9b9e5e5_

```
Privileged functions: restricted
```

**Limitations of the check.** Lightweight static pattern analysis of Solidity source without compilation or symbolic execution. It does not replace a full smart-contract audit; confirm manually or with dedicated tools (Slither, Foundry tests).

**Recommendation.** Use a multisig/timelock for admin roles and document them.

**Retest procedure.** Re-run static analysis and add a unit/fuzz test that exercises the pattern.

### QSI-2026-19446 — Privileged administrative functions in contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/access/Ownable.sol: renounceOwnership, transferOwnership

- Severity: **Info** · Classification: Improvement recommendation · Confidence: High
- Affected asset: `contract:contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/access/Ownable.sol`
- Data source: contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/access/Ownable.sol
- Detection method: Solidity source pattern analysis.
- Analyzer: solidity 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 37.0 / 100
- CVSS v3.1: not applicable

Functions guarded by owner/role modifiers: renounceOwnership, transferOwnership. (related: —)

**Potential impact.** Centralization risk: compromise of the admin key compromises the protocol.

**Reproduction steps.**

```
Open contract in the supplied file contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/access/Ownable.sol and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/access/Ownable.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/access/Ownable.sol) · multiple · SHA-256 c9178db25d8ef1b1a83ff9fe952090d86c1ef54a1f84a5a67cc0aac7fdd62bd6_

```
Privileged functions: renounceOwnership, transferOwnership
```

**Limitations of the check.** Lightweight static pattern analysis of Solidity source without compilation or symbolic execution. It does not replace a full smart-contract audit; confirm manually or with dedicated tools (Slither, Foundry tests).

**Recommendation.** Use a multisig/timelock for admin roles and document them.

**Retest procedure.** Re-run static analysis and add a unit/fuzz test that exercises the pattern.

### QSI-2026-19447 — Privileged administrative functions in contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/access/Ownable2Step.sol: transferOwnership

- Severity: **Info** · Classification: Improvement recommendation · Confidence: High
- Affected asset: `contract:contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/access/Ownable2Step.sol`
- Data source: contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/access/Ownable2Step.sol
- Detection method: Solidity source pattern analysis.
- Analyzer: solidity 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 37.0 / 100
- CVSS v3.1: not applicable

Functions guarded by owner/role modifiers: transferOwnership. (related: —)

**Potential impact.** Centralization risk: compromise of the admin key compromises the protocol.

**Reproduction steps.**

```
Open contract in the supplied file contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/access/Ownable2Step.sol and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/access/Ownable2Step.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/access/Ownable2Step.sol) · multiple · SHA-256 3ef6a6924988649e26a7e42a450b6976f80844a318d3ab2418fc99e4bae2bcee_

```
Privileged functions: transferOwnership
```

**Limitations of the check.** Lightweight static pattern analysis of Solidity source without compilation or symbolic execution. It does not replace a full smart-contract audit; confirm manually or with dedicated tools (Slither, Foundry tests).

**Recommendation.** Use a multisig/timelock for admin roles and document them.

**Retest procedure.** Re-run static analysis and add a unit/fuzz test that exercises the pattern.

### QSI-2026-19450 — Privileged administrative functions in contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/Governor.sol: relay

- Severity: **Info** · Classification: Improvement recommendation · Confidence: High
- Affected asset: `contract:contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/Governor.sol`
- Data source: contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/Governor.sol
- Detection method: Solidity source pattern analysis.
- Analyzer: solidity 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 37.0 / 100
- CVSS v3.1: not applicable

Functions guarded by owner/role modifiers: relay. (related: —)

**Potential impact.** Centralization risk: compromise of the admin key compromises the protocol.

**Reproduction steps.**

```
Open contract in the supplied file contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/Governor.sol and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/Governor.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/Governor.sol) · multiple · SHA-256 7ffca126961e19e9d9b0edb533fbaeacef6491d5098a94c1d9d5b988a15cb6ba_

```
Privileged functions: relay
```

**Limitations of the check.** Lightweight static pattern analysis of Solidity source without compilation or symbolic execution. It does not replace a full smart-contract audit; confirm manually or with dedicated tools (Slither, Foundry tests).

**Recommendation.** Use a multisig/timelock for admin roles and document them.

**Retest procedure.** Re-run static analysis and add a unit/fuzz test that exercises the pattern.

### QSI-2026-19451 — Privileged administrative functions in contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorPreventLateQuorum.sol: setLateQuorumVoteExtension

- Severity: **Info** · Classification: Improvement recommendation · Confidence: High
- Affected asset: `contract:contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorPreventLateQuorum.sol`
- Data source: contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorPreventLateQuorum.sol
- Detection method: Solidity source pattern analysis.
- Analyzer: solidity 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 37.0 / 100
- CVSS v3.1: not applicable

Functions guarded by owner/role modifiers: setLateQuorumVoteExtension. (related: —)

**Potential impact.** Centralization risk: compromise of the admin key compromises the protocol.

**Reproduction steps.**

```
Open contract in the supplied file contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorPreventLateQuorum.sol and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorPreventLateQuorum.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorPreventLateQuorum.sol) · multiple · SHA-256 514805472eac509275a6bf6ad6edb5f54cc24756ff9976c1eb00d142f771616d_

```
Privileged functions: setLateQuorumVoteExtension
```

**Limitations of the check.** Lightweight static pattern analysis of Solidity source without compilation or symbolic execution. It does not replace a full smart-contract audit; confirm manually or with dedicated tools (Slither, Foundry tests).

**Recommendation.** Use a multisig/timelock for admin roles and document them.

**Retest procedure.** Re-run static analysis and add a unit/fuzz test that exercises the pattern.

### QSI-2026-19452 — Privileged administrative functions in contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorProposalGuardian.sol: setProposalGuardian

- Severity: **Info** · Classification: Improvement recommendation · Confidence: High
- Affected asset: `contract:contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorProposalGuardian.sol`
- Data source: contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorProposalGuardian.sol
- Detection method: Solidity source pattern analysis.
- Analyzer: solidity 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 37.0 / 100
- CVSS v3.1: not applicable

Functions guarded by owner/role modifiers: setProposalGuardian. (related: —)

**Potential impact.** Centralization risk: compromise of the admin key compromises the protocol.

**Reproduction steps.**

```
Open contract in the supplied file contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorProposalGuardian.sol and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorProposalGuardian.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorProposalGuardian.sol) · multiple · SHA-256 07131118f6b2675894b2f4bfb84fe2a748fee242d9167f30d1ec33a4fc0f9f34_

```
Privileged functions: setProposalGuardian
```

**Limitations of the check.** Lightweight static pattern analysis of Solidity source without compilation or symbolic execution. It does not replace a full smart-contract audit; confirm manually or with dedicated tools (Slither, Foundry tests).

**Recommendation.** Use a multisig/timelock for admin roles and document them.

**Retest procedure.** Re-run static analysis and add a unit/fuzz test that exercises the pattern.

### QSI-2026-19453 — Privileged administrative functions in contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorSettings.sol: setVotingDelay, setVotingPeriod, setProposalThreshold

- Severity: **Info** · Classification: Improvement recommendation · Confidence: High
- Affected asset: `contract:contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorSettings.sol`
- Data source: contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorSettings.sol
- Detection method: Solidity source pattern analysis.
- Analyzer: solidity 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 37.0 / 100
- CVSS v3.1: not applicable

Functions guarded by owner/role modifiers: setVotingDelay, setVotingPeriod, setProposalThreshold. (related: —)

**Potential impact.** Centralization risk: compromise of the admin key compromises the protocol.

**Reproduction steps.**

```
Open contract in the supplied file contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorSettings.sol and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorSettings.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorSettings.sol) · multiple · SHA-256 86374e75349ee43fad2906180e81f23f3c94d19c2162c84a665cf6d22130b06e_

```
Privileged functions: setVotingDelay, setVotingPeriod, setProposalThreshold
```

**Limitations of the check.** Lightweight static pattern analysis of Solidity source without compilation or symbolic execution. It does not replace a full smart-contract audit; confirm manually or with dedicated tools (Slither, Foundry tests).

**Recommendation.** Use a multisig/timelock for admin roles and document them.

**Retest procedure.** Re-run static analysis and add a unit/fuzz test that exercises the pattern.

### QSI-2026-19454 — Privileged administrative functions in contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorTimelockAccess.sol: setBaseDelaySeconds, setAccessManagerIgnored

- Severity: **Info** · Classification: Improvement recommendation · Confidence: High
- Affected asset: `contract:contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorTimelockAccess.sol`
- Data source: contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorTimelockAccess.sol
- Detection method: Solidity source pattern analysis.
- Analyzer: solidity 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 37.0 / 100
- CVSS v3.1: not applicable

Functions guarded by owner/role modifiers: setBaseDelaySeconds, setAccessManagerIgnored. (related: —)

**Potential impact.** Centralization risk: compromise of the admin key compromises the protocol.

**Reproduction steps.**

```
Open contract in the supplied file contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorTimelockAccess.sol and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorTimelockAccess.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorTimelockAccess.sol) · multiple · SHA-256 f2f0ae2a1314268db485c56a4fe1f2d974856fd30405d8e1b223f1102f2a16d6_

```
Privileged functions: setBaseDelaySeconds, setAccessManagerIgnored
```

**Limitations of the check.** Lightweight static pattern analysis of Solidity source without compilation or symbolic execution. It does not replace a full smart-contract audit; confirm manually or with dedicated tools (Slither, Foundry tests).

**Recommendation.** Use a multisig/timelock for admin roles and document them.

**Retest procedure.** Re-run static analysis and add a unit/fuzz test that exercises the pattern.

### QSI-2026-19455 — Privileged administrative functions in contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorTimelockCompound.sol: updateTimelock

- Severity: **Info** · Classification: Improvement recommendation · Confidence: High
- Affected asset: `contract:contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorTimelockCompound.sol`
- Data source: contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorTimelockCompound.sol
- Detection method: Solidity source pattern analysis.
- Analyzer: solidity 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 37.0 / 100
- CVSS v3.1: not applicable

Functions guarded by owner/role modifiers: updateTimelock. (related: —)

**Potential impact.** Centralization risk: compromise of the admin key compromises the protocol.

**Reproduction steps.**

```
Open contract in the supplied file contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorTimelockCompound.sol and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorTimelockCompound.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorTimelockCompound.sol) · multiple · SHA-256 825de8a0266ca176b55c917fd9450222f4d40ce841c16a9f026715c5a07f3d75_

```
Privileged functions: updateTimelock
```

**Limitations of the check.** Lightweight static pattern analysis of Solidity source without compilation or symbolic execution. It does not replace a full smart-contract audit; confirm manually or with dedicated tools (Slither, Foundry tests).

**Recommendation.** Use a multisig/timelock for admin roles and document them.

**Retest procedure.** Re-run static analysis and add a unit/fuzz test that exercises the pattern.

### QSI-2026-19456 — Privileged administrative functions in contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorTimelockControl.sol: updateTimelock

- Severity: **Info** · Classification: Improvement recommendation · Confidence: High
- Affected asset: `contract:contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorTimelockControl.sol`
- Data source: contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorTimelockControl.sol
- Detection method: Solidity source pattern analysis.
- Analyzer: solidity 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 37.0 / 100
- CVSS v3.1: not applicable

Functions guarded by owner/role modifiers: updateTimelock. (related: —)

**Potential impact.** Centralization risk: compromise of the admin key compromises the protocol.

**Reproduction steps.**

```
Open contract in the supplied file contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorTimelockControl.sol and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorTimelockControl.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorTimelockControl.sol) · multiple · SHA-256 825de8a0266ca176b55c917fd9450222f4d40ce841c16a9f026715c5a07f3d75_

```
Privileged functions: updateTimelock
```

**Limitations of the check.** Lightweight static pattern analysis of Solidity source without compilation or symbolic execution. It does not replace a full smart-contract audit; confirm manually or with dedicated tools (Slither, Foundry tests).

**Recommendation.** Use a multisig/timelock for admin roles and document them.

**Retest procedure.** Re-run static analysis and add a unit/fuzz test that exercises the pattern.

### QSI-2026-19457 — Privileged administrative functions in contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorVotesQuorumFraction.sol: updateQuorumNumerator

- Severity: **Info** · Classification: Improvement recommendation · Confidence: High
- Affected asset: `contract:contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorVotesQuorumFraction.sol`
- Data source: contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorVotesQuorumFraction.sol
- Detection method: Solidity source pattern analysis.
- Analyzer: solidity 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 37.0 / 100
- CVSS v3.1: not applicable

Functions guarded by owner/role modifiers: updateQuorumNumerator. (related: —)

**Potential impact.** Centralization risk: compromise of the admin key compromises the protocol.

**Reproduction steps.**

```
Open contract in the supplied file contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorVotesQuorumFraction.sol and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorVotesQuorumFraction.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorVotesQuorumFraction.sol) · multiple · SHA-256 37d9e023fde908bbc2e9347f91ad2aa3006ddd93480c2ac0413f2847e2b727b4_

```
Privileged functions: updateQuorumNumerator
```

**Limitations of the check.** Lightweight static pattern analysis of Solidity source without compilation or symbolic execution. It does not replace a full smart-contract audit; confirm manually or with dedicated tools (Slither, Foundry tests).

**Recommendation.** Use a multisig/timelock for admin roles and document them.

**Retest procedure.** Re-run static analysis and add a unit/fuzz test that exercises the pattern.

### QSI-2026-19458 — Privileged administrative functions in contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorVotesSuperQuorumFraction.sol: updateSuperQuorumNumerator

- Severity: **Info** · Classification: Improvement recommendation · Confidence: High
- Affected asset: `contract:contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorVotesSuperQuorumFraction.sol`
- Data source: contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorVotesSuperQuorumFraction.sol
- Detection method: Solidity source pattern analysis.
- Analyzer: solidity 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 37.0 / 100
- CVSS v3.1: not applicable

Functions guarded by owner/role modifiers: updateSuperQuorumNumerator. (related: —)

**Potential impact.** Centralization risk: compromise of the admin key compromises the protocol.

**Reproduction steps.**

```
Open contract in the supplied file contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorVotesSuperQuorumFraction.sol and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorVotesSuperQuorumFraction.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorVotesSuperQuorumFraction.sol) · multiple · SHA-256 07f49116aa90ff89ec6b7b7d0820cc65a342e480d922ad1f7209983948f77120_

```
Privileged functions: updateSuperQuorumNumerator
```

**Limitations of the check.** Lightweight static pattern analysis of Solidity source without compilation or symbolic execution. It does not replace a full smart-contract audit; confirm manually or with dedicated tools (Slither, Foundry tests).

**Recommendation.** Use a multisig/timelock for admin roles and document them.

**Retest procedure.** Re-run static analysis and add a unit/fuzz test that exercises the pattern.

### QSI-2026-19463 — Privileged administrative functions in contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/proxy/beacon/UpgradeableBeacon.sol: upgradeTo

- Severity: **Info** · Classification: Improvement recommendation · Confidence: High
- Affected asset: `contract:contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/proxy/beacon/UpgradeableBeacon.sol`
- Data source: contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/proxy/beacon/UpgradeableBeacon.sol
- Detection method: Solidity source pattern analysis.
- Analyzer: solidity 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 37.0 / 100
- CVSS v3.1: not applicable

Functions guarded by owner/role modifiers: upgradeTo. (related: —)

**Potential impact.** Centralization risk: compromise of the admin key compromises the protocol.

**Reproduction steps.**

```
Open contract in the supplied file contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/proxy/beacon/UpgradeableBeacon.sol and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/proxy/beacon/UpgradeableBeacon.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/proxy/beacon/UpgradeableBeacon.sol) · multiple · SHA-256 02e606b6560ec4a99c06589dd8655178cca253b457dcec0438b77dd4a8cb04f5_

```
Privileged functions: upgradeTo
```

**Limitations of the check.** Lightweight static pattern analysis of Solidity source without compilation or symbolic execution. It does not replace a full smart-contract audit; confirm manually or with dedicated tools (Slither, Foundry tests).

**Recommendation.** Use a multisig/timelock for admin roles and document them.

**Retest procedure.** Re-run static analysis and add a unit/fuzz test that exercises the pattern.

### QSI-2026-19464 — Privileged administrative functions in contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/proxy/transparent/ProxyAdmin.sol: upgradeAndCall

- Severity: **Info** · Classification: Improvement recommendation · Confidence: High
- Affected asset: `contract:contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/proxy/transparent/ProxyAdmin.sol`
- Data source: contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/proxy/transparent/ProxyAdmin.sol
- Detection method: Solidity source pattern analysis.
- Analyzer: solidity 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 37.0 / 100
- CVSS v3.1: not applicable

Functions guarded by owner/role modifiers: upgradeAndCall. (related: —)

**Potential impact.** Centralization risk: compromise of the admin key compromises the protocol.

**Reproduction steps.**

```
Open contract in the supplied file contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/proxy/transparent/ProxyAdmin.sol and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/proxy/transparent/ProxyAdmin.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/proxy/transparent/ProxyAdmin.sol) · multiple · SHA-256 08d87f8ddab73b6f3211d313d176dd5e3323cdca43425bff268f49bee3960937_

```
Privileged functions: upgradeAndCall
```

**Limitations of the check.** Lightweight static pattern analysis of Solidity source without compilation or symbolic execution. It does not replace a full smart-contract audit; confirm manually or with dedicated tools (Slither, Foundry tests).

**Recommendation.** Use a multisig/timelock for admin roles and document them.

**Retest procedure.** Re-run static analysis and add a unit/fuzz test that exercises the pattern.

### QSI-2026-19468 — Privileged administrative functions in contracts/lib/openzeppelin-contracts/certora/harnesses/Ownable2StepHarness.sol: restricted

- Severity: **Info** · Classification: Improvement recommendation · Confidence: High
- Affected asset: `contract:contracts/lib/openzeppelin-contracts/certora/harnesses/Ownable2StepHarness.sol`
- Data source: contracts/lib/openzeppelin-contracts/certora/harnesses/Ownable2StepHarness.sol
- Detection method: Solidity source pattern analysis.
- Analyzer: solidity 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 37.0 / 100
- CVSS v3.1: not applicable

Functions guarded by owner/role modifiers: restricted. (related: —)

**Potential impact.** Centralization risk: compromise of the admin key compromises the protocol.

**Reproduction steps.**

```
Open contract in the supplied file contracts/lib/openzeppelin-contracts/certora/harnesses/Ownable2StepHarness.sol and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [contracts/lib/openzeppelin-contracts/certora/harnesses/Ownable2StepHarness.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts/certora/harnesses/Ownable2StepHarness.sol) · multiple · SHA-256 36ed478689eb7537103955dd954f943862d16e4135ccd297de1e6c99b9b9e5e5_

```
Privileged functions: restricted
```

**Limitations of the check.** Lightweight static pattern analysis of Solidity source without compilation or symbolic execution. It does not replace a full smart-contract audit; confirm manually or with dedicated tools (Slither, Foundry tests).

**Recommendation.** Use a multisig/timelock for admin roles and document them.

**Retest procedure.** Re-run static analysis and add a unit/fuzz test that exercises the pattern.

### QSI-2026-19469 — Privileged administrative functions in contracts/lib/openzeppelin-contracts/certora/harnesses/OwnableHarness.sol: restricted

- Severity: **Info** · Classification: Improvement recommendation · Confidence: High
- Affected asset: `contract:contracts/lib/openzeppelin-contracts/certora/harnesses/OwnableHarness.sol`
- Data source: contracts/lib/openzeppelin-contracts/certora/harnesses/OwnableHarness.sol
- Detection method: Solidity source pattern analysis.
- Analyzer: solidity 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 37.0 / 100
- CVSS v3.1: not applicable

Functions guarded by owner/role modifiers: restricted. (related: —)

**Potential impact.** Centralization risk: compromise of the admin key compromises the protocol.

**Reproduction steps.**

```
Open contract in the supplied file contracts/lib/openzeppelin-contracts/certora/harnesses/OwnableHarness.sol and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [contracts/lib/openzeppelin-contracts/certora/harnesses/OwnableHarness.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts/certora/harnesses/OwnableHarness.sol) · multiple · SHA-256 36ed478689eb7537103955dd954f943862d16e4135ccd297de1e6c99b9b9e5e5_

```
Privileged functions: restricted
```

**Limitations of the check.** Lightweight static pattern analysis of Solidity source without compilation or symbolic execution. It does not replace a full smart-contract audit; confirm manually or with dedicated tools (Slither, Foundry tests).

**Recommendation.** Use a multisig/timelock for admin roles and document them.

**Retest procedure.** Re-run static analysis and add a unit/fuzz test that exercises the pattern.

### QSI-2026-19470 — Privileged administrative functions in contracts/lib/openzeppelin-contracts/contracts/access/Ownable.sol: renounceOwnership, transferOwnership

- Severity: **Info** · Classification: Improvement recommendation · Confidence: High
- Affected asset: `contract:contracts/lib/openzeppelin-contracts/contracts/access/Ownable.sol`
- Data source: contracts/lib/openzeppelin-contracts/contracts/access/Ownable.sol
- Detection method: Solidity source pattern analysis.
- Analyzer: solidity 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 37.0 / 100
- CVSS v3.1: not applicable

Functions guarded by owner/role modifiers: renounceOwnership, transferOwnership. (related: —)

**Potential impact.** Centralization risk: compromise of the admin key compromises the protocol.

**Reproduction steps.**

```
Open contract in the supplied file contracts/lib/openzeppelin-contracts/contracts/access/Ownable.sol and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [contracts/lib/openzeppelin-contracts/contracts/access/Ownable.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts/contracts/access/Ownable.sol) · multiple · SHA-256 c9178db25d8ef1b1a83ff9fe952090d86c1ef54a1f84a5a67cc0aac7fdd62bd6_

```
Privileged functions: renounceOwnership, transferOwnership
```

**Limitations of the check.** Lightweight static pattern analysis of Solidity source without compilation or symbolic execution. It does not replace a full smart-contract audit; confirm manually or with dedicated tools (Slither, Foundry tests).

**Recommendation.** Use a multisig/timelock for admin roles and document them.

**Retest procedure.** Re-run static analysis and add a unit/fuzz test that exercises the pattern.

### QSI-2026-19471 — Privileged administrative functions in contracts/lib/openzeppelin-contracts/contracts/access/Ownable2Step.sol: transferOwnership

- Severity: **Info** · Classification: Improvement recommendation · Confidence: High
- Affected asset: `contract:contracts/lib/openzeppelin-contracts/contracts/access/Ownable2Step.sol`
- Data source: contracts/lib/openzeppelin-contracts/contracts/access/Ownable2Step.sol
- Detection method: Solidity source pattern analysis.
- Analyzer: solidity 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 37.0 / 100
- CVSS v3.1: not applicable

Functions guarded by owner/role modifiers: transferOwnership. (related: —)

**Potential impact.** Centralization risk: compromise of the admin key compromises the protocol.

**Reproduction steps.**

```
Open contract in the supplied file contracts/lib/openzeppelin-contracts/contracts/access/Ownable2Step.sol and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [contracts/lib/openzeppelin-contracts/contracts/access/Ownable2Step.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts/contracts/access/Ownable2Step.sol) · multiple · SHA-256 3ef6a6924988649e26a7e42a450b6976f80844a318d3ab2418fc99e4bae2bcee_

```
Privileged functions: transferOwnership
```

**Limitations of the check.** Lightweight static pattern analysis of Solidity source without compilation or symbolic execution. It does not replace a full smart-contract audit; confirm manually or with dedicated tools (Slither, Foundry tests).

**Recommendation.** Use a multisig/timelock for admin roles and document them.

**Retest procedure.** Re-run static analysis and add a unit/fuzz test that exercises the pattern.

### QSI-2026-19473 — Privileged administrative functions in contracts/lib/openzeppelin-contracts/contracts/governance/Governor.sol: relay

- Severity: **Info** · Classification: Improvement recommendation · Confidence: High
- Affected asset: `contract:contracts/lib/openzeppelin-contracts/contracts/governance/Governor.sol`
- Data source: contracts/lib/openzeppelin-contracts/contracts/governance/Governor.sol
- Detection method: Solidity source pattern analysis.
- Analyzer: solidity 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 37.0 / 100
- CVSS v3.1: not applicable

Functions guarded by owner/role modifiers: relay. (related: —)

**Potential impact.** Centralization risk: compromise of the admin key compromises the protocol.

**Reproduction steps.**

```
Open contract in the supplied file contracts/lib/openzeppelin-contracts/contracts/governance/Governor.sol and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [contracts/lib/openzeppelin-contracts/contracts/governance/Governor.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts/contracts/governance/Governor.sol) · multiple · SHA-256 7ffca126961e19e9d9b0edb533fbaeacef6491d5098a94c1d9d5b988a15cb6ba_

```
Privileged functions: relay
```

**Limitations of the check.** Lightweight static pattern analysis of Solidity source without compilation or symbolic execution. It does not replace a full smart-contract audit; confirm manually or with dedicated tools (Slither, Foundry tests).

**Recommendation.** Use a multisig/timelock for admin roles and document them.

**Retest procedure.** Re-run static analysis and add a unit/fuzz test that exercises the pattern.

### QSI-2026-19474 — Privileged administrative functions in contracts/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorPreventLateQuorum.sol: setLateQuorumVoteExtension

- Severity: **Info** · Classification: Improvement recommendation · Confidence: High
- Affected asset: `contract:contracts/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorPreventLateQuorum.sol`
- Data source: contracts/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorPreventLateQuorum.sol
- Detection method: Solidity source pattern analysis.
- Analyzer: solidity 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 37.0 / 100
- CVSS v3.1: not applicable

Functions guarded by owner/role modifiers: setLateQuorumVoteExtension. (related: —)

**Potential impact.** Centralization risk: compromise of the admin key compromises the protocol.

**Reproduction steps.**

```
Open contract in the supplied file contracts/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorPreventLateQuorum.sol and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [contracts/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorPreventLateQuorum.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorPreventLateQuorum.sol) · multiple · SHA-256 514805472eac509275a6bf6ad6edb5f54cc24756ff9976c1eb00d142f771616d_

```
Privileged functions: setLateQuorumVoteExtension
```

**Limitations of the check.** Lightweight static pattern analysis of Solidity source without compilation or symbolic execution. It does not replace a full smart-contract audit; confirm manually or with dedicated tools (Slither, Foundry tests).

**Recommendation.** Use a multisig/timelock for admin roles and document them.

**Retest procedure.** Re-run static analysis and add a unit/fuzz test that exercises the pattern.

### QSI-2026-19475 — Privileged administrative functions in contracts/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorProposalGuardian.sol: setProposalGuardian

- Severity: **Info** · Classification: Improvement recommendation · Confidence: High
- Affected asset: `contract:contracts/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorProposalGuardian.sol`
- Data source: contracts/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorProposalGuardian.sol
- Detection method: Solidity source pattern analysis.
- Analyzer: solidity 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 37.0 / 100
- CVSS v3.1: not applicable

Functions guarded by owner/role modifiers: setProposalGuardian. (related: —)

**Potential impact.** Centralization risk: compromise of the admin key compromises the protocol.

**Reproduction steps.**

```
Open contract in the supplied file contracts/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorProposalGuardian.sol and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [contracts/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorProposalGuardian.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorProposalGuardian.sol) · multiple · SHA-256 07131118f6b2675894b2f4bfb84fe2a748fee242d9167f30d1ec33a4fc0f9f34_

```
Privileged functions: setProposalGuardian
```

**Limitations of the check.** Lightweight static pattern analysis of Solidity source without compilation or symbolic execution. It does not replace a full smart-contract audit; confirm manually or with dedicated tools (Slither, Foundry tests).

**Recommendation.** Use a multisig/timelock for admin roles and document them.

**Retest procedure.** Re-run static analysis and add a unit/fuzz test that exercises the pattern.

### QSI-2026-19476 — Privileged administrative functions in contracts/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorSettings.sol: setVotingDelay, setVotingPeriod, setProposalThreshold

- Severity: **Info** · Classification: Improvement recommendation · Confidence: High
- Affected asset: `contract:contracts/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorSettings.sol`
- Data source: contracts/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorSettings.sol
- Detection method: Solidity source pattern analysis.
- Analyzer: solidity 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 37.0 / 100
- CVSS v3.1: not applicable

Functions guarded by owner/role modifiers: setVotingDelay, setVotingPeriod, setProposalThreshold. (related: —)

**Potential impact.** Centralization risk: compromise of the admin key compromises the protocol.

**Reproduction steps.**

```
Open contract in the supplied file contracts/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorSettings.sol and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [contracts/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorSettings.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorSettings.sol) · multiple · SHA-256 86374e75349ee43fad2906180e81f23f3c94d19c2162c84a665cf6d22130b06e_

```
Privileged functions: setVotingDelay, setVotingPeriod, setProposalThreshold
```

**Limitations of the check.** Lightweight static pattern analysis of Solidity source without compilation or symbolic execution. It does not replace a full smart-contract audit; confirm manually or with dedicated tools (Slither, Foundry tests).

**Recommendation.** Use a multisig/timelock for admin roles and document them.

**Retest procedure.** Re-run static analysis and add a unit/fuzz test that exercises the pattern.

### QSI-2026-19477 — Privileged administrative functions in contracts/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorTimelockAccess.sol: setBaseDelaySeconds, setAccessManagerIgnored

- Severity: **Info** · Classification: Improvement recommendation · Confidence: High
- Affected asset: `contract:contracts/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorTimelockAccess.sol`
- Data source: contracts/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorTimelockAccess.sol
- Detection method: Solidity source pattern analysis.
- Analyzer: solidity 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 37.0 / 100
- CVSS v3.1: not applicable

Functions guarded by owner/role modifiers: setBaseDelaySeconds, setAccessManagerIgnored. (related: —)

**Potential impact.** Centralization risk: compromise of the admin key compromises the protocol.

**Reproduction steps.**

```
Open contract in the supplied file contracts/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorTimelockAccess.sol and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [contracts/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorTimelockAccess.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorTimelockAccess.sol) · multiple · SHA-256 f2f0ae2a1314268db485c56a4fe1f2d974856fd30405d8e1b223f1102f2a16d6_

```
Privileged functions: setBaseDelaySeconds, setAccessManagerIgnored
```

**Limitations of the check.** Lightweight static pattern analysis of Solidity source without compilation or symbolic execution. It does not replace a full smart-contract audit; confirm manually or with dedicated tools (Slither, Foundry tests).

**Recommendation.** Use a multisig/timelock for admin roles and document them.

**Retest procedure.** Re-run static analysis and add a unit/fuzz test that exercises the pattern.

### QSI-2026-19478 — Privileged administrative functions in contracts/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorTimelockCompound.sol: updateTimelock

- Severity: **Info** · Classification: Improvement recommendation · Confidence: High
- Affected asset: `contract:contracts/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorTimelockCompound.sol`
- Data source: contracts/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorTimelockCompound.sol
- Detection method: Solidity source pattern analysis.
- Analyzer: solidity 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 37.0 / 100
- CVSS v3.1: not applicable

Functions guarded by owner/role modifiers: updateTimelock. (related: —)

**Potential impact.** Centralization risk: compromise of the admin key compromises the protocol.

**Reproduction steps.**

```
Open contract in the supplied file contracts/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorTimelockCompound.sol and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [contracts/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorTimelockCompound.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorTimelockCompound.sol) · multiple · SHA-256 825de8a0266ca176b55c917fd9450222f4d40ce841c16a9f026715c5a07f3d75_

```
Privileged functions: updateTimelock
```

**Limitations of the check.** Lightweight static pattern analysis of Solidity source without compilation or symbolic execution. It does not replace a full smart-contract audit; confirm manually or with dedicated tools (Slither, Foundry tests).

**Recommendation.** Use a multisig/timelock for admin roles and document them.

**Retest procedure.** Re-run static analysis and add a unit/fuzz test that exercises the pattern.

### QSI-2026-19479 — Privileged administrative functions in contracts/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorTimelockControl.sol: updateTimelock

- Severity: **Info** · Classification: Improvement recommendation · Confidence: High
- Affected asset: `contract:contracts/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorTimelockControl.sol`
- Data source: contracts/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorTimelockControl.sol
- Detection method: Solidity source pattern analysis.
- Analyzer: solidity 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 37.0 / 100
- CVSS v3.1: not applicable

Functions guarded by owner/role modifiers: updateTimelock. (related: —)

**Potential impact.** Centralization risk: compromise of the admin key compromises the protocol.

**Reproduction steps.**

```
Open contract in the supplied file contracts/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorTimelockControl.sol and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [contracts/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorTimelockControl.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorTimelockControl.sol) · multiple · SHA-256 825de8a0266ca176b55c917fd9450222f4d40ce841c16a9f026715c5a07f3d75_

```
Privileged functions: updateTimelock
```

**Limitations of the check.** Lightweight static pattern analysis of Solidity source without compilation or symbolic execution. It does not replace a full smart-contract audit; confirm manually or with dedicated tools (Slither, Foundry tests).

**Recommendation.** Use a multisig/timelock for admin roles and document them.

**Retest procedure.** Re-run static analysis and add a unit/fuzz test that exercises the pattern.

### QSI-2026-19480 — Privileged administrative functions in contracts/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorVotesQuorumFraction.sol: updateQuorumNumerator

- Severity: **Info** · Classification: Improvement recommendation · Confidence: High
- Affected asset: `contract:contracts/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorVotesQuorumFraction.sol`
- Data source: contracts/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorVotesQuorumFraction.sol
- Detection method: Solidity source pattern analysis.
- Analyzer: solidity 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 37.0 / 100
- CVSS v3.1: not applicable

Functions guarded by owner/role modifiers: updateQuorumNumerator. (related: —)

**Potential impact.** Centralization risk: compromise of the admin key compromises the protocol.

**Reproduction steps.**

```
Open contract in the supplied file contracts/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorVotesQuorumFraction.sol and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [contracts/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorVotesQuorumFraction.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorVotesQuorumFraction.sol) · multiple · SHA-256 37d9e023fde908bbc2e9347f91ad2aa3006ddd93480c2ac0413f2847e2b727b4_

```
Privileged functions: updateQuorumNumerator
```

**Limitations of the check.** Lightweight static pattern analysis of Solidity source without compilation or symbolic execution. It does not replace a full smart-contract audit; confirm manually or with dedicated tools (Slither, Foundry tests).

**Recommendation.** Use a multisig/timelock for admin roles and document them.

**Retest procedure.** Re-run static analysis and add a unit/fuzz test that exercises the pattern.

### QSI-2026-19481 — Privileged administrative functions in contracts/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorVotesSuperQuorumFraction.sol: updateSuperQuorumNumerator

- Severity: **Info** · Classification: Improvement recommendation · Confidence: High
- Affected asset: `contract:contracts/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorVotesSuperQuorumFraction.sol`
- Data source: contracts/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorVotesSuperQuorumFraction.sol
- Detection method: Solidity source pattern analysis.
- Analyzer: solidity 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 37.0 / 100
- CVSS v3.1: not applicable

Functions guarded by owner/role modifiers: updateSuperQuorumNumerator. (related: —)

**Potential impact.** Centralization risk: compromise of the admin key compromises the protocol.

**Reproduction steps.**

```
Open contract in the supplied file contracts/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorVotesSuperQuorumFraction.sol and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [contracts/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorVotesSuperQuorumFraction.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorVotesSuperQuorumFraction.sol) · multiple · SHA-256 07f49116aa90ff89ec6b7b7d0820cc65a342e480d922ad1f7209983948f77120_

```
Privileged functions: updateSuperQuorumNumerator
```

**Limitations of the check.** Lightweight static pattern analysis of Solidity source without compilation or symbolic execution. It does not replace a full smart-contract audit; confirm manually or with dedicated tools (Slither, Foundry tests).

**Recommendation.** Use a multisig/timelock for admin roles and document them.

**Retest procedure.** Re-run static analysis and add a unit/fuzz test that exercises the pattern.

### QSI-2026-19482 — Privileged administrative functions in contracts/lib/openzeppelin-contracts/contracts/proxy/beacon/UpgradeableBeacon.sol: upgradeTo

- Severity: **Info** · Classification: Improvement recommendation · Confidence: High
- Affected asset: `contract:contracts/lib/openzeppelin-contracts/contracts/proxy/beacon/UpgradeableBeacon.sol`
- Data source: contracts/lib/openzeppelin-contracts/contracts/proxy/beacon/UpgradeableBeacon.sol
- Detection method: Solidity source pattern analysis.
- Analyzer: solidity 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 37.0 / 100
- CVSS v3.1: not applicable

Functions guarded by owner/role modifiers: upgradeTo. (related: —)

**Potential impact.** Centralization risk: compromise of the admin key compromises the protocol.

**Reproduction steps.**

```
Open contract in the supplied file contracts/lib/openzeppelin-contracts/contracts/proxy/beacon/UpgradeableBeacon.sol and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [contracts/lib/openzeppelin-contracts/contracts/proxy/beacon/UpgradeableBeacon.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts/contracts/proxy/beacon/UpgradeableBeacon.sol) · multiple · SHA-256 02e606b6560ec4a99c06589dd8655178cca253b457dcec0438b77dd4a8cb04f5_

```
Privileged functions: upgradeTo
```

**Limitations of the check.** Lightweight static pattern analysis of Solidity source without compilation or symbolic execution. It does not replace a full smart-contract audit; confirm manually or with dedicated tools (Slither, Foundry tests).

**Recommendation.** Use a multisig/timelock for admin roles and document them.

**Retest procedure.** Re-run static analysis and add a unit/fuzz test that exercises the pattern.

### QSI-2026-19483 — Privileged administrative functions in contracts/lib/openzeppelin-contracts/contracts/proxy/transparent/ProxyAdmin.sol: upgradeAndCall

- Severity: **Info** · Classification: Improvement recommendation · Confidence: High
- Affected asset: `contract:contracts/lib/openzeppelin-contracts/contracts/proxy/transparent/ProxyAdmin.sol`
- Data source: contracts/lib/openzeppelin-contracts/contracts/proxy/transparent/ProxyAdmin.sol
- Detection method: Solidity source pattern analysis.
- Analyzer: solidity 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 37.0 / 100
- CVSS v3.1: not applicable

Functions guarded by owner/role modifiers: upgradeAndCall. (related: —)

**Potential impact.** Centralization risk: compromise of the admin key compromises the protocol.

**Reproduction steps.**

```
Open contract in the supplied file contracts/lib/openzeppelin-contracts/contracts/proxy/transparent/ProxyAdmin.sol and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [contracts/lib/openzeppelin-contracts/contracts/proxy/transparent/ProxyAdmin.sol](https://github.com/circlefin/arc-node/blob/6e764023ee6515fe70573e123ed2db912a7207b4/contracts/lib/openzeppelin-contracts/contracts/proxy/transparent/ProxyAdmin.sol) · multiple · SHA-256 08d87f8ddab73b6f3211d313d176dd5e3323cdca43425bff268f49bee3960937_

```
Privileged functions: upgradeAndCall
```

**Limitations of the check.** Lightweight static pattern analysis of Solidity source without compilation or symbolic execution. It does not replace a full smart-contract audit; confirm manually or with dedicated tools (Slither, Foundry tests).

**Recommendation.** Use a multisig/timelock for admin roles and document them.

**Retest procedure.** Re-run static analysis and add a unit/fuzz test that exercises the pattern.

### QSI-2026-19538 — tokio 1.52.3 is affected by RUSTSEC-2026-0386 (no severity rating)

- Severity: **Info** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/tokio@1.52.3`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 17.8 / 100
- CVSS v3.1: not applicable

OSV.dev reports RUSTSEC-2026-0386 for crates.io package tokio at version 1.52.3: `AsyncFd::new` and related constructors violate I/O safety. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. None of the affected functions (tokio::io::unix::AsyncFd::new, tokio::io::unix::AsyncFd::try_new, tokio::io::unix::AsyncFd::try_with_interest, tokio::io::unix::AsyncFd::with_interest) is named in the audited code: the advisory does not apply unless they are reached indirectly (traits, macros, other dependencies).

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

### QSI-2026-19539 — 1 advisories in 1 development or build-only crates.io package(s)

- Severity: **Info** · Classification: Improvement recommendation · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `dependencies:crates.io:non-runtime`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch lookup of exact versions; scope from devDependencies, package-lock.json dev flags, pnpm importers sections, the Cargo.lock graph rooted at the Cargo.toml tables, and — for yarn.lock, which records no scope — the lock graph walked from package.json. Where a runtime requirement cannot be resolved in a lock, that lock is left unclassified rather than risking a package being set aside wrongly.
- Analyzer: dependencies 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 15.5 / 100
- CVSS v3.1: not applicable

OSV.dev lists 1 advisories (0 rated high or critical) for 1 crates.io package(s) that only development or build tooling pulls in (Cargo.lock): e.g. scc@2.4.0 [dev]: RUSTSEC-2026-0205. The manifests mark them as such (devDependencies, "dev": true in package-lock.json, pnpm importers sections, [dev-dependencies]/[build-dependencies] reached through Cargo.lock, or — for yarn.lock, which records no scope at all — package.json reached through the lock graph), so they are not part of what ships.

**Potential impact.** They do not reach users of the product. They can affect developer machines and CI (supply chain): a compromised or vulnerable tool can tamper with builds.

**Reproduction steps.**

```
Look the packages listed in the evidence up at https://osv.dev and check their scope in Cargo.lock.
```

**Evidence.**

_tool_output · [OSV.dev (crates.io)](https://osv.dev/) · Cargo.lock · SHA-256 5e007e5af8431c90b8e66223e349bc9b101c9c1051b17b2b53bf779e045d124a_

```
scc@2.4.0 [dev]: RUSTSEC-2026-0205
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Scopes come from the manifests; a registry crate's own build dependencies cannot be told apart in Cargo.lock, so the runtime set may be larger than reality, never smaller.

**Recommendation.** Update the tooling during routine maintenance; prioritise packages that run in CI with secrets or that produce release artefacts.

**Retest procedure.** Re-run the dependency scan after updating.

### QSI-2026-19487 — bincode 1.3.3: informational advisory RUSTSEC-2025-0141 (unmaintained)

- Severity: **Info** · Classification: Improvement recommendation · Confidence: Low
- Affected asset: `dependency:crates.io/bincode@1.3.3`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 11.8 / 100
- CVSS v3.1: not applicable

OSV.dev lists RUSTSEC-2025-0141 for crates.io package bincode at version 1.3.3 as informational (unmaintained): Bincode is unmaintained. It reports no vulnerability; an unmaintained package will not receive fixes for future ones.

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

### QSI-2026-19489 — bitmaps 3.2.1: informational advisory RUSTSEC-2026-0247 (unmaintained)

- Severity: **Info** · Classification: Improvement recommendation · Confidence: Low
- Affected asset: `dependency:crates.io/bitmaps@3.2.1`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 11.8 / 100
- CVSS v3.1: not applicable

OSV.dev lists RUSTSEC-2026-0247 for crates.io package bitmaps at version 3.2.1 as informational (unmaintained): bitmaps is unmaintained. It reports no vulnerability; an unmaintained package will not receive fixes for future ones.

**Potential impact.** No known vulnerability. Future security fixes may not be released.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0247
```

**Evidence.**

_tool_output · [OSV.dev RUSTSEC-2026-0247](https://osv.dev/vulnerability/RUSTSEC-2026-0247) · manifest · SHA-256 0490df19bf77e9550b234acd867daf2068a02e110718d7cc15521f8ac2a12dfd_

```
{"id": "RUSTSEC-2026-0247", "aliases": [], "modified": "2026-08-10T19:45:04.540318330Z", "summary": "bitmaps is unmaintained", "severity": null, "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time.

**Recommendation.** Plan a move to a maintained alternative, or record the decision to keep it.

**Retest procedure.** Re-run the dependency scan after the change.

### QSI-2026-19492 — core2 0.4.0: informational advisory RUSTSEC-2026-0105 (unmaintained)

- Severity: **Info** · Classification: Improvement recommendation · Confidence: Low
- Affected asset: `dependency:crates.io/core2@0.4.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 11.8 / 100
- CVSS v3.1: not applicable

OSV.dev lists RUSTSEC-2026-0105 for crates.io package core2 at version 0.4.0 as informational (unmaintained): core2 is unmaintained, all versions yanked. It reports no vulnerability; an unmaintained package will not receive fixes for future ones.

**Potential impact.** No known vulnerability. Future security fixes may not be released.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0105
```

**Evidence.**

_tool_output · [OSV.dev RUSTSEC-2026-0105](https://osv.dev/vulnerability/RUSTSEC-2026-0105) · manifest · SHA-256 9c8a7a39cf41d1c8cae299044e250afa162c3875e01d87a435c06aafeea4fd1b_

```
{"id": "RUSTSEC-2026-0105", "aliases": [], "modified": "2026-04-25T15:15:06.139681Z", "summary": "core2 is unmaintained, all versions yanked", "severity": null, "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time.

**Recommendation.** Plan a move to a maintained alternative, or record the decision to keep it.

**Retest procedure.** Re-run the dependency scan after the change.

### QSI-2026-19495 — derivative 2.2.0: informational advisory RUSTSEC-2024-0388 (unmaintained)

- Severity: **Info** · Classification: Improvement recommendation · Confidence: Low
- Affected asset: `dependency:crates.io/derivative@2.2.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 11.8 / 100
- CVSS v3.1: not applicable

OSV.dev lists RUSTSEC-2024-0388 for crates.io package derivative at version 2.2.0 as informational (unmaintained): `derivative` is unmaintained; consider using an alternative. It reports no vulnerability; an unmaintained package will not receive fixes for future ones.

**Potential impact.** No known vulnerability. Future security fixes may not be released.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2024-0388
```

**Evidence.**

_tool_output · [OSV.dev RUSTSEC-2024-0388](https://osv.dev/vulnerability/RUSTSEC-2024-0388) · manifest · SHA-256 3438f6c3cab3309fb6388762a19097619076b18baff08e3e9ab34fa969478d55_

```
{"id": "RUSTSEC-2024-0388", "aliases": [], "modified": "2024-11-10T13:34:40Z", "summary": "`derivative` is unmaintained; consider using an alternative", "severity": null, "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time.

**Recommendation.** Plan a move to a maintained alternative, or record the decision to keep it.

**Retest procedure.** Re-run the dependency scan after the change.

### QSI-2026-19517 — paste 1.0.15: informational advisory RUSTSEC-2024-0436 (unmaintained)

- Severity: **Info** · Classification: Improvement recommendation · Confidence: Low
- Affected asset: `dependency:crates.io/paste@1.0.15`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 11.8 / 100
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

### QSI-2026-19518 — pin-utils 0.1.0: informational advisory RUSTSEC-2026-0441 (unmaintained)

- Severity: **Info** · Classification: Improvement recommendation · Confidence: Low
- Affected asset: `dependency:crates.io/pin-utils@0.1.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 11.8 / 100
- CVSS v3.1: not applicable

OSV.dev lists RUSTSEC-2026-0441 for crates.io package pin-utils at version 0.1.0 as informational (unmaintained): `pin-utils` is unmaintained. It reports no vulnerability; an unmaintained package will not receive fixes for future ones.

**Potential impact.** No known vulnerability. Future security fixes may not be released.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0441
```

**Evidence.**

_tool_output · [OSV.dev RUSTSEC-2026-0441](https://osv.dev/vulnerability/RUSTSEC-2026-0441) · manifest · SHA-256 514334496eebf73f46fcfef878104d886070964aa0d513b9f9078d9475b291ad_

```
{"id": "RUSTSEC-2026-0441", "aliases": [], "modified": "2026-11-05T09:00:02.627533155Z", "summary": "`pin-utils` is unmaintained", "severity": null, "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time.

**Recommendation.** Plan a move to a maintained alternative, or record the decision to keep it.

**Retest procedure.** Re-run the dependency scan after the change.

### QSI-2026-19519 — proc-macro-error2 2.0.1: informational advisory RUSTSEC-2026-0173 (unmaintained)

- Severity: **Info** · Classification: Improvement recommendation · Confidence: Low
- Affected asset: `dependency:crates.io/proc-macro-error2@2.0.1`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 11.8 / 100
- CVSS v3.1: not applicable

OSV.dev lists RUSTSEC-2026-0173 for crates.io package proc-macro-error2 at version 2.0.1 as informational (unmaintained): proc-macro-error2 is unmaintained. It reports no vulnerability; an unmaintained package will not receive fixes for future ones.

**Potential impact.** No known vulnerability. Future security fixes may not be released.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0173
```

**Evidence.**

_tool_output · [OSV.dev RUSTSEC-2026-0173](https://osv.dev/vulnerability/RUSTSEC-2026-0173) · manifest · SHA-256 0ecc182141bd9effc6d35bc24dc20c57e6473fb3877ad59a5fbdb1cd55b56528_

```
{"id": "RUSTSEC-2026-0173", "aliases": [], "modified": "2026-06-07T21:00:04.318567692Z", "summary": "proc-macro-error2 is unmaintained", "severity": null, "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time.

**Recommendation.** Plan a move to a maintained alternative, or record the decision to keep it.

**Retest procedure.** Re-run the dependency scan after the change.

### QSI-2026-19534 — rustls-pemfile 2.2.0: informational advisory RUSTSEC-2025-0134 (unmaintained)

- Severity: **Info** · Classification: Improvement recommendation · Confidence: Low
- Affected asset: `dependency:crates.io/rustls-pemfile@2.2.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 15:31 UTC
- Priority score: 11.8 / 100
- CVSS v3.1: not applicable

OSV.dev lists RUSTSEC-2025-0134 for crates.io package rustls-pemfile at version 2.2.0 as informational (unmaintained): rustls-pemfile is unmaintained. It reports no vulnerability; an unmaintained package will not receive fixes for future ones.

**Potential impact.** No known vulnerability. Future security fixes may not be released.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2025-0134
```

**Evidence.**

_tool_output · [OSV.dev RUSTSEC-2025-0134](https://osv.dev/vulnerability/RUSTSEC-2025-0134) · manifest · SHA-256 8a337a969850fe57bfcbd48340c157654002251ff4155f018ebd3fc00f0657fc_

```
{"id": "RUSTSEC-2025-0134", "aliases": [], "modified": "2025-12-05T19:07:59.622592Z", "summary": "rustls-pemfile is unmaintained", "severity": null, "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time.

**Recommendation.** Plan a move to a maintained alternative, or record the decision to keep it.

**Retest procedure.** Re-run the dependency scan after the change.


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

- In use: SLH-DSA — crates/pq-precompile/src/lib.rs
- In use: SLH-DSA — crates/precompiles/src/bin/generate_pq_test_vectors.rs
- In use: SLH-DSA — crates/precompiles/src/pq_test_vectors.rs
- A post-quantum library is declared as a dependency

**Next step:** Extend post-quantum protection to the critical roles that stay classical, starting with what can be recorded today (wrapped keys, channel key exchange).

_Levels: 0 none; 1 present, not wired; 2 in use outside the critical paths; 3 hybrid in a critical path; 4 post-quantum by default in the critical paths (root of trust, key wrapping, channel key exchange). Judged from code and manifests._

### What the quantum-vulnerable algorithms do

| Role | Algorithms (files) | ID | First step |
|---|---|---|---|
| **transaction and message signing** | ECDSA (4), Ed25519 (1) | QSI-2026-19421, QSI-2026-19422 | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains adopt them |
| **role not determined** | Ed25519 (4), ECDSA (2) | QSI-2026-19420, QSI-2026-19423 | Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it; introduce an abstraction layer for crypto-agility |

_Roles are judged from file paths, function names and the code around each match; review confirms them. Root-of-trust keys and wrapped keys come first: they are hard to replace or can be recorded today._
No readiness questionnaire was completed for this project.

### Quantum algorithms relevant to this inventory

| Quantum algorithm | Effect | Attack model | Inventoried algorithms (rows) | What it means for this audit |
|---|---|---|---|---|
| Shor's algorithm — elliptic-curve discrete logarithms | breaks | Q1 | ECDSA (9), Ed25519 (5) | Elliptic-curve keys are expected to fall before RSA keys of comparable classical strength. On blockchains, coins whose public key is already on chain (reused addresses, pay-to-public-key and Taproot outputs) are exposed first; plan the move to post-quantum signatures and avoid key reuse in the meantime. |
| Grover's algorithm — key search and preimages | weakens (larger keys restore the margin) | Q1 | Keccak-256 (90), SLH-DSA (4) | Not a break. 256-bit keys (AES-256, ChaCha20) keep a comfortable margin; AES-128 meets NIST category 1, while some authorities ask for 256-bit keys in quantum-resistant contexts (see the AES-128 entry). Prefer 256-bit keys for long-lived data; 256-bit hashes need no change for preimage resistance. |
| Brassard–Høyer–Tapp — collision search | weakens (larger keys restore the margin) | Q1 | Keccak-256 (90) | 256-bit hashes (SHA-256, SHA3-256) remain adequate for collision resistance; 160-bit hashes are already weak classically (SHA-1 collisions are practical). Use 384/512-bit hashes where NIST categories 4–5 are required. |

_Effects: breaks — replace the algorithm; weakens — larger keys or outputs restore the margin; included in standard parameters — no action at standard parameter sets; only with superposition queries — not applicable to ordinary deployments._


## 9. Limitations and assumptions

- This report presents automated and documented analysis results for the stated scope. It is not a legal opinion, a certification or an attestation of compliance with any standard.
- z is a planning assumption chosen per risk profile, not a prediction. A cryptographically relevant quantum computer is not publicly known to exist today.
- slither: 590 (examples: slither is not installed on the server (pip install slither-analyzer + solc))
- osv_advisories: 1 (examples: 125 package(s) are built from git repositories (forks or unreleased code), so registry advisories were not looked up for them: arc-malachitebft-app, arc-malachitebft-app-channel, arc-malachitebft-codec, arc-malachitebft-config, arc-malachitebft-core-consensus, arc-malachitebft-core-driver, arc-malachitebft-core-state-machine, arc-malachitebft-core-types, arc-malachitebft-core-votekeeper, arc-malachitebft-discovery, arc-malachitebft-engine, arc-malachitebft-engine-byzantine …)

## 10. Remediation plan / Priorities for 30, 60 and 90 days

### 30 days

| Priority | ID | Action | Type | Closure criteria |
|---|---|---|---|---|
| P1 | QSI-2026-19441 | Rotate and remove secrets found in contracts/lib/openzeppelin-contracts-upgradeable/contracts/token/ERC6909/extensions/draft-ERC6909TokenSupplyUpgradeable.sol. | root-cause fix | Secret scanner reports no secrets; old values revoked. |
| P1 | QSI-2026-19449 | Restrict delegatecall targets to trusted, immutable implementations. | root-cause fix | Re-run static analysis and add a unit/fuzz test that exercises the pattern. |
| P1 | QSI-2026-19465 | Restrict delegatecall targets to trusted, immutable implementations. | root-cause fix | Re-run static analysis and add a unit/fuzz test that exercises the pattern. |
| P1 | QSI-2026-19472 | Restrict delegatecall targets to trusted, immutable implementations. | root-cause fix | Re-run static analysis and add a unit/fuzz test that exercises the pattern. |
| P1 | QSI-2026-19484 | Restrict delegatecall targets to trusted, immutable implementations. | root-cause fix | Re-run static analysis and add a unit/fuzz test that exercises the pattern. |
| P2 | QSI-2026-19526 | Upgrade rmcp to a fixed version (2.0.0). | root-cause fix | Dependency scan no longer reports GHSA-33f5-2c5q-wgwj (CVE-2026-63127). |
| P2 | QSI-2026-19528 | Upgrade rmcp to a fixed version (2.0.0). | root-cause fix | Dependency scan no longer reports GHSA-9pj6-vhgr-3mwh (CVE-2026-63128). |
| P2 | QSI-2026-19499 | Upgrade hickory-proto to a fixed version (0.26.0-beta.1). | root-cause fix | Dependency scan no longer reports GHSA-3v94-mw7p-v465 (RUSTSEC-2026-0118). |
| P2 | QSI-2026-19501 | Upgrade hickory-resolver to a fixed version (0.26.2). | root-cause fix | Dependency scan no longer reports GHSA-5j98-2g5x-46v6 (CVE-2026-93657). |
| P2 | QSI-2026-19505 | Upgrade libp2p-quic to a fixed version (0.13.1). | root-cause fix | Dependency scan no longer reports GHSA-5hq8-qhww-jm7q (CVE-2026-61544). |
| P2 | QSI-2026-19508 | Upgrade openssl to a fixed version (0.10.78). | root-cause fix | Dependency scan no longer reports GHSA-8c75-8mhr-p7r9 (CVE-2026-41678). |
| P2 | QSI-2026-19509 | Upgrade openssl to a fixed version (0.10.78). | root-cause fix | Dependency scan no longer reports GHSA-ghm9-cr32-g9qj (CVE-2026-41681). |
| P2 | QSI-2026-19510 | Upgrade openssl to a fixed version (0.10.78). | root-cause fix | Dependency scan no longer reports GHSA-hppc-g8h3-xhp3 (CVE-2026-41898). |
| P2 | QSI-2026-19512 | Upgrade openssl to a fixed version (0.10.78). | root-cause fix | Dependency scan no longer reports GHSA-pqf5-4pqq-29f5 (CVE-2026-41676). |
| P2 | QSI-2026-19514 | Upgrade openssl to a fixed version (0.10.79). | root-cause fix | Dependency scan no longer reports GHSA-xp3w-r5p5-63rr (CVE-2026-42327). |
| P2 | QSI-2026-19522 | Upgrade quinn-proto to a fixed version (0.11.18). | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0340. |
| P2 | QSI-2026-19523 | Upgrade quinn-proto to a fixed version (0.11.17). | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0341. |
| P2 | QSI-2026-19504 | Upgrade jsonwebtoken to a fixed version (10.3.0). | root-cause fix | Dependency scan no longer reports GHSA-h395-gr6q-cpjc (CVE-2026-25537). |
| P2 | QSI-2026-19527 | Upgrade rmcp to a fixed version (2.1.0). | root-cause fix | Dependency scan no longer reports GHSA-9g45-5xwm-f3wc (CVE-2026-64684). |
| P2 | QSI-2026-19529 | Upgrade rmcp to a fixed version (2.0.0). | root-cause fix | Dependency scan no longer reports GHSA-c9xm-49cp-xcr9. |
| P2 | QSI-2026-19536 | Upgrade serde_with to a fixed version (3.21.0). | root-cause fix | Dependency scan no longer reports GHSA-7gcf-g7xr-8hxj. |
| P2 | QSI-2026-19537 | Upgrade tar to a fixed version (0.4.46). | root-cause fix | Dependency scan no longer reports GHSA-3pv8-6f4r-ffg2. |
| P2 | QSI-2026-19490 | Upgrade block-buffer to a fixed version (none published yet; see the advisory for mitigations). | root-cause fix | Dependency scan no longer reports GHSA-qwgh-2vcv-g2f7. |
| P2 | QSI-2026-19491 | Upgrade cmov to a fixed version (0.5.4). | root-cause fix | Dependency scan no longer reports GHSA-3rjw-m598-pq24 (CVE-2026-50185). |
| P2 | QSI-2026-19500 | Upgrade hickory-proto to a fixed version (0.26.1). | root-cause fix | Dependency scan no longer reports GHSA-q2qq-hmj6-3wpp (RUSTSEC-2026-0119). |
| P2 | QSI-2026-19502 | Upgrade hickory-resolver to a fixed version (0.26.2). | root-cause fix | Dependency scan no longer reports GHSA-6f2x-v7q7-m7m5. |
| P2 | QSI-2026-19511 | Upgrade openssl to a fixed version (0.10.80). | root-cause fix | Dependency scan no longer reports GHSA-phqj-4mhp-q6mq (CVE-2026-45784). |
| P2 | QSI-2026-19515 | Upgrade openssl to a fixed version (0.10.79). | root-cause fix | Dependency scan no longer reports GHSA-xv59-967r-8726 (CVE-2026-44662). |
| P2 | QSI-2026-19516 | Upgrade opentelemetry_sdk to a fixed version (0.32.1). | root-cause fix | Dependency scan no longer reports GHSA-w9wp-h8wv-79jx (CVE-2026-48504). |
| P2 | QSI-2026-19530 | Upgrade rustls to a fixed version (0.23.45). | root-cause fix | Dependency scan no longer reports GHSA-2mjx-qc3c-rqvc (RUSTSEC-2026-0285). |
| P2 | QSI-2026-19531 | Upgrade rustls to a fixed version (0.23.46, 0.24.0-dev.2). | root-cause fix | Dependency scan no longer reports GHSA-c8m5-c952-6cm4 (RUSTSEC-2026-0346). |
| P2 | QSI-2026-19525 | Upgrade rand to a fixed version (0.10.1, 0.8.6, 0.9.3). | root-cause fix | Dependency scan no longer reports GHSA-cq8v-f236-94qc (RUSTSEC-2026-0097). |
| P2 | QSI-2026-19513 | Upgrade openssl to a fixed version (0.10.78). | root-cause fix | Dependency scan no longer reports GHSA-xmgf-hq76-4vx2 (CVE-2026-41677). |
| P2 | QSI-2026-19533 | Upgrade rustls to a fixed version (0.23.46, 0.24.0-dev.2). | root-cause fix | Dependency scan no longer reports GHSA-w44r-93j7-qv28 (RUSTSEC-2026-0349). |
| P2 | QSI-2026-19532 | Upgrade rustls to a fixed version (0.23.46, 0.24.0-dev.2). | root-cause fix | Dependency scan no longer reports GHSA-h2v8-394m-p7vv (RUSTSEC-2026-0348). |
### 60 days

| Priority | ID | Action | Type | Closure criteria |
|---|---|---|---|---|
| P2 | QSI-2026-19466 | Use OpenZeppelin ECDSA.recover with EIP-712 domain separation and nonces. | root-cause fix | Re-run static analysis and add a unit/fuzz test that exercises the pattern. |
| P2 | QSI-2026-19485 | Use OpenZeppelin ECDSA.recover with EIP-712 domain separation and nonces. | root-cause fix | Re-run static analysis and add a unit/fuzz test that exercises the pattern. |
| P3 | QSI-2026-19486 | Triage RUSTSEC-2026-0190; upgrade anyhow to a fixed version (1.0.103) if it applies. | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0190, or the triage is recorded. |
| P3 | QSI-2026-19488 | Triage RUSTSEC-2025-0167; upgrade bitmaps to a fixed version (none published yet; see the advisory for mitigations) if it applies. | root-cause fix | Dependency scan no longer reports RUSTSEC-2025-0167, or the triage is recorded. |
| P3 | QSI-2026-19493 | Triage RUSTSEC-2026-0387; upgrade crypto-bigint to a fixed version (0.7.6) if it applies. | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0387, or the triage is recorded. |
| P3 | QSI-2026-19494 | Triage RUSTSEC-2026-0385; upgrade ctutils to a fixed version (0.4.4) if it applies. | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0385, or the triage is recorded. |
| P3 | QSI-2026-19496 | Triage RUSTSEC-2026-0221; upgrade event-listener to a fixed version (5.4.2) if it applies. | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0221, or the triage is recorded. |
| P3 | QSI-2026-19497 | Triage RUSTSEC-2026-0183; upgrade git2 to a fixed version (0.21.0) if it applies. | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0183, or the triage is recorded. |
| P3 | QSI-2026-19498 | Triage RUSTSEC-2026-0184; upgrade git2 to a fixed version (0.21.0) if it applies. | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0184, or the triage is recorded. |
| P3 | QSI-2026-19503 | Triage RUSTSEC-2026-0292; upgrade imbl-sized-chunks to a fixed version (0.2.0) if it applies. | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0292, or the triage is recorded. |
| P3 | QSI-2026-19506 | Triage RUSTSEC-2026-0418; upgrade libz-sys to a fixed version (1.1.31) if it applies. | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0418, or the triage is recorded. |
| P3 | QSI-2026-19507 | Triage RUSTSEC-2026-0253; upgrade lru to a fixed version (0.18.2) if it applies. | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0253, or the triage is recorded. |
| P3 | QSI-2026-19520 | Triage RUSTSEC-2026-0338; upgrade quinn-proto to a fixed version (0.11.18) if it applies. | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0338, or the triage is recorded. |
| P3 | QSI-2026-19521 | Triage RUSTSEC-2026-0339; upgrade quinn-proto to a fixed version (0.11.17) if it applies. | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0339, or the triage is recorded. |
| P3 | QSI-2026-19524 | Triage RUSTSEC-2026-0342; upgrade quinn-proto to a fixed version (0.11.17) if it applies. | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0342, or the triage is recorded. |
| P3 | QSI-2026-19535 | Triage RUSTSEC-2026-0382 (CVE-2026-111943); upgrade rustls-webpki to a fixed version (0.103.16, 0.104.0-alpha.8) if it applies. | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0382 (CVE-2026-111943), or the triage is recorded. |
| P3 | QSI-2026-19538 | Triage RUSTSEC-2026-0386; upgrade tokio to a fixed version (1.51.6, 1.53.3) if it applies. | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0386, or the triage is recorded. |
### 90 days

| Priority | ID | Action | Type | Closure criteria |
|---|---|---|---|---|
| P3 | QSI-2026-19421 | Add Ed25519 usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-19422 | Add ECDSA usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-19420 | Add ECDSA usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-19423 | Add Ed25519 usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-19411 | Pin the compiler version used in testing. | root-cause fix | Re-run static analysis and add a unit/fuzz test that exercises the pattern. |
| P3 | QSI-2026-19424 | Pin the compiler version used in testing. | root-cause fix | Re-run static analysis and add a unit/fuzz test that exercises the pattern. |
| P3 | QSI-2026-19429 | Pin the compiler version used in testing. | root-cause fix | Re-run static analysis and add a unit/fuzz test that exercises the pattern. |
| P3 | QSI-2026-19430 | Pin the compiler version used in testing. | root-cause fix | Re-run static analysis and add a unit/fuzz test that exercises the pattern. |
| P3 | QSI-2026-19440 | Pin the compiler version used in testing. | root-cause fix | Re-run static analysis and add a unit/fuzz test that exercises the pattern. |
| P3 | QSI-2026-19442 | Pin the compiler version used in testing. | root-cause fix | Re-run static analysis and add a unit/fuzz test that exercises the pattern. |
| P3 | QSI-2026-19445 | Pin the compiler version used in testing. | root-cause fix | Re-run static analysis and add a unit/fuzz test that exercises the pattern. |
| P3 | QSI-2026-19448 | Pin the compiler version used in testing. | root-cause fix | Re-run static analysis and add a unit/fuzz test that exercises the pattern. |
| P3 | QSI-2026-19459 | Pin the compiler version used in testing. | root-cause fix | Re-run static analysis and add a unit/fuzz test that exercises the pattern. |
| P3 | QSI-2026-19460 | Pin the compiler version used in testing. | root-cause fix | Re-run static analysis and add a unit/fuzz test that exercises the pattern. |
| P3 | QSI-2026-19461 | Pin the compiler version used in testing. | root-cause fix | Re-run static analysis and add a unit/fuzz test that exercises the pattern. |
| P3 | QSI-2026-19462 | Pin the compiler version used in testing. | root-cause fix | Re-run static analysis and add a unit/fuzz test that exercises the pattern. |
| P3 | QSI-2026-19467 | Pin the compiler version used in testing. | root-cause fix | Re-run static analysis and add a unit/fuzz test that exercises the pattern. |
| P4 | QSI-2026-19421 | Plan migration of Ed25519 to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-19422 | Plan migration of ECDSA to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-19420 | Plan migration of ECDSA to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-19423 | Plan migration of Ed25519 to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-19412 | Use a multisig/timelock for admin roles and document them. | root-cause fix | Re-run static analysis and add a unit/fuzz test that exercises the pattern. |
| P4 | QSI-2026-19413 | Use a multisig/timelock for admin roles and document them. | root-cause fix | Re-run static analysis and add a unit/fuzz test that exercises the pattern. |
| P4 | QSI-2026-19414 | Use a multisig/timelock for admin roles and document them. | root-cause fix | Re-run static analysis and add a unit/fuzz test that exercises the pattern. |
| P4 | QSI-2026-19415 | Use a multisig/timelock for admin roles and document them. | root-cause fix | Re-run static analysis and add a unit/fuzz test that exercises the pattern. |
| P4 | QSI-2026-19416 | Use a multisig/timelock for admin roles and document them. | root-cause fix | Re-run static analysis and add a unit/fuzz test that exercises the pattern. |
| P4 | QSI-2026-19417 | Use a multisig/timelock for admin roles and document them. | root-cause fix | Re-run static analysis and add a unit/fuzz test that exercises the pattern. |
| P4 | QSI-2026-19418 | Use a multisig/timelock for admin roles and document them. | root-cause fix | Re-run static analysis and add a unit/fuzz test that exercises the pattern. |
| P4 | QSI-2026-19419 | Use a multisig/timelock for admin roles and document them. | root-cause fix | Re-run static analysis and add a unit/fuzz test that exercises the pattern. |
| P4 | QSI-2026-19425 | Use a multisig/timelock for admin roles and document them. | root-cause fix | Re-run static analysis and add a unit/fuzz test that exercises the pattern. |
| P4 | QSI-2026-19426 | Use a multisig/timelock for admin roles and document them. | root-cause fix | Re-run static analysis and add a unit/fuzz test that exercises the pattern. |
| P4 | QSI-2026-19427 | Use a multisig/timelock for admin roles and document them. | root-cause fix | Re-run static analysis and add a unit/fuzz test that exercises the pattern. |
| P4 | QSI-2026-19428 | Use a multisig/timelock for admin roles and document them. | root-cause fix | Re-run static analysis and add a unit/fuzz test that exercises the pattern. |
| P4 | QSI-2026-19431 | Use a multisig/timelock for admin roles and document them. | root-cause fix | Re-run static analysis and add a unit/fuzz test that exercises the pattern. |
| P4 | QSI-2026-19432 | Use a multisig/timelock for admin roles and document them. | root-cause fix | Re-run static analysis and add a unit/fuzz test that exercises the pattern. |
| P4 | QSI-2026-19433 | Use a multisig/timelock for admin roles and document them. | root-cause fix | Re-run static analysis and add a unit/fuzz test that exercises the pattern. |
| P4 | QSI-2026-19434 | Use a multisig/timelock for admin roles and document them. | root-cause fix | Re-run static analysis and add a unit/fuzz test that exercises the pattern. |
| P4 | QSI-2026-19435 | Use a multisig/timelock for admin roles and document them. | root-cause fix | Re-run static analysis and add a unit/fuzz test that exercises the pattern. |
| P4 | QSI-2026-19436 | Use a multisig/timelock for admin roles and document them. | root-cause fix | Re-run static analysis and add a unit/fuzz test that exercises the pattern. |
| P4 | QSI-2026-19437 | Use a multisig/timelock for admin roles and document them. | root-cause fix | Re-run static analysis and add a unit/fuzz test that exercises the pattern. |
| P4 | QSI-2026-19438 | Use a multisig/timelock for admin roles and document them. | root-cause fix | Re-run static analysis and add a unit/fuzz test that exercises the pattern. |
| P4 | QSI-2026-19439 | Use a multisig/timelock for admin roles and document them. | root-cause fix | Re-run static analysis and add a unit/fuzz test that exercises the pattern. |
| P4 | QSI-2026-19443 | Use a multisig/timelock for admin roles and document them. | root-cause fix | Re-run static analysis and add a unit/fuzz test that exercises the pattern. |
| P4 | QSI-2026-19444 | Use a multisig/timelock for admin roles and document them. | root-cause fix | Re-run static analysis and add a unit/fuzz test that exercises the pattern. |
| P4 | QSI-2026-19446 | Use a multisig/timelock for admin roles and document them. | root-cause fix | Re-run static analysis and add a unit/fuzz test that exercises the pattern. |
| P4 | QSI-2026-19447 | Use a multisig/timelock for admin roles and document them. | root-cause fix | Re-run static analysis and add a unit/fuzz test that exercises the pattern. |
| P4 | QSI-2026-19450 | Use a multisig/timelock for admin roles and document them. | root-cause fix | Re-run static analysis and add a unit/fuzz test that exercises the pattern. |
| P4 | QSI-2026-19451 | Use a multisig/timelock for admin roles and document them. | root-cause fix | Re-run static analysis and add a unit/fuzz test that exercises the pattern. |
| P4 | QSI-2026-19452 | Use a multisig/timelock for admin roles and document them. | root-cause fix | Re-run static analysis and add a unit/fuzz test that exercises the pattern. |
| P4 | QSI-2026-19453 | Use a multisig/timelock for admin roles and document them. | root-cause fix | Re-run static analysis and add a unit/fuzz test that exercises the pattern. |
| P4 | QSI-2026-19454 | Use a multisig/timelock for admin roles and document them. | root-cause fix | Re-run static analysis and add a unit/fuzz test that exercises the pattern. |
| P4 | QSI-2026-19455 | Use a multisig/timelock for admin roles and document them. | root-cause fix | Re-run static analysis and add a unit/fuzz test that exercises the pattern. |
| P4 | QSI-2026-19456 | Use a multisig/timelock for admin roles and document them. | root-cause fix | Re-run static analysis and add a unit/fuzz test that exercises the pattern. |
| P4 | QSI-2026-19457 | Use a multisig/timelock for admin roles and document them. | root-cause fix | Re-run static analysis and add a unit/fuzz test that exercises the pattern. |
| P4 | QSI-2026-19458 | Use a multisig/timelock for admin roles and document them. | root-cause fix | Re-run static analysis and add a unit/fuzz test that exercises the pattern. |
| P4 | QSI-2026-19463 | Use a multisig/timelock for admin roles and document them. | root-cause fix | Re-run static analysis and add a unit/fuzz test that exercises the pattern. |
| P4 | QSI-2026-19464 | Use a multisig/timelock for admin roles and document them. | root-cause fix | Re-run static analysis and add a unit/fuzz test that exercises the pattern. |
| P4 | QSI-2026-19468 | Use a multisig/timelock for admin roles and document them. | root-cause fix | Re-run static analysis and add a unit/fuzz test that exercises the pattern. |
| P4 | QSI-2026-19469 | Use a multisig/timelock for admin roles and document them. | root-cause fix | Re-run static analysis and add a unit/fuzz test that exercises the pattern. |
| P4 | QSI-2026-19470 | Use a multisig/timelock for admin roles and document them. | root-cause fix | Re-run static analysis and add a unit/fuzz test that exercises the pattern. |
| P4 | QSI-2026-19471 | Use a multisig/timelock for admin roles and document them. | root-cause fix | Re-run static analysis and add a unit/fuzz test that exercises the pattern. |
| P4 | QSI-2026-19473 | Use a multisig/timelock for admin roles and document them. | root-cause fix | Re-run static analysis and add a unit/fuzz test that exercises the pattern. |
| P4 | QSI-2026-19474 | Use a multisig/timelock for admin roles and document them. | root-cause fix | Re-run static analysis and add a unit/fuzz test that exercises the pattern. |
| P4 | QSI-2026-19475 | Use a multisig/timelock for admin roles and document them. | root-cause fix | Re-run static analysis and add a unit/fuzz test that exercises the pattern. |
| P4 | QSI-2026-19476 | Use a multisig/timelock for admin roles and document them. | root-cause fix | Re-run static analysis and add a unit/fuzz test that exercises the pattern. |
| P4 | QSI-2026-19477 | Use a multisig/timelock for admin roles and document them. | root-cause fix | Re-run static analysis and add a unit/fuzz test that exercises the pattern. |
| P4 | QSI-2026-19478 | Use a multisig/timelock for admin roles and document them. | root-cause fix | Re-run static analysis and add a unit/fuzz test that exercises the pattern. |
| P4 | QSI-2026-19479 | Use a multisig/timelock for admin roles and document them. | root-cause fix | Re-run static analysis and add a unit/fuzz test that exercises the pattern. |
| P4 | QSI-2026-19480 | Use a multisig/timelock for admin roles and document them. | root-cause fix | Re-run static analysis and add a unit/fuzz test that exercises the pattern. |
| P4 | QSI-2026-19481 | Use a multisig/timelock for admin roles and document them. | root-cause fix | Re-run static analysis and add a unit/fuzz test that exercises the pattern. |
| P4 | QSI-2026-19482 | Use a multisig/timelock for admin roles and document them. | root-cause fix | Re-run static analysis and add a unit/fuzz test that exercises the pattern. |
| P4 | QSI-2026-19483 | Use a multisig/timelock for admin roles and document them. | root-cause fix | Re-run static analysis and add a unit/fuzz test that exercises the pattern. |
| P4 | QSI-2026-19539 | Update the development and build dependencies listed in the evidence. | root-cause fix | The dependency scan reports no advisories for tooling packages, or the remaining ones are recorded. |
| P4 | QSI-2026-19487 | Replace bincode with a maintained alternative or record why it stays. | root-cause fix | bincode replaced, or the decision recorded. |
| P4 | QSI-2026-19489 | Replace bitmaps with a maintained alternative or record why it stays. | root-cause fix | bitmaps replaced, or the decision recorded. |
| P4 | QSI-2026-19492 | Replace core2 with a maintained alternative or record why it stays. | root-cause fix | core2 replaced, or the decision recorded. |
| P4 | QSI-2026-19495 | Replace derivative with a maintained alternative or record why it stays. | root-cause fix | derivative replaced, or the decision recorded. |
| P4 | QSI-2026-19517 | Replace paste with a maintained alternative or record why it stays. | root-cause fix | paste replaced, or the decision recorded. |
| P4 | QSI-2026-19518 | Replace pin-utils with a maintained alternative or record why it stays. | root-cause fix | pin-utils replaced, or the decision recorded. |
| P4 | QSI-2026-19519 | Replace proc-macro-error2 with a maintained alternative or record why it stays. | root-cause fix | proc-macro-error2 replaced, or the decision recorded. |
| P4 | QSI-2026-19534 | Replace rustls-pemfile with a maintained alternative or record why it stays. | root-cause fix | rustls-pemfile replaced, or the decision recorded. |

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
17. NIST IR 8547 — Transition to Post-Quantum Cryptography Standards — NIST. <https://csrc.nist.gov/pubs/ir/8547/final> (final (2026-10-27; the initial public draft of November 2024 is obsoleted). Tables 2 and 4: ECDSA, EdDSA and RSA signatures, finite-field and elliptic-curve DH and MQV, and RSA key establishment are deprecated after 2030 and disallowed after 2035 at every key size — the draft deprecated only the 112-bit level. A composite (hybrid) key establishment stays FIPS 140-validatable while one input comes from an approved scheme. Repeats the federal deadlines of OMB M-26-15: post-quantum key establishment by 2030-12-31 and signatures by 2031-12-31 for high value assets and high impact systems)
18. NIST — Post-Quantum Cryptography Standardization: Evaluation Criteria, Security (Call for Proposals, Section 4.A.5) — NIST. <https://csrc.nist.gov/Projects/Post-Quantum-Cryptography/Post-Quantum-Cryptography-Standardization/Evaluation-Criteria/Security-(Evaluation-Criteria)> (security categories: AES-128 key search 2^170/MAXDEPTH quantum gates, AES-192 2^233/MAXDEPTH, AES-256 2^298/MAXDEPTH; MAXDEPTH 2^40–2^96)
19. OSV advisory GHSA-2mjx-qc3c-rqvc — OSV.dev. <https://osv.dev/vulnerability/GHSA-2mjx-qc3c-rqvc> (modified 2026-10-27T15:30:05.509305490Z)
20. OSV advisory GHSA-33f5-2c5q-wgwj — OSV.dev. <https://osv.dev/vulnerability/GHSA-33f5-2c5q-wgwj> (modified 2026-09-16T22:30:08.107391372Z)
21. OSV advisory GHSA-3pv8-6f4r-ffg2 — OSV.dev. <https://osv.dev/vulnerability/GHSA-3pv8-6f4r-ffg2> (modified 2026-09-10T03:51:04.454810375Z)
22. OSV advisory GHSA-3rjw-m598-pq24 — OSV.dev. <https://osv.dev/vulnerability/GHSA-3rjw-m598-pq24> (modified 2026-09-10T03:51:10.250390903Z)
23. OSV advisory GHSA-3v94-mw7p-v465 — OSV.dev. <https://osv.dev/vulnerability/GHSA-3v94-mw7p-v465> (modified 2026-09-10T03:50:45.304576252Z)
24. OSV advisory GHSA-5hq8-qhww-jm7q — OSV.dev. <https://osv.dev/vulnerability/GHSA-5hq8-qhww-jm7q> (modified 2026-09-15T20:15:04.814697144Z)
25. OSV advisory GHSA-5j98-2g5x-46v6 — OSV.dev. <https://osv.dev/vulnerability/GHSA-5j98-2g5x-46v6> (modified 2026-10-05T23:00:04.250222435Z)
26. OSV advisory GHSA-6f2x-v7q7-m7m5 — OSV.dev. <https://osv.dev/vulnerability/GHSA-6f2x-v7q7-m7m5> (modified 2026-10-05T23:15:03.987605025Z)
27. OSV advisory GHSA-7gcf-g7xr-8hxj — OSV.dev. <https://osv.dev/vulnerability/GHSA-7gcf-g7xr-8hxj> (modified 2026-09-10T03:51:10.897685062Z)
28. OSV advisory GHSA-8c75-8mhr-p7r9 — OSV.dev. <https://osv.dev/vulnerability/GHSA-8c75-8mhr-p7r9> (modified 2026-09-10T03:50:43.807790048Z)
29. OSV advisory GHSA-9g45-5xwm-f3wc — OSV.dev. <https://osv.dev/vulnerability/GHSA-9g45-5xwm-f3wc> (modified 2026-09-17T16:45:06.215938994Z)
30. OSV advisory GHSA-9pj6-vhgr-3mwh — OSV.dev. <https://osv.dev/vulnerability/GHSA-9pj6-vhgr-3mwh> (modified 2026-09-16T22:30:08.343637534Z)
31. OSV advisory GHSA-c8m5-c952-6cm4 — OSV.dev. <https://osv.dev/vulnerability/GHSA-c8m5-c952-6cm4> (modified 2026-10-27T16:15:05.354395696Z)
32. OSV advisory GHSA-c9xm-49cp-xcr9 — OSV.dev. <https://osv.dev/vulnerability/GHSA-c9xm-49cp-xcr9> (modified 2026-10-02T16:30:07.619134114Z)
33. OSV advisory GHSA-cq8v-f236-94qc — OSV.dev. <https://osv.dev/vulnerability/GHSA-cq8v-f236-94qc> (modified 2026-09-10T03:50:43.958966498Z)
34. OSV advisory GHSA-ghm9-cr32-g9qj — OSV.dev. <https://osv.dev/vulnerability/GHSA-ghm9-cr32-g9qj> (modified 2026-09-10T03:51:01.732377930Z)
35. OSV advisory GHSA-h2v8-394m-p7vv — OSV.dev. <https://osv.dev/vulnerability/GHSA-h2v8-394m-p7vv> (modified 2026-10-27T16:15:05.337819489Z)
36. OSV advisory GHSA-h395-gr6q-cpjc — OSV.dev. <https://osv.dev/vulnerability/GHSA-h395-gr6q-cpjc> (modified 2026-09-10T03:50:35.169824826Z)
37. OSV advisory GHSA-hppc-g8h3-xhp3 — OSV.dev. <https://osv.dev/vulnerability/GHSA-hppc-g8h3-xhp3> (modified 2026-09-10T03:51:02.103657748Z)
38. OSV advisory GHSA-phqj-4mhp-q6mq — OSV.dev. <https://osv.dev/vulnerability/GHSA-phqj-4mhp-q6mq> (modified 2026-09-10T03:51:06.601254514Z)
39. OSV advisory GHSA-pqf5-4pqq-29f5 — OSV.dev. <https://osv.dev/vulnerability/GHSA-pqf5-4pqq-29f5> (modified 2026-09-10T03:51:02.503624598Z)
40. OSV advisory GHSA-q2qq-hmj6-3wpp — OSV.dev. <https://osv.dev/vulnerability/GHSA-q2qq-hmj6-3wpp> (modified 2026-09-10T03:51:06.690531529Z)
41. OSV advisory GHSA-qwgh-2vcv-g2f7 — OSV.dev. <https://osv.dev/vulnerability/GHSA-qwgh-2vcv-g2f7> (modified 2026-10-30T15:45:11.580215361Z)
42. OSV advisory GHSA-w44r-93j7-qv28 — OSV.dev. <https://osv.dev/vulnerability/GHSA-w44r-93j7-qv28> (modified 2026-10-27T16:15:05.340347056Z)
43. OSV advisory GHSA-w9wp-h8wv-79jx — OSV.dev. <https://osv.dev/vulnerability/GHSA-w9wp-h8wv-79jx> (modified 2026-09-10T03:50:50.807599062Z)
44. OSV advisory GHSA-xmgf-hq76-4vx2 — OSV.dev. <https://osv.dev/vulnerability/GHSA-xmgf-hq76-4vx2> (modified 2026-09-10T03:50:44.840710191Z)
45. OSV advisory GHSA-xp3w-r5p5-63rr — OSV.dev. <https://osv.dev/vulnerability/GHSA-xp3w-r5p5-63rr> (modified 2026-09-10T03:51:07.254489393Z)
46. OSV advisory GHSA-xv59-967r-8726 — OSV.dev. <https://osv.dev/vulnerability/GHSA-xv59-967r-8726> (modified 2026-09-10T03:51:07.319185525Z)
47. OSV advisory RUSTSEC-2024-0388 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2024-0388> (modified 2024-11-10T13:34:40Z)
48. OSV advisory RUSTSEC-2024-0436 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2024-0436> (modified 2026-01-27T22:03:15.694766Z)
49. OSV advisory RUSTSEC-2025-0134 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2025-0134> (modified 2025-12-05T19:07:59.622592Z)
50. OSV advisory RUSTSEC-2025-0141 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2025-0141> (modified 2026-01-16T11:07:28.867553Z)
51. OSV advisory RUSTSEC-2025-0167 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2025-0167> (modified 2026-08-10T19:45:04.530683607Z)
52. OSV advisory RUSTSEC-2026-0105 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0105> (modified 2026-04-25T15:15:06.139681Z)
53. OSV advisory RUSTSEC-2026-0173 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0173> (modified 2026-06-07T21:00:04.318567692Z)
54. OSV advisory RUSTSEC-2026-0183 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0183> (modified 2026-06-17T13:00:04.696626611Z)
55. OSV advisory RUSTSEC-2026-0184 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0184> (modified 2026-06-17T14:00:05.672935662Z)
56. OSV advisory RUSTSEC-2026-0190 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0190> (modified 2026-06-29T14:15:03.650725453Z)
57. OSV advisory RUSTSEC-2026-0221 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0221> (modified 2026-07-31T12:15:04.629484145Z)
58. OSV advisory RUSTSEC-2026-0247 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0247> (modified 2026-08-10T19:45:04.540318330Z)
59. OSV advisory RUSTSEC-2026-0253 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0253> (modified 2026-08-11T11:15:06.101553049Z)
60. OSV advisory RUSTSEC-2026-0292 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0292> (modified 2026-09-21T09:15:02.898993962Z)
61. OSV advisory RUSTSEC-2026-0338 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0338> (modified 2026-10-12T18:15:01.969514645Z)
62. OSV advisory RUSTSEC-2026-0339 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0339> (modified 2026-10-12T18:15:01.956822776Z)
63. OSV advisory RUSTSEC-2026-0340 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0340> (modified 2026-10-12T18:15:01.975478256Z)
64. OSV advisory RUSTSEC-2026-0341 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0341> (modified 2026-10-12T18:15:01.969505433Z)
65. OSV advisory RUSTSEC-2026-0342 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0342> (modified 2026-10-12T18:15:01.956681478Z)
66. OSV advisory RUSTSEC-2026-0382 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0382> (modified 2026-10-29T10:55:54.096394276Z)
67. OSV advisory RUSTSEC-2026-0385 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0385> (modified 2026-10-23T08:30:02.389575143Z)
68. OSV advisory RUSTSEC-2026-0386 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0386> (modified 2026-10-23T14:45:03.847864944Z)
69. OSV advisory RUSTSEC-2026-0387 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0387> (modified 2026-10-24T03:45:02.365137418Z)
70. OSV advisory RUSTSEC-2026-0418 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0418> (modified 2026-10-29T14:15:02.333141406Z)
71. OSV advisory RUSTSEC-2026-0441 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0441> (modified 2026-11-05T09:00:02.627533155Z)
72. OSV.dev — open-source vulnerability database and API — Open Source Security Foundation. <https://osv.dev/> (the database QSI queries for each exactly pinned version; every advisory id in a finding resolves at https://osv.dev/vulnerability/<id>)
73. OWASP Application Security Verification Standard — OWASP. <https://owasp.org/www-project-application-security-verification-standard/> (living standard — check the project page for the current version)
74. P. W. Shor — Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms on a Quantum Computer (SIAM J. Comput., 1997) — SIAM. <https://doi.org/10.1137/S0097539795293172> (peer-reviewed article)
75. R. Babbush et al. — Securing Elliptic Curve Cryptocurrencies against Quantum Vulnerabilities: Resource Estimates and Mitigations (arXiv:2603.28846) — arXiv. <https://arxiv.org/abs/2603.28846> (preprint (2026-03-30, v2 2026-04-15): 256-bit ECDLP with < 1200 logical qubits and < 90 M Toffoli gates (or < 1450 and < 70 M); < 500,000 physical qubits at 10^-3 error, minutes)
76. S. Jaques, M. Naehrig, M. Roetteler, F. Virdia — Implementing Grover oracles for quantum key search on AES and LowMC (EUROCRYPT 2020; arXiv:1910.01700) — Springer / arXiv. <https://arxiv.org/abs/1910.01700> (peer-reviewed article: lower cost estimates for the AES key searches that define the NIST categories)
77. Smart Contract Weakness Classification (SWC) Registry — SWC community (no longer actively maintained). <https://swcregistry.io/> (historic reference; still widely cited)

## Appendices: Cryptographic inventory

By origin: dependency manifests 86 (0 Shor-breakable) · own code 37 (12 Shor-breakable) · third-party code in the tree 71 (2 Shor-breakable).

| Algorithm | Parameter | Library | Quantum status | Classical status | Count | Locations | Examples |
|---|---|---|---|---|---|---|---|
| Keccak-256 | Keccak-256 |  | Grover: acceptable to NIST, below ECCG/ANSSI guidance | acceptable | 90 | 90 | contracts/lib/openzeppelin-contracts-upgradeable/contracts/access/manager/AccessManagerUpgradeable.sol:625; contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/GovernorUpgradeable.sol:35; contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/TimelockControllerUpgradeable.sol:27 |
| Crypto library | 0.10.75 | openssl (OpenSSL) | n/a | acceptable | 1 | 1 | Cargo.lock |
| Crypto library | 0.13.2 | p256 (RustCrypto elliptic curves) | n/a | acceptable | 1 | 1 | Cargo.lock |
| Crypto library | 0.13.4 | k256 (RustCrypto elliptic curves) | n/a | acceptable | 1 | 1 | Cargo.lock |
| Crypto library | 0.16.9 | ecdsa (python-ecdsa) | n/a | acceptable | 1 | 1 | Cargo.lock |
| Crypto library | 0.17.14 | ring (ring (Rust)) | n/a | acceptable | 1 | 1 | Cargo.lock |
| Crypto library | 0.23.36 | rustls (rustls) | n/a | acceptable | 1 | 1 | Cargo.lock |
| Crypto library | 0.27.0 | secp256k1 (secp256k1 bindings) | n/a | acceptable | 1 | 1 | Cargo.lock |
| Crypto library | 0.30.0 | secp256k1 (secp256k1 bindings) | n/a | acceptable | 1 | 1 | Cargo.lock |
| Crypto library | 0.31.1 | secp256k1 (secp256k1 bindings) | n/a | acceptable | 1 | 1 | Cargo.lock |
| Crypto library | 10.4.0 | jsonwebtoken (jsonwebtoken (Node)) | n/a | acceptable | 1 | 1 | Cargo.lock |
| Crypto library | 2.0.1 | x25519-dalek (ed25519-dalek) | n/a | acceptable | 1 | 1 | Cargo.lock |
| Crypto library | 2.2.0 | ed25519-dalek (ed25519-dalek) | n/a | acceptable | 1 | 1 | Cargo.lock |
| Crypto library | 4.1.3 | curve25519-dalek (ed25519-dalek) | n/a | acceptable | 1 | 1 | Cargo.lock |
| Crypto library | 9.3.1 | jsonwebtoken (jsonwebtoken (Node)) | n/a | acceptable | 2 | 2 | Cargo.lock; Cargo.toml |
| Crypto library | 0.13 | k256 (RustCrypto elliptic curves) | n/a | acceptable | 1 | 1 | Cargo.toml |
| Crypto library | 0.30 | secp256k1 (secp256k1 bindings) | n/a | acceptable | 1 | 1 | Cargo.toml |
| Crypto library | 2.0 | ed25519-dalek (ed25519-dalek) | n/a | acceptable | 1 | 1 | Cargo.toml |
| Crypto library | 1.2.0 | @noble/hashes (noble-hashes) | n/a | acceptable | 4 | 4 | contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/package-lock.json; contracts/lib/openzeppelin-contracts-upgradeable/package-lock.json; contracts/lib/openzeppelin-contracts/package-lock.json |
| Crypto library | 1.2.0 | @noble/curves (noble-curves) | n/a | acceptable | 4 | 4 | contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/package-lock.json; contracts/lib/openzeppelin-contracts-upgradeable/package-lock.json; contracts/lib/openzeppelin-contracts/package-lock.json |
| Crypto library | 1.3.2 | @noble/hashes (noble-hashes) | n/a | acceptable | 4 | 4 | contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/package-lock.json; contracts/lib/openzeppelin-contracts-upgradeable/package-lock.json; contracts/lib/openzeppelin-contracts/package-lock.json |
| Crypto library | 1.4.0 | @noble/hashes (noble-hashes) | n/a | acceptable | 4 | 4 | contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/package-lock.json; contracts/lib/openzeppelin-contracts-upgradeable/package-lock.json; contracts/lib/openzeppelin-contracts/package-lock.json |
| Crypto library | 1.4.2 | @noble/curves (noble-curves) | n/a | acceptable | 4 | 4 | contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/package-lock.json; contracts/lib/openzeppelin-contracts-upgradeable/package-lock.json; contracts/lib/openzeppelin-contracts/package-lock.json |
| Crypto library | 1.7.1 | @noble/secp256k1 (noble-curves) | n/a | acceptable | 4 | 4 | contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/package-lock.json; contracts/lib/openzeppelin-contracts-upgradeable/package-lock.json; contracts/lib/openzeppelin-contracts/package-lock.json |
| Crypto library | 1.7.2 | @noble/hashes (noble-hashes) | n/a | acceptable | 4 | 4 | contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/package-lock.json; contracts/lib/openzeppelin-contracts-upgradeable/package-lock.json; contracts/lib/openzeppelin-contracts/package-lock.json |
| Crypto library | 1.8.0 | @noble/hashes (noble-hashes) | n/a | acceptable | 4 | 4 | contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/package-lock.json; contracts/lib/openzeppelin-contracts-upgradeable/package-lock.json; contracts/lib/openzeppelin-contracts/package-lock.json |
| Crypto library | 1.8.2 | @noble/curves (noble-curves) | n/a | acceptable | 4 | 4 | contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/package-lock.json; contracts/lib/openzeppelin-contracts-upgradeable/package-lock.json; contracts/lib/openzeppelin-contracts/package-lock.json |
| Crypto library | 1.9.0 | @noble/curves (noble-curves) | n/a | acceptable | 3 | 3 | contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/package-lock.json; contracts/lib/openzeppelin-contracts-upgradeable/package-lock.json; contracts/lib/openzeppelin-contracts/package-lock.json |
| Crypto library | 4.0.4 | secp256k1 (secp256k1 bindings) | n/a | acceptable | 4 | 4 | contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/package-lock.json; contracts/lib/openzeppelin-contracts-upgradeable/package-lock.json; contracts/lib/openzeppelin-contracts/package-lock.json |
| Crypto library | 6.14.0 | ethers (ethers.js) | n/a | acceptable | 3 | 3 | contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/package-lock.json; contracts/lib/openzeppelin-contracts-upgradeable/package-lock.json; contracts/lib/openzeppelin-contracts/package-lock.json |
| Crypto library | 6.6.1 | elliptic (elliptic (Node)) | n/a | acceptable | 4 | 4 | contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/package-lock.json; contracts/lib/openzeppelin-contracts-upgradeable/package-lock.json; contracts/lib/openzeppelin-contracts/package-lock.json |
| Crypto library | ^6.14.0 | ethers (ethers.js) | n/a | acceptable | 3 | 3 | contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/package.json; contracts/lib/openzeppelin-contracts-upgradeable/package.json; contracts/lib/openzeppelin-contracts/package.json |
| Crypto library | workspace | jsonwebtoken (jsonwebtoken (Node)) | n/a | acceptable | 1 | 1 | crates/eth-engine/Cargo.toml |
| Crypto library | workspace | k256 (RustCrypto elliptic curves) | n/a | acceptable | 3 | 3 | crates/execution-txpool/Cargo.toml; crates/quake/Cargo.toml; crates/spammer/Cargo.toml |
| Crypto library | workspace | secp256k1 (secp256k1 bindings) | n/a | acceptable | 1 | 1 | crates/quake/Cargo.toml |
| Crypto library | 1.9.2 | @noble/curves (noble-curves) | n/a | acceptable | 1 | 1 | package-lock.json |
| Crypto library | 1.9.4 | @noble/curves (noble-curves) | n/a | acceptable | 1 | 1 | package-lock.json |
| Crypto library | 2.3.0 | @noble/ed25519 (noble-curves) | n/a | acceptable | 1 | 1 | package-lock.json |
| Crypto library | 6.14.4 | ethers (ethers.js) | n/a | acceptable | 1 | 1 | package-lock.json |
| Crypto library | ^1.8.0 | @noble/hashes (noble-hashes) | n/a | acceptable | 1 | 1 | package.json |
| Crypto library | ^2.3.0 | @noble/ed25519 (noble-curves) | n/a | acceptable | 1 | 1 | package.json |
| PQC library | 0.2.0-rc.5 | slh-dsa (RustCrypto post-quantum crates) | post-quantum | acceptable | 2 | 2 | Cargo.lock; Cargo.toml |
| PQC library | workspace | slh-dsa (RustCrypto post-quantum crates) | post-quantum | acceptable | 2 | 2 | crates/pq-precompile/Cargo.toml; crates/precompiles/Cargo.toml |
| SLH-DSA |  |  | post-quantum | acceptable | 3 | 3 | crates/pq-precompile/src/lib.rs:22; crates/precompiles/src/bin/generate_pq_test_vectors.rs:11; crates/precompiles/src/pq_test_vectors.rs:26 |
| SLH-DSA | SLH-DSA-SHA2-128s |  | post-quantum | acceptable | 1 | 1 | crates/precompiles/src/bin/generate_pq_test_vectors.rs:56 |
| ECDSA | secp256k1 (ecrecover) |  | vulnerable (Shor) | acceptable | 2 | 2 | contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/cryptography/ECDSA.sol:148; contracts/lib/openzeppelin-contracts/contracts/utils/cryptography/ECDSA.sol:148 |
| ECDSA | secp256k1 |  | vulnerable (Shor) | acceptable | 4 | 4 | crates/quake/src/nodekey.rs:23; crates/quake/src/rpc/valset_manager.rs:25; crates/spammer/src/accounts.rs:20 |
| ECDSA |  |  | vulnerable (Shor) | acceptable | 3 | 3 | crates/quake/src/rpc/valset_manager.rs:25; crates/spammer/src/accounts.rs:20; crates/spammer/src/generator.rs:23 |
| Ed25519 | Ed25519 |  | vulnerable (Shor) | acceptable | 5 | 5 | crates/signer/src/local.rs:26; crates/types/src/codec/proto.rs:28; crates/types/src/proposal_part.rs:26 |

_Long lists are grouped here; the full per-file list is in the JSON report, signed with the same key._

## Appendices: Input files

| File | Size | SHA-256 | Redactions |
|---|---|---|---|
| .cargo/config.toml | 88 | `4869cd5432bb99dc9355fcef9097cafa8cc4801a1bb2476fc4522a5f6700eedd` | 0 |
| Cargo.lock | 383735 | `856e1f4149051554ac6ca8a41f9a85ac23398dfccdc428430879f27f75c3c73b` | 0 |
| Cargo.toml | 16100 | `48f968bca9c09b55e223ecff5a5fc0ead011a9cb8df170151fd2627086e736d2` | 0 |
| assets/devnet/genesis.config.ts | 5963 | `ffaa618e0729c2441e8af86f86affeca4f1759575aa436f287dca4ec1b12d7b9` | 0 |
| assets/localdev/genesis.config.ts | 6060 | `89c9971d57512d25e12cf947ac6b7a7359964de0878cfdf024e59a3b805fbb6f` | 0 |
| assets/mainnet/genesis.config.ts | 6297 | `df635ca0b44d667f3446abf6eed99ba30066fcee981ed4ac3b881b9e96c688d6` | 11 |
| assets/testnet/genesis.config.ts | 5687 | `274222211ae09b7088381d17c8f5672684b90b736e34c1aa325365f741390389` | 0 |
| contracts/scripts/Addresses.sol | 2466 | `66a5c565bd6f5d8c923e3c0055452abc6affb593d8851342fb5bc8c83475e8ad` | 0 |
| contracts/scripts/ArtifactHelper.s.sol | 12903 | `401ddc8f6d3fa2b1deadc7f37d3618a718432ef47562da9f818f68604045de6b` | 0 |
| contracts/scripts/DenylistManagement.s.sol | 8615 | `a65548e15480cd037a174ec7c23ce68533cc6ee2e141877a154ebc505f691899` | 0 |
| contracts/scripts/DeployGasGuzzler.s.sol | 1121 | `196141a931b87876a33814bb33d657c01161c86696fe182ca9542b744adc1211` | 0 |
| contracts/scripts/DeployMemo.s.sol | 1725 | `75cc596a34c87f5c67f3a06251e05cd04d095420da24d01560ad5dca33dcb600` | 0 |
| contracts/scripts/DeployMulticall3From.s.sol | 1176 | `4b90e646f1d7c04d608a8bdf09406e6b8c1defd24c4ad4ccd97142adde5eb654` | 0 |
| contracts/scripts/DeployPermissionedValidatorManager.s.sol | 4448 | `7d6ab17aac36e0d27584197e9591d6a892142ac03395c80d9625f27203b3dc58` | 0 |
| contracts/scripts/DeployProtocolConfig.s.sol | 1932 | `a23ed2a04f7ea0819b77a3b270bef7b6ffdf6b0c84e43bd0cf7e50769fbccfb1` | 0 |
| contracts/scripts/ProtocolConfigManagement.s.sol | 18919 | `6618428965b7dabeba4f2d7fc11424d368114441003bf3c89c3f67ff9f79b177` | 0 |
| contracts/scripts/ProxyManagement.s.sol | 2234 | `f4ba6d45bdd0785ec5a2dd71b5066176ff5e5c33f8607745028c9fbb6ad18545` | 0 |
| contracts/src/Denylist.sol | 6283 | `c149e7649461e6cf813f4da9b52eb1c503588ac93f7676a8776acb3047cc733c` | 0 |
| contracts/src/Precompiles.sol | 1251 | `4f3451b4d727b329cb79e558fcc13ac132c8f34aef5785abe47817a1e26c5589` | 0 |
| contracts/src/batch/IMulticall3From.sol | 4954 | `35a1770db908bd891b89a861fd30b0a83b2e149bd3e1470df8a54e50593fe00c` | 0 |
| contracts/src/batch/Multicall3From.sol | 7389 | `11728b7d21c8ea63bbafdc920b3832f721e883306f2a0b7b4a30ce9eb2bda77d` | 0 |
| contracts/src/call-from/ICallFrom.sol | 1443 | `76c879f70368d1b62b3c55146d11be9bb29bd9b5c6a5b922366c29a8e9ba1387` | 0 |
| contracts/src/common/roles/Pausable.sol | 5642 | `dfd50cdfab955f02501b55b90e2b48a78dfcdde42866ca83743b92f513de2e5c` | 0 |
| contracts/src/memo/IMemo.sol | 2342 | `c7c5ab6645867c7db15fe931d8320cc1a95bc03db21514ace9c2cdc92afd6fb7` | 0 |
| contracts/src/memo/Memo.sol | 2088 | `347349ba5428da3cc1f50bf6d739c11ba8a71138b256456627d7a0e2ec333a74` | 0 |
| contracts/src/pq/IPQ.sol | 1572 | `c21bab2326e33beb2fa0294ebd7d9bb2a64457c95d2bbd308c95c1d38ad74eb0` | 0 |
| contracts/src/protocol-config/ProtocolConfig.sol | 7639 | `8785eb70aec4e2b2b378d6ab0488e880ba00b29e5c9fb796744df4dac6d7bd6f` | 0 |
| contracts/src/protocol-config/interfaces/IProtocolConfig.sol | 3418 | `ef22eb02b705414f8ee5f728b3519de4b3f4cc6d4fa6bf7b69f3c54f04546371` | 0 |
| contracts/src/protocol-config/roles/Controller.sol | 4007 | `5cb3acbd81e41b845da0059357c93d526d77ce395ef1fa314ff1647ba8e2946a` | 0 |
| contracts/src/proxy/AdminUpgradeableProxy.sol | 4055 | `ad0ea3e7dac75d32c6064fcebb6789be2a834af68d46f7c3fe01bf399e9c0a3d` | 0 |
| contracts/src/validator-manager/PermissionedValidatorManager.sol | 7059 | `c5ed1f71c18d3021e12f06f3f9849cde89205d8af6ff599f3b3ad485ab9b6f31` | 0 |
| contracts/src/validator-manager/ValidatorRegistry.sol | 11396 | `7e3d7818a881f3ae77dc2b619a453f87bacabda16d1a2469ca2447551d310dab` | 0 |
| contracts/src/validator-manager/interfaces/IPermissionedValidatorManager.sol | 2169 | `67dc362f361e57221065b981cdd352353c951163338d4f4c3a828f15ce7c89a1` | 0 |
| contracts/src/validator-manager/interfaces/IValidatorRegistry.sol | 3273 | `c1054bce8bec98dcb90d3ce52d474cb6f928b8f160b9e5f78425ba9ae7520d94` | 0 |
| contracts/src/validator-manager/roles/Controller.sol | 8575 | `184585e0242064274a8a5381e6c50db428fa8a5f4707d51ade280dfdf173a5be` | 0 |
| contracts/src/validator-manager/roles/ValidatorRegisterer.sol | 5833 | `6127ac456a7e51fa35a4c951c536e097a1cffebbcec2883ab87e010c40246b30` | 0 |
| crates/consensus-db/Cargo.toml | 1069 | `e55b9483ea31cba36cc99c47a4626491d9b5f4d6a235b2c2fddb8a378de24561` | 0 |
| crates/consensus-db/src/decoder.rs | 23879 | `afd7327e1c697aedd1f9da6aebafbfe65bf89f7a001ca38565950433ed7eeda4` | 0 |
| crates/consensus-db/src/encoder.rs | 14875 | `9fc5300e25705495dd4589543ffec408614754479b425ed802b3a397502091df` | 0 |
| crates/consensus-db/src/invalid_payloads.rs | 4193 | `2d9c887819e7272078330f4d40dba6cd9e37496f259fa0636730ec5de16aa249` | 0 |
| crates/consensus-db/src/keys.rs | 3688 | `73e5388c7dc9888d10b385f2092de5c51824d2b92f07c4ef071e3b5d7ae37664` | 0 |
| crates/consensus-db/src/lib.rs | 1243 | `c46b3bb49f8a1f3cff6cf5d098e32e6755b4f425cc0cda3ecd7d83894810ca31` | 0 |
| crates/consensus-db/src/metrics.rs | 6279 | `7c20b5846eae31e99389e9b94835cccb3da295495d099b5f99575ed8df1e9839` | 0 |
| crates/consensus-db/src/migrations.rs | 52653 | `bdb6e03ed689562d14e6cb94cdd3146492b42ea0da5f7897a3247ad94cc5ff40` | 0 |
| crates/consensus-db/src/migrations/migrators.rs | 12910 | `f7bb9325ec504a13fab28693eddf2602c64b7320380459186e4faaf45f0e2d10` | 0 |
| crates/consensus-db/src/repositories/certificates.rs | 1946 | `abca9edd49e30af252e07dacc3adf9a06955b09ebaa13703ae51d4b45df91ad3` | 0 |
| crates/consensus-db/src/repositories/decided_blocks.rs | 2426 | `9cf2bd094df43af98be4211c61b93d648bf292be92bba90dafadc87d0a1d7a0d` | 0 |
| crates/consensus-db/src/repositories/invalid_payloads.rs | 2167 | `e5d3254529c1eee5d512402f6a5d39ab306303b6ab4fcae2ee543097e353d577` | 0 |
| crates/consensus-db/src/repositories/mod.rs | 1581 | `b597e3a548be36a2397aea8c60a139a51c79e9ab4b8eaa7bdd7962fc7487287d` | 0 |
| crates/consensus-db/src/repositories/payloads.rs | 1509 | `7095f1c170956ee5545ceda4367ff0bef5094f5740bc687a21887cd5c66b39cf` | 0 |
| crates/consensus-db/src/repositories/pending_proposals.rs | 2438 | `509b1eab77c6039d3e8c795dc9bf6585ca3fc9f3ec60c4409c2a99362ac21745` | 0 |
| crates/consensus-db/src/repositories/undecided_blocks.rs | 3883 | `ffe41d0a389ac508d32295b57f3f6f9a4f491dd0d3da9daeba9ed8feb43fe0a4` | 0 |
| crates/consensus-db/src/services/mod.rs | 870 | `dd947a9ef1d5cef6638b41cb8a7e489ba08c731808f1297446ebb79c688d40be` | 0 |
| crates/consensus-db/src/services/pruning.rs | 9519 | `0c40ce8fea186d1555b149897bd2579c58b8520ffbe3c7e9851eb04d0048032a` | 0 |
| crates/consensus-db/src/store.rs | 133040 | `f825d41a65195065d856ba1e1bbd8a73165b6f01fff1e59ea4a322dc534c9ead` | 0 |
| crates/consensus-db/src/versions.rs | 5647 | `be9c7dbc710a88d368b79363cf78f46a46af74a16692f9fe588bebab29482649` | 0 |
| crates/eth-engine/Cargo.toml | 2095 | `1b38647384de540273b6db2d5dd1a20255eff392c9c5177c46f121ef956f6f71` | 0 |
| crates/eth-engine/src/abi_utils.rs | 23225 | `697cb615b4649a13797f90edb6cfd098a55e6914c5d54ef243de2cb020486a8a` | 1 |
| crates/eth-engine/src/capabilities.rs | 4517 | `6b80e07915224f00de993ed791240c1cea967b37091a3df7f5098294421c9cb8` | 0 |
| crates/eth-engine/src/constants.rs | 6147 | `5418f89a0b5657994e80e16e60cc732d8bccfc438d0311cc625d6e6aeefe7812` | 0 |
| crates/eth-engine/src/deadline.rs | 5309 | `d8a6ad6ca1a243786e8120947ffc37c754d6fd96a387a7c865c860b36c0f8f74` | 0 |
| crates/eth-engine/src/engine.rs | 38373 | `c0cba73a6ac1d86aeccb44bc3dd68b41a85adc5dddfd17774373dd0a3aa71f1c` | 0 |
| crates/eth-engine/src/ipc/engine_ipc.rs | 6604 | `ae2c7cd50b59b5ff1f0f1c9d8d1c62745accfef049db00e5e811b261b0792c6f` | 0 |
| crates/eth-engine/src/ipc/ethereum_ipc.rs | 30189 | `5dc4c68f1ed9c79ca952dd3f79ff781b8b6056312c958c6b4a7d12951235fa18` | 0 |
| crates/eth-engine/src/ipc/ipc_builder.rs | 7875 | `69044aa92fbd6ec78a7c2c45bab897341c89d442f60d58e9a4e801e31ca18e53` | 0 |
| crates/eth-engine/src/ipc/mod.rs | 729 | `a7f6d4e6ad68c6bfe2ec8098133412ccf35d1559375b3ffa21bf22e093665642` | 0 |
| crates/eth-engine/src/json_structures.rs | 1228 | `38127184f86fee91464721bcfd3444420fc3de7917b82652b65eb92d8c523f39` | 0 |
| crates/eth-engine/src/lib.rs | 1171 | `c0c5f2cc4ab00c27f01d03bd86bc70fc4efa02f1db26e95470ba856b4b518b38` | 0 |
| crates/eth-engine/src/persistence_meter.rs | 28465 | `7288548c00eba8dacc8321dacd27e0916c57326364949df0c41056ae7674563f` | 0 |
| crates/eth-engine/src/retry.rs | 1799 | `287739978bf4da7dd257f4aff34e1cb7c44cbde4b21932d9d49504709c9f8033` | 0 |
| crates/eth-engine/src/rpc/auth.rs | 2567 | `c41be51c0fb99ace516c93f3841d4725376f70552bc7b66409206a66b931e632` | 0 |
| crates/eth-engine/src/rpc/engine_rpc.rs | 9007 | `2283b60e5db161c0407921a3f2c0dfa23dad603674ba58a3abfcab88556ede39` | 0 |
| crates/eth-engine/src/rpc/errors.rs | 8218 | `7c43a59967c06d12e4b4b4476b04663147caf9030d15ce971578498a2e2dbcf8` | 0 |
| crates/eth-engine/src/rpc/ethereum_rpc.rs | 26825 | `0a7ec9f5eca9d8d835537d52f2b695ebc7232989d9def96a2431e42f05d4275e` | 0 |
| crates/eth-engine/src/rpc/json_structs.rs | 1479 | `d514396ca1512cd6c3cb855c69e44ff47105a79f00e2a8612d5aa698e9afd478` | 0 |
| crates/eth-engine/src/rpc/mod.rs | 809 | `d5f455b1095aa0c5ef1876c7ff56e631fff7753980a0796ebf559960704a62d3` | 0 |
| crates/eth-engine/src/rpc/request_builder.rs | 4878 | `a907ed01136495c3f9d75bbaf299d868bc7145a291e5b5e8121fc82f7950a68f` | 0 |
| crates/evm-node/Cargo.toml | 2470 | `9c2e22bc63e0b7817544f13dc06c222ba5fd03b5992d0862b34e20ec8623e4e9` | 0 |
| crates/evm-node/src/engine.rs | 15511 | `9934090f8ee248cbbebb4acc818f18ce2b190509c7d12ec3aec5aa5fb07b4950` | 0 |
| crates/evm-node/src/lib.rs | 1073 | `960cc834dd39a4fa405716197f592acfceda72637dd89d7579bda62eefc96366` | 0 |
| crates/evm-node/src/node.rs | 33791 | `d930d6c5c7c7e1848071fac64046d1e3390dd7a76d63b6371543cb9d96162def` | 0 |
| crates/evm-node/src/payload.rs | 4975 | `d538057bb3b34ca0fa70498831fd7ed05a2e9f962dcc10211537da2772e0a00d` | 0 |
| crates/evm-node/src/rebroadcast.rs | 7335 | `ce89988d899278a1d54c793d6d1d80a2b7e292f1a3d06174d8d73c7199d7e906` | 0 |
| crates/evm-node/src/rpc/arc.rs | 2492 | `8394c74bae369bca8fc26a590ee6c423e7d44b094b213b14d4251d94bed9bb33` | 0 |
| crates/evm-node/src/rpc/common.rs | 3429 | `a95ba9e21aaa77641854021e221d44f5e540442e83e86f649f1586b0c26f539a` | 0 |
| crates/evm-node/src/rpc/get_certificate.rs | 10268 | `0cbefbf1f90608e40db93b13d4c4b8750a81a857eb3eaebe80053c827185dda4` | 0 |
| crates/evm-node/src/rpc/get_version.rs | 1511 | `6efc4cb5ee03c3efafbc5efdbfe8459d3c1fdc53797e96cc4da2be26219e4b03` | 0 |
| crates/evm-node/src/rpc/mod.rs | 776 | `9d075af585493a440ee9faeaf578ed1bc10ca56f671544c9f63bbc3840fd1330` | 0 |
| crates/evm-node/src/rpc_middleware.rs | 101581 | `02e9a4a6f9dd6a3e5fa6d9b1edef1ec312f02f9679ed3d5f7de4ca850c6637e9` | 0 |
| crates/evm/Cargo.toml | 1578 | `44cc1ae2197b436b7b7ee5eccf8f2f81ad733b1871ba3e1d21b27bdc6c0f8cc5` | 0 |
| crates/evm/src/assembler.rs | 4276 | `be122b73120ea49aa607a9a698694385c4f4fa779684a78eabc45849cc56e5db` | 0 |
| crates/evm/src/evm.rs | 347331 | `e7e6d819af5ac57529adaec76e719aa2d1c25f8a9a5cb0cc67896f2e6f9a704e` | 0 |
| crates/evm/src/executor.rs | 54917 | `36204a2532f30f451869c8703f2ba0b9a86fe09a119b3b3128d3298a8d84a4d2` | 0 |
| crates/evm/src/frame_result.rs | 5920 | `3e726b5e8b408466659c2e2b895325c5c26e65825ed8cef077419f7c9f4f02d7` | 0 |
| crates/evm/src/handler.rs | 32410 | `b0bf0d16c0d4aaa488870003a1b25bdaa84e556aad8f168decbce3a928b67187` | 0 |
| crates/evm/src/lib.rs | 1231 | `2dd4ca8eaff230041256afc4b1a8ce6cf6dda096aa21f8faab2862ed9f92dd87` | 0 |
| crates/evm/src/log.rs | 2964 | `3f1db926e8c54e471ac803311df4b1556212b0f9bbd887458c4fbadcae7a4b25` | 0 |
| crates/evm/src/opcode.rs | 60636 | `aef04b21c03418812a09d5ea53cd7fd44771f4be4047e3d03b4dfbfa81704d79` | 0 |
| crates/evm/src/subcall.rs | 5914 | `87a2964d94cdf06993597638dc8400484c2ad6d9dd01cb8ee8f7c63b0d5af947` | 0 |
| crates/execution-config/Cargo.toml | 1330 | `7f427db32d264a773e99d75a582b6f8ff15fb5e78e5ec8187c0f0d0aa4248825` | 0 |
| crates/execution-config/src/addresses_denylist.rs | 6023 | `dc4d077cbfe711e18162769e287dac62345c49b8acda58b3888d36facb0fed00` | 0 |
| crates/execution-config/src/call_from.rs | 1189 | `289602256d435e2d82b70a0ddf1a24077624e715638cfd4d2e4324bcd5f072f9` | 0 |
| crates/execution-config/src/chainspec.rs | 84748 | `af8fd10f217ed78c722f4f18ce738c31d7204ba00b94fb552b64980eeb57bbd7` | 0 |
| crates/execution-config/src/defaults.rs | 5279 | `3f0f463bf94b96f0e94f279ece2f02af736cc5bc149179d0fe560206b1fcba7d` | 0 |
| crates/execution-config/src/follow.rs | 3482 | `d02ce18930cbeaef8b6b69aec03f044a5fd70e4eee32e99cf025b21ef1891b3c` | 0 |
| crates/execution-config/src/gas_fee.rs | 15392 | `0344a2f7708e8ed3f8d533cdfc5c68e6bb0d20a6e18d73b8107903fcd345889c` | 0 |
| crates/execution-config/src/hardforks.rs | 37762 | `c41e9cf23920d3017e9fe01930801b71f1f810c67c825ece69b620a6cb0107ef` | 0 |
| crates/execution-config/src/lib.rs | 1005 | `718de89c46353dfd5a1990db42c84b8ea11746946846a5285759251f29da6fa6` | 0 |
| crates/execution-config/src/native_coin_control.rs | 3006 | `e04f3ba66a337fa8e695bde6eb24c32e2365ff33715c3db5613da4c0a160c0f8` | 0 |
| crates/execution-config/src/protocol_config.rs | 9732 | `79da91003807f4eaca85020e58fac086a2be65e66c4fe3548624ae6a022b0e9e` | 0 |
| crates/execution-e2e/Cargo.toml | 1840 | `3da97e51f53a60c4bee4906811febe970d8f504054d6fb1b354b29f1605d7dfe` | 0 |
| crates/execution-e2e/src/chainspec.rs | 3689 | `275a13a5a79728fc07b6aa5906d7c1b94f777352b9517f733de5b5d0a080faf8` | 0 |
| crates/execution-e2e/src/lib.rs | 1071 | `b33def44871c8a26a184bc028781cf7fcae68588352b19603a8ecfb6451bd8ea` | 0 |
| crates/execution-e2e/src/node.rs | 13822 | `ae38d5262f8865a2e0079b0dce73ce1f2b62541f846514d9549c99a3d9b531b3` | 0 |
| crates/execution-e2e/src/setup.rs | 9034 | `bf123b626d6487cef23390d1fa8747f1e92dec4080833c017ed1fb6ca7a7d470` | 0 |
| crates/execution-payload/Cargo.toml | 1588 | `161c3ecd426b0c5fd8721349e9c30b66663ef3c76433ce4bdd2b65783c089817` | 0 |
| crates/execution-payload/src/builder.rs | 1190 | `69ea2edfe1337c7ae96f217767d1de4d98ca35a23053b36bf19be0dec17dd261` | 0 |
| crates/execution-payload/src/lib.rs | 855 | `2610eb9ca6086e786ad975cd4aa5ad405bf66b80971b0958b033e048d14d675c` | 0 |
| crates/execution-payload/src/metrics.rs | 4531 | `cfcc8ef77495f6ab67f2cff917f977403c5778f1ef3beba1509865d3085f2df0` | 0 |
| crates/execution-payload/src/payload.rs | 73249 | `795461d1477c5ca6347ff77c4b2d8c9e4429c709da200ed0005dee2472552ea2` | 0 |
| crates/execution-txpool/Cargo.toml | 1501 | `82a10c92eaad4d3113e9fe5ac6be0b734b73a826e20dd3aed076514148452163` | 0 |
| crates/execution-txpool/src/error.rs | 3079 | `d72fae8f6b2c90e2f1b95a869e558b1600201bab600558021039143b3103de3e` | 0 |
| crates/execution-txpool/src/lib.rs | 1579 | `81f21c6b2df073b3f07fc386d739efebc8c8dce00c6829f3b1bf546f11953eda` | 0 |
| crates/execution-txpool/src/pool.rs | 9415 | `ba39ee2c013e3725515e8181e413c7afcd808a1cd36b02b6d6f5ed83e0e0a9bc` | 0 |
| crates/execution-txpool/src/validator.rs | 57425 | `43345385f0f8cd8dbbb4a924e0b040dc71997fe434d184fb5698011386bd47f9` | 0 |
| crates/execution-validation/Cargo.toml | 954 | `c1416254a72b0930306959f3c5e940ead253436f8b096a4f301871f8bbab0cef` | 0 |
| crates/execution-validation/src/consensus.rs | 34253 | `7424ad2807626911871010c7c7a98c283a4f1f3d9c6f0e2ec0276b30df5a07db` | 0 |
| crates/execution-validation/src/denylist.rs | 6094 | `7a35a811c731de9a16143f3ff522a5e78c0b8f28ac344014380d3995e2e846b5` | 0 |
| crates/execution-validation/src/lib.rs | 809 | `613c0606080a397f0412c643fdd0f4e332c9b4be1463ed6e113287649aee32f0` | 0 |
| crates/malachite-app/Cargo.toml | 3501 | `fd4b85f751c066f0bfce9f85cc7c4b24f5c9c3b5f3914552c31c063a955bf177` | 0 |
| crates/malachite-app/src/app.rs | 29116 | `7e23edfb8ec48d68415636982a484df3ff35194aea1e8437739cfd8cbe1115e7` | 0 |
| crates/malachite-app/src/block.rs | 708 | `b60818ff7dbec4a097bc5f55892be4edeafc551a78b3315fd211965e9be8fed4` | 0 |
| crates/malachite-app/src/config.rs | 13619 | `239b1f42604b3f9ecf5e638cb8d8107528a8909a0d9e0a07faa9f1a8d4549baf` | 0 |
| crates/malachite-app/src/env_config.rs | 24307 | `9e183b66c96b3844f63c6aec6e6191096636a164886999d8d0aab139358471af` | 0 |
| crates/malachite-app/src/finalize.rs | 7698 | `ea38984cba9808540d97cedc911f3ec7c9c42b2ceba802d6cdad2be2b15cf592` | 0 |
| crates/malachite-app/src/handlers/consensus_ready.rs | 71402 | `06610ad8e460beb6b506d47f015321d6bc8bda696fcfed4031ce83bc7dc69a57` | 0 |
| crates/malachite-app/src/handlers/decided.rs | 44604 | `5bd3bc367ca9d069336559735b351edde44fe3e8fc04d5eeca98752f64e6d58c` | 0 |
| crates/malachite-app/src/handlers/finalized.rs | 5204 | `9e44ef2cfeb6b8a6478ddcb98d0ac3641ad5b855abc97f67e316efd5b9f64a95` | 0 |
| crates/malachite-app/src/handlers/get_decided_values.rs | 18185 | `c79857206a5b69d9ab086c812643ea5bad7f64889efde561dd82ce4639d0b1cd` | 0 |
| crates/malachite-app/src/handlers/get_history_min_height.rs | 5736 | `5cdf0bfc0df23522454f11a439c1c10d94acad37293b0ca7ef82feb7e5fe5de4` | 0 |
| crates/malachite-app/src/handlers/get_value.rs | 26375 | `7b8ceccdfb187ea6848ad2fe262834700a1825d193ba21645ab4f514e46e4e5e` | 0 |
| crates/malachite-app/src/handlers/mod.rs | 1183 | `6021d9e0400e0d9acde1dd3877b8fe63fb05fc292449405394de705ced2f1fe9` | 0 |
| crates/malachite-app/src/handlers/process_synced_value.rs | 40506 | `5a9784910cd8a31b53fe621cdfb141b3292ec11fd146df8599a5b6e6de9ab0da` | 0 |
| crates/malachite-app/src/handlers/received_proposal_part.rs | 57261 | `3071bcc14ed42ca727dd364930ef2823424b0246f64de88ebdf62ecbbe4addd9` | 0 |
| crates/malachite-app/src/handlers/restream_proposal.rs | 12173 | `3b73452678d5bfed2ce9db3d17e2e33f00525bce5258d2fa193d295a531860ca` | 0 |
| crates/malachite-app/src/handlers/skew_gate.rs | 11016 | `ca6ac6df8c9fe58dc491018381c3e9f6844e989061ed897097358cb91c36c770` | 0 |
| crates/malachite-app/src/handlers/started_round.rs | 55764 | `67ccd8353e705b7892c4600b532ca483b075a7c94c390aeaaf0e93adbb697ec2` | 0 |
| crates/malachite-app/src/hardcoded_config.rs | 20007 | `8ea381235598364a9395ec6c02de9b3fb8be7da61e35975c9ac153d1f374dfed` | 0 |
| crates/malachite-app/src/lib.rs | 1092 | `578489ada036dc5ddca0b68de244ea2a9b9f0af727fd44cbbba09b362a34d5ae` | 0 |
| crates/malachite-app/src/main.rs | 29421 | `199c04a81ae85e70fca256a0fba9664343847e1aa4302e713bc0333975997707` | 0 |
| crates/malachite-app/src/metrics/app.rs | 36250 | `2824c4aadb2e3e6623b81fd2f24f2e14f775dba7fcf83bd2827f54ee400ad09a` | 0 |
| crates/malachite-app/src/metrics/db.rs | 706 | `90a1a97d5e730c0478601ad535bf1ed3a0d9726246b40ac05bd2210f540b7d53` | 0 |
| crates/malachite-app/src/metrics/mod.rs | 954 | `2d57ec59c06159a30e279bdd6a4e9272962ad18c0682ab4b365f6350640dede2` | 0 |
| crates/malachite-app/src/metrics/process.rs | 12281 | `c2bf0edaeb00da5f7aa7c4d45c2f9f197cf0a3bf7d335b7872af62097bfb0189` | 0 |
| crates/malachite-app/src/metrics/validator_set.rs | 2741 | `ca76bb7b3b6d52824c149dbe3f65c6c75629586548588ce0fd3d3d631c033f61` | 0 |
| crates/malachite-app/src/node.rs | 56902 | `8d415e08d4b13d3235eff785b1583c773d37d6bc4f3372e34fab9e5d35bb8e25` | 0 |
| crates/malachite-app/src/payload.rs | 44245 | `081291b1c393e13e05eaf1aeca7b6fd274b62e75460d34a61bd77599a918c903` | 0 |
| crates/malachite-app/src/proposal_parts.rs | 20783 | `46946af6d96e3e9993bf73832c010c5bdedc6b5934ad332c9c7b0e0ef3d8bbd8` | 0 |
| crates/malachite-app/src/request.rs | 14312 | `d49a485ea348ab41dca87c9bff148caaebb34303508645f79da2036ff2395529` | 0 |
| crates/malachite-app/src/rpc/handlers.rs | 19576 | `56986208065c711694c4d6997e7ba9d5757487390088a848695db7085d2f3c86` | 0 |
| crates/malachite-app/src/rpc/middleware.rs | 3883 | `b44ccee8ecd54cbafc84ea0ab785b7ddd46e3ae8ad606fefd5a040719dee61e4` | 0 |
| crates/malachite-app/src/rpc/mod.rs | 971 | `27da7c4f44ce611e3521b89344c7955920269b7a119976487369096f60f7cd7f` | 0 |
| crates/malachite-app/src/rpc/routes.rs | 60005 | `8a58dda9ed2c278cb30f42fea76ad7063c5055c93a1e6ee824764599b35cfc24` | 0 |
| crates/malachite-app/src/rpc/types.rs | 40906 | `327fa3eedd4554d37b625ab4314521fe17d2c4b78d1366517b567445bdb68ff2` | 0 |
| crates/malachite-app/src/rpc/version.rs | 5485 | `cae40866ffdb196fd3069dc868718a3bd5a02d4b361b5dcd6c409b1c566f95df` | 0 |
| crates/malachite-app/src/rpc_sync/client.rs | 10393 | `ee035702a2df37a795f72bba594e73318adada814aa9b145baec8017e8919af7` | 0 |
| crates/malachite-app/src/rpc_sync/mod.rs | 2186 | `9380ffc361600de1ca6faf792ff678ac8d7893ffc11f2846554fe974b4048deb` | 0 |
| crates/malachite-app/src/rpc_sync/network.rs | 15244 | `f65e0d1465bf50e354da69e4b091aec72ce46f3c6b3c7f1bfacc145219ed4d27` | 0 |
| crates/malachite-app/src/rpc_sync/peers.rs | 7989 | `a9b83e06cd4ef3e77507c7e14c6d9fad1f59d5ab376b8d99efdcac72882a2136` | 0 |
| crates/malachite-app/src/rpc_sync/ws_subscription.rs | 7894 | `067102ab3033805df88378c689ff614e89ab338c5b6079d912883e5fe5396d36` | 0 |
| crates/malachite-app/src/state.rs | 34813 | `042500f17fbb8f52edb8611d544941c979c3c26c95cad01b4f692b0c900212d7` | 0 |
| crates/malachite-app/src/stats.rs | 3081 | `a180c5f53dc9e3e072d6e89ed39d7ae53e5538662593048bd62fd0539ce0b223` | 0 |
| crates/malachite-app/src/streaming.rs | 103895 | `9dd2ee152680ee61b1166bb3b94677fb3c312c0a41906398dcdb77e326c6bacd` | 0 |
| crates/malachite-app/src/utils/coord_upgrade.rs | 1959 | `982b37264ef3bbd558f506ef49dd666f37f3336c3b1726a2058dbd297b53acc4` | 0 |
| crates/malachite-app/src/utils/mod.rs | 783 | `c610255f6156e584a48db97633b34190272554e18ed451571e1b8ae905ab1ba9` | 0 |
| crates/malachite-app/src/utils/pretty.rs | 2746 | `c9e6d1d7f5b32a86abe2b70c3ab0d8a733935009fd5d7afaeec693b2804f7e2b` | 0 |
| crates/malachite-app/src/utils/sync_state.rs | 3064 | `f2abfc6ee7657ecc2e99db3cecaa05e5115880b966f95a919c3ad80887ff2893` | 0 |
| crates/malachite-app/src/validator_proof.rs | 7458 | `572fb4d94cb4c8ff394585413959fc4ba7b8913f759f6e3ff9ad7254d3af5523` | 0 |
| crates/malachite-cli/Cargo.toml | 1372 | `d55990732c8817b309284c36f63efad240ca9b4e6716996a7c486827f5daf2aa` | 0 |
| crates/malachite-cli/src/args.rs | 4111 | `f510d773c5abb11d94783ea03746001b480ae7fbca54e47947cfe3aab40bf811` | 0 |
| crates/malachite-cli/src/cmd/db.rs | 1975 | `0daa8ed6fa160985c1a0678704ff89726ebdf6160f26a0c39769907b550e1227` | 0 |
| crates/malachite-cli/src/cmd/download.rs | 7956 | `45092418429ab253f17b5325c43ddd5bf6590daeb0d79f9993f2b02367a63495` | 0 |
| crates/malachite-cli/src/cmd/init.rs | 6873 | `3b5fb80b143154d1260bca40bce2503ab25805f11530f72e22ab6c6a07023de5` | 0 |
| crates/malachite-cli/src/cmd/key.rs | 3239 | `0a9da466be90eae2ae48b59eb6adf1445483e9b9198e314df14aac45c926eca2` | 0 |
| crates/malachite-cli/src/cmd/mod.rs | 741 | `f103ac7ae909e840aea595384f85f4900339f704531145da9b742fb9cf3cd26e` | 0 |
| crates/malachite-cli/src/cmd/start.rs | 64228 | `69aedb417d781ca03db79447aa750a019a647f8b21de55c332d64d64158f3810` | 0 |
| crates/malachite-cli/src/error.rs | 1963 | `368744ad553037c3eb60ed519e8a1c2a8751b7fd15cab885a841965f9644e1c5` | 0 |
| crates/malachite-cli/src/file.rs | 2104 | `23c25520bd142c9d7dd387154d6a0566498bf52280dd37f2d1b3d4d846fa43b6` | 0 |
| crates/malachite-cli/src/lib.rs | 845 | `65398d9ddeda4f21013ee547c0ab446174c67a7a6ce32ab72705d71976583c52` | 0 |
| crates/malachite-cli/src/logging.rs | 3347 | `892bc56cd5055a7e1901fc5b5011b84326621d10075f27210270b6e87b073f8c` | 0 |
| crates/malachite-cli/src/metrics.rs | 3969 | `7bcca5ad4f1af51650e27ac00a03f410422ce625d8a3dbe1e42de7c469e0aab8` | 0 |
| crates/malachite-cli/src/new.rs | 4378 | `ad66bb3aea1f42e0341570b74df646be030023dde463969fbe8e60c9d5a046bc` | 0 |
| crates/malachite-cli/src/runtime.rs | 1291 | `da4dccf2494b35de5051cbddf77615fd6155078b80b98849a744f3672a22b978` | 0 |
| crates/mesh-analysis/Cargo.toml | 600 | `1f2029691c90ba0dc8a6963d143e28e0363f1b030e2f86b55e351a165482cd3a` | 0 |
| crates/mesh-analysis/src/analyze.rs | 11476 | `b104539181bf9004516a9cbce9479ae4f6e65233571630dced680b599ef1a340` | 0 |
| crates/mesh-analysis/src/fetch.rs | 1902 | `35644539c5da12f22ef024fbf3838bdc93f1b70b326f4641db9f42185af378d3` | 0 |
| crates/mesh-analysis/src/lib.rs | 1204 | `7b7ae0d21743bcdbbacb23c3ae56d98b42a4812f3fb81d3c430b208daea20f3c` | 0 |
| crates/mesh-analysis/src/main.rs | 5131 | `3b38700b600eb2580c8aba7cd8b14d411b14c04007603989de5aecb66824d5e4` | 0 |
| crates/mesh-analysis/src/parse.rs | 10725 | `e98b01138ae97ec52988715783465a5e38baf9991e9cdd92788a2c516a696699` | 0 |
| crates/mesh-analysis/src/report.rs | 21201 | `cfab0bda342e407eb4ca9c2fb839bd4a32f842cf3dcefc894b3884d4746b830f` | 0 |
| crates/mesh-analysis/src/tier.rs | 7315 | `6dfc3cdec39174b4c8e18dda3a82bf430fa0be667505f9753f42abc789dfc7b4` | 0 |
| crates/mesh-analysis/src/types.rs | 4470 | `61229ab079a044c3e58cc2a591f70772aa9450d9eec32eb670ec2643ec856062` | 0 |
| crates/node/Cargo.toml | 2699 | `71e86956a4ceb9279ca319526c26e2a4d4ffc858623d693947d7ec4354f7494c` | 0 |
| crates/node/src/args.rs | 5690 | `ef55f273278c70e2edd5aec3e5afc5f26359d04e72321f5dd3ef4987ff1810bc` | 0 |
| crates/node/src/lib.rs | 1117 | `222dc8dbb389ffc86458afaa3180c117b11bf017feb73758c26e19d408268470` | 0 |
| crates/node/src/main.rs | 59061 | `0a338a30dc91fccc31d49f5515835fa6bbf806fdef4f710c5740e3b2f68804aa` | 0 |
| crates/node/src/metrics.rs | 1208 | `56e0258c7be17f0cfb571d73a3994e10e2c0af1e1fd9cd412db405e5af2e929f` | 0 |
| crates/pq-precompile/Cargo.toml | 434 | `2ac48178eb02afb9fd6c87b56abc50e63cca4c8b6f4a5f736313878802f1a6cb` | 0 |
| crates/pq-precompile/src/lib.rs | 10713 | `7dc6b9eb424053cf977f726602abfeabeff4f5b06f17d737907c7eeca96c8e3c` | 0 |
| crates/precompiles/Cargo.toml | 1389 | `1c364ce3c9d9453c031295963b274980e3eaacd99b3b9b3ee6510e43955b7468` | 0 |
| crates/precompiles/src/bin/generate_pq_test_vectors.rs | 2763 | `c6c925e90f303edb26a8954b15556642226cb8d5e97f9b9be6e68df7c847ab81` | 0 |
| crates/precompiles/src/call_from.rs | 18364 | `0b4aa52cb1e7d5d7ee9b1ac0e5e810f6f7a3946e8ae583eddd2b17ababd6fa2e` | 0 |
| crates/precompiles/src/helpers.rs | 50824 | `425612d11669684f15954f6cff822b6e6c3a28ab6685b6c2c474f8ace7c229f2` | 0 |
| crates/precompiles/src/lib.rs | 7460 | `001a43235b9c8ff3af09b069ea49f79b1488180c16ec18957db0308f141a1d34` | 0 |
| crates/precompiles/src/macros.rs | 5612 | `6f64927ac320247b806b4b0a2f7ab3c7759f1ea1a4096607c348872a494ec8b2` | 0 |
| crates/precompiles/src/native_coin_authority.rs | 100147 | `db22ab5be2dc4daad10ada283dd4dc43ae26d025732b010b252745617c5e7b83` | 0 |
| crates/precompiles/src/native_coin_control.rs | 48315 | `da22c78a060ba1b5248e27f44d87654054cd259dbfc02fa1f299c6f26a106ed5` | 0 |
| crates/precompiles/src/pq.rs | 10256 | `3963c67942011c41cea87531c2faf6c9199f1570c1999c0841b53eded82ac172` | 0 |
| crates/precompiles/src/pq_test_vectors.rs | 3024 | `81e460b9d42f7e76c946cd8dcbeb9e55fcbe349d83b556870bfb78683a601b4a` | 0 |
| crates/precompiles/src/precompile_provider.rs | 5602 | `91f0a57399bf96bd1f3445d91f323b21e2dbeee10aff039cc3811f7acb5ff434` | 0 |
| crates/precompiles/src/subcall.rs | 7013 | `1bd047487360ccf5b01c1af12a0d6e91be87c03636c2b4bdc05918f438029acf` | 0 |
| crates/precompiles/src/system_accounting.rs | 60318 | `e30da7119eabb9dc6eb06ce932edec30cfa81288cda19af0ee7589aeee49a8f5` | 0 |
| crates/quake/Cargo.toml | 2681 | `8bdfc75ab0b755f65833323050263a7304d1c6c7933fff70110981b4ed980f28` | 0 |
| crates/quake/macros/Cargo.toml | 189 | `4539dcf4332e36e359f63f12acaaf4ad3b720e8cf84e41dfb08358e75e5fc380` | 0 |
| crates/quake/macros/src/lib.rs | 4670 | `6aeb9f310a288021590e556e85d3f8716f477ea6f78d53abc5138d9809583b06` | 0 |
| crates/quake/src/build.rs | 7597 | `b9625b674ebf0998a678be680417a0450b91f166db21c8fdacb8edfcb46f4e19` | 0 |
| crates/quake/src/clean.rs | 6212 | `7bf5716b7749ede19158dcd9e8e6d3168714c4aa9b99c8ae0107609011a8b8d0` | 0 |
| crates/quake/src/cli_version.rs | 14120 | `2085087828d7b3e6fddad7fe1834c8bd33cfc5f787ce081fe9078b4a3930185c` | 0 |
| crates/quake/src/genesis.rs | 5322 | `4b6ec83191d2afc05e7b1b43ff53c3b68d5110c3fd851f753db93c48f1ae403e` | 0 |
| crates/quake/src/info.rs | 14669 | `5204e5f39b24d1cd37e4cdaeeb74b57e6800ce2f12f352b835742469b99ba1ce` | 0 |
| crates/quake/src/infra/docker.rs | 3772 | `8494889bb1303112bd3f7cba63d9aa8f901e5d716d37fd3b5f085d1e564fdf68` | 0 |
| crates/quake/src/infra/exec.rs | 3310 | `0b0b6124159d99eaa24a9985d989f295dec06a20a2ce5d4a5ee770d8e768bb7d` | 0 |
| crates/quake/src/infra/export.rs | 8907 | `088186198c532c1d4e29b31f9a3abb81637e4dd8cd96cd96df867aab9b188db2` | 0 |
| crates/quake/src/infra/local.rs | 11098 | `661dc4aba17f365220c47e90b4b886c1660b6de770c6066718a60cf728099469` | 0 |
| crates/quake/src/infra/mod.rs | 12177 | `36a818c7db8c7221be1c5cbd27bb7d8852f724dd74a0e4ffee3414a95be3b6f9` | 0 |
| crates/quake/src/infra/remote.rs | 29287 | `cb9580175ee174fe6756890d5aae9e21e986b447069e0244ccb8c9a75ce3d87c` | 0 |
| crates/quake/src/infra/ssm.rs | 42652 | `9cf7332bd156633329f98ecc19d9b7e2de01a7d83f170b7a3e960567eec9aa63` | 0 |
| crates/quake/src/infra/terraform.rs | 12065 | `2c6d252e29cc309f46460de54c44469f3cb3a39dde496baf3a5821ebde09a1d4` | 0 |
| crates/quake/src/latency.rs | 25599 | `c7c1b768fae04817e9a3f5504496ba26e1bbdec6dd27585f6be93199daf24fba` | 0 |
| crates/quake/src/load.rs | 17233 | `7d170ec7ee2506cc7a6206d460343a4c6ba6f8a6314cbf59c6375d6f08d487b8` | 0 |
| crates/quake/src/main.rs | 55538 | `a0799f66cf426437749f3105b35588674c7ac96c135ec19d7cf20f5f7bfb52d3` | 0 |
| crates/quake/src/manifest.rs | 106302 | `486dd94c0e68e4cb52477434cab2b338f41ad556b9f2e6658655777b2c098e6c` | 0 |
| crates/quake/src/manifest/flags.rs | 19120 | `88c169130d917e1cee97cec9e940c39fc189180b4885b0803a106e6bb626cabe` | 0 |
| crates/quake/src/manifest/generate.rs | 40448 | `ddfe73f2c78995c29cdbe94047a96986b82784b782492371993e90cd8c1bf7ee` | 0 |
| crates/quake/src/manifest/raw.rs | 48241 | `c4d3668903c205cc4f25e5013a2a38b20b611c596fcd904cba373c9b6a7644e1` | 0 |
| crates/quake/src/manifest/subnets.rs | 16817 | `b1b8ade64543478ed32d77865681e9c90440ed4667ce10d2e4c0dd4158b0269d` | 0 |
| crates/quake/src/mcp.rs | 60727 | `5a1841eb9a8b91b85b61297bf949c522833fd86c9bc94d7f7b16eca2873b1187` | 0 |
| crates/quake/src/mesh.rs | 1464 | `e74432a75ac5ca888d783ea09957f2703f90e0ab83be742f15177b3fd1545cda` | 0 |
| crates/quake/src/metrics.rs | 7245 | `90e2b88b21810215fbf064d50be4200c4dae0c4055a794fd41de5879eaccfb2b` | 0 |
| crates/quake/src/monitor.rs | 23887 | `e5863d716c6cb9bc3c32617cd840d6e670cec7b50d35b5cb3dc652b958c2b07c` | 0 |
| crates/quake/src/node.rs | 18307 | `d10b0b0ee887b86406619652213dcb4b2970fa6e1db81dfabd2e680a8ba3e0a9` | 0 |
| crates/quake/src/nodekey.rs | 9288 | `dac4f6d257240d7246f756d1199171d40df840eb59ff220c89d0276aedbab5c8` | 0 |
| crates/quake/src/nodes.rs | 29276 | `8a006666ade49ef5b75c8c3b89bb0598637e6ade5a929f9b483995690feae7e4` | 0 |
| crates/quake/src/perturb.rs | 30981 | `cd733afe44f5216efb6fcfbbe95b8ac3a3d195adc64073fbc2853457e192171a` | 0 |
| crates/quake/src/report.rs | 78547 | `bb1ac06dd185628ae4a110640ce8677af1204b6437a0bc78c34788ae17309c52` | 0 |
| crates/quake/src/rpc/mod.rs | 13136 | `f534ccb847cdd5dc523012da22e057b6aafb20e03c6c262f46924b0be575ef4e` | 0 |
| crates/quake/src/rpc/valset_manager.rs | 18099 | `d970e59689e268781357ccb0661a9b3b0e8c9a6b1744fcdcec60792223fcb6f5` | 0 |
| crates/quake/src/rpc_cmd.rs | 20085 | `bfe4ef5b6113e009ba2549c22d7bc0bf33487fd55151dbbbce75e7ba585a7316` | 0 |
| crates/quake/src/run.rs | 99014 | `7123bf9ca18fba6444163e9cc6d78aa7a70cf60de2553dc613912fdeab002b83` | 0 |
| crates/quake/src/setup.rs | 83580 | `6937f050482b3d9541bf532f1e21ef4a8b2eeda5f46f8bc23e3ef0a065b1091a` | 0 |
| crates/quake/src/shell.rs | 11621 | `6b050558984e8dd6fff674cd6a3868d5f1499e855966c5d01014de8830634f4a` | 0 |
| crates/quake/src/testnet.rs | 62626 | `7aa6847efcb6e321bd31302881644744fa3ebb94d1cdf0cb2748fef60b4dd6f8` | 0 |
| crates/quake/src/util.rs | 5284 | `36d5296c5420958e844119bda413e862e8f19ef5c5ff4cd1875d3e7e8ab6e4e7` | 0 |
| crates/quake/src/valset.rs | 3660 | `446bdf69bb7a2d3a59ca29eca781ef7c90f43b9088ece379b66e5193cd77007c` | 0 |
| crates/quake/src/wait.rs | 10757 | `15795ca1e62da071521e3829087622976c5546374733a5ab40eb87c213ba0ed3` | 0 |
| crates/quake/src/web.rs | 63845 | `1711b131afcb71b74d5065ffb637b4bba5af62a838a10dc03e37563aa76fa86c` | 0 |
| crates/remote-signer/Cargo.toml | 1112 | `c34c50ffc9653b5395ff96ae141680f1091eb243c33d90692bf3e6e4e4840f63` | 0 |
| crates/remote-signer/build.rs | 1607 | `f767eb732a7a5a079dbeb6a2f19ce52c49403a0bdb40c5c775987def589eceb6` | 0 |
| crates/remote-signer/proto/arc/signer/v1/signer.proto | 1143 | `9d575f7393db34af3b51c3dcaa439187f7ff7f9e9d63f5e31224cd6c4b66a942` | 0 |
| crates/remote-signer/src/client.rs | 14398 | `86a8aa6216ca3a2d87515da1244f9026066c1d29bfb31f9dd6680027b79acae3` | 0 |
| crates/remote-signer/src/config.rs | 5793 | `af0b7ed91c3baba97d32d5bd4d1f36765b3972f3b3d9e2f46db938c8c7d82c5e` | 0 |
| crates/remote-signer/src/error.rs | 1459 | `8b2f9ebc31b0da6b47dc7fae6302eb626c02dff207edeec8ca4d00b9f5576bc1` | 0 |
| crates/remote-signer/src/lib.rs | 1489 | `c6b8960b41ac9b6ccf3473140534129cac1f309e0eac2df1b1a53e4056fe9889` | 0 |
| crates/remote-signer/src/metrics.rs | 4690 | `bfdeaa4a532ed99d4210d425ffff08cd9026e29be0b99c1dd088fafe97925f9f` | 0 |
| crates/remote-signer/src/provider.rs | 22176 | `d65872545afaeeec53e826048cfedf37470f8e53c317608074867cbfd0ee003a` | 0 |
| crates/shared/Cargo.toml | 372 | `752a538cd952c779d08c514104618aeb766a60679da62d7b11fefcc634ca5eb2` | 0 |
| crates/shared/src/chain_ids.rs | 1036 | `703cc213fca3a3be7c36324df48561bbe50ad8c1bb6fee1f666f256d958f6ecc` | 0 |
| crates/shared/src/lib.rs | 762 | `bc7e8a932ca225fb31f8aaba6f6c656ab0c4604b71acfdf858787c22cc8ba3d5` | 0 |
| crates/shared/src/metrics/denylist.rs | 1456 | `c949f87174b93893c640639b359d314ed8c378430c8f26ea94dc363dba1ccc95` | 0 |
| crates/shared/src/metrics/mod.rs | 765 | `f5a5d676a468284be9aeb2458c0d9620cef4fa5dd0403ff6ca292f677ef8fe01` | 0 |
| crates/shared/src/metrics/validator_set.rs | 3270 | `69a5c71af1f84ed56463f00fedef74a39bf3887fad058223ead798a919a0144d` | 0 |
| crates/signer/Cargo.toml | 1349 | `1e41fc107282b3faf6490e2a34979f528cead9058296b263e5b9da3ea3961894` | 0 |
| crates/signer/src/lib.rs | 7008 | `0180306a8a404b01675998421f0970e898449211f4d9c3099a870c387804cbb3` | 0 |
| crates/signer/src/local.rs | 9411 | `7ee941a38ee12f1d0ae812618e9f3122087c87a815d957d2ed9314adbdd40fdc` | 0 |
| crates/signer/src/remote.rs | 699 | `2fd75d7cf46c4c5d2cd4d676c20bdc7518e5cf73e44e48db80a1b83d8695d921` | 0 |
| crates/snapshots/Cargo.toml | 964 | `465145e6099b04c6de80f213c2bf4240a599ce2b2949070cda711f29cee6f9eb` | 0 |
| crates/snapshots/src/download.rs | 106941 | `d4a410341ce811cf5bd548190a28bc88a00ab0b65c3fc2125ff607b24754d347` | 0 |
| crates/snapshots/src/lib.rs | 777 | `74875b8273f604a12c05452ae6329f8bae7b6a625af8b59e8265cbaba75ee654` | 0 |
| crates/snapshots/src/main.rs | 47026 | `b8beaf2d345bada34372fcb65516457dba70737e5c9f71e3bb71f8531a35ead0` | 0 |
| crates/snapshots/src/manifest.rs | 17279 | `f8be68cd3743010c80d5ae47cdad2ea1c679b9fa70244576f1e230e6c06ccf97` | 0 |
| crates/spammer/Cargo.toml | 1397 | `a2012da7f1c60b82e571742eb8d60b10483876a48bec5ada39371f05c76e78e1` | 0 |
| crates/spammer/src/accounts.rs | 7281 | `aa8313a7a71b80a521c197077e90eac3f57c1b0039b3c3e891200f7cb9c8098c` | 0 |
| crates/spammer/src/cli.rs | 21658 | `b5181a19df12642269e256e92b38b605647b80ecf9969644175ac955685d220c` | 0 |
| crates/spammer/src/config.rs | 23337 | `809486b71303f48164011bdfac3e216c6e8828ac791e5987033b6058945434a4` | 0 |
| crates/spammer/src/erc20.rs | 5165 | `3cec7645d751d6afeb9bcab75fef44b02dda2a9812c54879bedd6834ca9184df` | 0 |
| crates/spammer/src/generator.rs | 56015 | `7862edd64f3ca87ae1550482ab91544805a8cf0f2ca5ed28266da045f9c935ae` | 0 |
| crates/spammer/src/latency/block_stream.rs | 16577 | `a854ad26003c35dcc7ccc6c454cba6ff6096e08041f3987b951dfd4fce44a3f9` | 0 |
| crates/spammer/src/latency/csv.rs | 1700 | `060ee2585a488ce923491644268378c7a867ce2a0e231e55716fb2adb616d648` | 0 |
| crates/spammer/src/latency/mod.rs | 838 | `3921c47b50d2ded1a845a02503e2b979cda9a9efa0ef51591fd40733d434fdc5` | 0 |
| crates/spammer/src/latency/timestamp.rs | 3368 | `b679034594aaf0229c13ae22df18453650e760bfee16f5c92096b47b77f7090b` | 0 |
| crates/spammer/src/latency/tracker.rs | 20197 | `fb7d1d7b535d8c745cc4bb942edb3fb8d8a1ac496ed1bdbb2ec8ac73813c4d28` | 0 |
| crates/spammer/src/lib.rs | 1148 | `b07ad8ab32ed56c6b37518c00e9ce4bad2031fb1c17012f3a8110653199443e7` | 0 |
| crates/spammer/src/main.rs | 17698 | `03f6541d546497e9759f7b3c36c056b604f44b2711708240bb06074c111f2d50` | 0 |
| crates/spammer/src/rate_limiter.rs | 2544 | `445c1a65ca732c86b83fd7911ed7013a3d4f7b87695f6a6defe0810ed2dd7039` | 0 |
| crates/spammer/src/result_tracker.rs | 12194 | `0ac5f480907d2893cd9cb7e5e4d3640fb070c04880f547c5735fcb6bf08f7e84` | 0 |
| crates/spammer/src/sender.rs | 32459 | `876624240501c8be51b409bf669b6489604850d3927cabc13ffabe26170eddf3` | 0 |
| crates/spammer/src/spammer.rs | 31080 | `ef541eeebda114ebb91fdf96517e3838eb9b33b1a29c32067f01b98a598d2d53` | 0 |
| crates/spammer/src/ws.rs | 18381 | `bc82f9a2cd3ca4987ca10b06b985332c0d2f948eb5725fb2d4660631b85c7cf1` | 0 |
| crates/types/Cargo.toml | 2198 | `bef5415ba365daf5f495163ccea5b965af8958b559a5376e1e86ed504634b788` | 0 |
| crates/types/build.rs | 1309 | `da7966647ab7eb5688a0afd6dd3a48f262a7bb4595b16417c195bf6baf11089f` | 0 |
| crates/types/proto/arc/consensus/v1/consensus.proto | 2070 | `e8f86e1ac4a7534f788823cb32df1db39a912492f2f9ceb9a8de0cf60678914e` | 0 |
| crates/types/proto/arc/liveness/v1/liveness.proto | 1780 | `0cbe3d9f6c53f662e81b42c4c24a2c4ed259e259616e1e7f63f98a418e59f80c` | 0 |
| crates/types/proto/arc/store/v1/store.proto | 3040 | `5ed59a1e230ae77ae222417ace1db0d77e3da2d266fe9e51dcce3cc1615f03fd` | 0 |
| crates/types/proto/arc/sync/v1/sync.proto | 1881 | `fd4af642c70698001b7e75ab08b407c115b2af16e6d09e33a341c19c10fe16c0` | 0 |
| crates/types/src/address.rs | 10026 | `545dfd1944aa92abaf67ba6502ba21520b82489543979fdcab55d6cd4ee40e63` | 0 |
| crates/types/src/aliases.rs | 1141 | `58f39a0515fb1e2af52c28680f444fa04aa2d5b68a8c3f653f52d837696ff287` | 0 |
| crates/types/src/block.rs | 12335 | `ea0448ea1bfd67be595dbdee908a27567537d20092031ea33f8fe9dc1435d8ee` | 0 |
| crates/types/src/certificate.rs | 2015 | `746e91fcfd0d5ca321b4c659c5912c0b5e78239ca0f2b594aa3f9659c7778fd9` | 0 |
| crates/types/src/codec/error.rs | 984 | `c6df5f82f0bb203138bc32b59b8aea5bd37e76f154b5be4202d2a4e661890927` | 0 |
| crates/types/src/codec/mod.rs | 5346 | `7d49dbef1fd56f9843a0724ea8cfdefaae57785ec03d73f7f800a46db363cd01` | 0 |
| crates/types/src/codec/network.rs | 16629 | `48251d1f8c3faf4984bde36b07d3c060f067524815979595754255f47578b561` | 0 |
| crates/types/src/codec/proto.rs | 48334 | `442296defb2e70ce314cdaf9bb25c5ea4a3f6b3dc9f25bfbe3f581bdbb5e2df0` | 0 |
| crates/types/src/codec/versions.rs | 8745 | `d62a142a4dbfe5789666828ca06015f47c2626a5b1f92c4ac9904e1c75ed6b1b` | 0 |
| crates/types/src/codec/wal.rs | 12677 | `45f274d9c3cff57659b641fd43919186ebad0f96b98de5da543a71f8d706982a` | 0 |
| crates/types/src/commit_http.rs | 8488 | `d0e3e670fb3c50be861a40321cb306f3bc57bd5ac33523f1d93bac73c772b1df` | 0 |
| crates/types/src/config.rs | 14371 | `236eb6d26e39602dce25924234bce30b3fb53d04b3736a117ceceb7106194de8` | 0 |
| crates/types/src/consensus_params.rs | 16652 | `0c3a7d692886e68e8c682adafce417409930058593a22bb8104433a01e087ca9` | 0 |
| crates/types/src/context.rs | 10084 | `e9b977c9186970bd4f84a7408496b4a00fdb9640e790531bce9093228c7a5302` | 0 |
| crates/types/src/evidence.rs | 3947 | `6d5b89d0940580f70fcb534948e9d91c624fd5ead1b38d122eb07aa8d96df9ce` | 0 |
| crates/types/src/height.rs | 6805 | `fec6ca7ed9ba817d520f0fffda45fc74fa34b9e37b848250e2ddce77bf62aa91` | 0 |
| crates/types/src/lib.rs | 1682 | `f1a9863bf3e9b51aaf633f34b308ae0c7b9b388757e344ff1f3c902750542c89` | 0 |
| crates/types/src/proposal.rs | 5336 | `ecdd36b49d274967c04bfd503b6228396b0ce9a32ecea65d8e71f14e22f07049` | 0 |
| crates/types/src/proposal_monitor.rs | 13591 | `f61be836ca0f39a389e98187f3f6056bccc578d7fb3a818c4c2e0aaf803022f7` | 0 |
| crates/types/src/proposal_part.rs | 6961 | `b0e67dd548c42511e5cd460842ecdc6c7c83528d2861f662085ae373da11eed4` | 0 |
| crates/types/src/proposal_parts.rs | 6006 | `d032416d47adad7f2e2afc876c9321420efa660a222f6b36719cbc32b05136f5` | 0 |
| crates/types/src/proposer.rs | 2391 | `24b5579b63a3fefdf73771c5987dae5c7158af96df47d03c3ae12545872ff2d8` | 0 |
| crates/types/src/proto.rs | 2784 | `a03a00ff6b3bb4b31afc44e9ef95b93b841bb383c4137fd903d6d46c38ca0ed7` | 0 |
| crates/types/src/rpc_sync.rs | 13257 | `a1e4d1eced0e7ac13f7b79881885adebf7a73dd5ef9afc1964625d9c9bdf23ea` | 0 |
| crates/types/src/signing.rs | 1924 | `213fb515c28fb18323e8c5ee63a4acb4d04af0104919094c846a939a268b3b63` | 0 |
| crates/types/src/spec.rs | 19482 | `91deff630e7b08cbd524a3183188a24599b927b0252b66f2e6f04a8048ab97a9` | 0 |
| crates/types/src/ssz/mod.rs | 1009 | `ff4d888e5b6ea18f9d30b1982a450219f7eb3ba272741715b7ee2c3a66108e22` | 0 |
| crates/types/src/ssz/v1/block.rs | 1062 | `dd33683f1d6a0f33495d5d5361107c4c5310567eb5145ccfbbcafef83b00b593` | 0 |
| crates/types/src/ssz/v1/mod.rs | 936 | `f35a8a7d1d06a85a0108f0253f44a20f5da5d52a383aa70b357417f042c43463` | 0 |
| crates/types/src/ssz/v1/nil_or_val.rs | 3423 | `5007b6fd632c158160c79d9d2a02da239fa804913873345f062eb4ea023018bb` | 0 |
| crates/types/src/ssz/v1/round.rs | 2958 | `c04f81bb4f7aa68c8ae3a2b77b681f668cc6516b9d58b9acd133fc4be474b00f` | 0 |
| crates/types/src/ssz/v1/signature.rs | 1488 | `74585793a279e15c38f9f5d6f3042816c8ff34c329757cadc17f550bd23d3af3` | 0 |
| crates/types/src/ssz/v1/vote.rs | 3800 | `673a3c25af7c6f2d146445a56b55fc8924e9695ebba873189e6b16ff0728834e` | 0 |
| crates/types/src/sync.rs | 723 | `6850e99d719a460226f242153fa0357dd3488db452c62e80db46b690450e208d` | 0 |
| crates/types/src/validator_set.rs | 5928 | `d3e071804609f58c0c4751f91673581f3d1cfde514bcc86d7be8d24fa9f2150b` | 0 |
| crates/types/src/value.rs | 3611 | `1275e3324ae2cd4c603e53520e120524add6ca6755b95783e4e192b720aca195` | 0 |
| crates/types/src/vote.rs | 7059 | `21f56fdeed0e87daa6073e2e3aa529cc3aa47ed61c6fa7a52946c91f03fe0540` | 0 |
| crates/version/Cargo.toml | 397 | `405bfbaac7d95b1fd2c1e07835edd55e839632ef8fb051f507c980fd79d344e5` | 0 |
| crates/version/build.rs | 8138 | `fab40d5849bf921e834f186c0a88f19cec3fc74a6f17212347a00b9b82e13e84` | 0 |
| crates/version/src/lib.rs | 4133 | `37a96474e51362bf9011ac87c1d02c6a928a35a06095bc4b3a1e90abdf64c949` | 0 |
| eslint.config.mjs | 2040 | `556ad77bda33bb319dfabd7d05829626562427d9970ffa7fdabfbc99f1425946` | 0 |
| hardhat.config.ts | 3393 | `44c17bd01e187a8e8bd18866876f4b32d1abe37d51887a99349820fbfd187d7c` | 0 |
| package-lock.json | 526272 | `7ae179d633fbea0a1abcef0f9282e8b37b49cb7138caecee7510b865e601d80b` | 0 |
| package.json | 1202 | `b4335488168297ab7f9b3b5390eda9bd7618fce6eb997b6c929ab6efec9f6907` | 0 |
| rust-toolchain.toml | 66 | `4c0037189c8db7fc03ae3113ee1d9356b4c3960ebbb1db374027a51a99e450aa` | 0 |
| scripts/compare_saturation.py | 33924 | `8f1d0de7eefc91fe76f1ae5e3183128fc5def189f1de3ce21a2ec56b8794feb0` | 0 |
| scripts/engine-bench-report.py | 38302 | `4febf85619d75d5b94d075a50cdc70da4318917d8e30a2d6b30baa2d2ab48e27` | 0 |
| scripts/genesis/AccountCreator.ts | 9723 | `0eb23adaa4234e5b081cae85bc5782fd65452a0df9058673e3f4c9af86a7a987` | 0 |
| scripts/genesis/AdminUpgradeableProxy.ts | 2670 | `5785333efad8f599017c55b3911ee55e22ee8638c8f9d7c06e7c1346f071aef9` | 0 |
| scripts/genesis/Denylist.ts | 4115 | `9938b649d15f66d49ff10698347a4fdc170192c45a90ce76bf006e333bb08887` | 0 |
| scripts/genesis/NativeFiatToken.ts | 11197 | `1725eb119252e59b71bb4d14bdb17f8503f9228a11ad605ff6b55bdde1229722` | 0 |
| scripts/genesis/ProtocolConfig.ts | 8883 | `0a622ed6008ccc9f73a8662be2fc17ce18c1a6b7b9774cd398954a45dc60696a` | 0 |
| scripts/genesis/ValidatorManager.ts | 14538 | `42221bb951fc0b96a13c61939ae7d09e643e88a0d50d2e80b2d2a508e04a74de` | 0 |
| scripts/genesis/addresses.ts | 3055 | `ca33448377d52259a2c9b5515afdf9988417b5942a750a7ed9dfa3e9e5c7c989` | 0 |
| scripts/genesis/context.ts | 4125 | `7377c2f1ac0b660245fe086ebdbc5e37ae4e4ae26150d4e68d5780889d43d1a4` | 0 |
| scripts/genesis/genesis.ts | 11729 | `d25ba2f01dedb17254b46d97fa1fee284a48cc7edc54fd920d8fd3278fb5a131` | 0 |
| scripts/genesis/index.ts | 749 | `0b75bed3bc60c38776e6dad6cf9d355370e1c82948656980a1af2105e8f816de` | 0 |
| scripts/genesis/types.ts | 5911 | `5f4ed33b709c4ec8f6f659561f3bcb374d1dce502ad3989a66561c43d90c7756` | 0 |
| scripts/genesis/versions.ts | 1407 | `65e831e5179bdb30f06b76de8442ecfc7fccb6a4c730128fcdfb71e1485b3c54` | 0 |
| scripts/hardhat/chains/config.ts | 1342 | `b49059f1f27c38fe55ba460de66223e6109ac27b9b91fc70ba64fadabcb25713` | 0 |
| scripts/hardhat/chains/devnet.ts | 955 | `e0561140b7ab13f053cc01613f8e4471f27c777a0d6dc4dd21137fd1a1a6a942` | 0 |
| scripts/hardhat/chains/localdev.ts | 988 | `cd599681bce367d45d0c2993fbcc11c5ee258f0f79d7531531b422211f3b46a4` | 0 |
| scripts/hardhat/chains/testnet.ts | 957 | `a1b9fedd6124255a82f2798681e37f2611dcb2f404074299970deb27ea69f62e` | 0 |
| scripts/hardhat/tasks/genesis.ts | 5372 | `5facf107d591e7ad2f03d3d5ad4fd4292d566e5dc565acc021b1cf7110f2f718` | 0 |
| scripts/hardhat/tasks/query-fee.ts | 4756 | `6b83ab99d2f890ec3bc18c4fb216080b03ce012800194b0a7674924297762e1c` | 0 |
| scripts/hardhat/tasks/query-state.ts | 17370 | `2d3ed8c750d36f4e979398ddc08fe58b418c3046853aa6ac0aa230a97ecca5a4` | 0 |
| scripts/hardhat/viem-helper.ts | 2252 | `db96819326929b401313d5380c3082719f5eb61b7c5b05aef97ef6b63ec114ba` | 0 |
| scripts/localdev.mjs | 7661 | `84d49f04832663506c11bbc3a1dedf5c6af090a0764db68c5253baeb39b50b33` | 0 |
| scripts/md-exec.py | 27964 | `73d10e9269b09021c98b8a5734ac961c8d7c51b03d50a4ca60891c8f35d40783` | 0 |
| scripts/saturation_report.py | 58074 | `e140f1e7d1c364c5006bf52ad9e4f42defe75e63c47f1cfbd12f7b8f7374dadf` | 0 |
| scripts/tx_latency_report.py | 17015 | `03cdbe6ef992e7e866004f3c519e764fbee489439d85cb096e55b2afd37b7b4a` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/.mocharc.js | 70 | `434e1df653523a6bce5e53a62690018b51039b10fab4a734a10948bedd06789d` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/.solcover.js | 448 | `9111d1d9d5d8651916cf6e1afb033eeefd3f1ffa2d353a13f443518364c59420` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/certora/harnesses/AccessControlDefaultAdminRulesHarness.sol | 1454 | `e0ba6d8a937323046f2bbcc72ba70f7406276aa37b562e1a362004872def3ac8` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/certora/harnesses/AccessControlHarness.sol | 176 | `a49b1631dee3cd0b22358651751410bda67363f219d4c5dc5d9bcd105c5eb260` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/certora/harnesses/AccessManagedHarness.sol | 1636 | `e6d084707582b75bf29e170ec02da237fc21541e793a15b2b17482ed9e1a63f9` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/certora/harnesses/AccessManagerHarness.sol | 4475 | `65fc78a99fd9cfc3daec97c3b5656338e526a7ec639aaa304b185afb32fa50cf` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/certora/harnesses/DoubleEndedQueueHarness.sol | 1399 | `7473e0ca273983325153604dde0906745542b4ce90bf94984a0c86ea1f54f3b8` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/certora/harnesses/ERC20FlashMintHarness.sol | 1028 | `d14171faf0d2ccb9bf14fd9ad252c07e386689e69a39f0a65a7f5dae6540bcfe` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/certora/harnesses/ERC20PermitHarness.sol | 493 | `7f5eee48c453af458cec04df5678ee8618dd198d3ef399bd1e9efc543491cb97` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/certora/harnesses/ERC20WrapperHarness.sol | 1121 | `05f6d555cceadef86ae7dde4757897a685ed5c156e6034c7e1a760a8e54d133e` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/certora/harnesses/ERC3156FlashBorrowerHarness.sol | 405 | `68d31d5af5df023d29304b43e3720164b00d09c75240e9bad83995a8e138c9a6` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/certora/harnesses/ERC721Harness.sol | 891 | `69a5144e1ae8249774d795e69f815457f85d32b9aff3f3bcc8c15545233ff8bd` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/certora/harnesses/ERC721ReceiverHarness.sol | 325 | `ba334a1b77d8b0c5bf566957f03fab538938318f059fc1277ecd36e065e76ba1` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/certora/harnesses/EnumerableMapHarness.sol | 1488 | `9898955deb052f5c661ba6168e789f4f080f6a2a3411c7ad7412e76dd7b0a16b` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/certora/harnesses/EnumerableSetHarness.sol | 890 | `dc5621c2e221d8bf0e5eb74c841e44ab3f7b7568388f758db919c36e64658733` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/certora/harnesses/InitializableHarness.sol | 976 | `92af00cfefdefb5137d3fc9c0b615fd719a2ecab85832d28346b4d359ab54158` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/certora/harnesses/NoncesHarness.sol | 378 | `112c07190fdc3275661c418dcc9597de383422aa31fe76f861248bef979e9c94` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/certora/harnesses/Ownable2StepHarness.sol | 294 | `dd7ea7342e518bfdcbe4bf10980c1949e9ba67428f436b4d082b359560827eee` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/certora/harnesses/OwnableHarness.sol | 265 | `b285dad9f93bed4facd29fab94daea314baf78eab611daa3133323a2877a02ab` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/certora/harnesses/PausableHarness.sol | 387 | `d9c391078e05dceaa14d9731fb1542f5675b35670c556b705adb7c80b18e9374` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/certora/harnesses/TimelockControllerHarness.sol | 405 | `02d61705a0cce4d30449a7250da8e51e9eca48ce5598d962d9eadf6864096079` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/certora/run.js | 4317 | `650bcf5529ba30715fc0b215629a43439a2b4b3a977456b78ddc1912cf1a116c` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/access/AccessControlUpgradeable.sol | 8277 | `a5dee9f239e3334a7e3149dc9e72e2b0e7421813fb94660695b855384da6191e` | 1 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/access/Ownable2StepUpgradeable.sol | 3433 | `e65937e8c36af5c343406e97399759bd576090c0599b864bbea3501d617f7e1f` | 1 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/access/OwnableUpgradeable.sol | 3969 | `9247b9ad7939d23990dbdc9274917c3762ffb37e5137ef7bbfcc2e2fba1b8dd2` | 1 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/access/extensions/AccessControlDefaultAdminRulesUpgradeable.sol | 17149 | `7682ff33903dc82f397791cdf031a2409a87176f275492d0d5cb4003a2406fe8` | 1 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/access/extensions/AccessControlEnumerableUpgradeable.sol | 4786 | `758b88da96877250c4e3e3613492a78b489cc56e070817fce78abe0ce2939894` | 1 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/access/manager/AccessManagedUpgradeable.sol | 5891 | `2cef7cc20b5dc74d546ac3f401404a082d4851ff379ad9f418dc227321c2c83c` | 1 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/access/manager/AccessManagerUpgradeable.sol | 32629 | `cc4a118823d84eeb7736b60208a5658a1addfceada363d3c75afaf7049c46e95` | 1 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/account/extensions/draft-AccountERC7579HookedUpgradeable.sol | 5619 | `29aab215b51d8e252925aef0e5bca178ac7b9bfba160101cd3396c45db6ce4b9` | 1 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/account/extensions/draft-AccountERC7579Upgradeable.sol | 20341 | `60d31a8f7acce57ae28ffb6cc2d2bca0fb7cd09040b1072207c3b5978a11fc35` | 1 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/finance/VestingWalletCliffUpgradeable.sol | 3047 | `e1f8c203fd3ad167536df8dfa4fba69c67f02e19121992bf7dc3692f32b28104` | 1 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/finance/VestingWalletUpgradeable.sol | 7712 | `8bebf104cb5a34190b8172d01cb10b8fc8fb5f9285f6cac9ad6d0dc43110525b` | 1 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/GovernorUpgradeable.sol | 33882 | `0d312797476d43e317be31b5523109f97966c6961c0a1558735da5394dace4bd` | 1 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/TimelockControllerUpgradeable.sol | 18191 | `67598dee0ad0e2c520d260fbcd9f85dcf143be3d7494035df33883777653a69e` | 1 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorCountingFractionalUpgradeable.sol | 10843 | `061b370822d91306ce2bb53f4c4a8f6844ffe556575b6bcbbe36672e5a2ec8a1` | 1 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorCountingOverridableUpgradeable.sol | 10451 | `f490a2f9eebee3e3f1d04cc97592da67684fc098c528549cb5a958cc125d92d8` | 1 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorCountingSimpleUpgradeable.sol | 4613 | `f27144c31628b4c980d97a2c6aa2619a8117f0e5a34cddfbc5ed0e8a2f7b36c7` | 1 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorNoncesKeyedUpgradeable.sol | 3826 | `74bc08c63a08cc0f27c79a9aefb318f6dbb63d2023a29b4f1aabe84b8945624e` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorPreventLateQuorumUpgradeable.sol | 5463 | `69bb6d2fc9b613428a52d9f9f654da56f692269ba5a651e941b83283139d8c5f` | 1 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorProposalGuardianUpgradeable.sol | 3322 | `f02f5aaccf1c0e81c1c27c5d6c028e0fabca799ad15ac0115fab0d08fa8d88ee` | 1 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorSequentialProposalIdUpgradeable.sol | 4191 | `51b62f1d721d8ff75a85c623fc0176e87f355e7612487705abc0d0ecd35ea84a` | 1 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorSettingsUpgradeable.sol | 5062 | `86ffc956c7114026349b233ad8a3fb037d32d806b9c0578aaa9004831fcb49fe` | 1 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorStorageUpgradeable.sol | 5546 | `586f3115854f24130387b105e52d0a56d68b71cc5dc61227da359b8847c2afe8` | 1 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorSuperQuorumUpgradeable.sol | 3359 | `9a9eb6802563b915c630247a6197a38a7b98a460864421941e8a3d15887caac0` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorTimelockAccessUpgradeable.sol | 18438 | `a01b5b480a9b7f7357cebd5ce456a365829c08b456ad540587312c72d23f6849` | 1 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorTimelockCompoundUpgradeable.sol | 8169 | `f23f8c66c40ec824b70eb299737b4d10ebe56f41b0571cc5c557340f5c7988a3` | 1 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorTimelockControlUpgradeable.sol | 8358 | `17241d3e0c30cbb09345e08fede1616d13e9a890c0fd6e5022d7dc024653db7a` | 1 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorVotesQuorumFractionUpgradeable.sol | 5502 | `589df7421674804553bb75df000bfa76c4e0a0cd1d6d06d0ef51990db56e9f86` | 1 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorVotesSuperQuorumFractionUpgradeable.sol | 7231 | `cdcb483b88bc951937d851f8cb409f099c20104127cebc59af3ebd05e9174239` | 1 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorVotesUpgradeable.sol | 3001 | `447a653eb08b7b4101f6dfe56b0ff38f4290cf3d32b645c5fa9dc75330f8a7a3` | 1 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/utils/VotesExtendedUpgradeable.sol | 4830 | `cb284176a9167053ba0fddada9f68c493dc2a080e36798686f04c9fba8d70e6d` | 1 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/governance/utils/VotesUpgradeable.sol | 11103 | `2bd6798091ed10939dc9e421c1ca1734b4ed59572f838429fdab50eb74fffc6e` | 1 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/metatx/ERC2771ContextUpgradeable.sol | 3702 | `90b62c6898b5b616bfed1a0a9f917a49ecfb3c6dc35edf7521ce3a28bff5e640` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/metatx/ERC2771ForwarderUpgradeable.sol | 17542 | `4f713b7b52c6eae56070c299b7f103768e0713a355e8d8875dbca96471608593` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/package.json | 878 | `a2b61919debcbc734d1a7c7bd93a0154c8265a7912aff09c736db7cd022f6050` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/proxy/utils/Initializable.sol | 9223 | `f527a063813c2bf60c153fb08e38539578935402894fcc36fac42324ca325d3b` | 1 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/proxy/utils/UUPSUpgradeable.sol | 6573 | `2d07bcf9728190a5c807cf68defc3f3c52aa098d04770d44af37f30abade38d5` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/token/ERC1155/ERC1155Upgradeable.sol | 15694 | `b980ef2c998a057619a3a0d7cbcce4d8e234739cfafa5cec1964cf29c79e0862` | 1 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/token/ERC1155/extensions/ERC1155BurnableUpgradeable.sol | 1281 | `97afd1059918bdf9b365fb10550ea221ef142d45294da21e3dfff1bae5c50fe9` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/token/ERC1155/extensions/ERC1155PausableUpgradeable.sol | 1670 | `dd7257fc8906f0dba6fe58ef877db6cc588756dcb0ac54c93b2fc8620016f279` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/token/ERC1155/extensions/ERC1155SupplyUpgradeable.sol | 4147 | `8761aa791cb153deeb9fcce2ccb3cb752022e523281b915be396d96c6d25128d` | 1 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/token/ERC1155/extensions/ERC1155URIStorageUpgradeable.sol | 3292 | `7d202632221962f77ed8c1b8a9db24f5570ede69839e6da2648594d31ef98893` | 1 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/token/ERC1155/utils/ERC1155HolderUpgradeable.sol | 1717 | `9934f279898738b1e88ccdf4c4ca6e874d6d5a44c0a3528a3ea4edd0eb2e384a` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/token/ERC20/ERC20Upgradeable.sol | 12072 | `5c0c6f1cc199d0e388beb7cb63b8d157b878fe7018f29fe83a3dd3c9102c4e8b` | 1 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/token/ERC20/extensions/ERC1363Upgradeable.sol | 6063 | `9b2674535b02cc0c0006722c8d7e0f362ce0d4e30a5357d0ad16c8cd96701882` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/token/ERC20/extensions/ERC20BurnableUpgradeable.sol | 1495 | `15b8cfe5d0c0f93fd9cccdb25eb9b2e6ff6bf555bdf7110db305e53880435790` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/token/ERC20/extensions/ERC20CappedUpgradeable.sol | 2322 | `8886d1b6360942d139eb306dd3d73cb6dbaa77ea0ba0be6c62bd386ef8aedea9` | 1 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/token/ERC20/extensions/ERC20FlashMintUpgradeable.sol | 6084 | `ef30fc8af78eb529259a0a3216fc1062a086771d885a2fae618cab7158f28e5f` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/token/ERC20/extensions/ERC20PausableUpgradeable.sol | 1574 | `e802da2c7f567dc99019cdc6e146491a1a2c80924300a37097ad5322da1661f8` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/token/ERC20/extensions/ERC20PermitUpgradeable.sol | 3155 | `f624b376be44f15b6d25fc26bd3bd13f511160640d228c7e93dbf17310b81ab9` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/token/ERC20/extensions/ERC20VotesUpgradeable.sol | 3928 | `84cdb63ccc1699bd1816e5b143c10f35396cc1a6d11920f2830da622e924dac0` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/token/ERC20/extensions/ERC20WrapperUpgradeable.sol | 4831 | `00397ec06022f9a1e99359e3f9521e96b5cbcc324933462fdc71231c05456ec8` | 1 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/token/ERC20/extensions/ERC4626Upgradeable.sol | 13237 | `8769acf7e5cb0c978bdf117255097c59afb250b725f9114145eed6e59a9f35f0` | 1 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/token/ERC20/extensions/draft-ERC20BridgeableUpgradeable.sol | 2465 | `7d22b6638f0887d233d33b24097c5dded27eadf2a0b28ec7fae8475762a1b9c0` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/token/ERC20/extensions/draft-ERC20TemporaryApprovalUpgradeable.sol | 5557 | `5d904a21411b9c26476d0aef18b9d34f3ece98b7b65b6f6a6b784ffe5df516ec` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/token/ERC6909/draft-ERC6909Upgradeable.sol | 9516 | `13fda2d0565cba43651f3abfe3f83e10083ae92f058979b74c9e25791fe2e137` | 1 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/token/ERC6909/extensions/draft-ERC6909ContentURIUpgradeable.sol | 2766 | `85a6cd4c7d902d496bf76d874babd9ed00a480f47b913fa8fb67f6069d8ec225` | 1 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/token/ERC6909/extensions/draft-ERC6909MetadataUpgradeable.sol | 3788 | `fbd42d6c985aefe03bf6502d9030813a0e8c6abc25e6e4f5cc72a531ca132752` | 1 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/token/ERC6909/extensions/draft-ERC6909TokenSupplyUpgradeable.sol | 2247 | `2889ebe2756abe449c0735429d3dc16a46298eaabce749c46bcd8d227c3f0762` | 1 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/token/ERC721/ERC721Upgradeable.sol | 17744 | `2589016aed958e644f7235481c1639a8657640a746c33cbd9f42a5cc28519604` | 1 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/token/ERC721/extensions/ERC721BurnableUpgradeable.sol | 1195 | `b3c5805a42ec983a1daebdaacf2e3dbdc1dc68f3d14aa9eb307c22c729d72643` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/token/ERC721/extensions/ERC721ConsecutiveUpgradeable.sol | 8566 | `b4c727c3a0fad09d8872d7ccc8803d3df3a1c34226f9bf5b4ac97a458a6cf894` | 1 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/token/ERC721/extensions/ERC721EnumerableUpgradeable.sol | 8663 | `920effcf2f0fb79a5a197305adf24a4f2f12138313630be437a32cdfd5db9235` | 1 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/token/ERC721/extensions/ERC721PausableUpgradeable.sol | 1643 | `8a58a56c7e240fe767f09ddd3f6e90f3dccc4010366feb56ae8c4bc2cde0548a` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/token/ERC721/extensions/ERC721RoyaltyUpgradeable.sol | 1621 | `337c128044f7f3046091995b7ef4d01822b6d104dc46bb4549b6bde65d606006` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/token/ERC721/extensions/ERC721URIStorageUpgradeable.sol | 3162 | `205704dcb4f17cb667aecbb8a0a66bdd175012d342e1c3abd469b67449b8e7f3` | 1 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/token/ERC721/extensions/ERC721VotesUpgradeable.sol | 2140 | `6c22a84c27c0c12c9fea54db5e5fa95f542f64beafc03dd10bb427dbf1572b07` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/token/ERC721/extensions/ERC721WrapperUpgradeable.sol | 5341 | `265e00d60b434aabd5d40d9cb87dd8a6faae545a0e2f9a1954b69d680b08db22` | 1 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/token/ERC721/utils/ERC721HolderUpgradeable.sol | 1074 | `5f819dbf73677aecc2a8e7e5309a403e1b6c36296270f878fd54b2859420c83b` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/token/common/ERC2981Upgradeable.sol | 6427 | `6c8b441c325a9bbea847af197538a8abd28cdf9eadbf95690f5c5c5b3a57dcf6` | 1 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/utils/ContextUpgradeable.sol | 1194 | `a08e16324da33a9d666dc07a22ae58031c242a3869f6808e55b4b82fc70cb209` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/utils/MulticallUpgradeable.sol | 2005 | `28874e9eb73a2dcf03367ad26d89fd38d83f08509685c404a618f86435a8dd6d` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/utils/NoncesKeyedUpgradeable.sol | 4139 | `aeadfda6e58a8397a3537bc06dcf20d978fce932413beabdf2dc20004d6d9b07` | 1 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/utils/NoncesUpgradeable.sol | 2269 | `d63abfbf20ca119bf162ec5bb343df4b189208d1d0a73657555f688536498cd8` | 1 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/utils/PausableUpgradeable.sol | 3603 | `78df1c8d83d858b123485f7cc2e15e40e28d787a21f949374ee34aa45c1ad69c` | 1 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/utils/ReentrancyGuardTransientUpgradeable.sol | 2385 | `14bc1b2b959b74c3217ab4c14601b652f728248a4e4888a74015f7ef6ceb3cad` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/utils/ReentrancyGuardUpgradeable.sol | 4450 | `11b45418823fd6e961d8db5cf5c2795b08f51f88a66f8e37a38fcd052ee711a4` | 1 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/utils/cryptography/EIP712Upgradeable.sol | 8506 | `91c98a39169b1ad2a4babb09e7a7c89d895956739d3f960701911cbc8b542050` | 1 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/utils/cryptography/signers/MultiSignerERC7913Upgradeable.sol | 11359 | `4a8221d8eca6104d5e0930809e4f9fc3aec28b37881faaf94b1db33af269197e` | 1 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/utils/cryptography/signers/MultiSignerERC7913WeightedUpgradeable.sol | 10935 | `8474d0aea5fbe4f1cf39ac9af5d3fac24ebd2f760c951482a9f6bc65a9c19b39` | 1 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/utils/cryptography/signers/SignerECDSAUpgradeable.sol | 2859 | `4e34efe5321b72ee40b59be7bf509bd814c341c8e4c13ea613646dc68fbd7458` | 1 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/utils/cryptography/signers/SignerERC7913Upgradeable.sol | 3161 | `6bfab1f90384d13d5ab06a594e1efc0bbbedec5d6f5f6d7bb9488db284afdec6` | 1 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/utils/cryptography/signers/SignerP256Upgradeable.sol | 3112 | `d0f58b9ce96e54954d36320270899cedeaa98ae363a7064d47da83a51095ef42` | 1 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/utils/cryptography/signers/SignerRSAUpgradeable.sol | 3297 | `1d999567025d8a8d678ee3e38e987369cb882a2e8488dddff6165edeb0a512e6` | 1 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/utils/cryptography/signers/draft-ERC7739Upgradeable.sol | 4773 | `6d5b475659ded5c795d3c7dbbb608d8e584eb8d1b73b542ce443760893fae495` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/contracts/utils/introspection/ERC165Upgradeable.sol | 1151 | `d2105a1e3ba533399fb408105267329c2c134fcb18043a9c024d1b6e81982fc9` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/docs/config.js | 748 | `d5cdaf3c2d7b2724173f9664210cfae1aa4a700bf2a1f6a7b7820b74b04c15e7` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/docs/templates/helpers.js | 1423 | `c54072a039eb8e30ebdfc050e2366c4fd2d33aaef32693e000b355c28899fa13` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/docs/templates/properties.js | 2851 | `95274a10cfda2d35697e8ca57197757e9aa37e060db601bd8e1343be64eb8dd6` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/eslint.config.mjs | 636 | `4df149bf8e150d940a7a487ea567cba6d827796250772a2a073b9597cffb0791` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/hardhat.config.js | 3096 | `8e20b857a5f31aec1a213da42282f3fe0e3857dbf70b12a5a8cb6f87255db123` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/hardhat/async-test-sanity.js | 412 | `28d0b89767699dbf2d08c248727ba1ba99aed4ab723adeabdfb7da58b9680413` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/hardhat/common-contracts.js | 2990 | `762655bfdad5aa237ca4617c4eb64d51d75a185b69df4c0e5171cba063cf9bde` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/hardhat/env-artifacts.js | 1019 | `53209232db89939f0f8e047febfe15adfd52580c65594443e395423c7421f671` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/hardhat/ignore-unreachable-warnings.js | 2015 | `7d2b29651a623d2694aa22e8c185a9aae6a25c44023beb131bcb303de5033b75` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/hardhat/remappings.js | 508 | `8c937c074523720f867389503a24c6f1b24b729712995842fbb8fccf1c3fdb36` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/hardhat/skip-foundry-tests.js | 295 | `5e594373be07d38818abb95c62e159435c68e291aa230e7d95fc2e38f00cb8ea` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/hardhat/task-test-get-files.js | 1008 | `9851350b493983460df169f1c5dedac9c36930ee5bdbddaf977fb5fa75925a86` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/halmos-cheatcodes/src/SVM.sol | 2788 | `db2c73220b9f83d170e7c0ef085da11b5109a90441bb27326496d8f897b02a51` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/halmos-cheatcodes/src/SymTest.sol | 357 | `c5391a942e6ca4a31e1b48668ba80d12e5bc552453470fa153541ea322f8a88d` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/.mocharc.js | 70 | `434e1df653523a6bce5e53a62690018b51039b10fab4a734a10948bedd06789d` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/.solcover.js | 448 | `9111d1d9d5d8651916cf6e1afb033eeefd3f1ffa2d353a13f443518364c59420` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/certora/harnesses/AccessControlDefaultAdminRulesHarness.sol | 1454 | `e0ba6d8a937323046f2bbcc72ba70f7406276aa37b562e1a362004872def3ac8` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/certora/harnesses/AccessControlHarness.sol | 176 | `a49b1631dee3cd0b22358651751410bda67363f219d4c5dc5d9bcd105c5eb260` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/certora/harnesses/AccessManagedHarness.sol | 1636 | `e6d084707582b75bf29e170ec02da237fc21541e793a15b2b17482ed9e1a63f9` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/certora/harnesses/AccessManagerHarness.sol | 4475 | `65fc78a99fd9cfc3daec97c3b5656338e526a7ec639aaa304b185afb32fa50cf` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/certora/harnesses/DoubleEndedQueueHarness.sol | 1399 | `7473e0ca273983325153604dde0906745542b4ce90bf94984a0c86ea1f54f3b8` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/certora/harnesses/ERC20FlashMintHarness.sol | 1028 | `d14171faf0d2ccb9bf14fd9ad252c07e386689e69a39f0a65a7f5dae6540bcfe` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/certora/harnesses/ERC20PermitHarness.sol | 493 | `7f5eee48c453af458cec04df5678ee8618dd198d3ef399bd1e9efc543491cb97` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/certora/harnesses/ERC20WrapperHarness.sol | 1121 | `05f6d555cceadef86ae7dde4757897a685ed5c156e6034c7e1a760a8e54d133e` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/certora/harnesses/ERC3156FlashBorrowerHarness.sol | 405 | `68d31d5af5df023d29304b43e3720164b00d09c75240e9bad83995a8e138c9a6` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/certora/harnesses/ERC721Harness.sol | 891 | `69a5144e1ae8249774d795e69f815457f85d32b9aff3f3bcc8c15545233ff8bd` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/certora/harnesses/ERC721ReceiverHarness.sol | 325 | `ba334a1b77d8b0c5bf566957f03fab538938318f059fc1277ecd36e065e76ba1` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/certora/harnesses/EnumerableMapHarness.sol | 1488 | `9898955deb052f5c661ba6168e789f4f080f6a2a3411c7ad7412e76dd7b0a16b` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/certora/harnesses/EnumerableSetHarness.sol | 890 | `dc5621c2e221d8bf0e5eb74c841e44ab3f7b7568388f758db919c36e64658733` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/certora/harnesses/InitializableHarness.sol | 976 | `92af00cfefdefb5137d3fc9c0b615fd719a2ecab85832d28346b4d359ab54158` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/certora/harnesses/NoncesHarness.sol | 378 | `112c07190fdc3275661c418dcc9597de383422aa31fe76f861248bef979e9c94` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/certora/harnesses/Ownable2StepHarness.sol | 294 | `dd7ea7342e518bfdcbe4bf10980c1949e9ba67428f436b4d082b359560827eee` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/certora/harnesses/OwnableHarness.sol | 265 | `b285dad9f93bed4facd29fab94daea314baf78eab611daa3133323a2877a02ab` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/certora/harnesses/PausableHarness.sol | 387 | `d9c391078e05dceaa14d9731fb1542f5675b35670c556b705adb7c80b18e9374` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/certora/harnesses/TimelockControllerHarness.sol | 405 | `02d61705a0cce4d30449a7250da8e51e9eca48ce5598d962d9eadf6864096079` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/certora/run.js | 4317 | `650bcf5529ba30715fc0b215629a43439a2b4b3a977456b78ddc1912cf1a116c` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/access/AccessControl.sol | 7028 | `93c8ebfe7b36ef4d180f1660a5a741125691957726209720af476fdd5c7bac43` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/access/IAccessControl.sol | 3343 | `140304b7e99d517c57a13f391dfd3b550ca633a507f7b2af130f391b6cd89cc5` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/access/Ownable.sol | 3102 | `38578bd71c0a909840e67202db527cc6b4e6b437e0f39f0c909da32c1e30cb81` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/access/Ownable2Step.sol | 2476 | `c75345d7b9feef17ae29f2a800ca2f65f8021cf80436a41d6ec00f57f5180f36` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/access/extensions/AccessControlDefaultAdminRules.sol | 14734 | `54c4ee01bdbd8b8aac987cfea5e7c02eb69b417f5d645354267b2442475526cb` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/access/extensions/AccessControlEnumerable.sol | 3402 | `774f3a571556b120e3a26d0bdf5e970c5a65f0a7ed18bc14e3be69aac86974e3` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/access/extensions/IAccessControlDefaultAdminRules.sol | 8171 | `c2788df258d4e1aca2ed49195754790ae2c35fae061af58565bf5e3e02ff7ed1` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/access/extensions/IAccessControlEnumerable.sol | 1279 | `e0f69ae5acc588f27b8eba7f5a625f01409be5bb4a08e825774ccee32efc0ff9` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/access/manager/AccessManaged.sol | 4680 | `e5c9b2d8c676a69a12e054a0f5bdea62bd577bfc0831bd89ecc72e11ed157c91` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/access/manager/AccessManager.sol | 29876 | `72f06a0f03f2044d9b3bf036933aca7d589f0b8875a596206d50b696e59e8781` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/access/manager/AuthorityUtils.sol | 1376 | `d6d1da9c9278375b89aa4bae804f0ac36778badb8451b5fe77029a2d861135f6` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/access/manager/IAccessManaged.sol | 1111 | `2ef4db4c7c678372fe79af348ce3d60d4cf7136d195daf7a9bc2e434ffcbaacd` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/access/manager/IAccessManager.sol | 16314 | `5b98daaff196df5347fa5ddbdf48514007fa55b8e45f991da53458591905b5c5` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/access/manager/IAuthority.sol | 483 | `68428ead009a99c5270e2a0a93e4d2756b6f332ee14027963cc7bb06cd67a29a` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/account/Account.sol | 5163 | `fdd88fd15339ca8e7ff8284180140d4ad914feb61c2b5c042ebce0af86a80ba5` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/account/extensions/draft-AccountERC7579.sol | 19114 | `e61c0fd469d053b57549d4bdc648e6432e40bebe6ba699167ebc973d6caf8198` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/account/extensions/draft-AccountERC7579Hooked.sol | 4475 | `c59235653e2b81b4bc252e1b810b2716212a5b85b24138b9e881ea6fd95606ba` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/account/extensions/draft-ERC7821.sol | 2698 | `1945b38fe739ad1e5464a6b68616fad7f2c63fb60b6ed06a81574b60fbdfe217` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/account/utils/EIP7702Utils.sol | 721 | `19c252aea5567f6f066a2f9b4a7c10a9cf08c272fe39e09844a3660f71a850be` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/account/utils/draft-ERC4337Utils.sol | 8398 | `38521b36a804735004ce7d6858e9fa50951a77724d3045a31f51910d4548f3ea` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/account/utils/draft-ERC7579Utils.sol | 11312 | `819137a7c5f0da2ee64e8e16abd77a4125847c9a5748edd2fa369f69a83ad928` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/finance/VestingWallet.sol | 6055 | `3537b7f8c5a780ec0fc9c75f63ddc7b9a677a30f8237789e8162ebf405d1cebe` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/finance/VestingWalletCliff.sol | 2018 | `14981dea962b6c81e253295b702f2a461d7db60ae93715b293e95028d51b81f9` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/Governor.sol | 31931 | `a9fd3f809dcefe364c19b83b9ca8389a6e4d50f9d38bbb7ebef10724be2f9b74` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/IGovernor.sol | 16463 | `bc307a91cdad776b3219637649f6c89a9fae7099e9d0d2ab07c4fd3f31553a31` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/TimelockController.sol | 16324 | `4a5946a9ea4abbaef29225dc42da6c50c66bb13cae1b592607222599b0526f64` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorCountingFractional.sol | 9318 | `b4f872b9559fd97d98f868b1ea77ed18d9f27efb70e70686e8af581992d716fc` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorCountingOverridable.sol | 8692 | `abe4d4e13e4e846084d99e90d7cb132e4fc4cf085e1225074f6c2ee907339218` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorCountingSimple.sol | 3249 | `7b57caea0515e9121f2f2d64229b588609caab302eac01909c9d8361ae212554` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorNoncesKeyed.sol | 3442 | `8a550740cad348a89ea76c81f8d3563ffdb0db21cb9b94ed9cb43edfc84ed21f` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorPreventLateQuorum.sol | 4120 | `d50cf5e957c3ea9ff12992261eedd7231add05fb446277c39e72cda3288e3a9d` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorProposalGuardian.sol | 2273 | `c0a16f15c06bbbac8b3709e60b629cc8c20827b973e2cc11478f9ed2b8539a8c` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorSequentialProposalId.sol | 2823 | `8397bb8b90c99aa36fd1e5b1e993245db9d77fa24056a38cf642357ea160f36b` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorSettings.sol | 3554 | `bff3837e8deb8411352a71e43a0706d266b3dce29ef6fb5ce810af87eae3dbf7` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorStorage.sol | 4243 | `355a4f6a22c6483a63df4ec5e00f4fc64a8484535a043bcf14491698ffa5c0a0` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorSuperQuorum.sol | 3070 | `401eeeafc7f5548641136fc6560a72e4080fc3b7526771473b9d7bc86fd6210e` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorTimelockAccess.sol | 16249 | `a06730f1dc404e5c2b74ce2c60f7a37388e343f1a5ca29b817cdacfd2d340584` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorTimelockCompound.sol | 6362 | `9b7a53edfc89246735314c4eea84110540732a1602ba7a62f9fa4951b57ad6ff` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorTimelockControl.sol | 6620 | `1ceb0775536e4fbfbe2338f38f2d6fd5d44b126e5cd264a2a3b4e9d2746fd61d` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorVotes.sol | 1992 | `7df898e3e295914434fde0a7dbc890a5539fe2b61f2cbce6540d69014d416bcf` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorVotesQuorumFraction.sol | 4185 | `e7005800451ae5d1a678cb85acd4bfbc5ac80117b2dbdb49ebae98b81bd723d3` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorVotesSuperQuorumFraction.sol | 5625 | `fd6a895c1d26b9883e147121e6fad0e18d4558afc3fa24cb15bce64960fcfce1` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/utils/IVotes.sol | 2322 | `5876ce02c2f959a2b94a46735c8e4f9b717c645c9a47c72bc6e6ed1c659225e7` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/utils/Votes.sol | 9711 | `feded838fdab8e52e1a3352f95dd7e63311b2c079f2293bda17633fbefda6d96` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/utils/VotesExtended.sol | 3728 | `956c2a0ca22d5c2bbe3c700c4e3c47be67bcbfb240967654c85744fc8f7a7ca5` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC1155.sol | 189 | `4a472558a19793bd1ec0f09fd47c84774dfefbd15f9ba79f627de73629ab4df1` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC1155MetadataURI.sol | 233 | `bf8de067ebb7ec329c05c593f006ba6fbee9dbe9ed00dcd1e15852653c3ca5ec` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC1155Receiver.sol | 213 | `825aed7cb9f35079f4b12ada24b5cfee5e6a0bdceab0ae6fc3794d69e3d322e5` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC1271.sol | 656 | `2d17bba201aa2f9c55e317315b872272a60361848dfceb6b1e77081265c79a27` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC1363.sol | 4454 | `9c3a75a925a6dac9e88b03cddc58d42fe3131b0aaaad84408521f3f7af2f991b` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC1363Receiver.sol | 1316 | `39ebf8824bcd8d671abcc1afdd971cf63204b81318b83e0e4bbddebe256c6ff2` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC1363Spender.sol | 1119 | `594582216b8d5e0a5ff75d215f03ff8d1ad4fae69b069f04bec51ea6b605a9d1` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC165.sol | 193 | `dfb3f56fa928a7c6cae41a7ce2c86b9210fa18d33fa26389099d66a0fa790368` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC1820Implementer.sol | 768 | `99459de7cc9e3387a01835c34a6b5122163f20dbf19d4b1c4eb34489fe25c0c4` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC1820Registry.sol | 4836 | `d5c38c7fc97a0fc4c62cbe1987146e5a5ddfe84288dc84626f8affa41ef3d847` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC1967.sol | 637 | `c4e901318ab6d4963582c62c62ce988a34c68dbae71846b67decacde79e9a317` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC20.sol | 182 | `0158e2d3e0e28bedd99eec13dcf1a8aa3a70a5b7e4bb2ad709609c95fcc740d1` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC20Metadata.sol | 216 | `0ef8d844d8e066abd5c0d8cc1c550c89f2628a4ea9c9bb16c7593d4207800ca8` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC2309.sol | 533 | `a497c9e32f721912861542cc2a1c9b7b1bf566c8dafe430af5c06167a8222eb7` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC2612.sol | 245 | `7ebb71cd1a464a22ce7a4cdce29115d6569546fff8d5299ca3f2f7ba72b8e540` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC2981.sol | 1114 | `ea5f52ef580b9cb7c97091fd8164ec3ff211f5bdec359d18191eac4fcf7fcf76` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC3156.sol | 263 | `9fbd10c6970c328f348c9a86604bdad336743caeda2547f94b6a86d8a906c961` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC3156FlashBorrower.sol | 900 | `e4c78842b24628897539e92fbfbb9e82cda8e39c6e63edc0f43e5e1a58e9f952` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC3156FlashLender.sol | 1453 | `129df4dbdb600b20465a5e8b76a1701bf64cc234e6dd902ec6136b4e773eb5df` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC4626.sol | 12183 | `4e2150a099080629a8e9e30d346e79d92b6eedf8d6dfae3fdf1295fda0e146ec` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC4906.sol | 841 | `2b14563481c355e6a84127f0ee528d3e3b80fcdd76ff840660784c2445fcc0ae` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC5267.sol | 740 | `f89772d2d4fafcbef8b73bb10ee9a3373edec2eedb2f1b302320915b351dc3d1` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC5313.sol | 435 | `9c99e3d0f9a47337d59b7e245819b07860e329789aafb5d1275ffd27491686f0` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC5805.sol | 272 | `2b1e317a9ad0303948d00cfee78c42f99f7558c8d2002a7c63f04d2b70324cac` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC6372.sol | 520 | `b82e19cde1eaa6c179ac49ba38db89d8cf291522e3c7b90cc2dd327df2e6cc4d` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC721.sol | 185 | `4e4412e3eb28d5d2055e7b0e8153a2ab4d143f94e125a03a1b3d655ea7ed0002` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC721Enumerable.sol | 226 | `3c85a8e58edeeb5efcec3d274a25324c025d276fbc8d3d27d5ef4641fc1ca3c0` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC721Metadata.sol | 220 | `a8c823f1cee29f7169ded5e4a9204805343fd73d2fdbacf62d2d227f66abd960` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC721Receiver.sol | 209 | `875a2b4aaba1fe08770657ed44fcc4754a8f1ffed954eb06462dfe3b44338614` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC777.sol | 6733 | `9ed85c11bc308eeb33977efc9068fa948f952252982628c3729dae36c33684ab` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC777Recipient.sol | 1269 | `48473616ccf361df33723be1aab911bb41ab481dd9f2c3b4d2323bbba2523299` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC777Sender.sol | 1278 | `4ddc762186f658ea0a53496300c830c98f4a915c0a52afe5ddbc793ac3697ef1` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC7913.sol | 674 | `f66aad4249885b0f11369bfa825dded60aa4baa0d76d9becdac9daa48c350350` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/draft-IERC1822.sol | 882 | `73653312bc2eda0ec231553a5295242eaef2d4f46a023532d45fe76cbd0f565f` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/draft-IERC4337.sol | 10190 | `070fae39f5842c67f2ee0401d01d74ccd41b10ec4c030857428d34ec3782d8da` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/draft-IERC6093.sol | 6538 | `df936240c9a5d342582cbda70dd773b1c1d0e0dda3042b1c17b902ef0c36827b` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/draft-IERC6909.sol | 4039 | `95e299fdf3e700f7ad36c244b8ffe95d07cbeb3a318dc350cb2ec074c5f811ca` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/draft-IERC7579.sol | 8841 | `d42a07caf0e657d02a88afd53fe06a13a8bc01764b292bb3d7934fd4d7dc616d` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/draft-IERC7674.sol | 567 | `5e4dab6f3e075df9a22ca7d99c407e813b3444e69b23be10fcf92be1de0fee05` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/draft-IERC7802.sol | 1486 | `49d031a22c5aae86e6f7543e8e4ece83ef07275f1afbae0b99a3fe5d1e409c6b` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/draft-IERC7821.sol | 1758 | `809a971f062b7961518c410357d2cfa234ee3e07b08eca863c6aff5c54b85de1` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/metatx/ERC2771Context.sol | 3579 | `4a20dbcf842652e57b1bd4c3c08d8cbc2c0e167e2a5e8437e0d898a450443c34` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/metatx/ERC2771Forwarder.sol | 17002 | `823092e72404bac6612ee3dda312c79507d749ef265975fa84c686d0b2ee1ec9` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/package.json | 786 | `8c5b490fe133a9dda13c9a2915761c6b6c2e003a16c95863a800ce5527992bc4` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/proxy/Clones.sol | 14521 | `ae5a631c421d252eeeb842d83e581bcac1b3e88e24294df68ba0586bc105e507` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/proxy/ERC1967/ERC1967Proxy.sol | 1718 | `a06fe97082355529c1da9076ea6c4518875ca9fdb1a4fa1e194c35cff21b29a1` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/proxy/ERC1967/ERC1967Utils.sol | 6238 | `58c5b19893bf3d7f9e1aa0edc5b908b915eb7af4381800deb425a6e5331f4432` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/proxy/Proxy.sol | 2670 | `5f5081378d4bc82b814b0d64990b7f7b9c69697593b73a3341f4a269940ba540` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/proxy/beacon/BeaconProxy.sol | 2311 | `220626a31d80fb0d7a625f0c9ac741d40cd9f3c98ef74eb5b3dd43d224701282` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/proxy/beacon/IBeacon.sol | 473 | `c1c9726bbb0ec4c540c7c98059dcded69a8586b46c168036672381033ee76239` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/proxy/beacon/UpgradeableBeacon.sol | 2219 | `26dda9d5bb961b3df26602d49f9f5a0647cfdb78b63cc253aed8527030a64f25` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/proxy/transparent/ProxyAdmin.sol | 1965 | `4da9a90b1c8b45fdab7d73d8cf81f51cf7d990657ee4e3f943492c3bf0e4c2f1` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/proxy/transparent/TransparentUpgradeableProxy.sol | 6546 | `8391555685fb89d92ad37327d21e098b242058c10ded6398447b4eeb1c908ab0` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/proxy/utils/Initializable.sol | 9223 | `f527a063813c2bf60c153fb08e38539578935402894fcc36fac42324ca325d3b` | 1 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/proxy/utils/UUPSUpgradeable.sol | 6307 | `dc5dbb1675e3ca321b482eb6665b00a3b876f2119da1f0add8ef172a63eba2e1` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC1155/ERC1155.sol | 14340 | `a8216d80b0c17dc7b516692dff1880b133829c9e3864872b1a0a380cdb233234` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC1155/IERC1155.sol | 4750 | `62760e5ca354484140a29dddfa03b576c2e9e3adea6eb021eb28b394c085f3e4` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC1155/IERC1155Receiver.sol | 2599 | `3df310870e0187a59020ea48e910ed2693778b1f758b57b97a47365d74b92af5` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC1155/extensions/ERC1155Burnable.sol | 997 | `a8122e8e46870932b21294d5df9f013f6b1381fdad08ea7e7f48efe49cd3cb20` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC1155/extensions/ERC1155Pausable.sol | 1353 | `6bfd11fef86b179cc4369ebfc54926757d10820dd5552044215dc0213afe4c58` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC1155/extensions/ERC1155Supply.sol | 3141 | `8222e2a24621bfd8dcae6893e5f8dc53560a625002eacb95c43241641f38055c` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC1155/extensions/ERC1155URIStorage.sol | 2090 | `52bcb7aa728be29ef2dd0b328f1300a3748221b5c234ba71f80f979816d58196` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC1155/extensions/IERC1155MetadataURI.sol | 677 | `d5a148ccf8ac24f69f734cb2bcfba55ecc1d24209bf7aaa022cf3bde4bbe274f` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC1155/utils/ERC1155Holder.sol | 1319 | `08dbc044feab0e187a81a52142f907be598ecca0d35311766a346343af7b18af` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC1155/utils/ERC1155Utils.sol | 3554 | `8d75a5dd3db8f1c85362ef688d6f3cf5b2892dc62424bfe35678a49ce0d87956` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC20/ERC20.sol | 10798 | `9f906af4cba6e7e091dc12d45e6687e1239cf82d17678198424250fd64ab96bd` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC20/IERC20.sol | 2781 | `01b6f5c4fa45fd38822b286ecef6daf983d27306dd6362496fa71b3e4600b72c` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC20/extensions/ERC1363.sol | 5631 | `4ab0473a77a4bbcc4bbb8a22e2f2c56a451e85aa7014b7f4fb61e98373ca31a9` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC20/extensions/ERC20Burnable.sol | 1182 | `2e6108a11184dd0caab3f3ef31bd15fed1bc7e4c781a55bc867ccedd8474565c` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC20/extensions/ERC20Capped.sol | 1410 | `2403fec28c40f964320bfb4a025b12392ce240c732f648f9080e3521418ffea1` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC20/extensions/ERC20FlashMint.sol | 5772 | `50a9e14561603af062887bb3820c32cca62e9339042d480a8bed92b637d93ecd` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC20/extensions/ERC20Pausable.sol | 1261 | `12919f23b3b408e67b3b9c9543e37b7474e314d8f1c596472fd9201d9990a278` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC20/extensions/ERC20Permit.sol | 2729 | `076f17ea572a2761ec40fd5d4e982ef13c3e8fbd1b667628c50bf6e60ab0882f` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC20/extensions/ERC20Votes.sol | 3606 | `f2a0c9b7b4b67cec3ae19dad94454da68da553512f22e4eaf39c46447e11815a` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC20/extensions/ERC20Wrapper.sol | 3441 | `2a616f686774600c51ae2ed8a81735bc1e4171e3776897b97a2d0f1dbe0d6d14` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC20/extensions/ERC4626.sol | 12123 | `1411daee7cd45ad8b9eaccde2071ccfdf277b78f07e2591aca91c92c62d66c13` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC20/extensions/IERC20Metadata.sol | 684 | `0b7132f17d14d1d84b41b0bb429be62dafdff00fd3470f68724d8018eb07f57a` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC20/extensions/IERC20Permit.sol | 3806 | `e3e2cd98b7a5b9cba47c4ccec3685fdaf838a00e5d6f188b289907f9a6d0b58f` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC20/extensions/draft-ERC20Bridgeable.sol | 2039 | `6cc20d017e037dfbe92542dd0136c15ed1c19809591d3f34c1f73f9f8fe434e6` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC20/extensions/draft-ERC20TemporaryApproval.sol | 5125 | `3f14e8e359e07a1407659201abc760461fe7d2335bec5c3733e7e7d7672b5536` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC20/utils/ERC1363Utils.sol | 3297 | `17ed0dad7ec114eab7f188a8e5a410b37a43f556eb3893191f63da826052f860` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC20/utils/SafeERC20.sol | 10075 | `ac1fd9fa99b194a8db8dfa9ae8e3ff44feaa8f16668241fd2b66ae8b47d7c082` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC6909/draft-ERC6909.sol | 8265 | `d9b2febf476fd57c79113c66a9150494ec367741e3ce2983f0d8868ed581fcf0` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC6909/extensions/draft-ERC6909ContentURI.sol | 1638 | `141d7020907d74d0f61fb8cd939f35e1899fdffe2b971c8c54483474146904bc` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC6909/extensions/draft-ERC6909Metadata.sol | 2540 | `e0d0bdd8915804dcf091c7d182012b7a41b9451c8f0524855637f2d0f2b579f4` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC6909/extensions/draft-ERC6909TokenSupply.sol | 1258 | `ee998be397edc0f464cc05a7ed58e84889f23cab15e023681dc5b1645de84bb2` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC721/ERC721.sol | 16102 | `330a87f2bf94083df8ddd341735d712866455042aaca58d33ee1799773e1cae1` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC721/IERC721.sol | 4929 | `ff0eb9902bf0ac099205615fac90eacf34fae637571b05aab3ea35dea53d5f17` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC721/IERC721Receiver.sol | 997 | `eafee3ffdc7cb2fba4bf6bd16fb28f8e5b4679742e81c2ad42a1b1df5c179feb` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC721/extensions/ERC721Burnable.sol | 880 | `7b212ebdf844128dd2b3f02f824d7e855983495a75eea9c23852301c3887e861` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC721/extensions/ERC721Consecutive.sol | 7404 | `1a3649f45ee87e2dad54e9c2e88e1df8f5da303b520f02d51a65785ef86d2afd` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC721/extensions/ERC721Enumerable.sol | 7236 | `2eda4a86ad7947336c407da89826eb604dea67f966dccbf1fb04dca55666e130` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC721/extensions/ERC721Pausable.sol | 1328 | `d773f8c1ad695bad18631cec9f3ddfa337982a75562bb061f09f7ef4f216af7d` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC721/extensions/ERC721Royalty.sol | 1270 | `8c9d88365d8432d66b13ce8e8b5c12a2cfffd1cebbe181ac9cfa4190214a2e2a` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC721/extensions/ERC721URIStorage.sol | 2101 | `3d2ebf2cf0338322d3558ba67a7eb05ae2883cbdbb55c206cb516f101a339644` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC721/extensions/ERC721Votes.sol | 1831 | `37fdb0786bdfedc9e89357a9e9388ee92445ef6e14573e97348d03248ff70a80` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC721/extensions/ERC721Wrapper.sol | 4291 | `e646308e346689526041583bb2a426c5e95fa5bd9e77081fdc635b449abda505` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC721/extensions/IERC721Enumerable.sol | 1040 | `03c8c0b9ebbe6fe0a682332d9f980723996a1856ff0a767378eae95288069649` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC721/extensions/IERC721Metadata.sol | 792 | `33223782ea652dca413702ce92f9f59d91d758a035065b24bbedb7dc60c63a78` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC721/utils/ERC721Holder.sol | 795 | `fa1e231eedfd128232d8f34e9599165fb302c9dee5e58ef009f3b99f7e5d930d` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC721/utils/ERC721Utils.sol | 1922 | `f2041b1685dcf0cf6b968d9b8454e5a46068b1df5ab0e82ba0b269fa2f3099a8` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/common/ERC2981.sol | 5323 | `bac8f7ccae3c561a105a18cd1600ade43bb8856f9b7c9e0acc98d950af9ffa81` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/Address.sol | 5996 | `f1a9255dbc40cf9ae7c786abed3b022691a9d24bca0c7f05dc60e63421d405ab` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/Arrays.sol | 20906 | `8320f75b46c18204dd6f2b3654058129625b849a95c3a55a44ae531f77f0eca9` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/Base64.sol | 5183 | `b24abf66270126ee48e47646b1a2258b429aeb220b6ca828a1ee2163fd4dce87` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/Blockhash.sol | 2217 | `f6a4fd70d66fb0539083befe9079fcd6ae33b275a75f979fc4b06f545667b643` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/Bytes.sol | 4889 | `b8ecad25855c07fe0c65cffaf19c1517751b2837640f8a144ab26d5bf4e6f741` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/CAIP10.sol | 2377 | `5a1b57f39ae27e7da01e3c647964a38e516581b0505cf358c99aebe6eeb4d437` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/CAIP2.sol | 1919 | `cbf5e18e186a00400705880a4125d7e4534cdcefc484f96a33bd4b355bded8f6` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/Calldata.sol | 697 | `f400ffb13072d2cbe1de51c78e4fc38d1c29e2b1d7cb0b53c2641bed0effa4d6` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/Comparators.sol | 443 | `52fb1c8f57967d42a3214bde4a8a414ab25c2e3a844d00e171ca56487024e009` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/Context.sol | 963 | `847fda5460fee70f56f4200f59b82ae622bb03c79c77e67af010e31b7e2cc5b6` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/Create2.sol | 4466 | `1ddfef650decd5f4e4bb57ac5f42add20bf90bc8ff716de27b8f22619be332ef` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/Errors.sol | 896 | `0704b9d6c032cca8512a3bc3f30f49f86f1f03102d2896a3d23e794b82efea66` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/Multicall.sol | 1711 | `596b2e857cd4c3214279ec2ef46e160779bd80a0283d9b18bbb680e10ceb304e` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/Nonces.sol | 1490 | `9b4cbb85d1f5053c744e83302538eb643a713ffd14bc37665b224f1c66529339` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/NoncesKeyed.sol | 3264 | `ec835ccacbd09964b5ec4f46da1069e4bd6b943e5c7966ba6a4baad642ff62b1` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/Packing.sol | 64872 | `766829f6d9758a1318dd009143912d7aa6bbafa4f4b2a137c94d7f81a73b38ac` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/Panic.sol | 1973 | `270fc8401c1a13fae6a7a4a2dd6e381b95d658896701e51f0d3e2688acab3dec` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/Pausable.sol | 2706 | `2c26130748f06552c65ca74d89eaf78c9324a3cbac3ba6fdbadaa8beba0cb0b4` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/ReentrancyGuard.sol | 3384 | `32fbb1c908ec1b4de85cc1bb10091aebd5816ffe80dfdd5ca5e084fbea67a462` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/ReentrancyGuardTransient.sol | 2092 | `1797ed87f28982bf3226d3a77e9de83f49feb7a6f75e88d25540c57f8f26f98c` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/ShortStrings.sol | 4246 | `542d5dfe5e4375d83f2e3b5246b2d0d7507406a4b582844dbc73bd31ed2faa83` | 1 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/SlotDerivation.sol | 5323 | `daddbbeb265c87b7172548d58baede96b167cd89c6c7884ff2705676fab69438` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/StorageSlot.sol | 4182 | `75704538dcb223239280c6726d9a31cf769a7816718517c997fc7d63bdb70778` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/Strings.sol | 19280 | `2db7d21151644c57f75ed3ab55e87f3cf7fbf587a65345650fd740e2cfd50be3` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/TransientSlot.sol | 5075 | `ea92f361d697ba8b1fbd322b4d84b989998862c21fbebfa4b45289dc94a9eea2` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/cryptography/ECDSA.sol | 7815 | `0964ddd02f4a7a8cf9ba130e3aeead588ca3d425d5bc13cc4221358c69108ed0` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/cryptography/EIP712.sol | 6695 | `c20e0789a53610b2551058e0bd556dcd2caa20a7457348c3c73df037fba88861` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/cryptography/Hashes.sol | 1033 | `ecdbce11c5ecdf32b306e26b8ab1b878327c08154b4ccd04518b6b64b298cf31` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/cryptography/MerkleProof.sol | 24336 | `a174525c74ab5d2f066206ec9cebb6b3c618384c53ec35ad224ac1fbbf06b3f0` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/cryptography/MessageHashUtils.sol | 4251 | `936a89f512d5da84b0896b66d2398f2bea9eefdf2afa788af5265fcd74302693` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/cryptography/P256.sol | 19229 | `0d7bb2f2b5e0ceb0e1a28523ee179c1aee5980cb793df739dd9ccf87170dffe2` | 2 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/cryptography/RSA.sol | 8237 | `036c1fab2a132d7acb7fa0873812f2ad22c873d2efc91032b8ac7a1fda5ff476` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/cryptography/SignatureChecker.sol | 6048 | `df1954739f18679bae60450ccf2437a29a32a33e65756c1ec08e0f358c806246` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/cryptography/draft-ERC7739Utils.sol | 9415 | `ab478dab9c400f333e1cfd202508b9318d6e61b32e8929d4f5e91dd017973642` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/cryptography/signers/AbstractSigner.sol | 987 | `1119a95e6a2b709a6961fc9d5aa0a3d43249857d2edd05a174e191c573329111` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/cryptography/signers/MultiSignerERC7913.sol | 9742 | `aae5e64818e6ddc07063735bf0a98b8cdc370f02597e5c38af3d02041dbfbba2` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/cryptography/signers/MultiSignerERC7913Weighted.sol | 9474 | `3ff83c3c739a4f42172e133783b3a0f3206b6183791af9123920e34b1d35f82f` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/cryptography/signers/SignerECDSA.sol | 1880 | `79348d2204c34623df89352128f66e0cada694cb9c0e2637670810692d395955` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/cryptography/signers/SignerERC7702.sol | 858 | `0b51b0a3f797fd55a9f1815a669d097bf4d728354c5342a83fc936b570c117cb` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/cryptography/signers/SignerERC7913.sol | 2155 | `de875f910e523a88cbb3f0851f6b1b958de52b52ae262cd74efc9d9923448b94` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/cryptography/signers/SignerP256.sol | 2147 | `680777935eacce18916de879ce37d8c7592b35ada18ff701d94a0945589a3a74` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/cryptography/signers/SignerRSA.sol | 2340 | `35d55e0adc031d49ac802949cf933f6cbef8e9a43ebb6770a49a3d96656ae4b5` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/cryptography/signers/draft-ERC7739.sol | 4337 | `67bbe0cea35bf61fa4d567af0bace9c0930b516379e65fdb36235969b5a4d88b` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/cryptography/verifiers/ERC7913P256Verifier.sol | 1124 | `e65abb03ddb8062b534a09da74bef0765d47acdc25b8f390e3e7b12bf00cdf10` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/cryptography/verifiers/ERC7913RSAVerifier.sol | 876 | `924f6e04a2e03c62ae9667b604d32ac382c1aa512b1619183af670541c319aad` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/introspection/ERC165.sol | 879 | `61a2b12c96857aaa35f48aeda67a4281637a42494c0b3795be0ae976aa7b3793` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/introspection/ERC165Checker.sol | 5054 | `4a258c80eb26f4e93b0d80e470ea690d485cf4c0bb35300a693eea25182d9b15` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/introspection/IERC165.sol | 871 | `9055c2994b37dea1a41b7b7926dcb510f05dbe2540b0aafc5fbee9558fffd0ca` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/math/Math.sol | 32145 | `92fee281fd46a1b058b190cf21d6b1a528f0433a907850ae1c9bcf36c5c0cd98` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/math/SafeCast.sol | 34943 | `9769274bf53f26a7c7896c526ea1980dc9bea5bf5c2a5fd04870008c4afc1de9` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/math/SignedMath.sol | 2613 | `1ed50b1056af886752f0fb48a0165d381e69bb4a4b18b893b066dc144a7e08d7` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/structs/BitMaps.sol | 2020 | `12d7dd76e44e30d2d076df04f970a272969f30c2a2d240a89b6e2cac3f3e7c55` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/structs/Checkpoints.sol | 21428 | `d908ee19a12ef183693ba9635c4bd5ec902614c493fb7967898de286218e42f7` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/structs/CircularBuffer.sol | 5133 | `a1c6fdc6edc9a0e468f226c1365b6437d73eaedeb987d71d9ea386ab4299a7ba` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/structs/DoubleEndedQueue.sol | 5689 | `463c51e14acbb0b9afef3f1f6903203cce5798fb168742ccd7e049e0397b2184` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/structs/EnumerableMap.sol | 49145 | `90bdfbadfbb806a36dbc2facad96c850beb857f39ad5f48830244c48e7a735b6` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/structs/EnumerableSet.sol | 29625 | `53507e71995d0e76d29d6dd897d0bcc3f069fd81f03cb431d7342bdfcc0d5345` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/structs/Heap.sol | 10301 | `d9b945b169c77dd7d941a82e191edb709a31c0fb09e70252c32ec692b3d9c223` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/structs/MerkleTree.sol | 12091 | `93a746720b7de637066af1abe005ab1dcd340912d7c855199702ee76fa11bbe4` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/types/Time.sol | 5156 | `79534431c3934b23eafab9d02bda493cfc2ae383ba117a7c9698750c2e4845f1` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/vendor/compound/ICompoundTimelock.sol | 2357 | `b1062b283d59aea38dbecafabe94dedb7152b89ae001f85b35f86b3817929c4c` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/docs/config.js | 748 | `d5cdaf3c2d7b2724173f9664210cfae1aa4a700bf2a1f6a7b7820b74b04c15e7` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/docs/templates/helpers.js | 1423 | `c54072a039eb8e30ebdfc050e2366c4fd2d33aaef32693e000b355c28899fa13` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/docs/templates/properties.js | 2851 | `95274a10cfda2d35697e8ca57197757e9aa37e060db601bd8e1343be64eb8dd6` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/eslint.config.mjs | 636 | `4df149bf8e150d940a7a487ea567cba6d827796250772a2a073b9597cffb0791` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/hardhat.config.js | 3096 | `8e20b857a5f31aec1a213da42282f3fe0e3857dbf70b12a5a8cb6f87255db123` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/hardhat/async-test-sanity.js | 412 | `28d0b89767699dbf2d08c248727ba1ba99aed4ab723adeabdfb7da58b9680413` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/hardhat/common-contracts.js | 2990 | `762655bfdad5aa237ca4617c4eb64d51d75a185b69df4c0e5171cba063cf9bde` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/hardhat/env-artifacts.js | 1019 | `53209232db89939f0f8e047febfe15adfd52580c65594443e395423c7421f671` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/hardhat/ignore-unreachable-warnings.js | 2015 | `7d2b29651a623d2694aa22e8c185a9aae6a25c44023beb131bcb303de5033b75` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/hardhat/remappings.js | 508 | `8c937c074523720f867389503a24c6f1b24b729712995842fbb8fccf1c3fdb36` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/hardhat/skip-foundry-tests.js | 295 | `5e594373be07d38818abb95c62e159435c68e291aa230e7d95fc2e38f00cb8ea` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/hardhat/task-test-get-files.js | 1008 | `9851350b493983460df169f1c5dedac9c36930ee5bdbddaf977fb5fa75925a86` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/lib/halmos-cheatcodes/src/SVM.sol | 2788 | `db2c73220b9f83d170e7c0ef085da11b5109a90441bb27326496d8f897b02a51` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/lib/halmos-cheatcodes/src/SymTest.sol | 357 | `c5391a942e6ca4a31e1b48668ba80d12e5bc552453470fa153541ea322f8a88d` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/package-lock.json | 377238 | `129093d95e30e0242d685b74b08b4d3789f1c2104758ed8eb53c635ccd23e106` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/package.json | 3839 | `9623b9e2f7fec73a3b6b30fd1d843b17338be5107750e735a3dec375337af7ef` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/checks/compare-layout.js | 662 | `9db6f11c491c88e94eb7ca6700f50bfca1b6cd0ac5e1842ee797f89bff001140` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/checks/compareGasReports.js | 7020 | `d6023ec6f9b7ca10b8fd11c515fe945523d611295ce9b56b9282ca45c2c77401` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/checks/extract-layout.js | 1122 | `2c94e7b5cb32f542c6e4a7dd137a0d567114fa604d447d800013bed1b680ccb0` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/checks/inheritance-ordering.js | 2002 | `85382c6cab943e24e5f17c7d883746204095e0073f719950bb78fff88d29ff82` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/checks/pragma-consistency.js | 1883 | `e8c0f2fccfa56207d2846e7149a92ef63f334dd4d6dc22b587f8126367d0621c` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/fetch-common-contracts.js | 2048 | `2314e4bdabe3c33882c99f58323eb6e020674875c94c1b0daf7cb4ea898a0357` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/gen-nav.js | 1887 | `4230cfea9176a02373e09d7f0b560756edfd1f8ff3e1d30921efb22520100c6d` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/generate/format-lines.js | 422 | `de8e8ae2542d2db777ff3441efdd1b3f549c5ba473f1071180451c5e25575c12` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/generate/helpers/sanitize.js | 190 | `aa9db8aae572c1076e7d081114673a8fa56e8e228ff2f5e43d9454421e0686bb` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/generate/run.js | 2311 | `e746932be10a8bce1844601ab3cb2aa4fc8d02d1f89079bcbaa9d2e3b579a430` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/generate/templates/Arrays.js | 12531 | `47c29ad1985e8bab85f79f44837f298b80ca4875d8833123a67d89d7dd1cc097` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/generate/templates/Arrays.opts.js | 257 | `e462c6b4ad6c8bd988c50314ca276552ce4a571ba1436ac3163af0649e86c618` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/generate/templates/Checkpoints.js | 8340 | `288860f716d40a129b72a751b5c09993b40f9a0eac89165daa64888f356708ad` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/generate/templates/Checkpoints.opts.js | 411 | `47ac1d11a3e082049539e930b28e179cb665ce2c04e64bb434a606a591accaba` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/generate/templates/Checkpoints.t.js | 4505 | `9fbcfcfd9e57555b08e31efa26f902bcb009cb0f5e630296bd9647d4b430ab73` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/generate/templates/Enumerable.opts.js | 1465 | `d3e36cd8f6e76ac0b16bdb1e9930e52fb20cf05f779b54da327c7683f36f72bf` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/generate/templates/EnumerableMap.js | 15924 | `0e2b31077bca03ae8f8a21db4c7b1c7a97e53c651ac3fe64ee41df1f3308a82c` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/generate/templates/EnumerableSet.js | 16051 | `ff8b239ab8bc6b6f510fed09b630cd4c5d77a1b027f7e1d7e765260bd26a5793` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/generate/templates/MerkleProof.js | 7945 | `946bcad21a446465bb1626227d6b47ab08d51bc87fbdf8608fab69841a8b4f84` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/generate/templates/MerkleProof.opts.js | 307 | `b2dd437a8f00e7a973cceaf3d0faaa81f68c6a5e44cc9a48c6a9335c7b374de9` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/generate/templates/Packing.js | 2746 | `8fc4918bb789bf933638263c872ce22fc9f68ce6ae4c36d9d1f398b56a3faa54` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/generate/templates/Packing.opts.js | 80 | `97fc03e27e76666c1a564b07855bcf88924f65a7390ad27104ccd040193a7163` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/generate/templates/Packing.t.js | 1611 | `77a0937ce37a119f2aaa8ff50b6ebb54862220e85563549ab09198b6ec1426b5` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/generate/templates/SafeCast.js | 3770 | `463e6a7cb3ab55f541fb3d4312343d558c2695fb5240d36ce3d3f2ca7b319946` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/generate/templates/Slot.opts.js | 632 | `f566f7646afaa4a9731d38f05870539a2d2bfea84721c320aa1f4dd8a2879bfc` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/generate/templates/SlotDerivation.js | 3583 | `baca46f06b85655fa97b8a176b5db314d559b291166d1ffbe7f33f63e5bf9546` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/generate/templates/SlotDerivation.t.js | 3255 | `b7729e857cdae68348e875b14b64cbf71533dd7522f5c8553cee1c0ecb9f25d1` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/generate/templates/StorageSlot.js | 2321 | `daf387a4f34b198c78fe70fbeee28d5921630c6243c84fef988d04e4cbd6575f` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/generate/templates/StorageSlotMock.js | 1622 | `17cfce493dcaaa2e85ca1b01eea5bdc0ff8e501a4281c58073dc4852d0ebe899` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/generate/templates/TransientSlot.js | 2166 | `5ed88997123a71cf2408eff1bd9ec56b05b9457d9ede375186d4dcd329ca8933` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/generate/templates/TransientSlotMock.js | 804 | `5b8320fc0615731a32816a51e6ed535c72eaf8911217a69c66e85c4e49ff33e6` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/generate/templates/conversion.js | 678 | `134a41ead4e00cff47ef7d0f99b68dea2e730f5a8cc02dbca22f7603fb5b10f8` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/helpers.js | 155 | `58660f4bfe243e8720a6001ae4380d4329b2891b973bccc19a53d831c9535808` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/release/format-changelog.js | 1226 | `faff569d912d2a9823b70cb8476a5f8d276bfdb71fe97c5553db468aa6628f9d` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/release/synchronize-versions.js | 481 | `477c2b3c846a9faf36afa1a66d3ed8a7008a80aaec5a096ee7ed4d6a3ac1d54a` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/release/update-comment.js | 1280 | `258bad59128bf2f39480fc719a0d8b4b5874d84a877ca00953854f66ce3ef48d` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/release/workflow/github-release.js | 1660 | `4b88436e2c81e284ee0875402f21f63bb693ae3da96eac6d18d6cfdefb4217b4` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/release/workflow/rerun.js | 250 | `e6463d98a64df5794190341fe03aa3123dbac1d7ac46160b95bed3daa038aa0c` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/release/workflow/set-changesets-pr-title.js | 768 | `05305204f28f947b74ffa055756958d8ed7589ef5ded1b7fe711d1e463064747` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/release/workflow/state.js | 3595 | `daef1ae719c801d6cd20f69326d426609b9c78707146abfb3f170c91c52750dd` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/remove-ignored-artifacts.js | 1318 | `d760c8c71b7a6936b34c663402ec735f254d157830c6f2df3c1497b59b4ec806` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/solhint-custom/index.js | 2652 | `ec74c407ef34fcd219172a93948f1b1dd8e68b945883f188ed478877593a65a3` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/solhint-custom/package.json | 136 | `2440acd9a4aff80c411ae9e8eb96be37a45c9c3f9356a0ba8df687386986491f` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/update-docs-branch.js | 2095 | `e6e0877536359831c719b0c3fecd1a5eee8be527a06207bd1e31c436720bd46e` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/solhint.config.js | 695 | `4114184cd85c4d973d06e68746a2d8d7ba624cfebb28e4d26f80322dc4628f6e` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/package-lock.json | 377238 | `129093d95e30e0242d685b74b08b4d3789f1c2104758ed8eb53c635ccd23e106` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/package.json | 3851 | `568595c035e51cad38f2a1a87384b05d1283c38be01e8c1964e25e143a9353a4` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/scripts/checks/compare-layout.js | 662 | `9db6f11c491c88e94eb7ca6700f50bfca1b6cd0ac5e1842ee797f89bff001140` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/scripts/checks/compareGasReports.js | 7020 | `d6023ec6f9b7ca10b8fd11c515fe945523d611295ce9b56b9282ca45c2c77401` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/scripts/checks/extract-layout.js | 1122 | `2c94e7b5cb32f542c6e4a7dd137a0d567114fa604d447d800013bed1b680ccb0` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/scripts/checks/inheritance-ordering.js | 2002 | `85382c6cab943e24e5f17c7d883746204095e0073f719950bb78fff88d29ff82` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/scripts/checks/pragma-consistency.js | 1883 | `e8c0f2fccfa56207d2846e7149a92ef63f334dd4d6dc22b587f8126367d0621c` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/scripts/fetch-common-contracts.js | 2048 | `2314e4bdabe3c33882c99f58323eb6e020674875c94c1b0daf7cb4ea898a0357` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/scripts/gen-nav.js | 1887 | `4230cfea9176a02373e09d7f0b560756edfd1f8ff3e1d30921efb22520100c6d` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/scripts/generate/format-lines.js | 422 | `de8e8ae2542d2db777ff3441efdd1b3f549c5ba473f1071180451c5e25575c12` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/scripts/generate/helpers/sanitize.js | 190 | `aa9db8aae572c1076e7d081114673a8fa56e8e228ff2f5e43d9454421e0686bb` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/scripts/generate/run.js | 2311 | `e746932be10a8bce1844601ab3cb2aa4fc8d02d1f89079bcbaa9d2e3b579a430` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/scripts/generate/templates/Arrays.js | 12531 | `47c29ad1985e8bab85f79f44837f298b80ca4875d8833123a67d89d7dd1cc097` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/scripts/generate/templates/Arrays.opts.js | 257 | `e462c6b4ad6c8bd988c50314ca276552ce4a571ba1436ac3163af0649e86c618` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/scripts/generate/templates/Checkpoints.js | 8340 | `288860f716d40a129b72a751b5c09993b40f9a0eac89165daa64888f356708ad` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/scripts/generate/templates/Checkpoints.opts.js | 411 | `47ac1d11a3e082049539e930b28e179cb665ce2c04e64bb434a606a591accaba` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/scripts/generate/templates/Checkpoints.t.js | 4505 | `9fbcfcfd9e57555b08e31efa26f902bcb009cb0f5e630296bd9647d4b430ab73` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/scripts/generate/templates/Enumerable.opts.js | 1465 | `d3e36cd8f6e76ac0b16bdb1e9930e52fb20cf05f779b54da327c7683f36f72bf` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/scripts/generate/templates/EnumerableMap.js | 15924 | `0e2b31077bca03ae8f8a21db4c7b1c7a97e53c651ac3fe64ee41df1f3308a82c` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/scripts/generate/templates/EnumerableSet.js | 16051 | `ff8b239ab8bc6b6f510fed09b630cd4c5d77a1b027f7e1d7e765260bd26a5793` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/scripts/generate/templates/MerkleProof.js | 7945 | `946bcad21a446465bb1626227d6b47ab08d51bc87fbdf8608fab69841a8b4f84` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/scripts/generate/templates/MerkleProof.opts.js | 307 | `b2dd437a8f00e7a973cceaf3d0faaa81f68c6a5e44cc9a48c6a9335c7b374de9` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/scripts/generate/templates/Packing.js | 2746 | `8fc4918bb789bf933638263c872ce22fc9f68ce6ae4c36d9d1f398b56a3faa54` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/scripts/generate/templates/Packing.opts.js | 80 | `97fc03e27e76666c1a564b07855bcf88924f65a7390ad27104ccd040193a7163` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/scripts/generate/templates/Packing.t.js | 1611 | `77a0937ce37a119f2aaa8ff50b6ebb54862220e85563549ab09198b6ec1426b5` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/scripts/generate/templates/SafeCast.js | 3770 | `463e6a7cb3ab55f541fb3d4312343d558c2695fb5240d36ce3d3f2ca7b319946` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/scripts/generate/templates/Slot.opts.js | 632 | `f566f7646afaa4a9731d38f05870539a2d2bfea84721c320aa1f4dd8a2879bfc` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/scripts/generate/templates/SlotDerivation.js | 3583 | `baca46f06b85655fa97b8a176b5db314d559b291166d1ffbe7f33f63e5bf9546` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/scripts/generate/templates/SlotDerivation.t.js | 3255 | `b7729e857cdae68348e875b14b64cbf71533dd7522f5c8553cee1c0ecb9f25d1` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/scripts/generate/templates/StorageSlot.js | 2321 | `daf387a4f34b198c78fe70fbeee28d5921630c6243c84fef988d04e4cbd6575f` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/scripts/generate/templates/StorageSlotMock.js | 1622 | `17cfce493dcaaa2e85ca1b01eea5bdc0ff8e501a4281c58073dc4852d0ebe899` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/scripts/generate/templates/TransientSlot.js | 2166 | `5ed88997123a71cf2408eff1bd9ec56b05b9457d9ede375186d4dcd329ca8933` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/scripts/generate/templates/TransientSlotMock.js | 804 | `5b8320fc0615731a32816a51e6ed535c72eaf8911217a69c66e85c4e49ff33e6` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/scripts/generate/templates/conversion.js | 678 | `134a41ead4e00cff47ef7d0f99b68dea2e730f5a8cc02dbca22f7603fb5b10f8` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/scripts/helpers.js | 155 | `58660f4bfe243e8720a6001ae4380d4329b2891b973bccc19a53d831c9535808` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/scripts/release/format-changelog.js | 1226 | `faff569d912d2a9823b70cb8476a5f8d276bfdb71fe97c5553db468aa6628f9d` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/scripts/release/synchronize-versions.js | 481 | `477c2b3c846a9faf36afa1a66d3ed8a7008a80aaec5a096ee7ed4d6a3ac1d54a` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/scripts/release/update-comment.js | 1280 | `258bad59128bf2f39480fc719a0d8b4b5874d84a877ca00953854f66ce3ef48d` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/scripts/release/workflow/github-release.js | 1660 | `4b88436e2c81e284ee0875402f21f63bb693ae3da96eac6d18d6cfdefb4217b4` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/scripts/release/workflow/rerun.js | 250 | `e6463d98a64df5794190341fe03aa3123dbac1d7ac46160b95bed3daa038aa0c` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/scripts/release/workflow/set-changesets-pr-title.js | 768 | `05305204f28f947b74ffa055756958d8ed7589ef5ded1b7fe711d1e463064747` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/scripts/release/workflow/state.js | 3595 | `daef1ae719c801d6cd20f69326d426609b9c78707146abfb3f170c91c52750dd` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/scripts/remove-ignored-artifacts.js | 1318 | `d760c8c71b7a6936b34c663402ec735f254d157830c6f2df3c1497b59b4ec806` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/scripts/solhint-custom/index.js | 2652 | `ec74c407ef34fcd219172a93948f1b1dd8e68b945883f188ed478877593a65a3` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/scripts/solhint-custom/package.json | 136 | `2440acd9a4aff80c411ae9e8eb96be37a45c9c3f9356a0ba8df687386986491f` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/scripts/update-docs-branch.js | 2095 | `e6e0877536359831c719b0c3fecd1a5eee8be527a06207bd1e31c436720bd46e` | 0 |
| contracts/lib/openzeppelin-contracts-upgradeable/solhint.config.js | 695 | `4114184cd85c4d973d06e68746a2d8d7ba624cfebb28e4d26f80322dc4628f6e` | 0 |
| contracts/lib/openzeppelin-contracts/.mocharc.js | 70 | `434e1df653523a6bce5e53a62690018b51039b10fab4a734a10948bedd06789d` | 0 |
| contracts/lib/openzeppelin-contracts/.solcover.js | 448 | `9111d1d9d5d8651916cf6e1afb033eeefd3f1ffa2d353a13f443518364c59420` | 0 |
| contracts/lib/openzeppelin-contracts/certora/harnesses/AccessControlDefaultAdminRulesHarness.sol | 1454 | `e0ba6d8a937323046f2bbcc72ba70f7406276aa37b562e1a362004872def3ac8` | 0 |
| contracts/lib/openzeppelin-contracts/certora/harnesses/AccessControlHarness.sol | 176 | `a49b1631dee3cd0b22358651751410bda67363f219d4c5dc5d9bcd105c5eb260` | 0 |
| contracts/lib/openzeppelin-contracts/certora/harnesses/AccessManagedHarness.sol | 1636 | `e6d084707582b75bf29e170ec02da237fc21541e793a15b2b17482ed9e1a63f9` | 0 |
| contracts/lib/openzeppelin-contracts/certora/harnesses/AccessManagerHarness.sol | 4475 | `65fc78a99fd9cfc3daec97c3b5656338e526a7ec639aaa304b185afb32fa50cf` | 0 |
| contracts/lib/openzeppelin-contracts/certora/harnesses/DoubleEndedQueueHarness.sol | 1399 | `7473e0ca273983325153604dde0906745542b4ce90bf94984a0c86ea1f54f3b8` | 0 |
| contracts/lib/openzeppelin-contracts/certora/harnesses/ERC20FlashMintHarness.sol | 1028 | `d14171faf0d2ccb9bf14fd9ad252c07e386689e69a39f0a65a7f5dae6540bcfe` | 0 |
| contracts/lib/openzeppelin-contracts/certora/harnesses/ERC20PermitHarness.sol | 493 | `7f5eee48c453af458cec04df5678ee8618dd198d3ef399bd1e9efc543491cb97` | 0 |
| contracts/lib/openzeppelin-contracts/certora/harnesses/ERC20WrapperHarness.sol | 1121 | `05f6d555cceadef86ae7dde4757897a685ed5c156e6034c7e1a760a8e54d133e` | 0 |
| contracts/lib/openzeppelin-contracts/certora/harnesses/ERC3156FlashBorrowerHarness.sol | 405 | `68d31d5af5df023d29304b43e3720164b00d09c75240e9bad83995a8e138c9a6` | 0 |
| contracts/lib/openzeppelin-contracts/certora/harnesses/ERC721Harness.sol | 891 | `69a5144e1ae8249774d795e69f815457f85d32b9aff3f3bcc8c15545233ff8bd` | 0 |
| contracts/lib/openzeppelin-contracts/certora/harnesses/ERC721ReceiverHarness.sol | 325 | `ba334a1b77d8b0c5bf566957f03fab538938318f059fc1277ecd36e065e76ba1` | 0 |
| contracts/lib/openzeppelin-contracts/certora/harnesses/EnumerableMapHarness.sol | 1488 | `9898955deb052f5c661ba6168e789f4f080f6a2a3411c7ad7412e76dd7b0a16b` | 0 |
| contracts/lib/openzeppelin-contracts/certora/harnesses/EnumerableSetHarness.sol | 890 | `dc5621c2e221d8bf0e5eb74c841e44ab3f7b7568388f758db919c36e64658733` | 0 |
| contracts/lib/openzeppelin-contracts/certora/harnesses/InitializableHarness.sol | 976 | `92af00cfefdefb5137d3fc9c0b615fd719a2ecab85832d28346b4d359ab54158` | 0 |
| contracts/lib/openzeppelin-contracts/certora/harnesses/NoncesHarness.sol | 378 | `112c07190fdc3275661c418dcc9597de383422aa31fe76f861248bef979e9c94` | 0 |
| contracts/lib/openzeppelin-contracts/certora/harnesses/Ownable2StepHarness.sol | 294 | `dd7ea7342e518bfdcbe4bf10980c1949e9ba67428f436b4d082b359560827eee` | 0 |
| contracts/lib/openzeppelin-contracts/certora/harnesses/OwnableHarness.sol | 265 | `b285dad9f93bed4facd29fab94daea314baf78eab611daa3133323a2877a02ab` | 0 |
| contracts/lib/openzeppelin-contracts/certora/harnesses/PausableHarness.sol | 387 | `d9c391078e05dceaa14d9731fb1542f5675b35670c556b705adb7c80b18e9374` | 0 |
| contracts/lib/openzeppelin-contracts/certora/harnesses/TimelockControllerHarness.sol | 405 | `02d61705a0cce4d30449a7250da8e51e9eca48ce5598d962d9eadf6864096079` | 0 |
| contracts/lib/openzeppelin-contracts/certora/run.js | 4317 | `650bcf5529ba30715fc0b215629a43439a2b4b3a977456b78ddc1912cf1a116c` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/access/AccessControl.sol | 7028 | `93c8ebfe7b36ef4d180f1660a5a741125691957726209720af476fdd5c7bac43` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/access/IAccessControl.sol | 3343 | `140304b7e99d517c57a13f391dfd3b550ca633a507f7b2af130f391b6cd89cc5` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/access/Ownable.sol | 3102 | `38578bd71c0a909840e67202db527cc6b4e6b437e0f39f0c909da32c1e30cb81` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/access/Ownable2Step.sol | 2476 | `c75345d7b9feef17ae29f2a800ca2f65f8021cf80436a41d6ec00f57f5180f36` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/access/extensions/AccessControlDefaultAdminRules.sol | 14734 | `54c4ee01bdbd8b8aac987cfea5e7c02eb69b417f5d645354267b2442475526cb` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/access/extensions/AccessControlEnumerable.sol | 3402 | `774f3a571556b120e3a26d0bdf5e970c5a65f0a7ed18bc14e3be69aac86974e3` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/access/extensions/IAccessControlDefaultAdminRules.sol | 8171 | `c2788df258d4e1aca2ed49195754790ae2c35fae061af58565bf5e3e02ff7ed1` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/access/extensions/IAccessControlEnumerable.sol | 1279 | `e0f69ae5acc588f27b8eba7f5a625f01409be5bb4a08e825774ccee32efc0ff9` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/access/manager/AccessManaged.sol | 4680 | `e5c9b2d8c676a69a12e054a0f5bdea62bd577bfc0831bd89ecc72e11ed157c91` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/access/manager/AccessManager.sol | 29876 | `72f06a0f03f2044d9b3bf036933aca7d589f0b8875a596206d50b696e59e8781` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/access/manager/AuthorityUtils.sol | 1376 | `d6d1da9c9278375b89aa4bae804f0ac36778badb8451b5fe77029a2d861135f6` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/access/manager/IAccessManaged.sol | 1111 | `2ef4db4c7c678372fe79af348ce3d60d4cf7136d195daf7a9bc2e434ffcbaacd` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/access/manager/IAccessManager.sol | 16314 | `5b98daaff196df5347fa5ddbdf48514007fa55b8e45f991da53458591905b5c5` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/access/manager/IAuthority.sol | 483 | `68428ead009a99c5270e2a0a93e4d2756b6f332ee14027963cc7bb06cd67a29a` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/account/Account.sol | 5163 | `fdd88fd15339ca8e7ff8284180140d4ad914feb61c2b5c042ebce0af86a80ba5` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/account/extensions/draft-AccountERC7579.sol | 19114 | `e61c0fd469d053b57549d4bdc648e6432e40bebe6ba699167ebc973d6caf8198` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/account/extensions/draft-AccountERC7579Hooked.sol | 4475 | `c59235653e2b81b4bc252e1b810b2716212a5b85b24138b9e881ea6fd95606ba` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/account/extensions/draft-ERC7821.sol | 2698 | `1945b38fe739ad1e5464a6b68616fad7f2c63fb60b6ed06a81574b60fbdfe217` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/account/utils/EIP7702Utils.sol | 721 | `19c252aea5567f6f066a2f9b4a7c10a9cf08c272fe39e09844a3660f71a850be` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/account/utils/draft-ERC4337Utils.sol | 8398 | `38521b36a804735004ce7d6858e9fa50951a77724d3045a31f51910d4548f3ea` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/account/utils/draft-ERC7579Utils.sol | 11312 | `819137a7c5f0da2ee64e8e16abd77a4125847c9a5748edd2fa369f69a83ad928` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/finance/VestingWallet.sol | 6055 | `3537b7f8c5a780ec0fc9c75f63ddc7b9a677a30f8237789e8162ebf405d1cebe` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/finance/VestingWalletCliff.sol | 2018 | `14981dea962b6c81e253295b702f2a461d7db60ae93715b293e95028d51b81f9` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/governance/Governor.sol | 31931 | `a9fd3f809dcefe364c19b83b9ca8389a6e4d50f9d38bbb7ebef10724be2f9b74` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/governance/IGovernor.sol | 16463 | `bc307a91cdad776b3219637649f6c89a9fae7099e9d0d2ab07c4fd3f31553a31` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/governance/TimelockController.sol | 16324 | `4a5946a9ea4abbaef29225dc42da6c50c66bb13cae1b592607222599b0526f64` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorCountingFractional.sol | 9318 | `b4f872b9559fd97d98f868b1ea77ed18d9f27efb70e70686e8af581992d716fc` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorCountingOverridable.sol | 8692 | `abe4d4e13e4e846084d99e90d7cb132e4fc4cf085e1225074f6c2ee907339218` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorCountingSimple.sol | 3249 | `7b57caea0515e9121f2f2d64229b588609caab302eac01909c9d8361ae212554` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorNoncesKeyed.sol | 3442 | `8a550740cad348a89ea76c81f8d3563ffdb0db21cb9b94ed9cb43edfc84ed21f` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorPreventLateQuorum.sol | 4120 | `d50cf5e957c3ea9ff12992261eedd7231add05fb446277c39e72cda3288e3a9d` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorProposalGuardian.sol | 2273 | `c0a16f15c06bbbac8b3709e60b629cc8c20827b973e2cc11478f9ed2b8539a8c` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorSequentialProposalId.sol | 2823 | `8397bb8b90c99aa36fd1e5b1e993245db9d77fa24056a38cf642357ea160f36b` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorSettings.sol | 3554 | `bff3837e8deb8411352a71e43a0706d266b3dce29ef6fb5ce810af87eae3dbf7` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorStorage.sol | 4243 | `355a4f6a22c6483a63df4ec5e00f4fc64a8484535a043bcf14491698ffa5c0a0` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorSuperQuorum.sol | 3070 | `401eeeafc7f5548641136fc6560a72e4080fc3b7526771473b9d7bc86fd6210e` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorTimelockAccess.sol | 16249 | `a06730f1dc404e5c2b74ce2c60f7a37388e343f1a5ca29b817cdacfd2d340584` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorTimelockCompound.sol | 6362 | `9b7a53edfc89246735314c4eea84110540732a1602ba7a62f9fa4951b57ad6ff` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorTimelockControl.sol | 6620 | `1ceb0775536e4fbfbe2338f38f2d6fd5d44b126e5cd264a2a3b4e9d2746fd61d` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorVotes.sol | 1992 | `7df898e3e295914434fde0a7dbc890a5539fe2b61f2cbce6540d69014d416bcf` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorVotesQuorumFraction.sol | 4185 | `e7005800451ae5d1a678cb85acd4bfbc5ac80117b2dbdb49ebae98b81bd723d3` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorVotesSuperQuorumFraction.sol | 5625 | `fd6a895c1d26b9883e147121e6fad0e18d4558afc3fa24cb15bce64960fcfce1` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/governance/utils/IVotes.sol | 2322 | `5876ce02c2f959a2b94a46735c8e4f9b717c645c9a47c72bc6e6ed1c659225e7` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/governance/utils/Votes.sol | 9711 | `feded838fdab8e52e1a3352f95dd7e63311b2c079f2293bda17633fbefda6d96` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/governance/utils/VotesExtended.sol | 3728 | `956c2a0ca22d5c2bbe3c700c4e3c47be67bcbfb240967654c85744fc8f7a7ca5` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/interfaces/IERC1155.sol | 189 | `4a472558a19793bd1ec0f09fd47c84774dfefbd15f9ba79f627de73629ab4df1` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/interfaces/IERC1155MetadataURI.sol | 233 | `bf8de067ebb7ec329c05c593f006ba6fbee9dbe9ed00dcd1e15852653c3ca5ec` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/interfaces/IERC1155Receiver.sol | 213 | `825aed7cb9f35079f4b12ada24b5cfee5e6a0bdceab0ae6fc3794d69e3d322e5` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/interfaces/IERC1271.sol | 656 | `2d17bba201aa2f9c55e317315b872272a60361848dfceb6b1e77081265c79a27` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/interfaces/IERC1363.sol | 4454 | `9c3a75a925a6dac9e88b03cddc58d42fe3131b0aaaad84408521f3f7af2f991b` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/interfaces/IERC1363Receiver.sol | 1316 | `39ebf8824bcd8d671abcc1afdd971cf63204b81318b83e0e4bbddebe256c6ff2` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/interfaces/IERC1363Spender.sol | 1119 | `594582216b8d5e0a5ff75d215f03ff8d1ad4fae69b069f04bec51ea6b605a9d1` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/interfaces/IERC165.sol | 193 | `dfb3f56fa928a7c6cae41a7ce2c86b9210fa18d33fa26389099d66a0fa790368` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/interfaces/IERC1820Implementer.sol | 768 | `99459de7cc9e3387a01835c34a6b5122163f20dbf19d4b1c4eb34489fe25c0c4` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/interfaces/IERC1820Registry.sol | 4836 | `d5c38c7fc97a0fc4c62cbe1987146e5a5ddfe84288dc84626f8affa41ef3d847` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/interfaces/IERC1967.sol | 637 | `c4e901318ab6d4963582c62c62ce988a34c68dbae71846b67decacde79e9a317` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/interfaces/IERC20.sol | 182 | `0158e2d3e0e28bedd99eec13dcf1a8aa3a70a5b7e4bb2ad709609c95fcc740d1` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/interfaces/IERC20Metadata.sol | 216 | `0ef8d844d8e066abd5c0d8cc1c550c89f2628a4ea9c9bb16c7593d4207800ca8` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/interfaces/IERC2309.sol | 533 | `a497c9e32f721912861542cc2a1c9b7b1bf566c8dafe430af5c06167a8222eb7` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/interfaces/IERC2612.sol | 245 | `7ebb71cd1a464a22ce7a4cdce29115d6569546fff8d5299ca3f2f7ba72b8e540` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/interfaces/IERC2981.sol | 1114 | `ea5f52ef580b9cb7c97091fd8164ec3ff211f5bdec359d18191eac4fcf7fcf76` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/interfaces/IERC3156.sol | 263 | `9fbd10c6970c328f348c9a86604bdad336743caeda2547f94b6a86d8a906c961` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/interfaces/IERC3156FlashBorrower.sol | 900 | `e4c78842b24628897539e92fbfbb9e82cda8e39c6e63edc0f43e5e1a58e9f952` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/interfaces/IERC3156FlashLender.sol | 1453 | `129df4dbdb600b20465a5e8b76a1701bf64cc234e6dd902ec6136b4e773eb5df` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/interfaces/IERC4626.sol | 12183 | `4e2150a099080629a8e9e30d346e79d92b6eedf8d6dfae3fdf1295fda0e146ec` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/interfaces/IERC4906.sol | 841 | `2b14563481c355e6a84127f0ee528d3e3b80fcdd76ff840660784c2445fcc0ae` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/interfaces/IERC5267.sol | 740 | `f89772d2d4fafcbef8b73bb10ee9a3373edec2eedb2f1b302320915b351dc3d1` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/interfaces/IERC5313.sol | 435 | `9c99e3d0f9a47337d59b7e245819b07860e329789aafb5d1275ffd27491686f0` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/interfaces/IERC5805.sol | 272 | `2b1e317a9ad0303948d00cfee78c42f99f7558c8d2002a7c63f04d2b70324cac` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/interfaces/IERC6372.sol | 520 | `b82e19cde1eaa6c179ac49ba38db89d8cf291522e3c7b90cc2dd327df2e6cc4d` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/interfaces/IERC721.sol | 185 | `4e4412e3eb28d5d2055e7b0e8153a2ab4d143f94e125a03a1b3d655ea7ed0002` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/interfaces/IERC721Enumerable.sol | 226 | `3c85a8e58edeeb5efcec3d274a25324c025d276fbc8d3d27d5ef4641fc1ca3c0` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/interfaces/IERC721Metadata.sol | 220 | `a8c823f1cee29f7169ded5e4a9204805343fd73d2fdbacf62d2d227f66abd960` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/interfaces/IERC721Receiver.sol | 209 | `875a2b4aaba1fe08770657ed44fcc4754a8f1ffed954eb06462dfe3b44338614` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/interfaces/IERC777.sol | 6733 | `9ed85c11bc308eeb33977efc9068fa948f952252982628c3729dae36c33684ab` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/interfaces/IERC777Recipient.sol | 1269 | `48473616ccf361df33723be1aab911bb41ab481dd9f2c3b4d2323bbba2523299` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/interfaces/IERC777Sender.sol | 1278 | `4ddc762186f658ea0a53496300c830c98f4a915c0a52afe5ddbc793ac3697ef1` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/interfaces/IERC7913.sol | 674 | `f66aad4249885b0f11369bfa825dded60aa4baa0d76d9becdac9daa48c350350` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/interfaces/draft-IERC1822.sol | 882 | `73653312bc2eda0ec231553a5295242eaef2d4f46a023532d45fe76cbd0f565f` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/interfaces/draft-IERC4337.sol | 10190 | `070fae39f5842c67f2ee0401d01d74ccd41b10ec4c030857428d34ec3782d8da` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/interfaces/draft-IERC6093.sol | 6538 | `df936240c9a5d342582cbda70dd773b1c1d0e0dda3042b1c17b902ef0c36827b` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/interfaces/draft-IERC6909.sol | 4039 | `95e299fdf3e700f7ad36c244b8ffe95d07cbeb3a318dc350cb2ec074c5f811ca` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/interfaces/draft-IERC7579.sol | 8841 | `d42a07caf0e657d02a88afd53fe06a13a8bc01764b292bb3d7934fd4d7dc616d` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/interfaces/draft-IERC7674.sol | 567 | `5e4dab6f3e075df9a22ca7d99c407e813b3444e69b23be10fcf92be1de0fee05` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/interfaces/draft-IERC7802.sol | 1486 | `49d031a22c5aae86e6f7543e8e4ece83ef07275f1afbae0b99a3fe5d1e409c6b` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/interfaces/draft-IERC7821.sol | 1758 | `809a971f062b7961518c410357d2cfa234ee3e07b08eca863c6aff5c54b85de1` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/metatx/ERC2771Context.sol | 3579 | `4a20dbcf842652e57b1bd4c3c08d8cbc2c0e167e2a5e8437e0d898a450443c34` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/metatx/ERC2771Forwarder.sol | 17002 | `823092e72404bac6612ee3dda312c79507d749ef265975fa84c686d0b2ee1ec9` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/package.json | 786 | `8c5b490fe133a9dda13c9a2915761c6b6c2e003a16c95863a800ce5527992bc4` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/proxy/Clones.sol | 14521 | `ae5a631c421d252eeeb842d83e581bcac1b3e88e24294df68ba0586bc105e507` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/proxy/ERC1967/ERC1967Proxy.sol | 1718 | `a06fe97082355529c1da9076ea6c4518875ca9fdb1a4fa1e194c35cff21b29a1` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/proxy/ERC1967/ERC1967Utils.sol | 6238 | `58c5b19893bf3d7f9e1aa0edc5b908b915eb7af4381800deb425a6e5331f4432` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/proxy/Proxy.sol | 2670 | `5f5081378d4bc82b814b0d64990b7f7b9c69697593b73a3341f4a269940ba540` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/proxy/beacon/BeaconProxy.sol | 2311 | `220626a31d80fb0d7a625f0c9ac741d40cd9f3c98ef74eb5b3dd43d224701282` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/proxy/beacon/IBeacon.sol | 473 | `c1c9726bbb0ec4c540c7c98059dcded69a8586b46c168036672381033ee76239` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/proxy/beacon/UpgradeableBeacon.sol | 2219 | `26dda9d5bb961b3df26602d49f9f5a0647cfdb78b63cc253aed8527030a64f25` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/proxy/transparent/ProxyAdmin.sol | 1965 | `4da9a90b1c8b45fdab7d73d8cf81f51cf7d990657ee4e3f943492c3bf0e4c2f1` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/proxy/transparent/TransparentUpgradeableProxy.sol | 6546 | `8391555685fb89d92ad37327d21e098b242058c10ded6398447b4eeb1c908ab0` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/proxy/utils/Initializable.sol | 9223 | `f527a063813c2bf60c153fb08e38539578935402894fcc36fac42324ca325d3b` | 1 |
| contracts/lib/openzeppelin-contracts/contracts/proxy/utils/UUPSUpgradeable.sol | 6307 | `dc5dbb1675e3ca321b482eb6665b00a3b876f2119da1f0add8ef172a63eba2e1` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/token/ERC1155/ERC1155.sol | 14340 | `a8216d80b0c17dc7b516692dff1880b133829c9e3864872b1a0a380cdb233234` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/token/ERC1155/IERC1155.sol | 4750 | `62760e5ca354484140a29dddfa03b576c2e9e3adea6eb021eb28b394c085f3e4` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/token/ERC1155/IERC1155Receiver.sol | 2599 | `3df310870e0187a59020ea48e910ed2693778b1f758b57b97a47365d74b92af5` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/token/ERC1155/extensions/ERC1155Burnable.sol | 997 | `a8122e8e46870932b21294d5df9f013f6b1381fdad08ea7e7f48efe49cd3cb20` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/token/ERC1155/extensions/ERC1155Pausable.sol | 1353 | `6bfd11fef86b179cc4369ebfc54926757d10820dd5552044215dc0213afe4c58` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/token/ERC1155/extensions/ERC1155Supply.sol | 3141 | `8222e2a24621bfd8dcae6893e5f8dc53560a625002eacb95c43241641f38055c` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/token/ERC1155/extensions/ERC1155URIStorage.sol | 2090 | `52bcb7aa728be29ef2dd0b328f1300a3748221b5c234ba71f80f979816d58196` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/token/ERC1155/extensions/IERC1155MetadataURI.sol | 677 | `d5a148ccf8ac24f69f734cb2bcfba55ecc1d24209bf7aaa022cf3bde4bbe274f` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/token/ERC1155/utils/ERC1155Holder.sol | 1319 | `08dbc044feab0e187a81a52142f907be598ecca0d35311766a346343af7b18af` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/token/ERC1155/utils/ERC1155Utils.sol | 3554 | `8d75a5dd3db8f1c85362ef688d6f3cf5b2892dc62424bfe35678a49ce0d87956` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/token/ERC20/ERC20.sol | 10798 | `9f906af4cba6e7e091dc12d45e6687e1239cf82d17678198424250fd64ab96bd` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/token/ERC20/IERC20.sol | 2781 | `01b6f5c4fa45fd38822b286ecef6daf983d27306dd6362496fa71b3e4600b72c` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/token/ERC20/extensions/ERC1363.sol | 5631 | `4ab0473a77a4bbcc4bbb8a22e2f2c56a451e85aa7014b7f4fb61e98373ca31a9` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/token/ERC20/extensions/ERC20Burnable.sol | 1182 | `2e6108a11184dd0caab3f3ef31bd15fed1bc7e4c781a55bc867ccedd8474565c` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/token/ERC20/extensions/ERC20Capped.sol | 1410 | `2403fec28c40f964320bfb4a025b12392ce240c732f648f9080e3521418ffea1` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/token/ERC20/extensions/ERC20FlashMint.sol | 5772 | `50a9e14561603af062887bb3820c32cca62e9339042d480a8bed92b637d93ecd` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/token/ERC20/extensions/ERC20Pausable.sol | 1261 | `12919f23b3b408e67b3b9c9543e37b7474e314d8f1c596472fd9201d9990a278` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/token/ERC20/extensions/ERC20Permit.sol | 2729 | `076f17ea572a2761ec40fd5d4e982ef13c3e8fbd1b667628c50bf6e60ab0882f` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/token/ERC20/extensions/ERC20Votes.sol | 3606 | `f2a0c9b7b4b67cec3ae19dad94454da68da553512f22e4eaf39c46447e11815a` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/token/ERC20/extensions/ERC20Wrapper.sol | 3441 | `2a616f686774600c51ae2ed8a81735bc1e4171e3776897b97a2d0f1dbe0d6d14` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/token/ERC20/extensions/ERC4626.sol | 12123 | `1411daee7cd45ad8b9eaccde2071ccfdf277b78f07e2591aca91c92c62d66c13` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/token/ERC20/extensions/IERC20Metadata.sol | 684 | `0b7132f17d14d1d84b41b0bb429be62dafdff00fd3470f68724d8018eb07f57a` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/token/ERC20/extensions/IERC20Permit.sol | 3806 | `e3e2cd98b7a5b9cba47c4ccec3685fdaf838a00e5d6f188b289907f9a6d0b58f` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/token/ERC20/extensions/draft-ERC20Bridgeable.sol | 2039 | `6cc20d017e037dfbe92542dd0136c15ed1c19809591d3f34c1f73f9f8fe434e6` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/token/ERC20/extensions/draft-ERC20TemporaryApproval.sol | 5125 | `3f14e8e359e07a1407659201abc760461fe7d2335bec5c3733e7e7d7672b5536` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/token/ERC20/utils/ERC1363Utils.sol | 3297 | `17ed0dad7ec114eab7f188a8e5a410b37a43f556eb3893191f63da826052f860` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/token/ERC20/utils/SafeERC20.sol | 10075 | `ac1fd9fa99b194a8db8dfa9ae8e3ff44feaa8f16668241fd2b66ae8b47d7c082` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/token/ERC6909/draft-ERC6909.sol | 8265 | `d9b2febf476fd57c79113c66a9150494ec367741e3ce2983f0d8868ed581fcf0` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/token/ERC6909/extensions/draft-ERC6909ContentURI.sol | 1638 | `141d7020907d74d0f61fb8cd939f35e1899fdffe2b971c8c54483474146904bc` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/token/ERC6909/extensions/draft-ERC6909Metadata.sol | 2540 | `e0d0bdd8915804dcf091c7d182012b7a41b9451c8f0524855637f2d0f2b579f4` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/token/ERC6909/extensions/draft-ERC6909TokenSupply.sol | 1258 | `ee998be397edc0f464cc05a7ed58e84889f23cab15e023681dc5b1645de84bb2` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/token/ERC721/ERC721.sol | 16102 | `330a87f2bf94083df8ddd341735d712866455042aaca58d33ee1799773e1cae1` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/token/ERC721/IERC721.sol | 4929 | `ff0eb9902bf0ac099205615fac90eacf34fae637571b05aab3ea35dea53d5f17` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/token/ERC721/IERC721Receiver.sol | 997 | `eafee3ffdc7cb2fba4bf6bd16fb28f8e5b4679742e81c2ad42a1b1df5c179feb` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/token/ERC721/extensions/ERC721Burnable.sol | 880 | `7b212ebdf844128dd2b3f02f824d7e855983495a75eea9c23852301c3887e861` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/token/ERC721/extensions/ERC721Consecutive.sol | 7404 | `1a3649f45ee87e2dad54e9c2e88e1df8f5da303b520f02d51a65785ef86d2afd` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/token/ERC721/extensions/ERC721Enumerable.sol | 7236 | `2eda4a86ad7947336c407da89826eb604dea67f966dccbf1fb04dca55666e130` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/token/ERC721/extensions/ERC721Pausable.sol | 1328 | `d773f8c1ad695bad18631cec9f3ddfa337982a75562bb061f09f7ef4f216af7d` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/token/ERC721/extensions/ERC721Royalty.sol | 1270 | `8c9d88365d8432d66b13ce8e8b5c12a2cfffd1cebbe181ac9cfa4190214a2e2a` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/token/ERC721/extensions/ERC721URIStorage.sol | 2101 | `3d2ebf2cf0338322d3558ba67a7eb05ae2883cbdbb55c206cb516f101a339644` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/token/ERC721/extensions/ERC721Votes.sol | 1831 | `37fdb0786bdfedc9e89357a9e9388ee92445ef6e14573e97348d03248ff70a80` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/token/ERC721/extensions/ERC721Wrapper.sol | 4291 | `e646308e346689526041583bb2a426c5e95fa5bd9e77081fdc635b449abda505` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/token/ERC721/extensions/IERC721Enumerable.sol | 1040 | `03c8c0b9ebbe6fe0a682332d9f980723996a1856ff0a767378eae95288069649` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/token/ERC721/extensions/IERC721Metadata.sol | 792 | `33223782ea652dca413702ce92f9f59d91d758a035065b24bbedb7dc60c63a78` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/token/ERC721/utils/ERC721Holder.sol | 795 | `fa1e231eedfd128232d8f34e9599165fb302c9dee5e58ef009f3b99f7e5d930d` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/token/ERC721/utils/ERC721Utils.sol | 1922 | `f2041b1685dcf0cf6b968d9b8454e5a46068b1df5ab0e82ba0b269fa2f3099a8` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/token/common/ERC2981.sol | 5323 | `bac8f7ccae3c561a105a18cd1600ade43bb8856f9b7c9e0acc98d950af9ffa81` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/utils/Address.sol | 5996 | `f1a9255dbc40cf9ae7c786abed3b022691a9d24bca0c7f05dc60e63421d405ab` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/utils/Arrays.sol | 20906 | `8320f75b46c18204dd6f2b3654058129625b849a95c3a55a44ae531f77f0eca9` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/utils/Base64.sol | 5183 | `b24abf66270126ee48e47646b1a2258b429aeb220b6ca828a1ee2163fd4dce87` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/utils/Blockhash.sol | 2217 | `f6a4fd70d66fb0539083befe9079fcd6ae33b275a75f979fc4b06f545667b643` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/utils/Bytes.sol | 4889 | `b8ecad25855c07fe0c65cffaf19c1517751b2837640f8a144ab26d5bf4e6f741` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/utils/CAIP10.sol | 2377 | `5a1b57f39ae27e7da01e3c647964a38e516581b0505cf358c99aebe6eeb4d437` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/utils/CAIP2.sol | 1919 | `cbf5e18e186a00400705880a4125d7e4534cdcefc484f96a33bd4b355bded8f6` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/utils/Calldata.sol | 697 | `f400ffb13072d2cbe1de51c78e4fc38d1c29e2b1d7cb0b53c2641bed0effa4d6` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/utils/Comparators.sol | 443 | `52fb1c8f57967d42a3214bde4a8a414ab25c2e3a844d00e171ca56487024e009` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/utils/Context.sol | 963 | `847fda5460fee70f56f4200f59b82ae622bb03c79c77e67af010e31b7e2cc5b6` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/utils/Create2.sol | 4466 | `1ddfef650decd5f4e4bb57ac5f42add20bf90bc8ff716de27b8f22619be332ef` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/utils/Errors.sol | 896 | `0704b9d6c032cca8512a3bc3f30f49f86f1f03102d2896a3d23e794b82efea66` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/utils/Multicall.sol | 1711 | `596b2e857cd4c3214279ec2ef46e160779bd80a0283d9b18bbb680e10ceb304e` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/utils/Nonces.sol | 1490 | `9b4cbb85d1f5053c744e83302538eb643a713ffd14bc37665b224f1c66529339` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/utils/NoncesKeyed.sol | 3264 | `ec835ccacbd09964b5ec4f46da1069e4bd6b943e5c7966ba6a4baad642ff62b1` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/utils/Packing.sol | 64872 | `766829f6d9758a1318dd009143912d7aa6bbafa4f4b2a137c94d7f81a73b38ac` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/utils/Panic.sol | 1973 | `270fc8401c1a13fae6a7a4a2dd6e381b95d658896701e51f0d3e2688acab3dec` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/utils/Pausable.sol | 2706 | `2c26130748f06552c65ca74d89eaf78c9324a3cbac3ba6fdbadaa8beba0cb0b4` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/utils/ReentrancyGuard.sol | 3384 | `32fbb1c908ec1b4de85cc1bb10091aebd5816ffe80dfdd5ca5e084fbea67a462` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/utils/ReentrancyGuardTransient.sol | 2092 | `1797ed87f28982bf3226d3a77e9de83f49feb7a6f75e88d25540c57f8f26f98c` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/utils/ShortStrings.sol | 4246 | `542d5dfe5e4375d83f2e3b5246b2d0d7507406a4b582844dbc73bd31ed2faa83` | 1 |
| contracts/lib/openzeppelin-contracts/contracts/utils/SlotDerivation.sol | 5323 | `daddbbeb265c87b7172548d58baede96b167cd89c6c7884ff2705676fab69438` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/utils/StorageSlot.sol | 4182 | `75704538dcb223239280c6726d9a31cf769a7816718517c997fc7d63bdb70778` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/utils/Strings.sol | 19280 | `2db7d21151644c57f75ed3ab55e87f3cf7fbf587a65345650fd740e2cfd50be3` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/utils/TransientSlot.sol | 5075 | `ea92f361d697ba8b1fbd322b4d84b989998862c21fbebfa4b45289dc94a9eea2` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/utils/cryptography/ECDSA.sol | 7815 | `0964ddd02f4a7a8cf9ba130e3aeead588ca3d425d5bc13cc4221358c69108ed0` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/utils/cryptography/EIP712.sol | 6695 | `c20e0789a53610b2551058e0bd556dcd2caa20a7457348c3c73df037fba88861` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/utils/cryptography/Hashes.sol | 1033 | `ecdbce11c5ecdf32b306e26b8ab1b878327c08154b4ccd04518b6b64b298cf31` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/utils/cryptography/MerkleProof.sol | 24336 | `a174525c74ab5d2f066206ec9cebb6b3c618384c53ec35ad224ac1fbbf06b3f0` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/utils/cryptography/MessageHashUtils.sol | 4251 | `936a89f512d5da84b0896b66d2398f2bea9eefdf2afa788af5265fcd74302693` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/utils/cryptography/P256.sol | 19229 | `0d7bb2f2b5e0ceb0e1a28523ee179c1aee5980cb793df739dd9ccf87170dffe2` | 2 |
| contracts/lib/openzeppelin-contracts/contracts/utils/cryptography/RSA.sol | 8237 | `036c1fab2a132d7acb7fa0873812f2ad22c873d2efc91032b8ac7a1fda5ff476` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/utils/cryptography/SignatureChecker.sol | 6048 | `df1954739f18679bae60450ccf2437a29a32a33e65756c1ec08e0f358c806246` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/utils/cryptography/draft-ERC7739Utils.sol | 9415 | `ab478dab9c400f333e1cfd202508b9318d6e61b32e8929d4f5e91dd017973642` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/utils/cryptography/signers/AbstractSigner.sol | 987 | `1119a95e6a2b709a6961fc9d5aa0a3d43249857d2edd05a174e191c573329111` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/utils/cryptography/signers/MultiSignerERC7913.sol | 9742 | `aae5e64818e6ddc07063735bf0a98b8cdc370f02597e5c38af3d02041dbfbba2` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/utils/cryptography/signers/MultiSignerERC7913Weighted.sol | 9474 | `3ff83c3c739a4f42172e133783b3a0f3206b6183791af9123920e34b1d35f82f` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/utils/cryptography/signers/SignerECDSA.sol | 1880 | `79348d2204c34623df89352128f66e0cada694cb9c0e2637670810692d395955` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/utils/cryptography/signers/SignerERC7702.sol | 858 | `0b51b0a3f797fd55a9f1815a669d097bf4d728354c5342a83fc936b570c117cb` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/utils/cryptography/signers/SignerERC7913.sol | 2155 | `de875f910e523a88cbb3f0851f6b1b958de52b52ae262cd74efc9d9923448b94` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/utils/cryptography/signers/SignerP256.sol | 2147 | `680777935eacce18916de879ce37d8c7592b35ada18ff701d94a0945589a3a74` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/utils/cryptography/signers/SignerRSA.sol | 2340 | `35d55e0adc031d49ac802949cf933f6cbef8e9a43ebb6770a49a3d96656ae4b5` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/utils/cryptography/signers/draft-ERC7739.sol | 4337 | `67bbe0cea35bf61fa4d567af0bace9c0930b516379e65fdb36235969b5a4d88b` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/utils/cryptography/verifiers/ERC7913P256Verifier.sol | 1124 | `e65abb03ddb8062b534a09da74bef0765d47acdc25b8f390e3e7b12bf00cdf10` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/utils/cryptography/verifiers/ERC7913RSAVerifier.sol | 876 | `924f6e04a2e03c62ae9667b604d32ac382c1aa512b1619183af670541c319aad` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/utils/introspection/ERC165.sol | 879 | `61a2b12c96857aaa35f48aeda67a4281637a42494c0b3795be0ae976aa7b3793` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/utils/introspection/ERC165Checker.sol | 5054 | `4a258c80eb26f4e93b0d80e470ea690d485cf4c0bb35300a693eea25182d9b15` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/utils/introspection/IERC165.sol | 871 | `9055c2994b37dea1a41b7b7926dcb510f05dbe2540b0aafc5fbee9558fffd0ca` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/utils/math/Math.sol | 32145 | `92fee281fd46a1b058b190cf21d6b1a528f0433a907850ae1c9bcf36c5c0cd98` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/utils/math/SafeCast.sol | 34943 | `9769274bf53f26a7c7896c526ea1980dc9bea5bf5c2a5fd04870008c4afc1de9` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/utils/math/SignedMath.sol | 2613 | `1ed50b1056af886752f0fb48a0165d381e69bb4a4b18b893b066dc144a7e08d7` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/utils/structs/BitMaps.sol | 2020 | `12d7dd76e44e30d2d076df04f970a272969f30c2a2d240a89b6e2cac3f3e7c55` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/utils/structs/Checkpoints.sol | 21428 | `d908ee19a12ef183693ba9635c4bd5ec902614c493fb7967898de286218e42f7` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/utils/structs/CircularBuffer.sol | 5133 | `a1c6fdc6edc9a0e468f226c1365b6437d73eaedeb987d71d9ea386ab4299a7ba` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/utils/structs/DoubleEndedQueue.sol | 5689 | `463c51e14acbb0b9afef3f1f6903203cce5798fb168742ccd7e049e0397b2184` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/utils/structs/EnumerableMap.sol | 49145 | `90bdfbadfbb806a36dbc2facad96c850beb857f39ad5f48830244c48e7a735b6` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/utils/structs/EnumerableSet.sol | 29625 | `53507e71995d0e76d29d6dd897d0bcc3f069fd81f03cb431d7342bdfcc0d5345` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/utils/structs/Heap.sol | 10301 | `d9b945b169c77dd7d941a82e191edb709a31c0fb09e70252c32ec692b3d9c223` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/utils/structs/MerkleTree.sol | 12091 | `93a746720b7de637066af1abe005ab1dcd340912d7c855199702ee76fa11bbe4` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/utils/types/Time.sol | 5156 | `79534431c3934b23eafab9d02bda493cfc2ae383ba117a7c9698750c2e4845f1` | 0 |
| contracts/lib/openzeppelin-contracts/contracts/vendor/compound/ICompoundTimelock.sol | 2357 | `b1062b283d59aea38dbecafabe94dedb7152b89ae001f85b35f86b3817929c4c` | 0 |
| contracts/lib/openzeppelin-contracts/docs/config.js | 748 | `d5cdaf3c2d7b2724173f9664210cfae1aa4a700bf2a1f6a7b7820b74b04c15e7` | 0 |
| contracts/lib/openzeppelin-contracts/docs/templates/helpers.js | 1423 | `c54072a039eb8e30ebdfc050e2366c4fd2d33aaef32693e000b355c28899fa13` | 0 |
| contracts/lib/openzeppelin-contracts/docs/templates/properties.js | 2851 | `95274a10cfda2d35697e8ca57197757e9aa37e060db601bd8e1343be64eb8dd6` | 0 |
| contracts/lib/openzeppelin-contracts/eslint.config.mjs | 636 | `4df149bf8e150d940a7a487ea567cba6d827796250772a2a073b9597cffb0791` | 0 |
| contracts/lib/openzeppelin-contracts/hardhat.config.js | 3096 | `8e20b857a5f31aec1a213da42282f3fe0e3857dbf70b12a5a8cb6f87255db123` | 0 |
| contracts/lib/openzeppelin-contracts/hardhat/async-test-sanity.js | 412 | `28d0b89767699dbf2d08c248727ba1ba99aed4ab723adeabdfb7da58b9680413` | 0 |
| contracts/lib/openzeppelin-contracts/hardhat/common-contracts.js | 2990 | `762655bfdad5aa237ca4617c4eb64d51d75a185b69df4c0e5171cba063cf9bde` | 0 |
| contracts/lib/openzeppelin-contracts/hardhat/env-artifacts.js | 1019 | `53209232db89939f0f8e047febfe15adfd52580c65594443e395423c7421f671` | 0 |
| contracts/lib/openzeppelin-contracts/hardhat/ignore-unreachable-warnings.js | 2015 | `7d2b29651a623d2694aa22e8c185a9aae6a25c44023beb131bcb303de5033b75` | 0 |
| contracts/lib/openzeppelin-contracts/hardhat/remappings.js | 508 | `8c937c074523720f867389503a24c6f1b24b729712995842fbb8fccf1c3fdb36` | 0 |
| contracts/lib/openzeppelin-contracts/hardhat/skip-foundry-tests.js | 295 | `5e594373be07d38818abb95c62e159435c68e291aa230e7d95fc2e38f00cb8ea` | 0 |
| contracts/lib/openzeppelin-contracts/hardhat/task-test-get-files.js | 1008 | `9851350b493983460df169f1c5dedac9c36930ee5bdbddaf977fb5fa75925a86` | 0 |
| contracts/lib/openzeppelin-contracts/lib/halmos-cheatcodes/src/SVM.sol | 2788 | `db2c73220b9f83d170e7c0ef085da11b5109a90441bb27326496d8f897b02a51` | 0 |
| contracts/lib/openzeppelin-contracts/lib/halmos-cheatcodes/src/SymTest.sol | 357 | `c5391a942e6ca4a31e1b48668ba80d12e5bc552453470fa153541ea322f8a88d` | 0 |
| contracts/lib/openzeppelin-contracts/package-lock.json | 377238 | `129093d95e30e0242d685b74b08b4d3789f1c2104758ed8eb53c635ccd23e106` | 0 |
| contracts/lib/openzeppelin-contracts/package.json | 3839 | `9623b9e2f7fec73a3b6b30fd1d843b17338be5107750e735a3dec375337af7ef` | 0 |
| contracts/lib/openzeppelin-contracts/scripts/checks/compare-layout.js | 662 | `9db6f11c491c88e94eb7ca6700f50bfca1b6cd0ac5e1842ee797f89bff001140` | 0 |
| contracts/lib/openzeppelin-contracts/scripts/checks/compareGasReports.js | 7020 | `d6023ec6f9b7ca10b8fd11c515fe945523d611295ce9b56b9282ca45c2c77401` | 0 |
| contracts/lib/openzeppelin-contracts/scripts/checks/extract-layout.js | 1122 | `2c94e7b5cb32f542c6e4a7dd137a0d567114fa604d447d800013bed1b680ccb0` | 0 |
| contracts/lib/openzeppelin-contracts/scripts/checks/inheritance-ordering.js | 2002 | `85382c6cab943e24e5f17c7d883746204095e0073f719950bb78fff88d29ff82` | 0 |
| contracts/lib/openzeppelin-contracts/scripts/checks/pragma-consistency.js | 1883 | `e8c0f2fccfa56207d2846e7149a92ef63f334dd4d6dc22b587f8126367d0621c` | 0 |
| contracts/lib/openzeppelin-contracts/scripts/fetch-common-contracts.js | 2048 | `2314e4bdabe3c33882c99f58323eb6e020674875c94c1b0daf7cb4ea898a0357` | 0 |
| contracts/lib/openzeppelin-contracts/scripts/gen-nav.js | 1887 | `4230cfea9176a02373e09d7f0b560756edfd1f8ff3e1d30921efb22520100c6d` | 0 |
| contracts/lib/openzeppelin-contracts/scripts/generate/format-lines.js | 422 | `de8e8ae2542d2db777ff3441efdd1b3f549c5ba473f1071180451c5e25575c12` | 0 |
| contracts/lib/openzeppelin-contracts/scripts/generate/helpers/sanitize.js | 190 | `aa9db8aae572c1076e7d081114673a8fa56e8e228ff2f5e43d9454421e0686bb` | 0 |
| contracts/lib/openzeppelin-contracts/scripts/generate/run.js | 2311 | `e746932be10a8bce1844601ab3cb2aa4fc8d02d1f89079bcbaa9d2e3b579a430` | 0 |
| contracts/lib/openzeppelin-contracts/scripts/generate/templates/Arrays.js | 12531 | `47c29ad1985e8bab85f79f44837f298b80ca4875d8833123a67d89d7dd1cc097` | 0 |
| contracts/lib/openzeppelin-contracts/scripts/generate/templates/Arrays.opts.js | 257 | `e462c6b4ad6c8bd988c50314ca276552ce4a571ba1436ac3163af0649e86c618` | 0 |
| contracts/lib/openzeppelin-contracts/scripts/generate/templates/Checkpoints.js | 8340 | `288860f716d40a129b72a751b5c09993b40f9a0eac89165daa64888f356708ad` | 0 |
| contracts/lib/openzeppelin-contracts/scripts/generate/templates/Checkpoints.opts.js | 411 | `47ac1d11a3e082049539e930b28e179cb665ce2c04e64bb434a606a591accaba` | 0 |
| contracts/lib/openzeppelin-contracts/scripts/generate/templates/Checkpoints.t.js | 4505 | `9fbcfcfd9e57555b08e31efa26f902bcb009cb0f5e630296bd9647d4b430ab73` | 0 |
| contracts/lib/openzeppelin-contracts/scripts/generate/templates/Enumerable.opts.js | 1465 | `d3e36cd8f6e76ac0b16bdb1e9930e52fb20cf05f779b54da327c7683f36f72bf` | 0 |
| contracts/lib/openzeppelin-contracts/scripts/generate/templates/EnumerableMap.js | 15924 | `0e2b31077bca03ae8f8a21db4c7b1c7a97e53c651ac3fe64ee41df1f3308a82c` | 0 |
| contracts/lib/openzeppelin-contracts/scripts/generate/templates/EnumerableSet.js | 16051 | `ff8b239ab8bc6b6f510fed09b630cd4c5d77a1b027f7e1d7e765260bd26a5793` | 0 |
| contracts/lib/openzeppelin-contracts/scripts/generate/templates/MerkleProof.js | 7945 | `946bcad21a446465bb1626227d6b47ab08d51bc87fbdf8608fab69841a8b4f84` | 0 |
| contracts/lib/openzeppelin-contracts/scripts/generate/templates/MerkleProof.opts.js | 307 | `b2dd437a8f00e7a973cceaf3d0faaa81f68c6a5e44cc9a48c6a9335c7b374de9` | 0 |
| contracts/lib/openzeppelin-contracts/scripts/generate/templates/Packing.js | 2746 | `8fc4918bb789bf933638263c872ce22fc9f68ce6ae4c36d9d1f398b56a3faa54` | 0 |
| contracts/lib/openzeppelin-contracts/scripts/generate/templates/Packing.opts.js | 80 | `97fc03e27e76666c1a564b07855bcf88924f65a7390ad27104ccd040193a7163` | 0 |
| contracts/lib/openzeppelin-contracts/scripts/generate/templates/Packing.t.js | 1611 | `77a0937ce37a119f2aaa8ff50b6ebb54862220e85563549ab09198b6ec1426b5` | 0 |
| contracts/lib/openzeppelin-contracts/scripts/generate/templates/SafeCast.js | 3770 | `463e6a7cb3ab55f541fb3d4312343d558c2695fb5240d36ce3d3f2ca7b319946` | 0 |
| contracts/lib/openzeppelin-contracts/scripts/generate/templates/Slot.opts.js | 632 | `f566f7646afaa4a9731d38f05870539a2d2bfea84721c320aa1f4dd8a2879bfc` | 0 |
| contracts/lib/openzeppelin-contracts/scripts/generate/templates/SlotDerivation.js | 3583 | `baca46f06b85655fa97b8a176b5db314d559b291166d1ffbe7f33f63e5bf9546` | 0 |
| contracts/lib/openzeppelin-contracts/scripts/generate/templates/SlotDerivation.t.js | 3255 | `b7729e857cdae68348e875b14b64cbf71533dd7522f5c8553cee1c0ecb9f25d1` | 0 |
| contracts/lib/openzeppelin-contracts/scripts/generate/templates/StorageSlot.js | 2321 | `daf387a4f34b198c78fe70fbeee28d5921630c6243c84fef988d04e4cbd6575f` | 0 |
| contracts/lib/openzeppelin-contracts/scripts/generate/templates/StorageSlotMock.js | 1622 | `17cfce493dcaaa2e85ca1b01eea5bdc0ff8e501a4281c58073dc4852d0ebe899` | 0 |
| contracts/lib/openzeppelin-contracts/scripts/generate/templates/TransientSlot.js | 2166 | `5ed88997123a71cf2408eff1bd9ec56b05b9457d9ede375186d4dcd329ca8933` | 0 |
| contracts/lib/openzeppelin-contracts/scripts/generate/templates/TransientSlotMock.js | 804 | `5b8320fc0615731a32816a51e6ed535c72eaf8911217a69c66e85c4e49ff33e6` | 0 |
| contracts/lib/openzeppelin-contracts/scripts/generate/templates/conversion.js | 678 | `134a41ead4e00cff47ef7d0f99b68dea2e730f5a8cc02dbca22f7603fb5b10f8` | 0 |
| contracts/lib/openzeppelin-contracts/scripts/helpers.js | 155 | `58660f4bfe243e8720a6001ae4380d4329b2891b973bccc19a53d831c9535808` | 0 |
| contracts/lib/openzeppelin-contracts/scripts/release/format-changelog.js | 1226 | `faff569d912d2a9823b70cb8476a5f8d276bfdb71fe97c5553db468aa6628f9d` | 0 |
| contracts/lib/openzeppelin-contracts/scripts/release/synchronize-versions.js | 481 | `477c2b3c846a9faf36afa1a66d3ed8a7008a80aaec5a096ee7ed4d6a3ac1d54a` | 0 |
| contracts/lib/openzeppelin-contracts/scripts/release/update-comment.js | 1280 | `258bad59128bf2f39480fc719a0d8b4b5874d84a877ca00953854f66ce3ef48d` | 0 |
| contracts/lib/openzeppelin-contracts/scripts/release/workflow/github-release.js | 1660 | `4b88436e2c81e284ee0875402f21f63bb693ae3da96eac6d18d6cfdefb4217b4` | 0 |
| contracts/lib/openzeppelin-contracts/scripts/release/workflow/rerun.js | 250 | `e6463d98a64df5794190341fe03aa3123dbac1d7ac46160b95bed3daa038aa0c` | 0 |
| contracts/lib/openzeppelin-contracts/scripts/release/workflow/set-changesets-pr-title.js | 768 | `05305204f28f947b74ffa055756958d8ed7589ef5ded1b7fe711d1e463064747` | 0 |
| contracts/lib/openzeppelin-contracts/scripts/release/workflow/state.js | 3595 | `daef1ae719c801d6cd20f69326d426609b9c78707146abfb3f170c91c52750dd` | 0 |
| contracts/lib/openzeppelin-contracts/scripts/remove-ignored-artifacts.js | 1318 | `d760c8c71b7a6936b34c663402ec735f254d157830c6f2df3c1497b59b4ec806` | 0 |
| contracts/lib/openzeppelin-contracts/scripts/solhint-custom/index.js | 2652 | `ec74c407ef34fcd219172a93948f1b1dd8e68b945883f188ed478877593a65a3` | 0 |
| contracts/lib/openzeppelin-contracts/scripts/solhint-custom/package.json | 136 | `2440acd9a4aff80c411ae9e8eb96be37a45c9c3f9356a0ba8df687386986491f` | 0 |
| contracts/lib/openzeppelin-contracts/scripts/update-docs-branch.js | 2095 | `e6e0877536359831c719b0c3fecd1a5eee8be527a06207bd1e31c436720bd46e` | 0 |
| contracts/lib/openzeppelin-contracts/solhint.config.js | 695 | `4114184cd85c4d973d06e68746a2d8d7ba624cfebb28e4d26f80322dc4628f6e` | 0 |
