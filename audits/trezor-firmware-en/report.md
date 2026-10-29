# Security & Post-Quantum Readiness Audit Report

**Project:** trezor-firmware-en @ 72489948b3c4 · SatoshiLabs (Trezor) — public repository (passive review)
| | |
|---|---|
| Organization | QSI |
| Report date | 2026-10-28 18:57 UTC |
| Report version | 1 |
| Audit run | a7f00b63-4f9d-4441-8ea3-3c925595335f (Document audit) |
| Analyzer engine | qsi-engine 1.2.0 |
| Risk profile | Crypto exchange, custodian or wallet |
| Content SHA-256 | `5f237bcd3b3f212cf552c39f811bb7feec6f84750e4b79b7a4f3eaafac0ba77d` |
| Signature key (Ed25519, SHA-256 fingerprint; the signature is the separate file report.sig.json) | `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e` |
> This report presents automated and documented analysis results for the stated scope. It is not a legal opinion, a certification or an attestation of compliance with any standard.

## 1. Executive summary

- Critical: **0**
- High: **0**
- Medium: **11**
- Low: **0**
- Info: **0**

- Confirmed technical vulnerability: 0
- Known vulnerable component: 0
- Confirmed configuration error: 0
- Potential cryptographic risk: 0
- Long-term post-quantum risk: 11
- Improvement recommendation: 0
- Insufficient data: 0

Mosca's inequality (x + y > z): x = 10, y = 5, z = 8 → migration would finish too late under this scenario. _z is a planning assumption chosen per risk profile, not a prediction. A cryptographically relevant quantum computer is not publicly known to exist today._

Analyst review: 11 confirmed, 0 not applicable, 0 dismissed as false positives.

**Post-quantum maturity: Level 3 of 4 — hybrid protection in a critical path.** Next step: Cover the remaining classical critical roles and plan when the classical half can be dropped.

## 2. Scope and boundaries

Mode: Document audit

Repository: <https://github.com/trezor/trezor-firmware> @ `72489948b3c44a37598de9da658be28e4fabb4ae` — evidence links open the lines at this commit.

411 files, 2378051 bytes in total, 0 redaction(s); the per-file SHA-256 list is in appendix C.

## 3. Methodology

| Area | Status | Count | Examples |
|---|---|---|---|
| source_code | checked | 374 | common/protob/check.py: 49 lines scanned with 16 rule patterns and 122 registry patterns; common/protob/graph.py: 76 lines scanned with 16 rule patterns and 122 registry patterns; core/embed/projects/bootloader/bootui.c: 139 lines scanned with 16 rule patterns and 122 registry patterns |
| chain_map | checked | 13 | common/protob/messages-benchmark.proto: Bitcoin; common/protob/messages-bitcoin.proto: Bitcoin; common/protob/messages-cardano.proto: Cardano |
| dependencies | checked | 2 | core/embed/projects/bootloader/Cargo.toml: 9 dependencies parsed (0 pinned); core/embed/sec/Cargo.toml: 6 dependencies parsed (0 pinned) |
| certificates_and_keys | checked | 1 | core/embed/sec/secret/unix/certs/T3W1.der: certificates/keys parsed |
| osv_advisories | not checked | 1 | no exactly pinned versions to query |

_Long lists are grouped here; the full per-file list is in the JSON report, signed with the same key._

## 4. Assets examined and not examined

- osv_advisories — not checked: no exactly pinned versions to query

## 5. Architecture overview

Static review of the source tree trezor-firmware-en at 72489948b3c44a37598de9da658be28e4fabb4ae. 411 files analysed; of 464 files, 18 are test, fuzzing, benchmark or example code and were left out, 35 are not read by any analyzer, 0 exceed the per-file limit and 0 did not fit the total limit. No requests were sent to the owner's systems.

## 6. Overall security posture

- Indicative posture index: **100** / 100 — _Derived from findings in scope (confirmed and potential issues weighted by severity). Indicative only; not comparable across differently scoped audits._
- Quantum-vulnerable share of inventory: 65.8%

## 7. Detailed findings

### QSI-2026-06105 — Transaction signing for 11 chain(s) relies on elliptic-curve signatures

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: High
> **Analyst review (QSI review, 2026-10-28): confirmed by the analyst.** True by construction and the most important row in the report for planning. The protobuf message definitions in common/protob cover 11 chains whose signature schemes are fixed by consensus, not by the wallet: Bitcoin, Cardano, EOS, Ethereum and EVM, Monero, NEM, Solana, Stellar, Tezos, Tron, XRP. The wallet cannot migrate any of them unilaterally, so the deliverable here is a readiness map, not a code change — which is exactly why this belongs in an inventory rather than a vulnerability list.
- Affected asset: `chain-map`
- Data source: common/protob/messages-benchmark.proto
- Detection method: Message definitions (.proto) matched to QSI's table of chain signature schemes.
- Analyzer: chain_map 1.2.0 · 2026-10-28 18:57 UTC
- Priority score: 56.8 / 100
- CVSS v3.1: not applicable

The wallet's message definitions cover Bitcoin, Cardano, EOS, Ethereum and EVM chains, Monero, NEM, Solana, Stellar, Tezos, Tron, XRP Ledger. These chains authorize transactions with ECDSA, Ed25519, Schnorr (BIP-340), which Shor's algorithm breaks on a cryptographically relevant quantum computer. A wallet cannot move a chain to post-quantum signatures on its own: the chain has to adopt a scheme first.

**Potential impact.** Once a CRQC exists, an attacker who sees an account's public key could derive the private key and move funds; how soon keys are exposed depends on each chain (address reuse, account model).

**Reproduction steps.**

```
Open the .proto files named in the evidence.
```

**Evidence.**

