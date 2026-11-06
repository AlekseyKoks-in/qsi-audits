# Security & Post-Quantum Readiness Audit Report

**Project:** aptos-core @ 81d89f428fe8 · Aptos Labs — public repository (passive review)
| | |
|---|---|
| Organization | QSI |
| Report date | 2026-11-06 16:20 UTC |
| Report version | 1 |
| Audit run | 30269b00-7b13-4dea-be58-d53a0e2a5767 (Document audit) |
| Analyzer engine | qsi-engine 1.3.0 |
| Risk profile | Crypto exchange, custodian or wallet |
| Content SHA-256 | `496bbf2c0ceaa6407d995b8152ee8fd44f8f95ed1f641fbd08068a5bb313751f` |
| Signature key (Ed25519, SHA-256 fingerprint; the signature is the separate file report.sig.json) | `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e` |
> This report presents automated and documented analysis results for the stated scope. It is not a legal opinion, a certification or an attestation of compliance with any standard.

## 1. Executive summary

- Critical: **0**
- High: **0**
- Medium: **9**
- Low: **0**
- Info: **0**

- Confirmed technical vulnerability: 0
- Known vulnerable component: 0
- Confirmed configuration error: 0
- Potential cryptographic risk: 0
- Long-term post-quantum risk: 9
- Improvement recommendation: 0
- Insufficient data: 0

Mosca's inequality (x + y > z): x = 10, y = 5, z = 8 → migration would finish too late under this scenario. _z is a planning assumption chosen per risk profile, not a prediction. A cryptographically relevant quantum computer is not publicly known to exist today._

**Post-quantum maturity: Level 2 of 4 — post-quantum in use outside the critical paths.** Next step: Extend post-quantum protection to the critical roles that stay classical, starting with what can be recorded today (wrapped keys, channel key exchange).

## 2. Scope and boundaries

Mode: Document audit

Repository: <https://github.com/aptos-labs/aptos-core> @ `81d89f428fe8e4b69d53b4916993e9a930afc37c` — evidence links open the lines at this commit.

336 files, 3667051 bytes in total, 8 redaction(s); the per-file SHA-256 list is in appendix C.

## 3. Methodology

| Area | Status | Count | Examples |
|---|---|---|---|
| source_code | checked | 331 | aptos-move/framework/src/aptos.rs: 223 lines scanned with 16 rule patterns and 267 registry patterns; aptos-move/framework/src/built_package.rs: 773 lines scanned with 16 rule patterns and 267 registry patterns; aptos-move/framework/src/chunked_publish.rs: 223 lines scanned with 16 rule patterns and 267 registry patterns |
| dependencies | checked | 4 | crates/aptos-crypto/Cargo.toml: 78 dependencies parsed (0 pinned); keyless/pepper/common/Cargo.toml: 18 dependencies parsed (0 pinned); keyless/pepper/service/Cargo.toml: 36 dependencies parsed (0 pinned) |
| secrets | checked | 3 | crates/aptos-crypto/src/x25519.rs: 2 redacted value(s) not reported (comments, test modules, fixture declarations, placeholders, values the source annotates as published, or hex values not bound to a secret name); types/src/network_address/mod.rs: value(s) at line(s) 908 (test_network_address_display), 1069 (test_find_noise_proto), 1089 (test_parse_handshake) are declared inside a fixture and treated as test data, although the file itself is not test code; types/src/network_address/mod.rs: 5 redacted value(s) not reported (comments, test modules, fixture declarations, placeholders, values the source annotates as published, or hex values not bound to a secret name) |
| keys | checked | 1 | types/src/jwks/rsa/insecure_test_jwk_private_key.txt: private key block at line 1 is not reported: its path marks it as a non-production key ("insecure") |
| certificates_and_keys | checked | 1 | types/src/jwks/rsa/insecure_test_jwk_private_key.txt: certificates/keys parsed |
| entropy | checked | 1 | random-number generation: 331 code files read with 0 macro definitions from the tree; 0 ineffective guard(s), 0 weak random-bytes provider(s), 0 weak key-generation site(s) |
| osv_advisories | not checked | 1 | no exactly pinned versions to query |

_Long lists are grouped here; the full per-file list is in the JSON report, signed with the same key._

## 4. Assets examined and not examined

- osv_advisories — not checked: no exactly pinned versions to query

## 5. Architecture overview

Static review of the source tree aptos-core at 81d89f428fe8e4b69d53b4916993e9a930afc37c. 336 files analysed; of 625 files, 95 are test, fuzzing, benchmark or example code and were left out, 194 are not read by any analyzer, 0 exceed the per-file limit and 0 did not fit the total limit. The review was restricted to 5 path(s) of the repository: aptos-move/framework/aptos-framework/sources, aptos-move/framework/src, crates/aptos-crypto, keyless, types; 22057 files outside them were not read. Files no analyzer reads include: aptos-move/framework/aptos-framework/sources/account/account.move, aptos-move/framework/aptos-framework/sources/account/account.spec.move, aptos-move/framework/aptos-framework/sources/account/account_abstraction.move, aptos-move/framework/aptos-framework/sources/account/account_abstraction.spec.move, aptos-move/framework/aptos-framework/sources/account/auth_data.move. No requests were sent to the owner's systems.

## 6. Overall security posture

- Indicative posture index: **100** / 100 — _Derived from findings in scope (confirmed and potential issues weighted by severity). Indicative only; not comparable across differently scoped audits._
- Quantum-vulnerable share of inventory: 60.4%

## 7. Detailed findings

### QSI-2026-19659 — Quantum-vulnerable BLS12-381: transaction and message signing (2 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:BLS12-381:transaction_signing`
- Data source: crates/aptos-crypto/src/bls12381/bls12381_keys.rs
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.3.0 · 2026-11-06 16:20 UTC
- Priority score: 35.6 / 100
- CVSS v3.1: not applicable

