# Security & Post-Quantum Readiness Audit Report

**Project:** lightwalletd @ 4abfe9cd7b9b · Electric Coin Company (Zcash) — public repository (passive review)
| | |
|---|---|
| Organization | QSI |
| Report date | 2026-10-28 18:03 UTC |
| Report version | 1 |
| Audit run | 14a011b1-0b2f-4c1c-b464-2a7b8ae42265 (Document audit) |
| Analyzer engine | qsi-engine 1.2.0 |
| Risk profile | Small technology company |
| Content SHA-256 | `82414793308723f9630b1a40523260f8258d8b9c17a2b30005a7575edb8963e0` |
| Signature key (Ed25519, SHA-256 fingerprint; the signature is the separate file report.sig.json) | `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e` |
> This report presents automated and documented analysis results for the stated scope. It is not a legal opinion, a certification or an attestation of compliance with any standard.

## 1. Executive summary

- Critical: **0**
- High: **0**
- Medium: **0**
- Low: **10**
- Info: **4**

- Confirmed technical vulnerability: 1
- Known vulnerable component: 10
- Confirmed configuration error: 0
- Potential cryptographic risk: 0
- Long-term post-quantum risk: 2
- Improvement recommendation: 0
- Insufficient data: 1

Mosca's inequality (x + y > z): x = 5, y = 3, z = 12 → time available under this scenario. _z is a planning assumption chosen per risk profile, not a prediction. A cryptographically relevant quantum computer is not publicly known to exist today._

Analyst review: 0 confirmed, 1 not applicable, 0 dismissed as false positives.

**Post-quantum maturity: Level 0 of 4 — no post-quantum cryptography.** Next step: Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

## 2. Scope and boundaries

Mode: Document audit

Repository: <https://github.com/zcash/lightwalletd> @ `4abfe9cd7b9b13f6093df59911639d1d9195dc09` — evidence links open the lines at this commit.

34 files, 458533 bytes in total, 1 redaction(s); the per-file SHA-256 list is in appendix C.

## 3. Methodology

| Area | Status | Count | Examples |
|---|---|---|---|
| source_code | checked | 28 | cmd/connstats.go: 39 lines scanned with 16 rule patterns and 122 registry patterns; cmd/root.go: 535 lines scanned with 16 rule patterns and 122 registry patterns; cmd/version.go: 22 lines scanned with 16 rule patterns and 122 registry patterns |
| tls_code | checked | 2 | common/generatecerts.go: TLS key-exchange settings read; frontend/rawrequest.go: TLS key-exchange settings read |
| certificates_and_keys | checked | 2 | docker/cert.key: certificates/keys parsed; docker/cert.pem: certificates/keys parsed |
| dependencies | checked | 1 | go.mod: 48 dependencies parsed (48 pinned) |
| osv_advisories | checked | 1 | 48 pinned packages queried at OSV.dev; 2 affected |

_Long lists are grouped here; the full per-file list is in the JSON report, signed with the same key._

## 4. Assets examined and not examined

- None

## 5. Architecture overview

Static review of the source tree lightwalletd at 4abfe9cd7b9b13f6093df59911639d1d9195dc09. 34 files analysed; of 121 files, 24 are test, fuzzing, benchmark or example code and were left out, 63 are not read by any analyzer, 0 exceed the per-file limit and 0 did not fit the total limit. No requests were sent to the owner's systems.

## 6. Overall security posture

- Indicative posture index: **93** / 100 — _Derived from findings in scope (confirmed and potential issues weighted by severity). Indicative only; not comparable across differently scoped audits._
- Quantum-vulnerable share of inventory: 37.5%

## 7. Detailed findings

### QSI-2026-05532 — Quantum-vulnerable RSA key in certificate (lightwalletd.testnet.local)

- Severity: **Low** · Classification: Long-term post-quantum risk · Confidence: High
- Affected asset: `certificate:lightwalletd.testnet.local`
- Data source: docker/cert.pem
- Detection method: X.509 public key algorithm identification.
- Analyzer: certificates 1.2.0 · 2026-10-28 18:03 UTC
- Priority score: 36.2 / 100
- CVSS v3.1: not applicable

The certificate lightwalletd.testnet.local uses a RSA 2048-bit public key, valid until 2029-12-15. RSA is broken by Shor's algorithm on a CRQC.

**Potential impact.** For authentication, risk materializes only once a CRQC exists while the key/certificate is still trusted. Certificates are short-lived, so the main concern is the PKI and long-lived roots/intermediates.

**Reproduction steps.**

```
openssl x509 -in docker/cert.pem -noout -text | grep -A2 'Public Key Algorithm'
```

**Evidence.**

_certificate · docker/cert.pem · line 1 · SHA-256 4cd9b3240260015c81d32a7359585aeb0a8fc54aafe812cd312f2fa3b2bc2e7a_

