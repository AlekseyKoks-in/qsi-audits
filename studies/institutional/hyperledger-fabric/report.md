# Security & Post-Quantum Readiness Audit Report

**Project:** hyperledger-fabric @ 13ef9e5ee594 · Hyperledger Fabric (LF Decentralized Trust) — public repository (passive review)
| | |
|---|---|
| Organization | QSI |
| Report date | 2026-11-06 10:32 UTC |
| Report version | 1 |
| Audit run | 4d4b80d2-b345-4016-a57a-14639a8ee008 (Document audit) |
| Analyzer engine | qsi-engine 1.3.0 |
| Risk profile | Crypto exchange, custodian or wallet |
| Content SHA-256 | `c6d8ad0dc0ae1f4057b7a287b056a05648ac2555beac30700886e6ad50e9e186` |
| Signature key (Ed25519, SHA-256 fingerprint; the signature is the separate file report.sig.json) | `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e` |
> This report presents automated and documented analysis results for the stated scope. It is not a legal opinion, a certification or an attestation of compliance with any standard.

## 1. Executive summary

- Critical: **0**
- High: **1**
- Medium: **7**
- Low: **3**
- Info: **18**

- Confirmed technical vulnerability: 0
- Known vulnerable component: 20
- Confirmed configuration error: 0
- Potential cryptographic risk: 1
- Long-term post-quantum risk: 8
- Improvement recommendation: 0
- Insufficient data: 0

Mosca's inequality (x + y > z): x = 10, y = 5, z = 8 → migration would finish too late under this scenario. _z is a planning assumption chosen per risk profile, not a prediction. A cryptographically relevant quantum computer is not publicly known to exist today._

**Post-quantum maturity: Level 4 of 4 — post-quantum by default in the critical paths.** Next step: Keep the inventory current and review new code paths before release.

## 2. Scope and boundaries

Mode: Document audit

Repository: <https://github.com/hyperledger/fabric> @ `13ef9e5ee59466b152c8fe65b3a095234de671f7` — evidence links open the lines at this commit.

814 files, 5287906 bytes in total, 0 redaction(s); the per-file SHA-256 list is in appendix C.

## 3. Methodology

