# Security & Post-Quantum Readiness Audit Report

**Project:** corda @ 80033580ecfd · R3 — public repository (passive review)
| | |
|---|---|
| Organization | QSI |
| Report date | 2026-11-06 15:38 UTC |
| Report version | 1 |
| Audit run | ab2a7138-099f-4102-a6ca-533220ad3fb9 (Document audit) |
| Analyzer engine | qsi-engine 1.3.0 |
| Risk profile | Crypto exchange, custodian or wallet |
| Content SHA-256 | `09dd82bf776b5adb6af7367e5cccfe5b259eb10fde085b2eef6d9bb38f43d5c6` |
| Signature key (Ed25519, SHA-256 fingerprint; the signature is the separate file report.sig.json) | `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e` |
> This report presents automated and documented analysis results for the stated scope. It is not a legal opinion, a certification or an attestation of compliance with any standard.

## 1. Executive summary

- Critical: **0**
- High: **3**
- Medium: **6**
- Low: **1**
- Info: **0**

- Confirmed technical vulnerability: 0
- Known vulnerable component: 0
- Confirmed configuration error: 3
- Potential cryptographic risk: 0
- Long-term post-quantum risk: 7
- Improvement recommendation: 0
- Insufficient data: 0

Mosca's inequality (x + y > z): x = 10, y = 5, z = 8 → migration would finish too late under this scenario. _z is a planning assumption chosen per risk profile, not a prediction. A cryptographically relevant quantum computer is not publicly known to exist today._

**Post-quantum maturity: Level 0 of 4 — no post-quantum cryptography.** Next step: Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

## 2. Scope and boundaries

Mode: Document audit

Repository: <https://github.com/corda/corda> @ `80033580ecfd66a22ab5e9cf5a1319d1111ade92` — evidence links open the lines at this commit.

1117 files, 5785712 bytes in total, 3 redaction(s); the per-file SHA-256 list is in appendix C.

## 3. Methodology

| Area | Status | Count | Examples |
|---|---|---|---|
| source_code | checked | 1116 | build.gradle: 776 lines scanned with 16 rule patterns and 267 registry patterns; buildCacheSettings.gradle: 16 lines scanned with 16 rule patterns and 267 registry patterns; buildSrc/build.gradle: 56 lines scanned with 16 rule patterns and 267 registry patterns |
| certificates_and_keys | checked | 1 | config/dev/corda_dev_ca.cer: certificates/keys parsed |
| tls_configuration | checked | 1 | node-api/src/main/kotlin/net/corda/nodeapi/internal/protonwrapper/netty/SSLHelper.kt: apache TLS directives parsed |
| secrets | checked | 1 | node/src/main/kotlin/net/corda/node/utilities/registration/NetworkRegistrationHelper.kt: 1 redacted value(s) not reported (comments, test modules, fixture declarations, placeholders, values the source annotates as published, or hex values not bound to a secret name) |
| entropy | checked | 1 | random-number generation: 1064 code files read with 2 macro definitions from the tree; 0 ineffective guard(s), 0 weak random-bytes provider(s), 0 weak key-generation site(s) |

_Long lists are grouped here; the full per-file list is in the JSON report, signed with the same key._

## 4. Assets examined and not examined

- None

## 5. Architecture overview

Static review of the source tree corda at 80033580ecfd66a22ab5e9cf5a1319d1111ade92. 1117 files analysed; of 3034 files, 1293 are test, fuzzing, benchmark or example code and were left out, 624 are not read by any analyzer, 0 exceed the per-file limit and 0 did not fit the total limit. Files no analyzer reads include: .ci/Dockerfile, .ci/JenkinsfileStaticAnalysis, .ci/README.md, .ci/api-current.txt, .ci/check-api-changes.sh. 33 files in build-output or dependency-cache directories (.git, .hg, .venv, __pycache__, build, dist, node_modules, target, vendor, venv) were not read. No requests were sent to the owner's systems.

## 6. Overall security posture

- Indicative posture index: **74** / 100 — _Derived from findings in scope (confirmed and potential issues weighted by severity). Indicative only; not comparable across differently scoped audits._
- Quantum-vulnerable share of inventory: 68.0%

## 7. Detailed findings

### QSI-2026-19547 — Certificate has expired (Corda Node Root CA)

- Severity: **High** · Classification: Confirmed configuration error · Confidence: High
- Affected asset: `certificate:Corda Node Root CA`
- Data source: config/dev/corda_dev_ca.cer
- Detection method: X.509 parsing (pyca/cryptography), comparison of notAfter with the analysis time (UTC).
- Analyzer: certificates 1.3.0 · 2026-11-06 15:38 UTC
- Priority score: 61.4 / 100
- CVSS v3.1: not applicable

The X.509 certificate with subject Corda Node Root CA expired on 2026-07-17 (112 days ago).

**Potential impact.** Clients that validate certificates will refuse connections; users may be trained to ignore warnings.

**Reproduction steps.**

```
openssl x509 -in config/dev/corda_dev_ca.cer -noout -enddate
```

**Evidence.**

_certificate · config/dev/corda_dev_ca.cer · line 1 · SHA-256 fcb0f5a41fc213fa274755226a8330f59bb1ce98bdd922ce41f1bb0edddbf17a_

```
Subject: C=UK,L=London,OU=corda,O=R3,CN=Corda Node Root CA
Issuer: C=UK,L=London,OU=corda,O=R3,CN=Corda Node Root CA
Serial: 368d507782c9d515
Not before: 2016-07-19T00:00:00+00:00
Not after: 2026-07-17T00:00:00+00:00
Public key: ECDSA secp256k1
Signature algorithm: 1.2.840.10045.4.3.2 (ECDSA)
Signature hash: sha256
CA: True
SAN: -
SHA-256 fingerprint: 46266a82eebee45e1497a0a53ea80b4d6d382c505bd9ada0c134340f88ef7a72
```

**Limitations of the check.** Document-based analysis: only the supplied file was examined. Deployed configuration may differ; the result reflects the file content at the recorded SHA-256.

**Recommendation.** Renew the certificate and automate renewal (e.g. ACME) with expiry monitoring.

**Retest procedure.** Re-parse the deployed certificate and confirm notAfter is in the future.

### QSI-2026-19549 — Possible hard-coded secret in core/src/main/kotlin/net/corda/core/CordaOID.kt

- Severity: **High** · Classification: Confirmed configuration error · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `file:core/src/main/kotlin/net/corda/core/CordaOID.kt`
- Data source: core/src/main/kotlin/net/corda/core/CordaOID.kt
- Detection method: Regular-expression matching of language-specific API patterns.
- Analyzer: source_code 1.3.0 · 2026-11-06 15:38 UTC
- Priority score: 47.1 / 100
- CVSS v3.1: not applicable

1 secret-like value(s) of type generic_assignment (first at line 21). Values were redacted by QSI.

**Potential impact.** Credentials in source code leak through repositories, builds and logs.

**Reproduction steps.**

```
Open line 21 in the supplied file core/src/main/kotlin/net/corda/core/CordaOID.kt and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [core/src/main/kotlin/net/corda/core/CordaOID.kt](https://github.com/corda/corda/blob/80033580ecfd66a22ab5e9cf5a1319d1111ade92/core/src/main/kotlin/net/corda/core/CordaOID.kt#L21) · line 21 · SHA-256 15e2a40ba613452d9b5f52b33a8a6c42e0a1a695ba40760dbfad8d342da8873d_

```
   21 |     const val ALIAS_PRIVATE_KEY = "[REDACTED]"
```

**Limitations of the check.** Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Move secrets to a secrets manager/environment; rotate the exposed values.

**Retest procedure.** Re-scan the source and review the call sites listed in the evidence.

### QSI-2026-19556 — Possible hard-coded secret in node/src/main/kotlin/net/corda/node/utilities/registration/HTTPNetworkRegistrationService.kt

- Severity: **High** · Classification: Confirmed configuration error · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `file:node/src/main/kotlin/net/corda/node/utilities/registration/HTTPNetworkRegistrationService.kt`
- Data source: node/src/main/kotlin/net/corda/node/utilities/registration/HTTPNetworkRegistrationService.kt
- Detection method: Regular-expression matching of language-specific API patterns.
- Analyzer: source_code 1.3.0 · 2026-11-06 15:38 UTC
- Priority score: 47.1 / 100
- CVSS v3.1: not applicable

1 secret-like value(s) of type generic_assignment (first at line 31). Values were redacted by QSI.

**Potential impact.** Credentials in source code leak through repositories, builds and logs.

**Reproduction steps.**

```
Open line 31 in the supplied file node/src/main/kotlin/net/corda/node/utilities/registration/HTTPNetworkRegistrationService.kt and inspect the quoted lines (see evidence).
```

**Evidence.**

_file_excerpt · [node/src/main/kotlin/net/corda/node/utilities/registration/HTTPNetworkRegistrationService.kt](https://github.com/corda/corda/blob/80033580ecfd66a22ab5e9cf5a1319d1111ade92/node/src/main/kotlin/net/corda/node/utilities/registration/HTTPNetworkRegistrationService.kt#L31) · line 31 · SHA-256 cd5f56090a0380acb8b9d189aa07886bb6f9022e7ef47b99ced65e02f1e65d36_

```
   31 |         private const val CENM_SUBMISSION_TOKEN = "[REDACTED]"
```

**Limitations of the check.** Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Move secrets to a secrets manager/environment; rotate the exposed values.

**Retest procedure.** Re-scan the source and review the call sites listed in the evidence.

### QSI-2026-19553 — Quantum-vulnerable ECDSA: transaction and message signing (1 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:ECDSA:transaction_signing`
- Data source: core/src/main/kotlin/net/corda/core/crypto/internal/Secp256k1SupportProvider.kt
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.3.0 · 2026-11-06 15:38 UTC
- Priority score: 35.6 / 100
- CVSS v3.1: not applicable

