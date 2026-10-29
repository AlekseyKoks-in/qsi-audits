# Security & Post-Quantum Readiness Audit Report

**Project:** jade @ a59d14c2b397 · Blockstream (Jade) — public repository (passive review)
| | |
|---|---|
| Organization | QSI |
| Report date | 2026-10-28 21:17 UTC |
| Report version | 1 |
| Audit run | 633fed56-b826-4e1b-93cd-7d2ea40571e8 (Document audit) |
| Analyzer engine | qsi-engine 1.2.0 |
| Risk profile | Crypto exchange, custodian or wallet |
| Content SHA-256 | `7942ddb55815a12070642368e6e3ea6fc9c02c06f4bad7fe1df427ff83cae3e3` |
| Signature key (Ed25519, SHA-256 fingerprint; the signature is the separate file report.sig.json) | `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e` |
> This report presents automated and documented analysis results for the stated scope. It is not a legal opinion, a certification or an attestation of compliance with any standard.

## 1. Executive summary

- Critical: **0**
- High: **0**
- Medium: **7**
- Low: **0**
- Info: **1**

- Confirmed technical vulnerability: 0
- Known vulnerable component: 0
- Confirmed configuration error: 0
- Potential cryptographic risk: 0
- Long-term post-quantum risk: 7
- Improvement recommendation: 1
- Insufficient data: 0

Mosca's inequality (x + y > z): x = 10, y = 5, z = 8 → migration would finish too late under this scenario. _z is a planning assumption chosen per risk profile, not a prediction. A cryptographically relevant quantum computer is not publicly known to exist today._

**Post-quantum maturity: Level 0 of 4 — no post-quantum cryptography.** Next step: Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

## 2. Scope and boundaries

Mode: Document audit

Repository: <https://github.com/Blockstream/Jade> @ `a59d14c2b39715060e6721a309a7d49bedd3ee5b` — evidence links open the lines at this commit.

568 files, 10186070 bytes in total, 3 redaction(s); the per-file SHA-256 list is in appendix C.

## 3. Methodology

| Area | Status | Count | Examples |
|---|---|---|---|
| source_code | checked | 559 | components/assets/assets_snapshot.c: 47 lines scanned with 16 rule patterns and 122 registry patterns; components/assets/assets_snapshot.h: 19 lines scanned with 16 rule patterns and 122 registry patterns; components/assets/gen_assets.py: 86 lines scanned with 16 rule patterns and 122 registry patterns |
| certificates_and_keys | checked | 2 | components/libwally-core/upstream/SECURITY.md: certificates/keys parsed; components/libwally-core/upstream/src/secp256k1/src/wycheproof/ecdsa_secp256k1_sha256_bitcoin_test.json: certificates/keys parsed |
| dependencies | checked | 4 | components/libwally-core/upstream/contrib/requirements.txt: 7 dependencies parsed (0 pinned); components/libwally-core/upstream/pyproject.toml: 0 dependencies parsed (0 pinned); components/libwally-core/upstream/src/wasm_package/package-lock.json: 156 dependencies parsed (156 pinned) |
| keys | error (not checked) | 99 | components/libwally-core/upstream/src/secp256k1/src/wycheproof/ecdsa_secp256k1_sha256_bitcoin_test.json line 134: public key could not be parsed (ValueError); components/libwally-core/upstream/src/secp256k1/src/wycheproof/ecdsa_secp256k1_sha256_bitcoin_test.json line 3600: public key could not be parsed (ValueError); components/libwally-core/upstream/src/secp256k1/src/wycheproof/ecdsa_secp256k1_sha256_bitcoin_test.json line 3636: public key could not be parsed (ValueError) |
| secrets | checked | 3 | components/libwally-core/upstream/src/swig_python/contrib/aes.py: value(s) at line(s) 12 (test_aes_cbc_ecdh), 15 (test_aes_cbc_ecdh) are declared inside a fixture and treated as test data, although the file itself is not test code; components/libwally-core/upstream/src/swig_python/contrib/aes.py: 2 redacted value(s) not reported (comments, test modules, fixture declarations, placeholders, values the source annotates as published, or hex values not bound to a secret name); libjade/selfcheck/descriptor.c: 1 redacted value(s) not reported (comments, test modules, fixture declarations, placeholders, values the source annotates as published, or hex values not bound to a secret name) |
| osv_advisories | checked | 1 | 156 pinned packages queried at OSV.dev; 5 affected (5 of them only in development or build dependencies) |

_Long lists are grouped here; the full per-file list is in the JSON report, signed with the same key._

## 4. Assets examined and not examined

- keys — error (not checked): 99 (examples: components/libwally-core/upstream/src/secp256k1/src/wycheproof/ecdsa_secp256k1_sha256_bitcoin_test.json line 134: public key could not be parsed (ValueError); components/libwally-core/upstream/src/secp256k1/src/wycheproof/ecdsa_secp256k1_sha256_bitcoin_test.json line 3600: public key could not be parsed (ValueError); components/libwally-core/upstream/src/secp256k1/src/wycheproof/ecdsa_secp256k1_sha256_bitcoin_test.json line 3636: public key could not be parsed (ValueError))

## 5. Architecture overview

Static review of the source tree jade at a59d14c2b39715060e6721a309a7d49bedd3ee5b. 568 files analysed; of 965 files, 159 are test, fuzzing, benchmark or example code and were left out, 238 are not read by any analyzer, 0 exceed the per-file limit and 0 did not fit the total limit. No requests were sent to the owner's systems.

## 6. Overall security posture

- Indicative posture index: **100** / 100 — _Derived from findings in scope (confirmed and potential issues weighted by severity). Indicative only; not comparable across differently scoped audits._
- Quantum-vulnerable share of inventory: 71.0%

## 7. Detailed findings

### QSI-2026-06120 — Quantum-vulnerable RSA key (4096-bit) in components/libwally-core/upstream/SECURITY.md

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: High
- Affected asset: `file:components/libwally-core/upstream/SECURITY.md#line 52`
- Data source: components/libwally-core/upstream/SECURITY.md
- Detection method: Public key parsing.
- Analyzer: certificates 1.2.0 · 2026-10-28 21:17 UTC
- Priority score: 50.3 / 100
- CVSS v3.1: not applicable

A RSA 4096-bit public key was found (line 52).

**Potential impact.** Long-term risk once a CRQC exists; for key exchange, recorded traffic could be decrypted retroactively.

**Reproduction steps.**

```
Open line 52 in the supplied file components/libwally-core/upstream/SECURITY.md and inspect the quoted lines (see evidence).
```

**Evidence.**

_key · components/libwally-core/upstream/SECURITY.md · line 52 · SHA-256 18fb5f0b9bd19412cb5c0404d29bd26dc62ba6e0ff99543463ebc0757b50ef09_

```
OpenPGP primary key: algorithm ID 1 (RSA) 4096-bit
```

_key · components/libwally-core/upstream/SECURITY.md · line 52 · SHA-256 484f2172c4dd53b29fd23e321304b308266950550fb37c83431470e8045649f0_

```
OpenPGP subkey: algorithm ID 1 (RSA) 4096-bit
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability.

**Recommendation.** Inventory and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it..

**Retest procedure.** Re-audit after migration.

### QSI-2026-06121 — Quantum-vulnerable ECDSA: transaction and message signing (40 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:ECDSA:transaction_signing`
- Data source: components/libwally-core/upstream/setup.py
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.2.0 · 2026-10-28 21:17 UTC
- Priority score: 35.6 / 100
- CVSS v3.1: not applicable

