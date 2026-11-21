# Security & Post-Quantum Readiness Audit Report

**Project:** xrpl4j @ bbbd620b6214 · XRPL Foundation — public repository (passive review)
| | |
|---|---|
| Organization | QSI |
| Report date | 2026-11-21 10:22 UTC |
| Report version | 1 |
| Audit run | c388b044-b9ac-473d-9fe9-edf415fad5a5 (Document audit) |
| Analyzer engine | qsi-engine 1.8.1 |
| Risk profile | Web3 project |
| Content SHA-256 | `4b51766decd8fed732fc4d7790df3dbfacbcd2bde9d09b827d8df02287718f16` |
| Signature key (Ed25519 SHA-256 fingerprint, then the ML-DSA-65 one where it co-signs; the signature is the separate file report.sig.json) | `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e · ML-DSA-65 dbd4e297b3213d1d7577a565e76de14cc5ad0e409f1dc68291c67266fc95066a` |
> This report presents automated and documented analysis results for the stated scope. It is not a legal opinion, a certification or an attestation of compliance with any standard.

## 1. Executive summary

- Critical: **0**
- High: **0**
- Medium: **5**
- Low: **1**
- Info: **1**

- Confirmed technical vulnerability: 0
- Known vulnerable component: 0
- Confirmed configuration error: 0
- Potential cryptographic risk: 0
- Long-term post-quantum risk: 6
- Improvement recommendation: 0
- Insufficient data: 1

Mosca's inequality (x + y > z): x = 5, y = 5, z = 12 → tight margin. _z is a planning assumption chosen per risk profile, not a prediction. A cryptographically relevant quantum computer is not publicly known to exist today._

**Post-quantum maturity: Level 0 of 4 — no post-quantum cryptography.** Next step: Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

## 2. Scope and boundaries

Mode: Document audit

Repository: <https://github.com/XRPLF/xrpl4j> @ `bbbd620b621491765dab54dd6bf14ae8ef3b901a` — evidence links open the lines at this commit.

645 files, 2721893 bytes in total, 0 redaction(s); the per-file SHA-256 list is in appendix C.

## 3. Methodology

| Area | Status | Count | Examples |
|---|---|---|---|
| dependencies | checked | 6 | pom.xml: 28 dependencies parsed (16 pinned); xrpl4j-bom/pom.xml: 3 dependencies parsed (0 pinned); xrpl4j-client/pom.xml: 15 dependencies parsed (0 pinned) |
| source_code | checked | 639 | xrpl4j-client/src/main/java/org/xrpl/xrpl4j/client/JsonRpcClient.java: 247 lines scanned with 16 rule patterns and 313 registry patterns; xrpl4j-client/src/main/java/org/xrpl/xrpl4j/client/JsonRpcClientErrorException.java: 35 lines scanned with 16 rule patterns and 313 registry patterns; xrpl4j-client/src/main/java/org/xrpl/xrpl4j/client/JsonRpcRequest.java: 57 lines scanned with 16 rule patterns and 313 registry patterns |
| entropy | checked | 1 | random-number generation: 639 code files read with 0 macro definitions from the tree; 0 ineffective guard(s), 0 weak random-bytes provider(s), 0 weak key-generation site(s) |
| crediting | checked | 1 | payment crediting: 119 file(s) read incoming transfers on TON, the XRP Ledger, Tron or an EVM chain, 0 credit from a Tron or EVM node; 0 lead(s). A wait for confirmations or finality is recognised by its words, not traced; reorganisations and duplicate crediting are not checked |
| osv_advisories | checked | 1 | 16 pinned packages queried at OSV.dev; 0 affected |

_Long lists are grouped here; the full per-file list is in the JSON report, signed with the same key._

## 4. Assets examined and not examined

- None

## 5. Architecture overview

Static review of the source tree xrpl4j at bbbd620b621491765dab54dd6bf14ae8ef3b901a. 645 files analysed; of 1276 files, 605 are test, fuzzing, benchmark or example code and were left out, 26 are not read by any analyzer, 0 exceed the per-file limit and 0 did not fit the total limit. Files no analyzer reads include: .ai-review/instructions.md, .claude/skills/batch-deps-upgrade/README.md, .claude/skills/batch-deps-upgrade/SKILL.md, .coderabbit.yaml, .github/actions/xrpld-login/action.yml. 30 files in build-output or dependency-cache directories (.git, .hg, .venv, __pycache__, build, dist, node_modules, target, vendor, venv) were not read. No requests were sent to the owner's systems.

## 6. Overall security posture

- Indicative posture index: **100** / 100 — _Derived from findings in scope (confirmed and potential issues weighted by severity). Indicative only; not comparable across differently scoped audits._
- Quantum-vulnerable share of inventory: 72.7%

## 7. Detailed findings

### QSI-2026-34918 — Quantum-vulnerable Pedersen commitment: threshold signing and MPC protocols (2 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:Pedersen commitment:threshold_mpc`
- Data source: xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/util/jna/JnaPedersenCommitmentGenerator.java
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.8.1 · 2026-11-21 10:22 UTC
- Priority score: 33.0 / 100
- CVSS v3.1: not applicable

3 reference(s) to Pedersen commitment across 2 file(s), e.g. xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/util/jna/JnaPedersenCommitmentGenerator.java:75. Role, judged from paths, function names and nearby code: threshold signing and MPC protocols. Paillier, Pedersen commitments and the discrete-logarithm proofs inside threshold ECDSA and EdDSA protocols all fall to Shor's algorithm; a post-quantum threshold scheme is a protocol change, not a parameter change.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/util/jna/JnaPedersenCommitmentGenerator.java:75 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/util/jna/JnaPedersenCommitmentGenerator.java](https://github.com/XRPLF/xrpl4j/blob/bbbd620b621491765dab54dd6bf14ae8ef3b901a/xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/util/jna/JnaPedersenCommitmentGenerator.java#L75) · line 75 · SHA-256 9d42bfbe1e116d83b86b5196ebd5c74da763efaae58f855240bacb763260e7a2_

```
   74 |     try {
   75 |       result = lib.mpt_get_pedersen_commitment(amount.longValue(), blindingFactorBytes, outCommitment);
   76 |     } finally {
```

