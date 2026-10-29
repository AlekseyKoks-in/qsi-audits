# Security & Post-Quantum Readiness Audit Report

**Project:** trezor-vendored-crypto @ 72489948b3c4 · Trezor (vendored primitives) — public repository (passive review)
| | |
|---|---|
| Organization | QSI |
| Report date | 2026-10-29 05:35 UTC |
| Report version | 1 |
| Audit run | 2479351b-857a-4bec-888f-076ff6716d7d (Document audit) |
| Analyzer engine | qsi-engine 1.2.0 |
| Risk profile | Crypto exchange, custodian or wallet |
| Content SHA-256 | `0946734472e0712a577bfef0a07be6b9e19572e9b4966a66229e52b4f0abe051` |
| Signature key (Ed25519, SHA-256 fingerprint; the signature is the separate file report.sig.json) | `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e` |
> This report presents automated and documented analysis results for the stated scope. It is not a legal opinion, a certification or an attestation of compliance with any standard.

## 1. Executive summary

- Critical: **0**
- High: **0**
- Medium: **4**
- Low: **0**
- Info: **0**

- Confirmed technical vulnerability: 0
- Known vulnerable component: 0
- Confirmed configuration error: 0
- Potential cryptographic risk: 0
- Long-term post-quantum risk: 4
- Improvement recommendation: 0
- Insufficient data: 0

Mosca's inequality (x + y > z): x = 10, y = 5, z = 8 → migration would finish too late under this scenario. _z is a planning assumption chosen per risk profile, not a prediction. A cryptographically relevant quantum computer is not publicly known to exist today._

Analyst review: 4 confirmed, 0 not applicable, 0 dismissed as false positives.

**Post-quantum maturity: Level 1 of 4 — post-quantum code present, not wired.** Next step: Wire the existing post-quantum primitive into a critical path (key wrapping or the channel) behind a hybrid construction, and test interoperability.

## 2. Scope and boundaries

Mode: Document audit

Repository: <https://github.com/trezor/trezor-firmware> @ `72489948b3c44a37598de9da658be28e4fabb4ae` — evidence links open the lines at this commit.

519 files, 5085520 bytes in total, 0 redaction(s); the per-file SHA-256 list is in appendix C.

## 3. Methodology

| Area | Status | Count | Examples |
|---|---|---|---|
| source_code | checked | 519 | vendor/mldsa-native/.github/actions/cbmc/report.py: 297 lines scanned with 16 rule patterns and 123 registry patterns; vendor/mldsa-native/dev/aarch64_clean/meta.h: 247 lines scanned with 16 rule patterns and 123 registry patterns; vendor/mldsa-native/dev/aarch64_clean/src/aarch64_zetas.c: 231 lines scanned with 16 rule patterns and 123 registry patterns |

_Long lists are grouped here; the full per-file list is in the JSON report, signed with the same key._

## 4. Assets examined and not examined

- None

## 5. Architecture overview

Static review of the source tree trezor-vendored-crypto at 72489948b3c44a37598de9da658be28e4fabb4ae. 519 files analysed; of 1159 files, 174 are test, fuzzing, benchmark or example code and were left out, 466 are not read by any analyzer, 0 exceed the per-file limit and 0 did not fit the total limit. 519 files come from directories a .gitmodules pins and are read as shipped source rather than skipped as a dependency cache. No requests were sent to the owner's systems.

## 6. Overall security posture

- Indicative posture index: **100** / 100 — _Derived from findings in scope (confirmed and potential issues weighted by severity). Indicative only; not comparable across differently scoped audits._
- Quantum-vulnerable share of inventory: 26.8%

## 7. Detailed findings

### QSI-2026-06405 — Quantum-vulnerable ECDSA: transaction and message signing (24 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium
> **Analyst review (QSI review, 2026-10-29): confirmed by the analyst.** Correct: 24 files of vendor/secp256k1-zkp, Blockstream's fork of libsecp256k1, which is what a Trezor actually signs Bitcoin transactions with. The main audit's 73 Shor-breakable rows count the call sites in core/embed/sec; these are the implementation under them. The two should be read together and not added together — it is one dependency measured at two levels, which is why this bundle is not folded into the portfolio's per-codebase counts.
- Affected asset: `source-code:ECDSA:transaction_signing`
- Data source: vendor/secp256k1-zkp/contrib/lax_der_parsing.c
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.2.0 · 2026-10-29 05:35 UTC
- Priority score: 41.8 / 100
- CVSS v3.1: not applicable

