# Security & Post-Quantum Readiness Audit Report

**Project:** fabric-lib-go @ f8b4f4a833e4 · Hyperledger Fabric (LF Decentralized Trust) — public repository (passive review)
| | |
|---|---|
| Organization | QSI |
| Report date | 2026-11-06 10:15 UTC |
| Report version | 1 |
| Audit run | 9f3b8d12-9473-49de-9ebb-9f2f640f8653 (Document audit) |
| Analyzer engine | qsi-engine 1.3.0 |
| Risk profile | Crypto exchange, custodian or wallet |
| Content SHA-256 | `967ff3502b91c3f489ae4dc96bfd80d7f227c73a45038ab60ffb4c654876bd06` |
| Signature key (Ed25519, SHA-256 fingerprint; the signature is the separate file report.sig.json) | `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e` |
> This report presents automated and documented analysis results for the stated scope. It is not a legal opinion, a certification or an attestation of compliance with any standard.

## 1. Executive summary

- Critical: **0**
- High: **1**
- Medium: **3**
- Low: **0**
- Info: **7**

- Confirmed technical vulnerability: 0
- Known vulnerable component: 8
- Confirmed configuration error: 0
- Potential cryptographic risk: 0
- Long-term post-quantum risk: 3
- Improvement recommendation: 0
- Insufficient data: 0

Mosca's inequality (x + y > z): x = 10, y = 5, z = 8 → migration would finish too late under this scenario. _z is a planning assumption chosen per risk profile, not a prediction. A cryptographically relevant quantum computer is not publicly known to exist today._

**Post-quantum maturity: Level 0 of 4 — no post-quantum cryptography.** Next step: Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

## 2. Scope and boundaries

Mode: Document audit

Repository: <https://github.com/hyperledger/fabric-lib-go> @ `f8b4f4a833e4140a4d006fc2e0a46823952b5f1c` — evidence links open the lines at this commit.

67 files, 263295 bytes in total, 0 redaction(s); the per-file SHA-256 list is in appendix C.

## 3. Methodology

| Area | Status | Count | Examples |
|---|---|---|---|
| source_code | checked | 65 | bccsp/aesopts.go: 82 lines scanned with 16 rule patterns and 266 registry patterns; bccsp/bccsp.go: 134 lines scanned with 16 rule patterns and 266 registry patterns; bccsp/ecdsaopts.go: 49 lines scanned with 16 rule patterns and 266 registry patterns |
| dependencies | checked | 2 | go.mod: 41 dependencies parsed (41 pinned); tools/go.mod: 5 dependencies parsed (5 pinned) |
| entropy | checked | 1 | random-number generation: 65 code files read with 0 macro definitions from the tree; 0 ineffective guard(s), 0 weak random-bytes provider(s), 0 weak key-generation site(s) |
| osv_advisories | checked | 1 | 42 pinned packages queried at OSV.dev; 2 affected |

_Long lists are grouped here; the full per-file list is in the JSON report, signed with the same key._

## 4. Assets examined and not examined

- None

## 5. Architecture overview

Static review of the source tree fabric-lib-go at f8b4f4a833e4140a4d006fc2e0a46823952b5f1c. 67 files analysed; of 150 files, 63 are test, fuzzing, benchmark or example code and were left out, 20 are not read by any analyzer, 0 exceed the per-file limit and 0 did not fit the total limit. Files no analyzer reads include: .github/settings.yml, .github/workflows/build.yml, .github/workflows/schedule.yml, .gitignore, CODEOWNERS. 1581 files in build-output or dependency-cache directories (.git, .hg, .venv, __pycache__, build, dist, node_modules, target, vendor, venv) were not read. No requests were sent to the owner's systems.

## 6. Overall security posture

- Indicative posture index: **88** / 100 — _Derived from findings in scope (confirmed and potential issues weighted by severity). Indicative only; not comparable across differently scoped audits._
- Quantum-vulnerable share of inventory: 64.9%

## 7. Detailed findings

### QSI-2026-17514 — google.golang.org/grpc v1.83.1 is affected by GHSA-2v4p-qf9q-27wj (CVE-2026-84445, GO-2026-6443)

- Severity: **High** · Classification: Known vulnerable component · Confidence: Medium
- Affected asset: `dependency:Go/google.golang.org/grpc@v1.83.1`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 10:15 UTC
- Priority score: 50.2 / 100
- CVSS v3.1: not applicable