146 reference(s) to ECDSA across 40 file(s), e.g. components/libwally-core/upstream/setup.py:58. Role, judged from paths, function names and nearby code: transaction and message signing. A CRQC derives the private key from a public key that is already known (on chain after the first spend, in reused addresses): funds and approvals controlled by these keys need a migration path.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open components/libwally-core/upstream/setup.py:58 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [components/libwally-core/upstream/setup.py](https://github.com/Blockstream/Jade/blob/a59d14c2b39715060e6721a309a7d49bedd3ee5b/components/libwally-core/upstream/setup.py#L58) · line 58 · SHA-256 faf6a0cba5f30b003359e096b202e6312b83d259b06c8c18493fc02a13b16467_

```
   57 | 
   58 | if (USE_LIB == 'no' or not PKG_SECP256K1) and not os.path.exists('src/secp256k1/Makefile.am'):
   59 |     # Sync libsecp256k1-zkp (only if needed)
```

_file_excerpt · [components/libwally-core/upstream/setup.py](https://github.com/Blockstream/Jade/blob/a59d14c2b39715060e6721a309a7d49bedd3ee5b/components/libwally-core/upstream/setup.py#L75) · line 75 · SHA-256 07224e44121568888046b6db0a64d8c77d33d1715e2c4c0e03b44ebbcca10b36_

```
   74 | if PKG_SECP256K1:
   75 |     CONFIGURE_ARGS += ['--with-system-secp256k1=' + PKG_SECP256K1]
   76 | 
```

_file_excerpt · [components/libwally-core/upstream/setup.py](https://github.com/Blockstream/Jade/blob/a59d14c2b39715060e6721a309a7d49bedd3ee5b/components/libwally-core/upstream/setup.py#L132) · line 132 · SHA-256 790764e66fa46e6f76061b300ae744943186e2a604de2f62962c3fae53c69b3b_

```
  131 |         './src/ccan',
  132 |         './src/secp256k1/include',
  133 |     ]
```

_file_excerpt · [components/libwally-core/upstream/src/anti_exfil.c](https://github.com/Blockstream/Jade/blob/a59d14c2b39715060e6721a309a7d49bedd3ee5b/components/libwally-core/upstream/src/anti_exfil.c#L72) · line 72 · SHA-256 38a6257c59bd1576fcad77de26a0b8b07e8d637f0457829ebd386222ffc20554_

```
   71 | {
   72 |     secp256k1_ecdsa_signature sig_secp;
   73 |     const secp256k1_context *ctx = secp_ctx();
```

_file_excerpt · [components/libwally-core/upstream/src/anti_exfil.c](https://github.com/Blockstream/Jade/blob/a59d14c2b39715060e6721a309a7d49bedd3ee5b/components/libwally-core/upstream/src/anti_exfil.c#L87) · line 87 · SHA-256 9213bc4125f159f48bc6b0e8d7906dc826e6431c9b90cc8d1e9b98c342c9ee10_

```
   86 |     ok = secp256k1_anti_exfil_sign(ctx, &sig_secp, bytes, priv_key, entropy) &&
   87 |          secp256k1_ecdsa_signature_serialize_compact(ctx, bytes_out, &sig_secp);
   88 | 
```

_file_excerpt · [components/libwally-core/upstream/src/anti_exfil.c](https://github.com/Blockstream/Jade/blob/a59d14c2b39715060e6721a309a7d49bedd3ee5b/components/libwally-core/upstream/src/anti_exfil.c#L107) · line 107 · SHA-256 ccc27036c049ec2fe55b8cab5992c66b4834971552c32740b52ae96fbe16eecd_

```
  106 |     secp256k1_pubkey pub_secp;
  107 |     secp256k1_ecdsa_signature sig_secp;
  108 |     secp256k1_ecdsa_s2c_opening opening_secp;
```

_file_excerpt · [components/libwally-core/upstream/src/secp256k1/contrib/lax_der_parsing.c](https://github.com/Blockstream/Jade/blob/a59d14c2b39715060e6721a309a7d49bedd3ee5b/components/libwally-core/upstream/src/secp256k1/contrib/lax_der_parsing.c#L11) · line 11 · SHA-256 9197354c850cb53bbc475b348c0f97bb3f550706fcced8bf483336d626575330_

```
   10 | 
   11 | int ecdsa_signature_parse_der_lax(const secp256k1_context* ctx, secp256k1_ecdsa_signature* sig, const unsigned char *input, size_t inputlen) {
   12 |     size_t rpos, rlen, spos, slen;
```

_file_excerpt · [components/libwally-core/upstream/src/secp256k1/contrib/lax_der_parsing.c](https://github.com/Blockstream/Jade/blob/a59d14c2b39715060e6721a309a7d49bedd3ee5b/components/libwally-core/upstream/src/secp256k1/contrib/lax_der_parsing.c#L19) · line 19 · SHA-256 234aeaaf6b28e1d2ff43854e60a3119e3c3f55229e18841e2dc766404eab65d0_

```
   18 |     /* Hack to initialize sig with a correctly-parsed but invalid signature. */
   19 |     secp256k1_ecdsa_signature_parse_compact(ctx, sig, tmpsig);
   20 | 
```

_file_excerpt · [components/libwally-core/upstream/src/secp256k1/contrib/lax_der_parsing.c](https://github.com/Blockstream/Jade/blob/a59d14c2b39715060e6721a309a7d49bedd3ee5b/components/libwally-core/upstream/src/secp256k1/contrib/lax_der_parsing.c#L140) · line 140 · SHA-256 75ad5d0cba25ca64adb6d971da937879704b4abc8845c17dc1da9fa1eb773e5e_

```
  139 |     if (!overflow) {
  140 |         overflow = !secp256k1_ecdsa_signature_parse_compact(ctx, sig, tmpsig);
  141 |     }
```

_file_excerpt · [components/libwally-core/upstream/src/secp256k1/contrib/lax_der_parsing.h](https://github.com/Blockstream/Jade/blob/a59d14c2b39715060e6721a309a7d49bedd3ee5b/components/libwally-core/upstream/src/secp256k1/contrib/lax_der_parsing.h#L57) · line 57 · SHA-256 25af7e242d92af0d3c46ae8d8a48030e247c4bfdeba65068030e64eb4c88c912_

```
   56 |    files (such as tests.c) without the need to set an explicit -I flag,
   57 |    which would be necessary to locate secp256k1.h. */
   58 | #ifndef SECP256K1_H
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains adopt them.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-06123 — Quantum-vulnerable Schnorr (BIP-340): transaction and message signing (6 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:Schnorr (BIP-340):transaction_signing`
- Data source: components/libwally-core/upstream/src/secp256k1/include/secp256k1_schnorrsig.h
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.2.0 · 2026-10-28 21:17 UTC
- Priority score: 35.6 / 100
- CVSS v3.1: not applicable

37 reference(s) to Schnorr (BIP-340) across 6 file(s), e.g. components/libwally-core/upstream/src/secp256k1/include/secp256k1_schnorrsig.h:82. Role, judged from paths, function names and nearby code: transaction and message signing. A CRQC derives the private key from a public key that is already known (on chain after the first spend, in reused addresses): funds and approvals controlled by these keys need a migration path.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open components/libwally-core/upstream/src/secp256k1/include/secp256k1_schnorrsig.h:82 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [components/libwally-core/upstream/src/secp256k1/include/secp256k1_schnorrsig.h](https://github.com/Blockstream/Jade/blob/a59d14c2b39715060e6721a309a7d49bedd3ee5b/components/libwally-core/upstream/src/secp256k1/include/secp256k1_schnorrsig.h#L82) · line 82 · SHA-256 6aae3b20f8f8b503597acb97fe491246b6777b5a9660b8a41542605d18aab6f4_

```
   81 |  */
   82 | typedef struct secp256k1_schnorrsig_extraparams {
   83 |     unsigned char magic[4];
```

_file_excerpt · [components/libwally-core/upstream/src/secp256k1/include/secp256k1_schnorrsig.h](https://github.com/Blockstream/Jade/blob/a59d14c2b39715060e6721a309a7d49bedd3ee5b/components/libwally-core/upstream/src/secp256k1/include/secp256k1_schnorrsig.h#L86) · line 86 · SHA-256 43d5f6045ac4e6b23daf11fd6c10022dca16ca76afd775c3ee898ddbef44d5bd_

```
   85 |     void *ndata;
   86 | } secp256k1_schnorrsig_extraparams;
   87 | 
```

_file_excerpt · [components/libwally-core/upstream/src/secp256k1/include/secp256k1_schnorrsig.h](https://github.com/Blockstream/Jade/blob/a59d14c2b39715060e6721a309a7d49bedd3ee5b/components/libwally-core/upstream/src/secp256k1/include/secp256k1_schnorrsig.h#L119) · line 119 · SHA-256 1e555d327421285c8a81345e58876f5f2f017571adb2f2168aafc7c44770594c_

```
  118 |  */
  119 | SECP256K1_API int secp256k1_schnorrsig_sign32(
  120 |     const secp256k1_context *ctx,
```

_file_excerpt · [components/libwally-core/upstream/src/secp256k1/include/secp256k1_schnorrsig_halfagg.h](https://github.com/Blockstream/Jade/blob/a59d14c2b39715060e6721a309a7d49bedd3ee5b/components/libwally-core/upstream/src/secp256k1/include/secp256k1_schnorrsig_halfagg.h#L43) · line 43 · SHA-256 b3d54ae6f144846b9769cfe141d006f33bf49fa9572bafb7307c2ade17fd95eb_

```
   42 |  */
   43 | SECP256K1_API int secp256k1_schnorrsig_inc_aggregate(
   44 |     const secp256k1_context *ctx,
```

_file_excerpt · [components/libwally-core/upstream/src/secp256k1/include/secp256k1_schnorrsig_halfagg.h](https://github.com/Blockstream/Jade/blob/a59d14c2b39715060e6721a309a7d49bedd3ee5b/components/libwally-core/upstream/src/secp256k1/include/secp256k1_schnorrsig_halfagg.h#L70) · line 70 · SHA-256 be378be4953e3b3d2e2b5a4ddab26874bc43e6f72392495b730cac093c057a7a_

```
   69 |  */
   70 | SECP256K1_API int secp256k1_schnorrsig_aggregate(
   71 |     const secp256k1_context *ctx,
```

_file_excerpt · [components/libwally-core/upstream/src/secp256k1/include/secp256k1_schnorrsig_halfagg.h](https://github.com/Blockstream/Jade/blob/a59d14c2b39715060e6721a309a7d49bedd3ee5b/components/libwally-core/upstream/src/secp256k1/include/secp256k1_schnorrsig_halfagg.h#L94) · line 94 · SHA-256 b10de912dd2b9f3e510c8fe909f0b6db3a25cde95edbbe0af55b109a33026fce_

```
   93 |  */
   94 | SECP256K1_API SECP256K1_WARN_UNUSED_RESULT int secp256k1_schnorrsig_aggverify(
   95 |     const secp256k1_context *ctx,
```

_file_excerpt · [components/libwally-core/upstream/src/secp256k1/src/modules/musig/session_impl.h](https://github.com/Blockstream/Jade/blob/a59d14c2b39715060e6721a309a7d49bedd3ee5b/components/libwally-core/upstream/src/secp256k1/src/modules/musig/session_impl.h#L621) · line 621 · SHA-256 6254128e9a575e14bb87c68d5f2f12d65a6084dd7de58385e4a2764f96f3935a_

```
  620 |     secp256k1_musig_nonce_process_internal(ctx, &session_i.fin_nonce_parity, fin_nonce, &session_i.noncecoef, aggnonce_pts, agg_pk32, msg32);
  621 |     secp256k1_schnorrsig_challenge(secp256k1_get_hash_context(ctx), &session_i.challenge, fin_nonce, msg32, 32, agg_pk32);
  622 | 
```

_file_excerpt · [components/libwally-core/upstream/src/secp256k1/src/modules/schnorrsig/bench_impl.h](https://github.com/Blockstream/Jade/blob/a59d14c2b39715060e6721a309a7d49bedd3ee5b/components/libwally-core/upstream/src/secp256k1/src/modules/schnorrsig/bench_impl.h#L33) · line 33 · SHA-256 fc2c5559f32fc9bd9a85efef59a46eaf722b1b8e2745b837696cdf6a6c00259e_

```
   32 |         msg[1] = i >> 8;
   33 |         CHECK(secp256k1_schnorrsig_sign_custom(data->ctx, sig, msg, MSGLEN, data->keypairs[i], NULL));
   34 |     }
```

_file_excerpt · [components/libwally-core/upstream/src/secp256k1/src/modules/schnorrsig/bench_impl.h](https://github.com/Blockstream/Jade/blob/a59d14c2b39715060e6721a309a7d49bedd3ee5b/components/libwally-core/upstream/src/secp256k1/src/modules/schnorrsig/bench_impl.h#L44) · line 44 · SHA-256 4f2e9b7b2529431d8190d606bbe0ce49659d6e5a1e0410625d931eacdcd05a06_

```
   43 |         CHECK(secp256k1_xonly_pubkey_parse(data->ctx, &pk, data->pk[i]) == 1);
   44 |         CHECK(secp256k1_schnorrsig_verify(data->ctx, data->sigs[i], data->msgs[i], MSGLEN, &pk));
   45 |     }
```

_file_excerpt · [components/libwally-core/upstream/src/secp256k1/src/modules/schnorrsig/bench_impl.h](https://github.com/Blockstream/Jade/blob/a59d14c2b39715060e6721a309a7d49bedd3ee5b/components/libwally-core/upstream/src/secp256k1/src/modules/schnorrsig/bench_impl.h#L80) · line 80 · SHA-256 0ca8c9b51520014576b4c622e33014e8b93cc7c4bd0bc826e9cd4563a3642698_

```
   79 |         CHECK(secp256k1_keypair_create(data.ctx, keypair, sk));
   80 |         CHECK(secp256k1_schnorrsig_sign_custom(data.ctx, sig, msg, MSGLEN, keypair, NULL));
   81 |         CHECK(secp256k1_keypair_xonly_pub(data.ctx, &pk, NULL, keypair));
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains adopt them.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-06122 — Quantum-vulnerable ECDSA: role not determined (2 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:ECDSA:general`
- Data source: components/libwally-core/upstream/src/amalgamation/combined.c
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.2.0 · 2026-10-28 21:17 UTC
- Priority score: 34.2 / 100
- CVSS v3.1: not applicable

4 reference(s) to ECDSA across 2 file(s), e.g. components/libwally-core/upstream/src/amalgamation/combined.c:34. Role, judged from paths, function names and nearby code: role not determined. The code does not show what the keys protect; review decides the priority.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open components/libwally-core/upstream/src/amalgamation/combined.c:34 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [components/libwally-core/upstream/src/amalgamation/combined.c](https://github.com/Blockstream/Jade/blob/a59d14c2b39715060e6721a309a7d49bedd3ee5b/components/libwally-core/upstream/src/amalgamation/combined.c#L34) · line 34 · SHA-256 8cce795a23b61e665185923e4058d56ed7e106c55784ee042d2a237e9547756d_

```
   33 | #endif
   34 | #include "src/secp256k1/src/secp256k1.c"
   35 | #include "src/secp256k1/src/precomputed_ecmult_gen.c"
```

_file_excerpt · [components/libwally-core/upstream/src/amalgamation/combined.c](https://github.com/Blockstream/Jade/blob/a59d14c2b39715060e6721a309a7d49bedd3ee5b/components/libwally-core/upstream/src/amalgamation/combined.c#L35) · line 35 · SHA-256 b0ba42431dd53977e931a49f059369c0a07f7bb7b7924b65b78a0d467021b948_

```
   34 | #include "src/secp256k1/src/secp256k1.c"
   35 | #include "src/secp256k1/src/precomputed_ecmult_gen.c"
   36 | #include "src/secp256k1/src/precomputed_ecmult.c"
```

_file_excerpt · [components/libwally-core/upstream/src/amalgamation/combined.c](https://github.com/Blockstream/Jade/blob/a59d14c2b39715060e6721a309a7d49bedd3ee5b/components/libwally-core/upstream/src/amalgamation/combined.c#L36) · line 36 · SHA-256 9f2414696e322db70b097fe19907ea2f68a74d7db34037aad03b8dd534091072_

```
   35 | #include "src/secp256k1/src/precomputed_ecmult_gen.c"
   36 | #include "src/secp256k1/src/precomputed_ecmult.c"
   37 | 
```

_file_excerpt · [components/libwally-core/upstream/src/internal.h](https://github.com/Blockstream/Jade/blob/a59d14c2b39715060e6721a309a7d49bedd3ee5b/components/libwally-core/upstream/src/internal.h#L33) · line 33 · SHA-256 a3cf3e2c758ea293394dc165dc129bd87d56cac6ce0aa935b84a4eee6ffc8113_

```
   32 | 
   33 | #include <secp256k1.h>
   34 | #include <secp256k1_recovery.h>
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it; introduce an abstraction layer for crypto-agility.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-06124 — Quantum-vulnerable ECDH: role not determined (1 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:ECDH:general`
- Data source: components/libwally-core/upstream/src/secp256k1/src/bench.c
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.2.0 · 2026-10-28 21:17 UTC
- Priority score: 34.2 / 100
- CVSS v3.1: not applicable

4 reference(s) to ECDH across 1 file(s), e.g. components/libwally-core/upstream/src/secp256k1/src/bench.c:24. Role, judged from paths, function names and nearby code: role not determined. The code does not show what the keys protect; review decides the priority.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open components/libwally-core/upstream/src/secp256k1/src/bench.c:24 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [components/libwally-core/upstream/src/secp256k1/src/bench.c](https://github.com/Blockstream/Jade/blob/a59d14c2b39715060e6721a309a7d49bedd3ee5b/components/libwally-core/upstream/src/secp256k1/src/bench.c#L24) · line 24 · SHA-256 6ec91ca104f465f4b861193bee0ed1f6d91c4074fb5085511ca06c7dd6747616_

```
   23 | #ifdef ENABLE_MODULE_ECDH
   24 |     printf("    - ECDH key exchange (optional module)\n");
   25 | #endif
```

_file_excerpt · [components/libwally-core/upstream/src/secp256k1/src/bench.c](https://github.com/Blockstream/Jade/blob/a59d14c2b39715060e6721a309a7d49bedd3ee5b/components/libwally-core/upstream/src/secp256k1/src/bench.c#L54) · line 54 · SHA-256 b21ecd8d53157d4f920477f57713fa34b7fe6379df61daa64f27e4a77f9133e1_

```
   53 | #ifdef ENABLE_MODULE_ECDH
   54 |     printf("    ecdh              : ECDH key exchange algorithm\n");
   55 | #endif
```

_file_excerpt · [components/libwally-core/upstream/src/secp256k1/src/bench.c](https://github.com/Blockstream/Jade/blob/a59d14c2b39715060e6721a309a7d49bedd3ee5b/components/libwally-core/upstream/src/secp256k1/src/bench.c#L68) · line 68 · SHA-256 ae7392892e7a0840c3596f3442ca87927d89cc694ec91267d2a73193091dac83_

```
   67 |     printf("    ellswift_keygen   : ElligatorSwift key generation\n");
   68 |     printf("    ellswift_ecdh     : ECDH on ElligatorSwift keys\n");
   69 | #endif
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Classify each usage, record data lifetimes, and plan migration to Hybrid key establishment with ML-KEM (FIPS 203), e.g. X25519MLKEM768 in TLS 1.3 or mlkem768x25519-sha256 in SSH; introduce an abstraction layer for crypto-agility.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-06125 — Quantum-vulnerable Schnorr (BIP-340): role not determined (1 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:Schnorr (BIP-340):general`
- Data source: components/libwally-core/upstream/src/sign.c
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.2.0 · 2026-10-28 21:17 UTC
- Priority score: 34.2 / 100
- CVSS v3.1: not applicable

2 reference(s) to Schnorr (BIP-340) across 1 file(s), e.g. components/libwally-core/upstream/src/sign.c:387. Role, judged from paths, function names and nearby code: role not determined. The code does not show what the keys protect; review decides the priority.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open components/libwally-core/upstream/src/sign.c:387 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [components/libwally-core/upstream/src/sign.c](https://github.com/Blockstream/Jade/blob/a59d14c2b39715060e6721a309a7d49bedd3ee5b/components/libwally-core/upstream/src/sign.c#L387) · line 387 · SHA-256 b957a7949930facdb75237e2e6c12333acd87496052f7b47d028be3337f21aa3_

```
  386 |             ret = WALLY_EINVAL;
  387 |         else if (!secp256k1_schnorrsig_sign32(ctx, bytes_out, bytes, &keypair, aux_rand))
  388 |             ret = WALLY_ERROR;
```

_file_excerpt · [components/libwally-core/upstream/src/sign.c](https://github.com/Blockstream/Jade/blob/a59d14c2b39715060e6721a309a7d49bedd3ee5b/components/libwally-core/upstream/src/sign.c#L456) · line 456 · SHA-256 b2cc452c48e864fed16b916f1e68559e9d63deec6656b7f76f35916d3cb585af_

```
  455 |         ok = xpubkey_parse(&xonly_pub, pub_key, pub_key_len);
  456 |         ok = ok && secp256k1_schnorrsig_verify(ctx, sig, bytes, bytes_len, &xonly_pub);
  457 |         wally_clear(&xonly_pub, sizeof(xonly_pub));
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Classify each usage, record data lifetimes, and plan migration to a post-quantum algorithm; introduce an abstraction layer for crypto-agility.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-06126 — Quantum-vulnerable ECDSA: authentication and identity (certificates, tokens, device attestation) (1 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:ECDSA:authentication`
- Data source: main/identity.c
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.2.0 · 2026-10-28 21:17 UTC
- Priority score: 34.2 / 100
- CVSS v3.1: not applicable

3 reference(s) to ECDSA across 1 file(s), e.g. main/identity.c:251. Role, judged from paths, function names and nearby code: authentication and identity (certificates, tokens, device attestation). Short-lived authentication stays safe until a CRQC exists; long-lived identities (device attestation, CA and SSH keys) need a plan earlier.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open main/identity.c:251 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [main/identity.c](https://github.com/Blockstream/Jade/blob/a59d14c2b39715060e6721a309a7d49bedd3ee5b/main/identity.c#L251) · line 251 · SHA-256 e4f065671df536c8ac1aa4a99bc178b3d17ff42fa11fb09a36df34b5991b1488_

```
  250 |     // Use RFC6979 deterministic signatures
  251 |     const int ret = mbedtls_ecdsa_sign_det_ext(&keypair->MBEDTLS_PRIVATE(grp), pr, ps, &keypair->MBEDTLS_PRIVATE(d),
  252 |         challenge, challenge_len, MBEDTLS_MD_SHA256, random_mbedtls_cb, NULL);
```

_file_excerpt · [main/identity.c](https://github.com/Blockstream/Jade/blob/a59d14c2b39715060e6721a309a7d49bedd3ee5b/main/identity.c#L254) · line 254 · SHA-256 35d28b1ee44fa915a5b1e3e193e36c19d55df56f5841f6b478e1cec3dd5462bd_

```
  253 |     if (ret) {
  254 |         JADE_LOGE("mbedtls_ecdsa_sign_det_ext() failed, returned %d", ret);
  255 |         return false;
```

_file_excerpt · [main/identity.c](https://github.com/Blockstream/Jade/blob/a59d14c2b39715060e6721a309a7d49bedd3ee5b/main/identity.c#L275) · line 275 · SHA-256 039845d8802aeee967d9d03901cae13aa3efd9a0f0f29b8a4fa00132006a4ce5_

```
  274 |     // Sanity check
  275 |     JADE_ZERO_VERIFY(mbedtls_ecdsa_verify(
  276 |         &keypair->MBEDTLS_PRIVATE(grp), challenge, challenge_len, &keypair->MBEDTLS_PRIVATE(Q), pr, ps));
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Keep credentials short-lived and plan ML-DSA certificates, tokens and keys as the ecosystem supports them.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-06127 — 15 advisories in 5 development or build-only npm package(s)

- Severity: **Info** · Classification: Improvement recommendation · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `dependencies:npm:non-runtime`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch lookup of exact versions; scope from devDependencies, package-lock.json dev flags, pnpm importers sections, the Cargo.lock graph rooted at the Cargo.toml tables, and — for yarn.lock, which records no scope — the lock graph walked from package.json. Where a runtime requirement cannot be resolved in a lock, that lock is left unclassified rather than risking a package being set aside wrongly.
- Analyzer: dependencies 1.2.0 · 2026-10-28 21:17 UTC
- Priority score: 15.5 / 100
- CVSS v3.1: not applicable

OSV.dev lists 15 advisories (8 rated high or critical) for 5 npm package(s) that only development or build tooling pulls in (components/libwally-core/upstream/src/wasm_package/package-lock.json): e.g. ajv@8.17.1 [dev]: GHSA-2g4f-4pwh-qvx6; baseline-browser-mapping@2.9.19 [dev]: GHSA-w5vr-8v7q-w6rv; browserslist@4.28.1 [dev]: GHSA-73wf-gq98-2v4g, GHSA-c83g-rgw3-j3cx; cross-spawn@7.0.3 [dev]: GHSA-3xgq-45jj-v275; fast-uri@3.1.5 [dev]: GHSA-333x-w4r6-6crp, GHSA-5jgf-p345-68v8, GHSA-f65p-4m7j-42xc, GHSA-fph4-wmhf-6fwf, GHSA-hrr3-gc8f-f4qj, GHSA-jqff-g426-hqxp, GHSA-qw65-cvwx-89v3, GHSA-w74x-v6f9-j3xg, GHSA-wjr9-j795-jxcr, GHSA-xhq7-xmqj-769h. The manifests mark them as such (devDependencies, "dev": true in package-lock.json, pnpm importers sections, [dev-dependencies]/[build-dependencies] reached through Cargo.lock, or — for yarn.lock, which records no scope at all — package.json reached through the lock graph), so they are not part of what ships.

**Potential impact.** They do not reach users of the product. They can affect developer machines and CI (supply chain): a compromised or vulnerable tool can tamper with builds.

**Reproduction steps.**

```
Look the packages listed in the evidence up at https://osv.dev and check their scope in components/libwally-core/upstream/src/wasm_package/package-lock.json.
```

**Evidence.**

_tool_output · [OSV.dev (npm)](https://osv.dev/) · components/libwally-core/upstream/src/wasm_package/package-lock.json · SHA-256 33de8bddd802999eabbfb4e4b5e3ecf4a6765d989bd5c6b7e1fbc9284468c9fa_

```
ajv@8.17.1 [dev]: GHSA-2g4f-4pwh-qvx6
baseline-browser-mapping@2.9.19 [dev]: GHSA-w5vr-8v7q-w6rv
browserslist@4.28.1 [dev]: GHSA-73wf-gq98-2v4g, GHSA-c83g-rgw3-j3cx
cross-spawn@7.0.3 [dev]: GHSA-3xgq-45jj-v275
fast-uri@3.1.5 [dev]: GHSA-333x-w4r6-6crp, GHSA-5jgf-p345-68v8, GHSA-f65p-4m7j-42xc, GHSA-fph4-wmhf-6fwf, GHSA-hrr3-gc8f-f4qj, GHSA-jqff-g426-hqxp, GHSA-qw65-cvwx-89v3, GHSA-w74x-v6f9-j3xg, GHSA-wjr9-j795-jxcr, GHSA-xhq7-xmqj-769h
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Scopes come from the manifests; a registry crate's own build dependencies cannot be told apart in Cargo.lock, so the runtime set may be larger than reality, never smaller.

**Recommendation.** Update the tooling during routine maintenance; prioritise packages that run in CI with secrets or that produce release artefacts.

**Retest procedure.** Re-run the dependency scan after updating.


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
| **transaction and message signing** | ECDSA (40), Schnorr (BIP-340) (6) | QSI-2026-06121, QSI-2026-06123 | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains adopt them |
| **authentication and identity (certificates, tokens, device attestation)** | ECDSA (1) | QSI-2026-06126 | Keep credentials short-lived and plan ML-DSA certificates, tokens and keys as the ecosystem supports them |
| **role not determined** | ECDSA (2), ECDH (1), Schnorr (BIP-340) (1) | QSI-2026-06122, QSI-2026-06124, QSI-2026-06125 | Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it; introduce an abstraction layer for crypto-agility |

_Roles are judged from file paths, function names and the code around each match; review confirms them. Root-of-trust keys and wrapped keys come first: they are hard to replace or can be recorded today._
No readiness questionnaire was completed for this project.

### Quantum algorithms relevant to this inventory

| Quantum algorithm | Effect | Attack model | Inventoried algorithms (rows) | What it means for this audit |
|---|---|---|---|---|
| Shor's algorithm — factoring | breaks | Q1 | RSA (4) | Breaks RSA at every key length: a longer modulus only raises the cost polynomially. Plan migration to ML-KEM (or a hybrid) for key establishment and ML-DSA / SLH-DSA for signatures; start with keys protecting data that must stay confidential for years (harvest now, decrypt later) and with long-lived signatures. |
| Shor's algorithm — elliptic-curve discrete logarithms | breaks | Q1 | ECDH (3), ECDSA (52), Schnorr (BIP-340) (7) | Elliptic-curve keys are expected to fall before RSA keys of comparable classical strength. On blockchains, coins whose public key is already on chain (reused addresses, pay-to-public-key and Taproot outputs) are exposed first; plan the move to post-quantum signatures and avoid key reuse in the meantime. |
| Grover's algorithm — key search and preimages | weakens (larger keys restore the margin) | Q1 | HMAC (9), PBKDF2 (1), RIPEMD-160 (2), SHA-2 (8), SHAKE (2), scrypt (5) | Not a break. 256-bit keys (AES-256, ChaCha20) keep a comfortable margin; AES-128 meets NIST category 1, while some authorities ask for 256-bit keys in quantum-resistant contexts (see the AES-128 entry). Prefer 256-bit keys for long-lived data; 256-bit hashes need no change for preimage resistance. |
| Brassard–Høyer–Tapp — collision search | weakens (larger keys restore the margin) | Q1 | RIPEMD-160 (2), SHA-2 (8), SHAKE (2) | 256-bit hashes (SHA-256, SHA3-256) remain adequate for collision resistance; 160-bit hashes are already weak classically (SHA-1 collisions are practical). Use 384/512-bit hashes where NIST categories 4–5 are required. |

_Effects: breaks — replace the algorithm; weakens — larger keys or outputs restore the margin; included in standard parameters — no action at standard parameter sets; only with superposition queries — not applicable to ordinary deployments._


## 9. Limitations and assumptions

- This report presents automated and documented analysis results for the stated scope. It is not a legal opinion, a certification or an attestation of compliance with any standard.
- z is a planning assumption chosen per risk profile, not a prediction. A cryptographically relevant quantum computer is not publicly known to exist today.
- keys: 99 (examples: components/libwally-core/upstream/src/secp256k1/src/wycheproof/ecdsa_secp256k1_sha256_bitcoin_test.json line 134: public key could not be parsed (ValueError); components/libwally-core/upstream/src/secp256k1/src/wycheproof/ecdsa_secp256k1_sha256_bitcoin_test.json line 3600: public key could not be parsed (ValueError); components/libwally-core/upstream/src/secp256k1/src/wycheproof/ecdsa_secp256k1_sha256_bitcoin_test.json line 3636: public key could not be parsed (ValueError))

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
| P3 | QSI-2026-06120 | Add RSA usages at file:components/libwally-core/upstream/SECURITY.md to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-06121 | Add ECDSA usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-06123 | Add Schnorr (BIP-340) usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-06122 | Add ECDSA usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-06124 | Add ECDH usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-06125 | Add Schnorr (BIP-340) usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-06126 | Add ECDSA usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P4 | QSI-2026-06120 | Plan migration of RSA to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. or a hybrid scheme in use. |
| P4 | QSI-2026-06121 | Plan migration of ECDSA to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-06123 | Plan migration of Schnorr (BIP-340) to  (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows  or a hybrid scheme in use. |
| P4 | QSI-2026-06122 | Plan migration of ECDSA to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-06124 | Plan migration of ECDH to Hybrid key establishment with ML-KEM (FIPS 203), e.g. X25519MLKEM768 in TLS 1.3 or mlkem768x25519-sha256 in SSH (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows Hybrid key establishment with ML-KEM (FIPS 203), e.g. X25519MLKEM768 in TLS 1.3 or mlkem768x25519-sha256 in SSH or a hybrid scheme in use. |
| P4 | QSI-2026-06125 | Plan migration of Schnorr (BIP-340) to  (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows  or a hybrid scheme in use. |
| P4 | QSI-2026-06126 | Plan migration of ECDSA to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-06127 | Update the development and build dependencies listed in the evidence. | root-cause fix | The dependency scan reports no advisories for tooling packages, or the remaining ones are recorded. |

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
19. NIST IR 8547 — Transition to Post-Quantum Cryptography Standards — NIST. <https://csrc.nist.gov/pubs/ir/8547/ipd> (initial public draft (November 2024); proposes deprecating quantum-vulnerable public-key algorithms after 2030 and disallowing them after 2035 — dates may change in the final version)
20. NIST — Post-Quantum Cryptography Standardization: Evaluation Criteria, Security (Call for Proposals, Section 4.A.5) — NIST. <https://csrc.nist.gov/Projects/Post-Quantum-Cryptography/Post-Quantum-Cryptography-Standardization/Evaluation-Criteria/Security-(Evaluation-Criteria)> (security categories: AES-128 key search 2^170/MAXDEPTH quantum gates, AES-192 2^233/MAXDEPTH, AES-256 2^298/MAXDEPTH; MAXDEPTH 2^40–2^96)
21. OSV.dev — open-source vulnerability database and API — Open Source Security Foundation. <https://osv.dev/> (the database QSI queries for each exactly pinned version; every advisory id in a finding resolves at https://osv.dev/vulnerability/<id>)
22. P. W. Shor — Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms on a Quantum Computer (SIAM J. Comput., 1997) — SIAM. <https://doi.org/10.1137/S0097539795293172> (peer-reviewed article)
23. R. Babbush et al. — Securing Elliptic Curve Cryptocurrencies against Quantum Vulnerabilities: Resource Estimates and Mitigations (arXiv:2603.28846) — arXiv. <https://arxiv.org/abs/2603.28846> (preprint (2026-03-30, v2 2026-04-15): 256-bit ECDLP with < 1200 logical qubits and < 90 M Toffoli gates (or < 1450 and < 70 M); < 500,000 physical qubits at 10^-3 error, minutes)
24. S. Jaques, M. Naehrig, M. Roetteler, F. Virdia — Implementing Grover oracles for quantum key search on AES and LowMC (EUROCRYPT 2020; arXiv:1910.01700) — Springer / arXiv. <https://arxiv.org/abs/1910.01700> (peer-reviewed article: lower cost estimates for the AES key searches that define the NIST categories)

## Appendices: Cryptographic inventory

| Algorithm | Parameter | Library | Quantum status | Classical status | Count | Locations | Examples |
|---|---|---|---|---|---|---|---|
| RIPEMD-160 | RIPEMD-160 |  | weak classically | legacy | 2 | 2 | components/libwally-core/upstream/src/ccan/ccan/crypto/ripemd160/ripemd160.c; components/libwally-core/upstream/src/ccan/ccan/crypto/ripemd160/ripemd160.h |
| HMAC |  |  | reduced margin (Grover), approved | acceptable | 9 | 9 | components/libwally-core/upstream/include/wally.hpp:146; components/libwally-core/upstream/include/wally_bip32.h:170; components/libwally-core/upstream/src/aes.c:273 |
| PBKDF2 |  |  | reduced margin (Grover), approved | acceptable | 1 | 1 | components/libwally-core/upstream/src/pbkdf2.c |
| SHA-2 | SHA-512 |  | reduced margin (Grover), approved | acceptable | 2 | 2 | components/libwally-core/upstream/src/ccan/ccan/crypto/sha512/sha512.c; components/libwally-core/upstream/src/ccan/ccan/crypto/sha512/sha512.h |
| SHAKE | SHAKE256 |  | reduced margin (Grover), approved | acceptable | 2 | 2 | main/utils/shake256.c; main/utils/shake256.h |
| scrypt |  |  | reduced margin (Grover), approved | acceptable | 5 | 5 | components/libwally-core/upstream/src/scrypt.c; components/libwally-core/upstream/src/scrypt/crypto_scrypt.c; components/libwally-core/upstream/src/scrypt/crypto_scrypt_smix.c |
| SHA-2 |  |  | Grover: acceptable to NIST, below ECCG/ANSSI guidance | acceptable | 2 | 2 | components/esp32_bc-ur/src/sha2.c; components/esp32_bc-ur/src/sha2.h |
| SHA-2 | SHA-256 |  | Grover: acceptable to NIST, below ECCG/ANSSI guidance | acceptable | 4 | 4 | components/libwally-core/upstream/src/ccan/ccan/crypto/sha256/sha256.c; components/libwally-core/upstream/src/ccan/ccan/crypto/sha256/sha256.h; components/libwally-core/upstream/src/ccan/ccan/crypto/sha256/sha256_sse4.c |
| ECDH |  |  | vulnerable (Shor) | acceptable | 3 | 3 | components/libwally-core/upstream/src/ecdh.c; components/libwally-core/upstream/src/secp256k1/include/secp256k1_ecdh.h; components/libwally-core/upstream/src/secp256k1/src/bench.c:24 |
| ECDSA | secp256k1 |  | vulnerable (Shor) | acceptable | 36 | 36 | components/libwally-core/upstream/setup.py:58; components/libwally-core/upstream/src/amalgamation/combined.c:34; components/libwally-core/upstream/src/internal.h:33 |
| ECDSA |  |  | vulnerable (Shor) | acceptable | 16 | 16 | components/libwally-core/upstream/src/anti_exfil.c:72; components/libwally-core/upstream/src/secp256k1/contrib/lax_der_parsing.c:11; components/libwally-core/upstream/src/secp256k1/contrib/lax_der_parsing.h:88 |
| RSA | 4096-bit |  | vulnerable (Shor) | acceptable | 2 | 2 | components/libwally-core/upstream/SECURITY.md (line 52) |
| RSA |  |  | vulnerable (Shor) | acceptable | 2 | 2 | main/rsa.c; main/rsa.h |
| Schnorr (BIP-340) |  |  | vulnerable (Shor) | acceptable | 7 | 7 | components/libwally-core/upstream/src/secp256k1/include/secp256k1_schnorrsig.h:82; components/libwally-core/upstream/src/secp256k1/include/secp256k1_schnorrsig_halfagg.h:43; components/libwally-core/upstream/src/secp256k1/src/modules/musig/session_impl.h:621 |

_Long lists are grouped here; the full per-file list is in the JSON report, signed with the same key._

## Appendices: Input files

| File | Size | SHA-256 | Redactions |
|---|---|---|---|
| components/assets/assets_snapshot.c | 2103 | `ec1f77a3fc4474a97c955a063a815513508aed16ae9de70f91ca06452845d113` | 0 |
| components/assets/assets_snapshot.h | 514 | `a680e722bb23d471e95bbc65a990620dd383a2b971322d2bcea4748319c42a8f` | 0 |
| components/assets/gen_assets.py | 2715 | `9d8beedc80645bb85c3892b0d2532e4bf39015d7a6940aa17654afdd19062dbe` | 0 |
| components/autogenlang/gen_locale.py | 3762 | `5d86c480623ba04ca88a4eb227fe52ac22acdb6632a525e9f14d64348e72e06d` | 0 |
| components/autogenlang/jlocale.c | 1083 | `a2867e2942a695dd8f91dab15cf6638339bd91e66e459d243c1f5164034fb4f2` | 0 |
| components/autogenlang/jlocale.h | 703 | `237a507c4e96730d74f1966ff903c984bcaf6d2282983cd673f3b991ae17a43b` | 0 |
| components/esp32-quirc/lib/decode.c | 22800 | `eaae29c6cdc2b68e996dcc8fe1e17669a4c9bcd8b2a2871170b913d0e5d92686` | 0 |
| components/esp32-quirc/lib/identify.c | 33069 | `932e3f59f2a53449a6f9a96711f6b235f33098caaace0f5289d06c1b15eaab00` | 0 |
| components/esp32-quirc/lib/quirc.c | 2643 | `098d6fcff90f0f1b6e567bcd0106a9f2e3b2813a32eda55ea0abf8618e9b2ebd` | 0 |
| components/esp32-quirc/lib/quirc.h | 5789 | `4ae430f11eae91c19e497a5c6a33e8ae3d63959327cf4d7401185f05f203e218` | 0 |
| components/esp32-quirc/lib/quirc_internal.h | 3256 | `8f91d08224445af8f59b22c3ee7cbd8125b66dcad3c114617b321cf1f09dc9ed` | 0 |
| components/esp32-quirc/lib/version_db.c | 9934 | `1313ca98abb0342f1879cbc7cf2a2f7a6ec6c5f53f8342dda7be1251e508b590` | 0 |
| components/esp32-quirc/openmv/collections.c | 1662 | `832f54697073cc3476e4eaddc73362bf2378070f5bd03fd444d06f5e59bd2c63` | 0 |
| components/esp32-quirc/openmv/collections.h | 965 | `bb8700a2f2be2c8c4694896df16db1263df4d8ef4667c4f0f592a70ea2087cf1` | 0 |
| components/esp32-quirc/openmv/fmath.h | 1619 | `162de4e6e80de93f2ed28eafbfa16d90052c1f7ff6e7fc6afba47bbf2e7656c5` | 0 |
| components/esp32-rotary-encoder/include/rotary_encoder.h | 7247 | `b3ac17bb6ec08b1170f5806c55db7789b62716459a2585cdd6500449abc278d0` | 0 |
| components/esp32-rotary-encoder/rotary_encoder.c | 11045 | `1de7b32b77f37f3023f67c4161873b8f1632c9d0b43a65cc786f85ed293e2b50` | 0 |
| components/esp32_bc-ur/CLA-signed/CLA.gorazdko.41F0EA1699A74C1E2FA41B538CF96BC3FF9DBBCE.asc | 4412 | `7d33b77a5eb135e9b5a975edc67491f236f4a9a2a042a6fb4807e0692db597fa` | 0 |
| components/esp32_bc-ur/CLA-signed/CLA.wolfmcnally.943652EE38441760C3DC35364B6C2FCF894780AE.asc | 4028 | `d304435a759e2cb6e2fa2c7e16d84c4b2b15b5d09de58e4a84a35a09b9691ef1` | 0 |
| components/esp32_bc-ur/src/bc-ur.hpp | 528 | `40df2bfc8295525203a349c8ae60e8e965ad37f2337a216080a10fc2032e039f` | 0 |
| components/esp32_bc-ur/src/bytewords.cpp | 7264 | `78eb4d49e8435db5aacf352fa080ef4d388cdf74edc24e9f37c6187b7bae8a15` | 0 |
| components/esp32_bc-ur/src/bytewords.hpp | 528 | `7589b1785de98f2f845dccc06d3dbf13f8c8f6603cc2636f79660c977fc16d0a` | 0 |
| components/esp32_bc-ur/src/cbor-lite.hpp | 20610 | `896dec208c574224420b1415131e0b3916e833941e078873486fff570c5b09d8` | 0 |
| components/esp32_bc-ur/src/cdecoder.h | 998 | `f95f23b5c1c6203f785a3a1fd2c9a93d2345f9217933a567443421e21280bc52` | 0 |
| components/esp32_bc-ur/src/cencoder.h | 1017 | `e942fff6390e7a29db59dbf4cd1c73204db71e3ae85dfb7f7a76cd002bb11229` | 0 |
| components/esp32_bc-ur/src/crc32.c | 975 | `42a40df27042ba588a75c9dbb81fddb13ccdf2b6d23fe468c7e1ac69405d3db4` | 0 |
| components/esp32_bc-ur/src/crc32.h | 556 | `dd772af1a4c3424e02ea8a78a5b1e47e8c4e0e40d5a8a9591367b13e2a08c3b9` | 0 |
| components/esp32_bc-ur/src/fountain-decoder.cpp | 6560 | `1db9c5920b4f3451e32aa29a0d35000fcc187245476fdebcc55fd30b3342f548` | 0 |
| components/esp32_bc-ur/src/fountain-decoder.hpp | 3319 | `3feaaf5a28145c3812875f30f843067486e5971983db275c3a3520fe2da8084f` | 0 |
| components/esp32_bc-ur/src/fountain-encoder.cpp | 6696 | `23d95af7d1e0bfad0e9ba2abd45ae14c03e722938d3db5f2fbbb2c8a84dc9af3` | 0 |
| components/esp32_bc-ur/src/fountain-encoder.hpp | 2525 | `1928f66b4f66b2c7c0b0a0bb7944430c3a0b61685b4fc694ac9f1cca20d26433` | 0 |
| components/esp32_bc-ur/src/fountain-utils.cpp | 2122 | `4b2bb5060c09d049e7f702157d649e0968fa58d199c127c267eb5c2ba847bd53` | 0 |
| components/esp32_bc-ur/src/fountain-utils.hpp | 1308 | `a389b161d33037fa6d1f3817508c1c6c12270819a1a307abd178960196411707` | 0 |
| components/esp32_bc-ur/src/memzero.c | 2371 | `e079c96d106e8fb94792a84633d491b178151b485abccb1e70626c89b985cb2f` | 0 |
| components/esp32_bc-ur/src/memzero.h | 146 | `b97b8177b7e8a5145f1924a1195bb4228305741e141697bed8266913d11cb321` | 0 |
| components/esp32_bc-ur/src/psram-allocator.hpp | 1074 | `e0b889435117a283decd54954a229b23c98c3b65389ed3dd2ebf658d07dcce7c` | 0 |
| components/esp32_bc-ur/src/random-sampler.cpp | 2005 | `9db3b85bb093ab9a634318b6e7e1784fc3a55a8696cc1f144e110628f545020a` | 0 |
| components/esp32_bc-ur/src/random-sampler.hpp | 778 | `ed32061f179179b4f220affa3629b2ce9f5565fd452542ed137cbfaf3854ff7f` | 0 |
| components/esp32_bc-ur/src/sha2.c | 27586 | `f2d198651782b1fd9ce32308551955486b8a30c3d61a7205d9102662347ea324` | 0 |
| components/esp32_bc-ur/src/sha2.h | 4018 | `33c81cba2aca364b74a0205e1c294795046f29d206d730990b7b31487e14483d` | 0 |
| components/esp32_bc-ur/src/ur-decoder.cpp | 6206 | `561364d15d528855dff672332700bd4ff01db2cc30c38ad5981ff0311ae9669e` | 0 |
| components/esp32_bc-ur/src/ur-decoder.hpp | 2427 | `731ca04a557bcdbccbbeab1bedbdc3d830f3aa40860f525996ada83779891b60` | 0 |
| components/esp32_bc-ur/src/ur-encoder.cpp | 4142 | `719edb19a5cfe0aab44822447be58177824321a142ea1cdfba2bf934c178067e` | 0 |
| components/esp32_bc-ur/src/ur-encoder.hpp | 1698 | `70fbdfb8edeeaafc59319880a01aa0e63d5f870495ea1041146c4c8280af4a87` | 0 |
| components/esp32_bc-ur/src/ur.cpp | 536 | `a4a9ef9c96c9619d4f3fb055cbcfd44fc6a3beb85973ef7cbf632de1b94c60de` | 0 |
| components/esp32_bc-ur/src/ur.hpp | 629 | `aa99021077e929b2ddc37190e7bd65db0fd7be0ee24df1c436f6e41a6edb141b` | 0 |
| components/esp32_bc-ur/src/utils.cpp | 1980 | `e9eb8c577fd22f7463c86856f61539142bb264a713e35085bcb3b8fec45b457c` | 0 |
| components/esp32_bc-ur/src/utils.hpp | 2201 | `7f6484296e698ba343d1ec6f1e7f93809ab00de40d36d87f655ebfa2f1e15249` | 0 |
| components/esp32_bc-ur/src/xoshiro256.cpp | 2027 | `37c9183a02c28859c92422f0c69de314ccbaeb59fafced22572a2389f712b27a` | 0 |
| components/esp32_bc-ur/src/xoshiro256.hpp | 530 | `d72cd4a37d04a8553196a120d26132e1e57a67c2f527e67187239ad1207be778` | 0 |
| components/esp32_bsdiff/bsdiff.c | 9697 | `e03e27e1f289c7746bf3734245a77fbcc6bb615207feedf0239e9616a1519cc7` | 0 |
| components/esp32_bsdiff/bsdiff.h | 1738 | `0c62584472d7b1e97ee59221614b5270512fe335f44f9120b4aeb12693e92164` | 0 |
| components/esp32_bsdiff/bspatch.c | 6267 | `49727e4bcd81767180365c91f252bcb89b214afa3c116300de6376af64a59243` | 0 |
| components/esp32_bsdiff/bspatch.h | 1951 | `9f6d00b6b892e168f95c935eb4f98a74914c7a21afda3a6798d86b1f1c731067` | 0 |
| components/esp32_deflate/deflate.c | 7375 | `83f4ce0e28fda75cdd5ba7ef3cdac5ba4f319149594a8b07cb89a379c1353893` | 0 |
| components/esp32_deflate/deflate.h | 3881 | `51e86c8beb6991d8e7aeaa81eabbc11a2df2be0d987aa33a64e11581ef6ef33e` | 0 |
| components/google-otpauth-migrate/google-otpauth-migration.pb.c | 391 | `d75daa9efdf81db881563a904ca354d1c05c345d467b51b80182b780fff1643b` | 0 |
| components/google-otpauth-migrate/google-otpauth-migration.pb.h | 5866 | `0a37cbc704ef223415355e579f4077be77b2d2014bd1f21107ee372acf44741c` | 0 |
| components/google-otpauth-migrate/google-otpauth-migration.proto | 746 | `0661efbbeaf3b3d99ac84372a75ae45e0c60ef5949a9d9cf3db21b7c30cfa4bc` | 0 |
| components/google-otpauth-migrate/pb.h | 44863 | `8da6125d3b5e650781db012a97d3dd7d2586831b84eade542690f893337e87e4` | 0 |
| components/google-otpauth-migrate/pb_common.c | 12141 | `8d2ec28baaaf2b7a5e90e4cb2fa9700d21cef7f826f051a637c30b7a1e6a0516` | 0 |
| components/google-otpauth-migrate/pb_common.h | 1677 | `6495a691aca68d6973f2274b5dd54b74fbb57f6b019c45fff255a857fe1abcfd` | 0 |
| components/google-otpauth-migrate/pb_decode.c | 55680 | `3c3394300a93a152ac6280786a2d98ed57e0012ab9ee69af31176a6c549e51b5` | 0 |
| components/google-otpauth-migrate/pb_decode.h | 7870 | `1747746e5961de5789bcf0795588da0790cd18b2e4e706ad9c7099a0fa1cc83f` | 0 |
| components/libwally-core/config.h | 5305 | `ba770c0e09abb8fa74523560cc7e6b24fe6a7bcf15637501926595132080cdef` | 0 |
| components/libwally-core/upstream/SECURITY.md | 5780 | `3ab230590b464090a9bd2d92a77fe84b7f6514328b8922e4b7bfd4f8a73b0e6b` | 0 |
| components/libwally-core/upstream/contrib/requirements.txt | 76 | `40039c059b565df34460f06ccbc2e54a86f758b1347259ef84389837264698a7` | 0 |
| components/libwally-core/upstream/docs/source/conf.py | 9400 | `bc6dfa797847a290d783f88a90731a5b2e28c94598511824c10e7b3302b0be28` | 0 |
| components/libwally-core/upstream/include/wally.hpp | 173558 | `29fe67c31ac2364b9bcbddf331b1a2547c3484bd29a4bad36da1e0bf1723ea26` | 0 |
| components/libwally-core/upstream/include/wally_address.h | 14902 | `7f7c7746344d85a5d4c4dd294eacb28d93f80d7efc306ea47f83adf21d68b9f7` | 0 |
| components/libwally-core/upstream/include/wally_anti_exfil.h | 4298 | `3b5dc9737f3c2921ef1ef8f8b14254b705fe2df2d30202115ef5bbb85c347833` | 0 |
| components/libwally-core/upstream/include/wally_bip32.h | 18820 | `810cb696a773ebfc473140d4500466f4755b0874ffe0b4be941524d43684cda9` | 0 |
| components/libwally-core/upstream/include/wally_bip38.h | 4113 | `21b2a312a50b325c239960e44dbbfc71ed8c0c05db04ac6e4ac85c43f7f3ed6b` | 0 |
| components/libwally-core/upstream/include/wally_bip39.h | 4675 | `37d73b2b2c5477c56b5f226f8e6a67595f8135e0dbdf9022c5572955b4359068` | 0 |
| components/libwally-core/upstream/include/wally_bip85.h | 2147 | `e905f637ff408e6e406f9b4ee292be6e4592770c69af6dfbcb46674c63cb88ac` | 0 |
| components/libwally-core/upstream/include/wally_coinselection.h | 1952 | `7e8ffb7f18e814876726e5dc7338b745b6924ed7318148b6708fa98f17b87193` | 0 |
| components/libwally-core/upstream/include/wally_core.h | 14337 | `3022b6eee2211127b4b29afc07e9efa6a3b43c620cc5c19c8505a2517c4a33dc` | 0 |
| components/libwally-core/upstream/include/wally_crypto.h | 36912 | `2181a542b32bbf426de0259360751fa6e821dd45e0f67bc7015533bb08c629c0` | 0 |
| components/libwally-core/upstream/include/wally_descriptor.h | 18149 | `9651e5cd915347dc9033a9a3e8f69698f762bcda031bfbbb7b29334f2dcc1a95` | 0 |
| components/libwally-core/upstream/include/wally_elements.h | 30713 | `12520fe83d0d7a6985a8f89f3483465920a56c70ef8bfe2c5ccea238a7eea498` | 0 |
| components/libwally-core/upstream/include/wally_map.h | 23352 | `49e8504df27c0a3530f125fb11bf8b6476a9ec4abce40b1b5321121a85cd9e0e` | 0 |
| components/libwally-core/upstream/include/wally_psbt.h | 92379 | `5f22a3900c2be3fba63b3f0e48fe36509c7db4630ee14a9a6d48675c406a3cc0` | 0 |
| components/libwally-core/upstream/include/wally_psbt_members.h | 28550 | `02f5d3b6038d0ddc79830686dcfe05f92f5c0fdfd4e3d5974a586d82c1e570c7` | 0 |
| components/libwally-core/upstream/include/wally_script.h | 24734 | `f9714d64df46d9282d0af7295f3b5efad82558fa4ba6494fa52b0f989c09f19e` | 0 |
| components/libwally-core/upstream/include/wally_symmetric.h | 1403 | `c592f068170a611a0b4f45610f8af1901f25f7c835898ddf85cf48c02925cc31` | 0 |
| components/libwally-core/upstream/include/wally_transaction.h | 55083 | `02f09466ce2e7bc8f326f762efde701d02c84334018cb4bc5fa8d909be851007` | 0 |
| components/libwally-core/upstream/include/wally_transaction_members.h | 14257 | `71199aa909d73759bcb9328885072d810bfabe9cc7f661a3dd0b50597f390872` | 0 |
| components/libwally-core/upstream/pyproject.toml | 91 | `81562b11a9a84cb5d47f66a78e7338546fddb7f5c62f4308b337e891f7d8a0d7` | 0 |
| components/libwally-core/upstream/setup.py | 7382 | `016931c29406077b6d11f67500ba0bc5cc27e7fa9e76a7b4a7de30e9f0a17325` | 0 |
| components/libwally-core/upstream/src/address.c | 8162 | `f7faee93c6eec3fa6311ef59e30aee3aa5c38fbedb89567b53787602e5e7ec23` | 0 |
| components/libwally-core/upstream/src/aes.c | 13043 | `5a9d9d02276f306f18a1afec725d00544d43ce5e991df8f7f9e66f651b37fbda` | 0 |
| components/libwally-core/upstream/src/amalgamation/combined.c | 3370 | `ea2c2393b4f2f218bed700c4d880fdff8f6491ab98c42de945a14f9c1e265749` | 0 |
| components/libwally-core/upstream/src/amalgamation/windows_config/config.h | 518 | `1b14c47566007e84ccf825e180841132f485fbfa7cca9157024dde4f4c4b559e` | 0 |
| components/libwally-core/upstream/src/anti_exfil.c | 4182 | `9a82b2e8a8fb25df7d59ee0108552079c29c7f5e522a9ba9700f4fa10983a612` | 0 |
| components/libwally-core/upstream/src/base58.h | 329 | `19d52a6c48e467662faf41cbe7bcaf86850dcc79baa1dea43f29031910c8a75d` | 0 |
| components/libwally-core/upstream/src/base_58.c | 10621 | `2765b178cc94418c37ac520fbbcd7082fb817fa4d2ba484c5abba7971fcaba6e` | 0 |
| components/libwally-core/upstream/src/base_64.c | 2352 | `fdd2a5e08206baee701ede543348dcf13f6239af39992f5cd653f680461c7bac` | 0 |
| components/libwally-core/upstream/src/bech32.c | 11107 | `fbef184ce2e675180e1d4b08294fde0d22aace22c3bc6ccd3c76eb3eec11b458` | 0 |
| components/libwally-core/upstream/src/bip32.c | 42775 | `ebe4939b794fa8d447ef1054296842c5e1fa30bf16491dbb5cc5c08151937337` | 0 |
| components/libwally-core/upstream/src/bip32_int.h | 1789 | `00614706452155f6adcc4699a3bee9537ccb793993ffcd02a69e5c8f16e9aa99` | 0 |
| components/libwally-core/upstream/src/bip38.c | 13750 | `7ded4248d2176e6f18ef02d556bc138872d191299f460e4ef77f501d4679248f` | 0 |
| components/libwally-core/upstream/src/bip39.c | 7536 | `0b4ad66758f2f02a9fa5dbaa1daad4094deb8bff5290b612770b8c37d976d61d` | 0 |
| components/libwally-core/upstream/src/bip85.c | 4885 | `4eeff959873565157d2c8696536bdbb3db402e709e79dfddd7c9b7cb49f01a4a` | 0 |
| components/libwally-core/upstream/src/blech32.c | 11446 | `6f115f7716d84eb277e942fcb281b55a229b0befc7947f681b6ad861e8383153` | 0 |
| components/libwally-core/upstream/src/ccan/ccan/base64/base64.c | 7742 | `2660b9eeb6c66e0a8187f8b946471f1d9463bb601bf3780aaf4af901498bdf0f` | 0 |
| components/libwally-core/upstream/src/ccan/ccan/base64/base64.h | 8587 | `75e1376547570c23b5cb51a58b7eb06e00e22f117f45e3af5510970ea6934795` | 0 |
| components/libwally-core/upstream/src/ccan/ccan/build_assert/build_assert.h | 1228 | `eeebbbc75d152ab145fee9ea5fb3e914822047a67c487ad2f13d9c724fc9384d` | 0 |
| components/libwally-core/upstream/src/ccan/ccan/compiler/compiler.h | 6208 | `265ec2faa538935602f4d9527e027aff5d2201630a405c2194212e9e9282cc1a` | 0 |
| components/libwally-core/upstream/src/ccan/ccan/crypto/ripemd160/ripemd160.c | 14205 | `4d231f50f83073f1a4c0a79f9c3e755e9350b5d5577a2c0e22cf5670dc645a1d` | 0 |
| components/libwally-core/upstream/src/ccan/ccan/crypto/ripemd160/ripemd160.h | 4229 | `7f7d917d859e20b40c95e94b9a4862eda420dd9caed14b9619d1fcfc0e1d452b` | 0 |
| components/libwally-core/upstream/src/ccan/ccan/crypto/sha256/sha256.c | 12527 | `286fc60aeaef4c3f23e61f5c43068b39fbfa13336e6f0bee2223eca5865fe93f` | 0 |
| components/libwally-core/upstream/src/ccan/ccan/crypto/sha256/sha256.h | 4392 | `d68d0b50a1695e3762dc6a18f3e15de2c270c9d533831174c6e2d8dadaa040e7` | 0 |
| components/libwally-core/upstream/src/ccan/ccan/crypto/sha256/sha256_sse4.c | 26723 | `97974a76fb8ae60ea7b3f10e1f885631b38bd741739bfc29b82f2a9a4a896f32` | 0 |
| components/libwally-core/upstream/src/ccan/ccan/crypto/sha512/sha512.c | 12350 | `acfe1bc068339cee74a59ec420d11a1161fa3640b3a55e995409a76a3c33e80c` | 0 |
| components/libwally-core/upstream/src/ccan/ccan/crypto/sha512/sha512.h | 3799 | `2e013c21c38bdcecd5407f21a7cc7edb55d62cdaee0e2b6374241139324b7d1f` | 0 |
| components/libwally-core/upstream/src/ccan/ccan/endian/endian.h | 9168 | `079dc923af35babc0a19d48920453eac806aa28757809e5e431fb66f3c0511d9` | 0 |
| components/libwally-core/upstream/src/ccan/ccan/str/hex/hex.c | 1240 | `f19e45cfcd6f9e1a57135d0ab0f7664467a500db35a3377d7efa306bdef0670a` | 0 |
| components/libwally-core/upstream/src/ccan/ccan/str/hex/hex.h | 1907 | `bb26783b82e632be5a7bc2af185655119124086dbed9ea441eb96d3e30f224dd` | 0 |
| components/libwally-core/upstream/src/ccan/ccan/tap/tap.c | 9251 | `44ac24b231f4a27d49e3a14bd025394911740291b3ccfa56b0549972a14cdf99` | 0 |
| components/libwally-core/upstream/src/ccan/ccan/tap/tap.h | 8136 | `0349b6db4d1699703fae8ad17f0d8cd3c585a9eb5f259598d2c1011770914153` | 0 |
| components/libwally-core/upstream/src/ccan_config.h | 1856 | `fbfef65cb854aff875e982a0f3f49913a7e13e3425ad99fbcfb23ce5a7455526` | 0 |
| components/libwally-core/upstream/src/coins.c | 7481 | `32a65ff8892db2fa25f1ea43e4c5e4ae5dd2c853a369e771165cbd976ce98584` | 0 |
| components/libwally-core/upstream/src/cpufeatures/cpu-features.c | 40717 | `60b4e0194012595a58c88fcd4089bc72c4752f8fc829b022b1228a9c39afcc8b` | 0 |
| components/libwally-core/upstream/src/cpufeatures/cpu-features.h | 11746 | `4e85e43209f0ba184a4bc5d3353d99695d4b7543d436333cf465bd6c7ec0239f` | 0 |
| components/libwally-core/upstream/src/ctaes/bench.c | 4977 | `237677992b69e7dcc6d4fab66f74e8afa7c999dd3a16598e6acd3c9fdb13125b` | 0 |
| components/libwally-core/upstream/src/ctaes/ctaes.c | 18015 | `2f8a63e6a9a00da3fcc9c38d53dfbbb650376191689864ed211a36d8184c287b` | 0 |
| components/libwally-core/upstream/src/ctaes/ctaes.h | 1541 | `bf837cfa914ac30b11cea64d5267065614686d41586c886e84bd4e7e11112af2` | 0 |
| components/libwally-core/upstream/src/ctest/psbts.h | 96356 | `03ef1939fb98779fe78fd0619ac9af38b4b9f11d13d03ed5a4d5b8958dfc1d2e` | 0 |
| components/libwally-core/upstream/src/data/wordlists/chinese_simplified.c | 66952 | `0b5757eb83ab683d573f2f33a8f6beb55206f9341399350671a41bc8f97b41d9` | 0 |
| components/libwally-core/upstream/src/data/wordlists/chinese_traditional.c | 66952 | `e3c7f2043ed23fcc05a2d56c4a0fde20fb8d78e424a9de32d7cad151e8b4ceac` | 0 |
| components/libwally-core/upstream/src/data/wordlists/english.c | 90123 | `6281a94bbb2f078bf81c5e896ba256bfa647ecf15fba3fc17b56252b96a8eace` | 0 |
| components/libwally-core/upstream/src/data/wordlists/french.c | 108796 | `456ccc99b4e1deb3c32be31cd1da15fc2c24f68dcdf7bc44f728e92e696d0b2e` | 0 |
| components/libwally-core/upstream/src/data/wordlists/italian.c | 104983 | `a62efd66b93dba13bd6595c75223c16fba1c64249515745fdf692c1dc1adbe71` | 0 |
| components/libwally-core/upstream/src/data/wordlists/japanese.c | 157532 | `6e05670b15966f5ed2f9dda1eb65176ef0db0d9627d6722025c8b74f23be6c88` | 0 |
| components/libwally-core/upstream/src/data/wordlists/spanish.c | 94627 | `2868a35904d7a59825854b1c7aa74b1ceb48260706c841f2c24cd62ad608348a` | 0 |
| components/libwally-core/upstream/src/descriptor.c | 135286 | `67db7c1b957cef26b1b8c3c75804c8e0e0d2df5cb6e9fcbe7b18020c9a2c393c` | 0 |
| components/libwally-core/upstream/src/ecdh.c | 909 | `8ee530f4d9ae4d9bf59d56be587898902ef61da538b660f427dd222034bcb1f6` | 0 |
| components/libwally-core/upstream/src/elements.c | 45442 | `f2619a99c89c18b470b3d309f004bfa99994890e5c46df2527fe1f545189cae2` | 0 |
| components/libwally-core/upstream/src/hex_.c | 1814 | `b2d657a4efdea61b6fc6499384a54e084ece23b08283880d8d275bc36cb02d76` | 0 |
| components/libwally-core/upstream/src/hmac.c | 1029 | `ec26247e22f48069c0b590cab1df5c9eb6405e174e58bc6ecaca625dcf4c84f9` | 0 |
| components/libwally-core/upstream/src/hmac.h | 945 | `272f5733e09fcd7bbed99e7090d6dfa45f2804190eb86c9a865b152d71db64a7` | 0 |
| components/libwally-core/upstream/src/internal.c | 18775 | `fc35a46528e06386282ca70d31fde07b9aaee997a25ca7dcc41b69a04a8b36c4` | 0 |
| components/libwally-core/upstream/src/internal.h | 7781 | `f21377ed9eba49d06a5664dc4c28437e62d1b2868f4d6cfb75fd844804cd4b65` | 0 |
| components/libwally-core/upstream/src/map.c | 32790 | `d51f09a338d5453dacd2586c6704008c06fa308fe5349048377b686cdc8aedf8` | 0 |
| components/libwally-core/upstream/src/mnemonic.c | 3004 | `8a1bb43751a5bfd8702a970eaa6707af12c97df778ea917daedba6f12c75fbba` | 0 |
| components/libwally-core/upstream/src/mnemonic.h | 975 | `74f5df50a738b55423f5920b0d3d4441c1ceabc680aaac4a63e2454c6004cb13` | 0 |
| components/libwally-core/upstream/src/pbkdf2.c | 889 | `105f023951c03024c125a18b0f5862fe766f58fd0f4c64c5f389804f2a5bddf6` | 0 |
| components/libwally-core/upstream/src/psbt.c | 243364 | `e76cac2111ddcdbd1abe201be5f2411cb411156ec84e5848111007e3cfb28809` | 0 |
| components/libwally-core/upstream/src/psbt_io.h | 13779 | `851894fd3136feb0c911152c290491b5a858cbc454731fb1cebc347a5d8d4b0a` | 0 |
| components/libwally-core/upstream/src/pullpush.c | 7444 | `777d7edd1d1b649a2dcf32a7db0da3eab02548c4682355420db452bd2d60b6da` | 0 |
| components/libwally-core/upstream/src/pullpush.h | 4514 | `b1d4ce8e2abed2de4edb1917f4822517e235cfefc31ff238a57e5964f08fb121` | 0 |
| components/libwally-core/upstream/src/pyexample/anti-exfil.py | 660 | `1a667aaadb838d6e397bb99d1bf6b1cb5a4635c0c03174ef495db6644841b428` | 0 |
| components/libwally-core/upstream/src/pyexample/liquid/receive-send.py | 22276 | `bc90191a9307600954861a8368f2c4b5a3599a64d10068be4a4064a5a4130a71` | 0 |
| components/libwally-core/upstream/src/script.c | 46749 | `fb0fe6ddcd942103db5b0d2dc44259d154aea6b1f9f0fc792b6ab49f37932a9f` | 0 |
| components/libwally-core/upstream/src/script.h | 818 | `1617a0849f8db48baa659756a8df6fd8cda1ad03517959f392aa798f52c29cfa` | 0 |
| components/libwally-core/upstream/src/script_int.h | 3734 | `bfb7c554290734d0fd4204ebcbad2496f46e4c475bfcfa44b1d364ffa97d06f4` | 0 |
| components/libwally-core/upstream/src/scrypt/crypto_scrypt.c | 7396 | `033c20dbf6d9353f01f45cf14752afea67811c0fb487b7e2fc086d791c084ee5` | 0 |
| components/libwally-core/upstream/src/scrypt/crypto_scrypt_smix.c | 6241 | `87c79624c9a5b5d1375dd332734f14758fb87781e5ab4dc3638dabfcb09b0f6b` | 0 |
| components/libwally-core/upstream/src/scrypt/crypto_scrypt_smix_neon.c | 9554 | `a92a7abf7fcd2cd406acd8a3fa37a16fddf05f05581305d5900daf65a70ecdcd` | 0 |
| components/libwally-core/upstream/src/scrypt/crypto_scrypt_smix_sse2.c | 7101 | `5a0b698f710cdc38e951d574804fde85b74e67d014da2207a08441de17c616da` | 0 |
| components/libwally-core/upstream/src/scrypt.c | 2523 | `7912d0bfe719e149ed99ed1dc097e3087e0a9843433aedbeb749c42ac54d8e0c` | 0 |
| components/libwally-core/upstream/src/secp256k1/contrib/lax_der_parsing.c | 3595 | `4da2ecdc0a3b9dbb9029d188bb0243764a3c2f2324613a688f1ac4d3fc878851` | 0 |
| components/libwally-core/upstream/src/secp256k1/contrib/lax_der_parsing.h | 4230 | `7f3e8ba009f19a5f2759c9065af02cc8e62351100d69f8ae7e762fa4b65ea675` | 0 |
| components/libwally-core/upstream/src/secp256k1/contrib/lax_der_privatekey_parsing.c | 5112 | `48352c75520eecd141936c0011601925510cdf60afd3e46e79f0a0547cbc78da` | 0 |
| components/libwally-core/upstream/src/secp256k1/contrib/lax_der_privatekey_parsing.h | 4016 | `3420812d623c0f2f86debe0535f98eab9b929036bb2fee2de8e3b1adc3e1a0b9` | 0 |
| components/libwally-core/upstream/src/secp256k1/include/secp256k1.h | 44268 | `e1717d8943d4a28ad0c7dc6c0b19d0afbc40454caa9d1f50d80bb7bb49ed2209` | 0 |
| components/libwally-core/upstream/src/secp256k1/include/secp256k1_bppp.h | 2761 | `bbd36b1d30ba8d181a84a234a29b91e1af6a6610cb24b7bc61326d12279d0feb` | 0 |
| components/libwally-core/upstream/src/secp256k1/include/secp256k1_ecdh.h | 2560 | `ad314d14cb79a79d4113862f21e0deccf37962db7811c801dab2899f91dd8222` | 0 |
| components/libwally-core/upstream/src/secp256k1/include/secp256k1_ecdsa_adaptor.h | 7476 | `5bb2f1c0e958c2380ff3dcc15e5f70d5ecf24517349d25efdedf493882405015` | 0 |
| components/libwally-core/upstream/src/secp256k1/include/secp256k1_ecdsa_s2c.h | 12237 | `ffcb82928ed6e09cd0e95e15cb3c67d95b1914286cc1fe1408ade0ddf459294e` | 0 |
| components/libwally-core/upstream/src/secp256k1/include/secp256k1_ellswift.h | 9148 | `620db468b1c13968946e9f404ceb59a3f11c895603bf1dcd3399567d7bf10e99` | 0 |
| components/libwally-core/upstream/src/secp256k1/include/secp256k1_extrakeys.h | 10870 | `7c3468c9fd192ad152c5cf042cb44938961d752fcf19966123ce6a5e3fd31637` | 0 |
| components/libwally-core/upstream/src/secp256k1/include/secp256k1_generator.h | 10816 | `1c08ef2a929eb52bff724c2d3d6e8d5a355382d76f9d510c2c4b769e5902ea6d` | 0 |
| components/libwally-core/upstream/src/secp256k1/include/secp256k1_musig.h | 32175 | `e6e2595005881a64bce69a05cba3e2715e56a7a06398c029f736cc52bcfedc38` | 0 |
| components/libwally-core/upstream/src/secp256k1/include/secp256k1_preallocated.h | 5966 | `b7283d4cc9c13bb2572dc92e69cea76f3270403baf5748ea4d91a1064b951b85` | 0 |
| components/libwally-core/upstream/src/secp256k1/include/secp256k1_rangeproof.h | 11792 | `32ac0541545b6d8b562cd7e41043807fd06aed80dbdd89d820538f04e3b4e305` | 0 |
| components/libwally-core/upstream/src/secp256k1/include/secp256k1_recovery.h | 5250 | `e00678a1108acb36c6631a1e290cf33813b0ed5965d23226367008f58abb27f2` | 0 |
| components/libwally-core/upstream/src/secp256k1/include/secp256k1_schnorrsig.h | 8177 | `8185d6c6ea3234fff05f38fad4b1b6f48f0574ab599dfc87297ab9bca0abfca5` | 0 |
| components/libwally-core/upstream/src/secp256k1/include/secp256k1_schnorrsig_halfagg.h | 4908 | `89669a3ad2c904072c1177e7b783996af5d72635bb7590e02284e776cc4e085f` | 0 |
| components/libwally-core/upstream/src/secp256k1/include/secp256k1_surjectionproof.h | 12407 | `f6b245fe8234309715225fb6a3fdf3a4d20a4f5a7f395c1686debae189af07a0` | 0 |
| components/libwally-core/upstream/src/secp256k1/include/secp256k1_whitelist.h | 6241 | `2e060720e5f8bdef9b99021a3c1d45a610219f4026d1421c86a8112a0e5e7d66` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/assumptions.h | 4667 | `cc875f356cc8f7f272def71f7d7261e44cc27a18a5b668cd8192c84d238e4e68` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/bench.c | 10190 | `832edacf541809e3cbc59a4e698d5e33a9388a7dddd55662936244cd106fccce` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/bench.h | 4777 | `12fafa36167bb38d28698536cdb34bdbcf8c972eed4d3cf69e71796972b880d1` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/bench_bppp.c | 1102 | `7c17a6b0fada57db18cc68b1ec183f1e6346983903ee1da4f894acb09bfab6e2` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/bench_ecmult.c | 15684 | `7daaf2e676b42f08a509b846139e90f9f04da94aaeda62a64ce38f64e45884a4` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/bench_generator.c | 2001 | `6396798ee1f4a018d4ebd9e962b6c289f4a1928a870c20918285500f7972bf61` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/bench_internal.c | 19230 | `6fb683c1d9dd79261e9a519c033ee6934687f18bcdad0327f570769d57fe0e42` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/bench_rangeproof.c | 2349 | `6c24fa0c6c12242da3b2629742e0baab65b24967d173fb83e94e2ce1847d8a10` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/bench_whitelist.c | 4089 | `8f77ebf85792d8270790e1c0689d24896c2da3d7ce6f35c6dffec2909ddc4082` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/checkmem.h | 5355 | `f367089bffa53b8998047de2f718f75d627dad549a1e5dc2a9ce9ab9f581ffe8` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/eccommit.h | 2198 | `3b04b7fdae817984c26ce995fad4f3f6d72d5c05b9d3f78d5991c531a5e99eed` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/eccommit_impl.h | 3165 | `6c71a9cba341b7782302741603db3ae2179b699ce2e7670cb03a749b94d114ca` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/ecdsa.h | 1164 | `f97753416b0971133ad9d8acf9af02259931d0285a0333a9753201a353070ef6` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/ecdsa_impl.h | 10562 | `d396c1c758db5dffdc3044f00895bc1206f797003ea7f17004628c66b09e1c99` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/eckey.h | 1449 | `cf511599285faecd27ace6191eca3945d85bc852b11076a1b1727759a6b03056` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/eckey_impl.h | 3439 | `4d327c593520c3f60f7b86d407df0870c26cf58037e4156ba8f92258304fd6b6` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/ecmult.h | 2768 | `1e87f35efb7e7e5b6ea1d6ec22bbaeab33ccd4eacc41a9092ee518ece9237ced` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/ecmult_compute_table.h | 1073 | `5a8ce69b18d777c3ad608ef173fd6a47c75b9c37bc6801f19ca4c44eb4b9f8f6` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/ecmult_compute_table_impl.h | 1916 | `6082339f616cd5a628300df24e66353c1374a117e24ddd474fe6151dbc620d60` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/ecmult_const.h | 1354 | `4705e7baabcbf8fd1853f8cef45a7f6a3075b98925d91cc209afda2c956942ba` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/ecmult_const_impl.h | 19584 | `07238bcf17c3292bb8198f7f37baf068bdc9a6a57f843c439e220eb08f400607` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/ecmult_gen.h | 5458 | `38e1457b6e8ba8f488e5a0e19fb625df97603c0c3c7e03a34bad22026f365fd3` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/ecmult_gen_compute_table.h | 672 | `51eb54b0cb7b49b25cf751efb2799322d73c97bc9bdd2a263feff2d2d6eeff9f` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/ecmult_gen_compute_table_impl.h | 4705 | `9ae524743bb5871bff7e41e48b61218336b1919769132aafa944283ef1bb88f2` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/ecmult_gen_impl.h | 16504 | `568bb11a3ecbbf116f13009b9e6de78c23fce2521f5961db1329203b5d0ab219` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/ecmult_impl.h | 34325 | `ce70d26cb987c9bb2a2477389459437fc2831546c9c14404b58cf7ed07f32cc1` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/field.h | 15119 | `a031e8655f38464b47aedec8afd73b3320da565fb50d163ae4f3c0ee247e3444` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/field_10x26.h | 2338 | `ba9a43b62e7e70e6e18af2787bd01dfc3a57fea527cf8ad0333194211ac7d7de` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/field_10x26_impl.h | 52106 | `6f209a533fd96e73f4c92b101bd3ca46a2f7553967ba7f44650a68ccbf4fbcf6` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/field_5x52.h | 2380 | `cbaa91c253ba84d99efcd334c7a39906c164d5edf3cde81200a44a606205cdce` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/field_5x52_impl.h | 19360 | `8104a1b630635c9cc89628142c9fa7afc6f31a888fe50c8ebb2bdf69ca208975` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/field_5x52_int128_impl.h | 11341 | `ee6d585731507c51dc8acd819b66556cf0cd804da1a4b6072a79c17eafbc940a` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/field_impl.h | 14052 | `33cb488ee009334a7a2ac52a7eabe39795bd184da0238e7acf73ae11374643b3` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/group.h | 12243 | `d5443ba9dc805fb378d6dcdab02bd616ab34409b7b91ceb342ff4cee12adcf7f` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/group_impl.h | 35125 | `663da90fb18b6fc8dace045ceb28ea8fae6e1c68081c209cf0c7dc954398f30d` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/hash.h | 2625 | `a7f39f2ed170d70841eff7d43d9c480dfda6cb2e8ee25e7e04bf7433c27193af` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/hash_impl.h | 15448 | `70247571d95e3c8824d6ca2e90956f6941c196a42d860083040690aaf9ccf6cc` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/hsort.h | 1685 | `220cb669835d34c252598ecff860c93edda337a9f8c2fc07b2b6cead7d48b284` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/hsort_impl.h | 4798 | `2861489c01b927b27d99efe173799a812434748b4addd30d102187ce4f3b66a9` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/int128.h | 3622 | `89ac5d91d64f857038d063dd70eec4b29b4f32aa218c790fe049137c347186cb` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/int128_impl.h | 376 | `5683c02dfc495639da259d80624711c1c449bbaee6186729e399e713a28b4719` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/int128_native.h | 581 | `b4c52c7ff091083f5eca9879b98641c7a38356a3c5321cbcc22ae1573e7711e1` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/int128_native_impl.h | 2881 | `ecaafefadbde3db034d4f44678096833d2d113fd21b4ff7044095b6153ec03a8` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/int128_struct.h | 229 | `0733b3a65719a1e9a8fb3564c71a38f2f31ca3522f40087d536dba90361b66e7` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/int128_struct_impl.h | 7884 | `0b4e2200327f5357078ba43b0e0514c58c2b1eb217b87ebc14d95efb913b5be2` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/modinv32.h | 1865 | `774887ccd462b145434d1d6b9ae9455aa3618e791544a2b61267e18931d5010d` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/modinv32_impl.h | 33492 | `befe02af7099a871677c7b05a81302dff5a4dc1d59f19b20bcb58cc28e096112` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/modinv64.h | 1969 | `b71cf177d768beac28fcb4f0ef545aafaad16ad0f275c70ee4c60b5f7549ac41` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/modinv64_impl.h | 37653 | `1254dc7ea941fc4d4ef0a85eed80db58d9e2647a8b8d19238d6afc048d63764d` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/modules/bppp/bppp_norm_product_impl.h | 20378 | `13b376aadaf6ad496b82de06e57ce781c8dd591670405a50b41beb06d8b71614` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/modules/bppp/bppp_transcript_impl.h | 1552 | `bc8b8afcf3e985bdb355e715c2f56f109e2fb5a109f393fb0359db17b8aafbe4` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/modules/bppp/bppp_util.h | 2794 | `fb22fd546df224866adc6c756f76170b4aa2575cdda6872ee56f32af8079db95` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/modules/bppp/main.h | 403 | `20d3c6914baf5513f17d02787e51a97ecaa1670202ea5ca15bf7b09a35b0aa80` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/modules/bppp/main_impl.h | 3583 | `938885438c1a41562294d15e068e9a7dac58972113e7e4945cd945f196dd6e5b` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/modules/ecdh/bench_impl.h | 1761 | `3929ead352b3b6425f0fdf94a1b2268d124cc0176929ae6ea3b4fa82abac0bbf` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/modules/ecdh/main_impl.h | 2929 | `3cf3b168e8048cd7b03c9b4d56d072214ef859a31bc970e5a16c2cbeba8fc4eb` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/modules/ecdsa_adaptor/dleq_impl.h | 6275 | `d5973e606b4225b4cbce6ea02496385f3a8e9c221aa3bcf6f62c108357baf0de` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/modules/ecdsa_adaptor/main_impl.h | 15004 | `157bf8e45ad426f56583b7def22d91418c0d4bec281b5ab9cd5fce3158a5a238` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/modules/ecdsa_s2c/main_impl.h | 8784 | `20bea71274c43c26093e5e00a22a9a0ac97eca2330291e2b2fe9f9864cbb3e4b` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/modules/ellswift/bench_impl.h | 4399 | `8973d64bda27eb72a4807aae665a1a2932d624370f9d40f8833f7c8f03b05564` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/modules/ellswift/main_impl.h | 27602 | `8deffa7b37a0602be2b87d0378419410e6cc9683ebcf3fb033d2eed56c4f8416` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/modules/extrakeys/main_impl.h | 9961 | `a58762afb6a494aaec984d2e65adacf1125be5e55ad2904af0f26e490cc0d3b4` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/modules/generator/main_impl.h | 17287 | `756c2aea7b7221d6b523ae17d367a6e819b67f87485987b2bfff71ed75e2e785` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/modules/generator/pedersen.h | 904 | `6529271ae3f7e786df540f650164e66cae35478157b5bba6fc885cde61d3e81f` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/modules/generator/pedersen_impl.h | 1729 | `1cfde5758fb1d3cbe4a2b8f6e9f6ef00eeb75f6895810dadf213bffc4553297a` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/modules/musig/adaptor_impl.h | 3359 | `e22baaaa040a80c84f0cd72a8aef3b6ba4c260a926d4039bebb2618d54b78010` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/modules/musig/keyagg.h | 1324 | `5349443b84525a85434ff8f92a1e7542c0982b1b783a682613026203de4148dd` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/modules/musig/keyagg_impl.h | 11171 | `fa67be67a1cdb0ad05fc6fd5fce158731ea499a18f1b616bd17fe3cf19dead87` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/modules/musig/main_impl.h | 452 | `ea8d83ca27ceafc2d119c82d62975840302871978dd7a0309f8e3bcc132ed48e` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/modules/musig/session.h | 861 | `c256c3742a68849520569845640f152a22a4a8c21a96040cf0c1054516983980` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/modules/musig/session_impl.h | 31530 | `ddcb0d007ebaa3ccf9611de3671c8551ef93e7f33b588d27156d42a95bc46ede` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/modules/musig/vectors.h | 37797 | `c7cd9dc3804d864d17e43c5b00335a405a3bc4a30861838ac4599a213231e132` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/modules/rangeproof/borromean.h | 1167 | `204588b38d00b1db3765ab4b2c25e01f5afb5f5920a380cfeca381ace064377f` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/modules/rangeproof/borromean_impl.h | 7977 | `4e1e6b782851715a87440d62bbfbf7f6db6d292dd77a00a43e5605233aeada6e` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/modules/rangeproof/main_impl.h | 5051 | `5403c2086d4b81f9e85a91f2290cafd3234e111fae7adbd065a2f5eb78adae82` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/modules/rangeproof/rangeproof.h | 956 | `a8d6285ada07204cc46dab26087b3c61b732c3b37cbcbbbcb793a8705f0ff80f` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/modules/rangeproof/rangeproof_impl.h | 26166 | `94685312146bc3ac7ead5f4a29cddf7d9c51bdb2165b1a27af5ba2a0a6814137` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/modules/recovery/bench_impl.h | 2320 | `20d13192a4aabaa52ac4c2a2da772d8aafef00773051836b25faa2816226b386` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/modules/recovery/main_impl.h | 6153 | `93fb7455adaa364a3c1f8acef82ba409b88a49f688dfe23ab8555510fc614c96` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/modules/schnorrsig/bench_impl.h | 3795 | `9655992c7fd214231623716a738a1928e24a86b4bcdd909f331712df800a1abc` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/modules/schnorrsig/main_impl.h | 10970 | `138c330969201f4d7ff5eb512715b7e05665c3ab4f6d5d9b4172a41aa7c80164` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/modules/schnorrsig_halfagg/main_impl.h | 7991 | `ba7c408bf639159630920933e29fb97be7be5ebcbf978716f8c0b839ed4e6ffc` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/modules/surjection/main_impl.h | 16513 | `5a8dc46515e1a885f221fc8c036ef08c219a2d211fd403b86b482f4ef15904fb` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/modules/surjection/surjection.h | 1066 | `9ed963634320ce5779dfadc4543cea15493722b7b70046692b520e8d78fde2de` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/modules/surjection/surjection_impl.h | 3758 | `96034d371d002e572e6e3e7b79aadf3652f13746cc17713846c62099ac7ed2c7` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/modules/whitelist/main_impl.h | 6398 | `a6cb604aa66933d4c5bc1b8e9942eb2c8ea8fc5efb47743dbdd03f07dff1ff0b` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/modules/whitelist/whitelist_impl.h | 4653 | `6d5bfd9b6dde5d1186c0c886f3a8935b8f30c137b447c19226796b539e2adf9c` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/precompute_ecmult.c | 4017 | `8085ea86390eab2afeeec8b4f952036492fb81606dcd7bb038f940924b1b8400` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/precompute_ecmult_gen.c | 3864 | `23d1dadb40296d2752d024678e405b18d5c904fbd61d74598df3c8005ba64d2c` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/precomputed_ecmult.c | 2409168 | `1fba19c482de09f566ed9e7bf6a526e4edb59a1cf38218e3ab413000a0e0deda` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/precomputed_ecmult.h | 1585 | `d792b8a49759deff5f1e4092558fa9ae11d24e02695e44bee63a8f0ba8e18503` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/precomputed_ecmult_gen.c | 259715 | `c0a7af0884b7b07962be67e9da674e0d75a8d412d116153b8eae2a9e5527d401` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/precomputed_ecmult_gen.h | 973 | `8f514bed441bccf7e34ff05ff49d3a44e9395519a8fdcf176e6aeab7b5dbd5fc` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/scalar.h | 5729 | `87fea4d072b4db4a093527e7df75b654e66cc89202c07a7f7d20d44c12cb0f65` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/scalar_4x64.h | 801 | `42aed583b28bda7982c54a6f63e50c0ae5f9c27d5f66d92ec6bf6c90e765735a` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/scalar_4x64_impl.h | 38294 | `61d0fb4bf51c36819bb778479e7735605d64f8a23073c53afbc3c1eb14f4080d` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/scalar_8x32.h | 725 | `0614cea113aea88a47ef3b2ba8167722e850d7b2a696a4f16b03ec9a320ef1d6` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/scalar_8x32_impl.h | 32526 | `2fe7d67f3218e9fd60fc959a302571e7fbed0e302ed53ec8a3d797f629f6650d` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/scalar_impl.h | 12113 | `6ba654bd4edc0349d1d7f1dfc25ba2d73dd9f2ecdca8078e384bf7b7837d663f` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/scalar_low.h | 1135 | `3cab20db10224ff85ee7c6d975d2968c1370ed8e96ea26b94650f6e2bac31ac4` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/scalar_low_impl.h | 6258 | `c7c73a26dae95abd861b7927e5c0a1add5dd7efb20de69b3e62ff24987170206` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/scratch.h | 2224 | `4af5e1ff665c0418bcc5b1c2de954e7b377f9bdfdd4309e0296938918fac11ef` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/scratch_impl.h | 3677 | `294a55d429fa4cc9dec46ade345bbb2bfdff4055eb1cbf1ba6168a23e5e74db6` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/secp256k1.c | 34307 | `825b8e74f872f89ebd4d7bd3e404a889cf9e0efb1bf6f3441a502b9e15de2a31` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/selftest.h | 1494 | `d695cd5a7369b372285ba0371edb6bebdb3dd79b719af336c714a3013adba6d3` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/testrand.h | 1950 | `bfe1b9a78209aa90d5652a83efccf633bbd874ed72dfe523f2ff6125f97ceba1` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/testrand_impl.h | 5786 | `ac12496cdb04f5432b14dbb60ab464317669532fffa5b1de327e21075f01dbb6` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/testutil.h | 4945 | `5a780fc16fcd8549ea4774d15beb2d36c6ad9a2ca7180dd95f84199a2863d1ff` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/util.h | 16482 | `a203e19a64dc197ac051aadad15163515fb013ea37dfb8d241929bea4cd09ba7` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/util_local_visibility.h | 402 | `d47d4a58f40157ab2a298151f366c5ebec8f7a1e7aaba88e36b530b1c01584ca` | 0 |
| components/libwally-core/upstream/src/secp256k1/src/wycheproof/ecdsa_secp256k1_sha256_bitcoin_test.json | 299012 | `1be8742064fec73d670339f0036dec56b21baa94cb2d8e0fbbb6fb480f733869` | 0 |
| components/libwally-core/upstream/src/secp256k1/tools/symbol-check.py | 2416 | `1706069df728c1a2ac1d2578897076713c16eed73315be6c83ad9690007bca70` | 0 |
| components/libwally-core/upstream/src/secp256k1/tools/wycheproof_utils.py | 427 | `9f2c2368953eeb3c9b7c3b31a807cde76b3106df93fbb975993638d5eb1a1e8a` | 0 |
| components/libwally-core/upstream/src/sign.c | 28672 | `9e52718e9015f768784b457a4401d17c9d520b772d323ea87d6c8c69dbbac168` | 0 |
| components/libwally-core/upstream/src/swig_python/contrib/aes.py | 2010 | `a908a69ec88322237a640666b30549f7ffbcfbb6f1161fc27b7910e81718f28f` | 2 |
| components/libwally-core/upstream/src/swig_python/contrib/bip32.py | 2642 | `3f656b4c9cf631614cc98b3bd4fb86e83d25ec396af121a26da6f76715b1e888` | 0 |
| components/libwally-core/upstream/src/swig_python/contrib/coinselection.py | 865 | `e984a050ea05ed45367d0b9beeb21b25a039575b88fb56cfe9dda90cf30ded75` | 0 |
| components/libwally-core/upstream/src/swig_python/contrib/descriptor.py | 1238 | `293f13173b5700a5670f3fa59c09320769473ea577340fa1cbf4cc5f2a31b1d1` | 0 |
| components/libwally-core/upstream/src/swig_python/contrib/elements_tx.py | 8121 | `f7ed910ed53a4ba8f0cbc4cf65f2f998b8753d29f3b732716a2561432e4c0d4e` | 0 |
| components/libwally-core/upstream/src/swig_python/contrib/mnemonic.py | 1913 | `0affbe17869a1d77bc388af7b61d71b7eadde358f9804fb485c40ace73390f95` | 0 |
| components/libwally-core/upstream/src/swig_python/contrib/psbt.py | 42984 | `de4eede31606e8bf3e7bf885648765a1214fc951bc83ad5e42f8732e7827e41d` | 0 |
| components/libwally-core/upstream/src/swig_python/contrib/reconcile_sigs.py | 2854 | `0160b8f879594d0c33c9e08e0e0699e3d65a797d504383c3d2b42238d503b087` | 0 |
| components/libwally-core/upstream/src/swig_python/contrib/sha.py | 2019 | `3a36b14987e4051ba544d89424b76f37bede9b87791f33b27bbb046dd10f813e` | 0 |
| components/libwally-core/upstream/src/swig_python/contrib/signmessage.py | 1589 | `62c57fe76135de42dcd48c08bd33a0165ec566ad5610e58e9fe636723ecc3414` | 0 |
| components/libwally-core/upstream/src/swig_python/contrib/tx.py | 4916 | `23ea1bea593ab10be4a4ade0c979ddf184b577016f802a49aded92238c0f8ead` | 0 |
| components/libwally-core/upstream/src/symmetric.c | 1767 | `746f5c8d602544e0db731e54a287703536d6b462747001dff5122c2b10cd458f` | 0 |
| components/libwally-core/upstream/src/transaction.c | 124444 | `c9e1504610735267d7048c56d49da1935a29c128eeb10d9d0b7416a9eae23619` | 0 |
| components/libwally-core/upstream/src/tx_io.c | 38747 | `a3d59555fa1f81286d92027853842c8e1d09400c745220ac7541cb7cedb72503` | 0 |
| components/libwally-core/upstream/src/tx_io.h | 719 | `9d25152580f4b1d41d7e6f6b372a72b2e1df8cab6072bd79dd94b0b4fbce5b11` | 0 |
| components/libwally-core/upstream/src/wasm_package/package-lock.json | 126902 | `7f38f77a6cff50d36c4be0c6c88df743fc3ef0ee572c212155c9cf33bc88acf8` | 0 |
| components/libwally-core/upstream/src/wasm_package/package.json | 608 | `f1c0400fbd6b50d7866ede0d6c960bacfaefdc9fd9d0f9d76a422ca3353bd424` | 0 |
| components/libwally-core/upstream/src/wasm_package/src/browser/assert.js | 321 | `67e799d7b585943af24ff3d31d5d25b556d3f94812d2219d3eb703a472f4b82c` | 0 |
| components/libwally-core/upstream/src/wasm_package/src/browser/crypto.js | 114 | `1a0550b75fc50491d16e6564434529adaa5e77b60cc8abae1dade004b0d71e2d` | 0 |
| components/libwally-core/upstream/src/wasm_package/src/const.js | 18459 | `10b0567bdac844dec0eb80607e7343982967c900182bfa01d9bdcd6f37444f91` | 0 |
| components/libwally-core/upstream/src/wasm_package/src/core.js | 11103 | `cdd31896d2aff07dfa172e62b63c0d6c7d68f6fe69eaead859a1fa13297eb3ad` | 0 |
| components/libwally-core/upstream/src/wasm_package/src/exports.js | 110 | `95b7045e0888c44564dbdad98a4a97d10162767c28ace45a58a31a5b3f1fbf8e` | 0 |
| components/libwally-core/upstream/src/wasm_package/src/functions.js | 117722 | `bc0c2b8dad4780ed4a3232db0d0b00976071e84e59cd7494098bc050f34fa33e` | 0 |
| components/libwally-core/upstream/src/wasm_package/src/index.d.ts | 94390 | `e6e48634893b92ee0f07069971ab4d859e019c2fe8f0725380bbbc0236848692` | 0 |
| components/libwally-core/upstream/src/wasm_package/src/index.js | 644 | `e604bf7297be553a02b5a716288bb479d6b39571d3302aaf7c4da52c3a034acc` | 0 |
| components/libwally-core/upstream/src/wasm_package/src/util.js | 1217 | `34e03d693697456630eb3a9db4d8f253271b6536e0fbb7d6deb725081d715ffd` | 0 |
| components/libwally-core/upstream/src/wasm_package/webpack.config.js | 458 | `9a861d818ed3d7e3b9cae555eb82409c4acc722153ca7d8a0f1089e389e61304` | 0 |
| components/libwally-core/upstream/src/wif.c | 5335 | `2e01925997bcd34600c7e6e7e8831120b157fd13707a4897f411afc3c260d084` | 0 |
| components/libwally-core/upstream/src/wordlist.c | 2726 | `d3f630d36f8a7763a67daa88b7652ed40f77540302597574b9e059d234ef5ec2` | 0 |
| components/libwally-core/upstream/src/wordlist.h | 1678 | `7e8993598f450d95843cd4217f2d4fcfccf349a7464a8bc9dc0457c79a84f5d7` | 0 |
| components/libwally-core/upstream/tools/build_psbt_ctests.py | 854 | `ecc8332fc3ea0a904897ba05598608e174a64d02fdd77be821920a983c249419` | 0 |
| components/libwally-core/upstream/tools/build_wrappers.py | 26927 | `b59803b7ca9b045961bf6f446dc6c1d24b8c7b8c82fb9cf007299ccdad9c6f35` | 0 |
| components/libwally-core/upstream/tools/wordlist_cc.py | 1736 | `e389277f851b59a3d4167ffec131903087ffeb646312e49949691a67260b853c` | 0 |
| libjade/daemon.c | 13786 | `f7a879446d031324ab8a7c6f3852fe798423a27ce8836e3c31c057d1605021b2` | 0 |
| libjade/esp_camera.c | 4097 | `2dd75df9a8ea04009e2292489933d9fcf3d34cb00319c9279ab88d58cde13524` | 0 |
| libjade/esp_event.c | 7180 | `232359c418327dc712fe37fec5925be3f4376903e7cd89af152193a8816db56e` | 0 |
| libjade/gui.py | 33303 | `83bac459603739e79701326b723f64519eedfa82234e5ebd9b12e115f2fa5a5d` | 0 |
| libjade/include/arch/sys_arch.h | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| libjade/include/driver/gpio.h | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| libjade/include/driver/spi_master.h | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| libjade/include/esp_app_desc.h | 199 | `91d86dc8cff605493b74d674ebbc952013616e1014c4addf10c539f27efdb9bf` | 0 |
| libjade/include/esp_app_format.h | 110 | `bdbc9e3ed96e60b8ae18596b13293292637dc19774dcfaa4a5c89f9b77f9d155` | 0 |
| libjade/include/esp_camera.h | 2691 | `dec13aed2560745cced0c231bb50400c53cbf7d6d1c154cc3cbc02ab8e493d70` | 0 |
| libjade/include/esp_chip_info.h | 210 | `6a640247301af5c1544d439e9b4fcf26e8cc70ed71e6706a858145ae7f213174` | 0 |
| libjade/include/esp_crc.h | 223 | `bfd084c9d6b84484f924da49dd455483879154c6fb5e53fe366435ecabe3d664` | 0 |
| libjade/include/esp_efuse.h | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| libjade/include/esp_err.h | 345 | `42989c30b40bc2ce4dc91c1fb3a22d7ab528d762c6cafc98eb4243b7b7865aad` | 0 |
| libjade/include/esp_event.h | 1178 | `025b67230b51a1a2a82ca7203f0644fec01a368abfe1725e102e9787bee767f5` | 0 |
| libjade/include/esp_heap_caps.h | 1073 | `7b0a2298d9aac0b4f4aab1792c6c2f189e361b2bb83cb0f98cf0c75f7cdcf309` | 0 |
| libjade/include/esp_idf_version.h | 153 | `6853a6164c0590cfea0ccba19e580a18ca0c4d34ecc80e56ffd18daf88bcb679` | 0 |
| libjade/include/esp_log.h | 2829 | `536f591ec2787696398452c2ede62f0a325ed4a382762859a19398b28eb7573a` | 0 |
| libjade/include/esp_mac.h | 163 | `8b3ef41835b640d41502fcaf251b127737cdcfd3a8c1629cd53004d352f37c78` | 0 |
| libjade/include/esp_ota_ops.h | 1359 | `ac9147f3061e1552a023fb091f98a1fea94ef81ff5ea256127cfeff6051fcb59` | 0 |
| libjade/include/esp_partition.h | 603 | `ba52b5f0a106e4fe45c6a6d40b0a432e9bce9096999a3f1730b06045d9dddba1` | 0 |
| libjade/include/esp_sleep.h | 129 | `714e5d29e39de498e4e5fea7dfd7d48971c9628e8e8aaf2df01593639e54132f` | 0 |
| libjade/include/esp_system.h | 119 | `7433510b853e2aee76e094c0777431eefa692f7f10caed4379f51e8e931b1965` | 0 |
| libjade/include/freertos/FreeRTOS.h | 173 | `d396cdcc4f08e165f974bf7a7531e645e4099a998d46de2049edc7b23290a9c6` | 0 |
| libjade/include/freertos/idf_additions.h | 399 | `1421e9defdcbdeab90ae75a5930d5b8dc3ba00f9b8e039809903d7f08891f635` | 0 |
| libjade/include/freertos/projdefs.h | 260 | `39375a0187d7e96877292534c011376a07c938280ec1fc321f4e332a4b8fb28f` | 0 |
| libjade/include/freertos/ringbuf.h | 3484 | `5372dd67671bab23bede2abb75bd29ea496d018ccc83eefab785fbb54de649d7` | 0 |
| libjade/include/freertos/semphr.h | 3637 | `e4e90504e643d2a7ab1781a0a9968e02320ac1de854b422df0bb774bce5ff231` | 0 |
| libjade/include/freertos/semphr_darwin.h | 4571 | `63e6beea3c49daa4ad8d3ea36f710a4ae5e1480f78250e50a84d0635b42d07bb` | 0 |
| libjade/include/freertos/task.h | 1443 | `cfefd801a2183bf91518cb31c05c14a27f674e5ff6a07b1f371bc99b1d0bea6a` | 0 |
| libjade/include/freertos/timecvt.h | 1278 | `3ce86cfd1cf226da9a45b94a52eb287773ac2386dfd0ae4d3bac08c119305c16` | 0 |
| libjade/include/jlocale.h | 133 | `d082d6fc1f54bb2e4293df4c07bf2b913266c936b2250f02214103d97fab392f` | 0 |
| libjade/include/libjade_port.h | 1472 | `ec5e392b780f7842c48506bb308fc9e47acb36e4419e8a84caca8bdd0359a98d` | 0 |
| libjade/include/nvs.h | 92 | `fea28e5ca7d2fe5973f6e8cefdc982958f40ff5118192dec9ffe087807197f74` | 0 |
| libjade/include/nvs_flash.h | 1999 | `a155f6dfec622f88f08939da808fd662cf8b0fcfa382e79ad662ab7cea040913` | 0 |
| libjade/include/sdkconfig.h | 1133 | `44acd257bf5c3bd6c5237a85ab0c73b4b789c03ee094ff1daa9da8bce58c276f` | 0 |
| libjade/include/sodium/crypto_verify_32.h | 250 | `044b7a02852f333fdc1db96edb29747cf99f88ee60e21cfcad8887488cd53b9a` | 0 |
| libjade/include/sodium/crypto_verify_64.h | 250 | `a8d8acf4c3fe4df0d2bb8660fb8fa20be40ce0e12e06baa179f80114117a68a5` | 0 |
| libjade/include/sodium/utils.h | 210 | `7ef7d329ae47eb7fab7e6bc8d76c533c2e8064f694a2dd529e184897403fe756` | 0 |
| libjade/libjade.c | 15927 | `804d9d5bb845f69067b2a3e393cc605031f4080e981e9f76ea96b922929cc3ce` | 0 |
| libjade/libjade.h | 1401 | `cebd1bc02d72cc810cb7e0f372006b1998120b2ea877148e4df5233fb3492f22` | 0 |
| libjade/make_icons.py | 440 | `3cfbc4d0df1e563be89fc43e1781e1340f6bb3d8eae7b2d47ac1cc5c576bddea` | 0 |
| libjade/miniz.c | 94568 | `9b6ea606485c1ce9e1155b11e3d86710a4fde42127f3069cec47403e1dd928b0` | 0 |
| libjade/miniz.h | 33110 | `2a2c531f30ae3d6611c8956135a6d6cb8150a1aa2ec9447e9d55f83bb9fbe2f5` | 0 |
| libjade/nvs_flash.c | 8819 | `2dab1ea45e332ceeebeb1fead3d222667a9cecb6426d06ddc14dbee11ad22be0` | 0 |
| libjade/selfcheck/assets.c | 3680 | `b6d0fcf0640be91826ead9d811ab732f680c4a79ce3abd03365c2d8b37d19c8d` | 0 |
| libjade/selfcheck/bcur.c | 18883 | `f240136dad29434b390d8e214d682ac5ed73c6ca92f081cdab95da3be0e984d3` | 0 |
| libjade/selfcheck/cbor.c | 2740 | `f9e6cc1b46f0669504c55bb2b84d0fda748048d36427a8ff195e9f33fc1e9e3b` | 0 |
| libjade/selfcheck/descriptor.c | 23625 | `8fb673c7ba9825eb07d5a3c804c0320111726529d3f36d640af009445cfa22e1` | 1 |
| libjade/selfcheck/task.c | 3777 | `2cd922f9d11b3d1e35e4b1cd7086179fa30620673ee82e100810208549f9e0a5` | 0 |
| libjade/selfcheck/urldecode.c | 9085 | `952e3646b3aa5cfb9876921eaf6746839597f9a714347d56fb8a324680dd1bd1` | 0 |
| libjade/task.c | 14246 | `cffbe18f86ce557fe1fd87ad5c709ccbcbf98a87558c1350abfbadf2cf1e9909` | 0 |
| libjade/tcp_bridge.py | 3297 | `f53615430e1d62c23859662b383eaf4426dd1cc07f29c4225978104e40c5999f` | 0 |
| main/aes.c | 2577 | `cc9a126c7be550237fbd6b27f715a486e96a301e432ae9d6d23a51e9a4f00942` | 0 |
| main/aes.h | 802 | `49bec702f79dbd7d5d4a0095b126c263144410e445ae1be71aad27e01e1a7d37` | 0 |
| main/amalgamated.c | 5318 | `5e3b8981f49e16b1b72264eb4ca9a2c1f3d24a0802ced2dd3e21dc3aa2d36378` | 0 |
| main/assets.c | 10345 | `884bcab009426af20ebe5cdbcc363a89e7d30911be188ec1bb3c3057b271ef04` | 0 |
| main/assets.h | 1071 | `a80600f9c7f8fad97e9278a76eb507d70095e8b4550373292badd17090489c74` | 0 |
| main/attestation/attestation.c | 29559 | `109fb6032a9e94ab16af11fbdcaab65966f8bfa8504d3211d125816daa9586d0` | 0 |
| main/attestation/attestation.h | 1262 | `62b25a73c9ccfe3671d11c836620bbc9c1098adddd8b010a4ac78bffb0584ce0` | 0 |
| main/bcur.c | 33709 | `71c649ab160724204b8942429bbebd8f596db56484fead3ac5698e22311232c8` | 0 |
| main/bcur.h | 3404 | `7365bb4b7cd9a9dded0662f1d560568c6189f5258c7f7321fe29dc8afa271eb0` | 0 |
| main/ble/ble.c | 33067 | `e1f41bac969eb61fdd048f1c67a5e8d0a897362af5403679816f1ea8993d4719` | 0 |
| main/ble/ble.h | 846 | `57357773fe66db5f2e5cbc19a7f740238641820dae232cd96fcc107169398686` | 0 |
| main/button_events.h | 7009 | `72f3d0a7a66c62d5b6bb47a9fd8262302cb1e926f0cc66b8adb841c9c909af7c` | 0 |
| main/camera.c | 26492 | `5980e68ee7592f58aaf481ade8a80fab7ba89ac23a97992578fcc1ea9fd7f574` | 0 |
| main/camera.h | 2229 | `5bd4c26b6cabf613409bcbf5928a1c60acf915df6b8642e1e0e6af47610333c8` | 0 |
| main/descriptor.c | 30078 | `81985445c447d2314ad3fd3d3bb35ba19a0490e83b2bf0081dabb1673a11a091` | 0 |
| main/descriptor.h | 4566 | `639e67c90b499e92f7f1f88f941953419f03d3ec1b3cb3511110467b4dd0dd50` | 0 |
| main/display.c | 31542 | `1d537d51c1c3f7a7056c86856092f5e84847eb6449eb61a162e6ce432055ee9c` | 0 |
| main/display.h | 3421 | `68f42884be36496804252efb8456c7f8f540374774d736b48213724c6595dfc4` | 0 |
| main/display_hw.c | 14900 | `208256db8356a502065fd95d846f3fd59b4ea6121ce7e774ad2407bd6a7857a8` | 0 |
| main/display_hw.h | 508 | `777d9b714ecc0057fa9e03a17d978dfc4a51f6103d022e13f488f8fe13a43852` | 0 |
| main/fonts/BigFont.c | 19732 | `663d44895509eb139ffee9384db9e1a3fc4ee252f2f3706ff626c67972539c57` | 0 |
| main/fonts/DefaultFont.c | 10068 | `4786af48b658f7e44359236665830c5e488489e2bda35d2eebf914c80a7c5099` | 0 |
| main/fonts/DejaVuSans18.c | 13737 | `9e1316d88900d168bef760941843e5e811b5e067263bf94d1e9f42ce1d6c4438` | 0 |
| main/fonts/DejaVuSans24.c | 20500 | `4151ea519d38c7f95214ec30558f579435d6057a0cac810a3a06b5de0763b39b` | 0 |
| main/fonts/Retro8x16.c | 10239 | `f2e52ea1783a24d45af641fc7fe44a0e2d3366f72363afdf37148f57b1ea2166` | 0 |
| main/fonts/Sinclair_M.c | 19738 | `9b9720a19ff7b1dbde6093ce0cfdabb2c017dc7b2d6258eeb9d4253b40b0fe35` | 0 |
| main/fonts/Sinclair_S.c | 5674 | `4f0fe35115a3d379c910fef96b5205f1e6721776ea66202cfc48eb6fcb59d0c8` | 0 |
| main/fonts/SmallFont.c | 8209 | `51d60606ec2e687d505314fa6eedc72940e2471333b10832404b94be97f1287f` | 0 |
| main/fonts/Ubuntu16.c | 11651 | `c3c604f1beeb95251063b8c6c16233ae98e4b3a95ad23b57c3663183886556d0` | 0 |
| main/fonts/Various_Symbols_32x32.c | 76386 | `728647e3f9be98442e85df84c3765cc4368c388e74d7efb6f29caa15fd774fa4` | 0 |
| main/fonts/battery_24x48.c | 9261 | `258c579414b1001f2e6f1a9a4783ee8b20107f4c5637bcfc056cf7b321ad9296` | 0 |
| main/fonts/comic24.c | 20269 | `06eb7dd9c117b59154c500e9d59f33ee7fdd8e1a512dd1a44e106b881ba7ebb8` | 0 |
| main/fonts/def_small.c | 8577 | `d4202e5dfe6c3e69249f7875c03ca85e6a3e3174f78a0d13f011ef9c5813a436` | 0 |
| main/fonts/jade_symbols_16x16.c | 7691 | `c90585ea9df24bc4d562a85cf2ab6ec07a6930d18aad9ef786dde2e8d7ff9cff` | 0 |
| main/fonts/jade_symbols_16x32.c | 8452 | `44d914a4371de44e0e50e9435ac01093f86d755d4bd9d38577f0cda4102c46bc` | 0 |
| main/fonts/jade_symbols_24x24.c | 3381 | `803ae20ecbdeb75d86b4976abcf17a5412435caa8ebb44139ace646fbfbf56df` | 0 |
| main/fonts/minya24.c | 20253 | `ab78406f29ede3ea4b2904d32e1b01be5e970fe98315151f568788a13be3af23` | 0 |
| main/fonts/tooney32.c | 36755 | `bbaed9670759c8df1d98ca5f40977731695822506e158de422e6f6a7cc332e83` | 0 |
| main/fonts/various_symbols.c | 19771 | `e61f4091679fe50badcfd5f6e99652acd40044e9c4067cdcbe939cfd2f73c638` | 0 |
| main/gui.c | 106393 | `9c7b0771bc38bf80564d562273bb6c1549f30b4cd386179c6f1e7a4e9642c158` | 0 |
| main/gui.h | 16914 | `31c0755842f1d159f3c08e65ad1d54c1a7a66910de6116a3a8c2a79b4764f822` | 0 |
| main/identity.c | 19077 | `61059fdd5caf7e8236b18424591656cb56821b1349c1bc56d64570bd12229e10` | 0 |
| main/identity.h | 2296 | `cc5c1d0a6f9809e090fda870b683cc6ea0d55c49a87dd9cfa87b18c9f025e422` | 0 |
| main/idletimer.c | 9634 | `fd3090c7a71f9d4c396baf8b5bac86931969e35f68d944724347957c183d13c9` | 0 |
| main/idletimer.h | 249 | `dc55b5f0d24341f66247ad56f88a45e02eb91639df4fcd36df8526a9ac3bd250` | 0 |
| main/input.c | 595 | `abde01fe56c425c7f95cf6017eb870eafbf14f8897d727d2340e697125a49d28` | 0 |
| main/input.h | 81 | `25edf47c16e5569a9b7bcea838d2e4371d2d70292daee9cdcdb305e167719781` | 0 |
| main/jade_abort.c | 1545 | `e500f0952405f3443b8ca8d4ebae36137c99e14ba1f0907fd578c6f964f425ab` | 0 |
| main/jade_assert.h | 7244 | `8e2f6ec6b883ff3357d04381d912dc06ff4f0f6be1ffe6f6db87039e09d0089f` | 0 |
| main/jade_log.h | 430 | `031cfd4fe846aa37be2cfeb37ea9584fd93f3f9a69cc2eb5d4a9babd9bcf6cd9` | 0 |
| main/jade_tasks.h | 1193 | `2c2b6cbc8004fb5db54eca9a5f82265c228b460940c1081859db0f2824f72cc9` | 0 |
| main/jade_wally_verify.h | 693 | `aa4dc137a8a11fac416641f3d5525cba6c5ff0347d5d3f961870e35bedfbada5` | 0 |
| main/keychain.c | 26182 | `73e309e0c6c62dbcd90021db04bff0f5629105faabc40157c613fcbb0f152501` | 0 |
| main/keychain.h | 3092 | `5283bcf2460992938c5e0bd25f88c0cd61b6d847fb867003fad92ab23abff768` | 0 |
| main/logging.c | 2831 | `7681052739d1b4ab49a26eddfba5daaec2e76324f69225fc97e02fec15ce4b46` | 0 |
| main/main.c | 10371 | `ffbeb1491192c7be16cf1ca3f12a1896ac01a434429f5d73ca3272523542f975` | 0 |
| main/multisig.c | 27403 | `ad3b2fe43a0a531aa916a69ae77b378256c2e61643653b8cb7221047dd73a93f` | 0 |
| main/multisig.h | 4197 | `f1d1cbe6dce6f1dac7c790e02fd272811ca3526af1b86cff790a0cd319433cf8` | 0 |
| main/otpauth.c | 30114 | `da1f2217ba05ef1b5c5b80f155eaf2575e9f8aa3487419f40bbc66c2b175ce92` | 0 |
| main/otpauth.h | 2538 | `b28590eb82b20f88f9230141b8e4ac5711c847471f483e7499ead2cf5f7fa7a7` | 0 |
| main/power.c | 1744 | `c1153c8adaa9dde69ca6206ab6fdb8aa55e3c66fd65a35522c4f62d9ac53aaf1` | 0 |
| main/power.h | 907 | `337a0674fa7a49698cdc64e2e6a035507fcad1e12225c8dfc579f328c34667a9` | 0 |
| main/process/auth_user.c | 19586 | `0379d767bf64c8b99dd28b8f629d515e06331c4cfc6ca8c368bbe46457897709` | 0 |
| main/process/dashboard.c | 112704 | `f07a5a347910bbcdd4ec852327906e1c3abceccfcb5cb4909584a6dd55f1b3dd` | 0 |
| main/process/debug_clean.c | 2765 | `fbfc93f503c64502461f60e619f233f72422e1677d8f054c4c105f04c9df31bb` | 0 |
| main/process/debug_handshake.c | 5924 | `118f6d105d4b762a674d90b8cb31b09828dc129f5d3c437b4cc3fe3a64cf69ed` | 0 |
| main/process/debug_scan_qr.c | 6890 | `3a49e44f207a6462197cefc167789de00580e4105fe07844e1f19c431a7b8297` | 0 |
| main/process/debug_set_mnemonic.c | 5198 | `617984672ee4e7323d596062da494fd90c20a601663efa9e50dbd90566a6ec73` | 0 |
| main/process/get_bip85_entropy.c | 13579 | `a6fda19e47b899e0206e5262ea531970ed33c4aa520bb69d3a03cd4f8d762e46` | 0 |
| main/process/get_bip85_pubkey.c | 1316 | `9b919409523ec203f5b65df60a6bed904f4eb43a7aa1d7b5836823041c8fa2dd` | 0 |
| main/process/get_blinding_factor.c | 2825 | `67b1e5ce79c11dcbaf7a2d4965aaa026e3f461c11f1cdb93e4e0e4a73ae0779b` | 0 |
| main/process/get_blinding_key.c | 1831 | `3f1109641a7439c8d23fe6571e30269324364f81f16ddf213432c6f8d90d1cc6` | 0 |
| main/process/get_commitments.c | 5486 | `220d67c6e562634b7264d5dd4f1835d70ad3e8363eb21ef83c5bdf93877dbbad` | 0 |
| main/process/get_identity_pubkey.c | 2238 | `d687e7066ff605b7c37387632c747fd4a968dd0f287908dd36e3ae8d25bed2c1` | 0 |
| main/process/get_identity_shared_key.c | 3180 | `243cd8e3b2c5773f83ae15ffd5e477cc35a8b224c61c916b48dcff812f599943` | 0 |
| main/process/get_master_blinding_key.c | 2254 | `59a95842547b73bb6a559367f7c72b9f7f4f1f57f69cb58a5901ffe9e55d3593` | 0 |
| main/process/get_otp_code.c | 3725 | `27526eb95637148583a44992dbbff520fb1d0b98cff6d6586ebb42542ab71b94` | 0 |
| main/process/get_receive_address.c | 12607 | `a10e79d45374e7c4564e0fa6398850b7229e6cecf5ab06357483ebe73f24db82` | 0 |
| main/process/get_registered_descriptor.c | 4059 | `4afc6b5ed7a4c9efd4f9e6e7da8aca67ad916617d28930e16cc0a3242b56476d` | 0 |
| main/process/get_registered_descriptors.c | 3917 | `f533398692a49681212456ecc360b6ae1ae610c1ac857d048d87281bdef05e11` | 0 |
| main/process/get_registered_multisig.c | 7658 | `dd8d7a58913988701271dbe920106b7685c23cb102b0e3b13595b10432f4c239` | 0 |
| main/process/get_registered_multisigs.c | 5150 | `001f918539dbda9591cf710ebf25b5552ff385ab1205473b9a02fba14ac2dc41` | 0 |
| main/process/get_shared_nonce.c | 4626 | `d4280140163dc732d3a51566944e9e65d6d344fcf95f28f1f57710016db727c0` | 0 |
| main/process/get_xpubs.c | 1550 | `da4030c24a625538b79fbe02cf02f584bdecd58b519a824e34acb4625cf6973b` | 0 |
| main/process/mnemonic.c | 75565 | `d36ee56949ee52422b148685d056be9f673afc96be715f44d13447380ac1ba99` | 0 |
| main/process/ota.c | 3410 | `de6f4e915d4316a3569fe3288dae1d5e97a8a75c215a2464c43ea3f147d25059` | 0 |
| main/process/ota_defines.h | 2417 | `8e6f1399e10a7626e527b09dbb1f2cfb81de8fd6db7f253b88eaae90d840f18d` | 0 |
| main/process/ota_delta.c | 7711 | `193538cdbdb3a1d85577f534a8a59ba7e343ae4c818f9032cff593d9c2614f4a` | 0 |
| main/process/ota_util.c | 18857 | `c45d9bb4b24c5c35c22918e763bbd41a83a341e46089dea0b8783f181d8bd34a` | 0 |
| main/process/ota_util.h | 2644 | `098bd34e48b2e6bc75fd90a5df8a26d7d657256999f1562e91448b50fb35fa1a` | 0 |
| main/process/pinclient.c | 24785 | `541c57ef78078aeb565636c58b6e00abf8f51bf1ca9b763916e0fb7772c863ae` | 0 |
| main/process/process_utils.c | 22504 | `71028ab9c16eca06604bf53d2fba1489f6b3c28b35adef12f65fec7b1ea84b2d` | 0 |
| main/process/process_utils.h | 7881 | `1d220d075567ef7dd43d1fbb3d8a457e2efefc50fff5cb318256487f8c478e96` | 0 |
| main/process/register_attestation.c | 3488 | `6e292d309d56a078aa7eff0a7ebfa013c554b31212a8c01af3041a8fd6457d71` | 0 |
| main/process/register_descriptor.c | 9695 | `9d83a4f3d94cc7b8c6230c5544f77b25ccc78164399806c6e1b7ae9ff3b4cdd5` | 0 |
| main/process/register_multisig.c | 28846 | `e0048239f36c3e503bcbc622c5f3cecd357f2cc8df31e15a06286c9661f884c2` | 0 |
| main/process/register_otp.c | 16858 | `fea7399f1d0c4714cfdcfd57ecf6f91c947d6d72d74ddcca4207ba2ec2574d83` | 0 |
| main/process/sign_attestation.c | 3898 | `b7e02234b2176ecd30479ea85d1961aa500fda94593235b30a42124aede8eac2` | 0 |
| main/process/sign_bip85_digest.c | 5513 | `40cf03361d9c783feefd3ce1293e99b27363dac34a9ee338ada2133fb6977fe3` | 0 |
| main/process/sign_identity.c | 4081 | `3beb49072c68ae6bde613d5132e07ae2561186a14484819830c281430dcb469f` | 0 |
| main/process/sign_message.c | 12825 | `7d19e713fe281f9c72d17648cc6ab532c4202beaecc71e74dd14035803e96f5b` | 0 |
| main/process/sign_psbt.c | 58170 | `9c1b424fa472cec18cbd1293932e759a7eb5f5c49f294926076b58636e767b1f` | 0 |
| main/process/sign_tx.c | 45775 | `7ce145ef4faa8a1ba4eee2fb3027a280dfc4e2193de543c8db6ac09a6c421986` | 0 |
| main/process/sign_utils.c | 33877 | `179c9d7594218ecc0ac5676c453ac903254c5678401e50349ef4c45fc4ab6522` | 0 |
| main/process/sign_utils.h | 3431 | `fac558fd131f0dd75394e7afa80c42c9c8db32fc20b5a0277f5b78d085e60160` | 0 |
| main/process/update_pinserver.c | 11269 | `207629fe55e21ee8008689f6dff4b19e854f2a65d99c1eb40d2ce53adc3a7de9` | 0 |
| main/process.c | 27817 | `5b14f4bff63c5fe0bbd8748d3dee896f1bb600ef9847a1dc40a364eab4061568` | 0 |
| main/process.h | 5262 | `fef0b8a37b02364b6c4998ad4c38bd31cc8a2fb910ce9c4ac7cd568fcbf3cc88` | 0 |
| main/qemu/qemu_display.c | 9905 | `41be8d08db80de59b284c69a5f37f8638297a9d6a0795d7016d71bb669f8470c` | 0 |
| main/qemu/qemu_display.h | 279 | `2d18a4a60630d521c8f1f39084c9fa2b59ec8cc0aa30774726def8945764bc74` | 0 |
| main/qemu/qemu_tcp.c | 8461 | `467b0d175b584da39c4c53e862f0e4ee3601a1ba6269666cf9bf70190e19c177` | 0 |
| main/qemu/qemu_tcp.h | 190 | `fb748cc0decd96ffdbe5306ebbe6fd96f1fed8db292d26edc364b35244788586` | 0 |
| main/qrcode.c | 37506 | `ad8b8e9ca269cbb0af15a671b42a2ed355c090e504cbf70a695e260e1f436bca` | 0 |
| main/qrcode.h | 3061 | `8d050b24958572ee090ae3b5bc296d676f500435a005d6cc31d62577df515bec` | 0 |
| main/qrmode.c | 74171 | `ae9e0a93c4850c1252e5bdc7908f90d7cd3a46d912642c86202b2a3e5aa1b990` | 0 |
| main/qrmode.h | 1820 | `3400a52b8c0c3efc945340f2321be7885fcbec7283d2bfb5d53b846d211c7ee9` | 0 |
| main/qrscan.c | 7940 | `91e0aaed8a64ecb703ce9ed9e188cb5397f4f01f985afa3905e1a1bf52b1ecc4` | 0 |
| main/qrscan.h | 1702 | `39ded29b251021ccdee9ac80d99e830dd9f1de2c620902ea90fb0c2d2294cb45` | 0 |
| main/random.c | 11518 | `f6ba8919a0bd39348a8964c156aeb20fd9671143c147b1391e2a660afcecb099` | 0 |
| main/random.h | 606 | `da655b362510104a23d8406d7087c0cf4fb1074278e6eda4e3e3b830e7696e33` | 0 |
| main/rsa.c | 5370 | `44f71d31a8560a1d044784e8b04575fc406e850c3ff739b8498e661527687867` | 0 |
| main/rsa.h | 962 | `f395fe5d556a96cea8d327ed6e638a6aca38afbcf7b247d4534295637bad9dc1` | 0 |
| main/selfcheck.c | 17487 | `92a640e51db692fe50aaa3b8f0325ffd4004d3d5dfeeb0708097a8fc29a14fcf` | 0 |
| main/selfcheck.h | 1919 | `3c7dd66cc36179a72dcff7b702c04660cf8c6a12c36895f211e2d1c1329f3f56` | 0 |
| main/sensitive.c | 5212 | `3a765b45b6790fe7860ddaea4c88c02ee9fe6b186b3a78cf6a51078b0c3614b5` | 0 |
| main/sensitive.h | 2101 | `3a63596396c06650a3a12505730e64806245784f195408286ea734eb34a09045` | 0 |
| main/serial.c | 10406 | `7accefddd676dcb18e28812402429a8f51b32ec2cfa85f7d37feff672de11f09` | 0 |
| main/serial.h | 309 | `73bc6fa520e77691571433554ed7fec5f321524966f1fa9f38cdd82f652d689c` | 0 |
| main/signer.c | 3883 | `4172e6d05758443378845b24416de4a537d13833c7420393dface079d4f5dfd3` | 0 |
| main/signer.h | 1452 | `75068372b5e1f0ec4e0f28591da5f056f11fae08a296b19f4aeb31a481adf9ff` | 0 |
| main/smoketest.c | 18884 | `bec571bafd568d90dbf1e75acfe38370774efbf787e5601e246180ca798c99d4` | 0 |
| main/smoketest.h | 120 | `ecd8e7374234f0dea70274d6353cf3a9b5dbd1770b40e0167d8b15bcabc1c2c5` | 0 |
| main/storage.c | 32538 | `be9475e8734a339a1a7fccbaa976ce637a6ee1ecda7ad2c36142775965213aa4` | 0 |
| main/storage.h | 4897 | `c768e8fd83e0e62186b4f22d77ad6847eed3649498df312f2b74a2cc05c76d31` | 0 |
| main/ui/ble_confirm.c | 766 | `6c7f6038060d27cb9198593d597484620fe65ccf404814f316b7d76e6f28a76e` | 0 |
| main/ui/camera.c | 2741 | `da019d3f1f2f451de4d1eadeaa14222bb3358375518583d6637d938fc070cd72` | 0 |
| main/ui/confirm_address.c | 6257 | `4cd1c91d15e27dce32aeb4b3d4142be4b53dc54d4b6a11320c768cba28810693` | 0 |
| main/ui/dashboard.c | 38377 | `467214e13c102a6442edb86909c1aae99c527bff9ef3a5c6073fe6fc28baa6c4` | 0 |
| main/ui/descriptor.c | 15828 | `eb1b0346d3c8c542344e37514e12a9e6b3330e7cc4ec7451313c5c010dd6e45f` | 0 |
| main/ui/dialogs.c | 30011 | `50251b2002baa585763fc0374e3f048093917d56ff3d4b47f93526d398173653` | 0 |
| main/ui/digit_entry.c | 14903 | `75d3bd468463dd1771b8113f6f7cd801e28f36049552e5ec6e58dcb408fb8e87` | 0 |
| main/ui/keyboard.c | 10747 | `ba415a1f5741ba75a36f97d77d110ea8bb6710cd2531c81551bda44816c851e5` | 0 |
| main/ui/mnemonic.c | 22270 | `1b4b58645cf10ac3cdaa20778c89f9b32114f388ca3a3e7857696c84cfb86eee` | 0 |
| main/ui/multisig.c | 15919 | `478de0b242ddb53846da9309a4541dec4c1d7fe2eda52133de09e10f3175bb1b` | 0 |
| main/ui/ota.c | 5153 | `af44d015d6f08b73037bf8e8b2dd92c1df97aa0104b177bb643a41d03ae97d4b` | 0 |
| main/ui/otpauth.c | 13377 | `0c6fe581862a47c316b2ad8d6d1b64ca3011b6934a2b6190b7d0154b74c92aba` | 0 |
| main/ui/qrmode.c | 17928 | `dbd0b242f964aa6009b34b5191817ecf15f6b718b8ff3d78e63468a35821e0b7` | 0 |
| main/ui/select_registered_wallet.c | 3457 | `5d083eac87b93b8b92f893b573e09b4b20bd211c02063641cbf138fda4a2d1f7` | 0 |
| main/ui/sign_identity.c | 2408 | `83319e8311926c95451e83ab6887d65d9d8ac17f2deb2da42182f7e2eff6a50f` | 0 |
| main/ui/sign_message.c | 7103 | `1c44ed34d71f18a8ec8b555d15455cc0ec2366e67a9993648a52b8871b5e6826` | 0 |
| main/ui/sign_tx.c | 31154 | `c68ac7f25f690a17ab4b665975c2232aa4b6ecb28bc84f4fef01625803c8c08c` | 0 |
| main/ui/sign_tx.h | 1074 | `ecb8239a11d8fab093f7397fff4a41592bdd3440b1bb0bbcb522e8656d20d105` | 0 |
| main/ui/signer.c | 8232 | `2e59e02e306f4a61d16ef00ff97f3f86ae8a9f108ab10ed846a0c54d51c6f5e1` | 0 |
| main/ui/update_pinserver.c | 8359 | `04de1af452d4a8b6f038f3760887165ef47327a3c9c4f2af1dd2656b9ee9af96` | 0 |
| main/ui.h | 7837 | `f2a5526436add3772cd3afc50e062d95641fb905dfacbddaaf0b70d1a328aa1b` | 0 |
| main/usbhmsc/usbhmsc.c | 11342 | `f751c399bd28431b90bcf28cd9f8faab6a6bae601d57ca07ee251aafef9f6b82` | 0 |
| main/usbhmsc/usbhmsc.h | 643 | `64e8a037749b423bf7a8c1cfff1a7d2cbfefef0be6457fa12570c8123bf11f9f` | 0 |
| main/usbhmsc/usbmode.c | 36491 | `cf8387f59fced846d769e6a5cd7dd1e21fe9259f3fb8b2e241354cb812884f9f` | 0 |
| main/usbhmsc/usbmode.h | 377 | `47bf18c0bacf8d807a0efccbadabea74d63b4f3801665eaca8d9fff11ec57f24` | 0 |
| main/utils/address.c | 10283 | `678a7dd6f33487fd2464125cabe177ca3f7d6fe5215a1795e049bd963b560c0b` | 0 |
| main/utils/address.h | 1119 | `ff85133ff71681e53e70cd986cb5abf570abae8c44dd00e55b4528496b77798d` | 0 |
| main/utils/cbor_rpc.c | 21678 | `3639ad7f221082f17b991c7ce5df3f15d1290ffb45b49133690b5e497bcb8fe3` | 0 |
| main/utils/cbor_rpc.h | 4584 | `a8f950b65aa6d1f565eb5df2994bde2ca453c56e18b5111c5b18fd2d8dd7a4a6` | 0 |
| main/utils/event.c | 4978 | `a486786db4dbf40be24794b2beb072b716ff8c5911c1d639ff891b52bfc1c89f` | 0 |
| main/utils/event.h | 1455 | `3eb991ef183a40c8ee46564179061b020ecdac54e1a24a5e9a3e79ab5b720e6d` | 0 |
| main/utils/malloc_ext.h | 3630 | `f276221af422ef5c8e55f92d6f97f4ab5f04c1265ca5777a9e45f8879cf53f7d` | 0 |
| main/utils/network.c | 11202 | `a645709fe4bc725088719b3d3a3c02f9d4bdecb8c816b5877402a7fd8624c3ca` | 0 |
| main/utils/network.h | 1764 | `8f099fadd87d511a2075dc1baaf5ef0e635128388985996858239d32e12f3593` | 0 |
| main/utils/psbt.c | 9261 | `7e9e009a4aef8329efe88f6f1bc852d869a493e461744b14e49233564480ea6a` | 0 |
| main/utils/psbt.h | 2602 | `f4c081b54cd185597316182accdcf55913c1540b2770177cab3babc2d988036f` | 0 |
| main/utils/shake256.c | 3236 | `0f248acd752c2e4ac30b8a7746719b701bfa2831471787be5f1e7d4f47568a4e` | 0 |
| main/utils/shake256.h | 406 | `5d6531b00ecb44ee8d4787238a75d9681c769a39bcef7b062aabce92e49096f5` | 0 |
| main/utils/temporary_stack.c | 5015 | `9225a81af7da8e0fccf84923b54d52a83c36b35d49477815556ec4fc847b30a2` | 0 |
| main/utils/temporary_stack.h | 580 | `e62674406208b0252fc665066c78f4e05b6713927eb6fdca8ff520ba210771c3` | 0 |
| main/utils/urldecode.c | 5487 | `54818da78ccdf14d27f08156aaac6bd7038b6b7e1eb5aabcee68f1c5ebb4bbde` | 0 |
| main/utils/urldecode.h | 1694 | `77a573f188745a53f1ab544ca64adb32c2647e50d9c8ea480370905a554e3e8e` | 0 |
| main/utils/util.c | 6968 | `fb9002976cbe5b58c94041f0f9fb97cfc881f132ac75f0e6dde6895440c55dfd` | 0 |
| main/utils/util.h | 5319 | `bcaad10af73dc760c8f2d5890ccf824d86a178db8b9b7c1064f932b18a2af86c` | 0 |
| main/utils/wally_ext.c | 5481 | `2ed6fa1f3967ba5751a8810051310096851fbf218a6082826e52b27a8ebb462a` | 0 |
| main/utils/wally_ext.h | 294 | `8e4ca78aecbb261fe4401e761aeb3b1365ebbd289026411cb76bf2c0f1e53d27` | 0 |
| main/versioninfo.c | 6345 | `8a9fd493300a220db4aca9ea05c39bc71e65fb8f8ec57abd0424be96573b8ff4` | 0 |
| main/wallet.c | 60648 | `2355de892316eee3d8f799ceec58a988b26ffdec682b3a052df28aa54446324c` | 0 |
| main/wallet.h | 9463 | `bcb3ea05f748b4dfebbdea7c59468bb7864e54abd36f31bc0b7830f8c1943c57` | 0 |
| main/wifi.c | 20043 | `30820f634e4d57a7e4aa123a8f3e6dd7714711118125d29850177fed7a0fd0f6` | 0 |
| main/wifi.h | 460 | `8273dacaee29f457b4a5453c7ccbbf06b825416e8803b4588fa7ab9f3a619d2b` | 0 |
| main/wire.c | 7543 | `1a6c534cb518b8698aebbae58c13e7ae41dc72f85254914d24376ca412d36038` | 0 |
| main/wire.h | 746 | `c7dfa1c20463b7e99997545721fb2aacf08cf5474158466edf623eafc4f45436` | 0 |
