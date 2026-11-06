# Security & Post-Quantum Readiness Audit Report

**Project:** stellar-core @ 362dbc5184c5 · Stellar Development Foundation — public repository (passive review)
| | |
|---|---|
| Organization | QSI |
| Report date | 2026-11-06 16:13 UTC |
| Report version | 1 |
| Audit run | b0f4a6ed-9255-4307-8ee5-a8714e875faf (Document audit) |
| Analyzer engine | qsi-engine 1.3.0 |
| Risk profile | Crypto exchange, custodian or wallet |
| Content SHA-256 | `f327ba1b869fa8b4294a76c06b8c8cab443e20fce8fcaa92ea2b8a6bee57463e` |
| Signature key (Ed25519, SHA-256 fingerprint; the signature is the separate file report.sig.json) | `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e` |
> This report presents automated and documented analysis results for the stated scope. It is not a legal opinion, a certification or an attestation of compliance with any standard.

## 1. Executive summary

- Critical: **0**
- High: **3**
- Medium: **24**
- Low: **18**
- Info: **5**

- Confirmed technical vulnerability: 0
- Known vulnerable component: 32
- Confirmed configuration error: 2
- Potential cryptographic risk: 3
- Long-term post-quantum risk: 8
- Improvement recommendation: 5
- Insufficient data: 0

Mosca's inequality (x + y > z): x = 10, y = 5, z = 8 → migration would finish too late under this scenario. _z is a planning assumption chosen per risk profile, not a prediction. A cryptographically relevant quantum computer is not publicly known to exist today._

**Post-quantum maturity: Level 1 of 4 — post-quantum code present, not wired.** Next step: Wire the existing post-quantum primitive into a critical path (key wrapping or the channel) behind a hybrid construction, and test interoperability.

## 2. Scope and boundaries

Mode: Document audit

Repository: <https://github.com/stellar/stellar-core> @ `362dbc5184c5fdc0d6e898f3046639dc5e2a4f32` — evidence links open the lines at this commit.

3388 files, 52428740 bytes in total, 2 redaction(s); the per-file SHA-256 list is in appendix C.

## 3. Methodology

| Area | Status | Count | Examples |
|---|---|---|---|
| dependencies | checked | 148 | Cargo.lock: 288 dependencies parsed (288 pinned); Cargo.toml: 0 dependencies parsed (0 pinned); scripts/apply_load/token/Cargo.lock: 184 dependencies parsed (184 pinned) |
| source_code | checked | 3231 | lib/asio.cpp: 2 lines scanned with 16 rule patterns and 267 registry patterns; lib/autocheck/include/autocheck/arbitrary.hpp: 133 lines scanned with 16 rule patterns and 267 registry patterns; lib/autocheck/include/autocheck/autocheck.hpp: 5 lines scanned with 16 rule patterns and 267 registry patterns |
| tls_key_exchange_groups | Insufficient data | 1 | lib/fmt/support/docopt.py line 80: not in the algorithm registry, not assessed: [[pattern]] |
| tls_configuration | checked | 1 | lib/fmt/support/docopt.py: openssl TLS directives parsed |
| entropy | checked | 1 | random-number generation: 3227 code files read with 6405 macro definitions from the tree; 0 ineffective guard(s), 0 weak random-bytes provider(s), 1 weak key-generation site(s) |
| osv_advisories | not checked | 1 | 14 package(s) are built from git repositories (forks or unreleased code), so registry advisories were not looked up for them: soroban-builtin-sdk-macros, soroban-env-common, soroban-env-host, soroban-env-macros, soroban-fuzz-targets, soroban-synth-wasm, soroban-test-wasms, soroban-wasmi, stellar-quorum-analyzer, stellar-strkey, stellar-xdr, wasmi_arena … |
| osv_advisories | checked | 1 | 575 pinned packages queried at OSV.dev; 36 affected |

_Long lists are grouped here; the full per-file list is in the JSON report, signed with the same key._

## 4. Assets examined and not examined

- tls_key_exchange_groups — Insufficient data: lib/fmt/support/docopt.py line 80: not in the algorithm registry, not assessed: [[pattern]]
- osv_advisories — not checked: 14 package(s) are built from git repositories (forks or unreleased code), so registry advisories were not looked up for them: soroban-builtin-sdk-macros, soroban-env-common, soroban-env-host, soroban-env-macros, soroban-fuzz-targets, soroban-synth-wasm, soroban-test-wasms, soroban-wasmi, stellar-quorum-analyzer, stellar-strkey, stellar-xdr, wasmi_arena …

## 5. Architecture overview

Static review of the source tree stellar-core at 362dbc5184c5fdc0d6e898f3046639dc5e2a4f32. 3388 files analysed; of 27064 files, 5182 are test, fuzzing, benchmark or example code and were left out, 16879 are not read by any analyzer, 0 exceed the per-file limit and 1615 did not fit the total limit. Files no analyzer reads include: .clang-format, .claude/skills/adding-a-new-skill/SKILL.md, .claude/skills/configuring-the-build/SKILL.md, .claude/skills/high-level-code-review/SKILL.md, .claude/skills/low-level-code-review/SKILL.md. Because the total limit bound, this inventory covers 3388 of 27064 candidate files (12%) and is a sample of the tree rather than a reading of it; a different limit gives a different figure. Files it could not fit include: lib/tracy/server/TracyMicroArchitecture.cpp, src/rust/soroban/p24/soroban-env-host/src/host/metered_vector.rs, src/rust/soroban/p24/soroban-env-host/src/host/prng.rs, src/rust/soroban/p24/soroban-env-host/src/host/trace.rs, src/rust/soroban/p24/soroban-env-host/src/host/trace/fmt.rs. 765 files in build-output or dependency-cache directories (.git, .hg, .venv, __pycache__, build, dist, node_modules, target, vendor, venv) were not read. 2628 files come from directories a .gitmodules pins and are read as shipped source rather than skipped as a dependency cache: lib/asio (596), lib/tracy (344), lib/gperftools (240), lib/libsodium (240). No requests were sent to the owner's systems.

## 6. Overall security posture

- Indicative posture index: **0** / 100 — _Derived from findings in scope (confirmed and potential issues weighted by severity). Indicative only; not comparable across differently scoped audits._
- Quantum-vulnerable share of inventory: 42.0%

## 7. Detailed findings

### QSI-2026-19575 — Possible hard-coded secret in lib/sqlite/sqlite3.c

- Severity: **High** · Classification: Confirmed configuration error · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `file:lib/sqlite/sqlite3.c`
- Data source: lib/sqlite/sqlite3.c
- Detection method: Regular-expression matching of language-specific API patterns.
- Analyzer: source_code 1.3.0 · 2026-11-06 16:13 UTC
- Priority score: 47.1 / 100
- CVSS v3.1: not applicable

1 secret-like value(s) of type generic_assignment (first at line 106875). Values were redacted by QSI.

**Potential impact.** Credentials in source code leak through repositories, builds and logs.

**Reproduction steps.**

```
Open line 106875 in the supplied file lib/sqlite/sqlite3.c and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [lib/sqlite/sqlite3.c](https://github.com/stellar/stellar-core/blob/362dbc5184c5fdc0d6e898f3046639dc5e2a4f32/lib/sqlite/sqlite3.c#L106875) · line 106875 · SHA-256 de26a7a3e0a3f23bfd9c62f2cb070092564c702ea1a0f38afede9fd0e2535879_

```
106875 |         pExpr->u.zToken = "[REDACTED]";
```

**Limitations of the check.** Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Move secrets to a secrets manager/environment; rotate the exposed values.

**Retest procedure.** Re-scan the source and review the call sites listed in the evidence.

### QSI-2026-19582 — Possible hard-coded secret in lib/tracy/nfd/nfd_portal.cpp

- Severity: **High** · Classification: Confirmed configuration error · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `file:lib/tracy/nfd/nfd_portal.cpp`
- Data source: lib/tracy/nfd/nfd_portal.cpp
- Detection method: Regular-expression matching of language-specific API patterns.
- Analyzer: source_code 1.3.0 · 2026-11-06 16:13 UTC
- Priority score: 47.1 / 100
- CVSS v3.1: not applicable

1 secret-like value(s) of type generic_assignment (first at line 123). Values were redacted by QSI.

**Potential impact.** Credentials in source code leak through repositories, builds and logs.

**Reproduction steps.**

```
Open line 123 in the supplied file lib/tracy/nfd/nfd_portal.cpp and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [lib/tracy/nfd/nfd_portal.cpp](https://github.com/stellar/stellar-core/blob/362dbc5184c5fdc0d6e898f3046639dc5e2a4f32/lib/tracy/nfd/nfd_portal.cpp#L123) · line 123 · SHA-256 5cadec8ca1b53a8e78eb14b6fc15f0ad53008a4572baa20c6c53275e7030af72_

```
  123 | constexpr const char* STR_HANDLE_TOKEN = "[REDACTED]";
```

**Limitations of the check.** Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Move secrets to a secrets manager/environment; rotate the exposed values.

**Retest procedure.** Re-scan the source and review the call sites listed in the evidence.

### QSI-2026-19587 — Non-cryptographic generator next to key or seed generation in src/crypto/SecretKey.h

- Severity: **High** · Classification: Potential cryptographic risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `src/crypto/SecretKey.h:keygen`
- Data source: src/crypto/SecretKey.h
- Detection method: Regular-expression matching of language-specific API patterns.
- Analyzer: entropy 1.3.0 · 2026-11-06 16:13 UTC
- Priority score: 38.8 / 100
- CVSS v3.1: not applicable

'random()' at line 59, within a few lines of 'SecretKey' (1 occurrence(s)).

**Potential impact.** Mnemonics, seeds or private keys drawn from such a generator can be enumerated from its small internal state: Milk Sad (CVE-2023-39910, mt19937 behind 'bx seed') and Trust Wallet (CVE-2023-31290) lost funds this way.

**Reproduction steps.**

```
Open line 59 in the supplied file src/crypto/SecretKey.h and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [src/crypto/SecretKey.h](https://github.com/stellar/stellar-core/blob/362dbc5184c5fdc0d6e898f3046639dc5e2a4f32/src/crypto/SecretKey.h#L59) · line 59 · SHA-256 bc0ec8d966e45191018568a3dc143537c92d2b044e33224b88851b7f0ba43366_

```
   57 | 
   58 |     // Create a new, random secret key.
   59 |     static SecretKey random();
   60 | 
   61 |     // Measure the speed of sign-and-verify ops.
```

**Limitations of the check.** Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Use the platform CSPRNG (secrets, os.urandom, crypto.getRandomValues, crypto/rand, SecureRandom, OsRng) or a hardware TRNG for every key, seed and mnemonic.

**Retest procedure.** Re-scan the source and review the call sites listed in the evidence.

### QSI-2026-19595 — stellar-xdr 21.2.0 is affected by GHSA-x57h-xx53-v53w (CVE-2026-29795)

- Severity: **Medium** · Classification: Known vulnerable component · Confidence: Medium
- Affected asset: `dependency:crates.io/stellar-xdr@21.2.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 16:13 UTC
- Priority score: 44.2 / 100
- CVSS v3.1: 4.0 (`CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:N`)

OSV.dev reports GHSA-x57h-xx53-v53w (CVE-2026-29795) for crates.io package stellar-xdr at version 21.2.0: stellar-xdr's StringM::from_str bypasses max length validation. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-x57h-xx53-v53w
```

**Evidence.**

_tool_output · [OSV.dev GHSA-x57h-xx53-v53w](https://osv.dev/vulnerability/GHSA-x57h-xx53-v53w) · manifest · SHA-256 8303f2513b789fb23ce8020249b81fdaf696f193dc0ce9ed3044b8b855ed10ea_

```
{"id": "GHSA-x57h-xx53-v53w", "aliases": ["CVE-2026-29795"], "modified": "2026-03-06T23:02:40.557695Z", "summary": "stellar-xdr's StringM::from_str bypasses max length validation", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:N"}], "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (25.0.1).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-19596 — stellar-xdr 22.0.0 is affected by GHSA-x57h-xx53-v53w (CVE-2026-29795)

- Severity: **Medium** · Classification: Known vulnerable component · Confidence: Medium
- Affected asset: `dependency:crates.io/stellar-xdr@22.0.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 16:13 UTC
- Priority score: 44.2 / 100
- CVSS v3.1: 4.0 (`CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:N`)

OSV.dev reports GHSA-x57h-xx53-v53w (CVE-2026-29795) for crates.io package stellar-xdr at version 22.0.0: stellar-xdr's StringM::from_str bypasses max length validation. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-x57h-xx53-v53w
```

**Evidence.**

_tool_output · [OSV.dev GHSA-x57h-xx53-v53w](https://osv.dev/vulnerability/GHSA-x57h-xx53-v53w) · manifest · SHA-256 8303f2513b789fb23ce8020249b81fdaf696f193dc0ce9ed3044b8b855ed10ea_

```
{"id": "GHSA-x57h-xx53-v53w", "aliases": ["CVE-2026-29795"], "modified": "2026-03-06T23:02:40.557695Z", "summary": "stellar-xdr's StringM::from_str bypasses max length validation", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:N"}], "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (25.0.1).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-19597 — stellar-xdr 23.0.0 is affected by GHSA-x57h-xx53-v53w (CVE-2026-29795)

- Severity: **Medium** · Classification: Known vulnerable component · Confidence: Medium
- Affected asset: `dependency:crates.io/stellar-xdr@23.0.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 16:13 UTC
- Priority score: 44.2 / 100
- CVSS v3.1: 4.0 (`CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:N`)

OSV.dev reports GHSA-x57h-xx53-v53w (CVE-2026-29795) for crates.io package stellar-xdr at version 23.0.0: stellar-xdr's StringM::from_str bypasses max length validation. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-x57h-xx53-v53w
```

**Evidence.**

_tool_output · [OSV.dev GHSA-x57h-xx53-v53w](https://osv.dev/vulnerability/GHSA-x57h-xx53-v53w) · manifest · SHA-256 8303f2513b789fb23ce8020249b81fdaf696f193dc0ce9ed3044b8b855ed10ea_

```
{"id": "GHSA-x57h-xx53-v53w", "aliases": ["CVE-2026-29795"], "modified": "2026-03-06T23:02:40.557695Z", "summary": "stellar-xdr's StringM::from_str bypasses max length validation", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:N"}], "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (25.0.1).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-19598 — stellar-xdr 24.0.0 is affected by GHSA-x57h-xx53-v53w (CVE-2026-29795)

- Severity: **Medium** · Classification: Known vulnerable component · Confidence: Medium
- Affected asset: `dependency:crates.io/stellar-xdr@24.0.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 16:13 UTC
- Priority score: 44.2 / 100
- CVSS v3.1: 4.0 (`CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:N`)

OSV.dev reports GHSA-x57h-xx53-v53w (CVE-2026-29795) for crates.io package stellar-xdr at version 24.0.0: stellar-xdr's StringM::from_str bypasses max length validation. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-x57h-xx53-v53w
```

**Evidence.**

_tool_output · [OSV.dev GHSA-x57h-xx53-v53w](https://osv.dev/vulnerability/GHSA-x57h-xx53-v53w) · manifest · SHA-256 8303f2513b789fb23ce8020249b81fdaf696f193dc0ce9ed3044b8b855ed10ea_

```
{"id": "GHSA-x57h-xx53-v53w", "aliases": ["CVE-2026-29795"], "modified": "2026-03-06T23:02:40.557695Z", "summary": "stellar-xdr's StringM::from_str bypasses max length validation", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:N"}], "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (25.0.1).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-19615 — stellar-xdr 20.1.0 is affected by GHSA-x57h-xx53-v53w (CVE-2026-29795)

- Severity: **Medium** · Classification: Known vulnerable component · Confidence: Medium
- Affected asset: `dependency:crates.io/stellar-xdr@20.1.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 16:13 UTC
- Priority score: 44.2 / 100
- CVSS v3.1: 4.0 (`CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:N`)

OSV.dev reports GHSA-x57h-xx53-v53w (CVE-2026-29795) for crates.io package stellar-xdr at version 20.1.0: stellar-xdr's StringM::from_str bypasses max length validation. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-x57h-xx53-v53w
```

**Evidence.**

_tool_output · [OSV.dev GHSA-x57h-xx53-v53w](https://osv.dev/vulnerability/GHSA-x57h-xx53-v53w) · manifest · SHA-256 8303f2513b789fb23ce8020249b81fdaf696f193dc0ce9ed3044b8b855ed10ea_

```
{"id": "GHSA-x57h-xx53-v53w", "aliases": ["CVE-2026-29795"], "modified": "2026-03-06T23:02:40.557695Z", "summary": "stellar-xdr's StringM::from_str bypasses max length validation", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:N"}], "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (25.0.1).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-19617 — soroban-sdk 21.4.0 is affected by GHSA-96xm-fv9w-pf3f (CVE-2026-24889)

- Severity: **Medium** · Classification: Known vulnerable component · Confidence: Medium
- Affected asset: `dependency:crates.io/soroban-sdk@21.4.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 16:13 UTC
- Priority score: 44.2 / 100
- CVSS v3.1: 5.3 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:N`)

OSV.dev reports GHSA-96xm-fv9w-pf3f (CVE-2026-24889) for crates.io package soroban-sdk at version 21.4.0: soroban-sdk has overflow in Bytes::slice, Vec::slice, GenRange::gen_range for u64. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-96xm-fv9w-pf3f
```

**Evidence.**

_tool_output · [OSV.dev GHSA-96xm-fv9w-pf3f](https://osv.dev/vulnerability/GHSA-96xm-fv9w-pf3f) · manifest · SHA-256 5b23dbea201762df014224d30d1230a1d84fab5f03c2e79f87537d1c8c42bab0_

```
{"id": "GHSA-96xm-fv9w-pf3f", "aliases": ["CVE-2026-24889"], "modified": "2026-02-03T03:04:15.587576Z", "summary": "soroban-sdk has overflow in Bytes::slice, Vec::slice, GenRange::gen_range for u64", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:N"}], "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (22.0.9, 23.5.1, 25.0.2).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-19618 — soroban-sdk 21.4.0 is affected by GHSA-x2hw-px52-wp4m (CVE-2026-32322)

- Severity: **Medium** · Classification: Known vulnerable component · Confidence: Medium
- Affected asset: `dependency:crates.io/soroban-sdk@21.4.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 16:13 UTC
- Priority score: 44.2 / 100
- CVSS v3.1: 5.3 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:N`)

OSV.dev reports GHSA-x2hw-px52-wp4m (CVE-2026-32322) for crates.io package soroban-sdk at version 21.4.0: rs-soroban-sdk: `Fr` scalar field equality comparison bypasses modular reduction. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-x2hw-px52-wp4m
```

**Evidence.**

_tool_output · [OSV.dev GHSA-x2hw-px52-wp4m](https://osv.dev/vulnerability/GHSA-x2hw-px52-wp4m) · manifest · SHA-256 73de902765c346e5f5eb0e174c0654bdef6b7e36fde6663bd43958d99a5e564e_

```
{"id": "GHSA-x2hw-px52-wp4m", "aliases": ["CVE-2026-32322"], "modified": "2026-03-16T17:16:39.585918Z", "summary": "rs-soroban-sdk: `Fr` scalar field equality comparison bypasses modular reduction", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:N"}], "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (22.0.11, 23.5.3, 25.3.0).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-19623 — stellar-xdr 23.0.0-rc.2 is affected by GHSA-x57h-xx53-v53w (CVE-2026-29795)

- Severity: **Medium** · Classification: Known vulnerable component · Confidence: Medium
- Affected asset: `dependency:crates.io/stellar-xdr@23.0.0-rc.2`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 16:13 UTC
- Priority score: 44.2 / 100
- CVSS v3.1: 4.0 (`CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:N`)

OSV.dev reports GHSA-x57h-xx53-v53w (CVE-2026-29795) for crates.io package stellar-xdr at version 23.0.0-rc.2: stellar-xdr's StringM::from_str bypasses max length validation. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-x57h-xx53-v53w
```

**Evidence.**

_tool_output · [OSV.dev GHSA-x57h-xx53-v53w](https://osv.dev/vulnerability/GHSA-x57h-xx53-v53w) · manifest · SHA-256 8303f2513b789fb23ce8020249b81fdaf696f193dc0ce9ed3044b8b855ed10ea_

```
{"id": "GHSA-x57h-xx53-v53w", "aliases": ["CVE-2026-29795"], "modified": "2026-03-06T23:02:40.557695Z", "summary": "stellar-xdr's StringM::from_str bypasses max length validation", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:N"}], "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (25.0.1).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-19581 — Quantum-vulnerable X25519: key wrapping and data encryption at rest (1 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:X25519:key_wrapping`
- Data source: lib/libsodium/src/libsodium/crypto_box/crypto_box_seal.c
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.3.0 · 2026-11-06 16:13 UTC
- Priority score: 36.9 / 100
- CVSS v3.1: not applicable

1 reference(s) to X25519 across 1 file(s), e.g. lib/libsodium/src/libsodium/crypto_box/crypto_box_seal.c:32. Role, judged from paths, function names and nearby code: key wrapping and data encryption at rest. Keys or data encrypted to these public keys are stored: anyone who copies them now decrypts them once a CRQC exists (harvest now, decrypt later).

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open lib/libsodium/src/libsodium/crypto_box/crypto_box_seal.c:32 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [lib/libsodium/src/libsodium/crypto_box/crypto_box_seal.c](https://github.com/stellar/stellar-core/blob/362dbc5184c5fdc0d6e898f3046639dc5e2a4f32/lib/libsodium/src/libsodium/crypto_box/crypto_box_seal.c#L32) · line 32 · SHA-256 7639098c5e359f826c9a3a9916473df34aeaeacbae782ff962a91a2774a1d37e_

```
   31 | 
   32 |     if (crypto_box_keypair(epk, esk) != 0) {
   33 |         return -1; /* LCOV_EXCL_LINE */
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Wrap keys with ML-KEM or a hybrid KEM (X25519 + ML-KEM-768) and re-wrap the stored keys; data that may already have been copied needs its own assessment.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-19579 — Quantum-vulnerable Ed25519: transaction and message signing (12 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:Ed25519:transaction_signing`
- Data source: src/crypto/SignerKey.cpp
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.3.0 · 2026-11-06 16:13 UTC
- Priority score: 35.6 / 100
- CVSS v3.1: not applicable

20 reference(s) to Ed25519 across 12 file(s), e.g. src/crypto/SignerKey.cpp:132. Role, judged from paths, function names and nearby code: transaction and message signing. A CRQC derives the private key from a public key that is already known (on chain after the first spend, in reused addresses): funds and approvals controlled by these keys need a migration path.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open src/crypto/SignerKey.cpp:132 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [src/crypto/SignerKey.cpp](https://github.com/stellar/stellar-core/blob/362dbc5184c5fdc0d6e898f3046639dc5e2a4f32/src/crypto/SignerKey.cpp#L132) · line 132 · SHA-256 55320a5111bb845641cd3e68aeb57ffb77a6e9294fa88f8046fa6d0083abea39_

```
  131 |     case SIGNER_KEY_TYPE_ED25519_SIGNED_PAYLOAD:
  132 |         return xdr::xdr_to_opaque(key.ed25519SignedPayload());
  133 |     default:
```

_file_excerpt · [src/crypto/SignerKey.cpp](https://github.com/stellar/stellar-core/blob/362dbc5184c5fdc0d6e898f3046639dc5e2a4f32/src/crypto/SignerKey.cpp#L154) · line 154 · SHA-256 6d485aa3aa7f4ffe676072fb23b0c7f2fb686eefbfd8d8457075d5100e4bfa36_

```
  153 |     case SIGNER_KEY_TYPE_ED25519_SIGNED_PAYLOAD:
  154 |         xdr::xdr_from_opaque(data, key.ed25519SignedPayload());
  155 |         break;
```

_file_excerpt · [src/crypto/SignerKeyUtils.cpp](https://github.com/stellar/stellar-core/blob/362dbc5184c5fdc0d6e898f3046639dc5e2a4f32/src/crypto/SignerKeyUtils.cpp#L49) · line 49 · SHA-256 8643c711faca4c8589ff5d4541d26085ab2d6e0059e10e7b1a75747a7d8a4e6f_

```
   48 |     sk.type(SIGNER_KEY_TYPE_ED25519_SIGNED_PAYLOAD);
   49 |     sk.ed25519SignedPayload().ed25519 = ed25519;
   50 |     sk.ed25519SignedPayload().payload = payload;
```

_file_excerpt · [src/crypto/SignerKeyUtils.cpp](https://github.com/stellar/stellar-core/blob/362dbc5184c5fdc0d6e898f3046639dc5e2a4f32/src/crypto/SignerKeyUtils.cpp#L50) · line 50 · SHA-256 a7d1bd48bb0ab8c7a7234731a1e81bd608b24b607393b88607edeb996997887c_

```
   49 |     sk.ed25519SignedPayload().ed25519 = ed25519;
   50 |     sk.ed25519SignedPayload().payload = payload;
   51 |     return sk;
```

_file_excerpt · [src/transactions/SetOptionsOpFrame.cpp](https://github.com/stellar/stellar-core/blob/362dbc5184c5fdc0d6e898f3046639dc5e2a4f32/src/transactions/SetOptionsOpFrame.cpp#L311) · line 311 · SHA-256 61e1b04e4bf5c3a4445a6430af9e88b88636e729ac874f854f036edbe8ab91e4_

```
  310 |             (protocolVersionIsBefore(ledgerVersion, ProtocolVersion::V_19) ||
  311 |              mSetOptions.signer->key.ed25519SignedPayload().payload.empty()))
  312 |         {
```

_file_excerpt · [src/transactions/SignatureUtils.cpp](https://github.com/stellar/stellar-core/blob/362dbc5184c5fdc0d6e898f3046639dc5e2a4f32/src/transactions/SignatureUtils.cpp#L52) · line 52 · SHA-256 7730f215f0e85488f379e08fc5cf75104023e34ca3fdbae315623c4dc11c6d97_

```
   51 | {
   52 |     auto const& signedPayload = signer.ed25519SignedPayload();
   53 | 
```

_file_excerpt · [src/transactions/TransactionFrame.cpp](https://github.com/stellar/stellar-core/blob/362dbc5184c5fdc0d6e898f3046639dc5e2a4f32/src/transactions/TransactionFrame.cpp#L1290) · line 1290 · SHA-256 2be00e4259f9423243c7d2713aa9363489e71c66f3adec9ccd8e79354c7ec64c_

```
 1289 |             if (signer.type() == SIGNER_KEY_TYPE_ED25519_SIGNED_PAYLOAD &&
 1290 |                 signer.ed25519SignedPayload().payload.empty())
 1291 |             {
```

_file_excerpt · [src/rust/soroban/p21/soroban-env-host/src/builtin_contracts/stellar_asset_contract/metadata.rs](https://github.com/stellar/stellar-core/blob/362dbc5184c5fdc0d6e898f3046639dc5e2a4f32/src/rust/soroban/p21/soroban-env-host/src/builtin_contracts/stellar_asset_contract/metadata.rs#L158) · line 158 · SHA-256 3d7fb8af17a8920210188c6a4caffc601f7bc324ca0d4bb4d80a92121e56c790_

```
  157 |     s.push(':');
  158 |     s.push_str(&ed25519::PublicKey(issuer.to_array()?).to_string());
  159 |     let name = String::try_from_val(e, &e.string_new_from_slice(s.as_bytes())?)?;
```

_file_excerpt · [src/rust/soroban/p21/soroban-env-host/src/testutils.rs](https://github.com/stellar/stellar-core/blob/362dbc5184c5fdc0d6e898f3046639dc5e2a4f32/src/rust/soroban/p21/soroban-env-host/src/testutils.rs#L14) · line 14 · SHA-256 31181acc71844a88e7c8356ff1e5659de5d5240265a0a0bdb8295af30158cc37_

```
   13 | };
   14 | use ed25519_dalek::SigningKey;
   15 | use rand::RngCore;
```

_file_excerpt · [src/rust/soroban/p21/soroban-env-host/src/testutils.rs](https://github.com/stellar/stellar-core/blob/362dbc5184c5fdc0d6e898f3046639dc5e2a4f32/src/rust/soroban/p21/soroban-env-host/src/testutils.rs#L309) · line 309 · SHA-256 fc3690b3ba7ca3c5613563bacdf14b5c265ca7e42f9e4bcff56717585a7e8a3f_

```
  308 |         n_signers: usize,
  309 |     ) -> (Host, Vec<AddressObject>, Vec<ed25519_dalek::SigningKey>) {
  310 |         use crate::builtin_contracts::testutils::{
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains adopt them.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-19583 — Quantum-vulnerable ECDSA: transaction and message signing (8 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:ECDSA:transaction_signing`
- Data source: src/rust/soroban/p21/soroban-env-host/src/cost_runner/cost_types/recover_ecdsa_secp256k1_key.rs
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.3.0 · 2026-11-06 16:13 UTC
- Priority score: 35.6 / 100
- CVSS v3.1: not applicable

12 reference(s) to ECDSA across 8 file(s), e.g. src/rust/soroban/p21/soroban-env-host/src/cost_runner/cost_types/recover_ecdsa_secp256k1_key.rs:7. Role, judged from paths, function names and nearby code: transaction and message signing. A CRQC derives the private key from a public key that is already known (on chain after the first spend, in reused addresses): funds and approvals controlled by these keys need a migration path.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open src/rust/soroban/p21/soroban-env-host/src/cost_runner/cost_types/recover_ecdsa_secp256k1_key.rs:7 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [src/rust/soroban/p21/soroban-env-host/src/cost_runner/cost_types/recover_ecdsa_secp256k1_key.rs](https://github.com/stellar/stellar-core/blob/362dbc5184c5fdc0d6e898f3046639dc5e2a4f32/src/rust/soroban/p21/soroban-env-host/src/cost_runner/cost_types/recover_ecdsa_secp256k1_key.rs#L7) · line 7 · SHA-256 92080872f39f646ca72af7f62a1a86aafc23f66369b0c021ba531097dc6e1f43_

```
    6 | };
    7 | use k256::ecdsa::{RecoveryId, Signature};
    8 | 
```

_file_excerpt · [src/rust/soroban/p21/soroban-env-host/src/cost_runner/cost_types/recover_ecdsa_secp256k1_key.rs](https://github.com/stellar/stellar-core/blob/362dbc5184c5fdc0d6e898f3046639dc5e2a4f32/src/rust/soroban/p21/soroban-env-host/src/cost_runner/cost_types/recover_ecdsa_secp256k1_key.rs#L28) · line 28 · SHA-256 f3357cb7a595c1e3ce6deec4fed0973bae3735ea3092adff5321706ae9d88f8c_

```
   27 |             host.recover_key_ecdsa_secp256k1_internal(&sample.hash, &sample.sig, sample.rid)
   28 |                 .expect("recover ecdsa secp256k1 key"),
   29 |         );
```

_file_excerpt · [src/rust/soroban/p21/soroban-env-host/src/cost_runner/experimental/ecdsa_secp256k1_verify.rs](https://github.com/stellar/stellar-core/blob/362dbc5184c5fdc0d6e898f3046639dc5e2a4f32/src/rust/soroban/p21/soroban-env-host/src/cost_runner/experimental/ecdsa_secp256k1_verify.rs#L6) · line 6 · SHA-256 58340089301d1dbfa155c975109ed0bf7958615b3c0a53cda374c00df04c04a4_

```
    5 | };
    6 | use k256::ecdsa::{Signature, VerifyingKey};
    7 | use std::hint::black_box;
```

_file_excerpt · [src/rust/soroban/p22/soroban-env-host/src/cost_runner/cost_types/recover_ecdsa_secp256k1_key.rs](https://github.com/stellar/stellar-core/blob/362dbc5184c5fdc0d6e898f3046639dc5e2a4f32/src/rust/soroban/p22/soroban-env-host/src/cost_runner/cost_types/recover_ecdsa_secp256k1_key.rs#L7) · line 7 · SHA-256 92080872f39f646ca72af7f62a1a86aafc23f66369b0c021ba531097dc6e1f43_

```
    6 | };
    7 | use k256::ecdsa::{RecoveryId, Signature};
    8 | 
```

_file_excerpt · [src/rust/soroban/p22/soroban-env-host/src/cost_runner/cost_types/recover_ecdsa_secp256k1_key.rs](https://github.com/stellar/stellar-core/blob/362dbc5184c5fdc0d6e898f3046639dc5e2a4f32/src/rust/soroban/p22/soroban-env-host/src/cost_runner/cost_types/recover_ecdsa_secp256k1_key.rs#L28) · line 28 · SHA-256 f3357cb7a595c1e3ce6deec4fed0973bae3735ea3092adff5321706ae9d88f8c_

```
   27 |             host.recover_key_ecdsa_secp256k1_internal(&sample.hash, &sample.sig, sample.rid)
   28 |                 .expect("recover ecdsa secp256k1 key"),
   29 |         );
```

_file_excerpt · [src/rust/soroban/p22/soroban-env-host/src/cost_runner/experimental/ecdsa_secp256k1_verify.rs](https://github.com/stellar/stellar-core/blob/362dbc5184c5fdc0d6e898f3046639dc5e2a4f32/src/rust/soroban/p22/soroban-env-host/src/cost_runner/experimental/ecdsa_secp256k1_verify.rs#L6) · line 6 · SHA-256 58340089301d1dbfa155c975109ed0bf7958615b3c0a53cda374c00df04c04a4_

```
    5 | };
    6 | use k256::ecdsa::{Signature, VerifyingKey};
    7 | use std::hint::black_box;
```

_file_excerpt · [src/rust/soroban/p23/soroban-env-host/src/cost_runner/cost_types/recover_ecdsa_secp256k1_key.rs](https://github.com/stellar/stellar-core/blob/362dbc5184c5fdc0d6e898f3046639dc5e2a4f32/src/rust/soroban/p23/soroban-env-host/src/cost_runner/cost_types/recover_ecdsa_secp256k1_key.rs#L7) · line 7 · SHA-256 92080872f39f646ca72af7f62a1a86aafc23f66369b0c021ba531097dc6e1f43_

```
    6 | };
    7 | use k256::ecdsa::{RecoveryId, Signature};
    8 | 
```

_file_excerpt · [src/rust/soroban/p23/soroban-env-host/src/cost_runner/cost_types/recover_ecdsa_secp256k1_key.rs](https://github.com/stellar/stellar-core/blob/362dbc5184c5fdc0d6e898f3046639dc5e2a4f32/src/rust/soroban/p23/soroban-env-host/src/cost_runner/cost_types/recover_ecdsa_secp256k1_key.rs#L28) · line 28 · SHA-256 f3357cb7a595c1e3ce6deec4fed0973bae3735ea3092adff5321706ae9d88f8c_

```
   27 |             host.recover_key_ecdsa_secp256k1_internal(&sample.hash, &sample.sig, sample.rid)
   28 |                 .expect("recover ecdsa secp256k1 key"),
   29 |         );
```

_file_excerpt · [src/rust/soroban/p23/soroban-env-host/src/cost_runner/experimental/ecdsa_secp256k1_verify.rs](https://github.com/stellar/stellar-core/blob/362dbc5184c5fdc0d6e898f3046639dc5e2a4f32/src/rust/soroban/p23/soroban-env-host/src/cost_runner/experimental/ecdsa_secp256k1_verify.rs#L6) · line 6 · SHA-256 58340089301d1dbfa155c975109ed0bf7958615b3c0a53cda374c00df04c04a4_

```
    5 | };
    6 | use k256::ecdsa::{Signature, VerifyingKey};
    7 | use std::hint::black_box;
```

_file_excerpt · [src/rust/soroban/p24/soroban-env-host/src/cost_runner/cost_types/recover_ecdsa_secp256k1_key.rs](https://github.com/stellar/stellar-core/blob/362dbc5184c5fdc0d6e898f3046639dc5e2a4f32/src/rust/soroban/p24/soroban-env-host/src/cost_runner/cost_types/recover_ecdsa_secp256k1_key.rs#L7) · line 7 · SHA-256 92080872f39f646ca72af7f62a1a86aafc23f66369b0c021ba531097dc6e1f43_

```
    6 | };
    7 | use k256::ecdsa::{RecoveryId, Signature};
    8 | 
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains adopt them.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-19577 — Quantum-vulnerable X25519: role not determined (9 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:X25519:general`
- Data source: src/crypto/Curve25519.cpp
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.3.0 · 2026-11-06 16:13 UTC
- Priority score: 34.2 / 100
- CVSS v3.1: not applicable

18 reference(s) to X25519 across 9 file(s), e.g. src/crypto/Curve25519.cpp:35. Role, judged from paths, function names and nearby code: role not determined. The code does not show what the keys protect; review decides the priority.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open src/crypto/Curve25519.cpp:35 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [src/crypto/Curve25519.cpp](https://github.com/stellar/stellar-core/blob/362dbc5184c5fdc0d6e898f3046639dc5e2a4f32/src/crypto/Curve25519.cpp#L35) · line 35 · SHA-256 34b5a7f361a2076f165704d19d6c8bc72a57bc0f04a50f154d86825ae7804ecb_

```
   34 |     Curve25519Public out;
   35 |     if (crypto_scalarmult_base(out.key.data(), sec.key.data()) != 0)
   36 |     {
```

_file_excerpt · [src/crypto/Curve25519.cpp](https://github.com/stellar/stellar-core/blob/362dbc5184c5fdc0d6e898f3046639dc5e2a4f32/src/crypto/Curve25519.cpp#L60) · line 60 · SHA-256 f99598248d34bcd27601da554c7848d301156064073d000fb82f753cc5220c7f_

```
   59 |     unsigned char q[crypto_scalarmult_BYTES];
   60 |     if (crypto_scalarmult(q, localSecret.key.data(), remotePublic.key.data()) !=
   61 |         0)
```

_file_excerpt · [lib/libsodium/src/libsodium/crypto_box/crypto_box.c](https://github.com/stellar/stellar-core/blob/362dbc5184c5fdc0d6e898f3046639dc5e2a4f32/lib/libsodium/src/libsodium/crypto_box/crypto_box.c#L72) · line 72 · SHA-256 c0013e4cf7927fd70e25378a8286496ad969d4b79b00df8c55a6e5409c688412_

```
   71 | int
   72 | crypto_box_keypair(unsigned char *pk, unsigned char *sk)
   73 | {
```

_file_excerpt · [lib/libsodium/src/libsodium/crypto_kx/crypto_kx.c](https://github.com/stellar/stellar-core/blob/362dbc5184c5fdc0d6e898f3046639dc5e2a4f32/lib/libsodium/src/libsodium/crypto_kx/crypto_kx.c#L7) · line 7 · SHA-256 b83e11b5df3ca6749d82125bb5fd506677971c2838c5fa944770caa7bf54b093_

```
    6 | #include "crypto_kx.h"
    7 | #include "crypto_scalarmult.h"
    8 | #include "private/common.h"
```

_file_excerpt · [lib/libsodium/src/libsodium/crypto_kx/crypto_kx.c](https://github.com/stellar/stellar-core/blob/362dbc5184c5fdc0d6e898f3046639dc5e2a4f32/lib/libsodium/src/libsodium/crypto_kx/crypto_kx.c#L19) · line 19 · SHA-256 e7a0f139312c3eacae72fffe977326fc3f794ebf892a4122f800b74e7814c806_

```
   18 |                        seed, crypto_kx_SEEDBYTES, NULL, 0);
   19 |     return crypto_scalarmult_base(pk, sk);
   20 | }
```

_file_excerpt · [lib/libsodium/src/libsodium/crypto_kx/crypto_kx.c](https://github.com/stellar/stellar-core/blob/362dbc5184c5fdc0d6e898f3046639dc5e2a4f32/lib/libsodium/src/libsodium/crypto_kx/crypto_kx.c#L23) · line 23 · SHA-256 5383dc5a21d6f55f1471d2781d4cf72a3ddd9273156da5e2c116be73263793ca_

```
   22 | int
   23 | crypto_kx_keypair(unsigned char pk[crypto_kx_PUBLICKEYBYTES],
   24 |                   unsigned char sk[crypto_kx_SECRETKEYBYTES])
```

_file_excerpt · [lib/libsodium/src/libsodium/crypto_scalarmult/crypto_scalarmult.c](https://github.com/stellar/stellar-core/blob/362dbc5184c5fdc0d6e898f3046639dc5e2a4f32/lib/libsodium/src/libsodium/crypto_scalarmult/crypto_scalarmult.c#L2) · line 2 · SHA-256 9e041e272488a8a0e015c3ed4d2f88cc794e4a4624edd654c3479fd30584e19e_

```
    1 | 
    2 | #include "crypto_scalarmult.h"
    3 | 
```

_file_excerpt · [lib/libsodium/src/libsodium/crypto_scalarmult/crypto_scalarmult.c](https://github.com/stellar/stellar-core/blob/362dbc5184c5fdc0d6e898f3046639dc5e2a4f32/lib/libsodium/src/libsodium/crypto_scalarmult/crypto_scalarmult.c#L11) · line 11 · SHA-256 590a3b390a9b88adc1097caf758a9fb4db7943d6aad90aa926c13e3b4fc3517b_

```
   10 | int
   11 | crypto_scalarmult_base(unsigned char *q, const unsigned char *n)
   12 | {
```

_file_excerpt · [lib/libsodium/src/libsodium/crypto_scalarmult/crypto_scalarmult.c](https://github.com/stellar/stellar-core/blob/362dbc5184c5fdc0d6e898f3046639dc5e2a4f32/lib/libsodium/src/libsodium/crypto_scalarmult/crypto_scalarmult.c#L17) · line 17 · SHA-256 f6246df4fcb69f3a7aa66b422cfd40eb0895a3f3e743fd5effbb0a50ab21c7d0_

```
   16 | int
   17 | crypto_scalarmult(unsigned char *q, const unsigned char *n,
   18 |                   const unsigned char *p)
```

_file_excerpt · [lib/libsodium/src/libsodium/include/sodium.h](https://github.com/stellar/stellar-core/blob/362dbc5184c5fdc0d6e898f3046639dc5e2a4f32/lib/libsodium/src/libsodium/include/sodium.h#L34) · line 34 · SHA-256 1309d78496f4478e5aad9c0b0a2ff383888c6e5db2568d5c032018177c4220d9_

```
   33 | #include "sodium/crypto_pwhash_argon2i.h"
   34 | #include "sodium/crypto_scalarmult.h"
   35 | #include "sodium/crypto_scalarmult_curve25519.h"
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Classify each usage, record data lifetimes, and plan migration to Hybrid key establishment with ML-KEM (FIPS 203), e.g. X25519MLKEM768 in TLS 1.3 or mlkem768x25519-sha256 in SSH; introduce an abstraction layer for crypto-agility.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-19578 — Quantum-vulnerable Ed25519: role not determined (44 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:Ed25519:general`
- Data source: src/crypto/SecretKey.cpp
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.3.0 · 2026-11-06 16:13 UTC
- Priority score: 34.2 / 100
- CVSS v3.1: not applicable

156 reference(s) to Ed25519 across 44 file(s), e.g. src/crypto/SecretKey.cpp:117. Role, judged from paths, function names and nearby code: role not determined. The code does not show what the keys protect; review decides the priority.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open src/crypto/SecretKey.cpp:117 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [src/crypto/SecretKey.cpp](https://github.com/stellar/stellar-core/blob/362dbc5184c5fdc0d6e898f3046639dc5e2a4f32/src/crypto/SecretKey.cpp#L117) · line 117 · SHA-256 e13bbd853301b4e8f05b04723422bb04b139021473c5abff85c02dd331160815_

```
  116 |     seed.mKeyType = mKeyType;
  117 |     if (crypto_sign_ed25519_sk_to_seed(seed.mSeed.data(), mSecretKey.data()) !=
  118 |         0)
```

_file_excerpt · [src/crypto/SecretKey.cpp](https://github.com/stellar/stellar-core/blob/362dbc5184c5fdc0d6e898f3046639dc5e2a4f32/src/crypto/SecretKey.cpp#L159) · line 159 · SHA-256 b7c51af7ae2a9d516f561181fbd345d921e921d6d789408b85e272890edfe782_

```
  158 |     Signature out(crypto_sign_BYTES, 0);
  159 |     if (crypto_sign_detached(out.data(), NULL, bin.data(), bin.size(),
  160 |                              mSecretKey.data()) != 0)
```

_file_excerpt · [src/crypto/SecretKey.cpp](https://github.com/stellar/stellar-core/blob/362dbc5184c5fdc0d6e898f3046639dc5e2a4f32/src/crypto/SecretKey.cpp#L172) · line 172 · SHA-256 a5dc903188262aee9e5a2b0028077aec6b31276f9d68b683c7caeba04aa3c198_

```
  171 |     releaseAssert(sk.mKeyType == PUBLIC_KEY_TYPE_ED25519);
  172 |     if (crypto_sign_keypair(sk.mPublicKey.ed25519().data(),
  173 |                             sk.mSecretKey.data()) != 0)
```

_file_excerpt · [src/rust/src/bridge.rs](https://github.com/stellar/stellar-core/blob/362dbc5184c5fdc0d6e898f3046639dc5e2a4f32/src/rust/src/bridge.rs#L489) · line 489 · SHA-256 8f9ff5da6990be3688021ebc64632fbe3359e1e1144d2cb44fbe55689e41039f_

```
  488 | use crate::common::*;
  489 | use crate::ed25519_verify::*;
  490 | use crate::i128::*;
```

_file_excerpt · [src/rust/src/ed25519_verify.rs](https://github.com/stellar/stellar-core/blob/362dbc5184c5fdc0d6e898f3046639dc5e2a4f32/src/rust/src/ed25519_verify.rs#L5) · line 5 · SHA-256 1fcf1bfb83dd6c884748ef4836ee51e391b3ba7a417080d9ecde9781ae918614_

```
    4 | 
    5 | use ed25519_dalek::{Signature, VerifyingKey};
    6 | 
```

_file_excerpt · [src/rust/src/lib.rs](https://github.com/stellar/stellar-core/blob/362dbc5184c5fdc0d6e898f3046639dc5e2a4f32/src/rust/src/lib.rs#L32) · line 32 · SHA-256 e3686d827f58853c6a1f5eb7226c4285365c3a30ef1bf106b97224b7a166ad83_

```
   31 | mod b64;
   32 | mod ed25519_verify;
   33 | mod i128;
```

_file_excerpt · [lib/libsodium/src/libsodium/crypto_sign/crypto_sign.c](https://github.com/stellar/stellar-core/blob/362dbc5184c5fdc0d6e898f3046639dc5e2a4f32/lib/libsodium/src/libsodium/crypto_sign/crypto_sign.c#L47) · line 47 · SHA-256 9d5861bf117296091f651c6f5643112bd515d9687c90668e9f2bf828e4abd7d5_

```
   46 | int
   47 | crypto_sign_seed_keypair(unsigned char *pk, unsigned char *sk,
   48 |                          const unsigned char *seed)
```

_file_excerpt · [lib/libsodium/src/libsodium/crypto_sign/crypto_sign.c](https://github.com/stellar/stellar-core/blob/362dbc5184c5fdc0d6e898f3046639dc5e2a4f32/lib/libsodium/src/libsodium/crypto_sign/crypto_sign.c#L50) · line 50 · SHA-256 4041dc6f1ceb6e8b6d2ddc79e99c7e31f216124bf2397907c8b36888bc0fab64_

```
   49 | {
   50 |     return crypto_sign_ed25519_seed_keypair(pk, sk, seed);
   51 | }
```

_file_excerpt · [lib/libsodium/src/libsodium/crypto_sign/crypto_sign.c](https://github.com/stellar/stellar-core/blob/362dbc5184c5fdc0d6e898f3046639dc5e2a4f32/lib/libsodium/src/libsodium/crypto_sign/crypto_sign.c#L54) · line 54 · SHA-256 dc9bd25d6b018b7e868cf7af048f84f12bb8d71dd935bd5d963ab85d31ef69c9_

```
   53 | int
   54 | crypto_sign_keypair(unsigned char *pk, unsigned char *sk)
   55 | {
```

_file_excerpt · [lib/libsodium/src/libsodium/crypto_sign/ed25519/ref10/keypair.c](https://github.com/stellar/stellar-core/blob/362dbc5184c5fdc0d6e898f3046639dc5e2a4f32/lib/libsodium/src/libsodium/crypto_sign/ed25519/ref10/keypair.c#L6) · line 6 · SHA-256 a4144bdaa7041f7523dad3757cbc0402fd117682f45cd59969c3268fd593a0cd_

```
    5 | #include "crypto_scalarmult_curve25519.h"
    6 | #include "crypto_sign_ed25519.h"
    7 | #include "sign_ed25519_ref10.h"
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it; introduce an abstraction layer for crypto-agility.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-19584 — Quantum-vulnerable ECDSA: role not determined (24 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:ECDSA:general`
- Data source: src/rust/soroban/p21/soroban-env-host/src/cost_runner/cost_types/sec1_decode_point_uncompressed.rs
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.3.0 · 2026-11-06 16:13 UTC
- Priority score: 34.2 / 100
- CVSS v3.1: not applicable

92 reference(s) to ECDSA across 24 file(s), e.g. src/rust/soroban/p21/soroban-env-host/src/cost_runner/cost_types/sec1_decode_point_uncompressed.rs:5. Role, judged from paths, function names and nearby code: role not determined. The code does not show what the keys protect; review decides the priority.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open src/rust/soroban/p21/soroban-env-host/src/cost_runner/cost_types/sec1_decode_point_uncompressed.rs:5 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [src/rust/soroban/p21/soroban-env-host/src/cost_runner/cost_types/sec1_decode_point_uncompressed.rs](https://github.com/stellar/stellar-core/blob/362dbc5184c5fdc0d6e898f3046639dc5e2a4f32/src/rust/soroban/p21/soroban-env-host/src/cost_runner/cost_types/sec1_decode_point_uncompressed.rs#L5) · line 5 · SHA-256 7d2cb0b1b110ea53e52a6a1c0f0e5651f2b202b8ee2d8a87a785a863cef85eac_

```
    4 | };
    5 | use p256::ecdsa::VerifyingKey;
    6 | use std::hint::black_box;
```

_file_excerpt · [src/rust/soroban/p21/soroban-env-host/src/cost_runner/cost_types/verify_ecdsa_secp256r1_sig.rs](https://github.com/stellar/stellar-core/blob/362dbc5184c5fdc0d6e898f3046639dc5e2a4f32/src/rust/soroban/p21/soroban-env-host/src/cost_runner/cost_types/verify_ecdsa_secp256r1_sig.rs#L5) · line 5 · SHA-256 f2d53d01d18c1fcc2292c319846326c466197df63a11674ca35578b3d82a2a58_

```
    4 | };
    5 | use p256::ecdsa::{Signature, VerifyingKey};
    6 | use std::hint::black_box;
```

_file_excerpt · [src/rust/soroban/p21/soroban-env-host/src/cost_runner/experimental/ecdsa_secp256r1_recover.rs](https://github.com/stellar/stellar-core/blob/362dbc5184c5fdc0d6e898f3046639dc5e2a4f32/src/rust/soroban/p21/soroban-env-host/src/cost_runner/experimental/ecdsa_secp256r1_recover.rs#L7) · line 7 · SHA-256 f935f9980262fe702e4e637a6cf0d94ad4f11c566858c98586bc13d04001bcb0_

```
    6 | use ecdsa::RecoveryId;
    7 | use p256::ecdsa::Signature;
    8 | use std::hint::black_box;
```

_file_excerpt · [src/rust/soroban/p21/soroban-env-host/src/cost_runner/experimental/sec1_decode_point_compressed.rs](https://github.com/stellar/stellar-core/blob/362dbc5184c5fdc0d6e898f3046639dc5e2a4f32/src/rust/soroban/p21/soroban-env-host/src/cost_runner/experimental/sec1_decode_point_compressed.rs#L5) · line 5 · SHA-256 198adb0a3b79fd9b102dd1d8010f7ec744f8079e2a92651a7102cc7ae2294827_

```
    4 | };
    5 | use p256::ecdsa::VerifyingKey;
    6 | 
```

_file_excerpt · [src/rust/soroban/p21/soroban-env-host/src/cost_runner/util.rs](https://github.com/stellar/stellar-core/blob/362dbc5184c5fdc0d6e898f3046639dc5e2a4f32/src/rust/soroban/p21/soroban-env-host/src/cost_runner/util.rs#L12) · line 12 · SHA-256 ae5512776b1eff8b7ccfcfb61c0d70042d1f24134c5c6eda6ece2ae4ae526f1e_

```
   11 |         &self,
   12 |         verifying_key: &k256::ecdsa::VerifyingKey,
   13 |         msg_hash: &Hash,
```

_file_excerpt · [src/rust/soroban/p21/soroban-env-host/src/cost_runner/util.rs](https://github.com/stellar/stellar-core/blob/362dbc5184c5fdc0d6e898f3046639dc5e2a4f32/src/rust/soroban/p21/soroban-env-host/src/cost_runner/util.rs#L22) · line 22 · SHA-256 993641d576de59cd5cd5c46079bf94b0b97dd9b3daf2fa32acbb1a0ac59b3d3e_

```
   21 |                     ScErrorCode::InvalidInput,
   22 |                     "failed secp256r1 verification",
   23 |                     &[],
```

_file_excerpt · [src/rust/soroban/p21/soroban-env-host/src/cost_runner/util.rs](https://github.com/stellar/stellar-core/blob/362dbc5184c5fdc0d6e898f3046639dc5e2a4f32/src/rust/soroban/p21/soroban-env-host/src/cost_runner/util.rs#L35) · line 35 · SHA-256 50fcd60c33b696e792d7360322abca7b4a8d38f256054a0598d0e767569d7ccc_

```
   34 |         let recovered_key =
   35 |             p256::ecdsa::VerifyingKey::recover_from_prehash(msg_hash.as_slice(), &sig, rid)
   36 |                 .map_err(|_| {
```

_file_excerpt · [src/rust/soroban/p21/soroban-env-host/src/host/crypto.rs](https://github.com/stellar/stellar-core/blob/362dbc5184c5fdc0d6e898f3046639dc5e2a4f32/src/rust/soroban/p21/soroban-env-host/src/host/crypto.rs#L86) · line 86 · SHA-256 3dcc374d93ecf28ae4784c8385574da8fed9f0cada9ff3a5ec5b0bc637f24140_

```
   85 |         &self,
   86 |         verifying_key: &p256::ecdsa::VerifyingKey,
   87 |         msg_hash: &Hash,
```

_file_excerpt · [src/rust/soroban/p21/soroban-env-host/src/host/crypto.rs](https://github.com/stellar/stellar-core/blob/362dbc5184c5fdc0d6e898f3046639dc5e2a4f32/src/rust/soroban/p21/soroban-env-host/src/host/crypto.rs#L98) · line 98 · SHA-256 c1030f488369025e80792e36f00d4bf6bc81ef7d7d449caa0d556e5b0d16e3fd_

```
   97 |                     ScErrorCode::InvalidInput,
   98 |                     "failed secp256r1 verification",
   99 |                     &[],
```

_file_excerpt · [src/rust/soroban/p21/soroban-env-host/src/host/crypto.rs](https://github.com/stellar/stellar-core/blob/362dbc5184c5fdc0d6e898f3046639dc5e2a4f32/src/rust/soroban/p21/soroban-env-host/src/host/crypto.rs#L107) · line 107 · SHA-256 b7330de3888b47e40d0fd56c4b0322744d86f96059b92e6965c293155602ccb3_

```
  106 |         bytes: &[u8],
  107 |     ) -> Result<p256::ecdsa::VerifyingKey, HostError> {
  108 |         use sec1::point::Tag;
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it; introduce an abstraction layer for crypto-agility.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-19585 — Quantum-vulnerable Ed25519: authentication and identity (certificates, tokens, device attestation) (3 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:Ed25519:authentication`
- Data source: src/rust/soroban/p21/soroban-test-wasms/wasm-workspace/simple_account/src/lib.rs
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.3.0 · 2026-11-06 16:13 UTC
- Priority score: 34.2 / 100
- CVSS v3.1: not applicable

3 reference(s) to Ed25519 across 3 file(s), e.g. src/rust/soroban/p21/soroban-test-wasms/wasm-workspace/simple_account/src/lib.rs:33. Role, judged from paths, function names and nearby code: authentication and identity (certificates, tokens, device attestation). Short-lived authentication stays safe until a CRQC exists; long-lived identities (device attestation, CA and SSH keys) need a plan earlier.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open src/rust/soroban/p21/soroban-test-wasms/wasm-workspace/simple_account/src/lib.rs:33 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [src/rust/soroban/p21/soroban-test-wasms/wasm-workspace/simple_account/src/lib.rs](https://github.com/stellar/stellar-core/blob/362dbc5184c5fdc0d6e898f3046639dc5e2a4f32/src/rust/soroban/p21/soroban-test-wasms/wasm-workspace/simple_account/src/lib.rs#L33) · line 33 · SHA-256 304dbfe7372763418ad046fb11f27c77b2f1ff85af31a304470b3ab55e541259_

```
   32 |         env.crypto()
   33 |             .ed25519_verify(&public_key, &signature_payload.into(), &signature);
   34 |     }
```

_file_excerpt · [src/rust/soroban/p22/soroban-test-wasms/wasm-workspace/simple_account/src/lib.rs](https://github.com/stellar/stellar-core/blob/362dbc5184c5fdc0d6e898f3046639dc5e2a4f32/src/rust/soroban/p22/soroban-test-wasms/wasm-workspace/simple_account/src/lib.rs#L33) · line 33 · SHA-256 304dbfe7372763418ad046fb11f27c77b2f1ff85af31a304470b3ab55e541259_

```
   32 |         env.crypto()
   33 |             .ed25519_verify(&public_key, &signature_payload.into(), &signature);
   34 |     }
```

_file_excerpt · [src/rust/soroban/p23/soroban-test-wasms/wasm-workspace/simple_account/src/lib.rs](https://github.com/stellar/stellar-core/blob/362dbc5184c5fdc0d6e898f3046639dc5e2a4f32/src/rust/soroban/p23/soroban-test-wasms/wasm-workspace/simple_account/src/lib.rs#L33) · line 33 · SHA-256 304dbfe7372763418ad046fb11f27c77b2f1ff85af31a304470b3ab55e541259_

```
   32 |         env.crypto()
   33 |             .ed25519_verify(&public_key, &signature_payload.into(), &signature);
   34 |     }
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Keep credentials short-lived and plan ML-DSA certificates, tokens and keys as the ecosystem supports them.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-19586 — Quantum-vulnerable BLS12-381: role not determined (12 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:BLS12-381:general`
- Data source: src/rust/soroban/p22/soroban-env-host/src/cost_runner/cost_types/bls12_381.rs
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.3.0 · 2026-11-06 16:13 UTC
- Priority score: 34.2 / 100
- CVSS v3.1: not applicable

18 reference(s) to BLS12-381 across 12 file(s), e.g. src/rust/soroban/p22/soroban-env-host/src/cost_runner/cost_types/bls12_381.rs:6. Role, judged from paths, function names and nearby code: role not determined. The code does not show what the keys protect; review decides the priority.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open src/rust/soroban/p22/soroban-env-host/src/cost_runner/cost_types/bls12_381.rs:6 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [src/rust/soroban/p22/soroban-env-host/src/cost_runner/cost_types/bls12_381.rs](https://github.com/stellar/stellar-core/blob/362dbc5184c5fdc0d6e898f3046639dc5e2a4f32/src/rust/soroban/p22/soroban-env-host/src/cost_runner/cost_types/bls12_381.rs#L6) · line 6 · SHA-256 cbe62e9967b82476495c9289979771bf8833f7794b9da7dff040caf4695bf1f8_

```
    5 |     cost_runner::{CostRunner, CostType},
    6 |     crypto::bls12_381::FP_SERIALIZED_SIZE,
    7 |     impl_const_cost_runner_for_bls_consume_sample, impl_const_cost_runner_for_bls_deref_sample,
```

_file_excerpt · [src/rust/soroban/p22/soroban-env-host/src/cost_runner/cost_types/mod.rs](https://github.com/stellar/stellar-core/blob/362dbc5184c5fdc0d6e898f3046639dc5e2a4f32/src/rust/soroban/p22/soroban-env-host/src/cost_runner/cost_types/mod.rs#L1) · line 1 · SHA-256 efbd8cc16388e85c4398fca007e662d5a95ad2f4b6ccbeab99e246366a6a2d54_

```
    1 | mod bls12_381;
    2 | mod compute_ed25519_pubkey;
```

_file_excerpt · [src/rust/soroban/p22/soroban-env-host/src/cost_runner/cost_types/mod.rs](https://github.com/stellar/stellar-core/blob/362dbc5184c5fdc0d6e898f3046639dc5e2a4f32/src/rust/soroban/p22/soroban-env-host/src/cost_runner/cost_types/mod.rs#L22) · line 22 · SHA-256 5b8e0290b587c95f0e51fb26254a581f2cdd8890650bf4a8e5a2e70cf5f82547_

```
   21 | 
   22 | pub use bls12_381::*;
   23 | pub use compute_ed25519_pubkey::*;
```

_file_excerpt · [src/rust/soroban/p22/soroban-env-host/src/cost_runner/experimental/mod.rs](https://github.com/stellar/stellar-core/blob/362dbc5184c5fdc0d6e898f3046639dc5e2a4f32/src/rust/soroban/p22/soroban-env-host/src/cost_runner/experimental/mod.rs#L1) · line 1 · SHA-256 61704a40c8060cf429540fade251e2c1e888ad9950384d99454d1671677606d7_

```
    1 | mod bls12_381;
    2 | mod decode_secp256r1_sig;
```

_file_excerpt · [src/rust/soroban/p22/soroban-env-host/src/cost_runner/experimental/mod.rs](https://github.com/stellar/stellar-core/blob/362dbc5184c5fdc0d6e898f3046639dc5e2a4f32/src/rust/soroban/p22/soroban-env-host/src/cost_runner/experimental/mod.rs#L9) · line 9 · SHA-256 38ff3b522b1267ca4d3296c833e5512d6bc78f147cee0494ec3d69896b690949_

```
    8 | 
    9 | pub use bls12_381::*;
   10 | pub use decode_secp256r1_sig::*;
```

_file_excerpt · [src/rust/soroban/p22/soroban-env-host/src/crypto/mod.rs](https://github.com/stellar/stellar-core/blob/362dbc5184c5fdc0d6e898f3046639dc5e2a4f32/src/rust/soroban/p22/soroban-env-host/src/crypto/mod.rs#L20) · line 20 · SHA-256 cb3233be2ba455f96d95e9eb30bedc835251c0ae5a3be3312a24a81176a30702_

```
   19 | use generic_array::ArrayLength;
   20 | pub(crate) mod bls12_381;
   21 | 
```

_file_excerpt · [src/rust/soroban/p23/soroban-env-host/src/cost_runner/cost_types/bls12_381.rs](https://github.com/stellar/stellar-core/blob/362dbc5184c5fdc0d6e898f3046639dc5e2a4f32/src/rust/soroban/p23/soroban-env-host/src/cost_runner/cost_types/bls12_381.rs#L6) · line 6 · SHA-256 cbe62e9967b82476495c9289979771bf8833f7794b9da7dff040caf4695bf1f8_

```
    5 |     cost_runner::{CostRunner, CostType},
    6 |     crypto::bls12_381::FP_SERIALIZED_SIZE,
    7 |     impl_const_cost_runner_for_bls_consume_sample, impl_const_cost_runner_for_bls_deref_sample,
```

_file_excerpt · [src/rust/soroban/p23/soroban-env-host/src/cost_runner/cost_types/mod.rs](https://github.com/stellar/stellar-core/blob/362dbc5184c5fdc0d6e898f3046639dc5e2a4f32/src/rust/soroban/p23/soroban-env-host/src/cost_runner/cost_types/mod.rs#L1) · line 1 · SHA-256 efbd8cc16388e85c4398fca007e662d5a95ad2f4b6ccbeab99e246366a6a2d54_

```
    1 | mod bls12_381;
    2 | mod compute_ed25519_pubkey;
```

_file_excerpt · [src/rust/soroban/p23/soroban-env-host/src/cost_runner/cost_types/mod.rs](https://github.com/stellar/stellar-core/blob/362dbc5184c5fdc0d6e898f3046639dc5e2a4f32/src/rust/soroban/p23/soroban-env-host/src/cost_runner/cost_types/mod.rs#L22) · line 22 · SHA-256 5b8e0290b587c95f0e51fb26254a581f2cdd8890650bf4a8e5a2e70cf5f82547_

```
   21 | 
   22 | pub use bls12_381::*;
   23 | pub use compute_ed25519_pubkey::*;
```

_file_excerpt · [src/rust/soroban/p23/soroban-env-host/src/cost_runner/experimental/mod.rs](https://github.com/stellar/stellar-core/blob/362dbc5184c5fdc0d6e898f3046639dc5e2a4f32/src/rust/soroban/p23/soroban-env-host/src/cost_runner/experimental/mod.rs#L1) · line 1 · SHA-256 61704a40c8060cf429540fade251e2c1e888ad9950384d99454d1671677606d7_

```
    1 | mod bls12_381;
    2 | mod decode_secp256r1_sig;
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Classify each usage, record data lifetimes, and plan migration to a post-quantum algorithm; introduce an abstraction layer for crypto-agility.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-19580 — MD5 used in lib/gperftools/src/gen_getpc.rb

- Severity: **Medium** · Classification: Potential cryptographic risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `file:lib/gperftools/src/gen_getpc.rb`
- Data source: lib/gperftools/src/gen_getpc.rb
- Detection method: Regular-expression matching of language-specific API patterns.
- Analyzer: source_code 1.3.0 · 2026-11-06 16:13 UTC
- Priority score: 33.7 / 100
- CVSS v3.1: not applicable

1 call site(s) of MD5 (first at line 145).

**Potential impact.** If used for signatures, password storage, integrity against attackers or token generation, collisions/preimages may be exploitable. Non-security checksums are acceptable.

**Reproduction steps.**

```
Open line 145 in the supplied file lib/gperftools/src/gen_getpc.rb and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [lib/gperftools/src/gen_getpc.rb](https://github.com/stellar/stellar-core/blob/362dbc5184c5fdc0d6e898f3046639dc5e2a4f32/lib/gperftools/src/gen_getpc.rb#L145) · line 145 · SHA-256 0bc25f1fd08fdeda5e3ae0ffa09c547f767c85f1ae56d27356e438d5a43d6e7b_

```
  143 |              end
  144 |            end
  145 |     fingerprint = Digest::MD5.hexdigest(tmpl["%"] + "@" + comment)[0,8]
  146 | 
  147 |     maybe_open_ifdef = "\n#ifdef #{define}" if define
```

**Limitations of the check.** Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Replace with SHA-256/SHA-3 (or Argon2/bcrypt for passwords) where security-relevant.

**Retest procedure.** Re-scan the source and review the call sites listed in the evidence.

### QSI-2026-19600 — serde_with 3.18.0 is affected by GHSA-7gcf-g7xr-8hxj

- Severity: **Medium** · Classification: Known vulnerable component · Confidence: Low
- Affected asset: `dependency:crates.io/serde_with@3.18.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 16:13 UTC
- Priority score: 33.1 / 100
- CVSS v3.1: not applicable

OSV.dev reports GHSA-7gcf-g7xr-8hxj for crates.io package serde_with at version 3.18.0: serde_with: KeyValueMap serialization panics on empty sequence or map entries. The advisory names no affected functions, so reachability was not determined.

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

### QSI-2026-19608 — serde_with 3.4.0 is affected by GHSA-7gcf-g7xr-8hxj

- Severity: **Medium** · Classification: Known vulnerable component · Confidence: Low
- Affected asset: `dependency:crates.io/serde_with@3.4.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 16:13 UTC
- Priority score: 33.1 / 100
- CVSS v3.1: not applicable

OSV.dev reports GHSA-7gcf-g7xr-8hxj for crates.io package serde_with at version 3.4.0: serde_with: KeyValueMap serialization panics on empty sequence or map entries. The advisory names no affected functions, so reachability was not determined.

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

### QSI-2026-19609 — time 0.3.30 is affected by GHSA-r6v5-fh4h-64xc (CVE-2026-25727, RUSTSEC-2026-0009)

- Severity: **Medium** · Classification: Known vulnerable component · Confidence: Low
- Affected asset: `dependency:crates.io/time@0.3.30`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 16:13 UTC
- Priority score: 33.1 / 100
- CVSS v3.1: not applicable

OSV.dev reports GHSA-r6v5-fh4h-64xc (CVE-2026-25727, RUSTSEC-2026-0009) for crates.io package time at version 0.3.30: time vulnerable to stack exhaustion Denial of Service attack. Some product source files did not fit the size limits, so the affected functions were not looked up.

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

### QSI-2026-19619 — serde_with 3.12.0 is affected by GHSA-7gcf-g7xr-8hxj

- Severity: **Medium** · Classification: Known vulnerable component · Confidence: Low
- Affected asset: `dependency:crates.io/serde_with@3.12.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 16:13 UTC
- Priority score: 33.1 / 100
- CVSS v3.1: not applicable

OSV.dev reports GHSA-7gcf-g7xr-8hxj for crates.io package serde_with at version 3.12.0: serde_with: KeyValueMap serialization panics on empty sequence or map entries. The advisory names no affected functions, so reachability was not determined.

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

### QSI-2026-19620 — time 0.3.41 is affected by GHSA-r6v5-fh4h-64xc (CVE-2026-25727, RUSTSEC-2026-0009)

- Severity: **Medium** · Classification: Known vulnerable component · Confidence: Low
- Affected asset: `dependency:crates.io/time@0.3.41`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 16:13 UTC
- Priority score: 33.1 / 100
- CVSS v3.1: not applicable

OSV.dev reports GHSA-r6v5-fh4h-64xc (CVE-2026-25727, RUSTSEC-2026-0009) for crates.io package time at version 0.3.41: time vulnerable to stack exhaustion Denial of Service attack. Some product source files did not fit the size limits, so the affected functions were not looked up.

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

### QSI-2026-19622 — serde_with 3.14.0 is affected by GHSA-7gcf-g7xr-8hxj

- Severity: **Medium** · Classification: Known vulnerable component · Confidence: Low
- Affected asset: `dependency:crates.io/serde_with@3.14.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 16:13 UTC
- Priority score: 33.1 / 100
- CVSS v3.1: not applicable

OSV.dev reports GHSA-7gcf-g7xr-8hxj for crates.io package serde_with at version 3.14.0: serde_with: KeyValueMap serialization panics on empty sequence or map entries. The advisory names no affected functions, so reachability was not determined.

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

### QSI-2026-19576 — Non-cryptographic RNG near security-sensitive identifiers in scripts/OverlaySurvey.py

- Severity: **Medium** · Classification: Potential cryptographic risk · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `file:scripts/OverlaySurvey.py`
- Data source: scripts/OverlaySurvey.py
- Detection method: Regular-expression matching of language-specific API patterns.
- Analyzer: source_code 1.3.0 · 2026-11-06 16:13 UTC
- Priority score: 25.2 / 100
- CVSS v3.1: not applicable

'random.randint(' at line 348 on a line mentioning key/token/secret/password/nonce.

**Potential impact.** Predictable values may allow token or key guessing.

**Reproduction steps.**

```
Open line 348 in the supplied file scripts/OverlaySurvey.py and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [scripts/OverlaySurvey.py](https://github.com/stellar/stellar-core/blob/362dbc5184c5fdc0d6e898f3046639dc5e2a4f32/scripts/OverlaySurvey.py#L348) · line 348 · SHA-256 3e74215df99b1ee045c813964a29139344d54a29f368f98bae9d143d1de3ce51_

```
  346 |     start_collecting = url + "/startsurveycollecting"
  347 |     info = url + "/info"
  348 |     nonce = random.randint(0, 2**32-1)
  349 |     logger.info("Starting survey with nonce %s", nonce)
  350 |     response = get_request(url=start_collecting, params={'nonce': nonce})
```

**Limitations of the check.** Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Use a CSPRNG (secrets, crypto.getRandomValues, crypto/rand).

**Retest procedure.** Re-scan the source and review the call sites listed in the evidence.

### QSI-2026-19594 — rand 0.8.5 is affected by GHSA-cq8v-f236-94qc (RUSTSEC-2026-0097)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Medium
- Affected asset: `dependency:crates.io/rand@0.8.5`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 16:13 UTC
- Priority score: 39.2 / 100
- CVSS v3.1: not applicable

OSV.dev reports GHSA-cq8v-f236-94qc (RUSTSEC-2026-0097) for crates.io package rand at version 0.8.5: Rand is unsound with a custom logger using rand::rng(). Some product source files did not fit the size limits, so the affected functions were not looked up.

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

### QSI-2026-19601 — soroban-env-host 23.0.1 is affected by GHSA-pm4j-7r4q-ccg8

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Medium
- Affected asset: `dependency:crates.io/soroban-env-host@23.0.1`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 16:13 UTC
- Priority score: 39.2 / 100
- CVSS v3.1: not applicable

OSV.dev reports GHSA-pm4j-7r4q-ccg8 for crates.io package soroban-env-host at version 23.0.1: Soroban: Muxed address<->ScVal conversions may break after a conversion failure. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-pm4j-7r4q-ccg8
```

**Evidence.**

_tool_output · [OSV.dev GHSA-pm4j-7r4q-ccg8](https://osv.dev/vulnerability/GHSA-pm4j-7r4q-ccg8) · manifest · SHA-256 8ec7c5fed3ab66bac5c327dac5ca89326bf6696bcb1164bfd1f8cbbba8eff743_

```
{"id": "GHSA-pm4j-7r4q-ccg8", "aliases": [], "modified": "2026-03-07T02:47:39.508852Z", "summary": "Soroban: Muxed address<->ScVal conversions may break after a conversion failure", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N/E:U"}], "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (26.0.0).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-19605 — curve25519-dalek 4.1.1 is affected by GHSA-x4gp-pqpj-f43q (CVE-2024-58262, RUSTSEC-2024-0344)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Medium
- Affected asset: `dependency:crates.io/curve25519-dalek@4.1.1`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 16:13 UTC
- Priority score: 39.2 / 100
- CVSS v3.1: 2.9 (`CVSS:3.1/AV:L/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N`)

OSV.dev reports GHSA-x4gp-pqpj-f43q (CVE-2024-58262, RUSTSEC-2024-0344) for crates.io package curve25519-dalek at version 4.1.1: curve25519-dalek has timing variability in `curve25519-dalek`'s `Scalar29::sub`/`Scalar52::sub`. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-x4gp-pqpj-f43q
```

**Evidence.**

_tool_output · [OSV.dev GHSA-x4gp-pqpj-f43q](https://osv.dev/vulnerability/GHSA-x4gp-pqpj-f43q) · manifest · SHA-256 9c5ba7e4d1d09d2c4281ad759683fef0dfc421b4b4415921e436a1ddb8987906_

```
{"id": "GHSA-x4gp-pqpj-f43q", "aliases": ["CVE-2024-58262", "RUSTSEC-2024-0344"], "modified": "2026-09-10T03:50:15.886084155Z", "summary": "curve25519-dalek has timing variability in `curve25519-dalek`'s `Scalar29::sub`/`Scalar52::sub`", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:L/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N"}], "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (4.1.3).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-19611 — soroban-env-host 21.2.2 is affected by GHSA-pm4j-7r4q-ccg8

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Medium
- Affected asset: `dependency:crates.io/soroban-env-host@21.2.2`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 16:13 UTC
- Priority score: 39.2 / 100
- CVSS v3.1: not applicable

OSV.dev reports GHSA-pm4j-7r4q-ccg8 for crates.io package soroban-env-host at version 21.2.2: Soroban: Muxed address<->ScVal conversions may break after a conversion failure. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-pm4j-7r4q-ccg8
```

**Evidence.**

_tool_output · [OSV.dev GHSA-pm4j-7r4q-ccg8](https://osv.dev/vulnerability/GHSA-pm4j-7r4q-ccg8) · manifest · SHA-256 8ec7c5fed3ab66bac5c327dac5ca89326bf6696bcb1164bfd1f8cbbba8eff743_

```
{"id": "GHSA-pm4j-7r4q-ccg8", "aliases": [], "modified": "2026-03-07T02:47:39.508852Z", "summary": "Soroban: Muxed address<->ScVal conversions may break after a conversion failure", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N/E:U"}], "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (26.0.0).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-19614 — soroban-env-host 20.3.0 is affected by GHSA-pm4j-7r4q-ccg8

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Medium
- Affected asset: `dependency:crates.io/soroban-env-host@20.3.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 16:13 UTC
- Priority score: 39.2 / 100
- CVSS v3.1: not applicable

OSV.dev reports GHSA-pm4j-7r4q-ccg8 for crates.io package soroban-env-host at version 20.3.0: Soroban: Muxed address<->ScVal conversions may break after a conversion failure. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-pm4j-7r4q-ccg8
```

**Evidence.**

_tool_output · [OSV.dev GHSA-pm4j-7r4q-ccg8](https://osv.dev/vulnerability/GHSA-pm4j-7r4q-ccg8) · manifest · SHA-256 8ec7c5fed3ab66bac5c327dac5ca89326bf6696bcb1164bfd1f8cbbba8eff743_

```
{"id": "GHSA-pm4j-7r4q-ccg8", "aliases": [], "modified": "2026-03-07T02:47:39.508852Z", "summary": "Soroban: Muxed address<->ScVal conversions may break after a conversion failure", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N/E:U"}], "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (26.0.0).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-19616 — soroban-env-host 22.0.0 is affected by GHSA-pm4j-7r4q-ccg8

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Medium
- Affected asset: `dependency:crates.io/soroban-env-host@22.0.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 16:13 UTC
- Priority score: 39.2 / 100
- CVSS v3.1: not applicable

OSV.dev reports GHSA-pm4j-7r4q-ccg8 for crates.io package soroban-env-host at version 22.0.0: Soroban: Muxed address<->ScVal conversions may break after a conversion failure. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-pm4j-7r4q-ccg8
```

**Evidence.**

_tool_output · [OSV.dev GHSA-pm4j-7r4q-ccg8](https://osv.dev/vulnerability/GHSA-pm4j-7r4q-ccg8) · manifest · SHA-256 8ec7c5fed3ab66bac5c327dac5ca89326bf6696bcb1164bfd1f8cbbba8eff743_

```
{"id": "GHSA-pm4j-7r4q-ccg8", "aliases": [], "modified": "2026-03-07T02:47:39.508852Z", "summary": "Soroban: Muxed address<->ScVal conversions may break after a conversion failure", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N/E:U"}], "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (26.0.0).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-19621 — soroban-env-host 23.0.0 is affected by GHSA-pm4j-7r4q-ccg8

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Medium
- Affected asset: `dependency:crates.io/soroban-env-host@23.0.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 16:13 UTC
- Priority score: 39.2 / 100
- CVSS v3.1: not applicable

OSV.dev reports GHSA-pm4j-7r4q-ccg8 for crates.io package soroban-env-host at version 23.0.0: Soroban: Muxed address<->ScVal conversions may break after a conversion failure. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-pm4j-7r4q-ccg8
```

**Evidence.**

_tool_output · [OSV.dev GHSA-pm4j-7r4q-ccg8](https://osv.dev/vulnerability/GHSA-pm4j-7r4q-ccg8) · manifest · SHA-256 8ec7c5fed3ab66bac5c327dac5ca89326bf6696bcb1164bfd1f8cbbba8eff743_

```
{"id": "GHSA-pm4j-7r4q-ccg8", "aliases": [], "modified": "2026-03-07T02:47:39.508852Z", "summary": "Soroban: Muxed address<->ScVal conversions may break after a conversion failure", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N/E:U"}], "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (26.0.0).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-19624 — soroban-env-host 24.0.0 is affected by GHSA-pm4j-7r4q-ccg8

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Medium
- Affected asset: `dependency:crates.io/soroban-env-host@24.0.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 16:13 UTC
- Priority score: 39.2 / 100
- CVSS v3.1: not applicable

OSV.dev reports GHSA-pm4j-7r4q-ccg8 for crates.io package soroban-env-host at version 24.0.0: Soroban: Muxed address<->ScVal conversions may break after a conversion failure. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-pm4j-7r4q-ccg8
```

**Evidence.**

_tool_output · [OSV.dev GHSA-pm4j-7r4q-ccg8](https://osv.dev/vulnerability/GHSA-pm4j-7r4q-ccg8) · manifest · SHA-256 8ec7c5fed3ab66bac5c327dac5ca89326bf6696bcb1164bfd1f8cbbba8eff743_

```
{"id": "GHSA-pm4j-7r4q-ccg8", "aliases": [], "modified": "2026-03-07T02:47:39.508852Z", "summary": "Soroban: Muxed address<->ScVal conversions may break after a conversion failure", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N/E:U"}], "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (26.0.0).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-19599 — tracing-subscriber 0.3.17 is affected by GHSA-xwfj-jgwm-7wp5 (CVE-2025-58160, RUSTSEC-2025-0055)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low
- Affected asset: `dependency:crates.io/tracing-subscriber@0.3.17`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 16:13 UTC
- Priority score: 29.4 / 100
- CVSS v3.1: not applicable

OSV.dev reports GHSA-xwfj-jgwm-7wp5 (CVE-2025-58160, RUSTSEC-2025-0055) for crates.io package tracing-subscriber at version 0.3.17: Tracing logging user input may result in poisoning logs with ANSI escape sequences. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-xwfj-jgwm-7wp5
```

**Evidence.**

_tool_output · [OSV.dev GHSA-xwfj-jgwm-7wp5](https://osv.dev/vulnerability/GHSA-xwfj-jgwm-7wp5) · manifest · SHA-256 c5ea2040929b0bf0d590c444d6ef1ef2de439865d4d25d158415ac6297ef25c5_

```
{"id": "GHSA-xwfj-jgwm-7wp5", "aliases": ["CVE-2025-58160", "RUSTSEC-2025-0055"], "modified": "2026-09-10T03:50:27.766863705Z", "summary": " Tracing logging user input may result in poisoning logs with ANSI escape sequences", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (0.3.20).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-19610 — tracing-subscriber 0.3.18 is affected by GHSA-xwfj-jgwm-7wp5 (CVE-2025-58160, RUSTSEC-2025-0055)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low
- Affected asset: `dependency:crates.io/tracing-subscriber@0.3.18`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 16:13 UTC
- Priority score: 29.4 / 100
- CVSS v3.1: not applicable

OSV.dev reports GHSA-xwfj-jgwm-7wp5 (CVE-2025-58160, RUSTSEC-2025-0055) for crates.io package tracing-subscriber at version 0.3.18: Tracing logging user input may result in poisoning logs with ANSI escape sequences. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-xwfj-jgwm-7wp5
```

**Evidence.**

_tool_output · [OSV.dev GHSA-xwfj-jgwm-7wp5](https://osv.dev/vulnerability/GHSA-xwfj-jgwm-7wp5) · manifest · SHA-256 c5ea2040929b0bf0d590c444d6ef1ef2de439865d4d25d158415ac6297ef25c5_

```
{"id": "GHSA-xwfj-jgwm-7wp5", "aliases": ["CVE-2025-58160", "RUSTSEC-2025-0055"], "modified": "2026-09-10T03:50:27.766863705Z", "summary": " Tracing logging user input may result in poisoning logs with ANSI escape sequences", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (0.3.20).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-19592 — keccak 0.1.5 is affected by GHSA-3288-p39f-rqpv (RUSTSEC-2026-0012)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/keccak@0.1.5`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 16:13 UTC
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

### QSI-2026-19606 — keccak 0.1.4 is affected by GHSA-3288-p39f-rqpv (RUSTSEC-2026-0012)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/keccak@0.1.4`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 16:13 UTC
- Priority score: 25.0 / 100
- CVSS v3.1: not applicable

OSV.dev reports GHSA-3288-p39f-rqpv (RUSTSEC-2026-0012) for crates.io package keccak at version 0.1.4: Unsoundness in opt-in ARMv8 assembly backend for `keccak`. The affected code sits behind the `asm` Cargo feature, off by default, which no audited manifest enables: the advisory does not apply unless another dependency enables it.

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

### QSI-2026-19588 — crypto-bigint 0.5.5 is affected by RUSTSEC-2026-0387 (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/crypto-bigint@0.5.5`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 16:13 UTC
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

### QSI-2026-19589 — ctutils 0.4.2 is affected by RUSTSEC-2026-0385 (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/ctutils@0.4.2`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 16:13 UTC
- Priority score: 20.3 / 100
- CVSS v3.1: not applicable

OSV.dev reports RUSTSEC-2026-0385 for crates.io package ctutils at version 0.4.2: Non-constant-time mask generation and `u128` comparisons. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. The advisory names no affected functions, so reachability was not determined.

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

### QSI-2026-19590 — cxx 1.0.97 is affected by RUSTSEC-2026-0202 (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/cxx@1.0.97`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 16:13 UTC
- Priority score: 20.3 / 100
- CVSS v3.1: not applicable

OSV.dev reports RUSTSEC-2026-0202 for crates.io package cxx at version 1.0.97: `let_cxx_string!` uses uninitialized value due to exception safety violations. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. Some product source files did not fit the size limits, so the affected functions were not looked up.

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0202
```

**Evidence.**

_tool_output · [OSV.dev RUSTSEC-2026-0202](https://osv.dev/vulnerability/RUSTSEC-2026-0202) · manifest · SHA-256 e0977e9b12342f37e94beadb2b3b5103766aed6eb80deac0abbafd36fe62eaf3_

```
{"id": "RUSTSEC-2026-0202", "aliases": [], "modified": "2026-07-05T08:45:04.168768726Z", "summary": "`let_cxx_string!` uses uninitialized value due to exception safety violations", "severity": null, "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Triage the advisory; upgrade to a fixed version (1.0.195) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-19603 — anyhow 1.0.75 is affected by RUSTSEC-2026-0190 (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/anyhow@1.0.75`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 16:13 UTC
- Priority score: 20.3 / 100
- CVSS v3.1: not applicable

OSV.dev reports RUSTSEC-2026-0190 for crates.io package anyhow at version 1.0.75: Unsoundness in `Error::downcast_mut()`. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. Some product source files did not fit the size limits, so the affected functions were not looked up.

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0190
```

**Evidence.**

_tool_output · [OSV.dev RUSTSEC-2026-0190](https://osv.dev/vulnerability/RUSTSEC-2026-0190) · manifest · SHA-256 9b326e11cad5998fcbb9f1ebd28aa1272c12693cad71de91698880f0657cc0b1_

```
{"id": "RUSTSEC-2026-0190", "aliases": [], "modified": "2026-06-29T14:15:03.650725453Z", "summary": "Unsoundness in `Error::downcast_mut()`", "severity": null, "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Triage the advisory; upgrade to a fixed version (1.0.103) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-19604 — crypto-bigint 0.5.2 is affected by RUSTSEC-2026-0387 (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/crypto-bigint@0.5.2`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 16:13 UTC
- Priority score: 20.3 / 100
- CVSS v3.1: not applicable

OSV.dev reports RUSTSEC-2026-0387 for crates.io package crypto-bigint at version 0.5.2: Multiple timing variability issues in operations intended to be constant-time. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. The advisory names no affected functions, so reachability was not determined.

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

### QSI-2026-19612 — crypto-bigint 0.5.4 is affected by RUSTSEC-2026-0387 (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/crypto-bigint@0.5.4`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 16:13 UTC
- Priority score: 20.3 / 100
- CVSS v3.1: not applicable

OSV.dev reports RUSTSEC-2026-0387 for crates.io package crypto-bigint at version 0.5.4: Multiple timing variability issues in operations intended to be constant-time. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. The advisory names no affected functions, so reachability was not determined.

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

### QSI-2026-19591 — derivative 2.2.0: informational advisory RUSTSEC-2024-0388 (unmaintained)

- Severity: **Info** · Classification: Improvement recommendation · Confidence: Low
- Affected asset: `dependency:crates.io/derivative@2.2.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 16:13 UTC
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

### QSI-2026-19593 — paste 1.0.15: informational advisory RUSTSEC-2024-0436 (unmaintained)

- Severity: **Info** · Classification: Improvement recommendation · Confidence: Low
- Affected asset: `dependency:crates.io/paste@1.0.15`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 16:13 UTC
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

### QSI-2026-19602 — adler 1.0.2: informational advisory RUSTSEC-2025-0056 (unmaintained)

- Severity: **Info** · Classification: Improvement recommendation · Confidence: Low
- Affected asset: `dependency:crates.io/adler@1.0.2`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 16:13 UTC
- Priority score: 11.8 / 100
- CVSS v3.1: not applicable

OSV.dev lists RUSTSEC-2025-0056 for crates.io package adler at version 1.0.2 as informational (unmaintained): adler crate is unmaintained, use adler2 instead. It reports no vulnerability; an unmaintained package will not receive fixes for future ones.

**Potential impact.** No known vulnerability. Future security fixes may not be released.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2025-0056
```

**Evidence.**

_tool_output · [OSV.dev RUSTSEC-2025-0056](https://osv.dev/vulnerability/RUSTSEC-2025-0056) · manifest · SHA-256 e9b7ae0431d69f626bc876560ccaff44bb57b35757fd9296256424ca73e69fd2_

```
{"id": "RUSTSEC-2025-0056", "aliases": [], "modified": "2025-09-05T09:05:48Z", "summary": "adler crate is unmaintained, use adler2 instead", "severity": null, "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time.

**Recommendation.** Plan a move to a maintained alternative, or record the decision to keep it.

**Retest procedure.** Re-run the dependency scan after the change.

### QSI-2026-19607 — paste 1.0.12: informational advisory RUSTSEC-2024-0436 (unmaintained)

- Severity: **Info** · Classification: Improvement recommendation · Confidence: Low
- Affected asset: `dependency:crates.io/paste@1.0.12`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 16:13 UTC
- Priority score: 11.8 / 100
- CVSS v3.1: not applicable

OSV.dev lists RUSTSEC-2024-0436 for crates.io package paste at version 1.0.12 as informational (unmaintained): paste - no longer maintained. It reports no vulnerability; an unmaintained package will not receive fixes for future ones.

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

### QSI-2026-19613 — paste 1.0.14: informational advisory RUSTSEC-2024-0436 (unmaintained)

- Severity: **Info** · Classification: Improvement recommendation · Confidence: Low
- Affected asset: `dependency:crates.io/paste@1.0.14`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 16:13 UTC
- Priority score: 11.8 / 100
- CVSS v3.1: not applicable

OSV.dev lists RUSTSEC-2024-0436 for crates.io package paste at version 1.0.14 as informational (unmaintained): paste - no longer maintained. It reports no vulnerability; an unmaintained package will not receive fixes for future ones.

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

### Post-quantum maturity: Level 1 of 4 — post-quantum code present, not wired

- A post-quantum library is declared as a dependency
- Classical only — key wrapping and data encryption at rest: X25519 (1 file(s))

**Next step:** Wire the existing post-quantum primitive into a critical path (key wrapping or the channel) behind a hybrid construction, and test interoperability.

_Levels: 0 none; 1 present, not wired; 2 in use outside the critical paths; 3 hybrid in a critical path; 4 post-quantum by default in the critical paths (root of trust, key wrapping, channel key exchange). Judged from code and manifests._

### What the quantum-vulnerable algorithms do

| Role | Algorithms (files) | ID | First step |
|---|---|---|---|
| **key wrapping and data encryption at rest** | X25519 (1) | QSI-2026-19581 | Wrap keys with ML-KEM or a hybrid KEM (X25519 + ML-KEM-768) and re-wrap the stored keys; data that may already have been copied needs its own assessment |
| **transaction and message signing** | Ed25519 (12), ECDSA (8) | QSI-2026-19579, QSI-2026-19583 | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains adopt them |
| **authentication and identity (certificates, tokens, device attestation)** | Ed25519 (3) | QSI-2026-19585 | Keep credentials short-lived and plan ML-DSA certificates, tokens and keys as the ecosystem supports them |
| **role not determined** | Ed25519 (44), ECDSA (24), BLS12-381 (12), X25519 (9) | QSI-2026-19577, QSI-2026-19578, QSI-2026-19584, QSI-2026-19586 | Classify each usage, record data lifetimes, and plan migration to Hybrid key establishment with ML-KEM (FIPS 203), e.g. X25519MLKEM768 in TLS 1.3 or mlkem768x25519-sha256 in SSH; introduce an abstraction layer for crypto-agility |

_Roles are judged from file paths, function names and the code around each match; review confirms them. Root-of-trust keys and wrapped keys come first: they are hard to replace or can be recorded today._
No readiness questionnaire was completed for this project.

### Quantum algorithms relevant to this inventory

| Quantum algorithm | Effect | Attack model | Inventoried algorithms (rows) | What it means for this audit |
|---|---|---|---|---|
| Shor's algorithm — discrete logarithms in finite fields | breaks | Q1 | BLS12-381 (18) | Breaks finite-field Diffie–Hellman and DSA at every size. Move key establishment to ML-KEM (hybrid with X25519 or ECDH during the transition) and signatures to ML-DSA or SLH-DSA. |
| Shor's algorithm — elliptic-curve discrete logarithms | breaks | Q1 | BLS12-381 (18), ECDSA (64), Ed25519 (76), X25519 (18) | Elliptic-curve keys are expected to fall before RSA keys of comparable classical strength. On blockchains, coins whose public key is already on chain (reused addresses, pay-to-public-key and Taproot outputs) are exposed first; plan the move to post-quantum signatures and avoid key reuse in the meantime. |
| Grover's algorithm — key search and preimages | weakens (larger keys restore the margin) | Q1 | AES-256 (2), Argon2 (17), BLAKE2 (28), ChaCha20-Poly1305 (21), HMAC (16), Keccak-256 (8), MD5 (1), PBKDF2 (2), Poly1305 (18), SHA-2 (29), XSalsa20-Poly1305 (29), scrypt (3) | Not a break. 256-bit keys (AES-256, ChaCha20) keep a comfortable margin; AES-128 meets NIST category 1, while some authorities ask for 256-bit keys in quantum-resistant contexts (see the AES-128 entry). Prefer 256-bit keys for long-lived data; 256-bit hashes need no change for preimage resistance. |
| Brassard–Høyer–Tapp — collision search | weakens (larger keys restore the margin) | Q1 | BLAKE2 (28), Keccak-256 (8), MD5 (1), SHA-2 (29) | 256-bit hashes (SHA-256, SHA3-256) remain adequate for collision resistance; 160-bit hashes are already weak classically (SHA-1 collisions are practical). Use 384/512-bit hashes where NIST categories 4–5 are required. |

_Effects: breaks — replace the algorithm; weakens — larger keys or outputs restore the margin; included in standard parameters — no action at standard parameter sets; only with superposition queries — not applicable to ordinary deployments._


## 9. Limitations and assumptions

- This report presents automated and documented analysis results for the stated scope. It is not a legal opinion, a certification or an attestation of compliance with any standard.
- z is a planning assumption chosen per risk profile, not a prediction. A cryptographically relevant quantum computer is not publicly known to exist today.
- tls_key_exchange_groups: lib/fmt/support/docopt.py line 80: not in the algorithm registry, not assessed: [[pattern]]
- osv_advisories: 14 package(s) are built from git repositories (forks or unreleased code), so registry advisories were not looked up for them: soroban-builtin-sdk-macros, soroban-env-common, soroban-env-host, soroban-env-macros, soroban-fuzz-targets, soroban-synth-wasm, soroban-test-wasms, soroban-wasmi, stellar-quorum-analyzer, stellar-strkey, stellar-xdr, wasmi_arena …

## 10. Remediation plan / Priorities for 30, 60 and 90 days

### 30 days

| Priority | ID | Action | Type | Closure criteria |
|---|---|---|---|---|
| P1 | QSI-2026-19575 | Rotate and remove secrets found in lib/sqlite/sqlite3.c. | root-cause fix | Secret scanner reports no secrets; old values revoked. |
| P1 | QSI-2026-19582 | Rotate and remove secrets found in lib/tracy/nfd/nfd_portal.cpp. | root-cause fix | Secret scanner reports no secrets; old values revoked. |
| P1 | QSI-2026-19587 | Use the platform CSPRNG (secrets, os.urandom, crypto.getRandomValues, crypto/rand, SecureRandom, OsRng) or a hardware TRNG for every key, seed and mnemonic. | root-cause fix | Re-scan the source and review the call sites listed in the evidence. |
| P2 | QSI-2026-19595 | Upgrade stellar-xdr to a fixed version (25.0.1). | root-cause fix | Dependency scan no longer reports GHSA-x57h-xx53-v53w (CVE-2026-29795). |
| P2 | QSI-2026-19596 | Upgrade stellar-xdr to a fixed version (25.0.1). | root-cause fix | Dependency scan no longer reports GHSA-x57h-xx53-v53w (CVE-2026-29795). |
| P2 | QSI-2026-19597 | Upgrade stellar-xdr to a fixed version (25.0.1). | root-cause fix | Dependency scan no longer reports GHSA-x57h-xx53-v53w (CVE-2026-29795). |
| P2 | QSI-2026-19598 | Upgrade stellar-xdr to a fixed version (25.0.1). | root-cause fix | Dependency scan no longer reports GHSA-x57h-xx53-v53w (CVE-2026-29795). |
| P2 | QSI-2026-19615 | Upgrade stellar-xdr to a fixed version (25.0.1). | root-cause fix | Dependency scan no longer reports GHSA-x57h-xx53-v53w (CVE-2026-29795). |
| P2 | QSI-2026-19617 | Upgrade soroban-sdk to a fixed version (22.0.9, 23.5.1, 25.0.2). | root-cause fix | Dependency scan no longer reports GHSA-96xm-fv9w-pf3f (CVE-2026-24889). |
| P2 | QSI-2026-19618 | Upgrade soroban-sdk to a fixed version (22.0.11, 23.5.3, 25.3.0). | root-cause fix | Dependency scan no longer reports GHSA-x2hw-px52-wp4m (CVE-2026-32322). |
| P2 | QSI-2026-19623 | Upgrade stellar-xdr to a fixed version (25.0.1). | root-cause fix | Dependency scan no longer reports GHSA-x57h-xx53-v53w (CVE-2026-29795). |
| P2 | QSI-2026-19600 | Upgrade serde_with to a fixed version (3.21.0). | root-cause fix | Dependency scan no longer reports GHSA-7gcf-g7xr-8hxj. |
| P2 | QSI-2026-19608 | Upgrade serde_with to a fixed version (3.21.0). | root-cause fix | Dependency scan no longer reports GHSA-7gcf-g7xr-8hxj. |
| P2 | QSI-2026-19609 | Upgrade time to a fixed version (0.3.47). | root-cause fix | Dependency scan no longer reports GHSA-r6v5-fh4h-64xc (CVE-2026-25727, RUSTSEC-2026-0009). |
| P2 | QSI-2026-19619 | Upgrade serde_with to a fixed version (3.21.0). | root-cause fix | Dependency scan no longer reports GHSA-7gcf-g7xr-8hxj. |
| P2 | QSI-2026-19620 | Upgrade time to a fixed version (0.3.47). | root-cause fix | Dependency scan no longer reports GHSA-r6v5-fh4h-64xc (CVE-2026-25727, RUSTSEC-2026-0009). |
| P2 | QSI-2026-19622 | Upgrade serde_with to a fixed version (3.21.0). | root-cause fix | Dependency scan no longer reports GHSA-7gcf-g7xr-8hxj. |
| P2 | QSI-2026-19594 | Upgrade rand to a fixed version (0.10.1, 0.8.6, 0.9.3). | root-cause fix | Dependency scan no longer reports GHSA-cq8v-f236-94qc (RUSTSEC-2026-0097). |
| P2 | QSI-2026-19601 | Upgrade soroban-env-host to a fixed version (26.0.0). | root-cause fix | Dependency scan no longer reports GHSA-pm4j-7r4q-ccg8. |
| P2 | QSI-2026-19605 | Upgrade curve25519-dalek to a fixed version (4.1.3). | root-cause fix | Dependency scan no longer reports GHSA-x4gp-pqpj-f43q (CVE-2024-58262, RUSTSEC-2024-0344). |
| P2 | QSI-2026-19611 | Upgrade soroban-env-host to a fixed version (26.0.0). | root-cause fix | Dependency scan no longer reports GHSA-pm4j-7r4q-ccg8. |
| P2 | QSI-2026-19614 | Upgrade soroban-env-host to a fixed version (26.0.0). | root-cause fix | Dependency scan no longer reports GHSA-pm4j-7r4q-ccg8. |
| P2 | QSI-2026-19616 | Upgrade soroban-env-host to a fixed version (26.0.0). | root-cause fix | Dependency scan no longer reports GHSA-pm4j-7r4q-ccg8. |
| P2 | QSI-2026-19621 | Upgrade soroban-env-host to a fixed version (26.0.0). | root-cause fix | Dependency scan no longer reports GHSA-pm4j-7r4q-ccg8. |
| P2 | QSI-2026-19624 | Upgrade soroban-env-host to a fixed version (26.0.0). | root-cause fix | Dependency scan no longer reports GHSA-pm4j-7r4q-ccg8. |
| P2 | QSI-2026-19599 | Upgrade tracing-subscriber to a fixed version (0.3.20). | root-cause fix | Dependency scan no longer reports GHSA-xwfj-jgwm-7wp5 (CVE-2025-58160, RUSTSEC-2025-0055). |
| P2 | QSI-2026-19610 | Upgrade tracing-subscriber to a fixed version (0.3.20). | root-cause fix | Dependency scan no longer reports GHSA-xwfj-jgwm-7wp5 (CVE-2025-58160, RUSTSEC-2025-0055). |
| P2 | QSI-2026-19592 | Upgrade keccak to a fixed version (0.1.6). | root-cause fix | Dependency scan no longer reports GHSA-3288-p39f-rqpv (RUSTSEC-2026-0012). |
| P2 | QSI-2026-19606 | Upgrade keccak to a fixed version (0.1.6). | root-cause fix | Dependency scan no longer reports GHSA-3288-p39f-rqpv (RUSTSEC-2026-0012). |
### 60 days

| Priority | ID | Action | Type | Closure criteria |
|---|---|---|---|---|
| P2 | QSI-2026-19576 | Use a CSPRNG (secrets, crypto.getRandomValues, crypto/rand). | root-cause fix | Re-scan the source and review the call sites listed in the evidence. |
| P3 | QSI-2026-19580 | Review each MD5 call site in lib/gperftools/src/gen_getpc.rb; replace security-relevant ones with SHA-256 or a password hash. | root-cause fix | No security-relevant MD5 usage remains. |
| P3 | QSI-2026-19588 | Triage RUSTSEC-2026-0387; upgrade crypto-bigint to a fixed version (0.7.6) if it applies. | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0387, or the triage is recorded. |
| P3 | QSI-2026-19589 | Triage RUSTSEC-2026-0385; upgrade ctutils to a fixed version (0.4.4) if it applies. | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0385, or the triage is recorded. |
| P3 | QSI-2026-19590 | Triage RUSTSEC-2026-0202; upgrade cxx to a fixed version (1.0.195) if it applies. | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0202, or the triage is recorded. |
| P3 | QSI-2026-19603 | Triage RUSTSEC-2026-0190; upgrade anyhow to a fixed version (1.0.103) if it applies. | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0190, or the triage is recorded. |
| P3 | QSI-2026-19604 | Triage RUSTSEC-2026-0387; upgrade crypto-bigint to a fixed version (0.7.6) if it applies. | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0387, or the triage is recorded. |
| P3 | QSI-2026-19612 | Triage RUSTSEC-2026-0387; upgrade crypto-bigint to a fixed version (0.7.6) if it applies. | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0387, or the triage is recorded. |
### 90 days

| Priority | ID | Action | Type | Closure criteria |
|---|---|---|---|---|
| P3 | QSI-2026-19581 | Add X25519 usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-19579 | Add Ed25519 usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-19583 | Add ECDSA usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-19577 | Add X25519 usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-19578 | Add Ed25519 usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-19584 | Add ECDSA usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-19585 | Add Ed25519 usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-19586 | Add BLS12-381 usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P4 | QSI-2026-19581 | Plan migration of X25519 to Hybrid key establishment with ML-KEM (FIPS 203), e.g. X25519MLKEM768 in TLS 1.3 or mlkem768x25519-sha256 in SSH (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows Hybrid key establishment with ML-KEM (FIPS 203), e.g. X25519MLKEM768 in TLS 1.3 or mlkem768x25519-sha256 in SSH or a hybrid scheme in use. |
| P4 | QSI-2026-19579 | Plan migration of Ed25519 to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-19583 | Plan migration of ECDSA to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-19577 | Plan migration of X25519 to Hybrid key establishment with ML-KEM (FIPS 203), e.g. X25519MLKEM768 in TLS 1.3 or mlkem768x25519-sha256 in SSH (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows Hybrid key establishment with ML-KEM (FIPS 203), e.g. X25519MLKEM768 in TLS 1.3 or mlkem768x25519-sha256 in SSH or a hybrid scheme in use. |
| P4 | QSI-2026-19578 | Plan migration of Ed25519 to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-19584 | Plan migration of ECDSA to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-19585 | Plan migration of Ed25519 to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-19586 | Plan migration of BLS12-381 to  (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows  or a hybrid scheme in use. |
| P4 | QSI-2026-19591 | Replace derivative with a maintained alternative or record why it stays. | root-cause fix | derivative replaced, or the decision recorded. |
| P4 | QSI-2026-19593 | Replace paste with a maintained alternative or record why it stays. | root-cause fix | paste replaced, or the decision recorded. |
| P4 | QSI-2026-19602 | Replace adler with a maintained alternative or record why it stays. | root-cause fix | adler replaced, or the decision recorded. |
| P4 | QSI-2026-19607 | Replace paste with a maintained alternative or record why it stays. | root-cause fix | paste replaced, or the decision recorded. |
| P4 | QSI-2026-19613 | Replace paste with a maintained alternative or record why it stays. | root-cause fix | paste replaced, or the decision recorded. |

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
3. C. Gidney, M. Ekerå — How to factor 2048 bit RSA integers in 8 hours using 20 million noisy qubits (Quantum 5, 433) — Quantum. <https://doi.org/10.22331/q-2021-04-15-433> (peer-reviewed article (2021): 10^-3 gate error, 1 µs cycle, 10 µs reaction time)
4. C. Zalka — Grover's quantum searching algorithm is optimal (Phys. Rev. A 60, 2746, 1999; arXiv:quant-ph/9711070) — APS. <https://doi.org/10.1103/PhysRevA.60.2746> (peer-reviewed article: optimal for any success probability; parallel search gains no more than splitting the space)
5. CVE-2023-31290 — Trust Wallet Core: 32 bits of mnemonic entropy (mt19937 seeded with one 32-bit value) — NIST NVD. <https://nvd.nist.gov/vuln/detail/CVE-2023-31290> (published 2023-04-27; Trust Wallet Core before 3.1.1 (browser extension 0.0.172-0.0.182), exploited in the wild in December 2022 and March 2023: only about four billion possible mnemonics)
6. CVE-2023-39910 — Libbitcoin Explorer 'bx seed' entropy (Milk Sad): mt19937 limits it to 32 bits — NIST NVD. <https://nvd.nist.gov/vuln/detail/CVE-2023-39910> (published 2023-08-09; Libbitcoin Explorer 3.0.0-3.6.0, exploited in the wild in 2023)
7. CWE-338 — Use of Cryptographically Weak Pseudo-Random Number Generator (PRNG) — MITRE. <https://cwe.mitre.org/data/definitions/338.html> (weakness catalogue entry: the consequence is predictable values where unpredictability was assumed, which is what makes a token or key guessable)
8. Common Vulnerability Scoring System v3.1: Specification Document — FIRST. <https://www.first.org/cvss/v3.1/specification-document> (final)
9. D. J. Bernstein — Cost analysis of hash collisions: Will quantum computers make SHARCS obsolete? (2009) — cr.yp.to. <https://cr.yp.to/hash/collisioncost-20090823.pdf> (paper dated 2009-08-23)
10. D. Litinski — How to compute a 256-bit elliptic curve private key with only 50 million Toffoli gates (arXiv:2306.08585) — arXiv. <https://arxiv.org/abs/2306.08585> (preprint (2023-06-14): 6000 modules × 1152 physical qubits, one key per 10 minutes under its architecture assumptions)
11. FIPS 203 — Module-Lattice-Based Key-Encapsulation Mechanism Standard (ML-KEM) — NIST. <https://csrc.nist.gov/pubs/fips/203/final> (final (August 2024))
12. FIPS 204 — Module-Lattice-Based Digital Signature Standard (ML-DSA) — NIST. <https://csrc.nist.gov/pubs/fips/204/final> (final (August 2024))
13. FIPS 205 — Stateless Hash-Based Digital Signature Standard (SLH-DSA) — NIST. <https://csrc.nist.gov/pubs/fips/205/final> (final (August 2024))
14. G. Brassard, P. Høyer, A. Tapp — Quantum Algorithm for the Collision Problem (LATIN '98; arXiv:quant-ph/9705002) — Springer / arXiv. <https://arxiv.org/abs/quant-ph/9705002> (peer-reviewed article: collisions of r-to-one functions in O((N/r)^{1/3}) expected evaluations)
15. J. Proos, C. Zalka — Shor's discrete logarithm quantum algorithm for elliptic curves (Quantum Inf. Comput. 3(4), 2003; arXiv:quant-ph/0301141) — Quantum Information & Computation. <https://doi.org/10.26421/QIC3.4-3> (peer-reviewed article)
16. L. K. Grover — A fast quantum mechanical algorithm for database search (STOC 1996) — ACM. <https://doi.org/10.1145/237814.237866> (peer-reviewed article)
17. M. Amy et al. — Estimating the cost of generic quantum pre-image attacks on SHA-2 and SHA-3 (SAC 2016; arXiv:1603.09383) — Springer / arXiv. <https://arxiv.org/abs/1603.09383> (peer-reviewed article: SHA-256 about 2^153.8 surface-code cycles on 2^12.6 logical qubits; SHA3-256 about 2^146.5 cycles on 2^20)
18. M. Cain et al. — Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits (arXiv:2603.28627) — arXiv. <https://arxiv.org/abs/2603.28627> (preprint (2026-03-30): P-256 in a few days with 26,000 physical neutral-atom qubits; RSA-2048 one to two orders of magnitude longer)
19. M. Ekerå, J. Gärtner — A high-level comparison of state-of-the-art quantum algorithms for breaking asymmetric cryptography (arXiv:2405.14381) — arXiv. <https://arxiv.org/abs/2405.14381> (preprint (2024-05-23): Regev-style algorithms show no overall advantage yet for cryptographic RSA and finite-field sizes)
20. M. Mosca — Cybersecurity in an Era with Quantum Computers: Will We Be Ready? (IEEE Security & Privacy, 2018) — IEEE. <https://doi.org/10.1109/MSP.2018.3761723> (peer-reviewed article; source of the x + y > z migration inequality)
21. M. Roetteler, M. Naehrig, K. Svore, K. Lauter — Quantum resource estimates for computing elliptic curve discrete logarithms (ASIACRYPT 2017) — IACR / arXiv. <https://arxiv.org/abs/1706.06752> (peer-reviewed article: at most 9n + 2⌈log2 n⌉ + 10 qubits and 448 n^3 log2 n + 4090 n^3 Toffoli gates)
22. NIST IR 8547 — Transition to Post-Quantum Cryptography Standards — NIST. <https://csrc.nist.gov/pubs/ir/8547/final> (final (2026-10-27; the initial public draft of November 2024 is obsoleted). Tables 2 and 4: ECDSA, EdDSA and RSA signatures, finite-field and elliptic-curve DH and MQV, and RSA key establishment are deprecated after 2030 and disallowed after 2035 at every key size — the draft deprecated only the 112-bit level. A composite (hybrid) key establishment stays FIPS 140-validatable while one input comes from an approved scheme. Repeats the federal deadlines of OMB M-26-15: post-quantum key establishment by 2030-12-31 and signatures by 2031-12-31 for high value assets and high impact systems)
23. NIST SP 800-131A Rev. 2 — Transitioning the Use of Cryptographic Algorithms and Key Lengths — NIST. <https://csrc.nist.gov/pubs/sp/800/131/a/r2/final> (final (2019))
24. NIST SP 800-90A Rev. 1 — Recommendation for Random Number Generation Using Deterministic Random Bit Generators — NIST. <https://csrc.nist.gov/pubs/sp/800/90/a/r1/final> (final (June 2015; supersedes SP 800-90A of 2012): which constructions count as a cryptographically secure generator, and why a general-purpose PRNG does not)
25. NIST — Post-Quantum Cryptography Standardization: Evaluation Criteria, Security (Call for Proposals, Section 4.A.5) — NIST. <https://csrc.nist.gov/Projects/Post-Quantum-Cryptography/Post-Quantum-Cryptography-Standardization/Evaluation-Criteria/Security-(Evaluation-Criteria)> (security categories: AES-128 key search 2^170/MAXDEPTH quantum gates, AES-192 2^233/MAXDEPTH, AES-256 2^298/MAXDEPTH; MAXDEPTH 2^40–2^96)
26. OSV advisory GHSA-3288-p39f-rqpv — OSV.dev. <https://osv.dev/vulnerability/GHSA-3288-p39f-rqpv> (modified 2026-09-10T03:50:59.332505686Z)
27. OSV advisory GHSA-7gcf-g7xr-8hxj — OSV.dev. <https://osv.dev/vulnerability/GHSA-7gcf-g7xr-8hxj> (modified 2026-09-10T03:51:10.897685062Z)
28. OSV advisory GHSA-96xm-fv9w-pf3f — OSV.dev. <https://osv.dev/vulnerability/GHSA-96xm-fv9w-pf3f> (modified 2026-02-03T03:04:15.587576Z)
29. OSV advisory GHSA-cq8v-f236-94qc — OSV.dev. <https://osv.dev/vulnerability/GHSA-cq8v-f236-94qc> (modified 2026-09-10T03:50:43.958966498Z)
30. OSV advisory GHSA-pm4j-7r4q-ccg8 — OSV.dev. <https://osv.dev/vulnerability/GHSA-pm4j-7r4q-ccg8> (modified 2026-03-07T02:47:39.508852Z)
31. OSV advisory GHSA-r6v5-fh4h-64xc — OSV.dev. <https://osv.dev/vulnerability/GHSA-r6v5-fh4h-64xc> (modified 2026-09-10T03:50:35.583241382Z)
32. OSV advisory GHSA-x2hw-px52-wp4m — OSV.dev. <https://osv.dev/vulnerability/GHSA-x2hw-px52-wp4m> (modified 2026-03-16T17:16:39.585918Z)
33. OSV advisory GHSA-x4gp-pqpj-f43q — OSV.dev. <https://osv.dev/vulnerability/GHSA-x4gp-pqpj-f43q> (modified 2026-09-10T03:50:15.886084155Z)
34. OSV advisory GHSA-x57h-xx53-v53w — OSV.dev. <https://osv.dev/vulnerability/GHSA-x57h-xx53-v53w> (modified 2026-03-06T23:02:40.557695Z)
35. OSV advisory GHSA-xwfj-jgwm-7wp5 — OSV.dev. <https://osv.dev/vulnerability/GHSA-xwfj-jgwm-7wp5> (modified 2026-09-10T03:50:27.766863705Z)
36. OSV advisory RUSTSEC-2024-0388 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2024-0388> (modified 2024-11-10T13:34:40Z)
37. OSV advisory RUSTSEC-2024-0436 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2024-0436> (modified 2026-01-27T22:03:15.694766Z)
38. OSV advisory RUSTSEC-2025-0056 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2025-0056> (modified 2025-09-05T09:05:48Z)
39. OSV advisory RUSTSEC-2026-0190 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0190> (modified 2026-06-29T14:15:03.650725453Z)
40. OSV advisory RUSTSEC-2026-0202 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0202> (modified 2026-07-05T08:45:04.168768726Z)
41. OSV advisory RUSTSEC-2026-0385 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0385> (modified 2026-10-23T08:30:02.389575143Z)
42. OSV advisory RUSTSEC-2026-0387 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0387> (modified 2026-10-24T03:45:02.365137418Z)
43. OWASP Application Security Verification Standard — OWASP. <https://owasp.org/www-project-application-security-verification-standard/> (living standard — check the project page for the current version)
44. P. W. Shor — Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms on a Quantum Computer (SIAM J. Comput., 1997) — SIAM. <https://doi.org/10.1137/S0097539795293172> (peer-reviewed article)
45. R. Babbush et al. — Securing Elliptic Curve Cryptocurrencies against Quantum Vulnerabilities: Resource Estimates and Mitigations (arXiv:2603.28846) — arXiv. <https://arxiv.org/abs/2603.28846> (preprint (2026-03-30, v2 2026-04-15): 256-bit ECDLP with < 1200 logical qubits and < 90 M Toffoli gates (or < 1450 and < 70 M); < 500,000 physical qubits at 10^-3 error, minutes)
46. S. Jaques, M. Naehrig, M. Roetteler, F. Virdia — Implementing Grover oracles for quantum key search on AES and LowMC (EUROCRYPT 2020; arXiv:1910.01700) — Springer / arXiv. <https://arxiv.org/abs/1910.01700> (peer-reviewed article: lower cost estimates for the AES key searches that define the NIST categories)

## Appendices: Cryptographic inventory

By origin: dependency manifests 69 (0 Shor-breakable) · own code 186 (143 Shor-breakable) · third-party code in the tree 164 (33 Shor-breakable).

| Algorithm | Parameter | Library | Quantum status | Classical status | Count | Locations | Examples |
|---|---|---|---|---|---|---|---|
| MD5 |  |  | weak classically | broken | 1 | 1 | lib/gperftools/src/gen_getpc.rb:145 |
| AES-256 |  |  | reduced margin (Grover), approved | acceptable | 2 | 2 | lib/libsodium/src/libsodium/crypto_aead/aes256gcm/aesni/aead_aes256gcm_aesni.c; lib/libsodium/src/libsodium/include/sodium/crypto_aead_aes256gcm.h |
| Argon2 |  |  | reduced margin (Grover), approved | acceptable | 17 | 17 | lib/libsodium/src/libsodium/crypto_pwhash/argon2/argon2-core.c; lib/libsodium/src/libsodium/crypto_pwhash/argon2/argon2-core.h; lib/libsodium/src/libsodium/crypto_pwhash/argon2/argon2-encoding.c |
| ChaCha20-Poly1305 | ChaCha20-Poly1305 |  | reduced margin (Grover), approved | acceptable | 7 | 7 | lib/libsodium/src/libsodium/crypto_aead/chacha20poly1305/sodium/aead_chacha20poly1305.c:8; lib/libsodium/src/libsodium/crypto_aead/xchacha20poly1305/sodium/aead_xchacha20poly1305.c:8; lib/libsodium/src/libsodium/crypto_secretstream/xchacha20poly1305/secretstream_xchacha20poly1305.c:7 |
| ChaCha20-Poly1305 |  |  | reduced margin (Grover), approved | acceptable | 14 | 14 | lib/libsodium/src/libsodium/crypto_secretbox/xchacha20poly1305/secretbox_xchacha20poly1305.c; lib/libsodium/src/libsodium/crypto_stream/chacha20/dolbeau/chacha20_dolbeau-avx2.c; lib/libsodium/src/libsodium/crypto_stream/chacha20/dolbeau/chacha20_dolbeau-avx2.h |
| HMAC | HMAC-SHA-256 |  | reduced margin (Grover), approved | acceptable | 2 | 2 | lib/libsodium/src/libsodium/crypto_auth/hmacsha256/auth_hmacsha256.c; lib/libsodium/src/libsodium/include/sodium/crypto_auth_hmacsha256.h |
| HMAC | HMAC-SHA-512 |  | reduced margin (Grover), approved | acceptable | 2 | 2 | lib/libsodium/src/libsodium/crypto_auth/hmacsha512/auth_hmacsha512.c; lib/libsodium/src/libsodium/include/sodium/crypto_auth_hmacsha512.h |
| HMAC |  |  | reduced margin (Grover), approved | acceptable | 12 | 12 | src/crypto/Curve25519.cpp:50; src/crypto/Curve25519.h:45; src/crypto/SHA.cpp:85 |
| PBKDF2 |  |  | reduced margin (Grover), approved | acceptable | 2 | 2 | lib/libsodium/src/libsodium/crypto_pwhash/scryptsalsa208sha256/pbkdf2-sha256.c; lib/libsodium/src/libsodium/crypto_pwhash/scryptsalsa208sha256/pbkdf2-sha256.h |
| Poly1305 |  |  | reduced margin (Grover), approved | acceptable | 18 | 18 | lib/libsodium/src/libsodium/crypto_aead/chacha20poly1305/sodium/aead_chacha20poly1305.c:9; lib/libsodium/src/libsodium/crypto_aead/xchacha20poly1305/sodium/aead_xchacha20poly1305.c:11; lib/libsodium/src/libsodium/crypto_onetimeauth/crypto_onetimeauth.c:27 |
| SHA-2 | SHA-512 |  | reduced margin (Grover), approved | acceptable | 3 | 3 | lib/libsodium/src/libsodium/crypto_hash/sha512/cp/hash_sha512_cp.c:61; lib/libsodium/src/libsodium/crypto_hash/sha512/hash_sha512.c; lib/libsodium/src/libsodium/include/sodium/crypto_hash_sha512.h |
| XSalsa20-Poly1305 | XSalsa20-Poly1305 |  | reduced margin (Grover), approved | acceptable | 17 | 17 | lib/libsodium/src/libsodium/crypto_box/crypto_box_easy.c:8; lib/libsodium/src/libsodium/crypto_box/curve25519xchacha20poly1305/box_curve25519xchacha20poly1305.c:12; lib/libsodium/src/libsodium/crypto_box/curve25519xsalsa20poly1305/box_curve25519xsalsa20poly1305.c:7 |
| XSalsa20-Poly1305 |  |  | reduced margin (Grover), approved | acceptable | 12 | 12 | lib/libsodium/src/libsodium/crypto_stream/salsa20/ref/salsa20_ref.c; lib/libsodium/src/libsodium/crypto_stream/salsa20/ref/salsa20_ref.h; lib/libsodium/src/libsodium/crypto_stream/salsa20/stream_salsa20.c |
| scrypt |  |  | reduced margin (Grover), approved | acceptable | 3 | 3 | lib/libsodium/src/libsodium/crypto_pwhash/scryptsalsa208sha256/crypto_scrypt-common.c; lib/libsodium/src/libsodium/crypto_pwhash/scryptsalsa208sha256/crypto_scrypt.h; lib/libsodium/src/libsodium/crypto_pwhash/scryptsalsa208sha256/scrypt_platform.c |
| BLAKE2 |  |  | Grover: acceptable to NIST, below ECCG/ANSSI guidance | acceptable | 28 | 28 | lib/libsodium/src/libsodium/crypto_box/crypto_box_seal.c:5; lib/libsodium/src/libsodium/crypto_box/curve25519xchacha20poly1305/box_seal_curve25519xchacha20poly1305.c:5; lib/libsodium/src/libsodium/crypto_generichash/blake2b/generichash_blake2.c |
| Keccak-256 | Keccak-256 |  | Grover: acceptable to NIST, below ECCG/ANSSI guidance | acceptable | 8 | 8 | src/rust/soroban/p21/soroban-env-host/src/cost_runner/cost_types/compute_keccak256_hash.rs; src/rust/soroban/p21/soroban-env-host/src/host/crypto.rs:15; src/rust/soroban/p22/soroban-env-host/src/cost_runner/cost_types/compute_keccak256_hash.rs |
| SHA-2 | SHA-256 |  | Grover: acceptable to NIST, below ECCG/ANSSI guidance | acceptable | 26 | 26 | lib/libsodium/src/libsodium/crypto_hash/sha256/cp/hash_sha256_cp.c:61; lib/libsodium/src/libsodium/crypto_hash/sha256/hash_sha256.c; lib/libsodium/src/libsodium/crypto_pwhash/scryptsalsa208sha256/pbkdf2-sha256.c |
| Crypto library | 0.13.2 | p256 (RustCrypto elliptic curves) | n/a | acceptable | 12 | 12 | Cargo.lock; scripts/apply_load/token/Cargo.lock; src/rust/soroban/p21/Cargo.lock |
| Crypto library | 0.13.4 | k256 (RustCrypto elliptic curves) | n/a | acceptable | 6 | 6 | Cargo.lock; scripts/apply_load/token/Cargo.lock; src/rust/soroban/p22/Cargo.lock |
| Crypto library | 0.16.9 | ecdsa (python-ecdsa) | n/a | acceptable | 6 | 6 | Cargo.lock; scripts/apply_load/token/Cargo.lock; src/rust/soroban/p22/Cargo.lock |
| Crypto library | 2.2.0 | ed25519-dalek (ed25519-dalek) | n/a | acceptable | 2 | 2 | Cargo.lock; scripts/apply_load/token/Cargo.lock |
| Crypto library | 4.1.3 | curve25519-dalek (ed25519-dalek) | n/a | acceptable | 6 | 6 | Cargo.lock; scripts/apply_load/token/Cargo.lock; src/rust/soroban/p22/Cargo.lock |
| Crypto library | 2.1.1 | ed25519-dalek (ed25519-dalek) | n/a | acceptable | 5 | 5 | src/rust/Cargo.toml; src/rust/soroban/p22/Cargo.lock; src/rust/soroban/p22/soroban-test-wasms/wasm-workspace/Cargo.lock |
| Crypto library | 0.13.1 | k256 (RustCrypto elliptic curves) | n/a | acceptable | 7 | 7 | src/rust/soroban/p21/Cargo.lock; src/rust/soroban/p21/soroban-env-host/Cargo.toml; src/rust/soroban/p21/soroban-test-wasms/wasm-workspace/Cargo.lock |
| Crypto library | 0.16.7 | ecdsa (python-ecdsa) | n/a | acceptable | 6 | 6 | src/rust/soroban/p21/Cargo.lock; src/rust/soroban/p21/soroban-env-host/Cargo.toml; src/rust/soroban/p22/soroban-env-host/Cargo.toml |
| Crypto library | 2.0.0 | ed25519-dalek (ed25519-dalek) | n/a | acceptable | 3 | 3 | src/rust/soroban/p21/Cargo.lock; src/rust/soroban/p21/soroban-test-wasms/wasm-workspace/Cargo.lock; src/rust/soroban/p23/soroban-test-wasms/wasm-workspace/Cargo.lock |
| Crypto library | 4.1.1 | curve25519-dalek (ed25519-dalek) | n/a | acceptable | 3 | 3 | src/rust/soroban/p21/Cargo.lock; src/rust/soroban/p21/soroban-test-wasms/wasm-workspace/Cargo.lock; src/rust/soroban/p22/soroban-test-wasms/wasm-workspace/Cargo.lock |
| Crypto library | >=2.0.0 | ed25519-dalek (ed25519-dalek) | n/a | acceptable | 4 | 4 | src/rust/soroban/p21/soroban-env-host/Cargo.toml; src/rust/soroban/p22/soroban-env-host/Cargo.toml; src/rust/soroban/p23/soroban-env-host/Cargo.toml |
| Crypto library | >=4.1.1 | curve25519-dalek (ed25519-dalek) | n/a | acceptable | 1 | 1 | src/rust/soroban/p21/soroban-env-host/Cargo.toml |
| Crypto library | 0.16.8 | ecdsa (python-ecdsa) | n/a | acceptable | 1 | 1 | src/rust/soroban/p21/soroban-test-wasms/wasm-workspace/Cargo.lock |
| Crypto library | 0.13.3 | k256 (RustCrypto elliptic curves) | n/a | acceptable | 3 | 3 | src/rust/soroban/p22/soroban-env-host/Cargo.toml; src/rust/soroban/p23/soroban-env-host/Cargo.toml; src/rust/soroban/p24/soroban-env-host/Cargo.toml |
| Crypto library | >=4.1.3 | curve25519-dalek (ed25519-dalek) | n/a | acceptable | 3 | 3 | src/rust/soroban/p22/soroban-env-host/Cargo.toml; src/rust/soroban/p23/soroban-env-host/Cargo.toml; src/rust/soroban/p24/soroban-env-host/Cargo.toml |
| PQC library | 0.1.1 | ml-dsa (RustCrypto post-quantum crates) | post-quantum | acceptable | 1 | 1 | Cargo.lock |
| BLS12-381 |  |  | vulnerable (Shor) | acceptable | 18 | 18 | src/rust/soroban/p22/soroban-env-host/src/cost_runner/cost_types/bls12_381.rs:6; src/rust/soroban/p22/soroban-env-host/src/cost_runner/cost_types/mod.rs:1; src/rust/soroban/p22/soroban-env-host/src/cost_runner/experimental/bls12_381.rs |
| ECDSA |  |  | vulnerable (Shor) | acceptable | 24 | 24 | src/rust/soroban/p21/soroban-env-host/src/cost_runner/cost_types/decode_ecdsa_curve256_sig.rs; src/rust/soroban/p21/soroban-env-host/src/cost_runner/cost_types/sec1_decode_point_uncompressed.rs:5; src/rust/soroban/p21/soroban-env-host/src/cost_runner/experimental/ecdsa_secp256r1_recover.rs:7 |
| ECDSA | secp256k1 |  | vulnerable (Shor) | acceptable | 16 | 16 | src/rust/soroban/p21/soroban-env-host/src/cost_runner/cost_types/recover_ecdsa_secp256k1_key.rs:7; src/rust/soroban/p21/soroban-env-host/src/cost_runner/experimental/ecdsa_secp256k1_verify.rs:6; src/rust/soroban/p21/soroban-env-host/src/cost_runner/util.rs:12 |
| ECDSA | P-256 |  | vulnerable (Shor) | acceptable | 24 | 24 | src/rust/soroban/p21/soroban-env-host/src/cost_runner/cost_types/sec1_decode_point_uncompressed.rs:5; src/rust/soroban/p21/soroban-env-host/src/cost_runner/cost_types/verify_ecdsa_secp256r1_sig.rs:5; src/rust/soroban/p21/soroban-env-host/src/cost_runner/experimental/ecdsa_secp256r1_recover.rs:7 |
| Ed25519 | Ed25519 |  | vulnerable (Shor) | acceptable | 76 | 76 | lib/libsodium/src/libsodium/crypto_core/ed25519/core_ed25519.c; lib/libsodium/src/libsodium/crypto_core/ed25519/ref10/ed25519_ref10.c; lib/libsodium/src/libsodium/crypto_scalarmult/ed25519/ref10/scalarmult_ed25519_ref10.c |
| X25519 | X25519 |  | vulnerable (Shor) | acceptable | 12 | 12 | lib/libsodium/src/libsodium/crypto_box/crypto_box.c:72; lib/libsodium/src/libsodium/crypto_box/crypto_box_seal.c:32; lib/libsodium/src/libsodium/crypto_kx/crypto_kx.c:7 |
| X25519 |  |  | vulnerable (Shor) | acceptable | 6 | 6 | lib/libsodium/src/libsodium/crypto_scalarmult/curve25519/sandy2x/curve25519_sandy2x.c; lib/libsodium/src/libsodium/crypto_scalarmult/curve25519/sandy2x/curve25519_sandy2x.h; lib/libsodium/src/libsodium/crypto_scalarmult/curve25519/scalarmult_curve25519.c |

_Long lists are grouped here; the full per-file list is in the JSON report, signed with the same key._

## Appendices: Input files

| File | Size | SHA-256 | Redactions |
|---|---|---|---|
| Cargo.lock | 81148 | `467e294b5049bcae9544b405507ba4d9ce1fb3784e68a453514bf75d206ed038` | 0 |
| Cargo.toml | 609 | `173f391237ed93b1081b9594c426bb38440d01cb139b936b5b733d45ba4e4b4d` | 0 |
| lib/asio.cpp | 57 | `0b5f44cf69ac9dc0d7ed0d407e6de0634d2a3d5bd594fe5e68765bc8c01fa573` | 0 |
| lib/autocheck/include/autocheck/arbitrary.hpp | 3446 | `1bcffebcba1013cd0fe945013cfbdbd8c6893039e3d279e0495599c06a476fa3` | 0 |
| lib/autocheck/include/autocheck/autocheck.hpp | 90 | `1725a8cf40031e862e1471d9548e5205337457bfe100f5eb5ea4fa373a2aa1fb` | 0 |
| lib/autocheck/include/autocheck/check.hpp | 1654 | `677f4797f89723eab1de35d2b80095b0a1fd94ac99c011581ed58aa7ddf37cce` | 0 |
| lib/autocheck/include/autocheck/classifier.hpp | 3003 | `a6ac258c13bde86e431d3d0d6179a54f13896cf9959237ddac195bf9963ef468` | 0 |
| lib/autocheck/include/autocheck/distribution.hpp | 280 | `420b5cdddef0840eb6ed0a8afc8f48aa08bc0fff2575be3beedb60df3df956dd` | 0 |
| lib/autocheck/include/autocheck/function.hpp | 724 | `9cb3c8284708d8d967861e5df7e55db651ed10ee2cd62a23fd32b34add2ef496` | 0 |
| lib/autocheck/include/autocheck/generator.hpp | 8269 | `bbdfb66de649dced7e8874028b85710b9c89b13e9ec8407890e2b5a3e4c52205` | 0 |
| lib/autocheck/include/autocheck/generator_combinators.hpp | 2780 | `4c5a04245e18652f389b1426780c8f3bae09396fda3c47149da88c82134a6080` | 0 |
| lib/autocheck/include/autocheck/is_one_of.hpp | 571 | `e1f3de86dc7b55762422c78db1459c1a50e4e12eea3bd93582c6081e3c4ca91b` | 0 |
| lib/autocheck/include/autocheck/largest.hpp | 608 | `7f4be21db1fd0bf3751f6ea7ee6bd0d94ce0343d1080b1040043b38d1a7344aa` | 0 |
| lib/autocheck/include/autocheck/ostream.hpp | 413 | `ca0a0f9798c66e3335f0321b45ee5a23f700e77e31960e8bce938462335fa9e4` | 0 |
| lib/autocheck/include/autocheck/reporter.hpp | 2793 | `df09681b31963e0432e0a4b676bb1babc2976548665cabaccdb230828bdb0d47` | 0 |
| lib/autocheck/include/autocheck/sequence.hpp | 467 | `5310b871d974ec0bd06112a7eb107030af5701cd9c2fa5b956acc49d0af972dc` | 0 |
| lib/autocheck/include/autocheck/tuple.hpp | 919 | `33701c6226b240530180e4b6897819852002a4fb15a9235e0695f4ab3688d0c4` | 0 |
| lib/autocheck/include/autocheck/value.hpp | 2178 | `046714e9633c06140160eab79e48bba29d9ab42f4822a2b314091f0327d727c3` | 0 |
| lib/binaryfusefilter.h | 23959 | `ce639768153dffc68a0bc7818ffd9e2106b0b7ce101f112f9f393165b8e9f33e` | 0 |
| lib/catch.hpp | 657411 | `3725c0f0a75f376a5005dde31ead0feb8f7da7507644c201b814443de8355170` | 0 |
| lib/clara.hpp | 43157 | `442e9a90879b2724b9ab4657184111c694c6cca792bb1d2047568cc07f53560a` | 0 |
| lib/http/HttpClient.cpp | 3299 | `4adb3ed8be5d8dc4505aad0c80f856dc063e298d76c322895bbda7827866822a` | 0 |
| lib/http/HttpClient.h | 119 | `7649437dc821230c2736ade9172b7a98cf75336907e00a84340d30c7e4dcb44a` | 0 |
| lib/http/connection.cpp | 2667 | `710ffe1e42af102a53d20ef5489133d1a3b0e4c0289e22c8909c8f63ab1c358a` | 0 |
| lib/http/connection.hpp | 2013 | `93020e390b74eb0b7f2cba4b84125ad4e7cf3c55c42c211c3877d25e6975315d` | 0 |
| lib/http/connection_manager.cpp | 768 | `3f1d7c3a0aa0c91601e2c330869b3b03fecc22745e57e05c4f3a3103aec0699d` | 0 |
| lib/http/connection_manager.hpp | 1160 | `9d21b54a631c5ecfbbf169a733fc6559895bfae495d9b5c4fa4c5c2b69e1d6a8` | 0 |
| lib/http/header.hpp | 508 | `fbeb2d8d553af1f50a71c8ef432e00ed39cdb9702bfb795671cab661b5bc7be4` | 0 |
| lib/http/reply.cpp | 8294 | `044d3f44eefef044b945fb734f3136a1f70ce9c4208612c35a4a3572e390054e` | 0 |
| lib/http/reply.hpp | 1610 | `c6a59f8da7f1db7c41b0b15ef92e208edb15ba844b4415d857e09dd1c127db75` | 0 |
| lib/http/request.hpp | 675 | `538e9dfd4a4328313b944d6b433fedc45e94f78a4a887c74f8d1f203c503bcdc` | 0 |
| lib/http/request_parser.cpp | 7243 | `3b7e6bc3fd516199719d55c43b5a8c9e8ebd82e530919a5fa5909815d2235fd7` | 0 |
| lib/http/request_parser.hpp | 2340 | `874a2516e141b68e64cdb5f3aeacc60ebb461623559b607c1371b7ff2a7ca267` | 0 |
| lib/http/server.cpp | 5261 | `176e191a08024a7198afcd58e72652dc986872a0be0e4222aad2afdccc80615d` | 0 |
| lib/http/server.hpp | 2405 | `96d39b2edb47822d569c0ca70cb030c816782dfe9708bc64807e12e8480d1971` | 0 |
| lib/httpthreaded/connection.cpp | 3198 | `8cafc55419edaed42604d867966416ad471758d23a4f43394de0f6a1bba63f00` | 0 |
| lib/httpthreaded/connection.hpp | 1848 | `767f6c3657dd06a99ebdc15d60a159f67a580d41f4d8acee15cc1f56a5a7e7ac` | 0 |
| lib/httpthreaded/header.hpp | 555 | `16c692bff880f4b86cded2fbd5f698596d13bbd07e7d6294b310070a1f20eee7` | 0 |
| lib/httpthreaded/reply.cpp | 8331 | `6250e19d0ab6afa9104563c8d08e5adab33e0fdd6c1c2a968d1dc22e608feaea` | 0 |
| lib/httpthreaded/reply.hpp | 1718 | `af0c4390ce5ad12e7764c5638d8e37f6161ef27e35761898b8842d6acbb4e43d` | 0 |
| lib/httpthreaded/request.hpp | 752 | `0c1bcd04dbab87ea3edcab4430991545f18915ea523c18fefde60d87ddfc3f50` | 0 |
| lib/httpthreaded/request_parser.cpp | 8366 | `c687d0a8b5539194fc811fd70877c32d28bcb54a2931a23061e6d8b463144ca8` | 0 |
| lib/httpthreaded/request_parser.hpp | 3716 | `e91d80032ce0d24d2fcf3e3dd68222edaa1ee954ebf2a83e99aa5d19610b85af` | 0 |
| lib/httpthreaded/server.cpp | 7264 | `7df6c52ee4ca2c307fcd14c61ba045c568351cae047ad7056031c4a9ffddfdf0` | 0 |
| lib/httpthreaded/server.hpp | 2841 | `97c5f24927d2b357a661a963e1753fac282f69203c4c756b24f280168154644c` | 0 |
| lib/json/json-forwards.h | 9284 | `65b6a2cfc14a969c17ea3d0eb7747023e036bed2009be32b8b3a7f9bc7ad7cf2` | 0 |
| lib/json/json.h | 64162 | `01e10ee0f6cc8593b6508359e6eddb90088d38acdde32e554a9c11aa52757100` | 0 |
| lib/json/jsoncpp.cpp | 105567 | `75830466888ebb5e9337fc89ccf10b57d8043105fa3bc85391df3cb135079b34` | 0 |
| lib/soci/src/backends/postgresql/blob.cpp | 3959 | `8f9b21da8597b4ec0f80058ab1d2998127ff7803e3b0657674ae599ef8a82d67` | 0 |
| lib/soci/src/backends/postgresql/common.cpp | 2596 | `fdb0d28803bd373974da231b968809764cf2e1301be08992fa607c2a23ba327a` | 0 |
| lib/soci/src/backends/postgresql/common.h | 3368 | `ec7bbe787da623ee7ec43f93b1a9532559eb8b15ee2e809be1012708325c6fe2` | 0 |
| lib/soci/src/backends/postgresql/error.cpp | 1806 | `54480b302f0759ac27f34773d3c68c58b696bb7585acd671cd0dd1f371a47405` | 0 |
| lib/soci/src/backends/postgresql/factory.cpp | 1224 | `40a287586f90e22923ce740479bf323ff4d6b728b303d7e7769aa9b00bfea5e6` | 0 |
| lib/soci/src/backends/postgresql/row-id.cpp | 915 | `9ed793a3a151705c78424b4e98e278a777f16f0732a60f2edf6f36fbbd266a0d` | 0 |
| lib/soci/src/backends/postgresql/session.cpp | 3296 | `ce1c07f6cfe2c5708685a926319747095859d9041df4c7561445c53133c69c14` | 0 |
| lib/soci/src/backends/postgresql/soci-postgresql.h | 10919 | `b2c52023a9c0a803d215506126114ed2ea37260b656ebd526333120b035d18be` | 0 |
| lib/soci/src/backends/postgresql/standard-into-type.cpp | 5170 | `dbb47fd8fc23697297f8d80e5a99981aa8b432f6b9c5cca6c87c5ed4ca323d61` | 0 |
| lib/soci/src/backends/postgresql/standard-use-type.cpp | 6230 | `960fe00232137eb543f56a073a2944837cda4399d1b174061155fae81599dd36` | 0 |
| lib/soci/src/backends/postgresql/statement.cpp | 17478 | `5494011396c2caadbc0dcc65ba5110340295a8240a0aee2591109b42fe2680b0` | 0 |
| lib/soci/src/backends/postgresql/vector-into-type.cpp | 6653 | `dd866a9f758904a0f94ae98260fb661167aa164d97460d3b4cafb2339175b87e` | 0 |
| lib/soci/src/backends/postgresql/vector-use-type.cpp | 6984 | `01618b580c8385df0892e7c5676d54b9e42a63326c466cda7d6caf98cb1043bf` | 0 |
| lib/soci/src/backends/sqlite3/blob.cpp | 2204 | `64dfe7fe51ae6b03ede023a4dc343d279da759295c82bbbb0f70c2ee135fdfc8` | 0 |
| lib/soci/src/backends/sqlite3/common.cpp | 1444 | `1b0dc3aeef946687f84ae734f2d14ee682b01fcb3093001395782a5a44f28f27` | 0 |
| lib/soci/src/backends/sqlite3/common.h | 2369 | `9441b5f12096500698da9c823a8df917357954a0ea03187317b4e9800a0631ca` | 0 |
| lib/soci/src/backends/sqlite3/factory.cpp | 980 | `0560ea9227e24b68061456394f24c0cbbf527491cbd0a75c49af339e26d7b1ff` | 0 |
| lib/soci/src/backends/sqlite3/row-id.cpp | 542 | `e99f04e5cf2e9cf157efa33ca6a6b2907bba1e0cd755c02bbfb3444e0db56137` | 0 |
| lib/soci/src/backends/sqlite3/session.cpp | 4250 | `a199749518a9e32e79ac372beec998171016cafbb5253e8688ebd828bb51111f` | 0 |
| lib/soci/src/backends/sqlite3/soci-sqlite3.h | 7524 | `36fbfd570d706eeabe4acee1024c7d81b8711e6d246eda06ad2f754fd0d322b8` | 0 |
| lib/soci/src/backends/sqlite3/standard-into-type.cpp | 4754 | `fbf110c0b8c1ca309a5f22064222d1b05ae0836025744675ac27a7d787e0530a` | 0 |
| lib/soci/src/backends/sqlite3/standard-use-type.cpp | 7246 | `d5fa720a04e20b73fcd4fadf81485fa737f19af4041aeb5610d0985f05180e84` | 0 |
| lib/soci/src/backends/sqlite3/statement.cpp | 11346 | `4b0ac89401ec87e3e10bfeb966143bb3042e23096666b9451654a2a6b150bdf1` | 0 |
| lib/soci/src/backends/sqlite3/vector-into-type.cpp | 5443 | `bca7d9b4fe420a20f39bbb59e6b7b7184e6cba3752bd2aee8df5f83875e4281f` | 0 |
| lib/soci/src/backends/sqlite3/vector-use-type.cpp | 8049 | `07e21c3bfeb8580fd589aff98dd748bb2f4b36f14dc6bdab4ba4b6fcdcd93cd4` | 0 |
| lib/soci/src/core/backend-loader.cpp | 6072 | `d82653f3392484cf58b4174e434213b32a94a85a563ba02817270ebbef89a740` | 0 |
| lib/soci/src/core/backend-loader.h | 1045 | `0f34856d2a00e24d6fd367ed11267922f9cb233b5f38392b6c208755e707335c` | 0 |
| lib/soci/src/core/blob-exchange.h | 1498 | `631424544a3ea0846ce01a967f8a3ffe0ed91a80bf6be0609063f102d05dac01` | 0 |
| lib/soci/src/core/blob.cpp | 946 | `44cb2502fa13d93bff3d3c18c702f43536a4f016a808444b3bac8aacf2d64f6a` | 0 |
| lib/soci/src/core/blob.h | 965 | `714dce4189630a17c91543b46e5e408e3721572fb8b8070df66337a5774ac6f1` | 0 |
| lib/soci/src/core/connection-parameters.cpp | 1651 | `789160d9ab4bd6ff0bc171999a83024679e3ce3821e6ca9a4c34e78c2d739329` | 0 |
| lib/soci/src/core/connection-parameters.h | 2018 | `d040cba7c38dd6d209a06b3058066d591ce725d3dcbf517a31af1af71eba4fa6` | 0 |
| lib/soci/src/core/connection-pool.cpp | 7074 | `08e0126ddc9655a548dbb3ff7ccc3addbdc80d6a91d61a18ddac20debe79fbfb` | 0 |
| lib/soci/src/core/connection-pool.h | 759 | `8b417ceee88d5ac9ba9ee517843ae35eb6730d0e283f4f80a751bcdd97d4392e` | 0 |
| lib/soci/src/core/error.cpp | 368 | `555e6a47364408541db6ac9a213f1ad34f41cd5b719a756786de11b755a69c22` | 0 |
| lib/soci/src/core/error.h | 528 | `99735d98d0d04994ef5462a089a5db25ada0a0aa732d71fa107329b5dc9d3d11` | 0 |
| lib/soci/src/core/exchange-traits.h | 2814 | `59a37e8773ed4f549628abd1b4cd5f8e5a4c554839c66ec1ac419749f206fd72` | 0 |
| lib/soci/src/core/into-type.cpp | 2013 | `26b994ec59a5db6b12a883e95436bd154166a3ce8bf65e97b625edd851e9085d` | 0 |
| lib/soci/src/core/into-type.h | 4302 | `b1fd9ffe3f857214d8dfca22fef16491bf30ce7cfe445c32be3593518180459b` | 0 |
| lib/soci/src/core/into.h | 1403 | `866f4cfcd25b417a31d937a9d65ee60397d3a55a48588b5bd6d9d95abe23c9e7` | 0 |
| lib/soci/src/core/once-temp-type.cpp | 1129 | `8d80983fb47cbbf0457d6e97b40c0f1376266d5cffd270e0e4cf46146a31e895` | 0 |
| lib/soci/src/core/once-temp-type.h | 2049 | `88c3dcf5b7921a6fc1949f164f5a8f4e51d95d013448c4cf4afdb14cff50a55a` | 0 |
| lib/soci/src/core/prepare-temp-type.cpp | 1151 | `de1a30dc86739d5525b59c43661e019c77e015e34b4761be91529985dc822ec0` | 0 |
| lib/soci/src/core/prepare-temp-type.h | 1125 | `083eff9b1baf80bdd9827790730ac857bd864d748cba28bc35f0c1ca4edc0792` | 0 |
| lib/soci/src/core/procedure.cpp | 838 | `f31da56f59d67629d44da899063f1b0f411b7b41bd3757ffd3ac08c9c88cf74e` | 0 |
| lib/soci/src/core/procedure.h | 1733 | `e80883e3df19dc18b37bab8570fa046f2835d44d2d236f4b35acc8b1ea54c6cb` | 0 |
| lib/soci/src/core/query_transformation.h | 1362 | `78b1e15861ebf660d0a7ba6dcdfcb52922df03252733d6edc7db11545a938c10` | 0 |
| lib/soci/src/core/ref-counted-prepare-info.cpp | 1025 | `0437a674c8f6987bb75ada63960c85d61c69f7506fc1c6c04c5ef94146b80e97` | 0 |
| lib/soci/src/core/ref-counted-prepare-info.h | 1218 | `abc081d40f837e018be2ff15bbfcd729d24167161eb4baf87d96f06656681595` | 0 |
| lib/soci/src/core/ref-counted-statement.cpp | 931 | `e1e634aa2159e07691adc32146ad46e1a2d5c7d3aaa6da2940e856b0523d5bf1` | 0 |
| lib/soci/src/core/ref-counted-statement.h | 2021 | `b1276bcf73f092c45e7c8a685cc2bfd5e134e655acecd46de51358848c04fbe1` | 0 |
| lib/soci/src/core/row-exchange.h | 1602 | `e188be082183433836b7a35855e68620e33a85149b05ab820462e1fc6ee871e8` | 0 |
| lib/soci/src/core/row.cpp | 2447 | `dcab91fd9f4f0279a1efc5f0318fcec4217499b09b0d61fe6466c6c8f3e9298d` | 0 |
| lib/soci/src/core/row.h | 3395 | `c5f3cf3e96c5c5b830f9ba32f1e8a04962db8346718af879ee074b4eca51441c` | 0 |
| lib/soci/src/core/rowid-exchange.h | 1571 | `8e736d566c30e3b602f1d8851f165c825265bbc99d8ad46694d22d6dadc123e9` | 0 |
| lib/soci/src/core/rowid.cpp | 447 | `bec1434cf70878412cd06aface327ad62c5c5fcf4ce77134bbd0797d5466c35c` | 0 |
| lib/soci/src/core/rowid.h | 651 | `84fa414e71939ba225a9c326cb289995b3523b6f675553136f0a48089623d4df` | 0 |
| lib/soci/src/core/rowset.h | 4492 | `3a50b1432e7510b078df2e2744d891f76fe08c170971beb08116e239490b9b29` | 0 |
| lib/soci/src/core/session.cpp | 9417 | `255163f67f12d401acb0c4973644d9a3227100703d6431a059238800dbd244ca` | 0 |
| lib/soci/src/core/session.h | 4354 | `88caeece307128900d704cf2aca3439aabc8bd5c0c3e3cd509efc5842c51aae1` | 0 |
| lib/soci/src/core/soci-backend.h | 7043 | `bf9ec7af67c366b7f857ddd876a0f85c9d8ea59d1a60a84035b5bbfb2b06d0eb` | 0 |
| lib/soci/src/core/soci-config.h | 855 | `afdf34d130a1da5eff25d9aef021a10aec5d072b9045497ff1e07c94150a7727` | 0 |
| lib/soci/src/core/soci-platform.h | 1388 | `b2270c3290a815e0f26abc4c81b1f4f1f3cd87b88658580a65aaaf050e16e228` | 0 |
| lib/soci/src/core/soci-simple.cpp | 54300 | `4bcf983a41292a3c4f2ec8f6e053329471ef1e0b52a70ce98349f8315148fb88` | 0 |
| lib/soci/src/core/soci-simple.h | 6347 | `5f39733a21176cee1e30be94a36080cbe8f8d4d0ec480b795ef7aa4600156c10` | 0 |
| lib/soci/src/core/soci.h | 1210 | `c8495539ab0627892400e3dff8763e579de92e4fc6abee5d00166987ed6f8f64` | 0 |
| lib/soci/src/core/soci_backends_config.h | 359 | `2c9e00fe6d93d62b7e0b157dfaf14a819cd1e5df94222faaf14830c592af50ff` | 0 |
| lib/soci/src/core/statement.cpp | 18480 | `2304e8134ce578efc533029906eaf55d29826b5b8e19d86c3624a140a3ea399e` | 0 |
| lib/soci/src/core/statement.h | 6999 | `37a7bbbb41de18a861bc09a0f42acffe7b28c2b11fe910ab98beb381b587750f` | 0 |
| lib/soci/src/core/transaction.cpp | 910 | `68151e8276094eaee4fe52cb64ae09fb6d9d90d50293c4925c9dc1fddd6c96bb` | 0 |
| lib/soci/src/core/transaction.h | 715 | `581f71a37fbafd08b9bb14728eccc35895368eaaeca05febc54398c581d3cb97` | 0 |
| lib/soci/src/core/type-conversion-traits.h | 991 | `297aa10f19e93e1f0fa7c04ef2625c72c74a241d83b10717b2bbed8e076012d4` | 0 |
| lib/soci/src/core/type-conversion.h | 10310 | `6db4deb4e2be6cbce3bf19363237c85398ddc0c7692bde2b5ac0137c01e385c2` | 0 |
| lib/soci/src/core/type-holder.h | 1221 | `d58a8dd1e7fed82b0467b8f5782f30a1531bffef08acd6a4846355f5e4b2c4a2` | 0 |
| lib/soci/src/core/type-ptr.h | 621 | `1acb336b67a607a46840c800c54427b8c505b64a39ca6db3bbdd7fdb4fe86bd5` | 0 |
| lib/soci/src/core/unsigned-types.h | 2842 | `afcf52fa385f4b1a8ac619a7a00c9406ca2a2201573ac6a1bc2cc3c2f42ac5c9` | 0 |
| lib/soci/src/core/use-type.cpp | 2323 | `376c8e503514ac8d5926ea576841dcf045ae33f4770100b24867397b0b89e2e2` | 0 |
| lib/soci/src/core/use-type.h | 6739 | `34e7d375cc95539be7dcf05a793781d6aeb5fff098c25f88343ed48a5b0b4288` | 0 |
| lib/soci/src/core/use.h | 2478 | `92082473406f14ec381e326217652292c4237f041041f6b2762bd8d31197e39f` | 0 |
| lib/soci/src/core/values-exchange.h | 2455 | `e15beb4960bf069ab188d36136b515798d1f65868427e4b4eee80961476a2deb` | 0 |
| lib/soci/src/core/values.cpp | 1433 | `4709da968fa430672c8c319862d21d47567a2cbadce93181dd51fa58e7aa92d1` | 0 |
| lib/soci/src/core/values.h | 9385 | `fab4eee2e00d20072b35a9ffb6a34e3260f66902a4a7a18968a119e985776f2a` | 0 |
| lib/soci/src/core/version.h | 976 | `a5474fd3e6e582d41b10107c007485905b290a8ada1812bba38a704d95124b08` | 0 |
| lib/spdlog.cpp | 639 | `d05f7c3eb80f5d785375a857f32c857e8bd43b7ec9d37604d68d05e463661bb4` | 0 |
| lib/sqlite/carray.c | 16591 | `a9a443981b89534f90f887b0e84ad8850544707bd649c3115b01de4051ca5ccb` | 0 |
| lib/sqlite/shell.c | 910851 | `664beca40ec99a176abd1a6e88cf48fb45bb2c0b79e4368016b326a6171aebbc` | 0 |
| lib/sqlite/sqlite3.c | 9018111 | `1a206854aa9fe0ccc1b609f5cfce67eb52ac0a8f5aa2f5e853f7c3ed84c710ab` | 1 |
| lib/sqlite/sqlite3.h | 640658 | `41e066ccd4f89e938f136ceb48c996c54dc381b59fe566dea48864c3750b779e` | 0 |
| lib/sqlite/sqlite3ext.h | 38149 | `b184dd1586d935133d37ad76fa353faf0a1021ff2fdedeedcc3498fff74bbb94` | 0 |
| lib/util/basen.h | 9233 | `a883039eedacaa32da7c830abb82495fe52a3ae0e4c5e81d1eee4d06809a6926` | 0 |
| lib/util/cbitset.c | 12495 | `a05e52b7e9fa72138bab849a61b36a418ad1ce1c429ca9cac3a826fd49cac145` | 0 |
| lib/util/cbitset.h | 8658 | `5004c67cd840c91c66f4beeb93171972d8f8affcc1a818a15d4ac6802549252f` | 0 |
| lib/util/cbitset_portability.h | 2556 | `408784420d32a64cef374d37fd575c471495dba75d7282bea4b5221e0f884568` | 0 |
| lib/util/cpptoml.h | 96163 | `3e4e1d315fa1229921c7a4297ead08775b5bb1220c18a7eac62db9ca7e79df0d` | 0 |
| lib/util/crc16.cpp | 4517 | `13dac27edfc387dbb8f15ce95960a262bc195b1842e3bf4e85f8f0c9d69f98da` | 0 |
| lib/util/crc16.h | 75 | `2139a0433c3c6942db0788b4420f2b9cce273c33cae0daba72bd9c9444700a03` | 0 |
| lib/util/finally.h | 1980 | `fe1e833b1396f6f586a524ee3de37fd9b36b1049d5043ab38df92d20bd54bd23` | 0 |
| lib/util/getopt.h | 2703 | `9c9d2d0161b7c6ab6ecb753a4a82c0aa7f151525791ea7f0bb5926689aa5501d` | 0 |
| lib/util/getopt_long.c | 14863 | `1e487a28afaaa70006d4715bfab6ec6fc1bc06ad3d3a9013ca1c8478befe4251` | 0 |
| lib/util/siphash.cpp | 1474 | `3a4827bd03a234bb12f8a9ffc80703b36c5c3bf29e9fe35e45497972ff7a777c` | 0 |
| lib/util/siphash.h | 2406 | `01e303ec5fe133666e2edcc570efce481319ecebae143f65a61e046318176b49` | 0 |
| lib/util/stdrandom.h | 10838 | `5b4650d95a5ac3f073d9caf0f9eaa3b77587da181432bc4d0abd21088fd4b6d9` | 0 |
| lib/util/uint128_t.h | 31031 | `af4b500c566f110b834c40619dd5ae24548377c094bc52142d535a5f2de1e9d2` | 0 |
| rust-toolchain.toml | 31 | `696c2536031250a4fa61a1ec4daeba2e8ea2b1c5b725e659e19bf12be076c5f3` | 0 |
| scripts/DiffTracyCSV.py | 5758 | `67327fdd8305e27917eb20d66746b02663cdd86b225d203705cf0565620d000b` | 0 |
| scripts/HistogramGenerator.py | 10194 | `dcbfb684ff3faf3379e47052085ded61140eb0158818cbc6c1181e0d6268c516` | 0 |
| scripts/OverlaySurvey.py | 26401 | `29a7059085c144530139e716e10b4fe25d82fc59512c3a99b5aba0ba14e4c0dc` | 0 |
| scripts/ParseDump.py | 1588 | `139c2d5adbca86b9042190fa885bfad8d130f49c7cfc61c9e5068b50a16b72b6` | 0 |
| scripts/apply_load/aws/apply_load_aws.py | 30929 | `93c93c0e5dd786ea0642c2d8909691b24636c35c34fe353014d3a5a14cc55751` | 0 |
| scripts/apply_load/token/Cargo.lock | 45550 | `f4687bc8cd94389330f7b079b5f2e02a56c6619751538de3862c3ab9798f7e99` | 0 |
| scripts/apply_load/token/Cargo.toml | 538 | `7c55fe2576365b66fa54262de1a4a694284a75bb72303e8a5742c73427311f28` | 0 |
| scripts/apply_load/token/contracts/token/Cargo.toml | 504 | `8ed308de5105452f16636ed4a490fce3f945bf478dd7e9650f7c4ac1d81810be` | 0 |
| scripts/apply_load/token/contracts/token/src/contract.rs | 2475 | `f4a52476f56e14fd4fe774cbd4431701ffa4d69263f1934354065add0fe16926` | 0 |
| scripts/apply_load/token/contracts/token/src/lib.rs | 57 | `d8228987f3e43e9d4b5a178f3c7fd18e0b720a63e37a801ef7050b9a1f1bf4f2` | 0 |
| scripts/frozen_keys_base64_to_hex.py | 4926 | `887edf2327fb6a4226e0d5c0cf07b7298ebb9d8ea1f704a857244d289f82b7cf` | 0 |
| scripts/overlay_survey/simulation.py | 11914 | `4f65a2077c6ff05c5013006c58cd59aa7172c73c21f29b99b908bb3fa46f6eff` | 0 |
| scripts/overlay_survey/util.py | 1744 | `a1f903da25aace92e6a6739f22d657611d8c346c21b45a64e0c943ca8b99219d` | 0 |
| scripts/pyproject.toml | 358 | `236e2945890f20cb3b19bfb5a47a4e72f58d2c873e103eed3d9d74b292904131` | 0 |
| scripts/run_apply_load_matrix.py | 20065 | `7836f6adcd7f9c5ede17c39135dbbecc8313ef070ea7f328b44ef7d02f524c02` | 0 |
| scripts/run_test_timing_analysis.py | 5744 | `278abfc992b30ffce0387511f3b048111766e07b5185222998266d9de4669db0` | 0 |
| src/bucket/BucketApplicator.cpp | 9610 | `481a4a3a0b4ab077dc7e91b3712da28bd3c700710e9a109a9ae99279fd9a9a47` | 0 |
| src/bucket/BucketApplicator.h | 2856 | `6491331309bafb90799192ec1d75ac47f7d51ae46433d4cf36a07215644e85a2` | 0 |
| src/bucket/BucketBase.cpp | 15332 | `05812298d3f701227e9d8ab391586fa720f42ee625f8bdf9755735a1e1e5a501` | 0 |
| src/bucket/BucketBase.h | 8088 | `130764c5021b68929d2fdd35af08863c6d47b6711a26de7172401ac22cd166a1` | 0 |
| src/bucket/BucketIndexUtils.cpp | 3545 | `6fd00e38dbb193d0a0b82b268e9aa05618491deee9e25f4629d9d96e16fc524a` | 0 |
| src/bucket/BucketIndexUtils.h | 3643 | `446c3bf3ee254bebf6bb66733595ebc06cb079528cde4da83eb003eeb0924596` | 0 |
| src/bucket/BucketInputIterator.cpp | 4737 | `3af816531cf5b34aa5874a5379d7b300fdcb8556cfc6e654a503faa23f311d3d` | 0 |
| src/bucket/BucketInputIterator.h | 1909 | `6e3b2adc84f3491db9cf32479b86536d0512d33c4cea9684ccebb6e6aa68e960` | 0 |
| src/bucket/BucketListBase.cpp | 29788 | `bf8deda2d2deaaa3e8c81b314c7aca0200568215e0f921f4a2444baf2f5b252b` | 0 |
| src/bucket/BucketListBase.h | 26809 | `0d98d4a8a36d6a2e0b65fee3d163c5c3c19a554c389897816a68e9923a5af720` | 0 |
| src/bucket/BucketListSnapshot.cpp | 36201 | `a3d025ca6ce50b3d5bd2b9b160d0537a5abc23eec15c4e3b74e010bbe04280e5` | 0 |
| src/bucket/BucketListSnapshot.h | 11345 | `76c8331eb4dd03e32edee966f4e10cc911893114617565ded02bf50fac4025db` | 0 |
| src/bucket/BucketManager.cpp | 63975 | `fa4d8f927a08b60174eb4f55d791ec32a32c7d95191cb48d0c988e876de0c176` | 0 |
| src/bucket/BucketManager.h | 19783 | `3b3ad03b4056f1b8125631ec9b3deef9cf85dcb1be58bbf641ed10b9d3271da5` | 0 |
| src/bucket/BucketMergeAdapter.h | 4295 | `f00bba9f988e6bea149ae291acc99eeda8d8aa44d593c2ad02a891a73143b1a2` | 0 |
| src/bucket/BucketMergeMap.cpp | 4554 | `4a3d460404fcc43e9dfbd91e7db411aea60d6bb9165a18e1f19e5d07fe975451` | 0 |
| src/bucket/BucketMergeMap.h | 2193 | `cd260e8684686625d90805a92415f0bd643aef170e0a3361f5566af0576e96c3` | 0 |
| src/bucket/BucketOutputIterator.cpp | 8486 | `5aca924abe27aa74a7a247bb6dfc6986a557050fd8021c0cf3c3c97056eced2f` | 0 |
| src/bucket/BucketOutputIterator.h | 2136 | `b55b99538a2b40bc618561865a900ebaa7f021a759fc2b9d2e54c5bb8e77534c` | 0 |
| src/bucket/BucketUtils.cpp | 15074 | `c90e6ef6b596b8b0d0ad2e5ef33338f5559b0ffb18009d9a2092974292de2bb2` | 0 |
| src/bucket/BucketUtils.h | 7917 | `cb7a63a00e28bb98a949f7604210c2ba20f192c706e0177856da02ce9462afd2` | 0 |
| src/bucket/DiskIndex.cpp | 13927 | `b19bfb27756861281d63d60b7413496e155afa2d8804d29526243fab666f23b0` | 0 |
| src/bucket/DiskIndex.h | 6124 | `88a880045fe7f927c30eead9c341a45bf25f6a2553df3f55222d990a82df96cc` | 0 |
| src/bucket/FutureBucket.cpp | 16175 | `0c1dd5bf35e502d495c2da04a0704d5355bb0ca4b96f4df43f0d850087110051` | 0 |
| src/bucket/FutureBucket.h | 6747 | `f2fd0acfe616d21a2d7ae3c82919973ea3822367cdfec2d18ffea9ab8d820ee0` | 0 |
| src/bucket/HotArchiveBucket.cpp | 4432 | `bd3a453fb14d269c3a3caecb4b08e6c31d9dacbf2e0d7a3468bf78b65e63b89a` | 0 |
| src/bucket/HotArchiveBucket.h | 3378 | `0909e74b9c8fbdf0db932578bcab9fe0e175734172374af1df59369ee08c19a8` | 0 |
| src/bucket/HotArchiveBucketIndex.cpp | 2224 | `011226a58c4adddeca2505f0fb90e448b1aaf858641ce6d142b796bf8dd964f0` | 0 |
| src/bucket/HotArchiveBucketIndex.h | 3268 | `9190f383d339905984e9239a23d6fc71925562936788681071cdaf0419f5058d` | 0 |
| src/bucket/HotArchiveBucketList.cpp | 905 | `7356c86c4eb57593c31c39385045a71458eb4d4e6af73f6a1a3f76e2169d79d8` | 0 |
| src/bucket/HotArchiveBucketList.h | 872 | `5afd86b44ecf44b9a7bf4b72e456781dc1e244f1e99cd88ce12ebe5e24799244` | 0 |
| src/bucket/InMemoryIndex.cpp | 5959 | `34cd3bd15d210197a15479499cb4ff8cbdf5786f2b1794bdd6b30acc59d6dc88` | 0 |
| src/bucket/InMemoryIndex.h | 5780 | `4e27965e82a657d7348644471cf855084b20afdc71e3328c6ab4b0f5749b7bd8` | 0 |
| src/bucket/LedgerCmp.h | 8450 | `72a0db688b8a56a4d34faf51d66c6e2770cd5d9ee73c9f544fa4d3252d72e293` | 0 |
| src/bucket/LiveBucket.cpp | 23863 | `66e48b55c4cb5128b2d788d5da0f80effbae0af6675667240a15700d3ce8e6b4` | 0 |
| src/bucket/LiveBucket.h | 8539 | `860d37ccf2c38ab8e89e7836a255682e3aca632dd7b398bd1db1db4fe234bf88` | 0 |
| src/bucket/LiveBucketIndex.cpp | 10662 | `6c743331fc0d534047661be48c0a5ec82abaa66a8d5a7da89c0da266fdebc66f` | 0 |
| src/bucket/LiveBucketIndex.h | 5630 | `676bb492562e547a06e1bdce58e9060a3d10a12ceb8a00b0b43383e1a79b5c24` | 0 |
| src/bucket/LiveBucketList.cpp | 6237 | `933fedfca147048f04c658442067351bb8d5c133e2774d1404a6a02cb60d4ed5` | 0 |
| src/bucket/LiveBucketList.h | 3113 | `3c98a9d8cac8ac5263a35258f0130a7c61744f08e8616f9b2232e143d8fb4240` | 0 |
| src/bucket/MergeKey.cpp | 2000 | `acb82c94678250b7f53f928bf524464c20da813a9192032ae5d56ae4e11e92b0` | 0 |
| src/bucket/MergeKey.h | 1273 | `58e5ab87a696dc44150b0b3a153594f1c21b40f191b57a76dcdf78b60acd6342` | 0 |
| src/catchup/ApplyBucketsWork.cpp | 10148 | `15512229acc5ce8ffb034ce28eb03f54dcdb84c05093129b1f032942e353f597` | 0 |
| src/catchup/ApplyBucketsWork.h | 2144 | `5d4a43977a29d6017a7790a3c3cbbd6edab7a98fc89fdfea806ae0705322c679` | 0 |
| src/catchup/ApplyBufferedLedgersWork.cpp | 3051 | `ef7be8c4a30bd6d019d2fc2f1899b6be940fc91f90cd556eb83b4cd044ce8626` | 0 |
| src/catchup/ApplyBufferedLedgersWork.h | 705 | `2ff55ee75ce0cea4ac8c519e171af018b35eeb770f552a9fde10356a564bfcbd` | 0 |
| src/catchup/ApplyCheckpointWork.cpp | 18008 | `aabe6a81cd70ef0b34555b2b401263f6069ccbe3296c2407a4b49e491e9ecadb` | 0 |
| src/catchup/ApplyCheckpointWork.h | 3101 | `342e5930eb96ffcc33581a6e55eb52147ed7d3a0593b845cb50f078787db1d1f` | 0 |
| src/catchup/ApplyLedgerWork.cpp | 1143 | `030b316582f616fef9499b9d1791f9ebbf5ddb54ab8ba5f1d1dea81b0c1020ef` | 0 |
| src/catchup/ApplyLedgerWork.h | 618 | `715613b8ae55c9846a322dfdf67371f8e238963c4afc81f605a09fd0192fcdf4` | 0 |
| src/catchup/AssumeStateWork.cpp | 4581 | `5fe5b2611a856b7a9773ece786d5f04781e4bcdf7af1441760868c2507542530` | 0 |
| src/catchup/AssumeStateWork.h | 1012 | `1c2ad8ebb2ec1a04a6e2a091bbf1ac1cd74e76f86aeaceaf6c68223f591780a9` | 0 |
| src/catchup/CatchupConfiguration.cpp | 1808 | `b2771fc0404edfc90720b558c3cb339e2fdd431a88c8b58766d02fd7ca13b4d3` | 0 |
| src/catchup/CatchupConfiguration.h | 3314 | `13bb6aaeb1b2dec5a4f46de87b3586377c402c9e81988349411efd390a1b3b37` | 0 |
| src/catchup/CatchupRange.cpp | 4930 | `fd70bd36aa8145565c549d6395a6f66a780834095f4e0d8035c732c68a2ddb1b` | 0 |
| src/catchup/CatchupRange.h | 4859 | `4985e5ee93d0e2622e7f89c2575124a8b3c1f5483d300e762fe70253bbdc4e75` | 0 |
| src/catchup/CatchupWork.cpp | 22436 | `1a9e74cabe68b4e98fec09c6ef788f7bc6af6f9929f7e764ee1e58f2156b2ef4` | 0 |
| src/catchup/CatchupWork.h | 4675 | `56e155ca7f355a5c783d94e237937f5d0a6f8f026438879a06861cb6764d03bf` | 0 |
| src/catchup/DownloadApplyTxsWork.cpp | 10079 | `d42f60e87e8a25e8c7110a2a13519dc549e71711b06fa76ec64bb2214c30c832` | 0 |
| src/catchup/DownloadApplyTxsWork.h | 1337 | `e0c7c5a09211b55b43c4ccbfb52ed237e4231b90f7fed3787e27ea64f8c5472b` | 0 |
| src/catchup/IndexBucketsWork.cpp | 5581 | `55c1a5dcd3f78f9c0607658998e5557e2f746e9d6cc9f65081e6b185f9da004e` | 0 |
| src/catchup/IndexBucketsWork.h | 1214 | `6c9a2802513e1e6110dbbc6ac63fdaacbd12338ca958fd9a5b5c77607ecd6851` | 0 |
| src/catchup/LedgerApplyManager.h | 5040 | `a57616d03f56c96c1107ecc6881f5602e6af1bce5251ee69f74099350ff805f3` | 0 |
| src/catchup/LedgerApplyManagerImpl.cpp | 20890 | `d968fe7277898b22853efa3dd07dd5ec7b9b307b0d357eba7391f2800496c2f8` | 0 |
| src/catchup/LedgerApplyManagerImpl.h | 4736 | `1769c9cf4adb0d1febf3c4101e77350aac659f7c8c74b9aaec45f1ca5ad1acc8` | 0 |
| src/catchup/ReplayDebugMetaWork.cpp | 8193 | `65d33e79b2a34e1442525cc3ab2766f8d36564f7956d13dfecf7ab892e0f05c0` | 0 |
| src/catchup/ReplayDebugMetaWork.h | 1177 | `258e2338c6acc0d923ccf97fc9a20cf52cd04f7635bd358034cf2684832c93d3` | 0 |
| src/catchup/VerifyLedgerChainWork.cpp | 22528 | `6a777f31166d3371a58b8888581335cbd466f7aa4b743023605c3e49cd112f67` | 0 |
| src/catchup/VerifyLedgerChainWork.h | 4554 | `666c622783f78cfda0ae11f15bf1f4eb1b91675849ee5d01fa3ac76971dc9ce7` | 0 |
| src/crypto/BLAKE2.cpp | 1750 | `57503909c7d643fdc64b4536738d074f79c4649e332cf1f9a93875c9afc90c72` | 0 |
| src/crypto/BLAKE2.h | 1397 | `6e6c7729d98a3e64c2ea0449d82040cbf35e3a9473be5174a064b489be8c10e9` | 0 |
| src/crypto/ByteSlice.h | 1973 | `0a5a3583540573cdd96f7dab3ef4689fcd3feba4f56ebc9360b6963a0cd6436e` | 0 |
| src/crypto/CryptoError.h | 461 | `279e40e90b32f9c7d8c3fd48b2184a234e4fa92acfa0f0aa1f59b06890c7a66c` | 0 |
| src/crypto/Curve25519.cpp | 3179 | `7353d38b2414c32bebc6ae7ebbf53ab38418807589c35d61b1d91ee341e4865d` | 0 |
| src/crypto/Curve25519.h | 3043 | `fc9d09d5d03b1ae89e932d6780905923d8abef78634d5e6186c3eb244b4bf4b8` | 0 |
| src/crypto/Hex.cpp | 1727 | `ee9b4b907b0d7c938ac61e5e65866aa57d870fa9881b825d72fb32e473e63282` | 0 |
| src/crypto/Hex.h | 738 | `f0e4cf15fbc2aea283faa5ffc74fea830bc6665ba5e0503d12c5f77ae452fde3` | 0 |
| src/crypto/KeyUtils.cpp | 883 | `318fffbdd3dadc4ceda5f393c085c0d8500b171bbbaa4267f13ba1bfd7b743a8` | 0 |
| src/crypto/KeyUtils.h | 3624 | `2b38a0225f63c9b6f61e29212102288e993a762a5ab632dde4c8825b815af897` | 0 |
| src/crypto/Random.cpp | 1334 | `bb5a580d12852e5ddad2b02dbc266696874cc22f487d9e14b221d3c699bc2610` | 0 |
| src/crypto/Random.h | 423 | `e5fcbd78fc8c3b2e29cdedb4f820c3a9001ea1a3d13becde746527b8e5ad30d6` | 0 |
| src/crypto/SHA.cpp | 2866 | `32f7c7aca940cf210fd34e4e1427085ce08ec22f0074863465bc1035866bf977` | 0 |
| src/crypto/SHA.h | 2172 | `14ab25a80d578323f696e0d1aea787b6ce36e23714d6268cc3b07ae8749e083c` | 0 |
| src/crypto/SecretKey.cpp | 17403 | `d372db8119b4b24b167c5dc6f18b7f45b42f2ebbbd214b78330b4190daeaf53e` | 0 |
| src/crypto/SecretKey.h | 5366 | `f482c40875d15be5f973fb738663c065d525597d528649b71bb39f0a6d1c3f3b` | 0 |
| src/crypto/ShortHash.cpp | 2671 | `a7270ffeabe30ce69ba9bf934f0e8df7be40841400398278aaf36d45073bba9c` | 0 |
| src/crypto/ShortHash.h | 1918 | `895352705f9e57cbf5d5912bafc87fa4b34304c2b7f6eff7d86d1bc2dccb7d99` | 0 |
| src/crypto/SignerKey.cpp | 4351 | `2cb5eec31484826ed183489b480bb8aae26097be39c914876f386013e6c6f82d` | 0 |
| src/crypto/SignerKey.h | 1058 | `4ea2c2a22f99565a8d5f8561d54e4215a52a3a4b4ecba3a9639db065d427ed0f` | 0 |
| src/crypto/SignerKeyUtils.cpp | 1207 | `14dde9e734162d1b497a1113fee08beec64bde7611c3c58ee41e0d44ac00b8bd` | 0 |
| src/crypto/SignerKeyUtils.h | 684 | `f66b7a49076c8835d0e67e4a4d8ececa5c388c66da7df24553f42975915ee2f5` | 0 |
| src/crypto/StrKey.cpp | 1951 | `122d4fbcf88cffe3b37e0e5633192d9e3d6b7e24fb3c23a52fd2a193439b7579` | 0 |
| src/crypto/StrKey.h | 1205 | `7f57bb5d71d02620146b991b56b92261316f27c0c030312160826368b735486a` | 0 |
| src/crypto/XDRHasher.h | 2909 | `44d7732fad3a96727597a4264a1c8bd3cea805232584243d8beb6d75df04f5aa` | 0 |
| src/database/Database.cpp | 22773 | `4e6609bad08791fd98cd2f4777bb0f123d455de56660845f34c73f6cb2ff828f` | 0 |
| src/database/Database.h | 9429 | `4d08b1263b72ae4ad8907423c8e29f3a58429e03906798d3d8187608c212b697` | 0 |
| src/database/DatabaseConnectionString.cpp | 1193 | `6fef74cbd286e5a731a1c339b60edc956ecda0b8704005184bca318c7f775ce4` | 0 |
| src/database/DatabaseConnectionString.h | 359 | `4d49b9fc2fbe41b1f3849038a2ec5d5d131f07aca5803f109a8b1f078f66f5f2` | 0 |
| src/database/DatabaseTypeSpecificOperation.h | 801 | `81a56a5d11418b144ff912f57d35ccd620e9d7516b1462095564412ebbf3f7c1` | 0 |
| src/database/DatabaseUtils.cpp | 1139 | `06dd6e97e749afe94f8e040bbb9fc7ca347c3e2834ec792a4410790970504664` | 0 |
| src/database/DatabaseUtils.h | 520 | `4f0200bd05ed83e710f6a6322d1c42c13e66707e083e723f71be35c2487999ca` | 0 |
| src/herder/FilteredEntries.h | 390 | `bc60098dc7227dd2e460dcb4765cb419092423649531da4561f8488d5475a4b3` | 0 |
| src/herder/Herder.cpp | 1156 | `f7bfff996107f218919257b77101880846e9891b4cf02df5a76921c6db11ea54` | 0 |
| src/herder/Herder.h | 10144 | `da295dfa9de1ddb91b93caa0834b773e95dc95a914ff763bb233b52febea6df0` | 0 |
| src/herder/HerderImpl.cpp | 102717 | `d18bbfc92c909588436e15bfef8823139e36564bd2e434af7b0bafeca87ea7b6` | 0 |
| src/herder/HerderImpl.h | 13954 | `c61462b27ce5a1716c9280b572133b91dd223942aae4219396f6612a670de5b0` | 0 |
| src/herder/HerderPersistence.h | 1617 | `0af40ca7cf727684420f086ac4fef5b7192599f50b024dfb3fe21d05d91c79b6` | 0 |
| src/herder/HerderPersistenceImpl.cpp | 12913 | `27dd834915b4d8382bd3c1d3b48149e85451697d6ba1b699133f6cc73684cc20` | 0 |
| src/herder/HerderPersistenceImpl.h | 650 | `92e0188ac721fcb953e562ccd66b5229562179990906b4352737b5d4c113d4f3` | 0 |
| src/herder/HerderSCPDriver.cpp | 66630 | `660dc960b9e1540fa124f98a050f39a0becf9dc0a121f6baec0449d8a71cd6f1` | 0 |
| src/herder/HerderSCPDriver.h | 14029 | `24efe5330fb9e59ef1b8a83fab2b91f6f773207afba4a65e18309e14a04361c4` | 0 |
| src/herder/HerderUtils.cpp | 4765 | `319a4db1d2bab968aa9d339647ee5f1f2a46994c82ba3c122a73f960b54e7f4b` | 0 |
| src/herder/HerderUtils.h | 1693 | `0f6b9e3dac6fb20e77627fb6152e14acb75a5778e62410f7732d255a0bd10682` | 0 |
| src/herder/LedgerCloseData.cpp | 3158 | `569049700abddc28ab6fce0b7cc84118b3ade1ffc9d11af034837015273a6c66` | 0 |
| src/herder/LedgerCloseData.h | 2943 | `80d86dfd66c60d31cdb9ca5398209481c9e6caa681096a8da2c6a9662240fb1c` | 0 |
| src/herder/ParallelTxSetBuilder.cpp | 31166 | `37c027f184a5a52f29d9d5b3c6ade496e1304471dd91961763e311cd7bc22428` | 0 |
| src/herder/ParallelTxSetBuilder.h | 1221 | `0d70ae73aa490b410df973240f183fd331d1af0fc8e19604b220cb8c54945baa` | 0 |
| src/herder/PendingEnvelopes.cpp | 31684 | `7425ca5bfa33e422d39de66e6348f78a80f33a3e3552e2e30eb37dd49c2562b5` | 0 |
| src/herder/PendingEnvelopes.h | 8508 | `b5429b53286944080fa1c242d141c908ac1f0a6544a5228e861dcc672ab157df` | 0 |
| src/herder/QuorumIntersectionChecker.h | 2995 | `964d0ff86c38f2dd37d9f438604c1ae914ef3bae886d9b034f6a5ec5f45df0f5` | 0 |
| src/herder/QuorumIntersectionCheckerImpl.cpp | 30466 | `d98024f25327daaf0fd6e266efe24c57f1c201479ca37ec2832e7f73c1b351b2` | 0 |
| src/herder/QuorumIntersectionCheckerImpl.h | 24100 | `2184c18b8cd689ceb900d84388857edecad2733c534d66212c9a18714d76ef77` | 0 |
| src/herder/QuorumTracker.cpp | 7373 | `6cd75df115cb031cf023a64f32530edbb53879b9adef54e17b00b5ec9e5cf20b` | 0 |
| src/herder/QuorumTracker.h | 3446 | `c0d90adb7707be22073f289d433fa4994c5686a0235d3fed2ecad9870841e616` | 0 |
| src/herder/RustQuorumCheckerAdaptor.cpp | 22373 | `a8ac300ad1bb15d9fa59d8c6c0a5e59bb6f4cf786f6b2a462879d46690bbcc04` | 0 |
| src/herder/RustQuorumCheckerAdaptor.h | 3873 | `77229ccf55b3456ae94431b81fe1b03adf97c529a6d460cad586e288d5473b5b` | 0 |
| src/herder/SurgePricingUtils.cpp | 22361 | `d362cad889f5e239b12b3f8d80a7bf9c1f08a8036c7d1c14d8f254aab3d47491` | 0 |
| src/herder/SurgePricingUtils.h | 12558 | `e7e20040bd935b7d5b9ce0ecaecc96340bec6bee902aaf1ade9e7473a9d0abd0` | 0 |
| src/herder/TransactionQueue.cpp | 49961 | `284492bff77cc6c7a98ef099bf2b85b2ce502342333b9f0e402c3b2550a82590` | 0 |
| src/herder/TransactionQueue.h | 13482 | `00b90e78bd9d8fac09ea981a5f95b5db3d08f65c5bcfc48a65be6b1652b15975` | 0 |
| src/herder/TxQueueLimiter.cpp | 10607 | `04cab446440fba0a9a2ff1911bf0e87dfa5af90b4a85062b46869069d80a0e99` | 0 |
| src/herder/TxQueueLimiter.h | 4240 | `032154891f253f9383956d61581b1a7570293dc622413e28d345495fad140fd6` | 0 |
| src/herder/TxSetFrame.cpp | 83749 | `621b1bc5650541adc37f6a3eeeea0176b0a7248d0d7907288614de3e1e2ca7bf` | 0 |
| src/herder/TxSetFrame.h | 24554 | `aa6c9d53256a370240e5a44fd1b638e4a12535e00a051c12659a274e351cc787` | 0 |
| src/herder/TxSetUtils.cpp | 9211 | `188232be49628efcde756b1b8e37734591a0152364096f539aae1d1aa63829d4` | 0 |
| src/herder/TxSetUtils.h | 2162 | `7cee960b1f468ae36f632a01ec1b7c0ad59df2d9010d377ac3536f29f366abc7` | 0 |
| src/herder/Upgrades.cpp | 54873 | `1d000044c24ae27c7bfa3cf5f9cbe5f79087d5c487e97e5ad83c3bfe4ae11dd3` | 0 |
| src/herder/Upgrades.h | 6746 | `5231fe129b1120e2f65dd9a363c5cd1943f25cd08c084369ae6154224063f86f` | 0 |
| src/history/CheckpointBuilder.cpp | 11880 | `dae9ae5d78239459910450d780c4e1a8a09d3ffe64f44fff785097a62d907402` | 0 |
| src/history/CheckpointBuilder.h | 4135 | `0fe20aeedb241741580f1b1668111e23e3cbe7da53d84983353dc04452a0486c` | 0 |
| src/history/FileTransferInfo.cpp | 1915 | `febcf2b7ced679d992d92d6c7839155d7e06d872f2ec9d4f0bf762ce5b577459` | 0 |
| src/history/FileTransferInfo.h | 3248 | `ae06e7e37551d523304c8a97a1f32ae0a8c4505941887a785e37f9c5c6bb68fc` | 0 |
| src/history/HistoryArchive.cpp | 18892 | `469c67bdcb925851c9993a5c12c7c569844f7eb2b5cdae251d44e1161c46f1d2` | 0 |
| src/history/HistoryArchive.h | 7910 | `63686280a529479c2c783695c229e6df82eae513b1103cc9f91aacea5d2e412f` | 0 |
| src/history/HistoryArchiveManager.cpp | 8543 | `28cb74e04ddfb546e5ab9da128e8258eead7284667f7900c28004d34cd589295` | 0 |
| src/history/HistoryArchiveManager.h | 1937 | `e4495b40bda9556ff4021ca5c01f6f9f9c5f6b16cc0727404c0b4679b78dea28` | 0 |
| src/history/HistoryArchiveReportWork.cpp | 1668 | `337fcac3c87b07ff05fee2453a0e87dae8db1bbd3fbb69ec742fa09a3a0efaf7` | 0 |
| src/history/HistoryArchiveReportWork.h | 788 | `3c0d4418e1465c0434f2425ee979d5631e677d03a7883685a3b945b6239422f3` | 0 |
| src/history/HistoryManager.h | 18887 | `34c9d10a3296cf37194624556340ce799f4c7921ca8b7d6b4fee68c5586f39c6` | 0 |
| src/history/HistoryManagerImpl.cpp | 21529 | `2bf31a6b90725cb65d672b634b0862fb31aff76e1e71dbe3ca52599dfe65a64f` | 0 |
| src/history/HistoryManagerImpl.h | 2575 | `ff94a0fc713e68d055973280bc8c3ac4f930d1e05c0316f3b85d7d9cbe07cb74` | 0 |
| src/history/HistoryUtils.cpp | 1824 | `8fe2daf013d2c4f7882c7ef5fe041d26c4a9597d2e2e4c2a292728e93e10f5ec` | 0 |
| src/history/HistoryUtils.h | 990 | `4988cf9c05783fe517739ffe182e5a988dce44349b0183ba0ae523693d529bc3` | 0 |
| src/history/StateSnapshot.cpp | 5221 | `7044469aa2bc49179897f97209acc948ec37e4c0bc978b267a3787d75ef8a645` | 0 |
| src/history/StateSnapshot.h | 1040 | `42f0ab91126c825981222f52f9bcc7e8c23f0ed18fac82279af576ddf514f324` | 0 |
| src/historywork/BatchDownloadWork.cpp | 2241 | `102c67d01ed350194c627f6c1d249a5b13dca9863ee0b79152124ad76334ba66` | 0 |
| src/historywork/BatchDownloadWork.h | 1069 | `6c76c38f8d460e433b3ee9ad0212576bcce9f67ab11ff665ad78274106ec2a40` | 0 |
| src/historywork/CheckSingleLedgerHeaderWork.cpp | 5937 | `aa13f3d28446820b6a75644e153287b44725c07c2674cf41990096b1a13b3d2a` | 0 |
| src/historywork/CheckSingleLedgerHeaderWork.h | 1413 | `6804a8ed177758e15632db1945a5a9262fddbb7689defbc92e958c2fde4b53ba` | 0 |
| src/historywork/DownloadBucketsWork.cpp | 8845 | `aa031bb4bb9afd22a1c6121d4cb93016761ed2f5ffca80fc9a8f9f92f68001d2` | 0 |
| src/historywork/DownloadBucketsWork.h | 3113 | `d7782a66db9058a0e312523d839cbfeaebe594891f5e3997d8d591e2666bd546` | 0 |
| src/historywork/DownloadVerifyTxResultsWork.cpp | 2429 | `862c9037e1aa2350672b6c1533ba60c73b76da94070c5651124472af428845f6` | 0 |
| src/historywork/DownloadVerifyTxResultsWork.h | 971 | `2e43b7d0d5df43aa08544c2ad0e400bd2d443343ec3310f5fb813f3aa785ccf1` | 0 |
| src/historywork/FetchRecentQsetsWork.cpp | 3282 | `f02d114249eced02d6729c8676e0f5a9e9f45675bf63b898f4a3327a282994f2` | 0 |
| src/historywork/FetchRecentQsetsWork.h | 819 | `38d58b2869167f67432c39a9134a07876b3a2ae777dc420210d914486f527407` | 0 |
| src/historywork/GetAndUnzipRemoteFileWork.cpp | 6461 | `424de2ae7d00a49a3bde3d79315b841f6c80f04c54dfbc644dca756c6cd87ae4` | 0 |
| src/historywork/GetAndUnzipRemoteFileWork.h | 1403 | `e0c8b484b0058300e61fe4e7fb591cd52440e546d80690c17081af31719e61fc` | 0 |
| src/historywork/GetHistoryArchiveStateWork.cpp | 3740 | `e026ebb71dcb742967791063680a8ca5dbf1fb2f03793acfe90503397883af62` | 0 |
| src/historywork/GetHistoryArchiveStateWork.h | 1518 | `b2461803f8273514f08eb30b119e9bffb09056d84cb10f05ec4f9d6206cd9904` | 0 |
| src/historywork/GetRemoteFileWork.cpp | 2612 | `a093c4b1b4f5962f5facb3f2ca4d49d2efaecbc4753585803bb8038b268d3f2d` | 0 |
| src/historywork/GetRemoteFileWork.h | 1325 | `f0d453e41cafe005ea3b5de97a4e05e5055eaed087831ebcfbbf6e68c402d1f3` | 0 |
| src/historywork/GunzipFileWork.cpp | 1098 | `3397da1a4c1803b36242f7afa168be4e55f9ad1216a1230e87826ee57845d413` | 0 |
| src/historywork/GunzipFileWork.h | 717 | `dce2c07310009d416e2a9fa33b0549cd7b4eb018044d3d142d062a18aa4f4294` | 0 |
| src/historywork/GzipFileWork.cpp | 1059 | `0942273016dab102fb3a72865bbad64402a46fc7856904fc96265946fa029076` | 0 |
| src/historywork/GzipFileWork.h | 655 | `329d6ba08d6d25e9d0046790e44c75d8bf1ba8c8b0c7d22c293eea544e0e9287` | 0 |
| src/historywork/MakeRemoteDirWork.cpp | 940 | `b7871133024bab67b02fa6629f9ccae40ebe993900f3d12f80908c71a59d73f6` | 0 |
| src/historywork/MakeRemoteDirWork.h | 667 | `7f702851f05add9067918267d186f124a7c43faf420cc1c0c414360a523c213d` | 0 |
| src/historywork/Progress.cpp | 1265 | `c09c466f6efe9c7f5424096c70acde81aae30d2c317e6454daa192888e7ea17b` | 0 |
| src/historywork/Progress.h | 473 | `949cbdd8b4f5afa1194d19b5e9ae25b740a89e703268f4ee8b0efcfc0dca08fc` | 0 |
| src/historywork/PublishWork.cpp | 1562 | `6d9ebf6c66f90c9ea147974a38c25baeed0732cbb031ea9d97fa685a7bcac2aa` | 0 |
| src/historywork/PublishWork.h | 812 | `150635eb3f22e4f0c8062b7a207f3fdaa810fcfe9d7916f03440876280f93cf5` | 0 |
| src/historywork/PutFilesWork.cpp | 1940 | `ddf0ea1cfa0433109ed66950661c4547d9700a133a78c8d4ba26394eae549688` | 0 |
| src/historywork/PutFilesWork.h | 910 | `52cc58738a7cae85e2d64c07c0adaee61a1a53cbc43c234b5073f64f6c6ebe07` | 0 |
| src/historywork/PutHistoryArchiveStateWork.cpp | 3306 | `23467a1f8ba2213462f0a1f3f1fddc7938c83d0207adfd271a663c7b57136a82` | 0 |
| src/historywork/PutHistoryArchiveStateWork.h | 942 | `d210b76dbb0767792110bfeefb3ec5cc71c935b3125ce8590753e44dde5d506e` | 0 |
| src/historywork/PutRemoteFileWork.cpp | 1020 | `7876b6d0c3e4de27bdd90a54b7d3fa507e8e93bcdb9529f201300196f0891fb3` | 0 |
| src/historywork/PutRemoteFileWork.h | 751 | `1da865431ea96729101ac56c9c0d465fee8ece4641fc1b85e4a18dd0e3863dc9` | 0 |
| src/historywork/PutSnapshotFilesWork.cpp | 4998 | `b19af9fab26a9ac44b48ef932ca9b48f6fc0b3e351b104a81b23129ac4b70531` | 0 |
| src/historywork/PutSnapshotFilesWork.h | 1182 | `6e1f7599103b773581a067c150ee24fda3f675691478236e3abb07123ca4e0c4` | 0 |
| src/historywork/ResolveSnapshotWork.cpp | 1624 | `6b3f8fefa2343b7fb6ee702352ed2127d997a6643da43dcf142a9709703bd078` | 0 |
| src/historywork/ResolveSnapshotWork.h | 670 | `6abf697f3a23ffd47061322f71b69d4e554473dfb8944fce8769cbed5408b39d` | 0 |
| src/historywork/RunCommandWork.cpp | 2040 | `eacb68b9f2e391e38725c415db068cc7fa09f6001a0a4a6c5c1d41ca3a622f13` | 0 |
| src/historywork/RunCommandWork.h | 1074 | `31a819a4a86ac119e3e942faf006fe641eb82f474fbdc7757b16262db440b808` | 0 |
| src/historywork/VerifyBucketWork.cpp | 5305 | `2825de7372280f012064802e429b0bd1bf54c63e96d9e8b5b9b5aa65b04f7646` | 0 |
| src/historywork/VerifyBucketWork.h | 1191 | `59e8be963513961db2ccfbcd89795821dd3acd3464eb2647e4cf09965d6ef954` | 0 |
| src/historywork/VerifyTxResultsWork.cpp | 5621 | `2d0cdc8d8f271e48ed8c16c95b2dd94db5c093298ab0752db0836b880d407f81` | 0 |
| src/historywork/VerifyTxResultsWork.h | 1203 | `719a7748897e4fc77894b2d606e5a1d7e8329edd3bf324c0d8d7b84c96e8691e` | 0 |
| src/historywork/WriteSnapshotWork.cpp | 2434 | `677cedf51878e55449fcb9875798652efb2264ffd9c35527094c787474e8fe50` | 0 |
| src/historywork/WriteSnapshotWork.h | 710 | `382c433eda0528321878661678f6ceae919db88850572acff7a29549a19b18f8` | 0 |
| src/historywork/WriteVerifiedCheckpointHashesWork.cpp | 11205 | `3f95a41690ef79727b833c1a2eb9b43e1bed7a0013c08d64df16e2be03c68fd1` | 0 |
| src/historywork/WriteVerifiedCheckpointHashesWork.h | 3795 | `417b861a6285ec3de2af3209b0259620e9065b93e2575345d051678dacb715a2` | 0 |
| src/invariant/AccountSubEntriesCountIsValid.cpp | 6320 | `179c405c53b87a6a3a4dedb5c02e484584d0ce161d834b9272d8d3316b1372dd` | 0 |
| src/invariant/AccountSubEntriesCountIsValid.h | 1218 | `80144dccf2ac44fa6f6a8d35e0f29eee26b17836a8eb74dd59ea235fc2640f9e` | 0 |
| src/invariant/ArchivedStateConsistency.cpp | 17952 | `2943e45d44fb8d87cfba958bd347756be4930e63fa1d5dfdd78870c46d8fade6` | 0 |
| src/invariant/ArchivedStateConsistency.h | 1711 | `f4ebaeaf38249498fbae9b61499953d1f350dd4bdc3b45c3bcc33e6e8e0cdaa3` | 0 |
| src/invariant/BucketListIsConsistentWithDatabase.cpp | 10115 | `282b015c1a5e0123ba3cc80af9874902e52217549ef336de85252d495f7fae08` | 0 |
| src/invariant/BucketListIsConsistentWithDatabase.h | 2017 | `13628eea4e26bf37859edca31554158b7a9c61c57aa69a44ee2c4916d39df574` | 0 |
| src/invariant/BucketListStateConsistency.cpp | 16471 | `b6e501867f45c6df33b9090240dfbc744f8557d4d8c6e3fa6fa8c104b819abe4` | 0 |
| src/invariant/BucketListStateConsistency.h | 745 | `ee813869be1643c94af6cc13b0ea628257c8ed1e1915cd247ba330a041669a65` | 0 |
| src/invariant/ConservationOfLumens.cpp | 12631 | `3518eb18a271c348a28dcfeac72da9a9848dfe3dbfb9381a24e1b8d466d5ac32` | 0 |
| src/invariant/ConservationOfLumens.h | 1429 | `6a38b93d7d52754c163e982e93b79f3dc6d3a7c87352cc54665241b220e4d537` | 0 |
| src/invariant/ConstantProductInvariant.cpp | 3105 | `45a5edea25583d82b09e338285849d64a5058231dea0212f640994aa35863236` | 0 |
| src/invariant/ConstantProductInvariant.h | 923 | `5a1dcb1a1e4eb4cb7948c14795376e7f1a9cc0abebb33a0c8f7a5bb3d623ea33` | 0 |
| src/invariant/EventsAreConsistentWithEntryDiffs.cpp | 19303 | `d396a8c98164a2e11c7fda49c4433b868701db26038c15248cbc86d75eca2042` | 0 |
| src/invariant/EventsAreConsistentWithEntryDiffs.h | 971 | `b5201d9b9d7ed2187b71a345acc1a41a1ee98f1c1b8b7220d2baf0900aabd04d` | 0 |
| src/invariant/Invariant.h | 2926 | `38736b8990bfbf12e989eff248de7ca8d9069088fe63c0339f02d1ec305ad03f` | 0 |
| src/invariant/InvariantDoesNotHold.h | 505 | `8f4c651309fa8c9adabb6f30492712a55fc927012da1605a7067d6bdcff1415c` | 0 |
| src/invariant/InvariantManager.h | 3672 | `2109e7d909f4ab1a843c4b2e24b3f5c88626c9f9cbc34b5ae56b9a70d7db9787` | 0 |
| src/invariant/InvariantManagerImpl.cpp | 13513 | `6db3255ef027d5893990e0bac3637deb30b2a0c12046fbf4d3bd7e1ee7fc69e3` | 0 |
| src/invariant/InvariantManagerImpl.h | 3626 | `21a46765997ccb96ce9a097b7578cf52dcab3aa6fcd292120674352b260047c5` | 0 |
| src/invariant/LedgerEntryIsValid.cpp | 17372 | `9ed7d1adceeb5b7de5e549d29c29766e66c03c832f5e3804630b934bbacf18b7` | 0 |
| src/invariant/LedgerEntryIsValid.h | 2908 | `61b12e7f1553e58d1d771f0937f2e71251914c5c659622c6579c058dace11991` | 0 |
| src/invariant/LiabilitiesMatchOffers.cpp | 13420 | `c4094d620c47e3665741605ff5f0a8f1930147923e5dc9471f86e0d52e8724d2` | 0 |
| src/invariant/LiabilitiesMatchOffers.h | 1330 | `bf53fafc99e9c92fbae9a584c24b2735804e4886f698682f6290173f4fdfdd32` | 0 |
| src/invariant/OrderBookIsNotCrossed.cpp | 7390 | `66203729e55e720bd4d27aeb51e68c32b792b7fa81a463c11910710dc077378d` | 0 |
| src/invariant/OrderBookIsNotCrossed.h | 2834 | `349e7dc4c04781a10f5eb14775d2d621ebe99006ce6ed9814069cccb0de0bf20` | 0 |
| src/invariant/SponsorshipCountIsValid.cpp | 7906 | `cd0c92654fe64c749686fcf1e56a2e13bc7437876bcf2def5734867025c48535` | 0 |
| src/invariant/SponsorshipCountIsValid.h | 1049 | `fe21467a74b19bf22ecda36ede34fd850b48cef5419f5015ef94a28519b2edf0` | 0 |
| src/ledger/CheckpointRange.cpp | 2317 | `0425514d6440877e6794c9fd0a14d191a739c7c55c14d9209afec95f31d9757e` | 0 |
| src/ledger/CheckpointRange.h | 2436 | `5b14d6fb56c945fd2ed9e6f40a6fce5a933001068ebc5e2d49196ac0bbbee8eb` | 0 |
| src/ledger/FlushAndRotateMetaDebugWork.cpp | 5464 | `65c54307d45f301c65f5c283544f2d9dedede9cb8273f8d4b28d95af22f2f71e` | 0 |
| src/ledger/FlushAndRotateMetaDebugWork.h | 888 | `3d926c0cdfa0d2299df05c14fe184367ecb2afa21f433d2f5d3c5fa422afc83d` | 0 |
| src/ledger/ImmutableLedgerView.cpp | 13070 | `6220ae9fe82212891e8a0d33097c3b3a91fa53e2ef38d190c525ff188004e6a0` | 0 |
| src/ledger/ImmutableLedgerView.h | 15249 | `5815f47c109117c4feca9cb48f6fb2731bb7b963715cf7eaab09ba9f3114dadf` | 0 |
| src/ledger/InMemorySorobanState.cpp | 22296 | `808969ba7f067a192138745cdd9173b308a592cb94a3b61132567e7dc1200bcd` | 0 |
| src/ledger/InMemorySorobanState.h | 16534 | `cd8bc1d3a6924cb41aa53da15d763c8668913373108dd38b4302e34973c19932` | 0 |
| src/ledger/InternalLedgerEntry.cpp | 20384 | `7781de4c218a39d0cef7e51431e6dff8d42f267094e371d7c6a6b4b7a7667ca3` | 0 |
| src/ledger/InternalLedgerEntry.h | 5956 | `bcd29b5a4ebe00eab83f2cea4daad7e872294dd934b7b2e154933c5177478cf9` | 0 |
| src/ledger/LedgerCloseMetaFrame.cpp | 8932 | `af0984e078826d2c8afca5ed8b65811843a3c10db17baa11b5e8f58e85c66c99` | 0 |
| src/ledger/LedgerCloseMetaFrame.h | 1937 | `6dc77bf399524b90fa094e1c53d9758c3278da12ed282788054327ae113ead0a` | 0 |
| src/ledger/LedgerEntryRefs.h | 2247 | `ce5c782bf3b90c56691fa54a1e97d3916064be9a5d7be5a2a498bb484cad7adb` | 0 |
| src/ledger/LedgerEntryScope.cpp | 19694 | `63049ca9b0f3cbc67d09caa4a59d43007b1e37184d5d64afbfc62a60e107f4c1` | 0 |
| src/ledger/LedgerEntryScope.h | 17412 | `f1bc1b6fc7a58b930fecb28534ae9cf52dcfed24a7f55e5a78132fa149a1ca61` | 0 |
| src/ledger/LedgerHashUtils.h | 6672 | `7f72624c874eab3a29a5ee0601fd608e5536f83e69d3c772ba7522523647f133` | 0 |
| src/ledger/LedgerHeaderUtils.cpp | 10859 | `afe92acb9146a8523d67011ff80b92d8a81ae3d5e874f775c69cf4e6268b0508` | 0 |
| src/ledger/LedgerHeaderUtils.h | 6078 | `c00d8a1828401288ba399db1eedd29d8186eed4317df7eb31d60151ca3e53e59` | 0 |
| src/ledger/LedgerManager.h | 22972 | `dd4e18a5b7820a52937b7e4417fff1d5ab72c67d0e8d9a2b9d07642c0bb8bdd9` | 0 |
| src/ledger/LedgerManagerImpl.cpp | 129378 | `49abb918f00d50af58b3b2ab90a6efff6c854c1c8627323d0bf7a8129a0cbdf7` | 0 |
| src/ledger/LedgerManagerImpl.h | 28318 | `e664c9c5bd9e459b452239bdfe8090fd4ad9b7b72b670e3748fa719e25a9caf3` | 0 |
| src/ledger/LedgerRange.cpp | 898 | `152d38c6791e072d8aa806febae6d70141a8f3d83564ec472b5bacf73e0d2a6c` | 0 |
| src/ledger/LedgerRange.h | 1981 | `59593beaf2161540437c18b1e0b673cc04c6d03ba26c3f06f3cd73a1d07c90f5` | 0 |
| src/ledger/LedgerTxn.cpp | 112799 | `8a7f621229a9ef3591dd7cdafe859af58f4a29cd4403b7b97ae7a68b071cfa43` | 0 |
| src/ledger/LedgerTxn.h | 45133 | `fcd2f39ed7ff4e4c2366c888e52cb3a43282753ecaff8e41682e0a81fd46ac3e` | 0 |
| src/ledger/LedgerTxnEntry.cpp | 9059 | `9f09f3bc633f54fca6a68a153f6b6aa4411b6f58a54fd9431cc0abc008ce3e67` | 0 |
| src/ledger/LedgerTxnEntry.h | 2928 | `cbdd290cd55c1317b5665dc359b421e82d972ca9fbe757170e47bcf42fd67c42` | 0 |
| src/ledger/LedgerTxnHeader.cpp | 3216 | `52a9d16342159402f0ff2c1a2863b1d4eb465759adfd4c3d269721cea54cae87` | 0 |
| src/ledger/LedgerTxnHeader.h | 1321 | `e450e9918e7f4dce9ba8ed05a10a519ef5e89d2258cf3ac66cb70fac301fb98a` | 0 |
| src/ledger/LedgerTxnImpl.h | 37262 | `98b23f67490b712d8daa8bb459e137ae7dff9ed24035b5f15786cd3d17bf3ebc` | 0 |
| src/ledger/LedgerTxnOfferSQL.cpp | 29866 | `53d8db5e117754f9ce55c2744b376c01c2452b2618bedccfd1dd67c3ed7e65e2` | 0 |
| src/ledger/LedgerTypeUtils.cpp | 2957 | `44a35263c9798eb3c86e60c74fe20c3a4de78cf9398f7756f1644a6a42ca0af0` | 0 |
| src/ledger/LedgerTypeUtils.h | 2531 | `8ecec2af5bdfe2cc4804bd08bd2e8bef63a7f9920878b29ba3488cc4084634c2` | 0 |
| src/ledger/NetworkConfig.cpp | 109481 | `65f954dbde0b92fe4817e987395a1140c2906ddefd71c5507d3437ae4cbe995f` | 0 |
| src/ledger/NetworkConfig.h | 26271 | `bb6a674d00d0783462d33e8542378ba2e94fbeb0af27763e3f0a6ba42cd44017` | 0 |
| src/ledger/P23HotArchiveBug.cpp | 21188 | `cc637f6f414c3ebaca0afa45d3ab2d2439f3f89691e9e06cc56f7256b74f9c9e` | 0 |
| src/ledger/P23HotArchiveBug.h | 7750 | `1afc619eb125a0cbd2ff516b2d7648388f3fb06e004fc2f3c6ee805e443105a7` | 0 |
| src/ledger/P23HotArchiveBugData.cpp | 673062 | `8d7b3a6fda453c3dcd2e3187123093856f8fc4cdd9a70a873c688663b9832e8c` | 0 |
| src/ledger/SharedModuleCacheCompiler.cpp | 8188 | `f2967555893f2b8514987c3500a724e477cad5940f420dca24ba15f5e397cd21` | 0 |
| src/ledger/SharedModuleCacheCompiler.h | 2465 | `dd651759ab673ac1817ed14658d04ba451046c6a271fa0509f03ce9d425ffcdd` | 0 |
| src/ledger/SorobanMetrics.cpp | 15284 | `1dd8612d4f394cb1cc13958970aa713041565d0f02fd7fdb8f89879564e8675a` | 0 |
| src/ledger/SorobanMetrics.h | 8234 | `d1f0e0c9fbe00e13732486e66d3a7632f4b1b5c091cc6790f8bdfe57a3d8a921` | 0 |
| src/ledger/TrustLineWrapper.cpp | 13725 | `29dcf0ccb97cdfc17a8c8c67535192fcb75c4d10dc815ae559f988d8b8f8f2eb` | 0 |
| src/ledger/TrustLineWrapper.h | 4730 | `d31ef937929d711edcb3ddf2abf9d1b95a145dab2e387445cfb0ccd63f1b9fad` | 0 |
| src/main/AppConnector.cpp | 4647 | `59fe8d3e7972b931832e568f0d2691f52a766bdbc7589e7842e808d236a43c23` | 0 |
| src/main/AppConnector.h | 3597 | `45dd2c79c763e5f51f35911d86551c3276f4db36e32c3eae490e32a1b742e02e` | 0 |
| src/main/Application.cpp | 1651 | `f1a3e3cb2ab494cf9e935985de29f54479f0aaa7ce363f3d487d823f6627a1b2` | 0 |
| src/main/Application.h | 14350 | `002d596352694918c3ca3bddd6b154a5c2cf1685f43c4717d2e4ceff1d3ab433` | 0 |
| src/main/ApplicationImpl.cpp | 52421 | `166203822f8e6bc817324b4c7216defc6eb01524afa2e5a5b0bb0f566a911c9c` | 0 |
| src/main/ApplicationImpl.h | 12007 | `2e1859492eb15816e5f1c06494ab19f24bf115493aaa17273a61ab7a43df3aaf` | 0 |
| src/main/ApplicationUtils.cpp | 36485 | `f99625318aed9989209cd466bb0aae6a1ac62df53344621c12fc0f4b66570d7a` | 0 |
| src/main/ApplicationUtils.h | 3020 | `7743c9823b311739269a91ad35e9d2dc31ee259e23fe964398fc0b1086ad5a3e` | 0 |
| src/main/CommandHandler.cpp | 52222 | `47806ce7e4494ab2b21e264217be76d3539ec042deb15b6c79c58c48d7bd5296` | 0 |
| src/main/CommandHandler.h | 4299 | `434574ce8b5f54194e199566b91ecd22acf538f19077c2164f910f27548eeaed` | 0 |
| src/main/CommandLine.cpp | 70184 | `7e97d04b6e442718b00653b3b2ddd8c7a24e47a0ebb0d6238b631f9b00529b25` | 0 |
| src/main/CommandLine.h | 703 | `3fa181438a8baa3dcbf920887a95cef5902904f69e93f28a191efe3cf398a08e` | 0 |
| src/main/Config.cpp | 106728 | `26cddd9bda0b3d01a41743f84f5648882ded0eab4dec4cf81206ffe77884aa0a` | 0 |
| src/main/Config.h | 44199 | `6dda5fd7ab6a92ae2cb0a548a68f158f0770de9a5355a1b5f96433d33adc893e` | 0 |
| src/main/Diagnostics.cpp | 4501 | `b4f27b91b40a0d872a43dc01962bb3459930a4efd9b9a85c3bb7d63d5528788f` | 0 |
| src/main/Diagnostics.h | 391 | `e72355f33ffd617b37dad7e621ab17c493d1f2ccafaa23dc9475b8fec2a384df` | 0 |
| src/main/ErrorMessages.h | 1342 | `fa75bc023848d4d332b7b9433182abe898ef86e70f6f32941241f67259149358` | 0 |
| src/main/NtpProbe.cpp | 5041 | `53d6e1bebcc3cfc5e4bd76db4fad4e3a6a44ba6813d73f98d19749e31f54f12c` | 0 |
| src/main/NtpProbe.h | 1912 | `f22f766c41217f373e78a5e0f21fb3f07bfb12c71b586b4c90d91f057ec94d67` | 0 |
| src/main/PersistentState.cpp | 12085 | `5d0ac1660afbf872fe094de2212b31187fbe8b946d7759967b30a52232c7caee` | 0 |
| src/main/PersistentState.h | 2918 | `59bfae8d9de828cf812f5adfd8841fea35667a3ec8e91ff953d711c5bef299f6` | 0 |
| src/main/QueryServer.cpp | 13815 | `53a011c1d3f6ed5fd6c80b6a53cef30aa8a3d43113f0a81a3c7b3e7e5006aec4` | 0 |
| src/main/QueryServer.h | 3853 | `af0323de4d2679f0cf8d2a37efdb298f829a0984ea50e0c68345e540e57eeb34` | 0 |
| src/main/SettingsUpgradeUtils.cpp | 9787 | `3852b4f8a0e80232bf021230b8824718f259a9eb9f8e662da87207d252e95bd9` | 0 |
| src/main/SettingsUpgradeUtils.h | 1212 | `e3f200d93b57e71bb2c21ef97d6be3f208dd11179db5b3a9bf7fdc6ecbf16697` | 0 |
| src/main/StellarCoreVersion.h | 305 | `4b8032eff32c84ace1227c973074113d831bf36747fb74dea7558ad0463b5379` | 0 |
| src/main/dumpxdr.cpp | 14063 | `19cfe05332be981b5ac642844510182ddba81c3ae3835570d5d6bbacdbd782fd` | 0 |
| src/main/dumpxdr.h | 869 | `ecc78978adb92c272236acefdd20edc8fdf5e45bbf9c78d428673e138f3648d0` | 0 |
| src/main/main.cpp | 14455 | `d489fb1d4fc38cd7d791eb56e55051b024e2e054737bbea38592184eff8a4735` | 0 |
| src/overlay/BanManager.h | 887 | `9c475d25b959daf92403dc762a48e075013bb85abffdc642ca8ce18100b5af64` | 0 |
| src/overlay/BanManagerImpl.cpp | 3256 | `d1f6360d387c8362009b74549244a5df7b661060887a4ccfc9e639c78e4aeece` | 0 |
| src/overlay/BanManagerImpl.h | 667 | `e731bdce8b44b71d37a99105afbadfca55357acd3f69f08cfe2d633acc7aa318` | 0 |
| src/overlay/Floodgate.cpp | 5658 | `7960f90ae566cbd6c70dcca0c9112ca851a0189df1bb1a40b307a90164b7455a` | 0 |
| src/overlay/Floodgate.h | 2243 | `46d22ec9d26811c694e202e275148d587e9cac9de08f5d808983e1ace47be280` | 0 |
| src/overlay/FlowControl.cpp | 21442 | `e79ab5a7e31e32bf462b55d67d2660a86a71ebc900682a9dfd6fb7dab76b9f5d` | 0 |
| src/overlay/FlowControl.h | 9382 | `9563c0d93b944a2a483bf038de5a8db86621c5b0e28607c8bb5bf58e284e69af` | 0 |
| src/overlay/FlowControlCapacity.cpp | 6226 | `4ff5ed1ccdd9242854bcf81a28af424d25e3cd4c5479f561ca3370684c80544f` | 0 |
| src/overlay/FlowControlCapacity.h | 3995 | `10259b64a680644152fc81a2338ad9357aede2973b001c652babe575b619078a` | 0 |
| src/overlay/Hmac.cpp | 1921 | `c42cb77ab9eeb284d9d9d4000683b543b5d2ec86106bef2c2a11359d208b3248` | 0 |
| src/overlay/Hmac.h | 1210 | `3d5de9c0ff6b0025c2bc78e891c490c4af339ecc489bf171619ac6f80795496f` | 0 |
| src/overlay/ItemFetcher.cpp | 5245 | `c83c3c6d8c28feb3e036bc19b4f0cc41123dcc84d1e3847c668074382b1a7b8e` | 0 |
| src/overlay/ItemFetcher.h | 3543 | `ae92e558fd3d4234401a47639c2eb0b62ca9238075213c9da1e4a2d8384ad9bf` | 0 |
| src/overlay/OverlayManager.h | 9282 | `5d2df7713c167f7533f2a844f6bb1ab3c8234dc3ff5f1d6d2da328e15d77f02d` | 0 |
| src/overlay/OverlayManagerImpl.cpp | 44485 | `17bff807f1d30ca659417203a3c928927d452e7f93e6c348efb237724ef43fab` | 0 |
| src/overlay/OverlayManagerImpl.h | 8039 | `52f96a151268de1ba6c8f9b571e622039845a7c4dee70280496eb96e22e905a5` | 0 |
| src/overlay/OverlayMetrics.cpp | 9402 | `517972c6b0fe9d65bed51c81276173001547595f9fa7295aaca52367d7d5f4be` | 0 |
| src/overlay/OverlayMetrics.h | 4121 | `2dc637d6b037f68d82e17bcb4a34639dbe3fcc0d044736e15bf490065fb9c0f7` | 0 |
| src/overlay/OverlayUtils.cpp | 326 | `4940945b9ea356947c3b9378253cfb2c0df7d67360d445bd1b45a0fc208f72cf` | 0 |
| src/overlay/OverlayUtils.h | 430 | `e3115683d57e81a2941d43e23139596d002a35f2dd411702ac6d597bf5d55ee8` | 0 |
| src/overlay/Peer.cpp | 66516 | `77cbfead871d9608fc5555613e6adad551011c4edf3a3468a1a7db3030a08a15` | 0 |
| src/overlay/Peer.h | 20760 | `a2e653754ec2a1ac9415bf3fd1ef2b6966aa9b4bfe601ffe6ea9351fe0a88c06` | 0 |
| src/overlay/PeerAuth.cpp | 4453 | `48928f0357e88f0845062e21f7891f94f46c7626078846753e661e675bc72644` | 0 |
| src/overlay/PeerAuth.h | 1987 | `e97154ad93411cd49156acde02e90c7e7de7aeb8286e2f926f4527b7d30b0638` | 0 |
| src/overlay/PeerBareAddress.cpp | 4739 | `cafe135570ee8dc30f546ade74a70165cd811d272f5e02878d7b92b5a89a6b38` | 0 |
| src/overlay/PeerBareAddress.h | 1466 | `7409fbbef6f6f17bc4dbaee38112ff413454b283726dbceb73e3d87f1140a7e0` | 0 |
| src/overlay/PeerDoor.cpp | 3050 | `0b905aa48142961addfb7cce36feab26978a0db63c13b6798fdc874047e0b51f` | 0 |
| src/overlay/PeerDoor.h | 949 | `6306a886f530c53d521422dfc1f7d050b38ea1bd4eac29d2789a2cc0f22e6658` | 0 |
| src/overlay/PeerManager.cpp | 17826 | `d4629c603cc72289c6ecb69e243b11157d17e5d9809f1c032d42fef7d3faa7fb` | 0 |
| src/overlay/PeerManager.h | 4541 | `37c39d6437fd3cf04fca499ea226abe2485b9f539321b0c0f6602d68199c28ad` | 0 |
| src/overlay/PeerSharedKeyId.cpp | 783 | `c410662dc7b06b40ea4b2d8bcea1dceb742fd742ad8730224898438c04a6444c` | 0 |
| src/overlay/PeerSharedKeyId.h | 718 | `1391bd18ab7e938f02bdb95b014e4a9c267305d54fd277c6b44ab6e0151a74ec` | 0 |
| src/overlay/RandomPeerSource.cpp | 2077 | `6062ac2af316c638da1d54ef18c38d363dc84041e8b1afba3688f19423a7de01` | 0 |
| src/overlay/RandomPeerSource.h | 897 | `1f07d0e44f76f6eb56ce65eea9e279fad101061d5fd8d305aeb58e878090c0df` | 0 |
| src/overlay/StellarXDR.h | 446 | `5c5328c029ea9c26ed42dd0aaf9fe5d4b2806e0102ee0c70bf5a7a2c00ca87f0` | 0 |
| src/overlay/SurveyDataManager.cpp | 18302 | `39aa0c97bfd0f38141b8d5cdc8ae48347d06f42bf486ad0b1860c2b2eeca53f6` | 0 |
| src/overlay/SurveyDataManager.h | 9204 | `09dd394c1e5cd93d51a2847eda3d0ed112b0834c64f214680047da4c84b2016f` | 0 |
| src/overlay/SurveyManager.cpp | 28517 | `01017327f08e3b436984c5a11c687392e859bc1cb8831c3d8a5388ceb6efda6e` | 0 |
| src/overlay/SurveyManager.h | 6996 | `d67fa171ed18d6adc59e96c09b5d81cb93f3532d0dc599e30f8c3186a9c7c868` | 0 |
| src/overlay/SurveyMessageLimiter.cpp | 5632 | `c9f306f453c64cca72c18c534c69ca1858c3feed195b25c2bec118367a29a9e8` | 0 |
| src/overlay/SurveyMessageLimiter.h | 2636 | `0340f6dbbb1d79ed8a16d60210a84e72775894c59729a74043415aab529a3b6e` | 0 |
| src/overlay/TCPPeer.cpp | 29760 | `76a131562798f77ca8765ea5d1e2196fe61dd045bea2863567863e92318be54d` | 0 |
| src/overlay/TCPPeer.h | 5820 | `4b0f5c2f5fd461006b128d2c6609134098ce579b737cc5fd6273b5d258b4b1df` | 0 |
| src/overlay/Tracker.cpp | 8275 | `f07f7d692a593e644dc8dbfc367f4c7d821eef4d8b3cc4f6e3f9d6392b398960` | 0 |
| src/overlay/Tracker.h | 4371 | `0f7c6b73d6bee72e2694df319879c562a13160c81e9f4b99341d4912279def23` | 0 |
| src/overlay/TxAdverts.cpp | 5341 | `e8b035402efe6ed01d70e70dae52723698c5adcde4811ed86168d3a83d430763` | 0 |
| src/overlay/TxAdverts.h | 2608 | `76d9fd07d437857a939ca3af5f4ee55cb0b19153f437c458eebfdfaabbeb646e` | 0 |
| src/overlay/TxDemandsManager.cpp | 12280 | `0cf3761cadd6a8f897f6a8b8ca2c9c548aea6b7bde482bfcf5a9c5fa9b2fab33` | 0 |
| src/overlay/TxDemandsManager.h | 2374 | `a6427fdc32382924ba348f2d19c8b678ef9e52e90d7ad208ca930ed039164b38` | 0 |
| src/process/PosixSpawnFileActions.cpp | 1710 | `b51860a7ca079af4cb2550d18040e76f5f1de7f9ccd87cbfa879a852eb8cc8bf` | 0 |
| src/process/PosixSpawnFileActions.h | 716 | `25606443d06ea5e8885db51a4ee984994c28fc391de6c1be6ae604943ce07e9a` | 0 |
| src/process/ProcessManager.h | 3476 | `b1de0d805f64c83bd7ae0e81fe750c0ec7bd3ed09658a5b9b6956bf68c3ca4ef` | 0 |
| src/process/ProcessManagerImpl.cpp | 28276 | `b99dd5071aeea07bd8b7d8523a4e22d89a788cc25bf43c41d16c33cb3ba93d3f` | 0 |
| src/process/ProcessManagerImpl.h | 2223 | `12d8334613e9d2853084cd69c38270d9fe5b6426405e9f0249938c98e20154bf` | 0 |
| src/rust/Cargo.toml | 10582 | `e1508b777cd0928b6e11c5aece59a05153014cd4d283707fff617ca3c9257a0b` | 0 |
| src/rust/CppShims.h | 1103 | `70349212136741e639736171e09775f4f39dbef0a56315ba6fc259f51cb133dd` | 0 |
| src/rust/RustVecXdrMarshal.h | 891 | `c4a26bdbd4fe32b9dfeee189e1f97abb46ee5de3ba7f318bff03bd5403de3583` | 0 |
| src/rust/build.rs | 706 | `20f8f1a04f8d8df6916c0b7d08ac9c873dcfd1f493499cf5618774e7b4e18905` | 0 |
| src/rust/src/b64.rs | 1486 | `986e73a8b221e4019faa66f226207ca1938eaf7d4d6a95b12f17d7320fb337a6` | 0 |
| src/rust/src/bridge.rs | 19889 | `cbe49e7294bdf0fe5912b6c8c3a65d3e283c06a0eb8db1a058c55717a5412a0d` | 0 |
| src/rust/src/common.rs | 3638 | `de18ae3232501e9f954ce19a522455f46ab17e45d68d8af98dd175c3c507585d` | 0 |
| src/rust/src/ed25519_verify.rs | 1701 | `0c8a955b09410967749e56e4a3ceb839e522e6e86b80925604757e2e0ec0116f` | 0 |
| src/rust/src/i128.rs | 2175 | `5eab693ecd4b732cd7dbfc1a7fb3e3f97d5df14d8956752be6931a5d7feb83bb` | 0 |
| src/rust/src/lib.rs | 1903 | `e88257a50640d92fcaa297dbd37aa239c6239db67624a52d4a421275be1d32b4` | 0 |
| src/rust/src/log.rs | 4729 | `1adf29fd2b94110b4dd18ba807bbb21ff01bda7b3b5c982d12f0e200028f9e28` | 0 |
| src/rust/src/ntp.rs | 1721 | `bbbb4cbb0c7c07e96512c74f6e2e0c7b93988d021e45cd940a451d194283e0cb` | 0 |
| src/rust/src/quorum_checker.rs | 4028 | `00644d22472d362994c391f49f8f0b9ff0cf08b60ab831766b0cc88725780626` | 0 |
| src/rust/src/sha256.rs | 1949 | `9e6e0e3bc239389adac21386dc6d17e4ef76025966f1f388acf0d4ef75aea814` | 0 |
| src/rust/src/soroban_fuzz.rs | 2182 | `3048c48621f0d2ccbf8ab40c3fa26c864ef0aa10ed06aa91ec7007ee8831d54d` | 0 |
| src/rust/src/soroban_invoke.rs | 4490 | `50dd7871e388207d459b374f11aecb1c665f7841c8720c31b21ca233332cb3ce` | 0 |
| src/rust/src/soroban_module_cache.rs | 10471 | `fc36c15e50b689fc2b36163c4023e602b3fde9e2fbe7b4afd83544b97d158574` | 0 |
| src/rust/src/soroban_proto_all.rs | 86518 | `71c76d1182a12792c0152875379121341230a657df6239e02df40ae4f6c237ec` | 0 |
| src/rust/src/soroban_proto_any.rs | 34293 | `937c67d2a0af7a59d09e3f870958bb179bc1cc7bce50ba7a56f2e5c34b1e7296` | 0 |
| src/rust/src/soroban_test_extra_protocol.rs | 8339 | `2b2f34c7435eb885b02bbb829321a679299d0c98e90582328aad99d4983d7bc0` | 0 |
| src/rust/src/soroban_test_wasm.rs | 6609 | `01efa761a77632932664cc83e13c7a4d54fd09f7ffe360b027df533b0ed0a1e8` | 0 |
| src/rust/src/tcmalloc.rs | 3603 | `66aa39b3fed8f258c62a17c2fab386baf22f500fc7b923e3e042824eed6c85e6` | 0 |
| src/scp/BallotProtocol.cpp | 68363 | `1eba2feb54e4d53dbfe742b35e6aeffdc0523a254d8d2300ad6325906bd2a29a` | 0 |
| src/scp/BallotProtocol.h | 12270 | `91830680a75e08aba01ea6d415037a7a79466e53c1c95b968993769cbed895ca` | 0 |
| src/scp/LocalNode.cpp | 11271 | `69ad310c7f7dade2589821d871fd642aef323574a078da0fc8219f31207f68e9` | 0 |
| src/scp/LocalNode.h | 4349 | `c61e88f9a1ea5851d9c4e0418b0f62c17630948ceb65fad8c6cbaa5cff3644b7` | 0 |
| src/scp/NominationProtocol.cpp | 25695 | `2e700d99f199370ec0a45720a0c972b4a222480de79bb57e23926ba597e9f2ea` | 0 |
| src/scp/NominationProtocol.h | 4444 | `54e83abadc47c04546e5c8b3f1a22a90806244bb71123b753c1c663d37017cce` | 0 |
| src/scp/QuorumSetUtils.cpp | 7151 | `ef19ed2b8dc78c720cdd85e7628988614e912cc80573d6cde5e5ee390662b13a` | 0 |
| src/scp/QuorumSetUtils.h | 629 | `8586adf557f5f4c29b3089957aacda781dc728ea3cf3c55495d15c11f4b65546` | 0 |
| src/scp/SCP.cpp | 13239 | `18fe10f460800adf96a88750d2b3d50d23ff3e5596e77477ffd3d687bd7668ca` | 0 |
| src/scp/SCP.h | 6220 | `eee40a1d6c6667a2e85efbcb816e8173887a9ae9f37b4b549c19675af7ac42da` | 0 |
| src/scp/SCPDriver.cpp | 4717 | `c337dfa5de6f227e3ec85990fbf41e61c151775d8d158e5527297408463e8478` | 0 |
| src/scp/SCPDriver.h | 12807 | `bc2d4fa5ee2b0254e6499732cbd530747abd9316fea91130631f4cbe292ba4f3` | 0 |
| src/scp/Slot.cpp | 11903 | `f8b8b6fe1f4f8b48fd67b6324576420d816fbfac7c4d57358630a6bbd773544c` | 0 |
| src/scp/Slot.h | 6790 | `3e8d4576d6287eb8c3af976761a0d3b46a58a1a9ac75902256add0db258f7383` | 0 |
| src/simulation/ApplyLoad.cpp | 124035 | `14e1e3a9767fb6403861d4e49ca2b3c30d4201e1d80833278ebe91e3e4097cbe` | 0 |
| src/simulation/ApplyLoad.h | 8790 | `581f645005f2876c6f9ed6ee7fe626a6d45aff4a4ba64e1e1f5cf41d9b4224c7` | 0 |
| src/simulation/CoreTests.cpp | 22196 | `bda062db371c0782bc7ae36d223d898ac43277b935ebcbcdaa5415d546836fd6` | 0 |
| src/simulation/LoadGenerator.cpp | 67968 | `6e1cf9812b424b8c92e0b8786dee9e2d2ef2f2225a287c5b89558a09bdde5358` | 0 |
| src/simulation/LoadGenerator.h | 16309 | `d515a95e190300e993b8c10f4506a5e7bb777ff6361f9783c021c7d52ef702cb` | 0 |
| src/simulation/Simulation.cpp | 23080 | `40350a4714102aa6581e5a00df357837bc59030bc11730855f8bd5ac95b64cf0` | 0 |
| src/simulation/Simulation.h | 6594 | `e1281b0fcb806c7468115476ced8a6053537e6d63d28e751c50c1d030ce47429` | 0 |
| src/simulation/Topologies.cpp | 14535 | `dc6ae5279fd3143b4f0dd3e5e41f4a17ab2575e4fa5b5b4b40122c1cf767b8db` | 0 |
| src/simulation/Topologies.h | 4080 | `2437b53e69f2e878d32835d973f3dbcd24dbc1bf27bbe9352345b004d9c01ace` | 0 |
| src/simulation/TxGenerator.cpp | 67315 | `10c8a6c18aedb6a8cfc4f7d96d7e17fbef87e55222d63b873ed8da84070d5cb5` | 0 |
| src/simulation/TxGenerator.h | 15043 | `ecb5b92be6542cddb10c0a8d3fcea595c3ade264ca55ba82cdff5004d9a16514` | 0 |
| src/transactions/AllowTrustOpFrame.cpp | 5759 | `3a8c3290c521f35ba8a5c3e998b113ed62683b4750bac16bd2aee26c6e68c758` | 0 |
| src/transactions/AllowTrustOpFrame.h | 2085 | `726330acebd75e674ca9f5ece085fa69a25ed96ffd47e2babd3b0a1f66a6ebb2` | 0 |
| src/transactions/BeginSponsoringFutureReservesOpFrame.cpp | 3506 | `ba4f705978aafe38d890bce9773ace46bad61fd4073f6691c25de718bb429de3` | 0 |
| src/transactions/BeginSponsoringFutureReservesOpFrame.h | 1500 | `d4f79760e02b13bb373697aea9724508e84a44953b4d9090cf0beb1f9249086e` | 0 |
| src/transactions/BumpSequenceOpFrame.cpp | 2677 | `15bf88f1cbda4a6bcea02bf8e08f47d3d3fbe788879b80e1baab0f4a596d627a` | 0 |
| src/transactions/BumpSequenceOpFrame.h | 1344 | `7dca8d6a2be0230b48894f3a95e46b288a3b01619e62744bac0c925420e49a05` | 0 |
| src/transactions/ChangeTrustOpFrame.cpp | 11797 | `f52c24a6a95f7762122fa75cf04d487b8199c7f73176c8629c871ce57fb7831e` | 0 |
| src/transactions/ChangeTrustOpFrame.h | 1597 | `c1508a76fd74b19669d74e02cf824878e1242c5661d224917626c75c33397fb7` | 0 |
| src/transactions/ClaimClaimableBalanceOpFrame.cpp | 6752 | `88dabbc8648bbea177e2b18fe37db0435e214323f8fca496861c5e508e8b392a` | 0 |
| src/transactions/ClaimClaimableBalanceOpFrame.h | 1883 | `06d14b13360f98f6d47f2ce000adcf6a60eafc0e667ab936775dc978201ca285` | 0 |
| src/transactions/ClawbackClaimableBalanceOpFrame.cpp | 3333 | `c6d8195d42643c036b147b65a79f128ceb310fda7fc85dc9d12b4e8e121f0259` | 0 |
| src/transactions/ClawbackClaimableBalanceOpFrame.h | 1443 | `8c6e668f10eea92055b0961829b0b57935d46e288dec69f6f01f4625f1644f22` | 0 |
| src/transactions/ClawbackOpFrame.cpp | 3072 | `05fdf01677ed11d5820a6ce8098368c42cfe5320bebc31e542d4262f7bac291b` | 0 |
| src/transactions/ClawbackOpFrame.h | 1279 | `3ec84a6d1fa4524772f6280e2737cb844f4e08d3568c017921e5a0c98536d313` | 0 |
| src/transactions/CreateAccountOpFrame.cpp | 6410 | `100bcc573e6ba23789189e075f718761a048c169de8b2c5f74dadbfd1e8b3cd3` | 0 |
| src/transactions/CreateAccountOpFrame.h | 1436 | `04fcc6c9c07e00dd151a2dd9e1e411ea8e3d5305a3989327aa68e4e0f5c574f3` | 0 |
| src/transactions/CreateClaimableBalanceOpFrame.cpp | 9985 | `55491d3de603c3a8547d78c657d27f8adf9aabc5c55ef4f4d7b31f95e3f52063` | 0 |
| src/transactions/CreateClaimableBalanceOpFrame.h | 1538 | `ba73dda671f1461009e384aea7dcaeb1fefbe4ce32fd09603213861fabba5420` | 0 |
| src/transactions/CreatePassiveSellOfferOpFrame.cpp | 1095 | `b7109a85e7daefe9b773ea9b6745a860f264b6e8bc229d7bcdefd60411d50074` | 0 |
| src/transactions/CreatePassiveSellOfferOpFrame.h | 709 | `22fe202f2996c7ac0372eeec08d054c7f0e87c01458d571780abf8c1c4e03d5d` | 0 |
| src/transactions/EndSponsoringFutureReservesOpFrame.cpp | 2456 | `60f055d9067798b6ad6d6cf9a99da4036ece2285da9a00e9ffb71990f6604d27` | 0 |
| src/transactions/EndSponsoringFutureReservesOpFrame.h | 1285 | `b969be22de578488bcfe905bc2c807e306ea0e7ae17a1d5a6d47be1c5931059a` | 0 |
| src/transactions/EventManager.cpp | 18092 | `fc0254bb7a27efd89e8392cdbd01bb93f28bb4a14f4764011353af9c8e331ce8` | 0 |
| src/transactions/EventManager.h | 7493 | `3676ba3bcccf1fdfc0f4b6516f742c4b70d40118aadf3aceaf0368b0c4a27f1c` | 0 |
| src/transactions/ExtendFootprintTTLOpFrame.cpp | 13924 | `92ab2a106c8ac5bc6d1a4a9015ae4d214d533b61074baae71ff6d4df8360819e` | 0 |
| src/transactions/ExtendFootprintTTLOpFrame.h | 2743 | `edafee3018a73381d943535937ab6efec4c2f095550e46ccb7dbb0a769fd8493` | 0 |
| src/transactions/FeeBumpTransactionFrame.cpp | 24074 | `e1b3b19e620d5b1386fc2f07d90fffb54794972d487428861b666aed389fd49d` | 0 |
| src/transactions/FeeBumpTransactionFrame.h | 8255 | `d11c3cc93b6fc3edd3794d034ab05106c1edf8068e9369d66b2b45311f32e9ad` | 0 |
| src/transactions/InflationOpFrame.cpp | 5004 | `ab23e8a106a2d6070acb090d6fdb32b3fe5b69a9ba0f360c63b60c660dc23d9c` | 0 |
| src/transactions/InflationOpFrame.h | 1218 | `5d8b7212a594d2c2b0c56829c9755ba5fdd0a240b1f6c56fc9b48bf0a890733c` | 0 |
| src/transactions/InvokeHostFunctionOpFrame.cpp | 60406 | `785a333f7a9f1b179f20438534aea73a3e8e7d42de6d19203274c5eee08545ff` | 0 |
| src/transactions/InvokeHostFunctionOpFrame.h | 3071 | `5273dbc00eb9bdc968aa5eb22c25d35a13b066a3963d20defa7ef853d8e3270f` | 0 |
| src/transactions/LiquidityPoolDepositOpFrame.cpp | 14529 | `a74a7a86433ca54ebc6dae7d18def0d816ff8be74adde8b06d981627aef584bd` | 0 |
| src/transactions/LiquidityPoolDepositOpFrame.h | 2641 | `bc939523a3fdc86f335cb38c9011e042c9e573ad314f34451770cd24d54f94bb` | 0 |
| src/transactions/LiquidityPoolWithdrawOpFrame.cpp | 7933 | `83a8b5227867323f4aefdc000d59fbc2659a0a9d7077e1f1e8a43e5410280904` | 0 |
| src/transactions/LiquidityPoolWithdrawOpFrame.h | 2041 | `8792ef7bbb25e72b7171aef026025fb31a0455ecab09cbb70f472b3b8e07c877` | 0 |
| src/transactions/LumenEventReconciler.cpp | 2496 | `735c1a2d13a88edda43d3b0740fb11a40deb88f832f034455a27dec15ddae07d` | 0 |
| src/transactions/LumenEventReconciler.h | 789 | `f66a8bde26295f3f2b19052bdde6cc46c2647501309c5d0d9088a75a2a4ddf9d` | 0 |
| src/transactions/ManageBuyOfferOpFrame.cpp | 4932 | `46ca22edc28c87b1395f3171a1f07f7df02e8e3dfbbb145ecbc355eb6c664112` | 0 |
| src/transactions/ManageBuyOfferOpFrame.h | 2493 | `587147da5bdd8abba8ef5b7d25dcec696c8c3e5da0d27d25906b2d0acae08f69` | 0 |
| src/transactions/ManageDataOpFrame.cpp | 4404 | `42a455ca3ab2e2377a3c631b0878a9c1d0eb207fb9b00edade10942fd5098297` | 0 |
| src/transactions/ManageDataOpFrame.h | 1227 | `7d1f43a6159e8aea27b6b9251db3648417732e61569d084de4230f85742c2a11` | 0 |
| src/transactions/ManageOfferOpFrameBase.cpp | 24884 | `0ce1ba5254a2650ceadf84f51c90fa641916db5af1907caa0291355301e2209f` | 0 |
| src/transactions/ManageOfferOpFrameBase.h | 4029 | `d1a842aee43e35916a65d800a6d5dba13e5f871a17fe3f818cad6f414a5e418b` | 0 |
| src/transactions/ManageSellOfferOpFrame.cpp | 5282 | `2494b3d8ec7eea3752eaa729d789a664eb16c746bf9d2b025f57abf7eed9e676` | 0 |
| src/transactions/ManageSellOfferOpFrame.h | 2558 | `0dfa660254e773e41354df851f454be27ccf24a2ffd89cf718b7d3d0a6e9a455` | 0 |
| src/transactions/MergeOpFrame.cpp | 9169 | `696918ca756c8a9b14897a67da63caf9a43a39eea10c6e568e9c5081483f0bb1` | 0 |
| src/transactions/MergeOpFrame.h | 1619 | `4e3dcb34b16a227a706f4a4218c8c8c3c8e2a5ed042a7db10aa2aa3af3a608a0` | 0 |
| src/transactions/MutableTransactionResult.cpp | 13641 | `3785b62343db7783f9e30d5ef5ba9e95a69c371641a983164f55293837851215` | 0 |
| src/transactions/MutableTransactionResult.h | 8767 | `d763962cd11993dc8d868ea674a042bd5de6745b50bf4f096679ab2e60c7cec4` | 0 |
| src/transactions/OfferExchange.cpp | 74743 | `702b48fbc6ce710e4d3e8dc8a99dc2714c69aa3e1db734aa6cad283f4813b9e5` | 0 |
| src/transactions/OfferExchange.h | 15775 | `085fbd0d16dbf26bd7bbc8404193db6c9b5e576bed64410769355089d7bf3e58` | 0 |
| src/transactions/OperationFrame.cpp | 15294 | `3b3b023d1a4ebd7b0afcaf100b2894ce96519905f68f19db0df06ab3fc25ac41` | 0 |
| src/transactions/OperationFrame.h | 6057 | `c745fcaf63610ec08592d0e0bfacf61259602bef28fc1ebe53d6d2033dd18887` | 0 |
| src/transactions/ParallelApplyStage.cpp | 1882 | `4f811fc0842454d0d97cd21746e6d94e5590e485e2416e746f2592ecc62b7c1a` | 0 |
| src/transactions/ParallelApplyStage.h | 3782 | `2f7ebd15755afae9035542c0764c4fab66b6a9507a27e8f2cf4f5cf57e1228bc` | 0 |
| src/transactions/ParallelApplyTypes.h | 6221 | `3a2930e0de14cdcb1751c58236968da50baac9e764014ff24b9c9156a3330536` | 0 |
| src/transactions/ParallelApplyUtils.cpp | 45860 | `a72bf0bddbe62ee38051ad14dcbb0e7df4601422d7c501f525b0370a8a0dff83` | 0 |
| src/transactions/ParallelApplyUtils.h | 18326 | `03eacce8ae6cfa8851533c50d5187601a2a991f7724a0c47f00fd247046bea04` | 0 |
| src/transactions/PathPaymentOpFrameBase.cpp | 8658 | `22ee1005c3a3174eb0933de88caab7f5f4f396771a61ba5b4cfe1e3daa55be98` | 0 |
| src/transactions/PathPaymentOpFrameBase.h | 3200 | `f6abfc71cd4d59e14d80573cf30d5ec13918504e5a10babdfb180e3cdb63fca8` | 0 |
| src/transactions/PathPaymentStrictReceiveOpFrame.cpp | 8960 | `99b0c0aa99440b37e7c9d7026042a101987be885fbbdc6d9210e16a34637a864` | 0 |
| src/transactions/PathPaymentStrictReceiveOpFrame.h | 2708 | `5b0706896a526e6f9a4a31a1784be80a8d1cdf279ffdaebd3cb9c690db449467` | 0 |
| src/transactions/PathPaymentStrictSendOpFrame.cpp | 8383 | `a8fc354115457b296d24c061a4312dfc9094010912abc89c656e0ded148afacb` | 0 |
| src/transactions/PathPaymentStrictSendOpFrame.h | 2752 | `8290174e0b39b4b273604c202aaa35252500fecf074292d2e89bdd8e8ebb1af3` | 0 |
| src/transactions/PaymentOpFrame.cpp | 6198 | `0553d1e3e1dbe0924d50e5a95f7772529fef720e4fe4beee5a1541377a7cb150` | 0 |
| src/transactions/PaymentOpFrame.h | 1444 | `3eae7a42a64cd080447d4e936ad697b7148600aae19c5eec5bde72b8fd8c76e8` | 0 |
| src/transactions/RestoreFootprintOpFrame.cpp | 17725 | `8e1df5f2cdbef4988be3b837f78ed6a616aef8317d391bf295f6a194d9941cc6` | 0 |
| src/transactions/RestoreFootprintOpFrame.h | 2730 | `371f29e5c0015560727c8c2587a296d5af2f6bd7f16aee52fd6a5a0ba151404d` | 0 |
| src/transactions/RevokeSponsorshipOpFrame.cpp | 15582 | `d046ce6950f696a16b94bd6f691b49761901550eee10da1fa414b9c8546a09a8` | 0 |
| src/transactions/RevokeSponsorshipOpFrame.h | 2383 | `5dcff735e3d08f0bb19d04d3ff06ce3fc546c2c6613539de42057c522a53d295` | 0 |
| src/transactions/SetOptionsOpFrame.cpp | 10036 | `985a681225ffeafd43d9310ac947d3c73c987a28f773ac9b316f884af2a6c7c3` | 0 |
| src/transactions/SetOptionsOpFrame.h | 1411 | `e8e89c3fba72fa7352c8c5c874bd6b6c6da6b88bb25d907b805109525728474b` | 0 |
| src/transactions/SetTrustLineFlagsOpFrame.cpp | 6621 | `98f44b684ae83877bfecaa48f695b19494ff2f99e156a5751deee74db61a62bc` | 0 |
| src/transactions/SetTrustLineFlagsOpFrame.h | 2306 | `ee6511685f03e6baf813876ef508fef5225eda77daccfe07474cec347c8eb795` | 0 |
| src/transactions/SignatureChecker.cpp | 6788 | `52935b39e4e6353648b8e4c24cccea61ee9db50e104e0eaff716a32010e46a04` | 0 |
| src/transactions/SignatureChecker.h | 3981 | `b3df190fd79f3490c138803b37578b558dfb7817f34ad84c8a3d2d72f0c0efca` | 0 |
| src/transactions/SignatureUtils.cpp | 3416 | `d71641714058a9af5fc77b26f32a810f6c9ddd42bad3d411ec24fb6b56c3616d` | 0 |
| src/transactions/SignatureUtils.h | 1360 | `979624e13fbcbb15508f0003365df4e237e45fe9a0fe4e50b0c9a06155c1b813` | 0 |
| src/transactions/SponsorshipUtils.cpp | 28731 | `e05d24b6528d651c72d9f382a2b494670045de9500da9a517ba11fe336acd779` | 0 |
| src/transactions/SponsorshipUtils.h | 4550 | `a313f61fc186d103511a6fbf6860d894b60d1e1f9c47dd9adbbee8fd70dd325b` | 0 |
| src/transactions/TransactionBridge.cpp | 5132 | `115eeeb2b03f538c100a1da6ef0b6c1d51549c3ce21862775cb4d0846563a8e1` | 0 |
| src/transactions/TransactionBridge.h | 1543 | `0835daac03deefcda3da6b34cc492a9d5b61582f9a99357068439f1321d66f9d` | 0 |
| src/transactions/TransactionFrame.cpp | 87484 | `fb6c9fcb85589265c3199205d247ae8ebb2aacc662b6182fe8ef098337ac9fd5` | 0 |
| src/transactions/TransactionFrame.h | 17818 | `18f4316135a6c9e65572f0cb91185d82076bec42d9deb8a7ca63b4f7261447f3` | 0 |
| src/transactions/TransactionFrameBase.cpp | 865 | `83d206d04ec3560fe1b6b7b43bee20fa7d8c92991bcf94e984f38ba6ef5eef90` | 0 |
| src/transactions/TransactionFrameBase.h | 9055 | `cd0ce1772c30736d3a035d22591cb8fb37bda6ce444c90b3c79199a3ca2f6e76` | 0 |
| src/transactions/TransactionMeta.cpp | 36420 | `8c033c5e2888a4c3f352a46c42c20d8f858b6c1872107bc8a9f7ceaa8a9848d0` | 0 |
| src/transactions/TransactionMeta.h | 7174 | `add6d2e3f8f2517c5578596dc1e91f5a9944185b8f19a601ecd084406e8ee6e4` | 0 |
| src/transactions/TransactionUtils.cpp | 67349 | `8d4bcec6edfd76a6e2b4df3d087341a769d755a147027ba25018525bf49ea5e2` | 0 |
| src/transactions/TransactionUtils.h | 16556 | `869db1abb3474aa7b6208538b9680fc52f04c75dcafa872c4368a7839836180b` | 0 |
| src/transactions/TrustFlagsOpFrameBase.cpp | 4587 | `d815ee83c516efd02cd85bb08b95f04347121fd959eaa736e8ee8b49a1893d71` | 0 |
| src/transactions/TrustFlagsOpFrameBase.h | 1975 | `b0c7ee6e86e21d73d03a36d9ef2a6315b7c4043515d3012a89faf1323876e996` | 0 |
| src/util/Algorithm.h | 622 | `0f300e41e959e60bcd3235899a7bfb96a9a74c5f08bd8e428df6c7a25d64ed80` | 0 |
| src/util/Backtrace.cpp | 805 | `a12479429d2525226cceb252ae51bc85b42e58a02de08c330414b139b23e4019` | 0 |
| src/util/Backtrace.h | 291 | `c8ff075e748a63b8d94b654f98a7b704b1f5617d54bcd33a9290fb759d2fe27c` | 0 |
| src/util/BatchExecutor.cpp | 9949 | `1c4ed38d8de7e3b5e59e0a1c96d9c31688eb90e43e1f892c7ca70448f8ef4e53` | 0 |
| src/util/BatchExecutor.h | 6923 | `9e34af9350aa34313c5e8addec02cb72546cc25d336cc49225c7d70665853a8e` | 0 |
| src/util/BinaryFuseFilter.cpp | 1499 | `3abcbd94619011d36595fd9794bea5bd828fa1a9295585c25bb5afcaa71d4108` | 0 |
| src/util/BinaryFuseFilter.h | 2959 | `6bf33943062f950fdb5e0221be60bd12a116f3aa34e779efe1fccabe2999f5e7` | 0 |
| src/util/BitSet.h | 8809 | `9747d5ef2fcdf2ead3003df2e384900c00a7587d21c8338dba0bb8893ae63a55` | 0 |
| src/util/BufferedAsioCerealOutputArchive.h | 2723 | `cd3aa2115406081a57b0a6d07da2dccfc30534f959233afa5d7b09ce0bd2395c` | 0 |
| src/util/DebugMetaUtils.cpp | 1995 | `0e04ed9461eb785b4f21d8b9eb5fdf3649ad0f22ed41ae19f2df4f7dac0f00a6` | 0 |
| src/util/DebugMetaUtils.h | 1583 | `642c9b673f7937bdd5bfddff1c81556ea77c239a8c3f6c7e0e3eaf42092f6012` | 0 |
| src/util/Decoder.h | 1611 | `16495e8cc8fc5d27512e798ba371910eef17f3585f48fc50c0dd122f855e7c79` | 0 |
| src/util/FileSystemException.cpp | 964 | `40598052424a252803c2e45045018c619f80d45380bbea5b5d5ae7805aa201ac` | 0 |
| src/util/FileSystemException.h | 938 | `4969413ffcb954807c07b771603c6f569a6dcfd9aa945b36464d705d5a94e2cc` | 0 |
| src/util/Fs.cpp | 11375 | `5312673eb7ae2858776eeb353cdfe44c4c4cf16d4671bcc852f758a1427a7727` | 0 |
| src/util/Fs.h | 3960 | `64eb0ea47aa5361e69a60cf0606c8d2235acd12de7a78da91e73837baf52e7ea` | 0 |
| src/util/GlobalChecks.cpp | 1483 | `bbc9f0efba5817f45adb2f8e4cc9a1928d4bc74991c27cbdc0a00ed1decd7b16` | 0 |
| src/util/GlobalChecks.h | 1787 | `ce852da18d9c8a7ef906780ddabd395f0029e426d5a0224b7b7b98ee5fce10ab` | 0 |
| src/util/HashOfHash.cpp | 465 | `3384d63a66952539f2a1f8bcc52bbaaab90b399cac4f50f2e842a1cbe6b9b496` | 0 |
| src/util/HashOfHash.h | 401 | `360acd88fe5649ff7cb2c924d0e2b52f9274f62bbbdf031691d45b8324d2be37` | 0 |
| src/util/JitterInjection.cpp | 2984 | `9b3f97f116451c6b460d588eb41668804d0d28d43320d114c4c5b6494d9147aa` | 0 |
| src/util/JitterInjection.h | 4876 | `3630b8872ee5eb9e36617a9651715bbcd162caf416802fb3b4b5ddedf2945c97` | 0 |
| src/util/LogSlowExecution.cpp | 3655 | `0ce2843f70503f51c844371d79d2c4d1bdcac3ce3fbb79f2bacab9ccd0016dab` | 0 |
| src/util/LogSlowExecution.h | 1146 | `cddebd0a70f2b72ce9f884f995af503bc0f83d5c005bb96977f855baddec4652` | 0 |
| src/util/Logging.cpp | 15390 | `40557eca83b72d48132f8a23ec9d0b898b4a61f2c932adaefb727dc879434936` | 0 |
| src/util/Logging.h | 7861 | `38acfde8d78258aa71fcdfb7ab959b1870d1d130b98b36694ff48d16ebb62c07` | 0 |
| src/util/Math.cpp | 6799 | `2c60d32cde4ab47f4d8354adfa08e91d05446ba741b572ae0f340c2b16944878` | 0 |
| src/util/Math.h | 2622 | `1664ea2d24c5ceae79f5a06c78ed510b3a6005faefc5b3875051c08f2c72447b` | 0 |
| src/util/MetaUtils.cpp | 5754 | `696f1ab6eaddcb64be43b72804b758eaed69cf10c73e82dad2034860d5a87e18` | 0 |
| src/util/MetaUtils.h | 799 | `093ba10e8d38f13e763fd7686793dbcaf7b061f75c55bff311d969f72b0318dc` | 0 |
| src/util/MetricResetter.cpp | 675 | `c08cd9a9b874c52d69e7f5d20a82cc42ef9cad7bac587448ef8a33e18eb576bf` | 0 |
| src/util/MetricResetter.h | 749 | `3a466cc8d1cb62f1e940bf28c7f43f7c3df49c3bf9bb6b80ef0ada32a1fb5d88` | 0 |
| src/util/MetricsRegistry.cpp | 605 | `c6913a10376d5d636abcc133071d1c081efc58604ceb8e637a2a3e240c8f2ef4` | 0 |
| src/util/MetricsRegistry.h | 1275 | `c29e4a0421cd212d2f6ed3e0ada96a49dd1266b9404f15722f3f8e5177f074ad` | 0 |
| src/util/NonCopyable.h | 665 | `8df0d9b3d6d7055766f5713ca69d4d23f12a623231447ae9850768d5ef710709` | 0 |
| src/util/ProtocolVersion.cpp | 748 | `0d2c7d5f8e3df3dace91a91e0c9fc959c96d2b175428c267d1bfb27d25973cad` | 0 |
| src/util/ProtocolVersion.h | 3539 | `acec9e23aa993a6d679126043f007b988704df109d62cde5cf6aae4280455162` | 0 |
| src/util/RandHasher.cpp | 753 | `d7b866529d7e19f27ae9e6f857e10866b1c105cf7e211573d026ff3a06be093b` | 0 |
| src/util/RandHasher.h | 684 | `dda7efd973400db9d9d3645dd83597b7d15490b498f8e29a0f757fa49b5bc41b` | 0 |
| src/util/RandomEvictionCache.h | 7353 | `3e88ad5cb2d8730f709a5d0330eb4aa4bd079509db4788c48297ff4d8aa4b7b6` | 0 |
| src/util/Scheduler.cpp | 9907 | `f3fe4a20a62f4b4fbe6f7469209c9e2be35767c419f27df1790ebb429d7ea063` | 0 |
| src/util/Scheduler.h | 10897 | `a5e74cff6d3fe124f4c8665ca30cf691e1501e3a771b0fc2bf00b7d4cd2839e5` | 0 |
| src/util/SecretManager.cpp | 2327 | `c100d3cc20c3950167c695871f4d92e5f9b22fea0b49b0c41283f9b425f6bc9a` | 0 |
| src/util/SecretManager.h | 933 | `934a090322e15955bc8b40c35ec44bf2cef2ae474cc3b78bae05edd11d35109e` | 0 |
| src/util/SecretValue.cpp | 461 | `2cce32ec2bfedd0d5b30a514fb593ad1e4947f75f5baef61227c82674264833a` | 0 |
| src/util/SecretValue.h | 723 | `2735440303263383326dd66760e1434cdca239315f205b6421ba1ebd06983eda` | 0 |
| src/util/SimpleTimer.cpp | 1938 | `6921888f46dabf3936d390cb9d3b34d3a4fd1476dc1fba7cc1aae0f57bd188ba` | 0 |
| src/util/SimpleTimer.h | 2525 | `c933a1ef376bb6867e2c903468966b843de076c7475d66619207384f0e494d93` | 0 |
| src/util/SpdlogTweaks.h | 1091 | `a2f4b2f46609e35ab8e516c9bf655cce1c39b443478ef76ac7198b790436702f` | 0 |
| src/util/StatusManager.cpp | 848 | `d1451fd97d95c3f9d692369cbd1a9f14cab7787c130c90de771e246ab9090382` | 0 |
| src/util/StatusManager.h | 1277 | `13bcf44ad6f6d8bb9486ea1ccfc76e7169dd69189f393c5fc4974b1a8ca2e5e1` | 0 |
| src/util/TarjanSCCCalculator.cpp | 2150 | `6c4c1b7a0734744b27a6dc79f50abaa6e01e4519b1c4cb808c934f41a3bcb039` | 0 |
| src/util/TarjanSCCCalculator.h | 908 | `176eb00ef4396b5931c92fec90572671ab69ef1673e5361befa50b5fb852735b` | 0 |
| src/util/TcmallocConfig.cpp | 2278 | `27e3132b8b909dc160aa5b3cf47944c221faaaf76588a3336560589b40c104e7` | 0 |
| src/util/TcmallocConfig.h | 310 | `adaf21b2e10f6cdc1239cdaa98269e6281646931c01493c755c7c527cf7c3a8a` | 0 |
| src/util/Thread.cpp | 2562 | `bce9e6c80ca645f4d56e7ef2d5fbc844f1d9d0a3aa65fd242489d4b81f3fb574` | 0 |
| src/util/Thread.h | 883 | `c52865a7163c34691ad7c4d8a9d752791ae19521ce66637a24b3aa301fc4e298` | 0 |
| src/util/ThreadAnnotations.h | 11908 | `9384c730cef548bbcb401b13d46c98bd5cad0f2dbff80537046a958c4cd2b54b` | 0 |
| src/util/Timer.cpp | 18738 | `db65cc9277bfa50573152f47907fbfd9e690c3e677ef21499f8276c18964e4cf` | 0 |
| src/util/Timer.h | 12623 | `4b09fb9868b837961ed31549ea1cc798cdc9b580865c6037cfff6fa7ca2a274c` | 0 |
| src/util/TmpDir.cpp | 2067 | `a4d2f9c9d9ddef0ac4f391f9fee733cd7a3552bb32dae6927273f1a6f4d193b5` | 0 |
| src/util/TmpDir.h | 673 | `d4e612a2b7c7f3e868669cca6ee3a80e68220a18bd3e97ecbd630b420ac29db9` | 0 |
| src/util/TxResource.cpp | 4539 | `327fb3ac461127df3e587f44d391bda5b58a558dd4f0fcc858ce481cf5a466b3` | 0 |
| src/util/TxResource.h | 4199 | `ec669c8e7cdbd52b20f7dcd84c0ec1867a0f2affce3db0045972c2809f2e4adf` | 0 |
| src/util/UnorderedMap.h | 461 | `8579bed5398379320d2e2bf85dcf4964f94b6f401be8d28f16d55136abfd0c70` | 0 |
| src/util/UnorderedSet.h | 443 | `02d9806ad10c0fd0880a51b2703f10fd0932fcfc8af02caa12d3a89dae876fb4` | 0 |
| src/util/XDRCereal.cpp | 4946 | `6256aa1f94539b41630f540a8d8155dd7dc97e149293bc1fe9f20adedf8583d9` | 0 |
| src/util/XDRCereal.h | 6781 | `19b85601297a9bea94fb8f49782940c935df1c77f41228d72d78a08f4e8134e1` | 0 |
| src/util/XDROperators.h | 334 | `6f79cca7065228277e335bec5ddb05c273a107f9c33781343012cbb2e1c89a0d` | 0 |
| src/util/XDRStream.h | 14055 | `401a52c39de73021ab522d8f8b4f38ff9d2c0f47fc951053d20866127b1830bf` | 0 |
| src/util/asio.h | 1029 | `1d89800570808bb59b34904d75af17028054f18d48fa05f29a8ff2615f53a444` | 0 |
| src/util/must_use.h | 423 | `5cce14e1cffdc0c4fa3f4b6d424ca868d80bcde0228223cc519f73447a7c4678` | 0 |
| src/util/numeric.cpp | 11517 | `4c218b27585582311e76a32ee7a4494b58a1b09e4e2dadd4be3de24d83b5b26d` | 0 |
| src/util/numeric.h | 3613 | `8b1b178b91ab0bc3be158743dd440f7649eaf2e93e786ba0e640c5aa4609ca57` | 0 |
| src/util/numeric128.h | 900 | `1c77c09695c9e4d098d011b0738828a32926e0185ee0f6cff96be18267e9267e` | 0 |
| src/util/types.cpp | 8644 | `99c49e6288bc02bb40eeb834a991917ac12aac7f7f4d310def2b6ee5ce3eb067` | 0 |
| src/util/types.h | 5398 | `c0e241ea79a7c807e67f6c56c58fd6af78044a0361eebc14f6e6641ee81fa4fe` | 0 |
| src/util/xdrquery/XDRFieldResolver.h | 13862 | `bb9d78b00b62d3d60e08aefd606500379932372ebd9179dd8f0d2a4cbff72cc2` | 0 |
| src/util/xdrquery/XDRQuery.cpp | 1076 | `9694b253bce95d7b96809b5642700ffccec984fb98fe8cc2b9192ef0b4bb3671` | 0 |
| src/util/xdrquery/XDRQuery.h | 7015 | `14ccb2c8307f81e992a0cb4deb63bf0e159dfad0ae5ba3a0921dd2c148f06032` | 0 |
| src/util/xdrquery/XDRQueryError.h | 617 | `f5348464b85cd30bbc874aa3319118ac4f6f6ae6aa6c9a9de3f2996b18b52ac8` | 0 |
| src/util/xdrquery/XDRQueryEval.cpp | 12919 | `3c3be0288c7f958884cac2b370d6a16cde2f6f3c1bbaa8fe933f16e9dc740868` | 0 |
| src/util/xdrquery/XDRQueryEval.h | 7129 | `bcf6acdb4e1186f63ad3afe92894140f1278cddb5d89c084b5497498b0de5d45` | 0 |
| src/work/BasicWork.cpp | 11416 | `909c26a535e9caa810af5a72794003189785076078ccf1c80a27884062faabf8` | 0 |
| src/work/BasicWork.h | 11380 | `7ea70b287ace57e31acb9ea9311fc23717a8cc98f87d1db4a7d0859c9984c695` | 0 |
| src/work/BatchWork.cpp | 1882 | `7317c88f907cc437e770a4fb5cb04df0efe6f5aacda397fa199bc495b71eb6f3` | 0 |
| src/work/BatchWork.h | 1391 | `0ce70ded37764ddb9a0fd0596ebd9f7dab0a4467eba76f966d91809e12cf3675` | 0 |
| src/work/ConditionalWork.cpp | 2529 | `c37683eaf6154477445d8845e1ac33ecef66aaea9283ca718d55e8e7e32ec0d7` | 0 |
| src/work/ConditionalWork.h | 4872 | `aa42da4a5f0e6b6bcd63370324b4fec25dfdf8cc786ad9cdacbc9934efcdc398` | 0 |
| src/work/Work.cpp | 5568 | `b83ea990b317d14aa055a857682dbf337c127d618b2f5dd84e4c103ef4cc0785` | 0 |
| src/work/Work.h | 5139 | `a4b7eec155de474bc4dfddab0b24edec2d349ed0fa64a238f85212634c5e48f4` | 0 |
| src/work/WorkScheduler.cpp | 2322 | `db4b68ec8286af16adce8f3234603a93398d017940da3ffdb3269850570e41ba` | 0 |
| src/work/WorkScheduler.h | 2131 | `387ec31382b28a93f0f2b9b6e85b067baddbde4301682a73c2c78bae7e34cdcc` | 0 |
| src/work/WorkSequence.cpp | 2543 | `fe6c0463101f1f7b85ee5dfdd47841dee3f57a3c18644352c8bad2ff6f71393c` | 0 |
| src/work/WorkSequence.h | 1204 | `e5c4145875784ae9a6be0c376b8b22175a2e727c4c8ffee783ca5800bd8180bf` | 0 |
| src/work/WorkWithCallback.cpp | 1291 | `a2648a083d6d50a9e94e7ca966c3c1161811868ae4607b0b275e465633df1ac0` | 0 |
| src/work/WorkWithCallback.h | 654 | `21ab355243e1dea7bfa5594dcf21639ab97f97bf99c126f86ae1d4b643288072` | 0 |
| lib/asio/asio/include/asio.hpp | 7803 | `d81f5da7022952b78c302ea34a1ee6574159de30509526846e827eba49fc5e76` | 0 |
| lib/asio/asio/include/asio/any_completion_executor.hpp | 11955 | `f48ba1bb68d5b0b711de40b85ff3ce622fec100fcacabaa35f8d6c631c18ef6e` | 0 |
| lib/asio/asio/include/asio/any_completion_handler.hpp | 21761 | `5574cffe64849131ec871df7eeebc24292267ecc6dc552d6230cadfe5281ff61` | 0 |
| lib/asio/asio/include/asio/any_io_executor.hpp | 12318 | `16038b74df1d68fe3a0d705326f7c9d9e1bc6be93775f41c5990caa823383a54` | 0 |
| lib/asio/asio/include/asio/append.hpp | 2184 | `43e534ab2c0cf951bdff1b7787fe5201bd4d83da64537758de82168b8e9ac316` | 0 |
| lib/asio/asio/include/asio/as_tuple.hpp | 4415 | `a04beca95dee013804a3669bcdc05ddce99c31ff86c85910f34164f57acb8016` | 0 |
| lib/asio/asio/include/asio/associated_allocator.hpp | 6851 | `912024af25c24b24f563357c2f1a2d4ff691334b387a7170218ce2dfb9374dea` | 0 |
| lib/asio/asio/include/asio/associated_cancellation_slot.hpp | 7530 | `733543a5376d2d4c735550e8024caeb43689686f900dcd932d03073422f18475` | 0 |
| lib/asio/asio/include/asio/associated_executor.hpp | 7603 | `dcc32d162dee75f5794fcfc739dc95e3a352af251aa24756b3222dab8a83dcc0` | 0 |
| lib/asio/asio/include/asio/associated_immediate_executor.hpp | 9063 | `5a2d2e2863eea3328afae6b6538833cb1b679b504acfb0769e2d336e98c40e2c` | 0 |
| lib/asio/asio/include/asio/associator.hpp | 816 | `ac191907dd4e62c453614051923b6512f944a22eaded5398955aa92357e11a95` | 0 |
| lib/asio/asio/include/asio/async_result.hpp | 51266 | `70beb87ec6ee160f77558ad91dd142da1127cfd2d89cc910dae665d5363cd9c4` | 0 |
| lib/asio/asio/include/asio/awaitable.hpp | 3347 | `4dce0a40c2fb0e42b72c29beb4bcfb624f6e58af3d39a943c85721801b9f5c97` | 0 |
| lib/asio/asio/include/asio/basic_datagram_socket.hpp | 54069 | `3dfcd55f9bcf25f610fc4ccae567851cc36246434fa8792bfbeb5ab4933dd604` | 0 |
| lib/asio/asio/include/asio/basic_deadline_timer.hpp | 24403 | `47dc35d444e11873b88bf11b8d032be9234357277946c24199ac15fe2a2c59c6` | 0 |
| lib/asio/asio/include/asio/basic_file.hpp | 27110 | `f38ba2545a4015bb14aa320ab76c55696032b6c84529d6dd0e8704fa64a2d901` | 0 |
| lib/asio/asio/include/asio/basic_io_object.hpp | 7872 | `50372f202158b98cdca67f42631ea87dbabd934edb9bc8c045760caac4b9fc5d` | 0 |
| lib/asio/asio/include/asio/basic_random_access_file.hpp | 25682 | `72ad2eccf9095aa6cb7a495b71570b81d439836e6db68805c4dd7ab1d760287f` | 0 |
| lib/asio/asio/include/asio/basic_raw_socket.hpp | 53484 | `787e760e48a6b0f7cdcf7787a512feba6b1da38c323995afe3c8609917049455` | 0 |
| lib/asio/asio/include/asio/basic_readable_pipe.hpp | 21357 | `646d045254d8b4e10c2e75807283d3934fa2e320744bdcb27bcf38350e197e94` | 0 |
| lib/asio/asio/include/asio/basic_seq_packet_socket.hpp | 31804 | `1c7407c632665bdbe684285bb5bf1f5ae2b878542b7c2d0bfcdbb30d784855e3` | 0 |
| lib/asio/asio/include/asio/basic_serial_port.hpp | 34246 | `5664422639b2f25bc34067c3039d5aafac2dd31a5ca299cdf7e386015bb2b3ea` | 0 |
| lib/asio/asio/include/asio/basic_signal_set.hpp | 22530 | `598a2c495d4d3eacd740a9c73890f602e2330bb8f408b9ebe240db5a51744a83` | 0 |
| lib/asio/asio/include/asio/basic_socket.hpp | 65052 | `0e5b6616fd0c807d9092ab614c15b8aa333ba88f7c4806de781e0a43d89e8cf3` | 0 |
| lib/asio/asio/include/asio/basic_socket_acceptor.hpp | 96314 | `70a4f78e55d815d9dd918971d043e694c8bbb2fe53c920e78befcea2c8877477` | 0 |
| lib/asio/asio/include/asio/basic_socket_iostream.hpp | 12875 | `267937611e535b3ede9d6a0b18f10ff07238a399a76297338a29b8e53eb5683e` | 0 |
| lib/asio/asio/include/asio/basic_socket_streambuf.hpp | 20996 | `d616645deb3ff45c91111d6230845a6a99f7be19fdbd19dc01fe180d97ae690b` | 0 |
| lib/asio/asio/include/asio/basic_stream_file.hpp | 26724 | `ec6bff72b8ee6d5fe2ad7eb5d79fd4c69fbea951144ebb1cd1ee5b39c94dbadc` | 0 |
| lib/asio/asio/include/asio/basic_stream_socket.hpp | 46339 | `fe9347347af42914ef9019feb285b4944dfdf4629c5fcb0cff4c25434ed355bc` | 0 |
| lib/asio/asio/include/asio/basic_streambuf.hpp | 13450 | `a436cda805d163b8e40a333c93c6bc483fa5c1580939cb9e00249103c948a038` | 0 |
| lib/asio/asio/include/asio/basic_streambuf_fwd.hpp | 845 | `8fe271d744290390e281c43f0b5531652b532ea34f57ade25e863f837fb64899` | 0 |
| lib/asio/asio/include/asio/basic_waitable_timer.hpp | 28661 | `957c86bfd3799821ca91941f51a87bf6ed7baac530398f615d5d4324d7f3aab5` | 0 |
| lib/asio/asio/include/asio/basic_writable_pipe.hpp | 21253 | `18501d8b44464bdc79bdb096b9b6f378304f51969e1b90385595f9e4563ced1b` | 0 |
| lib/asio/asio/include/asio/bind_allocator.hpp | 20701 | `3aeb636ce47047d4a7bacd4441cd70c3f39057bcb3f88c2a9b18358f4d4c2871` | 0 |
| lib/asio/asio/include/asio/bind_cancellation_slot.hpp | 21771 | `d44f87d0252dab4710b8701324fe750cb4205d43f41fdb8ab4905ea860ae8709` | 0 |
| lib/asio/asio/include/asio/bind_executor.hpp | 22781 | `9c6c75587e0e59d69f1f22ebd4efb77fab1c62e5866c588c53b7bb0c982f88ab` | 0 |
| lib/asio/asio/include/asio/bind_immediate_executor.hpp | 21560 | `c1e7e69839027b4debc9da7921b214a4d4c37f6d888805550c4f068e8761f88d` | 0 |
| lib/asio/asio/include/asio/buffer.hpp | 94065 | `29737083d441455bf86be2e61df540138d194eed0c90dd2b11384b24c50208c6` | 0 |
| lib/asio/asio/include/asio/buffer_registration.hpp | 10264 | `4d4fe0eec4a3d0dcb0d7acd6df98510b3a0f787a6aff9ccaf1f69b355b46df18` | 0 |
| lib/asio/asio/include/asio/buffered_read_stream.hpp | 9351 | `23e7d2e61844f70ebbc9f41ed54c50256483358572cf324692519a73de4f1d19` | 0 |
| lib/asio/asio/include/asio/buffered_read_stream_fwd.hpp | 642 | `9dbf866a7c52d8dce2566f85f0985b0754417d404d98abcdc2559843e3fe31f7` | 0 |
| lib/asio/asio/include/asio/buffered_stream.hpp | 9814 | `e3e243257117977b7834b585112c415b9cdda6f49254897abcd7c356fcc19913` | 0 |
| lib/asio/asio/include/asio/buffered_stream_fwd.hpp | 612 | `d4b5cce8fa3d8de353070ad86c5240a706236accdcd7ee48673fda8d6c87d9e6` | 0 |
| lib/asio/asio/include/asio/buffered_write_stream.hpp | 8995 | `c3fb1c9449f5adb3fb0d2adba6abbbccddf6b620a190f742b53899cb78f8ff11` | 0 |
| lib/asio/asio/include/asio/buffered_write_stream_fwd.hpp | 648 | `4931cbec28c4691df84823d8ecab55a1fab18beba79980e57b3a3e3572649c3f` | 0 |
| lib/asio/asio/include/asio/buffers_iterator.hpp | 13866 | `2a0fc663f567f4d7b49871dd589ee666070d0ff498af51677b40f7d000805c06` | 0 |
| lib/asio/asio/include/asio/cancellation_signal.hpp | 8551 | `979ecb0f2d21ec96f4c654164cb7e104583e0ff95fe5fd3fc3209987f9e7a62b` | 0 |
| lib/asio/asio/include/asio/cancellation_state.hpp | 7133 | `bc7bf05ac2adf6ab57ffabce5dba4b65f5b1848c4f0dd49aa5017212c2c32480` | 0 |
| lib/asio/asio/include/asio/cancellation_type.hpp | 4087 | `47e24f5b24e84642c055787252a30caf1dcaff98c30a6cdc43e241c337975f57` | 0 |
| lib/asio/asio/include/asio/co_spawn.hpp | 16148 | `d145586a5034ca56a9b611f9b8a8710c6b9d2367be4ae99a2933af8d7737a286` | 0 |
| lib/asio/asio/include/asio/completion_condition.hpp | 5335 | `b29b02545bec5f57dc1136abb313224eb9498f382f18bf8a0f7bb33fc611cb12` | 0 |
| lib/asio/asio/include/asio/compose.hpp | 18469 | `a745261f34a46c8e8dea0d09ebf4fad64edec31bd6136f5a0ffd8284724b1f65` | 0 |
| lib/asio/asio/include/asio/connect.hpp | 47897 | `bd0f6b6b709286bdb00195e95d0afabf940bf92e583c4d47c58a931e63756555` | 0 |
| lib/asio/asio/include/asio/connect_pipe.hpp | 2203 | `32779e86d4f94bd7449ac655b21e2c4f41df861d2ce5e97790a867ad4357483a` | 0 |
| lib/asio/asio/include/asio/consign.hpp | 2551 | `44bcec4f9d6d56a2d36aa2b6c5edc16ae3f9573384e37edf1fe9b97493c4acc8` | 0 |
| lib/asio/asio/include/asio/coroutine.hpp | 9730 | `77146ca0e32f827de19626e33ee0c99ba82ff307b606213515eb3f12d137c20e` | 0 |
| lib/asio/asio/include/asio/deadline_timer.hpp | 1051 | `e49dbe1d2f983edf9ccd1d57c2bd1b93c1d5253ebb40a9258eeee4bcb0818ea4` | 0 |
| lib/asio/asio/include/asio/defer.hpp | 8491 | `877686365ed4a02591d1c4e7f49776d98442f27927228a7f1ba83d0efdd51592` | 0 |
| lib/asio/asio/include/asio/deferred.hpp | 24838 | `731b8f136092b9d56bd744dd0b95adac43414347d5f25f4528015f5df558f41b` | 0 |
| lib/asio/asio/include/asio/detached.hpp | 3436 | `05628c06b3aab8610089cb7443ce0b454476d31de96af559d5d2c6edd0fef476` | 0 |
| lib/asio/asio/include/asio/detail/array.hpp | 902 | `ccf5aab6a482f3e1c4dc8a65a628e3c4d66f6467c665b54fa4ec583619fc0b4d` | 0 |
| lib/asio/asio/include/asio/detail/array_fwd.hpp | 914 | `14fd38aa7660c71e7f67ea1612eb78a7f471756cabc75baba3577b6dcf7f11be` | 0 |
| lib/asio/asio/include/asio/detail/assert.hpp | 896 | `fe95a1f061312659fd5c44c0acc3c8d21d966ea1ef781b5fc1d4edad9d39cc0b` | 0 |
| lib/asio/asio/include/asio/detail/atomic_count.hpp | 2037 | `00be5a498e0efd3ef53ab2f5b507d4c701f79fa5a61df3fb63c56c797a46f3d5` | 0 |
| lib/asio/asio/include/asio/detail/base_from_cancellation_state.hpp | 4194 | `53f25fbd85466061d707b3d45ae97bd4e71be409d40f54eeb3846e6aeae65e43` | 0 |
| lib/asio/asio/include/asio/detail/base_from_completion_cond.hpp | 1690 | `e1b95b759aa285bc25a8bd736a4957718c1b1c627d6198c49b0a6cbf03e3648e` | 0 |
| lib/asio/asio/include/asio/detail/bind_handler.hpp | 34234 | `86ca7b401ac509bcb30e4a9826e90112f8e92bb655c1f4452729d275eff89e71` | 0 |
| lib/asio/asio/include/asio/detail/blocking_executor_op.hpp | 2685 | `97ce65eb5ef76dd02e65b4fdb2e432d1922700ee6f61a504df751622a04ae25e` | 0 |
| lib/asio/asio/include/asio/detail/buffer_resize_guard.hpp | 1512 | `0899e5eaa55517f83e6c0b4702d3a2e1e64fb6f6073e72c5b323cc8ec4617f7c` | 0 |
| lib/asio/asio/include/asio/detail/buffer_sequence_adapter.hpp | 19081 | `d7ea4daebbaa9eef2b5b7ee6571a3d57dde494b835f2bd3e4fcf29aa796d78a8` | 0 |
| lib/asio/asio/include/asio/detail/buffered_stream_storage.hpp | 2874 | `1e750580c6fde1ff0fcf9f11c34e3b04b7dea42a4e6af2144fe75f4903f302db` | 0 |
| lib/asio/asio/include/asio/detail/bulk_executor_op.hpp | 2657 | `2985b7575b283e9f77ee6cceff0abbd5ff45ae4b49822e0e370e87fa5f32ec2a` | 0 |
| lib/asio/asio/include/asio/detail/call_stack.hpp | 2916 | `764565cc7ae4faa289107c5455467cb7001c09c887a61bcb3a96f993f77e5199` | 0 |
| lib/asio/asio/include/asio/detail/chrono.hpp | 1964 | `c5bd75d1ed625295e3def18c66065c92137eb2a169b50ab70b8bb3b58cff11a2` | 0 |
| lib/asio/asio/include/asio/detail/chrono_time_traits.hpp | 4394 | `c794f5b1192c326ce399993b3f983f0ac5d78ec8f1ee884e9cfd67908fbdaecf` | 0 |
| lib/asio/asio/include/asio/detail/completion_handler.hpp | 2662 | `1b886fdf4db2e28ae2098cd5a0acdc7b701add5b9219ef96e55a3377c1785dee` | 0 |
| lib/asio/asio/include/asio/detail/composed_work.hpp | 7144 | `fac201d6acdae38c8a603da3067ef630637f332df78d076bb5f90131f37a010c` | 0 |
| lib/asio/asio/include/asio/detail/concurrency_hint.hpp | 3858 | `40dd848aac539da2b9ac511c720e55b646191b3da18823d354d6ea68e0947eb4` | 0 |
| lib/asio/asio/include/asio/detail/conditionally_enabled_event.hpp | 3012 | `4a17e25849653c83c198729e70394b56fbe708c6f146f12daa8bc2801a2bd79a` | 0 |
| lib/asio/asio/include/asio/detail/conditionally_enabled_mutex.hpp | 3019 | `0331a0f2c6f1d626c3a2c48da702da77dc6ecf4f8c3deae7bd002d2bda4307c6` | 0 |
| lib/asio/asio/include/asio/detail/config.hpp | 91572 | `f67aef4a87fc1b91f005d591d58e123666e3d9d222467bdb11e04e296902b26a` | 0 |
| lib/asio/asio/include/asio/detail/consuming_buffers.hpp | 11345 | `805c1153ff37eac555e9dd8c5019a57e6559955809f4bb8b56a31f8b7af90593` | 0 |
| lib/asio/asio/include/asio/detail/cstddef.hpp | 735 | `3a67ce0d5c2d7ff175e5ccc0a629d3a594158eab96efca9487aa546be01fdb4f` | 0 |
| lib/asio/asio/include/asio/detail/cstdint.hpp | 1505 | `01200b4acaf32ac22fb0f3e90feda0d4755c4cd548b98664e75eac205681dd90` | 0 |
| lib/asio/asio/include/asio/detail/date_time_fwd.hpp | 768 | `15f7e63ffd4b89c723d517946c49ede5eea2aea3f95af038b078fb223224278d` | 0 |
| lib/asio/asio/include/asio/detail/deadline_timer_service.hpp | 10016 | `95ca9fb6defdbb01e96556018ba3c977ebd7d3a9bbc873e8049da5e64154ee05` | 0 |
| lib/asio/asio/include/asio/detail/dependent_type.hpp | 816 | `d4c7cd80b0baabcb026493f0626156f9e0b8b545f98d98dc11cdbca71438e71d` | 0 |
| lib/asio/asio/include/asio/detail/descriptor_ops.hpp | 5231 | `451c4615a841b6881cb2a7c22845d4013972b59569adba4b388b95301953c8af` | 0 |
| lib/asio/asio/include/asio/detail/descriptor_read_op.hpp | 6065 | `4342ec26c41a655ee6e3c53d0ac7dcd0250136574f40da59bff4242d1a69b286` | 0 |
| lib/asio/asio/include/asio/detail/descriptor_write_op.hpp | 6041 | `fd086d004fce7402746889579422f36a834b01465f19fa9941d223f02a615998` | 0 |
| lib/asio/asio/include/asio/detail/dev_poll_reactor.hpp | 9033 | `c081dcfbfc4e8d14173845fa54f5d90c5cff30f953f780c0f6ffa9d472a8a44c` | 0 |
| lib/asio/asio/include/asio/detail/epoll_reactor.hpp | 10407 | `5b3b98e8c04aede7db92f5e32c55c42525407eab2896d48cb9b9b630b85859df` | 0 |
| lib/asio/asio/include/asio/detail/event.hpp | 1229 | `05da1c029bafbcf795f63820780a1a8a7f55f56a8353b36e32948a19a729c368` | 0 |
| lib/asio/asio/include/asio/detail/eventfd_select_interrupter.hpp | 2377 | `51bda324eb4e36330b1eb8d9b2afd8697c52739ff4e49675776275cc74bf58f3` | 0 |
| lib/asio/asio/include/asio/detail/exception.hpp | 1081 | `5ecd018c008d939a2c6b3ff4908e7403fa23d2f027f9f986d8eb2f5b9b34bb30` | 0 |
| lib/asio/asio/include/asio/detail/executor_function.hpp | 4805 | `0bc3668e143b36b71e2663f9eae394ffc87b0079489c352182eaa7669c41528d` | 0 |
| lib/asio/asio/include/asio/detail/executor_op.hpp | 2477 | `cb43dfc1aa98031e2f7bb42164adebc811a079d862a7c3677aa3a0940be6a681` | 0 |
| lib/asio/asio/include/asio/detail/fd_set_adapter.hpp | 971 | `399f9196223d85a0da64e495da9249c3940ddd791eef1bb86f5bceb89cd6511e` | 0 |
| lib/asio/asio/include/asio/detail/fenced_block.hpp | 2895 | `4060a2e506114e4dd3c894e8814e847ce4082948a3cc7bbedc33f4bdcd0e8dc5` | 0 |
| lib/asio/asio/include/asio/detail/functional.hpp | 1063 | `c87b6b64e52b1e077b21c6faef79c72e09117ca535524cec544803dd857c8c80` | 0 |
| lib/asio/asio/include/asio/detail/future.hpp | 1175 | `4ee1399609b850a2e2d63f49b15f9379e89f5110f1d307e4e02d43fb3ff2d46f` | 0 |
| lib/asio/asio/include/asio/detail/gcc_arm_fenced_block.hpp | 2157 | `07acf24d86d832411ef13a6e443dc94d34cd8b13d6b283a13a44e4c49051ce24` | 0 |
| lib/asio/asio/include/asio/detail/gcc_hppa_fenced_block.hpp | 1479 | `e94986b9b2e92fc8444863fce630243c1cbe725f21810c2487b8a26ffa2b4771` | 0 |
| lib/asio/asio/include/asio/detail/gcc_sync_fenced_block.hpp | 1598 | `6fbd74ba56e26610c591be3d04e4057170100b2b35b5b835cdfbc1ee7d6a6c83` | 0 |
| lib/asio/asio/include/asio/detail/gcc_x86_fenced_block.hpp | 2381 | `049efd86ee11b989efc0979779a587a985cba2f5cea90081abda9351564f79a0` | 0 |
| lib/asio/asio/include/asio/detail/global.hpp | 1262 | `945b3ffa5894fe3ecd530eaae9b4c609af68f0f8be673e4809bc64ce9dea55bc` | 0 |
| lib/asio/asio/include/asio/detail/handler_alloc_helpers.hpp | 7916 | `6f7b594e761324cb6cd236c6d7d917f9d9735248ada322565d12c2a3c07404da` | 0 |
| lib/asio/asio/include/asio/detail/handler_cont_helpers.hpp | 1284 | `c0811b1f348607329dd2a1e4d4b7c6a17492837f9217b7e10b5cb6121a1288b4` | 0 |
| lib/asio/asio/include/asio/detail/handler_invoke_helpers.hpp | 2564 | `131f6b7a136fb4b5c1188ab22b4f59d690d671347c6770489536addd3429508a` | 0 |
| lib/asio/asio/include/asio/detail/handler_tracking.hpp | 8413 | `b3a983d4a747f33d625723f538b7c28b1465eeb595995302249733b42ff3e8dd` | 0 |
| lib/asio/asio/include/asio/detail/handler_type_requirements.hpp | 18764 | `2a0cdca792ea1cdef5416ff32dacdc958a0fe53a1a5352e37a70b2e7f782f7b4` | 0 |
| lib/asio/asio/include/asio/detail/handler_work.hpp | 15753 | `2055be9d3b74dd9dbd2d2722a9280e50aaa20e207a0845dd285ed6c3f4cda57b` | 0 |
| lib/asio/asio/include/asio/detail/hash_map.hpp | 8184 | `b88eb6287182844e50806148207f6d737ace2d83e255ee23a7aba372dc7d06c2` | 0 |
| lib/asio/asio/include/asio/detail/impl/dev_poll_reactor.hpp | 3087 | `cb179808b1fb9ef4c463674af3e0ed643ac5f5058a60b6f69391fa4d0efa2c6d` | 0 |
| lib/asio/asio/include/asio/detail/impl/epoll_reactor.hpp | 2946 | `48c3278d8088cdb8493538ee61466610468db2033c7a0f619bcf9a480c61a582` | 0 |
| lib/asio/asio/include/asio/detail/impl/io_uring_service.hpp | 3021 | `3dbfb2d5c67b90e7aeefe4cfbc4a7fc6bd337ccd7bb43f5aac517894526e5562` | 0 |
| lib/asio/asio/include/asio/detail/impl/kqueue_reactor.hpp | 3093 | `1ca6cf43960cf5919b2ce63fc754173057d9a40a9d089b7accd611913a2a3fe6` | 0 |
| lib/asio/asio/include/asio/detail/impl/select_reactor.hpp | 3560 | `8aa95811752017a17d6b81077b9dcb77774a5f11ffda844353a53f1d582eb9fe` | 0 |
| lib/asio/asio/include/asio/detail/impl/service_registry.hpp | 2571 | `4ee1f7ca3a6e4757f2b13864ab098cdd080b578fcf7160c8e5c6f009e3c0ff4a` | 0 |
| lib/asio/asio/include/asio/detail/impl/strand_executor_service.hpp | 10447 | `9b564148424bcf02eee83ed36c67cc2b2219e0d534d66d22a79f0f64d78b6138` | 0 |
| lib/asio/asio/include/asio/detail/impl/strand_service.hpp | 2570 | `23c0c957856f459c19282ed80459d526db21e10b8061bf118e9b031ebad60a4f` | 0 |
| lib/asio/asio/include/asio/detail/impl/win_iocp_io_context.hpp | 3456 | `9cba1d20baa01057d2cf258c0c0036577cb57b1868c83d10ff07979d6e1baad5` | 0 |
| lib/asio/asio/include/asio/detail/impl/winrt_timer_scheduler.hpp | 2556 | `11a4c7852c9efc2f1bae514e15e87a29604daaa08b938e80a4ad95846f843fe0` | 0 |
| lib/asio/asio/include/asio/detail/initiate_defer.hpp | 7785 | `112bf6fee8d58e16a0078f708a61f124d04f5521475c30cc998b4da989c60c49` | 0 |
| lib/asio/asio/include/asio/detail/initiate_dispatch.hpp | 7078 | `097861dd4d23623457005136af47ce7fbe8ffccf7ebf519b9cf669d1c721705a` | 0 |
| lib/asio/asio/include/asio/detail/initiate_post.hpp | 7726 | `6222f0d62b6a9d4d2d70eecf1199037c6b6c6423e0025a087d866d4a19e71f6f` | 0 |
| lib/asio/asio/include/asio/detail/io_control.hpp | 1796 | `e48065304138a2049f015c7eb60964e7b05608b54b771d3d9c9e9ecc4d79259c` | 0 |
| lib/asio/asio/include/asio/detail/io_object_impl.hpp | 5098 | `38cb490e64733a595f694aa8ce3594c0f05b05d360bdaea1f9cdd324d4669121` | 0 |
| lib/asio/asio/include/asio/detail/io_uring_descriptor_read_at_op.hpp | 6227 | `48055b94dd46acd1e1693b15e032a3c78ffca6473805dd6ce89c960a324e3345` | 0 |
| lib/asio/asio/include/asio/detail/io_uring_descriptor_read_op.hpp | 5983 | `ac7dbafa563953653bc289985bb42c606b6957184b651993211affa3135c2726` | 0 |
| lib/asio/asio/include/asio/detail/io_uring_descriptor_service.hpp | 23263 | `1a5ed47799b6503e2b2ba3a220a9a0793ba59404baa789174d306e489d898248` | 0 |
| lib/asio/asio/include/asio/detail/io_uring_descriptor_write_at_op.hpp | 6073 | `f51b881e3f5e9b9c6cbcdf5c4dda60f73c48a9419e25d75733f587f88ef69938` | 0 |
| lib/asio/asio/include/asio/detail/io_uring_descriptor_write_op.hpp | 5864 | `da54a2c3324348c949bf50314720bb3beba0b5f93261716f287f64537614ff91` | 0 |
| lib/asio/asio/include/asio/detail/io_uring_file_service.hpp | 8428 | `926823bff15be0f38dcb114b3541ac30945415b7bc897c75372c11b4d4c6c72d` | 0 |
| lib/asio/asio/include/asio/detail/io_uring_null_buffers_op.hpp | 3676 | `160ebc2b0bb00cb6ee118c7a664b433c78c8cfcd625e908de25e08bb0d784458` | 0 |
| lib/asio/asio/include/asio/detail/io_uring_operation.hpp | 2119 | `e457af4d406cb20a24f4e03dc3635d025d5a3f1590bb3cadc3c780ca65b3276a` | 0 |
| lib/asio/asio/include/asio/detail/io_uring_service.hpp | 10341 | `aa4e7f0253ec8b34a355b6cf127326919cacc60de3058bc13fde59091ba9d52c` | 0 |
| lib/asio/asio/include/asio/detail/io_uring_socket_accept_op.hpp | 9229 | `0468977d2c51dceeff7159ed5037942fbe5ccabfcfa669c0beb3bd4e9f5ee6a4` | 0 |
| lib/asio/asio/include/asio/detail/io_uring_socket_connect_op.hpp | 4374 | `15f29e91dba55fd9313f0f5396bb56fa90e349e4d25d121965eec12ffff69ff1` | 0 |
| lib/asio/asio/include/asio/detail/io_uring_socket_recv_op.hpp | 6570 | `c3bf57d6c846f9dc0bca1094fd81c6e25ea530deaa4a5fd086c5a395f580a0f9` | 0 |
| lib/asio/asio/include/asio/detail/io_uring_socket_recvfrom_op.hpp | 6781 | `3ec394af09b2d8385f7328570b8608b9057ff1087cf3154df6064f6571c9f594` | 0 |
| lib/asio/asio/include/asio/detail/io_uring_socket_recvmsg_op.hpp | 6093 | `e230dfdab7fc99951de4952e41bb323e41047c7f2356393e97187e7691004652` | 0 |
| lib/asio/asio/include/asio/detail/io_uring_socket_send_op.hpp | 5977 | `2da0f250f487e14d1c30806dd159c6de75795a449260e531511d2132d7d74fac` | 0 |
| lib/asio/asio/include/asio/detail/io_uring_socket_sendto_op.hpp | 6194 | `96ea0c05068c4c136bf732402d96f8c43449ba3c83fa9707816d6c7730295dd1` | 0 |
| lib/asio/asio/include/asio/detail/io_uring_socket_service.hpp | 21476 | `1ec867841f23d81cc63fae54ee46a9e039be5e737a1c59a72bd84ae7d7976cf3` | 0 |
| lib/asio/asio/include/asio/detail/io_uring_socket_service_base.hpp | 22642 | `5e549fd0ccddcb9c2ea82837bc0f13c8c56d98c626859f9ff3d5fcd72d7163b5` | 0 |
| lib/asio/asio/include/asio/detail/io_uring_wait_op.hpp | 3504 | `effc9564f06435f50d9150cdb6a6c46dc2911f99146ef7d47d59d3532617b91f` | 0 |
| lib/asio/asio/include/asio/detail/is_buffer_sequence.hpp | 8258 | `7128b32dce187beb5fcb3047380cd9e21d888713f7dc62e45c867ca21de71fcd` | 0 |
| lib/asio/asio/include/asio/detail/is_executor.hpp | 2952 | `d56d034c27a89de41df3e8a751dbbe725e1ee872f6294fb32f4f225babd93ddc` | 0 |
| lib/asio/asio/include/asio/detail/keyword_tss_ptr.hpp | 1320 | `dc8815de08761a4284a4c0d098828fd22ba5742db7fe7af0d158e60558d70d4a` | 0 |
| lib/asio/asio/include/asio/detail/kqueue_reactor.hpp | 9309 | `bef2545c2aeb1fdd855dfef2e4211586d0cc6caa955979e3e1200d88c3777630` | 0 |
| lib/asio/asio/include/asio/detail/limits.hpp | 692 | `f9ec68ddd720db18fa4315fdd24263463944c075157f17c9b08a80949c741dfd` | 0 |
| lib/asio/asio/include/asio/detail/local_free_on_block_exit.hpp | 1359 | `5c5337b78651004488c1c60c17668a141c2408c9c0a4766e48c8b28437b4c01c` | 0 |
| lib/asio/asio/include/asio/detail/macos_fenced_block.hpp | 1299 | `21641169d355acf318bd1d554697e059b9cdc92f0fb8ccbb816e4ae4a1346673` | 0 |
| lib/asio/asio/include/asio/detail/memory.hpp | 5083 | `06fed90fbb254cd84a417afcfa939689ce67dbced8d2a588deb08aa673b32e74` | 0 |
| lib/asio/asio/include/asio/detail/mutex.hpp | 1216 | `8dfc232916fbe8869d1a06b4e29834537150b03b7535b416f1c58dbe852aa853` | 0 |
| lib/asio/asio/include/asio/detail/non_const_lvalue.hpp | 1407 | `c943b1f7c33af21cb6b72dc877c283691059a8a5e05e0d552c6daa26a3e644a0` | 0 |
| lib/asio/asio/include/asio/detail/noncopyable.hpp | 918 | `dc3f8558f0977a59619c6b91dfa73a3014c128aa7234c5f58197d9fa7cf50ec3` | 0 |
| lib/asio/asio/include/asio/detail/null_event.hpp | 2086 | `ec27d43397a1215f9a2b1f87fad4fe10ffa6d8b4ed73268f86bc47c3066b5f2d` | 0 |
| lib/asio/asio/include/asio/detail/null_fenced_block.hpp | 969 | `2038e5fe97c56774509988c1a68206626220f472b724830fde9c5c4c17c28f37` | 0 |
| lib/asio/asio/include/asio/detail/null_global.hpp | 1220 | `6a2a4db82784c75a1ae61e657d60b46349a46e87da4ce506c26e0c66214e3946` | 0 |
| lib/asio/asio/include/asio/detail/null_mutex.hpp | 1079 | `a0cef5c50c31cb50eae78480a69dd270daa7073d0d2cf095f0f725756cf060c5` | 0 |
| lib/asio/asio/include/asio/detail/null_reactor.hpp | 1721 | `2a188cedfb125f6cb98150cdd834218042ffeb242b0ea563216653b1142ef9c9` | 0 |
| lib/asio/asio/include/asio/detail/null_signal_blocker.hpp | 1510 | `3449c7658437d9d6ecb5ad1175debf8cf03e5ad21639d8700af00a762b1a6cb4` | 0 |
| lib/asio/asio/include/asio/detail/null_socket_service.hpp | 16294 | `ebdffe97eb78effd1b8a4ba441b60dad809b6f91cb2a6c3ff7eee3a1b0c42561` | 0 |
| lib/asio/asio/include/asio/detail/null_static_mutex.hpp | 1153 | `6160e5a6cfe33298587d2eb5bf16406eb08843555dcf02d7ba8e01c5b31a8f30` | 0 |
| lib/asio/asio/include/asio/detail/null_thread.hpp | 1323 | `e6d4fb2a0d485f6b493408d63a3f745a1943419ee52c500f16247911e50da086` | 0 |
| lib/asio/asio/include/asio/detail/null_tss_ptr.hpp | 1179 | `1dbcdaa4695c5d9132767ac786feb958018fac6da2ccf19070ef4de317222be9` | 0 |
| lib/asio/asio/include/asio/detail/object_pool.hpp | 3425 | `d09efcbd118c6ed1b54607e89d8a6e76b8554574db530d9d82b9d582f3754d85` | 0 |
| lib/asio/asio/include/asio/detail/old_win_sdk_compat.hpp | 4373 | `b4585269078fbb6ab0c7d2aa677e17be5821e9404af8aa86fa9689cd967d352f` | 0 |
| lib/asio/asio/include/asio/detail/op_queue.hpp | 3238 | `e10e7f8edd6ebab1bf08b7f27ee33edfd9683d814ea19fc2a05e143888cee9c9` | 0 |
| lib/asio/asio/include/asio/detail/operation.hpp | 876 | `1c80f50f9e66d5b10f7766e4b4bec3e5504e6abd046aaf87e8d656949c031009` | 0 |
| lib/asio/asio/include/asio/detail/pipe_select_interrupter.hpp | 2432 | `f8a3157bb370ced09808eb927496b70b3543ea318d5e0a0ad43630b77aca7e7b` | 0 |
| lib/asio/asio/include/asio/detail/pop_options.hpp | 3153 | `f76aa7843d0711ee060f7b1fb4459e4404abb149dec43e58d256430ca9004115` | 0 |
| lib/asio/asio/include/asio/detail/posix_event.hpp | 4383 | `a63be121e96bcf41efc047031fd5e1b52b2fc02277cf6902862020901e6aa1f5` | 0 |
| lib/asio/asio/include/asio/detail/posix_fd_set_adapter.hpp | 2866 | `68f6502149b2d6f96abd34f092b1b449b3c0f21e4b52589dde2394c49bd2d02e` | 0 |
| lib/asio/asio/include/asio/detail/posix_global.hpp | 1720 | `5de79f96ab988701ebc73e2d828e3a1fc1adcfa9ddce6670bea8beef72d7cfae` | 0 |
| lib/asio/asio/include/asio/detail/posix_mutex.hpp | 1555 | `a163e174f1422a8656ab2ffb28d7ef2314eca02fef2f62fe265a7aa79f7cd642` | 0 |
| lib/asio/asio/include/asio/detail/posix_serial_port_service.hpp | 8293 | `dfe345ad163a8f15cccecab9acea88f4511e7bf2d55ea1c611828087b4449a92` | 0 |
| lib/asio/asio/include/asio/detail/posix_signal_blocker.hpp | 1882 | `adf24723fa630dda1a78505c00958a8021200a35d6f1734896e169c41f81a715` | 0 |
| lib/asio/asio/include/asio/detail/posix_static_mutex.hpp | 1361 | `e341e383663b21ada2bfec03ca04557e1d3b956ac8d82022c8ff5e42b83772be` | 0 |
| lib/asio/asio/include/asio/detail/posix_thread.hpp | 2034 | `e9377b55fcd5434d9a30b798846ee96826aac2b6f4cf72759587f57c2ab99834` | 0 |
| lib/asio/asio/include/asio/detail/posix_tss_ptr.hpp | 1683 | `c43c0af2705158412d68632019e9216f218c015a6cb9aaf1ed1f0861b05c8021` | 0 |
| lib/asio/asio/include/asio/detail/push_options.hpp | 5574 | `6b751947b9004d91bbb68b80b0790ffec60dc70025a887c07b7ab7e639550a4f` | 0 |
| lib/asio/asio/include/asio/detail/reactive_descriptor_service.hpp | 18651 | `be7d28dc018a8be3127333c8ab425c3c226e8cd9d514a9ce5ffc14b3c9640d78` | 0 |
| lib/asio/asio/include/asio/detail/reactive_null_buffers_op.hpp | 4488 | `3326639e91e6441aeb023ebb3e9781a2a30d099c1e0c4c10bff420416de2e8ef` | 0 |
| lib/asio/asio/include/asio/detail/reactive_socket_accept_op.hpp | 11133 | `20a2210926da4d948c670612e279723cbfb4e334e2d931f21fda1125ff4b7126` | 0 |
| lib/asio/asio/include/asio/detail/reactive_socket_connect_op.hpp | 5233 | `ee8144a0260388d428119b022fa2be84c49fef240c14a70815b8ca1c152af95d` | 0 |
| lib/asio/asio/include/asio/detail/reactive_socket_recv_op.hpp | 6681 | `fea9efe09875ff50e596e8860e3005642218ff5a35192bb922156906801d8701` | 0 |
| lib/asio/asio/include/asio/detail/reactive_socket_recvfrom_op.hpp | 6925 | `32c5e38ea5ba700239c73fa7e7b4f28cb1d642aa8f6f6ad626326c4fcf93d4f0` | 0 |
| lib/asio/asio/include/asio/detail/reactive_socket_recvmsg_op.hpp | 6269 | `bed446ee6f017898ea1d55442658e4b056a6c4e698ef087937e9839f9e67fffa` | 0 |
| lib/asio/asio/include/asio/detail/reactive_socket_send_op.hpp | 6779 | `c36f6fdd23aa534684ef7264b80dcb59fe122cd6e64c9a49ed60faf49879a627` | 0 |
| lib/asio/asio/include/asio/detail/reactive_socket_sendto_op.hpp | 6614 | `ba62e04c42ddafae0fe1d45082f57f1c010c49a7743cb5c37323ad9d8df6cba9` | 0 |
| lib/asio/asio/include/asio/detail/reactive_socket_service.hpp | 21440 | `7f506a909cc25b63dda63140185e0680d999a67442c3d55c3b17105b6b5b692f` | 0 |
| lib/asio/asio/include/asio/detail/reactive_socket_service_base.hpp | 26247 | `ade01124bd7d01a772c8e407462e1f1f8bfccb151d090487af9d44e023f54239` | 0 |
| lib/asio/asio/include/asio/detail/reactive_wait_op.hpp | 4274 | `d422f2d62f56c2587b10ae6633bc5c9e731a1418ed0551e3a05c14157c39d964` | 0 |
| lib/asio/asio/include/asio/detail/reactor.hpp | 1480 | `9d0341092bdd75ffe6920878a4037fbd6224ff5fb38624cf2b34ec5a3ee0a5d7` | 0 |
| lib/asio/asio/include/asio/detail/reactor_op.hpp | 1775 | `3e755b412274f394cbcad01d7cde1d0b36615333f662d92e7e1930b46bd500d7` | 0 |
| lib/asio/asio/include/asio/detail/reactor_op_queue.hpp | 6467 | `39d6f0be65617c1acacb33900643f36c6e594419412462110b73b29d490dafcf` | 0 |
| lib/asio/asio/include/asio/detail/recycling_allocator.hpp | 2333 | `828ed37e6ecee8f74d42e9f30ef4721766d9aaca7aac13d4450c2dec6e851594` | 0 |
| lib/asio/asio/include/asio/detail/regex_fwd.hpp | 1136 | `1d0cc9face2e60396d4e7a6c415c3d2ebd57f5de132ac6af0fd51f6de3fa0ba2` | 0 |
| lib/asio/asio/include/asio/detail/resolve_endpoint_op.hpp | 4692 | `5780f246af1dbf19c39cd2ee59f0411e4463ec402061bc44210030c80a4b4939` | 0 |
| lib/asio/asio/include/asio/detail/resolve_op.hpp | 994 | `43a6d2edd6077f9b8f74246f9a63829956b14e479c0570b4fc6a86d7cff442ea` | 0 |
| lib/asio/asio/include/asio/detail/resolve_query_op.hpp | 4792 | `81f8ec45c01ce4ea2abff2a4fcdae73a22dbf234c05ecd0d7a44e81c9d0857bc` | 0 |
| lib/asio/asio/include/asio/detail/resolver_service.hpp | 4654 | `757f8db6a61d548308a400bc4c1186f873c44fcd5262c5f113c5c2c821211989` | 0 |
| lib/asio/asio/include/asio/detail/resolver_service_base.hpp | 4544 | `e938228a8ec6bd8aa2ce862773ddbd5a843fbc128e4e3a7f126eca25e80d6751` | 0 |
| lib/asio/asio/include/asio/detail/scheduler.hpp | 7580 | `e0e10e54829f4673963c0ecd060adb552dac0443707a97ab063871f989614d8c` | 0 |
| lib/asio/asio/include/asio/detail/scheduler_operation.hpp | 1800 | `b3a09bd378c97af3196ed881c365c1625da64bb7101d52eac35f35b29ffd2fb9` | 0 |
| lib/asio/asio/include/asio/detail/scheduler_task.hpp | 1142 | `82d78c7d8a0daa847ec978ea7143074de5e27a60a714fd8b2f8dc93cf343d610` | 0 |
| lib/asio/asio/include/asio/detail/scheduler_thread_info.hpp | 998 | `2e994fc4be5a9fc5f28b95e97857bcc4c006a6a0f6febbcc220e36cf581efac0` | 0 |
| lib/asio/asio/include/asio/detail/scoped_lock.hpp | 1867 | `1793470eabd549dd9ecbe5d8d572d22a23670757e58e3491d2d0970bf91773c8` | 0 |
| lib/asio/asio/include/asio/detail/scoped_ptr.hpp | 1373 | `57005d1b4cf87c31d0d8a4202cbf40be53e31dc9bb15c91a7e77da11f42992e0` | 0 |
| lib/asio/asio/include/asio/detail/select_interrupter.hpp | 1309 | `d40218b3b59e1ab84076da03b9c994e8c3a5b27cb393c28694ad88111690708b` | 0 |
| lib/asio/asio/include/asio/detail/select_reactor.hpp | 10294 | `54ee6fd3151449c4ee99a65f993255cdb380f309e0406a87c0c1b0a22cf42101` | 0 |
| lib/asio/asio/include/asio/detail/service_registry.hpp | 5425 | `db05069544915093499b9b2df779a145e8b1eff4323fe2f65857fbc9a53495da` | 0 |
| lib/asio/asio/include/asio/detail/signal_blocker.hpp | 1259 | `1ff6ddb6a776a91e76c94c4b8e48ebb1652d42ec2d86fdc22cdc442d9f68797d` | 0 |
| lib/asio/asio/include/asio/detail/signal_handler.hpp | 2752 | `abd729af3e3dceb265096126727e61f33616c7bb77adb28ae9dea48ada66030f` | 0 |
| lib/asio/asio/include/asio/detail/signal_init.hpp | 983 | `158ab1b0116de68d8f83f092f46e1f517ba066e994ff8e331000c4e7e8eb5946` | 0 |
| lib/asio/asio/include/asio/detail/signal_op.hpp | 1167 | `f6f4f1c128d64504c1ed4e259ce4bd7c8db248fdfd919d0f2ed1feca346a939f` | 0 |
| lib/asio/asio/include/asio/detail/signal_set_service.hpp | 8623 | `3f061ac676703663956a8190dd520e29ad1c3f2423b3119625490a00c5e04d35` | 0 |
| lib/asio/asio/include/asio/detail/socket_holder.hpp | 2043 | `f7abaf15b7698a36f01cb9f6c206315d7dcd94f30fdc017905a7d74b3ba76141` | 0 |
| lib/asio/asio/include/asio/detail/socket_ops.hpp | 12234 | `cd780bf0e1bcca37790bfa47076d96580a98500096a4d3d6bd614a0bb0be5bb0` | 0 |
| lib/asio/asio/include/asio/detail/socket_option.hpp | 6284 | `1a9de2b92ccd0be88491986f6b72dd01705c463c8b218fd9971c7d126aeb07ef` | 0 |
| lib/asio/asio/include/asio/detail/socket_select_interrupter.hpp | 2455 | `e8187cf7a8e45231c88e3653b3d6099ba27c44d0e32610f14cb4578fdd00bd92` | 0 |
| lib/asio/asio/include/asio/detail/socket_types.hpp | 15343 | `74885a62bd01833b40d3d747be6f66981ac69b8a28139d5d495b22037c6e43b7` | 0 |
| lib/asio/asio/include/asio/detail/solaris_fenced_block.hpp | 1257 | `ddac7fbda3243660e57140f0ebcc5e0597c3d93a4ead88d5f429bb33934665d4` | 0 |
| lib/asio/asio/include/asio/detail/source_location.hpp | 1337 | `1a672e10dea5fa2ae96b314c1f01bd8276f9e47854eb2d5bf5327a1e294cc63a` | 0 |
| lib/asio/asio/include/asio/detail/static_mutex.hpp | 1562 | `e3ac06b9475438d021845257edff278bfc03cbc31e8413e986c720f3ae84fd26` | 0 |
| lib/asio/asio/include/asio/detail/std_event.hpp | 3904 | `3c8719d06b3365ab0fc6b9a1d69fa3967435c67f1b5a2d5656a260f1400b0cb6` | 0 |
| lib/asio/asio/include/asio/detail/std_fenced_block.hpp | 1315 | `47669a6e68c1e386bf354effd4c4e4a7c2d3b1e5270ab993f171d6fa243de724` | 0 |
| lib/asio/asio/include/asio/detail/std_global.hpp | 1481 | `984717b75ec8fbe0686131efe04a44aeac7d964bed6bafd5bbc30879321ca2c9` | 0 |
| lib/asio/asio/include/asio/detail/std_mutex.hpp | 1298 | `201829fd27d215964c9c438cc2d5a4e2f8fb993db38caf3ef5146e0974bd9155` | 0 |
| lib/asio/asio/include/asio/detail/std_static_mutex.hpp | 1474 | `451c01c15aab7d9e47ce0668a401bea36a53b77e051f1c9c7625e830500736cd` | 0 |
| lib/asio/asio/include/asio/detail/std_thread.hpp | 1332 | `6e998c19c0f91403d897167fa22a03573df45fe04f5ec977cce68888033f85ea` | 0 |
| lib/asio/asio/include/asio/detail/strand_executor_service.hpp | 6178 | `59527646c5a8bf70ac13f6868db6e4e416fa13154a46aacc467cc1fd4dbe3769` | 0 |
| lib/asio/asio/include/asio/detail/strand_service.hpp | 4596 | `d8e9154862be604d4823ce327554ba4903b453930ac16ec94b998381df049267` | 0 |
| lib/asio/asio/include/asio/detail/string_view.hpp | 1426 | `8d63566b2b22808684623f37628ce7edd314cbb1b18b4e173a99c34580625fd2` | 0 |
| lib/asio/asio/include/asio/detail/thread.hpp | 1499 | `de98327c0c8368ffea29c542d5f633b69f834528faa3cf6ae23467c80d30f5d0` | 0 |
| lib/asio/asio/include/asio/detail/thread_context.hpp | 1371 | `e36fdecffcac0e7d5fb32c4b96d38b724f0113667316d5b64f6933a786a17f23` | 0 |
| lib/asio/asio/include/asio/detail/thread_group.hpp | 1992 | `5fe6a4ae8311cd980849782d218869666a6e507d5a104abb6465c6cff9563559` | 0 |
| lib/asio/asio/include/asio/detail/thread_info_base.hpp | 7096 | `4651f34dc2aeee8e7e4241c0d9ad3b3e03b35c554dd39b72f8570717ad26c3c4` | 0 |
| lib/asio/asio/include/asio/detail/throw_error.hpp | 1485 | `dc0f40cc9068768cb5b671b581e2aee9ce21d77410d11643a78d192ca1159e9f` | 0 |
| lib/asio/asio/include/asio/detail/throw_exception.hpp | 1489 | `98e5141239250c17c614d9e37afa9a5fe5360ebc51c50309a35efbc60330af52` | 0 |
| lib/asio/asio/include/asio/detail/timer_queue.hpp | 10562 | `07b10a02c44ee428b2eba2e9bb6a0fe5099bf59971e76b354994306a958ac63e` | 0 |
| lib/asio/asio/include/asio/detail/timer_queue_base.hpp | 1661 | `3ba8227e0fe41a6fc1114fa9ec5c0c827ed38df744652082f0545ee5d3409db9` | 0 |
| lib/asio/asio/include/asio/detail/timer_queue_ptime.hpp | 3137 | `116a789a142041599c072a300df3737112dc3859428f6b3dfd6a7c939d92389e` | 0 |
| lib/asio/asio/include/asio/detail/timer_queue_set.hpp | 1658 | `604fceea14375a6bf9e143ba66a5c77cced5663eb10541da003bc49e0ccacf1c` | 0 |
| lib/asio/asio/include/asio/detail/timer_scheduler.hpp | 1150 | `c1d2c80a8f633645ca47e4d36bd7d356c9100944f0d6a4d56d7d92b3c21b58b6` | 0 |
| lib/asio/asio/include/asio/detail/timer_scheduler_fwd.hpp | 1224 | `6f2d1a26660e1969826ac1c9073638d5e2f54b31182fb0f541a6f76bc66ca5b3` | 0 |
| lib/asio/asio/include/asio/detail/tss_ptr.hpp | 1712 | `ac1419b182f924a54569c157866c89ebf6e875943f6272e156b5a1c04e3da429` | 0 |
| lib/asio/asio/include/asio/detail/type_traits.hpp | 5454 | `7d971bfc95d56ca5fdc5d09c5518004aa599ff71491686e612e23da437b849a0` | 0 |
| lib/asio/asio/include/asio/detail/utility.hpp | 1849 | `3a3cbe374a425d28a393ba2882b8615a5ad02a32d5a6f243e253532150196cdc` | 0 |
| lib/asio/asio/include/asio/detail/variadic_templates.hpp | 11657 | `6d4d13b2d02a792081130eef93f2e8d261e499e7b5919e1af8a21c35928758bd` | 0 |
| lib/asio/asio/include/asio/detail/wait_handler.hpp | 2685 | `949b6fbcdf738856d99170a9e0a242fdca58ee6b1055500e7091486a057af476` | 0 |
| lib/asio/asio/include/asio/detail/wait_op.hpp | 1042 | `48d41cb5797e40107a296168fe6eee6d38f7895c0cf8c52d2af93115b4722404` | 0 |
| lib/asio/asio/include/asio/detail/win_event.hpp | 3723 | `41209913537ec441b8aebd949d6747079ee2ede4c30bfea31fa759847556f204` | 0 |
| lib/asio/asio/include/asio/detail/win_fd_set_adapter.hpp | 3806 | `8843c492a157f267f43fb45037f41348f7b749d8f1a034cdf56eaf1f007563e7` | 0 |
| lib/asio/asio/include/asio/detail/win_fenced_block.hpp | 2015 | `86a7d75ca7ce882ec980f7ec4baf0cd115170e3c8b3f6cf70478f619ee7f5da4` | 0 |
| lib/asio/asio/include/asio/detail/win_global.hpp | 1697 | `69e53c762e08614ce96a71e38dd3b3a97f11352e4f4f892ddaf95cadde2b4471` | 0 |
| lib/asio/asio/include/asio/detail/win_iocp_file_service.hpp | 9194 | `23f4d410101333ec0915911a2cc295486589e3d9b942520faa695edd239d593c` | 0 |
| lib/asio/asio/include/asio/detail/win_iocp_handle_read_op.hpp | 3770 | `abc684117275ea5a9210f20283cd40f8bafe09f02dae278d342f7d5b28b9953c` | 0 |
| lib/asio/asio/include/asio/detail/win_iocp_handle_service.hpp | 15909 | `6fb8faccf275f882f1061abde5960c24a7be4117645608b507bb379005698dc5` | 0 |
| lib/asio/asio/include/asio/detail/win_iocp_handle_write_op.hpp | 3632 | `658c4a2144bae74c4a7456194a98a65097c413897f313d48abe31d8c1fb7093b` | 0 |
| lib/asio/asio/include/asio/detail/win_iocp_io_context.hpp | 11658 | `a5289abdc7bbf74537dcecca5967f8700b22c50c858a6a5ef9b2bf72f57365f6` | 0 |
| lib/asio/asio/include/asio/detail/win_iocp_null_buffers_op.hpp | 3908 | `772bf5b5b7089504faced55f3f4e8300b16ee78473f9dee98efce72c834d2ae0` | 0 |
| lib/asio/asio/include/asio/detail/win_iocp_operation.hpp | 2041 | `4893f88568c254adf78df08f82d47fdb40824e957e35b6d0032d4a48cd36c191` | 0 |
| lib/asio/asio/include/asio/detail/win_iocp_overlapped_op.hpp | 3085 | `b788dc16f27f04c79748183ac2150b3bab194200ed91a796130dc468c09c349a` | 0 |
| lib/asio/asio/include/asio/detail/win_iocp_overlapped_ptr.hpp | 4241 | `e588fd00221024155e7614535928c1590547817be27dca92c400200fdf1e8293` | 0 |
| lib/asio/asio/include/asio/detail/win_iocp_serial_port_service.hpp | 7586 | `2803d81cec591fd8d23e1db46a17c72d0b515b336ccef785a5a8ce4714969dda` | 0 |
| lib/asio/asio/include/asio/detail/win_iocp_socket_accept_op.hpp | 10729 | `def57ef3ac79c70d0c82912875ea5dc04f040e923d3b25508912c3dd9d2c0fa3` | 0 |
| lib/asio/asio/include/asio/detail/win_iocp_socket_connect_op.hpp | 4005 | `2dc07df0e640031e48bf764f2e7f70a01668d02dfdad84a4d3a0cb9349e0e1de` | 0 |
| lib/asio/asio/include/asio/detail/win_iocp_socket_recv_op.hpp | 4040 | `b9faaee40ff7d72a5b15af667cc5a63a523e2db21fb453e4b5222fa3293ee0b1` | 0 |
| lib/asio/asio/include/asio/detail/win_iocp_socket_recvfrom_op.hpp | 4209 | `06357dfbd6c951c19b6f0bc7fcda2c7ff1296e3e143477b1849ab86cedd707f7` | 0 |
| lib/asio/asio/include/asio/detail/win_iocp_socket_recvmsg_op.hpp | 4020 | `d903d4f546273196179649d96b91a36cd50d67d35091a0f51816194727a973b1` | 0 |
| lib/asio/asio/include/asio/detail/win_iocp_socket_send_op.hpp | 3790 | `20c472655838673682f7a085c8697af9cf7a2f6cdfbbc735e7ab6ec1c5d1bdda` | 0 |
| lib/asio/asio/include/asio/detail/win_iocp_socket_service.hpp | 22833 | `ac3988d1837ef6ced0a1084b9dc7cc25f9a7fd400297b4a14b378c343a1c2b3d` | 0 |
| lib/asio/asio/include/asio/detail/win_iocp_socket_service_base.hpp | 29799 | `d18ffd40793678afefb59044dbb52585c680e62f01d2b48424db73289931d9c6` | 0 |
| lib/asio/asio/include/asio/detail/win_iocp_thread_info.hpp | 828 | `b46f583c22ea6e1a5742df5e1114f2eae822b0101eea628bddb6e3b6387a4026` | 0 |
| lib/asio/asio/include/asio/detail/win_iocp_wait_op.hpp | 3820 | `a35907c1ada0b8d2498c7ed1a9a07f3bfd902e8a8a22f5adddb2abdaf0e3c9b9` | 0 |
| lib/asio/asio/include/asio/detail/win_mutex.hpp | 1690 | `fbf453f0198e1241a4a117ee81169b2bee3533045915445c3c87f744c3c77934` | 0 |
| lib/asio/asio/include/asio/detail/win_object_handle_service.hpp | 6076 | `935e043a4a9261e15e1dc6492dc6856cbc6c345e68fe4dace158f8be04a6e5c6` | 0 |
| lib/asio/asio/include/asio/detail/win_static_mutex.hpp | 1795 | `08bbbeb442e9ab8933893fc5980966465e0db9dafd6a9c3dc5a0b43ce6de9a14` | 0 |
| lib/asio/asio/include/asio/detail/win_thread.hpp | 3044 | `44c565340e422864893dde5f8eeb11809468302f0c18c10c1df5492fe1a291ed` | 0 |
| lib/asio/asio/include/asio/detail/win_tss_ptr.hpp | 1621 | `98bfe8159fe891d6d785dddd88022d265a52ae8d0d15739035c591a1c9dcaa42` | 0 |
| lib/asio/asio/include/asio/detail/winapp_thread.hpp | 2588 | `ab37b916054b489c562828f3124a1f6c9ca839ff4777ce5dfb752906b7810f1a` | 0 |
| lib/asio/asio/include/asio/detail/wince_thread.hpp | 2543 | `8d6f2fd37bcef088299d31204de8de7ae32a81e23dba653a82a5bacb2daf50de` | 0 |
| lib/asio/asio/include/asio/detail/winrt_async_manager.hpp | 8673 | `c6aac02294f5f97501733b5b9bad057438a5f913af9ab4696f841805a33cf72c` | 0 |
| lib/asio/asio/include/asio/detail/winrt_async_op.hpp | 1388 | `93e71cb206488602f63d9a813092a78b6c6865d7993aad450ae7258689ab304b` | 0 |
| lib/asio/asio/include/asio/detail/winrt_resolve_op.hpp | 3849 | `b3ef83ba176ab9eb316a930ecb387f205eda911a4708b599ee9add20c29d8528` | 0 |
| lib/asio/asio/include/asio/detail/winrt_resolver_service.hpp | 6008 | `b15204eae0a90a64290e0b907bd07e6b7a24142f8fef4080c7193fa959f47764` | 0 |
| lib/asio/asio/include/asio/detail/winrt_socket_connect_op.hpp | 3056 | `adf458dea4aa0869f9490dae4ee14d88225bf32e25caf093889de2e32d74b812` | 0 |
| lib/asio/asio/include/asio/detail/winrt_socket_recv_op.hpp | 3828 | `4f27123bcbf9e9298e0b5ddfa2965ebca0e147e5285f20b76f9fd5ecf0b83e7b` | 0 |
| lib/asio/asio/include/asio/detail/winrt_socket_send_op.hpp | 3477 | `41d331e4f025e7a3d08cc5ddce3aa17302f863c114884a792704fcc7732eb48c` | 0 |
| lib/asio/asio/include/asio/detail/winrt_ssocket_service.hpp | 7099 | `cdf9331b5f1d59cfdee294deba663dcf3c57e102acf4e8d427c2b4b18f37f723` | 0 |
| lib/asio/asio/include/asio/detail/winrt_ssocket_service_base.hpp | 12133 | `0304f7cbac470c71d8aacaed8758a3c38e71ca5f43a77410109a61933f6ef577` | 0 |
| lib/asio/asio/include/asio/detail/winrt_timer_scheduler.hpp | 4545 | `5b1fae2af3d273a70af417c5840d077fc356a30d02d903c9a35e19e88419f755` | 0 |
| lib/asio/asio/include/asio/detail/winrt_utils.hpp | 2626 | `aa43bbfddd5fa51c5b714a3fe72fb611c98d47c727787b794df608b59d560b4f` | 0 |
| lib/asio/asio/include/asio/detail/winsock_init.hpp | 3090 | `4145b75a5ff67826e6626e1cc9317420b7fe9a331297762e31753b627f058b0e` | 0 |
| lib/asio/asio/include/asio/detail/work_dispatcher.hpp | 4268 | `016f4eda2c886652aae53f084b6a624bddf4e1036a4a71b13e5f208d5bd723cb` | 0 |
| lib/asio/asio/include/asio/detail/wrapped_handler.hpp | 9561 | `87229e73846b1828e38fbcf913c5ecdd069626abbf4d7f440ec2295789d3c46a` | 0 |
| lib/asio/asio/include/asio/dispatch.hpp | 7629 | `104bcf3130c6f60773a5c7bc5d924f0ac5cc91c1a1de4eb5ee9a35aaf01dcd74` | 0 |
| lib/asio/asio/include/asio/error.hpp | 10417 | `96a9be63036e3cbb39f26e89f250047e82d692cffb74188dcec1045406e10ce5` | 0 |
| lib/asio/asio/include/asio/error_code.hpp | 4560 | `722b9917e0da09972b26d1138202c47f588797fe908762eb3712b9092a3ca065` | 0 |
| lib/asio/asio/include/asio/execution.hpp | 1679 | `9b46df9b1583dd3c3dd6d0918cbf17566e5fac7eaf73c31602990751b5a0e0c4` | 0 |
| lib/asio/asio/include/asio/execution/allocator.hpp | 10225 | `a6f694142bf983ebe1a097c1facf30d92b3e15704bd2e731abcd8c7d788b7a68` | 0 |
| lib/asio/asio/include/asio/execution/any_executor.hpp | 80271 | `d02bb2d2ac83bfcf46abdf983aab79ba682c2887b04b15b724b8540e1bace26b` | 0 |
| lib/asio/asio/include/asio/execution/bad_executor.hpp | 1193 | `987fa011dd3f38546cef6c8beb7df764f9e4a9a91561095c99f5273dc96e1c93` | 0 |
| lib/asio/asio/include/asio/execution/blocking.hpp | 45920 | `cb9a65849ac37079bf3b5b905f13b39667519bf90d57a3eb5071a6c89686dae9` | 0 |
| lib/asio/asio/include/asio/execution/blocking_adaptation.hpp | 37217 | `776c799396f09a44144891ff8d12f7fe32157dc7b4c061d8b25b78180b7898e8` | 0 |
| lib/asio/asio/include/asio/execution/bulk_execute.hpp | 12722 | `eeb0d379170cad7becd27bbe7fa92104af1c449aa72374179f13c8b69d0b9f70` | 0 |
| lib/asio/asio/include/asio/execution/bulk_guarantee.hpp | 36971 | `97467ed09e8b386486254d363cf236d10b8cbda84a1496959df89b61f460e415` | 0 |
| lib/asio/asio/include/asio/execution/connect.hpp | 14349 | `52094258f73e41b6e72e9c2ca47950de11599bcf4735851026fe21625eb1d1fc` | 0 |
| lib/asio/asio/include/asio/execution/context.hpp | 6815 | `3328fc879ac9ea34f8d9958bd3122de6b83434fcaa1f88d1fa84a231b5d05b20` | 0 |
| lib/asio/asio/include/asio/execution/context_as.hpp | 6742 | `78c0dcd0e4349a77f471cbcf8b17374cc7f26fb4f8ed89bf6b8ccb07e54b25d1` | 0 |
| lib/asio/asio/include/asio/execution/detail/as_invocable.hpp | 3657 | `b756346044366bb79ab4ba0b4656f5af1b4fef3c76f9d6d259929f61325f6891` | 0 |
| lib/asio/asio/include/asio/execution/detail/as_operation.hpp | 3053 | `5832161b459f09024e51a646873724cbbeb5ae17b258020291491f25e9f2d836` | 0 |
| lib/asio/asio/include/asio/execution/detail/as_receiver.hpp | 3120 | `e1440d35fbe86e869d040b0d5552ddebbfbacc6d27534a1eb633d56b3686a042` | 0 |
| lib/asio/asio/include/asio/execution/detail/bulk_sender.hpp | 7878 | `72826fe2e82a0c1864ee9b0dd63b9ecf451b156df758e64e0328de916e7261f8` | 0 |
| lib/asio/asio/include/asio/execution/detail/submit_receiver.hpp | 6875 | `41b0693e7c27cc2656159de696c865a99763b42232b11b1be6d9f07f8a1d2fd0` | 0 |
| lib/asio/asio/include/asio/execution/detail/void_receiver.hpp | 2177 | `dbec1614aab3f3e7546b84ba8ad67298aca5c87b3ca68a8b07652e1b9d270c08` | 0 |
| lib/asio/asio/include/asio/execution/execute.hpp | 8259 | `927599f858952ab7e788027eaa20a1aa0e723816b0c8222fcc35dcc842b4fa9a` | 0 |
| lib/asio/asio/include/asio/execution/executor.hpp | 7406 | `582b877a6b4afb29f1c143c1f3531e3e4837ee08d3152b60f0460967f27a9ee6` | 0 |
| lib/asio/asio/include/asio/execution/invocable_archetype.hpp | 1890 | `2cdb6b87b7657270610cd9b94368d253a2309bc8fabab0d9742b31bfcefa9278` | 0 |
| lib/asio/asio/include/asio/execution/mapping.hpp | 33883 | `b6e5652c13e6233be1da315202f35aca7b5fb4244adac9ec647c49318dc75566` | 0 |
| lib/asio/asio/include/asio/execution/occupancy.hpp | 6762 | `a5709fa9d883d75175c94efc794f0feb52f4cb17cc25ebd2e0238e7395019567` | 0 |
| lib/asio/asio/include/asio/execution/operation_state.hpp | 2647 | `2fca81edd464e6f8f7a2bc2220ea275e73d8de0c0c583469da6291787c1d495f` | 0 |
| lib/asio/asio/include/asio/execution/outstanding_work.hpp | 26847 | `096897ebc1991c7dd6f8d612aebf4537d34ad4f04c16087a05b55bd2ebee42ee` | 0 |
| lib/asio/asio/include/asio/execution/prefer_only.hpp | 9247 | `aff38e3fafd03ac6df81d25ea36c4f8c1d04a9b6fc7ea67b1bffaa5f02bbf8c0` | 0 |
| lib/asio/asio/include/asio/execution/receiver.hpp | 9157 | `349a4d45e059ab430993d34d8bbf33b965c4ae5b34ae8f38a715526237a16bd2` | 0 |
| lib/asio/asio/include/asio/execution/receiver_invocation_error.hpp | 1304 | `2a79d70106d81fb2f4eec79b91316a37bfe056f64496f04010d6dbb469976dbc` | 0 |
| lib/asio/asio/include/asio/execution/relationship.hpp | 26246 | `79f38facdb9444bc17ec9cc6e476281ea840f486a2262ffa50272ebe185665bc` | 0 |
| lib/asio/asio/include/asio/execution/schedule.hpp | 7276 | `7090cf537196debb5f9cce2d14908a8fead1534c5f696c467666539874179885` | 0 |
| lib/asio/asio/include/asio/execution/scheduler.hpp | 2295 | `b22694beb7919e41bd1854e8c0e8614eb1e94a1b4ec2a427a0c7cfd09d0c8f89` | 0 |
| lib/asio/asio/include/asio/execution/sender.hpp | 8211 | `aee9d82ece39f6e1bd694358365868bb7eccd7fd3262234819e9401878d5a009` | 0 |
| lib/asio/asio/include/asio/execution/set_done.hpp | 6403 | `95f891ec468259719aeb924588a4c71adea35c44a25548b535e1aca389b578f1` | 0 |
| lib/asio/asio/include/asio/execution/set_error.hpp | 7118 | `024fcb8104dec111c1fa7f10c49b121a80231b85596692ad702e73f1864ca534` | 0 |
| lib/asio/asio/include/asio/execution/set_value.hpp | 14484 | `6108d92813b702ee7f45c4b461ef02a42c0387013de0804566f13b48818469df` | 0 |
| lib/asio/asio/include/asio/execution/start.hpp | 5981 | `a49cdef8e95de393dcaf18d693f88bca379267c1f758a413b68baee5128befc2` | 0 |
| lib/asio/asio/include/asio/execution/submit.hpp | 13068 | `2f81b5f5c1dd2630fb1e59d6d1178e90e38d852dbb9a727c9f64305e3b68c8a5` | 0 |
| lib/asio/asio/include/asio/execution_context.hpp | 14066 | `a63fcdbb8c5f9572ca008134bc6dffd533b109d7d1f6572503e9d912bd8d7467` | 0 |
| lib/asio/asio/include/asio/executor.hpp | 9982 | `32b1bee40eda5f3f2cfcb517c03bd0113036716749365bb6fdddc474d50accde` | 0 |
| lib/asio/asio/include/asio/executor_work_guard.hpp | 9918 | `03a23819dd26783768d7cc705e86f18213a8aabf581438ca058c6035b602b65d` | 0 |
| lib/asio/asio/include/asio/experimental/append.hpp | 872 | `12aa01364f4ddaf1bdd4cc5cf87d0fa0b46a78e09632ff80fa52f702e32c59f2` | 0 |
| lib/asio/asio/include/asio/experimental/as_single.hpp | 4469 | `2f51c77f0974f2b8b9ce1110b536d86cd7acd8880c56ff7a984d76998a411d8a` | 0 |
| lib/asio/asio/include/asio/experimental/as_tuple.hpp | 888 | `54b06c1130873bc7a1bfc0052845c85de079f110ce32410db80de51e7b983462` | 0 |
| lib/asio/asio/include/asio/experimental/awaitable_operators.hpp | 14987 | `5abbcf8d872e1df5c48538899a077ef45f8d9058ca2729f57012c516744df9ba` | 0 |
| lib/asio/asio/include/asio/experimental/basic_channel.hpp | 14917 | `466ca1ff28be60256a8770f3688d7f2cea3e5ea727dc86445d7855698e988c79` | 0 |
| lib/asio/asio/include/asio/experimental/basic_concurrent_channel.hpp | 15232 | `32d214171976614b2ca2ee7e2c14bb6f1a3e6d4ba88aa5bd1ce25ea5c3f09687` | 0 |
| lib/asio/asio/include/asio/experimental/cancellation_condition.hpp | 4079 | `95bbaf43123ba1a40bdc5a310b6aae96fb589336d82162799662069b1474e6a5` | 0 |
| lib/asio/asio/include/asio/experimental/channel.hpp | 1884 | `e8db96642b8f0da72aa5836a897b0a1b9fb0e5af465e57e21666c65e9648164c` | 0 |
| lib/asio/asio/include/asio/experimental/channel_error.hpp | 1959 | `9f9d9db07f9a98fbf0a5aeb15c7d55efc57fd95de5adf67bc39af7cee462ef9e` | 0 |
| lib/asio/asio/include/asio/experimental/channel_traits.hpp | 7300 | `9b177fafc14498490089f20c6215ae2328edf3916814e23a26621dc69ea5e2a8` | 0 |
| lib/asio/asio/include/asio/experimental/co_composed.hpp | 5194 | `27afa93e267003899a35ff678df202518d66971dac715747ffcd96853582a652` | 0 |
| lib/asio/asio/include/asio/experimental/co_spawn.hpp | 5353 | `fada233d3aee48b17c891a05cc1756620320b29d11505d375789fd3ce747e8aa` | 0 |
| lib/asio/asio/include/asio/experimental/concurrent_channel.hpp | 2016 | `1e41e73c85ab255dfb00dad9517aa6b5a9bbd871a3b315475bdc9c517729d5ab` | 0 |
| lib/asio/asio/include/asio/experimental/coro.hpp | 8144 | `679982aad70863825a7ba23f87af78e96d85a893ea1f738308ad538a4115da1c` | 0 |
| lib/asio/asio/include/asio/experimental/coro_traits.hpp | 6729 | `640d87c900d4caaa212ed804c590ba0c8aacbcc66e55fb7b47fc546925a10dd2` | 0 |
| lib/asio/asio/include/asio/experimental/deferred.hpp | 888 | `f7ae99afd9ee2d73cfa5892e1f201359e59b91fe00ddd44e558ffba1984c5348` | 0 |
| lib/asio/asio/include/asio/experimental/detail/channel_handler.hpp | 2197 | `78fc31f2387fffc19afd2b691e5e108fe1301ac261db838d243a03752cf6e28b` | 0 |
| lib/asio/asio/include/asio/experimental/detail/channel_message.hpp | 2924 | `9736fadff83c3487c3c4aa37155711f3642427fd7ee8ac7fe428df2a44e95953` | 0 |
| lib/asio/asio/include/asio/experimental/detail/channel_operation.hpp | 7761 | `115231d6e5e48b4c1d55c06e152942d5bc8fe02be4555dc3c03012adca66f27b` | 0 |
| lib/asio/asio/include/asio/experimental/detail/channel_payload.hpp | 3042 | `7162ea35b7561cb8ceb091b050f9f3303fd20b2cf442afe034acfcf914608eb3` | 0 |
| lib/asio/asio/include/asio/experimental/detail/channel_receive_op.hpp | 3651 | `04fe8502b5fc4fa96d2fbcf7e7360daeaa25edd0564154f95b739d152026c8be` | 0 |
| lib/asio/asio/include/asio/experimental/detail/channel_send_functions.hpp | 5455 | `9bd8cf6b7a069f4ca9d32ff5c4a9675fff642c64240d5b392e3847d70e2e0be1` | 0 |
| lib/asio/asio/include/asio/experimental/detail/channel_send_op.hpp | 3979 | `084d21271bce4ad169604c0370ded7126b5d36b5018c62acab12716dd965544f` | 0 |
| lib/asio/asio/include/asio/experimental/detail/channel_service.hpp | 19513 | `7b839263f069e4380a419c0e7417d37faf558026e000513cc48f83e3d3cb300b` | 0 |
| lib/asio/asio/include/asio/experimental/detail/coro_completion_handler.hpp | 4233 | `a8428b4f093e8a891a3ae40f2e7a95320f9b4c63011643ca579f853cec2015e2` | 0 |
| lib/asio/asio/include/asio/experimental/detail/coro_promise_allocator.hpp | 4023 | `c56ae3123459f8dabe7b3625c859ae33fcc944f374da164f3573666700d2a670` | 0 |
| lib/asio/asio/include/asio/experimental/detail/has_signature.hpp | 1317 | `043a5cd64ae994d6481fdb7d7f65b1d008aab4aa014ca12d814a35c9328fed25` | 0 |
| lib/asio/asio/include/asio/experimental/detail/impl/channel_service.hpp | 17505 | `b3a315a4d84d44a0eae96b4e28441c03607103000752d0baf39fa076aebb46de` | 0 |
| lib/asio/asio/include/asio/experimental/detail/partial_promise.hpp | 4821 | `3514195a67571d50eabe155da0fa90245a5beddcf184e3c7ce349defbf5427cf` | 0 |
| lib/asio/asio/include/asio/experimental/impl/as_single.hpp | 6658 | `2670b9f201289f42b58e9de0537ed37e817fe5081e1202dd8995cd05b38a58a6` | 0 |
| lib/asio/asio/include/asio/experimental/impl/co_composed.hpp | 34461 | `f860a44ec31a316905ab979087df045e4634052e8fdfe9df6561cad1323bed87` | 0 |
| lib/asio/asio/include/asio/experimental/impl/coro.hpp | 29706 | `d434b249dd752f66f3a5aa3ac45aadace2be1410079e1bb7e417b401eb4bd300` | 0 |
| lib/asio/asio/include/asio/experimental/impl/parallel_group.hpp | 26392 | `fd43f6fc1cb1dda361f6d38c1d6e0d86e50cb7e644737d34b34083f29c07ab1b` | 0 |
| lib/asio/asio/include/asio/experimental/impl/promise.hpp | 6615 | `2b03afca1d066690e36c6bd5725377568926fca7f10114c28bff54c442d45f33` | 0 |
| lib/asio/asio/include/asio/experimental/impl/use_coro.hpp | 7667 | `3f0194770218a68b8bafcce644a79e3f7fa5b4ae5d91f2dcd09222f282edea02` | 0 |
| lib/asio/asio/include/asio/experimental/impl/use_promise.hpp | 1909 | `ba723f138220a1851669df0f76cd05ce8bf04f1ad00913c51fad3262fd762f03` | 0 |
| lib/asio/asio/include/asio/experimental/parallel_group.hpp | 14182 | `dd50a8de3368222e0ba9a2a474fd69ffe15687869adfd620eee66370d7de04ad` | 0 |
| lib/asio/asio/include/asio/experimental/prepend.hpp | 880 | `8b7070a2ab5923e99c0429c6af0f8c52a8661d368aed54f1de4b3fec3d4ce56c` | 0 |
| lib/asio/asio/include/asio/experimental/promise.hpp | 6024 | `3081fd0d704a61ce9508b8780fc0d024ab84fed87fed370891e77af6498bdb5a` | 0 |
| lib/asio/asio/include/asio/experimental/use_coro.hpp | 6138 | `354d8829103dc819325baa52d45619a423802b7d098829e558b26d0a4b684c29` | 0 |
| lib/asio/asio/include/asio/experimental/use_promise.hpp | 3149 | `01af67fed2c14217d90727fd771ef17ec638e5ac405ce8da5fdb9aa347e98bd4` | 0 |
| lib/asio/asio/include/asio/file_base.hpp | 4022 | `bc8041d485ddfa58e61860a08be88b867503dce2881c0350985ae1ed435b4979` | 0 |
| lib/asio/asio/include/asio/generic/basic_endpoint.hpp | 4712 | `31a9648cdffdd415a331ca0e8723ee5a269fa0af4640f7a7a6d1ad2ef2286e57` | 0 |
| lib/asio/asio/include/asio/generic/datagram_protocol.hpp | 3206 | `3637d8df50a01825372ad916e2ab79ee9fcd260ed831e899f59f8548bafa46fb` | 0 |
| lib/asio/asio/include/asio/generic/detail/endpoint.hpp | 3189 | `063a545dae62bfeaac8b3d7d814de48a3671eeaf5f5d23c0cc7c8c3750c3ab02` | 0 |
| lib/asio/asio/include/asio/generic/raw_protocol.hpp | 3066 | `c41fb9bcbf83bb440c6683f3d0079ad35c94058a3e5707161407d33a3db346da` | 0 |
| lib/asio/asio/include/asio/generic/seq_packet_protocol.hpp | 3159 | `fa646ebeca04bb75d36ab3264857cb551b3fcb6174a99d56648d6435dedce4db` | 0 |
| lib/asio/asio/include/asio/generic/stream_protocol.hpp | 3361 | `fa9cf36f1892389140d84ca95686f5e1754ef668de2a55f9b49c1660a430f71e` | 0 |
| lib/asio/asio/include/asio/handler_alloc_hook.hpp | 3348 | `e6ec34d83e1df331a26c1cf58b4cf37e7eb793cabae76b671de857f46e7ddc46` | 0 |
| lib/asio/asio/include/asio/handler_continuation_hook.hpp | 1399 | `99748ce896bb9376fbed44ab41a278d4e616aa5d0a083be809d9a696d746e06a` | 0 |
| lib/asio/asio/include/asio/handler_invoke_hook.hpp | 3620 | `7f047d78f281fe95677739e9ffdbed6ac4535bdd55c69d64546ad14dd90ab291` | 0 |
| lib/asio/asio/include/asio/high_resolution_timer.hpp | 1307 | `56c62d70a38f867bea21cad5cdabf6db97e202b4c65b3e09d7e841ad65b9dbf6` | 0 |
| lib/asio/asio/include/asio/impl/append.hpp | 6790 | `55b3ecda3058d7edd6561c6f2efeb54bcec2a6608a2d79c8382c10ffd1031ddb` | 0 |
| lib/asio/asio/include/asio/impl/as_tuple.hpp | 9782 | `1410333c5373f723e71e11b6004cea177f5a82ba319c8e48e05e5190a9a28528` | 0 |
| lib/asio/asio/include/asio/impl/awaitable.hpp | 30737 | `80d588776cb8dbb003e5ba40b79627b7848ed74689a367b06fc18cce5e9af380` | 0 |
| lib/asio/asio/include/asio/impl/buffered_read_stream.hpp | 16861 | `d6d588f52aa827c43bda1b998c65df29bb9b55723ff5cf2e7c09fffbfa399822` | 0 |
| lib/asio/asio/include/asio/impl/buffered_write_stream.hpp | 16377 | `86070a510225799ad22e3de2ec2f7cdede2280fda8f43eeb12cee7fb86a49cb8` | 0 |
| lib/asio/asio/include/asio/impl/co_spawn.hpp | 11151 | `1062437b5e6b9f16763053ed61f692ccc7334623661f9d6909504897e8c65dcb` | 0 |
| lib/asio/asio/include/asio/impl/connect.hpp | 33497 | `335983a8c80bc0b70ee1ea7b4d9eb7f3a8796cf9529efd88469a72c11aea820a` | 0 |
| lib/asio/asio/include/asio/impl/connect_pipe.hpp | 1736 | `3d5d4b36b91cb93c34757c8139dd3a028c5b59aa350c06c8d8b453e59c7b6c38` | 0 |
| lib/asio/asio/include/asio/impl/consign.hpp | 6146 | `73da48da1973f8d788e790a3cc14d47e7de2a4688456f2dcfa698d90a9811813` | 0 |
| lib/asio/asio/include/asio/impl/deferred.hpp | 5277 | `75c63a6592c48a277d49d8ed8c4d0ea979dcaeed78090d25cedf5e06fd175e3c` | 0 |
| lib/asio/asio/include/asio/impl/detached.hpp | 3100 | `bec7f8ecda73b101a032ab8cf9d5c697a751976f4ff87cd5f9aa78fa1b317d50` | 0 |
| lib/asio/asio/include/asio/impl/execution_context.hpp | 3088 | `c0150f3b9c0100e8e51a7acbd1e08dcdb098559973eabbcfe67c8d72ea4b7d58` | 0 |
| lib/asio/asio/include/asio/impl/executor.hpp | 6419 | `ccf467f34a3ca1c9819824623d547459bd17abeaf4c407994d5a9189b39f6c0a` | 0 |
| lib/asio/asio/include/asio/impl/io_context.hpp | 13730 | `2de9a732084ff8ca7dc4b2779e04899bafad494bcde033e97d057e27ead3dcd9` | 0 |
| lib/asio/asio/include/asio/impl/prepend.hpp | 6813 | `45379d6ec469bb3ea7d7c441595b2eab899a9746651b7248b765e1d5e0d91f9e` | 0 |
| lib/asio/asio/include/asio/impl/read.hpp | 46755 | `b5b8f3adaf044745fbc0e7a368a85a902ab6252775c343afdf3bbfbaeb85ad07` | 0 |
| lib/asio/asio/include/asio/impl/read_at.hpp | 28888 | `72f14012769cdb203ec9c6b2b4c10f55deff4761afc03d5bdee9ae68a0ae64a6` | 0 |
| lib/asio/asio/include/asio/impl/read_until.hpp | 118255 | `4e14de048d3435245c4cce52cfa8f2ed884f4031861fc9316784109a5c2cbaf9` | 0 |
| lib/asio/asio/include/asio/impl/redirect_error.hpp | 18021 | `13304d45bd51f63803ba64ba20578870c14ad5271803140fc1eba3d6a7653acc` | 0 |
| lib/asio/asio/include/asio/impl/serial_port_base.hpp | 1306 | `86998ebf074448bf84f32cce747b549f65a67309a130b54907a3da666548df5e` | 0 |
| lib/asio/asio/include/asio/impl/spawn.hpp | 45413 | `a47407b94cd089722c4931bfc885ab41ca2cbab08ae05eae8248d72b503ba355` | 0 |
| lib/asio/asio/include/asio/impl/src.hpp | 4008 | `61d4c101584057fc6c57e34a854489431db5895a66ae4e09e8f6e638ac1bcd2e` | 0 |
| lib/asio/asio/include/asio/impl/system_context.hpp | 794 | `69ed8a49b65042bba2d061b4873513805f0b9cc3c1d49add53906a98c81a2f6e` | 0 |
| lib/asio/asio/include/asio/impl/system_executor.hpp | 6065 | `54529f27e8b40aab046e93a46b64e9a1eda863e35befa54bad4e099ed26f47cd` | 0 |
| lib/asio/asio/include/asio/impl/thread_pool.hpp | 10523 | `7289906f1554c63f0aafd81f6cba4b8c2e44fc7dcc2c06097426275deda61a9d` | 0 |
| lib/asio/asio/include/asio/impl/use_awaitable.hpp | 8019 | `47714d6e8a03646d5813a93579c4803711e09ef8da1cd15a7cd3ac0744a758d7` | 0 |
| lib/asio/asio/include/asio/impl/use_future.hpp | 26906 | `67ee5a2f50b7a605895c868e2a77dbfb425a52d84abed8b5279d8ecdeddec9af` | 0 |
| lib/asio/asio/include/asio/impl/write.hpp | 41655 | `265e581fdf79e0af01865ea2883bf6a02c9de189838955951987b8b2e9489777` | 0 |
| lib/asio/asio/include/asio/impl/write_at.hpp | 24957 | `2b63b9b3e68aa0a6614a6832ca5732d042e111d574528e111b72c518e11d9945` | 0 |
| lib/asio/asio/include/asio/io_context.hpp | 53037 | `2a6baf0a3faff471c8ae4c215471a0499781f47d8dc22ecd555c38343631d43b` | 0 |
| lib/asio/asio/include/asio/io_context_strand.hpp | 13800 | `e4996365d99bbbbd0d2e76e3456f2229506ae7b829c346841ccbb4270949bb6b` | 0 |
| lib/asio/asio/include/asio/io_service.hpp | 774 | `dee5605037409780d68680363c56fa978060dc4ff5846183431aca6c00dadcdb` | 0 |
| lib/asio/asio/include/asio/io_service_strand.hpp | 551 | `e5c5f8566559033deaa6d526b4ecd5bfb3aeda7ed5944a6d155c60536be8e1b6` | 0 |
| lib/asio/asio/include/asio/ip/address.hpp | 8163 | `7a1d76f3fdae4694962ae5fa9fd94f2a14df878059da19513c536ce67a39f121` | 0 |
| lib/asio/asio/include/asio/ip/address_v4.hpp | 12200 | `a7300552f61f33212dbe129d3b1e78f8b9ea9b17291fb995d493bf1ba6941484` | 0 |
| lib/asio/asio/include/asio/ip/address_v4_iterator.hpp | 4083 | `514bedda6e029c8ef893938ae84808af8fc0b6578505faddebf7a1a48e8b97b5` | 0 |
| lib/asio/asio/include/asio/ip/address_v4_range.hpp | 3197 | `8642ceba7655bb4ac6983e471002e5687511a7d01680d3701831faf5c68ecaf3` | 0 |
| lib/asio/asio/include/asio/ip/address_v6.hpp | 12111 | `bf222ae659b3f669adf6b3ffb0f0e62bb9800f11724e1c17afdd807a42c8f872` | 0 |
| lib/asio/asio/include/asio/ip/address_v6_iterator.hpp | 4425 | `dcfea8ae0bf79aa41581f2097e8e35844ec39659363b58dd1c5732291fa23552` | 0 |
| lib/asio/asio/include/asio/ip/address_v6_range.hpp | 3146 | `2d644e9975c7b843328bc1530576326f0095fe9b16e21976cec5ae392a03bd5f` | 0 |
| lib/asio/asio/include/asio/ip/bad_address_cast.hpp | 1224 | `7247786cb10e3b4b5de5d62d59628fe0574704c27a1c04d326afeba41c7321e4` | 0 |
| lib/asio/asio/include/asio/ip/basic_endpoint.hpp | 7814 | `6159fd3a036752678216b2bf44c476f3a6dcbd54049228c28218e19751ee0d0f` | 0 |
| lib/asio/asio/include/asio/ip/basic_resolver.hpp | 49044 | `cd836a1334eed0299bea09d79afdad07317cdc9511b05f7c4b3d5a9130125653` | 0 |
| lib/asio/asio/include/asio/ip/basic_resolver_entry.hpp | 2920 | `6643c44537e9f5d82fe7261c27b10e16c2267522d3a0526c2ced13dd278fa783` | 0 |
| lib/asio/asio/include/asio/ip/basic_resolver_iterator.hpp | 4987 | `c5d4d287efdf1101593fd2dfbb16445a0003ffe5473d943fd26a436a24ef0828` | 0 |
| lib/asio/asio/include/asio/ip/basic_resolver_query.hpp | 9242 | `63dc4ec8964cd8e8408a26b425443b778319dda63c2901f163ddd7a999194c2e` | 0 |
| lib/asio/asio/include/asio/ip/basic_resolver_results.hpp | 9483 | `e646dc06266fa2c58967df5a3e0f7e965880b749c87239b77b56b609cf3f1730` | 0 |
| lib/asio/asio/include/asio/ip/detail/endpoint.hpp | 3729 | `36648e69bdebfe2211aa2a6d66930b30d22a821a5fba8ab5112371f86c303fb7` | 0 |
| lib/asio/asio/include/asio/ip/detail/socket_option.hpp | 13982 | `aad73f61db6c8b28eac1ba21164ea84b91ebe07136f7219b6a501252db3c3fba` | 0 |
| lib/asio/asio/include/asio/ip/host_name.hpp | 984 | `1932e18cd57f9a7817fda87b20af7b753b0c1907f451450eb81a7ff189a7a87f` | 0 |
| lib/asio/asio/include/asio/ip/icmp.hpp | 2681 | `b84dd85e7ce8dafe5674ba2f8e718719537aad683d2e9716f749546a16fc38f2` | 0 |
| lib/asio/asio/include/asio/ip/impl/address.hpp | 1496 | `535eaa1475dbc7f77f5b92be11956b160371f457453b85c269fd35b5f0845033` | 0 |
| lib/asio/asio/include/asio/ip/impl/address_v4.hpp | 1550 | `e174274840292eddeb235b8fa311176e232ca1154fa6a3e3bafd7f8c408fd95a` | 0 |
| lib/asio/asio/include/asio/ip/impl/address_v6.hpp | 1550 | `533fb2e6c5bc8cc5eab61ca50878008c13738c5bd1ad8fadfb931b40ffd4b9ba` | 0 |
| lib/asio/asio/include/asio/ip/impl/basic_endpoint.hpp | 1133 | `1ae52a46805b5ea6a34325fe7cc44ea813396e180257326ff30361ebb836180d` | 0 |
| lib/asio/asio/include/asio/ip/impl/network_v4.hpp | 1381 | `a73d9aaa64fa2c871ee23ea653f4db82f3a5ee510f8d65bd02bd4aa4650a66f1` | 0 |
| lib/asio/asio/include/asio/ip/impl/network_v6.hpp | 1306 | `783c44ad4b156d65bb638bf12d12ee55dadaaf4d65cc75e744ea67a23d76ad2f` | 0 |
| lib/asio/asio/include/asio/ip/multicast.hpp | 5120 | `86836d51048fbc984aa0aefc1e034881d7213a9ffd3081cf723a1dc8d074ad5a` | 0 |
| lib/asio/asio/include/asio/ip/network_v4.hpp | 6904 | `db6cae5f31613912b90f2f0ab56b25438b1639c590c0067060889f8495c3ec48` | 0 |
| lib/asio/asio/include/asio/ip/network_v6.hpp | 6133 | `45b8500ea8754b4aba4be8ec90579a49f2814ebb8a1fcbff7dee3956c8899e8b` | 0 |
| lib/asio/asio/include/asio/ip/resolver_base.hpp | 3649 | `2ed488ec1250ad3d236adf62bfc4797cadcbe14f957cfc624b2a256ef6edffb6` | 0 |
| lib/asio/asio/include/asio/ip/resolver_query_base.hpp | 1088 | `c9a784faf24f79cc7461a3aae5bdc510cb1fe5defbe58a621a9be8ff899fa438` | 0 |
| lib/asio/asio/include/asio/ip/tcp.hpp | 3673 | `eeceff3517a2c19673a79d78136959533ecfef68a317ea4cce41036467caf9dd` | 0 |
| lib/asio/asio/include/asio/ip/udp.hpp | 2482 | `2008e6ee1b2b574258f0f0bbb9758e432a40d0c515d28001d24d545e03fbe434` | 0 |
| lib/asio/asio/include/asio/ip/unicast.hpp | 1645 | `93dddb7581f776cd03c02d06e25660575ac51c82bbb53a1ff9d5125412abbc6d` | 0 |
| lib/asio/asio/include/asio/ip/v6_only.hpp | 1674 | `3e8ac345977b6c048763dbb583dbdf0e23b85b76ac97170713a78c89505cec66` | 0 |
| lib/asio/asio/include/asio/is_applicable_property.hpp | 1506 | `ee1138774c6820eb1f8568aabfc31ad3c0d78641612ae303af6c9e847e51589e` | 0 |
| lib/asio/asio/include/asio/is_contiguous_iterator.hpp | 1267 | `271f25f400ec15bcbc6e0651d42c6029d81883e47a9ca4da91d70844bc7d9b4b` | 0 |
| lib/asio/asio/include/asio/is_executor.hpp | 1218 | `e54fed98fe8182db69bcc47c0f18f33736ba7060919f42399c830d1f71d173f4` | 0 |
| lib/asio/asio/include/asio/is_read_buffered.hpp | 1553 | `6574e313bdd8ea4921986a7a760756e4eed3bb1e96ee5dfc9c3dcfeff79119ad` | 0 |
| lib/asio/asio/include/asio/is_write_buffered.hpp | 1574 | `5ff4367bd25a05e2169c8954155cbeca59206fdc628b711994ea11a8735f2e28` | 0 |
| lib/asio/asio/include/asio/local/basic_endpoint.hpp | 5782 | `8bce55df8e1c8ba66a27330ab7528d571f00b0bff5695de111deb150554f9267` | 0 |
| lib/asio/asio/include/asio/local/connect_pair.hpp | 3128 | `7653400f3c9faf4f91b7edb53bf1725d7657a81bcba7ab6fac86eee4762ade56` | 0 |
| lib/asio/asio/include/asio/local/datagram_protocol.hpp | 1920 | `ff49abdf81f89a87f636f7061644d6db3c74b5b2651dc54b840c68cfd9829efd` | 0 |
| lib/asio/asio/include/asio/local/detail/endpoint.hpp | 3572 | `c0b7b6ab259512ed3cdf2f96834e4fbc8179c02221e9496d036addd9faaf9b22` | 0 |
| lib/asio/asio/include/asio/local/seq_packet_protocol.hpp | 2081 | `dfa59f698f84b4afffbcef4bd089804af6f70b4379c59fd5ab391631d4890464` | 0 |
| lib/asio/asio/include/asio/local/stream_protocol.hpp | 2241 | `d73c84bd8f5ae74b41ca683e0d379efbdd3dc10592254d8b8466cde85f94613f` | 0 |
| lib/asio/asio/include/asio/multiple_exceptions.hpp | 1496 | `e7cda42c3c067945a15bfd8ccc78befd904f7a046ce71370040e33b9ccfc20a5` | 0 |
| lib/asio/asio/include/asio/packaged_task.hpp | 3187 | `9c2bc4e94e9a7b18154ae662eca32dad28a2baf91da29281f98ab89b35ba2a07` | 0 |
| lib/asio/asio/include/asio/placeholders.hpp | 3915 | `4ce51222d06e79c1f9c0764f96aa8fd74bcc88c1b34cd64ce3d4e71c288d158c` | 0 |
| lib/asio/asio/include/asio/posix/basic_descriptor.hpp | 26178 | `e1a13cf1b5daeec50d7962ee20d941201a919abfa204c7b7e4aab409c533ef49` | 0 |
| lib/asio/asio/include/asio/posix/basic_stream_descriptor.hpp | 21033 | `6aa4bc4645cd50360682b5fe4819c097381ee32f949a98bf69baf6ef2e210393` | 0 |
| lib/asio/asio/include/asio/posix/descriptor.hpp | 947 | `cdae8ca935ea33572e70cc968c6ef98a02ba7423d49523d56441b2daa60d0e8c` | 0 |
| lib/asio/asio/include/asio/posix/descriptor_base.hpp | 2249 | `06d817613e750c1238f23ad55d6b280e0acdb1d5f2d5817b0b3191232309f601` | 0 |
| lib/asio/asio/include/asio/posix/stream_descriptor.hpp | 1017 | `a7f63fb5d0cc70088ab4e2d65d3e6c7f0d0e809f7630ac4ab20c1c525c8111f3` | 0 |
| lib/asio/asio/include/asio/post.hpp | 8159 | `ee124c04f39b4ae54158513d386e6b132d08e448408a5577cf4e790e78e386ca` | 0 |
| lib/asio/asio/include/asio/prefer.hpp | 20756 | `8fffb16a7eec16de512fc83de0558292a15c093b17baf8e6a9f2dab485371ed0` | 0 |
| lib/asio/asio/include/asio/prepend.hpp | 2197 | `3a6c87d424ba7a06f143209c3143102af8d6a48cf53192a3f8b8526e3a3244e2` | 0 |
| lib/asio/asio/include/asio/query.hpp | 8993 | `51e223ae64270a3dad5edb3e70ffe9006c04e03008a6298d77ab1800df71600a` | 0 |
| lib/asio/asio/include/asio/random_access_file.hpp | 904 | `e42d66da25569fec2a41f137bf16e6f954834967f98cbbea77ec96be4cf7993d` | 0 |
| lib/asio/asio/include/asio/read.hpp | 59120 | `c569f5ebec4ad8438be691bb25e4d4f628313b3ac5f0324777cb91b1b71416c5` | 0 |
| lib/asio/asio/include/asio/read_at.hpp | 31137 | `4f2e762b614ef98073ec0d491c72da1e382da72af720deb80527c2fe6a3078d4` | 0 |
| lib/asio/asio/include/asio/read_until.hpp | 129560 | `774f009e0c9ecaa8b406f3cd5b049921a192cd18574aa264a111a04712d48026` | 0 |
| lib/asio/asio/include/asio/readable_pipe.hpp | 859 | `a811559176bfeda569ea2a360c3e6672a182cb4dd1e3daa54931c2c206a1d04c` | 0 |
| lib/asio/asio/include/asio/recycling_allocator.hpp | 3441 | `e0d9ffa909d3cfd282247bfb7e414be9e3efe97b7e495f2afc6c16768a250be8` | 0 |
| lib/asio/asio/include/asio/redirect_error.hpp | 1806 | `dbd52424677d124a346bbf706b3a774e93b4f5ec30590fbe50848049b28204cb` | 0 |
| lib/asio/asio/include/asio/registered_buffer.hpp | 8609 | `4e79766fe308d50c8d021e893b0be2ad17aa14a13ae33a86b651dbe190494f9a` | 0 |
| lib/asio/asio/include/asio/require.hpp | 15761 | `4f4f41f6ec13b48e397770bcb97bb3378ac28a50f8d78cfea15dabdd6cba8570` | 0 |
| lib/asio/asio/include/asio/require_concept.hpp | 10127 | `d892f2162ee541b983c8e37be6523c08a36a7ecf627b948c9d923706b2295121` | 0 |
| lib/asio/asio/include/asio/serial_port.hpp | 929 | `37d46b9ad778044bbc02994d43d3fdb8c7a9de6e555207144a806712df563462` | 0 |
| lib/asio/asio/include/asio/serial_port_base.hpp | 4514 | `6fe09d717af79851f9c5de5f057b33919051fea5d2ac971bbba85b42d6e14b86` | 0 |
| lib/asio/asio/include/asio/signal_set.hpp | 679 | `6780dd1172841a2b2051a5f8881da98a0242485ce04d971e5ded7fc737c76007` | 0 |
| lib/asio/asio/include/asio/signal_set_base.hpp | 4587 | `e6b713e14ef38bdf61ec84464ac6f07ea734e8622b0eaeddb679b5254f555883` | 0 |
| lib/asio/asio/include/asio/socket_base.hpp | 15150 | `659e861b2d0fab853878ef794fc32846e7f63296ce19c161d5bb4fb2ea53bf8a` | 0 |
| lib/asio/asio/include/asio/spawn.hpp | 32960 | `4386a4623c531fb19409356b6e509d13585fafa9a186c0441a543b0ff86591d6` | 0 |
| lib/asio/asio/include/asio/ssl.hpp | 776 | `662fe4697fac4fd243c4ad6b678ce3170a0b06ac6c88c3815e5e2c46e7ec8493` | 0 |
| lib/asio/asio/include/asio/ssl/context.hpp | 25884 | `23a3f1aec78a081710d41b1c19f3b4296a9ae1289989872030c171067cbbcee2` | 0 |
| lib/asio/asio/include/asio/ssl/context_base.hpp | 5339 | `f78c77a9059146beb76a8baf70679f350f8babb7e8e8b91471db1fb326448dcd` | 0 |
| lib/asio/asio/include/asio/ssl/detail/buffered_handshake_op.hpp | 3291 | `eb54085ef7ad911149ba68681d4b75bde4197872cab2030a2f122741af553950` | 0 |
| lib/asio/asio/include/asio/ssl/detail/engine.hpp | 5859 | `bf85a27d0b62654815c5a6ba5cb63b9b006cbfd3642dd0c0f27f95d2951a697a` | 0 |
| lib/asio/asio/include/asio/ssl/detail/handshake_op.hpp | 1447 | `4b76b5ef23813654a2e2a30b7e6f7c4f4c69f5655e3dcdf45cc9556b2a1490b2` | 0 |
| lib/asio/asio/include/asio/ssl/detail/io.hpp | 13653 | `edd518491af29362c5f10d26f40b913f44c7a675ffde0e85cdc5ba46613cc38c` | 0 |
| lib/asio/asio/include/asio/ssl/detail/openssl_init.hpp | 2922 | `2fd0e62e8639b68b077f102d084d4fc543a91abbdbe1f2514e49842a10c3aef6` | 0 |
| lib/asio/asio/include/asio/ssl/detail/openssl_types.hpp | 996 | `1ee31d51a8c3070a6a91193abacf8025190e1e157e2be02d635e2a70fc372849` | 0 |
| lib/asio/asio/include/asio/ssl/detail/password_callback.hpp | 1431 | `e66c8ae47d7e00ab3dbda5cb3d3423d861a9986650feed483604000beabbf206` | 0 |
| lib/asio/asio/include/asio/ssl/detail/read_op.hpp | 1687 | `599698a7a68422d3e17f8d07c7a64a6d0540bb9a03bb033b278d3a97c6329bc9` | 0 |
| lib/asio/asio/include/asio/ssl/detail/shutdown_op.hpp | 1673 | `7f22d15a794e76c35cfe744fb4125f3b5559cc89f37c3fdc270935956b246ecd` | 0 |
| lib/asio/asio/include/asio/ssl/detail/stream_core.hpp | 6782 | `b0116bb0ec1557aab6e3cf50de16b7ba80c907cee692f052c26dda5111205a05` | 0 |
| lib/asio/asio/include/asio/ssl/detail/verify_callback.hpp | 1311 | `bcb551b2e8bfef6c202817d75e770e29ed19eefb669ce7d7c9b5ea0be5540e80` | 0 |
| lib/asio/asio/include/asio/ssl/detail/write_op.hpp | 1862 | `b1f382b4f532cbc4dfa58b27cd1be976e000d4a986b895455fabf572b205bee1` | 0 |
| lib/asio/asio/include/asio/ssl/error.hpp | 2889 | `bded604e39862709747d7f0869f511e5a5031a3bd156e17005be030788067b60` | 0 |
| lib/asio/asio/include/asio/ssl/host_name_verification.hpp | 2554 | `ce39cdf2396f64f6bef75d1526c6bcd18c275e91787f56f7c5b4d67f450eef8f` | 0 |
| lib/asio/asio/include/asio/ssl/impl/context.hpp | 1798 | `43cdbad697b5d9d85e9a93e7010a1ae480c9055ef3b27419785ccf4808ba8c0b` | 0 |
| lib/asio/asio/include/asio/ssl/impl/src.hpp | 812 | `111c79f43a5cf796bd998f1080be4d5f1362bc2e28a871ea02c579e74c0933fa` | 0 |
| lib/asio/asio/include/asio/ssl/rfc2818_verification.hpp | 2830 | `4bf36b999181f311a59c8eace5f5bc7fd1d6dbcd445403a7df8d974ad7f597af` | 0 |
| lib/asio/asio/include/asio/ssl/stream.hpp | 37372 | `e1f0aaeec99bc37ce9092c47e2988d2a679bc92bad684cde2b1e78bee68fc09e` | 0 |
| lib/asio/asio/include/asio/ssl/stream_base.hpp | 1142 | `913345b66d14d56c8b9b6671aae83c9d3a638ea11d8a2fbfb57253722252dd35` | 0 |
| lib/asio/asio/include/asio/ssl/verify_context.hpp | 1658 | `22dd4982c1534953525fedb9b3bf17eff582ce043baeec020343a1f577a2bb01` | 0 |
| lib/asio/asio/include/asio/ssl/verify_mode.hpp | 1677 | `a4f6575aa35d0ff92bb7aabd08918fc6149d27e19d9402bc600560519da2eaf9` | 0 |
| lib/asio/asio/include/asio/static_thread_pool.hpp | 745 | `cb00be497d4273fdfeb6bc68eb86f865df55257ab59484a72ab4cfffb0b0b1e1` | 0 |
| lib/asio/asio/include/asio/steady_timer.hpp | 1219 | `41c043622b733c375e140b845b5115dce3305cfd8dc9fefc6f512b1a24bb37bd` | 0 |
| lib/asio/asio/include/asio/strand.hpp | 18360 | `b49cbb63e639182fe8fc561cb8d867501d25a74eff658426cb7de04d35f97406` | 0 |
| lib/asio/asio/include/asio/stream_file.hpp | 850 | `0f93d7bc42c846054503114bd1d2417ea64844852b38fc1343d514413e621c4e` | 0 |
| lib/asio/asio/include/asio/streambuf.hpp | 745 | `e8893c501bf10c46cc4278ce79896873736b7532c4898cb2ebd696079a5923a2` | 0 |
| lib/asio/asio/include/asio/system_context.hpp | 2478 | `1aca6b6794eb5f63c0af370188ea72e92f77d13d097fec815de219d58aca0fb0` | 0 |
| lib/asio/asio/include/asio/system_error.hpp | 2881 | `480fb7367a0eb008323ffd012123732687f83eff8f7a69604003e127a0cfe15d` | 0 |
| lib/asio/asio/include/asio/system_executor.hpp | 21544 | `4d257a6c45fb806a37265c54abadf20abdd671fffe70a33f29eb89f2e7f51c16` | 0 |
| lib/asio/asio/include/asio/system_timer.hpp | 1219 | `7ce8daf30278adcf7a923804e46a0719313b5d48fc9db17825d3a2f2fdac04d3` | 0 |
| lib/asio/asio/include/asio/this_coro.hpp | 7559 | `b94d763105cfb68dc2f199cbc5040a9c29b40c8d31fc2fd7174be55125e589aa` | 0 |
| lib/asio/asio/include/asio/thread.hpp | 2309 | `8b793f5603f61c2aad389f77a8077e667905784454e767524208b053cf5a5d46` | 0 |
| lib/asio/asio/include/asio/thread_pool.hpp | 36326 | `45fcdf7cc3b7d97ac3301d52c17bfc0b9d28fde4f9ade9180ea18a59c9cac02d` | 0 |
| lib/asio/asio/include/asio/time_traits.hpp | 2194 | `44529149b42e161021f24676355958e38e4dd04e3b6b72cfb5f80dad4d763aeb` | 0 |
| lib/asio/asio/include/asio/traits/bulk_execute_free.hpp | 3127 | `b5cfc58a67b52757714e512b2d2ef1653ab01ccc9879d040a8e80242a9fcd19c` | 0 |
| lib/asio/asio/include/asio/traits/bulk_execute_member.hpp | 3170 | `d844795eed30f0387f93f4d3e1a7a18a6484ddabe359fe10a5dcbccbef46eed8` | 0 |
| lib/asio/asio/include/asio/traits/connect_free.hpp | 2776 | `1f4674499b7a89016c89d4006c62df4d62e9ea69ba4b4820c22634d91b91129e` | 0 |
| lib/asio/asio/include/asio/traits/connect_member.hpp | 2819 | `337892289dd5a5d3cdf3f930634ebe7747ff61ca69015f49c3efcc430be095f7` | 0 |
| lib/asio/asio/include/asio/traits/equality_comparable.hpp | 2648 | `41ef8f4f21efad616ec7133537ef8f4931206fa03832b795d83b99574279150e` | 0 |
| lib/asio/asio/include/asio/traits/execute_free.hpp | 2600 | `427680babd15fa296ea45194d9f0b104e88a44681ae3f4a9367325dba930d4d2` | 0 |
| lib/asio/asio/include/asio/traits/execute_member.hpp | 2641 | `8bea3ea11640ceeb94b8bba8cf72dd230830ee8062942cdc26bb2677df928847` | 0 |
| lib/asio/asio/include/asio/traits/prefer_free.hpp | 2687 | `b731b81b91aca5c8e9ed894b1245a0c7d452ee95fffbf81b34604c761a044875` | 0 |
| lib/asio/asio/include/asio/traits/prefer_member.hpp | 2728 | `db6455a3d3d7d47dcae85ac5319772ae4a4233d1f96463f8dfef35991a683fd1` | 0 |
| lib/asio/asio/include/asio/traits/query_free.hpp | 2662 | `e45de11d01d945014674c59d44532ab9ed7c1a21185bb65c2a94636992078674` | 0 |
| lib/asio/asio/include/asio/traits/query_member.hpp | 2703 | `c46295c424a6670fbd25fbc24f0a225f758e03ebe86a046ffe880ae73453eaff` | 0 |
| lib/asio/asio/include/asio/traits/query_static_constexpr_member.hpp | 3063 | `ba448eab090cadd594c0910f67b800df033beeb7b783f200bb55250d2d0da790` | 0 |
| lib/asio/asio/include/asio/traits/require_concept_free.hpp | 2912 | `288c366fe90f557f1fec7a103daded2e224b126aee12d4110c05db7fbb0fdc67` | 0 |
| lib/asio/asio/include/asio/traits/require_concept_member.hpp | 2953 | `35ae35449982fcad06df8fdaffa4d0cacc37679b0c35e631bc0e2349de9cb510` | 0 |
| lib/asio/asio/include/asio/traits/require_free.hpp | 2712 | `0c6796a90fd98d8fe777edc06da5bc03b2ef2af176b4bc3140ce8234c23a2398` | 0 |
| lib/asio/asio/include/asio/traits/require_member.hpp | 2753 | `9f7f2954dfca9dccfb3023ece668a9258470be5a0b48b809f37efefbe83513bb` | 0 |
| lib/asio/asio/include/asio/traits/schedule_free.hpp | 2568 | `4d9cad5b2b31ff06392d61a24529f034dd0213f8eb473f302bdeed8b248770c0` | 0 |
| lib/asio/asio/include/asio/traits/schedule_member.hpp | 2617 | `07caf3d137a7d7e6824cb6f7981f82d3f6076b0e74566456c4120e9cdb2b2e40` | 0 |
| lib/asio/asio/include/asio/traits/set_done_free.hpp | 2568 | `013127e1a82f36528c6b8bcdab42ece5306428b05ab88c6b29e35d5485f7471e` | 0 |
| lib/asio/asio/include/asio/traits/set_done_member.hpp | 2617 | `290e6d54ff5e95ad990b128517a52a5989cbe3f387446d08505f05b84167e5b4` | 0 |
| lib/asio/asio/include/asio/traits/set_error_free.hpp | 2828 | `169ebde0be357c03a3998a712d4dfbd34014768591de1e5e85ab273d0503a8fd` | 0 |
| lib/asio/asio/include/asio/traits/set_error_member.hpp | 2871 | `a23b161f7ff617aa51cfe7771ec163137bec633f9b9b46d830313304603be412` | 0 |
| lib/asio/asio/include/asio/traits/set_value_free.hpp | 7167 | `a09a45ea4dad2d7336ee3e7b00147cc4c6a78370ca03506794811eada180a20b` | 0 |
| lib/asio/asio/include/asio/traits/set_value_member.hpp | 7236 | `2f8370e6afb761f316b304f50aa304a021aad4d53d8ba93c789112dc84293bdc` | 0 |
| lib/asio/asio/include/asio/traits/start_free.hpp | 2490 | `d9e3134326dc96f1a9da6c4b090757d278572a37cd43790dd7b405ec160a7dbe` | 0 |
| lib/asio/asio/include/asio/traits/start_member.hpp | 2539 | `de7c884a2bc65fa7b0412326b3297c5edcaacac0e3a6c320eba86cf5da887150` | 0 |
| lib/asio/asio/include/asio/traits/static_query.hpp | 2878 | `dbd83fbc0154d13e2b0c083c5d7a77638ea804411fd6f06e13c3ae8b1f24f62c` | 0 |
| lib/asio/asio/include/asio/traits/static_require.hpp | 3166 | `43f38d49338b2313ad1b2e9616e60fae3b8214d25ce5967db7c5e2a4a2dbd7c0` | 0 |
| lib/asio/asio/include/asio/traits/static_require_concept.hpp | 3368 | `a34a0d7e94efe05fe9d972a88a7abefa176a7e40a4d27e363b66f1da06619b55` | 0 |
| lib/asio/asio/include/asio/traits/submit_free.hpp | 2750 | `28c1b0cfd8ef1ae051012b4d6399910223c89d7341a907fb9203cb45d75123c1` | 0 |
| lib/asio/asio/include/asio/traits/submit_member.hpp | 2793 | `5ab49ac3bceaeb6d60db5be9da333a48b687d47dacb4cfa14bdb06ad96dc4f82` | 0 |
| lib/asio/asio/include/asio/ts/buffer.hpp | 623 | `97fc06463d5076b1682ed66a318c076254b9c4f24850f7e86c5858a65058d8da` | 0 |
| lib/asio/asio/include/asio/ts/executor.hpp | 1014 | `ef904d562dbcd2001a75d32dc4d13fc1af7658d613e80c3416bb318f896eb5e3` | 0 |
| lib/asio/asio/include/asio/ts/internet.hpp | 1249 | `fe15bd419d385c45d0b6e95738b9f34c84d68c406ec03b7a2737ec78e0fb0770` | 0 |
| lib/asio/asio/include/asio/ts/io_context.hpp | 524 | `3a9d9f6eee7b788aa581c554874e370100ac9b936a485df88a00c32ed154ba91` | 0 |
| lib/asio/asio/include/asio/ts/net.hpp | 675 | `408a7c2ad0022dca038aa8b53760d2bc73e2a7a19f5711b0c23c7cdfd6dfc6f3` | 0 |
| lib/asio/asio/include/asio/ts/netfwd.hpp | 6334 | `b5bdd09212486a16483147dcd09ff99a6b02433d160fd9abbc7d058b12e60435` | 0 |
| lib/asio/asio/include/asio/ts/socket.hpp | 775 | `628758015b1370dc34c0a89ca367be9c8fea5ffa779520a307bff8f9b26c77c1` | 0 |
| lib/asio/asio/include/asio/ts/timer.hpp | 684 | `a2905a12173129b0af75c3126e12d93faa9b548025f1042ef3d06788457db179` | 0 |
| lib/asio/asio/include/asio/unyield.hpp | 381 | `c7d363874ed861eb0fd82daa710b5b1e8ac52965ffa463e4dec6a0ac113a72b1` | 0 |
| lib/asio/asio/include/asio/use_awaitable.hpp | 5453 | `1eeb3402aa8b97ef50b185475d601ebd122890642470838b57ccbecf43586606` | 0 |
| lib/asio/asio/include/asio/use_future.hpp | 4752 | `56438f47479d6e73db2e1e8e2d7467c8cec25ac7ed88a3e8ac7306f6734c839b` | 0 |
| lib/asio/asio/include/asio/uses_executor.hpp | 2229 | `835da053b4ce1627c90b626dcee8293ec27da959779dee51f110e470f076c8a4` | 0 |
| lib/asio/asio/include/asio/version.hpp | 644 | `b0166135691caa37cc5023924646f67c96c82b4c5af6eb55c081e4aa63be1721` | 0 |
| lib/asio/asio/include/asio/wait_traits.hpp | 1382 | `66e374ee8900c8eb216b61e2c6b0bdc438ac124a960ea5e3eee230a61aa86471` | 0 |
| lib/asio/asio/include/asio/windows/basic_object_handle.hpp | 15959 | `54e5c6db9daa46264c48208f605443dadc19f1542d1fd1070ff5924fcc79be4c` | 0 |
| lib/asio/asio/include/asio/windows/basic_overlapped_handle.hpp | 15108 | `a3d645786dedfa0e2addd501e87e1954549eb0d5f039a1691c444af02bea3d44` | 0 |
| lib/asio/asio/include/asio/windows/basic_random_access_handle.hpp | 21580 | `a577b209f79fdb2863f26a1165a6c5dc7c82cc74cf2075b8cc753f5b3b1bd0a8` | 0 |
| lib/asio/asio/include/asio/windows/basic_stream_handle.hpp | 20307 | `b606f1ed263353d294fb1064b2ebbc4c3ea43bb1aa85e072f8bfe5e3ee955d17` | 0 |
| lib/asio/asio/include/asio/windows/object_handle.hpp | 1044 | `bf98a29ec569daf015fa31eeb56f2720b7ecb0f94abd6ea3090331544ef3ad0a` | 0 |
| lib/asio/asio/include/asio/windows/overlapped_handle.hpp | 1137 | `256bc2562cb39bf3c48963a34f5256459c253ca0612351d552c36ef0c840c752` | 0 |
| lib/asio/asio/include/asio/windows/overlapped_ptr.hpp | 3904 | `c1d4cbebc0bc99b22b40c7b048f6698a02b40b59ce3d7aa5c3fae584842583d4` | 0 |
| lib/asio/asio/include/asio/windows/random_access_handle.hpp | 1061 | `6228a63ad3a8cdbfc294838ca49f176685f339d4cbaa313c3efc52dc5f607ef6` | 0 |
| lib/asio/asio/include/asio/windows/stream_handle.hpp | 993 | `416bb40031f4bfa0d727b9ce5bb08cb64a2f77276b630ea1c297463aa0ef826b` | 0 |
| lib/asio/asio/include/asio/writable_pipe.hpp | 859 | `4189c8b01ed0a07bd70e9890ee4c47bb3fd56304a878cc432d6c6765ed3396d0` | 0 |
| lib/asio/asio/include/asio/write.hpp | 58660 | `0df3bfc48643d89026b4de2d841c4e6789f702cf946d21d7527258905c335e45` | 0 |
| lib/asio/asio/include/asio/write_at.hpp | 32957 | `1dfcba7713e8bd62facd3d374966deee4fe1af5a37d5d98e655f6ca1141bea48` | 0 |
| lib/asio/asio/include/asio/yield.hpp | 464 | `501b82d007133d18b9b597b9205fa57f3df241e747247ded269617e2b831cfff` | 0 |
| lib/asio/asio/src/asio.cpp | 298 | `8812b49e483c1cf3b1f956767ab95718d312301170c16baa8a17e680837f2fb0` | 0 |
| lib/asio/asio/src/asio_ssl.cpp | 310 | `6dbea4e325ed02daed10a6b00877f6472437cd97fa6a73b55e2f0250caa79243` | 0 |
| lib/cereal/include/cereal/access.hpp | 14838 | `84f8e157ab247dddaf4ace33602d0b2d152bb922e5c614d0b359b7242bd5255e` | 0 |
| lib/cereal/include/cereal/archives/adapters.hpp | 6052 | `920019e4682edb7db3c20470a17b74d28eb1749491ee94d805e5df8443d7bb1b` | 0 |
| lib/cereal/include/cereal/archives/binary.hpp | 6778 | `23c3b0956594b49820ec91a5296539ac2e25a41270299874a00e099395fd6ba1` | 0 |
| lib/cereal/include/cereal/archives/json.hpp | 43989 | `f31a678dcc961ee741b4eec9b83c694ef908762ae763310df9b68420dda8d9a5` | 0 |
| lib/cereal/include/cereal/archives/portable_binary.hpp | 14798 | `aa01f981eac16a23de9718064fa9bbb8feedac296ee17fdc1601ae43c99dd366` | 0 |
| lib/cereal/include/cereal/archives/xml.hpp | 39089 | `55f8bfb6ab516e8b6eb7462ad71b2007e19e44c6f9b488b95ded46fdd49b6013` | 0 |
| lib/cereal/include/cereal/cereal.hpp | 47239 | `036d721d6fc8b84cfc8056b7b24d237431a17822a3f7e5b137789cae7e424a27` | 0 |
| lib/cereal/include/cereal/details/helpers.hpp | 15948 | `159e79148bdc5c63a01d0769161b2c46ac54a9ce1d16206566753ce7ac46b0b9` | 0 |
| lib/cereal/include/cereal/details/polymorphic_impl.hpp | 38789 | `19f77498793137218172c22b670dda993d9c27cf11ca75aeff6f411c1f38e0db` | 0 |
| lib/cereal/include/cereal/details/polymorphic_impl_fwd.hpp | 2920 | `0423ead989c6ab472e4c7473376d95ca7be46771695706ff7a290e0054aa1ad1` | 0 |
| lib/cereal/include/cereal/details/static_object.hpp | 5001 | `a0c20289499e3c6db3476c8013f34a92887ad575c2d7bed5a8bda3fd152e4069` | 0 |
| lib/cereal/include/cereal/details/traits.hpp | 96686 | `89ec46a466a0d21be3df9b72367ba18f24c44477996e494a674c5024549ad29c` | 0 |
| lib/cereal/include/cereal/details/util.hpp | 2949 | `463063f82172a5c96858998fa708e43c34adf226817c9e765ed439cb821994b6` | 0 |
| lib/cereal/include/cereal/external/base64.hpp | 4446 | `d9e523e8736ac0c68064c7ad312a222f285e82bf6c96a1b1c2cadaffff9fc64f` | 0 |
| lib/cereal/include/cereal/external/rapidjson/allocators.h | 10815 | `eb14a98d27a20e9381b07a0bc86aeb0845f079f2f896085a673eca6d8e3dd0d9` | 0 |
| lib/cereal/include/cereal/external/rapidjson/cursorstreamwrapper.h | 2365 | `793a239a7841ad102b77526af87d5c37e6ea6e338a5c5bd31dfb7adedea40ce3` | 0 |
| lib/cereal/include/cereal/external/rapidjson/document.h | 120119 | `8b8701b7a383cd6f41711fc91b007e52a05aaee5ff0f76a43d8fa93397995078` | 0 |
| lib/cereal/include/cereal/external/rapidjson/encodedstream.h | 10989 | `410c0fe9f778b5181f9e00ca4f77a107421e7ca2ae443335a153cf7929acb619` | 0 |
| lib/cereal/include/cereal/external/rapidjson/encodings.h | 30191 | `f753db0a026aa3450dc2c1e9dded09a69fc24d2f2bfd704b40cc316912ca8114` | 0 |
| lib/cereal/include/cereal/external/rapidjson/error/en.h | 4080 | `8f657ee931628041ef48e9dd293570f9159a0730ad60da9dee21474a5caf7329` | 0 |
| lib/cereal/include/cereal/external/rapidjson/error/error.h | 6374 | `4ac2adbd9c73b797a8e559dd7ba950c90b2de6296e7d9e84c3b69b4bd0877a25` | 0 |
| lib/cereal/include/cereal/external/rapidjson/filereadstream.h | 3113 | `d2bf436769cb26408022bbedc78b7ca3a0ab96c5246ee480f96f64a44f581695` | 0 |
| lib/cereal/include/cereal/external/rapidjson/filewritestream.h | 3244 | `f5da171cec98e3f5e3d8ce37aee268ec56a6cb46ffca21dc2d758a5f9ce5ff27` | 0 |
| lib/cereal/include/cereal/external/rapidjson/fwd.h | 4070 | `fe1bace06c3940c8797163d0be9ad62ce4f90e8a14dcd2a6cbc3eba0dc703020` | 0 |
| lib/cereal/include/cereal/external/rapidjson/internal/biginteger.h | 9218 | `6125cc192f0794c489544063d26984b94ec994893057c0042695b185fbfc2449` | 0 |
| lib/cereal/include/cereal/external/rapidjson/internal/diyfp.h | 12730 | `1e6db0146303f9bfe5491206c836168b7cd02c8e0cbe36fcdcb8f8c8be9e20d0` | 0 |
| lib/cereal/include/cereal/external/rapidjson/internal/dtoa.h | 8195 | `5163fd73db7baef87775d6291a8621896716f9bca7ac3abc216f5244923399e1` | 0 |
| lib/cereal/include/cereal/external/rapidjson/internal/ieee754.h | 3064 | `bef58c98f4afebb4a0698100cd9382fa4f11ad70d5a30c9caf261834be9bd517` | 0 |
| lib/cereal/include/cereal/external/rapidjson/internal/itoa.h | 10194 | `a75c5124883c2b1fcd9cd22fe26018dd1f87562861375e38d12dfa2d4564c153` | 0 |
| lib/cereal/include/cereal/external/rapidjson/internal/meta.h | 6879 | `a4d54e394c8a0a60b78847561d8d1870ff4f6d9937d3244868e75d385d6cc76e` | 0 |
| lib/cereal/include/cereal/external/rapidjson/internal/pow10.h | 3637 | `519cb36fe6d814bb547d296790d3be05de93f2c20436fd106c29da47faa19140` | 0 |
| lib/cereal/include/cereal/external/rapidjson/internal/regex.h | 26328 | `f6060164f0211eb4b26f60323d2c90aaa188c5c4557b10c66f6e5f3eceee34bf` | 0 |
| lib/cereal/include/cereal/external/rapidjson/internal/stack.h | 7345 | `2fb94522d0d92c0e3f73a37d6a6ff5d3b15af4f47c8712dd8d1ce9c10c0c6497` | 0 |
| lib/cereal/include/cereal/external/rapidjson/internal/strfunc.h | 2255 | `868e6f116d24d64f7c32f6d1c757dd9f13789987c2f490306b95d1930c292f7b` | 0 |
| lib/cereal/include/cereal/external/rapidjson/internal/strtod.h | 9155 | `de2fab5037ef80a11ee2d705f3d9dbd2595d5dffc10a776a7e00d5a7b3a67238` | 0 |
| lib/cereal/include/cereal/external/rapidjson/internal/swap.h | 1482 | `8820d72c714950ece7f2ceea046b93a246701bd87a45e4ba87f2f484f5b7c4f8` | 0 |
| lib/cereal/include/cereal/external/rapidjson/istreamwrapper.h | 4187 | `75c60a5a0921adcc50cd41f21475a278769f7ad600dddaa62fdcf634b855eed1` | 0 |
| lib/cereal/include/cereal/external/rapidjson/memorybuffer.h | 2595 | `bf9f69b1cc71e1691c0a0a35b88678f915b30dca3d2a1e59459cfa8d4a90344f` | 0 |
| lib/cereal/include/cereal/external/rapidjson/memorystream.h | 2772 | `4e749970cab7a05b3b0b08865bece11dcb320afa2c8340ca5d8c300cf708ebce` | 0 |
| lib/cereal/include/cereal/external/rapidjson/msinttypes/inttypes.h | 8372 | `78ee41fd99bcbe59ca93f6a870a83c0a90f4b179af571f6e684f2600491bbae7` | 0 |
| lib/cereal/include/cereal/external/rapidjson/msinttypes/stdint.h | 9386 | `bf2d1bc4885bc1e0720ec9af8f399477c7e105ae1e70e2863c31a8123cae1c17` | 0 |
| lib/cereal/include/cereal/external/rapidjson/ostreamwrapper.h | 2422 | `63007f4cd68260f2b70438a1b9840f1ef250570537d0db457e67b9c5d96c97e3` | 0 |
| lib/cereal/include/cereal/external/rapidjson/pointer.h | 61159 | `158b95272ae25a49d51e23a473090ba14f87e27fabe629e624e98e6df588a93f` | 0 |
| lib/cereal/include/cereal/external/rapidjson/prettywriter.h | 10703 | `4a61f6bd5d0c4f8ee2bf8c31d978c4e648e665be66ad353312c0dbbaa1710599` | 0 |
| lib/cereal/include/cereal/external/rapidjson/rapidjson.h | 25306 | `7fb69c707f0ed3a8b59b8f949f0928a9cc06d67bc15d599094693703ff70ea26` | 0 |
| lib/cereal/include/cereal/external/rapidjson/reader.h | 95072 | `6132690caf458c9090464cd73dbc722a29b4c71376d5cdbe2e08c57bc4cc1a76` | 0 |
| lib/cereal/include/cereal/external/rapidjson/schema.h | 105031 | `b41191ead411ccfe7eb92ab4b66eaf977a04fa84754bc587d33a1186040f1c5e` | 0 |
| lib/cereal/include/cereal/external/rapidjson/stream.h | 6851 | `6d1db24b952df2c93bf1c435df21450c1c59f42741dafed50141a95eda8dbe77` | 0 |
| lib/cereal/include/cereal/external/rapidjson/stringbuffer.h | 4063 | `ae4940dcdd29aedbe3447bc81f41b588be9881d348826f643bb78ad9e0e72fbd` | 0 |
| lib/cereal/include/cereal/external/rapidjson/writer.h | 27313 | `535a55d135725981228b72c63e3afcd5f792a07d7b3eb7940298473d763c0019` | 0 |
| lib/cereal/include/cereal/external/rapidxml/rapidxml.hpp | 119560 | `20611c23efc929e0794fcd54437b24cdce5902cb172c472262c911db3ae495e2` | 0 |
| lib/cereal/include/cereal/external/rapidxml/rapidxml_iterators.hpp | 3862 | `74bef669d62a59c0141fe768c8f0394eb8c37b420b2a9cd7b043ca1bbf26ddd4` | 0 |
| lib/cereal/include/cereal/external/rapidxml/rapidxml_print.hpp | 15689 | `e7d1d27cf94ff243ec120f881f76ceae4c8998d3036410acbadb6adef1328eee` | 0 |
| lib/cereal/include/cereal/external/rapidxml/rapidxml_utils.hpp | 3324 | `eec25cd76a5a39e98467e5441d9e7bd84a373c7420f0b5149374743fbf7a634c` | 0 |
| lib/cereal/include/cereal/macros.hpp | 6713 | `675f9f17f55b2af6245410317dc3add11a6f84bd935e549d4c2419b7a11b9d30` | 0 |
| lib/cereal/include/cereal/specialize.hpp | 6614 | `768135f2bb12eee8053f02cc1aa8d18e7b611764257dc28a56e1781c193dc96f` | 0 |
| lib/cereal/include/cereal/types/array.hpp | 3519 | `cc739bbc199a7bce951d9ef862b772976bcd9c2ae2cb99ea436d12cb2f9030b0` | 0 |
| lib/cereal/include/cereal/types/atomic.hpp | 2327 | `1f60d6304767f6783f265d49634a866c6334123e9ab7777f282ecee49d56044e` | 0 |
| lib/cereal/include/cereal/types/base_class.hpp | 7571 | `c292e890fd712a14d9e8a917c715b7a6b654dbe23b272ae1fbffa4f36574109b` | 0 |
| lib/cereal/include/cereal/types/bitset.hpp | 5473 | `79e4a87d7a8301ca1166a5027db7079c8510499cb73cc182038d04f475bdde36` | 0 |
| lib/cereal/include/cereal/types/boost_variant.hpp | 5563 | `d224529813dbc141cee2ee8164a811eae1b5864df657ec1152df9b61ef5cfe21` | 0 |
| lib/cereal/include/cereal/types/chrono.hpp | 2917 | `496099bf0db6591e94feee6efd507fbee9df1a590a18e034ee137b4da1a97fc8` | 0 |
| lib/cereal/include/cereal/types/common.hpp | 5394 | `092612375d40b8e1bf7995b360b7e7660f276605958fe819abed82a6ca654db8` | 0 |
| lib/cereal/include/cereal/types/complex.hpp | 2393 | `d562f9728f17dc682067185b4222e41b87c3309c436169444d191649369c58cf` | 0 |
| lib/cereal/include/cereal/types/concepts/pair_associative_container.hpp | 3228 | `b7b625f739dbf2068c76d264fa52daa1922cf1423d50f2e867f1e1510ff217fa` | 0 |
| lib/cereal/include/cereal/types/deque.hpp | 2466 | `c08285dcb404c881f1c94ee475e62f7f25da8590c659b6b155c3f3f568aace05` | 0 |
| lib/cereal/include/cereal/types/forward_list.hpp | 2904 | `977a07fb199e2ac28979a903d648962dfd2b5a853e304919156c6ce3346e171f` | 0 |
| lib/cereal/include/cereal/types/functional.hpp | 1993 | `f1d748ded8612b93d2d0ac7fc6fb249ec8e8062c42a59c2587a753edf0adaefc` | 0 |
| lib/cereal/include/cereal/types/list.hpp | 2450 | `62f5d62bbe5c93548b845b6972da9fd02cf087a66fddbddfee4c26d6a91a721f` | 0 |
| lib/cereal/include/cereal/types/map.hpp | 1851 | `85a7183f897f0c1697223e95a47eacf287a7cecb5ff15a1f6edddb909ec85b2b` | 0 |
| lib/cereal/include/cereal/types/memory.hpp | 16858 | `8c66bfbafd7866897748515ca96f3926d8a1b4f0a3aaf04eafdcc94d6e7cb7e6` | 0 |
| lib/cereal/include/cereal/types/optional.hpp | 2553 | `cc3842be869eae114bf921ef47f5365326d337ad40c6a950f2d6fa6f846ae164` | 0 |
| lib/cereal/include/cereal/types/polymorphic.hpp | 22354 | `caa1f76bad93fd0782cd5a6de57c6b562d767dccef815be0f1582d8003fbeeb1` | 0 |
| lib/cereal/include/cereal/types/queue.hpp | 4779 | `8e418478b4fa64411474df32f73780d9cecc1d73c6f461a1aa95e48a953e7b5d` | 0 |
| lib/cereal/include/cereal/types/set.hpp | 3566 | `10e03c04ce8da2a7d915a9e42e698c01d844766b836ba5ff1d5203d505b5549a` | 0 |
| lib/cereal/include/cereal/types/stack.hpp | 2898 | `c8e62e2474a8834780be757017a3d104307f7aca2ed46fcc2f4523ea6f6a43a5` | 0 |
| lib/cereal/include/cereal/types/string.hpp | 2953 | `473ff82531599b7df54c368a884ec1b388262cdb59b68e3325bfd19a64a72e7f` | 0 |
| lib/cereal/include/cereal/types/tuple.hpp | 4651 | `d1e0741be9e9f911dffb1a17f01113502373b0bbdb00f35ffcc053452c510e85` | 0 |
| lib/cereal/include/cereal/types/unordered_map.hpp | 1911 | `682bbddfdd7b7ebfc6c57f70eac0a3179cb897762b0c9f182c8b0fd6362339ce` | 0 |
| lib/cereal/include/cereal/types/unordered_set.hpp | 3736 | `af92b5abab55d6d075e6aa5ef5b628f4107c7b320e53be3942c33396dd6917df` | 0 |
| lib/cereal/include/cereal/types/utility.hpp | 2145 | `c6075328aa79795a7412a131c51b960fe131cf688dab123586e1fed26b48e0d1` | 0 |
| lib/cereal/include/cereal/types/valarray.hpp | 3946 | `3787ac86bc058de0f038d5c92ab1d96073bbf53bcdcba96b937cac3ffa4d823b` | 0 |
| lib/cereal/include/cereal/types/variant.hpp | 4123 | `281be6bbaf44ae3c9792849b5ff909747b04b03a917bb08f09314da92604a9a2` | 0 |
| lib/cereal/include/cereal/types/vector.hpp | 4866 | `2d4de56deff7c5f4c17e5a95239fdca389e95a53f524b5da82e366181239601d` | 0 |
| lib/cereal/include/cereal/version.hpp | 2360 | `5a6959e7c2a3e54589826af1db079ad72258e5a77cd353658b7d232f7fa5b9f7` | 0 |
| lib/cereal/sandbox/performance.cpp | 15373 | `d0cdc5d9a09ef8bf31736a47625a1a7d15671c063536289e742560033352b9de` | 0 |
| lib/cereal/sandbox/sandbox.cpp | 18451 | `10975e359d193ea6df07da59738e7deb800ad7429459c470dfb34c7279d26552` | 0 |
| lib/cereal/sandbox/sandbox_json.cpp | 9868 | `15f61202b1f41f5db78bb6bb59d64df4fcad1b34f3cff1292c8db8ae942879b0` | 0 |
| lib/cereal/sandbox/sandbox_rtti.cpp | 5575 | `405f0b197853a8f28d274189b6c72c28ab03db57fc6fd3a197afd3b670fab521` | 0 |
| lib/cereal/sandbox/sandbox_shared_lib/base.cpp | 321 | `13ee6323490686b22a6d0042bccdd81ad887da29a883cc8626940063647d4261` | 0 |
| lib/cereal/sandbox/sandbox_shared_lib/base.hpp | 968 | `7ba2133d8470c23c9d8a297e00b6a0e1c4d669ba78c024af72115235de16b543` | 0 |
| lib/cereal/sandbox/sandbox_shared_lib/derived.cpp | 331 | `2a60700f8035589d1d13bf19d0b6225678e7178117f643fbee97ab21d1224764` | 0 |
| lib/cereal/sandbox/sandbox_shared_lib/derived.hpp | 610 | `d2d59886fc4fc7f3286cf562ff9215ce5964f734ae49cea739b937a01b52d576` | 0 |
| lib/cereal/sandbox/sandbox_vs.cpp | 8918 | `e51abb3ecf8f175469918f27d2ed89985ac32f209fd1298b965dabd47ab45ffe` | 0 |
| lib/cereal/unittests/array.cpp | 2124 | `dc7c83985db2044e1fd2b0bb1cfd25ec410413d241b01b4bbb00fd28a171fcc8` | 0 |
| lib/cereal/unittests/array.hpp | 3578 | `5121e9292f403022bc3dc260f2c158f013d6cc8f60ae5aeb0f02d879d8f11f3b` | 0 |
| lib/cereal/unittests/atomic.cpp | 2134 | `832c8798693bdddadf9b670303fa1358f1eb42471be2595f7ea956dbb47804a8` | 0 |
| lib/cereal/unittests/atomic.hpp | 5080 | `ae0a905fb0c10dd196329f021d9a472a01f06d4062bb64e399da82665fae194c` | 0 |
| lib/cereal/unittests/basic_string.cpp | 4704 | `3d0adff5b641c58a2c44b11ee4f3009dc2a9cb0b82f92bf4cef777ff985af92f` | 0 |
| lib/cereal/unittests/basic_string.hpp | 3700 | `5d82cfe6da852dc3bf697becc80b7b9111697983dbfd3d321c6abe76a32f2005` | 0 |
| lib/cereal/unittests/bitset.cpp | 2134 | `2baa32af874b8656eb4650500b97e2872d565eeb7816823583c3142868127f86` | 0 |
| lib/cereal/unittests/bitset.hpp | 3044 | `67097762a15daff1d5581dd82ddfbe3a3861a907c59eb15868d33f011eec73ec` | 0 |
| lib/cereal/unittests/boost/boost_variant.cpp | 2186 | `7cf831199372a59c4d50ae437140092b33de609323a9c39245460b46e8355b6c` | 0 |
| lib/cereal/unittests/boost/boost_variant.hpp | 3469 | `23f674d0aa50fc75b2eff7ea85994938a2994ef86cd0f87a4ceb4386f0737842` | 0 |
| lib/cereal/unittests/chrono.cpp | 2134 | `e1967e04c4bbccd86f23140d1ebb49d6d12d0738864920f37e2951cd30059033` | 0 |
| lib/cereal/unittests/chrono.hpp | 3773 | `f3bd0a5abe7d0a036bbb8908feb246a710f43278237293fad263d63ce8665fe5` | 0 |
| lib/cereal/unittests/common.hpp | 8083 | `135d192468bbe0871c08013f10c57f233510884dee1d7d66708164a6b15f0f00` | 0 |
| lib/cereal/unittests/complex.cpp | 2144 | `25cac5c53f5be5237e3410a857976754df2414b086c80e2dae3d35f6db6d4b49` | 0 |
| lib/cereal/unittests/complex.hpp | 2955 | `c333fd23a549410109491211973be6c9ffebe8a948408f2e9477bb96ed6f4f19` | 0 |
| lib/cereal/unittests/cpp17/optional.cpp | 2239 | `6b0a0c80b9167250529944b0a8b9fbf9ada8fdb96a51521dc31b6395a48a9241` | 0 |
| lib/cereal/unittests/cpp17/optional.hpp | 3235 | `b9c233e98af2e489e2ec3fb0cb60e0f8f1b15dab1539bd6c848835114f6634c9` | 0 |
| lib/cereal/unittests/cpp17/variant.cpp | 2243 | `2925f3bdc7a182382384f032389e8bfb9c94bb8e0c21e18fd6aa560b7a601e2a` | 0 |
| lib/cereal/unittests/cpp17/variant.hpp | 2709 | `c2137914e8dfb93855ca856fd99482d5b14fd36821a8bc1df40efd212fe613dd` | 0 |
| lib/cereal/unittests/defer.cpp | 2124 | `2ce86c128dea0ee81d1fa3dec1c42c604773fa2e7b16af7b4eb4802dc0cf973c` | 0 |
| lib/cereal/unittests/defer.hpp | 5730 | `f767373e822aa6f8234c84876051453b1687d622546eee94e01468bbec9401cd` | 0 |
| lib/cereal/unittests/deque.cpp | 2132 | `82d8faff987c8491a34cde2c971e1592a630adff2aaec1c21040bea131140651` | 0 |
| lib/cereal/unittests/deque.hpp | 3808 | `01393e62acd98a7a41ed3e30299a86151e6ec60de32b807a20f74642a797811e` | 0 |
| lib/cereal/unittests/doctest.h | 305882 | `2b5cbdbf68516e26e93bc2d3a0edd5cec9d48969db04f731ac3c87fe530f11c5` | 0 |
| lib/cereal/unittests/forward_list.cpp | 2194 | `7036de7188ebc8dfb1cfcd4dcd09d7b4ac27be5fff81db892c12676b0f156523` | 0 |
| lib/cereal/unittests/forward_list.hpp | 3888 | `717cecb80e287679049c04ff10205302ac1fc613e06ed0edba3b15fc1c749c27` | 0 |
| lib/cereal/unittests/list.cpp | 2114 | `e2aa1f2a6b05907dc56ad55d4ab2f06482256f5e276bab29e416e550e6073598` | 0 |
| lib/cereal/unittests/list.hpp | 3495 | `c46fa7e926734fc7558cd2e7d1ef8f7472711981764270ae795cd577c014dfbb` | 0 |
| lib/cereal/unittests/load_construct.cpp | 2270 | `942cf0d5b5faaa5e5abd9f7b19c80edb987f18fb339d8cd3cdfeb6ff9bdfadb8` | 0 |
| lib/cereal/unittests/load_construct.hpp | 8803 | `68be2b187d542de7ab25ba9f5769096f13c920e07dc4014605e0308d407b41db` | 0 |
| lib/cereal/unittests/map.cpp | 2570 | `be04a546a4c33db90f6864824bb37551e91b3ab3bb9806cabf99aeb68b253928` | 0 |
| lib/cereal/unittests/map.hpp | 5942 | `4ec8b36cb5e2bbbd64af22403b28bd998e77a6d9e6eaed919df455a65eadd92b` | 0 |
| lib/cereal/unittests/memory.cpp | 2680 | `15c5f899163ec4bdbcfd6546e12705102d171684069c904e3aefb660545499b5` | 0 |
| lib/cereal/unittests/memory.hpp | 4664 | `18f672df1a6da98b2b6e611f8b08ad0dec13521d918768dfdb39f4d00085375b` | 0 |
| lib/cereal/unittests/memory_cycles.cpp | 2204 | `14deb71f8a2c7fb75eb99bef982079db5b43eb985f9c6979bd588a7ba8b8f2bf` | 0 |
| lib/cereal/unittests/memory_cycles.hpp | 4128 | `fbb9eeb6079a66fe832b11605aba24934045b5179086179e25dba49a18575a82` | 0 |
| lib/cereal/unittests/multimap.cpp | 2154 | `973266a320555a4d9467519035afcb10f3fc041e0816d137ae61e43cb193ad63` | 0 |
| lib/cereal/unittests/multimap.hpp | 4881 | `79a66ee1b3ac2491e22da828f09b04be8246265635408c0dc7ea8e8cd28c1cdd` | 0 |
| lib/cereal/unittests/multiset.cpp | 2154 | `2acf4f2e8d242e6f648596a5dc3d4b56c5daca95ff094d88ad04b4b7b25eb9d8` | 0 |
| lib/cereal/unittests/multiset.hpp | 4380 | `47d9bddddc9631c62651c208edddde3b63bc9c028c88b8df6dda64c12278d3d3` | 0 |
| lib/cereal/unittests/pair.cpp | 2113 | `a7ce4faaa618d309c348ae8f3ea5487dce521b90438a63eec07fe453b8caf712` | 0 |
| lib/cereal/unittests/pair.hpp | 3615 | `c551915a9b8ff7ae6b3b5e8933e578de06c5b3a3f85d95cef518f40866b7e258` | 0 |
| lib/cereal/unittests/pod.cpp | 2104 | `87a9a137a508f5e299793025b9f87925737dd7f98025c6d370f737136649bb2d` | 0 |
| lib/cereal/unittests/pod.hpp | 5547 | `493c572a7960662aa707a7754e3a677038c0640f147297ff540a18c0ccd512e1` | 0 |
| lib/cereal/unittests/polymorphic.cpp | 2790 | `534cb20f941896b1f6e15a54cee9d143f86a033e551d88e84417b0c7e2ba54c6` | 0 |
| lib/cereal/unittests/polymorphic.hpp | 24170 | `4a3af7870a09fd77538f719871f3f7e1b1e04eeae382a37380d0f5eebfe2de43` | 0 |
| lib/cereal/unittests/portable_binary_archive.cpp | 5110 | `d26bffd90ac3b7e213272d256863e492e071756adb549fdd23052b4e1b94bba9` | 0 |
| lib/cereal/unittests/portable_binary_archive.hpp | 5898 | `46d7f7f949b74b4f3bce09700ff371d598827bfbcb2bcb32b4c83330ec9127e7` | 0 |
| lib/cereal/unittests/priority_queue.cpp | 2214 | `b4ffc34c5700e07e30c762815385e87a651500a226b2699833a0be778dea8026` | 0 |
| lib/cereal/unittests/priority_queue.hpp | 4831 | `7d043aeabc28688d9fbe8ff9eb3d5d10dba6b5b735067c05a013c7f5e7b8b642` | 0 |
| lib/cereal/unittests/queue.cpp | 2124 | `315f15d68479f46061d2df7310b28677b07aba14762d7026a8e73f34eeecc76d` | 0 |
| lib/cereal/unittests/queue.hpp | 4210 | `22ccaa6bf59e78b7290fe8bdda231f0a4fa993c2f68bdb9e52c54e5eb4de2ce7` | 0 |
| lib/cereal/unittests/set.cpp | 2104 | `540bfeaf47188e97dfffaf2ee9e2086295093e50751035ead3f230ab9ac1e81b` | 0 |
| lib/cereal/unittests/set.hpp | 3379 | `45edc9d52f418fa3f16daefdcc0672099fa585484772f5c9704d2ac93873a0d6` | 0 |
| lib/cereal/unittests/stack.cpp | 2124 | `0bcd51d61f1a3945943d68e98f89b0f324b86e40112f1c22e01160fbd67543d3` | 0 |
| lib/cereal/unittests/stack.hpp | 4211 | `a91e8ba6f80935a1541271ad78b34dbca9e4f2effdefb9acd5a97986d01a3276` | 0 |
| lib/cereal/unittests/structs.cpp | 2144 | `5f6cf4a7c2a5ecbf80d2df8b49e9a3dbed0ae13e48ef5519ab45fc2bfd296713` | 0 |
| lib/cereal/unittests/structs.hpp | 2717 | `13c31978a0a00db778e7ff1710a8cdb137e0457ca05d5bd4c7eba3082c4677d5` | 0 |
| lib/cereal/unittests/structs_minimal.cpp | 2224 | `661ffc7c1f1778c85a705b165922290d9eb8434270ea330f6c9d5b9eb2bc773c` | 0 |
| lib/cereal/unittests/structs_minimal.hpp | 8212 | `edb7ca2763b0bafdd7af1fc1d15d15ceea612f5a67a22bbb51c213abd4ad220d` | 0 |
| lib/cereal/unittests/structs_specialized.cpp | 2264 | `67c40634c85ff3fd771ba4d59e91cdf5e49cc11e1463bb9ad433e82001293539` | 0 |
| lib/cereal/unittests/structs_specialized.hpp | 12751 | `c869e6d3aded3801109e013031464682ef1a0a0322c3219556e10419aeaf930b` | 0 |
| lib/cereal/unittests/tuple.cpp | 2124 | `26a2c77784c9e5ab86dac9b3df6ea488c8ae201d16a47aa66a0acdef7f866515` | 0 |
| lib/cereal/unittests/tuple.hpp | 3984 | `be2971de599447287d98f2d3916bcefb33531fb97344c53290418cbd1ae8ba2b` | 0 |
| lib/cereal/unittests/unordered_loads.cpp | 1951 | `08fdaef01e6d8b94b0825eb524107feb0a3345f138572494135a411123581c72` | 0 |
| lib/cereal/unittests/unordered_loads.hpp | 4876 | `761fb1c9148c633604d1f7ab324da7035b1dbe333cf56c17807cee02442d9355` | 0 |
| lib/cereal/unittests/unordered_map.cpp | 2204 | `28091ad1b314d2c89e90508d98f754f7d2473808064c940a93ab887855d448f1` | 0 |
| lib/cereal/unittests/unordered_map.hpp | 4763 | `c9af90222705acae2116dd544ebc365cce7b7cb395bc2cb8201fafb0d4f5b118` | 0 |
| lib/cereal/unittests/unordered_multimap.cpp | 2254 | `6bf42bf3ea3b4867b1319e8ab5755b2358d76f0366f0d03ab8ac7394f70c1f97` | 0 |
| lib/cereal/unittests/unordered_multimap.hpp | 6679 | `edc67619454c202a9227f1aa460b02383dca06d1ef3a9d9dab2f0d68bfd55085` | 0 |
| lib/cereal/unittests/unordered_multiset.cpp | 2254 | `ab21fb9a0aa410652319e88443d0fd9e1c0a4bb870489541f6d1a0cf13275a1b` | 0 |
| lib/cereal/unittests/unordered_multiset.hpp | 5258 | `9d66f027e1532bbf1b8ced23e96330cbe771b4444822adf6d0ea64a7f38338e7` | 0 |
| lib/cereal/unittests/unordered_set.cpp | 2204 | `ddb62c6d453107e7ffb67adc8f3a7800d274e7af7373f4a79ba4a242e9eb64f3` | 0 |
| lib/cereal/unittests/unordered_set.hpp | 4386 | `6d507cf9bcaf7ea4b49976eff1584aa37e508763fb6206e1c51f38e7f1dfdba7` | 0 |
| lib/cereal/unittests/user_data_adapters.cpp | 2254 | `b762dfa8b9e00fc272052110315b3ad944e38fe1cffefc095fbda116ef4a797e` | 0 |
| lib/cereal/unittests/user_data_adapters.hpp | 3539 | `4e8078752496440d91ada5b725e9025f1c5f633de820803714864b86fa3d7e47` | 0 |
| lib/cereal/unittests/valarray.cpp | 2051 | `2c65f8c048e6cf1ecc53fc9bce96f1e90276d58eb619da9e1eceb55dc367bc15` | 0 |
| lib/cereal/unittests/valarray.hpp | 3888 | `5bf86d9e71a2f2f2e99a1b8a409811a0fcf602dcf8804e846c3f295b8de7134d` | 0 |
| lib/cereal/unittests/vector.cpp | 2134 | `6583a2acb94c65df891fc48de737612c83ebb5012c78b18930b3462710dc1be6` | 0 |
| lib/cereal/unittests/vector.hpp | 4227 | `cf555af6f9798ef47dcddb39e84c768239358509be0b7371c1466ab9156eab2c` | 0 |
| lib/cereal/unittests/versioning.cpp | 2772 | `901575d7e513aa4d6d28fa7ae72e4ff723d94564d0511842d1d3349f1d22d5ab` | 0 |
| lib/cereal/unittests/versioning.hpp | 5841 | `12952259148c03c712ca2d6fc67eb204f81dcac6f4bbd4d67937d4798f28a14f` | 0 |
| lib/fmt/doc/fmt.js | 76 | `8a70279ed02d04ebeabfdd88945dcd59a6da04fd4cb69115312ec04ff4bdaa3b` | 0 |
| lib/fmt/include/fmt/args.h | 7199 | `6e0bf8ffbd904e6ef525cdce8e6e00312ce5d14f616cea5d88132606ca0384c4` | 0 |
| lib/fmt/include/fmt/base.h | 105031 | `73ba80ca15c02d6826a611d1651ca6f1495ec127815e257a5d6552d6f6ad313e` | 0 |
| lib/fmt/include/fmt/chrono.h | 77454 | `f8e2a69bd97bc5b90c9af7fb87e010775b695d487a77e8d8cbe624e57bd2f9bf` | 0 |
| lib/fmt/include/fmt/color.h | 24145 | `f88bf0c4833caed3a7f01b6d633c7b259741a26119e84c651ac1e31cfc980b72` | 0 |
| lib/fmt/include/fmt/compile.h | 20493 | `636c13842acce0b42b378e65fe67a69e5635e8225c9701975e5b326a97be5cb8` | 0 |
| lib/fmt/include/fmt/core.h | 187 | `b2b6692145b11c7c2774db106078c97575a47d18e80c7783c68566475325ebb4` | 0 |
| lib/fmt/include/fmt/format-inl.h | 81008 | `e7baf108b84e89b29915bb35733540f8f4262cd8f4b41c15754eed4d2f185f61` | 0 |
| lib/fmt/include/fmt/format.h | 162666 | `b4c65350362bf40e76a8e6b450587d912c7081b6eafeafaf3d7bcf53153e17fc` | 0 |
| lib/fmt/include/fmt/os.h | 12860 | `45d4e84be4e84a128442f04eda06e1305c8e02c61166854a3b8b348194d35da5` | 0 |
| lib/fmt/include/fmt/ostream.h | 5027 | `742416a6a88286609887fa512c4423820764aafbb723a42a825f3193cb52b4f0` | 0 |
| lib/fmt/include/fmt/printf.h | 19991 | `afddb422a86125e04a7260bb0f0ae3423ea8d591181ed5d4ef60b7a5d068993a` | 0 |
| lib/fmt/include/fmt/ranges.h | 28126 | `ccaf61c9b5937e0fa97737fb047121c5fca9db34de516b8edfc1d913583e3c8e` | 0 |
| lib/fmt/include/fmt/std.h | 23532 | `3f06cdf32774b9e6915e9762411f5f4de8b8ba5660adccbdea514be7f0b23826` | 0 |
| lib/fmt/include/fmt/xchar.h | 13098 | `f0903d522c64faaee2c374a0b2063ac3e43d0b5006dfd3411f0e5dccd8ff6062` | 0 |
| lib/fmt/src/fmt.cc | 3331 | `7b58ba737d2dc1e61a5abcbade6f96125e5ae799baeefb05f23e65639e547998` | 0 |
| lib/fmt/src/format.cc | 1221 | `f349197184b097403798c08b1758f4f7405916157cc7bcd070ea331f9f6604d5` | 0 |
| lib/fmt/src/os.cc | 11388 | `2dc03e2c6dc21197f5ac967e01211feca1e5da7c51c07b27e80a1e54126ee313` | 0 |
| lib/fmt/support/build.gradle | 3977 | `761326806692d751cfb7ff2f4f7d4d7c0aa10de6856bba6ceb22dda2582c4c19` | 0 |
| lib/fmt/support/docopt.py | 19784 | `ee8a677f71fa3ab35fb456c141d8853a366fe91d5fe73c2f84e7b4d3014f6980` | 0 |
| lib/fmt/support/printable.py | 6109 | `c60d5af1143573bfb0995b36c3de7b56b2d8f8a910fbd7fea58b64bccf95f669` | 0 |
| lib/fmt/support/python/mkdocstrings_handlers/cxx/__init__.py | 12091 | `5746f9b56895c28a1c5caaf5a496efe5549c24df0d6a3de7ad2ed6937abd5110` | 0 |
| lib/fmt/support/release.py | 5908 | `e01fb0fad01f5b81cbe7ce4d9b2863790b8e0f8e568c72b7d585735ccef9d8cd` | 0 |
| lib/gperftools/.github/workflows/scripts/msvc-env.rb | 1329 | `3a2e7d5d79e51a97ad7be32ba3233875704d9e039b8272af9841be5e3e1e51de` | 0 |
| lib/gperftools/gen_compile_commands.rb | 2716 | `2608c9125d82faaa08cc1b47cc55d114dd75e73228fdefcb151d31f506e7a428` | 0 |
| lib/gperftools/generic-config/config.h | 8560 | `be77f14fce43da23667143e019bb2617e8ef080d611d4eb1b275cbd84b8a0fb5` | 0 |
| lib/gperftools/src/addressmap-inl.h | 15674 | `138905a279222f4bfe373d8900280f188def640ad5f76ec3f8cdec11e5a405ae` | 0 |
| lib/gperftools/src/base/basictypes.h | 6965 | `8ca9c881f7a83970b9fc05ab162e7005aeeabdc0d65fe758ff0010725a3f7265` | 0 |
| lib/gperftools/src/base/cleanup.h | 2953 | `07703a3fffb0c1a7c3ebeee9d611728cc88819f43dc043a46634762968ac1a22` | 0 |
| lib/gperftools/src/base/commandlineflags.h | 6994 | `a90360a6a80ad90246dce6b6ee9fd8bfd0d8ce573bb7811dea2307cedd1d037e` | 0 |
| lib/gperftools/src/base/dynamic_annotations.cc | 2613 | `fa53a54cc8ababb6c1acf04e8eebc0b0517ab5fe0b177ff8036a97e676632a2a` | 0 |
| lib/gperftools/src/base/dynamic_annotations.h | 3560 | `5cb61b8f75a7f19d462e847fd02d6072cc3a836607323f8df3bfac5f314bac31` | 0 |
| lib/gperftools/src/base/elf_mem_image.cc | 14669 | `d992d1e94f2e9fa332023e71a67eb39fafe915383a1bf937dba5954576a14538` | 0 |
| lib/gperftools/src/base/elf_mem_image.h | 5034 | `07785db317db2ec7cce591de29f03dd2177676b0181688a7ee496a0617d7c37b` | 0 |
| lib/gperftools/src/base/environ.h | 2332 | `84a7911be4574cf279718ac641a9775d79da6b72ac4b69ab3a8e8e256a339071` | 0 |
| lib/gperftools/src/base/for_each_line.h | 3864 | `0ae0adb4ce5ef8def4ac778ccd75dc4a3859453bf3647ce5297896f43a006c35` | 0 |
| lib/gperftools/src/base/function_ref.h | 4680 | `5fa0b899eac02364eb52b81809121a14322cb721ab09cece49bc37fae66102e1` | 0 |
| lib/gperftools/src/base/generic_writer.cc | 6977 | `dc41de467093c1121c9a3ad3bf52f5e426d623febf54ae6f198b8f5f5cbd93bf` | 0 |
| lib/gperftools/src/base/generic_writer.h | 6630 | `ddb00076411589a75781bd151a4116c66e2da5db76ab69d132e398b8f17b0dac` | 0 |
| lib/gperftools/src/base/googleinit.h | 2938 | `778eda4b41fc9075ec0cdbf283bebb6e00dabc678d54fc790c9688fc74d2d7bb` | 0 |
| lib/gperftools/src/base/logging.cc | 3798 | `3fbbcb88b02e1f57409472bc0234fb76bb99f60eb340a7ed9ca4ac29549aac90` | 0 |
| lib/gperftools/src/base/logging.h | 10411 | `7072e1620db20bab176a3b86f56c1dd32958eb99dcd491a8fbb76c21a8c76230` | 0 |
| lib/gperftools/src/base/low_level_alloc.cc | 18993 | `eb519909014a4d4021ee67a68922b42376a48d96813be72ff7cfdbff8e4fe26f` | 0 |
| lib/gperftools/src/base/low_level_alloc.h | 3960 | `97fc853c980ba6728ff3d1cfb27973eb2440666abcaaa0196b7b7fa038bb784c` | 0 |
| lib/gperftools/src/base/memmap.h | 2615 | `27a7e2b493ada483ad71ee787ec790e96d92b102528b648f784326e629476526` | 0 |
| lib/gperftools/src/base/proc_maps_iterator.cc | 19508 | `b84e6a5969f5a18df588d836efa124295e7710edf5b77573e18ea6b7150cfa75` | 0 |
| lib/gperftools/src/base/proc_maps_iterator.h | 3200 | `393c4e70288121426731bfbc009a079b393b2dd6af38e701c8160bca60143457` | 0 |
| lib/gperftools/src/base/spinlock.cc | 6472 | `033bcdb46057125a279de64826e9c101d6714519711b751bcfbec0ede9056616` | 0 |
| lib/gperftools/src/base/spinlock.h | 4787 | `64607951628e08c4f62dddb433921e1effc9a4e5b5abc1a99e543ce7b433d5e1` | 0 |
| lib/gperftools/src/base/spinlock_internal.cc | 3548 | `0fd9a49759e85e610c6681d5bdee41d4384c20dc28de6d0be6b2f12360958efc` | 0 |
| lib/gperftools/src/base/spinlock_internal.h | 2099 | `87ccdb3f2dcf6dbf115c506d4d805de6cc1417f2c7a2dc78a4ac812a956d2488` | 0 |
| lib/gperftools/src/base/spinlock_linux-inl.h | 3590 | `1c6faf6ff53f17e6c3a90d8ef2ccac2a8026c4194a6a9c6afc6587453545aee1` | 0 |
| lib/gperftools/src/base/spinlock_posix-inl.h | 2325 | `c187bd6690658b9bcae7870c415eadf7bead493c4281ccdf6c24d10df20f2c0e` | 0 |
| lib/gperftools/src/base/spinlock_win32-inl.h | 2307 | `e1fdb50572f7a6510dc37c30d50b213c1a50ea59460b06f37abbe4649741700d` | 0 |
| lib/gperftools/src/base/static_storage.h | 2199 | `7ba368e43e874ac9484a500c1f291584a31139cf805e075656d5c5206f969cc2` | 0 |
| lib/gperftools/src/base/stl_allocator.h | 3691 | `ee029ab978c3178add21da9c27cc3fe7286ff7634e033526750f16b76a798bca` | 0 |
| lib/gperftools/src/base/sysinfo.cc | 12876 | `2d76f49455927a17cd1c3fb100982dd58b606674581ea667b674f44f522563af` | 0 |
| lib/gperftools/src/base/sysinfo.h | 3425 | `f11d1bf3b5e66c76e8661106fb10d32b142cb8c82a3677ead9f985aee5711c37` | 0 |
| lib/gperftools/src/base/thread_annotations.h | 6026 | `ced3f95174dba4684138ef90d0a4e7039c102d0cf7dcb3043e2dfd1f65d719e2` | 0 |
| lib/gperftools/src/base/threading.h | 4935 | `0f39afffa36a906d7756326ff791625e7d6807dee37fe4e1f39452a6a785e1b2` | 0 |
| lib/gperftools/src/base/vdso_support.cc | 5185 | `399e6368294f542f09812cbba970b10600176af4ba64a576b2aed0848f45ea83` | 0 |
| lib/gperftools/src/base/vdso_support.h | 5111 | `0d37de11b8033f71ea2b8f296389ad90b0c057b911a2a49cdf0d45f7f910779e` | 0 |
| lib/gperftools/src/central_freelist.cc | 12911 | `abfa3f3a94ba08f3f137bf28b13dc95f146091a78e91ac4398de8124c4123e0a` | 0 |
| lib/gperftools/src/central_freelist.h | 7585 | `461b36fc724d6e7a839e0bb7273ab078511bb749aa0e87897e0bbf79ca4965e4` | 0 |
| lib/gperftools/src/check_address-inl.h | 6819 | `614a5aae4b3ed377751c4e457b8dddf7f0aecc4654dc3fd9a391b47689e3c2e4` | 0 |
| lib/gperftools/src/common.cc | 11798 | `500b125070007d30d1caa1c469426a3d5c9b6e9d8c4c35e510909356ec7147bd` | 0 |
| lib/gperftools/src/common.h | 12199 | `088025bad22ee75d92f6c55998054f274e729c26f1f3d5a1c0bf5cc5c7ffef6f` | 0 |
| lib/gperftools/src/config_for_unittests.h | 3961 | `18cf3495ece4f6c41623bff7d665f5841ab95e8892ea118bff8ceefad308ce08` | 0 |
| lib/gperftools/src/debugallocation.cc | 58811 | `9fb845d8797022a90fa4fa2fda10f4170995ad3c08405d67b8eebc1d136bd54f` | 0 |
| lib/gperftools/src/emergency_malloc.cc | 5983 | `bb6c27e307d17ff2990537f49232fe11fbac8b4dcfeaa9cd66a5e4c55b0b58ae` | 0 |
| lib/gperftools/src/emergency_malloc.h | 2628 | `9ba7adeb1a2b70c842cab30f0fee938356d093277eee1fbbc422c6da93125287` | 0 |
| lib/gperftools/src/gen_getpc.rb | 6636 | `414c6e97ccb5de43f76432102e21df3b8d50df5a719afbc1e646e3c2ee1ef084` | 0 |
| lib/gperftools/src/getenv_safe.h | 2803 | `c06e282fa1f760d251b3e173e2651b7e6da7b0348a1a55ba6ef744c847353fc6` | 0 |
| lib/gperftools/src/getpc-inl.h | 11910 | `d72e10cc073eab7e56cf5437eea5b08a3c60477cfbaf9cb07bdf36d58b0f12a2` | 0 |
| lib/gperftools/src/getpc.h | 3649 | `dc84362f7c60c2e15443da6befa0d67f4087c87192096b532c2c9be179151b14` | 0 |
| lib/gperftools/src/gperftools/heap-checker.h | 5637 | `e2142add7217758f0443417d0046d675d3e68c940abd67537b6ea725a78db764` | 0 |
| lib/gperftools/src/gperftools/heap-profiler.h | 4046 | `91eb29603a83925f5c712c7dfefda698ebeb7737e7229b71ccf5a4f3b9b1aeb2` | 0 |
| lib/gperftools/src/gperftools/malloc_extension.h | 19610 | `e2d5e187cecfee4ffa545e7a92698db29a0f8dcea09a3e9d8d1d8f7d0792186a` | 0 |
| lib/gperftools/src/gperftools/malloc_extension_c.h | 4343 | `c1acd7ef5528e94e5c6fef26fc6f54f979ee2207d0baadf3019643bb3906f60a` | 0 |
| lib/gperftools/src/gperftools/malloc_hook.h | 8727 | `430fd1c360f58c0a043082acf95fd684c5b69c1c99cc5c199b8fcce6e688af45` | 0 |
| lib/gperftools/src/gperftools/malloc_hook_c.h | 6902 | `918170efeec2333b23e013e2567425461ad49a6b64cbeb8fbdbd5a1c2a12a99e` | 0 |
| lib/gperftools/src/gperftools/nallocx.h | 936 | `1f7258e62c06760b0dd61d7f10caf266a61f2e1d4996bcce82d2906b0d289e37` | 0 |
| lib/gperftools/src/gperftools/profiler.h | 6472 | `c7926d22c29165dc1621afc576a36d0e097c82dc58e6517d1a778bad848093ad` | 0 |
| lib/gperftools/src/gperftools/stacktrace.h | 4964 | `dcea7ff4db8d299ea73b4fbf3cc4059774cbdebb6bb7a7863acf0f4477b6ea0e` | 0 |
| lib/gperftools/src/gperftools/tcmalloc.h | 8319 | `bf714228fab71de7086c1da1ad91ed211b993cd51e4f7eb0b21fd640f65e7dff` | 0 |
| lib/gperftools/src/heap-checker-stub.cc | 2489 | `8d8fd255d24721f177551bed0cef8d6be2f88238ea223108b5c694280903072c` | 0 |
| lib/gperftools/src/heap-profile-stats.h | 3578 | `f13d02859df46330ae9d842e303aa9262898a0f684f5435a41d90d207844eb14` | 0 |
| lib/gperftools/src/heap-profile-table.cc | 10500 | `3b2d70423c110f668fe2ed712392580e093df1a07ecea91e7bf6609d9f6f8689` | 0 |
| lib/gperftools/src/heap-profile-table.h | 8573 | `9727cbdbeb7d0de90ce1e2db6f2dc9bbd70f1ec80d9f0a23f39062295d38a24b` | 0 |
| lib/gperftools/src/heap-profiler.cc | 16493 | `a9eb9a2fe19097259a3c240927022fce0a6bc464951ebacbbe5dcd0e4264bc75` | 0 |
| lib/gperftools/src/internal_logging.cc | 5067 | `9a843294bc3cbeefb9efe52a54d454fab0fb24346873b849f5d22ad3550a5680` | 0 |
| lib/gperftools/src/internal_logging.h | 5289 | `d1fbfc65f76df33db70cb4a2c866c025ed25d0b6a7cc0581e41e6b7b04638f2e` | 0 |
| lib/gperftools/src/libbacktrace_api.h | 4610 | `9b346e2580245a0e76f94fbd9200a124cc5f4823979833a4419cc530af957b1d` | 0 |
| lib/gperftools/src/libc_override.h | 4734 | `f8062ef524d7cb692d7d08d7110f7e14575c124af7a30642626dbe5f7be1bd9b` | 0 |
| lib/gperftools/src/libc_override_aix.h | 2883 | `444126652587253022627d3bc691ef5405ba4267cc0c8534c373e376718d36cb` | 0 |
| lib/gperftools/src/libc_override_gcc_and_weak.h | 9841 | `bd07f114c94082bcd56eea7114dfd42f6267e91ab7804fb6937c8a497d45a2f7` | 0 |
| lib/gperftools/src/libc_override_glibc.h | 4237 | `34f896568b01bea9ec9e4e149caa81b70e2bd25a4865c4515711626d27cd5522` | 0 |
| lib/gperftools/src/libc_override_osx.h | 14839 | `01be9e0d590440037620bfa14fad35412df2f74257c582de809da875153e9027` | 0 |
| lib/gperftools/src/libc_override_redefine.h | 6281 | `b92da76df6e1eb022a2cebf07fc80282d34bca1e334ad1b2fccb1c3fb55ee50b` | 0 |
| lib/gperftools/src/linked_list.h | 3402 | `75f6abe40fe07c8596508327e4b605668b0d029e8fbcc0e32a3f5be26bef6f05` | 0 |
| lib/gperftools/src/malloc_backtrace.cc | 3216 | `eb948ff61b1118652c0923ed44d8d21650516cf9f8603b2148d969c0b1659405` | 0 |
| lib/gperftools/src/malloc_backtrace.h | 2698 | `3d8895d66b07f90a2115f3f63cd9089584fb708d59daba8df4f42270359f3810` | 0 |
| lib/gperftools/src/malloc_extension.cc | 10563 | `b754bb12375efaadfb169ca18e1f7517488e2acb86aa8a0c991f66a2f1c825c6` | 0 |
| lib/gperftools/src/malloc_hook-inl.h | 5561 | `305dbd6ffabf49b12f21f816e5815337abdf15ea17cb72b0a5328cc75b346010` | 0 |
| lib/gperftools/src/malloc_hook.cc | 10675 | `9d9eb2329e1e8c6f64a67d15a22af46c98f053d13b2f71e1f5f865c1dd9be9c8` | 0 |
| lib/gperftools/src/maybe_emergency_malloc.h | 2364 | `f5c86b00c7f0f67d44fd0c2389d06bdd0020d16b6c7e59ff0a75d0b319220965` | 0 |
| lib/gperftools/src/memfs_malloc.cc | 10293 | `701ea956431c3418dde6fbbcf3bf7c794740c8d3f1a26d8c7537ca0d3f8cbfe8` | 0 |
| lib/gperftools/src/packed-cache-inl.h | 8745 | `fec5c501301f220fe80af8cad68de396bf550483e2bfd878c8ff6d53853e98cb` | 0 |
| lib/gperftools/src/page_heap.cc | 27901 | `b36f1de9344359c732d2649d352496e5c7fead5f91d2fbf44240bb9d0ab7ea17` | 0 |
| lib/gperftools/src/page_heap.h | 13879 | `71f14299fe4ea326489f224d0e07d7c72d2c10f35e83530c59fde014fee44706` | 0 |
| lib/gperftools/src/page_heap_allocator.h | 6152 | `4f3339dd7ffcc414ad043fdbb73fbb8bd99230826050f4a59a6bf53030f175fd` | 0 |
| lib/gperftools/src/pagemap.h | 10099 | `67a2815ed949c403e969a872ff0514894e2b7586c3b40d6cd5e0fc2732190cb2` | 0 |
| lib/gperftools/src/profile-handler.cc | 18981 | `6276e3743c444a0edfd7405123cf8f07a4b2decd3b249418c0c9ca6e7d64c4cd` | 0 |
| lib/gperftools/src/profile-handler.h | 6117 | `63be54ed2b9741b459c3b7bac3e393dc76e01d6057efc82a7a1083a1e37a651d` | 0 |
| lib/gperftools/src/profiledata.cc | 8926 | `e2f3be010da0a42dafe263b3b12b6a545bb2931015fae695923bc44c8cb8489f` | 0 |
| lib/gperftools/src/profiledata.h | 6626 | `528244df330f4e9d27010fb32075638b02741448b927410f17ee4909a8671a27` | 0 |
| lib/gperftools/src/profiler.cc | 14733 | `af69bed972c099f919de59b56c480e775382db967372cf286fd6c6aa8ca1d260` | 0 |
| lib/gperftools/src/safe_strerror.cc | 4926 | `ab24206243051075814b8c1aa033b68ea881873bb6d37d9ead28b67cd263e125` | 0 |
| lib/gperftools/src/safe_strerror.h | 2292 | `ed8030bfef15182a4fea23d109132a4f808c3a276c464e23771e6de90865e7f3` | 0 |
| lib/gperftools/src/sampler.cc | 5254 | `8be6b33eeec079febf9e961feed032ba5d807dab0163bac3ef82608843b211ca` | 0 |
| lib/gperftools/src/sampler.h | 9087 | `cb8cf229cdc67dc0fc91edf3c3bccc492940516af594cbcdc88149be9e309434` | 0 |
| lib/gperftools/src/span.cc | 2733 | `99b82b021364e6b280415b086960136962462af2dcdc7f14b317b3699d3dddb7` | 0 |
| lib/gperftools/src/span.h | 5865 | `cbd74076f43cb2d3e7dda177258cb64f9dd1f98e1683ed10bbd1cf913415a944` | 0 |
| lib/gperftools/src/stack_trace_table.cc | 4167 | `516d6c534ba70d99368fce1d5c9377c45a38d12879c27094f856fe81918996a9` | 0 |
| lib/gperftools/src/stack_trace_table.h | 3141 | `7d203164592eea7c1de5c1b34fe5a19dbb553195e927694b37f91a49b7a9ccb4` | 0 |
| lib/gperftools/src/stacktrace.cc | 15225 | `e00b9d3dfbef257b1967199a102b02b3549f702981885745716ef9307dd31fcd` | 0 |
| lib/gperftools/src/stacktrace_arm-inl.h | 6130 | `85d16f62518a790fdffa2d749f910066a93073d09a86704b9c0313302b461400` | 0 |
| lib/gperftools/src/stacktrace_generic-inl.h | 3416 | `8f32d99b9a166f9754bc5f679d692700fd7085a23763499d576ea5f131a724bd` | 0 |
| lib/gperftools/src/stacktrace_generic_fp-inl.h | 12463 | `73d839e17a88c9f9b4c659b34a295872d08d858fb9913e446adb32924b0e71dc` | 0 |
| lib/gperftools/src/stacktrace_impl_setup-inl.h | 3907 | `a1c2e159c53825ea3991283b4095622bb2b0ccb4f9b741c149835673351423b0` | 0 |
| lib/gperftools/src/stacktrace_instrument-inl.h | 5611 | `a3c104eb3e66e53b433ed6b1808e08b9bcb6ed840dd79e5901ef162419101d4a` | 0 |
| lib/gperftools/src/stacktrace_libgcc-inl.h | 4007 | `0cc4a6cb7e3c879cf91bb98a3b91224dfb75b087f3de618cc9128be68ab5e4c7` | 0 |
| lib/gperftools/src/stacktrace_libunwind-inl.h | 5140 | `be475ad49be05f3ea487516945818e5c44f3f5872042eb4ec765ce447ec523c5` | 0 |
| lib/gperftools/src/stacktrace_powerpc-darwin-inl.h | 7058 | `e60975de5e18650239ec2ab9ba602e6d71b384a17db80b3ea3c6805629b6ec80` | 0 |
| lib/gperftools/src/stacktrace_powerpc-linux-inl.h | 8795 | `1d2e27b422a52def76f1b4e16a6d76f1a997bea694b1bc55a906b14967f51bda` | 0 |
| lib/gperftools/src/stacktrace_win32-inl.h | 4601 | `036a16c6813488b5304df7a8cea9c26d578fd32bdd5a3f0776d6c2057dc4863d` | 0 |
| lib/gperftools/src/static_vars.cc | 5611 | `5911d704acfae257cc79e8ca3a87a3d940b475cd7982a27a96f9d2cd8c9668a9` | 0 |
| lib/gperftools/src/static_vars.h | 5043 | `9d0a6a956d8139a7dee7fb808a467b6af655df627c66c434b1fdc1b594288b22` | 0 |
| lib/gperftools/src/symbolize.cc | 6691 | `c36bb4997cce598dba69aee1492e65ef485b45e747670456af3824715536299f` | 0 |
| lib/gperftools/src/symbolize.h | 2742 | `0d7e96ba7723f35cb5949bc96ebc43d9c0e64d7f7ff85d5d3e6afa6626076487` | 0 |
| lib/gperftools/src/system-alloc.cc | 16496 | `b0c233fc5b033c7ebd3002438005349d2fb69c13181a6a4cb44357e8b03778ee` | 0 |
| lib/gperftools/src/system-alloc.h | 4132 | `3cc23c35571af67e5d693f6bd3f86a2c001ea03f4a8bb093c417d97595ab2152` | 0 |
| lib/gperftools/src/tcmalloc.cc | 81465 | `61abb55ee0e67e1d21194914d8762c0e17e9379d3d1f647019d92467f9c4b1ed` | 0 |
| lib/gperftools/src/tcmalloc_guard.h | 2195 | `57da62f72bc922e644b9abf0bda6e52fbc546467736b9579305463792c09b2de` | 0 |
| lib/gperftools/src/tcmalloc_internal.h | 3121 | `a3979fbb8eb7c808f94583cfcc6b479548f77d08a744dede67c98d628f16143b` | 0 |
| lib/gperftools/src/testing_portal.h | 3384 | `b9d035d3836f95a9fe301172182254cc4dc60189a45deabe1e382416b87bffbd` | 0 |
| lib/gperftools/src/thread_cache.cc | 14279 | `a935620968255d3a9eecfe60fc15e5effa4223eb29fbbea75e8683b9d9bc19e3` | 0 |
| lib/gperftools/src/thread_cache.h | 12936 | `347280cd172e9ab5d2021789f463663c7937b8a4914d79a61df3f7da34c640af` | 0 |
| lib/gperftools/src/thread_cache_ptr.cc | 13172 | `25f17c514f056a5ba5472f3c887949fea8e23bb6cd138f6531004fee0b36f5e8` | 0 |
| lib/gperftools/src/thread_cache_ptr.h | 5594 | `4e4b0d94a50da3338d3483103bc233e56b8fd2557ec7b15d4151f46d604115e6` | 0 |
| lib/gperftools/src/windows/auto_testing_hook.h | 6223 | `30427f6d58d8e33014b3f55e4f85dfe41f9850423a15cf4655f87ede532c21cf` | 0 |
| lib/gperftools/src/windows/get_mangled_names.cc | 3144 | `cd71467e3d0d462c1d54125a98dd7f02c97ad51a66683939e89b8156094df147` | 0 |
| lib/gperftools/src/windows/ia32_modrm_map.cc | 5179 | `d88d4c9a927244c16428672f39f0b9b4fb1bf7773d858c2ae35fc79eec30710b` | 0 |
| lib/gperftools/src/windows/ia32_opcode_map.cc | 113936 | `e82db325cc4e4bd54cdb09f9ec419e7fae14e0c88af1b6c005cd047b51316975` | 0 |
| lib/gperftools/src/windows/mini_disassembler.cc | 16050 | `ae9bdcd7cf512aba2ede26ccdfd6130db2e52498c5fdacbdcbf6e1e98a4d530b` | 0 |
| lib/gperftools/src/windows/mini_disassembler.h | 8130 | `9b2c0072de35994f8029cf44d8952d808ac6dde7d192b8136f4270d3bab30768` | 0 |
| lib/gperftools/src/windows/mini_disassembler_types.h | 8512 | `8124a90823bb6bbe3bdc78713c9757e66c470aa02130c912789f8817d902eda5` | 0 |
| lib/gperftools/src/windows/override_functions.cc | 5154 | `d7a24b88cff03d3a661c01c2e6e3ea80615dd009481a92f9ce3e6ee3482bb0e3` | 0 |
| lib/gperftools/src/windows/patch_functions.cc | 44638 | `b06800f7028b6d1d068b3593b49e8dd76359d06c8117b13bcc72ad592fc47bf6` | 0 |
| lib/gperftools/src/windows/port.cc | 8896 | `325d52309d1dd96fd7ec72ff70dca0e3232c4be7456ccf8c9c3f139db6d08ec9` | 0 |
| lib/gperftools/src/windows/port.h | 9593 | `d9b8db9df2150e68ebcd5e81b6b29b7d0813f7f6b20a858838373a6ff39257a4` | 0 |
| lib/gperftools/src/windows/preamble_patcher.cc | 29219 | `eb2fe21b4c97665255e16e3a69c990d7974b5e31f907a041a38a5777763682de` | 0 |
| lib/gperftools/src/windows/preamble_patcher.h | 26465 | `5d207dcd181720dcd3089eae40bbc45db6c495d0f527b2581e20c87d5fe5c40a` | 0 |
| lib/gperftools/src/windows/preamble_patcher_with_stub.cc | 13721 | `8142829ce257280332f7769ebfb2b39969e3b095a839a1de5b9c910977d5262f` | 0 |
| lib/gperftools/src/windows/system-alloc.cc | 7122 | `fe4b8bd42f6b63902db26d331a74637ce876b0fc822291a6fc6e3996c7bfe29c` | 0 |
| lib/gperftools/vendor/googletest/googlemock/include/gmock/gmock-actions.h | 92120 | `33a0c0b7fd9de0d8478d6160da1c6d55ce138a78d66bc50116356094cf990934` | 0 |
| lib/gperftools/vendor/googletest/googlemock/include/gmock/gmock-cardinalities.h | 6118 | `a565787f3e15f81e1873d1ff9d97888ab1e37466165258cfffd6d4bafc086214` | 0 |
| lib/gperftools/vendor/googletest/googlemock/include/gmock/gmock-function-mocker.h | 25796 | `1c7f47551aace89c30eb88563d4b1f147bdd368c25e10c1744673c4945c558c8` | 0 |
| lib/gperftools/vendor/googletest/googlemock/include/gmock/gmock-matchers.h | 222884 | `ad1b592dccb23f72c6d78fd371e69eb64eea8eb6bad1f5417bcfe92c804cd59e` | 0 |
| lib/gperftools/vendor/googletest/googlemock/include/gmock/gmock-more-actions.h | 38344 | `76db139ecd8af4272f979fa996e06ef52ba21d7cb1c6dc7f476fbbec1b3bac1f` | 0 |
| lib/gperftools/vendor/googletest/googlemock/include/gmock/gmock-more-matchers.h | 4499 | `b5dfa602f4f05a92000fffe06236cbbadb20bda8e1a4e55b1cddf27ba586232f` | 0 |
| lib/gperftools/vendor/googletest/googlemock/include/gmock/gmock-nice-strict.h | 10858 | `75324d2f796da7d611fb5d1da610c905f53e74247b02982ca63f5dcb91f4c33c` | 0 |
| lib/gperftools/vendor/googletest/googlemock/include/gmock/gmock-spec-builders.h | 82086 | `9a2bc69d5de83a18d813f1134c1249c35302bc37d7f815ee49252552d6e1d2b1` | 0 |
| lib/gperftools/vendor/googletest/googlemock/include/gmock/gmock.h | 3954 | `de3d73bc68ecffacc4935db34ea651b436cf4394ce61fb100b5dab1a5ff155d7` | 0 |
| lib/gperftools/vendor/googletest/googlemock/include/gmock/internal/custom/gmock-generated-actions.h | 314 | `8efd16064b3e19d98726a15f8bc40daa593576e4a190b2e8b95a6fee7242c36f` | 0 |
| lib/gperftools/vendor/googletest/googlemock/include/gmock/internal/custom/gmock-matchers.h | 1918 | `b6d245e95f0649a85aa7e29457f437da4c2f1fbadb0402cfc40f680159de510f` | 0 |
| lib/gperftools/vendor/googletest/googlemock/include/gmock/internal/custom/gmock-port.h | 1953 | `ee2cc87202e75759cfd98a5d657c69ee864e492a2c63584586938da81ab84995` | 0 |
| lib/gperftools/vendor/googletest/googlemock/include/gmock/internal/gmock-internal-utils.h | 19273 | `9b444dc928270691f5b0b92434d52ee7334bd6dcee9995db00564256ee702310` | 0 |
| lib/gperftools/vendor/googletest/googlemock/include/gmock/internal/gmock-port.h | 6472 | `459977819fbf723c19f781e55cbb0bba8cf395dc3ffb6f9e4b508103a58db3fb` | 0 |
| lib/gperftools/vendor/googletest/googlemock/include/gmock/internal/gmock-pp.h | 13491 | `5fcdad1707b172f8000d9f419f41d44318558600b00916785516eae49843bb4f` | 0 |
| lib/gperftools/vendor/googletest/googlemock/src/gmock-all.cc | 2107 | `166fc3f915d7abcb66f2b1d5cb31c13237838d3464d4de3015dcac00b9d354cd` | 0 |
| lib/gperftools/vendor/googletest/googlemock/src/gmock-cardinalities.cc | 5330 | `2203e2d2a37d96a97e06a9b9c20d516fbecc964f1e37d9d3029d774dff7abc43` | 0 |
| lib/gperftools/vendor/googletest/googlemock/src/gmock-internal-utils.cc | 9460 | `483c1e41ba20638c42a84f1a6ea38b53a480b020e3f79770d6f3c1d65b583045` | 0 |
| lib/gperftools/vendor/googletest/googlemock/src/gmock-matchers.cc | 18644 | `3d770fbfe37641b2e9f005c7ec5ada5daa7462794f7ce70a48c23e512c262f4a` | 0 |
| lib/gperftools/vendor/googletest/googlemock/src/gmock-spec-builders.cc | 29379 | `e4854e213cc766c4f2971d26679b85000684461332413c3de3c35a8dbe114ba3` | 0 |
| lib/gperftools/vendor/googletest/googlemock/src/gmock.cc | 8547 | `1376daf6387eac94b5afaf2dfbf2e3aac098b5f97985f3f5660ab3f7d4948452` | 0 |
| lib/gperftools/vendor/googletest/googlemock/src/gmock_main.cc | 3092 | `6c6f3fe5baaf769d384503793c3f44a59e1796bafe58f1eb37012944eb75bc18` | 0 |
| lib/gperftools/vendor/googletest/googletest/include/gtest/gtest-assertion-result.h | 8703 | `26e1b24865009327384eb87a3839bd89e73fd85e2dbb72d108361283b2710bc4` | 0 |
| lib/gperftools/vendor/googletest/googletest/include/gtest/gtest-death-test.h | 14917 | `ed31824987ec67ecd85a40a1be3b26293b22e888c9b73833e4e371cfc6add0f0` | 0 |
| lib/gperftools/vendor/googletest/googletest/include/gtest/gtest-matchers.h | 33848 | `4b45c1c6ae19e9506920affe8862a144d7a8a5ef5f73020df12118e8a57e8680` | 0 |
| lib/gperftools/vendor/googletest/googletest/include/gtest/gtest-message.h | 9147 | `f31bd107af1abe237bfb85cb09966571c7aa63a6c96a06f89352f382d5e38989` | 0 |
| lib/gperftools/vendor/googletest/googletest/include/gtest/gtest-param-test.h | 26376 | `7a246e017cb84010ae4bad5b6f789fb16941b4e46a130ffb8de9f328fa19ee78` | 0 |
| lib/gperftools/vendor/googletest/googletest/include/gtest/gtest-printers.h | 43992 | `b575b25d8ff1a57e2483e4e26b6aa64e6a1f0fc80cb49af569f26d9615fb1ff5` | 0 |
| lib/gperftools/vendor/googletest/googletest/include/gtest/gtest-spi.h | 12843 | `fc0bbebaeb211b81a2ec3df388e5e5f25a7c22e90186839854d2e5b26ce226e6` | 0 |
| lib/gperftools/vendor/googletest/googletest/include/gtest/gtest-test-part.h | 7164 | `2279b9bfd08aff7c0f764a2716bde0d3a61dc12573687a2cff91256b17681bf0` | 0 |
| lib/gperftools/vendor/googletest/googletest/include/gtest/gtest-typed-test.h | 15809 | `725a870e66409ce0d3bc8a6c1bfa7c71d8599602448509bf56ac5eaeb0de6987` | 0 |
| lib/gperftools/vendor/googletest/googletest/include/gtest/gtest.h | 92636 | `d7f3bb2a0ae21d13bb65243aef9ca31e09bc850247f2473ec2f4b81f20509ed9` | 0 |
| lib/gperftools/vendor/googletest/googletest/include/gtest/gtest_pred_impl.h | 12783 | `85e850e735a42ebb5f9a01a018708c1c0b9b7d83c94b14b7d5d29512c00b6ffd` | 0 |
| lib/gperftools/vendor/googletest/googletest/include/gtest/gtest_prod.h | 2502 | `3c6301ef533db8686e474dd5a0de4d98a31cbb630e2273f712472d1be25aa261` | 0 |
| lib/gperftools/vendor/googletest/googletest/include/gtest/internal/custom/gtest-port.h | 1873 | `5e06747c9e8b86e9d841fabd61c2f045b2bb1133716f127be4a963ced1c44e01` | 0 |
| lib/gperftools/vendor/googletest/googletest/include/gtest/internal/custom/gtest-printers.h | 2094 | `b95afda2426e8c4f09c11d3296d522fb336b248c0da7e078388db4bb072c2166` | 0 |
| lib/gperftools/vendor/googletest/googletest/include/gtest/internal/custom/gtest.h | 1858 | `21d20a1c64ea38c20c4b12337c261a1a18989d2a30710a83dfb5cd9a3bb3c55e` | 0 |
| lib/gperftools/vendor/googletest/googletest/include/gtest/internal/gtest-death-test-internal.h | 13854 | `7089f8bc0f0d880aa7ed99c8ba091270dc6fdc7af83f6ce2e55172ca7dc7013f` | 0 |
| lib/gperftools/vendor/googletest/googletest/include/gtest/internal/gtest-filepath.h | 10552 | `71c925cac74a844d5da43bdec9d4f3196cdef80df54ad13ad8dd7192587ce3ea` | 0 |
| lib/gperftools/vendor/googletest/googletest/include/gtest/internal/gtest-internal.h | 61548 | `f3745bd2715e459cf06dc36218fe57e217d27dfc71689fbbe2af28aed9055b17` | 0 |
| lib/gperftools/vendor/googletest/googletest/include/gtest/internal/gtest-param-util.h | 39712 | `4a80c7d76380d172ae2948c8ab3075ba8df6ab5eb82f44e0089ccac692c5a3bd` | 0 |
| lib/gperftools/vendor/googletest/googletest/include/gtest/internal/gtest-port-arch.h | 4392 | `36c1e834eef0cdb6a1c0dc69c9f6896d1b974a85c3bfd43ff8b839dc77d96e2b` | 0 |
| lib/gperftools/vendor/googletest/googletest/include/gtest/internal/gtest-port.h | 86382 | `5053b8bada9e8d17847cc295a941c40f8cb59cffc38df756a4b9b9f08fb35303` | 0 |
| lib/gperftools/vendor/googletest/googletest/include/gtest/internal/gtest-string.h | 7323 | `0cc08c746bceb2b101c61ffbc905c598eb62fee3c262c4585c21b10d8a3e6508` | 0 |
| lib/gperftools/vendor/googletest/googletest/include/gtest/internal/gtest-type-util.h | 7324 | `94336b1703807db6d9d2b729b5a30cf53016fd236b14774af118467d27f94ad8` | 0 |
| lib/gperftools/vendor/googletest/googletest/src/gtest-all.cc | 2201 | `972d3016860f9aa6452e078cf77406290fb7003b66fd6c0744a030bd1c323606` | 0 |
| lib/gperftools/vendor/googletest/googletest/src/gtest-assertion-result.cc | 3009 | `dbd2235676dcc0ef6409108a4041e05442fc6895735a5561d71151e6a14296bb` | 0 |
| lib/gperftools/vendor/googletest/googletest/src/gtest-death-test.cc | 62728 | `2881240c49961c095505f3c044483a79ef1c32e413e19630af7508d67994f619` | 0 |
| lib/gperftools/vendor/googletest/googletest/src/gtest-filepath.cc | 15726 | `b3d0011edbb81f782b88aac6ea20d04b24050e5738b3b2240a22033f675cb71f` | 0 |
| lib/gperftools/vendor/googletest/googletest/src/gtest-internal-inl.h | 48421 | `08c71f523cdf25a1c8ddcab54ee4ba3821c86273903ef16c54dc1bfd953fc220` | 0 |
| lib/gperftools/vendor/googletest/googletest/src/gtest-matchers.cc | 3724 | `e4ce9edf33493625353cc147a14caac14fdba7390d76166d101fa2fe9d16bbda` | 0 |
| lib/gperftools/vendor/googletest/googletest/src/gtest-port.cc | 49585 | `5efb91d426e321925787a13a5915c082db6c237eda42f288bacf86a1d1ae601f` | 0 |
| lib/gperftools/vendor/googletest/googletest/src/gtest-printers.cc | 18617 | `e0606758fe2faf77004d19502e093254b1f15b1d94d390f6590b075ae6c40761` | 0 |
| lib/gperftools/vendor/googletest/googletest/src/gtest-test-part.cc | 4028 | `b268314cbc718b485ff3e45fdeb5a1496bb8d87dadd5e824c558bf3b03e2dbf9` | 0 |
| lib/gperftools/vendor/googletest/googletest/src/gtest-typed-test.cc | 3823 | `b92e70b2d7ee3b86328162cbda269a28de4ce67f0e8d9beec5ec2c73a93ba006` | 0 |
| lib/gperftools/vendor/googletest/googletest/src/gtest.cc | 267916 | `2474ebe23fe042ecfe7c5a78788cc43e882a2abacf3952936bfc2ead48cebcfb` | 0 |
| lib/gperftools/vendor/googletest/googletest/src/gtest_main.cc | 2430 | `3836c1ce7c4829c44a30f368d888ae3bed218437d61d102c50c0db4afca33b3f` | 0 |
| lib/gperftools/vendor/libbacktrace-integration/backtrace-alloc.cc | 8509 | `f7c736df08d484cd1f40d9d0cf35f3a1143455d79d36304df2d23de6953136b1` | 0 |
| lib/gperftools/vendor/libbacktrace-integration/backtrace-supported.h | 192 | `b31fbaaa92aca49d0516fdc2ed9b9857cec0af382b3c56e1c8b976ada8308ec7` | 0 |
| lib/gperftools/vendor/libbacktrace-integration/config.h | 3940 | `a9a1f4fc3207c5a16404505c39a9195fcea8fd56f986382f721dc7b852bc8d55` | 0 |
| lib/gperftools/vendor/libbacktrace-integration/file-format.c | 258 | `91e6b04258cf292a1a69104230508bbb85549de248452ae6e1d67f8a13158579` | 0 |
| lib/gperftools/vendor/libbacktrace/alloc.c | 4445 | `40fa7aaa389370da6d8533855198a48b5ce8c457dac708f3fa59f07356b9d765` | 0 |
| lib/gperftools/vendor/libbacktrace/allocfail.c | 3486 | `c98c880a89f17a06931cb2dbb4993bc11411e3c8ddcaadfd44062101952f0b37` | 0 |
| lib/gperftools/vendor/libbacktrace/atomic.c | 2956 | `8d62c6408ed5f5fa0891b22b3b0eddde52cc6282bdde0aa8ff7a6aab20d92bdb` | 0 |
| lib/gperftools/vendor/libbacktrace/backtrace.c | 3748 | `3e9f9ee28fc150b913bdca1a6e1d7fab83b3b1797c399bc39da006e56f080c2c` | 0 |
| lib/gperftools/vendor/libbacktrace/backtrace.h | 8782 | `d2ac7d5c6910c011f860d04a04a4a6a6fbea2882f23878f1f5f6721831a28acd` | 0 |
| lib/gperftools/vendor/libbacktrace/btest.c | 11785 | `1c2194dabcfa22f8241612926d4adf244966e05db913d9b98f83c73e72de1497` | 0 |
| lib/gperftools/vendor/libbacktrace/dwarf.c | 122251 | `439170986c4ed3e0ee609011645c2b181e94b88b2d5ae35d4334956994fd2bd7` | 0 |
| lib/gperftools/vendor/libbacktrace/edtest.c | 3766 | `732b0a1e23e41212a468ab5d273e790081beb4d0e458641d9669f88a952a2bd3` | 0 |
| lib/gperftools/vendor/libbacktrace/edtest2.c | 1770 | `0bb1c382faeb9829a352613eb77ef9d3a99676a08ca8cd59f86971e8b9fc27aa` | 0 |
| lib/gperftools/vendor/libbacktrace/elf.c | 193096 | `5acab1e8823335c82e84877f502f887f61eae8b6f63ca74c714992a602213f13` | 0 |
| lib/gperftools/vendor/libbacktrace/fileline.c | 10902 | `639d8d581e93eaf18e1578e3b287b7f945260f001bb3c23eef48b250744b3bef` | 0 |
| lib/gperftools/vendor/libbacktrace/filenames.h | 2149 | `8d2c2d284c3f071a8b418c2ce71e42e48b48caa0c4485b7319a4afe82b236c36` | 0 |
| lib/gperftools/vendor/libbacktrace/instrumented_alloc.c | 3065 | `87cd6395c5161bec253cba42d814b4e5438a91b9bb293a14ece23ba8466f93c3` | 0 |
| lib/gperftools/vendor/libbacktrace/internal.h | 13831 | `0ccc73f08659683269cd5db058f5629a7b62c8bffc45f2fee5919d053aa18d8e` | 0 |
| lib/gperftools/vendor/libbacktrace/macho.c | 36514 | `7e5b72ee26d404477c172a2511213074d8ef82f8d01a66c196289ec20fae76c2` | 0 |
| lib/gperftools/vendor/libbacktrace/mmap.c | 8584 | `c6f638ca5629e0aebe63f578f9e3659b8fa22ebb2f0be20bf15f3bc5ef007055` | 0 |
| lib/gperftools/vendor/libbacktrace/mmapio.c | 3183 | `ebfa5fa59c292124510d6555d17f0872709b70c0ee0c6034e50d27aeb216cfe5` | 0 |
| lib/gperftools/vendor/libbacktrace/mtest.c | 9831 | `403be04a960c0c861404e7e1602866c028e8e2eae50c1b36b81290da05c85fa2` | 0 |
| lib/gperftools/vendor/libbacktrace/nounwind.c | 2337 | `c188891f00b1fa568698512ee76e199c74ee81a4a6daf592413b10c20d8b6b0f` | 0 |
| lib/gperftools/vendor/libbacktrace/pecoff.c | 28552 | `43bf474a5eebc984641838e38a8e74d7f4f95236cba6f3936c86b7d84147013d` | 0 |
| lib/gperftools/vendor/libbacktrace/posix.c | 3143 | `23d84b2eee48b645defc6e81b3a5b8dda1b1a7fe661f85591d93b21cdc8eb54e` | 0 |
| lib/gperftools/vendor/libbacktrace/print.c | 3541 | `3fb9dfe3a7e5c34026e271f0e95f657726502c895b54e79c78cddbfada926790` | 0 |
| lib/gperftools/vendor/libbacktrace/read.c | 3130 | `6903cbbe0f9f11a1d60fb89c0e8db5ae1bd31d721c857646d1efbe8b29c425dd` | 0 |
| lib/gperftools/vendor/libbacktrace/simple.c | 3213 | `95bca9ca4fea480e131bb3869d950a36a9b41b1fa673b75438f19150cc6bbaeb` | 0 |
| lib/gperftools/vendor/libbacktrace/sort.c | 3175 | `e372764bcf6a906daf82a4090530e42952d687b6aff9beebd51347224d901ce3` | 0 |
| lib/gperftools/vendor/libbacktrace/state.c | 2433 | `e88f2985847c9514a5d61b6dce0d062dc90be57a50a151f9da73cfd601ea8b0b` | 0 |
| lib/gperftools/vendor/libbacktrace/stest.c | 3434 | `b5b8d380237b244610127569a5755c78034f9a911ac22b056ae79f9bd7d4deec` | 0 |
| lib/gperftools/vendor/libbacktrace/testlib.c | 5867 | `df3819b03cb0773f8298e01d91e453dc5922d6f8a282d08c63d0768bdc253a22` | 0 |
| lib/gperftools/vendor/libbacktrace/testlib.h | 3280 | `e1c7714f3aba0900df66e913b52d617530a08074b413d3f6b0f01b25b957b543` | 0 |
| lib/gperftools/vendor/libbacktrace/ttest.c | 4276 | `df428a9cbfa314b32607a5b9ba02deeca994b7f5523280aaf6f5682edb600025` | 0 |
| lib/gperftools/vendor/libbacktrace/unittest.c | 2599 | `74136e820ef980220af5eef80dd0536ee6f54c1a7a6d678b0dcef3669705268d` | 0 |
| lib/gperftools/vendor/libbacktrace/unknown.c | 2418 | `7b57e16d0d4e64f81b7276d48e00089641f56b10b0793b5447c3d5961ff13724` | 0 |
| lib/gperftools/vendor/libbacktrace/xcoff.c | 41946 | `ff30acc0050487b4af76695e5662794792fb7b9d72e5d0bd41521f0b0c2e673f` | 0 |
| lib/gperftools/vendor/libbacktrace/xztest.c | 11938 | `5301fa31d53c24ba8391104597c3b1eaaa973f86974d184e5e52b732f2a67e29` | 0 |
| lib/gperftools/vendor/libbacktrace/zstdtest.c | 14478 | `415fb8ac60bdccc3f18daadd0e30b4eb112459fdcf012d5a54f26d04ff17e671` | 0 |
| lib/gperftools/vendor/libbacktrace/ztest.c | 15022 | `618a6cc4f9e33d450acb6e108563923e192a6b49916392ff0cca4794aa68f4fc` | 0 |
| lib/gperftools/vsprojects/include/config.h | 5130 | `1602f96994e72923a369b26f295e2a6a58619dded76dc3ae39733ec9ec03dbed` | 0 |
| lib/libmedida/doc/js/bootstrap.min.js | 25563 | `fe8aead0b04ede75588da9410ba730c7d8bde6deefd700fa5117d7b8352fd245` | 0 |
| lib/libmedida/src/medida/buckets.cc | 2738 | `45bbc83747da185f52223f05d17795faa10ae974d0a5b3ed847fe816d4bc492b` | 0 |
| lib/libmedida/src/medida/buckets.h | 1233 | `57a0661296bd435d7c5c6118ecfa11ba7b8ba6f58348bbb2375c55d49ace951b` | 0 |
| lib/libmedida/src/medida/counter.cc | 1550 | `b840f4b56e2d1432e63bc972290c815d3651b886252f58eebd7cc9c148319d7d` | 0 |
| lib/libmedida/src/medida/counter.h | 588 | `a040b1d1a46f578d92743a26eeb625ec68b87288094da014d4b310495370c676` | 0 |
| lib/libmedida/src/medida/histogram.cc | 6279 | `f5b79d42aa8295b1c5a45ec6c8c4df3b3f82d655bf052fc97313ad6a7e2ef280` | 0 |
| lib/libmedida/src/medida/histogram.h | 1736 | `b85938ff308fca398678bf554655d53345564ab44b126704d9d5206b6c6d6a37` | 0 |
| lib/libmedida/src/medida/medida.h | 301 | `42625b680ab510016854f61432f2d6fcce71da023f050a42cfa8efd330268ea6` | 0 |
| lib/libmedida/src/medida/meter.cc | 5209 | `99cc11ba5f312ff38ea284fe41f5fbbce189e579343bd502cbcb1d758ee34f72` | 0 |
| lib/libmedida/src/medida/meter.h | 998 | `cd62238f83fb66caf3f10cd015fda33fc3ff356a895b9b213487aebb9b8b1262` | 0 |
| lib/libmedida/src/medida/metered_interface.h | 620 | `c3571e3a69435eb6ada70cc023c3d34e96ec2b5be90027f64905b5bd4a6f71a0` | 0 |
| lib/libmedida/src/medida/metric_interface.h | 357 | `31b9f9c3df6264d8b240d9fded2d50c39dbb6ab0f20b3d284e8dc20a388af9de` | 0 |
| lib/libmedida/src/medida/metric_name.cc | 3364 | `92da1ce25aad6f831da8838aec498e1bf1f82ee1869e6f1276ed6c2b071cc0af` | 0 |
| lib/libmedida/src/medida/metric_name.h | 854 | `8cabb3dfc17007ceabcd0aa2db3a7fd42d947e0d6048f52ddd5996331713ebd2` | 0 |
| lib/libmedida/src/medida/metric_processor.cc | 488 | `283f9043190ec619ae9c8f0ff0208b419864d4f0c42bb0a867a97ae8a08b7b26` | 0 |
| lib/libmedida/src/medida/metric_processor.h | 612 | `0cc5f4317acf7d551cb2243d0d0c49fca966247d3821412e68bffe802e43b505` | 0 |
| lib/libmedida/src/medida/metrics_registry.cc | 4589 | `97763ffa68d724c2c269a10b14931f0f6e6bde64bcd852de8a1ca89e1647bf43` | 0 |
| lib/libmedida/src/medida/metrics_registry.h | 1542 | `189db27d9468964def55e0e290357a265bae0b0c60cbaa835d5fab8960645d12` | 0 |
| lib/libmedida/src/medida/reporting/abstract_polling_reporter.cc | 1605 | `53acf742eebf82dbb7a4f395867411efd5b1e281b4cf21a4e70b5068611ca8fe` | 0 |
| lib/libmedida/src/medida/reporting/abstract_polling_reporter.h | 632 | `d9fd270bbef4ea6039d8873b56521a349b728810d1b58590be3bdce96d89d566` | 0 |
| lib/libmedida/src/medida/reporting/collectd_reporter.cc | 8600 | `d9eeb3e6b045a0ea60c7459815111828ec5320964e58c7f30f5ced2dc5b4e42d` | 0 |
| lib/libmedida/src/medida/reporting/collectd_reporter.h | 941 | `532ad6d0c3de36f14f5fe37394c23afc5bd5f250e4aec2a03498a26fe204d0b7` | 0 |
| lib/libmedida/src/medida/reporting/console_reporter.cc | 6300 | `db469981c642326ba81a1d9f6ac6614c1a44bbfcf69d24806652f543b8e0eaaa` | 0 |
| lib/libmedida/src/medida/reporting/console_reporter.h | 866 | `d8e6a8bc3b615bcc5411cfa6c815a9fed0622f0a715bd82ce8aa17a25f09b505` | 0 |
| lib/libmedida/src/medida/reporting/json_reporter.cc | 7613 | `41780b9fa837b1479172c2fb76a030862ac8319bf89eb919cc74b2b369955b60` | 0 |
| lib/libmedida/src/medida/reporting/json_reporter.h | 892 | `d32e2f3abd8832bfc770254c4a5639f71c1fc8813e0060dfc9ac1ce71fb6109c` | 0 |
| lib/libmedida/src/medida/reporting/util.cc | 886 | `80a0b895891c6f1ca814ce91d72c618cc6dc3d1fe1d66dd34cd518f08156fd86` | 0 |
| lib/libmedida/src/medida/reporting/util.h | 344 | `8253d7128fb23e81eb190b8b9959c2f10b205d570aece7801e369383e01496a3` | 0 |
| lib/libmedida/src/medida/sampling_interface.h | 418 | `226902fcbd1e178f5d27f5c7b4a6d5af255a8273143e93a5f165010937b74cba` | 0 |
| lib/libmedida/src/medida/stats/ckms.cc | 8004 | `22ddc9ecbad39e6c0bc3f24aff2da765736c494775dd2c9539167580d2238a7f` | 0 |
| lib/libmedida/src/medida/stats/ckms.h | 1426 | `1a3f4787067686b634afe8110ef165ef9d7f01daa808f4dbc099f018ea1c1334` | 0 |
| lib/libmedida/src/medida/stats/ckms_sample.cc | 6330 | `fca12f0aa2bfcb44b35b4a9600c37fea42342092ccdbd589458a54afbb03800b` | 0 |
| lib/libmedida/src/medida/stats/ckms_sample.h | 2477 | `095c00d6f29778b11c28b59dce7bb8ea6a72dfd625c4daac498ab9a660e8012f` | 0 |
| lib/libmedida/src/medida/stats/ewma.cc | 3329 | `4bdeaebdce669f22a13486ecad1c5ba964bc5a5b305430898bfc47e1f73224c3` | 0 |
| lib/libmedida/src/medida/stats/ewma.h | 689 | `012e1f699a63d357ce8e3486ed54581b912950f5c3c9f61224080f8c7d8d360a` | 0 |
| lib/libmedida/src/medida/stats/exp_decay_sample.cc | 4074 | `0ec24d918f0f6ec214f3fa7312337588378167bb785ba4b8cf67c7c14e9586da` | 0 |
| lib/libmedida/src/medida/stats/exp_decay_sample.h | 787 | `87104e63210cf53dfa94fb789e679ece40a7432b7cf3f3d5b33b4154b4726ae5` | 0 |
| lib/libmedida/src/medida/stats/sample.h | 778 | `15092cb8cfb3ce148dcdb4d6c17a072058d5f6882efb6f5d8512a78d199dc83e` | 0 |
| lib/libmedida/src/medida/stats/sliding_window_sample.cc | 7394 | `39cc26ce68019c4290be3c7811cc9fad1d0ec2d63c2cfe2a1ca04c8896b717d7` | 0 |
| lib/libmedida/src/medida/stats/sliding_window_sample.h | 1320 | `384ca36d74355169e75a369e7cf97963f62abaf2a4edb90b975b6d8bcede55fd` | 0 |
| lib/libmedida/src/medida/stats/snapshot.cc | 7534 | `db6a5655089a057628052a299f1e9c6f0b3a68813d7beb1059479bdde450edbb` | 0 |
| lib/libmedida/src/medida/stats/snapshot.h | 1041 | `db4da3d0df5b8358cd1695e0f2805afaab6c1865326e8cc83d2f6694ae1ed1c6` | 0 |
| lib/libmedida/src/medida/stats/uniform_sample.cc | 2389 | `822fc3091e8386dafe66db5160b1219317d415b13f7f0df786771e57d7eb687f` | 0 |
| lib/libmedida/src/medida/stats/uniform_sample.h | 672 | `e69e560ed2fed271bacc77e4be290c86176ff9d76661303d6d3ed8d623f05cef` | 0 |
| lib/libmedida/src/medida/summarizable_interface.h | 468 | `bfc9479ac5efdb60c2612dce38e3c37d91d230870818df222f7c67b5677940a3` | 0 |
| lib/libmedida/src/medida/timer.cc | 6267 | `8b67748924889ca1cd27c646a16209f40bac386d401bd89850659fa463cb0c63` | 0 |
| lib/libmedida/src/medida/timer.h | 1799 | `8684b93d216b729a2091fa0792824a8409be30d5efd3fbd7af27db3812c791d4` | 0 |
| lib/libmedida/src/medida/timer_context.cc | 1676 | `adbf53a90777c3afe0a7c0487b4a51ce0f707a2be91e692d8d7fbe964de49bdc` | 0 |
| lib/libmedida/src/medida/timer_context.h | 587 | `42e7fbd7fc5495316e4e488886c5b4d50dc013f7b1a347d87fc643a320c0180f` | 0 |
| lib/libmedida/src/medida/tracy.h | 263 | `2302617fdaccf6ff4844b18e4279ddc0a0db61c8cda0b890ed078f52f366755b` | 0 |
| lib/libmedida/src/medida/types.h | 273 | `e909ea1cd13976982d4977039f615fd64e0e3a247fc2662a17e0dd57fbfae819` | 0 |
| lib/libsodium/builds/msvc/resource.h | 387 | `564ceb99be50ffe51b1189e56c1f79fd2b2425ee07eefcee078e72e8944d2acc` | 0 |
| lib/libsodium/builds/msvc/version.h | 508 | `fa06ff06867b2d0e8449f1574f687d7d0bb4e268826017f585de52e0daaffe16` | 0 |
| lib/libsodium/packaging/dotnet-core/prepare.py | 10627 | `163e7a26bedb4e3c9ded143d7a18ec8bd927d1daf4ed42a88149b39d8daaa261` | 0 |
| lib/libsodium/regen-msvc/regen-msvc.py | 5097 | `9f0314b4e71f9640c96aaf3e65d7dec1b3a91c6b3241a6fc2d635cf1bad0745b` | 0 |
| lib/libsodium/src/libsodium/crypto_aead/aes256gcm/aesni/aead_aes256gcm_aesni.c | 41637 | `b4f47ed172754b876427f4ad3789c1b18a9777299ae44cde5f7b3eb076ad66fa` | 0 |
| lib/libsodium/src/libsodium/crypto_aead/chacha20poly1305/sodium/aead_chacha20poly1305.c | 14254 | `1d88a62bd4c28dd9d36974dc13981a2c19978ccaa7add04cfb486cc86ca3e494` | 0 |
| lib/libsodium/src/libsodium/crypto_aead/xchacha20poly1305/sodium/aead_xchacha20poly1305.c | 9406 | `26b35c0c0d49676817b3935cadc30e9f9e2c814f16916ea177767e78e5b1ea0d` | 0 |
| lib/libsodium/src/libsodium/crypto_auth/crypto_auth.c | 775 | `0949551db403830e60d0526a2074a12c9cdfc4772ea9706a6ed1e205b676d40c` | 0 |
| lib/libsodium/src/libsodium/crypto_auth/hmacsha256/auth_hmacsha256.c | 2947 | `b4074f8ee81ad6a3fe98ae144ecd6c68f61706ae297c2f78470c519a162fd9cd` | 0 |
| lib/libsodium/src/libsodium/crypto_auth/hmacsha512/auth_hmacsha512.c | 2953 | `804e3d9bf2e20d7d866a3fa1213fecf07c526a1d2a3d0adc0e94e546019e9b75` | 0 |
| lib/libsodium/src/libsodium/crypto_auth/hmacsha512256/auth_hmacsha512256.c | 2523 | `fd57c37bd05aa9f188e87ac30bdef3b267d3698887c40ee16f0f949646331125` | 0 |
| lib/libsodium/src/libsodium/crypto_box/crypto_box.c | 2383 | `8741972f4f816baaf1b7409cd6412b06f85b8d02ee9aef9161522f5591b50911` | 0 |
| lib/libsodium/src/libsodium/crypto_box/crypto_box_easy.c | 3676 | `a71a822831333a2c8a1780ad224861e0aa4bf665520c9e9428f323adfc90b0a8` | 0 |
| lib/libsodium/src/libsodium/crypto_box/crypto_box_seal.c | 1973 | `c9bed6c747a4c6446813a1a82edf3f4a995e11a8f9bf59c38a055d55200dd9d8` | 0 |
| lib/libsodium/src/libsodium/crypto_box/curve25519xchacha20poly1305/box_curve25519xchacha20poly1305.c | 6514 | `f7933b5b3d45003d6e1d3aac14b5eef62f8fa044d1819153937eaf70562583f0` | 0 |
| lib/libsodium/src/libsodium/crypto_box/curve25519xchacha20poly1305/box_seal_curve25519xchacha20poly1305.c | 3052 | `d72af55e9f5003a372b5d2bfa8dfe3ad76bc595ea683f6243d8f45b29ff48be1` | 0 |
| lib/libsodium/src/libsodium/crypto_box/curve25519xsalsa20poly1305/box_curve25519xsalsa20poly1305.c | 4576 | `64cec48c8189d560eb1400eedbaf591c2f40b31be258d6e4c3db09283deb1a70` | 0 |
| lib/libsodium/src/libsodium/crypto_core/ed25519/core_ed25519.c | 6055 | `2c0fcc4a2bf74addc68f65fad4f19e08d3ea785070193fbe09ed56811e6274f0` | 0 |
| lib/libsodium/src/libsodium/crypto_core/ed25519/core_ristretto255.c | 3611 | `96c19d211b82d436363609007c1318d54ad9fe03666ba986c85e6882ec014300` | 0 |
| lib/libsodium/src/libsodium/crypto_core/ed25519/ref10/ed25519_ref10.c | 79518 | `e02f51605807a0fe8c00f16e862f4b256373cbb6149dfe92712bc6a9d0187926` | 0 |
| lib/libsodium/src/libsodium/crypto_core/ed25519/ref10/fe_25_5/base.h | 85502 | `4b55044010ee8b7270b5b58f3d064e1a5798966f3ecd317f287cb2ff61751fbc` | 0 |
| lib/libsodium/src/libsodium/crypto_core/ed25519/ref10/fe_25_5/base2.h | 2579 | `2ee371b7a19b20d076a93b47e06b0d8d7305a6e4501b7002ae16572aa19a258f` | 0 |
| lib/libsodium/src/libsodium/crypto_core/ed25519/ref10/fe_25_5/constants.h | 1362 | `a464a4aab2e6498d3201b83cab31833663bbee18f786b852a74a4f89cb012437` | 0 |
| lib/libsodium/src/libsodium/crypto_core/ed25519/ref10/fe_25_5/fe.h | 5787 | `6fde442ea8b8a6f252948168ceb9f203abfd48f4e00c3cdd4070e26a4e28ef9e` | 0 |
| lib/libsodium/src/libsodium/crypto_core/ed25519/ref10/fe_51/base.h | 75894 | `ed3ae74d98c89ac5a3aebada53e7ddb22d00c1968b7838d04a10665b4e651869` | 0 |
| lib/libsodium/src/libsodium/crypto_core/ed25519/ref10/fe_51/base2.h | 2280 | `0e6cecfa1747abd6f7a09d6119b33cd435fb4b88ed3811bc002d81ccccfbd29c` | 0 |
| lib/libsodium/src/libsodium/crypto_core/ed25519/ref10/fe_51/constants.h | 1254 | `6661adb3754c819987a75a03e44e2c478d260a06802dd1b7ec4e55281098dcc6` | 0 |
| lib/libsodium/src/libsodium/crypto_core/ed25519/ref10/fe_51/fe.h | 2473 | `a96a476b0a0615636b5867e8a80f1f18c1084fd6d59a7967203a54bf090082fd` | 0 |
| lib/libsodium/src/libsodium/crypto_core/hchacha20/core_hchacha20.c | 2232 | `9c891c646f9e6ec20d0597464d5d987512697a3d5b00051ad9ed67501ebdecc9` | 0 |
| lib/libsodium/src/libsodium/crypto_core/hsalsa20/core_hsalsa20.c | 408 | `ecb3514e479cc993366542f9efe71de9aafd8f439cf9223f4ab0d97e9b97625a` | 0 |
| lib/libsodium/src/libsodium/crypto_core/hsalsa20/ref2/core_hsalsa20_ref2.c | 2571 | `d9fdd18eeaaf6964ecb30eee30314a32abd10360c660af253cdab83826026a13` | 0 |
| lib/libsodium/src/libsodium/crypto_core/salsa/ref/core_salsa_ref.c | 4852 | `140bc08136a05e0d57aa829a5b49969d72a826602a2cbd4f0e0589f195750b4c` | 0 |
| lib/libsodium/src/libsodium/crypto_generichash/blake2b/generichash_blake2.c | 1216 | `dc60a6a9b7f2f668853596a547282ca47eb6b1a978a8906d93ce4d103e6bad44` | 0 |
| lib/libsodium/src/libsodium/crypto_generichash/blake2b/ref/blake2.h | 4543 | `cea6d217a1abb7058dbbafcf931fa65fe41a0a688d4b6b3a4e10ec972988f965` | 0 |
| lib/libsodium/src/libsodium/crypto_generichash/blake2b/ref/blake2b-compress-avx2.c | 1160 | `14a070b5b301f7dd023075c2929fb88697b83a438eedbdab11ec136994156343` | 0 |
| lib/libsodium/src/libsodium/crypto_generichash/blake2b/ref/blake2b-compress-avx2.h | 6101 | `26c3ff51405c94c2ce87beb4b4daf20afa196d0393a64b04fec70c21ea665d1d` | 0 |
| lib/libsodium/src/libsodium/crypto_generichash/blake2b/ref/blake2b-compress-ref.c | 2971 | `5b4b29ee9562bd821da2d6d2f65902a8b5b834ecac049a5f1af1e1405646a640` | 0 |
| lib/libsodium/src/libsodium/crypto_generichash/blake2b/ref/blake2b-compress-sse41.c | 2593 | `4f3de0b056a86ef2090ebf5a1db98238df56c607fa7cfaee8aa4f3359e6cb644` | 0 |
| lib/libsodium/src/libsodium/crypto_generichash/blake2b/ref/blake2b-compress-sse41.h | 6719 | `5a020c1492aef02727826f64056cf8725f79c30cd8aa7fb43f287ce1578f11f4` | 0 |
| lib/libsodium/src/libsodium/crypto_generichash/blake2b/ref/blake2b-compress-ssse3.c | 2930 | `2507623162b653296bca9feff58d4c0e67c8f2d3fda7babf6698beb0eb9fad43` | 0 |
| lib/libsodium/src/libsodium/crypto_generichash/blake2b/ref/blake2b-compress-ssse3.h | 6718 | `09c9c525c9505247fc2425d0cbe10d32805c91e06c3d4309f76be2f89a63482b` | 0 |
| lib/libsodium/src/libsodium/crypto_generichash/blake2b/ref/blake2b-load-avx2.h | 12810 | `426c1ca62b54d40606f3665feca519e8e6899d161eec3a31d48bef335016c51e` | 0 |
| lib/libsodium/src/libsodium/crypto_generichash/blake2b/ref/blake2b-load-sse2.h | 5594 | `daa18d55dfaf3c9a29e7bf390ea0f92aaf291aa0d315d912ae0082fd61e0fe3f` | 0 |
| lib/libsodium/src/libsodium/crypto_generichash/blake2b/ref/blake2b-load-sse41.h | 10060 | `89a96cf99ea570e450f608c509c52f11cb9775de17d201ab0cc57805202a3ac2` | 0 |
| lib/libsodium/src/libsodium/crypto_generichash/blake2b/ref/blake2b-ref.c | 11817 | `b712bc4f00a81ecec8fef02825506334983fa99e549107dc175ff1f48e3b17f6` | 0 |
| lib/libsodium/src/libsodium/crypto_generichash/blake2b/ref/generichash_blake2b.c | 3977 | `6c6bb63b0c9944c215af776e7325489c087e49bc513bccf8e1a518db0b7fedde` | 0 |
| lib/libsodium/src/libsodium/crypto_generichash/crypto_generichash.c | 2037 | `dc974ba3ab8ffcbd2684df7a842ad79d641a3c47e6f3a033fc4876fe12f1fbce` | 0 |
| lib/libsodium/src/libsodium/crypto_hash/crypto_hash.c | 323 | `bdc3db640637230f93fa859bc2715ec5905d911d32817b2fdf3bbf787b98d293` | 0 |
| lib/libsodium/src/libsodium/crypto_hash/sha256/cp/hash_sha256_cp.c | 7939 | `1835e9e6e071d2d82a80d33359f3c90ab3a24bfd633e96f1b1536e3780838ee4` | 0 |
| lib/libsodium/src/libsodium/crypto_hash/sha256/hash_sha256.c | 205 | `27966cb51a4f2ccf00d226bbed169dca16246cbbed82fbfc2ca18f9b99829526` | 0 |
| lib/libsodium/src/libsodium/crypto_hash/sha512/cp/hash_sha512_cp.c | 9407 | `60f428ee3d3b124b45055b31aa93c2a71f86dcc37110f7fd103baa276fc7eef9` | 0 |
| lib/libsodium/src/libsodium/crypto_hash/sha512/hash_sha512.c | 205 | `fca3b25c288cff440005ac36c4247f8df5ff3d38117e260eae8366d78178b641` | 0 |
| lib/libsodium/src/libsodium/crypto_kdf/blake2b/kdf_blake2b.c | 1635 | `802fe22def270bacd8166a17a99259cb538c5e24a90efde0c266c487b3e83c95` | 0 |
| lib/libsodium/src/libsodium/crypto_kdf/crypto_kdf.c | 931 | `0279ed40772be2c0f8c03e134026ccd8da2d1c3f756e9cab4d978d68dfaca283` | 0 |
| lib/libsodium/src/libsodium/crypto_kx/crypto_kx.c | 4379 | `c48d3aceab62c58ce5f8a9e57c347d698b65e0181ad026dd75c279d4a02b3f15` | 0 |
| lib/libsodium/src/libsodium/crypto_onetimeauth/crypto_onetimeauth.c | 1691 | `f9ccd6b3801c5819855a24bc3a0ad3ed4a9f397d59286fd4b9cff2063051711e` | 0 |
| lib/libsodium/src/libsodium/crypto_onetimeauth/poly1305/donna/poly1305_donna.c | 3494 | `ccbfba9202f7f7e318043bc9eb518277fadd171082202f85676a8f800287bf32` | 0 |
| lib/libsodium/src/libsodium/crypto_onetimeauth/poly1305/donna/poly1305_donna.h | 293 | `fe81733c21c22b47b8217627d40709e0d2f96fbfa385f2346ce697b7cebdd89b` | 0 |
| lib/libsodium/src/libsodium/crypto_onetimeauth/poly1305/donna/poly1305_donna32.h | 6729 | `40536f083dfaa6c969e71cb941669e863b7c6a34321b1804421fea8b1af646bd` | 0 |
| lib/libsodium/src/libsodium/crypto_onetimeauth/poly1305/donna/poly1305_donna64.h | 5282 | `8f5aedb3a4ca75a90813aa542cac12f7fc44d82b944102a9500e6518bc4a6216` | 0 |
| lib/libsodium/src/libsodium/crypto_onetimeauth/poly1305/onetimeauth_poly1305.c | 2464 | `0bbd1eec53c47abe43246962c8e655f7c159d152205b107c09d189e8d92792ad` | 0 |
| lib/libsodium/src/libsodium/crypto_onetimeauth/poly1305/onetimeauth_poly1305.h | 1016 | `7481732850bbe2cfbf6034581dfb8ab17b9005d2d22afdb030319072d637d1d3` | 0 |
| lib/libsodium/src/libsodium/crypto_onetimeauth/poly1305/sse2/poly1305_sse2.c | 31319 | `058d06d9dac94916e76c70f8d34e2a2deab17056fa237a39bea530b81785e731` | 0 |
| lib/libsodium/src/libsodium/crypto_onetimeauth/poly1305/sse2/poly1305_sse2.h | 289 | `689ac732de5fbf2f1552306e76e2edaa55057512599a3e1dce32b84ebfb6defa` | 0 |
| lib/libsodium/src/libsodium/crypto_pwhash/argon2/argon2-core.c | 15653 | `1850c013dd9a764fed92eabe128855ff3ebd63b517075141c5e56b117203bdf2` | 0 |
| lib/libsodium/src/libsodium/crypto_pwhash/argon2/argon2-core.h | 10216 | `de8d5f5a2c0fd3c57f941ed72bf625f2d54afb3db09a6fe19ba1120c27656893` | 0 |
| lib/libsodium/src/libsodium/crypto_pwhash/argon2/argon2-encoding.c | 10254 | `9cee75b62668cab99398f595b9a571d3136fd6bc35e60679d9cfba25ccad25f2` | 0 |
| lib/libsodium/src/libsodium/crypto_pwhash/argon2/argon2-encoding.h | 1064 | `932ff34acb1861ba418b85ad69c66a214b2cb62bf941cf9eb8220b8f9aaa1e4e` | 0 |
| lib/libsodium/src/libsodium/crypto_pwhash/argon2/argon2-fill-block-avx2.c | 8023 | `8192730e7e3c335d3a1924893b832e83832a3e87c7a26615bd4ae964d4509036` | 0 |
| lib/libsodium/src/libsodium/crypto_pwhash/argon2/argon2-fill-block-avx512f.c | 8208 | `1ee75ff725441be5c6f493f14ab3e14e427fd2bd33c27a2ac2bc3e84c80caacb` | 0 |
| lib/libsodium/src/libsodium/crypto_pwhash/argon2/argon2-fill-block-ref.c | 8576 | `5fbbace0055d92056cdcd7621a9694de1ef7046542f710e1a478c04b0ab423ba` | 0 |
| lib/libsodium/src/libsodium/crypto_pwhash/argon2/argon2-fill-block-ssse3.c | 7943 | `b57e67f3c976bbfec062815b1ce0b3afc796c1bd80fea3868c60119c083408f7` | 0 |
| lib/libsodium/src/libsodium/crypto_pwhash/argon2/argon2.c | 8063 | `3621714cd3677ecd346819a1e2e8b3e446a1465a5f35c2a8da1a5deae43587d3` | 0 |
| lib/libsodium/src/libsodium/crypto_pwhash/argon2/argon2.h | 11085 | `ffc82383ad8ad1aaff540975379dbba370e7bd40c23cdf3260aab8cb4922d41a` | 0 |
| lib/libsodium/src/libsodium/crypto_pwhash/argon2/blake2b-long.c | 3137 | `37f1b01973dd484e009346bc46d7eb16e74d2f9b5186c29f2d8df4a1d286ef2d` | 0 |
| lib/libsodium/src/libsodium/crypto_pwhash/argon2/blake2b-long.h | 151 | `541220c3cd78acb15a80398a4b732e3ed7cf4b8fac531fb99c574b97ef826557` | 0 |
| lib/libsodium/src/libsodium/crypto_pwhash/argon2/blamka-round-avx2.h | 5847 | `abcfd03ed9a4d26ca96fe493925019f21cd44fb22738385e09aa554ba3d21ff5` | 0 |
| lib/libsodium/src/libsodium/crypto_pwhash/argon2/blamka-round-avx512f.h | 4569 | `256cd0cad160e7c30ee9243a5e796566645a708f8ae1e52d32fa24efc78d0fa6` | 0 |
| lib/libsodium/src/libsodium/crypto_pwhash/argon2/blamka-round-ref.h | 1555 | `619594355542219396a9545b4ee4afbb7eae8493784fb9aca01a72e3cd9021a3` | 0 |
| lib/libsodium/src/libsodium/crypto_pwhash/argon2/blamka-round-ssse3.h | 5451 | `60b0f267e9b16ae6af9017b1d1ce6977eecaef7b8894444fadd0b670d1624f00` | 0 |
| lib/libsodium/src/libsodium/crypto_pwhash/argon2/pwhash_argon2i.c | 7970 | `3bd2226d68477e867c3c955c7673a9db9d643f202b48cf01ed589a37485bf395` | 0 |
| lib/libsodium/src/libsodium/crypto_pwhash/argon2/pwhash_argon2id.c | 6382 | `378829c702b6d957e3ee0c694e62e623e98840e2925f3c3e0289402f4f3a3187` | 0 |
| lib/libsodium/src/libsodium/crypto_pwhash/crypto_pwhash.c | 4779 | `318a2d22a9f50f16fffccb7c61b61a578a7f608ea49cd87baa8ab5013fde795d` | 0 |
| lib/libsodium/src/libsodium/crypto_pwhash/scryptsalsa208sha256/crypto_scrypt-common.c | 7069 | `93de04c2711f75a886ad362ed6867782c4cfce611f468b71fb779ac377d563e2` | 0 |
| lib/libsodium/src/libsodium/crypto_pwhash/scryptsalsa208sha256/crypto_scrypt.h | 4130 | `6de9449b535cd5ee647138178c6e0b26f18052bc1061dd0861efc1614cc6db62` | 0 |
| lib/libsodium/src/libsodium/crypto_pwhash/scryptsalsa208sha256/nosse/pwhash_scryptsalsa208sha256_nosse.c | 10579 | `253fe57ef1abe3a4f35720477ffabfe73f31de42b9691a0d37ae7a15f13ee080` | 0 |
| lib/libsodium/src/libsodium/crypto_pwhash/scryptsalsa208sha256/pbkdf2-sha256.c | 3534 | `21a4267540c36c52ddada2dbd733e361f566ff41eca2594311b87f56bc93ffed` | 0 |
| lib/libsodium/src/libsodium/crypto_pwhash/scryptsalsa208sha256/pbkdf2-sha256.h | 1870 | `98e99b1ac7599d8acde7cc2a76f6b342ac1803278ddc65850100c2a13fd58142` | 0 |
| lib/libsodium/src/libsodium/crypto_pwhash/scryptsalsa208sha256/pwhash_scryptsalsa208sha256.c | 8658 | `2c5df00871269c03c01f765d55b7c26fa3cc4af958668af9534ab2f97e12a8a2` | 0 |
| lib/libsodium/src/libsodium/crypto_pwhash/scryptsalsa208sha256/scrypt_platform.c | 2862 | `2e6822a7217899484f1c7d02d35568696818daddbfc8c82f905a9ce551f58f6a` | 0 |
| lib/libsodium/src/libsodium/crypto_pwhash/scryptsalsa208sha256/sse/pwhash_scryptsalsa208sha256_sse.c | 12527 | `ef211264b7f41021ebf033baf845927d52fdb250c181a29cb0a968946e8d4e15` | 0 |
| lib/libsodium/src/libsodium/crypto_scalarmult/crypto_scalarmult.c | 579 | `3aa1ce5272c4d77a0b03791becff2949a82db8c590dc10a423802984cbc08e99` | 0 |
| lib/libsodium/src/libsodium/crypto_scalarmult/curve25519/ref10/x25519_ref10.c | 5809 | `43c5c77e287775cc576a6ef64a6f669169ef8aecf8fb4fff791e5607137c611a` | 0 |
| lib/libsodium/src/libsodium/crypto_scalarmult/curve25519/ref10/x25519_ref10.h | 249 | `b9d6e13c9065f7f6f5d9fbff21f28bbc4956967b9bde802df172194702a05a9f` | 0 |
| lib/libsodium/src/libsodium/crypto_scalarmult/curve25519/sandy2x/consts_namespace.h | 906 | `7d2dd849708eafd885e6b72f38094a78bb75b13fbf581663b4882399b61ea5d6` | 0 |
| lib/libsodium/src/libsodium/crypto_scalarmult/curve25519/sandy2x/curve25519_sandy2x.c | 2555 | `b71a538b73766b07313cf982af1fefdec0be8592b993624d872d21d74fa8dce9` | 0 |
| lib/libsodium/src/libsodium/crypto_scalarmult/curve25519/sandy2x/curve25519_sandy2x.h | 225 | `3cd4f3ecc9f202e64c88a134452e4a23d1ce67b404935b73ed50280b32865859` | 0 |
| lib/libsodium/src/libsodium/crypto_scalarmult/curve25519/sandy2x/fe.h | 550 | `2274ea02748ade547d39084c2f5b41cd7f068ec2b648d2bf7dd6a55b07299a96` | 0 |
| lib/libsodium/src/libsodium/crypto_scalarmult/curve25519/sandy2x/fe51.h | 614 | `034410eea5c360bdb5ed5e2258e4d260363cececf00bbdad78369ca0e4463561` | 0 |
| lib/libsodium/src/libsodium/crypto_scalarmult/curve25519/sandy2x/fe51_invert.c | 1482 | `572e6a03f0f172c6d3f78ae9ad8df4e3b28215074220bf146fd707db3acaba57` | 0 |
| lib/libsodium/src/libsodium/crypto_scalarmult/curve25519/sandy2x/fe51_namespace.h | 753 | `74b2538f5ce69a87716264c763de047f31308a6e5a7cd912925b6ecd1b619ac6` | 0 |
| lib/libsodium/src/libsodium/crypto_scalarmult/curve25519/sandy2x/fe_frombytes_sandy2x.c | 1790 | `5bc870db6fcd8b2f52bde8b0a5a47e799ca361b1eaac98190c0258c81a5b108d` | 0 |
| lib/libsodium/src/libsodium/crypto_scalarmult/curve25519/sandy2x/ladder.h | 231 | `d4fddfc1d132c0b00ae8b50624c74de133e156dc498628eedcdb87a2c1c18fe1` | 0 |
| lib/libsodium/src/libsodium/crypto_scalarmult/curve25519/sandy2x/ladder_base.h | 256 | `4fb8a727d842fd44a660e677d9487045c6f0a1bd07f8d117c55c3b9a57e90e67` | 0 |
| lib/libsodium/src/libsodium/crypto_scalarmult/curve25519/sandy2x/ladder_base_namespace.h | 253 | `5d81a455988ec7b3ba673de0f027db4d5a54b634416dcb7df96a707898ed427c` | 0 |
| lib/libsodium/src/libsodium/crypto_scalarmult/curve25519/sandy2x/ladder_namespace.h | 218 | `3389364a25ea0a948f0fabe97635aff03cdb5f9d59fc21a1ae1c55c18aa968c3` | 0 |
| lib/libsodium/src/libsodium/crypto_scalarmult/curve25519/scalarmult_curve25519.c | 1427 | `64f473f5069dcb892b196019475f31f571ba46ac79ba31047010c2c506dafb87` | 0 |
| lib/libsodium/src/libsodium/crypto_scalarmult/curve25519/scalarmult_curve25519.h | 341 | `c887fe855f943cb70a0967bba811f9ac97d254f213930d96e9fb2ffdc71015e1` | 0 |
| lib/libsodium/src/libsodium/crypto_scalarmult/ed25519/ref10/scalarmult_ed25519_ref10.c | 2721 | `813a32242f69796468f434b3bca15d8abb8c2406f426945651ffbaec6b1cf717` | 0 |
| lib/libsodium/src/libsodium/crypto_scalarmult/ristretto255/ref10/scalarmult_ristretto255_ref10.c | 1313 | `6799f10cd14c621ef6fe4ad3fd39206756039ab79c1d70d6bfcd45e64ca6c164` | 0 |
| lib/libsodium/src/libsodium/crypto_secretbox/crypto_secretbox.c | 1295 | `7c9a3e3a11e709094c3c5fbdf0851810427dbca514c69bb22aabd97c148731a3` | 0 |
| lib/libsodium/src/libsodium/crypto_secretbox/crypto_secretbox_easy.c | 4915 | `6ff8e9d9420c898c99631d484a562abc5042c7ef6b5559e6765097449200f2c2` | 0 |
| lib/libsodium/src/libsodium/crypto_secretbox/xchacha20poly1305/secretbox_xchacha20poly1305.c | 6343 | `495923b6fc551cc10e667ebf031776a1ae3744d1445e1ffac0dfa767b4fd1a63` | 0 |
| lib/libsodium/src/libsodium/crypto_secretbox/xsalsa20poly1305/secretbox_xsalsa20poly1305.c | 2252 | `58d45fe808876822dd31820190dfe94da3a0c17d7451c1e66190d321f0d2abc9` | 0 |
| lib/libsodium/src/libsodium/crypto_secretstream/xchacha20poly1305/secretstream_xchacha20poly1305.c | 11380 | `b9bd13b46d0d0332c69069d3f829fcf30d267e584a998a6379f8a89b9b3ffb22` | 0 |
| lib/libsodium/src/libsodium/crypto_shorthash/crypto_shorthash.c | 629 | `b4f5e2bd83496b9ef0c5334c104f9c6a4e2dc1b8f46dc12a5de01c3de3900fc0` | 0 |
| lib/libsodium/src/libsodium/crypto_shorthash/siphash24/ref/shorthash_siphash24_ref.c | 1697 | `04f3d382837c2589d3959ff44351b716e55c16a886297aefcda0b77b272d5796` | 0 |
| lib/libsodium/src/libsodium/crypto_shorthash/siphash24/ref/shorthash_siphash_ref.h | 606 | `51548a9d39274f75b1a0054d8b0318cd5f1ecb6d24b58e1e3a0c2fcf248b7f0a` | 0 |
| lib/libsodium/src/libsodium/crypto_shorthash/siphash24/ref/shorthash_siphashx24_ref.c | 1781 | `3df5a0a7b46d0f69be027879c8fa3ffb0be0b6b54e687fb24d2ef1b0121f2d25` | 0 |
| lib/libsodium/src/libsodium/crypto_shorthash/siphash24/shorthash_siphash24.c | 238 | `72465eaaa527e9d42b2d6dd645069b64e30402de973cc972f114688c85ef7c83` | 0 |
| lib/libsodium/src/libsodium/crypto_shorthash/siphash24/shorthash_siphashx24.c | 242 | `48cb227728cdae63b7dfe0246f8c6d7e998f4dfe57f53fd492a4157ffbca1f27` | 0 |
| lib/libsodium/src/libsodium/crypto_sign/crypto_sign.c | 2554 | `4ab49ce7800a6c828d314ecc1a5813bc1c133636a8d335ba17dea3ef85679229` | 0 |
| lib/libsodium/src/libsodium/crypto_sign/ed25519/ref10/keypair.c | 1978 | `ef0d2cde816c39e4fd6d61a37e33fbbcd7192c78430477a763dada8822a319aa` | 0 |
| lib/libsodium/src/libsodium/crypto_sign/ed25519/ref10/obsolete.c | 3474 | `0af0f146518f46f8b43dce127703773bea129311701add64bd3874d14189248f` | 0 |
| lib/libsodium/src/libsodium/crypto_sign/ed25519/ref10/open.c | 2638 | `2b345bf78695844262832eb14d0655da3a815024db0d437791142ee3b34b062d` | 0 |
| lib/libsodium/src/libsodium/crypto_sign/ed25519/ref10/sign.c | 4364 | `b2d9233bf659ccfe5d038230aeb46104a3168ff7330a815800625c4bcfee9963` | 0 |
| lib/libsodium/src/libsodium/crypto_sign/ed25519/ref10/sign_ed25519_ref10.h | 823 | `1fec246674c8a39f8f3e0a2bd88713dd21bb02d6cb6b65a99b492148393ead79` | 0 |
| lib/libsodium/src/libsodium/crypto_sign/ed25519/sign_ed25519.c | 2245 | `d527cebb3656093aad67b2a231240997b76e9e88105618a9c56def4ba3641b54` | 0 |
| lib/libsodium/src/libsodium/crypto_stream/chacha20/dolbeau/chacha20_dolbeau-avx2.c | 4615 | `c35913b69aab652192e7f5a5fb05e01c6b86ce0432e3bc3aabfc9714308994a3` | 0 |
| lib/libsodium/src/libsodium/crypto_stream/chacha20/dolbeau/chacha20_dolbeau-avx2.h | 199 | `4bc87ed826dbf7beadd2b41c01bf6e7fb846ff941cd6e1c8da870310ec8aaab7` | 0 |
| lib/libsodium/src/libsodium/crypto_stream/chacha20/dolbeau/chacha20_dolbeau-ssse3.c | 4423 | `729df4cd33f1b6c54d420084c4bc8cac39da500a14651936a7b593c9c69e41cc` | 0 |
| lib/libsodium/src/libsodium/crypto_stream/chacha20/dolbeau/chacha20_dolbeau-ssse3.h | 200 | `26c77341fe9573788065f4ac77a2bd92bc55bab093c61518728ddc4abfd388a3` | 0 |
| lib/libsodium/src/libsodium/crypto_stream/chacha20/dolbeau/u0.h | 2872 | `19cf10cdd56122220d38647df58b5f7e331a75a00e2fa4d178225184b3fd7dd2` | 0 |
| lib/libsodium/src/libsodium/crypto_stream/chacha20/dolbeau/u1.h | 3168 | `455c1d8d854e274488f7b5b7659ad13c9ca5c3f28bad3f16e9be646abaf1d309` | 0 |
| lib/libsodium/src/libsodium/crypto_stream/chacha20/dolbeau/u4.h | 6574 | `b073331f5da9350214bcc6cd0905315b6af6a94245244cc628195f7ca43056c7` | 0 |
| lib/libsodium/src/libsodium/crypto_stream/chacha20/dolbeau/u8.h | 18061 | `020fda6dff06db8646bd973fd8d6c7a66b78af1774fbe1639b20b01225dcabb9` | 0 |
| lib/libsodium/src/libsodium/crypto_stream/chacha20/ref/chacha20_ref.c | 8466 | `a93ebb4cc15c590798cb095d48ed39eb5d8929fda7904ce148908485e38914c3` | 0 |
| lib/libsodium/src/libsodium/crypto_stream/chacha20/ref/chacha20_ref.h | 190 | `04942a791be36ecd42568d9ee34b751f4ff8a02d919fa8b16e1a6e604d246726` | 0 |
| lib/libsodium/src/libsodium/crypto_stream/chacha20/stream_chacha20.c | 5623 | `119f02db875d0b293631b3756884f659fb3c80754ac79857876e8d0cecff9c38` | 0 |
| lib/libsodium/src/libsodium/crypto_stream/chacha20/stream_chacha20.h | 947 | `91848ca3f4b7badcf29aa8b03d3179a20e4ff4d4662f64d42612a2b0a9a367b3` | 0 |
| lib/libsodium/src/libsodium/crypto_stream/crypto_stream.c | 919 | `c22d3728361f741eb89c220d0f2289168e1cf4ccc129f4bf6f6858dc209184f3` | 0 |
| lib/libsodium/src/libsodium/crypto_stream/salsa20/ref/salsa20_ref.c | 2665 | `e47d9a29430d6ee4d2f7789e309984bf98997b3e5e7665f4efb006b705d50fc2` | 0 |
| lib/libsodium/src/libsodium/crypto_stream/salsa20/ref/salsa20_ref.h | 186 | `6ae5115492511b18007b3561562d83b09248a8f34f86318813ced358ee7622fb` | 0 |
| lib/libsodium/src/libsodium/crypto_stream/salsa20/stream_salsa20.c | 2770 | `3c61a4a21512fca10a7555acb99c76d2e1992777994930fd8bd49265935ba84c` | 0 |
| lib/libsodium/src/libsodium/crypto_stream/salsa20/stream_salsa20.h | 532 | `c726237642e7c269fabbc2442f2ce008b0de9a2cf90469758853d78f27a1eee6` | 0 |
| lib/libsodium/src/libsodium/crypto_stream/salsa20/xmm6/salsa20_xmm6.c | 852 | `c3c8230ca99c8b79182ef706d22b32f9b47656884a80cd5e92effb6569dddefe` | 0 |
| lib/libsodium/src/libsodium/crypto_stream/salsa20/xmm6/salsa20_xmm6.h | 187 | `b56e570bfa5e15910a3b2c4fcc5999b7b8ac5f754e5f70bcb9ed938c211ac09d` | 0 |
| lib/libsodium/src/libsodium/crypto_stream/salsa20/xmm6int/salsa20_xmm6int-avx2.c | 3296 | `ca3783de60a965a6f41b2c4759a9218864a01ba3585dfe345343924e255644da` | 0 |
| lib/libsodium/src/libsodium/crypto_stream/salsa20/xmm6int/salsa20_xmm6int-avx2.h | 195 | `bfbc9a2d6513fdab5ede6dc8cec1f2f6a555a08aefef7e0b1b18c1017793c72a` | 0 |
| lib/libsodium/src/libsodium/crypto_stream/salsa20/xmm6int/salsa20_xmm6int-sse2.c | 3023 | `51a4af9211dcb908ca1b0368e54c0b3bdda4b1076f672d5f06773961c0b05d57` | 0 |
| lib/libsodium/src/libsodium/crypto_stream/salsa20/xmm6int/salsa20_xmm6int-sse2.h | 195 | `839d059a0ba385066a969bf582e1f9d9969d825b5d8debe778937de4e5de8bc3` | 0 |
| lib/libsodium/src/libsodium/crypto_stream/salsa20/xmm6int/u0.h | 6879 | `5d0f8743a38dee11ff160fc6a2f30c976548edb7479c17040d0e43865b8f10ed` | 0 |
| lib/libsodium/src/libsodium/crypto_stream/salsa20/xmm6int/u1.h | 6814 | `f35de0b5967c7f1ce03700f4f2d23783b34441216036aa745b9707305d4e6eae` | 0 |
| lib/libsodium/src/libsodium/crypto_stream/salsa20/xmm6int/u4.h | 19408 | `3bf51e537e7fa8ffe3db2dedf87c990ae7d6e90cfc1aa1ca666807ba7a65493b` | 0 |
| lib/libsodium/src/libsodium/crypto_stream/salsa20/xmm6int/u8.h | 18674 | `f06f540318841dcf94483aabf2511da791ba1d6a68d1f42665ced9a54d9d6715` | 0 |
| lib/libsodium/src/libsodium/crypto_stream/salsa2012/ref/stream_salsa2012_ref.c | 2370 | `20cc0512f97f70bcf65561e9bef9f0b042ab49640c443d7e9d454d2401ca166a` | 0 |
| lib/libsodium/src/libsodium/crypto_stream/salsa2012/stream_salsa2012.c | 520 | `2aaba5e9e9c6db319ff14e5dea314e911cfb10298430d202d66cea3f33b484dd` | 0 |
| lib/libsodium/src/libsodium/crypto_stream/salsa208/ref/stream_salsa208_ref.c | 2359 | `b9cddcf73aaef798b5c5359d7e629b1859fd8885ddd5b7889977ab17af74b923` | 0 |
| lib/libsodium/src/libsodium/crypto_stream/salsa208/stream_salsa208.c | 510 | `0e8ff1ff21298538da4ec94d6edfdd541f7ee97a421956a8323eafb5ba85e662` | 0 |
| lib/libsodium/src/libsodium/crypto_stream/xchacha20/stream_xchacha20.c | 1969 | `db04ab9c17b43330c0c109ca8c545e7cc9cae106b6313ca6b04cf80c113558b1` | 0 |
| lib/libsodium/src/libsodium/crypto_stream/xsalsa20/stream_xsalsa20.c | 1692 | `0c3d8b9b45ee606ac9b7a4b651347e72b2f629e6d17e513c7a7aa161058c4aec` | 0 |
| lib/libsodium/src/libsodium/crypto_verify/sodium/verify.c | 2296 | `2af44fcbde7abb7aacba6629689d19fea98b8dda19fd7d53c3186c077ee97e86` | 0 |
| lib/libsodium/src/libsodium/include/sodium.h | 2529 | `510bd520da2545bc9cfe3060230f4dffb345f1e96ccf25b53e4b8a3d73d1984b` | 0 |
| lib/libsodium/src/libsodium/include/sodium/core.h | 391 | `692c9a03eb49591a3ccacbef293f473c619cc86ef5dd4776a6e2e4321426fb07` | 0 |
| lib/libsodium/src/libsodium/include/sodium/crypto_aead_aes256gcm.h | 7980 | `b9d20e820519211b0cdbc37ccfad2195ccf1b0009965840ea87865054b7aab4e` | 0 |
| lib/libsodium/src/libsodium/include/sodium/crypto_aead_chacha20poly1305.h | 8782 | `829054e89c68f98c660c5f5cc65318e2fda345a888a0c337534a338bc96ee757` | 0 |
| lib/libsodium/src/libsodium/include/sodium/crypto_aead_xchacha20poly1305.h | 4848 | `be76cd253ee5ba929156186ff6b21477dac7f5e8d23da881b5a7babc3c2eba39` | 0 |
| lib/libsodium/src/libsodium/include/sodium/crypto_auth.h | 1143 | `6728e121bde1e328687d7222fe29e0eb5f95fecc982f179f2788735369da8fa2` | 0 |
| lib/libsodium/src/libsodium/include/sodium/crypto_auth_hmacsha256.h | 2136 | `c4de9221fb19f47478680839d3c5157363c8806c8c36b9a3ffa624a6500fff0c` | 0 |
| lib/libsodium/src/libsodium/include/sodium/crypto_auth_hmacsha512.h | 2123 | `53415ff29ec0578a631a04794e0486ffee8b9d90b790eee593e35a7d32ff0ec1` | 0 |
| lib/libsodium/src/libsodium/include/sodium/crypto_auth_hmacsha512256.h | 2133 | `a30f9c02e3b60842200523c062e2da1a29c9cc61a3cae10203a468a70fd41816` | 0 |
| lib/libsodium/src/libsodium/include/sodium/crypto_box.h | 6838 | `400153ce5d5c5da3513738b3e5b34c39f99fb9839a5ba5a01684d7e6ecfe1026` | 0 |
| lib/libsodium/src/libsodium/include/sodium/crypto_box_curve25519xchacha20poly1305.h | 7957 | `fd18828324c974159902e1fb21813b9c0be04da96ccb96f261bf989ddd7fd87a` | 0 |
| lib/libsodium/src/libsodium/include/sodium/crypto_box_curve25519xsalsa20poly1305.h | 4697 | `069ca8e79bcc8d316ef614f73383644b5490d22391283e1dfc9a9b3cdc6baf31` | 0 |
| lib/libsodium/src/libsodium/include/sodium/crypto_core_ed25519.h | 2898 | `ac47a76c87f08a96f475b2e0b05a7a12a61ee7a99e0258cc63967c7fb585a3c6` | 0 |
| lib/libsodium/src/libsodium/include/sodium/crypto_core_hchacha20.h | 816 | `d2a265946fab3fddb8ee4b7ee6b3fb34b6526efa6ba45c6609c7e395ed302fc1` | 0 |
| lib/libsodium/src/libsodium/include/sodium/crypto_core_hsalsa20.h | 804 | `5f9d48c0cdfcb8ce86a0e65cfa490cac0e9cacbca4aa864926593c691f69be63` | 0 |
| lib/libsodium/src/libsodium/include/sodium/crypto_core_ristretto255.h | 3140 | `cd421515c472fff15b22f5aa27a42f97c0fa5d438c28b9ea7d5908077ffd2099` | 0 |
| lib/libsodium/src/libsodium/include/sodium/crypto_core_salsa20.h | 792 | `614992c472e5c2bad2ba8d90a4b6d9023db3774847e3541d5c87ad4cb59d69d0` | 0 |
| lib/libsodium/src/libsodium/include/sodium/crypto_core_salsa2012.h | 816 | `1fce6f1b2a28c7764ba7ed99fefabefa2cbca688ce86e2574cc08ae235c8c3fd` | 0 |
| lib/libsodium/src/libsodium/include/sodium/crypto_core_salsa208.h | 968 | `f5f40276f7f06f3478750037c56b8e29b1717588b75bd1a3769ccc54f73a709a` | 0 |
| lib/libsodium/src/libsodium/include/sodium/crypto_generichash.h | 2495 | `df7e3590c86db50c6aa7329ecce967bab09004d71c23f458e557a07d734f944d` | 0 |
| lib/libsodium/src/libsodium/include/sodium/crypto_generichash_blake2b.h | 3963 | `da19eef8f229b8c5964972295f22e46c11bf964534816aea4bde31d7727afd20` | 0 |
| lib/libsodium/src/libsodium/include/sodium/crypto_hash.h | 901 | `5720698bd0072074ee163d8d89adaa5b6ade064bf38871afe3b814d4418487c1` | 0 |
| lib/libsodium/src/libsodium/include/sodium/crypto_hash_sha256.h | 1492 | `121d63b8749770b67b45eac983c5d602b9ca5d6dda02c11b88cdf888f17914ab` | 0 |
| lib/libsodium/src/libsodium/include/sodium/crypto_hash_sha512.h | 1496 | `a4c3976041ca76a28960bcb265e6de55ab2b876f9e2f1b3427a39888314de044` | 0 |
| lib/libsodium/src/libsodium/include/sodium/crypto_kdf.h | 1308 | `09901e619b1909e1802ace8f1e8b9ceb2218fd49c4ee430126802df7ff402525` | 0 |
| lib/libsodium/src/libsodium/include/sodium/crypto_kdf_blake2b.h | 1071 | `2f0739ea610fb5c9ad8c453d84fac1d09e187f67096c70887f22c32a750e922b` | 0 |
| lib/libsodium/src/libsodium/include/sodium/crypto_kx.h | 2201 | `b590d661674331aba7dade467ee902e1b61d0fe875bfc3780bd41b9e91dce316` | 0 |
| lib/libsodium/src/libsodium/include/sodium/crypto_onetimeauth.h | 1912 | `4d07e9033ba62f556ceb3a7412226e0d74481014026953d6815cb5c4d9955891` | 0 |
| lib/libsodium/src/libsodium/include/sodium/crypto_onetimeauth_poly1305.h | 2198 | `bed2ea5e07ffa89264413e2cf1d7730b0fd3c56d42399c86a36ccfef52f27296` | 0 |
| lib/libsodium/src/libsodium/include/sodium/crypto_pwhash.h | 4966 | `e529cb84849008caf0dd2f3f1bac6808a0be9c963f9d2814f59badeda85d0c5b` | 0 |
| lib/libsodium/src/libsodium/include/sodium/crypto_pwhash_argon2i.h | 3919 | `50a6b40ea240dd5f3b01198437ab56afabd050733ffa4d3dae5a90367e2e30ca` | 0 |
| lib/libsodium/src/libsodium/include/sodium/crypto_pwhash_argon2id.h | 3981 | `15fe59b3b5b7ef6562b446f39d28ec4d97de06c662005f0d9aad6788d61b8155` | 0 |
| lib/libsodium/src/libsodium/include/sodium/crypto_pwhash_scryptsalsa208sha256.h | 4688 | `5104ba3a227b676f0f8d3f0978d882b9d7ac683bf43c1d8995d6003e2ffe8e1f` | 0 |
| lib/libsodium/src/libsodium/include/sodium/crypto_scalarmult.h | 1184 | `80202693f962c5c5c69dab8e3398ee1e58c4422e21f110301ddfc6d137dd545b` | 0 |
| lib/libsodium/src/libsodium/include/sodium/crypto_scalarmult_curve25519.h | 1098 | `3122574b81d8365961aeef5e984c9ac33dfcc6f2767ef70e8622ceb20f81dbd8` | 0 |
| lib/libsodium/src/libsodium/include/sodium/crypto_scalarmult_ed25519.h | 1406 | `d1e92c568dc731b0770bada45ee23d970a17534c41f4e5a15f44e1210e002f16` | 0 |
| lib/libsodium/src/libsodium/include/sodium/crypto_scalarmult_ristretto255.h | 1119 | `cfd5cb3642ee1186adfd4f4752b7cf93215f0991aaf6a2af9a93d35733d07f42` | 0 |
| lib/libsodium/src/libsodium/include/sodium/crypto_secretbox.h | 3316 | `49655e9cf0302539ffa7de8d025f598fea330481575e767c134c5e06a2ac1f55` | 0 |
| lib/libsodium/src/libsodium/include/sodium/crypto_secretbox_xchacha20poly1305.h | 2853 | `dbbe1bf02d5abd16ad0604b9ff976f028340eac0eecd3ea5dd3512e29cfdd9b6` | 0 |
| lib/libsodium/src/libsodium/include/sodium/crypto_secretbox_xsalsa20poly1305.h | 2419 | `c03da9bf0c12555ba39a86ba9bf8e923272f5721530de69d658b477d2da27321` | 0 |
| lib/libsodium/src/libsodium/include/sodium/crypto_secretstream_xchacha20poly1305.h | 3832 | `84f514317b7feb33b644b2c3fc45b9f012dd5cbda98aeb8086ec8f6d7029851f` | 0 |
| lib/libsodium/src/libsodium/include/sodium/crypto_shorthash.h | 960 | `f085c63bff21b6917dfe4e7415d4db740ef49f177abaf25a747e9878830c067f` | 0 |
| lib/libsodium/src/libsodium/include/sodium/crypto_shorthash_siphash24.h | 1236 | `69b5ed9869b8b5da63991ad3426bf5bd56449827d87073202cbbe2ee7635d83e` | 0 |
| lib/libsodium/src/libsodium/include/sodium/crypto_sign.h | 3353 | `9631e38d8c9d0f338628cf3942a27500ef5bbe06f7d34b4c3c4bbbd74f1ffb0c` | 0 |
| lib/libsodium/src/libsodium/include/sodium/crypto_sign_ed25519.h | 4341 | `c86e5a3ee60ee0140b5aef3b91bf59de809c6f8fec596663d96304f4280dcf19` | 0 |
| lib/libsodium/src/libsodium/include/sodium/crypto_sign_edwards25519sha512batch.h | 2053 | `958060430c84e0a2ca4c036214e8b92220f9d5d41ac76903266e122f8e89d594` | 0 |
| lib/libsodium/src/libsodium/include/sodium/crypto_stream.h | 1606 | `ae8d27cabc066b6e369e0a4d04f0aea1aced45145d8e176a21bdcf359c4001a0` | 0 |
| lib/libsodium/src/libsodium/include/sodium/crypto_stream_chacha20.h | 3672 | `e6f0ef6cb1199bac25096f715fd9290e073c8a9e0fc03066699fed0fb800612b` | 0 |
| lib/libsodium/src/libsodium/include/sodium/crypto_stream_salsa20.h | 1836 | `cf1c051d837eaea3b102c63683394e415d2d9ee2f885ba105312af7e13db03b8` | 0 |
| lib/libsodium/src/libsodium/include/sodium/crypto_stream_salsa2012.h | 1532 | `bc65adc00270a7e18bd5acf3141c252bddb82a4628388299349ab94f9784bd8e` | 0 |
| lib/libsodium/src/libsodium/include/sodium/crypto_stream_salsa208.h | 1731 | `5430b7f5a934a75ee4f5c8e9ed9ddc3cec7dd1032ac8bec35c7188da5d738fa2` | 0 |
| lib/libsodium/src/libsodium/include/sodium/crypto_stream_xchacha20.h | 1875 | `dcaafd5679d02460b24fe877946458ff454f4e9d35c8e1f8f1f1b48d54c96698` | 0 |
| lib/libsodium/src/libsodium/include/sodium/crypto_stream_xsalsa20.h | 1856 | `de812c7463a2ca0f4db6c6edb671277777f0aaccff85d86a471c7da932a09b0c` | 0 |
| lib/libsodium/src/libsodium/include/sodium/crypto_verify_16.h | 419 | `d3b4fbea4b6d2bf23a9a079939a181625be76a006af129732af86bf4b544456c` | 0 |
| lib/libsodium/src/libsodium/include/sodium/crypto_verify_32.h | 419 | `6ea1ea855b691a2b08510afe74f893d4ff44e40b14501d774d1a73dd79ad4e73` | 0 |
| lib/libsodium/src/libsodium/include/sodium/crypto_verify_64.h | 419 | `9736126e6d38864b7c2aa0edf0075e3f6b1fe485a060067ce8c06afb340171a8` | 0 |
| lib/libsodium/src/libsodium/include/sodium/export.h | 1347 | `acc6ee537f831d535b0607be90f05150103765b7ca82170fd61a85bd5e6f73ff` | 0 |
| lib/libsodium/src/libsodium/include/sodium/private/chacha20_ietf_ext.h | 632 | `116e6f97313959c5c45eadeb1722b52f5ec0f38ad57ef1177b3eae4d57d3fa3f` | 0 |
| lib/libsodium/src/libsodium/include/sodium/private/common.h | 6224 | `aab3513a1486fa2b32187a8431a80144c5053549188af4a620913840ae34a9f9` | 0 |
| lib/libsodium/src/libsodium/include/sodium/private/ed25519_ref10.h | 3535 | `0acea90b49b5e8a0b83fe1757ef95f55c6b9c78fc63e8cc94e42ab5f6f222a14` | 0 |
| lib/libsodium/src/libsodium/include/sodium/private/ed25519_ref10_fe_25_5.h | 30154 | `7f1522d3286253add4d09c61df2fb4e96d4b4b8bc50db57c5ecadc0c10dae36a` | 0 |
| lib/libsodium/src/libsodium/include/sodium/private/ed25519_ref10_fe_51.h | 10968 | `4b9c0513603135de0f8f9a64632bb71f9dd4cb6a0cdf82907c8bcdc9e3398ed4` | 0 |
| lib/libsodium/src/libsodium/include/sodium/private/implementations.h | 433 | `c97f3bed15f648a925023527d25d4130774d0a15354cfb5184b20dbc5f7e328c` | 0 |
| lib/libsodium/src/libsodium/include/sodium/private/mutex.h | 115 | `ee045978cbd074c695e8e0b4ec074b84e768c9557c8b4d69ebccc0710bbc422c` | 0 |
| lib/libsodium/src/libsodium/include/sodium/private/sse2_64_32.h | 1119 | `cb456bfe3b22c8bf1062a8e579ed1f15bdff724a23c8313531a1a46dd2a2843b` | 0 |
| lib/libsodium/src/libsodium/include/sodium/randombytes.h | 1847 | `41bf6745f8343b39a48861e9128bbff39ddd7f784d3e8c59a8fcbc55c6511c05` | 0 |
| lib/libsodium/src/libsodium/include/sodium/randombytes_internal_random.h | 427 | `9909eaf527e325d69d08c55db2f76de379fd4de338ff82e72a1da5a206fa3b6b` | 0 |
| lib/libsodium/src/libsodium/include/sodium/randombytes_sysrandom.h | 282 | `cdcc193ee76bb69626b7cb63b105db2f83796b7c365c9f4e42193fa9e654bfb6` | 0 |
| lib/libsodium/src/libsodium/include/sodium/runtime.h | 889 | `5f618794bfa316c338bc166ffd21f00e5711a0ebf94aaa19440c88b0c94be023` | 0 |
| lib/libsodium/src/libsodium/include/sodium/utils.h | 6149 | `9e1edab33653155e3d4773963234b9eb0af9b1983b1ef3dc1f248c46e44dcae1` | 0 |
| lib/libsodium/src/libsodium/randombytes/internal/randombytes_internal_random.c | 15377 | `37a399fc23b582f9c4caed29280e8de63100a5d5a91f16d09534a750d63c0420` | 0 |
| lib/libsodium/src/libsodium/randombytes/randombytes.c | 4900 | `f4ae59f5208e6c878f1bc70f1102c45ea33959ab275a900feb388570c0394e20` | 0 |
| lib/libsodium/src/libsodium/randombytes/sysrandom/randombytes_sysrandom.c | 9596 | `9b0a9b2c7794deb25174ca2d3675c727944477fa45872d680103c1aa9f84661c` | 0 |
| lib/libsodium/src/libsodium/sodium/codecs.c | 9296 | `f2d9d92e607a47209199e29358d20179982ea64a3ef130caf0b8cefd0f98fd43` | 0 |
| lib/libsodium/src/libsodium/sodium/core.c | 4088 | `93939d012dc75877b1360ebea6720520209d0e30c86d482572748bf053526a2b` | 0 |
| lib/libsodium/src/libsodium/sodium/runtime.c | 7620 | `15d89eb540b4e4ead4729ffe5e716eb9b3dd03b812cf092d6963a5ad5df6c54a` | 0 |
| lib/libsodium/src/libsodium/sodium/utils.c | 20685 | `b22388b6cd8039b847a2ea003edbcd715132cb623d84ca716638da45c02363e4` | 0 |
| lib/libsodium/src/libsodium/sodium/version.c | 381 | `f156b71249e77d49a3d31b8cd76fe8251da2df20a851c2e2ba91978847893823` | 0 |
| lib/spdlog/include/spdlog/async.h | 4012 | `3ddaaba57d2f757d6cb09568fe1823949e45426d73f6baeb4ca8d8a2fe78121b` | 0 |
| lib/spdlog/include/spdlog/async_logger-inl.h | 2817 | `c298acfd85cd1ad21c0ff0a3cc930746174d4945f0844dcd6ca8b842ee9a22ce` | 0 |
| lib/spdlog/include/spdlog/async_logger.h | 2556 | `5e3219c74c29dee0b04a8c72ae6568e6d44999071f4416453a01514eccd21b64` | 0 |
| lib/spdlog/include/spdlog/cfg/argv.h | 1219 | `6f9aa40647fda08e2ad776598a7b5de1d1596ec9a73512c90c69504f6e347a2d` | 0 |
| lib/spdlog/include/spdlog/cfg/env.h | 1007 | `d2afd153fe8a1b2826feb60ec62ea42811d1ca085471fda238d002fedf5bb1bc` | 0 |
| lib/spdlog/include/spdlog/cfg/helpers-inl.h | 3164 | `1d43f8134b35efd52f6e3387be03602d3c85ca6df2dceab0313b660c37d1df90` | 0 |
| lib/spdlog/include/spdlog/cfg/helpers.h | 714 | `5134c03ca4795ed4e998a2249793b1917989bd2199ff66c689ef48fd9a827bfe` | 0 |
| lib/spdlog/include/spdlog/common-inl.h | 2046 | `e170ca1af147a885142c8afdf29722ae52a40416dfd6b666758b39b5b5588d62` | 0 |
| lib/spdlog/include/spdlog/common.h | 12569 | `ddf4fa8ee4687f364086c3f3bca3b9113df3622916c67776594d231418102143` | 0 |
| lib/spdlog/include/spdlog/details/backtracer-inl.h | 2000 | `9b2795b78571295776003345d7e2b9f264fa71fabb7a15cda7b049464a2d24c3` | 0 |
| lib/spdlog/include/spdlog/details/backtracer.h | 1161 | `d4d613badbe01d67bfaefaba0a7a934f0e5f5eb3f18096e5cba54ab2fd4da883` | 0 |
| lib/spdlog/include/spdlog/details/circular_q.h | 3377 | `0bc4025c81425023f4d58711d6aa6231a55ee606bb1fc88f4fb3e655e807e265` | 0 |
| lib/spdlog/include/spdlog/details/console_globals.h | 603 | `3dced73dc2bc5eacc678eec34af6458f910740c8949fd1bc8449808d1345467a` | 0 |
| lib/spdlog/include/spdlog/details/file_helper-inl.h | 4669 | `cb74c68b416fd94ef738b12e93af4bb571b69f2bcc3b6987cc7ee0a1fbee0547` | 0 |
| lib/spdlog/include/spdlog/details/file_helper.h | 1754 | `e23822a24c9f913328ceed3a7176e832114ec65abccf802bac280852b288415b` | 0 |
| lib/spdlog/include/spdlog/details/fmt_helper.h | 4443 | `7a2e655f077c1f9ceb7d7a69214594c3721702b691b7a301bad96f0affd45d06` | 0 |
| lib/spdlog/include/spdlog/details/log_msg-inl.h | 1392 | `7ec7033b384263180c041a4ab627cc8081d7550af6a4533f49334af5fce2d4f7` | 0 |
| lib/spdlog/include/spdlog/details/log_msg.h | 1200 | `7e9a3b7b89646cc1ad36d21de8e7d584f81dfa642760c12f40385dc0db65e3b0` | 0 |
| lib/spdlog/include/spdlog/details/log_msg_buffer-inl.h | 1664 | `e41147aa63dfb99b1b2285a88740d9e7c238099ae3518b2e88798e7e5991932a` | 0 |
| lib/spdlog/include/spdlog/details/log_msg_buffer.h | 931 | `5a79fdfa5429d23286c58926a53de3ee83b577db21a4cccbd104ceda8ded7c50` | 0 |
| lib/spdlog/include/spdlog/details/mpmc_blocking_q.h | 5280 | `66ed3083a98e5cc142aa8d9dc18ce8de5ff32f82382386546f6ff302a01fc6c6` | 0 |
| lib/spdlog/include/spdlog/details/null_mutex.h | 930 | `1377fde4b54417dca1b3d162d0f18c35f9418e1db91a333949952f1c877127b1` | 0 |
| lib/spdlog/include/spdlog/details/os-inl.h | 16986 | `f32d377e7b58e53b1d601a7e0fef5e2c1d137592c25df3bb4adbf89e015018ef` | 0 |
| lib/spdlog/include/spdlog/details/os.h | 4050 | `dc6af3c0fae5b49d8a703f6ef5432f3f25cd061290e81dd0d80441ba5719cf07` | 0 |
| lib/spdlog/include/spdlog/details/periodic_worker-inl.h | 616 | `72c338426a4cd5f1a387d222a867b575f01f8d1968326f5f30a82ff5071bd681` | 0 |
| lib/spdlog/include/spdlog/details/periodic_worker.h | 1809 | `2773bf8766655b9ba5b53c9a84b2abcd4a4f02ec5b55363740668534eaa217cc` | 0 |
| lib/spdlog/include/spdlog/details/registry-inl.h | 8849 | `52163509eb3f64e0b014646611a250a0ee01674fe85f4efdfd4afda0e003cb12` | 0 |
| lib/spdlog/include/spdlog/details/registry.h | 4460 | `a5ce3c5a8bc019e7d8508268b222136c01f1e81360df67f104f21bf4b49e4f4b` | 0 |
| lib/spdlog/include/spdlog/details/synchronous_factory.h | 751 | `3fcfcc28aa4edc2998e9e00d218362600605b89e0c58ebf2c7267950412e1cdc` | 0 |
| lib/spdlog/include/spdlog/details/tcp_client-windows.h | 7065 | `3553c39bc4a1a28e43ee05ab79f11762ba829847358e1f564bf4f8a96c683d73` | 0 |
| lib/spdlog/include/spdlog/details/tcp_client.h | 6393 | `6977deb87db2535da5afb0013644386bcf32e49b64655c31344f5835f1324029` | 0 |
| lib/spdlog/include/spdlog/details/thread_pool-inl.h | 4270 | `b7042c70da4d1c0398ddc74fc12bb5eec746647c18857ace1c6f425b5cf9435e` | 0 |
| lib/spdlog/include/spdlog/details/thread_pool.h | 3515 | `432bccde480274c911460d7ba30cda62afefd6fcc2cc57529b5f44d68324a62e` | 0 |
| lib/spdlog/include/spdlog/details/udp_client-windows.h | 3122 | `475721551d61f3749fe008762cf0359f67d6bd90383208749e30360bfa190d1d` | 0 |
| lib/spdlog/include/spdlog/details/udp_client.h | 2233 | `53e10fa54ef911f254fa485ff9e6f8047c9c7659f5b345f87a4a590831832903` | 0 |
| lib/spdlog/include/spdlog/details/windows_include.h | 180 | `ee78df4fa66a4e41ed97b47305953f9af2140718c5fab14d921ad8b195e9931b` | 0 |
| lib/spdlog/include/spdlog/fmt/bin_to_hex.h | 7362 | `5609bbf846807ba9a18330fdc0141d91a067c0e44b760b97693c2a88893a5635` | 0 |
| lib/spdlog/include/spdlog/fmt/bundled/args.h | 7199 | `6e0bf8ffbd904e6ef525cdce8e6e00312ce5d14f616cea5d88132606ca0384c4` | 0 |
| lib/spdlog/include/spdlog/fmt/bundled/base.h | 105054 | `892fcc48f31a80382f0e304e427d68d2fd62a2d78aef142020199120db5269fb` | 0 |
| lib/spdlog/include/spdlog/fmt/bundled/chrono.h | 77454 | `f8e2a69bd97bc5b90c9af7fb87e010775b695d487a77e8d8cbe624e57bd2f9bf` | 0 |
| lib/spdlog/include/spdlog/fmt/bundled/color.h | 24145 | `f88bf0c4833caed3a7f01b6d633c7b259741a26119e84c651ac1e31cfc980b72` | 0 |
| lib/spdlog/include/spdlog/fmt/bundled/compile.h | 20493 | `636c13842acce0b42b378e65fe67a69e5635e8225c9701975e5b326a97be5cb8` | 0 |
| lib/spdlog/include/spdlog/fmt/bundled/core.h | 187 | `b2b6692145b11c7c2774db106078c97575a47d18e80c7783c68566475325ebb4` | 0 |
| lib/spdlog/include/spdlog/fmt/bundled/format-inl.h | 81008 | `e7baf108b84e89b29915bb35733540f8f4262cd8f4b41c15754eed4d2f185f61` | 0 |
| lib/spdlog/include/spdlog/fmt/bundled/format.h | 162666 | `b4c65350362bf40e76a8e6b450587d912c7081b6eafeafaf3d7bcf53153e17fc` | 0 |
| lib/spdlog/include/spdlog/fmt/bundled/os.h | 12860 | `45d4e84be4e84a128442f04eda06e1305c8e02c61166854a3b8b348194d35da5` | 0 |
| lib/spdlog/include/spdlog/fmt/bundled/ostream.h | 5027 | `742416a6a88286609887fa512c4423820764aafbb723a42a825f3193cb52b4f0` | 0 |
| lib/spdlog/include/spdlog/fmt/bundled/printf.h | 19991 | `afddb422a86125e04a7260bb0f0ae3423ea8d591181ed5d4ef60b7a5d068993a` | 0 |
| lib/spdlog/include/spdlog/fmt/bundled/ranges.h | 28126 | `ccaf61c9b5937e0fa97737fb047121c5fca9db34de516b8edfc1d913583e3c8e` | 0 |
| lib/spdlog/include/spdlog/fmt/bundled/std.h | 23532 | `3f06cdf32774b9e6915e9762411f5f4de8b8ba5660adccbdea514be7f0b23826` | 0 |
| lib/spdlog/include/spdlog/fmt/bundled/xchar.h | 13098 | `f0903d522c64faaee2c374a0b2063ac3e43d0b5006dfd3411f0e5dccd8ff6062` | 0 |
| lib/spdlog/include/spdlog/fmt/chrono.h | 467 | `f57be9fd2c4c39dc7ff73f736c481eaa418723ccc7adeb16b3905a0f4a7b534e` | 0 |
| lib/spdlog/include/spdlog/fmt/compile.h | 475 | `6ecd7b2ae593e3b7b00d577ad035c0598c29c2df3947c21102ec110b2a33b5e9` | 0 |
| lib/spdlog/include/spdlog/fmt/fmt.h | 712 | `6fc4048665172d38d835203d757aa30d4136c622d26d26e881f72f96b86aa556` | 0 |
| lib/spdlog/include/spdlog/fmt/ostr.h | 470 | `d0437444e2da75ee732e392ce96e8f72d1db5bf9a6a79f0a1d36dbdd93ce1f1e` | 0 |
| lib/spdlog/include/spdlog/fmt/ranges.h | 467 | `7ef5f93f56f8f39ecda80b070bf1b3a93530832b6f69415c99acb72bd33a80ac` | 0 |
| lib/spdlog/include/spdlog/fmt/std.h | 557 | `4a72a66fa67040b429dd791b10e75b21d5c18017ababcab808ef09900c727484` | 0 |
| lib/spdlog/include/spdlog/fmt/xchar.h | 464 | `0f5db8046e2c81bca4d2dd0245702366d5d4c51131a25cb0b79e5001a5002177` | 0 |
| lib/spdlog/include/spdlog/formatter.h | 463 | `213631628274dc6c26fcc9a3bed36a3a9a83edea5e6b9f027baea58ca9c5eff3` | 0 |
| lib/spdlog/include/spdlog/fwd.h | 305 | `246d2754fb77dcdcb7ed4be2328944659fd154599ee09df865db5cdb33cbe349` | 0 |
| lib/spdlog/include/spdlog/logger-inl.h | 6742 | `1507122f5c8bc7428fd5a606c29bc0fff42b6f55c602311d1891e45d23afb7a7` | 0 |
| lib/spdlog/include/spdlog/logger.h | 13353 | `e6b8ba92b7c6b83b816871f9a663cab4c1c21da3c5b252904f3dae412dfad85d` | 0 |
| lib/spdlog/include/spdlog/mdc.h | 1493 | `c3516a85d687f806080d81d0b63cb0353665b26d78f6cdc2c51e526ae9c492d8` | 0 |
| lib/spdlog/include/spdlog/pattern_formatter-inl.h | 47192 | `7e05fab1303d952801143118e33525a50d77304b3b3fec117ccc8637c85135fb` | 0 |
| lib/spdlog/include/spdlog/pattern_formatter.h | 3754 | `87fffd034b0a2139a6373ba04d9f88ae57cfac3865138e0859f19a9e5858da43` | 0 |
| lib/spdlog/include/spdlog/sinks/android_sink.h | 4717 | `96f8c917be604bfc0cd4a84e6e9bebd790c9828170f921a50f0f013a653cda8d` | 0 |
| lib/spdlog/include/spdlog/sinks/ansicolor_sink-inl.h | 5095 | `62a5e7c2522606660d4faa683d206d748c94cdcd6c72540ce6ac46b28a153958` | 0 |
| lib/spdlog/include/spdlog/sinks/ansicolor_sink.h | 4031 | `c6078602b09b78f781e4a18b966e2a3ea2dbea5c9a84a77adbe1e27557e85de7` | 0 |
| lib/spdlog/include/spdlog/sinks/base_sink-inl.h | 1804 | `7fe3e5bb453018d03e2b850384b18f8c00a1b64be363bb22c4b9b92082d9bcc7` | 0 |
| lib/spdlog/include/spdlog/sinks/base_sink.h | 1600 | `86186e0d15535b94270c94ab5eeb798d47dfe7330f4e622bf7c66dc46c820f37` | 0 |
| lib/spdlog/include/spdlog/sinks/basic_file_sink-inl.h | 1387 | `613295eaac45babf5cd5e7bec262763a5214071eaeab58c5598ac60620285c6c` | 0 |
| lib/spdlog/include/spdlog/sinks/basic_file_sink.h | 2312 | `e4693c382833fc13d6adbdc68d602d479c72225a463892bc4fd6fde6475edd4c` | 0 |
| lib/spdlog/include/spdlog/sinks/callback_sink.h | 1705 | `568eed97d5c29f942d811afe8614ceae6c110b74ffa4535123a5bd9db31f263f` | 0 |
| lib/spdlog/include/spdlog/sinks/daily_file_sink.h | 9610 | `ee32cbdd80b9fe51abe04ae290d199c46cec2ecbf35e7a2e796daf712b8520d2` | 0 |
| lib/spdlog/include/spdlog/sinks/dist_sink.h | 2373 | `fa6b8b53368b3cc9490046f1a207c3852835f0a00f6f677005c9e52799e86247` | 0 |
| lib/spdlog/include/spdlog/sinks/dup_filter_sink.h | 3225 | `aded06d32de86861be0b07a7c1561cd1a9f1df80cdbc0eb15c4f9735c26cc309` | 0 |
| lib/spdlog/include/spdlog/sinks/hourly_file_sink.h | 7279 | `aa31439c3c3072e9b77acc2800005b586f6b6cdc2d790e0783050b8627a79411` | 0 |
| lib/spdlog/include/spdlog/sinks/kafka_sink.h | 4445 | `9bb10a5ea347f2400baadf0d794d5045169fae77388132bc0cf3dcf30ec00c08` | 0 |
| lib/spdlog/include/spdlog/sinks/mongo_sink.h | 4003 | `df9a5c34bef34a9a55f4bec51f98c3f0527fdc61bc8ee247a9b4f4149e8ff0f0` | 0 |
| lib/spdlog/include/spdlog/sinks/msvc_sink.h | 1988 | `2c9107975cc29f89880846dce6939f2e8670a0b4aacf36a83cf08c8190475402` | 0 |
| lib/spdlog/include/spdlog/sinks/null_sink.h | 1240 | `75d92f19d80ba59e15c8607e4c98a86a14e238e5ca9b5afd6150dcf9e86d10d6` | 0 |
| lib/spdlog/include/spdlog/sinks/ostream_sink.h | 1222 | `8a444e2537b82d6fe4a87c1162d4eb53f94ceb01acbc8d646828f2b24f869085` | 0 |
| lib/spdlog/include/spdlog/sinks/qt_sinks.h | 12697 | `e3bb4b606187dcfc06ef2abafb0bf285662ed1edc079f5525cd4039e081e5212` | 0 |
| lib/spdlog/include/spdlog/sinks/ringbuffer_sink.h | 2196 | `69dd445a2519bdc25261f2af884b479a09a54458468f9f351a8333ae6ab370a5` | 0 |
| lib/spdlog/include/spdlog/sinks/rotating_file_sink-inl.h | 6087 | `8dc1c0985be041ac2ec0f155b534b748cd44b3eb33e8836dc849f9314c21d13e` | 0 |
| lib/spdlog/include/spdlog/sinks/rotating_file_sink.h | 3348 | `27fa443b8bd9158f4472e116a05fea37e82b6452b6eb70a4ea78ae0089039142` | 0 |
| lib/spdlog/include/spdlog/sinks/sink-inl.h | 721 | `f8fabf0de532bef4788ad59f278afbd3c4187b598f5c856370cdfa3dd564f28a` | 0 |
| lib/spdlog/include/spdlog/sinks/sink.h | 889 | `75e5c2b43c253cfe7c553077125e3b158e9d71caf2765ad97bb08443ee83b56a` | 0 |
| lib/spdlog/include/spdlog/sinks/stdout_color_sinks-inl.h | 1431 | `4267753c6a0f8f8380999fa1445438cde62a62874a6be4555d8bd23245f9e1f7` | 0 |
| lib/spdlog/include/spdlog/sinks/stdout_color_sinks.h | 1780 | `03700ff3259fc97d2adb52ef5c470cf847bb1d417bf5d74e851c7c1b6212fe0e` | 0 |
| lib/spdlog/include/spdlog/sinks/stdout_sinks-inl.h | 4344 | `cd9298408922fcf38b45eec7853cd0e96efac4ca65a8fc0326dcc17189853dfe` | 0 |
| lib/spdlog/include/spdlog/sinks/stdout_sinks.h | 2421 | `a7eb6c3e4aedbed13c57ae517cbee30ef62582b3e02e35530123cae58ce1f526` | 0 |
| lib/spdlog/include/spdlog/sinks/syslog_sink.h | 4248 | `92dddbd22c8e62597eaef1d886093df50dbab19763a4d758b394227c68d55596` | 0 |
| lib/spdlog/include/spdlog/sinks/systemd_sink.h | 4868 | `e312d6a5a52dc5acd6321833f18fb6c29a438a1f24ee5dfe3dd29a550f35887f` | 0 |
| lib/spdlog/include/spdlog/sinks/tcp_sink.h | 2700 | `92092dec86bdc1cfced58bd61a28c6c22cb5cb905050aa416437f9c9eb4a71a1` | 0 |
| lib/spdlog/include/spdlog/sinks/udp_sink.h | 1850 | `6eb0b04604fa84e63b1bab51539a281a0bf17c912b9b5a5f794efdb0ddab190b` | 0 |
| lib/spdlog/include/spdlog/sinks/win_eventlog_sink.h | 8888 | `4783a96f7b89b19d48c14eea3f82f3ffd659e8faf34a4446659cd0c2d822e39c` | 0 |
| lib/spdlog/include/spdlog/sinks/wincolor_sink-inl.h | 7092 | `ed4e3f9ed012bf495044e414e1f921311bba888bc905a515da41ddde35c8c557` | 0 |
| lib/spdlog/include/spdlog/sinks/wincolor_sink.h | 2688 | `75a20f219b48c8ff63d2e7a11db9ed748fbc9cef5198e9cf739b889062665aaf` | 0 |
| lib/spdlog/include/spdlog/spdlog-inl.h | 3264 | `eca55774acb8f0cbe05f18cfa95405fd5ff1ed041cd7372556b2eee39776a5ef` | 0 |
| lib/spdlog/include/spdlog/spdlog.h | 11866 | `54283b3e3bf96c3df22c40caea526ffe0bbf203b5f76a98aa130b91a50487195` | 0 |
| lib/spdlog/include/spdlog/stopwatch.h | 1865 | `60f3aaed933185261ae603cc589cd39ebf93ef78321548871d469fb566903c44` | 0 |
| lib/spdlog/include/spdlog/tweakme.h | 6610 | `8e641df000560090a11adb04eff3f1a18e814f6eb8f2a9a9a1f22c0dcc572f82` | 0 |
| lib/spdlog/include/spdlog/version.h | 417 | `a0c15d9295eba580732dada20940a443c53ddb47d8565c730d7af1ee5f3bd712` | 0 |
| lib/spdlog/scripts/extract_version.py | 497 | `3f44c716f1329bb0bb4d76ba89600987dc5993b1382255cb1b490bad9125cd0b` | 0 |
| lib/spdlog/src/async.cpp | 394 | `1a985a2d65548d858a8171f7eb298d38129e4e554909f77005b4f45fae790121` | 0 |
| lib/spdlog/src/bundled_fmtlib_format.cpp | 1417 | `26c11b7389cb98f18f054cf39a3c8b64ab180c439c8677772048aeec4d628fe4` | 0 |
| lib/spdlog/src/cfg.cpp | 275 | `1734c9cf9421c3daf4d682d5998cb2d3d4f51fb7d2a9be77a2340d0388f7e92e` | 0 |
| lib/spdlog/src/color_sinks.cpp | 3137 | `eb5c7d22aaba48eff1e70452c6f55255a4922e05f84abba048790c3ef70c7f2b` | 0 |
| lib/spdlog/src/file_sinks.cpp | 797 | `02bfd1ee0bbdb51e476933c8da2db30810dbda9ace8a31485dd3aa854805629e` | 0 |
| lib/spdlog/src/spdlog.cpp | 1134 | `e357d79d7816fe72f8d5203ee5624d0d73cf8f90076fa08302ce92035ae72ca5` | 0 |
| lib/spdlog/src/stdout_sinks.cpp | 2014 | `f28d35429c75493a2cc67857fea53e4ad345666b04cc58082e023e684b91de39` | 0 |
| lib/tracy/capture/src/capture.cpp | 12123 | `fb02c5266d877279cf532fdcafdb307fc01b287852971bf860c47006a8473dce` | 0 |
| lib/tracy/csvexport/src/csvexport.cpp | 9540 | `1ee8b802084a7de22d60eb06448fbc900747ea2e79651cf4a03fc0276442cf49` | 0 |
| lib/tracy/dtl/Diff.hpp | 25667 | `a06791ab40e2e84e67c7b7581165828a2c2984471c75cf8f98ca4f8dc7ba27dc` | 0 |
| lib/tracy/dtl/Diff3.hpp | 9498 | `2feb6d6188ecee1c0450ff4f1559751e5297b8d9efda9905dcaa91ca60483630` | 0 |
| lib/tracy/dtl/Lcs.hpp | 2050 | `1e035f2a3706dc6376f89fa24939ae06fecbf41fa8974d3c894bf9c0045ecb1e` | 0 |
| lib/tracy/dtl/Sequence.hpp | 2295 | `be03c007753898580cd280e3d2d87967015a44e21296cfad72ab0787020b52dd` | 0 |
| lib/tracy/dtl/Ses.hpp | 4415 | `02ba757b9e6b69103781045652f6649e41a2d062394dbcdfad2b9792892703f7` | 0 |
| lib/tracy/dtl/dtl.hpp | 1906 | `06b22d03297ac080f11b8bd75badf81faabb5c8fd4a7c7236248c6222a7d6bdd` | 0 |
| lib/tracy/dtl/functors.hpp | 5188 | `6f77255009046f1eb449e69a4d840bf80537ca23b5a6639d085e9bcebd3b0c1b` | 0 |
| lib/tracy/dtl/variables.hpp | 4934 | `236ade0eff4c26c61663a29145ebdc213b281ef770ad9ff82745ec12a83d5732` | 0 |
| lib/tracy/extra/color-hot.cpp | 1663 | `c0958417f2c14e4a25889d58599759c12e00c5b506c598bacdbc0085939c62ee` | 0 |
| lib/tracy/extra/color.cpp | 1828 | `7ec93b6c08c70a36a94c3972a62adb23e9b2d5046ddaacad3eecb054145bfca4` | 0 |
| lib/tracy/extra/dxt1divtable.c | 439 | `70a4450e5cf335ea056cd3589fccf20f3d4f3690e3a181f22ce89bceb8c501e0` | 0 |
| lib/tracy/extra/dxt1table.c | 666 | `ae35ac6b0a96fb1666a3edcee3b765e622147206b478c6d47ee73d17844beabf` | 0 |
| lib/tracy/extra/identify.cpp | 1436 | `54593eebaf9cbc36c6ff4bc29f1af5d77ff43f9b517d1bf3f10233f591f42f52` | 0 |
| lib/tracy/extra/rdotbl.c | 532 | `49574565e6ea82576a629fcd820c7256808994b0ce3c4e960f4d0ec6f19ce9bb` | 0 |
| lib/tracy/extra/uarch/TracyMicroArchitecture.hpp | 716 | `78dce31aef40bba29bb35e8124ff41e65b2b406f25e3cc77efd91eab110a24f1` | 0 |
| lib/tracy/extra/uarch/uarch.cpp | 10552 | `07b4e6de29ac9193f96bf045d04ebe78bc9a063619a19511338b97c79dfa5389` | 0 |
| lib/tracy/extra/version.cpp | 300 | `4ba9be87abfe13379683d49cd87f4c8f5ffc34d98804da8ca61a86f8562ece03` | 0 |
| lib/tracy/extra/x11_colors.c | 897 | `4d6a3c88f3e886cbcba5d8a627bb4b5e39eadb54dec560dbc2f84939c91cbd9d` | 0 |
| lib/tracy/getopt/getopt.c | 8492 | `caa9e8e8957c942ab6ad4159562016d78b2e473792de5811fdb7d66c5dd425de` | 0 |
| lib/tracy/getopt/getopt.h | 2307 | `8df4d7ce4f278be1ae62e133b41aed38a382b0be8eab78c172418c6e4b249556` | 0 |
| lib/tracy/imgui/imconfig.h | 10399 | `e1a10ba1fa942005454c9700694439e2550a0617cb05fc34ec87311d228d6f5a` | 0 |
| lib/tracy/imgui/imgui.cpp | 1060218 | `fe25a154e9737c64928eeac892b4a2dfc14db55b7498b0fc16b4a464c9b6133d` | 0 |
| lib/tracy/imgui/imgui.h | 350080 | `2580ce0dbbc7fb2c03598f3556e6ab36ffdc2f9119b6be69eaab79919b43c7b4` | 0 |
| lib/tracy/imgui/imgui_demo.cpp | 442122 | `8ca0d46ebd1ad6bb54b6b7a8fdfb76391c19d7d976142dfe3bf457a60d75bc8a` | 0 |
| lib/tracy/imgui/imgui_draw.cpp | 218906 | `869f342f83250cfc0e0d9d8b26ef217cfa5eb4d57a27dad3c75ffac12c992511` | 0 |
| lib/tracy/imgui/imgui_internal.h | 271493 | `60c082a40ff9263fe33a53606a2490e2e2b3a5c5873de4252d025ec91d4d0281` | 0 |
| lib/tracy/imgui/imgui_tables.cpp | 222752 | `39200172f9f17e59035255f967d59b337997fab377049a06da25dda4a05ce68e` | 0 |
| lib/tracy/imgui/imgui_widgets.cpp | 435933 | `ac1f1f7bfd6ac10bc4340815422d43c8d20e748fcff8dfd629a21ad732259fb2` | 0 |
| lib/tracy/imgui/imstb_rectpack.h | 20344 | `2efa3d5f7d003c19743b15155dad9f46d9f9fc783a18893d703b431d3c990972` | 0 |
| lib/tracy/imgui/imstb_textedit.h | 54857 | `3f4cf71a2b771d938f62ce4225df3ebe429b334fcdb3b89f1fedf43eeb0a3e1e` | 0 |
| lib/tracy/imgui/imstb_truetype.h | 199484 | `5b7693f174b0458c7bec5522c8d6be4fe606d3f5da5082351959c14e59269b53` | 0 |
| lib/tracy/imgui/misc/freetype/imgui_freetype.cpp | 45632 | `65e43b2935c18d8dffdb602ff6908c0991a47eab024d2cd5c2d073b854f83a35` | 0 |
| lib/tracy/imgui/misc/freetype/imgui_freetype.h | 3601 | `481ecb27aa90fbeb01a96d8663465fd1c40b2f2ce3e8713dd9118c0133b317e5` | 0 |
| lib/tracy/import-chrome/src/import-chrome.cpp | 11540 | `ba0ee85f891b7c27df4728a897ee72c7332e911a9861c8cef04c202f0fc910d8` | 0 |
| lib/tracy/import-chrome/src/json.hpp | 907858 | `665fa14b8af3837966949e8eb0052d583e2ac105d3438baba9951785512cf921` | 0 |
| lib/tracy/nfd/nfd.h | 11200 | `8e17f52a84c26c2a1e5b136d2e6c1f64fe67c64f3c9883d1132c622095f0b573` | 0 |
| lib/tracy/nfd/nfd_cocoa.m | 13920 | `b2ad811e652afaa20cbdeb52a85627d1efbb5f05966124e988e4853ef9eece13` | 0 |
| lib/tracy/nfd/nfd_gtk.cpp | 22680 | `810bac6ad4f729ae4e05169b739e645236a8e4fba8716ebc55edc4b6198fbbf6` | 0 |
| lib/tracy/nfd/nfd_portal.cpp | 63775 | `dbb4e66831ee73c19dbc17a0cb867deb9325faeb8ce8256c7477eeefdcfdb96b` | 1 |
| lib/tracy/nfd/nfd_win.cpp | 32686 | `6897abb0967cbc8fabd4640239482a985d2d2943513792c668247726d7eacd47` | 0 |
| lib/tracy/profiler/build/wasm/httpd.py | 628 | `0fdcd467fafcc0f0723a92dd7bd75e7b19c1c0b4afd425d24f812384fbc6e800` | 0 |
| lib/tracy/profiler/src/Backend.hpp | 577 | `4768574c71f335393f6d59e4e9be2619716b01dd2516f26f72e964e0af8f7d62` | 0 |
| lib/tracy/profiler/src/BackendGlfw.cpp | 5782 | `229427fccacb5d63541f870d9ab0d09313f36fb533b823512ac7109aeb0f5e42` | 0 |
| lib/tracy/profiler/src/BackendWayland.cpp | 26458 | `3b81dfee65aba638234cadab2a6d85303bec59c3ad9d9f8a3f9761a6853ecea4` | 0 |
| lib/tracy/profiler/src/ConnectionHistory.cpp | 2285 | `d46a8966fcdabc0c4993a19b7417e1b47946c8c3a822c527b3077d9d41fd10f0` | 0 |
| lib/tracy/profiler/src/ConnectionHistory.hpp | 721 | `39d20ff03942cb7515acf5439249b1c2459c32869d182eafa1dc127c0d8fabec` | 0 |
| lib/tracy/profiler/src/Filters.cpp | 2000 | `75ba202db7e611502c378ac00481b921f63b034d758844410c8695947f214c85` | 0 |
| lib/tracy/profiler/src/Filters.hpp | 436 | `563f4388bb6c34f7481494cd98725750db8477cb5ecbba7d9881eb09e6b6fa8e` | 0 |
| lib/tracy/profiler/src/Fonts.cpp | 2615 | `e7c41a1c55ca33a4f83eb9c3d47906232576c67a5321e1f46fee2332c5938922` | 0 |
| lib/tracy/profiler/src/Fonts.hpp | 252 | `2206f6feece0deca57ff8b4484a8ae0c7c7ebcabf84fab65cd291009dc3c5c52` | 0 |
| lib/tracy/profiler/src/HttpRequest.cpp | 3555 | `5b3121e6a559186dfc9582f4e815ce4ef5a750d6c4318463db79f06da650d6e2` | 0 |
| lib/tracy/profiler/src/HttpRequest.hpp | 203 | `46a5cae8fa55af260d3b2a9096a80c11e71dabc478b36dae3db0d4dbd1d6a10d` | 0 |
| lib/tracy/profiler/src/ImGuiContext.cpp | 529 | `51942880a171cc0e526c8ccb9d0aceab868647a02a748c754e0b86c07d0a3d66` | 0 |
| lib/tracy/profiler/src/ImGuiContext.hpp | 215 | `d37da6863dfd690b76d2462d50629297c601f1fb652052aa91282b868631d5c4` | 0 |
| lib/tracy/profiler/src/IsElevated.cpp | 615 | `4201d8d41808008fe9f8390d9fe6e1a18436d43733aeb5934607a3b1c3631c62` | 0 |
| lib/tracy/profiler/src/IsElevated.hpp | 82 | `0356f1abe09219e8eaff85c6b05a063abb34491dfd4db2a8ea07bb54b82ae4b2` | 0 |
| lib/tracy/profiler/src/ResolvService.cpp | 1463 | `ce3882a006afe0590733ee5f06e0b1de374a099616824be31c7cde296d738479` | 0 |
| lib/tracy/profiler/src/ResolvService.hpp | 715 | `1c39355027f911e8b81c949f0300496abd7de62021e78058c49df5afb45ed21d` | 0 |
| lib/tracy/profiler/src/RunQueue.cpp | 636 | `0504908971a81a57fd39327ae044129bfd17a92cb04f02be15f338eb7035dac6` | 0 |
| lib/tracy/profiler/src/RunQueue.hpp | 387 | `54d22406de6dee54b0da7c7788a71d6b5a30326e80dda82677d8b26338af5388` | 0 |
| lib/tracy/profiler/src/WindowPosition.cpp | 979 | `3906a9b6e20a66d93adbe4aa375a9406cb136fc0d2050b3ecaaa9c3832253189` | 0 |
| lib/tracy/profiler/src/WindowPosition.hpp | 254 | `e186573c917fbd5b686ed300b44dade0e3c614180a871f6d3bb7fcb45e0ad4c2` | 0 |
| lib/tracy/profiler/src/font/DroidSans.hpp | 418892 | `70dc20d5ddc88350c8b4df1a15b041733c6dfb0b117672fe73ddb8753cf2c820` | 0 |
| lib/tracy/profiler/src/font/FiraCodeRetina.hpp | 593686 | `36fdb30e3fcadaa4e1ba79afd7102ccf04387eba81ddee685de5c33b30fcf312` | 0 |
| lib/tracy/profiler/src/font/FontAwesomeSolid.hpp | 1841209 | `bdf624549c0e31e172b14482072fe35ce624cbbc1e0e003dfcf9febfa0559b2a` | 0 |
| lib/tracy/profiler/src/icon.hpp | 2829 | `06c448c7818d7411d8c73591b514f501e790b144ee4f6cd1a737baaa2a406845` | 0 |
| lib/tracy/profiler/src/imgui/imgui_impl_glfw.cpp | 69040 | `cb6139815c1780bc439f4fc5ef97de7d25890a021ca4b757c40e23e03f7b333f` | 0 |
| lib/tracy/profiler/src/imgui/imgui_impl_glfw.h | 4048 | `5d0e20adda8f722564403eee002615cb458f11266291763cbb0916c9896a4c5a` | 0 |
| lib/tracy/profiler/src/imgui/imgui_impl_opengl3.cpp | 48398 | `2bf511925e6acc84ad8086947c6a0cd6c255111c40e3488c5491497d2400f75b` | 0 |
| lib/tracy/profiler/src/imgui/imgui_impl_opengl3.h | 3409 | `2a9b96b83ad0ead2a0ffb394e6c0069b490ce142e5677f83f2850d32a801668a` | 0 |
| lib/tracy/profiler/src/imgui/imgui_impl_opengl3_loader.h | 35962 | `b2933309b6e1656694ea81648dc817d7bad71cec948a489b61d1da1518d353bb` | 0 |
| lib/tracy/profiler/src/ini.c | 6005 | `a6ea2981ee05476937f53aa9ead534efd26f4765811562e0f0df541468a306dd` | 0 |
| lib/tracy/profiler/src/ini.h | 606 | `2fad721941f145186292120b99a71fc685a2ad43d82867580d571cb0290d410f` | 0 |
| lib/tracy/profiler/src/main.cpp | 42246 | `c077cc8046f7f23ce08473eb706090f493c990b2e2172f1610d8a4c518d55937` | 0 |
| lib/tracy/profiler/src/stb_image.h | 284733 | `38e08c1c5ab8869ae8d605ddaefa85ad3fea24a2964fd63a099c0c0f79c70bcc` | 0 |
| lib/tracy/profiler/src/stb_image_resize.h | 116516 | `6a0e75adbabb48df9031c2e39ccd97437bb226fe31e7d4a01c7bf70a18d32ec6` | 0 |
| lib/tracy/profiler/src/wayland/xdg-activation.c | 2994 | `9b62187117fc94d0fbea5f9a9505c6ccc20107fa5bad8bc36166a5568470e6c8` | 0 |
| lib/tracy/profiler/src/wayland/xdg-activation.h | 15153 | `7058f26dcfca034afaf4e721d4ae1a71408a6c6c72b133e9bbd14ab20235e420` | 0 |
| lib/tracy/profiler/src/wayland/xdg-decoration.c | 2784 | `7f039cf8ff475a9b15b086c15a8da6af8600f4138b6e49cd97208c46d40ca617` | 0 |
| lib/tracy/profiler/src/wayland/xdg-decoration.h | 14212 | `59f3e7eff1bc9a799b55dcc56d2566fe1cdb53ebb593b8ed0b91998b405bf3a1` | 0 |
| lib/tracy/profiler/src/wayland/xdg-shell.c | 5978 | `8619b0f278b0bf0946eeb072a61a06cda47b8a6e86a09abea7059fb6a8397216` | 0 |
| lib/tracy/profiler/src/wayland/xdg-shell.h | 81060 | `019b0347295f1886ba22ebbe537157b5a5bbc187ee648e212abedb0f4d53d8c7` | 0 |
| lib/tracy/profiler/src/winmain.cpp | 1728 | `e0b8bba178ade790a34fe6382d1e6fa326b2f185dcc6e4f53f85efc4e3b144c1` | 0 |
| lib/tracy/profiler/src/winmainArchDiscovery.cpp | 258 | `bb08f512ff925b45000079723b9af9fbe64fa73aa126e17265d2c56172971245` | 0 |
| lib/tracy/profiler/src/zigzag01.hpp | 582 | `61df087a72034fd7b930cb929926952987214e8a8c9b517b58672c24023a8eab` | 0 |
| lib/tracy/profiler/src/zigzag02.hpp | 606 | `72ecb533927a42b1e9088710ba9c96adb958a529db226a1fbafaad23e7dd3bda` | 0 |
| lib/tracy/profiler/src/zigzag04.hpp | 659 | `657bda47207e42739282310d675ee49221bae1a07dddb850cb90a561762af311` | 0 |
| lib/tracy/profiler/src/zigzag08.hpp | 779 | `6293a601dd005a4ef290de4478aa1563805a579c93425e384ff690a8fa656c14` | 0 |
| lib/tracy/profiler/src/zigzag16.hpp | 916 | `272794a2e3990900e81e70098e06971cdff82c66b43c072131f4aece24c71d64` | 0 |
| lib/tracy/profiler/src/zigzag32.hpp | 1005 | `6e37ee786479f0d026e16c950b3f60fcdafd717a31670e1d2f033007a2752c7b` | 0 |
| lib/tracy/public/TracyClient.cpp | 1517 | `deb8a783ab61ede3c12dc0e87d3f0d686699cb14a8f0e5cfe553a80e14664bcd` | 0 |
| lib/tracy/public/client/TracyAlloc.cpp | 1055 | `fba9bd76d112085ec9795c26e91dc0d8b9896a457fd2d37b32c01e943a26f985` | 0 |
| lib/tracy/public/client/TracyArmCpuTable.hpp | 13769 | `2b7f8a31de754ed664a2129d6332a439c2e4f5280bec433be98292bb27962ecf` | 0 |
| lib/tracy/public/client/TracyCallstack.cpp | 30918 | `7b30fa2e460229ddbff5f4d84c82d85121a985b3075e368f8f25a345b6e71499` | 0 |
| lib/tracy/public/client/TracyCallstack.h | 750 | `818f0cf86c9c53c09d066d84d48b460b46970595ff40488146b3a284298ae17d` | 0 |
| lib/tracy/public/client/TracyCallstack.hpp | 3172 | `e7dcb4df57321444a685a189ceb0ddc47c8629b58b00f980335f467d903e35af` | 0 |
| lib/tracy/public/client/TracyCpuid.hpp | 435 | `91f4b9da8b860b4b9f91e69668d3d29e384fd72f311b5458856562aec01440cb` | 0 |
| lib/tracy/public/client/TracyDebug.hpp | 202 | `038afed2e613d22f859f0937bfb7a07c6be5567cc33051c9dbed6ea613257e27` | 0 |
| lib/tracy/public/client/TracyDxt1.cpp | 32169 | `0bb2cb8a068492f93de5083ac00e7cb3ddce4afbf101a5c42f861c23b3013518` | 0 |
| lib/tracy/public/client/TracyDxt1.hpp | 151 | `3c21b2ec285b969b0f7aaff8a576a57ff5a32afd41c195a1943407654005912d` | 0 |
| lib/tracy/public/client/TracyFastVector.hpp | 2673 | `aec011fc54b1df82b6e7ffd78e974a85869cdae91cfaf73178114b4a54044c86` | 0 |
| lib/tracy/public/client/TracyLock.hpp | 17130 | `a29ed7b4206efa3322f828553ff6ab6c1a8840ba690fef660347e4156712df01` | 0 |
| lib/tracy/public/client/TracyOverride.cpp | 509 | `32fc9564d3ce6503b98d05517fff87aa3c0414ef092f3ef09e0aa93ae6732aa1` | 0 |
| lib/tracy/public/client/TracyProfiler.cpp | 151191 | `00cc8e12eeedf21bff0aac7cd09796b594129df916cdf22b14f9db680d53bf23` | 0 |
| lib/tracy/public/client/TracyProfiler.hpp | 33037 | `7fcc0962c224d840c855723e949304e8e90643146e38e8f6ec621fc77feba3d1` | 0 |
| lib/tracy/public/client/TracyRingBuffer.hpp | 3598 | `0ce9c5397676edd0c45e88ab2c10f32c6239b75dca38b5cc099c90e3ef6a954c` | 0 |
| lib/tracy/public/client/TracyScoped.hpp | 5890 | `1c7644b1d08868634b34531c57e892b7b7fa97a660fe463424024ce19bff8d58` | 0 |
| lib/tracy/public/client/TracyStringHelpers.hpp | 837 | `b655b26bf0df158e763f516aefc82faae81bdaa9213585a406bfa2be77515e01` | 0 |
| lib/tracy/public/client/TracySysPower.cpp | 4742 | `ee978bc06af793dfe3beab07fb8ec7b6a90920d8ffdab949c438c5ee1c47b49c` | 0 |
| lib/tracy/public/client/TracySysPower.hpp | 592 | `bb1edd89aa226572e6af54aaeadd22062f2636fd4c966ac63f642b1342f58903` | 0 |
| lib/tracy/public/client/TracySysTime.cpp | 2390 | `a4a91849b4fd546f6b9f0f3b0fc148bca14dfd520f18fd24a566a78749553a7f` | 0 |
| lib/tracy/public/client/TracySysTime.hpp | 435 | `a5a9a18671ab22c19bd88db1512be516d72e60509af4d836bec2b97b1c85b62e` | 0 |
| lib/tracy/public/client/TracySysTrace.cpp | 55338 | `969ed81689aa53d33663f458d3568da9874410bd9148a2813fa25cfeb9cbff95` | 0 |
| lib/tracy/public/client/TracySysTrace.hpp | 539 | `ce9286198ed1f218d9ee9edf298cf10f3b3832174af29b88850975390d510fb2` | 0 |
| lib/tracy/public/client/TracyThread.hpp | 1579 | `5c02df54ebda30ffc6d31e5b415a6c7a5b680781665bc3403d3a2a887270399b` | 0 |
| lib/tracy/public/client/tracy_SPSCQueue.h | 4954 | `8cb74f10b233693d83da294dc48aa8ba8bb2a860a1d4dafb19dfbe3a76620a70` | 0 |
| lib/tracy/public/client/tracy_concurrentqueue.h | 54120 | `f94ead8ee471b85320a4b549e1916919c7018f651ec00244642f4d7ca8eab74e` | 0 |
| lib/tracy/public/client/tracy_rpmalloc.cpp | 125674 | `4ceceed51c147716993764c23711e824005e899861abfd1ff6ae03e23edda74d` | 0 |
| lib/tracy/public/client/tracy_rpmalloc.hpp | 17850 | `5db11b9a63d08da1a9381a08c4f0c61f140c2cea44d84cee26d4c04fdc0c667b` | 0 |
| lib/tracy/public/common/TracyAlign.hpp | 394 | `316d6ec57c62834d2b83adde547f001160832705aa86abc46336709b1bdd615c` | 0 |
| lib/tracy/public/common/TracyAlloc.hpp | 1186 | `60706b629718792fff32372da4efa710a76d6bd7ca503eb20572f26c8158c5c0` | 0 |
| lib/tracy/public/common/TracyApi.h | 352 | `6198a31de880ab2037dead016f98392b25c2aa14c1151985a9576cb970b1d306` | 0 |
| lib/tracy/public/common/TracyColor.hpp | 17206 | `a9dc70ed1921fcca3258909d1a941f91bb18f6651c225d40e36ded48324a6640` | 0 |
| lib/tracy/public/common/TracyForceInline.hpp | 465 | `b4035600f7f1042c76e79d418fd49d3217d339a6b9435ba57528eaad6bda230e` | 0 |
| lib/tracy/public/common/TracyMutex.hpp | 255 | `e63b7a9cde4000c07cf4c965733e063762181ec3c11124cb93713eb55a54ab0b` | 0 |
| lib/tracy/public/common/TracyProtocol.hpp | 3875 | `1a0a3c59a4aee743612f2757ffc1326fd800284fc714ad929b41e4489ef2f7e7` | 0 |
| lib/tracy/public/common/TracyQueue.hpp | 21840 | `c6a21f631a564f3db17b73d4f369887dccb9960207ffb410233236cc4cad5d7e` | 0 |
| lib/tracy/public/common/TracySocket.cpp | 16888 | `afa23d4df9de37ac4ae2c2d2695901b9c0ae815f6c3eb94ac344b1c697a5fe74` | 0 |
| lib/tracy/public/common/TracySocket.hpp | 3236 | `b52b40eb848f799b2a3a7156b8a377630c40cbe0d6251690db16fe6d49794999` | 0 |
| lib/tracy/public/common/TracyStackFrames.cpp | 4471 | `30f20093ed436e65664f325c099f1f675737371b60d7e7f12b07cdf710a41f23` | 0 |
| lib/tracy/public/common/TracyStackFrames.hpp | 322 | `fbd2359bd907581b97c66a286dcda3eafec884498af260d108b38d2dcb06fc58` | 0 |
| lib/tracy/public/common/TracySystem.cpp | 7830 | `1792279e8e99a294fff4d378de84f3ea8e4667c320edc65bd9ed3ace951d86ba` | 0 |
| lib/tracy/public/common/TracySystem.hpp | 508 | `48f53687880d755d36c7df2ad4e89d78f16e08cc239fb072bc03a97559828dbb` | 0 |
| lib/tracy/public/common/TracyUwp.hpp | 245 | `403314c51903d0468a2a14c1402ff367149410931823919e6464739c1d9ca5b5` | 0 |
| lib/tracy/public/common/TracyVersion.hpp | 170 | `52fd0ea9757bdd32a47ae7ca378f3367fe0e247b1e762be99a61cb97f1296ca8` | 0 |
| lib/tracy/public/common/TracyYield.hpp | 512 | `7d4ea857b76a6c2a2d010579075a0fde28969c8e1201f5573239cd0288a311cc` | 0 |
| lib/tracy/public/common/tracy_lz4.cpp | 113348 | `7c8fe2308b1204e0f89fcca03b9deb828ad6dd20ac34900f61a5309c1ba5897d` | 0 |
| lib/tracy/public/common/tracy_lz4.hpp | 43279 | `4b3b0577518f334dee2c851f74f3fb4e940ba04e5d16deb18d00c2adacd8e7f7` | 0 |
| lib/tracy/public/common/tracy_lz4hc.cpp | 70167 | `71218c5612140f6d655f79458c43bac1e172f0f89d594f89679bff6628ba66b6` | 0 |
| lib/tracy/public/common/tracy_lz4hc.hpp | 20095 | `6284759c4a4c92750a61158af8c891b74cb7200a0931dd11faaf3e4d40004620` | 0 |
| lib/tracy/public/libbacktrace/alloc.cpp | 4538 | `7f6026e65e7bc7d1406a99d1ec798491dbd04d28862fe3ab61216f6eb313fc32` | 0 |
| lib/tracy/public/libbacktrace/backtrace.hpp | 8731 | `79231477cf0483608aa3f640a2d4f7d8aa8f239b4916e8bd60e4db3d00dec72b` | 0 |
| lib/tracy/public/libbacktrace/config.h | 598 | `2734b54de6d7695205c7be60cbb67d404e15ad86f04091f049cea85c6d52aa8e` | 0 |
| lib/tracy/public/libbacktrace/dwarf.cpp | 117229 | `3302aa6845e2e89029d24f6ecdc9589e26c5defad26eadff47741e036e43800f` | 0 |
| lib/tracy/public/libbacktrace/elf.cpp | 192608 | `b5d1f6e7d31d749990f4cc906d2323e0e22db6ec9ebc4c6b8c29943f635f4d74` | 0 |
| lib/tracy/public/libbacktrace/fileline.cpp | 8882 | `3e756c3a98a72d4e26b14000d207bc6ee6365c21e2fc8b459ea7169d5fb21adf` | 0 |
| lib/tracy/public/libbacktrace/filenames.hpp | 2149 | `8d2c2d284c3f071a8b418c2ce71e42e48b48caa0c4485b7319a4afe82b236c36` | 0 |
| lib/tracy/public/libbacktrace/internal.hpp | 13040 | `03f0e954f04968c0c59069aa6b21edb15078795aef14494b2a7fce83c890900a` | 0 |
| lib/tracy/public/libbacktrace/macho.cpp | 36137 | `64f4b6e3009715539e2316cb42036ca3bd3979f12807d87fc56d07263ccd2e3c` | 0 |
| lib/tracy/public/libbacktrace/mmapio.cpp | 3185 | `451eb6f0dcefb25b3ece0cd1fc18f993ec5b206fa54ed80bcefe102032517669` | 0 |
| lib/tracy/public/libbacktrace/posix.cpp | 3169 | `27038d75f4c8fbcc943ea8663cc8a2fac940e9995b0df5d679f8adea7d77a927` | 0 |
| lib/tracy/public/libbacktrace/sort.cpp | 3201 | `1bf7600c9186e86b1dec6f256231a3d6b348c3627e8bc6007c4ebf828f90c9b5` | 0 |
| lib/tracy/public/libbacktrace/state.cpp | 2426 | `33969d1444b919e0533dae8890c20c1d143cbb432aad3b683ac81de308cc493d` | 0 |
| lib/tracy/public/tracy/Tracy.hpp | 16870 | `c0c44f13aeadbabeb504fd0f21720d0f8205ebdcb674310ba8475289e961ae6d` | 0 |
| lib/tracy/public/tracy/TracyC.h | 18894 | `e25d321aa59e32e166f7c78f0073725e726cc19a225df0948076c74f1abbe255` | 0 |
| lib/tracy/public/tracy/TracyD3D11.hpp | 16973 | `2ac2bd211ee2b541ba217198a9fbea225ff53d7e0fab7b4375a3e8898310cf9e` | 0 |
| lib/tracy/public/tracy/TracyD3D12.hpp | 21558 | `c8990d2aaf6a3f0049b46013200d05a74e9490e74d0223e82bf45ab4dbefa0c3` | 0 |
| lib/tracy/public/tracy/TracyLua.hpp | 12786 | `feb39a711db897706e2d8f1fa25c66bece5958a27b39b1d7268030a0981af009` | 0 |
| lib/tracy/public/tracy/TracyOpenCL.hpp | 18610 | `23b8b778f691105975df993f74717e7371857e0a3f379cd631f39ad7e9a71023` | 0 |
| lib/tracy/public/tracy/TracyOpenGL.hpp | 13404 | `1166d9a745742bcefffc390039e1f2507c22a9ffa8d370e4eb0a15fd833054cd` | 0 |
| lib/tracy/public/tracy/TracyVulkan.hpp | 30297 | `dbeac1bfc55106e61a7dfb99e5a9237f4adfa04df41ce713da8992a2c67027b1` | 0 |
| lib/tracy/server/IconsFontAwesome6.h | 73902 | `0c741829ad4d4d1fa21b58cca5fb106fc1fc99e4a6e0f49e36ba322186c71056` | 0 |
| lib/tracy/server/TracyBadVersion.cpp | 3464 | `0aa9c129dc6a64da36fb2a783007eebc381750b555d5e55968f1277a85e373c3` | 0 |
| lib/tracy/server/TracyBadVersion.hpp | 603 | `26f0dd71a8620df4c5d11a319e35c451f6aab1e7a04d53a351b6f9d223a7f4dd` | 0 |
| lib/tracy/server/TracyBuzzAnim.hpp | 706 | `bfd87aabca77c995f2c374cc7b46ccb703155f14da5cea289c481c4353a092c4` | 0 |
| lib/tracy/server/TracyCharUtil.hpp | 1253 | `b85d2614117e9ac12d8f817491b33b86543816e3f35c2d8ff63ecfee985cdf12` | 0 |
| lib/tracy/server/TracyColor.cpp | 899 | `cde7a57b0c86bffcbc49312e879e5f56cf71d0b0399d3e4173d6278f35e44b81` | 0 |
| lib/tracy/server/TracyColor.hpp | 1175 | `4670b199cb5d4dbaa0e924a4acbb17708f1e062c4341c62729d7d4aef599fbea` | 0 |
| lib/tracy/server/TracyConfig.hpp | 165 | `cad37d16f4b9b32e657f204a09bedcc5de79adeb33d03b03523c9fa5dac55196` | 0 |
| lib/tracy/server/TracyDecayValue.hpp | 843 | `ab57e79c6f655572bfaac7c825f6c2a7d92d20e2787d76e0f9e99c603a153f60` | 0 |
| lib/tracy/server/TracyEvent.hpp | 25175 | `2f2fbf79820f0ac121c6524226b5a51a58b5decd4124416b1068fe9cc0409d76` | 0 |
| lib/tracy/server/TracyEventDebug.cpp | 13503 | `d6d84726bd5b6785c4412e617fa268e00a57cce90bf2a451b32f2c6977fe4e50` | 0 |
| lib/tracy/server/TracyEventDebug.hpp | 151 | `9790f34d8d270eb6aa7a87001572242bf6afca32016055ca2c5e4a13ddae122d` | 0 |
| lib/tracy/server/TracyFileHeader.hpp | 419 | `085b631031f3c302f4936a3bb1208b67967bb6733baaae3aa95d365fc30dcbf5` | 0 |
| lib/tracy/server/TracyFileRead.hpp | 23312 | `8094b78b75fb79cfb1e8fbcab3d838869bf8081812361b8449b85fb897e2e051` | 0 |
| lib/tracy/server/TracyFileWrite.hpp | 4674 | `8914e80fbed46f73e42754acb4d348191fad0822220326fa5502dff46cc8c755` | 0 |
| lib/tracy/server/TracyFileselector.cpp | 2916 | `24caafa213224490451a78c21b46a849883e8be9bc04e671935438f7d0729567` | 0 |
| lib/tracy/server/TracyFileselector.hpp | 389 | `f6c86932b8a54c4759dfe0d10014aef4856cc84a0a8a7e0549aebcc9d9737399` | 0 |
| lib/tracy/server/TracyFilesystem.cpp | 452 | `60cd978d569a4c7e94399bbac50adf9f74a2bba77e5df71bcb0d4094e00c9b9d` | 0 |
| lib/tracy/server/TracyFilesystem.hpp | 407 | `af93073f884593f9475030e93bbf2aa5836d3e50a6a1f4e73a4c3a629185f8aa` | 0 |
| lib/tracy/server/TracyImGui.cpp | 3441 | `42df42356c331905ed11bf4927afb63546a87747216b9ae3475d27ed6cc4c851` | 0 |
| lib/tracy/server/TracyImGui.hpp | 9308 | `102e2cea6265899b076858cc4fa972f5ada3fce435d5a761fbbc9208351d92d0` | 0 |
| lib/tracy/server/TracyLockHelpers.hpp | 541 | `8fdb2ad965e91feaf9c79a172409bd9690cb3490b4ae1f91524dff8656db9390` | 0 |
| lib/tracy/server/TracyMemory.cpp | 71 | `c9bac89b14452f4ae3e6d483f3f9aac67500d0c6e70f553e1b3cce8576628c57` | 0 |
| lib/tracy/server/TracyMemory.hpp | 132 | `1997a428e82ed9a3a6296a56346cbce7b78793a75680e75efebc4ad14ee9e807` | 0 |
| lib/tracy/server/TracyMicroArchitecture.hpp | 716 | `78dce31aef40bba29bb35e8124ff41e65b2b406f25e3cc77efd91eab110a24f1` | 0 |
| lib/tracy/server/TracyMmap.cpp | 938 | `14866631b95206189e8c934d5a99039ccd69161659fad995cc5479c3ba5c8331` | 0 |
| lib/tracy/server/TracyMmap.hpp | 361 | `89bb36c6625da403b041d78e7aa5afcf840832169f84ea574411ff0d5dc33c9b` | 0 |
| lib/tracy/server/TracyMouse.cpp | 2404 | `d11a9bae63bfdaa4854125baa163bfcfe77f53e00f9fe779d51f7ad7be0e915a` | 0 |
| lib/tracy/server/TracyMouse.hpp | 427 | `94b15d8464ef0f65da5cdaec9444573fb6d59a1b36adf66b77194b3523c837c1` | 0 |
| lib/tracy/server/TracyPopcnt.hpp | 939 | `998fdd92511499fcadf6a9b30e739b468dc1a63a52f82ef06363d639927c0e93` | 0 |
| lib/tracy/server/TracyPrint.cpp | 10335 | `74905758c19c3828a986346b6c2a42a7c97224d1acd449e025220a13531d91ab` | 0 |
| lib/tracy/server/TracyPrint.hpp | 3370 | `3297ba68c21cc605739d38e75a95716e3d1b309ecca12722ea8e3d39319bbc3d` | 0 |
| lib/tracy/server/TracyProtoHistory.cpp | 874 | `193f0847266c17bcc0f4a5df4a5a7c972668874287a6b49acac8831687c76194` | 0 |
| lib/tracy/server/TracyProtoHistory.hpp | 265 | `ed041a3ad791f6c6e6c2293169146edd1f14bbcee3cef1a01b29c6923d02df15` | 0 |
| lib/tracy/server/TracyShortPtr.hpp | 2238 | `1ab7d9a07650a38ba77c193ebff814cea6c003d4aff1e8c3a8865e6af83553d7` | 0 |
| lib/tracy/server/TracySlab.hpp | 3353 | `c9e481300c8582ba88f4e2651307fbca174732ede64cc3ddc7c92676d873e717` | 0 |
| lib/tracy/server/TracySort.hpp | 439 | `de7abaea37d1237ce1043f48537746770f42f4c5e649c4f1c004a51ac932a7e0` | 0 |
| lib/tracy/server/TracySortedVector.hpp | 3684 | `0a5fe363b7e019301b1a0f9cdbbb6c51e253c551a0499b04db38598cae106182` | 0 |
| lib/tracy/server/TracySourceContents.cpp | 2304 | `8e6a9d92b6f366ffbb21dabee665fe92c231825bb055408f23dd0646cea2c642` | 0 |
| lib/tracy/server/TracySourceContents.hpp | 851 | `77eb831f5f75a11be68fc0d11e4d4395893e0b892bdea1abc932e19566bb3c41` | 0 |
| lib/tracy/server/TracySourceTokenizer.cpp | 17990 | `64ba9a4d12f8ace39fe94a842dd51e7b4bf995349b08b472ad385afead5b467c` | 0 |
| lib/tracy/server/TracySourceTokenizer.hpp | 1389 | `0ecdc2d9e2399ed7548ebfe791c7bd583e068fbcc2a4e7f56028a0e864b68c78` | 0 |
| lib/tracy/server/TracySourceView.cpp | 221118 | `ebfc4f72c6adb33430a3ec41b2f68ff1dafc8efc6aa6d472ee382e86d492db7d` | 0 |
| lib/tracy/server/TracySourceView.hpp | 8943 | `701aa3aefaed65492dc5e832b09839f5e563b7e6b56f3726c31bee74fc5fa5e5` | 0 |
| lib/tracy/server/TracyStorage.cpp | 4072 | `6027c5858a92a7973f27d8b787838e6aa85f227c6ef4f06e792bd1fac4b3f02f` | 0 |
| lib/tracy/server/TracyStorage.hpp | 249 | `81beb41841f47cd3646767207bab4f3a4dac52913e508d479db9621a49bb2d65` | 0 |
| lib/tracy/server/TracyStringDiscovery.hpp | 2256 | `5cad31298025dbcc91f4dfc12407ccfadcd1e03160fdbe39561000ba18542ffe` | 0 |
| lib/tracy/server/TracyTaskDispatch.cpp | 2037 | `0292360e9292638d9c4a8307093cfb45e364503236f5973b3a4f4b00241fb6dc` | 0 |
| lib/tracy/server/TracyTaskDispatch.hpp | 750 | `f99cfb1f6ab426407a27cf03924f49e8378e14873302fe4b695ab6e482bea954` | 0 |
| lib/tracy/server/TracyTexture.cpp | 5324 | `8ff977ceeb745a537d1f7073e08da4c8c6b1ca2735b21588baea531672ba6216` | 0 |
| lib/tracy/server/TracyTexture.hpp | 476 | `dcafef8cf780495955bffad915a831c2c47847263dd71fd207ad472974befd02` | 0 |
| lib/tracy/server/TracyTextureCompression.cpp | 8873 | `9a7205702308b62fb71155f51fd0f900ed3f7050ea8ab164cf060955e247545e` | 0 |
| lib/tracy/server/TracyTextureCompression.hpp | 1657 | `8b4cd1fef2dee857773e836d9a7d448910ebb1aac4db79e2d7c43c473c0dc026` | 0 |
| lib/tracy/server/TracyThreadCompress.cpp | 1584 | `8e69b6ee530951e052f525c2cf818a718e034f9704abf0df390eb59b14b9f95e` | 0 |
| lib/tracy/server/TracyThreadCompress.hpp | 1401 | `74d8296bdd86b2c20bfc1260ad84d461e56d5ff7ec68f6a6ff92a407687cfa00` | 0 |
| lib/tracy/server/TracyTimelineContext.hpp | 307 | `8f2da2d1e4d51ed69ebd022562d0664caf3f8f9c885d5b05623e49eeb7bc1cef` | 0 |
| lib/tracy/server/TracyTimelineController.cpp | 4894 | `93b7616816bf01b1061d101765d1f73ada221f5bb046a10bdf754d0d7c86e4db` | 0 |
| lib/tracy/server/TracyTimelineController.hpp | 1704 | `4abb838c024898a7ab88f4d98890e5b8e5fbe0cce3fc7bc490fffea3d7f273fe` | 0 |
| lib/tracy/server/TracyTimelineDraw.hpp | 1406 | `9a380a563a09266ac2968ac1ec46158b3894eb03ccf585f9ac58d4c7cd847b68` | 0 |
| lib/tracy/server/TracyTimelineItem.cpp | 4581 | `a12da9bae4b9034c25584d83257b6203d2ac965934ac630dc33f2df0fc28f485` | 0 |
| lib/tracy/server/TracyTimelineItem.hpp | 2053 | `5838edbc19e5440f9e73ee386823a53a95486c1d086650568038bce1f9110f3e` | 0 |
| lib/tracy/server/TracyTimelineItemCpuData.cpp | 7952 | `c0ffa5d02f8e9900d39904417be77928ee3ba796d467ab97f35e0bcb2ac57731` | 0 |
| lib/tracy/server/TracyTimelineItemCpuData.hpp | 1358 | `a2558a22dc0539e702b17e319fdf891a0612f1579b2e23cd65d7604175e44020` | 0 |
| lib/tracy/server/TracyTimelineItemGpu.cpp | 5984 | `077077ca85e3e422d7bcd8da0f5dde92c6c10440d7dcadfb3e2975c4abea0267` | 0 |
| lib/tracy/server/TracyTimelineItemGpu.hpp | 1004 | `64e029502c020c35c5267e978cf936e1ebca5ae495074c583f892d5229010bb4` | 0 |
| lib/tracy/server/TracyTimelineItemPlot.cpp | 7610 | `b002a751b580a7f8da121db242363894f734273a3a1a6ffc57ab3cd492868e23` | 0 |
| lib/tracy/server/TracyTimelineItemPlot.hpp | 1154 | `c5ba44c75d5e602b0f8ea1f342120778e16cd714770e9d9ae8cbe8341918a013` | 0 |
| lib/tracy/server/TracyTimelineItemThread.cpp | 35552 | `9c07f8d2dc5f6d0ca15b13bdd59050452bd9a1a170dd2d34336d29d16f93844b` | 0 |
| lib/tracy/server/TracyTimelineItemThread.hpp | 2419 | `8a6ecaa8b119bf739cd72a81e42a4d79b5433206efd31b6dec0b83ef7bfc4de4` | 0 |
| lib/tracy/server/TracyUserData.cpp | 11334 | `651ffa721f6ea7696bbb7426124087be7d9bb47402308fcf0cae50a1d0d5fa44` | 0 |
| lib/tracy/server/TracyUserData.hpp | 1250 | `2d88186a97b254d4d62add9ee094722d10609708d4b870641101b81326b4abdb` | 0 |
| lib/tracy/server/TracyUtility.cpp | 4674 | `c4a3d4137840984d6533d96d822e8762f85bb3599ce638c03333a359c9f16937` | 0 |
| lib/tracy/server/TracyUtility.hpp | 811 | `212e98a90068f1c1ab0b272d3d88808bc61c1f046c23be7cd5aa0af303868972` | 0 |
| lib/tracy/server/TracyVarArray.hpp | 2320 | `3d446030bf6e0a60c93d3a983b451fc7ae853d3203fb42a363bd9649725c5d78` | 0 |
| lib/tracy/server/TracyVector.hpp | 9921 | `78dd3c7058b144b2ac4811a284b68ca551455f893bdbbbb44996c73546b0854d` | 0 |
| lib/tracy/server/TracyView.cpp | 48266 | `af11c0e935fadd9e3d94b4f26a6f9c9661eb5bdc80c499c94f990eefd692c664` | 0 |
| lib/tracy/server/TracyView.hpp | 30238 | `48f49fe6a3e03506fbe91b24f466f7f684fcf095a1d993647329ba61d9734ed8` | 0 |
| lib/tracy/server/TracyViewData.hpp | 1591 | `e4fbb15a20f033a2e4d016f622faede01f2605354ccff58b40a5ca14f9554b13` | 0 |
| lib/tracy/server/TracyView_Annotations.cpp | 5124 | `165e5c9394565cd70db230c3ff8e87f046e07034923d494f91dc2e24a18681fc` | 0 |
| lib/tracy/server/TracyView_Callstack.cpp | 18155 | `726874ab6b8539e1f37158f50f3decd889885da666d6e90772af7b14d9920b51` | 0 |
| lib/tracy/server/TracyView_Compare.cpp | 59456 | `3a61219fe436833eb6e0392f203c370c3e85f0b049cabbc928ec69f7ae2926cf` | 0 |
| lib/tracy/server/TracyView_ConnectionState.cpp | 8585 | `b4161e30e801570670d8687cc23dff1836a166937b558d227c3629d61f5d0539` | 0 |
| lib/tracy/server/TracyView_ContextSwitch.cpp | 23306 | `89d3ae5f56d628f27c59cdce3f6310f6dc12741f9eded4170de25c730b822257` | 0 |
| lib/tracy/server/TracyView_CpuData.cpp | 34286 | `f71093dac95080a3362fe4565596c93702099282f907a7c47157327060ffaa0a` | 0 |
| lib/tracy/server/TracyView_FindZone.cpp | 93890 | `fc741e489770d39df1a719e0f7f31afcadb4bd6a54a1181a265604b4a911c983` | 0 |
| lib/tracy/server/TracyView_FrameOverview.cpp | 20086 | `470e12a0fe20989053ab8d98d554a37b3865048dbbf7519be6c5cd00c5a96587` | 0 |
| lib/tracy/server/TracyView_FrameTimeline.cpp | 12459 | `a01cd0a89644eead9fea50025a3892878692067b1445a91489a193031831d80d` | 0 |
| lib/tracy/server/TracyView_FrameTree.cpp | 32728 | `4eca5192da4ae9773a128551f7e57169abb564bbe84686d2d2f72f55708fba9a` | 0 |
| lib/tracy/server/TracyView_GpuTimeline.cpp | 16124 | `2d6dbb13e6ff3de89db01512f98690356f0623b05299b39008a1b4b13bfd679a` | 0 |
| lib/tracy/server/TracyView_Locks.cpp | 29139 | `69233f5ed01332956df0f1a922978fa00089a6ddfcb5c19fb9dd68863c7b2e9d` | 0 |
| lib/tracy/server/TracyView_Memory.cpp | 37796 | `6d5884e5c411765769d6364855af4a4c26139ae37ecb1f7e344375a070cd2cba` | 0 |
| lib/tracy/server/TracyView_Messages.cpp | 10720 | `09ecfddbc53fb17ca48f9f91770ec866b9a7faaa1607960c666829af9b751d76` | 0 |
| lib/tracy/server/TracyView_Navigation.cpp | 3906 | `c3f28e3a36b2afafd6020d10bd941da4db1a1d23ca468eb8015d662cd4774d70` | 0 |
| lib/tracy/server/TracyView_NotificationArea.cpp | 8951 | `70fd9563703d1e797589e0670bc66e09f9b7d1d1b1f73f3a09f564b4463c0832` | 0 |
| lib/tracy/server/TracyView_Options.cpp | 29967 | `bb0529ebabc00e2e79859c8cf32a0995600eb6a5169e0932124e15f6a84677d1` | 0 |
| lib/tracy/server/TracyView_Playback.cpp | 6410 | `02121b29a104b7cf211162934539f6eb14139087406543b86bc9c0652863d6aa` | 0 |
| lib/tracy/server/TracyView_Plots.cpp | 14755 | `a8378339cdff4b78871fde5dfd5e0515606d659c0460d3efd2dca367c5a81325` | 0 |
| lib/tracy/server/TracyView_Ranges.cpp | 6448 | `a6e01df5389103fa9fad1ba67f417957fa2c2476acca269900f6a1f6c193a005` | 0 |
| lib/tracy/server/TracyView_Samples.cpp | 45825 | `23b236569820e741c4fa32775987299cd965a0bc935e85fd768c9674537a20cb` | 0 |
| lib/tracy/server/TracyView_Statistics.cpp | 39706 | `b494af0d2f4b33270ec10ca8e6abec5ffe0e972f78fd440b8378e9b6eee4e71d` | 0 |
| lib/tracy/server/TracyView_Timeline.cpp | 23307 | `ee27d998c7e2b8bf2fa476b71caf712587d17e7be96bc3ab6e2d4ea7687b362f` | 0 |
| lib/tracy/server/TracyView_TraceInfo.cpp | 45313 | `ed1ee1230ae5b3d3dcea51538398e340873482a82109145071621223eda6c722` | 0 |
| lib/tracy/server/TracyView_Utility.cpp | 31118 | `cbd8f84b3bbe00633332346d54db541f62a56b2e0d663f1160bb61b77d7059e9` | 0 |
| lib/tracy/server/TracyView_ZoneInfo.cpp | 80686 | `a836b9838e4b56038fb6e3bf3f08ff8a7708ff43a7ba05914a1747c6fe0be2af` | 0 |
| lib/tracy/server/TracyView_ZoneTimeline.cpp | 27618 | `f0a060b8302db8e6358f855c09af51ae121fe7d6eb11442d57d777599e332356` | 0 |
| lib/tracy/server/TracyWeb.cpp | 627 | `0ca2a3e36bfdb7f50dd357882879a9150f327804fff1c88ad9e2bf77b09b1080` | 0 |
| lib/tracy/server/TracyWeb.hpp | 118 | `579ae853209dd57a465e98e4d44d04744e897d49517a6915297380e45e3ce7fe` | 0 |
| lib/tracy/server/TracyWorker.cpp | 271219 | `464d6de0fe294519a9fe0c94e13b77e0ffaf38a29ce29cfcde056f7b6e19d253` | 0 |
| lib/tracy/server/TracyWorker.hpp | 49841 | `b1fc87200b4d9c7b7abc90e4fd4ab4e619b387eb02e32969f2a2f3ff4fe1e821` | 0 |
| lib/tracy/server/tracy_pdqsort.h | 22673 | `9f9267ed96c04c9ee58fc8a0e2f3ce76e5431127c1fe13bb7d3ac19645fbe1e7` | 0 |
| lib/tracy/server/tracy_robin_hood.h | 94668 | `b341cbc928ae25fa36cbc8feb642d3b9c5b06c2ec6731c66858424b61a20a862` | 0 |
| lib/tracy/server/tracy_xxhash.h | 253096 | `be275e9db21a503c37f24683cdb4908f2370a3e35ab96e02c4ea73dc8e399c43` | 0 |
| lib/tracy/update/src/update.cpp | 6733 | `02a2467374283d93b1d7413b96465dc73c398c91bdcbb6466b29a766a7a73c0c` | 0 |
| lib/tracy/zstd/common/allocations.h | 1632 | `c1c971ac240e7709e0da2a0a1b249c9bf68f138d41c9f76ab1f0d31118560ef8` | 0 |
| lib/tracy/zstd/common/bits.h | 6226 | `84447179d20e90fcb7ace6358ad79c1e1b978bc86f68568529ed24ca1777b49e` | 0 |
| lib/tracy/zstd/common/bitstream.h | 17522 | `0a3303e7860609c72d4e83eb254b8144b8242c14c4b837fea3d6ae6d1d426db7` | 0 |
| lib/tracy/zstd/common/compiler.h | 13012 | `bf3a8e4ca4b4eac823433cc1d3f637d036f1d6234fa7ffc236c8745f8c4a61f2` | 0 |
| lib/tracy/zstd/common/cpu.h | 4466 | `216681cb15aca5d63afb9b994512bcaf66f71ee02c7789248f26f1d3f7183e26` | 0 |
| lib/tracy/zstd/common/debug.c | 843 | `77083a66b80b7a677875adb765b581d800a934a87d29c0955410c6c027cd0f35` | 0 |
| lib/tracy/zstd/common/debug.h | 3761 | `79ff0630cfef960e5c1e4752c77b880306f41bff6c90f6a638da84e6e288cb9d` | 0 |
| lib/tracy/zstd/common/entropy_common.c | 13308 | `7dfce29c6bc807645b1f0c373dad94bbb49603b175a84e72d1739bf9df65feb8` | 0 |
| lib/tracy/zstd/common/error_private.c | 3797 | `749261716f8628275149880d88c8862207d2f7a550a4f84ef37710abb78a3bcc` | 0 |
| lib/tracy/zstd/common/error_private.h | 4876 | `d6dbf7bf651c0a40e0b92e7e56958c13cc772abd7e818fac1e85777e1f2ae853` | 0 |
| lib/tracy/zstd/common/fse.h | 30110 | `a4fc84da1392b7cb74d38e2a0b2e253fb663425039ff5651472cb51b9e8f12f5` | 0 |
| lib/tracy/zstd/common/fse_decompress.c | 12152 | `ca2a15f45fe0e87008775bbad1e787fea4f347740393eddf44ccd6070dce12b9` | 0 |
| lib/tracy/zstd/common/huf.h | 13808 | `4acc5a57ac61b3a549418f23605691f73744983accab8690ad35c3aae967a359` | 0 |
| lib/tracy/zstd/common/mem.h | 13278 | `bb9caee6a6de5b58d0fac7492d6df06c881b6d87b580c03224df5e29a795ef7a` | 0 |
| lib/tracy/zstd/common/pool.c | 11779 | `a0b36a9e700dfb5c67e309f5c4e634be84dce057bc51210b89676fd9d7c88989` | 0 |
| lib/tracy/zstd/common/pool.h | 2654 | `2fc00f45a21f01ce764b14287d23d527c32903101e6ed5219152b5d7ff3d6f38` | 0 |
| lib/tracy/zstd/common/portability_macros.h | 4403 | `3923b88fb6e973a6b1e944103abfb152fe5d95a795596cf37857f5f2df461d01` | 0 |
| lib/tracy/zstd/common/threading.c | 4740 | `4c6401b7501d3318f2ce2f094e72a2af37677df665e7d6bf922a817d577ecdb9` | 0 |
| lib/tracy/zstd/common/threading.h | 5195 | `05ca16720ca4686998d599088654fc98673451b5691a500cb9dc163b26c8fe32` | 0 |
| lib/tracy/zstd/common/xxhash.c | 767 | `ec39d4b0d383dc547ad6a8b1e66f66fa7fc085f8d6c9bf9747882b3e48f84b06` | 0 |
| lib/tracy/zstd/common/xxhash.h | 212896 | `d63803315e16fe11f9985a9bc5988449f97f729098337c4c154ef31fe58dbe31` | 0 |
| lib/tracy/zstd/common/zstd_common.c | 1683 | `f49eb8023a90d3de925373bd9ee0d36ed46b26c529840b64220397446cd73795` | 0 |
| lib/tracy/zstd/common/zstd_deps.h | 2508 | `6b57771c66247b2e5f15cf5e9a781128f885b33a0023d93f5822e67626962816` | 0 |
| lib/tracy/zstd/common/zstd_internal.h | 13342 | `cf31355503a0f7c4a1fe50f92c75e4e6029a7874bb1686d6fc626d9645a4d4bb` | 0 |
| lib/tracy/zstd/common/zstd_trace.h | 4619 | `eb1251bbb9091edb00b96987236b50bc11fb707807de3a83337f53fd6e231728` | 0 |
| lib/tracy/zstd/compress/clevels.h | 6860 | `d764daa89b7a636d26fe96ff3536c5075e9867fb5dddbf8c9d57023a8ff4a155` | 0 |
| lib/tracy/zstd/compress/fse_compress.c | 24096 | `6bc37877000072b4dcfb7ecc0486a33c0ce8e513fac7e5cdc0e0ab829ffdacdb` | 0 |
| lib/tracy/zstd/compress/hist.c | 7448 | `154e5efd4f3cf8a4e6f29db6463fd3aa4e3694ae9b9c73e5c275a6cb1e3fefe1` | 0 |
| lib/tracy/zstd/compress/hist.h | 3448 | `8dd30d7687fe59f8a3a5188dd36911bc1cf1211839e8c49afa1df8a8678fcada` | 0 |
| lib/tracy/zstd/compress/huf_compress.c | 57710 | `a00a8a4f90b6dd42ef7733d4481d7e5793f674e574af5a854e256db683ee88f6` | 0 |
| lib/tracy/zstd/compress/zstd_compress.c | 312776 | `298f4c03c87dc1c8443dc1d3ec24668d3834d8146c9c366bfb442836489245fe` | 0 |
| lib/tracy/zstd/compress/zstd_compress_internal.h | 64416 | `e006bd17a75790314e1d5e78cc3dbd00fce8442fa6d50e19eaeeeeaa88cfa03d` | 0 |
| lib/tracy/zstd/compress/zstd_compress_literals.c | 9155 | `c38586b65c69a1906e750bea5a49785b3502b1f52698eee597a4d037b2d9080f` | 0 |
| lib/tracy/zstd/compress/zstd_compress_literals.h | 1613 | `02270cd6bc060279217861776a53adb67f8d7e54f47f59d2a4ddcef2e705fe2d` | 0 |
| lib/tracy/zstd/compress/zstd_compress_sequences.c | 20004 | `b3685e8b987944206c9d92e5d3c773b73c1c03f4fbb970d8e62f0d6de2b16010` | 0 |
| lib/tracy/zstd/compress/zstd_compress_sequences.h | 2175 | `a119b546cc28baed798c3da181861500487229b61c379380b600adf41eb8f21e` | 0 |
| lib/tracy/zstd/compress/zstd_compress_superblock.c | 28499 | `7ec66723e2e806adaca3e718ca2743b04426d742581aa3761d8a600e77e58570` | 0 |
| lib/tracy/zstd/compress/zstd_compress_superblock.h | 1168 | `6b097999ea1d91776ca5a12e5ee02c1ed15edfcd31ba07b9ada94b0955195677` | 0 |
| lib/tracy/zstd/compress/zstd_cwksp.h | 27872 | `dbdcc18c52f7596511c4fcd609bddea88757aa2b1219e2502ab082bcbfa3e2be` | 0 |
| lib/tracy/zstd/compress/zstd_double_fast.c | 34479 | `46861b3ce7386c6105f7a007f0798e0f3897231dabadaa4a54142469b5144b5f` | 0 |
| lib/tracy/zstd/compress/zstd_double_fast.h | 1347 | `6efa67eb99d579d0b822bfba7954e641db3c116e3487dfc613c30bf75a7757da` | 0 |
| lib/tracy/zstd/compress/zstd_fast.c | 36950 | `95b0d5c110dff0d94a750615d9bcc3cd4a2b54b95e0064343d97a314ef991034` | 0 |
| lib/tracy/zstd/compress/zstd_fast.h | 1261 | `a40a5e53ecc259bb8e05bc6a81980de26b4f1bae41fe6c2df53b6d1d39a325a4` | 0 |
| lib/tracy/zstd/compress/zstd_lazy.c | 101952 | `70f13cfaa7d6567c984ba03b610df20c261e96a147f496611b5ab22db508abad` | 0 |
| lib/tracy/zstd/compress/zstd_lazy.h | 5722 | `62677ac5d95cec9f4ad16cdef862c9be79287b51ab676a8709e9964759b9ca05` | 0 |
| lib/tracy/zstd/compress/zstd_ldm.c | 28437 | `17169daefb742174d11a90a7ae484ba6840b26af2b7613b2053907cd84634fcc` | 0 |
| lib/tracy/zstd/compress/zstd_ldm.h | 4448 | `f06522debac7eb19b97bb0fa531f209cd06bd42a8636bb6139454923980125b5` | 0 |
| lib/tracy/zstd/compress/zstd_ldm_geartab.h | 6077 | `7285ac8ba1f0fa57a8cd8158bd427ded4e70e32a58e73b57c420b83a76e5e6e3` | 0 |
| lib/tracy/zstd/compress/zstd_opt.c | 67459 | `fabd179d004d3b99808a56d78acd6d772ee4759cbf945fb4a16164f10fd6620b` | 0 |
| lib/tracy/zstd/compress/zstd_opt.h | 2011 | `c7ffddfdc38a2a6f8be38d3074492a46d5f3fe03783ebda67a300f68596c1ee4` | 0 |
| lib/tracy/zstd/compress/zstdmt_compress.c | 81334 | `246c2cfb2367c46fbae3608b8e7b86243a33069b64130a5b7439d4be1046ff26` | 0 |
| lib/tracy/zstd/compress/zstdmt_compress.h | 4663 | `43838192752506a16afc054ec83580995d0cab4a53ef245720f5241ac1289b75` | 0 |
| lib/tracy/zstd/decompress/huf_decompress.c | 73701 | `7c0d521904d99733ea0d68685f91e14318186063ec2859e50f2155a58ba773d3` | 0 |
| lib/tracy/zstd/decompress/zstd_ddict.c | 9182 | `38bf812283d61f4cd1f6aea30f84b43317418257c4e6fc198b09b436bd484397` | 0 |
| lib/tracy/zstd/decompress/zstd_ddict.h | 1319 | `a97a250fd2f956e3ae419ddde68ae1f9fe4025bc0373254058d31bbd352fa71c` | 0 |
| lib/tracy/zstd/decompress/zstd_decompress.c | 99701 | `0645e788c5d1aa5f125e4c6993e0d8ca2f4cf276bdf9715f73873b975198c164` | 0 |
| lib/tracy/zstd/decompress/zstd_decompress_block.c | 99641 | `322603f4e778385cae939c32229767ceed455da217e75c90594de7c92d4e888a` | 0 |
| lib/tracy/zstd/decompress/zstd_decompress_block.h | 2699 | `a8116d6266eef14d5928731349cc9e6ab8ad3f022046968fc93e615aa34195dd` | 0 |
| lib/tracy/zstd/decompress/zstd_decompress_internal.h | 9630 | `e01c336c8ee233262711ef7732103413509406c55f7f26443a21d9468a692090` | 0 |
| lib/tracy/zstd/dictBuilder/cover.c | 42898 | `c1758516a628f24406e95f62f2275ed6f82b3927440ecc4352cd16e49ffdc900` | 0 |
| lib/tracy/zstd/dictBuilder/cover.h | 5026 | `17f9a62c0fe8d495700ba3073989aaa05dcb6a59a1a749b7bbb707dbc191890c` | 0 |
| lib/tracy/zstd/dictBuilder/divsufsort.c | 54649 | `2081acb08865f623857d2c0dcb0e79fce9489f01416528c30cfee7097915c616` | 0 |
| lib/tracy/zstd/dictBuilder/divsufsort.h | 2419 | `f8312544f98feb695e611c68d5191b5ae5302e01a3613e2a6f8e6cd365dd3b2d` | 0 |
| lib/tracy/zstd/dictBuilder/fastcover.c | 28561 | `937862174e9b76d01b3798dc08ae7f6a893fa42821a80742dc0eaea97f3494fc` | 0 |
| lib/tracy/zstd/dictBuilder/zdict.c | 44008 | `46abb11a97f5b52688e408c3496b1e702c22a191087663c311eba4050cce6896` | 0 |
| lib/tracy/zstd/zdict.h | 26433 | `02a34169467501fcc665cccb33f5bd455fdb665e9806851777dc8a6c4d5a75e3` | 0 |
| lib/tracy/zstd/zstd.h | 171378 | `41d0f43747d0dee56f60bd10aed262f193d725b7e11eb9e94aa4ad80183c7da8` | 0 |
| lib/tracy/zstd/zstd_errors.h | 4532 | `36dbd0a595852e10ff5b52992294f610055b8781101f4634036e05cf7d4bb506` | 0 |
| lib/xdrpp/compat/getopt.h | 2703 | `9c9d2d0161b7c6ab6ecb753a4a82c0aa7f151525791ea7f0bb5926689aa5501d` | 0 |
| lib/xdrpp/compat/getopt_long.c | 14854 | `228c4787e7b10abf81a38b6f84d05a2f63d23be0042d5f2f6d44f572e31c98ba` | 0 |
| lib/xdrpp/msvc_xdrpp/include/xdrpp/config.h | 137 | `d91760203b77a31336f1a9c286f178c5effdb13910de23a1e3eb60e24b4dcdb2` | 0 |
| lib/xdrpp/xdrc/gen_hh.cc | 25659 | `de047470af6a05262e58a0199317e2e4272e5e5194f06cd60c331c3c9bfe338b` | 0 |
| lib/xdrpp/xdrc/gen_server.cc | 3540 | `f3f270180eacfa48bd52a1539e4af7e86399b40caf494bb965f036b8818f27c0` | 0 |
| lib/xdrpp/xdrc/union.h | 8858 | `4d9e1fb047b61e539ecf6d50d8b43fecab32f1d14031377a33bf05ca07a977d4` | 0 |
| lib/xdrpp/xdrc/xdrc.cc | 5971 | `0756ee2f1d5329c44bb21056c539f8ffcd5e6f53ae450ea5fa4cae2c833b6162` | 0 |
| lib/xdrpp/xdrc/xdrc_internal.h | 6360 | `9c0f7e54dc85057048b734ab92ad2309b7a7d6377e79ef5266c1213dc7ffa246` | 0 |
| lib/xdrpp/xdrpp/arpc.cc | 162 | `c9b3311ca4262d3a81d744fcc8227d8f29a07ff58ac0dd9c30d6e626b3ddc99d` | 0 |
| lib/xdrpp/xdrpp/arpc.h | 6537 | `4cd6ddce84652613b0887bfa389556f6d6f0c6d72a127cf2b1542210907340e1` | 0 |
| lib/xdrpp/xdrpp/autocheck.h | 5860 | `5be264b8114d569ee4d87e4659865820fbbe58182c7c1f3abbe3f61dd47b8297` | 0 |
| lib/xdrpp/xdrpp/cereal.h | 5040 | `8647dd11524b125b1aaf59a145a1a1f012ecc2bdc90f9f676f2932b7e508d487` | 0 |
| lib/xdrpp/xdrpp/clear.h | 1721 | `67777705479dfd8e5ada8cf249cb7f2b7980ff0ec6e47044fba8fcf3259e3cd0` | 0 |
| lib/xdrpp/xdrpp/depth_checker.h | 2043 | `76636ed5fa08e013e945335b69580f79599cdd4fbddc070eb52c1c977a8637fa` | 0 |
| lib/xdrpp/xdrpp/endian.h | 2190 | `5b803cc5b23628324d8a99f17f2258aa8a79c6a2ba8d7c3399c3108059c94233` | 0 |
| lib/xdrpp/xdrpp/exception.h | 2376 | `f40d46827b6eae1a97ef60e30156021645648975487e228c1b19688bb94584ec` | 0 |
| lib/xdrpp/xdrpp/iniparse.cc | 5124 | `fabe5ab56335fed56e2d5c555b1f760a895a3add42987b47d8aeed99a09676c3` | 0 |
| lib/xdrpp/xdrpp/iniparse.h | 4048 | `ae14bcef1d2e3c684a5e0a3ce17f27bdce5c037c9a08fec4a9de88bb58dbf296` | 0 |
| lib/xdrpp/xdrpp/marshal.cc | 1808 | `62403727eb70e2fb2293fd56e3f8d04850724f6f2579c837f5a719630124cb7c` | 0 |
| lib/xdrpp/xdrpp/marshal.h | 10061 | `d7921a5648260b55550e6cb24303cfe2ce733d163af3228a7e256f351c6e8419` | 0 |
| lib/xdrpp/xdrpp/message.h | 2128 | `9af03af1f66104459b5f101c9e4adfcde112f8c622b51ab1c149719a148c60b8` | 0 |
| lib/xdrpp/xdrpp/msgsock.cc | 5096 | `aa75d32dc1c7bd1c714899fa4d45af9ecb414770afe0d3b749cba4f87ad07aec` | 0 |
| lib/xdrpp/xdrpp/msgsock.h | 4514 | `c98d6c5715e2284a2a55a16ca16f8b47d02d23997439ea5be2e4ab3b606e827a` | 0 |
| lib/xdrpp/xdrpp/pollset.cc | 10086 | `c957ac4e312cb48abb0d708eb68fd85daf4181fcb6076b20e22235ec76bd7c35` | 0 |
| lib/xdrpp/xdrpp/pollset.h | 10277 | `eb5b4b637f38613699f00f4de8e3f62f6ca379bc4dc85070dbd52f0d204efa2f` | 0 |
| lib/xdrpp/xdrpp/printer.cc | 1216 | `95a129c14302c754220ae3cac3b4bd40930e3cc615f744d8a345b4296e4ac2ca` | 0 |
| lib/xdrpp/xdrpp/printer.h | 5267 | `0b4d55dbd6a4463adc0c1a364331023e839645ea19e7530a295a1cc67277f422` | 0 |
| lib/xdrpp/xdrpp/rpc_msg.cc | 3366 | `f116e640bcb631bdc59d16c89561c4366bf79236189436f0727beed9e64bd3fd` | 0 |
| lib/xdrpp/xdrpp/rpcbind.cc | 5127 | `f500b58f44b23f358e4ae916da7badd6a5029dde1dbf12fc680368eb60e04e1b` | 0 |
| lib/xdrpp/xdrpp/rpcbind.h | 1242 | `be3988b10c8ca88c9341cabc16d3cfcf4a0ec0a5458a7fc4f6157037ba2622c5` | 0 |
| lib/xdrpp/xdrpp/server.cc | 3710 | `dc338c8acf347c426400fad94e90cba29771bcc4207cce5764cf79afc9357741` | 0 |
| lib/xdrpp/xdrpp/server.h | 9309 | `a55035c40bc5a632218e41600641adb458fc1d433bd79ffa04fccda4949ec102` | 0 |
| lib/xdrpp/xdrpp/socket.cc | 4581 | `9691d128745d071ca941f9c6a5dd608e8a100a51ecb55a83a69a599c27402165` | 0 |
| lib/xdrpp/xdrpp/socket.h | 5804 | `8602dedf1043d14867ab3a7473f399bc3912c9b68fe588c718d13fa55a095502` | 0 |
| lib/xdrpp/xdrpp/socket_unix.cc | 1664 | `5ec500aaf8dad4316f6785bfff38a42b63dd717d06db63614b2a3546d6bfd4c5` | 0 |
| lib/xdrpp/xdrpp/socket_windows.cc | 1878 | `4d58c05fd79cc5497c9b624bbf95f8d62dcfc4f41f6c24f34b04aff265c98e67` | 0 |
| lib/xdrpp/xdrpp/srpc.cc | 2002 | `0e08db82d78f1740d1063561d15ac6719d4d1dc3a79b462354784f31af504dd2` | 0 |
| lib/xdrpp/xdrpp/srpc.h | 5814 | `b51b9aa96d342ecce438ca46881692781f7f7356c36d483dadd5457894fbf484` | 0 |
| lib/xdrpp/xdrpp/types.h | 37097 | `4abf52222441b973c11dc2320da95b92a828c0cbc7dde9952178eebe827e36a1` | 0 |
| src/protocol-curr/xdr/.scripts/check-scspectype-superset.ts | 1652 | `30c4a2203b012e77d9cdcbf7b167c0381e8e0fe3f27eabb7286da26f410b0283` | 0 |
| src/rust/soroban/p21/.cargo/config.toml | 6711 | `b851d8821ee87ed933a3445bc9540231800afc8ce62e472e51a7af78b732930b` | 0 |
| src/rust/soroban/p21/Cargo.lock | 51958 | `2ad340fe76d63cd98f40f03c2626648b521ee8a38ad4746de3c88cb7695876bc` | 0 |
| src/rust/soroban/p21/Cargo.toml | 1896 | `1928c6a1ee45b09b46e9ec39cba8e611b2d572a61730a5448d0d577a27d7617b` | 0 |
| src/rust/soroban/p21/rust-toolchain.toml | 133 | `dd1e82393723dd0546770d2e0fd9b64baab923e2cdba735bdff577a34a791081` | 0 |
| src/rust/soroban/p21/soroban-bench-utils/Cargo.toml | 537 | `93988108ed3bea71358854bb28ad288013e9874d519c7ed41e4b0a8474cc9a0d` | 0 |
| src/rust/soroban/p21/soroban-bench-utils/src/lib.rs | 75 | `4ed9af88c90c8137a175e9b2e583a3076ef13bc4911e133e889aa6f559caeeab` | 0 |
| src/rust/soroban/p21/soroban-bench-utils/src/rusagev4.rs | 2027 | `e775f766b27fcece33febfaf91e1b2e46b4ff0d7028a326909fd910dd75c7b17` | 0 |
| src/rust/soroban/p21/soroban-bench-utils/src/tracker.rs | 5779 | `e74a81521adf897e59bfda013cfd74d9a0020b7262fb0379c4d9c124befedd54` | 0 |
| src/rust/soroban/p21/soroban-builtin-sdk-macros/Cargo.toml | 554 | `e1d1972e42e800ebea10f231b70d84999456cf99cca06b8bd371c5299e33cf2a` | 0 |
| src/rust/soroban/p21/soroban-builtin-sdk-macros/src/derive_fn.rs | 2815 | `627430878da696e94b872adc29d71390e866277ee7acf6c1b42e7cdd2ccf15a0` | 0 |
| src/rust/soroban/p21/soroban-builtin-sdk-macros/src/derive_type.rs | 8525 | `459416267127d646b9d105c16c046b210eeb22cd4c482511f268d8396120f215` | 0 |
| src/rust/soroban/p21/soroban-builtin-sdk-macros/src/lib.rs | 1734 | `7120a6c227f456234536bfef7c7f9d82918a8c89d8c25f3f16eaccc404a79aad` | 0 |
| src/rust/soroban/p21/soroban-env-common/Cargo.toml | 1564 | `13e8c1d44c2be115856ab715d280963f05c4fc0a9d9247d6ea6b7ce002c2e018` | 0 |
| src/rust/soroban/p21/soroban-env-common/build.rs | 99 | `818b5844721186dd913412974faaff4bb45954e41b2cedeecb4b0a5ddcf90b35` | 0 |
| src/rust/soroban/p21/soroban-env-common/src/arbitrary.rs | 2047 | `aaebd099ab97097e1ac2482ac4c437c99736f75ca822cfdcec435ccf8b8fb662` | 0 |
| src/rust/soroban/p21/soroban-env-common/src/bytes.rs | 3066 | `768838872830e2352670e97ad9d9313c24db0efb8854847474739ed33c7c5735` | 0 |
| src/rust/soroban/p21/soroban-env-common/src/compare.rs | 7453 | `6f02fb0afd08619f9566de017a510a5f7fb0202d4d5c589cf9f03dc7634d090d` | 0 |
| src/rust/soroban/p21/soroban-env-common/src/convert.rs | 18162 | `4d953a32ac45849c3a86b02d7fddea462c0ff9b74f289a0b4f43990dfb023352` | 0 |
| src/rust/soroban/p21/soroban-env-common/src/env.rs | 17907 | `30d4f9ada846516cef746a12ba36e700d260d43a18cd73d4b5cd619e9cf8da10` | 0 |
| src/rust/soroban/p21/soroban-env-common/src/error.rs | 15600 | `efd9f516f411d55dd01a22e33f3418068d82c715290382e98a5cba4f58bdc46e` | 0 |
| src/rust/soroban/p21/soroban-env-common/src/hash.rs | 1437 | `efb8351b71469d22beca2e1b2f2b65a9e18db9d82a04a60b79d7126979fca09b` | 0 |
| src/rust/soroban/p21/soroban-env-common/src/lib.rs | 4108 | `f8e7db3a7a5b1d236e46e9a4305bbf5eb2e3519e6bf5ebaea4f6079b71685c7a` | 0 |
| src/rust/soroban/p21/soroban-env-common/src/meta.rs | 3741 | `b8f95fe3432a220a487e059be0d6725948025ed593055b4626a1538d8d4a1c59` | 0 |
| src/rust/soroban/p21/soroban-env-common/src/num.rs | 14177 | `998194bffbd3c4949612605f097cd83bc67100acef169bbc5f1c6c1ead1432f7` | 0 |
| src/rust/soroban/p21/soroban-env-common/src/object.rs | 5974 | `055ee181559ba02962d8837461b8e9e81e6b7bf37cf3b0c1a6e99a4857c3aaf9` | 0 |
| src/rust/soroban/p21/soroban-env-common/src/option.rs | 673 | `d2efd530d62aa4b5d772cccbd7a8762171250b42a5c9ba16e390412cf35b4620` | 0 |
| src/rust/soroban/p21/soroban-env-common/src/result.rs | 1261 | `d3210db790113cf7950e76c15492358ca9a469159f8dee2c27c2dee91228c4b0` | 0 |
| src/rust/soroban/p21/soroban-env-common/src/storage_type.rs | 1076 | `f3dcf69433e9c8a2d1b1f3e3202955d87abb2ba9fe365f70629a402c30a56641` | 0 |
| src/rust/soroban/p21/soroban-env-common/src/string.rs | 2036 | `13ec3079a2f66e4affb3ecdeba15134f2941ef05076f544a195736dbd64bf8e9` | 0 |
| src/rust/soroban/p21/soroban-env-common/src/symbol.rs | 21414 | `39d94bce62166c231fc9904648384dcf94255332bca376a17bf986b5780b13d2` | 0 |
| src/rust/soroban/p21/soroban-env-common/src/tuple.rs | 3967 | `951cd7990e7feff06c030bfcf40ff439e2db8049224075d60fc21ed97d9af8b8` | 0 |
| src/rust/soroban/p21/soroban-env-common/src/val.rs | 30394 | `fe05f6e9b63fa05c40ff45f80c8bddf10cfb19888766d6d046b770d962eee816` | 0 |
| src/rust/soroban/p21/soroban-env-common/src/vmcaller_env.rs | 11519 | `74a5c41dbefeea05df0bae94274fb23302931a2f3eb6305382c9cd1c33cfc482` | 0 |
| src/rust/soroban/p21/soroban-env-common/src/wrapper_macros.rs | 11834 | `35eb9af1dd3fa232c0d18bb1993d9f2b303893ae6668c30e966afffd4b39a05b` | 0 |
| src/rust/soroban/p21/soroban-env-guest/Cargo.toml | 625 | `65d7195e1ef69e1cba7c6aabd96072fe37482f0b1c7ecaeb17e17cc38b2ab937` | 0 |
| src/rust/soroban/p21/soroban-env-guest/src/guest.rs | 15204 | `510b8fce90a317d8eb8622c38169663d1dd3a324b757b91b6aa2370cac4f5653` | 0 |
| src/rust/soroban/p21/soroban-env-guest/src/lib.rs | 561 | `b34cdc92dbf3880bd463d0c82b7df5866ac88d74b8bc42d8a9321eb9104dcfdf` | 0 |
| src/rust/soroban/p21/soroban-env-host/Cargo.toml | 5919 | `651d279c31a2316cd4722b26cda19cceeb2b816eb362557a64920992223a23c4` | 0 |
| src/rust/soroban/p21/soroban-env-host/build.rs | 226 | `8910e245e436fe32da52e569e3679576852bbe8fd40190748798284bf589b4a0` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/auth.rs | 95772 | `0f834f23efb523ad7270b8acd52d366c156b9f4ab46540d6bf84571c4fe9de27` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/bin/main.rs | 1403 | `aae7d92a9c7a40e441e38d8a5767eae368e3dc89c869a2f297c3be42683c883f` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/budget.rs | 43151 | `fe56f0191e9bdfdda8cc4b05ca4abe6a98e87842c7c3b161e5821f2da0a8447f` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/budget/dimension.rs | 6675 | `9fa79e2d272a2d2596536a2140fb77a8e4abe3ef2950e06fc966f0b62b72e981` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/budget/limits.rs | 4658 | `0080964f53ec49d2df64306354887cc5565b2628584e64548126a4b95e2eca1e` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/budget/model.rs | 4434 | `5513accbc3b5698c8f03d042b0b1d92a30cfd11657677f5f5cd94c20c72a6f78` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/budget/util.rs | 7104 | `77f7128a74a74a2da8fb994e87433848dae4bfd82059e32235781cab98f31d48` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/budget/wasmi_helper.rs | 4145 | `c7afc9c4c05a9ee57d0da858369312d9d0ba431bc337d02b98d750cfb4fbe0d0` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/builtin_contracts.rs | 560 | `f0bd26290068aff0d567b8e950c3abd9545b9f6fbb50a521001e21f9b3a7ed1e` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/builtin_contracts/account_contract.rs | 8194 | `eac81e1a253b6ae85391dcc5cb1f9aa06c7358f5aa6851c2fba33a037a76c8d1` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/builtin_contracts/base_types.rs | 9665 | `fd0545f90fa279369e72219b7873cc22e15e32b9fd6578fc7dde19d8bfa48e2b` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/builtin_contracts/common_types.rs | 657 | `21c7d8c3cd943a3384ec5c9545f912fd0f1ba2c2a6fa3f99afb071aec7d43d9d` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/builtin_contracts/contract_error.rs | 881 | `bf6a304eb50eac03bc3cf2a21fcfcd58cf0501b698a721c575b034f389b76d2a` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/builtin_contracts/invoker_contract_auth.rs | 4744 | `8d2cbabb37fa04506fa19f6a8ef641f820711f9397075db29a5c88daf8f5a964` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/builtin_contracts/stellar_asset_contract.rs | 248 | `944142447b113d671f1e47dc8a2d8191ef4ff11167b793f2a4c2f4d72efc8e4f` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/builtin_contracts/stellar_asset_contract/admin.rs | 704 | `ad70748dab976704bdf5fa87dfe30c0746280a24eb46c36a9c102aeb1f11980d` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/builtin_contracts/stellar_asset_contract/allowance.rs | 5086 | `6ea9c9360181cd73eaa569c5be0ae95301d56e5ce33aa06bb26b821d3eb56ce8` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/builtin_contracts/stellar_asset_contract/asset_info.rs | 3092 | `9a0583a6bec016f2822bc357baa2cce81c8e4ad3077fd8d5e2100172c0b22def` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/builtin_contracts/stellar_asset_contract/balance.rs | 28306 | `930595374eaff715e17b47aa2ddb0f4acf43b02330962b72ce60199b334d5e1d` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/builtin_contracts/stellar_asset_contract/contract.rs | 13008 | `c7234e92b6d31b00a16e454f57432ad9f2b1d61666a61ed1d150fa475f62feb8` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/builtin_contracts/stellar_asset_contract/event.rs | 2488 | `5fe7009aabbe3d29676bb0c8e5541163e5774a53f8967a70a79ae2cc24a67cd2` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/builtin_contracts/stellar_asset_contract/metadata.rs | 6992 | `12ca5219bd19e98b81880a01e5fe99bfffaf1c5d283371bff34961763ac00331` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/builtin_contracts/stellar_asset_contract/public_types.rs | 1318 | `84834c2fec3c9763ba73d89fdd44db86da9a35400e82401cd5ba04ed03874026` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/builtin_contracts/stellar_asset_contract/storage_types.rs | 1113 | `655a0cec594b78db2eeccabfe03e27f2ae0537c65729e456b604cbbdb579f298` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/builtin_contracts/storage_utils.rs | 362 | `216d16572291ac021fd3ee7a0ce6d4b1810f8dbee07fc2791bbf32236a75ed10` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/builtin_contracts/testutils.rs | 11060 | `d72eace5611ec5988f3a32a06ab52e8085823b3503b7f94d03def35d39795b74` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/cost_runner/cost_types/compute_ed25519_pubkey.rs | 952 | `c679365a8825299630452cf28daf21f4e6cff1805ca06910bc4ce49300d04a7c` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/cost_runner/cost_types/compute_keccak256_hash.rs | 916 | `c70f481dcea5eba30a4ae54ea476efec3fb3bf938d15987042aaeac222bbef3d` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/cost_runner/cost_types/compute_sha256_hash.rs | 902 | `5ef3a4dc6cbe4050c2b5d88e4bb438d948d21339ca57ab3fa9738285ea86d185` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/cost_runner/cost_types/decode_ecdsa_curve256_sig.rs | 1407 | `6eae776ff6b8ee070b6d51f70a4b231bf78c2bd0e964c0cae695be06a66b251e` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/cost_runner/cost_types/host_mem_alloc.rs | 951 | `53bd536e402308f09e0ead2a7825d8a7a88c6da46f0deb55ddce336d6a754a32` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/cost_runner/cost_types/host_mem_cmp.rs | 957 | `db2b390ce0892f2b450a9707d8f3d54a9fe2438d88f73ae021263dc18b266a3c` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/cost_runner/cost_types/host_mem_cpy.rs | 821 | `7ab8627489d5882ca2725d3e5872dc5cf3907890341065e5fa9149b121f11316` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/cost_runner/cost_types/invoke.rs | 2040 | `df0598b3e358e7b4a46f5d7f58caa6d08d19e9994afbc828de39759ebc0b56cc` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/cost_runner/cost_types/mod.rs | 946 | `a6f316e2befdaa4db531f8063f5e1e3ee6b6288032a0c929164d0a0bbd534600` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/cost_runner/cost_types/num_ops.rs | 1546 | `cf08647785a4ede49183258e305e4520b3db286536bf2a6e71583e76c89be32b` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/cost_runner/cost_types/prng.rs | 1009 | `bb034da3c3704cd2b2fd13d02e55d7edd3e1113ff189039812b03650170c178f` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/cost_runner/cost_types/recover_ecdsa_secp256k1_key.rs | 1140 | `21256191032a43cd2584275eebae7e034db553ee6c90c16d6ba5e5e2392eb69a` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/cost_runner/cost_types/sec1_decode_point_uncompressed.rs | 1155 | `06fda4cc5f09ca513953f45424b1aa5277fb1fa0805e598e63466ea6b45d1863` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/cost_runner/cost_types/val_deser.rs | 800 | `19b4abd59908d36bc2c1a2d7e05fc67db21df215cf02bcf91ff42d760f18e6d0` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/cost_runner/cost_types/val_ser.rs | 1385 | `2b3aa6b23feb1d99fdfc267146458eba577e8641124c8673a606fa0cb976b08e` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/cost_runner/cost_types/verify_ecdsa_secp256r1_sig.rs | 1124 | `8b1e249924c8f329e563122f8e2c1d0e60fbc6c788de70c0dd4e9aeaf8f8b833` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/cost_runner/cost_types/verify_ed25519_sig.rs | 1079 | `da86df368d3cdc769f57e48a6fd160ba5c7f1dab0a44876587875be1167215bc` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/cost_runner/cost_types/visit_object.rs | 1056 | `c66e1ae7580a923564f8694f34d3ee9ff4c3de2b768529cf75a9f86e23c9c656` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/cost_runner/cost_types/vm_ops.rs | 8434 | `1f77d6fc6ff198a85d1871352c92d3eb85ae952d07f496cba0c4b42c7c23cad4` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/cost_runner/cost_types/wasm_insn_exec.rs | 9536 | `87db0f3d05e23d612549c9aad6f2d4565ffa2476ca3c0503c82efdc139d3256b` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/cost_runner/experimental/decode_secp256r1_sig.rs | 1444 | `d7bb6de22a5ad5872390289ab6e289162f1eb4f672b212e167fdf80f42d2ef74` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/cost_runner/experimental/ecdsa_secp256k1_verify.rs | 1459 | `3595d51b531d9285d4685233f240282144308229e647f2aeefe9d0eef99d8f4d` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/cost_runner/experimental/ecdsa_secp256r1_recover.rs | 1471 | `4e292e0dc316b81bfa206e6158cc898e4126e8a85a1ca4d948840685c525dea3` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/cost_runner/experimental/ed25519_scalar_mut.rs | 1325 | `8ef1a776485ad7ec1bc9d833744c7bcf5860c44f2291397a9d983f5cd1a720dd` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/cost_runner/experimental/map_ops.rs | 1005 | `5feb978d228ff705dcee86bb90cedaa328dfa196c6fdbbfc48468d6dfbd8cd74` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/cost_runner/experimental/mod.rs | 1476 | `6cd01d916403d3882bb936346bc543924acbafdc89d4aafd44bc736b9306fe8a` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/cost_runner/experimental/read_xdr.rs | 1360 | `18541840e2c4f85872cf9f47e8497dea8cb18e917c4aa73d05e47e39756e4939` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/cost_runner/experimental/sec1_decode_point_compressed.rs | 1728 | `d36738ca320aa22f294f727b8997faeac7e29190c94560e328545d92b217aab4` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/cost_runner/experimental/vec_ops.rs | 1132 | `8116fc7fe3f8d9259a9a98a719f9a8a67d96e2159db1644fc1e14cf352aaae48` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/cost_runner/experimental/vm_ops.rs | 2196 | `a253e366b149b7583c7e48b3aff4a982fca99e0194b526c5276fcaa81253323a` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/cost_runner/mod.rs | 787 | `d8b4f3f225b31efed2489ac70a610d6a774514944bdbb5645431e9cfef8251e3` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/cost_runner/runner.rs | 4175 | `3b52809532b30053143a982ab1c7ca72ae810e02b13c80b6ae15d1602241c664` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/cost_runner/util.rs | 1548 | `8d9741de3bc0ab1c9b3e4179d35cd04d8d61d9e5e42101a87763ba8f62325f92` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/e2e_invoke.rs | 33424 | `8a3b090887f7078ccb34d134117a0bc0b1fcc10e43d2c40e989386e8cdcab8f0` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/e2e_testutils.rs | 10219 | `6d7e109ac6dff91a99c289e9134b09b10c3728449dec272e49028803d5453627` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/events/diagnostic.rs | 5724 | `cc9c9e7ed0036b849e7c42d73faf4e028fcf00a79d9d8b9e2bf8513eae78e6b6` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/events/internal.rs | 10770 | `e8e2f8e1c189d006db1d648f083857b519eb37c63012e25423b9e1c7ea58b64d` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/events/mod.rs | 6989 | `55902e2c28907e67e261eed174e060d9f4f4633cf0c19ce8dc7373623812119e` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/events/system_events.rs | 1356 | `126b8da42733be7deea23b239008eeca261828c191862f26be1d759b82422f53` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/fees.rs | 15376 | `f91a883c6e5ac86e53751b743938d3d776def7a25150bf3803ae0d7878ca9d53` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/host.rs | 114459 | `051831451e4a5ff547ccf93011b672b28110021da52b2abf5b00c1b94c65b6f7` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/host/comparison.rs | 27459 | `e19ff27dad30ca7ec5256ac9415ffe9482458ff4ad249b9c5bc2121dd4b00ab0` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/host/conversion.rs | 20263 | `3bfa43bf380ee4b1fbac1ce2819b93ebae9f5eb43a2d20e0e438eed5f63db60a` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/host/crypto.rs | 12984 | `3b8dfcceb67d0242813bb58ee28b311247e4d4d9b3a5e43cc25006c44e689626` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/host/data_helper.rs | 22544 | `074d33a3d2d4bd5b6ba503d449f71341d2b9a2ab53d1045d05df04895f0811c0` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/host/declared_size.rs | 35970 | `c2bb2a58bb233b24030c99a0b49d7ac5d6a8f3d6897c31e0cbe108838d73f76d` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/host/error.rs | 17142 | `c0635541c097f9e0be306bfac1bfeb97d4e9039de12032de3530f0077d0fd8a5` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/host/frame.rs | 46729 | `03df449bf25b9b9c80793b4dcf010c55dc62e3e77d30ea7259f938a97fd2c014` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/host/ledger_info_helper.rs | 1502 | `9144a723b7119e868776cb21260b2f44ce286bc6a6485ada29c6133fc71e33ae` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/host/lifecycle.rs | 11229 | `ea18b7455e940c596f5c020eaaa283f8849cf7efdf96cae75d357d54dd341ae1` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/host/mem_helper.rs | 16799 | `c8fc69ed3d6af0b35ba2905bd5e35c8768d057577ce5da1ef214db627536c10f` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/host/metered_clone.rs | 24693 | `e18f88b6ff5cbde2891b550ec5520d1a2ab693371b36ed8e789b4c05829142de` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/host/metered_hash.rs | 2482 | `3792f8eea8df5b983fb363b0a282f8e91e3b7dfca5a424484cb5d3e0ae5c056b` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/host/metered_map.rs | 13760 | `e798d6eb82f1dfc2054fc1216bd0bf13b2c2cb344ddcb5e8d41f1cb99788f350` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/host/metered_vector.rs | 14304 | `b872b5c595424df07bd377fa16ba3d5e10d43109bf66fe2420286c9f2bf847ce` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/host/metered_xdr.rs | 2634 | `a6478cfc1f76a885d7969c49ea724ad181f2e025df6a0f88032e9680db51cb6a` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/host/num.rs | 2430 | `59c437ff2556b2d4511642307a2590aa4f0390320d4ffb89179b1d37569a3777` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/host/prng.rs | 8168 | `e278d8f8523981e438c29d5fa2644e5fa56446aa57a6a8dd0d7cb8641acfbbc9` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/host/trace.rs | 13265 | `2796b32ae451304e5239b4ca1493c03d8ec5d9b692dd5b1755d898cc5209bd31` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/host/trace/fmt.rs | 7973 | `54d53fdb44233459ef3c8816b3e3bc6314787cdbaec4216b097b8866955c23fd` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/host/validity.rs | 1818 | `b5c6baa004d08a398e6553f5336c5c1dc2ccb099dfdc0ed708ed967147c883d5` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/host_object.rs | 19308 | `d452565fa68cbf9b18c8de56ff4f0d345e205ebce0fae16ed57299043d4916e9` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/ledger_info.rs | 1348 | `5a7d202b945c0e639624746f926040eb873f640217652d55fb68fbc5acfb1f4c` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/lib.rs | 1992 | `2cbe4d1cee3c1fb46629189a2b1d7520c8c498321ffe293de1c40d0a091c0a62` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/macros.rs | 2394 | `9f4ae1003353842d0b43727fab8047c44af9fe781092d62ff513db5a5c1ccafe` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/storage.rs | 30128 | `8649ce51069b9f17d2997b8560cf9833318656eb39b235ade33f2d52fe56058d` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/testutils.rs | 41174 | `ffc1b4b489e8ee867f7e826d32e9f3071962c4fceee58e7ed6b5a79aa27af839` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/vm.rs | 24038 | `e080386c7fe54324bb9474d8ad6ac121cd2abce8602b2d3ac5a21b33c7456be0` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/vm/dispatch.rs | 13221 | `35209bf562e299ce3928b180192fc26c9c4c0d153a704cea89bc07571dc05a22` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/vm/fuel_refillable.rs | 2310 | `b8e65b7971534028a2e4f2e865653cee23252a4b750ba5c9da35071b7b1cb110` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/vm/func_info.rs | 6264 | `e40e04935448d357b02cc5173d1762d1cfdda7095e11f292537a198fcae07693` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/vm/module_cache.rs | 6435 | `6950b840d1548c82be5d8e56fec457d1d7344c1184dd9f2d0f995b885fc254fe` | 0 |
| src/rust/soroban/p21/soroban-env-host/src/vm/parsed_module.rs | 25042 | `cf11af4bff0eb7fd33c66630b01db3a103933c59c3e88a665014fae4b2df8d96` | 0 |
| src/rust/soroban/p21/soroban-env-macros/Cargo.toml | 736 | `17865565276d548bf1684f3e84653d616f98b39c8efc769e438559a05ca2e711` | 0 |
| src/rust/soroban/p21/soroban-env-macros/src/call_macro_with_all_host_functions.rs | 5354 | `44cc078e72635e4869c16316e5d11c1aed11a61f3906fcccf51a058b96fadb18` | 0 |
| src/rust/soroban/p21/soroban-env-macros/src/lib.rs | 7577 | `c1a35bd17bd32bbf02d8e4314637c54872bd996d812418bcdcb70f239ab3d571` | 0 |
| src/rust/soroban/p21/soroban-env-macros/src/path.rs | 561 | `6d186fe3120e11b1deb22d5faa6005b68ded100c76cfde483d729fe8ea15c813` | 0 |
| src/rust/soroban/p21/soroban-env-macros/src/synth_wasm_expr_type.rs | 11789 | `17af9baa60b261a49a13592ad52dcfcd23badc734d5f3cc62fb7e65ae94c54ea` | 0 |
| src/rust/soroban/p21/soroban-simulation/Cargo.toml | 1071 | `668cdacd08e5daceb27e9a2dd0a3ae9eee182bde88002154ce86e975104a863f` | 0 |
| src/rust/soroban/p21/soroban-simulation/src/lib.rs | 305 | `e57b2acb367061d89eff1f0912a5d704118ed99fbb21f519d9f07587b4a31808` | 0 |
| src/rust/soroban/p21/soroban-simulation/src/network_config.rs | 6131 | `7d89326e97b6ef25d5d4bb8774502b4979634c25272516cd6b674094ff652c45` | 0 |
| src/rust/soroban/p21/soroban-simulation/src/resources.rs | 12351 | `cb4c45866e7b80e590a542d96cc2b163500aabf4c66fa9c6c35b5cba681248e8` | 0 |
| src/rust/soroban/p21/soroban-simulation/src/simulation.rs | 14279 | `1c49e7268cdddd6f7b2e57eeabc29dc58c0f5bca97a917583651158a8ac8e4f4` | 0 |
| src/rust/soroban/p21/soroban-simulation/src/snapshot_source.rs | 10988 | `f491f1dc868e10849ad7102d8728f04efed8a015a0fc64d889abd46a79f4eb81` | 0 |
| src/rust/soroban/p21/soroban-simulation/src/testutils.rs | 4012 | `c3120c9a6ba757fab7ae30ba4638c617f5823d3c4a3f16bb12bb6cbab19f575c` | 0 |
| src/rust/soroban/p21/soroban-synth-wasm/Cargo.toml | 809 | `716d98debb3338990d4d706eec504fc8dea0bad1f4a52626eae0da6e4ae138be` | 0 |
| src/rust/soroban/p21/soroban-synth-wasm/src/expr.rs | 3370 | `20abb89282b4fcc30d85aa162b3edf8c49cd59a5d90ebc6bfd6ae6a24eacc3cd` | 0 |
| src/rust/soroban/p21/soroban-synth-wasm/src/func_emitter.rs | 15938 | `38d2d41444363114390bd9272701b0441a27402584df4983a08e075b7b9440e2` | 0 |
| src/rust/soroban/p21/soroban-synth-wasm/src/host_funcs.rs | 3101 | `92915e01ca0f79e0254df9d102417c9a14dbb8ad39fa28c3de967b5f20876832` | 0 |
| src/rust/soroban/p21/soroban-synth-wasm/src/lib.rs | 1130 | `b94fdbd1d86e3438c269123a6f6c9426e0791bf3b60d81d7b0b40dceb9544328` | 0 |
| src/rust/soroban/p21/soroban-synth-wasm/src/mod_emitter.rs | 17571 | `a00ebcc5927127a2ca07f082eeb2023b2d75084b54d1fd62974f16f060aa8632` | 0 |
| src/rust/soroban/p21/soroban-test-wasms/Cargo.toml | 241 | `6eef4c0875ef4d266d255a5f5c6bdfee377c1d347b4f7e5418f6ee1134739280` | 0 |
| src/rust/soroban/p21/soroban-test-wasms/src/lib.rs | 6176 | `50f58dfeccbf81f54ff17a4e0005e3080ba76b948603e6895d99750570f9d8a4` | 0 |
| src/rust/soroban/p21/soroban-test-wasms/wasm-workspace/Cargo.lock | 40146 | `9a6efe112f6debec16ce78a60fc261cab0cc936fed56710172399cdca3eb3916` | 0 |
| src/rust/soroban/p21/soroban-test-wasms/wasm-workspace/Cargo.toml | 2426 | `74d7ff30f09ad74b8568052990bbb167439fb2a3a994d2a9ea2f962dbb6eb3df` | 0 |
| src/rust/soroban/p21/soroban-test-wasms/wasm-workspace/add_f32/Cargo.toml | 398 | `57b505c9403f7350323dc9766db9276f9ac37f114ab4b2d6eaefbf0d536fa478` | 0 |
| src/rust/soroban/p21/soroban-test-wasms/wasm-workspace/add_f32/src/lib.rs | 336 | `099703bd2f3f4088add74ae0d0f900d1cddb16967d483ca76480bd37e5aaa525` | 0 |
| src/rust/soroban/p21/soroban-test-wasms/wasm-workspace/add_i32/Cargo.toml | 398 | `bf7cbb00090208bb631be314c43a23bd82873a766f44117e95b6d2d5119d05c0` | 0 |
| src/rust/soroban/p21/soroban-test-wasms/wasm-workspace/add_i32/src/lib.rs | 275 | `609f7db6583e31743bb9b6baa6d7f9f272b3d0f76cc9bc633244bdadc1ae7856` | 0 |
| src/rust/soroban/p21/soroban-test-wasms/wasm-workspace/alloc/Cargo.toml | 418 | `3481fa592be927a6bc916cfa97a4bbd6fc3882e17e707f5c44d573ab2afb989c` | 0 |
| src/rust/soroban/p21/soroban-test-wasms/wasm-workspace/alloc/src/lib.rs | 708 | `3ad94be5c06b55ed4639bb79f59be677ae9f8c38884bccb249bade8e7f4ad870` | 0 |
| src/rust/soroban/p21/soroban-test-wasms/wasm-workspace/auth/Cargo.toml | 401 | `584b31c30ce5b2c0068535098587c2685bc51509257afe979574448724e76910` | 0 |
| src/rust/soroban/p21/soroban-test-wasms/wasm-workspace/auth/src/lib.rs | 8544 | `2e0064ca991f83c3a00177f052bbc5c053087546ed1e42a944c7af810bb03621` | 0 |
| src/rust/soroban/p21/soroban-test-wasms/wasm-workspace/complex/Cargo.toml | 382 | `1012d55446546ce1bdd1548f8e09d7ee382b7c543f30b0d45802981774d00f1d` | 0 |
| src/rust/soroban/p21/soroban-test-wasms/wasm-workspace/complex/src/lib.rs | 1522 | `7fb764db8fd1ff735f0077daa0c0f8fbca952fb621075820dd741321a27b37d0` | 0 |
| src/rust/soroban/p21/soroban-test-wasms/wasm-workspace/conditional_account/Cargo.toml | 391 | `cd4b7a2986343e3a1dc896dc015aa7ef752d9eb493a2f7ccb2f72c9f30292df4` | 0 |
| src/rust/soroban/p21/soroban-test-wasms/wasm-workspace/conditional_account/src/lib.rs | 1190 | `8373ab257590bdc0023784bdcd8c465630ca631a1f820b1db1e6fb9b88fbf4ab` | 0 |
| src/rust/soroban/p21/soroban-test-wasms/wasm-workspace/contract_data/Cargo.toml | 426 | `eea0cfb3398a8905b1c749d382010df92150da82a86208562c54c29f26ec44ca` | 0 |
| src/rust/soroban/p21/soroban-test-wasms/wasm-workspace/contract_data/src/lib.rs | 2543 | `6c0338d09518eb380e996f7ea007f5f50a9f3c6d37b1e2a26913622e71aec0d8` | 0 |
| src/rust/soroban/p21/soroban-test-wasms/wasm-workspace/contract_sac_transfer/Cargo.toml | 388 | `9b4d6396f0ffd2ed7d6cc30886dc66142ddab1b795a7e2880df933a6867df109` | 0 |
| src/rust/soroban/p21/soroban-test-wasms/wasm-workspace/contract_sac_transfer/src/lib.rs | 516 | `3ea0c5d8a73c364a635b1c2679bfa610ac657642451bc639f6dc5ff4c16020ba` | 0 |
| src/rust/soroban/p21/soroban-test-wasms/wasm-workspace/create_contract/Cargo.toml | 406 | `acfd5c14bf5d848c890dbed7d59f09438e497f3fb0b94558c7825395a2f30e93` | 0 |
| src/rust/soroban/p21/soroban-test-wasms/wasm-workspace/create_contract/src/lib.rs | 419 | `d999ae4431e2cca2ff8500a042c58581208a70775eada7264e8985de95b11138` | 0 |
| src/rust/soroban/p21/soroban-test-wasms/wasm-workspace/delegated_account/Cargo.toml | 389 | `775e8481ca0f918a0b3cecf8f72d3334f9e9ecafa7976cdf73c483b7d6480438` | 0 |
| src/rust/soroban/p21/soroban-test-wasms/wasm-workspace/delegated_account/src/lib.rs | 868 | `36ad27bafba63f3f84003fc542a5ea676ae40bd5cf95d76532fcbf15f57c64e2` | 0 |
| src/rust/soroban/p21/soroban-test-wasms/wasm-workspace/deployer/Cargo.toml | 333 | `ffac8815e6d766ee6503c586199ad9e737532fb2986e799c63be683baacdc544` | 0 |
| src/rust/soroban/p21/soroban-test-wasms/wasm-workspace/deployer/src/lib.rs | 1873 | `ade03dfecc57c2a865c94f0e96203aae80eb6b5a081827a7247768a55fd561cc` | 0 |
| src/rust/soroban/p21/soroban-test-wasms/wasm-workspace/err/Cargo.toml | 394 | `1199ec7e73ed605a36cec60abcf9e764efa1647a15bb70d752f5e6e7b41fd296` | 0 |
| src/rust/soroban/p21/soroban-test-wasms/wasm-workspace/err/src/lib.rs | 2881 | `6d421da68d5bcfb4dec07757387e48833cb5f3bbe6ce99dfd8730a08605aed23` | 0 |
| src/rust/soroban/p21/soroban-test-wasms/wasm-workspace/fannkuch/Cargo.toml | 399 | `671e27d1ef8a0fb4484973c5078c52a733411f1691f3ac81244ba436511d6346` | 0 |
| src/rust/soroban/p21/soroban-test-wasms/wasm-workspace/fannkuch/src/lib.rs | 2236 | `f8af8a42fd6fc33fde15a97091e4382bba5c851e44210cf3a840f70d8ef81c97` | 0 |
| src/rust/soroban/p21/soroban-test-wasms/wasm-workspace/fib/Cargo.toml | 394 | `ab3b6ac2010d7fb21193c223de82c9de425ac203ba5dade839346faf4ebe16a9` | 0 |
| src/rust/soroban/p21/soroban-test-wasms/wasm-workspace/fib/src/lib.rs | 268 | `c957875f4c1b35d053c3b2d746bcf748667913f12e33be6e03d244b537521d84` | 0 |
| src/rust/soroban/p21/soroban-test-wasms/wasm-workspace/hostile/Cargo.toml | 398 | `2fd054cecd1e274843d7646455d52e12387ffb57d1d5d7b2944e00d3731ba617` | 0 |
| src/rust/soroban/p21/soroban-test-wasms/wasm-workspace/hostile/src/lib.rs | 3124 | `c2eedf2f69c9f8cefbcf0e12967b76413d1b42e347f6478c221e8b294c6227f9` | 0 |
| src/rust/soroban/p21/soroban-test-wasms/wasm-workspace/hostile_large_val/Cargo.toml | 400 | `84c37ed639216b8696c0ca335098408978497b3f9b10fd5fc02f0d13eb260dc0` | 0 |
| src/rust/soroban/p21/soroban-test-wasms/wasm-workspace/hostile_large_val/src/lib.rs | 2553 | `dbf1d00afd9f5f62c0bab4a4e51114fb876585262f8da8af1f030f04031d9a02` | 0 |
| src/rust/soroban/p21/soroban-test-wasms/wasm-workspace/invoke_contract/Cargo.toml | 406 | `ef18142c281c7be0329a7a73a35bbac9682cedc8ddeb6fc59c7fd97fd346132b` | 0 |
| src/rust/soroban/p21/soroban-test-wasms/wasm-workspace/invoke_contract/src/lib.rs | 1943 | `331251706eeb7ca4c8f64877b2f4e2176b7195299989a6271db21db3c0a70357` | 0 |
| src/rust/soroban/p21/soroban-test-wasms/wasm-workspace/linear_memory/Cargo.toml | 388 | `68fcd3be1c41a4d6976d07965387ffcfe8f5245840cb44d0f41737caf7a4a02e` | 0 |
| src/rust/soroban/p21/soroban-test-wasms/wasm-workspace/linear_memory/src/lib.rs | 2861 | `998f890f085a31c269dee25aa5ac3eef9a62efc4166d2d26377073eab3574a3d` | 0 |
| src/rust/soroban/p21/soroban-test-wasms/wasm-workspace/loadgen/Cargo.toml | 382 | `ad44b1176d45c730d89e27b0ad3fab9da047ba3c7ca403bebe5578146e3b0db5` | 0 |
| src/rust/soroban/p21/soroban-test-wasms/wasm-workspace/loadgen/src/lib.rs | 1370 | `44d808454841cb78617330c260c6fe73b5fb13b095c15c88bc117a9787f6c664` | 0 |
| src/rust/soroban/p21/soroban-test-wasms/wasm-workspace/recursive_account/Cargo.toml | 375 | `aa8e4f9caf805a878a44d89cc8b4f1023a146ccb235467257b69a9d151d6b939` | 0 |
| src/rust/soroban/p21/soroban-test-wasms/wasm-workspace/recursive_account/src/lib.rs | 1819 | `99df3ded80c336870ed36935ca34af8306c1644bcc127f8adee9e6cb26ff2a24` | 0 |
| src/rust/soroban/p21/soroban-test-wasms/wasm-workspace/sac_reentry_account/Cargo.toml | 386 | `90859f5d2e828c0dfae664526a298218c3225f629ace5d27309e1296b55ab7e9` | 0 |
| src/rust/soroban/p21/soroban-test-wasms/wasm-workspace/sac_reentry_account/src/lib.rs | 1176 | `44c4a73769a6db79991b2b981560e4c62df6a07a5a467550c8995f5333af2164` | 0 |
| src/rust/soroban/p21/soroban-test-wasms/wasm-workspace/simple_account/Cargo.toml | 389 | `b4146ef0490991bc020fec1529ab9cf7abd8a1e0c9278f57fbd1c214652e3111` | 0 |
| src/rust/soroban/p21/soroban-test-wasms/wasm-workspace/simple_account/src/lib.rs | 948 | `7c74cf48ea7db5ed1ff209926ba7d98ba4c32127d9e52e229a3c90eedfed4e28` | 0 |
| src/rust/soroban/p21/soroban-test-wasms/wasm-workspace/sum_i32/Cargo.toml | 398 | `fceccbc33a828ebda7dd4aace444eb8a5b508ed79907b7478dc1ac3fbbe111b1` | 0 |
| src/rust/soroban/p21/soroban-test-wasms/wasm-workspace/sum_i32/src/lib.rs | 561 | `4b1c69bf2e59646c6202ce0e9e460a7d22eea3490e517ecc4f56cfc8e4b8f49b` | 0 |
| src/rust/soroban/p21/soroban-test-wasms/wasm-workspace/update/Cargo.toml | 410 | `7e3d997807ffbc354ffd26c1556458e6776aa98dbf978d05256b5e395289f02a` | 0 |
| src/rust/soroban/p21/soroban-test-wasms/wasm-workspace/update/src/lib.rs | 945 | `d0ae9d5190e0f6251ee7182be9c052e068695ed305c7666caf4b455789c72c93` | 0 |
| src/rust/soroban/p21/soroban-test-wasms/wasm-workspace/upload_contract/Cargo.toml | 406 | `79f437d05d1eb91269ba587ab4c1f40c5a76b3194864a16f55cb869f45bb5507` | 0 |
| src/rust/soroban/p21/soroban-test-wasms/wasm-workspace/upload_contract/src/lib.rs | 252 | `5033bb1c628243bdaecc55b1c7676b20b22f73fe4842905b5bb92a1a111061c9` | 0 |
| src/rust/soroban/p21/soroban-test-wasms/wasm-workspace/vec/Cargo.toml | 378 | `076d8806b4b214776eacf7e39cccb493b2db1b850e006ef73a6c33736ef8da4c` | 0 |
| src/rust/soroban/p21/soroban-test-wasms/wasm-workspace/vec/src/lib.rs | 346 | `a358381709762177476df8c9dcacdc6406e499b81de7523278f3fbf5212aa7d3` | 0 |
| src/rust/soroban/p21/soroban-test-wasms/wasm-workspace/write_upgrade_bytes/Cargo.toml | 419 | `dd1b71224963adf1942f76d1646e4740bea337536eb26da0ad22c651dc2bfc25` | 0 |
| src/rust/soroban/p21/soroban-test-wasms/wasm-workspace/write_upgrade_bytes/src/lib.rs | 996 | `8e689d1b7baa6649a6367775d91623e6ecd59da6841f151e39ddf937f8b7f260` | 0 |
| src/rust/soroban/p22/.cargo/config.toml | 6685 | `deaae172a164fb2ba5bfa0e6b3658fc8ef043a348c861936762a8a210c213ca0` | 0 |
| src/rust/soroban/p22/Cargo.lock | 59614 | `14c9c48bd35c564077aad0a9f4c0225fa40f9c92bcf4c31c4b8986934ee3ec5e` | 0 |
| src/rust/soroban/p22/Cargo.toml | 1913 | `3d1bc370af21e192a5f47d1d20cd03b4e8b0c24a667bb429a58fce75820a382e` | 0 |
| src/rust/soroban/p22/rust-toolchain.toml | 133 | `dd1e82393723dd0546770d2e0fd9b64baab923e2cdba735bdff577a34a791081` | 0 |
| src/rust/soroban/p22/soroban-bench-utils/Cargo.toml | 787 | `2020e9795c6dc4edfee39f36f1d78cf16b954f69ac16f9cba453485985d4edd3` | 0 |
| src/rust/soroban/p22/soroban-bench-utils/src/lib.rs | 75 | `4ed9af88c90c8137a175e9b2e583a3076ef13bc4911e133e889aa6f559caeeab` | 0 |
| src/rust/soroban/p22/soroban-bench-utils/src/rusagev4.rs | 2027 | `e775f766b27fcece33febfaf91e1b2e46b4ff0d7028a326909fd910dd75c7b17` | 0 |
| src/rust/soroban/p22/soroban-bench-utils/src/tracker.rs | 5923 | `71df7e2a505682276058fba51644bfe0f0d59934c327b9f4bb14ee6d59a6f8b4` | 0 |
| src/rust/soroban/p22/soroban-builtin-sdk-macros/Cargo.toml | 554 | `828f2414d8e7d7ded5567797a4eae4cd132908234489fc5ef6d327e99fe29d32` | 0 |
| src/rust/soroban/p22/soroban-builtin-sdk-macros/src/derive_fn.rs | 2815 | `627430878da696e94b872adc29d71390e866277ee7acf6c1b42e7cdd2ccf15a0` | 0 |
| src/rust/soroban/p22/soroban-builtin-sdk-macros/src/derive_type.rs | 8525 | `459416267127d646b9d105c16c046b210eeb22cd4c482511f268d8396120f215` | 0 |
| src/rust/soroban/p22/soroban-builtin-sdk-macros/src/lib.rs | 1734 | `7120a6c227f456234536bfef7c7f9d82918a8c89d8c25f3f16eaccc404a79aad` | 0 |
| src/rust/soroban/p22/soroban-env-common/Cargo.toml | 1564 | `0f5adc80e188724943b19317d9385671b59ca6f14d482a3cf067f4daeab7d89c` | 0 |
| src/rust/soroban/p22/soroban-env-common/build.rs | 99 | `818b5844721186dd913412974faaff4bb45954e41b2cedeecb4b0a5ddcf90b35` | 0 |
| src/rust/soroban/p22/soroban-env-common/src/arbitrary.rs | 2047 | `aaebd099ab97097e1ac2482ac4c437c99736f75ca822cfdcec435ccf8b8fb662` | 0 |
| src/rust/soroban/p22/soroban-env-common/src/bytes.rs | 3066 | `768838872830e2352670e97ad9d9313c24db0efb8854847474739ed33c7c5735` | 0 |
| src/rust/soroban/p22/soroban-env-common/src/compare.rs | 7453 | `6f02fb0afd08619f9566de017a510a5f7fb0202d4d5c589cf9f03dc7634d090d` | 0 |
| src/rust/soroban/p22/soroban-env-common/src/convert.rs | 19671 | `c5f685d8b7a75354c2b2b00154a331d5f93d97b9cf5ff8f0d6d245670da1e9f4` | 0 |
| src/rust/soroban/p22/soroban-env-common/src/env.rs | 17907 | `30d4f9ada846516cef746a12ba36e700d260d43a18cd73d4b5cd619e9cf8da10` | 0 |
| src/rust/soroban/p22/soroban-env-common/src/error.rs | 15600 | `efd9f516f411d55dd01a22e33f3418068d82c715290382e98a5cba4f58bdc46e` | 0 |
| src/rust/soroban/p22/soroban-env-common/src/hash.rs | 1437 | `efb8351b71469d22beca2e1b2f2b65a9e18db9d82a04a60b79d7126979fca09b` | 0 |
| src/rust/soroban/p22/soroban-env-common/src/lib.rs | 4140 | `be91955acebd113577bdd4fd6dec7b4cdb4b04b3fb28ad76f641fba42282d88b` | 0 |
| src/rust/soroban/p22/soroban-env-common/src/meta.rs | 3279 | `d44186ae2ade9c5920ee938405252b208141a820f1c4be17e9d7b174f183cc06` | 0 |
| src/rust/soroban/p22/soroban-env-common/src/num.rs | 14398 | `7e3c2c265ada670880e27d9d3f82036ab50a4c402a0d384d243dd412b97cb72f` | 0 |
| src/rust/soroban/p22/soroban-env-common/src/object.rs | 5974 | `055ee181559ba02962d8837461b8e9e81e6b7bf37cf3b0c1a6e99a4857c3aaf9` | 0 |
| src/rust/soroban/p22/soroban-env-common/src/option.rs | 907 | `870a61869cabc46e32f50c93605686f4d66f1952bf89f596b8fbfdcaf5deb38e` | 0 |
| src/rust/soroban/p22/soroban-env-common/src/result.rs | 1261 | `d3210db790113cf7950e76c15492358ca9a469159f8dee2c27c2dee91228c4b0` | 0 |
| src/rust/soroban/p22/soroban-env-common/src/storage_type.rs | 1076 | `f3dcf69433e9c8a2d1b1f3e3202955d87abb2ba9fe365f70629a402c30a56641` | 0 |
| src/rust/soroban/p22/soroban-env-common/src/string.rs | 2036 | `13ec3079a2f66e4affb3ecdeba15134f2941ef05076f544a195736dbd64bf8e9` | 0 |
| src/rust/soroban/p22/soroban-env-common/src/symbol.rs | 21416 | `535b8c4dc64fddc986e76d364ed319405f00e1f95bdf2fed02253fc1ecfab185` | 0 |
| src/rust/soroban/p22/soroban-env-common/src/tuple.rs | 4295 | `fed0d299699f9ad2f429f68199534af4b319cfbc960dfdf488e9dc943fae95ad` | 0 |
| src/rust/soroban/p22/soroban-env-common/src/val.rs | 30571 | `23506089c05ea5afc7100dd88b6ed2ef1ab803cfdcea5ea2b4048537537cf0de` | 0 |
| src/rust/soroban/p22/soroban-env-common/src/vmcaller_env.rs | 11519 | `74a5c41dbefeea05df0bae94274fb23302931a2f3eb6305382c9cd1c33cfc482` | 0 |
| src/rust/soroban/p22/soroban-env-common/src/wrapper_macros.rs | 12097 | `0228b5e35382d4dbca4b760f3f6a57d0a7ecbb9ffa897f16d445c82ce6e63e93` | 0 |
| src/rust/soroban/p22/soroban-env-guest/Cargo.toml | 625 | `65d7195e1ef69e1cba7c6aabd96072fe37482f0b1c7ecaeb17e17cc38b2ab937` | 0 |
| src/rust/soroban/p22/soroban-env-guest/src/guest.rs | 15204 | `510b8fce90a317d8eb8622c38169663d1dd3a324b757b91b6aa2370cac4f5653` | 0 |
| src/rust/soroban/p22/soroban-env-guest/src/lib.rs | 561 | `b34cdc92dbf3880bd463d0c82b7df5866ac88d74b8bc42d8a9321eb9104dcfdf` | 0 |
| src/rust/soroban/p22/soroban-env-host/Cargo.toml | 4897 | `92f69b02a2bde5caccb3dd39934d93b93decdac32a2006212fa14f2da7a4389c` | 0 |
| src/rust/soroban/p22/soroban-env-host/build.rs | 283 | `f90c468c4ab2735a8edeca9f82ca31cf327a27fd8baf47f7417dab8653151005` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/auth.rs | 97833 | `ca5fb26e39cbc28f14c94b1799a68ef939ede917f061558d0260c73f802d64b5` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/bin/main.rs | 1403 | `aae7d92a9c7a40e441e38d8a5767eae368e3dc89c869a2f297c3be42683c883f` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/budget.rs | 52597 | `8682fcde73d86809d506e8d9044f06b526ede4d0dd2dc1f0759e3161d174001c` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/budget/dimension.rs | 6660 | `571d461de66a88bcc491ae13d8394d3416774e09de981c22643a431775750553` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/budget/limits.rs | 4658 | `0080964f53ec49d2df64306354887cc5565b2628584e64548126a4b95e2eca1e` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/budget/model.rs | 5584 | `b6d99a8a793cd385cdcaaa7cd288d279b5628670ee34b7b83504a0276e982635` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/budget/util.rs | 7104 | `77f7128a74a74a2da8fb994e87433848dae4bfd82059e32235781cab98f31d48` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/budget/wasmi_helper.rs | 4145 | `c7afc9c4c05a9ee57d0da858369312d9d0ba431bc337d02b98d750cfb4fbe0d0` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/builtin_contracts.rs | 560 | `f0bd26290068aff0d567b8e950c3abd9545b9f6fbb50a521001e21f9b3a7ed1e` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/builtin_contracts/account_contract.rs | 9283 | `188eef0e0f48d8763b707a142e6f137b112b6abe510f9fa15c9141a768a9fe6c` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/builtin_contracts/base_types.rs | 9926 | `142fb5fda62ddeab16748770b70523b470cb46b080f421a328c41186b0391ca0` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/builtin_contracts/common_types.rs | 657 | `21c7d8c3cd943a3384ec5c9545f912fd0f1ba2c2a6fa3f99afb071aec7d43d9d` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/builtin_contracts/contract_error.rs | 881 | `bf6a304eb50eac03bc3cf2a21fcfcd58cf0501b698a721c575b034f389b76d2a` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/builtin_contracts/invoker_contract_auth.rs | 6548 | `78a4fdc1eed21493e5542ec6d6e53f64a3b0877dbef0e52f6ebc1c1cfe8d4af4` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/builtin_contracts/stellar_asset_contract.rs | 248 | `944142447b113d671f1e47dc8a2d8191ef4ff11167b793f2a4c2f4d72efc8e4f` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/builtin_contracts/stellar_asset_contract/admin.rs | 704 | `ad70748dab976704bdf5fa87dfe30c0746280a24eb46c36a9c102aeb1f11980d` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/builtin_contracts/stellar_asset_contract/allowance.rs | 5086 | `6ea9c9360181cd73eaa569c5be0ae95301d56e5ce33aa06bb26b821d3eb56ce8` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/builtin_contracts/stellar_asset_contract/asset_info.rs | 3092 | `9a0583a6bec016f2822bc357baa2cce81c8e4ad3077fd8d5e2100172c0b22def` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/builtin_contracts/stellar_asset_contract/balance.rs | 28306 | `930595374eaff715e17b47aa2ddb0f4acf43b02330962b72ce60199b334d5e1d` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/builtin_contracts/stellar_asset_contract/contract.rs | 13008 | `c7234e92b6d31b00a16e454f57432ad9f2b1d61666a61ed1d150fa475f62feb8` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/builtin_contracts/stellar_asset_contract/event.rs | 2488 | `5fe7009aabbe3d29676bb0c8e5541163e5774a53f8967a70a79ae2cc24a67cd2` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/builtin_contracts/stellar_asset_contract/metadata.rs | 6992 | `12ca5219bd19e98b81880a01e5fe99bfffaf1c5d283371bff34961763ac00331` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/builtin_contracts/stellar_asset_contract/public_types.rs | 1318 | `84834c2fec3c9763ba73d89fdd44db86da9a35400e82401cd5ba04ed03874026` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/builtin_contracts/stellar_asset_contract/storage_types.rs | 1113 | `655a0cec594b78db2eeccabfe03e27f2ae0537c65729e456b604cbbdb579f298` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/builtin_contracts/storage_utils.rs | 362 | `216d16572291ac021fd3ee7a0ce6d4b1810f8dbee07fc2791bbf32236a75ed10` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/builtin_contracts/testutils.rs | 11060 | `d72eace5611ec5988f3a32a06ab52e8085823b3503b7f94d03def35d39795b74` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/cost_runner/cost_types/bls12_381.rs | 10204 | `965dff98b1d17f2c58dd07697781db1c8033193651fb14d4473b091fb6ab43c4` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/cost_runner/cost_types/compute_ed25519_pubkey.rs | 952 | `c679365a8825299630452cf28daf21f4e6cff1805ca06910bc4ce49300d04a7c` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/cost_runner/cost_types/compute_keccak256_hash.rs | 916 | `c70f481dcea5eba30a4ae54ea476efec3fb3bf938d15987042aaeac222bbef3d` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/cost_runner/cost_types/compute_sha256_hash.rs | 896 | `99eece10c8e2379a0d3675f618b6c9192a57ddd98bc0063cc886ab22d526b509` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/cost_runner/cost_types/decode_ecdsa_curve256_sig.rs | 1407 | `6eae776ff6b8ee070b6d51f70a4b231bf78c2bd0e964c0cae695be06a66b251e` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/cost_runner/cost_types/host_mem_alloc.rs | 951 | `53bd536e402308f09e0ead2a7825d8a7a88c6da46f0deb55ddce336d6a754a32` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/cost_runner/cost_types/host_mem_cmp.rs | 957 | `db2b390ce0892f2b450a9707d8f3d54a9fe2438d88f73ae021263dc18b266a3c` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/cost_runner/cost_types/host_mem_cpy.rs | 821 | `7ab8627489d5882ca2725d3e5872dc5cf3907890341065e5fa9149b121f11316` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/cost_runner/cost_types/invoke.rs | 2183 | `451a7818021ac77658771411708fe709c328f8d29abb0906720cd4da4fbb069d` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/cost_runner/cost_types/mod.rs | 983 | `0e319de5bfa8eeafbc2f98d9187c31084ba8ae0755533496d9b3563ee62b3c43` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/cost_runner/cost_types/num_ops.rs | 1546 | `cf08647785a4ede49183258e305e4520b3db286536bf2a6e71583e76c89be32b` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/cost_runner/cost_types/prng.rs | 1003 | `fac74f446f916302d6b27d59040ae6c72aa4decbfe766a862f9b0a2dceb75223` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/cost_runner/cost_types/recover_ecdsa_secp256k1_key.rs | 1140 | `21256191032a43cd2584275eebae7e034db553ee6c90c16d6ba5e5e2392eb69a` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/cost_runner/cost_types/sec1_decode_point_uncompressed.rs | 1155 | `06fda4cc5f09ca513953f45424b1aa5277fb1fa0805e598e63466ea6b45d1863` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/cost_runner/cost_types/val_deser.rs | 800 | `19b4abd59908d36bc2c1a2d7e05fc67db21df215cf02bcf91ff42d760f18e6d0` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/cost_runner/cost_types/val_ser.rs | 1385 | `2b3aa6b23feb1d99fdfc267146458eba577e8641124c8673a606fa0cb976b08e` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/cost_runner/cost_types/verify_ecdsa_secp256r1_sig.rs | 1124 | `8b1e249924c8f329e563122f8e2c1d0e60fbc6c788de70c0dd4e9aeaf8f8b833` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/cost_runner/cost_types/verify_ed25519_sig.rs | 1079 | `da86df368d3cdc769f57e48a6fd160ba5c7f1dab0a44876587875be1167215bc` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/cost_runner/cost_types/visit_object.rs | 1056 | `c66e1ae7580a923564f8694f34d3ee9ff4c3de2b768529cf75a9f86e23c9c656` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/cost_runner/cost_types/vm_ops.rs | 8434 | `1f77d6fc6ff198a85d1871352c92d3eb85ae952d07f496cba0c4b42c7c23cad4` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/cost_runner/cost_types/wasm_insn_exec.rs | 9902 | `2c3bfc08db067c5d0320dfbbb55d477019e282d7c7a4d4c6c1c704b47a6b2983` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/cost_runner/experimental/bls12_381.rs | 6378 | `154aed6d61b073065304ff1b68dd8eb3709a82108a7983d23a44cb01cb744ac1` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/cost_runner/experimental/decode_secp256r1_sig.rs | 1472 | `2f7bf5f395b05ad7ae9ab37e404eae4c3bfa85d29eaa8d08becfcfef825b0a1e` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/cost_runner/experimental/ecdsa_secp256k1_verify.rs | 1487 | `d5d2bdc6133fc64cdbe0765a2d5ee6069a9cfedb8b03943dff269770d30b88c6` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/cost_runner/experimental/ecdsa_secp256r1_recover.rs | 1499 | `2e4920ce9df183016f9bf4765bde45f76b746f34d636b03d21647e8ee7bfb7f3` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/cost_runner/experimental/ed25519_scalar_mut.rs | 1353 | `5b0755082fbcd387ee756a4fcb85b19abb7f632aabefddae79063463cd81b480` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/cost_runner/experimental/map_ops.rs | 1005 | `5feb978d228ff705dcee86bb90cedaa328dfa196c6fdbbfc48468d6dfbd8cd74` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/cost_runner/experimental/mod.rs | 2700 | `cc07f061fc69b5348c5cb1e8dbaaad46f4b06ff7a396245618d954e98d4c77cd` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/cost_runner/experimental/read_xdr.rs | 1388 | `476f11215c5a4bdcebe94772688e45f28d96db4f5dfe4da029507cd01d4f3f3f` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/cost_runner/experimental/sec1_decode_point_compressed.rs | 1756 | `299089e64c18ca9c4414a6461eaf023cbcfdbdca24db9f55edbf28f922771643` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/cost_runner/experimental/vec_ops.rs | 1132 | `8116fc7fe3f8d9259a9a98a719f9a8a67d96e2159db1644fc1e14cf352aaae48` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/cost_runner/experimental/vm_ops.rs | 2196 | `a253e366b149b7583c7e48b3aff4a982fca99e0194b526c5276fcaa81253323a` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/cost_runner/mod.rs | 787 | `d8b4f3f225b31efed2489ac70a610d6a774514944bdbb5645431e9cfef8251e3` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/cost_runner/runner.rs | 4203 | `98f216ef92f42ce6364d6aa13cffcc33a6da9fa344469ebe0b7093614ca71fc7` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/cost_runner/util.rs | 4774 | `9cbbfe0c50bd607d1d879a9968fdd5ec69ae096faa34216a7bbbe7986e2bc57c` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/crypto/bls12_381.rs | 32393 | `e5a30609cf9ed9d774b3bff1cf2b74f8bc251f33c9ecdcdd5adf799e11140c20` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/crypto/mod.rs | 13040 | `ccbe1563db40bf085dacdc7d468d0ac5b3230274e1ac237509c81868c8af8411` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/e2e_invoke.rs | 33624 | `8b66f124a417ec6f58844d675a5231ba2cd5dbe2f25dd8085b79dcfb32b1f5c0` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/e2e_testutils.rs | 11470 | `e1aea83e5cd999e44161d9c61dddf1812545cc6e6d9c7f692e8d635fc0501878` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/events/diagnostic.rs | 5724 | `cc9c9e7ed0036b849e7c42d73faf4e028fcf00a79d9d8b9e2bf8513eae78e6b6` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/events/internal.rs | 10770 | `e8e2f8e1c189d006db1d648f083857b519eb37c63012e25423b9e1c7ea58b64d` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/events/mod.rs | 8183 | `a9a1455bf98a301a7f6b55e2f70cfc3b4af16e9c864f6a87724d93c7e63013e0` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/events/system_events.rs | 1356 | `126b8da42733be7deea23b239008eeca261828c191862f26be1d759b82422f53` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/fees.rs | 15376 | `f91a883c6e5ac86e53751b743938d3d776def7a25150bf3803ae0d7878ca9d53` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/host.rs | 124029 | `607a11e4c84f1ac188186d237b4acf91b309fd590b566adbbbde9c8962acf0a7` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/host/comparison.rs | 27508 | `89bcbde0728c61029a1fef38ed406c7cc894183c6adda8bbc66dd5315bf0a5fa` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/host/conversion.rs | 20263 | `3bfa43bf380ee4b1fbac1ce2819b93ebae9f5eb43a2d20e0e438eed5f63db60a` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/host/data_helper.rs | 22544 | `d0d561df569a17e52c32187728570d36d13bf70480680058cee9fe5c496c42ac` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/host/declared_size.rs | 36636 | `77cd5be035003bad0ff1c1c77e43cd8f47671ca1eb1265a2996cdbccd600bf0c` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/host/error.rs | 17240 | `ca3bb6123ed7b5cfd6c3ee57e98abe4f6a0817c861f5ad43e60f2dc9785e8759` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/host/frame.rs | 48194 | `7337231caf52a8dd7b8163b3774afcb6a6660acc5d22ea897bb6bcf04dfd93c1` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/host/ledger_info_helper.rs | 1502 | `9144a723b7119e868776cb21260b2f44ce286bc6a6485ada29c6133fc71e33ae` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/host/lifecycle.rs | 14897 | `9f8c05b89cdae988030a31275136a580192731b9699609d36e30637d6623d663` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/host/mem_helper.rs | 18140 | `b7a0185c89a1208d67944604763182986d336a54c13ca8ac496cac1abb25d9dd` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/host/metered_clone.rs | 25244 | `81e8841eac04debb379a41eaa2f522a1dbc2967281c0b11c5d3cc3dd5e0edab2` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/host/metered_hash.rs | 2482 | `3792f8eea8df5b983fb363b0a282f8e91e3b7dfca5a424484cb5d3e0ae5c056b` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/host/metered_map.rs | 13760 | `e798d6eb82f1dfc2054fc1216bd0bf13b2c2cb344ddcb5e8d41f1cb99788f350` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/host/metered_vector.rs | 14304 | `b872b5c595424df07bd377fa16ba3d5e10d43109bf66fe2420286c9f2bf847ce` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/host/metered_xdr.rs | 2628 | `049eac74615f58520b378e9fb1eec469d551da78bea9b635b52917c8ca806cf8` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/host/num.rs | 2933 | `e188fe8582e1ff99f1ed9123e6f30bbd3903c89c6ba3d31644c1d7a3c1e983df` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/host/prng.rs | 8157 | `eeed1bff44661301241a4bd31c87705cc202eb8efd829763646947091bb6de39` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/host/trace.rs | 13265 | `2796b32ae451304e5239b4ca1493c03d8ec5d9b692dd5b1755d898cc5209bd31` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/host/trace/fmt.rs | 7973 | `54d53fdb44233459ef3c8816b3e3bc6314787cdbaec4216b097b8866955c23fd` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/host/validity.rs | 1818 | `b5c6baa004d08a398e6553f5336c5c1dc2ccb099dfdc0ed708ed967147c883d5` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/host_object.rs | 19308 | `d452565fa68cbf9b18c8de56ff4f0d345e205ebce0fae16ed57299043d4916e9` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/ledger_info.rs | 1348 | `5a7d202b945c0e639624746f926040eb873f640217652d55fb68fbc5acfb1f4c` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/lib.rs | 2014 | `8318b8c3fdfc678a2ff9db0ee47163e26ba2d2bc17f9159b9de89779ba2671bc` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/macros.rs | 2394 | `9f4ae1003353842d0b43727fab8047c44af9fe781092d62ff513db5a5c1ccafe` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/storage.rs | 30128 | `8649ce51069b9f17d2997b8560cf9833318656eb39b235ade33f2d52fe56058d` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/testutils.rs | 42030 | `6b93fa0b1f7870bd91b6f1dda6e6d8d3f107d4f26dcdb14f823cde60f287d174` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/vm.rs | 25112 | `42618857ff314631dfd45464af3cc0cd5264092fc06507573da4c602a90c0ee6` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/vm/dispatch.rs | 13221 | `35209bf562e299ce3928b180192fc26c9c4c0d153a704cea89bc07571dc05a22` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/vm/fuel_refillable.rs | 2310 | `b8e65b7971534028a2e4f2e865653cee23252a4b750ba5c9da35071b7b1cb110` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/vm/func_info.rs | 6264 | `e40e04935448d357b02cc5173d1762d1cfdda7095e11f292537a198fcae07693` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/vm/module_cache.rs | 6323 | `6c5b859414e70df2618179e7f89ef040ae39dbc9f6800344e0fdf9a00286ed97` | 0 |
| src/rust/soroban/p22/soroban-env-host/src/vm/parsed_module.rs | 24800 | `74bc0de4aac74fb8282427137f5465a06da7db8c93b25119e306f519eee2327a` | 0 |
| src/rust/soroban/p22/soroban-env-macros/Cargo.toml | 736 | `d833e8b411fd3f88761e5f9cdee0b508b8984887deb703d07fb61c11a427381b` | 0 |
| src/rust/soroban/p22/soroban-env-macros/src/call_macro_with_all_host_functions.rs | 5354 | `44cc078e72635e4869c16316e5d11c1aed11a61f3906fcccf51a058b96fadb18` | 0 |
| src/rust/soroban/p22/soroban-env-macros/src/lib.rs | 7835 | `be18403225dc7bf00b2b985ca69e03d0c35f11899fdb0035f83ebb5c89a7abcd` | 0 |
| src/rust/soroban/p22/soroban-env-macros/src/path.rs | 561 | `6d186fe3120e11b1deb22d5faa6005b68ded100c76cfde483d729fe8ea15c813` | 0 |
| src/rust/soroban/p22/soroban-env-macros/src/synth_wasm_expr_type.rs | 12311 | `350dc56852495c24af799b1398a490f31eba313fc273a106a6997c346b96ed0f` | 0 |
| src/rust/soroban/p22/soroban-simulation/Cargo.toml | 1038 | `27262a641816f5cb55cfd7a8af64eb26229685dc2b4b130e3b5dfac837eac8e7` | 0 |
| src/rust/soroban/p22/soroban-simulation/src/lib.rs | 305 | `e57b2acb367061d89eff1f0912a5d704118ed99fbb21f519d9f07587b4a31808` | 0 |
| src/rust/soroban/p22/soroban-simulation/src/network_config.rs | 6131 | `7d89326e97b6ef25d5d4bb8774502b4979634c25272516cd6b674094ff652c45` | 0 |
| src/rust/soroban/p22/soroban-simulation/src/resources.rs | 12351 | `cb4c45866e7b80e590a542d96cc2b163500aabf4c66fa9c6c35b5cba681248e8` | 0 |
| src/rust/soroban/p22/soroban-simulation/src/simulation.rs | 14279 | `1c49e7268cdddd6f7b2e57eeabc29dc58c0f5bca97a917583651158a8ac8e4f4` | 0 |
| src/rust/soroban/p22/soroban-simulation/src/snapshot_source.rs | 10988 | `f491f1dc868e10849ad7102d8728f04efed8a015a0fc64d889abd46a79f4eb81` | 0 |
| src/rust/soroban/p22/soroban-simulation/src/testutils.rs | 3565 | `e6f3646ea375d2593b0b8b6854a8308e26b35541ecabbcde5948ac8602658baa` | 0 |
| src/rust/soroban/p22/soroban-synth-wasm/Cargo.toml | 809 | `716d98debb3338990d4d706eec504fc8dea0bad1f4a52626eae0da6e4ae138be` | 0 |
| src/rust/soroban/p22/soroban-synth-wasm/src/expr.rs | 3370 | `20abb89282b4fcc30d85aa162b3edf8c49cd59a5d90ebc6bfd6ae6a24eacc3cd` | 0 |
| src/rust/soroban/p22/soroban-synth-wasm/src/func_emitter.rs | 15938 | `38d2d41444363114390bd9272701b0441a27402584df4983a08e075b7b9440e2` | 0 |
| src/rust/soroban/p22/soroban-synth-wasm/src/host_funcs.rs | 3101 | `92915e01ca0f79e0254df9d102417c9a14dbb8ad39fa28c3de967b5f20876832` | 0 |
| src/rust/soroban/p22/soroban-synth-wasm/src/lib.rs | 1130 | `b94fdbd1d86e3438c269123a6f6c9426e0791bf3b60d81d7b0b40dceb9544328` | 0 |
| src/rust/soroban/p22/soroban-synth-wasm/src/mod_emitter.rs | 16665 | `eaf741f708b56774732766ea18231cc362be46ed44d95fa155e869e211fa59ee` | 0 |
| src/rust/soroban/p22/soroban-test-wasms/Cargo.toml | 241 | `6eef4c0875ef4d266d255a5f5c6bdfee377c1d347b4f7e5418f6ee1134739280` | 0 |
| src/rust/soroban/p22/soroban-test-wasms/src/lib.rs | 7339 | `a5981963857f9c618872d5fa29fa8ee64f6c2e7b291a8190581b9db5b97a99d6` | 0 |
| src/rust/soroban/p22/soroban-test-wasms/wasm-workspace/Cargo.lock | 40888 | `8d43ccf3f32e2154847ee27407fd3fddd4e7a8fe57e13e6ffa28f9273dfb0070` | 0 |
| src/rust/soroban/p22/soroban-test-wasms/wasm-workspace/Cargo.toml | 2631 | `9d712d50f54a546e9507d36fe8f0d2f00682383c53343f25436be5392d7c9427` | 0 |
| src/rust/soroban/p22/soroban-test-wasms/wasm-workspace/add_f32/Cargo.toml | 398 | `57b505c9403f7350323dc9766db9276f9ac37f114ab4b2d6eaefbf0d536fa478` | 0 |
| src/rust/soroban/p22/soroban-test-wasms/wasm-workspace/add_f32/src/lib.rs | 336 | `099703bd2f3f4088add74ae0d0f900d1cddb16967d483ca76480bd37e5aaa525` | 0 |
| src/rust/soroban/p22/soroban-test-wasms/wasm-workspace/add_i32/Cargo.toml | 398 | `bf7cbb00090208bb631be314c43a23bd82873a766f44117e95b6d2d5119d05c0` | 0 |
| src/rust/soroban/p22/soroban-test-wasms/wasm-workspace/add_i32/src/lib.rs | 275 | `609f7db6583e31743bb9b6baa6d7f9f272b3d0f76cc9bc633244bdadc1ae7856` | 0 |
| src/rust/soroban/p22/soroban-test-wasms/wasm-workspace/alloc/Cargo.toml | 418 | `3481fa592be927a6bc916cfa97a4bbd6fc3882e17e707f5c44d573ab2afb989c` | 0 |
| src/rust/soroban/p22/soroban-test-wasms/wasm-workspace/alloc/src/lib.rs | 708 | `3ad94be5c06b55ed4639bb79f59be677ae9f8c38884bccb249bade8e7f4ad870` | 0 |
| src/rust/soroban/p22/soroban-test-wasms/wasm-workspace/auth/Cargo.toml | 401 | `584b31c30ce5b2c0068535098587c2685bc51509257afe979574448724e76910` | 0 |
| src/rust/soroban/p22/soroban-test-wasms/wasm-workspace/auth/src/lib.rs | 8544 | `2e0064ca991f83c3a00177f052bbc5c053087546ed1e42a944c7af810bb03621` | 0 |
| src/rust/soroban/p22/soroban-test-wasms/wasm-workspace/complex/Cargo.toml | 382 | `1012d55446546ce1bdd1548f8e09d7ee382b7c543f30b0d45802981774d00f1d` | 0 |
| src/rust/soroban/p22/soroban-test-wasms/wasm-workspace/complex/src/lib.rs | 1522 | `7fb764db8fd1ff735f0077daa0c0f8fbca952fb621075820dd741321a27b37d0` | 0 |
| src/rust/soroban/p22/soroban-test-wasms/wasm-workspace/conditional_account/Cargo.toml | 391 | `cd4b7a2986343e3a1dc896dc015aa7ef752d9eb493a2f7ccb2f72c9f30292df4` | 0 |
| src/rust/soroban/p22/soroban-test-wasms/wasm-workspace/conditional_account/src/lib.rs | 1190 | `8373ab257590bdc0023784bdcd8c465630ca631a1f820b1db1e6fb9b88fbf4ab` | 0 |
| src/rust/soroban/p22/soroban-test-wasms/wasm-workspace/constructor/Cargo.toml | 336 | `04400d2415e5853165f9065f83cc04e13b46aca4a16e40f324e5fd91db073fda` | 0 |
| src/rust/soroban/p22/soroban-test-wasms/wasm-workspace/constructor/src/lib.rs | 1058 | `c423ed6d892c0286acc21a9fb78cb7bb159b247dce09c5c9b01b29cdcc246d76` | 0 |
| src/rust/soroban/p22/soroban-test-wasms/wasm-workspace/constructor_with_result/Cargo.toml | 348 | `4fb215713599effb42c76ea0af475dcdb7d617c5b5740c9fefeba379c3f13e02` | 0 |
| src/rust/soroban/p22/soroban-test-wasms/wasm-workspace/constructor_with_result/src/lib.rs | 621 | `32a1d47c7d3c10309b7aba51b7ac5138c80adcbed19b0726950c05b8946cf72d` | 0 |
| src/rust/soroban/p22/soroban-test-wasms/wasm-workspace/constructor_with_return_value/Cargo.toml | 354 | `635d9450eab0b554b978ec65656f52272cd54652d2b6a218a995b8955fb6dbad` | 0 |
| src/rust/soroban/p22/soroban-test-wasms/wasm-workspace/constructor_with_return_value/src/lib.rs | 234 | `c30ae802d69000e032c778d0558e7a3cd1fc93750e69f617a27d5a281b812522` | 0 |
| src/rust/soroban/p22/soroban-test-wasms/wasm-workspace/contract_data/Cargo.toml | 426 | `eea0cfb3398a8905b1c749d382010df92150da82a86208562c54c29f26ec44ca` | 0 |
| src/rust/soroban/p22/soroban-test-wasms/wasm-workspace/contract_data/src/lib.rs | 2543 | `6c0338d09518eb380e996f7ea007f5f50a9f3c6d37b1e2a26913622e71aec0d8` | 0 |
| src/rust/soroban/p22/soroban-test-wasms/wasm-workspace/contract_sac_transfer/Cargo.toml | 388 | `9b4d6396f0ffd2ed7d6cc30886dc66142ddab1b795a7e2880df933a6867df109` | 0 |
| src/rust/soroban/p22/soroban-test-wasms/wasm-workspace/contract_sac_transfer/src/lib.rs | 516 | `3ea0c5d8a73c364a635b1c2679bfa610ac657642451bc639f6dc5ff4c16020ba` | 0 |
| src/rust/soroban/p22/soroban-test-wasms/wasm-workspace/create_contract/Cargo.toml | 406 | `acfd5c14bf5d848c890dbed7d59f09438e497f3fb0b94558c7825395a2f30e93` | 0 |
| src/rust/soroban/p22/soroban-test-wasms/wasm-workspace/create_contract/src/lib.rs | 419 | `d999ae4431e2cca2ff8500a042c58581208a70775eada7264e8985de95b11138` | 0 |
| src/rust/soroban/p22/soroban-test-wasms/wasm-workspace/custom_account_context/Cargo.toml | 394 | `30f6797a3894265f91a91dd4553219eb984b3b619fe928c1fc58b083b1c5eeeb` | 0 |
| src/rust/soroban/p22/soroban-test-wasms/wasm-workspace/custom_account_context/src/lib.rs | 601 | `b657abdf54831ee754ff23623c5de4d0723013371aa201838112bc49df3bfb45` | 0 |
| src/rust/soroban/p22/soroban-test-wasms/wasm-workspace/delegated_account/Cargo.toml | 389 | `775e8481ca0f918a0b3cecf8f72d3334f9e9ecafa7976cdf73c483b7d6480438` | 0 |
| src/rust/soroban/p22/soroban-test-wasms/wasm-workspace/delegated_account/src/lib.rs | 868 | `36ad27bafba63f3f84003fc542a5ea676ae40bd5cf95d76532fcbf15f57c64e2` | 0 |
| src/rust/soroban/p22/soroban-test-wasms/wasm-workspace/deployer/Cargo.toml | 333 | `ffac8815e6d766ee6503c586199ad9e737532fb2986e799c63be683baacdc544` | 0 |
| src/rust/soroban/p22/soroban-test-wasms/wasm-workspace/deployer/src/lib.rs | 1873 | `ade03dfecc57c2a865c94f0e96203aae80eb6b5a081827a7247768a55fd561cc` | 0 |
| src/rust/soroban/p22/soroban-test-wasms/wasm-workspace/deployer_with_constructor/Cargo.toml | 350 | `ed79e616e63b073c37083f4b2c06110abfa593f633187a14be2d1bb283190364` | 0 |
| src/rust/soroban/p22/soroban-test-wasms/wasm-workspace/deployer_with_constructor/src/lib.rs | 5011 | `7648828e97d74ed7ece814fa105f4ad2bbff85acc1e599b62e3d5923a24aea54` | 0 |
| src/rust/soroban/p22/soroban-test-wasms/wasm-workspace/err/Cargo.toml | 394 | `1199ec7e73ed605a36cec60abcf9e764efa1647a15bb70d752f5e6e7b41fd296` | 0 |
| src/rust/soroban/p22/soroban-test-wasms/wasm-workspace/err/src/lib.rs | 2881 | `6d421da68d5bcfb4dec07757387e48833cb5f3bbe6ce99dfd8730a08605aed23` | 0 |
| src/rust/soroban/p22/soroban-test-wasms/wasm-workspace/fannkuch/Cargo.toml | 399 | `671e27d1ef8a0fb4484973c5078c52a733411f1691f3ac81244ba436511d6346` | 0 |
| src/rust/soroban/p22/soroban-test-wasms/wasm-workspace/fannkuch/src/lib.rs | 2236 | `f8af8a42fd6fc33fde15a97091e4382bba5c851e44210cf3a840f70d8ef81c97` | 0 |
| src/rust/soroban/p22/soroban-test-wasms/wasm-workspace/fib/Cargo.toml | 394 | `ab3b6ac2010d7fb21193c223de82c9de425ac203ba5dade839346faf4ebe16a9` | 0 |
| src/rust/soroban/p22/soroban-test-wasms/wasm-workspace/fib/src/lib.rs | 268 | `c957875f4c1b35d053c3b2d746bcf748667913f12e33be6e03d244b537521d84` | 0 |
| src/rust/soroban/p22/soroban-test-wasms/wasm-workspace/hostile/Cargo.toml | 398 | `2fd054cecd1e274843d7646455d52e12387ffb57d1d5d7b2944e00d3731ba617` | 0 |
| src/rust/soroban/p22/soroban-test-wasms/wasm-workspace/hostile/src/lib.rs | 3124 | `c2eedf2f69c9f8cefbcf0e12967b76413d1b42e347f6478c221e8b294c6227f9` | 0 |
| src/rust/soroban/p22/soroban-test-wasms/wasm-workspace/hostile_large_val/Cargo.toml | 400 | `84c37ed639216b8696c0ca335098408978497b3f9b10fd5fc02f0d13eb260dc0` | 0 |
| src/rust/soroban/p22/soroban-test-wasms/wasm-workspace/hostile_large_val/src/lib.rs | 2553 | `dbf1d00afd9f5f62c0bab4a4e51114fb876585262f8da8af1f030f04031d9a02` | 0 |
| src/rust/soroban/p22/soroban-test-wasms/wasm-workspace/invoke_contract/Cargo.toml | 406 | `ef18142c281c7be0329a7a73a35bbac9682cedc8ddeb6fc59c7fd97fd346132b` | 0 |
| src/rust/soroban/p22/soroban-test-wasms/wasm-workspace/invoke_contract/src/lib.rs | 1943 | `331251706eeb7ca4c8f64877b2f4e2176b7195299989a6271db21db3c0a70357` | 0 |
| src/rust/soroban/p22/soroban-test-wasms/wasm-workspace/linear_memory/Cargo.toml | 388 | `68fcd3be1c41a4d6976d07965387ffcfe8f5245840cb44d0f41737caf7a4a02e` | 0 |
| src/rust/soroban/p22/soroban-test-wasms/wasm-workspace/linear_memory/src/lib.rs | 2861 | `998f890f085a31c269dee25aa5ac3eef9a62efc4166d2d26377073eab3574a3d` | 0 |
| src/rust/soroban/p22/soroban-test-wasms/wasm-workspace/loadgen/Cargo.toml | 382 | `ad44b1176d45c730d89e27b0ad3fab9da047ba3c7ca403bebe5578146e3b0db5` | 0 |
| src/rust/soroban/p22/soroban-test-wasms/wasm-workspace/loadgen/src/lib.rs | 1370 | `44d808454841cb78617330c260c6fe73b5fb13b095c15c88bc117a9787f6c664` | 0 |
| src/rust/soroban/p22/soroban-test-wasms/wasm-workspace/no_arg_constructor/Cargo.toml | 343 | `377b43e2b9fd73dbe73f71b6a58210f4ff872d9450da339fa7e74cd0525563cc` | 0 |
| src/rust/soroban/p22/soroban-test-wasms/wasm-workspace/no_arg_constructor/src/lib.rs | 696 | `f49c7035942d9351dde370ed4ea4e00698f76f66f2cee13079ccc0636acdc413` | 0 |
| src/rust/soroban/p22/soroban-test-wasms/wasm-workspace/recursive_account/Cargo.toml | 375 | `aa8e4f9caf805a878a44d89cc8b4f1023a146ccb235467257b69a9d151d6b939` | 0 |
| src/rust/soroban/p22/soroban-test-wasms/wasm-workspace/recursive_account/src/lib.rs | 1819 | `99df3ded80c336870ed36935ca34af8306c1644bcc127f8adee9e6cb26ff2a24` | 0 |
| src/rust/soroban/p22/soroban-test-wasms/wasm-workspace/sac_reentry_account/Cargo.toml | 386 | `90859f5d2e828c0dfae664526a298218c3225f629ace5d27309e1296b55ab7e9` | 0 |
| src/rust/soroban/p22/soroban-test-wasms/wasm-workspace/sac_reentry_account/src/lib.rs | 1176 | `44c4a73769a6db79991b2b981560e4c62df6a07a5a467550c8995f5333af2164` | 0 |
| src/rust/soroban/p22/soroban-test-wasms/wasm-workspace/simple_account/Cargo.toml | 389 | `b4146ef0490991bc020fec1529ab9cf7abd8a1e0c9278f57fbd1c214652e3111` | 0 |
| src/rust/soroban/p22/soroban-test-wasms/wasm-workspace/simple_account/src/lib.rs | 948 | `7c74cf48ea7db5ed1ff209926ba7d98ba4c32127d9e52e229a3c90eedfed4e28` | 0 |
| src/rust/soroban/p22/soroban-test-wasms/wasm-workspace/sum_i32/Cargo.toml | 398 | `fceccbc33a828ebda7dd4aace444eb8a5b508ed79907b7478dc1ac3fbbe111b1` | 0 |
| src/rust/soroban/p22/soroban-test-wasms/wasm-workspace/sum_i32/src/lib.rs | 561 | `4b1c69bf2e59646c6202ce0e9e460a7d22eea3490e517ecc4f56cfc8e4b8f49b` | 0 |
| src/rust/soroban/p22/soroban-test-wasms/wasm-workspace/update/Cargo.toml | 410 | `7e3d997807ffbc354ffd26c1556458e6776aa98dbf978d05256b5e395289f02a` | 0 |
| src/rust/soroban/p22/soroban-test-wasms/wasm-workspace/update/src/lib.rs | 945 | `d0ae9d5190e0f6251ee7182be9c052e068695ed305c7666caf4b455789c72c93` | 0 |
| src/rust/soroban/p22/soroban-test-wasms/wasm-workspace/upload_contract/Cargo.toml | 406 | `79f437d05d1eb91269ba587ab4c1f40c5a76b3194864a16f55cb869f45bb5507` | 0 |
| src/rust/soroban/p22/soroban-test-wasms/wasm-workspace/upload_contract/src/lib.rs | 252 | `5033bb1c628243bdaecc55b1c7676b20b22f73fe4842905b5bb92a1a111061c9` | 0 |
| src/rust/soroban/p22/soroban-test-wasms/wasm-workspace/vec/Cargo.toml | 378 | `076d8806b4b214776eacf7e39cccb493b2db1b850e006ef73a6c33736ef8da4c` | 0 |
| src/rust/soroban/p22/soroban-test-wasms/wasm-workspace/vec/src/lib.rs | 346 | `a358381709762177476df8c9dcacdc6406e499b81de7523278f3fbf5212aa7d3` | 0 |
| src/rust/soroban/p22/soroban-test-wasms/wasm-workspace/write_upgrade_bytes/Cargo.toml | 419 | `dd1b71224963adf1942f76d1646e4740bea337536eb26da0ad22c651dc2bfc25` | 0 |
| src/rust/soroban/p22/soroban-test-wasms/wasm-workspace/write_upgrade_bytes/src/lib.rs | 1003 | `8a0cc6e5f77713ee726982d933260e90732e70873c0a2bb8cc662ec651472c6d` | 0 |
| src/rust/soroban/p23/.cargo/config.toml | 6685 | `deaae172a164fb2ba5bfa0e6b3658fc8ef043a348c861936762a8a210c213ca0` | 0 |
| src/rust/soroban/p23/Cargo.lock | 60639 | `1931574a5d1edfdf4f5331986283e516bc3426b44ef63bbbb369b4823957157e` | 0 |
| src/rust/soroban/p23/Cargo.toml | 1915 | `17327091d6624d381fed74b83aac32d14dfb7494b1a630743226225b90ae1c69` | 0 |
| src/rust/soroban/p23/rust-toolchain.toml | 369 | `a93034bc4702710436624ddc42e89325be59ebc8e584e7c58b9b6c00fc2d3b2d` | 0 |
| src/rust/soroban/p23/soroban-bench-utils/Cargo.toml | 787 | `2020e9795c6dc4edfee39f36f1d78cf16b954f69ac16f9cba453485985d4edd3` | 0 |
| src/rust/soroban/p23/soroban-bench-utils/src/lib.rs | 75 | `4ed9af88c90c8137a175e9b2e583a3076ef13bc4911e133e889aa6f559caeeab` | 0 |
| src/rust/soroban/p23/soroban-bench-utils/src/rusagev4.rs | 2027 | `e775f766b27fcece33febfaf91e1b2e46b4ff0d7028a326909fd910dd75c7b17` | 0 |
| src/rust/soroban/p23/soroban-bench-utils/src/tracker.rs | 5923 | `71df7e2a505682276058fba51644bfe0f0d59934c327b9f4bb14ee6d59a6f8b4` | 0 |
| src/rust/soroban/p23/soroban-builtin-sdk-macros/Cargo.toml | 554 | `828f2414d8e7d7ded5567797a4eae4cd132908234489fc5ef6d327e99fe29d32` | 0 |
| src/rust/soroban/p23/soroban-builtin-sdk-macros/src/derive_fn.rs | 2815 | `627430878da696e94b872adc29d71390e866277ee7acf6c1b42e7cdd2ccf15a0` | 0 |
| src/rust/soroban/p23/soroban-builtin-sdk-macros/src/derive_type.rs | 8525 | `459416267127d646b9d105c16c046b210eeb22cd4c482511f268d8396120f215` | 0 |
| src/rust/soroban/p23/soroban-builtin-sdk-macros/src/lib.rs | 1734 | `7120a6c227f456234536bfef7c7f9d82918a8c89d8c25f3f16eaccc404a79aad` | 0 |
| src/rust/soroban/p23/soroban-env-common/Cargo.toml | 1564 | `0f5adc80e188724943b19317d9385671b59ca6f14d482a3cf067f4daeab7d89c` | 0 |
| src/rust/soroban/p23/soroban-env-common/build.rs | 99 | `818b5844721186dd913412974faaff4bb45954e41b2cedeecb4b0a5ddcf90b35` | 0 |
| src/rust/soroban/p23/soroban-env-common/src/arbitrary.rs | 2047 | `aaebd099ab97097e1ac2482ac4c437c99736f75ca822cfdcec435ccf8b8fb662` | 0 |
| src/rust/soroban/p23/soroban-env-common/src/bytes.rs | 3066 | `768838872830e2352670e97ad9d9313c24db0efb8854847474739ed33c7c5735` | 0 |
| src/rust/soroban/p23/soroban-env-common/src/compare.rs | 7475 | `b0a0b3dfa266b7bb4952b7fe2d1919e1a78af240777114484bf82567d72d6704` | 0 |
| src/rust/soroban/p23/soroban-env-common/src/convert.rs | 19709 | `634ff85286ff9b9272102f06dac071534aff05d5733734a2220967a94dfd5fcb` | 0 |
| src/rust/soroban/p23/soroban-env-common/src/env.rs | 17843 | `348641178612a18f24636640b215b16388abe850a50655fecff5788c483d4877` | 0 |
| src/rust/soroban/p23/soroban-env-common/src/error.rs | 15600 | `efd9f516f411d55dd01a22e33f3418068d82c715290382e98a5cba4f58bdc46e` | 0 |
| src/rust/soroban/p23/soroban-env-common/src/hash.rs | 1501 | `15c9e63948d9ce9486581659f1aea95a08eb849416500a0a096f8d9d11ec1350` | 0 |
| src/rust/soroban/p23/soroban-env-common/src/lib.rs | 4160 | `fc0ab41b67c78d08d46944b045f75a5b1259895659dd758599deaf0a402f14ab` | 0 |
| src/rust/soroban/p23/soroban-env-common/src/meta.rs | 3279 | `62b2d10383f06d0a5a2d09941ccb27ad845048ad20913fe70b7c320f6c0bd56b` | 0 |
| src/rust/soroban/p23/soroban-env-common/src/num.rs | 14398 | `9242b8a3eeb918cbc602ecbb6e185b3d8bc6cacf27bb50d35c7aad767de5ff0c` | 0 |
| src/rust/soroban/p23/soroban-env-common/src/object.rs | 5970 | `b937c641ebab58af9bbbabab00a3351dac36d6937042b6eb1989eb32deb60318` | 0 |
| src/rust/soroban/p23/soroban-env-common/src/option.rs | 907 | `870a61869cabc46e32f50c93605686f4d66f1952bf89f596b8fbfdcaf5deb38e` | 0 |
| src/rust/soroban/p23/soroban-env-common/src/result.rs | 1261 | `d3210db790113cf7950e76c15492358ca9a469159f8dee2c27c2dee91228c4b0` | 0 |
| src/rust/soroban/p23/soroban-env-common/src/storage_type.rs | 1109 | `f6a406da19c791aeb5932a721bcea431eaad9ff0805199025796c6cf40e897c3` | 0 |
| src/rust/soroban/p23/soroban-env-common/src/string.rs | 2036 | `13ec3079a2f66e4affb3ecdeba15134f2941ef05076f544a195736dbd64bf8e9` | 0 |
| src/rust/soroban/p23/soroban-env-common/src/symbol.rs | 21416 | `535b8c4dc64fddc986e76d364ed319405f00e1f95bdf2fed02253fc1ecfab185` | 0 |
| src/rust/soroban/p23/soroban-env-common/src/tuple.rs | 4295 | `fed0d299699f9ad2f429f68199534af4b319cfbc960dfdf488e9dc943fae95ad` | 0 |
| src/rust/soroban/p23/soroban-env-common/src/val.rs | 30832 | `2528884f3114f81144f1a9a2cbdb0f7314ecc50070041c632b3ed75cdae5299b` | 0 |
| src/rust/soroban/p23/soroban-env-common/src/vmcaller_env.rs | 11584 | `a5de9e5baf5b6e2bdf9bed4051b635f22aa795be747a81e76cc816060dc33183` | 0 |
| src/rust/soroban/p23/soroban-env-common/src/wrapper_macros.rs | 12097 | `0228b5e35382d4dbca4b760f3f6a57d0a7ecbb9ffa897f16d445c82ce6e63e93` | 0 |
| src/rust/soroban/p23/soroban-env-guest/Cargo.toml | 625 | `65d7195e1ef69e1cba7c6aabd96072fe37482f0b1c7ecaeb17e17cc38b2ab937` | 0 |
| src/rust/soroban/p23/soroban-env-guest/src/guest.rs | 15156 | `ec9b060d0a83822824afbed9defc5c213d982019960a99ef613283baf851c6a1` | 0 |
| src/rust/soroban/p23/soroban-env-guest/src/lib.rs | 561 | `b34cdc92dbf3880bd463d0c82b7df5866ac88d74b8bc42d8a9321eb9104dcfdf` | 0 |
| src/rust/soroban/p23/soroban-env-host/Cargo.toml | 4911 | `555958b1e7d0ef5f6c54e7c7ff910fad2d756f8329408c384e7e69248a989f45` | 0 |
| src/rust/soroban/p23/soroban-env-host/build.rs | 283 | `f90c468c4ab2735a8edeca9f82ca31cf327a27fd8baf47f7417dab8653151005` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/auth.rs | 99466 | `230eed4674e3170751b1532c359154993a697307c51ef4251c782e6c0c494c81` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/bin/main.rs | 1503 | `9a76c921937802ea5e9c4017465e9dd471d2f933e928c4b0d559404ff8672845` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/budget.rs | 53692 | `277833a764520cce38b06c7023098716968b44c81850237c9bbb990c30d90b33` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/budget/dimension.rs | 6966 | `337bdb7857672f68b8e11ef76cf47107372c925930dd2c980e4409110ed613dc` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/budget/limits.rs | 4658 | `0080964f53ec49d2df64306354887cc5565b2628584e64548126a4b95e2eca1e` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/budget/model.rs | 5584 | `b6d99a8a793cd385cdcaaa7cd288d279b5628670ee34b7b83504a0276e982635` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/budget/util.rs | 7363 | `f652719196e0f9a290f6a597839191f89c858821ba2d79a06c9f04d1cf56a083` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/budget/wasmi_helper.rs | 4145 | `c7afc9c4c05a9ee57d0da858369312d9d0ba431bc337d02b98d750cfb4fbe0d0` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/builtin_contracts.rs | 560 | `f0bd26290068aff0d567b8e950c3abd9545b9f6fbb50a521001e21f9b3a7ed1e` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/builtin_contracts/account_contract.rs | 9309 | `370d6ab2b23e6e09199851d2fc77d033292ba49c4c14cc5bb71dad6f4fd6013f` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/builtin_contracts/base_types.rs | 13559 | `3c4d6c21676ab4b863536f10b7dc41615719161f97f025ce3fa9acfbd041295f` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/builtin_contracts/common_types.rs | 1225 | `69efad1515dfe980cf07c32fb08ec2697528171de6eaa4be800e7ecde5334dc6` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/builtin_contracts/contract_error.rs | 914 | `cfddfd3a20809a0c30d5d86f93135936780945aab909918f2e3d3351589310aa` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/builtin_contracts/invoker_contract_auth.rs | 6544 | `d0a8069c45de5a5cbef488726df63356cd81f09e1e32d23aed4a268bc42811df` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/builtin_contracts/stellar_asset_contract.rs | 248 | `944142447b113d671f1e47dc8a2d8191ef4ff11167b793f2a4c2f4d72efc8e4f` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/builtin_contracts/stellar_asset_contract/admin.rs | 704 | `ad70748dab976704bdf5fa87dfe30c0746280a24eb46c36a9c102aeb1f11980d` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/builtin_contracts/stellar_asset_contract/allowance.rs | 5082 | `533b7dde81bf6e70229d1e297aa1e8d6adb94eafd5ebe75c44c38ae179c9b36f` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/builtin_contracts/stellar_asset_contract/asset_info.rs | 3092 | `9a0583a6bec016f2822bc357baa2cce81c8e4ad3077fd8d5e2100172c0b22def` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/builtin_contracts/stellar_asset_contract/balance.rs | 29464 | `ffee339060c5e3857c0cac9708df112686d9af8fa2c4f781a66820f27f734c5c` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/builtin_contracts/stellar_asset_contract/contract.rs | 13122 | `d7601ef3510ec3d4591f207c4b544b29165ca2b0efc28ddcc22380434f6c491a` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/builtin_contracts/stellar_asset_contract/event.rs | 4403 | `125cc56ff663883f629520b9ea1fc1978527c61b86867063cd57cba7730b211c` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/builtin_contracts/stellar_asset_contract/metadata.rs | 6992 | `12ca5219bd19e98b81880a01e5fe99bfffaf1c5d283371bff34961763ac00331` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/builtin_contracts/stellar_asset_contract/public_types.rs | 1318 | `84834c2fec3c9763ba73d89fdd44db86da9a35400e82401cd5ba04ed03874026` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/builtin_contracts/stellar_asset_contract/storage_types.rs | 1113 | `655a0cec594b78db2eeccabfe03e27f2ae0537c65729e456b604cbbdb579f298` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/builtin_contracts/storage_utils.rs | 362 | `216d16572291ac021fd3ee7a0ce6d4b1810f8dbee07fc2791bbf32236a75ed10` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/builtin_contracts/testutils.rs | 12166 | `d7cfa0520c24dc9360d9126071f8ef48b88103196b29726dc9571cdc181c9af0` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/cost_runner/cost_types/bls12_381.rs | 10204 | `965dff98b1d17f2c58dd07697781db1c8033193651fb14d4473b091fb6ab43c4` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/cost_runner/cost_types/compute_ed25519_pubkey.rs | 952 | `c679365a8825299630452cf28daf21f4e6cff1805ca06910bc4ce49300d04a7c` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/cost_runner/cost_types/compute_keccak256_hash.rs | 916 | `c70f481dcea5eba30a4ae54ea476efec3fb3bf938d15987042aaeac222bbef3d` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/cost_runner/cost_types/compute_sha256_hash.rs | 896 | `99eece10c8e2379a0d3675f618b6c9192a57ddd98bc0063cc886ab22d526b509` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/cost_runner/cost_types/decode_ecdsa_curve256_sig.rs | 1407 | `6eae776ff6b8ee070b6d51f70a4b231bf78c2bd0e964c0cae695be06a66b251e` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/cost_runner/cost_types/host_mem_alloc.rs | 951 | `53bd536e402308f09e0ead2a7825d8a7a88c6da46f0deb55ddce336d6a754a32` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/cost_runner/cost_types/host_mem_cmp.rs | 957 | `db2b390ce0892f2b450a9707d8f3d54a9fe2438d88f73ae021263dc18b266a3c` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/cost_runner/cost_types/host_mem_cpy.rs | 821 | `7ab8627489d5882ca2725d3e5872dc5cf3907890341065e5fa9149b121f11316` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/cost_runner/cost_types/invoke.rs | 2183 | `451a7818021ac77658771411708fe709c328f8d29abb0906720cd4da4fbb069d` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/cost_runner/cost_types/mod.rs | 983 | `0e319de5bfa8eeafbc2f98d9187c31084ba8ae0755533496d9b3563ee62b3c43` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/cost_runner/cost_types/num_ops.rs | 1546 | `cf08647785a4ede49183258e305e4520b3db286536bf2a6e71583e76c89be32b` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/cost_runner/cost_types/prng.rs | 1003 | `fac74f446f916302d6b27d59040ae6c72aa4decbfe766a862f9b0a2dceb75223` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/cost_runner/cost_types/recover_ecdsa_secp256k1_key.rs | 1140 | `21256191032a43cd2584275eebae7e034db553ee6c90c16d6ba5e5e2392eb69a` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/cost_runner/cost_types/sec1_decode_point_uncompressed.rs | 1155 | `06fda4cc5f09ca513953f45424b1aa5277fb1fa0805e598e63466ea6b45d1863` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/cost_runner/cost_types/val_deser.rs | 800 | `19b4abd59908d36bc2c1a2d7e05fc67db21df215cf02bcf91ff42d760f18e6d0` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/cost_runner/cost_types/val_ser.rs | 1385 | `2b3aa6b23feb1d99fdfc267146458eba577e8641124c8673a606fa0cb976b08e` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/cost_runner/cost_types/verify_ecdsa_secp256r1_sig.rs | 1124 | `8b1e249924c8f329e563122f8e2c1d0e60fbc6c788de70c0dd4e9aeaf8f8b833` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/cost_runner/cost_types/verify_ed25519_sig.rs | 1079 | `da86df368d3cdc769f57e48a6fd160ba5c7f1dab0a44876587875be1167215bc` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/cost_runner/cost_types/visit_object.rs | 1056 | `c66e1ae7580a923564f8694f34d3ee9ff4c3de2b768529cf75a9f86e23c9c656` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/cost_runner/cost_types/vm_ops.rs | 8989 | `3a7c74abaa9d8e628d3bc586d8b3056218a8a234bd8e4f35857e186cb4fcc135` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/cost_runner/cost_types/wasm_insn_exec.rs | 9902 | `2c3bfc08db067c5d0320dfbbb55d477019e282d7c7a4d4c6c1c704b47a6b2983` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/cost_runner/experimental/bls12_381.rs | 6378 | `154aed6d61b073065304ff1b68dd8eb3709a82108a7983d23a44cb01cb744ac1` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/cost_runner/experimental/decode_secp256r1_sig.rs | 1472 | `2f7bf5f395b05ad7ae9ab37e404eae4c3bfa85d29eaa8d08becfcfef825b0a1e` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/cost_runner/experimental/ecdsa_secp256k1_verify.rs | 1487 | `d5d2bdc6133fc64cdbe0765a2d5ee6069a9cfedb8b03943dff269770d30b88c6` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/cost_runner/experimental/ecdsa_secp256r1_recover.rs | 1499 | `2e4920ce9df183016f9bf4765bde45f76b746f34d636b03d21647e8ee7bfb7f3` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/cost_runner/experimental/ed25519_scalar_mut.rs | 1353 | `5b0755082fbcd387ee756a4fcb85b19abb7f632aabefddae79063463cd81b480` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/cost_runner/experimental/map_ops.rs | 1005 | `5feb978d228ff705dcee86bb90cedaa328dfa196c6fdbbfc48468d6dfbd8cd74` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/cost_runner/experimental/mod.rs | 2700 | `cc07f061fc69b5348c5cb1e8dbaaad46f4b06ff7a396245618d954e98d4c77cd` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/cost_runner/experimental/read_xdr.rs | 1388 | `476f11215c5a4bdcebe94772688e45f28d96db4f5dfe4da029507cd01d4f3f3f` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/cost_runner/experimental/sec1_decode_point_compressed.rs | 1756 | `299089e64c18ca9c4414a6461eaf023cbcfdbdca24db9f55edbf28f922771643` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/cost_runner/experimental/vec_ops.rs | 1132 | `8116fc7fe3f8d9259a9a98a719f9a8a67d96e2159db1644fc1e14cf352aaae48` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/cost_runner/experimental/vm_ops.rs | 2196 | `a253e366b149b7583c7e48b3aff4a982fca99e0194b526c5276fcaa81253323a` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/cost_runner/mod.rs | 787 | `d8b4f3f225b31efed2489ac70a610d6a774514944bdbb5645431e9cfef8251e3` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/cost_runner/runner.rs | 4203 | `98f216ef92f42ce6364d6aa13cffcc33a6da9fa344469ebe0b7093614ca71fc7` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/cost_runner/util.rs | 4774 | `9cbbfe0c50bd607d1d879a9968fdd5ec69ae096faa34216a7bbbe7986e2bc57c` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/crypto/bls12_381.rs | 32386 | `53570a02f948b812a40b6ebf41054c842020a8c968639867c4a6d96508e4a136` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/crypto/mod.rs | 13040 | `ccbe1563db40bf085dacdc7d468d0ac5b3230274e1ac237509c81868c8af8411` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/e2e_invoke.rs | 45273 | `edb371aed251cd24236eb363f4ed427b74c696b105acf0d1fb59c2af80ca7932` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/e2e_testutils.rs | 11747 | `1e004e07778f6c0c921cb36f95e400435e6d59062a9f9f1663cd5cd80aa321bc` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/events/diagnostic.rs | 5750 | `a66118d5747c50c89b1c7e1fa859b6b43b91f10add59353f274b115e3a171776` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/events/internal.rs | 10946 | `1bbfaa4dbdb10c8d256d8a7722473da598b3d543b8bd7e07e20b55b198d34028` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/events/mod.rs | 9153 | `f9ad2d0f0c9e9fc74885433e1bafd8a3045f499176a4fb44c339ecb2fc0c0742` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/events/system_events.rs | 1356 | `126b8da42733be7deea23b239008eeca261828c191862f26be1d759b82422f53` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/fees.rs | 15746 | `b34056e45639409f8f8c541ddaaf6cb938ddfa22e6b803fe1b3c4df55fb38d4e` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/host.rs | 130206 | `dd8dca6842b629472a485534ac251b5707490b7f6233e016bbd0d3c9bc85236f` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/host/comparison.rs | 28373 | `573aa99e9e84a6ddf2bc1accec5e37eee08f0aec684bdf51a95345bda7813a55` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/host/conversion.rs | 22920 | `21e5177bdf0829dfb68774dce0d65c5c59f7b943c8216e97077cd7d46bb4b2fc` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/host/data_helper.rs | 23170 | `3ac29082e2e080b69fb24e2f3aea74b3869f9a9aa31720108608ab1d2fc348af` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/host/declared_size.rs | 37447 | `983113ec62422a9e1b08b2afbeb55b186622905bef556bde1232872f14750eb9` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/host/error.rs | 17247 | `5bdd44a03a3285c577b2af97db5d8033f07c565b52bb68ebc98691e8cd5a059d` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/host/frame.rs | 47758 | `9928337941a5e6023d6f952b06efee2175411d6bab7ecda79b85f1fbc8f4fade` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/host/invocation_metering.rs | 36975 | `0bca03bce199cd59053e231b52066f3f8ffe6fda7c12a63115624e0dd6363559` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/host/ledger_info_helper.rs | 1502 | `9144a723b7119e868776cb21260b2f44ce286bc6a6485ada29c6133fc71e33ae` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/host/lifecycle.rs | 15195 | `cb31f0596303414d26cdea9a170a5478336e789187871dbd2f9256a57645d8ca` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/host/mem_helper.rs | 18165 | `d178c7f39d95b245e33ae8bef94b381944191c9a899edee4640db6c6d21e77d5` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/host/metered_clone.rs | 25638 | `43de045d53cf824b83407c440275bf9d7498f0f9e5fbd6be04629889f92cc3a6` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/host/metered_hash.rs | 2482 | `3792f8eea8df5b983fb363b0a282f8e91e3b7dfca5a424484cb5d3e0ae5c056b` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/host/metered_map.rs | 14312 | `4364aece444234a7bc31ee7b0ca33e251a48a5283a1e8ae465fda1ebae7f35db` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/host/metered_vector.rs | 14304 | `b872b5c595424df07bd377fa16ba3d5e10d43109bf66fe2420286c9f2bf847ce` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/host/metered_xdr.rs | 2650 | `22e70db0f290b025fb1e992b230564210a7b315c9ea7dca1e3e28609c64b7a52` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/host/num.rs | 2933 | `e188fe8582e1ff99f1ed9123e6f30bbd3903c89c6ba3d31644c1d7a3c1e983df` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/host/prng.rs | 8157 | `eeed1bff44661301241a4bd31c87705cc202eb8efd829763646947091bb6de39` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/host/trace.rs | 13265 | `2796b32ae451304e5239b4ca1493c03d8ec5d9b692dd5b1755d898cc5209bd31` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/host/trace/fmt.rs | 7968 | `cd88957494c05f14961fccbd99707a506a08cd246ec6d063ff1fb1a1c252fd7d` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/host/validity.rs | 1818 | `b5c6baa004d08a398e6553f5336c5c1dc2ccb099dfdc0ed708ed967147c883d5` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/host_object.rs | 21487 | `1bd3907c903587b2854f7ff05f8326f19a72ed51970e436cb2b8f19f5b6474d1` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/ledger_info.rs | 1348 | `5a7d202b945c0e639624746f926040eb873f640217652d55fb68fbc5acfb1f4c` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/lib.rs | 2180 | `66a4ba6676268b0bcd59c1fb00a29f07e6c19b021e45244932a01a415f0247be` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/macros.rs | 3069 | `40406f573892430b2bdfce358923e0cd47bd06e0c2ab7d472a15f09b9a06b57d` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/storage.rs | 29990 | `5b05f3c0062dae790d1f9c06971f9ed36ebc6876c6bdf691d6bdbe5797d30bcc` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/testutils.rs | 42213 | `987c1309fba500c5b9168c4ad3d3aad0577688299de0cbf82a314c7c62aaed92` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/vm.rs | 20025 | `459a4c1e5805bb10bcd2e0a85ba58cd580e57ed64c49f196a86c1f77fe3a5c4a` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/vm/dispatch.rs | 13315 | `8f4f99793318ced48d810a380213945cd50f4f92992ae2baab7cb913f8f0e404` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/vm/fuel_refillable.rs | 2310 | `b8e65b7971534028a2e4f2e865653cee23252a4b750ba5c9da35071b7b1cb110` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/vm/func_info.rs | 6266 | `80fa97bf3e4b23155b0d52e9694d3f3351f2109f61b7a2bdf1df591f4df0d579` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/vm/module_cache.rs | 7540 | `f76b737e4f6a91bc8f7a9b75ac19c08020bc51f8aec27dbcc44e275924c6eab6` | 0 |
| src/rust/soroban/p23/soroban-env-host/src/vm/parsed_module.rs | 31359 | `cba6264ca734976cdffeded7ee037eaa3ae9e2869ce75f288318bb8567c5bd34` | 0 |
| src/rust/soroban/p23/soroban-env-macros/Cargo.toml | 736 | `d833e8b411fd3f88761e5f9cdee0b508b8984887deb703d07fb61c11a427381b` | 0 |
| src/rust/soroban/p23/soroban-env-macros/src/call_macro_with_all_host_functions.rs | 5354 | `44cc078e72635e4869c16316e5d11c1aed11a61f3906fcccf51a058b96fadb18` | 0 |
| src/rust/soroban/p23/soroban-env-macros/src/lib.rs | 7835 | `e3cdc9f1cf9206c5fa4562349916bf8b56c08f7494da2020f886db2326800f43` | 0 |
| src/rust/soroban/p23/soroban-env-macros/src/path.rs | 561 | `6d186fe3120e11b1deb22d5faa6005b68ded100c76cfde483d729fe8ea15c813` | 0 |
| src/rust/soroban/p23/soroban-env-macros/src/synth_wasm_expr_type.rs | 12311 | `350dc56852495c24af799b1398a490f31eba313fc273a106a6997c346b96ed0f` | 0 |
| src/rust/soroban/p23/soroban-simulation/Cargo.toml | 1055 | `f433950b59bf4790021894ef1c16e9aa6750a68e095bdfbbd7d45479713917a5` | 0 |
| src/rust/soroban/p23/soroban-simulation/src/lib.rs | 253 | `c554a9c4dc9655d33e65137f3e6b8f1335b256da59ea5460150c8b4e37b3b752` | 0 |
| src/rust/soroban/p23/soroban-simulation/src/network_config.rs | 6694 | `4c58115a603c918557b85d3693866e0792506648ef32b475449bd48cce5b113b` | 0 |
| src/rust/soroban/p23/soroban-simulation/src/resources.rs | 12449 | `dbfb46469d7539d86911d8487aaf303b365de52c38fc62e383274b3b4534921c` | 0 |
| src/rust/soroban/p23/soroban-simulation/src/simulation.rs | 15415 | `7278d70854bd6bed517560045aa282014568533401e5965b8d71813c5f3f40b7` | 0 |
| src/rust/soroban/p23/soroban-simulation/src/snapshot_source.rs | 9727 | `bb6febacc3e5729108305606c7724931ccc7ef67db9806f2b17f0097810e387c` | 0 |
| src/rust/soroban/p23/soroban-simulation/src/testutils.rs | 2772 | `6e1089e18f46f0b0403c6dd304307dd1debe481701574a306621e1654d1752aa` | 0 |
| src/rust/soroban/p23/soroban-synth-wasm/Cargo.toml | 809 | `716d98debb3338990d4d706eec504fc8dea0bad1f4a52626eae0da6e4ae138be` | 0 |
| src/rust/soroban/p23/soroban-synth-wasm/src/expr.rs | 3370 | `20abb89282b4fcc30d85aa162b3edf8c49cd59a5d90ebc6bfd6ae6a24eacc3cd` | 0 |
| src/rust/soroban/p23/soroban-synth-wasm/src/func_emitter.rs | 15938 | `38d2d41444363114390bd9272701b0441a27402584df4983a08e075b7b9440e2` | 0 |
| src/rust/soroban/p23/soroban-synth-wasm/src/host_funcs.rs | 3101 | `92915e01ca0f79e0254df9d102417c9a14dbb8ad39fa28c3de967b5f20876832` | 0 |
| src/rust/soroban/p23/soroban-synth-wasm/src/lib.rs | 1130 | `b94fdbd1d86e3438c269123a6f6c9426e0791bf3b60d81d7b0b40dceb9544328` | 0 |
| src/rust/soroban/p23/soroban-synth-wasm/src/mod_emitter.rs | 16665 | `eaf741f708b56774732766ea18231cc362be46ed44d95fa155e869e211fa59ee` | 0 |
| src/rust/soroban/p23/soroban-test-wasms/Cargo.toml | 241 | `6eef4c0875ef4d266d255a5f5c6bdfee377c1d347b4f7e5418f6ee1134739280` | 0 |
| src/rust/soroban/p23/soroban-test-wasms/src/lib.rs | 7866 | `af766c96a7fd0327fcb9a16d17ce4b2c62b701a3cbbb52baa5d08147734ff32d` | 0 |
| src/rust/soroban/p23/soroban-test-wasms/wasm-workspace/Cargo.lock | 42158 | `4cd2fca0c846762ec3ac09e1185ce3e4e5c12774355b2c8bc72d8a6c6043e177` | 0 |
| src/rust/soroban/p23/soroban-test-wasms/wasm-workspace/Cargo.toml | 2678 | `1bcd62f70b2087b1a7e601f453238ef41ba10b75212678570d3edbc76d3f362f` | 0 |
| src/rust/soroban/p23/soroban-test-wasms/wasm-workspace/add_f32/Cargo.toml | 309 | `549e4c2516c26da535fbc0adede29e1e326c418737f90a536b6edb4059bd3eb2` | 0 |
| src/rust/soroban/p23/soroban-test-wasms/wasm-workspace/add_f32/src/lib.rs | 336 | `099703bd2f3f4088add74ae0d0f900d1cddb16967d483ca76480bd37e5aaa525` | 0 |
| src/rust/soroban/p23/soroban-test-wasms/wasm-workspace/add_i32/Cargo.toml | 309 | `dd8f899b62614dd9aa7b485eb5de3b02b65c0f341c828e7c86fa01c0ef893d9f` | 0 |
| src/rust/soroban/p23/soroban-test-wasms/wasm-workspace/add_i32/src/lib.rs | 275 | `609f7db6583e31743bb9b6baa6d7f9f272b3d0f76cc9bc633244bdadc1ae7856` | 0 |
| src/rust/soroban/p23/soroban-test-wasms/wasm-workspace/alloc/Cargo.toml | 329 | `01be473ad078fed7227bf22ed802501063bdc72f25c1e4a53c69972e9c68ee18` | 0 |
| src/rust/soroban/p23/soroban-test-wasms/wasm-workspace/alloc/src/lib.rs | 708 | `3ad94be5c06b55ed4639bb79f59be677ae9f8c38884bccb249bade8e7f4ad870` | 0 |
| src/rust/soroban/p23/soroban-test-wasms/wasm-workspace/auth/Cargo.toml | 312 | `f04a346b02d6b304d0b1fe2f724f742545a48ed26bce353fc75d868d47201ba1` | 0 |
| src/rust/soroban/p23/soroban-test-wasms/wasm-workspace/auth/src/lib.rs | 8544 | `2e0064ca991f83c3a00177f052bbc5c053087546ed1e42a944c7af810bb03621` | 0 |
| src/rust/soroban/p23/soroban-test-wasms/wasm-workspace/complex/Cargo.toml | 293 | `0067ed9e3a4473fa625554efc2b026ff83ab9211a7ae243dbdb6afebb6fb9245` | 0 |
| src/rust/soroban/p23/soroban-test-wasms/wasm-workspace/complex/src/lib.rs | 1522 | `7fb764db8fd1ff735f0077daa0c0f8fbca952fb621075820dd741321a27b37d0` | 0 |
| src/rust/soroban/p23/soroban-test-wasms/wasm-workspace/conditional_account/Cargo.toml | 302 | `9dec27ee4ce2269cb4fcf2b36bf97314ca3e666314f8361e3f352b86e184cc8a` | 0 |
| src/rust/soroban/p23/soroban-test-wasms/wasm-workspace/conditional_account/src/lib.rs | 1190 | `8373ab257590bdc0023784bdcd8c465630ca631a1f820b1db1e6fb9b88fbf4ab` | 0 |
| src/rust/soroban/p23/soroban-test-wasms/wasm-workspace/constructor/Cargo.toml | 294 | `ff1e3d8dc9d364c3fe88c5ebd67a52db55b36c761b5bb0827cba0a25ce5bce18` | 0 |
| src/rust/soroban/p23/soroban-test-wasms/wasm-workspace/constructor/src/lib.rs | 1058 | `c423ed6d892c0286acc21a9fb78cb7bb159b247dce09c5c9b01b29cdcc246d76` | 0 |
| src/rust/soroban/p23/soroban-test-wasms/wasm-workspace/constructor_with_result/Cargo.toml | 306 | `2e96ef48cc040386131b56ed8a1d555850283e07eaf5087ef8d62abdb5452900` | 0 |
| src/rust/soroban/p23/soroban-test-wasms/wasm-workspace/constructor_with_result/src/lib.rs | 621 | `32a1d47c7d3c10309b7aba51b7ac5138c80adcbed19b0726950c05b8946cf72d` | 0 |
| src/rust/soroban/p23/soroban-test-wasms/wasm-workspace/constructor_with_return_value/Cargo.toml | 312 | `59d0b78167d61493e8e991da525ba1e65976a14b7c9ea8b06ad944c19b9b8798` | 0 |
| src/rust/soroban/p23/soroban-test-wasms/wasm-workspace/constructor_with_return_value/src/lib.rs | 234 | `c30ae802d69000e032c778d0558e7a3cd1fc93750e69f617a27d5a281b812522` | 0 |
| src/rust/soroban/p23/soroban-test-wasms/wasm-workspace/contract_data/Cargo.toml | 299 | `77083980ef46d4854eb10c3fc40df19e910dcac6df40935a6af45b0eb3d17332` | 0 |
| src/rust/soroban/p23/soroban-test-wasms/wasm-workspace/contract_data/src/lib.rs | 2543 | `6c0338d09518eb380e996f7ea007f5f50a9f3c6d37b1e2a26913622e71aec0d8` | 0 |
| src/rust/soroban/p23/soroban-test-wasms/wasm-workspace/contract_sac_transfer/Cargo.toml | 299 | `9e6a1c69f818e4c6a52f70f0340235131b9af4b81faeffed68f4ded27154d277` | 0 |
| src/rust/soroban/p23/soroban-test-wasms/wasm-workspace/contract_sac_transfer/src/lib.rs | 887 | `c9d6120e84d5feb71885c17c6ff9b2dea7f15c964cae998f7a6e899695954bc2` | 0 |
| src/rust/soroban/p23/soroban-test-wasms/wasm-workspace/create_contract/Cargo.toml | 317 | `281d6a213ecfeb71d508b60fb9240834123a0c7fb9b83d6690a7ef78625539bb` | 0 |
| src/rust/soroban/p23/soroban-test-wasms/wasm-workspace/create_contract/src/lib.rs | 419 | `d999ae4431e2cca2ff8500a042c58581208a70775eada7264e8985de95b11138` | 0 |
| src/rust/soroban/p23/soroban-test-wasms/wasm-workspace/custom_account_context/Cargo.toml | 305 | `92af459b76ad60e3ce347fcdc67aa5a1ad051c49b4adb77f7c67a55589badc64` | 0 |
| src/rust/soroban/p23/soroban-test-wasms/wasm-workspace/custom_account_context/src/lib.rs | 601 | `b657abdf54831ee754ff23623c5de4d0723013371aa201838112bc49df3bfb45` | 0 |
| src/rust/soroban/p23/soroban-test-wasms/wasm-workspace/delegated_account/Cargo.toml | 300 | `7908ae88dab514ec6d70894655953384c7da38a7d4f969c6d63ede8e23c6a439` | 0 |
| src/rust/soroban/p23/soroban-test-wasms/wasm-workspace/delegated_account/src/lib.rs | 868 | `36ad27bafba63f3f84003fc542a5ea676ae40bd5cf95d76532fcbf15f57c64e2` | 0 |
| src/rust/soroban/p23/soroban-test-wasms/wasm-workspace/deployer/Cargo.toml | 291 | `0a745dea42f11644e128a60ea95b230fc9228d657d1e59bd0505c06e8621d4d8` | 0 |
| src/rust/soroban/p23/soroban-test-wasms/wasm-workspace/deployer/src/lib.rs | 1873 | `ade03dfecc57c2a865c94f0e96203aae80eb6b5a081827a7247768a55fd561cc` | 0 |
| src/rust/soroban/p23/soroban-test-wasms/wasm-workspace/deployer_with_constructor/Cargo.toml | 308 | `7cd7dc3819357f91f599199090fd0c56e5ffa2f8e05e631255fb4e22330adce6` | 0 |
| src/rust/soroban/p23/soroban-test-wasms/wasm-workspace/deployer_with_constructor/src/lib.rs | 5011 | `7648828e97d74ed7ece814fa105f4ad2bbff85acc1e599b62e3d5923a24aea54` | 0 |
| src/rust/soroban/p23/soroban-test-wasms/wasm-workspace/err/Cargo.toml | 347 | `49a7e63a73faaa259430d07f3f4bfc4248053afd571a89ddad82b8b488e5c8be` | 0 |
| src/rust/soroban/p23/soroban-test-wasms/wasm-workspace/err/src/lib.rs | 2881 | `6d421da68d5bcfb4dec07757387e48833cb5f3bbe6ce99dfd8730a08605aed23` | 0 |
| src/rust/soroban/p23/soroban-test-wasms/wasm-workspace/fannkuch/Cargo.toml | 310 | `b6ec9f13152db30ec92fb459ede39594cbc77404f8e176e06baa71b323a11ef0` | 0 |
| src/rust/soroban/p23/soroban-test-wasms/wasm-workspace/fannkuch/src/lib.rs | 2236 | `f8af8a42fd6fc33fde15a97091e4382bba5c851e44210cf3a840f70d8ef81c97` | 0 |
| src/rust/soroban/p23/soroban-test-wasms/wasm-workspace/fib/Cargo.toml | 305 | `30b7bf6023952b31b3a9d8cb1df2aa7223149253f8678452726b0d0df58035be` | 0 |
| src/rust/soroban/p23/soroban-test-wasms/wasm-workspace/fib/src/lib.rs | 268 | `c957875f4c1b35d053c3b2d746bcf748667913f12e33be6e03d244b537521d84` | 0 |
| src/rust/soroban/p23/soroban-test-wasms/wasm-workspace/hostile/Cargo.toml | 350 | `a828d8f58a569be29dc2f6c64a35953cf15829e6ad1925b69d76d2ff08709752` | 0 |
| src/rust/soroban/p23/soroban-test-wasms/wasm-workspace/hostile/src/lib.rs | 3124 | `c2eedf2f69c9f8cefbcf0e12967b76413d1b42e347f6478c221e8b294c6227f9` | 0 |
| src/rust/soroban/p23/soroban-test-wasms/wasm-workspace/hostile_large_val/Cargo.toml | 311 | `1317a69cd05283c9f027d3211fb3b37d9ae9757257a5565ae5b145be0680c8eb` | 0 |
| src/rust/soroban/p23/soroban-test-wasms/wasm-workspace/hostile_large_val/src/lib.rs | 2553 | `dbf1d00afd9f5f62c0bab4a4e51114fb876585262f8da8af1f030f04031d9a02` | 0 |
| src/rust/soroban/p23/soroban-test-wasms/wasm-workspace/invoke_contract/Cargo.toml | 317 | `c1f763f78de7b09d9095efac80104d088f6bd41ecc2bd6fb59e345e90c5beb67` | 0 |
| src/rust/soroban/p23/soroban-test-wasms/wasm-workspace/invoke_contract/src/lib.rs | 1943 | `331251706eeb7ca4c8f64877b2f4e2176b7195299989a6271db21db3c0a70357` | 0 |
| src/rust/soroban/p23/soroban-test-wasms/wasm-workspace/invoker_auth/Cargo.toml | 320 | `cdcf51951afe17159a5b6297b81e29ecbb785db2b3a654f7378a70a7f62fc726` | 0 |
| src/rust/soroban/p23/soroban-test-wasms/wasm-workspace/invoker_auth/src/lib.rs | 5921 | `6deed63acc70a7cf0c92f307243454a2ba4b1d2aed10cbafb59ed07207d64b64` | 0 |
| src/rust/soroban/p23/soroban-test-wasms/wasm-workspace/linear_memory/Cargo.toml | 341 | `907403fc34c319e3f0c99cc42b49584c108d39a846eca72924ac03a49d6a707c` | 0 |
| src/rust/soroban/p23/soroban-test-wasms/wasm-workspace/linear_memory/src/lib.rs | 2861 | `998f890f085a31c269dee25aa5ac3eef9a62efc4166d2d26377073eab3574a3d` | 0 |
| src/rust/soroban/p23/soroban-test-wasms/wasm-workspace/loadgen/Cargo.toml | 293 | `54a775e24e6a6b93bd1a91e8a8f67c9ba8a34893ef5dc66b70aa2e4b8c3082b8` | 0 |
| src/rust/soroban/p23/soroban-test-wasms/wasm-workspace/loadgen/src/lib.rs | 2035 | `9a2077b1af173b0dad443032321f21dce3b6966d0ae88ff2c0043ec6f3859640` | 0 |
| src/rust/soroban/p23/soroban-test-wasms/wasm-workspace/no_arg_constructor/Cargo.toml | 301 | `cdd661d64e2e9731bdbc49637372195660a1f21304f516af3ec7fc6164fec8c2` | 0 |
| src/rust/soroban/p23/soroban-test-wasms/wasm-workspace/no_arg_constructor/src/lib.rs | 696 | `f49c7035942d9351dde370ed4ea4e00698f76f66f2cee13079ccc0636acdc413` | 0 |
| src/rust/soroban/p23/soroban-test-wasms/wasm-workspace/recursive_account/Cargo.toml | 287 | `ba3460e51138adcf00bcd2fe7e59d6dc01a78fa752ead699befae8c3c607ba16` | 0 |
| src/rust/soroban/p23/soroban-test-wasms/wasm-workspace/recursive_account/src/lib.rs | 1819 | `99df3ded80c336870ed36935ca34af8306c1644bcc127f8adee9e6cb26ff2a24` | 0 |
| src/rust/soroban/p23/soroban-test-wasms/wasm-workspace/sac_reentry_account/Cargo.toml | 297 | `a8627c01b2129d0dae15ed2f709724cbebcb641ab9f5c66b9893b57e9c7078f4` | 0 |
| src/rust/soroban/p23/soroban-test-wasms/wasm-workspace/sac_reentry_account/src/lib.rs | 1176 | `44c4a73769a6db79991b2b981560e4c62df6a07a5a467550c8995f5333af2164` | 0 |
| src/rust/soroban/p23/soroban-test-wasms/wasm-workspace/simple_account/Cargo.toml | 300 | `233daf8057939469264afc3dd17b237b7ef423085d4eea909e79ddf5a41b2cbb` | 0 |
| src/rust/soroban/p23/soroban-test-wasms/wasm-workspace/simple_account/src/lib.rs | 948 | `7c74cf48ea7db5ed1ff209926ba7d98ba4c32127d9e52e229a3c90eedfed4e28` | 0 |
| src/rust/soroban/p23/soroban-test-wasms/wasm-workspace/sum_i32/Cargo.toml | 309 | `c37d0a5d2621bb8edb11aaa0a111d4c0d8afa4e1a65df8dfc404136711141d25` | 0 |
| src/rust/soroban/p23/soroban-test-wasms/wasm-workspace/sum_i32/src/lib.rs | 561 | `4b1c69bf2e59646c6202ce0e9e460a7d22eea3490e517ecc4f56cfc8e4b8f49b` | 0 |
| src/rust/soroban/p23/soroban-test-wasms/wasm-workspace/try_call_sac/Cargo.toml | 295 | `a8ef3fd8c92173dbc8e0975d0ba005063a495e49bd2be96fec39d73c5c057599` | 0 |
| src/rust/soroban/p23/soroban-test-wasms/wasm-workspace/try_call_sac/src/lib.rs | 435 | `e469644aac889f9613c96038630e05302321aede066868c0ac67e55f68508c5f` | 0 |
| src/rust/soroban/p23/soroban-test-wasms/wasm-workspace/update/Cargo.toml | 321 | `add583b889fe9dba5aa81ac0e5aa0a4d1cf11df49c0600e720b71b6c932fc1c2` | 0 |
| src/rust/soroban/p23/soroban-test-wasms/wasm-workspace/update/src/lib.rs | 945 | `d0ae9d5190e0f6251ee7182be9c052e068695ed305c7666caf4b455789c72c93` | 0 |
| src/rust/soroban/p23/soroban-test-wasms/wasm-workspace/upload_contract/Cargo.toml | 317 | `521c2d07450d0ca5174ed43df2b01b0e85341b9291813f03476a8aec1db2472d` | 0 |
| src/rust/soroban/p23/soroban-test-wasms/wasm-workspace/upload_contract/src/lib.rs | 252 | `5033bb1c628243bdaecc55b1c7676b20b22f73fe4842905b5bb92a1a111061c9` | 0 |
| src/rust/soroban/p23/soroban-test-wasms/wasm-workspace/vec/Cargo.toml | 289 | `8e78cf5495f3569dcb16e392caec5420e0c4e38682a79bee9f24bdf1bd2ef8e3` | 0 |
| src/rust/soroban/p23/soroban-test-wasms/wasm-workspace/vec/src/lib.rs | 346 | `a358381709762177476df8c9dcacdc6406e499b81de7523278f3fbf5212aa7d3` | 0 |
| src/rust/soroban/p23/soroban-test-wasms/wasm-workspace/write_upgrade_bytes/Cargo.toml | 330 | `6f5ed7b39a290835d688ae0aa0ae465b065d7b02fc6f758f08e3df5fc090d95c` | 0 |
| src/rust/soroban/p23/soroban-test-wasms/wasm-workspace/write_upgrade_bytes/src/lib.rs | 1003 | `8a0cc6e5f77713ee726982d933260e90732e70873c0a2bb8cc662ec651472c6d` | 0 |
| src/rust/soroban/p24/.cargo/config.toml | 6685 | `deaae172a164fb2ba5bfa0e6b3658fc8ef043a348c861936762a8a210c213ca0` | 0 |
| src/rust/soroban/p24/Cargo.lock | 60847 | `43512be2ad2a5172c3af58a17c7b32f66e29489aeb638d20bb08c939bb777b14` | 0 |
| src/rust/soroban/p24/Cargo.toml | 1928 | `b8602ad6515c990e743baa7c91b19f4e0d4a03f5dee82081233fe6bc1db2333c` | 0 |
| src/rust/soroban/p24/rust-toolchain.toml | 369 | `a93034bc4702710436624ddc42e89325be59ebc8e584e7c58b9b6c00fc2d3b2d` | 0 |
| src/rust/soroban/p24/soroban-bench-utils/Cargo.toml | 787 | `2020e9795c6dc4edfee39f36f1d78cf16b954f69ac16f9cba453485985d4edd3` | 0 |
| src/rust/soroban/p24/soroban-bench-utils/src/lib.rs | 75 | `4ed9af88c90c8137a175e9b2e583a3076ef13bc4911e133e889aa6f559caeeab` | 0 |
| src/rust/soroban/p24/soroban-bench-utils/src/rusagev4.rs | 2027 | `e775f766b27fcece33febfaf91e1b2e46b4ff0d7028a326909fd910dd75c7b17` | 0 |
| src/rust/soroban/p24/soroban-bench-utils/src/tracker.rs | 5923 | `71df7e2a505682276058fba51644bfe0f0d59934c327b9f4bb14ee6d59a6f8b4` | 0 |
| src/rust/soroban/p24/soroban-builtin-sdk-macros/Cargo.toml | 554 | `828f2414d8e7d7ded5567797a4eae4cd132908234489fc5ef6d327e99fe29d32` | 0 |
| src/rust/soroban/p24/soroban-builtin-sdk-macros/src/derive_fn.rs | 2815 | `627430878da696e94b872adc29d71390e866277ee7acf6c1b42e7cdd2ccf15a0` | 0 |
| src/rust/soroban/p24/soroban-builtin-sdk-macros/src/derive_type.rs | 8525 | `459416267127d646b9d105c16c046b210eeb22cd4c482511f268d8396120f215` | 0 |
| src/rust/soroban/p24/soroban-builtin-sdk-macros/src/lib.rs | 1734 | `7120a6c227f456234536bfef7c7f9d82918a8c89d8c25f3f16eaccc404a79aad` | 0 |
| src/rust/soroban/p24/soroban-env-common/Cargo.toml | 1564 | `0f5adc80e188724943b19317d9385671b59ca6f14d482a3cf067f4daeab7d89c` | 0 |
| src/rust/soroban/p24/soroban-env-common/build.rs | 99 | `818b5844721186dd913412974faaff4bb45954e41b2cedeecb4b0a5ddcf90b35` | 0 |
| src/rust/soroban/p24/soroban-env-common/src/arbitrary.rs | 2047 | `aaebd099ab97097e1ac2482ac4c437c99736f75ca822cfdcec435ccf8b8fb662` | 0 |
| src/rust/soroban/p24/soroban-env-common/src/bytes.rs | 3066 | `768838872830e2352670e97ad9d9313c24db0efb8854847474739ed33c7c5735` | 0 |
| src/rust/soroban/p24/soroban-env-common/src/compare.rs | 7475 | `b0a0b3dfa266b7bb4952b7fe2d1919e1a78af240777114484bf82567d72d6704` | 0 |
| src/rust/soroban/p24/soroban-env-common/src/convert.rs | 19709 | `634ff85286ff9b9272102f06dac071534aff05d5733734a2220967a94dfd5fcb` | 0 |
| src/rust/soroban/p24/soroban-env-common/src/env.rs | 17843 | `348641178612a18f24636640b215b16388abe850a50655fecff5788c483d4877` | 0 |
| src/rust/soroban/p24/soroban-env-common/src/error.rs | 15600 | `efd9f516f411d55dd01a22e33f3418068d82c715290382e98a5cba4f58bdc46e` | 0 |
| src/rust/soroban/p24/soroban-env-common/src/hash.rs | 1501 | `15c9e63948d9ce9486581659f1aea95a08eb849416500a0a096f8d9d11ec1350` | 0 |
| src/rust/soroban/p24/soroban-env-common/src/lib.rs | 4160 | `fc0ab41b67c78d08d46944b045f75a5b1259895659dd758599deaf0a402f14ab` | 0 |
| src/rust/soroban/p24/soroban-env-common/src/meta.rs | 3279 | `8dea07ba53000a3529cfce9a9d5e4942057a34b8b9253c88eb59de53bfb2561f` | 0 |
| src/rust/soroban/p24/soroban-env-common/src/num.rs | 14398 | `9242b8a3eeb918cbc602ecbb6e185b3d8bc6cacf27bb50d35c7aad767de5ff0c` | 0 |
| src/rust/soroban/p24/soroban-env-common/src/object.rs | 5970 | `b937c641ebab58af9bbbabab00a3351dac36d6937042b6eb1989eb32deb60318` | 0 |
| src/rust/soroban/p24/soroban-env-common/src/option.rs | 907 | `870a61869cabc46e32f50c93605686f4d66f1952bf89f596b8fbfdcaf5deb38e` | 0 |
| src/rust/soroban/p24/soroban-env-common/src/result.rs | 1261 | `d3210db790113cf7950e76c15492358ca9a469159f8dee2c27c2dee91228c4b0` | 0 |
| src/rust/soroban/p24/soroban-env-common/src/storage_type.rs | 1109 | `f6a406da19c791aeb5932a721bcea431eaad9ff0805199025796c6cf40e897c3` | 0 |
| src/rust/soroban/p24/soroban-env-common/src/string.rs | 2036 | `13ec3079a2f66e4affb3ecdeba15134f2941ef05076f544a195736dbd64bf8e9` | 0 |
| src/rust/soroban/p24/soroban-env-common/src/symbol.rs | 21416 | `535b8c4dc64fddc986e76d364ed319405f00e1f95bdf2fed02253fc1ecfab185` | 0 |
| src/rust/soroban/p24/soroban-env-common/src/tuple.rs | 4295 | `fed0d299699f9ad2f429f68199534af4b319cfbc960dfdf488e9dc943fae95ad` | 0 |
| src/rust/soroban/p24/soroban-env-common/src/val.rs | 30832 | `2528884f3114f81144f1a9a2cbdb0f7314ecc50070041c632b3ed75cdae5299b` | 0 |
| src/rust/soroban/p24/soroban-env-common/src/vmcaller_env.rs | 11584 | `a5de9e5baf5b6e2bdf9bed4051b635f22aa795be747a81e76cc816060dc33183` | 0 |
| src/rust/soroban/p24/soroban-env-common/src/wrapper_macros.rs | 12097 | `0228b5e35382d4dbca4b760f3f6a57d0a7ecbb9ffa897f16d445c82ce6e63e93` | 0 |
| src/rust/soroban/p24/soroban-env-guest/Cargo.toml | 625 | `65d7195e1ef69e1cba7c6aabd96072fe37482f0b1c7ecaeb17e17cc38b2ab937` | 0 |
| src/rust/soroban/p24/soroban-env-guest/src/guest.rs | 15156 | `ec9b060d0a83822824afbed9defc5c213d982019960a99ef613283baf851c6a1` | 0 |
| src/rust/soroban/p24/soroban-env-guest/src/lib.rs | 561 | `b34cdc92dbf3880bd463d0c82b7df5866ac88d74b8bc42d8a9321eb9104dcfdf` | 0 |
| src/rust/soroban/p24/soroban-env-host/Cargo.toml | 4911 | `6cbeaccade3e568b8b4865051cfe83e78a3b110caadcfee61e9705f68f4dbe95` | 0 |
| src/rust/soroban/p24/soroban-env-host/build.rs | 283 | `f90c468c4ab2735a8edeca9f82ca31cf327a27fd8baf47f7417dab8653151005` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/auth.rs | 101200 | `b2383f209b7fd250d9c0b55c455d2bf4c86e8c95a7071e06824bd774b018bfa1` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/bin/main.rs | 1503 | `9a76c921937802ea5e9c4017465e9dd471d2f933e928c4b0d559404ff8672845` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/budget.rs | 53692 | `277833a764520cce38b06c7023098716968b44c81850237c9bbb990c30d90b33` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/budget/dimension.rs | 6966 | `337bdb7857672f68b8e11ef76cf47107372c925930dd2c980e4409110ed613dc` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/budget/limits.rs | 4658 | `0080964f53ec49d2df64306354887cc5565b2628584e64548126a4b95e2eca1e` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/budget/model.rs | 5584 | `b6d99a8a793cd385cdcaaa7cd288d279b5628670ee34b7b83504a0276e982635` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/budget/util.rs | 7363 | `f652719196e0f9a290f6a597839191f89c858821ba2d79a06c9f04d1cf56a083` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/budget/wasmi_helper.rs | 4145 | `c7afc9c4c05a9ee57d0da858369312d9d0ba431bc337d02b98d750cfb4fbe0d0` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/builtin_contracts.rs | 560 | `f0bd26290068aff0d567b8e950c3abd9545b9f6fbb50a521001e21f9b3a7ed1e` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/builtin_contracts/account_contract.rs | 9309 | `370d6ab2b23e6e09199851d2fc77d033292ba49c4c14cc5bb71dad6f4fd6013f` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/builtin_contracts/base_types.rs | 13559 | `3c4d6c21676ab4b863536f10b7dc41615719161f97f025ce3fa9acfbd041295f` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/builtin_contracts/common_types.rs | 1225 | `69efad1515dfe980cf07c32fb08ec2697528171de6eaa4be800e7ecde5334dc6` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/builtin_contracts/contract_error.rs | 914 | `cfddfd3a20809a0c30d5d86f93135936780945aab909918f2e3d3351589310aa` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/builtin_contracts/invoker_contract_auth.rs | 6544 | `d0a8069c45de5a5cbef488726df63356cd81f09e1e32d23aed4a268bc42811df` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/builtin_contracts/stellar_asset_contract.rs | 248 | `944142447b113d671f1e47dc8a2d8191ef4ff11167b793f2a4c2f4d72efc8e4f` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/builtin_contracts/stellar_asset_contract/admin.rs | 704 | `ad70748dab976704bdf5fa87dfe30c0746280a24eb46c36a9c102aeb1f11980d` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/builtin_contracts/stellar_asset_contract/allowance.rs | 5082 | `533b7dde81bf6e70229d1e297aa1e8d6adb94eafd5ebe75c44c38ae179c9b36f` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/builtin_contracts/stellar_asset_contract/asset_info.rs | 3092 | `9a0583a6bec016f2822bc357baa2cce81c8e4ad3077fd8d5e2100172c0b22def` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/builtin_contracts/stellar_asset_contract/balance.rs | 29464 | `ffee339060c5e3857c0cac9708df112686d9af8fa2c4f781a66820f27f734c5c` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/builtin_contracts/stellar_asset_contract/contract.rs | 13122 | `d7601ef3510ec3d4591f207c4b544b29165ca2b0efc28ddcc22380434f6c491a` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/builtin_contracts/stellar_asset_contract/event.rs | 4403 | `125cc56ff663883f629520b9ea1fc1978527c61b86867063cd57cba7730b211c` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/builtin_contracts/stellar_asset_contract/metadata.rs | 6992 | `12ca5219bd19e98b81880a01e5fe99bfffaf1c5d283371bff34961763ac00331` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/builtin_contracts/stellar_asset_contract/public_types.rs | 1318 | `84834c2fec3c9763ba73d89fdd44db86da9a35400e82401cd5ba04ed03874026` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/builtin_contracts/stellar_asset_contract/storage_types.rs | 1113 | `655a0cec594b78db2eeccabfe03e27f2ae0537c65729e456b604cbbdb579f298` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/builtin_contracts/storage_utils.rs | 362 | `216d16572291ac021fd3ee7a0ce6d4b1810f8dbee07fc2791bbf32236a75ed10` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/builtin_contracts/testutils.rs | 12166 | `d7cfa0520c24dc9360d9126071f8ef48b88103196b29726dc9571cdc181c9af0` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/cost_runner/cost_types/bls12_381.rs | 10204 | `965dff98b1d17f2c58dd07697781db1c8033193651fb14d4473b091fb6ab43c4` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/cost_runner/cost_types/compute_ed25519_pubkey.rs | 952 | `c679365a8825299630452cf28daf21f4e6cff1805ca06910bc4ce49300d04a7c` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/cost_runner/cost_types/compute_keccak256_hash.rs | 916 | `c70f481dcea5eba30a4ae54ea476efec3fb3bf938d15987042aaeac222bbef3d` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/cost_runner/cost_types/compute_sha256_hash.rs | 896 | `99eece10c8e2379a0d3675f618b6c9192a57ddd98bc0063cc886ab22d526b509` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/cost_runner/cost_types/decode_ecdsa_curve256_sig.rs | 1407 | `6eae776ff6b8ee070b6d51f70a4b231bf78c2bd0e964c0cae695be06a66b251e` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/cost_runner/cost_types/host_mem_alloc.rs | 951 | `53bd536e402308f09e0ead2a7825d8a7a88c6da46f0deb55ddce336d6a754a32` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/cost_runner/cost_types/host_mem_cmp.rs | 957 | `db2b390ce0892f2b450a9707d8f3d54a9fe2438d88f73ae021263dc18b266a3c` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/cost_runner/cost_types/host_mem_cpy.rs | 821 | `7ab8627489d5882ca2725d3e5872dc5cf3907890341065e5fa9149b121f11316` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/cost_runner/cost_types/invoke.rs | 2183 | `451a7818021ac77658771411708fe709c328f8d29abb0906720cd4da4fbb069d` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/cost_runner/cost_types/mod.rs | 983 | `0e319de5bfa8eeafbc2f98d9187c31084ba8ae0755533496d9b3563ee62b3c43` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/cost_runner/cost_types/num_ops.rs | 1546 | `cf08647785a4ede49183258e305e4520b3db286536bf2a6e71583e76c89be32b` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/cost_runner/cost_types/prng.rs | 1003 | `fac74f446f916302d6b27d59040ae6c72aa4decbfe766a862f9b0a2dceb75223` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/cost_runner/cost_types/recover_ecdsa_secp256k1_key.rs | 1140 | `21256191032a43cd2584275eebae7e034db553ee6c90c16d6ba5e5e2392eb69a` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/cost_runner/cost_types/sec1_decode_point_uncompressed.rs | 1155 | `06fda4cc5f09ca513953f45424b1aa5277fb1fa0805e598e63466ea6b45d1863` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/cost_runner/cost_types/val_deser.rs | 800 | `19b4abd59908d36bc2c1a2d7e05fc67db21df215cf02bcf91ff42d760f18e6d0` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/cost_runner/cost_types/val_ser.rs | 1385 | `2b3aa6b23feb1d99fdfc267146458eba577e8641124c8673a606fa0cb976b08e` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/cost_runner/cost_types/verify_ecdsa_secp256r1_sig.rs | 1124 | `8b1e249924c8f329e563122f8e2c1d0e60fbc6c788de70c0dd4e9aeaf8f8b833` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/cost_runner/cost_types/verify_ed25519_sig.rs | 1079 | `da86df368d3cdc769f57e48a6fd160ba5c7f1dab0a44876587875be1167215bc` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/cost_runner/cost_types/visit_object.rs | 1056 | `c66e1ae7580a923564f8694f34d3ee9ff4c3de2b768529cf75a9f86e23c9c656` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/cost_runner/cost_types/vm_ops.rs | 8989 | `3a7c74abaa9d8e628d3bc586d8b3056218a8a234bd8e4f35857e186cb4fcc135` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/cost_runner/cost_types/wasm_insn_exec.rs | 9902 | `2c3bfc08db067c5d0320dfbbb55d477019e282d7c7a4d4c6c1c704b47a6b2983` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/cost_runner/experimental/bls12_381.rs | 6378 | `154aed6d61b073065304ff1b68dd8eb3709a82108a7983d23a44cb01cb744ac1` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/cost_runner/experimental/decode_secp256r1_sig.rs | 1472 | `2f7bf5f395b05ad7ae9ab37e404eae4c3bfa85d29eaa8d08becfcfef825b0a1e` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/cost_runner/experimental/ecdsa_secp256k1_verify.rs | 1487 | `d5d2bdc6133fc64cdbe0765a2d5ee6069a9cfedb8b03943dff269770d30b88c6` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/cost_runner/experimental/ecdsa_secp256r1_recover.rs | 1499 | `2e4920ce9df183016f9bf4765bde45f76b746f34d636b03d21647e8ee7bfb7f3` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/cost_runner/experimental/ed25519_scalar_mut.rs | 1353 | `5b0755082fbcd387ee756a4fcb85b19abb7f632aabefddae79063463cd81b480` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/cost_runner/experimental/map_ops.rs | 1005 | `5feb978d228ff705dcee86bb90cedaa328dfa196c6fdbbfc48468d6dfbd8cd74` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/cost_runner/experimental/mod.rs | 2700 | `cc07f061fc69b5348c5cb1e8dbaaad46f4b06ff7a396245618d954e98d4c77cd` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/cost_runner/experimental/read_xdr.rs | 1388 | `476f11215c5a4bdcebe94772688e45f28d96db4f5dfe4da029507cd01d4f3f3f` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/cost_runner/experimental/sec1_decode_point_compressed.rs | 1756 | `299089e64c18ca9c4414a6461eaf023cbcfdbdca24db9f55edbf28f922771643` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/cost_runner/experimental/vec_ops.rs | 1132 | `8116fc7fe3f8d9259a9a98a719f9a8a67d96e2159db1644fc1e14cf352aaae48` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/cost_runner/experimental/vm_ops.rs | 2196 | `a253e366b149b7583c7e48b3aff4a982fca99e0194b526c5276fcaa81253323a` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/cost_runner/mod.rs | 787 | `d8b4f3f225b31efed2489ac70a610d6a774514944bdbb5645431e9cfef8251e3` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/cost_runner/runner.rs | 4203 | `98f216ef92f42ce6364d6aa13cffcc33a6da9fa344469ebe0b7093614ca71fc7` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/cost_runner/util.rs | 4774 | `9cbbfe0c50bd607d1d879a9968fdd5ec69ae096faa34216a7bbbe7986e2bc57c` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/crypto/bls12_381.rs | 32386 | `53570a02f948b812a40b6ebf41054c842020a8c968639867c4a6d96508e4a136` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/crypto/mod.rs | 13040 | `ccbe1563db40bf085dacdc7d468d0ac5b3230274e1ac237509c81868c8af8411` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/e2e_invoke.rs | 45261 | `e136857e26a7fe1fb4e16ad9a5398ab258b736391e5e8b2b9144321237b45a3a` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/e2e_testutils.rs | 11747 | `1e004e07778f6c0c921cb36f95e400435e6d59062a9f9f1663cd5cd80aa321bc` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/events/diagnostic.rs | 5750 | `a66118d5747c50c89b1c7e1fa859b6b43b91f10add59353f274b115e3a171776` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/events/internal.rs | 11050 | `44c6828241d86a89af619d88026b57b38a7915632a8d163716c4afe9ac6743be` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/events/mod.rs | 9660 | `763d64d569ba98e1ebfa0491a263291b8004d170629d6ae6902435ced6c92436` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/events/system_events.rs | 1356 | `126b8da42733be7deea23b239008eeca261828c191862f26be1d759b82422f53` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/fees.rs | 15746 | `b34056e45639409f8f8c541ddaaf6cb938ddfa22e6b803fe1b3c4df55fb38d4e` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/host.rs | 134196 | `86913fcaf25aab806c86572bc8930717eb0a342727696b541c17b32421b31d97` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/host/comparison.rs | 28373 | `573aa99e9e84a6ddf2bc1accec5e37eee08f0aec684bdf51a95345bda7813a55` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/host/conversion.rs | 22972 | `9de73ba3360b76ffaa81644e66ea95317fc511d2e078296c7dee38b24419a26f` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/host/data_helper.rs | 23170 | `3ac29082e2e080b69fb24e2f3aea74b3869f9a9aa31720108608ab1d2fc348af` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/host/declared_size.rs | 37447 | `983113ec62422a9e1b08b2afbeb55b186622905bef556bde1232872f14750eb9` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/host/error.rs | 17368 | `6d4fa87584f3dc60588f83ac2bc359f8b89f6ca2b89b6bbfc34a32f854155faa` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/host/frame.rs | 49700 | `ffe34c0f024f90f29ea4ca8dd8a2f5807542a366cba3aa82068b753795180355` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/host/invocation_metering.rs | 64160 | `fab3110f0383f4bd4d59f7b3e1caf1fca3e2d7d19ac30d269c2554add78a472d` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/host/ledger_info_helper.rs | 1502 | `9144a723b7119e868776cb21260b2f44ce286bc6a6485ada29c6133fc71e33ae` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/host/lifecycle.rs | 15395 | `3016559fe990948f61e4006d4ab1a8e6126ef066c8f546ec22d81051d8f57e21` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/host/mem_helper.rs | 18165 | `d178c7f39d95b245e33ae8bef94b381944191c9a899edee4640db6c6d21e77d5` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/host/metered_clone.rs | 25638 | `43de045d53cf824b83407c440275bf9d7498f0f9e5fbd6be04629889f92cc3a6` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/host/metered_hash.rs | 2482 | `3792f8eea8df5b983fb363b0a282f8e91e3b7dfca5a424484cb5d3e0ae5c056b` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/host/metered_map.rs | 15359 | `f81c4b76b8487f4f6d849751cd26353bf8778ecf0916266cf2e5fb09fd2e5b5c` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/host/metered_xdr.rs | 2650 | `22e70db0f290b025fb1e992b230564210a7b315c9ea7dca1e3e28609c64b7a52` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/host/num.rs | 2933 | `e188fe8582e1ff99f1ed9123e6f30bbd3903c89c6ba3d31644c1d7a3c1e983df` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/host/validity.rs | 1818 | `b5c6baa004d08a398e6553f5336c5c1dc2ccb099dfdc0ed708ed967147c883d5` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/ledger_info.rs | 1348 | `5a7d202b945c0e639624746f926040eb873f640217652d55fb68fbc5acfb1f4c` | 0 |
| src/rust/soroban/p24/soroban-env-host/src/lib.rs | 2180 | `66a4ba6676268b0bcd59c1fb00a29f07e6c19b021e45244932a01a415f0247be` | 0 |
| src/rust/soroban/p25/soroban-bench-utils/src/lib.rs | 75 | `4ed9af88c90c8137a175e9b2e583a3076ef13bc4911e133e889aa6f559caeeab` | 0 |
