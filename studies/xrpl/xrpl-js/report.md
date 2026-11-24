# Security & Post-Quantum Readiness Audit Report

**Project:** xrpl-js @ 126168271b8c · XRPL Foundation — public repository (passive review)
| | |
|---|---|
| Organization | QSI |
| Report date | 2026-11-24 12:24 UTC |
| Report version | 1 |
| Audit run | 22ad9cdd-66c7-4162-a9e8-c1b53206b328 (Document audit) |
| Analyzer engine | qsi-engine 1.20.0 |
| Risk profile | Web3 project |
| Content SHA-256 | `2dee7faa79d4a251b5d562c2e1b4e650bb907ea86372d81825e28752ee2db94d` |
| Signature key (Ed25519 SHA-256 fingerprint, then the ML-DSA-65 one where it co-signs; the signature is the separate file report.sig.json) | `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e · ML-DSA-65 dbd4e297b3213d1d7577a565e76de14cc5ad0e409f1dc68291c67266fc95066a` |
> This report presents automated and documented analysis results for the stated scope. It is not a legal opinion, a certification or an attestation of compliance with any standard.

## 1. Executive summary

- Critical: **0**
- High: **0**
- Medium: **4**
- Low: **3**
- Info: **2**

- Confirmed technical vulnerability: 0
- Known vulnerable component: 0
- Confirmed configuration error: 0
- Potential cryptographic risk: 0
- Long-term post-quantum risk: 7
- Improvement recommendation: 1
- Insufficient data: 1

Mosca's inequality (x + y > z): x = 5, y = 5, z = 12 → tight margin. _z is a planning assumption chosen per risk profile, not a prediction. A cryptographically relevant quantum computer is not publicly known to exist today._

**Post-quantum maturity: Level 0 of 4 — no post-quantum cryptography.** Next step: Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

## 2. Scope and boundaries

Mode: Document audit

Repository: <https://github.com/XRPLF/xrpl.js> @ `126168271b8cbe784baf77fec05d2cd8c1837815` — evidence links open the lines at this commit.

377 files, 4397494 bytes in total, 1 redaction(s); the per-file SHA-256 list is in appendix C.

## 3. Methodology

| Area | Status | Count | Examples |
|---|---|---|---|
| source_code | checked | 361 | .ci-config/getNewAmendments.js: 56 lines scanned with 17 rule patterns and 340 registry patterns; docs/assets/hierarchy.js: 1 lines scanned with 17 rule patterns and 340 registry patterns; docs/assets/icons.js: 18 lines scanned with 17 rule patterns and 340 registry patterns |
| dependencies | checked | 14 | package-lock.json: 1277 dependencies parsed (1270 pinned); package.json: 45 dependencies parsed (0 pinned); packages/isomorphic/package.json: 5 dependencies parsed (1 pinned) |
| certificates_and_keys | checked | 1 | packages/ripple-keypairs/SECURITY.md: certificates/keys parsed |
| secrets | checked | 1 | packages/xrpl/src/Wallet/index.ts: 1 redacted value(s) not reported (comments, test modules, fixture declarations, placeholders, values the source annotates as published, or hex values not bound to a secret name) |
| entropy | checked | 1 | random-number generation: 361 code files read with 0 macro definitions from the tree; 0 ineffective guard(s), 0 weak random-bytes provider(s), 0 weak key-generation site(s) |
| crediting | checked | 1 | payment crediting: 72 file(s) read incoming transfers on TON, the XRP Ledger (Xaman sign requests included), Tron or an EVM chain, 0 credit from a Tron or EVM node, 0 from fetched Solana transactions; 0 lead(s). A wait for confirmations or finality is recognised by its words, not traced; reorganisations and duplicate crediting are not checked |
| key_storage | checked | 1 | key settings with a fallback in the code: 0; decryption fallbacks: 0; derived nonces: 0; key columns: 0 (no KMS, HSM or vault service found); author warnings: 0 |
| osv_advisories | checked | 1 | 1122 pinned packages queried at OSV.dev; 6 affected (6 of them only in development or build dependencies) |

_Long lists are grouped here; the full per-file list is in the JSON report, signed with the same key._

## 4. Assets examined and not examined

- None

## 5. Architecture overview

Static review of the source tree xrpl-js at 126168271b8cbe784baf77fec05d2cd8c1837815. 377 files analysed; of 1274 files, 409 are test, fuzzing, benchmark or example code and were left out, 488 are not read by any analyzer, 0 exceed the per-file limit and 0 did not fit the total limit. Files no analyzer reads include: .ai-review/instructions.md, .ci-config/xrpld.cfg, .claude/skills/batch-deps-upgrade/README.md, .claude/skills/batch-deps-upgrade/SKILL.md, .coderabbit.yaml. 31 files in build-output or dependency-cache directories (.git, .hg, .venv, __pycache__, build, dist, node_modules, target, vendor, venv) were not read. No requests were sent to the owner's systems.

## 6. Overall security posture

- Indicative posture index: **100** / 100 — _Derived from findings in scope (confirmed and potential issues weighted by severity). Indicative only; not comparable across differently scoped audits._
- Quantum-vulnerable share of inventory: 65.9%

## 7. Detailed findings

### QSI-2026-50291 — Quantum-vulnerable Pedersen commitment: threshold signing and MPC protocols (8 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:Pedersen commitment:threshold_mpc`
- Data source: packages/mpt-crypto/src/index.ts
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.20.0 · 2026-11-24 12:24 UTC
- Priority score: 33.0 / 100
- CVSS v3.1: not applicable

11 reference(s) to Pedersen commitment across 8 file(s), e.g. packages/mpt-crypto/src/index.ts:34. Role, judged from paths, function names and nearby code: threshold signing and MPC protocols. Paillier, Pedersen commitments and the discrete-logarithm proofs inside threshold ECDSA and EdDSA protocols all fall to Shor's algorithm; a post-quantum threshold scheme is a protocol change, not a parameter change.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open packages/mpt-crypto/src/index.ts:34 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [packages/mpt-crypto/src/index.ts](https://github.com/XRPLF/xrpl.js/blob/126168271b8cbe784baf77fec05d2cd8c1837815/packages/mpt-crypto/src/index.ts#L34) · line 34 · SHA-256 272811dd801e9be1a20ee049444545977f35da9c4876676955bd6efa4b2503e6_

```
   33 |   decryptAmount,
   34 |   getPedersenCommitment,
   35 | } from './primitives'
```

