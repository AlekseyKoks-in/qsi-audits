# Security & Post-Quantum Readiness Audit Report

**Project:** rs-soroban-env @ 0c99950e9612 · Stellar Development Foundation — public repository (passive review)
| | |
|---|---|
| Organization | QSI |
| Report date | 2026-11-06 16:05 UTC |
| Report version | 1 |
| Audit run | b6dad59b-c7b1-4e8f-86d3-2c4d7916c720 (Document audit) |
| Analyzer engine | qsi-engine 1.3.0 |
| Risk profile | Crypto exchange, custodian or wallet |
| Content SHA-256 | `9b85f3462552f82353205b89d9274711efee1e99748e272a6e7abd94e0172d1e` |
| Signature key (Ed25519, SHA-256 fingerprint; the signature is the separate file report.sig.json) | `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e` |
> This report presents automated and documented analysis results for the stated scope. It is not a legal opinion, a certification or an attestation of compliance with any standard.

## 1. Executive summary

- Critical: **0**
- High: **0**
- Medium: **10**
- Low: **6**
- Info: **2**

- Confirmed technical vulnerability: 0
- Known vulnerable component: 9
- Confirmed configuration error: 0
- Potential cryptographic risk: 0
- Long-term post-quantum risk: 7
- Improvement recommendation: 2
- Insufficient data: 0

Mosca's inequality (x + y > z): x = 10, y = 5, z = 8 → migration would finish too late under this scenario. _z is a planning assumption chosen per risk profile, not a prediction. A cryptographically relevant quantum computer is not publicly known to exist today._

**Post-quantum maturity: Level 2 of 4 — post-quantum in use outside the critical paths.** Next step: Extend post-quantum protection to the critical roles that stay classical, starting with what can be recorded today (wrapped keys, channel key exchange).

## 2. Scope and boundaries

Mode: Document audit

Repository: <https://github.com/stellar/rs-soroban-env> @ `0c99950e96128beba3319aa96b116646ce974e69` — evidence links open the lines at this commit.

256 files, 2036998 bytes in total, 7 redaction(s); the per-file SHA-256 list is in appendix C.

## 3. Methodology

| Area | Status | Count | Examples |
|---|---|---|---|
| dependencies | checked | 52 | Cargo.lock: 273 dependencies parsed (273 pinned); Cargo.toml: 8 dependencies parsed (8 pinned); soroban-bench-utils/Cargo.toml: 4 dependencies parsed (2 pinned) |
| source_code | checked | 202 | soroban-bench-utils/src/lib.rs: 3 lines scanned with 16 rule patterns and 267 registry patterns; soroban-bench-utils/src/rusagev4.rs: 62 lines scanned with 16 rule patterns and 267 registry patterns; soroban-bench-utils/src/tracker.rs: 193 lines scanned with 16 rule patterns and 267 registry patterns |
| secrets | checked | 1 | soroban-env-host/src/host/invocation_metering.rs: 7 redacted value(s) not reported (comments, test modules, fixture declarations, placeholders, values the source annotates as published, or hex values not bound to a secret name) |
| entropy | checked | 1 | random-number generation: 202 code files read with 0 macro definitions from the tree; 0 ineffective guard(s), 0 weak random-bytes provider(s), 0 weak key-generation site(s) |
| osv_advisories | not checked | 1 | 3 package(s) are built from git repositories (forks or unreleased code), so registry advisories were not looked up for them: soroban-wasmi, wasmi_arena, wasmi_core |
| osv_advisories | checked | 1 | 340 pinned packages queried at OSV.dev; 11 affected |

_Long lists are grouped here; the full per-file list is in the JSON report, signed with the same key._

## 4. Assets examined and not examined

- osv_advisories — not checked: 3 package(s) are built from git repositories (forks or unreleased code), so registry advisories were not looked up for them: soroban-wasmi, wasmi_arena, wasmi_core

## 5. Architecture overview

Static review of the source tree rs-soroban-env at 0c99950e96128beba3319aa96b116646ce974e69. 256 files analysed; of 1132 files, 174 are test, fuzzing, benchmark or example code and were left out, 702 are not read by any analyzer, 0 exceed the per-file limit and 0 did not fit the total limit. Files no analyzer reads include: .devcontainer/Dockerfile, .devcontainer/devcontainer.json, .github/CODEOWNERS, .github/pull_request_template.md, .github/workflows/bump-version.yml. 31 files in build-output or dependency-cache directories (.git, .hg, .venv, __pycache__, build, dist, node_modules, target, vendor, venv) were not read. No requests were sent to the owner's systems.

## 6. Overall security posture

- Indicative posture index: **80** / 100 — _Derived from findings in scope (confirmed and potential issues weighted by severity). Indicative only; not comparable across differently scoped audits._
- Quantum-vulnerable share of inventory: 50.0%

## 7. Detailed findings

### QSI-2026-19557 — Quantum-vulnerable Ed25519: transaction and message signing (2 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:Ed25519:transaction_signing`
- Data source: soroban-env-host/src/builtin_contracts/stellar_asset_contract/metadata.rs
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.3.0 · 2026-11-06 16:05 UTC
- Priority score: 35.6 / 100
- CVSS v3.1: not applicable