OSV.dev reports GHSA-2v4p-qf9q-27wj (CVE-2026-84445, GO-2026-6443) for Go package google.golang.org/grpc at version v1.83.1: gRPC-Go xDS servers: Denial of Service (DoS) via crash due to missing `:authority` and `Host` headers. The advisory lists only unexported functions (google.golang.org/grpc/internal/transport.http2Server.HandleStreams, google.golang.org/grpc/internal/transport.http2Server.operateHeaders, google.golang.org/grpc/internal/xds/server.RouteAndProcess), which code outside the package cannot call by name, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-2v4p-qf9q-27wj
```

**Evidence.**

_tool_output · [OSV.dev GHSA-2v4p-qf9q-27wj](https://osv.dev/vulnerability/GHSA-2v4p-qf9q-27wj) · line 19 · SHA-256 3566bf539cd1bed726145fc02332a18308f9a065bb8b992c0e44deb9ec44221a_

```
{"id": "GHSA-2v4p-qf9q-27wj", "aliases": ["CVE-2026-84445", "GO-2026-6443"], "modified": "2026-09-25T18:00:05.270054427Z", "summary": "gRPC-Go xDS servers: Denial of Service (DoS) via crash due to missing `:authority` and `Host` headers", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X"}], "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed. A Go function counts only in a file that also names its package (a method: its type); unexported functions only through the exported ones.

**Recommendation.** Upgrade to a fixed version (1.82.2, 1.83.2, 1.84.0-dev.0.20260825144003-d5a41119e0e3, 1.85.0-dev.0.20260825072537-93e31b48545e).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-17511 — Quantum-vulnerable ECDSA: role not determined (10 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:ECDSA:general`
- Data source: bccsp/pkcs11/ecdsakey.go
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.3.0 · 2026-11-06 10:15 UTC
- Priority score: 34.2 / 100
- CVSS v3.1: not applicable

14 reference(s) to ECDSA across 10 file(s), e.g. bccsp/pkcs11/ecdsakey.go:19. Role, judged from paths, function names and nearby code: role not determined. The code does not show what the keys protect; review decides the priority.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open bccsp/pkcs11/ecdsakey.go:19 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [bccsp/pkcs11/ecdsakey.go](https://github.com/hyperledger/fabric-lib-go/blob/f8b4f4a833e4140a4d006fc2e0a46823952b5f1c/bccsp/pkcs11/ecdsakey.go#L19) · line 19 · SHA-256 87680e3cf321a1d927f748c94e56fef66319eb13e2554469b4d613e55886927b_

```
   18 | import (
   19 | 	"crypto/ecdsa"
   20 | 	"crypto/x509"
```

_file_excerpt · [bccsp/pkcs11/pkcs11.go](https://github.com/hyperledger/fabric-lib-go/blob/f8b4f4a833e4140a4d006fc2e0a46823952b5f1c/bccsp/pkcs11/pkcs11.go#L11) · line 11 · SHA-256 8da8b0c88ebe01946640787c08a65d84eb065c628bc69992d0bd8b7d1eda1ff8_

```
   10 | 	"context"
   11 | 	"crypto/ecdsa"
   12 | 	"crypto/elliptic"
```

_file_excerpt · [bccsp/pkcs11/pkcs11.go](https://github.com/hyperledger/fabric-lib-go/blob/f8b4f4a833e4140a4d006fc2e0a46823952b5f1c/bccsp/pkcs11/pkcs11.go#L330) · line 330 · SHA-256 c46c43f1ab599be0dc6777bac06d578b05466bf53f5527162b89cacfcc3b671c_

```
  329 | 	if csp.softVerify {
  330 | 		return ecdsa.Verify(k.pub, digest, r, s), nil
  331 | 	}
```

_file_excerpt · [bccsp/sw/ecdsa.go](https://github.com/hyperledger/fabric-lib-go/blob/f8b4f4a833e4140a4d006fc2e0a46823952b5f1c/bccsp/sw/ecdsa.go#L19) · line 19 · SHA-256 1515eca1cc78dc2b7c4fde09c0aa059dc7c5a6a53519f5c1b42098f4eadc395d_

```
   18 | import (
   19 | 	"crypto/ecdsa"
   20 | 	"crypto/rand"
```

_file_excerpt · [bccsp/sw/ecdsa.go](https://github.com/hyperledger/fabric-lib-go/blob/f8b4f4a833e4140a4d006fc2e0a46823952b5f1c/bccsp/sw/ecdsa.go#L28) · line 28 · SHA-256 5e03fc2ced291506b09bf90d810db18d327d592f8781b028b97d572b077c587c_

```
   27 | func signECDSA(k *ecdsa.PrivateKey, digest []byte, opts bccsp.SignerOpts) ([]byte, error) {
   28 | 	r, s, err := ecdsa.Sign(rand.Reader, k, digest)
   29 | 	if err != nil {
```

_file_excerpt · [bccsp/sw/ecdsa.go](https://github.com/hyperledger/fabric-lib-go/blob/f8b4f4a833e4140a4d006fc2e0a46823952b5f1c/bccsp/sw/ecdsa.go#L56) · line 56 · SHA-256 cc80b9b87564d0ae70ba183543c926e98984365178ee8a10c6384959a648b188_

```
   55 | 
   56 | 	return ecdsa.Verify(k, digest, r, s), nil
   57 | }
```

_file_excerpt · [bccsp/sw/ecdsakey.go](https://github.com/hyperledger/fabric-lib-go/blob/f8b4f4a833e4140a4d006fc2e0a46823952b5f1c/bccsp/sw/ecdsakey.go#L19) · line 19 · SHA-256 da30811132376f3039c613505f0d52458e1593d43e0280ad13aaf57389cf7c73_

```
   18 | import (
   19 | 	"crypto/ecdsa"
   20 | 	"crypto/elliptic"
```

_file_excerpt · [bccsp/sw/fileks.go](https://github.com/hyperledger/fabric-lib-go/blob/f8b4f4a833e4140a4d006fc2e0a46823952b5f1c/bccsp/sw/fileks.go#L11) · line 11 · SHA-256 e5b44015f00ef128ab2f3d1c4f1dee7dcd77a13dd2b3391fad9bc2ecb9c49ae6_

```
   10 | 	"bytes"
   11 | 	"crypto/ecdsa"
   12 | 	"crypto/ed25519"
```

_file_excerpt · [bccsp/sw/keyderiv.go](https://github.com/hyperledger/fabric-lib-go/blob/f8b4f4a833e4140a4d006fc2e0a46823952b5f1c/bccsp/sw/keyderiv.go#L20) · line 20 · SHA-256 9f85b73ac6ec142259370ca9358f25e99f4a2d13e133f7ddee639c918ed9af9b_

```
   19 | import (
   20 | 	"crypto/ecdsa"
   21 | 	"crypto/hmac"
```

_file_excerpt · [bccsp/sw/keygen.go](https://github.com/hyperledger/fabric-lib-go/blob/f8b4f4a833e4140a4d006fc2e0a46823952b5f1c/bccsp/sw/keygen.go#L10) · line 10 · SHA-256 7983932d009be78f478f371ae58c3f86b9f6b72f687b9ed011a4aee4ad95d71d_

```
    9 | import (
   10 | 	"crypto/ecdsa"
   11 | 	"crypto/ed25519"
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it; introduce an abstraction layer for crypto-agility.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-17512 — Quantum-vulnerable Ed25519: role not determined (6 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:Ed25519:general`
- Data source: bccsp/sw/ed25519.go
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.3.0 · 2026-11-06 10:15 UTC
- Priority score: 34.2 / 100
- CVSS v3.1: not applicable

39 reference(s) to Ed25519 across 6 file(s), e.g. bccsp/sw/ed25519.go:15. Role, judged from paths, function names and nearby code: role not determined. The code does not show what the keys protect; review decides the priority.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open bccsp/sw/ed25519.go:15 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [bccsp/sw/ed25519.go](https://github.com/hyperledger/fabric-lib-go/blob/f8b4f4a833e4140a4d006fc2e0a46823952b5f1c/bccsp/sw/ed25519.go#L15) · line 15 · SHA-256 be962610d24d0e25089b18a267e417de6efea2a91e686d6803d7a04d54b8cb0c_

```
   14 | func signED25519(k *ed25519.PrivateKey, msg []byte, opts bccsp.SignerOpts) ([]byte, error) {
   15 | 	signature := ed25519.Sign(*k, msg)
   16 | 	return signature, nil
```

_file_excerpt · [bccsp/sw/ed25519.go](https://github.com/hyperledger/fabric-lib-go/blob/f8b4f4a833e4140a4d006fc2e0a46823952b5f1c/bccsp/sw/ed25519.go#L20) · line 20 · SHA-256 aa94dd71ac249c8771fc540b4bc0ae1102dafe73a0a1f2722a94d7ba614d5d79_

```
   19 | func verifyED25519(k *ed25519.PublicKey, signature, msg []byte, opts bccsp.SignerOpts) (bool, error) {
   20 | 	return ed25519.Verify(*k, msg, signature), nil
   21 | }
```

_file_excerpt · [bccsp/sw/ed25519.go](https://github.com/hyperledger/fabric-lib-go/blob/f8b4f4a833e4140a4d006fc2e0a46823952b5f1c/bccsp/sw/ed25519.go#L23) · line 23 · SHA-256 6f33081caebdef556a3b8c3fe6eeca1f1c206bd80023c04d0dd16a68a6634e70_

```
   22 | 
   23 | type ed25519Signer struct{}
   24 | 
```

_file_excerpt · [bccsp/sw/ed25519key.go](https://github.com/hyperledger/fabric-lib-go/blob/f8b4f4a833e4140a4d006fc2e0a46823952b5f1c/bccsp/sw/ed25519key.go#L18) · line 18 · SHA-256 c161f2e6d9d89ebe1d96be52c121110e7611fbcf8cb5872b5816d483a91b9152_

```
   17 | 
   18 | type ed25519PrivateKey struct {
   19 | 	privKey *ed25519.PrivateKey
```

_file_excerpt · [bccsp/sw/ed25519key.go](https://github.com/hyperledger/fabric-lib-go/blob/f8b4f4a833e4140a4d006fc2e0a46823952b5f1c/bccsp/sw/ed25519key.go#L24) · line 24 · SHA-256 ee921a0dccc1f590e41024cdb8f552d96e7e79860fc51361bdd9e7282a296bd9_

```
   23 | // if this operation is allowed.
   24 | func (k *ed25519PrivateKey) Bytes() ([]byte, error) {
   25 | 	return nil, errors.New("Not supported.")
```

_file_excerpt · [bccsp/sw/ed25519key.go](https://github.com/hyperledger/fabric-lib-go/blob/f8b4f4a833e4140a4d006fc2e0a46823952b5f1c/bccsp/sw/ed25519key.go#L29) · line 29 · SHA-256 488f2f75c771d7f192ac75a4d1524cd88cad84dc34abaa8f25806c126cb56d58_

```
   28 | // SKI returns the subject key identifier of this key.
   29 | func (k *ed25519PrivateKey) SKI() []byte {
   30 | 	if k.privKey == nil {
```

_file_excerpt · [bccsp/sw/fileks.go](https://github.com/hyperledger/fabric-lib-go/blob/f8b4f4a833e4140a4d006fc2e0a46823952b5f1c/bccsp/sw/fileks.go#L147) · line 147 · SHA-256 1cfe306c77e7f7694c28b313f33d969f772a0285e232590afa48e1c614905b2c_

```
  146 | 		case ed25519.PrivateKey:
  147 | 			return &ed25519PrivateKey{&k}, nil
  148 | 		case *rsa.PrivateKey:
```

_file_excerpt · [bccsp/sw/fileks.go](https://github.com/hyperledger/fabric-lib-go/blob/f8b4f4a833e4140a4d006fc2e0a46823952b5f1c/bccsp/sw/fileks.go#L164) · line 164 · SHA-256 749ebaa93ccb680875e11da118e180004d476946a6c4e4bcacbc5ac6dc3056b6_

```
  163 | 		case ed25519.PublicKey:
  164 | 			return &ed25519PublicKey{&k}, nil
  165 | 		case *rsa.PublicKey:
```

_file_excerpt · [bccsp/sw/fileks.go](https://github.com/hyperledger/fabric-lib-go/blob/f8b4f4a833e4140a4d006fc2e0a46823952b5f1c/bccsp/sw/fileks.go#L198) · line 198 · SHA-256 070f2f8ff0382634eed998627dc8b68a8775020445d49702f7472219ea427e14_

```
  197 | 
  198 | 	case *ed25519PrivateKey:
  199 | 		err = ks.storePrivateKey(hex.EncodeToString(k.SKI()), kk.privKey)
```

_file_excerpt · [bccsp/sw/keygen.go](https://github.com/hyperledger/fabric-lib-go/blob/f8b4f4a833e4140a4d006fc2e0a46823952b5f1c/bccsp/sw/keygen.go#L36) · line 36 · SHA-256 07b0787395320c0dcb325ee82d4a64a304cd8fc2872374aa7dd3cfc78e7191c7_

```
   35 | func (kg *ed25519KeyGenerator) KeyGen(opts bccsp.KeyGenOpts) (bccsp.Key, error) {
   36 | 	_, privKey, err := ed25519.GenerateKey(rand.Reader)
   37 | 	if err != nil {
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it; introduce an abstraction layer for crypto-agility.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-17513 — Quantum-vulnerable RSA: role not determined (6 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:RSA:general`
- Data source: bccsp/sw/fileks.go
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.3.0 · 2026-11-06 10:15 UTC
- Priority score: 34.2 / 100
- CVSS v3.1: not applicable

7 reference(s) to RSA across 6 file(s), e.g. bccsp/sw/fileks.go:13. Role, judged from paths, function names and nearby code: role not determined. The code does not show what the keys protect; review decides the priority.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open bccsp/sw/fileks.go:13 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [bccsp/sw/fileks.go](https://github.com/hyperledger/fabric-lib-go/blob/f8b4f4a833e4140a4d006fc2e0a46823952b5f1c/bccsp/sw/fileks.go#L13) · line 13 · SHA-256 768ee06b9c3e2ed1d6af2ed858f328bdd5acdddaccbe6d3c2ecd30aebb1ab1d7_

```
   12 | 	"crypto/ed25519"
   13 | 	"crypto/rsa"
   14 | 	"encoding/hex"
```

_file_excerpt · [bccsp/sw/keygen.go](https://github.com/hyperledger/fabric-lib-go/blob/f8b4f4a833e4140a4d006fc2e0a46823952b5f1c/bccsp/sw/keygen.go#L14) · line 14 · SHA-256 364e7ffecee10ae3b8e624ca22f247d6c912d5e4981f71e890c23ab5677cf5dd_

```
   13 | 	"crypto/rand"
   14 | 	"crypto/rsa"
   15 | 	"fmt"
```

_file_excerpt · [bccsp/sw/keygen.go](https://github.com/hyperledger/fabric-lib-go/blob/f8b4f4a833e4140a4d006fc2e0a46823952b5f1c/bccsp/sw/keygen.go#L62) · line 62 · SHA-256 b7bba74d01f03eef780ca8edc8d8f543670a53cc919dc442239153bb3820145c_

```
   61 | func (kg *rsaKeyGenerator) KeyGen(opts bccsp.KeyGenOpts) (bccsp.Key, error) {
   62 | 	lowLevelKey, err := rsa.GenerateKey(rand.Reader, int(kg.length))
   63 | 	if err != nil {
```

_file_excerpt · [bccsp/sw/keyimport.go](https://github.com/hyperledger/fabric-lib-go/blob/f8b4f4a833e4140a4d006fc2e0a46823952b5f1c/bccsp/sw/keyimport.go#L12) · line 12 · SHA-256 7318348444f9d7d18c85c7efbf08d2965e7d68412a40ee459b218cde70685d97_

```
   11 | 	"crypto/ed25519"
   12 | 	"crypto/rsa"
   13 | 	"crypto/x509"
```

_file_excerpt · [bccsp/sw/keys.go](https://github.com/hyperledger/fabric-lib-go/blob/f8b4f4a833e4140a4d006fc2e0a46823952b5f1c/bccsp/sw/keys.go#L15) · line 15 · SHA-256 070992b7bb94b0dbc8e66fb1b57b459fe619fa742bac22418518a3f923a61864_

```
   14 | 	"crypto/rand"
   15 | 	"crypto/rsa"
   16 | 	"crypto/x509"
```

_file_excerpt · [bccsp/sw/rsa.go](https://github.com/hyperledger/fabric-lib-go/blob/f8b4f4a833e4140a4d006fc2e0a46823952b5f1c/bccsp/sw/rsa.go#L11) · line 11 · SHA-256 a77c4604bea38eaadc0ee9cf5c192333b6ac97a6a6ab944dce48ee75a086b6a3_

```
   10 | 	"crypto/rand"
   11 | 	"crypto/rsa"
   12 | 	"errors"
```

_file_excerpt · [bccsp/sw/rsakey.go](https://github.com/hyperledger/fabric-lib-go/blob/f8b4f4a833e4140a4d006fc2e0a46823952b5f1c/bccsp/sw/rsakey.go#L10) · line 10 · SHA-256 5e8f30d23b521293b331ecad3ad4d4d3b8072be834d89f4c17cd5a1a5cad919a_

```
    9 | import (
   10 | 	"crypto/rsa"
   11 | 	"crypto/sha256"
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it; introduce an abstraction layer for crypto-agility.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-17515 — golang.org/x/net v0.58.0 is affected by GO-2026-6603 (CVE-2026-78659) (no severity rating)

- Severity: **Info** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:Go/golang.org/x/net@v0.58.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 10:15 UTC
- Priority score: 17.8 / 100
- CVSS v3.1: not applicable

OSV.dev reports GO-2026-6603 (CVE-2026-78659) for Go package golang.org/x/net at version v0.58.0: HTTP/2 server memory exhaustion due to Trailer headers in net/http. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. None of the affected functions (golang.org/x/net/http2.ClientConn.Close, golang.org/x/net/http2.ClientConn.Ping, golang.org/x/net/http2.ClientConn.RoundTrip, golang.org/x/net/http2.ClientConn.Shutdown, golang.org/x/net/http2.ConfigureServer, golang.org/x/net/http2.ConfigureTransport …) is named in the audited code: the advisory does not apply unless they are reached indirectly (traits, macros, other dependencies).

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-6603
```

**Evidence.**

_tool_output · [OSV.dev GO-2026-6603](https://osv.dev/vulnerability/GO-2026-6603) · line 46 · SHA-256 9e43850e0da48e9d00589cc2bffb372f39ec5e5a280f2f4b04520a91328fd703_

```
{"id": "GO-2026-6603", "aliases": ["BIT-golang-2026-78659", "CVE-2026-78659"], "modified": "2026-10-16T09:55:47.068117441Z", "summary": "HTTP/2 server memory exhaustion due to Trailer headers in net/http", "severity": null, "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed. A Go function counts only in a file that also names its package (a method: its type); unexported functions only through the exported ones.

**Recommendation.** Triage the advisory; upgrade to a fixed version (0.60.0) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-17516 — golang.org/x/net v0.58.0 is affected by GO-2026-6610 (CVE-2026-78660) (no severity rating)

- Severity: **Info** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:Go/golang.org/x/net@v0.58.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 10:15 UTC
- Priority score: 17.8 / 100
- CVSS v3.1: not applicable

OSV.dev reports GO-2026-6610 (CVE-2026-78660) for Go package golang.org/x/net at version v0.58.0: HTTP/2 transport accepts malformed framing-related headers in net/http. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. None of the affected functions (golang.org/x/net/http2.Transport.NewClientConn, golang.org/x/net/http2.Transport.RoundTrip, golang.org/x/net/http2.Transport.RoundTripOpt, golang.org/x/net/http2.clientConnPool.GetClientConn, golang.org/x/net/http2.clientConnReadLoop.handleResponse, golang.org/x/net/http2.noDialClientConnPool.GetClientConn …) is named in the audited code: the advisory does not apply unless they are reached indirectly (traits, macros, other dependencies).

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-6610
```

**Evidence.**

_tool_output · [OSV.dev GO-2026-6610](https://osv.dev/vulnerability/GO-2026-6610) · line 46 · SHA-256 1b823e53f27093797b8a7909032006e1f0f818f04118ad593a4641236392faa9_

```
{"id": "GO-2026-6610", "aliases": ["BIT-golang-2026-78660", "CVE-2026-78660"], "modified": "2026-10-16T09:56:04.364467528Z", "summary": "HTTP/2 transport accepts malformed framing-related headers in net/http", "severity": null, "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed. A Go function counts only in a file that also names its package (a method: its type); unexported functions only through the exported ones.

**Recommendation.** Triage the advisory; upgrade to a fixed version (0.60.0) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-17517 — golang.org/x/net v0.58.0 is affected by GO-2026-6611 (CVE-2026-78669) (no severity rating)

- Severity: **Info** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:Go/golang.org/x/net@v0.58.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 10:15 UTC
- Priority score: 17.8 / 100
- CVSS v3.1: not applicable

OSV.dev reports GO-2026-6611 (CVE-2026-78669) for Go package golang.org/x/net at version v0.58.0: Excessive CPU consumption from repeated initial window changes in net/http. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. None of the affected functions (golang.org/x/net/http2.ClientConn.Close, golang.org/x/net/http2.ClientConn.Ping, golang.org/x/net/http2.ClientConn.RoundTrip, golang.org/x/net/http2.ClientConn.Shutdown, golang.org/x/net/http2.ClientConn.addStreamLocked, golang.org/x/net/http2.ConfigureServer …) is named in the audited code: the advisory does not apply unless they are reached indirectly (traits, macros, other dependencies).

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-6611
```

**Evidence.**

_tool_output · [OSV.dev GO-2026-6611](https://osv.dev/vulnerability/GO-2026-6611) · line 46 · SHA-256 c9b9f78637131224c5d4073e44c47b7cce490fc5526e3d6b0697b43bc85cab2f_

```
{"id": "GO-2026-6611", "aliases": ["BIT-golang-2026-78669", "CVE-2026-78669"], "modified": "2026-10-16T09:55:38.952277866Z", "summary": "Excessive CPU consumption from repeated initial window changes in net/http", "severity": null, "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed. A Go function counts only in a file that also names its package (a method: its type); unexported functions only through the exported ones.

**Recommendation.** Triage the advisory; upgrade to a fixed version (0.60.0) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-17518 — golang.org/x/net v0.58.0 is affected by GO-2026-6612 (CVE-2026-78663) (no severity rating)

- Severity: **Info** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:Go/golang.org/x/net@v0.58.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 10:15 UTC
- Priority score: 17.8 / 100
- CVSS v3.1: not applicable

OSV.dev reports GO-2026-6612 (CVE-2026-78663) for Go package golang.org/x/net at version v0.58.0: Double flow control refund on HTTP/2 server streams in net/http. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. None of the affected functions (golang.org/x/net/http2.ClientConn.Close, golang.org/x/net/http2.ClientConn.Ping, golang.org/x/net/http2.ClientConn.RoundTrip, golang.org/x/net/http2.ClientConn.Shutdown, golang.org/x/net/http2.ConfigureServer, golang.org/x/net/http2.ConfigureTransport …) is named in the audited code: the advisory does not apply unless they are reached indirectly (traits, macros, other dependencies).

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-6612
```

**Evidence.**

_tool_output · [OSV.dev GO-2026-6612](https://osv.dev/vulnerability/GO-2026-6612) · line 46 · SHA-256 1471910f88c9bbf8395a304fd82510f61567373756002de8bcdc3fbe305890cb_

```
{"id": "GO-2026-6612", "aliases": ["BIT-golang-2026-78663", "CVE-2026-78663"], "modified": "2026-10-16T09:55:54.129082194Z", "summary": "Double flow control refund on HTTP/2 server streams in net/http", "severity": null, "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed. A Go function counts only in a file that also names its package (a method: its type); unexported functions only through the exported ones.

**Recommendation.** Triage the advisory; upgrade to a fixed version (0.60.0) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-17519 — golang.org/x/net v0.58.0 is affected by GO-2026-6617 (CVE-2026-97032) (no severity rating)

- Severity: **Info** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:Go/golang.org/x/net@v0.58.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 10:15 UTC
- Priority score: 17.8 / 100
- CVSS v3.1: not applicable

OSV.dev reports GO-2026-6617 (CVE-2026-97032) for Go package golang.org/x/net at version v0.58.0: HTTP/2 server crash due to HPACK encoder race in net/http. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. None of the affected functions (golang.org/x/net/http2.ClientConn.Close, golang.org/x/net/http2.ClientConn.Ping, golang.org/x/net/http2.ClientConn.RoundTrip, golang.org/x/net/http2.ClientConn.Shutdown, golang.org/x/net/http2.ConfigureServer, golang.org/x/net/http2.ConfigureTransport …) is named in the audited code: the advisory does not apply unless they are reached indirectly (traits, macros, other dependencies).

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-6617
```

**Evidence.**

_tool_output · [OSV.dev GO-2026-6617](https://osv.dev/vulnerability/GO-2026-6617) · line 46 · SHA-256 b948c88d959bc78948c7e3b7a746ac4da179933798e9735d02870080906cfc96_

```
{"id": "GO-2026-6617", "aliases": ["BIT-golang-2026-97032", "CVE-2026-97032"], "modified": "2026-10-16T09:55:57.350751224Z", "summary": "HTTP/2 server crash due to HPACK encoder race in net/http", "severity": null, "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed. A Go function counts only in a file that also names its package (a method: its type); unexported functions only through the exported ones.

**Recommendation.** Triage the advisory; upgrade to a fixed version (0.60.0) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-17520 — golang.org/x/net v0.58.0 is affected by GO-2026-6860 (CVE-2026-78661) (no severity rating)

- Severity: **Info** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:Go/golang.org/x/net@v0.58.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 10:15 UTC
- Priority score: 17.8 / 100
- CVSS v3.1: not applicable

OSV.dev reports GO-2026-6860 (CVE-2026-78661) for Go package golang.org/x/net at version v0.58.0: Avoid quadratic complexity when coalescing text nodes in html in golang.org/x/net. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. None of the affected functions (golang.org/x/net/html.Parse, golang.org/x/net/html.ParseFragment, golang.org/x/net/html.ParseFragmentWithOptions, golang.org/x/net/html.ParseWithOptions, golang.org/x/net/html.parser.addText, golang.org/x/net/html.parser.fosterParent …) is named in the audited code: the advisory does not apply unless they are reached indirectly (traits, macros, other dependencies).

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-6860
```

**Evidence.**

_tool_output · [OSV.dev GO-2026-6860](https://osv.dev/vulnerability/GO-2026-6860) · line 46 · SHA-256 1f106c45371219bac0158f7ce44e57c439f50f0c32898616d1563f14cadb1b28_

```
{"id": "GO-2026-6860", "aliases": ["CVE-2026-78661"], "modified": "2026-10-27T21:30:04.890809062Z", "summary": "Avoid quadratic complexity when coalescing text nodes in html in golang.org/x/net", "severity": null, "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed. A Go function counts only in a file that also names its package (a method: its type); unexported functions only through the exported ones.

**Recommendation.** Triage the advisory; upgrade to a fixed version (0.62.0) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-17521 — golang.org/x/net v0.58.0 is affected by GO-2026-6866 (CVE-2026-97045) (no severity rating)

- Severity: **Info** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:Go/golang.org/x/net@v0.58.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 10:15 UTC
- Priority score: 17.8 / 100
- CVSS v3.1: not applicable

OSV.dev reports GO-2026-6866 (CVE-2026-97045) for Go package golang.org/x/net at version v0.58.0: Check all ancestor namespace transitions when rendering raw text in html in golang.org/x/net. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. None of the affected functions (golang.org/x/net/html.Render, golang.org/x/net/html.childTextNodesAreLiteral) is named in the audited code: the advisory does not apply unless they are reached indirectly (traits, macros, other dependencies).

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-6866
```

**Evidence.**

_tool_output · [OSV.dev GO-2026-6866](https://osv.dev/vulnerability/GO-2026-6866) · line 46 · SHA-256 102267a016bc5eef7979a90b1ddd2288ff36b09ab6fa040c808e62f3b55c1f42_

```
{"id": "GO-2026-6866", "aliases": ["CVE-2026-97045"], "modified": "2026-10-27T21:45:08.978077289Z", "summary": "Check all ancestor namespace transitions when rendering raw text in html in golang.org/x/net", "severity": null, "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed. A Go function counts only in a file that also names its package (a method: its type); unexported functions only through the exported ones.

**Recommendation.** Triage the advisory; upgrade to a fixed version (0.62.0) if it applies.

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

### Post-quantum maturity: Level 0 of 4 — no post-quantum cryptography


**Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

_Levels: 0 none; 1 present, not wired; 2 in use outside the critical paths; 3 hybrid in a critical path; 4 post-quantum by default in the critical paths (root of trust, key wrapping, channel key exchange). Judged from code and manifests._

### What the quantum-vulnerable algorithms do

| Role | Algorithms (files) | ID | First step |
|---|---|---|---|
| **role not determined** | ECDSA (10), Ed25519 (6), RSA (6) | QSI-2026-17511, QSI-2026-17512, QSI-2026-17513 | Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it; introduce an abstraction layer for crypto-agility |

_Roles are judged from file paths, function names and the code around each match; review confirms them. Root-of-trust keys and wrapped keys come first: they are hard to replace or can be recorded today._
No readiness questionnaire was completed for this project.

### Quantum algorithms relevant to this inventory

| Quantum algorithm | Effect | Attack model | Inventoried algorithms (rows) | What it means for this audit |
|---|---|---|---|---|
| Shor's algorithm — factoring | breaks | Q1 | RSA (6) | Breaks RSA at every key length: a longer modulus only raises the cost polynomially. Plan migration to ML-KEM (or a hybrid) for key establishment and ML-DSA / SLH-DSA for signatures; start with keys protecting data that must stay confidential for years (harvest now, decrypt later) and with long-lived signatures. |
| Shor's algorithm — elliptic-curve discrete logarithms | breaks | Q1 | ECDSA (10), Ed25519 (8) | Elliptic-curve keys are expected to fall before RSA keys of comparable classical strength. On blockchains, coins whose public key is already on chain (reused addresses, pay-to-public-key and Taproot outputs) are exposed first; plan the move to post-quantum signatures and avoid key reuse in the meantime. |
| Grover's algorithm — key search and preimages | weakens (larger keys restore the margin) | Q1 | HMAC (2), SHA-2 (9), SHA-3 (2) | Not a break. 256-bit keys (AES-256, ChaCha20) keep a comfortable margin; AES-128 meets NIST category 1, while some authorities ask for 256-bit keys in quantum-resistant contexts (see the AES-128 entry). Prefer 256-bit keys for long-lived data; 256-bit hashes need no change for preimage resistance. |
| Brassard–Høyer–Tapp — collision search | weakens (larger keys restore the margin) | Q1 | SHA-2 (9), SHA-3 (2) | 256-bit hashes (SHA-256, SHA3-256) remain adequate for collision resistance; 160-bit hashes are already weak classically (SHA-1 collisions are practical). Use 384/512-bit hashes where NIST categories 4–5 are required. |

_Effects: breaks — replace the algorithm; weakens — larger keys or outputs restore the margin; included in standard parameters — no action at standard parameter sets; only with superposition queries — not applicable to ordinary deployments._


## 9. Limitations and assumptions

- This report presents automated and documented analysis results for the stated scope. It is not a legal opinion, a certification or an attestation of compliance with any standard.
- z is a planning assumption chosen per risk profile, not a prediction. A cryptographically relevant quantum computer is not publicly known to exist today.

## 10. Remediation plan / Priorities for 30, 60 and 90 days

### 30 days

| Priority | ID | Action | Type | Closure criteria |
|---|---|---|---|---|
| P2 | QSI-2026-17514 | Upgrade google.golang.org/grpc to a fixed version (1.82.2, 1.83.2, 1.84.0-dev.0.20260825144003-d5a41119e0e3, 1.85.0-dev.0.20260825072537-93e31b48545e). | root-cause fix | Dependency scan no longer reports GHSA-2v4p-qf9q-27wj (CVE-2026-84445, GO-2026-6443). |
### 60 days

| Priority | ID | Action | Type | Closure criteria |
|---|---|---|---|---|
| P3 | QSI-2026-17515 | Triage GO-2026-6603 (CVE-2026-78659); upgrade golang.org/x/net to a fixed version (0.60.0) if it applies. | root-cause fix | Dependency scan no longer reports GO-2026-6603 (CVE-2026-78659), or the triage is recorded. |
| P3 | QSI-2026-17516 | Triage GO-2026-6610 (CVE-2026-78660); upgrade golang.org/x/net to a fixed version (0.60.0) if it applies. | root-cause fix | Dependency scan no longer reports GO-2026-6610 (CVE-2026-78660), or the triage is recorded. |
| P3 | QSI-2026-17517 | Triage GO-2026-6611 (CVE-2026-78669); upgrade golang.org/x/net to a fixed version (0.60.0) if it applies. | root-cause fix | Dependency scan no longer reports GO-2026-6611 (CVE-2026-78669), or the triage is recorded. |
| P3 | QSI-2026-17518 | Triage GO-2026-6612 (CVE-2026-78663); upgrade golang.org/x/net to a fixed version (0.60.0) if it applies. | root-cause fix | Dependency scan no longer reports GO-2026-6612 (CVE-2026-78663), or the triage is recorded. |
| P3 | QSI-2026-17519 | Triage GO-2026-6617 (CVE-2026-97032); upgrade golang.org/x/net to a fixed version (0.60.0) if it applies. | root-cause fix | Dependency scan no longer reports GO-2026-6617 (CVE-2026-97032), or the triage is recorded. |
| P3 | QSI-2026-17520 | Triage GO-2026-6860 (CVE-2026-78661); upgrade golang.org/x/net to a fixed version (0.62.0) if it applies. | root-cause fix | Dependency scan no longer reports GO-2026-6860 (CVE-2026-78661), or the triage is recorded. |
| P3 | QSI-2026-17521 | Triage GO-2026-6866 (CVE-2026-97045); upgrade golang.org/x/net to a fixed version (0.62.0) if it applies. | root-cause fix | Dependency scan no longer reports GO-2026-6866 (CVE-2026-97045), or the triage is recorded. |
### 90 days

| Priority | ID | Action | Type | Closure criteria |
|---|---|---|---|---|
| P3 | QSI-2026-17511 | Add ECDSA usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-17512 | Add Ed25519 usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-17513 | Add RSA usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P4 | QSI-2026-17511 | Plan migration of ECDSA to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-17512 | Plan migration of Ed25519 to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-17513 | Plan migration of RSA to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |

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
3. C. Gidney — How to factor 2048 bit RSA integers with less than a million noisy qubits (arXiv:2505.15917) — arXiv. <https://arxiv.org/abs/2505.15917> (preprint (2025-05-21): < 1 million noisy qubits, < 1 week, 0.1% gate error, 1 µs surface-code cycle)
4. C. Gidney, M. Ekerå — How to factor 2048 bit RSA integers in 8 hours using 20 million noisy qubits (Quantum 5, 433) — Quantum. <https://doi.org/10.22331/q-2021-04-15-433> (peer-reviewed article (2021): 10^-3 gate error, 1 µs cycle, 10 µs reaction time)
5. C. Zalka — Grover's quantum searching algorithm is optimal (Phys. Rev. A 60, 2746, 1999; arXiv:quant-ph/9711070) — APS. <https://doi.org/10.1103/PhysRevA.60.2746> (peer-reviewed article: optimal for any success probability; parallel search gains no more than splitting the space)
6. Common Vulnerability Scoring System v3.1: Specification Document — FIRST. <https://www.first.org/cvss/v3.1/specification-document> (final)
7. D. J. Bernstein — Cost analysis of hash collisions: Will quantum computers make SHARCS obsolete? (2009) — cr.yp.to. <https://cr.yp.to/hash/collisioncost-20090823.pdf> (paper dated 2009-08-23)
8. D. Litinski — How to compute a 256-bit elliptic curve private key with only 50 million Toffoli gates (arXiv:2306.08585) — arXiv. <https://arxiv.org/abs/2306.08585> (preprint (2023-06-14): 6000 modules × 1152 physical qubits, one key per 10 minutes under its architecture assumptions)
9. FIPS 203 — Module-Lattice-Based Key-Encapsulation Mechanism Standard (ML-KEM) — NIST. <https://csrc.nist.gov/pubs/fips/203/final> (final (August 2024))
10. FIPS 204 — Module-Lattice-Based Digital Signature Standard (ML-DSA) — NIST. <https://csrc.nist.gov/pubs/fips/204/final> (final (August 2024))
11. FIPS 205 — Stateless Hash-Based Digital Signature Standard (SLH-DSA) — NIST. <https://csrc.nist.gov/pubs/fips/205/final> (final (August 2024))
12. G. Brassard, P. Høyer, A. Tapp — Quantum Algorithm for the Collision Problem (LATIN '98; arXiv:quant-ph/9705002) — Springer / arXiv. <https://arxiv.org/abs/quant-ph/9705002> (peer-reviewed article: collisions of r-to-one functions in O((N/r)^{1/3}) expected evaluations)
13. J. Proos, C. Zalka — Shor's discrete logarithm quantum algorithm for elliptic curves (Quantum Inf. Comput. 3(4), 2003; arXiv:quant-ph/0301141) — Quantum Information & Computation. <https://doi.org/10.26421/QIC3.4-3> (peer-reviewed article)
14. L. K. Grover — A fast quantum mechanical algorithm for database search (STOC 1996) — ACM. <https://doi.org/10.1145/237814.237866> (peer-reviewed article)
15. M. Amy et al. — Estimating the cost of generic quantum pre-image attacks on SHA-2 and SHA-3 (SAC 2016; arXiv:1603.09383) — Springer / arXiv. <https://arxiv.org/abs/1603.09383> (peer-reviewed article: SHA-256 about 2^153.8 surface-code cycles on 2^12.6 logical qubits; SHA3-256 about 2^146.5 cycles on 2^20)
16. M. Cain et al. — Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits (arXiv:2603.28627) — arXiv. <https://arxiv.org/abs/2603.28627> (preprint (2026-03-30): P-256 in a few days with 26,000 physical neutral-atom qubits; RSA-2048 one to two orders of magnitude longer)
17. M. Mosca — Cybersecurity in an Era with Quantum Computers: Will We Be Ready? (IEEE Security & Privacy, 2018) — IEEE. <https://doi.org/10.1109/MSP.2018.3761723> (peer-reviewed article; source of the x + y > z migration inequality)
18. M. Roetteler, M. Naehrig, K. Svore, K. Lauter — Quantum resource estimates for computing elliptic curve discrete logarithms (ASIACRYPT 2017) — IACR / arXiv. <https://arxiv.org/abs/1706.06752> (peer-reviewed article: at most 9n + 2⌈log2 n⌉ + 10 qubits and 448 n^3 log2 n + 4090 n^3 Toffoli gates)
19. NIST IR 8547 — Transition to Post-Quantum Cryptography Standards — NIST. <https://csrc.nist.gov/pubs/ir/8547/final> (final (2026-10-27; the initial public draft of November 2024 is obsoleted). Tables 2 and 4: ECDSA, EdDSA and RSA signatures, finite-field and elliptic-curve DH and MQV, and RSA key establishment are deprecated after 2030 and disallowed after 2035 at every key size — the draft deprecated only the 112-bit level. A composite (hybrid) key establishment stays FIPS 140-validatable while one input comes from an approved scheme. Repeats the federal deadlines of OMB M-26-15: post-quantum key establishment by 2030-12-31 and signatures by 2031-12-31 for high value assets and high impact systems)
20. NIST — Post-Quantum Cryptography Standardization: Evaluation Criteria, Security (Call for Proposals, Section 4.A.5) — NIST. <https://csrc.nist.gov/Projects/Post-Quantum-Cryptography/Post-Quantum-Cryptography-Standardization/Evaluation-Criteria/Security-(Evaluation-Criteria)> (security categories: AES-128 key search 2^170/MAXDEPTH quantum gates, AES-192 2^233/MAXDEPTH, AES-256 2^298/MAXDEPTH; MAXDEPTH 2^40–2^96)
21. OSV advisory GHSA-2v4p-qf9q-27wj — OSV.dev. <https://osv.dev/vulnerability/GHSA-2v4p-qf9q-27wj> (modified 2026-09-25T18:00:05.270054427Z)
22. OSV advisory GO-2026-6603 — OSV.dev. <https://osv.dev/vulnerability/GO-2026-6603> (modified 2026-10-16T09:55:47.068117441Z)
23. OSV advisory GO-2026-6610 — OSV.dev. <https://osv.dev/vulnerability/GO-2026-6610> (modified 2026-10-16T09:56:04.364467528Z)
24. OSV advisory GO-2026-6611 — OSV.dev. <https://osv.dev/vulnerability/GO-2026-6611> (modified 2026-10-16T09:55:38.952277866Z)
25. OSV advisory GO-2026-6612 — OSV.dev. <https://osv.dev/vulnerability/GO-2026-6612> (modified 2026-10-16T09:55:54.129082194Z)
26. OSV advisory GO-2026-6617 — OSV.dev. <https://osv.dev/vulnerability/GO-2026-6617> (modified 2026-10-16T09:55:57.350751224Z)
27. OSV advisory GO-2026-6860 — OSV.dev. <https://osv.dev/vulnerability/GO-2026-6860> (modified 2026-10-27T21:30:04.890809062Z)
28. OSV advisory GO-2026-6866 — OSV.dev. <https://osv.dev/vulnerability/GO-2026-6866> (modified 2026-10-27T21:45:08.978077289Z)
29. P. W. Shor — Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms on a Quantum Computer (SIAM J. Comput., 1997) — SIAM. <https://doi.org/10.1137/S0097539795293172> (peer-reviewed article)
30. R. Babbush et al. — Securing Elliptic Curve Cryptocurrencies against Quantum Vulnerabilities: Resource Estimates and Mitigations (arXiv:2603.28846) — arXiv. <https://arxiv.org/abs/2603.28846> (preprint (2026-03-30, v2 2026-04-15): 256-bit ECDLP with < 1200 logical qubits and < 90 M Toffoli gates (or < 1450 and < 70 M); < 500,000 physical qubits at 10^-3 error, minutes)
31. S. Jaques, M. Naehrig, M. Roetteler, F. Virdia — Implementing Grover oracles for quantum key search on AES and LowMC (EUROCRYPT 2020; arXiv:1910.01700) — Springer / arXiv. <https://arxiv.org/abs/1910.01700> (peer-reviewed article: lower cost estimates for the AES key searches that define the NIST categories)

## Appendices: Cryptographic inventory

By origin: own code 37 (24 Shor-breakable).

| Algorithm | Parameter | Library | Quantum status | Classical status | Count | Locations | Examples |
|---|---|---|---|---|---|---|---|
| HMAC |  |  | reduced margin (Grover), approved | acceptable | 2 | 2 | bccsp/opts.go:53; bccsp/sw/keyderiv.go:21 |
| SHA-2 | SHA-512 |  | reduced margin (Grover), approved | acceptable | 2 | 2 | bccsp/sw/conf.go:13; bccsp/sw/new.go:13 |
| SHA-2 | SHA-256 |  | Grover: acceptable to NIST, below ECCG/ANSSI guidance | acceptable | 7 | 7 | bccsp/pkcs11/pkcs11.go:13; bccsp/sw/aeskey.go:19; bccsp/sw/conf.go:11 |
| SHA-3 |  |  | Grover: acceptable to NIST, below ECCG/ANSSI guidance | acceptable | 2 | 2 | bccsp/sw/conf.go:12; bccsp/sw/new.go:12 |
| ECDSA |  |  | vulnerable (Shor) | acceptable | 10 | 10 | bccsp/pkcs11/ecdsakey.go:19; bccsp/pkcs11/pkcs11.go:11; bccsp/sw/ecdsa.go:19 |
| Ed25519 | Ed25519 |  | vulnerable (Shor) | acceptable | 8 | 8 | bccsp/sw/ed25519.go:15; bccsp/sw/ed25519.go:23; bccsp/sw/ed25519key.go:18 |
| RSA |  |  | vulnerable (Shor) | acceptable | 6 | 6 | bccsp/sw/fileks.go:13; bccsp/sw/keygen.go:14; bccsp/sw/keyimport.go:12 |

_Long lists are grouped here; the full per-file list is in the JSON report, signed with the same key._

## Appendices: Input files

| File | Size | SHA-256 | Redactions |
|---|---|---|---|
| bccsp/aesopts.go | 2596 | `ca0493dd6054d092027e94af3901048adc01f16192de79807d30c85378b78543` | 0 |
| bccsp/bccsp.go | 4212 | `82df76a75ee87e4324e9c13879bc87aa471c84db6e7d689efee6174a274ff4da` | 0 |
| bccsp/ecdsaopts.go | 1499 | `ed667e09393298574ad06ed64fd2cb47d855adbceca018c0d23b24654679b649` | 0 |
| bccsp/factory/factory.go | 2478 | `a24b6d7c7ddad62bbc52aee8c7b01fb9f3a4601ef2ed943ddb84451273e08b99` | 0 |
| bccsp/factory/nopkcs11.go | 1880 | `24e6532515f4ff707d8b385cf73c4a16f3d279a782a85191b3a23772dbe07c40` | 0 |
| bccsp/factory/opts.go | 452 | `504596b431861eb308f783f1a6cb026a81f45f8f0e712411e2a9eb08ccc6cafa` | 0 |
| bccsp/factory/pkcs11.go | 2645 | `5264fbdf04137dfb54051eef9278ee7df1692e8a3c5da4c4b54b8f2f2f14f5ac` | 0 |
| bccsp/factory/pkcs11factory.go | 1453 | `c3ff2ec1dd00121e599cbccd98dce463d1cdbf22c113d0a924969ffe78eac559` | 0 |
| bccsp/factory/swfactory.go | 2196 | `d08d9a5961a76c2ded743dde029d20da7644a6fb329e3f27e95db53f2652360c` | 0 |
| bccsp/hashopts.go | 1861 | `29171b614a86730605c063fe1b05ca4abae7dbdb55765d15eb528371fc97f180` | 0 |
| bccsp/keystore.go | 1197 | `07eea30ab3a8cc6f2b94fb686cb158b64c27d95339c1603fe4153531a1e5b39c` | 0 |
| bccsp/opts.go | 10150 | `ed73949f83ce35e62e2d29bc2263b6b4e730e24f7e7e81582a32fd6b14c0c606` | 0 |
| bccsp/pkcs11/conf.go | 1330 | `1cc57eb00ecafb06d5c6d4ff8dea228eae6ed6b50f935c71451d5fa62d2bec06` | 0 |
| bccsp/pkcs11/ecdsakey.go | 2564 | `41b35f8b4e01edc52825fc73e1041ce296e6fc1d979622d7b437424f72160bd9` | 0 |
| bccsp/pkcs11/pkcs11.go | 27875 | `98a15788cd8cdca171d2c662f6e2eece206a5d8adc91994f75ddd67ffc6bbd4b` | 0 |
| bccsp/rsaopts.go | 1866 | `2a90bd507977049cd6a43eca3597569935c3f114c227ba1000dcf1113f3c4543` | 0 |
| bccsp/signer/signer.go | 2574 | `1806b0e0b2a4dc08d34a1285eeef7349b6a20bcdfa555363cdee4bf281bea41d` | 0 |
| bccsp/sw/aes.go | 5947 | `25e0c5cb3d867fa8c92f38a5e42c346538da18798f229934c0c00755fc4c057d` | 0 |
| bccsp/sw/aeskey.go | 1741 | `08b6095ec603d320e7839a36859404474eb443e640dc12c06718bb7cc5931dea` | 0 |
| bccsp/sw/conf.go | 1593 | `abcd19356cf759f0688ee38889e90bfd8ba8fc6a3b4608eb50653dde9b13e177` | 0 |
| bccsp/sw/dummyks.go | 1532 | `f6d1bc4e721f58f5471f5aef3659e3ba46fc822306d0093d556ede2df66dcb10` | 0 |
| bccsp/sw/ecdsa.go | 2224 | `f0d2594a515e856b310d5ff9ab4169d5c0a0f61fc24942e3d46e2500f928e02b` | 0 |
| bccsp/sw/ecdsakey.go | 3024 | `194f71f7e0d952ec3b87a50b5287d7bd139cb41941d75cd260e2e54ab8b01ff3` | 0 |
| bccsp/sw/ed25519.go | 1208 | `071a175c9ce2398e741a262d24325b73260f7d87ea7be622eebb9f505880d580` | 0 |
| bccsp/sw/ed25519key.go | 2555 | `5fd0b8364abab17d1378f6aba697ce2ffc0f47138f2d02056b75dd9178e9b158` | 0 |
| bccsp/sw/fileks.go | 11165 | `a0c92a6cfdcba39bd63cd9ce550b20f3a59567e53507468644c3f82330caa6db` | 0 |
| bccsp/sw/hash.go | 923 | `b5b4f1a45b5e2f3fd10d4e505ffa08ed1a087d6e9336af29357e11ceb10b4e0c` | 0 |
| bccsp/sw/impl.go | 9978 | `e86e5b101dcb085adbd489099d8566e0207e30265537f77ece063d71d0201eb0` | 0 |
| bccsp/sw/internals.go | 3357 | `855ba254295b233c474266690c944f8b5f0c425070fdcee8e5b72652d8d211d5` | 0 |
| bccsp/sw/keyderiv.go | 4131 | `fb6673a63d52fa58cdb93b3e75aeb88faf2c2c91ac3e29de9acd7f519f8ac418` | 0 |
| bccsp/sw/keygen.go | 1545 | `51177e8239b008e100259033f1075396fac4711b13d71a27d7fe1fd1697db1b4` | 0 |
| bccsp/sw/keyimport.go | 6380 | `573e238eea23ae85576a43554db460121e1ac8666fafebb84138326deedd0f25` | 0 |
| bccsp/sw/keys.go | 11408 | `cd0a974ae8900553a3f4828afcbbdd30cd479b75a51bc1723d369220e739fe3c` | 0 |
| bccsp/sw/new.go | 5934 | `fb412076a0df7836edb4a8823024134f0151607cbc8d6ac6ce27597d1cdb1c2e` | 0 |
| bccsp/sw/rsa.go | 1552 | `e3112f8c38642c19ebbb5a18c26ce471ec9fd56fae78909c4ff216d5216d2c42` | 0 |
| bccsp/sw/rsakey.go | 2754 | `93838157dd6a4eca5ecf566fa365064df1afa290b08829ae97074ccfcd473de1` | 0 |
| bccsp/utils/ecdsa.go | 2568 | `4d39accb8acba4c0041942b921c3a501e15926b19900e6ca8e5980bd5c863660` | 0 |
| common/flogging/core.go | 3184 | `ae5cbaeec703dceb5601ac4e5cf77c6c725ce02c6b1edc537d7b3bb9fc843196` | 0 |
| common/flogging/fabenc/color.go | 530 | `d32969c9dc25fa3a22acc28f2c289657433b5c06f154be3348cc8766d5ffa933` | 0 |
| common/flogging/fabenc/encoder.go | 3957 | `93ee108897c7c6dba06842927ae1701dc4dffaaea6983e0dd6f845702001cf36` | 0 |
| common/flogging/fabenc/formatter.go | 8861 | `bf6d5b76ee67a4d227fca209207f85ad41fc627de4450f8bd0f601f961d63c32` | 0 |
| common/flogging/floggingtest/logger.go | 5246 | `62d66823c89e6e9d93e5fe2712517ae65fa801885d0c4a4393931aae2f89568e` | 0 |
| common/flogging/global.go | 1876 | `d7b8402851c29934800911208966e44d8ff8c64056c7b6bdbaf91f9460931128` | 0 |
| common/flogging/httpadmin/fakes/logging.go | 4440 | `01ef7790f685bbd3884afc1e80e8e562ed54aa773b4f902bac5245e56c459e8f` | 0 |
| common/flogging/httpadmin/spec.go | 1860 | `73f3e5e5344a6f6efeb3e669f496e9010906eb2d0a36f663b266a695250a4483` | 0 |
| common/flogging/levels.go | 1565 | `aff982968eb7cf75d91c3320aba1889201187cfe4da94f10b022ebcd7eaba20a` | 0 |
| common/flogging/loggerlevels.go | 4891 | `d9ae711ddec04454937fb5c0197e90a6602af38f3dfef6d10fc27a2fcdd0a9fe` | 0 |
| common/flogging/logging.go | 5924 | `c24bcf1be2c7c246a8463974d5abff4b2768bf2bbdfbe4dd86ae706b832f044a` | 0 |
| common/flogging/metrics/observer.go | 1249 | `a9a75918b8b3ae94742ef39785c1ca947153374ca58abdd83368fb50623aa79d` | 0 |
| common/flogging/zap.go | 5211 | `0e1f06d541eed96918d47136c5d09d7a90ff64929ec223017446de85ccb929c3` | 0 |
| common/metrics/cmd/gendoc/main.go | 1641 | `0c47cc05ac4e472b424c81945358ac1cc07d21f2304610e7825ccd5ae96b7305` | 0 |
| common/metrics/disabled/provider.go | 947 | `cf31485e6ce257ecc591b9a79336a2e0fac078d4aa54565b9a3ae5c6670c4f7c` | 0 |
| common/metrics/gendoc/options.go | 4968 | `5d004d5bdc385491ccf26e12fa1e5fdd7b43348acc7b9ab16a5b53e7e3ca184b` | 0 |
| common/metrics/gendoc/table.go | 8899 | `893d08a5996bbc4a7d21c649ab44259d9d402373e2c56654ef9395cab9160b54` | 0 |
| common/metrics/metricsfakes/counter.go | 3624 | `4768783f78325d4c6590f4cd719a53ab3c61dd906a0dfc978f75622d7b1b9969` | 0 |
| common/metrics/metricsfakes/gauge.go | 4434 | `4a82092ced01547f3ad4d6abf1028a7afd1542ae133909d3ba3cf726e59d4b5c` | 0 |
| common/metrics/metricsfakes/histogram.go | 3774 | `ba7ca9aa1b4df78de4f5528e97e12708b9a42332dabd1ea9cd385abd5971697f` | 0 |
| common/metrics/metricsfakes/provider.go | 7331 | `482bdc8f1de53bdcb3553c204a0cc0eae65d0478aa209c563d1e26c9de637ed1` | 0 |
| common/metrics/namer/namer.go | 3213 | `269783a19cec93d1023653757d9880d2b688d2e8736663a002c1af0ac10e7899` | 0 |
| common/metrics/prometheus/provider.go | 1720 | `af19837203d17535cdb8f0f73e3b31ee64b59f74c1aff603f2c787f1853638ef` | 0 |
| common/metrics/provider.go | 6241 | `2e302c1f8f336fdeaa892bbb046dbfb96d9e535004d0fe964785946e495cda8c` | 0 |
| common/metrics/statsd/goruntime/collector.go | 4381 | `7a72e9edfd4a4c7073d7890e38ec4a4994b187722e5429742b6893825db17e06` | 0 |
| common/metrics/statsd/goruntime/metrics.go | 3003 | `c361fb329763628f27925de1d41e8ae1084293a6c30ddf57109f9fd690ee45e1` | 0 |
| common/metrics/statsd/provider.go | 2835 | `cc796d42a6f65cf46919a3ba217bcca739d42e0aaae470c258d4cfadae0bb219` | 0 |
| go.mod | 1877 | `f0b24cd1313a8979feb1f5e48251b2ee4ad8ad0a6c993c8f52ea581c39e41e5d` | 0 |
| healthz/checker.go | 4918 | `bec07fbe52e60910b0fc85149ea4f9b5e502f7e29ea3ad37a61f2dbf795a8d28` | 0 |
| tools/go.mod | 348 | `7b34cca11276a6eb65b446751aa74d984045b3e2fee742b56c25cfae62b3d5b5` | 0 |
