# Security & Post-Quantum Readiness Audit Report

**Project:** obp-api @ 6a4a13ef079f · TESOBE (Open Bank Project) — public repository (passive review)
| | |
|---|---|
| Organization | QSI |
| Report date | 2026-11-06 10:11 UTC |
| Report version | 1 |
| Audit run | 78a831be-14ad-42a7-b5fb-ace36174c24c (Document audit) |
| Analyzer engine | qsi-engine 1.3.0 |
| Risk profile | Crypto exchange, custodian or wallet |
| Content SHA-256 | `6e83fddb11fe4c5dcc78ace863f481960b11f629a8378ee1992ce77d9bae882f` |
| Signature key (Ed25519, SHA-256 fingerprint; the signature is the separate file report.sig.json) | `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e` |
> This report presents automated and documented analysis results for the stated scope. It is not a legal opinion, a certification or an attestation of compliance with any standard.

## 1. Executive summary

- Critical: **0**
- High: **24**
- Medium: **12**
- Low: **5**
- Info: **3**

- Confirmed technical vulnerability: 0
- Known vulnerable component: 18
- Confirmed configuration error: 15
- Potential cryptographic risk: 1
- Long-term post-quantum risk: 5
- Improvement recommendation: 4
- Insufficient data: 1

Mosca's inequality (x + y > z): x = 10, y = 5, z = 8 → migration would finish too late under this scenario. _z is a planning assumption chosen per risk profile, not a prediction. A cryptographically relevant quantum computer is not publicly known to exist today._

**Post-quantum maturity: Level 0 of 4 — no post-quantum cryptography.** Next step: Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

## 2. Scope and boundaries

Mode: Document audit

Repository: <https://github.com/OpenBankProject/OBP-API> @ `6a4a13ef079fa33707f4ee3dba1e600570ed34b4` — evidence links open the lines at this commit.

1190 files, 17649437 bytes in total, 111 redaction(s); the per-file SHA-256 list is in appendix C.

## 3. Methodology

| Area | Status | Count | Examples |
|---|---|---|---|
| source_code | checked | 1172 | .github/scripts/check_test_isolation.py: 231 lines scanned with 16 rule patterns and 266 registry patterns; obp-api/src/main/scala/bootstrap/http4s/Http4sMtls.scala: 236 lines scanned with 16 rule patterns and 266 registry patterns; obp-api/src/main/scala/bootstrap/http4s/Http4sServer.scala: 80 lines scanned with 16 rule patterns and 266 registry patterns |
| tls_configuration | checked | 4 | dev/mtls-nginx/nginx.conf: nginx TLS directives parsed; obp-api/src/main/resources/docs/introductory_system_documentation.md: nginx TLS directives parsed; obp-api/src/main/scala/code/api/v6_0_0/Http4s600.scala: openssl TLS directives parsed |
| certificates | error (not checked) | 14 | docs/MTLS.md line 403: certificate could not be parsed (ValueError); obp-api/src/main/scala/code/api/ResourceDocs1_4_0/SwaggerDefinitionsJSON.scala line 2968: certificate could not be parsed (ValueError); obp-api/src/main/scala/code/api/ResourceDocs1_4_0/SwaggerDefinitionsJSON.scala line 3067: certificate could not be parsed (ValueError) |
| certificates_and_keys | checked | 10 | docs/MTLS.md: certificates/keys parsed; obp-api/src/main/resources/props/sample.props.template: certificates/keys parsed; obp-api/src/main/scala/code/api/ResourceDocs1_4_0/SwaggerDefinitionsJSON.scala: certificates/keys parsed |
| dependencies | checked | 3 | obp-api/pom.xml: 89 dependencies parsed (68 pinned); obp-commons/pom.xml: 10 dependencies parsed (3 pinned); pom.xml: 15 dependencies parsed (13 pinned) |
| tls_key_exchange_groups | Insufficient data | 4 | obp-api/src/main/resources/docs/introductory_system_documentation.md: no key-exchange group directive; TLS library defaults apply and were not determined; obp-api/src/main/scala/code/api/v6_0_0/Http4s600.scala line 14214: not in the algorithm registry, not assessed: List(; obp-api/src/main/scala/code/api/v7_0_0/Http4s700Groups.scala line 304: not in the algorithm registry, not assessed: found.collect |
| secrets | checked | 14 | obp-api/src/main/resources/docs/introductory_system_documentation.md: 25 redacted value(s) not reported (comments, test modules, fixture declarations, placeholders, values the source annotates as published, or hex values not bound to a secret name); obp-api/src/main/scala/code/api/OAuth2.scala: 3 redacted value(s) not reported (comments, test modules, fixture declarations, placeholders, values the source annotates as published, or hex values not bound to a secret name); obp-api/src/main/scala/code/api/ResourceDocs1_4_0/OpenAPI31JSONFactory.scala: 1 redacted value(s) not reported (comments, test modules, fixture declarations, placeholders, values the source annotates as published, or hex values not bound to a secret name) |
| tls_code | checked | 1 | obp-api/src/main/scala/code/api/util/migration/MigrationOfDynamicEntityRoleNames.scala: TLS key-exchange settings read |
| entropy | checked | 1 | random-number generation: 10 code files read with 0 macro definitions from the tree; 0 ineffective guard(s), 0 weak random-bytes provider(s), 0 weak key-generation site(s) |
| osv_advisories | checked | 1 | 82 pinned packages queried at OSV.dev; 6 affected |

_Long lists are grouped here; the full per-file list is in the JSON report, signed with the same key._

## 4. Assets examined and not examined

- certificates — error (not checked): docs/MTLS.md line 403: certificate could not be parsed (ValueError)
- tls_key_exchange_groups — Insufficient data: obp-api/src/main/resources/docs/introductory_system_documentation.md: no key-exchange group directive; TLS library defaults apply and were not determined
- certificates — error (not checked): obp-api/src/main/scala/code/api/ResourceDocs1_4_0/SwaggerDefinitionsJSON.scala line 2968: certificate could not be parsed (ValueError)
- certificates — error (not checked): obp-api/src/main/scala/code/api/ResourceDocs1_4_0/SwaggerDefinitionsJSON.scala line 3067: certificate could not be parsed (ValueError)
- certificates — error (not checked): obp-api/src/main/scala/code/api/constant/constant.scala line 1035: certificate could not be parsed (ValueError)
- certificates — error (not checked): obp-api/src/main/scala/code/api/util/BerlinGroupSigning.scala line 129: certificate could not be parsed (ValueError)
- certificates — error (not checked): obp-api/src/main/scala/code/api/util/BerlinGroupSigning.scala line 283: certificate could not be parsed (ValueError)
- certificates — error (not checked): obp-api/src/main/scala/code/api/util/CertificateVerifier.scala line 138: certificate could not be parsed (ValueError)
- certificates — error (not checked): obp-api/src/main/scala/code/api/util/CertificateVerifier.scala line 146: certificate could not be parsed (ValueError)
- certificates — error (not checked): obp-api/src/main/scala/code/api/v2_2_0/Http4s220.scala line 884: certificate could not be parsed (ValueError)
- certificates — error (not checked): obp-api/src/main/scala/code/api/v2_2_0/Http4s220.scala line 897: certificate could not be parsed (ValueError)
- certificates — error (not checked): obp-api/src/main/scala/code/api/v4_0_0/Http4s400.scala line 11069: certificate could not be parsed (ValueError)
- tls_key_exchange_groups — Insufficient data: obp-api/src/main/scala/code/api/v6_0_0/Http4s600.scala line 14214: not in the algorithm registry, not assessed: List(
- tls_key_exchange_groups — Insufficient data: obp-api/src/main/scala/code/api/v7_0_0/Http4s700Groups.scala line 304: not in the algorithm registry, not assessed: found.collect
- tls_key_exchange_groups — Insufficient data: obp-api/src/main/scala/code/api/v7_0_0/Http4s700Groups.scala line 362: not in the algorithm registry, not assessed: List(
- certificates — error (not checked): scripts/resource_doc_baseline/lift_resource_docs_v2_2_0.json line 214: certificate could not be parsed (ValueError)
- certificates — error (not checked): scripts/resource_doc_baseline/lift_resource_docs_v2_2_0.json line 215: certificate could not be parsed (ValueError)
- certificates — error (not checked): scripts/resource_doc_baseline/lift_resource_docs_v4_0_0.json line 1107: certificate could not be parsed (ValueError)

## 5. Architecture overview

Static review of the source tree obp-api at 6a4a13ef079fa33707f4ee3dba1e600570ed34b4. 1190 files analysed; of 1917 files, 572 are test, fuzzing, benchmark or example code and were left out, 155 are not read by any analyzer, 0 exceed the per-file limit and 0 did not fit the total limit. Files no analyzer reads include: .dockerignore, .github/Dockerfile_PreBuild, .github/actions/setup-test-database/action.yml, .github/dependabot.yml, .github/workflows/build_container.yml. 30 files in build-output or dependency-cache directories (.git, .hg, .venv, __pycache__, build, dist, node_modules, target, vendor, venv) were not read. No requests were sent to the owner's systems.

## 6. Overall security posture

- Indicative posture index: **0** / 100 — _Derived from findings in scope (confirmed and potential issues weighted by severity). Indicative only; not comparable across differently scoped audits._
- Quantum-vulnerable share of inventory: 30.3%

## 7. Detailed findings

### QSI-2026-17438 — Certificate has expired (app.example.com)

- Severity: **High** · Classification: Confirmed configuration error · Confidence: High
- Affected asset: `certificate:app.example.com`
- Data source: obp-api/src/main/resources/props/sample.props.template
- Detection method: X.509 parsing (pyca/cryptography), comparison of notAfter with the analysis time (UTC).
- Analyzer: certificates 1.3.0 · 2026-11-06 10:11 UTC
- Priority score: 61.4 / 100
- CVSS v3.1: not applicable

The X.509 certificate with subject app.example.com expired on 2025-11-26 (344 days ago).

**Potential impact.** Clients that validate certificates will refuse connections; users may be trained to ignore warnings.

**Reproduction steps.**

```
openssl x509 -in obp-api/src/main/resources/props/sample.props.template -noout -enddate
```

**Evidence.**

_certificate · obp-api/src/main/resources/props/sample.props.template · line 2027 · SHA-256 0dda242ea754f0359967578bc4499e17a3c382359f0acb4bb6edcca1c07416ef_

```
Subject: CN=app.example.com
Issuer: CN=app.example.com
Serial: 18c10eb6474
Not before: 2023-11-27T13:15:11+00:00
Not after: 2025-11-26T13:15:11+00:00
Public key: RSA 2048-bit
Signature algorithm: 1.2.840.113549.1.1.11
Signature hash: sha256
CA: False
SAN: -
SHA-256 fingerprint: 25d91ac53796ca8c5598ee6d180ff0efb3919b4592b4ecef1c68fad35b20c726
```

**Limitations of the check.** Document-based analysis: only the supplied file was examined. Deployed configuration may differ; the result reflects the file content at the recorded SHA-256.

**Recommendation.** Renew the certificate and automate renewal (e.g. ACME) with expiry monitoring.

**Retest procedure.** Re-parse the deployed certificate and confirm notAfter is in the future.

### QSI-2026-17443 — Certificate has expired (app.example.com)

- Severity: **High** · Classification: Confirmed configuration error · Confidence: High
- Affected asset: `certificate:app.example.com`
- Data source: obp-api/src/main/scala/code/api/ResourceDocs1_4_0/SwaggerDefinitionsJSON.scala
- Detection method: X.509 parsing (pyca/cryptography), comparison of notAfter with the analysis time (UTC).
- Analyzer: certificates 1.3.0 · 2026-11-06 10:11 UTC
- Priority score: 61.4 / 100
- CVSS v3.1: not applicable

The X.509 certificate with subject app.example.com expired on 2025-11-26 (344 days ago).

**Potential impact.** Clients that validate certificates will refuse connections; users may be trained to ignore warnings.

**Reproduction steps.**

```
openssl x509 -in obp-api/src/main/scala/code/api/ResourceDocs1_4_0/SwaggerDefinitionsJSON.scala -noout -enddate
```

**Evidence.**

_certificate · obp-api/src/main/scala/code/api/ResourceDocs1_4_0/SwaggerDefinitionsJSON.scala · line 3040 · SHA-256 0dda242ea754f0359967578bc4499e17a3c382359f0acb4bb6edcca1c07416ef_

```
Subject: CN=app.example.com
Issuer: CN=app.example.com
Serial: 18c10eb6474
Not before: 2023-11-27T13:15:11+00:00
Not after: 2025-11-26T13:15:11+00:00
Public key: RSA 2048-bit
Signature algorithm: 1.2.840.113549.1.1.11
Signature hash: sha256
CA: False
SAN: -
SHA-256 fingerprint: 25d91ac53796ca8c5598ee6d180ff0efb3919b4592b4ecef1c68fad35b20c726
```

**Limitations of the check.** Document-based analysis: only the supplied file was examined. Deployed configuration may differ; the result reflects the file content at the recorded SHA-256.

**Recommendation.** Renew the certificate and automate renewal (e.g. ACME) with expiry monitoring.

**Retest procedure.** Re-parse the deployed certificate and confirm notAfter is in the future.

### QSI-2026-17463 — org.postgresql:postgresql 42.7.11 is affected by GHSA-j92g-9f8w-j867 (CVE-2026-54291)

- Severity: **High** · Classification: Known vulnerable component · Confidence: Medium
- Affected asset: `dependency:Maven/org.postgresql:postgresql@42.7.11`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 10:11 UTC
- Priority score: 50.2 / 100
- CVSS v3.1: not applicable

OSV.dev reports GHSA-j92g-9f8w-j867 (CVE-2026-54291) for Maven package org.postgresql:postgresql at version 42.7.11: PostgreSQL JDBC Driver: Silent channel-binding authentication downgrade via unsupported certificate algorithms. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-j92g-9f8w-j867
```

**Evidence.**

_tool_output · [OSV.dev GHSA-j92g-9f8w-j867](https://osv.dev/vulnerability/GHSA-j92g-9f8w-j867) · manifest · SHA-256 55c1d9f6200b1c48b1ec20aadc0770bd4ba772d41d7dcb9e1a6c644af53e7224_

```
{"id": "GHSA-j92g-9f8w-j867", "aliases": ["BIT-postgresql-jdbc-driver-2026-54291", "CVE-2026-54291"], "modified": "2026-09-10T03:50:12.377062079Z", "summary": "PostgreSQL JDBC Driver: Silent channel-binding authentication downgrade via unsupported certificate algorithms", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:L/SA:N"}], "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (42.7.12).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-17464 — org.xerial.snappy:snappy-java 1.1.10.4 is affected by GHSA-gwq9-9ffj-mvrv (CVE-2026-93451)

- Severity: **High** · Classification: Known vulnerable component · Confidence: Medium
- Affected asset: `dependency:Maven/org.xerial.snappy:snappy-java@1.1.10.4`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 10:11 UTC
- Priority score: 50.2 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev reports GHSA-gwq9-9ffj-mvrv (CVE-2026-93451) for Maven package org.xerial.snappy:snappy-java at version 1.1.10.4: snappy-java: Heap buffer overflow in Snappy.uncompress*Array typed-array methods. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-gwq9-9ffj-mvrv
```

**Evidence.**

_tool_output · [OSV.dev GHSA-gwq9-9ffj-mvrv](https://osv.dev/vulnerability/GHSA-gwq9-9ffj-mvrv) · manifest · SHA-256 6d5b35cc7a996c80fc06ef703f1e363b13bb47e8ec5b56efeb43c6e796821485_

```
{"id": "GHSA-gwq9-9ffj-mvrv", "aliases": ["CVE-2026-93451"], "modified": "2026-10-27T15:47:24.498155855Z", "summary": "snappy-java: Heap buffer overflow in Snappy.uncompress*Array typed-array methods", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (1.1.10.9).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-17465 — org.xerial.snappy:snappy-java 1.1.10.4 is affected by GHSA-q233-g92q-qxp6 (CVE-2026-108106)

- Severity: **High** · Classification: Known vulnerable component · Confidence: Medium
- Affected asset: `dependency:Maven/org.xerial.snappy:snappy-java@1.1.10.4`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 10:11 UTC
- Priority score: 50.2 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev reports GHSA-q233-g92q-qxp6 (CVE-2026-108106) for Maven package org.xerial.snappy:snappy-java at version 1.1.10.4: snappy-java: Unbounded memory allocation from attacker-declared uncompressed lengtha. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-q233-g92q-qxp6
```

**Evidence.**

_tool_output · [OSV.dev GHSA-q233-g92q-qxp6](https://osv.dev/vulnerability/GHSA-q233-g92q-qxp6) · manifest · SHA-256 5073b30c7117c1a1ef15020ce616e3a0bcf16a0d253a90776aecf87dbd7452bb_

```
{"id": "GHSA-q233-g92q-qxp6", "aliases": ["CVE-2026-108106"], "modified": "2026-10-27T15:47:24.815707184Z", "summary": "snappy-java: Unbounded memory allocation from attacker-declared uncompressed lengtha", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (1.1.10.9).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-17468 — org.jsoup:jsoup 1.18.3 is affected by GHSA-65r4-943x-97jj (CVE-2026-75140)

- Severity: **High** · Classification: Known vulnerable component · Confidence: Medium
- Affected asset: `dependency:Maven/org.jsoup:jsoup@1.18.3`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 10:11 UTC
- Priority score: 50.2 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev reports GHSA-65r4-943x-97jj (CVE-2026-75140) for Maven package org.jsoup:jsoup at version 1.18.3: jsoup XmlTreeBuilder vulnerable to memory exhaustion through deeply nested namespace declarations. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-65r4-943x-97jj
```

**Evidence.**

_tool_output · [OSV.dev GHSA-65r4-943x-97jj](https://osv.dev/vulnerability/GHSA-65r4-943x-97jj) · manifest · SHA-256 a6eff01bbff30178abaee3aa9fb806714a8d0581e2b70b09ef81218280bad38e_

```
{"id": "GHSA-65r4-943x-97jj", "aliases": ["CVE-2026-75140"], "modified": "2026-10-05T22:45:05.710363586Z", "summary": "jsoup XmlTreeBuilder vulnerable to memory exhaustion through deeply nested namespace declarations", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}, {"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N"}], "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (1.23.2).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-17472 — com.rabbitmq:amqp-client 5.22.0 is affected by GHSA-68mj-5wr7-6fgg (CVE-2026-69219)

- Severity: **High** · Classification: Known vulnerable component · Confidence: Medium
- Affected asset: `dependency:Maven/com.rabbitmq:amqp-client@5.22.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 10:11 UTC
- Priority score: 50.2 / 100
- CVSS v3.1: not applicable

OSV.dev reports GHSA-68mj-5wr7-6fgg (CVE-2026-69219) for Maven package com.rabbitmq:amqp-client at version 5.22.0: RabbitMQ Java client ValueReader: Oversized LongString/bytes length triggers OOM via unchecked allocation. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-68mj-5wr7-6fgg
```

**Evidence.**

_tool_output · [OSV.dev GHSA-68mj-5wr7-6fgg](https://osv.dev/vulnerability/GHSA-68mj-5wr7-6fgg) · manifest · SHA-256 9fc76e6a96dae44b9054874bdf2053b4fbf9651977368fceabc281ca603b5b69_

```
{"id": "GHSA-68mj-5wr7-6fgg", "aliases": ["CVE-2026-69219"], "modified": "2026-09-10T03:51:13.151154373Z", "summary": "RabbitMQ Java client ValueReader: Oversized LongString/bytes length triggers OOM via unchecked allocation", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N"}], "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (5.33.1).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-17473 — com.rabbitmq:amqp-client 5.22.0 is affected by GHSA-6g32-pxv4-2wfj (CVE-2026-63337)

- Severity: **High** · Classification: Known vulnerable component · Confidence: Medium
- Affected asset: `dependency:Maven/com.rabbitmq:amqp-client@5.22.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 10:11 UTC
- Priority score: 50.2 / 100
- CVSS v3.1: not applicable

OSV.dev reports GHSA-6g32-pxv4-2wfj (CVE-2026-63337) for Maven package com.rabbitmq:amqp-client at version 5.22.0: RabbitMQ Java client: Unvalidated Class.forName in JSON-RPC ProcedureDescription enables arbitrary class loading. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-6g32-pxv4-2wfj
```

**Evidence.**

_tool_output · [OSV.dev GHSA-6g32-pxv4-2wfj](https://osv.dev/vulnerability/GHSA-6g32-pxv4-2wfj) · manifest · SHA-256 92932aefbff018b9d50b93c1dcf8c3a30a5adad8ea50f6788f1194b134e614a2_

```
{"id": "GHSA-6g32-pxv4-2wfj", "aliases": ["CVE-2026-63337"], "modified": "2026-09-10T03:51:13.214436792Z", "summary": "RabbitMQ Java client: Unvalidated Class.forName in JSON-RPC ProcedureDescription enables arbitrary class loading", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:P/VC:H/VI:H/VA:H/SC:L/SI:L/SA:L"}], "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (5.33.0).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-17475 — com.rabbitmq:amqp-client 5.22.0 is affected by GHSA-93j5-89vc-pph4 (CVE-2026-69220)

- Severity: **High** · Classification: Known vulnerable component · Confidence: Medium
- Affected asset: `dependency:Maven/com.rabbitmq:amqp-client@5.22.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 10:11 UTC
- Priority score: 50.2 / 100
- CVSS v3.1: not applicable

OSV.dev reports GHSA-93j5-89vc-pph4 (CVE-2026-69220) for Maven package com.rabbitmq:amqp-client at version 5.22.0: RabbitMQ Java client ValueReader: Unbounded recursive table/array nesting causes StackOverflowError DoS. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-93j5-89vc-pph4
```

**Evidence.**

_tool_output · [OSV.dev GHSA-93j5-89vc-pph4](https://osv.dev/vulnerability/GHSA-93j5-89vc-pph4) · manifest · SHA-256 7e4e5e4e72f01a35c97cc81070a5b3d7d7e514c7a266ea5ab4b73836cef44552_

```
{"id": "GHSA-93j5-89vc-pph4", "aliases": ["CVE-2026-69220"], "modified": "2026-09-10T03:51:13.771990072Z", "summary": "RabbitMQ Java client ValueReader: Unbounded recursive table/array nesting causes StackOverflowError DoS", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N"}], "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (5.33.1).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-17478 — com.rabbitmq:amqp-client 5.22.0 is affected by GHSA-jh4v-gfqj-7rhx (CVE-2026-75516)

- Severity: **High** · Classification: Known vulnerable component · Confidence: Medium
- Affected asset: `dependency:Maven/com.rabbitmq:amqp-client@5.22.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 10:11 UTC
- Priority score: 50.2 / 100
- CVSS v3.1: not applicable

OSV.dev reports GHSA-jh4v-gfqj-7rhx (CVE-2026-75516) for Maven package com.rabbitmq:amqp-client at version 5.22.0: RabbitMQ Java client has frame-level OOM: Math.min(maxInboundMessageBodySize, 0) defeats frame size enforcement. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-jh4v-gfqj-7rhx
```

**Evidence.**

_tool_output · [OSV.dev GHSA-jh4v-gfqj-7rhx](https://osv.dev/vulnerability/GHSA-jh4v-gfqj-7rhx) · manifest · SHA-256 e87721f84d12fb2772add1f51b05dcd3384dbd5627249697eaf3244dade8271a_

```
{"id": "GHSA-jh4v-gfqj-7rhx", "aliases": ["CVE-2026-75516"], "modified": "2026-09-17T15:00:06.805894716Z", "summary": "RabbitMQ Java client has frame-level OOM: Math.min(maxInboundMessageBodySize, 0) defeats frame size enforcement", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N"}], "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (5.34.0).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-17437 — Possible hard-coded secret in obp-api/src/main/resources/docs/introductory_system_documentation.md

- Severity: **High** · Classification: Confirmed configuration error · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `file:obp-api/src/main/resources/docs/introductory_system_documentation.md`
- Data source: obp-api/src/main/resources/docs/introductory_system_documentation.md
- Detection method: Regular-expression matching of language-specific API patterns.
- Analyzer: source_code 1.3.0 · 2026-11-06 10:11 UTC
- Priority score: 47.1 / 100
- CVSS v3.1: not applicable

1 secret-like value(s) of type generic_assignment (first at line 5126). Values were redacted by QSI.

**Potential impact.** Credentials in source code leak through repositories, builds and logs.

**Reproduction steps.**

```
Open line 5126 in the supplied file obp-api/src/main/resources/docs/introductory_system_documentation.md and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [obp-api/src/main/resources/docs/introductory_system_documentation.md](https://github.com/OpenBankProject/OBP-API/blob/6a4a13ef079fa33707f4ee3dba1e600570ed34b4/obp-api/src/main/resources/docs/introductory_system_documentation.md#L5126) · line 5126 · SHA-256 9f978bb1c5c0376841869923240b332ccf2e14a3e17db416ed08cd0973f45105_

```
 5126 | Authorization: DirectLogin token="[REDACTED]"
```

**Limitations of the check.** Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Move secrets to a secrets manager/environment; rotate the exposed values.

**Retest procedure.** Re-scan the source and review the call sites listed in the evidence.

### QSI-2026-17442 — Possible hard-coded secret in obp-api/src/main/resources/props/sample.props.template

- Severity: **High** · Classification: Confirmed configuration error · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `file:obp-api/src/main/resources/props/sample.props.template`
- Data source: obp-api/src/main/resources/props/sample.props.template
- Detection method: Regular-expression matching of language-specific API patterns.
- Analyzer: source_code 1.3.0 · 2026-11-06 10:11 UTC
- Priority score: 47.1 / 100
- CVSS v3.1: not applicable

8 secret-like value(s) of type generic_assignment (first at line 188). Values were redacted by QSI.

**Potential impact.** Credentials in source code leak through repositories, builds and logs.

**Reproduction steps.**

```
Open line 188 in the supplied file obp-api/src/main/resources/props/sample.props.template and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [obp-api/src/main/resources/props/sample.props.template](https://github.com/OpenBankProject/OBP-API/blob/6a4a13ef079fa33707f4ee3dba1e600570ed34b4/obp-api/src/main/resources/props/sample.props.template#L188) · line 188 · SHA-256 df11d02a34608f03117e05f5847be146d57d14e0ebc91e25fe9d518ea2a13a4b_

```
  188 | #keystore.password = [REDACTED]
```

_file_excerpt · [obp-api/src/main/resources/props/sample.props.template](https://github.com/OpenBankProject/OBP-API/blob/6a4a13ef079fa33707f4ee3dba1e600570ed34b4/obp-api/src/main/resources/props/sample.props.template#L376) · line 376 · SHA-256 f0f11bd616c66694efa8205b409b798d5cf38082be608c607e22ed4be49a50a0_

```
  376 | #db.url=jdbc:postgresql://localhost:5432/dbname?user=dbusername&password=[REDACTED]
```

_file_excerpt · [obp-api/src/main/resources/props/sample.props.template](https://github.com/OpenBankProject/OBP-API/blob/6a4a13ef079fa33707f4ee3dba1e600570ed34b4/obp-api/src/main/resources/props/sample.props.template#L620) · line 620 · SHA-256 dbb4be7d2ab4e338bd2bbafd1bed3b01a4534e4dfa0c424cd8a3cdd7733cd792_

```
  620 | connection.password=[REDACTED]
```

_file_excerpt · [obp-api/src/main/resources/props/sample.props.template](https://github.com/OpenBankProject/OBP-API/blob/6a4a13ef079fa33707f4ee3dba1e600570ed34b4/obp-api/src/main/resources/props/sample.props.template#L1042) · line 1042 · SHA-256 f3a4617d419ff641ad81d4ea4de4be5f480060627cfb142862c1ef931b63d0e6_

```
 1042 | # jwt_token_secret=[REDACTED]
```

_file_excerpt · [obp-api/src/main/resources/props/sample.props.template](https://github.com/OpenBankProject/OBP-API/blob/6a4a13ef079fa33707f4ee3dba1e600570ed34b4/obp-api/src/main/resources/props/sample.props.template#L1457) · line 1457 · SHA-256 5e7423eb90ed12159e10fa94d2f819be7778397860e99c3a0032ec377f81eb74_

```
 1457 | # sca_phone_api_key = [REDACTED]
```

**Limitations of the check.** Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Move secrets to a secrets manager/environment; rotate the exposed values.

**Retest procedure.** Re-scan the source and review the call sites listed in the evidence.

### QSI-2026-17447 — Possible hard-coded secret in obp-api/src/main/scala/code/api/util/APIUtil.scala

- Severity: **High** · Classification: Confirmed configuration error · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `file:obp-api/src/main/scala/code/api/util/APIUtil.scala`
- Data source: obp-api/src/main/scala/code/api/util/APIUtil.scala
- Detection method: Regular-expression matching of language-specific API patterns.
- Analyzer: source_code 1.3.0 · 2026-11-06 10:11 UTC
- Priority score: 47.1 / 100
- CVSS v3.1: not applicable

2 secret-like value(s) of type jwt (first at line 2917). Values were redacted by QSI.

**Potential impact.** Credentials in source code leak through repositories, builds and logs.

**Reproduction steps.**

```
Open line 2917 in the supplied file obp-api/src/main/scala/code/api/util/APIUtil.scala and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [obp-api/src/main/scala/code/api/util/APIUtil.scala](https://github.com/OpenBankProject/OBP-API/blob/6a4a13ef079fa33707f4ee3dba1e600570ed34b4/obp-api/src/main/scala/code/api/util/APIUtil.scala#L2917) · line 2917 · SHA-256 71dee0294a08de49a803c572db3a855e6ec543c3780db750e55a709ec8fc0372_

```
 2917 |       } // Direct Login i.e DirectLogin: token=[REDACTED]
```

_file_excerpt · [obp-api/src/main/scala/code/api/util/APIUtil.scala](https://github.com/OpenBankProject/OBP-API/blob/6a4a13ef079fa33707f4ee3dba1e600570ed34b4/obp-api/src/main/scala/code/api/util/APIUtil.scala#L2920) · line 2920 · SHA-256 598c88fda54708850cf3b23fd58e904fcdedb8b706a6b2fd414db9ed8fda2c4d_

```
 2920 |       } // Direct Login Deprecated i.e Authorization: DirectLogin token=[REDACTED]
```

**Limitations of the check.** Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Move secrets to a secrets manager/environment; rotate the exposed values.

**Retest procedure.** Re-scan the source and review the call sites listed in the evidence.

### QSI-2026-17450 — Possible hard-coded secret in obp-api/src/main/scala/code/api/util/DBUtil.scala

- Severity: **High** · Classification: Confirmed configuration error · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `file:obp-api/src/main/scala/code/api/util/DBUtil.scala`
- Data source: obp-api/src/main/scala/code/api/util/DBUtil.scala
- Detection method: Regular-expression matching of language-specific API patterns.
- Analyzer: source_code 1.3.0 · 2026-11-06 10:11 UTC
- Priority score: 47.1 / 100
- CVSS v3.1: not applicable

1 secret-like value(s) of type generic_assignment (first at line 133). Values were redacted by QSI.

**Potential impact.** Credentials in source code leak through repositories, builds and logs.

**Reproduction steps.**

```
Open line 133 in the supplied file obp-api/src/main/scala/code/api/util/DBUtil.scala and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [obp-api/src/main/scala/code/api/util/DBUtil.scala](https://github.com/OpenBankProject/OBP-API/blob/6a4a13ef079fa33707f4ee3dba1e600570ed34b4/obp-api/src/main/scala/code/api/util/DBUtil.scala#L133) · line 133 · SHA-256 8d79aa1324583ed3744c9d9a299e2c1a7bd1a9a2e9a1c80b4d9b5f27de0531ad_

```
  133 |     val password = [REDACTED]"password="[REDACTED]"=", 2)(1))
```

**Limitations of the check.** Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Move secrets to a secrets manager/environment; rotate the exposed values.

**Retest procedure.** Re-scan the source and review the call sites listed in the evidence.

### QSI-2026-17452 — Possible hard-coded secret in obp-api/src/main/scala/code/api/util/Glossary.scala

- Severity: **High** · Classification: Confirmed configuration error · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `file:obp-api/src/main/scala/code/api/util/Glossary.scala`
- Data source: obp-api/src/main/scala/code/api/util/Glossary.scala
- Detection method: Regular-expression matching of language-specific API patterns.
- Analyzer: source_code 1.3.0 · 2026-11-06 10:11 UTC
- Priority score: 47.1 / 100
- CVSS v3.1: not applicable

9 secret-like value(s) of type jwt (first at line 1921). Values were redacted by QSI.

**Potential impact.** Credentials in source code leak through repositories, builds and logs.

**Reproduction steps.**

```
Open line 1921 in the supplied file obp-api/src/main/scala/code/api/util/Glossary.scala and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [obp-api/src/main/scala/code/api/util/Glossary.scala](https://github.com/OpenBankProject/OBP-API/blob/6a4a13ef079fa33707f4ee3dba1e600570ed34b4/obp-api/src/main/scala/code/api/util/Glossary.scala#L1921) · line 1921 · SHA-256 4708c10c4b5fb11bc041319b4bc40a1fa52f5bc62af9b0c8e40403e45b3d2667_

```
 1921 | 					|  "jwt":"[REDACTED]",
```

_file_excerpt · [obp-api/src/main/scala/code/api/util/Glossary.scala](https://github.com/OpenBankProject/OBP-API/blob/6a4a13ef079fa33707f4ee3dba1e600570ed34b4/obp-api/src/main/scala/code/api/util/Glossary.scala#L1945) · line 1945 · SHA-256 4f06874b3860c92e8bbdb6ec50403b393db5dcc2be72e5b209b92ff42505d318_

```
 1945 | 					|  "jwt":"[REDACTED]",
```

_file_excerpt · [obp-api/src/main/scala/code/api/util/Glossary.scala](https://github.com/OpenBankProject/OBP-API/blob/6a4a13ef079fa33707f4ee3dba1e600570ed34b4/obp-api/src/main/scala/code/api/util/Glossary.scala#L1959) · line 1959 · SHA-256 3b0bef94c8711fb9e3d87dc3784bb4c814ba08cb34e8feb8782c96bf01b86951_

```
 1959 | 					|Consent-JWT:[REDACTED]-
```

_file_excerpt · [obp-api/src/main/scala/code/api/util/Glossary.scala](https://github.com/OpenBankProject/OBP-API/blob/6a4a13ef079fa33707f4ee3dba1e600570ed34b4/obp-api/src/main/scala/code/api/util/Glossary.scala#L2837) · line 2837 · SHA-256 ede5831572efc3ed16bc09c2f92a0620ebdda1343919a840f320afc8e3f52f04_

```
 2837 | |  "id_token": "[REDACTED]",
```

_file_excerpt · [obp-api/src/main/scala/code/api/util/Glossary.scala](https://github.com/OpenBankProject/OBP-API/blob/6a4a13ef079fa33707f4ee3dba1e600570ed34b4/obp-api/src/main/scala/code/api/util/Glossary.scala#L2887) · line 2887 · SHA-256 34ee566587e35991522cf914b2ba3b377ad0a42e11516d4ee32b3a7190219f7c_

```
 2887 | |		Authorization: Bearer [REDACTED]
```

**Limitations of the check.** Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Move secrets to a secrets manager/environment; rotate the exposed values.

**Retest procedure.** Re-scan the source and review the call sites listed in the evidence.

### QSI-2026-17453 — Possible hard-coded secret in obp-api/src/main/scala/code/api/util/JwtUtil.scala

- Severity: **High** · Classification: Confirmed configuration error · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `file:obp-api/src/main/scala/code/api/util/JwtUtil.scala`
- Data source: obp-api/src/main/scala/code/api/util/JwtUtil.scala
- Detection method: Regular-expression matching of language-specific API patterns.
- Analyzer: source_code 1.3.0 · 2026-11-06 10:11 UTC
- Priority score: 47.1 / 100
- CVSS v3.1: not applicable

4 secret-like value(s) of type generic_assignment, jwt (first at line 361). Values were redacted by QSI.

**Potential impact.** Credentials in source code leak through repositories, builds and logs.

**Reproduction steps.**

```
Open line 361 in the supplied file obp-api/src/main/scala/code/api/util/JwtUtil.scala and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [obp-api/src/main/scala/code/api/util/JwtUtil.scala](https://github.com/OpenBankProject/OBP-API/blob/6a4a13ef079fa33707f4ee3dba1e600570ed34b4/obp-api/src/main/scala/code/api/util/JwtUtil.scala#L361) · line 361 · SHA-256 8bcc65a156f914bca64220235edf4abc0d367aebe05508bd62f52d95fb5edf6d_

```
  361 |     val jwtToken = "[REDACTED]"
```

_file_excerpt · [obp-api/src/main/scala/code/api/util/JwtUtil.scala](https://github.com/OpenBankProject/OBP-API/blob/6a4a13ef079fa33707f4ee3dba1e600570ed34b4/obp-api/src/main/scala/code/api/util/JwtUtil.scala#L366) · line 366 · SHA-256 04e0c67dadb67261e5c2398bd40af6f8d125080cbf33bee5bcf485ab3282d4e1_

```
  366 |     val idToken = "[REDACTED]"
```

_file_excerpt · [obp-api/src/main/scala/code/api/util/JwtUtil.scala](https://github.com/OpenBankProject/OBP-API/blob/6a4a13ef079fa33707f4ee3dba1e600570ed34b4/obp-api/src/main/scala/code/api/util/JwtUtil.scala#L361) · line 361 · SHA-256 8bcc65a156f914bca64220235edf4abc0d367aebe05508bd62f52d95fb5edf6d_

```
  361 |     val jwtToken = "[REDACTED]"
```

_file_excerpt · [obp-api/src/main/scala/code/api/util/JwtUtil.scala](https://github.com/OpenBankProject/OBP-API/blob/6a4a13ef079fa33707f4ee3dba1e600570ed34b4/obp-api/src/main/scala/code/api/util/JwtUtil.scala#L366) · line 366 · SHA-256 04e0c67dadb67261e5c2398bd40af6f8d125080cbf33bee5bcf485ab3282d4e1_

```
  366 |     val idToken = "[REDACTED]"
```

**Limitations of the check.** Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Move secrets to a secrets manager/environment; rotate the exposed values.

**Retest procedure.** Re-scan the source and review the call sites listed in the evidence.

### QSI-2026-17455 — Possible hard-coded secret in obp-api/src/main/scala/code/api/v3_1_0/Http4s310.scala

- Severity: **High** · Classification: Confirmed configuration error · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `file:obp-api/src/main/scala/code/api/v3_1_0/Http4s310.scala`
- Data source: obp-api/src/main/scala/code/api/v3_1_0/Http4s310.scala
- Detection method: Regular-expression matching of language-specific API patterns.
- Analyzer: source_code 1.3.0 · 2026-11-06 10:11 UTC
- Priority score: 47.1 / 100
- CVSS v3.1: not applicable

1 secret-like value(s) of type jwt (first at line 4917). Values were redacted by QSI.

**Potential impact.** Credentials in source code leak through repositories, builds and logs.

**Reproduction steps.**

```
Open line 4917 in the supplied file obp-api/src/main/scala/code/api/v3_1_0/Http4s310.scala and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [obp-api/src/main/scala/code/api/v3_1_0/Http4s310.scala](https://github.com/OpenBankProject/OBP-API/blob/6a4a13ef079fa33707f4ee3dba1e600570ed34b4/obp-api/src/main/scala/code/api/v3_1_0/Http4s310.scala#L4917) · line 4917 · SHA-256 45aaa17be5f95a3f493a3cbf041cc62deb5c8aa44055cfd7701c12116bfc7e0d_

```
 4917 |         jwt = "[REDACTED]",
```

**Limitations of the check.** Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Move secrets to a secrets manager/environment; rotate the exposed values.

**Retest procedure.** Re-scan the source and review the call sites listed in the evidence.

### QSI-2026-17456 — Possible hard-coded secret in obp-api/src/main/scala/code/api/v4_0_0/Http4s400.scala

- Severity: **High** · Classification: Confirmed configuration error · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `file:obp-api/src/main/scala/code/api/v4_0_0/Http4s400.scala`
- Data source: obp-api/src/main/scala/code/api/v4_0_0/Http4s400.scala
- Detection method: Regular-expression matching of language-specific API patterns.
- Analyzer: source_code 1.3.0 · 2026-11-06 10:11 UTC
- Priority score: 47.1 / 100
- CVSS v3.1: not applicable

2 secret-like value(s) of type jwt (first at line 5587). Values were redacted by QSI.

**Potential impact.** Credentials in source code leak through repositories, builds and logs.

**Reproduction steps.**

```
Open line 5587 in the supplied file obp-api/src/main/scala/code/api/v4_0_0/Http4s400.scala and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [obp-api/src/main/scala/code/api/v4_0_0/Http4s400.scala](https://github.com/OpenBankProject/OBP-API/blob/6a4a13ef079fa33707f4ee3dba1e600570ed34b4/obp-api/src/main/scala/code/api/v4_0_0/Http4s400.scala#L5587) · line 5587 · SHA-256 1415241fc995e35fffd9ed487c8e7002f1c99a5765fef5a7b82daaa20e163add_

```
 5587 |             "[REDACTED]",
```

_file_excerpt · [obp-api/src/main/scala/code/api/v4_0_0/Http4s400.scala](https://github.com/OpenBankProject/OBP-API/blob/6a4a13ef079fa33707f4ee3dba1e600570ed34b4/obp-api/src/main/scala/code/api/v4_0_0/Http4s400.scala#L5619) · line 5619 · SHA-256 a7a854d4f794bc161f027a27f009158d9c76b885d0c4b002339635a6931ec095_

```
 5619 |             "[REDACTED]",
```

**Limitations of the check.** Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Move secrets to a secrets manager/environment; rotate the exposed values.

**Retest procedure.** Re-scan the source and review the call sites listed in the evidence.

### QSI-2026-17457 — Possible hard-coded secret in obp-api/src/main/scala/code/api/v5_1_0/Http4s510.scala

- Severity: **High** · Classification: Confirmed configuration error · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `file:obp-api/src/main/scala/code/api/v5_1_0/Http4s510.scala`
- Data source: obp-api/src/main/scala/code/api/v5_1_0/Http4s510.scala
- Detection method: Regular-expression matching of language-specific API patterns.
- Analyzer: source_code 1.3.0 · 2026-11-06 10:11 UTC
- Priority score: 47.1 / 100
- CVSS v3.1: not applicable

4 secret-like value(s) of type jwt (first at line 3327). Values were redacted by QSI.

**Potential impact.** Credentials in source code leak through repositories, builds and logs.

**Reproduction steps.**

```
Open line 3327 in the supplied file obp-api/src/main/scala/code/api/v5_1_0/Http4s510.scala and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [obp-api/src/main/scala/code/api/v5_1_0/Http4s510.scala](https://github.com/OpenBankProject/OBP-API/blob/6a4a13ef079fa33707f4ee3dba1e600570ed34b4/obp-api/src/main/scala/code/api/v5_1_0/Http4s510.scala#L3327) · line 3327 · SHA-256 14aa4e819e9718f8a9ad41ad1be753dfc2216f342019bcad8607888e222fe488_

```
 3327 |       ConsumerJwtPostJsonV510("[REDACTED]"),
```

_file_excerpt · [obp-api/src/main/scala/code/api/v5_1_0/Http4s510.scala](https://github.com/OpenBankProject/OBP-API/blob/6a4a13ef079fa33707f4ee3dba1e600570ed34b4/obp-api/src/main/scala/code/api/v5_1_0/Http4s510.scala#L4329) · line 4329 · SHA-256 5fb105bd40a5ea95aa566deae841675ce6761fa95bbf736f5a267aa01ab33867_

```
 4329 |         jwt = "[REDACTED]",
```

_file_excerpt · [obp-api/src/main/scala/code/api/v5_1_0/Http4s510.scala](https://github.com/OpenBankProject/OBP-API/blob/6a4a13ef079fa33707f4ee3dba1e600570ed34b4/obp-api/src/main/scala/code/api/v5_1_0/Http4s510.scala#L4385) · line 4385 · SHA-256 b6fb5fc9b9fda1be1e1ae4623e78f7a4dd2655b8024a4c7a130cd1bbb66b33ae_

```
 4385 |         jwt = "[REDACTED]",
```

_file_excerpt · [obp-api/src/main/scala/code/api/v5_1_0/Http4s510.scala](https://github.com/OpenBankProject/OBP-API/blob/6a4a13ef079fa33707f4ee3dba1e600570ed34b4/obp-api/src/main/scala/code/api/v5_1_0/Http4s510.scala#L4441) · line 4441 · SHA-256 23843f240713d2c6e1c6df18302654109d8f2cd74eb3e004468bcec7203fd03e_

```
 4441 |         jwt = "[REDACTED]",
```

**Limitations of the check.** Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Move secrets to a secrets manager/environment; rotate the exposed values.

**Retest procedure.** Re-scan the source and review the call sites listed in the evidence.

### QSI-2026-17458 — Possible hard-coded secret in obp-api/src/main/scala/code/api/v6_0_0/Http4s600.scala

- Severity: **High** · Classification: Confirmed configuration error · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `file:obp-api/src/main/scala/code/api/v6_0_0/Http4s600.scala`
- Data source: obp-api/src/main/scala/code/api/v6_0_0/Http4s600.scala
- Detection method: Regular-expression matching of language-specific API patterns.
- Analyzer: source_code 1.3.0 · 2026-11-06 10:11 UTC
- Priority score: 47.1 / 100
- CVSS v3.1: not applicable

3 secret-like value(s) of type generic_assignment, jwt (first at line 9610). Values were redacted by QSI.

**Potential impact.** Credentials in source code leak through repositories, builds and logs.

**Reproduction steps.**

```
Open line 9610 in the supplied file obp-api/src/main/scala/code/api/v6_0_0/Http4s600.scala and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [obp-api/src/main/scala/code/api/v6_0_0/Http4s600.scala](https://github.com/OpenBankProject/OBP-API/blob/6a4a13ef079fa33707f4ee3dba1e600570ed34b4/obp-api/src/main/scala/code/api/v6_0_0/Http4s600.scala#L13221) · line 13221 · SHA-256 c7c551212314b66ce60393df810044aaa5756a26d876615c4faace12aed9eb76_

```
13221 |           JSONFactory600.createTokenJSON("[REDACTED]"),
```

_file_excerpt · [obp-api/src/main/scala/code/api/v6_0_0/Http4s600.scala](https://github.com/OpenBankProject/OBP-API/blob/6a4a13ef079fa33707f4ee3dba1e600570ed34b4/obp-api/src/main/scala/code/api/v6_0_0/Http4s600.scala#L9610) · line 9610 · SHA-256 30bb303e069156eb4c167e6b14a7139d29f488878793241be5fec759e34e1cdd_

```
 9610 |           client_secret = "[REDACTED]"
```

_file_excerpt · [obp-api/src/main/scala/code/api/v6_0_0/Http4s600.scala](https://github.com/OpenBankProject/OBP-API/blob/6a4a13ef079fa33707f4ee3dba1e600570ed34b4/obp-api/src/main/scala/code/api/v6_0_0/Http4s600.scala#L12748) · line 12748 · SHA-256 29aedecdc352e146b7a9ac91d114a9c77e2e52066c4942ca4b513eca8370860a_

```
12748 |             token = "[REDACTED]"
```

**Limitations of the check.** Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Move secrets to a secrets manager/environment; rotate the exposed values.

**Retest procedure.** Re-scan the source and review the call sites listed in the evidence.

### QSI-2026-17459 — Possible hard-coded secret in obp-api/src/main/scala/code/paymetngateway/StripeExample.scala

- Severity: **High** · Classification: Confirmed configuration error · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `file:obp-api/src/main/scala/code/paymetngateway/StripeExample.scala`
- Data source: obp-api/src/main/scala/code/paymetngateway/StripeExample.scala
- Detection method: Regular-expression matching of language-specific API patterns.
- Analyzer: source_code 1.3.0 · 2026-11-06 10:11 UTC
- Priority score: 47.1 / 100
- CVSS v3.1: not applicable

1 secret-like value(s) of type generic_assignment (first at line 42). Values were redacted by QSI.

**Potential impact.** Credentials in source code leak through repositories, builds and logs.

**Reproduction steps.**

```
Open line 42 in the supplied file obp-api/src/main/scala/code/paymetngateway/StripeExample.scala and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [obp-api/src/main/scala/code/paymetngateway/StripeExample.scala](https://github.com/OpenBankProject/OBP-API/blob/6a4a13ef079fa33707f4ee3dba1e600570ed34b4/obp-api/src/main/scala/code/paymetngateway/StripeExample.scala#L42) · line 42 · SHA-256 4832568d60d673765255866449deea640cc2b6cb1d05ee3cdf1f1c8b19adbeb8_

```
   42 |     Stripe.apiKey = "[REDACTED]"
```

**Limitations of the check.** Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Move secrets to a secrets manager/environment; rotate the exposed values.

**Retest procedure.** Re-scan the source and review the call sites listed in the evidence.

### QSI-2026-17460 — Possible hard-coded secret in obp-api/src/main/scala/code/sandbox/OBPDataImport.scala

- Severity: **High** · Classification: Confirmed configuration error · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `file:obp-api/src/main/scala/code/sandbox/OBPDataImport.scala`
- Data source: obp-api/src/main/scala/code/sandbox/OBPDataImport.scala
- Detection method: Regular-expression matching of language-specific API patterns.
- Analyzer: source_code 1.3.0 · 2026-11-06 10:11 UTC
- Priority score: 47.1 / 100
- CVSS v3.1: not applicable

2 secret-like value(s) of type generic_assignment (first at line 815). Values were redacted by QSI.

**Potential impact.** Credentials in source code leak through repositories, builds and logs.

**Reproduction steps.**

```
Open line 815 in the supplied file obp-api/src/main/scala/code/sandbox/OBPDataImport.scala and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [obp-api/src/main/scala/code/sandbox/OBPDataImport.scala](https://github.com/OpenBankProject/OBP-API/blob/6a4a13ef079fa33707f4ee3dba1e600570ed34b4/obp-api/src/main/scala/code/sandbox/OBPDataImport.scala#L815) · line 815 · SHA-256 8ffc27b6c250f11a97e5a35889799272cb27867a9b2b93e2d6d0cfcbee114b46_

```
  815 |   val user1 = SandboxUserImport(email = "user1@example.com", password = "[REDACTED]", user_name = "User 1")
```

_file_excerpt · [obp-api/src/main/scala/code/sandbox/OBPDataImport.scala](https://github.com/OpenBankProject/OBP-API/blob/6a4a13ef079fa33707f4ee3dba1e600570ed34b4/obp-api/src/main/scala/code/sandbox/OBPDataImport.scala#L816) · line 816 · SHA-256 9784bcbafb4b541a11c4d482c1e1aade8b47ac85cd53dcb29ce3ef100ef3d50a_

```
  816 |   val user2 = SandboxUserImport(email = "user2@example.com", password = "[REDACTED]", user_name = "User 2")
```

**Limitations of the check.** Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Move secrets to a secrets manager/environment; rotate the exposed values.

**Retest procedure.** Re-scan the source and review the call sites listed in the evidence.

### QSI-2026-17461 — Possible hard-coded secret in scripts/resource_doc_baseline/lift_resource_docs_v4_0_0.json

- Severity: **High** · Classification: Confirmed configuration error · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `file:scripts/resource_doc_baseline/lift_resource_docs_v4_0_0.json`
- Data source: scripts/resource_doc_baseline/lift_resource_docs_v4_0_0.json
- Detection method: Regular-expression matching of language-specific API patterns.
- Analyzer: source_code 1.3.0 · 2026-11-06 10:11 UTC
- Priority score: 47.1 / 100
- CVSS v3.1: not applicable

3 secret-like value(s) of type generic_assignment, jwt (first at line 784). Values were redacted by QSI.

**Potential impact.** Credentials in source code leak through repositories, builds and logs.

**Reproduction steps.**

```
Open line 784 in the supplied file scripts/resource_doc_baseline/lift_resource_docs_v4_0_0.json and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [scripts/resource_doc_baseline/lift_resource_docs_v4_0_0.json](https://github.com/OpenBankProject/OBP-API/blob/6a4a13ef079fa33707f4ee3dba1e600570ed34b4/scripts/resource_doc_baseline/lift_resource_docs_v4_0_0.json#L2038) · line 2038 · SHA-256 9a892ce1aed017955c3b2e2bf0d8eae91ca2c2880b786b8c18d47902210d76e7_

```
 2038 |       "success_response_body": "ConsentChallengeJsonV310(\n       consent_id = \"9d429899-24f5-42c8-8565-943ffa6a7945\",\n       jwt =\n         \"[REDACTED]\",\n       status = \"AUTHORISED\"\n     )",
```

_file_excerpt · [scripts/resource_doc_baseline/lift_resource_docs_v4_0_0.json](https://github.com/OpenBankProject/OBP-API/blob/6a4a13ef079fa33707f4ee3dba1e600570ed34b4/scripts/resource_doc_baseline/lift_resource_docs_v4_0_0.json#L2049) · line 2049 · SHA-256 257915153b75ccbb2b08e6f7b90823309a3fa24b0db460e4044eafc4c91dcaed_

```
 2049 |       "success_response_body": "ConsentChallengeJsonV310(\n       consent_id = \"9d429899-24f5-42c8-8565-943ffa6a7945\",\n       jwt =\n         \"[REDACTED]\",\n       status = \"AUTHORISED\"\n     )",
```

_file_excerpt · [scripts/resource_doc_baseline/lift_resource_docs_v4_0_0.json](https://github.com/OpenBankProject/OBP-API/blob/6a4a13ef079fa33707f4ee3dba1e600570ed34b4/scripts/resource_doc_baseline/lift_resource_docs_v4_0_0.json#L784) · line 784 · SHA-256 4d569836ba65f375f67efdc78b0a2c53f98844ab28da46a25e5da2d01357007d_

```
  784 |       "example_request_body": "PostUserInvitationAnonymousJsonV400(secret_key = [REDACTED]",
```

**Limitations of the check.** Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Move secrets to a secrets manager/environment; rotate the exposed values.

**Retest procedure.** Re-scan the source and review the call sites listed in the evidence.

### QSI-2026-17454 — ECB block-cipher mode used in obp-api/src/main/scala/code/api/util/RSAUtil.scala

- Severity: **High** · Classification: Potential cryptographic risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `file:obp-api/src/main/scala/code/api/util/RSAUtil.scala`
- Data source: obp-api/src/main/scala/code/api/util/RSAUtil.scala
- Detection method: Regular-expression matching of language-specific API patterns.
- Analyzer: source_code 1.3.0 · 2026-11-06 10:11 UTC
- Priority score: 38.8 / 100
- CVSS v3.1: not applicable

1 usage(s) of ECB mode (first at line 44).

**Potential impact.** ECB reveals patterns in encrypted data and provides no integrity.

**Reproduction steps.**

```
Open line 44 in the supplied file obp-api/src/main/scala/code/api/util/RSAUtil.scala and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [obp-api/src/main/scala/code/api/util/RSAUtil.scala](https://github.com/OpenBankProject/OBP-API/blob/6a4a13ef079fa33707f4ee3dba1e600570ed34b4/obp-api/src/main/scala/code/api/util/RSAUtil.scala#L44) · line 44 · SHA-256 ab13caf4ff64072500643bdfdf68089d20200e31b8d0b9150f5fb52efdcebdb2_

```
   42 | object RSAUtil  extends MdcLoggable {
   43 | 
   44 |   val cryptoSystem = "RSA/ECB/OAEPWithSHA-256AndMGF1Padding"
   45 | 
   46 |   def encrypt(text: String): String = {
```

**Limitations of the check.** Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Use an AEAD mode (GCM) with unique nonces.

**Retest procedure.** Re-scan the source and review the call sites listed in the evidence.

### QSI-2026-17466 — org.xerial.snappy:snappy-java 1.1.10.4 is affected by GHSA-xqrx-qh46-34m7 (CVE-2026-116590)

- Severity: **Medium** · Classification: Known vulnerable component · Confidence: Medium
- Affected asset: `dependency:Maven/org.xerial.snappy:snappy-java@1.1.10.4`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 10:11 UTC
- Priority score: 44.2 / 100
- CVSS v3.1: 5.9 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev reports GHSA-xqrx-qh46-34m7 (CVE-2026-116590) for Maven package org.xerial.snappy:snappy-java at version 1.1.10.4: snappy-java: JVM crash from unchecked ranges in Snappy.arrayCopy and SnappyOutputStream.rawWrite. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-xqrx-qh46-34m7
```

**Evidence.**

_tool_output · [OSV.dev GHSA-xqrx-qh46-34m7](https://osv.dev/vulnerability/GHSA-xqrx-qh46-34m7) · manifest · SHA-256 1e47744c23c7bc7c5a2cc81dccdb3b7859b21b8e763bfd822f71f74a4c255a4e_

```
{"id": "GHSA-xqrx-qh46-34m7", "aliases": ["CVE-2026-116590"], "modified": "2026-10-27T15:47:25.122359555Z", "summary": "snappy-java: JVM crash from unchecked ranges in Snappy.arrayCopy and SnappyOutputStream.rawWrite", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (1.1.10.9).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-17467 — org.apache.logging.log4j:log4j-api 2.26.0 is affected by GHSA-qv9r-c865-cp47 (CVE-2026-49844)

- Severity: **Medium** · Classification: Known vulnerable component · Confidence: Medium
- Affected asset: `dependency:Maven/org.apache.logging.log4j:log4j-api@2.26.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 10:11 UTC
- Priority score: 44.2 / 100
- CVSS v3.1: not applicable

OSV.dev reports GHSA-qv9r-c865-cp47 (CVE-2026-49844) for Maven package org.apache.logging.log4j:log4j-api at version 2.26.0: Apache Log4j API: Improper encoding of non-finite floating-point values during MapMessage JSON serialization. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-qv9r-c865-cp47
```

**Evidence.**

_tool_output · [OSV.dev GHSA-qv9r-c865-cp47](https://osv.dev/vulnerability/GHSA-qv9r-c865-cp47) · manifest · SHA-256 207fe7bc67e70e467ef1d013e612b27907f364586b7c52357b02838051a586d6_

```
{"id": "GHSA-qv9r-c865-cp47", "aliases": ["CVE-2026-49844"], "modified": "2026-09-10T03:50:52.972700022Z", "summary": "Apache Log4j API: Improper encoding of non-finite floating-point values during MapMessage JSON serialization", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:N/SC:N/SI:L/SA:N"}], "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (2.25.5, 2.26.1).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-17469 — org.jsoup:jsoup 1.18.3 is affected by GHSA-pmhh-3w7g-xqp8 (CVE-2026-71497)

- Severity: **Medium** · Classification: Known vulnerable component · Confidence: Medium
- Affected asset: `dependency:Maven/org.jsoup:jsoup@1.18.3`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 10:11 UTC
- Priority score: 44.2 / 100
- CVSS v3.1: 4.7 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:L/I:L/A:N`)

OSV.dev reports GHSA-pmhh-3w7g-xqp8 (CVE-2026-71497) for Maven package org.jsoup:jsoup at version 1.18.3: jsoup: Cleaner may expose markup with custom raw-text elements. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-pmhh-3w7g-xqp8
```

**Evidence.**

_tool_output · [OSV.dev GHSA-pmhh-3w7g-xqp8](https://osv.dev/vulnerability/GHSA-pmhh-3w7g-xqp8) · manifest · SHA-256 78cdc8fec250f8e99ff0773dc821860d621c1b52fa8ac8885a9452e315160a4a_

```
{"id": "GHSA-pmhh-3w7g-xqp8", "aliases": ["CVE-2026-71497"], "modified": "2026-09-10T03:50:53.809983880Z", "summary": "jsoup: Cleaner may expose markup with custom raw-text elements", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:L/I:L/A:N"}], "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (1.23.1).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-17470 — com.rabbitmq:amqp-client 5.22.0 is affected by GHSA-5m9f-rphj-c435 (CVE-2026-63336)

- Severity: **Medium** · Classification: Known vulnerable component · Confidence: Medium
- Affected asset: `dependency:Maven/com.rabbitmq:amqp-client@5.22.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 10:11 UTC
- Priority score: 44.2 / 100
- CVSS v3.1: not applicable

OSV.dev reports GHSA-5m9f-rphj-c435 (CVE-2026-63336) for Maven package com.rabbitmq:amqp-client at version 5.22.0: RabbitMQ Java client: TrustEverythingTrustManager used by default in useSslProtocol() enables MITM. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-5m9f-rphj-c435
```

**Evidence.**

_tool_output · [OSV.dev GHSA-5m9f-rphj-c435](https://osv.dev/vulnerability/GHSA-5m9f-rphj-c435) · manifest · SHA-256 df1f24662e55c01f5e56e884adbbc7db4dab7eb0425997a165eb1d7f334f9e5d_

```
{"id": "GHSA-5m9f-rphj-c435", "aliases": ["CVE-2026-63336"], "modified": "2026-09-10T03:51:13.150501327Z", "summary": "RabbitMQ Java client: TrustEverythingTrustManager used by default in useSslProtocol() enables MITM", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:N/VI:N/VA:N/SC:H/SI:L/SA:N"}], "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (5.33.0).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-17474 — com.rabbitmq:amqp-client 5.22.0 is affected by GHSA-7822-rcf6-97fx (CVE-2026-106122)

- Severity: **Medium** · Classification: Known vulnerable component · Confidence: Medium
- Affected asset: `dependency:Maven/com.rabbitmq:amqp-client@5.22.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 10:11 UTC
- Priority score: 44.2 / 100
- CVSS v3.1: not applicable

OSV.dev reports GHSA-7822-rcf6-97fx (CVE-2026-106122) for Maven package com.rabbitmq:amqp-client at version 5.22.0: RabbitMQ: Malformed UTF-8 in shortstr properties permanently disables RPC consumers. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-7822-rcf6-97fx
```

**Evidence.**

_tool_output · [OSV.dev GHSA-7822-rcf6-97fx](https://osv.dev/vulnerability/GHSA-7822-rcf6-97fx) · manifest · SHA-256 714a9992d656cfa759f2305675cc4bba3e887fbdd1f67a5860b7129f14cd354f_

```
{"id": "GHSA-7822-rcf6-97fx", "aliases": ["CVE-2026-106122"], "modified": "2026-10-07T20:30:07.156315722Z", "summary": "RabbitMQ: Malformed UTF-8 in shortstr properties permanently disables RPC consumers", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N"}], "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (5.36.0).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-17476 — com.rabbitmq:amqp-client 5.22.0 is affected by GHSA-cqgh-8p3p-mx4m (CVE-2026-106121)

- Severity: **Medium** · Classification: Known vulnerable component · Confidence: Medium
- Affected asset: `dependency:Maven/com.rabbitmq:amqp-client@5.22.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 10:11 UTC
- Priority score: 44.2 / 100
- CVSS v3.1: 4.9 (`CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev reports GHSA-cqgh-8p3p-mx4m (CVE-2026-106121) for Maven package com.rabbitmq:amqp-client at version 5.22.0: RabbitMQ: JSONReader in the default JSON-RPC mapper never terminates on truncated input, causing DoS. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-cqgh-8p3p-mx4m
```

**Evidence.**

_tool_output · [OSV.dev GHSA-cqgh-8p3p-mx4m](https://osv.dev/vulnerability/GHSA-cqgh-8p3p-mx4m) · manifest · SHA-256 d186581ae9580ffa443133e6bcdd306bcfa404364f80b5708f9a4e62c44df059_

```
{"id": "GHSA-cqgh-8p3p-mx4m", "aliases": ["CVE-2026-106121"], "modified": "2026-10-07T21:00:04.481305005Z", "summary": "RabbitMQ: JSONReader in the default JSON-RPC mapper never terminates on truncated input, causing DoS", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (5.36.1).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-17477 — com.rabbitmq:amqp-client 5.22.0 is affected by GHSA-h6w7-qmcm-q6xr (CVE-2026-106123)

- Severity: **Medium** · Classification: Known vulnerable component · Confidence: Medium
- Affected asset: `dependency:Maven/com.rabbitmq:amqp-client@5.22.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 10:11 UTC
- Priority score: 44.2 / 100
- CVSS v3.1: 5.5 (`CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:N`)

OSV.dev reports GHSA-h6w7-qmcm-q6xr (CVE-2026-106123) for Maven package com.rabbitmq:amqp-client at version 5.22.0: RabbitMQ Java client: plaintext broker credentials leaked in exception message from ConnectionFactoryConfigurator.load(). The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-h6w7-qmcm-q6xr
```

**Evidence.**

_tool_output · [OSV.dev GHSA-h6w7-qmcm-q6xr](https://osv.dev/vulnerability/GHSA-h6w7-qmcm-q6xr) · manifest · SHA-256 02a97ab4cfa70da61a062fbac3a25fca679e275b046f103736c31be46dea2b4e_

```
{"id": "GHSA-h6w7-qmcm-q6xr", "aliases": ["CVE-2026-106123"], "modified": "2026-10-19T19:45:04.498976139Z", "summary": "RabbitMQ Java client: plaintext broker credentials leaked in exception message from ConnectionFactoryConfigurator.load()", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:N"}, {"type": "CVSS_V4", "score": "CVSS:4.0/AV:L/AC:L/AT:P/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N"}], "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (5.35.0).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-17479 — com.rabbitmq:amqp-client 5.22.0 is affected by GHSA-qx7j-jv8m-fppr (CVE-2026-63335)

- Severity: **Medium** · Classification: Known vulnerable component · Confidence: Medium
- Affected asset: `dependency:Maven/com.rabbitmq:amqp-client@5.22.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 10:11 UTC
- Priority score: 44.2 / 100
- CVSS v3.1: not applicable

OSV.dev reports GHSA-qx7j-jv8m-fppr (CVE-2026-63335) for Maven package com.rabbitmq:amqp-client at version 5.22.0: RabbitMQ Java client malformed body frame triggers raw command assembler exception. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-qx7j-jv8m-fppr
```

**Evidence.**

_tool_output · [OSV.dev GHSA-qx7j-jv8m-fppr](https://osv.dev/vulnerability/GHSA-qx7j-jv8m-fppr) · manifest · SHA-256 8945a9e701ebd554b9a3e63df0c51e16fc0d5916e666afb691fa8326419aea93_

```
{"id": "GHSA-qx7j-jv8m-fppr", "aliases": ["CVE-2026-63335"], "modified": "2026-09-10T03:50:54.002021426Z", "summary": "RabbitMQ Java client malformed body frame triggers raw command assembler exception", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:N/SC:N/SI:N/SA:H"}], "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (5.31.0).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-17480 — com.google.guava:guava 32.0.0-jre is affected by GHSA-xxph-c9ww-hj94 (CVE-2026-102554)

- Severity: **Medium** · Classification: Known vulnerable component · Confidence: Medium
- Affected asset: `dependency:Maven/com.google.guava:guava@32.0.0-jre`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 10:11 UTC
- Priority score: 44.2 / 100
- CVSS v3.1: 5.9 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev reports GHSA-xxph-c9ww-hj94 (CVE-2026-102554) for Maven package com.google.guava:guava at version 32.0.0-jre: Google Guava: CompactHashMap/CompactHashSet/MapMakerInternalMap deserialization triggers uncontrolled memory allocation. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-xxph-c9ww-hj94
```

**Evidence.**

_tool_output · [OSV.dev GHSA-xxph-c9ww-hj94](https://osv.dev/vulnerability/GHSA-xxph-c9ww-hj94) · manifest · SHA-256 644d94f8abc6f1230e34b98eb21f280b407b1fcb664ce8a6706ad92b592855ef_

```
{"id": "GHSA-xxph-c9ww-hj94", "aliases": ["CVE-2026-102554"], "modified": "2026-10-27T14:45:04.803511466Z", "summary": "Google Guava: CompactHashMap/CompactHashSet/MapMakerInternalMap deserialization triggers uncontrolled memory allocation", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:N/A:H"}, {"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N"}], "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (33.7.2).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-17449 — Quantum-vulnerable RSA: key wrapping and data encryption at rest (1 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:RSA:key_wrapping`
- Data source: obp-api/src/main/scala/code/api/util/CertificateUtil.scala
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.3.0 · 2026-11-06 10:11 UTC
- Priority score: 36.9 / 100
- CVSS v3.1: not applicable

1 reference(s) to RSA across 1 file(s), e.g. obp-api/src/main/scala/code/api/util/CertificateUtil.scala:232. Role, judged from paths, function names and nearby code: key wrapping and data encryption at rest. Keys or data encrypted to these public keys are stored: anyone who copies them now decrypts them once a CRQC exists (harvest now, decrypt later).

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open obp-api/src/main/scala/code/api/util/CertificateUtil.scala:232 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [obp-api/src/main/scala/code/api/util/CertificateUtil.scala](https://github.com/OpenBankProject/OBP-API/blob/6a4a13ef079fa33707f4ee3dba1e600570ed34b4/obp-api/src/main/scala/code/api/util/CertificateUtil.scala#L232) · line 232 · SHA-256 7e6a56123c8c6b3d33687149408377283648aff8c9f0ed0b84931b2668e6b4c8_

```
  231 |     // Request JWT encrypted with RSA-OAEP-256 and 128-bit AES/GCM
  232 |     val header = new JWEHeader(JWEAlgorithm.RSA_OAEP_256, EncryptionMethod.A128GCM)
  233 |     // Create an encrypter with the specified public RSA key
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Wrap keys with ML-KEM or a hybrid KEM (X25519 + ML-KEM-768) and re-wrap the stored keys; data that may already have been copied needs its own assessment.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-17448 — Quantum-vulnerable RSA: authentication and identity (certificates, tokens, device attestation) (4 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:RSA:authentication`
- Data source: obp-api/src/main/scala/code/api/util/BerlinGroupSigning.scala
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.3.0 · 2026-11-06 10:11 UTC
- Priority score: 34.2 / 100
- CVSS v3.1: not applicable

7 reference(s) to RSA across 4 file(s), e.g. obp-api/src/main/scala/code/api/util/BerlinGroupSigning.scala:95. Role, judged from paths, function names and nearby code: authentication and identity (certificates, tokens, device attestation). Short-lived authentication stays safe until a CRQC exists; long-lived identities (device attestation, CA and SSH keys) need a plan earlier.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open obp-api/src/main/scala/code/api/util/BerlinGroupSigning.scala:95 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [obp-api/src/main/scala/code/api/util/BerlinGroupSigning.scala](https://github.com/OpenBankProject/OBP-API/blob/6a4a13ef079fa33707f4ee3dba1e600570ed34b4/obp-api/src/main/scala/code/api/util/BerlinGroupSigning.scala#L95) · line 95 · SHA-256 55ef8a46b3449c4c6c5fb66872ff8a4e835d660aa746991ef0510e850c938f60_

```
   94 |     val privateKey: [REDACTED] = loadPrivateKey(privateKeyPem)
   95 |     val signature = Signature.getInstance("SHA256withRSA")
   96 |     signature.initSign(privateKey)
```

_file_excerpt · [obp-api/src/main/scala/code/api/util/BerlinGroupSigning.scala](https://github.com/OpenBankProject/OBP-API/blob/6a4a13ef079fa33707f4ee3dba1e600570ed34b4/obp-api/src/main/scala/code/api/util/BerlinGroupSigning.scala#L110) · line 110 · SHA-256 12c08357b82ad7909d1019946dfb956c9ac90d0a59706824422785385a1dd7d8_

```
  109 |     val keySpec = new PKCS8EncodedKeySpec(decodedKey)
  110 |     KeyFactory.getInstance("RSA").generatePrivate(keySpec)
  111 |   }
```

_file_excerpt · [obp-api/src/main/scala/code/api/util/BerlinGroupSigning.scala](https://github.com/OpenBankProject/OBP-API/blob/6a4a13ef079fa33707f4ee3dba1e600570ed34b4/obp-api/src/main/scala/code/api/util/BerlinGroupSigning.scala#L120) · line 120 · SHA-256 a2ecf53b7d25d57a75a15c02496242cb328381982e8fb8a20e9bf3142413d634_

```
  119 |     logger.debug(s"signatureStr: $signatureStr")
  120 |     val signature = Signature.getInstance("SHA256withRSA")
  121 |     signature.initVerify(publicKey)
```

_file_excerpt · [obp-api/src/main/scala/code/api/util/JwsUtil.scala](https://github.com/OpenBankProject/OBP-API/blob/6a4a13ef079fa33707f4ee3dba1e600570ed34b4/obp-api/src/main/scala/code/api/util/JwsUtil.scala#L255) · line 255 · SHA-256 e46c21f28a6d12825066b7e1daa11b7351ca1af2a570d274458ca0a53c48ac80_

```
  254 |     logger.debug("signRequestResponseCommon says before Create and sign JWS")
  255 |     val jwsProtectedHeader: JWSHeader = new JWSHeader.Builder(JWSAlgorithm.RS256)
  256 |       .base64URLEncodePayload(false)
```

_file_excerpt · [obp-api/src/main/scala/code/api/util/JwtUtil.scala](https://github.com/OpenBankProject/OBP-API/blob/6a4a13ef079fa33707f4ee3dba1e600570ed34b4/obp-api/src/main/scala/code/api/util/JwtUtil.scala#L259) · line 259 · SHA-256 27efd592a76590f2d70e6810733bb4d825358c57d25524bee438506dca7a1d3d_

```
  258 |     // The JWS algorithm of the access tokens
  259 |     val jwsAlg: JWSAlgorithm = getAlgorithm(accessToken).getOrElse(JWSAlgorithm.RS256)
  260 | 
```

_file_excerpt · [obp-api/src/main/scala/code/api/util/JwtUtil.scala](https://github.com/OpenBankProject/OBP-API/blob/6a4a13ef079fa33707f4ee3dba1e600570ed34b4/obp-api/src/main/scala/code/api/util/JwtUtil.scala#L298) · line 298 · SHA-256 3ec5cca9c6e717d318b73ef90a69f3e75ac767aaf981082c443e58bc80ac80bf_

```
  297 |     val clientID: ClientID = new ClientID(aud)
  298 |     val jwsAlg: JWSAlgorithm = getAlgorithm(idToken).getOrElse(JWSAlgorithm.RS256)
  299 |     val jwkSetSource = getOrCreateRemoteJWKSet(remoteJWKSetUrl)
```

_file_excerpt · [obp-api/src/main/scala/code/api/util/SelfSignedCertificateUtil.scala](https://github.com/OpenBankProject/OBP-API/blob/6a4a13ef079fa33707f4ee3dba1e600570ed34b4/obp-api/src/main/scala/code/api/util/SelfSignedCertificateUtil.scala#L68) · line 68 · SHA-256 6d57ed7b3c94dee1b510fcc5fac230e9ff34dace9b5240ece29a3c0fc7a0338f_

```
   67 |     Security.addProvider(new BouncyCastleProvider)
   68 |     val keyPairGenerator = KeyPairGenerator.getInstance("RSA", bcProvider) // Define RSA as the algorithm for a key creation
   69 |     keyPairGenerator.initialize(2048) // Define 2048 as the size of the key
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Keep credentials short-lived and plan ML-DSA certificates, tokens and keys as the ecosystem supports them.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-17451 — Quantum-vulnerable RSA: role not determined (3 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:RSA:general`
- Data source: obp-api/src/main/scala/code/api/util/Glossary.scala
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.3.0 · 2026-11-06 10:11 UTC
- Priority score: 34.2 / 100
- CVSS v3.1: not applicable

3 reference(s) to RSA across 3 file(s), e.g. obp-api/src/main/scala/code/api/util/Glossary.scala:3097. Role, judged from paths, function names and nearby code: role not determined. The code does not show what the keys protect; review decides the priority.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open obp-api/src/main/scala/code/api/util/Glossary.scala:3097 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [obp-api/src/main/scala/code/api/util/Glossary.scala](https://github.com/OpenBankProject/OBP-API/blob/6a4a13ef079fa33707f4ee3dba1e600570ed34b4/obp-api/src/main/scala/code/api/util/Glossary.scala#L3097) · line 3097 · SHA-256 f094b45aa114d51c9d73652bb543b9235c93527aa46387a7ed713d92c6dc7569_

```
 3096 | |{
 3097 | |  "alg": "RS256",
 3098 | |  "typ": "JWT"
```

_file_excerpt · [obp-api/src/main/scala/code/api/util/RSAUtil.scala](https://github.com/OpenBankProject/OBP-API/blob/6a4a13ef079fa33707f4ee3dba1e600570ed34b4/obp-api/src/main/scala/code/api/util/RSAUtil.scala#L70) · line 70 · SHA-256 c8ba344a7fe82866d202b75a7f13828c6d772bb6d53e057c88b81e7dd3494c4e_

```
   69 |     val jwsObject = new JWSObject(
   70 |       new JWSHeader.Builder(JWSAlgorithm.RS256).build, 
   71 |       new Payload(payload)
```

_file_excerpt · [obp-api/src/main/scala/code/messageoutbox/WebhookOutbox.scala](https://github.com/OpenBankProject/OBP-API/blob/6a4a13ef079fa33707f4ee3dba1e600570ed34b4/obp-api/src/main/scala/code/messageoutbox/WebhookOutbox.scala#L111) · line 111 · SHA-256 3737a23ccaa6d6e514bc504d1e58976ceb1c1e97c8235496bc7397c44cea7b0b_

```
  110 |     val keyId = new RSAKey.Builder(publicKey).keyIDFromThumbprint().build().getKeyID
  111 |     val header = new JWSHeader.Builder(JWSAlgorithm.RS256)
  112 |       .keyID(keyId)
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it; introduce an abstraction layer for crypto-agility.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-17471 — com.rabbitmq:amqp-client 5.22.0 is affected by GHSA-5xwg-cfvj-gff5 (CVE-2026-61634)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Medium
- Affected asset: `dependency:Maven/com.rabbitmq:amqp-client@5.22.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 10:11 UTC
- Priority score: 39.2 / 100
- CVSS v3.1: not applicable

OSV.dev reports GHSA-5xwg-cfvj-gff5 (CVE-2026-61634) for Maven package com.rabbitmq:amqp-client at version 5.22.0: RabbitMQ Java client accepts broker frames larger than the negotiated AMQP frame_max. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-5xwg-cfvj-gff5
```

**Evidence.**

_tool_output · [OSV.dev GHSA-5xwg-cfvj-gff5](https://osv.dev/vulnerability/GHSA-5xwg-cfvj-gff5) · manifest · SHA-256 6f72836321403b85c6b4cc38ad9a04928781ce8d53ca5d213f682b9dcc9daeb4_

```
{"id": "GHSA-5xwg-cfvj-gff5", "aliases": ["CVE-2026-61634"], "modified": "2026-09-10T03:51:13.134044568Z", "summary": "RabbitMQ Java client accepts broker frames larger than the negotiated AMQP frame_max", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:N/VA:N/SC:N/SI:N/SA:N"}], "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (5.33.0).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-17439 — Quantum-vulnerable RSA key in certificate (app.example.com)

- Severity: **Low** · Classification: Long-term post-quantum risk · Confidence: High
- Affected asset: `certificate:app.example.com`
- Data source: obp-api/src/main/resources/props/sample.props.template
- Detection method: X.509 public key algorithm identification.
- Analyzer: certificates 1.3.0 · 2026-11-06 10:11 UTC
- Priority score: 36.5 / 100
- CVSS v3.1: not applicable

The certificate app.example.com uses a RSA 2048-bit public key, valid until 2025-11-26. RSA is broken by Shor's algorithm on a CRQC.

**Potential impact.** For authentication, risk materializes only once a CRQC exists while the key/certificate is still trusted. Certificates are short-lived, so the main concern is the PKI and long-lived roots/intermediates.

**Reproduction steps.**

```
openssl x509 -in obp-api/src/main/resources/props/sample.props.template -noout -text | grep -A2 'Public Key Algorithm'
```

**Evidence.**

_certificate · obp-api/src/main/resources/props/sample.props.template · line 2027 · SHA-256 0dda242ea754f0359967578bc4499e17a3c382359f0acb4bb6edcca1c07416ef_

```
Subject: CN=app.example.com
Issuer: CN=app.example.com
Serial: 18c10eb6474
Not before: 2023-11-27T13:15:11+00:00
Not after: 2025-11-26T13:15:11+00:00
Public key: RSA 2048-bit
Signature algorithm: 1.2.840.113549.1.1.11
Signature hash: sha256
CA: False
SAN: -
SHA-256 fingerprint: 25d91ac53796ca8c5598ee6d180ff0efb3919b4592b4ecef1c68fad35b20c726
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability.

**Recommendation.** Track in the PQC inventory; prefer short certificate lifetimes; follow CA/Browser Forum and NIST PQC transition guidance for ML-DSA certificates.

**Retest procedure.** Re-audit once PQC or hybrid certificates are deployed.

### QSI-2026-17444 — Quantum-vulnerable RSA key in certificate (app.example.com)

- Severity: **Low** · Classification: Long-term post-quantum risk · Confidence: High
- Affected asset: `certificate:app.example.com`
- Data source: obp-api/src/main/scala/code/api/ResourceDocs1_4_0/SwaggerDefinitionsJSON.scala
- Detection method: X.509 public key algorithm identification.
- Analyzer: certificates 1.3.0 · 2026-11-06 10:11 UTC
- Priority score: 36.5 / 100
- CVSS v3.1: not applicable

The certificate app.example.com uses a RSA 2048-bit public key, valid until 2025-11-26. RSA is broken by Shor's algorithm on a CRQC.

**Potential impact.** For authentication, risk materializes only once a CRQC exists while the key/certificate is still trusted. Certificates are short-lived, so the main concern is the PKI and long-lived roots/intermediates.

**Reproduction steps.**

```
openssl x509 -in obp-api/src/main/scala/code/api/ResourceDocs1_4_0/SwaggerDefinitionsJSON.scala -noout -text | grep -A2 'Public Key Algorithm'
```

**Evidence.**

_certificate · obp-api/src/main/scala/code/api/ResourceDocs1_4_0/SwaggerDefinitionsJSON.scala · line 3040 · SHA-256 0dda242ea754f0359967578bc4499e17a3c382359f0acb4bb6edcca1c07416ef_

```
Subject: CN=app.example.com
Issuer: CN=app.example.com
Serial: 18c10eb6474
Not before: 2023-11-27T13:15:11+00:00
Not after: 2025-11-26T13:15:11+00:00
Public key: RSA 2048-bit
Signature algorithm: 1.2.840.113549.1.1.11
Signature hash: sha256
CA: False
SAN: -
SHA-256 fingerprint: 25d91ac53796ca8c5598ee6d180ff0efb3919b4592b4ecef1c68fad35b20c726
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability.

**Recommendation.** Track in the PQC inventory; prefer short certificate lifetimes; follow CA/Browser Forum and NIST PQC transition guidance for ML-DSA certificates.

**Retest procedure.** Re-audit once PQC or hybrid certificates are deployed.

### QSI-2026-17440 — Leaf certificate validity of 730 days (app.example.com)

- Severity: **Low** · Classification: Improvement recommendation · Confidence: High
- Affected asset: `certificate:app.example.com`
- Data source: obp-api/src/main/resources/props/sample.props.template
- Detection method: X.509 validity period computation.
- Analyzer: certificates 1.3.0 · 2026-11-06 10:11 UTC
- Priority score: 30.9 / 100
- CVSS v3.1: not applicable

The end-entity certificate is valid for 730 days. Publicly trusted TLS certificates are limited to 398 days today, and CA/Browser Forum rules are reducing this further.

**Potential impact.** Long-lived certificates extend exposure if the key is compromised and slow down algorithm migration.

**Reproduction steps.**

```
openssl x509 -in obp-api/src/main/resources/props/sample.props.template -noout -dates
```

**Evidence.**

_certificate · obp-api/src/main/resources/props/sample.props.template · line 2027 · SHA-256 0dda242ea754f0359967578bc4499e17a3c382359f0acb4bb6edcca1c07416ef_

```
Subject: CN=app.example.com
Issuer: CN=app.example.com
Serial: 18c10eb6474
Not before: 2023-11-27T13:15:11+00:00
Not after: 2025-11-26T13:15:11+00:00
Public key: RSA 2048-bit
Signature algorithm: 1.2.840.113549.1.1.11
Signature hash: sha256
CA: False
SAN: -
SHA-256 fingerprint: 25d91ac53796ca8c5598ee6d180ff0efb3919b4592b4ecef1c68fad35b20c726
```

**Limitations of the check.** Document-based analysis: only the supplied file was examined. Deployed configuration may differ; the result reflects the file content at the recorded SHA-256. Private-PKI certificates may intentionally use other policies.

**Recommendation.** Use shorter validity with automated renewal.

**Retest procedure.** Check notBefore/notAfter of the next issuance.

### QSI-2026-17445 — Leaf certificate validity of 730 days (app.example.com)

- Severity: **Low** · Classification: Improvement recommendation · Confidence: High
- Affected asset: `certificate:app.example.com`
- Data source: obp-api/src/main/scala/code/api/ResourceDocs1_4_0/SwaggerDefinitionsJSON.scala
- Detection method: X.509 validity period computation.
- Analyzer: certificates 1.3.0 · 2026-11-06 10:11 UTC
- Priority score: 30.9 / 100
- CVSS v3.1: not applicable

The end-entity certificate is valid for 730 days. Publicly trusted TLS certificates are limited to 398 days today, and CA/Browser Forum rules are reducing this further.

**Potential impact.** Long-lived certificates extend exposure if the key is compromised and slow down algorithm migration.

**Reproduction steps.**

```
openssl x509 -in obp-api/src/main/scala/code/api/ResourceDocs1_4_0/SwaggerDefinitionsJSON.scala -noout -dates
```

**Evidence.**

_certificate · obp-api/src/main/scala/code/api/ResourceDocs1_4_0/SwaggerDefinitionsJSON.scala · line 3040 · SHA-256 0dda242ea754f0359967578bc4499e17a3c382359f0acb4bb6edcca1c07416ef_

```
Subject: CN=app.example.com
Issuer: CN=app.example.com
Serial: 18c10eb6474
Not before: 2023-11-27T13:15:11+00:00
Not after: 2025-11-26T13:15:11+00:00
Public key: RSA 2048-bit
Signature algorithm: 1.2.840.113549.1.1.11
Signature hash: sha256
CA: False
SAN: -
SHA-256 fingerprint: 25d91ac53796ca8c5598ee6d180ff0efb3919b4592b4ecef1c68fad35b20c726
```

**Limitations of the check.** Document-based analysis: only the supplied file was examined. Deployed configuration may differ; the result reflects the file content at the recorded SHA-256. Private-PKI certificates may intentionally use other policies.

**Recommendation.** Use shorter validity with automated renewal.

**Retest procedure.** Check notBefore/notAfter of the next issuance.

### QSI-2026-17441 — Self-signed end-entity certificate (app.example.com)

- Severity: **Info** · Classification: Improvement recommendation · Confidence: High
- Affected asset: `certificate:app.example.com`
- Data source: obp-api/src/main/resources/props/sample.props.template
- Detection method: X.509 issuer/subject comparison, BasicConstraints.
- Analyzer: certificates 1.3.0 · 2026-11-06 10:11 UTC
- Priority score: 32.0 / 100
- CVSS v3.1: not applicable

Issuer equals subject and the certificate is not marked as a CA.

**Potential impact.** Clients cannot validate it against a trust anchor unless pinned; may encourage disabling verification.

**Reproduction steps.**

```
openssl x509 -in obp-api/src/main/resources/props/sample.props.template -noout -issuer -subject
```

**Evidence.**

_certificate · obp-api/src/main/resources/props/sample.props.template · line 2027 · SHA-256 0dda242ea754f0359967578bc4499e17a3c382359f0acb4bb6edcca1c07416ef_

```
Subject: CN=app.example.com
Issuer: CN=app.example.com
Serial: 18c10eb6474
Not before: 2023-11-27T13:15:11+00:00
Not after: 2025-11-26T13:15:11+00:00
Public key: RSA 2048-bit
Signature algorithm: 1.2.840.113549.1.1.11
Signature hash: sha256
CA: False
SAN: -
SHA-256 fingerprint: 25d91ac53796ca8c5598ee6d180ff0efb3919b4592b4ecef1c68fad35b20c726
```

**Limitations of the check.** Document-based analysis: only the supplied file was examined. Deployed configuration may differ; the result reflects the file content at the recorded SHA-256. Acceptable in closed test environments.

**Recommendation.** Use a certificate from a public or internal CA, or pin explicitly.

**Retest procedure.** Check issuer of the deployed certificate.

### QSI-2026-17446 — Self-signed end-entity certificate (app.example.com)

- Severity: **Info** · Classification: Improvement recommendation · Confidence: High
- Affected asset: `certificate:app.example.com`
- Data source: obp-api/src/main/scala/code/api/ResourceDocs1_4_0/SwaggerDefinitionsJSON.scala
- Detection method: X.509 issuer/subject comparison, BasicConstraints.
- Analyzer: certificates 1.3.0 · 2026-11-06 10:11 UTC
- Priority score: 32.0 / 100
- CVSS v3.1: not applicable

Issuer equals subject and the certificate is not marked as a CA.

**Potential impact.** Clients cannot validate it against a trust anchor unless pinned; may encourage disabling verification.

**Reproduction steps.**

```
openssl x509 -in obp-api/src/main/scala/code/api/ResourceDocs1_4_0/SwaggerDefinitionsJSON.scala -noout -issuer -subject
```

**Evidence.**

_certificate · obp-api/src/main/scala/code/api/ResourceDocs1_4_0/SwaggerDefinitionsJSON.scala · line 3040 · SHA-256 0dda242ea754f0359967578bc4499e17a3c382359f0acb4bb6edcca1c07416ef_

```
Subject: CN=app.example.com
Issuer: CN=app.example.com
Serial: 18c10eb6474
Not before: 2023-11-27T13:15:11+00:00
Not after: 2025-11-26T13:15:11+00:00
Public key: RSA 2048-bit
Signature algorithm: 1.2.840.113549.1.1.11
Signature hash: sha256
CA: False
SAN: -
SHA-256 fingerprint: 25d91ac53796ca8c5598ee6d180ff0efb3919b4592b4ecef1c68fad35b20c726
```

**Limitations of the check.** Document-based analysis: only the supplied file was examined. Deployed configuration may differ; the result reflects the file content at the recorded SHA-256. Acceptable in closed test environments.

**Recommendation.** Use a certificate from a public or internal CA, or pin explicitly.

**Retest procedure.** Check issuer of the deployed certificate.

### QSI-2026-17462 — No post-quantum capable cryptographic library detected

- Severity: **Info** · Classification: Insufficient data · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `dependencies`
- Data source: dependency manifests
- Detection method: Dependency name matching.
- Analyzer: dependencies 1.3.0 · 2026-11-06 10:11 UTC
- Priority score: 13.3 / 100
- CVSS v3.1: not applicable

Across 3 dependency manifests, QSI found crypto libraries (com.nimbusds:nimbus-jose-jwt) but none from its PQC-capable list.

**Potential impact.** Readiness indicator only: PQC support may come from the platform (OpenSSL, OS, cloud KMS) rather than application dependencies.

**Reproduction steps.**

```
Review the dependency manifests listed in the evidence.
```

**Evidence.**

_dependency · obp-api/pom.xml, obp-commons/pom.xml, pom.xml · SHA-256 d7f938c8d0b32a1e5d9fa6803bbcfb0dd448ca7cd9ce0df292ef7c8bc0d4bf02_

```
Crypto libraries: com.nimbusds:nimbus-jose-jwt
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

- Classical only — key wrapping and data encryption at rest: RSA (1 file(s))

**Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

_Levels: 0 none; 1 present, not wired; 2 in use outside the critical paths; 3 hybrid in a critical path; 4 post-quantum by default in the critical paths (root of trust, key wrapping, channel key exchange). Judged from code and manifests._

### What the quantum-vulnerable algorithms do

| Role | Algorithms (files) | ID | First step |
|---|---|---|---|
| **key wrapping and data encryption at rest** | RSA (1) | QSI-2026-17449 | Wrap keys with ML-KEM or a hybrid KEM (X25519 + ML-KEM-768) and re-wrap the stored keys; data that may already have been copied needs its own assessment |
| **authentication and identity (certificates, tokens, device attestation)** | RSA (4) | QSI-2026-17448 | Keep credentials short-lived and plan ML-DSA certificates, tokens and keys as the ecosystem supports them |
| **role not determined** | RSA (3) | QSI-2026-17451 | Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it; introduce an abstraction layer for crypto-agility |

_Roles are judged from file paths, function names and the code around each match; review confirms them. Root-of-trust keys and wrapped keys come first: they are hard to replace or can be recorded today._
No readiness questionnaire was completed for this project.

### Quantum algorithms relevant to this inventory

| Quantum algorithm | Effect | Attack model | Inventoried algorithms (rows) | What it means for this audit |
|---|---|---|---|---|
| Shor's algorithm — factoring | breaks | Q1 | RSA (10) | Breaks RSA at every key length: a longer modulus only raises the cost polynomially. Plan migration to ML-KEM (or a hybrid) for key establishment and ML-DSA / SLH-DSA for signatures; start with keys protecting data that must stay confidential for years (harvest now, decrypt later) and with long-lived signatures. |
| Grover's algorithm — key search and preimages | weakens (larger keys restore the margin) | Q1 | HMAC (4), SHA-2 (13), bcrypt (3) | Not a break. 256-bit keys (AES-256, ChaCha20) keep a comfortable margin; AES-128 meets NIST category 1, while some authorities ask for 256-bit keys in quantum-resistant contexts (see the AES-128 entry). Prefer 256-bit keys for long-lived data; 256-bit hashes need no change for preimage resistance. |
| Brassard–Høyer–Tapp — collision search | weakens (larger keys restore the margin) | Q1 | SHA-2 (13) | 256-bit hashes (SHA-256, SHA3-256) remain adequate for collision resistance; 160-bit hashes are already weak classically (SHA-1 collisions are practical). Use 384/512-bit hashes where NIST categories 4–5 are required. |

_Effects: breaks — replace the algorithm; weakens — larger keys or outputs restore the margin; included in standard parameters — no action at standard parameter sets; only with superposition queries — not applicable to ordinary deployments._


## 9. Limitations and assumptions

- This report presents automated and documented analysis results for the stated scope. It is not a legal opinion, a certification or an attestation of compliance with any standard.
- z is a planning assumption chosen per risk profile, not a prediction. A cryptographically relevant quantum computer is not publicly known to exist today.
- certificates: docs/MTLS.md line 403: certificate could not be parsed (ValueError)
- tls_key_exchange_groups: obp-api/src/main/resources/docs/introductory_system_documentation.md: no key-exchange group directive; TLS library defaults apply and were not determined
- certificates: obp-api/src/main/scala/code/api/ResourceDocs1_4_0/SwaggerDefinitionsJSON.scala line 2968: certificate could not be parsed (ValueError)
- certificates: obp-api/src/main/scala/code/api/ResourceDocs1_4_0/SwaggerDefinitionsJSON.scala line 3067: certificate could not be parsed (ValueError)
- certificates: obp-api/src/main/scala/code/api/constant/constant.scala line 1035: certificate could not be parsed (ValueError)
- certificates: obp-api/src/main/scala/code/api/util/BerlinGroupSigning.scala line 129: certificate could not be parsed (ValueError)
- certificates: obp-api/src/main/scala/code/api/util/BerlinGroupSigning.scala line 283: certificate could not be parsed (ValueError)
- certificates: obp-api/src/main/scala/code/api/util/CertificateVerifier.scala line 138: certificate could not be parsed (ValueError)
- certificates: obp-api/src/main/scala/code/api/util/CertificateVerifier.scala line 146: certificate could not be parsed (ValueError)
- certificates: obp-api/src/main/scala/code/api/v2_2_0/Http4s220.scala line 884: certificate could not be parsed (ValueError)
- certificates: obp-api/src/main/scala/code/api/v2_2_0/Http4s220.scala line 897: certificate could not be parsed (ValueError)
- certificates: obp-api/src/main/scala/code/api/v4_0_0/Http4s400.scala line 11069: certificate could not be parsed (ValueError)
- tls_key_exchange_groups: obp-api/src/main/scala/code/api/v6_0_0/Http4s600.scala line 14214: not in the algorithm registry, not assessed: List(
- tls_key_exchange_groups: obp-api/src/main/scala/code/api/v7_0_0/Http4s700Groups.scala line 304: not in the algorithm registry, not assessed: found.collect
- tls_key_exchange_groups: obp-api/src/main/scala/code/api/v7_0_0/Http4s700Groups.scala line 362: not in the algorithm registry, not assessed: List(
- certificates: scripts/resource_doc_baseline/lift_resource_docs_v2_2_0.json line 214: certificate could not be parsed (ValueError)
- certificates: scripts/resource_doc_baseline/lift_resource_docs_v2_2_0.json line 215: certificate could not be parsed (ValueError)
- certificates: scripts/resource_doc_baseline/lift_resource_docs_v4_0_0.json line 1107: certificate could not be parsed (ValueError)

## 10. Remediation plan / Priorities for 30, 60 and 90 days

### 30 days

| Priority | ID | Action | Type | Closure criteria |
|---|---|---|---|---|
| P1 | QSI-2026-17438 | Renew the certificate for app.example.com and enable automated renewal with alerting ≥ 30 days before expiry. | root-cause fix | The deployed certificate is valid and renewal is automated. |
| P1 | QSI-2026-17443 | Renew the certificate for app.example.com and enable automated renewal with alerting ≥ 30 days before expiry. | root-cause fix | The deployed certificate is valid and renewal is automated. |
| P1 | QSI-2026-17437 | Rotate and remove secrets found in obp-api/src/main/resources/docs/introductory_system_documentation.md. | root-cause fix | Secret scanner reports no secrets; old values revoked. |
| P1 | QSI-2026-17442 | Rotate and remove secrets found in obp-api/src/main/resources/props/sample.props.template. | root-cause fix | Secret scanner reports no secrets; old values revoked. |
| P1 | QSI-2026-17447 | Rotate and remove secrets found in obp-api/src/main/scala/code/api/util/APIUtil.scala. | root-cause fix | Secret scanner reports no secrets; old values revoked. |
| P1 | QSI-2026-17450 | Rotate and remove secrets found in obp-api/src/main/scala/code/api/util/DBUtil.scala. | root-cause fix | Secret scanner reports no secrets; old values revoked. |
| P1 | QSI-2026-17452 | Rotate and remove secrets found in obp-api/src/main/scala/code/api/util/Glossary.scala. | root-cause fix | Secret scanner reports no secrets; old values revoked. |
| P1 | QSI-2026-17453 | Rotate and remove secrets found in obp-api/src/main/scala/code/api/util/JwtUtil.scala. | root-cause fix | Secret scanner reports no secrets; old values revoked. |
| P1 | QSI-2026-17455 | Rotate and remove secrets found in obp-api/src/main/scala/code/api/v3_1_0/Http4s310.scala. | root-cause fix | Secret scanner reports no secrets; old values revoked. |
| P1 | QSI-2026-17456 | Rotate and remove secrets found in obp-api/src/main/scala/code/api/v4_0_0/Http4s400.scala. | root-cause fix | Secret scanner reports no secrets; old values revoked. |
| P1 | QSI-2026-17457 | Rotate and remove secrets found in obp-api/src/main/scala/code/api/v5_1_0/Http4s510.scala. | root-cause fix | Secret scanner reports no secrets; old values revoked. |
| P1 | QSI-2026-17458 | Rotate and remove secrets found in obp-api/src/main/scala/code/api/v6_0_0/Http4s600.scala. | root-cause fix | Secret scanner reports no secrets; old values revoked. |
| P1 | QSI-2026-17459 | Rotate and remove secrets found in obp-api/src/main/scala/code/paymetngateway/StripeExample.scala. | root-cause fix | Secret scanner reports no secrets; old values revoked. |
| P1 | QSI-2026-17460 | Rotate and remove secrets found in obp-api/src/main/scala/code/sandbox/OBPDataImport.scala. | root-cause fix | Secret scanner reports no secrets; old values revoked. |
| P1 | QSI-2026-17461 | Rotate and remove secrets found in scripts/resource_doc_baseline/lift_resource_docs_v4_0_0.json. | root-cause fix | Secret scanner reports no secrets; old values revoked. |
| P1 | QSI-2026-17454 | Use an AEAD mode (GCM) with unique nonces. | root-cause fix | Re-scan the source and review the call sites listed in the evidence. |
| P2 | QSI-2026-17463 | Upgrade org.postgresql:postgresql to a fixed version (42.7.12). | root-cause fix | Dependency scan no longer reports GHSA-j92g-9f8w-j867 (CVE-2026-54291). |
| P2 | QSI-2026-17464 | Upgrade org.xerial.snappy:snappy-java to a fixed version (1.1.10.9). | root-cause fix | Dependency scan no longer reports GHSA-gwq9-9ffj-mvrv (CVE-2026-93451). |
| P2 | QSI-2026-17465 | Upgrade org.xerial.snappy:snappy-java to a fixed version (1.1.10.9). | root-cause fix | Dependency scan no longer reports GHSA-q233-g92q-qxp6 (CVE-2026-108106). |
| P2 | QSI-2026-17468 | Upgrade org.jsoup:jsoup to a fixed version (1.23.2). | root-cause fix | Dependency scan no longer reports GHSA-65r4-943x-97jj (CVE-2026-75140). |
| P2 | QSI-2026-17472 | Upgrade com.rabbitmq:amqp-client to a fixed version (5.33.1). | root-cause fix | Dependency scan no longer reports GHSA-68mj-5wr7-6fgg (CVE-2026-69219). |
| P2 | QSI-2026-17473 | Upgrade com.rabbitmq:amqp-client to a fixed version (5.33.0). | root-cause fix | Dependency scan no longer reports GHSA-6g32-pxv4-2wfj (CVE-2026-63337). |
| P2 | QSI-2026-17475 | Upgrade com.rabbitmq:amqp-client to a fixed version (5.33.1). | root-cause fix | Dependency scan no longer reports GHSA-93j5-89vc-pph4 (CVE-2026-69220). |
| P2 | QSI-2026-17478 | Upgrade com.rabbitmq:amqp-client to a fixed version (5.34.0). | root-cause fix | Dependency scan no longer reports GHSA-jh4v-gfqj-7rhx (CVE-2026-75516). |
| P2 | QSI-2026-17466 | Upgrade org.xerial.snappy:snappy-java to a fixed version (1.1.10.9). | root-cause fix | Dependency scan no longer reports GHSA-xqrx-qh46-34m7 (CVE-2026-116590). |
| P2 | QSI-2026-17467 | Upgrade org.apache.logging.log4j:log4j-api to a fixed version (2.25.5, 2.26.1). | root-cause fix | Dependency scan no longer reports GHSA-qv9r-c865-cp47 (CVE-2026-49844). |
| P2 | QSI-2026-17469 | Upgrade org.jsoup:jsoup to a fixed version (1.23.1). | root-cause fix | Dependency scan no longer reports GHSA-pmhh-3w7g-xqp8 (CVE-2026-71497). |
| P2 | QSI-2026-17470 | Upgrade com.rabbitmq:amqp-client to a fixed version (5.33.0). | root-cause fix | Dependency scan no longer reports GHSA-5m9f-rphj-c435 (CVE-2026-63336). |
| P2 | QSI-2026-17474 | Upgrade com.rabbitmq:amqp-client to a fixed version (5.36.0). | root-cause fix | Dependency scan no longer reports GHSA-7822-rcf6-97fx (CVE-2026-106122). |
| P2 | QSI-2026-17476 | Upgrade com.rabbitmq:amqp-client to a fixed version (5.36.1). | root-cause fix | Dependency scan no longer reports GHSA-cqgh-8p3p-mx4m (CVE-2026-106121). |
| P2 | QSI-2026-17477 | Upgrade com.rabbitmq:amqp-client to a fixed version (5.35.0). | root-cause fix | Dependency scan no longer reports GHSA-h6w7-qmcm-q6xr (CVE-2026-106123). |
| P2 | QSI-2026-17479 | Upgrade com.rabbitmq:amqp-client to a fixed version (5.31.0). | root-cause fix | Dependency scan no longer reports GHSA-qx7j-jv8m-fppr (CVE-2026-63335). |
| P2 | QSI-2026-17480 | Upgrade com.google.guava:guava to a fixed version (33.7.2). | root-cause fix | Dependency scan no longer reports GHSA-xxph-c9ww-hj94 (CVE-2026-102554). |
| P2 | QSI-2026-17471 | Upgrade com.rabbitmq:amqp-client to a fixed version (5.33.0). | root-cause fix | Dependency scan no longer reports GHSA-5xwg-cfvj-gff5 (CVE-2026-61634). |
### 60 days

| Priority | ID | Action | Type | Closure criteria |
|---|---|---|---|---|
### 90 days

| Priority | ID | Action | Type | Closure criteria |
|---|---|---|---|---|
| P3 | QSI-2026-17449 | Add RSA usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-17448 | Add RSA usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-17451 | Add RSA usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-17439 | Add RSA usages at certificate:app.example.com to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-17444 | Add RSA usages at certificate:app.example.com to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-17440 | Use shorter validity with automated renewal. | root-cause fix | Check notBefore/notAfter of the next issuance. |
| P3 | QSI-2026-17445 | Use shorter validity with automated renewal. | root-cause fix | Check notBefore/notAfter of the next issuance. |
| P4 | QSI-2026-17449 | Plan migration of RSA to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-17448 | Plan migration of RSA to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-17451 | Plan migration of RSA to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-17439 | Plan migration of RSA to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. or a hybrid scheme in use. |
| P4 | QSI-2026-17444 | Plan migration of RSA to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. or a hybrid scheme in use. |
| P4 | QSI-2026-17441 | Use a certificate from a public or internal CA, or pin explicitly. | root-cause fix | Check issuer of the deployed certificate. |
| P4 | QSI-2026-17446 | Use a certificate from a public or internal CA, or pin explicitly. | root-cause fix | Check issuer of the deployed certificate. |

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
15. NIST IR 8547 — Transition to Post-Quantum Cryptography Standards — NIST. <https://csrc.nist.gov/pubs/ir/8547/final> (final (2026-10-27; the initial public draft of November 2024 is obsoleted). Tables 2 and 4: ECDSA, EdDSA and RSA signatures, finite-field and elliptic-curve DH and MQV, and RSA key establishment are deprecated after 2030 and disallowed after 2035 at every key size — the draft deprecated only the 112-bit level. A composite (hybrid) key establishment stays FIPS 140-validatable while one input comes from an approved scheme. Repeats the federal deadlines of OMB M-26-15: post-quantum key establishment by 2030-12-31 and signatures by 2031-12-31 for high value assets and high impact systems)
16. NIST SP 800-131A Rev. 2 — Transitioning the Use of Cryptographic Algorithms and Key Lengths — NIST. <https://csrc.nist.gov/pubs/sp/800/131/a/r2/final> (final (2019))
17. NIST SP 800-57 Part 1 Rev. 5 — Recommendation for Key Management — NIST. <https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final> (final (2020))
18. NIST — Post-Quantum Cryptography Standardization: Evaluation Criteria, Security (Call for Proposals, Section 4.A.5) — NIST. <https://csrc.nist.gov/Projects/Post-Quantum-Cryptography/Post-Quantum-Cryptography-Standardization/Evaluation-Criteria/Security-(Evaluation-Criteria)> (security categories: AES-128 key search 2^170/MAXDEPTH quantum gates, AES-192 2^233/MAXDEPTH, AES-256 2^298/MAXDEPTH; MAXDEPTH 2^40–2^96)
19. OSV advisory GHSA-5m9f-rphj-c435 — OSV.dev. <https://osv.dev/vulnerability/GHSA-5m9f-rphj-c435> (modified 2026-09-10T03:51:13.150501327Z)
20. OSV advisory GHSA-5xwg-cfvj-gff5 — OSV.dev. <https://osv.dev/vulnerability/GHSA-5xwg-cfvj-gff5> (modified 2026-09-10T03:51:13.134044568Z)
21. OSV advisory GHSA-65r4-943x-97jj — OSV.dev. <https://osv.dev/vulnerability/GHSA-65r4-943x-97jj> (modified 2026-10-05T22:45:05.710363586Z)
22. OSV advisory GHSA-68mj-5wr7-6fgg — OSV.dev. <https://osv.dev/vulnerability/GHSA-68mj-5wr7-6fgg> (modified 2026-09-10T03:51:13.151154373Z)
23. OSV advisory GHSA-6g32-pxv4-2wfj — OSV.dev. <https://osv.dev/vulnerability/GHSA-6g32-pxv4-2wfj> (modified 2026-09-10T03:51:13.214436792Z)
24. OSV advisory GHSA-7822-rcf6-97fx — OSV.dev. <https://osv.dev/vulnerability/GHSA-7822-rcf6-97fx> (modified 2026-10-07T20:30:07.156315722Z)
25. OSV advisory GHSA-93j5-89vc-pph4 — OSV.dev. <https://osv.dev/vulnerability/GHSA-93j5-89vc-pph4> (modified 2026-09-10T03:51:13.771990072Z)
26. OSV advisory GHSA-cqgh-8p3p-mx4m — OSV.dev. <https://osv.dev/vulnerability/GHSA-cqgh-8p3p-mx4m> (modified 2026-10-07T21:00:04.481305005Z)
27. OSV advisory GHSA-gwq9-9ffj-mvrv — OSV.dev. <https://osv.dev/vulnerability/GHSA-gwq9-9ffj-mvrv> (modified 2026-10-27T15:47:24.498155855Z)
28. OSV advisory GHSA-h6w7-qmcm-q6xr — OSV.dev. <https://osv.dev/vulnerability/GHSA-h6w7-qmcm-q6xr> (modified 2026-10-19T19:45:04.498976139Z)
29. OSV advisory GHSA-j92g-9f8w-j867 — OSV.dev. <https://osv.dev/vulnerability/GHSA-j92g-9f8w-j867> (modified 2026-09-10T03:50:12.377062079Z)
30. OSV advisory GHSA-jh4v-gfqj-7rhx — OSV.dev. <https://osv.dev/vulnerability/GHSA-jh4v-gfqj-7rhx> (modified 2026-09-17T15:00:06.805894716Z)
31. OSV advisory GHSA-pmhh-3w7g-xqp8 — OSV.dev. <https://osv.dev/vulnerability/GHSA-pmhh-3w7g-xqp8> (modified 2026-09-10T03:50:53.809983880Z)
32. OSV advisory GHSA-q233-g92q-qxp6 — OSV.dev. <https://osv.dev/vulnerability/GHSA-q233-g92q-qxp6> (modified 2026-10-27T15:47:24.815707184Z)
33. OSV advisory GHSA-qv9r-c865-cp47 — OSV.dev. <https://osv.dev/vulnerability/GHSA-qv9r-c865-cp47> (modified 2026-09-10T03:50:52.972700022Z)
34. OSV advisory GHSA-qx7j-jv8m-fppr — OSV.dev. <https://osv.dev/vulnerability/GHSA-qx7j-jv8m-fppr> (modified 2026-09-10T03:50:54.002021426Z)
35. OSV advisory GHSA-xqrx-qh46-34m7 — OSV.dev. <https://osv.dev/vulnerability/GHSA-xqrx-qh46-34m7> (modified 2026-10-27T15:47:25.122359555Z)
36. OSV advisory GHSA-xxph-c9ww-hj94 — OSV.dev. <https://osv.dev/vulnerability/GHSA-xxph-c9ww-hj94> (modified 2026-10-27T14:45:04.803511466Z)
37. OWASP Application Security Verification Standard — OWASP. <https://owasp.org/www-project-application-security-verification-standard/> (living standard — check the project page for the current version)
38. P. W. Shor — Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms on a Quantum Computer (SIAM J. Comput., 1997) — SIAM. <https://doi.org/10.1137/S0097539795293172> (peer-reviewed article)
39. RFC 5280 — Internet X.509 Public Key Infrastructure Certificate and Certificate Revocation List (CRL) Profile — IETF. <https://www.rfc-editor.org/rfc/rfc5280> (proposed standard: path validation requires a trust anchor, so a self-signed certificate is trusted only where it has been installed as one — a deployment fact, not a defect in itself)
40. S. Jaques, M. Naehrig, M. Roetteler, F. Virdia — Implementing Grover oracles for quantum key search on AES and LowMC (EUROCRYPT 2020; arXiv:1910.01700) — Springer / arXiv. <https://arxiv.org/abs/1910.01700> (peer-reviewed article: lower cost estimates for the AES key searches that define the NIST categories)

## Appendices: Cryptographic inventory

By origin: dependency manifests 1 (0 Shor-breakable) · own code 32 (10 Shor-breakable).

| Algorithm | Parameter | Library | Quantum status | Classical status | Count | Locations | Examples |
|---|---|---|---|---|---|---|---|
| HMAC |  |  | reduced margin (Grover), approved | acceptable | 2 | 2 | obp-api/src/main/scala/code/api/GatewayLogin.scala:132; obp-api/src/main/scala/code/api/dauth.scala:120 |
| HMAC | HS256 |  | reduced margin (Grover), approved | acceptable | 2 | 2 | obp-api/src/main/scala/code/api/util/CertificateUtil.scala:179; obp-api/src/main/scala/code/api/util/Glossary.scala:2970 |
| bcrypt |  |  | reduced margin (Grover), approved | acceptable | 3 | 3 | obp-api/src/main/scala/code/bankconnectors/LocalMappedConnector.scala:414; obp-api/src/main/scala/code/consent/MappedConsent.scala:229; obp-api/src/main/scala/code/transactionChallenge/MappedChallengeProvider.scala:128 |
| SHA-2 | SHA-256 |  | Grover: acceptable to NIST, below ECCG/ANSSI guidance | acceptable | 13 | 13 | obp-api/src/main/resources/props/sample.props.template (line 2027); obp-api/src/main/scala/bootstrap/http4s/Http4sMtls.scala:118; obp-api/src/main/scala/code/api/ResourceDocs1_4_0/SwaggerDefinitionsJSON.scala (line 3040) |
| Crypto library | 10.5 | com.nimbusds:nimbus-jose-jwt (Nimbus JOSE+JWT) | n/a | acceptable | 1 | 1 | obp-api/pom.xml |
| TLS 1.2 |  |  | n/a | acceptable | 1 | 1 | obp-api/src/main/resources/docs/introductory_system_documentation.md (line 1768) |
| TLS 1.3 |  |  | n/a | acceptable | 1 | 1 | obp-api/src/main/resources/docs/introductory_system_documentation.md (line 1768) |
| RSA | 2048-bit |  | vulnerable (Shor) | acceptable | 2 | 2 | obp-api/src/main/resources/props/sample.props.template (line 2027) — app.example.com; obp-api/src/main/scala/code/api/ResourceDocs1_4_0/SwaggerDefinitionsJSON.scala (line 3040) — app.example.com |
| RSA |  |  | vulnerable (Shor) | acceptable | 2 | 2 | obp-api/src/main/scala/code/api/util/BerlinGroupSigning.scala:95; obp-api/src/main/scala/code/api/util/SelfSignedCertificateUtil.scala:68 |
| RSA | RSA-OAEP-256 |  | vulnerable (Shor) | acceptable | 1 | 1 | obp-api/src/main/scala/code/api/util/CertificateUtil.scala:232 |
| RSA | RS256 |  | vulnerable (Shor) | acceptable | 5 | 5 | obp-api/src/main/scala/code/api/util/Glossary.scala:3097; obp-api/src/main/scala/code/api/util/JwsUtil.scala:255; obp-api/src/main/scala/code/api/util/JwtUtil.scala:259 |

_Long lists are grouped here; the full per-file list is in the JSON report, signed with the same key._

## Appendices: Input files

| File | Size | SHA-256 | Redactions |
|---|---|---|---|
| .github/scripts/check_test_isolation.py | 7674 | `fe057b9c78be2cad2fe75eb56678a7c94d689ce67490ca3c32feebd234541809` | 0 |
| dev/mtls-nginx/nginx.conf | 2448 | `ae0b83095b15e123c08b4e7902c13dd33fcf347a1d608d951ed90a697f1600ed` | 0 |
| docs/MTLS.md | 27564 | `3753e5d90b725aaa4f9c82e44999b1d5420d82392d0e842c0fccd48b49c47e67` | 0 |
| obp-api/pom.xml | 35211 | `4663b32c309af2e981740bdcc07208ecece96e1ba86c2e4b7de720dec59b1422` | 0 |
| obp-api/src/main/protobuf/api.proto | 6669 | `01d3acecacd05293448793ec3260c57b0e1e88ce49d5d7d8104be959d2fb5c3c` | 0 |
| obp-api/src/main/protobuf/chat.proto | 1672 | `411436a082033ae3e35feb9358e319e80324ccbb208e77da68c7be3d9984de2a` | 0 |
| obp-api/src/main/protobuf/connector.proto | 405 | `ef426dd0c3021097db78df47c3538ba9d737b5bfd2ce90fa41f03b46aa29f154` | 0 |
| obp-api/src/main/protobuf/google/protobuf/empty.proto | 2421 | `a3d2c9810309d8b9f9dc59446b873a883dd5e400ed2b9cf88a7c3de96316df2d` | 0 |
| obp-api/src/main/protobuf/google/protobuf/timestamp.proto | 6217 | `9676e79a10857737ca23353b7877ea363856edbe94bf41caf7165e2473e1cbc3` | 0 |
| obp-api/src/main/protobuf/log_cache.proto | 1288 | `6dac771f191c60ea5b63195c543272b576f22fec7a86f9f1d807a32adbd56522` | 0 |
| obp-api/src/main/protobuf/metrics_stream.proto | 3907 | `f3ee2eafd78defad33a001f70502f2a04adb8c1860867ea47409e861ec7c5139` | 0 |
| obp-api/src/main/protobuf/signal.proto | 3035 | `2b6d0ae876baa5dc072768f05f7ff8c4214b17f67172f1f088e13a8f72e4624b` | 0 |
| obp-api/src/main/resources/docs/introductory_system_documentation.md | 193763 | `706e9805de38ccda0bda34ab6cff7aa2bdc0e9975d0cf25418c52d088bb4f10e` | 26 |
| obp-api/src/main/resources/props/sample.props.template | 120119 | `52cb94e0a128cd3bf8f2a545ab506cbc158ea50fb384d2ca4ed864c4f6d079cb` | 11 |
| obp-api/src/main/scala/bootstrap/http4s/Http4sMtls.scala | 12055 | `39ab3ac211bc76b762759e870d0b21b1c8f59f7007b6b6c0c50bbcfedb0fb19f` | 0 |
| obp-api/src/main/scala/bootstrap/http4s/Http4sServer.scala | 3338 | `5f52500a49fec860267c9381ccddc6db34d1e5b03e2d6649b6e96268da4fea0d` | 0 |
| obp-api/src/main/scala/bootstrap/liftweb/Boot.scala | 54798 | `273e7dc071a270f73551f2bef9cbb23289a685b5e9b244d7e67aed1e8ac8f7ae` | 0 |
| obp-api/src/main/scala/bootstrap/liftweb/CustomDBVendor.scala | 4967 | `b8de314dc648a0fa87dbec5e09828bc2810190f9a4f2bbe71c58dae3f59f7f2d` | 0 |
| obp-api/src/main/scala/code/abacrule/AbacRuleEngine.scala | 26454 | `322e3d1a5923206798f84c10b3d98d89490c92ebe0e3ae5f72081d577dbe294b` | 0 |
| obp-api/src/main/scala/code/abacrule/AbacRuleExamples.scala | 12362 | `e8c2dd1b75741be937246b4daddf2f64e56c364250b26858d25ea0c91eb656e8` | 0 |
| obp-api/src/main/scala/code/abacrule/AbacRuleTrait.scala | 5819 | `0b4f95f7380f94e6daf161856b5bb8ec0eb3e19ca0bf5a93893eaffe4f87c1c4` | 0 |
| obp-api/src/main/scala/code/accountaccessrequest/AccountAccessRequest.scala | 6366 | `0bbada3e06144fc3aab2e5d69832bc9e5e922169c1362538332315d6ca4b0ae3` | 0 |
| obp-api/src/main/scala/code/accountaccessrequest/AccountAccessRequestTrait.scala | 2565 | `51e8612bb31c6f9b64e2b6fb125746471f7115ad928dfb42a7c6d7b8843be9a5` | 0 |
| obp-api/src/main/scala/code/accountapplication/AccountApplication.scala | 1709 | `1f9e28766a414378a53b2c37cb6aaa285fbb1741462075c99ae74e7bfee57efa` | 0 |
| obp-api/src/main/scala/code/accountapplication/MappedAccountApplication.scala | 5129 | `2eb4136637725b15c3013c7cfb75e694219f5c261928666960252aec1cde7296` | 0 |
| obp-api/src/main/scala/code/accountattribute/AccountAttribute.scala | 3700 | `305e0701e09135e070be4fc3023a1ac827e1e815432c18a02f299ad7d2ca5395` | 0 |
| obp-api/src/main/scala/code/accountattribute/MappedAccountAttributeProvider.scala | 10460 | `4548b58979bf1802021f7ac425cc841ff03570ef7d5dcd920e9e520de7098166` | 0 |
| obp-api/src/main/scala/code/accountholders/AccountHolders.scala | 2438 | `36018d531333ce19beac83dc5e9eb874f41dca9f02549f9d383f7106d5d7b65f` | 0 |
| obp-api/src/main/scala/code/accountholders/MapperAccountHolders.scala | 7298 | `bfa9c5585fd9ce6f76caecb171a7e9eddb2f6b6b99d369d3609379c6e71863bb` | 0 |
| obp-api/src/main/scala/code/actorsystem/ObpActorConfig.scala | 3943 | `0d7e6053d67291e749e5e47ae664d2ab3f7a9bdea39bfa340944986c4a5c9406` | 0 |
| obp-api/src/main/scala/code/actorsystem/ObpActorHelper.scala | 1190 | `aa9ecc8a32701953444747d1365e8d4fdc29dd68781455adbbe6ebc0f4b96595` | 0 |
| obp-api/src/main/scala/code/actorsystem/ObpActorSystem.scala | 2567 | `04800e3e1f2c804d6fee696d98454e9e51e16177094bc90248bf2e9432a78bd0` | 0 |
| obp-api/src/main/scala/code/actorsystem/ObpLookupSystem.scala | 4054 | `058dc45bc408f27d51925e910294711cc25df2249a8c8f57e522a16ad0734995` | 0 |
| obp-api/src/main/scala/code/amqpbroker/AmqpBankBroker.scala | 4363 | `040acff973769c780aed43d45325498f7c97383b8932ad3102b57c4dc2a9f6a3` | 0 |
| obp-api/src/main/scala/code/api/AliveCheckRoutes.scala | 1625 | `67a48680966edeeec7c641cb28df90fd1d4d8e77e30ce1cd24d0df19020b1d37` | 0 |
| obp-api/src/main/scala/code/api/DirectLoginRoutes.scala | 5032 | `1c5498222f03f16c63536d5aa2d8ae8dc2df6cab8788cbf1702d8969c08dd605` | 0 |
| obp-api/src/main/scala/code/api/GatewayLogin.scala | 21679 | `facbcecdd72fc00916ae23c5bec92f3741af0ed50f1bedfbbd5a8c90fee436fb` | 0 |
| obp-api/src/main/scala/code/api/OAuth2.scala | 42955 | `879ea9cb7569034552bc75018139ee66a5bb6d080d05e0b6270f4dcd8a6d7045` | 3 |
| obp-api/src/main/scala/code/api/OBPRestHelper.scala | 9831 | `596e586061955a33758df4d04b03a59eef47979560709b75e9d598a9f9bac2dd` | 0 |
| obp-api/src/main/scala/code/api/ResourceDocs1_4_0/MessageDocsSwaggerDefinitions.scala | 11245 | `9b69431599e26e91bf8e6d58eca2e9ef702620c73f38e4c16f5cc35ec5a241e3` | 0 |
| obp-api/src/main/scala/code/api/ResourceDocs1_4_0/OpenAPI31JSONFactory.scala | 31333 | `91a0d25ec706ea18dba68bbafd2ea15a9308316e7764d5877dc122fd9e022dd0` | 1 |
| obp-api/src/main/scala/code/api/ResourceDocs1_4_0/ResourceDocs140.scala | 2624 | `aa55fe4aeb53e39ac86c83f1457a1799c453e26cb788c2c818c95a3decc134f5` | 0 |
| obp-api/src/main/scala/code/api/ResourceDocs1_4_0/ResourceDocsAPIMethods.scala | 76094 | `faf1710e2f266a02eb0bd32785e350668e785e217f0aba9f60664a4141fc8389` | 0 |
| obp-api/src/main/scala/code/api/ResourceDocs1_4_0/SwaggerDefinitionsJSON.scala | 245067 | `ef7ccd115d94166f2d2020c627699d0ab26cab361f0c4cd543964fed6b0410e5` | 0 |
| obp-api/src/main/scala/code/api/ResourceDocs1_4_0/SwaggerJSONFactory.scala | 58215 | `29e022acccf67cfa2ebf94581f7b152ef0eeec4f576b37aff64f7d36f494aa39` | 0 |
| obp-api/src/main/scala/code/api/SIWERoutes.scala | 6824 | `c5a8d68913ee693f0312ce68e1eff6aacc9c6a33d5bb79ec07a2d6aaa89ec3fb` | 0 |
| obp-api/src/main/scala/code/api/UKOpenBanking/UKAmounts.scala | 6652 | `0176e4e2834b7edae17fb968404d7590efcf6e7272cb87883898599e7f7d20f6` | 0 |
| obp-api/src/main/scala/code/api/UKOpenBanking/UKTransactionsQuery.scala | 7480 | `dcdd7357cff50832b9fabbceb1aa3c5e716c015331417f901b44110a741190ee` | 0 |
| obp-api/src/main/scala/code/api/UKOpenBanking/v2_0_0/Http4sUKOBv200.scala | 2464 | `18e7bb14fca96f99e399b64cdcd5bab6a6ca241219dff9d20377d4096a7da204` | 0 |
| obp-api/src/main/scala/code/api/UKOpenBanking/v2_0_0/Http4sUKOBv200AIS.scala | 9728 | `d5932105c57ea673f798c8ce690a7f47f6205e5a5f9bd26c6a30352e7d8c3e28` | 0 |
| obp-api/src/main/scala/code/api/UKOpenBanking/v2_0_0/JSONFactory_UKOpenBanking_200.scala | 9410 | `d7851ba35fd28170a446f03c9a75c1be620568ac6887bd11c3be1c273511dbed` | 0 |
| obp-api/src/main/scala/code/api/UKOpenBanking/v2_0_0/OBP_UKOpenBanking_200.scala | 1876 | `18c79a551e54876785a8bdb7e196383718ca7e417f011c276def45898ab29de7` | 0 |
| obp-api/src/main/scala/code/api/UKOpenBanking/v3_1_0/Http4sUKOBv310.scala | 4566 | `5a714638cb4f0b6082be583f99dc5a099c494dabd43a214e2552678970d0c144` | 0 |
| obp-api/src/main/scala/code/api/UKOpenBanking/v3_1_0/Http4sUKOBv310AccountAccess.scala | 15426 | `b5112373c9f2a872017a90c657378bb4ed903f468881f8220b171c514dd042a7` | 0 |
| obp-api/src/main/scala/code/api/UKOpenBanking/v3_1_0/Http4sUKOBv310Accounts.scala | 9665 | `cd5f98ca9edfa3a20c1c3a7be5ecd6937b4f961043f45c0f0d108f7b56d4c982` | 0 |
| obp-api/src/main/scala/code/api/UKOpenBanking/v3_1_0/Http4sUKOBv310Balances.scala | 7234 | `a3e969d81fab56beef5f33afc65189d12278eea826e617faa0a508cb3f3c6e11` | 0 |
| obp-api/src/main/scala/code/api/UKOpenBanking/v3_1_0/Http4sUKOBv310Beneficiaries.scala | 9162 | `7a1686f4b483c26f7ff091eaffbe0c2c391f6d59606dcadf6d63135e50faca0d` | 0 |
| obp-api/src/main/scala/code/api/UKOpenBanking/v3_1_0/Http4sUKOBv310DirectDebits.scala | 6048 | `cdf23c8fdde44551e798b12be15955136b5d3f3451e0ffbcf685df721fdf1e39` | 0 |
| obp-api/src/main/scala/code/api/UKOpenBanking/v3_1_0/Http4sUKOBv310DomesticPayments.scala | 20033 | `8702147b2881cb861b953b9c4c3b2a68672e264a624346d7e7844ad8f9358f85` | 0 |
| obp-api/src/main/scala/code/api/UKOpenBanking/v3_1_0/Http4sUKOBv310DomesticScheduledPayments.scala | 19351 | `899f0be95c309da449ebdc5072b049296378dcf4b7b0e52375b3eada528b31c7` | 0 |
| obp-api/src/main/scala/code/api/UKOpenBanking/v3_1_0/Http4sUKOBv310DomesticStandingOrders.scala | 16183 | `f986b52330731f62cbd8c24bdc7c5dbf7ecbfcd7005ee016f988a6b975b9d7c9` | 0 |
| obp-api/src/main/scala/code/api/UKOpenBanking/v3_1_0/Http4sUKOBv310FilePayments.scala | 16632 | `2f03bb242637f13dd1230f86dfcf622ff81253dba189c62383256698086696f8` | 0 |
| obp-api/src/main/scala/code/api/UKOpenBanking/v3_1_0/Http4sUKOBv310FundsConfirmations.scala | 7876 | `83c74084a08a98b0726f465cf8fdded31e4786da516bc7e6b1da32ec42f7fb1b` | 0 |
| obp-api/src/main/scala/code/api/UKOpenBanking/v3_1_0/Http4sUKOBv310InternationalPayments.scala | 25908 | `9f2927572209a4afd82f746a6a72ad49f4e194110510489d649587667861f63c` | 0 |
| obp-api/src/main/scala/code/api/UKOpenBanking/v3_1_0/Http4sUKOBv310InternationalScheduledPayments.scala | 26675 | `144ea2a4942bd6e93894dac736272a6dcbcabf636d3309397ed11ee7689172a8` | 0 |
| obp-api/src/main/scala/code/api/UKOpenBanking/v3_1_0/Http4sUKOBv310InternationalStandingOrders.scala | 20915 | `8ffa292f2d59edc9d86e20df3fcf60c23f061fa0b4f812cae640a10f7c9cfc82` | 0 |
| obp-api/src/main/scala/code/api/UKOpenBanking/v3_1_0/Http4sUKOBv310Offers.scala | 6447 | `6da2f0f98b5feef5627f3159a7a90f95b888fc0de1b35d3fa8d9ea20272840ad` | 0 |
| obp-api/src/main/scala/code/api/UKOpenBanking/v3_1_0/Http4sUKOBv310Partys.scala | 6443 | `a4ec38cb947f9dbda26c351a909a666b1eb6c1bdd611b3015f67a1224a056ead` | 0 |
| obp-api/src/main/scala/code/api/UKOpenBanking/v3_1_0/Http4sUKOBv310Products.scala | 4324 | `98fe875da6ad64bd629b40264be249c10c586e8c135278e75df026103abc8c6a` | 0 |
| obp-api/src/main/scala/code/api/UKOpenBanking/v3_1_0/Http4sUKOBv310ScheduledPayments.scala | 7607 | `2d0746bc6dc292751cbbb23ca31c0ceff78848f7dd49bf1dea3d1a0c414e6417` | 0 |
| obp-api/src/main/scala/code/api/UKOpenBanking/v3_1_0/Http4sUKOBv310StandingOrders.scala | 9094 | `08e5beb8e28d94574fde13d552aab9b64f4411740e779991a993d6b64c1b3ba7` | 0 |
| obp-api/src/main/scala/code/api/UKOpenBanking/v3_1_0/Http4sUKOBv310Statements.scala | 52964 | `7e08ec0b860ca4696d69151258af2b105041abe8c4d3621567ae8912bcf91d7b` | 0 |
| obp-api/src/main/scala/code/api/UKOpenBanking/v3_1_0/Http4sUKOBv310Transactions.scala | 33328 | `66f0c56eae79945a323db1f8302670b372c6db282f5aebbf38ac6d096e61c00e` | 0 |
| obp-api/src/main/scala/code/api/UKOpenBanking/v3_1_0/JSONFactory_UKOpenBanking_310.scala | 21335 | `ddfcea7a5fbf6b6696070e68d24947e88c9eefe2c6a8d81857082b576fa336cf` | 0 |
| obp-api/src/main/scala/code/api/UKOpenBanking/v3_1_0/OBP_UKOpenBanking_310.scala | 1946 | `b8fa4e19e078d5bb3fe934cb9c542a6faf7c7c1f13608e225cdf746d0f527c3c` | 0 |
| obp-api/src/main/scala/code/api/UKOpenBanking/v4_0_1/Http4sUKOBv401.scala | 4024 | `856989046606a23173046119ca983b22e47a8687d8ac88235b4229ea197170b2` | 0 |
| obp-api/src/main/scala/code/api/UKOpenBanking/v4_0_1/Http4sUKOBv401AccountInfo.scala | 121310 | `f48444c5235bb445a55b3f10abb3077a69d12f8091865e040cc08de70300dc8b` | 0 |
| obp-api/src/main/scala/code/api/UKOpenBanking/v4_0_1/Http4sUKOBv401ConfirmationFunds.scala | 9506 | `6a3b65f9b425b122e313e14f1d311d1f143ae04685422e0e74c3e2f4e90274bf` | 0 |
| obp-api/src/main/scala/code/api/UKOpenBanking/v4_0_1/Http4sUKOBv401EventNotifications.scala | 3395 | `2bf72852322f89d2eaa0141706c7c1a47378f99e88271ab48ed3adf7962f25cc` | 0 |
| obp-api/src/main/scala/code/api/UKOpenBanking/v4_0_1/Http4sUKOBv401Events.scala | 9104 | `ed9fe9f88d836a4b74b6c24c9363c0ee875408d5020cb3916fc79b82054d7305` | 0 |
| obp-api/src/main/scala/code/api/UKOpenBanking/v4_0_1/Http4sUKOBv401PaymentInitiation.scala | 323257 | `f7e5b2cbd4dd8782fbdaa473f042cbc20aee6bb580422eaa91daeaf700e0c57d` | 0 |
| obp-api/src/main/scala/code/api/UKOpenBanking/v4_0_1/Http4sUKOBv401Vrp.scala | 74175 | `dccf770bd8e551e67814f783b7cbd602523efad29ee6695bffb3f9748b0bfa75` | 0 |
| obp-api/src/main/scala/code/api/UKOpenBanking/v4_0_1/JSONFactory_UKOpenBanking_401.scala | 16608 | `01ba03bc4576212ee52486cc87ee45e41d391b9f8ab27e7ccdeb0e7c1cbab132` | 0 |
| obp-api/src/main/scala/code/api/UKOpenBanking/v4_0_1/OBP_UKOpenBanking_401.scala | 1890 | `9770602ee135cf55b037b8892ea1708b26a1f11db2d5c66984976e402969f6d7` | 0 |
| obp-api/src/main/scala/code/api/attributedefinition/AttributeDefinition.scala | 2576 | `7a4b89db4128d9665a0c00ef7380b117ffa46e99d65833e2ca6a23d34fb9b3d9` | 0 |
| obp-api/src/main/scala/code/api/attributedefinition/MappedAttributeDefinition.scala | 5365 | `f9277ff252947c6a453af1f90deec12cb7b39ef9bc715eada213c6bc2432d383` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/ConstantsBG.scala | 2400 | `9ec9c8cbc5eec4e08533eb119d89122766a96e79bb2a7450bd8de6f2094b8f44` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/BgSpecValidation.scala | 2803 | `bebf28676c7a4b1e4b559b713bb95ec71bb41a05b4bf06ef2055455c00231c2e` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/Http4sBGv13.scala | 2402 | `2498222a24207c8177e768f797d5c6148c447d054610020664b71b6a5fafed39` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/Http4sBGv13AIS.scala | 77030 | `6911be10fa260bf48cacf6c563477fe2941d04cb0a59aa3df4e2148c7d41b2ec` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/Http4sBGv13Alias.scala | 4205 | `f6ecfce57f3613c306f783389d6516db19c757dfa9d97a162946df99a176fc5c` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/Http4sBGv13PIIS.scala | 6375 | `e1931d3f627e51b5014c69e6a7e3fff88d3711f30320d121ed21169aa253ad9d` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/Http4sBGv13PIS.scala | 74491 | `7cc69574e06f1365fbc4b08f9f6289c5c137895699a9449599e3512d5a24bce6` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/Http4sBGv13SigningBaskets.scala | 31118 | `4bd0fbd4805a025f363da9916911d79173239a99a0d17461b907aa7d127eb38a` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/JSONFactory_BERLIN_GROUP_1_3.scala | 45261 | `1e973335612f9669445fc3ed6a213bfa4634aec04e36773dc7db75376c79aeac` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/OBP_BERLIN_GROUP_1_3.scala | 2194 | `ffca42ae8090b6e999261a0da8cfec1fc36dae277718e113a730ce9a411e9db2` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/OBP_BERLIN_GROUP_1_3_Alias.scala | 3827 | `0fccf942b044ae521b01f2695001ce7114d7a31d470f2fa842c507eec7aaa0d0` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/AccountAccess.scala | 7243 | `d5888948a8308d8b54025c066505c9215b248a8c9cbe9cbb842f8bfff873438c` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/AccountDetails.scala | 6938 | `a74331e7b351c0f78726adaaadbd35d3a5dd86871c4159fb41ac02160f3ff01a` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/AccountList.scala | 3937 | `9b364b95ebc6c7205f112b77383d899b2c5ce0cd7ec2b467f8542ec57b12f198` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/AccountOwner.scala | 4099 | `902a4fad0db29b418c2a0cc814f850b74facc1ead239eb526f3c506b7d333c18` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/AccountReference.scala | 4948 | `5342ec678e9201dab80ca976a8b8fc1063146e68f1a54c35d0617a6c456a84cb` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/AccountReport.scala | 4187 | `cb22c3bc9c7a37ac0c122b4ac098152284e074ba3dd0683da2a484f273779648` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/AccountStatus.scala | 3907 | `d5e475c0827b1aa27e320375da100103b24ac85205dfcb4612b20c4ed2cb4885` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/AdditionalInformationAccess.scala | 5331 | `205219e8f3daf8760225ba5b615db6dea1a982ddff98e3ddfa34fa986d278d99` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/AdditionalInformationStructured.scala | 3970 | `a3e24da18700e6d682d1106b3273b2d4f3324d3bbc3d36cfa1fd5fb3fda258e1` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Address.scala | 4105 | `9c9874610069b532329048a33559f1eec8fe7983a64f350be9701b6b54c9e861` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Amount.scala | 4306 | `c21854120bfd9f4f05f881856e21215aea384929dc5b3ce0c04ca557f25440c0` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/AuthenticationObject.scala | 4910 | `252466d88771b27fc6201812863d5c3f27ac4e2f93d92d173dc383616cb18bfd` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/AuthenticationType.scala | 3912 | `c85e6b954274a10d9e12861f319f83d393db611778d3a3e1a25420e50b1306e9` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/AuthorisationConfirmation.scala | 4033 | `beb7fcc27ba814617ff5c3373c3b89e3d616b6659874958aa050fc7f944939ff` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/AuthorisationConfirmationResponse.scala | 4145 | `73ff76e67ef2d6f7742364a7d3cf98d25a2b6b6ee0fd494c6ec8966dc9c323f6` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Authorisations.scala | 3982 | `9047f8961d64f7c0bf0c74efecdbff72cd5ab7f5822969cda9c7369134383f10` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Balance.scala | 4721 | `94164a5c8f4dce8cb87cd03a9dcb1693e9f24d112617a123731e00574734e5d3` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/BalanceType.scala | 3905 | `f6d8407219e08bcde7b0bd3c49b67427a607bd882ed15edffd71345924cb3d3f` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/BulkPaymentInitiationCrossBorderJson.scala | 4466 | `7aa557dcf36b587d4f3fa826e3932d917c0799d501928a1eb2a64b1d5c425f89` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/BulkPaymentInitiationCrossBorderWithStatusResponse.scala | 4592 | `e6264b891ff09e5f16594a4a128fd9e9b437b3ae71102caf342f4892bf64730a` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/BulkPaymentInitiationJson.scala | 4664 | `5498f1f57ee6d547f0073409b8f7e6435a935e158f2da37ab42841020c96dae0` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/BulkPaymentInitiationSctInstJson.scala | 4454 | `5e4e4f2f0ae7f3946c8c46edda35ef2d45361a705553d17b80e01d5d52cbb604` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/BulkPaymentInitiationSctInstWithStatusResponse.scala | 4576 | `dfaabb1888d92990ee8a9c3844aab6bf039e867a07b2be14863e03c01dbd8124` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/BulkPaymentInitiationSctJson.scala | 4441 | `be803a1185595b098170b072e2065dfa4ffa2c0832be0bacba78971d7a0252d1` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/BulkPaymentInitiationSctWithStatusResponse.scala | 4559 | `8ce8010715da10a3e194bc020940716ad0d895a645f0aa17255ae63d2b90da16` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/BulkPaymentInitiationTarget2Json.scala | 4454 | `ce42fc8732eeaacd2d684b1e0d120c0534740ef28eb8d7135e5e65915be73b9d` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/BulkPaymentInitiationTarget2WithStatusResponse.scala | 4576 | `9e433608edca0389616a8d4f17ccc909e8894660b2f61bea97d3dd1eb87c619f` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/BulkPaymentInitiationWithStatusResponse.scala | 4946 | `e581be2d6e1b63c5dda1604eb90d6238d045988b7f8fb1cd2d42b950e040574f` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/CardAccountDetails.scala | 6161 | `5577c37425574e5d7ba70345c44e1758ae9387dbeb5e3be401d85c20b4d7f256` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/CardAccountList.scala | 3949 | `d671961137ce31856d044d37719b0815619e8c8bbaaf41990a4e03eb95e9d3a6` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/CardAccountReport.scala | 4114 | `942a84a2889668390e9dc36d034eb993c16503a9721f118d9f114bdc21e00250` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/CardAccountsTransactionsResponse200.scala | 4495 | `edbdd3f40c4ab1dda51b1eccd7e9d7faebc2db453410107dbbfdf68cd7da240b` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/CardTransaction.scala | 5945 | `71c82a9c94dcab8de66fa1a6a6be28992fb9123e8cc90e5f0c95ac266d4637cb` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/CardTransactionGrandTotalAmount.scala | 4331 | `557679a40efb48ff66306def04a0cdb9c6ef75cb0ab6fa2fc7dea4462d020b3d` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/ChallengeData.scala | 4978 | `bdd6ab39deb11d613e66fcc904859794fd1f02e3e39bc427810409b4ff78857c` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/ChargeBearer.scala | 3906 | `0eeb156086a82cb36ff77f07b5724ab4500e7813c366124fc354aeef30993217` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/CheckAvailabilityOfFunds200Response.scala | 4323 | `33a579c26e7fcda523c449f533614b69a365962398bd550070ae3e4ebd362e77` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/ConfirmationOfFunds.scala | 4147 | `19957005415feced0a279e71b29405340742c5c15816a6c027d7c5ea4a18cddc` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/ConsentInformationResponse200Json.scala | 5277 | `079484214247ec67879a6d4c7aa709883bba268a75272d914d5d0d99b1130404` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/ConsentStatus.scala | 3907 | `afd4cec0b2e6b6370e47db3bfbe81760479d51187f3bd1d12d2f82452ab76df9` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/ConsentStatusResponse200.scala | 4069 | `5201e8ce044bbe5b8998e7d0f3d1adf16af7e1c52e29a0622ba5c9d58af2bbde` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Consents.scala | 5066 | `bef73dc43f0ff63cca9d4652914aac7061fe11c9e578bb7b5ce718b647d6a303` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/ConsentsResponse201.scala | 4929 | `53a36853c13f3598e4468bd12ef48c9fb146fbe94c198f493ea1e08d173f88fa` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/DayOfExecution.scala | 3908 | `41e026d7aa4df077cc4e3070d0a02d993b4557629e81d15847c49c05e35e155f` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/EntryDetailsElement.scala | 5378 | `8400ed15ad7fe632f0070f201cb349ba17cb709e85192cdd92290093cc90404f` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error400AIS.scala | 4766 | `45c5dde108c583197b539cd2a3f67e584fd19b4deeb8061ce44ce2ae756a935d` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error400AISAdditionalErrorsInner.scala | 4418 | `9bd1610f7b1b6b7e4bcc739360d14b5855dc1f92dedf65df17321be0eaee99db` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error400NGAIS.scala | 3994 | `576ce27ef3312a7c789119db0447f00813e88c4caa10cd804f0967cab529ae1e` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error400NGPIIS.scala | 3996 | `6abbf1b8b1bf2d39d3ca8513ed6c12ad8f6836cbc210add2cb1449951eb19c57` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error400NGPIS.scala | 3994 | `a3e1fd2175fe69e58b24b11715839c7b3a20bbe8f07d8580de3812147098ffea` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error400NGSB.scala | 3970 | `d42b769cc65757a5e12069f78e49ea2fa4c5f18d9a6fa2d49ff1949c87808987` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error400NGSBS.scala | 3994 | `ad75140b8de986e49b6b4c0eafd4b84619423a03606774fef8ebdd0721ad013c` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error400PIIS.scala | 4770 | `7c5b959fd2df3d673415b2852192262cab41451776b6ddcacfa4b862bd45d3f4` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error400PIISAdditionalErrorsInner.scala | 4421 | `9cad91ab6a7fc946fe987a9686b1c9d943903d65e54424f7f9287722b84869a0` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error400PIS.scala | 4766 | `ed717c42d1add27a4cee9c71158f424eca78c0c5840eb13d0cca4ea072180e67` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error400PISAdditionalErrorsInner.scala | 4418 | `c2714654dbfc0a7ee8adc8d5871f2c809900c101a4266e9084081ec13e39d4fa` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error400SB.scala | 4740 | `835a39500d0055020b81064b5335d5b72c4a7e7d2f1650cce6114d10bb14e629` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error400SBAdditionalErrorsInner.scala | 4393 | `8b07563b6afecc0330ef03d1fc04384bfe585a949e2e31ab15404cb357b8c856` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error400SBS.scala | 4766 | `7b49f2551c877e788ac09a8c72581edae2e9f28bf2d5851dd288bdabae6ba272` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error400SBSAdditionalErrorsInner.scala | 4418 | `b0260e57a3c57ccd1ba59813f304b57c9da396d80b01c47a10f003d758ce9bc5` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error401AIS.scala | 4766 | `ff424802c1e43af8c68b1975fbc4478cab958acae671eaa214dd7c669c4636e5` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error401AISAdditionalErrorsInner.scala | 4418 | `147dc18c9b0b60ce2f06958f91d492449dd890c5b487186877ec8b419ba4efd4` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error401NGAIS.scala | 3994 | `ea01cf227d78284aecedeef65525b9dc7317c67b7755c00578fb77ac8f7db9c5` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error401NGPIIS.scala | 3996 | `f019ab16415845a2fcfc544d33e342c1c18e7c208bb2b778d7de3c9dcd9a5c6a` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error401NGPIS.scala | 3994 | `932198c8740b9e3e517cfebeda5043907558ede1662a84a4c6e109442a516955` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error401NGSB.scala | 3970 | `753189de13fcd1d6e4c9a43e37b4b26368ad90a54a6d25f7f4c900d7e7f95433` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error401NGSBS.scala | 3994 | `4ca4933e5ecc35a2727343ef7f2024a7847270aafb5efe45320c919956aefb7e` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error401PIIS.scala | 4769 | `b7f56827f5aeee3b75974e65f6f2cf73d6f1aba19b4d46b1ff83600ecfb795eb` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error401PIISAdditionalErrorsInner.scala | 4421 | `73c917e060eeb3e4844c7e46fd366c0518ec79c43f12b30afb9c389918bd16a5` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error401PIS.scala | 4766 | `9cfd88457d9ad3c59e8c49bd6ef5a0d5086452ae4926d878b2cf5545f056b5f4` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error401PISAdditionalErrorsInner.scala | 4418 | `a0169a19b79ef611cfc876531eb66a06ec9c540c79a809b45b3279874233b83b` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error401SB.scala | 4740 | `788a672c0a5800ef0f935b7f1dd41ead24f5cc902e5b8b22ab6683e36f9e103c` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error401SBAdditionalErrorsInner.scala | 4393 | `e95133c24c32290663642e4ba62d95a478e2bec8249492c1039592a9c853d23d` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error401SBS.scala | 4766 | `b705b131ecad9b011c75201bb682d6653d28845691db17d0d052e3d76a04c057` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error401SBSAdditionalErrorsInner.scala | 4418 | `2e1c46f4cb38669df04352745392ed42d5f8db7db77e48acfaba9464a87b5011` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error403AIS.scala | 4766 | `b1841c8519af4c07e9318055d4a625b329dda60acde9c10789cbf988b1477640` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error403AISAdditionalErrorsInner.scala | 4418 | `858127d0c831312394e5cc9ad29878bc4716edf83759ca9332357d1b8cace565` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error403NGAIS.scala | 3994 | `4c4a15b4667c940d6da2da0f293ab1b1f837815d747454e1d1a44ef669234973` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error403NGPIIS.scala | 3996 | `3ee71fdf7f447fa29591b974ebf2966c904387ba58a98664fa99048697ef3a01` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error403NGPIS.scala | 3994 | `d65ff1b9e139940792cc7e5dae457cec7bf7c1cc95a0ae4f935d91243cf7c27b` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error403NGSB.scala | 3970 | `cd2f000f07edadce4b6082a9e38b123861c891b3c32c7949df21222d262421fd` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error403NGSBS.scala | 3994 | `832ceec693106d5bbac386ced1c258e75367806e0495788d18eb8576fdba986e` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error403PIIS.scala | 4770 | `84f84858bd7363705f63cb67b06265583b4c7a7647e3ff868ed2c49133408576` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error403PIISAdditionalErrorsInner.scala | 4421 | `f2e6c1382522d9c776cb16598492f2ff8d3404e4eb0314c5a9c895b902924c1d` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error403PIS.scala | 4766 | `eb6ac5033f642ec698ee9f5cc6aa3275e6e8f82b1aeaffc2b120f668d8dd8cba` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error403PISAdditionalErrorsInner.scala | 4418 | `b3852e55c8d9c0b7a670f002d3caa325b55219a4dc5597f692f60a4a9bf236ff` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error403SB.scala | 4740 | `d3448e9a1285866cc8d061c8e18afcde5e783076fc2515bed30f6aa68081aa45` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error403SBAdditionalErrorsInner.scala | 4393 | `369797a5c912ee46603b42bba1106617743ce7318065911a62547a44171e903f` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error403SBS.scala | 4766 | `bc01217ccf9eefa400a6ee223a4dfff010cfa637181899616a8d00d705b99a15` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error403SBSAdditionalErrorsInner.scala | 4418 | `30aa6037294cb04b8342edcac94f1610277020a31faa61767cc9e490b4f2e7c5` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error404AIS.scala | 4766 | `8657f9f7f04289cd2ac84644b31533dba83290c3aa701645f6fbfeb908ae0893` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error404AISAdditionalErrorsInner.scala | 4418 | `1f7f0b1af0daecafc996337b4dac6f7ea191745c33400f4550eaa2ac93c31e7e` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error404NGAIS.scala | 3994 | `8e6e1474678ab0e80a33b84171ddca4284fcc09a36354b4c4119766433c9897c` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error404NGPIIS.scala | 3996 | `f628b16e7c089e2e5ab48ef5cae3ac096b1336c95d7b0d9da8c1dd9bd332cef5` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error404NGPIS.scala | 3994 | `0d7b09ca235c5b04c9d1da775745d3b3c5c8b5c3fa03a13bf3d1e6d3532f45aa` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error404NGSB.scala | 3970 | `dd17328b690426fc6fcb5c8f1cb3b8a69f7f2f916da90838016882eed3e2a04b` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error404NGSBS.scala | 3994 | `5cda21d22fa6cd86c1667735c42347bbf75896146eeab49e26fbc94959e53925` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error404PIIS.scala | 4770 | `08b1ce55ad8ba270a69865305bfb14346701df91c71fa87a33083a4d7edc6ff8` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error404PIISAdditionalErrorsInner.scala | 4421 | `a35f96270ab33dc832c2f50e2a546dfb745d87047bf51c6033b366c5502f060a` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error404PIS.scala | 4766 | `ce2318b8a7ecc2a8d212110f4dbb2fd20b65bf3d6004a50e3a97560d3a1e0362` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error404PISAdditionalErrorsInner.scala | 4418 | `2f1b1d9a21cc07b856f7cec5e1353f5bbe2a9e5467d5e886a8a46666835ec4d9` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error404SB.scala | 4740 | `da798c0b2f74a6e1ec60b4f5f60842e4a2da4b60bb9af702a05ee3d0eecd7597` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error404SBAdditionalErrorsInner.scala | 4393 | `e86e384795206eb4d22cecbca17035bfa49b36fbd9961c6e9078971c3de7109d` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error404SBS.scala | 4766 | `d265c55e217ff9c829b698daaac28b9058291be4978233595c526ba947ce3bf8` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error404SBSAdditionalErrorsInner.scala | 4418 | `ee13b2de5b2d4044d34b36dadd223f44d3a560e6dbc73be52d1a62ba8849fb43` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error405AIS.scala | 4766 | `372689cad5689fcdae5a2ed753251ecb29dcce1dc31e00caa4dd642bf342e23e` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error405AISAdditionalErrorsInner.scala | 4418 | `21b197a866e9c0011459182aeff7191b0bc822e88441949b7bf62bc5ca02e415` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error405NGAIS.scala | 3994 | `646a82430a1698d6ce6260610af3992c6c8e3080f0af5302193f4027d0dcc665` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error405NGPIIS.scala | 3996 | `890c7e3ebcb0b01f4d5d1384a6deb8d0efeab3b72371d82ef82e214fc3764da8` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error405NGPIS.scala | 3994 | `236b7cbcd616e9a8bf1a8c67947733a13a73467f5232017a95b2d87495842548` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error405NGPISCANC.scala | 4002 | `d4fdb01f1619406adfaec6869912285dd0bf0cda1310f65ab09a237c51dd4f72` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error405NGSB.scala | 3970 | `9da692abe8c21fc317caf5a8e4a4159e827d753b3fc8feeb0e537fe25b9a4925` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error405NGSBS.scala | 3994 | `f56b675e8730a1504a1ebaf3f6b55e7cd546f9a2da172bd00f4c51314d267d68` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error405PIIS.scala | 4770 | `2305303d314bd1d908575175e76a5809fd254fb05cfb3dc5e267aa50b6ff92b2` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error405PIISAdditionalErrorsInner.scala | 4421 | `ff0086788810867995853b4f4678c964ba5318558b6f53385212952e0c2eb7f0` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error405PIS.scala | 4766 | `a07c084a96e205bd099f913e403e7c63b6d3a14a25ca03e4e2de362bc06c63a2` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error405PISAdditionalErrorsInner.scala | 4418 | `55bdb3a5d936738e01c38d84d16ee0ab0c76c38b97d8dd806e028806909ccefb` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error405PISCANC.scala | 4782 | `7136ab0a5262eb2804d1ab18bf803b534bed2b86a73d63cf2aa5cb014a21de16` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error405PISCANCAdditionalErrorsInner.scala | 4430 | `a9d242718438e5b5bb964bb8ba2f6d11aabdedf5a811762e1d735a0184ab8e09` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error405SB.scala | 4740 | `1804db20dd459234867f91d1b6b24766d344d2f5287993c9c1c3c76663efff28` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error405SBAdditionalErrorsInner.scala | 4393 | `89e479373be8c786640783390c1298322af757ed2e491a7164f1f562192a96d0` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error405SBS.scala | 4766 | `170796c85697229378583317f7fa6ce986093b63bfb4d35d9cd9422c664906fd` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error405SBSAdditionalErrorsInner.scala | 4418 | `d7991f0c1b1e9a35afe137ba28ce3e1e9e648692fdb0b0eb843b611f7a966b7e` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error406AIS.scala | 4766 | `c6379d8f02b743955da3b46580360af298355ad3901dce69745049f81f93a4ce` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error406AISAdditionalErrorsInner.scala | 4418 | `a4d1784eb8a62acb2d7826be0d6a39649251d82b0c0ede8d6c3ffddf24649405` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error406NGAIS.scala | 3994 | `39b54dce7aaaf6d6e2dee7810306a4eafc3f799ef6394d3ab585b37ea6841881` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error409AIS.scala | 4766 | `f52cef48e6c67ba2d47eacefacb9642bb96edec76949267737f2bb8f6d20a16c` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error409AISAdditionalErrorsInner.scala | 4418 | `e627387646a223e4daa74393a51b274190e0054fb2360948f3616c4f0db93526` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error409NGAIS.scala | 3994 | `53522fa8e805363e67b6d935be4393adb76a54ad15d3be9f604e3f9142c3a802` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error409NGPIIS.scala | 3996 | `f6cde1f596814468280c6924e6e9574be271645058bd2fb82b9cebcd2961e497` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error409NGPIS.scala | 3994 | `1a27b9957ffbf9dbe64f7755f3920c5046afeae238286c0cc4389d6c521c836c` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error409NGSB.scala | 3970 | `80d9747371281f969972345753ecc82cd9eab929eb53b9e0845657e261928954` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error409NGSBS.scala | 3994 | `c7ad4781d43206cf68be4357625c3a6836e9defc7db054dd2bb23ce79aeb75d7` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error409PIIS.scala | 4770 | `e82bb455b73310a1caba349f646d3ef20f5dbc76d9b3982fad6c54e7f5acf0b7` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error409PIISAdditionalErrorsInner.scala | 4421 | `c8ace74b2af544948931824191ec42f9632c33670b8e1d088b8c8c1d30be1836` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error409PIS.scala | 4766 | `ac8f7aa73e8dbe098ad6fa628767524ba022ac468faaf3da945b152690938ab0` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error409PISAdditionalErrorsInner.scala | 4418 | `9f85ecae2e25fde677ad538dee2186ade9b2589dcf4f9c6bad1dfbad36ce097a` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error409SB.scala | 4740 | `1295553114c7cf028d6df67cc5712533efb194c6d89c6c3ee062f1460c7d34f5` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error409SBAdditionalErrorsInner.scala | 4393 | `8e903d921736b8099c850fe3069ec9d60e63cac7f9469ba635273c0e6e95ac27` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error409SBS.scala | 4766 | `5c4a7e36150d1125adb4583a0f6e006b1bcab9272fc4e6a7c73e459c91a685e5` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error409SBSAdditionalErrorsInner.scala | 4418 | `8646d6615d990e0d5ab50dacdf1bfbfb8bfa998bc73706a489fa2e675accc5a4` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error429AIS.scala | 4766 | `f35f179e390399c79bbe7ca1362874a4c2cfa34411934faa2ffe3511ad9e6e4f` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error429AISAdditionalErrorsInner.scala | 4418 | `08fcb5a14c73c58444c0e3fe4002639380623a6b0fecab5fe07b4a8dc492fa78` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Error429NGAIS.scala | 3994 | `d1e105f99f6c537e9609d711dfa3cd06d3fdd5fdcf684cb93b1c535b85bc376a` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/ExchangeRate.scala | 4144 | `84ddee889c3ec0ad7e1746f9993dafc36cc3d427d683615de3970d204e5fc3a7` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/ExecutionRule.scala | 3907 | `a85b014c4dc157cd293be6ee2204591fbea1b3439b8de4dc292598a2d5110ece` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/FrequencyCode.scala | 3907 | `b8a6c466991249b9cd659c90188018331aaade9184492289eb1c5998ce73b0cf` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/GetPaymentInformation200Response.scala | 5670 | `f40fb1cc52e84675a1422b0671f7b04ac0da4585583fb61fe768d63801d6af7e` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/GetTransactionDetails200Response.scala | 3972 | `014ed40d89d8ff294870e69fb8d0e005e260d928cf00c84c2172f3aeccf8a0ed` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/GetTransactionList200Response.scala | 3923 | `1cc7f8ff394a198eefaaf66749d127776e54bba4dfc311258d937bd448219da2` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/GetTransactionList200Response1.scala | 3924 | `9d28240a011e585dafd65d3663e37fecae947fac07bb551f4acf26d8ae8f75aa` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/HrefType.scala | 3960 | `b2a39fd60d6ffe48682751ffa4661b7bf7ca3fe254ecd920daa9af524c971c8b` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/InitiatePayment201Response.scala | 5338 | `7912de6cb11d79f9aab83ed870bad3cac5fb5a3f16ea936b4052991cb400f0e9` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/InitiatePaymentRequest.scala | 5983 | `a727c7c80c8af99476dfe37d59a80894742654cd2e7d9de9e31b9757bbdb2ec9` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/InitiatePaymentRequest1.scala | 3917 | `3bd04028d8698f497da44846bdbc8a9e2e99a7c0cbf8ba9d26ce45bca2e93274` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/LinksAccountDetails.scala | 3990 | `f6138072423b362dc004c7801de5e8a515acca6177c2460dd545e70ea42ba8bf` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/LinksAccountReport.scala | 4069 | `f681114780195358453c8299c1e1776386038346a0c3d7520a0649bab1dab53e` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/LinksAll.scala | 5478 | `fd4c022fe54454a56e30023b94bbf110fbd25342d4eedc3ce142ab2441bba94a` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/LinksAuthorisationConfirmation.scala | 3961 | `b29cfdfa854901a180d91e9bf32e7c54f617ddb7bb10e5e277c8adbe9b86abc4` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/LinksCardAccountReport.scala | 4125 | `6bcd63096b49cd4d8adf7b3164312032023bde00aaaa60942a8327edc30b7ff5` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/LinksConsents.scala | 4545 | `af3534ab9d39966456eaf19c71a37a0836b85d1038186ba5372aea0601e5aeb4` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/LinksDownload.scala | 3928 | `172e7f13945a7e5d02bcb818f7b3a448ed12486033197e08d3e48aa80f4f5a98` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/LinksGetConsent.scala | 3984 | `ca94cd10bb08082ed7b7189adaf64ce092f4db97107ed4e7d091c4c7f7336353` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/LinksPaymentInitiation.scala | 4554 | `d380162f393e2dba45b46798b85ea22fc9ddf53274af7dded75f87e812b8637f` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/LinksPaymentInitiationCancel.scala | 4261 | `2ea0efe916b0e024147fffc13f3d985f50e0d214cb650ff1564a21c4f204fa78` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/LinksPaymentInitiationMultiLevelSca.scala | 4282 | `33a28731315b35b90577991a642a390f1d4a3e1753bd39190823cff2db7b8e38` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/LinksSelectPsuAuthenticationMethod.scala | 4369 | `5529cb74a37b0c1931f671c4fd508513163811c14392e66d2b19632713ceeeb4` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/LinksSigningBasket.scala | 4509 | `e7484c9538019dcbb759d2e488d3b917e321523256802e6489e6ae71d86d3d27` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/LinksStartScaProcess.scala | 4370 | `650c24716f943fa8017c98d6b0e805da0bd0dd9c959551aed2d674ea3c2d78d8` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/LinksTransactionDetails.scala | 3948 | `6066dd90c84aebd95b90da58201ec5a9640e1353ff9461f2e83b717f63ac67ca` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/LinksUpdatePsuAuthentication.scala | 4196 | `ce21e4b290791a470a8ac524757109eec2320c8b6b286899fefab25ee00d3bf7` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/LinksUpdatePsuIdentification.scala | 4014 | `b0292021dced924c186797bb170341390dfbb0f987981977f2829d814bd77acd` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/MessageCode200InitiationStatus.scala | 3924 | `65731cb741e201b707b62c5566fd0c9f16235245a5047ed15e423fe86f0fde1e` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/MessageCode201PaymentInitiation.scala | 3925 | `66c99d1fcd41c8de06705692136c01046b7981d449f4d8bc40fddb7f433270ce` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/MessageCode2XX.scala | 3908 | `c7b13465e4c17e50e166a9214dae8b02406c1ea18d60e1d2e130bf4102fb5391` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/MessageCode400AIS.scala | 3911 | `5ff65bd1071a09568601386567ef2c5e0367e3b9e6fbcb43502e89a4ae3341f8` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/MessageCode400PIIS.scala | 3912 | `863b25656b4cf27b12958435b5739131b71ffb732953367f2e96e92299f85c8b` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/MessageCode400PIS.scala | 3911 | `c0eec3e5760a49aba27cc618a7c4bb21f0d5ba11928a7c8aa4b779d39713f211` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/MessageCode400SB.scala | 3888 | `77d78b1a8d8aa66c1dce93f9636017cb073fdd3545b8ee95b0bacb06ac8f3337` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/MessageCode400SBS.scala | 3911 | `8be6a036f6aefd54c486d297d12ec07b215f6fd20592b09f35efb1a52ed1e7a3` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/MessageCode401AIS.scala | 3911 | `5e005f423b7d6409ab0c781c26dd5ae39691914f0a8774591bcb5a4570ae998f` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/MessageCode401PIIS.scala | 3912 | `ee230d2f472ed4077232050b9d6bbc055951279498b0e941a2445ff09d6c3726` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/MessageCode401PIS.scala | 3911 | `857dbfb63c10e4915b6b8b2745d03d1e6b037b8ceefc8fed08a80ca4da7eca1a` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/MessageCode401SB.scala | 3888 | `40ee6c8808ddd50f393d67e0793004e920ae419ef802245b2f989441b9561b26` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/MessageCode401SBS.scala | 3911 | `5c8a19119fb2b1a2f35909a81a64e2c7d54a3ce4efee23ecac13b49f107fe073` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/MessageCode403AIS.scala | 3911 | `e18e1906fb7073636d13cd8c49a67e0f143e786b27fea89afbb22039a397b32c` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/MessageCode403PIIS.scala | 3912 | `07ccad2301631ad59826cb63dcd7ef128d9c31a3cb9937cdee7c6807af6ee6b8` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/MessageCode403PIS.scala | 3911 | `10b467a99ce8e068700c4e86befee73cb62c7a5d8c25acedcd424683c598b974` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/MessageCode403SB.scala | 3888 | `673381c8f2bb2b6a171ddb48b44082cc4fa85f6e60ef413de7bda0b8287838c5` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/MessageCode403SBS.scala | 3911 | `f9e2e8a52e270d9076c83a72b7e5386a00e244704b11a83032359fe504d60834` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/MessageCode404AIS.scala | 3911 | `1af97456e4cb35d03a81666a3e39187bd3dd805789e3c7f0b56453c41c67aa59` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/MessageCode404PIIS.scala | 3912 | `d766bb9cc47695e888630bc4f1e7b877037e894921250ea5890d496268257416` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/MessageCode404PIS.scala | 3911 | `1333150186d56ceeca0ea33f6bd8bc4a20dfe56171250a7ed6832cf7ce672e3d` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/MessageCode404SB.scala | 3888 | `8d7e9af52f5a9d22e4ca1969e732e68ea6e9920b687d851d4bf68d794bdf65a8` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/MessageCode404SBS.scala | 3911 | `bdd16016acb62032aa9fa611ddecaf18acba2d795750cc5c1376f68b6443da0a` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/MessageCode405AIS.scala | 3911 | `a3137783c7a802b9d24660d4f0cd1885161e5d3b02df91c66d1bebcb277a713a` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/MessageCode405PIIS.scala | 3912 | `71938d4d37f0ccf7cb4fc01b0f1bcccfb3e55e97691d676d60983523295f0a32` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/MessageCode405PIS.scala | 3911 | `e81749800c213587ff57336182af44f9be07142785605acd6ee44452cd1d57dc` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/MessageCode405PISCANC.scala | 3915 | `658249c893c5c043865a130b7e33c5a78c9e7b1ea8ff2d672eb0cc28c43b982f` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/MessageCode405SB.scala | 3888 | `13430bf0a28d9752a582d61e9f21d8dbf2db6cae8332a73cf3a17c87a1bada3e` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/MessageCode405SBS.scala | 3911 | `a02ad7fd262bc9ac464fc00181cc4f2f0b74a1aebaee47107f20b27fc80e993e` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/MessageCode406AIS.scala | 3911 | `333c2f3e1551677ec7211f39289eddb109c87188e487757361d8631e37d273d4` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/MessageCode409AIS.scala | 3911 | `982f14468e3fc4e110d3127c0328e8d70db34a39bc5ef4357fb69084317b45b5` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/MessageCode409PIIS.scala | 3912 | `e8c97d6d5664e60f840914a6411e0667e5a7d1e5ec0d026201604993776510ef` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/MessageCode409PIS.scala | 3911 | `9065f7c1e532e29736c8aedfc55fdfefc64a409275fd7540c7b761df347be3fb` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/MessageCode409SB.scala | 3888 | `57aae5e158c96dc0c6694f1f1c924ab0dccbfeb3fccdf8e8818ca1d84cf45374` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/MessageCode409SBS.scala | 3911 | `24986e09e56f85d7466aebde7598444437487a704ab0ae22b7e90d7cb60768d9` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/MessageCode429AIS.scala | 3911 | `25c7f3c059a800308b3c5860b2d4d56e84cccb9ac86d2fef1a0a8a1ac264e642` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/OtherType.scala | 4247 | `c24253620306d7c25dfa82bb565645e148d21ff7a0de6616f96cf0fb6c69c6a6` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/PaymentExchangeRate.scala | 4344 | `65ac3db699d255e16d53ea49903c9f58743282a252dd239a65ca887c762dd601` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/PaymentInitationRequestMultiLevelScaResponse201.scala | 4657 | `c26f2affc8538602a68e6618655142176282db5b0a82b5fcdd3d9fa70b911e9e` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/PaymentInitationRequestResponse201.scala | 5341 | `4e6ce3dbc59ba6db93cf66576117e32c1f9b261128c738e55bfcbfd91f08955f` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/PaymentInitiationBulkElementJson.scala | 4363 | `42a0104b460a12a0c1675088191f35de6b6d442a7a2fc6e80fb8124a11760b84` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/PaymentInitiationCancelResponse202.scala | 4796 | `de51e7bcb5e8cf35d8470b4c56d59d855cccb2c2fdc09e2a582b232bb0da146d` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/PaymentInitiationCancelResponse204202.scala | 4781 | `d96794f4c0ebb0e909a2a8d0fec4c16205f3a6302627b338766c6fae802aa8c0` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/PaymentInitiationCrossBorderBulkElementJson.scala | 4183 | `45a5024dca3bfd43e8a2390aa6f6b82d38de50c4ff72b0aca12bfa21a082a204` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/PaymentInitiationCrossBorderJson.scala | 4207 | `791b47847f2a692e23d03058e278c81aaad1e4da8aaab4f1715f639da140c324` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/PaymentInitiationCrossBorderWithStatusResponse.scala | 4340 | `a7a6b1eef5bddf7f315b4f97541fd5b739b2bab1fb42ba5d1ac7dbc81f7eb748` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/PaymentInitiationJson.scala | 4387 | `6801cc782ab8caad4dad81bc70aa4fd2616b3aec1fa9a3e6cbb00e9ce34632b4` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/PaymentInitiationRequestResponse201.scala | 5839 | `9f34758295c26bd6f4c02c7d2f96bc380e500f1b8eae19d09f139fc4c9714089` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/PaymentInitiationSctBulkElementJson.scala | 4269 | `0072236467b105a59e083c38059d1ef300ce258c2da9d4856ab51bca68e442b3` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/PaymentInitiationSctInstBulkElementJson.scala | 4228 | `40b3246c59aba3232bf7cd17ff6c05fa45786c5be92614dcd0a025b24dd3caf7` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/PaymentInitiationSctInstJson.scala | 4252 | `0ae202441c37821be46e2e09f86ccdb0f1655078ac7e2898abb2551f5eee4ac4` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/PaymentInitiationSctInstWithStatusResponse.scala | 4381 | `495496313cce41d9074da1ee43cb30bf99ab95ff9ea53bfde5a49206efb0feff` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/PaymentInitiationSctJson.scala | 4293 | `af4c46a083e944c5cb8e80aff325ef0051d5c4dc0ff80bb205547d07c445fe68` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/PaymentInitiationSctWithStatusResponse.scala | 4418 | `d3935e6945da725bde5a6e556b2ae7b8357f7d506e9c2237d4d8cf3690ab11fe` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/PaymentInitiationStatusResponse200Json.scala | 5121 | `209958f88526322cf37bc756fc651fb41272b57a130dfcb520033d246ea5485a` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/PaymentInitiationTarget2BulkElementJson.scala | 4228 | `5a11082b9609992de2cc15265c5bcb398964c8c35a074c5bd14c674c63f4f48b` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/PaymentInitiationTarget2Json.scala | 4252 | `e565f5a08939a79339708148f04d06636dc4d30f925903c853e2075016a75567` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/PaymentInitiationTarget2WithStatusResponse.scala | 4381 | `9d56bd4574e0bcd92aa1cfb7465c431914b0a293ac7227aa8de617e2de7d2184` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/PaymentInitiationWithStatusResponse.scala | 4540 | `a91d3c8badcd0835ef396204b7798f90e0bf784cef836c38a86b0fc9090315eb` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/PeriodicPaymentInitiationCrossBorderJson.scala | 4672 | `0b0e39f43353ef07971b6662be849b441341c5b54ea8fbec6e887a746e8f6a8e` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/PeriodicPaymentInitiationCrossBorderWithStatusResponse.scala | 4755 | `6e8f371fefd76b5efaeb274ea8bd7b2e4686979817c64b4d7b980804780352d8` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/PeriodicPaymentInitiationJson.scala | 5250 | `0006b7ec5150fbfeb64c8087125fcbf20eb8146bfdba901e1f3e4a824c6e965c` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/PeriodicPaymentInitiationSctInstJson.scala | 4713 | `68eac8bc0f75e292d1a7eb65da55f5a3c11353202940f8ca19d8e246254f320f` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/PeriodicPaymentInitiationSctInstWithStatusResponse.scala | 4841 | `838c4a7d280e94dc5cd60cbea0dd6d612ede875fb5b43d39a1aca047261d40fa` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/PeriodicPaymentInitiationSctJson.scala | 4750 | `17f28cb0aa33672b12ca48d672991fb47915c578e6ab94e0c43e84c79a5c0590` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/PeriodicPaymentInitiationSctWithStatusResponse.scala | 4833 | `6ecea89ec3f2a87fe917d8d7331e324fe2d2f30fdcdb07c0cbf11128d5daf9b7` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/PeriodicPaymentInitiationTarget2Json.scala | 4713 | `2a1dacef53885b03206d3e9903f64430802309f45da256b7758d62867dd334df` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/PeriodicPaymentInitiationTarget2WithStatusResponse.scala | 4796 | `519794b37a67e41ccd2d345aacf3e121e1c86d0fbe52ad669ee93005ef574fd3` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/PeriodicPaymentInitiationWithStatusResponse.scala | 4956 | `61ba885efca9323b72cb1ace03913c4dff0dd399a1718fa7d9395f6425855207` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/PeriodicPaymentInitiationXmlPart2StandingorderTypeJson.scala | 4922 | `29c099d0531a11695d49d806fc04d07b843ad3c434a2987a97f288c46718ab2f` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/PsuData.scala | 4190 | `de28ec3972e6aca3f0e8de3ed01cdc06713f10cb9f3ff86716dd2b2d63b35a53` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/PurposeCode.scala | 3905 | `90f2c70ffd72558963c845fda911dad7a7f4b57bd3d7b507f0c53fc3c31110da` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/ReadAccountBalanceResponse200.scala | 4148 | `ae8384ab1e27a2b3b0e9838b6637d95c5b2c31d20dc1947d353ca835df026926` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/ReadAccountDetails200Response.scala | 3949 | `5472319cc5a8acb0249d097db990bb606adf5a53277782f16b9d960682205f7d` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/ReadCardAccountBalanceResponse200.scala | 4384 | `2db6a589351bb668c4db57dbc23e366db9cf4ddd0a6f58a1d704b5b434325216` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/ReadCardAccountDetails200Response.scala | 3961 | `bdb38c8560699deda4083639a1125c97d726d2feaf0673f2df98df7f5a685b59` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/RemittanceInformationStructured.scala | 4027 | `a77522588821157a02948dcd18deb5b1b27e1abad11f0acbaa9db7c98fa569d6` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/ReportExchangeRate.scala | 4238 | `e5d90921553971b7631eb791bb03a7015e2eb1d533150278cb88f0c02f2b3ad9` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/ScaStatus.scala | 3903 | `8a1cc8862dea3fe5e34798dda6356516893852a636dabc060edddafa7bfa9b11` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/ScaStatusAuthorisationConfirmation.scala | 3928 | `0a5b7bf03fa68cb6e878ebd3f51230b0900d99124009fb7ecd69717274d15e21` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/ScaStatusResponse.scala | 4652 | `853f7712e107faff8b278a9ab02c45dfa10efb28e03dcb86aef24a8869cd089f` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/SelectPsuAuthenticationMethod.scala | 4074 | `cc3044a03775ad921c2ad4715ba5deed0a9ff8197bf10fb3cf45d26530f2534f` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/SelectPsuAuthenticationMethodResponse.scala | 4450 | `29144afcbe4c50eafb4ce5fc8904a4fb45293bea268e9f8b8c38fd09ca02be29` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/ServiceLevelCode.scala | 3910 | `f99e8d2deb125d42b86db9095f2270ba8e2681ca219a5efbb1e0fc3fd5628730` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/SigningBasket.scala | 4050 | `e9b197b4bfdc8e1fcaa40dfd725166b51b3ff8306c24a78d17e60ea30a5ae551` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/SigningBasketResponse200.scala | 4187 | `a92735ff65927c3394a63d54ee12da3bfaa87cb794e6926d61f82d7edb5adf16` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/SigningBasketResponse201.scala | 4975 | `5361897f191391ce73cc27b1fbbe9fcd987f607ad287e0010d78a61614e6abff` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/SigningBasketStatusResponse200.scala | 4014 | `3478753ab7a78ef083e6429b381edfb9a9d498c93863337b6b257bffe2f32c2b` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/StandingOrderDetails.scala | 5789 | `c31b49913ac50347e1b80f9529d60595ae99f00a7b8a1bc793969e7561ba8668` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/StartPaymentAuthorisationRequest.scala | 4262 | `a1ca9c0f2b1a3f481301647fa56fef13f898f584e8afb1157f5265ff5869beac` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/StartScaprocessResponse.scala | 4891 | `b4bd8e5504e18a457c2858eadccceea2e7b97579080d77470c4b99e32bd56c3e` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/TppMessage201PaymentInitiation.scala | 4153 | `7dd55ee7931667ddf08a5999a551eaed3a5bc1c2451306796ef463e7f02af86d` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/TppMessage2XX.scala | 4102 | `95c10aef20af91deff795aaada4e373eaebcc9c0a5e7e7f59cdaa97bdca3582a` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/TppMessage400AIS.scala | 4111 | `e08b9325ee7e3e9a9ff9b0fe34c9bb8f604d43a0dc535f561f8ebf2bf89a910c` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/TppMessage400PIIS.scala | 4114 | `a3efc4fa9fdc3dd6955210706af5efafc5344a4491db574c44ce5cbe42500acb` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/TppMessage400PIS.scala | 4111 | `df2738e31a0b4f4c4eea8ddd18b95e9e8567c3ff6a7c313292f743a0cedf4046` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/TppMessage400SB.scala | 4086 | `b2ad647d43af0be4df42296827b5e5d299aa3fe55cb46e488190f77f395db670` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/TppMessage400SBS.scala | 4111 | `6956401e20aa6212068c0410a3ef9368ffb9ea914a1e8cf67f13e44352722553` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/TppMessage401AIS.scala | 4111 | `af67e07874ec14e0572e7e60c43b91735491fdfe7e2ab409475156a94d565a78` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/TppMessage401PIIS.scala | 4114 | `603df141fd79f1343291c9a9be57db2a978ba2caebc3901d217696624e737c07` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/TppMessage401PIS.scala | 4111 | `38d0a649017fd22dc2c3a778d7ab28f5472875ab8ef42476fbd70f8fe750d24b` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/TppMessage401SB.scala | 4086 | `d8e50d2e678923f247491c7544f0390cdc8e0d5ce2d88aedc51006d1acdfcc45` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/TppMessage401SBS.scala | 4111 | `6b9d9ae7872bf592de70eec033406904ace8535de9bdd90d501d5444f694f4ef` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/TppMessage403AIS.scala | 4111 | `d607783d79c8eaa94b763d1755e48f6783f293299e20a1dc315b4178189364f1` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/TppMessage403PIIS.scala | 4114 | `91f85b001ba62bc107544d748302736405a60acad1ea09ac77b511db730251d8` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/TppMessage403PIS.scala | 4111 | `a201e55fab2ebfac93ad566863dd676c1bd16bffe63274c89d26a404abcee188` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/TppMessage403SB.scala | 4086 | `4843ab65a84f435ece8f46098574348f3a9f07a0b4f91e43fe6bbaa0ec1923d5` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/TppMessage403SBS.scala | 4111 | `99252ad6698aeecdecc194a6997a15a959b9d5d49acb30bd768b796661f7fe63` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/TppMessage404AIS.scala | 4111 | `ce526dd08b264d5bc0ab9cb34054f4c4aac9915c4c9822633daf2258dee9f034` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/TppMessage404PIIS.scala | 4114 | `c23ab0f6db8f4d44e42878aeb750acc8a0efad9decff750d8e6acf4046f7ab8a` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/TppMessage404PIS.scala | 4111 | `cfc8d0571bd10fb0fbb14983ea6718d1b4934a937aa54eaa4af4a8842a5a7c9e` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/TppMessage404SB.scala | 4086 | `d23132e826f199ed2c81c77cee1b215f8c3e1daa2d0b3ba767e81e671ed45e7a` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/TppMessage404SBS.scala | 4111 | `2412b6cda753710447f5d8adeef03de8dabafe4f493a416aedede7e0d69c76ce` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/TppMessage405AIS.scala | 4111 | `42344c12c8f3569561680bccc5439c67ed88032f972707d43c29888556669073` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/TppMessage405PIIS.scala | 4114 | `dc6a690d552cef9e8b7baeaa8080f7807236ac8317497f78e105f1c1293a2f5b` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/TppMessage405PIS.scala | 4111 | `b37fd341d1226193fab0c331323b9a63803f669ce732ab0e9b17d82a4e7ede3d` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/TppMessage405PISCANC.scala | 4123 | `9bfb11696b5aa2c786d93f7bfe6960fd7f17d1eaddf7686235eeb37885c21a21` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/TppMessage405SB.scala | 4086 | `909f0663572194c00d973a0eab9feba9db03f61871013341b13ee5c1772c32e8` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/TppMessage405SBS.scala | 4111 | `f6cd5540c9f7331b7a4ec70e0482bc2b6008e9c7640a559743b86ef01cbf8fd9` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/TppMessage406AIS.scala | 4111 | `b0ab28888066a718cb94fdf4d5a7837487660c8ec9f8cf9802d4841c40878458` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/TppMessage409AIS.scala | 4111 | `8b58a8693be4073997a0070a880b3090f184fbd083bc07fadf60210b3a778eab` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/TppMessage409PIIS.scala | 4114 | `5f7f37cded97f5d33954998b6aa0a935638145c085c3f0d16c79145503006fe1` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/TppMessage409PIS.scala | 4111 | `6b48905acf5b9d5acdab18b55fd915b7ef9310f191d654bbbf00f67037b71931` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/TppMessage409SB.scala | 4086 | `a09c8b12878a838ac1425d350c0b460139b9723f107267870ca59de64e83567e` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/TppMessage409SBS.scala | 4111 | `a598f30bc51d028af7bb3d9ff06e6775ad857faa6e26daba211fc7f0d01faa2d` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/TppMessage429AIS.scala | 4111 | `41e1b23aaf6d87fbef558783768286af94875c28b06970cb5dd9b984ec2eddd5` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/TppMessageCategory.scala | 3912 | `ed7d8b07cd088a7abb7a168b82f1cedd8bf6c3cd0477644cc67d9eb47c3b515b` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/TppMessageGeneric.scala | 4144 | `7c25282bc5c8fa41a62ce57e37f7a79b0b0d2ada39a7b24b96157c5af36aae32` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/TppMessageInitiationStatusResponse200.scala | 4166 | `7cf09338c8233f417bdef10903c8323ad00fdd525a0b4cdb3eba791a2d922b26` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/TransactionAuthorisation.scala | 4082 | `a06344792582b1fae4cf59fb53819c62bfd1dbd8088c712cb0069dfa8e1b7259` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/TransactionDetails.scala | 6541 | `89d03141e6ec5e786d99c1812b7ec9e45f82c8374fe89a2b8ef75e89a57776a1` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/TransactionDetailsBody.scala | 3951 | `de3913451438f8a7185d86662d0469c013a2c709709605d69e24d1673c84cae7` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/TransactionStatus.scala | 6920 | `b4e2ba057dee209568155ea15f0eb48cc61a38e27f76f3a64f00e924f2ce3e41` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/TransactionStatusSB.scala | 3891 | `f520c99cc257d2c3c3e7a50d28e4c6baf270c601d579ea5bd608d9e7064c53f2` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/TransactionStatusSBS.scala | 3914 | `893d5c677ba85974c95a5019db3c7eb3b6d8d13a2fa90a647976f025b13f166e` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/Transactions.scala | 7969 | `e4aafb528f7b475c4d6b88f5338a44c4773ef67b69b57c716e943c61aa62a542` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/TransactionsResponse200Json.scala | 4247 | `2404501e185fe00d75fba7e2806af19ba253194f37054ae56caff0f153703c7f` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/UpdatePaymentPsuData200Response.scala | 5729 | `6ca19d5b1a8e8ec958a9d27944e5f27af399bf837c4e2023a23d9e6af0db9f50` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/UpdatePaymentPsuDataRequest.scala | 4372 | `8e1482074af9c876f0f61a5e53eca6113e5c51d321d3f88539f8d49437f93f82` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/UpdatePsuAuthentication.scala | 3936 | `d4a9912400d20781a245931e0022ed45c9940c7782fe4a4511e8596c4d6ef55f` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/UpdatePsuAuthenticationResponse.scala | 5142 | `fd1c205a1fd57f420459da567ecb0e58906764360959138ae526fd7acd9e8fde` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/UpdatePsuIdenticationResponse.scala | 4087 | `3ba9bfe65b487220a29dceccd3c02c16b0d8ce50a9b51d136795ad89d46fec46` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/UpdatePsuIdentificationResponse.scala | 4932 | `950370e00b5bdcc3c8993aaf50b3cf9d55b48601cdb5cbd1f3462dbf1cb70577` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v1_3/model/requests.scala | 3923 | `bc7de90c3eb9d3dbdbeffb3b47e64e768c4f43eb710e267ec53f97db3427b827` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v2/Http4sBGv2.scala | 2517 | `83689c05f113478e9ebf3e8a884af9286ab11c57f702d5935450f8f05ca373b4` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v2/Http4sBGv2AIS.scala | 9697 | `3107bc140e337c939543c4fbb42208487d0b36f03235153561691579b1a8d0d9` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v2/Http4sBGv2PIIS.scala | 3139 | `95025751bcd3e3c4b6d762bad34a5ec384c3bd210228907860d3db984096b78a` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v2/Http4sBGv2PIS.scala | 14023 | `5c44f176f699b7614d1a09c8811e00497c8c9a316b24f3bbae02607b93226ce0` | 0 |
| obp-api/src/main/scala/code/api/berlin/group/v2/JSONFactory_BERLIN_GROUP_v2.scala | 17132 | `9650a043f5e73ba0813f82017dac2181f208db255f91b2a0cbcd4603cc46cead` | 0 |
| obp-api/src/main/scala/code/api/cache/Caching.scala | 10454 | `34811fd527dced65ff83ed20ccae27daeb20cbccd2130d0519ffaf83db449c18` | 0 |
| obp-api/src/main/scala/code/api/cache/InMemory.scala | 3719 | `57ef45e5f2f274782741847e9807a809abbdb32c8d2fee4924f0a63a863804f3` | 0 |
| obp-api/src/main/scala/code/api/cache/Redis.scala | 25411 | `e44a74a8d7d45fc2539fc0464d651a7155e77d7544741221e28477e832504b9e` | 0 |
| obp-api/src/main/scala/code/api/cache/RedisLogger.scala | 15927 | `cad9aa44f9aab27705e346ce44f653354a18a99cedd19f1d2b33cb52c7ca0597` | 0 |
| obp-api/src/main/scala/code/api/cache/RedisMessaging.scala | 10424 | `1c748e5c0732c5a369ce642e7a57a4355e5888169a4209db5c6f0bb8213ea805` | 0 |
| obp-api/src/main/scala/code/api/constant/constant.scala | 51817 | `42e9c2bd56bda12d657ca286777f1f371e536d0db5cff70bf8400e381609d599` | 0 |
| obp-api/src/main/scala/code/api/dauth.scala | 9270 | `ff9a18687a34be5afe740f422314a999433a0c1144c12155044ab1520012a85b` | 0 |
| obp-api/src/main/scala/code/api/directlogin.scala | 23835 | `e28207774a62e6219675b2edd3a8778aea7014e9327148afb8c32ebc984d0b41` | 0 |
| obp-api/src/main/scala/code/api/dynamic/domainapi/DomainApiPaths.scala | 17348 | `f506bed396a808cf353db38cd91e16a3912c4315ad9fdcabdf479238dfe6b070` | 0 |
| obp-api/src/main/scala/code/api/dynamic/domainapi/Http4sDomainApi.scala | 8558 | `8d4c612076ad15edb2287079c24778caad6d30820ff5113391785f109b308580` | 0 |
| obp-api/src/main/scala/code/api/dynamic/endpoint/APIMethodsDynamicEndpoint.scala | 16182 | `2ab1f9b51a93c1239fe51f2b3164adb323751bb2ef83b47374ed87cda6b7f388` | 0 |
| obp-api/src/main/scala/code/api/dynamic/endpoint/Http4sDynamicEndpoint.scala | 9510 | `53a8407f8dd01277e2a4a0f5856ed70ccfb451938d54efbdc152a5e0d0ce864d` | 0 |
| obp-api/src/main/scala/code/api/dynamic/endpoint/OBPAPIDynamicEndpoint.scala | 2680 | `2791fe998c21d24793feb594fa50d229f05f5cb03ed6be10314ec527c8684d7b` | 0 |
| obp-api/src/main/scala/code/api/dynamic/endpoint/helper/DynamicCompileEndpoint.scala | 4294 | `61cb39b6c0b701c976a45fa9c336764621956afeea8cb9d232680e0b1515cc1c` | 0 |
| obp-api/src/main/scala/code/api/dynamic/endpoint/helper/DynamicEndpointHelper.scala | 45767 | `f73e374f1437cc217822d4ec468b2336b62f419d7956b84724f73995423ae229` | 0 |
| obp-api/src/main/scala/code/api/dynamic/endpoint/helper/DynamicEndpoints.scala | 22050 | `2636fc2e2cc1db18eb7dd816b8fc438a3bf16d0a7cdc058810862d36ebfcab15` | 0 |
| obp-api/src/main/scala/code/api/dynamic/endpoint/helper/DynamicQueryEndpoint.scala | 3129 | `6f3c1d1a3064f2678967e5bb47bc4e3d4a9d47caa48a79be9e598c55fea4ef13` | 0 |
| obp-api/src/main/scala/code/api/dynamic/endpoint/helper/DynamicResourceDocsEndpointGroup.scala | 7784 | `c881a3f52d3476b16906972f28d7ced953b34c18fc84620e7f98f54f8d7ce80d` | 0 |
| obp-api/src/main/scala/code/api/dynamic/endpoint/helper/practise/DynamicEndpointCodeGenerator.scala | 7083 | `a5ffb21ec1a5d0c657b23934bd7aede03a85d89ffc66cf13f812efc4e405e0cc` | 0 |
| obp-api/src/main/scala/code/api/dynamic/endpoint/helper/practise/PractiseEndpoint.scala | 4212 | `229e8aa2b93632e550e7201b3a6efb8a565d21a511416043cff8bf9e219ef0a2` | 0 |
| obp-api/src/main/scala/code/api/dynamic/endpoint/helper/practise/PractiseEndpointGroup.scala | 2485 | `9e94f2e32cc6b28f3804d866073d934d847820714293bea526b749b779f81c6a` | 0 |
| obp-api/src/main/scala/code/api/dynamic/entity/APIMethodsDynamicEntity.scala | 3185 | `52dcb74d6468ef6d65b0cb3ca4edbd7268997f76c2d0614445f15429f0381443` | 0 |
| obp-api/src/main/scala/code/api/dynamic/entity/Http4sDynamicEntity.scala | 67981 | `d5a4c56d99b4d5912eca1abdcbf2192ab139b219b9f07aead4340f04d9749a94` | 0 |
| obp-api/src/main/scala/code/api/dynamic/entity/OBPAPIDynamicEntity.scala | 3097 | `8d90def0fe02131e998b801789c207661eacbc0d54894db0869183057cc3d88b` | 0 |
| obp-api/src/main/scala/code/api/dynamic/entity/helper/DefinitionsMapCache.scala | 2485 | `bd4e7d452458c3a8c3b6e2eea94a1d167c86f67def2e97c07809fcf71a368c71` | 0 |
| obp-api/src/main/scala/code/api/dynamic/entity/helper/DynamicEntityHelper.scala | 72254 | `5444a40280ff209a5ebff773ebc7e48c127f8a28984bc476a1d6fc469fb18d85` | 0 |
| obp-api/src/main/scala/code/api/dynamic/entity/helper/DynamicEntitySpace.scala | 3558 | `940fb610fee902829505865dda626819a91d08c5f05d503ebe605a60d56eefb0` | 0 |
| obp-api/src/main/scala/code/api/dynamic/entity/projection/DynamicEntityIndex.scala | 3029 | `694583aabdd9951cd91d71d98a3552461faf1dbb83581c3774ea8e51f9014178` | 0 |
| obp-api/src/main/scala/code/api/dynamic/entity/projection/IndexingCapabilities.scala | 2812 | `695c48af5aff920991694aeb776f6878ec9915b707bb8dee73b5465266bec8da` | 0 |
| obp-api/src/main/scala/code/api/dynamic/entity/projection/PostgresProjectionBackend.scala | 10141 | `acf309b397e6c1687e3b25dfdfa60e7425c291131c19045260b66241eefc9d0e` | 0 |
| obp-api/src/main/scala/code/api/dynamic/entity/projection/ProjectionCoerce.scala | 2472 | `35d99c8f4bf4b01398d7abe8fec81b8ab419952ef00c5039f8bf2e9da6bf491a` | 0 |
| obp-api/src/main/scala/code/api/dynamic/entity/projection/ProjectionDDL.scala | 3686 | `80a542a45c54f8637b780a698cdc902ab892d2a5ea6faaac021a4df25f21b27a` | 0 |
| obp-api/src/main/scala/code/api/dynamic/entity/projection/ProjectionDb.scala | 1904 | `87236d5913ddd17e02094a13e6a84e3dcf030b941372ecbd7bf2e27502ca17ab` | 0 |
| obp-api/src/main/scala/code/api/dynamic/entity/projection/ProjectionDualWrite.scala | 3207 | `e285b3184cf40e733fa0b6436ccdc9f4b78be057c3b3a011db55a76d652423b8` | 0 |
| obp-api/src/main/scala/code/api/dynamic/entity/projection/ProjectionNaming.scala | 2628 | `1362dd4d3b48b42a980490c7a472023ddd105cf3b6cc3be7ca833689d5569d5c` | 0 |
| obp-api/src/main/scala/code/api/dynamic/entity/projection/ProjectionProvisioner.scala | 5894 | `834ce7358ff558561677d9347c716bf1f370ad6a21e5f404858ebbbd20c28ea3` | 0 |
| obp-api/src/main/scala/code/api/dynamic/entity/projection/ProjectionReadiness.scala | 2181 | `e975dfe169c60b33a99859c65f7e2f80ecc547ea157bfead6ad7a3b151af921a` | 0 |
| obp-api/src/main/scala/code/api/dynamic/entity/projection/ProjectionSql.scala | 5248 | `4c79d4875e611c9c3258050352c2fda07ea550735f972291448136e288abe9ad` | 0 |
| obp-api/src/main/scala/code/api/dynamic/entity/projection/ProjectionStore.scala | 7965 | `4e5646739db3a30bbff626a6bacbf4dad96bdc83b9eea9fc40ebcfbe5ddb4fd1` | 0 |
| obp-api/src/main/scala/code/api/dynamic/entity/query/DynamicEntityQueryBackend.scala | 2330 | `d3c835c6a54752295c28e15ad8b74295fa682d3647fea20d119e330f62270fa5` | 0 |
| obp-api/src/main/scala/code/api/dynamic/entity/query/DynamicQuery.scala | 32478 | `4008f533d80c336b863f7deb8fd605ad15bddb9c727da00ec813a88d4bdaae93` | 0 |
| obp-api/src/main/scala/code/api/dynamic/entity/query/InMemoryQueryExecutor.scala | 7488 | `339c7f1bee8296d0bc7b999349828c559387954d2e6aca203e03832932724ac6` | 0 |
| obp-api/src/main/scala/code/api/dynamic/entity/query/JoinPlanner.scala | 21714 | `064ce2bea5181389ec17d88fec898dad8a3df685deb37db12d13d23a3bf37af2` | 0 |
| obp-api/src/main/scala/code/api/dynamic/entity/query/OperatorMatrix.scala | 3208 | `68b21c92fe8e7f4b819a71b4ccbbb4b8fbd8c9d43bcab0b6840e0f57831b2dd5` | 0 |
| obp-api/src/main/scala/code/api/dynamic/entity/query/QueryModel.scala | 5644 | `53d28fc1d49e534567a7639043caaa4cf8f64f6e318c454bb6d7068b448b785d` | 0 |
| obp-api/src/main/scala/code/api/dynamic/entity/query/QueryParamParser.scala | 8883 | `f87371e51f1e98ba7635eaa2268727b4a8a7960bdf454a7b9c3a5fcccc0c21c3` | 0 |
| obp-api/src/main/scala/code/api/dynamic/entity/query/QueryPlanner.scala | 12555 | `aaa85a54c62ece4cea3ebac946611bdaa8bc28070440e3e520734adf8d06f986` | 0 |
| obp-api/src/main/scala/code/api/dynamic/entity/query/RecordJoiner.scala | 10886 | `339a4f98039f42566505ff414f0d1c567bc9b79b8798efd857693bda821eeeb2` | 0 |
| obp-api/src/main/scala/code/api/pemusage/MappedPemUsage.scala | 1664 | `c8a9387f01c9a14beda2cff2cdf89117574379ec6a1cd6332bb8292f1b8f4cd7` | 0 |
| obp-api/src/main/scala/code/api/pemusage/PemUsage.scala | 1255 | `924ab77a2ddde155e5d0cd9124065fb80d9f02fcc5704d33d60f861eb65955cd` | 0 |
| obp-api/src/main/scala/code/api/siwe.scala | 12031 | `7f364070e1272dad20e187988357913438853fad854d04b3e26dc3f7e45c4c54` | 0 |
| obp-api/src/main/scala/code/api/util/APIUtil.scala | 255158 | `9f72af18e127d466e59f885c05c499adc86cfd8837424ccaa488280e43fee523` | 3 |
| obp-api/src/main/scala/code/api/util/AfterApiAuth.scala | 9733 | `d3ee97430fc0d36d5e653e39692710f86cc4e12ce660af325c5a2c7ffefe4fb0` | 0 |
| obp-api/src/main/scala/code/api/util/ApiPropsWithAlias.scala | 6343 | `bc5e0d2ac9035840b9e41c9c60f675e2b9da87050fb9cc59ba9c7cb532fc4222` | 0 |
| obp-api/src/main/scala/code/api/util/ApiRole.scala | 91892 | `77a6048d0984c438328ad9b0769b4d6985044c1882a17fc790c5d2c5dac3081a` | 0 |
| obp-api/src/main/scala/code/api/util/ApiSession.scala | 25773 | `f7b746c6a404dd57013c3c38af79af9e79ff372bef8c93cd9066b85f1ed1dc95` | 0 |
| obp-api/src/main/scala/code/api/util/ApiTag.scala | 11098 | `213cf091abaad681ce718a74f47198157496a87e497050a041392a2c53c60abe` | 0 |
| obp-api/src/main/scala/code/api/util/ApiTrigger.scala | 2022 | `2fbc54380f7913ce6c49191983a75028e0f43e2b06510c5d9c577c284c133478` | 0 |
| obp-api/src/main/scala/code/api/util/ApiVersionUtils.scala | 3826 | `5fa0e5101170ff5546d2ee50b00ca6afe5a85d4939b33c33ab56fd562934da08` | 0 |
| obp-api/src/main/scala/code/api/util/ApiWarnings.scala | 2368 | `718847bd724da01d71d6de4967125bbe54ca4d90df31eb74d50a1173cb5e0aae` | 0 |
| obp-api/src/main/scala/code/api/util/AttributeTypeDocs.scala | 3380 | `d35efaefb11aefca0063190b3a33634422fb1578784e42ceb2934128e0c5527a` | 0 |
| obp-api/src/main/scala/code/api/util/AuthHeaderParser.scala | 3753 | `625b93174ac031e8d660bc6f32bffe6b336aecbb663f66e3d17b3710cf6fd546` | 0 |
| obp-api/src/main/scala/code/api/util/AuthRateLimiter.scala | 6188 | `4f3ef8cbd8e04b332ac82781f9825c2e935ec22e2da9b81fb238346f0c2ad433` | 0 |
| obp-api/src/main/scala/code/api/util/AuthorisationUtil.scala | 1237 | `15a5983e320d8c02f0964d7e19fef1d7c928cab87ba9f6fc5fe5e9d395c96be1` | 0 |
| obp-api/src/main/scala/code/api/util/BerlinGroupCheck.scala | 14884 | `b1b3ae2300b80a684f1cda4defbd9ae6f4cba3a4475e640f86b8b68f8e80250b` | 0 |
| obp-api/src/main/scala/code/api/util/BerlinGroupError.scala | 15091 | `150480b77b87c77fe0636743907c56c488494f975fd7965cf438c4a397a819c6` | 0 |
| obp-api/src/main/scala/code/api/util/BerlinGroupSignatureHeaderParser.scala | 5209 | `d136cabc8695d5dcf8c90076abbb826c0bff3889f02d0eb7196b1801f3bb2155` | 0 |
| obp-api/src/main/scala/code/api/util/BerlinGroupSigning.scala | 22133 | `735211d144848843dd33c72b6fff40e9e251cde69af7408835d7c51f03dc926d` | 0 |
| obp-api/src/main/scala/code/api/util/BlockingIoExecutionContext.scala | 1887 | `f5e5411b9323b56f83394560ea00bee1b07c0c328814088bb68ad0348bf7a605` | 0 |
| obp-api/src/main/scala/code/api/util/CertificateUtil.scala | 15668 | `b51a5a90b224e387aa71b2e69f7fcd73903a5a3ee446fa9d05506c9981d8dc9a` | 2 |
| obp-api/src/main/scala/code/api/util/CertificateVerifier.scala | 6798 | `570ef050cdcd3582a7cbce1e8617c6d741b8d789fd1b4d21e828ee6a24f61fe2` | 0 |
| obp-api/src/main/scala/code/api/util/CodeGenerateUtils.scala | 14267 | `1ebb7c2296474d49c1eafeb72a4b34695cee0be51fb15ed641594fb0a0c05823` | 0 |
| obp-api/src/main/scala/code/api/util/CommonFunctions.scala | 2626 | `dbb999f8e45a6acfe893abce576130eee8fd5c560eec3b2a1a911d44335b88c6` | 0 |
| obp-api/src/main/scala/code/api/util/CommonUtil.scala | 1472 | `f0165730fd59cf11a412f046d9591cb1270c985a2257817a3c53b4c953c37bd4` | 0 |
| obp-api/src/main/scala/code/api/util/CommonsEmailWrapper.scala | 14657 | `bd0d967630b6caa396a44184672b42ca35569f213771dc16b12b17c34d2e4601` | 0 |
| obp-api/src/main/scala/code/api/util/ConsentUtil.scala | 157781 | `c58958d57aa16c7233070ce30c5a1c822da48ef54821d639b679af4655b065f2` | 0 |
| obp-api/src/main/scala/code/api/util/CurrencyUtil.scala | 1949 | `827582ed90a468b1261a8693e43b9a34bd290aa6eda4d3b0a7371497418949d5` | 0 |
| obp-api/src/main/scala/code/api/util/CustomJsonFormats.scala | 7310 | `80c0a9cd42aa6785430a8050a71846921ab39509ba8d4bde7b587bd39eb880bd` | 0 |
| obp-api/src/main/scala/code/api/util/DBUtil.scala | 5842 | `f91153c220fc19a21ffa6744a732ecd031896147093c67461986ac7dda5a3a7f` | 1 |
| obp-api/src/main/scala/code/api/util/DateTimeUtil.scala | 2597 | `a57030a3a01986529ea6c9fce098e98bb8ec1c49a8cb59f0dcd7cd20eaf86167` | 0 |
| obp-api/src/main/scala/code/api/util/DeploymentChecks.scala | 16621 | `9da3f2d1a0dad0d6fec4c38f71adf2f7798e586efd6f55d874d700c6841982e7` | 0 |
| obp-api/src/main/scala/code/api/util/DiagnosticDynamicEntityCheck.scala | 13391 | `2962f4642bc7d3963daa4006a49c716c96fa07c8bf8d832a25d669c3630df260` | 0 |
| obp-api/src/main/scala/code/api/util/DoobieAccountAccessViewQueries.scala | 4651 | `4474e20fdce8dbefbe242889ec905524b69bd6538e17cd01a6172670617ecc13` | 0 |
| obp-api/src/main/scala/code/api/util/DoobieQueries.scala | 5117 | `365b362da7099b2713034c08ee39e1e05dd7af3b70fac3ee110b7f1fb4732dee` | 0 |
| obp-api/src/main/scala/code/api/util/DoobieTransactor.scala | 9852 | `690737646f9dae623d582bf4cd76482f5d14f157aa72b006cbce29c4a1ba8f2f` | 0 |
| obp-api/src/main/scala/code/api/util/DynamicUtil.scala | 52699 | `020e421aa7b1971483bb38432f909b88dd78c39fbc25eb6087b73d51913f1f8f` | 0 |
| obp-api/src/main/scala/code/api/util/ErrorMessages.scala | 114200 | `941a1564c39a2fcaea074e7e09966cddc4a77f155375536ed975c6473cacddeb` | 0 |
| obp-api/src/main/scala/code/api/util/ErrorUtil.scala | 2234 | `9631c1792f156fef96eba6c5a65988de7887bb178047be073d91696582c1860d` | 0 |
| obp-api/src/main/scala/code/api/util/ExampleValue.scala | 167210 | `5ffd33ba9cfff12499c29db9b33d417d4bf1400242ccfa038dfea9cd3e806494` | 0 |
| obp-api/src/main/scala/code/api/util/FutureUtil.scala | 4983 | `e596b7550d57c9c3d3453fa8f4b6ebc1fe325767a79aa17984e2d763f3588341` | 0 |
| obp-api/src/main/scala/code/api/util/Glossary.scala | 434752 | `c87f92b4dbd6585ffb6da5d6726bc0f4fd00403f86c0d551b03057dc5854b838` | 36 |
| obp-api/src/main/scala/code/api/util/HashUtil.scala | 2058 | `8ba13389d9c6241895d43734802909810ade1d99f63212ee018f12845eaa133d` | 0 |
| obp-api/src/main/scala/code/api/util/I18NUtil.scala | 3104 | `cf8558feddff24bf6c3e5504470476cbe2dff1c065825c74116b7a8f6ba27e85` | 0 |
| obp-api/src/main/scala/code/api/util/IpPenalties.scala | 8457 | `f2875db194f8ab9051e3513b1ac9a9f0cd70b88cd0d557a5a900100c13df1497` | 0 |
| obp-api/src/main/scala/code/api/util/JsonSchemaGenerator.scala | 13077 | `ef352f1a86e098fdf7c5f4c3edcbb606369bcd23b8bb4a2ca85991632ecd9136` | 0 |
| obp-api/src/main/scala/code/api/util/JwsUtil.scala | 14065 | `bc75d8ade88fafba445912327358cd739314c5033d7d15fd9c29de6d4a6a35a4` | 0 |
| obp-api/src/main/scala/code/api/util/JwtUtil.scala | 14132 | `b789b486917e9004004072be302ea67ba6fe914192b29bb988037d6f1ee96aa5` | 4 |
| obp-api/src/main/scala/code/api/util/KeycloakAdmin.scala | 4503 | `761638d283abab6eccd7d95d4efce1680aa08a960cc7f9a148114824622ee306` | 0 |
| obp-api/src/main/scala/code/api/util/KeycloakFederatedUserReference.scala | 2474 | `7b2b30373ea60774e7a4d009d064937eb293c5a11fdb708e3dcc3f4304923c23` | 0 |
| obp-api/src/main/scala/code/api/util/NewStyle.scala | 257665 | `42c988b93f1891bb9c13049ceb2af184fca119e885a12066785a06b939431887` | 0 |
| obp-api/src/main/scala/code/api/util/NotificationUtil.scala | 3414 | `76d7c3699f4152e26d5143c7163df544c7d11bfaa21acab35fe2620284be42f2` | 0 |
| obp-api/src/main/scala/code/api/util/OBPParam.scala | 8376 | `be4acd7cedbcf964d27e5a3f0f0953a5bf7e2b60895e92d829997442b1296574` | 0 |
| obp-api/src/main/scala/code/api/util/P12StoreUtil.scala | 3778 | `d3666e12a9474c2019fb4e840fb4e8aabaf24fb2837c564658107fc056a1e17c` | 0 |
| obp-api/src/main/scala/code/api/util/PasswordUtil.scala | 1349 | `90cc0b3742c3ca6e521ab3e59106723b94cb5f0e894d2ca22e65f2ff1f214b6a` | 0 |
| obp-api/src/main/scala/code/api/util/PeerTrust.scala | 12710 | `fb803ec692255397100bd9f360f5f18ab573ea7c6cacb8c432b440386b0e53e8` | 0 |
| obp-api/src/main/scala/code/api/util/PegdownOptions.scala | 5321 | `24e9d9f3faec90b1221b3af8967cbbef33cc56b483eeb99538be9dde85d450ea` | 0 |
| obp-api/src/main/scala/code/api/util/RSAUtil.scala | 5175 | `6a54aa33f128bfebcc0c1bf151e287449fd2320ce6f78cc4c92837288d56584a` | 1 |
| obp-api/src/main/scala/code/api/util/RateLimitingUtil.scala | 26439 | `e5ae261756395587404204bc593f0c45a3af485598bfbceef26cd86a2f56d1f6` | 0 |
| obp-api/src/main/scala/code/api/util/RedirectUrlValidation.scala | 8711 | `8466d8446d41e48a9a1d9c13c4b4dd66055f270a7e150576f94f341996c7e0b2` | 0 |
| obp-api/src/main/scala/code/api/util/RemoteIpUtil.scala | 10030 | `32ec9460ec635d6073cef4ffeb5fa9fd090610d46399c217d2d4b52d0cd6f187` | 0 |
| obp-api/src/main/scala/code/api/util/RequestHeadersUtil.scala | 3687 | `3b4718fcec0f0368560402b158d9cf21e3db17c2603dbb651d1998b9192fab66` | 0 |
| obp-api/src/main/scala/code/api/util/ResourceDocFilters.scala | 6923 | `adf3427b1074dcb0a830b5116491c284615f0a8e8898d35a5d7de0a4878b6573` | 0 |
| obp-api/src/main/scala/code/api/util/ResourceDocRegistry.scala | 11428 | `4ff67af926ae5bc0c377577f00e0916fb36f94d099bcd87022e7f500cc00a2d9` | 0 |
| obp-api/src/main/scala/code/api/util/ScannedApis.scala | 2793 | `f1abda0d42311bfcbe98f5e44d5084957dcab375f940e6ffb79720e4769d23d2` | 0 |
| obp-api/src/main/scala/code/api/util/SecureRandomUtil.scala | 2027 | `e782210ad9cc13532db8aeac7c053925b3f4f2d6a3e4407868be6b6b1e37a1cd` | 0 |
| obp-api/src/main/scala/code/api/util/SelfServiceRateLimiter.scala | 14323 | `3ac81e5d09bf27d583f526e59b72351232238621d0cb23332be11fd49a92d3a2` | 0 |
| obp-api/src/main/scala/code/api/util/SelfSignedCertificateUtil.scala | 3293 | `4dfcd06ec75fd07bd70f0946eafae02e31cdd1d8c28f331f3c3aceffac956099` | 0 |
| obp-api/src/main/scala/code/api/util/SortFields.scala | 3117 | `8a9fffd4558f4eb9c4be9e6f311dae480a64afc4e0eb6bf1cc41e8eaee37344a` | 0 |
| obp-api/src/main/scala/code/api/util/SqlServerDateTimeUpgrade.scala | 9088 | `9b5234fbe4ea95292d0c5b1c4c31bd53c7d5669676c7ff1675fe3471f3da262f` | 0 |
| obp-api/src/main/scala/code/api/util/TokenBinding.scala | 6390 | `fb66234dab536e9b9c66bf91a1ddf25b71f33396fd486bb6f4a016024a6a86f5` | 0 |
| obp-api/src/main/scala/code/api/util/WriteMetricUtil.scala | 11393 | `84808344e1453e4c2d36043658e9255a141b6d0f0b5f5d41105f2b0d820c6f70` | 0 |
| obp-api/src/main/scala/code/api/util/X509.scala | 11402 | `64677be6c73ca3610069379182b53f0db21b448e56cfb74ebc8254dc5fb48d5c` | 0 |
| obp-api/src/main/scala/code/api/util/YAMLUtils.scala | 3578 | `119103d1d42d6cf5fe2e61450c96b56561a270f71eb6dd31ffa26082502d98ff` | 0 |
| obp-api/src/main/scala/code/api/util/http4s/AppsPage.scala | 7532 | `3b66be53077800adda6b6436fcfd6ad7e06e4a378d865804c4322c573fb45770` | 0 |
| obp-api/src/main/scala/code/api/util/http4s/CallerCertificate.scala | 3680 | `518f83e3372d4b7048c25b8f699882067090465763d42583474b650a9fc64902` | 0 |
| obp-api/src/main/scala/code/api/util/http4s/ErrorResponseConverter.scala | 10642 | `2b976b2a35915ed5b3fba67e82f47e3eac39c735f235d2dfb1c35a2db5051de4` | 0 |
| obp-api/src/main/scala/code/api/util/http4s/Http4sApp.scala | 13001 | `b2df27d0ca506e950cb664effd988e02bd2e84029ef3a2bdcf1980ebe58abb34` | 0 |
| obp-api/src/main/scala/code/api/util/http4s/Http4sResourceDocAggregation.scala | 11362 | `9a1075338ac88e4e4bbd4c9c186d9a8ecc9c5c0721775d400f1dfae8918bf164` | 0 |
| obp-api/src/main/scala/code/api/util/http4s/Http4sResourceDocs.scala | 44650 | `6b39f9f9a4575d7f81393078bcad6f78eb9d8306fc3f289a0afb6a4d611d319d` | 0 |
| obp-api/src/main/scala/code/api/util/http4s/Http4sStandardHeaders.scala | 3365 | `6f969e0aaae42d6455f235a0ab819b51eee737c7b73ec7a9d25ecd57b61414fa` | 0 |
| obp-api/src/main/scala/code/api/util/http4s/Http4sSupport.scala | 49925 | `4d0e4caa7c26db638c63be2fcd4ba24a2c4d16262a659d29dd7a76b804e18487` | 0 |
| obp-api/src/main/scala/code/api/util/http4s/IdempotencyMiddleware.scala | 19415 | `d46724b13fb4fc1c66438d7d68b2ee03c4ef7fd73cafb2a7fdb2e487aa5af9dc` | 0 |
| obp-api/src/main/scala/code/api/util/http4s/Psd2CertIngress.scala | 3799 | `7ed96f972ec4dc72cf5b6f5000977744949cdf8d6d1fc5753ad336b4a9cfae53` | 0 |
| obp-api/src/main/scala/code/api/util/http4s/RequestScopeConnection.scala | 19773 | `585b7413902699a9505d8a6838862d5f000392543576eefdf49ea64a58b00c5d` | 0 |
| obp-api/src/main/scala/code/api/util/http4s/ResourceDocMiddleware.scala | 41828 | `843ecc2c86f3b67eb31afe955c76e7db5eec8f3320cfedab9209d650e017f852` | 0 |
| obp-api/src/main/scala/code/api/util/http4s/SelfServiceRateLimitMiddleware.scala | 10941 | `d15d794e2c1a9f09b66ecd9e5a927ec0779811f66718b5c5a7bb8dc335ac462a` | 0 |
| obp-api/src/main/scala/code/api/util/http4s/StatusPage.scala | 12066 | `f954f28c7332f3e46bc7d330e9f7874ab2e1cd9e9c398b26a30ed289485a3284` | 0 |
| obp-api/src/main/scala/code/api/util/migration/Migration.scala | 60604 | `f1c8e4d5bc136fe44916ecaf649fc511348dfbfaf8463052d6a260780c83f569` | 0 |
| obp-api/src/main/scala/code/api/util/migration/MigrationInfoOfAccoutHolders.scala | 4111 | `4bc52481a671a1cc4b633ded83089d3ee1d54deb496b910f4439d54011df654b` | 0 |
| obp-api/src/main/scala/code/api/util/migration/MigrationOfAccountAccessAddedConsumerId.scala | 2999 | `e5dedde1ddda74967b60a3b5ccd952197e047513e483189ed18a84bf60de3541` | 0 |
| obp-api/src/main/scala/code/api/util/migration/MigrationOfAccountAccessWithViewsView.scala | 7981 | `d1b8ea52e87eba1a466d0db5376998786d491a6dd59954ec9e8ad7176049a54e` | 0 |
| obp-api/src/main/scala/code/api/util/migration/MigrationOfAccountRoutings.scala | 4244 | `287038e659d6ee3f8935b364fcd5c912f617a114238ed4352314690d1db92f68` | 0 |
| obp-api/src/main/scala/code/api/util/migration/MigrationOfActivityDashboardIndexes.scala | 7598 | `1c3151a7846af104240c74eacf4b6a6b67de6a334ca0c119440a83516c906d1f` | 0 |
| obp-api/src/main/scala/code/api/util/migration/MigrationOfAuthUser.scala | 6647 | `e0493ed120121acd13ec6e82c56e3d8b414d77a0379a3cd60b2069c0fbc1bf48` | 0 |
| obp-api/src/main/scala/code/api/util/migration/MigrationOfChatRoomCreatedByAndLastMessageSender.scala | 4681 | `da83b6999e45493d56fba3f6d5edfbe621ff6b95f7984c3901c88f8b5ffe8a49` | 0 |
| obp-api/src/main/scala/code/api/util/migration/MigrationOfChatRoomIsOpenRoom.scala | 4104 | `f0a2a8f65d9b7bfbaddb09b47421b96d23b7be9330be1992a04b72429dc0a2d2` | 0 |
| obp-api/src/main/scala/code/api/util/migration/MigrationOfConsentAuthContextDropIndex.scala | 2911 | `d7d715f6223506e4d193577cf983d65502d15b38add6d20f098decaa033a2b2b` | 0 |
| obp-api/src/main/scala/code/api/util/migration/MigrationOfConsentJwtPayload.scala | 2358 | `7cb900fbec056591dd93c34f6af4d8d27d97ac9655e5104c07c1dce719286107` | 0 |
| obp-api/src/main/scala/code/api/util/migration/MigrationOfConsentReferenceIdUuid.scala | 10614 | `273e12dec68feb6591a9bc891484ade34ec12bc68c4a6a2b58835e1788ad5838` | 0 |
| obp-api/src/main/scala/code/api/util/migration/MigrationOfConsentRequestConsumerIdFieldLength.scala | 2777 | `8341bcde11b0bbb96c710e75b21a6333bcf1531a6b6d4280d3548a9d3a51f3de` | 0 |
| obp-api/src/main/scala/code/api/util/migration/MigrationOfConsentView.scala | 5431 | `5f51e9e766966f0b4a72ac14ad030d19c15acee2eee9c3bea54c116d63ee36b5` | 0 |
| obp-api/src/main/scala/code/api/util/migration/MigrationOfConsumer.scala | 6201 | `666d1bc058927fa45cf9e68e7c86820d06f7754004bcdb093e51cc6d1b95a94e` | 0 |
| obp-api/src/main/scala/code/api/util/migration/MigrationOfConsumerRateLimiting.scala | 3638 | `77c9a5b31b79e803aeb3eee6fc25be6279faae41272646e8f1998b77cf7fde7f` | 0 |
| obp-api/src/main/scala/code/api/util/migration/MigrationOfCounterpartyLimitFieldType.scala | 3800 | `6e6a88058eefb57bbe07e5f952d9577a9b8082ee2c2fa67c15c30db645eb1195` | 0 |
| obp-api/src/main/scala/code/api/util/migration/MigrationOfCurrencyCodesUpperCase.scala | 12256 | `9aff5cd6ec9a54bb1388ae2d4c8d95d5e3ee61be1a64d510f01fb7e9ff72f66e` | 0 |
| obp-api/src/main/scala/code/api/util/migration/MigrationOfCustomerAttributes.scala | 4784 | `c7fc6ff4e9d8b0d4c492acfeeff5d060b80c95fafed7360012f623cb1bdf350c` | 0 |
| obp-api/src/main/scala/code/api/util/migration/MigrationOfCustomerRoleNames.scala | 7430 | `a86b81cbe0cc53e6f5ab9a9a5d7b8a5d931f092c5bd94773cb8ee4ffbf543e95` | 0 |
| obp-api/src/main/scala/code/api/util/migration/MigrationOfDropFastFireHoseViews.scala | 3161 | `5f4e17f6365d816cd38d4b2585d45b30943a35085fd041832692f5759dafd690` | 0 |
| obp-api/src/main/scala/code/api/util/migration/MigrationOfDynamicDataIdFieldLength.scala | 5042 | `a260bd9358d4dd250d2f5e2f89180095b83ceccc3bbb8ca09bdbc6bda5b3d1d4` | 0 |
| obp-api/src/main/scala/code/api/util/migration/MigrationOfDynamicEntityRoleNames.scala | 13181 | `862f1c13856599f5e546e94cb1bd94a915b658ea1951e96f0a9a240525618e7d` | 0 |
| obp-api/src/main/scala/code/api/util/migration/MigrationOfDynamicResourceDocBodyFieldsLength.scala | 3662 | `88d5da9c9ecf244ee72742f36bc7540e5562745364e5f87939b7b0d7aa827848` | 0 |
| obp-api/src/main/scala/code/api/util/migration/MigrationOfDynamicResourceDocTextFieldsLength.scala | 4173 | `14e51ab8e96d918e0df0eaed5ad94173c1da9489d2ac7520e7e52f49918ed7aa` | 0 |
| obp-api/src/main/scala/code/api/util/migration/MigrationOfFastFireHoseMaterializedView.scala | 5670 | `6220cc23185d2b06fd0190966927f0cadd68adaa27d645ed60be56054eb0bd7c` | 0 |
| obp-api/src/main/scala/code/api/util/migration/MigrationOfFastFireHoseView.scala | 5509 | `b2392bbbcfd94a23e55f3da61239ba2cc83edd715948a512908c8781a0364784` | 0 |
| obp-api/src/main/scala/code/api/util/migration/MigrationOfMappedBadLoginAttemptDropIndex.scala | 2827 | `225cb42fefe0dbc07a4b1163b1701f41fcb81e0b5b1e2d9e104f94e3b58581b4` | 0 |
| obp-api/src/main/scala/code/api/util/migration/MigrationOfMappedConsent.scala | 7835 | `83937c5cb5a515c5cb550c769a7d8df6d8d60a79079d6e71430c5bd73aa9dc54` | 0 |
| obp-api/src/main/scala/code/api/util/migration/MigrationOfMappedCounterpartyDescriptionLength.scala | 3106 | `0c26673a70ee39bd7c989702a7de8ac2c773c8a377bdea7cd16646b31062b018` | 0 |
| obp-api/src/main/scala/code/api/util/migration/MigrationOfMappedExpectedChallengeAnswerFieldLength.scala | 3176 | `ced92cbc8f53b0d526cb36afe5fad5b3cc1097b5778dc1fc52fbd18ba2d24276` | 0 |
| obp-api/src/main/scala/code/api/util/migration/MigrationOfMappedTransactionRequestFieldsLength.scala | 4208 | `ca8bb1582fd4f6a8175dfa2cdf10fcac86103297deaf58f6d9edce34f2e4f1db` | 0 |
| obp-api/src/main/scala/code/api/util/migration/MigrationOfMappedUserAuthContext.scala | 3004 | `2ba60d3835d4a9854a4eaeec3992ef381a921d3fe7e5b05006271d4f6bcc58e9` | 0 |
| obp-api/src/main/scala/code/api/util/migration/MigrationOfMappedUserAuthContextUpdate.scala | 3233 | `ca81b81e9f6e96a3efcfd2ac6041bc98b424f165404dbf979ecfcdeffc2d5b87` | 0 |
| obp-api/src/main/scala/code/api/util/migration/MigrationOfMetricArchiveTable.scala | 3995 | `8da9c2741e8803aaee7c111537fcbe56a4eecf8b6e474000061a4df7d1f35685` | 0 |
| obp-api/src/main/scala/code/api/util/migration/MigrationOfMetricAuthType.scala | 4096 | `2135e1fd19b75475d66881c4b20704106f778b788651e906f857acf3f8df70e9` | 0 |
| obp-api/src/main/scala/code/api/util/migration/MigrationOfMetricCertificateTrust.scala | 5296 | `0477806a013b50369a9279a16b31b246bec51c7601fe0d8d10ae82ec8ab72540` | 0 |
| obp-api/src/main/scala/code/api/util/migration/MigrationOfMetricConsentReferenceId.scala | 6223 | `557abbc09ca08a119b0a5ef2f4f00f6e8b12eb007940c029d8cf188b1a54d9b5` | 0 |
| obp-api/src/main/scala/code/api/util/migration/MigrationOfMetricConsumerIdFieldLength.scala | 7277 | `0fdd4b7b2bc8795729f2f23202f889e54f52535ca4f35cc230a5c5bca682f38e` | 0 |
| obp-api/src/main/scala/code/api/util/migration/MigrationOfMetricTable.scala | 5168 | `c4dd8cc8f15794ea825ef227027b5fcfe44c4867c5c3e659552e87e383e5cce1` | 0 |
| obp-api/src/main/scala/code/api/util/migration/MigrationOfMetricView.scala | 5132 | `9b5778a3f3697c4e3903eec0128f332260fa1b22d8c01c6ca95e163f28c89031` | 0 |
| obp-api/src/main/scala/code/api/util/migration/MigrationOfOpnIDConnectToken.scala | 4825 | `36ecdfc6177df2da1d426f3ecfbc0c29870c8f66bc7e229e29ca6e7d157b42d3` | 0 |
| obp-api/src/main/scala/code/api/util/migration/MigrationOfProductAttribute.scala | 2818 | `57b27a06f2ff5cfa8a3a7cf474a746256b1d8ae9bfc35018f2f5e3ec8aea5c75` | 0 |
| obp-api/src/main/scala/code/api/util/migration/MigrationOfProductFee.scala | 3070 | `23fc9db709aa81e9466ceaa540bf6fc5e1277b5090d4445f42e59167c425b11d` | 0 |
| obp-api/src/main/scala/code/api/util/migration/MigrationOfResourceUser.scala | 5094 | `2171f93b43c1c376f42a15c97250765b00603bf309ba6a90fe5341df19030ca2` | 0 |
| obp-api/src/main/scala/code/api/util/migration/MigrationOfResourceUserIsDeleted.scala | 4366 | `b1c70810cce7866a10d0a8837ebfbb41a67ba621df8032011c9bd13803e3661d` | 0 |
| obp-api/src/main/scala/code/api/util/migration/MigrationOfRoleNameFieldLength.scala | 5764 | `0553e29ad3b391a62d17d8103d1309c542e54d6ade88efe1d9c043707bf6c73b` | 0 |
| obp-api/src/main/scala/code/api/util/migration/MigrationOfSettlementAccounts.scala | 4410 | `64774eabd680b9afd35c69bbadaf8d896046a9f83fd0dfdb863f1ab6cb91fbcc` | 0 |
| obp-api/src/main/scala/code/api/util/migration/MigrationOfSystemViewsToCustomViews.scala | 4068 | `9b86414c61afd378a3b46ee8e12c86ca98e6537f2f17bdb475a531c0d6d8206f` | 0 |
| obp-api/src/main/scala/code/api/util/migration/MigrationOfTransactionRequerst.scala | 3022 | `e7974ecf6554e39a28893fe9b2174431a8470cfa1371af29d9f53e02c4f7a13e` | 0 |
| obp-api/src/main/scala/code/api/util/migration/MigrationOfTransactionRequestAttributeValueType.scala | 3012 | `73e8b8e23e2ace0c5b58a99b764291a8fb393c90e5294cf464f67b81194fcf53` | 0 |
| obp-api/src/main/scala/code/api/util/migration/MigrationOfTransactionRequestChallengeChallengeTypeLength.scala | 3118 | `35c32e22ceb54cc1c5d1a6ef94120e3b3aa722f6edc046bb315954b2f7a32e18` | 0 |
| obp-api/src/main/scala/code/api/util/migration/MigrationOfUserAttributeNameFieldLength.scala | 3086 | `5f8156ba9d25d2964d7bf69d8cb0fb69b72814693461b466929e092fcea46d81` | 0 |
| obp-api/src/main/scala/code/api/util/migration/MigrationOfUserAuthContext.scala | 3188 | `bac388e52ebef52c38957b632eb5f1ec6e03b169c4544fed33b37b502134c129` | 0 |
| obp-api/src/main/scala/code/api/util/migration/MigrationOfUserAuthContextFieldLength.scala | 3684 | `d3d42ecec74afc2cf720add79fb2bad9e6db0b0bdf8a2dba298e0edd2cf69110` | 0 |
| obp-api/src/main/scala/code/api/util/migration/MigrationOfUserIdIndexes.scala | 7123 | `2d047b2e9a29c2e943c2c0d3818a74c8698d05298284b97404ef250f64b83850` | 0 |
| obp-api/src/main/scala/code/api/util/migration/MigrationOfWebhookUrlFieldLength.scala | 3965 | `a2572603dd80ef4ae3ce71a1a3a5cb87bb056bfdf8ff666d4bae64fea9472874` | 0 |
| obp-api/src/main/scala/code/api/util/newstyle/AttributeDocumentation.scala | 3395 | `222d3a5c76cf8fa25bdd3107997ed155e4ebd073ccca5091964d3cd38381ade2` | 0 |
| obp-api/src/main/scala/code/api/util/newstyle/BalanceNewStyle.scala | 3808 | `3039fe29a5ab9a03dc5ffeab9fdda8765f2da306d9e644847c504118fbd463e6` | 0 |
| obp-api/src/main/scala/code/api/util/newstyle/BankAccountBalanceNewStyle.scala | 3543 | `70f9b45931d405d4ca3fc3bb7fd0f75fd78de72f8ab972958d5f8b49d9ca1370` | 0 |
| obp-api/src/main/scala/code/api/util/newstyle/Consumer.scala | 2459 | `c9927605e4df7d0448e51a4fb8663565549a33fecb14cc688bf50edfb6dbf7ae` | 0 |
| obp-api/src/main/scala/code/api/util/newstyle/CounterpartyAttribute.scala | 3918 | `ac1d5fbbe2cf9b8b7cfb9c184a6b6bae02b3a5efb5504c50f0febbcb0e9a959c` | 0 |
| obp-api/src/main/scala/code/api/util/newstyle/RegulatedEntity.scala | 4416 | `8637dcbe0b9a4c4379c332c87a62d6d46ea4a7675c419874811d925e66a183b4` | 0 |
| obp-api/src/main/scala/code/api/util/newstyle/RegulatedEntityAttribute.scala | 4076 | `6660ea2c7906f71daa72cd1d03ecace3d1e766883e78b4780862d635a1ac2692` | 0 |
| obp-api/src/main/scala/code/api/util/newstyle/SigningBasketNewStyle.scala | 3559 | `9985f097c97acedaeafd8478d0a930ca246f533f4d62c755040f72f6c0659c68` | 0 |
| obp-api/src/main/scala/code/api/util/newstyle/UserCustomerLinkNewStyle.scala | 2180 | `00f9f4a33088167bb72c48f72b577aa0c6f9df9f0f401effe51894de135524b6` | 0 |
| obp-api/src/main/scala/code/api/util/newstyle/ViewNewStyle.scala | 11510 | `5a5704f92370d1dfa2d0fe00af80a8b46cab9b172c0c5ef0679229fc39d3e390` | 0 |
| obp-api/src/main/scala/code/api/util/poc/storedprocedure/CallingStoredProcedureReturningResultSet.scala | 2459 | `6bf1617ef1dd2acf5be50aafbf38c7397d3f780f84b0a3cb846b57bed8d2d0c6` | 0 |
| obp-api/src/main/scala/code/api/util/poc/storedprocedure/PostgreSQLFunctionOutputingSimpleValue.scala | 2706 | `8e620047a208770cf4027d82a2f06c8b83a1892d5a6bbb5ebe05f36f09c992b1` | 0 |
| obp-api/src/main/scala/code/api/v1_2/JSONFactory1.2.scala | 7786 | `659ffc61019b2c4d39b1776ae2d1ba4ad46d69284256cb08b9d64b04dfb6012a` | 0 |
| obp-api/src/main/scala/code/api/v1_2_1/Http4s121.scala | 162112 | `8f34a88a67a2b69e1fa85c2688ca1b5529fe2261bb3263fc6336c1a9fe168e98` | 0 |
| obp-api/src/main/scala/code/api/v1_2_1/JSONFactory1.2.1.scala | 25929 | `d7d3fae030592f845b8fc6c3bae5a940535de17a44527a749929d032743fd869` | 0 |
| obp-api/src/main/scala/code/api/v1_3_0/Http4s130.scala | 7503 | `f4a393989db2a94f89b72c25c0bcdfef416b03106fce5aed158878dc5c9b9ff3` | 0 |
| obp-api/src/main/scala/code/api/v1_3_0/JSONFactory1_3_0.scala | 5483 | `696f89a08889410df58ca21aa399e49dba56e8469141cffa2d46882418d2c399` | 0 |
| obp-api/src/main/scala/code/api/v1_4_0/Http4s140.scala | 25780 | `3b39c12bd44865d876135fe86a80a7130a3a472db1a3c5611ade7e5f6eb8bb7f` | 0 |
| obp-api/src/main/scala/code/api/v1_4_0/JSONFactory1_4_0.scala | 56285 | `5e286b234c9906bf8dd6374d587aec4ba55a41b8685a0e6547e54eced866ece7` | 0 |
| obp-api/src/main/scala/code/api/v2_0_0/AccountsHelper.scala | 1686 | `a2c5d2112ea9750898556de7442e7b86fd0114e3a6a8222b94bae9530c08c59e` | 0 |
| obp-api/src/main/scala/code/api/v2_0_0/Http4s200.scala | 86676 | `226bcb594e33816af1d3cb99c20d0d471ea9aef2429bd3de250922de61105dab` | 0 |
| obp-api/src/main/scala/code/api/v2_0_0/JSONFactory2.0.0.scala | 28405 | `14afa57f75bfafbd80b21488dfef35666b89101de35b21f50b9e4d906fce8fd5` | 0 |
| obp-api/src/main/scala/code/api/v2_1_0/Http4s210.scala | 78370 | `47c33910a3692a3fb68913733da2f6785dc1fa98b60d2be9d6763c02dfd125e5` | 0 |
| obp-api/src/main/scala/code/api/v2_1_0/JSONFactory2.1.0.scala | 36410 | `9da6566d7dc5cd5668f5884d9ca1550e12719c46e81398618d645690bc77d1c0` | 0 |
| obp-api/src/main/scala/code/api/v2_2_0/Http4s220.scala | 60449 | `6809a51bc5d9cab75b0e186b89241bb0f2c70764fbc16c2096772c20f3119465` | 0 |
| obp-api/src/main/scala/code/api/v2_2_0/JSONFactory2.2.0.scala | 36336 | `46b19f83bc60debb8808d37dbe0e0983779cafd129aae8f617c677a3e1c683bf` | 0 |
| obp-api/src/main/scala/code/api/v2_2_0/MessageDocsJsonCache.scala | 5769 | `5cb8633f96fdfc55c457ec3d70df3c93855ba37c6efb60dc155f53d550faad27` | 0 |
| obp-api/src/main/scala/code/api/v3_0_0/Http4s300.scala | 115615 | `1789e24e2e47443c0723c9790374f9a4e6848ae48d19ff0aecf143763b3b8783` | 0 |
| obp-api/src/main/scala/code/api/v3_0_0/JSONFactory3.0.0.scala | 59507 | `39ff342f89b95d9f3674bd7a53aacda2d431e7f94dd0cd457dc15df752afe3fe` | 0 |
| obp-api/src/main/scala/code/api/v3_0_0/custom/JSONFactoryCustom3.0.0.scala | 1257 | `8aa9bbb800a71f2b49b4d6824bd47a7b6637d39fb3eb5828d9c8f1b53b4424f9` | 0 |
| obp-api/src/main/scala/code/api/v3_1_0/Http4s310.scala | 251568 | `4d7ee2df5ace71e65330dab633dc86cf475cee469132ef3a74252f5bcbbd87bf` | 1 |
| obp-api/src/main/scala/code/api/v3_1_0/JSONFactory3.1.0.scala | 53827 | `a7bec8e2805ae267b2fa5d81979515af357425e2134f94de3db4141426bdef80` | 0 |
| obp-api/src/main/scala/code/api/v4_0_0/Http4s400.scala | 547704 | `aad66785fdca2f6cacd8440abe80d18f10a5a52032c1fc8deed6a9148c850206` | 2 |
| obp-api/src/main/scala/code/api/v4_0_0/JSONFactory4.0.0.scala | 86088 | `b93af5aa54cc803fe1e97383703585d606054bd13ff85ca3e15c2ef20e805c98` | 0 |
| obp-api/src/main/scala/code/api/v5_0_0/Http4s500.scala | 128457 | `f79f72ff46681bfbf3ea87f2246967ad6425fbd01b6593a2b7b4b6c9bceffd54` | 0 |
| obp-api/src/main/scala/code/api/v5_0_0/JSONFactory5.0.0.scala | 40328 | `08dcefc4b2bfc46bc89d1e9083685f35ae672d9f9596e4b5e14459c46e598cb1` | 0 |
| obp-api/src/main/scala/code/api/v5_1_0/Http4s510.scala | 282668 | `0ebd3e1e442acc631653113bc51ba19409e5bef8ab34e0df9c3629b48fa58e64` | 4 |
| obp-api/src/main/scala/code/api/v5_1_0/JSONFactory5.1.0.scala | 57453 | `0e6c8d9fcda2cf81d1f45fa5df449c345f04d1aa7ff005df2467e57913f364e4` | 0 |
| obp-api/src/main/scala/code/api/v6_0_0/Http4s600.scala | 786218 | `010d6af6b5856eb9a2162cc3700e404b8b4d66a5de8fbdb64a7933204f039d48` | 4 |
| obp-api/src/main/scala/code/api/v6_0_0/JSONFactory6.0.0.scala | 118640 | `c26560c43470cbe77933790e25e87db6f8a595397d4aac33a3aeab21ffcf47c0` | 0 |
| obp-api/src/main/scala/code/api/v7_0_0/Http4s700.scala | 427340 | `ee1b40abf2ff7bf46c7de322f2b2d88050031337a13f1b93c65a9305d0c32017` | 0 |
| obp-api/src/main/scala/code/api/v7_0_0/Http4s700Assets.scala | 9231 | `f78b127b50309a34c8ea943a50504d264c5561567337e4680fe0c789382b43bd` | 0 |
| obp-api/src/main/scala/code/api/v7_0_0/Http4s700DeploymentChecks.scala | 4555 | `e3e7a6be23484eae3b07aecc564f8199120f425f4067ce848179a2c004271f87` | 0 |
| obp-api/src/main/scala/code/api/v7_0_0/Http4s700DomainApis.scala | 20647 | `fbd56c471078c79276748a831112f2c79565c04627b05dbb825e20add3a51eb9` | 0 |
| obp-api/src/main/scala/code/api/v7_0_0/Http4s700DynamicEntityDefinitions.scala | 17463 | `c97cad6a29d1259a9763db06dd524eb0214a3b3572382a61e5fb82c10c375e5c` | 0 |
| obp-api/src/main/scala/code/api/v7_0_0/Http4s700DynamicEntityWebhooks.scala | 28699 | `bc8aa07d7b1d25f832cf9e52eabedbdfb1276848e5ae43aa7cccfb6532b20a0c` | 0 |
| obp-api/src/main/scala/code/api/v7_0_0/Http4s700Grants.scala | 5205 | `a4e5195e0d4ab310e439768f65c773213b8e82581ba94a7cc06f23f10ab2c854` | 0 |
| obp-api/src/main/scala/code/api/v7_0_0/Http4s700Groups.scala | 18793 | `41fb2f9d21dd1f62bdb2cf27271d1225a018c3345ed3dc1834a950e1aa99bcd7` | 0 |
| obp-api/src/main/scala/code/api/v7_0_0/Http4s700IpPenalties.scala | 7340 | `fb4783ef4555e1f1ecdfc5c262561bac5c81b526183abf7f65ad8c05b0eb454d` | 0 |
| obp-api/src/main/scala/code/api/v7_0_0/Http4s700MyRoles.scala | 8628 | `04f04243bb28a553502f67fe32d6035004cf1954b8f8d5400e9cea634f5cec6a` | 0 |
| obp-api/src/main/scala/code/api/v7_0_0/Http4s700OpenIdConnect.scala | 5351 | `4d4f2894a8734b8ad939ebe21230d709470bde895f9e93c145d777304df7a250` | 0 |
| obp-api/src/main/scala/code/api/v7_0_0/Http4s700PlatformApps.scala | 12644 | `435ed4bc9e6d9157d78c07f2d1a512e6b1c90ef221e82cf025433177c43c5eb7` | 0 |
| obp-api/src/main/scala/code/api/v7_0_0/Http4s700Telemetry.scala | 5676 | `06f85d47160e9deff16620f522753cc9075b182a7ccf29133949c4f1a7d19b2d` | 0 |
| obp-api/src/main/scala/code/api/v7_0_0/Http4s700TrafficSources.scala | 5705 | `d15206ae0dc5142968f27d400320d6de3984e5a9522653f79e5996d3bd651b99` | 0 |
| obp-api/src/main/scala/code/api/v7_0_0/JSONFactory7.0.0.scala | 130046 | `57eafb971a14e13eb82d0d0c111f70317f730085f688372df79b08a60db389d4` | 1 |
| obp-api/src/main/scala/code/api/v7_0_0/JSONFactory700Assets.scala | 4016 | `60d0ddfdc25058955f89b53e566eacc7d70e8dbca08a050a03100b858207fe84` | 0 |
| obp-api/src/main/scala/code/api/v7_0_0/JSONFactory700DomainApis.scala | 4794 | `c055b3e496d5ce23666fe94cd0b7f27da128af9b3d8b54853f686133f8dbe4e9` | 0 |
| obp-api/src/main/scala/code/api/v7_0_0/JSONFactory700DynamicEntityWebhooks.scala | 8076 | `78fbc10f6f627100f2e040000e41ccf14e8d48db1e30a752149894658f121393` | 0 |
| obp-api/src/main/scala/code/api/v7_0_0/JSONFactory700OpenIdConnect.scala | 1673 | `7ac390888c58ae6906e6948eed1997047ef42e5bbe879ae52730f956925e8c04` | 0 |
| obp-api/src/main/scala/code/api/v7_0_0/JSONFactory700Operations.scala | 14058 | `cda363963bda2420ac891ffe24d99c5acd69833d49fe974fb35b3aee49ede06b` | 0 |
| obp-api/src/main/scala/code/api/v7_0_0/JSONFactory700PlatformApps.scala | 4443 | `23b48aa7a012ef963a0b5851d17ccb7ff8adaf075a779faa3939dfa11536d246` | 0 |
| obp-api/src/main/scala/code/apicollection/ApiCollection.scala | 2034 | `33988a66990bc3546e081a889a6868321e154f649c034d6fff5673cd9a1c7a08` | 0 |
| obp-api/src/main/scala/code/apicollection/ApiCollectionsProvider.scala | 3525 | `3d30cd1db47997c9e07591e5d9303ca39a1dfeaa3b9a0b105286729aaff6dbc4` | 0 |
| obp-api/src/main/scala/code/apicollectionendpoint/ApiCollectionEndpoint.scala | 1890 | `86467613ca622f7b6e6dc6f7d3237eebe5f3551aeb2bb430c9703e96f6bffcac` | 0 |
| obp-api/src/main/scala/code/apicollectionendpoint/ApiCollectionEndpointsProvider.scala | 2932 | `224d842bfa0bd5ea9bbaeb88e93e7354f609d21ff16b6d5a6c21986d86cc2814` | 0 |
| obp-api/src/main/scala/code/apiproduct/ApiProduct.scala | 4978 | `9c7087a82197a66b5e06543207ebbad3a01a311d8380e95c3c4015187fc8633b` | 0 |
| obp-api/src/main/scala/code/apiproduct/ApiProductsProvider.scala | 5442 | `581d794cd9df4dd59a75c45ea978253120bb577cb582c33348adc1d56b02df62` | 0 |
| obp-api/src/main/scala/code/apiproductattribute/ApiProductAttribute.scala | 2277 | `082f8b2aeafdf94928161465588edad2485b2576a5a3c7f02934f216fdc63c8b` | 0 |
| obp-api/src/main/scala/code/apiproductattribute/ApiProductAttributesProvider.scala | 4442 | `1ea9e117c3ca69e3a78ecfc3a6e89b9a6eda0c360291ca5955b3938b46f4ff8a` | 0 |
| obp-api/src/main/scala/code/apiproductsubscription/ApiProductSubscription.scala | 4355 | `7ba2bf46023c7c6976037b855510dd208a745869a26e7cfee3887f2724f56a49` | 0 |
| obp-api/src/main/scala/code/apiproductsubscription/ApiProductSubscriptionEnforcer.scala | 8884 | `3107dd8e1899ec09f97417f9edc2e3c2e229037c951ee9f67fc47dc0ce1be54c` | 0 |
| obp-api/src/main/scala/code/apiproductsubscription/ApiProductSubscriptionScope.scala | 2548 | `a921291aaa2c5a45d3e06f64174ab0b5185713231732b8acac1d5e44228181bb` | 0 |
| obp-api/src/main/scala/code/apiproductsubscription/ApiProductSubscriptionsProvider.scala | 5880 | `dd66b618947b03bb9d2a4db08203e73863a59c1e2f5c51b4f54fb4b66cace817` | 0 |
| obp-api/src/main/scala/code/apiproductsubscriptionattribute/ApiProductSubscriptionAttribute.scala | 2491 | `3e63f3eadbcfda786e0eafe2836d12d3a8197a5d1c9f3b14ebd01fc78020a12f` | 0 |
| obp-api/src/main/scala/code/apiproductsubscriptionattribute/ApiProductSubscriptionAttributesProvider.scala | 4215 | `d22385ca13398b78dda983e1ada73933e7a706e2c78416d8cae6ba29610cc05d` | 0 |
| obp-api/src/main/scala/code/asset/AmountPrecision.scala | 6364 | `688636ca742b5459317f19afa18dd54d1b4df208b69ce515d2e3b8254cdece6e` | 0 |
| obp-api/src/main/scala/code/asset/Asset.scala | 5079 | `61cd974cf9f984e0b31b27fa03c03c3c9e83af62af48579752f97a286ff5ea02` | 0 |
| obp-api/src/main/scala/code/asset/AssetLookup.scala | 5912 | `ae51d46c2edfacd073884a0737d664088fee574467216c7e86b13a010d9bc4f0` | 0 |
| obp-api/src/main/scala/code/asset/AssetSeed.scala | 5451 | `f33a4e2fd5e6b432d52db15cea9d1af0326424f71c809299a8005583255d4c85` | 0 |
| obp-api/src/main/scala/code/asset/Assets.scala | 7329 | `b914ab499ce2c3e178d2535327c4133e017c166f5ac204cefa41fd050aa7b2f6` | 1 |
| obp-api/src/main/scala/code/asset/CurrencyCodes.scala | 5211 | `fcf7d5d84980e23e6c1165108ade995607c909c01c2c40659a4737359f1ea97e` | 0 |
| obp-api/src/main/scala/code/atmattribute/AtmAttribute.scala | 2404 | `8834a108e34ff805b86ed7bb69088a4b2ed7282e98a7768f7c472bdcb744c54e` | 0 |
| obp-api/src/main/scala/code/atmattribute/MappedAtmAttributeProvider.scala | 4775 | `574587843bf73aa9002e7c79e655230cc673b586e8b7e72ef1789741fd264c8d` | 0 |
| obp-api/src/main/scala/code/atms/Atms.scala | 3887 | `9a9d9801b972e02855e6b4ca476ec5371f3bae6eac2c675d1cc1c85423b74089` | 0 |
| obp-api/src/main/scala/code/atms/MappedAtmsProvider.scala | 16674 | `befd4cb8454d2777d6a5720a501d90fbaf4d98bdab36ff9e873b7c497cbc6667` | 0 |
| obp-api/src/main/scala/code/authtypevalidation/AuthenticationTypeValidationProvider.scala | 2440 | `5ef01b9f247209934f334d4c575a83779c9b8662239c5ce14a41d76374ea5258` | 0 |
| obp-api/src/main/scala/code/authtypevalidation/MappedAuthTypeValidationProvider.scala | 3150 | `76c7addac36eddd457c7fb0df9fe9fe3a121a835d87a3d8a10b0f5bf72d72633` | 0 |
| obp-api/src/main/scala/code/authtypevalidation/MappedAuthenticationTypeValidation.scala | 1557 | `29e7d7b2c95c78758604aa31ed68055224eeeb7166e03bc87f14dac2fc911ca1` | 0 |
| obp-api/src/main/scala/code/bankaccountbalance/BankAccountBalance.scala | 3585 | `a66ffadaf33f41ceb1351397bde06eb30a8fc47c9f09c6f3b5eef0fe4fe441b4` | 0 |
| obp-api/src/main/scala/code/bankaccountbalance/BankAccountBalanceProvider.scala | 4866 | `163e440cfc7b3328efafe62c8a18c6a885902ee03c63270ba920fc1d59294075` | 0 |
| obp-api/src/main/scala/code/bankattribute/BankAttribute.scala | 2317 | `ed93cb8192ed994537e80fdfcf573a1adcc0e61c30e8d36131f4e54ae4779430` | 0 |
| obp-api/src/main/scala/code/bankattribute/MappedBankAttributeProvider.scala | 4251 | `65a140463d736792922f2576c1fb0fd76c496f6ed928dd609edcbb2a841fd932` | 0 |
| obp-api/src/main/scala/code/bankconnectors/AvroSerializer.scala | 2286 | `74d3d985b35f0a0f8f82156666161f6a2adb50f5f464ab29c5c9539f26e09b72` | 0 |
| obp-api/src/main/scala/code/bankconnectors/Connector.scala | 126888 | `6f6d34288fab943a38fa9df7383b526abcee959d859d7158a3c48ce1321bcda1` | 0 |
| obp-api/src/main/scala/code/bankconnectors/ConnectorEndpoints.scala | 9154 | `76fd94693c68f8b4030f1bf196775527537ce2851e2b1fb311a2c94320d2b95b` | 0 |
| obp-api/src/main/scala/code/bankconnectors/ConnectorProxy.scala | 5292 | `a8c72c853f93adc9e3c792984f8eb5bc2e518cbe171dce0de9e4ff44e4c1450f` | 0 |
| obp-api/src/main/scala/code/bankconnectors/ConnectorUtils.scala | 6903 | `2fcff32f5f5f2f0efe027bff38a69215cad8b6cb877fb9a8d4d8455e55f15c89` | 0 |
| obp-api/src/main/scala/code/bankconnectors/DoobieBadLoginAttemptQueries.scala | 1826 | `b484d5366a8e585fc65a26a275421f260970689cd3fbf7ba18474180ede5f2d1` | 0 |
| obp-api/src/main/scala/code/bankconnectors/DoobieBankAccountQueries.scala | 2235 | `e8df54ca2dc8bea2ccb53742d8dfb7c6f1b6ad79006b5adabbc907202f281c57` | 0 |
| obp-api/src/main/scala/code/bankconnectors/DoobieBusinessStatusQueries.scala | 4058 | `d2a143708374a783cd97df34cbb57ad78f77a188d6ccce998194b7bb16f1fba0` | 0 |
| obp-api/src/main/scala/code/bankconnectors/DoobieChallengeQueries.scala | 1860 | `44d5af12e4d116718f56fb9660792b781b6b8794d1837f311d6db3e4d0225a64` | 0 |
| obp-api/src/main/scala/code/bankconnectors/DoobieConsentSchedulerQueries.scala | 1822 | `5bf6d899315985aba7ad9713c7bdc45e01097ad539cf90b3602d6c297150c845` | 0 |
| obp-api/src/main/scala/code/bankconnectors/DoobieConsentStatusQueries.scala | 3405 | `070d615d2f8b232866988f57e6660134c24f5f52ebee00458eefebe9ed1876e2` | 0 |
| obp-api/src/main/scala/code/bankconnectors/DoobieTransactionRequestQueries.scala | 3082 | `46076a628a34ba2bb8a420d4f929b5aae46903ae1e41f43d62ff3f00c5123eba` | 0 |
| obp-api/src/main/scala/code/bankconnectors/DoobieUserAuthContextUpdateQueries.scala | 1738 | `35adaf9b3bc072cc3b3ee49651dc0375482a62ef828c2a486707505bbf29f989` | 0 |
| obp-api/src/main/scala/code/bankconnectors/DynamicConnector.scala | 5853 | `2943ae34c8de05d3765fadf7e15524eec6a5a5316d467a3c0f4831b1a2b8887d` | 0 |
| obp-api/src/main/scala/code/bankconnectors/DynamicJavaConnector.java | 981 | `d008c0ef4e2ba5919e352458804971c2727617207d7cb96083949c2cf5d29193` | 0 |
| obp-api/src/main/scala/code/bankconnectors/InternalConnector.scala | 16455 | `75fca58f31964b58deca338e6015bfbdec9bd6459101d4845686428e50a8007c` | 0 |
| obp-api/src/main/scala/code/bankconnectors/LocalMappedConnector.scala | 324996 | `43ef119ef05f87d89a14bd284d5758e4a844c8e36592199f39448cab4bcbe279` | 0 |
| obp-api/src/main/scala/code/bankconnectors/LocalMappedConnectorInternal.scala | 88378 | `26c8bcd7d979a68c0d911ab2dcbb9b0ae47aca8a8ad94787227e1cca36310c2c` | 0 |
| obp-api/src/main/scala/code/bankconnectors/akka/AkkaConnectorBuilder.scala | 1637 | `0438b5ae78e6dcf7841cce791e760db7be70301fbdbf44ffd4ac8dd046d8fdea` | 0 |
| obp-api/src/main/scala/code/bankconnectors/akka/AkkaConnector_vDec2018.scala | 347869 | `861355642e8c2b9135567dc4b3c1071bb16a9dcca749ca1de03ea02ac5956aca` | 0 |
| obp-api/src/main/scala/code/bankconnectors/akka/actor/AkkaConnectorActorConfig.scala | 4196 | `3a2a58f3210c9fc2dad00d2a78598e77bdf419f8f09df125859f80f27510e398` | 0 |
| obp-api/src/main/scala/code/bankconnectors/akka/actor/AkkaConnectorActorInit.scala | 1338 | `98536ba20dbe71f1c1a19563bf474a15eb7434895511e84c926b1e5a96d9c5c0` | 0 |
| obp-api/src/main/scala/code/bankconnectors/akka/actor/AkkaConnectorHelperActor.scala | 1550 | `0e27fef033cb3de79f5bfd4e0fbe4115f5f54cd306bf414a75d0c64933727dbf` | 0 |
| obp-api/src/main/scala/code/bankconnectors/akka/actor/SouthSideActorOfAkkaConnector.scala | 7827 | `3e924166d23ebf5139ed61c447939ca2fc81ae73ae45825514b67b903f403d74` | 0 |
| obp-api/src/main/scala/code/bankconnectors/cardano/CardanoConnector_vJun2025.scala | 7203 | `4819ad07a5596139267a6ff9386fd1fca8c3e5900be8cb963fe3b8d7664a7c94` | 0 |
| obp-api/src/main/scala/code/bankconnectors/demoJsConnector.js | 1344 | `92d1b6ad9a1adc665c0c052d4fdac3d72abaa6fddbc642ec4d4bd36972ca1baf` | 0 |
| obp-api/src/main/scala/code/bankconnectors/ethereum/DecodeRawTx.scala | 7744 | `07d7e6add499f0a08952c24614373040d85cb57b6edda787e31d34cbffb0e42c` | 0 |
| obp-api/src/main/scala/code/bankconnectors/ethereum/EthereumConnector_vSept2025.scala | 6329 | `e4948ca1bd18af18cfae62ef8784b08c51b80952e83f25e21160173541aa0245` | 0 |
| obp-api/src/main/scala/code/bankconnectors/generator/CommonsCaseClassGenerator.scala | 3249 | `ec649800e9589d2116f9eca2753efb14c1fa53b74d039f334559c5770ffb3977` | 0 |
| obp-api/src/main/scala/code/bankconnectors/generator/ConnectorBuilderUtil.scala | 22054 | `f0b3dce71a7fa2b17f3dd88df0c86cbf798bc75a1974ed5799c9f578d36c8819` | 0 |
| obp-api/src/main/scala/code/bankconnectors/generator/InOutCaseClassGenerator.scala | 3134 | `1f5e1fac95272ad31682603b3907a4ffb96aa64407314379957db2220fe4d72f` | 0 |
| obp-api/src/main/scala/code/bankconnectors/grpc/GrpcConnectorBuilder.scala | 2250 | `7b6dda0dad900500fa0be7900c97c04e17815ea690d1c50f33395aac08515711` | 0 |
| obp-api/src/main/scala/code/bankconnectors/grpc/GrpcConnector_vFeb2026.scala | 417242 | `0d702a7df6e805fe5b157460d13ec7cf88ae00b9bcbfd24b9af952d85e2e8480` | 1 |
| obp-api/src/main/scala/code/bankconnectors/grpc/GrpcUtils.scala | 4227 | `019704ebcc7bedc0fbd3a4199b7968a19c1a45d5f01c96117870fb997fcd14f7` | 0 |
| obp-api/src/main/scala/code/bankconnectors/grpc/api/ObpConnectorServiceGrpc.scala | 4582 | `f9aae1b045dc2a71e70a0d8e359ebc051a4d17b2306db74dec4175d936763679` | 0 |
| obp-api/src/main/scala/code/bankconnectors/opencorridor/OpenCorridorProcessor.scala | 18716 | `5ab7b403e679bf241eea192f69dc4e51d6dea73c8665cf1b516b07111100bbd2` | 0 |
| obp-api/src/main/scala/code/bankconnectors/opencorridor/OpenCorridorPublisher.scala | 12320 | `2c280a1abca98c75b3d5076bbbf02af218ca4a67d12c8e2bf28c533e3c653260` | 0 |
| obp-api/src/main/scala/code/bankconnectors/opencorridor/OpenCorridorSettlement.scala | 21038 | `d244c43b15ac13aef9cf23a05755a0f6aa64037a8888c23cf96cc7c2817bb532` | 0 |
| obp-api/src/main/scala/code/bankconnectors/package.scala | 26966 | `ab23b15e2efbb50486e78924a55d149e7e4c41cc9444928c97400112aed06c5a` | 0 |
| obp-api/src/main/scala/code/bankconnectors/rabbitmq/Adapter/AdapterStubBuilder.scala | 9706 | `570b65fc71eb57075fa719ca1f2d87478b5478a59736e4c3ae2a5b064fd52e41` | 0 |
| obp-api/src/main/scala/code/bankconnectors/rabbitmq/Adapter/MockedRabbitMqAdapter.scala | 164376 | `a6d22a3e7a64c34595584ae9856672e38f2fabaaa3709e349158733c813343e5` | 0 |
| obp-api/src/main/scala/code/bankconnectors/rabbitmq/RabbitMQConnectionPool.scala | 4952 | `360798dc4d7bc0672f7aec6539a85d38ac25f2f6abacb82c4ed7fc4079850a60` | 0 |
| obp-api/src/main/scala/code/bankconnectors/rabbitmq/RabbitMQConnectorBuilder.scala | 1334 | `d8631861abd19da4eaa1b4497068f27b52dcf746413f4813f9c93305490039f8` | 0 |
| obp-api/src/main/scala/code/bankconnectors/rabbitmq/RabbitMQConnector_vOct2024.scala | 416444 | `78f6a1b9b3375bbf45276b77696af1543efa76a8d8955be71df110605a0dd45f` | 1 |
| obp-api/src/main/scala/code/bankconnectors/rabbitmq/RabbitMQUtils.scala | 11982 | `0e76a8b612c3cdcbe55f70a7d322157b039f05ad134290a1e34293cc7a059788` | 0 |
| obp-api/src/main/scala/code/bankconnectors/rest/RestConnectorBuilder.scala | 1271 | `4f49c40af545216b1796b7011d252b1f2d57b9060d0ea6b40831d9264e4ecf97` | 0 |
| obp-api/src/main/scala/code/bankconnectors/rest/RestConnector_vMar2019.scala | 412695 | `9227dfe13d0e8bb55a3d8c28dce35015336c45d7625591e360b7aaa400ea5831` | 1 |
| obp-api/src/main/scala/code/bankconnectors/storedprocedure/MSsqlStoredProcedureBuilder.scala | 4445 | `e430f39b574ed2b0098e8871ec89c737191cf2381c8c558ddd985b0a6036e78d` | 0 |
| obp-api/src/main/scala/code/bankconnectors/storedprocedure/StoredProcedureConnectorBuilder.scala | 1344 | `95c9ee6d04449a7e69d648cadd69cc75abf52af342b9dbc5aa878aa5ab83e7e8` | 0 |
| obp-api/src/main/scala/code/bankconnectors/storedprocedure/StoredProcedureConnector_vDec2019.scala | 417683 | `30989e5ff10ef368edda6b4934861606b87281e19aa8bf533168c2e79a3a134f` | 1 |
| obp-api/src/main/scala/code/bankconnectors/storedprocedure/StoredProcedureUtils.scala | 11574 | `c29df9d077f625187d3ab419493dc90507270b73683beae886ba13d24725ab79` | 0 |
| obp-api/src/main/scala/code/branches/Branches.scala | 8488 | `614c5cac66dbce60a29ab417403193875a6544dac6efa0ccdd45c2db691221a7` | 0 |
| obp-api/src/main/scala/code/branches/MappedBranchesProvider.scala | 11229 | `b0a859faaf97accf0a0dae4b6b77aa29b74e1bf907244f9914ba9ecff5525450` | 0 |
| obp-api/src/main/scala/code/bulkpayment/BulkPayment.scala | 5633 | `0ce504fcd436c9d39643e49eb52ffbd284789ce97fadb8887c13925018c35319` | 0 |
| obp-api/src/main/scala/code/bulkpayment/BulkPaymentHandler.scala | 9927 | `c7fec5243080c2fe5e8c6e9b4b9a4000152009325b83b114481c2679a195e3eb` | 0 |
| obp-api/src/main/scala/code/bulkpayment/BulkPaymentTrait.scala | 3174 | `b777b8a0c3ba3bf991923005595f4a182bf6837715c3ce4a266c3ef523173d61` | 0 |
| obp-api/src/main/scala/code/cardattribute/CardAttribute.scala | 2214 | `2b90c836bae80ec36b14cb960bb25da18698fb252ef81c49fc7195603b83ac35` | 0 |
| obp-api/src/main/scala/code/cardattribute/MappedCardAttribute.scala | 2126 | `423bc857e5bc970228077febe260362d4b3456f50c11bbd5271b5cc5ba294863` | 0 |
| obp-api/src/main/scala/code/cardattribute/MappedCardAttributeProvider.scala | 3062 | `d38f9a85af57021c06cfe2371f682d2bc9a1faf811df63992625d3934ed0383b` | 0 |
| obp-api/src/main/scala/code/cards/MappedPhisicalCard.scala | 15640 | `a7f2a0005e17c224449f0ce73c440dad7733b2326b24b09c315eda147f43d98e` | 0 |
| obp-api/src/main/scala/code/cards/PhisicalCardProvider.scala | 3206 | `e5d30d5d0c9b571eef2c2150c255c313105bdfd17d511b410bbadb88757baa07` | 0 |
| obp-api/src/main/scala/code/chat/ChatContentPolicy.scala | 1688 | `59201d26a601a17c4e1746a91bc6942c055b3f5a939934acee05339fe5b2580e` | 0 |
| obp-api/src/main/scala/code/chat/ChatEmailDigestScheduler.scala | 7579 | `e22c65d82c8d8c1913f1ffef71ddd2ace11e4e24a3c28d3b68ba7dc1eac9ab6c` | 0 |
| obp-api/src/main/scala/code/chat/ChatEmailDigestState.scala | 2111 | `825be200c27fd4707cb9da5cafcfe442de3bf3fbd5afa4f1af28b4eb45738a04` | 0 |
| obp-api/src/main/scala/code/chat/ChatEventBus.scala | 6017 | `8852783ef1c4244c4083c9b7626150d309368bab7156da4d8ba55d7c4678d558` | 0 |
| obp-api/src/main/scala/code/chat/ChatEventPublisher.scala | 8328 | `a78a63d93cbfd3e90d02957fabbf56617589a48901176dc4a7c0fd19bb40de34` | 0 |
| obp-api/src/main/scala/code/chat/ChatLinkPolicy.scala | 4049 | `9b8cd4f36271216a4ce7bd40101263d8dbda32bdc031feddbd4325825d7bc391` | 0 |
| obp-api/src/main/scala/code/chat/ChatMessageTrait.scala | 2476 | `7eef134e1bc8d49fdadcd58acff75278e7e970032d2d1ce035a9395351651516` | 0 |
| obp-api/src/main/scala/code/chat/ChatMessageValidation.scala | 2104 | `d1038a92701c5b8b38ea84bc844210cb3264da982b393d16431b82c5a6b31ebd` | 0 |
| obp-api/src/main/scala/code/chat/ChatPermissions.scala | 3276 | `15fce173e749d877af0f801a36813f90b29baa50ec72d2cf07a377067861be82` | 0 |
| obp-api/src/main/scala/code/chat/ChatRoomTrait.scala | 3237 | `0c87c71410b1dd695c591531a900ae99f020c6f1a8438182d96a0b8e54574463` | 0 |
| obp-api/src/main/scala/code/chat/DoobieChatMessageQueries.scala | 3908 | `1d5ae399349189da2945dd0dfc43a2e148733197b26d86aba601fcf63e979a76` | 0 |
| obp-api/src/main/scala/code/chat/MappedChatMessage.scala | 6035 | `4ecd31f2440e8c08012f5b64c849143e07b2dc615261251e3ad64f692ececb0a` | 0 |
| obp-api/src/main/scala/code/chat/MappedChatRoom.scala | 8216 | `59fc7d520ec4f53b2c456422db06e87ce108b900184d32b8c62c33a86740f706` | 0 |
| obp-api/src/main/scala/code/chat/MappedParticipant.scala | 5381 | `53954a431167e5cfdefc54799f8622f00889a0349da303189ff5134d3e690e72` | 0 |
| obp-api/src/main/scala/code/chat/MappedReaction.scala | 3229 | `f008b8c298fde7963a58d57b1206e2dbf95a70d1e0012967465fdd091fd00fba` | 0 |
| obp-api/src/main/scala/code/chat/ParticipantTrait.scala | 2440 | `0155da1be5360ee497c7f24afb5c1691f0d7c49242537808d60f094316d54818` | 0 |
| obp-api/src/main/scala/code/chat/ReactionTrait.scala | 1750 | `75ed162ea1258fe10b97a50f124bb00607ff587197a399da94f6b3cda79c1179` | 0 |
| obp-api/src/main/scala/code/connectormethod/ConnectorMethod.scala | 3096 | `d93c7cfec9d341df27d106bcad4cfa69be790ad68dbefc7f82fe03516f966314` | 0 |
| obp-api/src/main/scala/code/connectormethod/ConnectorMethodProvider.scala | 2295 | `05dee11f3953ee1facfe3b50e3d31018eaf8552539eafa628bf238ff5f2fb7d5` | 0 |
| obp-api/src/main/scala/code/connectormethod/MappedConnectorMethodProvider.scala | 4189 | `08caf187ade6f04f2096728374cc28bbea86032794820c506496052a341f2df2` | 0 |
| obp-api/src/main/scala/code/consent/ConsentItem.scala | 2451 | `6b21549a4977db82ca43f8e622be93175cf3907cc4918251164a4a05519ef5f8` | 0 |
| obp-api/src/main/scala/code/consent/ConsentProvider.scala | 9265 | `18d94c75435c6fb4dda576e4d4e9f101ae8e747885554b5a2b97d4c87c511e39` | 0 |
| obp-api/src/main/scala/code/consent/ConsentRequesProvider.scala | 1541 | `057298c79c84564ae8160434124c36816f2638de63f31c05905cdbe37408866d` | 0 |
| obp-api/src/main/scala/code/consent/ConsentRequest.scala | 2338 | `c6d8262e336e900540c13821a8c3ab2397f647f1dc272bbf6c22afaff13341a1` | 0 |
| obp-api/src/main/scala/code/consent/DoobieConsentQueries.scala | 10500 | `0fc19e432974affa614e33dfa9f2e0eea2c4daca2e0c484fb934ce21e4555ca2` | 0 |
| obp-api/src/main/scala/code/consent/MappedConsent.scala | 24286 | `20b69b856bdc3d5d95914cd29bf730814d0e8b562a2dd86521a98298e8d364a9` | 0 |
| obp-api/src/main/scala/code/consumer/ConsumerProvider.scala | 4439 | `a66b9c54cf75f81cbb54000426dfe556c1cd028a7a07e5de8a78828e3585488d` | 0 |
| obp-api/src/main/scala/code/context/ConsentAuthContextProvider.scala | 1966 | `eb76c6f31c46c51f42cf2bc8a2800b9b3cf3cb38e7e7bba7a3122c6389f4909b` | 0 |
| obp-api/src/main/scala/code/context/MappedConsentAuthContext.scala | 1906 | `c69cd9977ce1e1f3b8bb692ad3ca7a0d4ce3649931b40b62a65c0096c87096e0` | 0 |
| obp-api/src/main/scala/code/context/MappedConsentAuthContextProvider.scala | 4467 | `cd359b9d848384e7f36c6caf4b130a624d546ae2aa050c94c82d204e88c0f504` | 0 |
| obp-api/src/main/scala/code/context/MappedUserAuthContext.scala | 1889 | `fed52b7a6ff6bec62f72a8e166b6a00489a452a53b66e4b9481e736ffb521d57` | 0 |
| obp-api/src/main/scala/code/context/MappedUserAuthContextProvider.scala | 4628 | `eea9bcb8cda995881a4c4140a4bc6c569ba00a984527835de672e57558d53a10` | 0 |
| obp-api/src/main/scala/code/context/MappedUserAuthContextUpdate.scala | 2533 | `eccd1727940b32a9cfa419184a3929b4b8d2b9b924157ead738f96866531ca4c` | 0 |
| obp-api/src/main/scala/code/context/MappedUserAuthContextUpdateProvider.scala | 5551 | `379755a6a345ac546c034f218dcc2c44f16a95a7df7fb75913207c48782a6468` | 0 |
| obp-api/src/main/scala/code/context/UserAuthContextProvider.scala | 1920 | `e1646c7bdaf4d44b558705286640db68921a8bc177a7b461e4bfc803adc8df2b` | 0 |
| obp-api/src/main/scala/code/context/UserAuthContextUpdateProvider.scala | 2164 | `a6f54cdf453a27e731e08e8e4993e269e7a26f9813856a601014e5ce3da178f6` | 0 |
| obp-api/src/main/scala/code/counterpartyattribute/CounterpartyAttribute.scala | 2326 | `da414899c5ffd1bfc4e7f94f63ed3f7755be9c4ff736f22d67e8b0476b4e017a` | 0 |
| obp-api/src/main/scala/code/counterpartyattribute/MappedCounterpartyAttributeProvider.scala | 4829 | `81339925ec74f9893584ed9ebc3f0f2f263112ace51e371fb9528d870c5c3909` | 0 |
| obp-api/src/main/scala/code/counterpartylimit/CounterpartyLimit.scala | 2056 | `0e3fa06e3bfe16c0222168762ece6b6616c255ac9d2abb746cba972d2958a31b` | 0 |
| obp-api/src/main/scala/code/counterpartylimit/MappedCounterpartyLimit.scala | 7294 | `d9e37edd4a92810e6458cb0e2e42054ae01e0d68055b9ba35aa7ed3963141f5a` | 0 |
| obp-api/src/main/scala/code/crm/CrmEvent.scala | 3266 | `62be020175086805a6f3919991c9c183fd466df6eafd97025d7a02a15b0d283e` | 0 |
| obp-api/src/main/scala/code/crm/MappedCrmEventProvider.scala | 3909 | `830bfe462f652f6945c327dfd0273bfe68fd9e0f1b624e9dcd1fda1d2e5391d4` | 0 |
| obp-api/src/main/scala/code/customer/CustomerMessage.scala | 1773 | `fd2dcba56e658762a3e2e17290aca9395d2ed106e521d7d24328dee8496b4eee` | 0 |
| obp-api/src/main/scala/code/customer/CustomerProvider.scala | 5219 | `9f9a1f81563c2db07ae6d4aa7f3912179abb5a515fb2c0813930f13981001f7b` | 0 |
| obp-api/src/main/scala/code/customer/MappedCustomerMessageProvider.scala | 3982 | `0022adc6f55bbd1b85f2ba3ac36a37bd4ee06b71dc58fa7beef1b1a88b9a1c20` | 0 |
| obp-api/src/main/scala/code/customer/MappedCustomerProvider.scala | 19422 | `4d78600d2e6f1d4c72511855ec5eb25ac04a827726aa32312b738d157dde3d55` | 0 |
| obp-api/src/main/scala/code/customer/agent/AgentProvider.scala | 2417 | `ac82010df967c3916a5f821375968c18834d49614666762ae77d11a4105ed2d1` | 0 |
| obp-api/src/main/scala/code/customer/agent/MappedAgentProvider.scala | 4605 | `cb46a3b8cf8229889256e8ac85fcce7672bcc54a1d5bc7fc0b3d7f52e6739855` | 0 |
| obp-api/src/main/scala/code/customer/internalMapping/CustomerIdMapping.scala | 2138 | `b9cf74a8d3fceb8c343915467b6fe85e664cfff89da6e78dd6fba6ee2f94040e` | 0 |
| obp-api/src/main/scala/code/customer/internalMapping/CustomerIdMappingProvider.scala | 1436 | `5e534d4d809600482c78ac07b06bf69d6c5a997147ef810fb3369e225183b432` | 0 |
| obp-api/src/main/scala/code/customer/internalMapping/MappedCustomerIdMapping.scala | 2253 | `a2d1a61dab90a9546b187b088c32251709a36b6dffc4b76fda1b143272f61b2e` | 0 |
| obp-api/src/main/scala/code/customer/internalMapping/MappedCustomerIdMappingProvider.scala | 2723 | `e4ba4b6d91e6868396f5fe95d4688569b9d1e5f41f3b6281a2d7af5b8b7f8c3e` | 0 |
| obp-api/src/main/scala/code/customerDobDependants/CustomerDependants.scala | 1669 | `3ef0cb94b001828aa75fd56d2a13a14de77a96cef80851ca212c5399f71e83cd` | 0 |
| obp-api/src/main/scala/code/customerDobDependants/MapperCounterpartyBespoke.scala | 2202 | `977e28f170808e00115203f2dc289fd321015c48332ac785b0cdff8b24111da2` | 0 |
| obp-api/src/main/scala/code/customeraccountlinks/CustomerAccountLink.scala | 2444 | `b7e3390e43593f0ea63a37845ef7b0631c96c0c774acdbfe92c7fcd8caaba7f6` | 0 |
| obp-api/src/main/scala/code/customeraccountlinks/MappedCustomerAccountLink.scala | 6037 | `1237735671b033d00b95ddfcbccd50f49f7347f993123b2c74356e5938af0d28` | 0 |
| obp-api/src/main/scala/code/customeraddress/CustomerAddress.scala | 2337 | `a898417b98abaa5af69483ba8eddb243977e50f531d4b076cf1d1a3e596350b1` | 0 |
| obp-api/src/main/scala/code/customeraddress/MappedCustomerAddressProvider.scala | 6155 | `4ad3d99eeafbbc9b3402c720d505e0f3101e16b40e9f136330b5d8c301d3abbe` | 0 |
| obp-api/src/main/scala/code/customerattribute/CustomerAttribute.scala | 3144 | `4b2d1c034508b29c3ac341551e391ee75545f7970cc837a405c2e38f2cda0b97` | 0 |
| obp-api/src/main/scala/code/customerattribute/MappedCustomerAttributeProvider.scala | 7451 | `67ae1647415551792ce6e559e57439a110e68cae27d9a05b5dec636bd02d357c` | 0 |
| obp-api/src/main/scala/code/customerlinks/CustomerLink.scala | 2067 | `1700fa58dae6f1ac30fa1945f9a939f1e0c0cf49d9ea8c76ac77996e7752608f` | 0 |
| obp-api/src/main/scala/code/customerlinks/MappedCustomerLink.scala | 4263 | `a75cc9e76cab180ed3ab6ee585dcc0e1e7e7c79c2bcd6f21fa76c160e73b6969` | 0 |
| obp-api/src/main/scala/code/directdebit/DirectDebit.scala | 1789 | `f10fe20632f9a499e5569eea3ffc90ed23ac3644d70a1df603311cb719fa49b1` | 0 |
| obp-api/src/main/scala/code/directdebit/MappedDirectDebit.scala | 4041 | `06398126ab579923ae7dc2b7a03453b1bd04d97fdce97e21d2e677f71bb79310` | 0 |
| obp-api/src/main/scala/code/domainapi/DomainApi.scala | 9891 | `014267b03fa429376eef8fc0a3745878b4b0c6caf026ba27c5c3af7c87c7144e` | 0 |
| obp-api/src/main/scala/code/dynamicEndpoint/DynamicEndpointProvider.scala | 2623 | `21b8c420b0ee3a9fc0ee9e44b088a523bf2a3a32c09d0aebeb5288f1126ea284` | 0 |
| obp-api/src/main/scala/code/dynamicEndpoint/MapppedDynamicEndpointProvider.scala | 5342 | `8669303a74cf568b3d39aa1639a6f35eedf47844eaf5a43f5f7817f829427d6c` | 0 |
| obp-api/src/main/scala/code/dynamicEntity/DynamicDataAccessProvider.scala | 4488 | `27c9c29b10410ecc9f12fc6d4c711341e8cec47c3e06ab86d86f99f3103ed153` | 0 |
| obp-api/src/main/scala/code/dynamicEntity/DynamicDataProvider.scala | 5651 | `1f0c8ded39215acf4115e6870260d3718b14c55d8ef8fc181b65b020d9dc6670` | 0 |
| obp-api/src/main/scala/code/dynamicEntity/DynamicEntityProvider.scala | 41804 | `48797cb0db764ad779b9dd35911e3fcf8a72840bec59405a5af9ffb5a7e6db48` | 0 |
| obp-api/src/main/scala/code/dynamicEntity/MappedDynamicDataAccessProvider.scala | 8605 | `02b9aaef15ce4fbbf69c8d35d731a2d4d70ca86089efbafafdefde7a5874c476` | 0 |
| obp-api/src/main/scala/code/dynamicEntity/MapppedDynamicDataProvider.scala | 22633 | `e88b03ba99013aea8c26aa6dadbc31f764f7ef83b8ef8f13250139dbf591f2ab` | 0 |
| obp-api/src/main/scala/code/dynamicEntity/MapppedDynamicEntityProvider.scala | 11524 | `15d557c3800a04ffa2832f3533c6e2b9d09b9ec2ac3a1d0b4b44d750050aaf26` | 0 |
| obp-api/src/main/scala/code/dynamicMessageDoc/DynamicMessageDoc.scala | 4149 | `71c25406039773ebaf3d3c1c348a84b308925346b827e2eac82f60f5a3979581` | 0 |
| obp-api/src/main/scala/code/dynamicMessageDoc/DynamicMessageDocProvider.scala | 2504 | `8b35c1cf0c547c58e3c75517fe1ba3dd16c88f48d0bbf8ded4ba2adfcc0a0d3b` | 0 |
| obp-api/src/main/scala/code/dynamicMessageDoc/MappedDynamicMessageDocProvider.scala | 6357 | `1391523cee80df9b3faab859382418740f2852e8eaa5774f8861d36b895d7fc7` | 0 |
| obp-api/src/main/scala/code/dynamicResourceDoc/DynamicResourceDoc.scala | 5451 | `ed8beb3858ebd6170029d245dd0ac89a9bfc4f960227e9a0d1a867d914e3943d` | 0 |
| obp-api/src/main/scala/code/dynamicResourceDoc/DynamicResourceDocProvider.scala | 3504 | `8323b254a16d8e54669f8444071e4f48fd1a4bd4206356773c547e62168a43c4` | 0 |
| obp-api/src/main/scala/code/dynamicResourceDoc/MappedDynamicResourceDocProvider.scala | 7090 | `d7d4592afd6ba738245fb886d780e06b7afc5ca335f6d9945f421efde66b59b9` | 0 |
| obp-api/src/main/scala/code/dynamicchangerequest/DynamicChangeRequest.scala | 6642 | `b5db3e6d0488ef187ea8dabedaad0eec7eb650fce4d096534c92658cfb371932` | 0 |
| obp-api/src/main/scala/code/dynamicchangerequest/DynamicChangeRequestTrait.scala | 3436 | `13ca4f8c7534e7a5767bfdeebdd0a792003151dc7c1f184f167b061290c06069` | 0 |
| obp-api/src/main/scala/code/dynamicchangerequest/MakerChecker.scala | 38913 | `13adc6c155cf93083187e10ee7f21bea6b7ec18d34e27c259cfc7b5c16caddc4` | 0 |
| obp-api/src/main/scala/code/dynamicentitywebhook/DynamicEntityWebhook.scala | 15962 | `2aac018dadcb08d4e521a953752e96c54b37949551c4b2ebcd53505876d9fa6e` | 0 |
| obp-api/src/main/scala/code/dynamicentitywebhook/DynamicEntityWebhookConditions.scala | 4951 | `7447a9198f2bf29974ac6bfddfde42c64905bcf48b4ec39b1c621fb1a5a13904` | 0 |
| obp-api/src/main/scala/code/dynamicentitywebhook/DynamicEntityWebhookDefinitionChanges.scala | 3444 | `304c15f70b914b55334e7529f2b88aaaa30fb3a42dc16c7afa508247f5bb19fd` | 0 |
| obp-api/src/main/scala/code/dynamicentitywebhook/DynamicEntityWebhookEvents.scala | 4475 | `d72a0600d63724c2630ea3baa06b92050e866c1bbf4ec94128d394faedf84e48` | 0 |
| obp-api/src/main/scala/code/dynamicentitywebhook/DynamicEntityWebhookFiring.scala | 6458 | `6eacf9af1a058c8a8d2d880c800b234198b2eada276a9bd898511a128f36d6b1` | 0 |
| obp-api/src/main/scala/code/endpointMapping/EndpointMappingProvider.scala | 3166 | `f45f3bb16c5f70c15b822326353de66b4a0f74c445da6303668134020aa14006` | 0 |
| obp-api/src/main/scala/code/endpointMapping/MappedEndpointMappingProvider.scala | 4827 | `03cdd0d11a65875ecd75884bceb3879621d969f29c68e1869dd10355ebedaaa1` | 0 |
| obp-api/src/main/scala/code/endpointTag/EndpointMappingProvider.scala | 2549 | `2b58f28f6e3b8dd60e57eef7de281d1919109921269b588c4b7b644ace3b3071` | 0 |
| obp-api/src/main/scala/code/endpointTag/MappedEndpointMappingProvider.scala | 3369 | `db4784fbd77b9b4100da7a09bedc3d3143add91bc61cb2ed3d90e30e8e0146c0` | 0 |
| obp-api/src/main/scala/code/entitlement/Entilement.scala | 3578 | `1e487d0a77764249bca2cf6200da98f8325195f2e5c82c0d03b81c71bb69ad11` | 0 |
| obp-api/src/main/scala/code/entitlement/MappedEntitlements.scala | 11436 | `21be9620fdb3ad27052777369382bf519dc92e282e36611e22ef66c78e72222d` | 0 |
| obp-api/src/main/scala/code/entitlementrequest/EntilementRequest.scala | 2514 | `a657981aa2bb276f4b1672b8a1a997abeae4f470ce430fb7913876b41828913b` | 0 |
| obp-api/src/main/scala/code/entitlementrequest/MappedEntitlementRquests.scala | 6010 | `b8af55e55629bb67a3f44b9ab7ef956305ec706459a2d3cf2f8b835cd20cbb57` | 0 |
| obp-api/src/main/scala/code/etag/MappedETag.scala | 1743 | `446ffc7a8294bbe829a1b7dd38bcb897c0f4581c9c77716e6010704f0837a910` | 0 |
| obp-api/src/main/scala/code/examplething/MappedThingProvider.scala | 2248 | `a3b2d44061e9ab244c27a603ab40f4ccc515a7313e28503fba4c74fbc1ea3f4c` | 0 |
| obp-api/src/main/scala/code/examplething/Thing.scala | 2694 | `398d8f26372e45e927efb10d2469214432b64df042300f05467e84c05d03df94` | 0 |
| obp-api/src/main/scala/code/featuredapicollection/FeaturedApiCollection.scala | 1842 | `30216ac3830b62e5753dc4496eb9f5605285d7f7ef7f55b550b54a68522fba1c` | 0 |
| obp-api/src/main/scala/code/featuredapicollection/FeaturedApiCollectionsProvider.scala | 3625 | `b214b6f2aae36303af4d0c4a087947c7fae242b0b484861bcb2a59a61aac4c11` | 0 |
| obp-api/src/main/scala/code/files/Files.scala | 4979 | `bed4e038a0af0487fc6f2cc27a53bf03f3a5eeeff15d27953a8d6c785a9f451b` | 0 |
| obp-api/src/main/scala/code/files/MappedFilesProvider.scala | 9413 | `873091d841db570bde3886a0970fdde503ab005be7a78d03412c50af18e87e70` | 0 |
| obp-api/src/main/scala/code/fx/MappedCurrency.scala | 1762 | `6d09d39efe9473fa8cd17958c8ed60dd77fa89f3fce83da36288e6f32d98f7d4` | 0 |
| obp-api/src/main/scala/code/fx/MappedFXRate.scala | 2111 | `e3c0be7b027d52c7441f37275d52197234fc25f484028b0d078c199b29625ad4` | 0 |
| obp-api/src/main/scala/code/fx/fx.scala | 12669 | `d2a548dd94712846955c9bbfe567b4038eb26acf8712173fb9844147a242a0d9` | 0 |
| obp-api/src/main/scala/code/glossaryitem/DynamicGlossaryItem.scala | 5960 | `a1632ace218de1ee4f7f3a52531299de3cf0fda80ae0b9c52806c9d02bc9d54c` | 0 |
| obp-api/src/main/scala/code/glossaryitem/DynamicGlossaryItemTrait.scala | 3153 | `bd15eb6ae3e77c31423d8b61db473fe7b67488cce86980d112c989b76ca5bc0a` | 0 |
| obp-api/src/main/scala/code/group/Group.scala | 4216 | `6c55da41c7678885aa8cf4cb0f5621823b4c55ae90a9b91d0411ff70ee1a4f18` | 0 |
| obp-api/src/main/scala/code/group/GroupMembership.scala | 4768 | `8fa2f7ec750b22ad08c6d49eaaeda001c091c38252ccb521f17adf94fa2b6e49` | 0 |
| obp-api/src/main/scala/code/group/GroupTrait.scala | 1955 | `4a8af26ec7b085699a768c4fddeb560d77d1f09c316b6fd884c35e2b188d880c` | 0 |
| obp-api/src/main/scala/code/investigation/DoobieInvestigationQueries.scala | 6367 | `0eb3b987a31ad1fe13e9697640c82896b84023d96bac4d7c915b8429cc9bc658` | 0 |
| obp-api/src/main/scala/code/kyccheck/KycCheck.scala | 1494 | `965d63e1c76ddf7732f13a16b3ad83bcde9bf53dc4170c1baa8740afc9009cb5` | 0 |
| obp-api/src/main/scala/code/kyccheck/MappedKycChecksProvider.scala | 3698 | `5b59161dd21670b6feb9d951820c871d637aa9d43cfd5a60a5cff2ecbd4c884c` | 0 |
| obp-api/src/main/scala/code/kycdocuments/KycDocuments.scala | 1509 | `b7ac355402dcbee1e435b779ddbc21d69230ee0be5755c42499fc4b8118a0115` | 0 |
| obp-api/src/main/scala/code/kycdocuments/MappedKycDocumentsProvider.scala | 3680 | `43a86262c9db460f1b34c5d0f25485ffecabef9b670a005bc0656d55eb9f27f2` | 0 |
| obp-api/src/main/scala/code/kycmedia/KycMedia.scala | 1500 | `f116072dd662a004489e83849626dbdebf865f0aceba3a67820fdfbe92fce02d` | 0 |
| obp-api/src/main/scala/code/kycmedia/MappedKycMediasProvider.scala | 3591 | `0f909c10b94a81068500f4d623cfb11e0dc485f887d0e33842ce329a9f14162b` | 0 |
| obp-api/src/main/scala/code/kycstatus/KycStatus.scala | 1417 | `3fa2daf5cbd15aef2360a1bc0fe51505fca332b3da06af74e78badf0926380e4` | 0 |
| obp-api/src/main/scala/code/kycstatus/MappedKycStatusesProvider.scala | 2885 | `b61abc4eaacc43edba0d6a5fc33f3132ceef619d83c73068a3ea69eb9e1d23ea` | 0 |
| obp-api/src/main/scala/code/logcache/LogCacheEventBus.scala | 8489 | `72abed7572405f098e4f22ab2518006a4b4e6476d54719399cab96f1c80f0988` | 0 |
| obp-api/src/main/scala/code/loginattempts/LoginAttempts.scala | 5028 | `e837809e52bd03a9909dd4a0ce9ea9edfbbf26ec2509c0c49c34305c4f5197bd` | 0 |
| obp-api/src/main/scala/code/loginattempts/MappedBadLoginAttempt.scala | 1960 | `d2e88dad5b450479c5a1954c73337e278f8b19b2c430a123a2f4c606d33c798e` | 0 |
| obp-api/src/main/scala/code/mandate/MandateTrait.scala | 16072 | `efe9ee4e88ce4d74b00a69fd90526042b35e7622d41b1ad74ac2e39dec3d3b15` | 0 |
| obp-api/src/main/scala/code/meetings/MappedMeetingProvider.scala | 6689 | `5f295b398953048b56cc3cdf9147e9a549d7fe47614b3b181be4a5f869106549` | 0 |
| obp-api/src/main/scala/code/meetings/Meetings.scala | 1847 | `9e8dd0b375dea7321b36f9e623b866a251c9ff0af54dca61efebd27b657b051f` | 0 |
| obp-api/src/main/scala/code/messageoutbox/MessageOutbox.scala | 9785 | `825a553548d7ebabbedfea1cdc695947b9ee4df6aa7f2c949ff0595e3690c6e6` | 0 |
| obp-api/src/main/scala/code/messageoutbox/MessageOutboxRelay.scala | 13382 | `ac298940996b6a1434e34567417cdf76c869dc8ecbe1478b94a5e4f30c835a8b` | 0 |
| obp-api/src/main/scala/code/messageoutbox/WebhookOutbox.scala | 11923 | `2d2891ef1349cd66f86d5bbda2ad7a9c151cac559cd8fefc6daffe24219b7bb4` | 0 |
| obp-api/src/main/scala/code/messageoutbox/WebhookUrlCheck.scala | 6533 | `3678f8aa60f105889eb596cd87f61d5c016b8a7d3725ac164625be934994e4b5` | 0 |
| obp-api/src/main/scala/code/metadata/comments/Comments.scala | 1971 | `5b2105a1ce91514fb3718af18f713e13b03efa7ece525aba53fb143f394e98c4` | 0 |
| obp-api/src/main/scala/code/metadata/comments/MappedComment.scala | 4588 | `6df14c4c2b2c48409191a5fd1a893cbb91390f64f6c88b51a075e803d195cf1d` | 0 |
| obp-api/src/main/scala/code/metadata/counterparties/Counterparties.scala | 5528 | `9b7a9ca020239da894e42f6936c8727ecc86eee47c8bd2f1c5932a95f212503c` | 0 |
| obp-api/src/main/scala/code/metadata/counterparties/CounterpartyBespokes.scala | 1696 | `3d8f7b68e7262e056a92336e5441848dab6414f8a78428ac3bd8861448f04939` | 0 |
| obp-api/src/main/scala/code/metadata/counterparties/MapperCounterparties.scala | 28483 | `b1592e73e08ac2ce2242c49e58754614687d53093aaa07c97272b6d63a93c721` | 0 |
| obp-api/src/main/scala/code/metadata/counterparties/MapperCounterpartyBespoke.scala | 2255 | `a56f4680889148e70fa60da9733b89d2a3e8a730c3a8ae3bb78ae9156712f95b` | 0 |
| obp-api/src/main/scala/code/metadata/narrative/MappedNarratives.scala | 3426 | `4ccc935c85cd71d919f55e69cd4170bb156d334f30e212fc0bc4888d51da6a05` | 0 |
| obp-api/src/main/scala/code/metadata/narrative/Narrative.scala | 1856 | `1a9051dd8e0dd020c32175fbef5cacc49ac772738e7c4b41b99a645152f60b54` | 0 |
| obp-api/src/main/scala/code/metadata/tags/MappedTags.scala | 5550 | `a28fbe3a7e0789cb4eba2487eb1adbc7398a9dc5ae3a7e8f39a9b783bf23c12d` | 0 |
| obp-api/src/main/scala/code/metadata/tags/Tags.scala | 2321 | `34f42c6de8dbd6fee17d83aac5cb7fe8312ba689235cbbf789bd52ed71a85a44` | 0 |
| obp-api/src/main/scala/code/metadata/transactionimages/MapperTransactionImages.scala | 4918 | `4b63cdf0cb8821d954fb72dd188d17c3c2ccce11b8e64ce412214a670f642e9a` | 0 |
| obp-api/src/main/scala/code/metadata/transactionimages/TransactionImages.scala | 2012 | `434d1b597b7691e0be4e2f10dab424251d0205a94759eb40e947fbfc71144d82` | 0 |
| obp-api/src/main/scala/code/metadata/wheretags/MapperWhereTags.scala | 4789 | `c64bb2be7ffb1c5f143ab7da3c1bf81a80eba9183ac4882d7a9f9b8275033747` | 0 |
| obp-api/src/main/scala/code/metadata/wheretags/WhereTags.scala | 2251 | `c713877831c4bcb28e8d48e89d95ca61a0394b7ec8d9023744524dcdae7b009d` | 0 |
| obp-api/src/main/scala/code/methodrouting/MappedMethodRoutingProvider.scala | 5255 | `e7280be12ddf51052fb35c516fc18d50541238285ee2084464745c46119471cb` | 0 |
| obp-api/src/main/scala/code/methodrouting/MethodRoutingProvider.scala | 4827 | `e14428599dd13c3217389d5c9ac959c408ea126fee4ab8e77a566eb80f3c7420` | 0 |
| obp-api/src/main/scala/code/metrics/APIMetrics.scala | 12719 | `494ef1ca26c65ace51b58d97d77939a17f8d49804774263cafb2d42763d1098b` | 0 |
| obp-api/src/main/scala/code/metrics/ConnectorMetricBatchWriter.scala | 5026 | `db513be229dd9882927d4b9e4c983ec279783a19ab17027d40c52119a145beb7` | 0 |
| obp-api/src/main/scala/code/metrics/ConnectorMetrics.scala | 6048 | `1c2a012a14966f02b38e8eb9370f3f0f8bd98df1e2beb483af8aa399ed1d48ee` | 0 |
| obp-api/src/main/scala/code/metrics/ConnectorMetricsProvider.scala | 2904 | `e8a2d7c01b7be76970ecd1c99cba7e633f66e545bb58176ce4dc71704cab1e63` | 0 |
| obp-api/src/main/scala/code/metrics/ConnectorMetricsRedis.scala | 7760 | `cde05fdb2ce430defe08c813b8e58b92cc12ba90b99f4a24bb4ff37fa9e9fbfb` | 0 |
| obp-api/src/main/scala/code/metrics/ConnectorTrace.scala | 4428 | `f06cb4af612a21369755e65fd7b8a0539a0c07f4f01c8e33d42f5b304b19ec21` | 0 |
| obp-api/src/main/scala/code/metrics/ConsumerLastCall.scala | 3985 | `3582e15fc873cb6d68b9eb3c35a746f0e8e300f372de7a54d77561867e2b5ef9` | 0 |
| obp-api/src/main/scala/code/metrics/DoobieMetricsQueries.scala | 25009 | `9b9caaa9902b37a268700dd941012270946470dc42c67b2392b93d87b8e92bd0` | 0 |
| obp-api/src/main/scala/code/metrics/ElasticsearchMetrics.scala | 5379 | `30875c9e11920ee2482d44895cd70b7df8fd08e0821afc9411f2e6a81bf23199` | 0 |
| obp-api/src/main/scala/code/metrics/MappedMetrics.scala | 46883 | `639454ec01087a6ab11656065bcba7f0e4469f403ed9c45a7d79c3fe53b21fd4` | 0 |
| obp-api/src/main/scala/code/metrics/MetricBatchWriter.scala | 11333 | `5f58c6aaa61f71037592b6feba8ca3c1cef50f03e6845963a4bdb881ab71d75b` | 0 |
| obp-api/src/main/scala/code/metrics/MetricsArchiveRun.scala | 4520 | `54ce34b728b40eba668190ac12c44b0a6aa875a02e7356a8799c52ace45d658e` | 0 |
| obp-api/src/main/scala/code/metrics/MetricsProps.scala | 4209 | `ed8d052014b2f300f6a860c0e809137ea3fb40a46a3d211f8f464e2933bc2a58` | 0 |
| obp-api/src/main/scala/code/metricsstream/MetricsEventBus.scala | 7533 | `cee14a0db9dfb6942b9b5796625b5f260155c5250d5749155474bcebdfa57dfd` | 0 |
| obp-api/src/main/scala/code/migration/MappedMigrationScriptLogProvider.scala | 2217 | `26a39a195e888d366345df19ce86434722b047f7eef5cd1aa2bbb48ed48ac80b` | 0 |
| obp-api/src/main/scala/code/migration/MigrationScriptLog.scala | 2080 | `4a0bc1fbf16e995dbe2ebeb61ced69f227bee63e1dbb73ce39719d715fdd20a1` | 0 |
| obp-api/src/main/scala/code/migration/MigrationScriptLogProvider.scala | 1405 | `22df7477d05bbe346b12e76e5b31f3847e638161dbdfa8a8b2d6dc111199de7b` | 0 |
| obp-api/src/main/scala/code/migration/MigrationScriptLogTrait.scala | 1115 | `d87eb0f58fb3eaca6d9703c7e0c85f1094d046915d11bf599cfb4157db3b8304` | 0 |
| obp-api/src/main/scala/code/model/BankingData.scala | 30988 | `4211afb8a5afd7a70c7cf6437059b21955faf8b8d8a50876b75b456613a91968` | 0 |
| obp-api/src/main/scala/code/model/Metadata.scala | 1605 | `8493e67a88b7d17407fbab97be9191fc26b108ebe069063a23f47fe998a39e70` | 0 |
| obp-api/src/main/scala/code/model/ModeratedBankingData.scala | 15380 | `93dc94546204ea92bc5eb2439b24052dcb9416d1d5fad3d58ad932b17d9143ca` | 0 |
| obp-api/src/main/scala/code/model/OAuth.scala | 34704 | `67b635580ff5c3723adaa62f43d46fd0272675bee4e19e8c4a1001d4cdf82f1d` | 0 |
| obp-api/src/main/scala/code/model/User.scala | 7273 | `0c17e97bdf8836b73b01b76105febb15612ba5daef96215a14902b695bf0e86f` | 0 |
| obp-api/src/main/scala/code/model/View.scala | 33210 | `4e4c97ea67faef4aa3b0bf1d79a7327266dae272896b5174d3d7017a0ba99e12` | 0 |
| obp-api/src/main/scala/code/model/dataAccess/AuthUser.scala | 64499 | `352152ef398c9082a263d236f4bafcea47e093ae2fe794f1ecef6584efd8ac96` | 0 |
| obp-api/src/main/scala/code/model/dataAccess/BankAccountCreationDispatcher.scala | 6643 | `219b6741ea1cbe5cda09e1ba269c43d7342b03e0c328c62d74c0ef5a8a3ba47d` | 0 |
| obp-api/src/main/scala/code/model/dataAccess/BankAccountRouting.scala | 2054 | `006c41bfe5805b9a09280fffa6a23da094ae5f0623963b6531bce218f850e99c` | 0 |
| obp-api/src/main/scala/code/model/dataAccess/DoubleEntryBookTransaction.scala | 3568 | `393eb8eaeb8dc92382bf284e54f50fbeaf56be653e57551ec4b2dfcf0670ccfd` | 0 |
| obp-api/src/main/scala/code/model/dataAccess/MappedBank.scala | 2982 | `3e8f9017d98dd0e7c4583664d063513aa7668ecaa2803e51494c641bd5dd03fd` | 0 |
| obp-api/src/main/scala/code/model/dataAccess/MappedBankAccount.scala | 4027 | `37d7199698bb8a66880ef1d1e612f2eec313dd9f3feb0c8b23e2e549afa42955` | 0 |
| obp-api/src/main/scala/code/model/dataAccess/MappedBankAccountData.scala | 1697 | `c5587e5422b987c1ae0a5d2adc74bc21c7cf6a36ecd6f6ffefa95b8e63a0200f` | 0 |
| obp-api/src/main/scala/code/model/dataAccess/ResourceUser.scala | 7753 | `5f0b269c6a4428683ba918f01658b9dc15967c62046536751df2b2b95ebe5de8` | 0 |
| obp-api/src/main/scala/code/model/dataAccess/UpdatesRequestSender.scala | 2956 | `36724142a8457b128cd678d769c3bc631a51f5072bf12ca5c975698e008edab1` | 0 |
| obp-api/src/main/scala/code/model/dataAccess/internalMapping/AccountIdMapping.scala | 1707 | `cbd0c97f9124f6d535c2354cdcd9c2c432674a690cf8f8c18fbd54cbdb692774` | 0 |
| obp-api/src/main/scala/code/model/dataAccess/internalMapping/AccountIdMappingProvider.scala | 1432 | `ae19c43e799b9d7fe42f57e3a574c1bdf10980ee03a9f02297b4d497e9712b1f` | 0 |
| obp-api/src/main/scala/code/model/dataAccess/internalMapping/AccountIdMappingT.scala | 1871 | `918557aad928d01bcd8581e8fccfb224b42f76a2dcc021bd73cbcf2136d39f66` | 0 |
| obp-api/src/main/scala/code/model/dataAccess/internalMapping/MappedAccountIdMappingProvider.scala | 2670 | `f8bcb2eb5d3ebf12ce3a2cddc2bf950d252f84ec9aa2d0030d2468398ada5b40` | 0 |
| obp-api/src/main/scala/code/model/package.scala | 4329 | `9f229f5e7c1dad333fead7f3a171b5a67013f69a105287c9677740c009c70f49` | 0 |
| obp-api/src/main/scala/code/nonce/NonceProvider.scala | 1879 | `7187ed5a174ffc23aa92a773eae82c2be1f94e64d2f88e41e585992fbd240504` | 0 |
| obp-api/src/main/scala/code/obp/grpc/Client.scala | 2361 | `7a9140bbf862962b6d01b2bf479c5dc3498cbb9e4290d95a6771647f41421526` | 0 |
| obp-api/src/main/scala/code/obp/grpc/ObpGrpcServer.scala | 13758 | `8e345c7dd8db4bceec99cb7cb95609ee0963dbc6d47b5a30992c4b518b5d2cb9` | 0 |
| obp-api/src/main/scala/code/obp/grpc/api/AccountIdGrpc.scala | 4737 | `75a61ee07ce39c79b22c0c5436bb83e5ce9f6a191eb460177ab9e9ecb0e0e6a5` | 0 |
| obp-api/src/main/scala/code/obp/grpc/api/AccountJSONGrpc.scala | 8956 | `230cf9d1d68e59f4acd8df4414c10eb5a46d18d8af5ed865649079508db3deb0` | 0 |
| obp-api/src/main/scala/code/obp/grpc/api/AccountsBalancesV310JsonGrpc.scala | 35150 | `b881c51aa6de006b8e4b798b8815e6426243c655548e088171894e08c8b68320` | 0 |
| obp-api/src/main/scala/code/obp/grpc/api/AccountsGrpc.scala | 5793 | `4a40d8f0da0c99d3cf5088988a736da9243a926babd51e8448f00f75f50056bc` | 0 |
| obp-api/src/main/scala/code/obp/grpc/api/AccountsJSONGrpc.scala | 5802 | `ed830458551c62ba32f8f740d59aa705f26a3495fc1658a0e2c7f4d6550a5fec` | 0 |
| obp-api/src/main/scala/code/obp/grpc/api/ApiProto.scala | 13878 | `242cce385285af8494fc177ad870b0e72147bd2b1b3e42ccae7c4871b6aa0bf5` | 0 |
| obp-api/src/main/scala/code/obp/grpc/api/BankIdAccountIdAndUserIdGrpc.scala | 7157 | `c8a7404ab312106976957322ea5a40ddc54ec42f0192126f089da73225462b7c` | 0 |
| obp-api/src/main/scala/code/obp/grpc/api/BankIdAndAccountIdGrpc.scala | 6003 | `f4ebf562fbb0aa42d8609c181ce140aa52e4b5235bac6703bee49edda6e2e410` | 0 |
| obp-api/src/main/scala/code/obp/grpc/api/BankIdGrpc.scala | 5705 | `34daf3d59a3b6c3bff352d6269f141cc54bc4e8c02c397a86bacfbe6587063d5` | 0 |
| obp-api/src/main/scala/code/obp/grpc/api/BankIdUserIdGrpc.scala | 5836 | `837527fd8fa0330da1338d19a7ebfa05c152683a06bbdcf700c3eca2e527fd9f` | 0 |
| obp-api/src/main/scala/code/obp/grpc/api/BanksJson400Grpc.scala | 24275 | `68a027ac4d95f17a9acda421444350e687c6aa9f0dc61078e2395d49db07b9f2` | 0 |
| obp-api/src/main/scala/code/obp/grpc/api/BasicAccountJSONGrpc.scala | 16638 | `ceecc4060c70f9f0a1294923d3dea2dcf3644b6355187aaccb50ced68e8ea82a` | 0 |
| obp-api/src/main/scala/code/obp/grpc/api/CoreTransactionsJsonV300Grpc.scala | 84167 | `32d3cbfa7d243312da2807b4886ad2b316bc294710cb4386f810d267134808a5` | 0 |
| obp-api/src/main/scala/code/obp/grpc/api/ObpServiceGrpc.scala | 11833 | `1378c735b83be1c0827bf977273a48f9f5cb7b3703403f11665ca43fd531ea33` | 0 |
| obp-api/src/main/scala/code/obp/grpc/api/ViewJSONV121Grpc.scala | 85204 | `3ed36494dfb3b0fd43ab2b5ab44ca4c411f6d250d87579af2db9605985141992` | 0 |
| obp-api/src/main/scala/code/obp/grpc/api/ViewsJSONV121Grpc.scala | 5754 | `515ba7e6d44ccb3a910c9bd2beb5330f5a77780800732547dcad88690c83d0e2` | 0 |
| obp-api/src/main/scala/code/obp/grpc/chat/AuthInterceptor.scala | 5644 | `38f3e4ee9429cc6bbd148988df757d63b56614c65698e1cd5f033c35353b6102` | 0 |
| obp-api/src/main/scala/code/obp/grpc/chat/ChatStreamServiceImpl.scala | 13382 | `250e4ecfadbc55fa89a75c9d6c2ff8db2f9446612e3fe8de2a64d586e05dd855` | 0 |
| obp-api/src/main/scala/code/obp/grpc/chat/api/ChatMessageEvent.scala | 24168 | `04de66e6ebd06fd0f5e1243d71bf1fc71b7515a939f4b59dc9b65ebdbd1d7d91` | 0 |
| obp-api/src/main/scala/code/obp/grpc/chat/api/ChatProto.scala | 6724 | `bc3546d08ef3b77a6cf1851e83be43f714e5313e02e167022a11da2b5bd8b0f6` | 0 |
| obp-api/src/main/scala/code/obp/grpc/chat/api/ChatStreamServiceGrpc.scala | 7420 | `db359a56adc55f9c0677e35cdab2e4a2b8ed4c2290d2e0773e55c2ae1bf6b927` | 0 |
| obp-api/src/main/scala/code/obp/grpc/chat/api/PresenceEvent.scala | 8016 | `f559edc207e8e584d34dbb498be513511c51166b0b51f0bddf3ca8aef7a54a1e` | 0 |
| obp-api/src/main/scala/code/obp/grpc/chat/api/StreamMessagesRequest.scala | 5068 | `f0f5fa8240066e00b2f80f3793dbe4662082923d3d8af74afdc3df440a9967cf` | 0 |
| obp-api/src/main/scala/code/obp/grpc/chat/api/StreamPresenceRequest.scala | 5068 | `c56dbf94074ee8d293395085fa309f93942bfd102ef275a6a364d0fa403f37f8` | 0 |
| obp-api/src/main/scala/code/obp/grpc/chat/api/StreamUnreadCountsRequest.scala | 4097 | `14069a349dd053a2cae9d7ab6976eb08fcec54c3f5f7a44e17aef1a8846222a6` | 0 |
| obp-api/src/main/scala/code/obp/grpc/chat/api/TypingEvent.scala | 5928 | `38477e2960a2404056f1408a104bb112542300ceed9ea4622ca71064023b1261` | 0 |
| obp-api/src/main/scala/code/obp/grpc/chat/api/TypingIndicator.scala | 9153 | `a85402e61aa54cea825b794cb6b9e1f4fad1808f16fba5aed0e08cfde31fed6e` | 0 |
| obp-api/src/main/scala/code/obp/grpc/chat/api/UnreadCountEvent.scala | 6041 | `6a1608989a7fef245d0f346186fc193b2bff3a857bfb1253ea4e8abe9aba3fc8` | 0 |
| obp-api/src/main/scala/code/obp/grpc/logcache/LogCacheStreamServiceImpl.scala | 4712 | `3db206d90bde2333269ee578ab3aadff7ca1eb75bc5e4434479b8bf0495e61b3` | 0 |
| obp-api/src/main/scala/code/obp/grpc/logcache/api/LogCacheEntry.scala | 9965 | `0a7b5e10024ce6ca9e13599062e4a30557c9be8f3820ea19f013be0ac4e99606` | 0 |
| obp-api/src/main/scala/code/obp/grpc/logcache/api/LogCacheProto.scala | 4199 | `0dba112bd9b212985f7e76a249fda13619a75398958163e0bcce371eb4cd3f2a` | 0 |
| obp-api/src/main/scala/code/obp/grpc/logcache/api/LogCacheStreamServiceGrpc.scala | 3871 | `9b2eafd4ebb19afba2a76ffbc49cfab16b4eafae6521feff9f062bda70a7133f` | 0 |
| obp-api/src/main/scala/code/obp/grpc/logcache/api/LogLevel.scala | 2200 | `29aaf4b4b2b7ca6924721258146df8bc5a4b2116c8f298b34cd5f2de1a2b5fe5` | 0 |
| obp-api/src/main/scala/code/obp/grpc/logcache/api/StreamLogCacheRequest.scala | 6004 | `ed02ee32bc021858c143ca896dbda5d3d2dbcbb5fd8c5959d3488cd48d27af4b` | 0 |
| obp-api/src/main/scala/code/obp/grpc/metricsstream/MetricsStreamServiceImpl.scala | 7001 | `d00635527403342ca2763494c0e8bc3d170c37f70eeb9c301f8154f12e935e6b` | 0 |
| obp-api/src/main/scala/code/obp/grpc/metricsstream/api/MetricEvent.scala | 28631 | `d331e45fa38d9194f2fb03bde39665d410793ba0e552616b37ab01b3cecc02da` | 0 |
| obp-api/src/main/scala/code/obp/grpc/metricsstream/api/MetricsStreamProto.scala | 4456 | `b69bf5b4b2704c1356e1318ff68815c6c739426a73230ca6b3bff7b92facea15` | 0 |
| obp-api/src/main/scala/code/obp/grpc/metricsstream/api/MetricsStreamServiceGrpc.scala | 3814 | `c7e2f1f8963a5e8c241ea088a6004a5d0742ca7573042cc8685012f545a82d58` | 0 |
| obp-api/src/main/scala/code/obp/grpc/metricsstream/api/StreamMetricsRequest.scala | 12431 | `f62ed9b6a0102ae98d6d95b0d578b063377635ff65a7af2d9017febabce6c10c` | 0 |
| obp-api/src/main/scala/code/obp/grpc/signal/SignalChannelsServiceImpl.scala | 10279 | `62e134bfa7e63960dd21aa7f1eb61fbc2423a1d83cfd7246e2a02e0f609a0eea` | 0 |
| obp-api/src/main/scala/code/obp/grpc/signal/api/FetchRequest.scala | 8872 | `e20e1bd0e0816b70cdcf8a13a9fbc46d2d76f8d7b28265963a6e3154fba014f4` | 0 |
| obp-api/src/main/scala/code/obp/grpc/signal/api/FetchResponse.scala | 13290 | `6530b6fcda047a7c2d74cb198f7bd0ea1dca41b885e76e77fe011a51115a7ac4` | 0 |
| obp-api/src/main/scala/code/obp/grpc/signal/api/ListChannelsRequest.scala | 4955 | `fa9488df659c6f476fcb8bd87b3d4e6ffe7cd2948fe47d7e0373c22b0dd8403f` | 0 |
| obp-api/src/main/scala/code/obp/grpc/signal/api/ListChannelsResponse.scala | 7193 | `d23fa7a0e404d0fc32608a55f1ffee5f2b27962fb1d2ad39fa4c3b3596157033` | 0 |
| obp-api/src/main/scala/code/obp/grpc/signal/api/PublishRequest.scala | 9193 | `b21b0dbdc46c995ed0d658d8a188cbc7542e62c6385b5dfd58189d92863a3913` | 0 |
| obp-api/src/main/scala/code/obp/grpc/signal/api/PublishResponse.scala | 11211 | `bde4b1bf54b1ba670210e7ee2a11a13a4dcdc1dcd67b477f339a59cfcae3453b` | 0 |
| obp-api/src/main/scala/code/obp/grpc/signal/api/SignalChannelInfo.scala | 8134 | `0cb5132957781878c6e74ad9fa6c794b9f74fbde421419192668f0dfa3ccb4e0` | 0 |
| obp-api/src/main/scala/code/obp/grpc/signal/api/SignalChannelsServiceGrpc.scala | 10487 | `dd9e4090e4e922b270b1fbef161456ada9c65d0b95361fe502b025771a703b66` | 0 |
| obp-api/src/main/scala/code/obp/grpc/signal/api/SignalMessage.scala | 15404 | `e6cf4f1040588073247942318379eb00df0c71a6cba0e5196499d55866327b72` | 0 |
| obp-api/src/main/scala/code/obp/grpc/signal/api/SignalProto.scala | 7385 | `20e4ff59c21520c0654046db99db1e44e3b3434437cdfcf45bfff9f1a8951568` | 0 |
| obp-api/src/main/scala/code/obp/grpc/signal/api/SubscribeRequest.scala | 6072 | `079a5cf66655ccfe5c0e06e9c7493c0e846276635ad5af268c8eacad35b17ac0` | 0 |
| obp-api/src/main/scala/code/opencorridorfees/OpenCorridorFeeAccrual.scala | 5016 | `2f2105ff862fa43185489aef30d2af9de7216d6abba8728c07a8ef74ffd41e2b` | 0 |
| obp-api/src/main/scala/code/opencorridorfees/OpenCorridorFees.scala | 5814 | `dd3c9352dffb6035081998cc5853f947d1748769d4c6c1646486161005b6d531` | 0 |
| obp-api/src/main/scala/code/organisation/Organisation.scala | 4377 | `241b07fbc997f512d8f639f66c84fc61e7ec1fa6cb5ce570b0130173f40d0f5e` | 0 |
| obp-api/src/main/scala/code/organisation/OrganisationTrait.scala | 2129 | `ff5bdecf74ab9477b33010e630aa7601522540e77009406c13864c8f1d802465` | 0 |
| obp-api/src/main/scala/code/payeelookup/PayeeLookup.scala | 4617 | `9938d38dca1c0d635c2eb7f07084889cf6eb84105e93c9e57ee8ab57e658e3db` | 0 |
| obp-api/src/main/scala/code/payeelookup/PayeeLookupTrait.scala | 2325 | `110b5b8e1ab7aef4f7721dc7981cc7e18c43f5297f43316cf27f53f6289a722a` | 0 |
| obp-api/src/main/scala/code/paymetngateway/StripeExample.scala | 1914 | `4fe4c8e066ff25a01663e2612dab5f712e54bbdd9e6d1362f1a4bd11c04d081b` | 1 |
| obp-api/src/main/scala/code/platformapp/PlatformApp.scala | 3169 | `024420b177ac9c537371b5f93a421ca327ebb13c44f2ba727b9f8815dca02eb9` | 0 |
| obp-api/src/main/scala/code/platformapp/PlatformAppTables.scala | 6141 | `41f309a2b259f79edea374a6f1fe51833341ae359ab45715154c7eca0cbe9157` | 0 |
| obp-api/src/main/scala/code/productattribute/MappedProductAttributeProvider.scala | 5217 | `84242ae4814713ae7b23a3ef6eba29521d8943f484e1c855a0d0b767372e9c8a` | 0 |
| obp-api/src/main/scala/code/productattribute/ProductAttribute.scala | 2578 | `b058fafcab59d4396886aeecb16fea0d7cbce16faab0915125bc7847403d0b54` | 0 |
| obp-api/src/main/scala/code/productcollection/MappedProductCollection.scala | 2872 | `9cce25104b4cc9c6b4e126a5d618a37fe535d5c6ef822fbc2f7638b4ae18c79b` | 0 |
| obp-api/src/main/scala/code/productcollection/ProductCollction.scala | 1532 | `28f5f945c0c6e6e2fc37f5b834a7e1f66908b0cbff945cdd56e89b60545413b5` | 0 |
| obp-api/src/main/scala/code/productcollectionitem/MappedProductCollectionItem.scala | 3869 | `f4c9bdaf0f1fdc8a4f1ff2fc22ae489357d810e1c2c5619d57c3912b2512d654` | 0 |
| obp-api/src/main/scala/code/productcollectionitem/ProductCollctionItem.scala | 1796 | `1a12e1f50d1a08d8984c545c7fb0f8ce8ef9cd2058c74ab6cc670927fcda0a16` | 0 |
| obp-api/src/main/scala/code/productfee/MappedProductFeeProvider.scala | 4993 | `7e500c07a7e255b609516e2d2d748dafdd071c486f2d269aaf517486401807b7` | 0 |
| obp-api/src/main/scala/code/productfee/ProductFee.scala | 2206 | `6328ac3c1eaea5e04fe7ae0cc2581d84163e381112ea95f5f6b50ad05663f1da` | 0 |
| obp-api/src/main/scala/code/products/MappedProductsProvider.scala | 3599 | `43bfd57b23030de535c4d1ff6bfeea9b4287139a69789e5da539fa154d899de7` | 0 |
| obp-api/src/main/scala/code/products/ProductTag.scala | 3950 | `ccf5f8c44b8fa93e4b5e1e70c9aee43d3b7cf075847fcabe65eb6b5079c8ce56` | 0 |
| obp-api/src/main/scala/code/products/Products.scala | 2365 | `bea57294841db0a978de36af71a754d1aeabd76fde5d208c0c14c665026df267` | 0 |
| obp-api/src/main/scala/code/ratelimiting/MappedRateLimiting.scala | 16334 | `157770a1496e3ae6996ecf60fe8c4eac8332b05ad8bb1a5745987bb33faa08d7` | 0 |
| obp-api/src/main/scala/code/ratelimiting/RateLimiting.scala | 4505 | `3336518c870b3511b998db4c9b45a5d8ee96eb93d9d0dfb30bd9dc1f751f3118` | 0 |
| obp-api/src/main/scala/code/refreshuser/MappedUserRefreshesProvider.scala | 2933 | `60b61c9cd19a0a52a76a3db000d1b3065cc90b0c78848681b6da5f8a682acde3` | 0 |
| obp-api/src/main/scala/code/refreshuser/UserRefreshes.scala | 1508 | `23249b60fc0d27567c21302548a04c125655f9eb3f1c8fb7d950766a3db39009` | 0 |
| obp-api/src/main/scala/code/regulatedentities/MappedRegulatedEntitiyProvider.scala | 6083 | `2e9f06b5b04070305f393fbacd2fb5b4acef3eac521e354b6e57b18815540c42` | 0 |
| obp-api/src/main/scala/code/regulatedentities/RegulatedEntity.scala | 2257 | `041673a02f6e5f4b64737ed4baefd766ccad7bb4813a3930a775839319a4a19b` | 0 |
| obp-api/src/main/scala/code/regulatedentities/attribute/MappedRegulatedEntityAttributeProvider.scala | 5069 | `3c6c56832426c7e8e58e22a5e848bf7d2d801e1bf563fb8d04453a31393c4bed` | 0 |
| obp-api/src/main/scala/code/regulatedentities/attribute/RegulatedEntityAttribute.scala | 2468 | `c5380cbc7bbd44679530bbd5c76cd438edb28d3e25540a17481ae657c7cff009` | 0 |
| obp-api/src/main/scala/code/routingscheme/RoutingScheme.scala | 10889 | `8e0cb3d68c9d48074d29e820e347d6f0a999151edbb4b046e23b86643dfc77fd` | 0 |
| obp-api/src/main/scala/code/routingscheme/RoutingSchemeSeed.scala | 6144 | `dccc19346db2004c3d03ba06cd6a4ef4a18fada76bbb9538d69420f37c30df0e` | 0 |
| obp-api/src/main/scala/code/routingscheme/RoutingSchemeTrait.scala | 3159 | `9dd1e17d8e772e27d89949ccc6a55e0356c92719d95924f49e1870ff6dfce5b9` | 0 |
| obp-api/src/main/scala/code/sandbox/CreateOBPUsers.scala | 2410 | `c6d7c0cf0624c53d9aa606921421cff42b30cb349a45e78b1b3386f898bb28f9` | 0 |
| obp-api/src/main/scala/code/sandbox/LocalMappedConnectorDataImport.scala | 11063 | `65728519ab06c0918c83f8bbdc4ec2ca7db57cf6c4598b581b0e88937eae478d` | 0 |
| obp-api/src/main/scala/code/sandbox/OBPDataImport.scala | 35994 | `567ad0163c249219459cfec76b33a2b2223854d4a50f676fdbeb06ab6b9d4374` | 2 |
| obp-api/src/main/scala/code/scheduler/ConsentScheduler.scala | 11696 | `687157026d6c15904976b33d78298109ffe3d2e73b6a9f73035e1da8aca775fe` | 0 |
| obp-api/src/main/scala/code/scheduler/DataBaseCleanerScheduler.scala | 3860 | `3fb30082331659511714ccca6c72595eb70820b5895fe225682f14df98c34ab4` | 0 |
| obp-api/src/main/scala/code/scheduler/DatabaseDriverScheduler.scala | 2479 | `7352028d2d858cd5a7748d4b427c5e5b36c1cc3c82a5f0c807a0491fbd0e63fb` | 0 |
| obp-api/src/main/scala/code/scheduler/JobScheduler.scala | 2414 | `1825b9bb22d891baf7841d325a2a91ce6f9b0a95af615056f0687ae65f1d071b` | 0 |
| obp-api/src/main/scala/code/scheduler/JobSchedulerTrait.scala | 1008 | `3a1bd60fad60ffe6df1ea2f7ce26a806aef479f582152dca8ff6938d7e7a9e04` | 0 |
| obp-api/src/main/scala/code/scheduler/MetricsArchiveScheduler.scala | 12697 | `9cc85d5703f487440295a21841083a5f059e12a660b0e24d72bf20c5c14c9b2c` | 0 |
| obp-api/src/main/scala/code/scheduler/SchedulerUtil.scala | 1771 | `7b16ae6613b07bb197161d65497b88ddcba2e74566a0e5cdca6d10e09e44e7c4` | 0 |
| obp-api/src/main/scala/code/scheduler/TransactionScheduler.scala | 3075 | `1da08352c093573474f2eb7f5a8d7629f41f5677e9077f09b9e1adb592f7f804` | 0 |
| obp-api/src/main/scala/code/scope/MappedScopesProvider.scala | 3894 | `0214c94d76e00dd88eb33a508cb7697aedc89742a55618d63e39382bf69916f6` | 0 |
| obp-api/src/main/scala/code/scope/MappedUserScopeProvider.scala | 2599 | `c613e2ec2f0d8282245a940764a0e2506cc2766d632143c427811f0be7072ac2` | 0 |
| obp-api/src/main/scala/code/scope/Scope.scala | 1769 | `431ccfaff21d23a67788aa6edcb81b80d4f7aa9298efbd9234c7977e74131976` | 0 |
| obp-api/src/main/scala/code/scope/UserScope.scala | 1545 | `144658cc3c6d590227a5b568a07705362a48c0154980b212e7198f5840633eee` | 0 |
| obp-api/src/main/scala/code/search/search.scala | 12592 | `83fc6ebeb64320b691a74f91b85eb90d61b459df02ab5f72de17442e8a2f7ea4` | 0 |
| obp-api/src/main/scala/code/signal/SignalChannels.scala | 6300 | `dbf72e493c4a68d8bfab696350b5932c0c7a562cb6390c63abc471948289b4a5` | 0 |
| obp-api/src/main/scala/code/signal/SignalContentPolicy.scala | 2695 | `b1c207dba44b3e08599c7aae3a9cb66d22613350a28411239688d68276dc307a` | 0 |
| obp-api/src/main/scala/code/signal/SignalEventBus.scala | 5253 | `5d9137e69470d9504bd0cecc57ce99a4b408fb587c96b65f331f6cd3b540c396` | 0 |
| obp-api/src/main/scala/code/signingbaskets/MappedSigningBasketProvider.scala | 6667 | `e1016148048dbbabcca731f89292f9dbca8a7b770db8f03846bb5efa9866f784` | 0 |
| obp-api/src/main/scala/code/signingbaskets/SigningBasket.scala | 2299 | `82a1a0980433c093fd703b37292af0041fda18a20e416b0cf21167dab7e41000` | 0 |
| obp-api/src/main/scala/code/socialmedia/MappedSocialMediasProvider.scala | 2600 | `95ae9fa4a878f4b2268fdbe6fd9178d96ac201b605a53e99610f5af1d3c72830` | 0 |
| obp-api/src/main/scala/code/socialmedia/SocialMedia.scala | 1648 | `fc8459daec8bfa22c81ec3e2b9314a85d29b8fe4705ead8510984dce82f19242` | 0 |
| obp-api/src/main/scala/code/standingorders/MappedStandingOrder.scala | 5145 | `478dc82d9c38e5ad0b50b80ec2b16c1055f742b80fd3f1448e1c35300c1d8009` | 0 |
| obp-api/src/main/scala/code/standingorders/StandingOrder.scala | 2042 | `332f710f7e8dfa5c146bd7b5e959f4f484adda1ecf37833a338636f09675c234` | 0 |
| obp-api/src/main/scala/code/taxresidence/MappedTaxResidence.scala | 3422 | `11ff5393d96292d38e67bd0ea10708de31a1402e24259b93b5ed16b1d858b44c` | 0 |
| obp-api/src/main/scala/code/taxresidence/TaxResidence.scala | 1533 | `72464187a712a0dbec4d71e15cc793a2378f51133c5fac9a6994f76bbe97cb37` | 0 |
| obp-api/src/main/scala/code/telemetry/BatchWriterTelemetry.scala | 2717 | `f1414a9c43dd3d77e8dfd4eeb8c8499f34519cec979b3ab0cf3cef8e9c05792e` | 0 |
| obp-api/src/main/scala/code/telemetry/HeavyHitters.scala | 5159 | `c2f25b0acce4a463ac4ce05bfff0db61d74beb0eea0a10bbbac20a6d0b3fb641` | 0 |
| obp-api/src/main/scala/code/telemetry/Telemetry.scala | 12120 | `9ab58af33cbf4d15c2ba3ccd12303805a2a5f9f7438ad923329dd538f32f7999` | 0 |
| obp-api/src/main/scala/code/telemetry/TelemetryBindings.scala | 3902 | `6392dbc2615983c0630b94f4f70ef26bbd2e175a61d79e3ac2e6ae438d7cf133` | 0 |
| obp-api/src/main/scala/code/telemetry/TrafficSources.scala | 11641 | `275290f750e41d589d3d5091888966151247641fcbaf82b5d40113d4dfb13e2a` | 0 |
| obp-api/src/main/scala/code/tesobe/CashAPI.scala | 1149 | `78340ce71d24b205a382c85e06c4689447c9a3420ec8f51f3e1d60a09d87b63a` | 0 |
| obp-api/src/main/scala/code/token/MappedOpenIDConnectToken.scala | 2933 | `d43de844f6639e7a1b6af0bc65249ecaf6c872e863f8dd5b871ad40726c2e6c7` | 0 |
| obp-api/src/main/scala/code/token/OpenIDConnectTokenProvider.scala | 1763 | `e0dbaa7053edcada0a9d9717a8f217736851b9663ccad7c6b4eb810f735cb702` | 0 |
| obp-api/src/main/scala/code/token/TokenProvider.scala | 2163 | `87ffa576db9de77611cc83c6799cab5c3981e33beed84c65a5397ca42aa40f1f` | 0 |
| obp-api/src/main/scala/code/transaction/MappedTransaction.scala | 13875 | `fa6287e674e8b3b469e0b58cb64d96220114e818a264caeed02ddcd33f7e70b0` | 0 |
| obp-api/src/main/scala/code/transaction/internalMapping/MappedTransactionIdMappingProvider.scala | 2751 | `290437a4c94f24dfb7f728d90f74a9087b23f2f18555a10e015d827a07a438b5` | 0 |
| obp-api/src/main/scala/code/transaction/internalMapping/TransactionIdMapping.scala | 1822 | `5bd1a2f7bd853250f1aabfdfeaca9e54da0c2c8ff03b80b04f29bdb7e3e35995` | 0 |
| obp-api/src/main/scala/code/transaction/internalMapping/TransactionIdMappingProvider.scala | 1465 | `8e44dc69047366d7ee13dccd7d1ceea574d399c3f319848ededdcfdcc5e567e7` | 0 |
| obp-api/src/main/scala/code/transaction/internalMapping/TransactionIdMappingTrait.scala | 1878 | `d5f997aa6f4c28af973b6b01be1a6419202f9a7aa62a6436eeed03531c4f65b6` | 0 |
| obp-api/src/main/scala/code/transactionChallenge/ChallengeProvider.scala | 2734 | `64b9d70fa1d7ac3c261faaeff5faa3a36dc921aee4ea9f13bfcb6b779d5bea7c` | 0 |
| obp-api/src/main/scala/code/transactionChallenge/ChallengeTrait.scala | 1324 | `4ea7f22dd9e3ca946db4f8e31144d8491ba2bb0a82f424d670183eafe839ca06` | 0 |
| obp-api/src/main/scala/code/transactionChallenge/MappedChallengeProvider.scala | 7480 | `3b5973160431bc4859bfe886cc11c8f812c71a652d471af795b6d888ebaa434a` | 0 |
| obp-api/src/main/scala/code/transactionChallenge/MappedExpectedChallengeAnswer.scala | 3949 | `75f5e20da3424b8647b4a203a48cfb971521bd6cbd117b942c54c6974c953702` | 0 |
| obp-api/src/main/scala/code/transactionRequestAttribute/MappedTransactionRequestAttributeProvider.scala | 8164 | `8f7f269d5d4c77c1157202b91c227c412a9e03947621017d4d1827be702ae1bd` | 0 |
| obp-api/src/main/scala/code/transactionRequestAttribute/TransactionRequestAttribute.scala | 2929 | `a25b6a441fbd095552ee7b7a58083c7408621ad52a2c5e26ae02fbe448db817a` | 0 |
| obp-api/src/main/scala/code/transactionRequestAttribute/TransactionRequestAttributeProvider.scala | 3418 | `76ea40de25d7d0419097d3eeafd5efd307972a7a5923cf578aa1dc3bfa67c33c` | 0 |
| obp-api/src/main/scala/code/transactionRequestAttribute/TransactionRequestAttributeX.scala | 1589 | `1e5eaa93ae400ba4afed1d9e42e263db4589bdb4c929fd3fa0e953787a306b44` | 0 |
| obp-api/src/main/scala/code/transactionattribute/MappedTransactionAttributeProvider.scala | 9524 | `85024d67fffeced93ca620c267273b57a370d5558ba29bdb46ba69a6acb27366` | 0 |
| obp-api/src/main/scala/code/transactionattribute/TransactionAttribute.scala | 3578 | `5780e14809f8ca15775b4eed2c93e4cd30921d2be45df39484fa408a768840c2` | 0 |
| obp-api/src/main/scala/code/transactionrequests/MappedTransactionRequestProvider.scala | 28030 | `dd39c982e71f99d2a6d47eba3dd1941590a14b2024b0a4aeced11d7cec8328f9` | 0 |
| obp-api/src/main/scala/code/transactionrequests/MappedTransactionRequestReasons.scala | 2210 | `f7c10b7875f4a8b4bc277ce37fe3011220e6c69b8d7455bf1ff26e742ff2ca40` | 0 |
| obp-api/src/main/scala/code/transactionrequests/MappedTransactionRequestTypeCharge.scala | 2872 | `70dd42484407b780ad34da5ed4458501d0c8645b31a15a19e38309c7565b55c7` | 0 |
| obp-api/src/main/scala/code/transactionrequests/TransactionRequests.scala | 5480 | `cb2116355d98f59160f47860c73e3610b1f55eb384dac4152cddff6aefab4ae7` | 0 |
| obp-api/src/main/scala/code/transactionstatus/TransactionRequestStatusScheduler.scala | 1783 | `edc5fa01034d203d80de7dfe084887c406b9ef8cd871d9074aeb7866581f26b2` | 0 |
| obp-api/src/main/scala/code/transactiontypes/MappedTransactionTypeProvider.scala | 5445 | `65e5f7ece22f933de1ca732022cf2825a0d123003a09b1ab143eb43e6ee2b9e3` | 0 |
| obp-api/src/main/scala/code/transactiontypes/TransactionType.scala | 3937 | `f6a3ef944c3f4c5272dbf8241ec9c66e4b2b3f9f05dfb7c5ec6a304644c2402f` | 0 |
| obp-api/src/main/scala/code/usercustomerlinks/MappedUserCustomerLink.scala | 6796 | `5f62c71ebd53009de910892e129a1ffc4a2341f9c7a479428a7d5eb1c1ebdf12` | 0 |
| obp-api/src/main/scala/code/usercustomerlinks/UserCustomerLink.scala | 2200 | `4f428e60059baf88f11c2acc52cbf90a735369807e5401b042d6874c75a86136` | 0 |
| obp-api/src/main/scala/code/userlocks/UserLocks.scala | 1647 | `3e8771391ba9cc306b0ece5779e07fe6ea7232c4cb309c724886d98850eaf2c9` | 0 |
| obp-api/src/main/scala/code/userlocks/UserLocksProvider.scala | 2481 | `5e6f7504b7cb00dba044bc117df736eb839c7f93119342e14461032b2b2635ea` | 0 |
| obp-api/src/main/scala/code/users/DoobieUserQueries.scala | 9201 | `48bd45c9fc4698b3813a22d21af8fa2a3f8a277f6a1262de4961b0d5bdc60416` | 0 |
| obp-api/src/main/scala/code/users/LiftUsers.scala | 31072 | `608c2c2c3bd86cfeb3288dd425b1eb9670464766ac67ed4bac1f682b0e2448ef` | 0 |
| obp-api/src/main/scala/code/users/MappedUserAttribute.scala | 5000 | `bcd13569c2c998a818a255564cb5b0c98549cc34840bd70321952f4d4f163b24` | 0 |
| obp-api/src/main/scala/code/users/UserAgreement.scala | 3055 | `250068959dc48f6afa1f94fedb75e135d51bbe8b888726888d3a17a757f74ab0` | 0 |
| obp-api/src/main/scala/code/users/UserAgreementProvider.scala | 1606 | `ce09bf667f83ce0f50b8cd45d725beee44702681c630fe2fa4aca8da9bd2c845` | 0 |
| obp-api/src/main/scala/code/users/UserAttributeProvider.scala | 2460 | `92a4477561debf970ecb1e637397863b583ef403877282d45c0b4934770d785e` | 0 |
| obp-api/src/main/scala/code/users/UserInitAction.scala | 1827 | `af5b7fff8159851a5517f3f9333be52077cd2e780362fcb06e91c4654a8042d3` | 0 |
| obp-api/src/main/scala/code/users/UserInitActionProvider.scala | 1712 | `3f91632b3a16cb10fd4a4c1c501ba7f0022abeaf45b16d4073ad8473752a1303` | 0 |
| obp-api/src/main/scala/code/users/UserInvitation.scala | 4726 | `955f73283a830f65c6251ffa2bb4b10268c108af7bb2fbf4c39e9fc55e4cf615` | 0 |
| obp-api/src/main/scala/code/users/UserInvitationProvider.scala | 2038 | `1df9aa07e3baadcfbd2f670cbb8a8365b85bad071fc04a39a093a4be4cd16a6d` | 0 |
| obp-api/src/main/scala/code/users/UserReference.scala | 41252 | `8d46a93c472cee5af666b0334e0551aa652f2839a369a63bafbe61e4a4b85152` | 0 |
| obp-api/src/main/scala/code/users/Users.scala | 8276 | `1e3bbd38786e04ae6a31c4aa7d498e1b262b48f5cbaa48469f5a0ac79fcf98d4` | 0 |
| obp-api/src/main/scala/code/util/AkkaHttpClient.scala | 5875 | `d449f58e8acf05f768b72bfa06e8c445b423fc6d9091ef722d19cfe8961ab409` | 0 |
| obp-api/src/main/scala/code/util/AttributeQueryTrait.scala | 4184 | `7be5c83b933ec78eca1b5c85fe08c3794a605e110b4478835b3649054f89cdd2` | 0 |
| obp-api/src/main/scala/code/util/BankNameGenerator.scala | 7042 | `69a98487f40674fc886e711e8aefd441d8a1526a662ae18bb1f7dcd2faa05fd5` | 0 |
| obp-api/src/main/scala/code/util/ClassScanUtils.scala | 4867 | `f268e2ae1f70725ba67c24c46e513ffe37b4a61a5995cd6965b6e12fec7b4f58` | 0 |
| obp-api/src/main/scala/code/util/DangerousCharacters.scala | 1965 | `5f1b94384aa1aa8c55b8b71a06fbc5c4b519a07d18cb1bbd1aaf7bc6729a982e` | 0 |
| obp-api/src/main/scala/code/util/DatabaseConnectionHoldWatch.scala | 9347 | `5bdcd02de6f012058600cb348f4435d7878df543e9dd1d6e7341c05b6612c8f3` | 0 |
| obp-api/src/main/scala/code/util/DefaultStringField.scala | 1166 | `d742a8004b45a9fdc896985657ae845704d588f7648a57e816410505039f95ea` | 0 |
| obp-api/src/main/scala/code/util/Helper.scala | 33173 | `6ffb498bef4aac4fff7c29b49e167abc3c1e2d6fa4036c3d7ba0a5be28791528` | 0 |
| obp-api/src/main/scala/code/util/JsonSchemaUtil.scala | 8825 | `49709345fe3c1e6fa494fe1d947751f47fc91d56e8fcb230363b2dc8da9da2ea` | 0 |
| obp-api/src/main/scala/code/util/MappedAccountNumber.scala | 1160 | `558c71e385f4c7c917a4064b6e52ed92c93ce3a6d4908b741533d154b1e88e98` | 0 |
| obp-api/src/main/scala/code/util/MappedUUID.scala | 1127 | `dbcfa4e7d26338f020810aeb461961e10e0dc736abc55848f171783e30fda2d2` | 0 |
| obp-api/src/main/scala/code/util/NewAttributeQueryTrait.scala | 4182 | `759f4e2b79dbcbb1032a3b7f2df3753e34d550977e6f1eadf23b6f15ba2bba35` | 0 |
| obp-api/src/main/scala/code/util/ReflectionUtils.scala | 6402 | `8dc9134f92881d235086713762d49bc322d3d04b9713ffd10497f762419d0eae` | 0 |
| obp-api/src/main/scala/code/util/SecureLogging.scala | 11619 | `e06911e0d8986df0c3a5448e9e693be7ef31071ab5a59ea8f96cf92296f3d8e3` | 0 |
| obp-api/src/main/scala/code/util/SecureLoggingDemo.scala | 10315 | `efa3437d672fc3a362ede31268d01681a9de623b2a6ded95a53567e2c895bf13` | 0 |
| obp-api/src/main/scala/code/util/TTLCache.scala | 2673 | `0a275e1413e1fe487fdb36d5f3344056e5b59140d2d75ef824e7c1ac6db16646` | 0 |
| obp-api/src/main/scala/code/util/UUIDString.scala | 2354 | `55c331778f07b4b5a77497ef34c8c25a35d9671a9ac48034b99fc40e4661045f` | 0 |
| obp-api/src/main/scala/code/utilitypayment/UtilityCallbackDispatcher.scala | 3417 | `ea4640e99880007df988c4535a9aa302574e77f0d9f3b0496c034404060221be` | 0 |
| obp-api/src/main/scala/code/utilitypayment/UtilityPaymentCallback.scala | 6397 | `38650765dc6f92d85e4e3a2df5c8fc5e273a230b248f5a2930e97c6d5f89c869` | 0 |
| obp-api/src/main/scala/code/validation/JsonSchemaValidationProvider.scala | 1954 | `341997f057369ad2ce7b7a5b9b206933cdd0dac1badd24232982ade638c248c6` | 0 |
| obp-api/src/main/scala/code/validation/MappedJsonSchemaValidation.scala | 1482 | `e3dd42a04d34d580eacc312af5fec1f96d1bdc1fc129088e2befa0b068f8a383` | 0 |
| obp-api/src/main/scala/code/validation/MappedJsonSchemaValidationProvider.scala | 2920 | `ff1c09440e89867a83b789e4ea7318d19fa5d393308fdbae00d4406eee7393dd` | 0 |
| obp-api/src/main/scala/code/views/MapperViews.scala | 43259 | `479db51a1b422d4c5a664973288bfc224e42f4bac6dff0f867ee3b5e368a10b8` | 0 |
| obp-api/src/main/scala/code/views/Views.scala | 9679 | `5481f9754276d9e8a108076100e2d3e3bacf567643aaf90882abd72e1575c152` | 0 |
| obp-api/src/main/scala/code/views/system/AccountAccess.scala | 4547 | `d06e17d84106d199cb02bad3a681c705bcd2a67775ce25e1028627eb91b191c7` | 0 |
| obp-api/src/main/scala/code/views/system/ViewDefinition.scala | 18273 | `886b8dbf491aa29ce0ff1d81202f82a8f81a50638e75c7e32a94b2cdb0aafb57` | 0 |
| obp-api/src/main/scala/code/views/system/ViewPermission.scala | 6352 | `b8bec157c58ed03d3f8385fc4354c48f1a176100a589bce12e2c85cdd1719c60` | 0 |
| obp-api/src/main/scala/code/webhook/AccountWebhook.scala | 2460 | `d0f4f07a82d38d1619614adac02892136d6b2041d914bda147f4d8225c21a92b` | 0 |
| obp-api/src/main/scala/code/webhook/BankAccountNotification.scala | 2183 | `22458a0f608ab7459c044fcf2ae5f2418660c1b8db8437ec1fdc5ecca6f9ad30` | 0 |
| obp-api/src/main/scala/code/webhook/BankAccountNotificationWebhook.scala | 4585 | `13cdc18d70f8d8fe5fb3281de2a96dddbf0b460260b8a05f17aee8506ca42cd8` | 0 |
| obp-api/src/main/scala/code/webhook/MappedAccountWebhook.scala | 5454 | `49163435f2abf6470104f32f069f2dfb9f7e56591d4cd49401d9d8d54c4a2b28` | 0 |
| obp-api/src/main/scala/code/webhook/OkHttpWebhookClient.scala | 1825 | `cd54e95474d813102757e27734d175602a2cdfde92d5a8cfd25029258eb80f6b` | 0 |
| obp-api/src/main/scala/code/webhook/SystemAccountNotification.scala | 2284 | `6abc1560a1ec4933ed383ae322050f02626fb9b0a1a4e7eb5c01e363f42ca2a3` | 0 |
| obp-api/src/main/scala/code/webhook/SystemAccountNotificationWebhook.scala | 4534 | `f67104fe5d3ef6e21352f19828e259054c7a62af6597e71f4bea0ef71780588a` | 0 |
| obp-api/src/main/scala/code/webhook/WebhookActor.scala | 4776 | `b4bc582e4818e2cce48d7ca75d51cefb9161a14632d7e316d2a84dc043ec1ecb` | 0 |
| obp-api/src/main/scala/code/webhook/WebhookHttpClient.scala | 9831 | `1d3b9c13029e71ed1518fa33b9695828d8802595ac829db2810be458d8835f4d` | 0 |
| obp-api/src/main/scala/code/webuiprops/MappedWebUiPropsProvider.scala | 4662 | `e00648e407fabf4ef57b8948050c9697dc17e32c5aa74be17312543b53e214ad` | 0 |
| obp-api/src/main/scala/code/webuiprops/WebUiProps.scala | 1953 | `f9c0187c3b35665a649fda47dfabc9d43a0c74933c304640c30ae7b6b8b0c13f` | 0 |
| obp-api/src/main/scala/com/google/protobuf/empty/Empty.scala | 3537 | `2949be67cd0f472d48162adee4c84c2895873cb44c36c261155d0df252fd2ab1` | 0 |
| obp-api/src/main/scala/com/google/protobuf/empty/EmptyProto.scala | 1575 | `53995af08cb7016025178411e676e37a12265f67825008e09d49f8d4de001296` | 0 |
| obp-api/src/main/scala/com/google/protobuf/timestamp/Timestamp.scala | 10009 | `f929c0660516ef9f75b0facad1dff3abb73862a5e8e09a3c6a72dddc51d2b50e` | 0 |
| obp-api/src/main/scala/com/google/protobuf/timestamp/TimestampProto.scala | 1682 | `5ee0f2169dbd5280100d2f22650992f41b04251e4a519813383781263ea7bafc` | 0 |
| obp-api/src/main/scala/deletion/DeleteAccountCascade.scala | 10180 | `f9ce613f501d72887dc594999b1f1ad66ba53e63026ff744898567a3af751c7f` | 0 |
| obp-api/src/main/scala/deletion/DeleteBankCascade.scala | 2890 | `b2b8d85f872d3553ca6e7b64fc4348c2f0b967e920247cd34c24a463f0beaccf` | 0 |
| obp-api/src/main/scala/deletion/DeleteCustomerCascade.scala | 5179 | `c9910fd98ae6389d92efeacccd4904464bb790880c0e077c5120cda1551e261e` | 0 |
| obp-api/src/main/scala/deletion/DeleteProductCascade.scala | 3805 | `81700eccbcb36115515a3f6e8557d324b19fb6dd8df58b4b6e968627910d18f6` | 0 |
| obp-api/src/main/scala/deletion/DeleteTransactionCascade.scala | 3363 | `8cf0685a05abd6facd471765d652b4f639aefa18f7ecd70332ab1cd3d4566f20` | 0 |
| obp-api/src/main/scala/deletion/DeletionUtil.scala | 1114 | `ceaa74b87994323978ae16041a472191c94db1af5bae374e7106004623bfd201` | 0 |
| obp-commons/pom.xml | 10717 | `e6b8155ad1a632fe3456bc9c2c9f94c8fa84b342b75e2f4e29139a27e1ed7439` | 0 |
| obp-commons/src/main/scala/com/openbankproject/commons/ExecutionContext.scala | 2247 | `34d4353f35b86303599ba00d65fbb19501083b516313a8d05297e94326b656a5` | 0 |
| obp-commons/src/main/scala/com/openbankproject/commons/dto/JsonsTransfer.scala | 109115 | `f25f6bdf8fced5725ee47c58fc44746772c5eb2afb68e7db924417f0839455ed` | 0 |
| obp-commons/src/main/scala/com/openbankproject/commons/dto/OpenCorridorInterfaceC.scala | 7841 | `ba87ef943c33b2ff3f93905a6fa1e02c42e71613ad2354d7068805d7b48e5662` | 0 |
| obp-commons/src/main/scala/com/openbankproject/commons/dto/OutInBoundTransfer.scala | 1176 | `33bb3b4fe96642517dfdee69c28a897d2a836d25c9633432beb0dbf4f426249a` | 0 |
| obp-commons/src/main/scala/com/openbankproject/commons/model/BankingModel.scala | 14332 | `3e0b2d6e03d1966a2cc713b57109a5f0332217ac5493941ffb9b5ba402b171f1` | 0 |
| obp-commons/src/main/scala/com/openbankproject/commons/model/CommonModel.scala | 59857 | `efe8e7c1b101aede0a9862911bf0aa0227ec0cbadbfab7aee647ae2a89a97c8e` | 0 |
| obp-commons/src/main/scala/com/openbankproject/commons/model/CommonModelTrait.scala | 23016 | `b9cd3535fe0ad47f2793d83b812be6cb5058dfb1b53fac8dcd8fdec6073ca63c` | 0 |
| obp-commons/src/main/scala/com/openbankproject/commons/model/CounterpartyModel.scala | 2717 | `21617ace8ec63a0f1e1893d262ece533bc448b6bfaeefa1e0525af6d927c836a` | 0 |
| obp-commons/src/main/scala/com/openbankproject/commons/model/CustomerDataModel.scala | 2759 | `0326f6b692eb359df8feb0c6e541dd1693eb95284f31386019cdb973b3c67b5c` | 0 |
| obp-commons/src/main/scala/com/openbankproject/commons/model/MetadataModel.scala | 4364 | `65eeeb8f49c24558b7a3faa1d309d44ae21690af0d49c6749aaade566b694bd7` | 0 |
| obp-commons/src/main/scala/com/openbankproject/commons/model/PhysicalCardModel.scala | 4562 | `84c872e5bf80d4c43d16ce642e3ef43c34e260bd74c07dc6a6adf47628a1c6dd` | 0 |
| obp-commons/src/main/scala/com/openbankproject/commons/model/UserModel.scala | 3609 | `d442b1f0384074e6da7b0699922b530f163723e339d0ea78f0ea4ae2a6f16eeb` | 0 |
| obp-commons/src/main/scala/com/openbankproject/commons/model/ViewModel.scala | 10922 | `4daa7cb20dd546c9aa72da2b20e2412ba57437e43b1255b9955329f22f4b501f` | 0 |
| obp-commons/src/main/scala/com/openbankproject/commons/model/enums/Enumerations.scala | 17001 | `fee87e557e891ff6756da02d04ede3acd63151d3335e6c07c13e0b77a6609584` | 0 |
| obp-commons/src/main/scala/com/openbankproject/commons/util/ApiVersion.scala | 7780 | `42440688ff68d48df7f7ad2908afd3497880c90c383e6ffc6d79118f3e5886b0` | 0 |
| obp-commons/src/main/scala/com/openbankproject/commons/util/Functions.scala | 8423 | `c74a37ed19805a17fc7e2d57deaf8b9d7381d6ebec220d7f29827b0225aa95b4` | 0 |
| obp-commons/src/main/scala/com/openbankproject/commons/util/JsonAliases.scala | 3252 | `cd7e82a0f0497e9aef619b1415abc10538d667d1fc1b155d0588c2c7978e89ff` | 0 |
| obp-commons/src/main/scala/com/openbankproject/commons/util/JsonBoxSerializer.scala | 4443 | `7a2320a3d7342e33092f9fc9d3394fe69a71e0cbe493c54ac0041f1880fa8eb2` | 0 |
| obp-commons/src/main/scala/com/openbankproject/commons/util/JsonSerializers.scala | 23273 | `7a334d2181ddf0946151aaeaef52f06c87ba19cecf6c58f0664949a5cdaff442` | 0 |
| obp-commons/src/main/scala/com/openbankproject/commons/util/JsonUtils.scala | 39471 | `c75796e82e8714ca97eafef30acaccfb90f2d212e0898898fe11c8d8f5958a32` | 0 |
| obp-commons/src/main/scala/com/openbankproject/commons/util/OBPEnum.scala | 5162 | `80910279cad992bee46eed72c0b9680bb7ca4ac61c59e4909a506eea7612e33d` | 0 |
| obp-commons/src/main/scala/com/openbankproject/commons/util/ReflectUtils.scala | 30938 | `b2e4d15e0476d5c301b5b39fd53d6fb279b19c05ee57bd5ca376b9e38c4a5d10` | 0 |
| obp-commons/src/main/scala/com/openbankproject/commons/util/RequiredFieldValidation.scala | 16249 | `4e70a58a93a6d8778f41d8c7699c171c526fafed9e4cb4a147bdec1ccaa4b358` | 0 |
| pom.xml | 18829 | `0ede10727642b18179cae0a937308751effa22ca86cc175f62fabcc72ee8401a` | 0 |
| scripts/check_lift_http4s_resource_doc_parity.py | 34126 | `850c5944d66c71fe858d01d8f695878ba3477a498b8dcaca32a10a4d5c1b15b3` | 0 |
| scripts/count_v7_endpoints.py | 15031 | `6be3478e98741ffdcfcf769a6e2db905d03f930dc89f13fd0c3dcb5ec1658c4b` | 0 |
| scripts/rehydrate_resource_docs.py | 33341 | `d59ce96f599f7f77cd47c618b13ef614ac08b12a0cb88861e48aee05ac7d218e` | 0 |
| scripts/remove_duplicate_v7_endpoints.py | 2378 | `fb8cf1c7ca3e96dc1b3f9c73cccc4045f697ef2b0011a6717e1b8af75eff296c` | 0 |
| scripts/resource_doc_baseline/allowlist_helper.py | 6285 | `ae49ef57dda83559e326c6f046c3559da2f7f0e8675a03078f6bf27a4de8317b` | 0 |
| scripts/resource_doc_baseline/export_and_verify.py | 15027 | `5063062c2436e36239a5d9e85c906aa5fdec6c7d87f9a3f3e833daa6c8e7f5e4` | 0 |
| scripts/resource_doc_baseline/lift_resource_docs_v2_2_0.json | 24374 | `fa5622e08229887642b95c1e70f10e5303669d0ee56e5c1b55723d19cd17b712` | 0 |
| scripts/resource_doc_baseline/lift_resource_docs_v4_0_0.json | 247232 | `2ff65ec9486cd8778a82f9b4f42fcba3ab943dd875c1693976e8510c29b195cc` | 3 |
| scripts/restore_resource_doc_bodies.py | 17815 | `d75962443a8742985a4767e0d64ebaf6aa4b637de0a69e8b55ba031a848c8359` | 0 |
| security_check.sh | 4926 | `605501f6d16910303ce446829202366ad79fc8aad7b95c757fb3f78c5b80b128` | 0 |