82 reference(s) to ECDSA across 24 file(s), e.g. vendor/secp256k1-zkp/contrib/lax_der_parsing.c:11. Role, judged from paths, function names and nearby code: transaction and message signing. A CRQC derives the private key from a public key that is already known (on chain after the first spend, in reused addresses): funds and approvals controlled by these keys need a migration path.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open vendor/secp256k1-zkp/contrib/lax_der_parsing.c:11 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [vendor/secp256k1-zkp/contrib/lax_der_parsing.c](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/vendor/secp256k1-zkp/contrib/lax_der_parsing.c#L11) · line 11 · SHA-256 9197354c850cb53bbc475b348c0f97bb3f550706fcced8bf483336d626575330_

```
   10 | 
   11 | int ecdsa_signature_parse_der_lax(const secp256k1_context* ctx, secp256k1_ecdsa_signature* sig, const unsigned char *input, size_t inputlen) {
   12 |     size_t rpos, rlen, spos, slen;
```

_file_excerpt · [vendor/secp256k1-zkp/contrib/lax_der_parsing.c](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/vendor/secp256k1-zkp/contrib/lax_der_parsing.c#L19) · line 19 · SHA-256 234aeaaf6b28e1d2ff43854e60a3119e3c3f55229e18841e2dc766404eab65d0_

```
   18 |     /* Hack to initialize sig with a correctly-parsed but invalid signature. */
   19 |     secp256k1_ecdsa_signature_parse_compact(ctx, sig, tmpsig);
   20 | 
```

_file_excerpt · [vendor/secp256k1-zkp/contrib/lax_der_parsing.c](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/vendor/secp256k1-zkp/contrib/lax_der_parsing.c#L140) · line 140 · SHA-256 75ad5d0cba25ca64adb6d971da937879704b4abc8845c17dc1da9fa1eb773e5e_

```
  139 |     if (!overflow) {
  140 |         overflow = !secp256k1_ecdsa_signature_parse_compact(ctx, sig, tmpsig);
  141 |     }
```

_file_excerpt · [vendor/secp256k1-zkp/contrib/lax_der_parsing.h](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/vendor/secp256k1-zkp/contrib/lax_der_parsing.h#L57) · line 57 · SHA-256 25af7e242d92af0d3c46ae8d8a48030e247c4bfdeba65068030e64eb4c88c912_

```
   56 |    files (such as tests.c) without the need to set an explicit -I flag,
   57 |    which would be necessary to locate secp256k1.h. */
   58 | #ifndef SECP256K1_H
```

_file_excerpt · [vendor/secp256k1-zkp/contrib/lax_der_parsing.h](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/vendor/secp256k1-zkp/contrib/lax_der_parsing.h#L59) · line 59 · SHA-256 4c35a81e99a7eaf5ea7315346f3b8cacb0832f7c4a3b1a3d003ff0bd3b6a82c1_

```
   58 | #ifndef SECP256K1_H
   59 | #include <secp256k1.h>
   60 | #endif
```

_file_excerpt · [vendor/secp256k1-zkp/contrib/lax_der_parsing.h](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/vendor/secp256k1-zkp/contrib/lax_der_parsing.h#L88) · line 88 · SHA-256 85efcade66268dd4d0b42e8f31b634ea4cd93d9d55cdc2e036715108d8697665_

```
   87 |     const secp256k1_context* ctx,
   88 |     secp256k1_ecdsa_signature* sig,
   89 |     const unsigned char *input,
```

_file_excerpt · [vendor/secp256k1-zkp/contrib/lax_der_privatekey_parsing.h](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/vendor/secp256k1-zkp/contrib/lax_der_privatekey_parsing.h#L34) · line 34 · SHA-256 163cac24f6b60e798317e2383fb603da718e728035262dc9759d7cf3fbd47b4f_

```
   33 |    files (such as tests.c) without the need to set an explicit -I flag,
   34 |    which would be necessary to locate secp256k1.h. */
   35 | #ifndef SECP256K1_H
```

_file_excerpt · [vendor/secp256k1-zkp/contrib/lax_der_privatekey_parsing.h](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/vendor/secp256k1-zkp/contrib/lax_der_privatekey_parsing.h#L36) · line 36 · SHA-256 2741d1869779ddac4f151ac1740c338ba299b2bed7b98a38e6042acb62fca350_

```
   35 | #ifndef SECP256K1_H
   36 | #include <secp256k1.h>
   37 | #endif
```

_file_excerpt · [vendor/secp256k1-zkp/include/secp256k1.h](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/vendor/secp256k1-zkp/include/secp256k1.h#L74) · line 74 · SHA-256 712d2259ac1032ad406ddde4403d5a72e5739b8c7e004ad0b2293d26f4d10018_

```
   73 |  */
   74 | typedef struct secp256k1_ecdsa_signature {
   75 |     unsigned char data[64];
```

_file_excerpt · [vendor/secp256k1-zkp/include/secp256k1.h](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/vendor/secp256k1-zkp/include/secp256k1.h#L76) · line 76 · SHA-256 2ccd260bdbfd5dbcb2816a89d4808a078f7cf59fef64a70244b731ba3ec91ab9_

```
   75 |     unsigned char data[64];
   76 | } secp256k1_ecdsa_signature;
   77 | 
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains adopt them.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-06406 — Quantum-vulnerable Schnorr (BIP-340): transaction and message signing (4 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium
> **Analyst review (QSI review, 2026-10-29): confirmed by the analyst.** Correct, four files, the schnorrsig module of the same vendored library: Taproot spends.
- Affected asset: `source-code:Schnorr (BIP-340):transaction_signing`
- Data source: vendor/secp256k1-zkp/include/secp256k1_schnorrsig.h
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.2.0 · 2026-10-29 05:35 UTC
- Priority score: 41.8 / 100
- CVSS v3.1: not applicable

25 reference(s) to Schnorr (BIP-340) across 4 file(s), e.g. vendor/secp256k1-zkp/include/secp256k1_schnorrsig.h:82. Role, judged from paths, function names and nearby code: transaction and message signing. A CRQC derives the private key from a public key that is already known (on chain after the first spend, in reused addresses): funds and approvals controlled by these keys need a migration path.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open vendor/secp256k1-zkp/include/secp256k1_schnorrsig.h:82 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [vendor/secp256k1-zkp/include/secp256k1_schnorrsig.h](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/vendor/secp256k1-zkp/include/secp256k1_schnorrsig.h#L82) · line 82 · SHA-256 6aae3b20f8f8b503597acb97fe491246b6777b5a9660b8a41542605d18aab6f4_

```
   81 |  */
   82 | typedef struct secp256k1_schnorrsig_extraparams {
   83 |     unsigned char magic[4];
```

_file_excerpt · [vendor/secp256k1-zkp/include/secp256k1_schnorrsig.h](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/vendor/secp256k1-zkp/include/secp256k1_schnorrsig.h#L86) · line 86 · SHA-256 43d5f6045ac4e6b23daf11fd6c10022dca16ca76afd775c3ee898ddbef44d5bd_

```
   85 |     void *ndata;
   86 | } secp256k1_schnorrsig_extraparams;
   87 | 
```

_file_excerpt · [vendor/secp256k1-zkp/include/secp256k1_schnorrsig.h](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/vendor/secp256k1-zkp/include/secp256k1_schnorrsig.h#L119) · line 119 · SHA-256 1e555d327421285c8a81345e58876f5f2f017571adb2f2168aafc7c44770594c_

```
  118 |  */
  119 | SECP256K1_API int secp256k1_schnorrsig_sign32(
  120 |     const secp256k1_context *ctx,
```

_file_excerpt · [vendor/secp256k1-zkp/src/modules/musig/session_impl.h](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/vendor/secp256k1-zkp/src/modules/musig/session_impl.h#L626) · line 626 · SHA-256 a9274c7d82071c2c191759a1ad6acc91c4341fab17e9bfb18c95c5a25c535b29_

```
  625 |     secp256k1_musig_nonce_process_internal(&session_i.fin_nonce_parity, fin_nonce, &session_i.noncecoef, aggnonce_pts, agg_pk32, msg32);
  626 |     secp256k1_schnorrsig_challenge(&session_i.challenge, fin_nonce, msg32, 32, agg_pk32);
  627 | 
```

_file_excerpt · [vendor/secp256k1-zkp/src/modules/schnorrsig/bench_impl.h](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/vendor/secp256k1-zkp/src/modules/schnorrsig/bench_impl.h#L33) · line 33 · SHA-256 fc2c5559f32fc9bd9a85efef59a46eaf722b1b8e2745b837696cdf6a6c00259e_

```
   32 |         msg[1] = i >> 8;
   33 |         CHECK(secp256k1_schnorrsig_sign_custom(data->ctx, sig, msg, MSGLEN, data->keypairs[i], NULL));
   34 |     }
```

_file_excerpt · [vendor/secp256k1-zkp/src/modules/schnorrsig/bench_impl.h](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/vendor/secp256k1-zkp/src/modules/schnorrsig/bench_impl.h#L44) · line 44 · SHA-256 4f2e9b7b2529431d8190d606bbe0ce49659d6e5a1e0410625d931eacdcd05a06_

```
   43 |         CHECK(secp256k1_xonly_pubkey_parse(data->ctx, &pk, data->pk[i]) == 1);
   44 |         CHECK(secp256k1_schnorrsig_verify(data->ctx, data->sigs[i], data->msgs[i], MSGLEN, &pk));
   45 |     }
```

_file_excerpt · [vendor/secp256k1-zkp/src/modules/schnorrsig/bench_impl.h](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/vendor/secp256k1-zkp/src/modules/schnorrsig/bench_impl.h#L80) · line 80 · SHA-256 0ca8c9b51520014576b4c622e33014e8b93cc7c4bd0bc826e9cd4563a3642698_

```
   79 |         CHECK(secp256k1_keypair_create(data.ctx, keypair, sk));
   80 |         CHECK(secp256k1_schnorrsig_sign_custom(data.ctx, sig, msg, MSGLEN, keypair, NULL));
   81 |         CHECK(secp256k1_keypair_xonly_pub(data.ctx, &pk, NULL, keypair));
```

_file_excerpt · [vendor/secp256k1-zkp/src/modules/schnorrsig/main_impl.h](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/vendor/secp256k1-zkp/src/modules/schnorrsig/main_impl.h#L106) · line 106 · SHA-256 010e6d7bb200794264a2bce239dc7cc1cf2fb59c2ce7595deb9f5d4cea0f2cf7_

```
  105 |  * SHA256 to SHA256("BIP0340/challenge")||SHA256("BIP0340/challenge"). */
  106 | static void secp256k1_schnorrsig_sha256_tagged(secp256k1_sha256 *sha) {
  107 |     secp256k1_sha256_initialize(sha);
```

_file_excerpt · [vendor/secp256k1-zkp/src/modules/schnorrsig/main_impl.h](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/vendor/secp256k1-zkp/src/modules/schnorrsig/main_impl.h#L119) · line 119 · SHA-256 4a22e3f79b439b475e0b65863dad24c6233db490ff1eedb9bb5d1a4d8f99c68c_

```
  118 | 
  119 | static void secp256k1_schnorrsig_challenge(secp256k1_scalar* e, const unsigned char *r32, const unsigned char *msg, size_t msglen, const unsigned char *pubkey32)
  120 | {
```

_file_excerpt · [vendor/secp256k1-zkp/src/modules/schnorrsig/main_impl.h](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/vendor/secp256k1-zkp/src/modules/schnorrsig/main_impl.h#L125) · line 125 · SHA-256 521a9c533807ec4184854d2f7d1ebe0afbbe1f0b7ec13d0c705a0ab7bbb7eb2e_

```
  124 |     /* tagged hash(r.x, pk.x, msg) */
  125 |     secp256k1_schnorrsig_sha256_tagged(&sha);
  126 |     secp256k1_sha256_write(&sha, r32, 32);
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains adopt them.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-06404 — Quantum-vulnerable Ed25519: role not determined (5 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium
> **Analyst review (QSI review, 2026-10-29): confirmed by the analyst.** Correct and directly relevant to the migration story rather than to spending. Ed25519 is what the device's boot header is signed with today — core/embed/sec/image/boot_header.c:81 in the main audit — and these five rows are its implementation. This is the primitive SLH-DSA is being added alongside, so the pair Ed25519-plus-SLH-DSA in one header is the whole point: the root of trust is mid-migration, carrying both. Firmware signatures are forward-only exposure, but the consequence of a forgery is arbitrary code on a device holding keys, which is why a signer's boot path is where post-quantum signatures matter first even though the spending path is the louder number.
- Affected asset: `source-code:Ed25519:general`
- Data source: vendor/mldsa-native/mldsa/mldsa_native.c
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.2.0 · 2026-10-29 05:35 UTC
- Priority score: 40.2 / 100
- CVSS v3.1: not applicable

6 reference(s) to Ed25519 across 5 file(s), e.g. vendor/mldsa-native/mldsa/mldsa_native.c:212. Role, judged from paths, function names and nearby code: role not determined. The code does not show what the keys protect; review decides the priority.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open vendor/mldsa-native/mldsa/mldsa_native.c:212 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [vendor/mldsa-native/mldsa/mldsa_native.c](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/vendor/mldsa-native/mldsa/mldsa_native.c#L212) · line 212 · SHA-256 d866878f98e2f9d8188f28872711433022de6c18d69a1561655c918b959277b6_

```
  211 | #undef crypto_sign
  212 | #undef crypto_sign_keypair
  213 | #undef crypto_sign_open
```

_file_excerpt · [vendor/mldsa-native/mldsa/mldsa_native.h](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/vendor/mldsa-native/mldsa/mldsa_native.h#L866) · line 866 · SHA-256 cdc8f37b350eb9742546761cc89f9ecfc27e71b175d4e86246d3494cbdfa95f0_

```
  865 | 
  866 | #define crypto_sign_keypair MLD_API_NAMESPACE(keypair)
  867 | #define crypto_sign_signature MLD_API_NAMESPACE(signature)
```

_file_excerpt · [vendor/sphincsplus/ref/PQCgenKAT_sign.c](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/vendor/sphincsplus/ref/PQCgenKAT_sign.c#L118) · line 118 · SHA-256 86be2a14cdae0837afaa6df56e5c682e5cd4574050a77bd7b777631c9430b2ee_

```
  117 |         // Generate the public/private keypair
  118 |         if ( (ret_val = crypto_sign_keypair(pk, sk)) != 0) {
  119 |             printf("crypto_sign_keypair returned <%d>\n", ret_val);
```

_file_excerpt · [vendor/sphincsplus/ref/PQCgenKAT_sign.c](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/vendor/sphincsplus/ref/PQCgenKAT_sign.c#L119) · line 119 · SHA-256 26d224d32ba13de87a6b88d4993e9684549d45fae1b6992ac390883a660d8339_

```
  118 |         if ( (ret_val = crypto_sign_keypair(pk, sk)) != 0) {
  119 |             printf("crypto_sign_keypair returned <%d>\n", ret_val);
  120 |             return KAT_CRYPTO_FAILURE;
```

_file_excerpt · [vendor/sphincsplus/ref/api.h](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/vendor/sphincsplus/ref/api.h#L49) · line 49 · SHA-256 639ca6453aba334ed81ce97556bd5c8c134495bf530bc8e7b87b50a88052b0af_

```
   48 |  */
   49 | int crypto_sign_keypair(unsigned char *pk, unsigned char *sk);
   50 | 
```

_file_excerpt · [vendor/sphincsplus/ref/sign.c](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/vendor/sphincsplus/ref/sign.c#L83) · line 83 · SHA-256 689d2d643099c5e9f712db4d28751748d7fff094f1301c64ccaeae54aa1c5388_

```
   82 |  */
   83 | int crypto_sign_keypair(unsigned char *pk, unsigned char *sk)
   84 | {
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it; introduce an abstraction layer for crypto-agility.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-06407 — Quantum-vulnerable ECDH: role not determined (1 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium
> **Analyst review (QSI review, 2026-10-29): confirmed by the analyst.** One row, and the only retroactive one here: key agreement in the vendored secp256k1-zkp. Where a shared secret derived through it protects anything stored or recorded, a copy taken today becomes readable once a CRQC exists. Unlike the signature rows it can be hardened without a consensus change, by wrapping the agreed secret under a hybrid KEM.
- Affected asset: `source-code:ECDH:general`
- Data source: vendor/secp256k1-zkp/src/bench.c
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.2.0 · 2026-10-29 05:35 UTC
- Priority score: 40.2 / 100
- CVSS v3.1: not applicable

4 reference(s) to ECDH across 1 file(s), e.g. vendor/secp256k1-zkp/src/bench.c:24. Role, judged from paths, function names and nearby code: role not determined. The code does not show what the keys protect; review decides the priority.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open vendor/secp256k1-zkp/src/bench.c:24 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [vendor/secp256k1-zkp/src/bench.c](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/vendor/secp256k1-zkp/src/bench.c#L24) · line 24 · SHA-256 6ec91ca104f465f4b861193bee0ed1f6d91c4074fb5085511ca06c7dd6747616_

```
   23 | #ifdef ENABLE_MODULE_ECDH
   24 |     printf("    - ECDH key exchange (optional module)\n");
   25 | #endif
```

_file_excerpt · [vendor/secp256k1-zkp/src/bench.c](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/vendor/secp256k1-zkp/src/bench.c#L54) · line 54 · SHA-256 b21ecd8d53157d4f920477f57713fa34b7fe6379df61daa64f27e4a77f9133e1_

```
   53 | #ifdef ENABLE_MODULE_ECDH
   54 |     printf("    ecdh              : ECDH key exchange algorithm\n");
   55 | #endif
```

_file_excerpt · [vendor/secp256k1-zkp/src/bench.c](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/vendor/secp256k1-zkp/src/bench.c#L68) · line 68 · SHA-256 ae7392892e7a0840c3596f3442ca87927d89cc694ec91267d2a73193091dac83_

```
   67 |     printf("    ellswift_keygen   : ElligatorSwift key generation\n");
   68 |     printf("    ellswift_ecdh     : ECDH on ElligatorSwift keys\n");
   69 | #endif
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Classify each usage, record data lifetimes, and plan migration to Hybrid key establishment with ML-KEM (FIPS 203), e.g. X25519MLKEM768 in TLS 1.3 or mlkem768x25519-sha256 in SSH; introduce an abstraction layer for crypto-agility.

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

### Post-quantum maturity: Level 1 of 4 — post-quantum code present, not wired

- Present, not wired: ML-DSA — vendor/mldsa-native/integration/liboqs/config_aarch64.h
- Present, not wired: ML-DSA — vendor/mldsa-native/integration/liboqs/config_c.h
- Present, not wired: ML-DSA — vendor/mldsa-native/integration/liboqs/config_x86_64.h
- Present, not wired: ML-DSA — vendor/mldsa-native/mldsa/mldsa_native.c
- Present, not wired: ML-DSA — vendor/mldsa-native/mldsa/mldsa_native.h

**Next step:** Wire the existing post-quantum primitive into a critical path (key wrapping or the channel) behind a hybrid construction, and test interoperability.

_Levels: 0 none; 1 present, not wired; 2 in use outside the critical paths; 3 hybrid in a critical path; 4 post-quantum by default in the critical paths (root of trust, key wrapping, channel key exchange). Judged from code and manifests._

### What the quantum-vulnerable algorithms do

| Role | Algorithms (files) | ID | First step |
|---|---|---|---|
| **transaction and message signing** | ECDSA (24), Schnorr (BIP-340) (4) | QSI-2026-06405, QSI-2026-06406 | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains adopt them |
| **role not determined** | Ed25519 (5), ECDH (1) | QSI-2026-06404, QSI-2026-06407 | Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it; introduce an abstraction layer for crypto-agility |

_Roles are judged from file paths, function names and the code around each match; review confirms them. Root-of-trust keys and wrapped keys come first: they are hard to replace or can be recorded today._
No readiness questionnaire was completed for this project.

### Quantum algorithms relevant to this inventory

| Quantum algorithm | Effect | Attack model | Inventoried algorithms (rows) | What it means for this audit |
|---|---|---|---|---|
| Shor's algorithm — elliptic-curve discrete logarithms | breaks | Q1 | ECDH (1), ECDSA (28), Ed25519 (5), Schnorr (BIP-340) (4) | Elliptic-curve keys are expected to fall before RSA keys of comparable classical strength. On blockchains, coins whose public key is already on chain (reused addresses, pay-to-public-key and Taproot outputs) are exposed first; plan the move to post-quantum signatures and avoid key reuse in the meantime. |
| Grover's algorithm — key search and preimages | weakens (larger keys restore the margin) | Q1 | AES-256 (1), SHA-2 (1), SLH-DSA (94) | Not a break. 256-bit keys (AES-256, ChaCha20) keep a comfortable margin; AES-128 meets NIST category 1, while some authorities ask for 256-bit keys in quantum-resistant contexts (see the AES-128 entry). Prefer 256-bit keys for long-lived data; 256-bit hashes need no change for preimage resistance. |
| Brassard–Høyer–Tapp — collision search | weakens (larger keys restore the margin) | Q1 | SHA-2 (1) | 256-bit hashes (SHA-256, SHA3-256) remain adequate for collision resistance; 160-bit hashes are already weak classically (SHA-1 collisions are practical). Use 384/512-bit hashes where NIST categories 4–5 are required. |
| Quantum lattice sieving | included in standard parameters | Q1 | ML-DSA (8) | No change for ML-KEM or ML-DSA at the standard parameter sets. A 2024 claim of a polynomial-time quantum LWE algorithm was withdrawn after a bug was found (see claims). |

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
| P3 | QSI-2026-06405 | Add ECDSA usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-06406 | Add Schnorr (BIP-340) usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-06404 | Add Ed25519 usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-06407 | Add ECDH usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P4 | QSI-2026-06405 | Plan migration of ECDSA to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-06406 | Plan migration of Schnorr (BIP-340) to  (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows  or a hybrid scheme in use. |
| P4 | QSI-2026-06404 | Plan migration of Ed25519 to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-06407 | Plan migration of ECDH to Hybrid key establishment with ML-KEM (FIPS 203), e.g. X25519MLKEM768 in TLS 1.3 or mlkem768x25519-sha256 in SSH (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows Hybrid key establishment with ML-KEM (FIPS 203), e.g. X25519MLKEM768 in TLS 1.3 or mlkem768x25519-sha256 in SSH or a hybrid scheme in use. |

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
20. NIST IR 8547 — Transition to Post-Quantum Cryptography Standards — NIST. <https://csrc.nist.gov/pubs/ir/8547/ipd> (initial public draft (November 2024); proposes deprecating quantum-vulnerable public-key algorithms after 2030 and disallowing them after 2035 — dates may change in the final version)
21. NIST — Post-Quantum Cryptography Standardization: Evaluation Criteria, Security (Call for Proposals, Section 4.A.5) — NIST. <https://csrc.nist.gov/Projects/Post-Quantum-Cryptography/Post-Quantum-Cryptography-Standardization/Evaluation-Criteria/Security-(Evaluation-Criteria)> (security categories: AES-128 key search 2^170/MAXDEPTH quantum gates, AES-192 2^233/MAXDEPTH, AES-256 2^298/MAXDEPTH; MAXDEPTH 2^40–2^96)
22. P. W. Shor — Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms on a Quantum Computer (SIAM J. Comput., 1997) — SIAM. <https://doi.org/10.1137/S0097539795293172> (peer-reviewed article)
23. R. Babbush et al. — Securing Elliptic Curve Cryptocurrencies against Quantum Vulnerabilities: Resource Estimates and Mitigations (arXiv:2603.28846) — arXiv. <https://arxiv.org/abs/2603.28846> (preprint (2026-03-30, v2 2026-04-15): 256-bit ECDLP with < 1200 logical qubits and < 90 M Toffoli gates (or < 1450 and < 70 M); < 500,000 physical qubits at 10^-3 error, minutes)
24. S. Jaques, M. Naehrig, M. Roetteler, F. Virdia — Implementing Grover oracles for quantum key search on AES and LowMC (EUROCRYPT 2020; arXiv:1910.01700) — Springer / arXiv. <https://arxiv.org/abs/1910.01700> (peer-reviewed article: lower cost estimates for the AES key searches that define the NIST categories)

## Appendices: Cryptographic inventory

| Algorithm | Parameter | Library | Quantum status | Classical status | Count | Locations | Examples |
|---|---|---|---|---|---|---|---|
| AES-256 | AES-256 |  | reduced margin (Grover), approved | acceptable | 1 | 1 | vendor/sphincsplus/ref/rng.c:125 |
| SHA-2 | SHA-256 |  | Grover: acceptable to NIST, below ECCG/ANSSI guidance | acceptable | 1 | 1 | vendor/sphincsplus/vectors.py:59 |
| ML-DSA |  |  | post-quantum | acceptable | 8 | 8 | vendor/mldsa-native/integration/liboqs/config_aarch64.h:315; vendor/mldsa-native/integration/liboqs/config_c.h:319; vendor/mldsa-native/integration/liboqs/config_x86_64.h:317 |
| SLH-DSA |  |  | post-quantum | acceptable | 94 | 94 | vendor/sphincsplus/haraka-aesni/context.h:10; vendor/sphincsplus/haraka-aesni/haraka.c:117; vendor/sphincsplus/haraka-aesni/harakax4.h:19 |
| ECDH |  |  | vulnerable (Shor) | acceptable | 1 | 1 | vendor/secp256k1-zkp/src/bench.c:24 |
| ECDSA |  |  | vulnerable (Shor) | acceptable | 7 | 7 | vendor/secp256k1-zkp/contrib/lax_der_parsing.c:11; vendor/secp256k1-zkp/contrib/lax_der_parsing.h:88; vendor/secp256k1-zkp/include/secp256k1.h:74 |
| ECDSA | secp256k1 |  | vulnerable (Shor) | acceptable | 21 | 21 | vendor/secp256k1-zkp/contrib/lax_der_parsing.h:57; vendor/secp256k1-zkp/contrib/lax_der_privatekey_parsing.h:34; vendor/secp256k1-zkp/include/secp256k1_ecdh.h:4 |
| Ed25519 | Ed25519 |  | vulnerable (Shor) | acceptable | 5 | 5 | vendor/mldsa-native/mldsa/mldsa_native.c:212; vendor/mldsa-native/mldsa/mldsa_native.h:866; vendor/sphincsplus/ref/PQCgenKAT_sign.c:118 |
| Schnorr (BIP-340) |  |  | vulnerable (Shor) | acceptable | 4 | 4 | vendor/secp256k1-zkp/include/secp256k1_schnorrsig.h:82; vendor/secp256k1-zkp/src/modules/musig/session_impl.h:626; vendor/secp256k1-zkp/src/modules/schnorrsig/bench_impl.h:33 |

_Long lists are grouped here; the full per-file list is in the JSON report, signed with the same key._

## Appendices: Input files

| File | Size | SHA-256 | Redactions |
|---|---|---|---|
| vendor/mldsa-native/.github/actions/cbmc/report.py | 8847 | `6fa18f2c8481cc906f39b461fcf770b78b81af81d5e04183d0dafeede2874a81` | 0 |
| vendor/mldsa-native/dev/aarch64_clean/meta.h | 9372 | `86458b409219c5b521acd1c8e780a7dd5b680ab1607f548861cbf98a09ffbd59` | 0 |
| vendor/mldsa-native/dev/aarch64_clean/src/aarch64_zetas.c | 14368 | `87e22e4dd92e86f655870785fc8a6f40be187b543c0466920092f69daace620d` | 0 |
| vendor/mldsa-native/dev/aarch64_clean/src/arith_native_aarch64.h | 6497 | `406b41271328f5f5488b25a2dd061787c2d73bc4e1cc1e0b13ce7218860478ad` | 0 |
| vendor/mldsa-native/dev/aarch64_clean/src/polyz_unpack_table.c | 1417 | `0961cb66fd4951a3b01a243cf6886949d497b7ed19fefc7264d4507362ed87e6` | 0 |
| vendor/mldsa-native/dev/aarch64_clean/src/rej_uniform_eta_table.c | 25597 | `9bd3425816dcc0c21115f6955cc8830c4cdc3c7bebb1e1d6ed76ec717db50115` | 0 |
| vendor/mldsa-native/dev/aarch64_clean/src/rej_uniform_table.c | 2295 | `3308702a2208ea746e77c02792fa47ccfd0ea7ed7fc439e7cbcfde39d668c82a` | 0 |
| vendor/mldsa-native/dev/aarch64_opt/meta.h | 9372 | `86458b409219c5b521acd1c8e780a7dd5b680ab1607f548861cbf98a09ffbd59` | 0 |
| vendor/mldsa-native/dev/aarch64_opt/src/aarch64_zetas.c | 14368 | `87e22e4dd92e86f655870785fc8a6f40be187b543c0466920092f69daace620d` | 0 |
| vendor/mldsa-native/dev/aarch64_opt/src/arith_native_aarch64.h | 6497 | `406b41271328f5f5488b25a2dd061787c2d73bc4e1cc1e0b13ce7218860478ad` | 0 |
| vendor/mldsa-native/dev/aarch64_opt/src/polyz_unpack_table.c | 1417 | `0961cb66fd4951a3b01a243cf6886949d497b7ed19fefc7264d4507362ed87e6` | 0 |
| vendor/mldsa-native/dev/aarch64_opt/src/rej_uniform_eta_table.c | 25597 | `9bd3425816dcc0c21115f6955cc8830c4cdc3c7bebb1e1d6ed76ec717db50115` | 0 |
| vendor/mldsa-native/dev/aarch64_opt/src/rej_uniform_table.c | 2295 | `3308702a2208ea746e77c02792fa47ccfd0ea7ed7fc439e7cbcfde39d668c82a` | 0 |
| vendor/mldsa-native/dev/fips202/aarch64/auto.h | 1988 | `b47134bffe6ce1469e0c94c773d7fc03f317e9882917347de0f5699df98c9758` | 0 |
| vendor/mldsa-native/dev/fips202/aarch64/src/fips202_native_aarch64.h | 2478 | `184ac5106fe5e4501fb10bb1e0db4c5b55691c0d7647db00c9eb75495c9b52a9` | 0 |
| vendor/mldsa-native/dev/fips202/aarch64/src/keccakf1600_round_constants.c | 1996 | `c9351871c008c57156ea5b5192e39ffbef7dc617bd944c640ef8bb06c6433c7b` | 0 |
| vendor/mldsa-native/dev/fips202/aarch64/x1_scalar.h | 757 | `6f6204bf6b4a6bf83c3e8a8c2dd926832269fdd5d0d5a851af98237f21fe324c` | 0 |
| vendor/mldsa-native/dev/fips202/aarch64/x1_v84a.h | 956 | `9ba4f0efbe1c57790fa2bfdad454e435878610adb92738e454f858b575c29882` | 0 |
| vendor/mldsa-native/dev/fips202/aarch64/x2_v84a.h | 1047 | `9f2db3cabcd572733ca96019640200dac1d23729395c3d9f933778536f3045d0` | 0 |
| vendor/mldsa-native/dev/fips202/aarch64/x4_v8a_scalar.h | 835 | `fd36b58eab09c739f064d062437dc849345f255e7119b71a3e6536ddb5f1a25d` | 0 |
| vendor/mldsa-native/dev/fips202/aarch64/x4_v8a_v84a_scalar.h | 1032 | `a63e538011f4176b0e083f42cc35ef7c79ce1724fc21fb756c130f658d7855e2` | 0 |
| vendor/mldsa-native/dev/fips202/armv81m/mve.h | 813 | `0e2257310cfa60a98474c1d9201d7306f42ed5846406c37e4d8f12bbcb4d2df7` | 0 |
| vendor/mldsa-native/dev/fips202/armv81m/src/fips202_native_armv81m.h | 794 | `19f6ab96c9005836e0d2b945ac2bcb15f1b976fa4d19fd05869de488315739c7` | 0 |
| vendor/mldsa-native/dev/fips202/armv81m/src/keccak_f1600_x4_mve.c | 4687 | `03dd17852b4827d662ff622de4070b392ca5c590ef36de0cad9d6c0d831f9a31` | 0 |
| vendor/mldsa-native/dev/fips202/armv81m/src/keccakf1600_round_constants.c | 1729 | `9b8bf66e1bbf69d8ada688d0ebb029a4b57d1053ce3b0f6767240c5b740d4d1c` | 0 |
| vendor/mldsa-native/dev/x86_64/meta.h | 10542 | `5a629bba590fc8b7f8ade17e07a7e28ad93cf2e7007d8bf91fcbfaf46bfd1c0a` | 0 |
| vendor/mldsa-native/dev/x86_64/src/arith_native_x86_64.h | 5074 | `e52ef79ddefd09e1bf941a2794435393e8e2cd8c9e1916504342bcd1550a64c9` | 0 |
| vendor/mldsa-native/dev/x86_64/src/consts.c | 9085 | `25ab5b8f9def84990da5cd747f2ff2298c684c6c6fc2441ed79c488fc5f7b8f6` | 0 |
| vendor/mldsa-native/dev/x86_64/src/consts.h | 806 | `9f19c24b4b0c6b3de27568a98b41f5e59eafd8c060dee848992c443adaa95f76` | 0 |
| vendor/mldsa-native/dev/x86_64/src/poly_caddq_avx2.c | 1609 | `07a5d8faa06b24399aed68397059063a4afbc8fe8ebedd903f9aa3730b97c6ac` | 0 |
| vendor/mldsa-native/dev/x86_64/src/poly_chknorm_avx2.c | 1271 | `366ff5b9bac1e0d0cf3aedecbc5f3de0ee9677c9fd940091b7ae08dff66433fe` | 0 |
| vendor/mldsa-native/dev/x86_64/src/poly_decompose_32_avx2.c | 5971 | `a0cf2f3a88c685d1d8f78799baa6aa8878e54a17144b4fe3c79b85fd3d83b48d` | 0 |
| vendor/mldsa-native/dev/x86_64/src/poly_decompose_88_avx2.c | 5871 | `2a389287fc5ac137852aad1373f65cc11da9f178063296876f70bff0714fe687` | 0 |
| vendor/mldsa-native/dev/x86_64/src/poly_use_hint_32_avx2.c | 3690 | `87dccba1100f78804576cd41826e13ccc4598e0d36f6fc031d67a42a7422a7fb` | 0 |
| vendor/mldsa-native/dev/x86_64/src/poly_use_hint_88_avx2.c | 3673 | `00d6bd43e97a75c44da4adebd314aadbe77dc31c2889489aadb33ed232950a2a` | 0 |
| vendor/mldsa-native/dev/x86_64/src/polyz_unpack_17_avx2.c | 3834 | `16d0f450551f80edecd5c26fa6025ff54532589a0ca4360cff09fd5378557520` | 0 |
| vendor/mldsa-native/dev/x86_64/src/polyz_unpack_19_avx2.c | 4005 | `2c1a08402202bad2183b346fa262a88de442f0164bb25d1c1447e0bc5f63f89e` | 0 |
| vendor/mldsa-native/dev/x86_64/src/rej_uniform_avx2.c | 6353 | `f99f891e5c98bcef846d38925d053262851536b589dd7f0d3c28727e07548230` | 0 |
| vendor/mldsa-native/dev/x86_64/src/rej_uniform_eta2_avx2.c | 4574 | `7056af7757693807ac3efe1653dad224049ce5985974a4e14518d1d1ce1ee5f7` | 0 |
| vendor/mldsa-native/dev/x86_64/src/rej_uniform_eta4_avx2.c | 3936 | `42d382f31be9a4c934b6dd1142deb8574fdd6f4f8f41d03ea6bea25c89032d36` | 0 |
| vendor/mldsa-native/dev/x86_64/src/rej_uniform_table.c | 7960 | `d6caed3dd9d9cf6b1391cfc9537d31a84384b6bcf380cd0391a43e7553edc249` | 0 |
| vendor/mldsa-native/integration/liboqs/config_aarch64.h | 13321 | `d603eafb0fb7e5069e3013f01c9bdbb39b1ac70ad12b582cbaf22a52a0f7341b` | 0 |
| vendor/mldsa-native/integration/liboqs/config_c.h | 13408 | `956af96ce26cb46c1010235f204439e9de2f92a297f8ea7fe8fb9e66017d45c0` | 0 |
| vendor/mldsa-native/integration/liboqs/config_x86_64.h | 13314 | `9807424b0baeebbe19666a217b491ba45adb34dd69b6c30c6b80779ee1ad3591` | 0 |
| vendor/mldsa-native/integration/liboqs/fips202_glue.h | 923 | `b7174a806dec586fa6128b0f85d7bf611161502f788499de1779f529480c583c` | 0 |
| vendor/mldsa-native/integration/liboqs/fips202x4_glue.h | 987 | `b988cb80028187028a51f2a90ec427b870ae02d772f6a450d966bb5c8b7b5a89` | 0 |
| vendor/mldsa-native/mldsa/mldsa_native.c | 22252 | `cea0f7cd3c72998bf28762b906ed0b103cbcd911f59f0b080b76355213d34c2b` | 0 |
| vendor/mldsa-native/mldsa/mldsa_native.h | 37676 | `01ae99fa0e65a17f9481573af8c2dbea3bc6cb63dc0594610805aae8036bf615` | 0 |
| vendor/mldsa-native/mldsa/mldsa_native_config.h | 31211 | `7464f5fda2bb3b0baf368507c0344acb0b343a68864da5880aca9c2a64958ac5` | 0 |
| vendor/mldsa-native/mldsa/src/cbmc.h | 6227 | `328ed11c0652bc5bb3b58d1650d03190a83985e11f0817e84f483a7dc1bafb03` | 0 |
| vendor/mldsa-native/mldsa/src/common.h | 12294 | `5d4a056613b6ea8d8bec40af7838df48ffd079047a447472685674417766648d` | 0 |
| vendor/mldsa-native/mldsa/src/ct.c | 660 | `5d5641f89ee92f8d33f4489b7746ca20d4226cf6ecfcc9895bf644d4bc8871e5` | 0 |
| vendor/mldsa-native/mldsa/src/ct.h | 12552 | `95ef3775caabfd1e222b50ebea5c963754d6c270f8d5980065d85f98ab76747a` | 0 |
| vendor/mldsa-native/mldsa/src/debug.c | 1765 | `14c8356b7cd6ad0b6de8e2915468aa5271bcea2c2d959cfe22180c65fc9a580d` | 0 |
| vendor/mldsa-native/mldsa/src/debug.h | 5172 | `dbea92aa5b1a8b9afa09eb93bbf2532f5bb8656b7dc211a331e317de099500e7` | 0 |
| vendor/mldsa-native/mldsa/src/fips202/fips202.c | 8925 | `be2e087faac448a4a07f6680f569c890f91b365f00fbbc25caeddb6683fb3fb5` | 0 |
| vendor/mldsa-native/mldsa/src/fips202/fips202.h | 8890 | `29550569a1439261e6f587cadf18e956308c87e3c64f8f8d01119bc1302f1bc2` | 0 |
| vendor/mldsa-native/mldsa/src/fips202/fips202x4.c | 6470 | `0d97a2a25883f20a321c451ac77e3b8fa2683051e478adfc97900c9e8bc833eb` | 0 |
| vendor/mldsa-native/mldsa/src/fips202/fips202x4.h | 4429 | `5dc714bd8d106b8ce850e6ff2b5da0ad1eca92afc78aefa6d2e62dac7b3e0303` | 0 |
| vendor/mldsa-native/mldsa/src/fips202/keccakf1600.c | 12757 | `cd00ab2e66c80423ee597ca18aabe83f1c4c90cc2f44defd44c3aa9f32083ac2` | 0 |
| vendor/mldsa-native/mldsa/src/fips202/keccakf1600.h | 4522 | `9bd102a113dfe2799ff47b3755e14d69d5cc963d14e71a54a8552655c9f3479b` | 0 |
| vendor/mldsa-native/mldsa/src/fips202/native/aarch64/auto.h | 1997 | `df06198063437d5a83e5c99ae68cbdd221f402175ef4e7055b931095ccf67aae` | 0 |
| vendor/mldsa-native/mldsa/src/fips202/native/aarch64/src/fips202_native_aarch64.h | 2487 | `531fe8d1ec62897118f8df08ec83ff419f5772ef040d8c6f147d423e11b34d3d` | 0 |
| vendor/mldsa-native/mldsa/src/fips202/native/aarch64/src/keccakf1600_round_constants.c | 1996 | `c9351871c008c57156ea5b5192e39ffbef7dc617bd944c640ef8bb06c6433c7b` | 0 |
| vendor/mldsa-native/mldsa/src/fips202/native/aarch64/x1_scalar.h | 766 | `410b7e592502bd123cbb6564da582a205ed46fb15bf10115e3e27fb227c3ef60` | 0 |
| vendor/mldsa-native/mldsa/src/fips202/native/aarch64/x1_v84a.h | 965 | `38752a44470fc1a70ec29510f90c427fa1e9a47c6aa855211e6675455475032e` | 0 |
| vendor/mldsa-native/mldsa/src/fips202/native/aarch64/x2_v84a.h | 1056 | `8976244b9368e6e66c42f7f9ed62ae0fe42edf5766694930cdc79f43bcd3b759` | 0 |
| vendor/mldsa-native/mldsa/src/fips202/native/aarch64/x4_v8a_scalar.h | 844 | `9cbdf46a0e9264a60bf7b024482a15fabf17a52de5533cd39d359d137eab51f3` | 0 |
| vendor/mldsa-native/mldsa/src/fips202/native/aarch64/x4_v8a_v84a_scalar.h | 1041 | `987cc6617778df6152474d0a7529a6395b16ee67a9386ea39767cbd3665bcf1a` | 0 |
| vendor/mldsa-native/mldsa/src/fips202/native/api.h | 2812 | `8b3fc53dcfdd088b73519f274b6713aa370c00af98addc831eba7339d6ddde38` | 0 |
| vendor/mldsa-native/mldsa/src/fips202/native/armv81m/mve.h | 822 | `5ff69b17de89d246d6a13eba733a48e81b793d662007fac8aaaf6bea1bbb86d3` | 0 |
| vendor/mldsa-native/mldsa/src/fips202/native/armv81m/src/fips202_native_armv81m.h | 803 | `e629cabe779960e496858cd63e91ea6e599e0e0af1432927352f3597af73c99c` | 0 |
| vendor/mldsa-native/mldsa/src/fips202/native/armv81m/src/keccak_f1600_x4_mve.c | 4687 | `03dd17852b4827d662ff622de4070b392ca5c590ef36de0cad9d6c0d831f9a31` | 0 |
| vendor/mldsa-native/mldsa/src/fips202/native/armv81m/src/keccakf1600_round_constants.c | 1729 | `9b8bf66e1bbf69d8ada688d0ebb029a4b57d1053ce3b0f6767240c5b740d4d1c` | 0 |
| vendor/mldsa-native/mldsa/src/fips202/native/auto.h | 699 | `dc3607081d516a8d1310465a48984cb223ee4d5d1b789663047149979abd0043` | 0 |
| vendor/mldsa-native/mldsa/src/fips202/native/x86_64/src/KeccakP_1600_times4_SIMD256.c | 28194 | `3209f56295093fdb9749ee0639e3bc50c12cfa495ea537d557b2df35e57d6689` | 0 |
| vendor/mldsa-native/mldsa/src/fips202/native/x86_64/src/KeccakP_1600_times4_SIMD256.h | 547 | `54e7fe6f1bfbcf042888c82758ea8395bdd8b020fcba49109da7f9d0e80d9b18` | 0 |
| vendor/mldsa-native/mldsa/src/fips202/native/x86_64/xkcp.h | 777 | `8c56fa9a1fe025d35627cf6f48efad820ab4803e3600a099bd203756efbea6b6` | 0 |
| vendor/mldsa-native/mldsa/src/native/aarch64/meta.h | 9372 | `86458b409219c5b521acd1c8e780a7dd5b680ab1607f548861cbf98a09ffbd59` | 0 |
| vendor/mldsa-native/mldsa/src/native/aarch64/src/aarch64_zetas.c | 14368 | `87e22e4dd92e86f655870785fc8a6f40be187b543c0466920092f69daace620d` | 0 |
| vendor/mldsa-native/mldsa/src/native/aarch64/src/arith_native_aarch64.h | 6497 | `406b41271328f5f5488b25a2dd061787c2d73bc4e1cc1e0b13ce7218860478ad` | 0 |
| vendor/mldsa-native/mldsa/src/native/aarch64/src/polyz_unpack_table.c | 1417 | `0961cb66fd4951a3b01a243cf6886949d497b7ed19fefc7264d4507362ed87e6` | 0 |
| vendor/mldsa-native/mldsa/src/native/aarch64/src/rej_uniform_eta_table.c | 25597 | `9bd3425816dcc0c21115f6955cc8830c4cdc3c7bebb1e1d6ed76ec717db50115` | 0 |
| vendor/mldsa-native/mldsa/src/native/aarch64/src/rej_uniform_table.c | 2295 | `3308702a2208ea746e77c02792fa47ccfd0ea7ed7fc439e7cbcfde39d668c82a` | 0 |
| vendor/mldsa-native/mldsa/src/native/api.h | 31647 | `bef56a3797acf146c933f5f8bb759491ac1d9247992170cbe65a8e50f1bbd836` | 0 |
| vendor/mldsa-native/mldsa/src/native/meta.h | 421 | `bb197e13c58a1a71d7597cb5224b5e949ebc800463fe89ff28e0605ae46aff5c` | 0 |
| vendor/mldsa-native/mldsa/src/native/x86_64/meta.h | 10542 | `5a629bba590fc8b7f8ade17e07a7e28ad93cf2e7007d8bf91fcbfaf46bfd1c0a` | 0 |
| vendor/mldsa-native/mldsa/src/native/x86_64/src/arith_native_x86_64.h | 5074 | `e52ef79ddefd09e1bf941a2794435393e8e2cd8c9e1916504342bcd1550a64c9` | 0 |
| vendor/mldsa-native/mldsa/src/native/x86_64/src/consts.c | 9085 | `25ab5b8f9def84990da5cd747f2ff2298c684c6c6fc2441ed79c488fc5f7b8f6` | 0 |
| vendor/mldsa-native/mldsa/src/native/x86_64/src/consts.h | 806 | `9f19c24b4b0c6b3de27568a98b41f5e59eafd8c060dee848992c443adaa95f76` | 0 |
| vendor/mldsa-native/mldsa/src/native/x86_64/src/poly_caddq_avx2.c | 1609 | `07a5d8faa06b24399aed68397059063a4afbc8fe8ebedd903f9aa3730b97c6ac` | 0 |
| vendor/mldsa-native/mldsa/src/native/x86_64/src/poly_chknorm_avx2.c | 1271 | `366ff5b9bac1e0d0cf3aedecbc5f3de0ee9677c9fd940091b7ae08dff66433fe` | 0 |
| vendor/mldsa-native/mldsa/src/native/x86_64/src/poly_decompose_32_avx2.c | 5971 | `a0cf2f3a88c685d1d8f78799baa6aa8878e54a17144b4fe3c79b85fd3d83b48d` | 0 |
| vendor/mldsa-native/mldsa/src/native/x86_64/src/poly_decompose_88_avx2.c | 5871 | `2a389287fc5ac137852aad1373f65cc11da9f178063296876f70bff0714fe687` | 0 |
| vendor/mldsa-native/mldsa/src/native/x86_64/src/poly_use_hint_32_avx2.c | 3690 | `87dccba1100f78804576cd41826e13ccc4598e0d36f6fc031d67a42a7422a7fb` | 0 |
| vendor/mldsa-native/mldsa/src/native/x86_64/src/poly_use_hint_88_avx2.c | 3673 | `00d6bd43e97a75c44da4adebd314aadbe77dc31c2889489aadb33ed232950a2a` | 0 |
| vendor/mldsa-native/mldsa/src/native/x86_64/src/polyz_unpack_17_avx2.c | 3834 | `16d0f450551f80edecd5c26fa6025ff54532589a0ca4360cff09fd5378557520` | 0 |
| vendor/mldsa-native/mldsa/src/native/x86_64/src/polyz_unpack_19_avx2.c | 4005 | `2c1a08402202bad2183b346fa262a88de442f0164bb25d1c1447e0bc5f63f89e` | 0 |
| vendor/mldsa-native/mldsa/src/native/x86_64/src/rej_uniform_avx2.c | 6353 | `f99f891e5c98bcef846d38925d053262851536b589dd7f0d3c28727e07548230` | 0 |
| vendor/mldsa-native/mldsa/src/native/x86_64/src/rej_uniform_eta2_avx2.c | 4574 | `7056af7757693807ac3efe1653dad224049ce5985974a4e14518d1d1ce1ee5f7` | 0 |
| vendor/mldsa-native/mldsa/src/native/x86_64/src/rej_uniform_eta4_avx2.c | 3936 | `42d382f31be9a4c934b6dd1142deb8574fdd6f4f8f41d03ea6bea25c89032d36` | 0 |
| vendor/mldsa-native/mldsa/src/native/x86_64/src/rej_uniform_table.c | 7960 | `d6caed3dd9d9cf6b1391cfc9537d31a84384b6bcf380cd0391a43e7553edc249` | 0 |
| vendor/mldsa-native/mldsa/src/packing.c | 9210 | `a7fad3acf40f0b1f18813a5cad6066e3b84956bbcdc8fc7235e2c9660fa0970d` | 0 |
| vendor/mldsa-native/mldsa/src/packing.h | 9708 | `9852b2289f3b4172473423f6c15c25b9ad6dd57be8b987ad31f55ec15f0a8939` | 0 |
| vendor/mldsa-native/mldsa/src/params.h | 2176 | `9752e4fb21ed390fc94cd9d05691e5c1b76939a69b7c7ed72f8e19e193d5f54b` | 0 |
| vendor/mldsa-native/mldsa/src/poly.c | 35409 | `069577780908dc2d06a21556365712e8408340dfc0cdab39b68ce6b9286a8854` | 0 |
| vendor/mldsa-native/mldsa/src/poly.h | 16291 | `3b714379ae31e640dea735a24b3442e3e76096874e6739b67f133c8eaa956189` | 0 |
| vendor/mldsa-native/mldsa/src/poly_kl.c | 34192 | `5a4330471e2811364d67e2826ad94fa9b4ae69013f7357f21a7bfcece7463a04` | 0 |
| vendor/mldsa-native/mldsa/src/poly_kl.h | 15723 | `93bd01ec8d5f2e7f8e8c2cdff3e2a006276b198f255c7f58ebe5dccabf415dae` | 0 |
| vendor/mldsa-native/mldsa/src/polyvec.c | 29352 | `462482045e569d2a96df2bf829daba1900b816995831f6d9b3d162d780658b4d` | 0 |
| vendor/mldsa-native/mldsa/src/polyvec.h | 31718 | `547e679719c0e9adf02b9dd855946e700f368db556893b3fb452401156c9922e` | 0 |
| vendor/mldsa-native/mldsa/src/randombytes.h | 730 | `b8ccb9a34818d8e1cd0cfea9b24829ab9949cb88c20ed0648459c5c7d36aa492` | 0 |
| vendor/mldsa-native/mldsa/src/reduce.h | 4421 | `6bdce26e08c8d8895f242d6be2cd7145a5db227297a43ce161db5f560dc25ac5` | 0 |
| vendor/mldsa-native/mldsa/src/rounding.h | 8980 | `e32638772ee4564c683685b7f9acc84e5e0763e6ca3eb61abb7ed41424f478fc` | 0 |
| vendor/mldsa-native/mldsa/src/sign.c | 53437 | `b9ba66f68ba63d1462607cbc23aa7f66203084769dc2ab0ecfae3e982157acb6` | 0 |
| vendor/mldsa-native/mldsa/src/sign.h | 37165 | `6c3dc7a4e151257cff1dd30ed58c47c48886fa42fab69c178180c881587b87fb` | 0 |
| vendor/mldsa-native/mldsa/src/symmetric.h | 2635 | `4ed2df211b960a747e29aec04055100470def1ae8c481feb203c27fbc61a0b70` | 0 |
| vendor/mldsa-native/mldsa/src/sys.h | 8233 | `e06262e46cccab6479f296bea6ec25f7efe4fc0901dcca6fcc6c9aae0a087b74` | 0 |
| vendor/mldsa-native/proofs/cbmc/H/H_harness.c | 527 | `e749847d3f8c767b90624626b37b0c4af774eade89a9bf964c757ef0364ad119` | 0 |
| vendor/mldsa-native/proofs/cbmc/attempt_signature_generation/attempt_signature_generation_harness.c | 831 | `ae6995401b38cca523bba39b83d5680a0b992dbad065337c9df8cd021c9013ad` | 0 |
| vendor/mldsa-native/proofs/cbmc/caddq/caddq_harness.c | 194 | `f9d8824447cd28249f74839921d89964a3f2ec6e3123cc23fd74f13231ccc8cc` | 0 |
| vendor/mldsa-native/proofs/cbmc/check_pct/check_pct_harness.c | 370 | `689efda6dda3e3df8be93861b8603f636edb345170008653fc8fe37e1dc03e6b` | 0 |
| vendor/mldsa-native/proofs/cbmc/compute_pack_z/compute_pack_z_harness.c | 471 | `3c08fbd60f4b4f5ab3c4188dd541d06322bb860b029c7454af62a7b3fbbdadff` | 0 |
| vendor/mldsa-native/proofs/cbmc/compute_t0_t1_tr_from_sk_components/compute_t0_t1_tr_from_sk_components_harness.c | 592 | `a544301effa169155e36e7f65ce05d959376dcde387b97d8f9422fc6677e8eed` | 0 |
| vendor/mldsa-native/proofs/cbmc/ct_abs_i32/ct_abs_i32_harness.c | 178 | `e66eae9fc96dc3bcf4360c8be26126e06a0a4c59adaf5e1a4992e76f762e9728` | 0 |
| vendor/mldsa-native/proofs/cbmc/ct_cmask_neg_i32/ct_cmask_neg_i32_harness.c | 184 | `ed9551addb563305fa9cbec757a7d77ccf74b14948313a32e29b725a3ab33ab7` | 0 |
| vendor/mldsa-native/proofs/cbmc/ct_cmask_nonzero_u32/ct_cmask_nonzero_u32_harness.c | 313 | `331d478700ba98d10c129f7a25e9985c6cfed6d9e72872f33e2ec853a6b0c253` | 0 |
| vendor/mldsa-native/proofs/cbmc/ct_cmask_nonzero_u8/ct_cmask_nonzero_u8_harness.c | 311 | `6bc2b61cededf0e83ba25b14c673e8431ada042b6a794ecd032889472d1862d8` | 0 |
| vendor/mldsa-native/proofs/cbmc/ct_get_optblocker_i64/ct_get_optblocker_i64_harness.c | 173 | `5668162b8a1efca7c18f3ca85863c69934b819702c3c94d6f6200884c84c667e` | 0 |
| vendor/mldsa-native/proofs/cbmc/ct_get_optblocker_u32/ct_get_optblocker_u32_harness.c | 173 | `d049b9acb822c220941d4ff114b1f7e8f2b558341e45ab6e0db0f8e87179ad29` | 0 |
| vendor/mldsa-native/proofs/cbmc/ct_get_optblocker_u8/ct_get_optblocker_u8_harness.c | 250 | `b7808efafa87e3ea2277f24b3acf8cc1a19a94b7547add727c16f71a2d7e66f8` | 0 |
| vendor/mldsa-native/proofs/cbmc/ct_memcmp/ct_memcmp_harness.c | 293 | `8d9228d349de84dda94943610525af23819275c20427c7d6c366e21e56d4e54e` | 0 |
| vendor/mldsa-native/proofs/cbmc/ct_sel_int32/ct_sel_int32_harness.c | 209 | `3b5b44ba8264a5521744b3db9a2e3f4fd052ae277f91daffe67c19a0d6e0144d` | 0 |
| vendor/mldsa-native/proofs/cbmc/decompose/decompose_harness.c | 212 | `56a8d8087f70bf7df54ba5d17f6fe3cfc284fd3d53042522fcec2dfcc4a843aa` | 0 |
| vendor/mldsa-native/proofs/cbmc/dummy_backend.h | 1007 | `bd8e59bf29c6de7f0cad6063473a52e447d18af2d4b0a428ae2a0b315f732b1b` | 0 |
| vendor/mldsa-native/proofs/cbmc/dummy_backend_fips202_x1.h | 317 | `96b98dc14759349d4df9b22f64e14c3d0b115effb7f0bfd4c16b0e810ab31b65` | 0 |
| vendor/mldsa-native/proofs/cbmc/dummy_backend_fips202_x4.h | 317 | `cde24902521e1f5b71bb18d8b9180920760089b098916faa82aaa6591a61a9c0` | 0 |
| vendor/mldsa-native/proofs/cbmc/fqmul/fqmul_harness.c | 229 | `959b03e64a88f12451edb6c20566cdfb39d67143e998a93bb0642a61f9f12bd0` | 0 |
| vendor/mldsa-native/proofs/cbmc/fqscale/fqscale_harness.c | 216 | `75172268b10d4eb6438afab0da048e1d85d05aaeb60271a57e156634bf387a39` | 0 |
| vendor/mldsa-native/proofs/cbmc/intt_native_x86_64/intt_native_x86_64_harness.c | 281 | `b5c8189ba6f1fac79794453e916ccf64e9a11e5af527b5bcd8efef32bd73a8f3` | 0 |
| vendor/mldsa-native/proofs/cbmc/invntt_layer/invntt_layer_harness.c | 290 | `b6decf5f9c7b946d36a3584dceb636f61aa32f8eba47f0b5bc2b97a4e7b86ef4` | 0 |
| vendor/mldsa-native/proofs/cbmc/keccak_absorb/keccak_absorb_harness.c | 494 | `c8b604a618b2341f278ac085aa0387d6735c7efa63ffb2f7caf5459715b77cdf` | 0 |
| vendor/mldsa-native/proofs/cbmc/keccak_absorb_once_x4/keccak_absorb_once_x4_harness.c | 703 | `0ab6a116e2e7b4d0e17d33bef4e9e691ea923e3b25703c02f8ec252ea7210b1b` | 0 |
| vendor/mldsa-native/proofs/cbmc/keccak_finalize/keccak_finalize_harness.c | 375 | `4147bf5ceb790eb7403de0d2a0d2d045107d6a5b550693042f251f5efb20abdf` | 0 |
| vendor/mldsa-native/proofs/cbmc/keccak_init/keccak_init_harness.c | 247 | `d934019cc0e71d9eeaa62fc1a5e014f5fd5afe7b3d4435f84227461423610880` | 0 |
| vendor/mldsa-native/proofs/cbmc/keccak_squeeze/keccak_squeeze_harness.c | 471 | `cd602700f126ea46245fb11b92789cf213dfac73a7d4fd199d9c25c372ad0b19` | 0 |
| vendor/mldsa-native/proofs/cbmc/keccak_squeezeblocks_x4/keccak_squeezeblocks_x4_harness.c | 669 | `b57affd2cf79a582ecd3aa72be6b63819908a3f6c88b8294aa3be9429044de33` | 0 |
| vendor/mldsa-native/proofs/cbmc/keccakf1600_extract_bytes/keccakf1600_extract_bytes_harness.c | 325 | `1e1a3d064aa57342f541931970cd49198e801b059c6451f427b1821e67c75b64` | 0 |
| vendor/mldsa-native/proofs/cbmc/keccakf1600_extract_bytes_BE/keccakf1600_extract_bytes_be_harness.c | 325 | `1e1a3d064aa57342f541931970cd49198e801b059c6451f427b1821e67c75b64` | 0 |
| vendor/mldsa-native/proofs/cbmc/keccakf1600_permute/keccakf1600_permute_harness.c | 198 | `c844e9144ab782ec5604ade65ea925af1f2951cb7e80ff42e0a4cc9f713fffbb` | 0 |
| vendor/mldsa-native/proofs/cbmc/keccakf1600_permute_native/keccakf1600_permute_native_harness.c | 198 | `c844e9144ab782ec5604ade65ea925af1f2951cb7e80ff42e0a4cc9f713fffbb` | 0 |
| vendor/mldsa-native/proofs/cbmc/keccakf1600_xor_bytes/keccakf1600_xor_bytes_harness.c | 398 | `96d61e662fc375f9586f9d2d50092365630fb839ae464ac862e9d3da8d64d6ac` | 0 |
| vendor/mldsa-native/proofs/cbmc/keccakf1600_xor_bytes_BE/keccakf1600_xor_bytes_be_harness.c | 398 | `96d61e662fc375f9586f9d2d50092365630fb839ae464ac862e9d3da8d64d6ac` | 0 |
| vendor/mldsa-native/proofs/cbmc/keccakf1600x4_extract_bytes/keccakf1600x4_extract_bytes_harness.c | 479 | `cde3591d13269dbe5fe0071b1f9a321cd8c3f91fdf5070be6024f2a2bd8a5470` | 0 |
| vendor/mldsa-native/proofs/cbmc/keccakf1600x4_permute/keccakf1600x4_permute_harness.c | 301 | `32d13750d6249c35b8b49f1b24c96ff15456c3ac39e812d04a34b9cc777d819b` | 0 |
| vendor/mldsa-native/proofs/cbmc/keccakf1600x4_permute_native/keccakf1600x4_permute_native_harness.c | 301 | `32d13750d6249c35b8b49f1b24c96ff15456c3ac39e812d04a34b9cc777d819b` | 0 |
| vendor/mldsa-native/proofs/cbmc/keccakf1600x4_xor_bytes/keccakf1600x4_xor_bytes_harness.c | 477 | `19d4fa4254cf02f0415ad022f53fdb118b2e7c1f5af3cbe06301cfaca9cd3a2f` | 0 |
| vendor/mldsa-native/proofs/cbmc/lib/__init__.py | 52 | `34743113a2b63e6ac66a6019ce7182327c3435bbfdbe6486b17bf8c54a8d3578` | 0 |
| vendor/mldsa-native/proofs/cbmc/lib/print_tool_versions.py | 1875 | `b0ab0604a9d785964bcf05c344564361567567fcd076c711a475ff4a85be29de` | 0 |
| vendor/mldsa-native/proofs/cbmc/lib/summarize.py | 7122 | `d19d04bae53d0b7cf7aaa174592015a15e7f15efc9a0866ae2438e1b75445975` | 0 |
| vendor/mldsa-native/proofs/cbmc/make_hint/make_hint_harness.c | 211 | `e0e3c615e0e9ac954b545504c3428662d403adc5098e703068590fb54d011601` | 0 |
| vendor/mldsa-native/proofs/cbmc/mldsa_native_config_cbmc.h | 31575 | `27362b86f5896bdd16fecc5f31070ab5adb3fdd477e67580ee4540e5517dca45` | 0 |
| vendor/mldsa-native/proofs/cbmc/montgomery_reduce/montgomery_reduce_harness.c | 206 | `d3ec1f2d7a3c236a4d8b15171944fa1887cdd8930660d1bbccfd7b5c22b277e4` | 0 |
| vendor/mldsa-native/proofs/cbmc/ntt_butterfly_block/ntt_butterfly_block_harness.c | 424 | `8f0fa4eeab6935b7314d7652856bb8b1a374f124da1b28272eb3536778c1e1ce` | 0 |
| vendor/mldsa-native/proofs/cbmc/ntt_layer/ntt_layer_harness.c | 284 | `42b103c069ef26d6453ffb8acb4ed693dd71fcac4e3f14db4723e62a404aa7fb` | 0 |
| vendor/mldsa-native/proofs/cbmc/ntt_native_aarch64/ntt_native_aarch64_harness.c | 279 | `831338b93557f55f6e8f8bc5d68da5f30f0ca6f2899b20d0c3d63017307938d8` | 0 |
| vendor/mldsa-native/proofs/cbmc/ntt_native_x86_64/ntt_native_x86_64_harness.c | 279 | `831338b93557f55f6e8f8bc5d68da5f30f0ca6f2899b20d0c3d63017307938d8` | 0 |
| vendor/mldsa-native/proofs/cbmc/pack_pk/pack_pk_harness.c | 211 | `5f5464fe13fd1a13c39a9fea93bda4fe6e33cc01c069838b196f3a95007479ad` | 0 |
| vendor/mldsa-native/proofs/cbmc/pack_sig_c_h/pack_sig_c_h_harness.c | 239 | `d90dd7ebac29c2560ea9c2c07e89ceaa2814f9c89516e7d3a37065be594b54f0` | 0 |
| vendor/mldsa-native/proofs/cbmc/pack_sig_z/pack_sig_z_harness.c | 222 | `8543f988096f9dd4fc3510cb287359e644257593c7dfdccac600e9ff2f359f8a` | 0 |
| vendor/mldsa-native/proofs/cbmc/pack_sk/pack_sk_harness.c | 260 | `419f9e42d6191553ec99b6345a7bfb8ab729d5645b86cb7280adf2bdb30dd5f9` | 0 |
| vendor/mldsa-native/proofs/cbmc/poly_add/poly_add_harness.c | 187 | `692027b67f1a5d054cc7078c475d268b05a827baae2fa7afb3382c57f92a6bef` | 0 |
| vendor/mldsa-native/proofs/cbmc/poly_caddq/poly_caddq_harness.c | 183 | `6b0389b3d65f668c64e318bf1682fb405cab925d407d1ee71e34f744ae507168` | 0 |
| vendor/mldsa-native/proofs/cbmc/poly_caddq_c/poly_caddq_c_harness.c | 263 | `259862d68ad758d412dbacb668ece357b1d5e19bea7632f2b77e882d6ddfbe60` | 0 |
| vendor/mldsa-native/proofs/cbmc/poly_caddq_native/poly_caddq_native_harness.c | 183 | `6b0389b3d65f668c64e318bf1682fb405cab925d407d1ee71e34f744ae507168` | 0 |
| vendor/mldsa-native/proofs/cbmc/poly_caddq_native_aarch64/poly_caddq_native_aarch64_harness.c | 289 | `5f2f7e02d0661fc34bbab6c41d7fff957937eb83a659df9249425d55dd6d8d08` | 0 |
| vendor/mldsa-native/proofs/cbmc/poly_challenge/poly_challenge_harness.c | 213 | `18e7f7451aaac811149c8c305c1c7d96434fd5e3a0abdd772bc370ff8f538922` | 0 |
| vendor/mldsa-native/proofs/cbmc/poly_chknorm/poly_chknorm_harness.c | 222 | `edef1c4ef04e1ba7c42bc8a7e1dcc8ca761ceb216017c7757ffcd0b988f119d1` | 0 |
| vendor/mldsa-native/proofs/cbmc/poly_chknorm_c/poly_chknorm_c_harness.c | 318 | `bf1b411bfbadd8bec4775371e0260617af10852801faa4eb504a7696e10671c6` | 0 |
| vendor/mldsa-native/proofs/cbmc/poly_chknorm_native/poly_chknorm_native_harness.c | 222 | `edef1c4ef04e1ba7c42bc8a7e1dcc8ca761ceb216017c7757ffcd0b988f119d1` | 0 |
| vendor/mldsa-native/proofs/cbmc/poly_chknorm_native_aarch64/poly_chknorm_native_aarch64_harness.c | 332 | `b57e5b09592aa320aa81221a2e74becb22bd28057b31147b0d6d3038fc713611` | 0 |
| vendor/mldsa-native/proofs/cbmc/poly_decompose/poly_decompose_harness.c | 201 | `7b4e7156247c75e7395be5bad8220fa8654d10543f257cd1d865f8e1fb3203e1` | 0 |
| vendor/mldsa-native/proofs/cbmc/poly_decompose_c/poly_decompose_c_harness.c | 368 | `65ec91efab88016745e454c3a6739cf052ea484d0587e6491b5bf47189b1ce9f` | 0 |
| vendor/mldsa-native/proofs/cbmc/poly_decompose_native/poly_decompose_native_harness.c | 201 | `7b4e7156247c75e7395be5bad8220fa8654d10543f257cd1d865f8e1fb3203e1` | 0 |
| vendor/mldsa-native/proofs/cbmc/poly_invntt_tomont/poly_invntt_tomont_harness.c | 230 | `907160eb7f5dd06ca0ee79ac442783b5eed7ffb14b5db100241bab972ea0e8cc` | 0 |
| vendor/mldsa-native/proofs/cbmc/poly_invntt_tomont_c/poly_invntt_tomont_c_harness.c | 319 | `36c15a1fd269700c7a3ccb94421a098d80fde05db2ea30c068f086564d2511c3` | 0 |
| vendor/mldsa-native/proofs/cbmc/poly_invntt_tomont_native/poly_invntt_tomont_native_harness.c | 190 | `289370c115290baf53c6d099e9a2d484ae64b64b2bee805fc995d55d20209e08` | 0 |
| vendor/mldsa-native/proofs/cbmc/poly_make_hint/poly_make_hint_harness.c | 225 | `42bd17c27d93686c3aab69275becd2e1a9493e6ded3e3a71a70529a4740de0c6` | 0 |
| vendor/mldsa-native/proofs/cbmc/poly_ntt/poly_ntt_harness.c | 180 | `30de42fc7799dbc347dc1a0398182f378699b0f798a3b102cb05da621976d1f0` | 0 |
| vendor/mldsa-native/proofs/cbmc/poly_ntt_c/poly_ntt_c_harness.c | 258 | `3a4b83c31c13e0244228f831d55133138a77aef24b47af5e69307c24a2a2842a` | 0 |
| vendor/mldsa-native/proofs/cbmc/poly_ntt_native/poly_ntt_native_harness.c | 180 | `30de42fc7799dbc347dc1a0398182f378699b0f798a3b102cb05da621976d1f0` | 0 |
| vendor/mldsa-native/proofs/cbmc/poly_pointwise_montgomery/poly_pointwise_montgomery_harness.c | 211 | `9e9a87f3dece9742c166a0907d900ae5c889c919996197c31b664ee9f9a76a25` | 0 |
| vendor/mldsa-native/proofs/cbmc/poly_pointwise_montgomery_c/poly_pointwise_montgomery_c_harness.c | 333 | `d53b3d205f1712e6a9643a0408952aedc3f5cd92866fd54a8a47e1490152df64` | 0 |
| vendor/mldsa-native/proofs/cbmc/poly_pointwise_montgomery_native/poly_pointwise_montgomery_native_harness.c | 211 | `9e9a87f3dece9742c166a0907d900ae5c889c919996197c31b664ee9f9a76a25` | 0 |
| vendor/mldsa-native/proofs/cbmc/poly_power2round/poly_power2round_harness.c | 207 | `881bedd316a96fb7d3c4cb8b70bb2aa3f0377f18617cb5dcdae738b216389eba` | 0 |
| vendor/mldsa-native/proofs/cbmc/poly_reduce/poly_reduce_harness.c | 183 | `588953c052099600f23be51a09e1c812222a525cf8594e91c8c6386937e90e71` | 0 |
| vendor/mldsa-native/proofs/cbmc/poly_shiftl/poly_shiftl_harness.c | 183 | `0c1f24d94e6c978cca90a0d34a029f50eefe4b282e1ad01b3efdbe02222e4bc2` | 0 |
| vendor/mldsa-native/proofs/cbmc/poly_sub/poly_sub_harness.c | 187 | `334af03d7558ea47c76d1c939b66f86216c6191440e7f02aeb7edaf71616f2a5` | 0 |
| vendor/mldsa-native/proofs/cbmc/poly_uniform/poly_uniform_harness.c | 243 | `6d739549c4e484a3145e4802a5a6b70b6b58c6f9bda93c95a59cb224ff14577a` | 0 |
| vendor/mldsa-native/proofs/cbmc/poly_uniform_4x/poly_uniform_4x_harness.c | 310 | `f2cddb38b31e53d17ac20dda7e81a386e031009c747818d7cc96e6c3acee65aa` | 0 |
| vendor/mldsa-native/proofs/cbmc/poly_uniform_eta/poly_uniform_eta_harness.c | 241 | `6f2554154a41c68d5057bb9903bf4e8ff74254073c3199786499d2375afa7d3a` | 0 |
| vendor/mldsa-native/proofs/cbmc/poly_uniform_eta_4x/poly_uniform_eta_4x_harness.c | 295 | `9b8a74c5e7496bd197507cb19780c79232f26bd5103cd3e327050c70c5de8473` | 0 |
| vendor/mldsa-native/proofs/cbmc/poly_uniform_gamma1/poly_uniform_gamma1_harness.c | 388 | `232cbaca6d3c1f0d3f1b6d3901a1fd8ea18295125f3b2ef2833f4cd3b56c83be` | 0 |
| vendor/mldsa-native/proofs/cbmc/poly_uniform_gamma1_4x/poly_uniform_gamma1_4x_harness.c | 299 | `58b0068d870dddb94ba045e5f7c85365ff95f31dd1df664f07b45385e7be5693` | 0 |
| vendor/mldsa-native/proofs/cbmc/poly_use_hint/poly_use_hint_harness.c | 203 | `7861d11cf75f2b52050226a1310847612ef0bfb3266237c5dd57830278cad6c5` | 0 |
| vendor/mldsa-native/proofs/cbmc/poly_use_hint_c/poly_use_hint_c_harness.c | 379 | `e40f57748b95d4d4f1efdae4cad864f34e75cee1fcb11050266bdd9592c7189d` | 0 |
| vendor/mldsa-native/proofs/cbmc/poly_use_hint_native/poly_use_hint_native_harness.c | 203 | `7861d11cf75f2b52050226a1310847612ef0bfb3266237c5dd57830278cad6c5` | 0 |
| vendor/mldsa-native/proofs/cbmc/polyeta_pack/polyeta_pack_harness.c | 204 | `9f2346fbb8acdb498cab30f1b66f766ca0879360a874bf4ade603b26431e42b1` | 0 |
| vendor/mldsa-native/proofs/cbmc/polyeta_unpack/polyeta_unpack_harness.c | 206 | `e797b287b8e43be91d8b327baf8073def1f6e6ecb46a060dd2d59cbd60f1cf18` | 0 |
| vendor/mldsa-native/proofs/cbmc/polymat_permute_bitrev_to_custom/polymat_permute_bitrev_to_custom_harness.c | 276 | `5246e2088be4e55ec041752d3cd4e12e97bcd8f7e6cd26214cd84bc4594e0dfc` | 0 |
| vendor/mldsa-native/proofs/cbmc/polyt0_pack/polyt0_pack_harness.c | 200 | `0cc9c4c79e88d13dab0d7050fdc4d95fdc02b0f442ae5349177d53007d536257` | 0 |
| vendor/mldsa-native/proofs/cbmc/polyt0_unpack/polyt0_unpack_harness.c | 202 | `51b72eff6cedcbc85af6e65f30e71cdc83b267888e1532c619e12d3d73ec930d` | 0 |
| vendor/mldsa-native/proofs/cbmc/polyt1_pack/polyt1_pack_harness.c | 200 | `c5ff9ac76197959cf122094b52b10b7abd4b373a46791cf8a48b6183988c50c2` | 0 |
| vendor/mldsa-native/proofs/cbmc/polyt1_unpack/polyt1_unpack_harness.c | 202 | `55eaf2a62d5e2d8c74f654ded9473c192b76c386974217f626315c15353cbd26` | 0 |
| vendor/mldsa-native/proofs/cbmc/polyvec_matrix_expand/polyvec_matrix_expand_harness.c | 225 | `40c33a9fe78ca444fbf20cf1d6dce8b7e73e2bfa53e9f76611aafff14eda1dc4` | 0 |
| vendor/mldsa-native/proofs/cbmc/polyvec_matrix_expand_serial/polyvec_matrix_expand_harness.c | 225 | `40c33a9fe78ca444fbf20cf1d6dce8b7e73e2bfa53e9f76611aafff14eda1dc4` | 0 |
| vendor/mldsa-native/proofs/cbmc/polyvec_matrix_pointwise_montgomery/polyvec_matrix_pointwise_montgomery_harness.c | 257 | `6d863d6f846cb42ee9af68287dab732b0d6bc484f62d3a7026267c1fccadae9d` | 0 |
| vendor/mldsa-native/proofs/cbmc/polyveck_add/polyveck_add_harness.c | 198 | `02c2d04095b6417fd055b699122179cc14c225d39b1627da0e2e6e308b06f68d` | 0 |
| vendor/mldsa-native/proofs/cbmc/polyveck_caddq/polyveck_caddq_harness.c | 193 | `17e5fa581ada0f479e233fa24c7e00e5bd40f766de9720a88e9bd347db7083a8` | 0 |
| vendor/mldsa-native/proofs/cbmc/polyveck_chknorm/polyveck_chknorm_harness.c | 229 | `4af1d58a2a0683ba21e47a0576aa41d36ca001d81bbb5ef49746d8abd9b0c198` | 0 |
| vendor/mldsa-native/proofs/cbmc/polyveck_decompose/polyveck_decompose_harness.c | 208 | `44fc31ba646a62f36088f9bda37d2ba9435d70aa128f8671eecc3c08223b0675` | 0 |
| vendor/mldsa-native/proofs/cbmc/polyveck_invntt_tomont/polyveck_invntt_tomont_harness.c | 241 | `7b13da771afe678e3edfdc22876f02871d256774c4229c6279576d8502563876` | 0 |
| vendor/mldsa-native/proofs/cbmc/polyveck_make_hint/polyveck_make_hint_harness.c | 233 | `db53736caf25b8e189b2c727a643843708f8e4d9b990e46595f7d17610bafb75` | 0 |
| vendor/mldsa-native/proofs/cbmc/polyveck_ntt/polyveck_ntt_harness.c | 191 | `e40816a6c1925779ef2300db035f28cc46cd2fe497b05d1f446ab86abf746e7e` | 0 |
| vendor/mldsa-native/proofs/cbmc/polyveck_pack_eta/polyveck_pack_eta_harness.c | 213 | `766c08d262e5b5d87e530ef780dc4b41cb8b5f34f43983691150340dde37da09` | 0 |
| vendor/mldsa-native/proofs/cbmc/polyveck_pack_t0/polyveck_pack_t0_harness.c | 212 | `f9d2d448c4c5e5fe00270dfc2b7a9466cc04463e92da2062e3f134e0c912d66c` | 0 |
| vendor/mldsa-native/proofs/cbmc/polyveck_pack_w1/polyveck_pack_w1_harness.c | 212 | `998802abc5584ee719867e2723e4915aea25415e9e33878a8aa19162c7f2a3bb` | 0 |
| vendor/mldsa-native/proofs/cbmc/polyveck_pointwise_poly_montgomery/polyveck_pointwise_poly_montgomery_harness.c | 238 | `eba56283557e023eb4306656c1fc8830d9d1292bfce37ae87de2767e23b80511` | 0 |
| vendor/mldsa-native/proofs/cbmc/polyveck_power2round/polyveck_power2round_harness.c | 213 | `0a0fdfdbb62786d3840cf5344395c3ebe8132424f2f63b8b512d2fd51de5266e` | 0 |
| vendor/mldsa-native/proofs/cbmc/polyveck_reduce/polyveck_reduce_harness.c | 194 | `6c46aa82cf2965d7d72b62054cf16ff2d62a823e519ba584e550d58fa0f757c5` | 0 |
| vendor/mldsa-native/proofs/cbmc/polyveck_shiftl/polyveck_shiftl_harness.c | 194 | `96b4c489dd75a37d64ecf41cd8e8a444dce076488dd72052ec83d16414c8e325` | 0 |
| vendor/mldsa-native/proofs/cbmc/polyveck_sub/polyveck_sub_harness.c | 198 | `f1d0467f63cf2c521da6565547fffbcff2c7a7ca1bf362c26426c9fb751e4430` | 0 |
| vendor/mldsa-native/proofs/cbmc/polyveck_unpack_eta/polyveck_unpack_eta_harness.c | 215 | `d1bba1b5fca09379db8d0bc909707bc5459a6d0dd27ec7e7460b02ba995ad856` | 0 |
| vendor/mldsa-native/proofs/cbmc/polyveck_unpack_t0/polyveck_unpack_t0_harness.c | 214 | `7921912bb4dd500324da3f04d256c7a0d21fe93634095ac63000d6e48f750941` | 0 |
| vendor/mldsa-native/proofs/cbmc/polyveck_use_hint/polyveck_use_hint_harness.c | 210 | `f76c9f42a029dfac1342fffc976f18fc98fb7c9e76e12c98c6ae89d8131f3bb9` | 0 |
| vendor/mldsa-native/proofs/cbmc/polyvecl_chknorm/polyvecl_chknorm_harness.c | 220 | `12779c60b393ed168aa82ed17370832329580f4a459c287e310ea2b6da8fd0b5` | 0 |
| vendor/mldsa-native/proofs/cbmc/polyvecl_ntt/polyvecl_ntt_harness.c | 191 | `adf108ee1420e3908e1e670636caba6678df1ab5f5251edab814f9b43b90efeb` | 0 |
| vendor/mldsa-native/proofs/cbmc/polyvecl_pack_eta/polyvecl_pack_eta_harness.c | 213 | `e3e34ac585455e38de3fa8b4223134a0e6fab1596e3698ecb83d4594dbe9a270` | 0 |
| vendor/mldsa-native/proofs/cbmc/polyvecl_permute_bitrev_to_custom/polyvecl_permute_bitrev_to_custom_harness.c | 274 | `362188cffed11abeacb7f6eafa50fff67ae01e7813c8d9d5deb761d9942c431f` | 0 |
| vendor/mldsa-native/proofs/cbmc/polyvecl_permute_bitrev_to_custom_native/polyvecl_permute_bitrev_to_custom_native_harness.c | 274 | `362188cffed11abeacb7f6eafa50fff67ae01e7813c8d9d5deb761d9942c431f` | 0 |
| vendor/mldsa-native/proofs/cbmc/polyvecl_pointwise_acc_montgomery/polyvecl_pointwise_acc_montgomery_harness.c | 237 | `25f0386652609a7b56fc7ea3ccb52fd753de0bc0cc9d95a3875542939462c817` | 0 |
| vendor/mldsa-native/proofs/cbmc/polyvecl_pointwise_acc_montgomery_c/polyvecl_pointwise_acc_montgomery_c_harness.c | 531 | `139d2a314a5f2c508483dfe9ad3fa7d02b64bc238840d5d704c5d48ffac6deba` | 0 |
| vendor/mldsa-native/proofs/cbmc/polyvecl_pointwise_acc_montgomery_native/polyvecl_pointwise_acc_montgomery_native_harness.c | 237 | `25f0386652609a7b56fc7ea3ccb52fd753de0bc0cc9d95a3875542939462c817` | 0 |
| vendor/mldsa-native/proofs/cbmc/polyvecl_uniform_gamma1/polyvecl_uniform_gamma1_harness.c | 257 | `1c9026e4610b2c872902038aecec4f54a456f73e6d8ca0438708b16538dd0000` | 0 |
| vendor/mldsa-native/proofs/cbmc/polyvecl_uniform_gamma1_serial/polyvecl_uniform_gamma1_harness.c | 257 | `1c9026e4610b2c872902038aecec4f54a456f73e6d8ca0438708b16538dd0000` | 0 |
| vendor/mldsa-native/proofs/cbmc/polyvecl_unpack_eta/polyvecl_unpack_eta_harness.c | 215 | `e24c14259c7a72c3443d634abb5348f7e63b0af4dd6a30fac60f455d5e3ca743` | 0 |
| vendor/mldsa-native/proofs/cbmc/polyvecl_unpack_z/polyvecl_unpack_z_harness.c | 213 | `80a9e70b0d04bbd374d060c4f5c4574c93b66002e20b8ce5b734b5784de67d38` | 0 |
| vendor/mldsa-native/proofs/cbmc/polyw1_pack/polyw1_pack_harness.c | 203 | `98a6533440ed3a273f45e658d54b07bd931d08a80a5ae4109cca39c33ebce7d1` | 0 |
| vendor/mldsa-native/proofs/cbmc/polyz_pack/polyz_pack_harness.c | 202 | `97bd63a11889029bfce54e035f821c16ff7b72333dabe42265bec384d1475394` | 0 |
| vendor/mldsa-native/proofs/cbmc/polyz_unpack/polyz_unpack_harness.c | 204 | `167850a9aae54273f22f4f3c61774192a2ae90dcf8cc4b6e5e912b5a0e8c700f` | 0 |
| vendor/mldsa-native/proofs/cbmc/polyz_unpack_c/polyz_unpack_c_harness.c | 365 | `8d4a68a217b1f29174eab59348bcd0f9dc21ce69d147ae8049cc0822022f3c7d` | 0 |
| vendor/mldsa-native/proofs/cbmc/polyz_unpack_native/polyz_unpack_native_harness.c | 204 | `167850a9aae54273f22f4f3c61774192a2ae90dcf8cc4b6e5e912b5a0e8c700f` | 0 |
| vendor/mldsa-native/proofs/cbmc/power2round/power2round_harness.c | 214 | `da7ca4f0fe1941cc884a9d6220e32ee3726a5fe00b0bdd41e0badf354c98dbfd` | 0 |
| vendor/mldsa-native/proofs/cbmc/prepare_domain_separation_prefix/prepare_domain_separation_prefix_harness.c | 338 | `f35957138eac0b01011cc8a03a71d781141f104d472c69ded9a78a86e465b282` | 0 |
| vendor/mldsa-native/proofs/cbmc/reduce32/reduce32_harness.c | 197 | `725225bb92a0e44a4e9102a836bf05aace2beb90b069a88cb9e39991bab73025` | 0 |
| vendor/mldsa-native/proofs/cbmc/rej_eta/rej_eta_harness.c | 492 | `5a4e8571621f0ae80b9a2da803e820648a6c0214f41ce3a86be5e69d7a6708ac` | 0 |
| vendor/mldsa-native/proofs/cbmc/rej_eta_c/rej_eta_c_harness.c | 555 | `984de377f74fd69703f22c3c2ecba12b02bfd86f56af05dd84a956f65c71e4d0` | 0 |
| vendor/mldsa-native/proofs/cbmc/rej_eta_native/rej_eta_native_harness.c | 492 | `5a4e8571621f0ae80b9a2da803e820648a6c0214f41ce3a86be5e69d7a6708ac` | 0 |
| vendor/mldsa-native/proofs/cbmc/rej_uniform/rej_uniform_harness.c | 508 | `978cfa69c16c19ad668eea07cb18237ad19ce1309d37a80c42d7d596590b3c00` | 0 |
| vendor/mldsa-native/proofs/cbmc/rej_uniform_c/rej_uniform_c_harness.c | 516 | `3df2cba3e53afa788b334709c77740763d52b35fc0509bd250b60ecdfb36125a` | 0 |
| vendor/mldsa-native/proofs/cbmc/rej_uniform_native/rej_uniform_native_harness.c | 508 | `978cfa69c16c19ad668eea07cb18237ad19ce1309d37a80c42d7d596590b3c00` | 0 |
| vendor/mldsa-native/proofs/cbmc/run-cbmc-proofs.py | 16123 | `0cf33268a521d573aaa2c2063265dd0986bbb2e7fda50c5bce2598442af28638` | 0 |
| vendor/mldsa-native/proofs/cbmc/shake128_absorb/shake128_absorb_harness.c | 254 | `ffe929e975d1858338b860516f649bcefb3ba8a67b34202deeea6c5ac99b6955` | 0 |
| vendor/mldsa-native/proofs/cbmc/shake128_finalize/shake128_finalize_harness.c | 208 | `6cc48af79f24865e33690bd3207e382cc0e81ea018ff5c647d305de700a45724` | 0 |
| vendor/mldsa-native/proofs/cbmc/shake128_init/shake128_init_harness.c | 204 | `3852905daf05da84e2278f38836323066abe5a84fafb0c7272c00b90886ad7cd` | 0 |
| vendor/mldsa-native/proofs/cbmc/shake128_release/shake128_release_harness.c | 207 | `c803522db52c3c1bdd76dd5875215505ffe3612ac063c71ce32cefddd778508c` | 0 |
| vendor/mldsa-native/proofs/cbmc/shake128_squeeze/shake128_squeeze_harness.c | 261 | `a331241aa65a8ab8ab9124a145443161428e5e1848be3d29286880eedc488fb9` | 0 |
| vendor/mldsa-native/proofs/cbmc/shake128x4_absorb_once/shake128x4_absorb_once_harness.c | 457 | `2673de3726cac76151641bb219f4826052bd299287610e7aa074df21d42b0b81` | 0 |
| vendor/mldsa-native/proofs/cbmc/shake128x4_squeezeblocks/shake128x4_squeezeblocks_harness.c | 520 | `df05655fb74dd32d8644092575a659383477d3ad9e11f97748965bb2775b11fb` | 0 |
| vendor/mldsa-native/proofs/cbmc/shake256/shake256_harness.c | 268 | `f0252e6a66aebcc7f4377bdd924b1c57746f58a2f3bfa6cb690d005f405d4c02` | 0 |
| vendor/mldsa-native/proofs/cbmc/shake256_absorb/shake256_absorb_harness.c | 254 | `25d04147e7948c34b95b921222a5fd87978db34cd749748301e73e72c5fe2bde` | 0 |
| vendor/mldsa-native/proofs/cbmc/shake256_finalize/shake256_finalize_harness.c | 208 | `7b3d3a4f37d1005377d0884d93ca6b771c9a1fc43461c5cd7c078e54d84d856a` | 0 |
| vendor/mldsa-native/proofs/cbmc/shake256_init/shake256_init_harness.c | 204 | `fa067930119c65ed016589ac289e558cc55d866d276c1aab72983801251d77c3` | 0 |
| vendor/mldsa-native/proofs/cbmc/shake256_release/shake256_release_harness.c | 207 | `5fba1e02a3c7cc7589edba89bf49ad08d6226bbdbb103a0055ff2fb7e28a8d8e` | 0 |
| vendor/mldsa-native/proofs/cbmc/shake256_squeeze/shake256_squeeze_harness.c | 261 | `4c4db9c83ca163a9d1e609967aaa40418086d16919fefb2726e82f920610e1b8` | 0 |
| vendor/mldsa-native/proofs/cbmc/shake256x4_absorb_once/shake256x4_absorb_once_harness.c | 457 | `5f009ba561567b35e620e0b893a547361efbf444a40c35e8e5d8dbe6851034fb` | 0 |
| vendor/mldsa-native/proofs/cbmc/shake256x4_squeezeblocks/shake256x4_squeezeblocks_harness.c | 520 | `213521bcc666f500fa149c8dabec63638818050d52164e9fe0bd65857b832f7f` | 0 |
| vendor/mldsa-native/proofs/cbmc/sign/sign_harness.c | 385 | `c55578eb683a6e15aa017a2fbb8f982712ef7c225dee1e2aac3f44270f4fcfb3` | 0 |
| vendor/mldsa-native/proofs/cbmc/sign_keypair/sign_keypair_harness.c | 282 | `b75d18b1af095e0c6c6691228ad684b64df49a5f38ddf1d56710e09a8b55d0f6` | 0 |
| vendor/mldsa-native/proofs/cbmc/sign_keypair_internal/sign_keypair_internal_harness.c | 286 | `2570459c0c5720f01d04b858158a80017433683860b0feb072d15e8c20d18552` | 0 |
| vendor/mldsa-native/proofs/cbmc/sign_open/sign_open_harness.c | 396 | `69bad8f112936b863f41f67d96353e9835f18e6ebb557b545014ac5ffbbd6edc` | 0 |
| vendor/mldsa-native/proofs/cbmc/sign_pk_from_sk/sign_pk_from_sk_harness.c | 299 | `2295bce73a3f8983c9504e091dcf071d6731417d13aaa6131cff1ac3017a4f70` | 0 |
| vendor/mldsa-native/proofs/cbmc/sign_signature/sign_signature_harness.c | 409 | `f60db4865279c7ba91cb013be960acb736e11b3972281ba926e4917d98fe41b6` | 0 |
| vendor/mldsa-native/proofs/cbmc/sign_signature_extmu/sign_signature_extmu_harness.c | 332 | `1836b4bddf8d4fe59ef08857440ff0b07004fcfe0310d261b33d15edbea07832` | 0 |
| vendor/mldsa-native/proofs/cbmc/sign_signature_internal/sign_signature_internal_harness.c | 456 | `9f08ad9e854e850866ea1d5e4cd3cee72e7b675a002281d2d8aa2c19b60dc2c1` | 0 |
| vendor/mldsa-native/proofs/cbmc/sign_signature_pre_hash_internal/sign_signature_pre_hash_internal_harness.c | 487 | `062764b60b7a236b5d23cf2305069f76cb7207844cbcf901e08ffca9b7c78218` | 0 |
| vendor/mldsa-native/proofs/cbmc/sign_signature_pre_hash_shake256/sign_signature_pre_hash_shake256_harness.c | 459 | `c417ccc690fd8494d8f616589b773b7f564c789ce8069b6a882ce5dbd953a6a5` | 0 |
| vendor/mldsa-native/proofs/cbmc/sign_verify/sign_verify_harness.c | 427 | `0bb35259822af765896d6e0e5696eaae5c0eba8bad386a47fadc8a5a8969a8f1` | 0 |
| vendor/mldsa-native/proofs/cbmc/sign_verify_extmu/sign_verify_extmu_harness.c | 352 | `bbba233035e102ecd3612f2c182d7b1480eba3595921031ae2d0552a6d98adde` | 0 |
| vendor/mldsa-native/proofs/cbmc/sign_verify_internal/sign_verify_internal_harness.c | 457 | `8b2399f221589beeafc508221db1daf952dcc015c9fa9ac77873945cf8bd33e2` | 0 |
| vendor/mldsa-native/proofs/cbmc/sign_verify_pre_hash_internal/sign_verify_pre_hash_internal_harness.c | 462 | `f8097d88c40a83648bffdaff7be4e5ae2ec16d2ae2bc3943b0ed928fb82402a2` | 0 |
| vendor/mldsa-native/proofs/cbmc/sign_verify_pre_hash_shake256/sign_verify_pre_hash_shake256_harness.c | 434 | `300e312dd72cf1a6e419351e5074d05cf7ba10467b1ee0a1eb7f920741297e1d` | 0 |
| vendor/mldsa-native/proofs/cbmc/sys_check_capability/sys_check_capability_harness.c | 261 | `dacdec03b1cece8f747f4aa0f760a6f1a0e7e3af2c42463eae094fa3e5717f5e` | 0 |
| vendor/mldsa-native/proofs/cbmc/unpack_hints/unpack_hints_harness.c | 342 | `ad42b5e0e26fe0fd278b32ab4df5bf130b4588419caf4dad41ded883c2c04267` | 0 |
| vendor/mldsa-native/proofs/cbmc/unpack_pk/unpack_pk_harness.c | 213 | `6c61550567df357d0c730bdc1495982a993ae8720c7c951c313a200d4766bb1f` | 0 |
| vendor/mldsa-native/proofs/cbmc/unpack_sig/unpack_sig_harness.c | 263 | `3cdcbacd35378bac719449eaff2592b6ca7a6fa2fab16d16bb0eb12542e1804f` | 0 |
| vendor/mldsa-native/proofs/cbmc/unpack_sk/unpack_sk_harness.c | 262 | `7bca77f595eaa715552d94bd6f809382eba95b96dc96de0019eaa716118a2624` | 0 |
| vendor/mldsa-native/proofs/cbmc/use_hint/use_hint_harness.c | 201 | `4d037cbcea49b6b2e190eaf2db0c7d5f994723204153574f554a35e13e39c11b` | 0 |
| vendor/mldsa-native/proofs/cbmc/value_barrier_i64/value_barrier_i64_harness.c | 185 | `e892a64739e6dffdff0d178c8d99c1237195d43db1e27b038890f2fdd995810a` | 0 |
| vendor/mldsa-native/proofs/cbmc/value_barrier_u32/value_barrier_u32_harness.c | 186 | `5accd53c3deaa9e64b21bb5056b3f08fb07749bbe8dc9c433ebb66f1bed03aeb` | 0 |
| vendor/mldsa-native/proofs/cbmc/value_barrier_u8/value_barrier_u8_harness.c | 257 | `43b718b7fd4adcd05ccd0bc0b44753aa30f096fd954bee526eafcdaa250a6a12` | 0 |
| vendor/secp256k1-zkp/contrib/lax_der_parsing.c | 3595 | `4da2ecdc0a3b9dbb9029d188bb0243764a3c2f2324613a688f1ac4d3fc878851` | 0 |
| vendor/secp256k1-zkp/contrib/lax_der_parsing.h | 4230 | `7f3e8ba009f19a5f2759c9065af02cc8e62351100d69f8ae7e762fa4b65ea675` | 0 |
| vendor/secp256k1-zkp/contrib/lax_der_privatekey_parsing.c | 5112 | `48352c75520eecd141936c0011601925510cdf60afd3e46e79f0a0547cbc78da` | 0 |
| vendor/secp256k1-zkp/contrib/lax_der_privatekey_parsing.h | 4016 | `3420812d623c0f2f86debe0535f98eab9b929036bb2fee2de8e3b1adc3e1a0b9` | 0 |
| vendor/secp256k1-zkp/include/secp256k1.h | 42403 | `328da0a2e0433e9cdcfae1fbde894d50a17c349e366e03f3f99fe8558ebd9af9` | 0 |
| vendor/secp256k1-zkp/include/secp256k1_ecdh.h | 2560 | `ad314d14cb79a79d4113862f21e0deccf37962db7811c801dab2899f91dd8222` | 0 |
| vendor/secp256k1-zkp/include/secp256k1_ellswift.h | 9148 | `620db468b1c13968946e9f404ceb59a3f11c895603bf1dcd3399567d7bf10e99` | 0 |
| vendor/secp256k1-zkp/include/secp256k1_extrakeys.h | 10870 | `7c3468c9fd192ad152c5cf042cb44938961d752fcf19966123ce6a5e3fd31637` | 0 |
| vendor/secp256k1-zkp/include/secp256k1_musig.h | 28115 | `b7e7772dfc78585dac1d7c2921a44dc62b3aec92df50818fdf985eaeb88139ae` | 0 |
| vendor/secp256k1-zkp/include/secp256k1_preallocated.h | 5966 | `b7283d4cc9c13bb2572dc92e69cea76f3270403baf5748ea4d91a1064b951b85` | 0 |
| vendor/secp256k1-zkp/include/secp256k1_recovery.h | 5250 | `e00678a1108acb36c6631a1e290cf33813b0ed5965d23226367008f58abb27f2` | 0 |
| vendor/secp256k1-zkp/include/secp256k1_schnorrsig.h | 8177 | `8185d6c6ea3234fff05f38fad4b1b6f48f0574ab599dfc87297ab9bca0abfca5` | 0 |
| vendor/secp256k1-zkp/src/assumptions.h | 4667 | `cc875f356cc8f7f272def71f7d7261e44cc27a18a5b668cd8192c84d238e4e68` | 0 |
| vendor/secp256k1-zkp/src/bench.c | 10186 | `08b5b70457175cfd2928d361ae7f0ac2c055c2de0857523ac647c002cc11d237` | 0 |
| vendor/secp256k1-zkp/src/bench.h | 4778 | `82667b60e67a152936f8b3e7be8eb0224dc8f6f806b51edd0c4c108eb512cdc8` | 0 |
| vendor/secp256k1-zkp/src/bench_ecmult.c | 15580 | `c742aeab4b1af836ac736f5adc78d28482c9684a6823c0171360995aad9c90b8` | 0 |
| vendor/secp256k1-zkp/src/bench_internal.c | 17480 | `d7704fd54f646f295497b9f8c12c2cf82eab2f42179de64bcbaef05cc215e260` | 0 |
| vendor/secp256k1-zkp/src/checkmem.h | 5141 | `450e7928206b994693912ad5c9bbb890ca5250feded149f5025f67ad30d6d711` | 0 |
| vendor/secp256k1-zkp/src/ecdsa.h | 1164 | `f97753416b0971133ad9d8acf9af02259931d0285a0333a9753201a353070ef6` | 0 |
| vendor/secp256k1-zkp/src/ecdsa_impl.h | 10462 | `1e6041a11a45baa093df0c8037035bc0ac5a9a2b922cc2c9966aa4c14c2e5468` | 0 |
| vendor/secp256k1-zkp/src/eckey.h | 1449 | `cf511599285faecd27ace6191eca3945d85bc852b11076a1b1727759a6b03056` | 0 |
| vendor/secp256k1-zkp/src/eckey_impl.h | 3457 | `57ae9e8d50dc04bf7ee54cd13e56f1801c3cb587de6baa81c630fd8153f6423b` | 0 |
| vendor/secp256k1-zkp/src/ecmult.h | 2679 | `3158078d831594da3ff1222d8547ddca1a6ca28335ded360100fdced3091270c` | 0 |
| vendor/secp256k1-zkp/src/ecmult_compute_table.h | 1073 | `5a8ce69b18d777c3ad608ef173fd6a47c75b9c37bc6801f19ca4c44eb4b9f8f6` | 0 |
| vendor/secp256k1-zkp/src/ecmult_compute_table_impl.h | 1913 | `787c123550f8a7d03a72463abec9057ef7fa60b55ddbbb4fd274ee254e669401` | 0 |
| vendor/secp256k1-zkp/src/ecmult_const.h | 1354 | `4705e7baabcbf8fd1853f8cef45a7f6a3075b98925d91cc209afda2c956942ba` | 0 |
| vendor/secp256k1-zkp/src/ecmult_const_impl.h | 19584 | `07238bcf17c3292bb8198f7f37baf068bdc9a6a57f843c439e220eb08f400607` | 0 |
| vendor/secp256k1-zkp/src/ecmult_gen.h | 5368 | `992ad0e8f2c0dd4cb699af8a5db7c640e904e7696b98f008d9a164933f16ecbf` | 0 |
| vendor/secp256k1-zkp/src/ecmult_gen_compute_table.h | 672 | `51eb54b0cb7b49b25cf751efb2799322d73c97bc9bdd2a263feff2d2d6eeff9f` | 0 |
| vendor/secp256k1-zkp/src/ecmult_gen_compute_table_impl.h | 4705 | `9ae524743bb5871bff7e41e48b61218336b1919769132aafa944283ef1bb88f2` | 0 |
| vendor/secp256k1-zkp/src/ecmult_gen_impl.h | 16392 | `12e5d89186b8663e82eccbb868d9e82b266b06d9c931aa7c4cc179bc83c42cb5` | 0 |
| vendor/secp256k1-zkp/src/ecmult_impl.h | 34279 | `1d9505cf8d42d9c3e2006288bd95c48f876cf87701d8095fc71817b6a171f110` | 0 |
| vendor/secp256k1-zkp/src/field.h | 15120 | `481acd5c23d25ca8f5d963616ab9c3e94cf003fdb4b24608def011d7e9e5c955` | 0 |
| vendor/secp256k1-zkp/src/field_10x26.h | 2338 | `ba9a43b62e7e70e6e18af2787bd01dfc3a57fea527cf8ad0333194211ac7d7de` | 0 |
| vendor/secp256k1-zkp/src/field_10x26_impl.h | 52106 | `6f209a533fd96e73f4c92b101bd3ca46a2f7553967ba7f44650a68ccbf4fbcf6` | 0 |
| vendor/secp256k1-zkp/src/field_5x52.h | 2380 | `cbaa91c253ba84d99efcd334c7a39906c164d5edf3cde81200a44a606205cdce` | 0 |
| vendor/secp256k1-zkp/src/field_5x52_impl.h | 19360 | `8104a1b630635c9cc89628142c9fa7afc6f31a888fe50c8ebb2bdf69ca208975` | 0 |
| vendor/secp256k1-zkp/src/field_5x52_int128_impl.h | 11341 | `ee6d585731507c51dc8acd819b66556cf0cd804da1a4b6072a79c17eafbc940a` | 0 |
| vendor/secp256k1-zkp/src/field_impl.h | 14052 | `33cb488ee009334a7a2ac52a7eabe39795bd184da0238e7acf73ae11374643b3` | 0 |
| vendor/secp256k1-zkp/src/group.h | 11798 | `f5f85b79a0c1659bf0a85ff199844b60fc2ace13d46c15fcac518e1db0ee1fb0` | 0 |
| vendor/secp256k1-zkp/src/group_impl.h | 34553 | `f55f65b95486c79ab44b55a767fb0879b27983a119757f9207b3c367478ff29e` | 0 |
| vendor/secp256k1-zkp/src/hash.h | 1916 | `e0e586994dd4eb8d6fc6b1846519c1f71f00cf3c2f956264fb265c3e7523e1aa` | 0 |
| vendor/secp256k1-zkp/src/hash_impl.h | 13620 | `1dc20950aea3e66745a3f44f902e1de94b7effa8f3f82e40312f4e384f8dd88a` | 0 |
| vendor/secp256k1-zkp/src/hsort.h | 1685 | `220cb669835d34c252598ecff860c93edda337a9f8c2fc07b2b6cead7d48b284` | 0 |
| vendor/secp256k1-zkp/src/hsort_impl.h | 4798 | `2861489c01b927b27d99efe173799a812434748b4addd30d102187ce4f3b66a9` | 0 |
| vendor/secp256k1-zkp/src/int128.h | 3622 | `89ac5d91d64f857038d063dd70eec4b29b4f32aa218c790fe049137c347186cb` | 0 |
| vendor/secp256k1-zkp/src/int128_impl.h | 376 | `5683c02dfc495639da259d80624711c1c449bbaee6186729e399e713a28b4719` | 0 |
| vendor/secp256k1-zkp/src/int128_native.h | 581 | `b4c52c7ff091083f5eca9879b98641c7a38356a3c5321cbcc22ae1573e7711e1` | 0 |
| vendor/secp256k1-zkp/src/int128_native_impl.h | 2881 | `ecaafefadbde3db034d4f44678096833d2d113fd21b4ff7044095b6153ec03a8` | 0 |
| vendor/secp256k1-zkp/src/int128_struct.h | 229 | `0733b3a65719a1e9a8fb3564c71a38f2f31ca3522f40087d536dba90361b66e7` | 0 |
| vendor/secp256k1-zkp/src/int128_struct_impl.h | 7884 | `0b4e2200327f5357078ba43b0e0514c58c2b1eb217b87ebc14d95efb913b5be2` | 0 |
| vendor/secp256k1-zkp/src/modinv32.h | 1865 | `774887ccd462b145434d1d6b9ae9455aa3618e791544a2b61267e18931d5010d` | 0 |
| vendor/secp256k1-zkp/src/modinv32_impl.h | 33492 | `befe02af7099a871677c7b05a81302dff5a4dc1d59f19b20bcb58cc28e096112` | 0 |
| vendor/secp256k1-zkp/src/modinv64.h | 1969 | `b71cf177d768beac28fcb4f0ef545aafaad16ad0f275c70ee4c60b5f7549ac41` | 0 |
| vendor/secp256k1-zkp/src/modinv64_impl.h | 37653 | `1254dc7ea941fc4d4ef0a85eed80db58d9e2647a8b8d19238d6afc048d63764d` | 0 |
| vendor/secp256k1-zkp/src/modules/ecdh/bench_impl.h | 1761 | `3929ead352b3b6425f0fdf94a1b2268d124cc0176929ae6ea3b4fa82abac0bbf` | 0 |
| vendor/secp256k1-zkp/src/modules/ecdh/main_impl.h | 2500 | `c507af8f5c6a408765ed96879739737a86cf0da64a65e9e5d0f6eb1467b1db1f` | 0 |
| vendor/secp256k1-zkp/src/modules/ellswift/bench_impl.h | 4399 | `8973d64bda27eb72a4807aae665a1a2932d624370f9d40f8833f7c8f03b05564` | 0 |
| vendor/secp256k1-zkp/src/modules/ellswift/main_impl.h | 26216 | `707f86acbd1bef943bf313185bfa72068062ef385d33750e1cf461a975b6f1db` | 0 |
| vendor/secp256k1-zkp/src/modules/extrakeys/main_impl.h | 9961 | `a58762afb6a494aaec984d2e65adacf1125be5e55ad2904af0f26e490cc0d3b4` | 0 |
| vendor/secp256k1-zkp/src/modules/musig/keyagg.h | 1288 | `4d8bfe0a8955d2789205df2cd90e6bf9f53d0526f108bcbed051442c765d3e5b` | 0 |
| vendor/secp256k1-zkp/src/modules/musig/keyagg_impl.h | 11081 | `d3604de574cbf96fd7c0656c6ff9500645bf27f769709928e7336c6463a9346f` | 0 |
| vendor/secp256k1-zkp/src/modules/musig/main_impl.h | 426 | `9ec7e6082aa496353466769bb9f7705c32caf8d060b0c92815cb37f6c4265654` | 0 |
| vendor/secp256k1-zkp/src/modules/musig/session.h | 861 | `c256c3742a68849520569845640f152a22a4a8c21a96040cf0c1054516983980` | 0 |
| vendor/secp256k1-zkp/src/modules/musig/session_impl.h | 30822 | `9dcc4c823bd1bb9c1e68d0e2a656528f5c45ab2c9d2cf3f65945587943239f6b` | 0 |
| vendor/secp256k1-zkp/src/modules/musig/vectors.h | 37797 | `c7cd9dc3804d864d17e43c5b00335a405a3bc4a30861838ac4599a213231e132` | 0 |
| vendor/secp256k1-zkp/src/modules/recovery/bench_impl.h | 2320 | `20d13192a4aabaa52ac4c2a2da772d8aafef00773051836b25faa2816226b386` | 0 |
| vendor/secp256k1-zkp/src/modules/recovery/main_impl.h | 6135 | `fbec2358a560b669d85720108b0b1a8f653c91531a88ded0a1da339445266cc9` | 0 |
| vendor/secp256k1-zkp/src/modules/schnorrsig/bench_impl.h | 3967 | `1e9f3b239e1fac3f2b9f2c2e5d093f9d9811b1554e272a52f3ba8e85efae345a` | 0 |
| vendor/secp256k1-zkp/src/modules/schnorrsig/main_impl.h | 10281 | `d627be29e9a7e1e3b607df983c9f4e7b66990f056c7fcc242a16ee0345b03819` | 0 |
| vendor/secp256k1-zkp/src/precompute_ecmult.c | 4014 | `9d4d5f79ae0b7c2a2283b33486a397e2a4de40a68a35d15e3e52db55baa13d29` | 0 |
| vendor/secp256k1-zkp/src/precompute_ecmult_gen.c | 3879 | `bf49c461eda49ce4967396a3f6cf25aa92ec7029efb7609836fec8701c04ad7a` | 0 |
| vendor/secp256k1-zkp/src/precomputed_ecmult.c | 2409168 | `1fba19c482de09f566ed9e7bf6a526e4edb59a1cf38218e3ab413000a0e0deda` | 0 |
| vendor/secp256k1-zkp/src/precomputed_ecmult.h | 1585 | `d792b8a49759deff5f1e4092558fa9ae11d24e02695e44bee63a8f0ba8e18503` | 0 |
| vendor/secp256k1-zkp/src/precomputed_ecmult_gen.c | 259715 | `c0a7af0884b7b07962be67e9da674e0d75a8d412d116153b8eae2a9e5527d401` | 0 |
| vendor/secp256k1-zkp/src/precomputed_ecmult_gen.h | 973 | `8f514bed441bccf7e34ff05ff49d3a44e9395519a8fdcf176e6aeab7b5dbd5fc` | 0 |
| vendor/secp256k1-zkp/src/scalar.h | 5460 | `cdc9a0053321cc541c81bb02f5c4dbba1b9489947908b3187a7c3462c9e806bb` | 0 |
| vendor/secp256k1-zkp/src/scalar_4x64.h | 801 | `42aed583b28bda7982c54a6f63e50c0ae5f9c27d5f66d92ec6bf6c90e765735a` | 0 |
| vendor/secp256k1-zkp/src/scalar_4x64_impl.h | 32955 | `992b203310337ad913afbdc29691f184462aba37d121c13a76581e9ff2c891b6` | 0 |
| vendor/secp256k1-zkp/src/scalar_8x32.h | 725 | `0614cea113aea88a47ef3b2ba8167722e850d7b2a696a4f16b03ec9a320ef1d6` | 0 |
| vendor/secp256k1-zkp/src/scalar_8x32_impl.h | 29162 | `7dd402b15ae1c9b884f20a86c952db4aabb7c13fdba0a4d9addc7e752bc5a982` | 0 |
| vendor/secp256k1-zkp/src/scalar_impl.h | 12113 | `6ba654bd4edc0349d1d7f1dfc25ba2d73dd9f2ecdca8078e384bf7b7837d663f` | 0 |
| vendor/secp256k1-zkp/src/scalar_low.h | 1135 | `3cab20db10224ff85ee7c6d975d2968c1370ed8e96ea26b94650f6e2bac31ac4` | 0 |
| vendor/secp256k1-zkp/src/scalar_low_impl.h | 5967 | `b44c726ac42516345dff05b1d964807609e7c53112aefe584aa0a1d060fb8b9f` | 0 |
| vendor/secp256k1-zkp/src/scratch.h | 2224 | `4af5e1ff665c0418bcc5b1c2de954e7b377f9bdfdd4309e0296938918fac11ef` | 0 |
| vendor/secp256k1-zkp/src/scratch_impl.h | 3677 | `294a55d429fa4cc9dec46ade345bbb2bfdff4055eb1cbf1ba6168a23e5e74db6` | 0 |
| vendor/secp256k1-zkp/src/secp256k1.c | 29096 | `6a3cad3929bfd49c8f99d36c3e949f4067380dd40c4ba6b81a1ddc608fc65fd4` | 0 |
| vendor/secp256k1-zkp/src/selftest.h | 1271 | `fa95cb3e35c5d121da797653a58c4c43370d51245aa43b65e0292ce3adf09dd4` | 0 |
| vendor/secp256k1-zkp/src/testrand.h | 1886 | `b1708cdab67d44311b97af6f77c719f6dfc03d8c53e5e686bc1d9fd967a49687` | 0 |
| vendor/secp256k1-zkp/src/testrand_impl.h | 5585 | `5410f491bb7dc8e40715b597fb22c2fe16df52602beea32a2e045684a255bc76` | 0 |
| vendor/secp256k1-zkp/src/testutil.h | 4355 | `c904296216746f591f0404ef9507a93090bdd5b2826a28834154d79b5f1f0041` | 0 |
| vendor/secp256k1-zkp/src/util.h | 15742 | `a2d678ac4126c742cee549dda6de8b2def62cbd87103ec7e9fd42e04b3881a36` | 0 |
| vendor/secp256k1-zkp/src/util_local_visibility.h | 402 | `d47d4a58f40157ab2a298151f366c5ebec8f7a1e7aaba88e36b530b1c01584ca` | 0 |
| vendor/secp256k1-zkp/tools/symbol-check.py | 2416 | `1706069df728c1a2ac1d2578897076713c16eed73315be6c83ad9690007bca70` | 0 |
| vendor/secp256k1-zkp/tools/wycheproof_utils.py | 427 | `9f2c2368953eeb3c9b7c3b31a807cde76b3106df93fbb975993638d5eb1a1e8a` | 0 |
| vendor/sphincsplus/benchmark.py | 1333 | `6925bba99222e3667eef0e54416df34748650c868737e4143ee97780ba2b655d` | 0 |
| vendor/sphincsplus/haraka-aesni/context.h | 224 | `9bc8fdb0a0806946f5323c2c6eceb380380dbd0f84b23321ef3f1d027953c1aa` | 0 |
| vendor/sphincsplus/haraka-aesni/haraka.c | 22888 | `1bbec250d990bc84459f12bcdcfae1c82d2ab1f6eba55daa8c5419f94ef86d7a` | 0 |
| vendor/sphincsplus/haraka-aesni/harakax4.h | 1165 | `68a1c2f8f83f5f89ffb5fc4b02b1a81cd4a4da4e5cc9880a4d908b07c656d8e1` | 0 |
| vendor/sphincsplus/haraka-aesni/hash_harakax4.c | 999 | `e0ee5b5b6b44ae8f04038eee5223e8638b57954e84b41c04e40129a00d9b53b8` | 0 |
| vendor/sphincsplus/haraka-aesni/thash_haraka_robustx4.c | 3506 | `426efc721b11778b64e84216280c4854d5c19fe164340b1b5df7e79e0ca9da56` | 0 |
| vendor/sphincsplus/haraka-aesni/thash_haraka_simplex4.c | 2307 | `0e83c32e43788e7a364db2c517c87d2511ce6b2019d37afdf5e3cf424dea046b` | 0 |
| vendor/sphincsplus/ref/PQCgenKAT_sign.c | 7001 | `793da075036e906843d0ef33fd28d39761a08ee94cd84c98c0cef996fc0ccd70` | 0 |
| vendor/sphincsplus/ref/address.c | 2957 | `e07ecc87e564db0f2055b761d9b9a56edec7cb7508e3410117e857f4e4e5a5aa` | 0 |
| vendor/sphincsplus/ref/address.h | 1683 | `86b33648b11e72d09c21e4b478881f5e6aaf6770ef47a29df6fd7d424aaa4a88` | 0 |
| vendor/sphincsplus/ref/api.h | 2116 | `a0c7abd648a4a695ff031f034a68e431559338c37890b428f21ce3fd91314636` | 0 |
| vendor/sphincsplus/ref/context.h | 479 | `6953afd8e8d45fab9f47bf8beeac549fdb45aeb02c2d2e263c1304b3d11ccc85` | 0 |
| vendor/sphincsplus/ref/fips202.c | 19100 | `f2a076880fa2d32e585c4ba30750171b4b842591d1f6ade6038cf28567ea69c9` | 0 |
| vendor/sphincsplus/ref/fips202.h | 1676 | `125d3ac43b0c81b4b796de97955d8016478183fd4c10feb73858e0e45362e0e8` | 0 |
| vendor/sphincsplus/ref/fors.c | 5322 | `efa5c96c53814d84ea9a142dcf966adf17873a0f73a7a8704c24222902271ec4` | 0 |
| vendor/sphincsplus/ref/fors.h | 1104 | `349cbe538ae0c6510b8ceeb9685e40b226a7386ce2e2454c3269c354cb42f2a5` | 0 |
| vendor/sphincsplus/ref/haraka.c | 26095 | `529c127e606f47982dc3ac46b43b40d295098bddb2cbd93d703d9528d6af1f9b` | 0 |
| vendor/sphincsplus/ref/haraka.h | 1494 | `b48a0c762064217119557cc2e432ebcef2b063981a6fbd4f5b1df0e82f34d059` | 0 |
| vendor/sphincsplus/ref/haraka_offsets.h | 1059 | `499ba06ce128175145c661021a23cf140bba2e95288c664a5352d632e5774a5b` | 0 |
| vendor/sphincsplus/ref/hash.h | 967 | `2b09886addb6b9628e645d0054bc06ff1eb418f59a778c8a4b741b7184a6b1bd` | 0 |
| vendor/sphincsplus/ref/hash_haraka.c | 3032 | `e8919ed13da9675288d12b333dc50ea0ba3706d13ee8e618792d41455dda96b3` | 0 |
| vendor/sphincsplus/ref/hash_sha2.c | 6714 | `bc804b4d9b4df95531a8304dfdc01b7438870672d30ab0e7ca34aa4fed934f7a` | 0 |
| vendor/sphincsplus/ref/hash_shake.c | 3063 | `b4720bbf56f843e333391580ad9e9437f464f502331d3ce06e114179c5e0e4bc` | 0 |
| vendor/sphincsplus/ref/merkle.c | 1973 | `822c402a9dbe43274d2dad92ff215e80b20a5464c16ac59ee57d2d5079aedea6` | 0 |
| vendor/sphincsplus/ref/merkle.h | 571 | `2f704262633f56514218bb79798079102e50393879520c9d05b2bf77005ce23f` | 0 |
| vendor/sphincsplus/ref/params/params-sphincs-haraka-128f.h | 2131 | `8d67a228f57719cab9f8bc581af5fc321abb0393167adb1d95a7800e64f027ae` | 0 |
| vendor/sphincsplus/ref/params/params-sphincs-haraka-128s.h | 2131 | `bf9ea2f8825d64f14ee2f87504394b84e7d9c831080b26899123e7f8ab6ccaf9` | 0 |
| vendor/sphincsplus/ref/params/params-sphincs-haraka-192f.h | 2131 | `b127c87293548adf91d4e02cbb96968b3fa6a21f2fea02193d00c2552cec69a7` | 0 |
| vendor/sphincsplus/ref/params/params-sphincs-haraka-192s.h | 2131 | `0cf3601315cdc13ca78a6ae85ddc7b00e61363fe17eca9387afb51387adcd8ff` | 0 |
| vendor/sphincsplus/ref/params/params-sphincs-haraka-256f.h | 2131 | `bae1adff2781a5a9aad0c20b9d11b20cc5518a858449555227a37ab8b50ebfba` | 0 |
| vendor/sphincsplus/ref/params/params-sphincs-haraka-256s.h | 2131 | `6c329295f338557ed43495eee00a31bcacb8c948e3ce9a3ea344f668e996f172` | 0 |
| vendor/sphincsplus/ref/params/params-sphincs-sha2-128f.h | 2348 | `4bb379eec38814fd6a817016bc62810ad055e38f8902d268a464cd53d062c33b` | 0 |
| vendor/sphincsplus/ref/params/params-sphincs-sha2-128s.h | 2348 | `58df8304a35570699ac875b2cf233baee9127ec4df29f2a5461253076794ca6a` | 0 |
| vendor/sphincsplus/ref/params/params-sphincs-sha2-192f.h | 2355 | `570eed62eae97d14385f678965ce293bb51030d4be1a216a586636aa91636637` | 0 |
| vendor/sphincsplus/ref/params/params-sphincs-sha2-192s.h | 2355 | `d14c7c6a5754f48a583453a693a36bb293dd70b1733bd3ccd4c7eb75c1fc5172` | 0 |
| vendor/sphincsplus/ref/params/params-sphincs-sha2-256f.h | 2355 | `59ad3656e20d674329b69ce972e4f3e1cfc8778f73219875b2cd7285c2f1e492` | 0 |
| vendor/sphincsplus/ref/params/params-sphincs-sha2-256s.h | 2355 | `6648b7c2acfeb1aaa410ee9038235175ec64679db2c371cd3cde3a0136ace5f0` | 0 |
| vendor/sphincsplus/ref/params/params-sphincs-shake-128f.h | 2130 | `de37a1ad4de21af24c70262a97b74927a0decb8275eae1ad34dcf5ed52daa2e1` | 0 |
| vendor/sphincsplus/ref/params/params-sphincs-shake-128s.h | 2130 | `da4f8c1ee5b475a8103d856d80dbec15276eb2f566ce44318dcd286faba05c1d` | 0 |
| vendor/sphincsplus/ref/params/params-sphincs-shake-192f.h | 2130 | `5524ce6e92393fa176d3f3897c612a402386c8ae1a2f089f53b4e7e005e6044d` | 0 |
| vendor/sphincsplus/ref/params/params-sphincs-shake-192s.h | 2130 | `75fae04788d85078b605b540a45d8478251c2c8bd0b052972e1b39c5b2da2b2a` | 0 |
| vendor/sphincsplus/ref/params/params-sphincs-shake-256f.h | 2130 | `5042072dde059ebafe3b938b8e31e3c3ca97dbc70a7a01407323eb389c2462a2` | 0 |
| vendor/sphincsplus/ref/params/params-sphincs-shake-256s.h | 2130 | `11852f080cb720d08026d2dda6fe410a5cba933dca5b70332f9e8deef1fbf997` | 0 |
| vendor/sphincsplus/ref/params.h | 81 | `a413a8ac8f601b4631980cb1b11201def25591e9423254301ee6f75894fbfe07` | 0 |
| vendor/sphincsplus/ref/randombytes.c | 762 | `5cfaf24e8a2d130b2fec5def511f635c18d381712e78050124ecaf71b2d69dfb` | 0 |
| vendor/sphincsplus/ref/randombytes.h | 129 | `cb0022583e425fcf2cbb9227519893e336d194b04e7d8083c4ed6c60dbbfd7e4` | 0 |
| vendor/sphincsplus/ref/rng.c | 5363 | `3f7fff913ed542ab52a29c0ce4498b7a271f8d4d6abc6d038bab54844c9a0aba` | 0 |
| vendor/sphincsplus/ref/rng.h | 1216 | `0c438e7e18515030d902540060cf6755486b17b43d1f1f0b1a79085d274a0a8a` | 0 |
| vendor/sphincsplus/ref/sha2.c | 21257 | `cbe87248a6a794cf92df33759cbad5ac5f1a2df390edcbb292f07d44baa2de09` | 0 |
| vendor/sphincsplus/ref/sha2.h | 1368 | `c5b7768e75d52c68111b3cdf3e1b192d52bccb85e0ba9fa0ac2437bc3f427f83` | 0 |
| vendor/sphincsplus/ref/sha2_offsets.h | 1042 | `fbbece33219c2fcc4c76616ea779fbec1a977715a9fc0ac2c9c1b61c2e902f76` | 0 |
| vendor/sphincsplus/ref/shake_offsets.h | 1055 | `8aba4f437e28c23e0c020fbf9d68422718bdd15544c46d1fe6e4fa22e4f6ef12` | 0 |
| vendor/sphincsplus/ref/sign.c | 8147 | `4015a353fa2b0433de4c1d0496a847cede14ffd7f9e60c92a25c8c2dffbce2a0` | 0 |
| vendor/sphincsplus/ref/thash.h | 276 | `9a81d94591cb7d97606b0927525e59994b70b0043301f47861f98570d9e3cec2` | 0 |
| vendor/sphincsplus/ref/thash_haraka_robust.c | 1324 | `ec2068778c4ba6a75be14cdf959a185127dcea5fedecea6f09c6a058361bfabc` | 0 |
| vendor/sphincsplus/ref/thash_haraka_simple.c | 1020 | `42aa839c7d1b0a75cbd0e77fba93ff31a8438bfea891fc3a8222b979bc8abd77` | 0 |
| vendor/sphincsplus/ref/thash_sha2_robust.c | 2376 | `794697e3b37e6031d209ddb0da003d0154c8739ca8cd48f20e11bbecdde5f6db` | 0 |
| vendor/sphincsplus/ref/thash_sha2_simple.c | 1793 | `a6da924ab60437c37466a1fd2afe65cf9d7ae8edaba8458d345209cbb901c688` | 0 |
| vendor/sphincsplus/ref/thash_shake_robust.c | 831 | `7e012384223389138748ffeadd2bcdcabf6693d2d69fdb20d471968590117424` | 0 |
| vendor/sphincsplus/ref/thash_shake_simple.c | 641 | `a15e1c60a9fc3f4aec37abb95c117c360b1f91e93a08dc0a00953acb9248baad` | 0 |
| vendor/sphincsplus/ref/utils.c | 5332 | `9c3d1b5929997d3986d66c826a73c0f2cd39b36c68122c8823719ac52f719887` | 0 |
| vendor/sphincsplus/ref/utils.h | 2378 | `06d3eaf20944104873d9e143dce2c049719d4aff4a5073c70551bed79c5fa314` | 0 |
| vendor/sphincsplus/ref/utilsx1.c | 3787 | `c66cb53481cc2a02c44e53e5ec428d9565b51ee3554e1445d29ae5b731486773` | 0 |
| vendor/sphincsplus/ref/utilsx1.h | 1009 | `1df02869660b96a0e79205bfa6bf09b999392c42aeb5469f64b565cd5cdef752` | 0 |
| vendor/sphincsplus/ref/wots.c | 3225 | `e0624601c3bfa0c2878ed7be1efb75a490a10453d3e2ca70910883fe46258c7e` | 0 |
| vendor/sphincsplus/ref/wots.h | 663 | `18a7c81e8006bef01e33e2894f51f3d54583f43c29a631691cbb1e1c46674655` | 0 |
| vendor/sphincsplus/ref/wotsx1.c | 2269 | `37159c12b101033de2a53fe4125f9c5d8f254115e9e19f6b34d3b715c03f759b` | 0 |
| vendor/sphincsplus/ref/wotsx1.h | 1190 | `fdf5431c896cba8814fb5a682df259ba5267d0643e726469801ee9f33810a024` | 0 |
| vendor/sphincsplus/sha2-avx2/context.h | 267 | `63af0bb93c6c7b6647c096187fffa93ae85f420f7b1bbc0930d864363971c5e4` | 0 |
| vendor/sphincsplus/sha2-avx2/fors.c | 8090 | `353c87a66fffa6f359d4f9d2a31dd15e70555d3867f54c3bab2e0b21862a3818` | 0 |
| vendor/sphincsplus/sha2-avx2/hash_sha2x8.c | 2538 | `5704865283ff2d1c1878386fd36e5b8ca330b3d7aa2406c1f39ff9da8a619d19` | 0 |
| vendor/sphincsplus/sha2-avx2/hashx8.h | 514 | `5c9cdaf7e2661649fa38f80325f9de8b46de43109f72e06d38c31ffac1aef5a2` | 0 |
| vendor/sphincsplus/sha2-avx2/merkle.c | 2115 | `19ba62b5739fe9826e515bb5fefb765033fac3004065da9f1725b669afb92ab0` | 0 |
| vendor/sphincsplus/sha2-avx2/sha256avx.c | 15421 | `dd4b332dc080704c3780613c2787f1ed6c3e1d7a639b8359d327fabeb47ac9d0` | 0 |
| vendor/sphincsplus/sha2-avx2/sha256avx.h | 3512 | `8dbc3fd1999628825d59a928dc5227c7c8cd651c9a86186d6470149fa62a8434` | 0 |
| vendor/sphincsplus/sha2-avx2/sha256x8.c | 7040 | `8089a3db6ea8006723f2610bab819b493da9ef32171788e52eab3d5419355f4c` | 0 |
| vendor/sphincsplus/sha2-avx2/sha256x8.h | 2465 | `de07bcfae3e394523be4a0a3a85c263bf458f34d354f76b3d589da5b34ca5c75` | 0 |
| vendor/sphincsplus/sha2-avx2/sha512x4.c | 15546 | `375663933e3d89c7d47ae0c13a01fb3468f1e5bae8ecd21b56e88049a00f63a9` | 0 |
| vendor/sphincsplus/sha2-avx2/sha512x4.h | 1137 | `84329a9a73a6207319897a1a44bab78a2cf77c38d14d370713f547f220c49797` | 0 |
| vendor/sphincsplus/sha2-avx2/thash_sha2_robustx8.c | 11408 | `fab3a98115416a2eea2d82e47e1dbbf3bf2ab412d6cc9a9b4bd563c2f6133e73` | 0 |
| vendor/sphincsplus/sha2-avx2/thash_sha2_simplex8.c | 8176 | `a4a3c7aa96dad3669f98c683e1daae9614fd7741237aa3ef2799cad5dc013128` | 0 |
| vendor/sphincsplus/sha2-avx2/thashx8.h | 817 | `731b861507fd7dc9dea1d77a6a1fff4f406a4e84d02ca4078e98a9bb7886d3c6` | 0 |
| vendor/sphincsplus/sha2-avx2/utilsx8.c | 6238 | `b6a3ff08f4d0029bf4ac2741581ac2f619e2accb13940e43fc75be5894b4caf4` | 0 |
| vendor/sphincsplus/sha2-avx2/utilsx8.h | 1084 | `55d8fa8004c3a2457f8a52ab8b7f0a5c59874cbaba99718edbb6b963c119f7b2` | 0 |
| vendor/sphincsplus/sha2-avx2/wots.c | 9351 | `0d4fcb08b4f1927233d1b9542ac98b7db0909b93fd05ae589eb61b58c4637ab9` | 0 |
| vendor/sphincsplus/sha2-avx2/wotsx8.h | 1307 | `5b59d3e8e6eb9a66a598c91746c1ee4216aef974e3d99449ff3513662d00fdf4` | 0 |
| vendor/sphincsplus/shake-a64/context.h | 180 | `69f3f1756e1ac7cbc9827e8a83aab74d1086e9f70f505c39e5687be3194a26d3` | 0 |
| vendor/sphincsplus/shake-a64/f1600x2.h | 212 | `55a55ff09c9e06979dadba873be952b9cfa17b1289449564dfeef19b3a404204` | 0 |
| vendor/sphincsplus/shake-a64/f1600x2_const.c | 557 | `3b3fde30ca2c99c95a0ff283a226999f97908fcae4fb07a84d19f2b01ef58a2e` | 0 |
| vendor/sphincsplus/shake-a64/fips202x2.c | 3478 | `969e7567bd9dbbd2a54cb0236cdcaf83250a38a2e11e886bdf066fd2476a68be` | 0 |
| vendor/sphincsplus/shake-a64/fips202x2.h | 624 | `052b5f75cf065183f4f9da0a9aeaac6f8421fa6763e50ab98698939877bea7a3` | 0 |
| vendor/sphincsplus/shake-a64/fors.c | 6478 | `4d8e3d02d8bf84b9f5c00beebcbb2e3ca35860bc148f1c4fe6b687dc0fef37a0` | 0 |
| vendor/sphincsplus/shake-a64/hash_shakex2.c | 1470 | `743694ba9c55e60a09d4d1d7717aecb497f4629ff3934f352b957ea1ebe4f9d1` | 0 |
| vendor/sphincsplus/shake-a64/hashx2.h | 313 | `6d8ebe3b64a907157b6c4f724bbb0f199ddc39f4c2e8184b4b870b7bd36667a2` | 0 |
| vendor/sphincsplus/shake-a64/merkle.c | 2027 | `00b3f44547c02321bee94f860610e9b49a3b28143dd14fa29e2f4755f133a797` | 0 |
| vendor/sphincsplus/shake-a64/thash.h | 236 | `1a5ccef8bd200dc96ef9bd0d48715d32e32d7efc009c3a372f44a3ab16afe629` | 0 |
| vendor/sphincsplus/shake-a64/thash_shake_robustx2.c | 4069 | `bd86c6382f5658fca4fe1920618157afde31068130890b6bd91cd75a5cf96660` | 0 |
| vendor/sphincsplus/shake-a64/thash_shake_simplex2.c | 2815 | `651fb558e944c6b8c2ab4fd352450e2aa6226b9d067ab784cf540af73b056f6f` | 0 |
| vendor/sphincsplus/shake-a64/thashx2.h | 392 | `4ad051f46e956ce0a3c648f4758d2e14893c06883ac5fd814118bde3e1d994fc` | 0 |
| vendor/sphincsplus/shake-a64/utilsx2.c | 5458 | `167806d1a38e34049bb67e7879a656336a11d188ac18a57bf7ef7038520d1261` | 0 |
| vendor/sphincsplus/shake-a64/utilsx2.h | 1085 | `637d21c0996c970a8e227de0746c716ff812a58a2fc321b3358a88299060250f` | 0 |
| vendor/sphincsplus/shake-a64/wots.c | 8017 | `f30ebe58a2205e7974415949288f284824ec5fdad0a82d27757aa7eb54e24940` | 0 |
| vendor/sphincsplus/shake-a64/wotsx2.h | 1307 | `19a5bff0c7c5365049aaf8d3e1383b58659a4c2b666202b155974814432484c6` | 0 |
| vendor/sphincsplus/shake-avx2/context.h | 180 | `69f3f1756e1ac7cbc9827e8a83aab74d1086e9f70f505c39e5687be3194a26d3` | 0 |
| vendor/sphincsplus/shake-avx2/fips202x4.c | 5440 | `ee5b05ad7d7d0a18707b5fec2b55e50ac4d9ed1e090fa80bc89e45fee05a390f` | 0 |
| vendor/sphincsplus/shake-avx2/fips202x4.h | 774 | `57bedbbd125434c43982b95df9e8af0dfb55f853489834366221f8abda7ba65b` | 0 |
| vendor/sphincsplus/shake-avx2/fors.c | 6998 | `6198284a87c362e3dc273773dc9aa0bce6f20cbd809b35cb92174cdbd1ac22e5` | 0 |
| vendor/sphincsplus/shake-avx2/hash_shakex4.c | 1981 | `c7e9d49cc93e323b70e7227cf60658a2607c179944b01ef61477c9983095002c` | 0 |
| vendor/sphincsplus/shake-avx2/hashx4.h | 387 | `c6223dcf0c544a31be67b602015dee3fe3ab8661a14454f6c91b1d90c3f94fba` | 0 |
| vendor/sphincsplus/shake-avx2/keccak4x/KeccakP-1600-times4-SIMD256.c | 40006 | `a29188e05c33050fd703657ca3f29f9db0478941e4d4864b4a3ca8dd8810810c` | 0 |
| vendor/sphincsplus/shake-avx2/keccak4x/KeccakP-1600-times4-SnP.h | 3114 | `82b498f8e116b736cd77e1d1665300aa75606b354e02a90cb764c28936c7c0cb` | 0 |
| vendor/sphincsplus/shake-avx2/keccak4x/SIMD256-config.h | 150 | `2118d0bf6aa447bae934789610f2b1b61c29ed28702d470a64dc6b0d522bdb28` | 0 |
| vendor/sphincsplus/shake-avx2/keccak4x/align.h | 939 | `5033313cf7203ce3514cc22d8ce113b430237e8b15a6c66a79d3ee8b5e3d80b5` | 0 |
| vendor/sphincsplus/shake-avx2/keccak4x/brg_endian.h | 5546 | `5fbc8e476a28827e0fb764db47b4e94947fd9138cd9f26fce114cbc1ee507aa9` | 0 |
| vendor/sphincsplus/shake-avx2/merkle.c | 2027 | `66fdf83d6fa3b316bc6978bbb0fadcfa748b60076f8f67bdd365ec747e30247f` | 0 |
| vendor/sphincsplus/shake-avx2/thash_shake_robustx4.c | 5199 | `456e9ef43296fd0bd11872d386545c685ed6f55407a26f3ef54b9cc563038bf1` | 0 |
| vendor/sphincsplus/shake-avx2/thash_shake_simplex4.c | 3746 | `3891e608296f0b0f4c83d0904d9ca990dd9ccb60229ab445fba3aa38f6887504` | 0 |
| vendor/sphincsplus/shake-avx2/thashx4.h | 525 | `6859c5e1dcdb090d7c3127ea0dc9289b9e0d75b061083c8dc08b17885ee3de2c` | 0 |
| vendor/sphincsplus/shake-avx2/utilsx4.c | 5872 | `7683265c603aa71ff4b2effb5774d370b41dfbdc3880e289d437257f6716a17f` | 0 |
| vendor/sphincsplus/shake-avx2/utilsx4.h | 1084 | `79ab80de197ce967266920d85779c94c42b38ceaf53be261ff0233a30b694fca` | 0 |
| vendor/sphincsplus/shake-avx2/wots.c | 8464 | `ff111f14558268b4a9fc165fa60dea3110e5ef4b5865387062271082d9a17a51` | 0 |
| vendor/sphincsplus/shake-avx2/wotsx4.h | 1306 | `97fa5f08ccfdabe4a249e24e36ecd49ff1997a91423d9bbe29a5d7a3f35956c5` | 0 |
| vendor/sphincsplus/vectors.py | 3270 | `799e1ead884a113139bdb169f6a589d2eafd8b9920cf5d2cf1167d27f1e80c04` | 0 |
