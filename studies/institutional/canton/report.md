# Security & Post-Quantum Readiness Audit Report

**Project:** canton @ 4eab7a047040 · Digital Asset (Canton) — public repository (passive review)
| | |
|---|---|
| Organization | QSI |
| Report date | 2026-11-06 15:24 UTC |
| Report version | 1 |
| Audit run | 72442494-7235-47fa-a4c5-315573a7a4ac (Document audit) |
| Analyzer engine | qsi-engine 1.3.0 |
| Risk profile | Crypto exchange, custodian or wallet |
| Content SHA-256 | `efbd8a018afeed64113c4427d45e8d0033b998dc55ff0d735a440be80e9c9cb1` |
| Signature key (Ed25519, SHA-256 fingerprint; the signature is the separate file report.sig.json) | `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e` |
> This report presents automated and documented analysis results for the stated scope. It is not a legal opinion, a certification or an attestation of compliance with any standard.

## 1. Executive summary

- Critical: **0**
- High: **4**
- Medium: **9**
- Low: **4**
- Info: **0**

- Confirmed technical vulnerability: 2
- Known vulnerable component: 0
- Confirmed configuration error: 2
- Potential cryptographic risk: 0
- Long-term post-quantum risk: 11
- Improvement recommendation: 2
- Insufficient data: 0

Mosca's inequality (x + y > z): x = 10, y = 5, z = 8 → migration would finish too late under this scenario. _z is a planning assumption chosen per risk profile, not a prediction. A cryptographically relevant quantum computer is not publicly known to exist today._

**Post-quantum maturity: Level 2 of 4 — post-quantum in use outside the critical paths.** Next step: Extend post-quantum protection to the critical roles that stay classical, starting with what can be recorded today (wrapped keys, channel key exchange).

## 2. Scope and boundaries

Mode: Document audit

Repository: <https://github.com/digital-asset/canton> @ `4eab7a047040bb61798b66abde794c8cb27f7746` — evidence links open the lines at this commit.

3314 files, 26171202 bytes in total, 2 redaction(s); the per-file SHA-256 list is in appendix C.

## 3. Methodology

| Area | Status | Count | Examples |
|---|---|---|---|
| source_code | checked | 3154 | base/adjustable-clock/src/main/scala/com/daml/clock/AdjustableClock.scala: 37 lines scanned with 16 rule patterns and 267 registry patterns; base/contextualized-logging/src/main/scala/com/daml/logging/ContextualizedLogger.scala: 50 lines scanned with 16 rule patterns and 267 registry patterns; base/contextualized-logging/src/main/scala/com/daml/logging/JsonStringSerializer.scala: 42 lines scanned with 16 rule patterns and 267 registry patterns |
| tls_code | checked | 1 | base/daml-tls/src/main/scala/com/daml/tls/TlsConfig.scala: TLS key-exchange settings read |
| certificates_and_keys | checked | 4 | performance/src/main/console/tls/participant.crt: certificates/keys parsed; performance/src/main/console/tls/participant.pem: certificates/keys parsed; performance/src/main/console/tls/synchronizer.crt: certificates/keys parsed |
| dependencies | checked | 1 | scripts/pyproject.toml: 0 dependencies parsed (0 pinned) |
| entropy | checked | 1 | random-number generation: 202 code files read with 0 macro definitions from the tree; 0 ineffective guard(s), 0 weak random-bytes provider(s), 0 weak key-generation site(s) |
| osv_advisories | not checked | 1 | no exactly pinned versions to query |

_Long lists are grouped here; the full per-file list is in the JSON report, signed with the same key._

## 4. Assets examined and not examined

- osv_advisories — not checked: no exactly pinned versions to query

## 5. Architecture overview

Static review of the source tree canton at 4eab7a047040bb61798b66abde794c8cb27f7746. 3314 files analysed; of 8786 files, 4254 are test, fuzzing, benchmark or example code and were left out, 1218 are not read by any analyzer, 0 exceed the per-file limit and 0 did not fit the total limit. Files no analyzer reads include: .ci/Dockerfile.canton-build, .ci/Dockerfile.query-stats-postgres, .ci/README.md, .ci/nix-exec, .ci/setup-docker-build-container.sh. 36 files in build-output or dependency-cache directories (.git, .hg, .venv, __pycache__, build, dist, node_modules, target, vendor, venv) were not read. No requests were sent to the owner's systems.

## 6. Overall security posture

- Indicative posture index: **52** / 100 — _Derived from findings in scope (confirmed and potential issues weighted by severity). Indicative only; not comparable across differently scoped audits._
- Quantum-vulnerable share of inventory: 47.4%

## 7. Detailed findings

### QSI-2026-19406 — Private key material present in performance/src/main/console/tls/participant.pem

- Severity: **High** · Classification: Confirmed technical vulnerability · Confidence: High
- Affected asset: `file:performance/src/main/console/tls/participant.pem`
- Data source: performance/src/main/console/tls/participant.pem
- Detection method: PEM header detection.
- Analyzer: certificates 1.3.0 · 2026-11-06 15:24 UTC
- Priority score: 76.8 / 100
- CVSS v3.1: 8.1 (`CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N`)

A 'PRIVATE KEY' block was found at line 1 of performance/src/main/console/tls/participant.pem. QSI redacted the key before storage; the original file still contains it.

**Potential impact.** Anyone with access to this file (repository, backups, CI logs) can impersonate the key owner or decrypt protected data.

**Reproduction steps.**

```
grep -n 'PRIVATE KEY-----' performance/src/main/console/tls/participant.pem
```

**Evidence.**

_file_excerpt · [performance/src/main/console/tls/participant.pem](https://github.com/digital-asset/canton/blob/4eab7a047040bb61798b66abde794c8cb27f7746/performance/src/main/console/tls/participant.pem#L1) · line 1 · SHA-256 8ff5675e3f073e63b697c7e9001d2a28e01d7160748521613aeaa91195b89441_

```
Line 1: -----BEGIN PRIVATE KEY----- … [REDACTED BY QSI] … -----END …
```

**Limitations of the check.** QSI cannot determine whether this key is in production use. The key value was not retained.

**Recommendation.** Treat the key as compromised: rotate it, revoke associated certificates, remove it from version history and store keys in a secrets manager/HSM.

**Retest procedure.** Search the repository and its history for private key headers; confirm the old key is revoked.

### QSI-2026-19410 — Private key material present in performance/src/main/console/tls/synchronizer.pem

- Severity: **High** · Classification: Confirmed technical vulnerability · Confidence: High
- Affected asset: `file:performance/src/main/console/tls/synchronizer.pem`
- Data source: performance/src/main/console/tls/synchronizer.pem
- Detection method: PEM header detection.
- Analyzer: certificates 1.3.0 · 2026-11-06 15:24 UTC
- Priority score: 76.8 / 100
- CVSS v3.1: 8.1 (`CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N`)

A 'PRIVATE KEY' block was found at line 1 of performance/src/main/console/tls/synchronizer.pem. QSI redacted the key before storage; the original file still contains it.

**Potential impact.** Anyone with access to this file (repository, backups, CI logs) can impersonate the key owner or decrypt protected data.

**Reproduction steps.**

```
grep -n 'PRIVATE KEY-----' performance/src/main/console/tls/synchronizer.pem
```

**Evidence.**

_file_excerpt · [performance/src/main/console/tls/synchronizer.pem](https://github.com/digital-asset/canton/blob/4eab7a047040bb61798b66abde794c8cb27f7746/performance/src/main/console/tls/synchronizer.pem#L1) · line 1 · SHA-256 8ff5675e3f073e63b697c7e9001d2a28e01d7160748521613aeaa91195b89441_

```
Line 1: -----BEGIN PRIVATE KEY----- … [REDACTED BY QSI] … -----END …
```

**Limitations of the check.** QSI cannot determine whether this key is in production use. The key value was not retained.

**Recommendation.** Treat the key as compromised: rotate it, revoke associated certificates, remove it from version history and store keys in a secrets manager/HSM.

**Retest procedure.** Search the repository and its history for private key headers; confirm the old key is revoked.

### QSI-2026-19403 — Certificate has expired (localhost)

- Severity: **High** · Classification: Confirmed configuration error · Confidence: High
- Affected asset: `certificate:localhost`
- Data source: performance/src/main/console/tls/participant.crt
- Detection method: X.509 parsing (pyca/cryptography), comparison of notAfter with the analysis time (UTC).
- Analyzer: certificates 1.3.0 · 2026-11-06 15:24 UTC
- Priority score: 61.4 / 100
- CVSS v3.1: not applicable

The X.509 certificate with subject localhost expired on 2024-01-11 (1029 days ago).

**Potential impact.** Clients that validate certificates will refuse connections; users may be trained to ignore warnings.

**Reproduction steps.**

```
openssl x509 -in performance/src/main/console/tls/participant.crt -noout -enddate
```

**Evidence.**

_certificate · performance/src/main/console/tls/participant.crt · line 1 · SHA-256 c295cd5380fb92014753ea7924788adabf36724c6dbd902e0e0746b455df6471_

```
Subject: 1.2.840.113549.1.9.1=canton@digitalasset.com,CN=localhost,OU=PARTICIPANT,O=TESTING
Issuer: 1.2.840.113549.1.9.1=canton@digitalasset.com,OU=ROOT CA,O=TESTING
Serial: 16b05eb89bb687d6c01e2881824a05c0f2692a00
Not before: 2022-01-11T23:45:44+00:00
Not after: 2024-01-11T23:45:44+00:00
Public key: RSA 4096-bit
Signature algorithm: 1.2.840.113549.1.1.11
Signature hash: sha256
CA: False
SAN: localhost
SHA-256 fingerprint: 6abfe817bea30b9d9e5f597b52a12bdebe56d3ec526cad6b1bbec06ef349080d
```

**Limitations of the check.** Document-based analysis: only the supplied file was examined. Deployed configuration may differ; the result reflects the file content at the recorded SHA-256.

**Recommendation.** Renew the certificate and automate renewal (e.g. ACME) with expiry monitoring.

**Retest procedure.** Re-parse the deployed certificate and confirm notAfter is in the future.

### QSI-2026-19407 — Certificate has expired (localhost)

- Severity: **High** · Classification: Confirmed configuration error · Confidence: High
- Affected asset: `certificate:localhost`
- Data source: performance/src/main/console/tls/synchronizer.crt
- Detection method: X.509 parsing (pyca/cryptography), comparison of notAfter with the analysis time (UTC).
- Analyzer: certificates 1.3.0 · 2026-11-06 15:24 UTC
- Priority score: 61.4 / 100
- CVSS v3.1: not applicable

The X.509 certificate with subject localhost expired on 2024-01-11 (1029 days ago).

**Potential impact.** Clients that validate certificates will refuse connections; users may be trained to ignore warnings.

**Reproduction steps.**

```
openssl x509 -in performance/src/main/console/tls/synchronizer.crt -noout -enddate
```

**Evidence.**

_certificate · performance/src/main/console/tls/synchronizer.crt · line 1 · SHA-256 fba9ea853306852b5d15bf1c3f0c8d08dbaae0a9aeb4fb79131cd71bd01ab2fa_

```
Subject: 1.2.840.113549.1.9.1=canton@digitalasset.com,CN=localhost,OU=DOMAIN,O=TESTING
Issuer: 1.2.840.113549.1.9.1=canton@digitalasset.com,OU=ROOT CA,O=TESTING
Serial: 16b05eb89bb687d6c01e2881824a05c0f26929ff
Not before: 2022-01-11T23:45:44+00:00
Not after: 2024-01-11T23:45:44+00:00
Public key: RSA 4096-bit
Signature algorithm: 1.2.840.113549.1.1.11
Signature hash: sha256
CA: False
SAN: localhost
SHA-256 fingerprint: 3716da8a4d6794d5ddd37f9aad323658208ea4bea95ec7733f829a29532e6ebc
```

**Limitations of the check.** Document-based analysis: only the supplied file was examined. Deployed configuration may differ; the result reflects the file content at the recorded SHA-256.

**Recommendation.** Renew the certificate and automate renewal (e.g. ACME) with expiry monitoring.

**Retest procedure.** Re-parse the deployed certificate and confirm notAfter is in the future.

### QSI-2026-19399 — Quantum-vulnerable ECDH: key wrapping and data encryption at rest (10 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:ECDH:key_wrapping`
- Data source: community/app-base/src/main/scala/com/digitalasset/canton/admin/api/client/data/crypto/Encryption.scala
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.3.0 · 2026-11-06 15:24 UTC
- Priority score: 36.9 / 100
- CVSS v3.1: not applicable

31 reference(s) to ECDH across 10 file(s), e.g. community/app-base/src/main/scala/com/digitalasset/canton/admin/api/client/data/crypto/Encryption.scala:57. Role, judged from paths, function names and nearby code: key wrapping and data encryption at rest. Keys or data encrypted to these public keys are stored: anyone who copies them now decrypts them once a CRQC exists (harvest now, decrypt later).

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open community/app-base/src/main/scala/com/digitalasset/canton/admin/api/client/data/crypto/Encryption.scala:57 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [community/app-base/src/main/scala/com/digitalasset/canton/admin/api/client/data/crypto/Encryption.scala](https://github.com/digital-asset/canton/blob/4eab7a047040bb61798b66abde794c8cb27f7746/community/app-base/src/main/scala/com/digitalasset/canton/admin/api/client/data/crypto/Encryption.scala#L57) · line 57 · SHA-256 648160bf0e6f3fdb357c1cf7d810f918cfdedfdfc50729a456371b337699c0ec_

```
   56 |   override protected val pretty: Pretty[EncryptionAlgorithmSpec] = prettyOfString(_.name)
   57 |   case object EciesHkdfHmacSha256Aes128Cbc extends EncryptionAlgorithmSpec {
   58 |     override val name: String = "ECIES_HMAC256_AES128-CBC"
```

_file_excerpt · [community/base/src/main/scala/com/digitalasset/canton/config/CryptoProvider.scala](https://github.com/digital-asset/canton/blob/4eab7a047040bb61798b66abde794c8cb27f7746/community/base/src/main/scala/com/digitalasset/canton/config/CryptoProvider.scala#L81) · line 81 · SHA-256 65d575e480faf7bdee4c7ebac61f9fae8ce48d5860bf1cc8b4d57f1bb06a21ae_

```
   80 |       CryptoProviderScheme(
   81 |         EncryptionAlgorithmSpec.EciesHkdfHmacSha256Aes128Cbc,
   82 |         NonEmpty.mk(
```

_file_excerpt · [community/base/src/main/scala/com/digitalasset/canton/config/CryptoProvider.scala](https://github.com/digital-asset/canton/blob/4eab7a047040bb61798b66abde794c8cb27f7746/community/base/src/main/scala/com/digitalasset/canton/config/CryptoProvider.scala#L84) · line 84 · SHA-256 fd8dc959314d11f072771940336cbc570fb92e037a3107488e8536e70ac8836d_

```
   83 |           Set,
   84 |           EncryptionAlgorithmSpec.EciesHkdfHmacSha256Aes128Cbc,
   85 |           EncryptionAlgorithmSpec.RsaOaepSha256,
```

_file_excerpt · [community/base/src/main/scala/com/digitalasset/canton/config/CryptoProvider.scala](https://github.com/digital-asset/canton/blob/4eab7a047040bb61798b66abde794c8cb27f7746/community/base/src/main/scala/com/digitalasset/canton/config/CryptoProvider.scala#L192) · line 192 · SHA-256 495042512c6834bfd1e881ba7610ca66f44f82f1b2f4cc3865a2a1c4a19dc3b6_

```
  191 |           Set,
  192 |           EncryptionAlgorithmSpec.EciesHkdfHmacSha256Aes128Cbc,
  193 |           EncryptionAlgorithmSpec.RsaOaepSha256,
```

_file_excerpt · [community/base/src/main/scala/com/digitalasset/canton/crypto/Encryption.scala](https://github.com/digital-asset/canton/blob/4eab7a047040bb61798b66abde794c8cb27f7746/community/base/src/main/scala/com/digitalasset/canton/crypto/Encryption.scala#L380) · line 380 · SHA-256 81e8542739379b27c4609fa9869dd1386ef714d0a293f95bf8c37f455912f80b_

```
  379 |    */
  380 |   case object EciesHkdfHmacSha256Aes128Cbc extends EncryptionAlgorithmSpec {
  381 |     override val name: String = "ECIES_HMAC256_AES128-CBC"
```

_file_excerpt · [community/base/src/main/scala/com/digitalasset/canton/crypto/Encryption.scala](https://github.com/digital-asset/canton/blob/4eab7a047040bb61798b66abde794c8cb27f7746/community/base/src/main/scala/com/digitalasset/canton/crypto/Encryption.scala#L415) · line 415 · SHA-256 d50a5300f0c9a03fba504fd0f33dc6719f4b3b2570d66db8661e94c6c3d8e2a8_

```
  414 |       case v30.EncryptionAlgorithmSpec.ENCRYPTION_ALGORITHM_SPEC_ECIES_HKDF_HMAC_SHA256_AES128CBC =>
  415 |         Right(EncryptionAlgorithmSpec.EciesHkdfHmacSha256Aes128Cbc)
  416 |       case v30.EncryptionAlgorithmSpec.ENCRYPTION_ALGORITHM_SPEC_RSA_OAEP_SHA256 =>
```

_file_excerpt · [community/base/src/main/scala/com/digitalasset/canton/crypto/kms/aws/AwsKms.scala](https://github.com/digital-asset/canton/blob/4eab7a047040bb61798b66abde794c8cb27f7746/community/base/src/main/scala/com/digitalasset/canton/crypto/kms/aws/AwsKms.scala#L335) · line 335 · SHA-256 6c5084a90738cf86e9f9c61b0f8cb74f7c0ac1c17512edd16700e907ca00b9a7_

```
  334 |     encryptionAlgorithmSpec match {
  335 |       case EncryptionAlgorithmSpec.EciesHkdfHmacSha256Aes128Cbc =>
  336 |         Left(s"Unsupported encryption key type: ${encryptionAlgorithmSpec.name}")
```

_file_excerpt · [community/base/src/main/scala/com/digitalasset/canton/crypto/kms/driver/v1/KmsDriverSpecsConverter.scala](https://github.com/digital-asset/canton/blob/4eab7a047040bb61798b66abde794c8cb27f7746/community/base/src/main/scala/com/digitalasset/canton/crypto/kms/driver/v1/KmsDriverSpecsConverter.scala#L37) · line 37 · SHA-256 5893396071d67b45e80f93801e0af79d68335a729d711c6d22e8ec9d01b51afc_

```
   36 |     algoSpec match {
   37 |       case EncryptionAlgoSpec.EciesHkdfHmacSha256Aes128Cbc =>
   38 |         crypto.EncryptionAlgorithmSpec.EciesHkdfHmacSha256Aes128Cbc
```

_file_excerpt · [community/base/src/main/scala/com/digitalasset/canton/crypto/kms/driver/v1/KmsDriverSpecsConverter.scala](https://github.com/digital-asset/canton/blob/4eab7a047040bb61798b66abde794c8cb27f7746/community/base/src/main/scala/com/digitalasset/canton/crypto/kms/driver/v1/KmsDriverSpecsConverter.scala#L38) · line 38 · SHA-256 05d8ec5fe7218a5005630ce8d45d4e99999075761dc3012493e1bb7c3786dd60_

```
   37 |       case EncryptionAlgoSpec.EciesHkdfHmacSha256Aes128Cbc =>
   38 |         crypto.EncryptionAlgorithmSpec.EciesHkdfHmacSha256Aes128Cbc
   39 |       case EncryptionAlgoSpec.RsaEsOaepSha256 => crypto.EncryptionAlgorithmSpec.RsaOaepSha256
```

_file_excerpt · [community/base/src/main/scala/com/digitalasset/canton/crypto/kms/driver/v1/KmsDriverSpecsConverter.scala](https://github.com/digital-asset/canton/blob/4eab7a047040bb61798b66abde794c8cb27f7746/community/base/src/main/scala/com/digitalasset/canton/crypto/kms/driver/v1/KmsDriverSpecsConverter.scala#L76) · line 76 · SHA-256 554d00efb97c2eee48a7623640ea8ae9ec7c12d8ff9e5cb17ed7eaf0dd78ff3e_

```
   75 |   ): EncryptionAlgoSpec = spec match {
   76 |     case crypto.EncryptionAlgorithmSpec.EciesHkdfHmacSha256Aes128Cbc =>
   77 |       EncryptionAlgoSpec.EciesHkdfHmacSha256Aes128Cbc
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Wrap keys with ML-KEM or a hybrid KEM (X25519 + ML-KEM-768) and re-wrap the stored keys; data that may already have been copied needs its own assessment.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-19395 — Quantum-vulnerable RSA: transaction and message signing (1 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:RSA:transaction_signing`
- Data source: base/daml-jwt/src/main/scala/com/daml/jwt/JwtSigner.scala
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.3.0 · 2026-11-06 15:24 UTC
- Priority score: 35.6 / 100
- CVSS v3.1: not applicable

1 reference(s) to RSA across 1 file(s), e.g. base/daml-jwt/src/main/scala/com/daml/jwt/JwtSigner.scala:59. Role, judged from paths, function names and nearby code: transaction and message signing. A CRQC derives the private key from a public key that is already known (on chain after the first spend, in reused addresses): funds and approvals controlled by these keys need a migration path.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open base/daml-jwt/src/main/scala/com/daml/jwt/JwtSigner.scala:59 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [base/daml-jwt/src/main/scala/com/daml/jwt/JwtSigner.scala](https://github.com/digital-asset/canton/blob/4eab7a047040bb61798b66abde794c8cb27f7746/base/daml-jwt/src/main/scala/com/daml/jwt/JwtSigner.scala#L59) · line 59 · SHA-256 a95c4fd7b998e483779385cbbc71ee996979b1d67545d67527d1136397e03ab6_

```
   58 |   final case class RSA256(privateKey: [REDACTED] kid: Option[String] = None) extends JwtSigner {
   59 |     def alg = "RS256"
   60 |     def sign(jwt: DecodedJwt[String]): Either[Error, Jwt] =
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains adopt them.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-19396 — Quantum-vulnerable ECDSA: transaction and message signing (1 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:ECDSA:transaction_signing`
- Data source: base/daml-jwt/src/main/scala/com/daml/jwt/JwtSigner.scala
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.3.0 · 2026-11-06 15:24 UTC
- Priority score: 35.6 / 100
- CVSS v3.1: not applicable

3 reference(s) to ECDSA across 1 file(s), e.g. base/daml-jwt/src/main/scala/com/daml/jwt/JwtSigner.scala:100. Role, judged from paths, function names and nearby code: transaction and message signing. A CRQC derives the private key from a public key that is already known (on chain after the first spend, in reused addresses): funds and approvals controlled by these keys need a migration path.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open base/daml-jwt/src/main/scala/com/daml/jwt/JwtSigner.scala:100 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [base/daml-jwt/src/main/scala/com/daml/jwt/JwtSigner.scala](https://github.com/digital-asset/canton/blob/4eab7a047040bb61798b66abde794c8cb27f7746/base/daml-jwt/src/main/scala/com/daml/jwt/JwtSigner.scala#L100) · line 100 · SHA-256 fa9672781691551986dc2c14fc65fbe2fde3a5725ddbc5eee9b8f6f046c51adf_

```
   99 |       with JwtSigner {
  100 |     def alg = "ES256"
  101 |   }
```

_file_excerpt · [base/daml-jwt/src/main/scala/com/daml/jwt/JwtSigner.scala](https://github.com/digital-asset/canton/blob/4eab7a047040bb61798b66abde794c8cb27f7746/base/daml-jwt/src/main/scala/com/daml/jwt/JwtSigner.scala#L106) · line 106 · SHA-256 557e5f61d614cfe3e0c27c56f60731293d0ad027dab4c8a9d7c37d0c768fcd1a_

```
  105 |       with JwtSigner {
  106 |     def alg = "ES384"
  107 |   }
```

_file_excerpt · [base/daml-jwt/src/main/scala/com/daml/jwt/JwtSigner.scala](https://github.com/digital-asset/canton/blob/4eab7a047040bb61798b66abde794c8cb27f7746/base/daml-jwt/src/main/scala/com/daml/jwt/JwtSigner.scala#L112) · line 112 · SHA-256 41f1abf8b3fb03a81a8ff92136abb968e174620c160f2bda289629957d88525a_

```
  111 |       with JwtSigner {
  112 |     def alg = "ES512"
  113 |   }
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains adopt them.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-19397 — Quantum-vulnerable Ed25519: transaction and message signing (1 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:Ed25519:transaction_signing`
- Data source: base/daml-jwt/src/main/scala/com/daml/jwt/JwtSigner.scala
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.3.0 · 2026-11-06 15:24 UTC
- Priority score: 35.6 / 100
- CVSS v3.1: not applicable

1 reference(s) to Ed25519 across 1 file(s), e.g. base/daml-jwt/src/main/scala/com/daml/jwt/JwtSigner.scala:116. Role, judged from paths, function names and nearby code: transaction and message signing. A CRQC derives the private key from a public key that is already known (on chain after the first spend, in reused addresses): funds and approvals controlled by these keys need a migration path.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open base/daml-jwt/src/main/scala/com/daml/jwt/JwtSigner.scala:116 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [base/daml-jwt/src/main/scala/com/daml/jwt/JwtSigner.scala](https://github.com/digital-asset/canton/blob/4eab7a047040bb61798b66abde794c8cb27f7746/base/daml-jwt/src/main/scala/com/daml/jwt/JwtSigner.scala#L116) · line 116 · SHA-256 f95da987ae9d0149593b12737718c6248ba139bcbf47c16b7d0a9b4e2d66a4fa_

```
  115 |   final case class EdDSA(privateKey: [REDACTED] kid: Option[String] = None) extends JwtSigner {
  116 |     def alg = "EdDSA"
  117 |     def sign(jwt: DecodedJwt[String]): Either[Error, Jwt] =
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains adopt them.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-19394 — Quantum-vulnerable ECDSA: role not determined (9 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:ECDSA:general`
- Data source: base/crypto/src/main/scala/com/daml/crypto/MessageSignaturePrototype.scala
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.3.0 · 2026-11-06 15:24 UTC
- Priority score: 34.2 / 100
- CVSS v3.1: not applicable

14 reference(s) to ECDSA across 9 file(s), e.g. base/crypto/src/main/scala/com/daml/crypto/MessageSignaturePrototype.scala:54. Role, judged from paths, function names and nearby code: role not determined. The code does not show what the keys protect; review decides the priority.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open base/crypto/src/main/scala/com/daml/crypto/MessageSignaturePrototype.scala:54 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [base/crypto/src/main/scala/com/daml/crypto/MessageSignaturePrototype.scala](https://github.com/digital-asset/canton/blob/4eab7a047040bb61798b66abde794c8cb27f7746/base/crypto/src/main/scala/com/daml/crypto/MessageSignaturePrototype.scala#L54) · line 54 · SHA-256 365cf506c468b6f15e5af63e3d680d4ec12d85447f7f9083ef4b7335400bf057_

```
   53 | object MessageSignaturePrototype {
   54 |   val Secp256k1 = new MessageSignaturePrototype("NONEwithECDSA")
   55 | }
```

_file_excerpt · [base/crypto/src/main/scala/com/daml/crypto/MessageSignaturePrototypeUtil.scala](https://github.com/digital-asset/canton/blob/4eab7a047040bb61798b66abde794c8cb27f7746/base/crypto/src/main/scala/com/daml/crypto/MessageSignaturePrototypeUtil.scala#L30) · line 30 · SHA-256 b02bd77742374ab0b2ad282d38a2d7451bc800e9d8c792fc0c369071dcb0a7a6_

```
   29 | object MessageSignaturePrototypeUtil {
   30 |   val Secp256k1 = new MessageSignaturePrototypeUtil("NONEwithECDSA")
   31 | }
```

_file_excerpt · [community/base/src/main/scala/com/digitalasset/canton/crypto/CryptoKeyValidation.scala](https://github.com/digital-asset/canton/blob/4eab7a047040bb61798b66abde794c8cb27f7746/community/base/src/main/scala/com/digitalasset/canton/crypto/CryptoKeyValidation.scala#L196) · line 196 · SHA-256 68f7992ce7390794c98ab06afd1b85f8231e57f5de54f09e95272f99428783f3_

```
  195 | 
  196 |       kf = KeyFactory.getInstance("EC", JceSecurityProvider.bouncyCastleProvider)
  197 |       keySpec = kf.getKeySpec(privKey, classOf[ECPrivateKeySpec])
```

_file_excerpt · [community/base/src/main/scala/com/digitalasset/canton/crypto/Encryption.scala](https://github.com/digital-asset/canton/blob/4eab7a047040bb61798b66abde794c8cb27f7746/community/base/src/main/scala/com/digitalasset/canton/crypto/Encryption.scala#L291) · line 291 · SHA-256 82b5c6fc4cc139579356fe906956460fa0106411b8814c6c8f2775fa2fe50d3f_

```
  290 |     // Name of the elliptic curve as expected by Java's ECGenParameterSpec (JCA standard name)
  291 |     override val jcaCurveName: String = "secp256r1"
  292 |     override val experimental: Boolean = false
```

_file_excerpt · [community/base/src/main/scala/com/digitalasset/canton/crypto/Signing.scala](https://github.com/digital-asset/canton/blob/4eab7a047040bb61798b66abde794c8cb27f7746/community/base/src/main/scala/com/digitalasset/canton/crypto/Signing.scala#L988) · line 988 · SHA-256 e3f55d254414373cb5588d58997a3aac8c4ffb6ab9f89a52d7e7a4227b566602_

```
  987 |       v30.SigningKeySpec.SIGNING_KEY_SPEC_EC_P256
  988 |     override val jcaCurveName: String = "secp256r1"
  989 |     override val experimental: Boolean = false
```

_file_excerpt · [community/base/src/main/scala/com/digitalasset/canton/crypto/Signing.scala](https://github.com/digital-asset/canton/blob/4eab7a047040bb61798b66abde794c8cb27f7746/community/base/src/main/scala/com/digitalasset/canton/crypto/Signing.scala#L1010) · line 1010 · SHA-256 929104d4cb412b5fa356ea63aebe91a4f90c2a3e27f4e7a44942fd3db4981947_

```
 1009 |       v30.SigningKeySpec.SIGNING_KEY_SPEC_EC_SECP256K1
 1010 |     override val jcaCurveName: String = "secp256k1"
 1011 |     override val experimental: Boolean = false
```

_file_excerpt · [community/base/src/main/scala/com/digitalasset/canton/crypto/Signing.scala](https://github.com/digital-asset/canton/blob/4eab7a047040bb61798b66abde794c8cb27f7746/community/base/src/main/scala/com/digitalasset/canton/crypto/Signing.scala#L1141) · line 1141 · SHA-256 dba10c202d38ed29457741da982b872004da734dc669c9121b5da8555e50961e_

```
 1140 |     override def approximateSignatureSize: Int = 64
 1141 |     override def jcaAlgorithmName: String = "SHA256withECDSA"
 1142 |     override def experimental: Boolean = false
```

_file_excerpt · [community/base/src/main/scala/com/digitalasset/canton/crypto/provider/jce/JceJwks.scala](https://github.com/digital-asset/canton/blob/4eab7a047040bb61798b66abde794c8cb27f7746/community/base/src/main/scala/com/digitalasset/canton/crypto/provider/jce/JceJwks.scala#L156) · line 156 · SHA-256 dc21fe8c0e549e78484c800cdceba405669a0ca9d9a21717a25639ceae687757_

```
  155 |             Map(
  156 |               "crv" -> Json.fromString("secp256k1"),
  157 |               "x" -> Json.fromString(x),
```

_file_excerpt · [community/base/src/main/scala/com/digitalasset/canton/crypto/provider/jce/JcePrivateCrypto.scala](https://github.com/digital-asset/canton/blob/4eab7a047040bb61798b66abde794c8cb27f7746/community/base/src/main/scala/com/digitalasset/canton/crypto/provider/jce/JcePrivateCrypto.scala#L138) · line 138 · SHA-256 7571a4c8f232d9fad389e76f907a70dbdefecd128ef9818bc7d8b3c09216529c_

```
  137 |       .catchOnly[GeneralSecurityException] {
  138 |         val kpg = KeyPairGenerator.getInstance("EC", JceSecurityProvider.bouncyCastleProvider)
  139 |         kpg.initialize(new ECGenParameterSpec(keySpec.jcaCurveName))
```

_file_excerpt · [community/base/src/main/scala/com/digitalasset/canton/crypto/provider/jce/JcePrivateCrypto.scala](https://github.com/digital-asset/canton/blob/4eab7a047040bb61798b66abde794c8cb27f7746/community/base/src/main/scala/com/digitalasset/canton/crypto/provider/jce/JcePrivateCrypto.scala#L356) · line 356 · SHA-256 29c4e18b33712a6de5d83a8aa35dee7e4d2d76aa93cf00b02fd8cd3c77762770_

```
  355 |         pubSpec = new ECPublicKeySpec(javaPoint, javaParams)
  356 |         keyFactory = KeyFactory.getInstance("EC", JceSecurityProvider.bouncyCastleProvider)
  357 |         derivedPublicKey <- Either
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it; introduce an abstraction layer for crypto-agility.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-19398 — Quantum-vulnerable RSA: authentication and identity (certificates, tokens, device attestation) (2 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:RSA:authentication`
- Data source: base/daml-jwt/src/main/scala/com/daml/jwt/KeyUtils.scala
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.3.0 · 2026-11-06 15:24 UTC
- Priority score: 34.2 / 100
- CVSS v3.1: not applicable

4 reference(s) to RSA across 2 file(s), e.g. base/daml-jwt/src/main/scala/com/daml/jwt/KeyUtils.scala:78. Role, judged from paths, function names and nearby code: authentication and identity (certificates, tokens, device attestation). Short-lived authentication stays safe until a CRQC exists; long-lived identities (device attestation, CA and SSH keys) need a plan earlier.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open base/daml-jwt/src/main/scala/com/daml/jwt/KeyUtils.scala:78 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [base/daml-jwt/src/main/scala/com/daml/jwt/KeyUtils.scala](https://github.com/digital-asset/canton/blob/4eab7a047040bb61798b66abde794c8cb27f7746/base/daml-jwt/src/main/scala/com/daml/jwt/KeyUtils.scala#L78) · line 78 · SHA-256 e30d9c9e8e8f2ee3ea3d2bce2a3c762bca2ee6ed4b92ebcb5eded18f06120124_

```
   77 |       key <- Try {
   78 |         val kf = KeyFactory.getInstance("RSA")
   79 |         val keySpec = new PKCS8EncodedKeySpec(decoded.getBytes)
```

_file_excerpt · [base/daml-jwt/src/main/scala/com/daml/jwt/KeyUtils.scala](https://github.com/digital-asset/canton/blob/4eab7a047040bb61798b66abde794c8cb27f7746/base/daml-jwt/src/main/scala/com/daml/jwt/KeyUtils.scala#L94) · line 94 · SHA-256 b5efc2b5f8f90a617cbbc66ed238257e460eb711044a522eda7fc9c5c79b22d9_

```
   93 |       key <- Try {
   94 |         val kf = KeyFactory.getInstance("RSA")
   95 |         val keySpec = new PKCS8EncodedKeySpec(fileContent)
```

_file_excerpt · [base/daml-jwt/src/main/scala/com/daml/jwt/KeyUtils.scala](https://github.com/digital-asset/canton/blob/4eab7a047040bb61798b66abde794c8cb27f7746/base/daml-jwt/src/main/scala/com/daml/jwt/KeyUtils.scala#L110) · line 110 · SHA-256 4908f2b577a0256649157782d184b31365355397ab7e9f0c65bfea14fb227e45_

```
  109 |          |      "kty": "RSA",
  110 |          |      "alg": "RS256",
  111 |          |      "use": "sig",
```

_file_excerpt · [community/ledger/ledger-api-tools/src/main/scala/com/digitalasset/canton/ledger/api/auth/Main.scala](https://github.com/digital-asset/canton/blob/4eab7a047040bb61798b66abde794c8cb27f7746/community/ledger/ledger-api-tools/src/main/scala/com/digitalasset/canton/ledger/api/auth/Main.scala#L123) · line 123 · SHA-256 50d8ddadc8301589373c30984b095627ccf1aec61e9e93489f8e9d8221cccdb3_

```
  122 |         val jwtPayload = AuthServiceJWTCodec.compactPrint(payload)
  123 |         val jwtHeader = s"""{"alg": "RS256", "typ": "JWT", "kid": "$keyId"}"""
  124 |         val signed: Jwt = JwtSigner
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Keep credentials short-lived and plan ML-DSA certificates, tokens and keys as the ecosystem supports them.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-19400 — Quantum-vulnerable RSA: role not determined (2 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:RSA:general`
- Data source: community/base/src/main/scala/com/digitalasset/canton/crypto/provider/jce/JcePrivateCrypto.scala
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.3.0 · 2026-11-06 15:24 UTC
- Priority score: 34.2 / 100
- CVSS v3.1: not applicable

3 reference(s) to RSA across 2 file(s), e.g. community/base/src/main/scala/com/digitalasset/canton/crypto/provider/jce/JcePrivateCrypto.scala:249. Role, judged from paths, function names and nearby code: role not determined. The code does not show what the keys protect; review decides the priority.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open community/base/src/main/scala/com/digitalasset/canton/crypto/provider/jce/JcePrivateCrypto.scala:249 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [community/base/src/main/scala/com/digitalasset/canton/crypto/provider/jce/JcePrivateCrypto.scala](https://github.com/digital-asset/canton/blob/4eab7a047040bb61798b66abde794c8cb27f7746/community/base/src/main/scala/com/digitalasset/canton/crypto/provider/jce/JcePrivateCrypto.scala#L249) · line 249 · SHA-256 d503b34861800c4d92274a9ddcbaf07b796fe9a8adfc4271ecdd5dc518827c91_

```
  248 |                 val kpGen =
  249 |                   KeyPairGenerator.getInstance("RSA", JceSecurityProvider.bouncyCastleProvider)
  250 |                 kpGen.initialize(new RSAKeyGenParameterSpec(2048, RSAKeyGenParameterSpec.F4))
```

_file_excerpt · [community/base/src/main/scala/com/digitalasset/canton/crypto/provider/jce/JcePrivateCrypto.scala](https://github.com/digital-asset/canton/blob/4eab7a047040bb61798b66abde794c8cb27f7746/community/base/src/main/scala/com/digitalasset/canton/crypto/provider/jce/JcePrivateCrypto.scala#L386) · line 386 · SHA-256 7c778c300e498cdf42a53bbfbcfa5144ab17bbd6acdd92ee67e1dc058ce64bfb_

```
  385 |         pubSpec = new RSAPublicKeySpec(modulus, publicExponent)
  386 |         keyFactory = KeyFactory.getInstance("RSA", JceSecurityProvider.bouncyCastleProvider)
  387 |         derivedPublicKey <- Either
```

_file_excerpt · [scripts/ci/select_rota.py](https://github.com/digital-asset/canton/blob/4eab7a047040bb61798b66abde794c8cb27f7746/scripts/ci/select_rota.py#L184) · line 184 · SHA-256 f55f997298b936d904f94ee4f8b0acba4eda63a9f850d483c72990db8ff9eac8_

```
  183 |     now = int(dt.datetime.now(dt.timezone.utc).timestamp())
  184 |     header = {"alg": "RS256", "typ": "JWT"}
  185 |     claims = {
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it; introduce an abstraction layer for crypto-agility.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-19401 — Quantum-vulnerable Ed25519: authentication and identity (certificates, tokens, device attestation) (1 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:Ed25519:authentication`
- Data source: community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/auth/PartyJWTAuthService.scala
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.3.0 · 2026-11-06 15:24 UTC
- Priority score: 34.2 / 100
- CVSS v3.1: not applicable

1 reference(s) to Ed25519 across 1 file(s), e.g. community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/auth/PartyJWTAuthService.scala:215. Role, judged from paths, function names and nearby code: authentication and identity (certificates, tokens, device attestation). Short-lived authentication stays safe until a CRQC exists; long-lived identities (device attestation, CA and SSH keys) need a plan earlier.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/auth/PartyJWTAuthService.scala:215 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/auth/PartyJWTAuthService.scala](https://github.com/digital-asset/canton/blob/4eab7a047040bb61798b66abde794c8cb27f7746/community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/auth/PartyJWTAuthService.scala#L215) · line 215 · SHA-256 e7935129bdcb56b3cacbd9aa134b7eb3e4c1e2b8793ac724c6b65cbd5b6c460a_

```
  214 |     private object EdDSA extends Verifier {
  215 |       def alg = "EdDSA"
  216 | 
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Keep credentials short-lived and plan ML-DSA certificates, tokens and keys as the ecosystem supports them.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-19402 — Quantum-vulnerable ECDSA: authentication and identity (certificates, tokens, device attestation) (1 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:ECDSA:authentication`
- Data source: community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/auth/PartyJWTAuthService.scala
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.3.0 · 2026-11-06 15:24 UTC
- Priority score: 34.2 / 100
- CVSS v3.1: not applicable

2 reference(s) to ECDSA across 1 file(s), e.g. community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/auth/PartyJWTAuthService.scala:228. Role, judged from paths, function names and nearby code: authentication and identity (certificates, tokens, device attestation). Short-lived authentication stays safe until a CRQC exists; long-lived identities (device attestation, CA and SSH keys) need a plan earlier.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/auth/PartyJWTAuthService.scala:228 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/auth/PartyJWTAuthService.scala](https://github.com/digital-asset/canton/blob/4eab7a047040bb61798b66abde794c8cb27f7746/community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/auth/PartyJWTAuthService.scala#L228) · line 228 · SHA-256 b387db4013948b4bb78c6b29d21f09a5b16f6c9796d24fa9dbc9d44503314b28_

```
  227 |     private object ES256 extends Verifier {
  228 |       def alg = "ES256"
  229 | 
```

_file_excerpt · [community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/auth/PartyJWTAuthService.scala](https://github.com/digital-asset/canton/blob/4eab7a047040bb61798b66abde794c8cb27f7746/community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/auth/PartyJWTAuthService.scala#L241) · line 241 · SHA-256 d700bd4aad607c06c10c3df752dbfcc1cdb06061a658580de6343b4a364919e3_

```
  240 |     private object ES384 extends Verifier {
  241 |       def alg = "ES384"
  242 | 
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Keep credentials short-lived and plan ML-DSA certificates, tokens and keys as the ecosystem supports them.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-19404 — Quantum-vulnerable RSA key in certificate (localhost)

- Severity: **Low** · Classification: Long-term post-quantum risk · Confidence: High
- Affected asset: `certificate:localhost`
- Data source: performance/src/main/console/tls/participant.crt
- Detection method: X.509 public key algorithm identification.
- Analyzer: certificates 1.3.0 · 2026-11-06 15:24 UTC
- Priority score: 36.5 / 100
- CVSS v3.1: not applicable

The certificate localhost uses a RSA 4096-bit public key, valid until 2024-01-11. RSA is broken by Shor's algorithm on a CRQC.

**Potential impact.** For authentication, risk materializes only once a CRQC exists while the key/certificate is still trusted. Certificates are short-lived, so the main concern is the PKI and long-lived roots/intermediates.

**Reproduction steps.**

```
openssl x509 -in performance/src/main/console/tls/participant.crt -noout -text | grep -A2 'Public Key Algorithm'
```

**Evidence.**

_certificate · performance/src/main/console/tls/participant.crt · line 1 · SHA-256 c295cd5380fb92014753ea7924788adabf36724c6dbd902e0e0746b455df6471_

```
Subject: 1.2.840.113549.1.9.1=canton@digitalasset.com,CN=localhost,OU=PARTICIPANT,O=TESTING
Issuer: 1.2.840.113549.1.9.1=canton@digitalasset.com,OU=ROOT CA,O=TESTING
Serial: 16b05eb89bb687d6c01e2881824a05c0f2692a00
Not before: 2022-01-11T23:45:44+00:00
Not after: 2024-01-11T23:45:44+00:00
Public key: RSA 4096-bit
Signature algorithm: 1.2.840.113549.1.1.11
Signature hash: sha256
CA: False
SAN: localhost
SHA-256 fingerprint: 6abfe817bea30b9d9e5f597b52a12bdebe56d3ec526cad6b1bbec06ef349080d
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability.

**Recommendation.** Track in the PQC inventory; prefer short certificate lifetimes; follow CA/Browser Forum and NIST PQC transition guidance for ML-DSA certificates.

**Retest procedure.** Re-audit once PQC or hybrid certificates are deployed.

### QSI-2026-19408 — Quantum-vulnerable RSA key in certificate (localhost)

- Severity: **Low** · Classification: Long-term post-quantum risk · Confidence: High
- Affected asset: `certificate:localhost`
- Data source: performance/src/main/console/tls/synchronizer.crt
- Detection method: X.509 public key algorithm identification.
- Analyzer: certificates 1.3.0 · 2026-11-06 15:24 UTC
- Priority score: 36.5 / 100
- CVSS v3.1: not applicable

The certificate localhost uses a RSA 4096-bit public key, valid until 2024-01-11. RSA is broken by Shor's algorithm on a CRQC.

**Potential impact.** For authentication, risk materializes only once a CRQC exists while the key/certificate is still trusted. Certificates are short-lived, so the main concern is the PKI and long-lived roots/intermediates.

**Reproduction steps.**

```
openssl x509 -in performance/src/main/console/tls/synchronizer.crt -noout -text | grep -A2 'Public Key Algorithm'
```

**Evidence.**

_certificate · performance/src/main/console/tls/synchronizer.crt · line 1 · SHA-256 fba9ea853306852b5d15bf1c3f0c8d08dbaae0a9aeb4fb79131cd71bd01ab2fa_

```
Subject: 1.2.840.113549.1.9.1=canton@digitalasset.com,CN=localhost,OU=DOMAIN,O=TESTING
Issuer: 1.2.840.113549.1.9.1=canton@digitalasset.com,OU=ROOT CA,O=TESTING
Serial: 16b05eb89bb687d6c01e2881824a05c0f26929ff
Not before: 2022-01-11T23:45:44+00:00
Not after: 2024-01-11T23:45:44+00:00
Public key: RSA 4096-bit
Signature algorithm: 1.2.840.113549.1.1.11
Signature hash: sha256
CA: False
SAN: localhost
SHA-256 fingerprint: 3716da8a4d6794d5ddd37f9aad323658208ea4bea95ec7733f829a29532e6ebc
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability.

**Recommendation.** Track in the PQC inventory; prefer short certificate lifetimes; follow CA/Browser Forum and NIST PQC transition guidance for ML-DSA certificates.

**Retest procedure.** Re-audit once PQC or hybrid certificates are deployed.

### QSI-2026-19405 — Leaf certificate validity of 730 days (localhost)

- Severity: **Low** · Classification: Improvement recommendation · Confidence: High
- Affected asset: `certificate:localhost`
- Data source: performance/src/main/console/tls/participant.crt
- Detection method: X.509 validity period computation.
- Analyzer: certificates 1.3.0 · 2026-11-06 15:24 UTC
- Priority score: 30.9 / 100
- CVSS v3.1: not applicable

The end-entity certificate is valid for 730 days. Publicly trusted TLS certificates are limited to 398 days today, and CA/Browser Forum rules are reducing this further.

**Potential impact.** Long-lived certificates extend exposure if the key is compromised and slow down algorithm migration.

**Reproduction steps.**

```
openssl x509 -in performance/src/main/console/tls/participant.crt -noout -dates
```

**Evidence.**

_certificate · performance/src/main/console/tls/participant.crt · line 1 · SHA-256 c295cd5380fb92014753ea7924788adabf36724c6dbd902e0e0746b455df6471_

```
Subject: 1.2.840.113549.1.9.1=canton@digitalasset.com,CN=localhost,OU=PARTICIPANT,O=TESTING
Issuer: 1.2.840.113549.1.9.1=canton@digitalasset.com,OU=ROOT CA,O=TESTING
Serial: 16b05eb89bb687d6c01e2881824a05c0f2692a00
Not before: 2022-01-11T23:45:44+00:00
Not after: 2024-01-11T23:45:44+00:00
Public key: RSA 4096-bit
Signature algorithm: 1.2.840.113549.1.1.11
Signature hash: sha256
CA: False
SAN: localhost
SHA-256 fingerprint: 6abfe817bea30b9d9e5f597b52a12bdebe56d3ec526cad6b1bbec06ef349080d
```

**Limitations of the check.** Document-based analysis: only the supplied file was examined. Deployed configuration may differ; the result reflects the file content at the recorded SHA-256. Private-PKI certificates may intentionally use other policies.

**Recommendation.** Use shorter validity with automated renewal.

**Retest procedure.** Check notBefore/notAfter of the next issuance.

### QSI-2026-19409 — Leaf certificate validity of 730 days (localhost)

- Severity: **Low** · Classification: Improvement recommendation · Confidence: High
- Affected asset: `certificate:localhost`
- Data source: performance/src/main/console/tls/synchronizer.crt
- Detection method: X.509 validity period computation.
- Analyzer: certificates 1.3.0 · 2026-11-06 15:24 UTC
- Priority score: 30.9 / 100
- CVSS v3.1: not applicable

The end-entity certificate is valid for 730 days. Publicly trusted TLS certificates are limited to 398 days today, and CA/Browser Forum rules are reducing this further.

**Potential impact.** Long-lived certificates extend exposure if the key is compromised and slow down algorithm migration.

**Reproduction steps.**

```
openssl x509 -in performance/src/main/console/tls/synchronizer.crt -noout -dates
```

**Evidence.**

_certificate · performance/src/main/console/tls/synchronizer.crt · line 1 · SHA-256 fba9ea853306852b5d15bf1c3f0c8d08dbaae0a9aeb4fb79131cd71bd01ab2fa_

```
Subject: 1.2.840.113549.1.9.1=canton@digitalasset.com,CN=localhost,OU=DOMAIN,O=TESTING
Issuer: 1.2.840.113549.1.9.1=canton@digitalasset.com,OU=ROOT CA,O=TESTING
Serial: 16b05eb89bb687d6c01e2881824a05c0f26929ff
Not before: 2022-01-11T23:45:44+00:00
Not after: 2024-01-11T23:45:44+00:00
Public key: RSA 4096-bit
Signature algorithm: 1.2.840.113549.1.1.11
Signature hash: sha256
CA: False
SAN: localhost
SHA-256 fingerprint: 3716da8a4d6794d5ddd37f9aad323658208ea4bea95ec7733f829a29532e6ebc
```

**Limitations of the check.** Document-based analysis: only the supplied file was examined. Deployed configuration may differ; the result reflects the file content at the recorded SHA-256. Private-PKI certificates may intentionally use other policies.

**Recommendation.** Use shorter validity with automated renewal.

**Retest procedure.** Check notBefore/notAfter of the next issuance.


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

- In use: ML-DSA — community/app-base/src/main/scala/com/digitalasset/canton/admin/api/client/data/crypto/Signing.scala
- In use: ML-DSA — community/base/src/main/scala/com/digitalasset/canton/crypto/Signing.scala
- Classical only — key wrapping and data encryption at rest: ECDH (10 file(s))

**Next step:** Extend post-quantum protection to the critical roles that stay classical, starting with what can be recorded today (wrapped keys, channel key exchange).

_Levels: 0 none; 1 present, not wired; 2 in use outside the critical paths; 3 hybrid in a critical path; 4 post-quantum by default in the critical paths (root of trust, key wrapping, channel key exchange). Judged from code and manifests._

### What the quantum-vulnerable algorithms do

| Role | Algorithms (files) | ID | First step |
|---|---|---|---|
| **key wrapping and data encryption at rest** | ECDH (10) | QSI-2026-19399 | Wrap keys with ML-KEM or a hybrid KEM (X25519 + ML-KEM-768) and re-wrap the stored keys; data that may already have been copied needs its own assessment |
| **transaction and message signing** | ECDSA (1), Ed25519 (1), RSA (1) | QSI-2026-19395, QSI-2026-19396, QSI-2026-19397 | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains adopt them |
| **authentication and identity (certificates, tokens, device attestation)** | RSA (2), ECDSA (1), Ed25519 (1) | QSI-2026-19398, QSI-2026-19401, QSI-2026-19402 | Keep credentials short-lived and plan ML-DSA certificates, tokens and keys as the ecosystem supports them |
| **role not determined** | ECDSA (9), RSA (2) | QSI-2026-19394, QSI-2026-19400 | Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it; introduce an abstraction layer for crypto-agility |

_Roles are judged from file paths, function names and the code around each match; review confirms them. Root-of-trust keys and wrapped keys come first: they are hard to replace or can be recorded today._
No readiness questionnaire was completed for this project.

### Quantum algorithms relevant to this inventory

| Quantum algorithm | Effect | Attack model | Inventoried algorithms (rows) | What it means for this audit |
|---|---|---|---|---|
| Shor's algorithm — factoring | breaks | Q1 | RSA (8) | Breaks RSA at every key length: a longer modulus only raises the cost polynomially. Plan migration to ML-KEM (or a hybrid) for key establishment and ML-DSA / SLH-DSA for signatures; start with keys protecting data that must stay confidential for years (harvest now, decrypt later) and with long-lived signatures. |
| Shor's algorithm — elliptic-curve discrete logarithms | breaks | Q1 | ECDH (10), ECDSA (17), Ed25519 (2) | Elliptic-curve keys are expected to fall before RSA keys of comparable classical strength. On blockchains, coins whose public key is already on chain (reused addresses, pay-to-public-key and Taproot outputs) are exposed first; plan the move to post-quantum signatures and avoid key reuse in the meantime. |
| Grover's algorithm — key search and preimages | weakens (larger keys restore the margin) | Q1 | AES-128 (8), BLAKE2 (1), BLAKE3 (1), HMAC (20), IDEA (1), Keccak-256 (1), SHA-2 (7) | Not a break. 256-bit keys (AES-256, ChaCha20) keep a comfortable margin; AES-128 meets NIST category 1, while some authorities ask for 256-bit keys in quantum-resistant contexts (see the AES-128 entry). Prefer 256-bit keys for long-lived data; 256-bit hashes need no change for preimage resistance. |
| Brassard–Høyer–Tapp — collision search | weakens (larger keys restore the margin) | Q1 | BLAKE2 (1), BLAKE3 (1), Keccak-256 (1), SHA-2 (7) | 256-bit hashes (SHA-256, SHA3-256) remain adequate for collision resistance; 160-bit hashes are already weak classically (SHA-1 collisions are practical). Use 384/512-bit hashes where NIST categories 4–5 are required. |
| Quantum lattice sieving | included in standard parameters | Q1 | ML-DSA (2) | No change for ML-KEM or ML-DSA at the standard parameter sets. A 2024 claim of a polynomial-time quantum LWE algorithm was withdrawn after a bug was found (see claims). |

_Effects: breaks — replace the algorithm; weakens — larger keys or outputs restore the margin; included in standard parameters — no action at standard parameter sets; only with superposition queries — not applicable to ordinary deployments._


## 9. Limitations and assumptions

- This report presents automated and documented analysis results for the stated scope. It is not a legal opinion, a certification or an attestation of compliance with any standard.
- z is a planning assumption chosen per risk profile, not a prediction. A cryptographically relevant quantum computer is not publicly known to exist today.
- osv_advisories: no exactly pinned versions to query

## 10. Remediation plan / Priorities for 30, 60 and 90 days

### 30 days

| Priority | ID | Action | Type | Closure criteria |
|---|---|---|---|---|
| P1 | QSI-2026-19406 | Revoke/rotate the key found in performance/src/main/console/tls/participant.pem immediately and restrict access to the file. | short-term risk reduction | Old key revoked, new key deployed. |
| P1 | QSI-2026-19410 | Revoke/rotate the key found in performance/src/main/console/tls/synchronizer.pem immediately and restrict access to the file. | short-term risk reduction | Old key revoked, new key deployed. |
| P1 | QSI-2026-19403 | Renew the certificate for localhost and enable automated renewal with alerting ≥ 30 days before expiry. | root-cause fix | The deployed certificate is valid and renewal is automated. |
| P1 | QSI-2026-19407 | Renew the certificate for localhost and enable automated renewal with alerting ≥ 30 days before expiry. | root-cause fix | The deployed certificate is valid and renewal is automated. |
### 60 days

| Priority | ID | Action | Type | Closure criteria |
|---|---|---|---|---|
| P1 | QSI-2026-19406 | Move key storage to a secrets manager or HSM; add secret scanning to CI and pre-commit; purge history. | root-cause fix | Secret scanning enforced in CI; no keys in history. |
| P1 | QSI-2026-19410 | Move key storage to a secrets manager or HSM; add secret scanning to CI and pre-commit; purge history. | root-cause fix | Secret scanning enforced in CI; no keys in history. |
### 90 days

| Priority | ID | Action | Type | Closure criteria |
|---|---|---|---|---|
| P3 | QSI-2026-19399 | Add ECDH usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-19395 | Add RSA usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-19396 | Add ECDSA usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-19397 | Add Ed25519 usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-19394 | Add ECDSA usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-19398 | Add RSA usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-19400 | Add RSA usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-19401 | Add Ed25519 usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-19402 | Add ECDSA usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-19404 | Add RSA usages at certificate:localhost to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-19408 | Add RSA usages at certificate:localhost to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-19405 | Use shorter validity with automated renewal. | root-cause fix | Check notBefore/notAfter of the next issuance. |
| P3 | QSI-2026-19409 | Use shorter validity with automated renewal. | root-cause fix | Check notBefore/notAfter of the next issuance. |
| P4 | QSI-2026-19399 | Plan migration of ECDH to Hybrid key establishment with ML-KEM (FIPS 203), e.g. X25519MLKEM768 in TLS 1.3 or mlkem768x25519-sha256 in SSH (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows Hybrid key establishment with ML-KEM (FIPS 203), e.g. X25519MLKEM768 in TLS 1.3 or mlkem768x25519-sha256 in SSH or a hybrid scheme in use. |
| P4 | QSI-2026-19395 | Plan migration of RSA to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-19396 | Plan migration of ECDSA to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-19397 | Plan migration of Ed25519 to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-19394 | Plan migration of ECDSA to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-19398 | Plan migration of RSA to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-19400 | Plan migration of RSA to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-19401 | Plan migration of Ed25519 to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-19402 | Plan migration of ECDSA to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-19404 | Plan migration of RSA to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. or a hybrid scheme in use. |
| P4 | QSI-2026-19408 | Plan migration of RSA to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. or a hybrid scheme in use. |

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
23. NIST SP 800-57 Part 1 Rev. 5 — Recommendation for Key Management — NIST. <https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final> (final (2020))
24. NIST — Post-Quantum Cryptography Standardization: Evaluation Criteria, Security (Call for Proposals, Section 4.A.5) — NIST. <https://csrc.nist.gov/Projects/Post-Quantum-Cryptography/Post-Quantum-Cryptography-Standardization/Evaluation-Criteria/Security-(Evaluation-Criteria)> (security categories: AES-128 key search 2^170/MAXDEPTH quantum gates, AES-192 2^233/MAXDEPTH, AES-256 2^298/MAXDEPTH; MAXDEPTH 2^40–2^96)
25. OWASP Application Security Verification Standard — OWASP. <https://owasp.org/www-project-application-security-verification-standard/> (living standard — check the project page for the current version)
26. P. W. Shor — Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms on a Quantum Computer (SIAM J. Comput., 1997) — SIAM. <https://doi.org/10.1137/S0097539795293172> (peer-reviewed article)
27. R. Babbush et al. — Securing Elliptic Curve Cryptocurrencies against Quantum Vulnerabilities: Resource Estimates and Mitigations (arXiv:2603.28846) — arXiv. <https://arxiv.org/abs/2603.28846> (preprint (2026-03-30, v2 2026-04-15): 256-bit ECDLP with < 1200 logical qubits and < 90 M Toffoli gates (or < 1450 and < 70 M); < 500,000 physical qubits at 10^-3 error, minutes)
28. S. Jaques, M. Naehrig, M. Roetteler, F. Virdia — Implementing Grover oracles for quantum key search on AES and LowMC (EUROCRYPT 2020; arXiv:1910.01700) — Springer / arXiv. <https://arxiv.org/abs/1910.01700> (peer-reviewed article: lower cost estimates for the AES key searches that define the NIST categories)

## Appendices: Cryptographic inventory

By origin: keys and certificates 4 (2 Shor-breakable) · own code 74 (35 Shor-breakable).

| Algorithm | Parameter | Library | Quantum status | Classical status | Count | Locations | Examples |
|---|---|---|---|---|---|---|---|
| IDEA |  |  | weak classically | legacy | 1 | 1 | scripts/ci/todo_refs.py:55 |
| HMAC | HMAC-SHA-256 |  | reduced margin (Grover), approved | acceptable | 4 | 4 | base/crypto/src/jmh/scala/com/daml/crypto/MacPrototypeBenchmark.scala:28; base/crypto/src/main/scala/com/daml/crypto/MacPrototype.scala:44; community/base/src/main/scala/com/digitalasset/canton/crypto/Hmac.scala:29 |
| HMAC | HS256 |  | reduced margin (Grover), approved | acceptable | 2 | 2 | base/daml-jwt/src/main/scala/com/daml/jwt/JwtSigner.scala:38; community/ledger-api-bench-tool/src/main/scala/com/digitalasset/canton/ledger/api/benchtool/AuthorizationHelper.scala:40 |
| HMAC |  |  | reduced margin (Grover), approved | acceptable | 14 | 14 | community/base/src/main/scala/com/digitalasset/canton/crypto/CryptoApi.scala:175; community/base/src/main/scala/com/digitalasset/canton/crypto/Hmac.scala:18; community/base/src/main/scala/com/digitalasset/canton/crypto/Salt.scala:45 |
| AES-128 | AES-128 |  | Grover: acceptable to NIST, below ECCG/ANSSI guidance | acceptable | 8 | 8 | base/daml-tls/src/main/scala/com/daml/tls/TlsConfig.scala:30; community/app-base/src/main/scala/com/digitalasset/canton/admin/api/client/data/crypto/Encryption.scala:78; community/base/src/main/scala/com/digitalasset/canton/config/CryptoProvider.scala:101 |
| BLAKE2 |  |  | Grover: acceptable to NIST, below ECCG/ANSSI guidance | acceptable | 1 | 1 | community/lib/Blake2b/src/main/java/org/bouncycastle/crypto/digests/canton/Blake2bDigest.java:130 |
| BLAKE3 |  |  | Grover: acceptable to NIST, below ECCG/ANSSI guidance | acceptable | 1 | 1 | community/common/src/main/scala/com/digitalasset/canton/crypto/LtHash16Blake3.scala:174 |
| Keccak-256 | Keccak-256 |  | Grover: acceptable to NIST, below ECCG/ANSSI guidance | acceptable | 1 | 1 | community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/error/groups/CommandExecutionErrors.scala:1035 |
| SHA-2 |  |  | Grover: acceptable to NIST, below ECCG/ANSSI guidance | acceptable | 1 | 1 | community/base/src/main/scala/com/digitalasset/canton/crypto/deterministic/encryption/SP800HashDRBGSecureRandom.scala:43 |
| SHA-2 | SHA-256 |  | Grover: acceptable to NIST, below ECCG/ANSSI guidance | acceptable | 6 | 6 | community/base/src/main/scala/com/digitalasset/canton/crypto/deterministic/encryption/SP800HashDRBGSecureRandom.scala:90; performance/src/main/console/tls/participant.crt (line 1); performance/src/main/console/tls/synchronizer.crt (line 1) |
| ML-DSA | ML-DSA-65 |  | post-quantum | acceptable | 2 | 2 | community/app-base/src/main/scala/com/digitalasset/canton/admin/api/client/data/crypto/Signing.scala:53; community/base/src/main/scala/com/digitalasset/canton/crypto/Signing.scala:1020 |
| ECDH |  |  | vulnerable (Shor) | acceptable | 10 | 10 | community/app-base/src/main/scala/com/digitalasset/canton/admin/api/client/data/crypto/Encryption.scala:57; community/base/src/main/scala/com/digitalasset/canton/config/CryptoProvider.scala:81; community/base/src/main/scala/com/digitalasset/canton/crypto/Encryption.scala:380 |
| ECDSA |  |  | vulnerable (Shor) | acceptable | 7 | 7 | base/crypto/src/main/scala/com/daml/crypto/MessageSignaturePrototype.scala:54; base/crypto/src/main/scala/com/daml/crypto/MessageSignaturePrototypeUtil.scala:30; community/base/src/main/scala/com/digitalasset/canton/crypto/CryptoKeyValidation.scala:196 |
| ECDSA | ES256 |  | vulnerable (Shor) | acceptable | 2 | 2 | base/daml-jwt/src/main/scala/com/daml/jwt/JwtSigner.scala:100; community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/auth/PartyJWTAuthService.scala:228 |
| ECDSA | ES384 |  | vulnerable (Shor) | acceptable | 2 | 2 | base/daml-jwt/src/main/scala/com/daml/jwt/JwtSigner.scala:106; community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/auth/PartyJWTAuthService.scala:241 |
| ECDSA | ES512 |  | vulnerable (Shor) | acceptable | 1 | 1 | base/daml-jwt/src/main/scala/com/daml/jwt/JwtSigner.scala:112 |
| ECDSA | P-256 |  | vulnerable (Shor) | acceptable | 2 | 2 | community/base/src/main/scala/com/digitalasset/canton/crypto/Encryption.scala:291; community/base/src/main/scala/com/digitalasset/canton/crypto/Signing.scala:988 |
| ECDSA | secp256k1 |  | vulnerable (Shor) | acceptable | 3 | 3 | community/base/src/main/scala/com/digitalasset/canton/crypto/Signing.scala:1010; community/base/src/main/scala/com/digitalasset/canton/crypto/provider/jce/JceJwks.scala:156; community/daml-lf/data/src/main/scala/com/digitalasset/daml/lf/data/support/crypto/MessageSignatureUtil.scala:32 |
| Ed25519 | EdDSA |  | vulnerable (Shor) | acceptable | 2 | 2 | base/daml-jwt/src/main/scala/com/daml/jwt/JwtSigner.scala:116; community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/auth/PartyJWTAuthService.scala:215 |
| RSA | RS256 |  | vulnerable (Shor) | acceptable | 4 | 4 | base/daml-jwt/src/main/scala/com/daml/jwt/JwtSigner.scala:59; base/daml-jwt/src/main/scala/com/daml/jwt/KeyUtils.scala:110; community/ledger/ledger-api-tools/src/main/scala/com/digitalasset/canton/ledger/api/auth/Main.scala:123 |
| RSA |  |  | vulnerable (Shor) | acceptable | 2 | 2 | base/daml-jwt/src/main/scala/com/daml/jwt/KeyUtils.scala:78; community/base/src/main/scala/com/digitalasset/canton/crypto/provider/jce/JcePrivateCrypto.scala:249 |
| RSA | 4096-bit |  | vulnerable (Shor) | acceptable | 2 | 2 | performance/src/main/console/tls/participant.crt (line 1) — localhost; performance/src/main/console/tls/synchronizer.crt (line 1) — localhost |

_Long lists are grouped here; the full per-file list is in the JSON report, signed with the same key._

## Appendices: Input files

| File | Size | SHA-256 | Redactions |
|---|---|---|---|
| base/adjustable-clock/src/main/scala/com/daml/clock/AdjustableClock.scala | 1305 | `e275b1b99fc72d54d89b318a6e8f6235f685f14c74220d73b25d47cff955d696` | 0 |
| base/contextualized-logging/src/main/scala/com/daml/logging/ContextualizedLogger.scala | 1748 | `2de2c24a8e2eac1d4ae73c5f118bfc859ba25e5c0120f227db457c6a8fd69672` | 0 |
| base/contextualized-logging/src/main/scala/com/daml/logging/JsonStringSerializer.scala | 1378 | `230b145c2cbf74019f9eb9cde871fee9741f8a8d7dd88cfbdf6df5d868e8f336` | 0 |
| base/contextualized-logging/src/main/scala/com/daml/logging/LeveledLogger.scala | 3873 | `4b722451a9c8c4450729c255b317ffe5d088bc8b75550e6aac2c3db96a8c9884` | 0 |
| base/contextualized-logging/src/main/scala/com/daml/logging/LoggingContext.scala | 4448 | `bfcc77fe42bf21bcd6102042efc73538bc693303c3e8634973a4cbd5a8c8c52a` | 0 |
| base/contextualized-logging/src/main/scala/com/daml/logging/LoggingContextOf.scala | 3735 | `590bb9237f218bfc44e965071ef506a0d4a22b2894570c882d0288d6e0071bb8` | 0 |
| base/contextualized-logging/src/main/scala/com/daml/logging/LoggingMarker.scala | 966 | `9e1a4e84c9334053bc69ca8303c085671953a0793f6cff4d6d4a021fed9c2223` | 0 |
| base/contextualized-logging/src/main/scala/com/daml/logging/LoggingValueSerializer.scala | 1857 | `1b42f5501b44a523d11909c2a5daa081348db6bc08ae4275a79c0f0dd3731d1b` | 0 |
| base/contextualized-logging/src/main/scala/com/daml/logging/package.scala | 252 | `fec1b349d68a9dd25374bda9f7982ac03512138f9583af7fda55fc7de990935c` | 0 |
| base/crypto/src/jmh/scala/com/daml/crypto/MacPrototypeBenchmark.scala | 1122 | `14ab751822b56d8f5e5445c5452aaae1b8d6db48bacb23b14e78c56d7152fc4b` | 0 |
| base/crypto/src/jmh/scala/com/daml/crypto/MessageDigestPrototypeBenchmark.scala | 1116 | `77514c1c87a3af01f3dca4eebf21980974049be2e9c5df164f822f884324a21e` | 0 |
| base/crypto/src/main/scala/com/daml/crypto/MacPrototype.scala | 1157 | `cf1a87dabbf50349bfb05177b241ec8f82a16e98105b39e5157e9536a753db7e` | 0 |
| base/crypto/src/main/scala/com/daml/crypto/MessageDigestPrototype.scala | 1444 | `8c82f051e8ce59599f47b2e31ea5d65261fcfc69dbe83d17ec20b38a17e793ac` | 0 |
| base/crypto/src/main/scala/com/daml/crypto/MessageSignaturePrototype.scala | 1678 | `5b14eadf00898fbce25c0afbc548acadb7d344c98e740e9e47e360fdab3afb3d` | 0 |
| base/crypto/src/main/scala/com/daml/crypto/MessageSignaturePrototypeUtil.scala | 1009 | `774f774be2a25b977f450f4b45be28a8860741764cc4cd2bfef688d71fe23912` | 0 |
| base/daml-jwt/src/main/scala/com/daml/jwt/AuthServiceJWTPayload.scala | 20406 | `ba7e75e1df83009c6de66aeb14c99703df27291dd180bd453752509696b6922a` | 0 |
| base/daml-jwt/src/main/scala/com/daml/jwt/Base64.scala | 960 | `3d4f82796be9e389057cb2f55cd0f13b5d568bdb74e94ac33b6ffb956d32dc05` | 0 |
| base/daml-jwt/src/main/scala/com/daml/jwt/Error.scala | 493 | `6a1c2845e61ca05cd9bc419771413db32f029bdd865286dd639af0096823512b` | 0 |
| base/daml-jwt/src/main/scala/com/daml/jwt/JwtDecoder.scala | 654 | `9eade1a8de3b9e1a1405dcb960d7da1afef99db165b0731986e65a6c43c5d4fa` | 0 |
| base/daml-jwt/src/main/scala/com/daml/jwt/JwtFromBearerHeader.scala | 478 | `4b216225d54d371dbcc396d6028f598717917f217fea73f75dbb9afc8996980b` | 0 |
| base/daml-jwt/src/main/scala/com/daml/jwt/JwtGenerator.scala | 253 | `b908a86d938de31f72229ef51f1fe78b3b814600d3583f1f22bd97b177c6e58f` | 0 |
| base/daml-jwt/src/main/scala/com/daml/jwt/JwtSigner.scala | 4890 | `bd4f2bfdc20d186fb0a7e90ecdc96e6a0cd6e05a6236cc09474cd2be169a47fa` | 0 |
| base/daml-jwt/src/main/scala/com/daml/jwt/JwtTimestampLeeway.scala | 1443 | `af2c810f04d773d9b18554241884454b19bd07e0ee932ce5678b9017ffcdbaa2` | 0 |
| base/daml-jwt/src/main/scala/com/daml/jwt/JwtVerifier.scala | 6940 | `4055ffcded2e7d643543463f5af205b39e514f3793804144d3aec7f3b78ba837` | 0 |
| base/daml-jwt/src/main/scala/com/daml/jwt/KeyUtils.scala | 5317 | `733b42cc1203849b7bcf2e1b9fbd49e41a88a335be58c2c95e358cae33bceab5` | 0 |
| base/daml-jwt/src/main/scala/com/daml/jwt/WithExecuteUnsafe.scala | 343 | `1c24f43a396d5be448176bdd4ea4d909531e9a9922fe5b021f161e345833c85d` | 0 |
| base/daml-jwt/src/main/scala/com/daml/jwt/package.scala | 1039 | `4fcc383365e2afc72a0b3f6c6123b8a388b22f404ff3aad687f0b0aa37a4a9c1` | 0 |
| base/daml-tls/src/main/scala/com/daml/tls/OcspProperties.scala | 934 | `4f5c9426bc5514827b605644391fdc2b9a455d625e9b52fbd82f9543f428d89b` | 0 |
| base/daml-tls/src/main/scala/com/daml/tls/ProtocolDisabler.scala | 1118 | `3e1d0dad715bca20720130c466b7016bf651de790624721fe0a9871bb0a7169f` | 0 |
| base/daml-tls/src/main/scala/com/daml/tls/TlsConfig.scala | 11260 | `402df40d35ff5773eb2b7b6f89e6618c56ed2263b1399bfe77dba934df63d1e9` | 0 |
| base/daml-tls/src/main/scala/com/daml/tls/TlsConfiguration.scala | 3184 | `eec7e609af7087d870012397757893dda9122942cac41836234c579fba239e7b` | 0 |
| base/daml-tls/src/main/scala/com/daml/tls/TlsConfigurationCli.scala | 2162 | `881c48be2885a8170646baeaa5cfb17cb832194998ebbafacaa3333751201c31` | 0 |
| base/daml-tls/src/main/scala/com/daml/tls/TlsInfo.scala | 953 | `9b1944afed92af17d2d6527b3505603b78eec2ec8f17df142865f00fcdbdcf11` | 0 |
| base/daml-tls/src/main/scala/com/daml/tls/TlsVersion.scala | 572 | `74caf5435c99c8cde9d4b99459478d7ecae3699e3dfe66d484ad6bcca305ef1b` | 0 |
| base/errors/src/main/scala/com/digitalasset/base/error/Alarm.scala | 1588 | `24f73e90d3300a1d72aa681be901dd87564e8f7bdc482bda4764eb75de481eb0` | 0 |
| base/errors/src/main/scala/com/digitalasset/base/error/BaseError.scala | 4994 | `ec329647a86e042a720aa926fdffb372db424e8c8b50aeb87ff52f9cb9a78a04` | 0 |
| base/errors/src/main/scala/com/digitalasset/base/error/BaseErrorLogger.scala | 1150 | `2c9eb8f2f7dad480caab23613b86ae6e059ea2486990b848de7e42c1704bd504` | 0 |
| base/errors/src/main/scala/com/digitalasset/base/error/DamlError.scala | 1683 | `3abc18618920cc36dd91c769ad8027c3820aec82d1fc1c3f26d1ba1484eb0955` | 0 |
| base/errors/src/main/scala/com/digitalasset/base/error/ErrorCategory.scala | 18874 | `bb83f2a038332963ab1cc6ac6b6a87cf7cce4be302070c2c91a67aca5e83509a` | 0 |
| base/errors/src/main/scala/com/digitalasset/base/error/ErrorClass.scala | 935 | `0db499262321f8efb3d57e82adfdcf7315683d6a37b27a40d6bab8103bd6ff43` | 0 |
| base/errors/src/main/scala/com/digitalasset/base/error/ErrorCode.scala | 8582 | `32053103f909f7dd26c93e033dd4b6c61763babc4f643615203a7888754c8630` | 0 |
| base/errors/src/main/scala/com/digitalasset/base/error/ErrorGroup.scala | 491 | `2f67dbf44bbde7878b238c6509a151ee358c97fcf366b1ba1c683d04d3e172e7` | 0 |
| base/errors/src/main/scala/com/digitalasset/base/error/ErrorResource.scala | 3612 | `f1110cc41c8fe0533ba68c317281e55c0e94ffa13f26c7b2c133de6a3eb842f1` | 0 |
| base/errors/src/main/scala/com/digitalasset/base/error/GrpcStatuses.scala | 853 | `e9f246c4cf2d558dc095341fa288b7fe503d9e4722aa456ef8b9fe5740f381c3` | 0 |
| base/errors/src/main/scala/com/digitalasset/base/error/LogOnCreation.scala | 333 | `d9c387bdb37827f188e7e2066d0ed25f1ae122292b7daf5e31d6cbc3a41f3295` | 0 |
| base/errors/src/main/scala/com/digitalasset/base/error/RpcError.scala | 1025 | `e0493576465847227c9e6e5b1bf1649824174b981b68537ff90694a7dff73fc4` | 0 |
| base/errors/src/main/scala/com/digitalasset/base/error/SerializableErrorComponents.scala | 12299 | `64faf17df4bb697dd6bad7ce09671ebd6ffac5fec7a6c14588e77e7663729503` | 0 |
| base/errors/src/main/scala/com/digitalasset/base/error/utils/DecodedCantonError.scala | 8703 | `341d84c75ddc8482ec296b52058f1c4302e96ebcd59c18f80a16f8a61f72f52e` | 0 |
| base/errors/src/main/scala/com/digitalasset/base/error/utils/ErrorDetails.scala | 4498 | `e077f0832f8302e1f8da816ba2925bd4c9f2f056e405706894636827b338e816` | 0 |
| base/executors/src/main/scala/com/daml/executors/InstrumentedExecutors.scala | 1976 | `3be9d51616edc1d57e9f6a09c19f5182fa8f8f35ee1ed0a28a033284a45af835` | 0 |
| base/executors/src/main/scala/com/daml/executors/executors/NamedExecutionContextExecutorService.scala | 2470 | `09b79ed08f703ae51c611a0a23dca9e36873cbac42ec90dca3386692e079a9bb` | 0 |
| base/executors/src/main/scala/com/daml/executors/executors/NamedExecutor.scala | 323 | `5c456aa8e3b17e45d746e79a2a63b228d493aa766deb55ad8223bd6254dc31a7` | 0 |
| base/executors/src/main/scala/com/digitalasset/canton/concurrent/DirectExecutionContext.scala | 1217 | `d05b6b247921f71eb7498cc754fadb902ba4f9b92a2a80edbd19cd4dedce434f` | 0 |
| base/executors/src/main/scala/com/digitalasset/canton/lifecycle/ClosingException.scala | 855 | `840d9ebb18f56556bbb788f56b10e517748ddb9447cc27232825dc5bd727a737` | 0 |
| base/executors/src/main/scala/com/digitalasset/canton/util/ThrowableUtil.scala | 2087 | `4f008b5f7ad679bb58dfcbb1cc447efcaba69c4caffa6e8a9348443bc4a4dc64` | 0 |
| base/executors/src/main/scala/scala/concurrent/BatchingExecutorCanton.scala | 307 | `566c20185330171eb0cb512c3c9a3edf8751913d5f90721881dc50edd7c622dc` | 0 |
| base/grpc-utils/src/main/scala/com/daml/grpc/AuthCallCredentials.java | 1074 | `0a5376987332ede35758c0cb6c54336ce05d2e01d28549deafeca44f3d895afb` | 0 |
| base/grpc-utils/src/main/scala/com/daml/grpc/GrpcException.scala | 2118 | `d4269621e94f92b50b62bdde8a741652c305fc4214780d5c81145153e9c1281f` | 0 |
| base/grpc-utils/src/main/scala/com/daml/grpc/GrpcStatus.scala | 4493 | `83a1ddc04c0ae718b4fcf65b804426bc5683ac643d9856b1947483b2e32ca151` | 0 |
| base/grpc-utils/src/main/scala/com/daml/grpc/RpcProtoExtractors.scala | 528 | `82da711bf18d59a4ffde2712904d5890753a1dbaec96a31f6c2b444bc126a872` | 0 |
| base/ledger-resources/src/main/scala/com/daml/ledger/resources/ResourceContext.scala | 690 | `d6b2827a612560cf302f0368731bba92bbe00b7c1bcb117079b5deb1b55d348d` | 0 |
| base/ledger-resources/src/main/scala/com/daml/ledger/resources/ResourceOwner.scala | 694 | `21342ded02165493f665ce0382f95759e8eb29c337592580d1e710c35077c7c4` | 0 |
| base/ledger-resources/src/main/scala/com/daml/ledger/resources/package.scala | 481 | `e7a883c1cdef8c00b063884583aca05ba405f3f8453ec1d563d53699a2ed81f2` | 0 |
| base/logging-entries/src/main/scala/com/daml/logging/entries/LoggingEntries.scala | 886 | `b469caf78ad987fea010b68733fc1680d5377f965273add3e148fc04615aa420` | 0 |
| base/logging-entries/src/main/scala/com/daml/logging/entries/LoggingValue.scala | 1147 | `ea1638b7804ecdd00591987aaddc6c69cd2483f45b57387d5f901ec0b0caf56e` | 0 |
| base/logging-entries/src/main/scala/com/daml/logging/entries/ToLoggingKey.scala | 419 | `35e49983af849553737bf9312a6dc781941aedc3887b9e5d82131231d2448c8d` | 0 |
| base/logging-entries/src/main/scala/com/daml/logging/entries/ToLoggingValue.scala | 1568 | `a5ccfd6735b296c05d863a2487b70d26c15fb51a72166a2b264195a058f7c656` | 0 |
| base/logging-entries/src/main/scala/com/daml/logging/entries/package.scala | 268 | `185748b4bb6eeb88c89acb4de8c1c449a15f2b9b6aed1612c76931a16e082d3d` | 0 |
| base/nameof/src/main/scala/com/daml/nameof/NameOf.scala | 1620 | `6abe3b668c9fea7cabe3387fc2d80af9e05ea12cd8156249a0ec274c3059b64b` | 0 |
| base/nameof/src/main/scala/com/daml/nameof/NameOfImpl.scala | 1581 | `6d0d1d1ed432f31e1aaf1dbc558794adab18603e98f92406d12be7ca6e5aa2d4` | 0 |
| base/nonempty/src/main/scala/com/digitalasset/nonempty/NonEmpty.scala | 12689 | `8b86a639aaab51a2fbb5bc27b55b32b9bf7357309a469d98ab33989187679282` | 0 |
| base/nonempty/src/main/scala/com/digitalasset/nonempty/NonEmptyCollCompat.scala | 367 | `de7ec34963aa55b4ba5e08ae1db8d2e88e36dbaefa8c01610b27f84be0aeee41` | 0 |
| base/nonempty/src/main/scala/com/digitalasset/nonempty/NonEmptyReturningOps.scala | 1469 | `e7dd9cc83d83974c933fda05fe198170dc4951e747c364abddbe01fd51520c4a` | 0 |
| base/nonempty/src/main/scala/com/digitalasset/nonempty/Patterns.scala | 984 | `26848f07d9ae3eac7b3ef25329a24d2a451d427565ab2828ba6c4ef2315297e8` | 0 |
| base/nonempty/src/main/scala/com/digitalasset/nonempty/catsinstances/impl/CatsInstancesLow.scala | 2105 | `565f8fe5b450ec50e89bb938f8634e51cc7759eb0d899aa3b64a1525c74e1204` | 0 |
| base/nonempty/src/main/scala/com/digitalasset/nonempty/package.scala | 2591 | `d95732899ce774dc2e3a9115267c2ff6c4f2eea3ab28cd0c28b197187b7413de` | 0 |
| base/observability/metrics/src/main/scala/com/daml/metrics/CacheMetrics.scala | 2867 | `933d8a723451f9f3c0473ab801738bcb8ddbf4b6c3195b33356025064d40191e` | 0 |
| base/observability/metrics/src/main/scala/com/daml/metrics/DatabaseMetrics.scala | 4694 | `895477ddb8bb180cd4df40760181ef723ca49ebf56b256ea566286d6c64d70dc` | 0 |
| base/observability/metrics/src/main/scala/com/daml/metrics/ExecutorServiceMetrics.scala | 10736 | `5f03e99f0b08b40b35be71026ffa363f680f94b4b600bacbef67d4080b9417cc` | 0 |
| base/observability/metrics/src/main/scala/com/daml/metrics/HealthMetrics.scala | 1812 | `ca2f7493c8ef325da8468054fa6cb384461d32ba38d82799b837036e48118ba3` | 0 |
| base/observability/metrics/src/main/scala/com/daml/metrics/InstrumentedGraph.scala | 2971 | `4f5350c941ffaccde9c7863dbb45a7a7d7cc4d6bd82366b51fe3caf098a1e0d3` | 0 |
| base/observability/metrics/src/main/scala/com/daml/metrics/MetricsConfig.scala | 1929 | `1c7a40a3480743d0e4aac004cd5a08d10854f93e333a9b92e50270b5926d7e35` | 0 |
| base/observability/metrics/src/main/scala/com/daml/metrics/OnDemandMetricsReader.scala | 1794 | `ba498e915548fcd018de6a272769c9418679432aa93cefd6ecc710ac33a83bc5` | 0 |
| base/observability/metrics/src/main/scala/com/daml/metrics/Timed.scala | 1152 | `aea200524203b06d9903473282cd4369e70aa69d31c53fe76863df2e9d9f9fd7` | 0 |
| base/observability/metrics/src/main/scala/com/daml/metrics/Tracked.scala | 1058 | `1667d17f115088f28d6dda49fddb2477fa51cc841321f5bba69c5adcbca0a5c3` | 0 |
| base/observability/metrics/src/main/scala/com/daml/metrics/api/HistogramInventory.scala | 2831 | `e8566df435cb3c1326dbb43a43729edb383691c4b4707ca300253014825242e1` | 0 |
| base/observability/metrics/src/main/scala/com/daml/metrics/api/MetricHandle.scala | 6521 | `4f8032f6fcef4f67d754b034730537084b1453a7bea787d9ecb380fcfd05f7b9` | 0 |
| base/observability/metrics/src/main/scala/com/daml/metrics/api/MetricName.scala | 668 | `a9b5aad416d33f47fc9c0bb1e2a3153334a39e0d64fa3468a72f3355465ee8c8` | 0 |
| base/observability/metrics/src/main/scala/com/daml/metrics/api/MetricQualification.scala | 1043 | `9a65db6647c3f833e184eb444045cd4a94dec34f7af6300588a61f346848a395` | 0 |
| base/observability/metrics/src/main/scala/com/daml/metrics/api/MetricsContext.scala | 1968 | `00777fd0d15bbd66d71f8971b61ffdf44e5f3335b26bdc1bfd234d761f4cf774` | 0 |
| base/observability/metrics/src/main/scala/com/daml/metrics/api/noop/Metrics.scala | 2300 | `5ec11e7e518d243a4cfaf0b6d7f7a1c0a956ab2915fd83d1bfc4cd02b904e44f` | 0 |
| base/observability/metrics/src/main/scala/com/daml/metrics/api/noop/NoOpMetricsFactory.scala | 1632 | `4cb65f5284a7d265d20187e19c85da7c40beb394f8d3a7d7311fb3a8cb289751` | 0 |
| base/observability/metrics/src/main/scala/com/daml/metrics/api/opentelemetry/OpenTelemetryMetricsFactory.scala | 12945 | `9bc66aec07f81aae896ffa49bb6de6332905b89a7b7e1613d814641654b03139` | 0 |
| base/observability/metrics/src/main/scala/com/daml/metrics/grpc/DamlGrpcServerMetrics.scala | 3112 | `4107ee3df74739ffcf4b2db139a89d45897f0bdcaae1f9ff0576a7d44d566c14` | 0 |
| base/observability/metrics/src/main/scala/com/daml/metrics/grpc/GrpcMetricsServerInterceptor.scala | 4670 | `5b3ad79d28451ae5ff5d8313e48b06c9485bd986498d8b89f7c1661b449bb252` | 0 |
| base/observability/tracing/src/main/scala/com/daml/tracing/Event.scala | 539 | `21affef401c3b1fb6912625404792d9562d9292cead16225f849a18fef4567a8` | 0 |
| base/observability/tracing/src/main/scala/com/daml/tracing/SpanAttribute.scala | 962 | `b8b88a6313576ad1c85a26432e9d94b05ba053f2074adabe1466ebf8e6545a84` | 0 |
| base/observability/tracing/src/main/scala/com/daml/tracing/SpanKind.scala | 524 | `17839433de0ebcd90a77efa0af8648514d2fbb54a19a38b75c1a80e54e31358a` | 0 |
| base/observability/tracing/src/main/scala/com/daml/tracing/SpanName.scala | 321 | `50704ed25515e5348403670a0e7a63c0d91dd2922c012ff2de644e2d392c4e5d` | 0 |
| base/observability/tracing/src/main/scala/com/daml/tracing/Spans.scala | 702 | `d38d11937581e871232475527807a751efa2d146a72660f02a199de12be1aa73` | 0 |
| base/observability/tracing/src/main/scala/com/daml/tracing/package.scala | 407 | `b8b02e9a124e9b35b91740b86df0d1bedd5ae2e9103dfbba6fbaee5171a3b266` | 0 |
| base/ports/src/main/scala/com/daml/ports/FreePort.scala | 4759 | `3d516660397f80a704a7c4ebf3c198d65f64256d0eca9ed12f719e24f035effd` | 0 |
| base/ports/src/main/scala/com/daml/ports/LockedFreePort.scala | 676 | `dc0ae7d750886d19fbae33efa5ef9020dc3c9610241ad92bfaa0f5cfa11f130d` | 0 |
| base/ports/src/main/scala/com/daml/ports/Port.scala | 1035 | `7dc1b98a5fa588f8f8f34bcb5beaf6d2cd340b078b25049671290fc821d2ee6b` | 0 |
| base/ports/src/main/scala/com/daml/ports/PortFiles.scala | 1575 | `d3ef5a9d6d6f9659ae0b55ccfbf2c25bd2e3a36e4eae3c1cd868d1a9cf9de803` | 0 |
| base/ports/src/main/scala/com/daml/ports/PortLock.scala | 2192 | `7a51a70e330059a0e00052339ce49fc8a34621a1524b09cdaa5e0d44b7776b25` | 0 |
| base/resources-grpc/src/main/scala/com/daml/resources/grpc/GrpcResourceOwnerFactories.scala | 2262 | `b000af38afc78b8cc22bf136baf863c8a2df8c77eaece1a1f007eb188d09ed51` | 0 |
| base/resources-grpc/src/main/scala/com/daml/resources/grpc/ManagedChannelResourceOwner.scala | 927 | `ac91ccbd77084d6f10e96aeae94b305e48bca2c30a8474f48057c20f702a7ba7` | 0 |
| base/resources-grpc/src/main/scala/com/daml/resources/grpc/NioEventLoopGroupResourceOwner.scala | 1329 | `b34120aebfcae912af8ff2e6ca8d00aa85b3fee700356db87cd45f303265b6ab` | 0 |
| base/resources-grpc/src/main/scala/com/daml/resources/grpc/ServerResourceOwner.scala | 1140 | `f8b57545e8f4bad8c36ff0e4f23f8f85c8b5f9f8c46160ab583988342c33844d` | 0 |
| base/resources-pekko/src/main/scala/com/daml/resources/pekko/ActorMaterializerResourceOwner.scala | 723 | `5554ba3a47daa3364fa2893b2503cbf247f4cd079bf3dc1436c918ac12ebe40a` | 0 |
| base/resources-pekko/src/main/scala/com/daml/resources/pekko/ActorSystemResourceOwner.scala | 676 | `6eb79ea9f2bebe7774ce9400fb4a0dbd41f2cea21230d68b68ffa35d01021281` | 0 |
| base/resources-pekko/src/main/scala/com/daml/resources/pekko/BoundedSourceQueueResourceOwner.scala | 922 | `415e93436bd84dc1cd199b4ba14a0b9929eb7a57603fa37546c2a43de94b84f0` | 0 |
| base/resources-pekko/src/main/scala/com/daml/resources/pekko/CancellableResourceOwner.scala | 707 | `8768d42087b597552a6cc68056bc9d8fb48849b01fe5e7de7cad7a773353ddae` | 0 |
| base/resources-pekko/src/main/scala/com/daml/resources/pekko/PekkoResourceOwnerFactories.scala | 1728 | `4e6d7e6cf0954b7de0e880b43d73959ef8db813e7af81ad248bedad64a41af77` | 0 |
| base/resources/src/main/scala/daml/resources/AbstractResourceOwner.scala | 3168 | `59f0949093ac843ceb7216f7a2ae86abef6519ba52bbb96e9dc9c9ee987c1331` | 0 |
| base/resources/src/main/scala/daml/resources/CloseableResourceOwner.scala | 524 | `1eaf8e14aa09ea87035c643e6e6010710c8032a91497c342913205bb3fefc823` | 0 |
| base/resources/src/main/scala/daml/resources/ExecutorServiceResourceOwner.scala | 3070 | `c66e53050ab084778e3500c1f6975dd7bd2b225e0f110ca85dc492e64315be29` | 0 |
| base/resources/src/main/scala/daml/resources/FutureCloseableResourceOwner.scala | 542 | `068e597ec149527675e3d10fed410861c713dd00da6f649b5832fbd155463e09` | 0 |
| base/resources/src/main/scala/daml/resources/FutureResourceOwner.scala | 450 | `3c6137c0846550734a22ceab42d9297caedbb2c9068cca6b1605929449162ffc` | 0 |
| base/resources/src/main/scala/daml/resources/HasExecutionContext.scala | 813 | `b8f9a9aa567eab6066505880f72494e8696c9db5f6ff35c95013c402e68535d8` | 0 |
| base/resources/src/main/scala/daml/resources/NestedResource.scala | 2211 | `782ff2a6474d45ce4ab6f287370e29dbef1cdeba871537714cf796067fdabefe` | 0 |
| base/resources/src/main/scala/daml/resources/ProgramResource.scala | 3284 | `853b45e606248e27fa65a35aaabd4b7c91077dabab126a56aa8bff9c4e0b3bce` | 0 |
| base/resources/src/main/scala/daml/resources/PureResource.scala | 642 | `d795434e161f9811749400902368156f6c0f0f50e9cd473fb42002f93d760123` | 0 |
| base/resources/src/main/scala/daml/resources/ReleasableResource.scala | 453 | `c0b8bf46e6b758829336b8801e0c402eb97e5025cf98c31ebd53afd1b50926d1` | 0 |
| base/resources/src/main/scala/daml/resources/ReleasableResourceOwner.scala | 516 | `db6dece6225865db55b22b2cc00231f4e2cb4d274f0f38f40810f820ad68b54a` | 0 |
| base/resources/src/main/scala/daml/resources/Resource.scala | 3753 | `62bd281842e509dcf625eb0fa26871fbbdf721f10ecfdb1f56d20b08eb3a9348` | 0 |
| base/resources/src/main/scala/daml/resources/ResourceAcquisitionFilterException.scala | 321 | `f7b1fa2d82a7006e1f780261247ef06f66b34b425bc0e7e8fa94cdae8a98eabf` | 0 |
| base/resources/src/main/scala/daml/resources/ResourceFactories.scala | 3984 | `0c17d151f82da5d3afe127334748ec65fcc5579235dfa8c71a9164d6b5629589` | 0 |
| base/resources/src/main/scala/daml/resources/ResourceOwnerFactories.scala | 2952 | `736ae0d889573ffbd66ce5977f93a56d3dd5a482ba9138af29c247dd960e9b9a` | 0 |
| base/resources/src/main/scala/daml/resources/TimerResourceOwner.scala | 1477 | `c6e48c49c0a3c819ffe6f8b3ff0926f90e88c2ca6edc3346392167bb3a42f652` | 0 |
| base/resources/src/main/scala/daml/resources/UnitCanBuildFrom.scala | 617 | `aa4132fdbafb74315abcbfe078260147f127e20b299cb4876f128765e0b6f2de` | 0 |
| base/rs-grpc-bridge/src/main/java/com/daml/grpc/adapter/CallCounter.java | 402 | `475975a17d8811977d6f7f9913ed0befae61fbe29b6fbbb43327d0b6232ed3c1` | 0 |
| base/rs-grpc-bridge/src/main/java/com/daml/grpc/adapter/ExecutionSequencer.java | 705 | `dece7e1f62fe97bc3b5321b4f08fcc52cd617011c07f9e856431842f549ae59c` | 0 |
| base/rs-grpc-bridge/src/main/java/com/daml/grpc/adapter/ExecutionSequencerFactory.java | 536 | `5d58ddae5971309a431cfa9b56d4f703371183ce71f0bd05eb4ad7a6885d8483` | 0 |
| base/rs-grpc-bridge/src/main/java/com/daml/grpc/adapter/SingleThreadExecutionSequencer.java | 1395 | `669dd53e39a0cb648cfba137b8860020e93449026be005ee053694531cd9dfb8` | 0 |
| base/rs-grpc-bridge/src/main/java/com/daml/grpc/adapter/SingleThreadExecutionSequencerPool.java | 1537 | `a7ba3772cc98f4cd807c21d399a165db974abb76583de17ed792745b0ea8eb68` | 0 |
| base/rs-grpc-bridge/src/main/java/com/daml/grpc/adapter/client/rs/BufferingResponseObserver.java | 3764 | `10ba86931c587adb68348e9e27193f4e58f3fad9729629e6a80f9cc530068af9` | 0 |
| base/rs-grpc-bridge/src/main/java/com/daml/grpc/adapter/client/rs/BufferingSubscription.java | 6218 | `d426c64d1ddd45be6f4308aa18397f0a201ebb3b3f444b05deb7b41aecca7eb8` | 0 |
| base/rs-grpc-bridge/src/main/java/com/daml/grpc/adapter/client/rs/ClientPublisher.java | 1755 | `473854d7fb6e770bc798e9d360b15b0a2ea3c3e195de9e14473db4476c7fb833` | 0 |
| base/rs-grpc-bridge/src/main/java/com/daml/grpc/adapter/client/rs/DownstreamEventBuffer.java | 3747 | `8a55657ecc1fa9877cdb905d3d818d29eba121b94a70b796595fc7b71fa69064` | 0 |
| base/rs-grpc-bridge/src/main/java/com/daml/grpc/adapter/client/rs/UpstreamEventBuffer.java | 4293 | `ea678088207fb2bd517228cd07c35a72d09e761bdb513a1c0d957f4db9f94602` | 0 |
| base/rs-grpc-bridge/src/main/java/com/daml/grpc/adapter/server/rs/ServerSubscriber.java | 7781 | `8071b01078958ac0a85290cc1a7164b07789148de8b8b1fcdc4d29ac9e12b1b9` | 0 |
| base/rs-grpc-pekko/src/main/scala/com/daml/grpc/adapter/PekkoExecutionSequencer.scala | 3011 | `5cfa6d33b535d91cc27d1ed251fb243ba853652db5f69983f1e5959a689106d3` | 0 |
| base/rs-grpc-pekko/src/main/scala/com/daml/grpc/adapter/PekkoExecutionSequencerPool.scala | 1753 | `3aabce92eb54deaba7993f71db4902b0d776c84d743a4c4126196a5df16175fa` | 0 |
| base/rs-grpc-pekko/src/main/scala/com/daml/grpc/adapter/client/pekko/ClientAdapter.scala | 945 | `fc71052e5039c4483bacc0381bbea6104a260af03b5060d65c6aeac0abba5d06` | 0 |
| base/rs-grpc-pekko/src/main/scala/com/daml/grpc/adapter/server/pekko/ServerAdapter.scala | 1663 | `dbb2d56753c4e4b147eaa4779eed12471da3db030fd94c5f7602200d47c2b927` | 0 |
| base/scala-utils/src/main/scala/com/daml/scalautil/ExceptionOps.scala | 538 | `c78b5fe76a173b7b6a96f0a1c9a324ecd239c2f5fd68c4381fb4d759de0de4d0` | 0 |
| base/scala-utils/src/main/scala/com/daml/scalautil/ImplicitPreference.scala | 439 | `010ad8be8ab769be365ca22bd7d8ff91b44921f4a4a813791e0c69f03d7de645` | 0 |
| base/scala-utils/src/main/scala/com/daml/scalautil/NeverEqualsOverride.scala | 647 | `4c75e74cbb30549f3a6915eda08e4d76656a69b3a4ead618bb81e6fa702bc1c1` | 0 |
| base/scala-utils/src/main/scala/com/daml/scalautil/Statement.scala | 670 | `7139fda260e85e2360eb3440a69c5cc941afe8c1daadc3b7a79bec7fd7aee75b` | 0 |
| base/scala-utils/src/main/scala/com/daml/scalautil/package.scala | 327 | `c6e061d390d8e84c0f8b60fa7c3d4086fbdd61b64769255f79a5bfe418e5cf56` | 0 |
| base/scalatest-utils/src/main/scala/com/daml/scalatest/FlatSpecCheckLaws.scala | 1120 | `b886c2a77eb839a042b4e384721032cefbf2f98e3df0de7df6d871c12b74c047` | 0 |
| base/scalatest-utils/src/main/scala/com/daml/scalatest/WordSpecCheckLaws.scala | 1107 | `eecba0b724f694f4d7bc4815c1d0042d79eef72b0aaa7a2ba2f83fc0589dcde3` | 0 |
| base/scalatest-utils/src/main/scala/com/digitalasset/canton/scalatest/ScalatestEssentials.scala | 1316 | `f7bc85783605ea1e0b9dea26cb1da581114195909904bc66ebc8c01dd8630153` | 0 |
| base/timer-utils/src/main/scala/com/daml/timer/PromiseTask.scala | 765 | `c2a3c868d7c1bb07ca85bf36a5b1bd175134add48ea7dd64f21e708a04b0a763` | 0 |
| base/timer-utils/src/main/scala/com/daml/timer/Timer.scala | 236 | `9a5ce3de3584e2f0c5eb59a3b867324a97b7ae374045697eba068fd6f1b86071` | 0 |
| base/util-external/src/main/scala/com/digitalasset/canton/config/ConfidentialConfigWriter.scala | 641 | `b74a0a2eeba9ca12762ebaab7808dc886381c11400ce7939897f5cfb424fa640` | 0 |
| base/util-external/src/main/scala/com/digitalasset/canton/config/KeyStoreConfig.scala | 861 | `7826247438dc8a542a651baf949bcab08fe2b4a31e3edbbc40e863da9bdc5cd6` | 0 |
| base/util-external/src/main/scala/com/digitalasset/canton/config/PemFileOrString.scala | 1165 | `263b0eb04a8fc4484ccae11ba046782d2ebd147877a3068e0741ce1d8d87ac66` | 0 |
| base/util-external/src/main/scala/com/digitalasset/canton/config/RequireTypes.scala | 16334 | `edd90ef2bf4788a0f0f8e0903df7ddc335d9a64cd5d780c681d0628f6fd0f2a1` | 0 |
| base/util-external/src/main/scala/com/digitalasset/canton/discard/Implicits.scala | 400 | `639fb9d9bf562dbc56d8b194aab64bbed1bcbce86582d32f1a63b33d469e5462` | 0 |
| base/util-external/src/main/scala/com/digitalasset/canton/time/TimeProvider.scala | 295 | `da1a3aa454a44bf69bede9e0e3ea7b3b223a06a0b595bd8ab022dfe16c369fea` | 0 |
| base/util-external/src/main/scala/com/digitalasset/canton/util/BytesUnit.scala | 2041 | `dbc74b5fcc97fbbed5e732f60abb8e566dd1aa3afdbd3f385c28b24489d6866d` | 0 |
| base/util-external/src/main/scala/com/digitalasset/canton/util/JarResourceUtils.scala | 1447 | `d41106b8a5e30ee54421be21d4b63ad49bc8998b4ed09c97cc83e1de7bc03031` | 0 |
| base/util-external/src/main/scala/com/digitalasset/canton/util/Mutex.scala | 2793 | `bbbb981e6bfa1fc194dfa151d5f7e5256c400199fa5d21bb52b2d7bc103561cf` | 0 |
| base/util-external/src/main/scala/com/digitalasset/canton/util/VersionUtil.scala | 1264 | `9982b730058801edd725d40eede26de252f6e216511136932cb5b9b4a7e2391c` | 0 |
| base/validation/src/main/scala/com/digitalasset/base/validation/StringValidator.scala | 2948 | `6e31d08798fa14f424c9a6962eefe90a558ddb5507d4ecd5c6dd3d56aa119175` | 0 |
| community/admin-api/src/main/protobuf/com/digitalasset/canton/admin/crypto/v30/crypto.proto | 389 | `d64fedd29fbced790967d4475c1a60205ec23bb74597ddac736baec45dca58b7` | 0 |
| community/admin-api/src/main/protobuf/com/digitalasset/canton/admin/health/v30/status_service.proto | 2977 | `44753f11b2542cc3eff2ba0624ef12c0de0ed0725af2b7a56f81aa2615bd1ec7` | 0 |
| community/admin-api/src/main/protobuf/com/digitalasset/canton/admin/mediator/v30/mediator_status_service.proto | 802 | `4fc93d8738efe46c58261d0181835da935a957468125c3170fe4d9a93658439f` | 0 |
| community/admin-api/src/main/protobuf/com/digitalasset/canton/admin/participant/v30/acs_import.proto | 3102 | `a7583612d92e58ce7afdcdfd9e2d2021a899cfde856e81f383d9bb443b76c78f` | 0 |
| community/admin-api/src/main/protobuf/com/digitalasset/canton/admin/participant/v30/active_contract.proto | 1216 | `75bb6048160709b5953c5ac4af7e68f5dac61cb447c0c6aaba8741b680e4f32f` | 0 |
| community/admin-api/src/main/protobuf/com/digitalasset/canton/admin/participant/v30/package_service.proto | 5904 | `8b32f2169aa6190f3b5095f211b525256568ec8b5ef6cec3387daf46fad78ab1` | 0 |
| community/admin-api/src/main/protobuf/com/digitalasset/canton/admin/participant/v30/participant_inspection_service.proto | 18087 | `ebcb1c5822379f075ff76600a0dc2f5a0b2654ed7c712faf610fe73f597b9cf7` | 0 |
| community/admin-api/src/main/protobuf/com/digitalasset/canton/admin/participant/v30/participant_repair_service.proto | 19096 | `99dff268d97b22f0167c2934cd91e18c6105222cf1a1624ed4ce6393dbf4fc2c` | 0 |
| community/admin-api/src/main/protobuf/com/digitalasset/canton/admin/participant/v30/participant_replication_service.proto | 383 | `4249bd9e97351bd6d7229fe8073cffbd2f6bcb4b9a6a7c9dadfc4717b9fe800b` | 0 |
| community/admin-api/src/main/protobuf/com/digitalasset/canton/admin/participant/v30/participant_status_service.proto | 1832 | `acf444c73b24f90534bdab7f10264bd802598c319711d4ad5e61deb1b934bf0e` | 0 |
| community/admin-api/src/main/protobuf/com/digitalasset/canton/admin/participant/v30/party_management_service.proto | 26907 | `aea4ea27a3edbf5f689182cdc11c3fcd1905f2472603b95025420d0284816741` | 0 |
| community/admin-api/src/main/protobuf/com/digitalasset/canton/admin/participant/v30/ping_pong_service.proto | 852 | `8d1f481aa527a25b483315f56b6786fc6bb02fc042f81e499a8ebd0509eecc0d` | 0 |
| community/admin-api/src/main/protobuf/com/digitalasset/canton/admin/participant/v30/pruning_service.proto | 6965 | `02acde84e388d9bb6a4ad665149171ed965d7e4f5829bfe2687ca5fe67f073de` | 0 |
| community/admin-api/src/main/protobuf/com/digitalasset/canton/admin/participant/v30/reassignment_id.proto | 383 | `3066f4f3981a1065893fc9a320da8b21922e3bb40bb6b483fa7b0968165d1af7` | 0 |
| community/admin-api/src/main/protobuf/com/digitalasset/canton/admin/participant/v30/resource_management_service.proto | 1277 | `78802b340c7b1e870678d3411650d5c9aa7fb79b2088d8680abea375a4fc4ec5` | 0 |
| community/admin-api/src/main/protobuf/com/digitalasset/canton/admin/participant/v30/synchronizer_connectivity_service.proto | 12197 | `1752fd6b3f4af8c9c33f7cdd7b44707b85350bba13c7ad0efac98207b161ee7b` | 0 |
| community/admin-api/src/main/protobuf/com/digitalasset/canton/admin/participant/v30/traffic_control_service.proto | 1457 | `5c293589d0829a0802c285272d7ecbee1a27deb281858b0aec578370cee0d8d8` | 0 |
| community/admin-api/src/main/protobuf/com/digitalasset/canton/admin/pruning/v30/pruning.proto | 4041 | `4b38029cd9fef4fa79ced59c4b8f164ae28778bf8520324de77ec0fc6bde0234` | 0 |
| community/admin-api/src/main/protobuf/com/digitalasset/canton/admin/scalapb/package.proto | 355 | `eed70675b088bdf359b9f35ff9498396c4067c4a05a5cd6c3d31d7d27972c5be` | 0 |
| community/admin-api/src/main/protobuf/com/digitalasset/canton/admin/sequencer/v30/sequencer_connection.proto | 5692 | `5e1f909541e17f49b8f6926dee3048a78baf05d4f5e68549e09e2fdb2b7e1f8e` | 0 |
| community/admin-api/src/main/protobuf/com/digitalasset/canton/admin/sequencer/v30/sequencer_status_service.proto | 1676 | `c1774a9c79719b8c5392c66bf476ecce82581b270a56e5bf3531543ceaf8acbe` | 0 |
| community/admin-api/src/main/protobuf/com/digitalasset/canton/admin/time/v30/time_tracker_config.proto | 1001 | `7407ba25e6c83e5d21e2de9c4843f65db7a4cf77e627f2ce68360add5192e29c` | 0 |
| community/admin-api/src/main/protobuf/com/digitalasset/canton/admin/topology/v30/common.proto | 579 | `562dfb726744fb4158149537f945569e66768c910749004cd2257249b11b9080` | 0 |
| community/admin-api/src/main/protobuf/com/digitalasset/canton/topology/admin/scalapb/package.proto | 364 | `8e2f782406d4c0b0d0a7a83863d4f8a3a92975439b230b211085615b248209de` | 0 |
| community/admin-api/src/main/protobuf/com/digitalasset/canton/topology/admin/v30/common.proto | 1686 | `2706da1d0a80802f1e0c00b75d306ce20f0df0d8525d49fe3ee3a48f9f8ffbae` | 0 |
| community/admin-api/src/main/protobuf/com/digitalasset/canton/version/ProtocolVersionAnnotation.scala | 1429 | `0fb7ce7e15601264b5c4c5ae0b30479a214b2a81a6f5251348267ff9d2b6744d` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/admin/api/client/AdminApiResponseValidation.scala | 1064 | `4c3f392122bdbf46c7ccf2606000999156ebe8b35aeb532fb13ab3bdc3b13556` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/admin/api/client/GrpcCtlRunner.scala | 2883 | `9563e2f3e16af5d736c693085bac79c71514c28da7ebb489813b1509e54f0f62` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/admin/api/client/commands/AdminCommand.scala | 5295 | `957c2f1e71a822202ea94bcda287aca58107d9a755d4eefeab40b6946fe6bcac` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/admin/api/client/commands/AutoDetectSynchronizerHelper.scala | 1939 | `6ff8dee958dd58eab5552fe831fe09eda052e26620e4aeb51ebf3e65fe1c9527` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/admin/api/client/commands/LedgerApiCommands.scala | 108053 | `c3f79cc72c29332201ceea4c69c342d520618d880daaf629d2096e0d26abecd7` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/admin/api/client/commands/LedgerApiTypeWrappers.scala | 6083 | `5f30ba3d3395bedae91ce367c6d0d1e19a13862f012fe9296c6c93b85c4cab8e` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/admin/api/client/commands/MediatorAdminCommands.scala | 1621 | `330ffad7168ab514f2954f84f813bf979f6d8392fc7eb9958a38ee83f147dea0` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/admin/api/client/commands/MediatorAdministrationCommands.scala | 5228 | `5a90b0509d539c2e0d674670bc6c66418c9e590024815d24e2b5d3fbb7ed0bbe` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/admin/api/client/commands/MediatorInspectionCommands.scala | 2093 | `e79370cba68ca9380092697555e156bbf50bc44399f44bfb526f759a28bf0f22` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/admin/api/client/commands/ParticipantAdminCommands.scala | 113937 | `28ea1c717eb1fd2dc8d4b5b4679288955ce68c60c329c25b52d374dae3e8306d` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/admin/api/client/commands/PruningSchedulerCommands.scala | 6031 | `66be8b3680c5c8c02f18fde7a732050db610f246a89f00ad65d806f47c9d4d96` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/admin/api/client/commands/SequencerAdminCommands.scala | 30346 | `2bfb4700c0263c6cc6b2489bf6562c02ebe758abe66deab1329f46c8aec8048d` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/admin/api/client/commands/SequencerBftAdminCommands.scala | 7785 | `25701e36e734eabd288906e9876ecf34be20fe0fca0177880411f9a502bf0c45` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/admin/api/client/commands/SequencerBftPruningAdminCommands.scala | 6406 | `4b7b678f399924c2b29cbc00343ee15a9a158d743afcc929976096007f971a1e` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/admin/api/client/commands/SequencerConnectionAdminCommands.scala | 3305 | `52e0e29eeb3ad7b295db30d5714a7e07ed1edb602949108eb7de49ba0943754c` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/admin/api/client/commands/SequencerPublicCommands.scala | 4833 | `88eb9c193b0453b3420a8a55de3802175ce39e64340ea2034f457a4fc29786f2` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/admin/api/client/commands/StatusAdminCommands.scala | 4166 | `dd2add61f66f3352b2588493953219d13b51479c7659b43ef765e76432373081` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/admin/api/client/commands/SubscribeBase.scala | 1526 | `62d07cce01fdfd7be04c38d8c2139f936b47fb9f639babd856c9d9d3778e84c5` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/admin/api/client/commands/SynchronizerTimeCommands.scala | 3405 | `0f9902d3e3f31c6994b08ffea2c9ed5899e7942743d6fb2204323db622d16c1e` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/admin/api/client/commands/TopologyAdminCommands.scala | 63046 | `a7f7bdb7ea981d2bd4a1aafdf4da3426c5f7d607dfac44bc8ce0231a58b186d9` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/admin/api/client/commands/VaultAdminCommands.scala | 15268 | `e4d97c9d34276ddd0d14faf10e5bfe71fc8cc909b82d348a764e84c40f0d5194` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/admin/api/client/data/CantonStatus.scala | 3964 | `a325eeea034c46b1d090cf6e294a6492917ef828a984f3747cbbc8f83190e6f4` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/admin/api/client/data/ComponentStatus.scala | 7491 | `6a40031865d6a22fb2313bf2ea2f88d65894b7d6600ed532cbf88368b1272c79` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/admin/api/client/data/ConsoleApiDataObjects.scala | 5359 | `6903f79655a04808c4734da92c4ed200e041224a6e7fc4ca94930d6a31ab4896` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/admin/api/client/data/InFlightCount.scala | 1039 | `65680b0e2d77939d6e662b3b0e47d98502b5e4d6079af6b518c7fc9b42d21111` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/admin/api/client/data/LedgerApiObjectMeta.scala | 439 | `b51dd426d31a4c7b9ec1001c0c02a21c95b1e91f1a31f763b32098d7ff5818c4` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/admin/api/client/data/MediatorStatus.scala | 3633 | `5abd902658fb83486439f819c799c32bff184c2edbc425794cda924d447675a9` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/admin/api/client/data/MemberAuthenticationToken.scala | 833 | `4eedc9881eacd5f15474527eb093eb378a237a3f78f1f6fcd84fbf86d036ac59` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/admin/api/client/data/NodeStatus.scala | 8469 | `6140d3a3f13e8e20e638c356a12a64ec8a699d2196425fe9a26918c7120d873a` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/admin/api/client/data/ParticipantStatus.scala | 5422 | `d2d82dcf50fdbb4f7ffe72a40328c351e4f1356440214d2492593b4bfa70dc32` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/admin/api/client/data/ParticipantSynchronizerLimits.scala | 1194 | `7afeea686af2a91cb8110b8071078ce106f1bc9c809800341309a27f336956fe` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/admin/api/client/data/PartyOnboardingFlagStatus.scala | 1874 | `0dde214168b659333b1ab29e163c0639869f38e716f958703433b000c5629dbb` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/admin/api/client/data/PendingOperationMetadata.scala | 1584 | `c78f5dda8947bf392b78d5105ef330ea2ae30a0595c9a39b9cbb501db0ba5035` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/admin/api/client/data/PruningSchedule.scala | 1901 | `c4120006eee05dcb02ed72601b332e08ccc30c168db465b2deec6173c517bd3a` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/admin/api/client/data/RegisteredSynchronizer.scala | 4299 | `30141cf2bc8563f4beafd01023b5f960344931766cbf8a2f032e3393a5e18ee6` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/admin/api/client/data/SequencerConnection.scala | 6787 | `df764167b50342a39a4d91542eadac9aea9816b9df10fadf5162288ea8f2c9ca` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/admin/api/client/data/SequencerConnections.scala | 20011 | `3971f4333820483eda7549771b9092d72482db7a2ba8aa55f37775faf9480de0` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/admin/api/client/data/SequencerStatus.scala | 7297 | `4106b7f97b399f3de1561e5fdfc1603e091c6fa83b855d0aea00d654332fe130` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/admin/api/client/data/SequencingParameters.scala | 1132 | `c3f75146166037af2f0c4affc8ba801dae3d3c07054649a70d3b5fe2acbd7def` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/admin/api/client/data/SynchronizerConnectionConfig.scala | 16064 | `4660a95955be330b89f7113eb75c5019761a4c38a84b382acb46d449138fcda3` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/admin/api/client/data/SynchronizerLimits.scala | 6365 | `2ec8e5b32f8cf5f54126274aa4ba31867b839dfaca29085d8548a5fc08c1df1d` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/admin/api/client/data/SynchronizerParameters.scala | 33501 | `f4c0e3e4465236d88906c29114507543aaa753dc92a795946bba860d36b77430` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/admin/api/client/data/TemplateId.scala | 1443 | `adc687786a101b0db985aa3a641acc40d9ad53627e19d7bed723ae7da0679345` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/admin/api/client/data/Topology.scala | 5345 | `1f8d31396090dc8f1582a5b754dd52553f910ffd67785e4ca54a20df46ec086c` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/admin/api/client/data/TrafficControlParameters.scala | 3365 | `67776c9999f20deb0965990612e3bc288cd5f195414884cf7a1d357dfc843012` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/admin/api/client/data/UserManagement.scala | 5798 | `c6b24afa8f9b03384f743aac13673aaba411149cf50d7da490e2511fd1fcf536` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/admin/api/client/data/crypto/CryptoKeys.scala | 1215 | `6faa7b59414a6acbcbf4f0f2278258a9c05044259bb0d635cfc0f808d7f2fe05` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/admin/api/client/data/crypto/Encryption.scala | 2931 | `265bf4b37b633c7a3dae88c1fc110133044740f65e60b6a65c7503f97d361e11` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/admin/api/client/data/crypto/Hash.scala | 709 | `7de678b4defa0f58dc3afbb0994f9f81f934b32f46a54b075bddbc354c655ace` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/admin/api/client/data/crypto/Signing.scala | 2641 | `00febbf99d608efd491946af16f01646aae52e063faf8facbfe46d63108ddf00` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/admin/api/client/data/parties/GenerateExternalPartyTopology.scala | 2271 | `e823e3bb8f2cf8617ed912939a122fb21775a42f521e6c4d467b44e265517e83` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/admin/api/client/data/parties/PartyDetails.scala | 1574 | `5f1f772b1b03a0768ebca791b34631850415503465934ae521b3b601d0e7195b` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/admin/api/client/data/topology/Topology.scala | 18201 | `4b5132d8478e34129949e941d944cf4e9fb93af598f83ed9adac5f6b4ed04e95` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/config/CantonConfig.scala | 140312 | `286ba14ffa4a1a25fbf6b1d6887635ae4fdbcb1667368a93032075191828cdf0` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/config/CantonConfigDeprecations.scala | 10044 | `d43039f4698cbd9bb45a7b030ace8e358f9744bf3e822aebe18849189af0f3c9` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/config/ConfigErrors.scala | 6535 | `e9f4f3a493a459a6901c8d0db9851835222cae90656874db15512785727ed09d` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/config/ConfigValidations.scala | 49184 | `931792ee4a2ae4dc04476cb46061e12dfe3ee42ddb76dd8cf90d368ec80ebc62` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/console/AdminCommandRunner.scala | 4869 | `39c5256ad3d219e2b050615cba15be9fa3cdf56257d6903f64f006e24f5a0964` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/console/AmmoniteCacheLock.scala | 4696 | `90a1dea3145eb6f436d70e7e6c9d15be73e4a833c1b40906f859bb8544fbf962` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/console/AmmoniteConsoleConfig.scala | 3702 | `cbe970b082d851e1f4204ecb64b287b2667220a2e21b175a44b977b510b91366` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/console/BootstrapScriptException.scala | 371 | `d71057d66575f014a1cd724e5c2d0ba2f6cf64e6dfcb6fece8220af7d4a8abe4` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/console/CantonHealthAdministration.scala | 9128 | `c7decfbce88fb3339ce0c74fa08f199f269c6f854d02634db308767681886bd4` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/console/ConsoleCommandResult.scala | 6965 | `2555b2a682b7bd371579352438443700b8701c321ece85de7ecf5828714772e8` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/console/ConsoleEnvironment.scala | 27331 | `e19c029d32b31f239863f1498ec2738a463a4c0d81d93ac61ccc019f43b79d5e` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/console/ConsoleEnvironmentBinding.scala | 4653 | `d13eba9b2a1ce2102bd13f9ab7dba9bac7e7ee08cbad8f593266d28a2cdf39d1` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/console/ConsoleErrorHandler.scala | 1125 | `0dd64f6fee3a1aad8e0304fcade33a01316d29128d4c29d3ca1cf5572182056a` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/console/ConsoleMacros.scala | 50047 | `c0856144edbd6b11f92b830d81beb50aec44d9dab7ec6c4008d04c9c3c99ba11` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/console/ConsoleOutput.scala | 1093 | `438f0c1b715bc67ce7ca4f1be6dd45ce3fae399f7aab094234fecf54f3b34717` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/console/FeatureFlag.scala | 853 | `87d153301c85a12f66a3abcac4784948ddd50b18e25b30f05baef0e283e2a199` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/console/GrpcAdminCommandRunner.scala | 7112 | `e3174b92ad2645fe70d41d95781f7286b5ea65c17115b9d0f0ef73aed2767ed6` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/console/HealthDumpGenerator.scala | 8935 | `3517f5d367ddd01e83e390e8b37e70e55c2427e5cd107d200cfa40d7308e5a23` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/console/Help.scala | 14394 | `384e985d3c5d8bcab716e178c8071b018ec5609e44f8a382a68c7437f348b4ba` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/console/Helpful.scala | 965 | `cb0aec80331eab1096dd529851002fbe30204d8743bb00c291fa971059e7f63d` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/console/InstanceReference.scala | 62753 | `755193f09da8de6872ecee1b87185b6e91db59550acf871dd36f0ea41cc41685` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/console/InstancesExtensions.scala | 2894 | `dbf925f427b7ee605061ccc41a619abbd819d6c647d4cf000425b79183cd7e32` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/console/ParticipantReferencesExtensions.scala | 8546 | `266e91c85ddf7f8c80d76460d882bd21be579e7f534b3d54fc97d6894e19aafe` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/console/RepairMacros.scala | 16520 | `2fa7e25ce50720841963b3264e332dcf551472cd7ac6f66e0005ef4a5de23b2f` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/console/commands/ConsoleCommandGroup.scala | 1017 | `3438853ab1a58cd6137c05745f7d41a0c7b61c6e38d82968e385473ee2e5a80c` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/console/commands/ExternalPartiesTestingAdministration.scala | 28124 | `0ec741f4b5bab902939fba4d4c2a024da86cfc1cfc4fd0f815c3b1592ba1d1f7` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/console/commands/HealthAdministration.scala | 8279 | `a95796143b124ab72fb8e8595eb155beb7f8c0f2fee2a4e7634cc8683877eee8` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/console/commands/LedgerApiAdministration.scala | 179234 | `de243e123446d97212ea6cf2524aa936142c5e6b8ccec2887336b483561ec8fa` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/console/commands/MediatorAdministrationGroup.scala | 7744 | `aa3a81f326ffcca047152bc8300a706858f423a07af237b61d163dfb1b3f5d2f` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/console/commands/MediatorHealthAdministration.scala | 979 | `e5ce8d01b77c36760d02f4a794cd5aae50b2ad59ab57838dc3a9c5651eab2c71` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/console/commands/ParticipantAdministration.scala | 131526 | `f25bb98437bba54d573ded05f3883343584a2ed683c7545ffb2574e17e59db74` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/console/commands/ParticipantRepairAdministration.scala | 30812 | `50f1e0c9aa86434e663826439014ea67b2a480436ddf79a1c97443726e0f1a13` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/console/commands/ParticipantTrafficControlAdministrationGroup.scala | 1258 | `8a576335c04a588cc2145fb827b3611870d3b486b7d20326754cc4e01adb9626` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/console/commands/PartiesAdministration.scala | 48091 | `1be7d9065352b0f2516f1f2ae37cfae9710b4b1af414f9f4ff3a43a60923c173` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/console/commands/PruningSchedulerAdministration.scala | 5166 | `73a55e4a73e7b68962780e774cca10d5ab5fe87200a5497fb4a1df9d9cd360b6` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/console/commands/SequencerAdministration.scala | 14362 | `ea5bfc304cffc97dfc03971ea61a013d50761c94d16a950b43746369dab5e7af` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/console/commands/SequencerBftAdministration.scala | 4713 | `7a10581f4ef32e7a873522e3c11f5a60ef18ef2e0d1a91a6c9c3d73b01e321b3` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/console/commands/SequencerConnectionAdministration.scala | 4783 | `6f93cfc81dd4b51f79ab6cda43f88a29da4e0fea73fba79ab32f342287338589` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/console/commands/StreamingCommandHelper.scala | 1553 | `0ce05ba82a16c4bdab21ae15ed98b4cb72e8be89bde7b4ac9f0464da1f7e4068` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/console/commands/TopologyAdministrationGroup.scala | 198903 | `4e57734a593ee797bec359de3876d9235b35dcacc36f49f56beced61db9edf70` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/console/commands/TrafficControlSequencerAdministrationGroup.scala | 9849 | `829fd0c72532ba13a93f84a7ac069d5d585520c022facb1de73a227d5b1c3efc` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/console/commands/VaultAdministration.scala | 35150 | `371c1366a232a58ec732ae50aa765d648e91cf02c3d49c1baa01bbd671a15171` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/console/commands/package.scala | 3713 | `09a8dfd266d477c3c3b0fe3fef05d9af4026a73665750e43d4e6d40449cddd91` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/console/declarative/DeclarativeApi.scala | 17483 | `bca736fcd98f4b963fb268dfb500a2a64ca4de6898732a2fd8ece3df332ea978` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/console/declarative/DeclarativeApiManager.scala | 4797 | `ba51b11b118cf891c1e8418a562acafffeebc09780fdd6481d2514d79bb6a303` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/console/declarative/DeclarativeParticipantApi.scala | 43311 | `89f3b99e76099f8a90e573158d47cec21277967044791b362b1fbf600e0f13a8` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/console/declarative/DeclarativeSequencerApi.scala | 5063 | `f1c7a935426850e5f1c62e3f7c55464cd8361dae1dc842db482d43afb4a7b41c` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/console/package.scala | 1520 | `28c6e87aeb008a8da785a09a5482962d887dd073a030b8668230677286e0b507` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/environment/CommunityEnvironmentFactory.scala | 1035 | `c1384f2f3a5911f6d08615a6fb91b8d219a3a2ca35e9fe417c9f31f943a84788` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/environment/Environment.scala | 25434 | `8fb8fa96be9f55629e83251de191bce89198a1c759c830978376d008a5723050` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/environment/Nodes.scala | 16540 | `89274041276f0468a667ebb6369d0b6b6649d64f5b15b74fb9265a8f69b56cec` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/environment/package.scala | 317 | `c2cf24f661efcc4231228b4b6f98debc113dcfabeb2869a8da4c354025c9b8ff` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/metrics/CantonHistograms.scala | 1050 | `57e116c754454f1c98f25cafbb702029d9b6a41e907932071b01365da7919880` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/metrics/ClientCredentialsTokenProvider.scala | 5399 | `258937c2cb039546a977a1db76c10bb7b76eb52f7a78cda6d8256c2deba424dc` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/metrics/CsvReporter.scala | 5249 | `434706d7a2f978ef98d0fc8aa3318d6a47d3bec4fb72289624d78b7db441fd3c` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/metrics/FilteringMetricsReader.scala | 1604 | `ddf32e828b95d01f519b6a15a454992ba90eea637b73b1f3749aacb65564cb62` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/metrics/MetricsDocGenerator.scala | 2387 | `3f1b5a8f97fc20665680e7bd053c8a7d6d989fbb8d7e30426292854282f0accd` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/metrics/MetricsRegistry.scala | 12625 | `840a2288bb3d214f4285bcd8fe8b307ee828dc01343f4ae897d30f3b5fa05769` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/metrics/MetricsSnapshot.scala | 641 | `3c3b2cd63acdc38c31baa6aa52bba66037176d202914d321578dded59e8d527f` | 0 |
| community/app-base/src/main/scala/com/digitalasset/canton/metrics/OtlpReporter.scala | 6532 | `f0c3cd59f9d01e11b0c68813b2a8e37934dbd205e7b262c4f65c60deb23e1edf` | 0 |
| community/app/src/main/scala/com/digitalasset/canton/CantonAppDriver.scala | 15438 | `9a7f64597209f00bfb259d16caaf3ce68337e4ec15aa5c33145e71b80bb5d975` | 0 |
| community/app/src/main/scala/com/digitalasset/canton/CantonCommunityApp.scala | 1029 | `2ce9e1f7932a514180c33330e3a83108a3b578eaa4e2e6d580c601038f054352` | 0 |
| community/app/src/main/scala/com/digitalasset/canton/Runner.scala | 7504 | `5d0f142eb9c54e635848e8aa7d8b5c210979d6522ff0a415f7b4597e795c5642` | 0 |
| community/app/src/main/scala/com/digitalasset/canton/cli/Cli.scala | 21508 | `d8b4cd2f4d2c3a0d90cc124ad2fc5008c72d4d62d0d6440b4d36bc6d46ad73c9` | 0 |
| community/app/src/main/scala/com/digitalasset/canton/cli/Command.scala | 976 | `607eb3ce526dd09b3b9cc515e375645dee5f4d9df4ad6a773b4b1dd36b149187` | 0 |
| community/app/src/main/scala/com/digitalasset/canton/config/Generate.scala | 1461 | `3b238b2bf7f271f2631c847533157c39cfe15aa73b26ab26a9452c171672b885` | 0 |
| community/app/src/main/scala/com/digitalasset/canton/console/BindingsBridge.scala | 503 | `9f4ae2068629cb836a8b3a0e8c34f37b70a69772add1dfc23b5f094a100ace68` | 0 |
| community/app/src/main/scala/com/digitalasset/canton/console/HeadlessConsole.scala | 9193 | `5c2e8d70aabd9070986cdd9189ee000910c1d203c4aa456ca2c108ee0d9a6cd3` | 0 |
| community/app/src/main/scala/com/digitalasset/canton/console/InteractiveConsole.scala | 6843 | `13fb6db59eadca4bcc0bd2bc516e1e64079ea3edf9674e008959cb5c4867a24b` | 0 |
| community/aws-kms-driver/src/main/scala/com/digitalasset/canton/crypto/kms/driver/v1/aws/AwsKmsDriver.scala | 12314 | `499e97065740503dd4ec0bad46460fbfe40dd1a4dbadc728d0bfebf483c54b90` | 0 |
| community/base/src/main/java/com/google/common/util/concurrent/BurstyRateLimiterFactory.java | 2414 | `25c87ca10227c1af688f01bb9dd975c427f8658d47fad859058a935230edd8b2` | 0 |
| community/base/src/main/protobuf/com/digitalasset/canton/connection/v30/api_info.proto | 573 | `d5c196327af7428630ce7c071b5457eebe44ce7730a60aa94d1187c02f190267` | 0 |
| community/base/src/main/protobuf/com/digitalasset/canton/crypto/admin/v30/vault_service.proto | 8658 | `74000042528976f68b713afc042dfbd473deb065f82df10abf02206936ae93a6` | 0 |
| community/base/src/main/protobuf/com/digitalasset/canton/crypto/v30/crypto.proto | 12641 | `9d0903eb1b8188c3ddb5f1178ef86cd24e2d7aa5a25bf6cdb5ec19773a1334b1` | 0 |
| community/base/src/main/protobuf/com/digitalasset/canton/protocol/v30/acs_commitments.proto | 1603 | `4754c6cf8e9947954406e012f4e8337193f875b2af5d329247f07c2a225b54db` | 0 |
| community/base/src/main/protobuf/com/digitalasset/canton/protocol/v30/common.proto | 601 | `cd1d6a82d6d36d0503e30866d7890b7d676b65cf8900970fb838a77e7afab8b2` | 0 |
| community/base/src/main/protobuf/com/digitalasset/canton/protocol/v30/common_stable.proto | 1445 | `30c3be3efa8326106419093f8b7870c980e5f6fc9106d6b41834b0eed4fb6a42` | 0 |
| community/base/src/main/protobuf/com/digitalasset/canton/protocol/v30/confirmation_response.proto | 1476 | `e78c29b9bf03b461ec6e032f03cf2e9011d91edbd961d686a70634281fe9e37d` | 0 |
| community/base/src/main/protobuf/com/digitalasset/canton/protocol/v30/mediator.proto | 1840 | `342cca8aef04b38a9e3d051ec6487dff31deaac5bb528107cd619a5c96b74357` | 0 |
| community/base/src/main/protobuf/com/digitalasset/canton/protocol/v30/merkle.proto | 1082 | `6e0af58159bef854721cab0f3911379db5c357f585b05a2aa7d0daad51d4b7ae` | 0 |
| community/base/src/main/protobuf/com/digitalasset/canton/protocol/v30/ordering_request.proto | 526 | `14ff53cd21a5dc5912c0102fade38a8748ef7d7958f2b59e2bf0872cb665712f` | 0 |
| community/base/src/main/protobuf/com/digitalasset/canton/protocol/v30/participant_reassignment.proto | 4060 | `5bf98dfb8452659c174e86c0ea698f2b4ddd506cbdf2f2277d966e28c16162ed` | 0 |
| community/base/src/main/protobuf/com/digitalasset/canton/protocol/v30/participant_transaction.proto | 5144 | `89f2317cc819ba33c9c488fae0b86c9f4a61d6465ef9ff3a5b799391a3c9f06f` | 0 |
| community/base/src/main/protobuf/com/digitalasset/canton/protocol/v30/quorum.proto | 673 | `916722bc4052a6df5016767233e7b6bd1a13b11c13a998e688554a615f7793e6` | 0 |
| community/base/src/main/protobuf/com/digitalasset/canton/protocol/v30/sequencing.proto | 3085 | `8892dc3e3ea851a5ed009110c9ed1f03a72a9bc1b9f7cca6ab594bc7c3beac9e` | 0 |
| community/base/src/main/protobuf/com/digitalasset/canton/protocol/v30/sequencing_parameters.proto | 558 | `113e149722199ba4594139a0fafc79764d25c9537a5309aa0645f2a2d108635f` | 0 |
| community/base/src/main/protobuf/com/digitalasset/canton/protocol/v30/signed_content.proto | 622 | `200e7db17975736f2d623fb32072a3371a2c304547bdb694302f3d69000fa17a` | 0 |
| community/base/src/main/protobuf/com/digitalasset/canton/protocol/v30/storage.proto | 316 | `4a1631e305e55cfbbb80f304ddc72f5ea4f7555e54214ad2c185eea1ba808564` | 0 |
| community/base/src/main/protobuf/com/digitalasset/canton/protocol/v30/synchronization.proto | 1415 | `442076fb046be41f6f832307dc34c1dd47773c9cb9c99f2ebb25beef37adcf69` | 0 |
| community/base/src/main/protobuf/com/digitalasset/canton/protocol/v30/synchronizer_parameters.proto | 3310 | `6f283a7367ddf25efd564477fff56124e21a5ad980522074a36d0fd147014ca2` | 0 |
| community/base/src/main/protobuf/com/digitalasset/canton/protocol/v30/topology.proto | 21764 | `6f060f0a8e147a3d453118b8a897794bd1a2432740d85c85a1ff254c1c9f757b` | 0 |
| community/base/src/main/protobuf/com/digitalasset/canton/protocol/v30/traffic_control_parameters.proto | 4477 | `720d2aafb498452eb76406b1aa867c876af4891228f5627f7924079820616535` | 0 |
| community/base/src/main/protobuf/com/digitalasset/canton/protocol/v30/versioned_google_rpc_status.proto | 518 | `57ac37d71483ae13484c3172f2d746e4d7a27dced49bb25fe111f440c46d87fd` | 0 |
| community/base/src/main/protobuf/com/digitalasset/canton/protocol/v31/common.proto | 621 | `e8ef60afff3bab1354eed48d9cb12229efdd61e010ac6d19020ec40c69a79f7d` | 0 |
| community/base/src/main/protobuf/com/digitalasset/canton/protocol/v31/common_stable.proto | 315 | `ad50bc1e2fdbb19119a76b69eae6869fddf3b369e17a005ab252e676659c9df4` | 0 |
| community/base/src/main/protobuf/com/digitalasset/canton/protocol/v31/participant_reassignment.proto | 1920 | `cf149d9ca969d95eeb969cca0d981e0579c90758e5966608d8f1ec07c90b2470` | 0 |
| community/base/src/main/protobuf/com/digitalasset/canton/protocol/v31/participant_transaction.proto | 4150 | `b3cca3dce2927f40c2380a3b7de9e018dbfe38be2cd14f47155170c0ae562fb2` | 0 |
| community/base/src/main/protobuf/com/digitalasset/canton/protocol/v31/sequencing.proto | 3701 | `ec47288925bd611dcdcd44914ed631dcee5c42df767c02bb6d959a0e18178a4b` | 0 |
| community/base/src/main/protobuf/com/digitalasset/canton/protocol/v31/topology.proto | 6595 | `672b07645f7919f1355068f957053f468dbac5b32c9adb296aea76f6ac479688` | 0 |
| community/base/src/main/protobuf/com/digitalasset/canton/protocol/v32/acs_commitments.proto | 2579 | `800060c69b7adbc37d620d02be43983b76e9149fe389d38ff885c00a610123b2` | 0 |
| community/base/src/main/protobuf/com/digitalasset/canton/protocol/v32/participant_transaction.proto | 4793 | `e26821a0ca99f28be164cdc274b814404cf9ab1d0cc3cd2cc8fffa877322c9ad` | 0 |
| community/base/src/main/protobuf/com/digitalasset/canton/protocol/v32/sequencing.proto | 10689 | `a01e577db139613d32a45e773ddf7cf889c4e15a17922cef651ad533d1a7a06b` | 0 |
| community/base/src/main/protobuf/com/digitalasset/canton/protocol/v32/synchronization.proto | 2017 | `3bc89ae3b03408ecb5f3cee61513f7aa5df624282ffdbd1a08c21310ab4f326b` | 0 |
| community/base/src/main/protobuf/com/digitalasset/canton/protocol/v33/participant_transaction.proto | 1721 | `271b8f5d6ba6e159fa0fedd56b54b84c734770db58904326c2ca2a8eb989fdc0` | 0 |
| community/base/src/main/protobuf/com/digitalasset/canton/protocol/v33/sequencing.proto | 8751 | `0801d592d424dd3e431fd99672bd7da47409b86b4ca1d3914116c6655bafa9ad` | 0 |
| community/base/src/main/protobuf/com/digitalasset/canton/scalapb/package.proto | 1605 | `9d79af2cada718faa397c4595bcb8ff89070e87f0b4109e2263bafccd2311429` | 0 |
| community/base/src/main/protobuf/com/digitalasset/canton/sequencer/api/v30/sequencer_authentication_service.proto | 2296 | `df2feb98a8797cd440abaac39b642aa23bfc778539524f5d5f24749676eb43df` | 0 |
| community/base/src/main/protobuf/com/digitalasset/canton/sequencer/api/v30/sequencer_channel_service.proto | 6269 | `a90093d53756e6908c07153a0541b34df0b7cf6285f9f91e80de80f088cbac21` | 0 |
| community/base/src/main/protobuf/com/digitalasset/canton/sequencer/api/v30/sequencer_connect_service.proto | 2947 | `423c29628b66bf7f587a29bf2030b2ee9492597854b77e1c4808e7c0aae686e7` | 0 |
| community/base/src/main/protobuf/com/digitalasset/canton/sequencer/api/v30/sequencer_service.proto | 12462 | `f2a2856e3eb2200cdaf1908d2a6c9194d223628e0d82dd03ec73e3a524709143` | 0 |
| community/base/src/main/protobuf/com/digitalasset/canton/synchronizer/v30/synchronizer.proto | 712 | `fbf2134b9135bbe65e828af20f33e1d26c56adc430a084a00fef91f742c86ec6` | 0 |
| community/base/src/main/protobuf/com/digitalasset/canton/time/admin/v30/synchronizer_time_service.proto | 1460 | `c973f8a6c83f86cf30551bbe1c9d3b01aeee3587671a091caa820eaaf3bfe001` | 0 |
| community/base/src/main/protobuf/com/digitalasset/canton/topology/admin/v30/initialization_service.proto | 2018 | `2fdd170d02c37f4142e3cce6bb9c2dde95d99a2ffcd640f6d8c3ab38a227e1fe` | 0 |
| community/base/src/main/protobuf/com/digitalasset/canton/topology/admin/v30/topology_aggregation_service.proto | 4339 | `8b965bebc8f85b71ecd353b378e74a8cd1650c41929a0fbdc2871edf3b0d341d` | 0 |
| community/base/src/main/protobuf/com/digitalasset/canton/topology/admin/v30/topology_manager_read_service.proto | 13717 | `dde76c9ca82fc3a7102094254111b9d501490b771326a15a7a97c2be0c7de213` | 0 |
| community/base/src/main/protobuf/com/digitalasset/canton/topology/admin/v30/topology_manager_write_service.proto | 13235 | `b1b9d2d67f106a2ea60d60c3ec8edd0e302af27356825524aa9f688434a744a1` | 0 |
| community/base/src/main/protobuf/com/digitalasset/canton/v30/trace_context.proto | 333 | `54355345edff0304790263eef3ce7ed10ba923501b18ecf6c2e2314128bcaa9f` | 0 |
| community/base/src/main/protobuf/com/digitalasset/canton/version/v1/untyped_versioned_message.proto | 1149 | `46d7ceb34d69ad11d2ee7f42228578c69cdf553e5000dc9d43630873ddcbaeb6` | 0 |
| community/base/src/main/protobuf/google/rpc/package.proto | 284 | `b6af3b8ec48cfe191d6c5ba383f8c9d2a5a6cac67d46e8741817546f13239d7c` | 0 |
| community/base/src/main/scala/com/daml/nonempty/NonEmptyUtil.scala | 3021 | `a24183c493d576c142f635d2b02ccabc625fc7bfd2b01cb0e1229ef51bcd284a` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/ProtoDeserializationError.scala | 6464 | `9b37a240b0bb0aeba57324bf586e7fcdd25774fe6dd98ae3886324ef84ce16d4` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/ProtoSerDesUtils.scala | 2218 | `75c1672f002e0a6725f5a02ea37fba9f832bc4c3ee1109b173f0c5309aa80911` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/ProtoSerializationError.scala | 1202 | `411c7a4a5df520790aea715b2448b4b0e9b13cac418241f11f3d33cf29c6c875` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/Tags.scala | 6817 | `c17b53250fa8bd654f0d634df53a128bd252bdbd28b655c1f6e4077130f02bc6` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/auth/AsyncForwardingListener.scala | 1738 | `f156950a73677e48cbd897c1bb936783244a97ee7ac4854e4b27185f2ed32167` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/auth/AuthInterceptor.scala | 4405 | `36fc6be171419a7b41e4476cc64e4ec4d9812e5052ff46f01288f0032e2894b7` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/auth/AuthService.scala | 3105 | `f9ddcb9aac6b679cbd1ed02632019fc0a4dc713577fcf9d3000f8aa8753c358c` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/auth/AuthServiceJWT.scala | 9908 | `f81b5fbb5f1b99571949dfbc73ca8c9aefea53db7d6036c3d2f9b144bc777ae1` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/auth/AuthServiceWildcard.scala | 639 | `bfa0649e41e2dfeaa3132f4714125dea2cc1c7c3fb4c9c4a7cc831bc75eba107` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/auth/AuthorizationChecksErrors.scala | 5073 | `b546f24669a9462f5a7c7414ea9c31eeb9338794ce607d87a536172893e21242` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/auth/AuthorizationError.scala | 3690 | `cd9941b95bb7313621392387cb8bdbcd0c29007ff006c69c2c6c2fd31e0b66b1` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/auth/Authorizer.scala | 15739 | `414895bbbfda028fea2823deebea6c5d41a924ff97bfd2b382e5e67663d921d7` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/auth/CachedJwtVerifierLoader.scala | 5573 | `af99bdc402ab1d867854b7b291a8c36dbb1d78701509a52820bd57a360c4b64f` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/auth/CantonAdminTokenAuthService.scala | 2017 | `c3fdfff82342abc7017d645442f18addca23a40d2323de80dca05e99300da7ae` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/auth/CantonAdminTokenDispenser.scala | 2994 | `f5e7890686b9295a8a0120c23bc52e3a9a38e41571ebb4f3984dd9dbe5c10f65` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/auth/ClaimResolver.scala | 1420 | `5bff9280b081226b8d143425d8dac3a4e084b302b7254c369dbfba497f04d12b` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/auth/Claims.scala | 12442 | `70c4b38871a3db4d867069849a0dda2a3af08a55bd14cd4360cfdc9791e178f3` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/auth/GrpcAuthInterceptor.scala | 4457 | `27cea4e63d27b8b1ccaf3195d93c1f74cac6a4bab9eb0239a17ec420117da457` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/auth/GrpcAuthInterceptorFactory.scala | 1790 | `01c25375bae72089e75b3053fafbfc13c756c62c9dc12fde945916ab98646c3b` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/auth/IdentityProviderAwareAuthService.scala | 5188 | `7f63027991072678e059db836edf7a03ac47d41f47efe221d47397dc8c5cc3d6` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/auth/IdentityProviderConfigLoader.scala | 512 | `d98a503d3c9ef36b7a26ab60347b6a435c49226dc79906d0c04ac12c29c8342d` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/auth/JwksVerifier.scala | 4209 | `b9c0e5e5b5c9097fb6fd4e96c407709c508b5d53684a3c17f22eb70a4004a1d3` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/auth/JwtVerifierLoader.scala | 365 | `28e93b5e66ea2b8e1b557cdeb26b342a30e616c0858d2924e1c2982ae08c4ef4` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/auth/OngoingAuthorizationFactory.scala | 614 | `d272ee0a41e1cda6d3faa24231036c7986604f05e4324454df66b314a972d5d7` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/auth/TeaTokenAuthService.scala | 1639 | `662691b536763d2a42c478e9f4b49daa4f69a9e3232615ef6e77e77637ce00d4` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/auth/UninitializedPartyJWTAuthService.scala | 1131 | `e51118bdd40616f05c27d12df897fea0dabdaeda86f7bc33355406abe3fb7bf6` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/auth/UserBasedClaimResolver.scala | 6785 | `eed99b9a2556190640ff2bfbd4a9e10374d4374642dd614019bfac18c1fc6d48` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/caching/Cache.scala | 2854 | `4010840edec22ee09fd8e096d95c43345bc54a2c074e818ff393f610b805c536` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/caching/CaffeineCache.scala | 3064 | `a3bd8f64a0c0abaece39ff7f16494d345e28133f2e2138e20c202508811b86f8` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/caching/EffectTunnel.scala | 5407 | `c5695f589a1b513133ccc00aedf2f712a3ddc8177518469ccfbd940f9c3c6045` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/caching/MappedCache.scala | 1127 | `cf9bede9a069786cbfdfdb33e488396a8e3c32918cc73dcbd32f2c86049c17fb` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/caching/NoCache.scala | 922 | `41f39e46c41da6693ca23f554a44737d4aa3d12103bc1130cdcc3b07085b2c51` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/caching/ScaffeineCache.scala | 19175 | `fde2b29a08bf31e5ec3bc3a21f36bfdffc6d6196feead9cf5701cafc4aabca5d` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/caching/SizedCache.scala | 1501 | `9ae402fa5f4fae2ea5f51bbd4a61a42420eb5be7ebaada027fde16d8977527dc` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/caching/StatsCounterMetrics.scala | 1095 | `728ae83be4a9bf8ee547c8493caba207229eefbda35335ac2fe3990f2c0b84de` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/concurrent/ExecutionContextMonitor.scala | 4306 | `457eadf087034f5e2f35bcb5f44436ffa9790c1526c016e792782afd8aa7735b` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/concurrent/ExecutorServiceExtensions.scala | 1750 | `647c67a1d41946078ea73edee7a7edcd000aa682826f165441ba29ec0ae556dc` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/concurrent/FutureSupervisor.scala | 17720 | `b2b4e45805b9e7626e0bceba76d5655429bc0cee057d626463c0bddd38429f3e` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/concurrent/HasFutureSupervision.scala | 1219 | `cd191f620e10c0c165a32133db31e725de1cd9cfed217628e75785cdac7fc71b` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/concurrent/IdlenessExecutorService.scala | 3598 | `2608de901419d82fabfe2fd940054357cc322921f5ac3f130f85b2863b0074f3` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/concurrent/SupervisedPromise.scala | 1091 | `29542d0132c7bfe4f4d3b416f3723fecb7bead93166033e94d2ff53bf937a377` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/concurrent/Threading.scala | 12104 | `3ff91cca470819d73b8102f09159f835695286787eb5c8bb5c2f25b7f40f2f95` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/config/ApiLoggingConfig.scala | 2407 | `b2f76a3ba2c431d05d37aeae993b4453f6ec7fec5e640ef375a66196ecd7186a` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/config/AuthServiceConfig.scala | 10651 | `2dd21b076a3cd4b5ea30f4757f6104679fbb4551ab912c4d40dbefdc8a012b4c` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/config/BaseCantonConfig.scala | 3254 | `de824195043431507bc228983afa71d59bd08d92ead0fd70456990c10af6c097` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/config/BatchAggregatorConfig.scala | 2190 | `9c02fc2f02b507d9c5b4b72a03f9c5ae9c2dd4eb33fa62099facf2af58678385` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/config/CacheConfig.scala | 10878 | `35a5b8dfefd49b6381b9f66e032ead27e6d91aef6dc35a0f3bd7622ef1ea8a71` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/config/CantonRequireTypes.scala | 24013 | `9606e6987e572e90790a86003de7a32627dfc4025370a8ef326f12d4a682b2d4` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/config/CryptoConfig.scala | 3384 | `a6ac2e808abfd4f1d982c0937ebdc1b7a62eb46e19c532bf003c0cbdf1bc241c` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/config/CryptoParallelismConfig.scala | 981 | `ff16ac6c9035a264083892adb557af1bcc9712e4f08c8ed3cd685df683a723f1` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/config/CryptoProvider.scala | 7856 | `b12138d451dddeb4c15599d0a23f5e73f0eeb01c046df092995675f562aed131` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/config/DbLockConfig.scala | 5475 | `770829538a677b42639d48615bb8cafae4e563e70611e97c6138d7c12bdbd481` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/config/DeprecatedApiConfig.scala | 608 | `a4e5476a14bd573cedceb15b9a6eadc48878ced9917dd668b54c706ceb911ebd` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/config/EncryptedPrivateStoreConfig.scala | 989 | `a65f89c4a0c7c689824d8eca152d91b78958df896e28e6ef2c9c04afa6feddce` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/config/ExponentialBackoffConfig.scala | 620 | `cf222d185b5a870073284ab991841f651c4408601265f22e641a5ac6ab08c9bf` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/config/KmsConfig.scala | 5314 | `513f4afa389d31e16e1342d02e77dc909fd35147d331bcafb2bf63a94d9b110e` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/config/LoggingConfig.scala | 2375 | `d289b35ae9212125de3e1264ff877ba1f9a90218e95e7fa1d79ad439ac1d33f0` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/config/PackageMetadataViewConfig.scala | 1040 | `a6c961ac3058de6547d49789734169fa48d15935bc2b535e06ca894a7e8267dc` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/config/PrivateKeyStoreConfig.scala | 494 | `fb42f025a7bf1af0b104c003f64cf13c9dfdb04e096544c15a8799e9846a7821` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/config/ProcessingTimeouts.scala | 6098 | `39e4d46566621ec5d690c2b6ef1cf9b427ebc9c6cf343cd09ad1d6254ff11af6` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/config/QueryCostMonitoringConfig.scala | 1267 | `ffcea90ded0778ce5aec22309918bea3c75b6769950538441eaaf5b30e841e29` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/config/RateLimitersConfig.scala | 6235 | `d8279b999acc5efb084b0410f124106e5c0fb991b68142ece16f607d7cd14f9c` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/config/ReassignmentsConfig.scala | 1161 | `9377b3486cf9ed1c6d825e6f171406d4768c91b2d4612701ffe5d55629f2cfc4` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/config/RefinedNonNegativeDuration.scala | 20291 | `8a24629b47224fd8b848366a15d4e0ec13f32cf42857da0533a84ae598ba2701` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/config/ReplicationConfig.scala | 1584 | `4da64ff9d33dfedf42fd5ce6303ff9a89b8b1d7f9ec48ea3cdde1a113e1b40fe` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/config/ServerConfig.scala | 18716 | `340465a045ff4d2fc83e268d3201894e5f2bab36bdd6d7d44f687cfba2d8474b` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/config/SessionSigningKeysConfig.scala | 6872 | `a205de0638170ad32cb804b9a5edec4a08d783abd78c5bbbe7fcbf3a6d7753d4` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/config/StartupMemoryCheckConfig.scala | 585 | `2ffced7333092aa64dcf0a5387fdaea362a9ccb1517fd464d4c51dc3db649129` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/config/StorageConfig.scala | 26136 | `79f6089bdb10ec6cd0aa3c5ebea06697e9f8b401b25a3d1851d9e77907499b7d` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/config/SynchronizerTimeTrackerConfig.scala | 4777 | `3342adc52f649710bcb0751390e5e114aaef17512dfc72ffb1419b34802e777c` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/config/TestingConfigInternal.scala | 6390 | `eb393fc9963a8f1bb1a922f26bd0297d69be83b86427ff7f2d9cfaabf3757ef1` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/config/TimeProofRequestConfig.scala | 4112 | `4a7672ad7e5f2fc5e6660caf0a448da76f9238de4ec78e761f73db7f8bd286ad` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/config/TopologyConfig.scala | 4746 | `b4a8bc29ca0cd3acb378a050ad2b3d81ef054d7c0c57b59d8948f75ee905a358` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/config/TopologyConfigConverters.scala | 971 | `e3904e07b053c4097f895dc643724391fd6756014ec7267e90f4420d5dfe0217` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/config/WatchdogConfig.scala | 434 | `47d44d9d1e148df22c4f5661dad76fac428bc0028866d8cf2f6fff8814c284a0` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/connection/GrpcApiInfoService.scala | 580 | `d4f2b4f79122023903480045e5fe2b83a998d0b31af14f99aea46fc0a5f9003e` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/crypto/CryptoApi.scala | 25216 | `f40435a57ce4d9d83f354229050fdddf4b6a8209dff06d4fdcd0a64ba5bb24e8` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/crypto/CryptoKeyValidation.scala | 22385 | `123ea90ba30e948ac3927740e515763f116fb1c18928105930d6460ac2ef001c` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/crypto/CryptoKeys.scala | 21413 | `0f6f7eea442b371d366c92a533688a1a1149bfd40e9509a4b0efe61a714eb8e0` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/crypto/CryptoSchemes.scala | 11334 | `e82241e9e81224cd815e9266de52b1f1e7b1033eb13e08426f4c3df62ed6f245` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/crypto/Encryption.scala | 50876 | `55a762b644e475308d653a0704f2a0a275c71bad1dc12be888c7d5fd07474117` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/crypto/Hash.scala | 11245 | `671af97801e948c4b2067e96196daac7b487e2e6c0444c290905cda70c109fe3` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/crypto/HashBuilder.scala | 9845 | `6cbe300645481e3b542e86917a13747501da525ca7da289fd2ce7b8a0b6cc340` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/crypto/HashPurpose.scala | 7847 | `ccb8597a6c01c69449b27b27009c08a8d32d8a7a9cb2c1b30d3cc814051c9757` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/crypto/Hmac.scala | 6834 | `c5e4ccc88be99b00564429fda0cbc771194a98189349206c1813ca0e6e5762c3` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/crypto/InteractiveSubmission.scala | 10549 | `87e8b7fb3dbe7bd909ce2e5f6d43a6a93f3325d86bd6d43bbb8a5118a8c9db37` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/crypto/Jwks.scala | 3998 | `ba39131dabd1349a8c67c315b7055518718bb3ae70abaab3978e022756eb7d4f` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/crypto/MerkleHashTree.scala | 12888 | `347def6ce458d538cec693825ab12b732f41a253f13b7be158710ef2b58b52b2` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/crypto/Nonce.scala | 1545 | `3513c66755d1205db8f211fe46d6ca9a749885974198aa5f4486e9cd35724715` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/crypto/PasswordBasedEncryption.scala | 8330 | `8e3ab8634720665aca022c6e2211e54e2147cc427afc2ca49b7e444326e4d104` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/crypto/Random.scala | 2730 | `d7c3c1023b94c12367f62d1c1be8db51c1750fdb6e72bf17350197e16c718de1` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/crypto/Salt.scala | 6167 | `789d25cae700ddbd8708e1107ad8d87f0888bc3f8da03c146d949ea3b1ccd07e` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/crypto/Signing.scala | 98506 | `c2d2469fb6a072e43d2f23e38c36511b824982bd608944f643d43071f13a7c23` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/crypto/SyncCryptoApiParticipantProvider.scala | 23212 | `e7cc9c263a21dfdc764d596d9ce800c210c5ba9557aa26da0fe2dc09e28dc96f` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/crypto/SynchronizerCryptoPrivateApi.scala | 3427 | `5bf8ce4c7c9c2c7416448abeaa2b4d60134e6b43df0250545927eb0e1c260e1e` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/crypto/SynchronizerCryptoPureApi.scala | 6654 | `3f36e2caff896293c576e5a435667fc8763c1e5629cc306b4d3ced0330765124` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/crypto/SynchronizerCryptoValidation.scala | 4744 | `3037368079bd776cf093a181d9b3d099de21a21f5bced9f8e18b10981bf0ac64` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/crypto/X509CertificatePem.scala | 1934 | `d265cea750a7b5878f602f1c3da3ef68efb68a72e0f9bc89c7f6bdb756421158` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/crypto/deterministic/encryption/SP800HashDRBGSecureRandom.scala | 6693 | `e55c88e1c1bcd76d8ffd118d36ce13ecbf73000e39f4816d340b543d9a58260c` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/crypto/kms/Kms.scala | 29394 | `36b7f46f9d0042e1e148efe8d0e4f8cabb6cce59a41826377509f6c992ea42c1` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/crypto/kms/KmsFactory.scala | 1597 | `9221d17ba92424e102251f43676876e2a939a55c1b3d358b6c248be260572268` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/crypto/kms/audit/KmsRequestResponseLogger.scala | 3313 | `9feed6b93e81ae391df34811aadad388f2fff18317c3bcb6cf93771fc20a3dcd` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/crypto/kms/aws/AwsKms.scala | 27358 | `52e59d96394aa4f3b26cd1b2cbc0bd72a4ba5c044bd37a0bfad8a9c41bded07f` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/crypto/kms/aws/audit/AwsRequestResponseLogger.scala | 7571 | `038046ff2cce8a182f08e6e8b1c9694ac5f8ca7131c6d97fc3006396253a1983` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/crypto/kms/aws/tracing/AwsTraceContextInterceptor.scala | 2707 | `0add85541828b407903c0cef16cbf25f42f613ea545ff922425818d3c52de4a1` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/crypto/kms/driver/v1/DriverKms.scala | 18925 | `aa59c87e797cde8b6fb6b9b0212035c7f2e922ef713a8b843426bb9a1b6f5dae` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/crypto/kms/driver/v1/KmsDriverSpecsConverter.scala | 3498 | `f7464626f332496d657d0843e905c9813729fa230e2b5deab8cd736a2bd4880f` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/crypto/kms/gcp/GcpKms.scala | 29942 | `d41286f12faaf40b37f4124df583192811a457f81db74e02c911b5058783b8aa` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/crypto/kms/gcp/audit/GcpRequestResponseLogger.scala | 2079 | `a164766d7a6563dd2302e47cbc691ae42ec93dc3cb15e027f6bf84ef2c22c3b5` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/crypto/provider/jce/JceCrypto.scala | 2436 | `026705947cad148ef1d752cca15596e636baa339becaeb2a5a4061f41f098767` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/crypto/provider/jce/JceJavaKeyConverter.scala | 5983 | `2249a1df078a8d58205e878b25769ba87c27888a7a7380f1bc23ae6148950a2c` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/crypto/provider/jce/JceJwks.scala | 6797 | `70bdb17864b880136d19686b75e05b028cc86fdc664f7a517d8a54fa1ca4ce37` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/crypto/provider/jce/JcePrivateCrypto.scala | 18539 | `424a9ce2d0e397b2f14ec8fb2175ba87db0245fd9623c7c1b5a116245cba06b0` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/crypto/provider/jce/JcePureCrypto.scala | 37101 | `c24242d4558c8a51147f46bca132c4ba4ef5b142cf81ed18ec1727549d986db4` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/crypto/provider/jce/JceSecurityProvider.scala | 699 | `33fa3cb44496a460e1715e601b3c2df56af1cdc0326e7df13798d955b8fd0b70` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/crypto/provider/kms/KmsPrivateCrypto.scala | 13397 | `6880f559be80b7a92aac5554fc9a4f7af367546e7be39e68a1e6ac6e42d3bbb0` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/crypto/signer/SyncCryptoSigner.scala | 7677 | `c613d23ec0482b70d3599850d0efdf7195d7ab086dc756cad194b85e04273892` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/crypto/signer/SyncCryptoSignerWithLongTermKeys.scala | 2100 | `b82dca5ceac0c8fa67b37287f2afeb9d8699e18d00e00e2f1d6e4795ba1ea3a9` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/crypto/signer/SyncCryptoSignerWithSessionKeys.scala | 32002 | `38e85e7d9c5ef582f333b2b8e71f90cdb4752f8d3d842006687acb1220662a14` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/crypto/store/CryptoPrivateStore.scala | 11179 | `fedd6c98fcf3b62958cd80b299e2e74da66e2d7ad57445c91d817c6ffe79bf29` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/crypto/store/CryptoPrivateStoreExtended.scala | 21679 | `3878b2ac87fe1f28cdc446954a89a39da971a8710e5565b2492e8fa76cbbd1e1` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/crypto/store/CryptoPublicStore.scala | 15658 | `80620704a368499c4749066e5878a33b1ca0dbcb33d58fc025767c6af7a5e062` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/crypto/store/EncryptedCryptoPrivateStore.scala | 20560 | `fbb3e0bffc51de87455be8fd4b64e9aa0898cd207aec1e804caa5ef9a8ac9d08` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/crypto/store/EncryptedCryptoPrivateStoreHelper.scala | 4047 | `8c9c93611fc3009df5dca460a9c873c6ae1350dcec374cd79a2a8df423949c6d` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/crypto/store/KmsCryptoPrivateStore.scala | 6240 | `963ded3048e3901dc0393c6ebd9d07687fe92cc8b6dd2f142f6e6d2cd900bdcd` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/crypto/store/KmsMetadataStore.scala | 2904 | `86fe42b09a27aabd689daf99683bd62e9e19a0eb013127e03f040c578518f1cb` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/crypto/store/db/DbCryptoPrivateStore.scala | 10662 | `11c5aec79317412b22a8051c7e968b476e7d17db99f472e8b7237cd37b2823b3` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/crypto/store/db/DbCryptoPublicStore.scala | 6813 | `05e9dac3c1d491bd11914f50dd4e62f426e45b7ef08cbb0abff885d5add9cf93` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/crypto/store/db/DbKmsMetadataStore.scala | 5492 | `7b50854a35529017171d35775082a5ccb80d936eb933d1427efc417c6b81652a` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/crypto/store/memory/InMemoryCryptoPrivateStore.scala | 8686 | `ce4adf1c297c4fc5599b6454f2c1042ea07297115fb876a12365b4f213250983` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/crypto/store/memory/InMemoryCryptoPublicStore.scala | 5025 | `341cf7dba7266bbbb34270c9c7a78b5637c21c6df294d3c9adac1044509e11e0` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/crypto/store/memory/InMemoryKmsMetadataStore.scala | 2809 | `4e75c7ba718a21b89db878dc3f3f8d662d94db47edb71e1557dee88593e244ae` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/crypto/topology/TopologyStateHash.scala | 2530 | `0d6a3e94715767ed79ff0876a49b68fbe0dbaa62043819f76c576ab1005c800d` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/crypto/verifier/SyncCryptoVerifier.scala | 25280 | `b929ae42b082116661212d30ab6784c8f9422e6a1b0cc42ffe271584e7caae5a` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/data/ActionDescription.scala | 18707 | `d17812e5463601f855b0de35419bed1ac92f8ed0637b695b32eab572275959c1` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/data/AssignmentViewTree.scala | 19705 | `ffb7ce2304564db0a327b6ef7071ad8dea0f60cac1d328dbe6a65ff5e1a4cb4e` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/data/CantonTimestamp.scala | 8438 | `1ac5a7e906329e6a2d43431a6559490fe10ba4cd6ad79e5aec797de03566b521` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/data/CantonTimestampSecond.scala | 6078 | `30f31a74b7e8a7a4a463dcddd9eb918959c59d07a6466f34b2287c1906e5df0b` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/data/CommonMetadata.scala | 4678 | `2f581a02bd5982e8814cc0f6570b3e4619c47ab30e19d1d793a0d2d95d1a0377` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/data/ContractsReassignmentBatch.scala | 5709 | `71d3f6544e266ffe3484eb379653ce46b175d98bbb23782fa2ce4c06dac781d7` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/data/Counter.scala | 2741 | `d1f1f5fc4374ce9df0da12918486fda898daaa31b07ddeb60f622ce91ac96565` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/data/DeduplicationPeriod.scala | 2930 | `9d3776f2e2da3e2c69f71a848f6d2a3fbf0e373dc9ba9c730f1e81f85ebc0ce6` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/data/ExternalCallKey.scala | 1727 | `7fa6d48725fe87347a5a827ab0814434eade0f43fa4650b735dcb6d8fc20db6d` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/data/ExternalCallPayloadDescription.scala | 783 | `b8243e6f788bb085b3677f9422f35cdfa2ae5b2d70c993c81ef9852a6ecab1b9` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/data/ExternalCallReplayData.scala | 2719 | `8fe04ed9e9ff621014d81e3c690ec2d70c217441f713eed65a0d76d480c54169` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/data/FullInformeeTree.scala | 7858 | `0c0902257d872091ecbbedd6ce2b8921b6e8de75efcd558de5d5cd8b62f5785a` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/data/FullTransactionViewTree.scala | 2971 | `2c4c410f11e56bd67a550c2e994b886b384102232b0c83e93a922a1691e205d6` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/data/GenReassignmentViewTree.scala | 3302 | `08d8de0ae1ef24ec5cab803a632484966d25cc54ad343f6589fa24a3704c5675` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/data/GenTransactionTree.scala | 16108 | `c1ae93d1281032743abf1a8af2a4ea4b84e54d4683ec406ae54699a1ee991067` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/data/HasSubmissionTrackerData.scala | 1257 | `37f87b7701d349099118dcd48fad1bb0190085fab2a2164d2be59f2ea7da8da8` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/data/KeyResolutionWithMaintainers.scala | 2936 | `820c01e60233f6ab946ebdf4fbf5cf8e5a9e5bbd4df7889cb09559ef894b2dfa` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/data/LedgerTimeBoundaries.scala | 1035 | `e4963a4a330f5f55035f40ef3ee7d54ea58cddd65eed3444fa454cb1c11e686d` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/data/LegacyAcsCommitmentData.scala | 1958 | `9ea56be1b0ce456e276918ac3951762a3ea6492a9930f150dae00042c6d72e39` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/data/LegacyKeyResolution.scala | 3396 | `d908daba97687350e43cb982480b6f44e863b83485c987e2edc3e9c1c130be0c` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/data/LightTransactionViewTree.scala | 22326 | `f6dfa1c5ab573162c958821ababc656854bc004f5aba3eb71516145803baf2fd` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/data/LogicalSynchronizerUpgrade.scala | 5957 | `3f95109ed149cafeafecf57d68868038ab0da1533144bf8679b06a6f64d39dfd` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/data/MerkleSeq.scala | 27585 | `7463729b4627217f926a2fc1932a0e5af90a4015fcc8078dfcf8ff1535df7b99` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/data/MerkleTree.scala | 11187 | `35d9b4c16d91d90c178abc7ec0ffccd0041aad753b2f9392c80c37bea6379f16` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/data/Offset.scala | 2714 | `0d60693f295a2eb386550a21901d2905c81cf709b725da83926d975fe29454d1` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/data/OnboardingTransactions.scala | 1566 | `7c6321aa9386136e1b57af00eb389fa498eaf57289e57849d62f8f650c889a35` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/data/ParticipantMetadata.scala | 4515 | `519deab018f3f02cebce0e23d71a1ecb7893e94dcdbde804fb54d9ea182a3780` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/data/ParticipantTransactionView.scala | 1571 | `fb9d81fbed363119ab8f91359353aae5f1f4de03185f147a8df34cb63230d1d5` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/data/PeanoQueue.scala | 4931 | `4070025d2d1dd88a5b158713199eb69936c4f553511daa772317ccdb18f28119` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/data/PeanoTreeQueue.scala | 4866 | `fb5c1d342322857ddf4ed3ad84527422b22fa72d73c754f9061632d4ca65178c` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/data/Quorum.scala | 3572 | `10000f870a34bfecbd5e8893c777ecaf7bf5ce9ec8677f824faf4fff53ae20c7` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/data/ReassignmentRef.scala | 1062 | `78c95f3d6f0a6eb87b3aad6379fb98c9bb49a8a3734723d9e2e9085f1229a268` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/data/ReassignmentSubmitterMetadata.scala | 3845 | `989ed88e67396865ff839880df14cf226aa1eb019ef953d3ddee072746d47121` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/data/ReassignmentViewTree.scala | 1714 | `d68c3239f7f8fdfc514a9b9fba6e55a667a01d4673e9869d46793785d5f888d5` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/data/SubmitterMetadata.scala | 10803 | `cfa4ff97640d1ff6e0d7e262174be9dc07bf0bf16f0f8cec74d777880f56b1ac` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/data/Timestamp.scala | 2098 | `a307eee024f41a26aa715a6df9b91535ee583a83e6fcd28286b47476cfecc792` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/data/TransactionSubviews.scala | 6935 | `59c9877ce8d4a36d11a5ee092ae4ad7cf489321151a73d8f42777899e3fd4839` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/data/TransactionView.scala | 26036 | `376d69c707efe3c753d530d4b8d7b55892515018fab0af60fde2084b7b7ec985` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/data/TransactionViewTree.scala | 4095 | `069e6fa96db6cfd5cdb9b03f458a7f13c0886e47add49ad3ce516fb264273de3` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/data/UnassignmentData.scala | 13705 | `8ef12d734662456fb6829fda976dc1e0ddb0f43095fefa403308b88a74b80603` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/data/UnassignmentViewTree.scala | 19719 | `72aff0173870925b6ab51395f7fa8b875cddfe3acc9f70942f6be3305d503627` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/data/ViewCommonData.scala | 11029 | `3a5f7026ab3c222606b4a8c60e1be98c8f0183eb1a636e6d72705473a53ec67a` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/data/ViewParticipantData.scala | 27214 | `6e9cfe1f0fc63263fb822740553aa439e106cf2555ee03be864b6b7d974cb8d0` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/data/ViewPosition.scala | 7992 | `efb068e98d4a39cc3ad73f57ca3b29188b49f275961b2271f27aaf9a6db88603` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/data/ViewReference.scala | 2442 | `0c6b49aae35ea1e96ce6280978fea260a192c811db9470eea2ecfcefb779f8cf` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/data/ViewTree.scala | 2978 | `30952443d12e454fe2031fb41fc214b69d3acd487c6927215a052e6b286c5452` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/data/ViewType.scala | 3240 | `1d48e6a01173c7f9899b00f016be132379636aa60b91f007af02aabe5978a8c7` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/data/Witnesses.scala | 3504 | `6c17cd3eae2e47e4c34016d1cbfa5bebd9897ec72edca8488d00cd0df3c09e62` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/driver/v1/DriverLoader.scala | 3833 | `120d615cd10c7b25926b9286f665d2e4d95182ce353b135651c6a5adb00feeb5` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/environment/CantonNodeParameters.scala | 4908 | `5c3a5da182e009fc484e82d4e0a41c49b39ef5059ed88bfe3de62558fdc80ad4` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/error/CantonBaseError.scala | 10533 | `ff1cb2a31535226b3312588e5495792a6b284c45ee24192cb186a86b0e528589` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/error/CantonErrorGroups.scala | 2976 | `81d6350ec73adf1ddb3d2f4dc8b184dd4dcd7c17604468dc885dc734f5f59a5b` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/error/FatalError.scala | 1889 | `9bbc8dfc6b1fc224a77bc6fa6a2170e730ef6d7ac5d742668fa76b62f88b79b1` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/error/LsuError.scala | 4692 | `8d4457fbd46ef295f1cbe0e70dc1dfe2b2746801be4bf61074bba5f4492e6180` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/error/MediatorError.scala | 6837 | `a539a29be800c342c86a3d90128109216a4d73cc697f2b3995e3181ef0f00677` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/error/TransactionError.scala | 1530 | `2d00bffcef7fcc98bed8e7ff1049ef6461ef386aa372f1eeefe98acf73894e4f` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/error/TransactionRoutingError.scala | 23474 | `ad41710bf52915231b3afb6bc0a57215b24a3e0e30919999454cd084fc021ec3` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/grpc/ByteStringStreamObserver.scala | 2969 | `f452a47e2be802e94d853358a1a960396039658d6b5ca13ab8774d68f189065e` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/grpc/OutputFileStreamObserver.scala | 1522 | `4f87eeb2ff9bd4614ba41cc74a92e787666cb9a6f435fa582c4911354c315873` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/health/AtomicHealthElement.scala | 2566 | `64259ea7cf4b5748e0b7b9a87dabd845b442e2c8daf2f4b02aee034faff6e5f4` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/health/CloseableHealthElement.scala | 1131 | `ff4e1706008ce0014bbd84779fd5764cc08caae30b37e56cff8a859dba32b24a` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/health/ComponentHealthState.scala | 7687 | `51461f0dc82f57d475abf104d734fe2ce5052f6009bd4e7c78df0d5bdcf680a9` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/health/ComponentStatus.scala | 5739 | `a8b38b108340331d7cf0ff17a896e411e8528e2d6b472df0339f08076aff2d15` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/health/CompositeHealthElement.scala | 4913 | `56dda0df92785b07efaa7a915468ee95990acac6a719e2dee2f0a0368312efc7` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/health/DependenciesHealthService.scala | 4030 | `36ff616a1657ec1175eb57d964b3e2ae8be7ac620e19ea544683ec6ef4588e34` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/health/HealthChecks.scala | 900 | `66927dd37abe4bc93a8ded3a1a7605d451df435ee387429ebe31f8a90435e1b7` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/health/HealthComponent.scala | 1937 | `52d6fb8b7367bbe25fefcad37c44355a85f7036404d61a682c2e43ad1f917bf7` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/health/HealthElement.scala | 12189 | `d4e2d11499e7782e1d728c206a34b9322d8cd22d0e5c15c5d3990608405b2d04` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/health/HealthListener.scala | 1501 | `58aabad079172036a73f9102598360da89996600933c29cac01fa974ec2a10cb` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/health/HealthStatus.scala | 1151 | `210eff1f6464531fba1dccbe3f5d3a9fed42720ae01ee0796f79d5b07d9b39fb` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/health/LivenessHealthService.scala | 2792 | `a47b4e707fb5b50d9f954c648a015e5c687e3cf005b2d7564e306ff632d38b26` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/health/MutableHealthComponent.scala | 4360 | `a3b6e78205cc5290a9ebf23d511c58f264760ecb368674e13dccd1d8c82537ce` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/health/ReportsHealth.scala | 334 | `360b132f8f56efcac3c82834a6db0ee6a93a00f0f4392b4aa18881cf5cf0dd8d` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/health/ServiceHealthStatusManager.scala | 545 | `426de857a6881d692cfe9787b70240157a66414076a64c746ceb7e25169c6da4` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/health/ToComponentHealthState.scala | 353 | `ed7d37d0a43ab63cfab1cc0809ba7004ad6d35ca86d8c23b28776156ff8021f0` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/lifecycle/CanAbortDueToShutdown.scala | 2799 | `2b2ffa972fe91696d6621deece00f800f3f6ff8057fe148b1c4e740edd0d50d6` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/lifecycle/FlagCloseable.scala | 6495 | `624fa8efee159fe0b66a0cff86230414049b1fc531e697605047195e6221c468` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/lifecycle/FlagCloseableAsync.scala | 2419 | `6fe6f87d6e886ec37911f9ac51198fc6ad3a73df0bffc005d43a375c73cd535d` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/lifecycle/FutureUnlessShutdown.scala | 23023 | `6be031a3b892d84aba6305b0d56f3da3f65220edb06e196fc98e9b548a793eec` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/lifecycle/HasLifeCycleScope.scala | 9256 | `49c51cd73666777c79c5825e1db4ba9245bcd77992d66395494656995ea5da5a` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/lifecycle/HasRunOnClosing.scala | 2161 | `5ee8fe5bfdb03d278d1ecb3181898e408ea5585b6c56d9e10c79aa036b3f4dc3` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/lifecycle/HasSynchronizeWithClosing.scala | 3929 | `3dc12fa210ed73283bcb4cd4282d9d45dc1cbf01fe5d931e7a2893c1587ac1d2` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/lifecycle/HasSynchronizeWithReaders.scala | 8145 | `6bf2c6a51c1df7b3653018804179079e3c8f602374b877ded2cfd3c1e1f78d54` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/lifecycle/HasUnlessClosing.scala | 948 | `1a724a2db77ee64398e9b521d128217a511b0e51b97e188822b852a2e7c01352` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/lifecycle/LifeCycle.scala | 8281 | `6f92290eedd0811888174620a880ec98f3fff5e9cb7539558b3230f33702f609` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/lifecycle/LifeCycleManager.scala | 30320 | `42326a1761fecdf670d11753aa8d7a557d4e465301f491fe234898847bfc0342` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/lifecycle/LifeCycleScope.scala | 15513 | `3d35ff94187dc6ff5ba7c40df3f0b36df99bd441c864d375e7752ade132e4d43` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/lifecycle/OnShutdownRunner.scala | 2957 | `de57efed05285eb44643caef9f4868eca3cb9c3317138d2a38b802c64ebb0a54` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/lifecycle/PerformUnlessClosing.scala | 2802 | `6628cd515ac0d5e7b400292a9c4761901df8101900c412f172d68763f2bf8c9a` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/lifecycle/PromiseUnlessShutdown.scala | 8774 | `4d78844d5bb884b6408df0d0089407a32b23e45f9cf3f0a2b67b6d35ff9659fc` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/lifecycle/ShutdownFailedException.scala | 422 | `437668c7cb4bd3ef9648de620612727887179b02612664e11d182f9757d1d297` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/lifecycle/UnlessShutdown.scala | 7768 | `0921b88507359b06b75d341ba84d054d9d83c309a15be6437ff30b7dd2821372` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/lifecycle/package.scala | 836 | `2ba2efcfac976c45ef237c509a9cd34f3a2c4288a62036b0e099e3cead07c21b` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/logging/audit/ApiRequestLogger.scala | 5517 | `6100e84b35cf01d619650b928ace15693035f6237eedb7abcf77cc46f3016b31` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/logging/pretty/AnsiEscapeFix.scala | 1813 | `64f4db2ee73f8d3643e74fd605d0582dda4a97e6cf2188d4e1766768bd9e39b7` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/logging/pretty/CantonPrettyPrinter.scala | 2366 | `c70cfc918a4fc59f9e1ebc2ac73ef15f1c8055a05315d204578c2bf79a062170` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/logging/pretty/Pretty.scala | 2482 | `545ffedcc7bbe0257257abeff13fda48466170830bd71c3b308037a1ffe30a89` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/logging/pretty/PrettyInstances.scala | 13177 | `202a4b844674dbad878a173ee8c4fb15dd3197ff5b064f7cf92b1dd18f899004` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/logging/pretty/PrettyPrinting.scala | 2878 | `cb7908acbb8e5564768e544b9c1ffd6dc585b541fe7ad7fdec7f149ffa21d83c` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/logging/pretty/PrettyUtil.scala | 9081 | `50b2ae076e7ab22e9ed324fedb37e7fadbf27e7b2fa66997e1d042e9666c8119` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/metrics/ActiveRequestsMetrics.scala | 2974 | `08ab7947ad6986dfd29480ab1975abe2dd9e884e16e79339ee89c91ed0738724` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/metrics/CryptoMetrics.scala | 626 | `c555b286b340194975931757956cce5bc5a510ce4b65ade0e9c3ff55c5f070e7` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/metrics/DbStorageMetrics.scala | 4013 | `25eb08f3b75bd948ac8b87960efccd14996b84ee2def64d6f5871756397486e6` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/metrics/DeclarativeApiMetrics.scala | 1428 | `75f67fc404df4954be6f028934339acef750317d24764c8ae5b40056e968f2fd` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/metrics/DecryptionMetrics.scala | 1109 | `71569e256c2815546b88eb787aea42fcb827818557d398b6d762239387f3ddfc` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/metrics/KmsMetrics.scala | 1182 | `6db1a4058d63034a288e670e8ac7232d7b7d408dc8e46e6ec8563e430be18921` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/metrics/LogReporter.scala | 1429 | `aef0aa09d21893becedc87dfa14358b1d51dafb1901fca9a23a41fe7c24fd430` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/metrics/MetricValue.scala | 8537 | `b6557c622234f1c19e0dd946815cc8e4249a4c2a403e136bcc7c5e34a784271d` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/metrics/MetricsFactoryType.scala | 762 | `1d0ca2c7c0733b58fa0ac2fc6c9b19b0ba544f31cafc9b828529fd90d4c5cd8b` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/metrics/RateLimitMetrics.scala | 2807 | `f47ba81f15e69a29c3d85dcdde8de6e4d4116358fc1ca1f6665ca72a94b16729` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/metrics/SequencerClientMetrics.scala | 18209 | `b71c5b8919413c4d66cc41548ba02191a44db56c76b2eee06c5bd4b49d0229a6` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/metrics/SequencerConnectionPoolMetrics.scala | 9635 | `c683b4d2cb7a4e48d303413659827e5e74f239f776967d68c268087b49581776` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/metrics/SigningMetrics.scala | 1091 | `b371c458f9fdcaa86b2a92aaad4042bdf4ea8ff172fed6d5ed9b226c104f4da9` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/metrics/TrafficConsumptionMetrics.scala | 7613 | `1361d2af1d042a673c9b7e946670c9226f77136068f207ffa09077355318da41` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/metrics/TransactionViewMetrics.scala | 1398 | `543f90e11581ff7e5917f2a8aeaadb55e5243ca7776b38a0dfbcae22ec4ab2a9` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/networking/Endpoint.scala | 2885 | `b9f312a9d13ea6c393e9aec5b0aca10b37e07de8035388a99a213668215b956f` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/networking/UrlValidator.scala | 1149 | `6b8ccf83ec0ce8bb52aef6ed6b2fae273685d4e9f3410d9060205b763c213888` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/networking/grpc/CantonCommunityServerInterceptors.scala | 3095 | `d6b6a67d23caac42cd8b7863e8846060d06fbe139dae3da878ab62850ffbfdd4` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/networking/grpc/CantonGrpcUtil.scala | 20934 | `7b3574db20437cf2e4e512c4e3f8aa037cb80e30c124c0f4e6da422f6136a40d` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/networking/grpc/CantonServerBuilder.scala | 8274 | `e7e4b762ffb03589e776bb54e5379904bb2d38b12a541ea5474732d0f84b081f` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/networking/grpc/ClientChannelBuilder.scala | 9840 | `bf348369f5d1a43e4ba116f864fb20d7d78ef01c5c2ecbf195dc6eef36ccc308` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/networking/grpc/GrpcClient.scala | 791 | `513d5892c39781901ef48df7f5196ac2d7381511fe7b00ef4364a328e979996f` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/networking/grpc/GrpcError.scala | 9854 | `85c1f17055c57d4c16c251bf1d9c538fc1774a67914f4ae290bd91f13fbef727` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/networking/grpc/GrpcManagedChannel.scala | 1714 | `cc22b52055583e0904c71876e28e299a930ac9839e60daadf565fef5052704c2` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/networking/grpc/GrpcRequestLoggingInterceptor.scala | 13853 | `2efb9984c7e1bccb47a123f4398ab0ff255c2f2c504fc083fc0b2d4be6129614` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/networking/grpc/ManagedChannelBuilderProxy.scala | 1075 | `3c9ab667c20de721b4b9ca890d778b1e283d724e6281a40a17bdadd95ef6fb7c` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/networking/grpc/ratelimiting/ActiveRequestCounterInterceptor.scala | 10715 | `bc612bb4e25912dd6cede2f0eb57870899fd8d0beed07c5746234ac63c0fc9d2` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/networking/grpc/ratelimiting/IpCidr.scala | 4583 | `30a04b734aeb35bf111cf6a62e0c875daa57a81026a979d3b20cf4e6f59f1c4a` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/networking/grpc/ratelimiting/IpCidrRateLimits.scala | 1768 | `f42baa2c569716bdeda42e70e1a38187061e53d90c0b55bc50df3d38e5d3b625` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/networking/grpc/ratelimiting/LimitResult.scala | 1316 | `4e9c937a466ca9d2452a49f5785c8619f81c5493062b0095c4584f06e2ba915a` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/networking/grpc/ratelimiting/PerAttributeRateLimiter.scala | 5476 | `31c7ac19c9fba7e38c3e1cf0e852a45ea78ebbadefc20bf3f300dcc8fdb4970c` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/networking/grpc/ratelimiting/RateLimitingInterceptor.scala | 1741 | `cead9940496dbe9124355a142c665286b380483e20834410ee6b598ecaa0bb07` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/networking/grpc/ratelimiting/TokenBucketRateLimiter.scala | 3466 | `4b647b2823ddc9ac449891900b750983f99694e581feeb908b78dda22e2a0fcc` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/package.scala | 6444 | `51375a38666dfa195e13c1a81730d0dec80862f67209ceecd4caadf74457a0d1` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/pekkostreams/dispatcher/Dispatcher.scala | 2855 | `160092d1a4022f13671cad599fc32ea45531800198846d03802e25fe6e5e9df9` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/pekkostreams/dispatcher/DispatcherImpl.scala | 7156 | `575c9f99620149f15ea357ed9159e38e1ab63055697c3f5aea1796135bc4eebd` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/pekkostreams/dispatcher/SignalDispatcher.scala | 5004 | `83d409649355c4b9ccc12be600c96c8e9a7f90176a4a8dc79b986fc3a034aacc` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/pekkostreams/dispatcher/SubSource.scala | 1285 | `b88a47b78e577ab91514f395180d93b096744fcdeb45d55652c27c06dec4511d` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/protocol/CantonContractIdVersion.scala | 7350 | `79f8b1d32b9cd6ae0326beb77ca0ba23198818f0701b81ab4b292b33b42a29af` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/protocol/ContractAuthenticationData.scala | 11468 | `4735a8fa4b2ca42ce00c422a4b2d5be281754e6c8f61ce08a5dda9bc2b9af458` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/protocol/ContractInstance.scala | 8060 | `73dd0fd0a8399aedaf880c0818ce7351522a1b190b2c4e421c57faa74ddb020a` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/protocol/ContractMetadata.scala | 3246 | `ee82707cd46d78d9130a830f67f0e01a79a458b1870e7ff982b403a57f4ef357` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/protocol/CreatedContract.scala | 4658 | `07c5ad409bfec66ecc086b66f3605dd14351ebc44f86eb9b3ab2aa132fc6ab88` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/protocol/ExternalAuthorization.scala | 4374 | `d84b22703903f7f96319b1f4a33bb81ab43454e1d78c381770e43a912506ebb7` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/protocol/GlobalKeySerialization.scala | 2854 | `2e81a66bdfd15dcd6b66e26dd499c22806cb743334e46d887118823c1d7810d5` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/protocol/InputContract.scala | 1874 | `2ecd160dcacbab07fd09f08d60562596c58a9f6bf53c9352be31badffe22bd06` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/protocol/LfHashSyntax.scala | 945 | `9de174a3ea8bffc6767f1f975dec8b2831b3c04011bb743476343d8158329b42` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/protocol/LocalAbstainError.scala | 1721 | `587e23571cf2da948edaf80c5b854630b6630ef20fa6c2362ec953be31d97d7c` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/protocol/LocalContractId.scala | 1584 | `725278967636b832944bd2741d59dff4fc6b532501d71e67a53af6f85712f579` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/protocol/LocalError.scala | 2386 | `5d77db239bafdf4b0f406a69a5d9bdd9a8a65b0aad77d9df31efda7218d9b0aa` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/protocol/LocalRejectError.scala | 14869 | `cd12a5379635857bab133d07f0b34edc554d76689c8b42aaa4a9b87a0781af13` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/protocol/Phase37Processor.scala | 3685 | `c7a11e81d05dbdd155f88ece6a17b29286bc771363cbba638bfbd40ca5417c32` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/protocol/ProtocolSymmetricKey.scala | 1786 | `6faf2f80da1f53fc3359f373b07753ae16bb9d49eff6f35191b1a7070109163c` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/protocol/RefIdentifierSyntax.scala | 1158 | `1f96db6d30bb46d25053d06b8de229428a73ddd6c6a1b23d8bc0f114d9e6788e` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/protocol/RelativeContractIdSuffix.scala | 1661 | `8d1ea9e0025c75bbac7033d0bea634d53bc74b8732f2b84efb2a78680805772b` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/protocol/RollbackContext.scala | 7420 | `b84a01049557ba6e07f23d8aa08e7c0518836d5e77379f78fccb761ba0a9bed9` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/protocol/SequencerError.scala | 18178 | `8e0b737ecdbc709606ef90010aad89f716a369d42692c52305d7127ad22a8162` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/protocol/SequencingParameters.scala | 3486 | `e49bdcaf4bf0f435f810feb89a7335c5fc95899f40d1ad71ba7041ee7f9ccf3f` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/protocol/SerializableDeduplicationPeriod.scala | 1907 | `680ae8282440f7dd84a552198e8f3bc06d983cf52a2e232ac0862bec3ae9d627` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/protocol/Stakeholders.scala | 3411 | `f85c2a75b531ad5e6269b4a5150ebf0f6c1cf2b9cd1d3da23b2aa3e21e9144e0` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/protocol/SynchronizerLimits.scala | 30338 | `8e16aa1ad0a84d6241fa29d1845cf860205d8202b2474115dce0129cbbcbb36b` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/protocol/SynchronizerParameters.scala | 72376 | `d8e413d3d7dfe3e7be81c8f227a385b95644c81f34d2cb4168fb159358cf061a` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/protocol/SynchronizerParametersLookup.scala | 4441 | `ca495a68ce6e3a6a26c03335f69a22615cc064a5a78665c9caf39094bd759ca7` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/protocol/Tags.scala | 12985 | `05336a2a7647f570413411372bb2338bf98f4e5b62eeb7c271d9b490975e664e` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/protocol/Unicum.scala | 631 | `2533e484343bbf112cc6d62db555a00ad8316186b06f8fe610fb04305e1ddcce` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/protocol/hash/HashTracer.scala | 3810 | `68530cd61a620b0f5d94a0b251df8cf1a48857c0934571b868bb3a3e4deb83d8` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/protocol/hash/LfValueHashBuilder.scala | 5301 | `1e9e1f54da0fd6073a116f723b9480501c2a63f9cefec039112d417e6996a2df` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/protocol/hash/NodeHashBuilder.scala | 6969 | `8ceb6a8ec68c79cd24804ff5e6af9c1bc70b2b40745ae3a1c62fc5e66e19857b` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/protocol/hash/NodeHashBuilderCommon.scala | 8485 | `f36da37db11045f6ac540d09959122522e51c58a7f538516062cd05c86bc5042` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/protocol/hash/TransactionHash.scala | 3188 | `e6fed032679bfff5b7e0e258a0ab4047d4e1a2999de411952fa83a3efef80faa` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/protocol/hash/TransactionHashBuilder.scala | 1204 | `ec8236e15464e6164e6a069c7d3b82218b06e9160d4184517353244307d5ec6a` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/protocol/hash/TransactionMetadataHasher.scala | 1445 | `7f247a0617a24d25b6b051c620816dc80e0f86c5e9cb784221f89d1e3e600897` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/protocol/hash/VersionedTransactionHasher.scala | 2093 | `9bb43410d7879fddca753224f87a4ceab6fcbf956451f994bfc94465b0811add` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/protocol/hash/v2/NodeHashBuilder.scala | 1777 | `bf4044fb0bd0a836d0febf4f059e950691640d1d4d56c47bbfff112a5a0c8635` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/protocol/hash/v2/TransactionMetadataHasher.scala | 3311 | `96ddaa12c0bc0ae9f4f196f21d02b9fefbd2fa318a19ad31a257d4c3bc51c2be` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/protocol/hash/v3/NodeHashBuilder.scala | 4035 | `00a9592418da0b1f4ef3b69f41b46899751e0f5fd27473f1675a9a02f1964f40` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/protocol/hash/v3/TransactionMetadataHasher.scala | 1175 | `f48b3e79d624bd8f2ce3434dd1486c476882f39032432e5d44b6882b057bda4c` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/protocol/hash/v4/NodeHashBuilder.scala | 2451 | `e491322f8db7cffd48ba5cdcd34016c3becacb3c1af665eb303a539d9492b26d` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/protocol/hash/v4/TransactionMetadataHasher.scala | 664 | `9476b2e4c396ff38524153fc3cd56720fd4fde6c052f77f3f559ce4e42f284bb` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/protocol/messages/AcsCommitment.scala | 5770 | `ab77ed45cb7b10c93131bf6c5ed3b454555e9d8aef94b2805db212f0266c29cd` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/protocol/messages/AcsCommitmentApiHelpers.scala | 12321 | `6ef2d538592980832f9cdbd81c2e34bf8a8ff52e2f65639d9e6330160aeb9aa0` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/protocol/messages/AcsCommitmentProtocolMessage.scala | 7424 | `8c76b61acd005febe045017dc956ce850ff628134c4202832a95818f176f5aba` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/protocol/messages/AcsCommitmentSummary.scala | 7041 | `8e5d6491041a6723f2d79a7d6daf6307116ef2b1c2137c884c6872b97b16ff53` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/protocol/messages/AcsCommitmentSummaryProtocolMessage.scala | 6531 | `28564630201f60b1eb4874a5faf51087e51cd1cd9fff743b32a6fb0b7a582264` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/protocol/messages/AssignmentMediatorMessage.scala | 4886 | `f726ec05e123bd12f5a9a886d054b4112862959442e0abc634d765b4f3aedf84` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/protocol/messages/CommitmentPeriod.scala | 3692 | `326eda7824aa67fb8064a938d5566b1d18c0fc5948351b0b5bd251d262382b46` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/protocol/messages/ConfirmationResponse.scala | 13996 | `1d415c81de9ad7673416a2ce0d57c5f0ce718b87fb02dd46519bc89b7b4e04f1` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/protocol/messages/ConfirmationResultMessage.scala | 6102 | `51ae6eb658948e10fde59f630f6534d0ac70da8289a1920cfdf1bb0f6b3eb2af` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/protocol/messages/Digest.scala | 835 | `8e4071b4989c07d6aa4fb260ceb27d1e94eb3ef274c9dff29cb9eb9241f92686` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/protocol/messages/DigestForCounterparticipant.scala | 2501 | `6018db712be6870d36626f309f091bb7e3d295ac199e7a9f2e8abe1b22fc9351` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/protocol/messages/EncryptedViewMessage.scala | 27164 | `4aeb4fd77605c279e28ac3436125327e7b58a10b21def9f76b1cc015543412a7` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/protocol/messages/EnvelopeContent.scala | 6308 | `fefec26a062d22da08b1498c4b5377dabb2311890bb6a3c5a58af58b065bdbde` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/protocol/messages/ErrorDetails.scala | 2010 | `43670a14f63c04f33d41b9a500b2429239f12df3e7c00a1e6939a39b11d1306e` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/protocol/messages/HasRequestId.scala | 291 | `13a9bf97299901c1b401d0e497de7d78e09d5308eaada7d506030dfab03e1b07` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/protocol/messages/HasSynchronizerId.scala | 409 | `89ddad458324a5f60e908af3eb85776125b51154021fe688168027d5c87d6994` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/protocol/messages/InformeeMessage.scala | 7159 | `bcbecb4ea2f4b6881e27d14baf527b734f389261a24ceeb3c26de9a3aeeeed18` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/protocol/messages/LegacyAcsCommitment.scala | 7666 | `8a3e0fc90df8c59b0e1b53a5d075d598dd06cdbaa71dd3e825b4fbfca957b384` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/protocol/messages/LegacyAcsCommitmentProtocolMessage.scala | 4148 | `fab1e9a965ef9153711afaecbb69adbf6fd5cbb6ab37bc41b08fbee464bf7b6f` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/protocol/messages/LegacyCommitmentPeriod.scala | 3546 | `c63092ae37d3d765851c0e912b13ce608a317d27e51cf27088e0fa4629d5be1b` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/protocol/messages/LocalVerdict.scala | 6868 | `113c468528000ab369a368fbbefd70d20f593eca90fa3dea0ac34c1637e8fedf` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/protocol/messages/LsuSequencingTestMessage.scala | 6556 | `50b3c1f43bd8dcd4e5cc3d03f5d165bf0eca5f785e6cc80f33bb36de0d1e0d9c` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/protocol/messages/MediatorConfirmationRequest.scala | 1714 | `8a31646a59dc747d163f1f26b42a0945c35f83b743f27ea11a4c2864732bb302` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/protocol/messages/ProtocolMessage.scala | 12575 | `82de1d3c0ff7093afb8ae80d311f1ed1189cdfe7d995a78c2b6eb788407d3214` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/protocol/messages/ReassignmentMediatorMessage.scala | 1508 | `c3d3144a8bee712bca6137ba12139f3e2ecadac94d4bb3473daad419a6ada7ab` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/protocol/messages/RootHashMessage.scala | 9670 | `20997077cde8e237be0b3a5b7debcffbf16b29a67f58e7f3efa01d81195ccf7c` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/protocol/messages/RootHashMessageRecipients.scala | 5387 | `e3764dba9572869b3276526fdb524f333a958bdca8b9388c7cdb203f9fb99ac3` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/protocol/messages/SetTrafficPurchasedMessage.scala | 4861 | `da390e99302054c6184cd96384178d3db38abdee5d81b287181b26795ecc3435` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/protocol/messages/SignedProtocolMessageContent.scala | 2264 | `116d71ebea23274bee46172198812c239dc5045e7e974b34205c39b9be34d0ab` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/protocol/messages/TopologyTransactionsBroadcast.scala | 4430 | `4eba91a268069696947b9195458f060ad0a3b572cb5ac36ea5f6f8fa0b8f273b` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/protocol/messages/TypedSignedProtocolMessageContent.scala | 4650 | `0b829f7252184c53b027096f0526cff718b9cbdc79ae5db5cf3ffbe11e1e4c11` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/protocol/messages/UnassignmentMediatorMessage.scala | 4960 | `5a6788154f8f4ddb21d82c2cd5cc03cdd54ff3a922e02be885df5dc207531af6` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/protocol/messages/Verdict.scala | 11266 | `99c81340a98bf1ba957fade46d9ccc85950d2dfac59cc01bb6c960ceccb77fe0` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/protocol/messages/package.scala | 1147 | `01cb70890b24d18393906f8603dfa7ad4554fe805184dababf99d40fcd6ef965` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/protocol/package.scala | 5164 | `5dc3c845d84d7524f01ebe278caa6892b574bbf25c9371c308c65cd390dc4f13` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/pruning/PruningPhase.scala | 2247 | `75613be61a6696aee645b7beb4c722d04de4941ff4d04e20ade6f060b5210c36` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/replica/ReplicaManager.scala | 7609 | `2026bd7124ca6ffa711e144f24ad1d1f238a468c1f5cd68053ff8bf7ee404336` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/resource/DatabaseStorageError.scala | 2621 | `9a86bf59f500c264452e7d094fcee40d7f786a2c002fd4879902d4498e891bdc` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/resource/DbExceptionRetryPolicy.scala | 5613 | `1379303551756d25b9375c15ab7d0cae520d2d021cf9415219e961a70e7e6229` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/resource/DbLock.scala | 25087 | `3a27ab6b9722415b37c021f8ed261ea76bc8198a17edfc898978448bed8a150d` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/resource/DbLockPostgres.scala | 7203 | `df138d58f6919d9f90d4fafe8360c4a0287319ea64ded61f48520333e2af1c04` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/resource/DbLockedConnection.scala | 36989 | `8ae96d92f1816b5b1827af494e37f2f2bb324a57de12e8921643bf8105742259` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/resource/DbLockedConnectionPool.scala | 19636 | `31239639b794a4d18f91d608c86ede3c78ec0d8fa702e5ef22fc976b60564819` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/resource/DbMigrations.scala | 17691 | `9aebe3f569cd321008d143ef0f2436c0eec65b2253881a6de3d0cd75d3f4e2d6` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/resource/DbParameterUtils.scala | 7731 | `18ed92a37a240649c39c4faa30c3594b1359ae5f2e909bfa6cc84fc7fe448e96` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/resource/DbStorageMulti.scala | 16576 | `0f46c1089e661930a396810c28106d22feea1d24191ff83ab47cf4b117c88b84` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/resource/DbStorageSingle.scala | 8568 | `42115a6b58b62aafc4f815063732fd521c2c44572124e71fc9878cd7a895df46` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/resource/DbStringEncodingCheck.scala | 2237 | `4fc381934c6865044fe6efb2e6c44aadd861c27a0e9ac9ccf211da8eb0fb8a97` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/resource/DbVersionCheck.scala | 3655 | `c92de4a2494915287212f3cd74922b53d6616420e3636aa31de610cb2ad9403f` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/resource/IdempotentInsert.scala | 3527 | `0cd8d9afc1d02a1a2d0224cbaf9734af3ac115da904d65e634f32b63495c6c5c` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/resource/KeepAliveConnection.scala | 7345 | `2934c6af0ab64dd22300689cd918966a03ae35db66c4c2d6c583aafae8f3019f` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/resource/StateMachine.scala | 3265 | `2ca46ed9cf2a21db184cdd08d84e059b537b587a3dba9182ccdf0658fe2c921a` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/resource/Storage.scala | 42182 | `f22772c02e3cbc32487fdc111cfdecaaf70191258de94c4c4b5adcbc4d9ca09c` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/resource/StorageFactory.scala | 2103 | `4944505efb9cb79d23433108efbb42bd03c35beeef10ceb91554c7de69e8ff8e` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/resource/StorageMultiFactory.scala | 3838 | `24cbf5ef13f61c9ff6ce9e16c27062f852a5c878dd5f9d97fb90539229c066a6` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/resource/StorageSingleFactory.scala | 1792 | `1c620a9ff976321a7852b110fcf5db56c3c17cb974fe5866ab06b89be438edfe` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/resource/StorageSingleSetup.scala | 2695 | `933c696108404bd7e04182d10186edc7421d0205ec0cd398b46fed428f09f627` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/resource/ToDbPrimitive.scala | 947 | `48d741055c58c7f94581f03dcf0864693014cad5f232194aceb4bf6053d98b9c` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/resource/TransactionalStoreUpdate.scala | 4523 | `b4076cf0347b5dac040a9edbc58fae80bdcbe8442a94729d5a4764b32a8268c2` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/resource/WithDbLock.scala | 6927 | `6e4e3313e64e109c7239bd48074f37983a8927a5ea5b5e641d32d2d8b4386f14` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/ApplicationHandler.scala | 6283 | `cc5260253ffed94a63cb077f6fa575fc122bb33e3df9f9c37facc7d424ea2e63` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/ApplicationHandlerPekko.scala | 8294 | `fca57975b420dc4cb86de63857f67e734f39e3b982cf8f5d58cef80db7cd0ea7` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/AsyncResult.scala | 3304 | `f280b90b11e9db05a4c25304c04769168d9ec3847685e4d47122e73d79c009dc` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/BftSender.scala | 7292 | `d3985fc9131d2ad6504bdf75f0e7827134fdfe3db931a6e774fa472dcf6b532b` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/DelayLogger.scala | 2355 | `e966cc6881d07a49e8802e3f34dd53cc1675e929d8d2aac11c2c4936b2116065` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/EnvelopeBox.scala | 6325 | `b6b8305db049e7be9205e7d1edde50a8b8ab48cb4d6738f9d0d8dfe505e050cf` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/GroupAddressResolver.scala | 4095 | `98dc6da34ce308ab87f8d51de9522cc2d4b489ec47e9ad267e3555253bf9a53d` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/HandlerResult.scala | 3400 | `db14e9ee209806ba3915d858d9d7bcdbb76e8e6babe995299b39dfa6f7d5df0a` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/PostAggregationHandler.scala | 6245 | `a743794ff76cd48934530c15c36b1d91d1c31a1e4e2e239f19d9a77e4d66f3db` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/SequencedEventMonotonicityChecker.scala | 6060 | `0eaf98b04c5afe3d795d2e99731aa6211ff9176473ca9217a02158dd922bacb6` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/SequencerAggregator.scala | 17718 | `4656b583d84e5fe88986c6123649f6dafa494b9bf710c292da2a857026da7f43` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/SequencerAggregatorPekko.scala | 16470 | `074b13bb9fc8d35a174dbe06e6dc5281914eadad61b18c3ffb7b59599d030bf9` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/SequencerAggregatorXImpl.scala | 18041 | `b9358efa5f02d08f1bf93b8a84a027f3e96c5db8d30bfb9517336406aee056dd` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/SequencerClientRecorder.scala | 2797 | `2f83fd8bbbe19eddc6451c78a8bfcafb1adab2919743e32947ba576b7cfa8c26` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/SequencerConnection.scala | 7893 | `58090324366be79712faa758f0a46becda45aef5a25b20b04fb3ce14d28201fc` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/SequencerConnectionPenaltyConfig.scala | 4049 | `4bfa4c0fb6f496ddafc62ba2916d459b05d37958147b485a383a9a2991d451bc` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/SequencerConnectionPoolDelays.scala | 4315 | `b35c1f908b5f38fdd2cdf4c100faab9278e9c2ee2f0c31123dec31f9b95426df` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/SequencerConnections.scala | 12078 | `ae8d8ba7636a1f6614e7b5b128e0daaa56f9b17f4104cfd0e71433c5dd6c40a9` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/SubmissionRequestAmplification.scala | 4861 | `05bfe16d1f54c2a76dd0e3ecf4ca199538609d6dc247ae5962cfb8f7642392d6` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/SubscriptionLivenessLimits.scala | 3213 | `b5d724383e6972c4425ff7c18a3346fb21d3485e90c7264901a76a43434537da` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/TrafficControlParameters.scala | 7170 | `ae4fbb40872a20073038cb3f93a22b7b3bd3d092628bb7ba5affd9eac3efac19` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/UnthrottledAsync.scala | 1941 | `c82364ae304957db8f87c08a66561cfdb03ed648976889c049730ed43ac35e2f` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/WithCounter.scala | 1255 | `9cd6465616c66c382fbb1b538503ace730b144a7116c1bcaf03c4538d8519f5d` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/authentication/AuthenticationToken.scala | 3374 | `9e2b6e423e77e2c83eb466d901d6ac683ae3efcca832a9f7999d9f7eb5f353a6` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/authentication/AuthenticationTokenProvider.scala | 13138 | `789623e8a68ee05d8c1e617a8cd0cbf145139355f70049c7c34d479a509051c9` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/authentication/MemberAuthentication.scala | 8138 | `321f4e535310ff86beeb202b7220954a94a03bc122f74ebfb2a0d9bfe49b2027` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/authentication/grpc/AuthenticationTokenManager.scala | 8169 | `b0fd61199ae99c614612da8b872df2e10c5503cda0f0cb3af96d364f891f6610` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/authentication/grpc/Constant.scala | 1261 | `f5bd985b90c2fb1515b61238f7316a722216441f6f4abc9c503245964be52480` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/authentication/grpc/SequencerClientAuthentication.scala | 6043 | `38164a76102748b3f2ded5a4022462f3b08be622e605df4cbc8640066479b45d` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/channel/ConnectToSequencerChannelRequest.scala | 6312 | `b3aa0159d4bcd7544fecaae29c99dc1e76c810cbe087b47f510e6cb750841434` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/channel/ConnectToSequencerChannelResponse.scala | 4666 | `77ce618716a659159dfaa44feb57fda89cf9292d0172c09270bdc4f0e63b400b` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/client/BftTopologyForInitDownloader.scala | 7992 | `d0957a53ab77a8d8a88a8ca2974164f557e25335c3dd86bcf6a2083ea9733878` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/client/DelayedSequencerClient.scala | 2491 | `dc3492ab42f0b72c4468a1d50e296e824bdc3b80117cc786d89842c0c298b3bd` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/client/PeriodicAcknowledgements.scala | 6514 | `ce2e8ca907abf6091cfaa6c235cb347c5c2f6682068dbe8a598f20ffe89a5c76` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/client/ReplayConfig.scala | 3104 | `1fbc9a95b85a04b7cf5a8626dfb492ce8d0e50652893bc798a2da303c0092a16` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/client/RequestSigner.scala | 2422 | `9baff1b402b444afafbe0232913a1df3539937a335d3d2ac9681c8f2c72ecd79` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/client/SendAsyncClientError.scala | 3892 | `5f91e349ff2c80c502c87ea75857556907a561e02e1316929f80868fa2e8c97d` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/client/SendCallback.scala | 2445 | `86a4d33c38404b5cc007a550c7e1becccd126fc797b4225b4f17ac556168d320` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/client/SendResult.scala | 3843 | `967ea785f3af6ee4c4f20113f39bc23933751c19f55459c1832ccff9ed8019ff` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/client/SendTracker.scala | 15974 | `ed73bd17070014682c908c169a8efab87496ab022502a79fe1df25b9a10fe803` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/client/SequencedEventValidator.scala | 36504 | `db776c51e5f5a534444695dd2d3ba2686ec561d21db0a46070338fdbf70099e8` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/client/SequencerClient.scala | 103689 | `91e8ab4752a32ee30212e2afe53ab5cc2d48d6c9148a3f5d022c43452054f85f` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/client/SequencerClientConfig.scala | 8799 | `996dad39f111b3149e2e0f01432507a5d6fa56f4f3a47bf891236e4b750e3c9a` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/client/SequencerClientFactory.scala | 16991 | `d42283c4726cfbfa7975570f51730dadfded5716a09b2723e35d15e666b68f25` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/client/SequencerClientSend.scala | 9521 | `5491dd8c53069aec84a4ce7832cfac89d3de80b046b545e5c969a0c64d62caae` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/client/SequencerClientSubscriptionError.scala | 1975 | `8ee3964903a77050a1242db628d452ecacba905c1cb45c6c6d2626c79ed6010a` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/client/SequencerClientSubscriptionException.scala | 472 | `14e710d5b85fe0dcc48ed772ad02f470df6d1ae1d09892396d934acba9170e32` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/client/SequencerConnectClientInterceptor.scala | 1142 | `197c6f5a776c813e5c5ad2718239acaf49e55319fea121f73a2ec778cd5c2df5` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/client/SequencerSubscription.scala | 7598 | `249aea01710a92b395b7d83e289479b837a4f67dd8b09e4f513f470729bf5275` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/client/SequencerSubscriptionFactoryPekko.scala | 1920 | `96a848bc97cfdb5cd219b800235a72bcd426069428c891ad76c4a39786e23624` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/client/SequencerSubscriptionPekko.scala | 1065 | `3e681761e6a282b70fff718c9091e45829eed533472eb06b047c3c1aa8a894cf` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/client/SequencersTransportState.scala | 1322 | `5df100458bd9e4d6cc892009c21de663be59a605984369775ef6fd0bfc9739d9` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/client/SubscriptionErrorRetryPolicy.scala | 2003 | `dbbe84f6440c0e3a57d87372ca5e16000bbec570d5ac93ccb21ef17c0f003dd2` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/client/SubscriptionErrorRetryPolicyPekko.scala | 1178 | `f9493e0181d7c6eb4469d0cbcf481e7caf600218e0d704a58770f84664c6b9f9` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/client/SubscriptionRetryDelayRule.scala | 1762 | `2095b3f0cf8546331a7ba5c679369a2cc74d3eb53cab12c47cf4d9ecb303990f` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/client/channel/SequencerChannelClient.scala | 6915 | `a50b770b25776874cd7632656dd335a2d7e6a3237324a1223d0d0ec021393265` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/client/channel/SequencerChannelClientFactory.scala | 6383 | `9377581e53ffb16f21cbcd8b0493ec6dc790445c321a47d3ce917988cf13b664` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/client/channel/SequencerChannelClientState.scala | 5320 | `5d71f3d2db34632a4d37657d04e1631ab0a0ec4f1d4d52acfd3f5566d37483f0` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/client/channel/SequencerChannelClientTransport.scala | 4274 | `5de56f9d4c7a3cc950318b5e94f6e315dca8b037d559815e8cb2f9eaaf41a046` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/client/channel/SequencerChannelProtocolProcessor.scala | 7403 | `64d69e0197d61f343c1e4f35e6009239128840d710aabacb59112427ae9f26cb` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/client/channel/endpoint/ChannelStage.scala | 8336 | `2721c5f883a12ff1eebf2a1530380c08ab901412c2dd5df4fd2b627b3f7c1bcf` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/client/channel/endpoint/SequencerChannelClientEndpoint.scala | 13440 | `985e868a37219350e4bff7b12d9f9a1f449f2fd5464463eb14582fadcd76f74a` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/client/channel/endpoint/SequencerChannelSecurity.scala | 5451 | `79209162f01862578831dcfc4133913d66470b9ddcbfedaaecdf066bee9036d1` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/client/package.scala | 1038 | `f51748d9cd04a7226960a8252828ecf13059cb7527520ef541e8e81833d99673` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/client/pool/Connection.scala | 4923 | `bda6ea2897a04d2f6bb06f95c0c2fc5a95dff5d4013aaabdfe214b5bf9fa4a27` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/client/pool/ConnectionValidationLimiter.scala | 9815 | `59fbe597d0beccfc90148023af9f4d4961e457815a55ed41ab012125caaf4af0` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/client/pool/GrpcConnection.scala | 7944 | `621c84a88ec7e4221bf953c0ffaa9bf7883e20a94c40945ca99389c954a69b0e` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/client/pool/GrpcInternalSequencerConnection.scala | 23336 | `24781a365ee30210ad27afef7c104d16998862bac2ca065cb685ab29c75789c3` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/client/pool/GrpcSequencerConnection.scala | 12999 | `0d8c4c92411b1446fe75672d71307e7209a1c356167166881577bd3b3446c30e` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/client/pool/GrpcSequencerConnectionStub.scala | 9762 | `c9c21d294d8ff413c5766349bd9ad008c16eae78f9e11f080ccbd1093c59ac76` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/client/pool/GrpcUserSequencerConnectionStub.scala | 10323 | `f6adc827989a54f01ec5e2d5188ea65d6098e9fa4385ab9e83a28dc8f562b3cb` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/client/pool/InternalSequencerConnection.scala | 12069 | `d7bb76007320aa212813a9851c0ff06ad13269d66b0b4e2079969abf358834ef` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/client/pool/SequencerConnection.scala | 5698 | `d4483d2c366e38882544b4affa31c833bab28d96850b92d711351e1fe5251ae3` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/client/pool/SequencerConnectionPool.scala | 18701 | `da1e16800531da78c4bed919bf1408508e55d46b240a7e837d482b3fd9197227` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/client/pool/SequencerConnectionPoolImpl.scala | 39169 | `42d0e5f20d5de55aaf6ee8ee6a57159ec35a720f8b11c00462aa498d0aff1968` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/client/pool/SequencerConnectionStub.scala | 3923 | `42448392fa8bcd3d69e37d25ded70a6b3bd958b22e892b3dcfadbf2f4ff75004` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/client/pool/SequencerPenalties.scala | 4314 | `303af817643d735d4b49cb37d7232f86594a6d3a7b25c55371068d709f96f811` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/client/pool/SequencerSubscriptionPool.scala | 6941 | `a4f9a0cdacda2eafdd1e8487365d6ea4bcafeafe196a5c50f4654ba00202b727` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/client/pool/SequencerSubscriptionPoolImpl.scala | 26637 | `cead1fd47649bd5d4f8b8437f87d266a1e71227e97c57a3ee2ae06d82cb23ac4` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/client/pool/SequencerSubscriptionWrapper.scala | 9049 | `ca9abb57a41df39a9030d4fd118d6cdf060f46fd1d1d54fee45c144e0b47bfad` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/client/pool/SubscriptionHandler.scala | 6444 | `28c2c1c5e7e60055600218a1039593e2907be969eb47873755129f498965850b` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/client/pool/SubscriptionHandlerFactory.scala | 2227 | `8492ffba68cf0d1e6260882630c8972d84fa09eecaded67a7df9af9aa7a70b6d` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/client/pool/UserSequencerConnectionStub.scala | 4037 | `3ab4d1e6d420afc5a188c083366bfd084734dcd36c51f36dd6e2f3bb932755f8` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/client/time/fetcher/SequencingTimeFetcher.scala | 7601 | `467ee8eec3c531276dc743a073178bb9b7cf5e812deb187ecf92d84a7887e0c8` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/client/time/fetcher/SequencingTimeReadings.scala | 4297 | `39df95a5a7c2bc6cbb9efd7fc75b70d99cabf237c169850e5ef20243e1448efe` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/client/time/fetcher/TimeSourcesAccessor.scala | 6710 | `5698eccf2fb6b07ccd0a76aff782302b1b6a03cd085337171683541e97f4e938` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/client/transports/GrpcClientTransportHelpers.scala | 2044 | `67a0176fb1865293af9ab056c2e1dbb06a21a110a2f7affe5682cd648ccd2cb8` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/client/transports/GrpcSequencerClientAuth.scala | 4195 | `c0f8647bbd8cea68201973ba01136da6f41e04e074496033eeef344bb87a7d47` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/client/transports/GrpcSequencerSubscription.scala | 18217 | `5f501feac165420f08182111d4909189fc54b34ebfca67a127d73e8b47d1bb34` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/client/transports/GrpcSubscriptionErrorRetryPolicy.scala | 2885 | `6250ea0a975dcf52f61d12a781a561d76df2616bc860e5ee8562062e74b6a07d` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/client/transports/replay/ReplayClient.scala | 17729 | `7572bc15b8f10fa1d77f4408ea93bef27c5335aff1ac4e93706aaf7047b2a080` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/client/transports/replay/ReplaySequencerSubscriptionWrapper.scala | 8033 | `e548024451cae7b4b03ab22c8fe71910e7768dc58cf7b94d6cacbf9803421866` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/handlers/CleanSequencerCounterTracker.scala | 6480 | `e3d03f96e032692f5ead0d811574f15f08fb90db563edd7e12e1e17cdcd46212` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/handlers/EventTimestampCapture.scala | 1868 | `418833e976916a7ebf9def59d9bd02b56a94e637d50c789dfbb5df8f5262a6d9` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/handlers/StoreSequencedEvent.scala | 3998 | `f72e3e17541f2c2a4668a54e3c5ead6cf84b7aad5a41d6496a4516b09c34b726` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/handlers/ThrottlingApplicationEventHandler.scala | 5395 | `32ef2e3d50231c018dab7f0a65ab679fca82d928f7f5aa9f4cc8b404093d76b2` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/handlers/TimeLimitingApplicationEventHandler.scala | 6326 | `806859b9b649747627ab73dd3e3f23f6b7d0db9a090347490cb59412823db6d2` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/package.scala | 6501 | `5e25de1d86e88c3873d47ec6d5e6e6b1759612c4c258829f20fe533b9e154b16` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/protocol/AcknowledgeRequest.scala | 2768 | `9e4e1e89280057ffe2ba1366c64b0e502f51bf37c2b28dbdfd701b2425b9b33a` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/protocol/AggregationId.scala | 1700 | `5841cec0716c7edaac0b2bf13c6bc5485fedbd7d9865a9cc1f4daeb7036c15ea` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/protocol/AggregationRule.scala | 23413 | `3f75b475069e07fa5273f29488eecbc0c1afcd581feb6f72790bea12900e3e54` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/protocol/Batch.scala | 11309 | `6cd280bcefe7ef43e77668a8369ba7a28e1abbf4db82de86055f98d656b67cc3` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/protocol/ClosedCompressedEnvelope.scala | 5129 | `c6128539a9acb05ded1448f7d31cef14c7659dabc83bb425ed5c0733d1ec6136` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/protocol/ClosedEnvelope.scala | 3814 | `a72546f65b74e34b1e1365363a9fe31ce3bc2b9ade52a860e597cec88b146a4c` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/protocol/ClosedUncompressedEnvelope.scala | 8939 | `bcb2e3c1dca9a6838f13eda11c8d4b068891444cc14aac8e761a4fc487346c04` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/protocol/DecompressionBudget.scala | 2548 | `479671e48234b29f032967cd85210a6e28dbaa0cecdb3543b0af6be55a8c49c2` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/protocol/DecompressionPolicy.scala | 2574 | `9327bda53df90dafc8adb8bb3d10021265ff34e95597dc667ee8ae039137c8ce` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/protocol/Envelope.scala | 1239 | `80a3c41535e19e88d76e3297b22cd07afa28d59cd6685bd2aed2b9b39ee65e40` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/protocol/GetTrafficStateForMemberRequest.scala | 2558 | `a89ea8121615b588d80f1851393db6f8cfb6398d9125fecc8a3b38cd0b960750` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/protocol/GetTrafficStateForMemberResponse.scala | 2185 | `50fc2d5d466f4ca9b77a670cc93c0c9e02f9fc59bc660bde597b134d0e16de8e` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/protocol/HandshakeRequest.scala | 1320 | `002a7d8655927f49826560ba474b9e22db5abcb3dd333e45a8e6c79cc5d0b2e1` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/protocol/HandshakeResponse.scala | 1032 | `f444019ef3abcbb592d942222801ce404fe55105346c5e7b236281ea734c1a24` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/protocol/MessageId.scala | 1379 | `bc696e37fc73c7d9f1d9389bf2ab9ed0517bf184e8147b5bcd623225f3e372bb` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/protocol/OpenEnvelope.scala | 2447 | `076c343cf5bd8e5bba7371a50101be33f930f546eba7c9dfd7b079761471abb7` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/protocol/ProtoBatch.scala | 499 | `4a942cd2e90f8fe3f6d916f912d737c6dfd7813511aca9f65fccb3758bc8a8ef` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/protocol/Recipient.scala | 6189 | `965594f1ab9502dbd51333c9b3e96c1d14eec1952257cced1865f48c5fc40b0b` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/protocol/Recipients.scala | 5144 | `f72d4f63bea78f7a6d0f6393d22a1bf76dc6601d20653cf0c3b2c830b122e7bf` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/protocol/RecipientsTree.scala | 5760 | `7995b36f32ee28e91aed67ce8d65a082f966924e4cbfdaa802afb84bb1d2c47e` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/protocol/SendAsyncError.scala | 3106 | `baf1e0b5811e1f2a072610c080a2389806b3f1d7458d1f1ea3b1cc6c2fe79931` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/protocol/SequencedEvent.scala | 22384 | `499543b682e5657f75aae8ad4d2113daa5696a1158b87d64a3290b8628151420` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/protocol/SequencerDeliverError.scala | 12628 | `68c3f50fc73214c1faaf95b67560a0f3fdd78f4498b821c916dee1cba82aa809` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/protocol/SequencingSubmissionCost.scala | 2783 | `fd3a0b17055b57c5636a798764791d8f1ce531576b8a60d398b69236ae94de56` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/protocol/SignedContent.scala | 11930 | `1d8bfb2bf5e32225550c8070ecb2f9dd645cf8197a7ef6345a1819a5e6be0d11` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/protocol/SubmissionRequest.scala | 15487 | `8680ad0afce8ac246fd47bea8b1309d20c1dab2120383b0e16c2b71f9b87ad71` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/protocol/SubmissionRequestType.scala | 4121 | `4bfbc84b9a6c43c462f82e71729f0cbd4909e54551259b1a837adba575138b5d` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/protocol/SubmissionRequestValidations.scala | 4234 | `00eb4d27a3598fa3685bd3024621e1892935dd72ef9b66efb44a0874b67ca3a2` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/protocol/SubscriptionRequest.scala | 2454 | `ceb11e20a4e736f2b15e217a74416b9fb4423b5bfe032d3b7b50c8e2e8167a66` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/protocol/SubscriptionResponse.scala | 1598 | `1f9ec76a546a92822a805d0b19d562ce09a9dbbc24f24cae1e001ce8fdc0c7ec` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/protocol/TimeProof.scala | 6179 | `8693c4f3d761396b89afc791e09c44aa452d460f7ebdfbaa727ddefccce503a4` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/protocol/TopologyStateForInitHashResponse.scala | 1082 | `45b0490d9c7496735ead8d3158d94b95ee8892051058f296c9c030c806ab4fb4` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/protocol/TopologyStateForInitRequest.scala | 2913 | `dd03a7a4acd33f177de591a3c5dd8e67ae2042f9b4367641bdc532c1ef9979d4` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/protocol/TopologyStateForInitResponse.scala | 1528 | `549baca9b28678f82e40cc8b2f8b23533346ce4cea839dcdfafe4e800a580973` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/protocol/TrafficState.scala | 5336 | `42e6a37d2a340757f32515c2a4bfab2e6f682394db0878f0780c2aeee5f640dc` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/protocol/WithOpeningErrors.scala | 1225 | `b425a540965ddcbc46350bef21429dba07fa519fca0f940b59f1291ac88c6827` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/protocol/channel/SequencerChannelConnectedToAllEndpoints.scala | 2037 | `42579ae0fa5603202a25e69beb777bb2d2200e58d670e889b158639f37ff14ae` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/protocol/channel/SequencerChannelMetadata.scala | 3446 | `f4d9b0a0cc976d1b14fd384ec91584c34ec09269b9cd39c25b51c9d1aa45c870` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/protocol/channel/SequencerChannelSessionKey.scala | 2621 | `63480ef27a81bfccd074fa8f55152e0df254559d301389828b8ff9e6864464ab` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/protocol/channel/SequencerChannelSessionKeyAck.scala | 1858 | `1ccf0a2724cdbdab5802cdc3b5e1905bbe615ae285030439d59f378d6e4926e5` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/protocol/package.scala | 608 | `72e0d0dd42a0034fcf2e18a7a4cbd29aca563bed0dadbf507498da7a491d5397` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/traffic/EventCostCalculator.scala | 5513 | `c4b20d22c5d356b339a66cbe8011e3ee6bfb18d4f80251b97ca6c0cee2cad379` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/traffic/TrafficConsumed.scala | 10148 | `caae1ac3fbd982f1c430f5af585e5c5159f326ea8a6fd4721273d1ddb9bff12f` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/traffic/TrafficConsumedManager.scala | 6237 | `86aa21f1f3bdd92111264178627a9a823d573d45bcef17ce1320643aa9368b95` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/traffic/TrafficControlErrors.scala | 7227 | `d3da8aa67d59a022fab67c7cdc156768a932d49a8112b39beee454f4aa5872cb` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/traffic/TrafficControlProcessor.scala | 9041 | `4c139537317eea0656bd6ce74fc79d09cddd0756d4cdf8b66b4f5e828ec5758c` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/traffic/TrafficPurchased.scala | 3734 | `61528c525ef8b988cc2cdfa5cbb18005e3c7963d41d0ce23d70fe42730872f4a` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/traffic/TrafficPurchasedSubmissionHandler.scala | 11521 | `fb82017c2cee5a23f839abaa292019d43813437f77b7dfec7fe85cd58e71e3b9` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/traffic/TrafficReceipt.scala | 2948 | `51c24756cbd41d35feab401929d1afaf35413f995a8c7b33f195cbc6cf5b15f7` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/sequencing/traffic/TrafficStateController.scala | 8286 | `b3a201642f7d7baa46e39913f086ee0bf535447363334d977d278c53868952c6` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/serialization/DeterministicEncoding.scala | 10658 | `37fab315f2dd4e5c58b0a63bc46512c0834f4d675d51b01a52795a2c5cd1168d` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/serialization/HasCryptographicEvidence.scala | 5869 | `a8875c280b598b1b43baafc89cdf7c36c9b64e0c4ea047f7bcdd9d01766cdc5b` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/serialization/ProtoConverter.scala | 10783 | `b227a11859703806ce353183a1be12ed8abf9b6e189e38d582e83ddb4f00d426` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/store/CursorPreheadStore.scala | 2929 | `86ce44c750c185d1e8816157bec22525db49c67759023699f6a5e8c3f4998c04` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/store/IndexedStringStore.scala | 12139 | `49383259d33579fdfcfa21ac9fcaae9bee913149580551abbd083ac9a2ead2c7` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/store/PrunableByTime.scala | 11095 | `3b11d9215e3afbd2bb401dd395f3976196419718f5cefef0e9c858503abc80dd` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/store/Purgeable.scala | 1612 | `b9ca755ce57eb423c5fca9d270ef139063cd03f91d37d161928839dc9331a815` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/store/SendTrackerStore.scala | 1693 | `9e7f8d22d00dc6b09587131a039752409bb9bd924cead72a05ba0dcd92c4b61c` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/store/SequencedEventStore.scala | 26693 | `1e69fa18245283fb52968802f87605d4f31ad3d4fbfb2edc850160c6aec40501` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/store/SequencerCounterTrackerStore.scala | 3024 | `46861e400b1e7f3e0e687060bfdaeebbec3c7aed6b32d30f9ddd1fef86f56bf0` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/store/SessionKeyStore.scala | 9986 | `2ae9580890a57945a2095f35c90d0fbd0712e5eb75bfb8d161292aacb96e7a6e` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/store/db/DbCursorPreheadStore.scala | 5718 | `31530f26818d0dd925ea8ff5a01ef3ef214e16e4c191fdab396bf4e01a0fe53d` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/store/db/DbExceptions.scala | 907 | `3ea20a06f21fd30521844727e4a382ab41b7d07ff1098759f2f3655371e4e200` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/store/db/DbIndexedStringStore.scala | 2973 | `104ff1a1be1c8ce0a560575415223b921a56f05c8ef7ec7c78623bff847ac041` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/store/db/DbPrunableByTime.scala | 4930 | `50cee05eff173e6604c5259281febae0f3cbae36d3b44ece2a74e4ddeba5273f` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/store/db/DbSequencedEventStore.scala | 16196 | `34aee082893207879ae699a0e0ab39a3d885072598c3454a6b773ab2c58ab29a` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/store/db/DbSequencerCounterTrackerStore.scala | 1433 | `d4247a990f97e1f731d4f0e57a8145222192803b3b8002998e571c530ae47d1a` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/store/db/RequiredTypesCodec.scala | 2053 | `458e3837fc9e1b9c2f99c129c6fa017bd175cf764875d90d7df74ceff00e6a04` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/store/memory/InMemoryCursorPreheadStore.scala | 2517 | `fd50671ad4c8e0109c5d807e80f1174613ce26e642745357560f4c43411b5be1` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/store/memory/InMemoryIndexedStringStore.scala | 2652 | `ff35632ea38e30532df5e8ba5642427b3c5dc47144fa997f351dada9eca73b9a` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/store/memory/InMemoryPrunableByTime.scala | 2079 | `d2de86018b3c053bf73545510e9616e37ef38b2e4b065bee2c82f1ef1f5a9929` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/store/memory/InMemorySendTrackerStore.scala | 1425 | `0183ec37c2e5d8fbd6c5959a5f2f28420119a1c864e477e64f4b3b81d3980cfc` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/store/memory/InMemorySequencedEventStore.scala | 9758 | `bbb656a6882bea5bce94762c08079bfdc4b54a49334b993d8dc12bb6b070c130` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/store/memory/InMemorySequencerCounterTrackerStore.scala | 905 | `2890e6d6d4acfebb2a3cb9ad37b7243c0eaf50eca3cb4e572762e3cc1ebe0fe5` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/store/packagemeta/PackageMetadata.scala | 8595 | `8c6970b79b16762d1e0986e353a8f5211ea7bf72cc21b674e02b0ed70dbf3395` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/tea/AccountId.scala | 3368 | `a0328fb7d1fe8d43b64d7f26db9fcaac1cb5651365943d34d1b8f58e729b37c6` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/time/Clock.scala | 29937 | `0d698a19d4fd28c794a2d2a870f338e0aeb0cbdc6b9f81d6895a9ae34d8c00a1` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/time/PeriodicAction.scala | 1516 | `b12f3fff61b75f10e206dddc5b9c5e9d45a00d90b7784fa4a90e228784ba5455` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/time/RefinedDurations.scala | 13384 | `2d90a1170c95da84f1cf9a13c3a3e479494b8f7c1315ed2ba0af5c9bae16a1aa` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/time/SynchronizerTimeTracker.scala | 30284 | `2134702a42ddec1bd637cc2b86e75def166efd1e43a3304e1cd7db992a51c2cb` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/time/TimeAwaiter.scala | 4152 | `fc00308e0dd6c660348100190f5b6b5862530a387b06b1efd9949bfe67b52f13` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/time/TimeProofRequestSubmitter.scala | 6934 | `c18e3ea96027b91242292ddc1b5c6d393543d17b8f6a86d69dba97f8e2d86c71` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/topology/ConfiguredPhysicalSynchronizerId.scala | 2652 | `6d5023a0cce90ed2f3f7aae7334c0cce4d067ddad3e58f729eab35c8a70cf323` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/topology/ExternalPartyOnboardingDetails.scala | 23683 | `bfcfc4787044dcf106737b99b2d189843ffe28203ab24dee455201f861f5346c` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/topology/ForceFlags.scala | 5081 | `c639593e70aacc4750a7b01da6ea18b9b145cd4d8579fef16a5f87fe0529aac0` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/topology/Identifier.scala | 8829 | `057efbe41d77d1d598dd40a5f101d60d23cc9a706bb75ef5608a8faffdf5300c` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/topology/KeyCollection.scala | 875 | `d2303c52d1efd42ebcb7ac4bae8078a8abdd00d8fa9daeb9b370eb862d299376` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/topology/Member.scala | 26434 | `88c356746a1077a6e489470c3e4d15cdb4e5fd8108268c83f3553f244f428f4b` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/topology/PartyKind.scala | 1279 | `02e68db545279c0ec1bfaa11865f52de0f1716b3b6e61bd223c12e87db624112` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/topology/SynchronizerOutboxQueue.scala | 5971 | `d1f6911079855b3e83ec601a5681b6fea6efafbcf7c339b32dbe96a62c3e50d4` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/topology/TemporaryStoreRegistry.scala | 3087 | `46d0dfb237b430c65b16c82f154671c3c70114074440d819bfccac0253aaaec5` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/topology/TopologyManager.scala | 58775 | `df9d64fbf0cb7ed45448fddc7e6c3d48a75b977849b46d7016998017a94e80e8` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/topology/TopologyManagerError.scala | 61230 | `76f9688a757ff26124ae1adc51cc06b83f9b1bddce88608b7809113de2087548` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/topology/TopologyManagerStatus.scala | 620 | `bd8991790391376dc57f6327cbbdd7a296e0d9572f9c430f2e30873a85e400df` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/topology/cache/TopologyStateWriteThroughCache.scala | 61176 | `ed1b600cb7df99ce3291ed71cf98a016e1d6dac620ed7cee964483851ea1aa13` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/topology/client/BaseTopologySnapshot.scala | 27083 | `eef7782beaabcc5f47e763a34fef831db1f4f8573b6869117f9aa4739538259c` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/topology/client/ForwardingTopologySnapshot.scala | 21066 | `1e98fba8e3a22f6eeea5f07b2f14e0a86c539163c978a45ed95afbf3e34dcc52` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/topology/client/IdentityProvidingServiceClient.scala | 55078 | `1d57b22cbdb3aeb406b4641e95a5310ae10c6c6b228dfdee803af853fb4b1385` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/topology/client/StoreBasedSynchronizerTopologyClient.scala | 23587 | `71f2499eecffda8d7a87f082aeb7359d4ba300175ae8843e365120691991b72c` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/topology/client/StoreBasedTopologySnapshot.scala | 8219 | `04974758194b512f240830fb4e0b1c98cc2b0bc7cd8915abac652d33a9fd1b1e` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/topology/client/WriteThroughCacheSynchronizerTopologyClient.scala | 23531 | `2371ba549c6e2d4d09030f22fcb34b3a1c0e85bbccca9164f5aff8a8bd5eb93d` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/topology/client/WriteThroughCacheTopologySnapshot.scala | 11726 | `f3b8fc82e2bba50bf2a467d4e03dac8a4edadf28cec18574bb9797155c8c9302` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/topology/processing/AuthorizationGraph.scala | 17156 | `647b6af4d37f52932f40a7e00f164b4fc92b6de4fec795c0561dfea12f64b518` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/topology/processing/InitialTopologySnapshotValidator.scala | 14960 | `268d708bb6e682622401983c8783341cc6a2946d9ef33cc035f3d88e18705061` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/topology/processing/TerminateProcessing.scala | 2465 | `e2884092783b0bae39e7fdd816f0601a0fdeaa3cbd11c10f1f36d31a21c50bf8` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/topology/processing/TopologyManagerSigningKeyDetection.scala | 9823 | `00caa362d21c95499317287b4123d99ee17e347316d73d720c2bf7f64c786909` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/topology/processing/TopologyStateProcessor.scala | 21595 | `f7a0f11dad99bb5e5ac9ed6ddc57e4d462fd9a2199c644ea53fed136c2ecc240` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/topology/processing/TopologyTimes.scala | 3176 | `74ad8b8db6e429e2384d53cfaa12ca32f95517a174a9c4f0c6be24758d231702` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/topology/processing/TopologyTransactionAuthorizationValidator.scala | 27174 | `87cbd3899fad39153c04af6e013469bc1a1b3d36ee4038759b4a310116d82b03` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/topology/processing/TopologyTransactionProcessingSubscriber.scala | 2486 | `e141ac3cd498623966a53bea0f06150df0618e7793f59d5e7aad4956a5a4ef25` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/topology/processing/TopologyTransactionProcessor.scala | 21510 | `cb297a723eb502cddd1aee21501517ed7c2cad41f9f8c557de5df539aa7c1100` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/topology/processing/TransactionAuthorizationCache.scala | 13769 | `ef1ee812b56c9f184d0af4138444ea28ba18b97455d6dd217196b9d1b8c09693` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/topology/store/TopologyStateForInititalizationService.scala | 7239 | `8e2ab2ab9fbb640021ba40d884abd6078ed763c4f19356dcfddfaf3c2b8e889d` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/topology/store/TopologyStore.scala | 44396 | `e3189a3be2f3d665d43217c0905467df690413487a2f2c8eaa59fe1c7e9d4e42` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/topology/store/TopologyTransactionCollection.scala | 7686 | `1be1b9f4bed40a2ba939602da4c7516c7d5539a2ae651e6a6c5a35e31b07a18c` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/topology/store/TopologyTransactionRejection.scala | 23040 | `3924b3201ca3ffd39c95388c2acac2c3f94e50b82f6ecac2151a7271bd1aef6a` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/topology/store/db/DbTopologyStore.scala | 66209 | `d8e2e6a09f34f47a3474948e15a5aa539e936d2f18b041e014910aad524729df` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/topology/store/memory/InMemoryTopologyStore.scala | 33273 | `8610da52ca5899b1206f34013c98a16dffb902cbbb3bc460e81b981c2d3001bb` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/topology/transaction/ParticipantAttributes.scala | 569 | `beaf3c6ea50c9c8148df1d086432c06a0ace7c274075664b7466ac30f1e0c135` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/topology/transaction/SignedTopologyTransaction.scala | 25234 | `14b7dc942d0debd3a6a5a65351b58f4e85764aac99cc407e0279ef593a14e450` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/topology/transaction/TopologyMapping.scala | 125478 | `1da7d937914b2e48f83dcb52cc21ea1b90d81c61be262d160ae495ca9f4c9a92` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/topology/transaction/TopologyTransaction.scala | 16587 | `2c15536c9d2bb4ae75e3572a4923f5b2e6ec1709689b351163fa1cfff1b2c1f0` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/topology/transaction/TopologyTransactionSignature.scala | 5789 | `0ef0b22e9128668ef9256c4071a0a460dd3d474b53cab3b700b0000e89296323` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/topology/transaction/checks/OptionalTopologyMappingChecks.scala | 8010 | `4b47be11e474e5e711592a3d18c15b4540224ab70a043f321a247103c6b76feb` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/topology/transaction/checks/TopologyMappingChecks.scala | 53430 | `5df0b71176e6ba966a7b8030fc77a40c88d7867367fc57da3e2f7165de4854d2` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/topology/util/SerialUtils.scala | 1218 | `09269902b72ec3e8dd35636074991b8cd2104e9f0c90881c7733fe414b7662bd` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/tracing/SerializableTraceContext.scala | 3710 | `7dabf534280d3d123451e2d3c0b42318109183fb0c7f2f738aa6f763722df245` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/tracing/Spanning.scala | 5673 | `080acd0dace1107809dfad6e4db7e64078a30862fb0aa9fa40f9de2b63641549` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/user/IdentityProviderConfig.scala | 685 | `c4e52a1916817fda8ac195a1018391d612b73747bd9b68e3a61ca789fc384520` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/user/IdentityProviderId.scala | 1779 | `bc8d83d804eff7f1a27e7fe913e4a9652c28e537a7af5e2cdfa186ba01e5654b` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/user/ObjectMeta.scala | 675 | `caa3aad295cb5144258847ce5642787d5bafd54eb0934b7d723d787b34a1406d` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/user/User.scala | 1215 | `c8367e5c0ddc13cd82662136df2ff29a3a819a05076fce278c7be362a7100cda` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/user/UserRight.scala | 1082 | `ae7f092d6e810db658db19688aacd0dc0f7506652e0a2a77c6d7b7b96fd80a3a` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/user/store/IdentityProviderConfigStore.scala | 3027 | `3ced9d0818f4731b7ade869ab5203dfbf1b4343b2b5155bf7a705baee8baa258` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/user/store/UserManagementStore.scala | 3523 | `9655fee1b92553f5f623bdce9f48190b80a2425b3b731c4724a88f4545d854b2` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/util/AtomicUtil.scala | 1102 | `5c6d89ca27c5c0dd597f08d234fb49497f5e11ee9260238c44798f6c08bc756f` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/util/BatchAggregator.scala | 17375 | `5eeb52736346dc9328b5126858c077817d842da7322f17d193130236d9fcba36` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/util/BatchAggregatorUS.scala | 10769 | `5fa9d133d3636f358b76d8d13c00f55451527247af6374d58ce4228b8f42d5c4` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/util/BatchN.scala | 4355 | `c8645e58675cac4d4a985f37df90482b162b9ce668a26e9d17351c76099a15d5` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/util/BestFittingBatcher.scala | 3893 | `ccf8d2cfe56187fe5a16e8fdf7890282d8c70a457da3fd2f4c5dc6093f86561c` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/util/BinaryFileUtil.scala | 2675 | `f4b479093d20f99b584abee1f77b38f76e4f063889d10efb672c0d8acd590379` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/util/BisectUtil.scala | 4291 | `a9615f472cad3d4726daea8b6227972f592b6a13f0c8b561fcbc10114d0e1048` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/util/BooleanUtil.scala | 552 | `7d2ab8645c35958f40094f255cd7c153b1dab8e35d02e94c7129aa83520cd8ad` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/util/ByteStringUtil.scala | 5659 | `c0976d936f45f35f062934044c1d74dbdfb0156d3a0d2f1d062711904b6e0e31` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/util/ChainUtil.scala | 754 | `6039442027685d18538244c3d37816ae5d5758f84e9283629192dc990a803d98` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/util/Checked.scala | 12129 | `28f48c97c7ff5a496db155075c3e352c71b4dd57bca730f2950ea5508401153d` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/util/CheckedT.scala | 17910 | `a263ec1e0be429f1be335a004d76e54ea3eb1090885e0178372db61025600e0c` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/util/DBIOUtil.scala | 1284 | `13e10ef98e9f9a927ae74929d26a8b2f819227ee735baccbef3f431a2941aa11` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/util/DelayUtil.scala | 4160 | `016b752691f743350e7adf40b6c05ca7ca9cde511d3dba4d6c466dcb5cd7b21f` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/util/DisjointIntervals.scala | 11134 | `45691ef4b0a658c6f06edc3f72e20083158140dd9c21705d539acfabcd03f3ed` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/util/EitherTUtil.scala | 7837 | `46d741a72777701683c96b9e5886b60da0fb750ca49866152c882292da155d16` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/util/EitherUtil.scala | 2622 | `5576622f997df05af5c34106ba21de84200916dc213867210370e537e1ab7d16` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/util/ErrorUtil.scala | 6081 | `5c51a8cea973090e3836b595eb5541fa03114253ad6eaadf177d59e0c8ead5d4` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/util/FutureInstances.scala | 1361 | `c857591317a5a6b9f0ce9d75376898fd34e41186d1ad2df15b05aa4ca85b9454` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/util/FutureUnlessShutdownUtil.scala | 1504 | `b811d8d23b94e9495be20b74f871f3b13225681e33df676164fdf644be21f67f` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/util/FutureUtil.scala | 4622 | `fff38a00de42b4d700cf6a9c49cb4a664d4fa2a81482c2abfff70ef61ead497e` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/util/HasFlushFuture.scala | 5589 | `d77b47df114246a3f66e37f6934bccb0a599865f21cea4ca2d803604e39ed3fc` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/util/HexString.scala | 2313 | `1316600a2831cbc67be5cb09e57b569c45d70e1613466c87fd1f2b18c11aecd1` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/util/LazyValWithContext.scala | 2195 | `6ace22359da17f162a4174533846d832a53185eeba4740720e9691ac2b45cd17` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/util/LengthLimitedByteString.scala | 4725 | `161f01fbad9f397e9ce086e5cd5eca9c27829ac397fcad821fe71f14b41977b3` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/util/LfTransactionUtil.scala | 8027 | `9b69d829f3fb25bccfebac30d7d8bf9201b44ba85d44bfce945a33f03fc811a8` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/util/LoggerUtil.scala | 8150 | `1ef3b2fbd2729c639b43c50b5978dbafc28c87f4d8b897fc218e84a9c4685029` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/util/MaxBytesToDecompress.scala | 914 | `3d6bcb48901914ad5e0d3731cb0f073370f06183cf8037876b7eef36ac5d933c` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/util/MessageRecorder.scala | 4868 | `8c1f156337377755243f5ce878e6aae1b6072a95e063008855fe826bfecb0c49` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/util/MonadUtil.scala | 7528 | `5c3d55cdc4f4bc9d89efc5a097ca14f4c904e214719fda61c6c988db53027ad2` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/util/NoCopy.scala | 405 | `9537c8bbd4b23f5d844aaf3f314a3bf5fd1fb8bee53cd3b869485077a0553911` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/util/OptionUtil.scala | 2919 | `096286c0c08a181ced690d7197bbc419368e8a02fc09286e833e13d02fa20327` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/util/OrderedBucketMergeHub.scala | 61894 | `92bab775654e9ddcbbc9f5b30578e048e6367e617e2b417c2676a3437cf64260` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/util/PekkoUtil.scala | 100056 | `4233d269a5c3998e6c1389d854ec605cb896578c10cfa9f8cd9baf239cdf996e` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/util/PriorityBlockingQueueUtil.scala | 393 | `ffa3c1373b2e8625210fe30dcf9a8bd8ae035915b671ff131bececcc406a44fc` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/util/ReassignmentTag.scala | 5073 | `b7218e3082a75e600e3281bf95d93684008132bbe37486a8ca6429f406a83e81` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/util/ResourceUtil.scala | 4629 | `890661ca73da0e9d516727c93588c5082d034f1911e41b5e5c245e3c1367da9b` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/util/RoseTree.scala | 12173 | `a7b17fb145db596f8003fa7970366b68bedc21d8ebff5c7d678da25b13905c86` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/util/SetCover.scala | 4526 | `177529bf606e2d8c9ad13c452dc1ff0578f9fe789bfb0aafa5f173826b919c92` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/util/ShardedSequentialProcessingQueue.scala | 6770 | `1e02f3a0cbba8a00813244eea7e70a3006742189c115563a3ad9d7ae2eb27d8e` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/util/ShowUtil.scala | 5018 | `6b0645b2dace9ffae54de1ef3b8d2c8f7786db338e5e78591e875063c07dddeb` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/util/SimpleExecutionQueue.scala | 20155 | `87c5e8ba82c05f7ea1dcea20468067a435718fcf36c1d4ea5fb4da0c605c38bc` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/util/SingleUseCell.scala | 1469 | `24a19d3ba4aaf2d4869fd7281bf4051d94cadea23e726d73fed7c3bceaaabc96` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/util/SingletonTraverse.scala | 9327 | `2cf77f3142a6a924c58e3c0bd90a9cf673360cf80a13988f38f1478691c95c20` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/util/StackTraceUtil.scala | 1087 | `b9f6377570a832a284a93ae0431b00551187c4cdf3f97780c588246e5115d2d1` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/util/StampedLockWithHandle.scala | 4125 | `591e1987be33f7488e7d2f7035d81d457128a90931aa2f15cb4e8d15049ce51f` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/util/Thereafter.scala | 25488 | `ecda632e6bceac2c963fa7cc31630d200bfc682d40603869c4bd464cbde61e25` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/util/TimingSafeComparisonUtil.scala | 621 | `a92c0820b7ca023b5d1bde47fcfd93620091b6d63657c622633bfd0f9c3a829d` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/util/TracedPossiblyPrevalidated.scala | 1177 | `c1f9becc8e792af110ad2a8d9e3b67b36b902f78af7550e2e29dc1bf1a33f49f` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/util/TryUtil.scala | 2873 | `d7d5de28aff56455dbf83c930b0c885c0facbfa790f3f9601076e6e32d872f99` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/util/TwoPhasePriorityAccumulator.scala | 9221 | `99099cfbddfce11bc7aa6fabb8e5ae7b79306469ffd25d0460b0d75ae77025f5` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/util/WithGeneric.scala | 1770 | `24a5e95b9fa59ea75cf2e2e5e1f1fb6046a194b11939be3781190244f71ca3eb` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/util/collection/BoundedMap.scala | 965 | `6f70c40476b4f72ac10236fce1aee6d69dabbe193ac2bd55fe3f66dc429f0cc7` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/util/collection/BoundedQueue.scala | 1233 | `e40577ebf143880b15a21ffb8dcd62be0aa7511ec83f55515bb070d47302f7d2` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/util/collection/IterableUtil.scala | 8496 | `fe0b29502ed4287c6dd6c912fa393e20832b9fd4dc8cf9c1f6948797994e847b` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/util/collection/MapsUtil.scala | 13724 | `000b0d399d9a2e52ac90ce97106634c94ead8ee650b5206bab0e845afb2b249b` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/util/collection/SeqUtil.scala | 1453 | `ffd3a08fc9e39b3780b1a45c95605a1845153ba8cb03bd4cf2dac9a0127fac30` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/util/package.scala | 703 | `980f322e35cd740b58556d6b3239804fec9c719f1914019aa1bd6e613a92f8d9` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/util/retry/ExceptionRetryPolicy.scala | 5001 | `65994035c4e949bffbf00e5a6f3e02abad75f437814c7b243db030639cecb671` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/util/retry/Jitter.scala | 4432 | `dbc720c43841813b881749c70294a0d53c515ec0c87df8785f8ad05f5b1ddef1` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/util/retry/Policy.scala | 23099 | `c8418df2fd925fad9f53aa4ef4c2a93ead4785ef5dce36d2824e19fc86cd0cf6` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/util/retry/RetryEither.scala | 3235 | `cb8b8c174bb4e895ff7618ea7e7df390951c8939332fe0027ef5b95956da06b1` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/util/retry/Success.scala | 1624 | `7db27c271ae42760a6583b18ac74cda923e298a57fe75c2111dc1f3cbeff54ea` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/util/retry/package.scala | 236 | `824d08ea5b8632a2db0ccb723cd8f966f5c5fea2fdb297814a812990798f0c3b` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/validation/ProtoUnvalidated.scala | 3754 | `cb621beb94ae005d6c24c2a0805631be98e1ce28b360de83a5fa17bcd48ee765` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/validation/ProtoUnvalidatedSeq.scala | 5256 | `5f4d468e1be6cf3bfd267fb0a1ca42ae2b41cffaf4473d29c2b616aff9772bf1` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/validation/ProtoUnvalidatedString.scala | 2150 | `40b0b52021b3ecb63016082dc372fc4d7d72a427e53b48cb367743d3758cf7e7` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/validation/ProtoValidation.scala | 10929 | `6738c28c70e08ead69c355e180482ebbeb57581a19fb2fa1766635ed4640cac2` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/validation/ProtoValidator.scala | 2059 | `96cc35e2a24c80110fc324b1b3674d23c18756f21b256a2aa5a029814d27cc31` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/validation/ValidationParam.scala | 2073 | `bbdafe5a76208ed80821562a34a29b676ef1560c67fe33d24ca2fa1e05cc4086` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/version/ApiDeprecation.scala | 2857 | `6359cb528a3f08b04141576771f1ca6e667e79df406a064e9b287899efb153ad` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/version/CantonVersion.scala | 5733 | `281858832a5f452f4d34b4b1831dc9b07c636eaf21553aa45f9506d1d42278c3` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/version/DepthCounter.scala | 1598 | `e19d9434f26eeee40afbd436505c27195915646510d235a8598934193d06b246` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/version/HasProtocolVersionedWrapper.scala | 9141 | `91f12ec0a67acba2f88810c43eae6d977c2113c37e7e2cc4af864849f8831b53` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/version/HasToByteStringF.scala | 1121 | `1c1be57146f339590eb64c9820fc9c24c8f00276cbbfcef70e3916513df91120` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/version/HasVersionedJsonWrapper.scala | 5834 | `2a41720cb95a4d544de17638599f91840987c22d543aeab78816c08a143ae5b2` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/version/HasVersionedToByteStringF.scala | 1321 | `dc517f38d48a8b658e1e63c26ead3e00163676b51f5d7c79049e1c35e15032da` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/version/HasVersionedWrapper.scala | 16866 | `6202499362bb3bd8b570c2ae2acee283e2b6448f4673cea911abcc5af0a0ebba` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/version/HashingSchemeVersion.scala | 3844 | `12cccd1721d9fb9493e617af15e253edbb88e3cacfbb200ec89d7ab54b7f2a08` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/version/InterpretationConfig.scala | 1194 | `e619b548f1c181f576004a0ab946bc5733f04306132d88dd66eafb594e284757` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/version/Invariant.scala | 5127 | `bd884cfba2c0f6231b7472db1e1e301db53eac14eaa7629f5aa2ee2b1804d24b` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/version/LfSerializationVersionToProtocolVersions.scala | 2054 | `5dad9f5f4441f87d50af67fd8b6eee6c8ff4d4df3a161860b07e39be6586ec3a` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/version/ParticipantProtocolFeatureFlags.scala | 517 | `75e1049cf1b358d162bfd1610b764ffd196e1ac9ec24c0aaba3fd923662ca736` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/version/ProtoCodec.scala | 11852 | `85a76c5335ba110be56d800a21215af1551e24597ab4cf17908bbc231b337074` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/version/ProtocolVersion.scala | 16168 | `b3b4831c558fbba7356075432bf1e74a19942206272f72580c5fe0ba42cf1a23` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/version/ProtocolVersionValidation.scala | 1094 | `425353fc8bba2a05cddae9a0e84753636e2c290714a68c68dd5b4d4e0f924d5b` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/version/SupportedProtoVersions.scala | 7563 | `0c086c1c3e486f3783169b9a16ed503c1e33427e4e217ca258fcbb85a2a509c3` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/version/VersionedJsonMessage.scala | 2460 | `94127903342e3d5572dbdfbb2426bf2b01907cedf3ae426abde2465793a0134f` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/version/VersionedMessage.scala | 1061 | `8219153fd1338ed024048a1db603b3bf2cedf6b95df7a5c338db84dc15e64022` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/version/VersioningCompanion.scala | 22505 | `752cb7ef43a1ad8ea6fa0023810128a5fae23ad3e3e16e1ec91a1a616537f407` | 0 |
| community/base/src/main/scala/com/digitalasset/canton/version/version.scala | 7126 | `a14d3377eca087baf054ee570400001a0895aa5c5109877696bf32c390c242f5` | 0 |
| community/base/src/main/scala/slick/util/AsyncExecutorWithMetrics.scala | 10756 | `2e5eb4fbc5350d03b0b7d15234d66a54f1eac4d742719255085b991e0429128b` | 0 |
| community/base/src/main/scala/slick/util/AsyncExecutorWithShutdown.scala | 247 | `a67d859ebdbac96a9578e4a5afd70615ed92e435ef27e32c06dc9e133127360f` | 0 |
| community/base/src/main/scala/slick/util/QueryCostTracker.scala | 12823 | `07fe943df7d1ca54bfb304913850f11c4f8b6e6b518a25d6eab74580e4eba22c` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/ActiveContract.java | 2439 | `389b92a49e277bf735a8c740ab207398f2bd6a6251e16537f8992b4d771496a8` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/ActiveContracts.java | 1220 | `425938780db997be50b3e11c3d685d0f757759326237b749684fb54e7a07b7b6` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/ArchivedEvent.java | 4049 | `bdb8371e63ced1436fa9cb717538b0e81ebd82f617332e6ffa330c6aecfbd15e` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/AssignCommand.java | 2132 | `e0a0eef4d8e35e419a9deef590cb1c20aea91677f8821c57a2c8751d4b2f633f` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/AssignedEvent.java | 3430 | `be0019322589574c6b3b6b2145962300b1c77370a45032a3f41067e79bc17a90` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/Bool.java | 1251 | `3ed67095790fecb132a1f93bef21b4180b57a0474af3bf0be2c5c27d38f70fc9` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/Command.java | 2518 | `356313395807802f4b391685db62910cacea694b00613dbaf17c9ea213fbe15d` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/CommandsSubmission.java | 22114 | `28f99b38cebd6f0a9be79fa50a948abd395599511c2dd31a8159bb2d638b8b57` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/Completion.java | 7520 | `15650e880d03499965c5364993b8eb68e7accede4e773ca3ec9a963f167a1dd6` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/CompletionStreamRequest.java | 2403 | `b0d9ccfa2d54c5fb703311e7d9a4e432abe126aa5b23f2c6bb108a56ee1347d4` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/CompletionStreamResponse.java | 2693 | `28f8656bb79b62208f02cededb84721d6a42f79b8622e39fb99d0cac2958319d` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/ConnectedSynchronizer.java | 2558 | `4c52c926c8c6b9a3e98762ca86e6032e04a68f611f9ef66f5d97a670a4b68413` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/Contract.java | 207 | `e5b75d96573ca491a4d06212f77d9f7dee3725e736d31e95759404033bd21db6` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/ContractEntry.java | 472 | `ffcd6c039be21dcb9d8ad79ad03d49b421061bdce71d96e1c92089d8c4cea34d` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/ContractFilter.java | 6512 | `3a4df33297f94c7292b41e9f6ee87e729e9e4f1dcf655d8e95f5a732bf138fc1` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/ContractId.java | 1002 | `249e73ba3316fbae8e6f59b5c4fc5a6063bb61f6d7bc0290a3a8c68885f37b90` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/ConvertRecordTimeToOffsetRequest.java | 2132 | `c734dd2cc52876ee28b5bf97662238ca44b103faed5f7050d3b1678ae317ad43` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/ConvertRecordTimeToOffsetResponse.java | 1378 | `9dde25d3c557042cf9cb1d08b934532a52598cac7aa6e48b32d859413717acd3` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/CreateAndExerciseCommand.java | 2829 | `4803c009fa71b6a84edc4bde55d2a714a5b8c01ac19fc5a4df7c8bf3fd794a06` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/CreateCommand.java | 1960 | `6528609834374f2b57510eb479e36100ccd2394b1dd11e2a099c7f1cd1c0551f` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/CreateUserRequest.java | 1751 | `a3d341e0c82a9840c71db35a75459fd55a7879820c6e29f07b52b47683fbf801` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/CreateUserResponse.java | 1267 | `74422c12063acd37ea0b77b9880e66d52dc6c03a89a537404582ab841bbd988a` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/CreatedEvent.java | 10878 | `dd9da223744df465fc0c659e678ae0787f64c62ea4fd6bf9c8f4f48375df8824` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/CumulativeFilter.java | 6053 | `ebbefd2203783f56b65e3372d9ab571f1c06f6ebf850d0c138d33936a51e116d` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/DamlCollectors.java | 1999 | `200fab458b95ac9896e5c9d954f4e682e7840e902deae9ca178f78db53d148b7` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/DamlEnum.java | 2172 | `ea58818a7a3d1fd2ee8d0f8093a1f46ab94dd0963b2f8cf642bd9b5877e0c783` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/DamlGenMap.java | 2919 | `2c17528a69df51864ef02466a6ae3bd1fed8ed324789f68b80fa49b15ab812c0` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/DamlList.java | 2146 | `ef49d2efa0f09f44a56ae351196a68daa1e3a86160cd7aae7f7e72e9780968bf` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/DamlOptional.java | 2040 | `aeb2ee98b08ed9528b0332415807989900dbc4602cd5bb315026c34ff7dee212` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/DamlRecord.java | 5305 | `393123e867b29eb2030ace7aa66a8a163862b95fb8e47a2ba6e2d5de5ccb588b` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/DamlTextMap.java | 2870 | `72364dc8e960c0a52b5cbe811fcd1c120b829b81c3d916eb29e1efc0024d0231` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/Date.java | 1100 | `28e622eafb69b2935c764be726c27bdb28775c332c196330e709db5ea406bedb` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/DeleteUserRequest.java | 1178 | `4d2c71dca5935b9d397a22ac5a04d7f572e5c49442a0ddae9f9aab0896475c13` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/DeleteUserResponse.java | 693 | `ab7cadb85b0e56123a5c9a37cb7c0d4e438802876242a717c0384c2d49a4eff5` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/DisclosedContract.java | 3906 | `9cd16b6d3e866632a7f9ef01e7bf8d82f580e4972ed45df1061aefb430d711b3` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/Event.java | 1946 | `2e780f692d1e4a7cea2cf63dbf10ff0da30988123b9fc3d0f16a724afb983fd9` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/EventFormat.java | 4705 | `e338c4ecf8c5e858b7f87d87a50a9b4e8d1e86483ccda3302e2806656c2b011f` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/EventUtils.java | 595 | `59aba53e25a98bdc19cc0c6810aafd6a5c6ea7c9f2245f7c17aa7f63a0e43766` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/ExerciseByKeyCommand.java | 2791 | `dd1f6051a30a8e838fba55400b23e5d12b7114b23d6db8d28db16aa21ec45396` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/ExerciseCommand.java | 2703 | `b07a1fc8fc2cdce9296f2fb6b35e8e6158ee472a260a0347f9e9ed0555b9d100` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/ExercisedEvent.java | 7781 | `d24ed4c1bb0d8f1f708a5e78b603a2a7c1ac10942334b1ecd3b94e1bdef3b1bf` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/Filter.java | 4744 | `d2772d00c6b17a5a90d90c8797af240d12a18694025e3caf3c3d3914a05ff3fc` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/GetActiveContractsRequest.java | 2831 | `d4f6e93597e4d504b416616ea052c7bde64bc8007c0db7a2cb1f20d8f98d5bea` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/GetActiveContractsResponse.java | 3387 | `42e87d282ccb9fce26d7398abc272a1ad3879c8a3f11b6e43b32ead6c854e26c` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/GetCompletionByHashRequest.java | 1635 | `c566d55333814d939147b908e7fcdd78bb338082ab6f640bb59f76ed5f5138a4` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/GetCompletionByHashResponse.java | 3041 | `fdc31191a4f17702030f4e50a5f214b56e360be9384daca1faf8d3c9d3004797` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/GetCompletionsRequest.java | 1935 | `ea0fc5ddfed1a55dc64fbe2da23b39b8c7765b0e2d69cb94f626be620e221d67` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/GetConnectedSynchronizersRequest.java | 1456 | `d9a421d175d01aaaf1e5a7b3742413322ea8192b3d76fc69a8fb28ec427c9f24` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/GetConnectedSynchronizersResponse.java | 2135 | `aeefca5455a8d439625f3cd344f0b18615368e6ca46354b3144964e64d6305c0` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/GetEventsByContractIdRequest.java | 2130 | `396b00ecfb7bfe933fd500646bf970134cab479731a6a3823ed254c3bcf0192f` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/GetEventsByContractIdResponse.java | 5426 | `bc4285a23b2c47beae6ca74590d1183276c8eda87623e71accfd145bdec01392` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/GetLatestPrunedOffsetsResponse.java | 2631 | `07e31b83ba0a38762a805d3f0eee0a6c6c94f675eb27440f45b65ce6e34a347f` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/GetLedgerEndRequest.java | 1505 | `1c5022b730487b7335bd0c0805e0936bc50530d1795f8ba1164687749c380ea9` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/GetLedgerEndResponse.java | 2149 | `85eb25f3b093a9f3d2ab3395a82768ecfb478d3889b61091bdcdd11e36f582bb` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/GetPackageRequest.java | 1345 | `5b0dd4cbadd4de2bb54c16d39a12c1379009629f9ef9cf59524f2675c64938c8` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/GetPackageResponse.java | 1876 | `d48e9b0755e344fa69def5692cea572d83b8453d413848c28f05be6cb33fd8f5` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/GetPackageStatusRequest.java | 1430 | `7cbe75be1ca037ca52939b8346880c2523f6287ce528084f57aa6dcdd17677a1` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/GetPackageStatusResponse.java | 1433 | `a59498a38342a2f7bb75926870e7b2bff940192ff6e64390a33ebdae19f3164b` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/GetPreferredPackagesRequest.java | 3627 | `b878e05c560cb231846fcaceebfc4b01b692a79449ef99a48a9e156ed2bc45fd` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/GetPreferredPackagesResponse.java | 2456 | `bda8daaaeb0491c110d53096632ddad5c73fa509723646760dbbff48909f05b9` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/GetUpdateByHashRequest.java | 2025 | `4fe9136e47dc1d00734267d185a884e38179c472be2249f5c86c53e74495a1e9` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/GetUpdateByIdRequest.java | 1849 | `bb4db73d68f40c55cfd2f3b6c4a6a6db1cdecf7fd1797e915b9244721f9c7c7f` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/GetUpdateByOffsetRequest.java | 1847 | `cd54bc74ae207ceb7ac7803ea7e7af787b50f288436276811e1c7164523a1ee0` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/GetUpdateResponse.java | 3412 | `6d1480d2a8c9e836b5604c812c8fd4d6bc193c79be0d70828d8df8c0eb0dfa81` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/GetUpdatesRequest.java | 3158 | `70d0daa967f8b8dc27af707fed95eae948a88667c0ea31480e1bcaf5bbe87a3d` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/GetUpdatesResponse.java | 4314 | `a891c2756c08c964cad5fa0e12a8adcb018fcdc621b900a3b715612d1c58bb6b` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/GetUserRequest.java | 1157 | `e3ce29cc40981eb224c603c56594e0585480e5072aee36961162b5d6ff44807c` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/GetUserResponse.java | 1230 | `31d6104f113a98c60d5e079a072f5b0474db3b123cb12ff7a71f1033d241537f` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/GrantUserRightsRequest.java | 1694 | `0814e954c6d670d238a11aa721e18e08de893c0bbf286ccd6f7844279f81e845` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/GrantUserRightsResponse.java | 1594 | `402460c78ac99aa719868b7ca6c8308a92040c1e823f6b8856564ad1d50ab52f` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/Identifier.java | 2357 | `5ec2579cd02f5d7619c206eaa732872eb06b0f1331c04edf92893c8b05eefef5` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/IncompleteAssigned.java | 1560 | `ccf622e261dd29945528ef28dd5e8b14bdd2934847b6328607999554b8017c80` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/IncompleteUnassigned.java | 2102 | `e20c9dabff02c5d7cfebc0512be646b18df95082cd61753a742cf17952fc4437` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/Int64.java | 940 | `bd17f3b156a7f8990fa355acb4464eb2af31d99ed73a113cf75896f1e9173147` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/ListUserRightsRequest.java | 1206 | `d2937b3450a2da61ea589874cc4a90cce4e6dd8ef7f30dafc43b5e5a8a3069c0` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/ListUserRightsResponse.java | 1416 | `7240381fbf231c830ca72d6ffa1a98b116a0f52502a10319919c94ce714129a0` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/ListUsersRequest.java | 1618 | `f73e4be8d4322d9b0b19230fd8299134434e2f1fe656799b5bf317a99790ac15` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/ListUsersResponse.java | 1340 | `e2be8fb1de9bf709ad285d485d4434115dae0149e39196567b6ccca080886ad6` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/NoFilter.java | 512 | `797edf48089d33f19dd90e4beb71965ed230bfc089d2b60f7f9b29631cda40d0` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/Numeric.java | 1224 | `9ae58ff3a0443d67cba776caacf23e8007fe5356141d2f67e59215b822eff1d5` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/OffsetCheckpoint.java | 2170 | `b6da63ad1260ecfc8bf10e8621707007826bf1c537e4350bc20b42007d8e686c` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/PackageReference.java | 2344 | `30daff31123c3e0a5b1863155f44919f521d9df58eb0c5ac4e4fba3777879c28` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/PackageVersion.java | 2117 | `6b565b5f950240f2902139033b71e0ebb5b3dc4abc9a14cb1af4420e3dc9ace7` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/PackageVettingRequirement.java | 1925 | `f514b8198becb60b95bd47010ae06ee07c76dc0af93c3deab6aaa8f71219df38` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/ParticipantAuthorizationAdded.java | 2499 | `da98834c51dc6ce89ccde77cbaabec9595c34d80c24827183fa5e4b05f2710eb` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/ParticipantAuthorizationChanged.java | 2521 | `536d80db77be4595b83b4a1a17e2daca3e145a3e99a8f450c7604478c0099cf1` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/ParticipantAuthorizationRevoked.java | 2013 | `dfc82581e231f46a570ad99f994feb7bff55f11f24c6e576e5cc70fa61ad71ed` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/ParticipantAuthorizationTopologyFormat.java | 1664 | `cdc19ae8e5b1ef2cd8d430885e0aeea75b5e5c22de28659cb33ddecb10fbfaae` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/ParticipantPermission.java | 2975 | `0036538e90edcfae5499d3333c943472fc76fdea447257bef25cc433f2758b3e` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/Party.java | 1053 | `997d20286d5d226a8f6f21964aef7e0ca99d9dae3eb4bfd010cc783fd5c46255` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/PrefetchContractKey.java | 2182 | `3152edec9431b6d31512bf5aad47ddafb480e7554ae40b352d09328e351e0141` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/Reassignment.java | 5102 | `05813dbd7e6637e7a6c3e23c6bb40c9b22a7752309290fb202f633d718852a57` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/ReassignmentCommand.java | 1906 | `c34ab7cfabefc033922ab9ca51173141f439411beba1fb6e5efe8b8ad2c80d01` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/ReassignmentCommands.java | 6947 | `157a53d0bd7ee0e512b92e2dbc1e010d0612f7337f9252ce9a1d8f01b94b0214` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/ReassignmentEvent.java | 1404 | `1d4fd298dd23e41f9c5e6a568547e530b556d312b6b357547a0912e34ff6b3c8` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/RevokeUserRightsRequest.java | 1701 | `b6e69d55bd411ad41d64832122fc8275470076072a941a58f52accff9e8c0c0f` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/RevokeUserRightsResponse.java | 1602 | `bef6dcb0bfc750841139171bc4464ad365493bf335fea20718d3d33b72e18e30` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/SubmitAndWaitForReassignmentRequest.java | 2649 | `3217797d3f89cdb53b53b3328c0d0390cdbe79d002bbb63a083d8a851c401535` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/SubmitAndWaitForReassignmentResponse.java | 1758 | `e786f2ed792821d8329f24a2f450b1dd70e74de2bd2f5bb0b15a20a24328c238` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/SubmitAndWaitForTransactionRequest.java | 3147 | `3cf19bb9d5bded58b344b4ff7d96398b8b26e0ccaffbc75412aa98aae9b60aa1` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/SubmitAndWaitForTransactionResponse.java | 1729 | `7de98de00d3a4efc8799bae5ddf5a2fcf57de6fdbe4ac637d34668962db027c1` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/SubmitAndWaitRequest.java | 780 | `f21576b39c7b5b4f5c49e4f80c1717cc5c656aa9417c5aece68a3c6c77bfed4b` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/SubmitAndWaitResponse.java | 1889 | `11f49411ce32a704dc3e0d5b8ba0e1279546dabae94e708296f10cc54cc5f489` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/SubmitReassignmentRequest.java | 864 | `88ad5e363e5cce7add49f35cda530d775cafc5c75905aa2024d62c2007568e35` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/SubmitRequest.java | 792 | `de7a20b8edb8e50af0e98b274fbe72754b1c4f3225849852a4dc8f9ccfaeb2c0` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/SynchronizerTime.java | 2167 | `6ca73a97fa37df5e00c510f6bf68bdb5a2062d7f4f8b7b7fca700f7d47bfe33a` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/Template.java | 1958 | `e809c535a0a366cb5ab8beeb7bc5206b7c7fd588b72c3e97a69fedaf3548e939` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/Text.java | 1045 | `d8940c8e9843a036d52c2bcca788912772f5851bf5e7acb324a1afc6055228d1` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/Timestamp.java | 2429 | `213b9750a3b808a4646435e1e7a9c7ae7c0285331bcd6a3bebe307756bd21e99` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/TopologyEvent.java | 2343 | `a095876ed527c1289fa7937babaa63cb2ee80cafa1e0da327a7dc63d0bdc48d3` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/TopologyFormat.java | 2455 | `48bfc1a175d939229e46f3daf3c3f29997b32aeae035de28cbbd4ceddbdf3ef0` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/TopologyTransaction.java | 3968 | `dc4cd7048d95c10aa9b1dea6d1663317acaebac77f81603cec4e3e94b59d5b74` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/Transaction.java | 14462 | `6b6b0b7b585c5c0e50d4757b80bf33ed29914bf6a50b91895ffa6b0df9186987` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/TransactionFormat.java | 1995 | `617c6558e0e2e29cd4c74297fd28fc17d32618867860ec84bdb9bf0e65914fdb` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/TransactionShape.java | 1075 | `9d6380609084cf5d8f880aab584858a3b16f33f784c9b7b69d6284f1f98006db` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/UnassignCommand.java | 4315 | `c72e9c76d1247b02f56a763fede1ae6c5fa9b155b0c33ab92bfe8b6be513e47c` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/UnassignedEvent.java | 6093 | `d1b5c73b27c02fe0e47534df0e455d60a2cc5b5dae93c7651451a85a296f931d` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/Unit.java | 791 | `220f923a803b1a7e37db3307f07543730aca6ef85492531f758ec905d514154a` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/UnsupportedEventTypeException.java | 362 | `f8e89a9b3b7cbf7929e3644b1fd418dd20df9943975d9d2ca8ca2de7bff1b9ae` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/UpdateFormat.java | 5085 | `ec81c410242a286e86c4a217e4d5c9d7a22c0f34d4b0ec471868d6c6e935c41e` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/UpdateSubmission.java | 12881 | `e06233d82472b8cf35a35b81fad10836d9a3999f6a47608a3d6b47bb8ae7de92` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/User.java | 10504 | `bb76041fbe0ca355b985e41928638dc1cc5ab91101c9b2ec87d165147fbf6f5f` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/Utils.java | 1419 | `7839ba22b52bb768915cc8a69501e8100165fe40af0049063296d8016cb93afe` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/Value.java | 4443 | `2ffb9781c28dbdfe2b8ef00038273620effe0ce89f637403a6522f42357feeee` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/Variant.java | 2699 | `d213ff7d54797a42402357c46f13d13717ccfb1f9ca59f883e9d828560f03fca` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/WorkflowEvent.java | 340 | `7ed9155c49207068c96737f0d8b2a22cc8c9d8c594537fe5100eacd7dbe38f95` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/codegen/ByKey.java | 2308 | `475481ecf2c5175e23deebeffaa1cb25741b62f36561249bd1c9810fa982b065` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/codegen/Choice.java | 2956 | `a2e3efe29cacdd1d4fff8ed519a2d68efb1dfa6b5a3924375b2f29fd13607f57` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/codegen/Contract.java | 3065 | `11596ef0168a78859455cb90b7b5e89dffcc7a7e55c4998aad22e3964efa7011` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/codegen/ContractCompanion.java | 13898 | `d601bfc82a9b13d82eeb1a9a6ac84f328bf07fcec5a5f657184d1ce372e569c3` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/codegen/ContractDecoder.java | 3524 | `b72b4e91cd35b52cebb8289b73fdf4f5d1cfc03f7008799a7de7c7e1ca5a0443` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/codegen/ContractId.java | 3060 | `341abe04c44980eb2b9b42124ba584148372fff0b9b4c118d1f814281a5b798c` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/codegen/ContractTypeCompanion.java | 6099 | `dafeae50656eeee4765b44f9078c50950c2f7d085ff568761582364fbe118a95` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/codegen/ContractWithInterfaceView.java | 916 | `7646a0ff7a08d9ed0c3ab67d08746b44025c23d2ceb1c3a4bb626da8972815a5` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/codegen/ContractWithKey.java | 2257 | `9cf1e0ab87e491295fae480054264c84c0673aefd7938d34352db4ce04d70aed` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/codegen/CreateAnd.java | 2137 | `3c31f931a23c2e98e4f833de16b773c235a8aec8d8fd2ec900cb83ec4afda443` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/codegen/Created.java | 978 | `e54171d9c6a697dd9a4d34c39d48d38b0a7f7c7be30fe658e1f2b4ead689ff9d` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/codegen/DamlEnum.java | 573 | `48922b56034ba55c6f84111d88ebae97569eabb4218dcd18ebf0b213d2b6788c` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/codegen/DamlRecord.java | 861 | `68fef5203fc0808482938d0da22ba86ab9000bcc8b87b0d2b8f76d781d3e7a02` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/codegen/DefinedDataType.java | 982 | `590759c6fdd2eed0e16f169cb468c1ad043c9a3f089e4e4e84201669948c9383` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/codegen/Exercised.java | 949 | `ef2d2cc7f69389ffc85587aaa579a52c1c9f6676e57fef0cca58402432bea805` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/codegen/Exercises.java | 1632 | `6bad5e663c72874f46d7ae076a55040ccc197ff96c5b38f4b7313331acca6f60` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/codegen/HasCommands.java | 733 | `6a330dc2c8151591d3fad9856963c5e69e745c967cb6459f29aec59470beca91` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/codegen/InterfaceCompanion.java | 4572 | `945450157524cdfec03b2cca74f422d56571aefc95b76e38ef65d6a56925f936` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/codegen/PreparedRecord.java | 856 | `97c8cca7e81464152f4304b682d41ae31a846c1fbaf002fb0b3037e99e07520b` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/codegen/PrimitiveValueDecoders.java | 10989 | `390178c6c77f516b76e176055e66c65cd0c840f71c6189f0251b48fd3cc8b272` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/codegen/UnknownTrailingFieldPolicy.java | 490 | `8f696dea72d91ea02fed8241e13fceebe337ffa161c21addb71e1ec2790c79c6` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/codegen/Update.java | 3738 | `1997e51fdf5377183d4da4659e193492e9d8d9af10d038823464197ec86ac525` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/codegen/ValueDecoder.java | 5176 | `a21f3b62d7227a03931e6008db9c4bc3eb673d832ab4f1ed554543da380a1e72` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/codegen/Variant.java | 632 | `c53c0a4ac516e45c5d366f300c22c3207893c29c7920a8e33ace69bc4f79af28` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/codegen/json/JsonLfDecoder.java | 2170 | `f5c33bffd7816c3b120f63c54cb4b7e448347be630f3a61b2469e2bce49fe61e` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/codegen/json/JsonLfDecoders.java | 13922 | `623de9dc9994a58eff31a1f3c80a7a5efbb056f3187e6788d12b9e98519dcf84` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/codegen/json/JsonLfEncoder.java | 667 | `95429a42a0806a1689a19b3e985a839564407a5d2ded2f888e0a1d8b291c9868` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/codegen/json/JsonLfEncoders.java | 6550 | `5a12b91e546c1168756704398b991138da5f4f5aa09e2fbb3d890636da760325` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/codegen/json/JsonLfReader.java | 8047 | `84a348a43df5a116a0b5899e8f80b2e69bf52d436f6e096cf009060b24306a04` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/codegen/json/JsonLfWriter.java | 2197 | `a1347fdf2eb8b79c6932108c55d38cddfa0365df3662cd02b80ccaf8fc6d7652` | 0 |
| community/bindings-java/src/main/java/com/daml/ledger/javaapi/data/codegen/json/PolicyBasedJsonDecodingFunction.java | 742 | `5617688539fec7a3192af884a1646c7980e6c4960bf81eb096aac1740537a7e9` | 0 |
| community/common/src/main/scala/com/daml/lf/CantonOnly.scala | 878 | `88c3bf1cab4171469bcb661fe038daffc7bcf833ed514c75417da16dcf34615b` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/admin/grpc/GrpcPruningScheduler.scala | 4990 | `657855be7eb8c8d90c67a818eadf1876b3159ad1fc27af9a88cbcb0315b9271b` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/common/sequencer/SequencerBasedRegisterTopologyTransactionHandle.scala | 5898 | `8e0a2116d8a44617ca55e0efad6399e68223108eec7c7e3dcdcd846385f4d5d9` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/common/sequencer/SequencerConnectClient.scala | 4265 | `2e6579dc1afb1e193adc180ebebbfc0fd99b4ba9f61ded66132c7b4aa3ab7a27` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/common/sequencer/grpc/GrpcSequencerConnectClient.scala | 11585 | `a69578badd7470e02423a743f82d8fd3e0ae7f8e7bbcd1b9445af06a3e5c8d16` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/config/CantonConfigUtil.scala | 1430 | `f5e59ec1e04c28bc4601e2dcced6ed7b1c376282a66a94065ae760087833744c` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/config/ConfigDefaults.scala | 2214 | `b1acd8bee31de0e909eb764227507288c36269331de1b5fe51233a5f0185f013` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/config/DeprecatedConfigUtils.scala | 6615 | `cb2ebd93918a485fb0ab7ec94696e83988d1b156803cbd74a776eaef257be91d` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/config/InitConfig.scala | 3565 | `a8d031a00087809c7fe747639abbfd6819745f407c60b6572feb796ed7c6537a` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/config/LocalNodeConfig.scala | 1149 | `a591f743084030037573d4e4da0a535c9449a401463acab03bd9de60bc200a78` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/config/NodeMonitoringConfig.scala | 2709 | `598c98b7979311de5171ee0878cfe256f2b3f33ab56cd73a28a37819ad20bbd5` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/config/ProtocolConfig.scala | 344 | `d628ff1172c6cee219f202c8207547bd02a7e09b50c64cb61716cabf85ffe110` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/crypto/Blake2xb.scala | 1382 | `4edd24c493dd891a9bd08f1e9d68f13dd6f069badf24d948fb5cb65c01bad629` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/crypto/CryptoHandshakeValidator.scala | 3065 | `4509ee652401f21ba3432c6ae63b8e7348fe641ce9510eedde35ac148f58d128` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/crypto/LedgerApiCryptoConversions.scala | 5590 | `4373bb92594998d416c7cd6f532be6b23506f29b36f56feaf66ad2d96eaa889e` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/crypto/LtHash16.scala | 3516 | `463882f9ef7bacbb83be129a9c1491f8ffcc9079374fc73afd1bbb9b36ef67ad` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/crypto/LtHash16Blake3.scala | 6751 | `546492e821da9663705691cb69d993db7b7d673751e717fc0bd1eb06f89f2b0c` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/crypto/admin/grpc/GrpcVaultService.scala | 36689 | `63a962491a98c55c570a30d3cc1977a9f45645e11d212866c2982e103eda6d92` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/crypto/admin/grpc/PrivateKeyMetadata.scala | 2792 | `2850780f1629b6cfbe355f569fd1a932934161a41ebefe3f1177631a853c09d1` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/data/ConcurrentHMap.scala | 2345 | `eb4b03424df1268d395fea5538d6903ba704a0ae842218b88fe134d59aa69e0d` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/data/RollbackContextFactory.scala | 8493 | `b87124fb5bca0dcceb4c33687c7359bbc40675db2b11cd59b0abc40945bb866c` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/data/TaskScheduler.scala | 22074 | `26384c852bdba66fb458d7eff5200a30bc1ab83afe2fc11339223a0ff2653b5e` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/data/TransactionViewDecomposition.scala | 4089 | `fe33d599c7dbc67970215264b44742303dc1ee1f67141de8b519e3637d940959` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/data/TransactionViewDecompositionFactory.scala | 15173 | `2d203a1ec9899759bdddd4874dca63fd40f22823be2542c20f6686951248f43b` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/environment/BootstrapStage.scala | 15743 | `9ce0c2ddb1d17ba95172cf8748659630d4b535728177023f8c02c647c449c179` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/environment/CantonNode.scala | 529 | `e3a1e1be3101cbc8204523f9f0511dd65c28b817e1b83ff4bf93f93f7e186465` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/environment/CantonNodeBootstrap.scala | 48566 | `fb10af8c642c6bdb1d9ac9ccc05026083844278867a54666ad1da580f06fd37e` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/environment/Errors.scala | 2809 | `18cff38d3ea4434fa75148120fa3ba6354de09e9b858e4c6c6d5d9739b5d8d54` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/environment/MemoryConfigChecker.scala | 3264 | `28c6edea87a66924fa625e7a69381f749679f4a85ba4df7d9c7a0efd0159047d` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/environment/NodeFactoryArguments.scala | 2308 | `ddbcee9fed74c1e4ab50a6c27396d6ce5ccf81cb4f113daf5beb669078c858fe` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/environment/SynchronizerTopologyInitializationCallback.scala | 4504 | `656dcba01387f8d794d36a767a257bace6809146f05d87768b9a8bbd36db2775` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/health/GrpcHealthReporter.scala | 4325 | `84c63837ae4668912e16537d826a16fb613271093f09bca14d992928bf18592c` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/health/GrpcHealthServer.scala | 1762 | `1bf984c6074565bbfea046990d1d4dfd35893f4c6c1e68b02699055a69d02889` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/health/HttpHealthServer.scala | 6503 | `8947e62d86cae988d2d5ef0df55fa658321d5ae0880ccb90e9795f4a6cf7a4a2` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/health/admin/data/NodeStatus.scala | 7537 | `3fd642032382028a7888262fee5b1ecd8147c5f232d440acdef197ab9110cae8` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/health/admin/grpc/GrpcStatusService.scala | 1831 | `0cf01133534648dc920d764f1c4229a092b30749985ba1735078b1791b3fcd4f` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/interactive/InteractiveSubmissionEnricher.scala | 3415 | `0fe4afff1479fc257d6b3ad3e659ce58f1d370d4da8b0d126acdb1f6a70e12d9` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/logging/CantonFilterEvaluator.scala | 1662 | `77cc98dc4e9547a8c22394338df7a857405937c57b3d071079ff97e4d5f58d3c` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/logging/CantonJsonEncoder.scala | 726 | `0c6d15565f49d7922204625d399eac85b00f47edfb013eac66cd48fcfbeb86e8` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/logging/NodeLoggingUtil.scala | 1447 | `5cdde486861ba101c400e116effdb2d007ceba4f23db09eb44dfa2b9c88b7f9a` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/logging/ThrottleFilterEvaluator.scala | 3671 | `7f1fb3771c9eaaa569c776388679b6e486cb51bbc66cdcccb5ce23d21f2c74ab` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/metrics/MetricDoc.scala | 469 | `8a1d8a71ca6fe0f999d7ffe8f66b7d2c526ab2497027b49f323324f3c5a44e5d` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/metrics/MetricsHelper.scala | 1020 | `3abdcec4f8438dfb73585b7d83ca1f26ce95011c8792cb5c897fa68e45ebca9d` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/metrics/package.scala | 3384 | `361559b31ba363707f4b8132044cf2aedeaa45b6713f181ff1d3f398711b8dbb` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/networking/grpc/BaseStreamObserver.scala | 905 | `57f0aa01b0ad5b04e48621e159c15ab306deea3ce58331a7a8d319812bc8b49d` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/networking/grpc/CountingStreamObserver.scala | 889 | `ddf33377511461e7f61b99d04696e384249735892e309bc00fcd0af429df2945` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/networking/grpc/ErrorLoggingStreamObserver.scala | 1051 | `e4532f6391fd583ee6d5db26479b1f1a02dd5d4e2f84628058957e3676fa6da7` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/networking/grpc/ForwardingStreamObserver.scala | 992 | `41315d5587bf3e5c74e1e33285ce0d36297de31540d68ebc0e6c7ef91a7c5dee` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/networking/grpc/GrpcDynamicService.scala | 3354 | `33364507c3017a972d9d1cb9d76fdc39d92d0f78056df97ba0a188eab5736646` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/networking/grpc/RecordingStreamObserver.scala | 1371 | `b82e2a8b895579080d762309d9b174e9dc559d4875c7e3dec84e4e190aea08ad` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/participant/ledger/api/LedgerApiJdbcUrl.scala | 9806 | `075572209e4f87235ebefb1f92aa665d95a53a2b0b94cd576f097da5361523cc` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/participant/store/ContractLookup.scala | 5276 | `f3d7a6fd30ede5ce40aeee406cb779dad74f24b59042eb6487756d704f19cbe1` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/participant/store/ContractStore.scala | 6990 | `27e8d8ce0cc3442961c19d3eaf1601164204c04b7bf5a5a3192b2b79533d5f84` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/participant/store/db/DbContractStore.scala | 27323 | `4e2fe4ac06e660c92c24ae63b99975cf7d446964914108d173a74c5c0d49bafd` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/participant/store/memory/InMemoryContractStore.scala | 8501 | `95c68c46bdef5a14c078c3f5217417527fa2d7d2be590461adfc0a8cd47ac802` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/protocol/ContractIdAbsolutizer.scala | 9364 | `01cec4e1f65511a1532491715fa81a0616580968b998a68b19335dcfff18b73d` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/protocol/ContractIdSuffixer.scala | 3625 | `ffa9260f4a2e6a9fb401f3e274b7b3535a294ea20031573c0c6387bbd44f21f5` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/protocol/ContractSalt.scala | 4043 | `7765951e083b4ef10f853b5ffb81a505c0c772f2359c08d69cfc2a21c378c88d` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/protocol/HostedOnboardingParties.scala | 2847 | `98ca57efbc79161a66f6dd2b3541ee7c0fe73d8c4e940fe9e415e791eb4f2fe7` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/protocol/StoredParties.scala | 1958 | `c329fbb850adae5bcf97ecf40d0f24ea7015416a6f6dd029187bdc02e0bfea18` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/protocol/TransactionMerge.scala | 12720 | `623d9352332edb2e4b8c0b174dbe31e7db9d7bec07d88bb7d8589bef720d3e51` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/protocol/TransactionMetadata.scala | 1624 | `a4e3a4acadae2f7c7dcce22e49d320d9f87de2746f2adab2f9b1b39e06c2e164` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/protocol/UnicumGenerator.scala | 14054 | `2d518a10cedf0da920afce85375a78ceb73a1bb9b50bac1c1b6098420d6e5be9` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/protocol/UsedAndCreatedContracts.scala | 2005 | `d0d32ba063b30df5fc88d731dfd98d0405459579f6a402761c014db4f26ae7b8` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/protocol/WellFormedTransaction.scala | 24706 | `2486fa637e6d02a9ed72d847649d42898dd1e59444826127e7437472633c0108` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/protocol/messages/TransactionConfirmationRequest.scala | 3620 | `ecb098850726bf691c0b896ea8d95093f4dd88cb6ed2b79cc301ee6043d483ca` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/pruning/AcsCommitmentConfig.scala | 6713 | `1b2dcba8edc7f7ea5d3f66d39d509da15bb709e27b0500483b53a55e64a7406c` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/resource/StorageDebug.scala | 8204 | `6f520915a36d31aa73e0d45083981a77fcc3886fcbe77b46fcaa47d66858b897` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/scheduler/HasPruningSchedulerStore.scala | 2192 | `2fd7e0cd28fd94df6f0443ab8bd34a805f1dda9b43985942fe0554733a1fe395` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/scheduler/JobSchedule.scala | 8563 | `5c3bb59601b771b791c083c0e3ebc9014e4f4eadcadd2ca448705b3cb20f2d98` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/scheduler/JobScheduler.scala | 9164 | `379f733593acd955d02afe5ff8138ba760d7c020f764d82941aaa476f0189520` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/scheduler/SafeToPruneCommitmentState.scala | 3209 | `554d3fdce9f570c09ac368d7710acc0b54816ed2a9500b24efbe12b960a13993` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/scheduler/Schedule.scala | 4977 | `a742d9a7c6ece084983f79bd7d57d26195d8c90bd93c06b93a9fd4639d5b8793` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/scheduler/ScheduleRefresher.scala | 1010 | `899522059f62f537e9a076566fc5ae76415af52f9f1d0c3167c12a441b492d20` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/scheduler/Scheduler.scala | 1971 | `548c2762e697685ec9ddcafaafeab34dbf35710a0c017c90c993fbf206ca00b8` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/scheduler/Schedulers.scala | 503 | `f692e568154a43a9999e2bdbd66606e9850a8813309a5d36e5de3135562c3f32` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/scheduler/SchedulersImpl.scala | 2387 | `961f1e59a4f47d87745ad6f96e8d4e3b91567abcd1b7eb7e4123e43d4cf69557` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/scheduler/UpdatePruningMetric.scala | 1249 | `5ef1a9cce4c158d45169ec2d13cac99a76a4afdff5c1e7282312f138c4e41ca2` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/sequencing/handlers/DiscardIgnoredEvents.scala | 3077 | `bce62df87ca0bc221da184326b1fa96e217a5a8a6ee93b5c60ff1252d6ff0e2e` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/sequencing/handlers/EnvelopeOpener.scala | 3026 | `25df0387b8bdc6d0a4763ba2121a52b4df85f08646995314682384fe6788bb71` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/sequencing/handlers/StripSignature.scala | 871 | `839bdfe9bc559299f0d8cc16d43633c5b4714c129a1bcc61180e3aaac0e0cef0` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/sequencing/protocol/WithRecipients.scala | 630 | `77f45bad4accfa40da6e744206f42ab87317fde7f70f6e8e64ec12919c957483` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/store/PendingOperationStore.scala | 11674 | `e065b558de165f95c083a4a94862faec9da0392f0c275f3cb788160b5dfc0ef4` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/store/PruningSchedulerStore.scala | 2578 | `ea43e160ac7d7d482514322252921edc7e6422201c5ee5ded6a4def7d780a8b4` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/store/db/DbBulkUpdateProcessor.scala | 7614 | `34e32b48abfc6f1a008aa515e0bf22027bfdb52a528d6cca147172714e408c45` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/store/db/DbPendingOperationsStore.scala | 9816 | `d236c5d8e595135b0f2b7f98a772a1dc3aabd3857b615f57f5e855ea99a7d9fc` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/store/db/DbPruningSchedulerStore.scala | 4989 | `68e9032ec87a45fa8081c109e416240bebda589e65a821c237018ebc75e339f7` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/store/db/h2/H2FunctionAliases.scala | 488 | `81565930cb0f105ff2d26269db87978915e4574ab1e41f85425f510802bd488f` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/store/memory/InMemoryPendingOperationStore.scala | 7301 | `2ccdb27ca0802296d96464a943e94602799b520edc12df287b7c2006139de5d5` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/store/memory/InMemoryPruningSchedulerStore.scala | 2614 | `696ee4701a738ed07d6eb3643e3deed412478fcc7a2093cc9ad15c39a32452d4` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/time/GrpcSynchronizerTimeService.scala | 6157 | `b02a1eac8c89ec5a00e854227dbb6efd57510df7903f935d440df371b46ce1fe` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/time/HasUptime.scala | 435 | `14cf31bb7db5a12e4130a0ee2434265fbc214c49ec1699b7ff11e1b1a559178f` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/time/TestingTimeService.scala | 1528 | `32d38970f6284b26362767e9a33ec13846a791220c93a04297cb616227f158f1` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/topology/GenerateOnboardingTransactions.scala | 12566 | `8e9fc44d29ad9ab059e93d1ff4965c66c4e3badbf30d8235345b60ac9120520e` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/topology/MediatorGroupDeltaComputations.scala | 3255 | `b7ca0191f73bd8f2c114a019d1426b69e451e49765c0cebca19a28f39e490335` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/topology/PartyToParticipantComputations.scala | 4012 | `8194f66b82a8d00401f757d5edc787a5cb73aedbd218458971d9317160f5ef66` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/topology/QueueBasedSynchronizerOutbox.scala | 14859 | `f60614c06b687f49faec78e7ca8528e53d05e80d95f824501d33e2534c587c86` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/topology/StoreBasedSynchronizerOutbox.scala | 22380 | `487114f139d7c7161165d1de0ee02cdcc5a878c7ca8134887d7ab4ebaf31ab89` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/topology/SubmissionTopologyHelper.scala | 3791 | `1351593416f6df25317d716b3a9386adb9b52083e0c64f4ae76d10fec077cfcc` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/topology/SynchronizerOutboxDispatchHelper.scala | 7190 | `5837197a484bcbccaf10f910a343d4d935dc456ec1770fc2e9bfc6286fbac6e8` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/topology/TopologySigningHelper.scala | 3398 | `ea213d3be66b0e58b56403bc2e1e8a0c3cc23611eacb9d4127d7b0341d1e5162` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/topology/admin/grpc/GrpcIdentityInitializationService.scala | 5186 | `c7e844e0ca2cd849c08c3019047320db5feb49fe997689ba8e58155f37ccad24` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/topology/admin/grpc/GrpcTopologyAggregationService.scala | 12534 | `fee0194edf4478185390c564126229c1c8b29dd05aef3b2561775aafcb3fc8f3` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/topology/admin/grpc/GrpcTopologyManagerReadService.scala | 54327 | `0b1dbc19c31c6d18e51def0984d045f2656f7b13d594cf1166f3d7b0105bfb5d` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/topology/admin/grpc/GrpcTopologyManagerWriteService.scala | 25995 | `84193e1f9922461ac0b7fd785e35ccc003301ca9f2f62aedae31f735e7e3dc60` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/topology/admin/grpc/GrpcTopologyServiceUtil.scala | 3422 | `fab4d3f87cbb25b89a3a4c25cd61d0f566ef0808dae4d967796eb8d27049f8a3` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/topology/admin/grpc/TopologyStoreId.scala | 7109 | `85fbfa2ac34a8fced4b38da2cedcac90512fc65964dd1dbd0af2016308aa1370` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/topology/admin/grpc/TopologyStoreInitializationStatus.scala | 4061 | `cd3dfe24a8c1f19b5b014c56f4ab1e14f0e3468436483a3febba0f097378a99b` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/topology/store/InitializationStore.scala | 4476 | `c9a056b4d09e05918bcf2f5e1954635f9fbe359e709bdb524cd9d28e8671d127` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/tracing/BatchTracing.scala | 597 | `fa90ece19101416369b31ee732e01ccbf9b2e2c3f383390574f787d34e9d8697` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/util/ContractHasher.scala | 1733 | `1b7778e36ae7273b5f3c66a0d757b372a81a3adc9f278d7cebe7508917879110` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/util/ContractValidator.scala | 6014 | `f65e8b8c1551c17d89b4b8106b6a4f4a5991d6c339fe0f011a24b25ccd32d3ed` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/util/DamlPackageLoader.scala | 2110 | `93a6584b1deacb276202ad869396813150ab0ce4488d28ad65793af885c9bba9` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/util/GrpcStreamingUtils.scala | 32070 | `198b28e33e22d8ce1bb04355821c1bc096e86040dad30ae87739b9b89bc9f4e8` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/util/IdUtil.scala | 964 | `d383766c7fa41eb8c65b759b4d8a71f7a51ffdd41fbd6f22626535f52d41ddc4` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/util/LfContractValidation.scala | 2238 | `bbd3f3bf519d5abdf7684366a5e87f5cf4368292577e6fc638c1bf780fe68da6` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/util/OptionUtils.scala | 867 | `a47d38146ae130f059660fff0d36ce2bc6f8bcc71c4708332903822ab74505c9` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/util/PackageConsumer.scala | 4861 | `38ce06b3b49b69c79c7c1d874bf3c06d6582e61f5702e883a7a3cadc207a1597` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/util/PathUtils.scala | 602 | `9f1b11c88c355fa9a88276f1340fb148ba6c827c937d7c0c0d47e004f99bb65a` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/util/RangeUtil.scala | 824 | `00311bcf964513dcb4c731614a0a15873719541d3c7326bd8a964321389589a7` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/util/RateLimiter.scala | 2932 | `7cffb5841893e50f56da0df78b8def78cbd5f85489616a49609aa43a2d8b9545` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/util/SetsUtil.scala | 895 | `15887832d08dbf897439b8a64321895292051b196612284c318b0949b8dc7966` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/util/SnapshottableList.scala | 1162 | `a99b2f1aeecac185610cb252f34cc12437dd6624e32df8e05b1e99c155a2560a` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/util/SnapshottableVector.scala | 2066 | `bdd275cd4b11a44b52b3235c474ad272f5b8f584d4218a1e1c17abba4747daf1` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/util/TextFileUtil.scala | 880 | `90628e5093511c6bdec90aec0d52042316a8e0c9ab6b843cedff5bea12a7006f` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/util/UByte.scala | 1599 | `6d952a19e1afb67d61c8dbe344c191615335138bbb8170ffceebd5c3f1f90b7f` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/util/signalling/EventSignaller.scala | 1452 | `b7f919453249663d195d9f88c35901861924b4711abdb75c70bf0dd3cc92393c` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/util/signalling/LocalEventSignaller.scala | 6100 | `134f659a52198df359a7e4264f93180dfddb335c77b17a5c9232b00f976af1ae` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/util/signalling/Notification.scala | 1224 | `838e531558bd197979c3b6a44135bf073b503fd7dcd9f94bcb24a6fdbaee5648` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/util/signalling/PollingEventSignaller.scala | 1183 | `8e43afb090dde955148434b2819bfbb04c00e2ef5821729fd449ca388045cfe1` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/version/ProtocolVersionCompatibility.scala | 12751 | `b9a9cc44cf4a5456923a5eb2794509e917800a8ec5e90472222dd96e07a4c9c0` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/version/ReleaseVersionToProtocolVersions.scala | 5336 | `73ae8aa42741896b23b7db6899ecae027dfba12682207f24d16128e740f0f5b0` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/version/ReleaseVersions.scala | 1374 | `8e224550aa74351034fdfe17ecfa3df6a6bbd32d78e20113efab4f43b4a5894f` | 0 |
| community/common/src/main/scala/com/digitalasset/canton/watchdog/WatchdogService.scala | 3534 | `2e2d422fae16dafde9a0c633cbfbc1a95a2b7bd33e2bcf1c25770c978f31b518` | 0 |
| community/common/src/main/scala/db/migration/canton/CantonFlywayMigration.scala | 1677 | `2352ca80fb36750d624178577eba62755612067430a2a157e63b0ae66a9f2e2f` | 0 |
| community/common/src/main/scala/db/migration/canton/ReassignmentStoreStakeholdersMigration.scala | 2628 | `6ed90a868de5d2650a03d737bc86a521d43e980ee36bc9423e47fb0dc940ee99` | 0 |
| community/common/src/main/scala/db/migration/canton/h2/stable/V6_0__reassignment_store_stakeholders.scala | 342 | `29f61f79031b572cc003b6aa37fbc5182e8b67b4370af36c5575143da39fadb0` | 0 |
| community/common/src/main/scala/db/migration/canton/postgres/stable/V6_0__reassignment_store_stakeholders.scala | 348 | `35245bc3ffb2949584aeb658787f14bdb75c4466dbabf8482a8b16491a1c3b52` | 0 |
| community/daml-lf/api-type-signature/src/main/scala/com/daml/nonempty/NonEmpty.scala | 14463 | `ace2f7439d0600e841b78d994666cefb829d6b40f9b8c9eb2978727b61b9e40a` | 0 |
| community/daml-lf/api-type-signature/src/main/scala/com/daml/nonempty/NonEmptyCollCompat.scala | 359 | `0624caad338259e6760878a378cbc0f27ecd9dad02a93020be3d504cb95c6b50` | 0 |
| community/daml-lf/api-type-signature/src/main/scala/com/daml/nonempty/NonEmptyReturningOps.scala | 1824 | `1c22bee42b305bb5d95e93b6af27cbaa4331176349453001d2db54a8f5a57e29` | 0 |
| community/daml-lf/api-type-signature/src/main/scala/com/daml/nonempty/Patterns.scala | 976 | `418d7f4d5212761d5a2de1af74670de708cd2f48c8c3b48db7a8f1ce09fdde99` | 0 |
| community/daml-lf/api-type-signature/src/main/scala/com/daml/nonempty/package.scala | 2580 | `5f855dde2bb66ee55df67c4fa9b8737007f2ca8a50187230143ac7c18ee865bf` | 0 |
| community/daml-lf/api-type-signature/src/main/scala/com/daml/scalautil/FoldableContravariant.scala | 2568 | `e1d32a2b611c8cd8a07d04dfb7b23a09c115e66fe780a54d8d0859d3f8f71981` | 0 |
| community/daml-lf/api-type-signature/src/main/scala/com/daml/scalautil/nonempty/package.scala | 756 | `9a4d72ec27906010738088e7971cb137b37d1c201f39062fce073c9bee1d39d5` | 0 |
| community/daml-lf/api-type-signature/src/main/scala/com/digitalasset/daml/lf/typesig/DefDataType.scala | 12537 | `056a5a193ca3267c0747aeb54a5bec56d9c077189da2250ec9fe59c6d8af106c` | 0 |
| community/daml-lf/api-type-signature/src/main/scala/com/digitalasset/daml/lf/typesig/EnvironmentSignature.scala | 3766 | `f7287587e2f8497eda33ab470312e5dffb74664c96f885adc994469e1ce18255` | 0 |
| community/daml-lf/api-type-signature/src/main/scala/com/digitalasset/daml/lf/typesig/PackageSignature.scala | 10263 | `d4746397fcd7e0f9c908ae5d51e790072c6a7781e2932ba1c2969104945f4a6d` | 0 |
| community/daml-lf/api-type-signature/src/main/scala/com/digitalasset/daml/lf/typesig/Type.scala | 5002 | `a8c20aeb1d7f7e19d89a6f96319420b300b49260e701a5417a0fd921d26ad440` | 0 |
| community/daml-lf/api-type-signature/src/main/scala/com/digitalasset/daml/lf/typesig/package.scala | 570 | `0250cf6987001f7ca7991094964cef5f8c93ac7ef8a9eac2fd4223e4d966fac3` | 0 |
| community/daml-lf/api-type-signature/src/main/scala/com/digitalasset/daml/lf/typesig/reader/DamlLfArchiveReader.scala | 1159 | `6616eb4f7b150e79210acb3752558a4133f37be20a0b5c5b53dd8ce71a6d2c2c` | 0 |
| community/daml-lf/api-type-signature/src/main/scala/com/digitalasset/daml/lf/typesig/reader/Errors.scala | 5465 | `887af1ba75583a64c8910998f6d1e290fee436581d33c8b9281e305e99572be7` | 0 |
| community/daml-lf/api-type-signature/src/main/scala/com/digitalasset/daml/lf/typesig/reader/SignatureReader.scala | 12456 | `753e4be4ba90a4d3efaeb20603ef0ca4e803d2e27b82c39201b609956c96c437` | 0 |
| community/daml-lf/api-type-signature/src/main/scala/com/digitalasset/daml/lf/typesig/reader/SignatureReaderMain.scala | 664 | `347b604c52b6cd280bfcee3f2927603bf5d307878b0a616d1d8443e948f66fe9` | 0 |
| community/daml-lf/archive/encoder/src/main/scala/com/digitalasset/daml/lf/archive/DarManifestWriter.scala | 911 | `c11ec1932376496db84a9e8a30afe42a2c79170b835f6473dccd0803af452a24` | 0 |
| community/daml-lf/archive/encoder/src/main/scala/com/digitalasset/daml/lf/archive/DarWriter.scala | 1305 | `42238d1c268ce36791d63dde4f2c9481164b9ff51091ae05c31dfd48856c290d` | 0 |
| community/daml-lf/archive/src/main/protobuf/com/digitalasset/daml/lf/archive/daml_lf.proto | 1946 | `f9375b5d55701ff8953a81257b8e4d54201969c774b923196fb8afce3fa9e24f` | 0 |
| community/daml-lf/archive/src/main/protobuf/com/digitalasset/daml/lf/archive/daml_lf1.proto | 51595 | `71bf0a9994f69712f7fb93927f09ffea78985adbb838f75397647fcd550c94c0` | 0 |
| community/daml-lf/archive/src/main/protobuf/com/digitalasset/daml/lf/archive/daml_lf2.proto | 33659 | `0e11f581a2ac8ae1d5e1de4e5d27316b16988a69d3451bf81a68f1c36a5548c3` | 0 |
| community/daml-lf/archive/src/main/scala/com/digitalasset/daml/lf/Work.scala | 1416 | `9007b48b68cb11feaa0b1e1c38e0c65c5b23685a557c243f0a351f7a3876666d` | 0 |
| community/daml-lf/archive/src/main/scala/com/digitalasset/daml/lf/archive/Dar.scala | 364 | `ba890528f29f04e8474fb8f02ee7fdbe77ec0008bd82b47d17eb8b1a955adca7` | 0 |
| community/daml-lf/archive/src/main/scala/com/digitalasset/daml/lf/archive/DarManifestReader.scala | 1493 | `a4eb1890674ec3cbc7577c8467cd620eac5086ee5b478db363c5de87bdbb8d13` | 0 |
| community/daml-lf/archive/src/main/scala/com/digitalasset/daml/lf/archive/Decode.scala | 3236 | `77670241244760b335db87c9ce9bbe80eb11bb64edc6dffd71a9a7461b139135` | 0 |
| community/daml-lf/archive/src/main/scala/com/digitalasset/daml/lf/archive/DecodeV1.scala | 39504 | `fb511c03a6f9664ff9eb4465ac903741c57fa68b5eb611767e6008cfe7398ea3` | 0 |
| community/daml-lf/archive/src/main/scala/com/digitalasset/daml/lf/archive/DecodeV2.scala | 78283 | `7c8223fe352a22614f7d0cd37d4b8893561a8df7452811760a7a8889551c6fac` | 0 |
| community/daml-lf/archive/src/main/scala/com/digitalasset/daml/lf/archive/Error.scala | 1842 | `b7fa1d50073bb063a4e20022d987cb64cd4782a15870334e454940ed2263c31b` | 0 |
| community/daml-lf/archive/src/main/scala/com/digitalasset/daml/lf/archive/GenDarReader.scala | 4131 | `151a691380717b12a2881bf758fc1c83fed849b8cbe29962420011b8339ce118` | 0 |
| community/daml-lf/archive/src/main/scala/com/digitalasset/daml/lf/archive/GenReader.scala | 1886 | `149eb07532dbfe30fe991c4f0b5007ea11ee4ab5be33e3c2340f4b44912d70f9` | 0 |
| community/daml-lf/archive/src/main/scala/com/digitalasset/daml/lf/archive/Reader.scala | 3823 | `141b93ac84ba1f6786bd4c613f5e586d5f842f9dad83201c30f6e944897b1a96` | 0 |
| community/daml-lf/archive/src/main/scala/com/digitalasset/daml/lf/archive/UniversalArchiveReader.scala | 1430 | `126efe96919f560edf3850cacdf80ba3d65f66b1d17b940be140a10c713138ec` | 0 |
| community/daml-lf/archive/src/main/scala/com/digitalasset/daml/lf/archive/package.scala | 4473 | `842cb0bc8ecfa9815df2fe1abe67fc39b3e179594792f8d8918cf640d0aeb9d4` | 0 |
| community/daml-lf/data-scalacheck/src/main/scala/com/digitalasset/daml/lf/data/DataArbitrary.scala | 2004 | `5d79c6ef09666afb2b39e27928fe2f9f9ce3bf83a9aafa067f960a84584694ff` | 0 |
| community/daml-lf/data/src/main/scala/com/digitalasset/daml/SafeProto.scala | 3087 | `41b8f91a934745e705e169c05d86622f79219ad6d0c37e33478506c95559b2d9` | 0 |
| community/daml-lf/data/src/main/scala/com/digitalasset/daml/lf/InternalError.scala | 1515 | `0385133384ef7a0c36840efa069b22934bb87c29b077e83c125178ee592cdb07` | 0 |
| community/daml-lf/data/src/main/scala/com/digitalasset/daml/lf/VersionRange.scala | 4243 | `c901a7fb931ec877c99fa836f9dbffd411f14301333260cfafc0b80f5ac3c63c` | 0 |
| community/daml-lf/data/src/main/scala/com/digitalasset/daml/lf/data/ArrayFactory.scala | 399 | `fca380c34ded8f156272a5387f15aee98cbc01382fb2427226542deba16a3606` | 0 |
| community/daml-lf/data/src/main/scala/com/digitalasset/daml/lf/data/BackStack.scala | 4697 | `955e4f81ed1827934f7101f17eea93caf11268c43288dec93289ba4545858822` | 0 |
| community/daml-lf/data/src/main/scala/com/digitalasset/daml/lf/data/Bytes.scala | 2114 | `2522bde736885c7e084494df5ecec4c87e784497a93d2488589156c52c3802e4` | 0 |
| community/daml-lf/data/src/main/scala/com/digitalasset/daml/lf/data/Decimal.scala | 1718 | `b7f70882aba017437d4107be81c1999d651f72758dcd6345635819fbbea84141` | 0 |
| community/daml-lf/data/src/main/scala/com/digitalasset/daml/lf/data/Freer.scala | 6243 | `a216b28c63fa29713a92d1d013e03ef6883f5e3c2cdd22665e2b647087a1ce34` | 0 |
| community/daml-lf/data/src/main/scala/com/digitalasset/daml/lf/data/FrontStack.scala | 6285 | `2c15ac1ccce082e4711ef86a551cdddd3716cc0939357e22f208f8968be4803f` | 0 |
| community/daml-lf/data/src/main/scala/com/digitalasset/daml/lf/data/IdString.scala | 12464 | `97102868a33007011dd18d250dfabea147f27ca1dd2536b6328a000a32ed4e82` | 0 |
| community/daml-lf/data/src/main/scala/com/digitalasset/daml/lf/data/ImmArray.scala | 14683 | `dd578ce10fdd6b767a980412d269f930cc5644262a06564dc0d8323897dad445` | 0 |
| community/daml-lf/data/src/main/scala/com/digitalasset/daml/lf/data/InsertOrdSet.scala | 2310 | `c27bceb3d3cb68214a445c296180f4ed00ba01c658d54e3a9cecb7e042e94f82` | 0 |
| community/daml-lf/data/src/main/scala/com/digitalasset/daml/lf/data/NoCopy.scala | 311 | `1ca47455a45941316fc29c5c9880e6324f05948e213cd250a0fab56d48fafafb` | 0 |
| community/daml-lf/data/src/main/scala/com/digitalasset/daml/lf/data/NumericModule.scala | 13528 | `4e2137d25731d9c61829f5cb7a1767eb8610ae6220b169af1a2c2d53a15972e8` | 0 |
| community/daml-lf/data/src/main/scala/com/digitalasset/daml/lf/data/RedBlackTree.scala | 6243 | `32646fc893ef79732afdebe46a088ba54c9a868cf54cfc966780d42fabfff55c` | 0 |
| community/daml-lf/data/src/main/scala/com/digitalasset/daml/lf/data/Ref.scala | 15741 | `f1324d4d5e562451658ffc4079817d9e8fb2cb110bab624365dc70d7516a762c` | 0 |
| community/daml-lf/data/src/main/scala/com/digitalasset/daml/lf/data/Relation.scala | 1710 | `c7beeb880468fca5bc76e03704d0e772e670627138c4886ba82d8d62f102d31e` | 0 |
| community/daml-lf/data/src/main/scala/com/digitalasset/daml/lf/data/SortedLookupList.scala | 3458 | `ec23428787ef71d051c59a6b466b1ce9144a65c0b750e57d97908c935011a5bc` | 0 |
| community/daml-lf/data/src/main/scala/com/digitalasset/daml/lf/data/Struct.scala | 2882 | `ba51e3802896bfa431883219cbe85fc845fed8c2fc1a2c32115264161213ff09` | 0 |
| community/daml-lf/data/src/main/scala/com/digitalasset/daml/lf/data/TemplateOrInterface.scala | 525 | `d6dbd8db1571c2466e5382a5a6693115b1a092f1200316330cac949c9eb0f26e` | 0 |
| community/daml-lf/data/src/main/scala/com/digitalasset/daml/lf/data/Text.scala | 1302 | `158951b60ba9413c6546e612b082b505f319ed5d8597af2af8c10a71ce391894` | 0 |
| community/daml-lf/data/src/main/scala/com/digitalasset/daml/lf/data/Time.scala | 6501 | `26a4ab78ec6d974d49546bb724a9d14c5a86c5168ba77f8e00f40bb0b5e15134` | 0 |
| community/daml-lf/data/src/main/scala/com/digitalasset/daml/lf/data/Trampoline.scala | 601 | `55d4697a2a28b895e0ef3e2315b01c92b0b0e3a9f2fafb1aaba52ea2033f1dd7` | 0 |
| community/daml-lf/data/src/main/scala/com/digitalasset/daml/lf/data/TryOps.scala | 543 | `ad839e4c33e00550a7b8668dbcb775d26856c11702e143e2f25054c16be2d5db` | 0 |
| community/daml-lf/data/src/main/scala/com/digitalasset/daml/lf/data/Utf8.scala | 3478 | `37b49c5f1810f2da8a76adf67500968498513487166fc54a3c80902df0370507` | 0 |
| community/daml-lf/data/src/main/scala/com/digitalasset/daml/lf/data/logging/LoggingConfiguration.scala | 647 | `de7b648ff782099c543b0784fa52a049bbdf0b69b73bb1184fc571e2dcff41e7` | 0 |
| community/daml-lf/data/src/main/scala/com/digitalasset/daml/lf/data/logging/package.scala | 2013 | `9a7c3e0c213c1ee3c0d9b3ae6ba5113142756987852f6863ed24beb4026609b1` | 0 |
| community/daml-lf/data/src/main/scala/com/digitalasset/daml/lf/data/package.scala | 687 | `561928aaf412349d798a7f0849d2218c36499f8677d06aefdee529af07e2e66e` | 0 |
| community/daml-lf/data/src/main/scala/com/digitalasset/daml/lf/data/support/crypto/MessageDigest.scala | 519 | `e78c71c732c0aac6e70fad198c3c83d721dc36a1db0c2d2f04bedc72e2a1109d` | 0 |
| community/daml-lf/data/src/main/scala/com/digitalasset/daml/lf/data/support/crypto/MessageSignature.scala | 966 | `ee6289bd8ba67a0ab94b9ae626fbccd3972f7882790a5b0a212dd5742b7be110` | 0 |
| community/daml-lf/data/src/main/scala/com/digitalasset/daml/lf/data/support/crypto/MessageSignatureUtil.scala | 1164 | `dc71b96c5968bcf77e70ca8e51ef85f43aa19550fd6d04e0c5ec8314bf99addf` | 0 |
| community/daml-lf/engine/src/main/scala/com/digitalasset/daml/lf/engine/Blinding.scala | 3936 | `0b5290ee7345b13a0604f08739230909c6f242d1170a9dab12ad1d17b86711e4` | 0 |
| community/daml-lf/engine/src/main/scala/com/digitalasset/daml/lf/engine/ConcurrentCompiledPackages.scala | 7703 | `b4c6bb78e7da4e1dfd20d53425f931519056a4a99c3d7cf0e7b1166ecea37c0d` | 0 |
| community/daml-lf/engine/src/main/scala/com/digitalasset/daml/lf/engine/Engine.scala | 60369 | `d5dbcbb56e46bac0ec31ac83b8f2b275330c6a421106e7758e1a438e85944a4b` | 0 |
| community/daml-lf/engine/src/main/scala/com/digitalasset/daml/lf/engine/EngineConfig.scala | 3929 | `aeefafbeafb8108c867eb8f3c611792777d669aa8d6d804ef3fab30e55104916` | 0 |
| community/daml-lf/engine/src/main/scala/com/digitalasset/daml/lf/engine/EngineInfo.scala | 596 | `b268e4474d276605e48523e8c24283a44e787b8f1b63d2cdfc8a3405a3bdf750` | 0 |
| community/daml-lf/engine/src/main/scala/com/digitalasset/daml/lf/engine/EngineLoggingConfig.scala | 757 | `5b0e7f2fb4d768e759ec5593cff7bdbe808fe3d8645a15579c3eb99d73817429` | 0 |
| community/daml-lf/engine/src/main/scala/com/digitalasset/daml/lf/engine/Error.scala | 8626 | `f763c39f217e7c2c6875ada41dfad84feadff941992163cf590d2d964fc518e2` | 0 |
| community/daml-lf/engine/src/main/scala/com/digitalasset/daml/lf/engine/Event.scala | 4284 | `323f05f3c46267d235fadd9248c5e862ac6464d2d470a1f38cad5a3b96935686` | 0 |
| community/daml-lf/engine/src/main/scala/com/digitalasset/daml/lf/engine/MutableCompiledPackages.scala | 833 | `66985cd1a8185e359166d434506e813009ff761d07a6db2db3748cbd0c8b8e42` | 0 |
| community/daml-lf/engine/src/main/scala/com/digitalasset/daml/lf/engine/Result.scala | 9369 | `2de03d88756ddc6a21f29cf5fc4eea4172016268d97d9a518cab1add0930f076` | 0 |
| community/daml-lf/engine/src/main/scala/com/digitalasset/daml/lf/engine/ScriptEngine.scala | 6643 | `2767ad3ba729c62c3ad99716c5b45e7882b5dd07601874663d080a42e2b8e672` | 0 |
| community/daml-lf/engine/src/main/scala/com/digitalasset/daml/lf/engine/SnapshotRecorder.scala | 4090 | `c9d1fe7d0a0da1e33cfbc015c5af5645d4a92ec88086170ffa4f23a46aead231` | 0 |
| community/daml-lf/engine/src/main/scala/com/digitalasset/daml/lf/engine/TransactionCoder.scala | 26962 | `0efc1507c8311a0ca5d69bf0cb564ed6e2434b18605b373555a71aaebc7935aa` | 0 |
| community/daml-lf/engine/src/main/scala/com/digitalasset/daml/lf/engine/package.scala | 334 | `c6054a2e3cb587dc41400bc2a606014ba66e06f2c3f450663da934dbe1fcaa73` | 0 |
| community/daml-lf/engine/src/main/scala/com/digitalasset/daml/lf/engine/refinement/CommandPreprocessor.scala | 12529 | `79fb6b641e9e7640abefe9c9dba68ab2e52d345a0faa2ac855ba1a0bcb949a7b` | 0 |
| community/daml-lf/engine/src/main/scala/com/digitalasset/daml/lf/engine/refinement/Enricher.scala | 9123 | `1b72153675d35b42b3504f2acd9a654b9347f07a8b689cbe7b9dd07cfd0de7b2` | 0 |
| community/daml-lf/engine/src/main/scala/com/digitalasset/daml/lf/engine/refinement/EnricherImpl.scala | 12669 | `53548087bd0d19a7b589c2f7f0bcb4f3b6f103e267988d41d920bfa2da387fe4` | 0 |
| community/daml-lf/engine/src/main/scala/com/digitalasset/daml/lf/engine/refinement/Preprocessor.scala | 12881 | `008f18a5fa4e54fa5a2035ff1eda4306148a7256db4574f5cb9ad9cada1ff3c6` | 0 |
| community/daml-lf/engine/src/main/scala/com/digitalasset/daml/lf/engine/refinement/SafePackageResolver.scala | 4314 | `49465d61330d310ac5b291e808c475d27c4bf2cbd8bdc93287248037a6de70e1` | 0 |
| community/daml-lf/engine/src/main/scala/com/digitalasset/daml/lf/engine/refinement/ValueTranslator.scala | 11983 | `c4c6029bfe05db4f92a0ffc2217c58cf682402167dfcbf749563bb0ae7669dcf` | 0 |
| community/daml-lf/engine/src/main/scala/com/digitalasset/daml/lf/engine/refinement/package.scala | 1200 | `f4d38cf5f0937eb6529775dd5d6fe076feb90aa0c69a05af2ba5f15d89412c18` | 0 |
| community/daml-lf/ide-ledger/src/main/scala/com/digitalasset/daml/lf/script/Error.scala | 2593 | `d607ed6cbf1502e40e404f0dd973a651dc51e377627993361b0884ddb0274c48` | 0 |
| community/daml-lf/ide-ledger/src/main/scala/com/digitalasset/daml/lf/script/IdeLedgerRunner.scala | 21254 | `32b68d785115e16d8f345ad21a25274ef34073c696111ed3031334ff45332ddd` | 0 |
| community/daml-lf/ide-ledger/src/main/scala/com/digitalasset/daml/lf/script/Pretty.scala | 3563 | `42d9c1b5b1fe2ba916f8e6c1cfeef73844953ded869509232db272474c2387de` | 0 |
| community/daml-lf/ide-ledger/src/main/scala/com/digitalasset/daml/lf/script/TimeBomb.scala | 821 | `2d3458099849ee00554ba4e8aa91541290fd3bf36c72927fc98e9512e3cf2191` | 0 |
| community/daml-lf/interpreter/src/main/scala/com/digitalasset/daml/lf/CompiledPackages.scala | 5144 | `501a2782e68ee948b64d56bcc99ffb30f765cf1e647bcd49a5b5f93b33c462f9` | 0 |
| community/daml-lf/interpreter/src/main/scala/com/digitalasset/daml/lf/crypto/SValueHash.scala | 9397 | `ea97a47990d406d644b7a07d314f03bf31a773dfb6967c8da42206633a893cad` | 0 |
| community/daml-lf/interpreter/src/main/scala/com/digitalasset/daml/lf/ledger/BlindingTransaction.scala | 3029 | `c6c26c12224e93abbbe129b3ae6f9ab661017f411db04cea4d7acf0923acbc6b` | 0 |
| community/daml-lf/interpreter/src/main/scala/com/digitalasset/daml/lf/package.scala | 2171 | `3bb4032e7b16455628fa4a55ebc0027b08ba520685c7281eefc06f6b4d357f9c` | 0 |
| community/daml-lf/interpreter/src/main/scala/com/digitalasset/daml/lf/script/EventId.scala | 691 | `2835f7efa90213b08296f1cf7a7c76340b29cf81464cd74ed1679d353f426027` | 0 |
| community/daml-lf/interpreter/src/main/scala/com/digitalasset/daml/lf/script/IdeLedger.scala | 21897 | `56a91732301a6126f7fd66d8dac977f1d90d9a451399f5299e8df0b4b905da56` | 0 |
| community/daml-lf/interpreter/src/main/scala/com/digitalasset/daml/lf/speedy/AuthorizationChecker.scala | 5995 | `33a21fe4db1e0916a89d8320107dd8d90081927f54d93f4a47ed3f9dfb45fb26` | 0 |
| community/daml-lf/interpreter/src/main/scala/com/digitalasset/daml/lf/speedy/Classify.scala | 1726 | `62ca41ac1bfac9bf5e5c868c134ea7cbee6a0d1435c4eb5be4264bf5bcd044f0` | 0 |
| community/daml-lf/interpreter/src/main/scala/com/digitalasset/daml/lf/speedy/ClosureConversion.scala | 14459 | `9d6ce6e2ccedfc95090e0ab293231e606e6a939c4b9c1beb17547d835d0fa414` | 0 |
| community/daml-lf/interpreter/src/main/scala/com/digitalasset/daml/lf/speedy/Command.scala | 2345 | `196cb5de7e4c9dc7ec19f57017e5eb2f4d3fcdee5e1977e6fe259fa90603b051` | 0 |
| community/daml-lf/interpreter/src/main/scala/com/digitalasset/daml/lf/speedy/CostModel.scala | 38583 | `1cba99804aba679ced217cadd145e40c0ddd1699d1e9bdeaa709e793722ea5b7` | 0 |
| community/daml-lf/interpreter/src/main/scala/com/digitalasset/daml/lf/speedy/ExtendedValueTranslator.scala | 5514 | `4f392d03edf820fd6178d7281859b45396fec5acc35c954959c9bdd9061f28c0` | 0 |
| community/daml-lf/interpreter/src/main/scala/com/digitalasset/daml/lf/speedy/InitialSeeding.scala | 702 | `fbe0e6bacc02da50a5925864545aef19b14e50a57813ca0743f814302a355142` | 0 |
| community/daml-lf/interpreter/src/main/scala/com/digitalasset/daml/lf/speedy/MachineLogger.scala | 2771 | `6ef41fc527a4aceabf0aba44007b1c93929ab3b5f5afc6e61cd13dfa37d1bc20` | 0 |
| community/daml-lf/interpreter/src/main/scala/com/digitalasset/daml/lf/speedy/NormalizeRollbacks.scala | 8863 | `6c4aa4095808710455b3a9dc6f691143eae31c3a51eb9a4f28adbb49e9f72678` | 0 |
| community/daml-lf/interpreter/src/main/scala/com/digitalasset/daml/lf/speedy/PartialTransaction.scala | 28194 | `03b051c5f538933f5b734ffe54b6b0282e2b58449df75adf93e38ba2cac90b6a` | 0 |
| community/daml-lf/interpreter/src/main/scala/com/digitalasset/daml/lf/speedy/Pretty.scala | 35004 | `25d944b4912bebbb4d7ee6074c80f11503c5e1561c7bb0194ea479ee72aa990a` | 0 |
| community/daml-lf/interpreter/src/main/scala/com/digitalasset/daml/lf/speedy/PrettyLightweight.scala | 2871 | `42585ccc5f09be395da111c01186d8bf958b485076cdfc538c46d153dd675e75` | 0 |
| community/daml-lf/interpreter/src/main/scala/com/digitalasset/daml/lf/speedy/Profile.scala | 15035 | `56b6d39df68c5c56e983f7f106edd6b28ee0aceae9a8923542b3086a10eeb97f` | 0 |
| community/daml-lf/interpreter/src/main/scala/com/digitalasset/daml/lf/speedy/SBuiltinFun.scala | 118745 | `17e9d232f6286b4d4f9b930155469e8f5c0924786119c53cade5051ffc327824` | 0 |
| community/daml-lf/interpreter/src/main/scala/com/digitalasset/daml/lf/speedy/SDefinition.scala | 723 | `b0a68b4dfd52560029a69f1844d0230b77578f16ab30646114208dba06d8a77d` | 0 |
| community/daml-lf/interpreter/src/main/scala/com/digitalasset/daml/lf/speedy/SError.scala | 1262 | `2dd779468ccd6137f23a8639d3de60c64146bf969b0efe18a9c47589c3768b49` | 0 |
| community/daml-lf/interpreter/src/main/scala/com/digitalasset/daml/lf/speedy/SExpr.scala | 18224 | `4cd609e152b8a15eae77409c91f8a2c363480ddf1477060884b2051e9439817d` | 0 |
| community/daml-lf/interpreter/src/main/scala/com/digitalasset/daml/lf/speedy/SResult.scala | 6054 | `df135b63b57c3bd51ea58a004c842439136aaafb8162895b9747ae1819df61c2` | 0 |
| community/daml-lf/interpreter/src/main/scala/com/digitalasset/daml/lf/speedy/SValue.scala | 16971 | `a9c49b34dd0b0fa598cd932db2735a28dd2776abea8cb5c9ffa31b6e800893ee` | 0 |
| community/daml-lf/interpreter/src/main/scala/com/digitalasset/daml/lf/speedy/Speedy.scala | 62603 | `876a23d573a072dc4a0cc568432febfa04db84c10edb7d843f56cd1285398f5e` | 0 |
| community/daml-lf/interpreter/src/main/scala/com/digitalasset/daml/lf/speedy/Stack.scala | 2156 | `c5908d3f15676061582d8d9a5bd1ec7b8bddd68540681d04e923a0a07ffd7924` | 0 |
| community/daml-lf/interpreter/src/main/scala/com/digitalasset/daml/lf/speedy/TransactionConductor.scala | 62351 | `0fc7f03055e2c69d4401475cee6305807507757109b1ff43b220fde566a7d8c8` | 0 |
| community/daml-lf/interpreter/src/main/scala/com/digitalasset/daml/lf/speedy/TreeIterator.scala | 2118 | `6c0278dcbfdffd8d651eca708adb4bfe78266efe24bd128dac2799342c1e7cc4` | 0 |
| community/daml-lf/interpreter/src/main/scala/com/digitalasset/daml/lf/speedy/ValueTranslator.scala | 10396 | `473ad3fd9d849984574929ff7880b0b22f71dbbedadc486f2504b7dbbbe987c1` | 0 |
| community/daml-lf/interpreter/src/main/scala/com/digitalasset/daml/lf/speedy/compiler/Anf.scala | 13586 | `91d0b0e0d713c88bfa6eaf01d7493959b679e7fce4ef33eff2ab1a234dc5aaa0` | 0 |
| community/daml-lf/interpreter/src/main/scala/com/digitalasset/daml/lf/speedy/compiler/Compiler.scala | 47135 | `452f586c47136c4a30fc195845a8cb0d8f47fdebf53f661ba10810af4b296f68` | 0 |
| community/daml-lf/interpreter/src/main/scala/com/digitalasset/daml/lf/speedy/compiler/PhaseOne.scala | 31561 | `05ff24810755bf7284861a244beea97c049c25ceb31a37de6a80b1fb235edd43` | 0 |
| community/daml-lf/interpreter/src/main/scala/com/digitalasset/daml/lf/speedy/compiler/SExpr0.scala | 4668 | `d26a63a05ad0c5090183d84e27b26d093fb08855cd67d6e639c2da13ee41667d` | 0 |
| community/daml-lf/interpreter/src/main/scala/com/digitalasset/daml/lf/speedy/compiler/SExpr1.scala | 4204 | `bd74b9a9527ee7d18682ba34f9fb943ef8f452571da4339268427321c774868f` | 0 |
| community/daml-lf/interpreter/src/main/scala/com/digitalasset/daml/lf/speedy/iterable/SValueIterable.scala | 1443 | `8447f1c273b0ae635300270f3d7e2b96e16d88bf980b41f1ea9c8d51590d5d74` | 0 |
| community/daml-lf/interpreter/src/main/scala/com/digitalasset/daml/lf/speedy/metrics/FetchNodeCount.scala | 540 | `dd7f379bcb7d07c23a2394a3e1e8d2ab8959e9936bbdd4d455d4438c451d9ef3` | 0 |
| community/daml-lf/interpreter/src/main/scala/com/digitalasset/daml/lf/speedy/metrics/MetricPlugin.scala | 356 | `ab573f2c9669bfdd72c9bcb12c23849e45e3b50c962b2da84bf35dbc56cb0386` | 0 |
| community/daml-lf/interpreter/src/main/scala/com/digitalasset/daml/lf/speedy/metrics/MetricPlugins.scala | 861 | `3ed779815d726b73107617cd588df522325d8c980b1482c532de73b150ec8592` | 0 |
| community/daml-lf/interpreter/src/main/scala/com/digitalasset/daml/lf/speedy/metrics/StepCount.scala | 956 | `1b24c05a5ed2cc7dce641cd58070642855950e23781e780ca06864f2c0e199d5` | 0 |
| community/daml-lf/interpreter/src/main/scala/com/digitalasset/daml/lf/speedy/metrics/TxNodeCount.scala | 525 | `1d291fd58488fb5ce9ba8a9118f337b3c463b7cecf5320ed2998ef18d7f076e7` | 0 |
| community/daml-lf/interpreter/src/main/scala/com/digitalasset/daml/lf/speedy/svalue/Equality.scala | 4714 | `1139c845ad07208ae39ee0c89eb7d04df1f2a2cfb31afaaa32c0e1828d24c3da` | 0 |
| community/daml-lf/interpreter/src/main/scala/com/digitalasset/daml/lf/speedy/svalue/InterlacedIterator.scala | 590 | `359625a3915199bbd301d57547ca93e4ddb7f3cdf2e32bfb4d6db67701e3d3a4` | 0 |
| community/daml-lf/interpreter/src/main/scala/com/digitalasset/daml/lf/speedy/svalue/Ordering.scala | 5199 | `ebf0b19c8b51943e3ef0c272d18356919d7762d06975fde665e50afb7a8877ea` | 0 |
| community/daml-lf/interpreter/src/main/scala/com/digitalasset/daml/lf/transaction/LimitConfig.scala | 555 | `0340e66776911d9d3ec718358d61d21b2a397d5a6a2b1faccc713d796bf073de` | 0 |
| community/daml-lf/interpreter/src/main/scala/com/digitalasset/daml/lf/transaction/Limits.scala | 1228 | `a15c9fd2c4ebf3056c85723ab1475ec51bb90f789cf7b8c201675c6fd54006ca` | 0 |
| community/daml-lf/interpreter/src/main/scala/com/digitalasset/daml/lf/transaction/metrics/TransactionNodeMetrics.scala | 6745 | `c9e0b1eb506e9c5f611f4e44928e7074bbbd31b66a797c652c7fbdb95067aa1a` | 0 |
| community/daml-lf/interpreter/src/main/scala/com/digitalasset/daml/lf/transaction/validator/ActingPartiesValidator.scala | 2073 | `f60a565be584319e53a74606282a32acb3df0dadee2f80076ed8888abe00378a` | 0 |
| community/daml-lf/interpreter/src/main/scala/com/digitalasset/daml/lf/transaction/validator/ChoiceAuthorizersValidator.scala | 1562 | `97e60013894028cdc15be37585ae07e223c54a9d899d746e24a65376892d9c11` | 0 |
| community/daml-lf/interpreter/src/main/scala/com/digitalasset/daml/lf/transaction/validator/ChoiceObserversValidator.scala | 1530 | `616311b3951c2d72c795ae0600ec011375fe6dea32994d8b8f79d79ed3eab7d1` | 0 |
| community/daml-lf/interpreter/src/main/scala/com/digitalasset/daml/lf/transaction/validator/ExternalCallResultSizeValidator.scala | 2503 | `76a3e93a8b7ee4ab6b7911daf39703525581b8feaa2acfebfc326b64f89c6ac1` | 0 |
| community/daml-lf/interpreter/src/main/scala/com/digitalasset/daml/lf/transaction/validator/ExternalCallResultsValidator.scala | 1576 | `b451bc568b5b96541a4cbcf606d0ff5f7d3aa52ceceb91f0feff21bbb1cdf8f5` | 0 |
| community/daml-lf/interpreter/src/main/scala/com/digitalasset/daml/lf/transaction/validator/InputContractValidator.scala | 1255 | `13a798feefd0f142ce4e934366c8f3a946e2262f326f934f72acb1dcbdf37fee` | 0 |
| community/daml-lf/interpreter/src/main/scala/com/digitalasset/daml/lf/transaction/validator/KeyMaintainersValidator.scala | 3473 | `80542231f93177298bd75c7e10c5a46294ed43655a685e72693bb0bed23a208d` | 0 |
| community/daml-lf/interpreter/src/main/scala/com/digitalasset/daml/lf/transaction/validator/NodeChildrenValidator.scala | 1392 | `a17013cb91218425a4c13e37494fc21ced76acc471f7d607ce01c787ae0e9b6f` | 0 |
| community/daml-lf/interpreter/src/main/scala/com/digitalasset/daml/lf/transaction/validator/SignatoryValidator.scala | 2724 | `67cece9b44d3d856d2bf5c2285df0e880b6cbd4dad2e52b4711657577e2efe85` | 0 |
| community/daml-lf/interpreter/src/main/scala/com/digitalasset/daml/lf/transaction/validator/StakeholderValidator.scala | 2756 | `b7a07966966e851b479b36c0a55074ae20a0baef84ba48f359255c62dd833ff8` | 0 |
| community/daml-lf/interpreter/src/main/scala/com/digitalasset/daml/lf/transaction/validator/TotalInformeeValidator.scala | 1307 | `bea4330b94bada0649a271faa6747626e91c5bb44acb14ea0dc2dec274aef51f` | 0 |
| community/daml-lf/interpreter/src/main/scala/com/digitalasset/daml/lf/transaction/validator/TransactionNodesValidator.scala | 1238 | `b774b0fe50207be359335b8ecb0473ed9a07af3140172ad1753312b6215c0962` | 0 |
| community/daml-lf/interpreter/src/main/scala/com/digitalasset/daml/lf/transaction/validator/TransactionRootsValidator.scala | 1236 | `19fde862a4fcca374dd0a30d36bde44ca902ef81a602fe9fd3ebfe5b023d7a4f` | 0 |
| community/daml-lf/interpreter/src/main/scala/com/digitalasset/daml/lf/transaction/validator/TransactionValidator.scala | 2823 | `4bb3bebeb182b516240d344ea162293bd3e96b7b4f4d42e94972f6c458f50ad3` | 0 |
| community/daml-lf/interpreter/src/main/scala/com/digitalasset/daml/lf/transaction/validator/ValueValidator.scala | 6391 | `b70133eed38a4a600b31ce0f0445495030d27a4f5dd4b460b79918e5244498bd` | 0 |
| community/daml-lf/language/src/main/scala/com/digitalasset/daml/lf/language/Ast.scala | 54262 | `3f34b9fb14064d48eb65d43f7d439b68579e6b239008d7b51c8a91b5cc2ec733` | 0 |
| community/daml-lf/language/src/main/scala/com/digitalasset/daml/lf/language/Graphs.scala | 3265 | `be21df38a3f2f284346cedc459436875c171b51e0ffc9dc8bff5d60dc98d22db` | 0 |
| community/daml-lf/language/src/main/scala/com/digitalasset/daml/lf/language/LanguageVersion.scala | 7319 | `13a18f2c36982bb71559da1a0af123c5354e101fe41428690248bb232357961f` | 0 |
| community/daml-lf/language/src/main/scala/com/digitalasset/daml/lf/language/LegacyLanguageVersions.scala | 1967 | `9040633bd5a03ee0ccd21ae512d4b9a8048d1ef30ed866e8a3407e23b6a62fbc` | 0 |
| community/daml-lf/language/src/main/scala/com/digitalasset/daml/lf/language/LookupError.scala | 5380 | `21549e85c6f88332d207756a58c60e8c47db952332ea1abb0454298acdf37abf` | 0 |
| community/daml-lf/language/src/main/scala/com/digitalasset/daml/lf/language/PackageInterface.scala | 15253 | `b035c53c40cb5dc2c4183f2e2d9918dfedbdc5d481e2e8f424a9c9f957be6b06` | 0 |
| community/daml-lf/language/src/main/scala/com/digitalasset/daml/lf/language/StablePackages.scala | 1351 | `d4378612da8caed5dff1c6667aba084ff7e44ffb724e2356d32f1187d40b09e2` | 0 |
| community/daml-lf/language/src/main/scala/com/digitalasset/daml/lf/language/TypeDestructor.scala | 8364 | `311973f6d4a40732aa7c824699fe90a38e10561a80fec16e65c6ae945cfe61ab` | 0 |
| community/daml-lf/language/src/main/scala/com/digitalasset/daml/lf/language/TypeOrdering.scala | 3243 | `c6f780294e71e03aedddcae5ba8724f076d3a5989f4cde5eac56ada304174489` | 0 |
| community/daml-lf/language/src/main/scala/com/digitalasset/daml/lf/language/TypeSig.scala | 10206 | `b0b6d556690fc906a5643523ab166728b0f7a98a5b822c5696fb7ec29910ee90` | 0 |
| community/daml-lf/language/src/main/scala/com/digitalasset/daml/lf/language/Util.scala | 11702 | `058a941ef1162cae23219c9c9670d9b8e292026bc80f2458e245ef31b066e459` | 0 |
| community/daml-lf/language/src/main/scala/com/digitalasset/daml/lf/language/UtilityDamlPackages.scala | 44537 | `1c5e11b30c8af8197a749a181f3b9dd0e9f4c0876e8b000a47db1f2dce1e93b6` | 0 |
| community/daml-lf/language/src/main/scala/com/digitalasset/daml/lf/language/util/PackageInfo.scala | 2700 | `6037f2090791eb2676f3a76c56f600823ae40befc0a5af61eb28f84eb3899b1b` | 0 |
| community/daml-lf/language/src/main/scala/com/digitalasset/daml/lf/language/util/iterable/ExprIterable.scala | 8655 | `5bf99e1e897b7cf25fbef45ff3d0b7c64ded1ceca3d29ed63497ee571d4d7d24` | 0 |
| community/daml-lf/language/src/main/scala/com/digitalasset/daml/lf/language/util/iterable/TypeIterable.scala | 9752 | `7b05dbb1483ea836022f1d294212a0ae0103f122cde905399da8d0c13f71fd70` | 0 |
| community/daml-lf/ledger-api-value-proto/src/main/protobuf/com/daml/ledger/api/v2/value.proto | 6902 | `5474ef65abe5402ed1720d17031c0339176b3bdf83506b243e0663e2efb9b3f5` | 0 |
| community/daml-lf/ledger-api-value/src/main/protobuf/com/daml/ledger/api/scalapb/package.proto | 329 | `8561786ff14f9ef50c9f242e4bdddaecc1ee9e66421f81a73f1b89f66745726d` | 0 |
| community/daml-lf/snapshot-proto/src/main/protobuf/com/digitalasset/daml/lf/snapshot.proto | 3695 | `a301e1bcb788a2a7b63f08712a06bab348e1bbef9b01978d920fa912395578dc` | 0 |
| community/daml-lf/stable-packages/src/main/scala/com/digitalasset/daml/lf/stablepackages/StablePackages.scala | 4109 | `b51b9108c67f295e615f9c881ee54e2e606311d2b50f8491e4bff4e016160c26` | 0 |
| community/daml-lf/transaction-test-lib/src/main/scala/com/digitalasset/daml/lf/EitherAssertions.scala | 378 | `982fa0d0fe4790e952d86c5f1cd4daedefe5d9542c22884cb336a999b6426e04` | 0 |
| community/daml-lf/transaction/src/main/protobuf/com/digitalasset/daml/lf/transaction.proto | 2300 | `22884ba1092578dd010f408324bf7036fc26db67c312d93757d231b8f51413df` | 0 |
| community/daml-lf/transaction/src/main/protobuf/com/digitalasset/daml/lf/value.proto | 2996 | `2d3f94fc430d42074efbcbe79182d7204469547c65726e5c04cbaf2524628cc9` | 0 |
| community/daml-lf/transaction/src/main/scala/com/digitalasset/daml/lf/command.scala | 1249 | `cf7b1b447a4b49af7c504f8f6319ff5cbfc89ffa728e5314167bcb1e2e57f89b` | 0 |
| community/daml-lf/transaction/src/main/scala/com/digitalasset/daml/lf/command/ApiCommand.scala | 3418 | `825a611a78a25753ca4ae7d8e73abba95589b8a9f76b672494bade685f71f580` | 0 |
| community/daml-lf/transaction/src/main/scala/com/digitalasset/daml/lf/command/ReplayCommand.scala | 1656 | `5201f42a4a187714ea7768fbacfc01423fbe386f8f19636c4295f17ba1056e4c` | 0 |
| community/daml-lf/transaction/src/main/scala/com/digitalasset/daml/lf/crypto/Hash.scala | 43236 | `4640238c9a3bd2c2617b9297b69af1a0e4e7e2aededbd7fa72652d8fb14971d0` | 0 |
| community/daml-lf/transaction/src/main/scala/com/digitalasset/daml/lf/crypto/HashUtils.scala | 4264 | `4a5c8faf39bc60aae92f87277874049966d6a688a0509ec58905af8d6c6254aa` | 0 |
| community/daml-lf/transaction/src/main/scala/com/digitalasset/daml/lf/data/CostModel.scala | 15341 | `17495f48912864f01684824b0c582768dcaa9ff4bf3def64e5b63a6f91e0ab95` | 0 |
| community/daml-lf/transaction/src/main/scala/com/digitalasset/daml/lf/interpretation/Error.scala | 13956 | `8c21056df612b0687be993a52c85ede1b67866bd5c2d20012782710974feba85` | 0 |
| community/daml-lf/transaction/src/main/scala/com/digitalasset/daml/lf/interpretation/ExecutionMode.scala | 462 | `cf2f8f80702c19fa1a3d153834a12a2317ad50589fea29655910ea8bfeb8f081` | 0 |
| community/daml-lf/transaction/src/main/scala/com/digitalasset/daml/lf/interpretation/InterpretationConfig.scala | 1807 | `585427cb157be344327428092b222866c60609f9b885a689680fb5a4ce433c0a` | 0 |
| community/daml-lf/transaction/src/main/scala/com/digitalasset/daml/lf/ledger/Authorization.scala | 2084 | `d39eaac89157490428141b4045cf66e4467c318fa8382fc6edad3b62476b2098` | 0 |
| community/daml-lf/transaction/src/main/scala/com/digitalasset/daml/lf/transaction/BackwardsCompatibilityImplicits.scala | 1438 | `73fee1094a508bba98fb0700111a46ac0a3cd230485a5473203d5d899f1ccd70` | 0 |
| community/daml-lf/transaction/src/main/scala/com/digitalasset/daml/lf/transaction/BlindingInfo.scala | 2113 | `4fc9053449c8ad324eb281c1bce31218115e684d84cf25666bf3a6ec0ae44309` | 0 |
| community/daml-lf/transaction/src/main/scala/com/digitalasset/daml/lf/transaction/ContractInstanceCoder.scala | 13899 | `e4cc3f2017d9bbe6ce7f003599a9b96eb1ceb8f617d4459069bdf97b0732a8b8` | 0 |
| community/daml-lf/transaction/src/main/scala/com/digitalasset/daml/lf/transaction/ContractStateMachine.scala | 25058 | `1be8eac24bd7e17c0480a0972a578d0070a08dd88d8079c64776796bbf47f0ed` | 0 |
| community/daml-lf/transaction/src/main/scala/com/digitalasset/daml/lf/transaction/DiscriminatedSubtype.scala | 544 | `a7fe52d395f0861f2ccc13316d8ff4182a7fb6c527316845fec526fb00ed0344` | 0 |
| community/daml-lf/transaction/src/main/scala/com/digitalasset/daml/lf/transaction/FatContractInstance.scala | 8006 | `555b52460501778ecfdbd751a5f2a072284711b00e6a13674321b1fc71cf147f` | 0 |
| community/daml-lf/transaction/src/main/scala/com/digitalasset/daml/lf/transaction/GlobalKey.scala | 2628 | `51499e9b330ca1d8c304630b0d87ccdc520bd37990ca4ad6224588e2abdc73d8` | 0 |
| community/daml-lf/transaction/src/main/scala/com/digitalasset/daml/lf/transaction/IncompleteTransaction.scala | 357 | `046e6fe7f4a947784f49d2080993770aa2c42ff5db5844610745135b0b32820b` | 0 |
| community/daml-lf/transaction/src/main/scala/com/digitalasset/daml/lf/transaction/Node.scala | 12286 | `844bfa046b9f12e6a3a1a7b92a1aeb6537eb787d4b6ed40b0b19f73cb823cd9b` | 0 |
| community/daml-lf/transaction/src/main/scala/com/digitalasset/daml/lf/transaction/Normalization.scala | 3312 | `043491f32540f24b3c708cd4a5eabd66fa6a098c1d1bdd78f8d86a3490788545` | 0 |
| community/daml-lf/transaction/src/main/scala/com/digitalasset/daml/lf/transaction/SerializationVersion.scala | 3772 | `f10a85ce655afe0677b9e702f2f36660c14ae89fa07159eb45b59d7f56d94c03` | 0 |
| community/daml-lf/transaction/src/main/scala/com/digitalasset/daml/lf/transaction/Transaction.scala | 28895 | `5e347f5802ebe53944b9965e06471d57656c7b21b28fd47384e0cf369777ec3b` | 0 |
| community/daml-lf/transaction/src/main/scala/com/digitalasset/daml/lf/transaction/TransactionError.scala | 1863 | `d1e067608397af4df9e9c418a46f34a4043e2652c592fb8c688c4bf79cdfd951` | 0 |
| community/daml-lf/transaction/src/main/scala/com/digitalasset/daml/lf/transaction/TransactionNodeStatistics.scala | 6298 | `ceecb3bb75c14fb878e201f86aa17efae8d83de31052f8095c7709da9e829822` | 0 |
| community/daml-lf/transaction/src/main/scala/com/digitalasset/daml/lf/transaction/Util.scala | 2735 | `be013b79c9310c84bacc84ef4736710bf48910a9dd8dcf29fc762a521e00894b` | 0 |
| community/daml-lf/transaction/src/main/scala/com/digitalasset/daml/lf/transaction/Validation.scala | 777 | `db3417d63f30599076951649d77b278cb95fb3943be11ab7e42dda18e3d420b2` | 0 |
| community/daml-lf/transaction/src/main/scala/com/digitalasset/daml/lf/transaction/Versioned.scala | 443 | `cd35b394a3ee7cbe0c68b93ed75fdb393eb520b84facb37b7ca479f7e74efdc2` | 0 |
| community/daml-lf/transaction/src/main/scala/com/digitalasset/daml/lf/transaction/package.scala | 1705 | `528481d191dbbb759a61c5885716c3c9479754a924ff4bf7bf8dff0a15d2a560` | 0 |
| community/daml-lf/transaction/src/main/scala/com/digitalasset/daml/lf/value/CidContainer.scala | 1823 | `420662d02e2e75bdcb7deeffde2379bfe03076055f84d9d467441ae6f5eb30fc` | 0 |
| community/daml-lf/transaction/src/main/scala/com/digitalasset/daml/lf/value/Value.scala | 20043 | `837da01d78d06bd69b1cbae1afeb590d2c104eb22ec3eb0cefff5168c29d9f6c` | 0 |
| community/daml-lf/transaction/src/main/scala/com/digitalasset/daml/lf/value/ValueCoder.scala | 17705 | `b926c7824efc108c6a35047a1281acfd526778acbc59f89b5e4032e3c57a9167` | 0 |
| community/daml-lf/transaction/src/main/scala/com/digitalasset/daml/lf/value/package.scala | 241 | `e70f4dfb8d7e976bf3f801918f11814cd614d9292cd416545972874f33933983` | 0 |
| community/daml-lf/upgrade-check/src/main/scala/com/digitalasset/daml/lf/validation/UpgradeCheckMain.scala | 7880 | `98ebb17e25aa1805c6ae7ca593d4212111ad35d59a96241245ef47379b0fff96` | 0 |
| community/daml-lf/upgrades-matrix/src/main/scala/com/digitalasset/daml/lf/engine/UpgradesMatrix.scala | 112135 | `f0e66c2f6d916e49156ef8f084d6b400b400c44a1192a5510c1ae67858130d5e` | 0 |
| community/daml-lf/validation/src/main/scala/com/digitalasset/daml/lf/validation/AlphaEquiv.scala | 2381 | `878e94f5409700c1f8d423b6aca86cec8d6381c179186f178aae3a1cc5dd9b70` | 0 |
| community/daml-lf/validation/src/main/scala/com/digitalasset/daml/lf/validation/Collision.scala | 3636 | `6532abf2e9c1246cbbd2ec3faa64243bf1dbbc34303ce35cda00823b66f34cf9` | 0 |
| community/daml-lf/validation/src/main/scala/com/digitalasset/daml/lf/validation/DependencyVersion.scala | 775 | `95a73e1e9f2407a7cfa6e94a4f087304902b1a4bdfda7ba4adbe14659d1002ca` | 0 |
| community/daml-lf/validation/src/main/scala/com/digitalasset/daml/lf/validation/NamedEntity.scala | 4880 | `3f69049f05ae2ef49ecb37bdec1bf790b65512cd7a31db4e8e720cf0596844d4` | 0 |
| community/daml-lf/validation/src/main/scala/com/digitalasset/daml/lf/validation/Recursion.scala | 2051 | `70ce2be59ef28483661bf7ae51de66d53862ed8094df23514678aa8a5573f44d` | 0 |
| community/daml-lf/validation/src/main/scala/com/digitalasset/daml/lf/validation/Serializability.scala | 6490 | `7a5c3914412a07ebc4b3ae681317d923492a3c1933e549d9b9969baebecb3210` | 0 |
| community/daml-lf/validation/src/main/scala/com/digitalasset/daml/lf/validation/TypeSubst.scala | 2475 | `49c31e2314d69af903f35368d95355c87627d2711b164678762aa7b533bf3901` | 0 |
| community/daml-lf/validation/src/main/scala/com/digitalasset/daml/lf/validation/Typing.scala | 58389 | `e43d0623d85c7d4ded05d0fe3668079136062d1230c8a243ffa17fab96536de1` | 0 |
| community/daml-lf/validation/src/main/scala/com/digitalasset/daml/lf/validation/Upgrading.scala | 30380 | `359c249304fb88b6a6601faed598b0a17e18eb270e778d7ca14fb29afc06afa3` | 0 |
| community/daml-lf/validation/src/main/scala/com/digitalasset/daml/lf/validation/Util.scala | 1568 | `34290699d331d11668b344932549cf6820b86160d14a47d447dd6edb9579955d` | 0 |
| community/daml-lf/validation/src/main/scala/com/digitalasset/daml/lf/validation/Validation.scala | 2292 | `fc8b762897a816f42f3337a8e3d524ff81c2a91ece17ab19294589b6e03de4d3` | 0 |
| community/daml-lf/validation/src/main/scala/com/digitalasset/daml/lf/validation/ValidationError.scala | 20390 | `1548b195725f051902ee85142cffe8c7e8b64f55c7d1765975bc6b28e5d653e4` | 0 |
| community/kms-driver-api/src/main/scala/com/digitalasset/canton/crypto/kms/driver/api/KmsDriver.scala | 210 | `52f67ae07a0a07ebed4bd73d778527ee252e0445551e7060c038e617e54ea303` | 0 |
| community/kms-driver-api/src/main/scala/com/digitalasset/canton/crypto/kms/driver/api/KmsDriverFactory.scala | 336 | `60144db63893a24b24e3b149ee9716c56d722a712655f4862d8970fe7ef17131` | 0 |
| community/kms-driver-api/src/main/scala/com/digitalasset/canton/crypto/kms/driver/api/v1/KmsDriver.scala | 8539 | `2f987590247cb40670a9e635224fb33e0b42354c4182c6a8d042fc778ec230a8` | 0 |
| community/kms-driver-api/src/main/scala/com/digitalasset/canton/crypto/kms/driver/api/v1/KmsDriverException.scala | 661 | `00799ebe81d3cb7905062338a2ba98fe1436000eeeba88ba0822b7d6b45140af` | 0 |
| community/kms-driver-api/src/main/scala/com/digitalasset/canton/crypto/kms/driver/api/v1/KmsDriverFactory.scala | 445 | `7ad69edc8107efdc60fdc8200819e3b5bbed857a054f6e1ec6a874ffef381db8` | 0 |
| community/kms-driver-api/src/main/scala/com/digitalasset/canton/crypto/kms/driver/api/v1/KmsDriverHealth.scala | 1298 | `3f60c61e129d8d86063885a294930ec8efb39a8b807fdfd984349a6e74460252` | 0 |
| community/kms-driver-api/src/main/scala/com/digitalasset/canton/crypto/kms/driver/api/v1/KmsDriverSpecs.scala | 2514 | `fc114b3468d4a4594e3f988c87ea9127c66e96049a9334c616d90e1112bdf998` | 0 |
| community/kms-driver-api/src/main/scala/com/digitalasset/canton/driver/api/DriverFactory.scala | 533 | `210f5e3cdfcfab3d6fdf66919f9c24fbe629b972defb99d42a84b31593526ea2` | 0 |
| community/kms-driver-api/src/main/scala/com/digitalasset/canton/driver/api/v1/DriverFactory.scala | 1956 | `191b9df80c1790c0a10225fa79a76a2fbedea73215a98690c7ee5224b8d691c8` | 0 |
| community/ledger-api-bench-tool/src/main/scala/com/digitalasset/canton/ledger/api/benchtool/AuthorizationHelper.scala | 1312 | `97922b05cbff36ae9ba4ee0ed12959ce2aa5e5d58d2434e361cdd9ee0a770a08` | 0 |
| community/ledger-api-bench-tool/src/main/scala/com/digitalasset/canton/ledger/api/benchtool/Benchmark.scala | 6537 | `cbc62750adae6551254df933477767a36208e8215f29b4e60bd8bcbe26eb0789` | 0 |
| community/ledger-api-bench-tool/src/main/scala/com/digitalasset/canton/ledger/api/benchtool/ConfigEnricher.scala | 4531 | `c5761cc114ddb26f1fc5de4c78519f16f98aca5d7f30074cd309aceb77747a14` | 0 |
| community/ledger-api-bench-tool/src/main/scala/com/digitalasset/canton/ledger/api/benchtool/LedgerApiBenchTool.scala | 17312 | `150be7ee35f5e37b73e9c27d2beeb65475d99bb72672964b36feff924cbf81cb` | 0 |
| community/ledger-api-bench-tool/src/main/scala/com/digitalasset/canton/ledger/api/benchtool/PostgresUtils.scala | 1624 | `243652f84796c5e52f0deb67546471cbc7cacab15ef801840aedf906596de05f` | 0 |
| community/ledger-api-bench-tool/src/main/scala/com/digitalasset/canton/ledger/api/benchtool/PruningBenchmark.scala | 4913 | `30f01a88c5a7f3054590a6e0065c2f76a8189fc62e0270f65e704e7a1445d470` | 0 |
| community/ledger-api-bench-tool/src/main/scala/com/digitalasset/canton/ledger/api/benchtool/SubmittedDataAnalyzing.scala | 1447 | `b8cedef83b67ebbbb49759822e60b694e81bdd2a89a1f43e0493d77e581e2175` | 0 |
| community/ledger-api-bench-tool/src/main/scala/com/digitalasset/canton/ledger/api/benchtool/config/Cli.scala | 19150 | `1642737c9dcf07d146ce2fe4f15cb1ac2f7b895e173d57dbe6bd2a4dd3e6f08d` | 0 |
| community/ledger-api-bench-tool/src/main/scala/com/digitalasset/canton/ledger/api/benchtool/config/Config.scala | 1655 | `45d8c42db9580aed147b5237b34967d378189c49e67ab3922d090126e3400de4` | 0 |
| community/ledger-api-bench-tool/src/main/scala/com/digitalasset/canton/ledger/api/benchtool/config/ConfigMaker.scala | 1575 | `b341fdb47047a35e129f516a7ffc6d49c77586e4f227c47bb81cc2e1995422c7` | 0 |
| community/ledger-api-bench-tool/src/main/scala/com/digitalasset/canton/ledger/api/benchtool/config/WorkflowConfig.scala | 7541 | `c6eb51a94ae5dd4f4a2523b09adb93ac33f34486764c7fe1188b77514a6d5c5c` | 0 |
| community/ledger-api-bench-tool/src/main/scala/com/digitalasset/canton/ledger/api/benchtool/config/WorkflowConfigParser.scala | 13955 | `857951ce4f6a4ecfe4186286a1aca8a8da217cbaef2823f3a7188e30aae65ea8` | 0 |
| community/ledger-api-bench-tool/src/main/scala/com/digitalasset/canton/ledger/api/benchtool/infrastructure/TestDars.scala | 1641 | `97cb67bfab16b1af40bf20ffcba03206f0d388507056f6f702f6a87a4a6a7d1f` | 0 |
| community/ledger-api-bench-tool/src/main/scala/com/digitalasset/canton/ledger/api/benchtool/metrics/BenchmarkResult.scala | 402 | `18416b8a2890138e9baa59fc93fb9c28f3cf1a245e6a4dc47889c9dfa0741354` | 0 |
| community/ledger-api-bench-tool/src/main/scala/com/digitalasset/canton/ledger/api/benchtool/metrics/ConsumptionSpeedMetric.scala | 3813 | `79f763cb7734b084c79c6b95ac8538c24c875b07f3c7f3ce3394638a446e5b39` | 0 |
| community/ledger-api-bench-tool/src/main/scala/com/digitalasset/canton/ledger/api/benchtool/metrics/CountRateMetric.scala | 3561 | `c013b17fe1e32d77d9ead4e3fdcc01638de980c33e28194b74e626a262ef13ce` | 0 |
| community/ledger-api-bench-tool/src/main/scala/com/digitalasset/canton/ledger/api/benchtool/metrics/DelayMetric.scala | 3723 | `d9081850639f4cc55111d991df3c742674ec8fbf70fe5a4c0f02891e7b65f1c9` | 0 |
| community/ledger-api-bench-tool/src/main/scala/com/digitalasset/canton/ledger/api/benchtool/metrics/ExposedMetrics.scala | 3604 | `83ff561dc5990fbd733263c92cc72c2f669f1871f34005194842b1c16b1c20f6` | 0 |
| community/ledger-api-bench-tool/src/main/scala/com/digitalasset/canton/ledger/api/benchtool/metrics/LatencyMetric.scala | 1817 | `2c93241f2cbb0299db3ce28f9836152d699e523f48920503ab71b1d73a13aa1b` | 0 |
| community/ledger-api-bench-tool/src/main/scala/com/digitalasset/canton/ledger/api/benchtool/metrics/MeteredStreamObserver.scala | 966 | `5eabc7d21e965e5699efd6680ba32e2907458a01f95bf941516d1aec74df7eba` | 0 |
| community/ledger-api-bench-tool/src/main/scala/com/digitalasset/canton/ledger/api/benchtool/metrics/Metric.scala | 1319 | `de0f30a9454d2f407771045c0eef974d2a6acdb83ef5a383e06dad130c92d5ff` | 0 |
| community/ledger-api-bench-tool/src/main/scala/com/digitalasset/canton/ledger/api/benchtool/metrics/MetricRegistryOwner.scala | 1329 | `208c368c1d7441bed670c71a852941f39a40dadf93b52b25bee3cc3c6864ea5e` | 0 |
| community/ledger-api-bench-tool/src/main/scala/com/digitalasset/canton/ledger/api/benchtool/metrics/MetricValue.scala | 219 | `032006c9ccdcaba092341a9de79f369b12e4049e8c3df16412910924ae579c18` | 0 |
| community/ledger-api-bench-tool/src/main/scala/com/digitalasset/canton/ledger/api/benchtool/metrics/MetricsCollector.scala | 3858 | `1a56e6f95807c272110d30cb4e4dc9f693d8f5e948f3c2b4e41542dec05bbc62` | 0 |
| community/ledger-api-bench-tool/src/main/scala/com/digitalasset/canton/ledger/api/benchtool/metrics/MetricsManager.scala | 3807 | `9cafbb86073596c6bcabfe8af6d621b8330a27b6ad3c190751742fc7cee56dde` | 0 |
| community/ledger-api-bench-tool/src/main/scala/com/digitalasset/canton/ledger/api/benchtool/metrics/MetricsSet.scala | 6717 | `6b6aecb3b54edaab1a0ec00ea91c41a4dde7c75033da5ebac05e5e74b500faa2` | 0 |
| community/ledger-api-bench-tool/src/main/scala/com/digitalasset/canton/ledger/api/benchtool/metrics/ServiceLevelObjective.scala | 323 | `33308110a7c47a7629cd68a380a20dce667408d824bbf28c9dcb83c0f09feae0` | 0 |
| community/ledger-api-bench-tool/src/main/scala/com/digitalasset/canton/ledger/api/benchtool/metrics/SizeMetric.scala | 1672 | `ae94983f220684c30295a6dde43d866b596032abb68c638ce781dca89bf3adbb` | 0 |
| community/ledger-api-bench-tool/src/main/scala/com/digitalasset/canton/ledger/api/benchtool/metrics/StreamMetrics.scala | 1186 | `7fdd0c82fe1300d400bc313563d56dd3ee9d867babe2e8c56f47d30353cdbb1b` | 0 |
| community/ledger-api-bench-tool/src/main/scala/com/digitalasset/canton/ledger/api/benchtool/metrics/TotalCountMetric.scala | 1065 | `1961ea855bb79968ffd334c3c43e27fa8e46caa8541bcf94744287b8e30e2b5c` | 0 |
| community/ledger-api-bench-tool/src/main/scala/com/digitalasset/canton/ledger/api/benchtool/metrics/metrics/TotalRuntimeMetric.scala | 2368 | `46ea523dadde10b6df878f0447a125cf2ba51dc6eba5e93bed49fb0cae90dbf8` | 0 |
| community/ledger-api-bench-tool/src/main/scala/com/digitalasset/canton/ledger/api/benchtool/services/CommandCompletionService.scala | 2003 | `71c6bbe24251c0eff6fae17b4472ab511896796df65281b3a7f3ee09e2d60961` | 0 |
| community/ledger-api-bench-tool/src/main/scala/com/digitalasset/canton/ledger/api/benchtool/services/CommandService.scala | 1267 | `ab29080c2a93e8602cfd8fa72588d67038acc7ef2758e4ae613d6c6d8f626c93` | 0 |
| community/ledger-api-bench-tool/src/main/scala/com/digitalasset/canton/ledger/api/benchtool/services/CommandSubmissionService.scala | 1294 | `e1ece407044ae8a4d7417688fc104e36a6840c052f419e8de78afcd4de4ba541` | 0 |
| community/ledger-api-bench-tool/src/main/scala/com/digitalasset/canton/ledger/api/benchtool/services/LedgerApiServices.scala | 2094 | `baf0aaab17eb47eb6a230f5d8d3db35847d952c14f3770d08f64901ac57f4afb` | 0 |
| community/ledger-api-bench-tool/src/main/scala/com/digitalasset/canton/ledger/api/benchtool/services/PackageManagementService.scala | 1231 | `2f6dae9bed6ea442880101c676ac926d9d7b58853040ae9f02ad8dec4adfb1d0` | 0 |
| community/ledger-api-bench-tool/src/main/scala/com/digitalasset/canton/ledger/api/benchtool/services/PackageService.scala | 936 | `2420b797b46b3fa03a7b7b30dc47aa0aed72e26a46ccd69a519debcb2c36d39b` | 0 |
| community/ledger-api-bench-tool/src/main/scala/com/digitalasset/canton/ledger/api/benchtool/services/PartyManagementService.scala | 2425 | `9d12073ea2b3a6702cc3bb3ee78e1548473e9c1e720b8f701887d3066c995940` | 0 |
| community/ledger-api-bench-tool/src/main/scala/com/digitalasset/canton/ledger/api/benchtool/services/PruningService.scala | 916 | `52e25c24024be50d4c0fdf2548998f68c2886d77ed08bf768a80281599792d0b` | 0 |
| community/ledger-api-bench-tool/src/main/scala/com/digitalasset/canton/ledger/api/benchtool/services/StateService.scala | 2210 | `227b6ae07aee1b48d118b4261e6300172ceb0d50c6a1e2aa9f2878eb9922715b` | 0 |
| community/ledger-api-bench-tool/src/main/scala/com/digitalasset/canton/ledger/api/benchtool/services/StreamFilters.scala | 3388 | `a33cdb4e55e04d87bb4f531232fbda2dc5175332b6f44fdd889ead77ec8dc8b6` | 0 |
| community/ledger-api-bench-tool/src/main/scala/com/digitalasset/canton/ledger/api/benchtool/services/UpdateService.scala | 3881 | `440be4da7d07642cd06e45ee69183ddb87cbfdf4ecfa47956b4f5da7cbce2b5a` | 0 |
| community/ledger-api-bench-tool/src/main/scala/com/digitalasset/canton/ledger/api/benchtool/services/UserManagementService.scala | 3217 | `93b39ee5f0c2b61516277c0ab853ceb24bb83294456ce1d4d3b31372f5a103c8` | 0 |
| community/ledger-api-bench-tool/src/main/scala/com/digitalasset/canton/ledger/api/benchtool/submission/ActiveContractKeysPool.scala | 1874 | `94b9ccb9e01e82a599a26508b9f631711cf9f9d3ecf6dc506a228d03c7d3ae86` | 0 |
| community/ledger-api-bench-tool/src/main/scala/com/digitalasset/canton/ledger/api/benchtool/submission/AllocatedParties.scala | 2101 | `2afe20f521f779a41d0bb954457e01cf3fd5813b5d9730cc718434ade543e2e7` | 0 |
| community/ledger-api-bench-tool/src/main/scala/com/digitalasset/canton/ledger/api/benchtool/submission/AllocatedPartySet.scala | 633 | `6ad7c3982436b80bd10ca2bdbafc82ad940aed1f73a8a722efa27d5866c8c035` | 0 |
| community/ledger-api-bench-tool/src/main/scala/com/digitalasset/canton/ledger/api/benchtool/submission/BenchtoolTestsPackageInfo.scala | 566 | `89dd8fc0d016b713fb5e96e588e389be349cbf7665bb0e2930847ea2ddd548d2` | 0 |
| community/ledger-api-bench-tool/src/main/scala/com/digitalasset/canton/ledger/api/benchtool/submission/CommandGenerator.scala | 1292 | `43482e5c21d50013838dc21e6b55e15b826837e575cecb89c36282f014c761a1` | 0 |
| community/ledger-api-bench-tool/src/main/scala/com/digitalasset/canton/ledger/api/benchtool/submission/CommandSubmitter.scala | 11118 | `e13964b338788a7a47b2be186cc00f6eb17742476217963bcfcc5f9a05a0de27` | 0 |
| community/ledger-api-bench-tool/src/main/scala/com/digitalasset/canton/ledger/api/benchtool/submission/Distribution.scala | 1222 | `2c92f39472454cc7465b5fe31cb64156cbc94fea08cedccbc7d797eebc1d55e1` | 0 |
| community/ledger-api-bench-tool/src/main/scala/com/digitalasset/canton/ledger/api/benchtool/submission/FibonacciCommandGenerator.scala | 2165 | `aae3f8b1fe62362d211aca1168872aaf7d5d3d84bc448d73cc44587b38bf6baa` | 0 |
| community/ledger-api-bench-tool/src/main/scala/com/digitalasset/canton/ledger/api/benchtool/submission/FooCommandGenerator.scala | 12550 | `424fc2c2c923d1405dc0837ad7fd513083867e38f8525f7c23b53c1315217ef8` | 0 |
| community/ledger-api-bench-tool/src/main/scala/com/digitalasset/canton/ledger/api/benchtool/submission/FooDivulgerCommandGenerator.scala | 3885 | `f8a77d9edc0890d5d6e71d57434f3f8038e57121e9cca931fbd4b8f48ef369e8` | 0 |
| community/ledger-api-bench-tool/src/main/scala/com/digitalasset/canton/ledger/api/benchtool/submission/FooSubmission.scala | 2904 | `db2ffe218d740b6c293c3666dfd108fe34787831f7a0d762ac8ec6753f55bf17` | 0 |
| community/ledger-api-bench-tool/src/main/scala/com/digitalasset/canton/ledger/api/benchtool/submission/FooTemplateDescriptor.scala | 2819 | `eecd6539eefa3d3d4194360fcf449401e0f15d33b984a31384ae63d525a67dfb` | 0 |
| community/ledger-api-bench-tool/src/main/scala/com/digitalasset/canton/ledger/api/benchtool/submission/Names.scala | 3223 | `0dede032ae44960ea527133bd0c8ca9ff919e31c74a9baaf09aa53917fdc29dd` | 0 |
| community/ledger-api-bench-tool/src/main/scala/com/digitalasset/canton/ledger/api/benchtool/submission/PartyAllocating.scala | 3698 | `c2560afb7d631c9419171e916f149e94eb4bbcbe54b16166f36865a5f2a50805` | 0 |
| community/ledger-api-bench-tool/src/main/scala/com/digitalasset/canton/ledger/api/benchtool/submission/RandomnessProvider.scala | 1162 | `03d54bfe6e85eea958a9f974a9fbe6a12e8886075e27710ae831d29b3ef948b9` | 0 |
| community/ledger-api-bench-tool/src/main/scala/com/digitalasset/canton/ledger/api/benchtool/submission/foo/PartiesSelection.scala | 344 | `2063a7ee7b64d112b01b553b1dc783d9f6ab7524c0073c26838097bcf4d598b3` | 0 |
| community/ledger-api-bench-tool/src/main/scala/com/digitalasset/canton/ledger/api/benchtool/submission/foo/RandomPartySelecting.scala | 2557 | `69cb9e490e569aee75e9672be1c1d900a6d0efecd6b617a34698333f141063f7` | 0 |
| community/ledger-api-bench-tool/src/main/scala/com/digitalasset/canton/ledger/api/benchtool/util/ObserverWithResult.scala | 2177 | `2e1ac14d0b76e0e94c524cd27437c5aeb909e39188221d76b64608b5381fe179` | 0 |
| community/ledger-api-bench-tool/src/main/scala/com/digitalasset/canton/ledger/api/benchtool/util/ReportFormatter.scala | 5622 | `ace1507add351d82fb5fe03b4041df9883793cfc731fbb0975342ae752831baf` | 0 |
| community/ledger-api-bench-tool/src/main/scala/com/digitalasset/canton/ledger/api/benchtool/util/SimpleFileReader.scala | 626 | `c034b72a961e6c0a64d20bf5161157aa99996b1b1859db7b3db1e79f8ccb7e38` | 0 |
| community/ledger-api-bench-tool/src/main/scala/com/digitalasset/canton/ledger/api/benchtool/util/TimeUtil.scala | 805 | `a069faffb33e0d34ed20b10184d132af089163042858e050ae1ffa908a440bec` | 0 |
| community/ledger-api-bench-tool/src/main/scala/com/digitalasset/canton/ledger/api/benchtool/util/TypedActorSystemResourceOwner.scala | 1327 | `4e82bd6ef988a17e361b859d0ea4234042e0a1ce3aa3bf7b0f07b3320de977a2` | 0 |
| community/ledger-api-proto/src/main/protobuf/com/daml/ledger/api/v2/admin/command_inspection_service.proto | 3879 | `9fd2fa5cabb9f70ba0929e2d71ab05073a73ccc6badb187490c883f92ea28704` | 0 |
| community/ledger-api-proto/src/main/protobuf/com/daml/ledger/api/v2/admin/identity_provider_config_service.proto | 6649 | `41054314dc2c025220dd2d5b5324c9e57c3aee1bf674166667f578614c9a3738` | 0 |
| community/ledger-api-proto/src/main/protobuf/com/daml/ledger/api/v2/admin/object_meta.proto | 3615 | `2bedbe155b924d5ff50513106f72f70ca969203c92e438e989c343e2ad46b101` | 0 |
| community/ledger-api-proto/src/main/protobuf/com/daml/ledger/api/v2/admin/package_management_service.proto | 10682 | `69260e3d51e005410816bedfb8da034fa810d4da035f56180c294f7787a17f66` | 0 |
| community/ledger-api-proto/src/main/protobuf/com/daml/ledger/api/v2/admin/participant_pruning_service.proto | 2197 | `cc515b2da4f209ef15c25f76258ca91a6b9965bbfa5c701eac1515e48e4d8656` | 0 |
| community/ledger-api-proto/src/main/protobuf/com/daml/ledger/api/v2/admin/party_management_alpha_service.proto | 6511 | `518bb1652e177cf8a5a32a2304c18077b4f2b0bfd7929feb2040ebec49018c47` | 0 |
| community/ledger-api-proto/src/main/protobuf/com/daml/ledger/api/v2/admin/party_management_service.proto | 18888 | `5561675f6fd79d369d096f8f65e7b14abc1a4ea20524dcc7c869197cff15afa4` | 0 |
| community/ledger-api-proto/src/main/protobuf/com/daml/ledger/api/v2/admin/user_management_service.proto | 15547 | `ff7118f4d3c052056b246868beb28f00a6091bd58b88189699490ac5565f0e32` | 0 |
| community/ledger-api-proto/src/main/protobuf/com/daml/ledger/api/v2/command_completion_service.proto | 5499 | `0178ee1e98915a7ae9d972592d5761de1ebe9812375e3876aa1ce35d50116c86` | 0 |
| community/ledger-api-proto/src/main/protobuf/com/daml/ledger/api/v2/command_service.proto | 3989 | `cc09ef52d4c71fd072661052eaf4a1f4ecac9e7eeb8d1672184c18a7958bb7cb` | 0 |
| community/ledger-api-proto/src/main/protobuf/com/daml/ledger/api/v2/command_submission_service.proto | 2164 | `5f494dded547f0250f5e3b81cee2d6e56bd500cf0b8ea0ff3516f6825f468980` | 0 |
| community/ledger-api-proto/src/main/protobuf/com/daml/ledger/api/v2/commands.proto | 12430 | `b963e83da25035e972a7f499403a8d28d33029e7ea8fd9bb09aea252812dee4e` | 0 |
| community/ledger-api-proto/src/main/protobuf/com/daml/ledger/api/v2/completion.proto | 6414 | `e9157fe8b73b4ebae5075aebaa475661d2a6fd2fd8c16df7813819fb4ce2a5c6` | 0 |
| community/ledger-api-proto/src/main/protobuf/com/daml/ledger/api/v2/contract_service.proto | 2153 | `b9de4caa97508b164422fa2f8c50c386923a6e1d93c84f3ff0850de238cb2e95` | 0 |
| community/ledger-api-proto/src/main/protobuf/com/daml/ledger/api/v2/crypto.proto | 3759 | `dbf1e5227b917ee66a7e3ebbe062bbfcf36a5a9a47c35ed334ff8f8e3da7dd54` | 0 |
| community/ledger-api-proto/src/main/protobuf/com/daml/ledger/api/v2/event.proto | 14250 | `39cc6325a82b9de17ee42f015a5913c2a975c857208fecd9726ccc16c2994c08` | 0 |
| community/ledger-api-proto/src/main/protobuf/com/daml/ledger/api/v2/event_query_service.proto | 2511 | `ca48154c6623bb88a95f86c1afae80e2a9707abc61795ddf3477a65fd86fcdb3` | 0 |
| community/ledger-api-proto/src/main/protobuf/com/daml/ledger/api/v2/experimental_features.proto | 1174 | `a60bf5503992060ded3923a9e949c007b256bcdde45602c2197228c5a442fc42` | 0 |
| community/ledger-api-proto/src/main/protobuf/com/daml/ledger/api/v2/interactive/interactive_submission_common_data.proto | 887 | `72dc504747cb7545b51f3b19ee3567b0835194e599fc8ca194128e7242ebb577` | 0 |
| community/ledger-api-proto/src/main/protobuf/com/daml/ledger/api/v2/interactive/interactive_submission_service.proto | 33022 | `af78ec90ac32ab0044ed8c33d27e54fda239b013ce54fd49c77ac8c032ef60b9` | 0 |
| community/ledger-api-proto/src/main/protobuf/com/daml/ledger/api/v2/interactive/transaction/v1/interactive_submission_data.proto | 5036 | `5e550f8e96f207ca3eb51a7b53a042bdb056c6c61265370f69b60653da91c962` | 0 |
| community/ledger-api-proto/src/main/protobuf/com/daml/ledger/api/v2/jose_service.proto | 1007 | `0c1e539cfd7478ce81c7fbbf5ed61b74f13278bc5ecc654574332baf464aacb3` | 0 |
| community/ledger-api-proto/src/main/protobuf/com/daml/ledger/api/v2/offset_checkpoint.proto | 1248 | `f9307a4da9812b7466e0e2314ffa7cc639080135debf5d7319116d18b0a910c8` | 0 |
| community/ledger-api-proto/src/main/protobuf/com/daml/ledger/api/v2/package_reference.proto | 2915 | `1b263f7c2239c2ab1cee7ee3d57f85e6e29ef359238c2474d80020f130d3c74a` | 0 |
| community/ledger-api-proto/src/main/protobuf/com/daml/ledger/api/v2/package_service.proto | 6623 | `2eb1baa078781f6a36ea4ac8d2b2622ae9a692719ea33a5aff997fe17cc3c3c7` | 0 |
| community/ledger-api-proto/src/main/protobuf/com/daml/ledger/api/v2/reassignment.proto | 7191 | `2b0673e82384fd8e150713268c1a26848d0a4d181b1e79d054c9e834b86656bd` | 0 |
| community/ledger-api-proto/src/main/protobuf/com/daml/ledger/api/v2/reassignment_commands.proto | 3954 | `db32013bcff73784776b7496dba3cff8b6c6dabf96b87630bd9658c96d7c7523` | 0 |
| community/ledger-api-proto/src/main/protobuf/com/daml/ledger/api/v2/size_config_options.proto | 765 | `473df1d2d4c86ee384ef11d414a3e0167a2cb4d3c45d92ccca1f021619fc2e25` | 0 |
| community/ledger-api-proto/src/main/protobuf/com/daml/ledger/api/v2/state_service.proto | 16223 | `a8dcd489d0770c2b7817a147592ff07d48bcf766efb49d8e949e49fbf29b93ff` | 0 |
| community/ledger-api-proto/src/main/protobuf/com/daml/ledger/api/v2/topology_transaction.proto | 3326 | `95ce991207f13d09bc9bf353f752986a8913716b3404e96ce0c1ef611ea2142a` | 0 |
| community/ledger-api-proto/src/main/protobuf/com/daml/ledger/api/v2/trace_context.proto | 519 | `5d160ddcb6582c3f0379270e588802cac49d9c5c9925e81681f541b58849f0b7` | 0 |
| community/ledger-api-proto/src/main/protobuf/com/daml/ledger/api/v2/transaction.proto | 4156 | `65bb645c2190464a9f67c0f12141c353b4c472c34b0f9b5b21d4ec7e9bd80a44` | 0 |
| community/ledger-api-proto/src/main/protobuf/com/daml/ledger/api/v2/transaction_filter.proto | 8822 | `8aab74ace0f4bbd231bafc8e4251487bb4b6a4e4e3d2c58fc3c33ee980cda643` | 0 |
| community/ledger-api-proto/src/main/protobuf/com/daml/ledger/api/v2/update_service.proto | 8834 | `3834ec388223a93dce4b29b036ca3e9f02c2cef44ff57e58aeaa7502b0d770b2` | 0 |
| community/ledger-api-proto/src/main/protobuf/com/daml/ledger/api/v2/version_service.proto | 3790 | `1627ecb485ff9974962a262b4c7947b2d885954bdb0293eb29af0e4a756bede5` | 0 |
| community/ledger-api-scala/src/main/protobuf/com/daml/ledger/api/scalapb/package.proto | 371 | `e92fd7967929d4bdaee8ae67fd01e0697540cf1acedf74479992e8c99b32f740` | 0 |
| community/ledger-api-size-config/src/main/scala/com/digitalasset/canton/ledger/api/sizeconfig/v2/CommandsSizeConfig.scala | 1839 | `35c689a6a665e0dc8cd7e3c7c1d0fb2185604b30c7d1b27e4243fe668353dc20` | 0 |
| community/ledger-api-size-config/src/main/scala/com/digitalasset/canton/ledger/api/sizeconfig/v2/CompletionStreamRequestSizeConfig.scala | 1245 | `4b0f177b024f54e2915f76a8cc43a942e84069ae5eec04e24df37196a86afeac` | 0 |
| community/ledger-api-size-config/src/main/scala/com/digitalasset/canton/ledger/api/sizeconfig/v2/CreateAndExerciseCommandSizeConfig.scala | 1439 | `1bee5ad8297c701e92b308f940ebd626a1fbe48a6d67c87fb3fdb37051f8ca37` | 0 |
| community/ledger-api-size-config/src/main/scala/com/digitalasset/canton/ledger/api/sizeconfig/v2/CreateCommandSizeConfig.scala | 1162 | `b48b10da920292e7991916ecb4dec9412461f08532eca37a476e32d15642ae90` | 0 |
| community/ledger-api-size-config/src/main/scala/com/digitalasset/canton/ledger/api/sizeconfig/v2/DisclosedContractSizeConfig.scala | 1200 | `8cdb3fb9dcd578af01dd7735ccdfe786a62a097c14b84a4973befec59cf67b11` | 0 |
| community/ledger-api-size-config/src/main/scala/com/digitalasset/canton/ledger/api/sizeconfig/v2/EventFormatSizeConfig.scala | 1128 | `1f3a6b82f5e1284649562acc6edac7191c264c343e6a02bc0160d55d61816a66` | 0 |
| community/ledger-api-size-config/src/main/scala/com/digitalasset/canton/ledger/api/sizeconfig/v2/ExerciseByKeyCommandSizeConfig.scala | 1381 | `018db74dbd257edcf41af5a7d1c17a7a8212d3728c08ad4cbc93cd4a0626e9e2` | 0 |
| community/ledger-api-size-config/src/main/scala/com/digitalasset/canton/ledger/api/sizeconfig/v2/ExerciseCommandSizeConfig.scala | 1187 | `aa06192b5b9a0d6102377649b18cff52517cd3eea5adf4efbf4af97d3abfcd6c` | 0 |
| community/ledger-api-size-config/src/main/scala/com/digitalasset/canton/ledger/api/sizeconfig/v2/FiltersSizeConfig.scala | 1080 | `ccf0993ce4b056d434f953ff09d0810ed8c6183ed5d647f812f6973ddeba4c19` | 0 |
| community/ledger-api-size-config/src/main/scala/com/digitalasset/canton/ledger/api/sizeconfig/v2/GetActiveContractsPageRequestSizeConfig.scala | 1304 | `8a2b99e7020ed1b70eef51bcd35ba34e0449beef7d695c0cdfaa2c893bab1822` | 0 |
| community/ledger-api-size-config/src/main/scala/com/digitalasset/canton/ledger/api/sizeconfig/v2/GetActiveContractsRequestSizeConfig.scala | 1307 | `108dd484680925720a478ca03347df41a057290b8479460dfa82163a4bf1f6e2` | 0 |
| community/ledger-api-size-config/src/main/scala/com/digitalasset/canton/ledger/api/sizeconfig/v2/GetCompletionByHashRequestSizeConfig.scala | 1292 | `476f6f9dcca7577474a010435c01e4ce05dd6cab5dceaa35cac3b7d9db049b16` | 0 |
| community/ledger-api-size-config/src/main/scala/com/digitalasset/canton/ledger/api/sizeconfig/v2/GetCompletionsRequestSizeConfig.scala | 1225 | `2995f92f2477d236c069467ded2662c24ad9322437d1793340f594385b9f7119` | 0 |
| community/ledger-api-size-config/src/main/scala/com/digitalasset/canton/ledger/api/sizeconfig/v2/GetContractRequestSizeConfig.scala | 1214 | `393775dbbe2e5cc6c4f0647b9d0ba0a75ef88176d5c2274f37db42c528f444e6` | 0 |
| community/ledger-api-size-config/src/main/scala/com/digitalasset/canton/ledger/api/sizeconfig/v2/GetLedgerEndRequestSizeConfig.scala | 1221 | `df26d8f1584a5983d418681716652cab1ad4b36e6fd1bf95b2eace57dc72e8b7` | 0 |
| community/ledger-api-size-config/src/main/scala/com/digitalasset/canton/ledger/api/sizeconfig/v2/GetUpdateByHashRequestSizeConfig.scala | 1252 | `88405825aa38bd8bed49e0658b31565bebcee48bad62483305438da220d18beb` | 0 |
| community/ledger-api-size-config/src/main/scala/com/digitalasset/canton/ledger/api/sizeconfig/v2/GetUpdatesPageRequestSizeConfig.scala | 1224 | `300d291d13425b5ea50b844cc4ab3e7da795f12f16436179529de76b7e05b19f` | 0 |
| community/ledger-api-size-config/src/main/scala/com/digitalasset/canton/ledger/api/sizeconfig/v2/PackageMetadataFilterSizeConfig.scala | 1398 | `a6b6b41ede3d774cf4d649660b6f927389328c8491e63f9766cef092452b9df5` | 0 |
| community/ledger-api-size-config/src/main/scala/com/digitalasset/canton/ledger/api/sizeconfig/v2/ParticipantAuthorizationTopologyFormatSizeConfig.scala | 1395 | `1b28606040d377b1e42b09c2109ef4a7ebda31051a3f28aafb72555be63f9214` | 0 |
| community/ledger-api-size-config/src/main/scala/com/digitalasset/canton/ledger/api/sizeconfig/v2/PrefetchContractKeySizeConfig.scala | 1218 | `b8206f1fb4f08ba2d00fc7c4f992dea496a47fd858fd7603b6cbf4f7ed3a5181` | 0 |
| community/ledger-api-size-config/src/main/scala/com/digitalasset/canton/ledger/api/sizeconfig/v2/PublicLapiSizeConfig.scala | 2288 | `58dc5d258b59b1c95daf108fc3ca3c90e13b1185d5589c9d2b791f7f57c15997` | 0 |
| community/ledger-api-size-config/src/main/scala/com/digitalasset/canton/ledger/api/sizeconfig/v2/ReassignmentCommandsSizeConfig.scala | 1212 | `11bc832e7dae5d60d384c27c5db6b017498a2e31c6f51f2e74ac5bcd46414de3` | 0 |
| community/ledger-api-size-config/src/main/scala/com/digitalasset/canton/ledger/api/sizeconfig/v2/SignatureSizeConfig.scala | 1089 | `b3451a35a3cc8613240611f78bc83e3ab685d8cebd58442e65dbe418eca34fa6` | 0 |
| community/ledger-api-size-config/src/main/scala/com/digitalasset/canton/ledger/api/sizeconfig/v2/SigningPublicKeySizeConfig.scala | 1162 | `f75ae4e2d46858c9aeef87f4d1baed627493e5f111cb9b1f86e88151073af84e` | 0 |
| community/ledger-api-size-config/src/main/scala/com/digitalasset/canton/ledger/api/sizeconfig/v2/TopologyStateFilterSizeConfig.scala | 1371 | `36b40ec3b292d95ed0408c4335ae703fa2bed0b1cb5e22db3af4cd0cb4b7403b` | 0 |
| community/ledger-api-size-config/src/main/scala/com/digitalasset/canton/ledger/api/sizeconfig/v2/admin/AdminLapiSizeConfig.scala | 2088 | `9d3f52ec1a67e48f43ab2b21f9aa9f30d94a72178f4d7a6ada4f0baa71604573` | 0 |
| community/ledger-api-size-config/src/main/scala/com/digitalasset/canton/ledger/api/sizeconfig/v2/admin/AllocateExternalPartyRequestSignedTransactionSizeConfig.scala | 1634 | `c62b924eec67820b913e14699209bcbb1975fa41b5e2ace699579de2da1fe925` | 0 |
| community/ledger-api-size-config/src/main/scala/com/digitalasset/canton/ledger/api/sizeconfig/v2/admin/AllocateExternalPartyRequestSizeConfig.scala | 1522 | `c45ee3c1033d071855e36e639f85e24f369c468d6e892e1d17ce897ed9ff70bf` | 0 |
| community/ledger-api-size-config/src/main/scala/com/digitalasset/canton/ledger/api/sizeconfig/v2/admin/AuthorizePartyUpdateRequestSizeConfig.scala | 1441 | `4e72bf4973cfb2983acbf4ad1f05606c8f8939cd4aef41edd2d1e3fdda2d3d7f` | 0 |
| community/ledger-api-size-config/src/main/scala/com/digitalasset/canton/ledger/api/sizeconfig/v2/admin/CreateUserRequestSizeConfig.scala | 1194 | `9853d946d0f0113accf9c25404210703e3c64c09cc5fd0e8684e5650ae4ffb93` | 0 |
| community/ledger-api-size-config/src/main/scala/com/digitalasset/canton/ledger/api/sizeconfig/v2/admin/GenerateExternalPartyTopologyRequestSizeConfig.scala | 1647 | `04cffc633094f914ec1aec7f57ad69c51a96e573063ef8f16911deb50cf95254` | 0 |
| community/ledger-api-size-config/src/main/scala/com/digitalasset/canton/ledger/api/sizeconfig/v2/admin/GetPartiesRequestSizeConfig.scala | 1197 | `53fd0d8b11f503629faa8a6fb69beb64ee9c71bba98660cdb048441655686205` | 0 |
| community/ledger-api-size-config/src/main/scala/com/digitalasset/canton/ledger/api/sizeconfig/v2/admin/GrantUserRightsRequestSizeConfig.scala | 1250 | `0f1b846ec934a58af8928635244bb3e47c17251b326315d3da9452d54ffd91b1` | 0 |
| community/ledger-api-size-config/src/main/scala/com/digitalasset/canton/ledger/api/sizeconfig/v2/admin/ObjectMetaSizeConfig.scala | 1125 | `46f86aea11c03391f04cc07b2467a181e2932f3e34eccb635a07e0295d409cce` | 0 |
| community/ledger-api-size-config/src/main/scala/com/digitalasset/canton/ledger/api/sizeconfig/v2/admin/RevokeUserRightsRequestSizeConfig.scala | 1260 | `b9e1710e78cbf4eb67f756f9583fa73a8adfda8d58b4649966cb2a7a2af5c234` | 0 |
| community/ledger-api-size-config/src/main/scala/com/digitalasset/canton/ledger/api/sizeconfig/v2/admin/UpdateIdentityProviderConfigRequestSizeConfig.scala | 1403 | `7cfea5f981d5fb5826f58c9ee4813d4085f54d42e2e1be09694d42f5ab42d239` | 0 |
| community/ledger-api-size-config/src/main/scala/com/digitalasset/canton/ledger/api/sizeconfig/v2/admin/UpdatePartyDetailsRequestSizeConfig.scala | 1299 | `fe05f5526b3a82cf58c5bbe2c77b864e1b7b301e0234f0bab26be6a37b453061` | 0 |
| community/ledger-api-size-config/src/main/scala/com/digitalasset/canton/ledger/api/sizeconfig/v2/admin/UpdateUserRequestSizeConfig.scala | 1213 | `dd971ac460a4dbcf4fcf43b32f61001670757425496ce26c22045036baae0358` | 0 |
| community/ledger-api-size-config/src/main/scala/com/digitalasset/canton/ledger/api/sizeconfig/v2/admin/UpdateVettedPackagesRequestSizeConfig.scala | 1501 | `b81392613484d90cbb74d08aea48908b8806049091d00d7721c210c03eeb78e2` | 0 |
| community/ledger-api-size-config/src/main/scala/com/digitalasset/canton/ledger/api/sizeconfig/v2/admin/UploadDarFileRequestSizeConfig.scala | 1220 | `7cc413b4d8ae8f88ab35a07629cb94f176d40425e53e133d447d57a2cb64c91f` | 0 |
| community/ledger-api-size-config/src/main/scala/com/digitalasset/canton/ledger/api/sizeconfig/v2/admin/ValidateDarFileRequestSizeConfig.scala | 1246 | `cf2cd05fa784da2da663d68f74052a2b4f977625b95bb8575ea7f9cfb0066dfd` | 0 |
| community/ledger-api-size-config/src/main/scala/com/digitalasset/canton/ledger/api/sizeconfig/v2/admin/VettedPackagesChangeUnvetSizeConfig.scala | 1288 | `fcea87ded01828022b578df51a5907b0c1b13fd1a769eb069fa54ea614d8c748` | 0 |
| community/ledger-api-size-config/src/main/scala/com/digitalasset/canton/ledger/api/sizeconfig/v2/admin/VettedPackagesChangeVetSizeConfig.scala | 1268 | `d8e1aacbed72ba97eae0072e7cc6eb8f4fd4e0cc3154f8f2e5890a102cadb971` | 0 |
| community/ledger-api-size-config/src/main/scala/com/digitalasset/canton/ledger/api/sizeconfig/v2/interactive/CostEstimationHintsSizeConfig.scala | 1269 | `c94124621ecab44d1cccc177269b828464525f6deef5feef4d45120fa557f0da` | 0 |
| community/ledger-api-size-config/src/main/scala/com/digitalasset/canton/ledger/api/sizeconfig/v2/interactive/GetPreferredPackagesRequestSizeConfig.scala | 1380 | `5076a5ac71acdbdf3b65efade5ca348fb700cf20f779f59eaced318c4b8b22ec` | 0 |
| community/ledger-api-size-config/src/main/scala/com/digitalasset/canton/ledger/api/sizeconfig/v2/interactive/InteractiveLapiSizeConfig.scala | 1538 | `8f3ed18c34912ac2566026ac58ea154cbc54b0139b447bb7473967dac7041de1` | 0 |
| community/ledger-api-size-config/src/main/scala/com/digitalasset/canton/ledger/api/sizeconfig/v2/interactive/MetadataSizeConfig.scala | 1293 | `4b563a6c87c01a9375ec3a768fe5b43e18dcc1adb46e9a3b9d657d6bd4bb7951` | 0 |
| community/ledger-api-size-config/src/main/scala/com/digitalasset/canton/ledger/api/sizeconfig/v2/interactive/MetadataSubmitterInfoSizeConfig.scala | 1258 | `d8a4db78b6dca646c44d809dd55e28db1faafad39490ee7faf75576c18333592` | 0 |
| community/ledger-api-size-config/src/main/scala/com/digitalasset/canton/ledger/api/sizeconfig/v2/interactive/PackageVettingRequirementSizeConfig.scala | 1301 | `d789ec203efb7b34ac17aa419eb7cbbf65e0b816b20dd854b0f75e362746d5df` | 0 |
| community/ledger-api-size-config/src/main/scala/com/digitalasset/canton/ledger/api/sizeconfig/v2/interactive/PartySignaturesSizeConfig.scala | 1204 | `c935e49de412d2a62dcd7450e25ddd83522cb18eaea1b6e8cd867bfdac8031ea` | 0 |
| community/ledger-api-size-config/src/main/scala/com/digitalasset/canton/ledger/api/sizeconfig/v2/interactive/PrepareSubmissionRequestSizeConfig.scala | 2049 | `4abfec6b983f0da8beb749d60a0d28bfe0f8e789f300a77292dda54e6189b46e` | 0 |
| community/ledger-api-size-config/src/main/scala/com/digitalasset/canton/ledger/api/sizeconfig/v2/interactive/PreparedTransactionSizeConfig.scala | 1253 | `61d242de2c7c8dd88c5080a14a6a17a3de0521abf9877c9d289ed860d5039ef7` | 0 |
| community/ledger-api-size-config/src/main/scala/com/digitalasset/canton/ledger/api/sizeconfig/v2/interactive/SinglePartySignaturesSizeConfig.scala | 1270 | `a995dce41bb17b4ba407ae4090ed4480916c8132a64c5fa45d734b5f966c8110` | 0 |
| community/ledger-test-tool/src/main/scala/com/daml/ledger/api/testtool/CliParser.scala | 11057 | `95805fbdfb2eb15468443cc82ffd600923c6cfc3e0075d9ffbe11ba1e2105932` | 0 |
| community/ledger-test-tool/src/main/scala/com/daml/ledger/api/testtool/Main.scala | 521 | `179be921a2c1380cf79e832f6b4de4b410add98931e36f596d980126fa2a2ba4` | 0 |
| community/ledger-test-tool/src/main/scala/com/daml/ledger/api/testtool/infrastructure/Allocation.scala | 3546 | `cde4e4aacf6526d56a20876181e8e5daec6d8b18a829f03e5be9c7950156c6e6` | 0 |
| community/ledger-test-tool/src/main/scala/com/daml/ledger/api/testtool/infrastructure/AssertionErrorWithPreformattedMessage.scala | 339 | `0c46de622f18691509aa8dcdc51b69fade459b7bb5a2d2b3a79ce3d0ee1a2cb4` | 0 |
| community/ledger-test-tool/src/main/scala/com/daml/ledger/api/testtool/infrastructure/Assertions.scala | 8056 | `b59487a328ff6c8b237545341470ca216f7c66c03f70bb85b86cc6225bdf79c5` | 0 |
| community/ledger-test-tool/src/main/scala/com/daml/ledger/api/testtool/infrastructure/ChannelEndpoint.scala | 769 | `0e9992d2c8af7fa2a8c3cc0d1ed54283cb66a55e874136d147df0c0533c32535` | 0 |
| community/ledger-test-tool/src/main/scala/com/daml/ledger/api/testtool/infrastructure/Errors.scala | 736 | `e0c407351dbedadb65b8b2e8bb7690789a2a926ebf11176ca936dcd8e69378a0` | 0 |
| community/ledger-test-tool/src/main/scala/com/daml/ledger/api/testtool/infrastructure/Eventually.scala | 3610 | `fcbd36269ee1a6cdb808cecd8a33dfdf739d6b406a3085ee1d04897bb5fea741` | 0 |
| community/ledger-test-tool/src/main/scala/com/daml/ledger/api/testtool/infrastructure/ExternalPartyAllocationHelper.scala | 2918 | `40fb2e164331c7e97ff6c00a9c2388b28cb0585d3f0283088eb36343b1b55977` | 0 |
| community/ledger-test-tool/src/main/scala/com/daml/ledger/api/testtool/infrastructure/FutureAssertions.scala | 5621 | `44f44027f153635d5d9afe312cb28e84d75ad278feff57b9d8bba5625e3f3e1e` | 0 |
| community/ledger-test-tool/src/main/scala/com/daml/ledger/api/testtool/infrastructure/Identification.scala | 1677 | `3b2f2e838b643d126f74e940606ca0e44780116d7f25cf777fee127107d896ff` | 0 |
| community/ledger-test-tool/src/main/scala/com/daml/ledger/api/testtool/infrastructure/LedgerServices.scala | 42298 | `ea7949cac8b8a102ef1744733454e2b7b45bf85261135206f86d98f90c912b1e` | 0 |
| community/ledger-test-tool/src/main/scala/com/daml/ledger/api/testtool/infrastructure/LedgerSession.scala | 1646 | `f50c55d7a1218a66d416226efe18039bdfda5361a2c3585c36b640217ff4e261` | 0 |
| community/ledger-test-tool/src/main/scala/com/daml/ledger/api/testtool/infrastructure/LedgerSessionConfiguration.scala | 760 | `eb993fa9750ba02abecbc4af8b6160741f380af475543f71e41dadbddcedd167` | 0 |
| community/ledger-test-tool/src/main/scala/com/daml/ledger/api/testtool/infrastructure/LedgerTestCase.scala | 5351 | `dce96e40e60a17bd35c442025509bfc7e5df099104d9375ee8b618f21198845a` | 0 |
| community/ledger-test-tool/src/main/scala/com/daml/ledger/api/testtool/infrastructure/LedgerTestCasesRunner.scala | 12666 | `5d0538958e066ca3ea20ba8d83c5ff3da03908b1c6f515704514196fc211a7bf` | 0 |
| community/ledger-test-tool/src/main/scala/com/daml/ledger/api/testtool/infrastructure/LedgerTestContext.scala | 2929 | `6978b428af2c9169be1d84141dac0ae37108c62561a2047da22d5ada74971be4` | 0 |
| community/ledger-test-tool/src/main/scala/com/daml/ledger/api/testtool/infrastructure/LedgerTestSuite.scala | 6194 | `4fdf0e51e0ea6473421851c46c4cf885325a9ff74c1b0f75ddf246a8e1fa50a8` | 0 |
| community/ledger-test-tool/src/main/scala/com/daml/ledger/api/testtool/infrastructure/LedgerTestSummary.scala | 344 | `ac19f5d27528b23bdf9f7a85a05e07e103c99b3863e36f9bd2e932a5c28d59b2` | 0 |
| community/ledger-test-tool/src/main/scala/com/daml/ledger/api/testtool/infrastructure/NamePicker.scala | 2020 | `ee5bff363fd90ba0a938c86b3c9427babcfca71c248a792cf1a663b2f931ec6a` | 0 |
| community/ledger-test-tool/src/main/scala/com/daml/ledger/api/testtool/infrastructure/Party.scala | 2397 | `15f29911eb6d18fd16402a68dfc6c0de4e95f5554e97fcf1d69a92207c11dac6` | 0 |
| community/ledger-test-tool/src/main/scala/com/daml/ledger/api/testtool/infrastructure/PartyAllocationConfiguration.scala | 904 | `ec48353721f5390a502ebf82a1893bfe9540e458829a436da43a3706913fcb18` | 0 |
| community/ledger-test-tool/src/main/scala/com/daml/ledger/api/testtool/infrastructure/ProtobufConverters.scala | 1395 | `fc7056ed6e8922fb8ff0bdb8007b1892f34b28cfd6c1aa7fac74b92658d4d3db` | 0 |
| community/ledger-test-tool/src/main/scala/com/daml/ledger/api/testtool/infrastructure/RemoveTrailingNone.scala | 2047 | `008378747f2e198f864f23d157b4cb9ecb4fe60467d8eb1c525ebc5c99bf0508` | 0 |
| community/ledger-test-tool/src/main/scala/com/daml/ledger/api/testtool/infrastructure/Reporter.scala | 5895 | `d8c529203a1a0b3f0f55a72473e3aede053cfa0a8097ced5c4078ce1579d8f3a` | 0 |
| community/ledger-test-tool/src/main/scala/com/daml/ledger/api/testtool/infrastructure/ResourceOwner.scala | 819 | `dbeb23f0b414d0e65268c807babee708b45d278c78f018d86facc83f4d038372` | 0 |
| community/ledger-test-tool/src/main/scala/com/daml/ledger/api/testtool/infrastructure/Result.scala | 917 | `a9d443be01f7fc98a31eaca9c4a3b2f40739d3846435695939745838d92b8f5a` | 0 |
| community/ledger-test-tool/src/main/scala/com/daml/ledger/api/testtool/infrastructure/RetryingGetConnectedSynchronizersForParty.scala | 1692 | `f261f665f952de13dc6665f7730ee8a6fe0cc593849935f901faaf7fb5f03ffb` | 0 |
| community/ledger-test-tool/src/main/scala/com/daml/ledger/api/testtool/infrastructure/Synchronize.scala | 2952 | `e45672dc7c392a6c44287c6e80c5026a79df4cec78c721140a6cbbc7cd3ae88d` | 0 |
| community/ledger-test-tool/src/main/scala/com/daml/ledger/api/testtool/infrastructure/TimeoutException.scala | 486 | `b1ae1ecb32cd830a0cb134807203be80ff01df50a4d0ca35db4098d3b6f4f14f` | 0 |
| community/ledger-test-tool/src/main/scala/com/daml/ledger/api/testtool/infrastructure/TimeoutTask.scala | 405 | `faf33f246ccfdeb518ee5fab4a544288469b7ca01f22ddd49c289cf40f78675a` | 0 |
| community/ledger-test-tool/src/main/scala/com/daml/ledger/api/testtool/infrastructure/TransactionHelpers.scala | 881 | `4f3710cefcf09de735c28142b46eef00c2563b607fd84cfae63a385b413b64f6` | 0 |
| community/ledger-test-tool/src/main/scala/com/daml/ledger/api/testtool/infrastructure/TransactionOps.scala | 651 | `ce4722ae06a65e9c5639c11aac43f9d96cb44ca7fa598f9cce5037b66634ef13` | 0 |
| community/ledger-test-tool/src/main/scala/com/daml/ledger/api/testtool/infrastructure/WithTimeout.scala | 830 | `a158365636ed0f20b243918650f001c0149dfe8092457dc538de1410691933fb` | 0 |
| community/ledger-test-tool/src/main/scala/com/daml/ledger/api/testtool/infrastructure/assertions/CommandDeduplicationAssertions.scala | 4173 | `34cd19e6e4b94eb6e1a8f2e42ff6cb61e8adae0c8f35b4d4c9bcbf5f0a1ae6c1` | 0 |
| community/ledger-test-tool/src/main/scala/com/daml/ledger/api/testtool/infrastructure/participant/Features.scala | 1090 | `fdfab4e022834d853308d31edb7f55bb9d7edb7aed6304c069a2b481db18d1be` | 0 |
| community/ledger-test-tool/src/main/scala/com/daml/ledger/api/testtool/infrastructure/participant/ParticipantSession.scala | 5589 | `a2f90c655f46c67562ff11e218531c23128bfb62d6c631d58fea8c6f26fb2c94` | 0 |
| community/ledger-test-tool/src/main/scala/com/daml/ledger/api/testtool/infrastructure/participant/ParticipantSessionConfiguration.scala | 522 | `927ba9a07bdea265016bb246165b8a78880265afe17cdaac85e464be6b2d92bb` | 0 |
| community/ledger-test-tool/src/main/scala/com/daml/ledger/api/testtool/infrastructure/participant/ParticipantTestContext.scala | 27754 | `cff1180a5a89ff2f7810bf7b08e35409e029e67997a5f53c3737d311a5f96bd0` | 0 |
| community/ledger-test-tool/src/main/scala/com/daml/ledger/api/testtool/infrastructure/participant/SingleParticipantTestContext.scala | 70729 | `b29ae6b7d5633d60d943a5e51408dc7e12ac16679a651705a7865ef7cbfb6fb2` | 0 |
| community/ledger-test-tool/src/main/scala/com/daml/ledger/api/testtool/infrastructure/participant/TimeoutParticipantTestContext.scala | 37102 | `5f2d9efe24b95a2ca14a9547e596223246484d79a60a9b9a313d22212437fc54` | 0 |
| community/ledger-test-tool/src/main/scala/com/daml/ledger/api/testtool/infrastructure/participant/UserManagementTestContext.scala | 6750 | `70346cd49f9588209a3b2fcbdecaafc424981330eb1add7f42944073cbe2ab98` | 0 |
| community/ledger-test-tool/src/main/scala/com/daml/ledger/api/testtool/infrastructure/time/DelayMechanism.scala | 991 | `67c227b55d1e494cebd788f58655503f877ec132a0870eea4687c05a9b5a28f3` | 0 |
| community/ledger-test-tool/src/main/scala/com/daml/ledger/api/testtool/infrastructure/time/Durations.scala | 671 | `80729aa48b6e24cb5c887301533ca3fb09fe02a7c902f171c9d7957cdec69ba0` | 0 |
| community/ledger-test-tool/src/main/scala/com/daml/ledger/api/testtool/infrastructure/ws/WsHelper.scala | 2687 | `57e50752091fbe6bbd7921b6995f855034625f3abd62105b89e16ede1cd77c74` | 0 |
| community/ledger-test-tool/src/main/scala/com/daml/ledger/api/testtool/runner/Config.scala | 2301 | `05d23b1df62c302a2e0498c29184b94ca64c6a18805d8b084d11cfb624d50c4a` | 0 |
| community/ledger-test-tool/src/main/scala/com/daml/ledger/api/testtool/runner/Defaults.scala | 616 | `0e9381d5b594d4d05abb7e88756d53aea815ab1e043629b161e7faa8ca1e5ac3` | 0 |
| community/ledger-test-tool/src/main/scala/com/daml/ledger/api/testtool/runner/TestRunner.scala | 11117 | `2e22969254d3c661b520008f3f56fdffeb2a4b03ba3c6b66e5d7852c605942ad` | 0 |
| community/ledger-test-tool/src/main/scala/com/daml/ledger/api/testtool/suites/V2_2.scala | 3392 | `ccf2f6a67a1d053ee0e605b836b2b00dd3948bdb61cb26070bc09cedcf6b4150` | 0 |
| community/ledger-test-tool/src/main/scala/com/daml/ledger/api/testtool/suites/V2_3.scala | 1356 | `b3bc32448ab72ca7b34d0351d4fc799f74d066a9fe50b7700b7e118d09ac1b20` | 0 |
| community/ledger-test-tool/src/main/scala/com/daml/ledger/api/testtool/suites/V2_4.scala | 759 | `cc9a287f9e7073f7f92e8f5615ceae4253e837fd42386519a14a51b429fb29c0` | 0 |
| community/ledger-test-tool/src/main/scala/com/daml/ledger/api/testtool/suites/v2_2/CommandSubmissionTestUtils.scala | 1179 | `f5dfd993eabea71c535787acaf5a8576d8e87a09229bb46cc1645d8f160c37a7` | 0 |
| community/ledger-test-tool/src/main/scala/com/daml/ledger/api/testtool/suites/v2_2/PartyManagementITBase.scala | 4181 | `792c54ed6538a6aad1be0f4ea6aece022aa8ccf0c8c87a409f1d54aee8113c4e` | 0 |
| community/ledger-test-tool/src/main/scala/com/daml/ledger/api/testtool/suites/v2_2/UserManagementServiceITBase.scala | 6118 | `51665c8b86ea2ee303d4386dfb66af8d527c757e42ac2dd9a7b53f99c16e8fda` | 0 |
| community/ledger-test-tool/src/main/scala/com/daml/ledger/api/testtool/suites/v2_2/objectmeta/ObjectMetaTestsBase.scala | 2685 | `59b8e60775fb2a2bccd7a64e1e6edb4b282a8932cdd6314ab32613c24752e83e` | 0 |
| community/ledger/ledger-api-core/src/main/protobuf/daml/platform/v1/acs_continuation.proto | 781 | `0dc8e09f97a98f8d1b66dcaaa7a970c0dca62413e4d64225ca74df219c01596e` | 0 |
| community/ledger/ledger-api-core/src/main/protobuf/daml/platform/v1/acs_page_token.proto | 481 | `e2bf7bc3be0bdef252aa80b2155885fed967a9ff830b45f2236f11ec92cfc820` | 0 |
| community/ledger/ledger-api-core/src/main/protobuf/daml/platform/v1/index.proto | 719 | `22a540414394954fb7bb8115263c6033d82ee6392389c71a37b4ee7a9fcf94cd` | 0 |
| community/ledger/ledger-api-core/src/main/protobuf/daml/platform/v1/page_tokens.proto | 2694 | `e6b87d93b075b93b7ed6464d95864014375747ff2ac7b79ba45612b7e03ae6a6` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/error/generator/ErrorCategoryDocItem.scala | 437 | `59b5f52f97c790a830c6b3e9df750e80fbad349f22b2d8a241577b3f79c9955e` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/error/generator/ErrorCategoryInventoryDocsGenerator.scala | 1593 | `620f8abf5582033848b2bc693aa023bf5859dbc941ce62c238b93ab873759f48` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/error/generator/ErrorCodeDocItem.scala | 1402 | `1760ae33afb2525a967c36800064128c46c26cb84f3a1b8a75eb325266a78c5c` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/error/generator/ErrorCodeDocumentationGenerator.scala | 9351 | `b5f2a550e1061592fa6d5f4b2922d5a6be8271df5ae1c2594f4a3e42530a8d27` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/error/generator/ErrorCodeInventoryDocsGenerator.scala | 6184 | `c6000b400f579c75b43c34f16fa506227be38dbbd31165d16df42e01ea54e099` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/error/generator/ErrorGroupDocItem.scala | 708 | `cc3bed4adc43da040b9080074863fe956e3d5278c0d02108d3dcddf487f2e1b6` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/error/generator/app/ErrorCategoryInventoryDocsGenApp.scala | 1002 | `3970eda1edb36c26695a740f86ef7d53d51fe5d6555c799054c9afd064574a73` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/error/generator/app/ErrorCodeInventoryDocsGenApp.scala | 829 | `36f8b56aeefd4be88df92df81efaa664f8bec646f33cab72099f223b4d63d174` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/error/generator/app/Main.scala | 2498 | `6554529bf197d6859ea6cdd7732fad3c8e09f5a60e254e66c462f2c99fba66b2` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/DeprecatedApiGate.scala | 1935 | `c6ed1e71a11736023cc90577fb1c585f9715479273e7b32fe0122109572346ec` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/ProxyCloseable.scala | 318 | `fb8b92d2377fd92e395faa7a7a5cae81ae3acafd28a7e3c6f3e15eead23e00f9` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/SubmissionIdGenerator.scala | 567 | `9023048060687a49f97c75cf51eceb4dba4df273190bd67fd273fe676e744876` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/TraceIdentifiers.scala | 2997 | `a7d43b0857f82b52aada308071be2fce5364fce6f326e8adac1ff680380b7df8` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/ValidationLogger.scala | 866 | `83bba8e0e1b1d82c2790d2578ddaa2c57a9c21dc2f69ac20d9bd7e60e44cd95b` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/auth/PartyJWTAuthService.scala | 10962 | `6fdb3b2c533f518a207d42f5a378610427f401ec03cc679865d72e064226f996` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/auth/RequiredClaims.scala | 2767 | `716ac0a7f4a5bf96f72f8e6511b9108e5797d4004738cece07f53c157f6587e6` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/auth/TrafficAccountAuthorization.scala | 1916 | `81402e52175c8bfb2dbde13ba4147a2e341cefc62bf2f4df1d0007e808ef2764` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/auth/UserBasedOngoingAuthorization.scala | 9586 | `82fcf5c21c5dcf89dc29029a6f4c52fd2673a7265a05ca1f8ec6a66abd6d4c28` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/auth/UserRightsChangeAsyncChecker.scala | 3938 | `f782f826217d33880032ffa95f9a36ef264c9f53bcbe3ba7411d1c4f9e0d8f6d` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/auth/services/CommandCompletionServiceAuthorization.scala | 3946 | `5b25710d1fb46d0b0a1c51b4f6e5c9f00e06634962a27e10b634089a02e60a7e` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/auth/services/CommandInspectionServiceAuthorization.scala | 1358 | `5e2ec22950294cc89013644cfbc00bc0341d239ad5513f0c73c5a7d6eb261960` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/auth/services/CommandServiceAuthorization.scala | 4974 | `d287155f58d4242f4c228a44b1164cfc8223c83ecf1116b96d5dc9ab3c879a2d` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/auth/services/CommandSubmissionServiceAuthorization.scala | 2617 | `4a13f71ba43557a3b030ca13ae18e6b2c7861ec2fff73b91e2be495c6b51f107` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/auth/services/ContractServiceAuthorization.scala | 1494 | `44d4b05a409cbde330e3d130bc955334da0883a56effe4faaef467a25ec1f49f` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/auth/services/EventQueryServiceAuthorization.scala | 1812 | `c18d0656509f16666269a9c772ec35652c436157aa14f690faa4354aa1c961ef` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/auth/services/IdentityProviderConfigServiceAuthorization.scala | 2230 | `acaebe3809dc69d551c934cc5ba14d655a53a70d980039686616a6f9a9b26111` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/auth/services/InteractiveSubmissionServiceAuthorization.scala | 7241 | `7443ff07b4b603959fabb0261c7874d101e1399e693feb700910bc9d6217d132` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/auth/services/JoseServiceAuthorization.scala | 1122 | `9f0c68c1fcb19fa894fcc1e6d011c8942fdfc46c857530f26ad94d9c27b2462d` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/auth/services/PackageManagementServiceAuthorization.scala | 1871 | `18374c101ab505976d08c7900761b62654e94bc4cae63cac5bed3f9e0be13c9b` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/auth/services/PackageServiceAuthorization.scala | 1697 | `d880e11a60296eaec8a724d4080cc5a01f04c3ac52e0dbc805d497f33aad3d7d` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/auth/services/ParticipantPruningServiceAuthorization.scala | 1334 | `e6e7c3fd51007bf6d1ac9ccf8de409bec3f12afc2cf78d189907a67b68eb696d` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/auth/services/PartyManagementAlphaServiceAuthorization.scala | 2756 | `e05759d5493a8c5bb76816fafda1414b4426169d2d2b4544055fbefe65c67042` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/auth/services/PartyManagementServiceAuthorization.scala | 4523 | `8a7040657a5629ffb35e9ef83f92abc569538847d4bbdcb8e54bbc105960aff7` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/auth/services/StateServiceAuthorization.scala | 3847 | `22e3dcd36633ea0cb729fbeadb90a90c2fa45cb4b128741502896da3eba24f3d` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/auth/services/TimeServiceAuthorization.scala | 1295 | `d4aa86fefebb40525c6912095c133614495ecdb7b336b26387e908f04a23422c` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/auth/services/TrafficServiceAuthorization.scala | 2171 | `b48a9e90ecf38d85671351fbe6aacb679c3744bcec711e6d6b65e9dbc270844f` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/auth/services/UpdateServiceAuthorization.scala | 2740 | `b4c2d79cad4a2a660d1e8b0a7512f007fecad49d553b247dcb3fd683516b96fb` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/auth/services/UserManagementServiceAuthorization.scala | 5586 | `782bdfd7d83072a276f5f098798af273faa6c9b2f92da25ccbb12567bf95ad32` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/grpc/DropRepeated.scala | 1365 | `12654267bf02294991960ea986aaec537e0fb9ce54a8ff336d5bc79d529769f9` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/grpc/GrpcApiService.scala | 405 | `95ab95921a19a1a276168df92be54afd00d5cfdf88d6381cbac1ba71b25d9bc4` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/grpc/GrpcHealthService.scala | 3340 | `1f17595daae4217f0cc832c3bbc6bea340603931ac829abd3224c7bdee95a8d6` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/grpc/Logging.scala | 345 | `b1f0996b01b727b51f2e0dd72ec6fea6ee97e8a5aa7f86f06df02a01eb3c9db8` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/grpc/StreamingServiceLifecycleManagement.scala | 4091 | `46f12e14499a9e9b12191da623eda0b166f5915369b555c26ff24cd924ddb97a` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/messages/command/completion/CompletionStreamRequest.scala | 421 | `4216a5d615ea88c9f10b6b7458f4d75e7ba13a518b8d899f5e01e175af280914` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/messages/command/submission/SubmitReassignmentRequest.scala | 1340 | `1bf3680268ab9ae92a76fe38fb9f16c29bd4dedcf947625e3b1e1bd6c60b6c8c` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/messages/command/submission/SubmitRequest.scala | 314 | `1a91cb48ea7d0221f004949f6a59e0f0a7ad80b90ad53558bb7b980a2e2067f4` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/messages/event/GetEventsByContractIdRequest.scala | 415 | `6c8b962eb4e620bc4eb6dcb4f7630bc7c7d7da6bbd00c6e79f8315f295b63ffd` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/messages/event/GetEventsByContractKeyRequest.scala | 509 | `9fc1d1c2a7c77319c639b912048ce5a12a38a34b0ee6ee7540268d1f173b7fa8` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/messages/state/AcsContinuationToken.scala | 5339 | `13145cdd98ec411e5edc8626ebe9e9ed9fec5e17d4c61d01c3a1db4b2edac506` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/messages/state/AcsPageToken.scala | 4232 | `c15ec9694bd11612e660f2787b00876304cde2433628a4c63f8133df615edd4f` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/messages/state/ConvertRecordTimeToOffsetRequest.scala | 428 | `b089c5d85e5ddbe622e4527817320cc5200a4fae3a61bccad79e04c3476c8561` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/messages/update/GetTransactionByIdRequest.scala | 421 | `331badbbcf67738881f14c9645cb0bf1e9906bcd86ea309dc5aa818004518a4e` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/messages/update/GetTransactionByOffsetRequest.scala | 415 | `2e7e2f04d61576831d321e5c20ff2de4e248831e4b217f5d36ca52bbf2859593` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/messages/update/GetUpdateByHashRequest.scala | 390 | `067fcf0857f469999e70c255a33adf562c83710d785462158b6118a8368a855e` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/messages/update/GetUpdateByIdRequest.scala | 401 | `63844080e1bde4bf07b7f85b0e78060367b52329447d70ec622161d479fe5d54` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/messages/update/GetUpdateByOffsetRequest.scala | 395 | `3c07e735008b096e7c7984a68eb0d718f2964536bf7d76defea258c6dea9f499` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/messages/update/GetUpdatesPageRequest.scala | 748 | `663c303e689a0f9a327ae345c5450e452b922619b7ee073594743b0cebaa678c` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/messages/update/GetUpdatesRequest.scala | 468 | `268850e860a80d9f829896931c304d9daac1d7ba134d87a11836477762320199` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/messages/update/UpdatesPageToken.scala | 5629 | `8f2c9bcfb025941f570c2fbf514240dbd91d91f7fbe37d57c375cf3a930b7beb` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/package.scala | 35464 | `71cd5c46936b05ebe87ab2d2d5e125d9c29eaa369bda9ded7ce6c287d2174558` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/refinements/ApiTypes.scala | 1274 | `3094bff139b2b8cd9c4ce3625f3a0209ad52061b6bfaa20b6be1b32eecbe1ac5` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/services/CommandInspectionService.scala | 544 | `21b1aee38dcd0063a7298986081e7f65da925e8d90262fd0d2c4b6f7350a4c18` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/services/CommandService.scala | 1056 | `8c3845357a91edb844d9f5fa2cbf4f09e6571a17fd20ca270802e02dc3eda630` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/services/CommandSubmissionService.scala | 571 | `4fb0c3381cd89ceaf2c1ad32846e13849a087a601fb83ec6c4a24d8ff632377a` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/services/InteractiveSubmissionService.scala | 3204 | `3347658e8d121c0cada293f868df7d266c62d0b46fa06a934686972031d78528` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/util/DurationConversion.scala | 537 | `d4f8b95b44e91d84bfe3e64a95ea66ea655b36f40876f5fcebf875af39e2d0f1` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/util/LfEngineToApi.scala | 6376 | `0bf4585efb28e8a181761ba390bdf6208ed75d836328e2f1292bf342a58ed3f6` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/util/PageTokenUtils.scala | 694 | `8919873189e2fe4c47ad8eafd47ef24b32ce6fe0fd1e76ac0b48a025e8816b5d` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/util/TimeProvider.scala | 926 | `c11041f4818820ef027f0fdf567d080c593c116a898d733223de7a9e97e37239` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/util/TimeProviderType.scala | 550 | `e3ab567b5626e97ccdd1bdf35a0d10fc0bb40d083307b1c5ce5e395d6708b683` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/util/TimestampConversion.scala | 2749 | `0ff19c7f389225c97293e2c6e70a24d85284f3f82aba2d6c89eb5727c972c0f1` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/util/UpdateFormatHashUtils.scala | 2204 | `90b825f9a9d32f2b2342d95e2474f1c270ac47941d8b5833741e75b1067bdc6a` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/validation/CommandInspectionServiceRequestValidator.scala | 976 | `b0fbf3b590f69fc738fb28496be645717f0bf8b85620b9f93fe3adde151bec8c` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/validation/CommandsValidator.scala | 27090 | `73fe389a7f246e7927993d4ef69ac086a46ca09c3afb559b9c062445fba3bb81` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/validation/CompletionServiceRequestValidator.scala | 3623 | `8b9c2b2a59bc4f9c1cacf38cfe5faac859de5f047a6094bd075bd6b6b0a10d5f` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/validation/ContractServiceRequestValidator.scala | 1341 | `9c0d1effa066c8f51ac48716bc41baf85c2bc4950e4f3cff2421c334d467e9fb` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/validation/CryptoValidator.scala | 3195 | `e8d3f5a2cf5cf034203745b14cad9e8a614b8cd13757cf1a475951c5619bce85` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/validation/DeduplicationPeriodValidator.scala | 747 | `ade97c03a4776489c697b777bf25c06e5df8a202539b7dbcc24d6ab5f6a87d63` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/validation/EventQueryServiceRequestValidator.scala | 2366 | `c5e6af2d263683d224a1ab1d5fe7c3975b8734b063769c73522ec20d77506f6b` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/validation/FieldValidator.scala | 17914 | `b10dc503f7f88b0d55312f6d5708a6b4906d6a1f04baede83d34c95b2f1cacbd` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/validation/FormatValidator.scala | 14211 | `7b3d36d89207637efc8b4f3cf3531e0573a36bd51b9df1fdd928a331febe26f4` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/validation/GetPreferredPackagesRequestValidator.scala | 3661 | `ce85a24395716e6e760d5de708f9c3b56977c440aa1a4e4ddde0c9920a4ffa34` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/validation/IdentityProviderConfigServiceRequestValidator.scala | 1868 | `93d88ef34c9b5f2746820aa70ce3f2de9ab2e4bcd3054043b49abcc5fdf43721` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/validation/LedgerApiSizeLimitsConfig.scala | 17350 | `ee7632d64c7e7d88851d04fdba7fdb6b8c23f217f30ecdcec7a58b64611e523f` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/validation/PackageManagementServiceRequestValidator.scala | 2990 | `4103a01139d1eabfe93f0b58fd45bc650b66244e0f7dfa1fed5db1d6b881c0bd` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/validation/PackageServiceRequestValidator.scala | 2370 | `48efa55c88127ee897f24f6caf7cc6c1675ad9d4befc40add8d85ad91e99f3dd` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/validation/ParticipantOffsetValidator.scala | 2709 | `0c78d43345de9095f148a8fb8f49431cad062f0c727793fee553bde5d14a12e3` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/validation/PartyManagementAlphaServiceRequestValidator.scala | 1269 | `aee314ee88e3f863c451d97a7c57de320c73f650ab759908806841e0ad5e05f8` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/validation/PartyManagementServiceRequestValidator.scala | 6031 | `f9ef80dee347eb57f3fe73678a38784bdf1420398c193c0c9efac4cbcbe49668` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/validation/ResourceAnnotationValidator.scala | 5009 | `c644add9724276e5c04f6daeee70b46f34e1eaea364467c4440ec2a2900eb04c` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/validation/StateServiceRequestValidator.scala | 2453 | `49a37301b5df6ad27b6f529811ae1480436097ea0b24951780196e0eaad6ef50` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/validation/SubmitAndWaitRequestValidator.scala | 2360 | `6ab9642926049ca03fecf631e2c880126065a2ac631b876ec23491e222efd9a3` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/validation/SubmitRequestValidator.scala | 12075 | `056f635a3672965e578d3a3d3ae938108d8e109524e56cc284d55a79ce37aceb` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/validation/UpdateServiceRequestValidator.scala | 8087 | `4e5ffe71a35a8af85204c279129cbb539574842d300a38d14afe54cdfae2e43c` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/validation/UserManagementServiceRequestValidator.scala | 3839 | `7dd9fe6ff03e34c107ea18fe82f61ab923c303f1348b6e7b49c31eaae820c336` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/validation/ValidateDisclosedContracts.scala | 5797 | `60e8583690ff5a4cea320d842a7f0a43ef2998f4c973215c529afbc6d20564fe` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/validation/ValidateUpgradingPackageResolutions.scala | 4286 | `d3541c4a4acbf140f3bb5260eb7c86d88ec70616837fc3b756c532577d0dac14` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/validation/ValidationErrors.scala | 2301 | `42d0221629a96eedc7942f36ee6878a2b07246515b1ed5914ad0dbde09dc5973` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/api/validation/ValueValidator.scala | 8756 | `90e7374a0e04556cfea9619e9a75b3f5c07c16407f212c92a761de02e4e3cf66` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/client/GrpcChannel.scala | 1649 | `6e21b7f1a5af3ec294b4e594dbecd07911edc08cb99f15f44d8f99b78876567a` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/client/LedgerClient.scala | 9869 | `aebd2d8c44c70488d6757c51630d7bd6574554279e8b5ff7a71041506e0d3a74` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/client/LedgerClientUtils.scala | 1653 | `adaf625534517860e22d1db7ccd3e26b1183652a1121c1dbd2b62eb5dbf967b1` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/client/LedgerSubscription.scala | 3086 | `b44ae4b39502897e7ae4bacab788fc69ac447c65afef07aeeec467b5dc6a9b96` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/client/ResilientLedgerSubscription.scala | 7384 | `27f1fc91546aad17e4dfe62ef1816011ad89881e5be54b44a17cdefe37ffaf65` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/client/configuration/CommandClientConfiguration.scala | 1193 | `beb69ef90ea2d425aa79f7820bc466800bd70998f92e677b20b6a785f87a60fe` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/client/configuration/LedgerClientChannelConfiguration.scala | 2946 | `45d8206cccc6b696c170b16a9c8f346950f648b1c14d87787def5d1998d20853` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/client/configuration/LedgerClientConfiguration.scala | 853 | `7207202f8473e9e056661bd4c789f6a714899690f231873c80f46af101f48b86` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/client/services/EventQueryServiceClient.scala | 2025 | `5a39b1dace5139d577b1145dce621b336abfb9304b8a318742fa43ba16b4d8cd` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/client/services/admin/IdentityProviderConfigClient.scala | 4357 | `694f94434182240828a9f77ddbf6053eca9fff268997d2932350a1006a2ac24e` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/client/services/admin/PackageManagementClient.scala | 2976 | `6e87f0bd6dccabd363f5a1614d7c998a273cfb8f62c2da82be120d12d8f29b4a` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/client/services/admin/ParticipantPruningManagementClient.scala | 1416 | `f03ff7587f290c3a65438000b16a09dea4447a495e9d37abd1c3211f8abd50ec` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/client/services/admin/PartyManagementClient.scala | 4170 | `f35cbf42aeecfb74614abfe3bc2409b60a93e77d225b71dfd94c5fab864b9215` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/client/services/admin/UserManagementClient.scala | 10409 | `70714d1ae9595efd22101ac5b323122765acf0d33291994d7e57df57183f4433` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/client/services/commands/CommandClient.scala | 1983 | `75532e95d78c3091e106e900bb1abc6b6dffa6c6fbb1935fbc4db37f22e5d4ef` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/client/services/commands/CommandServiceClient.scala | 5607 | `3c3797cf97b29e3ffde75a0b8d84fb44adb233351d3b10c3e12fdc2f4932ea80` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/client/services/completions/CompletionServiceClient.scala | 1378 | `f859006fca9c0ef8e349332bd03a17d438b44380fc1d4c21b2309f128555cef6` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/client/services/pkg/PackageClient.scala | 2037 | `72f7b807bb629d82bc8cec4027a125b924dd2a2b040aea7e7fbd1d054161ccfd` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/client/services/state/StateServiceClient.scala | 4086 | `3e850cfa47d16ad16d1b092a5fc6d792156a307b2154a9c12282e94717cf8bb8` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/client/services/updates/UpdateServiceClient.scala | 1952 | `6828e57c143195ceff79a7a0aab00d00db3fbcd7ca65a6252b95421e789608bc` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/client/services/version/VersionClient.scala | 1952 | `fc521687db292d33eb1ef52d6ced44d96d948fc8a07790a574aef55703e9fd88` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/error/CommonErrors.scala | 4313 | `d8ddcb93ce3b14f896c5a89ef3f8fd21bb69c707fa11ecc79b31899336231e78` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/error/IndexErrors.scala | 5076 | `ba22069856d368f1655904a55c17bb6fbb7c1cd773ecd004f9315a46591aa21b` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/error/JsonApiErrors.scala | 3969 | `1780de0417d3c14e582ced05828e3ee2980094d7bc97b8fb359643b8d52c981c` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/error/LedgerApiErrors.scala | 10940 | `b88da7f4877199139e735470719028097790d471f399456acdc4a53bcecd68f6` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/error/PackageServiceErrors.scala | 12034 | `a01672e418f88167e24e48c83f2a73af68d13870ac8f5734a1c601592b7d9ef1` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/error/ParticipantErrorGroup.scala | 1320 | `f589f1f83725947fa015a2ca79ed160c4368813026684ede5d66cf2ee2a7e4a6` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/error/groups/AdminServiceErrors.scala | 1408 | `0354612164c8cdefadb71cee5603dab74b499a0386d828fff64d5cf91d0c62df` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/error/groups/CommandExecutionErrors.scala | 46337 | `6c55ba225ba8d49d64a0e239ec29887a9b4274855d8eba641c3ce61ffb401e43` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/error/groups/ConsistencyErrors.scala | 8111 | `c76fe8fb283d063838f5533d223ad3ccf813758bba077614e8dbb18818dbef9b` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/error/groups/IdentityProviderConfigServiceErrors.scala | 5753 | `d7668c5a5a402d686e139a157eeccbcaa346905f4a2be7f502904bb8cb5f695e` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/error/groups/PartyManagementServiceErrors.scala | 6144 | `dc95dffb0552a460d63f519f5d85f6103a7e9d05453c5eb132570ac02a7db1d6` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/error/groups/RequestValidationErrors.scala | 33268 | `3fe70b6643782f15d470e739a9c5723cf6ee78a352de1e42abc3c3218cf4ed74` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/error/groups/UserManagementServiceErrors.scala | 6746 | `b6c791abba35a7f02a0ab6a6de5a60632a0b007d560831e7c64e0c70901f1dad` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/localstore/CachedIdentityProviderConfigStore.scala | 3716 | `aaa7ffafe86b9ddab66cb49a335f46cb17c0c025544a7d0e24f758b2435e1de3` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/localstore/CachedUserManagementStore.scala | 4679 | `97e3e1fe1cd7bfc9c54ceebe418dcec783b980c6d83a97988aa90970211d080b` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/localstore/InMemoryIdentityProviderConfigStore.scala | 4834 | `e5fae1f50d8ae8907f69e266eb57b13ebc9a9c3e71744147d446ed137c52fe0f` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/localstore/InMemoryPartyRecordStore.scala | 8772 | `aeb8c3399caa0bf296a014c6b8b2d4f85137ffe830c1945204061dd22acbe091` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/localstore/InMemoryUserManagementStore.scala | 10674 | `133b0c60a14f59548fba5e72995ae7833b8bcd0b231d8fcb932a52200afc4730` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/localstore/Ops.scala | 1173 | `20b262e8d0c9a1530c5680846cd89818b14c68286fdafe535108a03d7f1eaa30` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/localstore/PersistentIdentityProviderConfigStore.scala | 8981 | `96f16fda700ee501d8cf259f3555825ebe8a15be9876c7f847a937f31130eb23` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/localstore/PersistentPartyRecordStore.scala | 13790 | `c032bee00e489f650e388fb0e6fb49b41faa5ab184d601a520bf0edcb3fc902e` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/localstore/PersistentUserManagementStore.scala | 18436 | `8b6cca3eab8ba52bb2b5fd83308631a09763011e4cca8aa2420c9e85a061bd3d` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/localstore/api/PartyRecord.scala | 589 | `8d1211117aa7a03beea5d524eb2dfb2350c2cb2d54ee1d1a9accfc7932e8cbf3` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/localstore/api/PartyRecordStore.scala | 2435 | `fade35521ed3e3035cbf04cdc8d30bb46f7e3668e93dbecfa77b4ec9218ca9c2` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/localstore/utils/LocalAnnotationsUtils.scala | 450 | `6f930c08aa944eaebd2888b3d7439f1e2da251bb2073a6eadf978d533adcfc77` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/metrics/CommandMetrics.scala | 6483 | `369d979d9395ae1bf4854b5ffa1a2c8b0b1b113487d9784e364f60f4e97ccbfa` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/metrics/ContractStoreMetrics.scala | 2546 | `49cb74ffc657f98c59c616ad574d6244a3fb62981168c53d04ed88ed0d6080c5` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/metrics/DatabaseMetricsFactory.scala | 532 | `b1ac63f65823374e754ebeffb871570bd124a97b15f06a2d5f49e366b4cb717f` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/metrics/ExecutionMetrics.scala | 10126 | `268fdf170dccd6351f84a61e6fc83a8b3e546e0c5821be62ef3c5d6ff0cc3e8a` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/metrics/IdentityProviderConfigStoreMetrics.scala | 1298 | `b4ee5fa7db046628307f6135f230ef8c2ecdb3b933ef0019468b43b8918fa30e` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/metrics/IndexDBMetrics.scala | 27036 | `c47a43c4541dc43f7a83872875af59587eef9487744bb79a8215f7fcd45887c1` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/metrics/IndexMetrics.scala | 5906 | `c681f393831abbd2bc15fffeb0891f800ec71dc9805236d206510e3222690b18` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/metrics/IndexerMetrics.scala | 15316 | `8d54265b933be69be6cda0f6bc21383a07d62d10edb02e3a771e0fa5469afbfb` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/metrics/LAPIMetrics.scala | 2711 | `b635b0ba6e24f7a754ad72038e14cda341437366d352d92e9d53afc542c8ee9b` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/metrics/PartyRecordStoreMetrics.scala | 994 | `de68cc44a00ce6e4a5cd51c56fa5b06d09e7b2d084af7f55ac68cdcda790dc07` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/metrics/PruningMetrics.scala | 1965 | `47c5044efb14ad35d36453ee7d0707fdbe79ec06aac6da145768986202fdb677` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/metrics/ServicesMetrics.scala | 17357 | `4cc5e2ac78eefef6261664794be47d10790ea788acfb48cc1fc55b955a5c09aa` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/metrics/UserManagementMetrics.scala | 1211 | `3df78e7e44b1cce9fa98f577fb63c571f4933950c4851e494cd7a7aea0cc413f` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/participant/state/AcsChange.scala | 6872 | `86865f5b91abfb8ee84042c5c6c13a424bcc2eafa48ccbd921ec1099d5837634` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/participant/state/ChangeId.scala | 1022 | `cc0e6eb70edf1423d6e99ff652d168a16ce242a7e4ffd33767ee940a58308049` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/participant/state/CompletionInfo.scala | 3310 | `9ace3e0247f41e5b27e7f32ff5b432a0c6c34022edf1f286540caf1a655413c2` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/participant/state/IndexingWatermark.scala | 1958 | `174366c4c3311c87e0f05e8cc380675ff5b58f00f78de7bfffc0c27ad5eaf346` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/participant/state/InternalIndexService.scala | 14602 | `683c3981c63973c0d13ceeeb3b997c5dab8f2a5b5a6437844ba0185988798b3d` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/participant/state/InternalIndexServiceImpl.scala | 10328 | `6749a279f6428e4dd53d835659bf0d78d0400ad1a7043d448bc3495e57ac4946` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/participant/state/PackageDescription.scala | 1450 | `3c2dd15321283b586965ea84480362170288a2eb8a64e281cd023bcd7e0966db` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/participant/state/PackageSyncService.scala | 2675 | `43dadc3d5077e56ec25e66da2e1ede3aedfc0ec3cb33a4ec6881ce0302aab134` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/participant/state/ParticipantPruningSyncService.scala | 2931 | `52d049e8631e7826225c3f7305d62f23f6d66a4168e27d7f8e2cd62f1cf870cd` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/participant/state/PartySyncService.scala | 2596 | `e4c166ade4f91eaa375f19948ad2fef1b7d517ee95f3607a9819df24cddef28f` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/participant/state/PruningResult.scala | 1362 | `1886bf72e761650321ee333f5365846cac119f2600fa8bab46bed58df93a1f71` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/participant/state/Reassignment.scala | 4758 | `250f8def11f1f2cfafd491ed0e4bd15d8d8de5ac4cf49895e52bccbbce580281` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/participant/state/ReassignmentCommand.scala | 1158 | `82e4ff3628e440f5895d1e0aed06e7432314bc060da606aa5b9c2bbf730b95b1` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/participant/state/ReassignmentCommandsBatch.scala | 4622 | `f9162e151159a82cde345898a89fe163861fdb436e49f9d57524e411040c500d` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/participant/state/RoutingSynchronizerState.scala | 2788 | `1cb189d938a1f595ad8b122013f2598898e49f2cb2b08d23707b6cfcfcac4b95` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/participant/state/SubmissionResult.scala | 1773 | `873241fe966cdd7cbed73a8cb73fa1da7f45e0acee40f055f2f7e5941135b2d2` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/participant/state/SubmissionSyncService.scala | 7532 | `fe6456e9d3dc4899a9002abf3de83e0f323c4aa424ffab47d9ee464072160c61` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/participant/state/SubmitterInfo.scala | 5491 | `1f2829620c53c3fc62a14e8e09a4730976db9d872444aedc3ddba75ef1ac7491` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/participant/state/SyncService.scala | 11215 | `fdbd3245d9772d68ff6b657fada73032534449c4593c6d4ac9002533f7150676` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/participant/state/SynchronizerIndex.scala | 3816 | `8e68720444d85f284ae20b5d674e4b57bbf6e29e9497d2cdcd1d9642920ac315` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/participant/state/SynchronizerRank.scala | 1313 | `b2f95b75484b6f092854b38589ad578ab009189af227449334d91bc1e659093b` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/participant/state/TransactionMeta.scala | 2605 | `422b69e727917eef435115057781d91e8a7394c688bcd218186af651e018b7f3` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/participant/state/Update.scala | 32413 | `92a81a2eae4f216bb39336af7a40650588a2eb0ac67340fcc74959f22b5a0f6f` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/participant/state/index/ContractStore.scala | 2375 | `feec26ce2d911fe25442e4a1a3a99766cc1606507c627923067f4c21fdcdcb4d` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/participant/state/index/IndexActiveContractsService.scala | 1774 | `456ad5934d31a281fac5a6ccb2057948bf3ecef30805b7396bbae1f8af9b4be8` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/participant/state/index/IndexCompletionsService.scala | 1679 | `b268cc4439370d33f07b3b139d4ca412f64c3cb45c06bbb2d0591a2fe40401c3` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/participant/state/index/IndexEventQueryService.scala | 1200 | `c7bd86a686a44820aebfd7b9ccc1d79474606d09ea8bc89a52448248dacacb0f` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/participant/state/index/IndexParticipantPruningService.scala | 884 | `fc88fa7241db3a0862859460f16e59b961b963c44b42caf5180d8b972d300cdb` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/participant/state/index/IndexPartyManagementService.scala | 1035 | `fc955f79b4c8d3b7cbf56aff98aa8968de3c2cb9dc72c5463d88e80fafe4e018` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/participant/state/index/IndexService.scala | 592 | `0249b5c8644ea59573f76c9cf8def3047e6eb784dc4eda321f1ce68e95e69990` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/participant/state/index/IndexStateService.scala | 877 | `f1019b64afc39e025e5f15e0c2755bf5eb1beb920e642107faa919b6873a9f5c` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/participant/state/index/IndexUpdateService.scala | 4428 | `9862f4d763f407289a01dbed10bd0fd1beee431d9384e45fd6780e95131b3882` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/participant/state/index/IndexerPartyDetails.scala | 833 | `666a1f74f0f0c71077a80e858923594f9ffe77b9a5563e6b49947e8a5920b7f1` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/participant/state/index/LedgerEndService.scala | 411 | `ac7f942f32cab2cbba2b2559980491422d102bd0cabe68bab9a2c31a7bd304ba` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/participant/state/index/MaximumLedgerTimeService.scala | 2304 | `ee0e7d58773b875625d458946dc0642907214b93e30eea267c374b0a986d2467` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/participant/state/metrics/TimedSyncService.scala | 11413 | `05546141bad0a562bfabddecd930311e7d22e50019f6d1e9213fdfcf42411ce6` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/participant/state/package.scala | 1309 | `fedbdc5bf55be7068f00440e0a481055b9799eff7a25fe02f4274f55f9a37831` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/runner/common/OptConfigValue.scala | 3385 | `61922d376d5a3de3d8561d41627310ee2af60fef304e9ff639b8468f693eaf00` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/ledger/runner/common/PureConfigReaderWriter.scala | 8312 | `5de7a57edb8485e2cc9af92c56a2615e610f2c8658317991af03dff72a33b7bf` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/metrics/LedgerApiServerMetrics.scala | 3812 | `fdf39a3b92eca7c3688b852a1b6faa79a7202c256068c5966e75de511b2cf8a1` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/DispatcherState.scala | 6217 | `c96ccf932bacf782fd1b080464508f5ab9b81bcb0ada5e0dbdbae29410bf3e21` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/InMemoryState.scala | 7736 | `6dc6861a121ed70c703be111e6e6c377e00e7526b53c54fec64f443285e4ab74` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/InternalUpdateFormat.scala | 930 | `5b11bcfee47d4a539f9295f595a9aaeb91509203759e7612b9c32f386a6d1b65` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/LedgerApiServerInternals.scala | 2870 | `ffece7482eab473f428d1ea3ae2090cc6e726fda4e38c79a570c932995139a5d` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/PackagePreferenceBackend.scala | 24177 | `0523340c40c1aebcae1f4d617c7fc59fc8fb8bd2566834ddcbc37dc7a12bcf49` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/ResourceCloseable.scala | 2303 | `92c25af93e8057eae9cf84382259868dda79456de3afbc4e08127182cec0bf16` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/TemplatePartiesFilter.scala | 1240 | `dacf4e6febe98f8fd1a1aec0f36c55e1049dcc531e376d9f8bbd86f7699816b7` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/ApiException.scala | 542 | `4b9c0224528111c8e16c882e1a7ae288b85fbba9c484508ca5c548dc49d8b4b7` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/ApiService.scala | 337 | `087fe7520cc3cd08358ba60bb4af828e7bba2837ff80576bc81ff184912ca5de` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/ApiServiceOwner.scala | 14342 | `59270ab8faccf9606a280b9c9f1ef6975d730885b9d234647604d3cf6f760c1b` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/ApiServices.scala | 20487 | `21467ee0822fbb409b6fd9cf8f102673383d73ec2dcced18cf13f7645f9464ea` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/ExecutionSequencerFactoryOwner.scala | 1286 | `b59a0ce38df96d42530f6f3f5a76a32c89096724afb524e58bfb25b038b76e53` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/GrpcConnectionLogger.scala | 1089 | `01e5c0ae052b8c86da294eaa0fd5fc0dd29abbbd313aec8440de489d53abe5a7` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/GrpcInterceptors.scala | 1352 | `a394cc06c663e25648299ad67fd5d6e3dd003d01570f858bf9653eac4f70ec45` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/GrpcServer.scala | 3608 | `1ae3e62c47408c7c486017b8cea000befda847497dc5ca5bb2de97af93cfd1e9` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/GrpcServerOwner.scala | 2655 | `019493cd468e4e224fcccb1c765c032a18c5662ceedb45e52e4d9b3e54b4f0fc` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/InProcessGrpcName.scala | 346 | `5aeec9a8072060857dbc0837a51677e16ac09845d5d5e5b690b30f9b5e6d8f7c` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/LedgerApiService.scala | 2851 | `6993ff3f18f47aedb1192f001e1216299ba879c8acb4d7c551f903f6026b6e6c` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/LedgerFeatures.scala | 826 | `f50db773bfafc924c56ba9b915f20fe514cac5ba2e19333f6760ae293bc7a0b5` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/SeedService.scala | 749 | `b7c5d059f8742a9b06a3423573c9798ce1ccf52b431a431e6d2d62507a4e5d07` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/SubmissionSeed.scala | 530 | `00b07d153eb4be10e1b9ba353d0d093ce58b883229f43b82d674b891cbbb7a85` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/TimeServiceBackend.scala | 1098 | `e47c8b0d482441da96627e7b7003b2c7f062720612b1ddf45abca754d7f7c645` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/TimedIndexService.scala | 9958 | `fc466d693110064b6dc7333d5d41e997b1d0f9a29de20802bfa6dd8c07c786c9` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/TruncatedStatusInterceptor.scala | 1172 | `b5fb0e30fd039dcea70978ae1a77842b4440d4eb8727b9770f0e5c7224079108` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/client/RichTrafficServiceClient.scala | 10144 | `53ffd081c00ef19924d7e7a43850f72dcc308a8a7718512156b25072984bd281` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/configuration/RateLimitingConfig.scala | 1875 | `a2993c63cd81df9fedd8d3f75414034d8b7eade0f1453b55bf16bed195cb4c2d` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/error/ErrorInterceptor.scala | 7908 | `217d097d5d4b3b186162d9917a4db817349faec15bb582db1ece79e20ee3d93a` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/execution/CommandExecutionResult.scala | 3125 | `b97edd4637d664da65dfb84565f69c320ffbd3f1d5ba04606d462a7686cba275` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/execution/CommandExecutor.scala | 5793 | `c844bd6404a14e550642c02032a1adf092a9d21d30bcb75c1a0ac8e3d3c791b1` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/execution/CommandProgressTracker.scala | 8966 | `2ab711397cca01011a6f9a550f05c9d696546b2573d581c6ca0cf3d71aebc390` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/execution/DynamicSynchronizerParameterGetter.scala | 1238 | `1ee4d700990379decda8d4039560457d37161b15b92ccd944e3a8778bed542d9` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/execution/LedgerTimeAwareCommandExecutor.scala | 6585 | `207332b5f0dc8f5e1dd7c2d5d7f249d14af6cc98742e97410adf99987e214e48` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/execution/ResolveMaximumLedgerTime.scala | 2879 | `ffb6158007e1dc87e83f6fdc5dfcf535e9e3197104971554f9957540cfbb1443` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/execution/StoreBackedCommandInterpreter.scala | 28982 | `c6c53260225bde823388dced9d4f2a9c8e8969eb14c07f5045c46b12d7342e9b` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/execution/TapsCommandExecutionFactory.scala | 18488 | `031c2bcfddc45897e05790f79fac5cd337942c4749554f54438c9952b678f4f4` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/execution/TimedCommandExecutor.scala | 1500 | `af0971909000866c14618f4f89fa1206ceb49db9926fca16b7005c51c91492cd` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/execution/TopologyAwareCommandExecutor.scala | 18654 | `a83786eb97c327a5f5e17a27a488db7dc17fbeda65ae965688444492aa15711d` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/ratelimiting/MemoryCheck.scala | 5702 | `929dd48f4369954ccd3da2386b076e4bc49396d4465a183e661a2f2c567c7002` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/ratelimiting/RateLimitingInterceptorFactory.scala | 1596 | `423d53332c632037f93d5c47d9c07fcddf2798629fdc8fa88a4cc01cb1802d38` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/services/ApiCommandCompletionService.scala | 8964 | `005c3aeeb42498e9d33bb9cea73d1b3f2a33ecbc3a4cde3014c7b43140e15661` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/services/ApiCommandService.scala | 8646 | `79849e24c90080e29f299fa9a1c6fb10e2c4fc665fd0df76f356888a642c3971` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/services/ApiCommandSubmissionService.scala | 9224 | `513500f00636da0439ba5b23e699ee0fff43684c6fa9e46d0fb81babe4bc495c` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/services/ApiContractService.scala | 4889 | `328e928dcfd68cffea1a1592cff81af646b951bd1b285b8257f75b0188fa25a9` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/services/ApiEventQueryService.scala | 2611 | `51ec943b86bc8ed3198d1defee0bd393b5444a0c333f84e95b865b862a66cb9f` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/services/ApiInteractiveSubmissionService.scala | 10934 | `5eea248b3f6fd40d6447074b116569c52acaee2f6f53af1b862d084465d4055b` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/services/ApiJoseService.scala | 4509 | `b821acfc6f78f0c6857420a84fe2b235c2d3aea3236038ee84fa281886197f53` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/services/ApiPackageService.scala | 7043 | `3d8d070d9ca469655313385e160c72789e5ab6bffb7edf7561b09fd57526e37f` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/services/ApiStateService.scala | 16486 | `d109d65f617ce42c15469ab3e2cc8302ff649a8506e624d6b594b01da2ff6a56` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/services/ApiTimeService.scala | 3831 | `61bd6db6ee89ff24cf2cd9c46b8c0b3c0bb3bcf25d881b7dc2981a38a6306a06` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/services/ApiUpdateService.scala | 12408 | `823bf8a0caa709c09d16ca586b8c84ec8d2ca258253cfb9bf9e5b20d7d921136` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/services/ApiVersionService.scala | 3094 | `592ffe0c1b9ede732e54c8027225946cbca09c4a17648b74b3c49ee1613208cc` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/services/RejectionGenerators.scala | 14282 | `d52b8f80d4d0a6f76f4ced5873d68ad8cfae89e3f1a0bcd1c3b091e650786de9` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/services/StreamMetrics.scala | 487 | `2a0d4cc0326d909d6021f336672f7b71562abb6ae2900394ef34350c184bda10` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/services/admin/ApiCommandInspectionService.scala | 2185 | `dd191d16e6ad69e840599f58deef3cbe11867daefd42553f2de353534fcc7aac` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/services/admin/ApiIdentityProviderConfigService.scala | 9242 | `a15313a9dbc3b413613c3943f9408cf5e6647077ac22fb96525cf694611fb795` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/services/admin/ApiPackageManagementService.scala | 8442 | `49bff891b0ba70018a09bbdb58563fe6e72e28e4e202c8d3b6bbcafb0d3848ee` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/services/admin/ApiParticipantPruningService.scala | 10001 | `4282d81618a2b3b8933d14dd83e9211385c42908f5b303b42e39188de724140f` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/services/admin/ApiPartyManagementAlphaService.scala | 8447 | `26d082967218381cb67b75ccf2b698d0af4d24f362168be03580ea409ba0d17c` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/services/admin/ApiPartyManagementService.scala | 49683 | `7e71d9b96a4c644a22380eb270a4dbdb43fc8b4581c741a8da53cf0e9b45adb2` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/services/admin/ApiUserManagementService.scala | 24949 | `4f33a8298d4208f45ace394d2018df9e52199c767ba96667aa2b8aefa6f679eb` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/services/admin/AuthenticatedUserContextResolver.scala | 1874 | `f2f26aed3e1c081676935b30886f515d5d9610d8be7fdaca924b89a2a2f292ef` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/services/admin/IdentityProviderExists.scala | 827 | `b6ce4bed876cc049507072d1a8b325a026d4ca01ec4c696bbb754473b4117fca` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/services/admin/ListKnownPartiesPageToken.scala | 4446 | `aaaee50de334d10a866a69eeebf90ff4464909567772ef816ed50ae873af6248` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/services/admin/PackageUpgradeValidator.scala | 8816 | `9340829d32f7907f0af8639dc421a242bda5bd48cc80bf9f5b5e9e8efdf7dfe2` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/services/admin/PartyAllocation.scala | 1682 | `e45bfbd65d9f77ba1768399686134512e31a8bf40c1a863f1a30742cd635dbb8` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/services/admin/PartyRecordsExist.scala | 980 | `c9d85b04a0a5d1fef66d5ca80a8b0a736008cb03749c78a80a4f62a53996e2ba` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/services/admin/PartyReplicationEndpoints.scala | 2052 | `9ee1b93fee92cff47e0f36f00f541cb4dc5a5a9bfafa18b7d53fa827e1e72879` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/services/admin/PendingPartyAllocations.scala | 1223 | `18893724bf53072cffad5df46ea287a72686fe29a8f899111ac1e8e1916a09f3` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/services/admin/Utils.scala | 4710 | `45f0f635744e48675bb7c856ea0da6560bc8beece497c8330fdaae4d5b50b786` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/services/admin/package.scala | 537 | `518f47a1dba27a522c9a72db0a8f433290e47f8a4a59e45610737e7605aebffe` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/services/command/CommandInspectionServiceImpl.scala | 1881 | `d13bb8843c7c3070c94d0d98ac9db1f6406629d32a4c875f9b170044e6c8cc11` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/services/command/CommandServiceImpl.scala | 15511 | `91756587549e8f92b5fb1e19c998b3ae60525247e38445c673841c7e302befdd` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/services/command/CommandSubmissionServiceImpl.scala | 9002 | `8db68976ea46be831e3dc487e08b210bf701998f58cac9586b4bff4b85491f66` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/services/command/SubmissionAccounting.scala | 3185 | `f16055e6ca9c562d88520b40c704a823124c73ae811fd5e388e0c65a5603ae92` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/services/command/TrafficEnforcementBackend.scala | 20856 | `964b5b2a23e06645df2c837f8976b8cb28a6250be45d1accdf3b8d497724f906` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/services/command/TrafficEnforcementOutcome.scala | 1363 | `47ffbdc582bba8c5c9470353baf6045488e91de447b8dc3a0947d5dc111cbbb1` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/services/command/interactive/CostEstimationHints.scala | 1404 | `f3209367fe062911656d284de8fc6c9edfb53c32260533302d377effb8b98e4b` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/services/command/interactive/InteractiveSubmissionServiceImpl.scala | 23589 | `65ad5542b699dd80ea01cdb9ac8deaf68cb4550a719eda7a1a0127afdeec9398` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/services/command/interactive/codec/EnrichedTransactionData.scala | 9500 | `e722de1838d25a44c39a8b4f52518c6fcc6a4b90b9572138f8bbdeed5d576b52` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/services/command/interactive/codec/ExternalTransactionProcessor.scala | 17563 | `286dbce928aadcc392a64dac9a601b1a24d8e2ae494ddee35521ecf8491120d4` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/services/command/interactive/codec/PreparedTransactionCodec.scala | 3913 | `d909a6bc36cf55ff9c8583c169f09f9de467e890ff40ef51a51f6db90eb3975b` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/services/command/interactive/codec/PreparedTransactionDecoder.scala | 27908 | `c4f08de07d9eae04ae939118df22ef13637e2c6fb6e76ebc9b2b1fec972bb32b` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/services/command/interactive/codec/PreparedTransactionEncoder.scala | 19988 | `0a8e149332cccceef0f97c1a7866ef2d122e43b67c805245ea979a5fed6da2fc` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/services/logging/package.scala | 7251 | `dc7bc0ea01fed601cae142c175bf02e12c9cfea349a48046937cf11a77ca83b6` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/services/metrics/TrafficEnforcementMetrics.scala | 6294 | `ede95d2cba1d5faa5337d0ffffa21957b8b7609687b03a29c25fd4bea769e43b` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/services/package.scala | 2369 | `9f328d1e9a5baf7b644766c18b01f4145c1ce94c7a83f8fffef8d0f1926beb2d` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/services/tracking/CancellableTimeoutSupport.scala | 1988 | `e0f40b3e029efb86b42017cc966c5ebdf847d9bb37893779ba8200b9849e15a0` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/services/tracking/CompletionResponse.scala | 340 | `5d437173a985e4cf35f2aa2a7312cbfcc023e459e6c5dc32084146e817d217df` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/services/tracking/StreamTracker.scala | 7614 | `035db07fb7e8c996b6538c188638fc518daba98c54636548b85832c6a2ccaf67` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/services/tracking/SubmissionTracker.scala | 6681 | `2ef8a9521b18efeb7dbaddc22a8d47b3fe6c24e060cb76929368efbf62761075` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/services/traffic/ApiTrafficService.scala | 4361 | `93220bc15ed855efd98589f9a42cdadeec797b90e2714c5a614a0bfb3cbd6502` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/update/FieldNames.scala | 3021 | `66b8faa171c4e5bc88903d230bbd59d44edde7b235dcb2df232a30833b4a843d` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/update/IdentityProviderConfigUpdateMapper.scala | 3072 | `e22ec7beaf7a94a862f2cb3020df508a357f6b6810a57b1c2ca441abae2f9ae9` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/update/PartyRecordUpdateMapper.scala | 2054 | `3e68f9165921897512f599f6edf0d38ee84c6977125a3052264628ae95ed5789` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/update/UpdateMapperBase.scala | 2819 | `268c9988884089b0c9b217015f1623e5c0b1ec68c403ecf20b5f367d45242077` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/update/UpdatePath.scala | 825 | `efce3f2e4dbbd766098e372751fbab1417170a35fb5a49b80c3c866e17d3c26a` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/update/UpdatePathError.scala | 959 | `3e05e12b65f9f25dec9099b52b062c39787ddc2bf6d1bb225d3fe661935a45dd` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/update/UpdatePathsTrie.scala | 4451 | `9e15daf01adedafdf7f16f8d1a8d692c68582bb31208d88c27e032adce362e70` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/update/UpdateRequestsPaths.scala | 2941 | `d58c8f092d1cdf63d16e33b123a92b7342a289465ea55ab921f5cf2739808f3c` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/update/UserUpdateMapper.scala | 3063 | `fe85e2f5a9dd480971d73fb0c9b542a5364a9e4b504c3845fbb1ce8a7ce505d2` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/apiserver/update/update.scala | 263 | `afe63f8a29b185bf8d7f52888d94164849b1c3d42a79861995bbc47342ce1066` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/config/CommandServiceConfig.scala | 1731 | `19e64a78f3db0450dca0412a3fe8031a9d534b346ecaccf7952e87d3d6ad3657` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/config/IdentityProviderManagementConfig.scala | 635 | `f1c841a0f7fa3d565dd6715a0b0ea71dadd363da2a5a23e39e07adf951cabba1` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/config/IndexServiceConfig.scala | 13239 | `deaace617e30f4d7a8348bea978163a6cc5ec713e3f287126c1e12ad43f2b119` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/config/InteractiveSubmissionServiceConfig.scala | 1933 | `d83f3d1986c491eb0d29f55a981295d7d7e0165bd4add459d841234c0f665175` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/config/InvalidConfigException.scala | 358 | `c9a5d66388ab3191188442f948223e926957482020f27955a85190be13fff554` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/config/PackageServiceConfig.scala | 794 | `981f7eec308a60db746f27ce27fd979f360722d60b2fdf3be6154e5e0b27d407` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/config/PartyManagementServiceConfig.scala | 1066 | `8cafa54a2d23dacb48a280fe822ffdc3687795dcf5392262ca10d3476eb7cf1b` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/config/Readers.scala | 1077 | `61c6c26ceabe4f497b971f5f7c07547e95b0371a1af642a0d5b1af6b15e0b6e9` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/config/ServerRole.scala | 920 | `71e1313e19d8c0af2264774022839b4913f7ea1ad7e1737262487eb7d90c1adb` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/config/StateServiceConfig.scala | 901 | `926c21e254641c8f624b1deb0f4c47a5695a89963b412f3d3cddf2fef370f62b` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/config/TopologyAwarePackageSelectionConfig.scala | 771 | `e625c39ded899252d75ec85ea64515d1827cde90433b83ee50ecc1826c20f3a1` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/config/TrafficAccountingConfig.scala | 11472 | `01ac9020662c390cbb50ab0a01b32c9010347b89e6fc5e5ff2b2fa4dd424521e` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/config/UpdateServiceConfig.scala | 1887 | `4bf8a6f8f7a6526e3c956a6707e084d4d331e11669b4aa91ed35511ba83a14e2` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/config/UserManagementServiceConfig.scala | 1689 | `07564dd9ad9ae7122a4a1c88eedea50b624b38b2e6f12eae89f309be3eaef99e` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/execution/ExternalCallHandler.scala | 1356 | `73ac1f1ec9eb09c995d6e7bcd2ede40220f9e59646d34cb0b8710cff3b7e6ce2` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/execution/ExternalCallMode.scala | 487 | `800079d7aed43ee1db1567013969213ef0543805ff8eee774670948614563bbb` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/index/AcsChangesReader.scala | 12780 | `7908f0775b8d55cf12236752547b01c976ed96037d4f0f1ae013fb40485e6383` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/index/ContractStoreBasedMaximumLedgerTimeService.scala | 2149 | `5396afb2b94f24ab776154f934bcaee930399ae4023372858e3c870c50a27a51` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/index/InMemoryStateUpdater.scala | 26821 | `d3751cc58c978f3790cc6f8309ee1673c1ff68e2baf91dd4c2c19e885a289b1c` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/index/IndexServiceImpl.scala | 61790 | `6eec6b1dcd98520fae5a49eb9812df9ae9dee6da89b2653fc3163cf706fd9aa9` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/index/IndexServiceOwner.scala | 13593 | `82d82d582aee0c76a25945f33da6ed07cb0cf16c55aa0b7e8b991dc3d91a2982` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/index/ParticipantIdNotFoundException.scala | 314 | `225a8111094d3871a855512111de85f7a883d9fb93982e99d1771bc073a283f0` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/indexer/IndexerConfig.scala | 9236 | `bdc4a6659ff1e3fd370e2a929da2ad386951033905e32569c5c622ba04fa2dd4` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/indexer/IndexerState.scala | 17084 | `bae07b13ae95e4a2dd3ae07c7434e6bdaffb4ec4a4a771c08e710b20bc6ea0c6` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/indexer/JdbcIndexer.scala | 8481 | `0f2857520acd926cb7449d1cf7333e27559d82dc02af68cc8063aebc44bd0692` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/indexer/TransactionTraversalUtils.scala | 4304 | `5236c5350d5141925833ca6345b368ac25d32d5487526171a6909aef43eb8a6d` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/indexer/ha/HaCoordinator.scala | 11391 | `f76f4942222a1071d0a64c53eed7f41ce942defa5b9bbc7e393125e434cde1a1` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/indexer/ha/KillSwitchCaptor.scala | 2126 | `2d77cbb984945e92749b7ffce44c66468ac1ebf22803383e25b883150fb2d985` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/indexer/ha/PollingCheckException.scala | 311 | `7650065a08960e539d24d29772e5ab764073b600b10f44f7944780ba6332ffc8` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/indexer/ha/PollingChecker.scala | 3231 | `0357d60e010258228c0a1c3ee24c061581d50c0fc3b870bd1ff7019624c5a1ed` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/indexer/ha/PreemptableSequence.scala | 9058 | `71f358990ff60250106f6911286c642da3fc3c20dfe937ffa35a52cd8f53ec85` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/indexer/package.scala | 1293 | `4acf8ec65f50ccad3a8b28c86419116df818b4b764433c3727a5e20bae8529f4` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/indexer/parallel/AchsMaintenancePipe.scala | 18010 | `01c558121440dacf2936b97dd876020bd0e74e64564f19dc08374a78a91c3129` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/indexer/parallel/AsyncSupport.scala | 1598 | `933418c9ffa4c914081ac31b21f99d280437b3d99f18cf59555c2bdf8167b822` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/indexer/parallel/BatchingParallelIngestionPipe.scala | 2838 | `a6d3468f368c7dbba097bedb24a31ba2cbb6bf528f4330277f0392464297a797` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/indexer/parallel/EventMetricsUpdater.scala | 1503 | `f94e98cc12201a6f5b621a2fac6bdadbce957136661ffc637b4448fcb11e8774` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/indexer/parallel/InitializeParallelIngestion.scala | 16633 | `60697c8b8a7640677af80e95fb8730fff106a18329349b07f2c1d1f3898073fe` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/indexer/parallel/ParallelIndexerFactory.scala | 13055 | `d224c71512b27dfbaaaf3b3c1eb0fd0ed6f103376d0c7505f08840085bc6a5b7` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/indexer/parallel/ParallelIndexerSubscription.scala | 53588 | `ddc4a60f08bfc75594add66170ebd80d5a226f076b52e03d337ac3a2b35cfa66` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/indexer/parallel/PostPublishData.scala | 3328 | `a8410333a493736dd210580b697100e78abf298a07fb8ccd03ff66e51e857020` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/package.scala | 4298 | `7ddd8bff598e624758281cdbeebc6795770bf3e29ce99819c58c3c988b348f2e` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/packages/DeduplicatingPackageLoader.scala | 2108 | `af40723d443eed8be87fe801b0252c005a9697d74fd5bfebac0fed94f9b2eade` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/CompletionFromTransaction.scala | 6939 | `b05f561be52e7795956120ba94bd0dfab378cb2b3c8d7b61e844fdd36e432c37` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/DbSupport.scala | 3895 | `497b84caad52fee6e7cf40d8eb26731844eed5841870ccc78f5a34b7d02f8da9` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/DbType.scala | 1434 | `3833d2a35299e6669407d008cb671de2a97e064c4532b9267102040d5a931572` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/EventSequentialId.scala | 326 | `93604b7b5ec9d96c8533e507957bb842e68b062842dcfaed821515f28ec48102` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/FlywayMigrations.scala | 3370 | `15d9421de29d9b5314604ed7320541c4e3e300cbff91a7e7e15d3bb7b7682215` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/LedgerApiContractStore.scala | 4215 | `fb59318f874e5b78961c15cbbfe67965c8d5cad3f160d94b47eac655022c30f4` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/PruningOffsetService.scala | 3442 | `33ff1b60708a688a0c1a45f015ff6bd9e4a256b4a10ab83d30c328758a565840` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/ScalaPbStreamingOptimizations.scala | 1841 | `d0575879871734cd52c5a2172310753bfd1f1d630364ae81ba57b64e1a7b4c74` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/backend/Conversions.scala | 8381 | `a453ae84c0241e92df4ac5e734498e2dfe357cd2b8f15b4854f2f6c9a31eb6f9` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/backend/DbDto.scala | 28400 | `320b7613d06438395f283da763a2c7e81cd1e5f584614e2a06b7a323d70b0d97` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/backend/LedgerEnd.scala | 2427 | `84d07388e7317610ec1986ad00091c64a534e6e545ef750612474549cf0d2fc8` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/backend/PersistentEventType.scala | 2529 | `d446466fd3571a41f2c2bf6ca2f04e6bd63fa7e8ab6bbbce13a909cd20e4518a` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/backend/RowDef.scala | 2581 | `4835ba59bddc960b7e432a36ad261250dc1d55bc206e350e1a4a706659b7e7bf` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/backend/StorageBackend.scala | 37477 | `cd02ab7a520046ecf454e56e577130f3f293a53167ebee03db1697583f0f210c` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/backend/StorageBackendFactory.scala | 3823 | `1e25d0f57a79c5bd2c0d522b5f36737a5cabe317458319f4e7a9831bda0029ef` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/backend/UpdateToDbDto.scala | 29936 | `ff4c67c04783f7643adf15faaa5be059fb82cb726d0110ea23c058bb10aa80f3` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/backend/VerifiedDataSource.scala | 2847 | `3a050cb1901fc1d904aaf6715ec509f25e51ad9f2123350e6c3fa363f0097dd5` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/backend/common/CommonRowDefs.scala | 1947 | `8dab947cea101ca6e7dc0cf71a0eb1bfe3f806fc4386af57bb56f9738e65afd2` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/backend/common/CommonStorageBackendFactory.scala | 1190 | `f99d1f8316a485a4dceb694329aa26da2946a68fb072020a0b065189d73a4915` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/backend/common/CompletionStorageBackendTemplate.scala | 15375 | `852a4b1d7303f855776ef95613b3629bb11ec43e95859851b3c94d6abeb36527` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/backend/common/ComposableQuery.scala | 2995 | `227e42313cbdbb708558e802aeea8e9646127334418e9b2a8d4f19cb3a1afc1c` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/backend/common/ContractStorageBackendTemplate.scala | 5681 | `39bbbcd86c98ee33e87ab090e9ac3a659d39c90cbb9ac0612a2a6359c6af388b` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/backend/common/DataSourceStorageBackendImpl.scala | 723 | `8e1422c1ea0fc348c5d44c0225dff5c68ec64d06d5299f0ccf346c1e0e1517fd` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/backend/common/EventReaderQueries.scala | 4337 | `0f516d1b928ebd7ea88bde18b1308a446430297999e530d3c68d1cd9e0281e63` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/backend/common/EventStorageBackendTemplate.scala | 76025 | `d589b675baeb32e5a130d2b06021ea5c804a1dd2ef84812acdbb094c06d15f32` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/backend/common/Field.scala | 5014 | `58709eb17068af888ca4010cd83fd217c649357cb9b35dd9ad9e64eaf4189f0c` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/backend/common/IngestionStorageBackendTemplate.scala | 4186 | `5b71c67eabcdaa736690793121a87a9c4c2fa66860ff3ee140cd1c316dc4af93` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/backend/common/InitHookDataSourceProxy.scala | 2441 | `33007c5fda4133d54d36d78f7fb2c323c21eee1376ad676757fce89af63071a6` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/backend/common/IntegrityStorageBackendImpl.scala | 28311 | `fdd95912903a589f9e3a7e427a1c5add0b2a5e06bd7c9246bed4a82f2da7b2f7` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/backend/common/MismatchException.scala | 770 | `5c3311e8d9d4b398d73025df06ef8bb8fcb7c5272bcb579c0d85c2d9305fa6ce` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/backend/common/ParameterStorageBackendImpl.scala | 18210 | `4eee39bae7e1fc459527b8fc1b1dfddf23aabb81621288c3f152dfac489b4005` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/backend/common/PartyStorageBackendTemplate.scala | 5321 | `b2a7fb26d31a89797733bd9dbfb778f40fec63c7c2c02d29af17a847c6a716f6` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/backend/common/QueryStrategy.scala | 8985 | `363069e850ac8b5383869e4f2c8cbac980d3a93538ed3df84d032d347d201bfb` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/backend/common/Schema.scala | 22907 | `efac7e530d0dda4a33c044b868be5d62854d897fd06f70f5eabd068d8784dfb6` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/backend/common/SimpleSqlExtensions.scala | 2098 | `eb6635bb1d06106410aecd3dd7fa9abadab12328680a27568ecf5b7f0b273b74` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/backend/common/StringInterningStorageBackendImpl.scala | 1180 | `4d2978df3f1e4f84a6f315cc0c5884cf3dd1d61175551c1fb2fdd7b4fed6c06c` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/backend/common/Table.scala | 2935 | `c519d1ca89300f4644e93d1cc8a6c8165c6f8574e759dd3bbdf29da4af8f2767` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/backend/common/UpdatePointwiseQueries.scala | 2573 | `99a9a5d92208e858e9831025e316296a826151b4269d3f07211cdbf76305f4ea` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/backend/common/UpdateStreamingQueries.scala | 17098 | `81cb473bc73b625a08225e5215da736c0e77160417329eee915b7c882de9895b` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/backend/h2/H2DBLockStorageBackend.scala | 1010 | `a1893afc31ae23354358e88a876863c6f83a98b80f56e7464ddf7c663fd4ebb7` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/backend/h2/H2DataSourceStorageBackend.scala | 2548 | `c1a72bb68bc6d6938a121a491b37f314c545632896b489bdfa1ec409ba3cf451` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/backend/h2/H2EventStorageBackend.scala | 2021 | `bd9f8231945ab015e467a5314b2a772e0491cf28291d1ed57a342cc80196e6af` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/backend/h2/H2Field.scala | 954 | `42167fcf79f9d34ab99ddf5776c20e8f597edc4622657d00c27a45614689face` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/backend/h2/H2QueryStrategy.scala | 1205 | `6114b71b8752c3daf8acb83a99cd6c657d1f3966173dd3b899ea5c89301096ed` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/backend/h2/H2ResetStorageBackend.scala | 2086 | `ca52a7dda30c647d3c146caf37e50c6e0ac95f583f8c54fff3313a2308a20e54` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/backend/h2/H2Schema.scala | 1185 | `e248e7c821816d31c36d0589479899e60f296dfac10be7aa08c16ec3a795d87a` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/backend/h2/H2StorageBackendFactory.scala | 3099 | `3be5365468e1725a3022d51c715127476256fe3edd4062a76d6ae478deeab49d` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/backend/localstore/IdentityProviderStorageBackend.scala | 1704 | `8d38d1d23e92974f9fb2e41f1d9745e288dd8639e53430dd8718d279e3d7e489` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/backend/localstore/IdentityProviderStorageBackendImpl.scala | 6574 | `89dfaacd4dd9563188481ff5656e068ab57200b20a3b50e213203043080cbe3a` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/backend/localstore/ParticipantMetadataBackend.scala | 3898 | `a44e955020097ffea4ba4c611ce80d1af9631202d4a9d03fedfd54112cc7f63d` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/backend/localstore/PartyRecordStorageBackend.scala | 1657 | `5f7bb3128c74fc794b9584dc428417429e547b685e80a96c14a47b735d195378` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/backend/localstore/PartyRecordStorageBackendImpl.scala | 5868 | `9e8eab63465ce5d636357ed4e58514a5786825ad44df206a03cea8e59fc2f82e` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/backend/localstore/ResourceVersionOps.scala | 492 | `b959c9c83ce4630c39e2df50e5c1fe8e73fa673b53ae3597c7315ed2307d29b2` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/backend/localstore/UserManagementStorageBackend.scala | 2810 | `951deee12470caee29268ba904c71a1d80b2324152625502bdacd96979d9d6a2` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/backend/localstore/UserManagementStorageBackendImpl.scala | 15909 | `4f181b20c9c855fc76b415b626b78ca9ee0d391c40b5d0806d4217002689b98d` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/backend/postgresql/PGField.scala | 1780 | `ad49c4b7ec9e692d4ea364beef969561ebb69544f5160a430b6c56b304260cca` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/backend/postgresql/PGSchema.scala | 1359 | `8c05f4390621f420a63d8bf91065602be6f9d40e014a6de0fc184c223dbf81d8` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/backend/postgresql/PGTable.scala | 2169 | `661b69dca3edfab823a4654c09db0a40d69291118b857f2b18cf5663a8bccfd4` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/backend/postgresql/PostgresContractStorageBackend.scala | 6986 | `dc3dd10b4de0789bb397c76142d0b5e41d17d491592ebe3e1409b3bbc4d8675d` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/backend/postgresql/PostgresDBLockStorageBackend.scala | 1963 | `97f3d467c0d8bd4e9a304c6e93f071342865087be00cf1450efae6416b697091` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/backend/postgresql/PostgresDataSourceStorageBackend.scala | 7161 | `eb3b88dbd9b8524ef76b4c3eb7fd1aab3df4ad61560082e248e28f2416fceb93` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/backend/postgresql/PostgresEventStorageBackend.scala | 3555 | `7b33fc9c65bcae5ae7d9063b8dda810072a444ea0138dd2c8171cde055774bc5` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/backend/postgresql/PostgresQueryStrategy.scala | 5854 | `fb5d418111cb40014a5f03ec38269996a3806dfb4ac98e41cec00f47bd984806` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/backend/postgresql/PostgresResetStorageBackend.scala | 2117 | `1aa3028f0f26020a5d2a14496530db03bd914a853cc5e2a01befd2ff38dcdd25` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/backend/postgresql/PostgresStorageBackendFactory.scala | 2589 | `43aba7ed8d6e80319ffad3410369d9c13fb976d0ba6e63787ee0a7217843c85f` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/cache/AchsStateCache.scala | 1213 | `d0d730e5b9211979d445d4f8fada8fc51723973c41ef526f8a397caf03672493` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/cache/ContractKeyStateCache.scala | 1790 | `01363435fc2324acfcab45c8f2b3369413197b62a9d25c979be07ad2bfb37b40` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/cache/ContractStateCaches.scala | 9339 | `f628761e42a6623a32890c3e396192d758f49d34af60c0105554208124baf047` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/cache/ContractsStateCache.scala | 1209 | `cfffef3b25994b3e85948859fb4ecc38882968972fb38040c362864cb8be7e32` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/cache/InMemoryFanoutBuffer.scala | 16873 | `5523bf665f46d5ed0416fe4587266e059c5ef2ae223d3e0035ce9ff64520b157` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/cache/LedgerEndCache.scala | 1268 | `2adbc2e310a194e982e7c6be18bc577be9b9f508ffee161c86bd8c458e2932e8` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/cache/MutableCacheBackedContractStore.scala | 8622 | `2796ae5edd1613d8555a52733fcd9909914ce4d463c343ee4f59a716157ee66c` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/cache/OffsetCheckpointCache.scala | 1320 | `1e900757c9afce2d679f6670819a5114e4561d34a82d8d06dca6ee3d9c460de8` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/cache/OnlyForTestingTransactionInMemoryStore.scala | 1461 | `c00e938354df35d13acd0827d8edb97ee3e12c72a1e8b014b03976a3c2a0988c` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/cache/StateCache.scala | 10664 | `d60d627ba72d2de9acf2ec3929a5142c7044e7aed13753177f11ae3c1355d77b` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/cache/package.scala | 919 | `7c5a30bfcf3744b85471194b345f8701b2217695b935ba7ea753b8a6f4f2976c` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/dao/BufferedCommandCompletionsReader.scala | 10249 | `d2aef97405b79b198c831ef82059f3b862ae9ef39caf8a624352525dde1aab2e` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/dao/BufferedStreamsReader.scala | 7846 | `64df54f9bdfb144cfb53346481efa46c80bd17f1425152b8058285647f1719cb` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/dao/BufferedUpdatePointwiseReader.scala | 2595 | `7cf0c65603df9a6f17653a99a5e351a73909e6ce947cd2e9ccb64a9cad71edc0` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/dao/CommandCompletionsReader.scala | 4395 | `f22453bb0ada2dfee4df457869f3caea11579a6d0796385564e28768f6b0eaf2` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/dao/DatabaseSelfServiceError.scala | 3766 | `d04431940b6eb9d68533a36cd4d8e5ea1cc37f289d473f454fbf9733a63abe2a` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/dao/DbDispatcher.scala | 12148 | `42f3fb31b5fb598aa192c8c3b1cbf978bfa18171abd122211e063266f401c66a` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/dao/EventProjectionProperties.scala | 6356 | `739e94ce929e97964933a37f911530503a56a72ea444d3f76f551c1a5e49498c` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/dao/HikariJdbcConnectionProvider.scala | 4401 | `192fb59c55ce8f6e5b74a38bc26a1d74f805fd98eafa590c0e39052e4f132c36` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/dao/JdbcConnectionProvider.scala | 729 | `49e1327a816e85aadc98c00277ecae8f2f8848dd4786c9b0bf965bab145be85a` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/dao/JdbcLedgerDao.scala | 17641 | `60485aa93874a8f7db76f5ba6fd017b435dbd301b9d4b2cf5898d3393b424736` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/dao/LedgerDao.scala | 5970 | `f2f49557d29c5856bd48fd80bc8d063006bdd4c165637f73de9dcb23247c579d` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/dao/PaginatingAsyncStream.scala | 11503 | `cd7e0b71daa7c1518e7f55ea3b16ffbb80ee676d6a0eb725300e5f359e85799e` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/dao/PersistenceResponse.scala | 382 | `7349ba3691af6c1730bf167d16a0fa95c30c0ad215fa9f13c3000f389a16c49c` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/dao/events/ACSReader.scala | 37770 | `30949593ab94fc001cdc7449de255b866d0034a82ca8bdac1ff88399b6af6812` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/dao/events/AcsCommitmentsStreamReader.scala | 4477 | `afadbc2f1178a837a588be98ca2c5632af8cf0cedc0b7de2b7418c612ddd32ab` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/dao/events/BufferedUpdateReader.scala | 8204 | `4c41bbd0d9fe1a5bed1b9ea19c15b4f029de4adc4d6e76ef0c43ad62793d905b` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/dao/events/CompressionMetrics.scala | 885 | `2806364ae8a90620fe9a6bfa2a81a9c9962348ebdb5781c1ca914e2823fb5859` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/dao/events/CompressionStrategy.scala | 3589 | `13423af91c315e430bd537c2f2775a8e597bb175f51760f3cfbbf2bfc8df40ad` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/dao/events/ContractLoader.scala | 15475 | `21237c9c75e8472e82892d6715f03543ca35a3161e326b2e6542065a0d0014d1` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/dao/events/ContractStateEvent.scala | 925 | `632bee1d701a08a6c516eb5bfdf49901c7931b5e7ced7c266163653cc4983170` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/dao/events/ContractsReader.scala | 4679 | `6afa51ecc23f3801ffbb88f9f550d2eebfb51acbfa9149f36c856ae39f2dc352` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/dao/events/EventIdsUtils.scala | 1395 | `ea51194003bbaa5cb3dc0d465b0a96704c7a103afc095f58739fb1ee585c7e8d` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/dao/events/EventsRange.scala | 1838 | `85df66db036c67b66178e1f98ad0314d4edba53598730e6300fb89db22a8f72b` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/dao/events/EventsReader.scala | 7155 | `b02d6f626edff37d925fd12cfda71a5e857437f5c3eca4ff96f958bde7a09b76` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/dao/events/EventsTable.scala | 4035 | `01a471b03ce75fc33806f2618358e16add5030f7b67dafd236475048df7065e6` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/dao/events/FilterUtils.scala | 1079 | `e4ff335dcf97dcb948b1b859a4627a04338d82e6ac394f771271345c95eefd82` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/dao/events/IdPageSizing.scala | 4106 | `7b249b08f6e72c5bfd821bc71224f9b0a27baa34b212a43c8bda3fd05c044ac7` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/dao/events/InputContractPackages.scala | 2578 | `f43caa22efc6e5ee0bfff46c45d8546156a52234fc9175006dd3413760b11f4e` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/dao/events/LfEnricher.scala | 5391 | `cc2342cfd0ea2e38040b173a9c6eb63b82399b166eb3c5bbf7f4017fbe0b3549` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/dao/events/LfValueTranslation.scala | 19771 | `1e437668ccd5b09bf87844bb9b9ad5bc26690101d4deebbe037a68df33aebd40` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/dao/events/OrderingUtils.scala | 729 | `371dbc6cedb3c7d255ae3607ae6eaf51212e9af505dde31511bf8a6d219b6592` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/dao/events/QueryValidRange.scala | 8140 | `25d11615e89b80d7853550fe321b817f1b29bdb7598f71cb1175aa4254cefa59` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/dao/events/TopologyTransactionPointwiseReader.scala | 3640 | `aef2fdc1943ee3c12b484abf10178524bebdfbe7668b79dd14a1d6fb4f543741` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/dao/events/TopologyTransactionsStreamReader.scala | 12886 | `77e43fa6fe2b3bf3db5f82766b337cdd5164572fee034e108d1b8509b3844473` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/dao/events/TransactionLogUpdatesConversions.scala | 29644 | `bb69b1a0dc8a3f39652ae66329cd21c968fa9cf243d754bc36474fff30f5dea5` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/dao/events/TransactionOrReassignmentPointwiseReader.scala | 9276 | `372e9ee165ca970efdcda84cfe3f9386cd07870beaf114841130a753655d0e3a` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/dao/events/UpdatePointwiseReader.scala | 3483 | `115f286ee59f22f6dfe592909e1709c030857dd232954cde106bf6884719d2ab` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/dao/events/UpdateReader.scala | 24057 | `9ba8128df862d27733adacc7bdb82de557c61d24f3a3c346553f3a41fa9ae6d8` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/dao/events/UpdatesStreamReader.scala | 48130 | `0507aa7cb41fc0981e72c3d4ef57d4af576a1193919ef87482c139e2153cb8c6` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/dao/events/Utils.scala | 830 | `d8b1e0810fede60526f75aa5151b8d2b9e41bb474581fd6eb62f040b96f32f0c` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/interfaces/LedgerDaoContractsReader.scala | 3168 | `de357e032d28e0ed31bdbf1ef08882a46104d2f217ffc738c4312eaf5610bebd` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/interfaces/TransactionLogUpdate.scala | 8765 | `e847cbec59a6820ec06546ff1517275cd90c59faa8d2aa7c2f0085455e0b1b1d` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/interning/MockStringInterning.scala | 7071 | `96d4eeb6e2a507c2ee75dbd54f261afa7ee60ffb287298c0402d833a4aaa3838` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/interning/RawStringInterning.scala | 2720 | `31c9599032db857316054098dcead9e85e8762ed1bc16e08e9578af58ec6d252` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/interning/StringInterning.scala | 4195 | `d9e8d6fa2e163d6fd08489de5a63eede93acbdb5e875c8c50e95d1ed9042360f` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/interning/StringInterningView.scala | 8133 | `3734f8de7cf9ec4669663b422d5cd18deee59255e72b39de4a57723d3fd8173e` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/serialization/Compression.scala | 1754 | `b8b37fe8e528b679f83824cd180ad1dfcb85655d8d8bf1a84c0da2c75dff94fa` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/serialization/ValueSerializer.scala | 1341 | `0c8cc9cf5d67fbc924ce756804f8331d452331cb5e6eed9a349373a1582cd437` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/utils/ConcurrencyLimiter.scala | 1693 | `b6e48c63d902c1cf3ad714cd4558f8e8abed02ae1be13770739efbca54eff084` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/utils/EventOps.scala | 3204 | `636e4decf38f78d6fbb3dc7be3ee91c6023f11e61537297a68f0b28ecb1f9f8d` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/platform/store/utils/Telemetry.scala | 1145 | `a0db05468bda721ed99a2283823f70067a5947985e885a061ad75932ad240311` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/tracing/SerializableTraceContextConverter.scala | 1797 | `47a6877bcd395f735fb61376a9ed6027f83194475b37800b8c40ec3c1bfdb068` | 0 |
| community/ledger/ledger-api-core/src/main/scala/com/digitalasset/canton/version/HashingSchemeVersionConverter.scala | 459 | `a9e1fcaf490820de3ecd6762ca1b3865fd7b9d09205efca9a88f73419f95511f` | 0 |
| community/ledger/ledger-api-core/src/perf/scala/com/digitalasset/canton/platform/component/Report.scala | 3134 | `6ed669e0d179bc33abf2da9be1d456385551e325e40e55829556cf5d3af173c0` | 0 |
| community/ledger/ledger-api-tools/src/main/scala/com/digitalasset/canton/ledger/api/auth/Main.scala | 8251 | `58d85dd73a1363d7784a338b15c55c3c4b899bc9c4f461ab6a30546bef62b73a` | 0 |
| community/ledger/ledger-api-tools/src/main/scala/com/digitalasset/canton/ledger/indexerbenchmark/Config.scala | 5618 | `7dbea6bd16172110f0e2a6e24076a3c4e0e93e1f06628d85f8b3b89f170e12e9` | 0 |
| community/ledger/ledger-api-tools/src/main/scala/com/digitalasset/canton/ledger/indexerbenchmark/IndexerBenchmark.scala | 7519 | `b69498e91a323d850eb4477d7b034cc81767a10ee179a538ca0ae7f5b18203f6` | 0 |
| community/ledger/ledger-api-tools/src/main/scala/com/digitalasset/canton/ledger/indexerbenchmark/IndexerBenchmarkResult.scala | 5144 | `e661aaa3a608b700673ed78abd9cd9ebbe67cfb5ab707f5c15922ccfbb8dedb7` | 0 |
| community/ledger/ledger-common-dars/src/main/scala/com/daml/ledger/api/testtool/CompanionImplicits.scala | 5948 | `c861e1d980a2e9165ae3240885170d8920236fc7e158abd2c2fb24b6aec5c650` | 0 |
| community/ledger/ledger-common-dars/src/main/scala/com/daml/ledger/api/testtool/ContractKeysCompanionImplicits.scala | 3399 | `e4ca49d7b21162f182a168b1bc08b2fd0d67851a2bbbb3f6bcd176aa17fc580c` | 0 |
| community/ledger/ledger-common-dars/src/main/scala/com/daml/ledger/api/testtool/TestDars.scala | 3754 | `6b7f9f8761f1b7b54aca5bfe3449f577524b746f9b09c73be94fa32de2119fb7` | 0 |
| community/ledger/ledger-json-api/src/main/scala/com/digitalasset/canton/http/EndpointsCompanion.scala | 4724 | `a0dde66a2fda9598583d0599978bcf9b1f788209b0129de138f356989d5684e1` | 0 |
| community/ledger/ledger-json-api/src/main/scala/com/digitalasset/canton/http/HealthService.scala | 1878 | `596eb8b3b5f1a762846e5f2ec108bf46bc71eaebe08721b809ae9decb8223e6c` | 0 |
| community/ledger/ledger-json-api/src/main/scala/com/digitalasset/canton/http/HttpApiServer.scala | 2749 | `080d5f04bdb970c026ec05974ecfa38614df4a7ff8e63b5491d81a01976a9d4a` | 0 |
| community/ledger/ledger-json-api/src/main/scala/com/digitalasset/canton/http/HttpService.scala | 13530 | `f9876b0a92081b2b2ced9b1522a408f18247d4400019fe07a74053bf3550d6b4` | 0 |
| community/ledger/ledger-json-api/src/main/scala/com/digitalasset/canton/http/JsonApiConfig.scala | 5387 | `ef16ea971921ee88c9d469fec06e867a656cb8f306e3ea683e1909958fda9935` | 0 |
| community/ledger/ledger-json-api/src/main/scala/com/digitalasset/canton/http/RequestTimeoutDirective.scala | 4850 | `ddcd88732ae953f93934686181ea3118d0ea7c171300c6e2aef83b8b71777e98` | 0 |
| community/ledger/ledger-json-api/src/main/scala/com/digitalasset/canton/http/json/Circe.scala | 1193 | `58fd22a0282217ffff56db0aa85ac67c25e90649fb1ef1e889913f341f90ab18` | 0 |
| community/ledger/ledger-json-api/src/main/scala/com/digitalasset/canton/http/json/JsHealthService.scala | 2604 | `a52b983b33f39746c802ece8f71f0a2b3887adcecea21f9514ed65188bfb4955` | 0 |
| community/ledger/ledger-json-api/src/main/scala/com/digitalasset/canton/http/json/JsonProtocol.scala | 4464 | `7f4abb22fb2a61ca606cf8577db8dff1a4be7668abdc66968068e81632f09da8` | 0 |
| community/ledger/ledger-json-api/src/main/scala/com/digitalasset/canton/http/json/v2/ApiDocsGenerator.scala | 13006 | `36f3bdcbcaa4ffb5aeb6152ea6eac899e1e1ae4faa2a5028cab5cef96b181e6a` | 0 |
| community/ledger/ledger-json-api/src/main/scala/com/digitalasset/canton/http/json/v2/CirceRelaxedCodec.scala | 4407 | `869a8c1d1a2992fe20b1342936c47e45f85d17c21d7bf9317c1f972a0b113137` | 0 |
| community/ledger/ledger-json-api/src/main/scala/com/digitalasset/canton/http/json/v2/CirceToUJson.scala | 1898 | `b72688bf0f65d646d22d2e7b4a3b84efba1678f85e0192b0ce0bd51aac189a7c` | 0 |
| community/ledger/ledger-json-api/src/main/scala/com/digitalasset/canton/http/json/v2/Endpoints.scala | 29593 | `96f1e4bc11c0421a826c566ad3eea926564048fd5ff3832eac122c3b91c222a6` | 0 |
| community/ledger/ledger-json-api/src/main/scala/com/digitalasset/canton/http/json/v2/JsApiDocsService.scala | 2500 | `6f502ea2c0c345e31bae0fa770c63c6df68c360a169a8c4018ef0ad86f8b9bfc` | 0 |
| community/ledger/ledger-json-api/src/main/scala/com/digitalasset/canton/http/json/v2/JsCommandService.scala | 22594 | `92f9338aefd06d45c36ce0786d083125109efcee77362e1cf22cfd57108f439d` | 0 |
| community/ledger/ledger-json-api/src/main/scala/com/digitalasset/canton/http/json/v2/JsContractService.scala | 3467 | `724d7a576b849ef1b1a5383c787ebd2055b0a7cbe5899b6260d95647e209bf0f` | 0 |
| community/ledger/ledger-json-api/src/main/scala/com/digitalasset/canton/http/json/v2/JsDamlDefinitionsService.scala | 3272 | `cf45223aaf6a7707a8a50835c071f655d6ddf3fa1ed983d53b5420b990fbcede` | 0 |
| community/ledger/ledger-json-api/src/main/scala/com/digitalasset/canton/http/json/v2/JsEventService.scala | 4111 | `6ee5de29d033bc388c5f95208bb35aee1b8e18167d060d1e9032b82bd579e350` | 0 |
| community/ledger/ledger-json-api/src/main/scala/com/digitalasset/canton/http/json/v2/JsIdentityProviderService.scala | 9020 | `c46fb1e6b3f96297a74d9933c1bb5f03d84acef29c3bf26934a33eb3b41bc28c` | 0 |
| community/ledger/ledger-json-api/src/main/scala/com/digitalasset/canton/http/json/v2/JsInteractiveSubmissionService.scala | 17275 | `45d0e154652f2c705b5a2e6bf12b3868c59fb5bfbd44b33b9711190443691aa1` | 0 |
| community/ledger/ledger-json-api/src/main/scala/com/digitalasset/canton/http/json/v2/JsJoseService.scala | 5026 | `a55103fd21c6b04ff867fa639a9f9800f7792ec6aab2d3d2d32723551008d402` | 0 |
| community/ledger/ledger-json-api/src/main/scala/com/digitalasset/canton/http/json/v2/JsPackageService.scala | 15005 | `d3d20a0c3df25a9612f376116cd8f7a31bada51ab7212681f2f86ec5647bec86` | 0 |
| community/ledger/ledger-json-api/src/main/scala/com/digitalasset/canton/http/json/v2/JsPartyManagementService.scala | 11475 | `9e95e688d2ea191a9c910e6ee39882fc021526df920bdc7204a3253487009116` | 0 |
| community/ledger/ledger-json-api/src/main/scala/com/digitalasset/canton/http/json/v2/JsSchema.scala | 25474 | `75488bd08bcb289e5a731f9b269f949b7863d8200773559e137640bc3e1e25c3` | 0 |
| community/ledger/ledger-json-api/src/main/scala/com/digitalasset/canton/http/json/v2/JsStateService.scala | 14059 | `dc47ef0f9849eacc67c8e04ac7186c659802cb44a243f2922c647c417c77a27c` | 0 |
| community/ledger/ledger-json-api/src/main/scala/com/digitalasset/canton/http/json/v2/JsTrafficService.scala | 8272 | `962fa11235bc1a792a9a8431e060556a1516cc7f6b1be5b62874560934af5f77` | 0 |
| community/ledger/ledger-json-api/src/main/scala/com/digitalasset/canton/http/json/v2/JsUpdateService.scala | 12099 | `947e3be69d05d206f8a0dd6ca076c306a302a1835a53b249ed3d17e53e7ec108` | 0 |
| community/ledger/ledger-json-api/src/main/scala/com/digitalasset/canton/http/json/v2/JsUserManagementService.scala | 17660 | `f8d335816239b33c15bd681788ebbfb33c216e0bfb52efbbe9e2e4fe8000f35f` | 0 |
| community/ledger/ledger-json-api/src/main/scala/com/digitalasset/canton/http/json/v2/JsVersionService.scala | 3336 | `f1901ce8b916f9d543cc668af5b7c84b99aaf698dbac25e669be9265a8a2a020` | 0 |
| community/ledger/ledger-json-api/src/main/scala/com/digitalasset/canton/http/json/v2/ProtoInfo.scala | 6909 | `4d8b9c3fd4d7be5f9f00ca30adb5a9a74442453dbba03a4f7b79dc17954c819e` | 0 |
| community/ledger/ledger-json-api/src/main/scala/com/digitalasset/canton/http/json/v2/ProtocolConverters.scala | 53456 | `eadbb5c37c7494625821d738a9bdb5567f082582c26321bd60816f0efde9886a` | 0 |
| community/ledger/ledger-json-api/src/main/scala/com/digitalasset/canton/http/json/v2/SchemaProcessors.scala | 1934 | `fe0db7917c834c60bfe9a77943f285a382fc2b955098ddcf64e2b1fff276422a` | 0 |
| community/ledger/ledger-json-api/src/main/scala/com/digitalasset/canton/http/json/v2/SchemaProcessorsImpl.scala | 12907 | `eab6bb3836ec63a29c390f12b903a46c1a0dce7741ce4b6fe2a9f30b3eeab4e2` | 0 |
| community/ledger/ledger-json-api/src/main/scala/com/digitalasset/canton/http/json/v2/TranscodePackageIdResolver.scala | 16247 | `6ad818e41508ec762d47f2a7a91d15ab4b6a6f87298dac68d1ec8a353b246ca9` | 0 |
| community/ledger/ledger-json-api/src/main/scala/com/digitalasset/canton/http/json/v2/V2Routes.scala | 14938 | `cf3280269a824ccc6d4bbeedd552c591774d631f097fe43bc0dc213dec03498d` | 0 |
| community/ledger/ledger-json-api/src/main/scala/com/digitalasset/canton/http/json/v2/damldefinitionsservice/DamlDefinitionsBuilders.scala | 13490 | `972b91a9660a68ebca47395b482b60b39ac0dbcb1c8ec827d795e868ab6d509a` | 0 |
| community/ledger/ledger-json-api/src/main/scala/com/digitalasset/canton/http/json/v2/damldefinitionsservice/DamlDefinitionsView.scala | 1709 | `edea1a523cc59cb7c4d6839cb399cbe1e6b231ad61e4afd351940c61de701482` | 0 |
| community/ledger/ledger-json-api/src/main/scala/com/digitalasset/canton/http/json/v2/damldefinitionsservice/Schema.scala | 8415 | `318d6703dca4153d9fd3f8517ffa98db837e4ad3d2fbb4e0c162439f4864b78a` | 0 |
| community/ledger/ledger-json-api/src/main/scala/com/digitalasset/canton/http/json/v2/js/package.scala | 380 | `376b826a0e3c4a8c74ee8a1d1b763101715427b07ede52a57e66abd0676101f8` | 0 |
| community/ledger/ledger-json-api/src/main/scala/com/digitalasset/canton/http/metrics/DamlHttpMetrics.scala | 2064 | `2965e9adae832664a1e43263fd37c0afbfc8d9bcef65b862809a4b8777ea1b43` | 0 |
| community/ledger/ledger-json-api/src/main/scala/com/digitalasset/canton/http/metrics/DamlWebSocketMetrics.scala | 2094 | `3b4ade7cf27e3223e324f5710d8b437d5f37b790704ee3b8b7e7b5fdfb9ee761` | 0 |
| community/ledger/ledger-json-api/src/main/scala/com/digitalasset/canton/http/metrics/HttpApiMetrics.scala | 1154 | `af905f42ec3a2cab7a851443d45e03d401761e612b1de2824e96b0b4bd65775f` | 0 |
| community/ledger/ledger-json-api/src/main/scala/com/digitalasset/canton/http/metrics/HttpMetrics.scala | 400 | `ddc7b1a683ddd88027983cb909df96415446e5e48b528ebbb276c6e209acaf9d` | 0 |
| community/ledger/ledger-json-api/src/main/scala/com/digitalasset/canton/http/metrics/HttpMetricsInterceptor.scala | 4903 | `52201ed320d5924b18f0ecd9e2befcbf5a7328ac440b48aab972b969bc54ba3b` | 0 |
| community/ledger/ledger-json-api/src/main/scala/com/digitalasset/canton/http/metrics/Labels.scala | 386 | `97a00246b7a9899a57a5a458af43091b3cb0fc1b45265f61cdc61d559deed267` | 0 |
| community/ledger/ledger-json-api/src/main/scala/com/digitalasset/canton/http/metrics/MetricLabelsExtractor.scala | 866 | `ad7642056717064b30d56a53dc10edf9352624dfad52bb13795ac473aec6df1c` | 0 |
| community/ledger/ledger-json-api/src/main/scala/com/digitalasset/canton/http/metrics/WebSocketMetrics.scala | 413 | `4991accec343d50b011abc5104176bf58adff9eca6fee90cc91b68f00c607e55` | 0 |
| community/ledger/ledger-json-api/src/main/scala/com/digitalasset/canton/http/metrics/WebSocketMetricsInterceptor.scala | 2520 | `cf20ba483651507d8662c45a737c8dd1a16c4c6ba4ca23c15c95ef8c2f8899b8` | 0 |
| community/ledger/ledger-json-api/src/main/scala/com/digitalasset/canton/http/package.scala | 2358 | `3c6b750a531727fa05abbb0f4b6c30327a7bf01796156cef1b3fc9688a34d3c3` | 0 |
| community/ledger/ledger-json-api/src/main/scala/com/digitalasset/canton/http/util/ClientUtil.scala | 279 | `d155bc68ae534a68e317b7ff9851e8e3409d6cea016be226fa82dc57611a8b79` | 0 |
| community/ledger/ledger-json-api/src/main/scala/com/digitalasset/canton/http/util/ErrorOps.scala | 1023 | `4f1214f3bfa0b7213b68a1e8260177c3370ff5251e5c80c9f85e11542017f891` | 0 |
| community/ledger/ledger-json-api/src/main/scala/com/digitalasset/canton/http/util/FutureUtil.scala | 708 | `aac4d4bd1162ac5bc7ea96f77916d435433762306fde71c9c0faa01f16061602` | 0 |
| community/ledger/ledger-json-api/src/main/scala/com/digitalasset/canton/http/util/GrpcHttpErrorCodes.scala | 1876 | `56260f1df106869e6196b5a4a3efa538fcae80064c9d9f0ef861b9f3616367d4` | 0 |
| community/ledger/ledger-json-api/src/main/scala/com/digitalasset/canton/http/util/Logging.scala | 1749 | `80c884763aa67dbb729efcda322c2ea4dcd74605e7ee34ba2f956c291827a48d` | 0 |
| community/ledger/ledger-json-api/src/main/scala/com/digitalasset/canton/ledger/service/Grpc.scala | 803 | `dccb1e9a506f69638a39ec43a4f31c685ac88fcc7e8286eaa5df6e429475c82e` | 0 |
| community/ledger/ledger-json-api/src/main/scala/com/digitalasset/canton/proto/ProtoDescriptionExtractor.scala | 2618 | `254d8f87d532e6469651b5ad9f002aab4d94107e691cf88820318695bd5169ed` | 0 |
| community/ledger/ledger-json-api/src/main/scala/com/digitalasset/canton/proto/ProtoParser.scala | 3423 | `454fc6260bc5d1f28c39ead2244716f799e40777fdf4516f67376592ad7fd2dd` | 0 |
| community/ledger/ledger-json-api/src/main/scala/com/digitalasset/canton/pureconfigutils/SharedConfigReaders.scala | 475 | `929efbaf78d58a4bf25ecbb11ca308a775adb7eb4cf82afa560682f0b859e989` | 0 |
| community/lib/Blake2b/src/main/java/org/bouncycastle/crypto/digests/canton/Blake2bDigest.java | 16131 | `e8f2b8110a7b6cedd118db899596103acfc4382193423e0fbceea08b04a9968e` | 0 |
| community/lib/magnolify/src/main/scala/magnolify/scalacheck/shrink/DerivedShrink.scala | 2356 | `a6d1a4a6b221a36cc827c2004b5c7580888d8422a7c60ef9bdaafc938f407862` | 0 |
| community/lib/magnolify/src/main/scala/magnolify/scalacheck/shrink/package.scala | 3203 | `499187f1519043e8d45934103f6accd87df3b0956e251f3ae2f65635e27c2e3a` | 0 |
| community/lib/scalatest/src/main/scala/org/scalatest/AssertionsUtil.scala | 578 | `c31af64e514fb8b883a66ded9e0b3a0bac31e02c3290efaa365eee815c481d72` | 0 |
| community/lib/scalatest/src/main/scala/org/scalatest/AssertionsUtilMacros.scala | 2425 | `1349f0d4af3593c9d35e366e6424db5fe564a5547b84e1b7db36ecc0080b8d6d` | 0 |
| community/lib/slick/src/main/scala/slick/jdbc/canton/StaticQuery.scala | 3981 | `5f97267ed7043948ecabc4297c3a3bba2a22cfe4ae2a3c04a3cf89131002d3c1` | 0 |
| community/lib/wartremover-annotations/src/main/scala/com/digitalasset/canton/AllowTraverseSingleContainer.scala | 280 | `2d9f9daaa54f57828c1bfb8883a20b115dbceffb4240ade2ac2f5c144d7ac31b` | 0 |
| community/lib/wartremover-annotations/src/main/scala/com/digitalasset/canton/DoNotDiscardLikeFuture.scala | 402 | `efc62a00e0572636c638a474a84413e3371755a4927a86f26779945ccb556d59` | 0 |
| community/lib/wartremover-annotations/src/main/scala/com/digitalasset/canton/DoNotReturnFromSynchronizedLikeFuture.scala | 438 | `30769e1a37b760801c96824f7721df5733ada5919375c99c23a49b065336ae2f` | 0 |
| community/lib/wartremover-annotations/src/main/scala/com/digitalasset/canton/DoNotTraverseLikeFuture.scala | 439 | `b84f4981ad4e7dab3b5676cd73a4c3bbd12decc01f708f9918544e842f007054` | 0 |
| community/lib/wartremover-annotations/src/main/scala/com/digitalasset/canton/FutureTransformer.scala | 625 | `59a0e84f56c19fce4c745f0e3969550e0e9a3471cc7ef0fcf2682424fe3ed90b` | 0 |
| community/lib/wartremover-annotations/src/main/scala/com/digitalasset/canton/GrpcServiceInvocationMethod.scala | 454 | `e0f3d58f67f2aad85503378eeefd44d5e99a21d28ef53d1a9ec0e6448ab3d657` | 0 |
| community/lib/wartremover-annotations/src/main/scala/com/digitalasset/canton/SynchronizedLikeMethod.scala | 536 | `00129d01561f27b44071df94167afccdf7d8804c7eed46d112b070497cabbaad` | 0 |
| community/lib/wartremover/src/main/scala-2/com/digitalasset/canton/ConcurrentMapSize.scala | 1869 | `8bb8bf0894a916a2c5243035b76cdfcc1c9ff81a3d4414b03fda388e5a4a7649` | 0 |
| community/lib/wartremover/src/main/scala-2/com/digitalasset/canton/DirectGrpcServiceInvocation.scala | 5495 | `81c4afaa63de6f257986f9178ac15da032fbc69e97094e821a0bf75a827f2598` | 0 |
| community/lib/wartremover/src/main/scala-2/com/digitalasset/canton/DiscardedFuture.scala | 11258 | `0a8d9558f016610194cc74576bc1a7df186b21d3166d0e65143c8425faeb8328` | 0 |
| community/lib/wartremover/src/main/scala-2/com/digitalasset/canton/EnforceVisibleForTesting.scala | 5041 | `17e874c02ba3d8197401d569ae045ed98fd66c5fd02d9d9edfb594bdbddf66c3` | 0 |
| community/lib/wartremover/src/main/scala-2/com/digitalasset/canton/FutureAndThen.scala | 1351 | `a011099e913e72560edf0460f590a8b71d628ebe4f4c0ce6e7257ad16716c1a2` | 0 |
| community/lib/wartremover/src/main/scala-2/com/digitalasset/canton/FutureLikeTester.scala | 2481 | `20db6f1c98e30ce05aa4c4ec070821f2929fbcf549d595d8e27dd991334ea0a2` | 0 |
| community/lib/wartremover/src/main/scala-2/com/digitalasset/canton/FutureTraverse.scala | 8003 | `29d5933a5f4eafa33f9d5e166fa88f9415a4fcea225866f959966e228b2d2878` | 0 |
| community/lib/wartremover/src/main/scala-2/com/digitalasset/canton/GetEndpointWithBody.scala | 3912 | `19c20d8bbcf9fdc312b7ad94543344d9ea6af264d83a2346ba0a5232add773f7` | 0 |
| community/lib/wartremover/src/main/scala-2/com/digitalasset/canton/GlobalExecutionContext.scala | 3038 | `ab0375105c533ba5995ee1c013811028278174002a7e5b792b246512f61b9c61` | 0 |
| community/lib/wartremover/src/main/scala-2/com/digitalasset/canton/NonUnitForEach.scala | 6586 | `25fb32dc2aa2b49da16e05c8cf23df3e01676914579028f26ef203534d30527b` | 0 |
| community/lib/wartremover/src/main/scala-2/com/digitalasset/canton/ProtobufToByteString.scala | 1606 | `4943bff5b8214d98e0646b0a77a431a50487cbf56066bd67f1e2f241427ac21c` | 0 |
| community/lib/wartremover/src/main/scala-2/com/digitalasset/canton/RequireBlocking.scala | 1796 | `0ad27e7dbd4cb8444bdd9e81e8978e232c1bd281c39bf244a7800bfcec4ae7eb` | 0 |
| community/lib/wartremover/src/main/scala-2/com/digitalasset/canton/ScalaVersion.scala | 201 | `3d6ba8aa739e04fcf252c50d5f9e423f6422fd9c6eb377c3dc45ce796d91038e` | 0 |
| community/lib/wartremover/src/main/scala-2/com/digitalasset/canton/SynchronizedFuture.scala | 4111 | `30ca4fda7507d5e1182add7542a4e427d90994dfefa3c8cb3e576c7b80f7838b` | 0 |
| community/lib/wartremover/src/main/scala-2/com/digitalasset/canton/TryFailed.scala | 1528 | `879c9f014b06c10acdac4b77dcde2f94d6fb72f28e1e997fc1aafa734719dc06` | 0 |
| community/lib/wartremover/src/main/scala-3/com/digitalasset/canton/ConcurrentMapSize.scala | 962 | `1b1fdea9f374bbfd954c0ce4a516356638f0aac250a28564f465aa64bcce81ea` | 0 |
| community/lib/wartremover/src/main/scala-3/com/digitalasset/canton/DirectGrpcServiceInvocation.scala | 4512 | `477dc03cab65d5057a877b1d901d8bc11cc83a94e3afd47bc78bb47c8ed80714` | 0 |
| community/lib/wartremover/src/main/scala-3/com/digitalasset/canton/DiscardedFuture.scala | 10409 | `cc35e3d6b6ed88fc9da4984f6d2da10c4ecd07965cceffee88445b39ed68306a` | 0 |
| community/lib/wartremover/src/main/scala-3/com/digitalasset/canton/EnforceVisibleForTesting.scala | 3633 | `ad89b6d372cecab0f988cbc112c6e899d27d3efb423b40235878f0ed4683d644` | 0 |
| community/lib/wartremover/src/main/scala-3/com/digitalasset/canton/FutureAndThen.scala | 1197 | `d8a522c7649e82af27f8d8ccd551494475c0864066769866fae5f5cf89761276` | 0 |
| community/lib/wartremover/src/main/scala-3/com/digitalasset/canton/FutureLikeTester.scala | 2483 | `279d9877a1aa6d8257b033e8d6d57aa7f070d96bd4b56a3c13232fd98e0df1e9` | 0 |
| community/lib/wartremover/src/main/scala-3/com/digitalasset/canton/FutureTraverse.scala | 5703 | `e975bfef19b76a6372d1f93c2170bbd02cbe62369d0f273aaf688eaae24c4775` | 0 |
| community/lib/wartremover/src/main/scala-3/com/digitalasset/canton/GetEndpointWithBody.scala | 4496 | `0ced862d8131b3e20fc56f20577c1f134bda6cf2daa332dac7e99aa00108fcd2` | 0 |
| community/lib/wartremover/src/main/scala-3/com/digitalasset/canton/GlobalExecutionContext.scala | 2561 | `45b4b1a62af15e8e1e745ef9192ff93b01476c7dff7dde8f61125451a927b532` | 0 |
| community/lib/wartremover/src/main/scala-3/com/digitalasset/canton/NonUnitForEach.scala | 5994 | `fd75e899d47e6d5f83a696d89f95c09649c441f36ca7d769fea364efe7fc2d3f` | 0 |
| community/lib/wartremover/src/main/scala-3/com/digitalasset/canton/ProtobufToByteString.scala | 1103 | `9a010eb3e983132df3f4e7eb8eabe32d4c175b37f4b276d314237396d965ac33` | 0 |
| community/lib/wartremover/src/main/scala-3/com/digitalasset/canton/RequireBlocking.scala | 1673 | `726ea28e9021a9f107edd539f75578c69581bada9a24642814386eab1028c389` | 0 |
| community/lib/wartremover/src/main/scala-3/com/digitalasset/canton/ScalaVersion.scala | 200 | `e399b492146e7b5cc8791d58086b2bb106d44e9d475c9e8f0ec7faaa23416c91` | 0 |
| community/lib/wartremover/src/main/scala-3/com/digitalasset/canton/SynchronizedFuture.scala | 3861 | `16b361ecd6b85d95345c6b79c7b89bd57bff21440489e80b4f1b9c1b0a4626dc` | 0 |
| community/lib/wartremover/src/main/scala-3/com/digitalasset/canton/TryFailed.scala | 1313 | `c2ae5d8791f0ed80d3f44aa981078ea84e846169647cb92a5619a5278efdce63` | 0 |
| community/microbench/src/main/scala/com/digitalasset/canton/AcsCommitmentBenchmark.scala | 30047 | `7cfb6c9443dd5f2fdb0ba8dec5539822858dd521b1e5167998cdfd8d32dac6a2` | 0 |
| community/microbench/src/main/scala/com/digitalasset/canton/AcsCommitmentBenchmarkCaching.scala | 2284 | `3910bac17a468e2e72c2e7c8b943d53084ba1d3e4f94b6116094bdb8d5209647` | 0 |
| community/microbench/src/main/scala/com/digitalasset/canton/AcsCommitmentBenchmarkCatchupConfig.scala | 1976 | `18175cb68f1d735581ac90958f82e10dc537219b57678dab47c74016c5009e48` | 0 |
| community/microbench/src/main/scala/com/digitalasset/canton/AcsCommitmentBenchmarkContractTypes.scala | 1808 | `6b4914c97aa1ad517374e04aa415bbfef41e56a2ff7fe5fab2eab829ff25d726` | 0 |
| community/microbench/src/main/scala/com/digitalasset/canton/AcsCommitmentBenchmarkLoad.scala | 2022 | `9bba9d7f6229d948ccf97f0000a0d616051bda1b3182f8ec4ef53ac9752ec0f8` | 0 |
| community/microbench/src/main/scala/com/digitalasset/canton/AsymmetricEncryptionBenchmark.scala | 3854 | `61536c155374e1fba59a59e69009026f29b0c405c3a04fa2c2ee8948fb7076b1` | 0 |
| community/microbench/src/main/scala/com/digitalasset/canton/LtHash16Benchmark.scala | 1007 | `c52c8d23588ae7dd7d6db896c23e99c849b309de2996bfa1ad5393826c3a15a6` | 0 |
| community/model-based-testing-drivers/src/main/scala/com/digitalasset/daml/lf/IdeLedgerBridge.scala | 3222 | `38a63d1af6fa114b34a9b80214fd22b99490be9fb697fa09c9c5ccae1dbabdbf` | 0 |
| community/participant/src/main/protobuf/com/digitalasset/canton/participant/protocol/v30/acs_commitments_storage.proto | 1503 | `1a52f5f8f05c02564cc814a7d04107b47a6e444855ec41256f0ccc6f7f1415a4` | 0 |
| community/participant/src/main/protobuf/com/digitalasset/canton/participant/protocol/v30/acs_replication.proto | 10393 | `d6c9daee5ccaf4b55487199d0a011e2cecc02a103641c6f7fd3d428a22c5fc4e` | 0 |
| community/participant/src/main/protobuf/com/digitalasset/canton/participant/protocol/v30/onboarding_clearance.proto | 796 | `9fa69113287a6ade5b46f591ac967aeb7ffba11cc8e9f299dc6cb74913296ff2` | 0 |
| community/participant/src/main/protobuf/com/digitalasset/canton/participant/protocol/v30/party_replication.proto | 4934 | `44004008868ebe88ca4c8f64df9f62c52d27bc9e29128429756b2817481fd2ba` | 0 |
| community/participant/src/main/protobuf/com/digitalasset/canton/participant/protocol/v30/submission_tracking.proto | 1528 | `296a4d951b186002f7b913706bf405c1fb2a63ad4ea8006b7a955cfe1571c4fd` | 0 |
| community/participant/src/main/protobuf/com/digitalasset/canton/participant/scalapb/package.proto | 361 | `4698dffb10aa7df67eb59fe6705bd25e003cd8fe18574888797b9981b620c12d` | 0 |
| community/participant/src/main/protobuf/com/digitalasset/canton/participant/synchronizer/v30/synchronizer.proto | 717 | `036d1e85e401bbb916daaa77f01aca8ddbdcc40bf8d04ccd82c9a52cca90cf33` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/LedgerApiServerBootstrapUtils.scala | 1835 | `9b120727754f5b40b814548efa7b521e7c39fa5913cb25cba63be2eadb7b48f0` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/LifeCycleContainer.scala | 3171 | `aa3db3cf67727baa0d6b3f650450fa97c8915850291fe7a4bc8f4397151b14c4` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/ParticipantNode.scala | 64116 | `a2240385e43e7ae14e8ac8d7fecbeb098a6a1b69599b4b7eda3b482eeae2effd` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/ParticipantNodeBootstrapFactory.scala | 8434 | `3147296e0e7cdb8caebecb0ffdee0627caefc40e186e88c8679b4c6d35df323b` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/ParticipantNodeParameters.scala | 6339 | `a1279ed4329ee44da3d6914b04a4534bf79dc2f7cc98e3df47627ede444724f6` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/Pruning.scala | 2670 | `da50f661bc350c8f315cc300982e84a08ae66926b498efcfd5390742b46542ee` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/admin/AdminWorkflowConfig.scala | 1611 | `d56e5cf7908595546814f5624c13183ef832e1a7a8e4f76b1e019a81664a6a11` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/admin/AdminWorkflowService.scala | 2607 | `683dfbff5c4439e82432f499113b0bb6c858c8a745cfe022ede5f25ae7fa055f` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/admin/AdminWorkflowServices.scala | 21412 | `ff2ca150dc977ed3b5686e9ed61d2e813dfee2fb8b4a1b3342861714a6248a9a` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/admin/CantonPackageServiceError.scala | 10599 | `d40f3b21ae6c1aa141031d8f74c1bf13f719b525bccbf48bfa505fc31610b193` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/admin/PackageService.scala | 30798 | `c52261d7a53d39a301d879fb3d60338f99a76326cd502202fe6b8f8df06e6bfc` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/admin/PackageUploader.scala | 9223 | `43bacd1c0e5d45c5149626f8dbd807870d010c18b906583d261f57352b1d48cd` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/admin/PackageVettingSynchronization.scala | 1104 | `e90b60d02e52ceb63669fedac4a2b6f8f3d56413e9f9218b62342a8d5d255134` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/admin/PingService.scala | 41578 | `50e13ae6973f07fdf02fa318a11da53c0c8774730f5df58f50bca8c06e0257d6` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/admin/ResourceLimits.scala | 3396 | `f42c99628e1f019aea638548915fec5a1d2eb11b358c0563105c0b937add6b51` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/admin/ResourceManagementService.scala | 5292 | `7f5e40372b9d8d99b2f0798c3cd983b71b94dbab9fccfbb87b8ba484ac10f1d1` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/admin/data/AcsReplicationStatus.scala | 12352 | `7c85d785b45fd2766c36eda256d8beb5736536d648752a3a6af685a8d139ff03` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/admin/data/ActiveContract.scala | 3572 | `b88936679fc51e64d54bd24474bc0384d8360cec3efc9e054080c19f920a62d0` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/admin/data/ContractImportMode.scala | 2397 | `4ee4cdd12f634c00c6a74e902e3b56e07a45028e6797e55c2a562b8e649a4253` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/admin/data/ImportPartyAcsForceFlag.scala | 1378 | `f5bb63af1981b9e073eae45bb742857f0de91bc26294aca019723b9b1ea3076a` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/admin/data/LateLsuRequest.scala | 3762 | `fbced2112b8b05cec03b593a512485c73a82d6e06e502f2e51c84c96729f9f92` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/admin/data/ManualLsuRequest.scala | 4624 | `bd6eaa5e3a04f67bbc45e84a3d56ef17f2cd96be30453fc267c032ae819424aa` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/admin/data/PartyOnboardingFlagStatus.scala | 1680 | `f00de90a5651bc7f0c88453c42514040a05e285c72f9ccfb380aed8f3dee2586` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/admin/data/PartyReplicationStatus.scala | 17543 | `83cb8fbfd6b271f09b45e450b50b9b7cd225a0ec6c41171d5af6ffae20f9a61e` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/admin/data/RepairContract.scala | 3390 | `af806075c6dc78b32b0926a1724b755932fc445c5333964c81ae2cbd9734b597` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/admin/data/RepresentativePackageIdOverride.scala | 3464 | `ca6ee90f60cd46e6f92d199d497c5a4cb23c22cce5aba010f9d421423e67de96` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/admin/data/UploadDarData.scala | 415 | `3008a394a07b2905415e217d966a0c5f1157a42c23e7f58e1cd164a97ad56db4` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/admin/grpc/GrpcPackageService.scala | 15992 | `64b9e67738abd2cdbf7090c60dda586a03da35d44b0bad515c5728651817b5c2` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/admin/grpc/GrpcParticipantInspectionService.scala | 29348 | `d07a99c03e21203f7962e42d8e6999f7046062cc2bc4ac335c2d641ce24f6473` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/admin/grpc/GrpcParticipantRepairService.scala | 32565 | `e9dc908af09ad8ba55295cc1a011e004cf877df6e7e4d0110d64ad459874cf2c` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/admin/grpc/GrpcParticipantReplicationService.scala | 3107 | `12ab2cc0533c9d4331d08d121da38be39008ef00a5dd6527bcb1118c13625dfd` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/admin/grpc/GrpcParticipantStatusService.scala | 2264 | `2698a97d90277aaa75a78e38e8e1cfbf5cde22169b7264c2852c51fbc630cb44` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/admin/grpc/GrpcPartyManagementService.scala | 45972 | `d787dda6e209166391a784d879e19a66d658d5c1478eaff99abef891b183e184` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/admin/grpc/GrpcPingService.scala | 3556 | `811b8d6553a14af3e92d9c1a8ed076df8a5beed5d04f4ae17c19c0f7712648dd` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/admin/grpc/GrpcPruningService.scala | 17845 | `85c15d1eb299ced888bff9414ab4b68fc0f60ebee8dbea48959b6d6292729c78` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/admin/grpc/GrpcResourceManagementService.scala | 2129 | `fe32ce099da83a3741d62c0ed323ee55963f98b34929ae515b32f2dc87ba7f3e` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/admin/grpc/GrpcSynchronizerConnectivityService.scala | 21490 | `70d4e936d7f19da597cba056504043daf910baf3bc4602cff69238c8a78fd10e` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/admin/grpc/GrpcTrafficControlService.scala | 2177 | `8146a550515d466d5f9cb32da26c09dc1e90c85d0aef06d0b745ccf028cb62e8` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/admin/grpc/ParticipantCommon.scala | 3569 | `d739182a89a623bcfee1884a4610bebddc87bf7633a5e15c6cbfeea53ed137da` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/admin/inspection/SyncStateInspection.scala | 42211 | `770302de717589645f0629dc60b0bd01ebe639da693bc6db24c2d17e723adae1` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/admin/party/AcsReplicationTestInterceptor.scala | 1792 | `167f4073db2b364a7b67688dadb0972ecba1f0fcd97f1e710d3af7a0eb436f7c` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/admin/party/AddPartyError.scala | 2347 | `646508590805c91294c06212c55a525797c31df690f91e4ef407b4492619fab5` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/admin/party/LapiAcsHelper.scala | 2867 | `62f739296a7b2ebad12c588786ef5c0b65f8a4c21d423a3671982dcb33995651` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/admin/party/PartyManagementServiceError.scala | 10825 | `d4876cd43970832ab897cd5a8a3ac2ba50d3c4f5abdf006305fdda22dc2bc4a1` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/admin/party/PartyOnboardingClearance.scala | 30107 | `b28581bb5f86b403a61786d3e6abae6dfca76c2cacac3ea1d13228f744b1853d` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/admin/party/PartyReplicationEndpoints.scala | 14464 | `01da3f3a518b22897f769381559a68744208beab1d1f036525f61f06b3610f6d` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/admin/party/PartyReplicationIndexingWorkflow.scala | 17509 | `dcc2a418a1ff788a5b176c62677050906a1f6cc0d4d23b01c7f96630d71917e9` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/admin/party/PartyReplicationStage.scala | 6272 | `d8330591a6a83b0f1a2d2ad4e6b77698bfa029e36fe4f532376149a2da204495` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/admin/party/PartyReplicationStatus.scala | 21814 | `25a9e4f08879b2fe96a02ec7269d1d9adca0c91c0e7dbee2265e6c5c2ae40c2a` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/admin/party/PartyReplicationTopologyWorkflow.scala | 28786 | `59663c97dd95ea971d677e636187d6cf0308ad682d44ba2f76b1898e584e51ed` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/admin/party/PartyReplicationTriggers.scala | 3206 | `12985c1b1a803495e66b40c2756f582a1aaf97586629ee2d21fa65570808ac35` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/admin/party/PartyReplicator.scala | 56435 | `2f5af3521439218bdb73dbdbc6f38428c90778847b2bab826feb7edca938af0f` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/admin/party/acsreplication/AcsReplicationAdminWorkflow.scala | 28226 | `e32f2141142914789e6b5752b826c8fd8eb766e355de9e33101a1dc70ca1b255` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/admin/party/acsreplication/AcsReplicationAgreementParams.scala | 3348 | `5de26896a238452e8d1b48606dd3c53ab4b5b80b0050fa04316ad7d0c8dc0ee0` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/admin/party/acsreplication/AcsReplicationProposalParams.scala | 3061 | `e781bd7be01a99a338080d0f9df4b6774d3f4032a807bf2632dbaaee784b45eb` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/admin/party/acsreplication/AcsReplicationStage.scala | 6063 | `dd669e7a5bac531f0c0095fcdc07e07ac8e096f7b652274f74308642f27b6a16` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/admin/party/acsreplication/AcsReplicationStatus.scala | 27899 | `1ffc7f64e94b19fbcd87f69854d3e76bba84d3068451928aef2bfad813f56daa` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/admin/party/acsreplication/AcsReplicationTopologyWorkflow.scala | 6700 | `e4962ac9aad927ad4a387afa1a2acdc0e23bbd10550deb9665495d51cef4b371` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/admin/party/acsreplication/AcsReplicator.scala | 64888 | `18481441a2f91c215c5ead8005a9dbc9f6fa1d3ef30c4fa0bdf129e6abda2253` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/admin/party/acsreplication/PartyParticipantPermission.scala | 2080 | `3d133c8f213e55c6f09b1b0898ceba2ac0a450e6a75e45343b192ba9f4802727` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/admin/party/acsreplication/ReplicateAcsError.scala | 2403 | `d8f856122b961ec293c0e6c2508ba55209212d667a0898bd040f62b0893eac8a` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/admin/repair/ChangeAssignation.scala | 22967 | `317b144a241697c70777a1b5fbd234feeb36891356bafb2f7492319f7c36f097` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/admin/repair/CommitmentsService.scala | 6117 | `303b47e8459c1da985c45ef392d8298b778014e4be672d0aa2bc7a48f06a9f52` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/admin/repair/ContractAuthenticationImportProcessor.scala | 4783 | `68185e4bfb0ac64c026817579bc98923662458259eaf7688ad6ea1420f72ce50` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/admin/repair/RepairContext.scala | 2185 | `ee48b80fde7588abf3b13b8380d510408c2f6e3f94d38991cef114bb01f13175` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/admin/repair/RepairLedgerApiEventMode.scala | 1678 | `f3895f078e0e48656ac007f602b45bf0d0e5ce0bc9f4a1755b517a6bb0453a3d` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/admin/repair/RepairRequest.scala | 2011 | `e3771336abd290056406a5576fb2d500823348bc74af7c8aba9f2b5c7c635f46` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/admin/repair/RepairService.scala | 33513 | `96dbabc5d4ab61432a17d9b75d76b46ce0cd1b9bb47ee5a79005555ad0aee80e` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/admin/repair/RepairServiceContractsImporter.scala | 30443 | `fdb5014e90206c1f445d265e94fcb59bb0dcd9f7e983fed58a5bd5cb3a6388da` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/admin/repair/RepairServiceError.scala | 3714 | `47c0947bf74f954ce425acaed8643a68662d7d08f3532683f20ade887c478b9d` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/admin/repair/RepairServiceHelpers.scala | 13716 | `6720301614a9ad95280f08c136d864b455692f101ac6b22e0daf523ec548417b` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/admin/repair/SelectRepresentativePackageIds.scala | 4983 | `e5da0b6fb1e96b6351c78f202b52aaed9040f36de46be1a82202add2ee324de4` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/admin/repair/TimeOfRepair.scala | 670 | `539f9349fc177335f2f3ae57bdafee0e4d6b007029d8de8063d16f35155c0550` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/admin/repair/package.scala | 1220 | `0a1e4e78d6e66bb1c10d87a1bf27f3e3daeff03d4ffcafe3a634cd23b86f6fe3` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/admin/traffic/TrafficStateAdmin.scala | 1365 | `cd42bf2e018010fc8f33142f969089cdd36486c0959da0cc662cfeaf9438d0dc` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/admin/workflows/PackageID.scala | 288 | `23c53e81d53c0a10e7b9471ad5248a921d437277471bab024e2d92ae780425db` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/commitment/AcsCommitmentHealthState.scala | 3851 | `ce8f42db7166099ebfcf054c2731d764deee353fb1f5362abfa6218ff0f56aa3` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/commitment/AcsCommitmentPeriodWriter.scala | 4828 | `2d1087c8cb2f4b4a6c5215c97d34a8de3c731c25c23812ef7a5b5aee82a9309f` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/commitment/AcsCommitmentProcessorManager.scala | 11230 | `98f6537c1ff59fbd971084e69c1ed25adb2af12d883a5af230c3a09e1e4e4e4a` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/commitment/AcsCommitmentSender.scala | 31910 | `cc5b7da17153212158e4025a88f8d0817176185ec1061b789c7473fa281bb257` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/commitment/AcsDigestTrace.scala | 5878 | `dfe81d01d7342082c987978d320eb2191a38cd82a0a073b07e3496f858b22d9b` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/commitment/BaseDigestProcessor.scala | 27079 | `e06c25fb459243c7887dda4851fb0f2beb09ca22b35f1c6d6206fabf0f7362f2` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/commitment/DigestAccumulator.scala | 1244 | `2da92a53cf44e67d2e243ead38b04e04761b45e6103eeeddb128ea83b4896f18` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/commitment/DigestConsistencyCheckProcessorImpl.scala | 16768 | `78a398d1792b3b700c598f59bd56e9b25b50fd985427907f29de233d29c0d6c8` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/commitment/DigestProcessor.scala | 841 | `3b298458688e5fb2f51bd329cdeae6b9385ffcff15a8b43a8c9e9969a5142b38` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/commitment/DigestProcessorFactory.scala | 11393 | `a45b40f7afca02352aa8ed02c5c8155f7f7e1c67f0bb9c4738bd0991853d5914` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/commitment/DigestProcessorManager.scala | 14331 | `fb9a508682dc2d538e5c4f3ce0e55b89b68b8b8d6e723a9105ab12815524e504` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/commitment/DigestProcessorTopologyLookup.scala | 9734 | `4fee705c5c2796840f7f3f4e151d4ed16b5f73973a749b3e22cc70eca6ade9db` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/commitment/InMemoryDigestAccumulator.scala | 39667 | `643936ee0006016ce3702e77e088c05fd228b171dd24d28b0aa7ec6282f1231b` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/commitment/ReceivedAcsCommitmentMatcher.scala | 16909 | `8caaa8573674dcf80646176b541c7aaa1a92ab71f434015f537b17a87053368d` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/commitment/ReceivedAcsCommitmentMatcherFactory.scala | 6696 | `d195bab96c01d844e63d5e16d3da7f661b615ebf9b61b0bc82374b3a5a7d6bd4` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/commitment/ReceivedAcsCommitmentValidator.scala | 9763 | `5c613bef4c136cd41976c3c42397cd68f77094d2585c607eb7aa45db78f6e899` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/commitment/ReinitializingDigestProcessor.scala | 10691 | `83349fc11ecb6bda6e5b1ee9531af891437d0b73e31da673ff13111bcfedf924` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/commitment/RunningDigestProcessor.scala | 45742 | `798704379d736adfd22284bbfa254caab87cc91dd252947ef791cbf1f6d4addf` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/commitment/SequentialDigestAccumulator.scala | 9058 | `8f4d61383f1f2d189d0ee06611b1279f621187f979adcadeb8c07e1fca29ee25` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/commitment/Timepoint.scala | 1183 | `3ca79d67af1998f130393ea1c526f749c874c268034ec776fcf5c9ec4138dfd6` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/commitment/TracedLtHash16Blake3.scala | 6013 | `f1013579d883793bf626868c177524784a85e2b1d25d44b914194564ac1941c8` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/commitment/WatermarkTracker.scala | 7086 | `a0784992c27fd2e7a820a4df81cc69a3e8a330e4c589d70d2d7a5f50f8f4b4d4` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/config/AcsDigestTracingMode.scala | 970 | `731513caca365f0ac0b10ff64f42f1aab3df0f908e9dcff56b8fb3044808d20e` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/config/CantonEngineConfig.scala | 2655 | `caecdb19b32f4d8a6c2b50417d92190797b9ce1e27b766a400b5be866ab5a125` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/config/DeclarativeParticipantConfig.scala | 18252 | `e30d8d9e36d5abbb12c5de8a27094d6cba8ef05391b8b07493bf444368f37af4` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/config/ExtensionServiceConfig.scala | 2971 | `2e8e8bc0be202abb36e89231f8e6a5413739c094d5d718cdb24fcd591c32bc2a` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/config/ParticipantInitConfig.scala | 1445 | `81e1676a5d3099c27393f979c376f34cbe3302b0498a54fc82c80ee073e45bd0` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/config/ParticipantNodeConfig.scala | 44951 | `56e9e4c00c89da7049fe752b6be954b38eaab2102d3fa037a5e1388bdb4b7d98` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/digest/DigestOps.scala | 5763 | `c1051af97e61a4c6d554bd50c6c667f7b66ca1f7273df848d600a525af205a2b` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/event/AcsChangeListener.scala | 5978 | `267f2eb7d676f7b20b8a7e15d63765c34ad34df319d4ec15996d73cbccc8e7f2` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/event/EventBuffer.scala | 3067 | `8f8ce81383c95d5bab8410ccef210860fab54eb9c210c22cde9c0dc8b7df413a` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/event/RecordOrderPublisher.scala | 24703 | `6e9e2337b82be09de280ca2afcfd36cb4c2b0fc291488719f0e0c01ecc1b3c45` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/event/RecordTime.scala | 3080 | `69dbcb8e9897c5cd29a75b7f9d07c427d96b94f506df63d975bdeff27013289a` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/extension/ExtensionServiceClient.scala | 3857 | `36af1b174edaa0f868c56aef66f8ee185ec1a65f8e08fe13b05219d876bdf1f9` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/extension/ExtensionServiceExternalCallHandler.scala | 3522 | `fe562a2f40636963e11f2f1c8c8a446a6b64fdc51869edd76eaaab71b116d6cb` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/extension/ExtensionServiceExternalCallValidator.scala | 2895 | `f21d7b91e17c0bc0f60de8628298d945da7580a0b54e5cfa13c055e3a14b3309` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/extension/ExtensionServiceManager.scala | 8912 | `cb33127d21524baf4058144695737fc6af0b8d41f6c1939d78d15c40881fce27` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/extension/HttpExtensionServiceClient.scala | 21133 | `939e4a86e03efc18157788337d98f479e4985c1ff46d540c5d06b71f244dac2e` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/health/admin/ParticipantStatus.scala | 4324 | `f34f1cc27efc320b1bb2f350fc959324e0d1cc1218653d451a8a8f364be4188a` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/ledger/api/AcsChangePublicationPostProcessor.scala | 3842 | `d2e2674ac052f18bc5cf2482db47f1d7013fbf472e8a604584368c37129cfe65` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/ledger/api/CantonExternalClockBackend.scala | 1125 | `525fa0ec226233bb27b1e1ead70a6b25511cbb5e9ffc8ba20f0f24c54c51517f` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/ledger/api/CantonTimeServiceBackend.scala | 1486 | `d675668377cf7ae44fca6fc3d05e97cc49ec010c22db1c600030009e2e0b2c5d` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/ledger/api/JwtTokenUtilities.scala | 1389 | `aca5677ec2fab59e4c39f3c42fd81d33244fe984135b8ae029343dcaf40645e4` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/ledger/api/LedgerApiIndexService.scala | 7822 | `053b8f1fa9f3537347185a78a1efae7ad603b8ff42472cc2d4954356340858a0` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/ledger/api/LedgerApiIndexer.scala | 13265 | `fd2c96557f83f396609a4e729486a00faa0edf4e372b2c9eb55845896c1ed3cb` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/ledger/api/LedgerApiServer.scala | 22199 | `3513fd5ffcc02803dbf7d3b327836d6753d33004b5069947709d9a6c56f0e214` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/ledger/api/LedgerApiStorage.scala | 3648 | `5f650749024d40e7a7fa4a2177b5e493fcb41dc491189c6a36051f9ccd87ba9c` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/ledger/api/LedgerApiStore.scala | 14879 | `2a787c84f879cd081fe70718a4988ce47f7e1ea9d1f7ed92b7b89f2cc7e96875` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/ledger/api/StartableStoppableLedgerApiDependentServices.scala | 8363 | `ff89fecf6805c7a1220e45f02925a5f9fa1a0688b43d0a920addb9f6242d1b88` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/ledger/api/client/CommandSubmitterWithRetry.scala | 7944 | `1324cfe3a87988e98d4c450cee81ac692beb349b7f0cbec911b21a8174486c55` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/ledger/api/client/JavaDecodeUtil.scala | 6030 | `bb0745584c19a2fc6c3a6de401f59d73a0c88aeb1f2d55e49350b4c1495b1b01` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/ledger/api/client/LedgerConnection.scala | 3467 | `a9f96241ff6810d53abf3d34da544e2241c5bd7ca3900ead5806727cdba744a7` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/metrics/CommitmentMetrics.scala | 30719 | `6e8f7a82eccfa22bf6148e337810d135d42d3db6fee25bf1820897af31a93d01` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/metrics/CommitmentSenderMetrics.scala | 5241 | `0bd315ad397179c6c4aa32aab1e6d5068142c4d5275f08943ddb0b894b601559` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/metrics/ParticipantMetrics.scala | 18473 | `df9a58f603403a017122fe262b333c6c12317b13a3a52c8e877b437793b28729` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/metrics/PruningMetrics.scala | 1559 | `431b4a5b415856b7ae1a4f9497a7b7107f30a433262052e26686e2791eb22b53` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/metrics/ReassignmentMetrics.scala | 4609 | `665a4b439d503e0db9fbd45c59df6228ce47db4dd8c9e2d13da01dec1598b830` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/metrics/TransactionProcessingMetrics.scala | 2733 | `1fd36a3e3153869038c917b7985ab2588fa7391c8663445ae5df62bd2b8b8ea2` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/pretty/Implicits.scala | 1275 | `9e08f4c3439d30490ed847fd469bae49c4fb8190271a741275e7ac85c3d0fe68` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/AbstractMessageProcessor.scala | 11810 | `2871c425ff789efc6e7bd999ff0c11fe525daa4bbe1385cf0106aaeeedc04d52` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/BadRootHashMessagesRequestProcessor.scala | 3521 | `d9fa0bdbf16b019153fda61d3a2160e6e7feec0737a681249a16b8f0970b0da7` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/EngineController.scala | 3440 | `4663a0ea9df6d4096245ce79b810ea80b122678ff7778710ca8e4b8d96d742c1` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/LedgerEffectAbsolutizer.scala | 4557 | `91d1303ffde020ec8f078e9217bbd6bdb5b43ff37a44e52631143699a291a346` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/MessageDispatcher.scala | 52772 | `9ebbde61f6b16dba15f51fa2133d84432c8b24b6ac90801d87f1fa78e8284907` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/MessageProcessingStartingPoint.scala | 7739 | `fb4df81ba90bbafb3fc348f75776b823672b807b3e27e40d23110797d88579d5` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/ParallelMessageDispatcher.scala | 15386 | `040084e132c19b9cee82047aad332beebab5fa809c1dbe749b33f45a8491619c` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/ParallelMessageDispatcherFactory.scala | 3036 | `d0f3c67111adf3461350d5d66780e28595f24693ddaeb2cb3ad2dbbfc577efb4` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/ParticipantTopologyTerminateProcessing.scala | 23702 | `2f05ef18162cab3d53124716f0eb4701c551032f172cfae098533ee5ac465402` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/Phase37Synchronizer.scala | 11520 | `8993d4861f07fc0a0f561aadc3471217ca350760667f598f16cd85e793d190c4` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/ProcessingSteps.scala | 36261 | `f0efcdd322e012b66f60cdcae445a6d4efeb2aab52a72a205bd6d71cbd7600d2` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/ProtocolProcessor.scala | 94344 | `4f793d33146f1bc91a0f5cf4bce13343909d41913206cd9217f3e18d49fd58d0` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/ReassignmentSynchronizer.scala | 1496 | `f5a0a5afa7a0b4e2aee6276a600bed2b4e80e5dbfccdee18c183675edab41f08` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/RequestCounterAllocator.scala | 6396 | `715176b5f8ad58bd5365cab6efc7ef4d8def7f1c23bc3c7680572ce3f255c35f` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/RequestJournal.scala | 14284 | `a2ec4f5e893bdc6c608f8e42f7e91d72804eac37b77d6fa6a1d6ee8434e13769` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/SubmissionTracker.scala | 14685 | `7bce51322ba5eec2b850aabd42b7f8fa4d28d401bdbf756a621fa32868dec344` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/TopologyTransactionDiff.scala | 9524 | `9b276857716d04ed243150cdd42e81db1bb97e2b9b37793aa3e30d13c0e4871b` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/TransactionProcessingSteps.scala | 71790 | `0f39f3b528af4a52ae917f6a7d04f2026a197f88e98ecdc347b43d487c93f5fc` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/TransactionProcessor.scala | 24758 | `82e52ffd1e6015e9c4af895181d8e38a50ce3eb0705e3b4e4eb8be0b3490365f` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/conflictdetection/ActivenessResult.scala | 3339 | `34a0d12467ef98460c8310c394864d983fa0555543ea05065e063ddb114fb1b4` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/conflictdetection/ActivenessSet.scala | 4883 | `ee52ce13cd818aae35ea8708e980b2ad852ff3576da95503a135f4a71b0169bd` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/conflictdetection/CommitSet.scala | 14102 | `80c4e271d68cf787e8391c5af966f7b205ad1fe5a8cf2daee8b98d3cd6432bc4` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/conflictdetection/ConflictDetector.scala | 39488 | `acffe075af545d99f7e12ce554dbb6131ae3ab6cf531987f68a5dc106d9a533d` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/conflictdetection/IllegalConflictDetectionStateException.scala | 435 | `655d638dcbb4ad55e56620f63b2ec4cd9234b253f465a6eab18f8c6b25d90622` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/conflictdetection/LockableState.scala | 13133 | `1f97ab21f4809a8de7759a81bba5c41095986a139845c7878d63b7be0f0a01a5` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/conflictdetection/LockableStates.scala | 31455 | `1dad96d82934b367b07a39bee0f1116dc6e10d0352c3d779431120c06759030a` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/conflictdetection/LockableStatus.scala | 1918 | `73af50d53a27cf48607f33a52638e05470f284baa0a46475ca4ad8180777e562` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/conflictdetection/NaiveRequestTracker.scala | 28933 | `dcfb1609e3c66be99c9862996612e87ba171ac6f70f591bf0b6794de04dae134` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/conflictdetection/RequestTracker.scala | 24772 | `9dc68b20e006b0b729b28851d239e46f87d5004a86d6cfa4887f532d0f0710c5` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/decrypter/ViewMessageDecrypter.scala | 3050 | `bb16e87eaa0160202c95c443cf91771e2aa63c59988ac2425fcf9e1084ff2e72` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/decrypter/ViewMessageDecrypterImplV1.scala | 11406 | `23c799f2151a9336cf725e525f0a5f36b921dca0880c4b5fff6ccb90a06356fe` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/decrypter/ViewMessageDecrypterImplV2.scala | 27501 | `b3bd33251f220181824fd0d02c1525373f34b1d3e51491f76379c47b4efdcd85` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/party/AcsReplicationContractHandlerFactory.scala | 2832 | `716355303443c3766e3876c80078c73b2503d995eed8bb167c51b002d0769ff2` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/party/InMemoryProcessorStore.scala | 8262 | `4d27e42e2821ca21201acac4f597c4bb2d0ef492e544cd104c560860be9f5b25` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/party/OnboardingClearanceOperation.scala | 3030 | `168e392761cda82ed47f45a9596fd373d770c936cc3ba2901047fbd44efac1f7` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/party/PartyReplicationFileImporter.scala | 10089 | `ec467c703b685f8076afd9655e82ea90c3b6616312cbabb1dc52682ee46a371c` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/party/ReceivedContractValidation.scala | 1658 | `d90ccb2205ed5b4b4a6c88493d8a2add3454ca663b68b4057db2fa57650d448d` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/party/TargetParticipantAcsPersistence.scala | 8974 | `4e62698fef86d24488b2295f25ad31143b6d5491dbdbbb72773577f7028d3632` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/party/acsreplication/AcsReplicationAcsReader.scala | 10782 | `ad97c315274d9d62fce2d5df3f771375eee9b43e3ff5407c2e2d959435cdb2e2` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/party/acsreplication/AcsReplicationProcessor.scala | 4664 | `4bccc2dee4fcc62f656f628b5ee91bc858cf8b6374548992c30506f92e7f4722` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/party/acsreplication/AcsReplicationSourceParticipantMessage.scala | 7963 | `e1dde07233be0752cd7c586686987191a37fa7d48c5b711f5101d4743c27a0f5` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/party/acsreplication/AcsReplicationSourceParticipantProcessor.scala | 17734 | `e617413b2e45f56bb879eb5c8939c85db0ac4063e8bf93bfbe848491df06d866` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/party/acsreplication/AcsReplicationTargetParticipantMessage.scala | 4181 | `a9ea3b9fa163a8024954456b4ecbe920829f19e5a6863359055df0b5332b5bb7` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/party/acsreplication/AcsReplicationTargetParticipantProcessor.scala | 16726 | `2bde0f5aed929069544cfd4c8514348681a3337cfc25219f336bfa73975779a2` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/party/acsreplication/PartyReplicationAcsDigestHelper.scala | 3067 | `9a9af1e2b455533571565ab0b64eb6e6cca9cfb9dba1d64895d3160e72b68234` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/reassignment/AssignmentData.scala | 698 | `55dbf338c3d75ae57f2caca556f548f12ffa0f6c4740b67350f5c136bbd9ac1c` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/reassignment/AssignmentProcessingSteps.scala | 30965 | `1ff31afa321ee6beb9e8da1a15d3b1da7892e92cc9ab55ead890b7ddef721b5b` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/reassignment/AssignmentProcessor.scala | 8238 | `53bee9ae156d483702df332dc6607f4c9f7821d28829d05545fe03b52505951c` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/reassignment/AssignmentValidation.scala | 16569 | `df84010084d65550889eb059c86e9f29fa06fac5ef0133080f5d03421e5b5922` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/reassignment/AssignmentValidationError.scala | 3395 | `9d9f5cdec0d5460701b1635957065964eb683d272a71a130d331384da147f0da` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/reassignment/AssignmentValidationResult.scala | 9802 | `6803031f25d43feb3f00b6f028e51d4a3cf0f899b1478770d2e97d1a823b9f5f` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/reassignment/AutomaticAssignment.scala | 11624 | `42eb13c3aba72e9b24e17311a3891fe765cdbf6783f61a360fc9ed2013c4f638` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/reassignment/ReassigningParticipantsComputation.scala | 9409 | `395bf97466fdc3d4446b1db587b32cbcf96aaced199fe2b5df29ef0515221c4e` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/reassignment/ReassignmentCoordination.scala | 16037 | `8b652765a35008f5b1b3c5dfd4be59ecfc6608cc5bf148d0a7f5f613377343b0` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/reassignment/ReassignmentData.scala | 6565 | `f61e8ae45b8d463725035dee91361fc81ee1e53fd38f9378e454d789bd536898` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/reassignment/ReassignmentProcessingSteps.scala | 34832 | `4ad4966143fe994c196cef800f718a7612fb9d32c958bd918c36f59d825bf48c` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/reassignment/ReassignmentValidation.scala | 11225 | `015cdc610dc78730b0dcc64c5288b3715a4660d0039374e94c9d2f7e11b1d10f` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/reassignment/ReassignmentValidationError.scala | 7444 | `214011193119c28536944ecc2340954b6dc489e5ca9db397832c590360b09798` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/reassignment/ReassignmentValidationResult.scala | 4886 | `24197e84e154ea13b0fbb946e4eff6fbb612ed8e91bc2723bcb380cb8df566c6` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/reassignment/UnassignmentProcessingSteps.scala | 33717 | `5abd17979a737b641bc88e19e32022d35ed290ea41027c61a4349c1d329b99d5` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/reassignment/UnassignmentProcessor.scala | 6061 | `4a7674cd53517b11dbcf68525eec537a99c883350ef6b401cbbfe082671833bd` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/reassignment/UnassignmentProcessorError.scala | 1967 | `82757e513bfa88a0f90a12d2fe4c25c74b54734d2a11e5a39bf800d9bb7db5ac` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/reassignment/UnassignmentRequest.scala | 6817 | `6f9990afeac21f63e211267108cc8bb2661647c75969aab36375d2ee4d117f57` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/reassignment/UnassignmentRequestValidated.scala | 402 | `4928cd2b3ec6b20b8978e1e35b158f6560301eabf3feb7a5bf7b254c8f43fd85` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/reassignment/UnassignmentValidation.scala | 14476 | `2ea9f5fcadfac387d57e3505cb71333adb7bccb88b9eea0e729fd4b74d777b7b` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/reassignment/UnassignmentValidationError.scala | 283 | `dc37334e4c18773495ea238215f122e9edef024fe3423ff2abc62d9ee16daeca` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/reassignment/UnassignmentValidationResult.scala | 7230 | `656ce7d42da04884dbcba6bf0c5248622e294844e7a9e3801be330eada1d5019` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/reassignment/ValidationPackage.scala | 3579 | `e9741d6e78d3bf89292b61c061b687a41e5a318731e3d7a6f1d8ccddd8aa65fa` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/submission/ChangeId.scala | 1378 | `849f65239aea4d3ef23fbd8768bfdbbbfedb3d612b8b1e58d1ea1c0deb419c3e` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/submission/CommandDeduplicator.scala | 10227 | `1c91269cf851c6bb73978fe01ae3332b36d63471f5568b47d25464bcde0401e1` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/submission/EncryptedViewMessageFactory.scala | 24563 | `563a913c8bd9de1c95a2096fe000729d46c249a2d18b5d8d6c320cbf7e2a28d4` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/submission/InFlightSubmission.scala | 9108 | `09347a71ff229a62a59f06bd5f5f0ab791313cca01630cb43d5c07ef5b1864a8` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/submission/InFlightSubmissionTracker.scala | 24689 | `bcfee2e3121070289381771d3111f6babd4898a193a7e6b53de6a543063d63ed` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/submission/NextGenTransactionTreeFactory.scala | 36856 | `f1dab4f786ef273d8b56b622d16850b84a970982f66f6858bb712aa87c1e3694` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/submission/PartyVettingMapComputation.scala | 9302 | `51b129145e55f351aebf937b801f96f5d78a97a17e756a665da795b83237d3c3` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/submission/SeedGenerator.scala | 522 | `f5d6ea93f6e2d586c2215d2886ea951a5c74eb6c4a73708c2da7418cf9237dcf` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/submission/SerializableSubmissionId.scala | 1756 | `14111ec98c9a52ff241c9339e1228216be6934ada93a200cd28e2c5b60e8426f` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/submission/SubmissionTrackingData.scala | 12974 | `ffd3c474ccc04e0d88a11a6215f46b06f3bf9fc6d5a49e0c36737d1fe1c3673f` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/submission/TransactionConfirmationRequestFactory.scala | 31294 | `1c4bf38cef7f3d97b7833bd888627128d6949a8dcdb1bac8bcc205eda89f3436` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/submission/TransactionTreeFactory.scala | 11574 | `8fa719cf3c23bc5845f3804fe306f8e3781d523a226e86a8099ccbc9cbcdcec7` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/submission/UsableSynchronizers.scala | 12952 | `67c690a66e02a42537cd4d35d14cdf13be1df9024953c3b083a77ab917207134` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/submission/routing/AdmissibleSynchronizersComputation.scala | 16815 | `242ff36c78fb7bce2b075efc636ad210e007aee7e8631321aaa57169efa0a378` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/submission/routing/ContractsReassigner.scala | 8582 | `c4c9751c36be89d3bad2f9afbb873ca52e644668a23f51933fcc0f48f1bf8ab0` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/submission/routing/ContractsSynchronizerData.scala | 3466 | `89e33ac331bc2eee9cd31b65fa50f6450dc78f77567a4cf483aeb717c49eee15` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/submission/routing/RoutingSynchronizerStateFactory.scala | 6182 | `747079afeccf0a372f4fef5499d9943a2ec3e2651edb95fabd4b22dbde8af9da` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/submission/routing/SynchronizerRankComputation.scala | 10093 | `90734c318d8351f613ec149840c0a01e806fec1e5b085467a1e5da1ce20f4cdb` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/submission/routing/SynchronizerSelector.scala | 12136 | `08c03c3df5e594f252f9553b47fd5e24b1fc3eea1c65be8986002cb01d0c7652` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/submission/routing/TransactionData.scala | 5509 | `1e92f6ebf33d1151c9face4fb89c57c1c5bac4e32ba009812566bea0cc8a69ca` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/submission/routing/TransactionRoutingProcessor.scala | 16903 | `b675a56756c236e4867496090b3a89026dc9bb414113a76db1c0e0c6fbfa72ad` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/validation/AuthenticationValidator.scala | 16175 | `443c748400f48c951f36e104794ec6dc84de934a0a0270400506dcce0c222b02` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/validation/AuthorizationValidator.scala | 6149 | `49b6937e637c7849a2da7461a0d7409b117780cf2d343b9a548fc057871dbc4a` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/validation/ContractConsistencyChecker.scala | 2405 | `938adb23229a212ef7a04aea57d653f92d961cde1ec5c06d14b6c56fbb8c49fe` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/validation/ExternalCallCheck.scala | 13905 | `d6fa5471c580deeb0e174de2b181499a0be6ffd944973104fe88cf9c7c18b51c` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/validation/ExternalCallConsistencyChecker.scala | 6082 | `30ae3fbc72207dc6d787eddd8e26bae5c02e19f2bbdef5725b5ca5eb150b8f5c` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/validation/ExternalCallValidationError.scala | 1023 | `f0ff14df247341e9640562b726e48087f3fb75bc7a404201a397b4abd3698077` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/validation/ExternalCallValidator.scala | 897 | `f6e44903e8fce005135969431da9a605919e348efc186024d79f10e25d2e96a3` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/validation/ExtractUsedAndCreated.scala | 12604 | `963b1ba7e67e648ec00606a5158c43fd5a86851c94ac315b373119e02f427dbc` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/validation/ExtractUsedContractsFromRootViews.scala | 1043 | `045b6fc5e073bc467caded6244989a52fe3fc344b860320436f5612afb9d30ff` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/validation/InternalConsistencyChecker.scala | 9082 | `3ba544709ddaaf7368505f8c1a1a1776785c759226d7e68016b3d0357ba097b7` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/validation/ModelConformanceChecker.scala | 33323 | `12ac67e0649d55dd9b7068c905374619656a5317a0712a889ad5400e184d6380` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/validation/NextGenInternalConsistencyChecker.scala | 3891 | `8798573393dd3908a1e2acee8238bf9e7c78be922c06594a288c8084c262edb3` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/validation/PendingTransaction.scala | 2277 | `d11f486bdecd2c9533cbc8fc02e93607f7148786be890ca9e65ba3bdf0ba9c63` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/validation/RecipientsValidator.scala | 20657 | `8702cd5c32cf4c695bcd278c78acf4dd6426d6f7eed6ef1df4dc8d5a2049c464` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/validation/TimeValidator.scala | 3387 | `8d33cc21da54e8af764395cc0640409939c634e0f9cde4e74a0e93e1cb0fdb5e` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/validation/TransactionConfirmationResponsesFactory.scala | 15549 | `dd287957aef9094e0a39fa2202569234b2cf84129a0a56bcb5ea6c44b3455790` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/validation/TransactionValidationResult.scala | 3295 | `f9f03f712f30ac16150475473023687fea8b9aa136d0af6dbe8d19d958a89cd0` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/validation/UsedAndCreated.scala | 2177 | `3a56e887ebed59021d7487e40c1fcd3e8b6baf7cc9d2a616012698b95c7fec82` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/protocol/validation/ViewValidationResult.scala | 903 | `e04e845e70273d8479e1e68f25a385f9d373bd20cc843b2326ad12ebfee7a080` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/pruning/AcsCommitmentProcessor.scala | 162321 | `6d1d7fddc7d1a12ad5a692268fe18a3f3e2386b8b8ccaf18442460cd2f44dd6d` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/pruning/CachedCommitments.scala | 4380 | `5d1b734642c2edace4f724917c216178dbcae0a0301f5b2c61ce09e3a2d6dc7d` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/pruning/CommitmentCommandsHelper.scala | 30666 | `eefbd79b6dbd1e2e9cd7a621e58d693bceecd11a07b43289f7e5e0f928be427e` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/pruning/FirstUnsafeOffsetComputation.scala | 21810 | `62a616852f32a76fd8ad7076a0932c4fb130bf9c26da5cbcc004734b8a9ee535` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/pruning/JournalGarbageCollector.scala | 8105 | `51dfbe98b4d9f96b1ed243d4cd6cad7c1b24295f9e53e38656caf28c19a0e301` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/pruning/PruningProcessor.scala | 26957 | `7cfbcf5ada613d2b72e771e82e61ad031b99d726b98b32e1adee7a8c51e9e920` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/pruning/RunningCommitments.scala | 6392 | `f0aace6e98c0678fc409c39719e56908014102b12d2df5270e34fd56672712dd` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/pruning/SortedReconciliationIntervals.scala | 8944 | `10438687934f0c7226fd94ccdaf982250ced3fa3be6ba6ede94c91052c2e6db1` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/pruning/SortedReconciliationIntervalsProvider.scala | 8877 | `0c77d85b25f1c5481bbbdc5d11673fda6aa87d673498f1165f3527e66cafff76` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/pruning/SortedReconciliationIntervalsProviderFactory.scala | 2232 | `1120a56a2ce22264fe5e78d4a2e61fd96c06aa4e6464c4e1b198310110d37d05` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/replica/ParticipantReplicaManager.scala | 11014 | `d6db58d211c20715422f7e807b86ffea334bcb5851cc3f9ed04e58247026e9e5` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/scheduler/ParticipantPruningSchedule.scala | 1588 | `4f8c2bf60d0a0a692b8398984e6038125d87c1673e003f12e5eb558e51ef5b14` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/scheduler/ParticipantPruningScheduler.scala | 12502 | `46de8fea2f5bf86415c0f508ecd9cd6b453badbe7c8d9e94cbb23a894d241490` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/scheduler/ParticipantPurgeStoresAfterLsuScheduler.scala | 5235 | `4759b92c270d54cc369ae680d314820320574d9b84cceb4b9d94633b8204163f` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/scheduler/PostLsuPurgeableStoresComputation.scala | 6167 | `1ad56e2bb2b7105c2ddc64011469d711a524662ca4dca7d8360ce88fa44f352d` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/AcsCommitmentConfigStore.scala | 3842 | `5fbb2b682babfc6ef3ecd2809e2a7bd30fc80ffe3c815fe8c96e29ac5f1b6303` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/AcsCommitmentPeriodStore.scala | 28088 | `63f644490c511c10457a40367a99c1805c3a94dd79ca6f9e8bb9d6a59c034d3a` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/AcsCommitmentSenderWatermarkStore.scala | 719 | `a6247134873bf3afe20b34c9d742c775947b4141bebe5b553c313b81d524564c` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/AcsCommitmentStore.scala | 19198 | `0346477e3ab910dab203078538f1d64b8732df9a5916f1da6d9c5b951c5c210c` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/AcsDigestJournal.scala | 1682 | `7c0c5058c4b6fe2fee837fddb8e310fe9cab0fb7b07a8a9aa9b417089ec1ee66` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/AcsDigestStore.scala | 31605 | `3a618d8d601910b659bbdabecffb9c92a846c88c8e4b1245a8352e79518338d2` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/AcsInspection.scala | 13437 | `9ac4d431861441a22e6bf342140a4a3394ecb28deb4613589a6642df22e30c33` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/AcsReplicationStateManager.scala | 13075 | `2435e37002e908834196e362184adbedbc286ccc12a7d1d124c09dab3608eca3` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/ActivationsDeactivationsConsistencyCheck.scala | 3964 | `d79f267a0f5cb6e89973a1bd8bf3e4d5627cc389c0db32fba45a9deb27408219` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/ActiveContractStore.scala | 43687 | `cc88bbcc4d85fd2bb2e5f7891d3c2a95c7c0aa2b022c47721ca8a727a52c3149` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/BatchingAcsDigestStore.scala | 8976 | `6118c92a2bab7b26f083fe7165f8ff54f540a7ad8c94390f2328db857de7e71f` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/CommandDeduplicationStore.scala | 10775 | `4460f9966014ae44c1388eedab14dd07e0ef21bf9660a179bf78af297509e72e` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/ConflictDetectionStore.scala | 1464 | `168966448438f70cc80b61b6926726b5be6d6ec64babb300c70ae2ae7696ee51` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/DamlPackageStore.scala | 6605 | `6f136984f320ee266eca796e045058f97cc752bda3c7d752dd19610737e47161` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/HasPrunable.scala | 325 | `9eee6a857813490f3d547d489872df41c50c755f78c870a611624b8d5af5f35e` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/InFlightSubmissionStore.scala | 13231 | `641d661752ae74c6621f04eeeeabafa011ab7f07924d2d1decae91b162c55eec` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/PackageDependencyResolverImpl.scala | 1426 | `d2476f437ccfe58eb42b0f57921d2f2c1805ba248b82a65bd85aeb5b2345f262` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/PaginationTokenDone.scala | 222 | `1697d3b6bf43566e784acc7cd2f3df5ad1909a043979e898c025a46a9c88c969` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/ParticipantNodeEphemeralState.scala | 707 | `3b0e951fdb46b51176b3a1b89f87784427074a499a4c0f1320229f6e3dccb55b` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/ParticipantNodePersistentState.scala | 7644 | `2b1b72371d3ecc6b132f3a49403b1bed1c842a4e99542e36b29dffeb72d281d9` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/ParticipantPruningSchedulerStore.scala | 2523 | `845839d96b600229e4dee018c5261bd2d5e4ea25cd43aaa42c0eba457ab44d12` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/ParticipantPruningStore.scala | 3267 | `2a2bb641ed807422a6cf39139262521f0ee7e927d7d45b91401b0d4650f470ba` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/ParticipantSettingsStore.scala | 3553 | `51ee1e325f2dcd8f0339664984c24d23dba16c6e4cf038470eb695b98e73cd73` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/PartyReplicationIndexingStore.scala | 11542 | `c928dfe147a909eb32310742f792b2a4ed3295bb293ef3f47b30fcd81991f744` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/PartyReplicationStateManager.scala | 11605 | `d4f33ed5a961f987b7abdee28030127c4b1ce6d8d0d00231c979a52681593486` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/ReassignmentStore.scala | 26763 | `4da5b6e823a27bd416afd3f0b2e6b9cd74f3aa8cd5d4233ddac47e9c7f9b32cf` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/RegisteredSynchronizersStore.scala | 2945 | `92e6bcec80848010e0d929875506a9d751b0a60f60e7688aca2d223761b12bbb` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/ReplayContractLookup.scala | 1734 | `fa7dcd9c030e45fce775ff1763190d6ca428f8e112b074b38e0e641ca32b9e6e` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/RequestJournalStore.scala | 7971 | `69ec86b49126794c4058713eb348ad45d69f92435231b54df35b7855ce144157` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/SerializableLedgerSyncEvent.scala | 2536 | `378db2f4f1d8316bcd879a9c32270cfc3a3802ade49065e4a1a4288ec83ef52a` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/SubmissionTrackerStore.scala | 1830 | `b86ab0dde52c8f03dbbb47c4b86ec49e3cd53f9e43372c107dd98547c8e5ee4f` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/SyncPersistentState.scala | 9820 | `575da04a2ce6d4bf7446a93f3b3afec21dce54ed75cb5ebdc4cc1395f44532c1` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/SynchronizerConnectionConfigStore.scala | 25049 | `b1401f8833ef4259087cad34a6c836c16870b8edca549deecce337bf64820867` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/SynchronizerConnectivityStatusStore.scala | 2246 | `5a480a8fa9b0ae8b76a10039c1a207bb04044af914c3a38e915796f53be2435e` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/data/AcsDigestJournalData.scala | 739 | `79a740571b26659b255a33ce191f17ffa08342939dc9de42b63450ff91a24e89` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/data/AcsDigestJournalImplicits.scala | 2088 | `6dad4808f743d519b5be7ad78737f3c6df9b662b6be7cf6b93d6b4c213ee633d` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/data/ActiveContractsData.scala | 2315 | `1a983aaaddf2cd84dd1b31f16ed32911ac6750e62092484dad0b3a34f0c2936b` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/db/DbAcsCommitmentConfigStore.scala | 11530 | `49bd6f8b2431b94442aa1604941b101aedcd287ef77d61b040d5480e14eed0fe` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/db/DbAcsCommitmentPeriodStore.scala | 33993 | `b1e70652a71b84d51d2eccb9ebdb98e62b3f0853d1c42345e417bbba5314a2f0` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/db/DbAcsCommitmentSenderWatermarkStore.scala | 2730 | `3ad9f6f9c6309dba65b6d6750803d8d0fdd6cad188bdfedb5ee2d425f1e25264` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/db/DbAcsCommitmentStore.scala | 39648 | `01376e6883e0e6bd5aef9b5bc0d67a83108978a053299708f2fa69b0e344960c` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/db/DbAcsDigestJournal.scala | 21737 | `24274ea76cb7fe2dbb685f99b5e9510cfae90309183d9f29afff65b16ea3fbc3` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/db/DbAcsDigestStore.scala | 14264 | `b26d75d50440cc4f7c1e492c69e8c8bc63778a5577751aa57f05dc0f02f92d6f` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/db/DbActiveContractStore.scala | 53149 | `60010384f3808f606cc9738b00187f186a49b6b3bc2a4c9704af5730da93663b` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/db/DbCommandDeduplicationStore.scala | 17127 | `df5ce059d9cc42d3c09b87b1d14900143a43d1a84691d535541141e8383c6f5e` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/db/DbDamlPackageStore.scala | 12092 | `84c6172ede282c2f044fc626762f35df9fff8c945b7b34852e17f602d01657e9` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/db/DbInFlightSubmissionStore.scala | 24234 | `60464bfa2c65902df74057973d44284dd720442691134715300d0c3d4dc60d82` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/db/DbParticipantPruningSchedulerStore.scala | 5210 | `5dc0a68a1e4b15fea7d125cbb6d10b088886d01c107fb42e6c5d4cedc1c4bc2f` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/db/DbParticipantPruningStore.scala | 7037 | `b40a7b66ded353fb5100c82a7e192c95bc4c2c7facf175a7d92524439328db98` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/db/DbParticipantSettingsStore.scala | 7553 | `022bc54045ad3e31d615cb24b5becf3a14fde4d5b44ecfa8b5d64c58f256cc72` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/db/DbPartyReplicationIndexingStore.scala | 13466 | `c641a1375252eb962ba493563e881a3f1ec46c216970d084e85e364e1a147c2c` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/db/DbReassignmentStore.scala | 35138 | `e52946d96dd692d345bb0d2854d2fc6a41b55952829307c72d3b0ae8f9073ee7` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/db/DbRegisteredSynchronizersStore.scala | 5729 | `b1e53c8345f3d6db5a639c0b7ab8b4e8aef0cd00fcad262d97fdfec6c3d136ea` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/db/DbRequestJournalStore.scala | 17935 | `b4ef76e285998a2035816ba02c5e0f754adacfd8b2d8cc5f639c7d7ae88c8668` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/db/DbSubmissionTrackerStore.scala | 6439 | `58be5921d229eb010177d588a99ce7635112ea5babeab5953de07bee70c51c7b` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/db/DbSyncPersistentState.scala | 8115 | `2b3bfd364aec20f683496230e30b4a44f354fd8d6ea2b63e6c109b8786a5eba5` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/db/DbSynchronizerConnectionConfigStore.scala | 31507 | `96a6c429547a07fa5959c75eeae9018f8b797d9a6629c90f2f71addb5ef9242a` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/db/DbSynchronizerConnectivityStatusStore.scala | 4663 | `68ab0e482e020182e221ccecac6c7fb4699bc0775bf8f12efa238e1d30fe134d` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/memory/InMemoryAcsCommitmentConfigStore.scala | 4413 | `aec2b0c4aab0e5d168e2feba34a1798cf2f88446033fe6da9943cac726bfa346` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/memory/InMemoryAcsCommitmentPeriodStore.scala | 14038 | `6efe0ff13656e5c765d5d92113c61c0e424522140eb7d790bd592a7d6ecc6955` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/memory/InMemoryAcsCommitmentSenderWatermarkStore.scala | 1493 | `b651c0e84829ac4adcefe3c1e749c44875dbe6b6121d75e7f87a97e1f788898c` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/memory/InMemoryAcsCommitmentStore.scala | 20392 | `817547a41b61480c4ba2805643d6770a1549f1f7edafcac681b4a14162ed1b00` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/memory/InMemoryAcsDigestJournal.scala | 10171 | `83f2a6e82c3769fffb51cce991f039a389bd13c8c8e02a803e0fa56ce573614a` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/memory/InMemoryAcsDigestStore.scala | 5389 | `31af3c9a8bfd17758153726cf8e3b1251ba6934a03a384867de89c8695cdd764` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/memory/InMemoryActiveContractStore.scala | 33212 | `b754b30b5405cc9e98154134c96b6fedc488790ea720e93bfeb5d5d985766c42` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/memory/InMemoryCommandDeduplicationStore.scala | 5296 | `ae3d9da8eb1754b68cd2cca67cd268e399699b6b0a5805897c179cb1cb5ebdf5` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/memory/InMemoryDamlPackageStore.scala | 7532 | `5257d7504f0d9d760f8a44b9ee6839c795c87a4c6e88623ea9df52cec939d1e2` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/memory/InMemoryInFlightSubmissionStore.scala | 8862 | `bb998b19c990668f1dcccda57c8e08a48a42b55568fe97c6aeb4d4158f22efcb` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/memory/InMemoryParticipantPruningSchedulerStore.scala | 2950 | `f13095591caa811a9bd465579552da589b172081152de0a35c6a604b6430cefe` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/memory/InMemoryParticipantPruningStore.scala | 1905 | `761f648f5a609090677c123dff993e87ed47eed8d7d97f94f631180a7a070d23` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/memory/InMemoryParticipantSettingsStore.scala | 2167 | `ea2052ffb6b3551f735f3e179df78b5e0818c102433df104c37b0f85d9987dfb` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/memory/InMemoryPartyReplicationIndexingStore.scala | 10578 | `2a984af78726f04e562ebb32e0274849186bc839bebfbcda565ab26e154ff663` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/memory/InMemoryReassignmentStore.scala | 18674 | `886481e7a0768a904917fd515ab780f5145a0600f7ba3133a9beb1a8a0a4738f` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/memory/InMemoryRegisteredSynchronizersStore.scala | 2937 | `e960644529eb184b819003a2dd8a76789ca4f5a5a3e52269c7edb6dab18714e5` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/memory/InMemoryRequestJournalStore.scala | 7109 | `c8bb40a90583dff1f6962f1f0ab757ff75b0bb830c6d40d89dacadcb0dd2d51a` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/memory/InMemorySubmissionTrackerStore.scala | 4142 | `5cb8032d31019464a7eacd5f860e78524a19b06fa9180efbbec30d2e8196656f` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/memory/InMemorySyncPersistentState.scala | 6204 | `0d9372e115fa16ae015f6e5decb3186db23c3f1e3b0f4fedd9dbac731c13c5ff` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/memory/InMemorySynchronizerConnectionConfigStore.scala | 17662 | `58995fe4e739e4993c254ca2f986d12acb09307b6c70e2da5af3fc89c371f9e3` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/memory/InMemorySynchronizerConnectivityStatusStore.scala | 1919 | `1220964403f979181687d4b3c707f049ee4217f30a9755e11baa5698119e328d` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/memory/PackageMetadataView.scala | 7557 | `86eaf0112d63853f14eae172d32f84de5ab0f8c3998f90ecc3cb1cbb9cbb59f8` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/memory/ReassignmentCache.scala | 9324 | `eebf1d3791ce3707f9c0b3f8e8d8188021961b7ab989b3c28d947feca079b5f6` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/store/package.scala | 263 | `a89605336e58fe2560beff95d92e0cd7b642af75d9ec342e6eedd00c6afe7c41` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/sync/CantonDynamicSynchronizerParameterGetter.scala | 4857 | `2c5e0d465a77117436f5b64f78da709c3efa2495c7cabd1f7d4ba33a873bd93f` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/sync/CantonSyncService.scala | 93303 | `97b7010cade380f46eac100cbfc749fe9c7fd86b4002c5396079dc252045e984` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/sync/CommandDeduplicationError.scala | 2958 | `9ab39fa6412233a88c62692b25020a36d9e533ebd2185bcf76f9320f0b092ae2` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/sync/CommandProgressTrackerImpl.scala | 17991 | `172f78a8025c4fa59edaf07e29f6f4f2400a879e371d24340777c7c4aeaa89a3` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/sync/ConnectedSynchronizer.scala | 63392 | `a18f7833250920f70136124db8b008411e7d4dce9bcad660bc5ec1c730af6165` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/sync/ConnectedSynchronizersHealth.scala | 3997 | `13694d58ca0d11db95dff65ff8a960d9185a6ff0361ac8ad1111a7ae87cd8976` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/sync/ConnectedSynchronizersLookup.scala | 2391 | `5669c97c421e387602d1adbb2e1212e9a5ae5a2de1bf3b999d5af0b1e131baff` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/sync/LogicalSynchronizerUpgrade.scala | 57127 | `4bdc7ae3c2300468edb78d2a9f13ee34efca4f436a097672860c76b1020f448d` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/sync/PartyAllocation.scala | 5011 | `3b3bcbb0e9b964c6d407497793a29ec22173e8fef30c4292073660cb213475db` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/sync/SequencerIdsRetriever.scala | 5460 | `fc64eec7ee297e253b756675bf54905c7ed9f201002dfd7bbaa323c3da08c221` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/sync/StaticSynchronizerParametersGetter.scala | 1394 | `83ea7f5028aba36ccce63476de11eddd39431fc7579583843621c61fcf993012` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/sync/SyncEphemeralState.scala | 6919 | `7e332d83a4f7b7dfa6bbd5db72f5ec24901b938fe121ea432cc9bfe1dbd1e524` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/sync/SyncEphemeralStateFactory.scala | 21476 | `58bb61458e0bc9300093ff3286b64c37c92b4e20aae0872c6c618363e703915f` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/sync/SyncPersistentStateManager.scala | 23152 | `1f2646141f30cec56fcbe7fa8578961212441a8d1d6ecf3688703ed491b88004` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/sync/SyncServiceError.scala | 21105 | `9ac942a527c7d6ab0f02b7f3c3606ee041d2ab25af586976d12dd188ce655a08` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/sync/SynchronizerConnectionsManager.scala | 77173 | `69a74a128a9623660e338c188538b4761cc4f15919c508f46094a905b893f744` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/sync/SynchronizerMigration.scala | 22114 | `a053b3392d1b6aac34988306a9a21c7621715f50cc4d2806774163a2c276441d` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/synchronizer/PendingLsuOperation.scala | 3165 | `2151eae4ff10e1c21527d3bc08956fe3263ab532b6c0d5597792ddf731fed30e` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/synchronizer/PendingOnboardingTransactions.scala | 4267 | `d18294304f484854a4fb0fa85143589cec6743854937bf1711401ecdcba4d8bf` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/synchronizer/SynchronizerAliasManager.scala | 6279 | `6184a1b660e7587522e17babc64e8858a6df6f102242bf6d039e93e3b186d7fb` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/synchronizer/SynchronizerConnectionConfig.scala | 13809 | `a8129e3386a0a4024ec4681a49c6858aa70e097d9b00718d4e343b1c841e4af4` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/synchronizer/SynchronizerRegistry.scala | 19190 | `0f4e587408c3c7e41d3f56b30b31aceaa5c833112a5c397d89cea4a966dc21f8` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/synchronizer/SynchronizerRegistryHelpers.scala | 24260 | `4eed696789183bd561748b18f868aae756666ba91449efa8572eb6485f072617` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/synchronizer/grpc/GrpcSynchronizerRegistry.scala | 21966 | `51b48499d0898fafc017c0fc6d8e48fef20d7881fa73ab2230148c3d66e45a77` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/topology/OfflineTopologyLookup.scala | 6349 | `449405f50727f194d5209e8ab0c8c4c38caf6256189fe0e00ab7ca06c970f668` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/topology/PackageOps.scala | 21206 | `a5cae9d867c57adaa7fb6ab148b59dfc028ee4d9050438b244b6380f057687e4` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/topology/ParticipantTopologyDispatcher.scala | 21568 | `c52dfbec00083e66fb46d1d5937646cde3e392c7fe305db13928f483707b34e8` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/topology/ParticipantTopologyValidation.scala | 11740 | `a4ccc8cb6c4fc65b1175478fdd81c2cdc4e0b17215cc1b660d169c4ce4bf6e4f` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/topology/PartyOps.scala | 13116 | `b450929520e2e70cfd998ff15c7aa800ca75f565fe74d925e4b3c5204509c543` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/topology/SequencerConnectionSuccessorListener.scala | 10973 | `9b3e24b8915e1bb8886b7f60d616de748ecc09c0a6b495ce1e6612e552555f29` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/topology/TopologyComponentFactory.scala | 13574 | `fd03f41c1509f242783e93cc61a5110be7260fc2f2f8c550c61951ccb490e92c` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/topology/TopologyLookup.scala | 9365 | `27beff678654de7181249858feaa29857b8b3228d94e5b0ae02e335830017955` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/topology/client/MissingKeysAlerter.scala | 4454 | `faf47827f0a0ed778aab4df8f5cf45f89319fa2cf2f85cfe5932a40c39ea6062` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/traffic/ParticipantTrafficControlSubscriber.scala | 2035 | `01093712e3797cd39ca424b7d7877f54576c657bba6678003e1f87321dc57057` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/traffic/TrafficCostEstimator.scala | 27410 | `71eef052c5c8f0ae32c079165d7f2a2c0660a6c5bf40662f1857411c0b23931f` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/util/DAMLe.scala | 19932 | `33d4939e3d2ed3a68c80679123863973583364aa41b8c89b54996285cb067be4` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/util/JavaCodegenUtil.scala | 477 | `eb59e366f18d74ac1fccca7277dffa59d17b5d433f25509ee25fe4629f089006` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/util/StateChange.scala | 1683 | `d3272ff38044573aa828de1771e36e8b988ddd230395961cb1493ff93d289ddd` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/util/TimeOfChange.scala | 4562 | `f939e04162e948e9d203a3133a7cad90c88362dddbe7207a63843f72673c27b7` | 0 |
| community/participant/src/main/scala/com/digitalasset/canton/participant/util/TimeOfRequest.scala | 1696 | `a4e0bb7e5412a70ccfd14b20de17dd5c510ca63d5b7d2220c3afb5fc32804b45` | 0 |
| community/performance-driver/src/main/scala/com/digitalasset/canton/performance/PerformanceRunner.scala | 25178 | `71df4f05c798f5151c308fc094d0caf8fad22c4abccbc2b805ec8a271aa4da29` | 0 |
| community/performance-driver/src/main/scala/com/digitalasset/canton/performance/acs/ContractObserver.scala | 2341 | `cc98d704b23e9bf7e59c72be15a6ff04dea29c1c6c66f34c21408ac188cafcdb` | 0 |
| community/performance-driver/src/main/scala/com/digitalasset/canton/performance/acs/ContractStore.scala | 8671 | `e988e0128d0927075b870eb3f9d26ac1b34579f2f4d12132397573edc596dd64` | 0 |
| community/performance-driver/src/main/scala/com/digitalasset/canton/performance/control/Balancer.scala | 3668 | `7ebdc8d1349c4b7131b528d4ee173a477e42d5a413bb475dfc269fafd03a8290` | 0 |
| community/performance-driver/src/main/scala/com/digitalasset/canton/performance/control/LatencyMonitor.scala | 1196 | `772952b567dc59452f00bee3aaea412dfd0a427236df1c1b01f104f84afba1b8` | 0 |
| community/performance-driver/src/main/scala/com/digitalasset/canton/performance/control/SubmissionRate.scala | 16743 | `c2951279319c2997e86b7792ce27105a277c3eda609d2df03d7760c2c0744b88` | 0 |
| community/performance-driver/src/main/scala/com/digitalasset/canton/performance/elements/BaseDriver.scala | 27649 | `715c94e9ef201b04674221da7a8629ba38141bbf333be9fb98e891e5e26634c6` | 0 |
| community/performance-driver/src/main/scala/com/digitalasset/canton/performance/elements/DriverStatus.scala | 2894 | `da7294fa56e0a0fc86fc6f11bfef8cac51459f051e9c5f9d4d9bdabfeecef0ca` | 0 |
| community/performance-driver/src/main/scala/com/digitalasset/canton/performance/elements/MasterDriver.scala | 25216 | `fd5be43d96e7a2b3b1d0ef4eaf6d0b3e9a54172a16c0376211c875d4463a5569` | 0 |
| community/performance-driver/src/main/scala/com/digitalasset/canton/performance/elements/ParticipantDriver.scala | 10545 | `7f918dd0772b8d15ae57ae0befecfc1cc79f450974e902b16dbec1d2441eaa12` | 0 |
| community/performance-driver/src/main/scala/com/digitalasset/canton/performance/elements/PerformancePrettyInstances.scala | 1973 | `1db72487b8c7c6785477931cf7b04c1d7dedd2795c72c9fc41b59ff3bd38b8a0` | 0 |
| community/performance-driver/src/main/scala/com/digitalasset/canton/performance/elements/SetupDriver.scala | 8261 | `2d96237bbbb990c648220e5d44aeabc9132c146612578deecc16ab6c4f9601e4` | 0 |
| community/performance-driver/src/main/scala/com/digitalasset/canton/performance/elements/dvp/AssetUserDriver.scala | 4594 | `a78013a8d6312e2d7c8ce4b642546b82e0c11437feb220e15d999e19d7693574` | 0 |
| community/performance-driver/src/main/scala/com/digitalasset/canton/performance/elements/dvp/ByStanderAllocation.scala | 5740 | `00543d8ea46fbe87eccc0de78de53599cc1ba49259e4eb47a234ea9b4072a027` | 0 |
| community/performance-driver/src/main/scala/com/digitalasset/canton/performance/elements/dvp/DvpPrettyInstances.scala | 1331 | `edf54db6c4e36c022dd0d3e8133da5d2375fef41ded9e47bf0c59e3386dd1340` | 0 |
| community/performance-driver/src/main/scala/com/digitalasset/canton/performance/elements/dvp/IssuerDriver.scala | 5261 | `2aed673c2a9b21379069b570862b96eae20e767eaf213372117156a160c46f64` | 0 |
| community/performance-driver/src/main/scala/com/digitalasset/canton/performance/elements/dvp/TraderDriver.scala | 29147 | `3b58e5695cc35c11a176e69dd9bd4dacc9d38ed1a162bad882f3706b9f44a6c4` | 0 |
| community/performance-driver/src/main/scala/com/digitalasset/canton/performance/elements/transfer/TransferDriver.scala | 18826 | `68cc6f5ff5370a56a8871ad698df0a5da592be6b36a5520ec474cf28b5f65af5` | 0 |
| community/performance-driver/src/main/scala/com/digitalasset/canton/performance/elements/triparty/TriPartyPassiveDriver.scala | 1949 | `c49a23b5a72869e7798b3e1daf3df41d26745e74c61967014e6e3a7906704c6e` | 0 |
| community/performance-driver/src/main/scala/com/digitalasset/canton/performance/elements/triparty/TriPartyUserDriver.scala | 16174 | `87d41f03b70366e327e84e602b313604fad79a8594cf7251b1cfcf38df4dd1c3` | 0 |
| community/performance-driver/src/main/scala/com/digitalasset/canton/performance/model/PackageID.scala | 259 | `4eee2b2df90554f5176400b03e229d96839afb70a3dc783348b1f2bf238727ec` | 0 |
| community/reference-sequencer-driver/src/main/protobuf/com/digitalasset/canton/synchronizer/sequencing/sequencer/reference/store/v1/reference_sequencer_block_events.proto | 662 | `0288e048bfa8c0e426e6e1b7efcf3a3d48c8babd877d2d15b69122de59684e11` | 0 |
| community/reference-sequencer-driver/src/main/scala/com/digitalasset/canton/synchronizer/sequencing/sequencer/reference/ReferenceSequencerDriver.scala | 11836 | `53b3fd6c3ca2c086a9e2a27f3816b13733738a567b5c1c8ea511d4a2c82ad68f` | 0 |
| community/reference-sequencer-driver/src/main/scala/com/digitalasset/canton/synchronizer/sequencing/sequencer/reference/ReferenceSequencerDriverFactory.scala | 5264 | `c5f5b7bac787b4443c92019f3a78e5b886ed8f20c7dc3b6d08d0e4d2ff29ef14` | 0 |
| community/reference-sequencer-driver/src/main/scala/com/digitalasset/canton/synchronizer/sequencing/sequencer/reference/store/DbReferenceBlockOrderingStore.scala | 9495 | `76f43a06402082821e7b0ad0b0946ef99be406be4ca2b722e1c547e09c788b99` | 0 |
| community/reference-sequencer-driver/src/main/scala/com/digitalasset/canton/synchronizer/sequencing/sequencer/reference/store/ReferenceBlockOrderingStore.scala | 5844 | `183e6913f5345c3839dbcdc2245c3afd7beac455467fbb3913b16290dec9b09f` | 0 |
| community/reference-sequencer-driver/src/main/scala/com/digitalasset/canton/synchronizer/sequencing/sequencer/reference/store/ReferenceSequencerDriverStore.scala | 1015 | `e410447aab59d40ca69010513f684ab3883f057d3ab3bc067a16db107fd853db` | 0 |
| community/sequencer-driver/src/main/scala/com/digitalasset/canton/synchronizer/block/BlockFormat.scala | 2296 | `c4df762851bcf49a0e30d61e1cf523b82d13d727ab27a58aa5d36056b781511a` | 0 |
| community/sequencer-driver/src/main/scala/com/digitalasset/canton/synchronizer/block/SequencerDriver.scala | 12554 | `e19f94fffd433903109d57f808de212181cb5ecf7750ad886cafbf4e7104b3a8` | 0 |
| community/sequencer-driver/src/main/scala/com/digitalasset/canton/synchronizer/block/TransactionSignature.scala | 573 | `3bd62237d6fc490ee4179355ef4a2bfe96c66be2702933ff6bb692f49e64d1da` | 0 |
| community/size-config-gen/src/main/scala/com/digitalasset/canton/sizeconfig/gen/SizeConfigGenerator.scala | 14363 | `2710b69b0c6c112610b6165b64ce5239501e83004df95e7efec5dde4afa4eae7` | 0 |
| community/synchronizer/src/main/protobuf/com/digitalasset/canton/mediator/admin/v30/mediator_administration_service.proto | 2221 | `053aa5010afcaa5e1177db43a87d5af725b550d343f356e23199073414bd3906` | 0 |
| community/synchronizer/src/main/protobuf/com/digitalasset/canton/mediator/admin/v30/mediator_initialization_service.proto | 1256 | `3922d2b2bfa85ff433bd8fc100cfa52d39fadb5729c09a3e492feeaba354699c` | 0 |
| community/synchronizer/src/main/protobuf/com/digitalasset/canton/mediator/admin/v30/mediator_inspection_service.proto | 3245 | `a0e4c5e9b26ec49189ac521593da9b736481e103ed33cc4665c3180492e46734` | 0 |
| community/synchronizer/src/main/protobuf/com/digitalasset/canton/mediator/admin/v30/sequencer_connection_service.proto | 1280 | `2744d1e70495cc90239d4da42150ab1914c23241c91e7e3d1ed72eddd882c390` | 0 |
| community/synchronizer/src/main/protobuf/com/digitalasset/canton/mediator/scalapb/package.proto | 358 | `30e64bb1a1180d7b424c021c9c630c67cc357ce0e01630714a7abc69b54a2bc8` | 0 |
| community/synchronizer/src/main/protobuf/com/digitalasset/canton/sequencer/admin/v30/sequencer_administration_service.proto | 9264 | `1aa1b41f50dd3d3993b10c4538d3842345a938058fcb83720e221dab6a00ad37` | 0 |
| community/synchronizer/src/main/protobuf/com/digitalasset/canton/sequencer/admin/v30/sequencer_bft_additional_snapshot_info.proto | 2185 | `d6070c98d575086779081b4fb5ff663bb012f1b4854a4e3d10fad00d1718f83e` | 0 |
| community/synchronizer/src/main/protobuf/com/digitalasset/canton/sequencer/admin/v30/sequencer_bft_administration_service.proto | 5549 | `3b760c2f6a381f854f653eebccabfa61b4b35adf698d48b771502e723515c151` | 0 |
| community/synchronizer/src/main/protobuf/com/digitalasset/canton/sequencer/admin/v30/sequencer_bft_pruning_administration_service.proto | 3173 | `2946624d34a51a06e0268f099d2e2a574ffd6a22c94bb253ea41b241b34d111e` | 0 |
| community/synchronizer/src/main/protobuf/com/digitalasset/canton/sequencer/admin/v30/sequencer_initialization_service.proto | 4787 | `5d385be27ce271bf823e3748c479c44cffb484238bf9d03c7703ed4bbec562ab` | 0 |
| community/synchronizer/src/main/protobuf/com/digitalasset/canton/sequencer/admin/v30/sequencer_initialization_snapshot.proto | 2917 | `7aed7424b86663572240dd17f9a328d8905954c70c05b078de5e026b191342b8` | 0 |
| community/synchronizer/src/main/protobuf/com/digitalasset/canton/sequencer/admin/v30/sequencer_pruning_administration_service.proto | 2126 | `e51a5382bada180204c95e592ba74782808afd08fdc0f803e883931fdadf9561` | 0 |
| community/synchronizer/src/main/protobuf/com/digitalasset/canton/sequencer/admin/v30/sequencer_traffic_inspection_service.proto | 1688 | `5a30020eb467331fa6f84fb2c5199dd93bb5dcd9b0a2cf27bf28b83aa51f5efc` | 0 |
| community/synchronizer/src/main/protobuf/com/digitalasset/canton/sequencer/admin/v31/sequencer_administration_service.proto | 782 | `33592be1c8377baa74386b5b23d980518219f9d227e6f7e5db82c5a9e7cc28b2` | 0 |
| community/synchronizer/src/main/protobuf/com/digitalasset/canton/sequencer/admin/v31/sequencer_initialization_snapshot.proto | 2533 | `39bb496e189d916ecb6c88abbc2039141b84a2de9ca7e94a257b9a221723be6d` | 0 |
| community/synchronizer/src/main/protobuf/com/digitalasset/canton/sequencer/scalapb/package.proto | 359 | `2a1c82f1429b0dfcb0788b46cf31ffe6f41f2d123a8927986fbec547f67abc51` | 0 |
| community/synchronizer/src/main/protobuf/com/digitalasset/canton/synchronizer/protocol/v30/aggregation.proto | 628 | `ccedb246a275df821472fd6851ce808f5346e7c893fbb6bad7b0bca02f3208f5` | 0 |
| community/synchronizer/src/main/protobuf/com/digitalasset/canton/synchronizer/scalapb/package.proto | 362 | `94b5461cfce1da66f934f011891225ad1ccd1bd3476c8955188fe4751fc50465` | 0 |
| community/synchronizer/src/main/protobuf/com/digitalasset/canton/synchronizer/sequencing/sequencer/bftordering/standalone/v1/standalone_bft_ordering_service.proto | 749 | `24359448fafbfea358f6fe762189195d46d297a6f8d8488b7a76cbc14c6a1fd3` | 0 |
| community/synchronizer/src/main/protobuf/com/digitalasset/canton/synchronizer/sequencing/sequencer/bftordering/v30/bft_ordering_service.proto | 8103 | `925b5716866fd26f6302292e5f19d5d1dd8a19b73630674fa4c490e06f677e6b` | 0 |
| community/synchronizer/src/main/protobuf/com/digitalasset/canton/synchronizer/sequencing/sequencer/bftordering/v31/bft_ordering_sequencing_parameters.proto | 1903 | `e76b3c49f18e3b54b0dae42cd08ed7f43a674398fc069b059315e60d997490fb` | 0 |
| community/synchronizer/src/main/protobuf/com/digitalasset/canton/synchronizer/sequencing/sequencer/bftordering/v31/bft_ordering_service.proto | 800 | `b80c034ae21ea3ead531a2bc26218494f436e1487b33e73fccf25decdfba547e` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/LsuSequencingTestMessageHandler.scala | 4629 | `e7b193f2fbd695a47f0aed85ea4195ee7c2fefc28b3f341efa13d182032e36cc` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/SynchronizerErrors.scala | 1738 | `bb1c86d4a8af8e09357944962f10c8b83efd3c8fa6e140340fd1b3208f029139` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/block/BlockSequencerStateManager.scala | 40936 | `66b97c730e584663bb8a225d523382e744c9a7cb019813236ce6f47826c34d7b` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/block/LedgerBlockEvent.scala | 5004 | `664f31efdbd8f2931e2b72d38ed72a3361ea21af060aa9f6659c1999cb9cee0d` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/block/data/BlockEphemeralState.scala | 4261 | `cb9223123470cd920575bb38017f0ed50d2e37ab9a2bfb81fa7f04697606a97f` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/block/data/SequencerBlockStore.scala | 7972 | `df5f654cb9a6e3740d31074492fc99d38fce4c30d78d85377c34818c9d5529f3` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/block/data/db/DbSequencerBlockStore.scala | 6696 | `26127ea52245d9a9d466195ef141a80b10a80750b89c2d1e78963955080094fc` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/block/data/memory/InMemorySequencerBlockStore.scala | 5533 | `7ba36b2893c223776fb1ae26317647cf29620a12302aec81e309e3e146166712` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/block/package.scala | 404 | `6d4987438513aca657b4947e8fe8cab5a3db6ff7719005e55e2d357ab589ae1f` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/block/update/BlockChunkProcessor.scala | 35947 | `f2dda3a4094b6c0060087773fd7f3000306231f06fc0c375e9f12dc116b67df5` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/block/update/BlockReorderer.scala | 4538 | `f534dc4dbd6cbd914e5494205a6190f1000c006930357372720025978b9e8415` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/block/update/BlockUpdate.scala | 3490 | `f9899fa99210e56fc9d9da88e3bac812b1dda0b48b4b32ff2521ebce67c1bcf1` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/block/update/BlockUpdateGenerator.scala | 24137 | `5d6e6c3f13113c70dc0cead8fc525b1af560b0824864957e7158321001dc48cd` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/block/update/InFlightAggregationHandler.scala | 16472 | `47f171f13588d893c72f372ee371f4b6e492875b46574e02d7419bfacaa27e32` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/block/update/SequencedSubmissionsValidator.scala | 15528 | `7c63de40a262023ecb131677d6e1e0cbdcc2c5d647e369139b527b8ce636d96f` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/block/update/SubmissionRequestValidator.scala | 24372 | `bca0a67f2f98aa50487c1f709313ee83724398e2d2ab86adba4ac83302638710` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/block/update/TrafficControlValidator.scala | 13662 | `45c88060030f8992e73d56b7f80931155ae953ee2f8fe5a10deb267407ecff32` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/config/DeclarativeSequencerConfig.scala | 1412 | `61983bd445c60939f48b7c156c867016103e0cd994b5ad01c852750c82788d09` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/config/PublicServerConfig.scala | 5145 | `fad68bb512cd7cb3a38796603a3583c91cc338cbe932ddfef68c7da510d1795e` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/config/SynchronizerParametersConfig.scala | 8490 | `6fd2c66a204f0bfdfeef7dd6a89d4df1e2dbca65461cd3b8e2a3982ec5b08b5b` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/config/store/BaseNodeSettingsStore.scala | 2957 | `278fd5d84a726038832a3fd4d3400b08db1c3ff8ffa633acf835a02bbaf65561` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/mediator/ConfirmationRequestAndResponseProcessor.scala | 42315 | `de871ab785b1b6892c3da763e5651aa799ba99ce573c9cda51bc3877e4704758` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/mediator/FinalizedResponse.scala | 2614 | `a29e77685fe5a8fbaf09ee78958dfc61854acc96159ac5c909b3a4f2fd3a64d8` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/mediator/Mediator.scala | 21845 | `eed90b325f67c1f0f2dfaf4f50df2682861fa42c8d9880cfc688c793a14ee7f9` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/mediator/MediatorConfig.scala | 1840 | `01dfe64dfaa86d802423f40e7071f045d2b131fd41416a1f265a69be4a1ca02d` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/mediator/MediatorEvent.scala | 3008 | `fdcb4ba67b37dcb77b7d42304a4a71529f7222bbde0928a5f06d57c324439be4` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/mediator/MediatorEventDeduplicator.scala | 8374 | `62491df3f9eb7f96baca1f00671c7536a5a1bc24a0c039a5d84611875084885a` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/mediator/MediatorEventsProcessor.scala | 8312 | `f548b7c9382cd1d701076a38c6e8836d65dd564e880800fbc518f5f6c7e6bfb6` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/mediator/MediatorNode.scala | 34950 | `3f6b12d49e6233a49cf79a6b064b4a34757eebf514615578828da1b25ca174f7` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/mediator/MediatorNodeBootstrapFactory.scala | 2626 | `9d45131592e0bfe8653d0ac18869f3ca4df08c24f689ed3f8d1f672e0b6126f2` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/mediator/MediatorPruningScheduler.scala | 3720 | `fa041261517881f9f4a495ede34efa80e5593293bb82b4fd4ec90ca1e0305694` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/mediator/MediatorReplicaManager.scala | 7789 | `6e2b7d3be9207c5b7f043b1d7c5ff05ba479e0c5ed60ab35eb98e1582f0c785b` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/mediator/MediatorRuntimeFactory.scala | 7651 | `68aa0eaae856a5c1db2b476d9b2d26b927dbe45b84e88ad5c9ac119be2bf12c5` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/mediator/MediatorStateInspection.scala | 1144 | `d1c1282a78efa5185ba795d01ed5b31d21526d5c366fc8e1103f67e7b8b7340b` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/mediator/MediatorVerdict.scala | 3182 | `0c08761fd9f93f26b970af356d0bb6dbeaa58ecc5873c8260fd8333915b56a1a` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/mediator/ResponseAggregation.scala | 26427 | `a0db73eb4eb5a1486f76169e32fd0e9f9d507f39f915f1e890f72b86ccd02f57` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/mediator/ResponseAggregator.scala | 11317 | `2fd07e38f680674d9d400c4fde0301e2dd93784f4f333ed32a4f3b1963fbe4ec` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/mediator/VerdictSender.scala | 21268 | `bdc51ff6d6548ea4059c25cdc3e365478e756c620066bac47a1c84fbfb730de5` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/mediator/admin/data/MediatorNodeStatus.scala | 1937 | `9804b0580c9ad8060684fe527682c3e571ec110deff768a6ac7ccf53126d5459` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/mediator/admin/gprc/InitializeMediatorRequest.scala | 1859 | `66b13c6ba13519fd159d319ca6db36f0601ceedceca3e416d715ea9b14d8b790` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/mediator/admin/gprc/InitializeMediatorResponse.scala | 720 | `a690e4304d93fa31bdc5279de5b1117c5a62a81bf1ed419a72278a211b79e2fb` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/mediator/service/GrpcMediatorAdministrationService.scala | 3988 | `e7fcb8c7ad1668ba2b6bf3b3b923bca423cc7705c3e9c69caefea19a22dcc609` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/mediator/service/GrpcMediatorInitializationService.scala | 2714 | `f6b1e9a7fe323c0d3c6d2bd988a02b6aa08262e2cb422b119f9a05ae818a51bb` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/mediator/service/GrpcMediatorInspectionService.scala | 16212 | `79519bd57693787cf5254e380988d880acb93f0d6b2db461f1e582890ddf18f9` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/mediator/service/GrpcMediatorStatusService.scala | 1692 | `1b8316e5dcab0203aaae6be2af23eb8879092ff535468e752b0461404a2ec599` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/mediator/store/DbMediatorSynchronizerConfigurationStore.scala | 5485 | `cf70c3f3988fe141e8f9e91c20c5c4292c2609d3dce7e81159f3aebf93c0c594` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/mediator/store/FinalizedResponseStore.scala | 19206 | `3c7e8516804ac3bc9dcd39ffb8e71c55996005de02fb2dd4287418ecc7b8066a` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/mediator/store/InMemoryMediatorSynchronizerConfigurationStore.scala | 1541 | `36062369f7439174b426d648af114812f208ee2949bb7d4784fe1b768a648582` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/mediator/store/MediatorDeduplicationStore.scala | 14652 | `f5901158b3e6117d030ab44bb0807454c49583ce0c4bc32497cd77a8a638f473` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/mediator/store/MediatorState.scala | 10275 | `9ebd18682fdcd785d8ecf5b4a8656127993e785a814edea07cba6b29a97b2f5b` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/mediator/store/MediatorStateInitialization.scala | 2753 | `830e8ba1dce72742b711275305bc18dfe3ecaf36546ca666284332f2ccf2b56e` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/mediator/store/MediatorSynchronizerConfigurationStore.scala | 1968 | `5157c6ae392d99eda3c7e1860e4abd89b2ee39bb2b6adabbe1bb3f124079ae3f` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/metrics/BftOrderingMetrics.scala | 74760 | `ce6c2d4a7598d2c2a13fed569109197b867e6633057ef1830375d093809d5818` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/metrics/BlockMetrics.scala | 5351 | `b801a217542d710f3e1b1215c27cc12b97905de276f88fd6e522867aac35fa65` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/metrics/CircuitBreakerMetrics.scala | 2137 | `f846793dfa769748c3d8836a23b18516dd0ef25d0d111858c822365ba55b2b3f` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/metrics/DatabaseSequencerMetrics.scala | 1617 | `1fc4aafca55d5381240a19f887d570ea7b5dec8ee19246628ff7d734a447943c` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/metrics/SynchronizerMetrics.scala | 23673 | `f9ee9e8658efe6feb2fa001c2abc68f88df830ee11eafe74a043efadfffa3663` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/metrics/ThroughputCapMetrics.scala | 3033 | `a2c97c56326b37034fab18962025fd445aca982acbcf7a25e13929a55715672d` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/AnnouncedLsu.scala | 3061 | `4f2f17600fcbb0921997a7a421b94e48d6cd56003deea0c9aff544dc81c1ff9d` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/AuthenticationServices.scala | 886 | `1459612e3a512561860f1d680555f699cb62133ef8ef7f6c8066ab9c0105df24` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/BaseSequencer.scala | 8220 | `fb3388ce207ff5b9a79ef5427a9ad9809146cb944575259475ccc5fd74e3ed7b` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/DatabaseSequencer.scala | 23673 | `e41496b9c08504235a45bc01c6b8c330c1b7b6d38ec91f5d877e448102e53022` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/DatabaseSequencerFactory.scala | 2286 | `2fe3763580ab8df70f6477e962909d6d2c76c7ee3f32e7e28c06cdf07ba66af1` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/DatabaseSequencerIntegration.scala | 4450 | `a033fac64cd72b2718d1940a5f2e6d57ceccd41495a2d81d5fddb9ebbce1307c` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/DatabaseSequencerPruningScheduler.scala | 5217 | `9dbc0aa1a08a308b7dac0eb397cc476c30cfa486e47b54befea8ff4461561c97` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/DirectSequencerConnection.scala | 10299 | `7d5e11be242efa8c7f2ae1d826b237f8862994330aee4325c09178b4aa458348` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/DirectSequencerConnectionPool.scala | 5975 | `9e6d505c6196af907022eed9c93c484e52822ff60d49484131f3e61479b302d3` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/FetchLatestEventsFlow.scala | 2453 | `05b1df529d1ff95f4fcefe631b43fd84a97f810606e690aac5b60f00fd7b5fbb` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/HADatabaseSequencerFactory.scala | 6873 | `bcbeae7b82d51524c0f1b13d316b85b3aab603f705464675c79adc3578cd159a` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/HASequencerExclusiveStorageBuilder.scala | 5663 | `81b0db2b62f778de2c81071957d758dbdc8ac2ba032d78945cc9482278e6272f` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/HASequencerExclusiveStorageNotifier.scala | 2616 | `e33f9ce30411553c573110f0eb20678b37dd56edbc03fca9af802100cb32e354` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/HASequencerWriterStoreFactory.scala | 9113 | `0c488d294126c5faeaa5190dfb237004daf28d72c4490f2bd886d4b28d159761` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/InFlightAggregation.scala | 12601 | `57feca6498a9373c65d950cd1c1ad0855857147c6198895329ffbe6d7906c4d0` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/InFlightAggregationUpdate.scala | 2193 | `628e8053dd499f53c5f5f450874af75923072237188678e500564938fb63ea88` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/OnboardingStateForSequencerV2.scala | 5249 | `2b8ff25382c0d39e1140b0ef293810a1cc869e32278273657179a6935fcf5a75` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/PartitionedTimestampGenerator.scala | 1414 | `50db0f09ba236a36b0deda639ca1124020dd5a2f4f7e9134902b24a4b6fe8430` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/Sequencer.scala | 18287 | `6112e3c1896276333d7f02ca9667739390f8ebc4e2564cb95cce0bc4af9f7794` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/SequencerConfig.scala | 15098 | `4f250336c56e4c7b370696007f09e39a0a17e6df7ecedee40a7b5df046ca77b2` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/SequencerFactory.scala | 7327 | `37084b69488062eead01b2190f1f21e0b45f9627b913381ca55e9a0148895ec4` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/SequencerNode.scala | 47211 | `20db35db5b2ed9b85307bb51c07eb3f54280a6f8ceddba4510fa7dddb0809253` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/SequencerNodeBootstrapFactory.scala | 3409 | `ca3f993985ed2eed3fb404919b1df9ffc3048643f298ed78f2a8115d1479a5f0` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/SequencerPruningStatus.scala | 11311 | `05c49d7f3fc4e6ed27edd229aeecc8b23971b1b6e77368bae86143269dd195cf` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/SequencerReader.scala | 41850 | `9376d4e1fe13ce272695f89a60b7ee3596bcfa86be323e28cb4f2e4845f83a90` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/SequencerRuntime.scala | 18000 | `f92bf4e797ac027384666ab62ce60a4fd637827aa64c0632a5ccd757daca0e4a` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/SequencerSnapshot.scala | 17690 | `fcdfc5e2eaa1e4f7840ec17bb240b8f539098d3cd5170fdf9b0ed9fc556528b4` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/SequencerUtils.scala | 3507 | `acf2f02f95b103fa20be2c2da95ea0944b6441414c57acd6c408984d7ed7a9bb` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/SequencerWriter.scala | 26011 | `dbd2483426e41fc566e6d35c2cb8eef4e18207fd8483b69bcbaea1fe0d039cc8` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/SequencerWriterConfig.scala | 8663 | `1ff50c74db1df2da90772b9f525d0e26bde5ff854fc6b215f9fbba2344a45362` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/SequencerWriterSource.scala | 35601 | `73ccdaaa54a6dda834750776ea5034ae679463e048f95abe331f6725b6856270` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/SignatureVerifier.scala | 5837 | `bd62576e72ea2e6fcda50780e15eea1d3b52ba7e7c6fd7bf6ce8e7e4544f2540` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/SubmissionOutcome.scala | 7472 | `9543729d020c7b0a1f1c75e7874aec81c00ee0c23ddb5bd6c7129c11420857be` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/WriteNotification.scala | 1221 | `ff2efe68695ca6d130e03d1f481c5d54e853523cacd9237ec8b318c34500e5f7` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/WriterStartupError.scala | 3944 | `796e9186fbcf72b0feab839eccc461a1fdec6762503b7c942c32dbde475896cd` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/admin/data/SequencerNodeStatus.scala | 6286 | `4abbeeb13302e89ab3cc7ba327c7fc80d9a7e70dd6a83967c24078474918cfdd` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/admin/grpc/InitializeSequencerRequest.scala | 674 | `d9d3137353c14df0ee87a51fd997df8c6ef4ad32e4a2914af283639b83ebe6c2` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/admin/grpc/InitializeSequencerResponse.scala | 272 | `29dae7738294e9da51e1a533a077e6d2585164a69e90787b6d8d680742c846ab` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/BlockOrderer.scala | 5789 | `667dddd522037940cee30df71e79ab53d83e1541b3dd2863e124bc70f2c824b8` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/BlockSequencer.scala | 71048 | `45cd1dd268ea044bd47a4258b39959e4a66febf280f7d3a2183bfd6a32a4bc95` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/BlockSequencerCircuitBreaker.scala | 10099 | `354e0650bb5aaed2a3d7d18474f5f5bf173b98fe5894d9986f4d08d10643418c` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/BlockSequencerFactory.scala | 11489 | `515c250cb3ac9ed46fcb6960c7643692733760f9f00faf5d575cca46e8a013f3` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/BlockSequencerThroughputCap.scala | 24614 | `c84449913929e590b20e9827438a9d3518039e91f05e1c1dad09053147e7f51a` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/DriverBlockOrderer.scala | 3360 | `99a859f65e5fb9cde8a27d482d19cecdf884899c48e0e5a09ca9340ef9b89113` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/DriverBlockSequencerFactory.scala | 5916 | `5fd18610cf245eacced68ad9ee0f42d73d48ac14d3979e9118b5b039596999ad` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/admin/BftOrderingSequencerAdminService.scala | 7319 | `869287968619c757be72edc45846d3df7039d3c74c45036a3ad78c5e0d56d3f1` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/admin/GrpcBftOrderingSequencerPruningAdminService.scala | 4157 | `645b1ccfd81294ea081265793a5eeaca210af2059ef54f04f237edc27576ecc0` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/admin/SequencerBftAdminData.scala | 19320 | `01d2a966808030a239ad7570b961d152cbb62210b8e8b4c03666297e93ee739c` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/bindings/canton/crypto/CantonCryptoProvider.scala | 4239 | `f4c047e776f054b5941cab48be84f015ccf2fbd1971e1ce66d0509f8ba8d6fa4` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/bindings/canton/crypto/FingerprintKeyId.scala | 533 | `ed44431abf372a7656eb344bf3fc5ad6173da2528e6c83fb35d2db110536fba1` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/bindings/canton/sequencing/BftBlockOrderer.scala | 43525 | `9aa5a5f8825c04c1cb43db34ae23b25e7f2fb4b59b39a4ff4dc50d1ac70e3a6b` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/bindings/canton/sequencing/BftSequencerFactory.scala | 5792 | `4761f3c626509a9c7e71fdc72b3d01e99a03a1aca5ff0584747da931707075be` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/bindings/canton/topology/CantonOrderingTopologyProvider.scala | 12982 | `723b7141aa3f3c20a4d36542c6ed1fb4a3ea0441d4adb26ced5d53053f7e4d2b` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/bindings/canton/topology/SequencerNodeId.scala | 776 | `0017fd9fa525cb9aaba9ad9f3e4132aa11bbffbf60bd311797a1e46ec7720af5` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/bindings/p2p/grpc/P2PGrpcBftOrderingService.scala | 2826 | `14f10f9695abe6400df32876e5ecc1e4266eda23200ef687ae1ba3cb0bc3aa34` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/bindings/p2p/grpc/P2PGrpcConnectionManager.scala | 100601 | `61cfc4f5cbeecda6013077f4f56a92f316b4b14a1e982c49038dfc6e900208be` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/bindings/p2p/grpc/P2PGrpcConnectionState.scala | 46105 | `c8d11a0fb0ad66e9c08be52675d03854c951b7a2cf94478a94d6d9a690ed2732` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/bindings/p2p/grpc/P2PGrpcNetworking.scala | 7219 | `b7150d8cb36f915f6d41716c726845b5345991b2a63d51afe3e3a9d5fd924646` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/bindings/p2p/grpc/P2PGrpcServerManager.scala | 2234 | `2794b6bd0139725425a2dfa7db81acb8bc711eb56931d270de9e10300ba641df` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/bindings/p2p/grpc/P2PGrpcStreamingReceiver.scala | 17451 | `ef329f3b62fb7341a7f3b24179fa411c682904338ea4551987f0a03a44b0ad73` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/bindings/p2p/grpc/PekkoP2PGrpcNetworking.scala | 29402 | `7620dd0669144afc52e868bbbbe0e28053a654aac71f76df9731cd50b6c2a77e` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/bindings/p2p/grpc/authentication/P2PAddAuthTokenHeaderGrpcServerInterceptor.scala | 11463 | `1a37fc6ef5729387534809e1bd54d1066bec717da1fc4c2e2703474ff388a24a` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/bindings/p2p/grpc/authentication/P2PAddEndpointHeaderGrpcClientInterceptor.scala | 2622 | `a63349f8a29a42eb3213e518489604c935a074d03e5f1675960e8e2afc85eb6c` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/bindings/p2p/grpc/authentication/P2PCheckAuthenticationGrpcClientInterceptor.scala | 5408 | `becec0ebd1e0ec620bd123a50f68cfbbb5603f58170fb24241ceafa4d733cec3` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/bindings/p2p/grpc/standalone/P2PGrpcStandaloneBftOrderingService.scala | 3088 | `713167a9688587845f061189fbb9b4a22f27ce5d9f2e548d94489de4ab28913f` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/bindings/p2p/grpc/transport/P2PGrpcTransportStatsReader.scala | 14060 | `7c5e01de0acd1eed29a48098247fa7ad2064a18bf5b19e9257a68a8427b0c143` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/bindings/p2p/grpc/transport/P2PNettyChannelInstrumentation.scala | 9096 | `d65de0344854d047373a5c6deee29b1dab4985d7b7db495710f275ab0c7107c0` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/bindings/p2p/grpc/transport/P2PNettyEpollInstrumentation.scala | 7633 | `277dcd190786ecff24fe4d8bd43a1dfe410a341e53e47ad1fea088c26bcbd690` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/bindings/p2p/grpc/transport/P2PNettyServerInstrumentation.scala | 2173 | `334f74d97feea76ce7b7389d33a7824850bc475dd2fd312048430213d5d1402f` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/bindings/p2p/grpc/transport/P2PTransportMetricsPublisher.scala | 20782 | `1873b0bbafdd9b81f2302fc27f709434a6252ae67aebda9e087b518a66b1faec` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/bindings/p2p/grpc/transport/P2PTransportMetricsServerInterceptor.scala | 1668 | `0dec83c54c66cf98b02794acf97bbbcc10aacb5acc91cd870ef695a1f9a8c464` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/bindings/pekko/CloseableActorSystem.scala | 1051 | `673d01d1e506256c8348ef1bd9e109b5d23cc58bc526a417b6a5a515e6e6a386` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/bindings/pekko/PekkoModuleSystem.scala | 24353 | `1cea289b1d3a9135e5c801d6abe5e293e8a573044307075d646f8b15a6431c24` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/bindings/standalone/crypto/FixedKeysCryptoProvider.scala | 4648 | `60bc8af0f9446cdf4d59db185685e6e1e5ee3818d8d46c6370b8ed66b6ecdf36` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/bindings/standalone/topology/StandaloneOrderingTopologyProvider.scala | 8335 | `4205168c358ab00af5fe5245e25c963d266f4103dac10bb1fe7fde1a16a7a609` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/BftBlockOrdererConfig.scala | 47693 | `2aceefa28688db9e5381e521bd877c5804bb717ba048cf0a673d736ecc7bbbc3` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/BftOrderingModuleSystemInitializer.scala | 24551 | `ff8eca86bf75417e1d1ee09993e50d20c63890c27882e506ea2cf6a5ac163bb9` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/integration/canton/SupportedVersions.scala | 1710 | `03e0ce86ccd1963ebe338a2b698aa9bac987f2c4046372613a52c48c8ec2abfa` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/integration/canton/crypto/CryptoProvider.scala | 6728 | `4c209464b795b9584d3c3d3e9c35059815d19ed63fe5f6a6792f6ac9f145c6dd` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/integration/canton/topology/OrderingTopologyProvider.scala | 2183 | `84ff74044260c3bdbcce899c6659c6a6976673e1f4627aadb7a233628c9dfc82` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/integration/canton/topology/TopologyActivationTime.scala | 1414 | `3271d4ae646fcb27a80e874ea6c74b2c7bcccfce09e10bdbf1b7bedec7f0fa60` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/HasDelayedInit.scala | 2181 | `788ebb208c5ddb1a36debae7a0a64ff7dcdce99f80d7053b735508f5615684e1` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/PeanoQueue.scala | 1661 | `d17218a523d6b098bc8768ae869945cd7c700a4be341fe5b1556bfd9d09a44d0` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/availability/AvailabilityModule.scala | 87125 | `413f2cd8a7e2299719ba83f1a6094da031544d47713e936b8448f712a983a3d3` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/availability/AvailabilityModuleMetrics.scala | 3874 | `808898e3f2c5e946da010ba48bd3f839a126f81bb77393db6efe0ac7a73ef1a2` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/availability/AvailabilityModuleSpanManager.scala | 2701 | `dfe87f6c98aa9ea669f43d6fe649a29c5a9618d1a3e861a4bac01ff412b8fe5d` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/availability/BatchDisseminationNodeQuotaTracker.scala | 3927 | `387c25c14e4d6a1c19714d18e76e94ccd791e824fef996e9c9003629c5802a50` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/availability/DisseminationProtocolState.scala | 2235 | `281562824607810edc6412b6a4797d7eebaa5c6aff3e53cb16021b4b1dd67587` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/availability/OutputFetchProtocolState.scala | 4884 | `e7f328f6721dcaff1ff69a9386f8456d56c2b8cdecddc02999f7f17dc308a4bb` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/availability/data/AvailabilityStore.scala | 3959 | `f1500abe923457711e50d7af4527e526bb18b3956ebd65de77fe5678c3666fe9` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/availability/data/db/DbAvailabilityStore.scala | 14834 | `32ebd07cf02a3d6381b485505f24ffd21bf2fe873418ee01c6f740e60d7c2e34` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/availability/data/memory/InMemoryAvailabilityStore.scala | 4537 | `e4b82dabc6ceb72f1e481510ec80997fb243eaad8b827c26bde926d2352c630e` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/consensus/iss/BftNodeRateLimiter.scala | 1500 | `8fcd7df09f90ce1e50b2fb18ee5cbba2e010366a0f6d274a94469ce795b3f544` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/consensus/iss/BlockedProgressDetector.scala | 3766 | `6a8477a57b7437b25e77ad53dec306106c551944d07d8cee0b027c416e41b018` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/consensus/iss/BootstrapDetector.scala | 3518 | `61cfa2bdd5ca1b2257a29dad03fb306446ef4069e83236ef10bb9c7498b3cb7c` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/consensus/iss/EpochMetricsAccumulator.scala | 2418 | `4c8e22f3fff299cb015aedb769989c674eea035c91ebc4ed0b10eda9ad7484ae` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/consensus/iss/EpochState.scala | 14196 | `1f1076b9196abb91c4d7c97768dff7698441fcf534e410b7870ea065a813b8e6` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/consensus/iss/IssConsensusModule.scala | 53261 | `daf4ce31a0e0e191cc2a5c86c5ed3e67ec76ba62bd60a2cc62a378fd183e7361` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/consensus/iss/IssConsensusModuleMetrics.scala | 4576 | `b43d620b147b2ad00619b4c19b3de6f284e0ef8211ebb3930dd88748c8fdc8fd` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/consensus/iss/IssSegmentModule.scala | 48629 | `5419e26024c8b28262326225aa9244757ded43e6eca6b4a38100d4c41ccebd61` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/consensus/iss/OriginalLeaderSegmentState.scala | 9831 | `bcbbba2b0d20db5cc128637f1069a7e7ac42dc35ea6ae776db66e43f0c220e52` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/consensus/iss/PbftBlockState.scala | 22064 | `f99311cef37ccd8abc653556b4e2aa04b81c3079eb3bc51ebfde75b9873895e8` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/consensus/iss/PbftViewChangeState.scala | 10283 | `84ad0e6fe44d949add08215f6e264aaf5bb9c086fa7fbc6001cd334efe7e1ae5` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/consensus/iss/PreIssConsensusModule.scala | 9400 | `effb83e3bdb05a8b30b3693ceb129586393540b0e80d145905573427ad8be51c` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/consensus/iss/PrePrepareStoreCoordinator.scala | 5002 | `a8e9409b73707a8ac4415239b43a51bbe616e4141fbf8b2e02b1382e37087636` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/consensus/iss/SegmentBlockState.scala | 6775 | `d24a0142f261d43a3f83a9aecf2f91d2ed1d3c5752659331a3993b66f896eb67` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/consensus/iss/SegmentClosingBehaviour.scala | 4003 | `c989382bcca9b05a47c4935e8dfa744666e01659ed75d1269f8edca416fba5c3` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/consensus/iss/SegmentInProgress.scala | 8397 | `7ae1036f89ccc1492b6f97d9bd4b1232a7a9351aa91d92e80e486023cbd9cd74` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/consensus/iss/SegmentModuleRefFactory.scala | 4392 | `2af68b75d05ce602739dbac7b88ffe97f6510182da95caed8d984e46702e778c` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/consensus/iss/SegmentState.scala | 42627 | `70aaf17558a4391100e0de1b22fbba63847d5780ba4926fe1f5aa0a94e61727b` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/consensus/iss/TimeoutManager.scala | 4234 | `f6d190deb9c7d87edbf02f0c72058f2c8482ecc36431f585f52337f5adcb69b6` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/consensus/iss/data/Bootstrap.scala | 1504 | `d76c6e0807aa2ded868ef8f81d2e084819083d971dbdc926dcceaca18fb954eb` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/consensus/iss/data/EpochStore.scala | 7657 | `6c58129af03b567f204b7b9b3fcd8d1a7f2248aa3221fbeaf4d0230ce25e4d40` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/consensus/iss/data/EpochStoreReader.scala | 1643 | `37bd0269e73a26a33e8d7de5bba08f955347448cdf8b18ba1803ef60d82fae0f` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/consensus/iss/data/db/DbEpochStore.scala | 34919 | `cac1756ce90f641fbeff56bff7b7358bb7f1490eeb6e7060cd556011c8b32ed4` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/consensus/iss/data/memory/InMemoryEpochStore.scala | 19666 | `6b3e35d12234f6a51ada00c5926a4906c9916417d62d8f184779f4ec86946b57` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/consensus/iss/retransmissions/EpochStatusBuilder.scala | 1979 | `6da88622c067c8077e8123424580e9c9a8232b0e7dd88eea1af70f64fd9c3f80` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/consensus/iss/retransmissions/PreviousEpochsRetransmissionsTracker.scala | 3121 | `55fb9bcefeb8544752f64d6f0f5d5620a51cc216d713fc6ec7f0da0083ca8a89` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/consensus/iss/retransmissions/RetransmissionsManager.scala | 21564 | `abdf5fc6788ead4ea4d05b653198d850bf03dcc9e6b0010f0d1a2426e8c25937` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/consensus/iss/statetransfer/CatchupDetector.scala | 5559 | `a8c8d19ef021e9b85ef7595f96cf5bdb57c806dbe2f61812ac37165beef992b2` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/consensus/iss/statetransfer/StateTransferBehavior.scala | 27316 | `7f7e346df51bc55b35ddd2efe4f1c017f7323468ecf5df6e4d09acbe4121fc15` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/consensus/iss/statetransfer/StateTransferManager.scala | 25376 | `3104dbdc38ae2172fabe9548b2192477a7e15b8f38fc866c8dc86959420d673d` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/consensus/iss/statetransfer/StateTransferMessageSender.scala | 9763 | `a0232cadd635a8fe73de2e64900d8b9cc52d6d80f07280cc3460ceee03f0316e` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/consensus/iss/statetransfer/StateTransferMessageValidator.scala | 13509 | `cbea74acbb5131286059e3ce57847a33b7940e6d84172e5b86f5c0f303a28349` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/consensus/iss/validation/ConsensusCertificateValidator.scala | 5910 | `101acf2081ad2827221ecb3b9ddefa5194fa175cbd6ff3cb91dec275247ae8a3` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/consensus/iss/validation/IssConsensusSignatureVerifier.scala | 11126 | `255012ba00848833a1ec920253bb452a0bcc1ab42fdc629dec4d8ca475c53b73` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/consensus/iss/validation/PbftMessageValidatorImpl.scala | 15316 | `0ef98167c9814ec1cfc86e19892457eb6cb225fb2ee925d3b8b435ebee53af71` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/consensus/iss/validation/RetransmissionMessageValidator.scala | 8021 | `9c61b94672eeca445f06e454d517c2b67e61f4a67cc264f0995c7ce570f093bf` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/consensus/iss/validation/ViewChangeMessageValidator.scala | 8883 | `8a2e2d5354e01e46665c12fcbc1e008b3c7faec9e0862c01c6abf2f291951516` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/mempool/MempoolModule.scala | 10798 | `362703eeba29533b4cdcc3cc6454c2b230a4d9c96b5dc81f9f46c89b3a43e320` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/mempool/MempoolModuleConfig.scala | 454 | `7d0609bf5f1d98112240b27e6f7ad91d7de6635a16af39128f2323a624a0ea66` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/mempool/MempoolModuleMetrics.scala | 2117 | `6f1b0b05f7a7fbf99f4bc450fe9a5c06abc18e1872d93cdd4b1f400ee6d56cb3` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/mempool/MempoolState.scala | 3732 | `9b8689a69a6b1f1ac2b02ce5ace3a77fd9bb65b3b6e50b7473d59dac65a72eac` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/output/EpochChecker.scala | 821 | `519581ea729db7d780e5404824e0cc5bd9035b7041e0eaa83e27f96bc27a311e` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/output/OutputModule.scala | 86900 | `27cedac69a7e4836bd83dabc985c885f0929ddc82f57762023315192a01d4ef9` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/output/OutputModuleMetrics.scala | 3056 | `d0344dbae9dc8cbd0606be151a1d94d7648a6a30487a2f398d8b5788d15b97a7` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/output/OutputQueueInterleavingWaitTracker.scala | 18218 | `6ce72986251bfe4c000aca7d6b3ee5afbc78454176f41e53ef8c96a70c2b1196` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/output/PekkoBlockSubscription.scala | 15702 | `4e563417f5edbb69ca302324450e681aa706ce4eacba0260abea8421470a2567` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/output/data/OutputMetadataStore.scala | 7854 | `ee05ba163c07db7ad5ee918f0333ad27b9a32541a7cdd88243a02499bb50a0db` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/output/data/db/DbOutputMetadataStore.scala | 19359 | `9e625b6cb667cc99e99f8a42c1eb263178676e636aba29b35bf0af9ef1731489` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/output/data/memory/InMemoryOutputMetadataStore.scala | 10872 | `b342c76edb1c439c4ff2990af9ad97c57cfad815c03ca6b656f78cc8dcd99a50` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/output/leaders/BlacklistLeaderSelectionInitializer.scala | 5020 | `3eb4894dda2a37c7fdbb584bdb467ff96b642e795d8991e4c3b128d3c117f3b2` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/output/leaders/BlacklistLeaderSelectionPolicy.scala | 6794 | `30142eac63a4b4116d01a10432f6b7b19e28d44ea4deb8240917d01abf916893` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/output/leaders/BlacklistLeaderSelectionPolicyState.scala | 7524 | `1740dacc0a1059b02df7b57a60cfd4139fbc0914d23f2abed423c54b8b1efb39` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/output/leaders/BlacklistStatus.scala | 4447 | `8270b259fceae4e74ac33691f9d0d53b300d22c4ea32d1174a0cc3d02a26eae8` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/output/leaders/LeaderSelectionInitializer.scala | 2531 | `375ab6e295144fba90f98a139909abe6cb5f96174e481e9935969fbd73c142e5` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/output/leaders/LeaderSelectionPolicy.scala | 3055 | `cf97094e04e7dff6de95ea842f583672c39d71c0420e6c0862974f2121ef9f69` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/output/snapshot/SequencerSnapshotAdditionalInfoProvider.scala | 12753 | `3ca79e3bee71fbf7a2e43b2dbdebdbebde5c6758bbdea3fc47384ef09e5a59ac` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/output/time/BftTime.scala | 3314 | `6ee4c80e812a72edb5bff6eaba991d2cdf666d0cd00b607e56b415cb9ee8f8ea` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/p2p/P2PConnectionState.scala | 4986 | `1a34465907ca75d57ac07b5ceda38af1230417f54758825307e57ccf915ed294` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/p2p/P2PMetrics.scala | 5201 | `f086951d269126abdc4a9625c898746203c0da33d8b3700874498803ae3bc926` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/p2p/P2PNetworkInModule.scala | 7774 | `09c63cf1c7ed4f34e0a08f595df01fb7a5e8d96409139bac76f59faeff26498e` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/p2p/P2PNetworkOutModule.scala | 44482 | `30f3cf7ddd6915b1509cdba210847678912ee92e38ee0c49448fe0bca0df834e` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/p2p/data/P2PEndpointsStore.scala | 2960 | `d75e4bbbd2f9eee959800c58687bbf1f3b5f7e482270fdec9fb846a4c38ae3cc` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/p2p/data/db/DbP2PEndpointsStore.scala | 9385 | `de4303f940cceaddd8d221b219ac0e3e92ff314cf1e20e1e59d92fcb1951f110` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/p2p/data/memory/InMemoryP2PEndpointsStore.scala | 3880 | `4feacf2771dd4d841c59e870a8c22f009a3452c13bdb77b6f8c02ef240db8f97` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/package.scala | 637 | `12ed0990015d003adabcce06a5073a361ca4779f0069f4e8d6b3ced6b781f3a3` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/pruning/BftOrdererPruningSchedule.scala | 1366 | `d6d917c69a7f79b7f859e06a282d9f1be20be04d3348163d5e71a32500cff4b3` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/pruning/BftOrdererPruningScheduler.scala | 2952 | `cd1da05feb226d8a092b1f9907302aa9b6dfe7df1d82828765dd63c3458d8eab` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/pruning/BftPruningStatus.scala | 1021 | `62549e5a9dfe01fa1528bd70b03401fe8139ce207c31a6119dc34b88f7d27454` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/pruning/PartitionManager.scala | 29399 | `9452392c745561045a72669d13bdbecb4bd12842bac265cba26986e77fafeeb4` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/pruning/PruningModule.scala | 13930 | `c941bb26ffab3666b3f47670d01440a661acddf5f17754b39a4aa5d3f159a316` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/pruning/data/BftOrdererPruningSchedulerStore.scala | 2619 | `3294601c60d9d23710eb88aee9a0646641059b028a46a2c9eea3f8cdd6b5c80c` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/pruning/data/db/DbBftOrdererPruningSchedulerStore.scala | 6409 | `f8726ecb827c15eb0196523430858122617ab9b81e965d042936844f6414bf47` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/core/modules/pruning/data/memory/InMemoryBftOrdererPruningSchedulerStore.scala | 4877 | `1836747edd57566534c94c866c1846c6f67b3788d73d6feaf3566ba5b144fb96` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/framework/BlockSubscription.scala | 767 | `0c55101d5320ab6786395f759fc5e15fb8f8474f63d9f171ab782249539d1d98` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/framework/Module.scala | 21703 | `98a8f6a6f972cf30613682adc2ffa2ebc999492e051946c74a2b5e722c52d8d6` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/framework/OrderingModuleSystemInitializer.scala | 5105 | `098a2780202f89b53212d810c041707be4433ae220356a07832869584d386659` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/framework/PureFun.scala | 2455 | `8bc876e643495991f04f533851a919bbc80f8cfcb8918029a1af49fde515f2e0` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/framework/data/BftOrderingIdentifiers.scala | 2510 | `7699cbcfca21b7de5b0a8b980dc2b368ff9dbcf6bcbfc659f47ab35938ae0ab1` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/framework/data/CompleteBlockData.scala | 949 | `26b62e819dbc982533bc0ae9303671611a42d2d675b5ccb67afb81efe82d5c78` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/framework/data/OrderingRequest.scala | 7830 | `b7cd1b0be72e8aa8ae96cb669e3bd8bd5226dddf3897b998908f478dfd2f1add` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/framework/data/SignedMessage.scala | 5653 | `3134a35d5e10e076dc1b0a5439489cebbaf52816240721e51b0ac81540a7bd1b` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/framework/data/availability/AvailabilityAck.scala | 3362 | `8bc06f41c2181a76f476bd58d508409d2014ea21d85fc6e4e3c1c53213627403` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/framework/data/availability/BatchId.scala | 2308 | `6a5e512a86e322b4695eb3d327c8373fd6a0d242426586a635c6d07aabb484bd` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/framework/data/availability/DisseminationStatus.scala | 15612 | `2794dec8eb72709445c4b8c852e98997784ea891ae4786965b97f0f294505d21` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/framework/data/availability/OrderingBlock.scala | 982 | `043d5dcae2111b3c984cb516cbcf34b0ba10950451fda31d23634a944a787547` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/framework/data/availability/ProofOfAvailability.scala | 1222 | `176838b56537c99694b3c222e8f5e632f0f786d244e7b735e974584603f860aa` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/framework/data/bfttime/CanonicalCommitSet.scala | 3173 | `0f49abc0d48544f6addd353107efa8e462dde7fcb3427b464d54334701fc8f6c` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/framework/data/ordering/ConsensusCertificate.scala | 5492 | `daecfb2a6dfd9a2073e2086ce18e291e00f78f9c1170eca2c2f95e4b9bc20397` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/framework/data/ordering/OrderedBlock.scala | 733 | `ed13f2c6006accc3a086dd6dc5e8236c6ab47781efe2dfbad9276e5c4990a7ff` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/framework/data/ordering/OrderedBlockForOutput.scala | 1068 | `4fd6148a75352b095be16d5f77f3f3cbec31f9c7378f6b58b35944d2010bcbdd` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/framework/data/ordering/OrderingMode.scala | 652 | `ed66a64314e4b8c31cd1b0bfd1660f4be473cb9ec301e7c02128d115c40c178f` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/framework/data/ordering/iss/BlockMetadata.scala | 1407 | `c36c36cd2463e6fae905ebf8f588e4f5e2cb254692a17f717a26303a47567840` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/framework/data/ordering/iss/EpochInfo.scala | 2438 | `a6761709ffaf6781239e60d2c3dd355bd739b1baea5c71bb3d21828b636290df` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/framework/data/snapshot/SequencerSnapshotAdditionalInfo.scala | 4934 | `c6e6889a2a704fada5caee6829ae7335c97d420297465dd652a0f9f8db8db581` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/framework/data/topology/BlacklistLeaderSelectionPolicyConfig.scala | 11916 | `fc674aab389148fc50eac0331ea91fb90eee1314378a4f21d0dcf2b7bd4bc038` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/framework/data/topology/Membership.scala | 3141 | `8a882a3bdeeecfbe5c7abfc3d7582f3abfa49ec795486ebe14c94fdab5d827f8` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/framework/data/topology/MessageAuthorizer.scala | 467 | `e32fcfe7c24bcc8ecd68b297c69b3743c8eee484df6e9ae9524c46ed23685fe4` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/framework/data/topology/OrderingTopology.scala | 7245 | `33910f346521a0cd2e2f86b51aab5d70170c517fd53aae6061bf5efbe8eca921` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/framework/data/topology/OrderingTopologyInfo.scala | 2025 | `bb64b67c76a46a78efc020054378eb731575957e15dae450a49fa6dde2e3cf92` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/framework/data/topology/SequencingParameters.scala | 14778 | `7498c9e94af0b0703541f4ae480685dd5a6fb46d0c6c1ead5f1d50b2a96c6165` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/framework/modules/Availability.scala | 19927 | `c6c52873d253c4b2743ea81b1d00280fb0e846526bffd1ed9266619741270669` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/framework/modules/Consensus.scala | 19278 | `d89826cfa2aa841c44359adb8b2902941607c554568ea5a40783ecb2ab9a1177` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/framework/modules/ConsensusSegment.scala | 30838 | `90b3f12d92fdc264a363fc9d0ed813e19fd20ea7abc3528bf0e2faa17caf0395` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/framework/modules/ConsensusStatus.scala | 9407 | `b6df566ef8441f950638c414859d3c48c5cde86102bd21b53a4f12e06dcdc6b2` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/framework/modules/Mempool.scala | 2971 | `a65749583c39590de9ee7a0b6d75a332c27cfe38f5cf86cc6ffe7d7b972770c4` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/framework/modules/Output.scala | 5193 | `54c2a640773e753f5ed20ad2e90349822b51c6ec03230f26ba24c7e2a9b59245` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/framework/modules/P2PNetworkIn.scala | 626 | `60d3efa7e124089644d3a805e7be37473ac8534f9771b34008c7cf8df4e3531e` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/framework/modules/P2PNetworkOut.scala | 5386 | `f1bcdd9d33d744a9bf1efa9a129b7404d36cd0a1a1b8059b8a0a1ab2d370366d` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/framework/modules/Pruning.scala | 2175 | `3ac90bd9fb147db19e36d2d3ec396c0c671462cc78a35e3cdca3556704693619` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/framework/modules/SequencerNode.scala | 2188 | `f5fb4ff38d1c4d9143bf9fe8e76a420a29f0c6f104b447bbf3a04867f47e7290` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/framework/modules/dependencies/AvailabilityModuleDependencies.scala | 720 | `2ccd46dd41e955daa2f0fd3ed6c4e616e853d198b85a7758deef96e766349cd9` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/framework/modules/dependencies/ConsensusModuleDependencies.scala | 674 | `c4ae52311c704ee06b59035e847d69c8b676166fd6843dcd686658842333e1c4` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/framework/modules/dependencies/P2PNetworkOutModuleDependencies.scala | 1207 | `2837ae8d349b14d5caad36f6a1dc6813de608a798e2525d7804b8e6163571121` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/utils/FairBoundedQueue.scala | 7899 | `cd9eb29b4756156f85da90c29ab00af6eb8221633302ad153945dcc01c762588` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/utils/FiniteDurationDistribution.scala | 3372 | `133933d972f6602944caf3a6cc99c10b6314ce34b2d73f0900a9102e4eedc5d3` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/utils/JitterGenerator.scala | 1233 | `b47a73166c7d3703a0c415f197be48012aa973af3550a28d144cab5d49b0e07e` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/utils/Miscellaneous.scala | 4806 | `85e3cdfeacc0562a84c41e662e60aba566816bb9ff9d4027212783588b58bca3` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/utils/NamedLoggingUtils.scala | 720 | `09aac1ab93dc504d904982dadda11e84e04ea01b4122735a50a51049549a002d` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/block/bftordering/utils/Probability.scala | 468 | `5d75efd5571a68f4d4f4dcb309cad26f3d540907feadd8df3ec03c66a1ead6e5` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/config/RemoteSequencerConfig.scala | 763 | `a5a61626b1904e31552f5b63d6fc8a0fc222bda60f24201f81586c460f35328c` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/config/SequencerLimits.scala | 753 | `852d8a3f5090642b79bfefc7c99ad88ce9d0f84dd090dd249da309c36f1b1205` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/config/SequencerNodeConfig.scala | 5313 | `85d92fda3c8739d2860bbdc995504613b8cd8d222579e6293e842114f8546b48` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/config/SequencerNodeParameterConfig.scala | 7561 | `5a161e594715c4549a1a129b5f7862e6db6282afcac11fbcb9750343fb51e1fb` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/config/SequencerNodeParameters.scala | 4215 | `0fa19af612ae9366165e296da94d96fae650680b3a8c3b3d621e7614921b84e8` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/config/TimeAdvancingTopologyConfig.scala | 2453 | `27c9c423c7dc31406cfeaf9d1af03e4c774870c8ee2c7898ddbbed730abe437e` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/errors/CreateSubscriptionError.scala | 2057 | `497f6c82e4f694cb1740b9c5fbf950eeb9a4d4b9048cfce79721aa6d1a3abcea` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/errors/RegisterMemberError.scala | 631 | `900b3650b7c482dd26cdcc6b489640bd0ef0817bc61944e7afdfe4a1080cc2c1` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/errors/SequencerAdministrationError.scala | 1446 | `9835062377333c8c8ba9d31e4614cae7e6eb0282d303869158dcc793e15e89e6` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/errors/SequencerWriteError.scala | 1403 | `d82112be18455bb839bfe8fde3881d652c9a71009c71a1bb0f65ea8da3d10de7` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/package.scala | 559 | `6c1d9b58e925ba6ce6e6edc805f3c07450690729d33dadbeafa5d8e6fc861e49` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/store/DbSequencerStore.scala | 81450 | `bb0907e051eda8f51980a3d9cd9eefdd0fc36481012f05526e5e449b8069195f` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/store/DbSequencerStorePruning.scala | 2340 | `e11eb572d565db4f5bc165a4da66732cb6e52ec4b1fe45a393f3c622e853b1ce` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/store/DbSequencerSynchronizerConfigurationStore.scala | 4242 | `467e543032b6f73563f325475231dfd4ac56417011288a8a04fbe56485fc1b9c` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/store/EventsBuffer.scala | 9040 | `39e4e70d9505ae03dc2894c0f00665d1e14a2ac6e7cbb4643920b56ad4bd8c70` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/store/HASequencerWriterStore.scala | 2210 | `09abe4c9887a23cf74ce4b78a5bc465e3cc74e687bed6be3bbd0a0bffe892309` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/store/InMemorySequencerStore.scala | 24453 | `7b893eeae0b652334f4796ee8ff4c7c004cd178f30213edef6c38225a45d8b49` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/store/InMemorySequencerSynchronizerConfigurationStore.scala | 1318 | `db5de7923f3d1f3347d41133fc04cd610ea6a9074585a14c075424f85c3caa6f` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/store/PruningUtils.scala | 1586 | `74d6051075626bfe48ab15b4cca9cb9060671ddabb108fbd50b4ff557d9de324` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/store/SequencerMemberCache.scala | 1885 | `dea1ea30eba94995d554854f2e6f9da71f9ef238a02856276ec0fd3d292749be` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/store/SequencerStore.scala | 53670 | `df4060f56344688e96cb73113d756c87d429eaa5c277edaa5ff108937613f956` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/store/SequencerSynchronizerConfigurationStore.scala | 2112 | `f64c805e3468e606d1b446346c62dc6488bbd255ca547920445e6d35d4f80f48` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/store/SequencerWriterStore.scala | 5956 | `11bb7b55043fee833fea635b14b46f959608d70c715bd554a030823e31f55179` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/store/VersionedStatus.scala | 1994 | `7f74572aae227a1b3658059587af8a86fa025f251d38183eb4d728900c7b90fa` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/time/BroadcastTimeTracker.scala | 2940 | `1d1713e034c8829ab263c286ec3c6ab0d8ce691ef027370c6ad6a09e0ae4c188` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/time/DisasterRecoverySequencingTimeUpperBound.scala | 658 | `d5ab89fff5f9f8b2b26d809a7ebb3405d3d5fb5ad4440934adbd446149124c52` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/time/LsuSequencingBounds.scala | 5293 | `33c1797babf5470cac7ff4ae20a0a4e824e3274b0163d23bb3bfe46e91b9d60b` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/traffic/LsuTrafficState.scala | 2060 | `61ad430798ed4b74dc5f4d697227181617eae2f08389ac0b483bb1a0ac9f1c20` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/traffic/SequencerRateLimitManager.scala | 11536 | `1be5a438e2c8159041f50d149a594c54128f10b4b6ae054f592bd40b7a9c08d8` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/traffic/SequencerTrafficConfig.scala | 2097 | `61ba4b15308e7f3a17c56b0ffb3b152d504b9a4edb59ce83d2ced3d96c461c6a` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/traffic/SequencerTrafficStatus.scala | 611 | `df15df49b095777b02f0404bdfc9fb90d0fc60944ceeefc5a6eb1a5bf6370387` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/traffic/TimestampSelector.scala | 2873 | `f35c2b03cd13dfd46c19e88cacd4d08e84a049309ed81165e2b2f47590d4a8aa` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencing/authentication/MemberAuthenticationService.scala | 31845 | `b66ee74149383508c6dbbf7611472af61190c0c10c3c621dc736a9c62e54fc72` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencing/authentication/MemberAuthenticationStore.scala | 11861 | `54f513e49c264955aa6636cf4d51162084712d492c35d4ac379950fe7d3b0d32` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencing/authentication/MemberAuthenticator.scala | 3358 | `d85969127e9b341d179a2a4af2a8eb0e1d94addd6b24c109acde2d789b1868af` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencing/authentication/grpc/IdentityContextHelper.scala | 965 | `9077f143935ecdf78288470b251bc17c3f7090a550b7d836384ec32bf7d022a6` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencing/authentication/grpc/SequencerAuthenticationServerInterceptor.scala | 4571 | `14ec28d5637934638f236655f9702641707eb439fe7c68ca285e4dd7d913606e` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencing/authentication/grpc/SequencerConnectServerInterceptor.scala | 2258 | `f68b3315616c2e116bf0bb1771879782df6cd840894a1477431d375c304fe381` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencing/integrations/state/DbSequencerStateManagerStore.scala | 13203 | `621e3a45eb8e0eee5ce5bd607353cde744f9f794f1d0eac8641ea0d379b1ecbf` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencing/integrations/state/InMemorySequencerStateManagerStore.scala | 5161 | `1b8e745b8299eb1d276a4adad0898a6bb32abdd57f1b4a134e7567a8c2ad1643` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencing/integrations/state/SequencerStateManagerStore.scala | 1961 | `1a246c37f6c637de426456c25019a719dac0bc91f982d6e4c2ed2a67d08d6a56` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencing/integrations/state/package.scala | 385 | `772ea924f7801e60d09a8c0cd9701a6c9923772376a63740e66f4b6a70bd239b` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencing/service/CloseNotification.scala | 795 | `10d40d083a97afe07737d6b21ab73acb46b2537ece6bc212ca58a480cae5c554` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencing/service/DirectSequencerSubscription.scala | 4938 | `a740c012be996390a2f8f74e6ca3607f28e9c35b3a353953f3345e600c6ca296` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencing/service/DirectSequencerSubscriptionFactory.scala | 2966 | `f4951a03c42b54d916df1bf274e5664d0293e0608bacbf7e8c9c208c9086cc39` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencing/service/GrpcManagedSubscription.scala | 10225 | `bea98d3d3af1f2ecdd0a0788277044899d77cb0d03a94b87ba9b52ac46cc9854` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencing/service/GrpcSequencerAdministrationService.scala | 21962 | `dc36e7dd8da6e1beafdd1293a1df76bc0ea2a3ad9d9dbd249508950267019891` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencing/service/GrpcSequencerAuthenticationService.scala | 14909 | `40f992fcea9f0959256c8e251521bafed40db1f922a56a5e3ee47e08057e1ce3` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencing/service/GrpcSequencerConnectService.scala | 20214 | `6f655cc7f72c0f92b3a0c5aa1b9ed520e5d3d5d78f3515ae992c2a0115483810` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencing/service/GrpcSequencerInitializationService.scala | 24074 | `eccadcaec507134eca2a87a741259ef54a3f52ffe3d00cdf45b4b991767a1578` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencing/service/GrpcSequencerPruningAdministrationService.scala | 4248 | `6340727a04618c4b004a8af48787afb8bda11716c92be986578aee6e134735d6` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencing/service/GrpcSequencerService.scala | 40387 | `5ad9117588d5138cdf4de1a76312e8bdbad473417a01ece98b12ec5a033c7b23` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencing/service/GrpcSequencerStatusService.scala | 1659 | `31b8c829cf77e8f06642dddb42643e30c2271bd5623c26e34ffa6d087ce0f98a` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencing/service/GrpcSequencerTrafficInspectionService.scala | 2237 | `c7695e7c7a9d25dccde214aaf1fbeb91a28fadcf3f2a313c85fc5ae583166207` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencing/service/SubscriptionPool.scala | 9452 | `eb198b627a75fb17dbd8d6a4885a4ad8f78a276e6d60fb090e69b15a4ecbe3eb` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencing/service/channel/CompletesGrpcResponseObserver.scala | 1416 | `98bb968226bf23b1641e89e2351682c509b26b46fec24adf644e2933ed86bcb3` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencing/service/channel/GrpcSequencerChannel.scala | 12856 | `2e286f8dde2792d36e6799d050228f71960fa92a25bb6be4ac6496a0c54d574d` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencing/service/channel/GrpcSequencerChannelMemberMessageHandler.scala | 9328 | `8cbea35c669d249f00f8a08004cbd67e79c6b9996d642979c485d9e46d6044b9` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencing/service/channel/GrpcSequencerChannelPool.scala | 11416 | `e5091b17d1ffe36fcc9fa7e3dcc76f9fe92c2fc76a03907c3c8762fa72594347` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencing/service/channel/GrpcSequencerChannelService.scala | 5305 | `032859de7366c4539dbd61570e98d53602fcbf67f05204623056579ef4d5f543` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencing/traffic/SequencerRateLimitManagerImpl.scala | 41980 | `e6c1c8cb7f8b7b0342f2008a8d68a2dbdb7e594d8dacd1b83e5805822e009735` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencing/traffic/SequencerTrafficControlSubscriber.scala | 1595 | `bfeb537516a27dda309556deb5651fd4889258d770be9c0d7755261e829b6511` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencing/traffic/TrafficConsumedManagerFactory.scala | 1081 | `82358c472fb9a59d4db352010763916538cb6fb4f9434b59e86644c86fb7a354` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencing/traffic/TrafficPurchasedManager.scala | 25447 | `a962c10e52aea1ff882b5b8f86cd12757e564b6ff6fda92287b84fad97076b17` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencing/traffic/store/TrafficConsumedStore.scala | 4701 | `3b7eff2f860564f6e218aa1457a74284ca0d1943c554d7e19a94cba0feee11f5` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencing/traffic/store/TrafficPurchasedStore.scala | 4342 | `39eff96d30c06c1a3785e5f5200a1fca1ce52aeaca51756f27641151b3d532f7` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencing/traffic/store/db/DbTrafficConsumedStore.scala | 12947 | `4fa3fd51aae311f29bc1a15afd6898b73189c177ee23181ffbcb3344124a2d5e` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencing/traffic/store/db/DbTrafficPurchasedStore.scala | 9988 | `2e0a2de65ac1190a7109f0d1bb1387bc3579a0c5acd5e530a91b65fb0741a42a` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencing/traffic/store/memory/InMemoryTrafficConsumedStore.scala | 6100 | `cc42b99b212a37377e7475754f95cbe2adf0c3005fb25a4e4427f3518300fcda` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencing/traffic/store/memory/InMemoryTrafficPurchasedStore.scala | 5789 | `b63b95868a40056b86df39e84068a54e52a860963179e83cf548f8b0068b7ca4` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/server/DynamicGrpcServer.scala | 3556 | `a77905eccf05eaa43f82e9768c3327f15aed457559877eccc0f3e058f03467d3` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/service/GrpcSequencerConnectionService.scala | 14147 | `72c8a5b14e2cf7ceb5dee99fc5b558872d4b0fa761e1dc9b8a7f3e26a661345a` | 0 |
| community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/service/HandshakeValidator.scala | 2727 | `f8d0b70af06331b345e68b7688e04ccf25846d764661a26b709c3204f225438f` | 0 |
| community/traffic-enforcement/api/protobuf/com/digitalasset/canton/tea/scalapb/package.proto | 353 | `720c7e0b16cf4063052e38a09731f97dbc6607b11fd414f22d382944af9b4ee7` | 0 |
| community/traffic-enforcement/api/protobuf/com/digitalasset/canton/tea/v1/submission_accounting_service.proto | 1405 | `32a7e1651a68de7a91c5a58fffd1ba8b332c3c6333b4d230dc4cf684ea89f6b1` | 0 |
| community/traffic-enforcement/api/protobuf/com/digitalasset/canton/tea/v1/traffic_service.proto | 6128 | `8c76798645dac14805255afeb10dd85f4de3f648bc2cc248993d41ccf86328ed` | 0 |
| community/traffic-enforcement/api/src/main/scala/com/digitalasset/canton/tea/TrafficEnforcementErrors.scala | 11264 | `63d08b6bd02536b97176a153e531c37556bff4e057e69a35e650c0acbd4acb8b` | 0 |
| community/traffic-enforcement/component/src/main/scala/com/digitalasset/canton/tea/TeaSubmissionAccountingServiceGrpc.scala | 1716 | `7f3dd9a34934605296e49221a9216254f257e3019e368fe75e1456d7051f52c5` | 0 |
| community/traffic-enforcement/component/src/main/scala/com/digitalasset/canton/tea/TrafficEnforcementApp.scala | 8200 | `a1d76f90221449149381f0499d925b9a6968cfdd5995f749e4ac3f24cdfdce4e` | 0 |
| community/traffic-enforcement/component/src/main/scala/com/digitalasset/canton/tea/TrafficEnforcementService.scala | 11679 | `5d7b886325e15c8ec477f7e10a184cce2191675db3674cf8dfcad5e9a0707b30` | 0 |
| community/traffic-enforcement/component/src/main/scala/com/digitalasset/canton/tea/TrafficEnforcementServiceGrpc.scala | 2940 | `4a6de4d4e690ef5c5d6bfba320827107e51b20f3b2b1aed9ff447c86a8d64673` | 0 |
| community/traffic-enforcement/component/src/main/scala/com/digitalasset/canton/tea/ingestion/OffsetCheckpoints.scala | 1189 | `61570ceb47b04a7488ccdca1d6c40795d8d36b6145e2d08a8c5276ed2e207189` | 0 |
| community/traffic-enforcement/component/src/main/scala/com/digitalasset/canton/tea/ingestion/TeaCreditIngestionService.scala | 9552 | `6478bd470877acd848b18ba704b6f2547085063360aa79e0754f045d17c8a6bd` | 0 |
| community/traffic-enforcement/component/src/main/scala/com/digitalasset/canton/tea/ingestion/TeaDebitIngestionService.scala | 5728 | `bcd1b97bf3d9bfe469d58b76d9fe6dc5c3761a51d44aeb2a59b2a03052f65f39` | 0 |
| community/traffic-enforcement/component/src/main/scala/com/digitalasset/canton/tea/ingestion/TeaLedgerResources.scala | 3437 | `089d03695e87eba6c5dae082599eb38cd8a2a4a1447de9ab239a4fcf135b9410` | 0 |
| community/traffic-enforcement/component/src/main/scala/com/digitalasset/canton/tea/projection/CloseableProjection.scala | 2365 | `3629f8232451c310e46fb56d625f5190662cc8861ffeec559c50c31b5afe145d` | 0 |
| community/traffic-enforcement/component/src/main/scala/com/digitalasset/canton/tea/projection/CompletionAccounting.scala | 2119 | `303be61f74b02804f85370083ad79ff710dae385f19d3dd1c7645036ae2dad48` | 0 |
| community/traffic-enforcement/component/src/main/scala/com/digitalasset/canton/tea/projection/CompletionRecord.scala | 3790 | `ccc335e70bf8cb77e632e9805cf326a43353ad76c1702e7f6f16486b685b57e5` | 0 |
| community/traffic-enforcement/component/src/main/scala/com/digitalasset/canton/tea/projection/ProjectionEvent.scala | 10433 | `d099bc2bba61f37adf67f22d828c3edbfd8c7b15dec88457419059a78c494934` | 0 |
| community/traffic-enforcement/component/src/main/scala/com/digitalasset/canton/tea/projection/SubmissionCorrelation.scala | 1414 | `afb54e4d62998a98af8ec6dacdb71d72433b772a3891d02dd9f953f31936aa8d` | 0 |
| community/traffic-enforcement/component/src/main/scala/com/digitalasset/canton/tea/projection/TeaProjectionFactory.scala | 12303 | `a53a987974d52106755b7db1d6d116a95a03c443b788d19c666d6ac1315f8455` | 0 |
| community/traffic-enforcement/component/src/main/scala/com/digitalasset/canton/tea/projection/TeaTrafficStore.scala | 5265 | `465d31a490c53a36b7e7ba580dde48cef571254dd68d7bdf6e097955efd13837` | 0 |
| community/traffic-enforcement/component/src/main/scala/com/digitalasset/canton/tea/projection/db/TeaDbProjectionFactory.scala | 6442 | `0f3f34ebd10d8a7300b967af77bd236ecba948f25588508b8bc69c291316ec6c` | 0 |
| community/traffic-enforcement/component/src/main/scala/com/digitalasset/canton/tea/projection/db/TeaDbTrafficStore.scala | 28591 | `4be54b838d1707e48240dc6eedce7e3bb9be7b65b9a57a262af24c1bff78db30` | 0 |
| community/traffic-enforcement/component/src/main/scala/com/digitalasset/canton/tea/projection/memory/TeaMemoryProjectionFactory.scala | 4690 | `0cb88fa6c2ede9f468903cb7e2e47b0687cc334a92b94dc4a4d7e252e4e200f7` | 0 |
| community/traffic-enforcement/component/src/main/scala/com/digitalasset/canton/tea/projection/memory/TeaMemoryTrafficStore.scala | 11906 | `080a8b11ab2ef5639745f49266022731ad5aeae2915162a3a998a79dabeb3a0e` | 0 |
| community/transcode/codec-json/src/main/scala/com/digitalasset/transcode/codec/json/JsonCodec.scala | 11689 | `ec84400281d82a09e5c28879001e85b8369d0196aa85377d99b6528f4cf0e734` | 0 |
| community/transcode/codec-json/src/main/scala/com/digitalasset/transcode/codec/json/JsonStringCodec.scala | 730 | `812556faac083a78924929ecf778c727270bbdf2cacbed72214ed874f2b2d62b` | 0 |
| community/transcode/codec-proto-java/src/main/scala/com/digitalasset/transcode/codec/proto/ProtobufCodec.scala | 6490 | `170dc65477fd315b6ebfead4762517674a716907def761d5f47bf7b74f1e0b23` | 0 |
| community/transcode/codec-proto-java/src/main/scala/com/digitalasset/transcode/codec/proto/package.scala | 1194 | `193953ecaed60a93563fd23a51f2937e3e29217100a20758dc5d4ca71527eadd` | 0 |
| community/transcode/codec-proto-scala/src/main/scala/com/digitalasset/transcode/codec/proto/ProtobufCodec.scala | 7785 | `362614019a0d59eba50959851c27c2321b8182c057a826edd46b2fd63de8a081` | 0 |
| community/transcode/codec-proto-scala/src/main/scala/com/digitalasset/transcode/codec/proto/package.scala | 783 | `3bd81524e2b8b89c2320c37dd7ac736c49e3600fa882b060ba9db3a45be6fdbc` | 0 |
| community/transcode/daml-lf/src/main/scala/com/digitalasset/transcode/daml_lf/LfSchemaProcessor.scala | 10645 | `343d34870193cd94c6cc7f1419fa45a29e518428b53150887143119453b0a11d` | 0 |
| community/transcode/daml-lf/src/main/scala/com/digitalasset/transcode/daml_lf/package.scala | 848 | `c3dd4a17ca73d2aefd4394a573d0724ee1e975621bbe939015344434c99a3708` | 0 |
| community/transcode/schema/src/main/scala/com/digitalasset/transcode/Codec.scala | 1067 | `deee9af3a261a0c112bb2c2ebe60bc638feee2ebde04a5d657597ae851f651d0` | 0 |
| community/transcode/schema/src/main/scala/com/digitalasset/transcode/Converter.scala | 384 | `6f39de1c15f78f28311e457afeead5b88b84d6d8194242c8038c58eeb727b605` | 0 |
| community/transcode/schema/src/main/scala/com/digitalasset/transcode/Decoder.scala | 406 | `7563ed61ace095ea8d4e8485f45c56dd2b2af6ac3799f7a5207d2dd931519c1a` | 0 |
| community/transcode/schema/src/main/scala/com/digitalasset/transcode/Encoder.scala | 409 | `6e651eac8e6e0a4e19c7e8f3db3273dc352b297234cbb8d7c90ae64b11de4d16` | 0 |
| community/transcode/schema/src/main/scala/com/digitalasset/transcode/IncorrectVariantRepresentationException.scala | 275 | `3f161a266a15b390932d884daa076a6c4993f34f3a149b71cf5ac1f53dee5fee` | 0 |
| community/transcode/schema/src/main/scala/com/digitalasset/transcode/MissingFieldsException.scala | 294 | `48320995d058863265abc22abc9db8e5be85d74a4ca02c85dabb4d79262784b6` | 0 |
| community/transcode/schema/src/main/scala/com/digitalasset/transcode/UnexpectedFieldsException.scala | 305 | `8d51cac5966592fa0776ccafb70c09e25b32c1405a76f8ce53d2bb91ea711aa4` | 0 |
| community/transcode/schema/src/main/scala/com/digitalasset/transcode/schema/Choice.scala | 565 | `0b19d91ac3728461167cc49408e187858fd02c5091ce3a95049f0e35be6c7df4` | 0 |
| community/transcode/schema/src/main/scala/com/digitalasset/transcode/schema/CodecVisitor.scala | 4083 | `2fd3d91ad4f33cbd3615157244569fbb5778bd87ca37a6c1830a472335e7b708` | 0 |
| community/transcode/schema/src/main/scala/com/digitalasset/transcode/schema/Debug.scala | 5569 | `670162afac2d994a5823ac4cbb6a12857962247ff3118f575fc4d6006c3d53a7` | 0 |
| community/transcode/schema/src/main/scala/com/digitalasset/transcode/schema/Descriptor.scala | 9735 | `cfa51d0988ca29a42459fc5e2ed89eaecc44e3b0d20d93a548fdb89d2cb62511` | 0 |
| community/transcode/schema/src/main/scala/com/digitalasset/transcode/schema/DescriptorSchemaProcessor.scala | 2949 | `8bae5d2154d129e8f5b181738d401e644a2aa99c1af0b8f7f566261f718954f0` | 0 |
| community/transcode/schema/src/main/scala/com/digitalasset/transcode/schema/DescriptorVisitor.scala | 2064 | `a0218a0db4830de450f38f6c42173fe8d13d108c2f41d2e61adc3f26faf68e51` | 0 |
| community/transcode/schema/src/main/scala/com/digitalasset/transcode/schema/Dictionary.scala | 5062 | `3337055b6df35909ae12a9c656267fcf037b2de14f4492b8aabbd6bec94681a3` | 0 |
| community/transcode/schema/src/main/scala/com/digitalasset/transcode/schema/DynamicValue.scala | 8720 | `930af0ade7b0982e931957062675465f91eec6b5f25534b1b2263c603b7695da` | 0 |
| community/transcode/schema/src/main/scala/com/digitalasset/transcode/schema/HasDescriptor.scala | 238 | `03c98805883aff0f9e7b75bd520897282551499d9febf2c2aff8da459b13f499` | 0 |
| community/transcode/schema/src/main/scala/com/digitalasset/transcode/schema/Identifier.scala | 1961 | `4035a2aa342b29cd23b28320ab2ecac0b6df51006351f01e42e3014ccb1f8ec3` | 0 |
| community/transcode/schema/src/main/scala/com/digitalasset/transcode/schema/IdentifierFilter.scala | 6642 | `412bd25b1606dd2801353fa1e76871e6494ee076715a0c4db0c9711622e8a734` | 0 |
| community/transcode/schema/src/main/scala/com/digitalasset/transcode/schema/LazinessManager.scala | 939 | `16c6b0e365c5fb2c0f4b37dc892752215e72afd097f5afb93a99ac1291d03ef9` | 0 |
| community/transcode/schema/src/main/scala/com/digitalasset/transcode/schema/Pickler.scala | 3477 | `801bb79f6cf1856cf3b64bffb5bfd48e57a9b83c4287a428313616e03c0870d7` | 0 |
| community/transcode/schema/src/main/scala/com/digitalasset/transcode/schema/SchemaVisitor.scala | 10987 | `3841778ea00d194b427f2c2a7bb1aeabe82e5e1ffe6851b5427d772489c297ff` | 0 |
| community/transcode/schema/src/main/scala/com/digitalasset/transcode/schema/Template.scala | 989 | `5c2987849b3edaff9cdf9654fb9ca9158f3704ad84e92c216cb9393078d9631c` | 0 |
| community/transcode/schema/src/main/scala/com/digitalasset/transcode/schema/package.scala | 2411 | `b933ca5562fe64731231a9f9b45235eacdc7e53e57e7cdac790d66774c76e602` | 0 |
| community/util-observability/src/main/scala/com/digitalasset/canton/logging/ErrorLoggingContext.scala | 9330 | `4008302dd7da896356611a549e29561c0fabcd91bb3fd5e467380e6ba8925aa9` | 0 |
| community/util-observability/src/main/scala/com/digitalasset/canton/logging/LoggingContextUtil.scala | 954 | `202138f2de19787ce323d1db20b9c50166eae239f665a485fb0fd2cbf4bb9aa2` | 0 |
| community/util-observability/src/main/scala/com/digitalasset/canton/logging/LoggingContextWithTrace.scala | 3915 | `e8e2ab9f39fbadb58ac7868921de5271f9c39b588d6891c8c8b5dc05677da8dd` | 0 |
| community/util-observability/src/main/scala/com/digitalasset/canton/logging/NamedLoggerFactory.scala | 5327 | `67c1293be47d3d8130814d3355bca55881ee8cdbb84dc4ad4ef33223a9a8f2d4` | 0 |
| community/util-observability/src/main/scala/com/digitalasset/canton/logging/NamedLogging.scala | 2299 | `83b8709941a0b7aef3334146097aa68f1838d64a86deb3327dc59bc29ee0d6d9` | 0 |
| community/util-observability/src/main/scala/com/digitalasset/canton/logging/NamedLoggingContext.scala | 3933 | `5a1284982dc2984543ef78a677ec2cff5e92431412222ab93d2a1f9ae6bb1388` | 0 |
| community/util-observability/src/main/scala/com/digitalasset/canton/logging/RewritingAppender.scala | 7567 | `28c390442f8383cd3c0e2aa328d463133d099f847cdcce9ffeb3507b6595d9dc` | 0 |
| community/util-observability/src/main/scala/com/digitalasset/canton/logging/TracedLogger.scala | 1604 | `fd3afaaa70c609047f7d4e77ad82d039f375959b9a58db61e8f07f11c892be9a` | 0 |
| community/util-observability/src/main/scala/com/digitalasset/canton/logging/TracedLoggerOps.scala | 2606 | `b83b149a15ea56148340bd9d4cb761037c24328833c64ca9c179f9a776615c7c` | 0 |
| community/util-observability/src/main/scala/com/digitalasset/canton/logging/package.scala | 487 | `d65609e4fd275edf35705693478746f47283082fb56d78bf0bfda6dc91eaac8e` | 0 |
| community/util-observability/src/main/scala/com/digitalasset/canton/telemetry/ConfiguredOpenTelemetry.scala | 1233 | `4654d29c408e10e041fe4242a461faf53e39e3dd8bd1dad60595bccb74535a5a` | 0 |
| community/util-observability/src/main/scala/com/digitalasset/canton/telemetry/OpenTelemetryFactory.scala | 6221 | `2d103b9ea334c9269ac3192ae88be08896a0d9317e75ad5500cd15cfadcd0077` | 0 |
| community/util-observability/src/main/scala/com/digitalasset/canton/telemetry/OpenTelemetryViews.scala | 6805 | `850ceb3133f0878fb5b3cebc9e914119c39bca2b767f776086faa643d4d0468b` | 0 |
| community/util-observability/src/main/scala/com/digitalasset/canton/tracing/HeaderName.scala | 751 | `d7de676955912e95283db1847e5ddc20a7fe4a4d8250fc2044c13d584c0548c1` | 0 |
| community/util-observability/src/main/scala/com/digitalasset/canton/tracing/NoTracing.scala | 359 | `60d271c0de7e0ff6af02f1e919578694bcd5583006d8cdd3dd0138fb2983f678` | 0 |
| community/util-observability/src/main/scala/com/digitalasset/canton/tracing/TraceContext.scala | 6749 | `a137af56e199179e3e4a7beaa4950797c8a01ec5b5ea4c12cd7044d62fbd791e` | 0 |
| community/util-observability/src/main/scala/com/digitalasset/canton/tracing/TraceContextGrpc.scala | 7799 | `26d2bc9bd89ef65c02b3e104e7ab9f0569a1c42b268e3ac65f5aa39101b0f1d9` | 0 |
| community/util-observability/src/main/scala/com/digitalasset/canton/tracing/Traced.scala | 2404 | `11c66b3f11ff7ef24d212cc93c2156101eea5b6d5ecb76f008ba3e588cde23f1` | 0 |
| community/util-observability/src/main/scala/com/digitalasset/canton/tracing/TracedMany.scala | 1518 | `3c8f26493545826cc47069fa897cc17e8ab764cc65764776077342eb909992ab` | 0 |
| community/util-observability/src/main/scala/com/digitalasset/canton/tracing/TracerProvider.scala | 3943 | `3d517a82afd601b9671276fa5b7201750b85a1ecebf74546facec505b90e3de0` | 0 |
| community/util-observability/src/main/scala/com/digitalasset/canton/tracing/TracingConfig.scala | 1963 | `882b71d93eef81e71a3d0b54aab5611b0cb0551b07615752f7b4522e1f7ccdd9` | 0 |
| community/util-observability/src/main/scala/com/digitalasset/canton/tracing/W3CTraceContext.scala | 4827 | `5b331f3ca4f9c5fd13fa167faa7248a60e78f8d8db0fdab0cc31a7d46729e918` | 0 |
| docs-open/src/main/resources/include_generator.py | 25245 | `175d2ad68cc8fa41441924390de6769355cadf794b59926e09c4050054968ad8` | 0 |
| docs-open/src/main/resources/literalinclude_directive_replace.py | 7701 | `051b1c156de181bc486b79b1621b351033eed6f9ec4dfc6a57b78689acdb3eac` | 0 |
| docs-open/src/main/resources/snippet_directive_replace.py | 3929 | `e7eefebc4c2a676dbb57d252f1fda32795432c2978cb67a95d0455d8507d417d` | 0 |
| docs-open/src/main/resources/storage.py | 1653 | `b67bb023b0c6867d0713db0a06f521208720188fa6c3053c820e05994e79408d` | 0 |
| docs-open/src/sphinx/conf.py | 6151 | `a8f6e2cb91637065af399e9a8a2e6ea82009dbbc1ad61901fb0016faafc2bb10` | 0 |
| docs-open/src/sphinx/exts/pygments_daml_lexer.py | 838 | `2f6490156425aa394e9c289ddf781e5349be8da7591a9872359faf195912c2b6` | 0 |
| docs-open/src/sphinx/exts/ref.py | 508 | `2152661f07a91112d68336a9544c1e7e1769339a801011cde09af1c0487983c4` | 0 |
| docs-open/src/sphinx/exts/wip.py | 632 | `3f82e2b185724e77f3b8678d44f5c45dcfb4c8f5738aa71c5da33357324ef6ba` | 0 |
| docs-open/src/sphinx/participant/howtos/secure/apis/jwt.rst | 9890 | `f1b4267ef060d430cd93c09f7668c1171c8cf865db15a82ebf2c299754ddab97` | 0 |
| performance/src/main/console/tls/participant.crt | 1996 | `4a787543ae5ca065b005dec9a4d7544cb4a3ad1e3025956a8b4387d52b924e05` | 0 |
| performance/src/main/console/tls/participant.pem | 121 | `41b6c1b1fe89bcc37ba533f616975bac36dac730be25255b58b4a595e5255531` | 1 |
| performance/src/main/console/tls/synchronizer.crt | 1988 | `dabbfea618c6fc1e021e61f40e4d7c5fa5b193ca8df03296af7f44c98c589998` | 0 |
| performance/src/main/console/tls/synchronizer.pem | 121 | `ce33b30d50711f87a8bc16840f77dd4036f8173dacfb5fe5d5acb2721c697f7d` | 1 |
| performance/src/main/scala/com/digitalasset/canton/performance/console/MissionControl.scala | 8004 | `4e6db69a34c0063a56516884d43b8045f43b5430862a0595270971f772cac08f` | 0 |
| performance/src/main/scala/com/digitalasset/canton/performance/scenarios/CantonTesting.scala | 17146 | `3b137dac4929bb9c071c1663de8fe6629c9d6451f053549e20a079e02d024842` | 0 |
| performance/src/main/scala/com/digitalasset/canton/performance/scenarios/LongRunning.scala | 15758 | `f089977d7b208ac99335fe340161a686149cf26aea98a732aae3958b9dc279d6` | 0 |
| performance/src/main/scala/com/digitalasset/canton/performance/scenarios/OfflinePartyReplication.scala | 9618 | `92acc587531105c9c3fe4ae694f776d57e1fe35c09fcf08bd3099179f5346634` | 0 |
| performance/src/main/scala/com/digitalasset/canton/performance/scenarios/SynchronizersConfiguration.scala | 7546 | `5aa0844c4dfe599b8097ab415c0cd77a0c79dc4c1157bd1ec70aea472072f807` | 0 |
| performance/src/main/scala/com/digitalasset/canton/performance/scenarios/TransferTesting.scala | 13839 | `f084d85139119fe43bd117271158a09304ce4ef1612962ded2ae885024c07d82` | 0 |
| performance/src/main/scala/com/digitalasset/canton/performance/util/FixedSyncCryptoApiForSigning.scala | 14101 | `a406a72f142777948af1496d25c30077278dc8649232d28fa82e044785068ecd` | 0 |
| performance/src/main/scala/com/digitalasset/canton/performance/util/ParticipantSimulator.scala | 29248 | `c5a055c24805c99c78224b8bbb266d1ea8e4eb2b188d4ad70c752eb97b52f876` | 0 |
| project/BufPlugin.scala | 2504 | `44aa0623c102ad2c57f23023b7dc63f7e27d5062e9989dd91826ae82add4c65c` | 0 |
| project/BuildCommon.scala | 163895 | `70d4bed9f8a53e0ca3d4abfb8fa94745de7bdfeb448a1fd54e618e1374d2b675` | 0 |
| project/CantonScalafmtPlugin.scala | 8576 | `93b11459d175787ecaf6eec761a7cac09498fbb4c4c59337e0220daf677f67b6` | 0 |
| project/ComponentTestDamlGenerator.scala | 2296 | `3afb787823552343f1e1f1dc3c4d8466737c34ee8cd2efc0dc358ee2dc4e80db` | 0 |
| project/DamlLfFeature.scala | 7634 | `98825523093097eac788eef86aa221c15d2b8fd2769f2a6322e9b89255701aa6` | 0 |
| project/DamlLfPlugin.scala | 4820 | `623a3118da466cd92180656537944b13962af243e73d6ce2b67c7b1114372127` | 0 |
| project/DamlLfVersion.scala | 4668 | `27c2ff10d28eae4673eaa092225e52ca5662ae53bb614ac1e74e46bdc2134f33` | 0 |
| project/DamlPlugin.scala | 32444 | `47d8c2bce8cb144dca0684b7cb4c598ec638bfc918c56c135dd210a2dc65d54f` | 0 |
| project/Dependencies.scala | 22766 | `2f073f11c6a48081b14e429fb3d440df42c5727ebec4be421cd65a0168a02e2f` | 0 |
| project/DocsOpenBuild.scala | 32211 | `041f627563a5f7dbb10e6954542761b52bc829df2839953b2f425c99f29df954` | 0 |
| project/Houserules.scala | 8164 | `8ca8153d0a60f5b09c9c8b37c3e8dc6bdad12d8326fc522da49c74297ba1cae6` | 0 |
| project/ProtocNixPlugin.scala | 4306 | `774e214286fb9b575feb5f0eb256bf0c76a7e8d13969eed2ce1951b741e8d6bd` | 0 |
| project/ProtocRetryPlugin.scala | 1540 | `7712161ef9c58c02dfaf02c812415ac841f7a8ad5fe6dc5c730a8206cce6ccbd` | 0 |
| project/Release.scala | 10914 | `8eff0fb3186b41e233de09094437735793fa56d7f54b4e1c46890c52c017f921` | 0 |
| project/Scala3Migration.scala | 433 | `d3deae3fd11d7cb59b06d640d72af8db6afebe91f71ea955c781022e200646c4` | 0 |
| project/SharedDependencies.scala | 11260 | `da2e3841d818d6f465422f7482241861a3d41f9360d30ad7f7689a149845c801` | 0 |
| project/UberLibrary.scala | 2846 | `f09b96c538dc7f5d637685499b9b99e8852a86b9acdeba57d06cf45858152510` | 0 |
| project/Z3.scala | 2743 | `88561b0ead15c6622444086e86ea042de111d717b277ad2e9ee312dab986af52` | 0 |
| project/project/DamlVersions.scala | 981 | `1f3ff28672fa36a1d086abd1d99d2771c80b3603d75275ca339fc859d2eaa3a7` | 0 |
| release/update_dependabot.py | 4844 | `ff0b6c8b90ccc3dfd3f5536b6c07a5cbb58e5ce187644ce146fb48d06918d301` | 0 |
| scripts/backport.scala | 5754 | `9005ac55610f8ba25f10f01e6020ed15fa1ff360da3bdc5ae6e1798a790490cd` | 0 |
| scripts/ci/alert_slack.py | 14125 | `6d226bc3c5b8ee52baed27ba851b39d86261e7ca47754e9a574acd434f2aaa23` | 0 |
| scripts/ci/check-datadog.py | 83 | `948d5cea0b77620250726104b92fda98c340fdb253f65de335591d25dee29386` | 0 |
| scripts/ci/check-multiarch-images.py | 3234 | `356f44bc49653be18da5225fbf05cf179a48c9d9d417a16646df3d504914d366` | 0 |
| scripts/ci/check_canton_build_required_gate.py | 8468 | `848eb51b36ce8b32305ace75a1b81d194cd2f6d5308e3cc6ae4440fa888d1947` | 0 |
| scripts/ci/check_guarded_excepts.py | 19403 | `182f3b153d05692c6e08b97aaccee459d2e1dc261ef79e754690a369832a72c6` | 0 |
| scripts/ci/check_sql_definitions.py | 2989 | `5ffbb0fd7e05e647d97cb594459fc90ad133b829b2b5364a2480e60267920303` | 0 |
| scripts/ci/close_stale_flake_issues.py | 7135 | `de4e1a3d9d5af176e2219e4265b4a4e08c02406472ba59673d38bc908e1b87ac` | 0 |
| scripts/ci/collect_flake_evidence.py | 61925 | `44b22195b3e9d0b370103d603f403e6a3db9eb19584fe0de64cbba6328d64e03` | 0 |
| scripts/ci/flaky_common.py | 45862 | `3440129a931bc80e0a8f28176bd1c01f811bfe9d39d632206e406437cb79f99f` | 0 |
| scripts/ci/generate_watchdog_xml.py | 8506 | `d52ad8cdcee63d59b1082b8ee24bb1f1ce06f644b1c5c2da3c10adeacb094abc` | 0 |
| scripts/ci/join_multiline_log_records.py | 3883 | `fa668260f63b895c6fc8b50a33eb34ca46da1c4a8024b0cd43f7f8d31493c5d1` | 0 |
| scripts/ci/manage_flaky_issues.py | 101005 | `07aa98528475e063c1528607a99f4c31fb6ab46d46bdbfe71c859e4e2b74eead` | 0 |
| scripts/ci/notify_job_classification.py | 3288 | `831d564c666ebdf93d15cd8c7c9a93f8c71c5df2f2f6c73b0de8d39b6e74dc7a` | 0 |
| scripts/ci/parse_compile_times.py | 1414 | `f88e60a25f7d88a75701d2aee6369000b8cb0f1e1fff59e06cf3aee881d6c77d` | 0 |
| scripts/ci/parse_sbt_cmd.py | 7718 | `c8a8bbdcebbdf37261b8136a81e8aa6f40b11f577f133879e051a8b3cfeb4857` | 0 |
| scripts/ci/prepare_rerun_command.py | 6410 | `f0cb58964ab56c6850d281f8f6bbeca160acfa32c0ad2db102809502abf8847d` | 0 |
| scripts/ci/remind_upcoming_rota.py | 15494 | `f629ff1ecedcf0c08ec08ab797f3cc40cda33f5f7d1b137f0ed89550724815e8` | 0 |
| scripts/ci/report_to_datadog.py | 3218 | `47fc533a0ea893e69d28877200e8875512ca1fdb3880aaf9fef94c5b54b3e7e8` | 0 |
| scripts/ci/rerun_failed_jobs_gate.py | 2761 | `a1702f39b2f406abc0bba072ba037e934cf786d5187b76e6e4d350e654306a8d` | 0 |
| scripts/ci/select_rota.py | 35045 | `83e7316a12e9e0c401e3e72f89eb8a6a8a43713593ecfa4d0669e04040140d30` | 0 |
| scripts/ci/todo_refs.py | 7058 | `952e17940e9cb5047edcca200d57ae7ca4de120bcec20d6d31fcab3790efca67` | 0 |
| scripts/ci/update_rota_topics.py | 16319 | `5a505cf56e8fdf6e7575facf951ae6f3d9749e942b8be746f9f76396b32f89d1` | 0 |
| scripts/pyproject.toml | 1794 | `5449a7ffce511604fd97a725e2a22b10b521625f95f82297e9e8988257dded94` | 0 |
