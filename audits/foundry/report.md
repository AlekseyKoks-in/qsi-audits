# Security & Post-Quantum Readiness Audit Report

**Project:** foundry @ 7f0a409a5c20 · Foundry (Paradigm) — public repository (passive review)
| | |
|---|---|
| Organization | QSI |
| Report date | 2026-10-28 12:26 UTC |
| Report version | 1 |
| Audit run | 0faa8d96-4d0e-46ac-8957-54843d2a3625 (Document audit) |
| Analyzer engine | qsi-engine 1.2.0 |
| Risk profile | Security software vendor |
| Content SHA-256 | `37dc71482c0ac19cdfddf6850b40a433a909c798e26a1f8725c5dfb354258319` |
| Signature key (Ed25519, SHA-256 fingerprint; the signature is the separate file report.sig.json) | `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e` |
> This report presents automated and documented analysis results for the stated scope. It is not a legal opinion, a certification or an attestation of compliance with any standard.

## 1. Executive summary

- Critical: **0**
- High: **2**
- Medium: **3**
- Low: **10**
- Info: **3**

- Confirmed technical vulnerability: 0
- Known vulnerable component: 7
- Confirmed configuration error: 0
- Potential cryptographic risk: 0
- Long-term post-quantum risk: 6
- Improvement recommendation: 4
- Insufficient data: 1

Mosca's inequality (x + y > z): x = 10, y = 3, z = 8 → migration would finish too late under this scenario. _z is a planning assumption chosen per risk profile, not a prediction. A cryptographically relevant quantum computer is not publicly known to exist today._

**Post-quantum maturity: Level 4 of 4 — post-quantum by default in the critical paths.** Next step: Keep the inventory current and review new code paths before release.

## 2. Scope and boundaries

Mode: Document audit

Repository: <https://github.com/foundry-rs/foundry> @ `7f0a409a5c2016f16cb2e8618a750cc04e13977c` — evidence links open the lines at this commit.

761 files, 13820446 bytes in total, 17 redaction(s); the per-file SHA-256 list is in appendix C.

## 3. Methodology

| Area | Status | Count | Examples |
|---|---|---|---|
| source_code | checked | 705 | .github/scripts/benchmark_clickhouse.py: 477 lines scanned with 16 rule patterns and 122 registry patterns; .github/scripts/compare-benchmark-thresholds.py: 141 lines scanned with 16 rule patterns and 122 registry patterns; .github/scripts/finalize-release.py: 313 lines scanned with 16 rule patterns and 122 registry patterns |
| smart_contracts | checked | 14 | .github/scripts/contracts/BatchCounter.sol: built-in Solidity pattern checks; .github/scripts/contracts/CounterWithRequire.sol: built-in Solidity pattern checks; .github/scripts/contracts/DeployAndCall.s.sol: built-in Solidity pattern checks |
| slither | not checked | 14 | slither is not installed on the server (pip install slither-analyzer + solc) |
| dependencies | checked | 41 | Cargo.lock: 1180 dependencies parsed (1180 pinned); Cargo.toml: 156 dependencies parsed (7 pinned); crates/anvil/Cargo.toml: 81 dependencies parsed (0 pinned) |
| secrets | checked | 8 | crates/cast/src/cmd/keychain.rs: 1 redacted value(s) not reported (comments, test modules, fixture declarations, placeholders, values the source annotates as published, or hex values not bound to a secret name); crates/cheatcodes/src/toml.rs: 3 redacted value(s) not reported (comments, test modules, fixture declarations, placeholders, values the source annotates as published, or hex values not bound to a secret name); crates/common/fmt/src/ui.rs: 8 redacted value(s) not reported (comments, test modules, fixture declarations, placeholders, values the source annotates as published, or hex values not bound to a secret name) |
| tls_code | checked | 1 | crates/cli/src/utils/mod.rs: TLS key-exchange settings read |
| osv_advisories | checked | 1 | 1000 pinned packages queried at OSV.dev; 8 affected |

_Long lists are grouped here; the full per-file list is in the JSON report, signed with the same key._

## 4. Assets examined and not examined

- slither — not checked: slither is not installed on the server (pip install slither-analyzer + solc)
- slither — not checked: slither is not installed on the server (pip install slither-analyzer + solc)
- slither — not checked: slither is not installed on the server (pip install slither-analyzer + solc)
- slither — not checked: slither is not installed on the server (pip install slither-analyzer + solc)
- slither — not checked: slither is not installed on the server (pip install slither-analyzer + solc)
- slither — not checked: slither is not installed on the server (pip install slither-analyzer + solc)
- slither — not checked: slither is not installed on the server (pip install slither-analyzer + solc)
- slither — not checked: slither is not installed on the server (pip install slither-analyzer + solc)
- slither — not checked: slither is not installed on the server (pip install slither-analyzer + solc)
- slither — not checked: slither is not installed on the server (pip install slither-analyzer + solc)
- slither — not checked: slither is not installed on the server (pip install slither-analyzer + solc)
- slither — not checked: slither is not installed on the server (pip install slither-analyzer + solc)
- slither — not checked: slither is not installed on the server (pip install slither-analyzer + solc)
- slither — not checked: slither is not installed on the server (pip install slither-analyzer + solc)

## 5. Architecture overview

Static review of the source tree foundry at 7f0a409a5c2016f16cb2e8618a750cc04e13977c. 761 files analysed; of 2104 files, 1113 are test, fuzzing, benchmark or example code and were left out, 230 are not read by any analyzer, 0 exceed the per-file limit and 0 did not fit the total limit. No requests were sent to the owner's systems.

## 6. Overall security posture

- Indicative posture index: **63** / 100 — _Derived from findings in scope (confirmed and potential issues weighted by severity). Indicative only; not comparable across differently scoped audits._
- Quantum-vulnerable share of inventory: 16.0%

## 7. Detailed findings

### QSI-2026-04469 — quick-xml 0.39.4 is affected by RUSTSEC-2026-0194