6 reference(s) to ECDSA across 1 file(s), e.g. core/src/main/kotlin/net/corda/core/crypto/internal/Secp256k1SupportProvider.kt:32. Role, judged from paths, function names and nearby code: transaction and message signing. A CRQC derives the private key from a public key that is already known (on chain after the first spend, in reused addresses): funds and approvals controlled by these keys need a migration path.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open core/src/main/kotlin/net/corda/core/crypto/internal/Secp256k1SupportProvider.kt:32 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [core/src/main/kotlin/net/corda/core/crypto/internal/Secp256k1SupportProvider.kt](https://github.com/corda/corda/blob/80033580ecfd66a22ab5e9cf5a1319d1111ade92/core/src/main/kotlin/net/corda/core/crypto/internal/Secp256k1SupportProvider.kt#L32) · line 32 · SHA-256 1cc21aed7f8b5ffe0ffeedc36b2344d08e907e1568da5d182bd7c20413b9fd57_

```
   31 |  */
   32 | class Secp256k1SupportProvider : Provider("Secp256k1Support", "1.0", "Augmenting SunEC with support for the secp256k1 curve via BC") {
   33 |     init {
```

_file_excerpt · [core/src/main/kotlin/net/corda/core/crypto/internal/Secp256k1SupportProvider.kt](https://github.com/corda/corda/blob/80033580ecfd66a22ab5e9cf5a1319d1111ade92/core/src/main/kotlin/net/corda/core/crypto/internal/Secp256k1SupportProvider.kt#L66) · line 66 · SHA-256 7ba0ac1a0c89777dc58c9b13d171c61b03955c3846c7743b200fac509bf898dc_

```
   65 |                 if (!::bc.isInitialized) {
   66 |                     bc = Signature.getInstance("SHA256withECDSA", cordaBouncyCastleProvider)
   67 |                 }
```

_file_excerpt · [core/src/main/kotlin/net/corda/core/crypto/internal/Secp256k1SupportProvider.kt](https://github.com/corda/corda/blob/80033580ecfd66a22ab5e9cf5a1319d1111ade92/core/src/main/kotlin/net/corda/core/crypto/internal/Secp256k1SupportProvider.kt#L76) · line 76 · SHA-256 b78449aeb3bcaf9e2aec6fef912446b66611b7eb7810803f8a43a4a4f810d9d4_

```
   75 |             if (!::sunEc.isInitialized) {
   76 |                 sunEc = Signature.getInstance("SHA256withECDSA", sunEcProvider)
   77 |             }
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains adopt them.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-19550 — Quantum-vulnerable RSA: role not determined (2 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:RSA:general`
- Data source: core/src/main/kotlin/net/corda/core/crypto/Crypto.kt
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.3.0 · 2026-11-06 15:38 UTC
- Priority score: 34.2 / 100
- CVSS v3.1: not applicable

3 reference(s) to RSA across 2 file(s), e.g. core/src/main/kotlin/net/corda/core/crypto/Crypto.kt:92. Role, judged from paths, function names and nearby code: role not determined. The code does not show what the keys protect; review decides the priority.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open core/src/main/kotlin/net/corda/core/crypto/Crypto.kt:92 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [core/src/main/kotlin/net/corda/core/crypto/Crypto.kt](https://github.com/corda/corda/blob/80033580ecfd66a22ab5e9cf5a1319d1111ade92/core/src/main/kotlin/net/corda/core/crypto/Crypto.kt#L92) · line 92 · SHA-256 fedad570e631922d0d8aeddf511a64b7db1f895249129dac52bdebbb1c283fe7_

```
   91 |             "RSA",
   92 |             "SHA256withRSA",
   93 |             null,
```

_file_excerpt · [node-api/src/main/kotlin/net/corda/nodeapi/internal/cryptoservice/DefaultCryptoService.kt](https://github.com/corda/corda/blob/80033580ecfd66a22ab5e9cf5a1319d1111ade92/node-api/src/main/kotlin/net/corda/nodeapi/internal/cryptoservice/DefaultCryptoService.kt#L224) · line 224 · SHA-256 d2836749b7a6179e0326f75d1d602413742ec0049b178bec52d7b5cdede0153c_

```
  223 |             Crypto.ECDSA_SECP256K1_SHA256 -> keyPairGenerator.initialize(ECGenParameterSpec("secp256k1"))
  224 |             Crypto.RSA_SHA256 -> keyPairGenerator.initialize(scheme.keySize!!)
  225 |             else -> throw IllegalArgumentException("No mapping for scheme ID ${scheme.schemeNumberID}")
```

_file_excerpt · [node-api/src/main/kotlin/net/corda/nodeapi/internal/cryptoservice/DefaultCryptoService.kt](https://github.com/corda/corda/blob/80033580ecfd66a22ab5e9cf5a1319d1111ade92/node-api/src/main/kotlin/net/corda/nodeapi/internal/cryptoservice/DefaultCryptoService.kt#L232) · line 232 · SHA-256 9c9d73cbab4b1b994cdec67bb3c1464d3977dc0a265c5d585f4d8f3655b2c00b_

```
  231 |         Crypto.ECDSA_SECP256R1_SHA256, Crypto.ECDSA_SECP256K1_SHA256 -> "EC"
  232 |         Crypto.RSA_SHA256 -> "RSA"
  233 |         else -> throw IllegalArgumentException("No algorithm for scheme ID ${scheme.schemeNumberID}")
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it; introduce an abstraction layer for crypto-agility.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-19551 — Quantum-vulnerable ECDSA: role not determined (4 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:ECDSA:general`
- Data source: core/src/main/kotlin/net/corda/core/crypto/Crypto.kt
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.3.0 · 2026-11-06 15:38 UTC
- Priority score: 34.2 / 100
- CVSS v3.1: not applicable

15 reference(s) to ECDSA across 4 file(s), e.g. core/src/main/kotlin/net/corda/core/crypto/Crypto.kt:103. Role, judged from paths, function names and nearby code: role not determined. The code does not show what the keys protect; review decides the priority.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open core/src/main/kotlin/net/corda/core/crypto/Crypto.kt:103 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [core/src/main/kotlin/net/corda/core/crypto/Crypto.kt](https://github.com/corda/corda/blob/80033580ecfd66a22ab5e9cf5a1319d1111ade92/core/src/main/kotlin/net/corda/core/crypto/Crypto.kt#L103) · line 103 · SHA-256 ddc1e3c37f91880d7b9ee05f3f9204217753318c2edc93f6edfa4fd85d35b2c0_

```
  102 |             "ECDSA_SECP256K1_SHA256",
  103 |             AlgorithmIdentifier(X9ObjectIdentifiers.ecdsa_with_SHA256, SECObjectIdentifiers.secp256k1),
  104 |             listOf(AlgorithmIdentifier(X9ObjectIdentifiers.id_ecPublicKey, SECObjectIdentifiers.secp256k1)),
```

_file_excerpt · [core/src/main/kotlin/net/corda/core/crypto/Crypto.kt](https://github.com/corda/corda/blob/80033580ecfd66a22ab5e9cf5a1319d1111ade92/core/src/main/kotlin/net/corda/core/crypto/Crypto.kt#L104) · line 104 · SHA-256 0cbd5b8d15e381e9030d404c63c1b8c0fc81f8ca2710def539f4e6ff1f9a162b_

```
  103 |             AlgorithmIdentifier(X9ObjectIdentifiers.ecdsa_with_SHA256, SECObjectIdentifiers.secp256k1),
  104 |             listOf(AlgorithmIdentifier(X9ObjectIdentifiers.id_ecPublicKey, SECObjectIdentifiers.secp256k1)),
  105 |             cordaBouncyCastleProvider.name,
```

_file_excerpt · [core/src/main/kotlin/net/corda/core/crypto/Crypto.kt](https://github.com/corda/corda/blob/80033580ecfd66a22ab5e9cf5a1319d1111ade92/core/src/main/kotlin/net/corda/core/crypto/Crypto.kt#L107) · line 107 · SHA-256 b74a0bc63bf81f600cf4dfe9064d3b056d4adea9d36160d192cbbfb7a55f0c2a_

```
  106 |             "EC",
  107 |             "SHA256withECDSA",
  108 |             ECNamedCurveTable.getParameterSpec("secp256k1"),
```

_file_excerpt · [node-api/src/main/kotlin/net/corda/nodeapi/internal/crypto/NOT_YET_REGISTERED_MARKER_KEYS_AND_CERTS.kt](https://github.com/corda/corda/blob/80033580ecfd66a22ab5e9cf5a1319d1111ade92/node-api/src/main/kotlin/net/corda/nodeapi/internal/crypto/NOT_YET_REGISTERED_MARKER_KEYS_AND_CERTS.kt#L12) · line 12 · SHA-256 bdbdc27ab1cd2296d6837cc2810b785b8144f1c968acfdac4389a25bae6d9af5_

```
   11 | object NOT_YET_REGISTERED_MARKER_KEYS_AND_CERTS {
   12 |     val ECDSAR1_KEYPAIR by lazy { Crypto.deriveKeyPairFromEntropy(Crypto.ECDSA_SECP256R1_SHA256, BigInteger.valueOf(0)) }
   13 |     val ECDSAR1_CERT by lazy { createSelfSignedCACertificate(X500Principal("CN=DUMMY"), ECDSAR1_KEYPAIR) }
```

_file_excerpt · [node-api/src/main/kotlin/net/corda/nodeapi/internal/cryptoservice/CryptoService.kt](https://github.com/corda/corda/blob/80033580ecfd66a22ab5e9cf5a1319d1111ade92/node-api/src/main/kotlin/net/corda/nodeapi/internal/cryptoservice/CryptoService.kt#L127) · line 127 · SHA-256 54855cad7202e394b18d1beb70ed5aae4659c901d4a5decea0edff6bbdd28fa6_

```
  126 |      */
  127 |     fun defaultWrappingSignatureScheme(): SignatureScheme = Crypto.ECDSA_SECP256R1_SHA256
  128 | 
```

_file_excerpt · [node-api/src/main/kotlin/net/corda/nodeapi/internal/cryptoservice/DefaultCryptoService.kt](https://github.com/corda/corda/blob/80033580ecfd66a22ab5e9cf5a1319d1111ade92/node-api/src/main/kotlin/net/corda/nodeapi/internal/cryptoservice/DefaultCryptoService.kt#L222) · line 222 · SHA-256 2369170574ed87d8d55ee2b51e8ae9357f1d3b1421311738f3fc2d27c6426824_

```
  221 |         when (scheme) {
  222 |             Crypto.ECDSA_SECP256R1_SHA256 -> keyPairGenerator.initialize(ECGenParameterSpec("secp256r1"))
  223 |             Crypto.ECDSA_SECP256K1_SHA256 -> keyPairGenerator.initialize(ECGenParameterSpec("secp256k1"))
```

_file_excerpt · [node-api/src/main/kotlin/net/corda/nodeapi/internal/cryptoservice/DefaultCryptoService.kt](https://github.com/corda/corda/blob/80033580ecfd66a22ab5e9cf5a1319d1111ade92/node-api/src/main/kotlin/net/corda/nodeapi/internal/cryptoservice/DefaultCryptoService.kt#L223) · line 223 · SHA-256 b2a0b1eb7158aa9f9c8bf2b0050285e85dfac7afb1ac65b94b8947cd70aa9bcc_

```
  222 |             Crypto.ECDSA_SECP256R1_SHA256 -> keyPairGenerator.initialize(ECGenParameterSpec("secp256r1"))
  223 |             Crypto.ECDSA_SECP256K1_SHA256 -> keyPairGenerator.initialize(ECGenParameterSpec("secp256k1"))
  224 |             Crypto.RSA_SHA256 -> keyPairGenerator.initialize(scheme.keySize!!)
```

_file_excerpt · [node-api/src/main/kotlin/net/corda/nodeapi/internal/cryptoservice/DefaultCryptoService.kt](https://github.com/corda/corda/blob/80033580ecfd66a22ab5e9cf5a1319d1111ade92/node-api/src/main/kotlin/net/corda/nodeapi/internal/cryptoservice/DefaultCryptoService.kt#L231) · line 231 · SHA-256 4d4226acca743a76d511d9ef4d8bd5110e01991d13e1da16956659ecca1fc237_

```
  230 |     private fun keyAlgorithmFromScheme(scheme: SignatureScheme): String = when (scheme) {
  231 |         Crypto.ECDSA_SECP256R1_SHA256, Crypto.ECDSA_SECP256K1_SHA256 -> "EC"
  232 |         Crypto.RSA_SHA256 -> "RSA"
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it; introduce an abstraction layer for crypto-agility.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-19552 — Quantum-vulnerable Ed25519: role not determined (1 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:Ed25519:general`
- Data source: core/src/main/kotlin/net/corda/core/crypto/Crypto.kt
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.3.0 · 2026-11-06 15:38 UTC
- Priority score: 34.2 / 100
- CVSS v3.1: not applicable

11 reference(s) to Ed25519 across 1 file(s), e.g. core/src/main/kotlin/net/corda/core/crypto/Crypto.kt:4. Role, judged from paths, function names and nearby code: role not determined. The code does not show what the keys protect; review decides the priority.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open core/src/main/kotlin/net/corda/core/crypto/Crypto.kt:4 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [core/src/main/kotlin/net/corda/core/crypto/Crypto.kt](https://github.com/corda/corda/blob/80033580ecfd66a22ab5e9cf5a1319d1111ade92/core/src/main/kotlin/net/corda/core/crypto/Crypto.kt#L4) · line 4 · SHA-256 099c04d861bc4fde1ab02770b565be944107d24083c872e77064a71db8af74f0_

```
    3 | import net.corda.core.CordaOID
    4 | import net.corda.core.crypto.Crypto.EDDSA_ED25519_SHA512
    5 | import net.corda.core.crypto.internal.AliasPrivateKey
```

_file_excerpt · [core/src/main/kotlin/net/corda/core/crypto/Crypto.kt](https://github.com/corda/corda/blob/80033580ecfd66a22ab5e9cf5a1319d1111ade92/core/src/main/kotlin/net/corda/core/crypto/Crypto.kt#L134) · line 134 · SHA-256 84bf586c243b183196895373ad877db448d5f8df6423aeb2e9d0a95825a80f39_

```
  133 |     @JvmField
  134 |     val EDDSA_ED25519_SHA512: SignatureScheme = SignatureScheme(
  135 |             4,
```

_file_excerpt · [core/src/main/kotlin/net/corda/core/crypto/Crypto.kt](https://github.com/corda/corda/blob/80033580ecfd66a22ab5e9cf5a1319d1111ade92/core/src/main/kotlin/net/corda/core/crypto/Crypto.kt#L136) · line 136 · SHA-256 4c3400ed0a6b6564fcc0a8dd1e44ad2a57d141abfed4c4a8610a3d5eec24ea1f_

```
  135 |             4,
  136 |             "EDDSA_ED25519_SHA512",
  137 |             AlgorithmIdentifier(EdECObjectIdentifiers.id_Ed25519, null),
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it; introduce an abstraction layer for crypto-agility.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-19554 — Quantum-vulnerable ECDSA: authentication and identity (certificates, tokens, device attestation) (1 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:ECDSA:authentication`
- Data source: node-api/src/main/kotlin/net/corda/nodeapi/internal/crypto/X509Utilities.kt
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.3.0 · 2026-11-06 15:38 UTC
- Priority score: 34.2 / 100
- CVSS v3.1: not applicable

1 reference(s) to ECDSA across 1 file(s), e.g. node-api/src/main/kotlin/net/corda/nodeapi/internal/crypto/X509Utilities.kt:75. Role, judged from paths, function names and nearby code: authentication and identity (certificates, tokens, device attestation). Short-lived authentication stays safe until a CRQC exists; long-lived identities (device attestation, CA and SSH keys) need a plan earlier.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open node-api/src/main/kotlin/net/corda/nodeapi/internal/crypto/X509Utilities.kt:75 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [node-api/src/main/kotlin/net/corda/nodeapi/internal/crypto/X509Utilities.kt](https://github.com/corda/corda/blob/80033580ecfd66a22ab5e9cf5a1319d1111ade92/node-api/src/main/kotlin/net/corda/nodeapi/internal/crypto/X509Utilities.kt#L75) · line 75 · SHA-256 796a593d0cda664eeeb5394fecebc03132ffcb31700f4e83e48ac621ad2fcffa_

```
   74 |     val DEFAULT_IDENTITY_SIGNATURE_SCHEME = Crypto.EDDSA_ED25519_SHA512
   75 |     val DEFAULT_TLS_SIGNATURE_SCHEME = Crypto.ECDSA_SECP256R1_SHA256
   76 | 
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Keep credentials short-lived and plan ML-DSA certificates, tokens and keys as the ecosystem supports them.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-19555 — Quantum-vulnerable Ed25519: authentication and identity (certificates, tokens, device attestation) (1 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:Ed25519:authentication`
- Data source: node-api/src/main/kotlin/net/corda/nodeapi/internal/crypto/X509Utilities.kt
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.3.0 · 2026-11-06 15:38 UTC
- Priority score: 34.2 / 100
- CVSS v3.1: not applicable

1 reference(s) to Ed25519 across 1 file(s), e.g. node-api/src/main/kotlin/net/corda/nodeapi/internal/crypto/X509Utilities.kt:74. Role, judged from paths, function names and nearby code: authentication and identity (certificates, tokens, device attestation). Short-lived authentication stays safe until a CRQC exists; long-lived identities (device attestation, CA and SSH keys) need a plan earlier.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open node-api/src/main/kotlin/net/corda/nodeapi/internal/crypto/X509Utilities.kt:74 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [node-api/src/main/kotlin/net/corda/nodeapi/internal/crypto/X509Utilities.kt](https://github.com/corda/corda/blob/80033580ecfd66a22ab5e9cf5a1319d1111ade92/node-api/src/main/kotlin/net/corda/nodeapi/internal/crypto/X509Utilities.kt#L74) · line 74 · SHA-256 450c55652268000b11d9f2c010decf2eeee63717aa406c24b7813f5ff3947993_

```
   73 |     // schemes (for instance `UtimacoCryptoService.DEFAULT_IDENTITY_SIGNATURE_SCHEME`).
   74 |     val DEFAULT_IDENTITY_SIGNATURE_SCHEME = Crypto.EDDSA_ED25519_SHA512
   75 |     val DEFAULT_TLS_SIGNATURE_SCHEME = Crypto.ECDSA_SECP256R1_SHA256
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Keep credentials short-lived and plan ML-DSA certificates, tokens and keys as the ecosystem supports them.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-19548 — Quantum-vulnerable ECDSA key in certificate (Corda Node Root CA)

- Severity: **Low** · Classification: Long-term post-quantum risk · Confidence: High
- Affected asset: `certificate:Corda Node Root CA`
- Data source: config/dev/corda_dev_ca.cer
- Detection method: X.509 public key algorithm identification.
- Analyzer: certificates 1.3.0 · 2026-11-06 15:38 UTC
- Priority score: 36.5 / 100
- CVSS v3.1: not applicable

The certificate Corda Node Root CA uses a ECDSA secp256k1 public key, valid until 2026-07-17. ECDSA is broken by Shor's algorithm on a CRQC.

**Potential impact.** For authentication, risk materializes only once a CRQC exists while the key/certificate is still trusted. Certificates are short-lived, so the main concern is the PKI and long-lived roots/intermediates.

**Reproduction steps.**

```
openssl x509 -in config/dev/corda_dev_ca.cer -noout -text | grep -A2 'Public Key Algorithm'
```

**Evidence.**

_certificate · config/dev/corda_dev_ca.cer · line 1 · SHA-256 fcb0f5a41fc213fa274755226a8330f59bb1ce98bdd922ce41f1bb0edddbf17a_

```
Subject: C=UK,L=London,OU=corda,O=R3,CN=Corda Node Root CA
Issuer: C=UK,L=London,OU=corda,O=R3,CN=Corda Node Root CA
Serial: 368d507782c9d515
Not before: 2016-07-19T00:00:00+00:00
Not after: 2026-07-17T00:00:00+00:00
Public key: ECDSA secp256k1
Signature algorithm: 1.2.840.10045.4.3.2 (ECDSA)
Signature hash: sha256
CA: True
SAN: -
SHA-256 fingerprint: 46266a82eebee45e1497a0a53ea80b4d6d382c505bd9ada0c134340f88ef7a72
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability.

**Recommendation.** Track in the PQC inventory; prefer short certificate lifetimes; follow CA/Browser Forum and NIST PQC transition guidance for ML-DSA certificates.

**Retest procedure.** Re-audit once PQC or hybrid certificates are deployed.


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
| **transaction and message signing** | ECDSA (1) | QSI-2026-19553 | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains adopt them |
| **authentication and identity (certificates, tokens, device attestation)** | ECDSA (1), Ed25519 (1) | QSI-2026-19554, QSI-2026-19555 | Keep credentials short-lived and plan ML-DSA certificates, tokens and keys as the ecosystem supports them |
| **role not determined** | ECDSA (4), RSA (2), Ed25519 (1) | QSI-2026-19550, QSI-2026-19551, QSI-2026-19552 | Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it; introduce an abstraction layer for crypto-agility |

_Roles are judged from file paths, function names and the code around each match; review confirms them. Root-of-trust keys and wrapped keys come first: they are hard to replace or can be recorded today._
No readiness questionnaire was completed for this project.

### Quantum algorithms relevant to this inventory

| Quantum algorithm | Effect | Attack model | Inventoried algorithms (rows) | What it means for this audit |
|---|---|---|---|---|
| Shor's algorithm — factoring | breaks | Q1 | RSA (2) | Breaks RSA at every key length: a longer modulus only raises the cost polynomially. Plan migration to ML-KEM (or a hybrid) for key establishment and ML-DSA / SLH-DSA for signatures; start with keys protecting data that must stay confidential for years (harvest now, decrypt later) and with long-lived signatures. |
| Shor's algorithm — elliptic-curve discrete logarithms | breaks | Q1 | ECDSA (12), Ed25519 (2), X25519 (1) | Elliptic-curve keys are expected to fall before RSA keys of comparable classical strength. On blockchains, coins whose public key is already on chain (reused addresses, pay-to-public-key and Taproot outputs) are exposed first; plan the move to post-quantum signatures and avoid key reuse in the meantime. |
| Grover's algorithm — key search and preimages | weakens (larger keys restore the margin) | Q1 | AES-128 (2), HMAC (1), SHA-2 (4) | Not a break. 256-bit keys (AES-256, ChaCha20) keep a comfortable margin; AES-128 meets NIST category 1, while some authorities ask for 256-bit keys in quantum-resistant contexts (see the AES-128 entry). Prefer 256-bit keys for long-lived data; 256-bit hashes need no change for preimage resistance. |
| Brassard–Høyer–Tapp — collision search | weakens (larger keys restore the margin) | Q1 | SHA-2 (4) | 256-bit hashes (SHA-256, SHA3-256) remain adequate for collision resistance; 160-bit hashes are already weak classically (SHA-1 collisions are practical). Use 384/512-bit hashes where NIST categories 4–5 are required. |
| Simon's algorithm — superposition attacks on symmetric constructions | only with superposition queries | Q2 | GCM mode (1) | No action for ordinary deployments of AES-GCM or CBC-MAC — the attack model does not apply. Record it as a model assumption; see the offline variant for Even–Mansour-type designs. |

_Effects: breaks — replace the algorithm; weakens — larger keys or outputs restore the margin; included in standard parameters — no action at standard parameter sets; only with superposition queries — not applicable to ordinary deployments._


## 9. Limitations and assumptions

- This report presents automated and documented analysis results for the stated scope. It is not a legal opinion, a certification or an attestation of compliance with any standard.
- z is a planning assumption chosen per risk profile, not a prediction. A cryptographically relevant quantum computer is not publicly known to exist today.

## 10. Remediation plan / Priorities for 30, 60 and 90 days

### 30 days

| Priority | ID | Action | Type | Closure criteria |
|---|---|---|---|---|
| P1 | QSI-2026-19547 | Renew the certificate for Corda Node Root CA and enable automated renewal with alerting ≥ 30 days before expiry. | root-cause fix | The deployed certificate is valid and renewal is automated. |
| P1 | QSI-2026-19549 | Rotate and remove secrets found in core/src/main/kotlin/net/corda/core/CordaOID.kt. | root-cause fix | Secret scanner reports no secrets; old values revoked. |
| P1 | QSI-2026-19556 | Rotate and remove secrets found in node/src/main/kotlin/net/corda/node/utilities/registration/HTTPNetworkRegistrationService.kt. | root-cause fix | Secret scanner reports no secrets; old values revoked. |
### 60 days

| Priority | ID | Action | Type | Closure criteria |
|---|---|---|---|---|
### 90 days

| Priority | ID | Action | Type | Closure criteria |
|---|---|---|---|---|
| P3 | QSI-2026-19553 | Add ECDSA usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-19550 | Add RSA usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-19551 | Add ECDSA usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-19552 | Add Ed25519 usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-19554 | Add ECDSA usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-19555 | Add Ed25519 usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-19548 | Add ECDSA usages at certificate:Corda Node Root CA to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P4 | QSI-2026-19553 | Plan migration of ECDSA to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-19550 | Plan migration of RSA to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-19551 | Plan migration of ECDSA to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-19552 | Plan migration of Ed25519 to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-19554 | Plan migration of ECDSA to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-19555 | Plan migration of Ed25519 to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-19548 | Plan migration of ECDSA to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. or a hybrid scheme in use. |

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
9. D. R. Simon — On the Power of Quantum Computation (SIAM J. Comput. 26, 1997) — SIAM. <https://doi.org/10.1137/S0097539796298637> (peer-reviewed article)
10. FIPS 203 — Module-Lattice-Based Key-Encapsulation Mechanism Standard (ML-KEM) — NIST. <https://csrc.nist.gov/pubs/fips/203/final> (final (August 2024))
11. FIPS 204 — Module-Lattice-Based Digital Signature Standard (ML-DSA) — NIST. <https://csrc.nist.gov/pubs/fips/204/final> (final (August 2024))
12. FIPS 205 — Stateless Hash-Based Digital Signature Standard (SLH-DSA) — NIST. <https://csrc.nist.gov/pubs/fips/205/final> (final (August 2024))
13. G. Brassard, P. Høyer, A. Tapp — Quantum Algorithm for the Collision Problem (LATIN '98; arXiv:quant-ph/9705002) — Springer / arXiv. <https://arxiv.org/abs/quant-ph/9705002> (peer-reviewed article: collisions of r-to-one functions in O((N/r)^{1/3}) expected evaluations)
14. H. Kuwakado, M. Morii — Quantum distinguisher between the 3-round Feistel cipher and the random permutation (IEEE ISIT 2010) — IEEE. <https://ieeexplore.ieee.org/document/5513654> (peer-reviewed conference paper)
15. J. Proos, C. Zalka — Shor's discrete logarithm quantum algorithm for elliptic curves (Quantum Inf. Comput. 3(4), 2003; arXiv:quant-ph/0301141) — Quantum Information & Computation. <https://doi.org/10.26421/QIC3.4-3> (peer-reviewed article)
16. L. K. Grover — A fast quantum mechanical algorithm for database search (STOC 1996) — ACM. <https://doi.org/10.1145/237814.237866> (peer-reviewed article)
17. M. Amy et al. — Estimating the cost of generic quantum pre-image attacks on SHA-2 and SHA-3 (SAC 2016; arXiv:1603.09383) — Springer / arXiv. <https://arxiv.org/abs/1603.09383> (peer-reviewed article: SHA-256 about 2^153.8 surface-code cycles on 2^12.6 logical qubits; SHA3-256 about 2^146.5 cycles on 2^20)
18. M. Cain et al. — Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits (arXiv:2603.28627) — arXiv. <https://arxiv.org/abs/2603.28627> (preprint (2026-03-30): P-256 in a few days with 26,000 physical neutral-atom qubits; RSA-2048 one to two orders of magnitude longer)
19. M. Kaplan, G. Leurent, A. Leverrier, M. Naya-Plasencia — Breaking Symmetric Cryptosystems using Quantum Period Finding (CRYPTO 2016; arXiv:1602.05973) — Springer / arXiv. <https://arxiv.org/abs/1602.05973> (peer-reviewed article: superposition-query forgeries on CBC-MAC, PMAC, GMAC, GCM, OCB)
20. M. Mosca — Cybersecurity in an Era with Quantum Computers: Will We Be Ready? (IEEE Security & Privacy, 2018) — IEEE. <https://doi.org/10.1109/MSP.2018.3761723> (peer-reviewed article; source of the x + y > z migration inequality)
21. M. Roetteler, M. Naehrig, K. Svore, K. Lauter — Quantum resource estimates for computing elliptic curve discrete logarithms (ASIACRYPT 2017) — IACR / arXiv. <https://arxiv.org/abs/1706.06752> (peer-reviewed article: at most 9n + 2⌈log2 n⌉ + 10 qubits and 448 n^3 log2 n + 4090 n^3 Toffoli gates)
22. NIST IR 8547 — Transition to Post-Quantum Cryptography Standards — NIST. <https://csrc.nist.gov/pubs/ir/8547/final> (final (2026-10-27; the initial public draft of November 2024 is obsoleted). Tables 2 and 4: ECDSA, EdDSA and RSA signatures, finite-field and elliptic-curve DH and MQV, and RSA key establishment are deprecated after 2030 and disallowed after 2035 at every key size — the draft deprecated only the 112-bit level. A composite (hybrid) key establishment stays FIPS 140-validatable while one input comes from an approved scheme. Repeats the federal deadlines of OMB M-26-15: post-quantum key establishment by 2030-12-31 and signatures by 2031-12-31 for high value assets and high impact systems)
23. NIST SP 800-57 Part 1 Rev. 5 — Recommendation for Key Management — NIST. <https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final> (final (2020))
24. NIST — Post-Quantum Cryptography Standardization: Evaluation Criteria, Security (Call for Proposals, Section 4.A.5) — NIST. <https://csrc.nist.gov/Projects/Post-Quantum-Cryptography/Post-Quantum-Cryptography-Standardization/Evaluation-Criteria/Security-(Evaluation-Criteria)> (security categories: AES-128 key search 2^170/MAXDEPTH quantum gates, AES-192 2^233/MAXDEPTH, AES-256 2^298/MAXDEPTH; MAXDEPTH 2^40–2^96)
25. OWASP Application Security Verification Standard — OWASP. <https://owasp.org/www-project-application-security-verification-standard/> (living standard — check the project page for the current version)
26. P. W. Shor — Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms on a Quantum Computer (SIAM J. Comput., 1997) — SIAM. <https://doi.org/10.1137/S0097539795293172> (peer-reviewed article)
27. R. Babbush et al. — Securing Elliptic Curve Cryptocurrencies against Quantum Vulnerabilities: Resource Estimates and Mitigations (arXiv:2603.28846) — arXiv. <https://arxiv.org/abs/2603.28846> (preprint (2026-03-30, v2 2026-04-15): 256-bit ECDLP with < 1200 logical qubits and < 90 M Toffoli gates (or < 1450 and < 70 M); < 500,000 physical qubits at 10^-3 error, minutes)
28. S. Jaques, M. Naehrig, M. Roetteler, F. Virdia — Implementing Grover oracles for quantum key search on AES and LowMC (EUROCRYPT 2020; arXiv:1910.01700) — Springer / arXiv. <https://arxiv.org/abs/1910.01700> (peer-reviewed article: lower cost estimates for the AES key searches that define the NIST categories)

## Appendices: Cryptographic inventory

By origin: keys and certificates 2 (1 Shor-breakable) · own code 23 (16 Shor-breakable).

| Algorithm | Parameter | Library | Location | Quantum status | Classical status |
|---|---|---|---|---|---|
| HMAC | HMAC-SHA-512 |  | core/src/main/kotlin/net/corda/core/crypto/Crypto.kt:910 | reduced margin (Grover), approved | acceptable |
| AES-128 | AES-128 |  | node-api/src/main/kotlin/net/corda/nodeapi/internal/ArtemisTcpTransport.kt:22 | Grover: acceptable to NIST, below ECCG/ANSSI guidance | acceptable |
| AES-128 | AES-128 |  | tools/loadtest/src/main/kotlin/net/corda/loadtest/Disruption.kt:71 | Grover: acceptable to NIST, below ECCG/ANSSI guidance | acceptable |
| SHA-2 | SHA-256 |  | config/dev/corda_dev_ca.cer (line 1) | Grover: acceptable to NIST, below ECCG/ANSSI guidance | acceptable |
| SHA-2 | SHA-256 |  | core/src/main/kotlin/net/corda/core/internal/InternalUtils.kt:192 | Grover: acceptable to NIST, below ECCG/ANSSI guidance | acceptable |
| SHA-2 | SHA-256 |  | node/src/main/kotlin/net/corda/node/services/messaging/InterceptingActiveMQJAASSecurityManager.kt:186 | Grover: acceptable to NIST, below ECCG/ANSSI guidance | acceptable |
| SHA-2 | SHA-256 |  | node/src/main/kotlin/net/corda/node/services/persistence/AesDbEncryptionService.kt:129 | Grover: acceptable to NIST, below ECCG/ANSSI guidance | acceptable |
| GCM mode |  |  | node-api/src/main/kotlin/net/corda/nodeapi/internal/crypto/AesEncryption.kt:32 | n/a | acceptable |
| ECDSA | secp256k1 |  | config/dev/corda_dev_ca.cer (line 1) — Corda Node Root CA | vulnerable (Shor) | acceptable |
| ECDSA | secp256k1 |  | core/src/main/kotlin/net/corda/core/crypto/Crypto.kt:103 | vulnerable (Shor) | acceptable |
| ECDSA |  |  | core/src/main/kotlin/net/corda/core/crypto/Crypto.kt:107 | vulnerable (Shor) | acceptable |
| ECDSA | P-256 |  | core/src/main/kotlin/net/corda/core/crypto/Crypto.kt:118 | vulnerable (Shor) | acceptable |
| ECDSA | secp256k1 |  | core/src/main/kotlin/net/corda/core/crypto/internal/Secp256k1SupportProvider.kt:32 | vulnerable (Shor) | acceptable |
| ECDSA |  |  | core/src/main/kotlin/net/corda/core/crypto/internal/Secp256k1SupportProvider.kt:66 | vulnerable (Shor) | acceptable |
| ECDSA | P-256 |  | node-api/src/main/kotlin/net/corda/nodeapi/internal/crypto/NOT_YET_REGISTERED_MARKER_KEYS_AND_CERTS.kt:12 | vulnerable (Shor) | acceptable |
| ECDSA | P-256 |  | node-api/src/main/kotlin/net/corda/nodeapi/internal/crypto/X509Utilities.kt:75 | vulnerable (Shor) | acceptable |
| ECDSA | P-256 |  | node-api/src/main/kotlin/net/corda/nodeapi/internal/cryptoservice/CryptoService.kt:127 | vulnerable (Shor) | acceptable |
| ECDSA | P-256 |  | node-api/src/main/kotlin/net/corda/nodeapi/internal/cryptoservice/DefaultCryptoService.kt:222 | vulnerable (Shor) | acceptable |
| ECDSA |  |  | node-api/src/main/kotlin/net/corda/nodeapi/internal/cryptoservice/DefaultCryptoService.kt:223 | vulnerable (Shor) | acceptable |
| ECDSA | secp256k1 |  | node-api/src/main/kotlin/net/corda/nodeapi/internal/cryptoservice/DefaultCryptoService.kt:223 | vulnerable (Shor) | acceptable |
| Ed25519 | Ed25519 |  | core/src/main/kotlin/net/corda/core/crypto/Crypto.kt:4 | vulnerable (Shor) | acceptable |
| Ed25519 | Ed25519 |  | node-api/src/main/kotlin/net/corda/nodeapi/internal/crypto/X509Utilities.kt:74 | vulnerable (Shor) | acceptable |
| RSA |  |  | core/src/main/kotlin/net/corda/core/crypto/Crypto.kt:92 | vulnerable (Shor) | acceptable |
| RSA |  |  | node-api/src/main/kotlin/net/corda/nodeapi/internal/cryptoservice/DefaultCryptoService.kt:224 | vulnerable (Shor) | acceptable |
| X25519 |  |  | core/src/main/kotlin/net/corda/core/crypto/internal/Curve25519.kt | vulnerable (Shor) | acceptable |

## Appendices: Input files

| File | Size | SHA-256 | Redactions |
|---|---|---|---|
| build.gradle | 37471 | `0b5fb42156188be73f1bfc00eb5e7b300b095d3dbe02a93a9d6a5a7e32adebc2` | 0 |
| buildCacheSettings.gradle | 525 | `c28dca0923ff6b910d706e494d96fa30fa9d032ab220407a89930f9bb8d5a6d7` | 0 |
| buildSrc/build.gradle | 2142 | `c4f6a554de07ae19161691a83273a94d72d983e552c29692497158b70eeb73b2` | 0 |
| buildSrc/src/main/groovy/corda.common-publishing.gradle | 9127 | `90327b14defff8d894057125084a2d201ad9d686cf6b57d57fae3ebe0dbb3f2e` | 0 |
| buildSrc/src/main/groovy/corda.kotlin-1.2.gradle | 4440 | `89f902c0caeeeaa716874c1dc54e59db5162ec7240ca19025aed780a2471cf59` | 0 |
| buildSrc/src/main/groovy/corda.root-publish.gradle | 294 | `196d9f7543be51e192b09ba482e56bba66e4d97ed7c2b76c1a0defbe804ea224` | 0 |
| buildSrc/src/main/groovy/net.corda.build.docker/ImageBuilder.groovy | 9681 | `e932bc2359c6b6d874414091ed583af84dd6c62f57afffcd3efd2f544ed07479` | 0 |
| client/jackson/build.gradle | 2391 | `6a125a6904a6c888a4747b0b7148413bd74a8fb15bc5920b2263fe6a8e0007f6` | 0 |
| client/jackson/src/main/kotlin/net/corda/client/jackson/JacksonSupport.kt | 26525 | `56b181af8cc60f94959588ccac114f4e41b5e5c1ebaeee61091a25a78886ad5b` | 0 |
| client/jackson/src/main/kotlin/net/corda/client/jackson/StringToMethodCallParser.kt | 13077 | `0a228141d344f2fa1c619eb4af47d8fa9cd03368107a3e801cc90e2db58d537e` | 0 |
| client/jackson/src/main/kotlin/net/corda/client/jackson/internal/CordaModule.kt | 31095 | `7af57bb1d906c12a6097e42c0ee5e3e1e609412cb8882a5d29bc8500c101c509` | 0 |
| client/jackson/src/main/kotlin/net/corda/client/jackson/internal/JacksonUtils.kt | 1273 | `1f4caf9566aab949119761e13c98ef5f518be14d5bdeb010135db9d467696f5f` | 0 |
| client/jfx/build.gradle | 3373 | `b8e09c89443588d8bc54244daa529d4557db3bddf812284de2dab756450ec109` | 0 |
| client/jfx/src/main/java/net/corda/client/jfx/utils/AggregatedList.java | 842 | `41d2a84b4caa3f7ea6a694df2f579dfdf98cf6851c6b724db72d74f91cdcb521` | 0 |
| client/jfx/src/main/java/net/corda/client/jfx/utils/ConcatenatedList.java | 645 | `6bb9ebc83720720af28cb17f9e84b6f0a78ac61d273b063c5341ffbc826b0e7e` | 0 |
| client/jfx/src/main/java/net/corda/client/jfx/utils/FlattenedList.java | 646 | `ce8d0d89281c3e81fc59a53deb52f2b10fcebda48346382e66cc0dfe813e6539` | 0 |
| client/jfx/src/main/java/net/corda/client/jfx/utils/MappedList.java | 686 | `ceee888a1eca49019ce0865e3c17f49de82f9ff15f9e07e1bcc07b09eb2ee501` | 0 |
| client/jfx/src/main/java/net/corda/client/jfx/utils/ReplayedList.java | 617 | `5e4957f52abe4b3b400808a5cce9e075800681685c62e0dd623a349a0136a488` | 0 |
| client/jfx/src/main/kotlin/net/corda/client/jfx/model/ContractStateModel.kt | 1998 | `be37ef327a62a3708021cea50ea712bb9b878eceac006729c977a172d0da0444` | 0 |
| client/jfx/src/main/kotlin/net/corda/client/jfx/model/ExchangeRateModel.kt | 1876 | `8c135cfe3aa801dff16327b2380bcc47b97a08cbbae9c9753d820ccf40b63013` | 0 |
| client/jfx/src/main/kotlin/net/corda/client/jfx/model/Models.kt | 3004 | `ad1f852a3e9c0cca67cbe70e9bc1b18b331d702918e3b294c136e7de6d78819d` | 0 |
| client/jfx/src/main/kotlin/net/corda/client/jfx/model/ModelsUtils.kt | 2122 | `c2df8792b9fdb243de7cdfbef5bce72292f030128ccb42daff5c862bdc9a8292` | 0 |
| client/jfx/src/main/kotlin/net/corda/client/jfx/model/NetworkIdentityModel.kt | 2027 | `7b28e62aa5dbad9889673ac6eb0284f8cf2ced03aeb951f20cfd56385fcc20bc` | 0 |
| client/jfx/src/main/kotlin/net/corda/client/jfx/model/NodeMonitorModel.kt | 6492 | `45277d9e8d04448cb30f2c4e03365f10f5ce84d56fac696032b5029a89a6b4d3` | 0 |
| client/jfx/src/main/kotlin/net/corda/client/jfx/model/TrackedDelegate.kt | 3821 | `d071a7a846d16500f5a0d88f72950349fa89d7629ddb310dcc87bd5d16a72fa5` | 0 |
| client/jfx/src/main/kotlin/net/corda/client/jfx/model/TransactionDataModel.kt | 5333 | `c524f9cf8e710c1301d15d5d18b655f98dc17150b4a8213c8213fb2c0fc7aba1` | 0 |
| client/jfx/src/main/kotlin/net/corda/client/jfx/utils/AbstractAggregatedList.kt | 6469 | `c197df0b8fe313614c1717559e40d8f5048299f822f0c9f956ba0160aa2d0c8a` | 0 |
| client/jfx/src/main/kotlin/net/corda/client/jfx/utils/AbstractConcatenatedList.kt | 14387 | `dfcc82353a517bb79fb735662c7099c796f04d66f378a97b52ee6a60221a63cd` | 0 |
| client/jfx/src/main/kotlin/net/corda/client/jfx/utils/AbstractFlattenedList.kt | 5394 | `aa4d298e3774be8fd018db6904f5c5074dc2feaa50ab0577ed5479deb7c2c8e8` | 0 |
| client/jfx/src/main/kotlin/net/corda/client/jfx/utils/AbstractMappedList.kt | 2842 | `980c6a462e9e0674c4161a470b27a20205a868fffd176ff0fc8ef85f70c8104b` | 0 |
| client/jfx/src/main/kotlin/net/corda/client/jfx/utils/AbstractReplayedList.kt | 2322 | `2c1ce340055059218405972cba7af6d3b602e4d9aefe3aaf5b356407c44b042a` | 0 |
| client/jfx/src/main/kotlin/net/corda/client/jfx/utils/AmountBindings.kt | 2131 | `f449a477f1501552d4e72c2ca0ae6c60874919006c711f94715c0fe620aabe69` | 0 |
| client/jfx/src/main/kotlin/net/corda/client/jfx/utils/AssociatedList.kt | 2690 | `7d60cdbe9ac700b3dbd532d986ac02424e1ef379fd04ce5090e605b7377b7fa8` | 0 |
| client/jfx/src/main/kotlin/net/corda/client/jfx/utils/ChosenList.kt | 2023 | `f33211f84e7202374d6348bf6a5b8e28e23c00a6d65644e37c7dbf1e721078b4` | 0 |
| client/jfx/src/main/kotlin/net/corda/client/jfx/utils/LeftOuterJoinedMap.kt | 1982 | `1674138ca61bd964b5e742e9be65704e542d8346d610bdc21d8a3db2282b89a9` | 0 |
| client/jfx/src/main/kotlin/net/corda/client/jfx/utils/MapValuesList.kt | 2603 | `7c30acca0cfe9b60273e1fc2cfa1093afedd3458b2a638dc193507dfd5667a16` | 0 |
| client/jfx/src/main/kotlin/net/corda/client/jfx/utils/ObservableFold.kt | 3025 | `f713e5b67770923a477454d25eb7b3df5327da63248971994d6ae4f3b96cf7e7` | 0 |
| client/jfx/src/main/kotlin/net/corda/client/jfx/utils/ObservableUtilities.kt | 14607 | `4627d257cc4ccc3b0be0bc4fc54f5a8b82621540b415b8bf40a0cbb75ba29a37` | 0 |
| client/jfx/src/main/kotlin/net/corda/client/jfx/utils/ReadOnlyBackedObservableMapBase.kt | 3748 | `9fe8147ee52e3148f0a964eb04dec20298d7a54917ce0cd3c678b2892ea26fb0` | 0 |
| client/rpc/build.gradle | 5433 | `dec0bdf717a853ab99f594a25b04c5e44eb99a1964ce72a9f5b3f34b63f9cc09` | 0 |
| client/rpc/src/main/kotlin/net/corda/client/rpc/CordaRPCClient.kt | 35650 | `0024cc4331abe2370925116931c11a27c6c7741123640bf7eec60f45de27d249` | 0 |
| client/rpc/src/main/kotlin/net/corda/client/rpc/PermissionException.kt | 465 | `13115985bb7e98780325e85aa9e9d35ecb55454f3b0f6a18a2bbab6988c01304` | 0 |
| client/rpc/src/main/kotlin/net/corda/client/rpc/RPCConnection.kt | 1978 | `e9496c9999ee139ce3c481bde9f760aedb7cf2e0479f6673550055da5e54c74f` | 0 |
| client/rpc/src/main/kotlin/net/corda/client/rpc/RPCException.kt | 1264 | `bcb185c6d640753d2da252ef53444f3808ef55778902c1bcf3eca0e9a39c2e10` | 0 |
| client/rpc/src/main/kotlin/net/corda/client/rpc/RPCSinceVersion.kt | 199 | `3d8c36c90e36ba295c54517e196d9d1d3e3538c395c27038a55436cb65343eb9` | 0 |
| client/rpc/src/main/kotlin/net/corda/client/rpc/Utils.kt | 702 | `4d943eedbf51ab631f96dfb6077b58cb1d136e9b8597d17df7bbd0a6fd009a7f` | 0 |
| client/rpc/src/main/kotlin/net/corda/client/rpc/ext/MultiRPCClient.kt | 18172 | `6451fa5fbbc9fb2d59f10ee57d515646098cbe46bfba3876c64a9f11b212e173` | 0 |
| client/rpc/src/main/kotlin/net/corda/client/rpc/ext/RPCConnectionListener.kt | 1882 | `2ee53aac0ada7a55d5b5e70cbfee4656399da52442eba62cb4e83b580c66653a` | 0 |
| client/rpc/src/main/kotlin/net/corda/client/rpc/internal/ClientCacheFactory.kt | 736 | `bb41c09993b42d0c8d74ac149071241ff803c8b81a4e1cf25654b19371076e5c` | 0 |
| client/rpc/src/main/kotlin/net/corda/client/rpc/internal/DistributionMux.kt | 2116 | `1b9cb0751e11edba3c96ca69e2f2f449b2706021be6c1a06795ab304f2e45d6f` | 0 |
| client/rpc/src/main/kotlin/net/corda/client/rpc/internal/RPCClient.kt | 11302 | `11e9d6cda37358444ab5674bd576f78a1fd6f5ec97107e05768e9c7e666edf65` | 0 |
| client/rpc/src/main/kotlin/net/corda/client/rpc/internal/RPCClientProxyHandler.kt | 35282 | `cf7f45a0f891c3a4fd91db35797e0bc23ff9f8f1e901fb1cb84d2a69e9a9eff5` | 0 |
| client/rpc/src/main/kotlin/net/corda/client/rpc/internal/RPCClientTelemetry.kt | 1755 | `6c9474abcc51f32b03b172fd2da1295f577c5690b3d1e16b7e6c54916803231a` | 0 |
| client/rpc/src/main/kotlin/net/corda/client/rpc/internal/RPCUtils.kt | 715 | `9a4f45ae669d363abcd2c62a1679604e268262c40faf383004d9735497d763f6` | 0 |
| client/rpc/src/main/kotlin/net/corda/client/rpc/internal/ReconnectingCordaRPCOps.kt | 21954 | `4b01753ddd35262bcf6bcbf2d5001128a24b9595069187aa7a6b8921bc80bd14` | 0 |
| client/rpc/src/main/kotlin/net/corda/client/rpc/internal/ReconnectingObservable.kt | 3655 | `67ac9c8603dbcb155a90ba5bc5829aef93f00981adf7d0cec5b0d75352102d10` | 0 |
| client/rpc/src/main/kotlin/net/corda/client/rpc/internal/SerializationEnvironmentHelper.kt | 2381 | `244bdde714083bc23e75c98c7326b4657dcc18b71be79570978dc39846fa36a9` | 0 |
| client/rpc/src/main/kotlin/net/corda/client/rpc/reconnect/CouldNotStartFlowException.kt | 465 | `8d5aca4473203de6224d47a2ff5c637f02f461257f8a8636509faa2fdcc6df5d` | 0 |
| common/configuration-parsing/build.gradle | 1209 | `99a706c784e902f80df33c1e18365a8aec64f0b3f3517b45e59a3006f23b1bc0` | 0 |
| common/configuration-parsing/src/main/kotlin/net/corda/common/configuration/parsing/internal/Configuration.kt | 30596 | `d259bffa77bb17b3fd0aa39d4ee1999067e238c409334ec4ab3a8a870d54f2ed` | 0 |
| common/configuration-parsing/src/main/kotlin/net/corda/common/configuration/parsing/internal/Properties.kt | 16752 | `6e8d9df0929078abe772528f07fc8006e7799b33c9e32c2382509f9269c5d85e` | 0 |
| common/configuration-parsing/src/main/kotlin/net/corda/common/configuration/parsing/internal/Schema.kt | 3061 | `52d1aac2231f244f09e8eb040836b3016486391494c6d4b80211246ab0951f79` | 0 |
| common/configuration-parsing/src/main/kotlin/net/corda/common/configuration/parsing/internal/Specification.kt | 10873 | `2fc6a67dcaec7d83af1fbca98e0ab65ea1e704ef057c6d55874ee7eb39a95af6` | 0 |
| common/configuration-parsing/src/main/kotlin/net/corda/common/configuration/parsing/internal/Utils.kt | 4632 | `8ae994378ec777e655349ca695f2bf76b4e6f83bc6231f92670ca0be73deb08d` | 0 |
| common/configuration-parsing/src/main/kotlin/net/corda/common/configuration/parsing/internal/versioned/VersionExtractor.kt | 1182 | `2d81dee258e9aa6d235ea70f05ad89c5f6c047ab73d372cfde50b00bbbaf5e51` | 0 |
| common/logging/build.gradle | 1515 | `842173f33e5102df46c2736ae165d9a9674b7bc1a6826d853d5926e39b43a371` | 0 |
| common/logging/src/main/kotlin/net/corda/common/logging/Constants.kt | 397 | `907d15d2e53480ec6b4b4af52cd6bcb50cd652fe0b688edc01b63d8c59a99c0e` | 0 |
| common/logging/src/main/kotlin/net/corda/common/logging/CordaVersion.kt | 1286 | `d52e1209c710e5171dc9cccf84c929ee96610e13e7436bd54e36b98fb8baad2f` | 0 |
| common/logging/src/main/kotlin/net/corda/common/logging/ExceptionsErrorCodeFunctions.kt | 2760 | `ae5e78bea6ec8fb0219d1b77416f71c6041fc677a5438115f688def4bdadfb9b` | 0 |
| common/logging/src/main/kotlin/net/corda/common/logging/errorReporting/CordaErrorContextProvider.kt | 571 | `76658903bb4d956822d11a492d7f514ab84d1d764f1f897d694fb3d2bf61449b` | 0 |
| common/logging/src/main/kotlin/net/corda/common/logging/errorReporting/ErrorCode.kt | 1438 | `52cb7aad3b3f4a79b9eb386309cddeec7c80c5a7de36e8ae031f8331e7077277` | 0 |
| common/logging/src/main/kotlin/net/corda/common/logging/errorReporting/ErrorCodes.kt | 470 | `e70f189981a80c34c278aae9dbf6ca9106218e2b9c7d87d7f1673566f9ccb7db` | 0 |
| common/logging/src/main/kotlin/net/corda/common/logging/errorReporting/ErrorContextProvider.kt | 788 | `daf6e6f0cdc3a6e6d372d0bae6a7025238d15e1bb9e1c1cc6b9c18820da63087` | 0 |
| common/logging/src/main/kotlin/net/corda/common/logging/errorReporting/ErrorReporter.kt | 414 | `d58780c28188f19a0a0338a00e396854aa6aa824c7846e54f1966e8f7f6e0656` | 0 |
| common/logging/src/main/kotlin/net/corda/common/logging/errorReporting/ErrorReporterImpl.kt | 1903 | `7f31b343423722f7f392777ad5c97b04eae24f1d835f7a0f562dc60f6d678f99` | 0 |
| common/logging/src/main/kotlin/net/corda/common/logging/errorReporting/ErrorReporting.kt | 2531 | `80e6fe9746d04a53e578b1b665ffc06a2bac03605fdb4cd9cb1a87fa836d819a` | 0 |
| common/logging/src/main/kotlin/net/corda/common/logging/errorReporting/ErrorReportingExceptions.kt | 1168 | `f0f271d5dfc40e8cc6c82488a86b42cfc4a44a1061ad14465a88da9f6c1cbe56` | 0 |
| common/logging/src/main/kotlin/net/corda/common/logging/errorReporting/ErrorReportingUtils.kt | 696 | `815773c9bba3a9a0bf4799fabc6c4e8cbd8de214e6957a9df5ff7c12d5382eb4` | 0 |
| common/logging/src/main/kotlin/net/corda/common/logging/errorReporting/ErrorResource.kt | 2584 | `d8a792bf61c1cb6305a5eea64229986a19f9e55a3b2dce2b05697c61ba27f009` | 0 |
| common/logging/src/main/kotlin/net/corda/common/logging/errorReporting/Errors.kt | 696 | `828c5d2a6b0c7c3d7fe727d9ff1263385508d8d2184fee3f5c86630ef4852653` | 0 |
| common/logging/src/main/kotlin/net/corda/common/logging/errorReporting/ResourceBundleProperties.kt | 351 | `a638b3b3126788b3251d70fad12268c6e71d6d5746a2074a6c42e928152a64e0` | 0 |
| common/logging/src/main/template/kotlin/net/corda/common/logging/Constants.kt | 407 | `2308d2ec16ffd75919ad16831d2a512247aa2f916f12592134cd938094db75ca` | 0 |
| common/validation/build.gradle | 420 | `da4ca20aadb657efe263f26a0f72b4f4164b636e40c703574197c36abfcb7113` | 0 |
| common/validation/src/main/kotlin/net/corda/common/validation/internal/Validated.kt | 5801 | `7741b21d42bf530348af96c43ba0a26d2482333da048822cfde389a82f99ae85` | 0 |
| common/validation/src/main/kotlin/net/corda/common/validation/internal/Validator.kt | 453 | `e1cbeca4db58a8b1930eeafc0ba186c6ca77bac881680ea2642564ae5708ff01` | 0 |
| confidential-identities/build.gradle | 2214 | `86451360c76b0708e18f3b01b7080ec9cce8d58fc8db06f2fb77173b184ab841` | 0 |
| confidential-identities/src/main/kotlin/net/corda/confidential/IdentitySyncFlow.kt | 6194 | `6732426603577e6dbdce86393560c7d55fc63d55bca863c759c580c75f285b4a` | 0 |
| confidential-identities/src/main/kotlin/net/corda/confidential/SwapIdentitiesFlow.kt | 7506 | `2338e6ccd8415c4dda0e68efa38d4a6b66f2d819f7d25cee6d1917d548646304` | 0 |
| config/dev/corda_dev_ca.cer | 769 | `5862e13fe47792831ef3776b46d6f66bbe1b8b8224eec2fa9cf121a0812bcdb7` | 0 |
| core-1.2/build.gradle | 927 | `830c780df4692e2a7ffa7c3a7b78ac53bf9addf0be7e641bacf9050a0c62332b` | 0 |
| core-1.2/src/main/kotlin/kotlin/CharCode1.2.kt | 164 | `c5d26b3d133edb831539b3432ca882c2f8b36a9f214e6f90d51d94f2e188e89c` | 0 |
| core-1.2/src/main/kotlin/kotlin/collections/KotlinCollections1.2.kt | 1187 | `126cdcaf17dc94330c018fffeb77f0ce88b5f868a87170324fa776080a883cc3` | 0 |
| core-1.2/src/main/kotlin/kotlin/io/path/KotlinIoPath1.2.kt | 1465 | `e6a1ed3275e771026a039a9c30895939e634c47cd5866ea1feece8815ce6dab8` | 0 |
| core-1.2/src/main/kotlin/kotlin/text/CharJVM1.2.kt | 984 | `4367c18af66e99058f86cfb12adc16e1bf7e12a75355a213fbb15f73d1cad96c` | 0 |
| core-1.2/src/main/kotlin/kotlin/text/StringBuilder1.2.kt | 452 | `0efe4be4e0d0ac3f64e8957bb077ace795b0ed8e1a538fbbfb3f7295aed37547` | 0 |
| core-1.2/src/main/kotlin/kotlin/text/Strings1.2.kt | 289 | `16ddaab0dc29b75779270e4574a3ca617136dbe720a62db2b5aa6c9530652dca` | 0 |
| core-1.2/src/main/kotlin/kotlin/text/StringsJVM1.2.kt | 611 | `c2d07d67764d2d52605eaa14bc33c7fda2cc02b0dad3ebcd34447347d793a387` | 0 |
| core/build.gradle | 6365 | `d8130b27da9fc1a7073c3e1543f23af31a454d2368ad8644886a50daf81c4c6b` | 0 |
| core/src/main/java/net/corda/core/crypto/AddressFormatException.java | 249 | `22ecdd94b6bb7f0f6aad61755b5bb73800bce513cc8903549f33bc70ca9b22ca` | 0 |
| core/src/main/java/net/corda/core/crypto/Base58.java | 7736 | `7c28c85e63c83670a9a9ddb9c5dcc49be506447db11d0b468a48edc1d911801d` | 0 |
| core/src/main/java/net/corda/core/flows/IdentifiableException.java | 485 | `b5b0a2746ec919076d359371b8fc0f2403deed5369a5d3140e4f70e6ce9a80d4` | 0 |
| core/src/main/java/net/corda/core/internal/package-info.java | 166 | `8abc50bca1e9549cb2b26d57e2b365a0e04bedccc688b99dcd05d87d759ddc39` | 0 |
| core/src/main/kotlin/net/corda/core/ClientRelevantError.kt | 301 | `dd6f1dc00786d1fd9e2ab3ee290a769b8978fdea34aef6cebfdfd2ec602faa89` | 0 |
| core/src/main/kotlin/net/corda/core/CordaException.kt | 3750 | `823b7c3073d049275030da51af38a37f4b2d12548d346a05844ebf72cb525b53` | 0 |
| core/src/main/kotlin/net/corda/core/CordaInternal.kt | 516 | `1cc2bc6def0504e108fab2b57947ca2b198d18c1a5172de0ef486945db85f881` | 0 |
| core/src/main/kotlin/net/corda/core/CordaOID.kt | 925 | `68cef7fe4d8dd644d9bd7441b298212c3ab00a99ce552d7ab78f7265a0a619e6` | 1 |
| core/src/main/kotlin/net/corda/core/DoNotImplement.kt | 686 | `63acdf05a63bc3336ca98c7fcf5337a7153f0750283c56513f3bdc9e34f4afff` | 0 |
| core/src/main/kotlin/net/corda/core/Utils.kt | 2208 | `cb5c4c3558474a21e101d1440713e226e42495aa6879efb6c475b10ecd493827` | 0 |
| core/src/main/kotlin/net/corda/core/concurrent/ConcurrencyUtils.kt | 1772 | `05a530a20f7efdcb9e2bcaea1a6419300f6c4b2d950bd3f916097c18e7d7d86d` | 0 |
| core/src/main/kotlin/net/corda/core/concurrent/CordaFuture.kt | 958 | `c2f6be6eee36b40affba7d683483726c413354a14d8bd61f4da81d63eedab1dd` | 0 |
| core/src/main/kotlin/net/corda/core/context/InvocationContext.kt | 9085 | `3b3065c37183d399e226bf5c353706a731fd2af9f15e1e98e8655fa45e77191a` | 0 |
| core/src/main/kotlin/net/corda/core/context/Trace.kt | 1965 | `69760652ff92ac9b34acf985d4fa0db8ed8f04f0144d7e955c07513ef9025cdd` | 0 |
| core/src/main/kotlin/net/corda/core/contracts/Amount.kt | 24845 | `79a2903b3c383eb6219d7fbb8fd2f03e916595e3b2f832c3d72f5db16f4a92fe` | 0 |
| core/src/main/kotlin/net/corda/core/contracts/Attachment.kt | 3040 | `029db995f9a15c3a6f1681f90952be0aca4df1f41dae096cca584b56de61ccaf` | 0 |
| core/src/main/kotlin/net/corda/core/contracts/AttachmentConstraint.kt | 6717 | `04b726dfb89885262634b6e392abab0704588df270e691b91af14dbfcd0b205f` | 0 |
| core/src/main/kotlin/net/corda/core/contracts/BelongsToContract.kt | 1285 | `5eca9edf113b02c83e5ed75d687bc4a66c79f23d5d3554037df6bc13643e5a24` | 0 |
| core/src/main/kotlin/net/corda/core/contracts/ComponentGroupEnum.kt | 876 | `90b7218b5f1cbdb1336f9a713602644e02260deb503f907c3fea10913691e5e5` | 0 |
| core/src/main/kotlin/net/corda/core/contracts/ContractAttachment.kt | 2060 | `48687a32841de17064e4d1cb510b24bb3316af90dd7568c8f5bdbccc2e640a3e` | 0 |
| core/src/main/kotlin/net/corda/core/contracts/ContractState.kt | 1375 | `80e300e51a621b850769eac20ab0d41110ad1484fd3698d198c845ecef777345` | 0 |
| core/src/main/kotlin/net/corda/core/contracts/ContractsDSL.kt | 5508 | `398d98823ef59a63e353e4f00b35cd82a5051454dfe0d4c25b7c5a952a405bd9` | 0 |
| core/src/main/kotlin/net/corda/core/contracts/FungibleAsset.kt | 2423 | `4ac443c2e174e128afafc25ddb2202993b3c17ee93a7daa598f8336ada0f5860` | 0 |
| core/src/main/kotlin/net/corda/core/contracts/FungibleState.kt | 1844 | `1ab9f063982b612c2525035f7d17bf3a297d709f2c5cc4f41db485b24196c67b` | 0 |
| core/src/main/kotlin/net/corda/core/contracts/NotaryInstruction.kt | 904 | `ec9c561e43ade961a03157d8e40beac9a0c314ee8025bb651c4a554beb0c763f` | 0 |
| core/src/main/kotlin/net/corda/core/contracts/RotatedKeys.kt | 5708 | `f4166ef42c01e5725d8a9929790d5c475adacc41bd97e5ac78c84046758faf77` | 0 |
| core/src/main/kotlin/net/corda/core/contracts/StatePointer.kt | 9622 | `d96c0ee2556050f37f9d0079b17c4acacce24ab33771ea414dedbe182e6c84b4` | 0 |
| core/src/main/kotlin/net/corda/core/contracts/Structures.kt | 18253 | `a5380eb9109fd2697df7d172824a08ad8f2c3a133b1fbfa6ec9c1a2c5ce0ecd2` | 0 |
| core/src/main/kotlin/net/corda/core/contracts/TimeWindow.kt | 4743 | `eba59138c8ee147c893d5a5a958c7395152c2bdcf1d229b58e56fea8dedc9c3f` | 0 |
| core/src/main/kotlin/net/corda/core/contracts/TransactionState.kt | 4624 | `604a2bbc6c1fd735dd68e3f25a6feb653c8775a98b960b63fa254d4cd1eed551` | 0 |
| core/src/main/kotlin/net/corda/core/contracts/TransactionVerificationException.kt | 20310 | `87f2d2d5c71099945f428d3b1c2c57e9094f632909b0ba1e38e0309bc3370b20` | 0 |
| core/src/main/kotlin/net/corda/core/contracts/UniqueIdentifier.kt | 1870 | `1cff08eb91439cb219377edcf447021c0eb781548654164e889f39a4f041fbc1` | 0 |
| core/src/main/kotlin/net/corda/core/cordapp/ConfigException.kt | 195 | `543b442df7ea66b0878731cdb0df3ebf9ecb6546128e6b56d6a57bd10b189e5c` | 0 |
| core/src/main/kotlin/net/corda/core/cordapp/Cordapp.kt | 7086 | `4cfdbc75ed2f266856bd48dcb9b01a47f7b80fff7291daf61cef884a01315f67` | 0 |
| core/src/main/kotlin/net/corda/core/cordapp/CordappConfig.kt | 2047 | `5d9f343e6e7bdad9445a0f4d3589a80def342184fd56682522f6d320fa2f081b` | 0 |
| core/src/main/kotlin/net/corda/core/cordapp/CordappContext.kt | 2981 | `beb6496da13ed8f35907d4575fc3c0f78197702f9c96f27b1886f99209770353` | 0 |
| core/src/main/kotlin/net/corda/core/cordapp/CordappInfo.kt | 1312 | `2d8b3ee7403ed0438b7112ed7f538158a33adb4273626899314296a067e759dd` | 0 |
| core/src/main/kotlin/net/corda/core/cordapp/CordappProvider.kt | 1072 | `6fa292bc18afacf941ea0055c211732def68451dfe57ea8fcdd45407287f76f6` | 0 |
| core/src/main/kotlin/net/corda/core/crypto/CompositeKey.kt | 14610 | `c0915ff0cb476c68774c4be080cf5822988508fe453b7d9393420daa54ebf9e0` | 0 |
| core/src/main/kotlin/net/corda/core/crypto/CompositeKeyFactory.kt | 1386 | `21f7f9b89755669c83820742da56a99f0c15ee4fe6327312f440bf6d15f40c3f` | 0 |
| core/src/main/kotlin/net/corda/core/crypto/CompositeSignature.kt | 3686 | `e67a5f9fe0d51d054d0a925fb7246953b8417e826b10013b8263b58f11d189d5` | 0 |
| core/src/main/kotlin/net/corda/core/crypto/CompositeSignaturesWithKeys.kt | 431 | `afbb31fb97e79cb3de2f6c95c52d12adb510eac23ab87fcc520c0472bee1cf9c` | 0 |
| core/src/main/kotlin/net/corda/core/crypto/CordaSecurityProvider.kt | 1954 | `e62758c2c1e62996c2c15158926aeec47c0ae2e3f3ad06c742e0d15295bea7fa` | 0 |
| core/src/main/kotlin/net/corda/core/crypto/Crypto.kt | 59754 | `a0bc267096ca6cb7725bea9df50565226dc0f2c2bebe7b816873c9d81df099a7` | 0 |
| core/src/main/kotlin/net/corda/core/crypto/CryptoUtils.kt | 15974 | `2d67521306ac43f2269d42243b7a2e8588f09bf755cb8fc35e1f638b4e6f963e` | 0 |
| core/src/main/kotlin/net/corda/core/crypto/DigestAlgorithm.kt | 1308 | `4ea49124c6769f0f8074830ac1a70ccce1a0790e0057f96e378775920a231ed4` | 0 |
| core/src/main/kotlin/net/corda/core/crypto/DigestService.kt | 5654 | `6fee1bbc2b26bfa13697bf8d5c0ee629ddc0f745463ab5038849fb69dd83cae3` | 0 |
| core/src/main/kotlin/net/corda/core/crypto/DigitalSignature.kt | 2434 | `187ff92a80494d5cd206e5330aa9e859c2d01311a0e48bc00d4c1552edf33471` | 0 |
| core/src/main/kotlin/net/corda/core/crypto/MerkleTree.kt | 3567 | `f72d81f883f63167779777c3649aa2a4568a87321a6a6ed7a028103bcfcc183e` | 0 |
| core/src/main/kotlin/net/corda/core/crypto/NullKeys.kt | 755 | `a25a058510dc0d16ad3b0d921b5f3ed4f0d13f4929d07586d5f83f4cfc96cda6` | 0 |
| core/src/main/kotlin/net/corda/core/crypto/PartialMerkleTree.kt | 10481 | `1457527e910bb0686eaec611f131eb2bf621d0463ab9d88e4c90a17c7fd80b35` | 0 |
| core/src/main/kotlin/net/corda/core/crypto/SecureHash.kt | 15828 | `865a4387463ba8d1e5c765de149d8d32438f30d742b5d7004636f12b63ea569a` | 0 |
| core/src/main/kotlin/net/corda/core/crypto/SignableData.kt | 730 | `fc238338bde66706d0c59c19dc07d208b0a7976471e7450e446dac3b9a479a09` | 0 |
| core/src/main/kotlin/net/corda/core/crypto/SignatureMetadata.kt | 1169 | `00420b5906b5c386a93636bde61b31ce1d8f1108752523f8583918aa2ed54260` | 0 |
| core/src/main/kotlin/net/corda/core/crypto/SignatureScheme.kt | 2023 | `9d6b6095e8dbf073c06916733c99494accd4ea64a3dfd530a5f6bc011a7cd171` | 0 |
| core/src/main/kotlin/net/corda/core/crypto/SignedData.kt | 1460 | `a33f2194358dcf081c08962351374c465404b6be0f6df18307beffae05554e45` | 0 |
| core/src/main/kotlin/net/corda/core/crypto/TransactionSignature.kt | 3536 | `282cc8067ec538d0ca9cbaa66bd26c93e5de606b66c28db3ba4db99b383b0e42` | 0 |
| core/src/main/kotlin/net/corda/core/crypto/internal/AliasPrivateKey.kt | 1531 | `84db5515c07c3d7256270be406b493852c60c532da1fb1ff72c76807dbdc8b8c` | 0 |
| core/src/main/kotlin/net/corda/core/crypto/internal/Curve25519.kt | 2031 | `7e037bd928013c8304d9456f97bd2510b5265f796bc658f7cf8168c7f6c9832e` | 0 |
| core/src/main/kotlin/net/corda/core/crypto/internal/DigestAlgorithmFactory.kt | 2872 | `bc22d8f13f279cae0cfdfe3ba2f168e69e450e7a1e96885c211c1988e543a6e8` | 0 |
| core/src/main/kotlin/net/corda/core/crypto/internal/Instances.kt | 2417 | `72be4a45b1a3853a721c8a8df468dc841efaa3d49747c571d948d052e5680526` | 0 |
| core/src/main/kotlin/net/corda/core/crypto/internal/PlatformSecureRandom.kt | 2805 | `e4ac676a5275ea92dbd30ad378782aa32c945990483ec6d80bedea9da65d4bf2` | 0 |
| core/src/main/kotlin/net/corda/core/crypto/internal/ProviderMap.kt | 1832 | `c38a4de5f6a7855efca172ae61594358fd9a277d778cedc557a30236f7bcc770` | 0 |
| core/src/main/kotlin/net/corda/core/crypto/internal/PublicKeyCache.kt | 2159 | `4e07692d56d4bdab93a25727043667e8ac7bb06b72a077f1cba31fb4f19317f3` | 0 |
| core/src/main/kotlin/net/corda/core/crypto/internal/Secp256k1SupportProvider.kt | 6670 | `0e66c3cbf611ceb74e699ac67bed3a2517a89c3a42f9d7798afd49925588a3f8` | 0 |
| core/src/main/kotlin/net/corda/core/crypto/internal/keyrotation/crossprovider/ProofProvider.kt | 728 | `7bd59da1283761c20e7b25e403121e2d030cbd30577293d7a8bd72928a481e74` | 0 |
| core/src/main/kotlin/net/corda/core/crypto/keyrotation/crossprovider/KeyRotationProof.kt | 1204 | `7011b28b8fe37526c7534bad1a60d97203b69e07e006c5a25e49fda5e15c2259` | 0 |
| core/src/main/kotlin/net/corda/core/crypto/keyrotation/crossprovider/KeyRotationProofChain.kt | 6657 | `41e38cff08b44788c7ce2b8fed3d5658adf811bf04e5b16e978d5b6ee2fea826` | 0 |
| core/src/main/kotlin/net/corda/core/crypto/keyrotation/crossprovider/KeyRotationUtils.kt | 527 | `5e87cd41c2136990ef66fb301f08ac6fd55fa07cdbbc9287bbf81833d0803579` | 0 |
| core/src/main/kotlin/net/corda/core/crypto/keyrotation/crossprovider/PartyIdentityResolved.kt | 1876 | `cf24dfeffc2dd154a56aa38161444f5249aaeb6f4fdf4327da12c617e7b04288` | 0 |
| core/src/main/kotlin/net/corda/core/crypto/keyrotation/crossprovider/PartyIdentityResolver.kt | 4814 | `3cff2add564dbeb12e86a752913d013daae8f9344e825b8b1e65c02f139c182f` | 0 |
| core/src/main/kotlin/net/corda/core/flows/AbstractStateReplacementFlow.kt | 9249 | `fc6a7c214833075603e4488d6560f431763fa71ce0b39f7bb968681b26deec89` | 0 |
| core/src/main/kotlin/net/corda/core/flows/CollectSignaturesFlow.kt | 19364 | `661f7200dbe97157e938a803c0191ed6fd63a7312ab52531c4b5daa3a6da9f4c` | 0 |
| core/src/main/kotlin/net/corda/core/flows/ContractUpgradeFlow.kt | 3880 | `bc43a5bff5898c5880c2362093abaa174af4050942c60f557944d70d6a037ec7` | 0 |
| core/src/main/kotlin/net/corda/core/flows/FinalityFlow.kt | 28208 | `c1be14e80f9e007e7338080bd429f6eb59701777dea125980d1c00bc379b326f` | 0 |
| core/src/main/kotlin/net/corda/core/flows/FinalityRecoveryFlow.kt | 4581 | `9180e9aa6cb9d63048e0edb192b5085882a10713cb581e6f205ded699b7c2d40` | 0 |
| core/src/main/kotlin/net/corda/core/flows/FlowException.kt | 2791 | `7ffc7244334e343b2a72801de6c452abb132e1e405dcfa310aeddff034cf1211` | 0 |
| core/src/main/kotlin/net/corda/core/flows/FlowExternalOperations.kt | 5834 | `571d5edd0eb4c64ab0dfaf02a71e88fc749886756beeb726f9e06e19db7b097a` | 0 |
| core/src/main/kotlin/net/corda/core/flows/FlowInitiator.kt | 3490 | `0a80ed8aaf57b652c351d1b7c469454746c0eae9662a582494853e9899db36aa` | 0 |
| core/src/main/kotlin/net/corda/core/flows/FlowLogic.kt | 35285 | `7b30721cc603f90dea61176e74121e05cee29c96ce0e9afda9907f0bddfe2973` | 0 |
| core/src/main/kotlin/net/corda/core/flows/FlowLogicRef.kt | 2598 | `e9c59ab1454b2ccd140c9c87e78574474c939d9163c68307fdce52e3689a47e4` | 0 |
| core/src/main/kotlin/net/corda/core/flows/FlowSession.kt | 10650 | `774b63e93204acb365f2406c1085c81cca1eebc0784fbf6adf686626ad60fe8e` | 0 |
| core/src/main/kotlin/net/corda/core/flows/FlowStackSnapshot.kt | 830 | `9ade388d058bd47c2cb07c4e6a6ca1ebaa7c93a8b267ae1441bcecd91feba950` | 0 |
| core/src/main/kotlin/net/corda/core/flows/HospitalizeFlowException.kt | 760 | `bd851b77cb66926b9eb4f7c9fda309579452f43d9604287738d80781d05fba07` | 0 |
| core/src/main/kotlin/net/corda/core/flows/InitiatedBy.kt | 793 | `bb3b20e360300db958a0ac20dceec42a58204a36a3e3e6bbcb91674b5bd798e7` | 0 |
| core/src/main/kotlin/net/corda/core/flows/InitiatingFlow.kt | 1658 | `e910f380f5e05c340a2f3f539f00319449bd9a5dbc3f8b3386d1cbe53d7abe47` | 0 |
| core/src/main/kotlin/net/corda/core/flows/KilledFlowException.kt | 569 | `9cfad36adfe5a14668a0f843580b38d4b56ca9a4b379ae87bc33d7623ebaf156` | 0 |
| core/src/main/kotlin/net/corda/core/flows/LedgerRecoverFlow.kt | 5630 | `0c3442b11b19c4a69b756165d70723b5b1fd607a73028f1401ed21e7e5dd8c12` | 0 |
| core/src/main/kotlin/net/corda/core/flows/MoveNotaryFlow.kt | 10288 | `d7dade9fabdf2368a7c402b875d871b726ce3fee07748aeca350280d1824a0a5` | 0 |
| core/src/main/kotlin/net/corda/core/flows/NotaryChangeFlow.kt | 3050 | `fbed06af5ef1e278d3d8e796cd8870d67592ae66dd2a3ded48b60ee5055110b5` | 0 |
| core/src/main/kotlin/net/corda/core/flows/NotaryError.kt | 4454 | `a6ad43a5e7a10503ec5616e1167426a3e2fb251af08b7461b4c8f9ae121eaf59` | 0 |
| core/src/main/kotlin/net/corda/core/flows/NotaryFlow.kt | 10220 | `f0a20f3d0502565d7d176a9cc1780cc2b84cbdb05a7c30ca3b0189ed73c982d1` | 0 |
| core/src/main/kotlin/net/corda/core/flows/NotaryWireFormat.kt | 5309 | `788298068fe203034d698c67e6ebbb3f67a8e4b82423236cf6cf0f92d3115ba8` | 0 |
| core/src/main/kotlin/net/corda/core/flows/ReceiveTransactionFlow.kt | 10457 | `f364acb2a2e718fa8543e04729c8444e34bd797bef75a2938a54a477abfd5e7d` | 0 |
| core/src/main/kotlin/net/corda/core/flows/RecoveryTypes.kt | 4654 | `a80d7018147b8a22bd7649f5d5860111d9f7ba4eb2e3bdba9bc8ef9ee264b15a` | 0 |
| core/src/main/kotlin/net/corda/core/flows/ResultSerializationException.kt | 425 | `8802925c168e5b1ee3ba1c3987b3988b10c046e58b4d3443ba970e0349af499e` | 0 |
| core/src/main/kotlin/net/corda/core/flows/SchedulableFlow.kt | 541 | `ca3657893eb0503d5d9869a6bffcd33562c6924f039a12cd6a2fd4aab69a582d` | 0 |
| core/src/main/kotlin/net/corda/core/flows/SendTransactionFlow.kt | 19139 | `c12279119912eea08d392360d200ec0dc0c7297ba05c2e73667a688f85ad3a50` | 0 |
| core/src/main/kotlin/net/corda/core/flows/StartableByRPC.kt | 539 | `bc93e12bae06f2b26f4242bd83974f393881e5373151864867343d725bac31dd` | 0 |
| core/src/main/kotlin/net/corda/core/flows/StartableByService.kt | 379 | `0e9b099b38a4188f2c95e4164bcd3030b8d196ea88f7c0080512303e21cac73e` | 0 |
| core/src/main/kotlin/net/corda/core/flows/StateMachineRunId.kt | 554 | `237f0283c790f59c6419a31a04b8611b6e2bf0e39bda69506f44b5930a122215` | 0 |
| core/src/main/kotlin/net/corda/core/flows/SystemFlow.kt | 337 | `39e5e0390e8e9863bbbd7a368860b8d5c394d3f023c1788894a685741f67b6e9` | 0 |
| core/src/main/kotlin/net/corda/core/flows/WithReferencedStatesFlow.kt | 5463 | `2c4ea8537acf1873b0fd9ab934ae23a96ee5f5798949b0beab5c8d4b039d3d0c` | 0 |
| core/src/main/kotlin/net/corda/core/flows/scheduler/mapper/FlowSchedulerMapper.kt | 582 | `9672412a41116b76c0ad43da0c4bb29f41b909487e93c2193d8c5e2b0166cf2f` | 0 |
| core/src/main/kotlin/net/corda/core/flows/scheduler/mapper/FlowSchedulerMapperImpl.kt | 2116 | `10e4425a6f6e147651b52df4fec0125a39d3c9e36b97505beb4c8572b2e0de67` | 0 |
| core/src/main/kotlin/net/corda/core/flows/scheduler/mapper/FlowThreadPool.kt | 478 | `5cfa1b09d1753b40360f7c5c1feeaebaecfc7af2ba8e549e792b9b1a4bb2baea` | 0 |
| core/src/main/kotlin/net/corda/core/identity/AbstractParty.kt | 2127 | `1483f8a4bf9a4a2f94d4a1bcc7ee8be30ee298ca1cee55e849ff4317384a1ede` | 0 |
| core/src/main/kotlin/net/corda/core/identity/AnonymousParty.kt | 1333 | `c397c86fc60a80e3ee4a1dfd15b3be57951fe6b93b1d8fdda7ec4d27fc5721b0` | 0 |
| core/src/main/kotlin/net/corda/core/identity/CordaX500Name.kt | 5602 | `a8a468db5c0d76341ae32fc8a5043b3cecab1f99a1c63aa7c5ab00f653be1419` | 0 |
| core/src/main/kotlin/net/corda/core/identity/IdentityUtils.kt | 4356 | `e08cf04ed30c62ab0632b233d3e783812aaebf406828e8818e71ba4404ca243f` | 0 |
| core/src/main/kotlin/net/corda/core/identity/Party.kt | 2959 | `537e1a200eba23d4987ed45d9ce0d96256015337d2fdb84b6b3f96aff8562cc9` | 0 |
| core/src/main/kotlin/net/corda/core/identity/PartyAndCertificate.kt | 3386 | `4bc6e6130f5a50b4d51e0e4661970afa2bc1571c09088cf0e7de5f66f86694ad` | 0 |
| core/src/main/kotlin/net/corda/core/internal/AbstractAttachment.kt | 4214 | `1a178423466639f5fcabf0295e532e89131b14dcc1eb67789a86a53f986d07eb` | 0 |
| core/src/main/kotlin/net/corda/core/internal/AttachmentTrustCalculator.kt | 1549 | `e4d71ab23ddbe69292a9fff79841a226c5d09109a80988df6778ad7f88b6bf57` | 0 |
| core/src/main/kotlin/net/corda/core/internal/AttachmentWithContext.kt | 893 | `07aa7f12e3b9b5092efdb2f1880b1ca647a6a27345330c3a296afcb7fb2df6af` | 0 |
| core/src/main/kotlin/net/corda/core/internal/BackpressureAwareTimedFlow.kt | 2268 | `0928a6b906f7ed26cc6e5706e45fed92200a0aedeb95520811f2b53f44247584` | 0 |
| core/src/main/kotlin/net/corda/core/internal/CertRole.kt | 4631 | `f46d731acaa856fdbf63b7781d7e2891124616b36ced919c294242e99fca0c97` | 0 |
| core/src/main/kotlin/net/corda/core/internal/ClassGraphUtils.kt | 554 | `ac60103f93c8f225e7ad9a96387d0652b200ea576daaba7910f766147318fae8` | 0 |
| core/src/main/kotlin/net/corda/core/internal/ClassLoadingUtils.kt | 3955 | `9ff4686df72523b89cad189a39b3e7769cce769cbcfa638cf71d872559086a46` | 0 |
| core/src/main/kotlin/net/corda/core/internal/ConstraintsUtils.kt | 6822 | `22dd76b3669bb9da1210c375e0bcb7469f493f07a5340f9a3ab7bbfd8a7e69cb` | 0 |
| core/src/main/kotlin/net/corda/core/internal/ContractStateClassCache.kt | 589 | `63d5dc355042108ede54922c1a249eb2501ba6c2aedfcea631b9bed570085f93` | 0 |
| core/src/main/kotlin/net/corda/core/internal/ContractUpgradeUtils.kt | 1897 | `971536b8f74765bc308b47b38e7df59af9626ce07b5696f5b7de409413575459` | 0 |
| core/src/main/kotlin/net/corda/core/internal/CordaUtils.kt | 4358 | `1538318d2c2a349ccaee6a3bf4fd19b096434cfebbbc7fba4fd1f08dc24f1ba2` | 0 |
| core/src/main/kotlin/net/corda/core/internal/DigitalSignatureWithCert.kt | 2505 | `acec2a3aef9bc9301a2a1c988804e1c62db1bbcd42cdda56fb8399eb6373a47a` | 0 |
| core/src/main/kotlin/net/corda/core/internal/Emoji.kt | 4915 | `cab9501072c208c9cc4084d3309ff3b4feceaf59d6988b04c6594a5bd0610db7` | 0 |
| core/src/main/kotlin/net/corda/core/internal/FetchDataFlow.kt | 17137 | `c18eed8a1b9b37cf598ae4bc6fcb29da34227b3d30069f0819da3ae3c32d6ab3` | 0 |
| core/src/main/kotlin/net/corda/core/internal/FlowAsyncOperation.kt | 2135 | `4d6ffc4ef77f1c6855d0edb08ff43658b3b0e6497e1dcd76f3836d6e9981de7f` | 0 |
| core/src/main/kotlin/net/corda/core/internal/FlowIORequest.kt | 3957 | `84439c8afaa8e1db3cd7869417075360dde353e308023d5ea0632202a541e526` | 0 |
| core/src/main/kotlin/net/corda/core/internal/FlowStateMachine.kt | 2003 | `607cb7336013215972b428d11a7bd80c47cb6d7496abf091e13ada1ea110572b` | 0 |
| core/src/main/kotlin/net/corda/core/internal/IdempotentFlow.kt | 1590 | `47b51d78cbce05d44edcf3ef949b9fb6311300b63fe4a900a971b6101c0447e7` | 0 |
| core/src/main/kotlin/net/corda/core/internal/InternalUtils.kt | 25833 | `4a4b73a6292acaff5dfad753fd8f7ff3252366cd98a083883eadb46e707b5a1f` | 0 |
| core/src/main/kotlin/net/corda/core/internal/JarSignatureCollector.kt | 4385 | `34facbb61bb80214235976e2a205bc88857cacccc9acb0d414a15e4655f8c00a` | 0 |
| core/src/main/kotlin/net/corda/core/internal/LazyPool.kt | 2956 | `3f98ad6c3fa6161322634a67afe147957fe4c111f6336c80fec1e2d4b6bf1fc2` | 0 |
| core/src/main/kotlin/net/corda/core/internal/LazyStickyPool.kt | 2322 | `ba7b80fd64e34929392d43ea1452ff537e20beeaa443a14750eab8157c1539b9` | 0 |
| core/src/main/kotlin/net/corda/core/internal/LegalNameValidator.kt | 7969 | `496c41c2f54a7214a03480c5c4eaf38a5345a09c44a25c981236301bcc3f6f9c` | 0 |
| core/src/main/kotlin/net/corda/core/internal/LifeCycle.kt | 2321 | `317faa41cba32b25fa729ffb158e9e6a94fd7d3193df77b4c3e27a4fe59fb224` | 0 |
| core/src/main/kotlin/net/corda/core/internal/NamedCache.kt | 1326 | `ddb200bcad2a25ebb8d4cb5615f80023f6afa17cc5e4a1f41db790f0bf192a1f` | 0 |
| core/src/main/kotlin/net/corda/core/internal/NetworkParametersStorage.kt | 1847 | `1d8154271b6f0849d1700d8ad438aa5d46f784b422ef679b7ba3d94f40d8c5f4` | 0 |
| core/src/main/kotlin/net/corda/core/internal/NodeInfoConstants.kt | 144 | `251550a03bfb69d79011e6057e5d3492e4f9b94c283677959ea9d1cce7c7fa3a` | 0 |
| core/src/main/kotlin/net/corda/core/internal/PathUtils.kt | 3558 | `1f569f617411d18eb5639961955f466e4467469b1c8a1913fd065b05cea93d81` | 0 |
| core/src/main/kotlin/net/corda/core/internal/PlatformVersionSwitches.kt | 1135 | `2171bcee20910e6cfd239e9fa6656ef370d3b026e5f070262b6ad0c71e703029` | 0 |
| core/src/main/kotlin/net/corda/core/internal/ProgressTracker.kt | 105 | `10fef032bb8ac92e092c223a0b198c67a5368dc97575cf77bba7029369a2f352` | 0 |
| core/src/main/kotlin/net/corda/core/internal/ResolveTransactionsFlow.kt | 6738 | `d65aa6a6270e155e75dc1421fd8a03f38d166295c1852e1a12155d67b39d5373` | 0 |
| core/src/main/kotlin/net/corda/core/internal/ServiceHubCoreInternal.kt | 3484 | `53ec3d3d31960ad7318e0813cb814d1f70199a0a52759ad4169fbb4a0535fdd0` | 0 |
| core/src/main/kotlin/net/corda/core/internal/StatePointerSearch.kt | 2818 | `092cb0dc13fb7d811933411e244860d8acac882079f144454b5421d4fd8614b1` | 0 |
| core/src/main/kotlin/net/corda/core/internal/ThreadBox.kt | 1403 | `fc00e654d42749f4e233148d7e67bf95a4a8b15b96039ce42f8681ec5e77bf5f` | 0 |
| core/src/main/kotlin/net/corda/core/internal/ToggleField.kt | 3541 | `30ec668a04e9ce9738439c82c396568bbaf6a49876e0e658800892bd673c5ffe` | 0 |
| core/src/main/kotlin/net/corda/core/internal/TransactionUtils.kt | 20542 | `ce56370e74d48e1cee1434f83ea5048edcf9d9afd3edd87bdfa3996b90755db3` | 0 |
| core/src/main/kotlin/net/corda/core/internal/WaitForStateConsumption.kt | 1828 | `c7036d5a7e098c46829b074655fffd0b409f31d117b1f668bffdc747068684ce` | 0 |
| core/src/main/kotlin/net/corda/core/internal/X500Utils.kt | 2735 | `81342a7f15eee190d968d9195af44804f0db59276c8ee9ca05636b5d79810f11` | 0 |
| core/src/main/kotlin/net/corda/core/internal/concurrent/CordaFutureImpl.kt | 7839 | `baf800c1e4f886e0198bbf7636a881307f9d0d2e4628b8e5d86887d1cb0e800c` | 0 |
| core/src/main/kotlin/net/corda/core/internal/cordapp/CordappImpl.kt | 5130 | `fe347e0683c93d96aa85290480d1aeacf3794b0613efa93b002ce531f4b8ba73` | 0 |
| core/src/main/kotlin/net/corda/core/internal/cordapp/CordappProviderInternal.kt | 1118 | `208deb80681353a23d44eec49990af1d06cfa427bcf7cd13b9122b21f206cf94` | 0 |
| core/src/main/kotlin/net/corda/core/internal/cordapp/KotlinMetadataVersion.kt | 1268 | `e8b5609b5f81b3c80fbfefe07acf377c0cf6525995a278333b0fe0c0feccfff0` | 0 |
| core/src/main/kotlin/net/corda/core/internal/cordapp/LanguageVersion.kt | 2293 | `71bedebe49686167f99c546a0d51562af3ee864dd61038a5fddfe9fa976ccea0` | 0 |
| core/src/main/kotlin/net/corda/core/internal/cordapp/ManifestUtils.kt | 776 | `ac621755c73eec3a7523668c64db92a43aa99c2fbffd43b300996ce2895b2e8e` | 0 |
| core/src/main/kotlin/net/corda/core/internal/errors/AddressBindingException.kt | 765 | `1853929edf8b5725f557ece1a7e932f714dccb04c8a0efabf23dee1bd014df3a` | 0 |
| core/src/main/kotlin/net/corda/core/internal/messaging/AttachmentTrustInfoRPCOps.kt | 302 | `732db3635ded5a5a0aa4038eba635d4a7f2e8e54b110a7f98bc41a20d88ae801` | 0 |
| core/src/main/kotlin/net/corda/core/internal/messaging/FlowManagerRPCOps.kt | 805 | `f5ba216e66f1f875265bfe80cf5ec36c933aeef2996b89304ca6c20def0ed934` | 0 |
| core/src/main/kotlin/net/corda/core/internal/notary/NotaryService.kt | 2259 | `2636652727a0cd5621c76a2a6a1f99cb9c4d3036f49ea0338c2163934bcd9df6` | 0 |
| core/src/main/kotlin/net/corda/core/internal/notary/NotaryServiceFlow.kt | 9397 | `53e107ce9f08cb9f624c4a95c24cde2787a013f32927842feadff67e46f50eb8` | 0 |
| core/src/main/kotlin/net/corda/core/internal/notary/NotaryUtils.kt | 3388 | `3ed781827ec9e6ed32b8e78749b4dd40e805a72fcf08810636f0cc5a7c3f6457` | 0 |
| core/src/main/kotlin/net/corda/core/internal/notary/SinglePartyNotaryService.kt | 4549 | `d793e668b61c6bd160c7b018106140201291c85a3beab1973c3b342dbb1a089c` | 0 |
| core/src/main/kotlin/net/corda/core/internal/notary/UniquenessProvider.kt | 2543 | `c0eb460a600ef2bee720416954581728a6031deb1189880fb14c8e377f52c67f` | 0 |
| core/src/main/kotlin/net/corda/core/internal/rules/TargetVersionDependentRules.kt | 1870 | `7355c7c9af516899d013f0849f7d60f8250297f7295f1c86662386fecf141def` | 0 |
| core/src/main/kotlin/net/corda/core/internal/telemetry/SimpleLogTelemetryComponent.kt | 5620 | `c23ec3ced28fe10abf9f4521fc547ee8b407b43e2feefbd8a670f30c1a147b13` | 0 |
| core/src/main/kotlin/net/corda/core/internal/telemetry/TelemetryServiceImpl.kt | 9227 | `58e10dcd2860f66cdda8d4dc5c47ad32ba3212cad86ee5787c945866fe7bb485` | 0 |
| core/src/main/kotlin/net/corda/core/internal/utilities/Internable.kt | 565 | `990539c7a129b6206cd4a0836e0d3ea1b0d8bc8df269b6985ab996aad6c81f91` | 0 |
| core/src/main/kotlin/net/corda/core/internal/utilities/InvocationHandlerTemplate.kt | 606 | `40217e147392e50c98d73018c45667a1f3c7f7f0a4dc7ebf71899bf41ecad00b` | 0 |
| core/src/main/kotlin/net/corda/core/internal/utilities/PrivateInterner.kt | 3556 | `65085784a4ea9bfda859632efb78aa86151007cf115269b2110d61f86f7e02b5` | 0 |
| core/src/main/kotlin/net/corda/core/internal/utilities/TimingUtils.kt | 267 | `d6c098e76a534b7d70c665e055e7b19a6b11f28203cae27af5c4860b7b3cc87c` | 0 |
| core/src/main/kotlin/net/corda/core/internal/utilities/ZipBombDetector.kt | 2327 | `6871e84d1e0861edd0a68f46f60b677902a077b78ca3860faead449006c66472` | 0 |
| core/src/main/kotlin/net/corda/core/internal/verification/AttachmentFixups.kt | 3438 | `26fa59d2329b8a1e2b4376c25f3d0e4cb4615d2d939a4b77e495ea5954dd5d4b` | 0 |
| core/src/main/kotlin/net/corda/core/internal/verification/ExternalVerifierHandle.kt | 199 | `745cc43357ba2540ba9333a97164442664ecc55702c9d1a63352117a1bc7a0bc` | 0 |
| core/src/main/kotlin/net/corda/core/internal/verification/NodeVerificationSupport.kt | 15168 | `17d4f2994d728466136fe7f4fd0f6babfde077df1d268d9499bf4551937d21f2` | 0 |
| core/src/main/kotlin/net/corda/core/internal/verification/VerificationResult.kt | 2638 | `fc2319e0ed2664b3225cc7592a771b1f607ba2b206691258594b498921eea732` | 0 |
| core/src/main/kotlin/net/corda/core/internal/verification/VerificationSupport.kt | 2031 | `5ea1c5f0cb9963c20294496439a8cde7570b0d21567d76f34229fbe61fae6b58` | 0 |
| core/src/main/kotlin/net/corda/core/internal/verification/Verifier.kt | 27157 | `c782c45d0acd3541fe1adc65a21449de7484f1fe25df30f39b138739337e1dd6` | 0 |
| core/src/main/kotlin/net/corda/core/internal/verification/VerifyingServiceHub.kt | 4118 | `1351bc2ec1f6c274778e85eae13ead7fdf7da50eb06b088888bc57e7b6d6d374` | 0 |
| core/src/main/kotlin/net/corda/core/messaging/ClientRpcSslOptions.kt | 321 | `142f1b3e39f0c7365c3bbc0f2c8ab3fdf7305800ec35085540cd4a6eef54210a` | 0 |
| core/src/main/kotlin/net/corda/core/messaging/CordaRPCOps.kt | 34663 | `b47b2c36e74e7fbb13f0972f4fdd78d479d2744b2f28bd60b1423ffb96d17a2f` | 0 |
| core/src/main/kotlin/net/corda/core/messaging/FlowHandle.kt | 3569 | `0d147fc2bba40d1e004f5134fb88f4acee0a6ff379c04b9e233bd6e02408cfa0` | 0 |
| core/src/main/kotlin/net/corda/core/messaging/Messaging.kt | 646 | `63f672070467a8f949f94cceba92028f0867aa68202bfb6178ac2a8b983da8fa` | 0 |
| core/src/main/kotlin/net/corda/core/messaging/RPCOps.kt | 686 | `970de7d83dec497e0f2c17557afa2117d4b96b265b7cd002fb5c8fa546940004` | 0 |
| core/src/main/kotlin/net/corda/core/messaging/RPCReturnsObservables.kt | 431 | `cc7892f79225d73f223e58c172b4730629ba9e6d628a793cc633d622ed9f1a3f` | 0 |
| core/src/main/kotlin/net/corda/core/messaging/flows/FlowManagerRPCOps.kt | 604 | `f15d0c1c4b8dba51918175d6bdd562f35ed687dc1a5eea15e28baf7dba2a645d` | 0 |
| core/src/main/kotlin/net/corda/core/node/AppServiceHub.kt | 3005 | `9e6271c3186ef05dc5d8a7f2a226775add1a0e809a7ca5442c78ceb276ab2a82` | 0 |
| core/src/main/kotlin/net/corda/core/node/AutoAcceptable.kt | 500 | `e1df2bc0711f2bc5682c4068585ba4b6b31b964305463194e3d2a732e7d13ae5` | 0 |
| core/src/main/kotlin/net/corda/core/node/NetworkParameters.kt | 14377 | `2415faf5e8fc778f481acd193012ea5759420f94709409c6bfd20ffce781d8ac` | 0 |
| core/src/main/kotlin/net/corda/core/node/NodeDiagnosticInfo.kt | 1263 | `3f122f6ecad646fa56b89ed113888b9e3b57cc68be277b1af8c68afed03242e0` | 0 |
| core/src/main/kotlin/net/corda/core/node/NodeInfo.kt | 3650 | `b4949e4542c8abfd114e2f15e165a5e168e810d878cb987dc0f31d045a90e37c` | 0 |
| core/src/main/kotlin/net/corda/core/node/ServiceHub.kt | 29113 | `ffc27597a509898f58059f25446347c3f3f0421a7a1c75c370ae6c59b6cfccfa` | 0 |
| core/src/main/kotlin/net/corda/core/node/services/AttachmentStorage.kt | 4430 | `d6a2aba4370d98fe8ff825ac7edad87db1309eb621752492e6ec4df3b8b5a384` | 0 |
| core/src/main/kotlin/net/corda/core/node/services/ContractUpgradeService.kt | 994 | `f5f9a12acc2b3b78c3b2636768420cd5ddd639bf09c438c5863e024c87c47836` | 0 |
| core/src/main/kotlin/net/corda/core/node/services/CordaService.kt | 1323 | `5aae32d1eb64dce30847dba60aa6dcd4ec486e3f415f3d8547f20c3c7ab263e2` | 0 |
| core/src/main/kotlin/net/corda/core/node/services/IdentityService.kt | 10042 | `8780b51970700f40f52428b06416ab43899d4bf548e6c0cd1818c855ccb1dc29` | 0 |
| core/src/main/kotlin/net/corda/core/node/services/KeyManagementService.kt | 4992 | `11010e505ebfcd922ab1f7c99fd87d34d1dc31cd902293a2f9f92ad6b4f4b801` | 0 |
| core/src/main/kotlin/net/corda/core/node/services/NetworkMapCache.kt | 6089 | `7f50b1294b24e82cc121141b6a76667d5e1cce316b39813b432f78693267f405` | 0 |
| core/src/main/kotlin/net/corda/core/node/services/NetworkParametersService.kt | 807 | `5c740b4f4bcee55481c93291615f1743697b4f3908b5723d77f0216c6cb6712b` | 0 |
| core/src/main/kotlin/net/corda/core/node/services/PartyInfo.kt | 467 | `48061b4cb3802aea4777887c36d712c0857f55105d7630322c3f4c88c03ef4a9` | 0 |
| core/src/main/kotlin/net/corda/core/node/services/ServiceLifecycleObserver.kt | 2163 | `e34fffb23021a5f2f4645e6f123b1806180146686a89633690a7f21dec080646` | 0 |
| core/src/main/kotlin/net/corda/core/node/services/TelemetryService.kt | 184 | `095f8f5fea1ca67c49f1ada12bcb09cc8494a70eb34e734a0e6076f1e96e77ff` | 0 |
| core/src/main/kotlin/net/corda/core/node/services/TimeWindowChecker.kt | 404 | `8d19d2318c59419d759e5bd44cc1d8a3c5c0fb04721c76c0b5b8a9506d2d6cb3` | 0 |
| core/src/main/kotlin/net/corda/core/node/services/TransactionStorage.kt | 1715 | `b5ca5622cb1ffd6f77b596641ed8284c6ab2ba61eb48c9e49862f4c3b91dd3fb` | 0 |
| core/src/main/kotlin/net/corda/core/node/services/VaultService.kt | 31731 | `dde536d4843539d2f536128a140950fe33646b22c3377fc28eb5fba6fce896fa` | 0 |
| core/src/main/kotlin/net/corda/core/node/services/diagnostics/DiagnosticsService.kt | 503 | `587012b50a616fd7914f007770a97c00ff5cc93c2ae18c08693243003a3c0a06` | 0 |
| core/src/main/kotlin/net/corda/core/node/services/diagnostics/NodeVersionInfo.kt | 715 | `108a3d7aef1793d6f4a65ee255e2e6d65f4b2dad413b3973b578eee6da44bb6e` | 0 |
| core/src/main/kotlin/net/corda/core/node/services/vault/CordaTransactionSupport.kt | 386 | `24876696c571c3ab58cb5b34a9e673608dc75049695c6aaffb2622f7e91fd9d0` | 0 |
| core/src/main/kotlin/net/corda/core/node/services/vault/QueryCriteria.kt | 39045 | `0e11863caf4523726de41716100cae1ef3a711e6b5e029c93aba41dd61bdb73a` | 0 |
| core/src/main/kotlin/net/corda/core/node/services/vault/QueryCriteriaUtils.kt | 24616 | `da3f20643386c1a6c7d4f2ac92d328fa16ab2ba3560e9cb1394e9c5ba4437b5f` | 0 |
| core/src/main/kotlin/net/corda/core/node/services/vault/SessionScope.kt | 283 | `3e95038ecb60d583b6552e7cadbe7f76e2fc2894fbdfe88253322da0e440f8e1` | 0 |
| core/src/main/kotlin/net/corda/core/observable/Observables.kt | 637 | `efd72249edcf3062d6cc9dc9c64f4c51b57e7ce9a156bb94267f8b13df9a3a26` | 0 |
| core/src/main/kotlin/net/corda/core/observable/internal/ResilientSubscriber.kt | 5332 | `10a075c9c7d6d88250c824922c9b6adb4bca4f8661de36ed1a34f26a11217416` | 0 |
| core/src/main/kotlin/net/corda/core/schemas/CommonSchema.kt | 2548 | `ba95c254392a267d06bb46b4d4037c02aeb04d2e0dde5df55e2d15208e849725` | 0 |
| core/src/main/kotlin/net/corda/core/schemas/PersistentTypes.kt | 7012 | `6865759ab861bfea4b55315f7835b651030d1e7f523920ad67336a57b7d6f2f0` | 0 |
| core/src/main/kotlin/net/corda/core/serialization/ConstructorForDeserialization.kt | 280 | `bf9a563cd92d35f0babe4b725ba2e8210340b153d06591c3abed818c1e29a24a` | 0 |
| core/src/main/kotlin/net/corda/core/serialization/CordaSerializationTransformEnumDefault.kt | 3384 | `3b5660f1a535769c8cc50ac554a5f85f515d40406f8f9c39a2c7f7fda02deafa` | 0 |
| core/src/main/kotlin/net/corda/core/serialization/CordaSerializationTransformRename.kt | 1549 | `139f0f1899ae51722a35c2640f2562e17a1fa3df82216013618e00a9ca77a010` | 0 |
| core/src/main/kotlin/net/corda/core/serialization/CustomSerializationScheme.kt | 1448 | `ebd996505d82d53547da469995caba6af6b77f44c718ae1348b62f80ac461411` | 0 |
| core/src/main/kotlin/net/corda/core/serialization/DeprecatedConstructorForDeserialization.kt | 526 | `8f52114465063f038a5105ac404e0d527731e5a350fbbed6407ecc820181ea58` | 0 |
| core/src/main/kotlin/net/corda/core/serialization/MissingAttachmentsException.kt | 425 | `c37ca9fb1540bb16ffc73a809e09d5e0a20ae5ecf786fdedb0a9626483846c9c` | 0 |
| core/src/main/kotlin/net/corda/core/serialization/MissingAttachmentsRuntimeException.kt | 507 | `c1f35bf8792a732b6cf0f646d8af1521e0752bfe90577b564e0809e048231c16` | 0 |
| core/src/main/kotlin/net/corda/core/serialization/SerializationAPI.kt | 15527 | `d47020d10de26b38786016e92c06f13ea676e2156a1bd10f940a3d7924625f7b` | 0 |
| core/src/main/kotlin/net/corda/core/serialization/SerializationAnnotations.kt | 1363 | `34cb0ef68df03ad770ec08763340b3ade44723f230fec385d079b20c9733bc53` | 0 |
| core/src/main/kotlin/net/corda/core/serialization/SerializationCustomSerializer.kt | 1813 | `0516f0fc8d762c72b7fbf64a129c39037662b188ee91863dc8b43dd0ce6aa36e` | 0 |
| core/src/main/kotlin/net/corda/core/serialization/SerializationSchemeContext.kt | 1562 | `ed57653946cff5600667ff7471fb5b6a355e872cb614149ca8867d56f0925aed` | 0 |
| core/src/main/kotlin/net/corda/core/serialization/SerializationToken.kt | 2628 | `9e5bb583b24e994c7c5f5ca1e93c2fe3376fcdb4a448d16600035126bcba8441` | 0 |
| core/src/main/kotlin/net/corda/core/serialization/SerializationWhitelist.kt | 802 | `59f91de8b5df7a4d951b919354ea27c6ff725749f5f35782ea2b0c7033a4c45e` | 0 |
| core/src/main/kotlin/net/corda/core/serialization/internal/AttachmentsClassLoader.kt | 30328 | `0da53afd302e6de25bf09c55bcbad2ac857a98c2fff63eefd80f9e4f1f2c652c` | 0 |
| core/src/main/kotlin/net/corda/core/serialization/internal/CheckpointSerializationAPI.kt | 5218 | `3256d24aceeb4edbfb23403b5499f9a9e519a52368a626522083e96e296faa46` | 0 |
| core/src/main/kotlin/net/corda/core/serialization/internal/CustomSerializationSchemeUtils.kt | 870 | `f59ef936288cb97bf45b3d03d59a5c8f524d5a55913a855f09aea91f8a8e4edf` | 0 |
| core/src/main/kotlin/net/corda/core/serialization/internal/MissingSerializerException.kt | 605 | `192e4d92154eb6cac7a89ec8c695f1c3601b2c3c5b185877fb1d6bd01f2712e1` | 0 |
| core/src/main/kotlin/net/corda/core/serialization/internal/SerializationEnvironment.kt | 5174 | `5bece15cbb3a7e3285eae4b78c3ecb23efc757d617d41904c4976bc170dbfa6d` | 0 |
| core/src/main/kotlin/net/corda/core/solana/AccountMeta.kt | 1253 | `bd43fc2e7c57317236dfe850e846aa6c26b2f1ab8d888edb5d992e6dd52b878e` | 0 |
| core/src/main/kotlin/net/corda/core/solana/Pubkey.kt | 893 | `b7ef000f21d5e186a2ab3ec90184062320e19439ac3b8f7820b16f51bd0c6a86` | 0 |
| core/src/main/kotlin/net/corda/core/solana/SolanaInstruction.kt | 1183 | `52217c4c7a7c5207e3ff9272e74c50530da2326894e11fcf1542811feffd3e5d` | 0 |
| core/src/main/kotlin/net/corda/core/transactions/BaseTransaction.kt | 8548 | `5ded6c9439d29e19bc938cb18ddd6d66c58b57f153a3fe5436ffebd87cafb8d0` | 0 |
| core/src/main/kotlin/net/corda/core/transactions/BaseTransactions.kt | 2860 | `11aba5003725067db2d0966a61f87663eeef9a671372289d2b33dc755ceb9385` | 0 |
| core/src/main/kotlin/net/corda/core/transactions/ContractUpgradeTransactions.kt | 23149 | `a7353563296123b4517469825dc7ae0274ece23675f0c5deb81f4512bd5f4fec` | 0 |
| core/src/main/kotlin/net/corda/core/transactions/LedgerTransaction.kt | 48255 | `5f10be6a49824c7237bb2dfafb2c0e62afd32da3c5455b853504bc5d6d53d43f` | 0 |
| core/src/main/kotlin/net/corda/core/transactions/MissingContractAttachments.kt | 1043 | `23bd83f753578a47d57e286ba894a41f01ba2efc5aca9b6ad50b735be2dcbb43` | 0 |
| core/src/main/kotlin/net/corda/core/transactions/NotaryChangeTransactions.kt | 12699 | `dfd98937e2af9747fcee93dbfb7780230c7ace0272b183f698e3ed892ef72c2b` | 0 |
| core/src/main/kotlin/net/corda/core/transactions/SignedTransaction.kt | 18720 | `5e0d988ff758dabbb4ea46450c9d67c40d36c4eac7dd23034728b7bc83f88b47` | 0 |
| core/src/main/kotlin/net/corda/core/transactions/TransactionBuilder.kt | 54678 | `a58291c7fbefbf7c57e6b562ea38eaa30bfbef0b130cd37a982a9ae84a23b4a8` | 0 |
| core/src/main/kotlin/net/corda/core/transactions/TransactionWithSignatures.kt | 5266 | `174580257de41cad9c6a32bbbde5f54d01b3733c6a344c2efc62566f685d64ad` | 0 |
| core/src/main/kotlin/net/corda/core/transactions/TraversableTransaction.kt | 28048 | `58d194e5924756e5d5d4a9b036af20e7fb19a6bd02282cbf344f19575d1b7a5d` | 0 |
| core/src/main/kotlin/net/corda/core/transactions/WireTransaction.kt | 34036 | `90dc7764bd631df2dd04f152250a5ce3019bdd1008bc5fe1183a4ea255019751` | 0 |
| core/src/main/kotlin/net/corda/core/utilities/ByteArrays.kt | 9398 | `d9737cfd12137945d95f1499822f0d409ff68fbe93900257700c403e843a137d` | 0 |
| core/src/main/kotlin/net/corda/core/utilities/EncodingUtils.kt | 4069 | `902d11b6a8292aa8c3df64331ea0fd2875e42d7057e21398c33037a88ff288cb` | 0 |
| core/src/main/kotlin/net/corda/core/utilities/Id.kt | 1260 | `a6d8bc4b43d031d4e4604eb17fc47ec87aa70fc3bd03344f2a6f62b1d08b7a5c` | 0 |
| core/src/main/kotlin/net/corda/core/utilities/KotlinUtils.kt | 4922 | `f1a16c539ad1dbfbea53802931330d84c56973d9fa48d18c84907d6275688dd5` | 0 |
| core/src/main/kotlin/net/corda/core/utilities/NetworkHostAndPort.kt | 2066 | `b40c8551ff2e2948c04791126dec649bbc7afc175c00afbf11d9f9c02093de6a` | 0 |
| core/src/main/kotlin/net/corda/core/utilities/NonEmptySet.kt | 2624 | `436ea9b720a2576842d815b18b136d11ef72cb99f8744811b8e0f47c4df81d5e` | 0 |
| core/src/main/kotlin/net/corda/core/utilities/ProgressTracker.kt | 14191 | `8ef3274c2c422d867d63b0fb99e690878a93d72b46683a240f2bbddc48e15bbb` | 0 |
| core/src/main/kotlin/net/corda/core/utilities/ThreadDumpUtils.kt | 2817 | `b42e90670522a040a6cab832eb2bf7ec82a0694c944770847676f86611fad0b5` | 0 |
| core/src/main/kotlin/net/corda/core/utilities/Try.kt | 3704 | `38eb70cc5d3536c2cd94d418334f6a1dcf2670c0f5397a292769f0ad12dc42b8` | 0 |
| core/src/main/kotlin/net/corda/core/utilities/UntrustworthyData.kt | 1330 | `a0a2bea2b741a1ef018bc4926ef81867a208aabaef07273f2ea8d97b3f0cf464` | 0 |
| core/src/main/kotlin/net/corda/core/utilities/UuidGenerator.kt | 152 | `73910fdf539fef6954ad8cb27357c4b9f34677424457a5df6967e8376a549957` | 0 |
| core/src/obfuscator/kotlin/net/corda/core/internal/utilities/TestResourceWriter.kt | 2338 | `fdd00a1853402e354710639fcb6aa16b5e97dc9ddd789c15d8472b11b1358337` | 0 |
| core/src/obfuscator/kotlin/net/corda/core/obfuscator/XorInputStream.kt | 763 | `563a7da6ec8069903024a1e07013ce8ef9d9c8ccc99d2025e0bfca329a2b03d3` | 0 |
| core/src/obfuscator/kotlin/net/corda/core/obfuscator/XorOutputStream.kt | 756 | `a5dee49ae4deabfd52edda4d1d4c2a146e2d2483ed2185ef2d9846d7443e607d` | 0 |
| detekt-plugins/build.gradle | 380 | `da6ca99768ad3ba61e3f8ab7683b80fe36d8eba85fb5e3671a410097d303c349` | 0 |
| detekt-plugins/src/main/kotlin/net/corda/detekt/plugins/CordaDetektProvider.kt | 593 | `3c20ed70b27b23f5a17cc3e8ac8ef2e6c4c181839973c9194c690549649b952e` | 0 |
| detekt-plugins/src/main/kotlin/net/corda/detekt/plugins/rules/TestWithMissingTimeout.kt | 1898 | `b7081d434d79cc65a8b78ca0bc10553691c4baeb02b5697fa78c5fcfe6ab1008` | 0 |
| docker/build.gradle | 8953 | `3f95bf68482ea45f5e11fa896cba23421d8280c7d13d2e5c3e6224b54e12c181` | 0 |
| docker/src/main/kotlin/net.corda.core/ConfigExporter.kt | 4156 | `41e029b62b2553342568c28e0ac0691ac28e804b240fedd38d006c09354d3abd` | 0 |
| docs/build.gradle | 4638 | `76939e1941a76463b9bdf5c7c3242bf9ae2b40bd3a50ae77a33a5a94ce432df1` | 0 |
| experimental/avalanche/build.gradle | 815 | `a959df656779b877d882a4a64ec8f1aaf72dbdff95948bc466b10e054790d19e` | 0 |
| experimental/avalanche/src/main/kotlin/net/corda/avalanche/Main.kt | 7942 | `0a8026383002386015a1b9c2de5f47c15e27220e616c2d66caf941f3db183706` | 0 |
| experimental/avalanche/src/main/kotlin/net/corda/avalanche/Parameters.kt | 1546 | `80506afce8a93d93b6d97c87bba6f7046aad02c1c8a316ede59bfa8d3cf3849a` | 0 |
| experimental/blobwriter/build.gradle | 890 | `94459b0b3375c7b9f9b27797f2ca8991317ee26adf7c54ef9bed7bf2701755cc` | 0 |
| experimental/blobwriter/src/main/kotlin/net/corda/blobwriter/BlobWriter.kt | 5158 | `6e4788639043d3d26ab3b1c8d7c01f722c520464eae00750eab959a1162f57ee` | 0 |
| experimental/build.gradle | 1263 | `161cec38a080787c2be5789397aafc8a3cb34af8cc9e678ff7fc834f69d9c93e` | 0 |
| experimental/corda-utils/build.gradle | 1086 | `bfda8d1b897bfad618b97a2704a4fe328835d44b01bede8bf538912cef3f00e5` | 0 |
| experimental/corda-utils/src/main/kotlin/io/cryptoblk/core/StatusTransitions.kt | 4956 | `66026ff77fc858403a9ff4655fe53e3d1170f3341ca8e27716bde62130677a53` | 0 |
| experimental/corda-utils/src/main/kotlin/io/cryptoblk/core/Utils.kt | 2781 | `4b1f1bb278a0c74fae2d517357cec4a41ad073ac501d7669394a75dafdafe870` | 0 |
| experimental/cpp-serializer/bin/blob-inspector/BlobInspector.h | 471 | `13b577526de5943ad5cb337c1437dfb3684201af029671bed562e39f96e7d9d6` | 0 |
| experimental/cpp-serializer/bin/blob-inspector/CordaBytes.h | 723 | `2485f7b4e0427849ac01ea0511cabe8b492f778344f250fd99e862ac408c1b7c` | 0 |
| experimental/cpp-serializer/include/amqp/AMQPDescribed.h | 291 | `a002839929da397b1fb6f3e4db6eec2e3a476aba93c8c138844285d1d07ce859` | 0 |
| experimental/cpp-serializer/include/amqp/AMQPHeader.h | 482 | `a14189768bff2dfee83b8baf8b1cde30a0155fb4c913622bbafe7ed824c23a98` | 0 |
| experimental/cpp-serializer/include/amqp/AMQPSectionId.h | 400 | `60aa70c6a24296c69baf1da897d1c8eaf7cdd7e3cfeb72cf383faede9e3b40f6` | 0 |
| experimental/cpp-serializer/include/amqp/ICompositeFactory.h | 927 | `4b8c0b11735895df71304008c311cb3cb8d2d26457d83487b8967ded7388021b` | 0 |
| experimental/cpp-serializer/include/amqp/reader/IReader.h | 2060 | `b83b81c3e4357dff48d4b5c146d1160f9c19fcc4afb6e20b16b0ae83631e4752` | 0 |
| experimental/cpp-serializer/include/amqp/schema/Descriptors.h | 799 | `5faca7e38c1bea4cb795d618d3c6b44039f4291d4c7b90699b82da4fd75011fc` | 0 |
| experimental/cpp-serializer/include/amqp/schema/ISchema.h | 317 | `2a5294b203b72f9af271bab73038e5914702c01baf440cb2248fcb01f1ea2d4c` | 0 |
| experimental/cpp-serializer/include/amqp/serializable/ISerializable.h | 148 | `7f39ad8461f2ae25a1753c76bd9de0819e4d2fb9e08d84b8d750846b90101bec` | 0 |
| experimental/cpp-serializer/include/colours.h | 454 | `7ca00d927a98c431bb79811cccc00e43d95950476bbc82c85c618b77cddde339` | 0 |
| experimental/cpp-serializer/include/debug.h | 430 | `7c078c37064434b143b320dfc8a852802749fcf2ccf2646df0653c54d49f6d41` | 0 |
| experimental/cpp-serializer/include/serialiser/Serialiser.h | 238 | `88103a8e7f3f920f547e6a324aecef739eaa9465a2792995d05184fca03e74dc` | 0 |
| experimental/cpp-serializer/include/types.h | 685 | `083f99a9355b2af24603c1d80cc1d75eb97c2bc1c1cd2cd2e9f3afc77faa405b` | 0 |
| experimental/cpp-serializer/src/amqp/CompositeFactory.h | 2362 | `1c6ff4b9b2902611d6da185b8e133c59abe465ccbd5c5f794a2301376ad692bb` | 0 |
| experimental/cpp-serializer/src/amqp/reader/CompositeReader.h | 1522 | `546388766f5d7e9c2115092a3d89aedb30f5d06fe6ef1caf499876d2116651e4` | 0 |
| experimental/cpp-serializer/src/amqp/reader/PropertyReader.h | 1554 | `ead07478db52bbdea702b81ec1f7e6c49fd80abc521e540f23fb8df12392adef` | 0 |
| experimental/cpp-serializer/src/amqp/reader/Reader.h | 7281 | `7b3428f4ee9ae51644556d5b4aac3f80ef3b8ff7ec2b8e00461836a833a6db30` | 0 |
| experimental/cpp-serializer/src/amqp/reader/RestrictedReader.h | 1201 | `2495983239e69e2295e911bf848b90443f2153c1fe959d0da7c74301106ace15` | 0 |
| experimental/cpp-serializer/src/amqp/reader/property-readers/BoolPropertyReader.h | 1066 | `67e567348e8f1492c04dd5dfcce5052e005dc801d24d5260ca004527ec34acfc` | 0 |
| experimental/cpp-serializer/src/amqp/reader/property-readers/DoublePropertyReader.h | 1069 | `effbbac0c194522683f7481a61fa47ef744994488cc601058544818b36a49a42` | 0 |
| experimental/cpp-serializer/src/amqp/reader/property-readers/IntPropertyReader.h | 1065 | `2457c6f1e4e76f15a03d11bd9740089adbb7f2db727e7f70213b66c53a25ef91` | 0 |
| experimental/cpp-serializer/src/amqp/reader/property-readers/LongPropertyReader.h | 1066 | `2f03d080bf7e41583e159cdcf7530be052f940b6199ae555674718243b45581b` | 0 |
| experimental/cpp-serializer/src/amqp/reader/property-readers/StringPropertyReader.h | 1069 | `687a79cace1a00a518dfdba676e289ee70ca5bf558343170771c0251b92e2f13` | 0 |
| experimental/cpp-serializer/src/amqp/reader/restricted-readers/ArrayReader.h | 1275 | `9c3883d94761248aa5f3830622be9e3bf33b287dae6208bc9b855c6edba97230` | 0 |
| experimental/cpp-serializer/src/amqp/reader/restricted-readers/EnumReader.h | 764 | `b18b4da7307077d98e39346fcad43f7ffeb635feaf856d7c0bc8372c77bcb662` | 0 |
| experimental/cpp-serializer/src/amqp/reader/restricted-readers/ListReader.h | 1302 | `e5e42653d1d4e442815c0ff5e1290e18746f1a6f9bb54bce51a3e9ecc42dba95` | 0 |
| experimental/cpp-serializer/src/amqp/reader/restricted-readers/MapReader.h | 1472 | `4edb4aec65ca425a0635d75c6f95b82968479d47b75145c7853be9375dfeb54e` | 0 |
| experimental/cpp-serializer/src/amqp/schema/AMQPTypeNotation.h | 1723 | `051e285a0908a3d154b53964e7fdca632b9320dc546d69f29d6531b5e318a565` | 0 |
| experimental/cpp-serializer/src/amqp/schema/OrderedTypeNotations.h | 5903 | `e62dccbe40265dbf4a725c09931b17ea83f21b335485af92285b72b434209acd` | 0 |
| experimental/cpp-serializer/src/amqp/schema/described-types/Choice.h | 616 | `88b0c4d22798aba4bdb016d7afb24830e62acf65906f687d5b872fbb8dc22a24` | 0 |
| experimental/cpp-serializer/src/amqp/schema/described-types/Composite.h | 2632 | `120ee2140dddbed7c0f761ad39fef3e801b30224ecc899de8127ed834790fd9d` | 0 |
| experimental/cpp-serializer/src/amqp/schema/described-types/Descriptor.h | 686 | `a2c536f864d05b275e671a9e5ca3455db99b82a72b8757488b7e116355285965` | 0 |
| experimental/cpp-serializer/src/amqp/schema/described-types/Envelope.h | 924 | `e29ff98938596b5fc288afef93b675ed2ab481c8ae79fe566646d376d770fc35` | 0 |
| experimental/cpp-serializer/src/amqp/schema/described-types/Schema.h | 1751 | `2aa444eab520abd4b446307193ce7827804b70812f3e236ea12936723f63997c` | 0 |
| experimental/cpp-serializer/src/amqp/schema/descriptors/AMQPDescriptor.h | 2253 | `eb4d91a79586811b84ac42d9334ef169980482d10db917d23a84e63f2a6bfc14` | 0 |
| experimental/cpp-serializer/src/amqp/schema/descriptors/AMQPDescriptorRegistory.h | 1222 | `c9edafe8147bd58a4dbf61e8f03d1257cd4f36205557747eb68e0243f7d13ad6` | 0 |
| experimental/cpp-serializer/src/amqp/schema/descriptors/AMQPDescriptors.h | 3622 | `ccf78c3d9f0f199cad51aad16539d20cf8eb620b07bca639e3116ab0eec8d0f1` | 0 |
| experimental/cpp-serializer/src/amqp/schema/descriptors/corda-descriptors/ChoiceDescriptor.h | 696 | `fea9430081f400e10681bace4ac283a841b0a7da4d5fda5f7fb68777335da630` | 0 |
| experimental/cpp-serializer/src/amqp/schema/descriptors/corda-descriptors/CompositeDescriptor.h | 735 | `4e0e6cd3daa517be3643c75ab5756d0d2f7371e145cf2dfe876ede796b03b35a` | 0 |
| experimental/cpp-serializer/src/amqp/schema/descriptors/corda-descriptors/EnvelopeDescriptor.h | 1087 | `81cbd87f7458d0fa4feded0639862360a5320e5d0478beb989163eb097459b38` | 0 |
| experimental/cpp-serializer/src/amqp/schema/descriptors/corda-descriptors/FieldDescriptor.h | 859 | `79973512d4547a4d0fec2565bb33bc1e155b790885fc9ff43c9540bddce749f7` | 0 |
| experimental/cpp-serializer/src/amqp/schema/descriptors/corda-descriptors/ObjectDescriptor.h | 883 | `0b7e57e0c121b26d0a81d2fe328e1acf8b9a1724a869a963739d61ec2acd273d` | 0 |
| experimental/cpp-serializer/src/amqp/schema/descriptors/corda-descriptors/RestrictedDescriptor.h | 1125 | `6b019d00173f53513a98f88cca16a1160d8698884e760b4ba734ab9525af5a85` | 0 |
| experimental/cpp-serializer/src/amqp/schema/descriptors/corda-descriptors/SchemaDescriptor.h | 799 | `f84ab5ba47be7d25dd77bf8b04359c1d5941289938b3aca407145eef6f5649fa` | 0 |
| experimental/cpp-serializer/src/amqp/schema/field-types/ArrayField.h | 658 | `0414d12d0cf5dbae469fa2898a1503c5b5ac909a7ab5f649afd751b17f6d9b0c` | 0 |
| experimental/cpp-serializer/src/amqp/schema/field-types/CompositeField.h | 691 | `1aced4bee775f9fc7b14666bf9c616f6fe73c20654dd16d698a75b3e3fb809c6` | 0 |
| experimental/cpp-serializer/src/amqp/schema/field-types/Field.h | 1966 | `1f28464e98ee673f92ad24c1c8b79055f229b418d0347317630f6e383dfa7770` | 0 |
| experimental/cpp-serializer/src/amqp/schema/field-types/PrimitiveField.h | 667 | `fc0186be77c87866c2bbaeeaedde4d21f2189cdbcd2d6ef465ca0ecc54e8b773` | 0 |
| experimental/cpp-serializer/src/amqp/schema/field-types/RestrictedField.h | 693 | `94d7cd0626ebf912afeda45718a3898aeab62884ea0feadda3dd03c36d0ad95c` | 0 |
| experimental/cpp-serializer/src/amqp/schema/restricted-types/Array.h | 1256 | `7ff4e7e3df52313b823e2089ef40d308a7b722390a509ac9b3bf3d646a24ac22` | 0 |
| experimental/cpp-serializer/src/amqp/schema/restricted-types/Enum.h | 1224 | `f44aec4338f2b0c12fc7ca9470380e77c8a501f6c8349b50df556796e6f9d349` | 0 |
| experimental/cpp-serializer/src/amqp/schema/restricted-types/List.h | 1237 | `b1282cd43e41c2560fba2e0f33ab988ec787aac59e2cdd682755624b780c3fe2` | 0 |
| experimental/cpp-serializer/src/amqp/schema/restricted-types/Map.h | 1346 | `443b00d67c69378e95921168ecc80c10050818e2d17823a0e5f9199d4390da56` | 0 |
| experimental/cpp-serializer/src/amqp/schema/restricted-types/Restricted.h | 3902 | `12cabe155131406fd298fe864f06a9e33fba6d0c6bca926e6510354b42ffece0` | 0 |
| experimental/cpp-serializer/src/proton/proton_wrapper.h | 2523 | `c44e829557f6da6dc212ea3ea4fa3b0ac9771d9f14b01f0294e21c7830535ce5` | 0 |
| experimental/kryo-hook/src/main/kotlin/net/corda/kryohook/KryoHook.kt | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| experimental/netparams/build.gradle | 1220 | `c011fe3d6bf68349eb70cf835e49e6417f234370b87e25a95cc2c4b43426e9b9` | 0 |
| experimental/netparams/src/main/kotlin/net/corda/netparams/NetParams.kt | 10121 | `b03fdef6e746a6f91252cf3bd8c0cc3f1318120d1de8fa76e3a823817a84a475` | 0 |
| experimental/nodeinfo/build.gradle | 1142 | `e909327e78104c2ca55e0632e4e435cb64f060a2dc68b6c914df7530443020a7` | 0 |
| experimental/nodeinfo/src/main/kotlin/net.corda.nodeinfo/NodeInfo.kt | 7528 | `239d7600c46e2bed6b3894f971fce1decbd9d6ab00fa8864139027bd342b7749` | 0 |
| experimental/quasar-hook/build.gradle | 950 | `ca827fe55a63187ebe7fe859979598cf2efe75189edd8f03b5f6192597ddbefc` | 0 |
| experimental/quasar-hook/src/main/kotlin/net/corda/quasarhook/QuasarInstrumentationHook.kt | 11925 | `f69cee99180eb8eb5fd81c6e738e2130ab474209a7efe040ae07e3527e8ab783` | 0 |
| experimental/src/main/kotlin/net/corda/finance/contracts/universal/Arrangement.kt | 2244 | `41c129491c8bbfa5ec73a8fc89ff324163eb898f65f2b54ad2ecb7571272119d` | 0 |
| experimental/src/main/kotlin/net/corda/finance/contracts/universal/ContractFunctions.kt | 1310 | `d5915e3e0e9a8c01dfdb7c0e7647861e99cf431ce283c957a4530128537ee147` | 0 |
| experimental/src/main/kotlin/net/corda/finance/contracts/universal/Literal.kt | 5517 | `484301804085210e841577579e60aca23fd2652b0616f6a72a8daf78ddb0f220` | 0 |
| experimental/src/main/kotlin/net/corda/finance/contracts/universal/Perceivable.kt | 9279 | `7c0c17afe54bed7f311fd082aa0485995b90d36e7a00b63cd2fe7adbb750821d` | 0 |
| experimental/src/main/kotlin/net/corda/finance/contracts/universal/PrettyPrint.kt | 7164 | `8789ce79c1b9b84482063c38ac8fae6ceb9dfb9cf9a53163713456412afafff0` | 0 |
| experimental/src/main/kotlin/net/corda/finance/contracts/universal/UniversalContract.kt | 16645 | `1d916f6b3cb5bde0a6a2f8dd76e33c8f389137eaad7f933dd3a9da7d3267444c` | 0 |
| experimental/src/main/kotlin/net/corda/finance/contracts/universal/Util.kt | 9557 | `0df852e0d61a9b6c2883536d14d687f05503e550e99c15a660765f0e32d097bc` | 0 |
| finance/contracts/build.gradle | 2636 | `c6cf093068a8c56a96c7b01e68f95b921993d4f98290f9d6486321698ab40ab9` | 0 |
| finance/contracts/src/main/java/net/corda/finance/contracts/ICommercialPaperState.java | 965 | `712f13da117f328bdd662aa4b786ecd950ab00deb85d9f35c0854f6ae7ebaac8` | 0 |
| finance/contracts/src/main/java/net/corda/finance/contracts/JavaCommercialPaper.java | 9863 | `b07563e6b6817dc4e7d92b622fc6ec2e429a682e74b6a74ef1e0bdd1ea00e9d9` | 0 |
| finance/contracts/src/main/kotlin/net/corda/finance/contracts/BusinessCalendar.kt | 5719 | `be6832cee9d508304eb889c6027245f951b8725444955551facecb810fed30aa` | 0 |
| finance/contracts/src/main/kotlin/net/corda/finance/contracts/CommercialPaper.kt | 8979 | `c55a9ffa9e5e30ce4b8fef3eae3a405f45b2c52b442c4c3a188bab633e7e819c` | 0 |
| finance/contracts/src/main/kotlin/net/corda/finance/contracts/FinanceTypes.kt | 11626 | `0f4b81e8c14d7ed939db093e5d6995849f6ef56b0e5a46fba98931df5cbf8e7d` | 0 |
| finance/contracts/src/main/kotlin/net/corda/finance/contracts/asset/Cash.kt | 13338 | `0aa9b04002aa2421956ef2d2bdd13ddac71ca8c3a383a1ddece6abb8e0c5dfbc` | 0 |
| finance/contracts/src/main/kotlin/net/corda/finance/contracts/asset/Obligation.kt | 28575 | `376f353e356c40d5d58f7dcf5757fe40a7026e0b7f55124d597f009a8ca5a8bd` | 0 |
| finance/contracts/src/main/kotlin/net/corda/finance/contracts/asset/OnLedgerAsset.kt | 23116 | `b0d8804c6d73e0acb3ba11806daecd1afeeddfbfb52ec6e70c439e3fe56bfd46` | 0 |
| finance/contracts/src/main/kotlin/net/corda/finance/contracts/utils/StateSummingUtilities.kt | 3366 | `4ac43625cce48764fd3b9ae7e2463c67726de5540e6da419a7e3e5c9cf83bb2e` | 0 |
| finance/contracts/src/main/kotlin/net/corda/finance/schemas/CashSchemaV1.kt | 1803 | `c38acd78966041e4cce2d338df95e3e9c648d12907322ce5622ef16b13154c4c` | 0 |
| finance/contracts/src/main/kotlin/net/corda/finance/schemas/CommercialPaperSchemaV1.kt | 2467 | `8b988fc965c4af8b5012d4c5141356c989feb2ade46e4c4fe7530e4a64e966f1` | 0 |
| finance/workflows/build.gradle | 3452 | `2b405142d26234670b763e6624a51e06ada6395a2e4d15d61cc7e8a014d1a3fb` | 0 |
| finance/workflows/src/main/kotlin/net/corda/finance/Currencies.kt | 2418 | `12dd29b9c545c765248210e63865f185987dbb899c94235be42dc04181d049e5` | 0 |
| finance/workflows/src/main/kotlin/net/corda/finance/flows/AbstractCashFlow.kt | 2363 | `ce3f780b6f52cdc601b77ab6756d9482880a12278e16919d94caa4f375ecf382` | 0 |
| finance/workflows/src/main/kotlin/net/corda/finance/flows/CashExitFlow.kt | 4450 | `94d0894f764d88f0962fa0d1b46b46d39f995e6ca2af773baadedd7f14c947e2` | 0 |
| finance/workflows/src/main/kotlin/net/corda/finance/flows/CashIssueAndPaymentFlow.kt | 2791 | `872f80dc332c45280543e90a4ff94de1d563f60e5e23006816915b1ffa72e54c` | 0 |
| finance/workflows/src/main/kotlin/net/corda/finance/flows/CashIssueFlow.kt | 2774 | `48c7e202af37cb4bb3a58daba62d6444808e25027843555f8642d7f33f5dfa55` | 0 |
| finance/workflows/src/main/kotlin/net/corda/finance/flows/CashPaymentFlow.kt | 5239 | `2567616c0d359e928d5151224a90449156f64874d66fe40692acd0ba8553d306` | 0 |
| finance/workflows/src/main/kotlin/net/corda/finance/flows/TwoPartyDealFlow.kt | 9451 | `4599db48d27a6bee1bf135ff9ed84e0ed94b69baaea528a5f0109a629088a5fc` | 0 |
| finance/workflows/src/main/kotlin/net/corda/finance/flows/TwoPartyTradeFlow.kt | 13142 | `6e91bed23d49ecda61f18151b9caf0b5f9f4d036205269915c9ffebe48eb7eee` | 0 |
| finance/workflows/src/main/kotlin/net/corda/finance/internal/CashConfigDataFlow.kt | 1859 | `84591a0dbee7dcfdf7c9bf706cac43b80b2b92fcc52725d9f0f6ed96f6b6e390` | 0 |
| finance/workflows/src/main/kotlin/net/corda/finance/workflows/CommercialPaperUtils.kt | 2785 | `40184011dc97a6c97826c65a0655268d0e698671bd4655c0479eccb6a519720c` | 0 |
| finance/workflows/src/main/kotlin/net/corda/finance/workflows/GetBalances.kt | 3458 | `66d8c519fb212ea385ed468248b10268f0c4dd95471c0cb3dcefa2c1e4bcd6c0` | 0 |
| finance/workflows/src/main/kotlin/net/corda/finance/workflows/asset/CashUtils.kt | 10520 | `d78f6a24b2b83da999d4a757c0be326beccf2ada87f5b6ac2537e08f1bc89611` | 0 |
| finance/workflows/src/main/kotlin/net/corda/finance/workflows/asset/ObligationUtils.kt | 14972 | `074fde272c233a23ddf1768f39240e3a8df8469d40972e0412d6c416419e4ef2` | 0 |
| finance/workflows/src/main/kotlin/net/corda/finance/workflows/asset/selection/AbstractCashSelection.kt | 9927 | `1699b1a0071cbad98b02119e547336dd4c8aaf6f51b5d35b7e444484990fc925` | 0 |
| finance/workflows/src/main/kotlin/net/corda/finance/workflows/asset/selection/CashSelectionH2Impl.kt | 3931 | `30b43ad56415c3593157af06b54c4f3c26d81343a40d0e4c9b4a4978e550cf06` | 0 |
| finance/workflows/src/main/kotlin/net/corda/finance/workflows/asset/selection/CashSelectionPostgreSQLImpl.kt | 4330 | `efa309fa3894dd7b43144bdc0c5e6b434953cce9859b0be7eedc84f6c8f294f8` | 0 |
| finance/workflows/src/main/kotlin/net/corda/finance/workflows/asset/selection/CashSelectionSQLServerImpl.kt | 5144 | `5ab46b9648dbd5fb3110e45e20f1e2c6b3ebf04adf2de7baa304f83fe522a659` | 0 |
| finance/workflows/src/main/kotlin/net/corda/finance/workflows/utils/FinanceWorkflowsUtils.kt | 722 | `4a86a7b8a30e38b0ce4fab1dde56d026eee0794815d83a5b05d6b7a1613b1b2e` | 0 |
| isolated/build.gradle | 684 | `e2b1f537de5bdf2e1b6dd3eccb94be57fc2ab938451cb9300befb8b9dc301416` | 0 |
| isolated/src/main/kotlin/net/corda/isolated/contracts/AnotherDummyContract.kt | 1254 | `e2d8169ef5e3af4c164d5b15b35e517a911f987627609665ac0705a0da945fe5` | 0 |
| isolated/src/main/kotlin/net/corda/isolated/contracts/DummyContractBackdoor.kt | 414 | `f17ff20b7885830f98508d5be673a5a6686468acaeca8be46ad5ab501e4ee813` | 0 |
| isolated/src/main/kotlin/net/corda/isolated/workflows/IsolatedIssuanceFlow.kt | 889 | `f2e34c7e9c07b37f2a54288230a62b8fe8d10b5334560de460d76f8ca87f0b38` | 0 |
| legacy411/build.gradle | 998 | `258e14cb2829afa100e7f4b34e2c9d3cd4f94db4b5f28712ebed3d7f9db6bc39` | 0 |
| legacy411/src/main/java/net/corda/legacy/contracts/AnotherDummyContract.java | 3831 | `0d237f8318c68840e587af2a9508b43fe1a1985b1535503a8c03cc4497246f15` | 0 |
| legacy411/src/main/java/net/corda/legacy/contracts/AnotherDummyContractWithSystemEnvVarDefined.java | 4189 | `760e543d100f479dcedefbb9d03f66f053381e1f1d230552735fa62254942126` | 0 |
| legacy412/build.gradle | 998 | `ae81f1f05bdfe447bb141b09240d8d75b50dc82d9194f1a55834519d9f885b3c` | 0 |
| legacy412/src/main/java/net/corda/legacy/contracts/AnotherDummyContract.java | 3831 | `0d237f8318c68840e587af2a9508b43fe1a1985b1535503a8c03cc4497246f15` | 0 |
| legacy412/src/main/java/net/corda/legacy/contracts/AnotherDummyContractWithSystemEnvVarDefined.java | 4189 | `760e543d100f479dcedefbb9d03f66f053381e1f1d230552735fa62254942126` | 0 |
| legacy412/src/main/java/net/corda/legacy/workflows/LegacyIssuanceFlow.java | 2300 | `d4faf5ce1615ce946377ac7537de7d511a353b74b6a61a6d900abc7676898754` | 0 |
| legacy412/src/main/java/net/corda/legacy/workflows/LegacyIssuanceWithSystemEnvVarFlow.java | 2401 | `190ffa0bd4bde2e85ca3465e8ef2540a8c921d512ea9a82cfeb8a8de8a3fd226` | 0 |
| node-api/build.gradle | 4726 | `231a98b278092da126b8d5fad2881ac52b4a32f588cf1aac5834c399558cf149` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/BrokerRpcSslOptions.kt | 138 | `b50669e4b384ffdcce78f511af20cec15e1151bb9185c8162cea756d6864ec86` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/RPCApi.kt | 19943 | `2afc4b37af8582f29c5a145e9e31e19c8e7ccb38f3d1b7a623364535a4a582ff` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/exceptions/RpcExceptions.kt | 1886 | `57cade233dada604d4a1fce0828474aece15f0e0a182dde46bdd65b2a5037d9a` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/ArtemisConstants.kt | 109 | `adcfa43cf82fda99bbdfefc6b3b5913d99c8e4f98767abfb196f6528c13c9bba` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/ArtemisMessagingClient.kt | 5955 | `180e1f07094ee9c65516e84767f101d3128c826c552af2ef39db749353fce5a2` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/ArtemisMessagingComponent.kt | 7424 | `f847f6c95a8ae43d1b5508cff302a4ffd0638d53aaf254ce21c1d6d29b0a87e5` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/ArtemisTcpTransport.kt | 16430 | `039574aa6a9051c720d1f0f7e98dedb556e22a5f3c925c4e4c49ec3deef80bfe` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/ArtemisUtils.kt | 1828 | `769d586ce1566f08b09ca84cd5c9d5c8b642f3e59813fc3348c6aad4d70b1bc1` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/ClientSessionUtils.kt | 297 | `7d46b89143a51364aab6d893e8d8079dc1ee869ba2765ec8a1603ebbd8ea1853` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/ConcurrentBox.kt | 732 | `a75465e3f71f43b02c1cb0317dd06bd0b500fdd92ef03a071321da6d423582c9` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/ContractsScanning.kt | 2549 | `c34ff443cca3ea0eb366eeb53f52c7615a11d422d34b3fb85ac69cc6fb67c37e` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/CordaNettyConnectorFactory.kt | 3711 | `3f9b7658972d2244de21dda7db09664a81c9d36cb7c99eaf2484498696c1f845` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/DeduplicationChecker.kt | 1300 | `4354cf536ca8400cd859f2c730995ccdfa2f589785b3772a54639d6b2291162c` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/DevIdentityGenerator.kt | 5755 | `3a383156386e3b40f87884fe0b21c12a6c42f8f4fa9d55a156c1ca1afd5e930a` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/JVMAgentUtilities.kt | 963 | `15b5c1fd82c9b1cc3ce43c70005928a2529009a9e4426b6f02555bb839c019a6` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/KeyOwningIdentity.kt | 1475 | `74dfa3c37f65d5b14d89c1da670d0437baa809f61a1afd38220c03593a127544` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/KeyStoreConfigHelpers.kt | 7869 | `efc445947784ad7f5b9ea515b1be78e63ba2e9b71be1b2e562987755e47a1751` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/MessageSizeChecksInterceptor.kt | 2542 | `5fe27532b472e16276d7bf925bea20ef0d2f9e05eee936ffb0ca1c664fe5592c` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/MigrationHelpers.kt | 1383 | `6e0f24a0cd83422fe7bf50f7ccb1b8dd78763f7ef3a50b78ec42330fb2abd3f7` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/NodeApiUtils.kt | 1257 | `5e7140d9c33c7fe48da6a4ce760befa55c38d2c980a2f96602392f219dc1105e` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/NodeStatus.kt | 124 | `95888ddef1178ae90990c666d33c5249c9dd6699e12cf1a5fc37195b1c6f26cd` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/PublicKeyToOwningIdentityCache.kt | 517 | `60af57949a78d34bc8572d6626489a380b8dba114371a914cb5df2f128c22bb2` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/RoundRobinConnectionPolicy.kt | 739 | `ea2ae667ec40aaedcf5198d3628d19568dbcda57a92e3b927458d6b5f4e68743` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/RpcHelpers.kt | 666 | `ea5719fcde9afa5c0ad1fbcf8d6d19f4ebe4e167cca1a572acfe2e1766c4fa6f` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/ShutdownHook.kt | 789 | `14c37064ebcdf88c82153f06ccea1056d3e09ad6c6ba1f66ab0dea118ce622f1` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/SignedNodeInfo.kt | 3202 | `085027a8cf9fe97133e08b8d90fc1eea5d42072f01491400b0681f36c8220bdd` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/bridging/AMQPBridgeManager.kt | 26989 | `f9a034506f71cab6e2f3f8452c745d542b5ccf947e3f766b77744f47a44e5462` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/bridging/BridgeControlListener.kt | 12806 | `d5e00ece116b68cf89cf9759be4c57b27d10747e244f3f7a60dc8df89f99b972` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/bridging/BridgeControlMessages.kt | 3639 | `199979d525b2bc2f956ffabf020e24699cc535c2934c965fbe9d0873253413ed` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/bridging/BridgeManager.kt | 758 | `c637682d0a9625394505d09b5d40b2ca9dee7da372420947c0a56a4ed867b4a4` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/bridging/BridgeMetricsService.kt | 809 | `a12b5bf1fa1db48d7f5537fc1639e5291b9438771334eb9a9ec428f55ccba870` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/bridging/LoopbackBridgeManager.kt | 11215 | `7ef2ccb71fe939fcfb625c309d3b0c887ac7ad497343ea82f1bc3d08d50ae41e` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/config/CertificateStore.kt | 3960 | `fcc650ad6581c222dfa60700b0a3b909a686e1d203c8e138c9d4cbe8ecb591b4` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/config/CertificateStoreSupplier.kt | 768 | `3a33374d8fddb8c943b4dd1b2f745bba875f18295174003e9b927f1ad8e12ce3` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/config/ConfigUtilities.kt | 14706 | `c517c844c8574a2a455edf026287ac4cedac7f319b63eafaa28de65b9b83f26a` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/config/MessagingServerConnectionConfiguration.kt | 2726 | `4068f02e170f51c4c38e8ab39a5ae72c16ba06becf334644eb56370e0a0d2153` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/config/SslConfiguration.kt | 1357 | `01b18b506106f29b66dd1b6bc8a760c76ebb1507cc37f4a564ada1958e27534d` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/config/User.kt | 290 | `734dfd492c6bd6c2cf3f5ee8d5568a1b48811a62a2cf2afdd7674d3085508b41` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/cordapp/CordappLoader.kt | 879 | `f7ef262510a03bf12c63391f58990f01f5bca453b85a8a64ecdf29e36a1d1180` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/crypto/AesEncryption.kt | 2901 | `bc24d67e2bca70a59dedeb2fe45f6460df2d5b6de3c13d3fbe9a4fe49830414d` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/crypto/ContentSignerBuilder.kt | 2777 | `a6abb731da5babbb19688316a1e57abe0effe049bb8dd6ecc3cae2667c6a5dbe` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/crypto/KeyStoreUtilities.kt | 7813 | `9daf7d5c3b64eb234fc06f7d4a1532599aed15d54338a87805b2e7bec6247f13` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/crypto/NOT_YET_REGISTERED_MARKER_KEYS_AND_CERTS.kt | 678 | `d0241aa19e69653a96c60cfd85c26c5454ec9df851eeebb2a6943b150ad6cc85` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/crypto/X509KeyStore.kt | 3935 | `12b1ad987129a5bfb1b4e045c372304300cc426500f3f8d0d0ddb9cfeed15ff9` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/crypto/X509Utilities.kt | 26285 | `48f8f548369b64b5c307d9be1663d16226ce6e26fc98a0e38f4cbdc421e5b9d2` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/cryptoservice/CryptoService.kt | 7711 | `4ea4fcfa338bf704c3f306cf875c94bb77e452a607e3c4de92e41eec43d4052a` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/cryptoservice/DefaultCryptoService.kt | 11955 | `85a9aa6e746282b3ea0689a4949de9affe1acbe16a18b8c5efced6acb87c1f3c` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/lifecycle/LifecycleStatusHelper.kt | 1056 | `b4fd0984d4e633ea2fdcb4319982c1ebdd7b2b8f44a8ad4124def3d283607451` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/lifecycle/NodeInitialContext.kt | 328 | `a2a3b9d686b444b32fc7916b1022353a937ac73661fbf6bfa9ce85a200f9c1ac` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/lifecycle/NodeLifecycleEventsDistributor.kt | 5887 | `0a20c7fa5482a17c5e373bf3b3c8d344e290edc7223890c04684592b31573b0d` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/lifecycle/NodeLifecycleObserver.kt | 2933 | `5a5d659aa33200483cf12cf8afc5bc7080be1f107cdaf701f32a0f2f93fa9f41` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/lifecycle/NodeServicesContext.kt | 627 | `2e9bfd5f179c56952d60ae0876ea72047876463812803e6a366d5e591354845e` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/lifecycle/ServiceLifecycleSupport.kt | 1692 | `2426ba5faca5732d94af048131e57d933c454a7d5798d9fccfa8b61ffccb678c` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/lifecycle/ServiceStateHelper.kt | 1865 | `243c0cc4e3bf68f755eedbf86a9d4f7887a4f1c5e18b9c11ae0346db35007ee6` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/network/NetworkBootstrapper.kt | 27726 | `c65d1f1f5f54deed41e6258c718ff198f73f23c1f789031b992cc093755e148a` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/network/NetworkMap.kt | 3621 | `bdc0ddfda18ebf88649bbcfa49b6229e4b218474c1280f81f1e26a95b8a6cff7` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/network/NetworkParametersCopier.kt | 1610 | `1301d4567220e127fd79ee566cc72ed71126600752385669a4e476230d507ebc` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/network/NodeInfoFilesCopier.kt | 6502 | `1967bc83430aa56174c7a1087c717b1e271c70585f6ec715eae8be9b1d8da1c6` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/network/WhitelistGenerator.kt | 2715 | `2693b1fb70778427485a2264e89449dbf3f1561e2bbfb66359608a67019c8e1d` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/persistence/AttachmentVersionNumberMigration.kt | 5132 | `910d9b1e51b25b66ac637af98a0886f09e73d0a93b373bb7560f704f704c3f92` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/persistence/CordaPersistence.kt | 20445 | `0c66533cf7a2d0d8780199c32d299936f414fbed9c616be291fea404d727068b` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/persistence/CordaTransactionSupportImpl.kt | 986 | `78257bbcbdedfa097c496d7d6054ec20ccd660abfbb0f8559b49c6dba3009520` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/persistence/DatabaseTransaction.kt | 5278 | `bcd2d21873e8e4ff113f7e75703b562eaeff711a8e6d01e490c56f5027336582` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/persistence/HibernateConfiguration.kt | 5273 | `c432c538afb932613189d275726dc2d2a8ed5a75c3f77aa946d1e127b9b6ad1c` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/persistence/HibernateStatistics.kt | 6745 | `15c96e7f093c8f36ead9f9ac2d2d8c7461bc4cdc162ff4a02061d683504207dd` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/persistence/LiquibaseDatabaseFactory.kt | 228 | `bd03596781b053adaecffd688e44ae1ee12dce858a4cf38389ca81f653384152` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/persistence/LiquibaseDatabaseFactoryImpl.kt | 399 | `741770e4db270f4959c53571b7fbe2c8a18083fe4b801aaa390e52ade4fbc3bb` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/persistence/RestrictedConnection.kt | 3216 | `c0dad0786fbb0517e3accdbd57bdd37bc1c589db9da75422c01851e7d3388839` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/persistence/RestrictedDatabaseOperations.kt | 1809 | `fbba7763b21a4cb38c9a87c25880c05300dfe7dbc9b6ef897d92bc8e8098077d` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/persistence/RestrictedEntityManager.kt | 2565 | `66f16f78f5ce1749afaba798470f0c965ee7e56cfb95f02be18ae64efbd792a5` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/persistence/SchemaMigration.kt | 14486 | `d351a259846f2cb8e5973ee5a315bbc7c245419ad4025c4ae4c07de46507ebfc` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/persistence/Slf4jLiquibaseLogService.kt | 385 | `5a104a4d57a5ff440e61d42c9899dfabb1b4638d94b43ec27388e5af0a012219` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/persistence/Slf4jLiquibaseLogger.kt | 2277 | `d9cb6da932e179bfa1d39a17a8b46c4d5b8a53ac079a83f50260e28f84569cc1` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/persistence/factory/BaseSessionFactoryFactory.kt | 7148 | `f47892182b00431fc0c5f11e6a9f0d5219ba98d22827f068894aa0c6b9d73224` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/persistence/factory/CordaSessionFactoryFactory.kt | 827 | `e2439d91cded7575f0687f3e3a0e04bf8ca200cef38ae211f3d7683db7cbc848` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/persistence/factory/H2SessionFactoryFactory.kt | 262 | `b4af1e24736ed247527c687e95fdf1afaa2c726a82990b04d767c13513b5dec9` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/persistence/factory/PostgresSessionFactoryFactory.kt | 1950 | `b6bf408bac27f033adae1b387ac2ef0b013726cce62c5e4c0599c8ad4eef2fb3` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/protonwrapper/engine/ConnectionStateMachine.kt | 25046 | `0dd3f5c8fd667817ff30e559c2cfc81d4ca0ba5137bd9375bd8ef062e26a1508` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/protonwrapper/engine/EventProcessor.kt | 7197 | `1d0e0654b1b1d1739e57757d8684921121bd708435f5b25800f980d661b4f8ff` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/protonwrapper/engine/NettyWritable.kt | 1732 | `45af4eab3e70f97665a590341f09d6eb33945c2e4cd442ac857529f3073e02f9` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/protonwrapper/engine/SessionState.kt | 694 | `3bee045591e430838d38965ecbce1f853dea9da17870fe06698366b27c75017a` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/protonwrapper/messages/ApplicationMessage.kt | 434 | `2e528b6c6def793d5b072e3b5e1aa95003789a6512ace16184afd379dcc374d7` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/protonwrapper/messages/MessageStatus.kt | 186 | `f02ce2653a55fd1f069f3057e94d6bca34a76b59bde886ec3fe19948b796b797` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/protonwrapper/messages/ReceivedMessage.kt | 349 | `8b5d3fe2eaf8c99d4d1f360ffc395818b0de2803c7248da652d1f15b5e5f6821` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/protonwrapper/messages/SendableMessage.kt | 280 | `0cbb7a82d0c7fa8a213dd6c593f992fdc287ec026878fbc70c46e1b6ff4ab472` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/protonwrapper/messages/impl/ReceivedMessageImpl.kt | 1953 | `5c24900b565fb81814d9f7056713c5092bc8de35e1224c88458042eedbd9250c` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/protonwrapper/messages/impl/SendableMessageImpl.kt | 1625 | `34e3ec8220dbb397c78ccfaed3351b66cf695956c9bf876c97c2f99de8d2635c` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/protonwrapper/netty/AMQPChannelHandler.kt | 14999 | `7fa97ad10dd6d691d6db4b37fac57022147983f008b2f976bd90b1a0ac8871f0` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/protonwrapper/netty/AMQPClient.kt | 17840 | `b93674b5fffccffd8106c58190b63c6d11192d19b4e7980282df33045b178fe5` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/protonwrapper/netty/AMQPConfiguration.kt | 2682 | `1bd9fb7e132d56355badaed7fb2ee5242f885ef8fc29095fa2666ee219804b59` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/protonwrapper/netty/AMQPServer.kt | 10362 | `c6046532473d30a46e0016aac84aae3ee4233195c03f235efc590e7b7af9bc27` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/protonwrapper/netty/AliasProvidingKeyMangerWrapper.kt | 2424 | `0b2ae4e0c7ee4acf53dbbf9dfc401f2e78bce85b484b08faff6acf3b81b9f064` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/protonwrapper/netty/AllowAllRevocationChecker.kt | 1039 | `d458511d8b183893ba2ec8e70a037b1db4f08733de405d7ec1f4dd92e5d0c541` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/protonwrapper/netty/CertHoldingKeyManagerFactoryWrapper.kt | 3256 | `2726566c112f1dd9f65414dbd73bd8e237eaa99aea8dc8eca1f2e007f29ff371` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/protonwrapper/netty/ConnectionChange.kt | 520 | `662d3f1bb2c30520f7ebbd0d957077b005d448dcd9f609ae234198d13e894edc` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/protonwrapper/netty/ConnectionResult.kt | 124 | `6cbb1a7a6e2d46d17d177b62435fa82d3fcce561714f9f5ea9486ddb1d9c76f7` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/protonwrapper/netty/CrlSource.kt | 347 | `1f1de9b1141d4d63bd7677e32c12c8a2ffb62626c01735037275c8a2d76e71f3` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/protonwrapper/netty/ModeSelectingChannel.kt | 2974 | `42ff6637b81f030d55d14ed68a40dde086f7d78cf1f34c70dc8d9a870b9aa97e` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/protonwrapper/netty/NettyServerEventLogger.kt | 2925 | `68feaf1d7b619d080105c2ddf3c205d8618f2940159d7abd3462d595c1984f63` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/protonwrapper/netty/RevocationConfig.kt | 2637 | `f71528d177878eb080b616e55c92bff06b5e553275f430a3e09b0892780df539` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/protonwrapper/netty/SNIKeyManager.kt | 4293 | `ffea0c80f2b63981902a6a6f48156545f919d196d139bdc64095229457d81439` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/protonwrapper/netty/SSLHelper.kt | 17035 | `ff1faebd2ac268593f88d74da43c7114b795acfa02eb2f6a5fa4d978861d8062` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/protonwrapper/netty/ServerSNIMatcher.kt | 1955 | `ae4f0a67795701a75f0b0b888e6f0aeb0777942ce2b01341db8e54d712d63ce1` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/protonwrapper/netty/TrustManagerFactoryWrapper.kt | 1080 | `a245a18a725639ca0082826caa4112be3430bf97b84cfbf14298b14d4a9109a8` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/revocation/CertDistPointCrlSource.kt | 5271 | `829dcaa30e5db36629397422af1a08be1ba336980d3c2c596b1a72cafd408b16` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/revocation/CordaRevocationChecker.kt | 5433 | `781d6b92c287cbf313894d2cf739bcac678098b467e7498fb0d386fbe6669277` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/rpc/ObservableContextInterface.kt | 924 | `48ac06b2aa7a10dd7b657a1216d26c6efaeb6e99e503323c14fe54b55d280b84` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/rpc/ObservableSubscription.kt | 135 | `10938d178f67797692bf7584170337d5a93a677c5768c1e92257e5650e1c52f4` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/rpc/client/AMQPClientSerializationScheme.kt | 5365 | `005e2e45bcb200f25e27b7475260e80be48dc44a2df025533fbb25a0da7ff916` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/rpc/client/ObservableContext.kt | 1223 | `c3a4c9151e408116a01366fdceb7f0e7f086bb8c861f99f1af2dbaefc07cb980` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/rpc/client/RpcClientCordaFutureSerializer.kt | 1313 | `560cb8cefeb3c409e38722d94913a462ac8bbf4f72e647d700f017073e6d2cf8` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/rpc/client/RpcClientObservableDeSerializer.kt | 6244 | `6469d2a191184cf99c33650b996ff53ff41c82b08e7e0de3867f3e439282aa12` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/serialization/amqp/AMQPServerSerializationScheme.kt | 2757 | `7c5a5b4cd9851e66233a4c84422fcbb43d4d75dad240e219b33460e8e7904403` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/serialization/amqp/RpcServerCordaFutureSerializer.kt | 1194 | `82130bb6c53bc07810432172c977847fa5cc74143f60e7e5634e9606057c80d8` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/serialization/amqp/RpcServerObservableSerializer.kt | 6446 | `8e5779c553e935f1d0d1fdf5c914d3ebb7ed3fd198d62aa015a8127fd8457841` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/serialization/kryo/CordaClassResolver.kt | 10083 | `ea49ac4ecd993e26d817eea38ad280de6d34d9d8b004ed2fec6871d7be2bfdd8` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/serialization/kryo/CordaClosureSerializer.kt | 798 | `5dd307dfe72ee8d90c23b6bf8dbdda7d1d2ed1bfad25b5cf9a55ca5ac47ea321` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/serialization/kryo/CustomIteratorSerializers.kt | 6420 | `706d65a1f49625d377f84590d5a7ba2a1a4049584c497a217741733a0f297ad0` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/serialization/kryo/CustomSerializerCheckpointAdaptor.kt | 3772 | `78f0b957f7c691a771664b1674594e47c35c5038126373ca631a443740dd232c` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/serialization/kryo/DefaultKryoCustomizer.kt | 14178 | `355e296beafda8d6011a874cc456876579b41b0d91036bcff994e3cc24272dc1` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/serialization/kryo/IteratorSerializer.kt | 1988 | `bf57a70a3407825217109a72f3a708ec55ad5b42d25ea6e0d091a49b8208a59d` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/serialization/kryo/Kryo.kt | 22017 | `dfdd2cf5a5bde1cbc1ae5ee9225b37bf10f500f703dbe363f8baa35869c4576d` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/serialization/kryo/KryoCheckpointSerializer.kt | 9434 | `e2f2da4a62b477db4f05c7cfb306ab57b2884e33a4a31715344092dfc631ea9b` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/serialization/kryo/KryoPool.kt | 511 | `fc07022952c7207bc79124b600b4ffd888eff35ce31ce7e33f0b60efde439171` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/serialization/kryo/KryoStreams.kt | 1314 | `0eae2ae8ce659773a00cebb869297e0dc3dbd6730009996aa638b06468e415f1` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/serialization/kryo/SerializeAsTokenSerializer.kt | 1526 | `86bf7baea69914183e3b5f4d8e6660fc33b2db4e97b42b9dcd959d3e43d29e51` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/internal/telemetry/OpenTelemetryComponent.kt | 18527 | `5579e101984ddffce2548bb6100a2559675b0164086e9e03c018eb290e4b74b3` | 0 |
| node-api/src/main/kotlin/net/corda/nodeapi/notary/NotaryQueries.kt | 1130 | `5d351dc19a35d8ad1191f378de23b0c2474efb39132602caf553fcba03be019e` | 0 |
| node/build.gradle | 17758 | `c54257552dec17c5d7b2f3a11a37ab9673fb347c5a1e2c510e82e2434a75de70` | 0 |
| node/capsule/build.gradle | 4489 | `38a2e9261a5a9abb57a786a11d1104acffb35a6473d2f15c3613fed41d661f9f` | 0 |
| node/capsule/src/main/java/CordaCaplet.java | 12370 | `3bee0b8429b0bbf59503df66e9fb362c0dc09757d1c16977b78421ee60a07926` | 0 |
| node/src/integration-test-slow/kotlin/net/corda/node/services/rpc/RandomFailingProxy.kt | 3371 | `562e2228bffa121abc91ec7646ec4b56c992ff3b10157de7fe8ec1e85605113b` | 0 |
| node/src/integration-test-slow/kotlin/net/corda/testMessage/MessageState.kt | 2611 | `ba433fd699f2c6f0bca6f25e8f4f336ead084b5db4b695f88ca1df080eee08ac` | 0 |
| node/src/integration-test1/kotlin/net/corda/contracts/incompatible/version1/AttachmentContract.kt | 1793 | `1109a8418c775bbc806916f58f1bec75eb863c0c88010bf2f4ff53399163cb67` | 0 |
| node/src/integration-test1/kotlin/net/corda/contracts/incompatible/version2/AttachmentContract.kt | 1074 | `c917c025f7c4243389632c171036a3ce661c6d0727f09244a0a1659d49af98b5` | 0 |
| node/src/integration-test1/kotlin/net/corda/flows/incompatible/version1/AttachmentFlow.kt | 4085 | `242bc206b440fa22c00e38939862a976050102efd5b43d3aa3e61480b074ff5b` | 0 |
| node/src/integration-test1/kotlin/net/corda/flows/incompatible/version2/AttachmentFlow.kt | 2547 | `aa21cb6a715bbebf5a3a6ba0dc1955834eda331c67e927d2e83ae4c7b331277d` | 0 |
| node/src/integration-test1/kotlin/net/corda/flows/incompatible/version3/AttachmentFlow.kt | 2361 | `634537cff423221b0dab140f8a582a4469aea1d01fbb21a224f2a6f1586c7e22` | 0 |
| node/src/integration-test2/kotlin/net/corda/contracts/serialization/missing/CustomData.kt | 545 | `296ecee4abdc91e4f4edc52b8f019bbad792b0b9dd7531a360849f581354bcf3` | 0 |
| node/src/integration-test2/kotlin/net/corda/contracts/serialization/missing/MissingSerializerContract.kt | 1196 | `5d43556e29b2fb817be4ddcfd1e4098f4c5a50623b06f80b1bb6a6c5af8e8fc4` | 0 |
| node/src/integration-test2/kotlin/net/corda/flows/serialization/missing/CustomDataSerializer.kt | 476 | `96f20f6c1250080231677c76e430f7b65140fdf1ede6303ee55bc13a364aa2ed` | 0 |
| node/src/integration-test2/kotlin/net/corda/flows/serialization/missing/MissingSerializerBuilderFlow.kt | 1120 | `526627293ee317ffcf69e0be8f6932704d328ede126ed784b302670a492b2286` | 0 |
| node/src/integration-test2/kotlin/net/corda/flows/serialization/missing/MissingSerializerFlow.kt | 2655 | `9a7e4ac0217926a72eda070271b91af7c3d6b28de39c253720784c6e5eab9ac7` | 0 |
| node/src/integration-test2/kotlin/net/corda/node/flows/QueueWithCountdown.kt | 763 | `640fdec4a87e4efaceec082dac14e8a53ebe715f26d43d366c948f793f9a53cb` | 0 |
| node/src/integration-test2/kotlin/net/corda/node/services/statemachine/OldFinalityFlow.kt | 15942 | `02304beed282c59c9e5264822e4301ef81b50ef5fffb448b315ad4ef27d4b0d7` | 0 |
| node/src/main/kotlin/net/corda/node/Corda.kt | 643 | `758186f320fce0520e4173b13aa069b55c197fcafcbc397a34a15c99748b5c04` | 0 |
| node/src/main/kotlin/net/corda/node/CordaClock.kt | 2992 | `2b2b5e4ee91c00abe4225dbee9070c592a2cdb13d061cc100491b465a6e2aa93` | 0 |
| node/src/main/kotlin/net/corda/node/JolokiaSlf4jAdapter.kt | 825 | `92019764b2d2facccda543c00fb522ef50f04681c936cca325f3846fe12c7ca8` | 0 |
| node/src/main/kotlin/net/corda/node/NodeCmdLineOptions.kt | 8724 | `8ac40acf46937ebd290d3982317eed224053a29df64076cffb78d860817ddbee` | 0 |
| node/src/main/kotlin/net/corda/node/SerialFilter.kt | 952 | `d43a338868d8d53054d055cd5ea0d3c606786203d5d9195c090c6f07ad65e4b7` | 0 |
| node/src/main/kotlin/net/corda/node/VersionInfo.kt | 825 | `bfcbbc8c5285dce6a4f10005911fde23cd26c5729c37fabd150a3b177fc5ed7b` | 0 |
| node/src/main/kotlin/net/corda/node/internal/AbstractNode.kt | 74185 | `d9c0f68893f4bd3dbfae83565721d46d95b370ddcc9e08af3ca752a84eca1a56` | 0 |
| node/src/main/kotlin/net/corda/node/internal/AppServiceHubImpl.kt | 6018 | `c60108442dfce903cfa783c716cbaad3c87af5a5ed512de71baca559ca561432` | 0 |
| node/src/main/kotlin/net/corda/node/internal/CheckpointVerifier.kt | 5811 | `21382c6fcc2e5dbb5536ee0bb9b1cee00a8b97e3b83c2e737c3485d1afe93f59` | 0 |
| node/src/main/kotlin/net/corda/node/internal/CordaRPCOpsImpl.kt | 21950 | `d626fabfc1266ce1a91242250a87d0a14fc5139fca2bd778b6b584168144580e` | 0 |
| node/src/main/kotlin/net/corda/node/internal/DBNetworkParametersStorage.kt | 8242 | `7f5787f1e7630bf89224289849136c7ea20979364d9e9241c6b4c5397ab8d2ed` | 0 |
| node/src/main/kotlin/net/corda/node/internal/DataSourceFactory.kt | 1631 | `b81c8a868b065c54a777dae9eb0e26b8749adbb5fdf653296b9d29061a8a3ca0` | 0 |
| node/src/main/kotlin/net/corda/node/internal/FlowManager.kt | 12197 | `abc79e2ca85704948a09e53659709295ce21f382e171fd64f09aa02c0d07ed19` | 0 |
| node/src/main/kotlin/net/corda/node/internal/GeneralExceptionHandler.kt | 1451 | `d4ba7cd30b2bbc6564fa4be2a1b415940b73f5651937fe663faf36694f08d530` | 0 |
| node/src/main/kotlin/net/corda/node/internal/InitiatedFlowFactory.kt | 681 | `f385ad272719410a5766006cd0bc28c10f46d119b1f3238a1b3f6c4eb003a430` | 0 |
| node/src/main/kotlin/net/corda/node/internal/KeyStoreHandler.kt | 11930 | `9a6a37092d86f587efca601e2a37f2cbb8d499cc470a88a3f648737b412c9743` | 0 |
| node/src/main/kotlin/net/corda/node/internal/LifecycleSupport.kt | 336 | `69e1de27ed0e4397bf8127c6cc129b80fb14da47f8f84d54420e1fd96f2b7e01` | 0 |
| node/src/main/kotlin/net/corda/node/internal/NetworkParametersReader.kt | 6220 | `04adf5cc95bb995595753c81007ee7fdc88bba371073685f7e6c02373291076b` | 0 |
| node/src/main/kotlin/net/corda/node/internal/Node.kt | 32226 | `ba175b35c7f2465323b78d198f0ec610c1423c1832ddb7141f95de7111e355f8` | 0 |
| node/src/main/kotlin/net/corda/node/internal/NodeStartup.kt | 32471 | `502b0194fce023463ab42f382e243b616430d070e3a8259118054e1381be8459` | 0 |
| node/src/main/kotlin/net/corda/node/internal/NodeUniqueIdProvider.kt | 558 | `e32aad2790dbce84bb75b60eab3b2ffad176ad682d2990cf8497347aa626dc9c` | 0 |
| node/src/main/kotlin/net/corda/node/internal/SwapIdentitiesHandler.kt | 944 | `04089bf57039e18527eb9e5da40bcd480c628b73a664b124d995dcdff4ca0679` | 0 |
| node/src/main/kotlin/net/corda/node/internal/artemis/ArtemisBroker.kt | 1084 | `2b2854d74e3f45cd3c034ef148196dd62022cd1c55a5571fbf14372e4b700db8` | 0 |
| node/src/main/kotlin/net/corda/node/internal/artemis/BrokerJaasLoginModule.kt | 11052 | `aad6072f7483ae774359f74e5ed3a5443543221934264c9a9128de051ab9dffe` | 0 |
| node/src/main/kotlin/net/corda/node/internal/artemis/CertificateChainCheckPolicy.kt | 3836 | `161d03eff145a984b0fcadc0a6d39cfad178672b81b2fc457c7ec20bd65f38b6` | 0 |
| node/src/main/kotlin/net/corda/node/internal/artemis/ReactiveArtemisConsumer.kt | 2947 | `7bcfb20abae996f112798d7a4ff2f936d21a908485c7373b51df2b898c31f6fe` | 0 |
| node/src/main/kotlin/net/corda/node/internal/artemis/SecureArtemisConfiguration.kt | 790 | `1b0950ee55de4b7c1abc2a69e88b18b6961f52f6fde26fab44170b8f24a6a5e1` | 0 |
| node/src/main/kotlin/net/corda/node/internal/artemis/UserValidationPlugin.kt | 2628 | `39d628598ea1c33ad26b7d22aa609cf97c407c9f544dc6cfe4ef98a24c4c85b9` | 0 |
| node/src/main/kotlin/net/corda/node/internal/attachments/AttachmentTrustInfoRPCOpsImpl.kt | 621 | `298d44e937a447514fcd2c634bc16e4605c940e9870d2a7f7b9e2f051a8728e5` | 0 |
| node/src/main/kotlin/net/corda/node/internal/checkpoints/FlowManagerRPCOpsImpl.kt | 718 | `e30e243798ce6189aaa0e8f3c7dc71d227b9e063d548cce17309c7848a860931` | 0 |
| node/src/main/kotlin/net/corda/node/internal/classloading/Utils.kt | 267 | `7df923204ede285a7bbba3ff14519fa2dfad3c5301c007a2464cb227653a9dc5` | 0 |
| node/src/main/kotlin/net/corda/node/internal/cordapp/CordappConfigFileProvider.kt | 1294 | `b4c0742449b3d92ac51dbf48cf14c7e5cab0d675a358ca49f62a7468180b5d77` | 0 |
| node/src/main/kotlin/net/corda/node/internal/cordapp/CordappConfigProvider.kt | 157 | `350f2d967f00aa184fb032dfdf3c02e883d7947e94ebfdfa9692e9a4ce2d790f` | 0 |
| node/src/main/kotlin/net/corda/node/internal/cordapp/CordappProviderImpl.kt | 6640 | `10ebf1bfa2f1e3b875f7c83db24883a06480c086ffbb2233ce0786dffcecb6f2` | 0 |
| node/src/main/kotlin/net/corda/node/internal/cordapp/JarScanningCordappLoader.kt | 26082 | `e67e32f3e8479c591f4776f7b6e17343c3ea24194461cbec9c7ed351506e722e` | 0 |
| node/src/main/kotlin/net/corda/node/internal/cordapp/TypesafeCordappConfig.kt | 2681 | `8460c32868f206dc233bedafea27870808ab0a26051178511bdfe494797dea25` | 0 |
| node/src/main/kotlin/net/corda/node/internal/cordapp/VirtualCordapps.kt | 6238 | `db08616c4661863ad475eb66ea621caaf477fb50f1b5f9acf47ec2fc6b1e4417` | 0 |
| node/src/main/kotlin/net/corda/node/internal/rpc/proxies/AuthenticatedRpcOpsProxy.kt | 3754 | `848553cfb8c4f97804a31588fbccade4817ec571223d8e75cdcd123c2e6b489a` | 0 |
| node/src/main/kotlin/net/corda/node/internal/rpc/proxies/ThreadContextAdjustingRpcOpsProxy.kt | 1665 | `53bb15002ceee2f8c35bbeb751d413d01e5509a32cc53260ab9a4ebc5cb7c520` | 0 |
| node/src/main/kotlin/net/corda/node/internal/schemas/NodeInfoSchema.kt | 4922 | `260ee87986c7d8b427f165832926715978e326a205f7760f75cc6ad26e3e8e2b` | 0 |
| node/src/main/kotlin/net/corda/node/internal/security/AuthorizingSubject.kt | 769 | `e1d2cce3b6942643d5d4b70316ee40549ef7c58dbb556c529d615368fcd26c4e` | 0 |
| node/src/main/kotlin/net/corda/node/internal/security/Password.kt | 1020 | `3fb68284765f34767008b2ff8bb3bd23d0c2d8c9522ecb0b6c575f2dba339e2a` | 0 |
| node/src/main/kotlin/net/corda/node/internal/security/RPCPermissionResolver.kt | 8795 | `5297c8ec682da3bedcef93c307fd5052898c177f6e5d4ee1fb11c1676a5b6a5c` | 0 |
| node/src/main/kotlin/net/corda/node/internal/security/RPCSecurityManager.kt | 1454 | `bc9750ec9f8996d0a9bca36d9fdba696cab856753807aa6041a53cfda7371928` | 0 |
| node/src/main/kotlin/net/corda/node/internal/security/RPCSecurityManagerImpl.kt | 10138 | `f4c4efb0615a623612925b3681b3f2c74e00f3c556bcce24d6561a75260339ba` | 0 |
| node/src/main/kotlin/net/corda/node/internal/security/RPCSecurityManagerWithAdditionalUser.kt | 1498 | `894fd0db7572b50f26a2edf4b705e1d1d6f24ab572c9598c7914bce5d955ef52` | 0 |
| node/src/main/kotlin/net/corda/node/internal/shell/InteractiveShell.kt | 3486 | `081c2b26f6fdbab259d9e82d48fcd80f02d25f7d38cb85b00bdc6d56e7e126da` | 0 |
| node/src/main/kotlin/net/corda/node/internal/subcommands/ClearNetworkCacheCli.kt | 647 | `001ac08234697524f42699d88290cc46a9782c05a67518c33e1e342142c8ca95` | 0 |
| node/src/main/kotlin/net/corda/node/internal/subcommands/GenerateNodeInfoCli.kt | 683 | `99ed11386fbdbe0dfc890340369145c0319a19ef6655d24da8c0797b88c7374c` | 0 |
| node/src/main/kotlin/net/corda/node/internal/subcommands/GenerateRpcSslCertsCli.kt | 4660 | `8203a3fa565bf52f129091842bf82ecc0fb5f7d74476a5e690fc19f786776545` | 0 |
| node/src/main/kotlin/net/corda/node/internal/subcommands/InitialRegistrationCli.kt | 6479 | `9eeb42398e38c0ac9d0c67b3b7ee0cb5f1c31b29c3477827c498cb4367798746` | 0 |
| node/src/main/kotlin/net/corda/node/internal/subcommands/RunMigrationScriptsCli.kt | 1383 | `f58037f92999ae15cdb389be27bf315b6dd8c3168239b42d35b783062817a66c` | 0 |
| node/src/main/kotlin/net/corda/node/internal/subcommands/SynchroniseSchemasCli.kt | 636 | `a0020520e753277edfc5340f45bc0dd6b1eb04da76fe710b48fcb5dbf9437ab4` | 0 |
| node/src/main/kotlin/net/corda/node/internal/subcommands/ValidateConfigurationCli.kt | 2153 | `7cb1fc2cbede30815401c623b4e631cd4f27bb1bee6ea40c222594c5f900c65a` | 0 |
| node/src/main/kotlin/net/corda/node/migration/CordaMigration.kt | 4717 | `3b1fa2b1cc905865488d7bb887a417e8dd733d9c8d5e3fd727e6d2627baf6f66` | 0 |
| node/src/main/kotlin/net/corda/node/migration/MigrationNamedCacheFactory.kt | 3544 | `872014d05c5a56183ed1e809d457e19a7fb57948deb3989fe9f6382f46f1bc22` | 0 |
| node/src/main/kotlin/net/corda/node/migration/PersistentIdentityMigration.kt | 3250 | `40a5112c4c3fe81f227c9159a0f7e3af24f7ff54bbef204840ca282689fbb47b` | 0 |
| node/src/main/kotlin/net/corda/node/migration/PersistentIdentityMigrationNewTable.kt | 3862 | `32e46c329ddf6e25ae8730cb97706f4e56c53b1e8b8466db9df189492f75dc49` | 0 |
| node/src/main/kotlin/net/corda/node/migration/VaultStateMigration.kt | 5388 | `4a1672502461da70acd5bfc8b60bb3c8df0b1163ab24d47c2f1ec2bf01806d59` | 0 |
| node/src/main/kotlin/net/corda/node/services/CoreFlowHandlers.kt | 4167 | `fc05e10f5ebf037473224281ee455f569ad9ae75460a2684d3907131c42ec5b3` | 0 |
| node/src/main/kotlin/net/corda/node/services/DbTransactionsResolver.kt | 9024 | `a8d0b77a29e857598625a415c5f15066210c8936f959cea67d80707e8c1fa356` | 0 |
| node/src/main/kotlin/net/corda/node/services/EncryptionService.kt | 2110 | `9b51ceb01e3e703ebe041d465318e20ae6fcbec7ab1fe417ad7a8278577b24bb` | 0 |
| node/src/main/kotlin/net/corda/node/services/Permissions.kt | 1653 | `a96f91fbd6927c31fc8809f69cb51650a699684ee80efaca544dafeec5bbd661` | 0 |
| node/src/main/kotlin/net/corda/node/services/api/AuditService.kt | 5940 | `07066b4379667fdc1dd4d4fd4b4ef25b5467103c55a5dd2a7a25c1e464cc9bbb` | 0 |
| node/src/main/kotlin/net/corda/node/services/api/CheckpointStorage.kt | 4728 | `f70f6b59a0211fbeb0293fca3df41abb2c739a41ffb7ab8a0905ba1fb0623251` | 0 |
| node/src/main/kotlin/net/corda/node/services/api/IdentityServiceInternal.kt | 812 | `a80b949cfe8d974575cb7428252635344d41c2361c9a94d174e6debd8695fed9` | 0 |
| node/src/main/kotlin/net/corda/node/services/api/MonitoringService.kt | 426 | `faa109ec060c12319441f6b7b0cc750cc2abfc1690b3af1a7ab519cb36fbea57` | 0 |
| node/src/main/kotlin/net/corda/node/services/api/NodePropertiesStore.kt | 364 | `10ab003984bdd5b9c71e0fc5aa0851c21567de7c960063947903a63bcb0d5dec` | 0 |
| node/src/main/kotlin/net/corda/node/services/api/SchedulerService.kt | 1077 | `d349e00e8873755d31a2df3382587f236b3be655d37aabaeb5e2620bc790bf42` | 0 |
| node/src/main/kotlin/net/corda/node/services/api/SchemaService.kt | 932 | `a401036b84771192b400121ec15b0c1e29ecdab7878595d102811eee02bc741e` | 0 |
| node/src/main/kotlin/net/corda/node/services/api/ServiceHubInternal.kt | 21729 | `6a26678278dd92c5247655501adca7f00fbfa81c9351c1533f39319819177a5b` | 0 |
| node/src/main/kotlin/net/corda/node/services/api/VaultServiceInternal.kt | 1243 | `154c25dc9cef883c077dc09c042485c6d4085d777311e02813251a0c35bce985` | 0 |
| node/src/main/kotlin/net/corda/node/services/attachments/NodeAttachmentTrustCalculator.kt | 7696 | `9f9052eb8895461a9d722df02b6d65d5964a0a719c99b5bfbb0c5d07a26945b0` | 0 |
| node/src/main/kotlin/net/corda/node/services/config/ConfigUtilities.kt | 11480 | `3bc7b613c0e92b98b336d694b7c277d160580e72a964661a8be491e13278b292` | 0 |
| node/src/main/kotlin/net/corda/node/services/config/NodeConfiguration.kt | 16440 | `d6aedc308f107b84bd76f0ae91f776762f85ed52f8c572a4eb26452f2cdf8767` | 0 |
| node/src/main/kotlin/net/corda/node/services/config/NodeConfigurationImpl.kt | 17225 | `4e05df8474117837e574f07374199299b10f89011141e6a757998447807c157d` | 0 |
| node/src/main/kotlin/net/corda/node/services/config/ShadowingException.kt | 298 | `29698951edfcba81b99e38bafaa3a2dcef6f774b81b672070603faacadc1b088` | 0 |
| node/src/main/kotlin/net/corda/node/services/config/rpc/NodeRpcOptions.kt | 344 | `a112b615daabb1afc2c65fc521c90b06cbc295ad93eb337362a7def74aadf6e0` | 0 |
| node/src/main/kotlin/net/corda/node/services/config/schema/parsers/StandardConfigValueParsers.kt | 2707 | `7d8f2328674bad3de48a2342f72d31dda11d8bdc256f60fe476db3a42215a09a` | 0 |
| node/src/main/kotlin/net/corda/node/services/config/schema/v1/ConfigSections.kt | 22692 | `4a6c3438289e7e3558f2b64ad676a2d7cafac00bb4f88c0b12c8bbd5648c18d2` | 0 |
| node/src/main/kotlin/net/corda/node/services/config/shell/SSHDConfiguration.kt | 946 | `621599732602a74c42333d0663d85988d87fc1da9ccc96f24c632816a7973494` | 0 |
| node/src/main/kotlin/net/corda/node/services/config/shell/ShellConfig.kt | 1117 | `1d340863fb34d4c6389932e97b1d8c979db7d0878b41d4922814a2c65de42c48` | 0 |
| node/src/main/kotlin/net/corda/node/services/config/shell/ShellSafetyConfig.kt | 1688 | `63e53084a3697c3ac36346dd94dd35b992b6683562ea878a396793c68df04b64` | 0 |
| node/src/main/kotlin/net/corda/node/services/diagnostics/NodeDiagnosticsService.kt | 690 | `58b3f1786f972c2fa9b299565d4fb1d149ac15feaebcf47098ff28594c9cfe3a` | 0 |
| node/src/main/kotlin/net/corda/node/services/events/NodeSchedulerService.kt | 20072 | `cf6e403cd7f6c662fb1a75740b89ecbe79828a51dfdd3867289749df0829d94d` | 0 |
| node/src/main/kotlin/net/corda/node/services/events/PersistentScheduledFlowRepository.kt | 3036 | `eaaa3c0273f21c62174201caa46a018575f7b7cb1f4862d64a54c2a358396058` | 0 |
| node/src/main/kotlin/net/corda/node/services/events/ScheduledActivityObserver.kt | 1848 | `f27fae9ee14cfbdb32e6b6f83f76924b195c58461994d080ecfa7ae95038c398` | 0 |
| node/src/main/kotlin/net/corda/node/services/identity/InMemoryIdentityService.kt | 7473 | `1f64b67baf796928d61d4f31e9cfe660041a5c0f5920777d9fe990eefafb4811` | 0 |
| node/src/main/kotlin/net/corda/node/services/identity/PersistentIdentityService.kt | 25532 | `93050a70515cc22eb0569f13da19eec725d61728a4047576ab8e3f6f80092ea0` | 0 |
| node/src/main/kotlin/net/corda/node/services/keys/BasicHSMKeyManagementService.kt | 7963 | `f480066e249e3e360221908cfae7f673f960919bf8b4cf4a69808fd7be6edb55` | 0 |
| node/src/main/kotlin/net/corda/node/services/keys/KMSUtils.kt | 2915 | `1aa3e56c2bd30f56bc697d2bd13dee439bd9ffd4349fb59b77527fc57482f810` | 0 |
| node/src/main/kotlin/net/corda/node/services/keys/KeyManagementServiceInternal.kt | 1444 | `e3cc8c18cbb3daab9f0fbe68b1f8d95b5600d361511ddfe709c86ef87d879252` | 0 |
| node/src/main/kotlin/net/corda/node/services/logging/ContextualLoggingUtils.kt | 1426 | `acc9fc5c4994fe33e81b50791c4f90f14a9af180f0b27e84eed64d95c818b773` | 0 |
| node/src/main/kotlin/net/corda/node/services/messaging/ArtemisMessagingServer.kt | 17479 | `556893a36a5ae7c505dc892b195fd96b09a9b6c2c8bd56122886c13dedf51fcc` | 0 |
| node/src/main/kotlin/net/corda/node/services/messaging/InterceptingActiveMQJAASSecurityManager.kt | 8624 | `124a106c61f7db2477afe59bf5eaf34f46a70f12f7e71d0b635e8f885b55ef95` | 0 |
| node/src/main/kotlin/net/corda/node/services/messaging/Messaging.kt | 9389 | `9297a9c53845269eacddddcda211ff71d3097f24fea51a3cdaa2ec143a144102` | 0 |
| node/src/main/kotlin/net/corda/node/services/messaging/MessagingExecutor.kt | 4583 | `6669f02d044116e86b0191fbbd502a1efdf7cc6351431ead30fc42fd7dbed26d` | 0 |
| node/src/main/kotlin/net/corda/node/services/messaging/NodeNettyAcceptorFactory.kt | 9733 | `99a59ba76120ab19011b0bc8eb206b19d0c0b4d21686af174085457fb4f4b416` | 0 |
| node/src/main/kotlin/net/corda/node/services/messaging/NodeSSLContextFactory.kt | 4406 | `308c7562f8dcdbe93df6a15c1b0e96bf65b51ce1115279b8e292fa2e213c0f4b` | 0 |
| node/src/main/kotlin/net/corda/node/services/messaging/P2PMessageDeduplicator.kt | 5248 | `1f8cb5b85bb91a7a8be1df09fe577e1ccbe0f83f80c96d1851bbd5d27af470c8` | 0 |
| node/src/main/kotlin/net/corda/node/services/messaging/P2PMessagingClient.kt | 36779 | `f32cf2cfa045ef7546a56fec29be71b1ae959ae6cf76fe0b450766caf7ddab6b` | 0 |
| node/src/main/kotlin/net/corda/node/services/network/NetworkMapClient.kt | 5591 | `67b0bb980e0ea560276402fdbfb759763340ca74370b973c2fb96469df5680f2` | 0 |
| node/src/main/kotlin/net/corda/node/services/network/NetworkMapUpdater.kt | 22802 | `4a75d3e52b5b96564c76ded010046c4e3754a6d1c3991c26d627c759c6334ca4` | 0 |
| node/src/main/kotlin/net/corda/node/services/network/NetworkParameterUpdateListener.kt | 401 | `1ca9641808c568f24605c349f366d23c48e021c588fc0d29f3dca1186113cc6e` | 0 |
| node/src/main/kotlin/net/corda/node/services/network/NetworkParametersHotloader.kt | 3986 | `db2315c51d168df359fe86220414e30c25a11d4ea03fe8b75288cbd283056d8f` | 0 |
| node/src/main/kotlin/net/corda/node/services/network/NodeInfoWatcher.kt | 5883 | `22b04f6dcee161a043dda210d5e4109e3125399b9e50d944bdb3c16970350824` | 0 |
| node/src/main/kotlin/net/corda/node/services/network/NotaryUpdateListener.kt | 377 | `680ca6862aef5a70df1020ad58526cc7edf09adc64c949b8e2f2cc7d2ef2d496` | 0 |
| node/src/main/kotlin/net/corda/node/services/network/PersistentNetworkMapCache.kt | 21538 | `db4393810e16a2b6c62fb52903d34171087c15f614c33eeb5649d48ba9eb4226` | 0 |
| node/src/main/kotlin/net/corda/node/services/network/PersistentPartyInfoCache.kt | 4141 | `cb9bdfb7533c264ca98b093654202cb0905946bb8ce1ddf4f602d72bee59af9a` | 0 |
| node/src/main/kotlin/net/corda/node/services/persistence/AbstractPartyDescriptor.kt | 2676 | `a7dbe1c30c1cf15e85c6cc0cdefee0fae1b27094cf9b468d29871464925589ed` | 0 |
| node/src/main/kotlin/net/corda/node/services/persistence/AbstractPartyToX500NameAsStringConverter.kt | 1644 | `64bb9ae0acc1b77acfd9bd5dca071931cfcf2f4eea2ecce273b93e8addbbec31` | 0 |
| node/src/main/kotlin/net/corda/node/services/persistence/AesDbEncryptionService.kt | 6684 | `90aed52472192bddf0664081d593bf3c4fd6f6ff31da29ca2e613b3cfee4e11e` | 0 |
| node/src/main/kotlin/net/corda/node/services/persistence/AttachmentStorageInternal.kt | 2038 | `0a726048790ac9197ab1b41762c48300ac143c632dec50a8ae6046290362f6d2` | 0 |
| node/src/main/kotlin/net/corda/node/services/persistence/DBCheckpointPerformanceRecorder.kt | 2960 | `b814af024bf41d2ff78ddfcec128209c6205ca12d8a0016e29cfbb85c69c03b6` | 0 |
| node/src/main/kotlin/net/corda/node/services/persistence/DBCheckpointStorage.kt | 33554 | `776d72234969bad1b61fa9b97b54c1bac88193fa78be67b90219af4348fb8cac` | 0 |
| node/src/main/kotlin/net/corda/node/services/persistence/DBTransactionMappingStorage.kt | 2363 | `c83c7a76ea15f382e331d04dc4784bbe433a770d180cec4cf157d4b140f3c232` | 0 |
| node/src/main/kotlin/net/corda/node/services/persistence/DBTransactionStorage.kt | 19887 | `4a2af71876421e9334c4950abfbc8f41a1ede4f49d93b2222346e71fc5982a22` | 0 |
| node/src/main/kotlin/net/corda/node/services/persistence/DBTransactionStorageLedgerRecovery.kt | 10482 | `d358e9e4b678617a3287bc2a6c2d951dc7fe3d1dd3bf5f11d1e6f048046ab075` | 0 |
| node/src/main/kotlin/net/corda/node/services/persistence/HashedDistributionList.kt | 5546 | `0bc868cc72d972c82fac23e5c182c1ccddde4b2fc5740dc35adc6dce64f13c3a` | 0 |
| node/src/main/kotlin/net/corda/node/services/persistence/NodeAttachmentService.kt | 28418 | `3e3f34212183496e615fa8870208f4d2c99d7095fc93c4cd08d913fcbaaf1ec8` | 0 |
| node/src/main/kotlin/net/corda/node/services/persistence/NodePropertiesPersistentStore.kt | 2779 | `42261881e25224b4ecb4a5bd94182aaa946206856feb40573ae1a78535863f65` | 0 |
| node/src/main/kotlin/net/corda/node/services/persistence/PublicKeyHashToExternalId.kt | 703 | `937667e8aa2e8ee441593ad91368d62e697740a3270be65900e0e882bda8bc94` | 0 |
| node/src/main/kotlin/net/corda/node/services/persistence/PublicKeyToOwningIdentityCacheImpl.kt | 3036 | `20cc2401d140c6294315d78f1990640c9954d91d3b7d8268c930504563ce4ab6` | 0 |
| node/src/main/kotlin/net/corda/node/services/persistence/PublicKeyToTextConverter.kt | 766 | `183686e68852febda6bb7080b1df049fcaaab923815c2ce672f5ce47e89d3f27` | 0 |
| node/src/main/kotlin/net/corda/node/services/persistence/WritablePublicKeyToOwningIdentityCache.kt | 543 | `224f405fe2ffb4e5380c05a0107f964efc0113a5d64c21b8e5fe36f5474d8bd1` | 0 |
| node/src/main/kotlin/net/corda/node/services/rpc/ArtemisRpcBroker.kt | 6509 | `1633268f64e2498521c2d7ddd66f854230e278044c8b3fd320d380526f9176df` | 0 |
| node/src/main/kotlin/net/corda/node/services/rpc/CheckpointDumperImpl.kt | 28035 | `b942a91430a39b1007db1121cf8ef456952086848ec075c05c39e9400ea75cf2` | 0 |
| node/src/main/kotlin/net/corda/node/services/rpc/InternalRPCMessagingClient.kt | 2391 | `cc85a7b412626acf2f6e73caec0f89c71f4d8e9897bc865eecc45c1a1c4766b9` | 0 |
| node/src/main/kotlin/net/corda/node/services/rpc/RPCServer.kt | 30494 | `4055f84c3fc4663690592ba1f6b9c00968065db5051ab5cf944f5829d49e2132` | 0 |
| node/src/main/kotlin/net/corda/node/services/rpc/RolesAdderOnLogin.kt | 1527 | `7473eaa699f00d0be9c558002bc06ca781d0294c116eddc29d055e302d18fb94` | 0 |
| node/src/main/kotlin/net/corda/node/services/rpc/RpcAuthContext.kt | 316 | `e4e6311ee687fb4294b71b35fe54c81cd99a9f050d21e6586c9e006fb1c3d0de` | 0 |
| node/src/main/kotlin/net/corda/node/services/rpc/RpcBrokerConfiguration.kt | 7804 | `42649b5d01d81c295bd41c70365bf98d3515199dc428411bb5b9c9bcd59618e9` | 0 |
| node/src/main/kotlin/net/corda/node/services/schema/NodeSchemaService.kt | 6118 | `9796b14235d5d53d56591ec7f5d9bfe8f9b5c607ef0c0f889065e9c55cdd707f` | 0 |
| node/src/main/kotlin/net/corda/node/services/schema/PersistentStateService.kt | 2177 | `2944c51cfd71808b25ea072cc9c6608e2d0f21b7fef68cc705add6807e08d07c` | 0 |
| node/src/main/kotlin/net/corda/node/services/statemachine/Action.kt | 7328 | `4f1a6ca31531ff838448de192a5bd0a2414998d3a3fcfe0f0eebeed12c295d14` | 0 |
| node/src/main/kotlin/net/corda/node/services/statemachine/ActionExecutor.kt | 354 | `cd37bea725ad285d6ad54e0d9c3df05fa1e03763c0ca7b16463675c61cc7a271` | 0 |
| node/src/main/kotlin/net/corda/node/services/statemachine/ActionExecutorImpl.kt | 11467 | `5b380a07bc2ae446eaebdd142d16844b10fed42668fe929e20494a89ed59de2b` | 0 |
| node/src/main/kotlin/net/corda/node/services/statemachine/ActionFutureExecutor.kt | 4239 | `438fdb80423d7e306812605f72f6a87b5f161115d9a9b4e6398ca6c6a396b868` | 0 |
| node/src/main/kotlin/net/corda/node/services/statemachine/CountUpDownLatch.kt | 1681 | `598ff0422d6fcd04a82fce16e579d631f0184463a02c3bebae4970eeb1b3dc3a` | 0 |
| node/src/main/kotlin/net/corda/node/services/statemachine/DeduplicationId.kt | 2803 | `8a95b9ac4ce01a8848fc880f62cba8651235ddaee12cdea6d21fa33261d5587f` | 0 |
| node/src/main/kotlin/net/corda/node/services/statemachine/Event.kt | 7634 | `eea7ad53b5b641da1e699a3c98c6dffeb20dd98f299629f79c06bcdbd528b1b5` | 0 |
| node/src/main/kotlin/net/corda/node/services/statemachine/FiberUtils.kt | 1125 | `0bc9140b4b4d82bfa351f6c4c8c08bc998162e815b3ebbd9eb52999ddcd24bcc` | 0 |
| node/src/main/kotlin/net/corda/node/services/statemachine/FlowCreator.kt | 15241 | `a3b83623f187f550e72acd14623e17dccbc90835689b0b6b980941fb38dc1184` | 0 |
| node/src/main/kotlin/net/corda/node/services/statemachine/FlowDefaultUncaughtExceptionHandler.kt | 3938 | `515c931a1e4f3c5bff032e072989a077fd20bd14395a2a823e253c9e6af7dbe3` | 0 |
| node/src/main/kotlin/net/corda/node/services/statemachine/FlowFiber.kt | 490 | `57a1e433d4d39b006495a80a80e5e9f050d83c93208548d8030701f30da943ec` | 0 |
| node/src/main/kotlin/net/corda/node/services/statemachine/FlowLogicRefFactoryImpl.kt | 12040 | `fc5206cdad20863b617451140edcb3fd0ea7a952be3ec04118f3567f7b579b20` | 0 |
| node/src/main/kotlin/net/corda/node/services/statemachine/FlowMessaging.kt | 5886 | `0fbed827ad29d0d87c3e3e034fea8ad91c0eb6b27b4ed9b978bc247838678083` | 0 |
| node/src/main/kotlin/net/corda/node/services/statemachine/FlowMonitor.kt | 4294 | `8c7b5796e2c39edacdd9ce33c939ddead023c31a74d14f30a0766a1c1ae9f558` | 0 |
| node/src/main/kotlin/net/corda/node/services/statemachine/FlowOperator.kt | 8020 | `c186f8a80495f75fff9aadb30c0feede4718986b456e746fc264866664edd1a7` | 0 |
| node/src/main/kotlin/net/corda/node/services/statemachine/FlowSessionImpl.kt | 4602 | `68ee9124e4e0f50ddc2479d483cae154f94300ab07c195578c1378d4580fcd59` | 0 |
| node/src/main/kotlin/net/corda/node/services/statemachine/FlowStackSnapshotFactory.kt | 1483 | `46376afafc7de910b3d9d595a5b9f1877b127d470f93d1aa4488f9a2c02627d9` | 0 |
| node/src/main/kotlin/net/corda/node/services/statemachine/FlowStateMachineImpl.kt | 30776 | `2c82d52b07330db5f03624396330c5572f4233769ed6c81c5de101ad81e9ac49` | 0 |
| node/src/main/kotlin/net/corda/node/services/statemachine/FlowStateMachineUtils.kt | 626 | `9c00ec83b04413630f71e5dcd658452715d698fcb8bff558cb6e9b8d2f0d34f1` | 0 |
| node/src/main/kotlin/net/corda/node/services/statemachine/FlowTimeoutException.kt | 316 | `6f8619621b98e6e9fe8ad3fda5d4ec091df1312f43deeac7c7cea40eeb52982a` | 0 |
| node/src/main/kotlin/net/corda/node/services/statemachine/FlowTimeoutScheduler.kt | 4366 | `e4af2c7b7cb3ae2b3cb0cf52cb974b5125a60dfaa68c1ca8acc60c1dd7fc8113` | 0 |
| node/src/main/kotlin/net/corda/node/services/statemachine/SessionMessage.kt | 5199 | `be050cc9a63ffb557f38df5d77dfcdeb5b1425d480b0420c5dbce7fd175cd745` | 0 |
| node/src/main/kotlin/net/corda/node/services/statemachine/SessionRejectException.kt | 669 | `09c49bfbcf2c386dca69549bf14700561114e329d6f11759ffda33e32a969294` | 0 |
| node/src/main/kotlin/net/corda/node/services/statemachine/SingleThreadedStateMachineManager.kt | 59755 | `6602c5b3bc6f45b7ac8085c0bbc7ca3801138f3188c2ecf9fe5bd80439cd50d0` | 0 |
| node/src/main/kotlin/net/corda/node/services/statemachine/StaffedFlowHospital.kt | 35665 | `761be75b44403c6b7e0e6161c50970240ae9612c74aae22bc8cb931a0c64bef0` | 0 |
| node/src/main/kotlin/net/corda/node/services/statemachine/StateMachineInnerState.kt | 2185 | `f991a877a7c12fc6c18c2247576d55c6b394d9c5ec3db049552a9a0b8c7777ef` | 0 |
| node/src/main/kotlin/net/corda/node/services/statemachine/StateMachineInstanceId.kt | 175 | `cfcd98a40a8733edb00c3c676f49f6eac56b91da0c6d8e5b4f985053e4d1f86c` | 0 |
| node/src/main/kotlin/net/corda/node/services/statemachine/StateMachineManager.kt | 7408 | `59e233a9209ac10d9b0c3fb23192ad30ae112ad68230777e0668e25c612877ec` | 0 |
| node/src/main/kotlin/net/corda/node/services/statemachine/StateMachineShutdownLogger.kt | 2508 | `4d3f4d18b358eff68f22612bddcce1b2c50580f5e4138d73e42e0ffce734afc9` | 0 |
| node/src/main/kotlin/net/corda/node/services/statemachine/StateMachineState.kt | 20257 | `be2eaa0d379f8fe824bc0d867235ff6c1ef564128a118fbf346bfe1c2b6612bd` | 0 |
| node/src/main/kotlin/net/corda/node/services/statemachine/StateTransitionExceptions.kt | 1063 | `6e83fe7b1531671bb973d917f71c3082575609753ef800249f8955f3d90705b3` | 0 |
| node/src/main/kotlin/net/corda/node/services/statemachine/SubFlow.kt | 3456 | `fbcde6f9e9feeb81abbf64447e51629dbfee064d5958514d2e65254ca6c10ee9` | 0 |
| node/src/main/kotlin/net/corda/node/services/statemachine/TransitionExecutor.kt | 928 | `5cad8b39ca6077ce136ccd757a924750eae5a7540867099bf39c4f4b470edd00` | 0 |
| node/src/main/kotlin/net/corda/node/services/statemachine/TransitionExecutorImpl.kt | 6271 | `1f35d37671bcc6f91e2985a17aaef9aee7b1c05f67f57007fdf77a04bd35f05e` | 0 |
| node/src/main/kotlin/net/corda/node/services/statemachine/interceptors/DumpHistoryOnErrorInterceptor.kt | 2870 | `783fb5c4efc5ff2f2942dfd19573351ac5cf43ed9e53f11b5031cfbb539de842` | 0 |
| node/src/main/kotlin/net/corda/node/services/statemachine/interceptors/HospitalisingInterceptor.kt | 2563 | `dbae7e5cccb9ae9e009b2f931a19fc480f8c6d14c708df6ccca8bdba662093b1` | 0 |
| node/src/main/kotlin/net/corda/node/services/statemachine/interceptors/MetricInterceptor.kt | 1579 | `ed4834fa35267fbee688ce8106a534d5a84bbe2334a773077b4733cd58297c9e` | 0 |
| node/src/main/kotlin/net/corda/node/services/statemachine/interceptors/PrintingInterceptor.kt | 1534 | `6d42da89046e40fdf85aedf0dda8294fb8c7b021abf4b348765069329d0bf37d` | 0 |
| node/src/main/kotlin/net/corda/node/services/statemachine/interceptors/TransitionDiagnosticRecord.kt | 2113 | `bcb221e5ffcde4eb5dd3a73f448c293cc5e137e2ce1bc16f9fd5e780fe4efc58` | 0 |
| node/src/main/kotlin/net/corda/node/services/statemachine/transitions/DeliverSessionMessageTransition.kt | 10404 | `d5b2ddb56fdaedf694b847a5aea37fc882a5c2d6692fea25da68d51ac6ec02e8` | 0 |
| node/src/main/kotlin/net/corda/node/services/statemachine/transitions/DoRemainingWorkTransition.kt | 1907 | `b54f52ddaeaccc84b0e90838e68135575260b19fe1a47932576f207b99f6326d` | 0 |
| node/src/main/kotlin/net/corda/node/services/statemachine/transitions/ErrorFlowTransition.kt | 8266 | `76d62cea7e7ed91143714b8f5eacb557bf2833945335dd9e1a6e7e64a603c28d` | 0 |
| node/src/main/kotlin/net/corda/node/services/statemachine/transitions/KilledFlowTransition.kt | 6448 | `f2a396c71e65ae834a0da4d02ac45a837f5a3e6b158bdcb3a682eda9cb4bc6e1` | 0 |
| node/src/main/kotlin/net/corda/node/services/statemachine/transitions/StartedFlowTransition.kt | 29602 | `de19453e70a8fc579257216be7f6c06f11f795e6f5c8db6301a2703d52613245` | 0 |
| node/src/main/kotlin/net/corda/node/services/statemachine/transitions/StateMachine.kt | 534 | `d3b5afc79c12426a8dfd31eed572d793ef2f80ddff8b9904ddfe2d40dbc80451` | 0 |
| node/src/main/kotlin/net/corda/node/services/statemachine/transitions/TopLevelTransition.kt | 19305 | `b7e34c31abea581ed7ca4ab3f530bf7335e844ace247c4bb98be466051c34c46` | 0 |
| node/src/main/kotlin/net/corda/node/services/statemachine/transitions/Transition.kt | 1942 | `2fedb72c10c71b45a291eaa9a1d0ef22e1da4960ce96a89e529c003a30d5508b` | 0 |
| node/src/main/kotlin/net/corda/node/services/statemachine/transitions/TransitionBuilder.kt | 3784 | `6303fcb54e779f6a91034e22ed391b5720b1a8aebaed6358bd543b7288de5079` | 0 |
| node/src/main/kotlin/net/corda/node/services/statemachine/transitions/TransitionResult.kt | 1693 | `d462ba91dab4d0a643965d4453f4b6e141f9a338afd2e8a962f855e97417d0ed` | 0 |
| node/src/main/kotlin/net/corda/node/services/statemachine/transitions/UnstartedFlowTransition.kt | 4340 | `159bf1d8fa59df2def1bd86b04f32e6aa479bcb3cbc88c0fb25630c98e259e7d` | 0 |
| node/src/main/kotlin/net/corda/node/services/transactions/NonValidatingNotaryFlow.kt | 6022 | `d87dd38fdcb1f39f54739be3e1f9ac9e2f9a1bfead11167683678c405cf98277` | 0 |
| node/src/main/kotlin/net/corda/node/services/transactions/PathManager.kt | 1520 | `b3038272bf8b2886d4c902ef5e48dffaeda22e2a11402acf550423924b21d6db` | 0 |
| node/src/main/kotlin/net/corda/node/services/transactions/PersistentUniquenessProvider.kt | 14475 | `5fdb98f1972300205e22484cadf233e3189c1f586a7c7875c2bc9db9024806e1` | 0 |
| node/src/main/kotlin/net/corda/node/services/transactions/ValidatingNotaryFlow.kt | 3051 | `6561feb132dab94c54257c69f82c25ef71382199027316ea2770ec6b51ba4462` | 0 |
| node/src/main/kotlin/net/corda/node/services/transactions/ValidatingNotaryService.kt | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| node/src/main/kotlin/net/corda/node/services/upgrade/ContractUpgradeServiceImpl.kt | 2531 | `1e9d17163728c685c79c0f2852975d2f2b0b5420f1ba21ecbbfffb9b3590e1e6` | 0 |
| node/src/main/kotlin/net/corda/node/services/vault/HibernateQueryCriteriaParser.kt | 48506 | `7e7d44f4e81053d8fe32b8de9dddc61d31daecc2ba2404b880edc14dae01e2b3` | 0 |
| node/src/main/kotlin/net/corda/node/services/vault/NodeVaultService.kt | 52990 | `3752203b93a1ced2358562b1f1702cfc64676765bc22181814983fa7ce5dfb32` | 0 |
| node/src/main/kotlin/net/corda/node/services/vault/VaultSchema.kt | 8664 | `6a8b23860e6e0f7dd5bae1cc8c4ccf0735bdfcf764476ada00f867017efd10d5` | 0 |
| node/src/main/kotlin/net/corda/node/utilities/AddressUtils.kt | 1069 | `7c0425977b1d38a62c64b5c78aacc4b5d18c875b3545629ff49f28e65802d2fa` | 0 |
| node/src/main/kotlin/net/corda/node/utilities/AffinityExecutor.kt | 3081 | `5a6c111c3239cfe37485ffb546c58995124938bddf101cdd497ae34236748e78` | 0 |
| node/src/main/kotlin/net/corda/node/utilities/AppendOnlyPersistentMap.kt | 24433 | `5bb1ac9c8afa615a5b9a5d663917a02d560ea3118b2190f0b8330a7e8c4cb7ea` | 0 |
| node/src/main/kotlin/net/corda/node/utilities/CertificatesUtils.kt | 1801 | `586ec0ce49d4cdb05db45d0fc5b708e717280ce7532a5292dd4b1811ed174ae0` | 0 |
| node/src/main/kotlin/net/corda/node/utilities/DemoClock.kt | 752 | `e6b60b1aaf931b6a881b1f4b374e9bf5761b19a9015ca4d6f5fc63ea20de470a` | 0 |
| node/src/main/kotlin/net/corda/node/utilities/InfrequentlyMutatedCache.kt | 4682 | `5d8bccba30a65832700feb1c42c5565e03d23cce01f07b1254bde483524c34fb` | 0 |
| node/src/main/kotlin/net/corda/node/utilities/NamedThreadFactory.kt | 852 | `a5f6d94194a4816fabef4e64af8fa9d8ca58b4668b17a012009f11acddbed1f1` | 0 |
| node/src/main/kotlin/net/corda/node/utilities/NodeBuildProperties.kt | 630 | `3d46f2bb3419bb9ab91a01862f29d79ac90d9cf1d327e321ae6884adfa1cbb43` | 0 |
| node/src/main/kotlin/net/corda/node/utilities/NodeNamedCache.kt | 6277 | `859d2acbd3b898f04aaaf94aba810ece1e582e488a1e44e0ac258e6ffbdeb223` | 0 |
| node/src/main/kotlin/net/corda/node/utilities/NonInvalidatingCache.kt | 2092 | `cb0b30ff573b48b8beeb2b34a896ab0300c155fcb764b1006f9c482f1f248235` | 0 |
| node/src/main/kotlin/net/corda/node/utilities/NonInvalidatingUnboundCache.kt | 1997 | `ceb16f720c846140d419079af17e97e10745763690b2bf806e4d31debf8fc8fe` | 0 |
| node/src/main/kotlin/net/corda/node/utilities/NotaryLoader.kt | 5830 | `86d394f5e18ca4d1d42b8d236cd5d42ed96876c19065d437c14bfec6903ae59d` | 0 |
| node/src/main/kotlin/net/corda/node/utilities/ObjectDiffer.kt | 5303 | `d0f82472ba59ef453fe00af2a15772d182efe530a4d6b5ddce25678869b062be` | 0 |
| node/src/main/kotlin/net/corda/node/utilities/PersistentMap.kt | 8961 | `3dd5f9770b25a5d8157a01ad158bd92864d9babd3d0817b0e64343800900e09a` | 0 |
| node/src/main/kotlin/net/corda/node/utilities/TimedFlowUtils.kt | 405 | `76324cdc8376732dcae3b49f7f41a5db1d8f3f0b1e012155088a914bcd68883d` | 0 |
| node/src/main/kotlin/net/corda/node/utilities/artemis/ArtemisStartupUtil.kt | 648 | `53b4bc1df2f5081fd45645780c6fdc1def90ca785d2ea677d659a636241f0c18` | 0 |
| node/src/main/kotlin/net/corda/node/utilities/errorAndTerminate.kt | 680 | `8096067be733bdbc8b7af75c71f0b2af9decc8a29c8a153c16fd9ca2bb7befd3` | 0 |
| node/src/main/kotlin/net/corda/node/utilities/logging/AsyncLoggerContextSelectorNoThreadLocal.kt | 1801 | `d5d4f0f657868e3423bc111b228774db9104d14840382dcecd3f70780071d011` | 0 |
| node/src/main/kotlin/net/corda/node/utilities/registration/HTTPNetworkRegistrationService.kt | 3568 | `c3cab1b88698dc3ff7aa894ff2195b28e50204f5bbf29aabc842f65630575832` | 1 |
| node/src/main/kotlin/net/corda/node/utilities/registration/NetworkRegistrationHelper.kt | 27738 | `79c6c65d63f659002a0013ea64193585a6249c9e38df25b7b8cfa3a13d05f63f` | 1 |
| node/src/main/kotlin/net/corda/node/utilities/registration/NetworkRegistrationService.kt | 838 | `63d464ea912e67ee367e0ab0ba8260bfdf18a4c4a43e058f784626bb0d8da08f` | 0 |
| node/src/main/kotlin/net/corda/node/verification/ExternalVerifierHandleImpl.kt | 13306 | `974705796c8b38860fe2c51b42c6a8d710b40742f01dcfac87a108599163e7c6` | 0 |
| node/src/main/kotlin/net/corda/node/verification/NoDbAccessVerifier.kt | 337 | `6d7d7b482ffe2d1e7cceab76f9954b08f2aa38935c4daf1193e59d7cd307d94d` | 0 |
| node/src/main/kotlin/net/corda/notary/common/BatchSigning.kt | 2518 | `57febf76b1582c3bd605bbbdc0774b48d739f686f2a073b141e50a7d99f9897c` | 0 |
| node/src/main/kotlin/net/corda/notary/common/ValidationModeNotaryService.kt | 1252 | `ba38d0e63bbbe1ffa40dc86ffe29a594b6107245c349f0c76ed707de29ccc497` | 0 |
| node/src/main/kotlin/net/corda/notary/experimental/bftsmart/BFTSmart.kt | 18631 | `330801014065201e806df08577657d8f8ef52f6612390621a124ee096f6485d8` | 0 |
| node/src/main/kotlin/net/corda/notary/experimental/bftsmart/BFTSmartConfigInternal.kt | 4792 | `4781c7c8e7e33b3ea58841b855920316270ff9e5f1b9293bccfc51454e0838c1` | 0 |
| node/src/main/kotlin/net/corda/notary/experimental/bftsmart/BFTSmartNotaryService.kt | 10146 | `377d8e801151497b1831d1654c4d9ea7693916dc036bd6f13cd93e60d0ac70d4` | 0 |
| node/src/main/kotlin/net/corda/notary/experimental/bftsmart/Schema.kt | 736 | `08f80a1dd9e9e23aeb980cfe8bd2fbeba80a07ecceaca2b3c82b3f910944ed81` | 0 |
| node/src/main/kotlin/net/corda/notary/experimental/raft/RaftConfig.kt | 819 | `5ca02deccbe338147ec382cff12d9265f38734642160078a7bbfdbd9d15069ad` | 0 |
| node/src/main/kotlin/net/corda/notary/experimental/raft/RaftNotaryService.kt | 1972 | `1455b3b6bd11aecb6815fdfa6f9b8e2fadf81b81920fc5da9168f710bc3369c5` | 0 |
| node/src/main/kotlin/net/corda/notary/experimental/raft/RaftTransactionCommitLog.kt | 12482 | `790e4e3fb6d68804700efd303c6ae8268cda41535aafd7897d423bdcb3380ac2` | 0 |
| node/src/main/kotlin/net/corda/notary/experimental/raft/RaftUniquenessProvider.kt | 10753 | `b2577f2a943457ddaa5abb021cb1498a9037d682414de959311fbe39b481e9e5` | 0 |
| node/src/main/kotlin/net/corda/notary/experimental/raft/Schema.kt | 717 | `b067756e780d7f4d0385208af66dc01a6895cc30514b338e1a569c8349bd541d` | 0 |
| node/src/main/kotlin/net/corda/notary/jpa/JPANotaryConfiguration.kt | 249 | `14e2775da73b460de7a7ba118edabbe23501e54ad2da43f95f638785157ff282` | 0 |
| node/src/main/kotlin/net/corda/notary/jpa/JPANotaryService.kt | 2132 | `14d1d47d5b238d36a30ee2d9449a105e84ccf89d52a3785f4f6dd4cfba637084` | 0 |
| node/src/main/kotlin/net/corda/notary/jpa/JPAUniquenessProvider.kt | 17042 | `c147e77fc6ac94c841d7a8e5c86847964cce56c96e96ab24d6206e890b4aba8a` | 0 |
| node/src/main/kotlin/net/corda/notary/jpa/Schema.kt | 543 | `cf95295e1d128c7d3fc764fa4db708f73ffeef6bb2e53c9b163ed6906ccc2c1a` | 0 |
| opentelemetry/build.gradle | 732 | `68e91fb2e30d63378904538981a569e337841d476702a0b9d1e6a0f7a245671d` | 0 |
| opentelemetry/opentelemetry-driver/build.gradle | 611 | `c467527d979ebf32512c84a5a14f9ae6dd215b03a92c4e29113730e3ef1fe493` | 0 |
| opentelemetry/src/main/kotlin/net/corda/opentelemetrydriver/OpenTelemetryDriver.kt | 2241 | `8610e0a2026d049b4ec7d6525170a297a8c629ce3850f7cd86433bb0ddc9e7e3` | 0 |
| release-tools/jiraReleaseChecker.py | 8918 | `35459025b5b507de898a921fe8621f46415259356808e4c202ec98123e2736a2` | 0 |
| serialization-1.2/build.gradle | 1065 | `58b2c477db3d515197c3f634447e41fd9ca1de8433abc6976b85c3b702157f02` | 0 |
| serialization/build.gradle | 2455 | `df547345417df26d4f379ab01b2112253f021093edacb5ad53dacdda40cb5737` | 0 |
| serialization/src/main/java/net/corda/serialization/internal/amqp/custom/CacheKey.java | 757 | `e0b800a8dfa718f3a3ad224e8378b2b082ee38cbb43fbc4c4d54f0365c2c421f` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/AllButBlacklisted.kt | 5808 | `3cd3f237dd5b11e9e10498fdba14b510383764016e32a10c3356b12d21f66925` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/ByteBufferStreams.kt | 2084 | `60fbef07f726b5410674e781d3157b8e26c5cc689889bcd944d80612e25f2aa8` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/CheckpointSerializationScheme.kt | 2438 | `c4d738a3e9bbbfeddcc3b2dab5baca350f68a282c5346cc62d5ec5e7563b7ee6` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/ClassWhitelists.kt | 1897 | `8967b1df63aab3fad7c21ff063c36bfbafedc7c8e8b44e8490363e70e1aac832` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/ClientContexts.kt | 743 | `5fe7255401dd6c65dceed0c33d2f55f12b579b0165ffc1e1f987deb546e2fddd` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/DefaultWhitelist.kt | 3049 | `8116ee750842f20cc13b56fade3891f12d3a2100730f1201c80c601ca47df193` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/GeneratedAttachment.kt | 279 | `d9978ac18a602c707d827e59df1ea9028dca996455ff32c18fbef0e79e61b13e` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/NotSerializableExceptions.kt | 621 | `d864c869c62045130978b14698716adb1422efc30c9f544fe69a20163f05953b` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/OrdinalIO.kt | 1083 | `d7552984b0fab8c38743d742d72a10c9284cc8a842240d40c3e11fb2a1aa2c9b` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/SerializationFormat.kt | 2812 | `b7be47ee525f87ab13a03666fc822cea9318d57087379ec84482b3867cd46a6f` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/SerializationScheme.kt | 8418 | `a82e218de280c408f38468a3bed13a1c308213ec432161065af9f3428ff79425` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/SerializationUtils.kt | 279 | `a1411a20e4a9f44813407dc106449f2f892cbc9adac49204cc124180c754ab58` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/SerializeAsTokenContextImpl.kt | 5574 | `7880be21f9288731cf551e2f9a5163aa39c82c6ae57e155abca01448b6448e8d` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/ServerContexts.kt | 1184 | `7e116bfdbbdaf18cd56f5c52218e39b107f07598bc379fabd7dc5a44a67e3021` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/SharedContexts.kt | 824 | `0f78fdd6cd0a31773a99095d2756b3a5e651e05f066e3adc12af6c117a0b18cc` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/UseCaseAwareness.kt | 998 | `dfa3b8e94fdaafddc7b40dd8dd3a691d5dc1cfae11601272259f13908b6e082b` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/amqp/AMQPDescriptorRegistry.kt | 972 | `e81a199ca9715e614dbedd9a1e801c2e9e7cbe51a0727a58991cbfe15e927e44` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/amqp/AMQPExceptions.kt | 3020 | `2e9e94fd82606694f636a291cdf404ce769d8f2103689436db306ff59eb1b8ca` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/amqp/AMQPPrimitiveSerializer.kt | 1326 | `c6fb49d509877848f29097d0b396bc5f427068eb9840e7cbc9e2d3453c3efe3b` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/amqp/AMQPRemoteTypeModel.kt | 10702 | `879ff97e3db31511149539edcff09267f9ec2ae3a10a11df4e72bf7063642d51` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/amqp/AMQPSerializationScheme.kt | 11033 | `5ba2cf6c111a055d6e4cbfd61eec5230acafe0b6f64d1ba989449ab9ec56b3e3` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/amqp/AMQPSerializationThreadContext.kt | 193 | `599371ee597bc91bfa32175190200314ac9aaa28ca965cd83df757afcd1339de` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/amqp/AMQPSerializer.kt | 1522 | `a2b3f6caff2dbbb28258cbe8953a40ed4e522c993e21f6486207586915ea05bb` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/amqp/AMQPSerializerFactories.kt | 945 | `afb95cdf47eb3a03312f355da176c0b2362abf7b369d9d4a89115600e5cecc8d` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/amqp/AMQPStreams.kt | 1013 | `d5a37a6f160e696901dade205556a49f25592387ffeb47dc0c253072405694e2` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/amqp/AMQPTypeIdentifierParser.kt | 8321 | `1f129e37d57f21f368baffd7ab4926e3bf222085a012a7f8e8a9b6ca10765341` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/amqp/AMQPTypeIdentifiers.kt | 3119 | `d122bfd9c09a26e875cea6a4d29ec1d5415504c7726a9e2c11ae762ddb1f4bf0` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/amqp/AccessOrderLinkedHashMap.kt | 340 | `e338687c88143fb82ed46c6d16c5803b1f22af35286375a9cbbebf6911580629` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/amqp/ArraySerializer.kt | 10064 | `4789ff4950d919e29993a810eba1381196837b17ffcc866d2b69b6ceebf5b6aa` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/amqp/CollectionSerializer.kt | 6322 | `fa479a7b47c905537516b3473eb7524a54762f44732595328a9891e415791300` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/amqp/ComposableTypePropertySerializer.kt | 11147 | `56262e3bb5211f7e50c7308e8a763d7be2ddc26a3e15be00f898a888ac897211` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/amqp/CorDappCustomSerializer.kt | 4296 | `2e396005835d915b30337a6451abad636e0b13cfcabf27f2644068855f7a793d` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/amqp/CustomSerializer.kt | 10863 | `5ae8d64e0ad2b04ec420bb413e6b4d4e40a109c1169c3087eddabefd9e8cde46` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/amqp/CustomSerializerRegistry.kt | 8875 | `f69082124c86461568370bf4a530f5574c1518d638aa9d7fc3a6e37758c89176` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/amqp/DescriptorBasedSerializerRegistry.kt | 1205 | `377648177745cd5272a83632a0fe7d697609fcd4e60806e2e1541443df895c01` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/amqp/DeserializationInput.kt | 13164 | `7adbdfe2c74c8e251ff5e13a6d9371b7368d0895ac00b6f9296cb72d26195655` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/amqp/EnumEvolutionSerializer.kt | 3382 | `8267875b2f60606a5f93dee7ff3d57817467b81e8f60236d786ae89ebc89ceb6` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/amqp/EnumSerializer.kt | 2257 | `dea19d12986422e34a429ace934b718dea57dd48f24faa54efd3904b05b6498f` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/amqp/Envelope.kt | 3619 | `1fc24b41ab546a97452b018e85f97368bcdbe3ca248d68fe013b4e171568e77f` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/amqp/EvolutionSerializerFactory.kt | 10498 | `0719ddd7e21ace6f158b0b411074b6ce9339976b5ceafb738fc92162a46dda36` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/amqp/InterningSerializer.kt | 1180 | `fa08039f510ce5e40d1e4b92df2d3506950c3e02a86d3523b01f8b1d141c19cd` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/amqp/LocalSerializerFactory.kt | 14571 | `8ec4bde4f8826c37e39d336d4822a782c6902ee04738958bbed762bd2c64788c` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/amqp/MapSerializer.kt | 8412 | `202a58e6bf746f3c3e18a72f0b17ed3e1e9b2df3fcea57ebb94e8d77efb7660b` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/amqp/ObjectBuilder.kt | 13003 | `a23b4fb9fc5fd0073e2f2c638cc5ebab84ca14fa037f3f29ea606a85ad98245a` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/amqp/ObjectSerializer.kt | 12368 | `e5aedc57dccde5aa73248a9c4e63ab36dec0c1cce851df3d5a3a67ab0bd9b930` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/amqp/OutputStreamWritableBuffer.kt | 2300 | `0d63a6aec0b68c1dc4af8ce5ac1a8973d8ce0299c11c9034702090c665d403f9` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/amqp/PropertyDescriptor.kt | 10941 | `21d4a279ec246caba38dafee9ea8a20069e98af250c676e5dc07de3dd9dd9693` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/amqp/RemoteSerializerFactory.kt | 7887 | `a1412ab3d09813165dc177777c4126602580361fb31f32b01ab1b81a4f5d4d1e` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/amqp/Schema.kt | 16267 | `f55b2c55fa0f96a446e4709595ba8b5b497d7ea57915ae0fdd48468c55565601` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/amqp/SerializationHelper.kt | 5073 | `64e0a2d7e7587d0de1a727565f41168c995bb17841c6c84ba1a30b9524b1a275` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/amqp/SerializationOutput.kt | 7096 | `7ac8c080cd30e4df97ef8ecdc82e26cd14aa96640b80b6b36e9284cf456a2243` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/amqp/SerializerFactory.kt | 1919 | `7cf8dff341f378618f1162c760841fd3bab25684f7f39283ea92cd0708956134` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/amqp/SerializerFactoryBuilder.kt | 6012 | `d48fbdab9308ca2a821e2df4bd30e31153fac881adc2f87600f9b93fd221e7e0` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/amqp/SingletonSerializer.kt | 1682 | `88b39d50055b403d117d2f8ef8f72c98ef4387401760f21fa61b9d9056801949` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/amqp/SupportedTransforms.kt | 3148 | `e855b09bf4591cb96f6719745e8e1af4d23d994c430a04da0c83387925660c6d` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/amqp/TransformTypes.kt | 3292 | `acaf16567c22195367a515e9c503a969eb7058e203c2aa5d4c10f4170fdddcb3` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/amqp/TransformsSchema.kt | 14464 | `761fb42fe5ce5513cca246e028056f29d072e3255c71ae81aee77ca8417efe30` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/amqp/TypeNotationGenerator.kt | 3112 | `a0a5921afd5d6d00689d4f642113c99bc4987430cc9830104f2be8035680b89b` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/amqp/TypeParameterUtils.kt | 3856 | `2adf2b2bd35520f7bdfd90da611e52e37451370171621ae3dc64085da6448b36` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/amqp/WhitelistBasedTypeModelConfiguration.kt | 2504 | `1572a2ec7277a6844e66b290ff2afddc94e2fd7ca919d6c07b30a618c999f185` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/amqp/custom/BigDecimalSerializer.kt | 516 | `899211eece8fc790d9862227ed3f8a5608487cc3763714c42142ee2ec1cf046d` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/amqp/custom/BigIntegerSerializer.kt | 516 | `3044d121a1a5915e0e71f7b8b7c4a3b4236b53dd78a551f7f6488b861a201f00` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/amqp/custom/BitSetSerializer.kt | 795 | `d5d4cbbbb4dadd5f0dc0bd16c3e1452ba4005d2608b7d67cd7e81bd455b502d3` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/amqp/custom/CertPathSerializer.kt | 1973 | `86024ca9097a8a0a74e40db0a1218357f8f1874852b0fb70e965408e85b1d09b` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/amqp/custom/ClassSerializer.kt | 1789 | `407592d2413d4d50d6561cf491cab6a5a9b58ed9d1afa5166dd5e6e50a86485d` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/amqp/custom/ContractAttachmentSerializer.kt | 1999 | `577e2bfd556f97e6fe95cdae55fbc86aa77fe209662f06d11563037363f0d14f` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/amqp/custom/CurrencySerializer.kt | 462 | `3f1c26ccbe64abe1d7f463ddce76be090acbd4b53fbd41511aa965a472ab9ada` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/amqp/custom/DurationSerializer.kt | 806 | `89d29f0143378d12582b06f4634ed223ee4a50f9a11a8b46415ebb1b7bb5c768` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/amqp/custom/EnumSetSerializer.kt | 1565 | `aca295e5c665161fc1c4a8d305d3d62ef133bc1b60a8cdde27730f68ca6bde3e` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/amqp/custom/InputStreamSerializer.kt | 2117 | `7d250ad2bf81abbb083fca9d4f087900915f13ed88303cceb705479e03260afd` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/amqp/custom/InstantSerializer.kt | 825 | `ba479a45ff3656ff218d5d210fd1f00dd09e06007ab4d461ec81aa08df3e5f33` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/amqp/custom/LocalDateSerializer.kt | 876 | `a4cb0e2342943434bbb42ee9c7d09b96886823040af54ebc535f81c5c9f4b7ba` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/amqp/custom/LocalDateTimeSerializer.kt | 1105 | `450a73e328861b8a15891128de5243a692508f325464c253cbddebd9c95519a0` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/amqp/custom/LocalTimeSerializer.kt | 1058 | `3623299391d8938bf7ebcdb50b319005c33d9555465189f81c1721fde3219fcc` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/amqp/custom/MonthDaySerializer.kt | 802 | `e3e044ffbc2b39f0cad70742d8c6776a9c1ef296df80ef9dc25919833dc184ee` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/amqp/custom/OffsetDateTimeSerializer.kt | 1148 | `9f28bfe246bd17b6b67c91b3e1cb5462e6bbc58d3cea26cf0bdcdf682ad20690` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/amqp/custom/OffsetTimeSerializer.kt | 1064 | `d982780d9ee0a49f35d3d0e7bee88175ab220512bbbbcda8a1b4f39b50388929` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/amqp/custom/OpaqueBytesSubSequenceSerializer.kt | 1056 | `4880b149626e1bae007c9d136bdaa8d6afd8b37287e2bd655ffa1d4663fec405` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/amqp/custom/OptionalSerializer.kt | 855 | `9690141756238b52f6300351217f332ba46caa782807dde0464602df25aefee9` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/amqp/custom/PeriodSerializer.kt | 786 | `25d1c8919e92b44987329e771925db7309d2fb135d1744018070bc01cec087a8` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/amqp/custom/PrivateKeySerializer.kt | 1426 | `9164cd51a5c6d625a22cf7149087482d66d5722c885185a9001a8d3471b83a10` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/amqp/custom/PublicKeySerializer.kt | 2183 | `f3dfed15a5cd994dbf4034d8e884715c4cef33f7563d8999e317445317c703a7` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/amqp/custom/RxNotificationSerializer.kt | 1003 | `e4eac76e99ef7b1de6f8bac86f2507da69a58af2457c09adc89d121231a6b66b` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/amqp/custom/SignableDataSerializer.kt | 4353 | `92d4e133f381c0b475660cfcd9017df77886caa3c96d2be008baf5225d53a9dd` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/amqp/custom/SignatureMetadataSerializer.kt | 4882 | `763e1ae6c1f90ff86ac7170a0bfcb124ca770ef529e6ae4c12a21103bc89c773` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/amqp/custom/SimpleStringSerializer.kt | 315 | `cec066f4c59699e6ab2341b8efb83137f7fae30f998052c01d5450ae563f03f6` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/amqp/custom/StringBufferSerializer.kt | 258 | `d929a93d022923c8b9a9438cbdc7d98007ab6c12f8159420b3fee11031fbeecc` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/amqp/custom/ThrowableSerializer.kt | 6057 | `4030e1910e26d8b3306c661ca81f1f8a7f331fa54ebbd81d4db621b8a779eb85` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/amqp/custom/X509CRLSerializer.kt | 1711 | `58a421ee34bb5ed21616fefbe876be0e7fd3a91803a2cc267aaf3747c5162624` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/amqp/custom/X509CertificateSerializer.kt | 1810 | `5fa9b9437a733df737d33264a2c56036eecec4feeeea4a6ede23b4f464a04921` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/amqp/custom/YearMonthSerializer.kt | 810 | `0e4c2efb85d7ccf0a2475ab0e7e5a21ef3f2ce5f3c807a1de01c4ab2ff381f6b` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/amqp/custom/YearSerializer.kt | 673 | `af157ee7213600d687d167125f171cc65058afd11dd97cf2500c9578943f5c25` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/amqp/custom/ZoneIdSerializer.kt | 781 | `2f7902d0db6bad3b464c47f7325dc6d403ae8ea92707ec2631c26935ca025d09` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/amqp/custom/ZonedDateTimeSerializer.kt | 1233 | `099ee2d4276d8b13256b27c33182f26f574173b7c14e7130073a71b66bafb6de` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/carpenter/ClassCarpenter.kt | 21712 | `7cc06b7e6d666ccf5f3683d6fcf1a61fb43b7cc584616c47e98a269c2c7bae8c` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/carpenter/Exceptions.kt | 1007 | `912b4427f59a62312bf6f643aad17a965ce904b535f0a436eda3d31d59b52d25` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/carpenter/Schema.kt | 4006 | `e00755dacd6c213ca04a42cc061a40a4987a531fd3c47c610bfe0f64fcccebfc` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/carpenter/SchemaFields.kt | 4178 | `28a3154005cb6339eb49ad7077950595d3b9f4b5161d01cbc7e6d1c963497333` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/model/CarpentryDependencyGraph.kt | 6014 | `a5af57a0cb7a82399eff8b18a014691ae786ff4a6ed5cf5ff0d07316b2e20a3b` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/model/EnumTransforms.kt | 7257 | `98629737f9d30b2a6f2426c8d1c6ea363701791910d44a42c7d969e9fe20a1ee` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/model/LocalPropertyInformation.kt | 3824 | `2242ee5eed897fdcdad317d8f3b47e1c64fb661da0a0479712ce6a17b447d64f` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/model/LocalTypeInformation.kt | 20331 | `df7352c572795cb4e044864f6ce4705fa490f072d148476c208b441d677a7483` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/model/LocalTypeInformationBuilder.kt | 29647 | `60c66121361c346909e6da5c82daf30159cb862f1a3f662ee44c845bad79f288` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/model/LocalTypeModel.kt | 6087 | `a73f195397987978c0a222f46ed130c23fb8fe44bd35fc04421310a6494a745a` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/model/RemoteTypeCarpenter.kt | 4140 | `f4a56c7670d3f7e11106bc364655b2b890ed25bab9d41a71e67b596d50e22320` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/model/RemoteTypeInformation.kt | 8846 | `c09ff537d68a30f581f0ecf71991198daaa1af182ab42911461ef81593a9a10d` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/model/TypeIdentifier.kt | 12194 | `28ba81953dd1bc0f0b120cdf88fb0bfd227a5305ee1e328fc80cb3f07561222f` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/model/TypeLoader.kt | 2830 | `479f5a4faceed3a2b7211f47db97cd43b50e1943b62d3ac95e4fab0de03c06e5` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/model/TypeModellingFingerPrinter.kt | 12096 | `249da54057150da1671d33b5a21a456d1fc961a5a1a1895cb278545b15eca86f` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/verifier/CustomSerializationSchemeAdapter.kt | 3423 | `f3dc58114b470ef2de25ac51e63cdb761f2e579792aa86aa2b93be9cd43de779` | 0 |
| serialization/src/main/kotlin/net/corda/serialization/internal/verifier/ExternalVerifierTypes.kt | 5184 | `01d99e6498f2c5a49e06141444a4ba60c02ce4793079286619fbcb98f568058f` | 0 |
| settings.gradle | 4598 | `9047eca9db9dc20decf28314375215181926ccf75b0d34865cbca813248f1532` | 0 |
| tools/blobinspector/build.gradle | 1915 | `31f57918506eaf8d24314e8c8e0c85e1c6de97a73caf8c7cd5afd893d873a33c` | 0 |
| tools/blobinspector/src/main/kotlin/net/corda/blobinspector/BlobInspector.kt | 6931 | `d952853a04e5544278d1d84b501999fa2ef9b74a26399802137d695eadca87e5` | 0 |
| tools/bootstrapper/build.gradle | 1948 | `b03165050c3aa541b463b0860d4d1aa60057ce34ab16176065efe5ebbb41d6ec` | 0 |
| tools/bootstrapper/src/main/kotlin/net/corda/bootstrapper/Main.kt | 6186 | `8597dea0e49485d6d642a924905651e476e93523cfc5c217246c441a7a8ced57` | 0 |
| tools/checkpoint-agent/build.gradle | 1255 | `c48a25011dcaff2d043d2cb0b93d21e2bcb5d71a8452da13a1ac58010cef216c` | 0 |
| tools/checkpoint-agent/src/main/kotlin/net/corda/tools/CheckpointAgent.kt | 24488 | `be60233d22e768d6d883a277362f9b2278262e49781f19ba6d15e69a5e67b293` | 0 |
| tools/cliutils/build.gradle | 885 | `fb60ce9364ee6b8ad64e011ae2cb16939ccf50d8303002ca8a44c1d65b0bc9d8` | 0 |
| tools/cliutils/src/main/kotlin/net/corda/cliutils/CordaCliWrapper.kt | 8909 | `8000c357a95bbed83e351d02f3dbca5149fc33264fa5473782bb96b4f7f977ed` | 0 |
| tools/cliutils/src/main/kotlin/net/corda/cliutils/CordaVersionProvider.kt | 459 | `fd321136e6c756dacd8d7a1f4d988c144bf8007f373d62a0311da6547a6a61a7` | 0 |
| tools/cliutils/src/main/kotlin/net/corda/cliutils/ExitCodes.kt | 151 | `a37afac14231eb65542ac8ea2fb2b66c5a48cc043de2c361a38d64f1ba7e0a70` | 0 |
| tools/cliutils/src/main/kotlin/net/corda/cliutils/InstallShellExtensionsParser.kt | 8235 | `1dd963163b7b0a0882c9c84e53edb03aac88dd40c72999c050046adcc863a391` | 0 |
| tools/demobench/build.gradle | 8189 | `835e997749f81f05220384460657557b7006ce957c62cd251c8c5a307b24e783` | 0 |
| tools/demobench/package/bugfixes/java/sun/swing/JLightweightFrame.java | 17866 | `dd0579ef47e2f9124ed46bae473f637a22bad3f62c2a674965feddd7c0baaa2c` | 0 |
| tools/demobench/src/main/java/net/corda/demobench/config/LoggingConfig.java | 1174 | `c8f717536a14b68c3c6c4d66e690700a880106bc2e4b7bba0f0df8022bb32a50` | 0 |
| tools/demobench/src/main/kotlin/net/corda/demobench/DemoBench.kt | 2999 | `e6dfef4e4a8328b03207671832b0f3f5daf3faa0d2d78f4ecb9420ed49710640` | 0 |
| tools/demobench/src/main/kotlin/net/corda/demobench/explorer/Explorer.kt | 5130 | `8a2f0a098585f941860753c134f1665e124b0decefbe5d7a9f44cab6daa027e5` | 0 |
| tools/demobench/src/main/kotlin/net/corda/demobench/model/DemoBenchNodeInfoFilesCopier.kt | 1453 | `ffb1de39afb6af03e7142cf7ee3dd511b84e48ae2d614c79af411a0845939a4f` | 0 |
| tools/demobench/src/main/kotlin/net/corda/demobench/model/HasCordapps.kt | 114 | `f81d0ab42e0fa4309fabb507fc8100b961ffd79e0ebd2862e846721a20043411` | 0 |
| tools/demobench/src/main/kotlin/net/corda/demobench/model/InstallFactory.kt | 1538 | `65ae86e0669d2ec412a26c58311bc0ab8c2b6a9c75c7f4f0a210391dd3fdbcaa` | 0 |
| tools/demobench/src/main/kotlin/net/corda/demobench/model/JVMConfig.kt | 1752 | `d531d1fe4a0369d7e5868db30a33ebb7de0cc63940ec8951d8245ba1a7b921b0` | 0 |
| tools/demobench/src/main/kotlin/net/corda/demobench/model/NodeConfig.kt | 5518 | `ea085b186d3266139bef28a03cded44068972e3b3e62dc268589753c6df6d90c` | 0 |
| tools/demobench/src/main/kotlin/net/corda/demobench/model/NodeController.kt | 9859 | `443236bb62a1957fc023bd070c0819ca7a4fcbf2c618ef6d6e21a883e2d2aaca` | 0 |
| tools/demobench/src/main/kotlin/net/corda/demobench/model/NodeData.kt | 2523 | `878897108fa7e07bb240f67764108cc93ac94a623dec0975b42366f92ccd8d69` | 0 |
| tools/demobench/src/main/kotlin/net/corda/demobench/model/NodeRpcSettings.kt | 202 | `6ba905e85a5a6d29a69b9d6c92e80bde8642bbbe578b9192abecd33b76093e6e` | 0 |
| tools/demobench/src/main/kotlin/net/corda/demobench/model/NodeState.kt | 96 | `16339648061b1660ccce7719e150009c11775951d97b107afd9868537d9ee0b2` | 0 |
| tools/demobench/src/main/kotlin/net/corda/demobench/plugin/CordappController.kt | 2133 | `f96015bb45e7d79045c3aee37de70b3c46c6ef0e42c1b1dc0532cc8707b75b78` | 0 |
| tools/demobench/src/main/kotlin/net/corda/demobench/profile/ProfileController.kt | 5673 | `b04192ec781cf0ce966ee439c54e3a2919646d23fef334fab7733d0fbc195b06` | 0 |
| tools/demobench/src/main/kotlin/net/corda/demobench/pty/PtyProcessTtyConnector.kt | 905 | `60896e00a9018584b70a0b4183d2b65b4baf781b2986df1d4d430c4b2a8f950f` | 0 |
| tools/demobench/src/main/kotlin/net/corda/demobench/pty/R3Pty.kt | 2643 | `445cfc3f987c8db5d6e9f623e00b9ce1f2b7c638c8c499dfe2f1b71dff8bb50e` | 0 |
| tools/demobench/src/main/kotlin/net/corda/demobench/pty/ZeroFilter.kt | 1808 | `e57973372b0858d9e0dfaa97c6c48d829dcc222ec0ac02109dbfbe4645122df0` | 0 |
| tools/demobench/src/main/kotlin/net/corda/demobench/rpc/NodeRPC.kt | 2787 | `55334fca47cf92428ba1d9bf1b40dda1707a1030370a35ba37e66ba984a6a719` | 0 |
| tools/demobench/src/main/kotlin/net/corda/demobench/ui/CloseableTab.kt | 734 | `92fe838e691e2794e4ef1b4f7ee5301ee20c88e74d3e9a55ca5fb0e5086f26c9` | 0 |
| tools/demobench/src/main/kotlin/net/corda/demobench/ui/PropertyLabel.kt | 995 | `4cdd8a587e42e516feef1df79a4207413a0af662649007035b9e9cab910c84c4` | 0 |
| tools/demobench/src/main/kotlin/net/corda/demobench/views/DemoBenchView.kt | 3676 | `24da8cf9a34ae6885b1822c19d8a0a9322e8e90f660bb0b2676f01ff5ea4542c` | 0 |
| tools/demobench/src/main/kotlin/net/corda/demobench/views/NodeTabView.kt | 12738 | `80acd200e6dcab171e9963578282a5a39addd08f2dc69e9b04700dbc99767cc8` | 0 |
| tools/demobench/src/main/kotlin/net/corda/demobench/views/NodeTerminalView.kt | 10721 | `15b1e14f8487bb095abcf4a0545e13b0a6be2db678526f0a0a5db5d53a83f591` | 0 |
| tools/demobench/src/main/kotlin/net/corda/demobench/web/DBViewer.kt | 1352 | `fd941284341b4b55417ef046f17985b288dd043b8c47c3f4a675a30bebe07630` | 0 |
| tools/demobench/src/main/kotlin/net/corda/demobench/web/WebServer.kt | 3647 | `6bf04f5716184f72b2344a7f6bccd4ace48d8a65fdb0de349a22d3f4c2009863` | 0 |
| tools/demobench/src/main/kotlin/net/corda/demobench/web/WebServerController.kt | 488 | `5d55315222ad1819bbaac87b36e4109c84fc2c5037d14128b663507a664b2c61` | 0 |
| tools/demobench/src/main/kotlin/org/h2/server/web/LocalWebServer.kt | 562 | `8ece0c03be42abda58321dd8b0c24166fcf5ac110161e423d8e4af2379ccf4c5` | 0 |
| tools/error-tool/build.gradle | 740 | `04e8d96a9cca1f069e25aa0151e2b2c7ed5bf52b4217612d7aea89bd685dd3a2` | 0 |
| tools/error-tool/src/main/kotlin/net/corda/errorUtilities/ErrorResourceUtilities.kt | 1538 | `9b00877ef7006401ed65b177cd787ffdd89dc6158bac6a022d0f71865cef6be4` | 0 |
| tools/error-tool/src/main/kotlin/net/corda/errorUtilities/ErrorTool.kt | 972 | `d716fac08403155d27ccc3a4a420965db09538547366a252613dd5982296464a` | 0 |
| tools/error-tool/src/main/kotlin/net/corda/errorUtilities/ErrorToolCLIUtilities.kt | 792 | `5cfbfcc5fe12594e3698209de32b927f00875f6601bef8066cc6333f1f95713c` | 0 |
| tools/error-tool/src/main/kotlin/net/corda/errorUtilities/ErrorToolExceptions.kt | 399 | `8b13d0fdfb8d19bfaead6d5836eaf42b45f5245b936885070a93e1c71e81baf3` | 0 |
| tools/error-tool/src/main/kotlin/net/corda/errorUtilities/docsTable/DocsTableCLI.kt | 2846 | `84395eb53b2e17610f7f77c38e8c501928707aed71c62c90c1d6f2a34c473a9f` | 0 |
| tools/error-tool/src/main/kotlin/net/corda/errorUtilities/docsTable/DocsTableGenerator.kt | 2310 | `3be415f1db0637c206253178d11e6024210bbd27c1011f43b70f32c36a1dda07` | 0 |
| tools/error-tool/src/main/kotlin/net/corda/errorUtilities/resourceGenerator/ResourceGenerator.kt | 3257 | `132eb54b573154921f1659e12c89aabfacf3553a175f20c72d0fdadb1745caf3` | 0 |
| tools/error-tool/src/main/kotlin/net/corda/errorUtilities/resourceGenerator/ResourceGeneratorCLI.kt | 2997 | `3facfcb7b5bbd03d6afe2bd10f6ebd1c6dbab175ed129f4362b1dadfe4dd0ee4` | 0 |
| tools/explorer/build.gradle | 3123 | `6d72f6c1008a4c7aee771200f38ff24ea1d09fc041fad36272cb6d4c0759bd40` | 0 |
| tools/explorer/capsule/build.gradle | 1408 | `0d4e44f75654d2c2f8613c052ac67c5d45c09b242000b6e35f05e1dd4481e701` | 0 |
| tools/explorer/src/main/java/ExplorerCaplet.java | 1630 | `a6a48306c6a99fe8aa128f6b051d9bb51769618096e34038703ab36994dfcd5c` | 0 |
| tools/explorer/src/main/kotlin/net/corda/explorer/AmountDiff.kt | 658 | `69788d2cc583e6093747acb60c271392c362da22cefa21310111e8b037d9e090` | 0 |
| tools/explorer/src/main/kotlin/net/corda/explorer/Main.kt | 4308 | `9eb2f4c6f40e3f32595e24a83b6b9dfe5d22f9a4485ff9cb3e291e1cba73939b` | 0 |
| tools/explorer/src/main/kotlin/net/corda/explorer/formatters/AmountFormatter.kt | 614 | `31bf4388ea0ccdc82a10126b660aa8a89c7c859664520ed85b0c24205dc07863` | 0 |
| tools/explorer/src/main/kotlin/net/corda/explorer/formatters/Formatter.kt | 102 | `e7d45f361a4bf7b85ffa795050949aa97e7ef6899950b9c1b144f94703f07b84` | 0 |
| tools/explorer/src/main/kotlin/net/corda/explorer/formatters/NumberFormatter.kt | 285 | `4c9df6efe132aa3adbd36ca23f79131b3f446d612301705b6b249088eb3364f8` | 0 |
| tools/explorer/src/main/kotlin/net/corda/explorer/formatters/PartyNameFormatter.kt | 379 | `1579102a15721a1abcd2ebaf3a31c9e43e954ac8a5cc1fbca48d1375ff963e1b` | 0 |
| tools/explorer/src/main/kotlin/net/corda/explorer/identicon/IdenticonRenderer.kt | 10051 | `d29d274e601fb7bbeddf8294adf7b3ac67039f43daf8726a3c9bbdaf6c49d0fd` | 0 |
| tools/explorer/src/main/kotlin/net/corda/explorer/model/CordaViewModel.kt | 1415 | `cec7f6a7ea45a2a67db3f584871493271623ee06983cf7797781b37682ee2477` | 0 |
| tools/explorer/src/main/kotlin/net/corda/explorer/model/IssuerModel.kt | 1337 | `718200d0b59292e4e35da0957a97d7899fa159a718c0cbfa7b2312a0e443380a` | 0 |
| tools/explorer/src/main/kotlin/net/corda/explorer/model/ReportingCurrencyModel.kt | 1106 | `d27cba362cd898a3adc3871ade77a79eefbe96d41f9833cfa1ac52acbf695a1e` | 0 |
| tools/explorer/src/main/kotlin/net/corda/explorer/model/SettingsModel.kt | 3838 | `e846fb35ec053d80a1111359944393fbf18dd7d10e4f39c2549c43ec106f0067` | 0 |
| tools/explorer/src/main/kotlin/net/corda/explorer/model/TransactionTypes.kt | 215 | `1852a840e7febe65a130d0c6b029044128fcf14a8fe5f5c7a762bc0ca9bb43e4` | 0 |
| tools/explorer/src/main/kotlin/net/corda/explorer/ui/AdvancedExceptionDialog.kt | 2654 | `2bdf98b5999cf90e18033275944b3ea9d06ca2470a9047c52da966c5618d6697` | 0 |
| tools/explorer/src/main/kotlin/net/corda/explorer/ui/ListViewUtilities.kt | 1057 | `246dac96423ed8d1556d6b6ec7ea602a994e0288c376d86b0cd74492335d51ec` | 0 |
| tools/explorer/src/main/kotlin/net/corda/explorer/ui/SingleRowSelection.kt | 187 | `98c2295488d24499503b03a90f2e3ac986aa4eb8fe82e69ef24db61c50f8c87d` | 0 |
| tools/explorer/src/main/kotlin/net/corda/explorer/ui/TableViewUtilities.kt | 2705 | `913a6e61935fd6f2d058c34d4e48cde7775255b1b169ef8a3710977e128a267c` | 0 |
| tools/explorer/src/main/kotlin/net/corda/explorer/ui/TreeTableViewUtilities.kt | 2257 | `08119b93e064c68313f7b1e7f5647107b1431ca31bc1068fd799c773c3e8748c` | 0 |
| tools/explorer/src/main/kotlin/net/corda/explorer/views/Dashboard.kt | 2225 | `5bf2f5e1f83a277a46067d3059b04c168aedbeaf54bf7133ff28341fb3414cf5` | 0 |
| tools/explorer/src/main/kotlin/net/corda/explorer/views/Formatter.kt | 1297 | `c8598750fa17609bd6a2a1b15a2104896cb7bf7f20c85cdc3da94d864442604d` | 0 |
| tools/explorer/src/main/kotlin/net/corda/explorer/views/GuiUtilities.kt | 3415 | `037c68f73df17536c35335723488f60b0fb587d2c4fea504f3a2b2485b61c59f` | 0 |
| tools/explorer/src/main/kotlin/net/corda/explorer/views/LoginView.kt | 4393 | `1163d0cc9cacb80f19e8bc3a1f527f1f86cbe6eae4cddc62d3fe20f9b112dce6` | 0 |
| tools/explorer/src/main/kotlin/net/corda/explorer/views/MainView.kt | 4739 | `0585d9970fb96f8ecd69ecb1e86a8db77ec6f6735d3dcdace4cabf2af6bc71fe` | 0 |
| tools/explorer/src/main/kotlin/net/corda/explorer/views/Network.kt | 13505 | `e9ba468c5a019bbbc0e4ce51c78562339dc95f925f65c57c4fca53badee64cd3` | 0 |
| tools/explorer/src/main/kotlin/net/corda/explorer/views/SearchField.kt | 2993 | `3fd62d6430becd89ef24b35a3524b72a2c6015b5a7a978d2e28ab16f4f9acbaa` | 0 |
| tools/explorer/src/main/kotlin/net/corda/explorer/views/Settings.kt | 2646 | `2cef758baec2974d5e7794ac7ae48b7cebc55ba7b4f5df2bb3eb0f7d9591fab8` | 0 |
| tools/explorer/src/main/kotlin/net/corda/explorer/views/TransactionViewer.kt | 16916 | `c02c64f6a6448283574daf0e9082d810d216ede9a61e9c944a41bfc67507a1e2` | 0 |
| tools/explorer/src/main/kotlin/net/corda/explorer/views/cordapps/cash/CashViewer.kt | 16959 | `9e913b67f3c1a2f3733ae189d3d6e3632371328743d41aa543031bbb410c8b38` | 0 |
| tools/explorer/src/main/kotlin/net/corda/explorer/views/cordapps/cash/NewTransaction.kt | 13014 | `14c41f989d7c94cc337fc0935806a2d7ff9fe3c4099eb67df9c5012801a89693` | 0 |
| tools/graphs/build.gradle | 2827 | `5f9d08c75e488975e5578d34fe8bc5a829d7464085e6b5e5e5b3556d20a101ff` | 0 |
| tools/loadtest/build.gradle | 1926 | `8b63dcce116c01ed0b44db5666c827981a46c69b0bfe4f688ad4656e90a4dc97` | 0 |
| tools/loadtest/src/main/kotlin/net/corda/loadtest/ConnectionManager.kt | 4577 | `8b9fa42086b269e6801b94981f18fb0d51809bbd608025fa427e89a2b6be6171` | 0 |
| tools/loadtest/src/main/kotlin/net/corda/loadtest/Disruption.kt | 4026 | `1147650af34cbdb88ecc525d98db96af84abada94069297e82c4cd5f56c71a20` | 0 |
| tools/loadtest/src/main/kotlin/net/corda/loadtest/LoadTestConfiguration.kt | 2242 | `9ff6500515c3ebfd0c84830e5229edf66df30e0813e0bd149909d5e5b22c76c4` | 0 |
| tools/loadtest/src/main/kotlin/net/corda/loadtest/Main.kt | 8484 | `04e731567c954c6b9d40aad806996daccae95554fbec2843a94b1c3decdc0d2c` | 0 |
| tools/loadtest/src/main/kotlin/net/corda/loadtest/NodeConnection.kt | 6801 | `77ccdaf1e82d5f353c808a579eb84fd47fcc27f4d65542da2348a46182f5bc07` | 0 |
| tools/network-builder/build.gradle | 2927 | `f2de20da5009d06e2862fd60ca5f4fa3324fd1adc0d801064eb36d183a54e8ab` | 0 |
| tools/network-builder/src/main/java/net/corda/networkbuilder/GuiUtils.java | 2146 | `53982b64ba329e99b953c8cb18d0c07c250fee2d1c2c486d56ff86749073d9a2` | 0 |
| tools/network-builder/src/main/kotlin/net/corda/networkbuilder/Constants.kt | 2100 | `bc176d0dbf78c9e69898c1aa47266b673b6932cd2a296e428c1cf70b0e0965c2` | 0 |
| tools/network-builder/src/main/kotlin/net/corda/networkbuilder/Main.kt | 1763 | `044328a051f296366b8f6480b6a6fa5e2e01853079eb0ca41404b1cf641c885f` | 0 |
| tools/network-builder/src/main/kotlin/net/corda/networkbuilder/NetworkBuilder.kt | 9759 | `e98220ec9e5d190853797be5bf2958fbaa2c42d3b583f28d861c450de290c7bb` | 0 |
| tools/network-builder/src/main/kotlin/net/corda/networkbuilder/backends/AzureBackend.kt | 3624 | `a5fd37d14b6ef2f887897e6d41f2014be4c75638a5c2b4e187ed034dcc95e82e` | 0 |
| tools/network-builder/src/main/kotlin/net/corda/networkbuilder/backends/Backend.kt | 1307 | `727f3faa18dd99a09363271396388202c80b74767ed32ca55f6b4d3062d61e46` | 0 |
| tools/network-builder/src/main/kotlin/net/corda/networkbuilder/backends/DockerBackend.kt | 938 | `51d2d9e9551259ab64fee307b83af01e9498f6ac685a50f17bc55bcf80c147e7` | 0 |
| tools/network-builder/src/main/kotlin/net/corda/networkbuilder/cli/CommandLineInterface.kt | 3216 | `896937a94c6987a3db4a52817d287d69fbc3a2f767e721a7d2704c1543795e9d` | 0 |
| tools/network-builder/src/main/kotlin/net/corda/networkbuilder/cli/CommandParsers.kt | 2084 | `1f964c4e244d0f3fe3823644cc86c23b28cc84851113b56362827b32925a2310` | 0 |
| tools/network-builder/src/main/kotlin/net/corda/networkbuilder/containers/instance/InstanceInfo.kt | 324 | `a5e15e832c528003158e545b298193ae3a1fd6d316dde30f99948f2d1fcff27b` | 0 |
| tools/network-builder/src/main/kotlin/net/corda/networkbuilder/containers/instance/Instantiator.kt | 555 | `0871641d42016d2f6da4ead99a8a20b2ba2688bff3f68c74a6d2bf5394753a06` | 0 |
| tools/network-builder/src/main/kotlin/net/corda/networkbuilder/containers/instance/azure/AzureInstantiator.kt | 4566 | `e29f0e95f19646641e1486b0c9fd9ce8679204e4abd4789847dd76bb42685084` | 0 |
| tools/network-builder/src/main/kotlin/net/corda/networkbuilder/containers/instance/docker/DockerInstantiator.kt | 4513 | `ac0e6efe54515ab1dc83082386210203d44334c2a3563d44e8ff174681b4dcbb` | 0 |
| tools/network-builder/src/main/kotlin/net/corda/networkbuilder/containers/push/ContainerPusher.kt | 338 | `7ff17e7f09fbb0c6c5eb4e9b27e1d3fbbbbca0d50ceb14eb03e3c9a8e01a66ce` | 0 |
| tools/network-builder/src/main/kotlin/net/corda/networkbuilder/containers/push/azure/AzureContainerPusher.kt | 2517 | `281f1ac5a6294a0f1806dc3bdbb9a8a44f9262c0e154baf32a87121f46468452` | 0 |
| tools/network-builder/src/main/kotlin/net/corda/networkbuilder/containers/push/azure/AzureRegistryLocator.kt | 2304 | `abdce410bead1d9987dc9f5229f9d3e1dc39b92bbc722e50be3d57d0eaf307da` | 0 |
| tools/network-builder/src/main/kotlin/net/corda/networkbuilder/containers/push/docker/DockerContainerPusher.kt | 664 | `6dde69fbd90b0fb26f217b43c88a7449a95c69fcb11bb31f20e6723f0b429d90` | 0 |
| tools/network-builder/src/main/kotlin/net/corda/networkbuilder/context/Context.kt | 2448 | `999f26dff4c07eb1e497ee822f57c6ee524f72fcf9c15f1ca5ebc03123bb764f` | 0 |
| tools/network-builder/src/main/kotlin/net/corda/networkbuilder/docker/DockerUtils.kt | 1422 | `3eb413227344150e86ca6f74f1c40e718f5d404faf53c2e69cd4e5ff0024343d` | 0 |
| tools/network-builder/src/main/kotlin/net/corda/networkbuilder/gui/BootstrapperView.kt | 15943 | `fabe4ba38a37e1eec28ffe90d20adf3d16e97ab25243f024ef1dc258f8dd48b3` | 0 |
| tools/network-builder/src/main/kotlin/net/corda/networkbuilder/gui/Gui.kt | 264 | `a98835612efacbb9c54840626048c1e49b08ee4bc2676a91c37badf70332961a` | 0 |
| tools/network-builder/src/main/kotlin/net/corda/networkbuilder/nodes/BuiltNode.kt | 826 | `f97ffe56bb6915ff32862584529a637e35509bc0c955fff3ed2eabc58c2c018f` | 0 |
| tools/network-builder/src/main/kotlin/net/corda/networkbuilder/nodes/CopiedNode.kt | 1311 | `dee108dac6b6f620e39689ff0e12bb250fecd943efc55b7be3cb06724f226f7b` | 0 |
| tools/network-builder/src/main/kotlin/net/corda/networkbuilder/nodes/FoundNode.kt | 1511 | `9f913f6ad58e834621c06a7a0962abaf77d484835776a9e3b73a03bbb0311bf4` | 0 |
| tools/network-builder/src/main/kotlin/net/corda/networkbuilder/nodes/NodeAdder.kt | 1273 | `951aee72786cfa6d8fff249952595d7ef5723b2545ec7cfddd8c776adf25a173` | 0 |
| tools/network-builder/src/main/kotlin/net/corda/networkbuilder/nodes/NodeBuilder.kt | 3277 | `fb35c9c14d5849114a840429ea79cedf6e9b61cdab6ffa5c320c737b3d011088` | 0 |
| tools/network-builder/src/main/kotlin/net/corda/networkbuilder/nodes/NodeCopier.kt | 4434 | `91562f893a6b36bd249fd1272c50c061adec7c47278e3b416e251359aa31ccc4` | 0 |
| tools/network-builder/src/main/kotlin/net/corda/networkbuilder/nodes/NodeFinder.kt | 1274 | `a3019ca1ee492e0a9692f669b035a79ebcb1e56553dfa575bde28b47dff98c75` | 0 |
| tools/network-builder/src/main/kotlin/net/corda/networkbuilder/nodes/NodeInstance.kt | 987 | `868cdc6e280d53c12a8564d803bb166ea4b9ac1df1fe000d156604e86dfc7839` | 0 |
| tools/network-builder/src/main/kotlin/net/corda/networkbuilder/nodes/NodeInstanceRequest.kt | 1227 | `1bab4debe6ba75398abd44e29623d08cfbc9b544aa205b85ac3d5383d34ac693` | 0 |
| tools/network-builder/src/main/kotlin/net/corda/networkbuilder/nodes/NodeInstantiator.kt | 4113 | `33d15f786a00d8524772fca939f1285c233cff1e2a57d0581014f942b9fa588b` | 0 |
| tools/network-builder/src/main/kotlin/net/corda/networkbuilder/nodes/NodePusher.kt | 755 | `6963eee6750f9c2d59ae17e85e7bd4f881ac1602d56ea062034d8c4614110d75` | 0 |
| tools/network-builder/src/main/kotlin/net/corda/networkbuilder/nodes/PushedNode.kt | 942 | `96d204ab824e3562a1d2642cca5179a483b35e723fbce6ce3911397b9a987d3a` | 0 |
| tools/network-builder/src/main/kotlin/net/corda/networkbuilder/notaries/CopiedNotary.kt | 520 | `7c93ecb24c61c06351a8e85d5fd4a9a7da0de4b622a678283f392f983a72dcac` | 0 |
| tools/network-builder/src/main/kotlin/net/corda/networkbuilder/notaries/NotaryCopier.kt | 3319 | `61febca96ceb4663e254d5fce33519cb528e61e08468adfb825a071c6e70e653` | 0 |
| tools/network-builder/src/main/kotlin/net/corda/networkbuilder/serialization/SerializationHelper.kt | 1617 | `748699fd26cc39bf61d3edfa1eac65d884cf490da1fb89c3e086c636ee4c7385` | 0 |
| tools/network-builder/src/main/kotlin/net/corda/networkbuilder/volumes/Volume.kt | 2340 | `66867565adba3eb3f55c6185048e795005515e001f2af54436c9cda33529f909` | 0 |
| tools/network-builder/src/main/kotlin/net/corda/networkbuilder/volumes/azure/AzureSmbVolume.kt | 4184 | `574e82031326451b177c84a2f069fba9328817b3e0d7a91202c1a87406122233` | 0 |
| tools/network-builder/src/main/kotlin/net/corda/networkbuilder/volumes/docker/LocalVolume.kt | 1448 | `c680dbef7c2424b69178b209119078ba8b91bf5dcd3952efb36e6ac6c8857d06` | 0 |
| tools/worldmap/build.gradle | 389 | `f587624413033345276d1aa4111de9d0770c7e95be2c642c67224f7092d94552` | 0 |
| tools/worldmap/src/main/kotlin/net/corda/worldmap/PhysicalLocationStructures.kt | 3746 | `6315204e802cbbb2cb022f61d53c067d4d0983e2645b8fd18999bc052a0d81e1` | 0 |
| verifier/build.gradle | 483 | `cf9162bd9e61a4376b38f83bea33463eebf9367a4972a698bc406de8d8887606` | 0 |
| verifier/src/main/kotlin/net/corda/verifier/ExternalVerificationContext.kt | 2122 | `9b6253a538f48007db7af9b6dda1caca5ff5a120f4fe4c0b7849654af87c742d` | 0 |
| verifier/src/main/kotlin/net/corda/verifier/ExternalVerifier.kt | 10654 | `ef02fd188478ab90545dde8876ad803b24385aa913a3f242f7ac3ba418b7f4d8` | 0 |
| verifier/src/main/kotlin/net/corda/verifier/ExternalVerifierNamedCacheFactory.kt | 1572 | `7328ddf6d8888e336ed6e161ae5d198f754ff1c9b8a4babdb9e236d818c3899f` | 0 |
| verifier/src/main/kotlin/net/corda/verifier/Main.kt | 1527 | `8e16e9e607ce45cbfc75a60931006f8b0f58ddc35cab314056fba1e00986826f` | 0 |