| Area | Status | Count | Examples |
|---|---|---|---|
| source_code | checked | 789 | ccaas_builder/cmd/detect/main.go: 68 lines scanned with 16 rule patterns and 266 registry patterns; ccaas_builder/cmd/release/main.go: 106 lines scanned with 16 rule patterns and 266 registry patterns; cmd/common/cli.go: 157 lines scanned with 16 rule patterns and 266 registry patterns |
| dependencies | checked | 6 | ccaas_builder/go.mod: 10 dependencies parsed (10 pinned); docs/requirements.txt: 39 dependencies parsed (39 pinned); docs/source/requirements.txt: 1 dependencies parsed (1 pinned) |
| tls_code | checked | 32 | cmd/common/comm/client.go: TLS key-exchange settings read; cmd/common/comm/config.go: TLS key-exchange settings read; cmd/common/signer/signer.go: TLS key-exchange settings read |
| certificates | error (not checked) | 14 | docs/source/cc_service.md line 164: certificate could not be parsed (ValueError); docs/source/commands/peerchaincode.md line 161: certificate could not be parsed (ValueError); docs/source/discovery-cli.md line 137: certificate could not be parsed (ValueError) |
| certificates_and_keys | checked | 6 | docs/source/cc_service.md: certificates/keys parsed; docs/source/commands/peerchaincode.md: certificates/keys parsed; docs/source/discovery-cli.md: certificates/keys parsed |
| tls_key_exchange_groups | Insufficient data | 1 | internal/pkg/gateway/endorse.go line 102: not in the algorithm registry, not assessed: append(groups |
| tls_configuration | checked | 1 | internal/pkg/gateway/endorse.go: openssl TLS directives parsed |
| entropy | checked | 1 | random-number generation: 789 code files read with 0 macro definitions from the tree; 0 ineffective guard(s), 0 weak random-bytes provider(s), 0 weak key-generation site(s) |
| osv_advisories | checked | 1 | 385 pinned packages queried at OSV.dev; 6 affected |

_Long lists are grouped here; the full per-file list is in the JSON report, signed with the same key._

## 4. Assets examined and not examined

- certificates — error (not checked): docs/source/cc_service.md line 164: certificate could not be parsed (ValueError)
- certificates — error (not checked): docs/source/commands/peerchaincode.md line 161: certificate could not be parsed (ValueError)
- certificates — error (not checked): docs/source/discovery-cli.md line 137: certificate could not be parsed (ValueError)
- certificates — error (not checked): docs/source/discovery-cli.md line 146: certificate could not be parsed (ValueError)
- certificates — error (not checked): docs/source/discovery-cli.md line 155: certificate could not be parsed (ValueError)
- certificates — error (not checked): docs/source/discovery-cli.md line 164: certificate could not be parsed (ValueError)
- certificates — error (not checked): docs/source/discovery-cli.md line 403: certificate could not be parsed (ValueError)
- certificates — error (not checked): docs/source/discovery-cli.md line 411: certificate could not be parsed (ValueError)
- certificates — error (not checked): docs/source/discovery-cli.md line 417: certificate could not be parsed (ValueError)
- certificates — error (not checked): docs/source/discovery-cli.md line 447: certificate could not be parsed (ValueError)
- certificates — error (not checked): docs/source/discovery-cli.md line 452: certificate could not be parsed (ValueError)
- certificates — error (not checked): docs/source/discovery-cli.md line 457: certificate could not be parsed (ValueError)
- certificates — error (not checked): docs/source/discovery-cli.md line 462: certificate could not be parsed (ValueError)
- certificates — error (not checked): docs/wrappers/peer_chaincode_postscript.md line 20: certificate could not be parsed (ValueError)
- tls_key_exchange_groups — Insufficient data: internal/pkg/gateway/endorse.go line 102: not in the algorithm registry, not assessed: append(groups

## 5. Architecture overview

Static review of the source tree hyperledger-fabric at 13ef9e5ee59466b152c8fe65b3a095234de671f7. 814 files analysed; of 2874 files, 1650 are test, fuzzing, benchmark or example code and were left out, 410 are not read by any analyzer, 0 exceed the per-file limit and 0 did not fit the total limit. Files no analyzer reads include: .dockerignore, .gitattributes, .github/ISSUE_TEMPLATE/bug.yaml, .github/ISSUE_TEMPLATE/feature.yaml, .github/ISSUE_TEMPLATE/workitem.yaml. 3582 files in build-output or dependency-cache directories (.git, .hg, .venv, __pycache__, build, dist, node_modules, target, vendor, venv) were not read. No requests were sent to the owner's systems.

## 6. Overall security posture

- Indicative posture index: **84** / 100 — _Derived from findings in scope (confirmed and potential issues weighted by severity). Indicative only; not comparable across differently scoped audits._
- Quantum-vulnerable share of inventory: 37.8%

## 7. Detailed findings

### QSI-2026-17550 — google.golang.org/grpc v1.83.1 is affected by GHSA-2v4p-qf9q-27wj (CVE-2026-84445, GO-2026-6443)

- Severity: **High** · Classification: Known vulnerable component · Confidence: Medium
- Affected asset: `dependency:Go/google.golang.org/grpc@v1.83.1`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 10:32 UTC
- Priority score: 50.2 / 100
- CVSS v3.1: not applicable

OSV.dev reports GHSA-2v4p-qf9q-27wj (CVE-2026-84445, GO-2026-6443) for Go package google.golang.org/grpc at version v1.83.1: gRPC-Go xDS servers: Denial of Service (DoS) via crash due to missing `:authority` and `Host` headers. The advisory lists only unexported functions (google.golang.org/grpc/internal/transport.http2Server.HandleStreams, google.golang.org/grpc/internal/transport.http2Server.operateHeaders, google.golang.org/grpc/internal/xds/server.RouteAndProcess), which code outside the package cannot call by name, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-2v4p-qf9q-27wj
```

**Evidence.**

_tool_output · [OSV.dev GHSA-2v4p-qf9q-27wj](https://osv.dev/vulnerability/GHSA-2v4p-qf9q-27wj) · line 15 · SHA-256 3566bf539cd1bed726145fc02332a18308f9a065bb8b992c0e44deb9ec44221a_

```
{"id": "GHSA-2v4p-qf9q-27wj", "aliases": ["CVE-2026-84445", "GO-2026-6443"], "modified": "2026-09-25T18:00:05.270054427Z", "summary": "gRPC-Go xDS servers: Denial of Service (DoS) via crash due to missing `:authority` and `Host` headers", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X"}], "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed. A Go function counts only in a file that also names its package (a method: its type); unexported functions only through the exported ones.

**Recommendation.** Upgrade to a fixed version (1.82.2, 1.83.2, 1.84.0-dev.0.20260825144003-d5a41119e0e3, 1.85.0-dev.0.20260825072537-93e31b48545e).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-17522 — Quantum-vulnerable ECDSA: transaction and message signing (1 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:ECDSA:transaction_signing`
- Data source: cmd/common/signer/signer.go
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.3.0 · 2026-11-06 10:32 UTC
- Priority score: 35.6 / 100
- CVSS v3.1: not applicable

2 reference(s) to ECDSA across 1 file(s), e.g. cmd/common/signer/signer.go:11. Role, judged from paths, function names and nearby code: transaction and message signing. A CRQC derives the private key from a public key that is already known (on chain after the first spend, in reused addresses): funds and approvals controlled by these keys need a migration path.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open cmd/common/signer/signer.go:11 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [cmd/common/signer/signer.go](https://github.com/hyperledger/fabric/blob/13ef9e5ee59466b152c8fe65b3a095234de671f7/cmd/common/signer/signer.go#L11) · line 11 · SHA-256 8ca7cf4a477c1e85b6a04804930e34f52fce6fc67c009fa9a7197362c13fc24d_

```
   10 | 	"crypto"
   11 | 	"crypto/ecdsa"
   12 | 	"crypto/ed25519"
```

_file_excerpt · [cmd/common/signer/signer.go](https://github.com/hyperledger/fabric/blob/13ef9e5ee59466b152c8fe65b3a095234de671f7/cmd/common/signer/signer.go#L150) · line 150 · SHA-256 f011e69596df627e3b3b07a4a83601487a855461b916d998f1b2d2d6c355769d_

```
  149 | func signECDSA(k *ecdsa.PrivateKey, digest []byte) (signature []byte, err error) {
  150 | 	r, s, err := ecdsa.Sign(rand.Reader, k, digest)
  151 | 	if err != nil {
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains adopt them.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-17523 — Quantum-vulnerable Ed25519: transaction and message signing (1 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:Ed25519:transaction_signing`
- Data source: cmd/common/signer/signer.go
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.3.0 · 2026-11-06 10:32 UTC
- Priority score: 35.6 / 100
- CVSS v3.1: not applicable

1 reference(s) to Ed25519 across 1 file(s), e.g. cmd/common/signer/signer.go:103. Role, judged from paths, function names and nearby code: transaction and message signing. A CRQC derives the private key from a public key that is already known (on chain after the first spend, in reused addresses): funds and approvals controlled by these keys need a migration path.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open cmd/common/signer/signer.go:103 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [cmd/common/signer/signer.go](https://github.com/hyperledger/fabric/blob/13ef9e5ee59466b152c8fe65b3a095234de671f7/cmd/common/signer/signer.go#L103) · line 103 · SHA-256 1fadca5c51485178e981fb470c56ccaa27c5299f4e25a910b8840674df903560_

```
  102 | 	case ed25519.PrivateKey:
  103 | 		return ed25519.Sign(si.key.(ed25519.PrivateKey), msg), nil
  104 | 	default:
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains adopt them.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-17524 — Quantum-vulnerable ECDSA: role not determined (8 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:ECDSA:general`
- Data source: common/crypto/sanitize.go
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.3.0 · 2026-11-06 10:32 UTC
- Priority score: 34.2 / 100
- CVSS v3.1: not applicable

13 reference(s) to ECDSA across 8 file(s), e.g. common/crypto/sanitize.go:10. Role, judged from paths, function names and nearby code: role not determined. The code does not show what the keys protect; review decides the priority.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open common/crypto/sanitize.go:10 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [common/crypto/sanitize.go](https://github.com/hyperledger/fabric/blob/13ef9e5ee59466b152c8fe65b3a095234de671f7/common/crypto/sanitize.go#L10) · line 10 · SHA-256 7084b7c99f554eecd0fd9091a867a2f25ebd736f4f12161ea4ea116842e57482_

```
    9 | import (
   10 | 	"crypto/ecdsa"
   11 | 	"crypto/x509"
```

_file_excerpt · [common/crypto/tlsgen/key.go](https://github.com/hyperledger/fabric/blob/13ef9e5ee59466b152c8fe65b3a095234de671f7/common/crypto/tlsgen/key.go#L11) · line 11 · SHA-256 9dcdbc8c39c2a748e23237a075a1ee592602e309634b495ca8ee95d667e3de28_

```
   10 | 	"crypto"
   11 | 	"crypto/ecdsa"
   12 | 	"crypto/elliptic"
```

_file_excerpt · [common/crypto/tlsgen/key.go](https://github.com/hyperledger/fabric/blob/13ef9e5ee59466b152c8fe65b3a095234de671f7/common/crypto/tlsgen/key.go#L27) · line 27 · SHA-256 36cd8f56fd06275a66a36a49980ed0bc027499c6a15d1086ccc80ea2b105b5bc_

```
   26 | func newPrivKey() (*ecdsa.PrivateKey, []byte, error) {
   27 | 	privateKey, err := ecdsa.GenerateKey(elliptic.P256(), rand.Reader)
   28 | 	if err != nil {
```

_file_excerpt · [integration/nwo/signingid.go](https://github.com/hyperledger/fabric/blob/13ef9e5ee59466b152c8fe65b3a095234de671f7/integration/nwo/signingid.go#L10) · line 10 · SHA-256 7983932d009be78f478f371ae58c3f86b9f6b72f687b9ed011a4aee4ad95d71d_

```
    9 | import (
   10 | 	"crypto/ecdsa"
   11 | 	"crypto/ed25519"
```

_file_excerpt · [integration/nwo/signingid.go](https://github.com/hyperledger/fabric/blob/13ef9e5ee59466b152c8fe65b3a095234de671f7/integration/nwo/signingid.go#L62) · line 62 · SHA-256 1fa03b22a497e32b00bc23cf5b6dd3ef33e3a433f7dcdec570513ad35a1e9e84_

```
   61 | 	case *ecdsa.PrivateKey:
   62 | 		r, _s, err := ecdsa.Sign(rand.Reader, k, digest[:])
   63 | 		if err != nil {
```

_file_excerpt · [integration/pkcs11/p11key.go](https://github.com/hyperledger/fabric/blob/13ef9e5ee59466b152c8fe65b3a095234de671f7/integration/pkcs11/p11key.go#L11) · line 11 · SHA-256 7c3c9ad2241d45350461ababc968c86b8e98df8d015e0369a24a0fe7b5d20d74_

```
   10 | 	"crypto"
   11 | 	"crypto/ecdsa"
   12 | 	"encoding/asn1"
```

_file_excerpt · [internal/cryptogen/ca/ca.go](https://github.com/hyperledger/fabric/blob/13ef9e5ee59466b152c8fe65b3a095234de671f7/internal/cryptogen/ca/ca.go#L10) · line 10 · SHA-256 28e1ebfdc5314af7f1518d8c3b1f1fe1dedb76343c9bd9f0c3d65a20ece8c7cd_

```
    9 | 	"crypto"
   10 | 	"crypto/ecdsa"
   11 | 	"crypto/ed25519"
```

_file_excerpt · [internal/cryptogen/csp/csp.go](https://github.com/hyperledger/fabric/blob/13ef9e5ee59466b152c8fe65b3a095234de671f7/internal/cryptogen/csp/csp.go#L10) · line 10 · SHA-256 28e1ebfdc5314af7f1518d8c3b1f1fe1dedb76343c9bd9f0c3d65a20ece8c7cd_

```
    9 | 	"crypto"
   10 | 	"crypto/ecdsa"
   11 | 	"crypto/ed25519"
```

_file_excerpt · [internal/cryptogen/csp/csp.go](https://github.com/hyperledger/fabric/blob/13ef9e5ee59466b152c8fe65b3a095234de671f7/internal/cryptogen/csp/csp.go#L85) · line 85 · SHA-256 145d377cd11be49991dd933abde274f50113c7f05784293ca783b26d0d4be8ff_

```
   84 | 	case "ecdsa":
   85 | 		priv, err = ecdsa.GenerateKey(elliptic.P256(), rand.Reader)
   86 | 	case "ed25519":
```

_file_excerpt · [internal/cryptogen/csp/csp.go](https://github.com/hyperledger/fabric/blob/13ef9e5ee59466b152c8fe65b3a095234de671f7/internal/cryptogen/csp/csp.go#L130) · line 130 · SHA-256 c418dec4450d28371606fd0d96d57a9f6595572b84a49e8a17bab4e8045d13d1_

```
  129 | func (e *ECDSASigner) Sign(rand io.Reader, digest []byte, opts crypto.SignerOpts) ([]byte, error) {
  130 | 	r, s, err := ecdsa.Sign(rand, e.PrivateKey, digest)
  131 | 	if err != nil {
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it; introduce an abstraction layer for crypto-agility.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-17525 — Quantum-vulnerable ECDH: role not determined (2 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:ECDH:general`
- Data source: common/crypto/tlsgen/key.go
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.3.0 · 2026-11-06 10:32 UTC
- Priority score: 34.2 / 100
- CVSS v3.1: not applicable

2 reference(s) to ECDH across 2 file(s), e.g. common/crypto/tlsgen/key.go:125. Role, judged from paths, function names and nearby code: role not determined. The code does not show what the keys protect; review decides the priority.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open common/crypto/tlsgen/key.go:125 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [common/crypto/tlsgen/key.go](https://github.com/hyperledger/fabric/blob/13ef9e5ee59466b152c8fe65b3a095234de671f7/common/crypto/tlsgen/key.go#L125) · line 125 · SHA-256 6c9e8147d92efa0629fa152aaeed0ae0b611281b61afef381df8b726d2b460c9_

```
  124 | func computeSKI(key *ecdsa.PublicKey) ([]byte, error) {
  125 | 	ecdhPk, err := key.ECDH()
  126 | 	if err != nil {
```

_file_excerpt · [internal/cryptogen/ca/ca.go](https://github.com/hyperledger/fabric/blob/13ef9e5ee59466b152c8fe65b3a095234de671f7/internal/cryptogen/ca/ca.go#L176) · line 176 · SHA-256 d5a2c3f468ada1cca9f2bac4b3877e1ad37dd14c9c244c67525edf6d6079d809_

```
  175 | 	case *ecdsa.PrivateKey:
  176 | 		ecdhKey, err := kk.ECDH()
  177 | 		if err != nil {
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Classify each usage, record data lifetimes, and plan migration to Hybrid key establishment with ML-KEM (FIPS 203), e.g. X25519MLKEM768 in TLS 1.3 or mlkem768x25519-sha256 in SSH; introduce an abstraction layer for crypto-agility.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-17527 — Quantum-vulnerable Ed25519: role not determined (2 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:Ed25519:general`
- Data source: integration/nwo/signingid.go
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.3.0 · 2026-11-06 10:32 UTC
- Priority score: 34.2 / 100
- CVSS v3.1: not applicable

3 reference(s) to Ed25519 across 2 file(s), e.g. integration/nwo/signingid.go:72. Role, judged from paths, function names and nearby code: role not determined. The code does not show what the keys protect; review decides the priority.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open integration/nwo/signingid.go:72 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [integration/nwo/signingid.go](https://github.com/hyperledger/fabric/blob/13ef9e5ee59466b152c8fe65b3a095234de671f7/integration/nwo/signingid.go#L72) · line 72 · SHA-256 1cd06a572b80e81212b611338acaada11769b9a861aad4a3dbef55253e270ee0_

```
   71 | 	case ed25519.PrivateKey:
   72 | 		return ed25519.Sign(k, msg), nil
   73 | 	default:
```

_file_excerpt · [internal/cryptogen/csp/csp.go](https://github.com/hyperledger/fabric/blob/13ef9e5ee59466b152c8fe65b3a095234de671f7/internal/cryptogen/csp/csp.go#L87) · line 87 · SHA-256 a62ce5e5d32b9cf92b326954f35a68c01f52ece0f651146afe1d287e0e0816c4_

```
   86 | 	case "ed25519":
   87 | 		_, priv, err = ed25519.GenerateKey(rand.Reader)
   88 | 	default:
```

_file_excerpt · [internal/cryptogen/csp/csp.go](https://github.com/hyperledger/fabric/blob/13ef9e5ee59466b152c8fe65b3a095234de671f7/internal/cryptogen/csp/csp.go#L182) · line 182 · SHA-256 3009ad2f91fe009ff14480bb74fee558cbbb53477de28a15f1f99cabcf2eefaa_

```
  181 | func (e *ED25519Signer) Sign(rand io.Reader, msg []byte, opts crypto.SignerOpts) ([]byte, error) {
  182 | 	sig := ed25519.Sign(e.PrivateKey, msg)
  183 | 
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it; introduce an abstraction layer for crypto-agility.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-17528 — Quantum-vulnerable ECDSA: authentication and identity (certificates, tokens, device attestation) (1 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:ECDSA:authentication`
- Data source: msp/cert.go
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.3.0 · 2026-11-06 10:32 UTC
- Priority score: 34.2 / 100
- CVSS v3.1: not applicable

1 reference(s) to ECDSA across 1 file(s), e.g. msp/cert.go:21. Role, judged from paths, function names and nearby code: authentication and identity (certificates, tokens, device attestation). Short-lived authentication stays safe until a CRQC exists; long-lived identities (device attestation, CA and SSH keys) need a plan earlier.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open msp/cert.go:21 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [msp/cert.go](https://github.com/hyperledger/fabric/blob/13ef9e5ee59466b152c8fe65b3a095234de671f7/msp/cert.go#L21) · line 21 · SHA-256 e90e392283b6e3044a88683aa385394d372eda877012ec6cd9f21b1bb1e1c94c_

```
   20 | 	"bytes"
   21 | 	"crypto/ecdsa"
   22 | 	"crypto/x509"
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Keep credentials short-lived and plan ML-DSA certificates, tokens and keys as the ecosystem supports them.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-17526 — MD5 used in common/deliverclient/orderers/connection.go

- Severity: **Medium** · Classification: Potential cryptographic risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `file:common/deliverclient/orderers/connection.go`
- Data source: common/deliverclient/orderers/connection.go
- Detection method: Regular-expression matching of language-specific API patterns.
- Analyzer: source_code 1.3.0 · 2026-11-06 10:32 UTC
- Priority score: 33.7 / 100
- CVSS v3.1: not applicable

2 call site(s) of MD5 (first at line 11).

**Potential impact.** If used for signatures, password storage, integrity against attackers or token generation, collisions/preimages may be exploitable. Non-security checksums are acceptable.

**Reproduction steps.**

```
Open line 11 in the supplied file common/deliverclient/orderers/connection.go and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [common/deliverclient/orderers/connection.go](https://github.com/hyperledger/fabric/blob/13ef9e5ee59466b152c8fe65b3a095234de671f7/common/deliverclient/orderers/connection.go#L11) · line 11 · SHA-256 5f725154eb3b4e46d92f2507aa51c107f83335a8f91b6bb0f8e819e776baa85c_

```
    9 | import (
   10 | 	"bytes"
   11 | 	"crypto/md5"
   12 | 	"crypto/sha256"
   13 | 	"fmt"
```

_file_excerpt · [common/deliverclient/orderers/connection.go](https://github.com/hyperledger/fabric/blob/13ef9e5ee59466b152c8fe65b3a095234de671f7/common/deliverclient/orderers/connection.go#L44) · line 44 · SHA-256 2d175c78e52285fd59899e3efc4903f3fde7328df11f4f8fb9711d5b36d78369_

```
   42 | 
   43 | 	if e.RootCerts != nil {
   44 | 		hasher := md5.New()
   45 | 		for _, cert := range e.RootCerts {
   46 | 			hasher.Write(cert)
```

**Limitations of the check.** Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Replace with SHA-256/SHA-3 (or Argon2/bcrypt for passwords) where security-relevant.

**Retest procedure.** Re-scan the source and review the call sites listed in the evidence.

### QSI-2026-17529 — Quantum-vulnerable ECDSA key in certificate (ca.org1.example.com)

- Severity: **Low** · Classification: Long-term post-quantum risk · Confidence: High
- Affected asset: `certificate:ca.org1.example.com`
- Data source: sampleconfig/msp/cacerts/cacert.pem
- Detection method: X.509 public key algorithm identification.
- Analyzer: certificates 1.3.0 · 2026-11-06 10:32 UTC
- Priority score: 40.0 / 100
- CVSS v3.1: not applicable

The certificate ca.org1.example.com uses a ECDSA secp256r1 public key, valid until 2027-11-10. ECDSA is broken by Shor's algorithm on a CRQC.

**Potential impact.** For authentication, risk materializes only once a CRQC exists while the key/certificate is still trusted. Certificates are short-lived, so the main concern is the PKI and long-lived roots/intermediates.

**Reproduction steps.**

```
openssl x509 -in sampleconfig/msp/cacerts/cacert.pem -noout -text | grep -A2 'Public Key Algorithm'
```

**Evidence.**

_certificate · sampleconfig/msp/cacerts/cacert.pem · line 1 · SHA-256 7d234b9db694a12867c13b15237565e0ed9ef98c6d0b3ce9ac79f192e1930cc1_

```
Subject: CN=ca.org1.example.com,OU=COP,O=org1.example.com,L=San Francisco,ST=California,C=US
Issuer: CN=ca.org1.example.com,OU=COP,O=org1.example.com,L=San Francisco,ST=California,C=US
Serial: bd5f1009f3e73a789a827c31d49bfe56
Not before: 2017-11-12T13:41:11+00:00
Not after: 2027-11-10T13:41:11+00:00
Public key: ECDSA secp256r1
Signature algorithm: 1.2.840.10045.4.3.2 (ECDSA)
Signature hash: sha256
CA: True
SAN: -
SHA-256 fingerprint: dfbbd654ce60aaac86dc995580aad33347a4a5baaf484ca64892cebd8ed014f2
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability.

**Recommendation.** Track in the PQC inventory; prefer short certificate lifetimes; follow CA/Browser Forum and NIST PQC transition guidance for ML-DSA certificates.

**Retest procedure.** Re-audit once PQC or hybrid certificates are deployed.

### QSI-2026-17530 — Quantum-vulnerable ECDSA key in certificate (Org2-child1)

- Severity: **Low** · Classification: Long-term post-quantum risk · Confidence: High
- Affected asset: `certificate:Org2-child1`
- Data source: sampleconfig/msp/tlsintermediatecerts/tlsintermediate.pem
- Detection method: X.509 public key algorithm identification.
- Analyzer: certificates 1.3.0 · 2026-11-06 10:32 UTC
- Priority score: 40.0 / 100
- CVSS v3.1: not applicable

The certificate Org2-child1 uses a ECDSA secp256r1 public key, valid until 2027-05-06. ECDSA is broken by Shor's algorithm on a CRQC.

**Potential impact.** For authentication, risk materializes only once a CRQC exists while the key/certificate is still trusted. Certificates are short-lived, so the main concern is the PKI and long-lived roots/intermediates.

**Reproduction steps.**

```
openssl x509 -in sampleconfig/msp/tlsintermediatecerts/tlsintermediate.pem -noout -text | grep -A2 'Public Key Algorithm'
```

**Evidence.**

_certificate · sampleconfig/msp/tlsintermediatecerts/tlsintermediate.pem · line 1 · SHA-256 d5fc619450742a088d4757537f3f7311c9445391166ce0c5da0d55aa1c6047ae_

```
Subject: CN=Org2-child1,O=Org2-child1,L=San Francisco,ST=California,C=US
Issuer: CN=Org2,O=Org2,L=San Francisco,ST=California,C=US
Serial: 36982801213d7e2d28a1954a727c2767
Not before: 2017-05-08T09:30:34+00:00
Not after: 2027-05-06T09:30:34+00:00
Public key: ECDSA secp256r1
Signature algorithm: 1.2.840.10045.4.3.2 (ECDSA)
Signature hash: sha256
CA: True
SAN: -
SHA-256 fingerprint: 9b616809f5500b33c2b0e19be94a8bd1122b049dd8b19b957487ad4ed0d24ed5
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability.

**Recommendation.** Track in the PQC inventory; prefer short certificate lifetimes; follow CA/Browser Forum and NIST PQC transition guidance for ML-DSA certificates.

**Retest procedure.** Re-audit once PQC or hybrid certificates are deployed.

### QSI-2026-17539 — golang.org/x/crypto v0.58.0 is affected by GO-2026-5932 (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:Go/golang.org/x/crypto@v0.58.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 10:32 UTC
- Priority score: 20.3 / 100
- CVSS v3.1: not applicable

OSV.dev reports GO-2026-5932 for Go package golang.org/x/crypto at version v0.58.0: The golang.org/x/crypto/openpgp package is unmaintained, unsafe by design, and has known security issues. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-5932
```

**Evidence.**

_tool_output · [OSV.dev GO-2026-5932](https://osv.dev/vulnerability/GO-2026-5932) · line 108 · SHA-256 79b7a13fb7767fbace049b5199d913b96ffabce881fc497fd2222d40644da151_

```
{"id": "GO-2026-5932", "aliases": [], "modified": "2026-11-02T22:15:06.677088389Z", "summary": "The golang.org/x/crypto/openpgp package is unmaintained, unsafe by design, and has known security issues", "severity": null, "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed. A Go function counts only in a file that also names its package (a method: its type); unexported functions only through the exported ones.

**Recommendation.** Triage the advisory; upgrade to a fixed version (0.58.1-0.20261009181718-2f1f834330b2) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-17531 — golang.org/x/net v0.57.0 is affected by GO-2026-6603 (CVE-2026-78659) (no severity rating)

- Severity: **Info** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:Go/golang.org/x/net@v0.57.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 10:32 UTC
- Priority score: 17.8 / 100
- CVSS v3.1: not applicable

OSV.dev reports GO-2026-6603 (CVE-2026-78659) for Go package golang.org/x/net at version v0.57.0: HTTP/2 server memory exhaustion due to Trailer headers in net/http. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. None of the affected functions (golang.org/x/net/http2.ClientConn.Close, golang.org/x/net/http2.ClientConn.Ping, golang.org/x/net/http2.ClientConn.RoundTrip, golang.org/x/net/http2.ClientConn.Shutdown, golang.org/x/net/http2.ConfigureServer, golang.org/x/net/http2.ConfigureTransport …) is named in the audited code: the advisory does not apply unless they are reached indirectly (traits, macros, other dependencies).

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-6603
```

**Evidence.**

_tool_output · [OSV.dev GO-2026-6603](https://osv.dev/vulnerability/GO-2026-6603) · line 15 · SHA-256 9e43850e0da48e9d00589cc2bffb372f39ec5e5a280f2f4b04520a91328fd703_

```
{"id": "GO-2026-6603", "aliases": ["BIT-golang-2026-78659", "CVE-2026-78659"], "modified": "2026-10-16T09:55:47.068117441Z", "summary": "HTTP/2 server memory exhaustion due to Trailer headers in net/http", "severity": null, "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed. A Go function counts only in a file that also names its package (a method: its type); unexported functions only through the exported ones.

**Recommendation.** Triage the advisory; upgrade to a fixed version (0.60.0) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-17532 — golang.org/x/net v0.57.0 is affected by GO-2026-6610 (CVE-2026-78660) (no severity rating)

- Severity: **Info** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:Go/golang.org/x/net@v0.57.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 10:32 UTC
- Priority score: 17.8 / 100
- CVSS v3.1: not applicable

OSV.dev reports GO-2026-6610 (CVE-2026-78660) for Go package golang.org/x/net at version v0.57.0: HTTP/2 transport accepts malformed framing-related headers in net/http. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. None of the affected functions (golang.org/x/net/http2.Transport.NewClientConn, golang.org/x/net/http2.Transport.RoundTrip, golang.org/x/net/http2.Transport.RoundTripOpt, golang.org/x/net/http2.clientConnPool.GetClientConn, golang.org/x/net/http2.clientConnReadLoop.handleResponse, golang.org/x/net/http2.noDialClientConnPool.GetClientConn …) is named in the audited code: the advisory does not apply unless they are reached indirectly (traits, macros, other dependencies).

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-6610
```

**Evidence.**

_tool_output · [OSV.dev GO-2026-6610](https://osv.dev/vulnerability/GO-2026-6610) · line 15 · SHA-256 1b823e53f27093797b8a7909032006e1f0f818f04118ad593a4641236392faa9_

```
{"id": "GO-2026-6610", "aliases": ["BIT-golang-2026-78660", "CVE-2026-78660"], "modified": "2026-10-16T09:56:04.364467528Z", "summary": "HTTP/2 transport accepts malformed framing-related headers in net/http", "severity": null, "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed. A Go function counts only in a file that also names its package (a method: its type); unexported functions only through the exported ones.

**Recommendation.** Triage the advisory; upgrade to a fixed version (0.60.0) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-17533 — golang.org/x/net v0.57.0 is affected by GO-2026-6611 (CVE-2026-78669) (no severity rating)

- Severity: **Info** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:Go/golang.org/x/net@v0.57.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 10:32 UTC
- Priority score: 17.8 / 100
- CVSS v3.1: not applicable

OSV.dev reports GO-2026-6611 (CVE-2026-78669) for Go package golang.org/x/net at version v0.57.0: Excessive CPU consumption from repeated initial window changes in net/http. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. None of the affected functions (golang.org/x/net/http2.ClientConn.Close, golang.org/x/net/http2.ClientConn.Ping, golang.org/x/net/http2.ClientConn.RoundTrip, golang.org/x/net/http2.ClientConn.Shutdown, golang.org/x/net/http2.ClientConn.addStreamLocked, golang.org/x/net/http2.ConfigureServer …) is named in the audited code: the advisory does not apply unless they are reached indirectly (traits, macros, other dependencies).

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-6611
```

**Evidence.**

_tool_output · [OSV.dev GO-2026-6611](https://osv.dev/vulnerability/GO-2026-6611) · line 15 · SHA-256 c9b9f78637131224c5d4073e44c47b7cce490fc5526e3d6b0697b43bc85cab2f_

```
{"id": "GO-2026-6611", "aliases": ["BIT-golang-2026-78669", "CVE-2026-78669"], "modified": "2026-10-16T09:55:38.952277866Z", "summary": "Excessive CPU consumption from repeated initial window changes in net/http", "severity": null, "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed. A Go function counts only in a file that also names its package (a method: its type); unexported functions only through the exported ones.

**Recommendation.** Triage the advisory; upgrade to a fixed version (0.60.0) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-17534 — golang.org/x/net v0.57.0 is affected by GO-2026-6612 (CVE-2026-78663) (no severity rating)

- Severity: **Info** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:Go/golang.org/x/net@v0.57.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 10:32 UTC
- Priority score: 17.8 / 100
- CVSS v3.1: not applicable

OSV.dev reports GO-2026-6612 (CVE-2026-78663) for Go package golang.org/x/net at version v0.57.0: Double flow control refund on HTTP/2 server streams in net/http. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. None of the affected functions (golang.org/x/net/http2.ClientConn.Close, golang.org/x/net/http2.ClientConn.Ping, golang.org/x/net/http2.ClientConn.RoundTrip, golang.org/x/net/http2.ClientConn.Shutdown, golang.org/x/net/http2.ConfigureServer, golang.org/x/net/http2.ConfigureTransport …) is named in the audited code: the advisory does not apply unless they are reached indirectly (traits, macros, other dependencies).

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-6612
```

**Evidence.**

_tool_output · [OSV.dev GO-2026-6612](https://osv.dev/vulnerability/GO-2026-6612) · line 15 · SHA-256 1471910f88c9bbf8395a304fd82510f61567373756002de8bcdc3fbe305890cb_

```
{"id": "GO-2026-6612", "aliases": ["BIT-golang-2026-78663", "CVE-2026-78663"], "modified": "2026-10-16T09:55:54.129082194Z", "summary": "Double flow control refund on HTTP/2 server streams in net/http", "severity": null, "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed. A Go function counts only in a file that also names its package (a method: its type); unexported functions only through the exported ones.

**Recommendation.** Triage the advisory; upgrade to a fixed version (0.60.0) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-17535 — golang.org/x/net v0.57.0 is affected by GO-2026-6617 (CVE-2026-97032) (no severity rating)

- Severity: **Info** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:Go/golang.org/x/net@v0.57.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 10:32 UTC
- Priority score: 17.8 / 100
- CVSS v3.1: not applicable

OSV.dev reports GO-2026-6617 (CVE-2026-97032) for Go package golang.org/x/net at version v0.57.0: HTTP/2 server crash due to HPACK encoder race in net/http. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. None of the affected functions (golang.org/x/net/http2.ClientConn.Close, golang.org/x/net/http2.ClientConn.Ping, golang.org/x/net/http2.ClientConn.RoundTrip, golang.org/x/net/http2.ClientConn.Shutdown, golang.org/x/net/http2.ConfigureServer, golang.org/x/net/http2.ConfigureTransport …) is named in the audited code: the advisory does not apply unless they are reached indirectly (traits, macros, other dependencies).

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-6617
```

**Evidence.**

_tool_output · [OSV.dev GO-2026-6617](https://osv.dev/vulnerability/GO-2026-6617) · line 15 · SHA-256 b948c88d959bc78948c7e3b7a746ac4da179933798e9735d02870080906cfc96_

```
{"id": "GO-2026-6617", "aliases": ["BIT-golang-2026-97032", "CVE-2026-97032"], "modified": "2026-10-16T09:55:57.350751224Z", "summary": "HTTP/2 server crash due to HPACK encoder race in net/http", "severity": null, "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed. A Go function counts only in a file that also names its package (a method: its type); unexported functions only through the exported ones.

**Recommendation.** Triage the advisory; upgrade to a fixed version (0.60.0) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-17536 — golang.org/x/net v0.57.0 is affected by GO-2026-6860 (CVE-2026-78661) (no severity rating)

- Severity: **Info** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:Go/golang.org/x/net@v0.57.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 10:32 UTC
- Priority score: 17.8 / 100
- CVSS v3.1: not applicable

OSV.dev reports GO-2026-6860 (CVE-2026-78661) for Go package golang.org/x/net at version v0.57.0: Avoid quadratic complexity when coalescing text nodes in html in golang.org/x/net. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. None of the affected functions (golang.org/x/net/html.Parse, golang.org/x/net/html.ParseFragment, golang.org/x/net/html.ParseFragmentWithOptions, golang.org/x/net/html.ParseWithOptions, golang.org/x/net/html.parser.addText, golang.org/x/net/html.parser.fosterParent …) is named in the audited code: the advisory does not apply unless they are reached indirectly (traits, macros, other dependencies).

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-6860
```

**Evidence.**

_tool_output · [OSV.dev GO-2026-6860](https://osv.dev/vulnerability/GO-2026-6860) · line 15 · SHA-256 1f106c45371219bac0158f7ce44e57c439f50f0c32898616d1563f14cadb1b28_

```
{"id": "GO-2026-6860", "aliases": ["CVE-2026-78661"], "modified": "2026-10-27T21:30:04.890809062Z", "summary": "Avoid quadratic complexity when coalescing text nodes in html in golang.org/x/net", "severity": null, "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed. A Go function counts only in a file that also names its package (a method: its type); unexported functions only through the exported ones.

**Recommendation.** Triage the advisory; upgrade to a fixed version (0.62.0) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-17537 — golang.org/x/net v0.57.0 is affected by GO-2026-6866 (CVE-2026-97045) (no severity rating)

- Severity: **Info** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:Go/golang.org/x/net@v0.57.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 10:32 UTC
- Priority score: 17.8 / 100
- CVSS v3.1: not applicable

OSV.dev reports GO-2026-6866 (CVE-2026-97045) for Go package golang.org/x/net at version v0.57.0: Check all ancestor namespace transitions when rendering raw text in html in golang.org/x/net. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. None of the affected functions (golang.org/x/net/html.Render, golang.org/x/net/html.childTextNodesAreLiteral) is named in the audited code: the advisory does not apply unless they are reached indirectly (traits, macros, other dependencies).

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-6866
```

**Evidence.**

_tool_output · [OSV.dev GO-2026-6866](https://osv.dev/vulnerability/GO-2026-6866) · line 15 · SHA-256 102267a016bc5eef7979a90b1ddd2288ff36b09ab6fa040c808e62f3b55c1f42_

```
{"id": "GO-2026-6866", "aliases": ["CVE-2026-97045"], "modified": "2026-10-27T21:45:08.978077289Z", "summary": "Check all ancestor namespace transitions when rendering raw text in html in golang.org/x/net", "severity": null, "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed. A Go function counts only in a file that also names its package (a method: its type); unexported functions only through the exported ones.

**Recommendation.** Triage the advisory; upgrade to a fixed version (0.62.0) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-17538 — golang.org/x/text v0.40.0 is affected by GO-2026-6629 (CVE-2026-56851) (no severity rating)

- Severity: **Info** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:Go/golang.org/x/text@v0.40.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 10:32 UTC
- Priority score: 17.8 / 100
- CVSS v3.1: not applicable

OSV.dev reports GO-2026-6629 (CVE-2026-56851) for Go package golang.org/x/text at version v0.40.0: Panic parsing crafted input in x/text/secure/precis in golang.org/x/text. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. None of the affected functions (golang.org/x/text/secure/precis.Profile.Append, golang.org/x/text/secure/precis.Profile.AppendCompareKey, golang.org/x/text/secure/precis.Profile.Bytes, golang.org/x/text/secure/precis.Profile.Compare, golang.org/x/text/secure/precis.Profile.CompareKey, golang.org/x/text/secure/precis.Profile.NewTransformer …) is named in the audited code: the advisory does not apply unless they are reached indirectly (traits, macros, other dependencies).

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-6629
```

**Evidence.**

_tool_output · [OSV.dev GO-2026-6629](https://osv.dev/vulnerability/GO-2026-6629) · line 18 · SHA-256 657419214ae5882e9b4ead4f61526561fcf5d98c9624b1701de82958bdc592d2_

```
{"id": "GO-2026-6629", "aliases": ["CVE-2026-56851"], "modified": "2026-10-20T10:42:24.514593111Z", "summary": "Panic parsing crafted input in x/text/secure/precis in golang.org/x/text", "severity": null, "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed. A Go function counts only in a file that also names its package (a method: its type); unexported functions only through the exported ones.

**Recommendation.** Triage the advisory; upgrade to a fixed version (0.41.0) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-17540 — golang.org/x/net v0.55.0 is affected by GO-2026-5942 (CVE-2026-46600) (no severity rating)

- Severity: **Info** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:Go/golang.org/x/net@v0.55.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 10:32 UTC
- Priority score: 17.8 / 100
- CVSS v3.1: not applicable

OSV.dev reports GO-2026-5942 (CVE-2026-46600) for Go package golang.org/x/net at version v0.55.0: Parsing an invalid SVCB or HTTPS RR can panic in golang.org/x/net/dns/dnsmessage. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. None of the affected functions (golang.org/x/net/dns/dnsmessage.Message.Unpack, golang.org/x/net/dns/dnsmessage.Parser.Additional, golang.org/x/net/dns/dnsmessage.Parser.AllAdditionals, golang.org/x/net/dns/dnsmessage.Parser.AllAnswers, golang.org/x/net/dns/dnsmessage.Parser.AllAuthorities, golang.org/x/net/dns/dnsmessage.Parser.Answer …) is named in the audited code: the advisory does not apply unless they are reached indirectly (traits, macros, other dependencies).

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-5942
```

**Evidence.**

_tool_output · [OSV.dev GO-2026-5942](https://osv.dev/vulnerability/GO-2026-5942) · line 11 · SHA-256 269e9768d90ae705c6a1a4bc91c14ed7037c3197d295e15bd8bdc0e4fd623f21_

```
{"id": "GO-2026-5942", "aliases": ["BIT-golang-2026-46600", "CVE-2026-46600"], "modified": "2026-08-17T12:25:32.471119200Z", "summary": "Parsing an invalid SVCB or HTTPS RR can panic in golang.org/x/net/dns/dnsmessage", "severity": null, "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed. A Go function counts only in a file that also names its package (a method: its type); unexported functions only through the exported ones.

**Recommendation.** Triage the advisory; upgrade to a fixed version (0.56.0) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-17541 — golang.org/x/net v0.55.0 is affected by GO-2026-6603 (CVE-2026-78659) (no severity rating)

- Severity: **Info** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:Go/golang.org/x/net@v0.55.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 10:32 UTC
- Priority score: 17.8 / 100
- CVSS v3.1: not applicable

OSV.dev reports GO-2026-6603 (CVE-2026-78659) for Go package golang.org/x/net at version v0.55.0: HTTP/2 server memory exhaustion due to Trailer headers in net/http. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. None of the affected functions (golang.org/x/net/http2.ClientConn.Close, golang.org/x/net/http2.ClientConn.Ping, golang.org/x/net/http2.ClientConn.RoundTrip, golang.org/x/net/http2.ClientConn.Shutdown, golang.org/x/net/http2.ConfigureServer, golang.org/x/net/http2.ConfigureTransport …) is named in the audited code: the advisory does not apply unless they are reached indirectly (traits, macros, other dependencies).

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-6603
```

**Evidence.**

_tool_output · [OSV.dev GO-2026-6603](https://osv.dev/vulnerability/GO-2026-6603) · line 11 · SHA-256 9e43850e0da48e9d00589cc2bffb372f39ec5e5a280f2f4b04520a91328fd703_

```
{"id": "GO-2026-6603", "aliases": ["BIT-golang-2026-78659", "CVE-2026-78659"], "modified": "2026-10-16T09:55:47.068117441Z", "summary": "HTTP/2 server memory exhaustion due to Trailer headers in net/http", "severity": null, "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed. A Go function counts only in a file that also names its package (a method: its type); unexported functions only through the exported ones.

**Recommendation.** Triage the advisory; upgrade to a fixed version (0.60.0) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-17542 — golang.org/x/net v0.55.0 is affected by GO-2026-6610 (CVE-2026-78660) (no severity rating)

- Severity: **Info** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:Go/golang.org/x/net@v0.55.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 10:32 UTC
- Priority score: 17.8 / 100
- CVSS v3.1: not applicable

OSV.dev reports GO-2026-6610 (CVE-2026-78660) for Go package golang.org/x/net at version v0.55.0: HTTP/2 transport accepts malformed framing-related headers in net/http. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. None of the affected functions (golang.org/x/net/http2.Transport.NewClientConn, golang.org/x/net/http2.Transport.RoundTrip, golang.org/x/net/http2.Transport.RoundTripOpt, golang.org/x/net/http2.clientConnPool.GetClientConn, golang.org/x/net/http2.clientConnReadLoop.handleResponse, golang.org/x/net/http2.noDialClientConnPool.GetClientConn …) is named in the audited code: the advisory does not apply unless they are reached indirectly (traits, macros, other dependencies).

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-6610
```

**Evidence.**

_tool_output · [OSV.dev GO-2026-6610](https://osv.dev/vulnerability/GO-2026-6610) · line 11 · SHA-256 1b823e53f27093797b8a7909032006e1f0f818f04118ad593a4641236392faa9_

```
{"id": "GO-2026-6610", "aliases": ["BIT-golang-2026-78660", "CVE-2026-78660"], "modified": "2026-10-16T09:56:04.364467528Z", "summary": "HTTP/2 transport accepts malformed framing-related headers in net/http", "severity": null, "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed. A Go function counts only in a file that also names its package (a method: its type); unexported functions only through the exported ones.

**Recommendation.** Triage the advisory; upgrade to a fixed version (0.60.0) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-17543 — golang.org/x/net v0.55.0 is affected by GO-2026-6611 (CVE-2026-78669) (no severity rating)

- Severity: **Info** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:Go/golang.org/x/net@v0.55.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 10:32 UTC
- Priority score: 17.8 / 100
- CVSS v3.1: not applicable

OSV.dev reports GO-2026-6611 (CVE-2026-78669) for Go package golang.org/x/net at version v0.55.0: Excessive CPU consumption from repeated initial window changes in net/http. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. None of the affected functions (golang.org/x/net/http2.ClientConn.Close, golang.org/x/net/http2.ClientConn.Ping, golang.org/x/net/http2.ClientConn.RoundTrip, golang.org/x/net/http2.ClientConn.Shutdown, golang.org/x/net/http2.ClientConn.addStreamLocked, golang.org/x/net/http2.ConfigureServer …) is named in the audited code: the advisory does not apply unless they are reached indirectly (traits, macros, other dependencies).

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-6611
```

**Evidence.**

_tool_output · [OSV.dev GO-2026-6611](https://osv.dev/vulnerability/GO-2026-6611) · line 11 · SHA-256 c9b9f78637131224c5d4073e44c47b7cce490fc5526e3d6b0697b43bc85cab2f_

```
{"id": "GO-2026-6611", "aliases": ["BIT-golang-2026-78669", "CVE-2026-78669"], "modified": "2026-10-16T09:55:38.952277866Z", "summary": "Excessive CPU consumption from repeated initial window changes in net/http", "severity": null, "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed. A Go function counts only in a file that also names its package (a method: its type); unexported functions only through the exported ones.

**Recommendation.** Triage the advisory; upgrade to a fixed version (0.60.0) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-17544 — golang.org/x/net v0.55.0 is affected by GO-2026-6612 (CVE-2026-78663) (no severity rating)

- Severity: **Info** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:Go/golang.org/x/net@v0.55.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 10:32 UTC
- Priority score: 17.8 / 100
- CVSS v3.1: not applicable

OSV.dev reports GO-2026-6612 (CVE-2026-78663) for Go package golang.org/x/net at version v0.55.0: Double flow control refund on HTTP/2 server streams in net/http. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. None of the affected functions (golang.org/x/net/http2.ClientConn.Close, golang.org/x/net/http2.ClientConn.Ping, golang.org/x/net/http2.ClientConn.RoundTrip, golang.org/x/net/http2.ClientConn.Shutdown, golang.org/x/net/http2.ConfigureServer, golang.org/x/net/http2.ConfigureTransport …) is named in the audited code: the advisory does not apply unless they are reached indirectly (traits, macros, other dependencies).

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-6612
```

**Evidence.**

_tool_output · [OSV.dev GO-2026-6612](https://osv.dev/vulnerability/GO-2026-6612) · line 11 · SHA-256 1471910f88c9bbf8395a304fd82510f61567373756002de8bcdc3fbe305890cb_

```
{"id": "GO-2026-6612", "aliases": ["BIT-golang-2026-78663", "CVE-2026-78663"], "modified": "2026-10-16T09:55:54.129082194Z", "summary": "Double flow control refund on HTTP/2 server streams in net/http", "severity": null, "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed. A Go function counts only in a file that also names its package (a method: its type); unexported functions only through the exported ones.

**Recommendation.** Triage the advisory; upgrade to a fixed version (0.60.0) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-17545 — golang.org/x/net v0.55.0 is affected by GO-2026-6617 (CVE-2026-97032) (no severity rating)

- Severity: **Info** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:Go/golang.org/x/net@v0.55.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 10:32 UTC
- Priority score: 17.8 / 100
- CVSS v3.1: not applicable

OSV.dev reports GO-2026-6617 (CVE-2026-97032) for Go package golang.org/x/net at version v0.55.0: HTTP/2 server crash due to HPACK encoder race in net/http. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. None of the affected functions (golang.org/x/net/http2.ClientConn.Close, golang.org/x/net/http2.ClientConn.Ping, golang.org/x/net/http2.ClientConn.RoundTrip, golang.org/x/net/http2.ClientConn.Shutdown, golang.org/x/net/http2.ConfigureServer, golang.org/x/net/http2.ConfigureTransport …) is named in the audited code: the advisory does not apply unless they are reached indirectly (traits, macros, other dependencies).

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-6617
```

**Evidence.**

_tool_output · [OSV.dev GO-2026-6617](https://osv.dev/vulnerability/GO-2026-6617) · line 11 · SHA-256 b948c88d959bc78948c7e3b7a746ac4da179933798e9735d02870080906cfc96_

```
{"id": "GO-2026-6617", "aliases": ["BIT-golang-2026-97032", "CVE-2026-97032"], "modified": "2026-10-16T09:55:57.350751224Z", "summary": "HTTP/2 server crash due to HPACK encoder race in net/http", "severity": null, "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed. A Go function counts only in a file that also names its package (a method: its type); unexported functions only through the exported ones.

**Recommendation.** Triage the advisory; upgrade to a fixed version (0.60.0) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-17546 — golang.org/x/net v0.55.0 is affected by GO-2026-6860 (CVE-2026-78661) (no severity rating)

- Severity: **Info** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:Go/golang.org/x/net@v0.55.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 10:32 UTC
- Priority score: 17.8 / 100
- CVSS v3.1: not applicable

OSV.dev reports GO-2026-6860 (CVE-2026-78661) for Go package golang.org/x/net at version v0.55.0: Avoid quadratic complexity when coalescing text nodes in html in golang.org/x/net. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. None of the affected functions (golang.org/x/net/html.Parse, golang.org/x/net/html.ParseFragment, golang.org/x/net/html.ParseFragmentWithOptions, golang.org/x/net/html.ParseWithOptions, golang.org/x/net/html.parser.addText, golang.org/x/net/html.parser.fosterParent …) is named in the audited code: the advisory does not apply unless they are reached indirectly (traits, macros, other dependencies).

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-6860
```

**Evidence.**

_tool_output · [OSV.dev GO-2026-6860](https://osv.dev/vulnerability/GO-2026-6860) · line 11 · SHA-256 1f106c45371219bac0158f7ce44e57c439f50f0c32898616d1563f14cadb1b28_

```
{"id": "GO-2026-6860", "aliases": ["CVE-2026-78661"], "modified": "2026-10-27T21:30:04.890809062Z", "summary": "Avoid quadratic complexity when coalescing text nodes in html in golang.org/x/net", "severity": null, "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed. A Go function counts only in a file that also names its package (a method: its type); unexported functions only through the exported ones.

**Recommendation.** Triage the advisory; upgrade to a fixed version (0.62.0) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-17547 — golang.org/x/net v0.55.0 is affected by GO-2026-6866 (CVE-2026-97045) (no severity rating)

- Severity: **Info** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:Go/golang.org/x/net@v0.55.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 10:32 UTC
- Priority score: 17.8 / 100
- CVSS v3.1: not applicable

OSV.dev reports GO-2026-6866 (CVE-2026-97045) for Go package golang.org/x/net at version v0.55.0: Check all ancestor namespace transitions when rendering raw text in html in golang.org/x/net. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. None of the affected functions (golang.org/x/net/html.Render, golang.org/x/net/html.childTextNodesAreLiteral) is named in the audited code: the advisory does not apply unless they are reached indirectly (traits, macros, other dependencies).

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-6866
```

**Evidence.**

_tool_output · [OSV.dev GO-2026-6866](https://osv.dev/vulnerability/GO-2026-6866) · line 11 · SHA-256 102267a016bc5eef7979a90b1ddd2288ff36b09ab6fa040c808e62f3b55c1f42_

```
{"id": "GO-2026-6866", "aliases": ["CVE-2026-97045"], "modified": "2026-10-27T21:45:08.978077289Z", "summary": "Check all ancestor namespace transitions when rendering raw text in html in golang.org/x/net", "severity": null, "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed. A Go function counts only in a file that also names its package (a method: its type); unexported functions only through the exported ones.

**Recommendation.** Triage the advisory; upgrade to a fixed version (0.62.0) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-17548 — golang.org/x/text v0.37.0 is affected by GO-2026-5970 (CVE-2026-56852) (no severity rating)

- Severity: **Info** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:Go/golang.org/x/text@v0.37.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 10:32 UTC
- Priority score: 17.8 / 100
- CVSS v3.1: not applicable

OSV.dev reports GO-2026-5970 (CVE-2026-56852) for Go package golang.org/x/text at version v0.37.0: Infinite loop on invalid input in golang.org/x/text. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. None of the affected functions (golang.org/x/text/unicode/norm.Form.Append, golang.org/x/text/unicode/norm.Form.AppendString, golang.org/x/text/unicode/norm.Form.Bytes, golang.org/x/text/unicode/norm.Form.FirstBoundary, golang.org/x/text/unicode/norm.Form.FirstBoundaryInString, golang.org/x/text/unicode/norm.Form.IsNormal …) is named in the audited code: the advisory does not apply unless they are reached indirectly (traits, macros, other dependencies).

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-5970
```

**Evidence.**

_tool_output · [OSV.dev GO-2026-5970](https://osv.dev/vulnerability/GO-2026-5970) · line 13 · SHA-256 bfbbe7709d9436223cf9210fce06d97700712894b3820800a0147dd4a0db8c5d_

```
{"id": "GO-2026-5970", "aliases": ["CVE-2026-56852"], "modified": "2026-09-23T10:41:39.386264978Z", "summary": "Infinite loop on invalid input in golang.org/x/text", "severity": null, "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed. A Go function counts only in a file that also names its package (a method: its type); unexported functions only through the exported ones.

**Recommendation.** Triage the advisory; upgrade to a fixed version (0.39.0) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-17549 — golang.org/x/text v0.37.0 is affected by GO-2026-6629 (CVE-2026-56851) (no severity rating)

- Severity: **Info** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:Go/golang.org/x/text@v0.37.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 10:32 UTC
- Priority score: 17.8 / 100
- CVSS v3.1: not applicable

OSV.dev reports GO-2026-6629 (CVE-2026-56851) for Go package golang.org/x/text at version v0.37.0: Panic parsing crafted input in x/text/secure/precis in golang.org/x/text. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. None of the affected functions (golang.org/x/text/secure/precis.Profile.Append, golang.org/x/text/secure/precis.Profile.AppendCompareKey, golang.org/x/text/secure/precis.Profile.Bytes, golang.org/x/text/secure/precis.Profile.Compare, golang.org/x/text/secure/precis.Profile.CompareKey, golang.org/x/text/secure/precis.Profile.NewTransformer …) is named in the audited code: the advisory does not apply unless they are reached indirectly (traits, macros, other dependencies).

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-6629
```

**Evidence.**

_tool_output · [OSV.dev GO-2026-6629](https://osv.dev/vulnerability/GO-2026-6629) · line 13 · SHA-256 657419214ae5882e9b4ead4f61526561fcf5d98c9624b1701de82958bdc592d2_

```
{"id": "GO-2026-6629", "aliases": ["CVE-2026-56851"], "modified": "2026-10-20T10:42:24.514593111Z", "summary": "Panic parsing crafted input in x/text/secure/precis in golang.org/x/text", "severity": null, "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed. A Go function counts only in a file that also names its package (a method: its type); unexported functions only through the exported ones.

**Recommendation.** Triage the advisory; upgrade to a fixed version (0.41.0) if it applies.

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

### Post-quantum maturity: Level 4 of 4 — post-quantum by default in the critical paths

- Hybrid — channel key exchange (TLS, Noise, handshakes): common/fabhttp/tls.go (classical group + X25519MLKEM768)
- Hybrid — channel key exchange (TLS, Noise, handshakes): gossip/util/grpc.go (classical group + X25519MLKEM768)
- Hybrid — channel key exchange (TLS, Noise, handshakes): integration/nwo/network.go (classical group + X25519MLKEM768)
- Hybrid — channel key exchange (TLS, Noise, handshakes): integration/nwo/operational_client.go (classical group + X25519MLKEM768)
- Hybrid — channel key exchange (TLS, Noise, handshakes): internal/osnadmin/httpclient.go (classical group + X25519MLKEM768)
- In use: X25519MLKEM768 — common/fabhttp/tls.go
- In use: X25519MLKEM768 — gossip/util/grpc.go
- In use: X25519MLKEM768 — integration/nwo/network.go
- In use: X25519MLKEM768 — integration/nwo/operational_client.go
- In use: X25519MLKEM768 — internal/osnadmin/httpclient.go

**Next step:** Keep the inventory current and review new code paths before release.

_Levels: 0 none; 1 present, not wired; 2 in use outside the critical paths; 3 hybrid in a critical path; 4 post-quantum by default in the critical paths (root of trust, key wrapping, channel key exchange). Judged from code and manifests._

### What the quantum-vulnerable algorithms do

| Role | Algorithms (files) | ID | First step |
|---|---|---|---|
| **transaction and message signing** | ECDSA (1), Ed25519 (1) | QSI-2026-17522, QSI-2026-17523 | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains adopt them |
| **authentication and identity (certificates, tokens, device attestation)** | ECDSA (1) | QSI-2026-17528 | Keep credentials short-lived and plan ML-DSA certificates, tokens and keys as the ecosystem supports them |
| **role not determined** | ECDSA (8), ECDH (2), Ed25519 (2) | QSI-2026-17524, QSI-2026-17525, QSI-2026-17527 | Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it; introduce an abstraction layer for crypto-agility |

_Roles are judged from file paths, function names and the code around each match; review confirms them. Root-of-trust keys and wrapped keys come first: they are hard to replace or can be recorded today._
No readiness questionnaire was completed for this project.

### Quantum algorithms relevant to this inventory

| Quantum algorithm | Effect | Attack model | Inventoried algorithms (rows) | What it means for this audit |
|---|---|---|---|---|
| Shor's algorithm — elliptic-curve discrete logarithms | breaks | Q1 | ECDH (2), ECDSA (12), Ed25519 (3), X25519MLKEM768 (9) | Elliptic-curve keys are expected to fall before RSA keys of comparable classical strength. On blockchains, coins whose public key is already on chain (reused addresses, pay-to-public-key and Taproot outputs) are exposed first; plan the move to post-quantum signatures and avoid key reuse in the meantime. |
| Grover's algorithm — key search and preimages | weakens (larger keys restore the margin) | Q1 | AES-128 (1), MD5 (1), SHA-2 (15) | Not a break. 256-bit keys (AES-256, ChaCha20) keep a comfortable margin; AES-128 meets NIST category 1, while some authorities ask for 256-bit keys in quantum-resistant contexts (see the AES-128 entry). Prefer 256-bit keys for long-lived data; 256-bit hashes need no change for preimage resistance. |
| Brassard–Høyer–Tapp — collision search | weakens (larger keys restore the margin) | Q1 | MD5 (1), SHA-2 (15) | 256-bit hashes (SHA-256, SHA3-256) remain adequate for collision resistance; 160-bit hashes are already weak classically (SHA-1 collisions are practical). Use 384/512-bit hashes where NIST categories 4–5 are required. |
| Quantum lattice sieving | included in standard parameters | Q1 | X25519MLKEM768 (9) | No change for ML-KEM or ML-DSA at the standard parameter sets. A 2024 claim of a polynomial-time quantum LWE algorithm was withdrawn after a bug was found (see claims). |

_Effects: breaks — replace the algorithm; weakens — larger keys or outputs restore the margin; included in standard parameters — no action at standard parameter sets; only with superposition queries — not applicable to ordinary deployments._


## 9. Limitations and assumptions

- This report presents automated and documented analysis results for the stated scope. It is not a legal opinion, a certification or an attestation of compliance with any standard.
- z is a planning assumption chosen per risk profile, not a prediction. A cryptographically relevant quantum computer is not publicly known to exist today.
- certificates: docs/source/cc_service.md line 164: certificate could not be parsed (ValueError)
- certificates: docs/source/commands/peerchaincode.md line 161: certificate could not be parsed (ValueError)
- certificates: docs/source/discovery-cli.md line 137: certificate could not be parsed (ValueError)
- certificates: docs/source/discovery-cli.md line 146: certificate could not be parsed (ValueError)
- certificates: docs/source/discovery-cli.md line 155: certificate could not be parsed (ValueError)
- certificates: docs/source/discovery-cli.md line 164: certificate could not be parsed (ValueError)
- certificates: docs/source/discovery-cli.md line 403: certificate could not be parsed (ValueError)
- certificates: docs/source/discovery-cli.md line 411: certificate could not be parsed (ValueError)
- certificates: docs/source/discovery-cli.md line 417: certificate could not be parsed (ValueError)
- certificates: docs/source/discovery-cli.md line 447: certificate could not be parsed (ValueError)
- certificates: docs/source/discovery-cli.md line 452: certificate could not be parsed (ValueError)
- certificates: docs/source/discovery-cli.md line 457: certificate could not be parsed (ValueError)
- certificates: docs/source/discovery-cli.md line 462: certificate could not be parsed (ValueError)
- certificates: docs/wrappers/peer_chaincode_postscript.md line 20: certificate could not be parsed (ValueError)
- tls_key_exchange_groups: internal/pkg/gateway/endorse.go line 102: not in the algorithm registry, not assessed: append(groups

## 10. Remediation plan / Priorities for 30, 60 and 90 days

### 30 days

| Priority | ID | Action | Type | Closure criteria |
|---|---|---|---|---|
| P2 | QSI-2026-17550 | Upgrade google.golang.org/grpc to a fixed version (1.82.2, 1.83.2, 1.84.0-dev.0.20260825144003-d5a41119e0e3, 1.85.0-dev.0.20260825072537-93e31b48545e). | root-cause fix | Dependency scan no longer reports GHSA-2v4p-qf9q-27wj (CVE-2026-84445, GO-2026-6443). |
### 60 days

| Priority | ID | Action | Type | Closure criteria |
|---|---|---|---|---|
| P3 | QSI-2026-17526 | Review each MD5 call site in common/deliverclient/orderers/connection.go; replace security-relevant ones with SHA-256 or a password hash. | root-cause fix | No security-relevant MD5 usage remains. |
| P3 | QSI-2026-17539 | Triage GO-2026-5932; upgrade golang.org/x/crypto to a fixed version (0.58.1-0.20261009181718-2f1f834330b2) if it applies. | root-cause fix | Dependency scan no longer reports GO-2026-5932, or the triage is recorded. |
| P3 | QSI-2026-17531 | Triage GO-2026-6603 (CVE-2026-78659); upgrade golang.org/x/net to a fixed version (0.60.0) if it applies. | root-cause fix | Dependency scan no longer reports GO-2026-6603 (CVE-2026-78659), or the triage is recorded. |
| P3 | QSI-2026-17532 | Triage GO-2026-6610 (CVE-2026-78660); upgrade golang.org/x/net to a fixed version (0.60.0) if it applies. | root-cause fix | Dependency scan no longer reports GO-2026-6610 (CVE-2026-78660), or the triage is recorded. |
| P3 | QSI-2026-17533 | Triage GO-2026-6611 (CVE-2026-78669); upgrade golang.org/x/net to a fixed version (0.60.0) if it applies. | root-cause fix | Dependency scan no longer reports GO-2026-6611 (CVE-2026-78669), or the triage is recorded. |
| P3 | QSI-2026-17534 | Triage GO-2026-6612 (CVE-2026-78663); upgrade golang.org/x/net to a fixed version (0.60.0) if it applies. | root-cause fix | Dependency scan no longer reports GO-2026-6612 (CVE-2026-78663), or the triage is recorded. |
| P3 | QSI-2026-17535 | Triage GO-2026-6617 (CVE-2026-97032); upgrade golang.org/x/net to a fixed version (0.60.0) if it applies. | root-cause fix | Dependency scan no longer reports GO-2026-6617 (CVE-2026-97032), or the triage is recorded. |
| P3 | QSI-2026-17536 | Triage GO-2026-6860 (CVE-2026-78661); upgrade golang.org/x/net to a fixed version (0.62.0) if it applies. | root-cause fix | Dependency scan no longer reports GO-2026-6860 (CVE-2026-78661), or the triage is recorded. |
| P3 | QSI-2026-17537 | Triage GO-2026-6866 (CVE-2026-97045); upgrade golang.org/x/net to a fixed version (0.62.0) if it applies. | root-cause fix | Dependency scan no longer reports GO-2026-6866 (CVE-2026-97045), or the triage is recorded. |
| P3 | QSI-2026-17538 | Triage GO-2026-6629 (CVE-2026-56851); upgrade golang.org/x/text to a fixed version (0.41.0) if it applies. | root-cause fix | Dependency scan no longer reports GO-2026-6629 (CVE-2026-56851), or the triage is recorded. |
| P3 | QSI-2026-17540 | Triage GO-2026-5942 (CVE-2026-46600); upgrade golang.org/x/net to a fixed version (0.56.0) if it applies. | root-cause fix | Dependency scan no longer reports GO-2026-5942 (CVE-2026-46600), or the triage is recorded. |
| P3 | QSI-2026-17541 | Triage GO-2026-6603 (CVE-2026-78659); upgrade golang.org/x/net to a fixed version (0.60.0) if it applies. | root-cause fix | Dependency scan no longer reports GO-2026-6603 (CVE-2026-78659), or the triage is recorded. |
| P3 | QSI-2026-17542 | Triage GO-2026-6610 (CVE-2026-78660); upgrade golang.org/x/net to a fixed version (0.60.0) if it applies. | root-cause fix | Dependency scan no longer reports GO-2026-6610 (CVE-2026-78660), or the triage is recorded. |
| P3 | QSI-2026-17543 | Triage GO-2026-6611 (CVE-2026-78669); upgrade golang.org/x/net to a fixed version (0.60.0) if it applies. | root-cause fix | Dependency scan no longer reports GO-2026-6611 (CVE-2026-78669), or the triage is recorded. |
| P3 | QSI-2026-17544 | Triage GO-2026-6612 (CVE-2026-78663); upgrade golang.org/x/net to a fixed version (0.60.0) if it applies. | root-cause fix | Dependency scan no longer reports GO-2026-6612 (CVE-2026-78663), or the triage is recorded. |
| P3 | QSI-2026-17545 | Triage GO-2026-6617 (CVE-2026-97032); upgrade golang.org/x/net to a fixed version (0.60.0) if it applies. | root-cause fix | Dependency scan no longer reports GO-2026-6617 (CVE-2026-97032), or the triage is recorded. |
| P3 | QSI-2026-17546 | Triage GO-2026-6860 (CVE-2026-78661); upgrade golang.org/x/net to a fixed version (0.62.0) if it applies. | root-cause fix | Dependency scan no longer reports GO-2026-6860 (CVE-2026-78661), or the triage is recorded. |
| P3 | QSI-2026-17547 | Triage GO-2026-6866 (CVE-2026-97045); upgrade golang.org/x/net to a fixed version (0.62.0) if it applies. | root-cause fix | Dependency scan no longer reports GO-2026-6866 (CVE-2026-97045), or the triage is recorded. |
| P3 | QSI-2026-17548 | Triage GO-2026-5970 (CVE-2026-56852); upgrade golang.org/x/text to a fixed version (0.39.0) if it applies. | root-cause fix | Dependency scan no longer reports GO-2026-5970 (CVE-2026-56852), or the triage is recorded. |
| P3 | QSI-2026-17549 | Triage GO-2026-6629 (CVE-2026-56851); upgrade golang.org/x/text to a fixed version (0.41.0) if it applies. | root-cause fix | Dependency scan no longer reports GO-2026-6629 (CVE-2026-56851), or the triage is recorded. |
### 90 days

| Priority | ID | Action | Type | Closure criteria |
|---|---|---|---|---|
| P3 | QSI-2026-17522 | Add ECDSA usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-17523 | Add Ed25519 usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-17524 | Add ECDSA usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-17525 | Add ECDH usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-17527 | Add Ed25519 usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-17528 | Add ECDSA usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-17529 | Add ECDSA usages at certificate:ca.org1.example.com to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-17530 | Add ECDSA usages at certificate:Org2-child1 to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P4 | QSI-2026-17522 | Plan migration of ECDSA to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-17523 | Plan migration of Ed25519 to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-17524 | Plan migration of ECDSA to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-17525 | Plan migration of ECDH to Hybrid key establishment with ML-KEM (FIPS 203), e.g. X25519MLKEM768 in TLS 1.3 or mlkem768x25519-sha256 in SSH (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows Hybrid key establishment with ML-KEM (FIPS 203), e.g. X25519MLKEM768 in TLS 1.3 or mlkem768x25519-sha256 in SSH or a hybrid scheme in use. |
| P4 | QSI-2026-17527 | Plan migration of Ed25519 to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-17528 | Plan migration of ECDSA to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-17529 | Plan migration of ECDSA to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. or a hybrid scheme in use. |
| P4 | QSI-2026-17530 | Plan migration of ECDSA to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. or a hybrid scheme in use. |

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
5. C. Zalka — Grover's quantum searching algorithm is optimal (Phys. Rev. A 60, 2746, 1999; arXiv:quant-ph/9711070) — APS. <https://doi.org/10.1103/PhysRevA.60.2746> (peer-reviewed article: optimal for any success probability; parallel search gains no more than splitting the space)
6. CRYSTALS-Kyber — Algorithm Specifications and Supporting Documentation (round 3, 2021-08-04) — CRYSTALS team. <https://pq-crystals.org/kyber/data/kyber-specification-round3-20210804.pdf> (NIST round-3 submission: core-SVP cost 2^{0.292β} classical, 2^{0.265β} quantum; Kyber768 166 quantum bits)
7. Common Vulnerability Scoring System v3.1: Specification Document — FIRST. <https://www.first.org/cvss/v3.1/specification-document> (final)
8. D. J. Bernstein — Cost analysis of hash collisions: Will quantum computers make SHARCS obsolete? (2009) — cr.yp.to. <https://cr.yp.to/hash/collisioncost-20090823.pdf> (paper dated 2009-08-23)
9. D. Litinski — How to compute a 256-bit elliptic curve private key with only 50 million Toffoli gates (arXiv:2306.08585) — arXiv. <https://arxiv.org/abs/2306.08585> (preprint (2023-06-14): 6000 modules × 1152 physical qubits, one key per 10 minutes under its architecture assumptions)
10. FIPS 203 — Module-Lattice-Based Key-Encapsulation Mechanism Standard (ML-KEM) — NIST. <https://csrc.nist.gov/pubs/fips/203/final> (final (August 2024))
11. FIPS 204 — Module-Lattice-Based Digital Signature Standard (ML-DSA) — NIST. <https://csrc.nist.gov/pubs/fips/204/final> (final (August 2024))
12. FIPS 205 — Stateless Hash-Based Digital Signature Standard (SLH-DSA) — NIST. <https://csrc.nist.gov/pubs/fips/205/final> (final (August 2024))
13. G. Brassard, P. Høyer, A. Tapp — Quantum Algorithm for the Collision Problem (LATIN '98; arXiv:quant-ph/9705002) — Springer / arXiv. <https://arxiv.org/abs/quant-ph/9705002> (peer-reviewed article: collisions of r-to-one functions in O((N/r)^{1/3}) expected evaluations)
14. J. Proos, C. Zalka — Shor's discrete logarithm quantum algorithm for elliptic curves (Quantum Inf. Comput. 3(4), 2003; arXiv:quant-ph/0301141) — Quantum Information & Computation. <https://doi.org/10.26421/QIC3.4-3> (peer-reviewed article)
15. L. K. Grover — A fast quantum mechanical algorithm for database search (STOC 1996) — ACM. <https://doi.org/10.1145/237814.237866> (peer-reviewed article)
16. M. Amy et al. — Estimating the cost of generic quantum pre-image attacks on SHA-2 and SHA-3 (SAC 2016; arXiv:1603.09383) — Springer / arXiv. <https://arxiv.org/abs/1603.09383> (peer-reviewed article: SHA-256 about 2^153.8 surface-code cycles on 2^12.6 logical qubits; SHA3-256 about 2^146.5 cycles on 2^20)
17. M. Cain et al. — Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits (arXiv:2603.28627) — arXiv. <https://arxiv.org/abs/2603.28627> (preprint (2026-03-30): P-256 in a few days with 26,000 physical neutral-atom qubits; RSA-2048 one to two orders of magnitude longer)
18. M. Mosca — Cybersecurity in an Era with Quantum Computers: Will We Be Ready? (IEEE Security & Privacy, 2018) — IEEE. <https://doi.org/10.1109/MSP.2018.3761723> (peer-reviewed article; source of the x + y > z migration inequality)
19. M. Roetteler, M. Naehrig, K. Svore, K. Lauter — Quantum resource estimates for computing elliptic curve discrete logarithms (ASIACRYPT 2017) — IACR / arXiv. <https://arxiv.org/abs/1706.06752> (peer-reviewed article: at most 9n + 2⌈log2 n⌉ + 10 qubits and 448 n^3 log2 n + 4090 n^3 Toffoli gates)
20. NIST IR 8547 — Transition to Post-Quantum Cryptography Standards — NIST. <https://csrc.nist.gov/pubs/ir/8547/final> (final (2026-10-27; the initial public draft of November 2024 is obsoleted). Tables 2 and 4: ECDSA, EdDSA and RSA signatures, finite-field and elliptic-curve DH and MQV, and RSA key establishment are deprecated after 2030 and disallowed after 2035 at every key size — the draft deprecated only the 112-bit level. A composite (hybrid) key establishment stays FIPS 140-validatable while one input comes from an approved scheme. Repeats the federal deadlines of OMB M-26-15: post-quantum key establishment by 2030-12-31 and signatures by 2031-12-31 for high value assets and high impact systems)
21. NIST SP 800-131A Rev. 2 — Transitioning the Use of Cryptographic Algorithms and Key Lengths — NIST. <https://csrc.nist.gov/pubs/sp/800/131/a/r2/final> (final (2019))
22. NIST — Post-Quantum Cryptography Standardization: Evaluation Criteria, Security (Call for Proposals, Section 4.A.5) — NIST. <https://csrc.nist.gov/Projects/Post-Quantum-Cryptography/Post-Quantum-Cryptography-Standardization/Evaluation-Criteria/Security-(Evaluation-Criteria)> (security categories: AES-128 key search 2^170/MAXDEPTH quantum gates, AES-192 2^233/MAXDEPTH, AES-256 2^298/MAXDEPTH; MAXDEPTH 2^40–2^96)
23. OSV advisory GHSA-2v4p-qf9q-27wj — OSV.dev. <https://osv.dev/vulnerability/GHSA-2v4p-qf9q-27wj> (modified 2026-09-25T18:00:05.270054427Z)
24. OSV advisory GO-2026-5932 — OSV.dev. <https://osv.dev/vulnerability/GO-2026-5932> (modified 2026-11-02T22:15:06.677088389Z)
25. OSV advisory GO-2026-5942 — OSV.dev. <https://osv.dev/vulnerability/GO-2026-5942> (modified 2026-08-17T12:25:32.471119200Z)
26. OSV advisory GO-2026-5970 — OSV.dev. <https://osv.dev/vulnerability/GO-2026-5970> (modified 2026-09-23T10:41:39.386264978Z)
27. OSV advisory GO-2026-6603 — OSV.dev. <https://osv.dev/vulnerability/GO-2026-6603> (modified 2026-10-16T09:55:47.068117441Z)
28. OSV advisory GO-2026-6610 — OSV.dev. <https://osv.dev/vulnerability/GO-2026-6610> (modified 2026-10-16T09:56:04.364467528Z)
29. OSV advisory GO-2026-6611 — OSV.dev. <https://osv.dev/vulnerability/GO-2026-6611> (modified 2026-10-16T09:55:38.952277866Z)
30. OSV advisory GO-2026-6612 — OSV.dev. <https://osv.dev/vulnerability/GO-2026-6612> (modified 2026-10-16T09:55:54.129082194Z)
31. OSV advisory GO-2026-6617 — OSV.dev. <https://osv.dev/vulnerability/GO-2026-6617> (modified 2026-10-16T09:55:57.350751224Z)
32. OSV advisory GO-2026-6629 — OSV.dev. <https://osv.dev/vulnerability/GO-2026-6629> (modified 2026-10-20T10:42:24.514593111Z)
33. OSV advisory GO-2026-6860 — OSV.dev. <https://osv.dev/vulnerability/GO-2026-6860> (modified 2026-10-27T21:30:04.890809062Z)
34. OSV advisory GO-2026-6866 — OSV.dev. <https://osv.dev/vulnerability/GO-2026-6866> (modified 2026-10-27T21:45:08.978077289Z)
35. P. W. Shor — Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms on a Quantum Computer (SIAM J. Comput., 1997) — SIAM. <https://doi.org/10.1137/S0097539795293172> (peer-reviewed article)
36. R. Babbush et al. — Securing Elliptic Curve Cryptocurrencies against Quantum Vulnerabilities: Resource Estimates and Mitigations (arXiv:2603.28846) — arXiv. <https://arxiv.org/abs/2603.28846> (preprint (2026-03-30, v2 2026-04-15): 256-bit ECDLP with < 1200 logical qubits and < 90 M Toffoli gates (or < 1450 and < 70 M); < 500,000 physical qubits at 10^-3 error, minutes)
37. S. Jaques, M. Naehrig, M. Roetteler, F. Virdia — Implementing Grover oracles for quantum key search on AES and LowMC (EUROCRYPT 2020; arXiv:1910.01700) — Springer / arXiv. <https://arxiv.org/abs/1910.01700> (peer-reviewed article: lower cost estimates for the AES key searches that define the NIST categories)

## Appendices: Cryptographic inventory

By origin: dependency manifests 2 (0 Shor-breakable) · keys and certificates 4 (2 Shor-breakable) · own code 39 (15 Shor-breakable).

| Algorithm | Parameter | Library | Quantum status | Classical status | Count | Locations | Examples |
|---|---|---|---|---|---|---|---|
| MD5 |  |  | weak classically | broken | 1 | 1 | common/deliverclient/orderers/connection.go:11 |
| AES-128 | AES-128 |  | Grover: acceptable to NIST, below ECCG/ANSSI guidance | acceptable | 1 | 1 | internal/pkg/comm/config.go:48 |
| SHA-2 | SHA-256 |  | Grover: acceptable to NIST, below ECCG/ANSSI guidance | acceptable | 15 | 15 | common/crypto/tlsgen/key.go:14; common/deliverclient/orderers/connection.go:12; common/ledger/blkstorage/blkstoragetest/blkstoragetest.go:10 |
| X25519MLKEM768 | X25519MLKEM768 |  | hybrid | acceptable | 9 | 9 | common/fabhttp/tls.go:43; gossip/util/grpc.go:58; integration/nwo/network.go:1448 |
| Crypto library | v0.58.0 | golang.org/x/crypto (Go x/crypto) | n/a | acceptable | 2 | 2 | go.mod:108; tools/go.mod:265 |
| ECDH |  |  | vulnerable (Shor) | acceptable | 2 | 2 | common/crypto/tlsgen/key.go:125; internal/cryptogen/ca/ca.go:176 |
| ECDSA |  |  | vulnerable (Shor) | acceptable | 10 | 10 | cmd/common/signer/signer.go:11; common/crypto/sanitize.go:10; common/crypto/tlsgen/key.go:11 |
| ECDSA | secp256r1 |  | vulnerable (Shor) | acceptable | 2 | 2 | sampleconfig/msp/cacerts/cacert.pem (line 1) — ca.org1.example.com; sampleconfig/msp/tlsintermediatecerts/tlsintermediate.pem (line 1) — Org2-child1 |
| Ed25519 | Ed25519 |  | vulnerable (Shor) | acceptable | 3 | 3 | cmd/common/signer/signer.go:103; integration/nwo/signingid.go:72; internal/cryptogen/csp/csp.go:87 |

_Long lists are grouped here; the full per-file list is in the JSON report, signed with the same key._

## Appendices: Input files

| File | Size | SHA-256 | Redactions |
|---|---|---|---|
| ccaas_builder/cmd/detect/main.go | 1353 | `1de145460a329829fb9f33e478316c932e1eb525d009a98db022df609f3b9260` | 0 |
| ccaas_builder/cmd/release/main.go | 2425 | `fd425bcc404d2cc8b8ad6441770fe066b2b59801afc7113fc85cbddff689362d` | 0 |
| ccaas_builder/go.mod | 465 | `310154c5e1171385c3a55b5b5d7902bfd1d7b7e3d42535c66b7ae0a8d8dc4390` | 0 |
| cmd/common/cli.go | 4278 | `b5b2f9fa09ae26277dfbb031b589e6dec9a6e9c03782b18e9d18fa7bd5d2cbe4` | 0 |
| cmd/common/comm/client.go | 1430 | `711cea577e723ee2b882aad08994f8e7d2597ff8151b5ca2b5f957a5dd79471a` | 0 |
| cmd/common/comm/config.go | 1899 | `a6fc53149a0d561e18f3a44472d7a27a330cb25fb3ac36d2b70ba2366bff8862` | 0 |
| cmd/common/config.go | 1631 | `f41930763208789dfce98e3f76cf9a35c0947e40f7d09cf29fdae23aad3768d5` | 0 |
| cmd/common/signer/signer.go | 4153 | `17c163a929b559ef19ed6777353cde8185eeb4bbf57e2878243cf70797a3b0c7` | 0 |
| cmd/configtxgen/main.go | 10341 | `81c85827fa80d23ab24dff97e171d10d3ed9ef2ba76ab545209645ada95ae666` | 0 |
| cmd/configtxlator/main.go | 8054 | `93dc99f261d899e7235eef7caf03f33d5f02bcc99a24d0a8f9ee618664ea12b7` | 0 |
| cmd/cryptogen/main.go | 23821 | `495c97532e1d28ea952ceaeb28e6885f44ec18829650b03aec28d56a095ec1db` | 0 |
| cmd/discover/main.go | 453 | `954de3e6d727534a30551a162dda5c1bb70ab1caf3c1cb74aa88c83483fa4483` | 0 |
| cmd/ledgerutil/main.go | 5261 | `37df5700c28b544fb4c59cd22c1bcef6a7a71910b8106cc9e8edfa6faf12b68a` | 0 |
| cmd/orderer/main.go | 362 | `89a420adb5d8c92208b5a049a91ca81b6810b1471a3a9da1e94fcd51afcb5463` | 0 |
| cmd/osnadmin/main.go | 8601 | `d0b74588d211ea374ed5756b213a465d071788f43d2fa9c6f32c4a142d35a72b` | 0 |
| cmd/peer/main.go | 1776 | `bcda24441b76551a5e39f926cc9e2c759f70c2a7554dfcda35d495254fc63864` | 0 |
| common/capabilities/application.go | 6587 | `779e2d2934daaa6e7bbc5352820c4de13876b61307323c14aa19cb70d888248d` | 0 |
| common/capabilities/capabilities.go | 1437 | `182b55ca728e0f7ee25adac741040b4f3b11daa94ef34ae3063d99f4693d18a1` | 0 |
| common/capabilities/channel.go | 3286 | `9c4c99bfc86203a43179f8298754b32e732e4159ba5ec723b8151442c39fd709` | 0 |
| common/capabilities/orderer.go | 3076 | `702a713ae85c4ef8520f280367d675591aaf1254c99a6e799caf136b08fb8935` | 0 |
| common/cauthdsl/cauthdsl.go | 3158 | `8f19ca23e091850f81bc9e29c6bb975dd234292b40318b9809d678a689a7b56f` | 0 |
| common/cauthdsl/policy.go | 3320 | `0d029f0b1cb946dc3b3224c4acf82363ea244a69fe405e5765d71de25dccc8f3` | 0 |
| common/chaincode/metadata.go | 2783 | `ac817be5d283bb0e456a27658e896d2fb41cd43f3d334f591972f19173cc9a61` | 0 |
| common/channelconfig/acls.go | 1214 | `63821109ef0603038b037b24c9e606e894299d8ba18c8cd5321265e65557e859` | 0 |
| common/channelconfig/api.go | 9911 | `4ee6e2c374d1e463fb3da62dcbd9727df09a890de3454f56a7af6891ffa0ae3b` | 0 |
| common/channelconfig/application.go | 2264 | `0a4fee52144fe3054252f1e54d799019d674fbc3b2107031160fc272a59d4e62` | 0 |
| common/channelconfig/applicationorg.go | 1863 | `4e129a9cfbd1110230e33bf14fb50e492179f1ad3997201b936b78c4e9134746` | 0 |
| common/channelconfig/bundle.go | 8380 | `788fb8f48f767d6706323835e236907c73c485fd757caf29bf7b0b1ee3579cad` | 0 |
| common/channelconfig/bundlesource.go | 3626 | `93aaa7c9502c6c272ccbd1b6c8fb4442f9666599484893958a4e63de677bce02` | 0 |
| common/channelconfig/channel.go | 7439 | `4fa96d1e902129003f08c6a81cd5fdd4e7642c349d08615cdcf45172bd56c87b` | 0 |
| common/channelconfig/consortium.go | 1729 | `83f52aa89326c56cbfee7064ce29640137b73b399a542eb1f27c7db8971fa159` | 0 |
| common/channelconfig/consortiums.go | 1093 | `7577248c3ff63d112ac900b3d42d2c7b9ce80e8220f389c5418e39d64ff727b2` | 0 |
| common/channelconfig/logsanitychecks.go | 1734 | `be6ce565d48ce9d40e7598aef8267e7e65050d488a81605f91acd191ab14c494` | 0 |
| common/channelconfig/msp.go | 2625 | `bdc69830b988ec6daffe6db7c888a7bffb1c81eb4b007fe5fd24fb17ce8e1869` | 0 |
| common/channelconfig/orderer.go | 8762 | `75c2dff486ce9b74133c1d9800dfe97d1faa6ec04acf47625da16281df1c11d2` | 0 |
| common/channelconfig/organization.go | 2306 | `c0bec01c4eeef51ea619925683d1d0f0cab953467eda1ce579c84ff9d4049b77` | 0 |
| common/channelconfig/standardvalues.go | 3365 | `f3f15b5cae014c2a97a0c82dc12b16d0a391279cabae870f7324d24017cf11f9` | 0 |
| common/channelconfig/util.go | 10822 | `0d74545c0393213bc7cbf22c3cb056184206608c381f99bc7339a27b628b6b89` | 0 |
| common/configtx/compare.go | 4035 | `5e8d0aa8b4075de7c165cf5afe812f2e3b3b5b65539d566d540cac3e66a54a26` | 0 |
| common/configtx/configmap.go | 6109 | `dfc57b9d0f9ae3ab80d4f29e5af21efa0043389bd5b4f4dff399a932361c0004` | 0 |
| common/configtx/configtx.go | 863 | `f58e267e9a1b07207bd7277b20ba40f0f8a754466dc5abb9ec0b147a655ab595` | 0 |
| common/configtx/update.go | 6408 | `b449f354a4ed0f92295631507baeb2b761346625ff2643727d523f783be40156` | 0 |
| common/configtx/util.go | 2955 | `0c8ffa2fa8d04c4e8257a2b9931cdbf8be11b19438c7e268a43ebe31d80fb604` | 0 |
| common/configtx/validator.go | 6426 | `79bb1530e608aa255cd6b68c2fb1a59c160519733cf72f864ca10f704099734d` | 0 |
| common/crypto/expiration.go | 4351 | `ff6300e21adcbc0002f22da5e01220d787c07f2a027282cc4b011bcd03cd3a5d` | 0 |
| common/crypto/random.go | 1107 | `9ff34ec4f14642fb3a76054012ea75ba5173b5768db1fe6a030f0e78c1ec43d2` | 0 |
| common/crypto/sanitize.go | 3407 | `07ebd62082c189a82e33775b5fbcaf46685a1a12d4677a5d8c92d246ee065fd1` | 0 |
| common/crypto/tlsgen/ca.go | 2673 | `1c8bf78ef0aa2bbfda5519dd00b65699f91814a07342406cc955a7035e514c77` | 0 |
| common/crypto/tlsgen/key.go | 3384 | `5087586f9dbed00e39741671106e43a9c7a86dfae42c33c1c0c3dbddf9c23715` | 0 |
| common/deliver/acl.go | 2345 | `73371523335cffa6c51a59ddc02605defa5f38be9c3959b2bf5bef7ec41ddb1a` | 0 |
| common/deliver/binding.go | 2262 | `eda98f4c8a4b87c69943ced61e4e0566f06326d04be50e0e30fba9d7ac0a86dc` | 0 |
| common/deliver/deliver.go | 14311 | `1f54e29f9fbe342fa0a970625979fa016cab31cc3925f9a2a56041209556a180` | 0 |
| common/deliver/metrics.go | 2016 | `091c1a5592bf7b72904cc57d65e2b653974a5c4e84295f15b530c98527c67a74` | 0 |
| common/deliverclient/block_verification.go | 13444 | `fef41fb18e7b5595f5960b79046e4e4542278932dd6a230f245a63cb69e4dbb3` | 0 |
| common/deliverclient/blocksprovider/adapters.go | 739 | `b095756ab89ba438f2670f03afeedb3a58c0b4392b6d4653e9ba99073b96fd4e` | 0 |
| common/deliverclient/blocksprovider/bft_censorship_monitor.go | 15574 | `4c62f49ff883f939c4006778d53eee4a5eccb302e91c31f1687255eae3d4c633` | 0 |
| common/deliverclient/blocksprovider/bft_censorship_monitor_factory.go | 844 | `9945702e1b34915f6a3bbf76791dfcd96e047f8949b7b7e0d5d371752305d0ef` | 0 |
| common/deliverclient/blocksprovider/bft_deliverer.go | 16398 | `86dadca0503eef2149add5a9aa6ea96a6aadb08ea236228b004c9752e9d88fb8` | 0 |
| common/deliverclient/blocksprovider/bft_header_receiver.go | 6489 | `9c03c1bc55b770f4fa84ba19a89039fd3addba62720a7007cd185bf59c7d2b41` | 0 |
| common/deliverclient/blocksprovider/block_receiver.go | 5577 | `3d851ba0ec903304915e38a132ef0a443f676522b0050f4fb0a596dcd619df7a` | 0 |
| common/deliverclient/blocksprovider/deliverer.go | 9312 | `6a32e662ea353f1f8473a1172e81dbf0ed9dc1238deae473bf52050956360efa` | 0 |
| common/deliverclient/blocksprovider/delivery_requester.go | 3957 | `ab08a80df91e444562803c22d9f7dcc82e7e8aad316e54cf3d481e2002218044` | 0 |
| common/deliverclient/blocksprovider/fake/ab_deliver_client.go | 15258 | `e01f8da2efb90fc774a08fda9977b01ac37dafc6682a4d61fb413b02bbd1c079` | 0 |
| common/deliverclient/blocksprovider/fake/block_handler.go | 3201 | `766bb03798c2eeef2ac994f2ddbeef9ac4e11d62cc916652512f4fa1277ebb0f` | 0 |
| common/deliverclient/blocksprovider/fake/block_progress_reporter.go | 3137 | `f18b3c6ffd67b52af469b9d4d664389733b541d9c4c00b48a0b698b25d1ad5b9` | 0 |
| common/deliverclient/blocksprovider/fake/censorship_detector.go | 4380 | `5e69124305751338a8c1afa6d73450a17f26837dece9c858612dd3811ed37228` | 0 |
| common/deliverclient/blocksprovider/fake/censorship_detector_factory.go | 4775 | `23e85738fda1103ede9472e2b1e03d0e6114a9c108d232e578645269b7638dc2` | 0 |
| common/deliverclient/blocksprovider/fake/deliver_client_requester.go | 6759 | `83021594654c74af9556ca64e0b6846ba12f540883afb1ad32c1c51a702abca2` | 0 |
| common/deliverclient/blocksprovider/fake/deliver_streamer.go | 3688 | `f2fc2eae9be0f5d7f5a6e04c85515124ee2ac51926248992877aae3f5069e56f` | 0 |
| common/deliverclient/blocksprovider/fake/dialer.go | 3200 | `0b049ccb1439bdeb67e2a0cedc191e95f2cd29dba4af52768026fdfa4beae1e3` | 0 |
| common/deliverclient/blocksprovider/fake/duration_exceeded_handler.go | 3269 | `e6f1a7ebf4b96200068af74e45ea854391584ac91d73750f57a12d73f31ecf8c` | 0 |
| common/deliverclient/blocksprovider/fake/gossip_service_adapter.go | 4351 | `d35c181cc8f0b9628a33df50cc16c4a3d6edab1b07db82f1096d250de714058f` | 0 |
| common/deliverclient/blocksprovider/fake/ledger_info.go | 5167 | `a1d4536cb47c4d43899bb8c074645eb192b1a6b8b165c5d0931693e386f5ef01` | 0 |
| common/deliverclient/blocksprovider/fake/orderer_connection_source.go | 6883 | `5235163f46eee06c441428bf74a2dcef24922d5049694c135f493004e451365d` | 0 |
| common/deliverclient/blocksprovider/fake/orderer_connection_source_factory.go | 4175 | `a77e2363789c5c17e18ec67f90e5fd0f509d25ff9f392aa55bd66318d86dc4e5` | 0 |
| common/deliverclient/blocksprovider/fake/signer.go | 4672 | `85eb9d339e32242cbc5db732c0bce5641d41918d8170785a62b940b114bfaebc` | 0 |
| common/deliverclient/blocksprovider/fake/sleeper.go | 1822 | `d382462c20e263f0c12cc4f406ea4142eef4be2a5d34a42f4e332f98a04dccab` | 0 |
| common/deliverclient/blocksprovider/fake/updatable_block_verifier.go | 11275 | `d6f6428cda0349110f9c594a7823a38c726101cc79a37359a5b6f8f0a69b28dc` | 0 |
| common/deliverclient/blocksprovider/stoppable_sleeper.go | 516 | `4874013f083053fe35fbc5acff8c0b3c62668dcdd07ed98b5d1cdc9fc3f0fc1e` | 0 |
| common/deliverclient/blocksprovider/timeout_config.go | 940 | `72156e712c3d818e47d4eab2904266eb8c74120328846abcae96a9e91b94da7e` | 0 |
| common/deliverclient/blocksprovider/util.go | 2568 | `a69bf7102a2b75448c688a27847e88cdebccbe69a7709d598f8301d2de425525` | 0 |
| common/deliverclient/orderers/connection.go | 7803 | `fa072f2d16bdf050f1439eb6d0ab5d3d1c1f7fa612506de267aa96071e165d27` | 0 |
| common/deliverclient/orderers/connection_factory.go | 935 | `790cdeedb6add540271f52c7c712530e83c60a068f5c27cd76692c799150f959` | 0 |
| common/deliverclient/util.go | 1698 | `b093d97e1c0c70933f30094a53df3327b2735c4d512ac4d90d9fcdf8e28b3380` | 0 |
| common/deliverclient/verifier_assembler.go | 1794 | `ae6313d393e0bec3192f834d1800695b883939c246e110014706436a7e713bec` | 0 |
| common/diag/goroutine.go | 631 | `2c2ff6908c8adcb45f621a8110a2741771ad7dab82cfac13e99c1848286e020a` | 0 |
| common/errors/errors.go | 1260 | `b803c02fc3250145290bcfa9aa74bda65b85e2b4f4067fe64fea0121d1d49407` | 0 |
| common/fabhttp/fakes/logger.go | 2919 | `9d15ac89fc5714e3368b7789ac8ce0a235b6852bf9811eed1e5c18467d7eadfa` | 0 |
| common/fabhttp/server.go | 2937 | `95a3569f8d0a046eca54ada2991f95fd85d13652bb7c6909eb5e3e527cdfc4e7` | 0 |
| common/fabhttp/tls.go | 1275 | `c5730d31da82f5a35d1364ab0de96f0c6d1fafe193bb79095ed6323baf9cb91e` | 0 |
| common/genesis/genesis.go | 1998 | `e3b530d2133a7355062464b98506ba72eba04cf24fb78507171e3bcc3e5ea51c` | 0 |
| common/graph/choose.go | 1743 | `51ed524478bfd6927b70545187b7d87df753c5814990f45924406b8d5d153e05` | 0 |
| common/graph/graph.go | 959 | `69dfe3a2a12faf080e5a4b659db4e8746ac55b689daede2c06c6446709719ff5` | 0 |
| common/graph/perm.go | 4178 | `874ea4293a59bcb42d38fd9c52db38ad2e43ddb55fbc95478a0a7564034ee0c1` | 0 |
| common/graph/tree.go | 4365 | `5de18bf5fea925b5032b45d35ae1a64751ef89d270799d131d7d2880d250302f` | 0 |
| common/grpclogging/context.go | 744 | `e0bdef8cf3fe63dcfedbfc54a8a894b974f0264763d54fd7ab7cc3e4331c0560` | 0 |
| common/grpclogging/fakes/echo_service.go | 5375 | `74b5aeac226186601eaff5a48ef574460577add517fc216468be468dc3c46771` | 0 |
| common/grpclogging/fakes/leveler.go | 2713 | `a3d4f6b97ed89d0c08b117b2daf5f15d685dd8c36794e238eda84dc76fa4e6f3` | 0 |
| common/grpclogging/fields.go | 1022 | `3075bc2d0124455976de2a97d6f6353f2592495a7cc1d0c9b5f4caad48e917f2` | 0 |
| common/grpclogging/server.go | 5304 | `f04ab5d688b79fc292e97e8cbd1db0021a74e3a101171286cf04af1848cdff17` | 0 |
| common/grpclogging/testpb/echo.pb.go | 5540 | `2b2085195c8580d62f4c1a35ba1925f2e9f12598aaf067ec3db2fc0da75618cd` | 0 |
| common/grpclogging/testpb/echo.proto | 393 | `9d4a54a8c1c5a2b41f72bdf14cfb59aefa9ed61e333eaa0b648cf72ac4a84482` | 0 |
| common/grpclogging/testpb/echo_grpc.pb.go | 5872 | `39d75304e585f5793d21dadcb0694a807306d0d1be1c765a63a637e756ba8e93` | 0 |
| common/grpcmetrics/fakes/echo_service.go | 5375 | `6c83ce077f558f954676a52607fcb10a89043dbd407b8059f8f31487eae53599` | 0 |
| common/grpcmetrics/interceptor.go | 2888 | `fced7ed428a571cc3991a761f4a375aef389464cba8d49afdc6b102badf133e6` | 0 |
| common/grpcmetrics/metrics.go | 3276 | `62859550cb48ebbb1bcc49d6d68a605b7964c17d13cfc147a9ca33b23d01dd7d` | 0 |
| common/grpcmetrics/testpb/echo.pb.go | 5540 | `6e32ccf5de5d9c55e35e2e1fe72f7f258edf880c7bdbc325cc1e9c830b7ac673` | 0 |
| common/grpcmetrics/testpb/echo.proto | 393 | `3f5e8f582ae32d9b25edebd855655c0cfde3c1df3da8f9d1c437a748946b6b40` | 0 |
| common/grpcmetrics/testpb/echo_grpc.pb.go | 5872 | `39d75304e585f5793d21dadcb0694a807306d0d1be1c765a63a637e756ba8e93` | 0 |
| common/ledger/blkstorage/blkstoragetest/blkstoragetest.go | 2414 | `827c474a2ddb3878ed92a97e0d936ee8b5b277737ef7992479fbd9f762753f60` | 0 |
| common/ledger/blkstorage/block_serialization.go | 5423 | `ba815b5113867e846c3807bef5c235c167dbad03a34d733173d67e9c96e2381e` | 0 |
| common/ledger/blkstorage/block_stream.go | 7344 | `92281a41f5ed76ba10e5c869f109b6601c66731a547a304b2aa2c0a457e8ed37` | 0 |
| common/ledger/blkstorage/blockfile_helper.go | 6740 | `9d6ebf86eb580515990be3dfd3c0190c600dcfb506132442b5e1b8679c2f077e` | 0 |
| common/ledger/blkstorage/blockfile_mgr.go | 28602 | `90537890eafb446e5648221282ad74f88547f575ebe8cc7833aa4e98d838cf14` | 0 |
| common/ledger/blkstorage/blockfile_rw.go | 2069 | `8c47b1ad5b77da6506f3f33b4043d3ad20f7310755ab41d8ef827194b08d6815` | 0 |
| common/ledger/blkstorage/blockindex.go | 16569 | `f880b20926d1e59a16c9ac73c7270beb45690fc98fcd643528d62fcc950bc5d7` | 0 |
| common/ledger/blkstorage/blocks_itr.go | 3453 | `4ba7f5ebba93fe98a60e83bca897d6c9945622d9a337bbc5980efdfd768cef42` | 0 |
| common/ledger/blkstorage/blockstore.go | 4278 | `599c95933d63d5acf063671945e752db33e5d2bb4f157896332f9b13766c24b3` | 0 |
| common/ledger/blkstorage/blockstore_provider.go | 5156 | `bddade8cd1e3b5c4a30f6c174b5cc34264a6e94c99c135f13aa4c8dd79271a8a` | 0 |
| common/ledger/blkstorage/cache.go | 2358 | `07a936c4ec4dad97de7daf48b58a97889f6f0443fa9aa3d76c859846873feed8` | 0 |
| common/ledger/blkstorage/config.go | 1171 | `c53bef6ca0e996ba35a97c47577644b3d75b2b0076c93d33f2d3e44f8b971630` | 0 |
| common/ledger/blkstorage/metrics.go | 1936 | `fe5d38200f957ac4631346ff592d6835d55f40af53a01978d6bdc0dfeb9ae7b6` | 0 |
| common/ledger/blkstorage/protobuf_util.go | 1328 | `27d6b58d6f48bd40d75f65b9ba33558a4660425594244812e14a367eb5ff68be` | 0 |
| common/ledger/blkstorage/reset.go | 7579 | `15ece243bab5dc2538928b9175a173831850caa7c897df6434f73f6408c790e0` | 0 |
| common/ledger/blkstorage/rollback.go | 8559 | `d6d420c857872c0b43ce40e42bfa4d5d345f255e76d529b0227c9dbb720fc082` | 0 |
| common/ledger/blkstorage/storage.pb.go | 8556 | `46c90bbf0b0ac382026755e28815743fee41582579434bcd00c0d8111928e514` | 0 |
| common/ledger/blkstorage/storage.proto | 444 | `fb6e0e161935c17578fd3ee7e51a7d79a4553d6659ac02c738cf0a1d73c14578` | 0 |
| common/ledger/blockledger/fileledger/factory.go | 3547 | `c9d99edc139f3df01517df4670f2d57765686fbb92f8671f9376020c66571dd4` | 0 |
| common/ledger/blockledger/fileledger/impl.go | 3960 | `2150f13759418b11799ccdb2ab37da02a8b9b9f66a30267b1176ee71c704a268` | 0 |
| common/ledger/blockledger/ledger.go | 1666 | `ceaf986a4e6ba82631943069f0e90917f6d1f36c6b90b1dfe39f1b5f33e741ee` | 0 |
| common/ledger/blockledger/util.go | 2783 | `51adef670cdc55250487a524da98a4c31b059618591b7eeef71addb79d0f202a` | 0 |
| common/ledger/dataformat/dataformats.go | 1490 | `0855f191d2dc141801fc98b00000694dd1115704fe198f414092bd10a7fdb43d` | 0 |
| common/ledger/db_interface.go | 1568 | `1352e7d4b9d352f8a40c5c1627742e953b5cc3258b467683039eec788cfc20ed` | 0 |
| common/ledger/ledger_interface.go | 2135 | `079fcdc40f021820a2f67bbcb1c3951b3710268c82362369a49ef8f7b1c9378c` | 0 |
| common/ledger/snapshot/file.go | 8033 | `2ebd37af0553e2cb6614a272ee1715d2808f739d82db39c6e9fe8cdaecc262a9` | 0 |
| common/ledger/util/dbfactory/factory.go | 2372 | `f5395a37cc893afb87d3aa44f08109e043ddd3a7148e6f20a6d8c89e4ba138d8` | 0 |
| common/ledger/util/leveldbhelper/leveldb_helper.go | 7723 | `35e2fcfd8abd64d767f04cfad61fc2c0f1e6007738e2243899af88cd4e2b066c` | 0 |
| common/ledger/util/leveldbhelper/leveldb_provider.go | 11096 | `a7ae55ca2f93e999a8a57042ae02a26cdd575505bdb3a2e92e07d7251f208732` | 0 |
| common/ledger/util/util.go | 2819 | `4dde8ecfac64c50f5f1fc2d12d95b02f156853418ceb7a5da00c16e923151981` | 0 |
| common/metadata/metadata.go | 336 | `5e480b5a2c6a5a23caaf1d5b08370cbd222a9e233607624dc4806f118138489e` | 0 |
| common/policies/bft.go | 1892 | `af74616343a18a7173453a7d462a04b574a4382464a1ce431f57cb8324fe5960` | 0 |
| common/policies/convert.go | 3888 | `78e77230776cfae9bf111da44ac481088a20d4761fbb82f70eaea153a6a36930` | 0 |
| common/policies/implicitmeta.go | 4212 | `b4010eea1b18b78749300d1cc18dd1285f03aa7176a06055422fb54541eca8ba` | 0 |
| common/policies/implicitmeta_util.go | 2430 | `755c15b514e7ba6859a2a37b5478d6fd06f9ccb1977aea429e9bcf9e88389f8f` | 0 |
| common/policies/implicitmetaparser.go | 894 | `17b74f4145da00cbdc7f7b6474f6cb624c518f7f334fdc7f03e9891577a3979c` | 0 |
| common/policies/inquire/compare.go | 7476 | `c0350428370d33406d557496a711c5def7e91e5eda93ba823b1b0ff6fba6478c` | 0 |
| common/policies/inquire/inquire.go | 2634 | `0e5092c7cd002ee971fcad3648b41ad4977f24effb000e9a0fd7eda1ba941b1d` | 0 |
| common/policies/inquire/merge.go | 10060 | `159b101fbcc3f28bf12e0626acd82df83cda7924c84c258c7e5e23098b95ae1f` | 0 |
| common/policies/policy.go | 13500 | `e70230e48ca0634e5398bb5994b9c128c5cc9a14c0ee68c72f8160a6e00bf1f2` | 0 |
| common/policies/util.go | 2547 | `f57783404698b8289239f0fb8579c73c84353a7bf26f6bcb31060bdc68a13a53` | 0 |
| common/policydsl/policydsl_builder.go | 7049 | `51023b84328eb4db246ef1e61f46d36add44019fe81e4eec2fbf70adbebb788a` | 0 |
| common/policydsl/policyparser.go | 9552 | `6ad016992600beca9fc436694071bd52a35f46b9710a767cda600c56e032a842` | 0 |
| common/semaphore/semaphore.go | 1294 | `dda4a6c1888911efca898e66a839b4805ab6e011d3e60aea1bbbbdb043cc82ec` | 0 |
| common/util/net.go | 1601 | `4fee8cf4a12d12aeacf0d2d0dd8c48fbd2cf74f99e3c59523411294ea25a8b78` | 0 |
| common/util/utils.go | 1871 | `68333d82b0a3b34f8ec6188bc7fa585309cb9086edc9d4491a9e08352676db3c` | 0 |
| common/viperutil/config_util.go | 10578 | `b430ed2480ec66c538edb5162852fd0ab77e160df390883ba0835fd1de44a1b3` | 0 |
| core/aclmgmt/aclmgmt.go | 766 | `ecb2f46f0c86c58590a9d02165e469aa28063631199c6c4ef21dd2c7c2055fbc` | 0 |
| core/aclmgmt/aclmgmtimpl.go | 1865 | `7b761b6dd6f056b80ba13e687c6ee3abd68519a7ae720f589c80be50f3d16810` | 0 |
| core/aclmgmt/defaultaclprovider.go | 7245 | `9f011dc439d15f984b02c4562880c5cd437683777a4e03f4ccf57d8e57394c37` | 0 |
| core/aclmgmt/resourceprovider.go | 6039 | `fbb59880ce8133a515f511b4da17bb3d46fbb88221ee5329b3fb8cf0bd261d84` | 0 |
| core/aclmgmt/resources/resources.go | 3029 | `dde36c6f7afad1708c70a3eac9e6b258a269aa0dfa36f6acdddc2fc526930736` | 0 |
| core/cclifecycle/lifecycle.go | 6795 | `2d9d075727f403e682ab301e87b727d2846a3fe9a04b8a6c4756b951bc75700a` | 0 |
| core/cclifecycle/subscription.go | 3780 | `e688a381e4fd1a3caced78964b394b58596e98eb9105ec86e92708a871a77102` | 0 |
| core/cclifecycle/util.go | 3163 | `93976af9c3cdc1bb653ade595616b890c2aa41d5050f3d3b1ea28509bcf89537` | 0 |
| core/chaincode/accesscontrol/access.go | 2798 | `765e46d821700c56f8a83ca58e4825be57a00c378c2c41d8540a896bbc7e64dd` | 0 |
| core/chaincode/accesscontrol/interceptor.go | 1832 | `60fc283d534c62cfb54bd3f99bfb60d73c6d4d70d81626cd84e4e26780d7ca28` | 0 |
| core/chaincode/accesscontrol/mapper.go | 1787 | `a6c370bf9df3384f64d1c4096e8146bfc371211520e43150724de49a19e9d6bf` | 0 |
| core/chaincode/active_transactions.go | 770 | `83050fe3e84947b4522e1cf39c17d86da821809eb5652bb9aa427ef911ea7ede` | 0 |
| core/chaincode/chaincode_support.go | 12853 | `f361b67f4e9c14d00bb99591783bd68509be3552f9ffc20ca5bab1e3abe1d777` | 0 |
| core/chaincode/config.go | 3848 | `56cfbdae6af9379b75abbeb9725525502c07459ba2581f16fde8f81622e8b4ce` | 0 |
| core/chaincode/container_runtime.go | 2405 | `215e3622c2711545daf5799c5975f90d770f59d650816cb30bc1fe371a6dca50` | 0 |
| core/chaincode/extcc/extcc_handler.go | 2041 | `ef163b3ac4b055627072d2bca229dcb2d6e7d5f2bf374ad832ba7bddf4a1e80f` | 0 |
| core/chaincode/fake/application_config_retriever.go | 3814 | `cda3a80d588885ce30303d0a8af5a98f61ed2c5587db3a0e4c867012ab6f11d7` | 0 |
| core/chaincode/fake/context_registry.go | 7168 | `20704c8648eb3a5bab3117e5e90b5668466463738d8b64c432c74577311f3b64` | 0 |
| core/chaincode/fake/launch_registry.go | 5192 | `c0d9f372a45e53dfdca9ff8167ed3518c58410c13527a2fe78c497b5eb53db35` | 0 |
| core/chaincode/fake/message_handler.go | 3483 | `e4a9c1b6120720a43fab30d5804d9a2fd2b82721c050d4e2fd0075f32cdf55c3` | 0 |
| core/chaincode/fake/query_response_builder.go | 4343 | `1aec928ca6398d160615e20f45793750a11951397361777271b9f6ea4bb1f2c1` | 0 |
| core/chaincode/fake/registry.go | 6736 | `72f296a3dff81e2ff88250b1138647362c41f597470816df14b4f1e5f67bd855` | 0 |
| core/chaincode/handler.go | 53422 | `1200d9f4ebf70de2e5a71b86eddbed0935b863399a46ecb88f34d5d25f483184` | 0 |
| core/chaincode/handler_registry.go | 5077 | `91f99068af52ac5135c3d0755ea9f3f1e4a44c6fa38c56ba7386a64641bc0356` | 0 |
| core/chaincode/implicitcollection/name.go | 785 | `26b473a3af6546334945f08e25187fd137cda600b58ca2604d6f7e477d2205b2` | 0 |
| core/chaincode/lifecycle/cache.go | 24471 | `96c93d0fbeb998940c4e3d3a756245797612178a0538374f51512b058e66d62a` | 0 |
| core/chaincode/lifecycle/custodian.go | 3427 | `5504b505ffc647b00f6bb7e224644eac6e41a1dd4bef93ed74dafbbd8fb722e4` | 0 |
| core/chaincode/lifecycle/deployedcc_infoprovider.go | 14879 | `ad8f5618a77a760733a6aaa6b962e791cc43c4f04a317c3a41c764faf1a49936` | 0 |
| core/chaincode/lifecycle/endorsement_info.go | 5951 | `3074a12ee102108a21a7cbe5383c523c8cf0d301322fe6fad9c67e204a02a8d3` | 0 |
| core/chaincode/lifecycle/event_broker.go | 8917 | `f09c4e47f5b5098fba707016b32875e5afabf828c8150a3575384dad99f031ad` | 0 |
| core/chaincode/lifecycle/ledger_shim.go | 6289 | `6a7a2405bbd77ebbaaabbc5ea18a162c0bb9cd1770cd9e39f6da06bd20c5cee1` | 0 |
| core/chaincode/lifecycle/lifecycle.go | 37113 | `735a727355c7f33a167b21ca96c0077b92e9569c11547b58786e6193b205281a` | 0 |
| core/chaincode/lifecycle/metadata_manager.go | 4154 | `bedb7024a09de971336202cbac0373d83cbbc4dd80770e35752b9df94d557953` | 0 |
| core/chaincode/lifecycle/metadata_provider.go | 7101 | `99f34d4dda923ae480141ca39a72056991d13a34abd5b077815a272ec53b0588` | 0 |
| core/chaincode/lifecycle/scc.go | 37243 | `2dded53ffd684fdd22db9a2d3e0d3dbd36b4fd854531c8ab5ee1f9415b1a0c7f` | 0 |
| core/chaincode/lifecycle/serializer.go | 16418 | `9192193409dfd126b34a283fe48fa4fb77974e0560acbabdaf82898c9a15691d` | 0 |
| core/chaincode/metrics.go | 3089 | `4ca0a1a8dd551e808911f5cd1fc805ac401d21b878c43a69550dad50a0845299` | 0 |
| core/chaincode/pending_query_result.go | 1040 | `f7956d5d4a3e8415f905243e1905730dea1dcc80bc0afb52df3ba02dccff72ee` | 0 |
| core/chaincode/persistence/chaincode_package.go | 9824 | `48439d6f30aedda3d2b0bd2c2679aa3e7ac85bb34a88e035c285ca1d55ccce33` | 0 |
| core/chaincode/persistence/persistence.go | 8564 | `c2f8a2b698e70ac36ad23d0f09c167164d4d09bc188b74eaf0e5d26e0484c224` | 0 |
| core/chaincode/platforms/builder.go | 410 | `d4cdb6a93a49b0ce109e4cadbdef1a6747751c819efe8617a2b43feeca1bb60f` | 0 |
| core/chaincode/platforms/golang/list.go | 3457 | `a6dea36b391e273e03bb8269c14bbc68c639766383b7998b2668a482f7616abc` | 0 |
| core/chaincode/platforms/golang/platform.go | 14272 | `b5738555199d713703d95bcffba502922dc67e064343092cade5d4aa0ada6296` | 0 |
| core/chaincode/platforms/java/platform.go | 3976 | `6e74e94bf34552e561463bce39a1afcabe66928dab65b445a6cc6711ec0d28d2` | 0 |
| core/chaincode/platforms/node/platform.go | 5510 | `ae4a38746df2c6eb1dfd38cb087ff94701ed24ddcd365d25b8c2195acd6e7970` | 0 |
| core/chaincode/platforms/platforms.go | 6954 | `e8150f9c21f95900f053a0ad4cc1c5976e0ef82cfaf769a506f87caba2b0ec7a` | 0 |
| core/chaincode/platforms/util/utils.go | 11718 | `b74ba8e0ef544b881f3ff26083b81025c27a362b59dbdfbdd1c2720b35c37be3` | 0 |
| core/chaincode/platforms/util/writer.go | 4038 | `1b3411a9d742d361d790a6fe64588f0a774fda2a96dd5dcee4d33b9a5b552d02` | 0 |
| core/chaincode/query_response_generator.go | 3225 | `796e0059288970ee7b32877eaf35333cc19ac3fe06e0f808254e407ffad4f462` | 0 |
| core/chaincode/runtime_launcher.go | 4611 | `209b1bdc2fa54d8821e30e968764b97bee77cf1d658d372d45d6b6d7b53cc643` | 0 |
| core/chaincode/transaction_context.go | 3899 | `6ce02837530f522de38545a3921a5215e3dbf375e8426a47c43f5e0dcd1853d6` | 0 |
| core/chaincode/transaction_contexts.go | 2854 | `07e780535716203bca4aaa56e41d11947ecb31e052efe1f808f4225e2cc4a4ea` | 0 |
| core/committer/committer.go | 2984 | `8b2b89ee7d7d62b06fbfc4011df78bb9f3aac2306c57318b1ced3de9cd733741` | 0 |
| core/committer/committer_impl.go | 3856 | `cf17456ee66abe9b15401d98f78a52ebbc27f712541b571758dde31465ed091c` | 0 |
| core/committer/txvalidator/plugin/plugin.go | 981 | `8f67ffbf453b02f16d62e0d12623bd51ab2b8a8198c2cbfa16ce6c4c01cc8d7b` | 0 |
| core/committer/txvalidator/router.go | 1640 | `efc700535a02d7819f97280d7c0e7ee36e2ec3bfe70abbb4dfb6f79774f20907` | 0 |
| core/committer/txvalidator/v14/plugin_validator.go | 8089 | `5b0940947a11cb5ae078055f6ea68c5591f60d22ac8879a3262fee8443d1f164` | 0 |
| core/committer/txvalidator/v14/validator.go | 22667 | `b6c608cf57544d5fe868ae3c493152ed111b763a8109d1653c8f784ac1f6a2a0` | 0 |
| core/committer/txvalidator/v14/vscc_validator.go | 15347 | `855c4283ee36d3226007dd85ef419f081a2b4ae61d408ab392dc986225ceb25a` | 0 |
| core/committer/txvalidator/v20/plugindispatcher/dispatcher.go | 11400 | `769b47cda2f8275492755e42c552a4b0a12c4a5c1ec8b322c47b0b85c97c1b02` | 0 |
| core/committer/txvalidator/v20/plugindispatcher/plugin_validator.go | 8789 | `bec781eef9b3cd2136aeb9a37aad475c4fc00aa69d80787e533bde4d709d3fb5` | 0 |
| core/committer/txvalidator/v20/validator.go | 18210 | `81316d4309df52e09a01b95e9b43c8183a3c6093e0e7d863e61fdd60fa9acd05` | 0 |
| core/committer/txvalidator/v20/valinforetriever/shim.go | 3157 | `437e538f78d1e7592c791b87184bb276c5c989b31d560f8eb834018e7c3e91ee` | 0 |
| core/common/ccpackage/ccpackage.go | 8477 | `56b7ec9c99409bba5d0e1a161514175654d00c94491cbd9aef656a3672f75a00` | 0 |
| core/common/ccprovider/cc_statedb_artifacts_provider.go | 3650 | `748982d03f2f2aa1c8d624c0fe924ebcdd2320859f5e06c2337e3ade66ca99de` | 0 |
| core/common/ccprovider/ccinfocache.go | 1865 | `1a005ce9ef5bd13f0859a99575b0e7bac11ca89787d83119eeb4383d348d12d4` | 0 |
| core/common/ccprovider/ccprovider.go | 12292 | `07baba41c8e6bfead02b66cbc3ca66894e3b72809b3701ebfef3cb9896ccb74d` | 0 |
| core/common/ccprovider/ccprovider.pb.go | 12951 | `0535b28adff59ff12d1703dce16ec01ec0b5b072275ea837962e46eadda6960c` | 0 |
| core/common/ccprovider/ccprovider.proto | 1798 | `088cd457fe6268fddece7e83178f2ad1f9e802ccf0a996893c262f7bb603e1ef` | 0 |
| core/common/ccprovider/cdspackage.go | 7809 | `ccbf78e49668a997fb522e0361f821c0ee1448390e6c12f7d4fd713661a45ba4` | 0 |
| core/common/ccprovider/common.go | 351 | `5e4509efcf0fdb02eed4cb0ca3e18d9d6a469d0e3c29bda5f023c62ff5deac78` | 0 |
| core/common/ccprovider/sigcdspackage.go | 9965 | `c065831355ef480617c95002a53155a103414d8500fd5f6619aed29fc37f9d21` | 0 |
| core/common/ccprovider/targzmetadataprovider.go | 1965 | `8ed00af5f8bd407759db8f43fd10deadf359d1952d504afbcca51ba094e39327` | 0 |
| core/common/privdata/collection.go | 6465 | `e0dce89c15745fe1db58ec824e6478a983012250f61821830b0125f8dbc15f72` | 0 |
| core/common/privdata/membershipinfo.go | 2112 | `2f8c1b58ba772b0a696b412cf2402491ab7786f4c7a7199793987691738f5694` | 0 |
| core/common/privdata/simplecollection.go | 4147 | `112e3740f88ca2e885048b2bf7c9873d298d2ea505677804c0c05a8b135983a2` | 0 |
| core/common/privdata/store.go | 9158 | `8b28ec9a92e6ec165a0e8f9aba392e5387ff90386b74f18212a088a4697cd549` | 0 |
| core/common/privdata/util.go | 2589 | `5e15b28dcb7276205b92ac83c91a61de76c50fe25c1cbac3ecfe3bfda2a6bcfd` | 0 |
| core/common/sysccprovider/sysccprovider.go | 1950 | `8df6f45dd9fe57c275301086184b0f92f8fad937e312a6a5b83d6feb3a986ab4` | 0 |
| core/common/validation/msgvalidation.go | 9675 | `363f5f553107e812fc03bd9b0c43f9b033c34c4b4289ca817f7b561809fc13cb` | 0 |
| core/common/validation/statebased/v13.go | 2467 | `06f855188f27ba3033e62d1e2864bd1cf9af797173829db858c84f28dd59382f` | 0 |
| core/common/validation/statebased/v20.go | 5334 | `9b02e65855fb46fb209e3c9ec966074ecb520777d3ce10a332e933b18b11a0a8` | 0 |
| core/common/validation/statebased/validator_keylevel.go | 12381 | `4e2ffd11924d24b63fce692215b6913efa4bd16b7295fb4bf3536f9a4f1b3c65` | 0 |
| core/common/validation/statebased/vpmanager.go | 3663 | `6efbba79f4e2906aa60c26d29a4f488c829becd58cb795370b11500ecfa76eeb` | 0 |
| core/common/validation/statebased/vpmanagerimpl.go | 12422 | `2a61247cba147fc233344590543d2d0c75bbd489deff8e5fca5c643a931ccf75` | 0 |
| core/config/config.go | 3665 | `f24a372cdc3a0bea8f8c665f4c4b7e63933098dd9a2461411b37ebb42dc33175` | 0 |
| core/config/configtest/config.go | 2258 | `9ac8b84e1e081d4dbb996c4503e9964d24d5448497f4718ea5907b4cc389ee91` | 0 |
| core/container/build_registry.go | 1686 | `bb52bf5c598ce00a16b12fee4d84ae0226fb148374b5a3a429d9235cb2eaea7d` | 0 |
| core/container/ccintf/ccintf.go | 924 | `7ac849e156ee7b4fb90e8615469b6905731110fd20ccc1bc172af26a6629ef96` | 0 |
| core/container/container.go | 5212 | `f420fdee36c268d6a418d3162d3a6e929e9678a7d8239d9f59d985243377be4e` | 0 |
| core/container/dockercontroller/dockercontroller.go | 15205 | `4598e49ca0b79de71114bf8b365d676270f2f14537ced0ecec25cd0811debfb9` | 0 |
| core/container/dockercontroller/metrics.go | 727 | `2e51e7d96431aede99cc3aacf1bdd566528bb03ce20c8b5078c0cd3fc4c26887` | 0 |
| core/container/externalbuilder/copy.go | 3117 | `a1949b51a01598e582decb92eaef48daa39d93a842feadc9680f260d7a3b6057` | 0 |
| core/container/externalbuilder/externalbuilder.go | 13169 | `a44608a579eaa22737a2b4b50cd127353abf8e0b11c5b73d01606950db828362` | 0 |
| core/container/externalbuilder/instance.go | 5302 | `19e0b89d2891d85ea66793e6d486d69b217a29e57eb63981be1c45d8029777f3` | 0 |
| core/container/externalbuilder/metadataprovider.go | 2174 | `3d30e54d9a8fe832d98d4a3afc45501b80cd1b8ae58c1f84ad7d59d37d9a098f` | 0 |
| core/container/externalbuilder/session.go | 2107 | `e8993e6f0d06c04f7a0b08dacd32007df87b89ecdb6234fbe1766ccbc2ab8068` | 0 |
| core/container/externalbuilder/tar.go | 2463 | `748ae7cadf374d03b067e57ab955101becca5646c7464425ba61a8713ce76897` | 0 |
| core/deliverservice/config.go | 8834 | `7fa35ff5f3a224d001482006f559fb25f3411ea17fc975833d05264b8b3cda9f` | 0 |
| core/deliverservice/deliveryclient.go | 13148 | `b3221d1d8c58d8d1e1ff38d97c4bf57f7f63b75a6ab1a66448ac8d0cb37ba27e` | 0 |
| core/deliverservice/fake/ledger_info.go | 5046 | `4277f770dac6c6417ac6bd45381ed32fded109a22d233208f3e3eb8bad541326` | 0 |
| core/deliverservice/gossip_block_handler.go | 2318 | `ed86d1ec3c10e7057235f21f1fdc9756ff042bfdec290582c7d1b115434bb52d` | 0 |
| core/dispatcher/dispatcher.go | 3061 | `94633561b732d0fb7573310de67828bfb3460bcd01bd6552efac710eb85c9e3a` | 0 |
| core/dispatcher/protobuf.go | 992 | `8394f803c4778ab5f29c618eb03b4c88c2c928ec5d878453af5baa8706bde3f0` | 0 |
| core/endorser/endorser.go | 24894 | `c2c2e576dc229e5ec54dc99cee2982a6b33079097228cb9d33f56182917b2272` | 0 |
| core/endorser/fake/channel_fetcher.go | 2946 | `958a2a4ce6349f165d3d35dc3c0706a662b005874883c3a3b4953f55762be6b5` | 0 |
| core/endorser/fake/history_query_executor.go | 3668 | `3e8df09fbf84be8931db187c2e0a177660faa6eb27fa09d8091aa37cc3fd58c0` | 0 |
| core/endorser/fake/id_deserializer.go | 5961 | `b5107cb5c9a558d2ad7598a132c12ca12e2c90dfd979e7c8233bcb62eacce3b7` | 0 |
| core/endorser/fake/identity.go | 18361 | `0474e86f6842a6ac3d81148e3f7f302ce142447432c64ab11801715da54c5d19` | 0 |
| core/endorser/fake/prvt_data_distributor.go | 4117 | `badd509b6c24607bd28c4e09a2c323dac82d2dbb778a40af927dbfbd26d486d8` | 0 |
| core/endorser/fake/query_executor.go | 43817 | `8cbfb6b20b894a7f66b1d28347e90337a37fbc99f10ef30fd6557d4d6905edad` | 0 |
| core/endorser/fake/support.go | 34653 | `0866de883f0746ae5eb42ae3ad2d288ee02d418e4292c417f06c45e30bd2e180` | 0 |
| core/endorser/fake/tx_simulator.go | 76084 | `e110150ce740730e40e714f7918a9f88dd35b1c6511466c4981e2aa1513e9ce6` | 0 |
| core/endorser/metrics.go | 3733 | `eb81602d19e31961ae80b049b013e1548bdd51390dbf0e49c385c1f84d4c1139` | 0 |
| core/endorser/msgvalidation.go | 6360 | `fc31b470af10d22f41561983834d646f1e69dfc9037e8dce5bb75b3043c632db` | 0 |
| core/endorser/plugin_endorser.go | 6249 | `540f087bf1aa97009a3ed649b56cbd1bb8527f37445b75a2fea64cd141d8e599` | 0 |
| core/endorser/pvtrwset_assembler.go | 3645 | `094bd45f6f3abadd3723ff18ad1d7d561003fa223418757914ad928f0dfb420d` | 0 |
| core/endorser/state.go | 1733 | `64b0dc3ba8515bd174c7c4b691c36ffd9ea413863b83308221949dcba2f49c98` | 0 |
| core/endorser/support.go | 5756 | `f73548ff27e34d9721fd30262a2efb6dde60897f31800781431120ccecc9f6a8` | 0 |
| core/handlers/auth/auth.go | 886 | `d5e139007ddee16056a4db16e880a05ab55c6a2b6227e35cbcf7b1c51c1c7564` | 0 |
| core/handlers/auth/filter/expiration.go | 1720 | `f6d676bf7e098f36ed32dca5de9a687cf21450ad99309b6b852c0d9e4ec5b3f4` | 0 |
| core/handlers/auth/filter/filter.go | 713 | `1f7a9436a32223dfd05b099027a348c99e8458973497084aade8cac557634bad` | 0 |
| core/handlers/auth/filter/timewindow.go | 2049 | `baf9b14daeae7c6e9ee46db8e1fbdd51b49b034d43f2c1f1eab33fe0af419e23` | 0 |
| core/handlers/auth/plugin/filter.go | 756 | `6b018c2be6302819e32033eaeaf394e7c21634c55e93e1e503c8236236ee1f93` | 0 |
| core/handlers/decoration/decoration.go | 673 | `b8ce9e9a5fd4076a0f1e2f278844602884cbff0686e3effad0849c64ee978d7b` | 0 |
| core/handlers/decoration/decorator/decorator.go | 536 | `0a40f29579a2607b634e1c26ad961afbf4c2191b6e34f49816b964c19ad361ae` | 0 |
| core/handlers/decoration/plugin/decorator.go | 576 | `400d25f74f0a42c61c453f1ae5c65959d1a3a9026559fdda72f4570f5fafff07` | 0 |
| core/handlers/endorsement/api/endorsement.go | 1070 | `3f1aa2bcb35131b027cc1f066d64b5c6ca926b54903a12a7b08dbcfd22799c39` | 0 |
| core/handlers/endorsement/api/identities/identities.go | 902 | `699a88f5fe87116881880b9876294c66606b63befa2144b29b4f2d20a647ae46` | 0 |
| core/handlers/endorsement/api/state/state.go | 1048 | `f9208fa706475cfb8f1cbc476a9ff0035394141ddb671054c16b99c4b272de5e` | 0 |
| core/handlers/endorsement/builtin/default_endorsement.go | 2501 | `ded0ab3acab9bbc54e5a338bce434acb4bee30722342a4876851e47cc9b686a4` | 0 |
| core/handlers/endorsement/plugin/plugin.go | 2787 | `5aae725a1ac4e2daf07cbd1a8a32c1ccd43784fb082f99629172f13792ef2185` | 0 |
| core/handlers/library/config.go | 2405 | `7f66ce37fe60d20da77cd8555090b1e29dcc0bf616a33afecfe2665a47ede53d` | 0 |
| core/handlers/library/library.go | 2036 | `2d735e0fc030af300811f935a55c3df1c11620efc516a6051f807471d6a3368a` | 0 |
| core/handlers/library/plugin.go | 3568 | `4adf2e5a43c3627b88ec8f91abd70a7fc9a501dcc73d0ab9aa1b363f721d9c0a` | 0 |
| core/handlers/library/plugin_stub.go | 332 | `c830bd55713503405676031cb1374f76e081b8bcb8e6603252e81c1c04ee9845` | 0 |
| core/handlers/library/registry.go | 4026 | `4b3e7c96dffdd459d71ea85b880785a34d78c8d0ab0eb71370b41f48f323b3f6` | 0 |
| core/handlers/validation/api/capabilities/capabilities.go | 2414 | `69e58398a7848ed7b35ac021fee3dea7b2e94eb0ca138381482f4f9f7d5c4607` | 0 |
| core/handlers/validation/api/identities/identities.go | 2060 | `ed6ca6ca0d8c215bfd539c0c9558680ce64de6a62fc0e42a40add6c58b2fe753` | 0 |
| core/handlers/validation/api/policies/policies.go | 713 | `1da192639ee3556d20c7ce5d75f1ed293087089f5aff88e51a95818066963bef` | 0 |
| core/handlers/validation/api/state/state.go | 2141 | `51b37c32c84cb132a7ed3b0c00925cfcb5aab0ca6bda644a5c6eb8fd119524ca` | 0 |
| core/handlers/validation/api/validation.go | 1437 | `2accdb46e239e8647421025fca1a1ada1c752d008e6d11fce4c7b79bb7033dc8` | 0 |
| core/handlers/validation/builtin/default_validation.go | 5222 | `32a2cc52d09082526c46e83d18e116a34596519c124d1f7267e28916c5ec007d` | 0 |
| core/handlers/validation/builtin/v12/validation_logic.go | 31780 | `97fc8933e7e0fdab0aa59f56fe3a3f41e0fa9dd9953be2aa142b32e3226e4738` | 0 |
| core/handlers/validation/builtin/v13/lscc_validation_logic.go | 24987 | `10c04d59828671eb8c407cd24c5654c1069ee47a9a8df283e7ed494ca11f041c` | 0 |
| core/handlers/validation/builtin/v13/validation_logic.go | 8041 | `1a157fdbbdf5b8d2137a07e3db48341f70d8381ddcef80c1f2e58a11b464760c` | 0 |
| core/handlers/validation/builtin/v13/validator.go | 1789 | `6f79bc85432b8c33fe147b8cb35848cf931c222ce449424a64269c8f360a6bd1` | 0 |
| core/handlers/validation/builtin/v20/validation_logic.go | 7416 | `b298559a7d1c889345ea43a9c83641e89650344b6ae4ef68310651bb40c9575b` | 0 |
| core/handlers/validation/builtin/v20/validator.go | 1789 | `2dbc9794f3deeaa26e2c7a6926b62668f551a313f86ce973df9dc34e6b02afa2` | 0 |
| core/ledger/cceventmgmt/defs.go | 2422 | `726c6410bf5b5e9b4e471af0f51b59f21804297012008bfa2f806434751d7895` | 0 |
| core/ledger/cceventmgmt/lsccstate_listener.go | 3181 | `da54a98e3e44c4fff3a27eacca2e86eaec7f9ebc65d5818da73a92695a8f9e60` | 0 |
| core/ledger/cceventmgmt/mgr.go | 8888 | `7a95971701d8550eddb53ef06b5f4fcadd7fe374b768da91bebeb827aaba1c0c` | 0 |
| core/ledger/confighistory/confighistorytest/confighistory.go | 2029 | `dc5cbe6e97e582df41418f741e76a2287792c7c0a9cae43adf24daf01fb1eed8` | 0 |
| core/ledger/confighistory/db_helper.go | 3512 | `fda1fa7ea6199f6f933c271183c3bad8ea9040fc40c5a66fac57e1eeb0004a20` | 0 |
| core/ledger/confighistory/mgr.go | 10613 | `3ea0537470e8440ffdbc7214bd7bc19e08f51a83db53f85e79d2fdf28fde154f` | 0 |
| core/ledger/internal/version/version.go | 2342 | `db0d31ca03684f1b01876e952a7ea3b7e8e225e257f7bdae2e811abef91d6612` | 0 |
| core/ledger/kvledger/bookkeeping/provider.go | 1793 | `fd4613db3dfe8972ff6e2f62d9fc6e27bd53b6c5cbba5cfd57962e81da3a0af2` | 0 |
| core/ledger/kvledger/channelinfo_provider.go | 5445 | `c7708d5d81a6c6491f74b4f00d4cc139742e3d555709f6d551b600861a9630ae` | 0 |
| core/ledger/kvledger/coll_elg_notifier.go | 6246 | `3dca732fa2cc00a02910f953a6818a7b3d070259de2f4af086ad1ef510ea1aad` | 0 |
| core/ledger/kvledger/drop_dbs.go | 2209 | `475aae186271b4a8bf5d3841f8041c74781f2583917a40afa871cdb093d94e8c` | 0 |
| core/ledger/kvledger/hashcheck_pvtdata.go | 9195 | `c58f991eaf6f947a99947a63e859e4b598ac11c5880a2eda417fa041bb807ace` | 0 |
| core/ledger/kvledger/history/db.go | 6431 | `8fde9a93641969759ed77f68804836d99fbfc7f554593606c3784dc5d56d727c` | 0 |
| core/ledger/kvledger/history/kv_encoding.go | 2670 | `029cc86d111a614233a29a3846b592761ad4bfb38665776274f859623b78a774` | 0 |
| core/ledger/kvledger/history/query_executer.go | 5377 | `75cfe3ff686f18eb07e2c899dfda6a95f1b099d9971c263b342f2c70e0ba1e49` | 0 |
| core/ledger/kvledger/kv_ledger.go | 42788 | `b7cd48e6cec6a1a812ca46ad213b5d5d28c8c2033a6e2386fc6b35ccf2458668` | 0 |
| core/ledger/kvledger/kv_ledger_provider.go | 23793 | `d7a97225dbae48393191c0c9888df11a1cacb64588754ca0c57afb66278c8fb5` | 0 |
| core/ledger/kvledger/ledger_data_remover.go | 2434 | `ae0fe52045ef1507688da51a7ae059cbb0a54d20a43d60dfac64b938a6fe8075` | 0 |
| core/ledger/kvledger/ledger_filepath.go | 2395 | `110be2b94b179ac59d8369cc32f7f9e3da4790086a85b5485ba154be83a1d471` | 0 |
| core/ledger/kvledger/metrics.go | 3683 | `035022be85f57a9bc653e58102ea55ad04463945bab67c4d551301bf6125e76e` | 0 |
| core/ledger/kvledger/missing_pvtdata_tracker.go | 1783 | `0ba9fd1c847e4edbe2397ad5f783fae7c5b84272a1cf8f6bbf14d54b4b6ef85f` | 0 |
| core/ledger/kvledger/msgs/ledger_metadata.pb.go | 10540 | `ed31c4976f888474b71e106d309c73c2ab1197bca038ddbc2c6b830f5f5e77b6` | 0 |
| core/ledger/kvledger/msgs/ledger_metadata.proto | 829 | `fef12c81ef15e864b7ca0c18238529c818a07435f7f647af30fbc23cef4a0044` | 0 |
| core/ledger/kvledger/pause_resume.go | 1546 | `ff170f4243c8263b7270772ee64498efb685327509abf4cd683de1b7f484c6a9` | 0 |
| core/ledger/kvledger/rebuild_dbs.go | 1622 | `fcbe42348384b66698906da8085605a31a90af0cc3f3bb32949a985f71e2162d` | 0 |
| core/ledger/kvledger/recovery.go | 1242 | `4ce95c02d63a0fffc6acb8f4ab797f16f9df7276361a62bb6d6429e08c1f1290` | 0 |
| core/ledger/kvledger/reset.go | 2428 | `9c941c65b9f866b10861494de9947352e0137a5cd9058886c99098c8a55fcc74` | 0 |
| core/ledger/kvledger/rollback.go | 1735 | `56218c40b8ac76efac0aa025eacc590b3d550428e4fadd71192c227b4bcf7e09` | 0 |
| core/ledger/kvledger/snapshot.go | 15192 | `ec2ced1276efff76a07c5bb2fc9ff3f579ab1486f13f9ab99009903c3f13405a` | 0 |
| core/ledger/kvledger/snapshot_mgmt.go | 14018 | `4c171b342f6443adf8411579cd47ba3035b2420a31e45272406e061db65c3ebb` | 0 |
| core/ledger/kvledger/txmgmt/privacyenabledstate/db.go | 19175 | `aed72c28bed3034ac0783a7cacbbcf1702f7d105dd23b844b0f10462af1e6975` | 0 |
| core/ledger/kvledger/txmgmt/privacyenabledstate/optimization.go | 1932 | `b640cfc021514946d86eb643f5953790b3b2a676e3ef472cccda54abb966ac29` | 0 |
| core/ledger/kvledger/txmgmt/privacyenabledstate/snapshot.go | 15089 | `b4e468a15204f92f009a21c88798a8ed848cebe3cb4daf69f4865d5e72e08d0a` | 0 |
| core/ledger/kvledger/txmgmt/privacyenabledstate/snapshot_record.pb.go | 6012 | `ad76d77d611dcb5e3c7c2fe45d506f8dda3630acdd565b6cf3693a9870d4fbe4` | 0 |
| core/ledger/kvledger/txmgmt/privacyenabledstate/snapshot_record.proto | 363 | `c37283ab281d4ff489590b95c5d2859d895825a0b96c93ed345405a55d1e04cf` | 0 |
| core/ledger/kvledger/txmgmt/privacyenabledstate/types.go | 6684 | `64e9981aef75e440ff5b62b4df49dc682ef11b7410c265bb59a7905fc996636a` | 0 |
| core/ledger/kvledger/txmgmt/pvtstatepurgemgmt/expiry_keeper.go | 5167 | `b84ee3f06fd96d829774cde4918dc989c7b5352f269ecd3e9f4c4024b7a53811` | 0 |
| core/ledger/kvledger/txmgmt/pvtstatepurgemgmt/expiry_schedule_builder.go | 3783 | `6bfb253738adf106791af136e00dcbb902a40ee86d46c0f37d1fd57a5cdb3d81` | 0 |
| core/ledger/kvledger/txmgmt/pvtstatepurgemgmt/purge_mgr.go | 12369 | `1bd915da28cd951d680539e5b799b352577b8914b77e2bfa19fdd17b4b713c38` | 0 |
| core/ledger/kvledger/txmgmt/pvtstatepurgemgmt/pvtdata_key.pb.go | 12602 | `09a38648d79d739ab624d599697ff3ec6ca859c9a0b489b7c3bebd4f9d468948` | 0 |
| core/ledger/kvledger/txmgmt/pvtstatepurgemgmt/pvtdata_key.proto | 486 | `cb8a0dd89260ba2c465e76d5d4d93fac5acf618fe004b48868ab96b17f9d34ec` | 0 |
| core/ledger/kvledger/txmgmt/pvtstatepurgemgmt/pvtdata_key_helper.go | 1300 | `49bd007853dc3b778a52b516dd96b6803456fb198de3543211d849fc69f05b1a` | 0 |
| core/ledger/kvledger/txmgmt/pvtstatepurgemgmt/snapshot_purge_mgr_builder.go | 1941 | `0831b555d5e4428b5947410edc6550d10e356b45724b5827a94c33a5b9f6d7b5` | 0 |
| core/ledger/kvledger/txmgmt/queryutil/iterator_combiner.go | 4449 | `f8cfb0143cf946d2ed0260199709831f21fa2425e4de0b2bf519137875f1f042` | 0 |
| core/ledger/kvledger/txmgmt/queryutil/query_executer_combiner.go | 4475 | `38d1adb9e03c779e0e6db7471ca3080f0ddef75e5c933ed7432f86147e0a1339` | 0 |
| core/ledger/kvledger/txmgmt/rwsetutil/kvrwset_proto_util.go | 749 | `b9d278d6ffb4ea18edc8df3809a49456f27e55c1469158df6c25835ae4c02c9d` | 0 |
| core/ledger/kvledger/txmgmt/rwsetutil/query_results_helper.go | 9224 | `e29152168bc52441d78a14f3d7ba6f3c9afca8e10a5a5be31800ba9c90312c61` | 0 |
| core/ledger/kvledger/txmgmt/rwsetutil/rwset_builder.go | 13238 | `fdf5aa5b958e8d0e17a03dabdc8716340d72bf73c5188a42a308ada99879f628` | 0 |
| core/ledger/kvledger/txmgmt/rwsetutil/rwset_proto_util.go | 13065 | `5e8d373b4f0ac133e247902212e07b56e2f59c156fe632ddc1db2edfaa31a0a8` | 0 |
| core/ledger/kvledger/txmgmt/statedb/statecouchdb/batch_util.go | 974 | `ebb02507e7cad863c117992a52dc01d79f30ce88427d2e600c5721325b3b2ca4` | 0 |
| core/ledger/kvledger/txmgmt/statedb/statecouchdb/cache.go | 4389 | `c93b30697e58798c42041a7f333826e81a3172a4610aa9403dab82602de3e26c` | 0 |
| core/ledger/kvledger/txmgmt/statedb/statecouchdb/cache_value.pb.go | 5924 | `273ee9e237ea9872c2d15973a99f29a8c8398d7c6d2dee1c89b4d1f97bd2b175` | 0 |
| core/ledger/kvledger/txmgmt/statedb/statecouchdb/cache_value.proto | 353 | `6571be8ec857248586d37f2a634bad78068246253525cad61ef15def85d5db75` | 0 |
| core/ledger/kvledger/txmgmt/statedb/statecouchdb/commit_handling.go | 8663 | `da9da38ac67f1f9d3760bcb91c07e2f7e060b80826206e868dfc0c08cb13e768` | 0 |
| core/ledger/kvledger/txmgmt/statedb/statecouchdb/couchdb.go | 60227 | `c66b04097312a51f68bc5dc8ecd72f7b35cc58ad59f9f96daafaf551494d332c` | 0 |
| core/ledger/kvledger/txmgmt/statedb/statecouchdb/couchdb_test_export.go | 1302 | `b0d62cbaa6902c3586d65e8076bfd7fa10535607c0277b1bd3958087c97055e2` | 0 |
| core/ledger/kvledger/txmgmt/statedb/statecouchdb/couchdbutil.go | 12997 | `6198df1e629aece47308419376b526caa45a29d8055b5108b77aa278ceb81f77` | 0 |
| core/ledger/kvledger/txmgmt/statedb/statecouchdb/couchdoc_conv.go | 8804 | `d08c997408803788036190d2d5e69dad4dc47c6265120aea1828f854d6b02983` | 0 |
| core/ledger/kvledger/txmgmt/statedb/statecouchdb/dbvalue.pb.go | 5119 | `f9d75e2646d0c18a934cd2b37fb3595032fd5c3a09a99280a5927723fb00df33` | 0 |
| core/ledger/kvledger/txmgmt/statedb/statecouchdb/dbvalue.proto | 309 | `282dd12ff467313be7af0b1f02427d1cb46ec2f7fa38968a97f20e051db26e4b` | 0 |
| core/ledger/kvledger/txmgmt/statedb/statecouchdb/dbvalue_encoding.go | 1188 | `59d3fcefa6490969cc58525524b42fe2dd7038212b53e502419b6818bc2ff829` | 0 |
| core/ledger/kvledger/txmgmt/statedb/statecouchdb/metadata_retrieval.go | 3202 | `4a2698498b55cb941229eb4bf784037641dfca03c3f10be48cc8ad3587239081` | 0 |
| core/ledger/kvledger/txmgmt/statedb/statecouchdb/metrics.go | 995 | `deae914591e5a5cfddc6ffe7efceb01632e7233e598c81bf2c25586126f52866` | 0 |
| core/ledger/kvledger/txmgmt/statedb/statecouchdb/redolog.go | 1815 | `4733a447d4f1f416b0297dac1e7b2f7317b5a14bd6cc84c45cbc18c539f45317` | 0 |
| core/ledger/kvledger/txmgmt/statedb/statecouchdb/statecouchdb.go | 41582 | `d35ad1a73bfb4ad47ee3647313c90457c154f58fa95ef7c22588f478d10fe29a` | 0 |
| core/ledger/kvledger/txmgmt/statedb/statecouchdb/version_cache.go | 1843 | `5e449eb7141a4ca1a06cb3adf2b687ec253d9d993260121bbf9b8418c0953ccc` | 0 |
| core/ledger/kvledger/txmgmt/statedb/statedb.go | 12522 | `477e5c96d23b602b89a17f9dca4fa722f896147c661ba34fb7c80d17c7a94447` | 0 |
| core/ledger/kvledger/txmgmt/statedb/statekvdb/db_value.pb.go | 4125 | `3f130ffe39b8393f6308221c22448529211700013e6f8e897d39fc8f02004475` | 0 |
| core/ledger/kvledger/txmgmt/statedb/statekvdb/db_value.proto | 313 | `fa7bee11ea6fe058ea2e06bc499577b92a18b5509d214b44d8dad440b896901d` | 0 |
| core/ledger/kvledger/txmgmt/statedb/statekvdb/statekvdb.go | 12090 | `bbf789241641c82d06ddc2e626a98545a28b33e0a013d464e8c21fb4dbb516e2` | 0 |
| core/ledger/kvledger/txmgmt/statedb/statekvdb/statekvdb_test_export.go | 797 | `772ccb0d05599c7f7c1772e554a2d446e4bde77f869bc4019c8fbdb402413f05` | 0 |
| core/ledger/kvledger/txmgmt/statedb/statekvdb/value_encoding.go | 1096 | `dbdfbbbbe841f4718add0c56f9b5d68330d4bda7ba2ccf56667f99122ef2d5e0` | 0 |
| core/ledger/kvledger/txmgmt/statemetadata/metadata.go | 954 | `c0862d64d28bd84d3a0132f0d3b23a00f5b82fa421f2f527dbbd2ab599c57e65` | 0 |
| core/ledger/kvledger/txmgmt/txmgr/collection_val.go | 2434 | `d60cdf2e686d39b43edfefe43c5bdea54c4babc0a58716735b3e6fc383d03552` | 0 |
| core/ledger/kvledger/txmgmt/txmgr/lockbased_txmgr.go | 27124 | `d503e2fd8c9301a63fe01f5cf352190fa3dde63ae7b851c1c5aedf51f35608b8` | 0 |
| core/ledger/kvledger/txmgmt/txmgr/query_executor.go | 18752 | `05ab1351d9e7d1a3baf0cf005016c272566fa1694bbba3f4e14216aafccf3100` | 0 |
| core/ledger/kvledger/txmgmt/txmgr/tx_simulator.go | 9567 | `70bdc643a565247996db085198bf8e0811202cc91faed074ad9cd2a7f9eed68b` | 0 |
| core/ledger/kvledger/txmgmt/txmgr/update_batch_bytes.go | 3386 | `3b5c20f81e8d1767cbfa63cd117edb50bf34eb7c24546a0316acf6a1154603c4` | 0 |
| core/ledger/kvledger/txmgmt/txmgr/updates.pb.go | 8010 | `91c40862ec87072d965858c6a49b5020bab1df89f729628cf393459801254fae` | 0 |
| core/ledger/kvledger/txmgmt/txmgr/updates.proto | 430 | `1f70ad55b5382f6bf0b817daca655cd221de385a23b7566ac6bb0c814c2df85d` | 0 |
| core/ledger/kvledger/txmgmt/validation/batch_preparer.go | 16370 | `23ef145ac8d24dc48c7c2a39201b9dc991411e731c6857f7e6966c42fff1fbc6` | 0 |
| core/ledger/kvledger/txmgmt/validation/combined_iterator.go | 5067 | `683b65ae664b93591be2d63679409f0298ac89ff24021a394220f59f456b98ac` | 0 |
| core/ledger/kvledger/txmgmt/validation/rangequery_validator.go | 5838 | `40a639488e05f9fb567066577a797e7bf011821137cffd722ff4b3b820b9fe88` | 0 |
| core/ledger/kvledger/txmgmt/validation/tx_ops.go | 7040 | `6e26be06668552567d9f637b2d195cbec4df224b280748eab2171f7fa81fbd0b` | 0 |
| core/ledger/kvledger/txmgmt/validation/types.go | 3378 | `b228cd9de65c0d4e5ac4e1330c9399531a32d422ce03da8dc5670f1eb6a03195` | 0 |
| core/ledger/kvledger/txmgmt/validation/validator.go | 14024 | `3a570273934edd6a79ee1f51d75ce8bb8449fabe6620cd9aca541519b2dbfe2a` | 0 |
| core/ledger/kvledger/unjoin_channel.go | 6249 | `0d94e5d15a4a466e3cb19e8251b630ff08eaa25d0511920f205e1d4020683456` | 0 |
| core/ledger/kvledger/upgrade_dbs.go | 2242 | `3effb52bec3956d439b1ef4be6201ae0f9766e10f34592b50504a827d4d8c39b` | 0 |
| core/ledger/ledger_interface.go | 43354 | `bb4558b7eca6558d36c98d846ee9c508015f8fee7186255e66d34a6ab27b1990` | 0 |
| core/ledger/ledgermgmt/ledger_mgmt.go | 11931 | `1b84c59fa14d2c79d9805c2d62beac5ca1ed3c3480d1f938359e62076ddd7edc` | 0 |
| core/ledger/ledgermgmt/ledgermgmttest/ledgermgmttest.go | 3258 | `5e4cf513cabf5e5f3751f09f30e09245a32f4b2f556fdc2deb15dc9450f3bb24` | 0 |
| core/ledger/pvtdatapolicy/btlpolicy.go | 2943 | `f20be984103f1e9af1088c588faf3fc26d747bfa67d3817c7d8917e1bd78b395` | 0 |
| core/ledger/pvtdatastorage/helper.go | 10531 | `07485a8b6786420684716661e870bc308f3f9ac2fd90b2db3b7139fa70ee0358` | 0 |
| core/ledger/pvtdatastorage/kv_encoding.go | 14645 | `78e17e8d7235cc0aebc4f3a34145b9d77ffa56f54de3c8dbd6be5c811292493f` | 0 |
| core/ledger/pvtdatastorage/persistent_msgs.pb.go | 22845 | `dee9a35db75dd660c58adf220a82d1d1a52b8efb241b44434102d323194c6c9b` | 0 |
| core/ledger/pvtdatastorage/persistent_msgs.proto | 942 | `5dc173dc6af9791e63c6960c69eb68799f840a8dd826536dcc9b77e38da5fac7` | 0 |
| core/ledger/pvtdatastorage/persistent_msgs_helper.go | 2250 | `0f0f7b6d2555bbaa9aade63b8188451c0fb92bb187c059fe758746a1534fafdd` | 0 |
| core/ledger/pvtdatastorage/reconcile_missing_pvtdata.go | 12298 | `1c1a93e459e2bf2ed0555e1a015bd5ece571e28e0b8b5c4f4ae3f4cbbe41384f` | 0 |
| core/ledger/pvtdatastorage/retroactive_hashed_index.go | 5002 | `e50363d1ed1c32052028e47e30bd22ec498f72681f4edbcca41eeb896f83292e` | 0 |
| core/ledger/pvtdatastorage/snapshot_data_importer.go | 13614 | `12b71faa50c9b32e6bc12f69a3d5e436aeeedd2296e5918b9847f10c9a934c83` | 0 |
| core/ledger/pvtdatastorage/store.go | 39817 | `6b83c0caec4295476ce50169a57b5beefbeb4cdf73f18e2b66c67fae2d076aeb` | 0 |
| core/ledger/pvtdatastorage/v11.go | 1405 | `3633e4521e5f7fd3371f07218f98c4c9d68328de859072f66c4aadf06435d0fd` | 0 |
| core/ledger/snapshotgrpc/snapshot_service.go | 4131 | `0f649a68953874a4707cd4d27986aed23221726b2887f1aba05bd2622cb6af6a` | 0 |
| core/ledger/util/util.go | 2364 | `e87c03551e54a0ace635fb50d56a2b5d4d83adb66165f42c608b127a8aeee7fe` | 0 |
| core/middleware/chain.go | 843 | `3591fd039f105c285a5900a0867c1b189b32c1693de6fb1ad33cfd0e0b313a42` | 0 |
| core/middleware/fakes/http_handler.go | 2122 | `85eda81b8dd4ec2e20df2569dbad3f25b281536643032e36a1602edf03f9b9f9` | 0 |
| core/middleware/request_id.go | 992 | `f02bc4f82565c39c5b159ec1b530cd16129227a7b753fa90800199f2f5f1fbbf` | 0 |
| core/middleware/require_cert.go | 882 | `58b8ceee65b4aae6d0f66d013242abc611b2257996bcac4f7eadf33552e75d53` | 0 |
| core/operations/fakes/handler.go | 297 | `ece8422ae68c0b8f2bc2a531346aeccb6afcad7bc6bbb55433a6b8751245f06b` | 0 |
| core/operations/fakes/healthchecker.go | 2950 | `10deb030a418e16000c275b8c1b661aad7524f45169a22aeb5cb08fcb64b9c16` | 0 |
| core/operations/fakes/logger.go | 2923 | `8b385953a09195b8ee5150d2db37318672fc0418fa1a362955413f9f72b2f7dd` | 0 |
| core/operations/metrics.go | 853 | `92282abff00347a872cded7fa57c39cb2dbf3fce17c0b03481098e002709ba6e` | 0 |
| core/operations/system.go | 5716 | `7361dbcf4d24c3bd2256628a3ffcb854b78bc2798a5b36c8c697662113697bb1` | 0 |
| core/operations/version.go | 1204 | `f74f258de6c03d3aa0755769263dc59dd83af263e7058b8e10273dbd81994715` | 0 |
| core/peer/channel.go | 5115 | `b230b953797ca81aa0348582e9ac31ab3adb358c4c7b2591433c50fd572fcfac` | 0 |
| core/peer/config.go | 20037 | `aa25024a89d6684dd921c5662fb1c96633a025f4cdbda521e9e0e8848814e5ba` | 0 |
| core/peer/configtx_processor.go | 1868 | `e95f108c40729923468fe50b2be74d85c454120e53f40a063c431f0bb1cf9337` | 0 |
| core/peer/deliverevents.go | 17714 | `0e049f462a30d9c2f01ac27d6907ae9667cbd8976170953acaa08e932bd603e9` | 0 |
| core/peer/mock_helpers.go | 1003 | `117efa0ba0b9813de532b0c8cab2ba7a1356b34ce7d234db4d312b5aac557c45` | 0 |
| core/peer/peer.go | 16585 | `5b2568556b8addb6ccae8e1d07fdb42725fc80b1a85110916b4e4f226311aebf` | 0 |
| core/policy/application.go | 6009 | `c8096b5a118dda58b73fc4f5d0edccbc34264d313ed57770ba7f945246abfae4` | 0 |
| core/policy/policy.go | 9783 | `9956f64e26fd3a40c3d977d5f8563c0edbd8b56655c17397ca8ffde052996496` | 0 |
| core/policy/principal.go | 2271 | `9d123582b0ea3968b549fe109d0ee5b05153c2fbce864f1d82d056cc297cfc9f` | 0 |
| core/scc/cscc/configure.go | 12297 | `244b59c038756e1b84e2e1b891a72fea83b8ec73104cb1a18255578105dac807` | 0 |
| core/scc/inprocstream.go | 1272 | `44de246c303b36b192ac003281a3dda52471462589b30ebf55a77c00c460a934` | 0 |
| core/scc/lscc/deployedcc_infoprovider.go | 5877 | `1071f47ccaf36dae5b8eef2899e61f311780dcaecb700fa9de70d1c4ff7e8dad` | 0 |
| core/scc/lscc/errors.go | 3824 | `1b11cd64769f970d69845a90dedd94d98023219afd8ab039df1e7a2e68a6cc9e` | 0 |
| core/scc/lscc/lscc.go | 11546 | `efae71264a7c47bb883c422eaf8d16c22508dc58954360aaab9178c4aba0209a` | 0 |
| core/scc/lscc/support.go | 3822 | `d22f591f0d1667a9f00dd54f83a64a12706cff33600523dfa7b877a2856eb47f` | 0 |
| core/scc/qscc/query.go | 6984 | `2df60e9435394b9701cd411da9bb3bddc172f34d3c144bfd7db4a76b67af0215` | 0 |
| core/scc/scc.go | 3191 | `2d1cb2a365ff5c816bc9c3933b50f5e6afb6ce135c1b02b9f48ef7ca60877f03` | 0 |
| core/transientstore/persistence.pb.go | 4795 | `95bed4129519586e6608abb9c08510ec4a2d58307eacbfba93233454d0fdae91` | 0 |
| core/transientstore/persistence.proto | 270 | `7fb127ef1f179b1cd2466c9d45c22d518205bc34d8f0ab159366bf9e45836607` | 0 |
| core/transientstore/store.go | 21019 | `513479c094129d6a577b9fad6b07dd3028b570e16dab422bcdbe3e153d1e18d6` | 0 |
| core/transientstore/store_helper.go | 9716 | `d7ef37b10de6749cc798763ec623f675c88a45dd70725a4c1331ae0f82a4fe76` | 0 |
| core/tx/endorser/parser.go | 5565 | `5b0670ac6cb4e55326ea0e2bdfccff133ffcd386c504ed689d97f29c73482323` | 0 |
| core/tx/processor_factory.go | 4103 | `169d8f2d03877e8785afa3764429b645a52fa18afe157e6b2db32b68239a6aeb` | 0 |
| discovery/api.go | 2881 | `aba538b2538c619b5da8b444e5e2f3935ce1527ca43ec5f1a67ed343229d3999` | 0 |
| discovery/authcache.go | 5292 | `9f4277ec9a07a15bae8731915ef0cd56484ff2d0e3644464e4882ebbb2c3c047` | 0 |
| discovery/client/api.go | 2559 | `0356281881bb04081ac1aedbbf6f0a0369c8180e14dfd5e055f64293de608c57` | 0 |
| discovery/client/client.go | 18749 | `4d7c22d357c31b203f17245c0937d72a9790692a2b3bf4afca088cc1e9bfa426` | 0 |
| discovery/client/selection.go | 3947 | `4109eb8dddeb58dc0a7096da8e3c3b32edb40c7fff75f1fcc462fa65256fadab` | 0 |
| discovery/client/signer.go | 2108 | `4797cb5adf643d913d98f4b6e2668fca3b10b6a45f3d2a5f1aa36aa04ba3a3aa` | 0 |
| discovery/cmd/cmd.go | 3320 | `59d72c2a0bacd32ab77a01f01116af68780fd73ebfdd72695a894e62f5d6442a` | 0 |
| discovery/cmd/config.go | 2055 | `3a19dc582bdc98f106c7024dab4966e826a0aaf058790f99b419d22680e09a45` | 0 |
| discovery/cmd/endorsers.go | 7132 | `a834d2c755ec1393e02ce5d64ac2a79bfb2b4d1a4ebfcbd171d77ff6f9b5cea1` | 0 |
| discovery/cmd/peers.go | 4310 | `78ff43fef62ab8f86d27a4890b864ac7fbd38827894ec9f9bd4d91fc4b6bef3a` | 0 |
| discovery/cmd/stub.go | 3613 | `45bf3c02965ffa2b06b107a780da50f1a8ce8418c11927cd4fe5870240bb122f` | 0 |
| discovery/endorsement/collection.go | 3631 | `e405fff150b011c83dfb553a24babe4c024f33a4a934993bfc395978f214c17e` | 0 |
| discovery/endorsement/endorsement.go | 25763 | `42ed3fb6a84960feeee350a02cd52b036b960de7928d3826bf30f9ac3b2dd681` | 0 |
| discovery/protoext/querytype.go | 780 | `058e0ec8e700c28503728b12d9cc35e343e2ce3de6c0323a492b42e0b5536784` | 0 |
| discovery/protoext/response.go | 1026 | `f7ce8d3c7b4c20d07e68820a25bc41f48e275e8f0d97740838eba072992d661b` | 0 |
| discovery/protoext/signedreq.go | 554 | `40e3b3e2474ac7eb2e98941200c4ee284fbb9f846cb3c985014fefcf019035db` | 0 |
| discovery/service.go | 9756 | `ca328f5a418a218a4bd6c029a00e28e330d9c2c89849f12b388b57b98a207a38` | 0 |
| discovery/support/acl/support.go | 5053 | `b43bfb4d062c6e77c1f9996bb779321da90668abde88e799e3ec3b8c35fb8ea9` | 0 |
| discovery/support/chaincode/support.go | 3596 | `dcbf67719deb032313064a328d509b941f59872f70c6ab7f83965609793358b2` | 0 |
| discovery/support/config/support.go | 8520 | `b4b86032c225ac965cb6cc18b01b84b49856cae256575a3f548b9e1038285f6f` | 0 |
| discovery/support/gossip/support.go | 2765 | `a8152929c569a86753efeda538c1768533f3c377a3610204ec49a5931f53e8f8` | 0 |
| discovery/support/support.go | 3015 | `22d2db8f2ce6c5f7bf2fe5183a454b3b2b16ed5e83293451ba8671954ded7e1b` | 0 |
| docs/requirements.txt | 815 | `a38d70b7cdc8de8fd432b12cd302fa341b91e3586ad789aa1d9a96c2c86971f2` | 0 |
| docs/source/cc_service.md | 14783 | `6acb92fde03c38e33997b79ed77e51464a532dd80f024d06ee72c3bb69d43257` | 0 |
| docs/source/commands/peerchaincode.md | 12168 | `36ed0eee09c21cd5fcffd7ef1a44974b7de8da226f03baa912b87e6252de2982` | 0 |
| docs/source/conf.py | 4068 | `77437e6a2d3f71386508ec078cfce9d4da7f8c4683717208b5dd27fa6aacfa27` | 0 |
| docs/source/discovery-cli.md | 41757 | `edcd8ac48a48a69ae4f871914ce5177af984f892a60b37baa614b024af376869` | 0 |
| docs/source/requirements.txt | 26 | `d32adf438ebe013e6f68f4ffc70072045da39d4306b16e6a8a4e47e35766618c` | 0 |
| docs/wrappers/peer_chaincode_postscript.md | 4589 | `e74548d0cfeadd6035590a9272871310d34dbc22a2c9b958c99a6bc6cdd2f94f` | 0 |
| go.mod | 5126 | `d115e2c102d45e7be8aef0b6d55ec69f4628d953af6c814dc080721041115963` | 0 |
| gossip/api/channel.go | 1816 | `09f299f1ed15c3b88e082cb493f7f39f09d1b7b7d5f4840cd1d26c4f28b490d0` | 0 |
| gossip/api/crypto.go | 6064 | `99ce2f3bb15dd2aa77c5a7c35dc226cda277973829de28d390f8cdc3777fc786` | 0 |
| gossip/api/subchannel.go | 898 | `a3cac7abd1595757bbd68a68eba6d7d17a35e6f9cb77c3d7de98bf5527fe2d78` | 0 |
| gossip/comm/ack.go | 1717 | `18d17eb96d5334e1c6840741309eb8203b02f9300da874fefbf554762468d318` | 0 |
| gossip/comm/comm.go | 3304 | `84a20a40557c6b63477597f65560e9db8b367fed41012907d3633ac50d5c0f91` | 0 |
| gossip/comm/comm_impl.go | 19385 | `3a0140ce7f45ccacda12946e573a6f6f2bf3a4f2d860f559e427e1ab81bc3427` | 0 |
| gossip/comm/conn.go | 9122 | `f6954caadf83701e30faf4fb75b6864583e33b2d942ebe64a62d8e66cbe53a8d` | 0 |
| gossip/comm/crypto.go | 885 | `b1ae2879453c92dbd27eb78909f6b7014c3350626c7cd45597e01cf4428d2ce2` | 0 |
| gossip/comm/demux.go | 2854 | `47ed43709cf5ba4116a8cafcbee73927d30969cff4d58160d9d750e2b0307d46` | 0 |
| gossip/comm/msg.go | 1663 | `a131682c3b5dbfcad688800374b83cc3809b307afabd1059a95bcb4aed231f1b` | 0 |
| gossip/common/cert.go | 383 | `6584474984f30581baf43582694a4a14cf2088edcf60e5af06e125235260786b` | 0 |
| gossip/common/common.go | 1930 | `136f3aadc7ba5ce2cdf13393d3ded9db306052026c89eee265ec6ec22782dee1` | 0 |
| gossip/discovery/discovery.go | 6873 | `21cfc6a93424da12960c4e716ea62e86247a8384a2e456a9023f239bbb2f291b` | 0 |
| gossip/discovery/discovery_impl.go | 32445 | `a8609024945fe530d49f727e354d197d4a15d08a458af037dc75a0b412eeee81` | 0 |
| gossip/election/adapter.go | 4261 | `99ff485f41c229f5a40d695547857a551a4f34c3a7ef1b22c3268006f504d9ae` | 0 |
| gossip/election/election.go | 12067 | `a37067a439f301f3b13b993836af68e70a406451351f4a18caf171a93741ffbf` | 0 |
| gossip/filter/filter.go | 2327 | `39f152a2d72ec697d39b61a91f9864a7161808a69efb75ed4a87f584b247dcf1` | 0 |
| gossip/gossip/algo/pull.go | 9273 | `4c7f6878e506e3d7b740a1d8dac38d1b8ecdaad8ad0d02d7e5e4a10bc03bbc92` | 0 |
| gossip/gossip/batcher.go | 2985 | `1af9ccc6b78df73b8241476c96928ccf36b862aaf2027f0638f5666961d4d754` | 0 |
| gossip/gossip/certstore.go | 4313 | `fefde0aa3ab6af358d3b25ab72ab2e572959219b8064fb006f344f8bfb267392` | 0 |
| gossip/gossip/channel/channel.go | 37299 | `2c226074a3996c9fbb3a05bb79c3b9e6837d3ea8b770a7bf8a900a9144eddea2` | 0 |
| gossip/gossip/chanstate.go | 6027 | `594f555d6297009f2f5fd4d3011344e52613f31dbdcda343bced402046b20b6a` | 0 |
| gossip/gossip/config.go | 7060 | `36cda88b76f5e35a42a5bf1ed75efff06f1afc080800b76e66077d53f20a4b40` | 0 |
| gossip/gossip/gossip.go | 1392 | `7e9a5f1fdf7eabc3fe84f23c48919134422cb832d6c442a4b3498f0480b66203` | 0 |
| gossip/gossip/gossip_impl.go | 44911 | `361aa6c8e556c6e9bbd13c216aee7b1390345b7abcabe6b1ec2394d4f81e9dcd` | 0 |
| gossip/gossip/msgstore/msgs.go | 6463 | `dfb2510e11ca6a908438a2b18369407b81a91f6b84615231ebe5277937cff471` | 0 |
| gossip/gossip/pull/pullstore.go | 13056 | `569ed95edf7f9081aedb2d597b9ac2efc122c8b929985a6a4ea65cf56532229b` | 0 |
| gossip/identity/identity.go | 8556 | `77888f825e5d43fdc18728691a64c2d1f71a27a6d78f57aa5ed9f1e654a97188` | 0 |
| gossip/metrics/metrics.go | 8127 | `ac3ca14ca2f2cc43e14c7af70555ed996ac4a931fb1655a80369b8802dd9ad86` | 0 |
| gossip/privdata/common/common.go | 818 | `5aacd6471f0b669d280821a3f3632a386eb8e1b0509165eb5264395df3bc59ad` | 0 |
| gossip/privdata/config.go | 3719 | `ed5370760fd7440c1ca7bf12cf02acefa75769c214cbbd02e9635bc385bc08b8` | 0 |
| gossip/privdata/coordinator.go | 18256 | `ac0877b5073ad6696cf8119ff2eff40e9290bc2b9a84c1de197040a7e12cba1f` | 0 |
| gossip/privdata/dataretriever.go | 10107 | `fe8684b58a6c22ae2dbfc9079ae210f60b507ca492a3c3b5b947fcef6047da81` | 0 |
| gossip/privdata/distributor.go | 17350 | `a49eebbdbe91601be24588a9e1afd0bbb6d2938b5eb1d32064e4c51ff01e5f5a` | 0 |
| gossip/privdata/pull.go | 24658 | `5bb3d5411534ef2fe4299ecd5519738797ac7e9579069a839e700a6a83db9f5d` | 0 |
| gossip/privdata/pvtdataprovider.go | 24434 | `b7b2c4744af8a163a2266d28abe8dd7d2eaf0e4114e349eff808ba1f9da62727` | 0 |
| gossip/privdata/reconcile.go | 12291 | `b0d32db7f7daf9db18bf2714455151d38d96fe414bfb74185774825cc71a606b` | 0 |
| gossip/privdata/util.go | 8558 | `3c14c7ee595b5f1de44f59efc580d4a9ea7e8c73215eeb67eba15b675140aabd` | 0 |
| gossip/protoext/message.go | 6112 | `13496633561c85743b1886e1c436acf1614329a998e2b90bbe4a89c3e6ebc316` | 0 |
| gossip/protoext/msgcomparator.go | 4169 | `733cd6f57a3e47e3fc30127119d99b122aa8b090d852b7ebbb4b03de3bd2274f` | 0 |
| gossip/protoext/receivedmessage.go | 1857 | `80104d629c6a2d8cb45e115972e93c8a84434b483bebd31258708058b7fa2c37` | 0 |
| gossip/protoext/signing.go | 6590 | `296899d8691285bb8e085e1f7f21e05882e9f2ebde264d8db6129cc67a053c18` | 0 |
| gossip/protoext/stringers.go | 4690 | `e0eacc50b7e41e5b09ccee44cd953c0eb3a4540821e810ff3177388d17e644fd` | 0 |
| gossip/service/config.go | 4601 | `8cce2f74bb077d84be9e97a82322f073656013395b79fb7e4f7da34ed9778772` | 0 |
| gossip/service/eventer.go | 3720 | `a772f52f4ce59dc891342d5e00249705d6a00156edf31b486e9c6515e32665ed` | 0 |
| gossip/service/gossip_service.go | 20930 | `71a3144b61956fd5c121dd554493c347e4c8c097ef5c67f932f73015a42c9870` | 0 |
| gossip/state/config.go | 2285 | `89fc5200329f287687b63f0dba8a6e20c2086455266dca05c0443695e6759e9d` | 0 |
| gossip/state/payloads_buffer.go | 4237 | `d137386e9606828636503473af5c6afb76b3fd2c36f10cf28c3006437822e20e` | 0 |
| gossip/state/state.go | 29153 | `40a1a2712d96dea7165d5c3cf81ebd87b8357d759509baf52cd67cf6d8ab7e39` | 0 |
| gossip/util/grpc.go | 2353 | `c5c152862f007253c0dd8f5951ca0f9fa04150eefd55bc2ed7c7c773863c64e4` | 0 |
| gossip/util/logging.go | 1995 | `e51543b236e114ddb7dd09f1264642a0e7c58c0eb6cd2b5920384b9a7e7e4472` | 0 |
| gossip/util/misc.go | 3982 | `aaf15514f2cc1318c73851a418b10b23e0620f9a535abe640757b4b47ce7dbb0` | 0 |
| gossip/util/msgs.go | 1664 | `abf0e66c80e0cddb6ac8f466876d28fb8ee26047fbe0a4c55103f93ffdbfb0be` | 0 |
| gossip/util/privdata.go | 3080 | `ec9655a618a497e8b5f969a801e5c2a14e18e6f5975819a758ba51526cc7e2a8` | 0 |
| gossip/util/pubsub.go | 2707 | `d4785ff2b99317bc104c8ffa01a4a5f559f1af10aba4c223a7d183305ba2811d` | 0 |
| integration/chaincode/keylevelep/chaincode.go | 7613 | `cfbcf74d69e8fdcfef17459a1d1ded73e213545127114b1c568762d7ba12420b` | 0 |
| integration/chaincode/keylevelep/cmd/main.go | 401 | `624d2b008129f73e3c7871e48bb4361877735cf38d5ac2c61fb26c41f4fceff1` | 0 |
| integration/chaincode/kvexecutor/chaincode.go | 3658 | `966a2eb95706849a5cbc73e9a1891c6028e1b45aa2511a98f245da0abb303554` | 0 |
| integration/chaincode/kvexecutor/cmd/main.go | 401 | `f9bbd83de7787da27c297fdabd2f00bb7ef289ec4b807dd0f7aa54d8e1fe351d` | 0 |
| integration/chaincode/marbles/cmd/main.go | 407 | `57345975b0dbc75e04b5028e12bc172dbb06087199a38b4f08c9d61f665157d9` | 0 |
| integration/chaincode/marbles/cmdwithindexspec/main.go | 407 | `57345975b0dbc75e04b5028e12bc172dbb06087199a38b4f08c9d61f665157d9` | 0 |
| integration/chaincode/marbles/cmdwithindexspecs/main.go | 407 | `57345975b0dbc75e04b5028e12bc172dbb06087199a38b4f08c9d61f665157d9` | 0 |
| integration/chaincode/marbles/marbles_chaincode.go | 30349 | `b2261ea7b59d856d089281b874aed9412c2890f932c05297036f94e013c82472` | 0 |
| integration/chaincode/marbles_private/chaincode.go | 23340 | `cca54d8e381487f0a6ad52e03299d000af849455ee470aa5150e06b7a953ad7b` | 0 |
| integration/chaincode/marbles_private/cmd/main.go | 424 | `1b08cd608daa1b97e17cd6dd93f3a1cac2b03f4e999a0c10d2ddf275bd81cd5d` | 0 |
| integration/chaincode/module/go.mod | 485 | `dc208dd0ea37bec23ab37f6ebfc9a97fbcd0e61cac9308df1e6a8425480df0ae` | 0 |
| integration/chaincode/module/main.go | 5213 | `d1d562d8496966779a199bafe0e0607a7e568fa66359cfeac777eef879d75eed` | 0 |
| integration/chaincode/multi/chaincode.go | 3722 | `f147e3d83cc786ce5eb296a6ed4fc10a328f66ca9e65353531361a93e05525ff` | 0 |
| integration/chaincode/multi/cmd/main.go | 388 | `5399768ebb297610ad65e69d4cab6e4204ff949cc1b47f02c938f56cfeb993d2` | 0 |
| integration/chaincode/server/main.go | 1453 | `ab8166de89f695b5a1410547a0f61edfd4fd0665fade7983055716dbf9d473ca` | 0 |
| integration/chaincode/simple/chaincode.go | 6972 | `4a42576a2c1d09ad0b8731b0343de404738bb1630d9c461fcb0a2d7cee4b8326` | 0 |
| integration/chaincode/simple/cmd/main.go | 1514 | `182dc80c481a54d578feab534a6174e49bf00722b8dc589984561b64fbd49ecd` | 0 |
| integration/configtx/host_port.go | 1097 | `6aebdc83093de1ecf8b2fc53ab5b80717a388a383842e38c6c6e7181ae54f80f` | 0 |
| integration/lifecycle/chaincode/callee/chaincode.go | 954 | `560025f9fc61a8c3494e54559f9380d73e50f522b5fd54b9c42a1819f525945d` | 0 |
| integration/lifecycle/chaincode/callee/cmd/main.go | 395 | `0fe9b586b3987cd7066f0c1a7dd94ab210030283c59864af25cc9799a340d254` | 0 |
| integration/lifecycle/chaincode/caller/chaincode.go | 1233 | `e8d8a060ba643eddb20bb61dea87321e091ef6a2920a7f5eda08693375e5c515` | 0 |
| integration/lifecycle/chaincode/caller/cmd/main.go | 395 | `b83445cae8132959a90fbaeabd7ab68aa65cc40cf060f45183156bc02440bb33` | 0 |
| integration/nwo/buildserver.go | 2072 | `da1becf24e36ad39362ef7c801c4545017041fa973a143bea739b964e87368bd` | 0 |
| integration/nwo/channel_participation.go | 12607 | `cd8145426c8a234cf37604db682623aafbed4d752f8695582bf74154c7bddace` | 0 |
| integration/nwo/command.go | 586 | `0ad1786f2aa2ce56aa77788562db94cb639ca15f9e7a761a49f4bfc9eddb1791` | 0 |
| integration/nwo/commands/configtxgen.go | 1307 | `f46b2da4f29a0c739f00bbce4910b4c7cd1de3d66ba8bd6a1f707a28f728ae23` | 0 |
| integration/nwo/commands/cryptogen.go | 592 | `f6037f36f511be5b2b3373f4364ba6d03d43be147d891dabc1b5c5b4622aff06` | 0 |
| integration/nwo/commands/discover.go | 2416 | `5bd2b6eacd187bdcca5a5d0edce6d7c3e8452575f146adb7a63a118374d356c6` | 0 |
| integration/nwo/commands/idemixgen.go | 793 | `65e87780f163f856f9f61efcedfd994b6bb75a0732c74a3b3d385fda87da6dbc` | 0 |
| integration/nwo/commands/peer.go | 14805 | `5fed9880e25147a834a68be4918a4bef5ccb2a5e4747704d2eb30139383f7848` | 0 |
| integration/nwo/components.go | 1778 | `a5ee9a75fc4b58539ceadc8e0d8c0afa96ba64e3adfe56fd02aea610f3600e86` | 0 |
| integration/nwo/config.go | 841 | `136da67e9c161a9267b8c86c90c40559ffb4dd293fed49f970864c59731cf7a5` | 0 |
| integration/nwo/configblock.go | 14734 | `eef318bca10e09b4c1a8616da85448cb42fb598b9c3c307e7289dfbe7064abe8` | 0 |
| integration/nwo/deploy.go | 20910 | `78725b6875a72131d6728fa84c07b90d6c4a99b4dc39d6b8ad4bad64f2203d95` | 0 |
| integration/nwo/discover.go | 1621 | `33b0749eee4e608d5beae275ce355235fb6972579dc21ae61e899e61f399dee8` | 0 |
| integration/nwo/fabricconfig/configtx.go | 4546 | `cf103d06cb48ae6b63112e86332480d092849633896e5b7270f335947d9dbb82` | 0 |
| integration/nwo/fabricconfig/core.go | 14177 | `c78a2dbbcab139d19feec2fe3a84d0b2f2fd04931e387758f90b09da50deae42` | 0 |
| integration/nwo/fabricconfig/orderer.go | 6383 | `8e7f82decb4962c19328d896322136b7cbea66580c3e30f97529b5ac071add95` | 0 |
| integration/nwo/network.go | 63715 | `5e92bc876b553bb797238468dec5d3abc215f627856744af83812714b70d79a0` | 0 |
| integration/nwo/operational_client.go | 2041 | `7c13843645e7261a9f294d78c0ecdf8e9e02f6efa2e5879b74f58ea5137f5d45` | 0 |
| integration/nwo/package.go | 2496 | `8c897e08dd0a6e67e59c0e9e67bcb2f3bb3a29b80852364bc426f60e69ad9d3b` | 0 |
| integration/nwo/runner/couchdb.go | 7204 | `b900d155a14875edecde8250454303b18fe3d8e073ae5197c563ad67bc23d873` | 0 |
| integration/nwo/runner/defaults.go | 714 | `0f8dffe86ff47ead837002912ae652b03621e3ab3a7b0a4a9f63ece6fe3b3376` | 0 |
| integration/nwo/signingid.go | 1841 | `5fc4f91644273dee98c763ff9dc5c2d0094f55f7b84049f60e45d26aa7079f8a` | 0 |
| integration/nwo/standard_networks.go | 7247 | `533efa34b01d5587be852d3ada6922d9d3a803d057b9ae0f036febc14ea0093f` | 0 |
| integration/nwo/template/configtx_template.go | 7480 | `b5bdd6a01f7fe7e473eb7297e3546aba1c3fe9f98fda95c440e345e6ce79d8c8` | 0 |
| integration/nwo/template/core_template.go | 6408 | `6430499bedc52d815c77e9390c22e3b3f1e6eb4f747b6837dac632284e6a16c7` | 0 |
| integration/nwo/template/crypto_template.go | 1485 | `ad970635df4fb02644150412926d5f17fec6fa59dd7b8fe7501e5423451f6df3` | 0 |
| integration/nwo/template/orderer_template.go | 3362 | `e67c0380640444b1f1c0ace200fb589c0a818e7e5f0e81b2a8c4e46c5115f725` | 0 |
| integration/nwo/templates.go | 930 | `cfe7d1880b73fcbeb6f0a9ea63163636d7cec756cfec0520a425d70254d96805` | 0 |
| integration/ordererclient/envelope_creator.go | 983 | `c6a7c3430ca913e61af2fcac1708726558311195fdc0646cfc3c6b78f4c3e417` | 0 |
| integration/ordererclient/orderer_client.go | 1773 | `e6ee9069fd1bc03018acf959b0c6d13f294d18b9e900fa0327f3b527cc2ff781` | 0 |
| integration/pkcs11/p11key.go | 1495 | `239a42d597cab9a1ffb2704dcfb5325c346efe1f41ed16573d27c528be46cb26` | 0 |
| integration/pluggable/plugin_activation.go | 2738 | `48a73986a5eb7ebdd6bbd6af9ffb0258ab35565b1673a6121064c3f8c5de9859` | 0 |
| integration/ports.go | 1300 | `9324ce74aaf10dcb135d02a35b1c5d74b2fffa7ab98fe55cf1ad24870bd7a5bf` | 0 |
| integration/pvtdata/marblechaincodeutil/testutil.go | 13583 | `12907be54928a15276eba76c2b460f20f97dc60b6f1aa5de92e41ec0be1716d8` | 0 |
| integration/raft/client.go | 1710 | `aa3a2ee68324cbe5b6d85ead98818fe99522c80e6915f29f8ae394713b8332a0` | 0 |
| integration/raft/util.go | 1352 | `6fe0ac7dda1d3a840109154b16924297013f5df3a293c2c1e48dfaa94238fbde` | 0 |
| integration/smartbft/mock_orderer.go | 8320 | `3f4d11ccd4b8da0ff48386a3d1702366d825f25eb76ad621d651a8d2e8d055c6` | 0 |
| internal/ccmetadata/validators.go | 8633 | `e958dc6feac97e6b033fe46e0c406e5fc575fc9c9e5a1d33b5a7ea5bf4ec9bc3` | 0 |
| internal/configtxgen/encoder/encoder.go | 27903 | `5d4f3b8fa8c1d609365f3ed239115f2dbb0a1c5eb162523d5ac5c0b4adbde957` | 0 |
| internal/configtxgen/encoder/fakes/signer_serializer.go | 4813 | `c2d58aa361d57ae3152228f14f524e963fb1d651f1e3de168ed546153fe7bf74` | 0 |
| internal/configtxgen/genesisconfig/config.go | 19499 | `506deefbd9fa041990bf8d5af4a244f4cc26d1684cdb28b5a10fa517ba4bb62f` | 0 |
| internal/configtxgen/metadata/metadata.go | 509 | `e89c2fe37d1fa5f2e6eede472b2dba6c08ad5030e0df632efeade257d1e3d6c1` | 0 |
| internal/configtxlator/metadata/metadata.go | 533 | `16173bc73a9e3bd109b8551ae8d16a6021f7dd707eb9f271ac296242aeb97161` | 0 |
| internal/configtxlator/rest/configtxlator_handlers.go | 1871 | `498e6f0f9c63d04cb83c97be7b98c6287e98c598cd229f4af9349cd766297451` | 0 |
| internal/configtxlator/rest/protolator_handlers.go | 2137 | `acf5bf21cf2c6b41d9615e9a66d34ff6e36f81e6fc04928aef252e984b984fa1` | 0 |
| internal/configtxlator/rest/router.go | 512 | `c3c509b3f7fcdc82935b2c7c056fbf4a4a5df86ba0f115fb42b2b3e70716b524` | 0 |
| internal/configtxlator/update/update.go | 7301 | `16d5042cae703b831acb02282e6a3dbd5747d4dd10a402f817a197c28c2ee476` | 0 |
| internal/cryptogen/ca/ca.go | 7379 | `9c4a52420badd786f188cad199eea405aff611bca991af3a4567be070d4e62e7` | 0 |
| internal/cryptogen/csp/csp.go | 4718 | `5c9ce9a5c042bf0b17e2ead9d464a61a485c280ca7157e9c041a9f1dae33e417` | 0 |
| internal/cryptogen/metadata/metadata.go | 529 | `4b9ffd9679924a78f56c542d1cbc488ac4a88f3fd2933c0107beda8ebe517124` | 0 |
| internal/cryptogen/msp/msp.go | 7530 | `520e9f341cf43d3e79dc543337cda8017370cb5b2f4481e8856808f2cbc3a435` | 0 |
| internal/fileutil/fileutil.go | 4164 | `1d00e3df252abda9cd2870efb08862248d59be71207a5b33fec8edc37cca7361` | 0 |
| internal/fileutil/syncdir.go | 592 | `7bfcc9c9826fdf9c5f53927d5c74187f158079017a4432e185db472970ed7286` | 0 |
| internal/fileutil/syncdir_windows.go | 191 | `3ebb8223ce5eb0482038f8d48f02e184b5272ba9eff4973c1af423f678fdf812` | 0 |
| internal/ledgerutil/compare/compare.go | 19571 | `27af55bdfa5aed4fedd0fcf609190be9dc9527497f23526fb7afc3f5bfb80446` | 0 |
| internal/ledgerutil/identifytxs/identifytxs.go | 15279 | `b47eb3979768297c69c3e3f5a2117a5f7393d522365d2aecc6fd948bdb18353d` | 0 |
| internal/ledgerutil/jsonrw/json_read_write.go | 4105 | `a38ab16abcfbe23489904fb2d74383ca6158a4a961c2edfd672454021e65e1ea` | 0 |
| internal/ledgerutil/models/diffrecord.go | 1568 | `faa74d01eba889371f391adad30d4cd8e4bdb607dd3441b80729e3743a3252b8` | 0 |
| internal/ledgerutil/verify/verify.go | 7329 | `629a4665fae80eecdb193695ff060438f5b03f54de2662811dba6e39d2866617` | 0 |
| internal/osnadmin/fetch.go | 526 | `bd1a2ddac848816df8f00de97bd1d1b2c6207947e2acc7bfc3138e20f46fa764` | 0 |
| internal/osnadmin/httpclient.go | 1403 | `94810bc4831afd18c55e7d4e4effcb6a0d1350d339fe8fac070d2c275d2c3e91` | 0 |
| internal/osnadmin/join.go | 1063 | `d55ba273799d76a7db279d3ca47c181114ec64a3deb322cd44fe5313d3792d14` | 0 |
| internal/osnadmin/list.go | 733 | `6a8e2bafbac32072e4c02dfe1762074df3a6ef3fc12bf279d4c09261287175dc` | 0 |
| internal/osnadmin/remove.go | 550 | `b967f0b6e966186db9d0a4162e4265a6d81ff3525e1d9c5f5a793468b1cb8346` | 0 |
| internal/osnadmin/update.go | 1145 | `5492e6662e8ad2cd86cf2afbed103b15f635184588d79e9f92a1bc1f531f003d` | 0 |
| internal/peer/chaincode/chaincode.go | 4099 | `3a51234e6db0f01b214846c6e9820ed52895a6852a891988e05f8f429cfa97d3` | 0 |
| internal/peer/chaincode/common.go | 25589 | `5cc084da2177e7cc6f43df3044c1d98184c07c762c92cfe290a2accf23f451fe` | 0 |
| internal/peer/chaincode/invoke.go | 1597 | `bbeaad9b5dcb4d1437024f071b3c564220851ebf4c1a4cad25ca4297117744cd` | 0 |
| internal/peer/chaincode/query.go | 1816 | `7aaabd0469fab4c71539e09ad1097fefd4fd27860ae004492f63661228ebc513` | 0 |
| internal/peer/channel/channel.go | 6042 | `10e65d35ff3ba163ea5119c952ab07651bd1c87ce5c13fee2ab0aecf1fbda98a` | 0 |
| internal/peer/channel/create.go | 6287 | `06339f25ccb99626c89fdc673cd04cf8b4757b14150a5223614405b4d28606e6` | 0 |
| internal/peer/channel/fetch.go | 2716 | `1637d5040a47558348d09fe451dcb62d8c2242d6006aab8afe3adab5b90d1dc7` | 0 |
| internal/peer/channel/getinfo.go | 3181 | `4ad9614c36e42cb64533ac229e01cdef0261c0a85870534f4d0b40968bebd370` | 0 |
| internal/peer/channel/join.go | 3702 | `f7f5e61df91924833a36ce4abe9ef950b9066f7083f1a475b252911979ad63b3` | 0 |
| internal/peer/channel/joinbysnapshot.go | 1803 | `a7dc261616428b3532be8042ca339e59ce0e31f30944d354018c5dfca7bdf246` | 0 |
| internal/peer/channel/joinbysnapshotstatus.go | 3120 | `4a24d754ce69c9f129d4f1c49bec93017bc68aa77b6c6fed4ef6fbc82496ec48` | 0 |
| internal/peer/channel/list.go | 2973 | `29ae355ed1995897d90d96c29dac2c0c5e440061a45dfdabef4ae20aa037bbb6` | 0 |
| internal/peer/channel/signconfigtx.go | 1459 | `8646248a7aa502d665bd244ef1306c92627821b56c6e31448d7fa2a990ddc3c8` | 0 |
| internal/peer/channel/update.go | 1914 | `02cbc6cc2c5d1e95e627bcec171657869a658133bda1e2a96fa262dafbe36782` | 0 |
| internal/peer/common/broadcastclient.go | 1273 | `d8d7b9845815c92fbde751969291d9b3ffb313fdc4abc5a8a030dbef1fd16790` | 0 |
| internal/peer/common/common.go | 14261 | `e52c8ac13154f83ca4acd05c71051ad57934f781e569ecab6ffc8e276bf67e2b` | 0 |
| internal/peer/common/deliverclient.go | 6567 | `4c75a772462cb82583b8904486bec47bf0ba9f24727bfe658864c86c7c79b3bf` | 0 |
| internal/peer/common/mockclient.go | 1134 | `c732c47dd418b6c4581f5951088cbc7c226d5984ce639aa7e2f7c11f9def8d1d` | 0 |
| internal/peer/common/networkconfig.go | 5573 | `da23d542a895badff57913b7b27c092fed0c3a5775e617d8e810aa367372466c` | 0 |
| internal/peer/common/ordererclient.go | 3342 | `8fc576488d58f68ef63e0a833e115cb63d91dbf5f77af3a995358398bdf997d0` | 0 |
| internal/peer/common/ordererenv.go | 3032 | `e260500adcef3ca8c73cfb3b5772dbc92e89ba3e5118e353e9831c10be32c649` | 0 |
| internal/peer/common/peerclient.go | 6980 | `e913d9c208fa60a52e9580df714ee9159f095ceb9013cb922d8e49f3945ef483` | 0 |
| internal/peer/gossip/deserializer.go | 1746 | `ace7789f54cffbe4915fd213b28b9f0a8a9531757a34e13b38cbc787164a3573` | 0 |
| internal/peer/gossip/mcs.go | 13924 | `d41bc050d57bf35362cf43052df52689e7a530348f0a1a5b128f85f4933b5fed` | 0 |
| internal/peer/gossip/sa.go | 2666 | `459c64221b6a8cddae22a30b225d88af01c710d3dfc19b79e9293d26db751c5b` | 0 |
| internal/peer/lifecycle/chaincode/approveformyorg.go | 9811 | `cb4bbdcd27dc6d3c3b036e20f4bc334178f8869a307a4665a216f4272729762e` | 0 |
| internal/peer/lifecycle/chaincode/calculatepackageid.go | 3466 | `f0e38c65ba1334f5fac195e2e52f685c1b5aea7a3231afd0877c01f7e64a5d0d` | 0 |
| internal/peer/lifecycle/chaincode/chaincode.go | 6582 | `7fa3bedd6b6e2c74a6209d38c40b0986e535e382a5cd35e4e0792c5f8f94e7a1` | 0 |
| internal/peer/lifecycle/chaincode/checkcommitreadiness.go | 10724 | `7e67eb9b1ad4751ee154d657fcf3cc5d910c8c504192e4d0727949b39c3ec1cf` | 0 |
| internal/peer/lifecycle/chaincode/client_connections.go | 6698 | `f8b0306a2c7f60a522176ec04043aedd2e3cefa4c1a6a1da55208d20fb94121e` | 0 |
| internal/peer/lifecycle/chaincode/commit.go | 9008 | `4607c2b05c306d558e16f7af2af6d2d62ac99b75f0199c80adcba81f7228f0ea` | 0 |
| internal/peer/lifecycle/chaincode/common.go | 4071 | `d402cade8f80cc7f19df10fc8aa9cb335e7843fc703cebdbb294de4219ad1cb1` | 0 |
| internal/peer/lifecycle/chaincode/getinstalledpackage.go | 6032 | `6df84aae154ebb0ef1abf2acb653deb9e62085d452309d685453baac8efbe58b` | 0 |
| internal/peer/lifecycle/chaincode/install.go | 5847 | `c64b3f704faa2f7edbcc9c86258f27ad231aed25189d6adff10adaa21415eea1` | 0 |
| internal/peer/lifecycle/chaincode/package.go | 5771 | `c83d4940443afc75eaefc9869836b8c20b2b9565720eb46f66515a3c68e17687` | 0 |
| internal/peer/lifecycle/chaincode/queryapproved.go | 7851 | `d2406eb9d0bd988b2b7bf407c9a1d869bbfcfc2b8490bc37fce32993ba9f0965` | 0 |
| internal/peer/lifecycle/chaincode/querycommitted.go | 7571 | `0a2a015f95261b26bf3ceae777f9fc8f6b692dd18fcdb945497114b75c069543` | 0 |
| internal/peer/lifecycle/chaincode/queryinstalled.go | 5219 | `eb85b9c2b5b2a0957bcc85d6efda570a702bd9b063e2b3e6c6e8626c858b000d` | 0 |
| internal/peer/lifecycle/lifecycle.go | 578 | `7af14183eee09681f1c26ce0f5330278a0c2990ff6cb9c58937dec0024c93a95` | 0 |
| internal/peer/node/config.go | 4265 | `3caa3c29b303164eab67768f0f98e126d3d4ac0471b0751a46ae057e6d1f72f9` | 0 |
| internal/peer/node/grpc_limiters.go | 2828 | `131781ac076eab8483bdc775b603dfd8a29c92d6275e476de7e0e155ea404886` | 0 |
| internal/peer/node/node.go | 960 | `3111c26766ee99ef061331416a88a128799c98bd5610c28b649c05554c86126d` | 0 |
| internal/peer/node/pause.go | 1040 | `33bd7b932a78b924a5e79222b156b9ecb1cff4d8873b884034ba92226621220b` | 0 |
| internal/peer/node/rebuild_dbs.go | 730 | `3807b7ca7dde4d62010044eea700d13f9d07d7843368542293ae54951dc3f1c5` | 0 |
| internal/peer/node/reset.go | 887 | `3c792257406332375ecd122f6e043c94ea9527623c49a731427177fdccee3635` | 0 |
| internal/peer/node/resume.go | 1048 | `8852d20bb0c25865859917a2c62de4a2d0639c07cf198ab368b7d387d7275dd2` | 0 |
| internal/peer/node/rollback.go | 1466 | `4eccdc845d96a9d82eea061c908ef056c8ab4c062b1b4c06ee698914b4822f7a` | 0 |
| internal/peer/node/signals.go | 361 | `91a6d71024a42f85f234e07f93aa16c68ca54da59ef0d34718598a362741784c` | 0 |
| internal/peer/node/signals_windows.go | 226 | `b0734b09b10c5f21cafd3f2393ad72965e36e3f0429ef6cd1f640d0be9f3d738` | 0 |
| internal/peer/node/start.go | 51656 | `ac146f7e3b8ba11ee9c8046fc8b0de679ccdd67cc7f994e75f15401188f3c00e` | 0 |
| internal/peer/node/unjoin.go | 1783 | `49e931f276ac49c5b749570dc2d9b84b458941bded6aaef1dbc5cb2d69346759` | 0 |
| internal/peer/node/upgrade_dbs.go | 706 | `976951a1872194ce37c347fe34d3e96f3c3c692abc30c54443b3e2eff10c51c4` | 0 |
| internal/peer/packaging/platforms.go | 2571 | `291ccdbe91ec0efe03ab2aeff7ff50d80c6c12916bf4999d9e7280d43db4bb1b` | 0 |
| internal/peer/snapshot/cancelrequest.go | 2209 | `ea4280a03e670606d8a6ec213a7089277eb3eb8883d98b9d52dbc93ead3feb80` | 0 |
| internal/peer/snapshot/client.go | 1442 | `7f945a8dd48b141bbc1833f86f0638d82de23295add128bb1f6a3bb9dc210462` | 0 |
| internal/peer/snapshot/listpending.go | 2012 | `ec0e2608e1100917be113cccec8483410d2ac9be5b85b70bbc8ea55d81aa68bd` | 0 |
| internal/peer/snapshot/snapshot.go | 2933 | `058721f469d4cd23f6745ea7c04950fb8e6bcfdfd4524539d03502d6036ad4f5` | 0 |
| internal/peer/snapshot/submitrequest.go | 2187 | `ffb310fa33336f60825e1a9f66be48c2ad2b26b348314869a3d8cc92bb5c82a6` | 0 |
| internal/peer/version/version.go | 1241 | `cab547e85db0f3810274bf7da4514b2a446e45d02108df503cd5a6218dca0b61` | 0 |
| internal/pkg/comm/config.go | 11186 | `a73017af39652462f3ed6b9ffef374dd7a1665a5cd6073f95e5bbc414b7f5f61` | 0 |
| internal/pkg/comm/connection.go | 3920 | `3833ea9b046e7081e58cec8c952df1e8f15d712cec94bfabb5cb75cf29b599d5` | 0 |
| internal/pkg/comm/creds.go | 5037 | `e5abda69d010aa8a5e736c43ab494cb4adef062af763a76ed330a4cd76e0f0fe` | 0 |
| internal/pkg/comm/metrics.go | 816 | `bbb166b1efdbff5cb4052348869935686b2029027dbf08ab91a194820d877618` | 0 |
| internal/pkg/comm/server.go | 8534 | `faa07e3fc74dac6dfe38345a7e37b366ac94fd97bb5898c84e192f97c6240cd8` | 0 |
| internal/pkg/comm/serverstatshandler.go | 836 | `5bd8a7161d9dce8a1ac5996119584c937d3dc78a29a7e8e9bd8f61be0f9bc84b` | 0 |
| internal/pkg/comm/testpb/test.pb.go | 6735 | `37965ade3663520994fcc4efbabb709261c0cb94ffe22dd871b10d6d46a7b666` | 0 |
| internal/pkg/gateway/apiutils.go | 3681 | `958cec9889e75ef93722359ae65f44ccb2b6f5d5284c11ef8aa841732629bfc7` | 0 |
| internal/pkg/gateway/chaincodeevents.go | 4562 | `a4a8e0af12f2056ba56e0ec2646173f740d1721018d2eaf7c165197a7700cf18` | 0 |
| internal/pkg/gateway/commit/blocknotifier.go | 1519 | `b74efe9479c7d242a328b09b90a0a30caf344d5421ff9634978444126c0ddce1` | 0 |
| internal/pkg/gateway/commit/finder.go | 1958 | `3b60355c998faffdd8486b41f938b8372b6c74e7a4810040b81a85b5607277c1` | 0 |
| internal/pkg/gateway/commit/notifier.go | 2148 | `d9bc7423977d5f05f914e36feffe97dcdbedd897d7708153b4c871a3a50a837f` | 0 |
| internal/pkg/gateway/commit/statusnotifier.go | 3140 | `bc5c79f4a4f084879617f115813894e09e37ea6e6f948329f77a5a459ee1fdbb` | 0 |
| internal/pkg/gateway/commitstatus.go | 2385 | `7864141d78035e919303b71207f88ec9c93e55094f3dbcf428c9f6328dc94cd0` | 0 |
| internal/pkg/gateway/config/options.go | 1519 | `2e056e0a82dfb1baf93851cba0f9f8b43ec28ffcc6e1fc3c524aa1063b132bf3` | 0 |
| internal/pkg/gateway/diff.go | 11837 | `f021298c2af6b720ede43496dce947b532532ebb21fabd34d7440eb78d9a1360` | 0 |
| internal/pkg/gateway/endorse.go | 11261 | `ed8127925693c34c391505b64ab2487a9d9ed03c5c86d5dd3e84c8eea1f4ee0b` | 0 |
| internal/pkg/gateway/endorsement.go | 7375 | `3da03bc246faba9f6a0e0ba74e412d57ebf4e413f050dc2128a78bf22d383716` | 0 |
| internal/pkg/gateway/endpoint.go | 4004 | `56bd03e480ccf31eb2fe00e2a75ba655ce8e763cbbea6ab2581e591f1561c85c` | 0 |
| internal/pkg/gateway/evaluate.go | 6894 | `dc2e3ac4dd8eaf5a9081dfcf084bd552f13afb9148fb01a1634df016bc921e14` | 0 |
| internal/pkg/gateway/event/block.go | 2314 | `a81f36f088df27e87b494f43924736f5d9b0c566276435a2d5309d54a53790e5` | 0 |
| internal/pkg/gateway/event/blockiterator.go | 790 | `537ecb7ff32f2ab9492fd120533b6a6ee5bbc97b0eada54b710c6015584f71b2` | 0 |
| internal/pkg/gateway/event/chaincode.go | 692 | `76c9288588364240d815235c61b2561d62948eedc8c0091dbad7c893d7437cf1` | 0 |
| internal/pkg/gateway/event/chaincodeiterator.go | 1692 | `a1161be16294dfd77adaa4cdd96cd23e2644f4a823cc55ada229b2bdd25dfe45` | 0 |
| internal/pkg/gateway/event/transaction.go | 2390 | `af0ba034754ee41679ccc150db951ec8a676cf9c34c246d3a15ad077c3e3a8ac` | 0 |
| internal/pkg/gateway/gateway.go | 3885 | `eb9791bbfea21f3034acdf76994472e3a1c4f9d070bb8ba4e199f4068f261a27` | 0 |
| internal/pkg/gateway/ledger/peeradapter.go | 1438 | `a18253f0104328297d7d4ae34cea43dc71fd669d5089955188b9a8134d25cf4d` | 0 |
| internal/pkg/gateway/registry.go | 19009 | `66ba2b109ed76ed9cbc521766eddda6cab9cd9605c1f53044c16112ab138a7d5` | 0 |
| internal/pkg/gateway/submit.go | 9212 | `5891716d0c86a4d7098551685b606a44198a91dd9df6c25c1d8675b86a19c950` | 0 |
| internal/pkg/identity/identity.go | 815 | `7155c32b46678ec00a930770c1e6b5d405ddd7099f05f8e5c0447cd49e0e40f0` | 0 |
| internal/pkg/txflags/validation_flags.go | 1784 | `3b629ee7b652802b121e1c10d395b3c3dc68a432c00fd73cc162caa21136974d` | 0 |
| msp/cache/cache.go | 3386 | `9de15d9c11ce2ee7a23e8939fd36ac6627abe9f421e5e8ca02953a4f59b20d4e` | 0 |
| msp/cache/second_chance.go | 2670 | `07829311265de781e29008b7db3f14fc4ffb26efaf2652717c36188292fe3592` | 0 |
| msp/cert.go | 4400 | `109d3fecdcba4e48f02886aa9267348f622093a29fa7f85aff24e2bffc4f02ed` | 0 |
| msp/configbuilder.go | 14023 | `ee88a0458353a674c1c86031a31ffa2983e425baf8127c6ac51cd34574068c19` | 0 |
| msp/factory.go | 2007 | `e0889fbf44596cd7d367f88bca1962d35fd89c87e95b1f7e06578294983b719b` | 0 |
| msp/idemix.go | 2704 | `e1ad09cb2d26221d16bdc8d392211fc7450ee8c147e51554bd2639a75c3a81f1` | 0 |
| msp/identities.go | 9172 | `629cdbecc7cf2b42b7afec2a73442cc2578dd31a4161d27f0fb675ceea4ac7b8` | 0 |
| msp/mgmt/mgmt.go | 3407 | `a85b414755dad2e3d8363cf41caafd3abfb2b93453726d4c3c3aa260ce445223` | 0 |
| msp/mgmt/testtools/config.go | 807 | `ea6e526693b8c8ee13720edd84433ae1f9cf12a8e35cfa218ff4db5049ad971a` | 0 |
| msp/msp.go | 8041 | `2952be7c4bf15ee279b9da866b7d1d1d24290e12ed7434ce53aa7e3ad6696d5f` | 0 |
| msp/mspimpl.go | 34886 | `ae0665b7a62712ca09b7e5d889e0fdba2e68d974b9e6a6450db6abe53a3b1863` | 0 |
| msp/mspimplsetup.go | 20702 | `b055cf4785d3f7722ed46c1d1d8939173a7dcd924a46d123bec8b3dc6f25b82e` | 0 |
| msp/mspimplvalidate.go | 12874 | `230e43557a2c8a13c31c40ed3d6fec82b3ea4e53bed661817f96a198d66f01eb` | 0 |
| msp/mspmgrimpl.go | 3321 | `7f3fc017b1d3119e1923702157fbc958420b0549fb4330f192eb859ea809ab13` | 0 |
| orderer/common/blockcutter/blockcutter.go | 4829 | `5aba55795ef920fe0977c1899a4c5983c30521a8a3d4d8148e989243bc912e61` | 0 |
| orderer/common/blockcutter/metrics.go | 645 | `4ad21449430f33ef65aafe9a343d865827518ef05a56f3f4a76aae0d5ff7b92c` | 0 |
| orderer/common/broadcast/broadcast.go | 8073 | `47469f31fd05d8ca5ff4e43a2976b72def0b59c58ebfdd302bc41082fbea47f9` | 0 |
| orderer/common/broadcast/metrics.go | 1391 | `b1049452fc65e2d5c92744a274142e91c8e9366ad76a7bb6ae23e4a63a41e247` | 0 |
| orderer/common/channelparticipation/restapi.go | 25404 | `07d8825ebf4a06c5d073c27bd3d420b8728a57dbe88ce42b202ad1124e3f398e` | 0 |
| orderer/common/channelparticipation/validator.go | 4120 | `5fc8a43e20ba8c11ba1b28539a8e3ed2312018e4c33531c3e625326bd638ccec` | 0 |
| orderer/common/cluster/clusterservice.go | 9969 | `9189145c4a4d64ff8321d0c47f6725f85891fe666a6dedfc09649c8963744322` | 0 |
| orderer/common/cluster/comm.go | 11423 | `db7bd3d20a9dbb01a80d7942bafeca65eca5f215d7e68802c26b5f74b87852c5` | 0 |
| orderer/common/cluster/commauth.go | 9459 | `be7df60b02fb3bcac7db426099c9707dd39d16cb7ac2b60811f47401fba3ad70` | 0 |
| orderer/common/cluster/connections.go | 3976 | `7900296095ff15fcdceb783dc4ab5337ffaa330bd5544bfcb48c7a15a09fa74e` | 0 |
| orderer/common/cluster/connectionsmgr.go | 1928 | `823d40353b8703fcddf4747950e990fd33ca80d4941532969e3535a7ad501bdb` | 0 |
| orderer/common/cluster/deliver.go | 19653 | `16b124dbbb56d71c01425bf4542ef8667de92db352a9a16e173cee522a0360a9` | 0 |
| orderer/common/cluster/interfaces.go | 2641 | `2db95d917ce5f051f888efac619509514202b7b9e5cc60cb65d642bd4d107348` | 0 |
| orderer/common/cluster/metrics.go | 5077 | `84291cf0b3326e721bfbdced3674ccf61ef36175b4756c912a3edc397ea9ee41` | 0 |
| orderer/common/cluster/remotecontext.go | 4520 | `83926b89a6c3f75762d0c08609cbf4ce8cbb524f20a5094f447d163253e9e9b6` | 0 |
| orderer/common/cluster/rpc.go | 6453 | `0c9dd15f65ed7da4374772814af925e8e9dbda5d8ccaec1b5f4e24c148cb048d` | 0 |
| orderer/common/cluster/service.go | 4515 | `e1b356a72e414f9ff2c77296de072c19d51be096a2617a00731217f11495a3d9` | 0 |
| orderer/common/cluster/stream.go | 5607 | `7cd311272c61156244ff7bc6f068c1d2afc8e608aa008ba6aadee72f0005b5d3` | 0 |
| orderer/common/cluster/stub.go | 1496 | `bde2ee52d508959d15133e28812cfa38bb02bf3846d985289063a997e3fcdc04` | 0 |
| orderer/common/cluster/util.go | 26580 | `57ab1f4c61205f61d5d09396fafb6cee9e718d7732dc9f49e56dfc98d8825545` | 0 |
| orderer/common/filerepo/filerepo.go | 4470 | `c764bab5b75c4be107c26497e4dc8f10b37a5a4ffee0be2c5e72f6a7f89b80cc` | 0 |
| orderer/common/follower/block_puller.go | 7983 | `0f4b87ae44d513ba2845d6dc62996b7653e9b0fe3fb6ab88b8ced278f2f0f1b6` | 0 |
| orderer/common/follower/follower_chain.go | 22899 | `17862abae40438289802a0bc6b13f3d5dcd0864914a778ba1b0f80458fc2a7fa` | 0 |
| orderer/common/follower/options.go | 2069 | `c00dda071ea03f0fa32680477d6b78f734eb95d976092b7ac8432a74f10a11b2` | 0 |
| orderer/common/localconfig/config.go | 14666 | `326a3793ba57652be75cc7564c545deebd93ec81c6fbac6fd4936fe4abfeca4e` | 0 |
| orderer/common/localconfig/flatten.go | 1590 | `15c7b09b131220b34c75c5906b754552bc61a605ad09362f14151a7dcda7d814` | 0 |
| orderer/common/metadata/metadata.go | 499 | `dde0757e351939ea32469234be2d2a0b809237e44df3d56ffadea14df5133836` | 0 |
| orderer/common/msgprocessor/expiration.go | 1631 | `72df984d3109c0a069d525a228b666e017da97a346c37bcf9624f64fb25cdbfd` | 0 |
| orderer/common/msgprocessor/filter.go | 1520 | `d9fc63160e3ffa5b2377085370b5afae773c877476c2861b2e7d13560f08e47d` | 0 |
| orderer/common/msgprocessor/maintenancefilter.go | 10171 | `c47304a3ed8cb5ded6fb3c5031ab1df45b97d3e94cd144d928c8ed310b556ea2` | 0 |
| orderer/common/msgprocessor/msgprocessor.go | 3389 | `7ee7b8ed03e891a70c5b9044684775a209fcc21faa26807382d806bf09bce423` | 0 |
| orderer/common/msgprocessor/sigfilter.go | 2964 | `76e1b028a87dc631414350a3d8d4b988a9522e259a42deb3987502cc16f9a6c7` | 0 |
| orderer/common/msgprocessor/sizefilter.go | 1676 | `7a809c5b5f3cc537766c3532e9daec6888cd5c60a3c3b50fee70917bed6e16f2` | 0 |
| orderer/common/msgprocessor/standardchannel.go | 6844 | `f6e24990285fe214a8ca890b47a03a7ea4aeb890c20e119b7dd9fcbe849d1819` | 0 |
| orderer/common/multichannel/blockwriter.go | 9645 | `b2ac572f82c947f8b9ffd09a4834d2779e0a92ab5c963a8343973c19b17495fd` | 0 |
| orderer/common/multichannel/chainsupport.go | 5859 | `55768da1b6469c1d24a84d8daeceffaaaeb3bb8273ccc0ba179f96a3f1e1ca9b` | 0 |
| orderer/common/multichannel/ledger_resources.go | 2696 | `6b04468b6873882d9b4e0c2d1dfcd5730f67b8808440fb3caff4c5c74d92e448` | 0 |
| orderer/common/multichannel/metrics.go | 2695 | `f81dc969c81903394c80b7ed2ded2577071781dbc33c8bab7a0f979b850e8238` | 0 |
| orderer/common/multichannel/registrar.go | 34901 | `22b64a61c6142439acc65fd9bf4cb974bd05f71e7b38c0dcd98f03ab4afc4201` | 0 |
| orderer/common/server/main.go | 27674 | `16ce8c8f8d5741f802f53c3af709d1e34ab9a6833d393ed89795ab440b861647` | 0 |
| orderer/common/server/policymanager.go | 1305 | `974a714f6294e191f5dacc2af49b21514d3f7f2edfffdaf0e77e0ea0ed415b85` | 0 |
| orderer/common/server/server.go | 6081 | `7cc48e3da0f43133b42d10446b0097a3536d35c570a7a76e79e91eb641faa16e` | 0 |
| orderer/common/server/signals.go | 363 | `3f9ba0eec5a8fdec32adf58299f3a5395ff59143d7fec9412c39948f249264f3` | 0 |
| orderer/common/server/signals_windows.go | 228 | `0fed93ed8c53d53302ae7158ba21d7ccd56c78d4b55b5c5ffdd67004b2037793` | 0 |
| orderer/common/server/util.go | 4497 | `ae2cf5925e59f60705ada3adbd7a9ab33ea2f709083233c0533bc5693cbd6514` | 0 |
| orderer/common/throttle/ratelimit.go | 3999 | `e5055c2eba776d0e4a0d3c83f7156425ec532b428393718d3db7b532bbc53341` | 0 |
| orderer/common/types/channelinfo.go | 3770 | `e0803b1db3c7676b06956924e3f765730b16638e2cb31a33202fd71ba489d000` | 0 |
| orderer/common/types/errors.go | 1708 | `3ca0b38cea489b2e7f5e0bb6f1ac25681a664b66fc19a2691382395071ce429d` | 0 |
| orderer/consensus/cluster_status.go | 1135 | `aff8de6879c36989f64ad6dd3d45e4ca701586a3f4113d94cc7533e0cfe6af47` | 0 |
| orderer/consensus/consensus.go | 7975 | `084be78fef42c292e075ebca5992584d48ad0003ee32b2ce2ed455a1a5db5dcf` | 0 |
| orderer/consensus/etcdraft/blockcreator.go | 1033 | `fb9936d1b6fff73ecbcbcf7de7606b5e53e290be0d159f8f6c6f31294960dd4e` | 0 |
| orderer/consensus/etcdraft/blockpuller.go | 3692 | `eb6ded8f5e3c5fa169bdde1ab4cb4e1e9b3c3b4ce3cc0504fd8ca91db10f5612` | 0 |
| orderer/consensus/etcdraft/chain.go | 52466 | `aed83b5cea203204877bc3d0af171f66c36de4e463f71590d980b8b530899e9f` | 0 |
| orderer/consensus/etcdraft/consenter.go | 13614 | `45f568bcaac8b323198f8a88e12792b17d74311a6582bf75d0795162ef9c18c1` | 0 |
| orderer/consensus/etcdraft/dispatcher.go | 2234 | `0320c7e7549ee668ed5dcb4fa5f7658b3a5647033d25dd98eda37d06723fc8e3` | 0 |
| orderer/consensus/etcdraft/disseminator.go | 1107 | `bd9d7117cc2f78e68fa24528704da7cedf17b29204298e206e5a1a37a47da7c3` | 0 |
| orderer/consensus/etcdraft/eviction.go | 4802 | `04b395854823c45334a4966e7e77adfe1b2060a37e3d9d385464104fc7f772e5` | 0 |
| orderer/consensus/etcdraft/membership.go | 5326 | `6bc94ea9674fb2e8b897eea645b02ce520b7b214671abe9a2cba02d5cf81420c` | 0 |
| orderer/consensus/etcdraft/metrics.go | 4220 | `a33c0e329e2c67703c0749133b54ff28f088a32c6944a7ad49f96aeb5a15842c` | 0 |
| orderer/consensus/etcdraft/node.go | 10282 | `4daef869de7429ad69489b6c3aa7a57714b090726ba5b9313fa903108636653c` | 0 |
| orderer/consensus/etcdraft/storage.go | 13137 | `d45d968812becceba518ba008913f3235140cd9e8b650d10c11256b34362c886` | 0 |
| orderer/consensus/etcdraft/tracker.go | 1926 | `00bc1f5d4d19a1aa7647ac00c8b2dd9e2bd347a744518ca55436281e7abcf36b` | 0 |
| orderer/consensus/etcdraft/util.go | 16889 | `ac56be3e8e9dc7437269b5dbf6869898c07389323d278e0a7d46701dc2e31c94` | 0 |
| orderer/consensus/smartbft/assembler.go | 5872 | `c2b6017f4bb9045384d2cb26d39c9414dccc45849568bff164df2801735170a9` | 0 |
| orderer/consensus/smartbft/block_puller_factory.go | 3447 | `f3eee110dfde76370e0a0d0f086d66ff1eb516960958bd058e0c7103d74a5098` | 0 |
| orderer/consensus/smartbft/chain.go | 22431 | `04bf2ec245b3fb9d5536ca3e19c0142c8f778708b275ebd17c0b802f5a322e64` | 0 |
| orderer/consensus/smartbft/configverifier.go | 8158 | `90fb20bbf3bd064fc45f1718f3752268fdb7c3987828d668cd484d54fedbaaac` | 0 |
| orderer/consensus/smartbft/consenter.go | 11955 | `b578df97e6e0648afd85f163956c651f3fd005f87a5640f27889a28d9df8250a` | 0 |
| orderer/consensus/smartbft/egress.go | 2545 | `da042e8cd3648c414064fa51d08b12892f74198be5c5fbb17fee014c7edbbbfa` | 0 |
| orderer/consensus/smartbft/ingress.go | 2429 | `c53475ec2f76f5edd02af5d0464fbf63896022ff5bb6b2f55ccbff289486ff51` | 0 |
| orderer/consensus/smartbft/interfaces.go | 1207 | `fca8480e5acba5de4e864b9905a02a67ba53738eb074b6185c8e73125f889098` | 0 |
| orderer/consensus/smartbft/metrics.go | 1863 | `202c838c3f8d1dad7434cb10ced39886d9f3035b3832b1547002a09ac7ef90e8` | 0 |
| orderer/consensus/smartbft/metrics_provider_converter.go | 2451 | `da98c443d57cb7f83f048c2fa3c37fe1b4c550690c4875e9d7c1ea51d7313a49` | 0 |
| orderer/consensus/smartbft/signature.go | 2199 | `ce0c455b87f2fc3073a693e536e9b8958d51ac902862ce436bc885fc4836c690` | 0 |
| orderer/consensus/smartbft/signer.go | 2189 | `0dbc17ea47b37a022608a531f5ec8e19cbe46106843a69b02037b850e1ca6a7f` | 0 |
| orderer/consensus/smartbft/sync_buffer.go | 1477 | `ca574afd25eee578be447e3707f06a7f5ec0e9a2b2169228f16353e59ff4faea` | 0 |
| orderer/consensus/smartbft/synchronizer.go | 5499 | `246e3c7d718d31d9fd29997ab706ba3be0ef8640db4fb455b30958b15fb2f175` | 0 |
| orderer/consensus/smartbft/synchronizer_bft.go | 10411 | `2e12ee6431c5c17c09a6da4f43ff4882936ce1e6d2c78745fd3a75a600f2d5a5` | 0 |
| orderer/consensus/smartbft/synchronizer_factory.go | 3833 | `e99379f0911a8ca5adf467f56e0b92d28f6b10063164f888ac0ed5944c013e27` | 0 |
| orderer/consensus/smartbft/util.go | 18182 | `bf8986e94385f53a1b3975ed8fc360f2a02f20d98ef31eebce49e463492203f1` | 0 |
| orderer/consensus/smartbft/util/util.go | 3070 | `253c5c74f39ae4de73d4e095d505b542fd08e339d163bfb03e6df28db9fa2d57` | 0 |
| orderer/consensus/smartbft/verifier.go | 16381 | `4bd3e669263107a68f57a3f489a40f2cc736b0d6975df75e7b8f4aa9c1ba143b` | 0 |
| pkg/statedata/types.go | 1712 | `9ffdc1cd9cab0bbc9dfe78488bb5efd5339d23f61e06d09ed4a468942ca77b6e` | 0 |
| pkg/tx/interfaces.go | 13226 | `dba343f611c2b7c38ad3802db37f3ada5735882e1aca4fd0f09a2627a6976a64` | 0 |
| protoutil/blockutils.go | 11519 | `13e239a6aaa1a338bde3605f336a52ed360bea9814835c69e038cd7966f8c8fd` | 0 |
| protoutil/commonutils.go | 8185 | `1c59989b9a58053623dce42f9e7ad7998de79148e02d433c34dee71f9f841efd` | 0 |
| protoutil/configtxutils.go | 396 | `65531e092d2555b6a21dc4fc2289d4f79c06cc7b54f4cf0c43502475a644bede` | 0 |
| protoutil/fakes/signer_serializer.go | 4813 | `c2d58aa361d57ae3152228f14f524e963fb1d651f1e3de168ed546153fe7bf74` | 0 |
| protoutil/proputils.go | 15552 | `57415c0e72484216ab180f60dfbb8041f638d69daa1db4c4781243acc427d623` | 0 |
| protoutil/signeddata.go | 3763 | `bfd7895cf428e0762f731163dc5014c33b6900cf2bf55bcd7a0a82a5e328e1a9` | 0 |
| protoutil/txutils.go | 15056 | `08e0a9c30cbf3db6f4677eb7d94e1340ad7155e937d13009b70efe35f5618a54` | 0 |
| protoutil/unmarshalers.go | 9364 | `a2ad7a4237d0aa7ebaaa3d39ac6de0062ac5246efcdb14c2d2469c21c219cb06` | 0 |
| sampleconfig/msp/cacerts/cacert.pem | 887 | `6d24d0804ade3d38931f6fd3545cc5fd793b2b8aa2dc188b8d61424b01a2f020` | 0 |
| sampleconfig/msp/tlsintermediatecerts/tlsintermediate.pem | 778 | `e9f18cc371b6c3b70ad082bee55f3d886073a2e46a416fd53cd4ccebd52ead79` | 0 |
| swagger/docs.go | 593 | `e3682a7d38f904b82143d47d6b5f682f6fb2fadab32acdf915e87ca221b73624` | 0 |
| tools/go.mod | 14090 | `fb7dab680041c396a3730520a64b48f692d38595e063f0d883f7aebae370937c` | 0 |