- Severity: **High** · Classification: Known vulnerable component · Confidence: Low
- Affected asset: `dependency:crates.io/quick-xml@0.39.4`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 12:26 UTC
- Priority score: 37.7 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev reports RUSTSEC-2026-0194 for crates.io package quick-xml at version 0.39.4: Quadratic run time when checking a start tag for duplicate attribute names. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0194
```

**Evidence.**

_tool_output · [OSV.dev RUSTSEC-2026-0194](https://osv.dev/vulnerability/RUSTSEC-2026-0194) · manifest · SHA-256 028cd2f8044c5c52031532eb91141d581476948b4fd115c63b565c4f52398450_

```
{"id": "RUSTSEC-2026-0194", "aliases": [], "modified": "2026-07-02T08:00:03.849273679Z", "summary": "Quadratic run time when checking a start tag for duplicate attribute names", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (0.41.0).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-04470 — quick-xml 0.39.4 is affected by RUSTSEC-2026-0195

- Severity: **High** · Classification: Known vulnerable component · Confidence: Low
- Affected asset: `dependency:crates.io/quick-xml@0.39.4`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 12:26 UTC
- Priority score: 37.7 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev reports RUSTSEC-2026-0195 for crates.io package quick-xml at version 0.39.4: Unbounded namespace-declaration allocation in `NsReader` enables memory-exhaustion denial of service. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0195
```

**Evidence.**

_tool_output · [OSV.dev RUSTSEC-2026-0195](https://osv.dev/vulnerability/RUSTSEC-2026-0195) · manifest · SHA-256 7934c935f3154b61c623e871c948769f40fd83ae102d44328fbedb576471f986_

```
{"id": "RUSTSEC-2026-0195", "aliases": [], "modified": "2026-07-02T09:00:04.037478193Z", "summary": "Unbounded namespace-declaration allocation in `NsReader` enables memory-exhaustion denial of service", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (0.41.0).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-04456 — TLS without a post-quantum key exchange: rustls with the ring crypto provider

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `tls-code:rustls`
- Data source: crates/cli/src/utils/mod.rs
- Detection method: Static reading of TLS library configuration in code and manifests: crypto provider, group and curve lists, GODEBUG.
- Analyzer: tls_code 1.2.0 · 2026-10-28 12:26 UTC
- Priority score: 38.1 / 100
- CVSS v3.1: not applicable

rustls with the ring crypto provider at crates/cli/src/utils/mod.rs:260: the configured key exchange (ring) has no hybrid ML-KEM group such as X25519MLKEM768 (RFC 10024), so the handshake cannot negotiate one.

**Potential impact.** Traffic protected only by classical ECDHE could be recorded today and decrypted once a CRQC exists (harvest now, decrypt later). Relevant when transmitted data must stay confidential for many years.

**Reproduction steps.**

```
Open crates/cli/src/utils/mod.rs:260 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [crates/cli/src/utils/mod.rs](https://github.com/foundry-rs/foundry/blob/7f0a409a5c2016f16cb2e8618a750cc04e13977c/crates/cli/src/utils/mod.rs#L260) · line 260 · SHA-256 0084c5a919bee6778c8436c47d41f06240827ab128eb7ef31339267091e759cf_

```
  259 |     // https://github.com/snapview/tokio-tungstenite/issues/353
  260 |     rustls::crypto::ring::default_provider()
  261 |         .install_default()
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Read from code and manifests only: the library versions deployed and settings made outside the code (environment, launch flags) were not determined.

**Recommendation.** Build rustls with the aws-lc-rs provider (rustls::crypto::aws_lc_rs) and the prefer-post-quantum feature, which puts X25519MLKEM768 first.

**Retest procedure.** Connect with a client that offers X25519MLKEM768 (openssl s_client -groups X25519MLKEM768 with OpenSSL 3.5+, or a Go 1.24+ client) and confirm the negotiated group.

### QSI-2026-04462 — block-buffer 0.9.0 is affected by GHSA-qwgh-2vcv-g2f7

- Severity: **Medium** · Classification: Known vulnerable component · Confidence: Low
- Affected asset: `dependency:crates.io/block-buffer@0.9.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 12:26 UTC
- Priority score: 33.2 / 100
- CVSS v3.1: not applicable

OSV.dev reports GHSA-qwgh-2vcv-g2f7 for crates.io package block-buffer at version 0.9.0: block_buffer: panic corrupts inline buffer position. The advisory names no affected functions, so reachability was not determined.

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

### QSI-2026-04463 — block-buffer 0.10.4 is affected by GHSA-qwgh-2vcv-g2f7

- Severity: **Medium** · Classification: Known vulnerable component · Confidence: Low
- Affected asset: `dependency:crates.io/block-buffer@0.10.4`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 12:26 UTC
- Priority score: 33.2 / 100
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

### QSI-2026-04453 — Floating pragma (^0.8.13) in 12 file(s)

- Severity: **Low** · Classification: Improvement recommendation · Confidence: High
- Affected asset: `solidity:pragma:^0.8.13`
- Data source: .github/scripts/contracts/BatchCounter.sol
- Detection method: Solidity source pattern analysis.
- Analyzer: solidity 1.2.0 · 2026-10-28 12:26 UTC
- Priority score: 33.5 / 100
- CVSS v3.1: not applicable

pragma ^0.8.13 in 12 file(s), first at .github/scripts/contracts/BatchCounter.sol:2. (related: SWC-103)

**Potential impact.** Contracts may be deployed with untested compiler versions. The compiler actually used is set by the build configuration, which this check does not read.

**Reproduction steps.**

```
Open .github/scripts/contracts/BatchCounter.sol:2 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · .github/scripts/contracts/BatchCounter.sol · line 2 · SHA-256 7c3708d9069ee80391b81af25f28478d8257cfe3f51a51b01be9827555524d9a_

```
    1 | // SPDX-License-Identifier: UNLICENSED
    2 | pragma solidity ^0.8.13;
    3 | 
    4 | contract BatchCounter {
```

_file_excerpt · .github/scripts/contracts/CounterWithRequire.sol · line 2 · SHA-256 5ba651f9d9a85f874646356b2e4882d9492ccd2c37892a189cd79790bf2fec59_

```
    1 | // SPDX-License-Identifier: UNLICENSED
    2 | pragma solidity ^0.8.13;
    3 | 
    4 | contract Counter {
```

_file_excerpt · .github/scripts/contracts/DeployAndCall.s.sol · line 2 · SHA-256 e480e29012507cfc6f4594f7a4fd4ab65d0adce3b3bb9b2323614637a52e2c3f_

```
    1 | // SPDX-License-Identifier: UNLICENSED
    2 | pragma solidity ^0.8.13;
    3 | 
    4 | import {Script, console} from "forge-std/Script.sol";
```

_file_excerpt · [crates/forge/assets/solidity/CounterTemplate.s.sol](https://github.com/foundry-rs/foundry/blob/7f0a409a5c2016f16cb2e8618a750cc04e13977c/crates/forge/assets/solidity/CounterTemplate.s.sol#L2) · line 2 · SHA-256 7da697e70396e1794f5ccb8835bcc5b58068f231c41d272719e977b7d8331437_

```
    1 | // SPDX-License-Identifier: UNLICENSED
    2 | pragma solidity ^0.8.13;
    3 | 
    4 | import {Script} from "forge-std/Script.sol";
```

_file_excerpt · [crates/forge/assets/solidity/CounterTemplate.sol](https://github.com/foundry-rs/foundry/blob/7f0a409a5c2016f16cb2e8618a750cc04e13977c/crates/forge/assets/solidity/CounterTemplate.sol#L2) · line 2 · SHA-256 5ba651f9d9a85f874646356b2e4882d9492ccd2c37892a189cd79790bf2fec59_

```
    1 | // SPDX-License-Identifier: UNLICENSED
    2 | pragma solidity ^0.8.13;
    3 | 
    4 | contract Counter {
```

_file_excerpt · [crates/forge/assets/solidity/CounterTemplate.t.sol](https://github.com/foundry-rs/foundry/blob/7f0a409a5c2016f16cb2e8618a750cc04e13977c/crates/forge/assets/solidity/CounterTemplate.t.sol#L2) · line 2 · SHA-256 b7d9e25cb26900b8a13c01b38782749ef0421704305f08208da38ed8f1de800a_

```
    1 | // SPDX-License-Identifier: UNLICENSED
    2 | pragma solidity ^0.8.13;
    3 | 
    4 | import {Test} from "forge-std/Test.sol";
```

_file_excerpt · [crates/forge/assets/tempo/MailTemplate.s.sol](https://github.com/foundry-rs/foundry/blob/7f0a409a5c2016f16cb2e8618a750cc04e13977c/crates/forge/assets/tempo/MailTemplate.s.sol#L2) · line 2 · SHA-256 7da697e70396e1794f5ccb8835bcc5b58068f231c41d272719e977b7d8331437_

```
    1 | // SPDX-License-Identifier: UNLICENSED
    2 | pragma solidity ^0.8.13;
    3 | 
    4 | import {Script} from "forge-std/Script.sol";
```

_file_excerpt · [crates/forge/assets/tempo/MailTemplate.sol](https://github.com/foundry-rs/foundry/blob/7f0a409a5c2016f16cb2e8618a750cc04e13977c/crates/forge/assets/tempo/MailTemplate.sol#L2) · line 2 · SHA-256 255e8e20fe021924c3a1bb809df0f9e26f8b4ba0d7d3d1c43464a6ec82136b54_

```
    1 | // SPDX-License-Identifier: UNLICENSED
    2 | pragma solidity ^0.8.13;
    3 | 
    4 | import {ITIP20} from "tempo-std/interfaces/ITIP20.sol";
```

_file_excerpt · [crates/forge/assets/tempo/MailTemplate.t.sol](https://github.com/foundry-rs/foundry/blob/7f0a409a5c2016f16cb2e8618a750cc04e13977c/crates/forge/assets/tempo/MailTemplate.t.sol#L2) · line 2 · SHA-256 b7d9e25cb26900b8a13c01b38782749ef0421704305f08208da38ed8f1de800a_

```
    1 | // SPDX-License-Identifier: UNLICENSED
    2 | pragma solidity ^0.8.13;
    3 | 
    4 | import {Test} from "forge-std/Test.sol";
```

_file_excerpt · [crates/forge/assets/vyper/CounterTemplate.s.sol](https://github.com/foundry-rs/foundry/blob/7f0a409a5c2016f16cb2e8618a750cc04e13977c/crates/forge/assets/vyper/CounterTemplate.s.sol#L2) · line 2 · SHA-256 7da697e70396e1794f5ccb8835bcc5b58068f231c41d272719e977b7d8331437_

```
    1 | // SPDX-License-Identifier: UNLICENSED
    2 | pragma solidity ^0.8.13;
    3 | 
    4 | import {Script} from "forge-std/Script.sol";
```

**Limitations of the check.** Lightweight static pattern analysis of Solidity source without compilation or symbolic execution. It does not replace a full smart-contract audit; confirm manually or with dedicated tools (Slither, Foundry tests).

**Recommendation.** Pin the compiler version used in testing.

**Retest procedure.** Re-run static analysis and add a unit/fuzz test that exercises the pattern.

### QSI-2026-04460 — Floating pragma (>=0.8.13 <0.9.0) in 2 file(s)

- Severity: **Low** · Classification: Improvement recommendation · Confidence: High
- Affected asset: `solidity:pragma:>=0.8.13 <0.9.0`
- Data source: crates/evm/traces/src/decoder/monad/IMonadStaking.sol
- Detection method: Solidity source pattern analysis.
- Analyzer: solidity 1.2.0 · 2026-10-28 12:26 UTC
- Priority score: 33.5 / 100
- CVSS v3.1: not applicable

pragma >=0.8.13 <0.9.0 in 2 file(s), first at crates/evm/traces/src/decoder/monad/IMonadStaking.sol:2. (related: SWC-103)

**Potential impact.** Contracts may be deployed with untested compiler versions. The compiler actually used is set by the build configuration, which this check does not read.

**Reproduction steps.**

```
Open crates/evm/traces/src/decoder/monad/IMonadStaking.sol:2 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [crates/evm/traces/src/decoder/monad/IMonadStaking.sol](https://github.com/foundry-rs/foundry/blob/7f0a409a5c2016f16cb2e8618a750cc04e13977c/crates/evm/traces/src/decoder/monad/IMonadStaking.sol#L2) · line 2 · SHA-256 0966fab580a62d690b1abff6275e91d132627c82ac011aa8596cc8723b757f4f_

```
    1 | // SPDX-License-Identifier: MIT
    2 | pragma solidity >=0.8.13 <0.9.0;
    3 | 
    4 | // Mirrors category-labs/monad-std/src/interfaces/IMonadStaking.sol for trace decoding.
```

_file_excerpt · [crates/evm/traces/src/decoder/monad/IReserveBalance.sol](https://github.com/foundry-rs/foundry/blob/7f0a409a5c2016f16cb2e8618a750cc04e13977c/crates/evm/traces/src/decoder/monad/IReserveBalance.sol#L2) · line 2 · SHA-256 c6df50db795a18ca9b1093b55e2b9d19cda0e05d8bc4e6d47c5566653ea65fc4_

```
    1 | // SPDX-License-Identifier: MIT
    2 | pragma solidity >=0.8.13 <0.9.0;
    3 | 
    4 | // Mirrors category-labs/monad-std/src/interfaces/IReserveBalance.sol for trace decoding.
```

**Limitations of the check.** Lightweight static pattern analysis of Solidity source without compilation or symbolic execution. It does not replace a full smart-contract audit; confirm manually or with dedicated tools (Slither, Foundry tests).

**Recommendation.** Pin the compiler version used in testing.

**Retest procedure.** Re-run static analysis and add a unit/fuzz test that exercises the pattern.

### QSI-2026-04454 — Quantum-vulnerable ECDSA: transaction and message signing (9 file(s))

- Severity: **Low** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:ECDSA:transaction_signing`
- Data source: crates/anvil/src/eth/backend/cheats.rs
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.2.0 · 2026-10-28 12:26 UTC
- Priority score: 29.7 / 100
- CVSS v3.1: not applicable

13 reference(s) to ECDSA across 9 file(s), e.g. crates/anvil/src/eth/backend/cheats.rs:11. Role, judged from paths, function names and nearby code: transaction and message signing. A CRQC derives the private key from a public key that is already known (on chain after the first spend, in reused addresses): funds and approvals controlled by these keys need a migration path.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open crates/anvil/src/eth/backend/cheats.rs:11 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [crates/anvil/src/eth/backend/cheats.rs](https://github.com/foundry-rs/foundry/blob/7f0a409a5c2016f16cb2e8618a750cc04e13977c/crates/anvil/src/eth/backend/cheats.rs#L11) · line 11 · SHA-256 e08fa6015cef9b6d59779c9f3e7c25ea0e325b4424289d7c3b847ae6965911a8_

```
   10 |     PrecompileHalt, PrecompileId, PrecompileOutput, PrecompileResult, call_eth_precompile,
   11 |     secp256k1::ec_recover_run, utilities::right_pad,
   12 | };
```

_file_excerpt · [crates/anvil/src/eth/backend/tempo.rs](https://github.com/foundry-rs/foundry/blob/7f0a409a5c2016f16cb2e8618a750cc04e13977c/crates/anvil/src/eth/backend/tempo.rs#L271) · line 271 · SHA-256 52f153efb18e17109443cc34089b5a89d1a1b4c83b8f5e68fba410ec9d1fcb2a_

```
  270 |                 account, // msg_sender (root account authorizes its own key)
  271 |                 account, // key ID = account address for secp256k1
  272 |                 SignatureType::Secp256k1,
```

_file_excerpt · [crates/cast/src/cmd/keychain.rs](https://github.com/foundry-rs/foundry/blob/7f0a409a5c2016f16cb2e8618a750cc04e13977c/crates/cast/src/cmd/keychain.rs#L153) · line 153 · SHA-256 5d58b11e699bbe1d28e4a75b890106a088de2218bba25f8fb944230db03ba773_

```
  152 |         /// Signature type: secp256k1, p256, or webauthn.
  153 |         #[arg(default_value = "secp256k1", value_parser = parse_signature_type)]
  154 |         key_type: SignatureType,
```

_file_excerpt · [crates/cast/src/cmd/keychain.rs](https://github.com/foundry-rs/foundry/blob/7f0a409a5c2016f16cb2e8618a750cc04e13977c/crates/cast/src/cmd/keychain.rs#L462) · line 462 · SHA-256 b07c462df7c1e73749099155ee6aaeaa1569cdd4568e13a1e1317ebef0fcc659_

```
  461 |     /// The root signature type is determined by the configured signer.
  462 |     #[arg(long, default_value = "secp256k1", value_parser = parse_auth_signature_type)]
  463 |     key_type: AuthSignatureType,
```

_file_excerpt · [crates/cast/src/cmd/keychain.rs](https://github.com/foundry-rs/foundry/blob/7f0a409a5c2016f16cb2e8618a750cc04e13977c/crates/cast/src/cmd/keychain.rs#L578) · line 578 · SHA-256 4a236801a5d76ecf75ecddf66d49cbadc28fe918e5218ae8bcbf2b0ab0c9523f_

```
  577 |     match s.to_lowercase().as_str() {
  578 |         "secp256k1" => Ok(AuthSignatureType::Secp256k1),
  579 |         "p256" => Ok(AuthSignatureType::P256),
```

_file_excerpt · [crates/cast/src/cmd/tempo/zone/mod.rs](https://github.com/foundry-rs/foundry/blob/7f0a409a5c2016f16cb2e8618a750cc04e13977c/crates/cast/src/cmd/tempo/zone/mod.rs#L221) · line 221 · SHA-256 46a53d505e0d3369700709c58dabf91c816e81e59906959d5af8ac3fc7670469_

```
  220 |                     && k256::PublicKey::from_sec1_bytes(&self.reveal_to).is_ok(),
  221 |                 "--reveal-to must be a compressed secp256k1 public key"
  222 |             );
```

_file_excerpt · [crates/cheatcodes/src/error.rs](https://github.com/foundry-rs/foundry/blob/7f0a409a5c2016f16cb2e8618a750cc04e13977c/crates/cheatcodes/src/error.rs#L10) · line 10 · SHA-256 3c595041c68eace648d774f0f69f05dd96ce13575114ecabcc71e2b3e835359a_

```
    9 | use foundry_wallets::error::WalletSignerError;
   10 | use k256::ecdsa::signature::Error as SignatureError;
   11 | use revm::context_interface::result::EVMError;
```

_file_excerpt · [crates/common/src/tempo/session.rs](https://github.com/foundry-rs/foundry/blob/7f0a409a5c2016f16cb2e8618a750cc04e13977c/crates/common/src/tempo/session.rs#L321) · line 321 · SHA-256 de4949f2f75dc96d7fa04e685806f1689470b0efacc7d096b13a61c80c782761_

```
  320 |         .ok_or_else(|| eyre::eyre!("managed access key has no local signing material"))?;
  321 |     ensure!(key.key_type == KeyType::Secp256k1, "only secp256k1 managed access keys are supported");
  322 |     let signer = foundry_wallets::utils::create_local_signer(&key.key)?;
```

_file_excerpt · [crates/evm/networks/src/lib.rs](https://github.com/foundry-rs/foundry/blob/7f0a409a5c2016f16cb2e8618a750cc04e13977c/crates/evm/networks/src/lib.rs#L29) · line 29 · SHA-256 c1eed0230f405adbff40033b2879b8000d521e302866b4850d9ad7705f2634a4_

```
   28 |     Precompile as RevmPrecompile,
   29 |     secp256r1::{P256VERIFY, P256VERIFY_OSAKA},
   30 | };
```

_file_excerpt · [crates/evm/symbolic/src/lib.rs](https://github.com/foundry-rs/foundry/blob/7f0a409a5c2016f16cb2e8618a750cc04e13977c/crates/evm/symbolic/src/lib.rs#L28) · line 28 · SHA-256 8a680edc9e74629b043692fee273270f039ea08b7aea8752cfa55e855b9a4100_

```
   27 |         database::DatabaseRef,
   28 |         precompile::{blake2, bn254, hash, identity, kzg_point_evaluation, modexp, secp256k1},
   29 |         primitives::hardfork::SpecId,
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains adopt them.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-04459 — Quantum-vulnerable BLS12-381: transaction and message signing (3 file(s))

- Severity: **Low** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:BLS12-381:transaction_signing`
- Data source: crates/evm/core/src/precompiles.rs
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.2.0 · 2026-10-28 12:26 UTC
- Priority score: 29.7 / 100
- CVSS v3.1: not applicable

39 reference(s) to BLS12-381 across 3 file(s), e.g. crates/evm/core/src/precompiles.rs:34. Role, judged from paths, function names and nearby code: transaction and message signing. A CRQC derives the private key from a public key that is already known (on chain after the first spend, in reused addresses): funds and approvals controlled by these keys need a migration path.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open crates/evm/core/src/precompiles.rs:34 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [crates/evm/core/src/precompiles.rs](https://github.com/foundry-rs/foundry/blob/7f0a409a5c2016f16cb2e8618a750cc04e13977c/crates/evm/core/src/precompiles.rs#L34) · line 34 · SHA-256 e9d6760e61c5d95615b59c481b236749a952ceda871fa5873803470b529b91ee_

```
   33 | /// The BLS12-381 G1ADD precompile address.
   34 | pub const BLS12_G1ADD: Address = Address::with_last_byte(0x0b);
   35 | 
```

_file_excerpt · [crates/evm/core/src/precompiles.rs](https://github.com/foundry-rs/foundry/blob/7f0a409a5c2016f16cb2e8618a750cc04e13977c/crates/evm/core/src/precompiles.rs#L37) · line 37 · SHA-256 cc66a9c2775894a525021ffc6fe4d347f52ebe34064d82f6e4400f828c654b67_

```
   36 | /// The BLS12-381 G1MSM precompile address.
   37 | pub const BLS12_G1MSM: Address = Address::with_last_byte(0x0c);
   38 | 
```

_file_excerpt · [crates/evm/core/src/precompiles.rs](https://github.com/foundry-rs/foundry/blob/7f0a409a5c2016f16cb2e8618a750cc04e13977c/crates/evm/core/src/precompiles.rs#L40) · line 40 · SHA-256 f64918fb0a20f796360c240232d3a80a6b804fce081c3effd117316c46a55719_

```
   39 | /// The BLS12-381 G2ADD precompile address.
   40 | pub const BLS12_G2ADD: Address = Address::with_last_byte(0x0d);
   41 | 
```

_file_excerpt · [crates/evm/traces/src/decoder/mod.rs](https://github.com/foundry-rs/foundry/blob/7f0a409a5c2016f16cb2e8618a750cc04e13977c/crates/evm/traces/src/decoder/mod.rs#L28) · line 28 · SHA-256 851a2373c0ad3c5e1fd446403193f757e5c833428427e332fc9ae97a7b32bf56_

```
   27 |     precompiles::{
   28 |         BLAKE_2F, BLS12_G1ADD, BLS12_G1MSM, BLS12_G2ADD, BLS12_G2MSM, BLS12_MAP_FP_TO_G1,
   29 |         BLS12_MAP_FP2_TO_G2, BLS12_PAIRING_CHECK, CELO_TRANSFER, EC_ADD, EC_MUL, EC_PAIRING,
```

_file_excerpt · [crates/evm/traces/src/decoder/mod.rs](https://github.com/foundry-rs/foundry/blob/7f0a409a5c2016f16cb2e8618a750cc04e13977c/crates/evm/traces/src/decoder/mod.rs#L29) · line 29 · SHA-256 8f52a29c8533dabc5a48d03c5d190efe2583470180e7a803d173c4a93d64c42a_

```
   28 |         BLAKE_2F, BLS12_G1ADD, BLS12_G1MSM, BLS12_G2ADD, BLS12_G2MSM, BLS12_MAP_FP_TO_G1,
   29 |         BLS12_MAP_FP2_TO_G2, BLS12_PAIRING_CHECK, CELO_TRANSFER, EC_ADD, EC_MUL, EC_PAIRING,
   30 |         EC_RECOVER, IDENTITY, MOD_EXP, POINT_EVALUATION, RIPEMD_160, SHA_256,
```

_file_excerpt · [crates/evm/traces/src/decoder/mod.rs](https://github.com/foundry-rs/foundry/blob/7f0a409a5c2016f16cb2e8618a750cc04e13977c/crates/evm/traces/src/decoder/mod.rs#L424) · line 424 · SHA-256 2dd54823637c9ad3500d6cdd67ea43a290e670e39a2ada89aacfa0b0c28aefc6_

```
  423 |             (POINT_EVALUATION, "PointEvaluation".to_string()),
  424 |             (BLS12_G1ADD, "BLS12_G1ADD".to_string()),
  425 |             (BLS12_G1MSM, "BLS12_G1MSM".to_string()),
```

_file_excerpt · [crates/evm/traces/src/decoder/precompiles.rs](https://github.com/foundry-rs/foundry/blob/7f0a409a5c2016f16cb2e8618a750cc04e13977c/crates/evm/traces/src/decoder/precompiles.rs#L7) · line 7 · SHA-256 6a45e6e6e64988c4d23c76ecc0727fe03dd6eb0a7a8f7f864be6f51f820b5017_

```
    6 |     precompiles::{
    7 |         BLAKE_2F, BLS12_G1ADD, BLS12_G1MSM, BLS12_G2ADD, BLS12_G2MSM, BLS12_MAP_FP_TO_G1,
    8 |         BLS12_MAP_FP2_TO_G2, BLS12_PAIRING_CHECK, CELO_TRANSFER, EC_ADD, EC_MUL, EC_PAIRING,
```

_file_excerpt · [crates/evm/traces/src/decoder/precompiles.rs](https://github.com/foundry-rs/foundry/blob/7f0a409a5c2016f16cb2e8618a750cc04e13977c/crates/evm/traces/src/decoder/precompiles.rs#L8) · line 8 · SHA-256 1cbc4db457becceed23c646a85a2191cb78062453411a6177172fa8e5e173bf5_

```
    7 |         BLAKE_2F, BLS12_G1ADD, BLS12_G1MSM, BLS12_G2ADD, BLS12_G2MSM, BLS12_MAP_FP_TO_G1,
    8 |         BLS12_MAP_FP2_TO_G2, BLS12_PAIRING_CHECK, CELO_TRANSFER, EC_ADD, EC_MUL, EC_PAIRING,
    9 |         EC_RECOVER, IDENTITY, MOD_EXP, P256_VERIFY, POINT_EVALUATION, RIPEMD_160, SHA_256,
```

_file_excerpt · [crates/evm/traces/src/decoder/precompiles.rs](https://github.com/foundry-rs/foundry/blob/7f0a409a5c2016f16cb2e8618a750cc04e13977c/crates/evm/traces/src/decoder/precompiles.rs#L332) · line 332 · SHA-256 8ab37a93305db1d491ed6efe32d5e924492f9493e2c298523b61abac7d4b3b2d_

```
  331 |     fn address(&self) -> Address {
  332 |         BLS12_G1ADD
  333 |     }
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains adopt them.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-04455 — Quantum-vulnerable ECDSA: role not determined (1 file(s))

- Severity: **Low** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:ECDSA:general`
- Data source: crates/cheatcodes/src/crypto.rs
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.2.0 · 2026-10-28 12:26 UTC
- Priority score: 28.3 / 100
- CVSS v3.1: not applicable

4 reference(s) to ECDSA across 1 file(s), e.g. crates/cheatcodes/src/crypto.rs:26. Role, judged from paths, function names and nearby code: role not determined. The code does not show what the keys protect; review decides the priority.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open crates/cheatcodes/src/crypto.rs:26 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [crates/cheatcodes/src/crypto.rs](https://github.com/foundry-rs/foundry/blob/7f0a409a5c2016f16cb2e8618a750cc04e13977c/crates/cheatcodes/src/crypto.rs#L26) · line 26 · SHA-256 a551137cff41361990a5981742fde03e462e2a4e7b40a49fba299d7f1e749358_

```
   25 | 
   26 | use p256::ecdsa::{
   27 |     Signature as P256Signature, SigningKey as P256SigningKey, signature::hazmat::PrehashSigner,
```

_file_excerpt · [crates/cheatcodes/src/crypto.rs](https://github.com/foundry-rs/foundry/blob/7f0a409a5c2016f16cb2e8618a750cc04e13977c/crates/cheatcodes/src/crypto.rs#L526) · line 526 · SHA-256 2d2ae3b338f8f2b933a2a78de2bb94bc04717a27b2ef71b413d6c154c3dabd1c_

```
  525 |         .into_option()
  526 |         .ok_or_else(|| fmt_err!("invalid secp256k1 {name}"))
  527 | }
```

_file_excerpt · [crates/cheatcodes/src/crypto.rs](https://github.com/foundry-rs/foundry/blob/7f0a409a5c2016f16cb2e8618a750cc04e13977c/crates/cheatcodes/src/crypto.rs#L537) · line 537 · SHA-256 7c1a1c232d462506831f9bb7247a932ae80cf42f2152bf84d0ef117aa4f141da_

```
  536 |             bool::from(x_field.is_zero()) && !bool::from(y_field.is_zero()),
  537 |             "invalid secp256k1 {name}"
  538 |         );
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it; introduce an abstraction layer for crypto-agility.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-04457 — Quantum-vulnerable ECDSA: authentication and identity (certificates, tokens, device attestation) (1 file(s))

- Severity: **Low** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:ECDSA:authentication`
- Data source: crates/common/src/tempo/auth.rs
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.2.0 · 2026-10-28 12:26 UTC
- Priority score: 28.3 / 100
- CVSS v3.1: not applicable

2 reference(s) to ECDSA across 1 file(s), e.g. crates/common/src/tempo/auth.rs:115. Role, judged from paths, function names and nearby code: authentication and identity (certificates, tokens, device attestation). Short-lived authentication stays safe until a CRQC exists; long-lived identities (device attestation, CA and SSH keys) need a plan earlier.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open crates/common/src/tempo/auth.rs:115 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [crates/common/src/tempo/auth.rs](https://github.com/foundry-rs/foundry/blob/7f0a409a5c2016f16cb2e8618a750cc04e13977c/crates/common/src/tempo/auth.rs#L115) · line 115 · SHA-256 e8866289afb498a1ad1214bcef2aa268e90cbd3b50ca37d9682ea1fb0df87f5f_

```
  114 |         code_challenge: sha256_b64url(&code_verifier),
  115 |         key_type: "secp256k1",
  116 |         pub_key: pub_key_hex,
```

_file_excerpt · [crates/common/src/tempo/auth.rs](https://github.com/foundry-rs/foundry/blob/7f0a409a5c2016f16cb2e8618a750cc04e13977c/crates/common/src/tempo/auth.rs#L191) · line 191 · SHA-256 54ee92aeb19ba7eadea1ba0f5101140294f899f35d74cd9254d58fb4aff93353_

```
  190 |                     eyre::bail!(
  191 |                         "wallet returned keyType {:?} but secp256k1 was requested",
  192 |                         signed.authorization.key_type,
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Keep credentials short-lived and plan ML-DSA certificates, tokens and keys as the ecosystem supports them.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-04458 — Quantum-vulnerable BLS12-381: role not determined (1 file(s))

- Severity: **Low** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:BLS12-381:general`
- Data source: crates/debugger/src/node.rs
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.2.0 · 2026-10-28 12:26 UTC
- Priority score: 28.3 / 100
- CVSS v3.1: not applicable

7 reference(s) to BLS12-381 across 1 file(s), e.g. crates/debugger/src/node.rs:291. Role, judged from paths, function names and nearby code: role not determined. The code does not show what the keys protect; review decides the priority.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open crates/debugger/src/node.rs:291 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [crates/debugger/src/node.rs](https://github.com/foundry-rs/foundry/blob/7f0a409a5c2016f16cb2e8618a750cc04e13977c/crates/debugger/src/node.rs#L291) · line 291 · SHA-256 b5a33afbc110921885d6fdc2b239b77fa64c68479bad7f0654313bd4f95988a9_

```
  290 |         precompiles::POINT_EVALUATION => Some("pointEvaluation"),
  291 |         precompiles::BLS12_G1ADD => Some("bls12G1Add"),
  292 |         precompiles::BLS12_G1MSM => Some("bls12G1Msm"),
```

_file_excerpt · [crates/debugger/src/node.rs](https://github.com/foundry-rs/foundry/blob/7f0a409a5c2016f16cb2e8618a750cc04e13977c/crates/debugger/src/node.rs#L292) · line 292 · SHA-256 7f2d22ce6fc44deb9ea5a0267f4ae6d9e169b33af3f20db693583e3c0a1aabff_

```
  291 |         precompiles::BLS12_G1ADD => Some("bls12G1Add"),
  292 |         precompiles::BLS12_G1MSM => Some("bls12G1Msm"),
  293 |         precompiles::BLS12_G2ADD => Some("bls12G2Add"),
```

_file_excerpt · [crates/debugger/src/node.rs](https://github.com/foundry-rs/foundry/blob/7f0a409a5c2016f16cb2e8618a750cc04e13977c/crates/debugger/src/node.rs#L293) · line 293 · SHA-256 cb4c72ccdcd20bf16e22255941bc70ae5baacd7ea1ae3ca30e0d13cb5f106be7_

```
  292 |         precompiles::BLS12_G1MSM => Some("bls12G1Msm"),
  293 |         precompiles::BLS12_G2ADD => Some("bls12G2Add"),
  294 |         precompiles::BLS12_G2MSM => Some("bls12G2Msm"),
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Classify each usage, record data lifetimes, and plan migration to a post-quantum algorithm; introduce an abstraction layer for crypto-agility.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-04464 — crypto-bigint 0.5.5 is affected by RUSTSEC-2026-0387 (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/crypto-bigint@0.5.5`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 12:26 UTC
- Priority score: 20.4 / 100
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

### QSI-2026-04465 — crypto-bigint 0.7.5 is affected by RUSTSEC-2026-0387 (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/crypto-bigint@0.7.5`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 12:26 UTC
- Priority score: 20.4 / 100
- CVSS v3.1: not applicable

OSV.dev reports RUSTSEC-2026-0387 for crates.io package crypto-bigint at version 0.7.5: Multiple timing variability issues in operations intended to be constant-time. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. The advisory names no affected functions, so reachability was not determined.

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

### QSI-2026-04466 — ctutils 0.4.3 is affected by RUSTSEC-2026-0385 (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/ctutils@0.4.3`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 12:26 UTC
- Priority score: 20.4 / 100
- CVSS v3.1: not applicable

OSV.dev reports RUSTSEC-2026-0385 for crates.io package ctutils at version 0.4.3: Non-constant-time mask generation and `u128` comparisons. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. The advisory names no affected functions, so reachability was not determined.

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

### QSI-2026-04461 — No post-quantum capable cryptographic library detected

- Severity: **Info** · Classification: Insufficient data · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `dependencies`
- Data source: dependency manifests
- Detection method: Dependency name matching.
- Analyzer: dependencies 1.2.0 · 2026-10-28 12:26 UTC
- Priority score: 13.5 / 100
- CVSS v3.1: not applicable

Across 41 dependency manifests, QSI found crypto libraries (curve25519-dalek, ecdsa, jsonwebtoken, k256, p256, ring, rustls, secp256k1, x25519-dalek) but none from its PQC-capable list.

**Potential impact.** Readiness indicator only: PQC support may come from the platform (OpenSSL, OS, cloud KMS) rather than application dependencies.

**Reproduction steps.**

```
Review the dependency manifests listed in the evidence.
```

**Evidence.**

_dependency · Cargo.lock, Cargo.toml, crates/anvil/Cargo.toml, crates/anvil/core/Cargo.toml, crates/anvil/rpc/Cargo.toml, crates/anvil/server/Cargo.toml, crates/cast/Cargo.toml, crates/cheatcodes/Cargo.toml, crates/chisel/Cargo.toml, crates/cli/Cargo.toml, crates/cli-markdown/Cargo.toml, crates/common/Cargo.toml, crates/common/fmt/Cargo.toml, crates/config/Cargo.toml, crates/debugger/Cargo.toml, crates/doc/Cargo.toml, crates/evm/abi/Cargo.toml, crates/evm/core/Cargo.toml, crates/evm/coverage/Cargo.toml, crate · SHA-256 9ef612a016445014f08d85cc3387a0a580edeb71639dbaf41d6ca6d92c8daf57_

```
Crypto libraries: curve25519-dalek, ecdsa, jsonwebtoken, k256, p256, ring, rustls, secp256k1, x25519-dalek
```

**Limitations of the check.** Absence of evidence is not evidence of absence: system libraries and transitive dependencies may not be listed.

**Recommendation.** Confirm where PQC support will come from (TLS terminator, KMS/HSM, library upgrade).

**Retest procedure.** Re-scan after upgrades.

### QSI-2026-04467 — derivative 2.2.0: informational advisory RUSTSEC-2024-0388 (unmaintained)

- Severity: **Info** · Classification: Improvement recommendation · Confidence: Low
- Affected asset: `dependency:crates.io/derivative@2.2.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 12:26 UTC
- Priority score: 11.6 / 100
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

### QSI-2026-04468 — paste 1.0.15: informational advisory RUSTSEC-2024-0436 (unmaintained)

- Severity: **Info** · Classification: Improvement recommendation · Confidence: Low
- Affected asset: `dependency:crates.io/paste@1.0.15`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 12:26 UTC
- Priority score: 11.6 / 100
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
| Data/key lifetime x | 10 | 5 |
| Migration time y | 3 | 3 |
| Assumed years to CRQC z | 8 (early) | 8 |
| x + y − z | 5 → migration would finish too late under this scenario | 0 → tight margin |
#### Where z comes from

Averaged expert likelihood that a CRQC exists within each horizon, from the annual survey published by the author of this inequality. Likelihood estimates, not predictions of a date.

| Within | Likelihood | The report's wording |
|---|---|---|
| 5 years | ~15% | averaged estimate |
| 10 years | 28-49% | quite possible |
| 15 years | 51-70% | likely |

**Why this scenario (early, z = 8):** Inside the 10-year horizon the survey puts at 28-49% ('quite possible'), and consistent with the BSI estimate of 15 years that 'could shrink to 10 or even less'. Use it for data that must stay confidential for decades, where being wrong is expensive.
_Planning assumptions: x for key establishment, x for signatures, y are the defaults of the risk profile “Security software vendor”, not the client's figures; with the client's actual lifetimes the verdict can change._

### Post-quantum maturity: Level 4 of 4 — post-quantum by default in the critical paths

- Hybrid — channel key exchange (TLS, Noise, handshakes): Cargo.toml (classical group + X25519MLKEM768)
- In use: X25519MLKEM768 — Cargo.toml

**Next step:** Keep the inventory current and review new code paths before release.

_Levels: 0 none; 1 present, not wired; 2 in use outside the critical paths; 3 hybrid in a critical path; 4 post-quantum by default in the critical paths (root of trust, key wrapping, channel key exchange). Judged from code and manifests._

### What the quantum-vulnerable algorithms do

| Role | Algorithms (files) | ID | First step |
|---|---|---|---|
| **channel key exchange (TLS, Noise, handshakes)** | TLS ECDHE (1) | QSI-2026-04456 | Move the handshake to a hybrid key exchange (X25519MLKEM768 in TLS 1.3; a hybrid KEM in Noise-based protocols) |
| **transaction and message signing** | ECDSA (9), BLS12-381 (3) | QSI-2026-04454, QSI-2026-04459 | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains adopt them |
| **authentication and identity (certificates, tokens, device attestation)** | ECDSA (1) | QSI-2026-04457 | Keep credentials short-lived and plan ML-DSA certificates, tokens and keys as the ecosystem supports them |
| **role not determined** | BLS12-381 (1), ECDSA (1) | QSI-2026-04455, QSI-2026-04458 | Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it; introduce an abstraction layer for crypto-agility |

_Roles are judged from file paths, function names and the code around each match; review confirms them. Root-of-trust keys and wrapped keys come first: they are hard to replace or can be recorded today._
No readiness questionnaire was completed for this project.

### Quantum algorithms relevant to this inventory

| Quantum algorithm | Effect | Attack model | Inventoried algorithms (rows) | What it means for this audit |
|---|---|---|---|---|
| Shor's algorithm — discrete logarithms in finite fields | breaks | Q1 | BLS12-381 (4) | Breaks finite-field Diffie–Hellman and DSA at every size. Move key establishment to ML-KEM (hybrid with X25519 or ECDH during the transition) and signatures to ML-DSA or SLH-DSA. |
| Shor's algorithm — elliptic-curve discrete logarithms | breaks | Q1 | BLS12-381 (4), ECDSA (12), X25519MLKEM768 (1) | Elliptic-curve keys are expected to fall before RSA keys of comparable classical strength. On blockchains, coins whose public key is already on chain (reused addresses, pay-to-public-key and Taproot outputs) are exposed first; plan the move to post-quantum signatures and avoid key reuse in the meantime. |
| Grover's algorithm — key search and preimages | weakens (larger keys restore the margin) | Q1 | AES-256 (1), HKDF (1), Keccak-256 (55), RIPEMD-160 (1), SHA-2 (4) | Not a break. 256-bit keys (AES-256, ChaCha20) keep a comfortable margin; AES-128 meets NIST category 1, while some authorities ask for 256-bit keys in quantum-resistant contexts (see the AES-128 entry). Prefer 256-bit keys for long-lived data; 256-bit hashes need no change for preimage resistance. |
| Brassard–Høyer–Tapp — collision search | weakens (larger keys restore the margin) | Q1 | Keccak-256 (55), RIPEMD-160 (1), SHA-2 (4) | 256-bit hashes (SHA-256, SHA3-256) remain adequate for collision resistance; 160-bit hashes are already weak classically (SHA-1 collisions are practical). Use 384/512-bit hashes where NIST categories 4–5 are required. |
| Quantum lattice sieving | included in standard parameters | Q1 | X25519MLKEM768 (1) | No change for ML-KEM or ML-DSA at the standard parameter sets. A 2024 claim of a polynomial-time quantum LWE algorithm was withdrawn after a bug was found (see claims). |

_Effects: breaks — replace the algorithm; weakens — larger keys or outputs restore the margin; included in standard parameters — no action at standard parameter sets; only with superposition queries — not applicable to ordinary deployments._


## 9. Limitations and assumptions

- This report presents automated and documented analysis results for the stated scope. It is not a legal opinion, a certification or an attestation of compliance with any standard.
- z is a planning assumption chosen per risk profile, not a prediction. A cryptographically relevant quantum computer is not publicly known to exist today.
- slither: slither is not installed on the server (pip install slither-analyzer + solc)
- slither: slither is not installed on the server (pip install slither-analyzer + solc)
- slither: slither is not installed on the server (pip install slither-analyzer + solc)
- slither: slither is not installed on the server (pip install slither-analyzer + solc)
- slither: slither is not installed on the server (pip install slither-analyzer + solc)
- slither: slither is not installed on the server (pip install slither-analyzer + solc)
- slither: slither is not installed on the server (pip install slither-analyzer + solc)
- slither: slither is not installed on the server (pip install slither-analyzer + solc)
- slither: slither is not installed on the server (pip install slither-analyzer + solc)
- slither: slither is not installed on the server (pip install slither-analyzer + solc)
- slither: slither is not installed on the server (pip install slither-analyzer + solc)
- slither: slither is not installed on the server (pip install slither-analyzer + solc)
- slither: slither is not installed on the server (pip install slither-analyzer + solc)
- slither: slither is not installed on the server (pip install slither-analyzer + solc)

## 10. Remediation plan / Priorities for 30, 60 and 90 days

### 30 days

| Priority | ID | Action | Type | Closure criteria |
|---|---|---|---|---|
| P2 | QSI-2026-04469 | Upgrade quick-xml to a fixed version (0.41.0). | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0194. |
| P2 | QSI-2026-04470 | Upgrade quick-xml to a fixed version (0.41.0). | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0195. |
| P2 | QSI-2026-04462 | Upgrade block-buffer to a fixed version (none published yet; see the advisory for mitigations). | root-cause fix | Dependency scan no longer reports GHSA-qwgh-2vcv-g2f7. |
| P2 | QSI-2026-04463 | Upgrade block-buffer to a fixed version (none published yet; see the advisory for mitigations). | root-cause fix | Dependency scan no longer reports GHSA-qwgh-2vcv-g2f7. |
### 60 days

| Priority | ID | Action | Type | Closure criteria |
|---|---|---|---|---|
| P2 | QSI-2026-04456 | Build rustls with the aws-lc-rs provider (rustls::crypto::aws_lc_rs) and the prefer-post-quantum feature, which puts X25519MLKEM768 first. | root-cause fix | A PQ-capable client negotiates X25519MLKEM768. |
| P3 | QSI-2026-04464 | Triage RUSTSEC-2026-0387; upgrade crypto-bigint to a fixed version (0.7.6) if it applies. | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0387, or the triage is recorded. |
| P3 | QSI-2026-04465 | Triage RUSTSEC-2026-0387; upgrade crypto-bigint to a fixed version (0.7.6) if it applies. | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0387, or the triage is recorded. |
| P3 | QSI-2026-04466 | Triage RUSTSEC-2026-0385; upgrade ctutils to a fixed version (0.4.4) if it applies. | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0385, or the triage is recorded. |
### 90 days

| Priority | ID | Action | Type | Closure criteria |
|---|---|---|---|---|
| P3 | QSI-2026-04453 | Pin the compiler version used in testing. | root-cause fix | Re-run static analysis and add a unit/fuzz test that exercises the pattern. |
| P3 | QSI-2026-04460 | Pin the compiler version used in testing. | root-cause fix | Re-run static analysis and add a unit/fuzz test that exercises the pattern. |
| P3 | QSI-2026-04454 | Add ECDSA usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-04459 | Add BLS12-381 usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-04455 | Add ECDSA usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-04457 | Add ECDSA usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-04458 | Add BLS12-381 usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P4 | QSI-2026-04454 | Plan migration of ECDSA to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-04459 | Plan migration of BLS12-381 to  (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows  or a hybrid scheme in use. |
| P4 | QSI-2026-04455 | Plan migration of ECDSA to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-04457 | Plan migration of ECDSA to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-04458 | Plan migration of BLS12-381 to  (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows  or a hybrid scheme in use. |
| P4 | QSI-2026-04467 | Replace derivative with a maintained alternative or record why it stays. | root-cause fix | derivative replaced, or the decision recorded. |
| P4 | QSI-2026-04468 | Replace paste with a maintained alternative or record why it stays. | root-cause fix | paste replaced, or the decision recorded. |

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

1. A. Becker, L. Ducas, N. Gama, T. Laarhoven — New directions in nearest neighbor searching with applications to lattice sieving (SODA 2016; IACR ePrint 2015/1128) — IACR ePrint. <https://eprint.iacr.org/2015/1128> (peer-reviewed article: classical sieving in 2^{0.292n + o(n)})
2. A. Chailloux, J. Loyer — Lattice sieving via quantum random walks (ASIACRYPT 2021; IACR ePrint 2021/570) — IACR ePrint. <https://eprint.iacr.org/2021/570> (peer-reviewed article: 2^{0.2570d + o(d)}, previously 2^{0.2653d + o(d)} (Laarhoven))
3. A. Chailloux, M. Naya-Plasencia, A. Schrottenloher — An Efficient Quantum Collision Search Algorithm and Implications on Symmetric Cryptography (ASIACRYPT 2017; IACR ePrint 2017/847) — IACR ePrint. <https://eprint.iacr.org/2017/847> (peer-reviewed article: Õ(2^{2n/5}) time, O(n) qubits, Õ(2^{n/5}) classical memory)
4. C. Chevignard, P.-A. Fouque, A. Schrottenloher — Reducing the Number of Qubits in Quantum Discrete Logarithms on Elliptic Curves (IACR ePrint 2026/280) — IACR ePrint. <https://eprint.iacr.org/2026/280> (revision of a EUROCRYPT 2026 paper: 3.12n + o(n) qubits; for n = 256, 1193 qubits and 22 runs of 2^38.98 Toffoli gates)
5. C. Gidney, M. Ekerå — How to factor 2048 bit RSA integers in 8 hours using 20 million noisy qubits (Quantum 5, 433) — Quantum. <https://doi.org/10.22331/q-2021-04-15-433> (peer-reviewed article (2021): 10^-3 gate error, 1 µs cycle, 10 µs reaction time)
6. C. Zalka — Grover's quantum searching algorithm is optimal (Phys. Rev. A 60, 2746, 1999; arXiv:quant-ph/9711070) — APS. <https://doi.org/10.1103/PhysRevA.60.2746> (peer-reviewed article: optimal for any success probability; parallel search gains no more than splitting the space)
7. CRYSTALS-Kyber — Algorithm Specifications and Supporting Documentation (round 3, 2021-08-04) — CRYSTALS team. <https://pq-crystals.org/kyber/data/kyber-specification-round3-20210804.pdf> (NIST round-3 submission: core-SVP cost 2^{0.292β} classical, 2^{0.265β} quantum; Kyber768 166 quantum bits)
8. Common Vulnerability Scoring System v3.1: Specification Document — FIRST. <https://www.first.org/cvss/v3.1/specification-document> (final)
9. D. J. Bernstein — Cost analysis of hash collisions: Will quantum computers make SHARCS obsolete? (2009) — cr.yp.to. <https://cr.yp.to/hash/collisioncost-20090823.pdf> (paper dated 2009-08-23)
10. D. Litinski — How to compute a 256-bit elliptic curve private key with only 50 million Toffoli gates (arXiv:2306.08585) — arXiv. <https://arxiv.org/abs/2306.08585> (preprint (2023-06-14): 6000 modules × 1152 physical qubits, one key per 10 minutes under its architecture assumptions)
11. FIPS 203 — Module-Lattice-Based Key-Encapsulation Mechanism Standard (ML-KEM) — NIST. <https://csrc.nist.gov/pubs/fips/203/final> (final (August 2024))
12. FIPS 204 — Module-Lattice-Based Digital Signature Standard (ML-DSA) — NIST. <https://csrc.nist.gov/pubs/fips/204/final> (final (August 2024))
13. FIPS 205 — Stateless Hash-Based Digital Signature Standard (SLH-DSA) — NIST. <https://csrc.nist.gov/pubs/fips/205/final> (final (August 2024))
14. G. Brassard, P. Høyer, A. Tapp — Quantum Algorithm for the Collision Problem (LATIN '98; arXiv:quant-ph/9705002) — Springer / arXiv. <https://arxiv.org/abs/quant-ph/9705002> (peer-reviewed article: collisions of r-to-one functions in O((N/r)^{1/3}) expected evaluations)
15. IANA — Transport Layer Security (TLS) Parameters (Supported Groups, SignatureScheme, Cipher Suites) — IANA. <https://www.iana.org/assignments/tls-parameters/> (living registry (checked 2026-10-13); 'Recommended' column Y/N/D)
16. J. Proos, C. Zalka — Shor's discrete logarithm quantum algorithm for elliptic curves (Quantum Inf. Comput. 3(4), 2003; arXiv:quant-ph/0301141) — Quantum Information & Computation. <https://doi.org/10.26421/QIC3.4-3> (peer-reviewed article)
17. L. K. Grover — A fast quantum mechanical algorithm for database search (STOC 1996) — ACM. <https://doi.org/10.1145/237814.237866> (peer-reviewed article)
18. M. Amy et al. — Estimating the cost of generic quantum pre-image attacks on SHA-2 and SHA-3 (SAC 2016; arXiv:1603.09383) — Springer / arXiv. <https://arxiv.org/abs/1603.09383> (peer-reviewed article: SHA-256 about 2^153.8 surface-code cycles on 2^12.6 logical qubits; SHA3-256 about 2^146.5 cycles on 2^20)
19. M. Cain et al. — Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits (arXiv:2603.28627) — arXiv. <https://arxiv.org/abs/2603.28627> (preprint (2026-03-30): P-256 in a few days with 26,000 physical neutral-atom qubits; RSA-2048 one to two orders of magnitude longer)
20. M. Ekerå, J. Gärtner — A high-level comparison of state-of-the-art quantum algorithms for breaking asymmetric cryptography (arXiv:2405.14381) — arXiv. <https://arxiv.org/abs/2405.14381> (preprint (2024-05-23): Regev-style algorithms show no overall advantage yet for cryptographic RSA and finite-field sizes)
21. M. Mosca — Cybersecurity in an Era with Quantum Computers: Will We Be Ready? (IEEE Security & Privacy, 2018) — IEEE. <https://doi.org/10.1109/MSP.2018.3761723> (peer-reviewed article; source of the x + y > z migration inequality)
22. M. Roetteler, M. Naehrig, K. Svore, K. Lauter — Quantum resource estimates for computing elliptic curve discrete logarithms (ASIACRYPT 2017) — IACR / arXiv. <https://arxiv.org/abs/1706.06752> (peer-reviewed article: at most 9n + 2⌈log2 n⌉ + 10 qubits and 448 n^3 log2 n + 4090 n^3 Toffoli gates)
23. NIST IR 8547 — Transition to Post-Quantum Cryptography Standards — NIST. <https://csrc.nist.gov/pubs/ir/8547/ipd> (initial public draft (November 2024); proposes deprecating quantum-vulnerable public-key algorithms after 2030 and disallowing them after 2035 — dates may change in the final version)
24. NIST — Post-Quantum Cryptography Standardization: Evaluation Criteria, Security (Call for Proposals, Section 4.A.5) — NIST. <https://csrc.nist.gov/Projects/Post-Quantum-Cryptography/Post-Quantum-Cryptography-Standardization/Evaluation-Criteria/Security-(Evaluation-Criteria)> (security categories: AES-128 key search 2^170/MAXDEPTH quantum gates, AES-192 2^233/MAXDEPTH, AES-256 2^298/MAXDEPTH; MAXDEPTH 2^40–2^96)
25. OSV advisory GHSA-qwgh-2vcv-g2f7 — OSV.dev. <https://osv.dev/vulnerability/GHSA-qwgh-2vcv-g2f7> (modified 2026-08-19T19:30:06.686866977Z)
26. OSV advisory RUSTSEC-2024-0388 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2024-0388> (modified 2024-11-10T13:34:40Z)
27. OSV advisory RUSTSEC-2024-0436 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2024-0436> (modified 2026-01-27T22:03:15.694766Z)
28. OSV advisory RUSTSEC-2026-0194 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0194> (modified 2026-07-02T08:00:03.849273679Z)
29. OSV advisory RUSTSEC-2026-0195 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0195> (modified 2026-07-02T09:00:04.037478193Z)
30. OSV advisory RUSTSEC-2026-0385 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0385> (modified 2026-10-23T08:30:02.389575143Z)
31. OSV advisory RUSTSEC-2026-0387 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0387> (modified 2026-10-24T03:45:02.365137418Z)
32. P. W. Shor — Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms on a Quantum Computer (SIAM J. Comput., 1997) — SIAM. <https://doi.org/10.1137/S0097539795293172> (peer-reviewed article)
33. R. Babbush et al. — Securing Elliptic Curve Cryptocurrencies against Quantum Vulnerabilities: Resource Estimates and Mitigations (arXiv:2603.28846) — arXiv. <https://arxiv.org/abs/2603.28846> (preprint (2026-03-30, v2 2026-04-15): 256-bit ECDLP with < 1200 logical qubits and < 90 M Toffoli gates (or < 1450 and < 70 M); < 500,000 physical qubits at 10^-3 error, minutes)
34. RFC 10024 — Hybrid ECDHE-MLKEM key agreement for TLS 1.3 (X25519MLKEM768, SecP256r1MLKEM768, SecP384r1MLKEM1024) — IETF. <https://www.rfc-editor.org/rfc/rfc10024> (standards track; checked 2026-10-13)
35. S. Jaques, M. Naehrig, M. Roetteler, F. Virdia — Implementing Grover oracles for quantum key search on AES and LowMC (EUROCRYPT 2020; arXiv:1910.01700) — Springer / arXiv. <https://arxiv.org/abs/1910.01700> (peer-reviewed article: lower cost estimates for the AES key searches that define the NIST categories)
36. Smart Contract Weakness Classification (SWC) Registry — SWC community (no longer actively maintained). <https://swcregistry.io/> (historic reference; still widely cited)

## Appendices: Cryptographic inventory

| Algorithm | Parameter | Library | Quantum status | Classical status | Count | Locations | Examples |
|---|---|---|---|---|---|---|---|
| RIPEMD-160 | RIPEMD-160 |  | weak classically | legacy | 1 | 1 | crates/evm/traces/src/decoder/precompiles.rs:78 |
| AES-256 | AES-256 |  | reduced margin (Grover), approved | acceptable | 1 | 1 | crates/cast/src/cmd/tempo/zone/encryption.rs:6 |
| HKDF |  |  | reduced margin (Grover), approved | acceptable | 1 | 1 | crates/cast/src/cmd/tempo/zone/encryption.rs:9 |
| Keccak-256 | Keccak-256 |  | Grover: acceptable to NIST, below ECCG/ANSSI guidance | acceptable | 55 | 55 | crates/anvil/core/src/eth/transaction/mod.rs:82; crates/anvil/src/config.rs:222; crates/anvil/src/eth/api.rs:964 |
| SHA-2 | SHA-256 |  | Grover: acceptable to NIST, below ECCG/ANSSI guidance | acceptable | 4 | 4 | .github/scripts/benchmark_clickhouse.py:170; crates/cast/src/cmd/tempo/zone/encryption.rs:13; crates/common/src/external_compiler.rs:276 |
| X25519MLKEM768 |  |  | hybrid | acceptable | 1 | 1 | Cargo.toml:494 |
| Crypto library | 0.13.2 | p256 (RustCrypto elliptic curves) | n/a | acceptable | 1 | 1 | Cargo.lock |
| Crypto library | 0.13.4 | k256 (RustCrypto elliptic curves) | n/a | acceptable | 1 | 1 | Cargo.lock |
| Crypto library | 0.14.0 | p256 (RustCrypto elliptic curves) | n/a | acceptable | 1 | 1 | Cargo.lock |
| Crypto library | 0.16.9 | ecdsa (python-ecdsa) | n/a | acceptable | 1 | 1 | Cargo.lock |
| Crypto library | 0.17.0 | ecdsa (python-ecdsa) | n/a | acceptable | 1 | 1 | Cargo.lock |
| Crypto library | 0.17.14 | ring (ring (Rust)) | n/a | acceptable | 1 | 1 | Cargo.lock |
| Crypto library | 0.23.46 | rustls (rustls) | n/a | acceptable | 2 | 2 | Cargo.lock; Cargo.toml |
| Crypto library | 0.30.0 | secp256k1 (secp256k1 bindings) | n/a | acceptable | 1 | 1 | Cargo.lock |
| Crypto library | 0.31.1 | secp256k1 (secp256k1 bindings) | n/a | acceptable | 1 | 1 | Cargo.lock |
| Crypto library | 10.4.0 | jsonwebtoken (jsonwebtoken (Node)) | n/a | acceptable | 1 | 1 | Cargo.lock |
| Crypto library | 3.0.0 | x25519-dalek (ed25519-dalek) | n/a | acceptable | 1 | 1 | Cargo.lock |
| Crypto library | 5.0.0 | curve25519-dalek (ed25519-dalek) | n/a | acceptable | 1 | 1 | Cargo.lock |
| Crypto library | 0.13 | k256 (RustCrypto elliptic curves) | n/a | acceptable | 1 | 1 | Cargo.toml |
| Crypto library | workspace | k256 (RustCrypto elliptic curves) | n/a | acceptable | 3 | 3 | crates/cast/Cargo.toml; crates/cheatcodes/Cargo.toml; crates/common/Cargo.toml |
| Crypto library | 0.13 | p256 (RustCrypto elliptic curves) | n/a | acceptable | 1 | 1 | crates/cheatcodes/Cargo.toml |
| Crypto library | 0.16 | ecdsa (python-ecdsa) | n/a | acceptable | 1 | 1 | crates/cheatcodes/Cargo.toml |
| Crypto library | workspace | rustls (rustls) | n/a | acceptable | 1 | 1 | crates/cli/Cargo.toml |
| Crypto library | 9.0.3 | jsonwebtoken (jsonwebtoken (Node)) | n/a | acceptable | 1 | 1 | editors/vscode/package-lock.json |
| BLS12-381 |  |  | vulnerable (Shor) | acceptable | 4 | 4 | crates/debugger/src/node.rs:291; crates/evm/core/src/precompiles.rs:34; crates/evm/traces/src/decoder/mod.rs:28 |
| ECDSA | secp256k1 |  | vulnerable (Shor) | acceptable | 10 | 10 | crates/anvil/src/eth/backend/cheats.rs:11; crates/anvil/src/eth/backend/tempo.rs:271; crates/cast/src/cmd/keychain.rs:153 |
| ECDSA | P-256 |  | vulnerable (Shor) | acceptable | 2 | 2 | crates/cheatcodes/src/crypto.rs:26; crates/evm/networks/src/lib.rs:29 |

_Long lists are grouped here; the full per-file list is in the JSON report, signed with the same key._

## Appendices: Input files

| File | Size | SHA-256 | Redactions |
|---|---|---|---|
| .cargo/config.toml | 496 | `e1030cf1b1c221476b21cf0b0693491fc8b8506f4eb9be92fbf5af210b9779b1` | 0 |
| .github/scripts/benchmark_clickhouse.py | 20787 | `ecf2466268d103c6477f39bd2ab08d4f837d428fdd133e11612982328a492794` | 0 |
| .github/scripts/compare-benchmark-thresholds.py | 4807 | `1c6d4ebf60a43f16347f9199ea7c2df73a9da4649857d30b48e41c62ba3a1622` | 0 |
| .github/scripts/contracts/BatchCounter.sol | 343 | `d573ae940de4141c483f0e933d27ee0c40754f72ccf07f144dc5e3499faaa320` | 0 |
| .github/scripts/contracts/CounterWithRequire.sol | 306 | `427bf1ddf5d91be68251f54ce74ae541ed241e8014b70a98c656a511a6ecea95` | 0 |
| .github/scripts/contracts/DeployAndCall.s.sol | 727 | `1595eb42765b9e3b88060afbb49a0f98fae88422c07d8aff4209b2dc0ae181da` | 0 |
| .github/scripts/finalize-release.py | 13109 | `6fd40f9dc173c98d9ebd753f5836cbe218adb091b834d13a7cb65503954e735a` | 0 |
| .github/scripts/matrices.py | 3734 | `ccce395736307d2cdb1db7345bee3411e48c118d5f10338fa619517c78b7b0b8` | 0 |
| Cargo.lock | 346630 | `41f718fa4c0ce70e1b47e3efc513a531ba0c6726277dabb963fc67bb32d49f78` | 0 |
| Cargo.toml | 24712 | `20deefd91be60baa4e2d2fbe3920c30ed7e7caa5ec44fb552624ae991beae6db` | 0 |
| crates/anvil/Cargo.toml | 6031 | `abea5ad23023925b79bf6d39dc333106e55b0fd07a01982fb149c0b7c637776c` | 0 |
| crates/anvil/bin/main.rs | 357 | `014945ca3b087fc2fb4c1681bf804f84f202b472eec1eab73370b985c28d19ab` | 0 |
| crates/anvil/core/Cargo.toml | 1255 | `92e4e18254f46dbf9e02a0c3ce4d465d416ad55ec3e5906205716ac184473649` | 0 |
| crates/anvil/core/src/eth/block.rs | 16191 | `5ae5c5c0e5824d76a2ae6e050b43d1415265f91f97f4537f1c5570b04e629a4d` | 0 |
| crates/anvil/core/src/eth/mod.rs | 103288 | `94b52329b63f049fe2003deca2bdd04ecf2ce7ba0310a4f37a5b6429035e1b25` | 0 |
| crates/anvil/core/src/eth/serde_helpers.rs | 3861 | `a29fc7ca2c67478ada2e087f6cbb1c501a9a6dae407f219107eb4bbe4987ce66` | 0 |
| crates/anvil/core/src/eth/subscription.rs | 1579 | `c8cda3db87534c9981eb2416a36c5c61140f2702fc9c6990ae3d570fcdeca359` | 0 |
| crates/anvil/core/src/eth/transaction/mod.rs | 7127 | `31e1c34e6bf96e75d6764dbfb87d48e0a373020c7f608509df8e91b6a2a2d02c` | 0 |
| crates/anvil/core/src/eth/wallet.rs | 1825 | `bc850b214b25cf6182b10939ac9b09d237c179a6f67b5fcd18808fc0a9f5915b` | 0 |
| crates/anvil/core/src/lib.rs | 238 | `60f164c7bce42b1cb605f83682c6393c4762ea32e161573af31906769bfd09ad` | 0 |
| crates/anvil/core/src/types.rs | 617 | `fd9cfe3664906a1c0b4933a256496f75d1ca6dec998a2b6341716cb979241230` | 0 |
| crates/anvil/rpc/Cargo.toml | 339 | `80aacf456a16bd29337a7a906ea63ebeaf4837484f3a501857012913227ac225` | 0 |
| crates/anvil/rpc/src/error.rs | 4820 | `3122e8bd0afa735d16437f3badbe88a40064e3863940f2b908516c7bc29c39c9` | 0 |
| crates/anvil/rpc/src/lib.rs | 279 | `e228c7206be098af5e3d733833674456bd19235021f294d057a4ac31ece6444d` | 0 |
| crates/anvil/rpc/src/request.rs | 10008 | `3734a59bcb46ebd2818aa1b72c8e0e290a1d9928e7b9d814a2199e90f221061d` | 0 |
| crates/anvil/rpc/src/response.rs | 2374 | `38021d1a30abcac3c929122e7d232c0413e07138def36c67c88ba0e930d39a61` | 0 |
| crates/anvil/server/Cargo.toml | 1072 | `bd97894874cb94fa54f56cb323b2f421c1ecb15452076e7b5567a5dd36d2b6e5` | 0 |
| crates/anvil/server/src/config.rs | 2578 | `7ff7c490a8d903759e1ece5cffcdb8e774cbaeac13361c3d505717e76cdf7e12` | 0 |
| crates/anvil/server/src/error.rs | 407 | `1c98788ff135ac8dc9e6201334cdf4aaea0d8fa8881517679d1e1c257aea1125` | 0 |
| crates/anvil/server/src/handler.rs | 12717 | `00f419075c4d55fd96a952fcd3c398ca5f46f5da56abfb23792699bf39bc07f1` | 0 |
| crates/anvil/server/src/ipc.rs | 6252 | `c650f768a7d79917792d31eaee4836fb14690efcad5b4edc478ac70ca2aceb3b` | 0 |
| crates/anvil/server/src/lib.rs | 13597 | `2e6877ada227c84fffb804719fb52a0b6c188999d7eecf2ee94ea724fc0ee893` | 0 |
| crates/anvil/server/src/pubsub.rs | 13298 | `11157e97c4d8fc83029df748b00a54b6a767c769d9d203acf2a7347bd3606f99` | 0 |
| crates/anvil/server/src/ws.rs | 2365 | `6a7446aae0920e12e7f506d4c939f12d3299f1b750414e32defea734e11cf175` | 0 |
| crates/anvil/src/args.rs | 2022 | `e37b9f1851663dc9b1c65fa0affd3cdb5f4d33cd466c64feba222904bb2a8ded` | 0 |
| crates/anvil/src/cmd.rs | 62739 | `22eed0693ab0baa5b4e1c9b133ec6ef5fde5fd36bbe4b38f0863743c9990a41b` | 0 |
| crates/anvil/src/config.rs | 114953 | `c7027e252ab18f3ada81c4c7b3fb1b72e854f8dd9a58b904f0dbc026b930485e` | 0 |
| crates/anvil/src/error.rs | 300 | `38fa9a7c3588858e410f88c326783496b8d63e6daef8454aed4c31e7a40f3519` | 0 |
| crates/anvil/src/eth/api.rs | 248171 | `ce3cefe14f2f4ee30f2f6bf352a242cf3b3617ea32e14fa25f4f01c7792e2ec0` | 0 |
| crates/anvil/src/eth/backend/cheats.rs | 9880 | `31fbcf6016a3810cdacd6adcabaa8b97bbeeba80a7ad238e7ae8f16670bdfeb1` | 0 |
| crates/anvil/src/eth/backend/db.rs | 42307 | `dcc44889732e1bd639c87574758c3612aa784797fa566f713bdef489e4256f32` | 0 |
| crates/anvil/src/eth/backend/executor/optimism.rs | 5280 | `e2aee0089311395d1467e6ab15546083cad392a8b4da7ff64ad57fbe546c9321` | 0 |
| crates/anvil/src/eth/backend/executor.rs | 38017 | `a579a3f9044fd24a19e4ee0a8033833c44a7de2107d9fe030185cd5389ba679b` | 0 |
| crates/anvil/src/eth/backend/fork.rs | 39449 | `993c58ae6204d61590ee662e4f4f3e092f973b2c762c16c810410fd8da524f86` | 0 |
| crates/anvil/src/eth/backend/genesis.rs | 2518 | `b07487534afa0fd47a7addbc326a73db065cb9368acf1e05b5f8b3e57b64d6f0` | 0 |
| crates/anvil/src/eth/backend/info.rs | 1968 | `870024ae660d4134c0252413e91bcf0f8145beba826ad8777480f4cf52f12935` | 0 |
| crates/anvil/src/eth/backend/mem/base.rs | 10928 | `0973b9fc31540d1d0a023f6ee9d61f2060c334d2db168657e3d5faa13679610d` | 0 |
| crates/anvil/src/eth/backend/mem/cache.rs | 4573 | `94e079b7c558d14b8db33c8732201c5ab80eee36c347af863d2b5496b2102a62` | 0 |
| crates/anvil/src/eth/backend/mem/fork_db.rs | 7193 | `d5187d494a41712f44a2aadeba319405b4155ec847051e15ba0fb974205da977` | 0 |
| crates/anvil/src/eth/backend/mem/in_memory_db.rs | 35907 | `6039e63f7f90200da223b632a6b032249df392fbc284a60bb0959772c51e232f` | 0 |
| crates/anvil/src/eth/backend/mem/inspector.rs | 14807 | `4929578357312a7ffadf0e1758a62a30c67d3e5d60f1703a98068f2cefe0cb14` | 0 |
| crates/anvil/src/eth/backend/mem/mod.rs | 478575 | `adf028dd539a767de0270f2ed236f231a663f5653184fed1b803f912e472a6e3` | 0 |
| crates/anvil/src/eth/backend/mem/monad.rs | 35995 | `67c999e22fb886d6af02f2b7a608ff56b6de71e0413c646be9102972e85c363f` | 0 |
| crates/anvil/src/eth/backend/mem/optimism.rs | 1955 | `f6188a8802387033cbdf7871eeb3934f63de8aac9664a6c9a7a1a40eb09b3ae8` | 0 |
| crates/anvil/src/eth/backend/mem/state.rs | 27273 | `d6f3ffc8b66185b617f430b95fb83493c199e0ea7adfd1d401d69ea532f45d76` | 0 |
| crates/anvil/src/eth/backend/mem/storage.rs | 47037 | `cdf13f0e85ced3c9d735cbef8a56f49dd88d9da1f69b650a3a553acd2f12f916` | 0 |
| crates/anvil/src/eth/backend/mod.rs | 270 | `b4e512990d35fd687e29f8dd9d4de5589c8e4f900598cd16fcc44583a0ab06d8` | 0 |
| crates/anvil/src/eth/backend/notifications.rs | 1340 | `ea12bd6e5edabe950c89f75ff7554c9a42f9801a20d1f255e73b96315186001e` | 0 |
| crates/anvil/src/eth/backend/replay.rs | 17229 | `48d6e67f61111d2af3a36beb5589bf06b5f60e71ce6ff36adae5a99cf30e1eec` | 0 |
| crates/anvil/src/eth/backend/tempo.rs | 10906 | `3bba5daeff0a18a0517bc06b4e9b0534caa5c46f117ab066748d163312c5506a` | 0 |
| crates/anvil/src/eth/backend/time.rs | 22083 | `9255590a064e9f4ef2fd4a88f7b13ce4ec466c9aef27ddf81279b04fbd134cc1` | 0 |
| crates/anvil/src/eth/backend/validate.rs | 1330 | `84e79dade8298f6e9244b534f55f345b21482479337589fc10d3d71724536e3a` | 0 |
| crates/anvil/src/eth/error/base.rs | 1467 | `708c91e8951c2e1fe93fb133da1dba29f61dc10826385f130b0775c47a1bda0a` | 0 |
| crates/anvil/src/eth/error/mod.rs | 31831 | `d235fb662e2a6fd58d4d7c10592b61013a8bbec58152078d3ae2a76bdc8b66f0` | 0 |
| crates/anvil/src/eth/error/optimism.rs | 2497 | `3008e7f4efbbe68c145081bef46584aa039f76736d9e3de3ada3b04033901242` | 0 |
| crates/anvil/src/eth/fees/optimism.rs | 7290 | `08ecff4d5409341afa440e5a8c3a8e6fde35325be29dfd37abc2870adf991755` | 0 |
| crates/anvil/src/eth/fees.rs | 33508 | `b6cc86328fcd56c7cdd9ac919fa835dcad1241da1ede6319d43130ec19ea82e6` | 0 |
| crates/anvil/src/eth/macros.rs | 247 | `de8b7226023fb194a25d89452be5620967b3c09f1ae0cba80350d16405ba6c64` | 0 |
| crates/anvil/src/eth/miner.rs | 26629 | `eb4b67b8f240ba87f9069cb514667c2668befbd76ecc99f3b515ad4ef9a2d580` | 0 |
| crates/anvil/src/eth/mod.rs | 999 | `9b5dfb5c833aa43dde23a15ccf5f3356af7e97284dd43ed266c8917789638464` | 0 |
| crates/anvil/src/eth/otterscan/api.rs | 17768 | `199618c2b471befa0fdddc11405883052103cdc127341553a9d4d7d8246da8e2` | 0 |
| crates/anvil/src/eth/otterscan/mod.rs | 13 | `339973d2699a48cfe2208af247916535e23b436f613c1eba94b60e09cd9d1c6b` | 0 |
| crates/anvil/src/eth/pool/mod.rs | 22837 | `ac65910be47f201c4902a289b575c84c63bafa6c36347c7049855fce7d5dd922` | 0 |
| crates/anvil/src/eth/pool/transactions.rs | 31199 | `a9f602eb1cd997f36fe2064d3e36646bd9bf9dc7cd4f0a948c86fc3b7f32dbbc` | 0 |
| crates/anvil/src/eth/sign.rs | 6772 | `388d52c3950a378c93ea2aea5f513abc01d70cc9facb52e72bee91eae9f1a8b0` | 0 |
| crates/anvil/src/eth/util.rs | 319 | `089b42724ee727b4f89dd0a40c6f74d2855a128f5002e92c1da0897c8ecd8657` | 0 |
| crates/anvil/src/evm/mod.rs | 7329 | `e0b6f6ea124720cf1bc915a99a3d3b2577edafeb402671794fe16c0db4718e07` | 0 |
| crates/anvil/src/evm/optimism.rs | 3091 | `f17918c733a416359d76291fa5b1ada09f934b8f7712afd20374e89d1b9f1809` | 0 |
| crates/anvil/src/filter.rs | 10342 | `beb85bedff338bfcf6acffbb6e1c11c3c7420a385b2586da9c5ae100f4c6c829` | 0 |
| crates/anvil/src/lib.rs | 15015 | `e4b92774862bf705868972cac53e55b0e5e50f4fe3d118175f78ae258b9f36dd` | 0 |
| crates/anvil/src/logging.rs | 2211 | `ae560f0532febedd797cf0b199b923cef64264feb251661a8fed10a5b518ae8c` | 0 |
| crates/anvil/src/opts.rs | 1081 | `8b70308e27f18fe813cd43d7c1887937dd9994b949e5cd710215bd7b807a46da` | 0 |
| crates/anvil/src/pubsub.rs | 10767 | `31ba5f5b3f76f5875b9ea6ac4f7ea2ae48938a817f9f9f4495673d3beec2297a` | 0 |
| crates/anvil/src/server/beacon/error.rs | 3784 | `99453b48a0d01bb1b6087fdf7c2309e95fe30f20b1c294aadd344249c89f07a1` | 0 |
| crates/anvil/src/server/beacon/handlers.rs | 5580 | `6824ea4ad0dcc7c183a723f23f38966d5343437d7c89d9decf28d2e40c0f42fc` | 0 |
| crates/anvil/src/server/beacon/mod.rs | 655 | `e8ec8b2b9c2dc97d48bfbfc35722141bdf3bc0f3935469525987ece50bf79104` | 0 |
| crates/anvil/src/server/beacon/utils.rs | 1285 | `46ed719fe149f644521e8e195a5b4f3395b51f261dc66dbe310b55f2f332f561` | 0 |
| crates/anvil/src/server/mod.rs | 3126 | `cd50016c1b6c9d9ceb7f9e7207057bc7e16a6690b87e2eb1ade9205c2e817db6` | 0 |
| crates/anvil/src/server/rpc_handlers.rs | 7459 | `4a830df3e78ed1fa0f625d5f64dbe2b92becc134d2fbf9b13f003d9f18c9eeb0` | 0 |
| crates/anvil/src/service.rs | 9901 | `f566316c5586dd9d282ccab5f361972f848f56702b010f59173298950b0b9979` | 0 |
| crates/anvil/src/shutdown.rs | 1084 | `e903baf7a9f0fe917b7733ad0a4de0474fff8b34b9e75043f722573556d75198` | 0 |
| crates/anvil/src/tasks/block_listener.rs | 3992 | `774b5d2ddb0850bde38b03becd5f99c732275e716392661198af585282e6f7dd` | 0 |
| crates/anvil/src/tasks/mod.rs | 6057 | `efb4a9bae45b3e77cfa265bcac4cb2aacd25acbc56dba3d38ddddb1855351654` | 0 |
| crates/cast/Cargo.toml | 4511 | `d782e29438e52280be002114069e8f72282bb6627cb8db0a669aa3fe23af2810` | 0 |
| crates/cast/bin/main.rs | 1258 | `c899a4a65fd42274255f348c662cfac3d5a35aa443b88fda140db7afe3c15f7b` | 0 |
| crates/cast/src/args.rs | 76897 | `ca07c14f047aa11d454c2b9a628ebe580a1a4da3c498b3b607620f811fce69fe` | 0 |
| crates/cast/src/base.rs | 13424 | `4ddce386d9788e1417b8a43d06cf750322d431bbdddb102c3bbe5ba9e88dd41c` | 0 |
| crates/cast/src/call_spec.rs | 16224 | `4da4189f65188f0382bf67cfc1898cea4ce7d2b2f58a69802f33a5a8c8f44b4a` | 0 |
| crates/cast/src/cmd/access_list.rs | 4915 | `711f0621ee72410c6972f704553c0ba2eab675219200b8a6cbfb5999e82443a7` | 0 |
| crates/cast/src/cmd/artifact.rs | 2041 | `a7940ee442f3039e74fc3461022cf81614391beea13dad384af3ee5b1b787911` | 0 |
| crates/cast/src/cmd/auth.rs | 3664 | `c5c2102fceb960bbcfe45eb5e07f38e0f084ed191631e63a392bc24c3dd37550` | 0 |
| crates/cast/src/cmd/b2e_payload.rs | 2194 | `2164c62c249e7bcde47326d8a729cd88baaaf0703620b33f0e1c67eec56bf5c5` | 0 |
| crates/cast/src/cmd/bal.rs | 1339 | `02a94cb796a43650f918ace12dbc272bca290606824979627b215dc2c84dbbbc` | 0 |
| crates/cast/src/cmd/batch_mktx.rs | 6097 | `cc6d971cb3547f706dd3fa3410bd65f25d30efac2e6b2876c619b3da121d359b` | 0 |
| crates/cast/src/cmd/batch_send.rs | 5917 | `bcd6480b143b0cfc12a934979f4bc80e2aec6c0e749f1c78742ffcab52615604` | 0 |
| crates/cast/src/cmd/bind.rs | 595 | `cd627115857297c0da60938f5aa82909958a1eebb4d6a2d48b7bcff95a5bd0d4` | 0 |
| crates/cast/src/cmd/call.rs | 41968 | `7111f45ebcb61b4732f8e4d9654130d6f3921561639e4dd752ac56678d5cf207` | 0 |
| crates/cast/src/cmd/call_overrides.rs | 8711 | `ce964e9ffa42d601cac00a7e14f6ab323c9a7880b9312ed33654ed3cb4e5add2` | 0 |
| crates/cast/src/cmd/constructor_args.rs | 1484 | `780584d3ffc6b210821ddcc41a3d80b1ac8e08aeb0d64115a6bc4eaf4c9c544c` | 0 |
| crates/cast/src/cmd/create2.rs | 20350 | `bac819f47cbdeeba4f46e5c215d9cde4c4e8fab71b586cd3f3ca96db65d8c26a` | 0 |
| crates/cast/src/cmd/creation_code.rs | 11427 | `062e8c967e136a5bdbd7e2ee29f421cf4ca55661ef8c984e8da659f79d63cd98` | 0 |
| crates/cast/src/cmd/da_estimate.rs | 2982 | `9e1cafc7caecf6fc2c65256875f9dfacb3865c0354399f9b8d9858926cc8638b` | 0 |
| crates/cast/src/cmd/erc20/permit.rs | 14413 | `0a02c7d223092c61b07876b9e025ca5875a71bf5a2233737681a33818b8185c6` | 0 |
| crates/cast/src/cmd/erc20.rs | 11822 | `10410c587cf31fc50fa233f108a757db70adb690f77a4c6a574c395d408ce7af` | 0 |
| crates/cast/src/cmd/erc4626.rs | 55984 | `cb89bfe514ccb60e5da588e679fa32c664bbd7828deb497c9ca362f5ed8be34c` | 0 |
| crates/cast/src/cmd/estimate.rs | 5046 | `f097a07634fbef9dbafb24dfc8f891fd3bc8c90dced13ac06c5d71c1443d6602` | 0 |
| crates/cast/src/cmd/events.rs | 15605 | `3aaaf2f27bbdd4e623448aa1d50a8bc86cce8b7ad5e059ac64f27191d3f0854c` | 0 |
| crates/cast/src/cmd/find_block.rs | 4893 | `353bb012783b0a4a669f89ab8ecd2f74fe17913f008ee20ba0c19e046c01fa0f` | 0 |
| crates/cast/src/cmd/interface.rs | 8232 | `d4d2aebeea5390405cfaf2c924354ef0599531fa8d6629d5f988d1573e8c8d4d` | 0 |
| crates/cast/src/cmd/keychain.rs | 147631 | `ea0a6cf003885ea9f33bdb910fcad4231fb733d4cb07b389d856539a8476b076` | 1 |
| crates/cast/src/cmd/logs.rs | 32986 | `4a7e71c0990d6d82d5ad82ded075ca669d582323f0732859f0111c6ca7c28ecf` | 0 |
| crates/cast/src/cmd/miner.rs | 1747 | `83e8468211c5c142cc17aa1d3ad14e3288bf045691cfd0073c546baa9367838a` | 0 |
| crates/cast/src/cmd/mktx.rs | 11339 | `945ad6e13691339dffb7be51b675a9f5e8e91185542ae7d9f7821ffb8d94748a` | 0 |
| crates/cast/src/cmd/mod.rs | 11327 | `f78e11f1ef40d488924811b4562752b19e15f08c8402758a700643140a409fab` | 0 |
| crates/cast/src/cmd/receive_policy.rs | 29539 | `6fa0ec3e9f663a778a1de5a1ba4bb3518f6f2d56614b16ca7533723228fbea55` | 0 |
| crates/cast/src/cmd/rpc.rs | 2663 | `3b96f4cec4c7feb778468f3dd973e18105720221c49ca4e5d93feb2a33a9eaa5` | 0 |
| crates/cast/src/cmd/run.rs | 52830 | `131d63bccf536a54157384968a26a94abc438d7c3dc998322600fcf74b11dc2f` | 0 |
| crates/cast/src/cmd/safe/contracts.rs | 2936 | `93ff9eb95612e4fea14d645215c618eb06c6fea32c3770b683c878a979d3a64a` | 0 |
| crates/cast/src/cmd/safe/delegates.rs | 4614 | `c99388a29bc88fd02651ccb628e3cbaabac27eb56ef28d0b30f885d794e5f363` | 0 |
| crates/cast/src/cmd/safe/deploy.rs | 6377 | `bf3959916b7453d9caa15e64c8debf3adab7f8ad74c57b3549bb6b73f216c9f4` | 0 |
| crates/cast/src/cmd/safe/execute.rs | 5185 | `4b9b419d579f95daafd4e776a067b10a6219021ea6687ed9dfaf064f61ebfe5d` | 0 |
| crates/cast/src/cmd/safe/mod.rs | 2863 | `aba35d47972bfc763aa3f89ca440c89cb4bc595f7b85e63c71c775c9492b568b` | 0 |
| crates/cast/src/cmd/safe/proposal.rs | 5637 | `7a50024bd2a291073f1291d94aef1afec2cf5e555383ffc292cf67859add6e66` | 0 |
| crates/cast/src/cmd/safe/service.rs | 25692 | `7d1c5a315a47f406b05f6fc4f7776260f215d73f06dd1927fdd4751d17693da8` | 0 |
| crates/cast/src/cmd/safe/signing.rs | 3965 | `a3992ac2b62bfa903d1d252f40388c7585e948ab0937cc6c5dba19ab10a4c5bb` | 0 |
| crates/cast/src/cmd/safe/simulate.rs | 4983 | `df8209dec6a30eaf2c8b416c2b6ee3dab9fb18d8a1c7dba39e68e6b91f0f1129` | 0 |
| crates/cast/src/cmd/safe/transaction.rs | 5376 | `36d7952f468e679f72b560c3272050dffb6d23678530fdc2058dfac7b99be022` | 0 |
| crates/cast/src/cmd/send.rs | 28845 | `297e1b3886e561c598acd49ab55216efe295b13e5b2ce02194fe6180f0edd064` | 0 |
| crates/cast/src/cmd/storage.rs | 31224 | `7efd4535605a6ab3ee6e31a77eb43822cc78b2c331121a0fac648be664bae1ce` | 0 |
| crates/cast/src/cmd/storage_credits.rs | 6818 | `010043901ef1936cdc66bc4cc3375019c86a5674bca67120400efdb81d52683d` | 0 |
| crates/cast/src/cmd/tempo/zone/abi.rs | 2437 | `5ab4bcad72b7f804f0754cc8dfe350752fe46891a4c91eade8032e0ad84ab908` | 0 |
| crates/cast/src/cmd/tempo/zone/auth.rs | 2881 | `ef249ddc1ce411691a05416e2659cb979f2bafd2d154032a1eeaa57f55c74c31` | 0 |
| crates/cast/src/cmd/tempo/zone/earn.rs | 9842 | `51760e61efd583a3849f9962a84a5617f212cbee62a8ca90355e01b71e9a5fb0` | 0 |
| crates/cast/src/cmd/tempo/zone/encryption.rs | 5890 | `d326aa419e0cb53c2f23d07643bb792dc029b82b750a17f24beb265c3d8ae82e` | 0 |
| crates/cast/src/cmd/tempo/zone/l1.rs | 10500 | `e03ce5109285eed7fd0f3fc7e94d5319327daba5a180ac1f23c5efbe31edf734` | 0 |
| crates/cast/src/cmd/tempo/zone/mod.rs | 15457 | `3534969a0c0a712a3fb5e627499da2fc24f9dd4b0f868f43e9356e4e92125a57` | 0 |
| crates/cast/src/cmd/tempo.rs | 3705 | `84305c59dc4af281ebce79b80f3c0cc88b2cbc26f492cadc475b7506b83530a4` | 0 |
| crates/cast/src/cmd/tempo_policy_args.rs | 11137 | `7e387203b06d5b81eea31a2671f93ae76d6d4313a2d31f9158cd258bcc24820b` | 0 |
| crates/cast/src/cmd/tip20/create.rs | 4118 | `65b045ea40bd4057bf53a5f9cdb684fe0528b51f57b68a9eb4bd4a684a2b7370` | 0 |
| crates/cast/src/cmd/tip20/logo.rs | 1368 | `aa5dfc587af46b8e36f2b761f052bcf46dab3929abd2530c822690dd63fa863d` | 0 |
| crates/cast/src/cmd/tip20/mine.rs | 10254 | `c3986528bbb6d9ab0c7e73d01109a25e749ef44dcc8fa821fb0c44ba8815ca77` | 0 |
| crates/cast/src/cmd/tip20/mod.rs | 9198 | `2afc1175160a1a8ee57430c2813a06165fb0b446ed157f3c09d4119afafe18db` | 0 |
| crates/cast/src/cmd/tip20/role.rs | 6822 | `cc9ca00923bb117332f4a9b7d36cced88505b28cd0b0fd4c864f4cadc05465b9` | 0 |
| crates/cast/src/cmd/tip403.rs | 9659 | `bc8b54de61399a26633b8dfea9b7b434a380fe361499f696c3d1c5f890a914e2` | 0 |
| crates/cast/src/cmd/trace.rs | 2780 | `f1453574b91808ec29f31456ae12d83170a136aca1cbcc08ff55b0370b316601` | 0 |
| crates/cast/src/cmd/txpool.rs | 1704 | `11a618cfcf1044cc426af3829c67ed0185d353960203ab310c75b5fffaafbf24` | 0 |
| crates/cast/src/cmd/vaddr/create.rs | 2808 | `4a1ab984248debabd86804e05b9806ae7d38c1572374ee507eb1d03d76a5c644` | 0 |
| crates/cast/src/cmd/vaddr/mod.rs | 4235 | `0559cdbcb8e57b7601393da83ca407844bfa9d20ec1350eea709fd355d04548c` | 0 |
| crates/cast/src/cmd/vaddr/resolve.rs | 1325 | `d5f007ce17ce054306f1f4dba6fb966aaaebc6160e4b49c34a5e6b3279749b34` | 0 |
| crates/cast/src/cmd/vaddr/watch.rs | 3649 | `feac4ac65c513306906c87edcaa6d7eaad8252cf48f26301618c307eab3eed04` | 0 |
| crates/cast/src/cmd/wallet/list.rs | 6619 | `c63d8fa74bab3ddaf186bf2331b7d0258076cc256991c670dd964770da6072a5` | 0 |
| crates/cast/src/cmd/wallet/mod.rs | 65440 | `00cd702b56ae34933622d9ef9099819e7d30b88ec6b5b21bd34f9cad7fa9939e` | 0 |
| crates/cast/src/cmd/wallet/process_tree.rs | 7189 | `add4c4c6f5cab22756d71aa5f11fbac6ce89646c9232c8720a4f5cc685d441b9` | 0 |
| crates/cast/src/cmd/wallet/session.rs | 31378 | `c3188c54b1a6450371cbaf861c6a6276a819df7d05201c73aae0393e9baf7ea1` | 0 |
| crates/cast/src/cmd/wallet/touch_id.rs | 6711 | `0e7c7e9e14198c946c689c7586fe13b05cad4b3d0dd076f6987dad5e39cd8cc1` | 0 |
| crates/cast/src/cmd/wallet/vanity.rs | 10646 | `78c7fdc443faef5de0125503e95260dce53e7f5e8cea7f0cf556e8af1beb8d56` | 0 |
| crates/cast/src/debug.rs | 6721 | `8e5849a28a0394a30b8ab698b5284b699a548540a137fc25ab2ff751530de24d` | 0 |
| crates/cast/src/evm_version.rs | 7661 | `907d63b089df1ad88d39b4b085d9f35694ecee1c8c5835cacb286b7111d45c7b` | 0 |
| crates/cast/src/lib.rs | 564 | `319c0e3215220d906f50567d6feb72266333ca9bf12defdafb764c4e423b996b` | 0 |
| crates/cast/src/opts.rs | 51453 | `e2ba447ed8d7cede05fb23b5135b0ebcce40f7ae98859d46f8b4e72c8dbbc904` | 0 |
| crates/cast/src/rlp_converter.rs | 8028 | `fc844cdf7804ebca1dedf27ee0fadf7acc5458c3ae8f689c5db07b23aab8334e` | 0 |
| crates/cast/src/rpc_trace.rs | 20594 | `57af9d945d108bde5ee71a505a71f7b7c2fc69fcefa11117790590f7f7e7a40f` | 0 |
| crates/cast/src/tempo.rs | 12852 | `40e6c23fa579c0c2b6c0c9b4d10f03cde212d852fb28f552503bec610c535c63` | 0 |
| crates/cast/src/tx.rs | 42221 | `7acba5cda85a202d2dc0b8d03bff7361ac20f76bbf9972f8a52b4d41c54462d6` | 0 |
| crates/cheatcodes/Cargo.toml | 2699 | `15e048af18214cacfd79b38b4e6b6f4b68b01da40346bcbdbe78900576c8b3d0` | 0 |
| crates/cheatcodes/src/base64.rs | 932 | `76dc8360106c4702ec24d3d13a87944b27d73be6fb4416367fd54a049583b5e1` | 0 |
| crates/cheatcodes/src/config.rs | 16488 | `9f8bde8f6240599647ff268698226d9e4a87e79d810e7eba523526b28d92f2bb` | 0 |
| crates/cheatcodes/src/crypto.rs | 42870 | `194dec89b94c09b4f26b174039af33c90fbf98af1e25231f61d6578c4f68a73e` | 0 |
| crates/cheatcodes/src/env.rs | 12371 | `2218b98ee5bb8aa766834e76e60291566d043b963eb35aee932182fd917dfd52` | 0 |
| crates/cheatcodes/src/error.rs | 9026 | `c181922ad0f3e4d3be9338e219cf23d17a29f21236fa565ba54530a27af735c9` | 0 |
| crates/cheatcodes/src/evm/fork.rs | 24858 | `21abacd1ec20d2bcf1d1894f6bdb32a4ebf1b1ff6dc67af97dc3b29857ac2006` | 0 |
| crates/cheatcodes/src/evm/mapping.rs | 2414 | `0cac4b7bd9771d48e6afc2685cbc3a5fc0480f82109ef4ad22cffeca986560aa` | 0 |
| crates/cheatcodes/src/evm/mock.rs | 12035 | `1ffbf33788161d3638fc8eb046828bcba650bd2eb151f045c7a01916906cf2a3` | 0 |
| crates/cheatcodes/src/evm/prank.rs | 8121 | `37ea89631b241377ba3342f99f7b21ec6eda7b2b91629bf83e354e654708b4cd` | 0 |
| crates/cheatcodes/src/evm/record_debug_step.rs | 6045 | `f7c9e16a101d1352ce124375734f9960a65bb9794bb1682eb65634b35fbda3f6` | 0 |
| crates/cheatcodes/src/evm.rs | 100856 | `0af2787598ba83b4573effcab5a13cd919cb8f1a357c945e5650fe1178d58ea3` | 0 |
| crates/cheatcodes/src/expected_emit.rs | 39131 | `947622bbe4aecb0379bcc97b6ed48ca6abd6d4407729ba74a4757c2cea61a479` | 0 |
| crates/cheatcodes/src/external_storage.rs | 3300 | `d891e5f55f6778328ebb31b3ac5dee2ccda255c2cabd6fd5a14655947ea9081b` | 0 |
| crates/cheatcodes/src/fs.rs | 65434 | `ec82c8a9ad24a7131dbc95463e9dbe679aef826ee98ac7cec4ff28040d0ff551` | 0 |
| crates/cheatcodes/src/inspector/analysis.rs | 6331 | `04b4fbbbdb1a01d8361b1e6b62ddbd897f9cb73d814a4792e6c71b96b429241e` | 0 |
| crates/cheatcodes/src/inspector/env_overrides.rs | 13056 | `5508036f0c5ff183e841eb0b080324efac9916f53a7e6fd9171d094423483d16` | 0 |
| crates/cheatcodes/src/inspector/utils.rs | 2394 | `acbdc5355e2c66a7b14c042842281448216dd4c5ff974077f823d30776e0f04e` | 0 |
| crates/cheatcodes/src/inspector.rs | 169792 | `ec08c2c28e80041c877312283085a630206dc19f57ab9e54115d6caa9ae91dc7` | 0 |
| crates/cheatcodes/src/json.rs | 52852 | `fb51bf4aa7a5a11424c56ea455485f5553ae548792b93048c1361a23fb88a5e5` | 0 |
| crates/cheatcodes/src/lib.rs | 7224 | `f7f77e10a95d9f1c67b2c242a36eeb71616536c381c6f7f096ea9edc765cdd0d` | 0 |
| crates/cheatcodes/src/monad.rs | 8225 | `538f2016e405f4f145de5e5637a1bce2bfcbf30f633a57dfeaffb50cc943072f` | 0 |
| crates/cheatcodes/src/script.rs | 15171 | `56c227f65be736706e18982da94b641a6e42da452a013c02b86baf2f7de5238b` | 0 |
| crates/cheatcodes/src/state.rs | 6447 | `4c71313a5e8067467a7ec7d250710170d088f5d21000a9c9faf891bbef26a1a2` | 0 |
| crates/cheatcodes/src/string.rs | 5668 | `d6289a588e6523050cd8b62c684c3e538f7b08c75d6e3544797450dfd9ffbd61` | 0 |
| crates/cheatcodes/src/tempo.rs | 1748 | `2e06f8e8f04fd59f83684095c1cc73bf1308ed1b71c1155fda29f811fd451203` | 0 |
| crates/cheatcodes/src/toml.rs | 21387 | `4c5b7594e077e1849db4b330d7fe96a24c6535883cbdbb744c6edb5fb2da01d1` | 3 |
| crates/cheatcodes/src/utils.rs | 17749 | `40722217d33710ceeac5e80a3fdf0f9dcb867619191f907a38b11bdf78fcac48` | 0 |
| crates/cheatcodes/src/version.rs | 3928 | `df73cbd40611058a68d04f9a5ff359b0eef8d67a38b478381107f25a251fe201` | 0 |
| crates/chisel/Cargo.toml | 2052 | `a0caf8e4933f815395de271aa93c7fe4b9856a3a01b3606094d270a529078825` | 0 |
| crates/chisel/bin/main.rs | 332 | `bd76e4de788611712a1a0485abc5e3252a3604043524fb94e72032e5f106f3a4` | 0 |
| crates/chisel/src/args.rs | 12034 | `e2cf567661b5c135782d969e3e530e3f73e6abb5264eba713659e6b05997fe26` | 0 |
| crates/chisel/src/cmd.rs | 5907 | `0de6ff36a9f9c7729b1d62c9b1a9963ada4133e174c7103d6fa8c6aee3e4d8d6` | 0 |
| crates/chisel/src/dispatcher.rs | 38308 | `b88d3679c0a7487cbf742f3d5cd2d34264a1f1a75d7fc44922fce5617f7a36e2` | 0 |
| crates/chisel/src/executor.rs | 43835 | `2c1f4e32b938186a3af312114dbc3ab1e54e932e4549381725c0c982da5afec2` | 0 |
| crates/chisel/src/lib.rs | 555 | `851168e414b5b8bba5d8f65a39ef1a7a3cf4179d435a643cb51fd68617f19efa` | 0 |
| crates/chisel/src/opts.rs | 2286 | `4a08fda55eb8e742059659c9e1dc8b58c87c2b527b92b19720134febba04769a` | 0 |
| crates/chisel/src/runner.rs | 3656 | `74d492d483d7c4809f8f2d12c31ce989fc48c3c2d151f7655ae999d5367fac2b` | 0 |
| crates/chisel/src/session.rs | 35471 | `c8e6b667f7764edbead6f820cbfc7b9530736061dc2910c77ebb6ec1d5232e11` | 0 |
| crates/chisel/src/solidity_helper.rs | 11593 | `c0d10afac440fa805d69d6e7e2f4a1028df44d203664b7a579d7c71b18477998` | 0 |
| crates/chisel/src/source.rs | 46688 | `98c1e3348a506b5de0b085605e4cd63f7f3b35584578fac3339fc999af5e7721` | 0 |
| crates/cli/Cargo.toml | 2509 | `6e26830fa7cf2ae6141c4cd678be7adc2c5a627b440596125f8992f2ff4582e4` | 0 |
| crates/cli/src/clap.rs | 1397 | `6fd145a77df4c1c4966294cb381ee37b25d630236d5a79566abd94ec6b00b829` | 0 |
| crates/cli/src/handler.rs | 2970 | `2d72596a0633cdc60b7a96f50496e794cdd68157acf605b184fb40d5f588abee` | 0 |
| crates/cli/src/install.rs | 33735 | `6cbadff479689732774b7e82fd2ac5fe104f3e7ddc7deeac2ba6dbda0c9d4eb5` | 0 |
| crates/cli/src/json.rs | 10876 | `f3473648415e2acbb634eae2fbe467292f16669ed9aeb78fb865980fa0877ab7` | 0 |
| crates/cli/src/lib.rs | 407 | `61dd319d9a2285fdeb24aae11eb73c783ad6fb48e35639b4cc4245c56ce30c63` | 0 |
| crates/cli/src/lockfile.rs | 22585 | `d8864832913621a7f74c13023c4c7210c3636e884e5ee32dddf5bd07d81b5e49` | 0 |
| crates/cli/src/opts/chain.rs | 1408 | `1f89504ee9f34eff36b6503ee9e1aa1d9e54431bdc982d86f2b6ae78aaebcf12` | 0 |
| crates/cli/src/opts/dependency.rs | 15429 | `997dd54fcc14c8c63522f2db94fd7eb9bba830f4758b3970fd6fd59342c61c9e` | 0 |
| crates/cli/src/opts/evm.rs | 20516 | `d925ca5d687dc2a0d8f7a7cdb76a2874a83534b89c80589227a3f0049d201b25` | 0 |
| crates/cli/src/opts/global.rs | 5741 | `61a64023b98152bdba617bde32bfb3574e617c38c1bcb0aec89ad5a1d7a49c6c` | 0 |
| crates/cli/src/opts/mod.rs | 321 | `5b286e48d0e12db1b03808a65ec4d2474fd5ad53ca7111633e50f93a3bfe2a10` | 0 |
| crates/cli/src/opts/rpc.rs | 9036 | `80c432665d0166b324673fbbea56dc9152630175d11f957876b98fd1c050f588` | 0 |
| crates/cli/src/opts/rpc_common.rs | 4510 | `015e34b778b445339ec59a78546bbd8e04249224c446818b6457d2cc9fb40dac` | 0 |
| crates/cli/src/opts/tempo/session.rs | 16768 | `8b6c5f40bfeb15e73bc73307a6c2c007d55a5abe67eaf7350b1975982102aceb` | 0 |
| crates/cli/src/opts/tempo.rs | 20485 | `674cbd3ef8b8fa658be12349ba241195472f72ac7775c405bf1db488a344379a` | 0 |
| crates/cli/src/opts/tracing.rs | 5457 | `52b337f47c04f2f486f6c83c9b43c86c5ff8aa7748e041cf2a4dac0e7c0fed7a` | 0 |
| crates/cli/src/opts/transaction.rs | 5225 | `7d42a9bee15422d872c4e4b3002913bf3d0fd7c5027188c59964b8d62f39548a` | 0 |
| crates/cli/src/utils/abi.rs | 2565 | `1e598a53aa3c73cb0cce60f467181c37c42296ebe7b23b5aa7bc0020a884ff21` | 0 |
| crates/cli/src/utils/allocator.rs | 1275 | `de46048af5ddae82d7d8cc5dc1a899e6102aaa641d6d5f72cce86b998325e1a0` | 0 |
| crates/cli/src/utils/cmd.rs | 17216 | `cd833dfabb9235641dcef0d47d6a1de9dde82e7b0a28e7987b46215ce56964da` | 0 |
| crates/cli/src/utils/mod.rs | 59134 | `0784360683f1c5dcc8fe0cc9fb581d1761f3bb6baa9df157d849695cd49235dc` | 0 |
| crates/cli/src/utils/suggestions.rs | 1471 | `b20278c3806021a5b013e799d8545546374333ff0fc787305616b31221e0396f` | 0 |
| crates/cli/src/utils/tempo.rs | 8697 | `15a82cc4b43725650fa92d37580f039132daad4b8682113678eae87b41a9a387` | 0 |
| crates/cli-markdown/Cargo.toml | 465 | `5dc57e7ff5b7ae9c1caf938df1b551878ec67ceb74ab5e7c2bb4a8f881919c58` | 0 |
| crates/cli-markdown/src/lib.rs | 18718 | `f0296ed3066add3bdcdea489a4d9b50964707efeaff93b24a98fa468990462a7` | 0 |
| crates/common/Cargo.toml | 3294 | `7e2925e1957925ea894da1472118155a5ca4c5bdd6788d6a69080007bf7814d0` | 0 |
| crates/common/build.rs | 4046 | `888378e236140116b10efa7d5be3a82a9c89f22b955f9091bacb051d663dfcdf` | 0 |
| crates/common/fmt/Cargo.toml | 1348 | `aec0ad33f396623ffde835f84eaf4322dd66b652ae807c0b91878127a8b799fd` | 0 |
| crates/common/fmt/src/console.rs | 28595 | `74f4433676adcc2ada6d8d9156d43f821040d64d2f920f6fe3e0589cf6229bc8` | 0 |
| crates/common/fmt/src/dynamic.rs | 16550 | `0dee13518c6ff0bcb0190e5e4f22e8d1beeee7373609825d22a919ea17d6b535` | 0 |
| crates/common/fmt/src/exp.rs | 3930 | `17ccee7249d7d75450eb2a04c44edf7ba5ad4b1221313cd7fbfdb47ef6dbd5d7` | 0 |
| crates/common/fmt/src/lib.rs | 622 | `eb2ca61579fb6ffb4fe2e50ba6e3c988f0a50c1c11501b11dfaa391f2e14add3` | 0 |
| crates/common/fmt/src/ui.rs | 85593 | `ca99ae4073de7a36c4fc534261429c5540c0b5902d5e6c3afe6fc822818b3ab2` | 8 |
| crates/common/src/abi.rs | 17108 | `3d628ccd6a2e075e0e24b09eff061422312108c318cda0a4d5864301b78b78d5` | 0 |
| crates/common/src/calc.rs | 1470 | `c40fedce9c98a637be0591c7f0a49a633eb4088742faf7b054fa1e8c9c66d5f9` | 0 |
| crates/common/src/comments/comment.rs | 1859 | `4537adf9db7b2cbacb439b6eec5bbd4d3c8e3106016a45f804d74cfd3fc6e8b6` | 0 |
| crates/common/src/comments/inline_config.rs | 19803 | `0f67fe3702517cb27fd12f060c4a776f6619d5c960db484c9eb51a9ae8b560fd` | 0 |
| crates/common/src/comments/mod.rs | 18615 | `6f092958487c6d34eca008a3ebcbb879272d47c92ed296d8f6c6d91726ffe8fa` | 0 |
| crates/common/src/compile.rs | 43606 | `96729aaf02f8bdd06bd67075cd57165e1867c9a6e1240192c1d529ef917076f9` | 0 |
| crates/common/src/constants.rs | 4081 | `35acb8be671e776e8ecb7a361b788232d4f7ce684600050b1c50b9c5f96167c6` | 0 |
| crates/common/src/contracts.rs | 38390 | `2c9b0cb4a123d5287e761b0356aba518f5355baeea14f6c7de163dcc3a89aee6` | 0 |
| crates/common/src/errors/fs.rs | 6290 | `0452b64ce065d05c14a16f8d25f6e8abf8ac8a29c9844dfbb0244e22c55804c7` | 0 |
| crates/common/src/errors/mod.rs | 3721 | `fd3c2247f5f02af0d856ba6559bfcd03797d9fb850282043f8029815ee6b519e` | 0 |
| crates/common/src/external_compiler.rs | 31519 | `d72b4af15251e81bbf777df644620071ab04c3207272996d50bb5d9f56ff5e19` | 0 |
| crates/common/src/external_storage.rs | 29161 | `87948be050a3ae1f3da96af73ed3efe06efc0788d7ac54f36f81aa44454fc962` | 0 |
| crates/common/src/fs.rs | 13261 | `3c988ff90ed09d8410eb66d97923889bb51258c07e225fc479db756f7491bafd` | 0 |
| crates/common/src/io/macros.rs | 9359 | `0d3b861fd09eb5534da3422d3ee09a7a3b0bad9585ee27ff48865e8fb3b0d615` | 0 |
| crates/common/src/io/mod.rs | 179 | `8231147184ebb1a6986329f6e5e91b485ae6f449ce8aed6d75e05f0247b323a7` | 0 |
| crates/common/src/io/shell.rs | 18344 | `9f1e2a25b02bfe98850188a45e3ba632fbf44aef2a682a4fbf66131fe9461eaa` | 0 |
| crates/common/src/io/stdin.rs | 3102 | `46aacd78bc9718f5540ff4547a60e634099283b0078fa6488b2e3aea41f252e8` | 0 |
| crates/common/src/io/style.rs | 197 | `6ebea7b8deae70cf989be62924745e27aa6907456033b8286aca5d13298fa99e` | 0 |
| crates/common/src/iter.rs | 752 | `67f752a8d8ba6f4a9666c03d58ad685b59c2ca33746dbf189b1656d43dddc154` | 0 |
| crates/common/src/lib.rs | 1038 | `3c8d9ced1b66458bc9608901da2595c4ab17005cf23c92b78657904b5140ca4f` | 0 |
| crates/common/src/mapping_slots.rs | 5660 | `abfe9cb33326fe2974391a108c36b81565e944c942faba4ec8ce4e9c56187f80` | 0 |
| crates/common/src/preprocessor/data.rs | 12259 | `deaacf710ce48081c04cd552cbaf9cd35a323e05666d79c84136e386f534fd98` | 0 |
| crates/common/src/preprocessor/deps.rs | 54776 | `ab813378177d3b865edc610f758e3ab7a8421bb75fb524eddccc0fd40122adf4` | 0 |
| crates/common/src/preprocessor/mod.rs | 41515 | `077b6d20d5266dea039ad6ef943b811d8005a19905ed9579f18969e136c45d93` | 0 |
| crates/common/src/provider/curl_transport.rs | 7306 | `46e0adea2cc55df8a13e4010348c24de57fb52ab7faac7c34105725dc18eb6c9` | 1 |
| crates/common/src/provider/fee.rs | 14527 | `f63c6fe33714e9322bb130d5cfbe209b936d8d36d117a8c0728faa77e5f86b74` | 0 |
| crates/common/src/provider/mod.rs | 24093 | `031a525fb4587c3bd5f16fa277f0764ad649759149fbfaa03ba65182f5eb5b72` | 0 |
| crates/common/src/provider/mpp/mod.rs | 184 | `05f3cd3f2f0bc5a5dc9864255bad9d252706b2e238498b7d17544e49d1d9311b` | 0 |
| crates/common/src/provider/mpp/transport.rs | 25412 | `9e3d5860f0ffb40d7133993e2884102ca18bebb1c29bfb1015bca63aa78067e3` | 0 |
| crates/common/src/provider/runtime_transport.rs | 24498 | `8ca3597f92d18f9e5f4527210bc8f1bee08d61015153c7ff57024d06972a1d4a` | 0 |
| crates/common/src/retry.rs | 3711 | `7a9719bce03410ef07c2c94c996f00d925d95f21383480019ed80bcd1081cb79` | 0 |
| crates/common/src/selectors.rs | 28610 | `09c3440253000c9022ee1eec348480e875c48717b57349ecd3b9e054526bdcb3` | 0 |
| crates/common/src/serde_helpers.rs | 6880 | `c522f2404d28d499ba57daa334394551f022bd51fc29a4db01b303f889a4d96e` | 0 |
| crates/common/src/slot_identifier.rs | 41543 | `8407356b41b000b2c86385b18099afe65b2695fc8efeb3bbeb3f33bf2e2c218b` | 0 |
| crates/common/src/tempo/auth.rs | 24956 | `78b112c3b9d632766a958b36ed9117f1a1d2f94600bd20264f2821750433af6f` | 0 |
| crates/common/src/tempo/hardfork.rs | 7494 | `01deef067a93613ebfd79c0450ae31bdc3faf6d95f4afbffbbfda536d3c11f87` | 0 |
| crates/common/src/tempo/keystore.rs | 5486 | `027c781cceb54ee0d78b7105733e83d780c0c10adfaccb8c3f9db977d383d743` | 0 |
| crates/common/src/tempo/lane.rs | 4931 | `134543a557720bf58317e738945158ff8c389a0530380b472a9e79a6f2376a5e` | 0 |
| crates/common/src/tempo/mod.rs | 16752 | `098f00b035d1df4150ff0bbfb23f17503228213b4b543f59fc750efbb4969254` | 0 |
| crates/common/src/tempo/session.rs | 15232 | `59453fcff95b4f79b622c1d88d9979efba6319feafb0de982d4f24cc73aad95b` | 0 |
| crates/common/src/tempo/session_policy.rs | 18659 | `579b5cd281f1e8132c14b18d683e61f2d780e54a3c6098c76de980c6293c503d` | 0 |
| crates/common/src/tempo/tip20.rs | 3097 | `772dc61557ee6392da102b7950f5f1d9013c14c0bd5872803c6da6b65421362b` | 0 |
| crates/common/src/term.rs | 9640 | `a8e6d6649a55519987a1cb053961ba2d840f865c790b5f84ae514498bb61ab88` | 0 |
| crates/common/src/traits.rs | 11258 | `028eed88b71434544d7f8387c1e6a0baf676222b5ab1247df9cf4fe396957f83` | 0 |
| crates/common/src/transactions/broadcast.rs | 4033 | `e9944e6ef3923ee5b2683b451cf3db0d850b8274c6e89d3a36b7e862440318a2` | 0 |
| crates/common/src/transactions/builder.rs | 19724 | `892516b589cb84fb786fc2e2ad1a701ab7f1ff1e045128952b635195c734085d` | 0 |
| crates/common/src/transactions/mod.rs | 136 | `247f348e0d8747454ffe9b5e65921701d154a6a7c1a3f7d006ce93aac92adde3` | 0 |
| crates/common/src/transactions/receipt.rs | 5903 | `0f1bdfe87f2dd763396023ba0927c871ec9bc32b8295ca95f277e491eb31b066` | 0 |
| crates/common/src/utils.rs | 4640 | `7230d7e8d215ae108d0ec405f004dd08408fb935ca77ed325383afe760c453dc` | 0 |
| crates/common/src/version.rs | 1074 | `31083bb8f494e7ed9ad60fb1e7b201e534e536379ea51cf985ec5948607d76d3` | 0 |
| crates/common/src/wallet.rs | 6229 | `14be0fd7b850f9c83711e5dfe4f2b9c6d9567d67d92d9a703337e6fd6989956a` | 0 |
| crates/config/Cargo.toml | 1805 | `b8bb5fbe738bc66c7d3f6d3a8809388203f1607213523c260b982dfd2c1c14b4` | 0 |
| crates/config/src/bind_json.rs | 781 | `ab6230c83c09c55a731f158e2190776c53954616d0632916fb66c7df8942a1bd` | 0 |
| crates/config/src/cache.rs | 9578 | `a8ce09eae18fe3201e932ccde05d285c3de05aa0c03df2ec643a3171282c049d` | 0 |
| crates/config/src/compilation.rs | 5944 | `efe26679be5644b0c10d011125961e45929f13eb08c433aefb9034a76a01e30f` | 0 |
| crates/config/src/coverage.rs | 6448 | `4574ba9d3f49b09be23485dc4ce1b574ea4997607b3a227b1aec29685d885355` | 0 |
| crates/config/src/doc.rs | 1655 | `44325362089fce7cca28ab0e3a3a909cb9399800a7b40a345db224c6d8735303` | 0 |
| crates/config/src/endpoints.rs | 20772 | `baead2a113a3ca4332290f7fbe426dffe359f3e1d7bc59feb3954b7c00d4c8e4` | 0 |
| crates/config/src/error.rs | 11894 | `d7594efc7edf6d159757351a3fafce4834299d9a6b7241f2bfb35fcd9152b31f` | 0 |
| crates/config/src/etherscan.rs | 20877 | `3b19f5179363a03833b6ca081a702f1c807aefc262ef9736067058ef6bf1aaf7` | 0 |
| crates/config/src/extend.rs | 2339 | `b9449078d85a98d8ac3931c0bbf1a21343fbff65dd468926ef86e71af7ab46e5` | 0 |
| crates/config/src/external_compiler.rs | 830 | `7e7b6ecf3a4bb7a387d67ef325795c14e64ed2d1c4dccc1053190e56b30ff779` | 0 |
| crates/config/src/fee.rs | 2755 | `99910c1c68beaa257721865286d8b981a06101584b6acfd77d97f4b20b495a2e` | 0 |
| crates/config/src/filter.rs | 9547 | `b0c25688804a531cc563fd511e588c6935f3c1a7bf25ecb4777f37e00e02f877` | 0 |
| crates/config/src/fix.rs | 10282 | `72960352eb2f0a9fdd91837aaa247413e9b38eb4c38e25450a165fe598293f70` | 0 |
| crates/config/src/fmt.rs | 8905 | `bcd3e8389c2b7cf7021c2065ef99c9e9e3da4f6e4e552846dae752e571e38c76` | 0 |
| crates/config/src/fs_permissions.rs | 11328 | `57d783b0c6b46f9307004344c4e4afc2a5be0996cb429304782a33f23db5b9ec` | 0 |
| crates/config/src/fuzz.rs | 12512 | `d8b0b42ae07292385d06f679806d2bf3d20507d188235b085e19fdee7c667687` | 0 |
| crates/config/src/inline/mod.rs | 16708 | `76203e70ae8a1d50ea77d640e080a19e86ffbb6cdcff393e3d76c0abeb648d87` | 0 |
| crates/config/src/inline/natspec.rs | 34114 | `130bca638405bdff8bc99aa997d82dcf1f3f045e9dddedbfa6d9d99433ab6d93` | 0 |
| crates/config/src/invariant.rs | 10269 | `e0369b4b6ff5909cc7491201b66f76c99ca756641fe796bc94cdae0c2b2bbdc2` | 0 |
| crates/config/src/lib.rs | 347281 | `b88e5285452e8ddf089b2e82ca4b72e257b5442524358cb0fb243c8fa26876e5` | 1 |
| crates/config/src/lint.rs | 6588 | `72d8a269f9f84251d61ba7bf773d0cde23b56c361be223e45523fe693565881b` | 0 |
| crates/config/src/macros.rs | 6610 | `1489c4c811077583e4a2add9273cc96d98b0480c541821eb477b42c4c8192dbd` | 0 |
| crates/config/src/mutation.rs | 2964 | `4b08112ce1133fb8cb60eaa41bcead03bd6dff3a79754089a188976d6ce4ad6c` | 0 |
| crates/config/src/providers/ext.rs | 34588 | `7280decbe19fbf823c480f92e539ae515cc8bfa174d57d0776f486644a4233e9` | 0 |
| crates/config/src/providers/mod.rs | 124 | `5d70580a3fcf51c87f3e714098c1cb9b6924d383509e82e8cceb59f752b4c3ee` | 0 |
| crates/config/src/providers/remappings.rs | 51144 | `e3ca809cab8577f194dab53a6d0dc17c5a498702652cb46c23e1a4eb86f1988e` | 0 |
| crates/config/src/providers/warnings.rs | 16698 | `54596a58f822c8d2d8e78b50027a49551d614cc60038d8ec2ad9ce1d7e721f0e` | 0 |
| crates/config/src/resolve.rs | 2899 | `345d0d2af1784b818212716cf905ff344007d1ebed98fa0b6dc73d53362233ac` | 0 |
| crates/config/src/soldeer.rs | 1989 | `1375b2184c062ae55c7458879cb797c2d26bfe9f0d08f474aeb3fcb6dba44948` | 0 |
| crates/config/src/symbolic.rs | 8571 | `c568c872e7bcbf01b88830313abcd09f1538a0526c72e5818b89fba86fc9d752` | 0 |
| crates/config/src/trace.rs | 1451 | `2f11fb046030ddafaaa39078199570f9a0d5ed63ad097aad112ac140708e06ab` | 0 |
| crates/config/src/utils.rs | 13610 | `668399c586c08a7b6c8728e0812346d9807cb02bd19f0e4129b72ded60da324b` | 0 |
| crates/config/src/vyper.rs | 1565 | `ab343ea8a5d71657b574ddaa75a7cc2dda73d73f357fb45073b3b3e5091cff5e` | 0 |
| crates/config/src/warning.rs | 5042 | `494525d4d9d1f5854b41b7a4bf93a35731a97933e6010f10dcf65944ba28a031` | 0 |
| crates/debugger/Cargo.toml | 967 | `dbf8fba9ff7d7f1f26e9a504be9d7c00f2af5d24f65acac6433d1e1849d28a93` | 0 |
| crates/debugger/src/builder.rs | 10487 | `3d6e4ff0ab94a4ce0b7f3398a76545b8220456b26fe37f709a9baf01e7df2575` | 0 |
| crates/debugger/src/debugger.rs | 6171 | `582be2f42b813dfca3682fc28eed787312b3a47bf1326fd19d47526a5e193d18` | 0 |
| crates/debugger/src/dump.rs | 4244 | `8e5d0c599c2e3641c6715b20cd395b65924c6fb924f6855e216f62ffccb146ed` | 0 |
| crates/debugger/src/lib.rs | 477 | `73cbac7ec9a2f8f43db5505b8ed8377036e68605cf573bc1ab47f06a565ee388` | 0 |
| crates/debugger/src/node.rs | 23798 | `faf733e62eb7e172582bd2e1704c5c14e6f066303ba39567516cf0ec110a86ff` | 0 |
| crates/debugger/src/op.rs | 8495 | `f8a93af3eecdc7df79138570044c6c4f164756268ffce2916412723a7f99f99d` | 0 |
| crates/debugger/src/tui/context.rs | 116629 | `a8dbaa04d3e376a44e4b0170713d6214680457f851c5e36481a6c6bc52c6ae0b` | 0 |
| crates/debugger/src/tui/draw.rs | 88642 | `0895fa146cc2272c4bfc74fc684d3dcec3e3e83b92d442e951c26a0791c80be4` | 0 |
| crates/debugger/src/tui/mod.rs | 3469 | `fdb9fb5760ab8fd3b8e1a3aabccf52d10f9f70386984e6e0d80c670072152558` | 0 |
| crates/debugger/src/tui/storage.rs | 7263 | `4ef546f90e164bbb2aa98dc930434519e10433053abb38fdaede9467e22c28fc` | 0 |
| crates/doc/Cargo.toml | 787 | `34e679795d733c54b33ad04e2ea2c2e0f357ad4c432d298a0269cc9165570ea4` | 0 |
| crates/doc/src/builder.rs | 13271 | `accabf24a172cfe8d13fe7addb1eb22a65e5609c8b2661d6ec7464579cc84080` | 0 |
| crates/doc/src/hir_ext.rs | 46184 | `824937f1f4fe94c14473b029ce61f0da489c1d3a42f86156c82e36780fd24d99` | 0 |
| crates/doc/src/lib.rs | 289 | `a5a1911cbcb741bc36342720df9edc118b7a707626dd7fefee0f51822f2b2404` | 0 |
| crates/doc/src/markdown.rs | 3974 | `8d36c4a1e95f0bb1f70cf103a78e00e1ca6ad6eca491a22dd5f5b07cdef3f8c2` | 0 |
| crates/doc/src/render.rs | 55589 | `dfcb27264018a1ef880fbf810c007eb9352f56c173fee8e10a8a3014bb391e5e` | 0 |
| crates/doc/src/utils.rs | 5653 | `e5d2cdd2cbc77be33c3eeb5eb38fd8d9280e456fdf92265b8be110d16a81a097` | 0 |
| crates/doc/src/vocs.rs | 27555 | `05894a78ec1f7e162897ecd069daad51455905d67f38617b9b145d419850fcb6` | 0 |
| crates/evm/abi/Cargo.toml | 551 | `e973759dbb0dd69a72c30c5c03ad12171740404b254c44b912684a91908a19cb` | 0 |
| crates/evm/abi/src/console/ds.rs | 2584 | `fcc02485bc12bbf6e62531d6995816347aee260c8cdb924b4cc573f2ab09fdc5` | 0 |
| crates/evm/abi/src/console/hh.rs | 232 | `f63076167f92e37280fc9fb7fbf875c909285d2470e8f634b77bd7d3475afb72` | 0 |
| crates/evm/abi/src/console/mod.rs | 500 | `d05bbe627bb3ab10777eb52ceb2c7809a39e2c8be768102f6632211caa77585a` | 0 |
| crates/evm/abi/src/console.py | 1327 | `5a1e8b94614e3ed414f60dd7bba1c4c4a990d7259bf5a1c32c221a2090122436` | 0 |
| crates/evm/abi/src/lib.rs | 198 | `6a981e6116475c0cbbba4222d40b8fde059e7f2f401d1aed6e78232a8f83c114` | 0 |
| crates/evm/core/Cargo.toml | 4210 | `01a5a1ce771123b5e153b8a267603b484049b1e714be7df0da63ddbee6247421` | 0 |
| crates/evm/core/src/backend/bal.rs | 1895 | `da3a14f7c0b3cead54859f9ea35999249e4ec4e6118ff9339fe444c5bf4e911c` | 0 |
| crates/evm/core/src/backend/cow.rs | 16032 | `6bc2880d3d275bc8aaa2c15b721794c8a0bdcceed8e7d1d52f759790dcd5b5f7` | 0 |
| crates/evm/core/src/backend/diagnostic.rs | 1790 | `43e3b4a2cca9f687375cbf14e07eeec18d124e7b82fddbed6a2efd8b83572ec0` | 0 |
| crates/evm/core/src/backend/error.rs | 2172 | `33cc7af8e6854782e4ae4738817c50c98bff2b4c88b05adc4551f28693ae4ebd` | 0 |
| crates/evm/core/src/backend/in_memory_db.rs | 6856 | `5e0b748e381924a65395d0f14818afc2e13a74b13dba82abe410f41299c30af2` | 0 |
| crates/evm/core/src/backend/mod.rs | 192198 | `5d470ccc1a11e393941fbb55974d61483b6357587a4881c7693ddb3964db2d79` | 0 |
| crates/evm/core/src/backend/snapshot.rs | 5467 | `773f35e043321b485931c7b6c46c91e4ab88a000840d7f80c08d44db68e1a46b` | 0 |
| crates/evm/core/src/buffer.rs | 4128 | `dba6cf818ce326e73006563c5adcbc86f08c41cda0354b14ed797439ecdc7698` | 0 |
| crates/evm/core/src/bytecode.rs | 7276 | `ac42465dccdaca204f17371a60f087152ec97284363f533f7da65cda2da457ec` | 0 |
| crates/evm/core/src/constants.rs | 3318 | `9b14b857687e76ff6155952865d392e586240867e67858ebd73492915d45558b` | 0 |
| crates/evm/core/src/decode.rs | 10458 | `c6146a70a68a9c94acf02643364956f3720710d3a22026ba418bca9a079bfddd` | 0 |
| crates/evm/core/src/eip2935.rs | 1188 | `b1842ab5c5bbf250b53e50c4d30441d310f136522bf37a37c1c13f928390069e` | 0 |
| crates/evm/core/src/env/block.rs | 4199 | `f5a5d9ed7d7f89a200b15c6c802d86bdc84d6bf803778e2c15d0b30728db772e` | 0 |
| crates/evm/core/src/env/cfg.rs | 2686 | `01f5ae8dd45053f7691f9601d723ce271a0c86bd3131887362e580e973ceb857` | 0 |
| crates/evm/core/src/env/chain.rs | 1058 | `73984ccd8a1f3974a7ef6a68dc9b621456f96d890e3cd8a68dd635fdc5352bc4` | 0 |
| crates/evm/core/src/env/context.rs | 6939 | `f88eb7873793f4b5f95779baf6df01795765b7585613634bdb6b198fe6990bc4` | 0 |
| crates/evm/core/src/env/journal.rs | 2791 | `ce2d62c8acc84da97db411142497234ced833ed0c41985ef733c8ceb2b53d1cb` | 0 |
| crates/evm/core/src/env/mod.rs | 431 | `d595d27a407679064c17f2c990bdb553a74797a0d2daa8adea30bb2e0d4f1a71` | 0 |
| crates/evm/core/src/env/rpc.rs | 27072 | `21f772a550e3e73d7a7d99e634dcee6d3844d2be41ea536484a9b6628ae9015b` | 0 |
| crates/evm/core/src/env/transaction.rs | 17780 | `11b5457c936522e787d4cd8956ada2c506c86eabe9bacb635510e5a930f59dae` | 0 |
| crates/evm/core/src/evm/base.rs | 15683 | `e9eb477524f91251d2996a54346f33d907955eb71906c13b2e8b7e206abbb1e9` | 0 |
| crates/evm/core/src/evm/eth.rs | 4269 | `517534957a7923be97e92045eb83a717e27f5de2cab3e66a829f74f640c6f7db` | 0 |
| crates/evm/core/src/evm/mod.rs | 26138 | `d5b3eae80c8320a3ff7a9ce7382321585124b1545d985a8359614ac9ca2edf9c` | 0 |
| crates/evm/core/src/evm/monad.rs | 51713 | `ec94eecd5a6ec41984cd52bfd4beb422f49ed7a0155544b9302d00d60fe45483` | 0 |
| crates/evm/core/src/evm/op.rs | 9487 | `dc430f89f2f84f16907bcf94ec5e885a3f5b7654086a8bc4a6c8547d05cdb7de` | 0 |
| crates/evm/core/src/evm/tempo.rs | 8834 | `733bd918df7bf11bfbfd4899f3245817bda111bea3ef0873d5b8ad88f70ed01e` | 0 |
| crates/evm/core/src/fork/bal.rs | 6562 | `743afc3476194bad033757d0419019ff8f5bcf3dcfd290c4b484b91bba62595e` | 0 |
| crates/evm/core/src/fork/database.rs | 14991 | `3733420b1ec927b8aed17487f67c5a38063f7b83ac768448b432fb59b034f6c4` | 0 |
| crates/evm/core/src/fork/mod.rs | 12924 | `6eae83b1b812bd1a2a95a45841a646e2af4fcdb16bfa3f329dd640666d531321` | 0 |
| crates/evm/core/src/fork/multi.rs | 59589 | `fc1f3f101823b4213f1ab87c6017a5a37852b03507235c6394e5c6c29180ad9a` | 0 |
| crates/evm/core/src/fork/prefetch.rs | 6934 | `e1cea5b45803e6687c14f16c6e64ce48154f218366682380cb1dec34aaa680af` | 0 |
| crates/evm/core/src/hardfork.rs | 34 | `4ff7c216c3bf0823791b4ee0655baf23cc35bf21b7041c16a1307c9819e66f0f` | 0 |
| crates/evm/core/src/ic.rs | 2150 | `89404faf69636dc5ec0c3ea2f40749d6f9d609ac8fa451692ad28bd87de24eb2` | 0 |
| crates/evm/core/src/lib.rs | 3124 | `6b7d608173ccb354b6d141c5850cf0bf57d693360e6741a1c1cd6dcfed1f8248` | 0 |
| crates/evm/core/src/opts.rs | 118847 | `82d0a1d416f696c53426317777adfb1dcba770465c9fcaf65c71032395a70f05` | 0 |
| crates/evm/core/src/precompiles.rs | 2517 | `2de3445f021fd297bb57e2ada44a4a64dce3ccf4edb25270ae0f6d497984af28` | 0 |
| crates/evm/core/src/state_snapshot.rs | 2283 | `3189dfad6e4205299b45fc26cc519dbc382d477eb12aea4fb60769b73dbe7d7d` | 0 |
| crates/evm/core/src/tempo.rs | 7240 | `e4611a6731e91049121bb28f7ec105183376733a3a848292e5632c39ac539cb5` | 0 |
| crates/evm/core/src/utils.rs | 20652 | `057ad830684db584dd4e7db64628f66b47a12b779572918cde5999b374ab1a90` | 0 |
| crates/evm/coverage/Cargo.toml | 783 | `dcdc5a8a873d9ea7c422636368ba40f6b505c03e19cdb34363baadc6a9f3f170` | 0 |
| crates/evm/coverage/src/analysis.rs | 31445 | `fe634ca6da7731659d066238e6f60e195fcc8e4de4e63c4bac22d75777c4b3c2` | 0 |
| crates/evm/coverage/src/anchors.rs | 9685 | `6e308d26bda8cd0c47229323fe17832abaf3bf4afc632e4fc3f7d4f60d21f6cd` | 0 |
| crates/evm/coverage/src/inspector.rs | 3488 | `042f8befe6530c4241383fcb090138b66d597d8572c33672710f9963cefbf227` | 0 |
| crates/evm/coverage/src/lib.rs | 30911 | `c1e1030188e4c3caebd48c6ac3d86a347e3b3e0518f4fd2063049d88c3bebac8` | 0 |
| crates/evm/evm/Cargo.toml | 2789 | `b3803ddd6668b099b5216c2fd4b21e13f52964e10856cbe2ad3b357b96c2aa79` | 0 |
| crates/evm/evm/src/executors/builder.rs | 5400 | `4af64ec77589169a5d09d04d93b619cb3fbe9576e5672181f559e9a1187cb308` | 0 |
| crates/evm/evm/src/executors/campaign.rs | 9620 | `b7d9c6b4f9aa28c5e5d5648e7c6ba8763eb235079f7a177017a47812797383ba` | 0 |
| crates/evm/evm/src/executors/corpus.rs | 136886 | `8f0d8bd0fcf304dfeaedcbe23ebf3d325762da552ec96931306aaa3d1c9ffab7` | 0 |
| crates/evm/evm/src/executors/corpus_io.rs | 12602 | `58b4f9f20bb2967021d174d0c3b40812155ff5fb90918bc25d12305883d06490` | 0 |
| crates/evm/evm/src/executors/invariant/campaign.rs | 41424 | `1ae69ee40d0c1f5e97e697ed7078b3b90128c2b049dc0c156a9f745c2916f455` | 0 |
| crates/evm/evm/src/executors/invariant/error.rs | 21400 | `2029b9668d5aa18d697a0301d4b1a03d3097d96afd5e2dfe76874dfa0082e7e4` | 0 |
| crates/evm/evm/src/executors/invariant/mod.rs | 138136 | `e93d25bd126afd8a3160e8c4ec8f7ee5f2e99db7caabe572a941fbbe69c94682` | 0 |
| crates/evm/evm/src/executors/invariant/replay.rs | 7713 | `86ff8231dca1f221e9216fbe840b1796ccd53b3593001b89d2b2df20a51e2d01` | 0 |
| crates/evm/evm/src/executors/invariant/result.rs | 24287 | `bc87a20871f7ae6b17706852af22d293f20aaea1d36c3870b2064259dbb2ef35` | 0 |
| crates/evm/evm/src/executors/invariant/shrink.rs | 48214 | `7029943008f355d5bb7f9914d3ca02acdd27bad43d73a4ea1c3a434c9a0cf742` | 0 |
| crates/evm/evm/src/executors/mod.rs | 109446 | `a1dbb96bab8c2465f176bfaeec647057e11b392797b32a5ba1c2716840630a4b` | 0 |
| crates/evm/evm/src/executors/sancov.rs | 2296 | `29aaab656421fae47fd6e499867bc13bd153cff1fee4f2c7f168c71729335156` | 0 |
| crates/evm/evm/src/executors/showmap.rs | 43745 | `ebfdc5dc7631a9705fc435bd7accc9bcfadd9b424c0e5c54f2fae5fd73a59dfe` | 0 |
| crates/evm/evm/src/executors/trace.rs | 12972 | `71ba47af89c227f646dea911cf59b0e14a1ea65fdeae8c6ccc415c5fdd9a0568` | 0 |
| crates/evm/evm/src/inspectors/chisel_state.rs | 1083 | `a5dafd7270efe4debbc756d72e58e64d08aed5e7616f4acdbf103f6fbfa3c7c1` | 0 |
| crates/evm/evm/src/inspectors/custom_printer.rs | 3437 | `5a9e8724ede2ab664e911daff8ef174d1f3aabfce9e5e11bc853372c09baebff` | 0 |
| crates/evm/evm/src/inspectors/edge_cov.rs | 22009 | `7e4c02bff8e312a6cb3055399052a9c88b9950770a431882d70819bec2692dfb` | 0 |
| crates/evm/evm/src/inspectors/logs.rs | 3672 | `f460744945447d95dce1ac089d158412dda245ba11ac1e49af1936e715f3369b` | 0 |
| crates/evm/evm/src/inspectors/mod.rs | 955 | `328bd071a3de7f255b751e0391652f1138ba320e2acb07a1703c35ce54a5cf0a` | 0 |
| crates/evm/evm/src/inspectors/revert_diagnostic.rs | 8271 | `d2731bd2c1a45642b655859dcfb0011c0765e73c40b522cfca6a80012273b0fc` | 0 |
| crates/evm/evm/src/inspectors/script.rs | 1436 | `d90027b9138d79bad6b291fed29425964b743eabc26a12d32b82b3a9a6090a6d` | 0 |
| crates/evm/evm/src/inspectors/stack.rs | 101307 | `654cf99d7b9a826b403dfc88d356983738b6dd3b50399a0250028fb5f4865c4b` | 0 |
| crates/evm/evm/src/inspectors/tempo_labels.rs | 2881 | `35654efac7c293e3757957fd2cae244cf11881c16f91d0e6b02e2fa06bfea0f2` | 0 |
| crates/evm/evm/src/lib.rs | 681 | `cf30f8dd7a596b6a8814960cc22b98e0ff2a68492891378f2e01d50ce6de5381` | 0 |
| crates/evm/hardforks/Cargo.toml | 1055 | `e4e43b57255f1b7ae28f04678d205009a82b200f94e7eb16d03008f220d8a3ee` | 0 |
| crates/evm/hardforks/src/lib.rs | 45178 | `a6e9dfd7ea3cf2e24f7646a682a7de04d56c85b6f5449196701c70429a2e6a37` | 0 |
| crates/evm/networks/Cargo.toml | 1419 | `e5be4871621defcf34e2f882c6c72533b94fe5f3aee640867bbb3fb95a3de9e4` | 0 |
| crates/evm/networks/src/arbitrum.rs | 2378 | `385d9112aa2c6266d1ca1c3f088be6eed2fa6d643ca84691f5c55c9d439d2350` | 0 |
| crates/evm/networks/src/celo/mod.rs | 164 | `831e135796e449a385125f7aef209c5d788b34f1cd93b93391d9787110b5621c` | 0 |
| crates/evm/networks/src/celo/transfer.rs | 4484 | `67fb433fd139c57e79ffbb98f208e3c7a306981024c098d3e048149e1fb668b3` | 0 |
| crates/evm/networks/src/lib.rs | 81914 | `82ee234439f0109c51a48fa17d0789db34c14c19f45e8a374639daff758c84cd` | 0 |
| crates/evm/networks/src/optimism.rs | 803 | `32c1da5f967b42ce359090e02ba3c1f0cce74d49cb2995916f915a66a1e37f23` | 0 |
| crates/evm/sancov/Cargo.toml | 341 | `efb34d45fafc8ad9fce993343d5a5a737bbeff40335050387fc5248470ac7b0b` | 0 |
| crates/evm/sancov/src/lib.rs | 8139 | `1fc8303b855ddc6243c4f3844672005155cddc16255963e95a19ec977513624b` | 0 |
| crates/evm/symbolic/Cargo.toml | 1034 | `6eea12f3dbb9d3fb28ac86e7d37b990796b503908c7dbf5c6b4db4dce692c1bc` | 0 |
| crates/evm/symbolic/src/abi.rs | 36087 | `a9924a6340a77ea3fa1061032b49f260498db668d1ee424898804c1487f17b5e` | 0 |
| crates/evm/symbolic/src/consts.rs | 1926 | `e7d77bbcba9fac4a5221803304065f50b31f0999ee80c2f79130d5971577aae7` | 0 |
| crates/evm/symbolic/src/executor/calls.rs | 73781 | `02657ccfeb6f6674a2edc7be997ebc280aa485dd0777f0a9e674e898ff30f83b` | 0 |
| crates/evm/symbolic/src/executor/cheatcodes.rs | 111666 | `153aaf1f4f6eb5ce9ebc5215974275ac66095fe3cf7b30fbbc03d3c292a2c1a9` | 0 |
| crates/evm/symbolic/src/executor/constraints.rs | 9554 | `9085441f46259194c546559e2f004cf77bfb51e3787aa0cb3dad3876c0b95ec7` | 0 |
| crates/evm/symbolic/src/executor/create.rs | 9287 | `c180db9689f23776ca92e0459920ba5e76710ffed53c14c558a34d0ade6e6111` | 0 |
| crates/evm/symbolic/src/executor/invariant.rs | 14321 | `2996454d9fc54aa30e5cf705aee4448c6a8ced12571537f32af4db86f7813827` | 0 |
| crates/evm/symbolic/src/executor/mod.rs | 15267 | `5271578485a5d9f750d1eb1c98c27e7d448f5fa87682dad7b7e015634116053b` | 0 |
| crates/evm/symbolic/src/executor/opcodes.rs | 67382 | `d681b897105b70ff92f3f3e5e6c670fc511d7b48f498138c1e0f53ddf543ed48` | 0 |
| crates/evm/symbolic/src/executor/run.rs | 36276 | `d198feffae2abdce5f934512e5d90397b76a4e08e77f693c1281a3eef3d0cdd8` | 0 |
| crates/evm/symbolic/src/lib.rs | 16557 | `15cac19e5476b5c4aaf6741ae3f2f957081dfdb01dbdcc2794e6f48fffc18b1f` | 0 |
| crates/evm/symbolic/src/runtime/address.rs | 4950 | `8e26d99f7af5685d34f4744512e88abff7ae78bcd25cca103b1f3f2b91111921` | 0 |
| crates/evm/symbolic/src/runtime/bytes.rs | 23308 | `8c7e5eabeae27a5c459ef778b9896666d77bef2350f99206453d1eacc27b0eda` | 0 |
| crates/evm/symbolic/src/runtime/calldata.rs | 2978 | `37e26a1c8858fa1fcfafefe3b42c42067e4d6d8e43c31d704fb9fedfb2208df6` | 0 |
| crates/evm/symbolic/src/runtime/cheatcodes.rs | 37460 | `d679a7b340e16e1040dad730e8044803bc6e89be03f9cd5ab04254ad9f3bc161` | 0 |
| crates/evm/symbolic/src/runtime/control.rs | 558 | `41d6f06b3038375f19af633c980c42de626adb9a5eab50cafd63557343e25770` | 0 |
| crates/evm/symbolic/src/runtime/evm.rs | 5407 | `bf8daa1320eaed2885b05392d0b6d0440dccb0f4abdbb9b0eba1c55ad0d4882c` | 0 |
| crates/evm/symbolic/src/runtime/expr/bool.rs | 37082 | `f09a19d66da8554b6d1cda682d3a366fd4427ebdfe9561baa4d9cf4314809625` | 0 |
| crates/evm/symbolic/src/runtime/expr/cx.rs | 3627 | `da1f13a57982b8442725e81805f0d7e1a1375a6f5ffa94b4c2e32030abb574a3` | 0 |
| crates/evm/symbolic/src/runtime/expr/expr.rs | 98135 | `c7de9505a002bdf19d84b1755bdc847668a32de5cedc701d7b41f94daf3f3d0f` | 0 |
| crates/evm/symbolic/src/runtime/expr/hashcons.rs | 5140 | `2202925e04afaa0b223efa42ae2f1ca70afac862abb8d585026e10586ae55796` | 0 |
| crates/evm/symbolic/src/runtime/expr/mod.rs | 10728 | `e4d96ac92d7a7ad4e2be0a9ba90835802cdc11f387a14f6ce56df76da6303d69` | 0 |
| crates/evm/symbolic/src/runtime/memory.rs | 39350 | `d986bb43a8f068b2cf46d9ea1a3657f5c6d1702d2071852af73d7f1f7afb88ad` | 0 |
| crates/evm/symbolic/src/runtime/precompiles.rs | 10537 | `4ae57d2dd902566267083f141ae31eb68c45efba84b8272dddd41be8ef769e38` | 0 |
| crates/evm/symbolic/src/runtime/solver/fallback/mod.rs | 38131 | `46e7eb0c8feee6ae6fd6811837b73db70f7700e33b23f656c46b71d44c33ab41` | 0 |
| crates/evm/symbolic/src/runtime/solver/mod.rs | 65338 | `af6910f69cea376402bde9e9d5ae2c1f47b156cbf88cf2c02e5222b71861e800` | 0 |
| crates/evm/symbolic/src/runtime/solver/normalize/mod.rs | 87294 | `b0a2ec5b99d9a78b4c9aeb1706df80c4c6754d7bf9bf7d7361fc9fb3bac59320` | 0 |
| crates/evm/symbolic/src/runtime/solver/normalize/polynomial.rs | 8689 | `e09bd17036a1f3336fb6d2a8bde4acfd40ed7f8f572b8f84b99c0a1ca276bd8c` | 0 |
| crates/evm/symbolic/src/runtime/solver/normalize/rounding.rs | 6741 | `a164890836daaeab8495e25d96f2425794c5c824f61be6657c0d81b0b06b3847` | 0 |
| crates/evm/symbolic/src/runtime/solver/reasoning/mod.rs | 258 | `d48c84e1127d0a2a6e78d22c94f1c3b6a91daa3de7d184662eb5dc893411ece1` | 0 |
| crates/evm/symbolic/src/runtime/solver/reasoning/monotonic_product.rs | 10949 | `76ad4a2bae114d278f64eb07b46d1db36851342822576b37e00fdce180305692` | 0 |
| crates/evm/symbolic/src/runtime/solver/smt/mod.rs | 11757 | `0c98d7f51899e09965007e189a11088f2bdef039d5c43af9695a2ced09dfcf0e` | 0 |
| crates/evm/symbolic/src/runtime/state.rs | 92778 | `89a35a2102909fa9601cba4971bfb8d96d27d47245eb64e9e08d8b4f6620e773` | 0 |
| crates/evm/symbolic/src/runtime/symbols.rs | 1254 | `131d0defb8beca0476834d5bdb51383a0a2682103fd6eda02c3f5aed5ac2f59a` | 0 |
| crates/evm/symbolic/src/runtime.rs | 6387 | `688982ec092475eb64b862099f2f95732d2d4002de961289c8e1d5517d0a450d` | 0 |
| crates/evm/traces/Cargo.toml | 2128 | `66e07791ef76b70839b84e52386fa9fa1dc795a63baa6aab35b6ad166d5286aa` | 0 |
| crates/evm/traces/src/backtrace/mod.rs | 14299 | `92c3643d9b7c45c698eeda5a04ec8a3b24573fd897de18e8c497e084bd442fbf` | 0 |
| crates/evm/traces/src/backtrace/source_map.rs | 6699 | `98d5e6855a2b0bfd4f1898ff884900eff76a724497d68e953397f397b59154f8` | 0 |
| crates/evm/traces/src/debug/mod.rs | 20488 | `a2c075a51fd35140293ff9628455ec58e5f1a328404cb7ef8f0ea3c42650775a` | 0 |
| crates/evm/traces/src/debug/sources.rs | 22367 | `9c032a89efae721e725784b0129500a909c21886b4180e6cfda9d9327459354e` | 0 |
| crates/evm/traces/src/decoder/base.rs | 28618 | `3d5a6fbcfac44b6ed38329c3dcc1044558a33bae092fe05fdad70e0ea63f7e36` | 0 |
| crates/evm/traces/src/decoder/mod.rs | 191894 | `9a1d93e87fc5f3d58e01e88de0ddb2f089a1c2a6bcdec33302b8464e1acb427a` | 2 |
| crates/evm/traces/src/decoder/monad/IMonadStaking.sol | 3926 | `04c61cabeb2fe14ca7eebfc4f1ce0e8bc23eac4fc3f2296b0e6f1f77d5081d20` | 0 |
| crates/evm/traces/src/decoder/monad/IReserveBalance.sol | 251 | `7479aa5f41b8ce3110a42256d44aa0cf35f6e6d33c224d3d782f50ef35e91c7f` | 0 |
| crates/evm/traces/src/decoder/monad.rs | 589 | `3b552e8d8e51eb6eb050be21697a16e697a6e2a14a047cf75fd134bf019792c4` | 0 |
| crates/evm/traces/src/decoder/precompiles.rs | 24685 | `939dd5d3921de298f94d61d0e833dea91a8414137910920fa0f9fd2f26cae7a1` | 0 |
| crates/evm/traces/src/erc8021.rs | 6335 | `abbabfc9e9a47ab5d82c01e1fbc496c380dc553403fbe5a50c663d518bccea9b` | 0 |
| crates/evm/traces/src/folded_stack_trace.rs | 14230 | `88264c2f13ed3b1ac8e4e23b9065fc4b98cdeaa5d4cb560bbde5be1e261a2e6b` | 0 |
| crates/evm/traces/src/identifier/external.rs | 53045 | `dc9d74e7693ad3f07a35573190c933e46f9d170da93d363b3175f47bb9b661d1` | 0 |
| crates/evm/traces/src/identifier/local.rs | 8192 | `85da2181233fb62e1d229dfc001cd6ef516ed6f459596137c8f1a032a5aabd1e` | 0 |
| crates/evm/traces/src/identifier/mod.rs | 3573 | `60204acf601bb06f405263b7296b0c8e23e556da1f4055a16a65db5bce1da976` | 0 |
| crates/evm/traces/src/identifier/signatures.rs | 18590 | `722f8511013dace7548f8ce8b3cd6575957b7dd538ec8d3bcec62c7f104b40e8` | 0 |
| crates/evm/traces/src/lib.rs | 38994 | `19d38840840320cdd2da2bd8de3a6485a6eb3d9543145226a77e832b14c41cd6` | 0 |
| crates/evm/traces/src/speedscope/builder.rs | 12049 | `05b6880f00884ac2847ddbf8d19f699d0005efbe42adce682fb6c128ca6ddc07` | 0 |
| crates/evm/traces/src/speedscope/mod.rs | 84 | `7c466b80800f6c5978bc0152726f3c6ad3314f9558e0538990fd9895eeb7784a` | 0 |
| crates/evm/traces/src/speedscope/schema.rs | 8702 | `29663e81f01b5133abc3fd7d8409867a2b46b86d500338d88d1cfb0aea3cc770` | 0 |
| crates/fmt/Cargo.toml | 601 | `fb5b2daa0ca5e1958ef0796f9f74b9df3b86c1edd5e49ae9828265e31f726672` | 0 |
| crates/fmt/src/lib.rs | 9603 | `de5e71f58a34ebc6ebcda6defc989485e29b6e7c9b32018c76bb011d636a56ea` | 0 |
| crates/fmt/src/pp/convenience.rs | 4951 | `11efb6ecd71cae810ca5729b996a5e074c8f1dcf701cf97740704b1391972af8` | 0 |
| crates/fmt/src/pp/helpers.rs | 1204 | `a598fb9129314d3ce4888c62682c306e15170cbd1b42f87acd265dc8148fea8b` | 0 |
| crates/fmt/src/pp/mod.rs | 16917 | `dc7109d2ed1e1027b55d14298c95f678a8eb77cea7cad056d300d6d7df8bd5f7` | 0 |
| crates/fmt/src/pp/ring.rs | 2083 | `8790d04aa29e1819f2c3df1c1e011c7b083e20d790ecc18cba44fc6c93fe442c` | 0 |
| crates/fmt/src/state/common.rs | 35703 | `6de797bb65d53dc6aad2efa2f35ddc5830ef51eccdcba62148f881c29cbc4d8e` | 0 |
| crates/fmt/src/state/mod.rs | 52418 | `662b4a20cbf2172ff0ebcd17814116fdc5e29d823cc8525ab984664a963635dd` | 0 |
| crates/fmt/src/state/sol.rs | 138050 | `3486c15d736629c3d7fd31624fd13da0548b3d5f38699c5d49373d14406a6f53` | 0 |
| crates/fmt/src/state/yul.rs | 13433 | `73d9816d33b8f71975edd4ab76a9748b17c4d083113094518178cf46c23a0b60` | 0 |
| crates/forge/Cargo.toml | 4824 | `0e9df26adb3a77b7dc7c5ff780fa8ef64a485a96469e406eb2c4234c14650b16` | 0 |
| crates/forge/assets/solidity/CounterTemplate.s.sol | 379 | `87e3edfaadcbf61a39942601a11e4b6cc3d86011583aeda13dd148295f2b8ea6` | 0 |
| crates/forge/assets/solidity/CounterTemplate.sol | 258 | `4b5eaa107784609cabdbd23e34e479cc957ee69bd4c4de2881625b884e6bbacc` | 0 |
| crates/forge/assets/solidity/CounterTemplate.t.sol | 554 | `6525887dd3620bd7b28a28fce1b9d596441d2ece58f8cbaf15a851f57a460bb7` | 0 |
| crates/forge/assets/tempo/MailTemplate.s.sol | 1090 | `1d13a522def4b49168fefa58cab8e4d24f6e39ecfdfe5f7bdd85745af51136b8` | 0 |
| crates/forge/assets/tempo/MailTemplate.sol | 3173 | `be683ed20abdc3da045d719fd40f149d0e53139e94ea7cb931b7bdca8bade116` | 0 |
| crates/forge/assets/tempo/MailTemplate.t.sol | 7071 | `f0aaa90bd7882e2835cd4cf533c4509300b346964b02b6a2b00a571831f923a9` | 0 |
| crates/forge/assets/vyper/CounterTemplate.s.sol | 407 | `89deefbf70e5943c117cf9bd88b385c72eabea1f890787ecf88512163b4355cd` | 0 |
| crates/forge/assets/vyper/CounterTemplate.t.sol | 582 | `99d98893aa2a9eb67b080f5b9c0a10390490bffe14a5e9c79bb9fda9880d1e96` | 0 |
| crates/forge/assets/vyper/ICounterTemplate.sol | 230 | `b2995f78a5fe8ee34d2935427cb330f094e7e6af80d26a81cff8e65c7f73034a` | 0 |
| crates/forge/bin/main.rs | 545 | `d061065275441582b0327d0c7d759b76bc700aa46ac72bc43156fa2609051dac` | 0 |
| crates/forge/src/args.rs | 7532 | `cf8b88d60e9859576655253c9393738e4f4597cd3b3f9d1f08fc1be2c51882c3` | 0 |
| crates/forge/src/brutalizer/assembly.rs | 6325 | `5cbad2e982afefcf72e1b4487e366f2186f92528e7d174a0343dbd5d4777845d` | 0 |
| crates/forge/src/brutalizer/mod.rs | 6867 | `6e49d4d0a8529a2c8da5b979d810843cade5511e14f34aa6c5abf274dbfb1165` | 0 |
| crates/forge/src/brutalizer/transform.rs | 1343 | `569d01c6882f39bc0d1267e2876f21d9b9efcdd43a2f5fcefdf7c8917e2700cb` | 0 |
| crates/forge/src/brutalizer/value.rs | 6782 | `a55e9f80f85eed7b8db73e1357b0a02a66d04324c87fca2617ccacbc065372cd` | 0 |
| crates/forge/src/brutalizer/visitor.rs | 2720 | `3ead5689590558efe86958340fb2123268dfc7f210af0867717eed4488d6cc64` | 0 |
| crates/forge/src/cmd/bind.rs | 27007 | `b86686f67d2b4974241d93aa8bf27fa6b39fa087efa51171a3e28af2617430c6` | 0 |
| crates/forge/src/cmd/bind_json.rs | 19111 | `0ada130cda38d1a8ed3939643a2f1203438f3ceffb3b562b78777a96df52a9f8` | 0 |
| crates/forge/src/cmd/build.rs | 13796 | `49181ef185c83fda547eac2f0b28a4ea389d84f1f024cef5681668163426b4fe` | 0 |
| crates/forge/src/cmd/cache.rs | 5379 | `aa46063e4f90158c4c1e4be543dba704cd657a88d63b83c1dfe2c69860429c90` | 0 |
| crates/forge/src/cmd/clone.rs | 186939 | `460af7c36d69b43cc6cb589eb9fc990a51517f57637671c6bc172b1efd98731e` | 0 |
| crates/forge/src/cmd/compiler.rs | 7719 | `522502879be2b2e39848483fe82c987d3be794fd823fa96ac36049c78fa6bacb` | 0 |
| crates/forge/src/cmd/config.rs | 1662 | `f4e0008aa90b2dcf956ef3fd20fba0c726a3eab7f7547798238faefc340e9efa` | 0 |
| crates/forge/src/cmd/coverage.rs | 34704 | `0e33a45fcb14c78a0963d3c5c02c8236511b6ddb4620431918905072dc508c53` | 0 |
| crates/forge/src/cmd/create.rs | 38216 | `5e5d5c4da8775c57a4988825dc8e780101a4c849e8a0ae37d49803e761d7c3ca` | 0 |
| crates/forge/src/cmd/doc.rs | 6330 | `ea838dc458b23b2c6d963ba988cf4bad0dde9f82e79298efb32fbf0e9f049920` | 0 |
| crates/forge/src/cmd/eip712.rs | 8409 | `2235910034595dbe655c4284ff4460a43d318a0dc9c61a9e4bd57bf8bc0d8cb3` | 0 |
| crates/forge/src/cmd/flatten.rs | 1652 | `6ac0bdaee58bfbc93986fd6cc32ce905166e3ab888409c5ae489664eea99eea5` | 0 |
| crates/forge/src/cmd/fmt.rs | 15823 | `5e88c3fce9607b158cb8b26831ad21e7fff4f960c2c6e3e11d3ab4a5b84e9179` | 0 |
| crates/forge/src/cmd/fuzz.rs | 59049 | `cfe2d3f5b45f6618be684a02782f96cca1ae4cfcc92cf681d003a22c180f68bc` | 0 |
| crates/forge/src/cmd/geiger.rs | 1781 | `be1c4f6d8b0596422570294d5f214798c035a3680831c2faa13cf7c3c8197dfd` | 0 |
| crates/forge/src/cmd/init.rs | 14115 | `4b0acf3cd2891e424ada6e1da2528d2ba13ecbf75f1230d505ff5749db03550b` | 0 |
| crates/forge/src/cmd/inspect.rs | 33168 | `42768daa24bd610b84f7245de034b79278e5d6c2bce379d83e06fb4ea61c3f25` | 0 |
| crates/forge/src/cmd/lint.rs | 6539 | `b4ce97823e012caf422067a11ba0599df50ec718f37f052ccec585815cc99c82` | 0 |
| crates/forge/src/cmd/lsp/editor.rs | 17053 | `39b237cdba5b6e54baa1151ecf5399934168239c6990a6378cf8fb9979495acf` | 0 |
| crates/forge/src/cmd/lsp.rs | 3701 | `17b7fa4e2e0eba19538ef1270bfddd717891fe202bee84c97cbbf8e76a0ef625` | 0 |
| crates/forge/src/cmd/mod.rs | 815 | `88bd365f09cb497a166da975d68387017748d53e1e5147aebadf506af8baa541` | 0 |
| crates/forge/src/cmd/reinit.rs | 993 | `0b5fff6d2dcd6f145f9b2c4dda3b5366528eaddd7b80e07542cfa5d859de1dd0` | 0 |
| crates/forge/src/cmd/remappings.rs | 1563 | `f36c986444d391c93226a28d5ed8af10d0d1f8c06287bda8c664d5a396a029b7` | 0 |
| crates/forge/src/cmd/remove.rs | 2084 | `afac27155adc7c9f9ce7425537de32df555405b59de526fe4c6269e07b963b1b` | 0 |
| crates/forge/src/cmd/selectors.rs | 21596 | `8c47313057f8cb569481cfadd7726cc00455630f88d1f952f6086522ca44ed9d` | 0 |
| crates/forge/src/cmd/snapshot.rs | 26818 | `17be3c7d3d97b429c98fae2237c432866891747e1b059430c1ed1d51757772b5` | 0 |
| crates/forge/src/cmd/soldeer.rs | 1722 | `3801da62d96bfd368a911b31e4ab82f76348878cbe7f013cde4ec9bfdf796752` | 0 |
| crates/forge/src/cmd/tree.rs | 971 | `8d1fc02105ed048386d1b7f3a7dde01ce73cbf6dd119cc8f53024a86bf364ca1` | 0 |
| crates/forge/src/cmd/update.rs | 12357 | `967bd1384500acbca9233c3294783a9beabd02ca34234867e94ab4c4e25b34b7` | 0 |
| crates/forge/src/cmd/watch.rs | 34607 | `23aab2ae1ffaafb7f6990fec0c6fb25c84fa7b479aeeb6d44b8a8f2660e8ffd1` | 0 |
| crates/forge/src/coverage.rs | 25739 | `6297e0a5c530863c7145d7292c2de1d940d17360831e0af9c6182527a6dce3f7` | 0 |
| crates/forge/src/gas_report.rs | 11311 | `88a83063a70ba8afe3d82ac77a391ef28f549b6ea9944e0230e8e8b89530792e` | 0 |
| crates/forge/src/lib.rs | 930 | `176f1f3e3cca58c478a7b6e76a98a82d8177fd47fba262631f044f629568e877` | 0 |
| crates/forge/src/multi_runner.rs | 43111 | `55ad7ba073fc0ce2600a0a34f790f33c3d382ff50fb5137ec86f0d2c70d00121` | 0 |
| crates/forge/src/mutation/mod.rs | 26033 | `2af69a84233f356a70bb9cd5c3a0aa20b588499dbbe9508805c67b4084487925` | 0 |
| crates/forge/src/mutation/mutant.rs | 14980 | `2034a0d68159b242e2a428c98c1da4aef086f4769dbe56cc443d819a0d79d726` | 0 |
| crates/forge/src/mutation/mutators/assembly_mutator.rs | 7572 | `159858c89040961e50edd32f7d7c5b4cdb534bd6e97b049a6ad599f1d8140d4b` | 0 |
| crates/forge/src/mutation/mutators/assignment_mutator.rs | 6274 | `f1e9c6d1e01254c49c73261f93b7bf6b7d3fa2f92606f4bfdef8b2233ad299a9` | 0 |
| crates/forge/src/mutation/mutators/binary_op_mutator.rs | 4503 | `a8d0dc1965245d89096b72d6198f6daa5e322d48767564e5e1ac505b74d6cf86` | 0 |
| crates/forge/src/mutation/mutators/delete_expression_mutator.rs | 822 | `cb70056ccf76f91363f342cafd0a65d52b2dedffcf707e2d1b1b206e5ecec4f6` | 0 |
| crates/forge/src/mutation/mutators/elim_delegate_mutator.rs | 2105 | `01f7a399e1beb000515b4a21910b7643937d4e588e5a268de4121c988d38c7fd` | 0 |
| crates/forge/src/mutation/mutators/function_body_mutator.rs | 4666 | `ec5f3ee21b4904e97c18c3aa52ef1c589b6fde8fa2120e5c813313ad8d595a02` | 0 |
| crates/forge/src/mutation/mutators/mod.rs | 5289 | `74eddc6caecc549deb460492d51f10cc7187863892d91aef06d506ada0e83b07` | 0 |
| crates/forge/src/mutation/mutators/mutator_registry.rs | 3910 | `1d9d73d03f9ee3516b14e5c21e7bdfe13d8626198a377720767af03cf2c6be31` | 0 |
| crates/forge/src/mutation/mutators/require_mutator.rs | 5724 | `e273e1fb56d6e4d148f39e3a08b37c27c3b8f1909d67cae1a82ad8556096e356` | 0 |
| crates/forge/src/mutation/mutators/unary_op_mutator.rs | 4695 | `22ede764e07084dcff8e9be9fd593e0b0c38eedb8a6dade317bb2d6c29dea4c1` | 0 |
| crates/forge/src/mutation/orchestrator.rs | 35005 | `d41e302611a8e4d8f5b976c2cdbc935ae241225080ac7cf979b750834c2b1cff` | 0 |
| crates/forge/src/mutation/progress.rs | 11053 | `3fd789665489d073aa6460f795f112fc3a75c986834e6aa4b12c56e7eb58869d` | 0 |
| crates/forge/src/mutation/reporter.rs | 7790 | `0d35a9eb7f9a87f0f00a18eb4469cf107ca8301224d1fa83cd17250e34d7b74c` | 0 |
| crates/forge/src/mutation/runner.rs | 32749 | `6e24a553786667d3b2e6aeadcabfab7a2a932b9a20036e476897ca61e18ce6f9` | 0 |
| crates/forge/src/mutation/type_analysis.rs | 28368 | `c1d193f042a549bd6c88b47c7373c5d0cb7753eeb7fafe5b7fd622a4a884947c` | 0 |
| crates/forge/src/mutation/visitor.rs | 23925 | `72830db8f8045682b237c4b51ec60a466a6541fcfb1e759511242583db0b3b69` | 0 |
| crates/forge/src/opts.rs | 9596 | `15ebdc6f4327dedb0777bae4bb5893376b56e6dbb1eb4abee464d33fd22d1b7e` | 0 |
| crates/forge/src/progress.rs | 4362 | `a847415dbf5ca5c70c70ebd072a30ccadeb82dfe514cd693240026909123859a` | 0 |
| crates/forge/src/result.rs | 89274 | `3db88876130b346f65e757c307a7e295ebf4fc2e24dae0931443fbe1f640098b` | 0 |
| crates/forge/src/runner.rs | 262591 | `e83d7cdd1b83b00a113e1b8de2e1e5f596ea923ddd732d78acb96e8a4701b1a8` | 0 |
| crates/forge/src/symbolic_minimizer.rs | 72680 | `ca91a86c65e3f0931f21c95daa88b1247f42b2c2fdf797a69dd2214ec846d3f8` | 0 |
| crates/forge/src/symbolic_regression.rs | 27799 | `6315e7ac809aac7499ef5540e47d917b2cee06ae9c3e6e03175c7218f081659a` | 0 |
| crates/forge/src/workspace.rs | 72821 | `89f68d80d0eadfdbee3e4500f3e5c6cdfab7ba703723ca4a3d2d326cc3833e84` | 0 |
| crates/linking/Cargo.toml | 498 | `8d6c329fa511eb101cdcdbe8a2e664c98d04a17f2e9d38d11e5d87deec8bcd01` | 0 |
| crates/linking/src/lib.rs | 88999 | `ee86ecbd103247d668a18be969989bbadbcfb80c2e0b299bcbad7dd4a2dd7811` | 0 |
| crates/lint/Cargo.toml | 594 | `2495571da9030fd67b6eb2593e4934bdea8f16ff0f728d1166bc46ad13080455` | 0 |
| crates/lint/src/lib.rs | 202 | `facebcbca14a0b098527336535574871e305ddc3b994d07e3cd296df4dbe69b8` | 0 |
| crates/lint/src/linter/mod.rs | 747 | `ea17269188b40d97657d5f7090ffe01b9f809e36da26be53161479e8b57b4812` | 0 |
| crates/lint/src/sol/analysis/access_control.rs | 14656 | `d2b55b8396528d015511f1c40772d397940a05547d16ef76b1b650a2c19ae01f` | 0 |
| crates/lint/src/sol/analysis/exprs.rs | 16354 | `26c886354fe3fcb5aa073db0e504eccc37b89ec7a5eb6b99de3522e491d0d430` | 0 |
| crates/lint/src/sol/analysis/helper_cache.rs | 1518 | `f7a52e458d46cf52b13bf6609eb71665d939235c2fad72504de207237a4134d6` | 0 |
| crates/lint/src/sol/analysis/mod.rs | 296 | `b1b9d4bd5834b3d033c6240c2170fe3bc48f3abe3e1ff36e63d74bce6ac083dc` | 0 |
| crates/lint/src/sol/analysis/modifier_outcome.rs | 7038 | `5b03b32f0509d8d84de67050767eefb24b46ecbe202c6ed4bf147d243888497d` | 0 |
| crates/lint/src/sol/analysis/stmts.rs | 7357 | `e6f7725ceb0ffae525e436e6e93ad36e6a02ebe09c7ca0b73208467e7adbc444` | 0 |
| crates/lint/src/sol/analysis/types.rs | 1737 | `a6656fcb73358c9e81421447cc9c815a441366942ca7b5d1e90930e4bf8cf7aa` | 0 |
| crates/lint/src/sol/codesize/mod.rs | 167 | `626b501f8704dd2c239b32f922a5a155ee33ff329fde8f81e6ade5e0df37b67f` | 0 |
| crates/lint/src/sol/codesize/unwrapped_modifier_logic.rs | 7807 | `ff324bff91ed077551470e8b17fac075ea30b9580266d3c35da9ff32af54871d` | 0 |
| crates/lint/src/sol/gas/cache_array_length.rs | 5292 | `e4014e5fe80df7c21daf6f1bed2449c6367f249e4c3783a0428c1ba3b022a498` | 0 |
| crates/lint/src/sol/gas/costly_loop.rs | 2694 | `e0390da79ead93d4f60674d01ef72b5fd63b747a4071e1dbd9977ab1424ae053` | 0 |
| crates/lint/src/sol/gas/custom_errors.rs | 1268 | `c8315d0bdba70b6802ce7beb7a08e53886ecbc7a7443b973df7a70dcd28239d2` | 0 |
| crates/lint/src/sol/gas/external_function.rs | 9403 | `93785cd52075ce11582e1c49a5e4b6de44435c7aefb0f42d4b9b35301808e82f` | 0 |
| crates/lint/src/sol/gas/immutable.rs | 7978 | `49a893aa6b7266d2f3c769f162ab73adbf395d9366e247a1c81fef1990973cef` | 0 |
| crates/lint/src/sol/gas/keccak.rs | 1193 | `5562e071f826ab5460bed31517b5dab8d3463ed355974a06a28a5cac6cb74699` | 0 |
| crates/lint/src/sol/gas/mod.rs | 853 | `e66ba2b3a9c8fc8e712d06269f217e13db8921c5a52d5406494ec1fcb143564e` | 0 |
| crates/lint/src/sol/gas/unused_state_variables.rs | 1982 | `3e5aba3d43d6e8762c239e0b918e029499bd9084d0a8e5382a90b3969b70bf06` | 0 |
| crates/lint/src/sol/gas/var_read_using_this.rs | 4983 | `3ae5970d78f02c63ab0552bd7ac5bc9ed1d3968d3ab4d031d31bebb1f40e7e09` | 0 |
| crates/lint/src/sol/gas/write_after_write.rs | 10640 | `ce9c35c4d320744e614d0df88a4f1516cab9b56d6c9f3e5d3383e6b1426de785` | 0 |
| crates/lint/src/sol/high/arbitrary_send_erc20.rs | 41612 | `b97200d45dc2624beeeff34299a5b4060a73e48d6e2ee86895f8675cfc239274` | 0 |
| crates/lint/src/sol/high/arbitrary_send_eth.rs | 39614 | `b8c6152ca374820d6660e3352a33d3ed86dfa02dafb7dac97a0106fe07d7051f` | 0 |
| crates/lint/src/sol/high/controlled_delegatecall.rs | 20211 | `e451d8dc8b796dbddd49b14d280a1e33e151c1499c7cc30bc383f2d34400893b` | 0 |
| crates/lint/src/sol/high/encode_packed_collision.rs | 1568 | `aa6df4b94d47d6605ad08a0f64b971dfafee2707b4205df80b9b9f76a04a1068` | 0 |
| crates/lint/src/sol/high/enumerable_loop_removal.rs | 21178 | `a98bcf95a7f6356af8e20a17d97b7e36ade2616c007dcad641ff0de9b8550aad` | 0 |
| crates/lint/src/sol/high/function_selector_collision.rs | 30772 | `926bd3819dc9f1564d24d3cb213ed8ee594ef16418950d0e852f6d6570b15778` | 0 |
| crates/lint/src/sol/high/incorrect_exp.rs | 3504 | `e8d5e05fb18771a3e1203a7f084a2bb55f97efc2f9417f5a121f0973718e427b` | 0 |
| crates/lint/src/sol/high/incorrect_shift.rs | 1638 | `ae7de1ad1484fcb6a5ff7fd74006f16efb979b82b4771d4770b6ba915a128782` | 0 |
| crates/lint/src/sol/high/mod.rs | 1442 | `16c07e40fbd7644efe3c5f76173fde1069aae3cb523d28a1046c23184886e840` | 0 |
| crates/lint/src/sol/high/protected_vars.rs | 48079 | `a4c22d6f8971284241beda01b41ef40e33cc25de33d84251f0b6dcc96daa6983` | 0 |
| crates/lint/src/sol/high/reentrancy.rs | 83037 | `a42053772fca3fbfa79eccabd092efabb7ae34220c603d1fa964333d599067be` | 0 |
| crates/lint/src/sol/high/rtlo.rs | 1746 | `a8f6f86bb20f6a3b06515cb90dfa6da9614712ddd8f3360dcbe649fbb1c388e0` | 0 |
| crates/lint/src/sol/high/unchecked_calls.rs | 3896 | `6f8d5e088669884032f1426f646d10f43212fb30518b54710bab3d71e02cd988` | 0 |
| crates/lint/src/sol/high/unprotected_initializer.rs | 8496 | `b42c86f46720f3d54d869040225a2301b9e85db564d41d466f182564fd946d89` | 0 |
| crates/lint/src/sol/info/boolean_cst.rs | 2980 | `48df49d954279b3887684819e1c07ae09628911536a6741762c5ff0d2a6c1f75` | 0 |
| crates/lint/src/sol/info/boolean_equal.rs | 2103 | `27b4aa2534b095ebd67289a4af5d4d4de8e6ffe06c76fba99fe9348b75cc589b` | 0 |
| crates/lint/src/sol/info/cyclomatic_complexity.rs | 3637 | `575162e9cb6f848e6a14d5bee66be2fd9fbe853b0b082dad36179aeb86ff51ba` | 0 |
| crates/lint/src/sol/info/event_fields.rs | 1754 | `7aaa5053ac374b295ef71acad0dd5f78e3081ea9d49e3d69f51f05d3ed81778f` | 0 |
| crates/lint/src/sol/info/function_init_state.rs | 3275 | `5af7ff60b16b9107475b43d95fdef455db82d40d7c216317c3570456bd41d54d` | 0 |
| crates/lint/src/sol/info/imports.rs | 4442 | `86a00023f5db1c86e2db9e5f8f22d200acc7ff0c75565d042104c9b2a817f903` | 0 |
| crates/lint/src/sol/info/incorrect_using_for.rs | 3001 | `f019a4445dd84ec2a60a5fa0a070b2664748f336edab7c21892996366d11e331` | 0 |
| crates/lint/src/sol/info/inline_assembly.rs | 1733 | `868776fd8a989c7ffacb4be7c08163000869ff5d4a447849683172b978e26e73` | 0 |
| crates/lint/src/sol/info/interface_naming.rs | 1932 | `da64d88ac59f80dcf8179d7e9911108c8a734153e613b947caeb79a2d66416fd` | 0 |
| crates/lint/src/sol/info/internal_function_used_once.rs | 7171 | `1dc1b864732bf56178dc3b20bb1f5bc7e3e7a93b10e37266ead7c871d69ca17d` | 0 |
| crates/lint/src/sol/info/literal_instead_of_constant.rs | 7515 | `8dc30f0ca37c8ca9046d6458625077752817a23db948051cd0d00fa8f51fb14a` | 0 |
| crates/lint/src/sol/info/low_level_calls.rs | 530 | `d5dd09b2ccafba7be3ea0229096daf4db29ce06efc91e07eebe44b82e4c95dc8` | 0 |
| crates/lint/src/sol/info/missing_inheritance.rs | 5901 | `76cf568a47caf032679579dcfb707ebbc63362317eeb7e8d0db2c2409b7a9606` | 0 |
| crates/lint/src/sol/info/mixed_case.rs | 3410 | `a53b7966f3875e208a9839c51785b8dcce03ac1b93c48bcae4c8e9367a4b2ef9` | 0 |
| crates/lint/src/sol/info/mod.rs | 2735 | `4ec6a15fbb8a079b803296c04184754d296dc0670d7e6184a766f81cc46b08fb` | 0 |
| crates/lint/src/sol/info/modifier_used_only_once.rs | 2640 | `255c30d4985a42a164c39786a057a548bca454b9079dda722a5958ba4d7e653a` | 0 |
| crates/lint/src/sol/info/multi_contract_file.rs | 1422 | `8293107089286a22a74bafa956536ac87ac175dafd2cbfaa15f7c37f226a2fe5` | 0 |
| crates/lint/src/sol/info/named_struct_fields.rs | 1989 | `f9c7557f91565ee8d94cff8884ac46f9c978a1102eaaf9ef798f17fddb47c4aa` | 0 |
| crates/lint/src/sol/info/pascal_case.rs | 1257 | `c6b0c4d06282fa4bf7bc979593e2d2ec39efd1c09310c8edcac950108c110a57` | 0 |
| crates/lint/src/sol/info/pragma_directive.rs | 2025 | `90f70e093d9203e6322bf0bb1d5beb71ef00a3bbe0db47b193d3a064c3a12086` | 0 |
| crates/lint/src/sol/info/redundant_base_constructor_call.rs | 3131 | `ddb83e97955b91f8449e7ee98ff9bc9dfbcc2c6c77eae2c189f81e414d999221` | 0 |
| crates/lint/src/sol/info/screaming_snake_case.rs | 1196 | `d5f9358a122a4da3bc62dbe4bed2d2e688d847e52df4ca094c91c4abea985282` | 0 |
| crates/lint/src/sol/info/todo.rs | 3265 | `bfb6bc57d9dbf1026c820bb65ef346793d2ededda8ffbdcedf13c60f1b3b52f3` | 0 |
| crates/lint/src/sol/info/too_many_digits.rs | 2322 | `6f5b7bae52626b8014c9b9bcc15e0bf0470f91f18f738236a8ed0cd15482e99d` | 0 |
| crates/lint/src/sol/info/unsafe_cheatcodes.rs | 897 | `91c2cb75f2e1add42491cd951f6ecb8fd2b427ae6e35b9c9ac95cff0c9c3b3de` | 0 |
| crates/lint/src/sol/info/unused_error.rs | 2994 | `54e3dcfcea9a48ba14fcc7e1bab75b14770b2a46a01078ad0d2113e22031c91f` | 0 |
| crates/lint/src/sol/low/block_timestamp.rs | 11728 | `0631c1b5744d8e80049fa897cc0ff737ace78731207f7293177c8510b206e1ff` | 0 |
| crates/lint/src/sol/low/calls_loop.rs | 2921 | `831e5ae736fff9cab90fed75d99defede5a6965737126f7bc1ea46bd988ea788` | 0 |
| crates/lint/src/sol/low/delegatecall_loop.rs | 851 | `56194a5be04460353de6c489a2df7de18889c57b620a23ed765a685c290c8557` | 0 |
| crates/lint/src/sol/low/deprecated_oz_function.rs | 2182 | `c1dd74b7febf0167c53583ff77c17a51d8779244aad2e7d0ad86ff28581aeafc` | 0 |
| crates/lint/src/sol/low/empty_block.rs | 1658 | `02fcc7d7790d66ee9f6a1a9c70271e35101615c02115507636c9ed4799c81dcb` | 0 |
| crates/lint/src/sol/low/inconsistent_type_names.rs | 3741 | `bf183e5533aec9e4bbfbb48102e9c4c7ae8d0ec54c0549df857e0b1ed43bdbdc` | 0 |
| crates/lint/src/sol/low/incorrect_modifier.rs | 748 | `f537040089f2979e244a80107f3e053f5dbb481778e0705e26901d95e0901fe4` | 0 |
| crates/lint/src/sol/low/missing_events_access_control.rs | 27369 | `dc1ca05f8d49956add489048aa9ab146544e30193ca593271cde26779051dc78` | 0 |
| crates/lint/src/sol/low/missing_events_arithmetic.rs | 21422 | `36981c699594c02ee652a8105371585c805c80a36ed7372ccfb9f13ca9a6fd11` | 0 |
| crates/lint/src/sol/low/missing_zero_check.rs | 11107 | `aede4e7f1eee5e28dd73909ca65299347c71d23f1198fda8f9702ca8931cf5e5` | 0 |
| crates/lint/src/sol/low/mod.rs | 1549 | `c800fcda849d31eb6aab8768bf81dd8d292182a2fe128de83a90ab366f2925f5` | 0 |
| crates/lint/src/sol/low/msg_value_loop.rs | 716 | `492578c98dd8cf89925e4bd99ab8a06fb9fd3983a2dad29e96858fa4006b9313` | 0 |
| crates/lint/src/sol/low/payable_loop.rs | 7342 | `d8734f4c6cdb97701a9c27c68081530f17902de213ecf14be99712efd4db494c` | 0 |
| crates/lint/src/sol/low/reentrancy_events.rs | 21121 | `a87596cda002512457e7fe5a3418e0705bf18666f706e5c87e17f77c20871395` | 0 |
| crates/lint/src/sol/low/require_revert_in_loop.rs | 1458 | `1f74ebb65469fb3dabcd3b06c096a0c2be83acdf9cd1647f6a2ce65e799a768c` | 0 |
| crates/lint/src/sol/low/return_bomb.rs | 1480 | `15a342d4936a4e1ca2b77db3608f54f5b248a0060799cd9e48424eb2244c8e0a` | 0 |
| crates/lint/src/sol/low/solmate_safe_transfer_lib.rs | 2399 | `e2521f7b24615e6b46c405889ba77700c8f70413f8f15fb2ad9b96d99c0aeb77` | 0 |
| crates/lint/src/sol/macros.rs | 3146 | `9b8414cca615465f8ca8aefa3445229239a2d186603554e2961513a3bb6dc794` | 0 |
| crates/lint/src/sol/med/assert_state_change.rs | 3572 | `1ed7d9f74fd965fc01bea2bd6df8f0c572065a26377a723a885a42085b8d537a` | 0 |
| crates/lint/src/sol/med/cheatcode_environment.rs | 43555 | `14f7249c26b0a423247a27210b6e72afb34bd1d593952c2b8f9e4404cb3f228f` | 0 |
| crates/lint/src/sol/med/dangerous_unary_operator.rs | 1791 | `551dcfa5effb9c60d4b5285a338eea28993e4fe90a3b32e127565921a48342c3` | 0 |
| crates/lint/src/sol/med/div_mul.rs | 11168 | `3b84e19c7236c9ed5d4f6d70e60ada30293f39c24e121b2e7696acd01aa5eab5` | 0 |
| crates/lint/src/sol/med/ecrecover.rs | 35829 | `be9813ad3ed37f80e81bfed52b42b21c500d2c4e2dd46797a5d54b5261b7bc74` | 0 |
| crates/lint/src/sol/med/incorrect_erc20_interface.rs | 2179 | `820012e6a3498233d5c828cd0e114d8d7573fa2cd386eb856667d2c895d8ebfe` | 0 |
| crates/lint/src/sol/med/incorrect_erc721_interface.rs | 2229 | `718dc3f8d3ab49740ece0662004e0f33e7b83d881e8806767879ce9a0e74c0e9` | 0 |
| crates/lint/src/sol/med/incorrect_strict_equality.rs | 2124 | `544d5f2d26c62ab13f31fdd1d64fb03a594e6e1cfef105c8d3ae9d9ce6498078` | 0 |
| crates/lint/src/sol/med/locked_ether.rs | 8364 | `b39b64653b3c7cb31c36559f98f0c71987fe529c1ccfa9c570cd8c8c5c64170d` | 0 |
| crates/lint/src/sol/med/mapping_deletion.rs | 727 | `ab578411817df848b8404f73000a229c48dda5551aa0d62c36b5ffa13e1b6467` | 0 |
| crates/lint/src/sol/med/mod.rs | 2016 | `991c7b2d8a9e196574b4d2538eb79621b508aaa084ce635f3429648f81e1114e` | 0 |
| crates/lint/src/sol/med/non_reentrant_not_first.rs | 1083 | `2b962f01c8dde2c5cb3373f6158e227011b655d73bcdc6a7d180a2efcfc0eec2` | 0 |
| crates/lint/src/sol/med/tautological_compare.rs | 3906 | `b4c037bfd2c025da39a288c0e8c281ec8162a4872df1d1001fbd5e89fe1700cd` | 0 |
| crates/lint/src/sol/med/tautology.rs | 7284 | `1e209cf34eae8f16abc4d95607011569b05bba13ed6f64dd064afad414d63d43` | 0 |
| crates/lint/src/sol/med/tx_origin.rs | 1710 | `1264826bc6ca91501818a5f4780d0ce57387aebfd5d00f5be3571a8b632b5e1b` | 0 |
| crates/lint/src/sol/med/uninitialized_local.rs | 7830 | `ecb76f649ab8648820457410943187a110f9187266f751f041e3e2862e5cd736` | 0 |
| crates/lint/src/sol/med/uninitialized_state_variables.rs | 11025 | `e61e1bf7a90a11dbe088c08f126d1f0ebe3e87e9bd1efd565caa40da70f1fff3` | 0 |
| crates/lint/src/sol/med/unsafe_oz_erc721_mint.rs | 62798 | `06d1057d22af81f5335b47f24d61c44fbd6eb5f3fbeee4e0320655bb1612f3d7` | 0 |
| crates/lint/src/sol/med/unsafe_typecast.rs | 4560 | `e03151b02dd8e3f795e746b6c249b509c8cd277c7623e0186e92f867d965858e` | 0 |
| crates/lint/src/sol/med/unused_return.rs | 2591 | `df6ad4ed94f86273ec965a0fb8153203d964ef4f6b4307d1521f574b841fc608` | 0 |
| crates/lint/src/sol/med/weak_prng.rs | 3877 | `c296bae2a7e319d15a7120eecdb85c96c41bcf7302c755956fb5eedd46d4da44` | 0 |
| crates/lint/src/sol/mod.rs | 31064 | `7d0be24649bc362b0349549d2bc9cb081e4f248992f2a39fd9d419c2f1d5e9ca` | 0 |
| crates/lint/src/sol/naming.rs | 2524 | `cb57905ff99b1d7c9b4c7ade748d0d1ae45f08a04ddd5094b0f650874afb3e1f` | 0 |
| crates/macros/Cargo.toml | 452 | `905220df27f05b71c165e38994b0284eaa4940ec3218bebc23bec541575c4874` | 0 |
| crates/macros/src/cheatcodes.rs | 14286 | `1a9477ee6265c2a6932ff09b21259e22a77c38e961a348617e26ec70c8e44f33` | 0 |
| crates/macros/src/console_fmt.rs | 4792 | `3cc88f95e93fe4b760aa220b259503ce9b27b714d3837db6c16cf9754da5d5a5` | 0 |
| crates/macros/src/lib.rs | 877 | `182ee5e5d8fe9967c06890436f741a567b6dcc373f1b65d35f2ae66221a6dc6e` | 0 |
| crates/primitives/Cargo.toml | 1888 | `de481f7a4d2bd81b20b9f376ac8ff1c65ee2fa2f19baf132aa7b3487757a7907` | 0 |
| crates/primitives/src/lib.rs | 98 | `605240cd21bdc57f1b1b76c722ce534d6f6391cf7a2d694543f569baa86a452f` | 0 |
| crates/primitives/src/network/header.rs | 6571 | `043607b3c3b6f81751500b0df507b6fa81a79eaae8af8da926ba0e455e5f5d82` | 0 |
| crates/primitives/src/network/mod.rs | 2169 | `88f151db104d7813036eac15c09ade2da4ca7f0a3031e6c8e90bf6c14cd9ce83` | 0 |
| crates/primitives/src/network/optimism.rs | 1864 | `cc896ed84673cbe7c54c7d83e470a9e79545b63e6fb693737279fbcf63ddbb8f` | 0 |
| crates/primitives/src/network/receipt.rs | 12666 | `e9c53e0faf4d7c839ca23c673c95300743fda1e3686f3592e1b410c741c6a108` | 0 |
| crates/primitives/src/transaction/base.rs | 9110 | `bc4d2be481d78ab7fc52836f4a3e85e533277343d0a9b67a651e219e7c1ee589` | 0 |
| crates/primitives/src/transaction/celo.rs | 7679 | `5a5e0d4bc31c1da30c545dd5024bd0abbbdb6b497678b8fbf844201dfba8c12a` | 0 |
| crates/primitives/src/transaction/deposit.rs | 2266 | `e9d49c58a29dfc9100663ceff5ff162051a61b2ee8c996447b3bb2183f2026e8` | 0 |
| crates/primitives/src/transaction/envelope.rs | 46741 | `392149d657345beb715102a6c4f9d7890ef57a60f9882ecdd742c0e6977a2057` | 0 |
| crates/primitives/src/transaction/mod.rs | 533 | `8c22f7fd1a57815a43a11f4bc8ec11312e3aaae5b1cca61e3fe549d2fe72422a` | 0 |
| crates/primitives/src/transaction/optimism.rs | 7483 | `123c255b82617d3af7e62141017f69aa67dba2d0ec63435f99e9ab4655e23aae` | 0 |
| crates/primitives/src/transaction/receipt.rs | 33561 | `e1a0fb900c4edec1d904925cf5c0d72c62a743d23eeee2cf537a8d25757343bc` | 0 |
| crates/primitives/src/transaction/request.rs | 44400 | `6975b0c2021a0648c3095372ac6e3ab904537857510923032c324786227482c9` | 0 |
| crates/script/Cargo.toml | 2715 | `21461a0c8a597c68fe5b3ea6b8856565d6a40768176ab03025bd5d855bbde83c` | 0 |
| crates/script/src/broadcast.rs | 107821 | `bc2cc6769473e19373ef4dfc5693f11a76bc48ff92bf0bb4c934f2281dfb5855` | 0 |
| crates/script/src/build.rs | 23553 | `904676a22d95ab9ff1016978a233fa3ff85564fa96d81956be6053e957757620` | 0 |
| crates/script/src/execute.rs | 23417 | `475f314b3e39744f6adb6df9d6af3b1c4cd973cbf98555667ca0f480023ef0b0` | 0 |
| crates/script/src/lib.rs | 102094 | `d19c43743b2946283ed97332677ad61e8a05b4d1c19bb256ce5a859f45b173c1` | 1 |
| crates/script/src/library_deployments.rs | 14721 | `60c683e039fae1eaa9b41e511056bab8e9ca7001639283eb20d7e4eb6a03e2b4` | 0 |
| crates/script/src/multi_sequence.rs | 8156 | `34b3bb1b1cf55f4745c8002ed49d76c096bcb7b5235b5d375e531bac4df44da8` | 0 |
| crates/script/src/progress.rs | 14845 | `306e61d5b488d4c323e04627104a29d98bc9c59e811a31283c7f54e08a2d8a62` | 0 |
| crates/script/src/providers.rs | 3656 | `57297d79c9a060c1a463552cf6f35e496ebcd15e4e8cdaf0c7895165a45f00fd` | 0 |
| crates/script/src/receipts.rs | 22771 | `4efa0c4f4b8b5cac208af6b26bae667cfe9296dfaeced39fc6c8c333404dec32` | 0 |
| crates/script/src/recovery.rs | 78342 | `4328c5590955e8530c6620aa39f7728057131f12fa3ab92fc68dfed0b6dc7733` | 0 |
| crates/script/src/runner.rs | 27220 | `dbfa6a9029371d7660ae99ee1c1b3e82c38e16eac83e1a5e2e5761d6465c1b8a` | 0 |
| crates/script/src/sequence.rs | 27247 | `8104240aca0b00dd08ce62cbf33e30e2bc8a33d5028aded379bb1a2f9655fc86` | 0 |
| crates/script/src/session.rs | 5796 | `c8c0602a5b677e135e54299e2de050bb89fec9079af8b916b24e430502b4c0c4` | 0 |
| crates/script/src/simulate/monad.rs | 19523 | `8fee6c5e8597eb5fd5c74ef8b340a59db3c518042206361a9e1ffa67db5ffd2a` | 0 |
| crates/script/src/simulate.rs | 37200 | `0365eb393ef9cf149fb09d5c5ee0fffe1fade44ecfba32b42fabc5a44a2ec2a8` | 0 |
| crates/script/src/transaction.rs | 12527 | `aa94e4081143353566a037e89ef193e027d3c772d25b995e4b507ffc2d418bda` | 0 |
| crates/script/src/verify/external.rs | 58203 | `392679e795e700b5882f603654a14da6c9a565683509a4c517a074e3617bbe93` | 0 |
| crates/script/src/verify.rs | 32812 | `847b8a04da7c039f77bfe264abb8a8d31eb7e30370b15f27561889d176c1e709` | 0 |
| crates/script/src/wallet_session.rs | 29277 | `6baae13c8664cb4a3e39f9cf8458c88bd470a49778cd349bfecbdd4e401a0cb9` | 0 |
| crates/script-sequence/Cargo.toml | 766 | `e74f225bc1a0fe0fbfe8ca2b61c60b5c60150ffc823201b036d544818ae65fbe` | 0 |
| crates/script-sequence/src/lib.rs | 260 | `f652ab0fd28980c616becb2cc357c1693616378fb130eec2f135714d5e957bee` | 0 |
| crates/script-sequence/src/reader.rs | 11123 | `eb8e4d54cb9aec43e40e3cc143c93520c6d31ad2db495c2067713d4ff04ef6d7` | 0 |
| crates/script-sequence/src/sequence.rs | 14333 | `7bf6e2e60cb6ac2adbc18d0ad1987b22bdd6a67293d7912f74983738d36b4afc` | 0 |
| crates/script-sequence/src/transaction.rs | 3955 | `76799914b6eef6385eb8a49378be60d5b8a914224d2619f8cc2d9b578bdf818c` | 0 |
| crates/sol-macro-gen/Cargo.toml | 816 | `47c8ee55ac9c87a14b1b748d236800595aeb4c258df94c1b2fa2206c608e68d7` | 0 |
| crates/sol-macro-gen/src/lib.rs | 195 | `c0f12be28450e726aa8940f4bcec1526323ff839fd41947a4ce35014467874d3` | 0 |
| crates/sol-macro-gen/src/sol_macro_gen.rs | 21388 | `5e44967fe23257f390a3dd5757e9275fd7635eb87618699d7a5c0d789045456a` | 0 |
| crates/solar/Cargo.toml | 569 | `d89e5f3a5b79cb66d31ab375b10272afb24c7506580e3cd47ac692fe58767c27` | 0 |
| crates/solar/bin/main.rs | 169 | `14b2dea020c8b3f4658c4ebbc4f06bce66ba4daf473909d47e4e5c41ad5c8e19` | 0 |
| crates/tui/Cargo.toml | 342 | `4c9957610ddf05709e9c5729f6a4f1c0d99874eb19206e23b2ab71c215b0ead8` | 0 |
| crates/tui/src/lib.rs | 8274 | `deec2ae2c481c4d3505826bb483e0993353c001ba7cfe868ef310dee204ba134` | 0 |
| crates/verify/Cargo.toml | 2039 | `8fa3337bc9f47eba742f6f710bf1123f7fc90c6982d2327320866a03288fffd7` | 0 |
| crates/verify/src/bytecode.rs | 51201 | `f7f67545c4a3657efe584fdc0e1aabda37a27ea62e56a309f6cb5c8bf0c13d09` | 0 |
| crates/verify/src/etherscan/flatten.rs | 4334 | `031b67f756fd01253e74232ee8c3ccbea201e4aaab4cac02e94df81c3af2863b` | 0 |
| crates/verify/src/etherscan/mod.rs | 30508 | `ff7bf3fb1ce0904ffa3dccc92450588f81275fb3c69c0977a5248e1a0c63cbaf` | 0 |
| crates/verify/src/etherscan/standard_json.rs | 1620 | `3ec88d7335fea8535cf02f4893f972fb21a4223a18607583576f63257c5c1a52` | 0 |
| crates/verify/src/lib.rs | 494 | `077d2bede5603e2acb5e872ad544f6fab1e656f161ae900207ce6242b22b5a3f` | 0 |
| crates/verify/src/provider.rs | 15310 | `89f85fc9afe2a58e30bd41a7b429e38dafb445d7e28ea0755f8738cdfc9d2de9` | 0 |
| crates/verify/src/retry.rs | 1885 | `f5e4f0c9c42d3564aa0507c7eb47d3d5b0781f17387322cae94ab6c830324526` | 0 |
| crates/verify/src/sourcify.rs | 24485 | `2d4f708d205b7d31826124b7789727d0f45c62ae9d54d6ce0ea456f914d7a17b` | 0 |
| crates/verify/src/types.rs | 1004 | `e563b8b6e5f129bdb8ac174324fb5e45aa7e71769b52e0ee63a9d11d39a6d63a` | 0 |
| crates/verify/src/utils.rs | 31548 | `26ee38efe4ee2abbc28119223e2ec1428bf2f0825f3aadf977eed4d96fc9c0ad` | 0 |
| crates/verify/src/verify.rs | 55099 | `cd8748d191b2599e8a9a7325b8267b89741307140df9f108b572ef9275da7803` | 0 |
| editors/prepare-vscode.mjs | 1981 | `e5def9c17b066937f5674d882a81e9b31fb880829b9a22a079f5c7e6fb96e53d` | 0 |
| editors/vscode/package-lock.json | 215779 | `384e98f8ab8f2565e3f8c014ea98fd157a3bbbbc2ff5cd1c8075a68599e560cb` | 0 |
| editors/vscode/package.json | 7794 | `53ba2a22c770693b368f372f649ab8d34de71954afa48dac4932acf53ef53ada` | 0 |
| editors/vscode/scripts/bundle.mjs | 3639 | `724796c36d1c56c3ac73588d5a0b3a7f3612de0e580d1882d970c09f36e9a371` | 0 |
| editors/vscode/scripts/package.mjs | 2034 | `0d383bbb37c491eaacbf9610dd92bed0a1f5f23c414a8c58b00ff45cc6a3abd7` | 0 |
| editors/vscode/scripts/test-host.cjs | 6185 | `9b0b01e4f00c7790d8c095809367842ad8de9604122497ea018e6a0f65ee030e` | 0 |
| editors/vscode/src/extension.ts | 16555 | `b9d017e50c1f39f5ca37c3932851966926be874ac81a2b217f4cd27597353c28` | 0 |
| editors/vscode/src/forge.ts | 3456 | `13c38d9db2a9f94d58b71341fa01885c41e4cf787cd6d50cb5559ca587ef47f4` | 0 |
| editors/zed/Cargo.lock | 21078 | `e6c2c91373afdcef336e792304d205e657e6110cbade0af0137f5fef73c783f5` | 0 |
| editors/zed/Cargo.toml | 183 | `204feff22f5783f07891f230a27aaa6cbfc56fe29554208d7cb9f2e0bdd2cd9c` | 0 |
| editors/zed/src/lib.rs | 10465 | `c256e49a3b6719909e51c47617c3d735c7514c17c0e355563f3624b6a5bd9d70` | 0 |