4 reference(s) to Ed25519 across 2 file(s), e.g. soroban-env-host/src/builtin_contracts/stellar_asset_contract/metadata.rs:158. Role, judged from paths, function names and nearby code: transaction and message signing. A CRQC derives the private key from a public key that is already known (on chain after the first spend, in reused addresses): funds and approvals controlled by these keys need a migration path.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open soroban-env-host/src/builtin_contracts/stellar_asset_contract/metadata.rs:158 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [soroban-env-host/src/builtin_contracts/stellar_asset_contract/metadata.rs](https://github.com/stellar/rs-soroban-env/blob/0c99950e96128beba3319aa96b116646ce974e69/soroban-env-host/src/builtin_contracts/stellar_asset_contract/metadata.rs#L158) · line 158 · SHA-256 3d7fb8af17a8920210188c6a4caffc601f7bc324ca0d4bb4d80a92121e56c790_

```
  157 |     s.push(':');
  158 |     s.push_str(&ed25519::PublicKey(issuer.to_array()?).to_string());
  159 |     let name = String::try_from_val(e, &e.string_new_from_slice(s.as_bytes())?)?;
```

_file_excerpt · [soroban-env-host/src/testutils.rs](https://github.com/stellar/rs-soroban-env/blob/0c99950e96128beba3319aa96b116646ce974e69/soroban-env-host/src/testutils.rs#L15) · line 15 · SHA-256 c8d71454e9e88769c00e358ff438c6a9feb5ef52d447c80c45bca69a7cd2cb4d_

```
   14 | };
   15 | use ed25519_dalek::SigningKey;
   16 | use rand::RngCore;
```

_file_excerpt · [soroban-env-host/src/testutils.rs](https://github.com/stellar/rs-soroban-env/blob/0c99950e96128beba3319aa96b116646ce974e69/soroban-env-host/src/testutils.rs#L316) · line 316 · SHA-256 ccca624ff7d49ed38d518548cc6e466cad617e88f73ada2129dc23ebf4ce70d9_

```
  315 |         n_signers: usize,
  316 |     ) -> (Host, Vec<AddressObject>, Vec<ed25519_dalek::SigningKey>) {
  317 |         use crate::builtin_contracts::testutils::{
```

_file_excerpt · [soroban-env-host/src/testutils.rs](https://github.com/stellar/rs-soroban-env/blob/0c99950e96128beba3319aa96b116646ce974e69/soroban-env-host/src/testutils.rs#L376) · line 376 · SHA-256 5c948ca4d4acf0e68fb3ff6bfee3dd06b880aa4012d1dd8ac629ba7ca2e85698_

```
  375 |         data_keys: &BTreeMap<ScVal, (StorageType, bool)>,
  376 |         signing_keys: &[ed25519_dalek::SigningKey],
  377 |     ) {
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains adopt them.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-19561 — Quantum-vulnerable ECDSA: transaction and message signing (2 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:ECDSA:transaction_signing`
- Data source: soroban-env-host/src/cost_runner/cost_types/recover_ecdsa_secp256k1_key.rs
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.3.0 · 2026-11-06 16:05 UTC
- Priority score: 35.6 / 100
- CVSS v3.1: not applicable

3 reference(s) to ECDSA across 2 file(s), e.g. soroban-env-host/src/cost_runner/cost_types/recover_ecdsa_secp256k1_key.rs:7. Role, judged from paths, function names and nearby code: transaction and message signing. A CRQC derives the private key from a public key that is already known (on chain after the first spend, in reused addresses): funds and approvals controlled by these keys need a migration path.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open soroban-env-host/src/cost_runner/cost_types/recover_ecdsa_secp256k1_key.rs:7 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [soroban-env-host/src/cost_runner/cost_types/recover_ecdsa_secp256k1_key.rs](https://github.com/stellar/rs-soroban-env/blob/0c99950e96128beba3319aa96b116646ce974e69/soroban-env-host/src/cost_runner/cost_types/recover_ecdsa_secp256k1_key.rs#L7) · line 7 · SHA-256 92080872f39f646ca72af7f62a1a86aafc23f66369b0c021ba531097dc6e1f43_

```
    6 | };
    7 | use k256::ecdsa::{RecoveryId, Signature};
    8 | 
```

_file_excerpt · [soroban-env-host/src/cost_runner/cost_types/recover_ecdsa_secp256k1_key.rs](https://github.com/stellar/rs-soroban-env/blob/0c99950e96128beba3319aa96b116646ce974e69/soroban-env-host/src/cost_runner/cost_types/recover_ecdsa_secp256k1_key.rs#L28) · line 28 · SHA-256 f3357cb7a595c1e3ce6deec4fed0973bae3735ea3092adff5321706ae9d88f8c_

```
   27 |             host.recover_key_ecdsa_secp256k1_internal(&sample.hash, &sample.sig, sample.rid)
   28 |                 .expect("recover ecdsa secp256k1 key"),
   29 |         );
```

_file_excerpt · [soroban-env-host/src/cost_runner/experimental/ecdsa_secp256k1_verify.rs](https://github.com/stellar/rs-soroban-env/blob/0c99950e96128beba3319aa96b116646ce974e69/soroban-env-host/src/cost_runner/experimental/ecdsa_secp256k1_verify.rs#L6) · line 6 · SHA-256 58340089301d1dbfa155c975109ed0bf7958615b3c0a53cda374c00df04c04a4_

```
    5 | };
    6 | use k256::ecdsa::{Signature, VerifyingKey};
    7 | use std::hint::black_box;
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains adopt them.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-19558 — Quantum-vulnerable Ed25519: role not determined (9 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:Ed25519:general`
- Data source: soroban-env-host/src/builtin_contracts/testutils.rs
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.3.0 · 2026-11-06 16:05 UTC
- Priority score: 34.2 / 100
- CVSS v3.1: not applicable

19 reference(s) to Ed25519 across 9 file(s), e.g. soroban-env-host/src/builtin_contracts/testutils.rs:7. Role, judged from paths, function names and nearby code: role not determined. The code does not show what the keys protect; review decides the priority.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open soroban-env-host/src/builtin_contracts/testutils.rs:7 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [soroban-env-host/src/builtin_contracts/testutils.rs](https://github.com/stellar/rs-soroban-env/blob/0c99950e96128beba3319aa96b116646ce974e69/soroban-env-host/src/builtin_contracts/testutils.rs#L7) · line 7 · SHA-256 da5b8c5b9f906fbda229feb92e848a55c67100ba443c96cd7ed1d45e44834fff_

```
    6 | use crate::{Host, LedgerInfo};
    7 | use ed25519_dalek::{Signer, SigningKey};
    8 | use rand::Rng;
```

_file_excerpt · [soroban-env-host/src/cost_runner/cost_types/compute_ed25519_pubkey.rs](https://github.com/stellar/rs-soroban-env/blob/0c99950e96128beba3319aa96b116646ce974e69/soroban-env-host/src/cost_runner/cost_types/compute_ed25519_pubkey.rs#L3) · line 3 · SHA-256 74b96e0e9b3aa5141b6dd1b7ed5f7590736faade905cb0fa9e3ea1fc04b5a809_

```
    2 | 
    3 | use ed25519_dalek::VerifyingKey;
    4 | 
```

_file_excerpt · [soroban-env-host/src/cost_runner/cost_types/mod.rs](https://github.com/stellar/rs-soroban-env/blob/0c99950e96128beba3319aa96b116646ce974e69/soroban-env-host/src/cost_runner/cost_types/mod.rs#L26) · line 26 · SHA-256 f42d84c9a863f0627967b5f03b249c98b9e410073e1e885324d674ec7ca84e00_

```
   25 | pub use bn254::*;
   26 | pub use compute_ed25519_pubkey::*;
   27 | pub use compute_keccak256_hash::*;
```

_file_excerpt · [soroban-env-host/src/cost_runner/cost_types/mod.rs](https://github.com/stellar/rs-soroban-env/blob/0c99950e96128beba3319aa96b116646ce974e69/soroban-env-host/src/cost_runner/cost_types/mod.rs#L42) · line 42 · SHA-256 6b9c07086467aba6a28db1678918325cc31c972f1e0c79307f859b0157940268_

```
   41 | pub use verify_ecdsa_secp256r1_sig::*;
   42 | pub use verify_ed25519_sig::*;
   43 | pub use visit_object::*;
```

_file_excerpt · [soroban-env-host/src/cost_runner/cost_types/verify_ed25519_sig.rs](https://github.com/stellar/rs-soroban-env/blob/0c99950e96128beba3319aa96b116646ce974e69/soroban-env-host/src/cost_runner/cost_types/verify_ed25519_sig.rs#L7) · line 7 · SHA-256 27fd12545ba8cdbed39e35e8e33d4ec4344551df83db28052eb1ef64d82b2e13_

```
    6 | };
    7 | use ed25519_dalek::{Signature, VerifyingKey};
    8 | 
```

_file_excerpt · [soroban-env-host/src/cost_runner/experimental/mod.rs](https://github.com/stellar/rs-soroban-env/blob/0c99950e96128beba3319aa96b116646ce974e69/soroban-env-host/src/cost_runner/experimental/mod.rs#L13) · line 13 · SHA-256 50e2bafcfdae7acadbc0e94bfa00f85ca5b7f4a2639b0518c11ec89070082dad_

```
   12 | pub use ecdsa_secp256r1_recover::*;
   13 | pub use ed25519_scalar_mut::*;
   14 | pub use read_xdr::*;
```

_file_excerpt · [soroban-env-host/src/crypto/mod.rs](https://github.com/stellar/rs-soroban-env/blob/0c99950e96128beba3319aa96b116646ce974e69/soroban-env-host/src/crypto/mod.rs#L39) · line 39 · SHA-256 cc46d772ead6ea569a6eb081e8122217b5cd15b0e9ff554689bac4a153c37c26_

```
   38 |     // Ed25519 functions
   39 |     pub(crate) fn ed25519_signature_from_bytesobj_input(
   40 |         &self,
```

_file_excerpt · [soroban-env-host/src/crypto/mod.rs](https://github.com/stellar/rs-soroban-env/blob/0c99950e96128beba3319aa96b116646ce974e69/soroban-env-host/src/crypto/mod.rs#L43) · line 43 · SHA-256 4bd187849dd9995abe44a09658e6908138d52b8fc02de9fcf43760229a4333e4_

```
   42 |         sig: BytesObject,
   43 |     ) -> Result<ed25519_dalek::Signature, HostError> {
   44 |         self.fixed_length_bytes_from_bytesobj_input::<ed25519_dalek::Signature, {ed25519_dalek::SIGNATURE_LENGTH}>(name, sig)
```

_file_excerpt · [soroban-env-host/src/crypto/mod.rs](https://github.com/stellar/rs-soroban-env/blob/0c99950e96128beba3319aa96b116646ce974e69/soroban-env-host/src/crypto/mod.rs#L44) · line 44 · SHA-256 9d58b2c021c122e57885affb53f02fd2a5fc0cd59817ba5c4b70a7badd009372_

```
   43 |     ) -> Result<ed25519_dalek::Signature, HostError> {
   44 |         self.fixed_length_bytes_from_bytesobj_input::<ed25519_dalek::Signature, {ed25519_dalek::SIGNATURE_LENGTH}>(name, sig)
   45 |     }
```

_file_excerpt · [soroban-env-host/src/events/mod.rs](https://github.com/stellar/rs-soroban-env/blob/0c99950e96128beba3319aa96b116646ce974e69/soroban-env-host/src/events/mod.rs#L30) · line 30 · SHA-256 3482bc89aebfeb8ad0d9b9651d72695d317c56f48b7ac7efad2d530f58e7f910_

```
   29 |             PublicKeyTypeEd25519(e) => {
   30 |                 let strkey = stellar_strkey::ed25519::PublicKey(e.0);
   31 |                 write!(f, "{}", strkey)
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it; introduce an abstraction layer for crypto-agility.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-19559 — Quantum-vulnerable BLS12-381: role not determined (5 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:BLS12-381:general`
- Data source: soroban-env-host/src/cost_runner/cost_types/bls12_381.rs
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.3.0 · 2026-11-06 16:05 UTC
- Priority score: 34.2 / 100
- CVSS v3.1: not applicable

9 reference(s) to BLS12-381 across 5 file(s), e.g. soroban-env-host/src/cost_runner/cost_types/bls12_381.rs:6. Role, judged from paths, function names and nearby code: role not determined. The code does not show what the keys protect; review decides the priority.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open soroban-env-host/src/cost_runner/cost_types/bls12_381.rs:6 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [soroban-env-host/src/cost_runner/cost_types/bls12_381.rs](https://github.com/stellar/rs-soroban-env/blob/0c99950e96128beba3319aa96b116646ce974e69/soroban-env-host/src/cost_runner/cost_types/bls12_381.rs#L6) · line 6 · SHA-256 cbe62e9967b82476495c9289979771bf8833f7794b9da7dff040caf4695bf1f8_

```
    5 |     cost_runner::{CostRunner, CostType},
    6 |     crypto::bls12_381::FP_SERIALIZED_SIZE,
    7 |     impl_const_cost_runner_for_bls_consume_sample, impl_const_cost_runner_for_bls_deref_sample,
```

_file_excerpt · [soroban-env-host/src/cost_runner/cost_types/mod.rs](https://github.com/stellar/rs-soroban-env/blob/0c99950e96128beba3319aa96b116646ce974e69/soroban-env-host/src/cost_runner/cost_types/mod.rs#L1) · line 1 · SHA-256 018bdeb4d2d82bbb73383000c031377b65daa884f6aa060762552569e60b20ff_

```
    1 | mod bls12_381;
    2 | mod bn254;
```

_file_excerpt · [soroban-env-host/src/cost_runner/cost_types/mod.rs](https://github.com/stellar/rs-soroban-env/blob/0c99950e96128beba3319aa96b116646ce974e69/soroban-env-host/src/cost_runner/cost_types/mod.rs#L24) · line 24 · SHA-256 1173daa967547ef6f92015858df988ca204347e3b0c86165f8d56bac7b056555_

```
   23 | 
   24 | pub use bls12_381::*;
   25 | pub use bn254::*;
```

_file_excerpt · [soroban-env-host/src/cost_runner/experimental/mod.rs](https://github.com/stellar/rs-soroban-env/blob/0c99950e96128beba3319aa96b116646ce974e69/soroban-env-host/src/cost_runner/experimental/mod.rs#L1) · line 1 · SHA-256 61704a40c8060cf429540fade251e2c1e888ad9950384d99454d1671677606d7_

```
    1 | mod bls12_381;
    2 | mod decode_secp256r1_sig;
```

_file_excerpt · [soroban-env-host/src/cost_runner/experimental/mod.rs](https://github.com/stellar/rs-soroban-env/blob/0c99950e96128beba3319aa96b116646ce974e69/soroban-env-host/src/cost_runner/experimental/mod.rs#L9) · line 9 · SHA-256 38ff3b522b1267ca4d3296c833e5512d6bc78f147cee0494ec3d69896b690949_

```
    8 | 
    9 | pub use bls12_381::*;
   10 | pub use decode_secp256r1_sig::*;
```

_file_excerpt · [soroban-env-host/src/crypto/mod.rs](https://github.com/stellar/rs-soroban-env/blob/0c99950e96128beba3319aa96b116646ce974e69/soroban-env-host/src/crypto/mod.rs#L23) · line 23 · SHA-256 7990a12f3e16bfef9c4846c4ef99db1fac6a5217e5e22db8ff01a957ee395551_

```
   22 | use generic_array::ArrayLength;
   23 | pub(crate) mod bls12_381;
   24 | pub(crate) mod bn254;
```

_file_excerpt · [soroban-env-host/src/host.rs](https://github.com/stellar/rs-soroban-env/blob/0c99950e96128beba3319aa96b116646ce974e69/soroban-env-host/src/host.rs#L3415) · line 3415 · SHA-256 18ef08fa0a3b37cc3441d8d4bb1466aa33065b16ac19f8229edbede023ef8f32_

```
 3414 | 
 3415 |         if self.symbol_matches("BLS12_381".as_bytes(), field)? {
 3416 |             self.poseidon_permutation_impl::<BlsScalar>(
```

_file_excerpt · [soroban-env-host/src/host.rs](https://github.com/stellar/rs-soroban-env/blob/0c99950e96128beba3319aa96b116646ce974e69/soroban-env-host/src/host.rs#L3439) · line 3439 · SHA-256 89a8366163fe76c93b72608f1660664a4d76ad4083e851695fff38613604ab80_

```
 3438 |                 ScErrorCode::InvalidInput,
 3439 |                 "poseidon_permutation: invalid field symbol, must be 'BLS12_381' or 'BN254'",
 3440 |                 &[field.to_val()],
```

_file_excerpt · [soroban-env-host/src/host.rs](https://github.com/stellar/rs-soroban-env/blob/0c99950e96128beba3319aa96b116646ce974e69/soroban-env-host/src/host.rs#L3465) · line 3465 · SHA-256 6cc20e9377d6f35423e985acb0fa303ed0a23c3d796e183e770af6cf197addd5_

```
 3464 | 
 3465 |         if self.symbol_matches("BLS12_381".as_bytes(), field)? {
 3466 |             self.poseidon2_permutation_impl::<BlsScalar>(
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Classify each usage, record data lifetimes, and plan migration to a post-quantum algorithm; introduce an abstraction layer for crypto-agility.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-19560 — Quantum-vulnerable BN254 (alt_bn128): role not determined (2 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:BN254 (alt_bn128):general`
- Data source: soroban-env-host/src/cost_runner/cost_types/bn254.rs
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.3.0 · 2026-11-06 16:05 UTC
- Priority score: 34.2 / 100
- CVSS v3.1: not applicable

7 reference(s) to BN254 (alt_bn128) across 2 file(s), e.g. soroban-env-host/src/cost_runner/cost_types/bn254.rs:1. Role, judged from paths, function names and nearby code: role not determined. The code does not show what the keys protect; review decides the priority.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open soroban-env-host/src/cost_runner/cost_types/bn254.rs:1 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [soroban-env-host/src/cost_runner/cost_types/bn254.rs](https://github.com/stellar/rs-soroban-env/blob/0c99950e96128beba3319aa96b116646ce974e69/soroban-env-host/src/cost_runner/cost_types/bn254.rs#L1) · line 1 · SHA-256 be13ce1be21acf8085c5bf580cbd12293aa118ec05a6bb03c044a4de43d87b59_

```
    1 | use ark_bn254::{Bn254, Fq, Fr, G1Affine, G1Projective, G2Affine};
    2 | use ark_ec::pairing::PairingOutput;
```

_file_excerpt · [soroban-env-host/src/cost_runner/cost_types/bn254.rs](https://github.com/stellar/rs-soroban-env/blob/0c99950e96128beba3319aa96b116646ce974e69/soroban-env-host/src/cost_runner/cost_types/bn254.rs#L120) · line 120 · SHA-256 9a0f6e8dbd18df5bc4f14ddd7dde622d23472fa85a9cb2a205d1ab776200a560_

```
  119 | 
  120 | type InternalPairingOutput = PairingOutput<Bn254>;
  121 | impl_lin_cost_runner_for_bls_deref_sample!(
```

_file_excerpt · [soroban-env-host/src/crypto/bn254.rs](https://github.com/stellar/rs-soroban-env/blob/0c99950e96128beba3319aa96b116646ce974e69/soroban-env-host/src/crypto/bn254.rs#L4) · line 4 · SHA-256 f7bf8b218395ce977ab90e65b7e49029f29344afa5b619dacdde20dd077539fd_

```
    3 | 
    4 | use ark_bn254::{Bn254, Fq as Fp, Fq12, Fq2 as Fp2, Fr, G1Affine, G1Projective, G2Affine};
    5 | use ark_ec::AffineRepr;
```

_file_excerpt · [soroban-env-host/src/crypto/bn254.rs](https://github.com/stellar/rs-soroban-env/blob/0c99950e96128beba3319aa96b116646ce974e69/soroban-env-host/src/crypto/bn254.rs#L526) · line 526 · SHA-256 a4274c7c0a1836e3effc17a944587fc4523bc97379c56241b9941d97db383452_

```
  525 |         vp2: &Vec<G2Affine>,
  526 |     ) -> Result<PairingOutput<Bn254>, HostError> {
  527 |         self.charge_budget(ContractCostType::Bn254Pairing, Some(vp1.len() as u64))?;
```

_file_excerpt · [soroban-env-host/src/crypto/bn254.rs](https://github.com/stellar/rs-soroban-env/blob/0c99950e96128beba3319aa96b116646ce974e69/soroban-env-host/src/crypto/bn254.rs#L560) · line 560 · SHA-256 05f2a34a6c508f13012111c63e0e6e88430ec4b4a066bf4716afa2a06874d00d_

```
  559 |         // every panic condition has been excluded.
  560 |         let mlo = Bn254::multi_miller_loop(vp1, vp2);
  561 |         // final_exponentiation returning None means the `mlo.0.is_zero()`
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Classify each usage, record data lifetimes, and plan migration to a post-quantum algorithm; introduce an abstraction layer for crypto-agility.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-19562 — Quantum-vulnerable ECDSA: role not determined (6 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:ECDSA:general`
- Data source: soroban-env-host/src/cost_runner/cost_types/sec1_decode_point_uncompressed.rs
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.3.0 · 2026-11-06 16:05 UTC
- Priority score: 34.2 / 100
- CVSS v3.1: not applicable

23 reference(s) to ECDSA across 6 file(s), e.g. soroban-env-host/src/cost_runner/cost_types/sec1_decode_point_uncompressed.rs:5. Role, judged from paths, function names and nearby code: role not determined. The code does not show what the keys protect; review decides the priority.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open soroban-env-host/src/cost_runner/cost_types/sec1_decode_point_uncompressed.rs:5 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [soroban-env-host/src/cost_runner/cost_types/sec1_decode_point_uncompressed.rs](https://github.com/stellar/rs-soroban-env/blob/0c99950e96128beba3319aa96b116646ce974e69/soroban-env-host/src/cost_runner/cost_types/sec1_decode_point_uncompressed.rs#L5) · line 5 · SHA-256 7d2cb0b1b110ea53e52a6a1c0f0e5651f2b202b8ee2d8a87a785a863cef85eac_

```
    4 | };
    5 | use p256::ecdsa::VerifyingKey;
    6 | use std::hint::black_box;
```

_file_excerpt · [soroban-env-host/src/cost_runner/cost_types/verify_ecdsa_secp256r1_sig.rs](https://github.com/stellar/rs-soroban-env/blob/0c99950e96128beba3319aa96b116646ce974e69/soroban-env-host/src/cost_runner/cost_types/verify_ecdsa_secp256r1_sig.rs#L5) · line 5 · SHA-256 f2d53d01d18c1fcc2292c319846326c466197df63a11674ca35578b3d82a2a58_

```
    4 | };
    5 | use p256::ecdsa::{Signature, VerifyingKey};
    6 | use std::hint::black_box;
```

_file_excerpt · [soroban-env-host/src/cost_runner/experimental/ecdsa_secp256r1_recover.rs](https://github.com/stellar/rs-soroban-env/blob/0c99950e96128beba3319aa96b116646ce974e69/soroban-env-host/src/cost_runner/experimental/ecdsa_secp256r1_recover.rs#L7) · line 7 · SHA-256 f935f9980262fe702e4e637a6cf0d94ad4f11c566858c98586bc13d04001bcb0_

```
    6 | use ecdsa::RecoveryId;
    7 | use p256::ecdsa::Signature;
    8 | use std::hint::black_box;
```

_file_excerpt · [soroban-env-host/src/cost_runner/experimental/sec1_decode_point_compressed.rs](https://github.com/stellar/rs-soroban-env/blob/0c99950e96128beba3319aa96b116646ce974e69/soroban-env-host/src/cost_runner/experimental/sec1_decode_point_compressed.rs#L5) · line 5 · SHA-256 198adb0a3b79fd9b102dd1d8010f7ec744f8079e2a92651a7102cc7ae2294827_

```
    4 | };
    5 | use p256::ecdsa::VerifyingKey;
    6 | 
```

_file_excerpt · [soroban-env-host/src/cost_runner/util.rs](https://github.com/stellar/rs-soroban-env/blob/0c99950e96128beba3319aa96b116646ce974e69/soroban-env-host/src/cost_runner/util.rs#L12) · line 12 · SHA-256 ae5512776b1eff8b7ccfcfb61c0d70042d1f24134c5c6eda6ece2ae4ae526f1e_

```
   11 |         &self,
   12 |         verifying_key: &k256::ecdsa::VerifyingKey,
   13 |         msg_hash: &Hash,
```

_file_excerpt · [soroban-env-host/src/cost_runner/util.rs](https://github.com/stellar/rs-soroban-env/blob/0c99950e96128beba3319aa96b116646ce974e69/soroban-env-host/src/cost_runner/util.rs#L22) · line 22 · SHA-256 993641d576de59cd5cd5c46079bf94b0b97dd9b3daf2fa32acbb1a0ac59b3d3e_

```
   21 |                     ScErrorCode::InvalidInput,
   22 |                     "failed secp256r1 verification",
   23 |                     &[],
```

_file_excerpt · [soroban-env-host/src/cost_runner/util.rs](https://github.com/stellar/rs-soroban-env/blob/0c99950e96128beba3319aa96b116646ce974e69/soroban-env-host/src/cost_runner/util.rs#L35) · line 35 · SHA-256 50fcd60c33b696e792d7360322abca7b4a8d38f256054a0598d0e767569d7ccc_

```
   34 |         let recovered_key =
   35 |             p256::ecdsa::VerifyingKey::recover_from_prehash(msg_hash.as_slice(), &sig, rid)
   36 |                 .map_err(|_| {
```

_file_excerpt · [soroban-env-host/src/crypto/mod.rs](https://github.com/stellar/rs-soroban-env/blob/0c99950e96128beba3319aa96b116646ce974e69/soroban-env-host/src/crypto/mod.rs#L102) · line 102 · SHA-256 d93603853957e179e153b1c85f5515848dab1bb4afe578505093e1387081e68a_

```
  101 |         &self,
  102 |         verifying_key: &p256::ecdsa::VerifyingKey,
  103 |         msg_hash: &Hash,
```

_file_excerpt · [soroban-env-host/src/crypto/mod.rs](https://github.com/stellar/rs-soroban-env/blob/0c99950e96128beba3319aa96b116646ce974e69/soroban-env-host/src/crypto/mod.rs#L114) · line 114 · SHA-256 24c43897781920baa5c997781ba7250fbf2159ab9566832351490ca542ebf8a2_

```
  113 |                     ScErrorCode::InvalidInput,
  114 |                     "failed secp256r1 verification",
  115 |                     &[],
```

_file_excerpt · [soroban-env-host/src/crypto/mod.rs](https://github.com/stellar/rs-soroban-env/blob/0c99950e96128beba3319aa96b116646ce974e69/soroban-env-host/src/crypto/mod.rs#L123) · line 123 · SHA-256 fadb54cf6ddd44355e4ad2b67f56ed06be857d0c58fb0c9a5ae4526afc548654_

```
  122 |         bytes: &[u8],
  123 |     ) -> Result<p256::ecdsa::VerifyingKey, HostError> {
  124 |         use sec1::point::Tag;
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it; introduce an abstraction layer for crypto-agility.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-19563 — Quantum-vulnerable Ed25519: authentication and identity (certificates, tokens, device attestation) (1 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:Ed25519:authentication`
- Data source: soroban-test-wasms/wasm-workspace/simple_account/src/lib.rs
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.3.0 · 2026-11-06 16:05 UTC
- Priority score: 34.2 / 100
- CVSS v3.1: not applicable

1 reference(s) to Ed25519 across 1 file(s), e.g. soroban-test-wasms/wasm-workspace/simple_account/src/lib.rs:33. Role, judged from paths, function names and nearby code: authentication and identity (certificates, tokens, device attestation). Short-lived authentication stays safe until a CRQC exists; long-lived identities (device attestation, CA and SSH keys) need a plan earlier.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open soroban-test-wasms/wasm-workspace/simple_account/src/lib.rs:33 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [soroban-test-wasms/wasm-workspace/simple_account/src/lib.rs](https://github.com/stellar/rs-soroban-env/blob/0c99950e96128beba3319aa96b116646ce974e69/soroban-test-wasms/wasm-workspace/simple_account/src/lib.rs#L33) · line 33 · SHA-256 304dbfe7372763418ad046fb11f27c77b2f1ff85af31a304470b3ab55e541259_

```
   32 |         env.crypto()
   33 |             .ed25519_verify(&public_key, &signature_payload.into(), &signature);
   34 |     }
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Keep credentials short-lived and plan ML-DSA certificates, tokens and keys as the ecosystem supports them.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-19569 — serde_with 3.12.0 is affected by GHSA-7gcf-g7xr-8hxj

- Severity: **Medium** · Classification: Known vulnerable component · Confidence: Low
- Affected asset: `dependency:crates.io/serde_with@3.12.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 16:05 UTC
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

### QSI-2026-19574 — serde_with 3.14.0 is affected by GHSA-7gcf-g7xr-8hxj

- Severity: **Medium** · Classification: Known vulnerable component · Confidence: Low
- Affected asset: `dependency:crates.io/serde_with@3.14.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 16:05 UTC
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

### QSI-2026-19570 — time 0.3.41 is affected by GHSA-r6v5-fh4h-64xc (CVE-2026-25727, RUSTSEC-2026-0009)

- Severity: **Medium** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/time@0.3.41`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 16:05 UTC
- Priority score: 28.2 / 100
- CVSS v3.1: not applicable

OSV.dev reports GHSA-r6v5-fh4h-64xc (CVE-2026-25727, RUSTSEC-2026-0009) for crates.io package time at version 0.3.41: time vulnerable to stack exhaustion Denial of Service attack. The audited code does not name the affected functions (time::Date::parse, time::OffsetDateTime::parse, time::PrimitiveDateTime::parse, time::Time::parse, time::UtcDateTime::parse, time::UtcOffset::parse …); time comes in through other dependencies, which may still call them.

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

### QSI-2026-19568 — rand 0.8.5 is affected by GHSA-cq8v-f236-94qc (RUSTSEC-2026-0097)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Medium
- Affected asset: `dependency:crates.io/rand@0.8.5`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 16:05 UTC
- Priority score: 39.2 / 100
- CVSS v3.1: not applicable

OSV.dev reports GHSA-cq8v-f236-94qc (RUSTSEC-2026-0097) for crates.io package rand at version 0.8.5: Rand is unsound with a custom logger using rand::rng(). The audited code names rand::rng: the affected code may be reachable.

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

### QSI-2026-19571 — tracing-subscriber 0.3.18 is affected by GHSA-xwfj-jgwm-7wp5 (CVE-2025-58160, RUSTSEC-2025-0055)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low
- Affected asset: `dependency:crates.io/tracing-subscriber@0.3.18`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 16:05 UTC
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

### QSI-2026-19566 — keccak 0.1.4 is affected by GHSA-3288-p39f-rqpv (RUSTSEC-2026-0012)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/keccak@0.1.4`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 16:05 UTC
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

### QSI-2026-19564 — crypto-bigint 0.5.2 is affected by RUSTSEC-2026-0387 (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/crypto-bigint@0.5.2`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 16:05 UTC
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

### QSI-2026-19565 — ctutils 0.4.2 is affected by RUSTSEC-2026-0385 (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/ctutils@0.4.2`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 16:05 UTC
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

### QSI-2026-19572 — crypto-bigint 0.5.4 is affected by RUSTSEC-2026-0387 (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:crates.io/crypto-bigint@0.5.4`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 16:05 UTC
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

### QSI-2026-19567 — paste 1.0.12: informational advisory RUSTSEC-2024-0436 (unmaintained)

- Severity: **Info** · Classification: Improvement recommendation · Confidence: Low
- Affected asset: `dependency:crates.io/paste@1.0.12`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 16:05 UTC
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

### QSI-2026-19573 — paste 1.0.14: informational advisory RUSTSEC-2024-0436 (unmaintained)

- Severity: **Info** · Classification: Improvement recommendation · Confidence: Low
- Affected asset: `dependency:crates.io/paste@1.0.14`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.3.0 · 2026-11-06 16:05 UTC
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

### Post-quantum maturity: Level 2 of 4 — post-quantum in use outside the critical paths

- In use: ML-DSA — soroban-env-host/src/cost_runner/cost_types/mod.rs
- In use: ML-DSA — soroban-env-host/src/host.rs
- Present, not wired: ML-DSA — soroban-env-host/src/cost_runner/cost_types/ml_dsa.rs
- Present, not wired: ML-DSA — soroban-env-host/src/crypto/ml_dsa.rs
- A post-quantum library is declared as a dependency

**Next step:** Extend post-quantum protection to the critical roles that stay classical, starting with what can be recorded today (wrapped keys, channel key exchange).

_Levels: 0 none; 1 present, not wired; 2 in use outside the critical paths; 3 hybrid in a critical path; 4 post-quantum by default in the critical paths (root of trust, key wrapping, channel key exchange). Judged from code and manifests._

### What the quantum-vulnerable algorithms do

| Role | Algorithms (files) | ID | First step |
|---|---|---|---|
| **transaction and message signing** | ECDSA (2), Ed25519 (2) | QSI-2026-19557, QSI-2026-19561 | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains adopt them |
| **authentication and identity (certificates, tokens, device attestation)** | Ed25519 (1) | QSI-2026-19563 | Keep credentials short-lived and plan ML-DSA certificates, tokens and keys as the ecosystem supports them |
| **role not determined** | Ed25519 (9), ECDSA (6), BLS12-381 (5), BN254 (alt_bn128) (2) | QSI-2026-19558, QSI-2026-19559, QSI-2026-19560, QSI-2026-19562 | Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it; introduce an abstraction layer for crypto-agility |

_Roles are judged from file paths, function names and the code around each match; review confirms them. Root-of-trust keys and wrapped keys come first: they are hard to replace or can be recorded today._
No readiness questionnaire was completed for this project.

### Quantum algorithms relevant to this inventory

| Quantum algorithm | Effect | Attack model | Inventoried algorithms (rows) | What it means for this audit |
|---|---|---|---|---|
| Shor's algorithm — discrete logarithms in finite fields | breaks | Q1 | BLS12-381 (7), BN254 (alt_bn128) (2) | Breaks finite-field Diffie–Hellman and DSA at every size. Move key establishment to ML-KEM (hybrid with X25519 or ECDH during the transition) and signatures to ML-DSA or SLH-DSA. |
| Shor's algorithm — elliptic-curve discrete logarithms | breaks | Q1 | BLS12-381 (7), BN254 (alt_bn128) (2), ECDSA (16), Ed25519 (13) | Elliptic-curve keys are expected to fall before RSA keys of comparable classical strength. On blockchains, coins whose public key is already on chain (reused addresses, pay-to-public-key and Taproot outputs) are exposed first; plan the move to post-quantum signatures and avoid key reuse in the meantime. |
| Grover's algorithm — key search and preimages | weakens (larger keys restore the margin) | Q1 | HMAC (1), Keccak-256 (2), Poseidon (8), SHA-2 (5) | Not a break. 256-bit keys (AES-256, ChaCha20) keep a comfortable margin; AES-128 meets NIST category 1, while some authorities ask for 256-bit keys in quantum-resistant contexts (see the AES-128 entry). Prefer 256-bit keys for long-lived data; 256-bit hashes need no change for preimage resistance. |
| Brassard–Høyer–Tapp — collision search | weakens (larger keys restore the margin) | Q1 | Keccak-256 (2), Poseidon (8), SHA-2 (5) | 256-bit hashes (SHA-256, SHA3-256) remain adequate for collision resistance; 160-bit hashes are already weak classically (SHA-1 collisions are practical). Use 384/512-bit hashes where NIST categories 4–5 are required. |
| Quantum lattice sieving | included in standard parameters | Q1 | ML-DSA (4) | No change for ML-KEM or ML-DSA at the standard parameter sets. A 2024 claim of a polynomial-time quantum LWE algorithm was withdrawn after a bug was found (see claims). |

_Effects: breaks — replace the algorithm; weakens — larger keys or outputs restore the margin; included in standard parameters — no action at standard parameter sets; only with superposition queries — not applicable to ordinary deployments._


## 9. Limitations and assumptions

- This report presents automated and documented analysis results for the stated scope. It is not a legal opinion, a certification or an attestation of compliance with any standard.
- z is a planning assumption chosen per risk profile, not a prediction. A cryptographically relevant quantum computer is not publicly known to exist today.
- osv_advisories: 3 package(s) are built from git repositories (forks or unreleased code), so registry advisories were not looked up for them: soroban-wasmi, wasmi_arena, wasmi_core

## 10. Remediation plan / Priorities for 30, 60 and 90 days

### 30 days

| Priority | ID | Action | Type | Closure criteria |
|---|---|---|---|---|
| P2 | QSI-2026-19569 | Upgrade serde_with to a fixed version (3.21.0). | root-cause fix | Dependency scan no longer reports GHSA-7gcf-g7xr-8hxj. |
| P2 | QSI-2026-19574 | Upgrade serde_with to a fixed version (3.21.0). | root-cause fix | Dependency scan no longer reports GHSA-7gcf-g7xr-8hxj. |
| P2 | QSI-2026-19570 | Upgrade time to a fixed version (0.3.47). | root-cause fix | Dependency scan no longer reports GHSA-r6v5-fh4h-64xc (CVE-2026-25727, RUSTSEC-2026-0009). |
| P2 | QSI-2026-19568 | Upgrade rand to a fixed version (0.10.1, 0.8.6, 0.9.3). | root-cause fix | Dependency scan no longer reports GHSA-cq8v-f236-94qc (RUSTSEC-2026-0097). |
| P2 | QSI-2026-19571 | Upgrade tracing-subscriber to a fixed version (0.3.20). | root-cause fix | Dependency scan no longer reports GHSA-xwfj-jgwm-7wp5 (CVE-2025-58160, RUSTSEC-2025-0055). |
| P2 | QSI-2026-19566 | Upgrade keccak to a fixed version (0.1.6). | root-cause fix | Dependency scan no longer reports GHSA-3288-p39f-rqpv (RUSTSEC-2026-0012). |
### 60 days

| Priority | ID | Action | Type | Closure criteria |
|---|---|---|---|---|
| P3 | QSI-2026-19564 | Triage RUSTSEC-2026-0387; upgrade crypto-bigint to a fixed version (0.7.6) if it applies. | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0387, or the triage is recorded. |
| P3 | QSI-2026-19565 | Triage RUSTSEC-2026-0385; upgrade ctutils to a fixed version (0.4.4) if it applies. | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0385, or the triage is recorded. |
| P3 | QSI-2026-19572 | Triage RUSTSEC-2026-0387; upgrade crypto-bigint to a fixed version (0.7.6) if it applies. | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0387, or the triage is recorded. |
### 90 days

| Priority | ID | Action | Type | Closure criteria |
|---|---|---|---|---|
| P3 | QSI-2026-19557 | Add Ed25519 usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-19561 | Add ECDSA usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-19558 | Add Ed25519 usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-19559 | Add BLS12-381 usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-19560 | Add BN254 (alt_bn128) usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-19562 | Add ECDSA usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-19563 | Add Ed25519 usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P4 | QSI-2026-19557 | Plan migration of Ed25519 to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-19561 | Plan migration of ECDSA to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-19558 | Plan migration of Ed25519 to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-19559 | Plan migration of BLS12-381 to  (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows  or a hybrid scheme in use. |
| P4 | QSI-2026-19560 | Plan migration of BN254 (alt_bn128) to  (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows  or a hybrid scheme in use. |
| P4 | QSI-2026-19562 | Plan migration of ECDSA to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-19563 | Plan migration of Ed25519 to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-19567 | Replace paste with a maintained alternative or record why it stays. | root-cause fix | paste replaced, or the decision recorded. |
| P4 | QSI-2026-19573 | Replace paste with a maintained alternative or record why it stays. | root-cause fix | paste replaced, or the decision recorded. |

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
15. J. Proos, C. Zalka — Shor's discrete logarithm quantum algorithm for elliptic curves (Quantum Inf. Comput. 3(4), 2003; arXiv:quant-ph/0301141) — Quantum Information & Computation. <https://doi.org/10.26421/QIC3.4-3> (peer-reviewed article)
16. L. K. Grover — A fast quantum mechanical algorithm for database search (STOC 1996) — ACM. <https://doi.org/10.1145/237814.237866> (peer-reviewed article)
17. M. Amy et al. — Estimating the cost of generic quantum pre-image attacks on SHA-2 and SHA-3 (SAC 2016; arXiv:1603.09383) — Springer / arXiv. <https://arxiv.org/abs/1603.09383> (peer-reviewed article: SHA-256 about 2^153.8 surface-code cycles on 2^12.6 logical qubits; SHA3-256 about 2^146.5 cycles on 2^20)
18. M. Cain et al. — Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits (arXiv:2603.28627) — arXiv. <https://arxiv.org/abs/2603.28627> (preprint (2026-03-30): P-256 in a few days with 26,000 physical neutral-atom qubits; RSA-2048 one to two orders of magnitude longer)
19. M. Ekerå, J. Gärtner — A high-level comparison of state-of-the-art quantum algorithms for breaking asymmetric cryptography (arXiv:2405.14381) — arXiv. <https://arxiv.org/abs/2405.14381> (preprint (2024-05-23): Regev-style algorithms show no overall advantage yet for cryptographic RSA and finite-field sizes)
20. M. Mosca — Cybersecurity in an Era with Quantum Computers: Will We Be Ready? (IEEE Security & Privacy, 2018) — IEEE. <https://doi.org/10.1109/MSP.2018.3761723> (peer-reviewed article; source of the x + y > z migration inequality)
21. M. Roetteler, M. Naehrig, K. Svore, K. Lauter — Quantum resource estimates for computing elliptic curve discrete logarithms (ASIACRYPT 2017) — IACR / arXiv. <https://arxiv.org/abs/1706.06752> (peer-reviewed article: at most 9n + 2⌈log2 n⌉ + 10 qubits and 448 n^3 log2 n + 4090 n^3 Toffoli gates)
22. NIST IR 8547 — Transition to Post-Quantum Cryptography Standards — NIST. <https://csrc.nist.gov/pubs/ir/8547/final> (final (2026-10-27; the initial public draft of November 2024 is obsoleted). Tables 2 and 4: ECDSA, EdDSA and RSA signatures, finite-field and elliptic-curve DH and MQV, and RSA key establishment are deprecated after 2030 and disallowed after 2035 at every key size — the draft deprecated only the 112-bit level. A composite (hybrid) key establishment stays FIPS 140-validatable while one input comes from an approved scheme. Repeats the federal deadlines of OMB M-26-15: post-quantum key establishment by 2030-12-31 and signatures by 2031-12-31 for high value assets and high impact systems)
23. NIST — Post-Quantum Cryptography Standardization: Evaluation Criteria, Security (Call for Proposals, Section 4.A.5) — NIST. <https://csrc.nist.gov/Projects/Post-Quantum-Cryptography/Post-Quantum-Cryptography-Standardization/Evaluation-Criteria/Security-(Evaluation-Criteria)> (security categories: AES-128 key search 2^170/MAXDEPTH quantum gates, AES-192 2^233/MAXDEPTH, AES-256 2^298/MAXDEPTH; MAXDEPTH 2^40–2^96)
24. OSV advisory GHSA-3288-p39f-rqpv — OSV.dev. <https://osv.dev/vulnerability/GHSA-3288-p39f-rqpv> (modified 2026-09-10T03:50:59.332505686Z)
25. OSV advisory GHSA-7gcf-g7xr-8hxj — OSV.dev. <https://osv.dev/vulnerability/GHSA-7gcf-g7xr-8hxj> (modified 2026-09-10T03:51:10.897685062Z)
26. OSV advisory GHSA-cq8v-f236-94qc — OSV.dev. <https://osv.dev/vulnerability/GHSA-cq8v-f236-94qc> (modified 2026-09-10T03:50:43.958966498Z)
27. OSV advisory GHSA-r6v5-fh4h-64xc — OSV.dev. <https://osv.dev/vulnerability/GHSA-r6v5-fh4h-64xc> (modified 2026-09-10T03:50:35.583241382Z)
28. OSV advisory GHSA-xwfj-jgwm-7wp5 — OSV.dev. <https://osv.dev/vulnerability/GHSA-xwfj-jgwm-7wp5> (modified 2026-09-10T03:50:27.766863705Z)
29. OSV advisory RUSTSEC-2024-0436 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2024-0436> (modified 2026-01-27T22:03:15.694766Z)
30. OSV advisory RUSTSEC-2026-0385 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0385> (modified 2026-10-23T08:30:02.389575143Z)
31. OSV advisory RUSTSEC-2026-0387 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0387> (modified 2026-10-24T03:45:02.365137418Z)
32. P. W. Shor — Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms on a Quantum Computer (SIAM J. Comput., 1997) — SIAM. <https://doi.org/10.1137/S0097539795293172> (peer-reviewed article)
33. R. Babbush et al. — Securing Elliptic Curve Cryptocurrencies against Quantum Vulnerabilities: Resource Estimates and Mitigations (arXiv:2603.28846) — arXiv. <https://arxiv.org/abs/2603.28846> (preprint (2026-03-30, v2 2026-04-15): 256-bit ECDLP with < 1200 logical qubits and < 90 M Toffoli gates (or < 1450 and < 70 M); < 500,000 physical qubits at 10^-3 error, minutes)
34. S. Jaques, M. Naehrig, M. Roetteler, F. Virdia — Implementing Grover oracles for quantum key search on AES and LowMC (EUROCRYPT 2020; arXiv:1910.01700) — Springer / arXiv. <https://arxiv.org/abs/1910.01700> (peer-reviewed article: lower cost estimates for the AES key searches that define the NIST categories)

## Appendices: Cryptographic inventory

By origin: dependency manifests 18 (0 Shor-breakable) · own code 58 (38 Shor-breakable).

| Algorithm | Parameter | Library | Quantum status | Classical status | Count | Locations | Examples |
|---|---|---|---|---|---|---|---|
| HMAC |  |  | reduced margin (Grover), approved | acceptable | 1 | 1 | soroban-env-host/src/crypto/mod.rs:14 |
| Keccak-256 | Keccak-256 |  | Grover: acceptable to NIST, below ECCG/ANSSI guidance | acceptable | 2 | 2 | soroban-env-host/src/cost_runner/cost_types/compute_keccak256_hash.rs; soroban-env-host/src/crypto/mod.rs:18 |
| Poseidon |  |  | Grover: acceptable to NIST, below ECCG/ANSSI guidance | acceptable | 8 | 8 | soroban-env-host/src/crypto/mod.rs:5; soroban-env-host/src/crypto/poseidon/mod.rs:6; soroban-env-host/src/crypto/poseidon/poseidon.rs:4 |
| SHA-2 | SHA-256 |  | Grover: acceptable to NIST, below ECCG/ANSSI guidance | acceptable | 5 | 5 | soroban-env-host/src/cost_runner/cost_types/compute_sha256_hash.rs; soroban-env-host/src/crypto/bls12_381.rs:27; soroban-env-host/src/crypto/mod.rs:17 |
| Crypto library | 0.13.2 | p256 (RustCrypto elliptic curves) | n/a | acceptable | 3 | 3 | Cargo.lock; soroban-env-host/Cargo.toml; soroban-test-wasms/wasm-workspace/Cargo.lock |
| Crypto library | 0.13.4 | k256 (RustCrypto elliptic curves) | n/a | acceptable | 2 | 2 | Cargo.lock; soroban-test-wasms/wasm-workspace/Cargo.lock |
| Crypto library | 0.16.9 | ecdsa (python-ecdsa) | n/a | acceptable | 2 | 2 | Cargo.lock; soroban-test-wasms/wasm-workspace/Cargo.lock |
| Crypto library | 2.1.1 | ed25519-dalek (ed25519-dalek) | n/a | acceptable | 1 | 1 | Cargo.lock |
| Crypto library | 4.1.3 | curve25519-dalek (ed25519-dalek) | n/a | acceptable | 2 | 2 | Cargo.lock; soroban-test-wasms/wasm-workspace/Cargo.lock |
| Crypto library | 0.13.1 | k256 (RustCrypto elliptic curves) | n/a | acceptable | 1 | 1 | soroban-env-host/Cargo.toml |
| Crypto library | 0.13.3 | k256 (RustCrypto elliptic curves) | n/a | acceptable | 1 | 1 | soroban-env-host/Cargo.toml |
| Crypto library | 0.16.7 | ecdsa (python-ecdsa) | n/a | acceptable | 1 | 1 | soroban-env-host/Cargo.toml |
| Crypto library | 2.0.0 | ed25519-dalek (ed25519-dalek) | n/a | acceptable | 2 | 2 | soroban-env-host/Cargo.toml; soroban-test-wasms/wasm-workspace/Cargo.lock |
| Crypto library | >=4.1.3 | curve25519-dalek (ed25519-dalek) | n/a | acceptable | 1 | 1 | soroban-env-host/Cargo.toml |
| ML-DSA |  |  | post-quantum | acceptable | 4 | 4 | soroban-env-host/src/cost_runner/cost_types/ml_dsa.rs:9; soroban-env-host/src/cost_runner/cost_types/mod.rs:34; soroban-env-host/src/crypto/ml_dsa.rs:21 |
| PQC library | 0.1.1 | ml-dsa (RustCrypto post-quantum crates) | post-quantum | acceptable | 2 | 2 | Cargo.lock; soroban-env-host/Cargo.toml |
| BLS12-381 |  |  | vulnerable (Shor) | acceptable | 7 | 7 | soroban-env-host/src/cost_runner/cost_types/bls12_381.rs:6; soroban-env-host/src/cost_runner/cost_types/mod.rs:1; soroban-env-host/src/cost_runner/experimental/bls12_381.rs |
| BN254 (alt_bn128) |  |  | vulnerable (Shor) | acceptable | 2 | 2 | soroban-env-host/src/cost_runner/cost_types/bn254.rs:1; soroban-env-host/src/crypto/bn254.rs:4 |
| ECDSA |  |  | vulnerable (Shor) | acceptable | 6 | 6 | soroban-env-host/src/cost_runner/cost_types/decode_ecdsa_curve256_sig.rs; soroban-env-host/src/cost_runner/cost_types/sec1_decode_point_uncompressed.rs:5; soroban-env-host/src/cost_runner/experimental/ecdsa_secp256r1_recover.rs:7 |
| ECDSA | secp256k1 |  | vulnerable (Shor) | acceptable | 4 | 4 | soroban-env-host/src/cost_runner/cost_types/recover_ecdsa_secp256k1_key.rs:7; soroban-env-host/src/cost_runner/experimental/ecdsa_secp256k1_verify.rs:6; soroban-env-host/src/cost_runner/util.rs:12 |
| ECDSA | P-256 |  | vulnerable (Shor) | acceptable | 6 | 6 | soroban-env-host/src/cost_runner/cost_types/sec1_decode_point_uncompressed.rs:5; soroban-env-host/src/cost_runner/cost_types/verify_ecdsa_secp256r1_sig.rs:5; soroban-env-host/src/cost_runner/experimental/ecdsa_secp256r1_recover.rs:7 |
| Ed25519 | Ed25519 |  | vulnerable (Shor) | acceptable | 13 | 13 | soroban-env-host/src/builtin_contracts/stellar_asset_contract/metadata.rs:158; soroban-env-host/src/builtin_contracts/testutils.rs:7; soroban-env-host/src/cost_runner/cost_types/compute_ed25519_pubkey.rs:3 |

_Long lists are grouped here; the full per-file list is in the JSON report, signed with the same key._

## Appendices: Input files

| File | Size | SHA-256 | Redactions |
|---|---|---|---|
| .cargo/config.toml | 6685 | `deaae172a164fb2ba5bfa0e6b3658fc8ef043a348c861936762a8a210c213ca0` | 0 |
| Cargo.lock | 66997 | `8004e3b6495cf7791937bff1131e216c8998def149562f66e2cf431ed99d3995` | 0 |
| Cargo.toml | 1714 | `d24c948dc1b2ed4c0bd856c41493867d866a4b4965b640ad6315db9716347152` | 0 |
| rust-toolchain.toml | 369 | `a93034bc4702710436624ddc42e89325be59ebc8e584e7c58b9b6c00fc2d3b2d` | 0 |
| soroban-bench-utils/Cargo.toml | 787 | `2020e9795c6dc4edfee39f36f1d78cf16b954f69ac16f9cba453485985d4edd3` | 0 |
| soroban-bench-utils/src/lib.rs | 75 | `4ed9af88c90c8137a175e9b2e583a3076ef13bc4911e133e889aa6f559caeeab` | 0 |
| soroban-bench-utils/src/rusagev4.rs | 2027 | `e775f766b27fcece33febfaf91e1b2e46b4ff0d7028a326909fd910dd75c7b17` | 0 |
| soroban-bench-utils/src/tracker.rs | 5923 | `71df7e2a505682276058fba51644bfe0f0d59934c327b9f4bb14ee6d59a6f8b4` | 0 |
| soroban-builtin-sdk-macros/Cargo.toml | 554 | `e2e52a67795c6540896ee63bfaf72c0b52ad318e78ca7028a1b02e961d8ff063` | 0 |
| soroban-builtin-sdk-macros/src/derive_fn.rs | 2815 | `627430878da696e94b872adc29d71390e866277ee7acf6c1b42e7cdd2ccf15a0` | 0 |
| soroban-builtin-sdk-macros/src/derive_type.rs | 8525 | `459416267127d646b9d105c16c046b210eeb22cd4c482511f268d8396120f215` | 0 |
| soroban-builtin-sdk-macros/src/lib.rs | 1734 | `7120a6c227f456234536bfef7c7f9d82918a8c89d8c25f3f16eaccc404a79aad` | 0 |
| soroban-env-common/Cargo.toml | 1521 | `07a820c9c891a409cbe763dfbdb2321d0103fa844ffc2bdefaffaed275a7f2be` | 0 |
| soroban-env-common/build.rs | 99 | `818b5844721186dd913412974faaff4bb45954e41b2cedeecb4b0a5ddcf90b35` | 0 |
| soroban-env-common/src/arbitrary.rs | 2047 | `aaebd099ab97097e1ac2482ac4c437c99736f75ca822cfdcec435ccf8b8fb662` | 0 |
| soroban-env-common/src/bytes.rs | 3066 | `768838872830e2352670e97ad9d9313c24db0efb8854847474739ed33c7c5735` | 0 |
| soroban-env-common/src/compare.rs | 7518 | `a61b9a80f87ee4b47ec8fb731fe2352ab4152941de87c0c3a4d4d032fa2f155e` | 0 |
| soroban-env-common/src/convert.rs | 19786 | `0ec5cb77ee4849bd270ce7ad629c793e921246f7f26e9c5d12bc6f412214b5ab` | 0 |
| soroban-env-common/src/env.rs | 18735 | `d2b81cd30de3099dc714503c6d87904b38d76e5da23a70c33dc9a36e9ead3150` | 0 |
| soroban-env-common/src/error.rs | 15600 | `efd9f516f411d55dd01a22e33f3418068d82c715290382e98a5cba4f58bdc46e` | 0 |
| soroban-env-common/src/hash.rs | 1501 | `15c9e63948d9ce9486581659f1aea95a08eb849416500a0a096f8d9d11ec1350` | 0 |
| soroban-env-common/src/lib.rs | 4018 | `57665754a7a74c76b2f6c90a6f846e45d917eec2b48427f7c606fb8049cf74d2` | 0 |
| soroban-env-common/src/meta.rs | 3279 | `4cd2287db41b82d68928def2b71ad815c1cf3e3ea5efafe8e4f02b9392001c31` | 0 |
| soroban-env-common/src/num.rs | 14398 | `9242b8a3eeb918cbc602ecbb6e185b3d8bc6cacf27bb50d35c7aad767de5ff0c` | 0 |
| soroban-env-common/src/object.rs | 6008 | `8241f6640f0fb0f0fa875fce49490d0fe8247c682a6eeee37391f2d93a4ec8a7` | 0 |
| soroban-env-common/src/option.rs | 907 | `870a61869cabc46e32f50c93605686f4d66f1952bf89f596b8fbfdcaf5deb38e` | 0 |
| soroban-env-common/src/result.rs | 1261 | `d3210db790113cf7950e76c15492358ca9a469159f8dee2c27c2dee91228c4b0` | 0 |
| soroban-env-common/src/storage_type.rs | 1474 | `056d61661c117c628f61dbc1307aa76a72254c69be680d9508f9e5598a977bc0` | 0 |
| soroban-env-common/src/string.rs | 2036 | `13ec3079a2f66e4affb3ecdeba15134f2941ef05076f544a195736dbd64bf8e9` | 0 |
| soroban-env-common/src/symbol.rs | 21593 | `8c11e956065de27f8d67d55eab1fdfacc515d31c57c3e8e30baa5d905d30d68d` | 0 |
| soroban-env-common/src/tuple.rs | 4295 | `fed0d299699f9ad2f429f68199534af4b319cfbc960dfdf488e9dc943fae95ad` | 0 |
| soroban-env-common/src/val.rs | 31320 | `c236111a028b7dcde91dfc1e816ed22f5eabe94b95499d03fccf089a73b6ef8e` | 0 |
| soroban-env-common/src/vmcaller_env.rs | 11627 | `ea4fba3d54f89bdaacb93ba6132955f6b9fb4d78e4d07890adee5cdb6f6da1d8` | 0 |
| soroban-env-common/src/wrapper_macros.rs | 12097 | `0228b5e35382d4dbca4b760f3f6a57d0a7ecbb9ffa897f16d445c82ce6e63e93` | 0 |
| soroban-env-guest/Cargo.toml | 625 | `65d7195e1ef69e1cba7c6aabd96072fe37482f0b1c7ecaeb17e17cc38b2ab937` | 0 |
| soroban-env-guest/src/guest.rs | 16376 | `d837794209e6f0cd20b4ee4de10dd2019417577fab6c6f4866da0397a6add69b` | 0 |
| soroban-env-guest/src/lib.rs | 561 | `b34cdc92dbf3880bd463d0c82b7df5866ac88d74b8bc42d8a9321eb9104dcfdf` | 0 |
| soroban-env-host/Cargo.toml | 5123 | `10866901b8a2f16b1876dd7e80ac5cb1c3b08339c6883f76a83c5cfa72a39e87` | 0 |
| soroban-env-host/build.rs | 283 | `f90c468c4ab2735a8edeca9f82ca31cf327a27fd8baf47f7417dab8653151005` | 0 |
| soroban-env-host/src/auth.rs | 129016 | `8307d3aeaf9c1a7c8199d2107714aff9c298ae299475ec4470ad28ead446e91b` | 0 |
| soroban-env-host/src/bin/main.rs | 1615 | `499367447384bdebd2654a72fe3f3f916e523762b2442e1b8417ea7d98d49e9f` | 0 |
| soroban-env-host/src/budget.rs | 64867 | `2ce3d7ba5c0c1ad1593a4e76c2ab1b7d88d5aede0501e875dd99902f8346fe80` | 0 |
| soroban-env-host/src/budget/dimension.rs | 8056 | `14d8a99a08a0844636e62d66a77e15d9a215929a65bc062777730f88ce532bfe` | 0 |
| soroban-env-host/src/budget/limits.rs | 4658 | `0080964f53ec49d2df64306354887cc5565b2628584e64548126a4b95e2eca1e` | 0 |
| soroban-env-host/src/budget/model.rs | 5668 | `70c47d818a27c286180e758280590839971b0cb071f227d33f96f2e935bcc3c7` | 0 |
| soroban-env-host/src/budget/util.rs | 7351 | `2e16740c47331fe2c88aad6bf3f80ede095f0259e5517cf3ff848a242495a6f9` | 0 |
| soroban-env-host/src/budget/wasmi_helper.rs | 5257 | `72c4869ce8a190b7afb82091692330700c6f43ba984164815d95ca3c1d62b6b3` | 0 |
| soroban-env-host/src/builtin_contracts.rs | 560 | `f0bd26290068aff0d567b8e950c3abd9545b9f6fbb50a521001e21f9b3a7ed1e` | 0 |
| soroban-env-host/src/builtin_contracts/account_contract.rs | 9242 | `7af518b93ec3124d9b38a67a8272e73a7f5af6a5f495e612d08fec87416aad3c` | 0 |
| soroban-env-host/src/builtin_contracts/base_types.rs | 14101 | `a66d54af8360d2c950f469f7aceb2a5ebb805e716b94b687dc15f366c0900f7d` | 0 |
| soroban-env-host/src/builtin_contracts/common_types.rs | 3474 | `e70a1ef6507838259fba577aefb9add282e7fe108ea4c98fa79d4b4af50f7348` | 0 |
| soroban-env-host/src/builtin_contracts/contract_error.rs | 1099 | `f763a1979d169c8df77ece0426b40a29686435b9b5da466243de60fd005761db` | 0 |
| soroban-env-host/src/builtin_contracts/invoker_contract_auth.rs | 6122 | `f3ae7c92ba3f2e9b80cfee73b1b6eba1b3edffbf2c7d92ee1ec649f618617690` | 0 |
| soroban-env-host/src/builtin_contracts/stellar_asset_contract.rs | 248 | `944142447b113d671f1e47dc8a2d8191ef4ff11167b793f2a4c2f4d72efc8e4f` | 0 |
| soroban-env-host/src/builtin_contracts/stellar_asset_contract/admin.rs | 704 | `ad70748dab976704bdf5fa87dfe30c0746280a24eb46c36a9c102aeb1f11980d` | 0 |
| soroban-env-host/src/builtin_contracts/stellar_asset_contract/allowance.rs | 5164 | `9bb65ada40aa4430359eb27a7e77aed2d90d7d7316e48b99dda71540eecb2fe3` | 0 |
| soroban-env-host/src/builtin_contracts/stellar_asset_contract/asset_info.rs | 3092 | `9a0583a6bec016f2822bc357baa2cce81c8e4ad3077fd8d5e2100172c0b22def` | 0 |
| soroban-env-host/src/builtin_contracts/stellar_asset_contract/balance.rs | 39345 | `671ea7ffb78b3c59b97ce417fac9cb5b4a6c8af5a592d8d51bd0b8a344108d29` | 0 |
| soroban-env-host/src/builtin_contracts/stellar_asset_contract/contract.rs | 14110 | `5fe6f53f7da37861501ae6e6205907f3473679a8cabe1eca61759d50210e997a` | 0 |
| soroban-env-host/src/builtin_contracts/stellar_asset_contract/event.rs | 4403 | `125cc56ff663883f629520b9ea1fc1978527c61b86867063cd57cba7730b211c` | 0 |
| soroban-env-host/src/builtin_contracts/stellar_asset_contract/metadata.rs | 6992 | `12ca5219bd19e98b81880a01e5fe99bfffaf1c5d283371bff34961763ac00331` | 0 |
| soroban-env-host/src/builtin_contracts/stellar_asset_contract/public_types.rs | 1318 | `84834c2fec3c9763ba73d89fdd44db86da9a35400e82401cd5ba04ed03874026` | 0 |
| soroban-env-host/src/builtin_contracts/stellar_asset_contract/storage_types.rs | 1113 | `655a0cec594b78db2eeccabfe03e27f2ae0537c65729e456b604cbbdb579f298` | 0 |
| soroban-env-host/src/builtin_contracts/storage_utils.rs | 362 | `216d16572291ac021fd3ee7a0ce6d4b1810f8dbee07fc2791bbf32236a75ed10` | 0 |
| soroban-env-host/src/builtin_contracts/testutils.rs | 14105 | `59edd2300fad57079e61b23aab7a44bcd62b22fcf16b525fbf7e01596e57c460` | 0 |
| soroban-env-host/src/cost_runner/cost_types/bls12_381.rs | 10204 | `965dff98b1d17f2c58dd07697781db1c8033193651fb14d4473b091fb6ab43c4` | 0 |
| soroban-env-host/src/cost_runner/cost_types/bn254.rs | 6857 | `b77f33938ce6e3aab58c9ce36abbe2d5ffe5f11643557264de93e493647711e1` | 0 |
| soroban-env-host/src/cost_runner/cost_types/compute_ed25519_pubkey.rs | 952 | `c679365a8825299630452cf28daf21f4e6cff1805ca06910bc4ce49300d04a7c` | 0 |
| soroban-env-host/src/cost_runner/cost_types/compute_keccak256_hash.rs | 916 | `c70f481dcea5eba30a4ae54ea476efec3fb3bf938d15987042aaeac222bbef3d` | 0 |
| soroban-env-host/src/cost_runner/cost_types/compute_sha256_hash.rs | 896 | `99eece10c8e2379a0d3675f618b6c9192a57ddd98bc0063cc886ab22d526b509` | 0 |
| soroban-env-host/src/cost_runner/cost_types/decode_ecdsa_curve256_sig.rs | 1407 | `6eae776ff6b8ee070b6d51f70a4b231bf78c2bd0e964c0cae695be06a66b251e` | 0 |
| soroban-env-host/src/cost_runner/cost_types/host_mem_alloc.rs | 951 | `53bd536e402308f09e0ead2a7825d8a7a88c6da46f0deb55ddce336d6a754a32` | 0 |
| soroban-env-host/src/cost_runner/cost_types/host_mem_cmp.rs | 957 | `db2b390ce0892f2b450a9707d8f3d54a9fe2438d88f73ae021263dc18b266a3c` | 0 |
| soroban-env-host/src/cost_runner/cost_types/host_mem_cpy.rs | 821 | `7ab8627489d5882ca2725d3e5872dc5cf3907890341065e5fa9149b121f11316` | 0 |
| soroban-env-host/src/cost_runner/cost_types/invoke.rs | 2183 | `451a7818021ac77658771411708fe709c328f8d29abb0906720cd4da4fbb069d` | 0 |
| soroban-env-host/src/cost_runner/cost_types/ml_dsa.rs | 5640 | `9b22af01136e5ea270aa291e845b33189d96bf106f893528a293e677cb9d9fc6` | 0 |
| soroban-env-host/src/cost_runner/cost_types/mod.rs | 1043 | `fd0538987c9bb5d51e38e84665ae18e2093e3b868f0f3d90efec7de08c2388f2` | 0 |
| soroban-env-host/src/cost_runner/cost_types/num_ops.rs | 1546 | `cf08647785a4ede49183258e305e4520b3db286536bf2a6e71583e76c89be32b` | 0 |
| soroban-env-host/src/cost_runner/cost_types/prng.rs | 1003 | `fac74f446f916302d6b27d59040ae6c72aa4decbfe766a862f9b0a2dceb75223` | 0 |
| soroban-env-host/src/cost_runner/cost_types/recover_ecdsa_secp256k1_key.rs | 1140 | `21256191032a43cd2584275eebae7e034db553ee6c90c16d6ba5e5e2392eb69a` | 0 |
| soroban-env-host/src/cost_runner/cost_types/sec1_decode_point_uncompressed.rs | 1155 | `06fda4cc5f09ca513953f45424b1aa5277fb1fa0805e598e63466ea6b45d1863` | 0 |
| soroban-env-host/src/cost_runner/cost_types/val_deser.rs | 800 | `19b4abd59908d36bc2c1a2d7e05fc67db21df215cf02bcf91ff42d760f18e6d0` | 0 |
| soroban-env-host/src/cost_runner/cost_types/val_ser.rs | 1385 | `2b3aa6b23feb1d99fdfc267146458eba577e8641124c8673a606fa0cb976b08e` | 0 |
| soroban-env-host/src/cost_runner/cost_types/verify_ecdsa_secp256r1_sig.rs | 1124 | `8b1e249924c8f329e563122f8e2c1d0e60fbc6c788de70c0dd4e9aeaf8f8b833` | 0 |
| soroban-env-host/src/cost_runner/cost_types/verify_ed25519_sig.rs | 1079 | `da86df368d3cdc769f57e48a6fd160ba5c7f1dab0a44876587875be1167215bc` | 0 |
| soroban-env-host/src/cost_runner/cost_types/visit_object.rs | 1056 | `c66e1ae7580a923564f8694f34d3ee9ff4c3de2b768529cf75a9f86e23c9c656` | 0 |
| soroban-env-host/src/cost_runner/cost_types/vm_ops.rs | 8989 | `3a7c74abaa9d8e628d3bc586d8b3056218a8a234bd8e4f35857e186cb4fcc135` | 0 |
| soroban-env-host/src/cost_runner/cost_types/wasm_insn_exec.rs | 9902 | `2c3bfc08db067c5d0320dfbbb55d477019e282d7c7a4d4c6c1c704b47a6b2983` | 0 |
| soroban-env-host/src/cost_runner/experimental/bls12_381.rs | 6378 | `154aed6d61b073065304ff1b68dd8eb3709a82108a7983d23a44cb01cb744ac1` | 0 |
| soroban-env-host/src/cost_runner/experimental/decode_secp256r1_sig.rs | 1472 | `2f7bf5f395b05ad7ae9ab37e404eae4c3bfa85d29eaa8d08becfcfef825b0a1e` | 0 |
| soroban-env-host/src/cost_runner/experimental/ecdsa_secp256k1_verify.rs | 1487 | `d5d2bdc6133fc64cdbe0765a2d5ee6069a9cfedb8b03943dff269770d30b88c6` | 0 |
| soroban-env-host/src/cost_runner/experimental/ecdsa_secp256r1_recover.rs | 1499 | `2e4920ce9df183016f9bf4765bde45f76b746f34d636b03d21647e8ee7bfb7f3` | 0 |
| soroban-env-host/src/cost_runner/experimental/ed25519_scalar_mut.rs | 1353 | `5b0755082fbcd387ee756a4fcb85b19abb7f632aabefddae79063463cd81b480` | 0 |
| soroban-env-host/src/cost_runner/experimental/map_ops.rs | 1005 | `5feb978d228ff705dcee86bb90cedaa328dfa196c6fdbbfc48468d6dfbd8cd74` | 0 |
| soroban-env-host/src/cost_runner/experimental/mod.rs | 2700 | `cc07f061fc69b5348c5cb1e8dbaaad46f4b06ff7a396245618d954e98d4c77cd` | 0 |
| soroban-env-host/src/cost_runner/experimental/read_xdr.rs | 1388 | `476f11215c5a4bdcebe94772688e45f28d96db4f5dfe4da029507cd01d4f3f3f` | 0 |
| soroban-env-host/src/cost_runner/experimental/sec1_decode_point_compressed.rs | 1756 | `299089e64c18ca9c4414a6461eaf023cbcfdbdca24db9f55edbf28f922771643` | 0 |
| soroban-env-host/src/cost_runner/experimental/vec_ops.rs | 1132 | `8116fc7fe3f8d9259a9a98a719f9a8a67d96e2159db1644fc1e14cf352aaae48` | 0 |
| soroban-env-host/src/cost_runner/experimental/vm_ops.rs | 2196 | `a253e366b149b7583c7e48b3aff4a982fca99e0194b526c5276fcaa81253323a` | 0 |
| soroban-env-host/src/cost_runner/mod.rs | 787 | `d8b4f3f225b31efed2489ac70a610d6a774514944bdbb5645431e9cfef8251e3` | 0 |
| soroban-env-host/src/cost_runner/runner.rs | 4203 | `98f216ef92f42ce6364d6aa13cffcc33a6da9fa344469ebe0b7093614ca71fc7` | 0 |
| soroban-env-host/src/cost_runner/util.rs | 4774 | `9cbbfe0c50bd607d1d879a9968fdd5ec69ae096faa34216a7bbbe7986e2bc57c` | 0 |
| soroban-env-host/src/crypto/bls12_381.rs | 31382 | `1d75840927326348ef2e75c4e0c8d40106187e942eae5aa6b8a767bd7f4083f2` | 0 |
| soroban-env-host/src/crypto/bn254.rs | 22741 | `91d5f195e217783d883732c31e1ce33c318c553663bfcd299805b88b61c94885` | 0 |
| soroban-env-host/src/crypto/metered_scalar.rs | 8459 | `b84d9c5e689fd4055ec2de080d3a3c84088943c49d1920bff296d9240f1f833e` | 0 |
| soroban-env-host/src/crypto/ml_dsa.rs | 9649 | `106302dab96ec9e9f99551b8b138a585b99bb86982fac5715ff37b99f18d4201` | 0 |
| soroban-env-host/src/crypto/mod.rs | 16449 | `cdfde68a22e3fc0acf01d44d0efd9024c1d46802bc1ebf88c1ca3bdac6994af9` | 0 |
| soroban-env-host/src/crypto/poseidon/mod.rs | 915 | `a4fc963a5c1761ea73004b2906789078d4eec801d10f63e11c76930a95742ae7` | 0 |
| soroban-env-host/src/crypto/poseidon/poseidon.rs | 4398 | `5846c5e04d6bf324f3acf731886de138f0b0885d56231ffd5894267a4979b13e` | 0 |
| soroban-env-host/src/crypto/poseidon/poseidon2.rs | 11235 | `7a56d57770d361a570eb485ee8631268ddeade991566f5383b8f99d715ab926e` | 0 |
| soroban-env-host/src/crypto/poseidon/poseidon2_params.rs | 4136 | `6af419d0ef7e91cea5a67c0a158fbe72111a50e3fd46ef9fad2be03528f57c48` | 0 |
| soroban-env-host/src/crypto/poseidon/poseidon_params.rs | 3957 | `32820b7efefe8f1e3260f5fd710e5e32f3f6cdc865952cf1584dfb638eb9c5bb` | 0 |
| soroban-env-host/src/crypto/poseidon/utils.rs | 1188 | `ad887f21baf85f2221d85818720c5b0705f1b15ca9e4dc52225e38b52685d158` | 0 |
| soroban-env-host/src/e2e_invoke.rs | 50421 | `3ae8d07e58e898ec8144c5127bc3435427d45591fd72c04ca6fe747f66ea0de4` | 0 |
| soroban-env-host/src/e2e_testutils.rs | 11749 | `27727b47a61951317a21b854bd3440dae8ee7ba95fd913f03a9d84a08c1ccef3` | 0 |
| soroban-env-host/src/events/diagnostic.rs | 5750 | `a66118d5747c50c89b1c7e1fa859b6b43b91f10add59353f274b115e3a171776` | 0 |
| soroban-env-host/src/events/internal.rs | 11050 | `44c6828241d86a89af619d88026b57b38a7915632a8d163716c4afe9ac6743be` | 0 |
| soroban-env-host/src/events/mod.rs | 10348 | `8e8c489af9b03c9783bc9e396e6bd3fbd9d88b26e53ef345c77756af344ab8fe` | 0 |
| soroban-env-host/src/events/system_events.rs | 1356 | `126b8da42733be7deea23b239008eeca261828c191862f26be1d759b82422f53` | 0 |
| soroban-env-host/src/fees.rs | 15773 | `08017d0c144556974f05c7511887c91bdf4f9650772bd1b7bb630667fb3be46b` | 0 |
| soroban-env-host/src/host.rs | 143192 | `29dab11703256fe8fa58cf1f76556540325a8ca55beec6f75b75539d0d74f44e` | 0 |
| soroban-env-host/src/host/comparison.rs | 30570 | `58acd6130f38aa371d8bb78c7780314a1c3afdc05ee6b8fbe9e0ca19f3003382` | 0 |
| soroban-env-host/src/host/conversion.rs | 34426 | `bccb03358f834c0558e7b077de23643c2a5cb2bbf13b427612c63c34a59a93f4` | 0 |
| soroban-env-host/src/host/data_helper.rs | 42914 | `24f431604013d735654eec72c0fec8e41ff4dd9b3e353dbc0a641450062fa64b` | 0 |
| soroban-env-host/src/host/declared_size.rs | 39159 | `d7dba05a3added5b195a2d3985fe7a6261055e30967cb71ccbedcafe54f91e5e` | 0 |
| soroban-env-host/src/host/error.rs | 17368 | `6d4fa87584f3dc60588f83ac2bc359f8b89f6ca2b89b6bbfc34a32f854155faa` | 0 |
| soroban-env-host/src/host/frame.rs | 59783 | `55fce1dfc160bdff39bb5ea7d9d57b8a7eb0edcc21d94b253544d7f0645e9221` | 0 |
| soroban-env-host/src/host/invocation_metering.rs | 82843 | `ae1340afaadfed817c60897f244ce60494b38783e461f6d587a4ae55b21485fa` | 7 |
| soroban-env-host/src/host/ledger_entry.rs | 5565 | `101f183dfa65ec07d52bb1a96f3656de5121a301bcc96000fd058cefa5b39fbf` | 0 |
| soroban-env-host/src/host/ledger_info_helper.rs | 1502 | `9144a723b7119e868776cb21260b2f44ce286bc6a6485ada29c6133fc71e33ae` | 0 |
| soroban-env-host/src/host/lifecycle.rs | 26854 | `e842de9f63a3d3f833d460d52914a361026dfd823dc51c5a82ca46fc5a897ee1` | 0 |
| soroban-env-host/src/host/mem_helper.rs | 18356 | `7572dd84a13b22d152005ea55d3ee37ce2293da6d013382114815b8b9ec1e58e` | 0 |
| soroban-env-host/src/host/metered_clone.rs | 27328 | `e987eab2736380414d73d6d353743c42410751fac027630a9172fd6e812c1469` | 0 |
| soroban-env-host/src/host/metered_hash.rs | 2482 | `3792f8eea8df5b983fb363b0a282f8e91e3b7dfca5a424484cb5d3e0ae5c056b` | 0 |
| soroban-env-host/src/host/metered_map.rs | 15359 | `f81c4b76b8487f4f6d849751cd26353bf8778ecf0916266cf2e5fb09fd2e5b5c` | 0 |
| soroban-env-host/src/host/metered_vector.rs | 15101 | `01cb08e2b689a539d06d23518fb7f6507be48677e3b30919cd28151d8dd78da5` | 0 |
| soroban-env-host/src/host/metered_xdr.rs | 2650 | `22e70db0f290b025fb1e992b230564210a7b315c9ea7dca1e3e28609c64b7a52` | 0 |
| soroban-env-host/src/host/num.rs | 3676 | `db5c486082fc7c58daba77fb9690801c6e68601b3db7a6a2de9ed04590327d3a` | 0 |
| soroban-env-host/src/host/prng.rs | 8157 | `eeed1bff44661301241a4bd31c87705cc202eb8efd829763646947091bb6de39` | 0 |
| soroban-env-host/src/host/trace.rs | 13358 | `6de79ddfdcc146c188a6f340329d9ec62dfe7cfea46a534b3d8734e487855226` | 0 |
| soroban-env-host/src/host/trace/fmt.rs | 8072 | `0436f0f15540985f007b728d426470218ea463ed8b1dde23dedee0c08b986b07` | 0 |
| soroban-env-host/src/host/validity.rs | 1818 | `b5c6baa004d08a398e6553f5336c5c1dc2ccb099dfdc0ed708ed967147c883d5` | 0 |
| soroban-env-host/src/host_object.rs | 22259 | `f48df34cfd08f6a06c2b6a7e34e227524832648db1999792ff3f656d308e916e` | 0 |
| soroban-env-host/src/ledger_info.rs | 1348 | `5a7d202b945c0e639624746f926040eb873f640217652d55fb68fbc5acfb1f4c` | 0 |
| soroban-env-host/src/lib.rs | 2295 | `066328815dd01b7616d29bf56f74cf089c53cac95ae66910b44a56befe931cbb` | 0 |
| soroban-env-host/src/macros.rs | 3069 | `40406f573892430b2bdfce358923e0cd47bd06e0c2ab7d472a15f09b9a06b57d` | 0 |
| soroban-env-host/src/storage.rs | 39421 | `03831101eefc0fa9957ec690152f932aec42b3f9b7282e4a60da813dd756e3aa` | 0 |
| soroban-env-host/src/testutils.rs | 47592 | `b39bf85a8500949900f290c9d934ac29540d7f0a9ffa42e4a5af024b4566d78f` | 0 |
| soroban-env-host/src/vm.rs | 20023 | `dcaa075b50bb4aa900ef1dec78a715fcdcb2e189f80d61a85cc03aa9d5676ae0` | 0 |
| soroban-env-host/src/vm/dispatch.rs | 13945 | `6814aed8a87857b728a4a0dcffd959df516bad781875fe874ecc035e232e0eae` | 0 |
| soroban-env-host/src/vm/fuel_refillable.rs | 2310 | `b8e65b7971534028a2e4f2e865653cee23252a4b750ba5c9da35071b7b1cb110` | 0 |
| soroban-env-host/src/vm/func_info.rs | 6266 | `80fa97bf3e4b23155b0d52e9694d3f3351f2109f61b7a2bdf1df591f4df0d579` | 0 |
| soroban-env-host/src/vm/module_cache.rs | 7959 | `240ce8aa32e6723bde86891ba02930d7dc723ffee8af1411c9ae9262ed1fcf0e` | 0 |
| soroban-env-host/src/vm/parsed_module.rs | 31859 | `67900843e0903d307bbd93696950cc9943a79be6b4e55fd7a9a2fb0795e048ce` | 0 |
| soroban-env-macros/Cargo.toml | 710 | `ceca1d0ef5d050e4122b778a6f922ff9638365556a49398cf57192a0029bb858` | 0 |
| soroban-env-macros/src/call_macro_with_all_host_functions.rs | 5468 | `c09e407ee43ff22459be37984b927fee60e24fc649950d0c55f349030a11e52c` | 0 |
| soroban-env-macros/src/lib.rs | 7805 | `363a909ad723b7b97b568793f865979d935bebe102b055f9ec88daca1bdf2044` | 0 |
| soroban-env-macros/src/path.rs | 561 | `6d186fe3120e11b1deb22d5faa6005b68ded100c76cfde483d729fe8ea15c813` | 0 |
| soroban-env-macros/src/synth_wasm_expr_type.rs | 12311 | `350dc56852495c24af799b1398a490f31eba313fc273a106a6997c346b96ed0f` | 0 |
| soroban-fuzz-targets/Cargo.toml | 689 | `d30c34a4f158a2ccc57a4a4b9f4437edcd1d42e4cb6bb6e7aabc5e9de08bc906` | 0 |
| soroban-fuzz-targets/src/expr.rs | 6631 | `a73a323a5cbdb1bc9e48f233acb5098941c4d786b8882c312fdc0d414e604534` | 0 |
| soroban-fuzz-targets/src/lib.rs | 1150 | `3515e355cf1166e6786fb8bb3de69fad701890bd02e94272eaf08bb05d34eebf` | 0 |
| soroban-fuzz-targets/src/wasmi.rs | 4166 | `7466fbb5786c8e457ea19c947f1cff7a74b21ee93a477606b082179c21447115` | 0 |
| soroban-simulation/Cargo.toml | 1049 | `f12c43a7bfbb5def7e8a3d42c3e6f55f7330b10394367ac789eaef38fa50f58b` | 0 |
| soroban-simulation/src/lib.rs | 253 | `c554a9c4dc9655d33e65137f3e6b8f1335b256da59ea5460150c8b4e37b3b752` | 0 |
| soroban-simulation/src/network_config.rs | 7233 | `4f94adec79e4ec265a9b3760de3e2e5e39ce08ccf4ed380406f51e6b31ac1bec` | 0 |
| soroban-simulation/src/resources.rs | 12456 | `35702ace20e4c6712bb4680ab0b6f651749e8cb56367629e2e3daae07718ba03` | 0 |
| soroban-simulation/src/simulation.rs | 15415 | `7278d70854bd6bed517560045aa282014568533401e5965b8d71813c5f3f40b7` | 0 |
| soroban-simulation/src/snapshot_source.rs | 9727 | `bb6febacc3e5729108305606c7724931ccc7ef67db9806f2b17f0097810e387c` | 0 |
| soroban-simulation/src/testutils.rs | 2760 | `030d98797f9bbffee2409a0166d649042158a764c7982be9fc9f698f39b336f7` | 0 |
| soroban-synth-wasm/Cargo.toml | 809 | `4115f43e6325b4964960785e38559d7295734d4eac2ab7cec49fc33bac039ac5` | 0 |
| soroban-synth-wasm/src/expr.rs | 3370 | `20abb89282b4fcc30d85aa162b3edf8c49cd59a5d90ebc6bfd6ae6a24eacc3cd` | 0 |
| soroban-synth-wasm/src/func_emitter.rs | 15938 | `38d2d41444363114390bd9272701b0441a27402584df4983a08e075b7b9440e2` | 0 |
| soroban-synth-wasm/src/host_funcs.rs | 3306 | `5e70c2dfd0919f3f262b88e19aaf38b660cde443636533fb8c44bcfc08ba18f5` | 0 |
| soroban-synth-wasm/src/lib.rs | 1130 | `b94fdbd1d86e3438c269123a6f6c9426e0791bf3b60d81d7b0b40dceb9544328` | 0 |
| soroban-synth-wasm/src/mod_emitter.rs | 16360 | `cba054710ff6760889e36d128beeca2f4f94fbf1abacd82094daedafddbf0eec` | 0 |
| soroban-test-wasms/Cargo.toml | 241 | `6eef4c0875ef4d266d255a5f5c6bdfee377c1d347b4f7e5418f6ee1134739280` | 0 |
| soroban-test-wasms/src/lib.rs | 8515 | `eba4444d5652375364351b7ebf6cfe43575ac59506d10f5a6abb3c28f08d04b0` | 0 |
| soroban-test-wasms/wasm-workspace/Cargo.lock | 45193 | `d8e0f8458198b54e0361a56f9d1184b6ad0251bab768e6a88441953261c36b03` | 0 |
| soroban-test-wasms/wasm-workspace/Cargo.toml | 2761 | `8458693e1750830a592cf3594bc2d24c39d312b8863bdddcf3eb53e53725d6e5` | 0 |
| soroban-test-wasms/wasm-workspace/add_f32/Cargo.toml | 309 | `549e4c2516c26da535fbc0adede29e1e326c418737f90a536b6edb4059bd3eb2` | 0 |
| soroban-test-wasms/wasm-workspace/add_f32/src/lib.rs | 336 | `099703bd2f3f4088add74ae0d0f900d1cddb16967d483ca76480bd37e5aaa525` | 0 |
| soroban-test-wasms/wasm-workspace/add_i32/Cargo.toml | 309 | `dd8f899b62614dd9aa7b485eb5de3b02b65c0f341c828e7c86fa01c0ef893d9f` | 0 |
| soroban-test-wasms/wasm-workspace/add_i32/src/lib.rs | 275 | `609f7db6583e31743bb9b6baa6d7f9f272b3d0f76cc9bc633244bdadc1ae7856` | 0 |
| soroban-test-wasms/wasm-workspace/alloc/Cargo.toml | 329 | `01be473ad078fed7227bf22ed802501063bdc72f25c1e4a53c69972e9c68ee18` | 0 |
| soroban-test-wasms/wasm-workspace/alloc/src/lib.rs | 708 | `3ad94be5c06b55ed4639bb79f59be677ae9f8c38884bccb249bade8e7f4ad870` | 0 |
| soroban-test-wasms/wasm-workspace/auth/Cargo.toml | 312 | `f04a346b02d6b304d0b1fe2f724f742545a48ed26bce353fc75d868d47201ba1` | 0 |
| soroban-test-wasms/wasm-workspace/auth/src/lib.rs | 8544 | `2e0064ca991f83c3a00177f052bbc5c053087546ed1e42a944c7af810bb03621` | 0 |
| soroban-test-wasms/wasm-workspace/builtin_auth_delegation/Cargo.toml | 306 | `585673f879ec8063f7cc5b6a7e5e714ab5315f3a3fa2f054d13e8e65b9b9bc24` | 0 |
| soroban-test-wasms/wasm-workspace/builtin_auth_delegation/src/lib.rs | 4959 | `aea2b21df2e94d204ff31f7ccdea5efdcc044afce347060732dd47581482ac1a` | 0 |
| soroban-test-wasms/wasm-workspace/check_auth_instance_storage/Cargo.toml | 310 | `5d3baa922a48fbb24bf0fd4d6caf9057a6f0f4f0de307fdbf4ade6dd119b5862` | 0 |
| soroban-test-wasms/wasm-workspace/check_auth_instance_storage/src/lib.rs | 1900 | `8aaca638c110973cec3b5aa5fe3e45b77ed12f9e189120c88c0a7ba3737fb92d` | 0 |
| soroban-test-wasms/wasm-workspace/complex/Cargo.toml | 293 | `0067ed9e3a4473fa625554efc2b026ff83ab9211a7ae243dbdb6afebb6fb9245` | 0 |
| soroban-test-wasms/wasm-workspace/complex/src/lib.rs | 1522 | `7fb764db8fd1ff735f0077daa0c0f8fbca952fb621075820dd741321a27b37d0` | 0 |
| soroban-test-wasms/wasm-workspace/conditional_account/Cargo.toml | 302 | `9dec27ee4ce2269cb4fcf2b36bf97314ca3e666314f8361e3f352b86e184cc8a` | 0 |
| soroban-test-wasms/wasm-workspace/conditional_account/src/lib.rs | 1190 | `8373ab257590bdc0023784bdcd8c465630ca631a1f820b1db1e6fb9b88fbf4ab` | 0 |
| soroban-test-wasms/wasm-workspace/constructor/Cargo.toml | 294 | `ff1e3d8dc9d364c3fe88c5ebd67a52db55b36c761b5bb0827cba0a25ce5bce18` | 0 |
| soroban-test-wasms/wasm-workspace/constructor/src/lib.rs | 1058 | `c423ed6d892c0286acc21a9fb78cb7bb159b247dce09c5c9b01b29cdcc246d76` | 0 |
| soroban-test-wasms/wasm-workspace/constructor_with_result/Cargo.toml | 306 | `2e96ef48cc040386131b56ed8a1d555850283e07eaf5087ef8d62abdb5452900` | 0 |
| soroban-test-wasms/wasm-workspace/constructor_with_result/src/lib.rs | 621 | `32a1d47c7d3c10309b7aba51b7ac5138c80adcbed19b0726950c05b8946cf72d` | 0 |
| soroban-test-wasms/wasm-workspace/constructor_with_return_value/Cargo.toml | 312 | `59d0b78167d61493e8e991da525ba1e65976a14b7c9ea8b06ad944c19b9b8798` | 0 |
| soroban-test-wasms/wasm-workspace/constructor_with_return_value/src/lib.rs | 234 | `c30ae802d69000e032c778d0558e7a3cd1fc93750e69f617a27d5a281b812522` | 0 |
| soroban-test-wasms/wasm-workspace/contract_data/Cargo.toml | 299 | `77083980ef46d4854eb10c3fc40df19e910dcac6df40935a6af45b0eb3d17332` | 0 |
| soroban-test-wasms/wasm-workspace/contract_data/src/lib.rs | 3353 | `dbb18e27f6dff3765423e305add70da6a038f1a81835d0479b56c2ecce7733f1` | 0 |
| soroban-test-wasms/wasm-workspace/contract_sac_transfer/Cargo.toml | 299 | `9e6a1c69f818e4c6a52f70f0340235131b9af4b81faeffed68f4ded27154d277` | 0 |
| soroban-test-wasms/wasm-workspace/contract_sac_transfer/src/lib.rs | 1284 | `bbfce0bd50690fb25cce60b10178aec5d0292b1f3423cd59013297764bbd35d8` | 0 |
| soroban-test-wasms/wasm-workspace/create_contract/Cargo.toml | 317 | `281d6a213ecfeb71d508b60fb9240834123a0c7fb9b83d6690a7ef78625539bb` | 0 |
| soroban-test-wasms/wasm-workspace/create_contract/src/lib.rs | 419 | `d999ae4431e2cca2ff8500a042c58581208a70775eada7264e8985de95b11138` | 0 |
| soroban-test-wasms/wasm-workspace/custom_account_context/Cargo.toml | 305 | `92af459b76ad60e3ce347fcdc67aa5a1ad051c49b4adb77f7c67a55589badc64` | 0 |
| soroban-test-wasms/wasm-workspace/custom_account_context/src/lib.rs | 601 | `b657abdf54831ee754ff23623c5de4d0723013371aa201838112bc49df3bfb45` | 0 |
| soroban-test-wasms/wasm-workspace/delegated_account/Cargo.toml | 300 | `7908ae88dab514ec6d70894655953384c7da38a7d4f969c6d63ede8e23c6a439` | 0 |
| soroban-test-wasms/wasm-workspace/delegated_account/src/lib.rs | 868 | `36ad27bafba63f3f84003fc542a5ea676ae40bd5cf95d76532fcbf15f57c64e2` | 0 |
| soroban-test-wasms/wasm-workspace/deployer/Cargo.toml | 291 | `0a745dea42f11644e128a60ea95b230fc9228d657d1e59bd0505c06e8621d4d8` | 0 |
| soroban-test-wasms/wasm-workspace/deployer/src/lib.rs | 1873 | `ade03dfecc57c2a865c94f0e96203aae80eb6b5a081827a7247768a55fd561cc` | 0 |
| soroban-test-wasms/wasm-workspace/deployer_with_constructor/Cargo.toml | 308 | `7cd7dc3819357f91f599199090fd0c56e5ffa2f8e05e631255fb4e22330adce6` | 0 |
| soroban-test-wasms/wasm-workspace/deployer_with_constructor/src/lib.rs | 5011 | `7648828e97d74ed7ece814fa105f4ad2bbff85acc1e599b62e3d5923a24aea54` | 0 |
| soroban-test-wasms/wasm-workspace/err/Cargo.toml | 347 | `49a7e63a73faaa259430d07f3f4bfc4248053afd571a89ddad82b8b488e5c8be` | 0 |
| soroban-test-wasms/wasm-workspace/err/src/lib.rs | 2881 | `6d421da68d5bcfb4dec07757387e48833cb5f3bbe6ce99dfd8730a08605aed23` | 0 |
| soroban-test-wasms/wasm-workspace/fannkuch/Cargo.toml | 310 | `b6ec9f13152db30ec92fb459ede39594cbc77404f8e176e06baa71b323a11ef0` | 0 |
| soroban-test-wasms/wasm-workspace/fannkuch/src/lib.rs | 2236 | `f8af8a42fd6fc33fde15a97091e4382bba5c851e44210cf3a840f70d8ef81c97` | 0 |
| soroban-test-wasms/wasm-workspace/fib/Cargo.toml | 305 | `30b7bf6023952b31b3a9d8cb1df2aa7223149253f8678452726b0d0df58035be` | 0 |
| soroban-test-wasms/wasm-workspace/fib/src/lib.rs | 268 | `c957875f4c1b35d053c3b2d746bcf748667913f12e33be6e03d244b537521d84` | 0 |
| soroban-test-wasms/wasm-workspace/hostile/Cargo.toml | 350 | `a828d8f58a569be29dc2f6c64a35953cf15829e6ad1925b69d76d2ff08709752` | 0 |
| soroban-test-wasms/wasm-workspace/hostile/src/lib.rs | 3124 | `c2eedf2f69c9f8cefbcf0e12967b76413d1b42e347f6478c221e8b294c6227f9` | 0 |
| soroban-test-wasms/wasm-workspace/hostile_large_val/Cargo.toml | 311 | `1317a69cd05283c9f027d3211fb3b37d9ae9757257a5565ae5b145be0680c8eb` | 0 |
| soroban-test-wasms/wasm-workspace/hostile_large_val/src/lib.rs | 2553 | `dbf1d00afd9f5f62c0bab4a4e51114fb876585262f8da8af1f030f04031d9a02` | 0 |
| soroban-test-wasms/wasm-workspace/invoke_contract/Cargo.toml | 317 | `c1f763f78de7b09d9095efac80104d088f6bd41ecc2bd6fb59e345e90c5beb67` | 0 |
| soroban-test-wasms/wasm-workspace/invoke_contract/src/lib.rs | 1943 | `331251706eeb7ca4c8f64877b2f4e2176b7195299989a6271db21db3c0a70357` | 0 |
| soroban-test-wasms/wasm-workspace/invoker_auth/Cargo.toml | 320 | `cdcf51951afe17159a5b6297b81e29ecbb785db2b3a654f7378a70a7f62fc726` | 0 |
| soroban-test-wasms/wasm-workspace/invoker_auth/src/lib.rs | 5921 | `6deed63acc70a7cf0c92f307243454a2ba4b1d2aed10cbafb59ed07207d64b64` | 0 |
| soroban-test-wasms/wasm-workspace/linear_memory/Cargo.toml | 341 | `907403fc34c319e3f0c99cc42b49584c108d39a846eca72924ac03a49d6a707c` | 0 |
| soroban-test-wasms/wasm-workspace/linear_memory/src/lib.rs | 2861 | `998f890f085a31c269dee25aa5ac3eef9a62efc4166d2d26377073eab3574a3d` | 0 |
| soroban-test-wasms/wasm-workspace/loadgen/Cargo.toml | 293 | `54a775e24e6a6b93bd1a91e8a8f67c9ba8a34893ef5dc66b70aa2e4b8c3082b8` | 0 |
| soroban-test-wasms/wasm-workspace/loadgen/src/lib.rs | 2035 | `9a2077b1af173b0dad443032321f21dce3b6966d0ae88ff2c0043ec6f3859640` | 0 |
| soroban-test-wasms/wasm-workspace/no_arg_constructor/Cargo.toml | 301 | `cdd661d64e2e9731bdbc49637372195660a1f21304f516af3ec7fc6164fec8c2` | 0 |
| soroban-test-wasms/wasm-workspace/no_arg_constructor/src/lib.rs | 696 | `f49c7035942d9351dde370ed4ea4e00698f76f66f2cee13079ccc0636acdc413` | 0 |
| soroban-test-wasms/wasm-workspace/recursive_account/Cargo.toml | 287 | `ba3460e51138adcf00bcd2fe7e59d6dc01a78fa752ead699befae8c3c607ba16` | 0 |
| soroban-test-wasms/wasm-workspace/recursive_account/src/lib.rs | 1819 | `99df3ded80c336870ed36935ca34af8306c1644bcc127f8adee9e6cb26ff2a24` | 0 |
| soroban-test-wasms/wasm-workspace/sac_reentry_account/Cargo.toml | 297 | `a8627c01b2129d0dae15ed2f709724cbebcb641ab9f5c66b9893b57e9c7078f4` | 0 |
| soroban-test-wasms/wasm-workspace/sac_reentry_account/src/lib.rs | 1176 | `44c4a73769a6db79991b2b981560e4c62df6a07a5a467550c8995f5333af2164` | 0 |
| soroban-test-wasms/wasm-workspace/simple_account/Cargo.toml | 300 | `233daf8057939469264afc3dd17b237b7ef423085d4eea909e79ddf5a41b2cbb` | 0 |
| soroban-test-wasms/wasm-workspace/simple_account/src/lib.rs | 948 | `7c74cf48ea7db5ed1ff209926ba7d98ba4c32127d9e52e229a3c90eedfed4e28` | 0 |
| soroban-test-wasms/wasm-workspace/sum_i32/Cargo.toml | 309 | `c37d0a5d2621bb8edb11aaa0a111d4c0d8afa4e1a65df8dfc404136711141d25` | 0 |
| soroban-test-wasms/wasm-workspace/sum_i32/src/lib.rs | 561 | `4b1c69bf2e59646c6202ce0e9e460a7d22eea3490e517ecc4f56cfc8e4b8f49b` | 0 |
| soroban-test-wasms/wasm-workspace/try_call_sac/Cargo.toml | 295 | `a8ef3fd8c92173dbc8e0975d0ba005063a495e49bd2be96fec39d73c5c057599` | 0 |
| soroban-test-wasms/wasm-workspace/try_call_sac/src/lib.rs | 435 | `e469644aac889f9613c96038630e05302321aede066868c0ac67e55f68508c5f` | 0 |
| soroban-test-wasms/wasm-workspace/update/Cargo.toml | 321 | `add583b889fe9dba5aa81ac0e5aa0a4d1cf11df49c0600e720b71b6c932fc1c2` | 0 |
| soroban-test-wasms/wasm-workspace/update/src/lib.rs | 945 | `d0ae9d5190e0f6251ee7182be9c052e068695ed305c7666caf4b455789c72c93` | 0 |
| soroban-test-wasms/wasm-workspace/update_exec_ref/Cargo.toml | 314 | `9422d19fe2ef02653a2083bfca58d6ae52eddf7a04071a96c66cd327501a0705` | 0 |
| soroban-test-wasms/wasm-workspace/update_exec_ref/src/lib.rs | 1105 | `064e0dcae88d9e531fcf0d64240f1d650ab7c77afeaac0d07bec787a95dbc8a5` | 0 |
| soroban-test-wasms/wasm-workspace/upload_contract/Cargo.toml | 317 | `521c2d07450d0ca5174ed43df2b01b0e85341b9291813f03476a8aec1db2472d` | 0 |
| soroban-test-wasms/wasm-workspace/upload_contract/src/lib.rs | 252 | `5033bb1c628243bdaecc55b1c7676b20b22f73fe4842905b5bb92a1a111061c9` | 0 |
| soroban-test-wasms/wasm-workspace/vec/Cargo.toml | 289 | `8e78cf5495f3569dcb16e392caec5420e0c4e38682a79bee9f24bdf1bd2ef8e3` | 0 |
| soroban-test-wasms/wasm-workspace/vec/src/lib.rs | 346 | `a358381709762177476df8c9dcacdc6406e499b81de7523278f3fbf5212aa7d3` | 0 |
| soroban-test-wasms/wasm-workspace/write_upgrade_bytes/Cargo.toml | 330 | `6f5ed7b39a290835d688ae0aa0ae465b065d7b02fc6f758f08e3df5fc090d95c` | 0 |
| soroban-test-wasms/wasm-workspace/write_upgrade_bytes/src/lib.rs | 1003 | `8a0cc6e5f77713ee726982d933260e90732e70873c0a2bb8cc662ec651472c6d` | 0 |