_file_excerpt · [xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/util/jna/JnaPedersenCommitmentGenerator.java](https://github.com/XRPLF/xrpl4j/blob/bbbd620b621491765dab54dd6bf14ae8ef3b901a/xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/util/jna/JnaPedersenCommitmentGenerator.java#L80) · line 80 · SHA-256 500a84959fab36c8ea9b293a845253cd9e3e06c8e5dfab57091adfe9db174c2e_

```
   79 |     if (result != 0) {
   80 |       throw new IllegalStateException("mpt_get_pedersen_commitment failed with error code: " + result);
   81 |     }
```

_file_excerpt · [xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/util/jna/MptCryptoLibrary.java](https://github.com/XRPLF/xrpl4j/blob/bbbd620b621491765dab54dd6bf14ae8ef3b901a/xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/util/jna/MptCryptoLibrary.java#L106) · line 106 · SHA-256 3ba041406f8f0edf718d36c45fa36e6554ee02ab258ceff05fe99d5908e9832b_

```
  105 |    */
  106 |   int mpt_get_pedersen_commitment(long amount, byte[] blindingFactor, byte[] outCommitment);
  107 | 
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Track post-quantum threshold signatures (NIST IR 8214C) and keep the protocol layer ready to swap the signature scheme; record which keys and shares must stay valid for how long.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-34921 — Quantum-vulnerable Ed25519: transaction and message signing (2 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:Ed25519:transaction_signing`
- Data source: xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/signing/bc/BcDerivedKeySignatureService.java
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.8.1 · 2026-11-21 10:22 UTC
- Priority score: 33.0 / 100
- CVSS v3.1: not applicable

16 reference(s) to Ed25519 across 2 file(s), e.g. xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/signing/bc/BcDerivedKeySignatureService.java:32. Role, judged from paths, function names and nearby code: transaction and message signing. A CRQC derives the private key from a public key that is already known (on chain after the first spend, in reused addresses): funds and approvals controlled by these keys need a migration path.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/signing/bc/BcDerivedKeySignatureService.java:32 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/signing/bc/BcDerivedKeySignatureService.java](https://github.com/XRPLF/xrpl4j/blob/bbbd620b621491765dab54dd6bf14ae8ef3b901a/xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/signing/bc/BcDerivedKeySignatureService.java#L32) · line 32 · SHA-256 3cf2076b8af60e003819913188842798949946ceca596b600642ea3053a881e7_

```
   31 | import org.bouncycastle.crypto.signers.ECDSASigner;
   32 | import org.bouncycastle.crypto.signers.Ed25519Signer;
   33 | import org.bouncycastle.crypto.signers.HMacDSAKCalculator;
```

_file_excerpt · [xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/signing/bc/BcDerivedKeySignatureService.java](https://github.com/XRPLF/xrpl4j/blob/bbbd620b621491765dab54dd6bf14ae8ef3b901a/xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/signing/bc/BcDerivedKeySignatureService.java#L108) · line 108 · SHA-256 ad592fd14fe2305a8b3d454f5b383c432636c4ab7b84f47ed363ff8f642ee3a1_

```
  107 |       SignatureUtils.getInstance(),
  108 |       new Ed25519Signer(),
  109 |       new ECDSASigner(new HMacDSAKCalculator(new SHA256Digest()))
```

_file_excerpt · [xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/signing/bc/BcDerivedKeySignatureService.java](https://github.com/XRPLF/xrpl4j/blob/bbbd620b621491765dab54dd6bf14ae8ef3b901a/xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/signing/bc/BcDerivedKeySignatureService.java#L294) · line 294 · SHA-256 35a9eab450f19a1726e819e06261965a7721db15adb0dd8c12e89abf63c8509e_

```
  293 |         .asBytes();
  294 |       return Seed.ed25519SeedFromPassphrase(Passphrase.of(passphraseBytes));
  295 |     } finally {
```

_file_excerpt · [xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/signing/bc/BcSignatureService.java](https://github.com/XRPLF/xrpl4j/blob/bbbd620b621491765dab54dd6bf14ae8ef3b901a/xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/signing/bc/BcSignatureService.java#L29) · line 29 · SHA-256 5147e430da6428dcfe320dc4500c5a9786ddce7fa6ab1851c93eb0ba87c5c597_

```
   28 | import org.bouncycastle.crypto.signers.ECDSASigner;
   29 | import org.bouncycastle.crypto.signers.Ed25519Signer;
   30 | import org.bouncycastle.crypto.signers.HMacDSAKCalculator;
```

_file_excerpt · [xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/signing/bc/BcSignatureService.java](https://github.com/XRPLF/xrpl4j/blob/bbbd620b621491765dab54dd6bf14ae8ef3b901a/xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/signing/bc/BcSignatureService.java#L59) · line 59 · SHA-256 75d2d916e76d66e731c946e41fd67a0ffbbd33476e0ab646f513dd690037092b_

```
   58 | 
   59 |   private final Ed25519Signer ed25519Signer;
   60 |   private final ECDSASigner ecdsaSigner;
```

_file_excerpt · [xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/signing/bc/BcSignatureService.java](https://github.com/XRPLF/xrpl4j/blob/bbbd620b621491765dab54dd6bf14ae8ef3b901a/xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/signing/bc/BcSignatureService.java#L68) · line 68 · SHA-256 dac2320439cf4392f11b2a33d3695fb51f021bae9f2d548028f3f166538dc66d_

```
   67 |       new SignatureUtils(ObjectMapperFactory.create(), XrplBinaryCodec.getInstance()),
   68 |       new Ed25519Signer(),
   69 |       new ECDSASigner(new HMacDSAKCalculator(new SHA256Digest()))
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains adopt them.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-34922 — Quantum-vulnerable ECDSA: transaction and message signing (1 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:ECDSA:transaction_signing`
- Data source: xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/signing/bc/Secp256k1.java
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.8.1 · 2026-11-21 10:22 UTC
- Priority score: 33.0 / 100
- CVSS v3.1: not applicable

1 reference(s) to ECDSA across 1 file(s), e.g. xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/signing/bc/Secp256k1.java:45. Role, judged from paths, function names and nearby code: transaction and message signing. A CRQC derives the private key from a public key that is already known (on chain after the first spend, in reused addresses): funds and approvals controlled by these keys need a migration path.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/signing/bc/Secp256k1.java:45 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/signing/bc/Secp256k1.java](https://github.com/XRPLF/xrpl4j/blob/bbbd620b621491765dab54dd6bf14ae8ef3b901a/xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/signing/bc/Secp256k1.java#L45) · line 45 · SHA-256 fc8af049a6dd5b72ba36cca8a943bcc824f37deca220467fc84c46fdd0a1ae7e_

```
   44 |   @Deprecated
   45 |   X9ECParameters EC_PARAMETERS = SECNamedCurves.getByName("secp256k1");
   46 | 
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains adopt them.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-34919 — Quantum-vulnerable ECDSA: role not determined (5 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:ECDSA:general`
- Data source: xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/keys/PrivateKey.java
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.8.1 · 2026-11-21 10:22 UTC
- Priority score: 31.7 / 100
- CVSS v3.1: not applicable

5 reference(s) to ECDSA across 5 file(s), e.g. xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/keys/PrivateKey.java:109. Role, judged from paths, function names and nearby code: role not determined. The code does not show what the keys protect; review decides the priority.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/keys/PrivateKey.java:109 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/keys/PrivateKey.java](https://github.com/XRPLF/xrpl4j/blob/bbbd620b621491765dab54dd6bf14ae8ef3b901a/xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/keys/PrivateKey.java#L109) · line 109 · SHA-256 af04b015fd6a739f767e6fe31f4b8670bad6ae4a28abbbd228f88113cc11df8f_

```
  108 |         "PrivateKey construction requires 32 natural bytes plug a one-byte prefix value of either `0xED` for ed25519 " +
  109 |           "private keys or `0x00` for secp256k1 private keys. Input byte length was %s bytes with a prefixByte value " +
  110 |           "of `0x%s`", value.length(), prefixByte.hexValue())
```

_file_excerpt · [xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/keys/Seed.java](https://github.com/XRPLF/xrpl4j/blob/bbbd620b621491765dab54dd6bf14ae8ef3b901a/xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/keys/Seed.java#L401) · line 401 · SHA-256 4d48f9db74167076795bf520932b9a4fd5b66f82bcd02337c34e191183505767_

```
  400 |        */
  401 |       static X9ECParameters EC_PARAMETERS = SECNamedCurves.getByName("secp256k1");
  402 |       static ECDomainParameters EC_DOMAIN_PARAMETERS = new ECDomainParameters(
```

_file_excerpt · [xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/keys/bc/BcKeyUtils.java](https://github.com/XRPLF/xrpl4j/blob/bbbd620b621491765dab54dd6bf14ae8ef3b901a/xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/keys/bc/BcKeyUtils.java#L52) · line 52 · SHA-256 0760f51eb6dd3c48b310651ca6ee571ae783f9f589e35eae64b993408eccd21b_

```
   51 | 
   52 |   private static final String SECP256K1 = "secp256k1";
   53 |   private static final ECNamedCurveParameterSpec EC_PARAMS = ECNamedCurveTable.getParameterSpec(SECP256K1);
```

_file_excerpt · [xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/signing/bc/BcDerivedKeySignatureService.java](https://github.com/XRPLF/xrpl4j/blob/bbbd620b621491765dab54dd6bf14ae8ef3b901a/xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/signing/bc/BcDerivedKeySignatureService.java#L109) · line 109 · SHA-256 a4b9c8b0a5dc6d66593b4b051769fce3c0fef892902ad3e204c91de7862ce77e_

```
  108 |       new Ed25519Signer(),
  109 |       new ECDSASigner(new HMacDSAKCalculator(new SHA256Digest()))
  110 |     );
```

_file_excerpt · [xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/signing/bc/BcSignatureService.java](https://github.com/XRPLF/xrpl4j/blob/bbbd620b621491765dab54dd6bf14ae8ef3b901a/xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/signing/bc/BcSignatureService.java#L69) · line 69 · SHA-256 6b204bbc6149270cadb6b03174dbe3ccb2276002b8a48a81c2d20e2799472b9e_

```
   68 |       new Ed25519Signer(),
   69 |       new ECDSASigner(new HMacDSAKCalculator(new SHA256Digest()))
   70 |     );
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it; introduce an abstraction layer for crypto-agility.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-34920 — Quantum-vulnerable Ed25519: role not determined (2 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:Ed25519:general`
- Data source: xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/keys/Seed.java
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.8.1 · 2026-11-21 10:22 UTC
- Priority score: 31.7 / 100
- CVSS v3.1: not applicable

13 reference(s) to Ed25519 across 2 file(s), e.g. xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/keys/Seed.java:77. Role, judged from paths, function names and nearby code: role not determined. The code does not show what the keys protect; review decides the priority.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/keys/Seed.java:77 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/keys/Seed.java](https://github.com/XRPLF/xrpl4j/blob/bbbd620b621491765dab54dd6bf14ae8ef3b901a/xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/keys/Seed.java#L77) · line 77 · SHA-256 f90a9a34af56806cee9f51a5a24f7fe421457b7aa6dec312ac1d6d673193e5db_

```
   76 |    */
   77 |   static Seed ed25519SeedFromPassphrase(final Passphrase passphrase) {
   78 |     Objects.requireNonNull(passphrase);
```

_file_excerpt · [xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/keys/Seed.java](https://github.com/XRPLF/xrpl4j/blob/bbbd620b621491765dab54dd6bf14ae8ef3b901a/xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/keys/Seed.java#L87) · line 87 · SHA-256 8af5dc03399b00776b4966ed2a16c8c4c333799996cc8ffe20a72a7747ae964a_

```
   86 | 
   87 |     return ed25519SeedFromEntropy(Entropy.of(entropyBytes));
   88 |   }
```

_file_excerpt · [xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/keys/Seed.java](https://github.com/XRPLF/xrpl4j/blob/bbbd620b621491765dab54dd6bf14ae8ef3b901a/xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/keys/Seed.java#L139) · line 139 · SHA-256 fa50b7b6dd7edd264a8b19aa5dda5fbe7cfde9ab56fb73d58d619ce7e7a41234_

```
  138 |    */
  139 |   static Seed ed25519Seed() {
  140 |     return ed25519SeedFromEntropy(Entropy.newInstance());
```

_file_excerpt · [xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/keys/bc/BcKeyUtils.java](https://github.com/XRPLF/xrpl4j/blob/bbbd620b621491765dab54dd6bf14ae8ef3b901a/xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/keys/bc/BcKeyUtils.java#L84) · line 84 · SHA-256 10a94063c57c5c907b30fbcbb692d1e2abd2d1853dc711e5b077d72a53d1fb54_

```
   83 |    */
   84 |   public static PrivateKey toPrivateKey(final Ed25519PrivateKeyParameters ed25519PrivateKeyParameters) {
   85 |     Objects.requireNonNull(ed25519PrivateKeyParameters);
```

_file_excerpt · [xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/keys/bc/BcKeyUtils.java](https://github.com/XRPLF/xrpl4j/blob/bbbd620b621491765dab54dd6bf14ae8ef3b901a/xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/keys/bc/BcKeyUtils.java#L85) · line 85 · SHA-256 e10e35fb4eb319e50cedd936a83c47ed90dbe19eb0ed6dd5a13e7ca048c537be_

```
   84 |   public static PrivateKey toPrivateKey(final Ed25519PrivateKeyParameters ed25519PrivateKeyParameters) {
   85 |     Objects.requireNonNull(ed25519PrivateKeyParameters);
   86 | 
```

_file_excerpt · [xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/keys/bc/BcKeyUtils.java](https://github.com/XRPLF/xrpl4j/blob/bbbd620b621491765dab54dd6bf14ae8ef3b901a/xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/keys/bc/BcKeyUtils.java#L91) · line 91 · SHA-256 448eb309116056b4bb19e3d94ad540a3127b051783587a3aca725bfc69a60ecc_

```
   90 |     return PrivateKey.fromNaturalBytes(
   91 |       UnsignedByteArray.of(ed25519PrivateKeyParameters.getEncoded()), KeyType.ED25519
   92 |     );
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it; introduce an abstraction layer for crypto-agility.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-34917 — Quantum-vulnerable EC-ElGamal: key wrapping and data encryption at rest (4 file(s))

- Severity: **Low** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:EC-ElGamal:key_wrapping`
- Data source: xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/util/jna/JnaConfidentialCiphertextArithmetic.java
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.8.1 · 2026-11-21 10:22 UTC
- Priority score: 27.9 / 100
- CVSS v3.1: not applicable

18 reference(s) to EC-ElGamal across 4 file(s), e.g. xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/util/jna/JnaConfidentialCiphertextArithmetic.java:107. Role, judged from paths, function names and nearby code: key wrapping and data encryption at rest. Keys or data encrypted to these public keys are stored: anyone who copies them now decrypts them once a CRQC exists (harvest now, decrypt later).

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/util/jna/JnaConfidentialCiphertextArithmetic.java:107 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/util/jna/JnaConfidentialCiphertextArithmetic.java](https://github.com/XRPLF/xrpl4j/blob/bbbd620b621491765dab54dd6bf14ae8ef3b901a/xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/util/jna/JnaConfidentialCiphertextArithmetic.java#L107) · line 107 · SHA-256 6f66916f9d1c5bd5e3e898df0693fffaae9ba2950458ff32d44619b302e46d2f_

```
  106 |     try {
  107 |       if (!lib.mpt_make_ec_pair(leftBytes, leftC1, leftC2)) {
  108 |         throw new IllegalStateException("mpt_make_ec_pair failed to parse the left ciphertext");
```

_file_excerpt · [xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/util/jna/JnaConfidentialCiphertextArithmetic.java](https://github.com/XRPLF/xrpl4j/blob/bbbd620b621491765dab54dd6bf14ae8ef3b901a/xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/util/jna/JnaConfidentialCiphertextArithmetic.java#L108) · line 108 · SHA-256 7f6ffbce7fb6efa4b99831b8eb9caa914622c09871c94b1e3a1320b92224c630_

```
  107 |       if (!lib.mpt_make_ec_pair(leftBytes, leftC1, leftC2)) {
  108 |         throw new IllegalStateException("mpt_make_ec_pair failed to parse the left ciphertext");
  109 |       }
```

_file_excerpt · [xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/util/jna/JnaConfidentialCiphertextArithmetic.java](https://github.com/XRPLF/xrpl4j/blob/bbbd620b621491765dab54dd6bf14ae8ef3b901a/xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/util/jna/JnaConfidentialCiphertextArithmetic.java#L110) · line 110 · SHA-256 12536bb37616211c120b3352a8e956d8f77104acdf40f2f4cb9fb991f411b3eb_

```
  109 |       }
  110 |       if (!lib.mpt_make_ec_pair(rightBytes, rightC1, rightC2)) {
  111 |         throw new IllegalStateException("mpt_make_ec_pair failed to parse the right ciphertext");
```

_file_excerpt · [xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/util/jna/JnaMptAmountDecryptor.java](https://github.com/XRPLF/xrpl4j/blob/bbbd620b621491765dab54dd6bf14ae8ef3b901a/xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/util/jna/JnaMptAmountDecryptor.java#L105) · line 105 · SHA-256 4dbdd6478bc7da3f2bd4d41b22444e4bd1bf1499ed7c6b08f8f5f04e0199d44b_

```
  104 |       long[] outAmount = new long[1];
  105 |       int result = lib.mpt_decrypt_amount(
  106 |         ciphertextBytes, privateKeyBytes, outAmount, minAmount.longValue(), maxAmount.longValue()
```

_file_excerpt · [xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/util/jna/JnaMptAmountDecryptor.java](https://github.com/XRPLF/xrpl4j/blob/bbbd620b621491765dab54dd6bf14ae8ef3b901a/xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/util/jna/JnaMptAmountDecryptor.java#L109) · line 109 · SHA-256 ce4d8ed84a440d06ecb2d1fc22302690958e2296a3a0ffba40c7175983818211_

```
  108 |       if (result != 0) {
  109 |         throw new IllegalStateException("mpt_decrypt_amount failed with error code: " + result);
  110 |       }
```

_file_excerpt · [xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/util/jna/JnaMptAmountEncryptor.java](https://github.com/XRPLF/xrpl4j/blob/bbbd620b621491765dab54dd6bf14ae8ef3b901a/xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/util/jna/JnaMptAmountEncryptor.java#L97) · line 97 · SHA-256 04aec153ea68f8a6e19f55d542602f6970b084d73c3fc143866f7438d279ad60_

```
   96 |       byte[] outCiphertext = new byte[EncryptedAmount.LENGTH];
   97 |       int result = lib.mpt_encrypt_amount(amount.longValue(), publicKeyBytes, blindingBytes, outCiphertext);
   98 |       if (result != 0) {
```

_file_excerpt · [xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/util/jna/JnaMptAmountEncryptor.java](https://github.com/XRPLF/xrpl4j/blob/bbbd620b621491765dab54dd6bf14ae8ef3b901a/xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/util/jna/JnaMptAmountEncryptor.java#L99) · line 99 · SHA-256 58c439820c35a35beda4f6e61ffbedf3e9e0850f99abb12f81d4c88424d51afb_

```
   98 |       if (result != 0) {
   99 |         throw new IllegalStateException("mpt_encrypt_amount failed with error code: " + result);
  100 |       }
```

_file_excerpt · [xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/util/jna/MptCryptoLibrary.java](https://github.com/XRPLF/xrpl4j/blob/bbbd620b621491765dab54dd6bf14ae8ef3b901a/xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/util/jna/MptCryptoLibrary.java#L69) · line 69 · SHA-256 7fa6431699b5667214a4efd9078913bdf924600749913c52a9d988e816ec4b0f_

```
   68 |    */
   69 |   int mpt_encrypt_amount(long amount, byte[] publicKey, byte[] blindingFactor, byte[] outCiphertext);
   70 | 
```

_file_excerpt · [xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/util/jna/MptCryptoLibrary.java](https://github.com/XRPLF/xrpl4j/blob/bbbd620b621491765dab54dd6bf14ae8ef3b901a/xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/util/jna/MptCryptoLibrary.java#L86) · line 86 · SHA-256 ba71a8229ae3fe5c8a76ca407a89b49f579841053fbd63ac4f5f15b3ba0965cd_

```
   85 |    */
   86 |   int mpt_decrypt_amount(byte[] ciphertext, byte[] privateKey, long[] outAmount, long rangeLow, long rangeHigh);
   87 | 
```

_file_excerpt · [xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/util/jna/MptCryptoLibrary.java](https://github.com/XRPLF/xrpl4j/blob/bbbd620b621491765dab54dd6bf14ae8ef3b901a/xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/util/jna/MptCryptoLibrary.java#L136) · line 136 · SHA-256 bc655fc29473d2b7a701e946c20642fec4513c9a1db37369e04bd642e8dcd3da_

```
  135 |    */
  136 |   boolean mpt_make_ec_pair(byte[] buffer, Pointer out1, Pointer out2);
  137 | 
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Wrap keys with ML-KEM or a hybrid KEM (X25519 + ML-KEM-768) and re-wrap the stored keys; data that may already have been copied needs its own assessment.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-34923 — No post-quantum capable cryptographic library detected

- Severity: **Info** · Classification: Insufficient data · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `dependencies`
- Data source: dependency manifests
- Detection method: Dependency name matching.
- Analyzer: dependencies 1.8.1 · 2026-11-21 10:22 UTC
- Priority score: 12.2 / 100
- CVSS v3.1: not applicable

Across 6 dependency manifests, QSI found crypto libraries (org.bouncycastle:bcprov-jdk18on) but none from its PQC-capable list.

**Potential impact.** Readiness indicator only: PQC support may come from the platform (OpenSSL, OS, cloud KMS) rather than application dependencies.

**Reproduction steps.**

```
Review the dependency manifests listed in the evidence.
```

**Evidence.**

_dependency · pom.xml, xrpl4j-bom/pom.xml, xrpl4j-client/pom.xml, xrpl4j-core/pom.xml, xrpl4j-coverage/pom.xml, xrpl4j-mpt-crypto/pom.xml · SHA-256 ed23bf220f8e570503d83544d732bab69bf12e2d5e979d01f5dcb8772bdf2688_

```
Crypto libraries: org.bouncycastle:bcprov-jdk18on. PQC support depends on the version for: org.bouncycastle:bcprov-jdk18on
```

**Limitations of the check.** Absence of evidence is not evidence of absence: system libraries and transitive dependencies may not be listed.

**Recommendation.** Confirm where PQC support will come from (TLS terminator, KMS/HSM, library upgrade).

**Retest procedure.** Re-scan after upgrades.


## 8. Post-quantum assessment

| | Key establishment (x = how long data must stay confidential; harvest now, decrypt later) | Signatures (x = how long signatures/keys must stay trusted) |
|---|---|---|
| Data/key lifetime x | 5 | 10 |
| Migration time y | 5 | 5 |
| Assumed years to CRQC z | 12 (central) | 12 |
| x + y − z | -2 → tight margin | 3 → migration would finish too late under this scenario |
#### Where z comes from

Averaged expert likelihood that a CRQC exists within each horizon, from the annual survey published by the author of this inequality. Likelihood estimates, not predictions of a date.

| Within | Likelihood | The report's wording |
|---|---|---|
| 5 years | ~15% | averaged estimate |
| 10 years | 28-49% | quite possible |
| 15 years | 51-70% | likely |

**Why this scenario (central, z = 12):** Between the 10-year band (28-49%) and the 15-year band (51-70%): roughly where the experts' averaged likelihood crosses one half. More than half of the respondents (13 of 26) already put the likelihood at 50% or more for some horizon.
_Planning assumptions: x for key establishment, x for signatures, y are the defaults of the risk profile “Web3 project”, not the client's figures; with the client's actual lifetimes the verdict can change._

### Post-quantum maturity: Level 0 of 4 — no post-quantum cryptography

- Classical only — key wrapping and data encryption at rest: EC-ElGamal (4 file(s))
- Classical only — threshold signing and MPC protocols: Pedersen commitment (2 file(s))

**Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

_Levels: 0 none; 1 present, not wired; 2 in use outside the critical paths; 3 hybrid in a critical path; 4 post-quantum by default in the critical paths (root of trust, key wrapping, channel key exchange). Judged from code and manifests._

### What the quantum-vulnerable algorithms do

| Role | Algorithms (files) | ID | First step |
|---|---|---|---|
| **key wrapping and data encryption at rest** | EC-ElGamal (4) | QSI-2026-34917 | Wrap keys with ML-KEM or a hybrid KEM (X25519 + ML-KEM-768) and re-wrap the stored keys; data that may already have been copied needs its own assessment |
| **threshold signing and MPC protocols** | Pedersen commitment (2) | QSI-2026-34918 | Track post-quantum threshold signatures (NIST IR 8214C) and keep the protocol layer ready to swap the signature scheme; record which keys and shares must stay valid for how long |
| **transaction and message signing** | Ed25519 (2), ECDSA (1) | QSI-2026-34921, QSI-2026-34922 | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains adopt them |
| **role not determined** | ECDSA (5), Ed25519 (2) | QSI-2026-34919, QSI-2026-34920 | Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it; introduce an abstraction layer for crypto-agility |

_Roles are judged from file paths, function names and the code around each match; review confirms them. Root-of-trust keys and wrapped keys come first: they are hard to replace or can be recorded today._
No readiness questionnaire was completed for this project.

### Quantum algorithms relevant to this inventory

| Quantum algorithm | Effect | Attack model | Inventoried algorithms (rows) | What it means for this audit |
|---|---|---|---|---|
| Shor's algorithm — elliptic-curve discrete logarithms | breaks | Q1 | EC-ElGamal (4), ECDSA (6), Ed25519 (4), Pedersen commitment (2) | Elliptic-curve keys are expected to fall before RSA keys of comparable classical strength. On blockchains, coins whose public key is already on chain (reused addresses, pay-to-public-key and Taproot outputs) are exposed first; plan the move to post-quantum signatures and avoid key reuse in the meantime. |
| Grover's algorithm — key search and preimages | weakens (larger keys restore the margin) | Q1 | RIPEMD-160 (1), SHA-2 (3) | Not a break. 256-bit keys (AES-256, ChaCha20) keep a comfortable margin; AES-128 meets NIST category 1, while some authorities ask for 256-bit keys in quantum-resistant contexts (see the AES-128 entry). Prefer 256-bit keys for long-lived data; 256-bit hashes need no change for preimage resistance. |
| Brassard–Høyer–Tapp — collision search | weakens (larger keys restore the margin) | Q1 | RIPEMD-160 (1), SHA-2 (3) | 256-bit hashes (SHA-256, SHA3-256) remain adequate for collision resistance; 160-bit hashes are already weak classically (SHA-1 collisions are practical). Use 384/512-bit hashes where NIST categories 4–5 are required. |

_Effects: breaks — replace the algorithm; weakens — larger keys or outputs restore the margin; included in standard parameters — no action at standard parameter sets; only with superposition queries — not applicable to ordinary deployments._


## 9. Limitations and assumptions

- This report presents automated and documented analysis results for the stated scope. It is not a legal opinion, a certification or an attestation of compliance with any standard.
- z is a planning assumption chosen per risk profile, not a prediction. A cryptographically relevant quantum computer is not publicly known to exist today.

## 10. Remediation plan / Priorities for 30, 60 and 90 days

### 30 days

| Priority | ID | Action | Type | Closure criteria |
|---|---|---|---|---|
### 60 days

| Priority | ID | Action | Type | Closure criteria |
|---|---|---|---|---|
### 90 days

| Priority | ID | Action | Type | Closure criteria |
|---|---|---|---|---|
| P3 | QSI-2026-34918 | Add Pedersen commitment usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-34921 | Add Ed25519 usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-34922 | Add ECDSA usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-34919 | Add ECDSA usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-34920 | Add Ed25519 usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-34917 | Add EC-ElGamal usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P4 | QSI-2026-34918 | Plan migration of Pedersen commitment to  (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows  or a hybrid scheme in use. |
| P4 | QSI-2026-34921 | Plan migration of Ed25519 to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-34922 | Plan migration of ECDSA to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-34919 | Plan migration of ECDSA to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-34920 | Plan migration of Ed25519 to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-34917 | Plan migration of EC-ElGamal to NIST's post-quantum standards cover key encapsulation and signatures; none covers additively homomorphic encryption. Treat amounts encrypted this way as eventually public, and limit what a design must store on-ledger; lattice-based homomorphic schemes are the research direction (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows NIST's post-quantum standards cover key encapsulation and signatures; none covers additively homomorphic encryption. Treat amounts encrypted this way as eventually public, and limit what a design must store on-ledger; lattice-based homomorphic schemes are the research direction or a hybrid scheme in use. |

## 11. Tools used

- blockchain 1.0.0
- certificates 1.2.0
- chain_map 1.0.0
- configs 1.1.0
- crediting 1.1.0
- dependencies 1.4.3
- hndl 1.0.0
- inventory_document 1.1.0
- mpc 1.0.0
- solidity 1.5.2
- source_code 1.7.1
- tls_code 1.1.0
- tls_live 1.0.0
- ton_contracts 1.0.0
- validator_keys 1.2.0
- wallet_login 1.0.0
- qsi-engine 1.8.1
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
19. P. W. Shor — Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms on a Quantum Computer (SIAM J. Comput., 1997) — SIAM. <https://doi.org/10.1137/S0097539795293172> (peer-reviewed article)
20. R. Babbush et al. — Securing Elliptic Curve Cryptocurrencies against Quantum Vulnerabilities: Resource Estimates and Mitigations (arXiv:2603.28846) — arXiv. <https://arxiv.org/abs/2603.28846> (preprint (2026-03-30, v2 2026-04-15): 256-bit ECDLP with < 1200 logical qubits and < 90 M Toffoli gates (or < 1450 and < 70 M); < 500,000 physical qubits at 10^-3 error, minutes)
21. S. Jaques, M. Naehrig, M. Roetteler, F. Virdia — Implementing Grover oracles for quantum key search on AES and LowMC (EUROCRYPT 2020; arXiv:1910.01700) — Springer / arXiv. <https://arxiv.org/abs/1910.01700> (peer-reviewed article: lower cost estimates for the AES key searches that define the NIST categories)

## Appendices: Cryptographic inventory

By origin: dependency manifests 2 (0 Shor-breakable) · own code 20 (16 Shor-breakable).

| Algorithm | Parameter | Library | Location | Quantum status | Classical status |
|---|---|---|---|---|---|
| RIPEMD-160 | RIPEMD-160 |  | xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/keys/PublicKey.java:186 | weak classically | legacy |
| SHA-2 | SHA-256 |  | xrpl4j-core/src/main/java/org/xrpl/xrpl4j/codec/addresses/Utils.java:32 | Grover: acceptable to NIST, below ECCG/ANSSI guidance | acceptable |
| SHA-2 |  |  | xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/signing/bc/BcDerivedKeySignatureService.java:109 | Grover: acceptable to NIST, below ECCG/ANSSI guidance | acceptable |
| SHA-2 |  |  | xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/signing/bc/BcSignatureService.java:69 | Grover: acceptable to NIST, below ECCG/ANSSI guidance | acceptable |
| Crypto library | 1.86 | org.bouncycastle:bcprov-jdk18on (Bouncy Castle) | pom.xml | n/a | acceptable |
| Crypto library | unpinned | org.bouncycastle:bcprov-jdk18on (Bouncy Castle) | xrpl4j-core/pom.xml | n/a | acceptable |
| EC-ElGamal |  |  | xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/util/jna/JnaConfidentialCiphertextArithmetic.java:107 | vulnerable (Shor) | acceptable |
| EC-ElGamal |  |  | xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/util/jna/JnaMptAmountDecryptor.java:105 | vulnerable (Shor) | acceptable |
| EC-ElGamal |  |  | xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/util/jna/JnaMptAmountEncryptor.java:97 | vulnerable (Shor) | acceptable |
| EC-ElGamal |  |  | xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/util/jna/MptCryptoLibrary.java:69 | vulnerable (Shor) | acceptable |
| ECDSA | secp256k1 |  | xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/keys/PrivateKey.java:109 | vulnerable (Shor) | acceptable |
| ECDSA | secp256k1 |  | xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/keys/Seed.java:401 | vulnerable (Shor) | acceptable |
| ECDSA | secp256k1 |  | xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/keys/bc/BcKeyUtils.java:52 | vulnerable (Shor) | acceptable |
| ECDSA |  |  | xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/signing/bc/BcDerivedKeySignatureService.java:109 | vulnerable (Shor) | acceptable |
| ECDSA |  |  | xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/signing/bc/BcSignatureService.java:69 | vulnerable (Shor) | acceptable |
| ECDSA | secp256k1 |  | xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/signing/bc/Secp256k1.java:45 | vulnerable (Shor) | acceptable |
| Ed25519 | Ed25519 |  | xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/keys/Seed.java:77 | vulnerable (Shor) | acceptable |
| Ed25519 | Ed25519 |  | xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/keys/bc/BcKeyUtils.java:84 | vulnerable (Shor) | acceptable |
| Ed25519 | Ed25519 |  | xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/signing/bc/BcDerivedKeySignatureService.java:32 | vulnerable (Shor) | acceptable |
| Ed25519 | Ed25519 |  | xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/signing/bc/BcSignatureService.java:29 | vulnerable (Shor) | acceptable |
| Pedersen commitment |  |  | xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/util/jna/JnaPedersenCommitmentGenerator.java:75 | vulnerable (Shor) | acceptable |
| Pedersen commitment |  |  | xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/util/jna/MptCryptoLibrary.java:106 | vulnerable (Shor) | acceptable |

## Appendices: Input files

| File | Size | SHA-256 | Redactions |
|---|---|---|---|
| pom.xml | 23823 | `835fe6815b0d4c8e7d2ca4734a96202067f11e2781f13cfad486886f03544318` | 0 |
| xrpl4j-bom/pom.xml | 1227 | `ac087456ae398d39484f8a54f6ff373cbdc1814cf71db43eb378886c9c906eb3` | 0 |
| xrpl4j-client/pom.xml | 2498 | `1a5080b076af71d777f0a967ac8fbcf217e4f0e101df6c4feb0e277f811b4088` | 0 |
| xrpl4j-client/src/main/java/org/xrpl/xrpl4j/client/JsonRpcClient.java | 9798 | `6cc18abde6739e1493e14ddf507f1c4df744b74c57ec0048365ea0bf12aeb469` | 0 |
| xrpl4j-client/src/main/java/org/xrpl/xrpl4j/client/JsonRpcClientErrorException.java | 1135 | `1663e9da6af2306417ec13fb5d03133e3e9689c8a6463ce96a61fb690cc5cb46` | 0 |
| xrpl4j-client/src/main/java/org/xrpl/xrpl4j/client/JsonRpcRequest.java | 1888 | `9f9204e3975a329e948aa8a5f90428d294ff7fbc1f5daa0e55215dcf1d18a871` | 0 |
| xrpl4j-client/src/main/java/org/xrpl/xrpl4j/client/JsonRpcResponse.java | 1624 | `c505c28906ad45040019cd05385cc59343caeaabedc46fafc25e63fbf4ef538a` | 0 |
| xrpl4j-client/src/main/java/org/xrpl/xrpl4j/client/RetryStatusDecoder.java | 2509 | `f9d1cdb0cdd9f53a7d30c92628bb23b1d506f96916b6e35909d96804021b8789` | 0 |
| xrpl4j-client/src/main/java/org/xrpl/xrpl4j/client/XrplAdminClient.java | 2156 | `87b9e5f22aa59585386db774e9df249b1537663d3924b14f95b359dd4e7299ba` | 0 |
| xrpl4j-client/src/main/java/org/xrpl/xrpl4j/client/XrplClient.java | 41408 | `648301a73be47768f3b863358b5cafd6eb9c05632a157b9d23dae9af6a2b2bad` | 0 |
| xrpl4j-client/src/main/java/org/xrpl/xrpl4j/client/faucet/FaucetAccount.java | 2020 | `4caab177b6c8d93140ab8a54c65ce273350a13b6965ccee670a9e215319b31da` | 0 |
| xrpl4j-client/src/main/java/org/xrpl/xrpl4j/client/faucet/FaucetAccountResponse.java | 1802 | `0e7c123fb4f446e6b72b5369afdf92273caf02c0c202cbb2ff2232f35b9f7db8` | 0 |
| xrpl4j-client/src/main/java/org/xrpl/xrpl4j/client/faucet/FaucetClient.java | 2768 | `530f52616784962f264bc658847d21ab3b1c38490054ef1d168b0a6b2bb42c87` | 0 |
| xrpl4j-client/src/main/java/org/xrpl/xrpl4j/client/faucet/FundAccountRequest.java | 1918 | `4047a506c3b8be4239bee5eca5def824b0eea19f61eefa6e584ab3923cf28626` | 0 |
| xrpl4j-core/pom.xml | 3832 | `53015ed9cb4f847e67a26e83501c78d7d39a6f3af2e9b4b66e9c8ae1bcb16c6f` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/codec/addresses/AddressBase58.java | 7331 | `1e1e8bc7dc82b7513db4b5783a7ba86432dbc1f07bb16e9947540f000361cedf` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/codec/addresses/AddressCodec.java | 11699 | `befac5ffa2d1362d46edb74802ddeb3219af2b3f7e81b85a042947db6518674f` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/codec/addresses/Base58.java | 6437 | `4564689ad7e8050a87c9231d8ac754ce3df91732828e21a62c4f8edec61d19ec` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/codec/addresses/ByteUtils.java | 5777 | `ca98b29fd3cd4cb30e17f0a25418d1da6d02bc8e83388b8b56207b89dc4728a0` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/codec/addresses/ClassicAddress.java | 2044 | `ab60da049013dfa750b88de69d1ee73137886c428385c03f7fcfffd38528b987` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/codec/addresses/Decoded.java | 1680 | `131faa1c785b5000b6b685d24de2e26fa7edf14dd6d695e38ec3a86b4f0afe7b` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/codec/addresses/DecodedXAddress.java | 1913 | `5e46c44005f83114cfed0ea4dd46c05539918401577fa5c69dd5e549f7ce8873` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/codec/addresses/KeyType.java | 911 | `0b08ac0292e12453e7248284078957e115f62de724aa47a05e7424499a84db68` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/codec/addresses/PrivateKeyCodec.java | 3456 | `b9e91bc861772b74f07c6630b0e27037575cda53f9eefac0e66b4e195f39556f` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/codec/addresses/PublicKeyCodec.java | 3326 | `609c76e1c3666f01a3804538e7946afa20fbd8c05b1b944a112b27dcf3a94e5b` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/codec/addresses/SeedCodec.java | 5266 | `835a6cfc58b48fdb7e9ed88509c01360061608e060a8677e907bea2500b16eb2` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/codec/addresses/UnsignedByte.java | 5748 | `b303224e91d6661399df5c9853ef221ca125e570f8e366e7a0c6821ce71f3245` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/codec/addresses/UnsignedByteArray.java | 8275 | `8f182bda6a7f73a9e80673e7c119f414dc2e4339fb33941c6e4d7849bdf10b9a` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/codec/addresses/Utils.java | 2197 | `4210e94c753d2bcd8e55ddf39c51c05bfb57db588d18d4b70db32338293fef9e` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/codec/addresses/Version.java | 1646 | `4f81532241e9022142f85d5edd8f88405fb61bcead9f31cc646cb0357d530c5e` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/codec/addresses/exceptions/DecodeException.java | 998 | `02b0f6ea727f854f92c4dc4d2ae9cffcec6a1bc53136acba8127f417aedc02cb` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/codec/addresses/exceptions/EncodeException.java | 998 | `dd1dd7da57ea97fd4392814556032d4b7b21c533dd82b9c2fe274744c536d5b3` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/codec/addresses/exceptions/EncodingFormatException.java | 1069 | `a26728cf3ce7130651a496fbef0355b864f81f018f6fb32b5d796b01a9de93da` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/codec/binary/BinaryCodecObjectMapperFactory.java | 2167 | `09d65a15bfc02db0e900861788b73d3b4a211bd866f3e3eb799811f4785c7bab` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/codec/binary/FieldHeader.java | 1401 | `1df010c5b089c780140e20b04e37d4c9b1fa7212ee97df92313c0fce18bc6be4` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/codec/binary/FieldHeaderCodec.java | 5961 | `71f145302653ed478b519ae00b821981005091e6d87f45543047e42395e59b65` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/codec/binary/XrplBinaryCodec.java | 23222 | `63c78e06c5e3fff85f884ef4c68216b1a685484fc6dde13ced16a397c1a0bcc8` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/codec/binary/definitions/DefaultDefinitionsProvider.java | 4209 | `084b723c5394fb398b126c0a779d86f5537e657ac1c963b8e0a55bb785c8225e` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/codec/binary/definitions/Definitions.java | 4739 | `b781bf2a063ede8144e8b3c3b4e58ff164df46dcc45c49980afbdfef9cb98f67` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/codec/binary/definitions/DefinitionsProvider.java | 1280 | `0bca64a3ef30e83694c178f1e235e4d56760f209a7115ad5f3061ed0f2bfba60` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/codec/binary/definitions/DefinitionsService.java | 8886 | `8f1a43d0c0d71f854b6230625cb72b3f6f0b81fa5893eecb021ff2cd89ce00ec` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/codec/binary/definitions/FieldFormat.java | 1723 | `668628dbe1ab1798e7b3bfd07dd6d769e9781b8d6a5e7e09e899844cbbfca721` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/codec/binary/definitions/FieldInfo.java | 2114 | `bf61a44f0a8da8bb70861640cbb2119f3a7819ed878e0645c20e8074c9970a7a` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/codec/binary/definitions/FieldInstance.java | 2908 | `5d4572b874fc9d4885740c92b780d7d45912578bb2379895c0189720e2da9751` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/codec/binary/math/MathUtils.java | 2903 | `228bc2e20c1963ebc025df2d470c98e790d28d967ab1fd7b5c030cd88b23bcaa` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/codec/binary/serdes/BinaryParser.java | 7568 | `47a4ee6b8e907e3c87c57e29ad853babd50f57084542f6e2021287f70b5f95dc` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/codec/binary/serdes/BinarySerializer.java | 4300 | `97a9657580fd72f482e3add47d9e11ffb55f366c11d345c098b3117ce966044e` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/codec/binary/types/AccountIdType.java | 2113 | `d14ae8abd91b7521a35343ca7e835ba7bb98bb52c54f5e7195003da9ec4c2de3` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/codec/binary/types/Amount.java | 1358 | `d6ebda1381e575355545bcf75b89982e78adf3221e9e9ac5c42f73dd69549bed` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/codec/binary/types/AmountType.java | 12737 | `ac5c5835620f0a24a8d148e0facad0c0f4f79ce5f810e9c99045d78099ed0f0b` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/codec/binary/types/BlobType.java | 1518 | `fa615298a81a0b7710f88094b8b881dbeda957b0b35e01906d9112cb4f91a86b` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/codec/binary/types/CurrencyType.java | 4863 | `deba2599ad0899e206e96638d4a6325c2cdcfa091365faca638af227685c3cdf` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/codec/binary/types/FieldWithValue.java | 1385 | `08edfffa2ad9f0caab47b6b50ae20fd6bf55a440ab238a01ba4d46782b1b629b` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/codec/binary/types/Hash128Type.java | 1569 | `f6a8acbb8bbb2a33e3db94ad71fda698f5d5ddf8bfcf33f1a3b6f49be35fc423` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/codec/binary/types/Hash160Type.java | 1682 | `bdd51bf082ef6cb9a549c4d8aef4b9f2b964211c1b3a999bb4f12ff39caf22fd` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/codec/binary/types/Hash256Type.java | 1569 | `fcbd234b3e6e6e00f1f35d9ce96bb0c9e322926880b9679dcbb8978bc0620806` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/codec/binary/types/HashType.java | 2169 | `a1facfc9b3ec089d8b5425e76ab5bd84047d0a1d04048214fc4d23e036a48fd1` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/codec/binary/types/Hop.java | 1492 | `97427b23cd1407cf69fb6ff45f87601f20edd8fab13a07acc7d1fe46b0a16d95` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/codec/binary/types/HopType.java | 3882 | `ff827a4023cbf3534acd5ff32b783e9c8bb7b32b08f5d81d5b25a093ee032f51` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/codec/binary/types/Int32Type.java | 2494 | `a84db9c542d25d54a6be9832c6476c6ac0edef1e9024668080ea1ba333d77acc` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/codec/binary/types/Issue.java | 2080 | `139f66c5cd4ce47f4a9aa8f7f6ba61e8c39d951f8e4cd39a5ffee7c3e6bef79f` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/codec/binary/types/IssueType.java | 4520 | `4cabbcea531bbfdb378cb37db8e120360b263d36b7b85de416ff8267a843a8e7` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/codec/binary/types/NumberType.java | 7548 | `65bbfb563452029ec7c4d844801213d9796a78bbd8b9125b092cf8a0ea01fa15` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/codec/binary/types/PathSetType.java | 3223 | `7b556e94e87767f2a3895fe08167d2a9cd3ca46a47a02acc0fa8378a019ea4c8` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/codec/binary/types/PathType.java | 2975 | `9e5e93dbb2122f850cab27c8dc8972bec256976bacd86c9aab643490eb04e947` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/codec/binary/types/STArrayType.java | 3995 | `c9dc3ef1c54dab18b9b86c32e9c2ce99977947abec8e39f13dc3f5ba1df497fc` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/codec/binary/types/STObjectType.java | 7302 | `4498506368d56a4e37537104f57ab7538c618c66f0cbcf29e7093e22afd6c94e` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/codec/binary/types/SerializedType.java | 9176 | `0142e799920dbea708e9e269099f6ab6a60fed0541443f0c75ea201727b5f943` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/codec/binary/types/UInt16Type.java | 1660 | `f4717710701f1a97321e1520d816d2f860734cefb19d3b437a3e0ecd60a4ea5f` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/codec/binary/types/UInt192Type.java | 911 | `66b3662ce24687840b5f3120de9f3a47b12fa1ef2bf98efca47ac6f29fa9c2a7` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/codec/binary/types/UInt32Type.java | 1662 | `1828f3561c00abf5949dcf75eabe64f42040a95ab58c4305b9e025f91a8fe1b2` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/codec/binary/types/UInt64Type.java | 3305 | `0521b7cecf12601a891a667363ba09792449e2dcaff25d161bad3d13ede6fd9d` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/codec/binary/types/UInt8Type.java | 1649 | `6130d440883a20e97d160626704fb0c8aa8fb65a0991abe55d4353b70e3b3f33` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/codec/binary/types/UIntType.java | 1990 | `773f69eeeb6feeb81b2cd622b84ea4ea16b0ce8de9a24a2c43e8051b7fbc71e0` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/codec/binary/types/Vector256Type.java | 2917 | `7f431f217c960cd9fac1fa6c2d9bc34d27e3fc3580c35cfa1e6e641fc445329c` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/codec/binary/types/XChainBridge.java | 1845 | `94619dad803000c7b16d8b27293b6c0262dd2b7e66fafbac7d25a6edf42fe8f2` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/codec/binary/types/XChainBridgeType.java | 4536 | `713e8ed0633f5dd46d60457c9d5842fcce5a4d82a4d5bd62649adaffde3157f5` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/HashingUtils.java | 2818 | `6c92e8be13c15f231d18ccda4ef9b60935619c500801318fcfbb289deef7e5d4` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/JavaKeystoreLoader.java | 2424 | `71f4f59af46a231ef021f33610996dadbaceb4d92619f727a494cc05267dde86` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/LinuxSecureRandom.java | 4596 | `0ddf0ac071222e3dcf37f343c20f457a560b68a87dd2b8defad1728367df7d1d` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/SecureRandomUtils.java | 2662 | `823fae5e8a2dd4b724b63288f80dc9040f48ccdffe258c950f5fe594911e09dd` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/ServerSecret.java | 3596 | `1f790828bf396213371fbac68683640d0b5563eaa67084d5840bd972a29e3c03` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/ServerSecretSupplier.java | 1770 | `bf9bb8c712b9ea573c71a7c0acca1576989cbe5dda6e48aa89e461c2d3b3f490` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/ConfidentialBatchInner.java | 3512 | `f04eddb220a9cc46b6340bb388d60c4977a738c35d86d2e759a1c7413995c274` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/ConfidentialBatchRequest.java | 4791 | `76bbe9f0cc3da02de8f39b55ed1e3761064bd1c25e8a89bc080af9f17f3dd0af` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/ConfidentialClawbackOp.java | 2021 | `9d0e52e66ef3b10a6f58f305bdd39ceeb4f3581f30c9f9db1f24a47869ad2e29` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/ConfidentialConvertBackOp.java | 1828 | `6ec72b51262c3c6e0787a9a1efd3bbe437d1d7de9a00242fbb0508cad888e226` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/ConfidentialConvertOp.java | 2667 | `b37a76ee6a660eff3b7ffe39333e4173d1c70bdd9d2d755f31bde047cc742fb3` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/ConfidentialMergeInboxOp.java | 1454 | `8ccb6936f39e8398a96dbc534ec7b442df6f77fd141cb46497a826f2aa172ffc` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/ConfidentialMptBatchAssembler.java | 39767 | `18706f8688ba93f77500a86845b93f72b428848ee49bc2071e8bd17bef56d1c4` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/ConfidentialMptClawbackService.java | 6328 | `bb2a5eb1b6d9da765ca98cb2fd99c5ee4024b6af9062e309171a41ac82768954` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/ConfidentialMptConvertBackService.java | 8626 | `3f10e3ddd7fb36021807a960c4b4ba2a2670f7f313488151058ef93ef9a11f1a` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/ConfidentialMptConvertService.java | 5195 | `c37bf555c36a5dbd0dbbe430d0c0a2231266bc428a9ff1a392e28da96d22e75e` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/ConfidentialMptOp.java | 5613 | `c0800f74fa6a6ab4b7616f63143517a3fca44e878d1a444171943163b83d10fd` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/ConfidentialMptSendService.java | 9643 | `f107018543997beb26df897ceb26a678fd87e7e819ce3d80fd0a069d7d979608` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/ConfidentialSendOp.java | 2027 | `f7abfd96a8003fcdd9d13e02e60a481f2c4e06454fe70969fd7f0c0b5432cb3e` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/model/BlindingFactor.java | 6156 | `83c9894ded3967ca8eb91f165c74601b8408d2c56dea5d0881e5d9722869092d` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/model/Commitment.java | 3668 | `5bd67ec44401f19dca1826dbf2704a8c5e25e22c7b1b8ae442579cf78edd1ca6` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/model/ConfidentialIssuanceInfo.java | 2478 | `34e4609e88b2b9c55b009eaa97d65113df0955bbc0ea609c4c8dab103e2591e6` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/model/ConfidentialTokenState.java | 4686 | `e4adca1ec0b271ee742ba34a722331857904e59a1fcced618253329f403c4a3a` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/model/EncryptedAmount.java | 3858 | `ccbf4b789cb6759ac4d2dc59f8d029e433af9b809205ccdc87d0b80a8d470cf5` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/model/MptConfidentialParty.java | 2934 | `06ff4210d6b706ac8541d01d390f18b1cff80bfacc007b1d688516e71a06b638` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/model/PedersenProofParams.java | 2902 | `edbaef8468883bbe82476d3a358127b139f20ebe7dbbda1b50348853f50e9bb9` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/model/SecretBlindingFactor.java | 7991 | `50ab27b7dc44ff72857d99fe6acbf0d2d972efe18dbd83bfd435344e1d6ee376` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/model/context/ConfidentialMptClawbackContext.java | 3626 | `baef3000951caf9c24382bad24e30678984fc0465f948add369adc1622bbe4f2` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/model/context/ConfidentialMptConvertBackContext.java | 3662 | `f07a446852afc6d5054c281f88474f5410d611b296443a05cfbe5d55dbfa36a3` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/model/context/ConfidentialMptConvertContext.java | 3614 | `03d02a9e29610bbf5bcac6f84da356d6c9320c67b85e8915466ad2d67eeb4e24` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/model/context/ConfidentialMptSendContext.java | 3578 | `a445c1a1b9539531a16fe17c24aaf79f06fbe8b90343c3a5db7386247d87fa90` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/model/proof/ConfidentialMptClawbackProof.java | 3733 | `f86beb4a1d3faee3b437821615ffd2da3c19f21a9ba9bd1ef8d5afa2d9488045` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/model/proof/ConfidentialMptConvertBackProof.java | 3993 | `0169e88d1e595e41c999c55a414e4b0830eba5e7d872d2a2161c22bdbfd71540` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/model/proof/ConfidentialMptConvertProof.java | 3677 | `4f3ff53ee1b721b582614c19ee0a3b5a2352d0c0f7583a14639e9e6399dc37ad` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/model/proof/ConfidentialMptSendProof.java | 3919 | `9b8e8629496df34a13e0a26c928ea11448ddadece954df75a6259aac72c45b7a` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/util/BlindingFactorGenerator.java | 1780 | `19a9865ab50e50aec74713de893781d4896149c96bc90a26c574817e8f192ff4` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/util/ConfidentialCiphertextArithmetic.java | 3277 | `4d63d36819dd21ede3dafaad96fedc1c276c5e1bfbf0a7605def7d427f3ea85d` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/util/ConfidentialMptClawbackProofGenerator.java | 3060 | `ca47c86e5ae75bfcd42c1a099489d03ebfe23e4c3e76afe677adb5dc17e7b0c2` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/util/ConfidentialMptClawbackProofVerifier.java | 2431 | `c17cce38c543390ed2a90e2eceed94218f5322806662839a668cfe0ce4671f0f` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/util/ConfidentialMptConvertBackProofGenerator.java | 2600 | `64283be66ec611b148fc2db7e4598bf272bb4cd0f6b2ae5cdd91afe0feb11f1e` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/util/ConfidentialMptConvertBackProofVerifier.java | 2377 | `d07e8a0165fb6f448222f3cc0e5539b265b01a675c0e005ab910033a2a847239` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/util/ConfidentialMptConvertProofGenerator.java | 2391 | `6f4c94448360b73244f1bfb39c66e165e71c3adf63526b4d3b4d54b6df722003` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/util/ConfidentialMptConvertProofVerifier.java | 2091 | `694bb352dcbf23e3bfcdbb9adcb3db15af6b50bea4ba39c11b5db3184df47d8d` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/util/ConfidentialMptSendProofGenerator.java | 3427 | `8dbc7245d9a11ab463fc597ac465244ad9ac4cd7e46518bda53da02e6e6cfb87` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/util/ConfidentialMptSendProofVerifier.java | 3012 | `2ebd0bd757fe1e1b0815977cd62e50df3ba17f0c43cb26b7a539d3658b2547f7` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/util/ContextHashGenerator.java | 4062 | `43b9978b14c4f8e5b459acea33bcceb236e57f8e9513138259b3df3f78cc5267` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/util/MptAmountDecryptor.java | 2657 | `1190b4b87bd4b29d8ca9a16ecc45c157fc232fe7d6ea9024fb03abeb51d0eb5e` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/util/MptAmountEncryptor.java | 3392 | `cc7e5263d9a95e5f7dd87a36fc2f5dbfa472048f3fa462e9f3d747aec7066ca5` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/util/PedersenCommitmentGenerator.java | 2162 | `372b885d05c0d6ddb1a4cad05a234c9a53f2cd4149a9545de6d4fb69bb65b9ce` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/util/jna/JnaBlindingFactorGenerator.java | 2881 | `e1f89c9a4beed9590013d413ecdb776f8c3433fc76ffeca79b07a2ec61bc2e36` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/util/jna/JnaConfidentialCiphertextArithmetic.java | 5514 | `dfb1fcd004d44a35f7c3309a3915276478a3d9301aaf2f1881fd26f0ae1971a9` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/util/jna/JnaConfidentialMptClawbackProofGenerator.java | 4826 | `99d1574484f5029ef9694352d7f40ab72d89842769d3c3445d3b4ee3908540b6` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/util/jna/JnaConfidentialMptClawbackProofVerifier.java | 3741 | `df5333303d56548227bc8adae25eb940e87aa51cc3293d3e42eef3099f4c14ed` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/util/jna/JnaConfidentialMptConvertBackProofGenerator.java | 6353 | `69938936f25afd4f0b8df9a19d466cc16d7c4ae9fe25cf6683a780a80009be23` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/util/jna/JnaConfidentialMptConvertBackProofVerifier.java | 3964 | `8b980536647ffc36b222c7fbeee5704f1ed24f32e84ae476f1d6b19c0c69c1f8` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/util/jna/JnaConfidentialMptConvertProofGenerator.java | 4177 | `03665858a4d2e36ac02a95621e3cbc98c21530cf4ded8aa2809114a2da5e7001` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/util/jna/JnaConfidentialMptConvertProofVerifier.java | 3194 | `d46785e68f0d59db8e05fa4dbe3d44b73d1a5117f621d765410709f5ff33defb` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/util/jna/JnaConfidentialMptSendProofGenerator.java | 9767 | `4a5493fabee8dde2702063618cabefb3c2054ab50e8f3674399da2ab959eeb6f` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/util/jna/JnaConfidentialMptSendProofVerifier.java | 5256 | `4597359d77c0f559a78fa4983311b521da6b074c81290889470f5687392fc898` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/util/jna/JnaContextHashGenerator.java | 8428 | `6d65175f78f5164aad3914f8b06da9020fa640c1ca55e35a6609a3004dc76baf` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/util/jna/JnaMptAmountDecryptor.java | 4247 | `bcfc24feb98f2bb0ac76dd38e2b5a8b9ab7089fb3f4a348aeb7e9fb5d3c32302` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/util/jna/JnaMptAmountEncryptor.java | 3937 | `91e20c641d8d2f467494ac09239da1c4bc18322f75988463d13d5266b1b9140a` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/util/jna/JnaPedersenCommitmentGenerator.java | 3316 | `5dc5f00ea3642d8e5d930054e5983915b44248547eaed5fb73ed99e31d3b5290` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/confidential/util/jna/MptCryptoLibrary.java | 21263 | `db8dde34e0bf364b6ac3abc2fe076cc4413388ff1ad3d98eff4c514e8be0cdde` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/keys/Base58EncodedSecret.java | 2205 | `816cad04323203fce83432aec5a15068b96118145ce76b5e3b3a1d14386fe48d` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/keys/Entropy.java | 3868 | `fc6cf827206147c90b06a493fdde58c18bbf24fb5a291d1955b59198b70fa57e` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/keys/KeyPair.java | 1470 | `64b9f7339693cb296a6d26a1f02eda8ad4feae8e814efacf4ddab7a208c8d8f1` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/keys/Passphrase.java | 3158 | `b7835508021cf35bf56b9c8cc0de57afd51e808159677f44c03db50ae15d905c` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/keys/PrivateKey.java | 11149 | `c1f0995ac729066a9f562faa488f754ff1a65814d159d83a6db17d6cd84c9a00` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/keys/PrivateKeyReference.java | 1118 | `fd17ee9770f59645b1a36b32d1ff13f44397eb91a90f6953a5826d6fa302a942` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/keys/PrivateKeyable.java | 1096 | `c421573637ea3cd7e2f53f774dabf87fdf2aba3110d69c17ad417046440a08c7` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/keys/PublicKey.java | 6584 | `5bc666fa64c2db4f74b42e6f4d5c84e0086cbf5b131a16f698bfa164bd6e6099` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/keys/Seed.java | 20405 | `7104b074ff8095cd47a0d09a59e4883348beafc1805860f99b3e26be39d369c3` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/keys/bc/BcKeyUtils.java | 9641 | `d215b119585134744235543879d2578a6c71a0f5b9b0ceffee6aef1ccc213482` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/signing/AbstractSignatureService.java | 8687 | `94fcdd589d61aab24325974dd0516e5b9793d03f683e7bee678222e258f7fafa` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/signing/AbstractTransactionSigner.java | 11593 | `ec379a798932473bf882479be212e01be1f397f6be930981d06fc0e630e2072d` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/signing/AbstractTransactionVerifier.java | 5700 | `4436b289eb40c282f30815f916a8e143b8de8270f1570e0c6f299dc2f662c3cb` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/signing/MultiSignedTransaction.java | 4442 | `5f9e0c30016714d1bab0bc154257fddc90599eaa3bddd9eb74b1236f394369ae` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/signing/Signature.java | 3033 | `926cf587a5aa43f1266c9aa652f2dfb367a17dc22910788cf8778ff175a565bb` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/signing/SignatureService.java | 1132 | `9ebb5932f02ea7afdd9dbacd76d6b9004ecc3b95bb7b41c334cfb71d4beae460` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/signing/SignatureUtils.java | 13250 | `b3a4668b5cdf0de82474a33b120b1cf509362d60149ed5e2b4118126f354b491` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/signing/SignedTransaction.java | 3319 | `881d517cfa999b7f0805a4726d8329b6d9e0b0767bcb8e8c0fc4eb57f629d23a` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/signing/SingleSignedTransaction.java | 3181 | `c9d88b2d43e673db3e03830e1297d14c1708644069a0b3fc1d476bcced293c11` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/signing/TransactionSigner.java | 14351 | `ac01e6dd36d3a55224fdf38880b9453a0681e1c0ea0466e1d0dc389c8dfbc198` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/signing/TransactionVerifier.java | 3751 | `81c5914a36d91ee5cd8c5dcde2d827eb72f55742659f0bc0d7f5c7720f2a0f89` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/signing/bc/BcDerivedKeySignatureService.java | 17925 | `da9f81682a3691be8e63cbbc4df0887e58676acbc153eb1da8d14f482613915c` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/signing/bc/BcSignatureService.java | 6963 | `5cb063fd7185fc5870359ee0e1288ee00bb7cc10496d70ab270bdf24b1e38a83` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/signing/bc/EcDsaSignature.java | 5936 | `67807d0668760495bb55a063ea3bb3e1e75d02d5c6c06c533222db60249fc92d` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/crypto/signing/bc/Secp256k1.java | 7742 | `f731f164fe630f9ecac40a9fa0cc7286041315067e8d030b5bc1136babe51fdd` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/AddressConstants.java | 2666 | `570d44ed8f281dfbd3da000c72b1c01bbb2b624490bd99758e11496d2a04de03` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/Finality.java | 2488 | `f9831cef3eb5c5879c84be11785e7ee96fc15269b7b96ca0fe189b8231cef9e1` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/FinalityStatus.java | 2502 | `edcdad8f575b20a6727ed4bc2173915da1e9777d662d773e866f5c55bafb6ff5` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/XrplMethods.java | 8619 | `3f1e46fbb9f8d609833c67047ad1d865d490a559f1c234c5012cecdf6bb0cd0e` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/XrplRequestParams.java | 954 | `5570315469c5b893ec97529d2539c99ef69e19aaa267b620f6b9dcc7481c44e3` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/XrplResult.java | 1240 | `290cb12d452e41743f097fe9eb3bb579901152791793b6d0d23ded9ea29565af` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/accounts/AccountChannelsRequestParams.java | 3274 | `8a34470fcb964c88eb8a282e170ba31e8bb3fd65c316c11713a14b1f8af6b41d` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/accounts/AccountChannelsResult.java | 5645 | `099efc3ee6add9e26d88404c56568185d5a59c3a22a4ca53e99603b927d757de` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/accounts/AccountCurrenciesRequestParams.java | 2730 | `6bda716a905a072f94618563988c61cfe9210b2463c6dc3dcbe385e6a50d0c1a` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/accounts/AccountCurrenciesResult.java | 4818 | `dced2babe2fb490df1b8619b6ad5a7a5ec4386677f5116d3668dfc82d45d79d6` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/accounts/AccountInfoRequestParams.java | 4102 | `3b487962eddb3780882070794223f32ae3700721aadfa917b7b83e07eae58311` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/accounts/AccountInfoResult.java | 4566 | `f552e4f6ab34b1dcb9dc88605f923fc989e93240a8272ff2292f13518ba4b285` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/accounts/AccountLinesRequestParams.java | 3122 | `a68697ff6a810c4f8873cc7807bc00f1b08424161f312c1b6163cf74f35a93c8` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/accounts/AccountLinesResult.java | 4951 | `b15e9bdabc3eba8b21c8504c0e9865f4c9e4353a544397e234237405070bd2f1` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/accounts/AccountNftsRequestParams.java | 2468 | `4d3fbec11241352ee07f685ec8b6374fd469da6de727f2d1aa210c062da2c422` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/accounts/AccountNftsResult.java | 5586 | `f1115bee934510883e169256b40985813634eb7116f20d204887bc9fcf273243` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/accounts/AccountObjectsRequestParams.java | 6863 | `c2ce9bd79512d7673ac1e7df1aeece3484ac67e7306b6fc59a2a31db4af3d8f5` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/accounts/AccountObjectsResult.java | 5665 | `b3d4185dae43b11abd76fb95861904b552659097011872db3192d7d8f294f41b` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/accounts/AccountOffersRequestParams.java | 3282 | `586984518775e98f7da4fb037c99d9508f3fd2c0ed763beeabb9ce5ffe964add` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/accounts/AccountOffersResult.java | 4824 | `e95ddfbea9de95634950657f3df22353f8eda258369d3d77e14d6983ebe5a22c` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/accounts/AccountSponsoringRequestParams.java | 4632 | `fe9c24da9e2b6169c36e8a5d70ab0d6000bacd610b588bbf423f82c509e89d80` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/accounts/AccountSponsoringResult.java | 4127 | `1c1c2acbf2c947d5eebc755b24e5514712d4ed5fbb2306c21c9d0129295d2b66` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/accounts/AccountTransactionsRequestParams.java | 8169 | `0e8f1c9ec5ce8453e204b4d9c58fb2bad4d3d197e5b7cb605c03277aef1dbb09` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/accounts/AccountTransactionsResult.java | 3707 | `530d822c80861e315971acd367774aa5257756c7bf8477b6113c9497456c5d13` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/accounts/AccountTransactionsTransaction.java | 3560 | `5fef599861ae3c5c787f7654625731ce05f024e82e7ba3af9071602683fa5bdd` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/accounts/AccountTransactionsTransactionResult.java | 3016 | `a1eaf9249728c0ad1f69e49c67f37b4f9c995c9a2027d2c9cbbc6060d4f14df6` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/accounts/GatewayBalancesAssets.java | 2244 | `a8328fd811b88d4d0708964d25f5e67b4335646ee2750ce7b84cdebaa978991a` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/accounts/GatewayBalancesHotWallets.java | 2297 | `1e8e518008b26ab4fae4cb24b7d31cfa5c785419b2f59d2f043d6732aca47115` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/accounts/GatewayBalancesIssuedCurrencyAmount.java | 2891 | `88f31611ed405ff01a76b6b2f6c709374bc31de8960b4d84c5d91bdf90c45c72` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/accounts/GatewayBalancesObligations.java | 2150 | `294eb55cdfc41cb9c4b5dd5976563a4a0d614caff4a827eff4a0501c0e4080d3` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/accounts/GatewayBalancesRequestParams.java | 3328 | `8f72d89c94f779bfcdf99a3ac98466462058006f8a8d3f30da05567e8edcd5a9` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/accounts/GatewayBalancesResult.java | 6427 | `5c444fd9dcc9e5e26dbe113c4c30398b1a49fa59a10aeecd7379829348d25f5f` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/accounts/NfTokenObject.java | 3388 | `ed70dc6de893e51aeda331f28e582a6a89ec32115721305295c8b64c7978e734` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/accounts/OfferResultObject.java | 3339 | `d3e7af1c418af36d3f2e813492aef5ff1d5fb14e281a46728f62fe54185e19e1` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/accounts/PaymentChannelResultObject.java | 6068 | `eb6888242ef4cc1358fe4d75bd0d51147231ca4acb0248567891758e5c9f6768` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/accounts/QueueData.java | 3715 | `df271562805d2e75f1ecacccb3afd82866728530f9f0d6f4e174395a8ee73445` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/accounts/QueueTransaction.java | 2957 | `ff8502036e6f8859d7c43e26d3549478508e28adaf4cf10722b03835132e1e84` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/accounts/TrustLine.java | 6064 | `e96cd16bd9f39d0aa3493727bf4cfafae10d84e24cb1c5d258b375f1083aa7a8` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/admin/AcceptLedgerResult.java | 1906 | `01a8bc0f9592e74c64238c1cbffaf6f1f772800ce4a562227d17cb175103be3f` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/amm/AmmInfo.java | 3558 | `f89e6b0fc080281c672bf581b7316af3e5e80db3e05e128798c8cc1bf176be7d` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/amm/AmmInfoAuctionSlot.java | 3118 | `60f89182cf5bc39c5ed7e30adc3136437e980d54f12e7877fd408fc581021b08` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/amm/AmmInfoAuthAccount.java | 1392 | `6ac774eab4b65c84c3362c48690a88b6350bb2098c190e90ddda3c147486068e` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/amm/AmmInfoRequestParams.java | 2569 | `3aebf346dd43bb1d881ce75d85c0490d69a90684acc4a63e8f563b962af7a4d0` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/amm/AmmInfoResult.java | 3846 | `e985f03bb38491555b7cae884eac254b9d4b066ddb8aac16d8d40dd227b8cd51` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/amm/AmmInfoVoteEntry.java | 1565 | `b664076a5d791200ccf858ce57342b4de73a4da695cb2bb3e4fcc8b03e2b10a1` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/channels/ChannelVerifyRequestParams.java | 2543 | `d3a15c13d1e186cc6bcef9fe48271b565895e0bf359fab059dfce45f7bb03bc2` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/channels/ChannelVerifyResult.java | 1878 | `03e6a6c8e8d9293e935c872e38dad0cdde468d6bb9bc4b7a0a65ac1a74cf11c5` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/channels/UnsignedClaim.java | 2327 | `baa990024f9e96c868f9683466021684c0d9f12395804756b739bf76b429f09a` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/common/LedgerIndex.java | 4778 | `5f3953ce477e1d64cd445a5a96fd77e44340eb880f92ee1e8419c24d55f4b6e8` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/common/LedgerIndexShortcut.java | 2479 | `725a6701fcb9aa12bd1c3f6b1f85c7b9516989195c25ac1a11454108e3fce8df` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/common/LedgerSpecifier.java | 7676 | `8ffdee1f8faf33612e282589a0fbf9d5735b2f751312caf0f3d67d4a70ebef1a` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/common/TimeUtils.java | 953 | `62b82550795439166395350208efc894b353d3f5e0f3cd0fd1fcb9d1a46631bd` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/common/Wrappers.java | 7710 | `3dc7418b370a92df1a1da43671fbdc475cb1ea6eea0a6120505e90bed9e9d368` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/fees/ComputedNetworkFees.java | 4297 | `85202f9b08d61ce1d47adc125f18eb9443fe3779fdf9f0f80c969d0d81bffdb2` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/fees/FeeBreakdown.java | 4822 | `821657f47b52ab0334253340d03957e5a2de71d99d82ae8d04fede26aeb8d3bb` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/fees/FeeDrops.java | 2889 | `672bd7347ff717fb5e6d965bbc54b44fb1be39552de8ceea46ed71a659f98259` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/fees/FeeLevels.java | 2822 | `90e6174cfb69784085605cddc66c2668c9b2ab66f443d70b876412bc42c8eb5e` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/fees/FeeParams.java | 32891 | `14077ebc2ba0e12de192f032fe971132cbc958c4bbcc5a6c5a83c89d8bc7092f` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/fees/FeeResult.java | 4281 | `f2c656fd5dcce2f4a59c826c78823113ce5ba30d6fc81be4cf759adf364dda35` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/fees/FeeTerm.java | 4921 | `bb9214c682edb5a05881cbf6372143e135de1c668c8437b668135a7680ca31cd` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/fees/FeeUtils.java | 41534 | `51eee99e6a12e1e1ff845f4a162a54a2b01a5988485a14c142aa5c92a04ed60a` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/ledger/AmmLedgerEntryParams.java | 1142 | `fd3d074ec75f740a3737105919ac9324c8d64262d59a9b5ac91b6879c657f27b` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/ledger/CredentialLedgerEntryParams.java | 1620 | `6647b01faf61732d565243dd0117f06be32afe7909ef8b1693ecb909dc579e21` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/ledger/DelegateLedgerEntryParams.java | 1440 | `15d892e54c42471a76029a9200b824fa1c262d5ec48366ed82f92b3f21df7d7d` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/ledger/DepositPreAuthCredential.java | 2125 | `e62f879ea0990c732b3c82a19e2f2953c656dceb9bf6d760c115b0adb5ce7b99` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/ledger/DepositPreAuthLedgerEntryParams.java | 2617 | `a55ab2f57f5937c4773078c6cb07881096a2506de8c099184a9cebac0106946a` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/ledger/EscrowLedgerEntryParams.java | 1289 | `29ba44af1e4d9a9522ab2c8468b52e5fdabb3ce8416421e8211c8b5b4609bb6b` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/ledger/LedgerEntryRequestParams.java | 32499 | `66d63717c9ed940843ca27e3c2c66b39d4325b1ba300cde7f184c230a7471a40` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/ledger/LedgerEntryResult.java | 3922 | `8d4b5b3954f54050b69a4090509048bea9e84a59d18a7d23c2949fa41c29e3c2` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/ledger/LedgerRequestParams.java | 5183 | `94628a6a69671ba50c832d1b1fa355a469d70bd1d3caaf20c205d6a6ebd4ed09` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/ledger/LedgerResult.java | 4425 | `df4ea25c2e4384b0ddc521a77ebd65cd98ec3d18aec47491d49c977ac4dd5cac` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/ledger/LoanBrokerLedgerEntryParams.java | 1592 | `868468973665779a2cbc27ee56fce098451a23478c5b236673b9e1c82bf7fc00` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/ledger/LoanLedgerEntryParams.java | 1553 | `9cb208d99b9ba16944b226e5ff59fdbd422630686937bbc67a6578f08c4e252c` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/ledger/MpTokenLedgerEntryParams.java | 1414 | `5b7d1f7fe115fc4155bd0f5226246814da901b256562723a06539addf213257e` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/ledger/OfferLedgerEntryParams.java | 1276 | `a6b45de39c99c8edba8c5b1a6a6b395202892c12442a600288bd6e0f6ff3a0a4` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/ledger/OracleLedgerEntryParams.java | 1116 | `b9bc20ed8223622d2b68ebabaf11e00246745e4432482500f611023626bcae89` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/ledger/PermissionedDomainLedgerEntryParams.java | 1566 | `2d033b025cf3b30026b6414d829481e221eeafd04a579797d8435426fe0a2f75` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/ledger/RippleStateLedgerEntryParams.java | 2641 | `88ff4ed06d0de07b1db03704c444abf36b119b3046f80e0a6a1df075dff38121` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/ledger/SponsorshipLedgerEntryParams.java | 1592 | `a94484a8e9cd01be40bb713c8cc25c2b710483cd3154d4b138818adf1ecd0196` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/ledger/TicketLedgerEntryParams.java | 1346 | `b1e55c34423eb7cdace279d8f37c7c339cd4b7e90e3c78178595b968cfe7fed1` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/ledger/VaultLedgerEntryParams.java | 1534 | `76c8b265655e54a5d10c17b2db46f3a0f3c98948c04aaca05ebe755a23a8ea44` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/mpt/MptHoldersMpToken.java | 1747 | `703294732ec83ed8204ae23355b8301dff294d54cb720759f72385749ed24e88` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/mpt/MptHoldersRequestParams.java | 1567 | `8875c02900ec21b59dc0633849f862067a4e6daf0f11cc9e3e71520cc3598379` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/mpt/MptHoldersResponse.java | 1348 | `3eb69668c9b38ed1fceff112e40d77b32ed68c513aae00ac733be776a8560b96` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/nft/BuyOffer.java | 2422 | `7111729e82b39cef0f295c95a721f7c6c64a6f2e5404fdb6c28d9018a35bba31` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/nft/NftBuyOffersRequestParams.java | 3374 | `28a70b487d435bc10fe1f153c9d7f6bce6ef5fef0f43354d8416d1f93f17a061` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/nft/NftBuyOffersResult.java | 2685 | `abeb10e22708e8b553c354eaba9863652a0b1baafb73ab6ca70a0ed7bb7d8b1b` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/nft/NftInfoRequestParams.java | 1842 | `a25817ff57a4c3168cae0754774dc2786fb4e87ab04689517fc59cd9356f1e08` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/nft/NftInfoResult.java | 3349 | `75ff0180e2041ffffe5124b7cc21d7e9e3b862ec77974d170f2a0b6b8af672e9` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/nft/NftSellOffersRequestParams.java | 3380 | `3ec6c8ae1137d8ce3b6b79b66d7fd915a2ba7ccf2f1b9efde4168fbaa9191bac` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/nft/NftSellOffersResult.java | 2702 | `a875c3ad7299d7cca4613489916374f1984710b991e86432a89bb494684ad53f` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/nft/SellOffer.java | 2359 | `6c7d8b80bffc2eb529eb7f28a134237a7ad3e0501caf70141863a7cc88889542` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/oracle/AggregatePriceSet.java | 1787 | `c1b1e6500fde0dc5cb68efbb7108f4fb531850539e24658e9d7797b53db36997` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/oracle/GetAggregatePriceRequestParams.java | 2579 | `438991e14cdc101ee3e1c46cbc8d5f6da2d6d630ea8b787823dec29e33b57ec5` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/oracle/GetAggregatePriceResult.java | 4846 | `d954bbd8f01a31eeb23eec3195fb6c6551a3ef2ffd8f0644806b07034852b0a6` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/path/BookOffersOffer.java | 8039 | `427981c9a89cc29d63da2cc6d920d971f31f0b0cca029f627549412001e1eca2` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/path/BookOffersRequestParams.java | 2938 | `370b65c40f007c0e0b541cee83498b4d7363e1c1f2df529d01a01626e9ebf1e7` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/path/BookOffersResult.java | 3597 | `d60670e3e95f6cb3d237156733ba0624a0d5e45bd20c7023912d6b829a7235ea` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/path/DepositAuthorizedRequestParams.java | 3947 | `f88117b49765022ddc1e3be2cb23a0f737ee4e69a22083cacdad21507a90a1d1` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/path/DepositAuthorizedResult.java | 5951 | `f93998056ff8f08bc745946875bbc0f1b458b9fda794d5d4f0e86060b8cc7ec8` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/path/PathAlternative.java | 2336 | `bf9d8d04363124f15d15b2b2fb92966fe402180fc32e63ed1e613efa3976d536` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/path/PathCurrency.java | 2424 | `ccb36dc7d83fc61e6db2a89a06d493ea9859bdb1d2c116338583847fdc04cf0e` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/path/RipplePathFindRequestParams.java | 4520 | `6c65aa7b1e8d0a24b9e4c33b954b54acbb4b870fc719e7a7b879371bf4cd1673` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/path/RipplePathFindResult.java | 2701 | `c4592b5b39f28ed7273c3330546631deb7b019fcb26d945617ada5c4a0367abf` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/serverinfo/ClioServerInfo.java | 2169 | `4db89a8baa8ea6f5b43070d43bbcac98996759c407564f6206088d737da24301` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/serverinfo/LedgerRangeUtils.java | 3309 | `6115657d934b8a0b805012d86acad32f1417a3189870b98a97eab05a53b237ab` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/serverinfo/ReportingModeServerInfo.java | 9476 | `9b885293a8953b236d5dc92c4caf9c9bd58fee3e98e2016c52a694f0dabeec72` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/serverinfo/RippledServerInfo.java | 10761 | `aae80ed96b6e4243e21e26195b802801e4b7f5c48b4c436f176e15f4ed0a2739` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/serverinfo/ServerInfo.java | 16699 | `121d7816a1c6c00a3f25f97ce8d652cddd4b61748219b91e694e32d68ec04b8a` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/serverinfo/ServerInfoResult.java | 1666 | `d42a84b7d142c8a0465d9f536577861b6b60e6249f28f68cf04f13ece9415f6b` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/transactions/SubmitMultiSignedRequestParams.java | 2422 | `6bbb61c80fa0fad7560f9c4e17a75cd60be43b5ce40a38be5eb628655e31af70` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/transactions/SubmitMultiSignedResult.java | 3153 | `8bc4e087ed58d30c14130aeb1f45ef3fcb970c5487816c35fd8041b2d7be5e30` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/transactions/SubmitRequestParams.java | 2029 | `1b63ea87c1d2a13ec2917497d33270f66a0c7dbcdbea9834fe4743fd5b663485` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/transactions/SubmitResult.java | 6088 | `de5f2c667f8fd67dbec93d6d090f95012db1f73252f5e144a334992846adb628` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/transactions/TransactionRequestParams.java | 3926 | `1d81961d70526f32c78f33ebc596c8f8115051693c496252e0405c2bf7ce73bc` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/transactions/TransactionResult.java | 4601 | `a091d0386e6c94e9458e2fe6676231485bb3adf72c32057aaf77ce6e5a726cbe` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/vault/VaultInfoRequestParams.java | 4035 | `db0d4118f911c488fa652ffb722632c4a5bcf9566918463d134e2488f93ac748` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/client/vault/VaultInfoResult.java | 3727 | `abe7efced0dc248c3e84029b2a2cce891d47c5dfd6810053cad8f7dae9c6957b` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/flags/AccountRootFlags.java | 9616 | `07be9cba2b70bbb551ff5bf2bce16aaeb2e048da0e412ec5b3b8cb48e06368fc` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/flags/AccountSetTransactionFlags.java | 10162 | `02b08e803d9230f0f7d544a19fa1213d5762842ccddc30a0cc29eb399672f45b` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/flags/AmmClawbackFlags.java | 2459 | `b4daff17fb5c7ade6b67a0a8c2da8bac3e9b325951c5e613bd1ffb4671b9f676` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/flags/AmmDepositFlags.java | 3746 | `eaf8af5099794affb0bc30c813bcc5decd4d8aa31a5be6750c07e72d6ee1f2ff` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/flags/AmmWithdrawFlags.java | 4222 | `ee189c6200fcef899500f15fe34bf06f12a20d7f2ad1662e327b91a724d943b7` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/flags/BatchFlags.java | 7989 | `9981f27ce2570205416a0dfb43cab08f300c7e9016ac42cafef4670b6bb3f428` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/flags/CredentialFlags.java | 1940 | `d87bcfcab803803a7cba93e776ddeb6a172294760889c07f45758be34218fa50` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/flags/EnableAmendmentFlags.java | 4140 | `0c88d262b0118682d88a1141209b2094cd2cf43f1c20411118c46548de681153` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/flags/Flags.java | 3957 | `a06aef3c90bdb527cdc13dd381b5474f74e7a3749df141152c113a9cc8027e61` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/flags/LoanFlags.java | 2176 | `8961ed843711cbab64b7fa89cdc20581144b5418763740c03c267ea9e0b6a8fc` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/flags/LoanManageFlags.java | 4435 | `9d95042661252a326750e5918b3b19233f671a6884f213eec3734c450663c162` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/flags/LoanPayFlags.java | 4596 | `f777e55551a0ea9f5d5920824543cf104c06a5d15cc26beacdfa413a7c9e0c6a` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/flags/LoanSetFlags.java | 2689 | `7082928b09417bfa4465cc82d461c08cf0978f1af43d17333bcb987e28c80aff` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/flags/MpTokenAuthorizeFlags.java | 2076 | `57272f3952e92da06f78e1560e95f9fa3a17c23611c74f129884ede751238601` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/flags/MpTokenFlags.java | 1839 | `e17bb4316595b11ae8af60666f4a9fd0f902c3452a232e9e95b9ff069d09b8e6` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/flags/MpTokenIssuanceCreateFlags.java | 9624 | `d93b7cd25d4babbb024b3d1624717d20da9a34c2949ae451105e55cc74aed576` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/flags/MpTokenIssuanceFlags.java | 5113 | `7c6e4fdbd813bcb411080d29dfb0ce804ed6eda52e6bca7c9e20bc38f7ad0488` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/flags/MpTokenIssuanceImmutableFlags.java | 10949 | `048dd793b99cfbe0fec962b416a7bc551d958b00684a07dfb3cd8edc6958d329` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/flags/MpTokenIssuanceSetFlags.java | 12018 | `0f4ce70bdc1793147ee9679f68073513e78397273ffb7d238bca4f32312302fd` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/flags/NfTokenCreateOfferFlags.java | 4528 | `975997e79c960370924a2dc30e8cf898e5d8a16ddf9dfdf28f8dfd7ee29b96c9` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/flags/NfTokenFlags.java | 3710 | `da145082833a04d7e5e93e88c95a43f4ff467167cbb0cf58d3e2c47fc854e384` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/flags/NfTokenMintFlags.java | 6922 | `e34ffa7e2289f49d72d7176b25524b6ab9409467a2cf458f77ef87a49b939c4d` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/flags/NfTokenOfferFlags.java | 2221 | `901c98808fff80bd4af2fd77824f57c07e3d3dd3804b95384dabeafa5ee9c39e` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/flags/OfferCreateFlags.java | 8740 | `e71bb7c136bf2b692c99235658fbd3399ed8de12285cb0106b82687391cf285d` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/flags/OfferFlags.java | 2714 | `a9fcc0daf621cc9370b25bd54cbeb2717cd76020f128028ee055ac8c9af26a48` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/flags/PaymentChannelClaimFlags.java | 6573 | `ceca33679795a703138942724a5d7fc659ec4ff6cc6b0d40d9120478ada5bbab` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/flags/PaymentFlags.java | 8614 | `9f8d7c11ec0994880bce7b51f5f96f600101cecd4bd453dac446263e3cb3732d` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/flags/RippleStateFlags.java | 6206 | `ff632426b9d0ed43464aec4626ccdf00fde440c03b186bf2cc4705098811887e` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/flags/SignerListFlags.java | 2215 | `81649b039b5880352931cc6bd1460834962b14d8a545fd1e983cbda0923c2c62` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/flags/SponsorFlags.java | 3855 | `5260da663c3efbb62dc55bbc14f54ef1a67d41484ab7b47fdeffed8d9013e33c` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/flags/SponsorshipFlags.java | 3456 | `faf64a82c2f87b9e16167073caaf42771873d9db82679a8b946ff83a57b03e9f` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/flags/SponsorshipSetFlags.java | 10546 | `85ecfe52bb9c09bf93ae4feb67353654f8a6e5b2ebc5fc1067d748640fc44a3f` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/flags/SponsorshipTransferFlags.java | 6351 | `a4d28c7905e3ec611afc231f29540a1af4eceae7ee661c312b00071c8a0182a0` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/flags/TransactionFlags.java | 3227 | `159f2d8b2d661e2f6bf34a9140db8c8f1e3a8b9404015430c872eb20547c55cb` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/flags/TrustSetFlags.java | 9867 | `55d1d4d020d4c546190663af3b6e707be17eeb483570ac77a2ce1b1bcb92ab7b` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/flags/VaultCreateFlags.java | 3901 | `e3605d83b18decf373a609b443187962687d31801df8e37ceda401899c9f654b` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/flags/VaultFlags.java | 1392 | `13506cd199b935465bef36ccabba9481d9c39c9e159f02987607c216f5736dce` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/flags/XChainModifyBridgeFlags.java | 3818 | `df3e0720c058420dc7cc04a36f620607a7d2c75450d4baebe200f9bdf51a276c` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/immutables/FluentCompareTo.java | 6510 | `d28cf6f89f4e1ef825c1c4d6dbdf3b546d105656199db5023eff45dab8a72f9d` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/immutables/Wrapped.java | 1556 | `91120b7199450a1f7ed5be60f2a196625be08bca01566eaa5a08bd2a7159c981` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/immutables/Wrapper.java | 1815 | `61a2da0447cb7a08a60de19a7184b31de73ab3a7e92ed2b9210e4e79250f0371` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/ObjectMapperFactory.java | 2328 | `19e6391579de7c484f3aa5e11aaa3fb90b809b9f3718aff99af2c33ce7b3b3e1` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/AccountTransactionsRequestParamsDeserializer.java | 4920 | `84ddd98a7739abf2d92dccda4bbea98e9f319e362c84bb02d0939c4832ae69d7` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/AccountTransactionsTransactionDeserializer.java | 3501 | `3576702141584dd3fc95b4486eb9e8ce54c18ba08a96c44d4c3459304c5ef638` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/AddressDeserializer.java | 1512 | `4295cd3bac115ce23b2e1249681c3a6c7739c0fe17727140ec67666205e7c24a` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/AddressSerializer.java | 1519 | `f0be020624b18e5519490ea07c0ac9d7711a3df1d61f997d29d71d9b4dabd1e6` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/AffectedNodeDeserializer.java | 6902 | `e2f46d85236872fe3087ea34008757075e3a97e00fb0f4844f13e6fc9912edbf` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/AffectedNodeSerializer.java | 5560 | `1c99e7aa0c5b9f8e8cfbdbcc407c0a884ac1c92ae379bfa4c661a4be2191f284` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/AffectedNodeSerializerModifier.java | 1924 | `962e99bf0392188b5dec41eb1592abc52cd0762d67acfeff93bea35483298acc` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/AmountDeserializer.java | 724 | `7036a0817979db6ae539eb07fe784ccd2c22e546e4369110d71c5e18eca6f0da` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/AmountSerializer.java | 734 | `4ad95ffce030c8f25587e024a4fef1f0a6c6661e920dd1f0e00c51493e87db81` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/AssetPriceDeserializer.java | 890 | `c1213d0c7c59c0abf04e5362d7dc62cc6bdc9bc16ad01035e337ca066e719900` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/AssetPriceSerializer.java | 827 | `4229de691c327b021fd26272437c53a9d298135f302dae2a4bde25a370aaa379` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/AssetScaleDeserializer.java | 910 | `18cb8783bbebdb59478af6c7731e011506cc7981c80ee55e7f9a15b2685aee0c` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/AssetScaleSerializer.java | 789 | `b65edbd774e025f9c96270a1bea52b5def70d5362156f5820bb54dd0501a39c5` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/BaseFeeDropsDeserializer.java | 2479 | `6de1574a8add9a76cd814827ac8b3c4f81adfd4278d02a1c8b71a03ffe4cbfd8` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/BigDecimalPlainSerializer.java | 2169 | `57edf272ffd27907b1652cd448ace29f641d775e7dcd9fac54504192e27d0d2d` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/BlindingFactorDeserializer.java | 1572 | `f5ea34712bc3ae0bd284f05c0c9c281e3bd873f553231fef624c0fedaa1e2fed` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/BlindingFactorSerializer.java | 1593 | `9c39b578c5c58d8560339c7ede21d5c4646d48caee6e4d4e76a38a29dc9b4cf9` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/CommitmentDeserializer.java | 1540 | `280dcfb6d5db8621b87cb042e10d09bc3d77969523062d7c586b656aa594e2bc` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/CommitmentSerializer.java | 1553 | `7ce31dd3831961e3ebd392ab3bf12538228b28aa0e7837f04012ec04bce7705e` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/ConfidentialMptClawbackProofDeserializer.java | 1736 | `45eb8fcb102997b6c1c64e0af541897e63d047733b4bc4ca478407c28be4460b` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/ConfidentialMptClawbackProofSerializer.java | 1733 | `4413fcba9c4293860f09a16ac6f3ffa92b48e48b7947d1c966cd9cedf5eb18a0` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/ConfidentialMptConvertBackProofDeserializer.java | 1760 | `cd2d7742cd99b6802997881145dd6dde24bc4c30e47dc72cc62189fa84d6cc1b` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/ConfidentialMptConvertBackProofSerializer.java | 1754 | `169e4439e19f8b552a8ecea978990b577d9cda35eda015983008998ee1394576` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/ConfidentialMptConvertProofDeserializer.java | 1728 | `1c7c94f193a8766b477e0ce07f62340217c3d2b9fbdc70a058f4a4556ba2e471` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/ConfidentialMptConvertProofSerializer.java | 1726 | `8afee7027b97a59e43fdc6dc868e993115876907462c692621cf8fd155fc8e92` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/ConfidentialMptSendProofDeserializer.java | 1704 | `4a41af632299cb042e6ec0c8358608b5443a395b844bd7b52c7cf122c819f213` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/ConfidentialMptSendProofSerializer.java | 1702 | `e36a3b15a8c1d9ad8fc44ac7c6c02e5ed11bfc15056668dfd46512864b2f0b19` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/CredentialTypeDeserializer.java | 1566 | `d50383e35c9da7c30c2c7784772ea8b59bb866302ff9091bb7127b930ad4f5ce` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/CredentialTypeSerializer.java | 1568 | `3a86fff19930e82ce210e43544266d50f185b056151075ca90bd28468b64cf7e` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/CredentialUriDeserializer.java | 1558 | `0dc2fbcabf9f32bd5e0690580e6d7ad00cf0935aa45ecd8cf81b7f14ff694aa6` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/CredentialUriSerializer.java | 1558 | `f3e61177845ccf3d03e09acb62ff2e64cde6fb7dba2f387d2b9dfae459b105fe` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/CurrencyAmountDeserializer.java | 2718 | `d89d32d2312edf4f4e9c13099452b2f0842ae3ca7c0a95c2495d9ec7a7b2064c` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/DidDataDeserializer.java | 1511 | `5d3223967d37311a1833d67008203c4f0202f30d285ebf3679dc0ef190e4b2d1` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/DidDataSerializer.java | 1518 | `b9f644a6acea4434229ae76196c47aee15ad52115993ea58e0882a8b7080aebd` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/DidDocumentDeserializer.java | 1594 | `fab041b1df0ed0ab222d263fa73b98aa4210c45ac8ec531e3a96561ea1fe8e87` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/DidDocumentSerializer.java | 1554 | `48f376b8525ce650a54c6667f31c78b5ac0f067ccfb9257620a4ca76f14ea927` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/DidUriDeserializer.java | 1503 | `49cbea062fb23aa3e7c49ae8a6ab14399651d6268c3f6eea6ea1e0939424fcfa` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/DidUriSerializer.java | 1509 | `28a97ef52331f3f8aff3990d6f14e9b4de538ed13c0466fe78073b30f2d20cf5` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/EncryptedAmountDeserializer.java | 1580 | `514e11ff99e66d05f241c95a569a016491852dbb4f85b5473c6d8a2a4b293f23` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/EncryptedAmountSerializer.java | 1602 | `9bad4566747c45f4e8b082d4ecb3e302bb5f4b698188d118651aa09e90464e21` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/FlagsSerializer.java | 1713 | `99ca3ce88670fa649a9bdc8fec0359035b2d9c2d24335c4b4788bb332e01e36f` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/GatewayBalancesAssetsDeserializer.java | 2331 | `43ca2943dd66215727bc46f5a3ba8fa0c5f30aacd51246e78385b347f6e512d4` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/GatewayBalancesHotWalletsDeserializer.java | 2394 | `4c999b3a129898ffbacd29baa5a320ce519fb36c8312cda52caf9f7369f45ea4` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/GatewayBalancesObligationsDeserializer.java | 2542 | `66f1cc448112373f46e58d6ca0f2ac6a33f72913356988f157761fdacfaa093e` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/Hash256Deserializer.java | 1511 | `98e6214e86be62aaefa9114b3d92c6a6b393c467f2bf62eb063d7f33747fb943` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/Hash256Serializer.java | 1518 | `bd7c56c88ed65684644ab3e80da0f7ba0b27a3770657499906f7ad6f06e307ff` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/IssueDeserializer.java | 2601 | `06d22e1bc7c18cc9e787bcfbd5882cbad7974d5f9fd166d56ef839007134f137` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/LedgerIndexBoundDeserializer.java | 1597 | `0dc86ac4148b6b30b7c5fa76e073f001d9a6c8cfd32090d8f99f7fb1a71c81a2` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/LedgerIndexBoundSerializer.java | 1634 | `9d3656d7e77a108a73c50f19308f84551febd049b46a3dee4e945e151c7b510e` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/LedgerIndexDeserializer.java | 1635 | `8c16980ca821da3a455e46e60afbf86a0d94dc1dd0b8db2c47fd0867040aedd3` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/LedgerIndexSerializer.java | 1583 | `3fa6684cdc612947a074e13913c91e05760c12adeaaeda4942591885affccc43` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/LedgerSpecifierDeserializer.java | 3099 | `afdbc7fda04ba2f46c8952f868dabbfe017d811a7b18f3de178497897713e771` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/LedgerSpecifierSerializer.java | 2189 | `491cfcb413742645f51aada449f6c184c6dfc9af7e6a234c81a38ddd59bb5327` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/LoanBrokerDataDeserializer.java | 1565 | `a4320c47f804d2cbd88e5f8889eafde809c706f8078efa41cdd7650ed97d5576` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/LoanBrokerDataSerializer.java | 1585 | `d068a1bee2ecd92325e9f78caf4c9fc23fc7770146c03497dcc2662814d62889` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/LoanDataDeserializer.java | 1517 | `1645f16cbd0932ec748ff9ce4252fc0d4051cb4b004d17fe99cb0a63966ef23e` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/LoanDataSerializer.java | 1531 | `b7cd2e0138497e52bc67a9db2b65377eed92df9e9909c59a6d29ce27dc29bd40` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/MarkerDeserializer.java | 1896 | `c80db0856a3cf76d2e689e1935988d726437b3fa3c84be69b2d97a567cecddff` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/MarkerSerializer.java | 1593 | `60d03272ed573582d3d89bfed8296b083d9de946ab4bd9e2df301bf4a18d57e5` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/MpTokenIssuanceIdDeserializer.java | 1591 | `3cb19dbebd0e6a34a298a349957df7b63595a4d43da2a2cea6c6148d58839dc5` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/MpTokenIssuanceIdSerializer.java | 1584 | `6b5254cc895956224b1db00523dbf02234e33d7381d8dbcbe72bb66870627998` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/MpTokenMetadataDeserializer.java | 1575 | `5ecc1c1d43782d35379309c4b29d2ceffff93331d2dc0feac423672be210ea9c` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/MpTokenMetadataSerializer.java | 1570 | `9cb6a851bfa7dacd0a9a8feac0026bf2a74f45e59d789c6acc88e6f49917739d` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/MpTokenNumericAmountDeserializer.java | 1005 | `61751cfb9fd6652ba1bc06d1dbdb6c0505e8722dbeeaa97073428c6d2551152f` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/MpTokenNumericAmountSerializer.java | 934 | `8cc010d027daea6133e3dafa06a430ebca0d20650e88845d49e7266a283e0b56` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/NetworkIdDeserializer.java | 1611 | `fe4d15ff3eff6d066bd885e7321c31fe796032f0559bb4e02cf80bfb8236d3d7` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/NetworkIdSerializer.java | 1540 | `f16d4fed0e4486e676d3e782e448875be1dee970b76ea02944c9a3c5406521a6` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/NfTokenIdDeserializer.java | 1525 | `78e99bf82bd98a15d8f794710aeaa6880ed6fc9b98db4e15643362f5d5a3c62d` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/NfTokenIdSerializer.java | 1530 | `eef68667fdfcf23d062107fc25139ab0dd2d4bcbe7cce1245927056d0b2c06ee` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/NfTokenUriSerializer.java | 1531 | `38d6a69ff9089d0c4bccb92c1740d107b3e08588ccbc34b412b76ae345081b9f` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/OracleDocumentIdDeserializer.java | 854 | `006fa0e5e700cba1bb605e86b50392645ff394ae8ecbe29e3b70e5f16e73b700` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/OracleDocumentIdSerializer.java | 815 | `4ec0c8a8e3997cb29963bc0eae3c167c08fbcb2f8000f3359188928cce99a619` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/OracleProviderDeserializer.java | 795 | `f029ba3e04a340cf1f3f3f7bfba47ece74e850116390f2107542833f6e690c5f` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/OracleUriDeserializer.java | 755 | `e5a6a7399fd9d7af33161d8bef918954c0b5d392c3658ead2cbba3e3eb6f90dd` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/PermissionDeserializer.java | 2405 | `71e419dde1e2dd54ee7c3ccf77211dd522a6abcac46861556873b8552c5e982c` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/PermissionSerializer.java | 1724 | `becd4de4ddb828eb118b5c6493cedb084a5d3a444176b5613196adf8cb8ec95c` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/PublicKeyDeserializer.java | 1583 | `bdde4b6f9680d68dad946c16080af942002d6b22dff4ebcde1b6dd67b3963159` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/PublicKeySerializer.java | 1717 | `c87cda081a3a5d01b0ae66211af7237f514b927488d53b236b72a211ce7a612d` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/ServerInfoDeserializer.java | 2379 | `8091e3d1d9f20815802322ada609c510dbb8e660a45853dda45152cb6f250b3e` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/SignatureDeserializer.java | 1647 | `d56d68357291850b6701b8d80d8b9824594b82cc6cadb44a9f5931ef1d42bb90` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/SignatureSerializer.java | 1408 | `8731c6bd391ad0cef9a636a86fd7861e7d16923a3d6f3fb689a0ace0e17f121d` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/TradingFeeDeserializer.java | 806 | `1b19e4a07795fd2fc24c1df1d709b875ebd7f279f3949c39b5fea249540b90f3` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/TradingFeeSerializer.java | 745 | `ec8d30d5da89094d4620496ba5ac68d6a6e2cddc030596f370c6b446a1e67e93` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/TransactionDeserializer.java | 3080 | `b26b91514d3dce65b68cd3420f35156faacef489dabcdcc016cc4b7003d80705` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/TransactionResultDeserializer.java | 4766 | `98afdc7eafc4c3ecc8764be7ca26dc4ab5e6f37801f95cf50f20820ddd955296` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/TransferFeeDeserializer.java | 1621 | `6286671c3b369ac82163633a0f1405fe9b47636855caf46eec5b2ec5a61f499e` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/TransferFeeSerializer.java | 1557 | `2b3cc4b5487c848ad0b06f08c77eb308bd980ae108028ed2c9c5f7e128452e07` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/UnknownLedgerObjectDeserializer.java | 1668 | `0e49dd104d826c2be5936f2572f2fa5a74d0717767a26b02945dce5014ee2b71` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/UnsignedByteArrayDeserializer.java | 1597 | `cbff95f505ef99fc80e14b0f4f1960fe5b3c501d045bbd8ecaeec4ed73f22c61` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/UnsignedByteArraySerializer.java | 1560 | `62d5f8d269148d447186ab0be54703d079432eb2ff525829acd1fe52c79bbd51` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/UnsignedIntegerStringDeserializer.java | 1691 | `61c34974dec1cdaf841a161be77139abf934aeb731b842c24d5ae280fc76ff8a` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/VaultDataDeserializer.java | 1525 | `44b169ed19c0534d43d179f6cd5435f7959bab2befb5f89f440b392d857030ca` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/VaultDataSerializer.java | 1534 | `1bef06d6f887689b47c90c51a4a4355672040f20367a2060596274f673ea78bd` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/VoteWeightDeserializer.java | 806 | `f5d7581d71f7decc3e07fe8b0dc43b9d2388c6f7c83f140a80aada6fc16be656` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/VoteWeightSerializer.java | 745 | `7f775b399cf8dcc736b55184a9fb691a4cfff10d5de804bd6f2bcfd490b22ce8` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/XChainClaimIdDeserializer.java | 1048 | `b7d3348689d875d350ff2f6dbb4ef6268b903adc03865cc251a4a1ef33006b06` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/XChainClaimIdSerializer.java | 904 | `cc467a9cc06b7a05bb5a901b77b9c3d1e8c8c4daa766b9c1f8430f127a11223a` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/XChainCountDeserializer.java | 1057 | `86311e3b220a49e5a43c6710f2801c5a95d5862dcb4bf8e9b591fe3eca13543b` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/XChainCountSerializer.java | 993 | `859f05a4b069f27f460cb391ccf313117a6ce41810270a31fb9446e952437dcb` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/XrpCurrencyAmountDeserializer.java | 1603 | `044b488cf60413dc4d326286d34c94aa565228df7793eac7c1cfab07e218fd0a` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/XrpCurrencyAmountSerializer.java | 1627 | `924c6133e78ca4578c735233bd780f2b0c6ca017d8a321a5ca436b3114945b61` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/Xrpl4jAnnotationIntrospector.java | 5340 | `bd43152886fab654d83a30dae2b59b91c96f988570101cffa9380dc114c7d0cc` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/Xrpl4jModule.java | 3509 | `a5de0feae16481cc3ee7141c5812b3786fab333e51e1bcf1bef90297dc16fd02` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/ZonedDateTimeDeserializer.java | 3080 | `6c3c5b63ed36c40d2c6bf63a050197d593312bd61309f1f263223bbb2d7c9aa3` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/jackson/modules/ZonedDateTimeSerializer.java | 3225 | `b27630410252e4e9a07541316288160ea70db9f777a85ca8cd4eb3e194acbc6a` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/ledger/AccountRootObject.java | 11369 | `d208b1528bda7c717e12a39a6ea491aa19ddecc1e0cc092044446e08daca2dbd` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/ledger/AmmObject.java | 4361 | `2a140f57ff94548156d0de099cabc760fb4deffc60dc139988b76dd227c3e4f7` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/ledger/Attestation.java | 2045 | `928a7859403aeb006a212048a7985d4c592c79b339a8d252e18caa40ba898d1d` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/ledger/AttestationClaim.java | 1540 | `161e2b3faaee2fe74c583dcfe0fe4da33cefbe3c1c38cd9273d0765d24cde9ab` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/ledger/AttestationCreateAccount.java | 2006 | `4cef396de070183d275c027933c594acdf3b35447dfb38a95b87ba77d1279a48` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/ledger/AuctionSlot.java | 2766 | `9946d767f4535c2a024bc00822a10828cacc83a7e23e2b7ac5eab6595a1ddba1` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/ledger/AuthAccount.java | 1175 | `450618329886a91cf73f4fd51524bca173a714a6340c36fd1811a0cc9c202e4f` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/ledger/AuthAccountWrapper.java | 1170 | `0392c9bfd4c714f7de18322e022051fdfd19434fc2e020385a7224cb97369511` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/ledger/Book.java | 1950 | `321fdc5bf81d940641c0535952751603c0a83919274330eae2e5f46104641e49` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/ledger/BookWrapper.java | 1628 | `28f14f6eead6b5eaa6209e3f15c7c4f83585dbddae46a2caed5345b116b47aad` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/ledger/BridgeObject.java | 6005 | `b2e5799bf521056860da34a1285d3dedeb48db9c42dee008705b7fe6ab348b13` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/ledger/CheckObject.java | 7064 | `d07512515128ca1bd8a0f5673571729c6359633c39922087de5723f30d0560ae` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/ledger/CredentialObject.java | 5627 | `931a7d59151a16c0aefe52b9bc47a0d937454d9a0eab066792dfce67fa101538` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/ledger/DelegateObject.java | 4968 | `2e1acc22579ce4773ff5da83ff5f5959ab6844aaf9dc4b95314ee9a45c3d781e` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/ledger/DepositPreAuthObject.java | 5415 | `71b12abb4d1fe3d03137566409b5add58fc6d2e95768054d88b3ae3ec1e40707` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/ledger/DidObject.java | 4234 | `7e79e6a494a87f1a9cda3ad5792b0659fa7acf16f07802f1a7803f00bafb4fca` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/ledger/EscrowObject.java | 10421 | `6648c0c05cbe8e9edd832f75109efce9847daa46ec1547c5c8fd53721cdf8da4` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/ledger/IouIssue.java | 1891 | `06c9bf3a7318ac61429c57ab08a40fdec4c751c199e2758846e2942bbb39ef8f` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/ledger/Issue.java | 4152 | `517b760e14a7f6620b98f7dbcb23f943efe341636d06623601c5fa80113dbbe7` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/ledger/LedgerHeader.java | 6361 | `2bd73419cc52557f22124de6404ceca279f4c8eced8a00c548837ef64507847a` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/ledger/LedgerObject.java | 10805 | `31a20cee74e5c7cbcf195cbbdb9c9c2ead4d72fc1a7f96d8a6de20cb62bc7ed5` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/ledger/LoanBrokerObject.java | 10157 | `528b51359ea9ca7fe88b0293af5d7477cb65cae817a4afdada45c6c44025ca56` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/ledger/LoanObject.java | 17163 | `ab3965ee716a1d195a3cd3b29d2a59f99a81455a0872aed62f8de48e02f10e76` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/ledger/MpTokenIssuanceObject.java | 8347 | `da4e77cc967c6c0f19ae282f1307c718786c977293f0cdcee22268a081756d6e` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/ledger/MpTokenObject.java | 6297 | `9cd0d8a0536679eb39283b4a83f6c5873fd58ca4676b3bf7bc0d5c671d4e4400` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/ledger/MptIssue.java | 1938 | `11f235537b17e7b391d7b422ea106e7b38826376510280ecd6ba2fa31b1dbcaa` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/ledger/NfToken.java | 1300 | `00986ec42b2904ac1c9cb8b34b9366e409527d1d7d681c4c4715bea0c58c39c6` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/ledger/NfTokenOfferObject.java | 5022 | `0db0741d2f5b6c7b574dedb1f790f8fb28935334f71e8fa132573cd33f444cd0` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/ledger/NfTokenPageObject.java | 4017 | `b8213c5f628343228e2fe786592ca3c3aed3207ce102249b44e17b175345699f` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/ledger/NfTokenWrapper.java | 969 | `b9c1c42318fe5cb20b2091fb9e37d6b6c3572bf716f94e93606ed5577f17f898` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/ledger/OfferObject.java | 5753 | `792de387c8085817029fccd8947a0d06ec1e4c0f16997cbb46c785789d629bc4` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/ledger/OracleObject.java | 4810 | `3d4808e5c3efc47a10e04fd101f9d0587a61f1f89eee3175e58f4052e909007f` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/ledger/PayChannelObject.java | 9927 | `5a77f1f7cd34a2ab2bb70e96ff7fe800752891b4f8b99c1282d30689048c7dfa` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/ledger/PermissionedDomainObject.java | 4268 | `efce3edda4316eee25ff1dbd88e1eb2c5973beaaa4d61ae4fb11550ba8e45a10` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/ledger/RippleStateObject.java | 8245 | `e7c6016a1024e34ac4acec4b40c1d159c5d68ff91ba0d81959e30930ebd4e2ed` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/ledger/SignerEntry.java | 2232 | `7f520b07f497e2fa3f37e76892abd283b743b8aa52702285dae34e7fed34d9c1` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/ledger/SignerEntryWrapper.java | 1857 | `0b189e47a8ce2f40a89ad2606159e17c21aa3c4e81f6d3124cf6896ac38ee962` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/ledger/SignerListObject.java | 5045 | `5dd02db2011b384ce6e8f6279c47f7cd66d931b87604b37a469cc8b63ace00d5` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/ledger/SponsorshipObject.java | 6951 | `77672bd1b17b98c3509ddf39fe8b050e6756f42710362376944b33f656ee4048` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/ledger/TicketObject.java | 3778 | `caa41b765324745173dfc98f073d2ea71e19828260b62479f30c10207e20ccba` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/ledger/UnknownLedgerObject.java | 1420 | `e5d50233fc85aa70813ffae3a1f2bf3b76e36e046413358db52592cecd83b53c` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/ledger/VaultObject.java | 7529 | `5c0051c16040cb4395fc53b3a8bca30bee76782583f27d0f3776d888a288e9b9` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/ledger/VoteEntry.java | 1455 | `56c9493e88d0c3d0956a024ec1504dac68e83e28aa4ea15cef74f6c2ccb404ac` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/ledger/VoteEntryWrapper.java | 1131 | `0f8734f9de21e2791d8800b03a6f1cff7881946be39c283e55f6cdb7b422e86d` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/ledger/XChainClaimAttestation.java | 1322 | `ff8d68e39ae5531af4f6dc39984f389295c2063bc8716720f5d30bfa1deb39ad` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/ledger/XChainClaimProofSig.java | 2544 | `7e65386a9c9b7f880f5b692a22ad2161eadc66bb1712ddaf7da0bbf35f5fb173` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/ledger/XChainCreateAccountAttestation.java | 1461 | `42ad6b70df974e9b7ca3b73492c4f88a15f1991123f553938c2b6ed26f26d3e4` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/ledger/XChainCreateAccountProofSig.java | 2991 | `e9bf9796217096f440c2ab74d11cbcbdfc7dfe826cd3ba1d696ee847d116faa8` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/ledger/XChainOwnedClaimIdObject.java | 6044 | `0fadef5d55607f885efc9b1b7442bfbf795ad255777169f35df85ca9a23b2f9e` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/ledger/XChainOwnedCreateAccountClaimIdObject.java | 5104 | `9be66fa8c4f6b670608735d3aadf2cbf6d24ecd4af1312fc4da308959abf4453` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/ledger/XrpIssue.java | 1498 | `2ec083bd2b59b1424681d16c8800e7edf51160b2fc185d9b7ad35bbf02150daf` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/AccountDelete.java | 4107 | `9a0d6e1ebe7b7679a91243e2e153185f21936ae2c9d53d11d04c2544f81878f7` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/AccountPermission.java | 3292 | `91db2dd4970b1d0b1f3f0b0f5e262bdcc12aaa05685214a4dc42573442910882` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/AccountPermissionWrapper.java | 2066 | `291d430b1e80c97673e492253b50dce89b90e8da52f86aad4493e5609a58b048` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/AccountSet.java | 23302 | `91553a4e63d724725ca8c019f696c0d86ad69453ac5bcbfd54ece3a99f717779` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/AmmBid.java | 3792 | `dd4c2c7dcbc0524c5f249472c52d75c27bbd5cc7c1bfbe33aafa4e57b5df83e8` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/AmmClawback.java | 1958 | `73bd1771ef4d90a60b19633bd05c45c09b642410e9d8717f0f8a0f7aa9eab293` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/AmmCreate.java | 1979 | `1bbcc25d0a39d6e562440c95cf426ddfcf5523ac23b4f0a550d953d2b9f3708b` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/AmmDelete.java | 1648 | `3a6f7d34e58ae488464400613a84c7dcad62bce81ff0f3fe052fbc3ddfa42b36` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/AmmDeposit.java | 3423 | `6a5f0c7d4f661409eda29f49aa844eb72952c06c1802ba0f404fedf185e621e7` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/AmmVote.java | 1906 | `21d4ace30a70e6bad18bb0f589e75df6bbb524f37f89c9e6311e21f2eac7c9bd` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/AmmWithdraw.java | 3143 | `cacd98be4b8799cd1d8964aef9cbadc3cbf0334ad8c1ce7940acb18c86720ea5` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/Amount.java | 6282 | `42436634e627ffb3fcec64099a8268a64d1a1e74322fc0ff79d0be2239f4b0ab` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/Batch.java | 21200 | `1f2aef1a67b205345fd712f71036e0e1108b82e57ffd8c5e69b1fff1c1ee9a05` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/BatchSigner.java | 5408 | `095a87d3900b7b562a9e69ffde1a05cefc94b424e5ed2acdef5a1b515f205bf5` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/BatchSignerWrapper.java | 2399 | `69650d77d2ef9485666e658e5bef4fab1c66401dcb80f32ae46c76a1f105d31f` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/CheckCancel.java | 2566 | `7270bc8bcb371bf70542cf3de379b1199beb772677a356923541a049c7aefbdb` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/CheckCash.java | 4346 | `52422cad022510d150008f7f0ceeeea0c8d3f1f7789f453c1600b6b2d8284975` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/CheckCreate.java | 3941 | `48b0f45c800869841f7bf26e937977635ed96dc86c27892b30f1ff51ace64598` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/Clawback.java | 1901 | `87c42944a7ed366daf27325af5f3c6e4833986a6103a20647860960ce28e73bb` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/ConfidentialMptClawback.java | 4861 | `790eeb56f16b445d864d0078c3e44d2b7c0a8090ef426f6634d0a0af123ac047` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/ConfidentialMptConvert.java | 7030 | `c45350244fa2259e30e5eca02b05939012549dc81df4a802056687d40641375f` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/ConfidentialMptConvertBack.java | 6252 | `f261f45ee28ea7067cdf55b4196f566259576d823a2cdb2a15821cd2499cbfd0` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/ConfidentialMptMergeInbox.java | 2899 | `0638f16a0d628b66095190f203f181b1eea90de69b2d271a0fc87ab43a854e62` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/ConfidentialMptSend.java | 7286 | `87455ec403f48744c693ad642de31377cd62be570239bbb90237a8afcd9d10f0` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/CounterpartySignature.java | 5628 | `25539954c940cc75555f6f92f8851802b690542bdbdbbdad961625b230fb95cd` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/Credential.java | 1907 | `e3145b08954a0430daba26ef1f3ad19351a2ca12bb1e0a4a7ccec19f20ae28fa` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/CredentialAccept.java | 1644 | `62f8d47cb55a54244ee5e9af9db57c4175df61047373b6f5940bc77690ad9f7f` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/CredentialCreate.java | 2250 | `fd3c087c598373e58bc2edc29878542927cb4729b377da4cf3e73a4335b8d6a8` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/CredentialDelete.java | 2118 | `79842e658f0d5d1a8c890b52dc26af53ddce0e729c48fa73c62b2dee4b669f83` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/CredentialWrapper.java | 1789 | `5b6c7385fdf168c8ccab6742dd00742d55a46f5640080256e16f315c57f783a6` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/CurrencyAmount.java | 5387 | `67dc94aaf420daf45f3abdfc099881337a1c6c12f31a527e19369095a32e4594` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/DelegateSet.java | 7438 | `93820023b2f2e6d0a41c6b0a22fa5e99d36fadd7569049574db568602ba99457` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/DepositPreAuth.java | 5950 | `dee415eec5fc0ce73edd17b6b3838c427b1697f596b939f17ac7744be10eb0c4` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/DidDelete.java | 1521 | `63184463d1bfc0f0e0e3267c159dcfcdaff22d3641ad71672cdd79c7f78ee643` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/DidSet.java | 2184 | `9e1872ba433cc1af64978d4a76634f8b5f6ea4be4f164ebd328460fb48ecfdcf` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/EnableAmendment.java | 3774 | `3689943f80b01194ccd10d4b2eafdccd1adc448cca4e75ca85ec82f092fbb8d7` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/EscrowCancel.java | 2995 | `0d2b7bb03f97865d0d9ee1ac504bfd50364a9fb364b4598c6c4754f6ca2ab645` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/EscrowCreate.java | 5525 | `8f78a66d94aacdedb91bcb8343f630e9248a9ab108b8fb165696a8aa759e1226` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/EscrowFinish.java | 19353 | `f5ee488b0cbc7a61ca8a2d0f4411921155ed91bb80b9970714cf258a19611ce4` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/GranularPermission.java | 4630 | `193207b35ac094fc36cf8ec7f92a45db73a24afbb8be2879d84e96f63be875b8` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/GranularPermissionValue.java | 2724 | `66a00d0b33c0356f1aab7f4e7ae9ea2de1ced99bfcb3a558be0324682e6d947f` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/IssuedCurrencyAmount.java | 4674 | `9d13afa9bd8727b6048337de3d057abb73fc9b3d26fb18a6e15f33c42b0ad7bd` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/LoanBrokerCoverClawback.java | 3956 | `e1e2a9dc5c28a734e548ed6a85d1ad8e94bbed6ec81579db1d155aa3a319a1cd` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/LoanBrokerCoverDeposit.java | 2055 | `d79ece83f0589670015fbd8f4c5df5db561860ff0a946ee71f6bb7b110dfbf74` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/LoanBrokerCoverWithdraw.java | 3584 | `dfb8a56be484c6ad3f3a72f84a06e3529f89d569eb35d1e05ed9120ec516e383` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/LoanBrokerDelete.java | 1692 | `3c655bc4729766b5e14adaae528f11f545bb3b596fa7f6b344c332157d9ca179` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/LoanBrokerSet.java | 5785 | `47276011de34be406ee8b527614ad5f3cb9c4ef434552090ecf4f5fc66293879` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/LoanDelete.java | 1606 | `72abd65826b00f76f884cd9e8e0f6a1fc2aa48c63bae3015aab20d31e8c20adb` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/LoanManage.java | 1996 | `8609aa3adff196c1d6f946919f2cbf352b1bf0b8902d05009316f614565393f9` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/LoanPay.java | 2257 | `ee81a7752d01b288af8870ee77e146a1b7a39bb6df23bbe2ba5bd39bd5b4c3f4` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/LoanSet.java | 10474 | `33d0d00b8adbdcf7187d6139ddd8831d7b116dcb3536b28a91978158cfb7ef78` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/Memo.java | 4651 | `b1f07312ddfefae293152ea84ae1a31c4fbb938b2bd406237dce31fd30e76bf5` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/MemoWrapper.java | 1754 | `49df5a3bd55f3024a4fd9d946b0f81be8e0c3927d85b2edfc58615dc9b0555c3` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/MpTokenAuthorize.java | 1511 | `d56941b6eebc60c27a6de8516be4b9387a3386d51e8a1c9eeb6c20c196d7f105` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/MpTokenIssuanceCreate.java | 5406 | `25e0779c0aeba501cf0093b6b801a1ac6a5a5eaedb09b2c80fef51070af22b67` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/MpTokenIssuanceDestroy.java | 1725 | `6d7cbd908b3af054fddee2adc4e28b5cbf0e791fd6348aa7904e4bcab7ec5ebc` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/MpTokenIssuanceSet.java | 8139 | `9ccac7df595c16a03efc589863f621897b85351ae535d485645d1f3c3917a418` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/MptCurrencyAmount.java | 2433 | `0cc27615220b959425bb5ae37421cada330d723342412ed94f0b7ee6aab7bd2a` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/NfTokenAcceptOffer.java | 5477 | `4e8c95eeccfef57bc7522e9645a269fbc5c0a78b417ba59d31fda1c8068a4582` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/NfTokenBurn.java | 3597 | `fa9776333affc8313fb440254ee192654393382c351dc4a3d89fc0877a640653` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/NfTokenCancelOffer.java | 3197 | `6df41f909f6f0bbca3792a941b996025e5a3284de9d37bb45e7d61c55b3e211d` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/NfTokenCreateOffer.java | 4381 | `d6bbf65d2ac14544b749fc2e14d88dbff6a57355ae11d5d0e8e52f48c359d7bb` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/NfTokenMint.java | 4115 | `da0352b1c938d5c3ac1175e2e68839dbe34ff2c157da57f3db799a0bbcc16ecb` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/OfferCancel.java | 2532 | `65473ec841dae9ba6f13a0a27f4edca70f5174530be3f5ac3463b96c4be08546` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/OfferCreate.java | 3791 | `db232da779847b5996414976cfbeb5f9c56cdef899747e4097efd34e65860d14` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/OracleDelete.java | 1600 | `3e61220e79c64f5889a5ce31ab0e43913a66b9891d3257708852c4720aa0f6d3` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/OracleSet.java | 3234 | `f39bbcba63e5514713ad162abbee3aa6c27c9ae95b1fc31228600d39f04db63f` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/PathStep.java | 2851 | `89831822f7af2bf4358e48cbaa80ea8a6e0428b9b2fed2b6c82a458fb35284a1` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/Payment.java | 6402 | `519d416c91faab9d25bde3763106e793b42a6b22f5bdbd816b8282f331e47d90` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/PaymentChannelClaim.java | 6424 | `3ac4763efe242b8eb356d483edf6e72afce1d72312b694ecd2a13975297d2069` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/PaymentChannelCreate.java | 4601 | `87723d7345190a81197883c43e8344365c5382b45e1c09acbaed9baee244c206` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/PaymentChannelFund.java | 3650 | `0ea262ad74cdc395611313a45fd8f7955af2d913a8f92699576c440e605da333` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/Permission.java | 4321 | `090147d3f8e19ba32ad1bba3574bf4e4267e98c90551d070bfc5640ad40d6bd6` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/PermissionedDomainDelete.java | 1470 | `3202b7ba1e355487fb1708527af2f523c927a4321762fad56b0e1624a9f8141c` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/PermissionedDomainSet.java | 2798 | `ab6c9a565d9e1fdad31b3600af4c319ce952a5916445447b540140178df00eaf` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/PriceData.java | 2293 | `f10d23a21d5e677b9bdd1e793fecafb1a3fea13c292ca008f50ae7f819595a4d` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/PriceDataWrapper.java | 837 | `76a3fdd472d8d5d64eec1f416c407467c53173874a8109e2a1e16fb836e6a612` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/RawTransactionWrapper.java | 3799 | `1fa3ae108a47330eed63abc0b9a86642c682e15942f336e8df9370a7610f6ea9` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/SetFee.java | 6487 | `b45c2829f1a37cc5d37c1ce1f8bf8d404ff7d14913b3af43466347302b943f20` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/SetRegularKey.java | 2878 | `8647e027abf377b5589346f23011b230e7a08dce081ac0b6dc04297a1c0b74f7` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/Signer.java | 2780 | `7775af53da77240ce9d2590821b2395e90b45fdd0c118c85d8ebee8ad8da7777` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/SignerListSet.java | 3225 | `3ffed09881727bfa4dc5e3c50c282b5b884a6c71260a88a542dc328634c2e9ff` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/SignerWrapper.java | 1991 | `0170fdb8f74d314109e09553fb187bee2f94c5efa9f7cb3b5f877d605c59ec08` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/SponsorSignature.java | 7176 | `fd71ac6a47160fcdb8238a2fde75a929aa6ac0e4008080b053dcab73bb035fda` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/SponsorshipSet.java | 10574 | `cd1d83b134751d3e74b61fd3966cbabd33ee11f8a9aeaeeb1c4e0ff5003e7c9e` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/SponsorshipTransfer.java | 7871 | `454b24e1840e66b99ba957372327c7a953685fe6f704e452e94fb8daa564f9f6` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/TicketCreate.java | 2526 | `fecdc4d2163dadae27357e6907aeeb39323f6eccb752d14c5304a9d31d35628f` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/Transaction.java | 27266 | `371170db77af255cee59b501fbfcd0a445c1eec8db42b493e8e8048792553243` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/TransactionMetadata.java | 4331 | `a987accc94d5aa49d77581b6904b896b914807279515670bfc25fb4a642851a0` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/TransactionResultCodes.java | 8975 | `726ceb41cd3e8fad479b94af0acc972afd111b5afde1623aed6dcc0353d8530e` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/TransactionType.java | 18787 | `d6031ce61c5529e5ef1a66b4e27b3f86ee361c9ac4262966459bf51bab6bf028` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/TransactionTypePermission.java | 2657 | `6292207fe36cf592989b0c2f2c7832522b0ad3b00bebc1d0e96f2fcc95079487` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/TrustSet.java | 3196 | `ff98a0db06f280307e5530ef1c2f35fe631bd9cb064da9e39f154f503a69b56f` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/UnknownTransaction.java | 2277 | `8bbca81077eedd1728d426df88f60ea11f9fd57b5b77d3c1a62aaa073ca6af8a` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/UnlModify.java | 4284 | `f98ad09d9f501a85d347e81d814fb5f1801935cd16a55757bd690c6f9effe18d` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/VaultClawback.java | 2212 | `06445fb4c9ff440f002c4a37115dc2ccb09001fb00995273b0d841ae6b222ade` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/VaultCreate.java | 6746 | `ecdb0531a975d5f1009eacefdb0909762f58479c05da7ab91ea98392e313b8ec` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/VaultDelete.java | 1904 | `94583e4f01ad71ebba64fab205b2fde87e7cd0da2d78071282c36455a048cae6` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/VaultDeposit.java | 1535 | `bf592d2dab0493c83010ea65b5a86a676010f56105ecdd6b5d14e9d9ddc2c59b` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/VaultKind.java | 2101 | `ee668dbaf70c2cd72cf1d6f3b4cf299048421f746d1945582663ad58cf4402a1` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/VaultSet.java | 2019 | `4af6d73b9aee249bea62d84a4c05e2690291b02230ba939286e1ff33ad086ded` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/VaultWithdraw.java | 3208 | `3a4b76d941f482086fb288c4ed80dafd382a8f5347e5179d73d857fd994e9754` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/WithdrawalPolicy.java | 1183 | `44d689c0d534c720465e67e9c947f64a8c66de8869b752dc06e00072ffc51e03` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/Wrappers.java | 45353 | `c0b8a1e73975f507c02c4bbb118a25dc4f24ef05b8c3c1df5f8737af5f32e34b` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/XChainAccountCreateCommit.java | 2553 | `c443d09ae0e17fb82da297c55b02a985df76f41d4ec5590b554a07a4a31368e8` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/XChainAddAccountCreateAttestation.java | 4440 | `67ee1e0572fdf151e95547b5ed276eac2d36956e0dd2e3d8139c0ef67f21f77b` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/XChainAddClaimAttestation.java | 4147 | `1bf70cde7cc92cff1445935b2df90be791d30d9ede92cc065ad73272479ba53c` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/XChainBridge.java | 1930 | `271df739e7082e1f37790f20c44182dd61ddee9e6c8f45a2e82a9c45c4d9cb70` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/XChainClaim.java | 2809 | `3cf9b0ce3dc02a79d2331bce1f6cfa8b2fa46f7248d6970f1ba03bbf79a266e2` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/XChainCommit.java | 2938 | `9b8c3f7e3eacd593fd5a012473864a07439dcc8f3eb9add94a85002472af1cda` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/XChainCreateBridge.java | 2348 | `7a191a1a00856a772f53bc3a40232f99b96c71e6199026fdc00a20bfe7593ffc` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/XChainCreateClaimId.java | 2147 | `d50c7319df3b20393b9bd52a4cfa1f331565044f3b674119a86e377acbe33c55` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/XChainModifyBridge.java | 2639 | `8720d8cce04b770a5964b06e5274971b84c1d96a7c5797ee5eb952445eeb5352` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/metadata/AffectedNode.java | 4060 | `47407bd0ad88298fd8e08b885eabbb8ddecd0011f46b33c43f24546d0e02178e` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/metadata/CreatedNode.java | 858 | `bbdd669fb6f7f26c67a097c87813efa6137e70281b3bfc8716663ff674e6e18c` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/metadata/DeletedNode.java | 1235 | `4df9407e24ad2541f7b06e03c2074032ac9621cb8d79ff88c1ab578e9cbca181` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/metadata/MetaAccountRootObject.java | 10326 | `72c5d4a16b300da35f20c3a546871d57908d9f7353db76f554cfad58b3e7e4cd` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/metadata/MetaAmmObject.java | 3542 | `97b589982732830532a7f596b567b7957febfa85211ec44a873f59468d5e960e` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/metadata/MetaAuctionSlot.java | 2808 | `95f1e593b61f2613927978d0f7be2bfe71480b4bb3c877c627313e7daa245094` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/metadata/MetaAuthAccount.java | 989 | `def383f754b63ead20a9657102457b7bb1d0494086f06e420cff87aeb79db5d7` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/metadata/MetaAuthAccountWrapper.java | 951 | `edd9a60d76d4967c2baa37526ac06d7317b662165ff0847eace6548ad88fbbd0` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/metadata/MetaBook.java | 1876 | `0ba56bfa50b18fde859b3dbab4ebf5fd5aff17f2fb11d69a0636ac0cd125dbfb` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/metadata/MetaBookWrapper.java | 1457 | `9c8354ae3ac640dd3b94361170dde8a6340fb7524abd9202900181aa14588d0f` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/metadata/MetaBridgeObject.java | 5552 | `2e7ae1e54bb625712e72f09f52c3ec76d933c674f8a4fc3e6ed7ad6a1ed68d7a` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/metadata/MetaCheckObject.java | 6731 | `cf601f08c8c6f5f0b934b673d05e4e7a860849b24a956b4d3d634fef403dd5f2` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/metadata/MetaCredential.java | 1887 | `56204a8968d9e210c4bd0aa7211c061b8d871a35e06f09def6b497b537f620ab` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/metadata/MetaCredentialObject.java | 5102 | `bd9644fd1451feb5cbf36644682b07101894f35aee1db483b87f8db4817e82c0` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/metadata/MetaCredentialWrapper.java | 1497 | `e1249515a47da03d3f496e7ae3639d6d76dd86dffa4453d2eb89a7740941cc05` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/metadata/MetaDelegateObject.java | 4511 | `6cb6ed696ff4f52d9fcca3c480308fe5e9c3236a7533ccc29b64d2a93d33fa1a` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/metadata/MetaDepositPreAuthObject.java | 4835 | `935ed0bf96a395b6f810989e95594a6ab7ed760546264c9da2d1f8bc180404d9` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/metadata/MetaDidObject.java | 3660 | `473bc182c0183c0f64f5c8652222f157994219ef9e06280837e7feb0f303263c` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/metadata/MetaEscrowObject.java | 9975 | `840e533f219f18b285eac5829371b4d04a97932c882b93a9120bf6bbb13ec20d` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/metadata/MetaLedgerEntryType.java | 5766 | `9c2166254a8fb5318b4b5cab194f5e0a768647139d19e5cbc598b8667b199600` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/metadata/MetaLedgerObject.java | 1280 | `4085f42bc52ea925596715cb891acdee72a3b6644825261951cf468ecb69ebaf` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/metadata/MetaLoanBrokerObject.java | 5582 | `aa15df4c95f25c62bb11b53d6584ffee3213b09bac5b37671c07d286ab414093` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/metadata/MetaLoanObject.java | 7857 | `8c9764ca9919c0a9a0e629d1ac340997418a1f5fe946413f2915572e1ad3ae91` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/metadata/MetaMpTokenIssuanceObject.java | 5099 | `b22ff5ebb1322cb192cd107b310b4cc594f0b0d15e8be20a0b70ea01529bd728` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/metadata/MetaMpTokenObject.java | 4648 | `cc4e5c6dc0743583f0e56b681f1a30815da58eb7af3363db10376067e92f8192` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/metadata/MetaNfTokenOfferObject.java | 4561 | `5ec936ee21b2d62946317e4e402585cab6b64dc143ba2fae861726bfa84d6e49` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/metadata/MetaNfTokenPageObject.java | 3177 | `ecec3986e81f956caa7735014bf187de3a176dc1aaa73a631d44c1726a227e3e` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/metadata/MetaOfferObject.java | 5209 | `b4e1630a1b30cfcaf8443d7577149c82fa6afb98cfcd07f7707ad4e4437fad39` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/metadata/MetaOracleObject.java | 3705 | `d46028250d45a5cc1092b93b2ae68ff5e77daa0f6acc0de28d760a0dbcd6ac7d` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/metadata/MetaPayChannelObject.java | 9523 | `f430f60797d04879183ab16ce912f42678246995b5ee5a6c1e70da166b77f166` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/metadata/MetaPermissionedDomainObject.java | 3681 | `e03a43390b00ae4f442143c2a008226761ead4e4c899d2c35d624a6b1e43f6ae` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/metadata/MetaRippleStateObject.java | 7972 | `c1927b0cd13f419cbc8578ef7513875029baf5928c8471b50107aad5d0effba6` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/metadata/MetaSignerEntry.java | 2143 | `f21b9ac606a5a0318679dfc3dd5e3112c532d488c435345370ec20392b2acb47` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/metadata/MetaSignerEntryWrapper.java | 1606 | `9f1438b73b03ebfb37e12091b2faffe9da9f15b494d517875d1ed85c99172650` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/metadata/MetaSignerListObject.java | 4690 | `b54ca28e1934fefb4cedc11b9b355e12d7d2a629b193a16e106a53c0d982b82e` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/metadata/MetaSponsorshipObject.java | 4372 | `b729196eb54c3c90308f4ca2e7ca07b35a1dbc45c0956cfb57791c71c7fa2724` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/metadata/MetaTicketObject.java | 3437 | `28c311794d7b5a9179c1399c50cd0b884bc3627b2f9c2f43a7147055077ab9bb` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/metadata/MetaUnknownObject.java | 1438 | `b70714c8d1467893e277b83c4cc8eec56e61190690a674e0e565f697aa3ddf24` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/metadata/MetaVaultObject.java | 5678 | `214759918dfa117bbd81c8168ce40731c44ca711bdd451e040cd79c59fd9d903` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/metadata/MetaVoteEntry.java | 1427 | `536c9e54b5158d73be0794723bbd58385dfb55974701a8f9cc42bc34f74eed65` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/metadata/MetaVoteEntryWrapper.java | 930 | `1d7cfc47f9e23b05507ee01dfd5a28b1304ecc7087e47a7358f4fa750403c3dd` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/metadata/MetaXChainClaimAttestation.java | 1030 | `4ad5603ad3a1676de436c1f10b0cefb080ef927545c2b9fa220163d8d21edf60` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/metadata/MetaXChainClaimProofSig.java | 2500 | `25b200590b5a91f6dfaace1e0123116a907ffb0c96c7001e3e5c775047da7975` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/metadata/MetaXChainCreateAccountAttestation.java | 1017 | `a213f3b4f840d3cb842b93110507fe44e8d1e52865ee945c612cbb0cabcc5a68` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/metadata/MetaXChainCreateAccountProofSig.java | 2984 | `ac2348f0b9be86e852b98b24030ad1fe405917a289923b7c3d4273e8c26d4faa` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/metadata/MetaXChainOwnedClaimIdObject.java | 5483 | `949b9be758db8e49441399504e5c69b26e5ed5c2244e17f4c741a7f3107199c4` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/metadata/MetaXChainOwnedCreateAccountClaimIdObject.java | 4373 | `e1bcfcfa79341ebf0480c056c226fd6c8df8e524e5f882ee61531416e6d6b7bc` | 0 |
| xrpl4j-core/src/main/java/org/xrpl/xrpl4j/model/transactions/metadata/ModifiedNode.java | 2328 | `a703eefca9c906c0fa9e87d5ec433a3f587377d427ccab5b94ee198cfc2b8f63` | 0 |
| xrpl4j-coverage/pom.xml | 3165 | `9341e2c996b72a80e37e320cc5d7d246a733fb35ed4b8221e53aa399927a311a` | 0 |
| xrpl4j-mpt-crypto/pom.xml | 2307 | `a3c600b7b294f82b87f058f71c9ffde8d1875e23613a1dc9b1d9693795a31496` | 0 |