3 reference(s) to BLS12-381 across 2 file(s), e.g. crates/aptos-crypto/src/bls12381/bls12381_keys.rs:77. Role, judged from paths, function names and nearby code: transaction and message signing. A CRQC derives the private key from a public key that is already known (on chain after the first spend, in reused addresses): funds and approvals controlled by these keys need a migration path.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open crates/aptos-crypto/src/bls12381/bls12381_keys.rs:77 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [crates/aptos-crypto/src/bls12381/bls12381_keys.rs](https://github.com/aptos-labs/aptos-core/blob/81d89f428fe8e4b69d53b4916993e9a930afc37c/crates/aptos-crypto/src/bls12381/bls12381_keys.rs#L77) · line 77 · SHA-256 f86b41febe322eda289a9b3744910f9f56e1842a57985dd8f18e9dfde490efc2_

```
   76 |     pub fn aggregate(pubkeys: Vec<&Self>) -> Result<PublicKey> {
   77 |         let blst_pubkeys: Vec<_> = pubkeys.iter().map(|pk| &pk.pubkey).collect();
   78 | 
```

_file_excerpt · [crates/aptos-crypto/src/bls12381/bls12381_keys.rs](https://github.com/aptos-labs/aptos-core/blob/81d89f428fe8e4b69d53b4916993e9a930afc37c/crates/aptos-crypto/src/bls12381/bls12381_keys.rs#L80) · line 80 · SHA-256 a99c05717793c659435d625fc91a078fa8de99cac0b7c2f81426a4891e0dba25_

```
   79 |         // CRYPTONOTE(Alin): We assume the PKs have had their PoPs verified and thus have also been subgroup-checked
   80 |         let aggpk = blst::min_pk::AggregatePublicKey::aggregate(&blst_pubkeys[..], false)
   81 |             .map_err(|e| anyhow!("{:?}", e))?;
```

_file_excerpt · [crates/aptos-crypto/src/constant_time/zkcrypto_scalar_mul.rs](https://github.com/aptos-labs/aptos-core/blob/81d89f428fe8e4b69d53b4916993e9a930afc37c/crates/aptos-crypto/src/constant_time/zkcrypto_scalar_mul.rs#L4) · line 4 · SHA-256 221f1dca25f14b9dfb0bda3a9eef2c447551e2ee404ab82af2906b77afbe582c_

```
    3 | 
    4 | use bls12_381::{G1Projective, Scalar};
    5 | use dudect_bencher::{
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains adopt them.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-19660 — Quantum-vulnerable Ed25519: transaction and message signing (10 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:Ed25519:transaction_signing`
- Data source: crates/aptos-crypto/src/ed25519/ed25519_keys.rs
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.3.0 · 2026-11-06 16:20 UTC
- Priority score: 35.6 / 100
- CVSS v3.1: not applicable

151 reference(s) to Ed25519 across 10 file(s), e.g. crates/aptos-crypto/src/ed25519/ed25519_keys.rs:9. Role, judged from paths, function names and nearby code: transaction and message signing. A CRQC derives the private key from a public key that is already known (on chain after the first spend, in reused addresses): funds and approvals controlled by these keys need a migration path.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open crates/aptos-crypto/src/ed25519/ed25519_keys.rs:9 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [crates/aptos-crypto/src/ed25519/ed25519_keys.rs](https://github.com/aptos-labs/aptos-core/blob/81d89f428fe8e4b69d53b4916993e9a930afc37c/crates/aptos-crypto/src/ed25519/ed25519_keys.rs#L9) · line 9 · SHA-256 adf76b09b67a86ab80f62343703cd06f08aaa6ef2d74c838afbaf3087a568625_

```
    8 | use crate::{
    9 |     ed25519::{Ed25519Signature, ED25519_PRIVATE_KEY_LENGTH, ED25519_PUBLIC_KEY_LENGTH},
   10 |     hash::CryptoHash,
```

_file_excerpt · [crates/aptos-crypto/src/ed25519/ed25519_keys.rs](https://github.com/aptos-labs/aptos-core/blob/81d89f428fe8e4b69d53b4916993e9a930afc37c/crates/aptos-crypto/src/ed25519/ed25519_keys.rs#L16) · line 16 · SHA-256 1caccba153f57a757992b88183d03a08f2b137bc1eed9afe190890307f3f240e_

```
   15 | use curve25519_dalek::{edwards::CompressedEdwardsY, scalar::Scalar};
   16 | use ed25519_dalek::ExpandedSecretKey;
   17 | #[cfg(any(test, feature = "fuzzing"))]
```

_file_excerpt · [crates/aptos-crypto/src/ed25519/ed25519_keys.rs](https://github.com/aptos-labs/aptos-core/blob/81d89f428fe8e4b69d53b4916993e9a930afc37c/crates/aptos-crypto/src/ed25519/ed25519_keys.rs#L24) · line 24 · SHA-256 1a0100275641151db47cb652da5dffeeadab86a7c7dce2b1bbae80b7b138b328_

```
   23 | #[derive(DeserializeKey, SerializeKey, SilentDebug, SilentDisplay)]
   24 | pub struct Ed25519PrivateKey(pub(crate) ed25519_dalek::SecretKey);
   25 | 
```

_file_excerpt · [crates/aptos-crypto/src/ed25519/ed25519_sigs.rs](https://github.com/aptos-labs/aptos-core/blob/81d89f428fe8e4b69d53b4916993e9a930afc37c/crates/aptos-crypto/src/ed25519/ed25519_sigs.rs#L7) · line 7 · SHA-256 e348dba0532f4e56f86d5b2e1db90e28010ed349c9accf0f2f0204c73a272062_

```
    6 | use crate::{
    7 |     ed25519::{Ed25519PrivateKey, Ed25519PublicKey, ED25519_SIGNATURE_LENGTH, L},
    8 |     hash::CryptoHash,
```

_file_excerpt · [crates/aptos-crypto/src/ed25519/ed25519_sigs.rs](https://github.com/aptos-labs/aptos-core/blob/81d89f428fe8e4b69d53b4916993e9a930afc37c/crates/aptos-crypto/src/ed25519/ed25519_sigs.rs#L19) · line 19 · SHA-256 7c9df4c2d607763e63885116d7333c8f1ec08aebc1c8cec80201faf59a31672d_

```
   18 | #[derive(DeserializeKey, Clone, SerializeKey)]
   19 | pub struct Ed25519Signature(pub(crate) ed25519_dalek::Signature);
   20 | 
```

_file_excerpt · [crates/aptos-crypto/src/ed25519/ed25519_sigs.rs](https://github.com/aptos-labs/aptos-core/blob/81d89f428fe8e4b69d53b4916993e9a930afc37c/crates/aptos-crypto/src/ed25519/ed25519_sigs.rs#L44) · line 44 · SHA-256 2d4aff20c28e007490dbb4df38c52c7ce6cf4f507647f7fbf72494e771ad4a64_

```
   43 |     ) -> std::result::Result<Ed25519Signature, CryptoMaterialError> {
   44 |         match ed25519_dalek::Signature::try_from(bytes) {
   45 |             Ok(dalek_signature) => Ok(Ed25519Signature(dalek_signature)),
```

_file_excerpt · [crates/aptos-crypto/src/ed25519/mod.rs](https://github.com/aptos-labs/aptos-core/blob/81d89f428fe8e4b69d53b4916993e9a930afc37c/crates/aptos-crypto/src/ed25519/mod.rs#L34) · line 34 · SHA-256 4109af929d07df4dac5c3148e82f383831c21b4c7a72e67752f1cb2e414a1de4_

```
   33 | /// The length of the Ed25519PrivateKey
   34 | pub const ED25519_PRIVATE_KEY_LENGTH: usize = ed25519_dalek::SECRET_KEY_LENGTH;
   35 | /// The length of the Ed25519PublicKey
```

_file_excerpt · [crates/aptos-crypto/src/ed25519/mod.rs](https://github.com/aptos-labs/aptos-core/blob/81d89f428fe8e4b69d53b4916993e9a930afc37c/crates/aptos-crypto/src/ed25519/mod.rs#L36) · line 36 · SHA-256 e36e845052f25c992bc097ff2643a8919a542814ca3d80a30c23bbdeefd221d2_

```
   35 | /// The length of the Ed25519PublicKey
   36 | pub const ED25519_PUBLIC_KEY_LENGTH: usize = ed25519_dalek::PUBLIC_KEY_LENGTH;
   37 | /// The length of the Ed25519Signature
```

_file_excerpt · [crates/aptos-crypto/src/ed25519/mod.rs](https://github.com/aptos-labs/aptos-core/blob/81d89f428fe8e4b69d53b4916993e9a930afc37c/crates/aptos-crypto/src/ed25519/mod.rs#L38) · line 38 · SHA-256 fa75a35cf657ddee121a387d195c85f31e9bd4ff176e92985131bd3a19a2caed_

```
   37 | /// The length of the Ed25519Signature
   38 | pub const ED25519_SIGNATURE_LENGTH: usize = ed25519_dalek::SIGNATURE_LENGTH;
   39 | 
```

_file_excerpt · [crates/aptos-crypto/src/multi_ed25519.rs](https://github.com/aptos-labs/aptos-core/blob/81d89f428fe8e4b69d53b4916993e9a930afc37c/crates/aptos-crypto/src/multi_ed25519.rs#L10) · line 10 · SHA-256 0d5facec0d4dac56115065a9c632c1ed1a25aaa7e14a7ba15b8ac6bb9921271d_

```
    9 | use crate::{
   10 |     ed25519::{
   11 |         Ed25519PrivateKey, Ed25519PublicKey, Ed25519Signature, ED25519_PRIVATE_KEY_LENGTH,
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains adopt them.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-19662 — Quantum-vulnerable X25519: channel key exchange (TLS, Noise, handshakes) (2 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:X25519:channel`
- Data source: crates/aptos-crypto/src/noise.rs
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.3.0 · 2026-11-06 16:20 UTC
- Priority score: 35.6 / 100
- CVSS v3.1: not applicable

36 reference(s) to X25519 across 2 file(s), e.g. crates/aptos-crypto/src/noise.rs:65. Role, judged from paths, function names and nearby code: channel key exchange (TLS, Noise, handshakes). Traffic protected by this key exchange can be recorded now and decrypted later; a hybrid exchange keeps the classical guarantees and adds post-quantum ones.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open crates/aptos-crypto/src/noise.rs:65 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [crates/aptos-crypto/src/noise.rs](https://github.com/aptos-labs/aptos-core/blob/81d89f428fe8e4b69d53b4916993e9a930afc37c/crates/aptos-crypto/src/noise.rs#L65) · line 65 · SHA-256 21f98045a9d7699e76ccf75949f7da21bb9582d0e9cce6c86a823b43280710bd_

```
   64 | 
   65 | use crate::{hash::HashValue, hkdf::Hkdf, traits::Uniform as _, x25519, ValidCryptoMaterial};
   66 | use ring::aead::{self, Aad, LessSafeKey, UnboundKey};
```

_file_excerpt · [crates/aptos-crypto/src/noise.rs](https://github.com/aptos-labs/aptos-core/blob/81d89f428fe8e4b69d53b4916993e9a930afc37c/crates/aptos-crypto/src/noise.rs#L104) · line 104 · SHA-256 c42db5b8ba200f00cea1b1af6a1e59e326dfdf1720dc5852f8111f8c7b23abc4_

```
  103 |     // e
  104 |     let e_len = x25519::PUBLIC_KEY_SIZE;
  105 |     // encrypted s
```

_file_excerpt · [crates/aptos-crypto/src/noise.rs](https://github.com/aptos-labs/aptos-core/blob/81d89f428fe8e4b69d53b4916993e9a930afc37c/crates/aptos-crypto/src/noise.rs#L106) · line 106 · SHA-256 b77110997bf970e95f378f3e430067fa6d2c6e9e44a6aa6d7afc327b132c655d_

```
  105 |     // encrypted s
  106 |     let enc_s_len = encrypted_len(x25519::PUBLIC_KEY_SIZE);
  107 |     // encrypted payload
```

_file_excerpt · [types/src/network_address/mod.rs](https://github.com/aptos-labs/aptos-core/blob/81d89f428fe8e4b69d53b4916993e9a930afc37c/types/src/network_address/mod.rs#L8) · line 8 · SHA-256 4e7aafdd34a2f6c3daa63b8613f3d54065e58c42599434b49c750a80c7e3b156_

```
    7 |     traits::{CryptoMaterialError, ValidCryptoMaterialStringExt},
    8 |     x25519,
    9 | };
```

_file_excerpt · [types/src/network_address/mod.rs](https://github.com/aptos-labs/aptos-core/blob/81d89f428fe8e4b69d53b4916993e9a930afc37c/types/src/network_address/mod.rs#L122) · line 122 · SHA-256 74a6f19114396ccb2c0c1d35129e8a6590a3243fe4c2ba18b831a8eabde622e7_

```
  121 |     // human-readable x25519::PublicKey is lower-case hex encoded
  122 |     NoiseIK(x25519::PublicKey),
  123 |     // TODO(philiphayes): use actual handshake::MessagingProtocolVersion. we
```

_file_excerpt · [types/src/network_address/mod.rs](https://github.com/aptos-labs/aptos-core/blob/81d89f428fe8e4b69d53b4916993e9a930afc37c/types/src/network_address/mod.rs#L166) · line 166 · SHA-256 614fe3ed0c2b75b2f74023381798dd798583e5bc0022e8571275e8155143e354_

```
  165 | 
  166 |     #[error("error parsing x25519 public key: {0}")]
  167 |     ParseX25519PubkeyError(#[from] CryptoMaterialError),
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Move the handshake to a hybrid key exchange (X25519MLKEM768 in TLS 1.3; a hybrid KEM in Noise-based protocols).

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-19663 — Quantum-vulnerable ECDSA: transaction and message signing (3 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:ECDSA:transaction_signing`
- Data source: crates/aptos-crypto/src/secp256k1_ecdsa.rs
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.3.0 · 2026-11-06 16:20 UTC
- Priority score: 35.6 / 100
- CVSS v3.1: not applicable

14 reference(s) to ECDSA across 3 file(s), e.g. crates/aptos-crypto/src/secp256k1_ecdsa.rs:120. Role, judged from paths, function names and nearby code: transaction and message signing. A CRQC derives the private key from a public key that is already known (on chain after the first spend, in reused addresses): funds and approvals controlled by these keys need a migration path.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open crates/aptos-crypto/src/secp256k1_ecdsa.rs:120 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [crates/aptos-crypto/src/secp256k1_ecdsa.rs](https://github.com/aptos-labs/aptos-core/blob/81d89f428fe8e4b69d53b4916993e9a930afc37c/crates/aptos-crypto/src/secp256k1_ecdsa.rs#L120) · line 120 · SHA-256 0a1fc93a27f369c174809d52f96d68567e75108bf4af7db9ab12f33309312dfb_

```
  119 | impl ValidCryptoMaterial for PrivateKey {
  120 |     const AIP_80_PREFIX: &'static str = "secp256k1-priv-";
  121 | 
```

_file_excerpt · [crates/aptos-crypto/src/secp256k1_ecdsa.rs](https://github.com/aptos-labs/aptos-core/blob/81d89f428fe8e4b69d53b4916993e9a930afc37c/crates/aptos-crypto/src/secp256k1_ecdsa.rs#L186) · line 186 · SHA-256 5fc60fc076c992614ddae3137a4c2774ba1d79a69368c280f4b82969a02a1d0c_

```
  185 | impl ValidCryptoMaterial for PublicKey {
  186 |     const AIP_80_PREFIX: &'static str = "secp256k1-pub-";
  187 | 
```

_file_excerpt · [crates/aptos-crypto/src/secp256k1_ecdsa.rs](https://github.com/aptos-labs/aptos-core/blob/81d89f428fe8e4b69d53b4916993e9a930afc37c/crates/aptos-crypto/src/secp256k1_ecdsa.rs#L289) · line 289 · SHA-256 77cce12d3bdba7700d8f5431dce16cccfb1eb7eaf8e08e29177a821bc85a3dea_

```
  288 | impl ValidCryptoMaterial for Signature {
  289 |     const AIP_80_PREFIX: &'static str = "secp256k1-sig-";
  290 | 
```

_file_excerpt · [crates/aptos-crypto/src/secp256r1_ecdsa/secp256r1_ecdsa_keys.rs](https://github.com/aptos-labs/aptos-core/blob/81d89f428fe8e4b69d53b4916993e9a930afc37c/crates/aptos-crypto/src/secp256r1_ecdsa/secp256r1_ecdsa_keys.rs#L26) · line 26 · SHA-256 84af77bba23df6b8d90baf6a3498d3b5a95a1b4e3a08d61ffa1e1116262322f5_

```
   25 | #[key_name("Secp256r1EcdsaPrivateKey")]
   26 | pub struct PrivateKey(pub(crate) p256::ecdsa::SigningKey);
   27 | 
```

_file_excerpt · [crates/aptos-crypto/src/secp256r1_ecdsa/secp256r1_ecdsa_keys.rs](https://github.com/aptos-labs/aptos-core/blob/81d89f428fe8e4b69d53b4916993e9a930afc37c/crates/aptos-crypto/src/secp256r1_ecdsa/secp256r1_ecdsa_keys.rs#L42) · line 42 · SHA-256 67a910a2cba142805ca03842c07ad5995bcd28afd9755e1dc58ec17f8d277806_

```
   41 | #[key_name("Secp256r1EcdsaPublicKey")]
   42 | pub struct PublicKey(pub(crate) p256::ecdsa::VerifyingKey);
   43 | 
```

_file_excerpt · [crates/aptos-crypto/src/secp256r1_ecdsa/secp256r1_ecdsa_keys.rs](https://github.com/aptos-labs/aptos-core/blob/81d89f428fe8e4b69d53b4916993e9a930afc37c/crates/aptos-crypto/src/secp256r1_ecdsa/secp256r1_ecdsa_keys.rs#L66) · line 66 · SHA-256 77b6daa36734653a5846b1caa099fbc550c118768f7bd39749cf49d52dffaa0b_

```
   65 |     ) -> std::result::Result<PrivateKey, CryptoMaterialError> {
   66 |         match p256::ecdsa::SigningKey::from_slice(bytes) {
   67 |             Ok(p256_secret_key) => Ok(PrivateKey(p256_secret_key)),
```

_file_excerpt · [crates/aptos-crypto/src/secp256r1_ecdsa/secp256r1_ecdsa_sigs.rs](https://github.com/aptos-labs/aptos-core/blob/81d89f428fe8e4b69d53b4916993e9a930afc37c/crates/aptos-crypto/src/secp256r1_ecdsa/secp256r1_ecdsa_sigs.rs#L24) · line 24 · SHA-256 a323ce9f251b5a44ced790963b723501b8adabadc96888ad9a7fbfad5c039566_

```
   23 | #[key_name("Secp256r1EcdsaSignature")]
   24 | pub struct Signature(pub(crate) p256::ecdsa::Signature);
   25 | 
```

_file_excerpt · [crates/aptos-crypto/src/secp256r1_ecdsa/secp256r1_ecdsa_sigs.rs](https://github.com/aptos-labs/aptos-core/blob/81d89f428fe8e4b69d53b4916993e9a930afc37c/crates/aptos-crypto/src/secp256r1_ecdsa/secp256r1_ecdsa_sigs.rs#L41) · line 41 · SHA-256 870bc135c86c31b1a04131454f9174df611635be94fbea23c9df58f60f7a1f7a_

```
   40 |     ) -> std::result::Result<Signature, CryptoMaterialError> {
   41 |         match p256::ecdsa::Signature::try_from(bytes) {
   42 |             Ok(p256_signature) => Ok(Signature(p256_signature)),
```

_file_excerpt · [crates/aptos-crypto/src/secp256r1_ecdsa/secp256r1_ecdsa_sigs.rs](https://github.com/aptos-labs/aptos-core/blob/81d89f428fe8e4b69d53b4916993e9a930afc37c/crates/aptos-crypto/src/secp256r1_ecdsa/secp256r1_ecdsa_sigs.rs#L98) · line 98 · SHA-256 3f403f5ecdb50dfc7676ddf953a25712ebbf6649c2f9e3f0318c7529c0468f98_

```
   97 |         let new_s_nonzero = NonZeroScalar::new(new_s).unwrap();
   98 |         let new_sig = p256::ecdsa::Signature::from_scalars(r, new_s_nonzero).unwrap();
   99 |         Signature(new_sig)
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains adopt them.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-19667 — Quantum-vulnerable BN254 (alt_bn128): transaction and message signing (1 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:BN254 (alt_bn128):transaction_signing`
- Data source: types/src/keyless/mod.rs
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.3.0 · 2026-11-06 16:20 UTC
- Priority score: 35.6 / 100
- CVSS v3.1: not applicable

2 reference(s) to BN254 (alt_bn128) across 1 file(s), e.g. types/src/keyless/mod.rs:17. Role, judged from paths, function names and nearby code: transaction and message signing. A CRQC derives the private key from a public key that is already known (on chain after the first spend, in reused addresses): funds and approvals controlled by these keys need a migration path.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open types/src/keyless/mod.rs:17 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [types/src/keyless/mod.rs](https://github.com/aptos-labs/aptos-core/blob/81d89f428fe8e4b69d53b4916993e9a930afc37c/types/src/keyless/mod.rs#L17) · line 17 · SHA-256 cbc533ba4a0ce3f09b8065b0bbeb02e7698f15ef6145e4fd754d42bf0ce1d9b5_

```
   16 | use aptos_crypto_derive::{BCSCryptoHash, CryptoHasher};
   17 | use ark_bn254::Bn254;
   18 | use ark_groth16::PreparedVerifyingKey;
```

_file_excerpt · [types/src/keyless/mod.rs](https://github.com/aptos-labs/aptos-core/blob/81d89f428fe8e4b69d53b4916993e9a930afc37c/types/src/keyless/mod.rs#L63) · line 63 · SHA-256 ba7a34f492e7d3a1c0740b7e81dac32c308ebe5fea669e29b5e31dbc995f6a32_

```
   62 | /// A VK that we use often for keyless e2e tests and smoke tests.
   63 | pub static VERIFICATION_KEY_FOR_TESTING: Lazy<PreparedVerifyingKey<Bn254>> =
   64 |     Lazy::new(prepared_vk_for_testing);
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains adopt them.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-19661 — Quantum-vulnerable X25519: role not determined (3 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:X25519:general`
- Data source: crates/aptos-crypto/src/lib.rs
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.3.0 · 2026-11-06 16:20 UTC
- Priority score: 34.2 / 100
- CVSS v3.1: not applicable

17 reference(s) to X25519 across 3 file(s), e.g. crates/aptos-crypto/src/lib.rs:34. Role, judged from paths, function names and nearby code: role not determined. The code does not show what the keys protect; review decides the priority.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open crates/aptos-crypto/src/lib.rs:34 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [crates/aptos-crypto/src/lib.rs](https://github.com/aptos-labs/aptos-core/blob/81d89f428fe8e4b69d53b4916993e9a930afc37c/crates/aptos-crypto/src/lib.rs#L34) · line 34 · SHA-256 f134d93afe02965c942aabb6047efed4da543bcb252f8809256b8b68023bd847_

```
   33 | pub mod weighted_config;
   34 | pub mod x25519;
   35 | 
```

_file_excerpt · [crates/aptos-crypto/src/x25519.rs](https://github.com/aptos-labs/aptos-core/blob/81d89f428fe8e4b69d53b4916993e9a930afc37c/crates/aptos-crypto/src/x25519.rs#L35) · line 35 · SHA-256 cd421b6ecb48ccae14cf74794f6dc5d3e6e4604dad96c9a86e09924cf387a2c6_

```
   34 |     traits::{self, CryptoMaterialError, ValidCryptoMaterial, ValidCryptoMaterialStringExt},
   35 |     x25519,
   36 | };
```

_file_excerpt · [crates/aptos-crypto/src/x25519.rs](https://github.com/aptos-labs/aptos-core/blob/81d89f428fe8e4b69d53b4916993e9a930afc37c/crates/aptos-crypto/src/x25519.rs#L49) · line 49 · SHA-256 f36c219d0438d9571c16a3e24335b85bdeb2d9d3f76329bf3b30f516d0a36b2d_

```
   48 | //
   49 | pub use x25519_dalek;
   50 | 
```

_file_excerpt · [crates/aptos-crypto/src/x25519.rs](https://github.com/aptos-labs/aptos-core/blob/81d89f428fe8e4b69d53b4916993e9a930afc37c/crates/aptos-crypto/src/x25519.rs#L68) · line 68 · SHA-256 62032054174ffee15e2c56a8f615a05646757644061691a29be5bedb23841d4f_

```
   67 | #[cfg_attr(any(test, feature = "fuzzing"), derive(Clone))]
   68 | pub struct PrivateKey(x25519_dalek::StaticSecret);
   69 | 
```

_file_excerpt · [types/src/account_address.rs](https://github.com/aptos-labs/aptos-core/blob/81d89f428fe8e4b69d53b4916993e9a930afc37c/types/src/account_address.rs#L8) · line 8 · SHA-256 60d89570fe4ecd229fa47359b9ef69023bf2d8827a46efc259eb6796a0429133_

```
    7 |     hash::{CryptoHasher, HashValue},
    8 |     x25519,
    9 | };
```

_file_excerpt · [types/src/account_address.rs](https://github.com/aptos-labs/aptos-core/blob/81d89f428fe8e4b69d53b4916993e9a930afc37c/types/src/account_address.rs#L140) · line 140 · SHA-256 a03e636a2a3651852d60d27d8b841ba7302caf9773d571273c7cdb52be0d15ad_

```
  139 | // See this issue for potential improvements: https://github.com/aptos-labs/aptos-core/issues/3960
  140 | pub fn from_identity_public_key(identity_public_key: x25519::PublicKey) -> AccountAddress {
  141 |     let mut array = [0u8; AccountAddress::LENGTH];
```

_file_excerpt · [types/src/account_address.rs](https://github.com/aptos-labs/aptos-core/blob/81d89f428fe8e4b69d53b4916993e9a930afc37c/types/src/account_address.rs#L144) · line 144 · SHA-256 60b516aca6b2d73706710a24a8e076ef7fe5272b002129931a954fa2f95b723f_

```
  143 |     // keep only the last 16 bytes
  144 |     array.copy_from_slice(&pubkey_slice[x25519::PUBLIC_KEY_SIZE - AccountAddress::LENGTH..]);
  145 |     AccountAddress::new(array)
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Classify each usage, record data lifetimes, and plan migration to Hybrid key establishment with ML-KEM (FIPS 203), e.g. X25519MLKEM768 in TLS 1.3 or mlkem768x25519-sha256 in SSH; introduce an abstraction layer for crypto-agility.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-19664 — Quantum-vulnerable Ed25519: role not determined (4 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:Ed25519:general`
- Data source: keyless/pepper/common/src/account_recovery_db.rs
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.3.0 · 2026-11-06 16:20 UTC
- Priority score: 34.2 / 100
- CVSS v3.1: not applicable

8 reference(s) to Ed25519 across 4 file(s), e.g. keyless/pepper/common/src/account_recovery_db.rs:6. Role, judged from paths, function names and nearby code: role not determined. The code does not show what the keys protect; review decides the priority.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open keyless/pepper/common/src/account_recovery_db.rs:6 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [keyless/pepper/common/src/account_recovery_db.rs](https://github.com/aptos-labs/aptos-core/blob/81d89f428fe8e4b69d53b4916993e9a930afc37c/keyless/pepper/common/src/account_recovery_db.rs#L6) · line 6 · SHA-256 02ad39cd3ff40d72b87d99b9b831167be159bb8a884d0ac819b09009066219c6_

```
    5 | use aptos_crypto::compat::Sha3_256;
    6 | use ed25519_dalek::Digest;
    7 | 
```

_file_excerpt · [keyless/pepper/common/src/vuf/slip_10.rs](https://github.com/aptos-labs/aptos-core/blob/81d89f428fe8e4b69d53b4916993e9a930afc37c/keyless/pepper/common/src/vuf/slip_10.rs#L7) · line 7 · SHA-256 55bd92343ceed586851337d79d69c5713464591d8dc1223743f6d2fb24e50d46_

```
    6 | pub extern crate derivation_path;
    7 | pub extern crate ed25519_dalek;
    8 | 
```

_file_excerpt · [keyless/pepper/common/src/vuf/slip_10.rs](https://github.com/aptos-labs/aptos-core/blob/81d89f428fe8e4b69d53b4916993e9a930afc37c/keyless/pepper/common/src/vuf/slip_10.rs#L13) · line 13 · SHA-256 8b5a0cd4032bfcb9514272fadbd1cc057daf874a5aa7482dca93265104c2e759_

```
   12 | pub use derivation_path::{ChildIndex, DerivationPath};
   13 | pub use ed25519_dalek::{PublicKey, SecretKey};
   14 | use hmac::{Hmac, Mac};
```

_file_excerpt · [keyless/pepper/service/src/dedicated_handlers/handlers.rs](https://github.com/aptos-labs/aptos-core/blob/81d89f428fe8e4b69d53b4916993e9a930afc37c/keyless/pepper/service/src/dedicated_handlers/handlers.rs#L17) · line 17 · SHA-256 a48683095bc2b7fa5407bd4300b9b89fbd2d2251dc96f1a3d2f45c32261d630f_

```
   16 | };
   17 | use aptos_crypto::ed25519::Ed25519PublicKey;
   18 | use aptos_keyless_pepper_common::{
```

_file_excerpt · [keyless/pepper/service/src/dedicated_handlers/handlers.rs](https://github.com/aptos-labs/aptos-core/blob/81d89f428fe8e4b69d53b4916993e9a930afc37c/keyless/pepper/service/src/dedicated_handlers/handlers.rs#L332) · line 332 · SHA-256 d7e13e0ab6a536c71db9df79afc46eb9c48297931b6a36490cd8aafa35743d31_

```
  331 |         Some(public_key_bytes) => Some(EphemeralPublicKey::ed25519(
  332 |             Ed25519PublicKey::try_from(public_key_bytes.as_slice()).map_err(|error| {
  333 |                 PepperServiceError::InternalError(format!(
```

_file_excerpt · [types/src/keyless/circuit_testcases.rs](https://github.com/aptos-labs/aptos-core/blob/81d89f428fe8e4b69d53b4916993e9a930afc37c/types/src/keyless/circuit_testcases.rs#L20) · line 20 · SHA-256 80e0e13b47f0f080c33a94538f572b39340ce59d7a12ffc7c4d94c52db7ed7c6_

```
   19 | };
   20 | use aptos_crypto::{ed25519::Ed25519PrivateKey, PrivateKey, Uniform};
   21 | use ark_bn254::Bn254;
```

_file_excerpt · [types/src/keyless/circuit_testcases.rs](https://github.com/aptos-labs/aptos-core/blob/81d89f428fe8e4b69d53b4916993e9a930afc37c/types/src/keyless/circuit_testcases.rs#L151) · line 151 · SHA-256 ce8a0b28f35892a16fb066050c2e1a8d9466731b3a205679be1bbca33213f1e3_

```
  150 | 
  151 | pub(crate) static SAMPLE_ESK: Lazy<Ed25519PrivateKey> =
  152 |     Lazy::new(Ed25519PrivateKey::generate_for_testing);
```

_file_excerpt · [types/src/keyless/circuit_testcases.rs](https://github.com/aptos-labs/aptos-core/blob/81d89f428fe8e4b69d53b4916993e9a930afc37c/types/src/keyless/circuit_testcases.rs#L152) · line 152 · SHA-256 f97b86c13556a982a6661478a0b0cb7636899a3c523c02ae57c9eadf6b002ac5_

```
  151 | pub(crate) static SAMPLE_ESK: Lazy<Ed25519PrivateKey> =
  152 |     Lazy::new(Ed25519PrivateKey::generate_for_testing);
  153 | 
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it; introduce an abstraction layer for crypto-agility.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-19665 — Quantum-vulnerable BN254 (alt_bn128): role not determined (6 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:BN254 (alt_bn128):general`
- Data source: keyless/pepper/service/src/external_resources/groth16_vk.rs
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.3.0 · 2026-11-06 16:20 UTC
- Priority score: 34.2 / 100
- CVSS v3.1: not applicable

24 reference(s) to BN254 (alt_bn128) across 6 file(s), e.g. keyless/pepper/service/src/external_resources/groth16_vk.rs:6. Role, judged from paths, function names and nearby code: role not determined. The code does not show what the keys protect; review decides the priority.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open keyless/pepper/service/src/external_resources/groth16_vk.rs:6 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [keyless/pepper/service/src/external_resources/groth16_vk.rs](https://github.com/aptos-labs/aptos-core/blob/81d89f428fe8e4b69d53b4916993e9a930afc37c/keyless/pepper/service/src/external_resources/groth16_vk.rs#L6) · line 6 · SHA-256 8b71194ad53a02db1b15dd081670d21504c9d2bfa14c15b3003a7be10517cc79_

```
    5 | use anyhow::{anyhow, Result};
    6 | use ark_bn254::Bn254;
    7 | use ark_groth16::{PreparedVerifyingKey, VerifyingKey};
```

_file_excerpt · [keyless/pepper/service/src/external_resources/groth16_vk.rs](https://github.com/aptos-labs/aptos-core/blob/81d89f428fe8e4b69d53b4916993e9a930afc37c/keyless/pepper/service/src/external_resources/groth16_vk.rs#L47) · line 47 · SHA-256 c92b34abfe8acfd578a35eb1f6a2d59be216084165af58b9ef55a5ef65a21880_

```
   46 |     /// Converts the on-chain verification key to a prepared verifying key
   47 |     pub fn to_ark_prepared_verifying_key(&self) -> Result<PreparedVerifyingKey<Bn254>> {
   48 |         // Collect and parse the gamma_abc_g1 elements
```

_file_excerpt · [types/src/keyless/circuit_constants.rs](https://github.com/aptos-labs/aptos-core/blob/81d89f428fe8e4b69d53b4916993e9a930afc37c/types/src/keyless/circuit_constants.rs#L11) · line 11 · SHA-256 8714c79b04efe1e9428b8ac6055e6cda1f3b008f535881d839713db56092f5d3_

```
   10 | use aptos_crypto::poseidon_bn254;
   11 | use ark_bn254::Bn254;
   12 | use ark_groth16::{PreparedVerifyingKey, VerifyingKey};
```

_file_excerpt · [types/src/keyless/circuit_constants.rs](https://github.com/aptos-labs/aptos-core/blob/81d89f428fe8e4b69d53b4916993e9a930afc37c/types/src/keyless/circuit_constants.rs#L30) · line 30 · SHA-256 ac39114a4a4160acdfcf11a9c8e9f7c7a0cc8bcea12e80685e72159e5b5e8df8_

```
   29 | /// https://github.com/aptos-labs/devnet-groth16-keys/commit/02e5675f46ce97f8b61a4638e7a0aaeaa4351f76
   30 | pub fn prepared_vk_for_testing() -> PreparedVerifyingKey<Bn254> {
   31 |     // Convert the projective points to affine.
```

_file_excerpt · [types/src/keyless/circuit_constants.rs](https://github.com/aptos-labs/aptos-core/blob/81d89f428fe8e4b69d53b4916993e9a930afc37c/types/src/keyless/circuit_constants.rs#L102) · line 102 · SHA-256 f7d97ed84d9587a0def5ee51627c14fd791790704b7c80a081f25046569918aa_

```
  101 | pub struct Groth16TrapdoorSetup {
  102 |     pub simulation_pk: Trapdoor<Bn254>,
  103 |     pub prepared_vk: PreparedVerifyingKey<Bn254>,
```

_file_excerpt · [types/src/keyless/circuit_testcases.rs](https://github.com/aptos-labs/aptos-core/blob/81d89f428fe8e4b69d53b4916993e9a930afc37c/types/src/keyless/circuit_testcases.rs#L21) · line 21 · SHA-256 b89ecf8dca334e4f373b14be738d126c94d3f8274b6b2b1b7dc43bf6c882fb43_

```
   20 | use aptos_crypto::{ed25519::Ed25519PrivateKey, PrivateKey, Uniform};
   21 | use ark_bn254::Bn254;
   22 | use ark_groth16::{PreparedVerifyingKey, VerifyingKey};
```

_file_excerpt · [types/src/keyless/circuit_testcases.rs](https://github.com/aptos-labs/aptos-core/blob/81d89f428fe8e4b69d53b4916993e9a930afc37c/types/src/keyless/circuit_testcases.rs#L205) · line 205 · SHA-256 7a31aaf35992b186681f27b482553c40ffd2901c7df978b53e36fe12774de45e_

```
  204 | /// A new Groth16 VK to test the VK rotation.  Using https://raw.githubusercontent.com/aptos-labs/devnet-groth16-keys/refs/heads/master/verification_key.json
  205 | pub(crate) static SAMPLE_UPGRADED_VK: Lazy<PreparedVerifyingKey<Bn254>> = Lazy::new(|| {
  206 |     let alpha_g1 = g1_projective_str_to_affine(
```

_file_excerpt · [types/src/keyless/groth16_sig.rs](https://github.com/aptos-labs/aptos-core/blob/81d89f428fe8e4b69d53b4916993e9a930afc37c/types/src/keyless/groth16_sig.rs#L17) · line 17 · SHA-256 ac3f63a07e42fdc8535a951ef251dd8fa1b4d283f116eb4f18904247b0c729b9_

```
   16 | use aptos_crypto_derive::{BCSCryptoHash, CryptoHasher};
   17 | use ark_bn254::{Bn254, Fr};
   18 | use ark_ff::{BigInteger, PrimeField};
```

_file_excerpt · [types/src/keyless/groth16_sig.rs](https://github.com/aptos-labs/aptos-core/blob/81d89f428fe8e4b69d53b4916993e9a930afc37c/types/src/keyless/groth16_sig.rs#L163) · line 163 · SHA-256 e7018db89ae59472286666220c398aa35ed4b5d2bb6162e88b9211f8f3abead4_

```
  162 |         public_inputs_hash: Fr,
  163 |         pvk: &PreparedVerifyingKey<Bn254>,
  164 |     ) -> anyhow::Result<()> {
```

_file_excerpt · [types/src/keyless/groth16_sig.rs](https://github.com/aptos-labs/aptos-core/blob/81d89f428fe8e4b69d53b4916993e9a930afc37c/types/src/keyless/groth16_sig.rs#L218) · line 218 · SHA-256 0a7b806327385c8f13574ddf1b99f4ba952029879a3d1feaa3757c313091a49e_

```
  217 |         public_inputs_hash: Fr,
  218 |         pvk: &PreparedVerifyingKey<Bn254>,
  219 |     ) -> anyhow::Result<()> {
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Classify each usage, record data lifetimes, and plan migration to a post-quantum algorithm; introduce an abstraction layer for crypto-agility.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-19666 — Quantum-vulnerable RSA: role not determined (1 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:RSA:general`
- Data source: types/src/jwks/rsa/mod.rs
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.3.0 · 2026-11-06 16:20 UTC
- Priority score: 34.2 / 100
- CVSS v3.1: not applicable

3 reference(s) to RSA across 1 file(s), e.g. types/src/jwks/rsa/mod.rs:45. Role, judged from paths, function names and nearby code: role not determined. The code does not show what the keys protect; review decides the priority.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open types/src/jwks/rsa/mod.rs:45 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [types/src/jwks/rsa/mod.rs](https://github.com/aptos-labs/aptos-core/blob/81d89f428fe8e4b69d53b4916993e9a930afc37c/types/src/jwks/rsa/mod.rs#L45) · line 45 · SHA-256 0aeed392528e804e81c65f28227f220c4f05ff1bdc4a98e6522f519cc102b9cc_

```
   44 |     // TODO(keyless): Hacking around the difficulty of parsing PKCS#8-encoded PEM files with the `pem` crate
   45 |     let der = rsa::RsaPrivateKey::from_pkcs8_pem(include_str!("insecure_test_jwk_private_key.txt"))
   46 |         .unwrap()
```

_file_excerpt · [types/src/jwks/rsa/mod.rs](https://github.com/aptos-labs/aptos-core/blob/81d89f428fe8e4b69d53b4916993e9a930afc37c/types/src/jwks/rsa/mod.rs#L62) · line 62 · SHA-256 badfcb56f8b0b0bdfdaca56c7b9f0fdb8ae485d74d3daa225b8e78a2fb450755_

```
   61 |             kty: "RSA".to_string(),
   62 |             alg: "RS256".to_string(),
   63 |             e: "AQAB".to_string(),
```

_file_excerpt · [types/src/jwks/rsa/mod.rs](https://github.com/aptos-labs/aptos-core/blob/81d89f428fe8e4b69d53b4916993e9a930afc37c/types/src/jwks/rsa/mod.rs#L83) · line 83 · SHA-256 d1a9a53ec8744bfbb8c1fda5c05f046f54da1d55ec5bf082d5e3ddeeb6ab385e_

```
   82 |             kty:"RSA".to_owned(),
   83 |             alg:"RS256".to_owned(),
   84 |             e:"AQAB".to_owned(),
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it; introduce an abstraction layer for crypto-agility.

**Retest procedure.** Re-run the inventory after refactoring.


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

- In use: SLH-DSA — types/src/on_chain_config/aptos_features.rs
- Present, not wired: SLH-DSA — crates/aptos-crypto/src/slh_dsa_sha2_128s/slh_dsa_keys.rs
- Present, not wired: SLH-DSA — crates/aptos-crypto/src/slh_dsa_sha2_128s/slh_dsa_sigs.rs
- A post-quantum library is declared as a dependency
- Classical only — channel key exchange (TLS, Noise, handshakes): X25519 (2 file(s))

**Next step:** Extend post-quantum protection to the critical roles that stay classical, starting with what can be recorded today (wrapped keys, channel key exchange).

_Levels: 0 none; 1 present, not wired; 2 in use outside the critical paths; 3 hybrid in a critical path; 4 post-quantum by default in the critical paths (root of trust, key wrapping, channel key exchange). Judged from code and manifests._

### What the quantum-vulnerable algorithms do

| Role | Algorithms (files) | ID | First step |
|---|---|---|---|
| **channel key exchange (TLS, Noise, handshakes)** | X25519 (2) | QSI-2026-19662 | Move the handshake to a hybrid key exchange (X25519MLKEM768 in TLS 1.3; a hybrid KEM in Noise-based protocols) |
| **transaction and message signing** | Ed25519 (10), ECDSA (3), BLS12-381 (2), BN254 (alt_bn128) (1) | QSI-2026-19659, QSI-2026-19660, QSI-2026-19663, QSI-2026-19667 | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains adopt them |
| **role not determined** | BN254 (alt_bn128) (6), Ed25519 (4), X25519 (3), RSA (1) | QSI-2026-19661, QSI-2026-19664, QSI-2026-19665, QSI-2026-19666 | Classify each usage, record data lifetimes, and plan migration to Hybrid key establishment with ML-KEM (FIPS 203), e.g. X25519MLKEM768 in TLS 1.3 or mlkem768x25519-sha256 in SSH; introduce an abstraction layer for crypto-agility |

_Roles are judged from file paths, function names and the code around each match; review confirms them. Root-of-trust keys and wrapped keys come first: they are hard to replace or can be recorded today._
No readiness questionnaire was completed for this project.

### Quantum algorithms relevant to this inventory

| Quantum algorithm | Effect | Attack model | Inventoried algorithms (rows) | What it means for this audit |
|---|---|---|---|---|
| Shor's algorithm — factoring | breaks | Q1 | RSA (2) | Breaks RSA at every key length: a longer modulus only raises the cost polynomially. Plan migration to ML-KEM (or a hybrid) for key establishment and ML-DSA / SLH-DSA for signatures; start with keys protecting data that must stay confidential for years (harvest now, decrypt later) and with long-lived signatures. |
| Shor's algorithm — discrete logarithms in finite fields | breaks | Q1 | BLS12-381 (6), BN254 (alt_bn128) (8), ElGamal (1), Groth16 (3) | Breaks finite-field Diffie–Hellman and DSA at every size. Move key establishment to ML-KEM (hybrid with X25519 or ECDH during the transition) and signatures to ML-DSA or SLH-DSA. |
| Shor's algorithm — elliptic-curve discrete logarithms | breaks | Q1 | BLS12-381 (6), BN254 (alt_bn128) (8), ECDSA (6), Ed25519 (24), Groth16 (3), X25519 (8) | Elliptic-curve keys are expected to fall before RSA keys of comparable classical strength. On blockchains, coins whose public key is already on chain (reused addresses, pay-to-public-key and Taproot outputs) are exposed first; plan the move to post-quantum signatures and avoid key reuse in the meantime. |
| Grover's algorithm — key search and preimages | weakens (larger keys restore the margin) | Q1 | AES-256 (2), HKDF (2), HMAC (2), Poseidon (9), SHA-2 (1), SHA-3 (4), SLH-DSA (3) | Not a break. 256-bit keys (AES-256, ChaCha20) keep a comfortable margin; AES-128 meets NIST category 1, while some authorities ask for 256-bit keys in quantum-resistant contexts (see the AES-128 entry). Prefer 256-bit keys for long-lived data; 256-bit hashes need no change for preimage resistance. |
| Brassard–Høyer–Tapp — collision search | weakens (larger keys restore the margin) | Q1 | Poseidon (9), SHA-2 (1), SHA-3 (4) | 256-bit hashes (SHA-256, SHA3-256) remain adequate for collision resistance; 160-bit hashes are already weak classically (SHA-1 collisions are practical). Use 384/512-bit hashes where NIST categories 4–5 are required. |
| Simon's algorithm — superposition attacks on symmetric constructions | only with superposition queries | Q2 | GCM mode (1) | No action for ordinary deployments of AES-GCM or CBC-MAC — the attack model does not apply. Record it as a model assumption; see the offline variant for Even–Mansour-type designs. |

_Effects: breaks — replace the algorithm; weakens — larger keys or outputs restore the margin; included in standard parameters — no action at standard parameter sets; only with superposition queries — not applicable to ordinary deployments._


## 9. Limitations and assumptions

- This report presents automated and documented analysis results for the stated scope. It is not a legal opinion, a certification or an attestation of compliance with any standard.
- z is a planning assumption chosen per risk profile, not a prediction. A cryptographically relevant quantum computer is not publicly known to exist today.
- osv_advisories: no exactly pinned versions to query

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
| P3 | QSI-2026-19659 | Add BLS12-381 usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-19660 | Add Ed25519 usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-19662 | Add X25519 usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-19663 | Add ECDSA usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-19667 | Add BN254 (alt_bn128) usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-19661 | Add X25519 usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-19664 | Add Ed25519 usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-19665 | Add BN254 (alt_bn128) usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-19666 | Add RSA usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P4 | QSI-2026-19659 | Plan migration of BLS12-381 to  (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows  or a hybrid scheme in use. |
| P4 | QSI-2026-19660 | Plan migration of Ed25519 to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-19662 | Plan migration of X25519 to Hybrid key establishment with ML-KEM (FIPS 203), e.g. X25519MLKEM768 in TLS 1.3 or mlkem768x25519-sha256 in SSH (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows Hybrid key establishment with ML-KEM (FIPS 203), e.g. X25519MLKEM768 in TLS 1.3 or mlkem768x25519-sha256 in SSH or a hybrid scheme in use. |
| P4 | QSI-2026-19663 | Plan migration of ECDSA to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-19667 | Plan migration of BN254 (alt_bn128) to  (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows  or a hybrid scheme in use. |
| P4 | QSI-2026-19661 | Plan migration of X25519 to Hybrid key establishment with ML-KEM (FIPS 203), e.g. X25519MLKEM768 in TLS 1.3 or mlkem768x25519-sha256 in SSH (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows Hybrid key establishment with ML-KEM (FIPS 203), e.g. X25519MLKEM768 in TLS 1.3 or mlkem768x25519-sha256 in SSH or a hybrid scheme in use. |
| P4 | QSI-2026-19664 | Plan migration of Ed25519 to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-19665 | Plan migration of BN254 (alt_bn128) to  (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows  or a hybrid scheme in use. |
| P4 | QSI-2026-19666 | Plan migration of RSA to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |

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
19. M. Ekerå, J. Gärtner — A high-level comparison of state-of-the-art quantum algorithms for breaking asymmetric cryptography (arXiv:2405.14381) — arXiv. <https://arxiv.org/abs/2405.14381> (preprint (2024-05-23): Regev-style algorithms show no overall advantage yet for cryptographic RSA and finite-field sizes)
20. M. Kaplan, G. Leurent, A. Leverrier, M. Naya-Plasencia — Breaking Symmetric Cryptosystems using Quantum Period Finding (CRYPTO 2016; arXiv:1602.05973) — Springer / arXiv. <https://arxiv.org/abs/1602.05973> (peer-reviewed article: superposition-query forgeries on CBC-MAC, PMAC, GMAC, GCM, OCB)
21. M. Mosca — Cybersecurity in an Era with Quantum Computers: Will We Be Ready? (IEEE Security & Privacy, 2018) — IEEE. <https://doi.org/10.1109/MSP.2018.3761723> (peer-reviewed article; source of the x + y > z migration inequality)
22. M. Roetteler, M. Naehrig, K. Svore, K. Lauter — Quantum resource estimates for computing elliptic curve discrete logarithms (ASIACRYPT 2017) — IACR / arXiv. <https://arxiv.org/abs/1706.06752> (peer-reviewed article: at most 9n + 2⌈log2 n⌉ + 10 qubits and 448 n^3 log2 n + 4090 n^3 Toffoli gates)
23. NIST IR 8547 — Transition to Post-Quantum Cryptography Standards — NIST. <https://csrc.nist.gov/pubs/ir/8547/final> (final (2026-10-27; the initial public draft of November 2024 is obsoleted). Tables 2 and 4: ECDSA, EdDSA and RSA signatures, finite-field and elliptic-curve DH and MQV, and RSA key establishment are deprecated after 2030 and disallowed after 2035 at every key size — the draft deprecated only the 112-bit level. A composite (hybrid) key establishment stays FIPS 140-validatable while one input comes from an approved scheme. Repeats the federal deadlines of OMB M-26-15: post-quantum key establishment by 2030-12-31 and signatures by 2031-12-31 for high value assets and high impact systems)
24. NIST — Post-Quantum Cryptography Standardization: Evaluation Criteria, Security (Call for Proposals, Section 4.A.5) — NIST. <https://csrc.nist.gov/Projects/Post-Quantum-Cryptography/Post-Quantum-Cryptography-Standardization/Evaluation-Criteria/Security-(Evaluation-Criteria)> (security categories: AES-128 key search 2^170/MAXDEPTH quantum gates, AES-192 2^233/MAXDEPTH, AES-256 2^298/MAXDEPTH; MAXDEPTH 2^40–2^96)
25. P. W. Shor — Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms on a Quantum Computer (SIAM J. Comput., 1997) — SIAM. <https://doi.org/10.1137/S0097539795293172> (peer-reviewed article)
26. R. Babbush et al. — Securing Elliptic Curve Cryptocurrencies against Quantum Vulnerabilities: Resource Estimates and Mitigations (arXiv:2603.28846) — arXiv. <https://arxiv.org/abs/2603.28846> (preprint (2026-03-30, v2 2026-04-15): 256-bit ECDLP with < 1200 logical qubits and < 90 M Toffoli gates (or < 1450 and < 70 M); < 500,000 physical qubits at 10^-3 error, minutes)
27. S. Jaques, M. Naehrig, M. Roetteler, F. Virdia — Implementing Grover oracles for quantum key search on AES and LowMC (EUROCRYPT 2020; arXiv:1910.01700) — Springer / arXiv. <https://arxiv.org/abs/1910.01700> (peer-reviewed article: lower cost estimates for the AES key searches that define the NIST categories)

## Appendices: Cryptographic inventory

By origin: dependency manifests 14 (0 Shor-breakable) · own code 82 (58 Shor-breakable).

| Algorithm | Parameter | Library | Quantum status | Classical status | Count | Locations | Examples |
|---|---|---|---|---|---|---|---|
| AES-256 | AES-256 |  | reduced margin (Grover), approved | acceptable | 2 | 2 | crates/aptos-crypto/src/asymmetric_encryption/elgamal_curve25519_aes256_gcm.rs:15; crates/aptos-crypto/src/noise.rs:126 |
| HKDF |  |  | reduced margin (Grover), approved | acceptable | 2 | 2 | crates/aptos-crypto/src/hkdf.rs:116; crates/aptos-crypto/src/noise.rs:65 |
| HMAC |  |  | reduced margin (Grover), approved | acceptable | 1 | 1 | keyless/pepper/common/src/vuf/slip_10.rs:14 |
| HMAC | HMAC-SHA-512 |  | reduced margin (Grover), approved | acceptable | 1 | 1 | keyless/pepper/common/src/vuf/slip_10.rs:55 |
| SHA-3 | SHA3-512 |  | reduced margin (Grover), approved | acceptable | 2 | 2 | crates/aptos-crypto/src/arkworks/hashing.rs:41; keyless/pepper/service/src/vuf_keypair.rs:73 |
| Poseidon |  |  | Grover: acceptable to NIST, below ECCG/ANSSI guidance | acceptable | 9 | 9 | crates/aptos-crypto/src/lib.rs:24; crates/aptos-crypto/src/poseidon_bn254/constants.rs:4; crates/aptos-crypto/src/poseidon_bn254/keyless.rs:6 |
| SHA-2 | SHA-256 |  | Grover: acceptable to NIST, below ECCG/ANSSI guidance | acceptable | 1 | 1 | crates/aptos-crypto/src/noise.rs:189 |
| SHA-3 | SHA3-256 |  | Grover: acceptable to NIST, below ECCG/ANSSI guidance | acceptable | 2 | 2 | crates/aptos-crypto/src/asymmetric_encryption/elgamal_curve25519_aes256_gcm.rs:32; keyless/pepper/common/src/account_recovery_db.rs:28 |
| Crypto library | workspace | ed25519-dalek (ed25519-dalek) | n/a | acceptable | 2 | 2 | crates/aptos-crypto/Cargo.toml; keyless/pepper/common/Cargo.toml |
| Crypto library | workspace | x25519-dalek (ed25519-dalek) | n/a | acceptable | 1 | 1 | crates/aptos-crypto/Cargo.toml |
| Crypto library | workspace | bls12_381 (bls12_381) | n/a | acceptable | 1 | 1 | crates/aptos-crypto/Cargo.toml |
| Crypto library | workspace | curve25519-dalek (ed25519-dalek) | n/a | acceptable | 1 | 1 | crates/aptos-crypto/Cargo.toml |
| Crypto library | workspace | ring (ring (Rust)) | n/a | acceptable | 2 | 2 | crates/aptos-crypto/Cargo.toml; types/Cargo.toml |
| Crypto library | workspace | p256 (RustCrypto elliptic curves) | n/a | acceptable | 2 | 2 | crates/aptos-crypto/Cargo.toml; types/Cargo.toml |
| Crypto library | workspace | jsonwebtoken (jsonwebtoken (Node)) | n/a | acceptable | 3 | 3 | keyless/pepper/common/Cargo.toml; keyless/pepper/service/Cargo.toml; types/Cargo.toml |
| Crypto library | workspace | rsa (RustCrypto rsa) | n/a | acceptable | 1 | 1 | types/Cargo.toml |
| GCM mode |  |  | n/a | acceptable | 1 | 1 | crates/aptos-crypto/src/asymmetric_encryption/elgamal_curve25519_aes256_gcm.rs |
| PQC library | workspace | slh-dsa (RustCrypto post-quantum crates) | post-quantum | acceptable | 1 | 1 | crates/aptos-crypto/Cargo.toml |
| SLH-DSA |  |  | post-quantum | acceptable | 3 | 3 | crates/aptos-crypto/src/slh_dsa_sha2_128s/slh_dsa_keys.rs:18; crates/aptos-crypto/src/slh_dsa_sha2_128s/slh_dsa_sigs.rs:16; types/src/on_chain_config/aptos_features.rs:170 |
| BLS12-381 |  |  | vulnerable (Shor) | acceptable | 6 | 6 | crates/aptos-crypto/src/bls12381/bls12381_keys.rs:77; crates/aptos-crypto/src/bls12381/bls12381_pop.rs; crates/aptos-crypto/src/bls12381/bls12381_sigs.rs |
| BN254 (alt_bn128) |  |  | vulnerable (Shor) | acceptable | 8 | 8 | keyless/pepper/service/src/external_resources/groth16_vk.rs:6; types/src/keyless/bn254_circom.rs; types/src/keyless/circuit_constants.rs:11 |
| ECDSA | secp256k1 |  | vulnerable (Shor) | acceptable | 1 | 1 | crates/aptos-crypto/src/secp256k1_ecdsa.rs:120 |
| ECDSA |  |  | vulnerable (Shor) | acceptable | 3 | 3 | crates/aptos-crypto/src/secp256r1_ecdsa/mod.rs:44; crates/aptos-crypto/src/secp256r1_ecdsa/secp256r1_ecdsa_keys.rs:26; crates/aptos-crypto/src/secp256r1_ecdsa/secp256r1_ecdsa_sigs.rs:24 |
| ECDSA | P-256 |  | vulnerable (Shor) | acceptable | 2 | 2 | crates/aptos-crypto/src/secp256r1_ecdsa/secp256r1_ecdsa_keys.rs:26; crates/aptos-crypto/src/secp256r1_ecdsa/secp256r1_ecdsa_sigs.rs:24 |
| Ed25519 | Ed25519 |  | vulnerable (Shor) | acceptable | 24 | 24 | crates/aptos-crypto/src/ed25519/ed25519_keys.rs:16; crates/aptos-crypto/src/ed25519/ed25519_keys.rs:9; crates/aptos-crypto/src/ed25519/ed25519_sigs.rs:7 |
| ElGamal |  |  | vulnerable (Shor) | deprecated | 1 | 1 | crates/aptos-crypto/src/asymmetric_encryption/elgamal_curve25519_aes256_gcm.rs |
| Groth16 |  |  | vulnerable (Shor) | acceptable | 3 | 3 | keyless/pepper/service/src/external_resources/groth16_vk.rs; types/src/keyless/groth16_sig.rs; types/src/keyless/groth16_vk.rs |
| RSA |  |  | vulnerable (Shor) | acceptable | 1 | 1 | types/src/jwks/rsa/mod.rs:45 |
| RSA | RS256 |  | vulnerable (Shor) | acceptable | 1 | 1 | types/src/jwks/rsa/mod.rs:62 |
| X25519 |  |  | vulnerable (Shor) | acceptable | 2 | 2 | crates/aptos-crypto/src/asymmetric_encryption/elgamal_curve25519_aes256_gcm.rs; crates/aptos-crypto/src/elgamal/curve25519.rs |
| X25519 | X25519 |  | vulnerable (Shor) | acceptable | 6 | 6 | crates/aptos-crypto/src/lib.rs:34; crates/aptos-crypto/src/noise.rs:65; crates/aptos-crypto/src/x25519.rs:35 |

_Long lists are grouped here; the full per-file list is in the JSON report, signed with the same key._

## Appendices: Input files

| File | Size | SHA-256 | Redactions |
|---|---|---|---|
| aptos-move/framework/src/aptos.rs | 8542 | `fcf083dd26c8621f3790d2135561197bb2dde15dcb4dbc10281080bac9417997` | 0 |
| aptos-move/framework/src/built_package.rs | 28767 | `c35c94adfde8f8bae53b6a85aecd0cf23c026c502a7f277eff372911e743d1a8` | 0 |
| aptos-move/framework/src/chunked_publish.rs | 7922 | `0147d227083a1a99f03dc98e5b7d4902d782bdccc7278c7cfadfe0eb28926888` | 0 |
| aptos-move/framework/src/docgen.rs | 5267 | `998a21a6a0e5e57e6717808d00f66fc4ed0cca1c25601881b6c9a35cf5f2386b` | 0 |
| aptos-move/framework/src/extended_checks.rs | 38284 | `bf18b4a2fb461aaa4810fd4f457c43a8a77114eafb66e7c6d562acbc5a99806a` | 0 |
| aptos-move/framework/src/lib.rs | 1308 | `bf55073178dacf1fa2f2201687a8d730604cbb0fbb4a76ccdfa55a5ac0aaaaf8` | 0 |
| aptos-move/framework/src/main.rs | 2975 | `79e70277296b372102d4b7db1a5252fc29731b0e01f6b95406f6a91ecafa4197` | 0 |
| aptos-move/framework/src/prover.rs | 19222 | `36d2b5eb124c63e6819579c0a20e4ac4adda69bdb9198c6c1214f58046d0be9e` | 0 |
| aptos-move/framework/src/release_builder.rs | 5125 | `d3b433b4191c96586f92ce2e8443a3f550502eae0f1fb02246b55210479e3b1e` | 0 |
| aptos-move/framework/src/release_bundle.rs | 1428 | `650f244c4402a6bd7cc5f00d93f62d3cc35a24fd1be68f872ab86ae8dc9bb658` | 0 |
| crates/aptos-crypto/Cargo.toml | 4150 | `427240ded930807125514251be202b173d814c54dbfe1196963c5d5bddfe895b` | 0 |
| crates/aptos-crypto/src/arkworks/differentiate.rs | 2641 | `535935d73d2ee8b9052c0df97a5c13b295a4e61b002538af747176d8dc599222` | 0 |
| crates/aptos-crypto/src/arkworks/hashing.rs | 4378 | `f6423e811efd0e94961d3d799f1dc6d2a82985a44793a3f14c5f2a8a78b51675` | 0 |
| crates/aptos-crypto/src/arkworks/mod.rs | 4122 | `a169eeb3e3a5c14c46b75b1698ccee9933e4df801c361f51a4e747ce12e3dd07` | 0 |
| crates/aptos-crypto/src/arkworks/msm.rs | 4829 | `c37af58ba43dd67dd988086d66a2f2676d0b8f3d11f8b9d8788c722cf73d0345` | 0 |
| crates/aptos-crypto/src/arkworks/random.rs | 4979 | `c1c21ed11f1faaff52c99a588b61dbafd74aaf2b84fd31a9f05476fcd162c186` | 0 |
| crates/aptos-crypto/src/arkworks/scrape.rs | 11248 | `d5a08178f5a24d15c34c9765486cf472cd1c5592c81407d5a470ab521b99db9d` | 0 |
| crates/aptos-crypto/src/arkworks/serialization.rs | 4958 | `f2df1c7f19a0aac6d4809f62a1e558ccebf14f119dbce3762cb2617693a3241f` | 0 |
| crates/aptos-crypto/src/arkworks/shamir.rs | 18514 | `4739f5e1c70ec6cf2475cbbd711d19f992dbbb4035cd812f84794f0e803ebae5` | 0 |
| crates/aptos-crypto/src/arkworks/srs.rs | 8411 | `0e11689ff310df143a22d526923c88259149b1f7c88b32d7fc810cf35701c8af` | 0 |
| crates/aptos-crypto/src/arkworks/vanishing_poly.rs | 3321 | `b2645ccc303cf0cadf6a5eb7ab59c61ef77d638eb78c46ce382a402907899fdb` | 0 |
| crates/aptos-crypto/src/arkworks/weighted_sum.rs | 1365 | `702231ffd20ad9eb6a3a7d181b22983fce1d4eddca150ea830bd1c973449b942` | 0 |
| crates/aptos-crypto/src/asymmetric_encryption/elgamal_curve25519_aes256_gcm.rs | 6045 | `6b01dda952ebe1960565b297a2d67fac4572c53baeecde311dbb24ca90f740a1` | 0 |
| crates/aptos-crypto/src/asymmetric_encryption/mod.rs | 1491 | `4f58c0c94e7c521cc7455d2c25290e35dad6b0e523278b22b56542c91c77cc4d` | 0 |
| crates/aptos-crypto/src/bls12381/bls12381_keys.rs | 10760 | `b2ebf8767ada59dc70cc0b6b01f525d9bdcb77753bd527770db30b44f476e512` | 0 |
| crates/aptos-crypto/src/bls12381/bls12381_pop.rs | 6512 | `ce93253d1294e232768f51235d4d29145f569e38a9f97df18de89d13405a5c38` | 0 |
| crates/aptos-crypto/src/bls12381/bls12381_sigs.rs | 8454 | `76831485928ebc9dd3d96224d913361f7a120b60f8e714bad1bf6856735843b8` | 0 |
| crates/aptos-crypto/src/bls12381/bls12381_validatable.rs | 7303 | `d17948f1d6363296bd855204618c52428ec0730f78d1bf0c49b8193361cab57e` | 0 |
| crates/aptos-crypto/src/bls12381/mod.rs | 23250 | `4afd88a46f7d49ae01d78c704e3e7b1d09897992133e72f943cdff82c09d1311` | 0 |
| crates/aptos-crypto/src/blstrs/evaluation_domain.rs | 8024 | `9c9a0eb6de846e719b24297ec68b7bc833ea19189aeb93d2c708da870d05712f` | 0 |
| crates/aptos-crypto/src/blstrs/fft.rs | 6631 | `76306cde79adc8f4610ee2e77f61b12f0f48c185a645b9452ff255673d883a91` | 0 |
| crates/aptos-crypto/src/blstrs/lagrange.rs | 15244 | `7c88a82115ad016d6f8ab4f2f5eae35018ee181c8fd873cbe5f23b3aa9ab6f47` | 0 |
| crates/aptos-crypto/src/blstrs/mod.rs | 6860 | `95fde1ecccf049114d882eb20d14570ec73505fa02e2d26512440062514cf2bd` | 0 |
| crates/aptos-crypto/src/blstrs/polynomials.rs | 21122 | `79759c144e0ad0bcda97805d0236024f94833f92f5743a90879a93166bc9626e` | 0 |
| crates/aptos-crypto/src/blstrs/random.rs | 5920 | `77ed170dbaadf8deec686583675f69c76ce766a8470e86c4ed5a922c1d01e29a` | 0 |
| crates/aptos-crypto/src/blstrs/scalar_secret_key.rs | 1492 | `98334ee57e6a96bf2ead9f634e86d57285437400c853c0b3d01bbce3523be3d7` | 0 |
| crates/aptos-crypto/src/blstrs/threshold_config.rs | 4858 | `342cda1d07632e5614f8782940dd49654eed26a4ea0f94c2e7911fee6dd085a5` | 0 |
| crates/aptos-crypto/src/bulletproofs/mod.rs | 425 | `d846f3b90cc120939fb006a8c5913e0f4f9d339eaa631ca58a0fbeef0bb456bf` | 0 |
| crates/aptos-crypto/src/compat.rs | 1705 | `c18f5c5ad97ebf51b82c2be6e3ac016b1c0f774d97ef34900301a84c0d31fe7e` | 0 |
| crates/aptos-crypto/src/constant_time/blstrs_scalar_mul.rs | 4472 | `afa62e1a6d411f2a4ec0f8f18398aefe3aa70482e5c49884085e1445fefcac0e` | 0 |
| crates/aptos-crypto/src/constant_time/mod.rs | 537 | `fa46c51086a77b79a861fd4ea8dda3b48c691c97d87ed3fe81e0d82f4e29eb44` | 0 |
| crates/aptos-crypto/src/constant_time/zkcrypto_scalar_mul.rs | 3387 | `c791efc46427451263e753218ac6a2b1a74c9192762c79a971d5c9fdcb0f56b0` | 0 |
| crates/aptos-crypto/src/ed25519/ed25519_keys.rs | 12368 | `79a6f426fb5efb58ae8e072947d4e9347eda7cc281509f2dff57263559b8c4a9` | 0 |
| crates/aptos-crypto/src/ed25519/ed25519_sigs.rs | 7998 | `838e7e95fe58782ee363ebf441d73b32f13e4987712a4e23c8c6b7d45b281856` | 0 |
| crates/aptos-crypto/src/ed25519/mod.rs | 2187 | `7b21ea56b9c4fbf31f19ae1789d1bfe612ffa33d990560cb65a8b2f958c38d58` | 0 |
| crates/aptos-crypto/src/elgamal/curve25519.rs | 1196 | `6d54354f3f24d7a6e7bc76b20ae3b52d3cc6443d7ab2d7616cc1f150c221ec51` | 0 |
| crates/aptos-crypto/src/elgamal/mod.rs | 2500 | `83d8912dfc5e3d2deac79735478945fcbdea9918ef912e5ddec4fab3c79f5bfd` | 0 |
| crates/aptos-crypto/src/encoding_type.rs | 4238 | `db4dcf8c76d0bc883ad6bab893154ea447fdebf9bb28a1443367d95fdb8a74b6` | 0 |
| crates/aptos-crypto/src/hash.rs | 29640 | `5e92ab53b41b8b98cf24866c26693e970131cff99c48f01f7329a700f608f500` | 0 |
| crates/aptos-crypto/src/hkdf.rs | 9334 | `c12e0c2a3ced207bdeb0f4fcc649f81ec011e96d7b1754f6e129174b903d6883` | 0 |
| crates/aptos-crypto/src/input_secret.rs | 2336 | `ebf3023280af59784f347d07b7d14de79ec2617f7ace22781d99dedcf48baa8b` | 0 |
| crates/aptos-crypto/src/lib.rs | 1064 | `6536c4a7b7bd5d55ddc372edf35c88335b09d18de020015aebb4c482143dd907` | 0 |
| crates/aptos-crypto/src/multi_ed25519.rs | 23396 | `ae1c4781f7a6ba11430ff69a738a66c695301f1366134b1102b69b4f9657ceae` | 0 |
| crates/aptos-crypto/src/noise.rs | 24482 | `2cb8c0264ae10b0e55f89da85b7505bce380a505886e62d210a86a0524968c3e` | 0 |
| crates/aptos-crypto/src/player.rs | 1098 | `a762b8ffb60ea539a33d8eb9161fa6e7d4dbe14fa2972f7f5eac75904f33e2c8` | 0 |
| crates/aptos-crypto/src/poseidon_bn254/alt_fr.rs | 1187 | `bdf936df121cc626c36266d86160148c9dcbabd1812a42c21c62029bff5afef1` | 0 |
| crates/aptos-crypto/src/poseidon_bn254/constants.rs | 1311506 | `77b60d61b5d52f231b1e481ab1999b4f5210e808aceccac75ab083945376dd1a` | 0 |
| crates/aptos-crypto/src/poseidon_bn254/keyless.rs | 14848 | `7e842fd4c814c22c11d11f99432389e8826e5db1dd46d1de8ed56e6dd14a06a5` | 0 |
| crates/aptos-crypto/src/poseidon_bn254/mod.rs | 5914 | `e8c1710988df9cfd67e60cc353c72f0e289a226ffc521b955b8a695f2b2a076a` | 0 |
| crates/aptos-crypto/src/secp256k1_ecdsa.rs | 9137 | `6c3560abca72d30a926e776c6d8575440ff115c2b2e95f90818b04079a2b305d` | 0 |
| crates/aptos-crypto/src/secp256r1_ecdsa/mod.rs | 2839 | `28d55d895077405cd4eb4c741b4ea329cb9cdd04097156d5e804e568f174e5a7` | 0 |
| crates/aptos-crypto/src/secp256r1_ecdsa/secp256r1_ecdsa_keys.rs | 9340 | `89ccb0ac1699817da1b5220747870eaa01ba06f2356e33f8d75a7e85cf16f719` | 0 |
| crates/aptos-crypto/src/secp256r1_ecdsa/secp256r1_ecdsa_sigs.rs | 7381 | `33d282f06a6e7d76d77dd13cbe304689838f5dd2ca56007948dc39418833317c` | 0 |
| crates/aptos-crypto/src/slh_dsa_sha2_128s/mod.rs | 2115 | `b13baf6f2dde07bd7ba865af2c1d456f7094675cb54a71295d089fa02e64515f` | 0 |
| crates/aptos-crypto/src/slh_dsa_sha2_128s/slh_dsa_keys.rs | 18824 | `24fec169f9f85b7bc650011fa43b338ec2f7629640083c5ee600541a02065c9e` | 0 |
| crates/aptos-crypto/src/slh_dsa_sha2_128s/slh_dsa_sigs.rs | 4351 | `0547e0962260a4b1dbd297f96b21ed69858d694ac2504e58bacc880aa3973c82` | 0 |
| crates/aptos-crypto/src/traits/mod.rs | 15507 | `eaf0b9771e5ed0798af939e0a7895ec215bf5393993d49dbfb40ae4d03d0becf` | 0 |
| crates/aptos-crypto/src/utils.rs | 1593 | `c1c20941082db1db8145b46819df485ea5ae61ba06c4cdb5481a0f86e5854255` | 0 |
| crates/aptos-crypto/src/validatable.rs | 4700 | `3bc1a50fa2466b6e07aaa454fb71fae3083eb3cbdd77cd0d4a1339be47ecf881` | 0 |
| crates/aptos-crypto/src/weighted_config.rs | 21569 | `bd5e96b85159ca83d4eee684db0bb3a49657111f62903331b10cacc2ffe5139a` | 0 |
| crates/aptos-crypto/src/x25519.rs | 9254 | `98ce32435fbf406d0b5f541260fefdb82a3fbbf7a734fec59d221fe79e23245c` | 2 |
| keyless/pepper/common/Cargo.toml | 1035 | `4bf6025c80b280d8415c369feb7c36171037890a69c6da51ca301e286beec498` | 0 |
| keyless/pepper/common/src/account_recovery_db.rs | 1455 | `511cee839218320b0c80a0d6d39a88beed134b4f64d71adf0ab40de26e7c7f18` | 0 |
| keyless/pepper/common/src/jwt.rs | 1112 | `bfb8232ced840395778af71de3001b2a8454ff5062ee6e21239980550c72fd73` | 0 |
| keyless/pepper/common/src/lib.rs | 7312 | `b594ae7bb2cd19a292af6145791a7ee0bbf781ca040116195fa692e232ce584d` | 0 |
| keyless/pepper/common/src/vuf/bls12381_g1_bls.rs | 4184 | `bb3439691e1861fae253498ff947dd5285630382a07786a7d4850a5ade1a7caa` | 0 |
| keyless/pepper/common/src/vuf/mod.rs | 1044 | `3d8f6ae49835b02a879e83fd4a0c4160a6d3978a1d4163f193fac5ec27041fa0` | 0 |
| keyless/pepper/common/src/vuf/slip_10.rs | 6293 | `3f246c07d30f5759f0eec0c7600a2cd892e075aeb41c05964049e308c6ee39bc` | 0 |
| keyless/pepper/service/Cargo.toml | 1658 | `c1b332270bb1fdd5d25aaeb76ba6df4a593e929f404426903197212ee7282f90` | 0 |
| keyless/pepper/service/src/accounts/account_managers.rs | 3653 | `05ab7709bf7b451e8ace13a122b95594968119a60509cb1dcbe9f989a79778ba` | 0 |
| keyless/pepper/service/src/accounts/account_recovery_db.rs | 9098 | `c91f59771ac154d3c2160f1b6784155dbf37d2481ced46485baf06bd468a1ee9` | 0 |
| keyless/pepper/service/src/accounts/mod.rs | 231 | `332701b0f73fb4d8f9b1a1206a16be259154da921420e189446600741064d934` | 0 |
| keyless/pepper/service/src/dedicated_handlers/handlers.rs | 17198 | `46b496f4bce4ad545fc06c386c0e11adf0630d00069866a8ed1da3d913577522` | 0 |
| keyless/pepper/service/src/dedicated_handlers/mod.rs | 218 | `bd485aa22d27e24e7fc19d7a82033f47b27a114ea8bc0fbd4bd30198d32e373a` | 0 |
| keyless/pepper/service/src/dedicated_handlers/pepper_request.rs | 28733 | `f50bbf77d32067c6a7a4d21222f0125adf3367eed90a595515da14edba7c9aab` | 0 |
| keyless/pepper/service/src/deployment_information.rs | 1339 | `e8b2c33837785a6d4f62455adccb35140a18faeb86aa97a6872d6b4a26f892ea` | 0 |
| keyless/pepper/service/src/error.rs | 832 | `378a3aa9dabebd46127dd4dd03c22b8d00395aab8ee3463591a6720422a536df` | 0 |
| keyless/pepper/service/src/external_resources/groth16_vk.rs | 7570 | `6b43294876f6294ecfa0953d3d7f4ef952ba458c0f36554a9e279e38d05961b0` | 0 |
| keyless/pepper/service/src/external_resources/jwk_fetcher.rs | 11533 | `66e6d3b59794b557e853ebb7227c0d441b33752fdcd125d063f26938e9cdbf34` | 0 |
| keyless/pepper/service/src/external_resources/jwk_types.rs | 5420 | `7d9a8f275c836dbca5cfeee5da2a9839be1a93c48a96824a6395495c3e67e499` | 0 |
| keyless/pepper/service/src/external_resources/keyless_config.rs | 5074 | `b4b12f28129292891dfd565ecfc2635e4e4a0c0450d8bdd8c88ce4529dd284c9` | 0 |
| keyless/pepper/service/src/external_resources/mod.rs | 286 | `30c753f788d2223c5436d8457320db0bf380919daa1275205ffac703d9b743bf` | 0 |
| keyless/pepper/service/src/external_resources/resource_fetcher.rs | 10624 | `99e0bba35f52c92f9ff8fe59a258dd402581664ff48512781306acf9f2f24965` | 0 |
| keyless/pepper/service/src/lib.rs | 400 | `822c5b5d84aa0c374f18b4d704b43b260eaa6afa8914a7fe295b96db1f38cb6d` | 0 |
| keyless/pepper/service/src/main.rs | 22130 | `f17845f1a77d0fc059718b199fed388c5806801dca7ddbc1daf0038e8f0aee73` | 0 |
| keyless/pepper/service/src/metrics.rs | 5820 | `4ce9ee9beab799c1ffc8a1605baaa3121cdb924f1e979a4cc670390bbc4284f4` | 0 |
| keyless/pepper/service/src/request_handler.rs | 16211 | `bc5f4ac466b5ef451296854e8d7235ec92a6cf6358dd520ff2b073e4bcbb3d7b` | 0 |
| keyless/pepper/service/src/utils.rs | 4725 | `f71a94fe71c1d7e586e2d0e9eafc696229fd9be28117fe45563070311f50a65f` | 0 |
| keyless/pepper/service/src/vuf_keypair.rs | 9269 | `6fff64509d9751551aa54b9eb761c706248cf282110c0b22e508e850edde694f` | 0 |
| types/Cargo.toml | 3901 | `4b2f8b535413b475490f0f28c5e914d704ae7acc2e212da99dfaec951952a2bd` | 0 |
| types/src/access_path.rs | 8030 | `ecf1c87c4ae66b9d015a3a79e461d30b7c6053424feea1d266f60621531a11e6` | 0 |
| types/src/account_address.rs | 9982 | `ee51cce722e41a743f94cf1fd4d0a38034ff59bf9fb2682700437155f1a134bb` | 0 |
| types/src/account_config/constants/account.rs | 291 | `66b83be874fa71d9e9e169766ccdf54e5f7ff0ae4143aeb1c4cf8577834478cf` | 0 |
| types/src/account_config/constants/addresses.rs | 591 | `e75ffbffa7ede1a76c512107626319667e0c717af818a00459b6048e54f6ad3b` | 0 |
| types/src/account_config/constants/mod.rs | 255 | `9bd540838b6c6a1416e55c53df5c70cf2788def18312b7d9c9e338c1f97be5b3` | 0 |
| types/src/account_config/events/burn.rs | 1892 | `c24924e6e051c9a5a6f42f992a0dc1675262e8754a203ec12c0dbffeabfffa88` | 0 |
| types/src/account_config/events/burn_event.rs | 1504 | `70fb45d7c905e922484a965a63d7aa603b4f03934a00a732fb3ff7edc245a819` | 0 |
| types/src/account_config/events/burn_token.rs | 1636 | `0a2147dd902675a676161525e3a29c72a3a3989fa7b1d30c32b843aa1a5a2716` | 0 |
| types/src/account_config/events/burn_token_event.rs | 1461 | `2c9311164a2eb5533132ac625a0f86ccc1e8db9253a0d67c8203a62478e5ac8e` | 0 |
| types/src/account_config/events/cancel_offer.rs | 1915 | `26ffa2a4458524e28ee720975f3d998f4d8088277a02a93a733743d1d1ddfb16` | 0 |
| types/src/account_config/events/claim.rs | 1872 | `9c50ef85c7c28b526c5a97799802976c4066c0032918557bcc35ed8e58d50067` | 0 |
| types/src/account_config/events/coin_deposit.rs | 1690 | `16757d28a363d279c916ad9a4cac1d686e93e6789f9c1347321f335b503e59fc` | 0 |
| types/src/account_config/events/coin_register.rs | 1492 | `6c5292bbdf3064dda11193ba272e910a8634adef6ecaaef3ab80b5f6005c3a8f` | 0 |
| types/src/account_config/events/coin_register_event.rs | 1384 | `4c3e53fa0ad000b3924bbd74ee6a949149b139d770e769073cf67e8893fe622b` | 0 |
| types/src/account_config/events/coin_withdraw.rs | 1697 | `d735f625899b5e8a34716ef5565975b1c8ea4a660759ccafbe7931b872e865a9` | 0 |
| types/src/account_config/events/collection_description_mutate.rs | 2119 | `df20e4d5d529b09805b71073f3cd0ed0bb6b5aa4fb518ea9e9aafe77ed5a6c37` | 0 |
| types/src/account_config/events/collection_description_mutate_event.rs | 2155 | `82dd47cb0882373b42989c339e4936b2b7e782e462810bedcf62d670a60f27e7` | 0 |
| types/src/account_config/events/collection_maximum_mutate.rs | 2033 | `e4c42e3033f660b03a79ee7dceef7bd2172cb8c86353c1a5f5afa6b3fa22c974` | 0 |
| types/src/account_config/events/collection_maximum_mutate_event.rs | 2185 | `c69f706fa4db31fb48f909182b11b9320aa9c2b938e23721cef320d9aae8bffd` | 0 |
| types/src/account_config/events/collection_mutation.rs | 1957 | `c7a1861aaffe4baa5ce79a8b7da397aa6eaae9dbfab506a8eb9ce22bbad013f4` | 0 |
| types/src/account_config/events/collection_mutation_event.rs | 1491 | `5563136b89ee2088893d80fdc3c3c17fafb8fc5292b13156b5f37c0d9e2cc204` | 0 |
| types/src/account_config/events/collection_uri_mutate.rs | 1983 | `66001f77360aa4a77f2cfee42c0d08487399434c68870de2762a75076bebac26` | 0 |
| types/src/account_config/events/collection_uri_mutate_event.rs | 2019 | `30eb9279685e2b2690b761ba68bebb1b189aa3e147e4448c66ae1583822b76e7` | 0 |
| types/src/account_config/events/create_collection.rs | 2036 | `eb758dd19135a11c2ebfb1880c364180db1dfe0c34d8920a3066733d2b41c0a4` | 0 |
| types/src/account_config/events/create_collection_event.rs | 2072 | `13cc4d8c0de81603dd1bf8f024e226338cd4a4d27418f18d679bc8d70e417d3b` | 0 |
| types/src/account_config/events/create_token_data_event.rs | 3489 | `22c9e6ff7cfe18dd4869de248c0f8f117273e9dd31cd59eb535bae812525e46a` | 0 |
| types/src/account_config/events/default_property_mutate.rs | 2555 | `329a5821be637f5b514ea9db6a449cade3213cdb4da73280b51de7f84d2c390c` | 0 |
| types/src/account_config/events/default_property_mutate_event.rs | 2439 | `5af56b944274f5a93f0ae3b138dd3862cdb1305919f93702f788213fd58c4d09` | 0 |
| types/src/account_config/events/deposit_event.rs | 1372 | `d4f4ad058d40936f68a1f05ac171ee626ef132764632909f9a063155f309468b` | 0 |
| types/src/account_config/events/description_mutate.rs | 2123 | `354ea5d42da1e9cef90dffa5e2f8370b98dedbfa51580a7bfb5ec254abd9887e` | 0 |
| types/src/account_config/events/description_mutate_event.rs | 2159 | `04da68f4566a7e30da91c1acd202b714ebe15acead81dffb9198cf447afa71d9` | 0 |
| types/src/account_config/events/fungible_asset.rs | 1190 | `d71f8a7d4c4c95e78d996e133115b4dd9dbdf85bb6c156480ed6b9ed94b51d25` | 0 |
| types/src/account_config/events/key_rotation.rs | 1598 | `b02613ba7e8ee7c2d8b8c1cac22530cf2acf5176ab7093cffd13323c58dff59e` | 0 |
| types/src/account_config/events/key_rotation_event.rs | 1687 | `2af804a0ee759c1d88b94b670fbe614331a481877580e816f52211fa79ea4b21` | 0 |
| types/src/account_config/events/maximum_mutate.rs | 2037 | `2c7bb224f820f453295a3dd6dc49d45b966d9b17f12e9de6e218f42789ff525a` | 0 |
| types/src/account_config/events/maximum_mutate_event.rs | 2189 | `ccb5198dda28140413a3946ddb1115bb203ecfa9fd1c00adf2993bfa3a559cf3` | 0 |
| types/src/account_config/events/mint.rs | 1829 | `1903501a2b45d7fd7af8e0bacad5f00c6e80cef5557b2d6c00b2e62ff7cc8857` | 0 |
| types/src/account_config/events/mint_event.rs | 1482 | `6a4e3c1cec112ad8344e54c88e98c2deb54c80937891e6aa0009ad897c2b508f` | 0 |
| types/src/account_config/events/mint_token.rs | 1652 | `b92411631c4f4677a104c7cc0c6cdc715e75529a652a9885a03b5e005542bd0e` | 0 |
| types/src/account_config/events/mint_token_event.rs | 1477 | `ffedff6de8b976b72cddba5c524223d77e6d53569835c3f0b2abf69711e6e311` | 0 |
| types/src/account_config/events/mod.rs | 3768 | `cae46428243ccb9183462728b1a88f3624d2ac530e0e493766c4b3730b4b66d7` | 0 |
| types/src/account_config/events/mutate_property_map.rs | 2191 | `01bf08c95d4f778c828f962006b6e532bc72149ff543b2635b89f786f8df4e59` | 0 |
| types/src/account_config/events/mutate_token_property_map_event.rs | 2067 | `089ef272e40016c15dbff6e31b7bb49eb2eef0a5055236f9e7dd962a87ae1abc` | 0 |
| types/src/account_config/events/new_block.rs | 3422 | `6c51af4396767ba1e8e27a15fa54dff11a5aca7df789a1c4c2f17fad35cdb74e` | 0 |
| types/src/account_config/events/new_epoch.rs | 1440 | `e32383a2a078bb6345d0972c56b0bde5b9b62f16749444b16f08d35cd7d2d37e` | 0 |
| types/src/account_config/events/offer.rs | 1872 | `75519848e72df15801c2f7e968fdb1a48d1a7c9fbc90d19dd9bd2f2fe53c9814` | 0 |
| types/src/account_config/events/opt_in_transfer.rs | 1612 | `b38bea4b0c23e8cb41f7db331594c56dad898a58f743318aaf6c9608184e19d5` | 0 |
| types/src/account_config/events/opt_in_transfer_event.rs | 1399 | `5963affa223809b4689bd48dd9c1ee85c8fa3e6f0ec1e8191d013ad9a701d113` | 0 |
| types/src/account_config/events/randomness_event.rs | 452 | `3974575a5db8370988527fc4ccf8bbf142464f9b22bddfa5e427e11db46a05a7` | 0 |
| types/src/account_config/events/royalty_mutate.rs | 3017 | `233369e803809a257377f6474981eb89344daaa97e419752f6b785cf8ff362a4` | 0 |
| types/src/account_config/events/royalty_mutate_event.rs | 3053 | `829f203adcac2673f54aadf8793b3523a36bff5b279982b5a33f707a94748d21` | 0 |
| types/src/account_config/events/token_cancel_offer_event.rs | 1797 | `02034248d5773d0ab8ef36c121df52f4acece99e6af945855c9ab3de82c7fc6e` | 0 |
| types/src/account_config/events/token_claim_event.rs | 1754 | `7374dbd5f68ff8bbb1a15b53ed0b1ea4e246cb03cec7cfcfcd3048901520d02d` | 0 |
| types/src/account_config/events/token_data_creation.rs | 3773 | `9b854a1a1b484ef05f42858d95640fed0f103105b04c88a52413bde4c1f37083` | 0 |
| types/src/account_config/events/token_deposit.rs | 1918 | `2ab3a3dc953576c5d92d07f5730317e31e50c2966800980790106184b8c8fdb0` | 0 |
| types/src/account_config/events/token_deposit_event.rs | 1472 | `5158edcc6a3527bfd8897e2c4e21b92657e2ea8d3ccf393eb97c967645f00c0b` | 0 |
| types/src/account_config/events/token_mutation.rs | 1972 | `a31ff06bde4633c2d137dd9b6fd2b8ac7c17b589941f449053ab6d18e91f0d63` | 0 |
| types/src/account_config/events/token_mutation_event.rs | 1751 | `f9209e94a9b5826881bf793cf12cea919292e6cab98397d380a70f96dc7f9845` | 0 |
| types/src/account_config/events/token_offer_event.rs | 1754 | `68c6306735f87252bd206ec16b9c76c9fef8ec70d3926606731480dee2ccd404` | 0 |
| types/src/account_config/events/token_withdraw.rs | 1674 | `3fcc76d0c18d28be43f919ea32643006f2fc9442b0fd758fe286f9c2747d11c8` | 0 |
| types/src/account_config/events/token_withdraw_event.rs | 1479 | `75a5b0c64f591cfc3d54777c38edc8782d1abef1087c915ef3800414902cd234` | 0 |
| types/src/account_config/events/transfer.rs | 1627 | `d9fc333437a3c74dce22510c23b6b85163934bc1b07e12c591ffd38df39ac2e8` | 0 |
| types/src/account_config/events/transfer_event.rs | 1663 | `24b769e37a7cc7b048ad20436e88819f7a6bdcacd37912742620b367f7d522ce` | 0 |
| types/src/account_config/events/uri_mutation.rs | 2001 | `a2033d3da1291df0657edfbfd3f6b2c329acfdea5fda8c052285d4b1ac0e7cf3` | 0 |
| types/src/account_config/events/uri_mutation_event.rs | 2037 | `5c413788631c906e373674bb2c7d275f16f2ec8f2c8afa37a26d466b5fbc7500` | 0 |
| types/src/account_config/events/withdraw_event.rs | 1386 | `a10fcbf44e4d70cc155aeab757e9d72e25b232c1cd2d8652f4ad21dfa0d09d19` | 0 |
| types/src/account_config/mod.rs | 294 | `069bf0839db38747fa1c078b13a3237ee38871e0293f20c4354afd4278d60331` | 0 |
| types/src/account_config/resources/aggregator.rs | 2079 | `2a823ffa3b715d233a4284fe09802e39006ca560032bd945e4d3ffbb9bc7a0ad` | 0 |
| types/src/account_config/resources/any.rs | 1182 | `59a0d430f860cb217f83f408f79e02e081baa3924565c37577b97b1daf99c939` | 0 |
| types/src/account_config/resources/chain_id.rs | 936 | `46581f07a365c5b892d71651d5f4b3a5c2712ef832496542721472b3776c444e` | 0 |
| types/src/account_config/resources/challenge.rs | 1143 | `bff4e473aa8ae9967397ff315c150661f2449eba8ba75f17b9b4da69961515e4` | 0 |
| types/src/account_config/resources/coin_info.rs | 3661 | `be64345b9157cc123d35ceae80d41c097ebd48a85191d54c2e2d8031d104c008` | 0 |
| types/src/account_config/resources/coin_store.rs | 2804 | `c23f3df613e8b36b4f3414fd0b1819beaf5119c4af91706a78b6ff0250adf7a0` | 0 |
| types/src/account_config/resources/collection.rs | 1552 | `7c3829f3ce65b764253948401442ffe5d2a23ac5b31efbec6fa5e774d4824bd7` | 0 |
| types/src/account_config/resources/collections.rs | 1775 | `ff1957ea66c93012b4c003b754a34976ea383d5a7728496a29eabd973a9546cb` | 0 |
| types/src/account_config/resources/core_account.rs | 3492 | `976192647c086fcd8bab104396679da6ef1563166713863e8ecdb72b6a11c64b` | 0 |
| types/src/account_config/resources/fixed_supply.rs | 1568 | `6cf325e3053de8b7b42477df4ebfd46a4dc9090427cea54e4bd3d56ec9efc617` | 0 |
| types/src/account_config/resources/fungible_asset_metadata.rs | 752 | `31fea1b80b4ecf16e4660b19946f61cd10d1352247ed46a8c248b1b358940fc6` | 0 |
| types/src/account_config/resources/fungible_store.rs | 2944 | `c1065e321eee5c0914fdef5f7df59c7814e4df86f960df9687b70e36fab9f4bf` | 0 |
| types/src/account_config/resources/mod.rs | 1038 | `ff09916e3eb34d268d84f0298f642536d7c3166c33801d7f8e14c379a2be54d5` | 0 |
| types/src/account_config/resources/object.rs | 2529 | `67b5c54c89652c17c90a8f01b3f40dea3c1b3029a02dc04c5b1110cb77b15eae` | 0 |
| types/src/account_config/resources/pending_claims.rs | 1523 | `7094138db58b287b2c69bf85f902279fdbe6b5d453e55325a5965d95d677d5bb` | 0 |
| types/src/account_config/resources/token.rs | 1626 | `798de48d5a2808531f4ee818c550a6f8786554bbe4aad6c1f4840f6c10f993f1` | 0 |
| types/src/account_config/resources/token_event_store_v1.rs | 3168 | `91226223b3778d5e9062946f7321091e58fd30dcb531ef5a74f953de5eefca6f` | 0 |
| types/src/account_config/resources/token_store.rs | 1978 | `04f0284e9b47b37ac868d72d42c6b0da4925bd5e40bd4c7b0e99353be72c9e76` | 0 |
| types/src/account_config/resources/type_info.rs | 1365 | `445e2ac3054261f058c66b798ddf94d8b853925215693db88aa05c6b483e5a4d` | 0 |
| types/src/account_config/resources/unlimited_supply.rs | 1449 | `fb868e5477a052260fa20dadf8a49be5e321911d5c8c9d66b6b15b7b97e0360c` | 0 |
| types/src/aggregate_signature.rs | 4701 | `7393bfbbb65bb784d967dffee8ef94d02181b7635a82ffb7e8a6e639286f0ba2` | 0 |
| types/src/block_executor/config.rs | 10057 | `7e76b1a2863363523e44023e3ae1baf3492edc130cf330a43205ed37004ca79d` | 0 |
| types/src/block_executor/mod.rs | 280 | `ed1ec89a20802b3438c1c274cb86fbe48ec6337f0fd52fc0b66ca52ff924921d` | 0 |
| types/src/block_executor/output.rs | 2405 | `a33715e27c11fcacd7c29dd16c2791d9bedcae8e538eb9d8ec742fe65f127f7f` | 0 |
| types/src/block_executor/partitioner.rs | 18596 | `a2fa5d1682231e46bf00c0205f9fb7e7a2a5168f5533083e3cfa24cd85f3e422` | 0 |
| types/src/block_executor/transaction_slice_metadata.rs | 6098 | `095be58d8c8f719019ee32ed4e043415c750c86c4058e71b35125b9a08880fd1` | 0 |
| types/src/block_executor/value.rs | 4333 | `1e8e1033ace6235a0415bd0b3d227b2b669290007ce2051636be520f51483b41` | 0 |
| types/src/block_info.rs | 8273 | `a842d82896dc618bdc9c6e0cff7035a9b4768130e54f8bbd72a78d2b3b7d650c` | 0 |
| types/src/block_metadata.rs | 3333 | `db388a5a2d123f5155d226dc08ebcf0e6369e16264f252c78d5d6c4283ceed1d` | 0 |
| types/src/block_metadata_ext.rs | 7575 | `4ac13141cf2f5600fffa9223986b0cc0bac9e681c43c9953c253e2a9581b2aa9` | 0 |
| types/src/bytes.rs | 399 | `bdce4dd1ab649d5a46d3fa3368b868ee8cdd6b6213dddd2c4f556944aeaec00a` | 0 |
| types/src/chain_id.rs | 7625 | `22df94b24040c9eefeb02b01fed59887338dd08b37243f2a94ef7da12ae123b3` | 0 |
| types/src/contract_event.rs | 13940 | `d93e983c084ee74762681eaca670fb908e81869fa2b5801d1d483b8d241ed677` | 0 |
| types/src/crypto/algebra.rs | 12420 | `757bba4179583778fb17631a7fcf97910694f663bbbd7d7403141265745f4f14` | 0 |
| types/src/crypto/mod.rs | 275 | `d7a97e463e3edff1c6ae4cb29cb88093bb5ee9104f001c58ba8824b90e9969d9` | 0 |
| types/src/decryption.rs | 3374 | `455b57c4969a59466028d7665799ec5668112921d3ae99fe670c10be30d8675a` | 0 |
| types/src/delayed_fields.rs | 4514 | `e78460e1644c67037bef3315f6ade600d7be93e0567f378544d1ec1b7a64fb4f` | 0 |
| types/src/dkg/chunky_dkg.rs | 22794 | `825c5797d23258c038b228dd800f1df42c3832dc1578d42eb0d45a9ed9175c49` | 0 |
| types/src/dkg/dummy_dkg/mod.rs | 5062 | `cd6236d967f1937866751af820d09a3430c7c5b648a2536c3797b22032f72bd5` | 0 |
| types/src/dkg/mod.rs | 539 | `63f2c96d28c8fbee7d76365619712776465f4e024a6db5ddadfc97b12f0956d3` | 0 |
| types/src/dkg/randomness_dkg.rs | 7929 | `45f99df2a9c913686a82ed5495b83284ed8379cecea4c3c3781f62877cf45684` | 0 |
| types/src/dkg/real_dkg/mod.rs | 16211 | `1a4dfedefc039e982e0e825e945abe240c7048829bfbbfe6aaade2b3af4c0fd2` | 0 |
| types/src/dkg/real_dkg/rounding/mod.rs | 14699 | `8093ddc9417f1e1c71a91a92a60d49058e0a57b88662ef394c4c605b8f0e9bad` | 0 |
| types/src/epoch_change.rs | 15554 | `1dace03de73eddd86587af745c5d10cfa4021e6bf2a6f286e9ab8bf8180957b4` | 0 |
| types/src/epoch_state.rs | 2195 | `553785c9bc90679e7fa4c54951e60787ae0229891296fabc8a8aa479ab3653c4` | 0 |
| types/src/error.rs | 6934 | `f3941c855e3d6e88a479b1dfac773b9c610a3616f791ba06cd13452e76c714b3` | 0 |
| types/src/event.rs | 3336 | `a8aad7b38c093ed895437bc8afc374509d5312dc69b5f14bd02a1a35a3bea9bf` | 0 |
| types/src/executable.rs | 974 | `d96823fbceaae0567772910dea3c8b7b8d108816eb4b6b18c23334bfd9885ca1` | 0 |
| types/src/fee_statement.rs | 3976 | `3db2c9f5c8089bd203561395faeacf480708e64f96643c67921a43390ab9e324` | 0 |
| types/src/function_info.rs | 2070 | `6ba4fec2c2f5b80a17ba6be6e6ae0c0677a62c4bc712a800004bb46a08dcbb5f` | 0 |
| types/src/governance.rs | 359 | `b7e1339a36e98d037cf65d56964c07deca497b7999228410950045dd98011e1f` | 0 |
| types/src/indexer/indexer_db_reader.rs | 2500 | `c835f4f244b40c8cceb2bd6cc1498caee03d0663b9c697cf037c184deb52e62b` | 0 |
| types/src/indexer/mod.rs | 203 | `c0f455b28784da3333bf2a8b36177ba5f4c2a1d2c0ddd0ecc448ed8e5fbcf336` | 0 |
| types/src/jwks/jwk/mod.rs | 4028 | `604662d9550e09ded059a2e30569f13d82392e447f64cd5d1bd82f7f55486999` | 0 |
| types/src/jwks/mod.rs | 15517 | `dc31f041e311baf548ee741823e000ccf6c82a6e8a69d1ec3fd3a5aca697d940` | 0 |
| types/src/jwks/patch/mod.rs | 1233 | `1fe0d1ff6faddebce8e774199123b32a08b1d8c6389677d33f1bd96732f03716` | 0 |
| types/src/jwks/rsa/insecure_test_jwk_private_key.txt | 96 | `20016265e8d12b02cde1ddbe782ce70e944d46e0d546bcc3bb99c45d10073143` | 1 |
| types/src/jwks/rsa/mod.rs | 7011 | `f5389d0b7d210a3ce2ff377055ee7f2352c48d9893cf2cf8cf72f586e234bd15` | 0 |
| types/src/jwks/unsupported/mod.rs | 2238 | `c8a1faa6698059932f1b89d205af3d80ee931971890fe94ee88e17144e746465` | 0 |
| types/src/keyless/bn254_circom.rs | 16339 | `8493c75c555dad296ad5867c5bc8ae58fd14bc3fb253d2c6b665aea39c359743` | 0 |
| types/src/keyless/circuit_constants.rs | 4443 | `4e47662a9faa45b82f150000e9557dedeb476c0b1a13fb68fdcf589f9b15ec8b` | 0 |
| types/src/keyless/circuit_testcases.rs | 10671 | `792305e4068a22b3a300c4734f5f2d27b29f506f04f1f3107bf5bb0872e216e8` | 0 |
| types/src/keyless/configuration.rs | 3566 | `63b2c1dda971d46b27abefaf0100e9e47558e74d518b5376b185fe15d787e606` | 0 |
| types/src/keyless/groth16_sig.rs | 8306 | `9de9c6410d73e6d2f7bd990b378957661e189b58e84c4e899b18d6cb3643ed8c` | 0 |
| types/src/keyless/groth16_vk.rs | 5826 | `9f69a4e8d6e56d2ae1a57ecdb9473b0429f0e426bf79654e71efadcb54ce7c41` | 0 |
| types/src/keyless/mod.rs | 18837 | `aec84ffbda933e5e148001155cd65cd20890ad13d6bacadc89818ce16bd5f232` | 0 |
| types/src/keyless/openid_sig.rs | 8562 | `512e5e37c795208f20fe6049ebe68b15b2f73589ef1fe7063910d351ce69343e` | 0 |
| types/src/keyless/proof_simulation.rs | 14668 | `bf98dac69c4c14a0f2e54b6a3a3d363118a1606442835cb675bf33ab3530b50d` | 0 |
| types/src/keyless/zkp_sig.rs | 783 | `6395f99ff356f33bd4f10ab26c8270a7b71fd2532f533a43ad93d49c2d10adc3` | 0 |
| types/src/lazy_bls.rs | 14480 | `1584138e4a7bbeaf8b407a86cd657a87520bd82f05d5c77134374f1983ae0985` | 0 |
| types/src/lazy_crypto.rs | 5590 | `da03c7bb79b5be9529c23cdd322ed24058c8084e63680ededc47cfcbf993834f` | 0 |
| types/src/ledger_info.rs | 41824 | `092d6395d8a0ede0b4a356d883abbd002df46083fc07d011cfad0f36e3a8f7ea` | 0 |
| types/src/lib.rs | 1743 | `43dbe71d6eaadbd8c370ec02cd9b22800eb3a8c02da4de0018dc80e978462721` | 0 |
| types/src/mempool_status.rs | 3205 | `dcd3837a4bf1028567252be0fd62785499f28d40104301b5cab09fcdf324a8c8` | 0 |
| types/src/move_any.rs | 1494 | `48f5efbb3faa42b64509bdd33fe525fe8b0713d36a2b1ce0979bce91b6c40fcd` | 0 |
| types/src/move_fixed_point.rs | 587 | `511cea51c9a17245c51b385ee3fb92732769b9459d5e0b5fb90fbf48c2c9a7f1` | 0 |
| types/src/move_stdlib/mod.rs | 337 | `0162dd9ea9a9fcc719d1964b038c07ac08aded852f7e385f73312da39e8171b6` | 0 |
| types/src/move_stdlib/reflect.rs | 1335 | `a6366318338d301c6b7e542668065926c106d3b33c249ef355ec6c5aa0ff6aa1` | 0 |
| types/src/move_stdlib/result.rs | 297 | `b0069dd5fb5ce823d2d19173e3d96b0c1bf7277e8cc2419e9bb7ddc65f85013b` | 0 |
| types/src/move_utils/as_move_value.rs | 1550 | `b5e42802a0b157bbb7979eb395779268a3c7bb75ec603922f0bf051e8bd0f03c` | 0 |
| types/src/move_utils/mod.rs | 1409 | `8683e9930a62fef5362f0261336ae3a0af1d6acff56fd0be6ce22594fbef1ef2` | 0 |
| types/src/move_utils/move_event_v1.rs | 796 | `bee404230e9a9bce07c6093b12a1b017670251e195940e07ecf1edc7fd6cd87e` | 0 |
| types/src/move_utils/move_event_v2.rs | 585 | `c6410bf68680dd2c293d00f0d44caff97dd684dfd888603be124ba292b4ebe83` | 0 |
| types/src/network_address/mod.rs | 36409 | `4975d0e2ec175a34a40327721910a12733f99070948a0e1a9db1742b98a09853` | 5 |
| types/src/nibble/mod.rs | 1676 | `bcf4607f4d63f6d2c8bcab777e765bdc028deeba411199f9b760525f48932785` | 0 |
| types/src/nibble/nibble_path/mod.rs | 12503 | `2311ed09285a54b2ecef5b1ee2a053b58f7df3db342283e48855cb739cbe94f8` | 0 |
| types/src/object_address.rs | 733 | `b5adb0735fe5d0fca5f5c9bd155adfd9bc9620c3db31367ecc9d725a6221f2d0` | 0 |
| types/src/on_chain_config/approved_execution_hashes.rs | 998 | `dc3e031a1973c42f3d6b1de92c32ea0ef51ed5492245a66d520a88d6758e1c4e` | 0 |
| types/src/on_chain_config/aptos_features.rs | 30005 | `cb348034ebdbadca299ac0a6173f86585bfa2a803d2fe48a9c78cd6114296bde` | 0 |
| types/src/on_chain_config/aptos_version.rs | 1293 | `252460a676db6df62688db12f0e5cf65f2dbc9b8cf36fa72a3d8dc5e0e5bce5b` | 0 |
| types/src/on_chain_config/chain_id.rs | 385 | `b7263da4a34565e6af67f361ce7faa60b661ff0829aeb5412d895bee9cfc2d5f` | 0 |
| types/src/on_chain_config/chunky_dkg_config.rs | 7460 | `32839bcf2c6cf9fe2304fb083d02dbabfda6848226fd557fa9cff06a1f76296d` | 0 |
| types/src/on_chain_config/commit_history.rs | 1076 | `2309c5e397aeb5547ec1f98b6372b1285690055ac6c1b987e0a23d4fb2caefa6` | 0 |
| types/src/on_chain_config/consensus_config.rs | 22110 | `21a10c32c9ce9ce92e0efc096eb803944c8cbc71a4be17173a2518ca1169ce60` | 0 |
| types/src/on_chain_config/epoch_timeout_config.rs | 1375 | `258a66fea4fd2b8c755582004f626e414d901cef596adedb7574c609f874a7af` | 0 |
| types/src/on_chain_config/execution_config.rs | 21780 | `89c1b5b455c234b99c8b94b574910fb5349a091b3b035cab054abd9ba9a34b1b` | 0 |
| types/src/on_chain_config/gas_schedule.rs | 3299 | `66d346bb0d05329c64f10a552180fa8502a27fc11f5bf3509fb595e2d742ef40` | 0 |
| types/src/on_chain_config/hot_state_config.rs | 5812 | `04a8f61991754c704fa2cc6e421b109a912ace5a83c23c0614a3bf3b55936ba0` | 0 |
| types/src/on_chain_config/jwk_consensus_config.rs | 4353 | `e4e99234695856703e9bed9d26df4bb77a8788d9cde372783c0621b29ae5441c` | 0 |
| types/src/on_chain_config/mod.rs | 10154 | `727ceb6f8f2925fc5c5de50570327b3fc6f9bd7c5019bc9293c71574c7a6d912` | 0 |
| types/src/on_chain_config/randomness_api_v0_config.rs | 1661 | `03eb08ca61b212a02209feafdc03d768611b38d1078b358fe3c29835aafd5749` | 0 |
| types/src/on_chain_config/randomness_config.rs | 7931 | `3b8d9f3396a7824ee4e71796cbd206424e3743f5f2945e9916806b9cc34543ae` | 0 |
| types/src/on_chain_config/timed_features.rs | 25211 | `cf14230f8b9407a9f7f8531230ebf8a9d6f37f9f90d52d6b4a6179f5e8392297` | 0 |
| types/src/on_chain_config/timestamp.rs | 564 | `9b9828e5d45ce4ca8b9eae722baf8030d5b3164a9235e14b40a97e442069beed` | 0 |
| types/src/on_chain_config/transaction_fee.rs | 534 | `fe9c48693907de4f0153bded4d9d2fa0d4650eff54921958511656b11c8df917` | 0 |
| types/src/on_chain_config/validator_set.rs | 3113 | `8566fa8178e7b1c8022afb6b0254b0f9c01398a30a93776c99f06d58786811df` | 0 |
| types/src/proof/accumulator/mock.rs | 12581 | `e94346c424accd0c2e7b3522f037dd21b7ff41b08ae802948fa79be33b893e02` | 0 |
| types/src/proof/accumulator/mod.rs | 15444 | `a23b47e6f3625080c47d4f9eab21977633df847a59e8928b9d9905f3cdae9b9d` | 0 |
| types/src/proof/definition.rs | 37684 | `208c571bdaad6894a92892eae79bbe3fe19a4f6cce39fcea0c3ea16df00e1db2` | 0 |
| types/src/proof/mod.rs | 3775 | `703ba773bb02adde8d2d052827caae891bd4b295f23f92e5504af0c96d5575c3` | 0 |
| types/src/proof/position/mod.rs | 18304 | `7a3200534d3829481fb9e3448017207a67ce075537b7a101f8814bc8e427ba9b` | 0 |
| types/src/proof/proptest_proof.rs | 5430 | `b81799ba3c19984b42acb560ccb85147d07f765056873e7c5f4fdfb5508a1976` | 0 |
| types/src/proptest_types.rs | 45523 | `8f72d7856db3e71d1d5938d3a4be9ea2ec9ddede1ffc3a640557dad324c072a3` | 0 |
| types/src/quorum_store/mod.rs | 1611 | `48b8fdec0d02837e434eb93216933528247e266bd2008786de1c8f24e4c89cc0` | 0 |
| types/src/randomness.rs | 4002 | `0b85879162c6fab76de3ee0045520fab66319e5d4f20b6135340c0dab4741f02` | 0 |
| types/src/secret_sharing.rs | 6979 | `cc7123acff99e51126a5d1ba7f3f7d445cc1b3463603641a6aafc18bef9be1a2` | 0 |
| types/src/serde_helper/bcs_utils.rs | 1003 | `3fd10762a50f266e9d5a0f8dee245b16f64affa1051477df379a2516766bcf0b` | 0 |
| types/src/serde_helper/mod.rs | 214 | `fc197ba018cf7f78fc8c32a40f707f4689afbb592349482860ab5521c55c65a7` | 0 |
| types/src/serde_helper/vec_bytes.rs | 816 | `3f90b12f602af5408b032cc3a99e37909edcbb8ea0608edc693aef34b85f2f70` | 0 |
| types/src/stake_pool.rs | 3360 | `cc81818fb29765d04a365ef2d45f1f198fcf00e2309cc3effb49b590d363e22e` | 0 |
| types/src/staking_contract.rs | 1574 | `9c126979748aa93f21bf9912517cb8296d21b48e8fc34b0af869ec8610e82e0e` | 0 |
| types/src/state_proof.rs | 2319 | `b963f76385b9e6928b234337158a2eb23714885235c04f1f832891e20637ee78` | 0 |
| types/src/state_store/errors.rs | 580 | `0b8abd23aa009e47cff1ae0480e9fc6c59062655334118d8f6fc82f1e6bd50f5` | 0 |
| types/src/state_store/hot_state.rs | 5855 | `73de17ceef0d54f28d4bb854d01267ea8dde7766de6fda03dfe424d88d3faf23` | 0 |
| types/src/state_store/mod.rs | 7167 | `1eaaee36c1cdbb979fc3bb2b7909affe27cbd1308abbf3da41d64225818cde67` | 0 |
| types/src/state_store/native_collateral.rs | 7379 | `89012a8a387cc3e784dc8337d93bdf3f66c4537b2f39583a7b1be0f98ff942ca` | 0 |
| types/src/state_store/native_order.rs | 25001 | `8bc7ffe26c5a4cc4a43bed10272d495d22dd0c4372e8101b13e183b1129ef52b` | 0 |
| types/src/state_store/native_position.rs | 5208 | `ad7eefbe41bbf2c94ea8525b70a15c903593d4402764278e0374734822e0d214` | 0 |
| types/src/state_store/state_key/inner.rs | 9976 | `37c10fb9b52d27ecc6e17d6ddd4e7169edb6026a5f3587044606dee925e31b86` | 0 |
| types/src/state_store/state_key/mod.rs | 20535 | `903390ef5c9a3af2ddb9a120b9b9f872bd31e544785f91b4aee01596c894f748` | 0 |
| types/src/state_store/state_key/prefix.rs | 2617 | `1332a959b0ec7404e1495a76146110c2cadcb45b7571076ff3ae58f7ee812488` | 0 |
| types/src/state_store/state_key/registry.rs | 13622 | `c45ee16c8f31c18e5a84862714fbc0e4bfcf00bd8d4623a64c66415e3fa51bff` | 0 |
| types/src/state_store/state_slot.rs | 10300 | `89e8c250501930cb6498aac18b7fb54bbea812e331dc856f01cfd84504de930f` | 0 |
| types/src/state_store/state_storage_usage.rs | 1627 | `9a1c79a9e14e50f02fa3326873374a09f02f3df2e9e4038a68b83c9fb73588f9` | 0 |
| types/src/state_store/state_value.rs | 12200 | `9dcce2dd86ededde31650855a6c9dec6e67840b85345a2939f880d96b56dc509` | 0 |
| types/src/state_store/table.rs | 1423 | `38c815170f3bb244ef44450185300b1a9079369f0dfdf7b6d50fd5f9989aff86` | 0 |
| types/src/timestamp.rs | 778 | `86886ea56b28a95ace95f0a300a088dc5cd19c4d745161684a6327a14ed0de30` | 0 |
| types/src/transaction/analyzed_transaction.rs | 10548 | `29d40e893c1de3c399de81fe021c4f049f586896eed62039606a8b71625d8d98` | 0 |
| types/src/transaction/authenticator.rs | 97841 | `30fa99d247f36e2e359534968093be3d21c9dc3c147ba4c2020144da0652b6c3` | 0 |
| types/src/transaction/block_epilogue.rs | 5362 | `7cb091e80364786b45fafd187c76b40e00f079682fba76b5ce6a9ff5690cd58f` | 0 |
| types/src/transaction/block_output.rs | 2040 | `4c805459fbcd14aad7d4795493457e7d113510170f6e438b7987284bfc97fd5e` | 0 |
| types/src/transaction/change_set.rs | 950 | `44b85b95f9fd0e6d8ed9470b63be690e49b570219468b76c0570a34c01047c7e` | 0 |
| types/src/transaction/encrypted_payload.rs | 12484 | `f0591e21df64c7f8642119302e13c9e0ebe87ccae3183e11662a53ac11065d34` | 0 |
| types/src/transaction/mod.rs | 132928 | `88fc7d10033dd069293d85da58869b5768149ae6c8d1138de171781f12572a8e` | 0 |
| types/src/transaction/module.rs | 2146 | `c2d003708fd6ac4da0bca54aad7799e97bff616caac415273ee00a6388259d79` | 0 |
| types/src/transaction/multisig.rs | 4557 | `a4eecb859fa4627155af87d52f4894cbeb3de06c667a4938dbf055130402ae95` | 0 |
| types/src/transaction/script.rs | 4371 | `2a2027fe377911e700b25c4f74e44ac5faaad7576396bfaa8389c403a7eeec47` | 0 |
| types/src/transaction/session_id.rs | 8559 | `cd1f829c9cdae939ff0b049ee09974cad22a68c6d5b78dd9a9b1602fd3f67fd2` | 0 |
| types/src/transaction/signature_verified_transaction.rs | 5530 | `e884a43c33d3a2d34e6bd32ef1e6bd3ee1b395c05bd05c2ba55472668f66cab9` | 0 |
| types/src/transaction/use_case.rs | 13583 | `eab572a6548aba2c0099b87faa170654304acdaa6e61134d4aae5203d8752a58` | 0 |
| types/src/transaction/user_transaction_context.rs | 5042 | `3dd946a13cca89a2bf30909b1f0e72621dd14a6c5d2b68f110c18981e7bd6daa` | 0 |
| types/src/transaction/validation.rs | 6144 | `eaa8a946ac92f3bf40fe1d5dcf028300a6219381987cae99a98c8c92a4ae3d06` | 0 |
| types/src/transaction/webauthn.rs | 43853 | `27b8e1351299b43f17df226ebd75acae01c352c824f045d3006ca5cf9ba768f7` | 0 |
| types/src/trusted_state.rs | 11468 | `890651066fe0b81518f4d4b9304d4739a168fd0575384bce942ac9b4f469da7f` | 0 |
| types/src/utility_coin.rs | 1739 | `f1e11675a7d0f3f9e1c47525fb3f1f6f61f65e04582f0b5afb978996357d3d04` | 0 |
| types/src/validator_config.rs | 2303 | `f7297cbdd6447d0009df70317ab2882a5dd8b01313f853e4907a5f56e5cf4f4f` | 0 |
| types/src/validator_info.rs | 3442 | `b8ceaf28929b6d76e43092874d29dd4fd6950d994322b5bb757e38512ef36e00` | 0 |
| types/src/validator_performances.rs | 527 | `45f92eacfbe85e7887bbfe5fab4b1430dda400af581323b98d524352efaf764d` | 0 |
| types/src/validator_signer.rs | 5137 | `526b657d7e6298a200db93226ef00db6d7eda4c99d7c5bbcd446393a196338ed` | 0 |
| types/src/validator_txn.rs | 2479 | `fbcbe49c93c332928e5d6ddeaab2ebd576140f9ab27b88432fffe0d405c61729` | 0 |
| types/src/validator_verifier.rs | 45626 | `e9a43a02fce8923b4a650ae5b7766dfd14edb2bdeee9887868efcb6635937aff` | 0 |
| types/src/vesting.rs | 450 | `00519bc61fd556235206c390d5c20ad62a2184b72b00077b5cbbcaefb390f72d` | 0 |
| types/src/vm/code.rs | 943 | `25cfc228df49de3e7427822ab05d779d5b6c02135dc45e7635282a54f12bd394` | 0 |
| types/src/vm/mod.rs | 232 | `087e680bcae319fe803bf60f867c5aeacad8234451f1e5e30ffbbf82a327d671` | 0 |
| types/src/vm/module_metadata.rs | 28943 | `f92b6c5476a0da302daf1222d9c5007aac863199d649fffe81703584d29f5abf` | 0 |
| types/src/vm/modules.rs | 1420 | `898742b2db80c5d82bf5d624867a14c93dcd9c915322463b4b9f2c8222f0e56f` | 0 |
| types/src/vm_status.rs | 335 | `078c5919053e6d1cc4b390c0f89ca338d0563be8cb35ec2d80fba4bb78580a68` | 0 |
| types/src/waypoint.rs | 7283 | `371de942d0930a34581935c4ac53fb3801aeed12aa65acbe62c4f1bfbd74c899` | 0 |
| types/src/write_set.rs | 39838 | `0198b5622e7ba3de97474e0771f65b2403fe45e5eae3897ef0de1ea66056266a` | 0 |