```
Subject: CN=lightwalletd.testnet.local,O=MyOrg\, Inc.,ST=CA,C=US
Issuer: CN=lightwalletd.testnet.local,O=MyOrg\, Inc.,ST=CA,C=US
Serial: 7af3c04cf3fbe2a63724f13ab376b1c670bcaf1c
Not before: 2019-12-18T14:24:54+00:00
Not after: 2029-12-15T14:24:54+00:00
Public key: RSA 2048-bit
Signature algorithm: 1.2.840.113549.1.1.11
Signature hash: sha256
CA: True
SAN: -
SHA-256 fingerprint: 907548fce41ead924e1a866da5bb154a58b5b7e503443babd2da3e6d597341c4
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability.

**Recommendation.** Track in the PQC inventory; prefer short certificate lifetimes; follow CA/Browser Forum and NIST PQC transition guidance for ML-DSA certificates.

**Retest procedure.** Re-audit once PQC or hybrid certificates are deployed.

### QSI-2026-05530 — Quantum-vulnerable RSA: role not determined (1 file(s))

- Severity: **Low** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:RSA:general`
- Data source: common/generatecerts.go
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.2.0 · 2026-10-28 18:03 UTC
- Priority score: 23.6 / 100
- CVSS v3.1: not applicable

2 reference(s) to RSA across 1 file(s), e.g. common/generatecerts.go:8. Role, judged from paths, function names and nearby code: role not determined. The code does not show what the keys protect; review decides the priority.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open common/generatecerts.go:8 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [common/generatecerts.go](https://github.com/zcash/lightwalletd/blob/4abfe9cd7b9b13f6093df59911639d1d9195dc09/common/generatecerts.go#L8) · line 8 · SHA-256 9b1ce2f208b801d04fec37816b6888e4ae8b469d0344091f5c8a837ee93158f9_

```
    7 | 	"crypto/rand"
    8 | 	"crypto/rsa"
    9 | 	"crypto/tls"
```

_file_excerpt · [common/generatecerts.go](https://github.com/zcash/lightwalletd/blob/4abfe9cd7b9b13f6093df59911639d1d9195dc09/common/generatecerts.go#L21) · line 21 · SHA-256 7bc59a5974adbfd5570196de74190cfdee0b2b136760fe696a10a96bbe4f03d0_

```
   20 | 
   21 | 	privKey, err := rsa.GenerateKey(rand.Reader, 2048)
   22 | 	if err != nil {
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it; introduce an abstraction layer for crypto-agility.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-05534 — golang.org/x/crypto v0.55.0 is affected by GO-2026-5932 (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:Go/golang.org/x/crypto@v0.55.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 18:03 UTC
- Priority score: 20.2 / 100
- CVSS v3.1: not applicable

OSV.dev reports GO-2026-5932 for Go package golang.org/x/crypto at version v0.55.0: The golang.org/x/crypto/openpgp package is unmaintained, unsafe by design, and has known security issues. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-5932
```

**Evidence.**

_tool_output · [OSV.dev GO-2026-5932](https://osv.dev/vulnerability/GO-2026-5932) · line 53 · SHA-256 ccbd80f24a2d759ed3db1ed22b247aaeb8d2704fa45844ff83df82b05bff5e93_

```
{"id": "GO-2026-5932", "aliases": [], "modified": "2026-07-10T05:44:31.101996029Z", "summary": "The golang.org/x/crypto/openpgp package is unmaintained, unsafe by design, and has known security issues", "severity": null, "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Triage the advisory; upgrade to a fixed version (none published yet; see the advisory for mitigations) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-05535 — golang.org/x/crypto v0.55.0 is affected by GO-2026-6354 (CVE-2026-78662) (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:Go/golang.org/x/crypto@v0.55.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 18:03 UTC
- Priority score: 20.2 / 100
- CVSS v3.1: not applicable

OSV.dev reports GO-2026-6354 (CVE-2026-78662) for Go package golang.org/x/crypto at version v0.55.0: Prevent DoS on deadlocked undecided channel in golang.org/x/crypto/ssh. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. The audited code names golang.org/x/crypto/ssh.Dial: the affected code may be reachable.

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-6354
```

**Evidence.**

_tool_output · [OSV.dev GO-2026-6354](https://osv.dev/vulnerability/GO-2026-6354) · line 53 · SHA-256 fb187877ccc7bca3e1e620fe5ac478176b0bfa60d40289c6b8513c063eaec76c_

```
{"id": "GO-2026-6354", "aliases": ["CVE-2026-78662"], "modified": "2026-09-03T10:10:55.147673102Z", "summary": "Prevent DoS on deadlocked undecided channel in golang.org/x/crypto/ssh", "severity": null, "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Triage the advisory; upgrade to a fixed version (0.56.0) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-05536 — golang.org/x/crypto v0.55.0 is affected by GO-2026-6355 (CVE-2026-56855) (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:Go/golang.org/x/crypto@v0.55.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 18:03 UTC
- Priority score: 20.2 / 100
- CVSS v3.1: not applicable

OSV.dev reports GO-2026-6355 (CVE-2026-56855) for Go package golang.org/x/crypto at version v0.55.0: Prevent DoS on deadlocked established channel in golang.org/x/crypto/ssh. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. The audited code names golang.org/x/crypto/ssh.Dial: the affected code may be reachable.

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-6355
```

**Evidence.**

_tool_output · [OSV.dev GO-2026-6355](https://osv.dev/vulnerability/GO-2026-6355) · line 53 · SHA-256 4e6adace91e1ca1e94bf05a7bfb237f4851e56b8c982501612e1583273e4073e_

```
{"id": "GO-2026-6355", "aliases": ["CVE-2026-56855"], "modified": "2026-09-24T10:41:42.556134596Z", "summary": "Prevent DoS on deadlocked established channel in golang.org/x/crypto/ssh", "severity": null, "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Triage the advisory; upgrade to a fixed version (0.56.0) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-05537 — golang.org/x/net v0.58.0 is affected by GO-2026-6603 (CVE-2026-78659) (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:Go/golang.org/x/net@v0.58.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 18:03 UTC
- Priority score: 20.2 / 100
- CVSS v3.1: not applicable

OSV.dev reports GO-2026-6603 (CVE-2026-78659) for Go package golang.org/x/net at version v0.58.0: HTTP/2 server memory exhaustion due to Trailer headers in net/http. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. The audited code names golang.org/x/net/http2.ClientConn.Ping, golang.org/x/net/http2.connError.Error, golang.org/x/net/http2.duplicatePseudoHeaderError.Error, golang.org/x/net/http2.headerFieldNameError.Error …: the affected code may be reachable.

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-6603
```

**Evidence.**

_tool_output · [OSV.dev GO-2026-6603](https://osv.dev/vulnerability/GO-2026-6603) · line 54 · SHA-256 9e43850e0da48e9d00589cc2bffb372f39ec5e5a280f2f4b04520a91328fd703_

```
{"id": "GO-2026-6603", "aliases": ["BIT-golang-2026-78659", "CVE-2026-78659"], "modified": "2026-10-16T09:55:47.068117441Z", "summary": "HTTP/2 server memory exhaustion due to Trailer headers in net/http", "severity": null, "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Triage the advisory; upgrade to a fixed version (0.60.0) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-05539 — golang.org/x/net v0.58.0 is affected by GO-2026-6611 (CVE-2026-78669) (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:Go/golang.org/x/net@v0.58.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 18:03 UTC
- Priority score: 20.2 / 100
- CVSS v3.1: not applicable

OSV.dev reports GO-2026-6611 (CVE-2026-78669) for Go package golang.org/x/net at version v0.58.0: Excessive CPU consumption from repeated initial window changes in net/http. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. The audited code names golang.org/x/net/http2.ClientConn.Ping, golang.org/x/net/http2.connError.Error, golang.org/x/net/http2.duplicatePseudoHeaderError.Error, golang.org/x/net/http2.headerFieldNameError.Error …: the affected code may be reachable.

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-6611
```

**Evidence.**

_tool_output · [OSV.dev GO-2026-6611](https://osv.dev/vulnerability/GO-2026-6611) · line 54 · SHA-256 c9b9f78637131224c5d4073e44c47b7cce490fc5526e3d6b0697b43bc85cab2f_

```
{"id": "GO-2026-6611", "aliases": ["BIT-golang-2026-78669", "CVE-2026-78669"], "modified": "2026-10-16T09:55:38.952277866Z", "summary": "Excessive CPU consumption from repeated initial window changes in net/http", "severity": null, "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Triage the advisory; upgrade to a fixed version (0.60.0) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-05540 — golang.org/x/net v0.58.0 is affected by GO-2026-6612 (CVE-2026-78663) (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:Go/golang.org/x/net@v0.58.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 18:03 UTC
- Priority score: 20.2 / 100
- CVSS v3.1: not applicable

OSV.dev reports GO-2026-6612 (CVE-2026-78663) for Go package golang.org/x/net at version v0.58.0: Double flow control refund on HTTP/2 server streams in net/http. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. The audited code names golang.org/x/net/http2.ClientConn.Ping, golang.org/x/net/http2.connError.Error, golang.org/x/net/http2.duplicatePseudoHeaderError.Error, golang.org/x/net/http2.headerFieldNameError.Error …: the affected code may be reachable.

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-6612
```

**Evidence.**

_tool_output · [OSV.dev GO-2026-6612](https://osv.dev/vulnerability/GO-2026-6612) · line 54 · SHA-256 1471910f88c9bbf8395a304fd82510f61567373756002de8bcdc3fbe305890cb_

```
{"id": "GO-2026-6612", "aliases": ["BIT-golang-2026-78663", "CVE-2026-78663"], "modified": "2026-10-16T09:55:54.129082194Z", "summary": "Double flow control refund on HTTP/2 server streams in net/http", "severity": null, "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Triage the advisory; upgrade to a fixed version (0.60.0) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-05541 — golang.org/x/net v0.58.0 is affected by GO-2026-6617 (CVE-2026-97032) (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:Go/golang.org/x/net@v0.58.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 18:03 UTC
- Priority score: 20.2 / 100
- CVSS v3.1: not applicable

OSV.dev reports GO-2026-6617 (CVE-2026-97032) for Go package golang.org/x/net at version v0.58.0: HTTP/2 server crash due to HPACK encoder race in net/http. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. The audited code names golang.org/x/net/http2.ClientConn.Ping, golang.org/x/net/http2.connError.Error, golang.org/x/net/http2.duplicatePseudoHeaderError.Error, golang.org/x/net/http2.headerFieldNameError.Error …: the affected code may be reachable.

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-6617
```

**Evidence.**

_tool_output · [OSV.dev GO-2026-6617](https://osv.dev/vulnerability/GO-2026-6617) · line 54 · SHA-256 b948c88d959bc78948c7e3b7a746ac4da179933798e9735d02870080906cfc96_

```
{"id": "GO-2026-6617", "aliases": ["BIT-golang-2026-97032", "CVE-2026-97032"], "modified": "2026-10-16T09:55:57.350751224Z", "summary": "HTTP/2 server crash due to HPACK encoder race in net/http", "severity": null, "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Triage the advisory; upgrade to a fixed version (0.60.0) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-05542 — golang.org/x/net v0.58.0 is affected by GO-2026-6860 (CVE-2026-78661) (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:Go/golang.org/x/net@v0.58.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 18:03 UTC
- Priority score: 20.2 / 100
- CVSS v3.1: not applicable

OSV.dev reports GO-2026-6860 (CVE-2026-78661) for Go package golang.org/x/net at version v0.58.0: Avoid quadratic complexity when coalescing text nodes in html in golang.org/x/net. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. The audited code names golang.org/x/net/html.parser.parse: the affected code may be reachable.

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-6860
```

**Evidence.**

_tool_output · [OSV.dev GO-2026-6860](https://osv.dev/vulnerability/GO-2026-6860) · line 54 · SHA-256 1f106c45371219bac0158f7ce44e57c439f50f0c32898616d1563f14cadb1b28_

```
{"id": "GO-2026-6860", "aliases": ["CVE-2026-78661"], "modified": "2026-10-27T21:30:04.890809062Z", "summary": "Avoid quadratic complexity when coalescing text nodes in html in golang.org/x/net", "severity": null, "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Triage the advisory; upgrade to a fixed version (0.62.0) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-05531 — Private key material present in docker/cert.key

- Severity: **Info** · Classification: Confirmed technical vulnerability · Confidence: High
> **Analyst review (QSI review, 2026-10-23): not applicable to this code.** Self-signed development certificate generated by gen_cert.sh beside it: CN=lightwalletd.testnet.local with subjectAltName covering only localhost and 127.0.0.1. The key really is committed, so the rule is right, but it authenticates no real domain and is not a production credential. Hygiene for the maintainers rather than a vulnerability; deleting it and relying on gen_cert.sh would close it. _automated severity: High._
- Affected asset: `file:docker/cert.key`
- Data source: docker/cert.key
- Detection method: PEM header detection.
- Analyzer: certificates 1.2.0 · 2026-10-28 18:03 UTC
- Priority score: 51.5 / 100
- CVSS v3.1: 8.1 (`CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N`)

A 'PRIVATE KEY' block was found at line 1 of docker/cert.key. QSI redacted the key before storage; the original file still contains it.

**Potential impact.** Anyone with access to this file (repository, backups, CI logs) can impersonate the key owner or decrypt protected data.

**Reproduction steps.**

```
grep -n 'PRIVATE KEY-----' docker/cert.key
```

**Evidence.**

_file_excerpt · [docker/cert.key](https://github.com/zcash/lightwalletd/blob/4abfe9cd7b9b13f6093df59911639d1d9195dc09/docker/cert.key#L1) · line 1 · SHA-256 8ff5675e3f073e63b697c7e9001d2a28e01d7160748521613aeaa91195b89441_

```
Line 1: -----BEGIN PRIVATE KEY----- … [REDACTED BY QSI] … -----END …
```

**Limitations of the check.** QSI cannot determine whether this key is in production use. The key value was not retained.

**Recommendation.** Treat the key as compromised: rotate it, revoke associated certificates, remove it from version history and store keys in a secrets manager/HSM.

**Retest procedure.** Search the repository and its history for private key headers; confirm the old key is revoked.

### QSI-2026-05538 — golang.org/x/net v0.58.0 is affected by GO-2026-6610 (CVE-2026-78660) (no severity rating)

- Severity: **Info** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:Go/golang.org/x/net@v0.58.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 18:03 UTC
- Priority score: 17.1 / 100
- CVSS v3.1: not applicable

OSV.dev reports GO-2026-6610 (CVE-2026-78660) for Go package golang.org/x/net at version v0.58.0: HTTP/2 transport accepts malformed framing-related headers in net/http. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. None of the affected functions (golang.org/x/net/http2.Transport.NewClientConn, golang.org/x/net/http2.Transport.RoundTrip, golang.org/x/net/http2.Transport.RoundTripOpt, golang.org/x/net/http2.clientConnPool.GetClientConn, golang.org/x/net/http2.clientConnReadLoop.handleResponse, golang.org/x/net/http2.noDialClientConnPool.GetClientConn …) is named in the audited code: the advisory does not apply unless they are reached indirectly (traits, macros, other dependencies).

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-6610
```

**Evidence.**

_tool_output · [OSV.dev GO-2026-6610](https://osv.dev/vulnerability/GO-2026-6610) · line 54 · SHA-256 1b823e53f27093797b8a7909032006e1f0f818f04118ad593a4641236392faa9_

```
{"id": "GO-2026-6610", "aliases": ["BIT-golang-2026-78660", "CVE-2026-78660"], "modified": "2026-10-16T09:56:04.364467528Z", "summary": "HTTP/2 transport accepts malformed framing-related headers in net/http", "severity": null, "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Triage the advisory; upgrade to a fixed version (0.60.0) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-05543 — golang.org/x/net v0.58.0 is affected by GO-2026-6866 (CVE-2026-97045) (no severity rating)

- Severity: **Info** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:Go/golang.org/x/net@v0.58.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-28 18:03 UTC
- Priority score: 17.1 / 100
- CVSS v3.1: not applicable

OSV.dev reports GO-2026-6866 (CVE-2026-97045) for Go package golang.org/x/net at version v0.58.0: Check all ancestor namespace transitions when rendering raw text in html in golang.org/x/net. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. None of the affected functions (golang.org/x/net/html.Render, golang.org/x/net/html.childTextNodesAreLiteral) is named in the audited code: the advisory does not apply unless they are reached indirectly (traits, macros, other dependencies).

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-6866
```

**Evidence.**

_tool_output · [OSV.dev GO-2026-6866](https://osv.dev/vulnerability/GO-2026-6866) · line 54 · SHA-256 102267a016bc5eef7979a90b1ddd2288ff36b09ab6fa040c808e62f3b55c1f42_

```
{"id": "GO-2026-6866", "aliases": ["CVE-2026-97045"], "modified": "2026-10-27T21:45:08.978077289Z", "summary": "Check all ancestor namespace transitions when rendering raw text in html in golang.org/x/net", "severity": null, "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Triage the advisory; upgrade to a fixed version (0.62.0) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-05533 — No post-quantum capable cryptographic library detected

- Severity: **Info** · Classification: Insufficient data · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `dependencies`
- Data source: dependency manifests
- Detection method: Dependency name matching.
- Analyzer: dependencies 1.2.0 · 2026-10-28 18:03 UTC
- Priority score: 13.4 / 100
- CVSS v3.1: not applicable

Across 1 dependency manifests, QSI found crypto libraries (golang.org/x/crypto) but none from its PQC-capable list.

**Potential impact.** Readiness indicator only: PQC support may come from the platform (OpenSSL, OS, cloud KMS) rather than application dependencies.

**Reproduction steps.**

```
Review the dependency manifests listed in the evidence.
```

**Evidence.**

_dependency · go.mod · SHA-256 08e31f77129cdbad6d0a0f04c40df31cd6fe947d800a44bd559bcbe68f820e1b_

```
Crypto libraries: golang.org/x/crypto
```

**Limitations of the check.** Absence of evidence is not evidence of absence: system libraries and transitive dependencies may not be listed.

**Recommendation.** Confirm where PQC support will come from (TLS terminator, KMS/HSM, library upgrade).

**Retest procedure.** Re-scan after upgrades.


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

### What the quantum-vulnerable algorithms do

| Role | Algorithms (files) | ID | First step |
|---|---|---|---|
| **role not determined** | RSA (1) | QSI-2026-05530 | Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it; introduce an abstraction layer for crypto-agility |

_Roles are judged from file paths, function names and the code around each match; review confirms them. Root-of-trust keys and wrapped keys come first: they are hard to replace or can be recorded today._
No readiness questionnaire was completed for this project.

### Quantum algorithms relevant to this inventory

| Quantum algorithm | Effect | Attack model | Inventoried algorithms (rows) | What it means for this audit |
|---|---|---|---|---|
| Shor's algorithm — factoring | breaks | Q1 | RSA (3) | Breaks RSA at every key length: a longer modulus only raises the cost polynomially. Plan migration to ML-KEM (or a hybrid) for key establishment and ML-DSA / SLH-DSA for signatures; start with keys protecting data that must stay confidential for years (harvest now, decrypt later) and with long-lived signatures. |
| Grover's algorithm — key search and preimages | weakens (larger keys restore the margin) | Q1 | SHA-2 (4) | Not a break. 256-bit keys (AES-256, ChaCha20) keep a comfortable margin; AES-128 meets NIST category 1, while some authorities ask for 256-bit keys in quantum-resistant contexts (see the AES-128 entry). Prefer 256-bit keys for long-lived data; 256-bit hashes need no change for preimage resistance. |
| Brassard–Høyer–Tapp — collision search | weakens (larger keys restore the margin) | Q1 | SHA-2 (4) | 256-bit hashes (SHA-256, SHA3-256) remain adequate for collision resistance; 160-bit hashes are already weak classically (SHA-1 collisions are practical). Use 384/512-bit hashes where NIST categories 4–5 are required. |

_Effects: breaks — replace the algorithm; weakens — larger keys or outputs restore the margin; included in standard parameters — no action at standard parameter sets; only with superposition queries — not applicable to ordinary deployments._


## 9. Limitations and assumptions

- This report presents automated and documented analysis results for the stated scope. It is not a legal opinion, a certification or an attestation of compliance with any standard.
- z is a planning assumption chosen per risk profile, not a prediction. A cryptographically relevant quantum computer is not publicly known to exist today.

## 10. Remediation plan / Priorities for 30, 60 and 90 days

### 30 days

| Priority | ID | Action | Type | Closure criteria |
|---|---|---|---|---|
| P1 | QSI-2026-05531 | Revoke/rotate the key found in docker/cert.key immediately and restrict access to the file. | short-term risk reduction | Old key revoked, new key deployed. |
### 60 days

| Priority | ID | Action | Type | Closure criteria |
|---|---|---|---|---|
| P1 | QSI-2026-05531 | Move key storage to a secrets manager or HSM; add secret scanning to CI and pre-commit; purge history. | root-cause fix | Secret scanning enforced in CI; no keys in history. |
| P3 | QSI-2026-05534 | Triage GO-2026-5932; upgrade golang.org/x/crypto to a fixed version (none published yet; see the advisory for mitigations) if it applies. | root-cause fix | Dependency scan no longer reports GO-2026-5932, or the triage is recorded. |
| P3 | QSI-2026-05535 | Triage GO-2026-6354 (CVE-2026-78662); upgrade golang.org/x/crypto to a fixed version (0.56.0) if it applies. | root-cause fix | Dependency scan no longer reports GO-2026-6354 (CVE-2026-78662), or the triage is recorded. |
| P3 | QSI-2026-05536 | Triage GO-2026-6355 (CVE-2026-56855); upgrade golang.org/x/crypto to a fixed version (0.56.0) if it applies. | root-cause fix | Dependency scan no longer reports GO-2026-6355 (CVE-2026-56855), or the triage is recorded. |
| P3 | QSI-2026-05537 | Triage GO-2026-6603 (CVE-2026-78659); upgrade golang.org/x/net to a fixed version (0.60.0) if it applies. | root-cause fix | Dependency scan no longer reports GO-2026-6603 (CVE-2026-78659), or the triage is recorded. |
| P3 | QSI-2026-05539 | Triage GO-2026-6611 (CVE-2026-78669); upgrade golang.org/x/net to a fixed version (0.60.0) if it applies. | root-cause fix | Dependency scan no longer reports GO-2026-6611 (CVE-2026-78669), or the triage is recorded. |
| P3 | QSI-2026-05540 | Triage GO-2026-6612 (CVE-2026-78663); upgrade golang.org/x/net to a fixed version (0.60.0) if it applies. | root-cause fix | Dependency scan no longer reports GO-2026-6612 (CVE-2026-78663), or the triage is recorded. |
| P3 | QSI-2026-05541 | Triage GO-2026-6617 (CVE-2026-97032); upgrade golang.org/x/net to a fixed version (0.60.0) if it applies. | root-cause fix | Dependency scan no longer reports GO-2026-6617 (CVE-2026-97032), or the triage is recorded. |
| P3 | QSI-2026-05542 | Triage GO-2026-6860 (CVE-2026-78661); upgrade golang.org/x/net to a fixed version (0.62.0) if it applies. | root-cause fix | Dependency scan no longer reports GO-2026-6860 (CVE-2026-78661), or the triage is recorded. |
| P3 | QSI-2026-05538 | Triage GO-2026-6610 (CVE-2026-78660); upgrade golang.org/x/net to a fixed version (0.60.0) if it applies. | root-cause fix | Dependency scan no longer reports GO-2026-6610 (CVE-2026-78660), or the triage is recorded. |
| P3 | QSI-2026-05543 | Triage GO-2026-6866 (CVE-2026-97045); upgrade golang.org/x/net to a fixed version (0.62.0) if it applies. | root-cause fix | Dependency scan no longer reports GO-2026-6866 (CVE-2026-97045), or the triage is recorded. |
### 90 days

| Priority | ID | Action | Type | Closure criteria |
|---|---|---|---|---|
| P3 | QSI-2026-05532 | Add RSA usages at certificate:lightwalletd.testnet.local to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-05530 | Add RSA usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P4 | QSI-2026-05532 | Plan migration of RSA to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. or a hybrid scheme in use. |
| P4 | QSI-2026-05530 | Plan migration of RSA to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |

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
16. NIST — Post-Quantum Cryptography Standardization: Evaluation Criteria, Security (Call for Proposals, Section 4.A.5) — NIST. <https://csrc.nist.gov/Projects/Post-Quantum-Cryptography/Post-Quantum-Cryptography-Standardization/Evaluation-Criteria/Security-(Evaluation-Criteria)> (security categories: AES-128 key search 2^170/MAXDEPTH quantum gates, AES-192 2^233/MAXDEPTH, AES-256 2^298/MAXDEPTH; MAXDEPTH 2^40–2^96)
17. OSV advisory GO-2026-5932 — OSV.dev. <https://osv.dev/vulnerability/GO-2026-5932> (modified 2026-07-10T05:44:31.101996029Z)
18. OSV advisory GO-2026-6354 — OSV.dev. <https://osv.dev/vulnerability/GO-2026-6354> (modified 2026-09-03T10:10:55.147673102Z)
19. OSV advisory GO-2026-6355 — OSV.dev. <https://osv.dev/vulnerability/GO-2026-6355> (modified 2026-09-24T10:41:42.556134596Z)
20. OSV advisory GO-2026-6603 — OSV.dev. <https://osv.dev/vulnerability/GO-2026-6603> (modified 2026-10-16T09:55:47.068117441Z)
21. OSV advisory GO-2026-6610 — OSV.dev. <https://osv.dev/vulnerability/GO-2026-6610> (modified 2026-10-16T09:56:04.364467528Z)
22. OSV advisory GO-2026-6611 — OSV.dev. <https://osv.dev/vulnerability/GO-2026-6611> (modified 2026-10-16T09:55:38.952277866Z)
23. OSV advisory GO-2026-6612 — OSV.dev. <https://osv.dev/vulnerability/GO-2026-6612> (modified 2026-10-16T09:55:54.129082194Z)
24. OSV advisory GO-2026-6617 — OSV.dev. <https://osv.dev/vulnerability/GO-2026-6617> (modified 2026-10-16T09:55:57.350751224Z)
25. OSV advisory GO-2026-6860 — OSV.dev. <https://osv.dev/vulnerability/GO-2026-6860> (modified 2026-10-27T21:30:04.890809062Z)
26. OSV advisory GO-2026-6866 — OSV.dev. <https://osv.dev/vulnerability/GO-2026-6866> (modified 2026-10-27T21:45:08.978077289Z)
27. OWASP Application Security Verification Standard — OWASP. <https://owasp.org/www-project-application-security-verification-standard/> (living standard — check the project page for the current version)
28. P. W. Shor — Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms on a Quantum Computer (SIAM J. Comput., 1997) — SIAM. <https://doi.org/10.1137/S0097539795293172> (peer-reviewed article)
29. S. Jaques, M. Naehrig, M. Roetteler, F. Virdia — Implementing Grover oracles for quantum key search on AES and LowMC (EUROCRYPT 2020; arXiv:1910.01700) — Springer / arXiv. <https://arxiv.org/abs/1910.01700> (peer-reviewed article: lower cost estimates for the AES key searches that define the NIST categories)

## Appendices: Cryptographic inventory

| Algorithm | Parameter | Library | Location | Quantum status | Classical status |
|---|---|---|---|---|---|
| SHA-2 | SHA-256 |  | common/darkside.go:6 | Grover: acceptable to NIST, below ECCG/ANSSI guidance | acceptable |
| SHA-2 | SHA-256 |  | docker/cert.pem (line 1) | Grover: acceptable to NIST, below ECCG/ANSSI guidance | acceptable |
| SHA-2 | SHA-256 |  | parser/block_header.go:10 | Grover: acceptable to NIST, below ECCG/ANSSI guidance | acceptable |
| SHA-2 | SHA-256 |  | testtools/genblocks/main.go:28 | Grover: acceptable to NIST, below ECCG/ANSSI guidance | acceptable |
| Crypto library | v0.55.0 | golang.org/x/crypto (Go x/crypto) | go.mod:53 | n/a | acceptable |
| RSA | 2048-bit |  | common/generatecerts.go:21 | vulnerable (Shor) | acceptable |
| RSA |  |  | common/generatecerts.go:8 | vulnerable (Shor) | acceptable |
| RSA | 2048-bit |  | docker/cert.pem (line 1) — lightwalletd.testnet.local | vulnerable (Shor) | acceptable |

## Appendices: Input files

| File | Size | SHA-256 | Redactions |
|---|---|---|---|
| cmd/connstats.go | 1196 | `47405d57d1b057faf3be41fdcc1227795319cdcdfee56629c630e66953351311` | 0 |
| cmd/root.go | 20101 | `e6152b83ea0eb6273e64456e350279e7be0268da4c136648d4afeaf3e2a1cf9c` | 0 |
| cmd/version.go | 517 | `33979cac0db08986defae5ac62072805d733c30dd303540733b17277616d10cd` | 0 |
| common/cache.go | 11643 | `ba5f9da3c1492a90d48c20c15256a1bf6e354ba8bb1b58cd2fd62d9b4ddcd2a7` | 0 |
| common/common.go | 25507 | `c8f7603b7d32f5b076d1d61bce1be524acbe7ef20bfd35007978e638a04e9d75` | 0 |
| common/darkside.go | 33254 | `129a6d62e78a2bfaf78eaf34fc5fd29cadb5d074de1907669c4c63921e7dd30a` | 0 |
| common/generatecerts.go | 2135 | `010d1a90f0fea3babe111d4e2d463b754c4d574a16ff2840e69b6f6ef92dc19b` | 0 |
| common/logging/logging.go | 1036 | `5478a895e3bdb5f83bc14e71d715e55d325ceaae9030e6e00a3655460bf1f307` | 0 |
| common/mempool.go | 4431 | `13def4c96768f0e46aaeec5b248b801c1c267e4f6f4adc4d94ea49f7f9cc5ef2` | 0 |
| docker/cert.key | 97 | `4d417087d1f5076360d4260961ed5c29a58fa722450b20caf8d68765c54ab3c4` | 1 |
| docker/cert.pem | 1289 | `8d44580bca050fd5b3a266b8e9c102a88cbdd88c5996c342b4ab8757b94d720c` | 0 |
| frontend/rawrequest.go | 4645 | `fad7ec20c623c12a517ca838059b1f6f99d76b971c42204a9c168db3cc562efb` | 0 |
| frontend/rpc_client.go | 3780 | `dd87e4a43595a01119338a5cbc010134af1eae4c90a3857ba8527deeeaec8583` | 0 |
| frontend/service.go | 51588 | `33abee53b15eece3dadbd2193eadd7c39815b8fedec4c0d589764223fcb78d47` | 0 |
| go.mod | 2431 | `2c741f2d97ee03e96e8afbeaacc5f3c7ab44cb73af859d3ad4c99930d595c108` | 0 |
| hash32/hash32.go | 1527 | `961a695822b5bc76ff5decfebc65cfab1fbbb4aada7097177ba9d3d76082c5fa` | 0 |
| lightwallet-protocol/walletrpc/compact_formats.proto | 6490 | `d8d0c8aaa5ceec7d5dcc188ef25b04011df2ec0254901620fce982fc13aeb32d` | 0 |
| lightwallet-protocol/walletrpc/service.proto | 16054 | `9352e90977cfd55ead3a0b97048c40d673ad0024d33882ae89e15727fad19138` | 0 |
| main.go | 89 | `ec16ed2f1a286086fd738c4cbb990cd6790116a39711c6a35fa405ad888a116e` | 0 |
| parser/block.go | 4546 | `3b21fb1aaf2d4d1737325894d4d2ccbff6013a29257170c67548326884a096a5` | 0 |
| parser/block_header.go | 8236 | `9fc7957a45629ec9dbadca29fee6ac6527c71a155d123c32bacf743f021a66b2` | 0 |
| parser/bounds.go | 3289 | `4303340054eaed723ee8da6e0dd6bf431d7cedb4fa9e7bf45691780ad0c7d731` | 0 |
| parser/fuzz.go | 354 | `d18aa41f9e4f215c8499d4e48add2b3075a481ab746f7f6af4144bdc19994d34` | 0 |
| parser/internal/bytestring/bytestring.go | 6427 | `cb01a5a03292979ae9d055e1ce37a137fc1c9af4f8a32b8f762040e18fe2719a` | 0 |
| parser/transaction.go | 24187 | `ff9c519ffdad866ec1ca573f742f2081df7f67c8ace42299f13513c714428265` | 0 |
| testclient/main.go | 4293 | `3f607912b23700a153a32c0f4ac95f3bb1c353a358ccf5ed2db5979f2f97eb35` | 0 |
| testtools/genblocks/main.go | 4934 | `6a7eca671d69272de2ba5471acf4d4007fbf1d6289153474360c77ba108048cc` | 0 |
| testtools/zap/main.go | 764 | `fc24949d4b8271fb936e68aeb6e6240fb258bab038a29a7eef91f615c5607de2` | 0 |
| walletrpc/compact_formats.pb.go | 25356 | `5ad9198be37bcab74f36ccbc7dca5d891632d03635f65bd70a559b46e74d04ed` | 0 |
| walletrpc/darkside.pb.go | 24975 | `51100120dc12c58486ad0eff68f564e93d70bbb2096521bef2bb5d59fa8f9b14` | 0 |
| walletrpc/darkside.proto | 7344 | `8d3582ed9efaaefeb44c2ee432191127339154b677b253350fd8ff85befff5d2` | 0 |
| walletrpc/darkside_grpc.pb.go | 42355 | `8dd2070e114aeb584628b082dce641654fb7157d4bdac5900e4ab640eb04d740` | 0 |
| walletrpc/service.pb.go | 62312 | `79749fecb58b41f9c762c374d2e4c4889665c9e450862b2a882061770b00c734` | 0 |
| walletrpc/service_grpc.pb.go | 51351 | `d5ec3b07634d3b8bbc83bb0981fc370c62b7bd24080b28d44ecc9f8f54cccd43` | 0 |