_file_excerpt · [common/protob/messages-benchmark.proto](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/common/protob/messages-benchmark.proto#L2) · line 2 · SHA-256 d58a0f922546e5589a782c4c431b203a948e0ba3367b16acc48b083757337b57_

```
package hw.trezor.messages.bitcoin;
```

_file_excerpt · [common/protob/messages-bitcoin.proto](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/common/protob/messages-bitcoin.proto#L2) · line 2 · SHA-256 d58a0f922546e5589a782c4c431b203a948e0ba3367b16acc48b083757337b57_

```
package hw.trezor.messages.bitcoin;
```

_file_excerpt · [common/protob/messages-cardano.proto](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/common/protob/messages-cardano.proto#L2) · line 2 · SHA-256 790478e3c9df02a9cc167174f39aa681bc17bc797f083b31cf5bc62de73da6d2_

```
package hw.trezor.messages.cardano;
```

_file_excerpt · [common/protob/messages-eos.proto](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/common/protob/messages-eos.proto#L2) · line 2 · SHA-256 1bc71146f1570006a9a973ea956409f0e3a01cb63fa24947ee54d8bf842a73c5_

```
package hw.trezor.messages.eos;
```

_file_excerpt · [common/protob/messages-ethereum-eip712.proto](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/common/protob/messages-ethereum-eip712.proto#L2) · line 2 · SHA-256 1e20c49087fd2d8274025478654c869acc2208573fb52d553fd9ae6ad5b2e57b_

```
package hw.trezor.messages.ethereum_eip712;
```

_file_excerpt · [common/protob/messages-ethereum.proto](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/common/protob/messages-ethereum.proto#L2) · line 2 · SHA-256 2c715738dc6f29a41f531184d048ec35830475da4152cdbdc22a4ee88cc1327c_

```
package hw.trezor.messages.ethereum;
```

_file_excerpt · [common/protob/messages-monero.proto](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/common/protob/messages-monero.proto#L2) · line 2 · SHA-256 2a60fdbae9c4da472daabb0e85b95bb7592b561df57b5344c02f5d168a37c8d9_

```
package hw.trezor.messages.monero;
```

_file_excerpt · [common/protob/messages-nem.proto](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/common/protob/messages-nem.proto#L2) · line 2 · SHA-256 ae6d3c9d0ee3ae3e09e2007756938e4722cde7d467e71445ec9bdaa4af8d8e8a_

```
package hw.trezor.messages.nem;
```

_file_excerpt · [common/protob/messages-ripple.proto](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/common/protob/messages-ripple.proto#L2) · line 2 · SHA-256 fc5096c71f30511dd5c0ea991b9a539f8aa06b6516b8317d4f738e6f164d30bb_

```
package hw.trezor.messages.ripple;
```

_file_excerpt · [common/protob/messages-solana.proto](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/common/protob/messages-solana.proto#L2) · line 2 · SHA-256 bfc45618be53d3facd05de533c2d5bb4a77983730fe6ec3542fb7c63e67a6d17_

```
package hw.trezor.messages.solana;
```

_file_excerpt · [common/protob/messages-stellar.proto](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/common/protob/messages-stellar.proto#L2) · line 2 · SHA-256 fad5a4b7a72a767742eb23629aef3942a53935e1c62cde7787ccad8cedb0e31a_

```
package hw.trezor.messages.stellar;
```

_file_excerpt · [common/protob/messages-tezos.proto](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/common/protob/messages-tezos.proto#L2) · line 2 · SHA-256 967d28a5f166e7d47d445277efcfecf0dc0f0596300340afd84afa0277ee829b_

```
package hw.trezor.messages.tezos;
```

_file_excerpt · [common/protob/messages-tron.proto](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/common/protob/messages-tron.proto#L2) · line 2 · SHA-256 19b3678a04d39ff5ab88fc9368ffcc08a139179c086ed362f6b6a4b2391b46ea_

```
package hw.trezor.messages.tron;
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Chains are recognized from the names of the message definitions (.proto files and packages); the schemes are the chains' documented account signatures, not an analysis of the wallet's signing code.

**Recommendation.** Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains adopt them. Keep the signing layer crypto-agile per chain (algorithm identifiers in messages and storage, room for larger keys and signatures) and track each chain's post-quantum proposals, so that a new scheme can be added when a chain activates it.

**Retest procedure.** Re-run when a chain activates a post-quantum signature scheme or the wallet adds one.

### QSI-2026-06095 — Quantum-vulnerable Ed25519: firmware and boot verification (root of trust) (2 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium
> **Analyst review (QSI review, 2026-10-28): confirmed by the analyst.** The remaining rows carry a role the engine determined and review agrees with, each checked against the cited file. Ed25519 at core/embed/sec/image/boot_header.c:81 and image.c is firmware and boot verification, with the public keys fixed in the bootloader. **It must not be called unmigrated, because this vendor has already started**: SLH-DSA appears in that same boot_header.c at line 30, there is a whole ML-DSA-44 module at core/embed/sec/mldsa44/, MCU attestation uses ML-DSA (core/embed/sec/mcu_attestation/), and the tree ships an X.509 certificate with an ML-DSA-44 public key (core/embed/sec/secret/unix/certs/T3W1.der). The inventory carries those seven rows as post-quantum. So the correct reading of this repository is a root of trust **mid-transition**, carrying both schemes, and the Ed25519 rows are what remains of the classical half rather than evidence that nothing has been done. Trezor is the most advanced repository in this portfolio on post-quantum readiness, and any report that presents it otherwise is wrong on a point its own engineers would see immediately. X25519 at core/embed/sec/tropic/tropic.c:383 plus crypto/noise_kk1.c and noise_xxpsk3.c is channel key exchange with the Tropic01 secure element over Noise — recordable now, decryptable later, and the standard answer is a hybrid exchange. ECDSA at crypto/bip32.c:40, crypto/secp256k1.c and crypto/zkp_bip340.c, and Schnorr (BIP-340) at crypto/zkp_bip340.c:139, are transaction signing. Ed25519 at crypto/bip32.c:477, crypto/nem.c and nem.h is transaction signing on the NEM path.
- Affected asset: `source-code:Ed25519:root_of_trust`
- Data source: core/embed/sec/image/boot_header.c
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.2.0 · 2026-10-28 18:57 UTC
- Priority score: 43.4 / 100
- CVSS v3.1: not applicable

4 reference(s) to Ed25519 across 2 file(s), e.g. core/embed/sec/image/boot_header.c:81. Role, judged from paths, function names and nearby code: firmware and boot verification (root of trust). These public keys are fixed in the bootloader or the device: with a cryptographically relevant quantum computer (CRQC) an attacker forges a firmware signature, and replacing the keys needs a bootloader update in the field.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open core/embed/sec/image/boot_header.c:81 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [core/embed/sec/image/boot_header.c](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/core/embed/sec/image/boot_header.c#L81) · line 81 · SHA-256 b2af0c1adee8c4fb6c493c712f1d917bb01ae6443327255e3d28e94b27eb762e_

```
   80 |     int ec_result =
   81 |         ed25519_sign_open(hash, sizeof(hash), BOARDLOADER_EC_KEYS[key_idx],
   82 |                           sig->ec_signature[sig_idx]);
```

_file_excerpt · [core/embed/sec/image/image.c](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/core/embed/sec/image/image.c#L190) · line 190 · SHA-256 dfcc4a69e889974486837aa4be50157bff4a2e73e324925df33bc30df7fc03b3_

```
  189 |   return sectrue *
  190 |          (0 == ed25519_sign_open(fingerprint, IMAGE_HASH_DIGEST_LENGTH, pub,
  191 |                                  *(const ed25519_signature *)hdr->sig));
```

_file_excerpt · [core/embed/sec/image/image.c](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/core/embed/sec/image/image.c#L249) · line 249 · SHA-256 708bc289abcbd866d09ef041c2d9869e54b53f060c69c50d2f9fd26d00edadd2_

```
  248 |   return sectrue *
  249 |          (0 == ed25519_sign_open(fingerprint, IMAGE_HASH_DIGEST_LENGTH, pub,
  250 |                                  *(const ed25519_signature *)hdr->sig));
```

_file_excerpt · [core/embed/sec/image/image.c](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/core/embed/sec/image/image.c#L411) · line 411 · SHA-256 69cfc8f4b867ff5bea83d7fbadbbfe788411ba06e037fc81aa3ceca6b842628b_

```
  410 |   return sectrue *
  411 |          (0 == ed25519_sign_open(hash, IMAGE_HASH_DIGEST_LENGTH, pub,
  412 |                                  *(const ed25519_signature *)vhdr->sig));
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Plan a hybrid firmware signature (the classical one plus ML-DSA or SLH-DSA, both required) and the path to ship the new keys in a bootloader update.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-06097 — Quantum-vulnerable X25519: channel key exchange (TLS, Noise, handshakes) (3 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium
> **Analyst review (QSI review, 2026-10-28): confirmed by the analyst.** The remaining rows carry a role the engine determined and review agrees with, each checked against the cited file. Ed25519 at core/embed/sec/image/boot_header.c:81 and image.c is firmware and boot verification, with the public keys fixed in the bootloader. **It must not be called unmigrated, because this vendor has already started**: SLH-DSA appears in that same boot_header.c at line 30, there is a whole ML-DSA-44 module at core/embed/sec/mldsa44/, MCU attestation uses ML-DSA (core/embed/sec/mcu_attestation/), and the tree ships an X.509 certificate with an ML-DSA-44 public key (core/embed/sec/secret/unix/certs/T3W1.der). The inventory carries those seven rows as post-quantum. So the correct reading of this repository is a root of trust **mid-transition**, carrying both schemes, and the Ed25519 rows are what remains of the classical half rather than evidence that nothing has been done. Trezor is the most advanced repository in this portfolio on post-quantum readiness, and any report that presents it otherwise is wrong on a point its own engineers would see immediately. X25519 at core/embed/sec/tropic/tropic.c:383 plus crypto/noise_kk1.c and noise_xxpsk3.c is channel key exchange with the Tropic01 secure element over Noise — recordable now, decryptable later, and the standard answer is a hybrid exchange. ECDSA at crypto/bip32.c:40, crypto/secp256k1.c and crypto/zkp_bip340.c, and Schnorr (BIP-340) at crypto/zkp_bip340.c:139, are transaction signing. Ed25519 at crypto/bip32.c:477, crypto/nem.c and nem.h is transaction signing on the NEM path.
- Affected asset: `source-code:X25519:channel`
- Data source: core/embed/sec/tropic/tropic.c
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.2.0 · 2026-10-28 18:57 UTC
- Priority score: 41.8 / 100
- CVSS v3.1: not applicable

14 reference(s) to X25519 across 3 file(s), e.g. core/embed/sec/tropic/tropic.c:383. Role, judged from paths, function names and nearby code: channel key exchange (TLS, Noise, handshakes). Traffic protected by this key exchange can be recorded now and decrypted later; a hybrid exchange keeps the classical guarantees and adds post-quantum ones.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open core/embed/sec/tropic/tropic.c:383 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [core/embed/sec/tropic/tropic.c](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/core/embed/sec/tropic/tropic.c#L383) · line 383 · SHA-256 6a8b8eac9f12e02ddff658df23166595bf7d7db27950826444f652d9b3d16687_

```
  382 |   curve25519_key trezor_public = {0};
  383 |   curve25519_scalarmult_basepoint(trezor_public, trezor_private);
  384 | 
```

_file_excerpt · [crypto/noise_kk1.c](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/crypto/noise_kk1.c#L187) · line 187 · SHA-256 92dfee834b4c368531df7ad9283f7d6639899197e7d98ba295c0e2ca0305c92f_

```
  186 |                 sizeof(ctx->initiator_ephemeral_private_key));
  187 |   curve25519_scalarmult_basepoint(request->initiator_ephemeral_public_key,
  188 |                                   ctx->initiator_ephemeral_private_key);
```

_file_excerpt · [crypto/noise_kk1.c](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/crypto/noise_kk1.c#L199) · line 199 · SHA-256 561606d6dbe7a1230e6670690b51b03eeb28f323fcc81250a5a75dd012373b11_

```
  198 |   curve25519_key responder_public_key = {0};
  199 |   curve25519_scalarmult_basepoint(responder_public_key, responder_private_key);
  200 | 
```

_file_excerpt · [crypto/noise_kk1.c](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/crypto/noise_kk1.c#L205) · line 205 · SHA-256 e17fd3f06c5cea712465187e110e0ea951f81d40d8ce732a92df067866302bc6_

```
  204 |   curve25519_key responder_ephemeral_public_key = {0};
  205 |   curve25519_scalarmult_basepoint(responder_ephemeral_public_key,
  206 |                                   responder_ephemeral_private_key);
```

_file_excerpt · [crypto/noise_xxpsk3.c](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/crypto/noise_xxpsk3.c#L138) · line 138 · SHA-256 9648d44dace3fff12b561c2e3e511312ec7def54cb7275384d84c2778cdbb3df_

```
  137 |                uint8_t (*output)[NOISE_XXPSK3_DHLEN]) {
  138 |   curve25519_scalarmult(*output, *private_key, *public_key);
  139 | }
```

_file_excerpt · [crypto/noise_xxpsk3.c](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/crypto/noise_xxpsk3.c#L197) · line 197 · SHA-256 4e128b42ab2d3d6fed69a9574f691e939ebc76321a124491053274cc9b5770eb_

```
  196 |   (*private_key)[31] |= 64;
  197 |   curve25519_scalarmult_basepoint(*public_key, *private_key);
  198 | }
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Move the handshake to a hybrid key exchange (X25519MLKEM768 in TLS 1.3; a hybrid KEM in Noise-based protocols).

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-06098 — Quantum-vulnerable ECDSA: transaction and message signing (4 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium
> **Analyst review (QSI review, 2026-10-28): confirmed by the analyst.** The remaining rows carry a role the engine determined and review agrees with, each checked against the cited file. Ed25519 at core/embed/sec/image/boot_header.c:81 and image.c is firmware and boot verification, with the public keys fixed in the bootloader. **It must not be called unmigrated, because this vendor has already started**: SLH-DSA appears in that same boot_header.c at line 30, there is a whole ML-DSA-44 module at core/embed/sec/mldsa44/, MCU attestation uses ML-DSA (core/embed/sec/mcu_attestation/), and the tree ships an X.509 certificate with an ML-DSA-44 public key (core/embed/sec/secret/unix/certs/T3W1.der). The inventory carries those seven rows as post-quantum. So the correct reading of this repository is a root of trust **mid-transition**, carrying both schemes, and the Ed25519 rows are what remains of the classical half rather than evidence that nothing has been done. Trezor is the most advanced repository in this portfolio on post-quantum readiness, and any report that presents it otherwise is wrong on a point its own engineers would see immediately. X25519 at core/embed/sec/tropic/tropic.c:383 plus crypto/noise_kk1.c and noise_xxpsk3.c is channel key exchange with the Tropic01 secure element over Noise — recordable now, decryptable later, and the standard answer is a hybrid exchange. ECDSA at crypto/bip32.c:40, crypto/secp256k1.c and crypto/zkp_bip340.c, and Schnorr (BIP-340) at crypto/zkp_bip340.c:139, are transaction signing. Ed25519 at crypto/bip32.c:477, crypto/nem.c and nem.h is transaction signing on the NEM path.
- Affected asset: `source-code:ECDSA:transaction_signing`
- Data source: crypto/bip32.c
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.2.0 · 2026-10-28 18:57 UTC
- Priority score: 41.8 / 100
- CVSS v3.1: not applicable

13 reference(s) to ECDSA across 4 file(s), e.g. crypto/bip32.c:40. Role, judged from paths, function names and nearby code: transaction and message signing. A CRQC derives the private key from a public key that is already known (on chain after the first spend, in reused addresses): funds and approvals controlled by these keys need a migration path.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open crypto/bip32.c:40 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [crypto/bip32.c](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/crypto/bip32.c#L40) · line 40 · SHA-256 a9165bffdef5ae27e2ba39ddb3d8ba0c10eb9341570969040cd15e1128810354_

```
   39 | #include "nist256p1.h"
   40 | #include "secp256k1.h"
   41 | #include "sha2.h"
```

_file_excerpt · [crypto/bip32.c](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/crypto/bip32.c#L670) · line 670 · SHA-256 81ebab5faffac9ea0878d776655e59b42e6187f392af97d4484cd8633ebb2b8b_

```
  669 |   if (node->curve->params) {
  670 |     return ecdsa_sign_digest(node->curve->params, node->private_key, digest,
  671 |                              sig, pby, is_canonical);
```

_file_excerpt · [crypto/secp256k1.c](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/crypto/secp256k1.c#L24) · line 24 · SHA-256 aaefce0c635dd2025b251d5f2b3a6d7e5d4f3329ad49681589c1452ed3fcf659_

```
   23 | 
   24 | #include "secp256k1.h"
   25 | 
```

_file_excerpt · [crypto/secp256k1.c](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/crypto/secp256k1.c#L26) · line 26 · SHA-256 3fcb800f4c815d9d84ae60c3e4f2b8a6a4de071b52686015e530cfcd254dcd05_

```
   25 | 
   26 | const ecdsa_curve secp256k1 = {
   27 |     /* .prime */ {/*.val =*/{0x1ffffc2f, 0x1ffffff7, 0x1fffffff, 0x1fffffff,
```

_file_excerpt · [crypto/secp256k1.c](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/crypto/secp256k1.c#L55) · line 55 · SHA-256 7e89b542010777ba928e99a932d1a071fb882a321b72f98f8f748d3584428fe4_

```
   54 |     {
   55 | #include "secp256k1.table"
   56 |     }
```

_file_excerpt · [crypto/secp256k1.h](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/crypto/secp256k1.h#L32) · line 32 · SHA-256 5257b883e95e417a1661c06e7caa265fe8170e9ff108435e83c354ca6b840dad_

```
   31 | 
   32 | extern const ecdsa_curve secp256k1;
   33 | extern const curve_info secp256k1_info;
```

_file_excerpt · [crypto/zkp_bip340.c](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/crypto/zkp_bip340.c#L30) · line 30 · SHA-256 ef19a8a2b914c5235289dd3b646042c2401b62b2b6e4014c65666ba7ec2c07b6_

```
   29 | 
   30 | #include "vendor/secp256k1-zkp/include/secp256k1.h"
   31 | #include "vendor/secp256k1-zkp/include/secp256k1_extrakeys.h"
```

_file_excerpt · [crypto/zkp_bip340.c](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/crypto/zkp_bip340.c#L31) · line 31 · SHA-256 860dd605d6fca510e08f9c516a9e05341047eef9ba000f45bcfc306db7ea4787_

```
   30 | #include "vendor/secp256k1-zkp/include/secp256k1.h"
   31 | #include "vendor/secp256k1-zkp/include/secp256k1_extrakeys.h"
   32 | #include "vendor/secp256k1-zkp/include/secp256k1_schnorrsig.h"
```

_file_excerpt · [crypto/zkp_bip340.c](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/crypto/zkp_bip340.c#L32) · line 32 · SHA-256 f0d785deb2e91ec837b7e79180e1ee76920a0e886315f256da82f00db6ae5a5f_

```
   31 | #include "vendor/secp256k1-zkp/include/secp256k1_extrakeys.h"
   32 | #include "vendor/secp256k1-zkp/include/secp256k1_schnorrsig.h"
   33 | 
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains adopt them.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-06101 — Quantum-vulnerable Ed25519: transaction and message signing (3 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium
> **Analyst review (QSI review, 2026-10-28): confirmed by the analyst.** The remaining rows carry a role the engine determined and review agrees with, each checked against the cited file. Ed25519 at core/embed/sec/image/boot_header.c:81 and image.c is firmware and boot verification, with the public keys fixed in the bootloader. **It must not be called unmigrated, because this vendor has already started**: SLH-DSA appears in that same boot_header.c at line 30, there is a whole ML-DSA-44 module at core/embed/sec/mldsa44/, MCU attestation uses ML-DSA (core/embed/sec/mcu_attestation/), and the tree ships an X.509 certificate with an ML-DSA-44 public key (core/embed/sec/secret/unix/certs/T3W1.der). The inventory carries those seven rows as post-quantum. So the correct reading of this repository is a root of trust **mid-transition**, carrying both schemes, and the Ed25519 rows are what remains of the classical half rather than evidence that nothing has been done. Trezor is the most advanced repository in this portfolio on post-quantum readiness, and any report that presents it otherwise is wrong on a point its own engineers would see immediately. X25519 at core/embed/sec/tropic/tropic.c:383 plus crypto/noise_kk1.c and noise_xxpsk3.c is channel key exchange with the Tropic01 secure element over Noise — recordable now, decryptable later, and the standard answer is a hybrid exchange. ECDSA at crypto/bip32.c:40, crypto/secp256k1.c and crypto/zkp_bip340.c, and Schnorr (BIP-340) at crypto/zkp_bip340.c:139, are transaction signing. Ed25519 at crypto/bip32.c:477, crypto/nem.c and nem.h is transaction signing on the NEM path.
- Affected asset: `source-code:Ed25519:transaction_signing`
- Data source: crypto/bip32.c
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.2.0 · 2026-10-28 18:57 UTC
- Priority score: 41.8 / 100
- CVSS v3.1: not applicable

10 reference(s) to Ed25519 across 3 file(s), e.g. crypto/bip32.c:477. Role, judged from paths, function names and nearby code: transaction and message signing. A CRQC derives the private key from a public key that is already known (on chain after the first spend, in reused addresses): funds and approvals controlled by these keys need a migration path.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open crypto/bip32.c:477 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [crypto/bip32.c](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/crypto/bip32.c#L477) · line 477 · SHA-256 c93b42f00e9370066521cf79c2798fde91c9b2822853563ab3afceb469dabc28_

```
  476 |     if (node->curve == &ed25519_info) {
  477 |       ed25519_publickey(node->private_key, node->public_key + 1);
  478 |     } else if (node->curve == &ed25519_sha3_info) {
```

_file_excerpt · [crypto/bip32.c](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/crypto/bip32.c#L479) · line 479 · SHA-256 8ed678007d138957d9e205451ce947cd59213b5bbbb84462156ddd6ed04a303c_

```
  478 |     } else if (node->curve == &ed25519_sha3_info) {
  479 |       ed25519_publickey_sha3(node->private_key, node->public_key + 1);
  480 | #if USE_KECCAK
```

_file_excerpt · [crypto/bip32.c](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/crypto/bip32.c#L482) · line 482 · SHA-256 183902ffc93a30934c7802c54d27eec2bd33efac586d1eead5fbcac4656e92f8_

```
  481 |     } else if (node->curve == &ed25519_keccak_info) {
  482 |       ed25519_publickey_keccak(node->private_key, node->public_key + 1);
  483 | #endif
```

_file_excerpt · [crypto/nem.c](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/crypto/nem.c#L207) · line 207 · SHA-256 ffe72c257d7484e9296d04484e172589e186505be9b773b097a0e5e0aa0f47f2_

```
  206 |                            const ed25519_secret_key private_key,
  207 |                            ed25519_signature signature) {
  208 |   if (private_key != NULL && signature != NULL) {
```

_file_excerpt · [crypto/nem.c](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/crypto/nem.c#L209) · line 209 · SHA-256 19f8b44e8439c39d9fd1783e94997f6dabee1f50815d190afaab2ec10e81c58e_

```
  208 |   if (private_key != NULL && signature != NULL) {
  209 |     ed25519_sign_keccak(ctx->buffer, ctx->offset, private_key, signature);
  210 |   }
```

_file_excerpt · [crypto/nem.h](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/crypto/nem.h#L90) · line 90 · SHA-256 89c1645bf199ca12171f92e84bfa0d38b9fd2b1d2d4638a2e9aa3431e9ffdf38_

```
   89 |                            const ed25519_secret_key private_key,
   90 |                            ed25519_signature signature);
   91 | 
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains adopt them.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-06104 — Quantum-vulnerable Schnorr (BIP-340): transaction and message signing (1 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium
> **Analyst review (QSI review, 2026-10-28): confirmed by the analyst.** The remaining rows carry a role the engine determined and review agrees with, each checked against the cited file. Ed25519 at core/embed/sec/image/boot_header.c:81 and image.c is firmware and boot verification, with the public keys fixed in the bootloader. **It must not be called unmigrated, because this vendor has already started**: SLH-DSA appears in that same boot_header.c at line 30, there is a whole ML-DSA-44 module at core/embed/sec/mldsa44/, MCU attestation uses ML-DSA (core/embed/sec/mcu_attestation/), and the tree ships an X.509 certificate with an ML-DSA-44 public key (core/embed/sec/secret/unix/certs/T3W1.der). The inventory carries those seven rows as post-quantum. So the correct reading of this repository is a root of trust **mid-transition**, carrying both schemes, and the Ed25519 rows are what remains of the classical half rather than evidence that nothing has been done. Trezor is the most advanced repository in this portfolio on post-quantum readiness, and any report that presents it otherwise is wrong on a point its own engineers would see immediately. X25519 at core/embed/sec/tropic/tropic.c:383 plus crypto/noise_kk1.c and noise_xxpsk3.c is channel key exchange with the Tropic01 secure element over Noise — recordable now, decryptable later, and the standard answer is a hybrid exchange. ECDSA at crypto/bip32.c:40, crypto/secp256k1.c and crypto/zkp_bip340.c, and Schnorr (BIP-340) at crypto/zkp_bip340.c:139, are transaction signing. Ed25519 at crypto/bip32.c:477, crypto/nem.c and nem.h is transaction signing on the NEM path.
- Affected asset: `source-code:Schnorr (BIP-340):transaction_signing`
- Data source: crypto/zkp_bip340.c
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.2.0 · 2026-10-28 18:57 UTC
- Priority score: 41.8 / 100
- CVSS v3.1: not applicable

2 reference(s) to Schnorr (BIP-340) across 1 file(s), e.g. crypto/zkp_bip340.c:139. Role, judged from paths, function names and nearby code: transaction and message signing. A CRQC derives the private key from a public key that is already known (on chain after the first spend, in reused addresses): funds and approvals controlled by these keys need a migration path.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open crypto/zkp_bip340.c:139 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [crypto/zkp_bip340.c](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/crypto/zkp_bip340.c#L139) · line 139 · SHA-256 0cf0a8147e0f6339f73b0bb98dcde6414ca590a73ef0343d41e17dcc39812427_

```
  138 |   if (result == 0) {
  139 |     if (secp256k1_schnorrsig_sign32(context_writable, signature_bytes, digest,
  140 |                                     &keypair, auxiliary_data) != 1) {
```

_file_excerpt · [crypto/zkp_bip340.c](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/crypto/zkp_bip340.c#L176) · line 176 · SHA-256 713fd6fd7674234717caf272b5694b243a75dca531942f64b80fb738a30cdcb5_

```
  175 |   if (result == 0) {
  176 |     if (secp256k1_schnorrsig_verify(context_read_only, signature_bytes, digest,
  177 |                                     32, &xonly_pubkey) != 1) {
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains adopt them.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-06096 — Quantum-vulnerable ECDSA: authentication and identity (certificates, tokens, device attestation) (2 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium
> **Analyst review (QSI review, 2026-10-28): confirmed by the analyst.** Correct and worth separating from transaction signing. The anchors are core/embed/sec/optiga/ optiga_commands.c:1055 and optiga/unix/optiga.c — the Infineon OPTIGA secure element, which the device uses for device attestation and pairing rather than for spending. Short-lived authentication survives until a CRQC exists; a device identity that outlives the hardware does not, so this is a replace-at-next-hardware- revision item, not a firmware-update item.
- Affected asset: `source-code:ECDSA:authentication`
- Data source: core/embed/sec/optiga/optiga_commands.c
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.2.0 · 2026-10-28 18:57 UTC
- Priority score: 40.2 / 100
- CVSS v3.1: not applicable

2 reference(s) to ECDSA across 2 file(s), e.g. core/embed/sec/optiga/optiga_commands.c:1055. Role, judged from paths, function names and nearby code: authentication and identity (certificates, tokens, device attestation). Short-lived authentication stays safe until a CRQC exists; long-lived identities (device attestation, CA and SSH keys) need a plan earlier.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open core/embed/sec/optiga/optiga_commands.c:1055 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [core/embed/sec/optiga/optiga_commands.c](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/core/embed/sec/optiga/optiga_commands.c#L1055) · line 1055 · SHA-256 c6bd24690265c1b07db19daf28e91399ac13d6eb0cbc38c1205a7879e8cc5525_

```
 1054 | 
 1055 |   if (0 != ecdsa_sign_digest(&nist256p1, TA_PRIV_KEY, digest, &sop_cmd1[81],
 1056 |                              NULL, NULL)) {
```

_file_excerpt · [core/embed/sec/optiga/unix/optiga.c](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/core/embed/sec/optiga/unix/optiga.c#L58) · line 58 · SHA-256 fa6d6a3639322b2dfe9b568a69249366c4ac66f519d039a02e601df7e31f0449_

```
   57 |   uint8_t raw_signature[ECDSA_RAW_SIGNATURE_SIZE] = {0};
   58 |   int ret = ecdsa_sign_digest(&nist256p1, DEVICE_PRIV_KEY, digest,
   59 |                               raw_signature, NULL, NULL);
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Keep credentials short-lived and plan ML-DSA certificates, tokens and keys as the ecosystem supports them.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-06099 — Quantum-vulnerable ECDH: role not determined (1 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium
> **Analyst review (QSI review, 2026-10-28): confirmed by the analyst.** Role resolved. crypto/bip32.c:702 is inside hdnode_get_shared_key: it calls curve25519_scalarmult(session_key + 1, node->private_key, peer_public_key + 1) and returns "ECDH is not supported" for any other curve. So this is ECDH between a BIP-32 node's private key and a peer public key, producing a session key for the identity and encryption features (SLIP-0017 style), not for spending. Harvest-now-decrypt-later applies to anything wrapped under such a session key, and because the node keys are derived from the device seed, a CRQC that recovers one node's private key recovers every session that node ever established. Priority: below transaction signing, above attestation.
- Affected asset: `source-code:ECDH:general`
- Data source: crypto/bip32.c
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.2.0 · 2026-10-28 18:57 UTC
- Priority score: 40.2 / 100
- CVSS v3.1: not applicable

1 reference(s) to ECDH across 1 file(s), e.g. crypto/bip32.c:702. Role, judged from paths, function names and nearby code: role not determined. The code does not show what the keys protect; review decides the priority.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open crypto/bip32.c:702 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [crypto/bip32.c](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/crypto/bip32.c#L702) · line 702 · SHA-256 389be3881695685895f920c4ceb0ad2dce6816c07e0808be71ddd0d9276f3d93_

```
  701 |     *result_size = 0;
  702 |     return 1;  // ECDH is not supported
  703 |   }
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Classify each usage, record data lifetimes, and plan migration to Hybrid key establishment with ML-KEM (FIPS 203), e.g. X25519MLKEM768 in TLS 1.3 or mlkem768x25519-sha256 in SSH; introduce an abstraction layer for crypto-agility.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-06100 — Quantum-vulnerable X25519: role not determined (3 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium
> **Analyst review (QSI review, 2026-10-28): confirmed by the analyst.** Role resolved. crypto/bip32.c:485 is inside hdnode_fill_public_key, which dispatches per curve: ed25519_publickey, ed25519_publickey_sha3, ed25519_publickey_keccak, curve25519_scalarmult_basepoint and the Cardano variant. The remaining anchors are crypto/ed25519-donna/ed25519.{c,h}, the vendored implementation. So these rows are the public-key derivation layer feeding the signing and ECDH paths that are inventoried separately, not an independent use. They belong in the inventory because the derivation itself has to change in a post-quantum scheme, but a reader should not count them as extra exposure on top of the signing rows.
- Affected asset: `source-code:X25519:general`
- Data source: crypto/bip32.c
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.2.0 · 2026-10-28 18:57 UTC
- Priority score: 40.2 / 100
- CVSS v3.1: not applicable

6 reference(s) to X25519 across 3 file(s), e.g. crypto/bip32.c:485. Role, judged from paths, function names and nearby code: role not determined. The code does not show what the keys protect; review decides the priority.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open crypto/bip32.c:485 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [crypto/bip32.c](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/crypto/bip32.c#L485) · line 485 · SHA-256 20d65e62022d83190469af099e68f304e380abf8949209c7259d85048d87b803_

```
  484 |     } else if (node->curve == &curve25519_info) {
  485 |       curve25519_scalarmult_basepoint(node->public_key + 1, node->private_key);
  486 | #if USE_CARDANO
```

_file_excerpt · [crypto/bip32.c](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/crypto/bip32.c#L696) · line 696 · SHA-256 812181201a85f579d5d09a17ff9a49f0fa03fb8fcd9619daad1e577da9b7e1fe_

```
  695 |     }
  696 |     curve25519_scalarmult(session_key + 1, node->private_key,
  697 |                           peer_public_key + 1);
```

_file_excerpt · [crypto/ed25519-donna/ed25519.c](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/crypto/ed25519-donna/ed25519.c#L274) · line 274 · SHA-256 822b93d7b53ae8cde5036e6fca18fcafece86f3fbc88b6bc5cc54d1cb5797cf5_

```
  273 | void
  274 | curve25519_scalarmult_basepoint(curve25519_key pk, const curve25519_key e) {
  275 | 	curve25519_key ec = {0};
```

_file_excerpt · [crypto/ed25519-donna/ed25519.c](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/crypto/ed25519-donna/ed25519.c#L303) · line 303 · SHA-256 37ac0de6a16b455ba9987423827a952280ef698f728ebf87d1abffd5eb988187_

```
  302 | void
  303 | curve25519_scalarmult(curve25519_key mypublic, const curve25519_key secret, const curve25519_key basepoint) {
  304 | 	curve25519_key e = {0};
```

_file_excerpt · [crypto/ed25519-donna/ed25519.h](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/crypto/ed25519-donna/ed25519.h#L29) · line 29 · SHA-256 7441e37eaff8b03f481182a533b231b8fa511fdd3274ae0e4e3e11d30856b7f4_

```
   28 | 
   29 | void curve25519_scalarmult(curve25519_key mypublic, const curve25519_key secret, const curve25519_key basepoint);
   30 | void curve25519_scalarmult_basepoint(curve25519_key mypublic, const curve25519_key secret);
```

_file_excerpt · [crypto/ed25519-donna/ed25519.h](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/crypto/ed25519-donna/ed25519.h#L30) · line 30 · SHA-256 64e240fedc50cea38d023195f79cd62e4ad04135aa27e585b1d044f65f9eb20b_

```
   29 | void curve25519_scalarmult(curve25519_key mypublic, const curve25519_key secret, const curve25519_key basepoint);
   30 | void curve25519_scalarmult_basepoint(curve25519_key mypublic, const curve25519_key secret);
   31 | 
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Classify each usage, record data lifetimes, and plan migration to Hybrid key establishment with ML-KEM (FIPS 203), e.g. X25519MLKEM768 in TLS 1.3 or mlkem768x25519-sha256 in SSH; introduce an abstraction layer for crypto-agility.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-06102 — Quantum-vulnerable ECDSA: role not determined (8 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium
> **Analyst review (QSI review, 2026-10-28): confirmed by the analyst.** Role resolved, and the anchor set is mixed, which matters for scoping. crypto/curves.c, crypto/ecdsa.c and crypto/ecdsa.h are the ECDSA implementation the device signs with — the correct and highest-priority inventory rows. But two of the eight files are not firmware: crypto/setup.py is the build script for the Python bindings, and crypto/tools/bip39bruteforce.c is a standalone demonstration utility. Neither ships on the device, so a migration plan should carry the three implementation files and drop those two. Flagging this rather than dismissing the whole finding: the rule is right, its file list is broader than the deployed surface.
- Affected asset: `source-code:ECDSA:general`
- Data source: crypto/curves.c
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.2.0 · 2026-10-28 18:57 UTC
- Priority score: 40.2 / 100
- CVSS v3.1: not applicable

50 reference(s) to ECDSA across 8 file(s), e.g. crypto/curves.c:25. Role, judged from paths, function names and nearby code: role not determined. The code does not show what the keys protect; review decides the priority.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open crypto/curves.c:25 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [crypto/curves.c](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/crypto/curves.c#L25) · line 25 · SHA-256 af1973cfc17dac6a1989d2dd3431fe53093e5f4ec5cdcd8f9bcc9eca21824254_

```
   24 | 
   25 | const char SECP256K1_NAME[] = "secp256k1";
   26 | const char SECP256K1_DECRED_NAME[] = "secp256k1-decred";
```

_file_excerpt · [crypto/curves.c](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/crypto/curves.c#L26) · line 26 · SHA-256 df8e4e49ae68afc481ddc06f8dce5afbfe7451fba7984f22c7d5d57602f2471f_

```
   25 | const char SECP256K1_NAME[] = "secp256k1";
   26 | const char SECP256K1_DECRED_NAME[] = "secp256k1-decred";
   27 | const char SECP256K1_GROESTL_NAME[] = "secp256k1-groestl";
```

_file_excerpt · [crypto/curves.c](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/crypto/curves.c#L27) · line 27 · SHA-256 ed9fb77eedfc925096d5cd8386f66c89e44624dc25a9b75b49b3c11861e85b25_

```
   26 | const char SECP256K1_DECRED_NAME[] = "secp256k1-decred";
   27 | const char SECP256K1_GROESTL_NAME[] = "secp256k1-groestl";
   28 | const char SECP256K1_SMART_NAME[] = "secp256k1-smart";
```

_file_excerpt · [crypto/ecdsa.c](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/crypto/ecdsa.c#L38) · line 38 · SHA-256 44a615006e3d1200cc0d551f228b76e71bc6480255ec5e98e0c98d49cfb275fb_

```
   37 | #include "rfc6979.h"
   38 | #include "secp256k1.h"
   39 | #ifdef USE_SECP256K1_ZKP_ECDSA
```

_file_excerpt · [crypto/ecdsa.c](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/crypto/ecdsa.c#L672) · line 672 · SHA-256 e6ea0e71dbb0e64b63b0e5cb5ceef206cf4767db7abb4f45a5b76f4a23a218dc_

```
  671 |   hasher_Raw(hasher_sign, msg, msg_len, hash);
  672 |   int res = ecdsa_sign_digest(curve, priv_key, hash, sig, pby, is_canonical);
  673 |   memzero(hash, sizeof(hash));
```

_file_excerpt · [crypto/ecdsa.c](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/crypto/ecdsa.c#L983) · line 983 · SHA-256 0809fafc1eba50e65dafc9e1fbeb55b5344f95d8c0a7474d1054332494da2a9c_

```
  982 |   if (!curve) {
  983 |     curve = &secp256k1;
  984 |   }
```

_file_excerpt · [crypto/ecdsa.h](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/crypto/ecdsa.h#L98) · line 98 · SHA-256 9286f08eb43642fb5f95454a9d75f988673971caeab2b04687a958b20033c8e6_

```
   97 |                int (*is_canonical)(uint8_t by, uint8_t sig[64]));
   98 | int ecdsa_sign_digest(const ecdsa_curve *curve, const uint8_t *priv_key,
   99 |                       const uint8_t *digest, uint8_t *sig, uint8_t *pby,
```

_file_excerpt · [crypto/ecdsa.h](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/crypto/ecdsa.h#L130) · line 130 · SHA-256 5ad92182d47e7850613b3230f1ccd1d44384b955791f31f7345f17c971ca1dc7_

```
  129 |                  uint32_t msg_len);
  130 | int ecdsa_verify_digest(const ecdsa_curve *curve, const uint8_t *pub_key,
  131 |                         const uint8_t *sig, const uint8_t *digest);
```

_file_excerpt · [crypto/setup.py](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/crypto/setup.py#L18) · line 18 · SHA-256 35d07f36d6767d0d01fc07a769cd4a7df500e6c1d293d069fe8ef2f79547c1e6_

```
   17 |     "ripemd160",
   18 |     "secp256k1",
   19 |     "sha2",
```

_file_excerpt · [crypto/tools/bip39bruteforce.c](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/crypto/tools/bip39bruteforce.c#L8) · line 8 · SHA-256 de5f2fc1cd87824b1ddf275bb2273a6b7a26fe992025d825d1bbcb429b21a86c_

```
    7 | #include "ecdsa.h"
    8 | #include "secp256k1.h"
    9 | 
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it; introduce an abstraction layer for crypto-agility.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-06103 — Quantum-vulnerable Ed25519: role not determined (4 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium
> **Analyst review (QSI review, 2026-10-28): confirmed by the analyst.** Role resolved. All four anchors are the vendored ed25519-donna implementation, including its keccak and sha3 variants (crypto/ed25519-donna/ed25519-keccak.h, ed25519-sha3.h, ed25519.c, ed25519.h), which the NEM and Monero paths select through hdnode_fill_public_key. This is the Ed25519 implementation itself: the thing a migration replaces, reached by the transaction-signing rows already counted.
- Affected asset: `source-code:Ed25519:general`
- Data source: crypto/ed25519-donna/ed25519-keccak.h
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.2.0 · 2026-10-28 18:57 UTC
- Priority score: 40.2 / 100
- CVSS v3.1: not applicable

21 reference(s) to Ed25519 across 4 file(s), e.g. crypto/ed25519-donna/ed25519-keccak.h:10. Role, judged from paths, function names and nearby code: role not determined. The code does not show what the keys protect; review decides the priority.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open crypto/ed25519-donna/ed25519-keccak.h:10 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [crypto/ed25519-donna/ed25519-keccak.h](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/crypto/ed25519-donna/ed25519-keccak.h#L10) · line 10 · SHA-256 9374afb8171aa7b315e6f8553b4065cfc7badf444f7da8747c0ebb0952478ab0_

```
    9 | 
   10 | void ed25519_publickey_keccak(const ed25519_secret_key sk, ed25519_public_key pk);
   11 | 
```

_file_excerpt · [crypto/ed25519-donna/ed25519-keccak.h](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/crypto/ed25519-donna/ed25519-keccak.h#L12) · line 12 · SHA-256 f1505aedb366f82a780a48e9d03c23168a3f8db8d473041211d4b29183f97ae4_

```
   11 | 
   12 | int ed25519_sign_open_keccak(const unsigned char *m, size_t mlen, const ed25519_public_key pk, const ed25519_signature RS);
   13 | void ed25519_sign_keccak(const unsigned char *m, size_t mlen, const ed25519_secret_key sk, ed25519_signature RS);
```

_file_excerpt · [crypto/ed25519-donna/ed25519-keccak.h](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/crypto/ed25519-donna/ed25519-keccak.h#L13) · line 13 · SHA-256 62dd018334b7d3d19aade9cd71b6ec2e3489d20546ada5a4526524c1a452298b_

```
   12 | int ed25519_sign_open_keccak(const unsigned char *m, size_t mlen, const ed25519_public_key pk, const ed25519_signature RS);
   13 | void ed25519_sign_keccak(const unsigned char *m, size_t mlen, const ed25519_secret_key sk, ed25519_signature RS);
   14 | 
```

_file_excerpt · [crypto/ed25519-donna/ed25519-sha3.h](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/crypto/ed25519-donna/ed25519-sha3.h#L10) · line 10 · SHA-256 d6e35a345375ce78aa3b055f726efa89bca19e06ebee6812d0860f85cb2beb00_

```
    9 | 
   10 | void ed25519_publickey_sha3(const ed25519_secret_key sk, ed25519_public_key pk);
   11 | 
```

_file_excerpt · [crypto/ed25519-donna/ed25519-sha3.h](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/crypto/ed25519-donna/ed25519-sha3.h#L12) · line 12 · SHA-256 c2198e821aab4c59e07fcd1c2d91cc86f51e671156c91f0507e10651d2905566_

```
   11 | 
   12 | int ed25519_sign_open_sha3(const unsigned char *m, size_t mlen, const ed25519_public_key pk, const ed25519_signature RS);
   13 | void ed25519_sign_sha3(const unsigned char *m, size_t mlen, const ed25519_secret_key sk, ed25519_signature RS);
```

_file_excerpt · [crypto/ed25519-donna/ed25519-sha3.h](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/crypto/ed25519-donna/ed25519-sha3.h#L13) · line 13 · SHA-256 5acc5cdff3b6d75ed5c1bef9fafbf2bd5939f58ea63f04710fd8141fd0cb9bc7_

```
   12 | int ed25519_sign_open_sha3(const unsigned char *m, size_t mlen, const ed25519_public_key pk, const ed25519_signature RS);
   13 | void ed25519_sign_sha3(const unsigned char *m, size_t mlen, const ed25519_secret_key sk, ed25519_signature RS);
   14 | 
```

_file_excerpt · [crypto/ed25519-donna/ed25519.c](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/crypto/ed25519-donna/ed25519.c#L47) · line 47 · SHA-256 2375eee09341b31cd7358c1363832b24e0732231c1b4f60360bd51325ac231d2_

```
   46 | void
   47 | ED25519_FN(ed25519_publickey) (const ed25519_secret_key sk, ed25519_public_key pk) {
   48 | 	hash_512bits extsk = {0};
```

_file_excerpt · [crypto/ed25519-donna/ed25519.c](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/crypto/ed25519-donna/ed25519.c#L50) · line 50 · SHA-256 e40eeeebef9f32d11972a9b630385dd03bbfd34fd827f55fa6e274bd440316f3_

```
   49 | 	ed25519_extsk(extsk, sk);
   50 | 	ed25519_publickey_ext(extsk, pk);
   51 | 	memzero(&extsk, sizeof(extsk));
```

_file_excerpt · [crypto/ed25519-donna/ed25519.c](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/crypto/ed25519-donna/ed25519.c#L108) · line 108 · SHA-256 5cf2afb8cd79ce2bc6441aa80d3579ee0b34b2b90585209ca6135a4cdbee681c_

```
  107 | void
  108 | ED25519_FN(ed25519_sign_ext) (const unsigned char *m, size_t mlen, const ed25519_secret_key secret_scalar, const ed25519_secret_key skext, ed25519_signature RS) {
  109 | 	ed25519_hash_context ctx;
```

_file_excerpt · [crypto/ed25519-donna/ed25519.h](https://github.com/trezor/trezor-firmware/blob/72489948b3c44a37598de9da658be28e4fabb4ae/crypto/ed25519-donna/ed25519.h#L12) · line 12 · SHA-256 ab884f62531724e35b3e585259b46eeddf4ec6fb71606706c23b5537f02e91b2_

```
   11 | 
   12 | typedef unsigned char ed25519_signature[64];
   13 | typedef unsigned char ed25519_public_key[32];
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

### Post-quantum maturity: Level 3 of 4 — hybrid protection in a critical path

- Hybrid — firmware and boot verification (root of trust): core/embed/sec/image/boot_header.c (Ed25519 + SLH-DSA)
- In use: SLH-DSA — core/embed/sec/image/boot_header.c
- In use: ML-DSA — core/embed/sec/mcu_attestation/inc/sec/mcu_attestation.h
- In use: ML-DSA — core/embed/sec/mcu_attestation/mcu_attestation.c
- In use: ML-DSA — core/embed/sec/secret/unix/certs/T3W1.der (DER) — T3W1 Trezor Safe 7
- In use: ML-DSA — core/embed/sec/secret_keys/inc/sec/secret_keys.h
- Present, not wired: ML-DSA — core/embed/sec/mldsa44/inc/sec/mldsa44.h
- Present, not wired: ML-DSA — core/embed/sec/mldsa44/mldsa44.c
- Classical only — channel key exchange (TLS, Noise, handshakes): X25519 (3 file(s))

**Next step:** Cover the remaining classical critical roles and plan when the classical half can be dropped.

_Levels: 0 none; 1 present, not wired; 2 in use outside the critical paths; 3 hybrid in a critical path; 4 post-quantum by default in the critical paths (root of trust, key wrapping, channel key exchange). Judged from code and manifests._

### What the quantum-vulnerable algorithms do

| Role | Algorithms (files) | ID | First step |
|---|---|---|---|
| **firmware and boot verification (root of trust)** | Ed25519 (2) | QSI-2026-06095 | Plan a hybrid firmware signature (the classical one plus ML-DSA or SLH-DSA, both required) and the path to ship the new keys in a bootloader update |
| **channel key exchange (TLS, Noise, handshakes)** | X25519 (3) | QSI-2026-06097 | Move the handshake to a hybrid key exchange (X25519MLKEM768 in TLS 1.3; a hybrid KEM in Noise-based protocols) |
| **transaction and message signing** | ECDSA (17), Ed25519 (16), Schnorr (BIP-340) (14) | QSI-2026-06098, QSI-2026-06101, QSI-2026-06104, QSI-2026-06105 | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains adopt them |
| **authentication and identity (certificates, tokens, device attestation)** | ECDSA (2) | QSI-2026-06096 | Keep credentials short-lived and plan ML-DSA certificates, tokens and keys as the ecosystem supports them |
| **role not determined** | ECDSA (8), Ed25519 (4), X25519 (3), ECDH (1) | QSI-2026-06099, QSI-2026-06100, QSI-2026-06102, QSI-2026-06103 | Classify each usage, record data lifetimes, and plan migration to Hybrid key establishment with ML-KEM (FIPS 203), e.g. X25519MLKEM768 in TLS 1.3 or mlkem768x25519-sha256 in SSH; introduce an abstraction layer for crypto-agility |

_Roles are judged from file paths, function names and the code around each match; review confirms them. Root-of-trust keys and wrapped keys come first: they are hard to replace or can be recorded today._
No readiness questionnaire was completed for this project.

### Quantum algorithms relevant to this inventory

| Quantum algorithm | Effect | Attack model | Inventoried algorithms (rows) | What it means for this audit |
|---|---|---|---|---|
| Shor's algorithm — elliptic-curve discrete logarithms | breaks | Q1 | ECDH (1), ECDSA (27), Ed25519 (29), Schnorr (BIP-340) (4), X25519 (12) | Elliptic-curve keys are expected to fall before RSA keys of comparable classical strength. On blockchains, coins whose public key is already on chain (reused addresses, pay-to-public-key and Taproot outputs) are exposed first; plan the move to post-quantum signatures and avoid key reuse in the meantime. |
| Grover's algorithm — key search and preimages | weakens (larger keys restore the margin) | Q1 | BLAKE2 (5), ChaCha20-Poly1305 (2), HMAC (4), Keccak-256 (4), PBKDF2 (2), Poly1305 (3), RC4 (2), RIPEMD-160 (2), SHA-2 (2), SHA-3 (5), SLH-DSA (1) | Not a break. 256-bit keys (AES-256, ChaCha20) keep a comfortable margin; AES-128 meets NIST category 1, while some authorities ask for 256-bit keys in quantum-resistant contexts (see the AES-128 entry). Prefer 256-bit keys for long-lived data; 256-bit hashes need no change for preimage resistance. |
| Brassard–Høyer–Tapp — collision search | weakens (larger keys restore the margin) | Q1 | BLAKE2 (5), Keccak-256 (4), RIPEMD-160 (2), SHA-2 (2), SHA-3 (5) | 256-bit hashes (SHA-256, SHA3-256) remain adequate for collision resistance; 160-bit hashes are already weak classically (SHA-1 collisions are practical). Use 384/512-bit hashes where NIST categories 4–5 are required. |
| Quantum lattice sieving | included in standard parameters | Q1 | ML-DSA (6) | No change for ML-KEM or ML-DSA at the standard parameter sets. A 2024 claim of a polynomial-time quantum LWE algorithm was withdrawn after a bug was found (see claims). |

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
| P3 | QSI-2026-06105 | Add ECDSA, Ed25519, Schnorr (BIP-340) usages at the wallet's transaction signing to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-06095 | Add Ed25519 usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-06097 | Add X25519 usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-06098 | Add ECDSA usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-06101 | Add Ed25519 usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-06104 | Add Schnorr (BIP-340) usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-06096 | Add ECDSA usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-06099 | Add ECDH usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-06100 | Add X25519 usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-06102 | Add ECDSA usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-06103 | Add Ed25519 usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P4 | QSI-2026-06105 | Plan migration of ECDSA, Ed25519, Schnorr (BIP-340) to ? (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ? or a hybrid scheme in use. |
| P4 | QSI-2026-06095 | Plan migration of Ed25519 to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-06097 | Plan migration of X25519 to Hybrid key establishment with ML-KEM (FIPS 203), e.g. X25519MLKEM768 in TLS 1.3 or mlkem768x25519-sha256 in SSH (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows Hybrid key establishment with ML-KEM (FIPS 203), e.g. X25519MLKEM768 in TLS 1.3 or mlkem768x25519-sha256 in SSH or a hybrid scheme in use. |
| P4 | QSI-2026-06098 | Plan migration of ECDSA to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-06101 | Plan migration of Ed25519 to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-06104 | Plan migration of Schnorr (BIP-340) to  (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows  or a hybrid scheme in use. |
| P4 | QSI-2026-06096 | Plan migration of ECDSA to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-06099 | Plan migration of ECDH to Hybrid key establishment with ML-KEM (FIPS 203), e.g. X25519MLKEM768 in TLS 1.3 or mlkem768x25519-sha256 in SSH (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows Hybrid key establishment with ML-KEM (FIPS 203), e.g. X25519MLKEM768 in TLS 1.3 or mlkem768x25519-sha256 in SSH or a hybrid scheme in use. |
| P4 | QSI-2026-06100 | Plan migration of X25519 to Hybrid key establishment with ML-KEM (FIPS 203), e.g. X25519MLKEM768 in TLS 1.3 or mlkem768x25519-sha256 in SSH (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows Hybrid key establishment with ML-KEM (FIPS 203), e.g. X25519MLKEM768 in TLS 1.3 or mlkem768x25519-sha256 in SSH or a hybrid scheme in use. |
| P4 | QSI-2026-06102 | Plan migration of ECDSA to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-06103 | Plan migration of Ed25519 to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |

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
| RC4 |  |  | weak classically | broken | 2 | 2 | crypto/rc4.c; crypto/rc4.h |
| RIPEMD-160 | RIPEMD-160 |  | weak classically | legacy | 2 | 2 | crypto/ripemd160.c; crypto/ripemd160.h |
| ChaCha20-Poly1305 | ChaCha20-Poly1305 |  | reduced margin (Grover), approved | acceptable | 2 | 2 | crypto/chacha20poly1305/chacha20poly1305.c:13; crypto/chacha20poly1305/chacha20poly1305.h:13 |
| HMAC |  |  | reduced margin (Grover), approved | acceptable | 4 | 4 | crypto/hmac.c; crypto/hmac.h; crypto/hmac_drbg.c |
| PBKDF2 |  |  | reduced margin (Grover), approved | acceptable | 2 | 2 | crypto/pbkdf2.c; crypto/pbkdf2.h |
| Poly1305 |  |  | reduced margin (Grover), approved | acceptable | 3 | 3 | crypto/chacha20poly1305/poly1305-donna-32.h; crypto/chacha20poly1305/poly1305-donna.c; crypto/chacha20poly1305/poly1305-donna.h |
| BLAKE2 |  |  | Grover: acceptable to NIST, below ECCG/ANSSI guidance | acceptable | 5 | 5 | crypto/blake2_common.h; crypto/blake2b.c; crypto/blake2b.h |
| Keccak-256 | Keccak-256 |  | Grover: acceptable to NIST, below ECCG/ANSSI guidance | acceptable | 4 | 4 | crypto/bip32.c:558; crypto/nem.c:135; crypto/sha3.c:397 |
| SHA-2 |  |  | Grover: acceptable to NIST, below ECCG/ANSSI guidance | acceptable | 2 | 2 | crypto/sha2.c; crypto/sha2.h |
| SHA-3 |  |  | Grover: acceptable to NIST, below ECCG/ANSSI guidance | acceptable | 5 | 5 | crypto/ed25519-donna/ed25519-hash-custom-sha3.h; crypto/ed25519-donna/ed25519-sha3.c; crypto/ed25519-donna/ed25519-sha3.h |
| ML-DSA |  |  | post-quantum | acceptable | 5 | 5 | core/embed/sec/mcu_attestation/inc/sec/mcu_attestation.h:24; core/embed/sec/mcu_attestation/mcu_attestation.c:31; core/embed/sec/mldsa44/inc/sec/mldsa44.h:25 |
| ML-DSA | ML-DSA-44 |  | post-quantum | acceptable | 1 | 1 | core/embed/sec/secret/unix/certs/T3W1.der (DER) — T3W1 Trezor Safe 7 |
| SLH-DSA |  |  | post-quantum | acceptable | 1 | 1 | core/embed/sec/image/boot_header.c:30 |
| ECDH |  |  | vulnerable (Shor) | acceptable | 1 | 1 | crypto/bip32.c:702 |
| ECDSA | secp256k1 |  | vulnerable (Shor) | acceptable | 17 | 17 | common/protob/messages-benchmark.proto:2; common/protob/messages-bitcoin.proto:2; common/protob/messages-ethereum-eip712.proto:2 |
| ECDSA | secp256k1, P-256 |  | vulnerable (Shor) | acceptable | 2 | 2 | common/protob/messages-eos.proto:2; common/protob/messages-tezos.proto:2 |
| ECDSA |  |  | vulnerable (Shor) | acceptable | 8 | 8 | core/embed/sec/optiga/optiga_commands.c:1055; core/embed/sec/optiga/unix/optiga.c:58; crypto/bip32.c:670 |
| Ed25519 | BIP32-Ed25519 |  | vulnerable (Shor) | acceptable | 1 | 1 | common/protob/messages-cardano.proto:2 |
| Ed25519 | CLSAG ring signatures on the Ed25519 curve |  | vulnerable (Shor) | acceptable | 1 | 1 | common/protob/messages-monero.proto:2 |
| Ed25519 | Keccak-512 variant |  | vulnerable (Shor) | acceptable | 1 | 1 | common/protob/messages-nem.proto:2 |
| Ed25519 |  |  | vulnerable (Shor) | acceptable | 4 | 4 | common/protob/messages-ripple.proto:2; common/protob/messages-solana.proto:2; common/protob/messages-stellar.proto:2 |
| Ed25519 | Ed25519 |  | vulnerable (Shor) | acceptable | 22 | 22 | core/embed/sec/image/boot_header.c:81; core/embed/sec/image/image.c:190; crypto/bip32.c:477 |
| Schnorr (BIP-340) | secp256k1, Taproot |  | vulnerable (Shor) | acceptable | 2 | 2 | common/protob/messages-benchmark.proto:2; common/protob/messages-bitcoin.proto:2 |
| Schnorr (BIP-340) |  |  | vulnerable (Shor) | acceptable | 2 | 2 | crypto/zkp_bip340.c:139; crypto/zkp_bip340.h |
| X25519 | X25519 |  | vulnerable (Shor) | acceptable | 6 | 6 | core/embed/sec/tropic/tropic.c:383; crypto/bip32.c:485; crypto/ed25519-donna/ed25519.c:274 |
| X25519 |  |  | vulnerable (Shor) | acceptable | 6 | 6 | crypto/ed25519-donna/curve25519-donna-32bit.c; crypto/ed25519-donna/curve25519-donna-32bit.h; crypto/ed25519-donna/curve25519-donna-helpers.c |

_Long lists are grouped here; the full per-file list is in the JSON report, signed with the same key._

## Appendices: Input files

| File | Size | SHA-256 | Redactions |
|---|---|---|---|
| common/protob/check.py | 1462 | `a1ffbf48b6690b8f01cbcfec154342846af9462ae5d47b23a3b2a2fbcd22a077` | 0 |
| common/protob/graph.py | 2082 | `1a60fccc6ea36a1339669ddb296f1b456b1bbe31419dc3b820e19e22d74cde28` | 0 |
| common/protob/messages-benchmark.proto | 923 | `8f6a6137c4158b2df1caf34b8d4fae8cf4acdb9968a37e5481bb657fae21b4c2` | 0 |
| common/protob/messages-bitcoin.proto | 28370 | `58e11f34625d55b9f62328a9b15b51843e02d34dd5da5d276c392c9d6db68b7f` | 0 |
| common/protob/messages-ble.proto | 741 | `67831e5b157e206dd1d3c2fc70b51b42160e8fd0b5f602a252dc2cd168c5dd0a` | 0 |
| common/protob/messages-bootloader.proto | 1116 | `9b0da32e12699c8f6ed114761f6a10cd06dfbc18cb649a50a238ac19962b2ed8` | 0 |
| common/protob/messages-cardano.proto | 18660 | `a6bec889024e85fe2f5bdc8f4730b975593443567b6cdaa7f189d6b1aa71a828` | 0 |
| common/protob/messages-common.proto | 7180 | `dbe669e87ef07922b0baf13b824337a3fc2b52b48f2c429970f3d76e59c80a35` | 0 |
| common/protob/messages-crypto.proto | 3191 | `835b80f7132972a7ca38848320cbc40223899c9950b17e1fcc11e3239f2d3b64` | 0 |
| common/protob/messages-debug.proto | 10196 | `6712380787106b9cc6fc9d31d36cf7d1b66b3eb838ca90d63629561e98a59c1e` | 0 |
| common/protob/messages-definitions.proto | 6388 | `9b4d80e3e6e9a801614a9255596a22f1e7006e5b393e3be8e1ab7349274f73e7` | 0 |
| common/protob/messages-eos.proto | 8913 | `1f78ce827ea132d06975f586fd492727d9b62436363488095c1b180ff4a09c32` | 0 |
| common/protob/messages-ethereum-eip712.proto | 3449 | `30fb535d393c3e61a0804b6298ef83beedc955eaf4da41ee071f16357dafd2f6` | 0 |
| common/protob/messages-ethereum.proto | 10198 | `33d2cdc65b0c0bf310be078947d753157417101dd8c638030766f101de078d34` | 0 |
| common/protob/messages-evolu.proto | 2725 | `cde2c188f13fab325586b5cfa84cfa8992157d6b82fa4284e7fb94e8f29c82a1` | 0 |
| common/protob/messages-extapp.proto | 3245 | `ea931433e9605db80b90afc41a1c2a3ab60d22da37d9134babfd82b1b8d2230c` | 0 |
| common/protob/messages-management.proto | 30329 | `1d1b306fc65adfaaa1b598e0948b70cc3259afac9ee0c7bd1196e3ca924509d1` | 0 |
| common/protob/messages-monero.proto | 15967 | `b5b5d9b971f5834db8b41901cf6e89fcfa491e6ac3e8bc26287465b8881ee4d2` | 0 |
| common/protob/messages-nem.proto | 9176 | `e6ecf0bbfe659e11be4866389d0e4c9f67b9e5fbb78e13f2460c3ecaf517eedb` | 0 |
| common/protob/messages-nostr.proto | 1809 | `778854486467aca41a9cf2678d309661017954bfbbdc8e42c6a9565a964727ef` | 0 |
| common/protob/messages-ripple.proto | 2896 | `c243dd611be61edf5f61ee968b23b63bfa6697cd043eca622f30e9bda81b7a35` | 0 |
| common/protob/messages-solana.proto | 3744 | `5132eea2e4101bf61d44e7c827d433aa82ed5b851d25e123c2244f456e969b0a` | 0 |
| common/protob/messages-stellar.proto | 25096 | `196c94ae6af8d1fc97c0f0ed30c78a2baa71ca4600da9dc4b2bdd31f15159773` | 0 |
| common/protob/messages-telemetry.proto | 845 | `43ba424447f061e44d3fde5e204dc032fd812e112f521e3331a7218a71967cf8` | 0 |
| common/protob/messages-tezos.proto | 5841 | `890233da5bd6398bb2de5037c4f4018269179b85eff85a46028f679fb707b934` | 0 |
| common/protob/messages-thp.proto | 9651 | `8e998a47a134e7a31cb8c26879dd714859ce0d4e68bb0c891c0baf0b680b3624` | 0 |
| common/protob/messages-tron.proto | 9885 | `f01e34d9ac5d45c1e208a78a818651e98f243ce1231c6f3b15119fad3068908b` | 0 |
| common/protob/messages-webauthn.proto | 1689 | `849f10aa7618f62032bfe1da7ebb5b9458af0441876c9a31c03fb32fc39c480c` | 0 |
| common/protob/messages.proto | 25205 | `a71b012dbb7d07f74c58cdc7a4afeb9616bb160ccd851e565156580a1d7f5687` | 0 |
| common/protob/options.proto | 3772 | `91cdd9232d1e08fef809b9814e33ab07a5a0e4885ea10ee71a1f9785106d27a7` | 0 |
| core/embed/projects/bootloader/Cargo.toml | 4129 | `6faa232eefde225a4e739da8b9a2a273e3cd76ca8e90cf9ab2b4bee96508e06d` | 0 |
| core/embed/projects/bootloader/bootui.c | 4687 | `6a551b35d4313e5f0c2fd9e1b33a3c1c0072231e2e3d51d696a612576414303c` | 0 |
| core/embed/projects/bootloader/bootui.h | 2668 | `7dc4f0217734cf6e580d5ae3779734041eab0cc9ea52c2f21caa7582fac31e98` | 0 |
| core/embed/projects/bootloader/build.rs | 2480 | `a275a9f3046d4314781186749d17615a7556dd429c050b4926e26e445325c593` | 0 |
| core/embed/projects/bootloader/emulator.c | 6765 | `d0393aaa563d021389ae61ec9315e5b022715c12173c403ba9689ef29dcc60a3` | 0 |
| core/embed/projects/bootloader/emulator.h | 849 | `77c4d5ef0cc6835fb444be4dd89f3fa3c4aaa92354575289bec9eb39c7830fb5` | 0 |
| core/embed/projects/bootloader/fw_check.c | 9048 | `369b3baa6960337efe794eaa7018ef32482a2aa836300bc109e91163597c1b04` | 0 |
| core/embed/projects/bootloader/fw_check.h | 4973 | `26f0183f8f4b2529d63c243b346ff5f92ef9d13c8711dfc7ceaef42d8d2c37ca` | 0 |
| core/embed/projects/bootloader/header_pq.c | 2590 | `72968e66a51497fd923272028f7f5440cf2358871b4f3d48742b9a958a15b313` | 0 |
| core/embed/projects/bootloader/main.c | 16005 | `91d266698a86858f4bd4acac9b6902ad11c0bb8923673506f22e2b2c96a7085c` | 0 |
| core/embed/projects/bootloader/protob/pb/messages-debug.pb.c | 579 | `30166dca7cf97a98e327c23aa185687e88a59d58f8eab6781268f45c2b6d8a25` | 0 |
| core/embed/projects/bootloader/protob/pb/messages-debug.pb.h | 13006 | `ef12062b1ff5e318aa88beeabc403c52cc3c9f95ec25cad709482288956841f8` | 0 |
| core/embed/projects/bootloader/protob/pb/messages-debug.proto | 4004 | `7bff5f5a52d9487be34df297354b9bebb0c5c5626f29b510388d94df7fd55fd9` | 0 |
| core/embed/projects/bootloader/protob/pb/messages.pb.c | 763 | `906fa5d22128433b3b478a76a4de3eef4f6bbdbfeecd7900db2d445f6e75e96f` | 0 |
| core/embed/projects/bootloader/protob/pb/messages.pb.h | 15305 | `aee15b545bdb3b9eef1cba9f82f264643c0c7f8ff4c4ab63f29a672e7c8647d1` | 0 |
| core/embed/projects/bootloader/protob/pb/messages.proto | 5529 | `3814ee49ce4767c6434a294451e77eef1671344f0305f5d9cbc47e595bb408ed` | 0 |
| core/embed/projects/bootloader/protob/protob.c | 7347 | `a909b4f76772c97553d58fd6beb77a7e30f06ca9bc10810dce2cf2e688f25ff7` | 0 |
| core/embed/projects/bootloader/protob/protob.h | 2308 | `65860166f5b7af173285b49d6963e6a44f75446e7c123c57d5338b9281ef746a` | 0 |
| core/embed/projects/bootloader/protob/protob_common.h | 3052 | `48cb5836996acfa321a9ca58e358da41190753886f5e1f2813fb6a633f6d0043` | 0 |
| core/embed/projects/bootloader/protob/protob_debug.c | 2920 | `c8973541cf462776b9b94d453ecc59a0b1fe60d720c3cebb6880cc514f95d11b` | 0 |
| core/embed/projects/bootloader/protob/protob_debug.h | 1365 | `a6b0c0b52b7f0c52105875b0933ce6b7a78db924fbbe5fe70f36fc588f6f41cc` | 0 |
| core/embed/projects/bootloader/src/main.rs | 125 | `9e6acc25712dac4982a96e90d6c740faebce1e78891df7b5863f6b00c77c754a` | 0 |
| core/embed/projects/bootloader/ui_helpers.c | 3135 | `380600c12f121c2f6433fbf745624488e7094552bea7985986b230c7eed2220d` | 0 |
| core/embed/projects/bootloader/ui_helpers.h | 951 | `7f7650a1737c6829a5502aa9c8fa03b8fa051f6d11b60cfa4a4a1f1fa63afda2` | 0 |
| core/embed/projects/bootloader/version.h | 414 | `3c5cf64b2af97f5a77b016d53aa7b8ea2e242976e3c2bf7f196fd5c5ef08f2b8` | 0 |
| core/embed/projects/bootloader/version_check.c | 3049 | `c2e62aaa755e802a113d7839cd407743330d2ecd94f50d676fa707e5353ddbf0` | 0 |
| core/embed/projects/bootloader/version_check.h | 1883 | `74e7c51d3e8737385e7da2e51f182b6e37419b2d560d9baa7b311dcf2e091319` | 0 |
| core/embed/projects/bootloader/wire/codec_v1.c | 7264 | `d03b7743f42e3f176fbfef8f0204fcb891c9678b5c4fec14fcd78aab95c3e30b` | 0 |
| core/embed/projects/bootloader/wire/codec_v1.h | 1811 | `b2c113dd0e7502aea3eb8fc01fae5d990ad0b74940ee0de190875dc358d8c0af` | 0 |
| core/embed/projects/bootloader/wire/debug_iface_usb.c | 2591 | `7ecedb924bc2a001bbd15f937fb20a849a6941480e0ae6a79266adf7daa9aec8` | 0 |
| core/embed/projects/bootloader/wire/debug_iface_usb.h | 909 | `0f1feaa29a0dc9b048d86e35891cc1829d6e57da0c6e06b9df71552c3308248b` | 0 |
| core/embed/projects/bootloader/wire/wire_iface_ble.c | 4548 | `0b1753453caa6eb671f9c0ab996ee46b48620c3ea00e08af5aa31aca61628610` | 0 |
| core/embed/projects/bootloader/wire/wire_iface_ble.h | 963 | `d091fec78cfb45f8d455f43e0a7770dc92c429818d04de7984bf351a8420a457` | 0 |
| core/embed/projects/bootloader/wire/wire_iface_usb.c | 2677 | `bd2014667fe0768fe1997f15bf64510312c8d254f48fc9fb9d743851d1d27bda` | 0 |
| core/embed/projects/bootloader/wire/wire_iface_usb.h | 931 | `4c2223b02ca7dc117c3329fb51f79641721ad6453ad92b655476f4b281899d24` | 0 |
| core/embed/projects/bootloader/workflow/debuglink.c | 5313 | `9ded890ae9c388785ff1a04cc94e2a37da2821c9ceccb8ec548dbc3dce40bde4` | 0 |
| core/embed/projects/bootloader/workflow/debuglink.h | 1030 | `033ef235c113f65d1dfd396dd0c6ac307cf3466dbf6731c43ac80006f7a94548` | 0 |
| core/embed/projects/bootloader/workflow/wf_auto_update.c | 1506 | `55fcaefcd28ef58441aec0c8dbc29a729c4a8bcfd85fe4810ad285232afb1c06` | 0 |
| core/embed/projects/bootloader/workflow/wf_ble_pairing_request.c | 5153 | `7c2a0197c1e2bcbc6dbd676ed4f9a68a6c8024be34277c901bc5b3897697d12b` | 0 |
| core/embed/projects/bootloader/workflow/wf_bootloader.c | 6709 | `c04c6b143de803a3f9f3e91e751ba4179a5ef20f65b214cb158b4f3e388578bd` | 0 |
| core/embed/projects/bootloader/workflow/wf_empty_device.c | 2528 | `c63aa59e1973af055fe81ab8d18f086e49d789805ba97e4d3833e218aa8a400a` | 0 |
| core/embed/projects/bootloader/workflow/wf_firmware_update.c | 16214 | `756c14cd1232b84b4df8eb5620b680e3519ec5a4dfe5c5f8f150cbba9b562d1e` | 0 |
| core/embed/projects/bootloader/workflow/wf_get_features.c | 1092 | `d9926653fd42f2785146cb508fafe7c265af7c71cdfa1446c2b5ca6218cd50a6` | 0 |
| core/embed/projects/bootloader/workflow/wf_host_control.c | 3593 | `60048eed5077390148f8a19ae1ef57edd1aa90c7c8d1ae5167fbbf66174f28a1` | 0 |
| core/embed/projects/bootloader/workflow/wf_image_upload.c | 12925 | `97384d25e91aa218ae444f5e78ee4dbc0f096b66c7488acffb118332178b8465` | 0 |
| core/embed/projects/bootloader/workflow/wf_image_upload.h | 7859 | `673f9ae576932eafa3981c47a47ab7663619f782943fd63b31e6a2ba0e5176e8` | 0 |
| core/embed/projects/bootloader/workflow/wf_initialize.c | 1085 | `f20614547336a484c9470b450bd91554a5d4eae9c8550c3071e39fd6731a7069` | 0 |
| core/embed/projects/bootloader/workflow/wf_ping.c | 1057 | `257907c1010f92d5fbff8b4225be8849dccc3c5e075c448c319bf39651bc9b7f` | 0 |
| core/embed/projects/bootloader/workflow/wf_unlock_bootloader.c | 1585 | `7b70feac57098fec83d6fdb2c14951e1835d17c869ec66377ef4d80c5013ffb7` | 0 |
| core/embed/projects/bootloader/workflow/wf_wipe_device.c | 3183 | `5dc051121baa1d70c14f0f6563e0ed694088e96e6ead48301266ff8bc2a62e5b` | 0 |
| core/embed/projects/bootloader/workflow/workflow.h | 2384 | `e407e9abd43800b10e5e3f4fbd7991133329656c9535049272c8122ec83420f4` | 0 |
| core/embed/projects/bootloader/workflow/workflow_common.h | 1263 | `bfa9440135ca5a4459795308c70e7132bf5e0d9ea3cbe5fc7987c3db0268a533` | 0 |
| core/embed/sec/Cargo.toml | 2374 | `01f264a9101775c0eb48517fec082bb1643e95f06886ea54d9907e2d5c2ac8b6` | 0 |
| core/embed/sec/backup_ram/backup_ram_crc.c | 1283 | `9a16d2b783c1197df005802bb4c109047da9bea104a8d7562534ca7b78575b70` | 0 |
| core/embed/sec/backup_ram/backup_ram_crc.h | 1386 | `d9edf2201a3c57d49f13c57ac7cfe49fe29448a5f5de2af2dce1223da09c21e8` | 0 |
| core/embed/sec/backup_ram/build.rs | 506 | `2d1283b95f503ff9fac8f4770c6a528955e9cf1d9d6d763597af8d5cd1cc2ef9` | 0 |
| core/embed/sec/backup_ram/inc/sec/backup_ram.h | 4424 | `86ae1f8e77c992f6ae3d4257b1ab9b45dd30b30bbb0107ee54a69146493611b8` | 0 |
| core/embed/sec/backup_ram/stm32u5/backup_ram.c | 14131 | `958852dc3fc1a6711fc781623167f51ae6cf893aa5a9589a9e74772c17c51599` | 0 |
| core/embed/sec/backup_ram/unix/backup_ram.c | 1442 | `e03af58cc7db205c71c0f5577bb02e12b64b0816aa2c38dfe1456d6f03dfe433` | 0 |
| core/embed/sec/board_capabilities/build.rs | 440 | `9b2b071dc5e8caa49d4477b183e674fd2099e6fe05fcdc22985be76ef7477d6f` | 0 |
| core/embed/sec/board_capabilities/inc/sec/board_capabilities.h | 2354 | `6972e1d6c6786bc2638f997289a0e118f7d8829353489512f47d6b353a773cb6` | 0 |
| core/embed/sec/board_capabilities/stm32/board_capabilities.c | 2366 | `68bd92926a40e379a7e28f934591bd30e9a1de0087b1e0a6605f039b6cb8a091` | 0 |
| core/embed/sec/board_capabilities/unix/board_capabilities.c | 1238 | `ac750ab207d3ac08ed5f34787e3cb4734ab656c5643cfd23d45ef3e3f69fe8e4` | 0 |
| core/embed/sec/build.rs | 3173 | `f8373796793e1f74f00bab4344f2571e1cbf8c212c79e09d08373584a05f0b6b` | 0 |
| core/embed/sec/consumption_mask/build.rs | 607 | `3832993d984fdd6482dec26222f25559141f7146440ff136f394ccf7f939fa55` | 0 |
| core/embed/sec/consumption_mask/inc/sec/consumption_mask.h | 951 | `51c6c87525c741b3d1dcf176063b668dfdfb6ce1a70af9b74727f24a07cbc381` | 0 |
| core/embed/sec/consumption_mask/stm32f4/consumption_mask.c | 4000 | `fb10fe34e200e9e5157fc591ed9d82547c1d593b116e004ea2e0ed90f0146053` | 0 |
| core/embed/sec/consumption_mask/stm32u5/consumption_mask.c | 5449 | `e71ad31a9754e0447230099ceb689b3973a8932e84521abaeca88d415d482560` | 0 |
| core/embed/sec/consumption_mask/unix/consumption_mask.c | 861 | `8370922fd2ed99c5a6aa468b770074a355b2d494a3abe39cf4019475e0fb5f48` | 0 |
| core/embed/sec/fwutils/build.rs | 179 | `df6e58b25c14babbb3f7b0e43903b471f21bbf19a6d5a3c5ce87572061bf7841` | 0 |
| core/embed/sec/fwutils/fwutils.c | 3732 | `1e9ba3553be64d1a9367e78ef35cb173c80a5d499d0039f0066047d17615c735` | 0 |
| core/embed/sec/fwutils/inc/sec/fwutils.h | 2151 | `75ba689a500f275efc5ee959fecc65f59fbb8b3c1586065c8355ef2afc84380e` | 0 |
| core/embed/sec/hash_processor/build.rs | 449 | `d2ff48c9a719cf3964cc956244f759f6ff1e8bb4a4435046ffc83782ecccb7fb` | 0 |
| core/embed/sec/hash_processor/inc/sec/hash_processor.h | 1819 | `f3d39b7a288559fc9b693c6e4977d3271f6f8e8b678573a880394659b161cc5c` | 0 |
| core/embed/sec/hash_processor/stm32u5/hash_processor.c | 5031 | `1c9eaecfe35d94793b57533e81e29b7787f997ea599af7afd81aaf53a71dff79` | 0 |
| core/embed/sec/hw_revision/build.rs | 456 | `1bf9a59aa0c0f0f41e8ce87c2e1c64ed6a60014e94c34d49015492cd9630567a` | 0 |
| core/embed/sec/hw_revision/inc/sec/hw_revision.h | 886 | `c3ec55542bb28dadba8b2c516c8a7f2fb23280bd348a4f097a8845d24989c894` | 0 |
| core/embed/sec/hw_revision/stm32/hw_revision.c | 3504 | `ae7401335382db8852a2e4a758e7bca580dc61c317061a684448b48d26da1c2c` | 0 |
| core/embed/sec/hw_revision/unix/hw_revision.c | 892 | `ea7adc245f9512046791e42e6107551137d0c869a2157b9093b49e178bf4d7cb` | 0 |
| core/embed/sec/image/boot_header.c | 8961 | `4506855d1b81cc19bb839d161266bed6404090dc9628c47de448fd17206b1df4` | 0 |
| core/embed/sec/image/build.rs | 802 | `d12f9a339b3d935fc9436d9fb1e7b46c2b48e195eccf1364f5f1ae82274bddc5` | 0 |
| core/embed/sec/image/image.c | 18805 | `3977fe12259f229c80c911094ff36164c6def2f15b20c36c6597edfac3997fef` | 0 |
| core/embed/sec/image/inc/sec/boot_header.h | 7371 | `ca6e16ae99fcf8c11ef8edfb7798b76a3597cf10e56d3f044f80d2dce255cf08` | 0 |
| core/embed/sec/image/inc/sec/boot_image.h | 2298 | `cbc400d0007a81fa57403075d53d2ad09cc80d3636299ca8fb9c6d0aa1583cdc` | 0 |
| core/embed/sec/image/inc/sec/boot_ucb.h | 2915 | `2b3ec18c71444c07bb42617ac64fce3e69e0df8cb05799a70f0d2e5e2318b6ef` | 0 |
| core/embed/sec/image/inc/sec/image.h | 6525 | `2654a3304e5ab4837b21c8dd7c8da6564abfdd879d3e203a615dd15d66870139` | 0 |
| core/embed/sec/image/inc/sec/image_hash_conf.h | 2230 | `71b096c8a9966115e7ee2aa0f3ebcbf1dd20bb1490e1528f7770eaf8292ab6f7` | 0 |
| core/embed/sec/image/inc/sec/root_keys.h | 3760 | `faa1c126b0259937d2d28dd42528dba2c97c84f23f74e41fa8cf745d918df268` | 0 |
| core/embed/sec/image/stm32/boot_image.c | 9817 | `d00f22374d6217e90f0dbed8b79f56771669e2d0db7e7985abb9152159511c93` | 0 |
| core/embed/sec/image/stm32/boot_ucb.c | 5523 | `d92657cf121e1c55702538bb48490d8e17d427756fc08f576ced87a31414821e` | 0 |
| core/embed/sec/image/unix/boot_ucb.c | 828 | `a42f7e49e37e82964facd48cc8d23e4e8255d55d74049aebb1f26c1fe74178df` | 0 |
| core/embed/sec/iwdg/build.rs | 414 | `1c7146464c3a4e0ba13ea8d29fea2ae8468644223bf7f522d50ac52dd083c55f` | 0 |
| core/embed/sec/iwdg/inc/sec/iwdg.h | 1288 | `dc19d91df2bdd576f9f8f042eb8796ca932fc7f90bd70b00c3e067753e34ed0e` | 0 |
| core/embed/sec/iwdg/stm32/iwdg.c | 1448 | `629e75f096e02af97e1bdc8c91b2d5133d7483eeeaeb2d3afc1a80d93857e2c6` | 0 |
| core/embed/sec/iwdg/unix/iwdg.c | 811 | `8fac0005b1a451692818f163cadb6405758872b55c396d9bed84aaa4ceaa5edc` | 0 |
| core/embed/sec/mcu_attestation/build.rs | 258 | `d57bf59e901394dbf2ba4d4e936b23d8279a4afa9f304b8c6af502fdeeccf23e` | 0 |
| core/embed/sec/mcu_attestation/inc/sec/mcu_attestation.h | 2357 | `873ee1bf6ae510a03ab9f28583e467d8b064a6bfd22a44eeba1d8c12deebe12f` | 0 |
| core/embed/sec/mcu_attestation/mcu_attestation.c | 2922 | `bdd4c58eb333727d7342865a7f21675cf6f6b7535fbe75cd40fd0fa20471e28d` | 0 |
| core/embed/sec/mldsa44/build.rs | 226 | `2f25187894fdf60d4acee296ef21e916a501ca5b11b5792820d19997d86db53a` | 0 |
| core/embed/sec/mldsa44/inc/sec/mldsa44.h | 1883 | `e1a692d1b32bfa3ee119f64b5816788e1913b1a882ae20e7e7d2fbd54db24464` | 0 |
| core/embed/sec/mldsa44/mldsa44.c | 1679 | `39d4e9751f5377b76009ce76b794b4fd5fa494569ee175873605f477369d108b` | 0 |
| core/embed/sec/monoctr/build.rs | 488 | `b57d07bdf2fb0c53f137c1cdff4d4553600eebfb0cfc81bac43c4d48f87ac44d` | 0 |
| core/embed/sec/monoctr/inc/sec/monoctr.h | 2111 | `78f1912acabf3b7d1997c6a541f75c852b45efe87c9b97b30c1dee332b9640e1` | 0 |
| core/embed/sec/monoctr/stm32f4/monoctr.c | 3434 | `c682eafe38b1e4e7cdc7b9e575de8ae1f6f3df9c579befc408e60147b6d4a7ff` | 0 |
| core/embed/sec/monoctr/stm32u5/monoctr.c | 3557 | `55717c1c6be1ec2a03f3dcbf1eaaa717d182af718bca0263cb3c48549d0ccf82` | 0 |
| core/embed/sec/monoctr/unix/monoctr.c | 3600 | `b7b154d11f4104a3a6d85c289803e83bb7ac71ee49930e342d2cd86022161c66` | 0 |
| core/embed/sec/optiga/build.rs | 920 | `e855d0f17e92e0c6d6a969431b2c7e138da7ee988cbc256fd8c27ccc37abc7d4` | 0 |
| core/embed/sec/optiga/inc/optiga.h | 912 | `0953ff667ee720a039f7e5dd5e2cfbd480dcfa9889e5081fe1f54b709a730c31` | 0 |
| core/embed/sec/optiga/inc/sec/optiga.h | 4208 | `02a723fa3941034aef998efcd920b76cac6a65ef93b120694c783401457702a0` | 0 |
| core/embed/sec/optiga/inc/sec/optiga_commands.h | 13186 | `6e8a7491fefe2d6533b17e7dcbff816a225d890fa9412deced552248b5173557` | 0 |
| core/embed/sec/optiga/inc/sec/optiga_common.h | 1695 | `97ee5ba6720c4bf877b3e2d2a0900e474dfc15b849b2ac49b7f655fb1a200ce0` | 0 |
| core/embed/sec/optiga/inc/sec/optiga_hal.h | 947 | `156c0de82bfea7951124674ec66813ca78f93aabb557e1c769fbd29973ed2060` | 0 |
| core/embed/sec/optiga/inc/sec/optiga_init.h | 2567 | `6ed55906c4a835ed72ad1e50b535e1a8eec1dfd70431a368201a4c720651c985` | 0 |
| core/embed/sec/optiga/inc/sec/optiga_transport.h | 1792 | `d710512d36f10ee51765760963695a1b84740110342e1a8e5df31319a0d22b24` | 0 |
| core/embed/sec/optiga/optiga.c | 43686 | `86953c6e9c6e270342c04d994c58eac57fd5d5ee233c3dce40421611c9b06dd8` | 0 |
| core/embed/sec/optiga/optiga_commands.c | 36849 | `9cfb47224dfdc5400ffccd64e0bdafc94598d870e43a06664163f15879e767d3` | 0 |
| core/embed/sec/optiga/optiga_init.c | 3578 | `1b2d1e9093b3dd759bd73c0d322f79bf293e48af69363ddc80059f84b821d24c` | 0 |
| core/embed/sec/optiga/optiga_transport.c | 26822 | `7f1cb8c2abcff0e93e5facfcb5870cc6491ce9ff4366cae35b18017202a61088` | 0 |
| core/embed/sec/optiga/stm32/optiga_hal.c | 2780 | `cfa0320e20151394bea8e25b509b10d9961a8134b4a78fbb01448e331c2bdcd1` | 0 |
| core/embed/sec/optiga/unix/certs/T2B1.der | 901 | `eeb363d0ae4658f0094309633221a6183bbebd810b2e0d049ff660d615c3cec3` | 0 |
| core/embed/sec/optiga/unix/certs/T2B1.h | 6419 | `9f1e10a773e4df55950999bb83ae7df31bf4dcaeff6bbaef4594bd27ba9ac4e5` | 0 |
| core/embed/sec/optiga/unix/certs/T3B1.der | 908 | `544579e03b3873704697ff3b9898f084fbed1eaaa7f80b845679ac9d1ad155bf` | 0 |
| core/embed/sec/optiga/unix/certs/T3B1.h | 6419 | `445bbe90652a89a5eeb0ff51c43221bd943a7a58d16a8b136159e9717dac61c1` | 0 |
| core/embed/sec/optiga/unix/certs/T3T1.der | 906 | `e8456966682be783d12a02143d7bf75a15d3a2aac410426e54f9f1b5adf8a9b8` | 0 |
| core/embed/sec/optiga/unix/certs/T3T1.h | 6419 | `04d5a15e77c8ff483a818ddfd70454c405c4912b1be9e46499ae0e89c6108863` | 0 |
| core/embed/sec/optiga/unix/certs/T3W1.der | 978 | `125146b2836658d22fb5303858eb2cd1662cbc16da245369f56e8b23a246e310` | 0 |
| core/embed/sec/optiga/unix/certs/T3W1.h | 6899 | `175695be34a0aa47ed7356a42b8e6875ce44595ea7d656e8da83de618ed0f8cc` | 0 |
| core/embed/sec/optiga/unix/optiga.c | 4931 | `8098dc92e54f18853be020b5ce9fca365ca33eafa694784bd8783b998ab768c8` | 0 |
| core/embed/sec/optiga/unix/optiga_commands.c | 857 | `7f6230fbe09ab1b9769d97cd588bc6c01b013a50f0fee4ff65b64bb2701db7c1` | 0 |
| core/embed/sec/optiga/unix/optiga_hal.c | 903 | `22efe05b14652fa9160e49120992e97483e015c19ec232015a877b583648baec` | 0 |
| core/embed/sec/optiga/unix/optiga_mock.c | 1823 | `ce5f984d391de93485ba0705ec47aeafaf45f4019689055fe28331f00afe4001` | 0 |
| core/embed/sec/optiga/unix/optiga_transport.c | 905 | `4c3f619cac65e74627ffe67cbcb228715ba92c5a179b4285b6bd82151d704f69` | 0 |
| core/embed/sec/option_bytes/build.rs | 492 | `c40f2aca2dc758d2505b22774d2dc6b396f6fe2d2fc42e7d3286c3a30dcf5149` | 0 |
| core/embed/sec/option_bytes/inc/sec/option_bytes.h | 1428 | `41d8df05143f7bc2090e7087c21cc85fdc0ae0f344fb432c047b499b37d0578a` | 0 |
| core/embed/sec/option_bytes/stm32f4/option_bytes.c | 5613 | `e5a9cea7638d839172bf64d4b261a03e1ad072eb4056b806438800d85f8f5316` | 0 |
| core/embed/sec/option_bytes/stm32u5/option_bytes.c | 8742 | `6bff0cb62703677c0de82a20c0924a3cb6059b93740abf02b39c8beae0017a18` | 0 |
| core/embed/sec/random_delays/build.rs | 495 | `1ca3687b6542f98797d93ef55c5f4c4c123650daacc260e85822c222a9d3f450` | 0 |
| core/embed/sec/random_delays/inc/random_delays.h | 919 | `49fe70229b9a9d1e424105337cae4c1e1a0824a735ff6003b2a995d9586f1ba2` | 0 |
| core/embed/sec/random_delays/inc/sec/random_delays.h | 2581 | `929bca79bfd664e6b8fb1e86916b5725846f7dbb9e5200de4a554f8a4dc34aef` | 0 |
| core/embed/sec/random_delays/stm32/random_delays.c | 5737 | `e0924b5c8f8ea5cb01f4ff4041a80939021ffc177b58932e6d7cf6ab9d5758c0` | 0 |
| core/embed/sec/random_delays/unix/random_delays.c | 844 | `94820067ebba247ca5752d69b80b46649666f68e8ed7166bca965908ffdf92bf` | 0 |
| core/embed/sec/rng/build.rs | 174 | `6a9f19933b06d841f3aafe11b4550bad639b996214cb9bdb4d7ce3a259d61fdf` | 0 |
| core/embed/sec/rng/inc/sec/rng_strong.h | 2191 | `2df4879d6c972e3bfd41fc86755ffc59b0e2325bcf71dd41f5465e6ad623a3bb` | 0 |
| core/embed/sec/rng/rng_strong.c | 2731 | `780f5365b0ba3d83afe6099307944042bd61b41d1976c97beacd923afb283694` | 0 |
| core/embed/sec/rsod/build.rs | 178 | `46e236b779048c6672182a6aec4daf3b537c5e228c6e31042575f2fae4d871ac` | 0 |
| core/embed/sec/rsod/inc/sec/rsod_special.h | 1711 | `00b8cc295a039f269d301fbb76841a98811c61a9e6bfcc6a5c056fcaad170829` | 0 |
| core/embed/sec/rsod/rsod_special.c | 2139 | `51108360fb408d79eddcc18c366c189cb2d383fcaf5693ee9060900371697b74` | 0 |
| core/embed/sec/secret/build.rs | 527 | `91d6aca75e97e8086102a0a4dcdafeaece7297b71cf9c8267d0ac693a83100d1` | 0 |
| core/embed/sec/secret/inc/sec/secret.h | 6136 | `2f811658255f16e3eadfdd1d79a6a20a39aa3f2fb1c30561c8af1ec410dc4e3f` | 0 |
| core/embed/sec/secret/stm32f4/secret.c | 5273 | `c90a1501e645ded27b95dc63eec5bda26607392403484ce894e4b3fbcc32d20a` | 0 |
| core/embed/sec/secret/stm32u5/secret.c | 19034 | `8e319207add55d057fdcc6ab0723ef6b13aa4568e50e9e40e72ef3014a88815d` | 0 |
| core/embed/sec/secret/unix/certs/T3W1.der | 4067 | `d6ab4e4371b9bb1de0399cc895da9c8750e05df69f3f72646941e128bb6e658d` | 0 |
| core/embed/sec/secret/unix/certs/T3W1.h | 27459 | `1fdf6d5b02bc9df85c9da4c2ec0783016bdb1c773e0bc668d1197b7118d98e88` | 0 |
| core/embed/sec/secret/unix/secret.c | 5732 | `6e72912f9e0e34e48d371f6e3c80b19a4c112bc42a610f67beaa7daa46feb928` | 0 |
| core/embed/sec/secret_keys/build.rs | 718 | `bef75c8d4a5aa6db90509d2a0ad197a21e03887062442ae99ba95f7c591c9460` | 0 |
| core/embed/sec/secret_keys/inc/sec/secret_keys.h | 2847 | `ae6d50f502a5502d465f1812b85d437563a9f5bf144daa7bf3bb839a90a9164f` | 0 |
| core/embed/sec/secret_keys/secret_keys_common.c | 4456 | `638c5e7674446634a43bf13eeddae4edd8b512e8010d1f22b5c55a970289856b` | 0 |
| core/embed/sec/secret_keys/secret_keys_common.h | 1847 | `6aac098add0fb4b7f231ee967e43201c233b1c4c0d68bac1dcdf009f7d9aeade` | 0 |
| core/embed/sec/secret_keys/stm32f4/secret_keys.c | 2183 | `cddf2e742228c0c4bc3c4aff7aca902d03caf0525c430d10356443c77359dc93` | 0 |
| core/embed/sec/secret_keys/stm32u5/secret_keys.c | 6713 | `7fffa6707930d72b6311d31ed09ffac7324ec62c0ba536b903a56cfc27b513fd` | 0 |
| core/embed/sec/secret_keys/unix/secret_keys.c | 3226 | `32745efdcabd75bb7aab533dd7144928e0f88a9ce5a755ad9fcea9a0dad73e67` | 0 |
| core/embed/sec/secure_aes/build.rs | 470 | `7198c9198353b848a3b62121e1ed97f2811e895bf7fc96a59a50c42781f80510` | 0 |
| core/embed/sec/secure_aes/inc/sec/secure_aes.h | 2097 | `2e88affb899ffcf6d2a5092fd2840d43803dd5d2a40ae78904bbea5f0e140e5b` | 0 |
| core/embed/sec/secure_aes/inc/secure_aes.h | 916 | `80ee83a0852f879f3e3034095793047010654495e4df71215c076083873f481b` | 0 |
| core/embed/sec/secure_aes/stm32u5/secure_aes.c | 7127 | `c024544b576d2f2be7834c7368295efa052b0e9e4c945b0c1c6c2dd45eff58e4` | 0 |
| core/embed/sec/secure_aes/stm32u5/secure_aes_unpriv.c | 5149 | `7c17aa64a955f5688e6a05babeca8aabc5de55e005091dc5a7f8fe6b7ccfcbbd` | 0 |
| core/embed/sec/secure_aes/stm32u5/secure_aes_unpriv.h | 912 | `3a97bdb9514522c3d4e15d3b20b6fb255d78102eb91a0ffad60951019ecac5e4` | 0 |
| core/embed/sec/secure_aes/unix/secure_aes.c | 832 | `43083eeaaf1f2861a5732dadf723fcf5a9724df7acb99c58f9388ba88144c244` | 0 |
| core/embed/sec/src/lib.rs | 658 | `9cdc881760e9754fa5b867e4f509dc14c4349ccd37913cc95a751fe360d80e69` | 0 |
| core/embed/sec/storage/build.rs | 1110 | `a20346f3dabdb08a088a13d3c9efbe7fda2d35c4e4f985d29d7ef7e576761b4f` | 0 |
| core/embed/sec/storage/inc/norcow_config.h | 1409 | `3e8815693e8c644f49596fed42ad06e09f459581caa50a83a0317a292a3200e1` | 0 |
| core/embed/sec/storage/inc/sec/storage.h | 1156 | `47224f5152ab718fdf672cfec365e7fda050371097bc29f1358c70c34a3f288d` | 0 |
| core/embed/sec/storage/stm32f4/storage_salt.c | 1967 | `af2067592fa9f342f4af6db31f9bd3b0e8fadd70b2578dd143c67812d1cae7bd` | 0 |
| core/embed/sec/storage/stm32u5/storage_salt.c | 2752 | `2df8cbe775631bce91c8017d7c6195860cd48a5a7fe81859281fe3dc2990ab58` | 0 |
| core/embed/sec/storage/storage_salt.h | 1451 | `f822bf3e2629653666e3c18246ced0cb6a5dc76a4f5d1189d74d2aebc4c649be` | 0 |
| core/embed/sec/storage/storage_setup.c | 1055 | `3ad894cbce0792c400936c479ac1c763db95d5f9f625ecedd0f981678c2ff498` | 0 |
| core/embed/sec/storage/unix/storage_salt.c | 1024 | `8818039a784d3467850674c2c0c15cc5aa7e8e213275b33976be1c1040182437` | 0 |
| core/embed/sec/suspend/build.rs | 418 | `bdadc93aeecf8459a46a308ebb9acaf18ae1dd5d824a67cb7b8f715aebf74b41` | 0 |
| core/embed/sec/suspend/inc/sec/suspend_io.h | 1456 | `dd9496271ba55340fc2df7ac6d4f6384a678d03f97c7e399a935fde0d4615041` | 0 |
| core/embed/sec/suspend/stm32u5/suspend_io.c | 1995 | `ea45b8f6a447575c8d7dad2f4b62a68a75937d57ac3f90f4af54113c9ec8fd5b` | 0 |
| core/embed/sec/tamper/build.rs | 430 | `f79aca7d78ba98d022b39ff7ddc8e3c21203f230f300736b3ed8d25d26a5322f` | 0 |
| core/embed/sec/tamper/inc/sec/tamper.h | 1263 | `2b88d5059803308db1c6f9ecbf9b53173746e37fbb8932bb176c4d5350f5fa96` | 0 |
| core/embed/sec/tamper/stm32u5/tamper.c | 8810 | `cebb07c63651dec077756fdad38d6d5c65e5ee99b77cb33deb0871949f780b03` | 0 |
| core/embed/sec/tamper/unix/tamper.c | 944 | `53b8b1a8ac82c33e2e0b4e5e3a04ccaa1e79021241cebad19dbfae8ec29e84da` | 0 |
| core/embed/sec/telemetry/build.rs | 448 | `d644e1f216527dc677e66f4d062a7c40a6adbd02b6d2d4b10f4633cc7f9564fa` | 0 |
| core/embed/sec/telemetry/inc/sec/telemetry.h | 2966 | `f4b8e43c54b4e1d43cc0e5e9f978c4362a0a6e5bdbe61b5a8e71265cbe1e0d85` | 0 |
| core/embed/sec/telemetry/stm32u5/telemetry.c | 3626 | `8c69f73e024b7a81f68041fc0c2c20e0f3edeb75ad6dc28abe6ab9a19b486ed7` | 0 |
| core/embed/sec/telemetry/unix/telemetry.c | 1200 | `906ec8c58badeae9418d99fae8ccf19d08fa69032e61ee4f10a91c4adead0ab9` | 0 |
| core/embed/sec/time_estimate/build.rs | 415 | `942afba329fc1eb90d1ac8a6ae766bf7f19afe1f485cec5956d9dd1d73d2b607` | 0 |
| core/embed/sec/time_estimate/inc/sec/time_estimate.h | 1011 | `6c714445e35a1468de49afc586eb2db0e7b124ca2331b31e28ff12cf04ec482b` | 0 |
| core/embed/sec/time_estimate/inc/time_estimate.h | 919 | `e767266afba79c54c19316fded82c0882e79b381aff2e4b859d6b2b88b3210ad` | 0 |
| core/embed/sec/time_estimate/stm32/time_estimate.c | 1414 | `655a8f5bd898141ea5bae7f88f3e95e3e3f70a35b6dd72e28646af330b65bc8c` | 0 |
| core/embed/sec/time_estimate/unix/time_estimate.c | 947 | `e3bd0549984801b1b55e60420623bb3e0a367e7d6ae8055a2b4154d7200b2310` | 0 |
| core/embed/sec/tropic/build.rs | 2550 | `d864604c158167d548473a34ef1cb44ecaa79a4f2eb330689a3f9f13807535be` | 0 |
| core/embed/sec/tropic/config/tropic_configs.c | 6144 | `fddf577fd4eae6b56506ede53fe63aa185d5587feb28f7e184135a97bb0fd16d` | 0 |
| core/embed/sec/tropic/inc/sec/tropic.h | 7641 | `3051664f352f8896f5d8d7d4b97f81bd88b97aaa2447a384c6e1af65242ebd2f` | 0 |
| core/embed/sec/tropic/inc/sec/tropic_configs.h | 1506 | `526aaffa7bdc782ac68df28980e15076833e5e1d71ec3a84535b16386f8ab5d7` | 0 |
| core/embed/sec/tropic/stm32/tropic01.c | 6902 | `0748452c297092a6e1c4878a2f115f83d57a2610eb6698803e1afe1f149bdc1c` | 0 |
| core/embed/sec/tropic/tropic.c | 63454 | `06c12cd103221953f5062cac17dcdac5ce30c90faf1c5765074b0059bff4acb2` | 0 |
| core/embed/sec/tropic/unix/tropic01.c | 1134 | `33e20cb495d39bd2132b9f5908958ff77640e67d0ab35c912cfea483f051b25c` | 0 |
| core/embed/sec/tropic/unix/tropic_mock.c | 1987 | `389b7503fef16d6e7e787747e5b548d6dbdd580ed8ab1578a4ab8934f62c06e2` | 0 |
| core/embed/sec/trustzone/build.rs | 496 | `3b44789edd289f74a9a2fdc070c47fb9c743bc6fcae42bc1c4e9b78e3268c745` | 0 |
| core/embed/sec/trustzone/inc/sec/tz_init.h | 853 | `963d7a8c19c0bd11a0b26aba72ba66bc73c43882149d1691d3403adf2f09fc83` | 0 |
| core/embed/sec/trustzone/inc/sec/tz_periph.h | 1596 | `978f7c95a712004fa8efe709e5d6f389ee9a99c498fed9184fa3f230a269dec5` | 0 |
| core/embed/sec/trustzone/stm32u5/tz_init.c | 15066 | `805220eab859d0b0a0c1a0c073d2222b18eb3742d7414799d00be3af55f22207` | 0 |
| core/embed/sec/trustzone/stm32u5/tz_periph.c | 1963 | `36c22839bdf5dade940d7e6d2b1c16e0b014e9b2d18aa1e03454a630b362a34f` | 0 |
| core/embed/sec/trustzone/unix/tz_init.c | 838 | `416a7977baf16d67c24fb260a284bdb99e9d46c6ba39b4ef033069344e15c31f` | 0 |
| core/embed/sec/unit_properties/build.rs | 425 | `24e070527e39579650b2123bfd2ee3b4ea659554db289489756249c162558ab4` | 0 |
| core/embed/sec/unit_properties/inc/sec/unit_properties.h | 4035 | `79a6188c32d7195f2f8476a684d9994e48341d838c8ddfd497b0c03f1c3a92b7` | 0 |
| core/embed/sec/unit_properties/stm32/unit_properties.c | 7224 | `eb93cf0996c2f07b66383b995a39c341d1ac95cffec4fd97bad17697ccda4dc0` | 0 |
| core/embed/sec/unit_properties/unix/unit_properties.c | 2596 | `7116803c69f0cccc1184262691d08f1ba4c4c488dc991b9627f5a3df472a79bc` | 0 |
| crypto/address.c | 3437 | `a114dd3fed92c28efc9ac86bb114359c64326075dd533e7cb7108873f6119462` | 0 |
| crypto/address.h | 1644 | `612ef87eff552dc85aa5e85dee2ecb43ff164b1867baacd09919eed665e8e914` | 0 |
| crypto/aes/aes.h | 8027 | `268e51fc6678770e88bb4a42e3047818d4d35239a49ba7c0c2a3d25edcda6677` | 0 |
| crypto/aes/aes_modes.c | 31255 | `08a8615b6b66c8965c026d7c5aaf9b56e3612f53d7f263fa3be956826cd31fcd` | 0 |
| crypto/aes/aesccm.c | 10364 | `beed09cbd374d23d19855991de1159e0cc79711ba8d3ac7a12599662aed9d715` | 0 |
| crypto/aes/aesccm.h | 1898 | `32eb3a758714d00b4cc3ba96444664d8e8396db38853484d9eb79d7c088961ba` | 0 |
| crypto/aes/aescrypt.c | 10385 | `bffc247b4231fdea460d6b587264b3bf60a1f2c8616797c605c2d4570894c7f6` | 0 |
| crypto/aes/aesgcm.c | 19524 | `99e1834ba9c2cb24ac680d0bf8517a0767d04694a4cfc46bc38482b5b2e187cd` | 0 |
| crypto/aes/aesgcm.h | 10723 | `dc03c25b255a671fba25ba14c28cc350207a15cb9bf904c277960e24aadf12c2` | 0 |
| crypto/aes/aeskey.c | 16156 | `06de2b55fbb4636f41882ef5e7a4898e58291783a41560cb24f7e7c8e6696b75` | 0 |
| crypto/aes/aesopt.h | 27763 | `eee8cfb072ea283e77cbd5492d2cfeb3c1bf288ccac29cd19af8e0178938c5d7` | 0 |
| crypto/aes/aestab.c | 15862 | `b56f0a709400d6a346ccef8aadc95a8c5f4da435dbdab6b9fe8083b2874688c3` | 0 |
| crypto/aes/aestab.h | 5162 | `54a0b84dfb358c0b1577f777c85cf9d90abea3c6f4ec5d587b7d230f123154d5` | 0 |
| crypto/aes/brg_endian.h | 1072 | `882c1a6b44d1a2825dfc45e1ff1521724a9c42d0630a50c5e03792c9b4611334` | 0 |
| crypto/aes/gf128mul.c | 14140 | `c8a16c99f928fcbda1e924d3f9d01944cb3cb31f6599fe4140103c3dd75f573d` | 0 |
| crypto/aes/gf128mul.h | 6831 | `bde5b69030831d35ad28849276db9e717ad91e613b7aec6cb9a72dd7f4a0fd7d` | 0 |
| crypto/aes/gf_mul_lo.h | 27314 | `697a0f03307c5c7e5164a4e36e9697066337eddf5464cbe4599f7d3029fe6aa8` | 0 |
| crypto/aes/mode_hdr.h | 11901 | `0d8e0a86a9b64f0f7b8c4a7540bb2037ad7fcae384eae2e113a7fa17aac09f72` | 0 |
| crypto/base32.c | 6224 | `9865ee24997300d0fa0c0c513c112dcea14725a2732b933b50375ccbd5b7e4b4` | 0 |
| crypto/base32.h | 1820 | `af06a1cef3f0e92ed35124527607a24c423513033223251b24c1f5a8ed62d7fe` | 0 |
| crypto/base58.c | 6905 | `9675f568be65fec72ddd6fdb849d8c30ad318cd3f4e1d44d522b27b8238497b7` | 0 |
| crypto/base58.h | 1915 | `f9e2ac2294b68ae67920e2050c776cfb34617dbce97a571307fbda879af37613` | 0 |
| crypto/bignum.c | 64369 | `e6051759e8a86f0d90f26ff2220b8c5c96ce51a1a8997015525c5848348d7fec` | 0 |
| crypto/bignum.h | 7306 | `1b92bc5469e786f1700510ae091592ca58fd8fa52e02c5622907950d76113eb3` | 0 |
| crypto/bip32.c | 25521 | `2429e49ef1cc89c504ae0815c890c5bac059606b775811c38e8bc1369be903f9` | 0 |
| crypto/bip32.h | 5628 | `d939c43c23ffa672e524ca8d6a57609d8593c665ad160aa5acd43158452ccaa6` | 0 |
| crypto/bip39.c | 9764 | `6baf82d7a522d2334c5d6777a9aa2452eeea1925891a14556dd15998ce546225` | 0 |
| crypto/bip39.h | 2513 | `3774828450685eae9f3c47af5c95d0a0062be6c35c73b61d194dcc9465d25c15` | 0 |
| crypto/bip39_english.c | 26292 | `7d594a31f97c7732ca5b88c1382ff83961607288c544cf3e339bbc5804eac021` | 0 |
| crypto/blake256.c | 6582 | `69d2f6baf60f9743f14ba9e76b80a7153b910b68a89a7e5ae653164fe2ad438d` | 0 |
| crypto/blake256.h | 2185 | `db53c134b10bdb781d99e69faa38ba204be21329e53c88a372aa1fff16848480` | 0 |
| crypto/blake2_common.h | 945 | `b35578aef4002e2d60ae670aafeacbbca08e68c9bcad31b53030d091bd0008c6` | 0 |
| crypto/blake2b.c | 9875 | `13a96853d7db5a69c15132204c7e7bb9d37633477feb244c3c72c64c2c2a913f` | 0 |
| crypto/blake2b.h | 1244 | `5ed610574dea1a47e0e352fc58b5b2a9ea4c051cc88833cd65732dd91105fdfe` | 0 |
| crypto/blake2s.c | 9549 | `b07dad1a25778fedef287824b1ed4b55a073fc96a28238231d5629ef51d2f5a6` | 0 |
| crypto/blake2s.h | 1244 | `1b63131f4ce1457c98e7733ab3e951765848ebb41bd59dae168df3b648451d4e` | 0 |
| crypto/buffer.c | 3695 | `9293e14aa8e257e3e3528fe5ccf44bf6d79fc3518edb6c7d8bf8b57f3541d7f3` | 0 |
| crypto/buffer.h | 2498 | `0cea3d5b7659011afc02c10424a923b5171d370fccd2dc99ce1fa28a54c15d6a` | 0 |
| crypto/byte_order.h | 1761 | `496a5a80346a0fb48ef3fbf53c0da2b69399e1de224d67962342657a9dfd77d1` | 0 |
| crypto/cardano.c | 10342 | `c28881b92bd59b7a9f8f3368675c2d5fbf53cb7fedcf523aad172c7d656eb61d` | 0 |
| crypto/cardano.h | 2189 | `d6e6bce678f522f0fe3d229cc1a4baa91e1bc6a3e9a05e4b93f81c9dcadfbe3a` | 0 |
| crypto/cash_addr.c | 6397 | `637e51700eb115326f3b039211731607d4bc4a2dc63ce953d46ca6eb315feec7` | 0 |
| crypto/cash_addr.h | 3533 | `92908d32e408da03300fa25867f65e02b5a770453295e6cda8cc983b61a84988` | 0 |
| crypto/chacha20poly1305/chacha20poly1305.c | 2505 | `a827ab1f975618f343ae2468cb8ff4b3aee307b84a69f66205fcca00a102489b` | 0 |
| crypto/chacha20poly1305/chacha20poly1305.h | 727 | `4e75c8d3a0044625d80b98b9500799da84fd387c28b72dcb0d90a3aec5465ee8` | 0 |
| crypto/chacha20poly1305/chacha_merged.c | 6500 | `410cfbaf6c0e6b986cc951f08d6991ef0a45b884dfc0dc6b21d82b8b8002c695` | 0 |
| crypto/chacha20poly1305/ecrypt-config.h | 5804 | `7ed8cab12d40e1f86fe2511d0c3c0332594bbb56eea0e9592e7d9c825c1876a9` | 0 |
| crypto/chacha20poly1305/ecrypt-machine.h | 1182 | `70dd1a45d677c3cfa62955fd1d3e125a31002f44f550e85a25364ae6cac159b9` | 0 |
| crypto/chacha20poly1305/ecrypt-portable.h | 6780 | `8a1f73bb364d19382983d2bc1a8ca568c4a5f7cc9dafa696ace5ebe954dbbcce` | 0 |
| crypto/chacha20poly1305/ecrypt-sync.h | 7851 | `2684a9c88e80749f88e94caea40b8ba57ddea17c5cfc06dc6c479d48d2b15c0f` | 0 |
| crypto/chacha20poly1305/ecrypt-types.h | 1175 | `7d0b98aad7734e79ad1a897d7c568d60547ece3d3f03e639fc274e8c9bcc1639` | 0 |
| crypto/chacha20poly1305/poly1305-donna-32.h | 6515 | `85bc63c1a468fe31a896c242be1cb7afe0cc9a262e5042911abc2cc5dbd1bcb6` | 0 |
| crypto/chacha20poly1305/poly1305-donna.c | 5075 | `f47eda9544fbbdace81f24914f988f2133f1614bafaabba0e7b2718309d81a9b` | 0 |
| crypto/chacha20poly1305/poly1305-donna.h | 658 | `db2194945f4aeb914e13efee982d365cd32cc16009febb6f68b51b6aaf17514e` | 0 |
| crypto/chacha20poly1305/rfc7539.c | 1770 | `57ddcc6e371ff5b9ce1221796c4a6bc7110259f3493a27c99b8c677e3a8c1f26` | 0 |
| crypto/chacha20poly1305/rfc7539.h | 351 | `699340a53d5d2c02ea95450966fddd210a0c06551d48c96895c9005a45c6e67e` | 0 |
| crypto/chacha_drbg.c | 4950 | `3a79708e2a3061b6908755577f7cd1a837bb2ff0edc56a6d9c8a9490f648c965` | 0 |
| crypto/chacha_drbg.h | 2746 | `a9315eb6531dda82f61958387002f42b02c17724474d92c20e93fb21f528a9e3` | 0 |
| crypto/check_mem.h | 1099 | `ec7d5a86c9745d80faa310ffbd07710267493b08e7f71bd3fb8e5ed9038fc6a0` | 0 |
| crypto/consteq.c | 1697 | `5bfe0f3b7a79c7d4e8cdd4d052273ae8d4f2e5180a07db0bcad07076220a07c7` | 0 |
| crypto/consteq.h | 1521 | `09b70ff94f5daf83a0bfa6bb76a1c110d19456f07b61c0982a16ce2e7b7e4fec` | 0 |
| crypto/curves.c | 1740 | `6117082c17ca7f8e0fee9b39218d4911bc111dcc0e0aa6c733c9c3c8b882e146` | 0 |
| crypto/curves.h | 1650 | `883ce4ab5e2417a94eaf1cd8817a10eeed6e55ea96a3fae65666586ba5c0ee9a` | 0 |
| crypto/der.c | 4447 | `7cd3558a5b529e73b53c5f35d19d0dc0d91680e41030c1f47cad0fbc0dfa78f2` | 0 |
| crypto/der.h | 2342 | `e054ea4c45ff29f9424c6642cbf22a7d94e9d7bcee4568749ebe45c7bca38363` | 0 |
| crypto/ecdsa.c | 44260 | `76140e6cea8e4b04b5e388f295bbd71f43471e8fdec252bb014a4ab9ee067478` | 0 |
| crypto/ecdsa.h | 7939 | `206848978bfff6c343e44eee2ce3b8ecda31a920b9f5618ef3eaaeb0d77175a5` | 0 |
| crypto/ecdsa_internal.h | 2421 | `7e6d403a2ac5ded03706456d464aa7de50db928f782931a67e3e65ad1220595e` | 0 |
| crypto/ed25519-donna/curve25519-donna-32bit.c | 26969 | `efaa64f1471b7e16a1a2b97f4f328501a80a177743d5700b18799fa338d30b21` | 0 |
| crypto/ed25519-donna/curve25519-donna-32bit.h | 2641 | `a4d39914f88b3daef07b81e26163c1b5c7161a85d6d339edf6dd830fa2c69d22` | 0 |
| crypto/ed25519-donna/curve25519-donna-helpers.c | 2414 | `aeed56aeef2e3d2136d0f4bcb2a7df8c82d608d21ad63f04d8ed6e0869a961cd` | 0 |
| crypto/ed25519-donna/curve25519-donna-helpers.h | 479 | `5f8a33382d9d4a53b7d88326a4104bd6e35e619676bcf7985146f2c25ffba4b4` | 0 |
| crypto/ed25519-donna/curve25519-donna-scalarmult-base.c | 2201 | `370a0c8b649ad61807a4220c9b961824dcb3b703f0af21135d04bb4d55930c7f` | 0 |
| crypto/ed25519-donna/curve25519-donna-scalarmult-base.h | 372 | `6b09a09393ce4a4d6cb0fde19db63785b5097d6521c6375fc664c3be8a5c6984` | 0 |
| crypto/ed25519-donna/ed25519-donna-32bit-tables.c | 11995 | `8345a35068d2fe7b39570a60644527a0265ce9cae75eaf70b98c2edb50595b26` | 0 |
| crypto/ed25519-donna/ed25519-donna-32bit-tables.h | 305 | `b8770e7c29cf8dabdda470537e56148a873519909b2de08f31a2dc8d9fe44f45` | 0 |
| crypto/ed25519-donna/ed25519-donna-basepoint-table.c | 124124 | `e35f8593c69d90a35a9694c6216eadc6ec79f660c984c0aa086d4b988a1a982d` | 0 |
| crypto/ed25519-donna/ed25519-donna-basepoint-table.h | 195 | `9edbe5f6537d72253acabe4a5c330827bd6802d17a57982837967b6f2ae4bc83` | 0 |
| crypto/ed25519-donna/ed25519-donna-impl-base.c | 22564 | `1724565c868af1d5af51d104b8ddd2ee6a6c85a6372107be2dd84d7c2c181bbe` | 0 |
| crypto/ed25519-donna/ed25519-donna-impl-base.h | 2793 | `1ea034e8b10f2f0474bbb64a0b71408ee0112126742e77b2042ab6d092f76970` | 0 |
| crypto/ed25519-donna/ed25519-donna-portable.h | 580 | `181fa91d854115b301633b6ebfb36ea28eef6528cefadc173592352f41ad516c` | 0 |
| crypto/ed25519-donna/ed25519-donna.h | 1218 | `51a561027071fcf644817152f43ee3ebbb7cf19bfdf102678058e3ab3638e84b` | 0 |
| crypto/ed25519-donna/ed25519-hash-custom-keccak.h | 785 | `04c8d8d1e9ed4c4cd63e88e24ba19f6eb56b04737c757730df7f69e032550ad3` | 0 |
| crypto/ed25519-donna/ed25519-hash-custom-sha3.h | 777 | `a0b36ebdb684c046933ff44a6293134274f75aee9a6cdd328af6caed55e8131e` | 0 |
| crypto/ed25519-donna/ed25519-hash-custom.h | 783 | `1bdce380cbe192dd220ee0786558d2c9d9a7814ebf2f58c46f87a0d0cabf4b42` | 0 |
| crypto/ed25519-donna/ed25519-keccak.c | 143 | `e80f13fd615ff1c457f077e08023f40845308d28a3016b485b8aad173499fc5b` | 0 |
| crypto/ed25519-donna/ed25519-keccak.h | 618 | `b75b56fd205bb694cb18c32e1054f68160a35f73a03fb9fc53db82b237713ad1` | 0 |
| crypto/ed25519-donna/ed25519-sha3.c | 137 | `036fc208ee7d4d2c75a700506b1c212bdd22fb075572f303544f7e8fbaab3e00` | 0 |
| crypto/ed25519-donna/ed25519-sha3.h | 604 | `6e163e5a187b69d2a53b12a5a22ec3502fcdb868c9d6d46f40f08f348dbf81ae` | 0 |
| crypto/ed25519-donna/ed25519.c | 7802 | `ef450fd2ea3296b3d9848e2b4a27d91807011103c95dca493339d6fc0319c55e` | 0 |
| crypto/ed25519-donna/ed25519.h | 1794 | `9d9ceea846c11ecd32ca4bc6e19b5169d7ecbc7b4dbabf62b335228df66b721f` | 0 |
| crypto/ed25519-donna/modm-donna-32bit.c | 23068 | `c4529c31b9f17c919b8d9c2fcddb05151c97de36c7c2dcf60dbb84c053e4a2d0` | 0 |
| crypto/ed25519-donna/modm-donna-32bit.h | 2703 | `6763fa27aadb7d26d83b825a0bd29a5ccc1662c6b42bd49ae794750b3bb4cd87` | 0 |
| crypto/elligator2.c | 5179 | `13e55ea9bf8db14d9bc6f0fba089696e5a77b0578e615d74624bef3222a58a32` | 0 |
| crypto/elligator2.h | 1344 | `ace382673072ce01ebdaf2fd262eb49bdc0747b14a8ac33c046cdfc1a40d0093` | 0 |
| crypto/fault_handler.h | 1228 | `a82155e446d326f0155a7ef6696b6e425e18cc4a59c50014e16e69ae36e2352d` | 0 |
| crypto/fault_handler_noop.c | 1352 | `314e9ecdde817e33f29e4139592e4803393fedc507fea043e324c00bffb35f19` | 0 |
| crypto/groestl.c | 29219 | `74c5b437ebe61325c78e508cfe23e9f7512188495ad8ba25f944bb20c8287b8f` | 0 |
| crypto/groestl.h | 3413 | `eb7ab0d6d707661f61411a3643fd5623fbe81f1fbc07304758c06c494417405b` | 0 |
| crypto/groestl_internal.h | 15138 | `360dd64ee6a7bb1411953ec37d8f9f5e3466ea3242571555f47e5c591225e1ce` | 0 |
| crypto/gui/main.cpp | 171 | `bf673474a73ac48682dedf65f57fdbee70bd5b6abb743e5566f58434a3ebe026` | 0 |
| crypto/gui/mainwindow.cpp | 2806 | `7f47cb8522f72158cfcf1bdf868fa9131e8ea648b9f8aa850dd23e63f94761d3` | 0 |
| crypto/gui/mainwindow.h | 412 | `aa4de2a09718dec1f4930220849602f244e9d3cd0f1c579294c8ba2918f5111d` | 0 |
| crypto/hash_to_curve.c | 11660 | `cc39ea65756d1f424f8f9643396b9515d34216e0eb3b41e9b1ffad7b31465c23` | 0 |
| crypto/hash_to_curve.h | 1584 | `6fce4d043d7808ad42616297d1f06100cc69387cf4402d27a047878ebb688fbb` | 0 |
| crypto/hasher.c | 4963 | `c6eab350c653e8769a33ba0cf0655b4cb1655021a69dccbac7f04065d51e434b` | 0 |
| crypto/hasher.h | 3410 | `4a423c86d326eda9bc1a55848e9eb7b5f3649edb2dc865261cb969769eacf55f` | 0 |
| crypto/hmac.c | 6389 | `ef44ae6fb924e2aa975e58789603e59399f9383887d3eda55e6920d23c627e24` | 0 |
| crypto/hmac.h | 2610 | `268e806610171b276d5e9bfb2fab84e825782b755eb62500c77ee812e50d4026` | 0 |
| crypto/hmac_drbg.c | 4708 | `9b82f03ecaf95cc1255a7e75e4ec4ecaba537bd7681f4a22a1fc6f00879ed201` | 0 |
| crypto/hmac_drbg.h | 1843 | `56cc90eded1de170f3d28b7c49ebe19072f824202d3c2e2f48a8dacf102690d2` | 0 |
| crypto/memzero.c | 1886 | `2f014e8d03420b42fb7b9df39f9150a33ac96d1c48a065f5a908a967561bca02` | 0 |
| crypto/memzero.h | 123 | `ffec031a236dde8df1c0b95cd0c3bd28ca046f6dc62faff36be8401ba82b214a` | 0 |
| crypto/monero/base58.c | 8545 | `7d5c45b0534c98f51918a7ca26bde2c7be2c8554e69019225fe278b024324bba` | 0 |
| crypto/monero/base58.h | 2297 | `eeb43561fa034917ab30921ab0d1c43ea49f4426ff2f719361b54fb28e20791c` | 0 |
| crypto/monero/int-util.h | 3223 | `43c09ffe3112b307a0725b67c88b983fb7ee5aef963d943158bafc48853e20bb` | 0 |
| crypto/monero/monero.h | 329 | `101b1cd67e8da011d098dfc18ee5027773ea38db17c09600c81ec4a402ffb8cc` | 0 |
| crypto/monero/serialize.c | 1073 | `5c10a6e62ce0527b7974406add5f97d2c20c883afb9aabf3b3116b9dabdfbda8` | 0 |
| crypto/monero/serialize.h | 361 | `f2a4135173f708918ed8bf802d8fbb2e10c6b3548cfe18d11d705925027350f5` | 0 |
| crypto/monero/xmr.c | 4383 | `28287d5ed78240a0ebaec6f3ecc941361fa2a1ddb144925ca7fa3422d95b2370` | 0 |
| crypto/monero/xmr.h | 2270 | `7de7ec3c2757158ef9734c0ddf706c44b99dd410ee6574ae42ecd0df3228ed71` | 0 |
| crypto/nem.c | 17425 | `c8858bed9e52cdac8606b46455d3af935a248941877b0360dc725e2044f74cc4` | 0 |
| crypto/nem.h | 6873 | `cdb89fd8d040261a129f20221e3c79814619857cf307266cbd6ed16d99e08bae` | 0 |
| crypto/nist256p1.c | 2625 | `76e4814899f47b5dea3380ff25da257b9b980d957d1fbbf1046e803a7be113f1` | 0 |
| crypto/nist256p1.h | 1360 | `1a8be02d270c3267eb5dc07465d305105c50c06498b19e7cd7a90b38e4776f67` | 0 |
| crypto/noise_kk1.c | 16163 | `2ddf35ff89fa3390d2c2bc86dd137a4426ed6cf889a88c104ed8a779c1120b9f` | 0 |
| crypto/noise_kk1.h | 5029 | `ccd8421270479065cddf8b425f6cee2f96fc455d1fead60ac3c96e47096f063e` | 0 |
| crypto/noise_xxpsk3.c | 30669 | `5550a2dcad0d68deb78bc1266fe4aaa6a4fe25e9c267593fa8840d5ece19c6ee` | 0 |
| crypto/noise_xxpsk3.h | 16382 | `928c7f768d721e9fc9b28793ced0d0218d86e7674e519c25bb0e3908519f6998` | 0 |
| crypto/options.h | 3023 | `762e3f5cf352740183330743d52e8f7aa977797038f97a3c0d8b88ff98074b1a` | 0 |
| crypto/pbkdf2.c | 6796 | `8482559322823c26ba3676eb281f229d4b0fc9d0cf22f9271629a1b8eef89736` | 0 |
| crypto/pbkdf2.h | 3084 | `8dfb7eea8ee9e0f99ff875a16d7fec538518227fbaa71fb0b9efc9a18b4e0483` | 0 |
| crypto/rand.c | 1615 | `a28436181f55ccccec8ea89f3598bba9342e0e8dad9284bac586dde0cf01a374` | 0 |
| crypto/rand.h | 1574 | `161ecc075038007a61fa7805b2d532bf36dabe521c3de480899eb4b8daa37c66` | 0 |
| crypto/rand_insecure.c | 2485 | `cac714a5c402542e3b85041d6cfa27f7f15459429f20264b21c0f06fa39a4f8e` | 0 |
| crypto/rc4.c | 1844 | `27d2f661c173af397dd954d14222291c0ff3016905dd618493c0868f1bf06ff8` | 0 |
| crypto/rc4.h | 1397 | `183634a8819215c6f1c0828ae37d91cb4672b0689c3bd6436a6b8b4168a099e6` | 0 |
| crypto/rfc6979.c | 2377 | `5e3f9afd203cdbfa411eff32aef0a3240f49664d3898e3c3027593ae001f501c` | 0 |
| crypto/rfc6979.h | 1680 | `876cd568de73effbfdf8b33b441d9fa4ea38456a4dd42b6312e44aca56a70c15` | 0 |
| crypto/ripemd160.c | 12630 | `819dbc7aa10c919feb7ede7aca303abd561379e5f816f680aab87a06f7181b7d` | 0 |
| crypto/ripemd160.h | 615 | `1c9cafb5cb0444ae815c138801252c6f0ffe3306e85180d952ff21be943b0305` | 0 |
| crypto/script.c | 2387 | `34c7128fcfe42f9fb88656893b61944898eadd7cc04981ce590a0bc328a8e0db` | 0 |
| crypto/script.h | 1346 | `797cd6d788b224ad800d1d7e1b5409643722aa86dc98f5cba3900e7e486c541f` | 0 |
| crypto/secp256k1.c | 3257 | `0a3762230f652a872f84a42b790b7c774be8a1a48564965d752f111ae5d1ce69` | 0 |
| crypto/secp256k1.h | 1501 | `ea553cc2e389005fd1b3041d3efbc169e57a03e1150f462f3f36e1858e612612` | 0 |
| crypto/segwit_addr.c | 7556 | `6f55007478e9988cc4fed000852f689bbf6869da08c8a0ff6ed59a91bbff4e94` | 0 |
| crypto/segwit_addr.h | 4295 | `5274a0701e4cac8d811c83f5c66873754af41fdbb89d414044d424acd55f3dad` | 0 |
| crypto/setup.py | 828 | `7d35389b6dd2553ff3f32e2c567d4c79fb86f59d058377a96a8854a054c91d59` | 0 |
| crypto/sha2.c | 39700 | `4e0a22b05988882a1f857084fc6c5a0731a115f5637e9946f65ccd23f361e24a` | 0 |
| crypto/sha2.h | 5035 | `acc5ba73f3ca604ebbaa34651d254eee7eaab808198ce60c42c015e723d9a656` | 0 |
| crypto/sha3.c | 11650 | `246f3f3f49b58803e654e72cc39d26451d7214fd47a6d594402304cc84aad3ba` | 0 |
| crypto/sha3.h | 3068 | `0e8f1617e73d948e60ce0c93598a1edea7c61f74b742d6caf408e2db0d9b9101` | 0 |
| crypto/shamir.c | 9937 | `f58a4b3a6f0c46f99a5ce3779b92ebd1064e1c46ca09a7be94cc3f14d3dad88d` | 0 |
| crypto/shamir.h | 3246 | `8d8a1286ab5cd315e0210862c2a61c354854c81ec412908b265d3a4e8f0a190c` | 0 |
| crypto/slip39.c | 4168 | `b486cf15acffa5f75d0c2c360bc476250c5860f6712b2d562cc7f88ec67b97b0` | 0 |
| crypto/slip39.h | 1589 | `dd177a5e49e17eb0e7def1be13e4b3e529c1fb890f83f5442e05cb0315bba738` | 0 |
| crypto/slip39_english.c | 13890 | `8fc3f9315190504ed455fc9da1cc88fdc2a4bef020c116edbb9b4d46a919c132` | 0 |
| crypto/slip39_wordlist.h | 31482 | `f8c5419144775a45bb6ec49a5a2e339b5b35006795065d4b914427a1dd8714b8` | 0 |
| crypto/tls_prf.c | 3255 | `a35878a414d0e4828067bcc8f5e6f3e0278f7d5da05287337e10072209463d84` | 0 |
| crypto/tls_prf.h | 1429 | `e2f86e529f96f208167b8118122da54756bff87fa06a6339afb607ecf2b3980a` | 0 |
| crypto/tools/bip39bruteforce.c | 2709 | `c9cda21c0539505e8d7503178bc33a1a3fbb0c610ec9b1660a21566bf9a0d7bf` | 0 |
| crypto/tools/mktable.c | 1954 | `d817e8d8badcf9ec5221550175dfb3f5ed15ad3f5a8fe46c0562e7b63f924dc7` | 0 |
| crypto/tools/nem_test_vectors.rb | 2644 | `99184a81184c8f4e522bbc5edf3d9fb25a83e4a8e7f2e193476b36e568f9c1d0` | 0 |
| crypto/tools/xpubaddrgen.c | 1290 | `7f5354bb6605cad3e42a8c649750025e33eba26140949bc8c08d518b4241c549` | 0 |
| crypto/zkp_bip340.c | 10496 | `05e714da983b70ec8a124dbc24e25d3481b34d08c59a75e50ce3b07679056977` | 0 |
| crypto/zkp_bip340.h | 1013 | `349bdf50fa07102e46ce6e03204caf808aa9e39a6a9918791b08a63dd330e6a2` | 0 |
| crypto/zkp_context.c | 3584 | `486a23bd0406f599915dff608709ff04d5d239888dc8a53483711287ee3e6341` | 0 |
| crypto/zkp_context.h | 471 | `5eed6687a0cb95b70dceb5519eb756bfd47235721fa93d25507a8d1b86a11501` | 0 |
| crypto/zkp_ecdsa.c | 15993 | `bf9f86cfb6cd8826db58eec012d766f88515633d7a382ce401291ab172970418` | 0 |
| crypto/zkp_ecdsa.h | 1789 | `96e11e8dedc258e63c6b60e475631075d67bbf0cd29b61bbcc8d4e0619d62227` | 0 |