_file_excerpt · [packages/mpt-crypto/src/module.ts](https://github.com/XRPLF/xrpl.js/blob/126168271b8cbe784baf77fec05d2cd8c1837815/packages/mpt-crypto/src/module.ts#L34) · line 34 · SHA-256 873c48d7a7faeb88edea9f22461b42509302d05914087c7b82324c1e9ee3fe4d_

```
   33 |   ) => number
   34 |   _mpt_get_pedersen_commitment: (
   35 |     amount: bigint,
```

_file_excerpt · [packages/mpt-crypto/src/primitives.ts](https://github.com/XRPLF/xrpl.js/blob/126168271b8cbe784baf77fec05d2cd8c1837815/packages/mpt-crypto/src/primitives.ts#L125) · line 125 · SHA-256 9d034bd632b0a946d4490920309bd39f0ecacc00af6bf8c52d5676b0c268a726_

```
  124 |  */
  125 | export async function getPedersenCommitment(
  126 |   amount: bigint,
```

_file_excerpt · [packages/mpt-crypto/src/primitives.ts](https://github.com/XRPLF/xrpl.js/blob/126168271b8cbe784baf77fec05d2cd8c1837815/packages/mpt-crypto/src/primitives.ts#L140) · line 140 · SHA-256 926b86bf4f64f49cb41a4f350dab2254002d97ec4b4b088b8a99a5155f32bfdf_

```
  139 |     const outPtr = marshaller.alloc(PEDERSEN_COMMIT_SIZE)
  140 |     if (mod._mpt_get_pedersen_commitment(amount, blindingPtr, outPtr) !== 0) {
  141 |       throw new Error('mpt_get_pedersen_commitment failed')
```

_file_excerpt · [packages/mpt-crypto/src/primitives.ts](https://github.com/XRPLF/xrpl.js/blob/126168271b8cbe784baf77fec05d2cd8c1837815/packages/mpt-crypto/src/primitives.ts#L141) · line 141 · SHA-256 f48a257d8922a8ac74f545c6e778ef499aba191664206fa8e840b51f38655f0f_

```
  140 |     if (mod._mpt_get_pedersen_commitment(amount, blindingPtr, outPtr) !== 0) {
  141 |       throw new Error('mpt_get_pedersen_commitment failed')
  142 |     }
```

_file_excerpt · [packages/mpt-crypto/wasm/mpt_crypto.js](https://github.com/XRPLF/xrpl.js/blob/126168271b8cbe784baf77fec05d2cd8c1837815/packages/mpt-crypto/wasm/mpt_crypto.js#L1) · line 1 · SHA-256 beda46149a036ede838fefe450f8ebc0df16a6ceacc5d6bd9f91ddcee15e2c65_

```
    1 | var MptCrypto=(()=>{var _scriptName=globalThis.document?.currentScript?.src;return async function(moduleArg={}){var Module=moduleArg;var ENVIRONMENT_IS_WEB=!!globalThis.window;var ENVIRONMENT_IS_WORKER=!!globalThis.WorkerGlobalScope;var ENVIRONMENT_IS_NODE=globalThis.process?.versions?.node&&globalT
    2 | ;return Module}})();if(typeof exports==="object"&&typeof module==="object"){module.exports=MptCrypto;module.exports.default=MptCrypto}else if(typeof define==="function"&&define["amd"])define([],()=>MptCrypto);
```

_file_excerpt · [packages/mpt-crypto/wasm/mpt_crypto.mjs](https://github.com/XRPLF/xrpl.js/blob/126168271b8cbe784baf77fec05d2cd8c1837815/packages/mpt-crypto/wasm/mpt_crypto.mjs#L1) · line 1 · SHA-256 b452b444f90f48b742052febc8d226744196e6f3cabd5ca015b481bec994a1b0_

```
    1 | async function MptCrypto(moduleArg={}){var Module=moduleArg;var ENVIRONMENT_IS_WEB=!!globalThis.window;var ENVIRONMENT_IS_WORKER=!!globalThis.WorkerGlobalScope;var ENVIRONMENT_IS_NODE=globalThis.process?.versions?.node&&globalThis.process?.type!="renderer";if(ENVIRONMENT_IS_NODE){const{createRequire
    2 | ;return Module}export default MptCrypto;
```

_file_excerpt · [packages/mpt-crypto/wasm/mpt_crypto.web.mjs](https://github.com/XRPLF/xrpl.js/blob/126168271b8cbe784baf77fec05d2cd8c1837815/packages/mpt-crypto/wasm/mpt_crypto.web.mjs#L1) · line 1 · SHA-256 92544b1af8f4256bf82285e006d4043ff7d0f3d06e04aec5d26e4a457a48ab0c_

```
    1 | async function MptCrypto(moduleArg={}){var Module=moduleArg;var ENVIRONMENT_IS_WEB=!!globalThis.window;var ENVIRONMENT_IS_WORKER=!!globalThis.WorkerGlobalScope;var ENVIRONMENT_IS_NODE=globalThis.process?.versions?.node&&globalThis.process?.type!="renderer";var programArgs=[];var thisProgram="./this.
    2 | ;return Module}export default MptCrypto;
```

_file_excerpt · [packages/xrpl/src/confidential/convert.ts](https://github.com/XRPLF/xrpl.js/blob/126168271b8cbe784baf77fec05d2cd8c1837815/packages/xrpl/src/confidential/convert.ts#L162) · line 162 · SHA-256 454c0b50821f443f184484db1da7b1fb465d234acb98a2f3e9d518a73db564db_

```
  161 |   ])
  162 |   const balanceCommitment = await crypto.getPedersenCommitment(balance, rho)
  163 |   const [holderEncryptedAmount, issuerEncryptedAmount, zkProof] =
```

_file_excerpt · [packages/xrpl/src/confidential/transfer.ts](https://github.com/XRPLF/xrpl.js/blob/126168271b8cbe784baf77fec05d2cd8c1837815/packages/xrpl/src/confidential/transfer.ts#L97) · line 97 · SHA-256 c082068b53776d80f715ec37d6e14204904770ed786a038e1cb0665fb0f5b3c0_

```
   96 |     await Promise.all([
   97 |       crypto.getPedersenCommitment(amount, txBlinding),
   98 |       crypto.getPedersenCommitment(balance, rho),
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Track post-quantum threshold signatures (NIST IR 8214C) and keep the protocol layer ready to swap the signature scheme; record which keys and shares must stay valid for how long.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-50293 — Quantum-vulnerable ECDSA: transaction and message signing (8 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:ECDSA:transaction_signing`
- Data source: packages/ripple-address-codec/src/xrp-codec.ts
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.20.0 · 2026-11-24 12:24 UTC
- Priority score: 33.0 / 100
- CVSS v3.1: not applicable

33 reference(s) to ECDSA across 8 file(s), e.g. packages/ripple-address-codec/src/xrp-codec.ts:49. Role, judged from paths, function names and nearby code: transaction and message signing. A CRQC derives the private key from a public key that is already known (on chain after the first spend, in reused addresses): funds and approvals controlled by these keys need a migration path.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open packages/ripple-address-codec/src/xrp-codec.ts:49 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [packages/ripple-address-codec/src/xrp-codec.ts](https://github.com/XRPLF/xrpl.js/blob/126168271b8cbe784baf77fec05d2cd8c1837815/packages/ripple-address-codec/src/xrp-codec.ts#L49) · line 49 · SHA-256 a7ce798a6d19415f2fd5a328fedb10a94b9f6593eaafe055979b90d1ef939bdc_

```
   48 |       expectedLength?: number
   49 |       versionTypes?: ['ed25519', 'secp256k1']
   50 |     },
```

_file_excerpt · [packages/ripple-address-codec/src/xrp-codec.ts](https://github.com/XRPLF/xrpl.js/blob/126168271b8cbe784baf77fec05d2cd8c1837815/packages/ripple-address-codec/src/xrp-codec.ts#L54) · line 54 · SHA-256 7932e17040b0c16019f170c74b61090e355dfc5a7d26e8eb0183142bc8a2353e_

```
   53 |     bytes: Uint8Array
   54 |     type: 'ed25519' | 'secp256k1' | null
   55 |   } {
```

_file_excerpt · [packages/ripple-address-codec/src/xrp-codec.ts](https://github.com/XRPLF/xrpl.js/blob/126168271b8cbe784baf77fec05d2cd8c1837815/packages/ripple-address-codec/src/xrp-codec.ts#L169) · line 169 · SHA-256 c323ee667704fa5309cc04ea56c0d81b9331785f3b44298fdd4909e17ffb7f09_

```
  168 |   entropy: ByteArray,
  169 |   type: 'ed25519' | 'secp256k1',
  170 | ): string {
```

_file_excerpt · [packages/ripple-keypairs/src/index.ts](https://github.com/XRPLF/xrpl.js/blob/126168271b8cbe784baf77fec05d2cd8c1837815/packages/ripple-keypairs/src/index.ts#L11) · line 11 · SHA-256 6633fbb58408b007bfaec243c4d2d46e959b3c67640cfc58021ac9bc82353410_

```
   10 | 
   11 | import { accountPublicFromPublicGenerator } from './signing-schemes/secp256k1/utils'
   12 | import Sha512 from './utils/Sha512'
```

_file_excerpt · [packages/ripple-keypairs/src/index.ts](https://github.com/XRPLF/xrpl.js/blob/126168271b8cbe784baf77fec05d2cd8c1837815/packages/ripple-keypairs/src/index.ts#L20) · line 20 · SHA-256 c782e83f709f2b4f4a6db880d248f2ca5fea537e160269e83bacb41db5f95571_

```
   19 | 
   20 | import secp256k1 from './signing-schemes/secp256k1'
   21 | import ed25519 from './signing-schemes/ed25519'
```

_file_excerpt · [packages/ripple-keypairs/src/index.ts](https://github.com/XRPLF/xrpl.js/blob/126168271b8cbe784baf77fec05d2cd8c1837815/packages/ripple-keypairs/src/index.ts#L45) · line 45 · SHA-256 3f197b6be35f7623e516244d987fae898562c76cf380ea797920845d547843a0_

```
   44 | function getSigningScheme(algorithm: Algorithm): SigningScheme {
   45 |   const schemes = { 'ecdsa-secp256k1': secp256k1, ed25519 }
   46 |   return schemes[algorithm]
```

_file_excerpt · [packages/ripple-keypairs/src/signing-schemes/secp256k1/index.ts](https://github.com/XRPLF/xrpl.js/blob/126168271b8cbe784baf77fec05d2cd8c1837815/packages/ripple-keypairs/src/signing-schemes/secp256k1/index.ts#L2) · line 2 · SHA-256 ca87b12d95c1b77983ee9ac5e0c02f7e97fb01244a0380220445783dd74056ab_

```
    1 | import { numberToBytesBE } from '@noble/curves/utils.js'
    2 | import { secp256k1 as nobleSecp256k1 } from '@noble/curves/secp256k1.js'
    3 | import { bytesToHex, hexToBytes } from '@xrplf/isomorphic/utils'
```

_file_excerpt · [packages/ripple-keypairs/src/signing-schemes/secp256k1/index.ts](https://github.com/XRPLF/xrpl.js/blob/126168271b8cbe784baf77fec05d2cd8c1837815/packages/ripple-keypairs/src/signing-schemes/secp256k1/index.ts#L17) · line 17 · SHA-256 b4e331fbe4db257b7c1bff25143b9d1da12a62e4f768c944be8dbdb0f42e6f24_

```
   16 | 
   17 | const secp256k1: SigningScheme = {
   18 |   deriveKeypair(
```

_file_excerpt · [packages/ripple-keypairs/src/signing-schemes/secp256k1/index.ts](https://github.com/XRPLF/xrpl.js/blob/126168271b8cbe784baf77fec05d2cd8c1837815/packages/ripple-keypairs/src/signing-schemes/secp256k1/index.ts#L74) · line 74 · SHA-256 1fc4d4bf3a78ad0e4060c6eed3b153cd7e3e87e7fd438aeaab9392a13ecc1cd9_

```
   73 | 
   74 | export default secp256k1
```

_file_excerpt · [packages/ripple-keypairs/src/signing-schemes/secp256k1/utils.ts](https://github.com/XRPLF/xrpl.js/blob/126168271b8cbe784baf77fec05d2cd8c1837815/packages/ripple-keypairs/src/signing-schemes/secp256k1/utils.ts#L1) · line 1 · SHA-256 93125f0d057c71035b8645323520837aeb14c0345cfaf304d4086664b50b9368_

```
    1 | import { secp256k1 } from '@noble/curves/secp256k1.js'
    2 | 
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains adopt them.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-50295 — Quantum-vulnerable Ed25519: transaction and message signing (1 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:Ed25519:transaction_signing`
- Data source: packages/ripple-keypairs/src/signing-schemes/ed25519/index.ts
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.20.0 · 2026-11-24 12:24 UTC
- Priority score: 33.0 / 100
- CVSS v3.1: not applicable

1 reference(s) to Ed25519 across 1 file(s), e.g. packages/ripple-keypairs/src/signing-schemes/ed25519/index.ts:1. Role, judged from paths, function names and nearby code: transaction and message signing. A CRQC derives the private key from a public key that is already known (on chain after the first spend, in reused addresses): funds and approvals controlled by these keys need a migration path.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open packages/ripple-keypairs/src/signing-schemes/ed25519/index.ts:1 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [packages/ripple-keypairs/src/signing-schemes/ed25519/index.ts](https://github.com/XRPLF/xrpl.js/blob/126168271b8cbe784baf77fec05d2cd8c1837815/packages/ripple-keypairs/src/signing-schemes/ed25519/index.ts#L1) · line 1 · SHA-256 6d60f80f9d57cc05d6757b0f6598c903cccf4c80d9e1be85936ff490218c2487_

```
    1 | import { ed25519 as nobleEd25519 } from '@noble/curves/ed25519.js'
    2 | import { bytesToHex, hexToBytes } from '@xrplf/isomorphic/utils'
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains adopt them.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-50289 — Quantum-vulnerable ECDSA: role not determined (4 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:ECDSA:general`
- Data source: packages/mpt-crypto/src/homomorphic.ts
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.20.0 · 2026-11-24 12:24 UTC
- Priority score: 31.7 / 100
- CVSS v3.1: not applicable

5 reference(s) to ECDSA across 4 file(s), e.g. packages/mpt-crypto/src/homomorphic.ts:40. Role, judged from paths, function names and nearby code: role not determined. The code does not show what the keys protect; review decides the priority.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open packages/mpt-crypto/src/homomorphic.ts:40 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [packages/mpt-crypto/src/homomorphic.ts](https://github.com/XRPLF/xrpl.js/blob/126168271b8cbe784baf77fec05d2cd8c1837815/packages/mpt-crypto/src/homomorphic.ts#L40) · line 40 · SHA-256 cf13ea6ac7d49a8bf63a8cdb39fde812d984e5c2cf881c4f3e539d1565a2c45b_

```
   39 |     if (ctx === 0) {
   40 |       throw new Error('mpt-crypto: secp256k1 context unavailable')
   41 |     }
```

_file_excerpt · [packages/mpt-crypto/src/module.ts](https://github.com/XRPLF/xrpl.js/blob/126168271b8cbe784baf77fec05d2cd8c1837815/packages/mpt-crypto/src/module.ts#L162) · line 162 · SHA-256 8ad912e0ff49d249dedb96654aefe463fe2f85c4aaf0eb624a969410907208b9_

```
  161 |   if (instance._mpt_secp256k1_context() === 0) {
  162 |     throw new Error('mpt-crypto: failed to initialize the secp256k1 context')
  163 |   }
```

_file_excerpt · [packages/xrpl/src/ECDSA.ts](https://github.com/XRPLF/xrpl.js/blob/126168271b8cbe784baf77fec05d2cd8c1837815/packages/xrpl/src/ECDSA.ts#L3) · line 3 · SHA-256 a9262e2dcbe7e50501c2dad0fb797c2f4faab36c6bdcde29ee2a5f69b81b5ec1_

```
    2 |   ed25519 = 'ed25519',
    3 |   secp256k1 = 'ecdsa-secp256k1',
    4 | }
```

_file_excerpt · [packages/xrpl/src/confidential/keys.ts](https://github.com/XRPLF/xrpl.js/blob/126168271b8cbe784baf77fec05d2cd8c1837815/packages/xrpl/src/confidential/keys.ts#L28) · line 28 · SHA-256 32e295c55418d697363fa33a6609e8a96a65876495a9fe794550b60d08ed3a9a_

```
   27 | export function deriveConfidentialKeypair(seed?: string): ConfidentialKeypair {
   28 |   const familySeed = seed ?? generateSeed({ algorithm: ECDSA.secp256k1 })
   29 |   const { publicKey, privateKey } = deriveKeypair(familySeed, {
```

_file_excerpt · [packages/xrpl/src/confidential/keys.ts](https://github.com/XRPLF/xrpl.js/blob/126168271b8cbe784baf77fec05d2cd8c1837815/packages/xrpl/src/confidential/keys.ts#L30) · line 30 · SHA-256 37b1888377a6487efb05999f94a9bebe35e83716ccb24eff5a862ecbef60851a_

```
   29 |   const { publicKey, privateKey } = deriveKeypair(familySeed, {
   30 |     algorithm: ECDSA.secp256k1,
   31 |   })
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it; introduce an abstraction layer for crypto-agility.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-50294 — Quantum-vulnerable RSA key (4096-bit) in packages/ripple-keypairs/SECURITY.md

- Severity: **Low** · Classification: Long-term post-quantum risk · Confidence: High
- Affected asset: `file:packages/ripple-keypairs/SECURITY.md#line 28`
- Data source: packages/ripple-keypairs/SECURITY.md
- Detection method: Public key parsing.
- Analyzer: certificates 1.20.0 · 2026-11-24 12:24 UTC
- Priority score: 37.1 / 100
- CVSS v3.1: not applicable

A RSA 4096-bit public key was found (line 28).

**Potential impact.** Long-term risk once a CRQC exists; for key exchange, recorded traffic could be decrypted retroactively.

**Reproduction steps.**

```
Open line 28 in the supplied file packages/ripple-keypairs/SECURITY.md and inspect the quoted lines (see evidence).
```

**Evidence.**

_key · packages/ripple-keypairs/SECURITY.md · line 28 · SHA-256 18fb5f0b9bd19412cb5c0404d29bd26dc62ba6e0ff99543463ebc0757b50ef09_

```
OpenPGP primary key: algorithm ID 1 (RSA) 4096-bit
```

_key · packages/ripple-keypairs/SECURITY.md · line 28 · SHA-256 484f2172c4dd53b29fd23e321304b308266950550fb37c83431470e8045649f0_

```
OpenPGP subkey: algorithm ID 1 (RSA) 4096-bit
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability.

**Recommendation.** Inventory and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it..

**Retest procedure.** Re-audit after migration.

### QSI-2026-50292 — Quantum-vulnerable EC-ElGamal: key wrapping and data encryption at rest (1 file(s))

- Severity: **Low** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:EC-ElGamal:key_wrapping`
- Data source: packages/mpt-crypto/src/module.ts
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.20.0 · 2026-11-24 12:24 UTC
- Priority score: 27.9 / 100
- CVSS v3.1: not applicable

4 reference(s) to EC-ElGamal across 1 file(s), e.g. packages/mpt-crypto/src/module.ts:21. Role, judged from paths, function names and nearby code: key wrapping and data encryption at rest. Keys or data encrypted to these public keys are stored: anyone who copies them now decrypts them once a CRQC exists (harvest now, decrypt later).

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open packages/mpt-crypto/src/module.ts:21 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [packages/mpt-crypto/src/module.ts](https://github.com/XRPLF/xrpl.js/blob/126168271b8cbe784baf77fec05d2cd8c1837815/packages/mpt-crypto/src/module.ts#L21) · line 21 · SHA-256 39db9614e8eb03ee3884b922f5c476e76cf6462df13096bc896b9db09b089580_

```
   20 |   _mpt_generate_blinding_factor: (outFactor: number) => number
   21 |   _mpt_encrypt_amount: (
   22 |     amount: bigint,
```

_file_excerpt · [packages/mpt-crypto/src/module.ts](https://github.com/XRPLF/xrpl.js/blob/126168271b8cbe784baf77fec05d2cd8c1837815/packages/mpt-crypto/src/module.ts#L27) · line 27 · SHA-256 cbdbe530e2b55b320eb0b504f955d2bcd5ce8dfe8a7ae9f2548d0606255f809a_

```
   26 |   ) => number
   27 |   _mpt_decrypt_amount: (
   28 |     ciphertext: number,
```

_file_excerpt · [packages/mpt-crypto/src/module.ts](https://github.com/XRPLF/xrpl.js/blob/126168271b8cbe784baf77fec05d2cd8c1837815/packages/mpt-crypto/src/module.ts#L109) · line 109 · SHA-256 d03b85eaf371a1806d9ba307815e6c9a5b7a02fc18609f78874d058830ca2ed1_

```
  108 |   // A `secp256k1_pubkey` is a 64-byte opaque struct. Both return 1 on success.
  109 |   _mpt_make_ec_pair: (buffer: number, out1: number, out2: number) => number
  110 |   _mpt_serialize_ec_pair: (in1: number, in2: number, out: number) => number
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Wrap keys with ML-KEM or a hybrid KEM (X25519 + ML-KEM-768) and re-wrap the stored keys; data that may already have been copied needs its own assessment.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-50290 — Quantum-vulnerable EC-ElGamal: role not determined (5 file(s))

- Severity: **Low** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:EC-ElGamal:general`
- Data source: packages/mpt-crypto/src/homomorphic.ts
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.20.0 · 2026-11-24 12:24 UTC
- Priority score: 25.2 / 100
- CVSS v3.1: not applicable

10 reference(s) to EC-ElGamal across 5 file(s), e.g. packages/mpt-crypto/src/homomorphic.ts:51. Role, judged from paths, function names and nearby code: role not determined. The code does not show what the keys protect; review decides the priority.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open packages/mpt-crypto/src/homomorphic.ts:51 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [packages/mpt-crypto/src/homomorphic.ts](https://github.com/XRPLF/xrpl.js/blob/126168271b8cbe784baf77fec05d2cd8c1837815/packages/mpt-crypto/src/homomorphic.ts#L51) · line 51 · SHA-256 5052b2046a45d44bfde31d664276238ba194316260b327712f4493ac2270e813_

```
   50 |     const o2 = marshaller.alloc(PUBKEY_STRUCT_SIZE)
   51 |     if (mod._mpt_make_ec_pair(aPtr, a1, a2) !== WASM_OK) {
   52 |       throw new Error('mpt-crypto: failed to parse ciphertext a')
```

_file_excerpt · [packages/mpt-crypto/src/homomorphic.ts](https://github.com/XRPLF/xrpl.js/blob/126168271b8cbe784baf77fec05d2cd8c1837815/packages/mpt-crypto/src/homomorphic.ts#L54) · line 54 · SHA-256 b5031532f540e1b3067c6a7ae9a60848dab533fadb14f0cef036a50dbb0b8251_

```
   53 |     }
   54 |     if (mod._mpt_make_ec_pair(bPtr, b1, b2) !== WASM_OK) {
   55 |       throw new Error('mpt-crypto: failed to parse ciphertext b')
```

_file_excerpt · [packages/mpt-crypto/src/homomorphic.ts](https://github.com/XRPLF/xrpl.js/blob/126168271b8cbe784baf77fec05d2cd8c1837815/packages/mpt-crypto/src/homomorphic.ts#L65) · line 65 · SHA-256 b133e07edd70a11830096f2cc0f23d76c7455b814315ff0ea01e75c6a7859a5e_

```
   64 |     const outPtr = marshaller.alloc(ELGAMAL_TOTAL_SIZE)
   65 |     if (mod._mpt_serialize_ec_pair(o1, o2, outPtr) !== WASM_OK) {
   66 |       throw new Error('mpt-crypto: failed to serialize combined ciphertext')
```

_file_excerpt · [packages/mpt-crypto/src/primitives.ts](https://github.com/XRPLF/xrpl.js/blob/126168271b8cbe784baf77fec05d2cd8c1837815/packages/mpt-crypto/src/primitives.ts#L66) · line 66 · SHA-256 a446bf9cd313a1fb8da26a2de8eb0a0babe7720889248f4449ef3a148bc3b9e9_

```
   65 |     const outPtr = marshaller.alloc(ELGAMAL_TOTAL_SIZE)
   66 |     if (mod._mpt_encrypt_amount(amount, pubPtr, blindingPtr, outPtr) !== 0) {
   67 |       throw new Error('mpt_encrypt_amount failed')
```

_file_excerpt · [packages/mpt-crypto/src/primitives.ts](https://github.com/XRPLF/xrpl.js/blob/126168271b8cbe784baf77fec05d2cd8c1837815/packages/mpt-crypto/src/primitives.ts#L67) · line 67 · SHA-256 1129c3dec810e80206e77a675f5d82f49ad4642bb3c029e5456b4324bd9b648f_

```
   66 |     if (mod._mpt_encrypt_amount(amount, pubPtr, blindingPtr, outPtr) !== 0) {
   67 |       throw new Error('mpt_encrypt_amount failed')
   68 |     }
```

_file_excerpt · [packages/mpt-crypto/src/primitives.ts](https://github.com/XRPLF/xrpl.js/blob/126168271b8cbe784baf77fec05d2cd8c1837815/packages/mpt-crypto/src/primitives.ts#L103) · line 103 · SHA-256 a880166145740464edf2c5ab4cd423892b9a701f095904270c4f1e89469a02e8_

```
  102 |     if (
  103 |       mod._mpt_decrypt_amount(
  104 |         ctPtr,
```

_file_excerpt · [packages/mpt-crypto/wasm/mpt_crypto.js](https://github.com/XRPLF/xrpl.js/blob/126168271b8cbe784baf77fec05d2cd8c1837815/packages/mpt-crypto/wasm/mpt_crypto.js#L1) · line 1 · SHA-256 beda46149a036ede838fefe450f8ebc0df16a6ceacc5d6bd9f91ddcee15e2c65_

```
    1 | var MptCrypto=(()=>{var _scriptName=globalThis.document?.currentScript?.src;return async function(moduleArg={}){var Module=moduleArg;var ENVIRONMENT_IS_WEB=!!globalThis.window;var ENVIRONMENT_IS_WORKER=!!globalThis.WorkerGlobalScope;var ENVIRONMENT_IS_NODE=globalThis.process?.versions?.node&&globalT
    2 | ;return Module}})();if(typeof exports==="object"&&typeof module==="object"){module.exports=MptCrypto;module.exports.default=MptCrypto}else if(typeof define==="function"&&define["amd"])define([],()=>MptCrypto);
```

_file_excerpt · [packages/mpt-crypto/wasm/mpt_crypto.mjs](https://github.com/XRPLF/xrpl.js/blob/126168271b8cbe784baf77fec05d2cd8c1837815/packages/mpt-crypto/wasm/mpt_crypto.mjs#L1) · line 1 · SHA-256 b452b444f90f48b742052febc8d226744196e6f3cabd5ca015b481bec994a1b0_

```
    1 | async function MptCrypto(moduleArg={}){var Module=moduleArg;var ENVIRONMENT_IS_WEB=!!globalThis.window;var ENVIRONMENT_IS_WORKER=!!globalThis.WorkerGlobalScope;var ENVIRONMENT_IS_NODE=globalThis.process?.versions?.node&&globalThis.process?.type!="renderer";if(ENVIRONMENT_IS_NODE){const{createRequire
    2 | ;return Module}export default MptCrypto;
```

_file_excerpt · [packages/mpt-crypto/wasm/mpt_crypto.web.mjs](https://github.com/XRPLF/xrpl.js/blob/126168271b8cbe784baf77fec05d2cd8c1837815/packages/mpt-crypto/wasm/mpt_crypto.web.mjs#L1) · line 1 · SHA-256 92544b1af8f4256bf82285e006d4043ff7d0f3d06e04aec5d26e4a457a48ab0c_

```
    1 | async function MptCrypto(moduleArg={}){var Module=moduleArg;var ENVIRONMENT_IS_WEB=!!globalThis.window;var ENVIRONMENT_IS_WORKER=!!globalThis.WorkerGlobalScope;var ENVIRONMENT_IS_NODE=globalThis.process?.versions?.node&&globalThis.process?.type!="renderer";var programArgs=[];var thisProgram="./this.
    2 | ;return Module}export default MptCrypto;
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Classify each usage, record data lifetimes, and plan migration to NIST's post-quantum standards cover key encapsulation and signatures; none covers additively homomorphic encryption. Treat amounts encrypted this way as eventually public, and limit what a design must store on-ledger; lattice-based homomorphic schemes are the research direction; introduce an abstraction layer for crypto-agility.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-50297 — 23 advisories in 6 development or build-only npm package(s)

- Severity: **Info** · Classification: Improvement recommendation · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `dependencies:npm:non-runtime`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch lookup of exact versions; scope from devDependencies, package-lock.json dev flags, pnpm importers sections, the Cargo.lock graph rooted at the Cargo.toml tables, and — for yarn.lock, which records no scope — the lock graph walked from package.json. Where a runtime requirement cannot be resolved in a lock, that lock is left unclassified rather than risking a package being set aside wrongly.
- Analyzer: dependencies 1.20.0 · 2026-11-24 12:24 UTC
- Priority score: 13.7 / 100
- CVSS v3.1: not applicable

OSV.dev lists 23 advisories (6 rated high or critical) for 6 npm package(s) that only development or build tooling pulls in (package-lock.json): e.g. glob@10.5.0 [dev]: GHSA-3g3m-2fjr-6pw4; glob@13.0.7 [dev]: GHSA-3g3m-2fjr-6pw4; minimatch@10.2.5 [dev]: GHSA-g3hv-75wg-m249; minimatch@10.2.6 [dev]: GHSA-g3hv-75wg-m249; minimatch@9.0.9 [dev]: GHSA-g3hv-75wg-m249. The manifests mark them as such (devDependencies, "dev": true in package-lock.json, pnpm importers sections, [dev-dependencies]/[build-dependencies] reached through Cargo.lock, or — for yarn.lock, which records no scope at all — package.json reached through the lock graph), so they are not part of what ships.

**Potential impact.** They do not reach users of the product. They can affect developer machines and CI (supply chain): a compromised or vulnerable tool can tamper with builds.

**Reproduction steps.**

```
Look the packages listed in the evidence up at https://osv.dev and check their scope in package-lock.json.
```

**Evidence.**

_tool_output · [OSV.dev (npm)](https://osv.dev/) · package-lock.json · SHA-256 62ba07b0907ef934900081803d218d4e4c02a75ddb2d468c8ea9aaf4ab2afb64_

```
glob@10.5.0 [dev]: GHSA-3g3m-2fjr-6pw4
glob@13.0.7 [dev]: GHSA-3g3m-2fjr-6pw4
minimatch@10.2.5 [dev]: GHSA-g3hv-75wg-m249
minimatch@10.2.6 [dev]: GHSA-g3hv-75wg-m249
minimatch@9.0.9 [dev]: GHSA-g3hv-75wg-m249
undici@7.29.0 [dev]: GHSA-2gqq-gqf2-x968, GHSA-2jfj-6hjv-fm6j, GHSA-2m5v-pch6-74hx, GHSA-3wwx-pv8p-q78v, GHSA-3xpg-4rpp-hhhm, GHSA-4qv8-2p9j-2685, GHSA-4w7w-5xrc-9h26, GHSA-55wc-3pg8-jfw6, GHSA-8436-99hf-9mmv, GHSA-9fm3-97px-rjf6, GHSA-f72v-6w45-q472, GHSA-pmjh-fq2x-6v4x, GHSA-qrxm-fqhp-jwvm, GHSA-r53p-7pc4-xj5r, GHSA-rfgv-xxqx-mfg5, GHSA-rx4f-c7p8-82vq, GHSA-w293-vg96-wgc3, GHSA-xjj6-f33q-929c
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Scopes come from the manifests; a registry crate's own build dependencies cannot be told apart in Cargo.lock, so the runtime set may be larger than reality, never smaller.

**Recommendation.** Update the tooling during routine maintenance; prioritise packages that run in CI with secrets or that produce release artefacts.

**Retest procedure.** Re-run the dependency scan after updating.

### QSI-2026-50296 — No post-quantum capable cryptographic library detected

- Severity: **Info** · Classification: Insufficient data · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `dependencies`
- Data source: dependency manifests
- Detection method: Dependency name matching.
- Analyzer: dependencies 1.20.0 · 2026-11-24 12:24 UTC
- Priority score: 12.2 / 100
- CVSS v3.1: not applicable

Across 14 dependency manifests, QSI found crypto libraries (@noble/curves, @noble/hashes, @xrplf/mpt-crypto, ripple-keypairs, xrpl) but none from its PQC-capable list.

**Potential impact.** Readiness indicator only: PQC support may come from the platform (OpenSSL, OS, cloud KMS) rather than application dependencies.

**Reproduction steps.**

```
Review the dependency manifests listed in the evidence.
```

**Evidence.**

_dependency · package-lock.json, package.json, packages/isomorphic/package.json, packages/isomorphic/ripemd160/package.json, packages/isomorphic/sha256/package.json, packages/isomorphic/sha512/package.json, packages/isomorphic/utils/package.json, packages/isomorphic/ws/package.json, packages/mpt-crypto/package.json, packages/ripple-address-codec/package.json, packages/ripple-binary-codec/package.json, packages/ripple-keypairs/package.json, packages/secret-numbers/package.json, packages/xrpl/package.json · SHA-256 1586510d5ea94b68b5494769ddaf63737891452f40b45675043ce7dad8633c9b_

```
Crypto libraries: @noble/curves, @noble/hashes, @xrplf/mpt-crypto, ripple-keypairs, xrpl
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

- Classical only — key wrapping and data encryption at rest: EC-ElGamal (1 file(s))
- Classical only — threshold signing and MPC protocols: Pedersen commitment (8 file(s))

**Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

_Levels: 0 none; 1 present, not wired; 2 in use outside the critical paths; 3 hybrid in a critical path; 4 post-quantum by default in the critical paths (root of trust, key wrapping, channel key exchange). Judged from code and manifests._

### What the quantum-vulnerable algorithms do

| Role | Algorithms (files) | ID | First step |
|---|---|---|---|
| **key wrapping and data encryption at rest** | EC-ElGamal (1) | QSI-2026-50292 | Wrap keys with ML-KEM or a hybrid KEM (X25519 + ML-KEM-768) and re-wrap the stored keys; data that may already have been copied needs its own assessment |
| **threshold signing and MPC protocols** | Pedersen commitment (8) | QSI-2026-50291 | Track post-quantum threshold signatures (NIST IR 8214C) and keep the protocol layer ready to swap the signature scheme; record which keys and shares must stay valid for how long |
| **transaction and message signing** | ECDSA (8), Ed25519 (1) | QSI-2026-50293, QSI-2026-50295 | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains adopt them |
| **role not determined** | EC-ElGamal (5), ECDSA (4) | QSI-2026-50289, QSI-2026-50290 | Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it; introduce an abstraction layer for crypto-agility |

_Roles are judged from file paths, function names and the code around each match; review confirms them. Root-of-trust keys and wrapped keys come first: they are hard to replace or can be recorded today._
No readiness questionnaire was completed for this project.

### Quantum algorithms relevant to this inventory

| Quantum algorithm | Effect | Attack model | Inventoried algorithms (rows) | What it means for this audit |
|---|---|---|---|---|
| Shor's algorithm — factoring | breaks | Q1 | RSA (2) | Breaks RSA at every key length: a longer modulus only raises the cost polynomially. Plan migration to ML-KEM (or a hybrid) for key establishment and ML-DSA / SLH-DSA for signatures; start with keys protecting data that must stay confidential for years (harvest now, decrypt later) and with long-lived signatures. |
| Shor's algorithm — elliptic-curve discrete logarithms | breaks | Q1 | EC-ElGamal (6), ECDSA (12), Ed25519 (1), Pedersen commitment (8) | Elliptic-curve keys are expected to fall before RSA keys of comparable classical strength. On blockchains, coins whose public key is already on chain (reused addresses, pay-to-public-key and Taproot outputs) are exposed first; plan the move to post-quantum signatures and avoid key reuse in the meantime. |
| Grover's algorithm — key search and preimages | weakens (larger keys restore the margin) | Q1 | SHA-2 (1) | Not a break. 256-bit keys (AES-256, ChaCha20) keep a comfortable margin; AES-128 meets NIST category 1, while some authorities ask for 256-bit keys in quantum-resistant contexts (see the AES-128 entry). Prefer 256-bit keys for long-lived data; 256-bit hashes need no change for preimage resistance. |
| Brassard–Høyer–Tapp — collision search | weakens (larger keys restore the margin) | Q1 | SHA-2 (1) | 256-bit hashes (SHA-256, SHA3-256) remain adequate for collision resistance; 160-bit hashes are already weak classically (SHA-1 collisions are practical). Use 384/512-bit hashes where NIST categories 4–5 are required. |

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
| P3 | QSI-2026-50291 | Add Pedersen commitment usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-50293 | Add ECDSA usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-50295 | Add Ed25519 usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-50289 | Add ECDSA usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-50294 | Add RSA usages at file:packages/ripple-keypairs/SECURITY.md to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-50292 | Add EC-ElGamal usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-50290 | Add EC-ElGamal usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P4 | QSI-2026-50291 | Plan migration of Pedersen commitment to  (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows  or a hybrid scheme in use. |
| P4 | QSI-2026-50293 | Plan migration of ECDSA to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-50295 | Plan migration of Ed25519 to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-50289 | Plan migration of ECDSA to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-50294 | Plan migration of RSA to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. or a hybrid scheme in use. |
| P4 | QSI-2026-50292 | Plan migration of EC-ElGamal to NIST's post-quantum standards cover key encapsulation and signatures; none covers additively homomorphic encryption. Treat amounts encrypted this way as eventually public, and limit what a design must store on-ledger; lattice-based homomorphic schemes are the research direction (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows NIST's post-quantum standards cover key encapsulation and signatures; none covers additively homomorphic encryption. Treat amounts encrypted this way as eventually public, and limit what a design must store on-ledger; lattice-based homomorphic schemes are the research direction or a hybrid scheme in use. |
| P4 | QSI-2026-50290 | Plan migration of EC-ElGamal to NIST's post-quantum standards cover key encapsulation and signatures; none covers additively homomorphic encryption. Treat amounts encrypted this way as eventually public, and limit what a design must store on-ledger; lattice-based homomorphic schemes are the research direction (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows NIST's post-quantum standards cover key encapsulation and signatures; none covers additively homomorphic encryption. Treat amounts encrypted this way as eventually public, and limit what a design must store on-ledger; lattice-based homomorphic schemes are the research direction or a hybrid scheme in use. |
| P4 | QSI-2026-50297 | Update the development and build dependencies listed in the evidence. | root-cause fix | The dependency scan reports no advisories for tooling packages, or the remaining ones are recorded. |

## 11. Tools used

- blockchain 1.0.0
- certificates 1.2.0
- chain_map 1.0.0
- configs 1.1.0
- crediting 1.4.0
- dependencies 1.6.0
- hndl 1.0.0
- inventory_document 1.1.0
- key_storage 1.0.0
- mpc 1.0.0
- solidity 1.8.1
- source_code 1.11.0
- tls_code 1.1.0
- tls_live 1.0.0
- ton_contracts 1.0.0
- validator_keys 1.2.0
- wallet_login 1.0.0
- qsi-engine 1.20.0
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
21. OSV.dev — open-source vulnerability database and API — Open Source Security Foundation. <https://osv.dev/> (the database QSI queries for each exactly pinned version; every advisory id in a finding resolves at https://osv.dev/vulnerability/<id>)
22. P. W. Shor — Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms on a Quantum Computer (SIAM J. Comput., 1997) — SIAM. <https://doi.org/10.1137/S0097539795293172> (peer-reviewed article)
23. R. Babbush et al. — Securing Elliptic Curve Cryptocurrencies against Quantum Vulnerabilities: Resource Estimates and Mitigations (arXiv:2603.28846) — arXiv. <https://arxiv.org/abs/2603.28846> (preprint (2026-03-30, v2 2026-04-15): 256-bit ECDLP with < 1200 logical qubits and < 90 M Toffoli gates (or < 1450 and < 70 M); < 500,000 physical qubits at 10^-3 error, minutes)
24. S. Jaques, M. Naehrig, M. Roetteler, F. Virdia — Implementing Grover oracles for quantum key search on AES and LowMC (EUROCRYPT 2020; arXiv:1910.01700) — Springer / arXiv. <https://arxiv.org/abs/1910.01700> (peer-reviewed article: lower cost estimates for the AES key searches that define the NIST categories)

## Appendices: Cryptographic inventory

By origin: dependency manifests 14 (0 Shor-breakable) · own code 28 (27 Shor-breakable) · third-party code in the tree 2 (2 Shor-breakable).

| Algorithm | Parameter | Library | Quantum status | Classical status | Count | Locations | Examples |
|---|---|---|---|---|---|---|---|
| SHA-2 | SHA-512 |  | reduced margin (Grover), approved | acceptable | 1 | 1 | packages/ripple-keypairs/src/utils/Sha512.ts |
| Crypto library | 0.1.1 | @xrplf/mpt-crypto (xrpl.js) | n/a | acceptable | 1 | 1 | package-lock.json |
| Crypto library | 2.0.0 | ripple-keypairs (xrpl.js) | n/a | acceptable | 1 | 1 | package-lock.json |
| Crypto library | 2.4.0 | @noble/curves (noble-curves) | n/a | acceptable | 1 | 1 | package-lock.json |
| Crypto library | 2.4.0 | @noble/hashes (noble-hashes) | n/a | acceptable | 1 | 1 | package-lock.json |
| Crypto library | unpinned | xrpl (xrpl.js) | n/a | acceptable | 1 | 1 | package-lock.json |
| Crypto library | unpinned | ripple-keypairs (xrpl.js) | n/a | acceptable | 1 | 1 | package-lock.json |
| Crypto library | unpinned | @xrplf/mpt-crypto (xrpl.js) | n/a | acceptable | 1 | 1 | package-lock.json |
| Crypto library | file:packages/ripple-keypairs | ripple-keypairs (xrpl.js) | n/a | acceptable | 1 | 1 | package.json |
| Crypto library | file:packages/xrpl | xrpl (xrpl.js) | n/a | acceptable | 1 | 1 | package.json |
| Crypto library | ^2.2.0 | @noble/hashes (noble-hashes) | n/a | acceptable | 1 | 1 | packages/isomorphic/package.json |
| Crypto library | ^2.2.0 | @noble/curves (noble-curves) | n/a | acceptable | 1 | 1 | packages/ripple-keypairs/package.json |
| Crypto library | ^3.0.0 | ripple-keypairs (xrpl.js) | n/a | acceptable | 1 | 1 | packages/secret-numbers/package.json |
| Crypto library | ^0.1.1 | @xrplf/mpt-crypto (xrpl.js) | n/a | acceptable | 1 | 1 | packages/xrpl/package.json |
| Crypto library | ^3.1.0 | ripple-keypairs (xrpl.js) | n/a | acceptable | 1 | 1 | packages/xrpl/package.json |
| EC-ElGamal |  |  | vulnerable (Shor) | acceptable | 6 | 6 | packages/mpt-crypto/src/homomorphic.ts:51; packages/mpt-crypto/src/module.ts:21; packages/mpt-crypto/src/primitives.ts:66 |
| ECDSA | secp256k1 |  | vulnerable (Shor) | acceptable | 12 | 12 | packages/mpt-crypto/src/homomorphic.ts:40; packages/mpt-crypto/src/module.ts:162; packages/ripple-address-codec/src/xrp-codec.ts:49 |
| Ed25519 | Ed25519 |  | vulnerable (Shor) | acceptable | 1 | 1 | packages/ripple-keypairs/src/signing-schemes/ed25519/index.ts:1 |
| Pedersen commitment |  |  | vulnerable (Shor) | acceptable | 8 | 8 | packages/mpt-crypto/src/index.ts:34; packages/mpt-crypto/src/module.ts:34; packages/mpt-crypto/src/primitives.ts:125 |
| RSA | 4096-bit |  | vulnerable (Shor) | acceptable | 2 | 2 | packages/ripple-keypairs/SECURITY.md (line 28) |

_Long lists are grouped here; the full per-file list is in the JSON report, signed with the same key._

## Appendices: Input files

| File | Size | SHA-256 | Redactions |
|---|---|---|---|
| .ci-config/getNewAmendments.js | 1524 | `94673b67dba26e8f74f157b6ef0942c0f1a398cb1b7be5e902678a90c5e1f1bf` | 0 |
| docs/assets/hierarchy.js | 3605 | `52b71d4b6fed5962044c5324a4991b69e7aa7d1c295ab310950e3bff70b3ed51` | 0 |
| docs/assets/icons.js | 12929 | `f1cc7f305cc1acc9642e6681a33f4f7a094e9b32b50790bc3ba22578f2c1e370` | 0 |
| docs/assets/main.js | 48653 | `e7e78b80ea92f2ac7a892b8d7fa6d2d51991776bb77982ca5f99f20f65e0b75d` | 0 |
| docs/assets/navigation.js | 5022 | `2af8b6d13267e995476d550df5ba5ad94375d5fab41d9506dc018d87417af638` | 0 |
| docs/assets/search.js | 104143 | `cecbeebd760789a311166ba48279e5d4fbf6e8bf7458d93809fa9e286627b5aa` | 0 |
| jest.config.base.js | 2039 | `2578542fbca593a38c783f55cdadf82fdb02e18fcc6471813064b4d47c853e1a` | 0 |
| jest.config.js | 209 | `ea4f442536705e2fb74c8c7b4d7c37ec68850a955a9958cd96f11992f3c1a3d8` | 0 |
| karma.config.js | 806 | `d0c9b74a9bc0562d7417e7195e2528959787eae0587b331590fcf0fe16f6ac8a` | 0 |
| package-lock.json | 644736 | `ca1c0d3910aa8ae91141086c687a3e6b40bd2094c5a4f195d3e444be97e30b31` | 0 |
| package.json | 2395 | `3810da955a8ed4da62b041f3c0c7e5864d4f9f312d37f68fcd2bedf9aa9d4f0a` | 0 |
| packages/isomorphic/eslint.config.js | 3190 | `3d19c891eb1901e4d386c607282961a217ea0c50ac15429e42b28fd24ed397fe` | 0 |
| packages/isomorphic/jest.config.js | 193 | `1663a33965bf58b738d2d21fad551eb0156bc64e794c546acac42b07b5fb874e` | 0 |
| packages/isomorphic/karma.config.js | 355 | `af0e416793369bf0b525676c588aa576e6d0bfb9a29204cdd056752e61895099` | 0 |
| packages/isomorphic/package.json | 1176 | `23e218c60efa7c258ecf003b211f95499db1b486d21ed9a97c387c10f78e07ce` | 0 |
| packages/isomorphic/ripemd160/package.json | 171 | `86aeff2760127d84f71c4917efbea45da1533e64927e1c4b0aff07a5233921e3` | 0 |
| packages/isomorphic/sha256/package.json | 159 | `d50ee9090f50120f06caf448bf922cd9be805509d3a7514da7039cee789d51b8` | 0 |
| packages/isomorphic/sha512/package.json | 159 | `12bf587ae6070114360a77ba57e1446e18f7a0f28311e9863a0e4df62390111e` | 0 |
| packages/isomorphic/src/internal/normalizeInput.ts | 484 | `c13bf2e80ab297c06e9f677f56d10d28c7f356e5effe2faf1ecde1d29d215fa0` | 0 |
| packages/isomorphic/src/internal/types.ts | 848 | `3128600da2b84fe60a251949a3dbe7a73f1fba3968ce245b34ea169422cdcea8` | 0 |
| packages/isomorphic/src/internal/wrapCryptoCreateHash.ts | 770 | `2777f0ffc070ad726b7563fe956a12571809276febf70d56598619f385d028f9` | 0 |
| packages/isomorphic/src/internal/wrapNoble.ts | 714 | `f42da67776568566ffd8dff221e3513a7344c0c1ed6402a56b0345da410646e2` | 0 |
| packages/isomorphic/src/ripemd160/browser.ts | 223 | `d0ccb4d69a053d7cb278ed0bfa0b7444508b3601b7cb90276b574c239bd4fa65` | 0 |
| packages/isomorphic/src/ripemd160/index.ts | 241 | `75e9ad73e6278c3be6df322d73972f68a6fcb11b8cf00d2b1ddb7f570787b91b` | 0 |
| packages/isomorphic/src/sha256/browser.ts | 212 | `fb3d3f99f215174aacfce00c6c9ac86348f3903c7d83d5541597317f5cc17d54` | 0 |
| packages/isomorphic/src/sha256/index.ts | 232 | `bc3c08b5757e634234006ba21b4b6350167d9ea49b3765926b2a0d5ec9f7db65` | 0 |
| packages/isomorphic/src/sha512/browser.ts | 212 | `398bd5aa57def27594ac4404e7ee9ac9a3176741ee8131fc9fbfd19e62996649` | 0 |
| packages/isomorphic/src/sha512/index.ts | 232 | `1cd2f87f1a4955b43b2c04cd48d73a1aac0bd4979a833e95ef41004544017bb9` | 0 |
| packages/isomorphic/src/utils/browser.ts | 1591 | `639aec404bd864f48c74cafdd68b6ac7f307dc42cb708fbaf55408b3472394c0` | 0 |
| packages/isomorphic/src/utils/index.ts | 3663 | `2711bb84cc2f9d3a4b23dc325b74e683e720a4a5d8338e296e41a729b5525fe1` | 0 |
| packages/isomorphic/src/utils/shared.ts | 513 | `e501c1812ad1734aa3a306df75a5d2efc388a9eb875ddb58cbceb9548b0c8419` | 0 |
| packages/isomorphic/src/utils/types.ts | 1116 | `944c8c06c246354edfeec806bb2c8184101239a22b293ec94218ff8799f3c98e` | 0 |
| packages/isomorphic/src/ws/browser.ts | 2581 | `99d04defcaf0ae6d4eeca015b6aae82d34a5a77cbfc9bd03c90505ddbe09a2d0` | 0 |
| packages/isomorphic/src/ws/index.ts | 232 | `d4cf6975d99470e38e92bb44f9544ccb58247dea7074b81a131096ecf54eea1d` | 0 |
| packages/isomorphic/utils/package.json | 155 | `c10bd97c7e742e071abab2808d8e89f21543df9bd7c695249479519fae5b2837` | 0 |
| packages/isomorphic/ws/package.json | 219 | `aab20052b54b2edc0d7836bc7ebc4928c7f203dfbc4762ac1ab389b54376b979` | 0 |
| packages/mpt-crypto/eslint.config.js | 1983 | `3159c4d5ab367dc6dd262f2719e86a26fd0b0938386295a61695f8e642514604` | 0 |
| packages/mpt-crypto/jest.config.js | 193 | `690c41e74d808ab4ec1cd8149d909e562a2f88ac98c605d5e1875a624fe9c580` | 0 |
| packages/mpt-crypto/package.json | 1622 | `e0642f001f18f656f4d1139811db8b53f23b256dde9f72d512dc3af0d11ee598` | 0 |
| packages/mpt-crypto/scripts/finalize-esm.js | 1345 | `74e3866bc5c6d6d8f001b568580fb59c96514a8dd8ffc7e1f684b3adadb45c0e` | 0 |
| packages/mpt-crypto/src/constants.ts | 2165 | `192df5550eda5b2d2c2e59260ff0f74f3cdb1ea0dff064c8b47e3bd7843ef4c3` | 0 |
| packages/mpt-crypto/src/context.ts | 5448 | `d2ec383d92642caf46a06508957729de19e8b224267f5e0da4201a49cb0437d5` | 0 |
| packages/mpt-crypto/src/hex.ts | 1571 | `841c4648d8dba5de8adcc8084339996d42b92d5f6b21d695446cd0df2559a606` | 0 |
| packages/mpt-crypto/src/homomorphic.ts | 4076 | `dd57886cbb24e738a7159e1c94321c13369e3a58b73e0a807a94662f044f8925` | 0 |
| packages/mpt-crypto/src/index.ts | 1370 | `9692cfe48da2edff902b4649324e1833c031f5e54d9eb49d37c1162cf129d898` | 0 |
| packages/mpt-crypto/src/internal.ts | 3776 | `4b77249cb4111b2c443a3298bf974f311fa4a6280bcd825fe6b5962b2a909936` | 0 |
| packages/mpt-crypto/src/marshal.ts | 4865 | `ca1af2087813716f5022dded9b31e69cae73d510f2d50d1dc63d176d58fefb79` | 0 |
| packages/mpt-crypto/src/module.ts | 7327 | `b33902e3c655bae56b8b9164d5b28e6ed66b74001029f314561f41abbb9d47b7` | 0 |
| packages/mpt-crypto/src/primitives.ts | 4986 | `f8582f32a0b8f321fd561c0dddc50c49f6b4f56e7e3b51150f412e7dd6ff9aea` | 0 |
| packages/mpt-crypto/src/proofs.ts | 7979 | `bb952207a07c46683106de57c4b9014a517e39031a31a2fc96b2b9fa1b46db18` | 0 |
| packages/mpt-crypto/src/runtime.ts | 854 | `3f4f11024a8cdda842fecb771489a4fced87182e093e28884283e7462e0d430f` | 0 |
| packages/mpt-crypto/src/types.ts | 1783 | `71fc165ba81d175b46633d2ee06219e85880ed30445a76cc4c9a31ff168fa464` | 0 |
| packages/mpt-crypto/src/wasm.d.ts | 532 | `eabdaac42a53af93328ef7c7190258abb894523b8842d3541c78981f9b8fe533` | 0 |
| packages/mpt-crypto/wasm/mpt_crypto.js | 64186 | `2d568a94344685d53712593678230f56696f1483f5e5859a32ce266c10fc8af2` | 0 |
| packages/mpt-crypto/wasm/mpt_crypto.mjs | 64211 | `8ae3ad22a8c706ffec63d5d90066d5a2379d3c8f449da8537b05d9e66ab67a1b` | 0 |
| packages/mpt-crypto/wasm/mpt_crypto.wasm | 2110544 | `68ddb99a0e70f99d88bbf82ba135e8a8f75817a630d774f1f5798e8c37ff6c86` | 0 |
| packages/mpt-crypto/wasm/mpt_crypto.web.mjs | 63138 | `d3a8aad8ce2547e6b17c8ef1abd13c69eda8ae7b77f89ce602adbdcb1efbac4d` | 0 |
| packages/ripple-address-codec/eslint.config.js | 1710 | `e99e74e79a969d5c7b2ca9cdeb0b277df2b76a46bf8240ec5b7f2d808996f55a` | 0 |
| packages/ripple-address-codec/jest.config.js | 196 | `ef3620efe0b1c4e289ab31b378c98dc49e103627fc8f2da9311de4c27b92edcd` | 0 |
| packages/ripple-address-codec/karma.config.js | 355 | `af0e416793369bf0b525676c588aa576e6d0bfb9a29204cdd056752e61895099` | 0 |
| packages/ripple-address-codec/package.json | 995 | `2c4e6e11ec2810408651034e85f00ba1538bc6e778a39fdfebbb344de156cc08` | 0 |
| packages/ripple-address-codec/src/index.ts | 4916 | `0992667f68f2d23dbdea31bc5ce32980fd6ea973d0ff071d9ef9e64fd899fd9d` | 0 |
| packages/ripple-address-codec/src/utils.ts | 1336 | `0e9a8c0341f075764ff285e8abc876331fd4c34821a93ca6e2d14ab35eac0109` | 0 |
| packages/ripple-address-codec/src/xrp-codec.ts | 7572 | `dcb66f9db95d69491b00beb47d6da7e5545ac5c77f15b901a804b70c2349f951` | 0 |
| packages/ripple-binary-codec/eslint.config.js | 5121 | `14ca414331dd631ef664cf3d66dd81193621099968903960fea560643be44b18` | 0 |
| packages/ripple-binary-codec/jest.config.js | 195 | `324949fee02870fcb5b8c7c6a471e9c9c475fd537dbd2f06074fa0215da84487` | 0 |
| packages/ripple-binary-codec/karma.config.js | 355 | `af0e416793369bf0b525676c588aa576e6d0bfb9a29204cdd056752e61895099` | 0 |
| packages/ripple-binary-codec/package.json | 1312 | `c3ba692f162ccadd7c15de949a95be0684866e7650287edaafc688ba7f4027c7` | 0 |
| packages/ripple-binary-codec/src/binary.ts | 8260 | `1d651103171427e4609fcf426e948688f0cf5d1605f5f60d6fff3824c6319649` | 0 |
| packages/ripple-binary-codec/src/coretypes.ts | 582 | `936a5e0f0f6320c33e62f413de10cdd2e478e5f7c9a1738e36005a21ddb0978e` | 0 |
| packages/ripple-binary-codec/src/enums/bytes.ts | 2107 | `65088bc560f2a27062cdde5346c54538b199e035c7328b7a2a9b0c29676a223e` | 0 |
| packages/ripple-binary-codec/src/enums/constants.ts | 242 | `9bc3ebb825b935585ad281d9b4eba3915726a556c7859b6d50a4b93671380d4a` | 0 |
| packages/ripple-binary-codec/src/enums/field.ts | 2324 | `d2fb9f38d1d6c3da6b3003b1361b112f44bb8c9f68d281c81974ab213841f8e4` | 0 |
| packages/ripple-binary-codec/src/enums/index.ts | 876 | `61fe6cca16b56849c7b89683ef1210c99d917595a64678ebef7e6afafdf9a907` | 0 |
| packages/ripple-binary-codec/src/enums/utils-renumber.ts | 3148 | `73ab9c318b7ff1f4f7fca6f9516c12f0b431ee1f0abec5f330cf8e0dc7b62404` | 0 |
| packages/ripple-binary-codec/src/enums/xrpl-definitions-base.ts | 5952 | `ccd61ecc18fe77cea5cb937d3a54357d55099dcc05797f070f685d7334c974ae` | 0 |
| packages/ripple-binary-codec/src/enums/xrpl-definitions.ts | 1407 | `0d18086de88431a1b6b496aa2732c5a3936d9d5e9f9e59b5ea4e2e1b3a3b76d6` | 0 |
| packages/ripple-binary-codec/src/hash-prefixes.ts | 1612 | `6c9ae8875152e44ce6ed8f586f79a8c7c8d582f3c9de70b7075f89ff02579abe` | 0 |
| packages/ripple-binary-codec/src/hashes.ts | 1821 | `8a5668ceccf6ee90073c2c27a894bae967a03e20865ee6c431e3cd0671168b66` | 0 |
| packages/ripple-binary-codec/src/index.ts | 7461 | `83b2712fdd6916b9f27247acd3d19ffe677a8aba6861b363dc9f0e3396a8f09d` | 0 |
| packages/ripple-binary-codec/src/ledger-hashes.ts | 5530 | `9e014f13e0748b16e15ff821c48a51ad7428255aeaea9264f2f844c43101c9e6` | 0 |
| packages/ripple-binary-codec/src/quality.ts | 1309 | `9880ce090eee36274d944c1e2e38ad269a9e20145101d71e83c9ca96289e797c` | 0 |
| packages/ripple-binary-codec/src/serdes/binary-parser.ts | 5885 | `f4a37aae59cb27ad1cd5535c95428cd684a9588cb4198b02df8185e9407b9980` | 0 |
| packages/ripple-binary-codec/src/serdes/binary-serializer.ts | 4105 | `796a1e17ebe8fb526a7a92e6c72bff808cfb84601aae8625fd0821c5e6e3a7cc` | 0 |
| packages/ripple-binary-codec/src/shamap.ts | 4457 | `fc47814ce72ecdc678b458e100a62d63df17f597eaf0625d62d034a2a6709ee3` | 0 |
| packages/ripple-binary-codec/src/types/account-id.ts | 2015 | `9063463ef0d1d70ff95ab0ca804f25942988d04846e8ea4dd7b22950daaec200` | 0 |
| packages/ripple-binary-codec/src/types/amount.ts | 10119 | `3fd703eb2d1d38764cb4d9a7955fd8232305266df6fba61fe907e36cf7273e14` | 0 |
| packages/ripple-binary-codec/src/types/blob.ts | 1202 | `13e22fc6268cb572d2fbaea7ad13c678f9f3d3c407143b08cb0ada4b250d1603` | 0 |
| packages/ripple-binary-codec/src/types/currency.ts | 3344 | `dde4f08de034752ab16061517965314f1dd8b4c839ad259021fef9aacd59ac89` | 0 |
| packages/ripple-binary-codec/src/types/hash-128.ts | 705 | `02cf0a03de7419da08b4d416e1440861ef87033d521d218ab7d1c8c22d7b28dd` | 0 |
| packages/ripple-binary-codec/src/types/hash-160.ts | 396 | `287a2068e2cb46545047f64191270017c79618f7c79b4cd3f69b78987ff9a6a0` | 0 |
| packages/ripple-binary-codec/src/types/hash-192.ts | 396 | `dbc2395b5d87def922c8db17e1166a65696ac0ecfb1ad013a8c998d10cfb26a8` | 0 |
| packages/ripple-binary-codec/src/types/hash-256.ts | 307 | `937a63a382e26717d68ae906bf92ed42f1d47b1c1eda43de5faed9df1f023d92` | 0 |
| packages/ripple-binary-codec/src/types/hash.ts | 2163 | `8bd6bdaea6e96659ff52883d8a0181c04174d1b5cf90d509f039edda531c0c13` | 0 |
| packages/ripple-binary-codec/src/types/index.ts | 1743 | `c04cb187ee1148f31d9780aa7e67236eb28567f223b263d39a157d8a051b0e50` | 0 |
| packages/ripple-binary-codec/src/types/int-32.ts | 2007 | `e7ea7e29064e28ca09094eb796b81f47d6ec93957184d960dd459ecfd4a9fd46` | 0 |
| packages/ripple-binary-codec/src/types/int.ts | 1921 | `9bd2c1cf0909c6a8c18ba95c9da22a1de33fbf5427e0f9992864d0c11c3c3f15` | 0 |
| packages/ripple-binary-codec/src/types/issue.ts | 4610 | `bbd646b8291ea22f687a88b709414d5945b76788278dbe62e130191e7d83c76e` | 0 |
| packages/ripple-binary-codec/src/types/path-set.ts | 6868 | `3b6e18ee0274def1bd427a7d2a1db116ffc20edfee0d2b901911f05b016f9538` | 0 |
| packages/ripple-binary-codec/src/types/serialized-type.ts | 3345 | `c037dc612051944592c56d152a3531406d1f3e0b77a173dffcafe83279a236c3` | 0 |
| packages/ripple-binary-codec/src/types/signed-amount.ts | 3174 | `1e08b480d721abd66707666b4ecf0fc7f89b14309e1339a933a476b71884c3d6` | 0 |
| packages/ripple-binary-codec/src/types/st-array.ts | 2967 | `6ec637292591601f421893c6007c176548e1cd4681b647a9b7d405126c0ba872` | 0 |
| packages/ripple-binary-codec/src/types/st-number.ts | 10742 | `758038ac8c9691854d47a4159f84e775789e01c58d2f059c0b9036eb3a499dfc` | 0 |
| packages/ripple-binary-codec/src/types/st-object.ts | 6683 | `743b846e139ac12325307eb26317184e996d6d424b6f4c283366d654f737136a` | 0 |
| packages/ripple-binary-codec/src/types/uint-16.ts | 1291 | `dbab4cf2c8ac88aa9607326d1a7fa9421a9ff4aade952cfa9fb05cb3384657c6` | 0 |
| packages/ripple-binary-codec/src/types/uint-32.ts | 1449 | `193cdd01c81865931022cf75107bc87a89cd7502e2933f60a69e8ec13e333ec2` | 0 |
| packages/ripple-binary-codec/src/types/uint-64.ts | 3588 | `71a59175e1ff398c9cbeaaf7f1217af1c4c131393b9269b1108fbe82a14fa7f0` | 0 |
| packages/ripple-binary-codec/src/types/uint-8.ts | 1290 | `ca083a285ebfd11de62168d24909c3866318b6d6c0d8c1db21fe59edd26ff012` | 0 |
| packages/ripple-binary-codec/src/types/uint.ts | 1479 | `af3b0e1bab1ce16b081ea585356e723380e36ac5b728e0b8a33458d65c1042a7` | 0 |
| packages/ripple-binary-codec/src/types/vector-256.ts | 2211 | `ce77d246a17eaab891098ed0129d62a8e7156c4cc5c72cc57951b7d464e0e5cf` | 0 |
| packages/ripple-binary-codec/src/types/xchain-bridge.ts | 3474 | `368efaa19034f7e3b628a6377dbe421948641c945f0956f13b6d063ef99f81d4` | 0 |
| packages/ripple-binary-codec/src/utils.ts | 6473 | `712908a01355d3dc9c582001de0b7e755ffb8348764e2f9148c374d81972ec55` | 0 |
| packages/ripple-binary-codec/tools/generateDefinitions.js | 10968 | `f76cb7e7331570f2914ed351b72fa4da6affcb85667218dd661c77df6e233f48` | 0 |
| packages/ripple-keypairs/SECURITY.md | 5086 | `3570584b3f97cba7d811ee8256c133fb9d532b6d1d9066160152f64e91a8838b` | 0 |
| packages/ripple-keypairs/eslint.config.js | 2761 | `313d21eb15092a381945060f06b4533162d2444f49079f42a724664d56e1da91` | 0 |
| packages/ripple-keypairs/jest.config.js | 191 | `9710fcf7c7c3befc844ff747988efda55b7b44a9cd4e5985617568fed0b27461` | 0 |
| packages/ripple-keypairs/karma.config.js | 355 | `af0e416793369bf0b525676c588aa576e6d0bfb9a29204cdd056752e61895099` | 0 |
| packages/ripple-keypairs/package.json | 1000 | `adb4338350af6cb5190b6217738ed3688750fffb92e8be65243bde7092dae65c` | 0 |
| packages/ripple-keypairs/src/index.ts | 4765 | `319b2a16df95930e926a4c33799f2ef1a0c3e382c337ba11f5b5075621e2e497` | 0 |
| packages/ripple-keypairs/src/signing-schemes/ed25519/index.ts | 1833 | `feed31ab6fd2da0fc165db76c54ea56c90e44917dfa8899723dbef0ee459c04f` | 0 |
| packages/ripple-keypairs/src/signing-schemes/secp256k1/index.ts | 2259 | `9fb40db24a6ff49e8fb2609d0528cb06cf05e28a3bb26488d1a9b9eae59895e5` | 0 |
| packages/ripple-keypairs/src/signing-schemes/secp256k1/utils.ts | 2844 | `f9016d3e40bac72e6093ae8b5e1b960ac99c617109ff1d6f6202372fed2553ce` | 0 |
| packages/ripple-keypairs/src/types.ts | 845 | `c045e382a4cea1d106ba667513b239a43a16fde8d5cdddef0a87f356d43630aa` | 0 |
| packages/ripple-keypairs/src/utils/Sha512.ts | 769 | `54ff3591cd7645f7fa2e393058cfe0a2ae9ea5524404a784ee456d965a41f959` | 0 |
| packages/ripple-keypairs/src/utils/assert.ts | 226 | `a49e8475f1c7abceacc87bb43038bbc690ea4603d8463b35b954a71d9130004d` | 0 |
| packages/ripple-keypairs/src/utils/getAlgorithmFromKey.ts | 4357 | `1696ed5936607bd99f6607ec99e8863d30dca81ab8ad8821dfcbd706327630a6` | 0 |
| packages/secret-numbers/eslint.config.js | 1732 | `a48e94a1a66e9775bc77d6c443cf60695c5e15fb17221a2221f7f9a712df90a4` | 0 |
| packages/secret-numbers/jest.config.js | 199 | `b26315b4aedc3528487a1ad6de34292e302441ad22a593aa54c81acfda18170e` | 0 |
| packages/secret-numbers/karma.config.js | 384 | `64059a44129e07374a91244a97caa48fc45710156bd9bda6bf886de1e2c61c91` | 0 |
| packages/secret-numbers/package.json | 1458 | `3b56757456d5777b3e01f6c8755f461ddbfbb0c1079facae2a435d433d7a4728` | 0 |
| packages/secret-numbers/src/index.ts | 57 | `86f5fc2945827f3b199949c7c0041f59a3adb913c121ac3c5159a42e3694e461` | 0 |
| packages/secret-numbers/src/schema/Account.ts | 2744 | `3f7f777d988cadd4c8206a1876a8e8714fe63c9ae03c96eaa94680a09c1ccce5` | 0 |
| packages/secret-numbers/src/utils/index.ts | 2560 | `f64203ad97a5c89d82c84017008437a1cfc56c3c0f20d7542f9b3962ca366124` | 0 |
| packages/secret-numbers/webpack.base.config.js | 444 | `ba3ef4e5bdd27ad2e5c41ef88b77209e3c3e06bbd22a77f32fb62c7a0f7f184c` | 0 |
| packages/secret-numbers/webpack.config.js | 283 | `cbf90f8ffbe766da785475013e8cd4706af2d551a18ff1e4777abe6288dbc2cc` | 0 |
| packages/xrpl/eslint.config.js | 4053 | `f7967a01b1129f327a095aec46bf0c3f2ae3cc2c5a020207f19c2328c59d200e` | 0 |
| packages/xrpl/jest.config.faucet.js | 357 | `a3f113eea5cfeebad3ce20db45fab1ede5201421808ceac26ea0d58d004519b2` | 0 |
| packages/xrpl/jest.config.integration.js | 405 | `c7d73a4f4932d950aab58370e370ed6de763ae1119e02d4219925a822305879f` | 0 |
| packages/xrpl/jest.config.unit.js | 356 | `f69a26c72847a0c708217827149ccae5f4348184fb6a187d76697ec3ac0c8580` | 0 |
| packages/xrpl/karma.config.js | 2534 | `c5fe142dbdd993b37b4e3ad463ceda45eb070ab9a332cd65029b7d6ddc34920d` | 0 |
| packages/xrpl/package.json | 2844 | `a353aae9b6efb4c6ab2b31f80e5514aea5f513a278efdaf0b40f876b13445b32` | 0 |
| packages/xrpl/src/ECDSA.ts | 93 | `cbcbad367ed3f2daf8a962801517ce8d837ee06e8d8e0e830072290dc4b78d5b` | 0 |
| packages/xrpl/src/Wallet/authorizeChannel.ts | 805 | `8a92153ceee72ee5d41444cbf2d23319a9d07c65a60bf7e63f345f557f1bae45` | 0 |
| packages/xrpl/src/Wallet/batchSigner.ts | 9717 | `d8e371614da24d2cc3f8fac11221e664ce2deb1faa6e367f87ae01a7dec71a3b` | 0 |
| packages/xrpl/src/Wallet/counterpartySigner.ts | 6944 | `ba71b06ed8ce20ce29faf1f9cd09bdf9e35358a4ba3ed9edb77e9d0bb035b224` | 0 |
| packages/xrpl/src/Wallet/defaultFaucets.ts | 1852 | `921304a15a3167691030e367dd3f4b5d1ab45cdae1ad43fbae35d465876e85f6` | 0 |
| packages/xrpl/src/Wallet/fundWallet.ts | 9337 | `143105fdb0743a2068e336350b1e2c6e4433ec64e16715abce0ff64f22fe72ea` | 0 |
| packages/xrpl/src/Wallet/index.ts | 20315 | `a9e1f4460a6a69f1a9b4b29be6f6d7ab35033063cc22cd2a4ea56e75cda3bdaa` | 1 |
| packages/xrpl/src/Wallet/rfc1751.ts | 6890 | `ca8450319869d250ab85fdb43650de4a0a803056520c327225f03f0300b9ead1` | 0 |
| packages/xrpl/src/Wallet/signer.ts | 4591 | `67ee1f0b9972a09f21bfc7b4dfdadfe6223e8aebca5258e4d139b0dd9bce76a2` | 0 |
| packages/xrpl/src/Wallet/sponsorSigner.ts | 10162 | `b2aa9648c09d774ac9d8764de308a284e19cc4c7e840caeeb8a10c47ae456437` | 0 |
| packages/xrpl/src/Wallet/utils.ts | 8054 | `4c917357f16e54d17a4e02c5639cb864de2c4479ef6e91c62c2ac3ce20519202` | 0 |
| packages/xrpl/src/Wallet/walletFromSecretNumbers.ts | 1783 | `839d32aeaa76dbe60584ce6e09f58a243a7cc1efe8c7dd4079d509a48fdecc72` | 0 |
| packages/xrpl/src/client/ConnectionManager.ts | 1125 | `c7f1746d69d1d03ff84ecdb07df603ec4f4084090a23e37227de99107385a7c9` | 0 |
| packages/xrpl/src/client/ExponentialBackoff.ts | 2460 | `f298694d6ad420282dde267f512b3bd771c2f8755aa3702d4105d73bd095f9cb` | 0 |
| packages/xrpl/src/client/RequestManager.ts | 7654 | `c2e53d6b0b592bdb6d4c803c68c7d872b9be9f7e9d3cfabad65df96da5e45588` | 0 |
| packages/xrpl/src/client/connection.ts | 21692 | `4cf8560e02317098ba39a38fb03eb56c945618b0052948c8921b24c32dbe44bc` | 0 |
| packages/xrpl/src/client/index.ts | 43127 | `a4896187b6671c61b0bb21518ccdf44bfb93de270b763059dc24cedea660dd2c` | 0 |
| packages/xrpl/src/client/partialPayment.ts | 6633 | `28895bfb491534aa67957f32800b4857a1f820ffdebb5622b41b007b8be25831` | 0 |
| packages/xrpl/src/confidential/batch.ts | 29040 | `cdc640a6e4efe2374f4b7df429ecb33233610222b67397518353964cca5b09d0` | 0 |
| packages/xrpl/src/confidential/convert.ts | 8255 | `85dda6739e2e5d29701c7bb0d7fc09d502ae119a43858d0abd3970602efbd6c0` | 0 |
| packages/xrpl/src/confidential/index.ts | 1416 | `ffb2c04327b6bcbec59b070539fa6deddd2a0a6764f5596da7f8c612d3089420` | 0 |
| packages/xrpl/src/confidential/keys.ts | 1617 | `24367729fa75d6d2b9919a82bcdda317d1c62a3b3e120dd253224b590c773ca4` | 0 |
| packages/xrpl/src/confidential/ledger.ts | 11182 | `3d3574c4a614c296f148e18b1eb07ae0096af8cfb2e5d0cfd04ab959a08a46d9` | 0 |
| packages/xrpl/src/confidential/loader.ts | 1382 | `ce1d90ba4c3de2a54985e06b98e05fb324e40b24e83d85df1d97d0ae3383696c` | 0 |
| packages/xrpl/src/confidential/transfer.ts | 8278 | `281ab39d336d338855b42687e3dc600f95e7b160ae86fb9a3180192e9963ef29` | 0 |
| packages/xrpl/src/confidential/types.ts | 10407 | `a063bbc30c35d4b292fda4a0edf04ea6d1502bc616978759ab54ee258361bfc1` | 0 |
| packages/xrpl/src/errors.ts | 3602 | `b826714baebb147e78dab3ff6667d466df9cf2a50042708b034453cf3ca35bcb` | 0 |
| packages/xrpl/src/index.ts | 898 | `330095173dcc6a71147ba09092b10dd86986459989351ad3a8a3b42f3dc14af0` | 0 |
| packages/xrpl/src/models/common/index.ts | 9176 | `0b67ef6a5157aab566b4b1ca7b306861b2c137254accc16a9d83a0d6c2536dd3` | 0 |
| packages/xrpl/src/models/index.ts | 883 | `77a4ee2fcb86559a5b119fa5ddb34ef47a74bca2ed29559a63791b242257dccb` | 0 |
| packages/xrpl/src/models/ledger/AMM.ts | 2378 | `48f9613cbf224c77e54520bc1aec39da134937d52b1143df7289b08b7182e45c` | 0 |
| packages/xrpl/src/models/ledger/AccountRoot.ts | 8446 | `78d9161e13fd547ad8b39d445a78b8b38b1d9f27d68fd1604e37a5cc424814fd` | 0 |
| packages/xrpl/src/models/ledger/Amendments.ts | 1345 | `c40e089ec5dbf6d2205a45caad8a97a8f01861bce682c7124b5bdeac743deb5c` | 0 |
| packages/xrpl/src/models/ledger/BaseLedgerEntry.ts | 895 | `53a491888f80b26d121a09d2e2fcd0d882d8762e6ad924c91235863372e2c09c` | 0 |
| packages/xrpl/src/models/ledger/Bridge.ts | 2441 | `a9c645c8b34ac33a6c743da34a50cbcbcdb89d15421342fcd25864235687594c` | 0 |
| packages/xrpl/src/models/ledger/Check.ts | 2488 | `3b63a1fecaec8b09061e2e5b09648a540fded4fa5f3801c4d5748e322e74a97d` | 0 |
| packages/xrpl/src/models/ledger/Credential.ts | 1579 | `24263129e74eb77431ce5ce2acfb8652040ad001f88dfb2e5a2f8aef61186690` | 0 |
| packages/xrpl/src/models/ledger/DID.ts | 335 | `4a35e7b77417b56f0088c4d06f23c067b63021f820fb372b6f0bad518217386c` | 0 |
| packages/xrpl/src/models/ledger/Delegate.ts | 1159 | `b11890b08350ceb58ea702e7c1fe8f9f435c69d58e73495c8cd5754cab13e066` | 0 |
| packages/xrpl/src/models/ledger/DepositPreauth.ts | 1202 | `4a54d7f166d0502582d8a6655fe840581b8540aba407f7fd96b124cb3795c6bd` | 0 |
| packages/xrpl/src/models/ledger/DirectoryNode.ts | 1665 | `4614f6c3862e2e08fb5514031471d3e6f8557b416cb581c91c9d69a53b9e7ee9` | 0 |
| packages/xrpl/src/models/ledger/Escrow.ts | 2685 | `f75e9fb813eb834315642358950bde60bf57e71de5282acdfd0c478fd0015034` | 0 |
| packages/xrpl/src/models/ledger/FeeSettings.ts | 1832 | `33900b27222cecca95448057882ad5917f13b159d1735d6f1a7cbc8c2f0be335` | 0 |
| packages/xrpl/src/models/ledger/Ledger.ts | 3357 | `158ad5a7ccfd133f040e7e0ff3e7732db0c31fedc9459798bfd49cfadfb0fa11` | 0 |
| packages/xrpl/src/models/ledger/LedgerEntry.ts | 2249 | `385744266b257ff04f96ba6ac19103e515ece45de0e117e2ce47f4fa47937065` | 0 |
| packages/xrpl/src/models/ledger/LedgerHashes.ts | 749 | `7484b745a24a64fab7ff43bf90e0832207ecab3af46a7c11a658351ce46e99a9` | 0 |
| packages/xrpl/src/models/ledger/Loan.ts | 3914 | `7dccc3203af3871227fc83fabbe42678ada4fa1b3e3c81f2527c38c06c4bcb2d` | 0 |
| packages/xrpl/src/models/ledger/LoanBroker.ts | 2513 | `867ac5a1797bf5281a4abd94966dde4b87798fa57a481b22eee9e787fd81c470` | 0 |
| packages/xrpl/src/models/ledger/MPToken.ts | 1199 | `521ab9284544320cc79f6acfb256844bb18d37b205bf11e1b103a7cae46005c1` | 0 |
| packages/xrpl/src/models/ledger/MPTokenIssuance.ts | 5515 | `12aba43cc27c6a91164a079a7888989ff125711700d770d7d21f56038bdd0a5b` | 0 |
| packages/xrpl/src/models/ledger/NFTokenOffer.ts | 380 | `0e43b44935d37e512c65eebb342dc2a82091f3fee27ef46909d0b914d5e45623` | 0 |
| packages/xrpl/src/models/ledger/NFTokenPage.ts | 483 | `69607bb048e6ce51bdd67f540ce358eed854c571b760534b52aee924ac458983` | 0 |
| packages/xrpl/src/models/ledger/NegativeUNL.ts | 1076 | `5274acbc79dd2c8357744838031ce4dc9c6cc37ec95224cc9a6706be82b40024` | 0 |
| packages/xrpl/src/models/ledger/Offer.ts | 1953 | `393fa1b7fa96f0e34104066ee860815d588304d758828bbab208dc9fb7c3b155` | 0 |
| packages/xrpl/src/models/ledger/Oracle.ts | 978 | `8d16e11afbdf7b181bbfd35345afcaa98af3f6b619a0ff5d15fffa62f558df63` | 0 |
| packages/xrpl/src/models/ledger/PayChannel.ts | 4301 | `23e12609408768d0225607327792ad8d5d0d83a2a50ac3cdacdbcb5201c5afac` | 0 |
| packages/xrpl/src/models/ledger/PermissionedDomain.ts | 923 | `20be3bd464871baff0c45946f6e81b1170daec7cb9c2ca337c27eb2549486744` | 0 |
| packages/xrpl/src/models/ledger/RippleState.ts | 3533 | `0c9baeb0f3d6ded9ee9cbaeaba044a8ba19933c4b5983bda69927a960ff2c88b` | 0 |
| packages/xrpl/src/models/ledger/SignerList.ts | 1692 | `67f59c4a4fc4ce24b72e3848b75dbdf62f21c711e1a6b23b47e7fbf87f6b67de` | 0 |
| packages/xrpl/src/models/ledger/Sponsorship.ts | 2543 | `4fceb692ea67ff8ac6a01406256e0d7cba14c18bc188bd23af1aa529d0030063` | 0 |
| packages/xrpl/src/models/ledger/Ticket.ts | 856 | `a75f972577f3625d8edfd61b55c03ee0ee826501aa4eedeab03bffd3b2f48e43` | 0 |
| packages/xrpl/src/models/ledger/Vault.ts | 2623 | `a701036763529402530aeeb96261d5f1c5047f1415b2a3b79b0c075a599a3619` | 0 |
| packages/xrpl/src/models/ledger/XChainOwnedClaimID.ts | 2363 | `23948d7e28fd7b5b29e01617ba78663b6330f81942cc6227d431e32491e89c78` | 0 |
| packages/xrpl/src/models/ledger/XChainOwnedCreateAccountClaimID.ts | 1849 | `61a3c62d79c5708a48a6c4dd4548fef5b330a6387055a7c7720a17e50ef17c9d` | 0 |
| packages/xrpl/src/models/ledger/index.ts | 2717 | `57c92748c6fae622025d81396ae44e1ca8b69fc0095dd91732f74cbe02bdb45a` | 0 |
| packages/xrpl/src/models/methods/accountChannels.ts | 5136 | `b03350cb1cf17810aaf13c7f64c1bfd5b734ff3e3ad5f60a33b0de00d57b0d5f` | 0 |
| packages/xrpl/src/models/methods/accountCurrencies.ts | 1466 | `a7537cb61deedfff9e11f4c3c3d6fb7f06f1936cd8266e1ecd3d76450633b6e1` | 0 |
| packages/xrpl/src/models/methods/accountInfo.ts | 7857 | `e936568c5f745b21a00ad8f248c5d33316b790fdc17738de5489b3ce302accf1` | 0 |
| packages/xrpl/src/models/methods/accountLines.ts | 5238 | `0a496cf1b0c8181213d38d7ef2252dbcf77ca6d383b94a2b1940d9a55e5ca757` | 0 |
| packages/xrpl/src/models/methods/accountNFTs.ts | 2109 | `3f310256076802881d3d929222140cc26e473361de1bff518371051a83a077c0` | 0 |
| packages/xrpl/src/models/methods/accountObjects.ts | 3330 | `1b365cd12bd30c25bdc034d86beb5726ae8a04ce68ed8d43d5a4f5152e6b33d8` | 0 |
| packages/xrpl/src/models/methods/accountOffers.ts | 3196 | `d4d5ea1599bc9de5e47f9a9e7e6a7db5acfc23396e1cf3b7d3200a0141bc4652` | 0 |
| packages/xrpl/src/models/methods/accountSponsoring.ts | 3087 | `0efcdfb8ac2d37b18ba623ca4e80e0417e1f739469c3c512b721a7a9616fdabd` | 0 |
| packages/xrpl/src/models/methods/accountTx.ts | 4636 | `db531c4c8a859f5e4cd587100407033ced60c8c899f8385f530d0949897e552e` | 0 |
| packages/xrpl/src/models/methods/ammInfo.ts | 4294 | `22931f742010358b694a3b581ed427ec7b1b46bf6cb5df0ebed0b653927e032f` | 0 |
| packages/xrpl/src/models/methods/baseMethod.ts | 1498 | `9b68c160ab7c56ca3015d5db2eab1df627c100659d174bfcb2304087592812e5` | 0 |
| packages/xrpl/src/models/methods/bookOffers.ts | 3350 | `997712e76466bd50f7ebb6e6dbc0adb0a1a9d6dc387c4daf00ad0bf168783437` | 0 |
| packages/xrpl/src/models/methods/channelVerify.ts | 1190 | `42223ff08dc087efd18ecd39ae82e668fa5f791d73041764b6599047706d1155` | 0 |
| packages/xrpl/src/models/methods/depositAuthorized.ts | 2231 | `250f0a2330b4f44a42067647bbf4cb464b0763af451a37816e9af5f8f12470f1` | 0 |
| packages/xrpl/src/models/methods/feature.ts | 1430 | `9814a112d3e619a7c4fa2211860c2fec75be8bb8086f795c132d7a7e9b1e531f` | 0 |
| packages/xrpl/src/models/methods/fee.ts | 2873 | `7d8c6508b35cc99377ff41b6b37fe4f258501bbf032e81c465378e30f5e74f9c` | 0 |
| packages/xrpl/src/models/methods/gatewayBalances.ts | 2568 | `46e3379e90d429da299e6d27698d303d4a180ccd2327e04b631ad85c27576f2b` | 0 |
| packages/xrpl/src/models/methods/getAggregatePrice.ts | 2725 | `c15f3b6a253ce3cf7cfe7de2d820d0b78fa1992a7a7d021915211d1ec8bc2465` | 0 |
| packages/xrpl/src/models/methods/index.ts | 18418 | `983ba716920a666d67fa338cd8360ba8ae729ca4c9d2478ec8405e815bdcdb50` | 0 |
| packages/xrpl/src/models/methods/ledger.ts | 8420 | `3ae8059703abcb072b06a1f36cd084e6382807fcd7368e2d39784936fcf75864` | 0 |
| packages/xrpl/src/models/methods/ledgerClosed.ts | 691 | `83b2820c15a1bd28d2e9942f362ff8febd23e65f1a4cf407386bb91fae02dc9c` | 0 |
| packages/xrpl/src/models/methods/ledgerCurrent.ts | 725 | `258a5e7f9164c476ea8b616aeecfe3ea8cbc2cfadf13f8b197542e876ca26945` | 0 |
| packages/xrpl/src/models/methods/ledgerData.ts | 2165 | `459a48c0aef19f7858a83b7805ece3444d08c87b7df2c3c2d7dabe5396120ba6` | 0 |
| packages/xrpl/src/models/methods/ledgerEntry.ts | 8625 | `25e3c5b453c7f249b856ca44d50b5e5e2c0d4886eea9c9555fa809ab4b59efaf` | 0 |
| packages/xrpl/src/models/methods/manifest.ts | 1496 | `d1e320ae975b8a3f256c3b5396d64f84fff8029894a4ded82733e58f463ef036` | 0 |
| packages/xrpl/src/models/methods/nftBuyOffers.ts | 1406 | `144143eb44a636c38d6076edebd2f7ccdc770bc7ba1676c3835bcaa789c10555` | 0 |
| packages/xrpl/src/models/methods/nftHistory.ts | 3480 | `26404b99c18f6f0110b6ee4264fcc300f569472989d627a305eb6a3a89b0ee61` | 0 |
| packages/xrpl/src/models/methods/nftInfo.ts | 552 | `7faa2d3bd535d1418a8140c599d07e2b12e61f341e5ff1e97bcb1706faeedb6e` | 0 |
| packages/xrpl/src/models/methods/nftSellOffers.ts | 1415 | `7a786fb81f3273185dc527112eb6c8ef95cfa86d532189106ba29f1eb62fecac` | 0 |
| packages/xrpl/src/models/methods/nftsByIssuer.ts | 1891 | `cd50881b917a995a8ae1e57d145fe96fca9911d03c2bb3f4da7485d27c8cd2c7` | 0 |
| packages/xrpl/src/models/methods/norippleCheck.ts | 2854 | `093ccaf291bc6aade820f2affc6aeb34895a6f8f2ee74c8ab5ce448fcb854f56` | 0 |
| packages/xrpl/src/models/methods/pathFind.ts | 4019 | `d970a0a59525e26dbe6b29b5af122c94a4f8bffbe11443a3081da28f5011fb10` | 0 |
| packages/xrpl/src/models/methods/ping.ts | 527 | `915a9c788ca919e2cc2d1b96704917c48b71b23e4e28b7f0c231dbfbe39d1f99` | 0 |
| packages/xrpl/src/models/methods/random.ts | 532 | `b58da5a3dd9e88e6253e8ffc9a972f7061f7ccbd9a59ffa4fee9b2673e9fa46f` | 0 |
| packages/xrpl/src/models/methods/ripplePathFind.ts | 2753 | `9fe1a3dec87a789dcdea90250b677c21946b56dd83fbda3cf9ef8d5f0970391d` | 0 |
| packages/xrpl/src/models/methods/serverDefinitions.ts | 2513 | `85db1052b3d4859d1aaaa817e4f6bbf0ff3634f62c6080ce9dcd006722bef9c4` | 0 |
| packages/xrpl/src/models/methods/serverInfo.ts | 9476 | `06915f01f7c37846f5dcb43f4e6306ab1e4a241fd8c8a0d91bc3b1a754a1fb1e` | 0 |
| packages/xrpl/src/models/methods/serverState.ts | 2300 | `0cb8514083d65d49fa85cef0f9b444f35778cb865d1e541ae2a83fb49ca6f08c` | 0 |
| packages/xrpl/src/models/methods/simulate.ts | 1655 | `516527092d28c54b65a24f94b97720b94d64c8a4ddf495562da81514a352cb01` | 0 |
| packages/xrpl/src/models/methods/submit.ts | 3239 | `277706357ce0eccb7c476727e3553dc91adc5bfdb7ee0c82abb5c209c5bdb702` | 0 |
| packages/xrpl/src/models/methods/submitMultisigned.ts | 2400 | `79054a9c4b2bb079ef9356e11826be23e8cf74a5e0cd7c351078050b1439cb2e` | 0 |
| packages/xrpl/src/models/methods/subscribe.ts | 17799 | `5d9016c9b044d67fbfcaa7a1995cecb8b247eb4ba43464bd1563a7954cf75de2` | 0 |
| packages/xrpl/src/models/methods/transactionEntry.ts | 1393 | `e6a0780b0f475d0b5a5dfbbfe1909af0f0d1ba7e50d450b63fdb876a1d4213ec` | 0 |
| packages/xrpl/src/models/methods/tx.ts | 4437 | `22ffcc33ac62968b87a4910a01ff4c7b6148fe5f0f394074781857805cee5317` | 0 |
| packages/xrpl/src/models/methods/unsubscribe.ts | 1318 | `5d02c6050823d88d9b584aaf8f3c5fd1124d4ecc0334b06026a6a3cb89d80718` | 0 |
| packages/xrpl/src/models/methods/vaultInfo.ts | 6047 | `38df490d66cbbc4bc1cc443402b561e0caffe2a5b8a5c19e80ea92ead8c7e5f5` | 0 |
| packages/xrpl/src/models/transactions/AMMBid.ts | 3303 | `30885a89f9168e0a09fb130b0e1fa6cc1629fcf804b97bf58bbced5000d30bdf` | 0 |
| packages/xrpl/src/models/transactions/AMMClawback.ts | 3476 | `0a7cd39c416d30a64b26a0378eb7f4660723cc4dc7cacb8b43e0df334ede5d10` | 0 |
| packages/xrpl/src/models/transactions/AMMCreate.ts | 2316 | `8a0b93eb38ed56a6b2d6d95455faeb8445558e86e5483827c8efa0b721f56e06` | 0 |
| packages/xrpl/src/models/transactions/AMMDelete.ts | 1545 | `95ade5570328929bd2700e542dc1b2691dd964cdc24592c59124a58e2e559824` | 0 |
| packages/xrpl/src/models/transactions/AMMDeposit.ts | 3064 | `2fde5d23f90da9c262301a98b639bae56b7b02066855b7714b4b9a340c7e3a3f` | 0 |
| packages/xrpl/src/models/transactions/AMMVote.ts | 1580 | `4ffdd94dc2d87d80eafaafa0c3c9fc58109baab93f92486334a2f6a9d09f6727` | 0 |
| packages/xrpl/src/models/transactions/AMMWithdraw.ts | 2806 | `464fd224b2420b639235d9285b6bcd56c923f70b42ea66e9703ec663d36c6313` | 0 |
| packages/xrpl/src/models/transactions/ConfidentialMPTClawback.ts | 1996 | `fce4a53451553451e1ec76e81415f4ac1298ff31c35e72304fc79522a20975b2` | 0 |
| packages/xrpl/src/models/transactions/ConfidentialMPTConvert.ts | 3979 | `f3870d179994af79b283e9d9af94af5c606cf40104b8e04336516eeb01778a4a` | 0 |
| packages/xrpl/src/models/transactions/ConfidentialMPTConvertBack.ts | 3366 | `3e6d0d5f6126e969fed8c9240f220fb10494cb8646e4288288bc8fe5db9a3e9f` | 0 |
| packages/xrpl/src/models/transactions/ConfidentialMPTMergeInbox.ts | 1235 | `de6b205830979cfb464fe6f633a10d3c017d5708e3ee404615fd2e9acbff0201` | 0 |
| packages/xrpl/src/models/transactions/ConfidentialMPTSend.ts | 4337 | `38cb28ae5f5c52b64e326fccb4b9bf1e6a1a4b8e0d8ccb343fd1c5be87c5aee0` | 0 |
| packages/xrpl/src/models/transactions/CredentialAccept.ts | 1257 | `762b3750ace75d745aed15384bbefc21969ad8376c2f6b023fbd480f638d6174` | 0 |
| packages/xrpl/src/models/transactions/CredentialCreate.ts | 1945 | `9595019c3ed6ba78a4f8c347c04f5e6ce625365cf29903e166bc5f6fac4bd011` | 0 |
| packages/xrpl/src/models/transactions/CredentialDelete.ts | 1385 | `ec3b33ee8ba7857a287879b3cd17269c2eb75be2678b47ab27c0854f554d34a7` | 0 |
| packages/xrpl/src/models/transactions/DIDDelete.ts | 468 | `eadaa35885915ee46f6f74685f59bc8be3768e596ad932d2949c46ae56f8ccb5` | 0 |
| packages/xrpl/src/models/transactions/DIDSet.ts | 977 | `cc04e8c055a1bc075b2d1a9b7dcdd1868e40553d7da1d19b8d81289f609db601` | 0 |
| packages/xrpl/src/models/transactions/MPTokenAuthorize.ts | 2086 | `93c0409dd3eb48158fffb728fc7c631e86835181f6fff4d068dac3f87b673280` | 0 |
| packages/xrpl/src/models/transactions/MPTokenIssuanceCreate.ts | 13206 | `5ea122c81ed7743b0bebbc673f663aec99f546bbe81016d0c0c80b7e68aee245` | 0 |
| packages/xrpl/src/models/transactions/MPTokenIssuanceDestroy.ts | 1131 | `8c5d5d46a9b5bdd3963c656149bdd45a71b70a7b9afb38156bfa171579515bbf` | 0 |
| packages/xrpl/src/models/transactions/MPTokenIssuanceSet.ts | 12304 | `19d112b99307676f269514039cbceb920c756e61951e05479ffd76e64017b957` | 0 |
| packages/xrpl/src/models/transactions/NFTokenAcceptOffer.ts | 3908 | `d56064c874c713890e1c28a1b856028ebeb8d94b4d2363a8daeafaf9ab7f44f1` | 0 |
| packages/xrpl/src/models/transactions/NFTokenBurn.ts | 1706 | `406ee2460bb7a578181117968f0aa782b65277ee76847db004899ed34fdcfd2a` | 0 |
| packages/xrpl/src/models/transactions/NFTokenCancelOffer.ts | 1753 | `e97288b03f1bf6184c698d615511f2c12958474554288902ae7f7d5386e032ce` | 0 |
| packages/xrpl/src/models/transactions/NFTokenCreateOffer.ts | 4709 | `a670ff7f02c44a47e908f93dee6fdb732356c53f6f897be639bb3fdcc75e94bf` | 0 |
| packages/xrpl/src/models/transactions/NFTokenMint.ts | 5755 | `b638583a306dd010efa7979928766972cee01a543120fec52d5ea927f9902b19` | 0 |
| packages/xrpl/src/models/transactions/NFTokenModify.ts | 2110 | `18ba4969774931a34fcf9022ca9e5a0cd30880b00700fd17ac018dc29e7caf3f` | 0 |
| packages/xrpl/src/models/transactions/UNLModify.ts | 708 | `801a0667b2d1e6d168740774faac692fdaaf9bc57e4a3107efc0aef82cad5d86` | 0 |
| packages/xrpl/src/models/transactions/XChainAccountCreateCommit.ts | 2040 | `fc076a46add8aaee9bef1296d749bc879ce5ac78dc09331f895263d9b043cceb` | 0 |
| packages/xrpl/src/models/transactions/XChainAddAccountCreateAttestation.ts | 3111 | `83c6d693f6f0e15e4d33dd1cf782f63995924628574f5c815f681d363955e240` | 0 |
| packages/xrpl/src/models/transactions/XChainAddClaimAttestation.ts | 2900 | `8463297e4c2f678d4b4e600c993fd19f42bb5b62f7a86b4b493b2d3b335b067b` | 0 |
| packages/xrpl/src/models/transactions/XChainClaim.ts | 2051 | `6fba354d21c61177af465f26de8d85efd4764ef51526a5da1b4f95506f1fe674` | 0 |
| packages/xrpl/src/models/transactions/XChainCommit.ts | 2215 | `9a274dab2880881862bfc454ad6bbc4ad9ce1b554f6ff821e9d78e237ca52af2` | 0 |
| packages/xrpl/src/models/transactions/XChainCreateBridge.ts | 1628 | `5652f7d18f67c1f999e6520878fb8c09d9e1f762de67052c5093af524c2c85dc` | 0 |
| packages/xrpl/src/models/transactions/XChainCreateClaimID.ts | 1423 | `cf7dc6984e68f7f605a1776a5b172daed4cec64b59c82aa8ac37892cd2555aa7` | 0 |
| packages/xrpl/src/models/transactions/XChainModifyBridge.ts | 2068 | `288ec4d4c58b30b9fa8998405b589a12f20ed9c9e513861d2a6eaf0868257625` | 0 |
| packages/xrpl/src/models/transactions/accountDelete.ts | 1690 | `9de8e656861e5f7d6e19b04e37981c82e512b05d67cafe278a89f41e48fe3bb3` | 0 |
| packages/xrpl/src/models/transactions/accountSet.ts | 6577 | `a67144d143a7c1980fd95f65c368db5bed0a7a8608ca011b850980dea9a81f2e` | 0 |
| packages/xrpl/src/models/transactions/batch.ts | 4479 | `0f1a50ffa013539a0653053dfc7253083228673c813c5dc39e69cf938b131808` | 0 |
| packages/xrpl/src/models/transactions/checkCancel.ts | 938 | `e28a5d47aa5c265b0292ba68c0f211656b3b2006222e66a201b351d5859c0a6a` | 0 |
| packages/xrpl/src/models/transactions/checkCash.ts | 1894 | `79e58c7f4e64c32784e63fd31615950c7e18d1573be5bc8c7906ac867da4381e` | 0 |
| packages/xrpl/src/models/transactions/checkCreate.ts | 2170 | `492d46b8a562cdebb0f62b579f3db0e18e8ffb4c7f8cb3184d2c9e5a0f292dcd` | 0 |
| packages/xrpl/src/models/transactions/clawback.ts | 1920 | `9fc746f86ef3cecfa40a087e229f8f726517ec5335ad9ac9934a14727ba3a6af` | 0 |
| packages/xrpl/src/models/transactions/common.ts | 38511 | `befec08d565c2199fce7b20ef5bd2e440cbab687de72ae86dc05653c9b4618dc` | 0 |
| packages/xrpl/src/models/transactions/delegateSet.ts | 3339 | `9e0e5231b99bd3fc21eb0faa1773c79118ff79d8df53c4dd10113e17a7c41055` | 0 |
| packages/xrpl/src/models/transactions/depositPreauth.ts | 2967 | `c38a62dca4ecfdafb33940f5366306ce61d6657558e1d9877711e3fa278f9c05` | 0 |
| packages/xrpl/src/models/transactions/enableAmendment.ts | 898 | `9ee861e15a753d3b35f65d5b1ab6cb2b8bdaf422427cd92eed35fd8d057243e9` | 0 |
| packages/xrpl/src/models/transactions/escrowCancel.ts | 1248 | `38466fa1d749df277ba7c74b39e8f7dbee31a765cb8699d9e19d7b1dda9f2c61` | 0 |
| packages/xrpl/src/models/transactions/escrowCreate.ts | 2709 | `a5b0eb0d32714bc3019619d55ac9beff793a51c6802eb26c6aacbcf648c3455e` | 0 |
| packages/xrpl/src/models/transactions/escrowFinish.ts | 2021 | `d0214fd85f5e96e3e9e879f733b8dc04d06e4a871dcbd36a861345e44f7c5894` | 0 |
| packages/xrpl/src/models/transactions/index.ts | 5748 | `97c3b680df66619c1397720682bfc771b8c59be1ac4972b961d0d86049c0ec95` | 0 |
| packages/xrpl/src/models/transactions/loanBrokerCoverClawback.ts | 2145 | `728b84b83e3fb79449dd409e7df330aedd9f7f4aa26403b9b2a28a7f716b2def` | 0 |
| packages/xrpl/src/models/transactions/loanBrokerCoverDeposit.ts | 1227 | `4ae8c732575f668d57876fc5c1ec095753f7c6b59eb9979b6069185ba5955a8b` | 0 |
| packages/xrpl/src/models/transactions/loanBrokerCoverWithdraw.ts | 2010 | `fada5c395c91a2e9b9a0ded309fe16f478b7b3ba097ebc5cb5a1eeede43eb789` | 0 |
| packages/xrpl/src/models/transactions/loanBrokerDelete.ts | 966 | `f53dc54395d01206484b2bda653cc2bcebe2ffafd4f0082327f26de176f392e6` | 0 |
| packages/xrpl/src/models/transactions/loanBrokerSet.ts | 4572 | `b9ca287f5901fefc78f7d935f7996b1a7b8538c7ce9c9905b49ffd4a1dcda3db` | 0 |
| packages/xrpl/src/models/transactions/loanDelete.ts | 887 | `a7abcc0e72bdbedbfd208169e17176b56bb008df116dfa17d574348923050461` | 0 |
| packages/xrpl/src/models/transactions/loanManage.ts | 2495 | `ae3b9cfc8db849b965b8750409dfdbd6d4337798555206d2c446ad274f40198f` | 0 |
| packages/xrpl/src/models/transactions/loanPay.ts | 3052 | `415791b19dd301e822fe67d21398cb6e38396ef7ee80b6d7a124efdadf8e6f98` | 0 |
| packages/xrpl/src/models/transactions/loanSet.ts | 8946 | `e2d9d3ea9392e09565659d90c25fef96df6c650dfc2cb6e0870fb9fb5d67e6c9` | 0 |
| packages/xrpl/src/models/transactions/metadata.ts | 3033 | `b71385106cf1eb6a840ac004caec3c0396e0d07ba0de5d6f5998195003f2a345` | 0 |
| packages/xrpl/src/models/transactions/offerCancel.ts | 934 | `e10ef1412e026152e59c5d335f400a192934c3002511eae4abfaf9b1acce990e` | 0 |
| packages/xrpl/src/models/transactions/offerCreate.ts | 4647 | `38b20cdec1e940ce76797dea24d800157a42e9bdaf2c8aa1a3944af66e64b143` | 0 |
| packages/xrpl/src/models/transactions/oracleDelete.ts | 707 | `1b692a145cb9b160ea866a12fc71dd1f58c743926ae7fa5232f289076a05aa17` | 0 |
| packages/xrpl/src/models/transactions/oracleSet.ts | 6564 | `47759fa3d96361469474e727c51cbd105e97f99e3937135b43c3d038223749bc` | 0 |
| packages/xrpl/src/models/transactions/payment.ts | 11147 | `de89725f69d936ce3650115f22f533ab6a8db41a85b17e0c021f1ee6e73754f2` | 0 |
| packages/xrpl/src/models/transactions/paymentChannelClaim.ts | 6081 | `b9f3a9fca0bcad503f617883d6240ec0e6787349cffe285e95d3599836eb6611` | 0 |
| packages/xrpl/src/models/transactions/paymentChannelCreate.ts | 2456 | `e06f9f4f8e8d9eb969ab80a156ed808719e884f38d5f1ca71eeb7ed082479a11` | 0 |
| packages/xrpl/src/models/transactions/paymentChannelFund.ts | 1782 | `ce4df2894eea2a260bd6bdb4b1533857575ffd138fe511a39c84cd2e905876f2` | 0 |
| packages/xrpl/src/models/transactions/permissionedDomainDelete.ts | 685 | `3a83f078323fd64a198dd7216b9dd1dc72fb6520def962842d18567f409fcf1a` | 0 |
| packages/xrpl/src/models/transactions/permissionedDomainSet.ts | 1510 | `e2f4c8e987e7179e2e018b08e3a7dd8fbd8a2c896d15ef0ee9d3e84c81953cf2` | 0 |
| packages/xrpl/src/models/transactions/setFee.ts | 1378 | `89e5cf4d08e89143e814d77fe3dde65e28052c4a5f806d12ed221f26b6819a2e` | 0 |
| packages/xrpl/src/models/transactions/setRegularKey.ts | 946 | `f989e28e164935a32f80b506a7a6e001c3b636fc87f335d134905708fdf7f01d` | 0 |
| packages/xrpl/src/models/transactions/signerListSet.ts | 2605 | `b7502b7510dcd6c04906aa2185e2f2d55d8e1dc756d41b464600f39d31ffb542` | 0 |
| packages/xrpl/src/models/transactions/sponsorshipSet.ts | 14121 | `f0c1488148f94e62cf94fa86fd6af8806ba2ad52c2a19e02e6fcecd2a17d8fd0` | 0 |
| packages/xrpl/src/models/transactions/sponsorshipTransfer.ts | 8362 | `3b62a863b5f4295d3aecc777c45030730dbb612e879177d5b4dbd23d9f03f464` | 0 |
| packages/xrpl/src/models/transactions/ticketCreate.ts | 1166 | `f9d0801b279be1397e78a278c3e30ba6ab7607b939a40aba621eb10baf95b97c` | 0 |
| packages/xrpl/src/models/transactions/transaction.ts | 16316 | `6154fef1d2389f0cb50c1bbb69f7e9b7bebd0cef4929d0044abd6abf57beb3b0` | 0 |
| packages/xrpl/src/models/transactions/trustSet.ts | 4414 | `2dbb15e1d7edbebdca55e18a02dc4711a6d1c1489b6bcc89c087e0e36f0834da` | 0 |
| packages/xrpl/src/models/transactions/vaultClawback.ts | 1604 | `f1be395f25669db9e9e705d40527aa94b895a1ec99bb40373b1d2efc7e54e2fb` | 0 |
| packages/xrpl/src/models/transactions/vaultCreate.ts | 10360 | `c7108a8ac025ac22ba1634434a903347192e93cc67923dc5149e095510bca766` | 0 |
| packages/xrpl/src/models/transactions/vaultDelete.ts | 1673 | `aa75bf3e436664e4a39a4588ce9dad708a829e01061109a666cb23fdb74cdf14` | 0 |
| packages/xrpl/src/models/transactions/vaultDeposit.ts | 989 | `1f72136c688588e87a33fde2b43460b29d670d8ee050d1a1d9123e92c54130a6` | 0 |
| packages/xrpl/src/models/transactions/vaultSet.ts | 1898 | `709132100598b06bc7899fe99eb6d88007a30fb92159731a5169d00b73916039` | 0 |
| packages/xrpl/src/models/transactions/vaultWithdraw.ts | 1758 | `0aaee327ca2e744cf418e0c03fdd869ad6fe234d54b3799b60fb3590b668b286` | 0 |
| packages/xrpl/src/models/utils/flags.ts | 8087 | `052ea34014f30a3d21746daa8b69291b1a6c6bff3b8643e1e3167c90dfcf419a` | 0 |
| packages/xrpl/src/models/utils/index.ts | 1796 | `ec468337f0b6955786677f60273d84bde7e8777789186f622c17c01047d0fc95` | 0 |
| packages/xrpl/src/models/utils/mptokenMetadata.ts | 15106 | `ee46c62fe78e936ac4db53e587a18d672118b5d08884d5f3cef4d24796c18f00` | 0 |
| packages/xrpl/src/sugar/autofill.ts | 23564 | `4cedeffb3b35108c2da6604e9466c4bfe6bc60987ca0ad3b5b09ca43468f0c94` | 0 |
| packages/xrpl/src/sugar/balances.ts | 499 | `6131bbd2c0f01c6818739eabf49b94d8ed155e254ed49e6c3c5cab382bfe537f` | 0 |
| packages/xrpl/src/sugar/getFeeXrp.ts | 1278 | `cc10af42c8d97bbfdb94a5637ef690879c3941a14bcc74a753c2862b200d66dc` | 0 |
| packages/xrpl/src/sugar/getOrderbook.ts | 6264 | `bd432c860982daceefe66cf9ef856e63599848d31bfbe9890c873f54e6d65f70` | 0 |
| packages/xrpl/src/sugar/index.ts | 89 | `b261a7aa98c097d99e6fa595b97565122a4d1d0d6cbed3e4ad91e9aac0497460` | 0 |
| packages/xrpl/src/sugar/submit.ts | 11476 | `4150ac053ef83aafccf062112247259d648ddd3faab862d7b0bd858651456f2f` | 0 |
| packages/xrpl/src/sugar/utils.ts | 926 | `9ca1d17eaf7d5351811b1fca5eb95b5a9bc47110979c53b893dcce2b46722265` | 0 |
| packages/xrpl/src/sugar/validateSponsorship.ts | 9624 | `9d5bf540e2ce7944db664d712782aa8bf49004a857963b8d19d9d85bb8b440a7` | 0 |
| packages/xrpl/src/utils/collections.ts | 2057 | `e36348ea35a1ba3b73e671e6f9e95ba6c720d81d693fca64b08c1efee1d42d31` | 0 |
| packages/xrpl/src/utils/derive.ts | 877 | `dc19b9fcf0984ddcba2ac45c92d7b3d62e7712ff0e58637331b6e1a46df7767b` | 0 |
| packages/xrpl/src/utils/getBalanceChanges.ts | 5312 | `639999d28ef8143f0515ac437933fdda907e02155f14030cf8402cb7fe46c518` | 0 |
| packages/xrpl/src/utils/getNFTokenID.ts | 3803 | `feb04f1216ba6fb1f44aff83b8e5a5f67dd5553fa040fddccd9dec6df026d841` | 0 |
| packages/xrpl/src/utils/getXChainClaimID.ts | 2093 | `4464c1fe7bab0234114318e1f2ba306be9dab93c9ab370caf3c62e4342ce54cd` | 0 |
| packages/xrpl/src/utils/hashes/HashPrefix.ts | 1077 | `01431e043ee61cba02cd8a3ba2f3b52c5a5e1e027ab1e682b9b191fd65acf9bf` | 0 |
| packages/xrpl/src/utils/hashes/SHAMap/InnerNode.ts | 3244 | `d79eb05f6d6bd995c91df5d2b68feebb74b67b8d198b0042d3fb2c64aed52de8` | 0 |
| packages/xrpl/src/utils/hashes/SHAMap/LeafNode.ts | 1975 | `9bb662366ba57107eb8bf3325a8e4fbbf0e9a6b0ccd21b1c282aac992029d4d4` | 0 |
| packages/xrpl/src/utils/hashes/SHAMap/index.ts | 925 | `879f087e5105b534abbe9b33b7cab278b3f6e6286d447a51cc5e1bd99fc892f2` | 0 |
| packages/xrpl/src/utils/hashes/SHAMap/node.ts | 293 | `f069aefaafc2715701e140998a3b3a84573fa6c8eec74f4abb6cae074beb85e8` | 0 |
| packages/xrpl/src/utils/hashes/hashLedger.ts | 6899 | `b2bfbacd786ea0026819d4b855ead5a04244038a6a48063d0d3a21dac855eabc` | 0 |
| packages/xrpl/src/utils/hashes/index.ts | 7536 | `9353c350d2632c241e01c4b1f0b3fefbee557ff5ae1366749466ccd3b85e5bbf` | 0 |
| packages/xrpl/src/utils/hashes/ledgerSpaces.ts | 831 | `a0e6d57a4ac4353d2c389b7bd8b6565213c295e3c403df9a176df8a87515ae70` | 0 |
| packages/xrpl/src/utils/hashes/sha512Half.ts | 395 | `c7d9a10d81d60ab83dbdd4be95201cd9ab9152d0ea3db2c8ae87191fd6692cbb` | 0 |
| packages/xrpl/src/utils/index.ts | 6346 | `afd71f8c3d6323ac2ceed259882f35e0ba5862c14056e7a9718a1247796f7ca1` | 0 |
| packages/xrpl/src/utils/parseNFTokenID.ts | 3624 | `dc4afa2650bf7e0cb75c15502db337a024d0509f2ebe6cffeab878fc1f264d3e` | 0 |
| packages/xrpl/src/utils/quality.ts | 4846 | `cc4766952613604ec2812879bffbe74d5bbbdcd967e3d7e309fd898d8d6be97c` | 0 |
| packages/xrpl/src/utils/signPaymentChannelClaim.ts | 760 | `7c62fb8f41dcdcdf602419542a884be06be56d511c46344f5cc1a57eee1935c5` | 0 |
| packages/xrpl/src/utils/stringConversion.ts | 939 | `6163819a27a4df49ce55fede0bb82b0a1babb1daa91f0826fa34c365d5575ff3` | 0 |
| packages/xrpl/src/utils/timeConversion.ts | 1479 | `e962c2a15a4aa3c539f2083b4e1c6ae57a8b6104078c8a4915ff06272e1cb45c` | 0 |
| packages/xrpl/src/utils/verifyPaymentChannelClaim.ts | 951 | `e06e657148ea03f7f35a6add588f591c1b053857987d09bd836db5e6aad6b0a4` | 0 |
| packages/xrpl/src/utils/xrpConversion.ts | 3112 | `a76aed23f264300a0e85fbf402c92d5512659af2e9f3c85c9085346c50d30fdb` | 0 |
| packages/xrpl/tools/createValidate.js | 3993 | `a810bfd7442a03fec3ce5c8a5f0d04827a80b04fc593c4bcc7d7c3eab015d828` | 0 |
| packages/xrpl/tools/createValidateTests.js | 4909 | `5c28514bcc9f9ea9edde55899867dd04d00b1a2d9a72d559c83987cceb5c4d9e` | 0 |
| packages/xrpl/tools/generateModels.js | 8597 | `e7b84d65578bc74af06aa2532a6244523810a7e3c8764ec8a2284535a92657f5` | 0 |
| packages/xrpl/webpack.base.config.js | 420 | `a5780930d5356424f376ed7100f5f79d6ee07b4b2d0b826121757dc957bb1b20` | 0 |
| packages/xrpl/webpack.config.js | 248 | `5bfec6746840afac614f3bd26cd2da10d0728b30ed10a4bde2422c8c2497658b` | 0 |
| webpack.config.js | 1596 | `bbd5aea2e4c0ef67c7b95dfb2bc0143a60b73ef66007d79b8028d69a471101eb` | 0 |
| webpack.test.config.js | 1482 | `4d5ba4bb5f4f99cfd3e55230fa5e75f4bd2095934db47b0f3e99e74d75f3cbf2` | 0 |
