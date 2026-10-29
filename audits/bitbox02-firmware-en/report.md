# Security & Post-Quantum Readiness Audit Report

**Project:** bitbox02-firmware-en @ ae548ef4e40f · BitBox (Shift Crypto) — public repository (passive review)
| | |
|---|---|
| Organization | QSI |
| Report date | 2026-10-29 05:31 UTC |
| Report version | 1 |
| Audit run | 5e18f914-8dcb-4f3c-b1a4-538f892ea149 (Document audit) |
| Analyzer engine | qsi-engine 1.2.0 |
| Risk profile | Crypto exchange, custodian or wallet |
| Content SHA-256 | `0f265adc21c8c990d44fbf098fcee7eebde1b04c28396bf07b7094b1e54e848b` |
| Signature key (Ed25519, SHA-256 fingerprint; the signature is the separate file report.sig.json) | `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e` |
> This report presents automated and documented analysis results for the stated scope. It is not a legal opinion, a certification or an attestation of compliance with any standard.

## 1. Executive summary

- Critical: **0**
- High: **0**
- Medium: **11**
- Low: **0**
- Info: **6**

- Confirmed technical vulnerability: 1
- Known vulnerable component: 4
- Confirmed configuration error: 0
- Potential cryptographic risk: 0
- Long-term post-quantum risk: 10
- Improvement recommendation: 1
- Insufficient data: 1

Mosca's inequality (x + y > z): x = 10, y = 5, z = 8 → migration would finish too late under this scenario. _z is a planning assumption chosen per risk profile, not a prediction. A cryptographically relevant quantum computer is not publicly known to exist today._

Analyst review: 12 confirmed, 5 not applicable, 0 dismissed as false positives.

**Post-quantum maturity: Level 0 of 4 — no post-quantum cryptography.** Next step: Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

## 2. Scope and boundaries

Mode: Document audit

Repository: <https://github.com/BitBoxSwiss/bitbox02-firmware> @ `ae548ef4e40f548a17542ba457f138db4fa0069d` — evidence links open the lines at this commit.

721 files, 11803951 bytes in total, 16 redaction(s); the per-file SHA-256 list is in appendix C.

## 3. Methodology

| Area | Status | Count | Examples |
|---|---|---|---|
| chain_map | checked | 3 | messages/btc.proto: Bitcoin; messages/cardano.proto: Cardano; messages/eth.proto: Ethereum and EVM chains |
| source_code | checked | 664 | src/atecc/atecc.c: 795 lines scanned with 16 rule patterns and 123 registry patterns; src/atecc/atecc.h: 38 lines scanned with 16 rule patterns and 123 registry patterns; src/bootloader/boot_args.h: 69 lines scanned with 16 rule patterns and 123 registry patterns |
| dependencies | checked | 40 | src/rust/Cargo.lock: 135 dependencies parsed (135 pinned); src/rust/Cargo.toml: 18 dependencies parsed (0 pinned); src/rust/bins/bitbox03-boot0/Cargo.toml: 2 dependencies parsed (0 pinned) |
| secrets | checked | 8 | src/rust/bitbox-secp256k1/src/lib.rs: value(s) at line(s) 375 (test_dleq), 407 (test_secp256k1_sign), 441 (test_secp256k1_sign_zero_host_nonce_differs_from_no_host_nonce_sign), 456 (test_secp256k1_sign_no_host_nonce_deterministic), 491 (test_secp256k1_nonce_commit) are declared inside a fixture and treated as test data, although the file itself is not test code; src/rust/bitbox-secp256k1/src/lib.rs: 5 redacted value(s) not reported (comments, test modules, fixture declarations, placeholders, values the source annotates as published, or hex values not bound to a secret name); src/rust/bitbox02/src/securechip/imp_fake.rs: 1 redacted value(s) not reported (comments, test modules, fixture declarations, placeholders, values the source annotates as published, or hex values not bound to a secret name) |
| osv_advisories | checked | 1 | 135 pinned packages queried at OSV.dev; 6 affected |

_Long lists are grouped here; the full per-file list is in the JSON report, signed with the same key._

## 4. Assets examined and not examined

- None

## 5. Architecture overview

Static review of the source tree bitbox02-firmware-en at ae548ef4e40f548a17542ba457f138db4fa0069d. 721 files analysed; of 1013 files, 78 are test, fuzzing, benchmark or example code and were left out, 214 are not read by any analyzer, 0 exceed the per-file limit and 0 did not fit the total limit. 132 files come from directories a .gitmodules pins and are read as shipped source rather than skipped as a dependency cache. No requests were sent to the owner's systems.

## 6. Overall security posture

- Indicative posture index: **95** / 100 — _Derived from findings in scope (confirmed and potential issues weighted by severity). Indicative only; not comparable across differently scoped audits._
- Quantum-vulnerable share of inventory: 66.2%

## 7. Detailed findings

### QSI-2026-06382 — Transaction signing for 3 chain(s) relies on elliptic-curve signatures

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: High
> **Analyst review (QSI review, 2026-10-28): confirmed by the analyst.** True by construction. messages/btc.proto, cardano.proto and eth.proto define the supported chains, whose signature schemes are set by consensus rather than by the wallet. The wallet cannot migrate them unilaterally, so this is a readiness map rather than a defect.
- Affected asset: `chain-map`
- Data source: messages/btc.proto
- Detection method: Message definitions (.proto) matched to QSI's table of chain signature schemes.
- Analyzer: chain_map 1.2.0 · 2026-10-29 05:31 UTC
- Priority score: 56.8 / 100
- CVSS v3.1: not applicable

The wallet's message definitions cover Bitcoin, Cardano, Ethereum and EVM chains. These chains authorize transactions with ECDSA, Ed25519, Schnorr (BIP-340), which Shor's algorithm breaks on a cryptographically relevant quantum computer. A wallet cannot move a chain to post-quantum signatures on its own: the chain has to adopt a scheme first.

**Potential impact.** Once a CRQC exists, an attacker who sees an account's public key could derive the private key and move funds; how soon keys are exposed depends on each chain (address reuse, account model).

**Reproduction steps.**

```
Open the .proto files named in the evidence.
```

**Evidence.**

_file_excerpt · [messages/btc.proto](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/messages/btc.proto#L4) · line 4 · SHA-256 9397cf36c17bba81b4bbbc6db29f3dc450925e4566727b47ce57892de62d691d_

```
package shiftcrypto.bitbox02;
```

_file_excerpt · [messages/cardano.proto](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/messages/cardano.proto#L4) · line 4 · SHA-256 9397cf36c17bba81b4bbbc6db29f3dc450925e4566727b47ce57892de62d691d_

```
package shiftcrypto.bitbox02;
```

_file_excerpt · [messages/eth.proto](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/messages/eth.proto#L4) · line 4 · SHA-256 9397cf36c17bba81b4bbbc6db29f3dc450925e4566727b47ce57892de62d691d_

```
package shiftcrypto.bitbox02;
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Chains are recognized from the names of the message definitions (.proto files and packages); the schemes are the chains' documented account signatures, not an analysis of the wallet's signing code.

**Recommendation.** Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains adopt them. Keep the signing layer crypto-agile per chain (algorithm identifiers in messages and storage, room for larger keys and signatures) and track each chain's post-quantum proposals, so that a new scheme can be added when a chain activates it.

**Retest procedure.** Re-run when a chain activates a post-quantum signature scheme or the wallet adds one.

### QSI-2026-06373 — Quantum-vulnerable ECDSA: firmware and boot verification (root of trust) (3 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium
> **Analyst review (QSI review, 2026-10-28): confirmed by the analyst.** The remaining rows carry roles the engine determined and review agrees with, each checked against the cited file. ECDSA at src/bootloader/bootloader.c:537 and stage0/stage1_sigcheck.c is firmware and boot verification, with the public keys fixed in the bootloader: the hardest item to migrate, because it needs new hardware or a signed transition path. X25519 at bitbox-noise/{lib,noise_xx,x25519}.rs is the Noise channel to the host — recordable now, decryptable later, answered by a hybrid exchange. X25519 at bitboxsync.rs is key wrapping at rest. ECDSA across bitbox-secp256k1 and bitbox02-rust (bip32.rs, bip39.rs, hww/api/bitcoin/signmsg.rs) is transaction and message signing on secp256k1. Ed25519 at bitbox02-rust/src/keystore/ed25519.rs is transaction signing on the Cardano path.
- Affected asset: `source-code:ECDSA:root_of_trust`
- Data source: src/bootloader/bootloader.c
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.2.0 · 2026-10-29 05:31 UTC
- Priority score: 43.4 / 100
- CVSS v3.1: not applicable

7 reference(s) to ECDSA across 3 file(s), e.g. src/bootloader/bootloader.c:537. Role, judged from paths, function names and nearby code: firmware and boot verification (root of trust). These public keys are fixed in the bootloader or the device: with a cryptographically relevant quantum computer (CRQC) an attacker forges a firmware signature, and replacing the keys needs a bootloader update in the field.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open src/bootloader/bootloader.c:537 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [src/bootloader/bootloader.c](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/bootloader/bootloader.c#L537) · line 537 · SHA-256 a692ec93e05c715e251b70d5df1203b876ed7d82bd28e9c6b1c10a24cdb7c3d9_

```
  536 |         // First is sanity check
  537 |         if (pukcc_ecdsa_verify(_root_pubkeys[i], sig, random, sizeof(random), curve_p256) != 0) {
  538 |             if (pukcc_ecdsa_verify(_root_pubkeys[i], sig, hash, sizeof(hash), curve_p256) == 0) {
```

_file_excerpt · [src/bootloader/bootloader.c](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/bootloader/bootloader.c#L538) · line 538 · SHA-256 c8910947b0750cbb6c7959f9780e84bfbe3cd04a9d2bb09cbbf7cc1ab9daef34_

```
  537 |         if (pukcc_ecdsa_verify(_root_pubkeys[i], sig, random, sizeof(random), curve_p256) != 0) {
  538 |             if (pukcc_ecdsa_verify(_root_pubkeys[i], sig, hash, sizeof(hash), curve_p256) == 0) {
  539 |                 valid++;
```

_file_excerpt · [src/bootloader/bootloader.c](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/bootloader/bootloader.c#L609) · line 609 · SHA-256 110ab61f5a0020b335e42ad45c11bc760596590d7806f6ab45ae8af2068235cd_

```
  608 |         // First is sanity check
  609 |         if (pukcc_ecdsa_verify(pubkey, sig, random, sizeof(random), curve_p256) != 0) {
  610 |             if (pukcc_ecdsa_verify(pubkey, sig, hash, sizeof(hash), curve_p256) == 0) {
```

_file_excerpt · [src/bootloader/stage0/stage1_sigcheck.c](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/bootloader/stage0/stage1_sigcheck.c#L165) · line 165 · SHA-256 40465ea406a87913706627f03d6592256e6307cc6510acfb3fd097deefc1140b_

```
  164 |         const size_t signature_offset = (size_t)key_idx * BB02_STAGE1_SIGNATURE_LEN;
  165 |         const uint8_t valid = _is_zero_u8(pukcc_ecdsa_verify(
  166 |             pubkeys[key_idx],
```

_file_excerpt · [src/rust/bitbox02-rust-c/src/firmware_c_api.rs](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/rust/bitbox02-rust-c/src/firmware_c_api.rs#L23) · line 23 · SHA-256 0239908a79adffb8db0de707bb0d8d79652f9eee0c4c289c416254e3f87e156a_

```
   22 |     let mut hal = crate::HalImpl::new();
   23 |     util::bb02_async::block_on(bitbox02_rust::secp256k1::init(&mut hal))
   24 |         .expect("secp256k1 context initialization failed");
```

_file_excerpt · [src/rust/bitbox02-rust-c/src/firmware_c_api.rs](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/rust/bitbox02-rust-c/src/firmware_c_api.rs#L24) · line 24 · SHA-256 d2c149057a83a51f66f258261f3e75f6e5d333f7e7cf8e4fb0e01a56de1f4257_

```
   23 |     util::bb02_async::block_on(bitbox02_rust::secp256k1::init(&mut hal))
   24 |         .expect("secp256k1 context initialization failed");
   25 |     bitbox02_rust::main_loop::main_loop(&mut hal)
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Plan a hybrid firmware signature (the classical one plus ML-DSA or SLH-DSA, both required) and the path to ship the new keys in a bootloader update.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-06379 — Quantum-vulnerable X25519: key wrapping and data encryption at rest (1 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium
> **Analyst review (QSI review, 2026-10-28): confirmed by the analyst.** The remaining rows carry roles the engine determined and review agrees with, each checked against the cited file. ECDSA at src/bootloader/bootloader.c:537 and stage0/stage1_sigcheck.c is firmware and boot verification, with the public keys fixed in the bootloader: the hardest item to migrate, because it needs new hardware or a signed transition path. X25519 at bitbox-noise/{lib,noise_xx,x25519}.rs is the Noise channel to the host — recordable now, decryptable later, answered by a hybrid exchange. X25519 at bitboxsync.rs is key wrapping at rest. ECDSA across bitbox-secp256k1 and bitbox02-rust (bip32.rs, bip39.rs, hww/api/bitcoin/signmsg.rs) is transaction and message signing on secp256k1. Ed25519 at bitbox02-rust/src/keystore/ed25519.rs is transaction signing on the Cardano path.
- Affected asset: `source-code:X25519:key_wrapping`
- Data source: src/rust/bitbox02-rust/src/hww/api/bitboxsync.rs
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.2.0 · 2026-10-29 05:31 UTC
- Priority score: 43.4 / 100
- CVSS v3.1: not applicable

4 reference(s) to X25519 across 1 file(s), e.g. src/rust/bitbox02-rust/src/hww/api/bitboxsync.rs:15. Role, judged from paths, function names and nearby code: key wrapping and data encryption at rest. Keys or data encrypted to these public keys are stored: anyone who copies them now decrypts them once a CRQC exists (harvest now, decrypt later).

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open src/rust/bitbox02-rust/src/hww/api/bitboxsync.rs:15 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [src/rust/bitbox02-rust/src/hww/api/bitboxsync.rs](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/rust/bitbox02-rust/src/hww/api/bitboxsync.rs#L15) · line 15 · SHA-256 1c153d0b1adf9cd8ecf03da5502f8e68db447b4ab09e5e61188fc538699029d9_

```
   14 | use sha2::{Digest, Sha256};
   15 | use x25519_dalek::{PublicKey as X25519PublicKey, StaticSecret as X25519StaticSecret};
   16 | use zeroize::{Zeroize, Zeroizing};
```

_file_excerpt · [src/rust/bitbox02-rust/src/hww/api/bitboxsync.rs](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/rust/bitbox02-rust/src/hww/api/bitboxsync.rs#L19) · line 19 · SHA-256 4b67afd4d285deeff00b1d8a4e6ef086fbb387cad74ce1646456a0830671584e_

```
   18 | const AUTH_SEED_LABEL: &[u8] = b"bitboxsync-auth-ed25519-seed-v1";
   19 | const WRAP_SEED_LABEL: &[u8] = b"bitboxsync-wrap-x25519-seed-v1";
   20 | 
```

_file_excerpt · [src/rust/bitbox02-rust/src/hww/api/bitboxsync.rs](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/rust/bitbox02-rust/src/hww/api/bitboxsync.rs#L60) · line 60 · SHA-256 f8ee14a435cd94f2c3694c380ab36b8cca17c6d237875854295e567d7ab0e0ef_

```
   59 |     let wrap_secret = [REDACTED]
   60 |     let wrap_public_key = X25519PublicKey::from(&wrap_secret).to_bytes();
   61 | 
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Wrap keys with ML-KEM or a hybrid KEM (X25519 + ML-KEM-768) and re-wrap the stored keys; data that may already have been copied needs its own assessment.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-06375 — Quantum-vulnerable X25519: channel key exchange (TLS, Noise, handshakes) (3 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium
> **Analyst review (QSI review, 2026-10-28): confirmed by the analyst.** The remaining rows carry roles the engine determined and review agrees with, each checked against the cited file. ECDSA at src/bootloader/bootloader.c:537 and stage0/stage1_sigcheck.c is firmware and boot verification, with the public keys fixed in the bootloader: the hardest item to migrate, because it needs new hardware or a signed transition path. X25519 at bitbox-noise/{lib,noise_xx,x25519}.rs is the Noise channel to the host — recordable now, decryptable later, answered by a hybrid exchange. X25519 at bitboxsync.rs is key wrapping at rest. ECDSA across bitbox-secp256k1 and bitbox02-rust (bip32.rs, bip39.rs, hww/api/bitcoin/signmsg.rs) is transaction and message signing on secp256k1. Ed25519 at bitbox02-rust/src/keystore/ed25519.rs is transaction signing on the Cardano path.
- Affected asset: `source-code:X25519:channel`
- Data source: src/rust/bitbox-noise/src/lib.rs
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.2.0 · 2026-10-29 05:31 UTC
- Priority score: 41.8 / 100
- CVSS v3.1: not applicable

6 reference(s) to X25519 across 3 file(s), e.g. src/rust/bitbox-noise/src/lib.rs:16. Role, judged from paths, function names and nearby code: channel key exchange (TLS, Noise, handshakes). Traffic protected by this key exchange can be recorded now and decrypted later; a hybrid exchange keeps the classical guarantees and adds post-quantum ones.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open src/rust/bitbox-noise/src/lib.rs:16 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [src/rust/bitbox-noise/src/lib.rs](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/rust/bitbox-noise/src/lib.rs#L16) · line 16 · SHA-256 bec1cc899b2ee57631342068081612e177c1e131b0062f84dbf4bd19b81f7b9e_

```
   15 | pub mod testing;
   16 | mod x25519;
   17 | 
```

_file_excerpt · [src/rust/bitbox-noise/src/lib.rs](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/rust/bitbox-noise/src/lib.rs#L19) · line 19 · SHA-256 57cd8f7157563d1d7dcdedce2582f83213eb268d9f974d8d82700859104ba8c2_

```
   18 | pub use noise_xx::{Error, HandshakeHash, HandshakeResult, State};
   19 | pub use x25519::{X25519, genkey};
   20 | 
```

_file_excerpt · [src/rust/bitbox-noise/src/noise_xx.rs](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/rust/bitbox-noise/src/noise_xx.rs#L8) · line 8 · SHA-256 784affd9139fdfbf69bb890deb430326b00ccb48a47de6340bd5071c807628b4_

```
    7 | 
    8 | use crate::x25519::{PrivateKey, PublicKey, X25519, genkey};
    9 | use noise_rust_crypto::{ChaCha20Poly1305, Sha256, sensitive::Sensitive};
```

_file_excerpt · [src/rust/bitbox-noise/src/x25519.rs](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/rust/bitbox-noise/src/x25519.rs#L49) · line 49 · SHA-256 43d70ab747c41c47e17b5ba00fdf0933116113165cc5310d5e74f3736664266f_

```
   48 |     fn pubkey(k: &Self::Key) -> Self::Pubkey {
   49 |         let static_secret = [REDACTED]
   50 |         *x25519_dalek::PublicKey::from(&static_secret).as_bytes()
```

_file_excerpt · [src/rust/bitbox-noise/src/x25519.rs](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/rust/bitbox-noise/src/x25519.rs#L54) · line 54 · SHA-256 fae4ff917820e0219e7ac326306ae796207dce8f7af4ff5e75fd4328d8d0eaee_

```
   53 |     fn dh(k: &Self::Key, pk: &Self::Pubkey) -> Result<Self::Output, ()> {
   54 |         let k = x25519_dalek::StaticSecret::from(*k.deref());
   55 |         let pk = x25519_dalek::PublicKey::from(*pk);
```

_file_excerpt · [src/rust/bitbox-noise/src/x25519.rs](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/rust/bitbox-noise/src/x25519.rs#L55) · line 55 · SHA-256 9cb9b67a0b6ccdefe882b0cd12a8a8e62cc7886bd8c3fa9cc44154fd180c819c_

```
   54 |         let k = x25519_dalek::StaticSecret::from(*k.deref());
   55 |         let pk = x25519_dalek::PublicKey::from(*pk);
   56 |         Ok(*k.diffie_hellman(&pk).as_bytes())
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Move the handshake to a hybrid key exchange (X25519MLKEM768 in TLS 1.3; a hybrid KEM in Noise-based protocols).

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-06376 — Quantum-vulnerable ECDSA: transaction and message signing (50 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium
> **Analyst review (QSI review, 2026-10-28): confirmed by the analyst.** The remaining rows carry roles the engine determined and review agrees with, each checked against the cited file. ECDSA at src/bootloader/bootloader.c:537 and stage0/stage1_sigcheck.c is firmware and boot verification, with the public keys fixed in the bootloader: the hardest item to migrate, because it needs new hardware or a signed transition path. X25519 at bitbox-noise/{lib,noise_xx,x25519}.rs is the Noise channel to the host — recordable now, decryptable later, answered by a hybrid exchange. X25519 at bitboxsync.rs is key wrapping at rest. ECDSA across bitbox-secp256k1 and bitbox02-rust (bip32.rs, bip39.rs, hww/api/bitcoin/signmsg.rs) is transaction and message signing on secp256k1. Ed25519 at bitbox02-rust/src/keystore/ed25519.rs is transaction signing on the Cardano path.
- Affected asset: `source-code:ECDSA:transaction_signing`
- Data source: src/rust/bitbox-secp256k1/build.rs
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.2.0 · 2026-10-29 05:31 UTC
- Priority score: 41.8 / 100
- CVSS v3.1: not applicable

161 reference(s) to ECDSA across 50 file(s), e.g. src/rust/bitbox-secp256k1/build.rs:6. Role, judged from paths, function names and nearby code: transaction and message signing. A CRQC derives the private key from a public key that is already known (on chain after the first spend, in reused addresses): funds and approvals controlled by these keys need a migration path.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open src/rust/bitbox-secp256k1/build.rs:6 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [src/rust/bitbox-secp256k1/build.rs](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/rust/bitbox-secp256k1/build.rs#L6) · line 6 · SHA-256 c0e8a8076dd2e70e550d1aa3c11d2672989702f68a84802e08636e784b6d41f8_

```
    5 | fn main() {
    6 |     let secp_dir = PathBuf::from("depend/secp256k1-zkp");
    7 |     let callbacks = PathBuf::from("src/default_callbacks.c");
```

_file_excerpt · [src/rust/bitbox-secp256k1/build.rs](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/rust/bitbox-secp256k1/build.rs#L18) · line 18 · SHA-256 25e9545e63d24ed02198281c8da70ca8d5106db13c770d3cb0563ef91611ce31_

```
   17 |     build
   18 |         .file(secp_dir.join("src/secp256k1.c"))
   19 |         .file(secp_dir.join("src/precomputed_ecmult.c"))
```

_file_excerpt · [src/rust/bitbox-secp256k1/build.rs](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/rust/bitbox-secp256k1/build.rs#L37) · line 37 · SHA-256 47d7abfe9efe1b2bea40a263634d29da5de554eb838641f36186b8d302876eb6_

```
   36 | 
   37 |     build.compile("secp256k1");
   38 | }
```

_file_excerpt · [src/rust/bitbox-secp256k1/depend/secp256k1-zkp/contrib/lax_der_parsing.c](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/rust/bitbox-secp256k1/depend/secp256k1-zkp/contrib/lax_der_parsing.c#L11) · line 11 · SHA-256 9197354c850cb53bbc475b348c0f97bb3f550706fcced8bf483336d626575330_

```
   10 | 
   11 | int ecdsa_signature_parse_der_lax(const secp256k1_context* ctx, secp256k1_ecdsa_signature* sig, const unsigned char *input, size_t inputlen) {
   12 |     size_t rpos, rlen, spos, slen;
```

_file_excerpt · [src/rust/bitbox-secp256k1/depend/secp256k1-zkp/contrib/lax_der_parsing.c](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/rust/bitbox-secp256k1/depend/secp256k1-zkp/contrib/lax_der_parsing.c#L19) · line 19 · SHA-256 234aeaaf6b28e1d2ff43854e60a3119e3c3f55229e18841e2dc766404eab65d0_

```
   18 |     /* Hack to initialize sig with a correctly-parsed but invalid signature. */
   19 |     secp256k1_ecdsa_signature_parse_compact(ctx, sig, tmpsig);
   20 | 
```

_file_excerpt · [src/rust/bitbox-secp256k1/depend/secp256k1-zkp/contrib/lax_der_parsing.c](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/rust/bitbox-secp256k1/depend/secp256k1-zkp/contrib/lax_der_parsing.c#L140) · line 140 · SHA-256 75ad5d0cba25ca64adb6d971da937879704b4abc8845c17dc1da9fa1eb773e5e_

```
  139 |     if (!overflow) {
  140 |         overflow = !secp256k1_ecdsa_signature_parse_compact(ctx, sig, tmpsig);
  141 |     }
```

_file_excerpt · [src/rust/bitbox-secp256k1/depend/secp256k1-zkp/contrib/lax_der_parsing.h](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/rust/bitbox-secp256k1/depend/secp256k1-zkp/contrib/lax_der_parsing.h#L57) · line 57 · SHA-256 25af7e242d92af0d3c46ae8d8a48030e247c4bfdeba65068030e64eb4c88c912_

```
   56 |    files (such as tests.c) without the need to set an explicit -I flag,
   57 |    which would be necessary to locate secp256k1.h. */
   58 | #ifndef SECP256K1_H
```

_file_excerpt · [src/rust/bitbox-secp256k1/depend/secp256k1-zkp/contrib/lax_der_parsing.h](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/rust/bitbox-secp256k1/depend/secp256k1-zkp/contrib/lax_der_parsing.h#L59) · line 59 · SHA-256 4c35a81e99a7eaf5ea7315346f3b8cacb0832f7c4a3b1a3d003ff0bd3b6a82c1_

```
   58 | #ifndef SECP256K1_H
   59 | #include <secp256k1.h>
   60 | #endif
```

_file_excerpt · [src/rust/bitbox-secp256k1/depend/secp256k1-zkp/contrib/lax_der_parsing.h](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/rust/bitbox-secp256k1/depend/secp256k1-zkp/contrib/lax_der_parsing.h#L88) · line 88 · SHA-256 85efcade66268dd4d0b42e8f31b634ea4cd93d9d55cdc2e036715108d8697665_

```
   87 |     const secp256k1_context* ctx,
   88 |     secp256k1_ecdsa_signature* sig,
   89 |     const unsigned char *input,
```

_file_excerpt · [src/rust/bitbox-secp256k1/depend/secp256k1-zkp/contrib/lax_der_privatekey_parsing.h](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/rust/bitbox-secp256k1/depend/secp256k1-zkp/contrib/lax_der_privatekey_parsing.h#L34) · line 34 · SHA-256 163cac24f6b60e798317e2383fb603da718e728035262dc9759d7cf3fbd47b4f_

```
   33 |    files (such as tests.c) without the need to set an explicit -I flag,
   34 |    which would be necessary to locate secp256k1.h. */
   35 | #ifndef SECP256K1_H
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains adopt them.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-06377 — Quantum-vulnerable Schnorr (BIP-340): transaction and message signing (6 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium
> **Analyst review (QSI review, 2026-10-28): confirmed by the analyst.** The remaining rows carry roles the engine determined and review agrees with, each checked against the cited file. ECDSA at src/bootloader/bootloader.c:537 and stage0/stage1_sigcheck.c is firmware and boot verification, with the public keys fixed in the bootloader: the hardest item to migrate, because it needs new hardware or a signed transition path. X25519 at bitbox-noise/{lib,noise_xx,x25519}.rs is the Noise channel to the host — recordable now, decryptable later, answered by a hybrid exchange. X25519 at bitboxsync.rs is key wrapping at rest. ECDSA across bitbox-secp256k1 and bitbox02-rust (bip32.rs, bip39.rs, hww/api/bitcoin/signmsg.rs) is transaction and message signing on secp256k1. Ed25519 at bitbox02-rust/src/keystore/ed25519.rs is transaction signing on the Cardano path.
- Affected asset: `source-code:Schnorr (BIP-340):transaction_signing`
- Data source: src/rust/bitbox-secp256k1/depend/secp256k1-zkp/include/secp256k1_schnorrsig.h
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.2.0 · 2026-10-29 05:31 UTC
- Priority score: 41.8 / 100
- CVSS v3.1: not applicable

37 reference(s) to Schnorr (BIP-340) across 6 file(s), e.g. src/rust/bitbox-secp256k1/depend/secp256k1-zkp/include/secp256k1_schnorrsig.h:82. Role, judged from paths, function names and nearby code: transaction and message signing. A CRQC derives the private key from a public key that is already known (on chain after the first spend, in reused addresses): funds and approvals controlled by these keys need a migration path.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open src/rust/bitbox-secp256k1/depend/secp256k1-zkp/include/secp256k1_schnorrsig.h:82 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [src/rust/bitbox-secp256k1/depend/secp256k1-zkp/include/secp256k1_schnorrsig.h](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/rust/bitbox-secp256k1/depend/secp256k1-zkp/include/secp256k1_schnorrsig.h#L82) · line 82 · SHA-256 6aae3b20f8f8b503597acb97fe491246b6777b5a9660b8a41542605d18aab6f4_

```
   81 |  */
   82 | typedef struct secp256k1_schnorrsig_extraparams {
   83 |     unsigned char magic[4];
```

_file_excerpt · [src/rust/bitbox-secp256k1/depend/secp256k1-zkp/include/secp256k1_schnorrsig.h](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/rust/bitbox-secp256k1/depend/secp256k1-zkp/include/secp256k1_schnorrsig.h#L86) · line 86 · SHA-256 43d5f6045ac4e6b23daf11fd6c10022dca16ca76afd775c3ee898ddbef44d5bd_

```
   85 |     void *ndata;
   86 | } secp256k1_schnorrsig_extraparams;
   87 | 
```

_file_excerpt · [src/rust/bitbox-secp256k1/depend/secp256k1-zkp/include/secp256k1_schnorrsig.h](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/rust/bitbox-secp256k1/depend/secp256k1-zkp/include/secp256k1_schnorrsig.h#L119) · line 119 · SHA-256 1e555d327421285c8a81345e58876f5f2f017571adb2f2168aafc7c44770594c_

```
  118 |  */
  119 | SECP256K1_API int secp256k1_schnorrsig_sign32(
  120 |     const secp256k1_context *ctx,
```

_file_excerpt · [src/rust/bitbox-secp256k1/depend/secp256k1-zkp/include/secp256k1_schnorrsig_halfagg.h](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/rust/bitbox-secp256k1/depend/secp256k1-zkp/include/secp256k1_schnorrsig_halfagg.h#L43) · line 43 · SHA-256 b3d54ae6f144846b9769cfe141d006f33bf49fa9572bafb7307c2ade17fd95eb_

```
   42 |  */
   43 | SECP256K1_API int secp256k1_schnorrsig_inc_aggregate(
   44 |     const secp256k1_context *ctx,
```

_file_excerpt · [src/rust/bitbox-secp256k1/depend/secp256k1-zkp/include/secp256k1_schnorrsig_halfagg.h](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/rust/bitbox-secp256k1/depend/secp256k1-zkp/include/secp256k1_schnorrsig_halfagg.h#L70) · line 70 · SHA-256 be378be4953e3b3d2e2b5a4ddab26874bc43e6f72392495b730cac093c057a7a_

```
   69 |  */
   70 | SECP256K1_API int secp256k1_schnorrsig_aggregate(
   71 |     const secp256k1_context *ctx,
```

_file_excerpt · [src/rust/bitbox-secp256k1/depend/secp256k1-zkp/include/secp256k1_schnorrsig_halfagg.h](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/rust/bitbox-secp256k1/depend/secp256k1-zkp/include/secp256k1_schnorrsig_halfagg.h#L94) · line 94 · SHA-256 b10de912dd2b9f3e510c8fe909f0b6db3a25cde95edbbe0af55b109a33026fce_

```
   93 |  */
   94 | SECP256K1_API SECP256K1_WARN_UNUSED_RESULT int secp256k1_schnorrsig_aggverify(
   95 |     const secp256k1_context *ctx,
```

_file_excerpt · [src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/modules/musig/session_impl.h](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/modules/musig/session_impl.h#L621) · line 621 · SHA-256 6254128e9a575e14bb87c68d5f2f12d65a6084dd7de58385e4a2764f96f3935a_

```
  620 |     secp256k1_musig_nonce_process_internal(ctx, &session_i.fin_nonce_parity, fin_nonce, &session_i.noncecoef, aggnonce_pts, agg_pk32, msg32);
  621 |     secp256k1_schnorrsig_challenge(secp256k1_get_hash_context(ctx), &session_i.challenge, fin_nonce, msg32, 32, agg_pk32);
  622 | 
```

_file_excerpt · [src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/modules/schnorrsig/bench_impl.h](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/modules/schnorrsig/bench_impl.h#L33) · line 33 · SHA-256 fc2c5559f32fc9bd9a85efef59a46eaf722b1b8e2745b837696cdf6a6c00259e_

```
   32 |         msg[1] = i >> 8;
   33 |         CHECK(secp256k1_schnorrsig_sign_custom(data->ctx, sig, msg, MSGLEN, data->keypairs[i], NULL));
   34 |     }
```

_file_excerpt · [src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/modules/schnorrsig/bench_impl.h](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/modules/schnorrsig/bench_impl.h#L44) · line 44 · SHA-256 4f2e9b7b2529431d8190d606bbe0ce49659d6e5a1e0410625d931eacdcd05a06_

```
   43 |         CHECK(secp256k1_xonly_pubkey_parse(data->ctx, &pk, data->pk[i]) == 1);
   44 |         CHECK(secp256k1_schnorrsig_verify(data->ctx, data->sigs[i], data->msgs[i], MSGLEN, &pk));
   45 |     }
```

_file_excerpt · [src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/modules/schnorrsig/bench_impl.h](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/modules/schnorrsig/bench_impl.h#L80) · line 80 · SHA-256 0ca8c9b51520014576b4c622e33014e8b93cc7c4bd0bc826e9cd4563a3642698_

```
   79 |         CHECK(secp256k1_keypair_create(data.ctx, keypair, sk));
   80 |         CHECK(secp256k1_schnorrsig_sign_custom(data.ctx, sig, msg, MSGLEN, keypair, NULL));
   81 |         CHECK(secp256k1_keypair_xonly_pub(data.ctx, &pk, NULL, keypair));
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains adopt them.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-06381 — Quantum-vulnerable Ed25519: transaction and message signing (1 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium
> **Analyst review (QSI review, 2026-10-28): confirmed by the analyst.** The remaining rows carry roles the engine determined and review agrees with, each checked against the cited file. ECDSA at src/bootloader/bootloader.c:537 and stage0/stage1_sigcheck.c is firmware and boot verification, with the public keys fixed in the bootloader: the hardest item to migrate, because it needs new hardware or a signed transition path. X25519 at bitbox-noise/{lib,noise_xx,x25519}.rs is the Noise channel to the host — recordable now, decryptable later, answered by a hybrid exchange. X25519 at bitboxsync.rs is key wrapping at rest. ECDSA across bitbox-secp256k1 and bitbox02-rust (bip32.rs, bip39.rs, hww/api/bitcoin/signmsg.rs) is transaction and message signing on secp256k1. Ed25519 at bitbox02-rust/src/keystore/ed25519.rs is transaction signing on the Cardano path.
- Affected asset: `source-code:Ed25519:transaction_signing`
- Data source: src/rust/bitbox02-rust/src/keystore/ed25519.rs
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.2.0 · 2026-10-29 05:31 UTC
- Priority score: 41.8 / 100
- CVSS v3.1: not applicable

2 reference(s) to Ed25519 across 1 file(s), e.g. src/rust/bitbox02-rust/src/keystore/ed25519.rs:10. Role, judged from paths, function names and nearby code: transaction and message signing. A CRQC derives the private key from a public key that is already known (on chain after the first spend, in reused addresses): funds and approvals controlled by these keys need a migration path.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open src/rust/bitbox02-rust/src/keystore/ed25519.rs:10 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [src/rust/bitbox02-rust/src/keystore/ed25519.rs](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/rust/bitbox02-rust/src/keystore/ed25519.rs#L10) · line 10 · SHA-256 0d1f71033a48c3c6e0b8363e9a41c2f5e9ee07f08735238e9856e64b2125dfbc_

```
    9 | use digest::Digest;
   10 | use ed25519_dalek::VerifyingKey;
   11 | use ed25519_dalek::hazmat::{ExpandedSecretKey, raw_sign};
```

_file_excerpt · [src/rust/bitbox02-rust/src/keystore/ed25519.rs](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/rust/bitbox02-rust/src/keystore/ed25519.rs#L11) · line 11 · SHA-256 449e9e250d19db94ff94019815e29a47323da4b3df842285684544d908651dd6_

```
   10 | use ed25519_dalek::VerifyingKey;
   11 | use ed25519_dalek::hazmat::{ExpandedSecretKey, raw_sign};
   12 | 
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains adopt them.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-06374 — Quantum-vulnerable ECDSA: role not determined (6 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium
> **Analyst review (QSI review, 2026-10-28): confirmed by the analyst.** Role resolved for all six files, and they are three different roles rather than one. src/pukcc/pukcc.c:181 is pukcc_ecdsa_verify, the ATSAM PUKCC hardware public-key controller performing ECDSA *verification* — the bootloader's signature check, so a root-of-trust item, and verification uses public keys only, which puts it outside any timing concern. src/rust/streaming-silent-payments/{lib,hash}.rs is BIP-352 silent payments, i.e. address derivation on secp256k1. src/rust/util/src/p256.rs is the U2F/FIDO P-256 signing described in the crypto-bigint decision above. Each has a different migration deadline, which is why leaving them merged as "role not determined" would be the wrong input to a plan.
- Affected asset: `source-code:ECDSA:general`
- Data source: src/pukcc/pukcc.c
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.2.0 · 2026-10-29 05:31 UTC
- Priority score: 40.2 / 100
- CVSS v3.1: not applicable

10 reference(s) to ECDSA across 6 file(s), e.g. src/pukcc/pukcc.c:181. Role, judged from paths, function names and nearby code: role not determined. The code does not show what the keys protect; review decides the priority.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open src/pukcc/pukcc.c:181 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [src/pukcc/pukcc.c](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/pukcc/pukcc.c#L181) · line 181 · SHA-256 53085ff2be44540f9ac0d6f54f71ca19c4e1ac12898aef6c3ecb093df8a5a67f_

```
  180 | // Returns 0 on success
  181 | uint8_t pukcc_ecdsa_verify(
  182 |     const uint8_t* public_key,
```

_file_excerpt · [src/pukcc/pukcc.h](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/pukcc/pukcc.h#L30) · line 30 · SHA-256 dae3c783558d199701f2f4d6fa2a10c198ed29cea93653a188e191295bde9364_

```
   29 | 
   30 | uint8_t pukcc_ecdsa_verify(
   31 |     const uint8_t* public_key,
```

_file_excerpt · [src/rust/bitbox02-rust-c/src/lib.rs](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/rust/bitbox02-rust-c/src/lib.rs#L23) · line 23 · SHA-256 e527a51a0f0f62d0ee3a3e27b910a798f61d791ba1bc143ec92bfdcc1f607025_

```
   22 | #[cfg(feature = "factory-setup")]
   23 | mod secp256k1;
   24 | 
```

_file_excerpt · [src/rust/streaming-silent-payments/src/hash.rs](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/rust/streaming-silent-payments/src/hash.rs#L7) · line 7 · SHA-256 33201f813f216ace1faa8378e7cbee0f992739d6b30c90a1a740a8cc81e3f455_

```
    6 | use bitcoin::hashes::{Hash, HashEngine, sha256t_hash_newtype};
    7 | use bitcoin::secp256k1::{PublicKey, Scalar};
    8 | 
```

_file_excerpt · [src/rust/streaming-silent-payments/src/lib.rs](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/rust/streaming-silent-payments/src/lib.rs#L12) · line 12 · SHA-256 08a764387fbe8ba1e77642c172a087172ccf897e6ed0de3209ef2dc8587547dc_

```
   11 | use bitcoin::hashes::Hash;
   12 | use bitcoin::secp256k1::{self, PublicKey, Scalar, Secp256k1, SecretKey, XOnlyPublicKey};
   13 | 
```

_file_excerpt · [src/rust/streaming-silent-payments/src/lib.rs](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/rust/streaming-silent-payments/src/lib.rs#L43) · line 43 · SHA-256 08787745f17bf5694851af8a934a9791f92c751c329c4e20cd230db9145ae5ba_

```
   42 | pub struct SilentPayment<'a> {
   43 |     secp: &'a Secp256k1<secp256k1::All>,
   44 |     network: Network,
```

_file_excerpt · [src/rust/streaming-silent-payments/src/lib.rs](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/rust/streaming-silent-payments/src/lib.rs#L124) · line 124 · SHA-256 14bc8680433716b8fc52ba9a85b1577a9648567735eefacba61ba01fa093709e_

```
  123 | fn create_dleq_proof(
  124 |     secp: &Secp256k1<secp256k1::All>,
  125 |     a_sum: &SecretKey,
```

_file_excerpt · [src/rust/util/src/p256.rs](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/rust/util/src/p256.rs#L28) · line 28 · SHA-256 925484476bdd234888084554a30574f13c31fd235705950f76e225d606f36aee_

```
   27 | ) {
   28 |     use p256::ecdsa::{Signature, SigningKey, signature::hazmat::PrehashSigner};
   29 |     let signing_key = SigningKey::from_slice(private_key.as_ref()).unwrap();
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it; introduce an abstraction layer for crypto-agility.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-06378 — Quantum-vulnerable ECDH: role not determined (1 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium
> **Analyst review (QSI review, 2026-10-28): confirmed by the analyst.** The remaining rows carry roles the engine determined and review agrees with, each checked against the cited file. ECDSA at src/bootloader/bootloader.c:537 and stage0/stage1_sigcheck.c is firmware and boot verification, with the public keys fixed in the bootloader: the hardest item to migrate, because it needs new hardware or a signed transition path. X25519 at bitbox-noise/{lib,noise_xx,x25519}.rs is the Noise channel to the host — recordable now, decryptable later, answered by a hybrid exchange. X25519 at bitboxsync.rs is key wrapping at rest. ECDSA across bitbox-secp256k1 and bitbox02-rust (bip32.rs, bip39.rs, hww/api/bitcoin/signmsg.rs) is transaction and message signing on secp256k1. Ed25519 at bitbox02-rust/src/keystore/ed25519.rs is transaction signing on the Cardano path.
- Affected asset: `source-code:ECDH:general`
- Data source: src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/bench.c
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.2.0 · 2026-10-29 05:31 UTC
- Priority score: 40.2 / 100
- CVSS v3.1: not applicable

4 reference(s) to ECDH across 1 file(s), e.g. src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/bench.c:24. Role, judged from paths, function names and nearby code: role not determined. The code does not show what the keys protect; review decides the priority.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/bench.c:24 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/bench.c](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/bench.c#L24) · line 24 · SHA-256 6ec91ca104f465f4b861193bee0ed1f6d91c4074fb5085511ca06c7dd6747616_

```
   23 | #ifdef ENABLE_MODULE_ECDH
   24 |     printf("    - ECDH key exchange (optional module)\n");
   25 | #endif
```

_file_excerpt · [src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/bench.c](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/bench.c#L54) · line 54 · SHA-256 b21ecd8d53157d4f920477f57713fa34b7fe6379df61daa64f27e4a77f9133e1_

```
   53 | #ifdef ENABLE_MODULE_ECDH
   54 |     printf("    ecdh              : ECDH key exchange algorithm\n");
   55 | #endif
```

_file_excerpt · [src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/bench.c](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/bench.c#L68) · line 68 · SHA-256 ae7392892e7a0840c3596f3442ca87927d89cc694ec91267d2a73193091dac83_

```
   67 |     printf("    ellswift_keygen   : ElligatorSwift key generation\n");
   68 |     printf("    ellswift_ecdh     : ECDH on ElligatorSwift keys\n");
   69 | #endif
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Classify each usage, record data lifetimes, and plan migration to Hybrid key establishment with ML-KEM (FIPS 203), e.g. X25519MLKEM768 in TLS 1.3 or mlkem768x25519-sha256 in SSH; introduce an abstraction layer for crypto-agility.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-06380 — Quantum-vulnerable Ed25519: role not determined (1 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium
> **Analyst review (QSI review, 2026-10-28): confirmed by the analyst.** Role resolved: the single anchor is src/rust/bitbox02-rust/src/hww/api/bitboxsync.rs:11, the same file that carries the X25519 at-rest row. BitBoxSync wraps synchronised data to a recipient public key, so this is key wrapping and encryption at rest, and harvest-now-decrypt-later applies: anything copied today is readable once a CRQC exists. Highest-urgency class in this repository, because unlike signing it cannot be fixed retroactively.
- Affected asset: `source-code:Ed25519:general`
- Data source: src/rust/bitbox02-rust/src/hww/api/bitboxsync.rs
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.2.0 · 2026-10-29 05:31 UTC
- Priority score: 40.2 / 100
- CVSS v3.1: not applicable

1 reference(s) to Ed25519 across 1 file(s), e.g. src/rust/bitbox02-rust/src/hww/api/bitboxsync.rs:11. Role, judged from paths, function names and nearby code: role not determined. The code does not show what the keys protect; review decides the priority.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open src/rust/bitbox02-rust/src/hww/api/bitboxsync.rs:11 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [src/rust/bitbox02-rust/src/hww/api/bitboxsync.rs](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/rust/bitbox02-rust/src/hww/api/bitboxsync.rs#L11) · line 11 · SHA-256 3637a75aa4245184b2de8e6f4f098698530fa03b423eab7638b978e20ddeb24d_

```
   10 | use chacha20poly1305::aead::{AeadInPlace, KeyInit};
   11 | use ed25519_dalek::VerifyingKey;
   12 | use hkdf::Hkdf;
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it; introduce an abstraction layer for crypto-agility.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-06387 — crypto-bigint 0.5.5 is affected by RUSTSEC-2026-0387 (no severity rating)

- Severity: **Medium** · Classification: Confirmed technical vulnerability · Confidence: Low
> **Analyst review (QSI review, 2026-10-28): confirmed by the analyst.** crypto-bigint 0.5.5 (multiple timing variability issues in operations intended to be constant-time) is reachable in shipped firmware, and the path is worth stating exactly because it is narrower than it looks. src/rust/util/Cargo.toml:17 takes p256 as an *optional* dependency with features ["arithmetic", "ecdsa"], and lib.rs guards it with #[cfg(feature = "p256")]. That feature is switched on in exactly one place: src/rust/bitbox02-rust-c/Cargo.toml, inside the app-u2f feature block ("util/p256"). So p256 -> elliptic-curve -> crypto-bigint is compiled in whenever the U2F/FIDO app is built — the Multi edition — and is absent from a Bitcoin-only build. What it does there is secret-dependent: util/src/p256.rs exports rust_p256_sign, which calls SigningKey::sign_prehash with a private key over the C FFI, i.e. U2F authentication signatures on NIST P-256. The keys at stake are therefore FIDO credentials, NOT bitcoin spending keys: those go through bitbox-secp256k1 (libsecp256k1 in C), which this advisory does not touch. Stated precisely: no exploit is demonstrated, and the attacker model is physical possession plus timing measurement, which is the threat a hardware wallet exists to resist — hence medium rather than low. Fix available in crypto-bigint 0.7.6; maintainers should match the advisory's named operations against p256's scalar arithmetic. _automated severity: Low._
- Affected asset: `dependency:crates.io/crypto-bigint@0.5.5`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-29 05:31 UTC
- Priority score: 27.7 / 100
- CVSS v3.1: not applicable

OSV.dev reports RUSTSEC-2026-0387 for crates.io package crypto-bigint at version 0.5.5: Multiple timing variability issues in operations intended to be constant-time. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. The advisory names no affected functions, so reachability was not determined.

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

### QSI-2026-06388 — keccak 0.1.4 is affected by GHSA-3288-p39f-rqpv (RUSTSEC-2026-0012)

- Severity: **Info** · Classification: Known vulnerable component · Confidence: Medium
> **Analyst review (QSI review, 2026-10-28): not applicable to this code.** keccak 0.1.4's unsoundness is in the opt-in ARMv8 assembly backend behind the asm Cargo feature, which is off by default and which no manifest in src/rust enables. Its consumers are bitbox02-rust and sha3, both using the portable implementation. Upgrading to 0.1.6 is still the cheap move during routine maintenance.
- Affected asset: `dependency:crates.io/keccak@0.1.4`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-29 05:31 UTC
- Priority score: 35.2 / 100
- CVSS v3.1: not applicable

OSV.dev reports GHSA-3288-p39f-rqpv (RUSTSEC-2026-0012) for crates.io package keccak at version 0.1.4: Unsoundness in opt-in ARMv8 assembly backend for `keccak`. The affected code sits behind the `asm` Cargo feature, off by default, which no audited manifest enables: the advisory does not apply unless another dependency enables it.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-3288-p39f-rqpv
```

**Evidence.**

_tool_output · [OSV.dev GHSA-3288-p39f-rqpv](https://osv.dev/vulnerability/GHSA-3288-p39f-rqpv) · manifest · SHA-256 638750a493b76f126adef65e1dd53e2ef494cf4b1d4c7edcc7db12181ba27f6c_

```
{"id": "GHSA-3288-p39f-rqpv", "aliases": ["RUSTSEC-2026-0012"], "modified": "2026-09-10T03:50:59.332505686Z", "summary": "Unsoundness in opt-in ARMv8 assembly backend for `keccak`", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:L/AC:H/AT:P/PR:N/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N/E:U"}], "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (0.1.6).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-06389 — time 0.3.44 is affected by GHSA-r6v5-fh4h-64xc (CVE-2026-25727, RUSTSEC-2026-0009)

- Severity: **Info** · Classification: Known vulnerable component · Confidence: Medium
> **Analyst review (QSI review, 2026-10-28): not applicable to this code.** time 0.3.44's stack-exhaustion issue is in the RFC 2822 and RFC 3339 parsing entry points (time::Date::parse, time::OffsetDateTime::parse and friends). time is pulled in by the workspace's own util crate, which uses it for datetime formatting in util/src/datetime.rs, not for parsing attacker-supplied strings, and no audited file names the affected functions.
- Affected asset: `dependency:crates.io/time@0.3.44`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-29 05:31 UTC
- Priority score: 35.2 / 100
- CVSS v3.1: not applicable

OSV.dev reports GHSA-r6v5-fh4h-64xc (CVE-2026-25727, RUSTSEC-2026-0009) for crates.io package time at version 0.3.44: time vulnerable to stack exhaustion Denial of Service attack. None of the affected functions (time::Date::parse, time::OffsetDateTime::parse, time::PrimitiveDateTime::parse, time::Time::parse, time::UtcDateTime::parse, time::UtcOffset::parse …) is named in the audited code: the advisory does not apply unless they are reached indirectly (traits, macros, other dependencies).

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-r6v5-fh4h-64xc
```

**Evidence.**

_tool_output · [OSV.dev GHSA-r6v5-fh4h-64xc](https://osv.dev/vulnerability/GHSA-r6v5-fh4h-64xc) · manifest · SHA-256 f9407c25f7cc6bacd2695a5be9ea893203cf87df27320f0289d5e50d5077d0d1_

```
{"id": "GHSA-r6v5-fh4h-64xc", "aliases": ["CVE-2026-25727", "RUSTSEC-2026-0009"], "modified": "2026-09-10T03:50:35.583241382Z", "summary": "time vulnerable to stack exhaustion Denial of Service attack", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:H/AT:N/PR:L/UI:A/VC:N/VI:N/VA:H/SC:N/SI:N/SA:H"}], "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (0.3.47).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-06386 — block-buffer 0.10.3 is affected by GHSA-qwgh-2vcv-g2f7

- Severity: **Info** · Classification: Known vulnerable component · Confidence: Low
> **Analyst review (QSI review, 2026-10-28): not applicable to this code.** block-buffer 0.10.3 reaches this tree through digest, so every hash in it (sha2, sha3, blake2, hmac, ripemd, the dalek curves) sits above it and the dependency really is there. But the advisory is that a panic leaves the inline buffer position corrupted, which only matters if the panic is caught and the same buffer is then reused. This is no_std firmware on Cortex-M: std::panic::catch_unwind does not exist in that build. Checked rather than assumed — of 30 catch_unwind occurrences in the repository, 26 are in external/vendor third-party crates and the 4 under src/ are all test code: a #[cfg(test)] mod in bitbox-executor/src/lib.rs, two TestingHal tests in bitbox02-rust/src/hww.rs and async_usb.rs, and the integration test bitbox-secp256k1/tests/context.rs. The precondition cannot occur on the device. _automated severity: Medium._
- Affected asset: `dependency:crates.io/block-buffer@0.10.3`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-29 05:31 UTC
- Priority score: 26.4 / 100
- CVSS v3.1: not applicable

OSV.dev reports GHSA-qwgh-2vcv-g2f7 for crates.io package block-buffer at version 0.10.3: block_buffer: panic corrupts inline buffer position. The advisory names no affected functions, so reachability was not determined.

**Potential impact.** Depends on whether the vulnerable code path is reachable in your application.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-qwgh-2vcv-g2f7
```

**Evidence.**

_tool_output · [OSV.dev GHSA-qwgh-2vcv-g2f7](https://osv.dev/vulnerability/GHSA-qwgh-2vcv-g2f7) · manifest · SHA-256 ac22c9ee6301d8c1e4b09ca6951303d71527ccba2df30c96af92531d8efbb71e_

```
{"id": "GHSA-qwgh-2vcv-g2f7", "aliases": [], "modified": "2026-08-19T19:30:06.686866977Z", "summary": "block_buffer: panic corrupts inline buffer position", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:L/VI:L/VA:N/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Upgrade to a fixed version (none published yet; see the advisory for mitigations).

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-06384 — anyhow 1.0.31 is affected by RUSTSEC-2026-0190 (no severity rating)

- Severity: **Info** · Classification: Known vulnerable component · Confidence: Low
> **Analyst review (QSI review, 2026-10-28): not applicable to this code.** anyhow 1.0.31 (unsoundness in Error::downcast_mut) enters only through prost-derive, which is a proc-macro crate, so it runs in the code generator at build time and is never linked into the firmware image. Traced in src/rust/Cargo.lock: anyhow <- prost-derive <- prost <- bitbox-proto <- bitbox02-rust <- bitbox02-rust-c. Error::downcast_mut is not called anywhere in the audited tree. _automated severity: Low._
- Affected asset: `dependency:crates.io/anyhow@1.0.31`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-29 05:31 UTC
- Priority score: 20.9 / 100
- CVSS v3.1: not applicable

OSV.dev reports RUSTSEC-2026-0190 for crates.io package anyhow at version 1.0.31: Unsoundness in `Error::downcast_mut()`. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. The audited code does not name the affected functions (anyhow::Error::downcast_mut); anyhow comes in through other dependencies, which may still call them.

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0190
```

**Evidence.**

_tool_output · [OSV.dev RUSTSEC-2026-0190](https://osv.dev/vulnerability/RUSTSEC-2026-0190) · manifest · SHA-256 12d4b3eeb5a7dc67549bc112051813542621c4c3bb2d3ddfb353886e687f8013_

```
{"id": "RUSTSEC-2026-0190", "aliases": [], "modified": "2026-06-29T14:15:03.650725453Z", "summary": "Unsoundness in `Error::downcast_mut()`", "severity": null, "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability is judged from names, not a call graph: the affected functions the advisory lists against the identifiers in the audited product code, a Cargo feature it says is off by default against the audited manifests, the platforms it lists against the declared Rust targets. Indirect calls (traits, macros, other dependencies) are not followed.

**Recommendation.** Triage the advisory; upgrade to a fixed version (1.0.103) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-06383 — No post-quantum capable cryptographic library detected

- Severity: **Info** · Classification: Insufficient data · Confidence: Medium
> **Analyst review (QSI review, 2026-10-28): confirmed by the analyst.** Accurate and the single most quotable row for a migration budget: across 40 dependency manifests the tree declares curve25519-dalek, ecdsa, ed25519-dalek, p256, secp256k1 and x25519-dalek, and nothing PQC-capable. On a Cortex-M target that is not an oversight — ML-DSA and SLH-DSA signature and key sizes are the constraint, and a no_std PQ implementation that fits the flash and RAM budget is itself the engineering problem. Worth stating as a finding precisely because the fix is not "add a crate".
- Affected asset: `dependencies`
- Data source: dependency manifests
- Detection method: Dependency name matching.
- Analyzer: dependencies 1.2.0 · 2026-10-29 05:31 UTC
- Priority score: 15.0 / 100
- CVSS v3.1: not applicable

Across 40 dependency manifests, QSI found crypto libraries (curve25519-dalek, ecdsa, ed25519-dalek, p256, secp256k1, x25519-dalek) but none from its PQC-capable list.

**Potential impact.** Readiness indicator only: PQC support may come from the platform (OpenSSL, OS, cloud KMS) rather than application dependencies.

**Reproduction steps.**

```
Review the dependency manifests listed in the evidence.
```

**Evidence.**

_dependency · src/rust/Cargo.lock, src/rust/Cargo.toml, src/rust/bins/bitbox03-boot0/Cargo.toml, src/rust/bins/bitbox03-boot1/Cargo.toml, src/rust/bins/bitbox03-factorysetup/Cargo.toml, src/rust/bins/bitbox03-firmware/Cargo.toml, src/rust/bitbox-aes/Cargo.toml, src/rust/bitbox-board-stm32u5a9j-dk/Cargo.toml, src/rust/bitbox-board-stm32u5a9j-dk-build/Cargo.toml, src/rust/bitbox-board-stm32u5a9j-dk-sys/Cargo.toml, src/rust/bitbox-boot-utils/Cargo.toml, src/rust/bitbox-bytequeue/Cargo.toml, src/rust/bitbox-core- · SHA-256 bf8c520f29fbbee5a6f56af359cab24476ceec5fc694f1dd615a03d9b2a066fd_

```
Crypto libraries: curve25519-dalek, ecdsa, ed25519-dalek, p256, secp256k1, x25519-dalek
```

**Limitations of the check.** Absence of evidence is not evidence of absence: system libraries and transitive dependencies may not be listed.

**Recommendation.** Confirm where PQC support will come from (TLS terminator, KMS/HSM, library upgrade).

**Retest procedure.** Re-scan after upgrades.

### QSI-2026-06385 — bare-metal 0.2.5: informational advisory RUSTSEC-2026-0110 (unmaintained)

- Severity: **Info** · Classification: Improvement recommendation · Confidence: Low
> **Analyst review (QSI review, 2026-10-28): not applicable to this code.** bare-metal 0.2.5 is flagged as deprecated, not vulnerable; the advisory reports no defect. Recording the decision to keep it, which is what an informational advisory asks for. It is relevant to post-quantum readiness only in the weak sense that an unmaintained crate will not gain PQ support, and this one carries no cryptography at all.
- Affected asset: `dependency:crates.io/bare-metal@0.2.5`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.2.0 · 2026-10-29 05:31 UTC
- Priority score: 11.8 / 100
- CVSS v3.1: not applicable

OSV.dev lists RUSTSEC-2026-0110 for crates.io package bare-metal at version 0.2.5 as informational (unmaintained): bare-metal is deprecated. It reports no vulnerability; an unmaintained package will not receive fixes for future ones.

**Potential impact.** No known vulnerability. Future security fixes may not be released.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0110
```

**Evidence.**

_tool_output · [OSV.dev RUSTSEC-2026-0110](https://osv.dev/vulnerability/RUSTSEC-2026-0110) · manifest · SHA-256 1377cbc63847011c54324d486e3a7bae12ccbda6c1c9a981451db3532783f3c2_

```
{"id": "RUSTSEC-2026-0110", "aliases": [], "modified": "2026-04-24T09:45:08.136572Z", "summary": "bare-metal is deprecated", "severity": null, "declared_in_manifest": false}
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

### Post-quantum maturity: Level 0 of 4 — no post-quantum cryptography

- Classical only — channel key exchange (TLS, Noise, handshakes): X25519 (3 file(s))
- Classical only — key wrapping and data encryption at rest: X25519 (1 file(s))
- Classical only — firmware and boot verification (root of trust): ECDSA (3 file(s))

**Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

_Levels: 0 none; 1 present, not wired; 2 in use outside the critical paths; 3 hybrid in a critical path; 4 post-quantum by default in the critical paths (root of trust, key wrapping, channel key exchange). Judged from code and manifests._

### What the quantum-vulnerable algorithms do

| Role | Algorithms (files) | ID | First step |
|---|---|---|---|
| **firmware and boot verification (root of trust)** | ECDSA (3) | QSI-2026-06373 | Plan a hybrid firmware signature (the classical one plus ML-DSA or SLH-DSA, both required) and the path to ship the new keys in a bootloader update |
| **key wrapping and data encryption at rest** | X25519 (1) | QSI-2026-06379 | Wrap keys with ML-KEM or a hybrid KEM (X25519 + ML-KEM-768) and re-wrap the stored keys; data that may already have been copied needs its own assessment |
| **channel key exchange (TLS, Noise, handshakes)** | X25519 (3) | QSI-2026-06375 | Move the handshake to a hybrid key exchange (X25519MLKEM768 in TLS 1.3; a hybrid KEM in Noise-based protocols) |
| **transaction and message signing** | ECDSA (53), Schnorr (BIP-340) (9), Ed25519 (4) | QSI-2026-06376, QSI-2026-06377, QSI-2026-06381, QSI-2026-06382 | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains adopt them |
| **role not determined** | ECDSA (6), ECDH (1), Ed25519 (1) | QSI-2026-06374, QSI-2026-06378, QSI-2026-06380 | Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it; introduce an abstraction layer for crypto-agility |

_Roles are judged from file paths, function names and the code around each match; review confirms them. Root-of-trust keys and wrapped keys come first: they are hard to replace or can be recorded today._
No readiness questionnaire was completed for this project.

### Quantum algorithms relevant to this inventory

| Quantum algorithm | Effect | Attack model | Inventoried algorithms (rows) | What it means for this audit |
|---|---|---|---|---|
| Shor's algorithm — elliptic-curve discrete logarithms | breaks | Q1 | ECDH (2), ECDSA (73), Ed25519 (3), Schnorr (BIP-340) (7), X25519 (5) | Elliptic-curve keys are expected to fall before RSA keys of comparable classical strength. On blockchains, coins whose public key is already on chain (reused addresses, pay-to-public-key and Taproot outputs) are exposed first; plan the move to post-quantum signatures and avoid key reuse in the meantime. |
| Grover's algorithm — key search and preimages | weakens (larger keys restore the margin) | Q1 | ChaCha20-Poly1305 (2), HKDF (1), HMAC (9), Keccak-256 (4), RIPEMD-160 (1), SHA-2 (19) | Not a break. 256-bit keys (AES-256, ChaCha20) keep a comfortable margin; AES-128 meets NIST category 1, while some authorities ask for 256-bit keys in quantum-resistant contexts (see the AES-128 entry). Prefer 256-bit keys for long-lived data; 256-bit hashes need no change for preimage resistance. |
| Brassard–Høyer–Tapp — collision search | weakens (larger keys restore the margin) | Q1 | Keccak-256 (4), RIPEMD-160 (1), SHA-2 (19) | 256-bit hashes (SHA-256, SHA3-256) remain adequate for collision resistance; 160-bit hashes are already weak classically (SHA-1 collisions are practical). Use 384/512-bit hashes where NIST categories 4–5 are required. |

_Effects: breaks — replace the algorithm; weakens — larger keys or outputs restore the margin; included in standard parameters — no action at standard parameter sets; only with superposition queries — not applicable to ordinary deployments._


## 9. Limitations and assumptions

- This report presents automated and documented analysis results for the stated scope. It is not a legal opinion, a certification or an attestation of compliance with any standard.
- z is a planning assumption chosen per risk profile, not a prediction. A cryptographically relevant quantum computer is not publicly known to exist today.

## 10. Remediation plan / Priorities for 30, 60 and 90 days

### 30 days

| Priority | ID | Action | Type | Closure criteria |
|---|---|---|---|---|
| P2 | QSI-2026-06388 | Upgrade keccak to a fixed version (0.1.6). | root-cause fix | Dependency scan no longer reports GHSA-3288-p39f-rqpv (RUSTSEC-2026-0012). |
| P2 | QSI-2026-06389 | Upgrade time to a fixed version (0.3.47). | root-cause fix | Dependency scan no longer reports GHSA-r6v5-fh4h-64xc (CVE-2026-25727, RUSTSEC-2026-0009). |
| P2 | QSI-2026-06386 | Upgrade block-buffer to a fixed version (none published yet; see the advisory for mitigations). | root-cause fix | Dependency scan no longer reports GHSA-qwgh-2vcv-g2f7. |
### 60 days

| Priority | ID | Action | Type | Closure criteria |
|---|---|---|---|---|
| P3 | QSI-2026-06387 | Triage RUSTSEC-2026-0387; upgrade crypto-bigint to a fixed version (0.7.6) if it applies. | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0387, or the triage is recorded. |
| P3 | QSI-2026-06384 | Triage RUSTSEC-2026-0190; upgrade anyhow to a fixed version (1.0.103) if it applies. | root-cause fix | Dependency scan no longer reports RUSTSEC-2026-0190, or the triage is recorded. |
### 90 days

| Priority | ID | Action | Type | Closure criteria |
|---|---|---|---|---|
| P3 | QSI-2026-06382 | Add ECDSA, Ed25519, Schnorr (BIP-340) usages at the wallet's transaction signing to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-06373 | Add ECDSA usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-06379 | Add X25519 usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-06375 | Add X25519 usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-06376 | Add ECDSA usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-06377 | Add Schnorr (BIP-340) usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-06381 | Add Ed25519 usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-06374 | Add ECDSA usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-06378 | Add ECDH usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-06380 | Add Ed25519 usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P4 | QSI-2026-06382 | Plan migration of ECDSA, Ed25519, Schnorr (BIP-340) to ? (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ? or a hybrid scheme in use. |
| P4 | QSI-2026-06373 | Plan migration of ECDSA to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-06379 | Plan migration of X25519 to Hybrid key establishment with ML-KEM (FIPS 203), e.g. X25519MLKEM768 in TLS 1.3 or mlkem768x25519-sha256 in SSH (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows Hybrid key establishment with ML-KEM (FIPS 203), e.g. X25519MLKEM768 in TLS 1.3 or mlkem768x25519-sha256 in SSH or a hybrid scheme in use. |
| P4 | QSI-2026-06375 | Plan migration of X25519 to Hybrid key establishment with ML-KEM (FIPS 203), e.g. X25519MLKEM768 in TLS 1.3 or mlkem768x25519-sha256 in SSH (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows Hybrid key establishment with ML-KEM (FIPS 203), e.g. X25519MLKEM768 in TLS 1.3 or mlkem768x25519-sha256 in SSH or a hybrid scheme in use. |
| P4 | QSI-2026-06376 | Plan migration of ECDSA to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-06377 | Plan migration of Schnorr (BIP-340) to  (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows  or a hybrid scheme in use. |
| P4 | QSI-2026-06381 | Plan migration of Ed25519 to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-06374 | Plan migration of ECDSA to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-06378 | Plan migration of ECDH to Hybrid key establishment with ML-KEM (FIPS 203), e.g. X25519MLKEM768 in TLS 1.3 or mlkem768x25519-sha256 in SSH (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows Hybrid key establishment with ML-KEM (FIPS 203), e.g. X25519MLKEM768 in TLS 1.3 or mlkem768x25519-sha256 in SSH or a hybrid scheme in use. |
| P4 | QSI-2026-06380 | Plan migration of Ed25519 to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-06385 | Replace bare-metal with a maintained alternative or record why it stays. | root-cause fix | bare-metal replaced, or the decision recorded. |

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
17. NIST IR 8547 — Transition to Post-Quantum Cryptography Standards — NIST. <https://csrc.nist.gov/pubs/ir/8547/ipd> (initial public draft (November 2024); proposes deprecating quantum-vulnerable public-key algorithms after 2030 and disallowing them after 2035 — dates may change in the final version)
18. NIST — Post-Quantum Cryptography Standardization: Evaluation Criteria, Security (Call for Proposals, Section 4.A.5) — NIST. <https://csrc.nist.gov/Projects/Post-Quantum-Cryptography/Post-Quantum-Cryptography-Standardization/Evaluation-Criteria/Security-(Evaluation-Criteria)> (security categories: AES-128 key search 2^170/MAXDEPTH quantum gates, AES-192 2^233/MAXDEPTH, AES-256 2^298/MAXDEPTH; MAXDEPTH 2^40–2^96)
19. OSV advisory GHSA-3288-p39f-rqpv — OSV.dev. <https://osv.dev/vulnerability/GHSA-3288-p39f-rqpv> (modified 2026-09-10T03:50:59.332505686Z)
20. OSV advisory GHSA-qwgh-2vcv-g2f7 — OSV.dev. <https://osv.dev/vulnerability/GHSA-qwgh-2vcv-g2f7> (modified 2026-08-19T19:30:06.686866977Z)
21. OSV advisory GHSA-r6v5-fh4h-64xc — OSV.dev. <https://osv.dev/vulnerability/GHSA-r6v5-fh4h-64xc> (modified 2026-09-10T03:50:35.583241382Z)
22. OSV advisory RUSTSEC-2026-0110 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0110> (modified 2026-04-24T09:45:08.136572Z)
23. OSV advisory RUSTSEC-2026-0190 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0190> (modified 2026-06-29T14:15:03.650725453Z)
24. OSV advisory RUSTSEC-2026-0387 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0387> (modified 2026-10-24T03:45:02.365137418Z)
25. P. W. Shor — Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms on a Quantum Computer (SIAM J. Comput., 1997) — SIAM. <https://doi.org/10.1137/S0097539795293172> (peer-reviewed article)
26. R. Babbush et al. — Securing Elliptic Curve Cryptocurrencies against Quantum Vulnerabilities: Resource Estimates and Mitigations (arXiv:2603.28846) — arXiv. <https://arxiv.org/abs/2603.28846> (preprint (2026-03-30, v2 2026-04-15): 256-bit ECDLP with < 1200 logical qubits and < 90 M Toffoli gates (or < 1450 and < 70 M); < 500,000 physical qubits at 10^-3 error, minutes)
27. S. Jaques, M. Naehrig, M. Roetteler, F. Virdia — Implementing Grover oracles for quantum key search on AES and LowMC (EUROCRYPT 2020; arXiv:1910.01700) — Springer / arXiv. <https://arxiv.org/abs/1910.01700> (peer-reviewed article: lower cost estimates for the AES key searches that define the NIST categories)

## Appendices: Cryptographic inventory

| Algorithm | Parameter | Library | Quantum status | Classical status | Count | Locations | Examples |
|---|---|---|---|---|---|---|---|
| RIPEMD-160 | RIPEMD-160 |  | weak classically | legacy | 1 | 1 | src/rust/bitbox02-rust/src/hww/api/bitcoin/policies.rs:51 |
| ChaCha20-Poly1305 | ChaCha20-Poly1305 |  | reduced margin (Grover), approved | acceptable | 2 | 2 | src/rust/bitbox-noise/src/noise_xx.rs:9; src/rust/bitbox02-rust/src/hww/api/bitboxsync.rs:549 |
| HKDF |  |  | reduced margin (Grover), approved | acceptable | 1 | 1 | src/rust/bitbox02-rust/src/hww/api/bitboxsync.rs:12 |
| HMAC |  |  | reduced margin (Grover), approved | acceptable | 8 | 8 | src/rust/bitbox-aes/src/lib.rs:10; src/rust/bitbox-platform-host/src/securechip.rs:94; src/rust/bitbox-securechip/src/optiga.rs:175 |
| HMAC | HMAC-SHA-256 |  | reduced margin (Grover), approved | acceptable | 1 | 1 | src/rust/bitbox02/src/securechip/imp_fake.rs:16 |
| SHA-2 | SHA-512 |  | reduced margin (Grover), approved | acceptable | 1 | 1 | src/rust/bitbox02-rust/src/keystore/ed25519.rs:85 |
| Keccak-256 | Keccak-256 |  | Grover: acceptable to NIST, below ECCG/ANSSI guidance | acceptable | 4 | 4 | src/rust/bitbox02-rust/src/hww/api/ethereum/address.rs:17; src/rust/bitbox02-rust/src/hww/api/ethereum/sighash.rs:3; src/rust/bitbox02-rust/src/hww/api/ethereum/sign_typed_msg.rs:274 |
| SHA-2 | SHA-256 |  | Grover: acceptable to NIST, below ECCG/ANSSI guidance | acceptable | 18 | 18 | src/rust/bitbox-core-utils/src/random.rs:28; src/rust/bitbox-core-utils/src/salt.rs:22; src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/modules/generator/main_impl.h:27 |
| Crypto library | 0.13.2 | p256 (RustCrypto elliptic curves) | n/a | acceptable | 2 | 2 | src/rust/Cargo.lock; src/rust/util/Cargo.toml |
| Crypto library | 0.16.9 | ecdsa (python-ecdsa) | n/a | acceptable | 1 | 1 | src/rust/Cargo.lock |
| Crypto library | 0.29.0 | secp256k1 (secp256k1 bindings) | n/a | acceptable | 1 | 1 | src/rust/Cargo.lock |
| Crypto library | 2.0.0 | x25519-dalek (ed25519-dalek) | n/a | acceptable | 3 | 3 | src/rust/Cargo.lock; src/rust/bitbox-noise/Cargo.toml; src/rust/bitbox02-rust/Cargo.toml |
| Crypto library | 2.1.1 | ed25519-dalek (ed25519-dalek) | n/a | acceptable | 2 | 2 | src/rust/Cargo.lock; src/rust/bitbox02-rust/Cargo.toml |
| Crypto library | 4.1.3 | curve25519-dalek (ed25519-dalek) | n/a | acceptable | 1 | 1 | src/rust/Cargo.lock |
| ECDH |  |  | vulnerable (Shor) | acceptable | 2 | 2 | src/rust/bitbox-secp256k1/depend/secp256k1-zkp/include/secp256k1_ecdh.h; src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/bench.c:24 |
| ECDSA | secp256k1 |  | vulnerable (Shor) | acceptable | 52 | 52 | messages/btc.proto:4; messages/eth.proto:4; src/rust/bitbox-secp256k1/build.rs:6 |
| ECDSA |  |  | vulnerable (Shor) | acceptable | 20 | 20 | src/bootloader/bootloader.c:537; src/bootloader/stage0/stage1_sigcheck.c:165; src/i2c_ecc.c |
| ECDSA | P-256 |  | vulnerable (Shor) | acceptable | 1 | 1 | src/rust/util/src/p256.rs:28 |
| Ed25519 | BIP32-Ed25519 |  | vulnerable (Shor) | acceptable | 1 | 1 | messages/cardano.proto:4 |
| Ed25519 | Ed25519 |  | vulnerable (Shor) | acceptable | 2 | 2 | src/rust/bitbox02-rust/src/hww/api/bitboxsync.rs:11; src/rust/bitbox02-rust/src/keystore/ed25519.rs:10 |
| Schnorr (BIP-340) | secp256k1, Taproot |  | vulnerable (Shor) | acceptable | 1 | 1 | messages/btc.proto:4 |
| Schnorr (BIP-340) |  |  | vulnerable (Shor) | acceptable | 6 | 6 | src/rust/bitbox-secp256k1/depend/secp256k1-zkp/include/secp256k1_schnorrsig.h:82; src/rust/bitbox-secp256k1/depend/secp256k1-zkp/include/secp256k1_schnorrsig_halfagg.h:43; src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/modules/musig/session_impl.h:621 |
| X25519 | X25519 |  | vulnerable (Shor) | acceptable | 5 | 5 | src/rust/bitbox-noise/src/lib.rs:16; src/rust/bitbox-noise/src/noise_xx.rs:8; src/rust/bitbox-noise/src/x25519.rs:49 |

_Long lists are grouped here; the full per-file list is in the JSON report, signed with the same key._

## Appendices: Input files

| File | Size | SHA-256 | Redactions |
|---|---|---|---|
| messages/antiklepto.proto | 284 | `89caa2946283a469e5c783b9dd886d99728a40dd36b0e6156abe83c025ec9f0c` | 0 |
| messages/backup.proto | 1713 | `4616978a3a2b14c4523d1823c1a2b48373bcf731e5e35ff59f48316ada556737` | 0 |
| messages/backup_commands.proto | 724 | `17a8e01da16b238061f256546900a21af5b3a5bbe150b39e5d519a360e459488` | 0 |
| messages/bitbox02_system.proto | 1509 | `5e3ff16c8571d177180788a164d64bfb61e0e94415307a1f5f861965839743b8` | 0 |
| messages/bitboxsync.proto | 1814 | `8d87a05e25ba6cfec7f68a878906677ed218d64f663f6a20b24724f0d38ec54f` | 0 |
| messages/bluetooth.proto | 705 | `d7944887f55ee5e5196e4c62ea60564ad2a94e9d47257e49d05dbf3c4e805a0e` | 0 |
| messages/btc.proto | 9302 | `6f2fe1d3b1663e2617fd9587e6ec21242d02140624c797f222db4f8a26701928` | 0 |
| messages/cardano.proto | 4114 | `8e11c3628cc98b02d5904edf3a4d21e0492bad53ad74c89009b086e5ff111523` | 0 |
| messages/common.proto | 870 | `369ca12555a7810d196055abb643594d0723c7807fd46e5cca8a4a4ae8421342` | 0 |
| messages/eth.proto | 5601 | `3e2422076d196a16b59f743651cb1d6beecd9dae5a183bfc0c813936d49642ff` | 0 |
| messages/hww.proto | 3047 | `1faae60899577cf627e7c54b319b34f883aa126393d94d0cc1b84471b12cbaae` | 0 |
| messages/keystore.proto | 1894 | `ed5c5d677e3c017c55d71ce274246a4cd55cc8a867b259eaa9be77f204bb45a7` | 0 |
| messages/mnemonic.proto | 282 | `9cd94eff3b2bdd7a9d60981db9f487d2104119088ff7a912a8536654d571024b` | 0 |
| messages/perform_attestation.proto | 436 | `632df1278569322d391e4648de139ddf81ca83b26b5d14a0b3f0818605c0d5d5` | 0 |
| messages/system.proto | 195 | `706284195da36379d9d511f54e0ecc6a910b8fa8fa8158a47459567129fde382` | 0 |
| src/atecc/atecc.c | 24952 | `b08f8a566a7090a9f9ca736145e9565a28add3f47c8572f3a3013d56551d7266` | 0 |
| src/atecc/atecc.h | 1332 | `fa90590d9c07db88f66b7714dd7e74603c2f5c228332228df162c9e3e1ce3af0` | 0 |
| src/bootloader/boot_args.h | 1954 | `4211ed331ec60a4cebd8a66a05bc924d06a1eaf6808d6247d96c5a495b57cd7f` | 0 |
| src/bootloader/bootloader.c | 36479 | `f168d61e94931ac4ebd646e1317716b95b7ceb6ad14a2642b08d46ef28fe4d6e` | 0 |
| src/bootloader/bootloader.h | 589 | `06c21dcaacb655508bf4cf0f7fce19c7b556c589717595a45fb348c1c3b81051` | 0 |
| src/bootloader/bootloader_format.c | 2480 | `a8d11e946c4155c4ad0bd9cde5c67e6bd7bb2677af3e2a14dae78252e1720c43` | 0 |
| src/bootloader/bootloader_format.h | 1521 | `201e9cc589180cef9de3abfce4b2e98139402faf6b99ebe9accf5a8313f1b583` | 0 |
| src/bootloader/bootloader_product.h | 1455 | `bc0884527d99033bc323721392226a690153d3f874fd573493e02a3d1db6c467` | 0 |
| src/bootloader/mpu_regions.c | 4998 | `ce6c37a9c92a7ef982192a5e7e1df86a4f147fca5c9f22735276606f4124f870` | 0 |
| src/bootloader/mpu_regions.h | 633 | `2e0d365b60c5f4af7308cc1a3bf726beabda6581ad8d989ad111b18062b66504` | 0 |
| src/bootloader/stage0/stage0.c | 21703 | `e7602bdbf3060508b511e757832adbe9a9995bc6dd13477ba481d8970abdbdeb` | 0 |
| src/bootloader/stage0/stage0_descriptor.c | 648 | `e466f37f5e5ab14d521c3bef5ca673a0d824a5dad24bf67b0616d4f7bb9e21a6` | 0 |
| src/bootloader/stage0/stage0_descriptor.h | 1483 | `9a5d822def8bdb79e9505ef0453bb8214024bc4667d893f4beecad143f650d5d` | 0 |
| src/bootloader/stage0/stage0_flash.h | 7485 | `923840cec8b59d2a0150b15a393a36ff4ca70547602a3769a1475073ae838c82` | 0 |
| src/bootloader/stage0/stage0_runtime.c | 1000 | `27538c86f302b07025f7be542832db5d2843e8fa6893bc523724968ad4486e31` | 0 |
| src/bootloader/stage0/stage0_startup.c | 1872 | `570ef28ad3f830c70d9713b0dbe9a2323172df00e1240964459cf0541a447881` | 0 |
| src/bootloader/stage0/stage1_sigcheck.c | 9311 | `5704d66ba1ca763bac3bd4e998eb68c26d63ddcc74c8912267a4d5cfecd9a083` | 0 |
| src/bootloader/stage0/stage1_sigcheck.h | 333 | `cd78c8accb34bfcc118cdf91425314a0a79cd67d91eeb560080cbdaecbb1a602` | 0 |
| src/bootloader/startup.c | 7383 | `0790af69af4ff3105e7b5be5f3107d14a66043b7ca893f402be9790b49b62a67` | 0 |
| src/bootloader_upgrade/bootloader_upgrade.h | 4938 | `5509b50fcadf1b81604abb566a2655e91ea46525627c4bede0ce55cf00629753` | 0 |
| src/bootloader_upgrade/firmware_installer.c | 6308 | `fbe4a58ce6c5ee5a49b10482f7cb082c5a5ab846d7cf4dfae408f3cf86689374` | 0 |
| src/bootloader_upgrade/firmware_installer.h | 198 | `db2fe193d39c09380b6cec28f9190146e837048cf3c9f7ff5473ecd2ca551bad` | 0 |
| src/bootloader_upgrade/firmware_installer_check.c | 3641 | `2ffa4ba9da129ca84ec2eb826fa2233378ea07bedd12e6188c32a22e7889a5b8` | 0 |
| src/bootloader_upgrade/firmware_installer_check.h | 626 | `e6b04cd3dba6479e1d4a52f0d018c75bfa28ec4a531cc5641b5804f8a6137df7` | 0 |
| src/bootloader_upgrade/stage1_pubkeys.c | 1453 | `d0dbfb66799b31c124d1d47a5536b3d0ee40afb323563a7f2104668ea43d5ec7` | 0 |
| src/bootloader_upgrade/stage1_pubkeys.h | 268 | `6861334872aa5690cb7d9c0f6fca8b2da3c0224ccb1f2e09c2898ef50a6cc4e1` | 0 |
| src/common_main.c | 2237 | `6a5a78f034fdb3ff90f6b29937b3f7370b75996d6f8599ae1f28d5426580b1ad` | 0 |
| src/common_main.h | 258 | `00c2607686f4b979a45b494dd6465be74028d95f3758fa9cdcccd3b4b4a09011` | 0 |
| src/compiler_util.h | 156 | `766b232901874eff32c3045b845cdbf8b7f26bede78a78e6ea66668b04bef762` | 0 |
| src/da14531/da14531.c | 148 | `0e137eb5f9ed0c6017372cebe6a13c665f179c73d7ee74c5281f6ea3d5b5ccd4` | 0 |
| src/da14531/da14531.h | 757 | `699f504277cca1dec2db35d3a729c3d2496af56bee2d715460a9cf8bca9007aa` | 0 |
| src/da14531/da14531_binary.h | 615 | `ab36b4d19ab2e92690987e13a9bb764070dc4fe1b37f582b13dfb1920dbd7378` | 0 |
| src/da14531/da14531_handler.c | 10934 | `470474701180c1c3a831ca43c73b3323456cc31f063eac2cc536b77fe5cd8a9c` | 0 |
| src/da14531/da14531_handler.h | 488 | `c4f4950fa1e7095bf80defffee2d29224512c369d4d42a51c3b37b7f7a9a0075` | 0 |
| src/da14531/da14531_protocol.c | 14092 | `fccf1437f23c480e2b2675366367ab4ce8d4f41ebef6584a5c729f14c0a32697` | 0 |
| src/da14531/da14531_protocol.h | 2026 | `b35f9a6a828becdd2ae5b9e93f8615982afd923518df14ee269d34d27493c248` | 0 |
| src/delay.c | 2214 | `d9b814da8a0b29b9316c7d4d9062aad566376b3f580111e44e62b572c218aaa7` | 0 |
| src/delay.h | 527 | `b181e4281855a1a7ee890769b72d7884157729456e11760b93319ea8065c54ff` | 0 |
| src/factorysetup.c | 40551 | `f23340c080fa71056e24109f64c2404ff90acf2b6bcc516e5daa267731c94e18` | 0 |
| src/firmware.c | 1346 | `e8c3cd856d1329684a6519d907dc516953a5da6260bb895cb8288986fa80058f` | 0 |
| src/flags.h | 4465 | `20b4d9f439ebac1783b6a6a9b58d3f44f5795a4da84148d9f7772c2d7234fa77` | 0 |
| src/hardfault.c | 1227 | `5d2a769cf3e77da97afcea5b416c9853b2c8db0db8bfb6c52a9de6345d16eea4` | 0 |
| src/hardfault.h | 858 | `5944df9738bce65d30ad8a83310a4ba489613bc075efd653c2807edd20232a12` | 0 |
| src/hww.c | 8090 | `a01aa7f5b50ae9766c9316cdfc8a4fea04f22202b5dfeec770bbb2042e3496f7` | 0 |
| src/hww.h | 1190 | `3dc95f986eab99ef6868410b64498f5af12e661ab68871c0c8c6f61912b85fd1` | 0 |
| src/i2c_ecc.c | 2276 | `ed06ab53c14f7911372708f60f040238decc514e7163c2decb99e8db658ffc96` | 0 |
| src/i2c_ecc.h | 1462 | `c36dd2e4b88288c1d4d5422884b2eaf273edc3973dc880ea06c30f3035a59496` | 0 |
| src/memory/bitbox02_smarteeprom.c | 4544 | `2d4869e79d0baa5614a11659bea610b382cf25f17fb5ba76683cacba93dc0eea` | 0 |
| src/memory/bitbox02_smarteeprom.h | 891 | `a014fb1fc58e11fcd563a9281dd3b992c0aa75385b54be6124ae950e85c32ad3` | 0 |
| src/memory/memory.c | 35229 | `10d47933c8921fb95a5c15b3e91291f273a5ace9f1ee9c98568bffc8c894820a` | 0 |
| src/memory/memory.h | 10717 | `f5f44c8b0780a106f193a012d03db97abf90230eed6b88491df8146610f95963` | 0 |
| src/memory/memory_shared.c | 8175 | `4b5997eff681a1063e56e689a03adae0a6edfa5ccddd5eb12f966c759096bb9f` | 0 |
| src/memory/memory_shared.h | 5977 | `b7c85bf18214d96b882c4e5ababf4bfe5194a8d29e3db15d9d07dbde50912f5b` | 0 |
| src/memory/memory_spi.c | 2980 | `5c7ec0943599eb710ab7d2b1681fa72fa2e7148ad26f1f2d73e90127682438e1` | 0 |
| src/memory/memory_spi.h | 1279 | `8810697f34c32b38045a4e398daf86d59353a28cb0b35a9bfe0bb39e4bf3b49a` | 0 |
| src/memory/mpu.c | 1183 | `428c3a5c05260bea2d6c8fd7a9648904c05ef48e756ce13d54ec8b2cc49a8919` | 0 |
| src/memory/mpu.h | 3189 | `e3e8eeaa6c7f657e82c8afbf80ee43af9268ac058bfe93c5bbe289012097de4c` | 0 |
| src/memory/nvmctrl.c | 383 | `51c13e773d9816fa9b3d8a4fb402ca07aec6d745072f4616c3c04a7dec09ad50` | 0 |
| src/memory/nvmctrl.h | 312 | `eb730b09fd1ba0120da5f956d8dfb4d2a39f5ca55f8660d8777dd1ab59717937` | 0 |
| src/memory/smarteeprom.c | 5033 | `28653e4583b809e72e8bb6104a23db25c6fa963dd12f0a4b7c9b142fa4d961e4` | 0 |
| src/memory/smarteeprom.h | 3092 | `eac71c154b3af713597f18c878aa2c2d2b72b43a811df1220b46710b27f07a42` | 0 |
| src/memory/spi_mem.c | 11033 | `9f2bba7727e4ee26a6e3c29b3108259feb98bce5515d8397ff9dff907ba179d8` | 0 |
| src/memory/spi_mem.h | 3912 | `032202c6f683a3a269ceba9e51ad78d9b11bd12924eb29b765caf3ea09fc62c2` | 0 |
| src/optiga/optiga.c | 36862 | `d81c6f4b45d9923458bf7b218170acfaf729a6d36876d9bea34b848e03c6a54f` | 0 |
| src/optiga/optiga.h | 4906 | `d992cdf0cda34979f1a75dbca2c1307f5aaf6fded168246fe36a9e771bdcad96` | 0 |
| src/optiga/optiga_ops.c | 5215 | `faeb33491aae26ecb601778ffad183100f4fd698bda52e9b1321d353b69b58ad` | 0 |
| src/optiga/optiga_ops.h | 1694 | `ab2ed1d32962652a76c14fc95fd58b1ad24d273d3a692a896d2cd23ab4a8055a` | 0 |
| src/optiga/pal/pal.c | 1558 | `3769a1635f88870578cbd926257df76749f1b9774f78bcf82569fab8efe527a7` | 0 |
| src/optiga/pal/pal_gpio.c | 1979 | `89e0f438ddc439ed69d259aa4f760fe92f41f2f5751fcd1b570b21a31d00912e` | 0 |
| src/optiga/pal/pal_i2c.c | 11391 | `8e9c342201674cdb6241e0b3fd9dfc7efa17100944b49c8660fff0dec82071fa` | 0 |
| src/optiga/pal/pal_ifx_i2c_config.c | 2906 | `e4ff9782e587b6fb265086c5dace6a2ae8d2d15709d7a79dcd085ca48e731303` | 0 |
| src/optiga/pal/pal_logger.c | 2858 | `ed4810ab3dbb786ec7cd1902053f342869822b9ff765497cd256ff1887a73de3` | 0 |
| src/optiga/pal/pal_os_datastore.c | 2763 | `178127d32e56421ee047b0cc0e6ee0afa935fa85c717c7da6cdf1c8fa2306195` | 0 |
| src/optiga/pal/pal_os_event.c | 3355 | `245c5a1d4c696fdbb90764e6b2b5b8dd59fd531929e856f3a57b2916eadf6ae0` | 0 |
| src/optiga/pal/pal_os_lock.c | 2603 | `71ffab63bbf2f395b09df0a1b198a6d418473d35b06263f64639816eefb08709` | 0 |
| src/optiga/pal/pal_os_memory.c | 470 | `7b29109eb25ffa9f501f444ac0e7675a8e9cea8068a395a6b85ef59864105eff` | 0 |
| src/optiga/pal/pal_os_timer.c | 2550 | `ecf6f183c7cb7b6c865f9e58ad392ebf6a69718c7faddceeceed0beeb8642b55` | 0 |
| src/pac_ext.h | 654 | `1b829db5cbc08b8d68626be28855dc5508bd39233aadb20cd5b347b39b84c0b3` | 0 |
| src/platform/bitbox02_pins.h | 1308 | `7b73cfee547ae31cadde79c3c727001b7f8268b132a446d7884bb78401ba9d70` | 0 |
| src/platform/driver_init.c | 13012 | `ce0ab53cd6fab718023fca835d52705f61e6b1b412d85fba33e74dec346e7189` | 0 |
| src/platform/driver_init.h | 2021 | `057862dc09feac0d0d67e191dd027d26cc0d91677b29838111b46140d1b1f745` | 0 |
| src/platform/platform_config.h | 1732 | `c6a8ff515fcf1c87f79c366b42870d3ad34b09adac5b02a4d6451b658b2b6374` | 0 |
| src/platform/platform_init.c | 2465 | `cc2d88ab9b7eee346288271974f1200f40ce6b33f233877990d1889a93961a6c` | 0 |
| src/platform/platform_init.h | 359 | `d4c05fefa903b6446086660da71863f44bc3baa11b76f7148caf14815c026123` | 0 |
| src/platform/sbrk.c | 1187 | `5552fa9172238701b473d3b0bfa0df1b1906e85037596958d12305850e73c8ad` | 0 |
| src/pukcc/curve_p256.c | 4832 | `f4aba16f4398bbf89102e62b826cefc8c02d3a4731a73387393d48a864a8b212` | 0 |
| src/pukcc/curve_p256.h | 211 | `c620f92a051fc37d6c4b976a72cadc61f24595dbfa1dfed6326dddcde19f1225` | 0 |
| src/pukcc/pukcc.c | 9798 | `b5049dd725362a4217e5797928ba8ad32e3c7235d029f366a411e38631151540` | 0 |
| src/pukcc/pukcc.h | 1169 | `a7650ddfd0bfe8a9c23dce685d1d648c412ea08b65c28f1403569071e88d5e74` | 0 |
| src/qtouch/qtouch.c | 28561 | `a3ce935421670987dcc50cbb7fa710d2e507fd5f5dff108a1c53ecbc3205da6c` | 0 |
| src/qtouch/qtouch.h | 10273 | `ece235d4e91d9b3b459490b835463f2c1e9a621ea7e327c42cc5c4eb0a917a86` | 0 |
| src/random.c | 2290 | `8e70d7c104bf78ace2348c526b5e4e12625ad8bb56b0938be2bcf88421054019` | 0 |
| src/random.h | 711 | `8c2bca629ef2ac0214138b7c3756b271540426323fb18c0a80b1d1a14ecfd64b` | 0 |
| src/reset.c | 648 | `817e226f032c6a0fc76fde0f4906ff0c6151f609bb4d6c38d4fc86bed4e074d0` | 0 |
| src/reset.h | 243 | `7050c993ba457968af7b3411d33e22754620c9aee2a8000305488e92ea3653fa` | 0 |
| src/rust/.cargo/config.toml | 1932 | `a6bddaebf210d9245b6e206167b95b578e86e14a44e8ebf6c588fd7ae3669b72` | 0 |
| src/rust/Cargo.lock | 37444 | `26c6fdf274b15f25b33b594f5adaae1be5d54998c1ab4584a91a53be681c323a` | 0 |
| src/rust/Cargo.toml | 4099 | `73bfb23592887b4a84691a76f5034f4c29830dbcfeff26eb17d8b6e5d9dbbce4` | 0 |
| src/rust/bins/bitbox03-boot0/Cargo.toml | 602 | `b45eb014db8ef2e7ac79a791989422bcfbae6bf8e6bd6254b37d887b5fae035e` | 0 |
| src/rust/bins/bitbox03-boot0/build.rs | 1188 | `ce807537a25ae8a54e4d07708b44fa86de7cd518bd820c4fd493cf05378d58ae` | 0 |
| src/rust/bins/bitbox03-boot0/src/main.rs | 1411 | `65d8b40c8876936d6b38e3fec8aa11fdc622c8a984a0ba697abe7bdc3f01d7c2` | 0 |
| src/rust/bins/bitbox03-boot1/Cargo.toml | 602 | `dd41d2262a5b31bb5233966eb1a761d326f1ceff70144a451f406eb427bcabaf` | 0 |
| src/rust/bins/bitbox03-boot1/build.rs | 2885 | `56d2bc01330a026f7ecca4fbdd782a6ab33a2f99e50a75cbae2f8f449b962151` | 0 |
| src/rust/bins/bitbox03-boot1/src/main.rs | 1452 | `5147e04dc133dc02a987c6d5fea26176da929eb8adbb89d36cd5786ad81a90e7` | 0 |
| src/rust/bins/bitbox03-factorysetup/Cargo.toml | 900 | `7e0ad6e8bdd8aae31eac633c9da465cbc325a4b27f587e3a6f320c75ffddc1de` | 0 |
| src/rust/bins/bitbox03-factorysetup/build.rs | 2285 | `d29edafa35af5298df345ada8e61b938812591fb73cf0655bb022b7375a20d9a` | 0 |
| src/rust/bins/bitbox03-factorysetup/src/main.rs | 3628 | `a253e1c4415b9ffd333355e274b1ec08c9cfa1adc0eb9af9cbb97d6cfafd589d` | 0 |
| src/rust/bins/bitbox03-firmware/Cargo.toml | 819 | `93fc8dab006fc6c5b9b5336b7ac129445d9a47a4aca353989674a928a3244ed1` | 0 |
| src/rust/bins/bitbox03-firmware/build.rs | 3198 | `a7109b841bc352e2af96fd651504faa5bb14d263843df3f99a3e177fe2e5d179` | 0 |
| src/rust/bins/bitbox03-firmware/src/main.rs | 556 | `e02dc06cc0918423fbc2fca5b373064fd2086c68ee174e9e7b41fb218f8e9860` | 0 |
| src/rust/bitbox-aes/Cargo.toml | 315 | `f8c0eda103f0f2a76ea59a2ee7469215f09951ef490a28b9bb1a1c478ea0dc1c` | 0 |
| src/rust/bitbox-aes/src/lib.rs | 189665 | `d1b6231d59cddb178fbde87ab0f9ab35fb8bdbdc5c1d197e8298dfb13f5f2394` | 0 |
| src/rust/bitbox-board-stm32u5a9j-dk/Cargo.toml | 497 | `b41260fdc41c8a6146e9325384c72c19e3eea5bf026ca13af9e370bb0f85e87c` | 0 |
| src/rust/bitbox-board-stm32u5a9j-dk/build.rs | 2484 | `342a59fec95ff796491f0382609d4885c17a70bd9c4ca4350cb5b7065cdd95c1` | 0 |
| src/rust/bitbox-board-stm32u5a9j-dk/src/lib.rs | 629 | `98780551b6e10d5bdb56bca266d7c84c7bd5b2f1ec9cfb4d985cab2383af6d04` | 0 |
| src/rust/bitbox-board-stm32u5a9j-dk/src/memory.rs | 4370 | `59076a19e7152ab2f5a5aab0d9005a31fdfa297bb68e03f37a18b32f32f22999` | 0 |
| src/rust/bitbox-board-stm32u5a9j-dk-build/Cargo.toml | 331 | `f3b43b17755cd35be3bb7cdc2a5a3f635864ba7a72098d51c0898bdeb1608477` | 0 |
| src/rust/bitbox-board-stm32u5a9j-dk-build/src/lib.rs | 2349 | `ef079b608145f4834765b3aea1cee1f7ab519853e1e9892f712d8b3fb2961721` | 0 |
| src/rust/bitbox-board-stm32u5a9j-dk-sys/Cargo.toml | 363 | `e86eece21be38507a20b4c38642399bf2e5d404343c0ad8ac8cf39708cc7644c` | 0 |
| src/rust/bitbox-board-stm32u5a9j-dk-sys/build.rs | 4573 | `94c13a1fdaf427adcdff8c386e2a44644c58c21ea8e7f2e7261fe8024b867922` | 0 |
| src/rust/bitbox-board-stm32u5a9j-dk-sys/src/lib.rs | 272 | `1b57158882a13471de4be80cc918e22e9628a33222e9d20fdd21b2cdedeb5d45` | 0 |
| src/rust/bitbox-board-stm32u5a9j-dk-sys/wrapper.h | 141 | `100e3781691854b92ceb38c0eb2f61f40f7da3c1245e7b158a6480dc670c0a5f` | 0 |
| src/rust/bitbox-boot-utils/Cargo.toml | 143 | `25690b5da7d4452621cd5ab17a91bea7ffe634075f88dc5a97bba49181347b6a` | 0 |
| src/rust/bitbox-boot-utils/src/image_header.rs | 3066 | `0a54aa9230fd76555626b278bfac1ea7a7a280d93ac20635a1efb26c11da3cf7` | 0 |
| src/rust/bitbox-boot-utils/src/lib.rs | 22385 | `517532d8b9006f867adb50754bcdbf773e43afb4fc7e90abfbbf0ace89ef9234` | 0 |
| src/rust/bitbox-bytequeue/Cargo.toml | 230 | `1b9256563d1f7b139b57c44e71673f17b4e6adf34023ebfddb15a93c839c0f7f` | 0 |
| src/rust/bitbox-bytequeue/src/lib.rs | 11527 | `a297010473f7b7f5043a2cead7181cccbc5dd5acf852059bd2ccaa55f7bb00ad` | 0 |
| src/rust/bitbox-core-utils/Cargo.toml | 535 | `ea9a88c066735da317bb3c937e841a12c93b005dc41cbff7647080dbefbfc1e0` | 0 |
| src/rust/bitbox-core-utils/src/lib.rs | 103 | `0096bd43bcfd4ce09e49a2e95943e5bf27f8f73611d08b61dcbd9f061f5ba220` | 0 |
| src/rust/bitbox-core-utils/src/random.rs | 4073 | `27fc4f4a389b1010b5ce0f37de67f00751724b1a9fdf83d10e2e601ab42a8b35` | 0 |
| src/rust/bitbox-core-utils/src/salt.rs | 1973 | `0a5be445ef7f2d5a2b1df43462fff5b4dd52b7a2e5cb6e5492ca6054f61cd035` | 0 |
| src/rust/bitbox-da14531/Cargo.toml | 401 | `dc7a28ec383a3eb83ecb0f364d10b1da99b32f8be098e990488693c4fa075e79` | 0 |
| src/rust/bitbox-da14531/src/lib.rs | 7209 | `ff8cb7cd0e1ee5290e86ce22f3629aec737ebde2ca1ca5cf87334d3886e717a4` | 0 |
| src/rust/bitbox-debug/Cargo.toml | 275 | `82ccb7a869fb1c4fcfa222bd5fa9e74389a268f45d746282a625bf40f4219a0a` | 0 |
| src/rust/bitbox-debug/src/lib.rs | 949 | `140a69f4d3b87b65e651e7af56f409c94b8db6324409636938c2444879bbf32c` | 0 |
| src/rust/bitbox-executor/Cargo.toml | 267 | `98befdb3a6d49e8b576b0ac2f21918db7f94b0d24620878be6e3c2674b81512a` | 0 |
| src/rust/bitbox-executor/src/lib.rs | 7140 | `facd59247f5511a85d021b99e248223d4c98ca45e97a89fd2824f900fe3b061a` | 0 |
| src/rust/bitbox-framed-serial-link/Cargo.toml | 360 | `0b715df72f2c74113151e0b699e79c6661e8f2091e0bb80434aab754a2ee4e3f` | 0 |
| src/rust/bitbox-framed-serial-link/src/lib.rs | 17048 | `c97d73bd553608be30463d109f86b23b0284e973c5ffdaadef961aadf00dcb31` | 0 |
| src/rust/bitbox-hal/Cargo.toml | 252 | `8e639839c006a38521fe6ef232ce70588f8b88a404f68bf0053526fad2d6dd6d` | 0 |
| src/rust/bitbox-hal/src/eeprom.rs | 1948 | `200715d25813eeb9d50c237a7c8d4a0861cf7de64d38f81b6fe0cff849389a93` | 0 |
| src/rust/bitbox-hal/src/lib.rs | 1913 | `456f9367a84f57322c65ae911c5e1aeb41c33c020343204d4b78db1d02a42e97` | 0 |
| src/rust/bitbox-hal/src/memory.rs | 4151 | `ed950634d4ebb11fa50c62f323f2dcd92901986820d8c0d769146e9f31f51d4e` | 0 |
| src/rust/bitbox-hal/src/random.rs | 172 | `3d53abdd13fc8d9c29b0534d41864d1f8fb97c9a04c38da2ad112fc391761b8a` | 0 |
| src/rust/bitbox-hal/src/sd.rs | 588 | `7a3c3a204b2985238560a1951307ae884f86f5c9c76e66391b0ad84981381306` | 0 |
| src/rust/bitbox-hal/src/securechip.rs | 4226 | `da71595a0cca42f468cb939ff2a6fbd9c62eed395caf4d4d16425a1f8d3bb36e` | 0 |
| src/rust/bitbox-hal/src/system.rs | 1019 | `6da346170863b3ba80e5d7ab3e456fa322d94d0a36ab1e1a1769ceb3cfd87771` | 0 |
| src/rust/bitbox-hal/src/timer.rs | 159 | `ab7bfc9e02e33d3b86168f606ced6332ea33d39b5503fae655b11cae2a52dfd9` | 0 |
| src/rust/bitbox-hal/src/ui.rs | 8042 | `bc9fb5c0d36d1a1e879cd4d02e116998272c37f1e537d48eb6a505d20946f1b7` | 0 |
| src/rust/bitbox-lvgl/Cargo.toml | 268 | `daefc6d741706e60098419b9ec4d5b2ceb5a3de23878b9bc7206085aaa9cf3bb` | 0 |
| src/rust/bitbox-lvgl/src/color.rs | 473 | `71d7bea77d1589672a954ef696f73db64bb36192eae7d0f37898c13d04bfe829` | 0 |
| src/rust/bitbox-lvgl/src/display.rs | 5374 | `916b3d2e5a95aea091b5f9368115cc017ce770ed6c7f2e1fd2f001651822469e` | 0 |
| src/rust/bitbox-lvgl/src/font.rs | 1900 | `5f87b8d677c62d374ffe1c4d4c557abcec777306bcf8e8c877840fe449ea9d8c` | 0 |
| src/rust/bitbox-lvgl/src/indev.rs | 2037 | `bbf58a031fdbf5b41ef0f9b6616b54a24891ed27481c92a9b41d6d59f24bccfd` | 0 |
| src/rust/bitbox-lvgl/src/lib.rs | 3486 | `7b69d1adbd4abb46f93f8ab9312bf857383eb1f18acf73e3116216070dbfa9de` | 0 |
| src/rust/bitbox-lvgl/src/log.rs | 985 | `fe230bbebb5892fa4ea4fa3d6f3fe7b0034bf21fd318a2265db03267b814dc7d` | 0 |
| src/rust/bitbox-lvgl/src/style.rs | 3816 | `6db64a1617b4f2647ec3d2c6de756f7a027b773a27bd7d92f2778779ce8b30b4` | 0 |
| src/rust/bitbox-lvgl/src/system.rs | 105 | `ffd20d867f7d4328e68d59f135e9134ca691dd5851cd271a609b6c96b6e02036` | 0 |
| src/rust/bitbox-lvgl/src/tick.rs | 157 | `ad20354b120701fbd19ef4be25425cdc219eeb71e5951ea0c0ab28de87a8ee89` | 0 |
| src/rust/bitbox-lvgl/src/timer.rs | 130 | `3eabc6b60fd7223fbef597a37088779ffda143d1bc6985f3918f280ce5c78e3b` | 0 |
| src/rust/bitbox-lvgl/src/util.rs | 1312 | `f3f9f97063188336dd790b1aba5c0b085020096af6a57711c0401ae575eae491` | 0 |
| src/rust/bitbox-lvgl/src/widgets/arc.rs | 3409 | `0a116c3cc38d71e7fb015b929fe518a3dcbd44e7bf0d046390c0fb67f7fc2238` | 0 |
| src/rust/bitbox-lvgl/src/widgets/bar.rs | 2207 | `1684518d5e6da6338ef0df80538b98941221ecb55002d737b76a4eb2e1532a07` | 0 |
| src/rust/bitbox-lvgl/src/widgets/button.rs | 521 | `3f8a2ac68192d05fc1539694ab44e2f6f8b28c6fc72bb1d2b757474ddde8083c` | 0 |
| src/rust/bitbox-lvgl/src/widgets/buttonmatrix.rs | 6488 | `5024d703f760384f238652d387ded9200aa1baebce14e48d5c0848e441538121` | 0 |
| src/rust/bitbox-lvgl/src/widgets/canvas.rs | 4115 | `a5b70aa02b2edb1924c0945b781853a9172f0ba1f18a66dc830d2eb838896c62` | 0 |
| src/rust/bitbox-lvgl/src/widgets/class.rs | 2361 | `efa9537454a60a2d4db805c8139483aee33a8fd71e7a1a9d3dc59d035a8310f8` | 0 |
| src/rust/bitbox-lvgl/src/widgets/image.rs | 3280 | `fd27b5b532c89fea4ad00cd82e0aad8551b4b8720565d3e09a0a32047a640faa` | 0 |
| src/rust/bitbox-lvgl/src/widgets/keyboard.rs | 4508 | `267840305dfce7dd03cee5bbd73c66b2c0acf6484fbd6937ab9719baaf7e5ea7` | 0 |
| src/rust/bitbox-lvgl/src/widgets/label.rs | 3497 | `9c01936e4c2ffea788935298186fa3165630ec5d5d7993cb1aad1ef9a3220cd6` | 0 |
| src/rust/bitbox-lvgl/src/widgets/line.rs | 2822 | `65f099ad38111fdbd0092cea34299168ef3886c47f10a94569fd887db9a28f84` | 0 |
| src/rust/bitbox-lvgl/src/widgets/mod.rs | 2567 | `4a1f2a556ae514d9a87b742134f675d8f8fa041a1a832699c434a5419425e335` | 0 |
| src/rust/bitbox-lvgl/src/widgets/obj.rs | 26478 | `986a3fb1a9bd5628a7428f9feb7f6d9c2b0aa2436ac7e25ca5fbba866f0ba007` | 0 |
| src/rust/bitbox-lvgl/src/widgets/slider.rs | 2700 | `7ff614b820dbb41728c77822445f8d9acabf0eb2405fdbc54c13ca5a10bfcf2c` | 0 |
| src/rust/bitbox-lvgl/src/widgets/span.rs | 18294 | `d53070663d6ebff5243cbffc2a73460492fd4d5e6465a7a09947974fbe263f6e` | 0 |
| src/rust/bitbox-lvgl/src/widgets/spinner.rs | 774 | `c3f69a2baf9c498ba1574b2133fb1a10fc3f66e01ca0efe6735f214d7f70b896` | 0 |
| src/rust/bitbox-lvgl/src/widgets/textarea.rs | 6641 | `c0a550e929d8ef527d767c582394858c4d0a3a9eeb1b3182a4298ab68ebc2658` | 0 |
| src/rust/bitbox-lvgl/src/widgets/util.rs | 3599 | `64c737a005a0aba480725702fe5539a2fbfd92ad419678a82bfd03ef3219e715` | 0 |
| src/rust/bitbox-lvgl-sys/Cargo.toml | 248 | `389cb4c1c28f0ccc4a422025b75061db160cc8fdbfb68b51f77fd00e1bba91be` | 0 |
| src/rust/bitbox-lvgl-sys/build.rs | 9866 | `d28e575ad9baa893bce904d3b2b74b2db3fb600a1b4ee36f6a911c7040bf7366` | 0 |
| src/rust/bitbox-lvgl-sys/lv_conf.h | 51220 | `5a13d194e9d7013099caf89cea5091b78ff16a22b9c9ea928f7276c1f35bf7d1` | 0 |
| src/rust/bitbox-lvgl-sys/src/lib.rs | 341 | `fcab8b13940551094a4a7a4fe477bc6186711f50e0dfa2026dfab7013858f313` | 0 |
| src/rust/bitbox-lvgl-sys/wrapper.h | 338 | `acd8d58b7615012977b0147392b8c616a71205c3b2cbc66b9953a5d0bfbe1f09` | 0 |
| src/rust/bitbox-mcu-stm32u5/Cargo.toml | 356 | `4980c20d6863a9faddd52520b0ea0f39205f5ea2baa2441d203e6b6cb38c08e4` | 0 |
| src/rust/bitbox-mcu-stm32u5/src/lib.rs | 87 | `33f59b81e49b867519f3e09635f27a1a46f6bc4acd9d0f4aacbbc0adaca3d127` | 0 |
| src/rust/bitbox-noise/Cargo.toml | 620 | `1903f4c84f747fe0de9b1af349aa437b9ca54624f36075226df2314080c4e751` | 0 |
| src/rust/bitbox-noise/src/lib.rs | 556 | `6787c6b484f801c7d4e95443f0512b7247bff8dba8f871c54b92f21685e2d930` | 0 |
| src/rust/bitbox-noise/src/noise_xx.rs | 10043 | `4ade64136c560f523c56ae0e567721938ae097ab6a192c547f5891d45764c599` | 0 |
| src/rust/bitbox-noise/src/x25519.rs | 2023 | `63617ea3d8acc0f018c1664ce5abae381d71c29cec4b9f994bd042e92d982315` | 0 |
| src/rust/bitbox-platform-host/Cargo.toml | 534 | `e13d76508db7d5e832dbcea9d159fd868d9705976d3f96491af589acac2cc51d` | 0 |
| src/rust/bitbox-platform-host/src/eeprom.rs | 1808 | `e90f8286ddc5068a56e3b59f033f32e0292148117c35f826df0ee2fd36e3c259` | 0 |
| src/rust/bitbox-platform-host/src/lib.rs | 199 | `aa279b040b8a9357dd020dba45c6996af8780a46caa027bd1adb80c7dbfb116f` | 0 |
| src/rust/bitbox-platform-host/src/memory.rs | 12192 | `702d8734b4db0d0a259d6bc831b273411179bf57fdad065bd47c6cd677d60ed4` | 0 |
| src/rust/bitbox-platform-host/src/random.rs | 2083 | `fde390232194f51b1530025eec812bda2d16781b2ff11b7fa72b68d5a472a393` | 0 |
| src/rust/bitbox-platform-host/src/sd.rs | 3060 | `3f40d002d85cd970f8c70473f32197c54313c5766203d5fce33f2a5371c82b3b` | 0 |
| src/rust/bitbox-platform-host/src/securechip.rs | 7297 | `a383fe084917e785e7794e8950397b3fb5d39628ea0a926efdcb1bf9746c0bad` | 0 |
| src/rust/bitbox-platform-host/src/timer.rs | 1617 | `0e643681b0e7089742a91cb2621e39fa2123f634f50e908f6140751f8fa44f5e` | 0 |
| src/rust/bitbox-platform-stm32u5/Cargo.toml | 718 | `5501510cdaf7eb902f231f719b19f3fec7a542b4dc3160310cacc4a5e129d3cf` | 0 |
| src/rust/bitbox-platform-stm32u5/build.rs | 597 | `ab8ee6746d73105d4ea8cdb73205d7b3422b288c16cd5922c2ea5ca146b0697d` | 0 |
| src/rust/bitbox-platform-stm32u5/src/flash.rs | 3007 | `a128bfb727a5d77c521eadc35601cc385be833f8d0ce7089aa9bbdddd4a59bdb` | 0 |
| src/rust/bitbox-platform-stm32u5/src/inner.rs | 2010 | `f3c9459d7051aab14209a7e53d6995a9c9c2aa500ff9b1c910f522f74b57def9` | 0 |
| src/rust/bitbox-platform-stm32u5/src/lib.rs | 185 | `2ee9aac744280d9c128b6d74eab47a33a60e8f4524aaf75cf6ae1a8c1a0041b9` | 0 |
| src/rust/bitbox-platform-stm32u5-sys/Cargo.toml | 345 | `f00953d4fdd7b0a339a4275ba3a016813153790f1440bda76edffc6bb65a7700` | 0 |
| src/rust/bitbox-platform-stm32u5-sys/build.rs | 4624 | `e5a03d01598e2c749dc94ca18a3d1c069e1726108c863a167648be5c5f450f98` | 0 |
| src/rust/bitbox-platform-stm32u5-sys/src/lib.rs | 1804 | `7779a494a7b1f81a99cfe6da8e827ffaafa632b1e15d543bc8b55ba93aa53ace` | 0 |
| src/rust/bitbox-platform-stm32u5-sys/wrapper.h | 67 | `7bdf790812e8172badd61a9db85127dff2425a4654ecad202c1840d37e733db4` | 0 |
| src/rust/bitbox-proto/Cargo.toml | 529 | `21decdfa25e99c6645d4bfa993c898bdace001c059e9f7fa7b0023e22a0768ec` | 0 |
| src/rust/bitbox-proto/build.rs | 808 | `6d4f6136eadec490c81d39aae758968650da4c2442022749a034d968f027d141` | 0 |
| src/rust/bitbox-proto/src/generated/shiftcrypto.bitbox02.backups.rs | 3421 | `45f3b31bcbddbb90b7b8b29ebb0fa4cde683b573ea309bfa41e9c08f4a7122af` | 0 |
| src/rust/bitbox-proto/src/generated/shiftcrypto.bitbox02.rs | 86465 | `5b538703f43ef6f30896a79c051a3e37caf7b6c365b5493db6d535adba0c6fad` | 0 |
| src/rust/bitbox-proto/src/lib.rs | 1372 | `1d36872343cc062e807a7315fead89a405251f59fb66be5980de93594fdbf647` | 0 |
| src/rust/bitbox-secp256k1/Cargo.toml | 484 | `77442775d85b6ad99b047180d03c077b5427273e767a06175c5befb7ffb275a6` | 0 |
| src/rust/bitbox-secp256k1/build.rs | 1565 | `91983851f534bb1e29d57360162a303f9847ba6378c5873aa4088c655c748f7e` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/contrib/lax_der_parsing.c | 3595 | `4da2ecdc0a3b9dbb9029d188bb0243764a3c2f2324613a688f1ac4d3fc878851` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/contrib/lax_der_parsing.h | 4230 | `7f3e8ba009f19a5f2759c9065af02cc8e62351100d69f8ae7e762fa4b65ea675` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/contrib/lax_der_privatekey_parsing.c | 5112 | `48352c75520eecd141936c0011601925510cdf60afd3e46e79f0a0547cbc78da` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/contrib/lax_der_privatekey_parsing.h | 4016 | `3420812d623c0f2f86debe0535f98eab9b929036bb2fee2de8e3b1adc3e1a0b9` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/include/secp256k1.h | 44243 | `c04f49681ef8c9c5cf28ce0f9cc528ef39d64df0bace093bc3a18de4855b516e` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/include/secp256k1_bppp.h | 2761 | `bbd36b1d30ba8d181a84a234a29b91e1af6a6610cb24b7bc61326d12279d0feb` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/include/secp256k1_ecdh.h | 2560 | `ad314d14cb79a79d4113862f21e0deccf37962db7811c801dab2899f91dd8222` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/include/secp256k1_ecdsa_adaptor.h | 8168 | `c0f418ba9344aa4314ef9358fca624008db57ad17191f448b967daa16b45804e` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/include/secp256k1_ecdsa_s2c.h | 12269 | `ff02de0c7f482bd1bc68c725293d555e265809656b26a9d3c13adb2ccfa6926a` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/include/secp256k1_ellswift.h | 9148 | `620db468b1c13968946e9f404ceb59a3f11c895603bf1dcd3399567d7bf10e99` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/include/secp256k1_extrakeys.h | 10870 | `7c3468c9fd192ad152c5cf042cb44938961d752fcf19966123ce6a5e3fd31637` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/include/secp256k1_generator.h | 10816 | `1c08ef2a929eb52bff724c2d3d6e8d5a355382d76f9d510c2c4b769e5902ea6d` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/include/secp256k1_musig.h | 32175 | `e6e2595005881a64bce69a05cba3e2715e56a7a06398c029f736cc52bcfedc38` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/include/secp256k1_preallocated.h | 5966 | `b7283d4cc9c13bb2572dc92e69cea76f3270403baf5748ea4d91a1064b951b85` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/include/secp256k1_rangeproof.h | 12175 | `0b816f0b669a240ec5f0e90d724f43c21b03cd000926cb6dbf9ef8791e8e8ddc` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/include/secp256k1_recovery.h | 5225 | `3b2efb3ccf53e9f1bce93a4afae31946585958d5cba3b38fdfb1eea4c6ce2622` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/include/secp256k1_schnorrsig.h | 8177 | `8185d6c6ea3234fff05f38fad4b1b6f48f0574ab599dfc87297ab9bca0abfca5` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/include/secp256k1_schnorrsig_halfagg.h | 4908 | `89669a3ad2c904072c1177e7b783996af5d72635bb7590e02284e776cc4e085f` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/include/secp256k1_surjectionproof.h | 12407 | `f6b245fe8234309715225fb6a3fdf3a4d20a4f5a7f395c1686debae189af07a0` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/include/secp256k1_whitelist.h | 6944 | `12fba29620f0b7624ba1fd54bd4c7bfd8d73c259c725213d28d3a32518287efb` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/assumptions.h | 4667 | `cc875f356cc8f7f272def71f7d7261e44cc27a18a5b668cd8192c84d238e4e68` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/bench.c | 10190 | `832edacf541809e3cbc59a4e698d5e33a9388a7dddd55662936244cd106fccce` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/bench.h | 4777 | `12fafa36167bb38d28698536cdb34bdbcf8c972eed4d3cf69e71796972b880d1` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/bench_bppp.c | 1102 | `7c17a6b0fada57db18cc68b1ec183f1e6346983903ee1da4f894acb09bfab6e2` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/bench_ecmult.c | 15692 | `7749b0935da862249209c8903c3cb51aa8ed1ad6e4ebc0b92e3bfbb624e9ea99` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/bench_generator.c | 2001 | `6396798ee1f4a018d4ebd9e962b6c289f4a1928a870c20918285500f7972bf61` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/bench_internal.c | 19819 | `8e8c24bde37d16c24fb1da91617efee49000aeb8b54a750cafbbb55443d8fa69` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/bench_rangeproof.c | 2349 | `6c24fa0c6c12242da3b2629742e0baab65b24967d173fb83e94e2ce1847d8a10` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/bench_whitelist.c | 4089 | `8f77ebf85792d8270790e1c0689d24896c2da3d7ce6f35c6dffec2909ddc4082` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/checkmem.h | 5355 | `f367089bffa53b8998047de2f718f75d627dad549a1e5dc2a9ce9ab9f581ffe8` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/eccommit.h | 2198 | `3b04b7fdae817984c26ce995fad4f3f6d72d5c05b9d3f78d5991c531a5e99eed` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/eccommit_impl.h | 3165 | `6c71a9cba341b7782302741603db3ae2179b699ce2e7670cb03a749b94d114ca` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/ecdsa.h | 1164 | `f97753416b0971133ad9d8acf9af02259931d0285a0333a9753201a353070ef6` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/ecdsa_impl.h | 10477 | `883ad9ac4dfa224a1cc97bc2a4cc09b1078545a1632917dac2524a18ba4e53ee` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/eckey.h | 1449 | `cf511599285faecd27ace6191eca3945d85bc852b11076a1b1727759a6b03056` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/eckey_impl.h | 3439 | `4d327c593520c3f60f7b86d407df0870c26cf58037e4156ba8f92258304fd6b6` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/ecmult.h | 2768 | `1e87f35efb7e7e5b6ea1d6ec22bbaeab33ccd4eacc41a9092ee518ece9237ced` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/ecmult_compute_table.h | 1073 | `5a8ce69b18d777c3ad608ef173fd6a47c75b9c37bc6801f19ca4c44eb4b9f8f6` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/ecmult_compute_table_impl.h | 1916 | `6082339f616cd5a628300df24e66353c1374a117e24ddd474fe6151dbc620d60` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/ecmult_const.h | 1354 | `4705e7baabcbf8fd1853f8cef45a7f6a3075b98925d91cc209afda2c956942ba` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/ecmult_const_impl.h | 19584 | `07238bcf17c3292bb8198f7f37baf068bdc9a6a57f843c439e220eb08f400607` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/ecmult_gen.h | 5584 | `b15359caff9a96a348d23305b20b6b0f24d667d2614e3e078b0749e3aaedeb75` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/ecmult_gen_compute_table.h | 672 | `51eb54b0cb7b49b25cf751efb2799322d73c97bc9bdd2a263feff2d2d6eeff9f` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/ecmult_gen_compute_table_impl.h | 4705 | `9ae524743bb5871bff7e41e48b61218336b1919769132aafa944283ef1bb88f2` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/ecmult_gen_impl.h | 16891 | `a97fb72b41a12644520c09e9290346e7bd52c48492a74d6c90613e869163f88b` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/ecmult_impl.h | 34325 | `ce70d26cb987c9bb2a2477389459437fc2831546c9c14404b58cf7ed07f32cc1` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/field.h | 15119 | `4a044d83637686a021448c152bcef029337af9c53ce5d70983b73fa450b58ffc` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/field_10x26.h | 2338 | `ba9a43b62e7e70e6e18af2787bd01dfc3a57fea527cf8ad0333194211ac7d7de` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/field_10x26_impl.h | 52106 | `6f209a533fd96e73f4c92b101bd3ca46a2f7553967ba7f44650a68ccbf4fbcf6` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/field_5x52.h | 2380 | `cbaa91c253ba84d99efcd334c7a39906c164d5edf3cde81200a44a606205cdce` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/field_5x52_impl.h | 19372 | `414438d05bb496a6cf4e84938bdc286a0c13902fe8ea5e4a4bb862f90176af41` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/field_5x52_int128_impl.h | 11353 | `9f3071c7da547b94e0e6eabe0dbedc42535ea7c470f1dc891d0a24aa5d19dcf7` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/field_impl.h | 14052 | `a0ffc1e76ae4087ecb0a38bff62924710c5094ba9a209aeadc73a291b2f7b2af` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/group.h | 12243 | `d5443ba9dc805fb378d6dcdab02bd616ab34409b7b91ceb342ff4cee12adcf7f` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/group_impl.h | 35125 | `663da90fb18b6fc8dace045ceb28ea8fae6e1c68081c209cf0c7dc954398f30d` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/hash.h | 2625 | `a7f39f2ed170d70841eff7d43d9c480dfda6cb2e8ee25e7e04bf7433c27193af` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/hash_impl.h | 15448 | `70247571d95e3c8824d6ca2e90956f6941c196a42d860083040690aaf9ccf6cc` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/hsort.h | 1685 | `220cb669835d34c252598ecff860c93edda337a9f8c2fc07b2b6cead7d48b284` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/hsort_impl.h | 4798 | `2861489c01b927b27d99efe173799a812434748b4addd30d102187ce4f3b66a9` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/int128.h | 3622 | `89ac5d91d64f857038d063dd70eec4b29b4f32aa218c790fe049137c347186cb` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/int128_impl.h | 376 | `5683c02dfc495639da259d80624711c1c449bbaee6186729e399e713a28b4719` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/int128_native.h | 581 | `b4c52c7ff091083f5eca9879b98641c7a38356a3c5321cbcc22ae1573e7711e1` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/int128_native_impl.h | 2881 | `ecaafefadbde3db034d4f44678096833d2d113fd21b4ff7044095b6153ec03a8` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/int128_struct.h | 229 | `0733b3a65719a1e9a8fb3564c71a38f2f31ca3522f40087d536dba90361b66e7` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/int128_struct_impl.h | 7884 | `0b4e2200327f5357078ba43b0e0514c58c2b1eb217b87ebc14d95efb913b5be2` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/modinv32.h | 1865 | `774887ccd462b145434d1d6b9ae9455aa3618e791544a2b61267e18931d5010d` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/modinv32_impl.h | 33492 | `befe02af7099a871677c7b05a81302dff5a4dc1d59f19b20bcb58cc28e096112` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/modinv64.h | 1969 | `b71cf177d768beac28fcb4f0ef545aafaad16ad0f275c70ee4c60b5f7549ac41` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/modinv64_impl.h | 37653 | `1254dc7ea941fc4d4ef0a85eed80db58d9e2647a8b8d19238d6afc048d63764d` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/modules/bppp/bppp_norm_product_impl.h | 20378 | `13b376aadaf6ad496b82de06e57ce781c8dd591670405a50b41beb06d8b71614` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/modules/bppp/bppp_transcript_impl.h | 1552 | `bc8b8afcf3e985bdb355e715c2f56f109e2fb5a109f393fb0359db17b8aafbe4` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/modules/bppp/bppp_util.h | 2794 | `fb22fd546df224866adc6c756f76170b4aa2575cdda6872ee56f32af8079db95` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/modules/bppp/main.h | 403 | `20d3c6914baf5513f17d02787e51a97ecaa1670202ea5ca15bf7b09a35b0aa80` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/modules/bppp/main_impl.h | 3732 | `5b1f7a16c50b355846634222bf300c2887b094207b9a50f7488a2ff01b70cfa3` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/modules/ecdh/bench_impl.h | 1761 | `3929ead352b3b6425f0fdf94a1b2268d124cc0176929ae6ea3b4fa82abac0bbf` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/modules/ecdh/main_impl.h | 2929 | `3cf3b168e8048cd7b03c9b4d56d072214ef859a31bc970e5a16c2cbeba8fc4eb` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/modules/ecdsa_adaptor/dleq_impl.h | 8527 | `601af2921f4ae4f9964d440e0ea755ac15276b5dc90468ee640eb58e79f7cf69` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/modules/ecdsa_adaptor/main_impl.h | 15218 | `30b5b37a9b7ae794427399ab9522c74400ecbb2f8cafde6dbd7352db28809262` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/modules/ecdsa_s2c/main_impl.h | 8761 | `bbdeb3e19eff0731a80f2fbb07c5e44a2dc8d77a1944ead679bd3acfc0d51563` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/modules/ellswift/bench_impl.h | 4399 | `8973d64bda27eb72a4807aae665a1a2932d624370f9d40f8833f7c8f03b05564` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/modules/ellswift/main_impl.h | 27602 | `8deffa7b37a0602be2b87d0378419410e6cc9683ebcf3fb033d2eed56c4f8416` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/modules/extrakeys/main_impl.h | 9961 | `a58762afb6a494aaec984d2e65adacf1125be5e55ad2904af0f26e490cc0d3b4` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/modules/generator/main_impl.h | 17447 | `cde0530ab9af0b8b1d1d80e63fc8360484578fa68f2844295fb87d90e9284bf4` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/modules/generator/pedersen.h | 904 | `6529271ae3f7e786df540f650164e66cae35478157b5bba6fc885cde61d3e81f` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/modules/generator/pedersen_impl.h | 1733 | `ad22e7826eb983f0a629b20c7bb7d4caa452d09647248a9ea54be2c9f7bfdf6b` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/modules/musig/adaptor_impl.h | 3359 | `e22baaaa040a80c84f0cd72a8aef3b6ba4c260a926d4039bebb2618d54b78010` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/modules/musig/keyagg.h | 1324 | `5349443b84525a85434ff8f92a1e7542c0982b1b783a682613026203de4148dd` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/modules/musig/keyagg_impl.h | 11171 | `fa67be67a1cdb0ad05fc6fd5fce158731ea499a18f1b616bd17fe3cf19dead87` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/modules/musig/main_impl.h | 452 | `ea8d83ca27ceafc2d119c82d62975840302871978dd7a0309f8e3bcc132ed48e` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/modules/musig/session.h | 861 | `c256c3742a68849520569845640f152a22a4a8c21a96040cf0c1054516983980` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/modules/musig/session_impl.h | 31534 | `45c89618be2ef40dbc2006f96c6ee67d4ddabb84df2588731deb20e513c85c3c` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/modules/musig/vectors.h | 37797 | `c7cd9dc3804d864d17e43c5b00335a405a3bc4a30861838ac4599a213231e132` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/modules/rangeproof/borromean.h | 1167 | `204588b38d00b1db3765ab4b2c25e01f5afb5f5920a380cfeca381ace064377f` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/modules/rangeproof/borromean_impl.h | 7934 | `0afc699394931d77dff7d20f8ef6a0a18dc5146cab67921faf8c9ec2cd0e87f1` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/modules/rangeproof/main_impl.h | 5051 | `5403c2086d4b81f9e85a91f2290cafd3234e111fae7adbd065a2f5eb78adae82` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/modules/rangeproof/rangeproof.h | 956 | `a8d6285ada07204cc46dab26087b3c61b732c3b37cbcbbbcb793a8705f0ff80f` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/modules/rangeproof/rangeproof_impl.h | 26864 | `a691750d411ed06b4d15f1f566db992e77f7bb075f6ec52069038979dcfaa42d` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/modules/recovery/bench_impl.h | 2320 | `20d13192a4aabaa52ac4c2a2da772d8aafef00773051836b25faa2816226b386` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/modules/recovery/main_impl.h | 6153 | `93fb7455adaa364a3c1f8acef82ba409b88a49f688dfe23ab8555510fc614c96` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/modules/schnorrsig/bench_impl.h | 3795 | `9655992c7fd214231623716a738a1928e24a86b4bcdd909f331712df800a1abc` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/modules/schnorrsig/main_impl.h | 10885 | `24e5cbbaaf25cfa613b42c4b0d2e146ab85188a9a262fded6cbc40024a77c440` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/modules/schnorrsig_halfagg/main_impl.h | 7995 | `b39f484416360cfed7d061b0e7f80c0ded79c0ed68473d377a07e3f7f434b36e` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/modules/surjection/main_impl.h | 17974 | `f34a06bebf853edad54e7363c122f422b72eafeb3677f52f6216e2ee08422f04` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/modules/surjection/surjection.h | 1246 | `1a3179eb1793a56f224ac54942c07c5defad4d904382854090e5807877d76a34` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/modules/surjection/surjection_impl.h | 5058 | `62b41c3676ac78bfc7258a9513676fdaeec6bef7ef90b3980ac098f08ff42b27` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/modules/whitelist/main_impl.h | 6884 | `2f90904122c9b814a8f765c03c3c7d50bc57affb3ae720362ef2931ad2d3d306` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/modules/whitelist/whitelist_impl.h | 4915 | `3db091ee31cde1a3e2df2e2418fe07ce2f2d5c26cc63df71b1da49248efd4f1a` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/precompute_ecmult.c | 4017 | `8085ea86390eab2afeeec8b4f952036492fb81606dcd7bb038f940924b1b8400` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/precompute_ecmult_gen.c | 3864 | `23d1dadb40296d2752d024678e405b18d5c904fbd61d74598df3c8005ba64d2c` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/precomputed_ecmult.c | 2409168 | `1fba19c482de09f566ed9e7bf6a526e4edb59a1cf38218e3ab413000a0e0deda` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/precomputed_ecmult.h | 1585 | `d792b8a49759deff5f1e4092558fa9ae11d24e02695e44bee63a8f0ba8e18503` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/precomputed_ecmult_gen.c | 259715 | `c0a7af0884b7b07962be67e9da674e0d75a8d412d116153b8eae2a9e5527d401` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/precomputed_ecmult_gen.h | 973 | `8f514bed441bccf7e34ff05ff49d3a44e9395519a8fdcf176e6aeab7b5dbd5fc` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/scalar.h | 5732 | `fca33c29790cc58c71be8c8918a9f15a86b170e648e3770b08914dcfc2834017` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/scalar_4x64.h | 801 | `42aed583b28bda7982c54a6f63e50c0ae5f9c27d5f66d92ec6bf6c90e765735a` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/scalar_4x64_impl.h | 38397 | `1526b4710019a16d5ed719ad3559427366c662fa585206b1c0cf20d4e1d8f12c` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/scalar_8x32.h | 725 | `0614cea113aea88a47ef3b2ba8167722e850d7b2a696a4f16b03ec9a320ef1d6` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/scalar_8x32_impl.h | 32567 | `e1e3b7acc395ec440778e3ce99d139ffc9fd981981fe60976f3c042d7388c91b` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/scalar_impl.h | 12113 | `6ba654bd4edc0349d1d7f1dfc25ba2d73dd9f2ecdca8078e384bf7b7837d663f` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/scalar_low.h | 1135 | `3cab20db10224ff85ee7c6d975d2968c1370ed8e96ea26b94650f6e2bac31ac4` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/scalar_low_impl.h | 6503 | `0f47343a7d632e1aa983348c25be2fa011775208d66c6c6ddc1dba2d58172de0` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/scratch.h | 2224 | `4af5e1ff665c0418bcc5b1c2de954e7b377f9bdfdd4309e0296938918fac11ef` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/scratch_impl.h | 3677 | `294a55d429fa4cc9dec46ade345bbb2bfdff4055eb1cbf1ba6168a23e5e74db6` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/secp256k1.c | 34125 | `edf17de4216e2304af018511b54e3691021896811eb64693ae950254abbe7693` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/selftest.h | 1494 | `d695cd5a7369b372285ba0371edb6bebdb3dd79b719af336c714a3013adba6d3` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/testrand.h | 1950 | `bfe1b9a78209aa90d5652a83efccf633bbd874ed72dfe523f2ff6125f97ceba1` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/testrand_impl.h | 5786 | `ac12496cdb04f5432b14dbb60ab464317669532fffa5b1de327e21075f01dbb6` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/testutil.h | 4945 | `5a780fc16fcd8549ea4774d15beb2d36c6ad9a2ca7180dd95f84199a2863d1ff` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/util.h | 16909 | `950f48c6bce72ccc83cce14cefb441ddd7bc1377f8a675f453d2adcc0fa1108f` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/util_local_visibility.h | 402 | `d47d4a58f40157ab2a298151f366c5ebec8f7a1e7aaba88e36b530b1c01584ca` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/tools/symbol-check.py | 2428 | `1aa22d8ae539b6af24304679bc92bfc0bdde47818d9b81ee92af7800603bd34e` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/tools/wycheproof_utils.py | 427 | `9f2c2368953eeb3c9b7c3b31a807cde76b3106df93fbb975993638d5eb1a1e8a` | 0 |
| src/rust/bitbox-secp256k1/src/default_callbacks.c | 297 | `da45e3b9ba84a8289455a354a0e12d934ac515a09c0c0080afd1561c08ba0074` | 0 |
| src/rust/bitbox-secp256k1/src/lib.rs | 15733 | `42fc499883f91dea548d9ff0b11ad9770a60a560c74271563e66e7e573d77e28` | 5 |
| src/rust/bitbox-securechip/Cargo.toml | 862 | `6f3d69d24c02306d7c1b1ebb8d0e6f53e386217cc4132f786bdf4c14b259c373` | 0 |
| src/rust/bitbox-securechip/src/atecc.rs | 3668 | `a8cbd36ebbda21ff5f525a3842e75e94fc76bf377aba97ee8c924a87e0c7f7e5` | 0 |
| src/rust/bitbox-securechip/src/lib.rs | 3301 | `9d71da45b4b72c61b0f0648a6e2756ade7604486ecb0f2d331ca1896c6e3764e` | 0 |
| src/rust/bitbox-securechip/src/optiga/der.rs | 1945 | `51c9a5b5999f696830104a30fc38669b68985cc1fa15ebe1a2c8717fcc4bd124` | 0 |
| src/rust/bitbox-securechip/src/optiga/ops.rs | 20626 | `28f6ef019296d7087c62a4ade4089952ed70e8b5f4f1151b1f2061c495442071` | 0 |
| src/rust/bitbox-securechip/src/optiga/ops_fake.rs | 15685 | `de3f330803a923572ae8e073ae4af8a057a0391c32a6499d62bd4c962eef60b2` | 0 |
| src/rust/bitbox-securechip/src/optiga.rs | 37182 | `dd80d44ba7dd070e3c0c1c2ef42c318cfabf7e96eaaa9817aae6e4ff1beea024` | 0 |
| src/rust/bitbox-securechip-sys/Cargo.toml | 259 | `c8ecf19222651c1788eb0599179b20ee850fff55cc34e3ab9c36952289951d71` | 0 |
| src/rust/bitbox-securechip-sys/build.rs | 7537 | `3c435995bb9a2ac536ea75f6bc5d2857a14214b43e24d496e5413b4cce091855` | 0 |
| src/rust/bitbox-securechip-sys/src/lib.rs | 311 | `1531ac58123bde8556099e327af91ec8e5db645bd971854fa6876e7a8d100ffa` | 0 |
| src/rust/bitbox-securechip-sys/wrapper.h | 123 | `c2f4dac6ec8ac622887b6938beb8ea123b16d32fc64c151256fc5bef9159917b` | 0 |
| src/rust/bitbox-u2fhid/Cargo.toml | 212 | `3e941a6766699c0e11a57e5a81779d4563e0ef4cf9b71bdc56a4be0bfbaea031` | 0 |
| src/rust/bitbox-u2fhid/src/lib.rs | 23418 | `7b70b84d5579fba6237c5a176e5479c5b94502f655d63e81e047400350dc8b07` | 0 |
| src/rust/bitbox-usb-report-queue/Cargo.toml | 291 | `053b288e4a5823e95b6362dfd133f63f2bd87634db7343b95c931ac75007b710` | 0 |
| src/rust/bitbox-usb-report-queue/src/lib.rs | 10931 | `5a161e6b53648bda9c93dc66bbe58e5f1de2019925404073a2ebecaf474f807f` | 0 |
| src/rust/bitbox02/Cargo.toml | 1669 | `b70d719688aa910b578befca33864e88ee5c4011f2c03e68cb22e3ff612bf4df` | 0 |
| src/rust/bitbox02/src/da14531_handler.rs | 584 | `a4ef27ce8aa7d67aed9ec004d45235b0ebbb9cf9f6cc3f27b4f2963edf179343` | 0 |
| src/rust/bitbox02/src/da14531_protocol.rs | 880 | `63a96c8132ae1e3c14081bd8cef8b1f4617c4ea1ef586091cd8dd70c0205d72b` | 0 |
| src/rust/bitbox02/src/event.rs | 248 | `bf922d48b6110e575cf44bc25bbdafe56949fd54ef922730cf2b028d092735db` | 0 |
| src/rust/bitbox02/src/hal/eeprom.rs | 942 | `8154b22c49dfc6aba4a2c3b9940a0691738d899e4fe1f086c35a992e9a6f6a14` | 0 |
| src/rust/bitbox02/src/hal/memory.rs | 13523 | `473863fe6af3fb418ab72f97c99e8312d305a39517412a675e08e8175b793259` | 0 |
| src/rust/bitbox02/src/hal/random.rs | 783 | `2e1db38e7270a448d0ec60d8edfaec3156bdca102d6c3daa149748289fa5c22d` | 0 |
| src/rust/bitbox02/src/hal/sd.rs | 1306 | `7ab3174a13fd91733d38d08b24bd2ccafbcf1243dfecaa37d93527ad095b77aa` | 0 |
| src/rust/bitbox02/src/hal/securechip.rs | 11172 | `1cd7cce092509b4025fea0317afe9aa7ef2e59bcf9958b3c20d0de3d51bf0a94` | 0 |
| src/rust/bitbox02/src/hal/system.rs | 1477 | `6b1b1d5546d581e3ffc1fe9d7da92e52d312e0078cdee9db506dcd2ed04ce170` | 0 |
| src/rust/bitbox02/src/hal/timer.rs | 2636 | `85c0bed052cc43976f4c401ffdf5d83bfe1d7d15b2b84a6c2aa0d80984b3b5dc` | 0 |
| src/rust/bitbox02/src/hal/ui.rs | 14681 | `8e7d3ad2359f392ae852b68da7d6723f831adabedaf5883e9d00fa8012d81a96` | 0 |
| src/rust/bitbox02/src/hal.rs | 2058 | `d6915485b75c894ba22b5a62c8b90d521f53157ce6c2d217d4bead82eccce5a8` | 0 |
| src/rust/bitbox02/src/hid_hww.rs | 321 | `724870b9fac503e4e30a9dcfa7f3bc066419776ff26fdc2ca94f88fb72aa312c` | 0 |
| src/rust/bitbox02/src/hid_u2f.rs | 321 | `8643cda0f6b2d05d969ce9173354761b2264745d3c4b65277a5e8650389300e1` | 0 |
| src/rust/bitbox02/src/hww.rs | 101 | `d4cbb84bb30eae55a5d2a57c3b4cd3d1581c465305f0a7aa8228c62e6cb09d75` | 0 |
| src/rust/bitbox02/src/lib.rs | 3431 | `b6e93585807f0e85bf91e713932d289f18759f3e9f90871f3e1e2d24030a5c0a` | 0 |
| src/rust/bitbox02/src/memory.rs | 29086 | `d3ad0bad7493c2002c330e45c3fde403fb95d37db43f9cd3f9c7ea68fd9c6548` | 0 |
| src/rust/bitbox02/src/platform.rs | 387 | `d2ecae56b160e9760f16ced2e9a17174b270fe43e0d7b714358bfa17f4f50e0f` | 0 |
| src/rust/bitbox02/src/random.rs | 1425 | `edcc95719949a75adde6a34205951544cd8960c8f8742cf82d7e1a24480aa218` | 0 |
| src/rust/bitbox02/src/screen.rs | 1206 | `6b5d0d4eab685a82c934dea778c963e411c91aabd8a62f943931d734c566eabc` | 0 |
| src/rust/bitbox02/src/screen_saver.rs | 686 | `f08978cd4f9adc7285150e7fc806a61df24fda669027b9137356b44c113e3948` | 0 |
| src/rust/bitbox02/src/sd.rs | 3633 | `332eed271f3a1b655dd3bca4a6e4de60a011e46d9da11fdabfc70e294110065e` | 0 |
| src/rust/bitbox02/src/securechip/imp.rs | 6338 | `83020355fa265b9e4e37c87c4f36c5909b62d628162b1982f065c6ed6b54d55c` | 0 |
| src/rust/bitbox02/src/securechip/imp_fake.rs | 3211 | `330cd9da55af9c84a08d8f350e84e2fdc8c1c73ee96ea77c91681efd17c22af7` | 1 |
| src/rust/bitbox02/src/securechip.rs | 259 | `74f1549267b89c45abeb33faa7b537897aad0c8fc1257ce160dc50e960a24cc5` | 0 |
| src/rust/bitbox02/src/spi_mem.rs | 1334 | `f62ac7882ba064c5e08ef0f6e6d6fd466bfa68adda78f14a34c55f5772cd8049` | 0 |
| src/rust/bitbox02/src/u2f.rs | 198 | `1a80974c4b199c6418d90887e5895b2e89ea249936bfd652315fe8dec147305c` | 0 |
| src/rust/bitbox02/src/u2f_packet.rs | 463 | `1de6b32c0488616e6343e5ceeb4131d1621a35824139984fb1510d09c052def3` | 0 |
| src/rust/bitbox02/src/uart.rs | 822 | `12c23b2e2d988d49d67a3efb9647408309d40fa0e95b1f4054090e6e321d0d15` | 0 |
| src/rust/bitbox02/src/ui/types.rs | 3770 | `09f8ea3ffa8ca24ade9793ffd205a1eda3ac3216bb291daf72fc3a770d29572c` | 0 |
| src/rust/bitbox02/src/ui/ugui.rs | 72 | `c3c17298da8d70199030dfc0c054cd953f08460fb924f74ad9dab7a9dc2860d1` | 0 |
| src/rust/bitbox02/src/ui/ui.rs | 32463 | `df7dbba10ee96a9ded04a6cf9891b49bb239d8374911e637073d315b1fdbe02b` | 0 |
| src/rust/bitbox02/src/ui/ui_stub.rs | 2885 | `44a7c3b57ab698f176f1a6dd661d2b4fdd8e44481e70f3b52da95b50e2b8b820` | 0 |
| src/rust/bitbox02/src/ui.rs | 632 | `29e754c46c1185d2fefa2261446a4d6cdf656ff2f2675233ea373e46fac5d8fa` | 0 |
| src/rust/bitbox02/src/usb.rs | 153 | `965aefb4815cdccdf10f5a2898efd9506e6fff5de3ca33e5ce9234acfd353544` | 0 |
| src/rust/bitbox02/src/usb_packet.rs | 912 | `b54e3d1f804137366c10d343e0b69b0433384ec1ff156e15d108ff61c0362eba` | 0 |
| src/rust/bitbox02/src/usb_processing.rs | 1240 | `60de0f4120276030ec4689de0b3e2df8e83779f34627eeee87533081970fbaa5` | 0 |
| src/rust/bitbox02-rust/Cargo.toml | 4607 | `70708f2472b1cc14d6973c14214edd75afdc82ef08293b74fa3212b721ec253a` | 0 |
| src/rust/bitbox02-rust/build.rs | 2374 | `0fdd53625ca0ef342a07b6511534ccc0413dfb7ae06c455dbc58e14661a39798` | 0 |
| src/rust/bitbox02-rust/src/async_usb.rs | 16034 | `f24da5058d7c408f62069012f5f2463b1c76a5421a3d4e370c556121859da605` | 0 |
| src/rust/bitbox02-rust/src/attestation.rs | 2902 | `c20b01cb077b8baaa32a6ee878c0fd3038266ad5659829bdfbb1ec9bfcb19404` | 0 |
| src/rust/bitbox02-rust/src/backup.rs | 21345 | `4efaf420eec850fec73301ebd5a101c28acd12a1fbcad82d7a2cd32321a34fa4` | 0 |
| src/rust/bitbox02-rust/src/bip32.rs | 13090 | `69904362ecbb2911101474f83924b9dd5cbd17e7ea748a733573e9d09d02d7ea` | 0 |
| src/rust/bitbox02-rust/src/bip39.rs | 10472 | `3066de8005955ca3128da1bab484d55ba24d368a5ea113d36f1d89123ffe47a5` | 0 |
| src/rust/bitbox02-rust/src/communication_mode.rs | 1970 | `f0301d116abedb634542e247de509b5893e48290c851a420a948cf3db219fff8` | 0 |
| src/rust/bitbox02-rust/src/general.rs | 367 | `51fc5e6dda75ecf8de8e25c673afc1bb44214079f9fc848b5f1b733e7191dc09` | 0 |
| src/rust/bitbox02-rust/src/hal.rs | 120 | `18d3943a548c4b5d51e366ea87f01d61e419958ea8f91002d931ea04c1da10cd` | 0 |
| src/rust/bitbox02-rust/src/hash.rs | 1517 | `4b667a9836bade2671d5c320ba17c8644e245b613d4e6cee8d5f155697952ade` | 0 |
| src/rust/bitbox02-rust/src/hww/api/backup.rs | 14916 | `5374eff995386d703bcf4520b299484ee5673049bcb93f968f49c5374c0f0657` | 0 |
| src/rust/bitbox02-rust/src/hww/api/bip85.rs | 4647 | `ca089a3a18442b292edfe900b31b8c59f600cdaa5e9cfb287c4683474a39834d` | 0 |
| src/rust/bitbox02-rust/src/hww/api/bitboxsync.rs | 41098 | `e15d530066a769341285a06cd933c9a5bb5fbffee95c9d6abc10ed581713428d` | 0 |
| src/rust/bitbox02-rust/src/hww/api/bitcoin/bip143.rs | 3095 | `1f374135c58bae745e88d9500fc29164ac723d522752bf67fbce069a45730684` | 0 |
| src/rust/bitbox02-rust/src/hww/api/bitcoin/bip341.rs | 5494 | `7217fe9028053addc3c36337b2a43958d7e56a3a4d8a92c1e630dba3301fadfc` | 0 |
| src/rust/bitbox02-rust/src/hww/api/bitcoin/common.rs | 26882 | `b8a6f3c01008c0631fb04cbc9b8f389c6cf30de321502f994110143f0a7eab56` | 0 |
| src/rust/bitbox02-rust/src/hww/api/bitcoin/keypath.rs | 18724 | `d5d08ddb0cf20c3ca0497a723a08d748f863118b90d170ddf1a0d308a7d39801` | 0 |
| src/rust/bitbox02-rust/src/hww/api/bitcoin/multisig.rs | 42734 | `cff6a02dc53347895b0f6c7562c316eb354eba5a81ecaf8cf111da6f00e8a88f` | 0 |
| src/rust/bitbox02-rust/src/hww/api/bitcoin/params.rs | 2291 | `fae19e0b1a338960fb97055efcd6bd6c1d1572962faf960644cdf239592341ff` | 0 |
| src/rust/bitbox02-rust/src/hww/api/bitcoin/policies.rs | 82001 | `abc68ccee396717d58844920139f2d29bb75a4fabc74f976897470f0232d4b91` | 0 |
| src/rust/bitbox02-rust/src/hww/api/bitcoin/registration.rs | 12363 | `338b00774cb29f0dbfe5a480dc6c944f70fa72d112e976fd4e9bb873ad1deda3` | 0 |
| src/rust/bitbox02-rust/src/hww/api/bitcoin/script_configs.rs | 5506 | `17594a528cf37f0398f0deb18b16e996060fb670dae8520de29c243379c7c170` | 0 |
| src/rust/bitbox02-rust/src/hww/api/bitcoin/signmsg.rs | 25339 | `7f2d957f821c1930f16dc8c1de5982ece4f50b3468307cdbc8925ff34b21a979` | 0 |
| src/rust/bitbox02-rust/src/hww/api/bitcoin/signtx.rs | 138278 | `195b930b906cd84cefc9bb4ceecae73268d702b22b019f80b18992d56c6a45d3` | 0 |
| src/rust/bitbox02-rust/src/hww/api/bitcoin/xpubs.rs | 6970 | `4bc855177239b7b5cf15dd545a461bc421f39555d8f7fb3a65b672af96848836` | 0 |
| src/rust/bitbox02-rust/src/hww/api/bitcoin.rs | 53465 | `181410dc293fae8eb397eeb72e4b0ac6094efb5740c9d8de249b12b8253e69cc` | 0 |
| src/rust/bitbox02-rust/src/hww/api/bluetooth.rs | 14999 | `54fc1a9ca2d9412a3708551436f0d0b2b4c93ff2aaae3f51deee8c3a77c4e539` | 0 |
| src/rust/bitbox02-rust/src/hww/api/cardano/address.rs | 25289 | `2edeeab72109e5d9c5244ae16cf22b7397aa658364c5f27466538b16deb366ab` | 0 |
| src/rust/bitbox02-rust/src/hww/api/cardano/keypath.rs | 9489 | `669a3af625f388c46d5718aeb4cd88476c16a2629e3d12134b811f0068882350` | 0 |
| src/rust/bitbox02-rust/src/hww/api/cardano/params.rs | 1354 | `d7afb92488f4c471889b2d5db2526630a474377dcbd903d85659d12d671ace3e` | 0 |
| src/rust/bitbox02-rust/src/hww/api/cardano/sign_transaction/cbor.rs | 11409 | `89e1d37d2bfb99b67ab18817241be589831874e5f56a5f0075f3a6bbf0bf70ec` | 0 |
| src/rust/bitbox02-rust/src/hww/api/cardano/sign_transaction/certificates.rs | 5772 | `039d3fb80dec40bf724d7daaf3dd4ab7c9d3f1d35b159a04503ead5a3564c8d4` | 0 |
| src/rust/bitbox02-rust/src/hww/api/cardano/sign_transaction.rs | 74982 | `5e94e09ed5e9e28ba9935be3120f5926f5ebcf6c4a275e79c2a25c2cc0564ad9` | 0 |
| src/rust/bitbox02-rust/src/hww/api/cardano/xpubs.rs | 5566 | `ca845c4de879d93b868925ace61c0471acf3041011d8bb63f916239064c2055a` | 0 |
| src/rust/bitbox02-rust/src/hww/api/cardano.rs | 782 | `fb2b77c02fecf5d5b0927aff56ec1ee7c4d90fdbaf3e112043b66f58508891e6` | 0 |
| src/rust/bitbox02-rust/src/hww/api/change_password.rs | 8093 | `df7e6672fc66ba2ce24c092ff0b58224b7181bf87fd978f501eea082a2aba4ab` | 6 |
| src/rust/bitbox02-rust/src/hww/api/device_info.rs | 3187 | `cf7700970753c5467429c85b88e4f21dd87f88aed83c0e879cfc899700c270f8` | 0 |
| src/rust/bitbox02-rust/src/hww/api/electrum.rs | 3010 | `9cf68840f7aed0f19a71e0ed7771e423a77cf662ae54ffc196e88999215249a7` | 0 |
| src/rust/bitbox02-rust/src/hww/api/error.rs | 4335 | `b6a13ec95227e726cf487267d3a0ed53bc9cab5b1d3860d497dee0ec97cd59c1` | 0 |
| src/rust/bitbox02-rust/src/hww/api/ethereum/address.rs | 6735 | `57664aa3edfb4b15fc9341ccf65cc9c7da221fd0a59b988b4a4b2bbd05d42d37` | 0 |
| src/rust/bitbox02-rust/src/hww/api/ethereum/amount.rs | 4447 | `78effd3b340e7034d0c5bb3332151d9fca0b944c312f2235be007a3bb7d0fb74` | 0 |
| src/rust/bitbox02-rust/src/hww/api/ethereum/keypath.rs | 5510 | `e7129e999976e13aaed04d41604ae3e7d65b5d3e8c6da7d5ece9063554523369` | 0 |
| src/rust/bitbox02-rust/src/hww/api/ethereum/params.rs | 6318 | `6d45acd07d99ea9e40064d668797b13f5b24947beca278a8ec67ec96a63c68ad` | 0 |
| src/rust/bitbox02-rust/src/hww/api/ethereum/pubrequest.rs | 11492 | `1fb38f29c8acc366e5e28ee31505eda46b33d29abca6006453cfb3aeb5fb3614` | 0 |
| src/rust/bitbox02-rust/src/hww/api/ethereum/sighash.rs | 27142 | `cccb0d7501d1db215c00bbc9586b3d873625b63606d2a072319eb5b1f7408e8e` | 0 |
| src/rust/bitbox02-rust/src/hww/api/ethereum/sign.rs | 96116 | `1891a4b2d603dcb45aedd9b2fc409ddaf9d27a813264145b7b9b3cbda7001b46` | 0 |
| src/rust/bitbox02-rust/src/hww/api/ethereum/sign_typed_msg.rs | 117444 | `890c26321761c405f6ec0b238a67ecfa3aa3ad9d2c594f2bcbb85487e57020de` | 0 |
| src/rust/bitbox02-rust/src/hww/api/ethereum/signmsg.rs | 10476 | `b4de40b5a63033ec24e52f0077c80a3a73a9471fdc6d10d5289322356cd626cc` | 0 |
| src/rust/bitbox02-rust/src/hww/api/ethereum.rs | 5189 | `873ca1378407cae796dfac9032da1bc6e980612f5f2846592ff2d493384071bb` | 0 |
| src/rust/bitbox02-rust/src/hww/api/payment_request.rs | 67439 | `c76bd2db8e0205ee3cf3e26cb00132da08975241342a6f88939966e2c4a24684` | 0 |
| src/rust/bitbox02-rust/src/hww/api/reset.rs | 2174 | `44fa3b048c424a65d24d853cd2fe6aaa805c37b6f23b2c7bc0bca915c98145d0` | 0 |
| src/rust/bitbox02-rust/src/hww/api/restore.rs | 9331 | `3afe08e63f02f6e0e547bced73824bb37800e52551da477c4cc95f1f2925f307` | 0 |
| src/rust/bitbox02-rust/src/hww/api/rootfingerprint.rs | 1540 | `bec5a60dbc30d5c9fbc4b387d121c35cc82420262422c85693f79b65d6c07626` | 0 |
| src/rust/bitbox02-rust/src/hww/api/sdcard.rs | 2540 | `9ac1af0cd1531ed86ab3dee9b9ca1711573ef131617453faec1a161a3245afc1` | 0 |
| src/rust/bitbox02-rust/src/hww/api/set_device_name.rs | 4581 | `b336413a7ca7043f89df8cfeb781e7c602739c44b6d17fd21811dde8b6e3f0f4` | 0 |
| src/rust/bitbox02-rust/src/hww/api/set_mnemonic_passphrase_enabled.rs | 2612 | `c1361dc350dcc62f74137349a37b5190afa02dfae0952e622569b8636f8b8e60` | 0 |
| src/rust/bitbox02-rust/src/hww/api/set_password.rs | 4915 | `34eb42602dc38d169e1994f8e360c960562739af09700e633fa6057dc09b4a05` | 0 |
| src/rust/bitbox02-rust/src/hww/api/show_mnemonic.rs | 7482 | `a5180d83d601f5774114f1cba451a2783358e952e52cbbc421a1de46c81f4f13` | 0 |
| src/rust/bitbox02-rust/src/hww/api/system.rs | 1785 | `a0527f375722906e809a1410e5cbbd8404ec3d19bbd8d4d278e675a8b69e2531` | 0 |
| src/rust/bitbox02-rust/src/hww/api/unlock.rs | 6665 | `29ec66437733d134968bb4e5b366d71cf0e47aeacbcaa8e5d157ad2fc90c889b` | 0 |
| src/rust/bitbox02-rust/src/hww/api.rs | 8874 | `4e88939f98f0466f8f635eac082d397f58abb032590ea8f0a29afe55741f1f7c` | 0 |
| src/rust/bitbox02-rust/src/hww/noise.rs | 5095 | `84f8975fbe603db802539bd6b6973505ce5938787617d4f53fa3923056d50024` | 0 |
| src/rust/bitbox02-rust/src/hww/transport.rs | 16808 | `371927da8fdefc6f47d8a5cdb7518242446f2340efdcca17ca0b90a5ee023dab` | 0 |
| src/rust/bitbox02-rust/src/hww.rs | 28291 | `2927bcad9778746803fd0da2c14bf7959bea20c137c5fd572a5e3968e3614cb8` | 0 |
| src/rust/bitbox02-rust/src/keystore/ed25519.rs | 10193 | `85cb066d8f6e599c0f1eeafe7aa139d6c51c0bb678c4d0308173de566c61304d` | 0 |
| src/rust/bitbox02-rust/src/keystore.rs | 83987 | `b7918fdd4b52ef1b088e28bf88f3442f8243d706fdf1db79c60e71fb8817420b` | 2 |
| src/rust/bitbox02-rust/src/lib.rs | 869 | `54ccda57e672294cdd51137f4e529824830c58457644c67d8b6d2952442471b5` | 0 |
| src/rust/bitbox02-rust/src/main_loop.rs | 6571 | `8f8dc3d87d7a372ba046e88c3e844c1ca14b8ff5340d715af412297fe820f381` | 0 |
| src/rust/bitbox02-rust/src/reset.rs | 4440 | `fc08d0007d657de5b8f162034006b1eefd42822948c09ad247aacb2bd28ce528` | 0 |
| src/rust/bitbox02-rust/src/secp256k1.rs | 287 | `4da9a5cfc6fee6086c57c29d11367c6473c6f2bc7e7ec31c593ef67a6464883f` | 0 |
| src/rust/bitbox02-rust/src/u2f.rs | 6712 | `3d6bffb5411151496b3962d2f9c5ee559fc86e060f86791f8b2ca1b40439e5e9` | 0 |
| src/rust/bitbox02-rust/src/version.rs | 166 | `49bbc061dde4aa1a081e6e79d3e0a65ef4067cadfeb636c0b02a4aa6f311a33b` | 0 |
| src/rust/bitbox02-rust/src/workflow/confirm.rs | 1449 | `84c4285756710f56d7ccabd75246644e49ae186c2d1d3aae6a4579911550bc02` | 0 |
| src/rust/bitbox02-rust/src/workflow/mnemonic.rs | 34778 | `2257e6aceeca61f3939defe9bb98fa092f5ce6bcd4a424b84aa298af40037831` | 0 |
| src/rust/bitbox02-rust/src/workflow/pairing.rs | 1690 | `345b1b3d5c9873b12eff6f03f40d279bdd27dd077daeddab88199d49874315b7` | 0 |
| src/rust/bitbox02-rust/src/workflow/password.rs | 6278 | `f0a995ecf8584cd5c58cb37f20686d39e9654c5cfa35289d267b3ff939c3b019` | 0 |
| src/rust/bitbox02-rust/src/workflow/transaction.rs | 3554 | `6451402352fb8ff628bba81fabd478aec289f32385735b8b68a1372b6fc02c05` | 0 |
| src/rust/bitbox02-rust/src/workflow/unlock.rs | 17747 | `065962fe57d9cb6640869677d8f5489bc0fc188a060f746dd83b562f80805fa9` | 0 |
| src/rust/bitbox02-rust/src/workflow/verify_message.rs | 13559 | `4a2c0f3cea125caeae7d0371c7629ae08b03f3cb6d76f183cd6d11385e6fe846` | 0 |
| src/rust/bitbox02-rust/src/workflow.rs | 296 | `885ca432cb372563ae134d554254bdbd8b914a880c12c5e15517df1b8fb668e0` | 0 |
| src/rust/bitbox02-rust/src/xpubcache.rs | 11790 | `fcc3f7f8340292a2d682a108772c490f6d41827c31f331a0edd32f4d7fddfc8d` | 0 |
| src/rust/bitbox02-rust-c/Cargo.toml | 3932 | `2c730e8b213a5d8e3a381d0a5e4c2745e0ba2a12344883db570fd8d70ddd061c` | 0 |
| src/rust/bitbox02-rust-c/src/async_usb.rs | 2063 | `47a9499822950a6254d095bc1561302952fe6335fa5563cc400b79426b97978a` | 0 |
| src/rust/bitbox02-rust-c/src/c_alloc.rs | 905 | `471866858b22495db4c369feba9db9b5af816cb01d5e4c87f0f882573f1fa697` | 0 |
| src/rust/bitbox02-rust-c/src/communication_mode.rs | 378 | `c8d296555831770fa32351f31bad19787ed3693d366c9f42f2e4c9d9515e971f` | 0 |
| src/rust/bitbox02-rust-c/src/firmware_c_api.rs | 5436 | `029d99f0ae93aafe5fa6331d4ed1787be0189241340a75018052958599fa4358` | 0 |
| src/rust/bitbox02-rust-c/src/lib.rs | 5125 | `c872df632ac63a1f4735660e6ac132b661f80f0939a38c07914203d6a3ac31f8` | 0 |
| src/rust/bitbox02-rust-c/src/secp256k1.rs | 6624 | `54c1ff4e1f9ed19a0c92a26d1f83cc8a2fea72509e0394ce4ed01973e0f2c3c6` | 0 |
| src/rust/bitbox02-rust-c/src/u2f_c_api.rs | 9830 | `f9dd4d7daa5fcf8b4361292668bfaf314c9e817e2a6d8bdeb8f22e9d476ba5e9` | 0 |
| src/rust/bitbox02-rust-c/src/u2f_c_api_stubs.rs | 781 | `e7f0952fdbfff2c7a2f00c76c01ad871c4ce0bcc8d783a445321b1f27840ef5a` | 0 |
| src/rust/bitbox02-sys/Cargo.toml | 390 | `4492ef51f8a188413a4ee87a0dc30f58c2cd5a28f890a631480558672e3faaeb` | 0 |
| src/rust/bitbox02-sys/build.rs | 21680 | `6370b2397f94e9e9531ae43ecb9dfba9e819e1d7f0dae4c23a3e89d8658a3a07` | 0 |
| src/rust/bitbox02-sys/src/lib.rs | 892 | `8ed5a6852000ff1e71639e70b0d8243624213c16d85a0f7b64aff02ab41a6e9e` | 0 |
| src/rust/bitbox02-sys/wrapper.h | 2101 | `ce7ee138f934a422cd5a49f23498dab908a330bbc1ebba755c99bb1832c385b9` | 0 |
| src/rust/bitbox03/Cargo.toml | 400 | `6927165100e35a7e5b2e199208a4c7db809060ea479f375649961c1658d8c3c3` | 0 |
| src/rust/bitbox03/src/eeprom.rs | 792 | `ddfb8813943a33930450b01e2bb1616811ee5ba688a51a5cec5f37ed4bc39ede` | 0 |
| src/rust/bitbox03/src/io/touchscreen.rs | 1866 | `ae775069eb670b7d1f0e62545590e920d12b10a817b7e031a9829b2cf360b471` | 0 |
| src/rust/bitbox03/src/io.rs | 61 | `2953777db481a5a05c64b72d4f3a9ba953aa2f72a9b38c2ffc270b50c2a644f5` | 0 |
| src/rust/bitbox03/src/lib.rs | 2578 | `38cd67b71d70f90fee279114ad5d1398c695eaa859950b85d5a022ae358368c5` | 0 |
| src/rust/bitbox03/src/memory.rs | 3894 | `4245c2ea7d8b4506f821543c2b4f92c9c03b7da8c6575f7d6ac344f07b592284` | 0 |
| src/rust/bitbox03/src/random.rs | 259 | `19138960ca09317cf42a71bd818c0171ddd703c0db9c1ff6a0019157bd492420` | 0 |
| src/rust/bitbox03/src/sd.rs | 727 | `6d7d16479a0cdd1f9fbd270ded12f5d8231208e48299c62bf1086112e9da162c` | 0 |
| src/rust/bitbox03/src/securechip.rs | 1946 | `42c32de5b793c2c21ef8cd188192fb821c778cb6b47e5c9d37eccdca3452862c` | 0 |
| src/rust/bitbox03/src/system.rs | 446 | `d748f74fd561901eeec5b1e43bfc50a30d3515b57090f468f786009b394d3613` | 0 |
| src/rust/bitbox03/src/timer.rs | 239 | `71b861386ab450012cb83ff87a1a5799dd4ebfb234b3f7781a65d5872c815409` | 0 |
| src/rust/bitbox03/src/ui/choice.rs | 3868 | `161d493f0600ce9c57d8ecdeafde6066ebb5ecd02e94c0e201c8d69be5852779` | 0 |
| src/rust/bitbox03/src/ui/confirm.rs | 6097 | `38396a0ad70cbc306c39df4293d497916bcffde5674b5918c7f7b81f385625d7` | 0 |
| src/rust/bitbox03/src/ui/demo.rs | 3421 | `1d9858404809ee7f4b0d9bcbba9b76fa7360386db1064c7784a6b9bf45dbb3b6` | 0 |
| src/rust/bitbox03/src/ui/enter_string.rs | 98270 | `3742ca93ba5aeed6c2a0a5d1a1a4d0f0797c8b0ee01e5217072e1c2bd0c4d5a3` | 0 |
| src/rust/bitbox03/src/ui/keyboard.rs | 33770 | `8e3bf28083cf243c0c9f45f7c30675ba0655c488ef01480bf845293f26c4d01c` | 0 |
| src/rust/bitbox03/src/ui/keypad.rs | 5537 | `67c0c3ed07ff6dfbd20609f8f95854356e7bf107bcd00217a3fbfaf30fd5891b` | 0 |
| src/rust/bitbox03/src/ui/menu.rs | 4895 | `cf75ab296292809f1b3c571e2e47024268d50aa889cf81dac52a27f2846460da` | 0 |
| src/rust/bitbox03/src/ui/nav_button.rs | 8533 | `695ae86711d9a7bb9b5e4dbbcb96f988de3200878dae044a86b7cb9c72a15d9a` | 0 |
| src/rust/bitbox03/src/ui/recovery_words.rs | 21855 | `8693f42ae62696f45f923dfadb51c55349385f2ff23484a158fb8741f8ca662a` | 0 |
| src/rust/bitbox03/src/ui/slide_to_confirm.rs | 33146 | `f2cc8a66ddfef7be8e0d521e23104cdfb7eeba3ff1129c99adb135883a97bc57` | 0 |
| src/rust/bitbox03/src/ui/status.rs | 2746 | `28cfc602ea285c799d834462b8013ee85bd14e11a0eb94f6473211d26ddee11a` | 0 |
| src/rust/bitbox03/src/ui.rs | 14682 | `1d353457089c94e7747b248670e64a5203f4407e0aee997d325d5afacf872e34` | 0 |
| src/rust/erc20_params/Cargo.toml | 309 | `9e7f84d4c08350c9fd01151b5e00bc58ae558fb6b612678ffc0b5ad9a81ec76d` | 0 |
| src/rust/erc20_params/build.rs | 5606 | `036ca79ff51cde8f3d84746440840185f617b63d2068367058c566003d0651f7` | 0 |
| src/rust/erc20_params/src/lib.rs | 7510 | `2692c60e866fd7ef4fbc5c3691b101e43f50255e99c3fe8d877fdf3211c24b5e` | 0 |
| src/rust/fatfs-sys/Cargo.toml | 253 | `8e99c5b88d0e76f8c315afb2a1b7cd57da52bcc40e673b717b7d0a13e9dff266` | 0 |
| src/rust/fatfs-sys/build.rs | 590 | `19030cba4386dfedb0e812698684f5b7f225079e2c9e3218fe44886a59b26e63` | 0 |
| src/rust/fatfs-sys/depend/fatfs/documents/res/app1.c | 1135 | `17f99c12e7017ceaf25734165745b5b43b734fdd6fdabf5c8c6a01ec2e778aef` | 0 |
| src/rust/fatfs-sys/depend/fatfs/documents/res/app2.c | 2236 | `11c9bf944aca5e55c7642225e1a59f5998a3dc43a302b6f1c5310e9a4ad1433a` | 0 |
| src/rust/fatfs-sys/depend/fatfs/documents/res/app3.c | 4133 | `e5b1c71593750cda3cb11ca638f75d55e23578515fcebcc7607cb66de4e21bec` | 0 |
| src/rust/fatfs-sys/depend/fatfs/documents/res/app4.c | 10567 | `11ff9994c90bd50a04754f6aae344cd2863b2de142d401ec86f81d9d99232dc9` | 0 |
| src/rust/fatfs-sys/depend/fatfs/documents/res/app5.c | 1411 | `ed551e157dc26a5902e59beba3dabe3052d1cacdb806ccfcefa76a519c9893cc` | 0 |
| src/rust/fatfs-sys/depend/fatfs/documents/res/app6.c | 1974 | `209a05020537c1a63cff1d5a4c48a8510ac05fddce400d2e7f440e721c330b68` | 0 |
| src/rust/fatfs-sys/depend/fatfs/source/diskio.c | 5385 | `435567bf00b4607a803339ec31d9402ea12536cbf65bb65ef9301027f7d38836` | 0 |
| src/rust/fatfs-sys/depend/fatfs/source/diskio.h | 2733 | `1c2b29f53e061c55d43b2e412c3a61320b2621bac7561a05e275514baa44785a` | 0 |
| src/rust/fatfs-sys/depend/fatfs/source/ff.c | 266970 | `58ec7816a45870331b2a9c0eb977db19d1f0d95d7416a1482df07675a402c8a6` | 0 |
| src/rust/fatfs-sys/depend/fatfs/source/ff.h | 17365 | `42920ae4d6080bfc2a72d92a9969b5e94eeaff070e5e71d90da9ab6d7d8e158e` | 0 |
| src/rust/fatfs-sys/depend/fatfs/source/ffconf.h | 12714 | `6dc2ff2adf09b990a5b91eb253543061bd77ed498f92f4887837b35e8ffa5236` | 0 |
| src/rust/fatfs-sys/depend/fatfs/source/ffsystem.c | 6172 | `4ef367d61c6060d2bedeac57985ec293cf29d33faa98d15fbd78c5d63260eac7` | 0 |
| src/rust/fatfs-sys/depend/fatfs/source/ffunicode.c | 1974995 | `3f1632c1f1e64b0b683b0d7e51341b9870728f398604869dd8211f1819509a8e` | 0 |
| src/rust/fatfs-sys/src/lib.rs | 11 | `bdf6c7cf1fc01f69cc1d4e52948d1f246fdd310e6323d5dd1efd23f1daf382ef` | 0 |
| src/rust/rust-toolchain.toml | 178 | `adc23c7a875dbd0c12bae71d2e35f74ef87baf17d0660dd4ec245ea41d14e5ff` | 0 |
| src/rust/streaming-silent-payments/Cargo.toml | 404 | `b7a6dba7cfde137b16a86d3d65157dc965d70835aa6f6ee6cea66dfe2d23b044` | 0 |
| src/rust/streaming-silent-payments/src/hash.rs | 1776 | `ec49885fa0902fafb0b1bbd6ac6e4444aee0a3edb622adbd887f23792b637219` | 0 |
| src/rust/streaming-silent-payments/src/lib.rs | 14461 | `4e33062aad0ad48284857ac80a9b626078474c94ab7901ba3f2c17eedf925488` | 0 |
| src/rust/util/Cargo.toml | 878 | `543d8a138679badb32951a85c9c276ce05fd7ba1ca05952148f1f844e69be7ef` | 0 |
| src/rust/util/src/ascii.rs | 2089 | `fde025eaad4c2af6ae324939a7fdf659c09af403649596354181de113363b640` | 0 |
| src/rust/util/src/bb02_async.rs | 1686 | `6ed61692ba8092d58add3b157ed5eb9cb1fa81dd448f53cf5b56ba7ae025cb21` | 0 |
| src/rust/util/src/bip32.rs | 1412 | `457688519fc8b6a097ccabd27c189b1f6ed218437d8b478e029459d58c781125` | 0 |
| src/rust/util/src/bytes.rs | 7737 | `9e7f5104142dc0fd492bcaf693ebbb2c4bc98a91f19cf3c929b4185f3ce4c5fa` | 0 |
| src/rust/util/src/cell.rs | 1286 | `4fb9bdf81aa82bac48d10dd8ba8b2443e2fd5d523ef6b6275cc09ac5d614b975` | 0 |
| src/rust/util/src/datetime.rs | 3468 | `741a7d3fdce76a0a30d332b29f73f237691783190c06f9c3922b0a532fe0e939` | 0 |
| src/rust/util/src/decimal.rs | 4784 | `01a1b5c401e594edfbbe05a5261deaf57841f8a63c5f762238f07b580db22509` | 0 |
| src/rust/util/src/futures/completion.rs | 3750 | `339f12b2cffad430257aee544aba322fdcdd803a23b52dc443480e22f0988980` | 0 |
| src/rust/util/src/futures.rs | 60 | `8fdafb7122f20d1b5ce988e860031c57512db4fcc1d0a86d01e53777f5c4b0c1` | 0 |
| src/rust/util/src/lib.rs | 2166 | `dbba9c609740021556b8cde831364aa22ae8415addf76f481941ee34c09c2de9` | 0 |
| src/rust/util/src/log.rs | 4249 | `d9b518ed3e5292c284bf90958e551320c39b18c1bf88f79094dedc7ee3698be8` | 0 |
| src/rust/util/src/name.rs | 1558 | `998da04d404cfd53209df659581886544d34ae1a4c314a0c044086f7b837e883` | 0 |
| src/rust/util/src/p256.rs | 3298 | `7662a6309089b842bfba84fb5a187419ef8588678035d9f9766bc456d9ab0185` | 2 |
| src/rust/util/src/sha2.rs | 11704 | `ea2cb924dd5d2189531c80450997fba14624ba4244fc2063ded4b5bf7f4c5648` | 0 |
| src/rust/util/src/strings.rs | 9623 | `bb60b4f1763c9444ff1675b49c130c87ed3394b6ef479589abb168e6ac86b811` | 0 |
| src/screen.c | 3476 | `cfe33ab69a62ae78bf8bd1a52d007ecbe0a2d8799f1917ce5052f259acabaeb5` | 0 |
| src/screen.h | 943 | `35e89291cfb88bbc08bcd4ab8b913e406808ac84fc5a112743ad60eb32775262` | 0 |
| src/sd.c | 10969 | `8dcf171b7d515317a15e17a90a6fb1073bb4175e9eb3561e415aad93c5de6f31` | 0 |
| src/sd.h | 1898 | `c91c4fd60a64f13e33871264bc51668534a51576535f4b39378f24b2f1be79eb` | 0 |
| src/sd_mmc/sd_mmc_ext.c | 698 | `79fb100d033d6068fc812405f98f56ebfdc9536fc350fbc80bec1629e1839fe7` | 0 |
| src/sd_mmc/sd_mmc_ext.h | 206 | `6b4c4b41838ce53d4723c1566344eb30dfa8292e3ff033e33dbc6bed601345d2` | 0 |
| src/sd_mmc/sd_mmc_start.c | 430 | `ffd9c7aa3251780e2374147433d3bad4e01b670ad9b0e6eb0c0c5f59a4fa5659` | 0 |
| src/sd_mmc/sd_mmc_start.h | 51 | `ec31f931047363fac9aee9778d3afc0b523683a9d5b21701c424f062a30a3848` | 0 |
| src/securechip/securechip.h | 2253 | `553fd604572b88af6d037102db994a94ffbf5bab836db0783d439b3d70e6f9be` | 0 |
| src/system.c | 1093 | `b6ff1e7ab0ec14f265f906eaae439977df28d9b9bfe7835aee62a71dfdd792e9` | 0 |
| src/system.h | 262 | `b2188c4cdc59fd46318d22edd41cf2ddfbe25023c3226490c7b2716ca64db2c0` | 0 |
| src/touch/gestures.c | 7780 | `15d289b74f8d1afd120c857425dc1b5614c3aac3bd767564056cad032ee00228` | 0 |
| src/touch/gestures.h | 1036 | `f1431c6bc572c1ff0bb639b596d83bfbda72e30440550db2f7af5b943e45650f` | 0 |
| src/u2f/u2f_app.c | 2770 | `0cdd0a8722f62744d8f89ef5d303b007836f4fb5ab5c70086639149abf965394` | 0 |
| src/u2f/u2f_app.h | 1429 | `4922af347b06b58cf350f854f0e3d824d34c4d6ebbd5252ec37e7dad3bb3877f` | 0 |
| src/u2f/u2f_packet.c | 5265 | `b255472c0baaf4fa28be35ceaf7f367bfac3c144800080815b0ace821daf9c55` | 0 |
| src/u2f/u2f_packet.h | 1048 | `62fec15e5a9779ba29e3876e6979f65a3e9918c7758a467c3099028b64fb8f0e` | 0 |
| src/u2f.c | 32289 | `5f6bfa1e7cc4b94edf3c23fcfe699c74c484856841debe934de3f86abef08ce6` | 0 |
| src/u2f.h | 1076 | `85ee65d73887ef958af72a5495e5134c5619b2db53a1817379c7e90ae2af84e7` | 0 |
| src/uart.c | 3229 | `8a2f1cc8191b42d45b03d0712e73a238b6c1de7bd126d8325cc1b7df7fa123b3` | 0 |
| src/uart.h | 545 | `e43783cf909e54c395b4d4f7b9f8059ec4ee8c99a080ed4acdc9fff84b2c2296` | 0 |
| src/ui/component.h | 1821 | `a07473e0ffc5c839fba5d583fa2a5d543facc81064f087f04b3d79fd2605ccf5` | 0 |
| src/ui/components/button.c | 5022 | `cc451912b4ccd09fed913d03fd0369ad53acaffaf8778e24b9c02889046fbe47` | 0 |
| src/ui/components/button.h | 1399 | `3a1736c1bd6fc90a784a73bf31d7afa16714dbc5c16996049f9aaf1b65d88408` | 0 |
| src/ui/components/confirm.c | 4677 | `ff7fc3bff893ce08e68a27c1a73c3d21a061d03b574d7557dff7ee86e52cd525` | 0 |
| src/ui/components/confirm.h | 1636 | `e8bed0d30352f14a1301317974040fd9a631ffd1193fed5e1e2559a86a91b060` | 0 |
| src/ui/components/confirm_gesture.c | 4737 | `b74d570fd5e75f68404265f705fe36fdfd0b611122732ec21c458df31dd8edb9` | 0 |
| src/ui/components/confirm_gesture.h | 493 | `447f87d9695c6941ad76066593024fd4128ccf286db7ea105b9be27031c09c4c` | 0 |
| src/ui/components/confirm_swap.c | 3118 | `e54acf522bfd2eea84a76be00993c645a92995312eb3b385fa97f68215f76fa8` | 0 |
| src/ui/components/confirm_swap.h | 686 | `7a4a9ffc3cd075256c6135bf9436a36e4b0e492eced8187af5d9af66f17d01ce` | 0 |
| src/ui/components/confirm_transaction.c | 4813 | `810d55e494198ee188e15aa696d2354c6ef6041fa79181d385dc74d96cd37643` | 0 |
| src/ui/components/confirm_transaction.h | 1200 | `61f867ffb8af1557dc717e5b667f5f52ed7d4ce2255ec8f2ed591f6dc5fa0936` | 0 |
| src/ui/components/empty.c | 679 | `cd1c8fc5e607e841c9d92235e2ebcfba6c8cbcd6425cb39060f2d8040ef34ffe` | 0 |
| src/ui/components/empty.h | 225 | `6c17f7e1f19f22a91275f7c6093def976bd7de8c997ac927ffd7fc10a1705656` | 0 |
| src/ui/components/icon_button.c | 5054 | `ecb4e2b2970c787c8db7deed590b4633ffa6f100c7b86bae5d7520e54b481bea` | 0 |
| src/ui/components/icon_button.h | 616 | `4ee6d9866e86b07ca04465d3164b8773d83bedc6752cb856ed25ee1652a2eec5` | 0 |
| src/ui/components/image.c | 2682 | `9000e883ffc7ddc70e34bc49bf145bc31eb3af716ec6ef9b79e42fdbbcca8b38` | 0 |
| src/ui/components/image.h | 753 | `f749e5a75baf96d686d30acccfb1b1c4d739353799d340ced306c8be48dac2e8` | 0 |
| src/ui/components/info_centered.c | 1662 | `be0d954ae5733ed1ea1eb5fe759236704a98e246c45f9b067719068d76b8c956` | 0 |
| src/ui/components/info_centered.h | 550 | `2cc0857e51f6966a3225bb5796e8e1295f8d5bd92154a16244d548974617bb95` | 0 |
| src/ui/components/keyboard_switch.c | 5153 | `4ee1d5a0b16f35b8e986e3d16cb50086340db1c5a665c4fbf79f2e7e7938c536` | 0 |
| src/ui/components/keyboard_switch.h | 958 | `78786a829330eaf101021614d0f9aa94d76319965e16ef37e165393a0a71ee58` | 0 |
| src/ui/components/knight_rider.c | 1836 | `e227df5a99bfb0fb90159492462438e4871b089d96f676ae0cef2194db397a0d` | 0 |
| src/ui/components/knight_rider.h | 425 | `5b38b3b1f8a035e4446c84eda0a9a305cb80b80f1d7ef7bc89208213cb6af382` | 0 |
| src/ui/components/label.c | 8871 | `208edee08788d00a3ccdde38fcb505a6279b0a90c7cefd00bafcbd803412e23d` | 0 |
| src/ui/components/label.h | 3426 | `f135077b533da03cc075498e897570a3f0161bef23aa48864becb5977167bac0` | 0 |
| src/ui/components/left_arrow.c | 3444 | `09d2d637d63f8a5c6c61ec0c6276d7f2f6fa97b23d58a6582af3f21569efc5e0` | 0 |
| src/ui/components/left_arrow.h | 511 | `3196849704e2eba89ba6c5ea85f0ea13127dd1081445818ec9fa409d046730f5` | 0 |
| src/ui/components/lockscreen.c | 3456 | `199c5bd8d11f4aece24ca0ec834764cf799cb2db3175fee5bb89ece21f7c5db7` | 0 |
| src/ui/components/lockscreen.h | 223 | `900e7f56572d6f06caec37d075aa969818a165ccaa7c5bc4b917362560dcd34c` | 0 |
| src/ui/components/menu.c | 9273 | `21ebdaac62d659f4a8019c82ab870e764626fa348923a3231e59d111ed115ef1` | 0 |
| src/ui/components/menu.h | 1345 | `706c6ff3f2345513b3c10cff0806c5b85b27cb4a35c087d80716fff790912a99` | 0 |
| src/ui/components/orientation_arrows.c | 6207 | `71686192af175d7e295191e46879b26be6b44c59ed696329cc1530467fa608b5` | 0 |
| src/ui/components/orientation_arrows.h | 530 | `1bf76607ee6050cffed3efe2faa9a9e8ad81190411f803ee0dac28d273ab8544` | 0 |
| src/ui/components/progress.c | 1648 | `947e90bc3a27026e979ce9f48f5ed71c30d9e62e11449c27ef72dc60a3eebc37` | 0 |
| src/ui/components/progress.h | 402 | `8232044dd9aef38e46af994c30c99b30303d61f2d6c8ec442d3ec45f7bfcb9b9` | 0 |
| src/ui/components/right_arrow.c | 3650 | `83a10b58ca690de826c330750f2e24a09eebe43a5390a304236078e97cc1dfcc` | 0 |
| src/ui/components/right_arrow.h | 515 | `8ba6ea528f44d08b61d363e81d5f65d2caca802205d89c8b18df130ef736eddb` | 0 |
| src/ui/components/screensaver.c | 3122 | `474414d341c7f942ca9435d3eef090a1e4d0cc6bd507eacd20fb4e9584b5d75d` | 0 |
| src/ui/components/screensaver.h | 375 | `7ec6bd40c73af2d8f8fb5cf196568acfed60b2979463df6cc9c590d7bd42a62d` | 0 |
| src/ui/components/sdcard.c | 2748 | `8c319b47b9d4c4041cafdf47c7094e2ff5daadc6b7d522e977ebd6b1fb937f30` | 0 |
| src/ui/components/sdcard.h | 389 | `2287aa5eced8006a9e9b407923b89841de7cc505a78bb84ec5372a51c4f3b89d` | 0 |
| src/ui/components/status.c | 1672 | `56d47212b55dd91f6cc887b1a1d877ebc8a8f6d3a4f778aa37ee5939fed34041` | 0 |
| src/ui/components/status.h | 507 | `afa759656dc103c185a053bf5ec2643fc5a7f3df5464ab170938b6cf217467c3` | 0 |
| src/ui/components/trinary_choice.c | 3257 | `4b7f85ae36693ca5a89323187fb542474277fed672670351e5ea096b38868688` | 0 |
| src/ui/components/trinary_choice.h | 905 | `86a614340e27105664d95ae72c1579823cdacad01250dcb35aa2495a2dcf477e` | 0 |
| src/ui/components/trinary_input_char.c | 14903 | `bc419ea37ed53cfb0c960c2aecde3c9b040ad7aa5e07081116e8f0eeda293ed2` | 0 |
| src/ui/components/trinary_input_char.h | 1663 | `ed246da425389a34d86d366639ce4a8ca5a1b8b93458de5b4a6f39c736ac6b35` | 0 |
| src/ui/components/trinary_input_string.c | 18762 | `c565e0b6e2e4f32072a611c257b76f29d20efb27aea23a38c26672a6a14bbad9` | 0 |
| src/ui/components/trinary_input_string.h | 2123 | `d7c341feef38c0723581490bcc465a243460a5085792d83baad8f32e17281d0d` | 0 |
| src/ui/components/ui_images.c | 14893 | `38788e6b993403db59eb8b9675c05c5b5f82ef12f9d059491b98dac29e3b1c36` | 0 |
| src/ui/components/ui_images.h | 1814 | `9d0d48dc2a867a42c1c1f8935d6964906f18c509b5183d9ef5f18b8e7027a6e2` | 0 |
| src/ui/components/unlock_animation.c | 10949 | `8cfedb0276426a8b6ad17cc94382d747285b74e95c820cb0b8a1f9cd62322bd1` | 0 |
| src/ui/components/unlock_animation.h | 269 | `031cb5d1a4a989b037b9c91785b7128f7e4a02621c4bb72973eb80e60ffd7221` | 0 |
| src/ui/components/waiting.c | 2901 | `876058da24e77fa58c9f4799480b7def7ffcd96bc3b80d5705fc74d140ba8fb6` | 0 |
| src/ui/components/waiting.h | 611 | `0c497151feb5ed87172f218a79524b725ba06c6b8ad2dac99e9123988313514d` | 0 |
| src/ui/event.h | 563 | `ceb3e26bfa9d5441f571eb846273ecade740f6b1353311ce55e990dd5e659779` | 0 |
| src/ui/event_handler.c | 1520 | `7e183e8ce31c33254a45ec1a02e2fd7d3fb91e69bb1cef7e5e190030fb08dea9` | 0 |
| src/ui/event_handler.h | 267 | `43ec16c77d45de807db6cd8a50463e1fc7bc4a79443493973eaccd70ce019467` | 0 |
| src/ui/fonts/inter_bold_32.c | 220230 | `a1b38b3f0de200baeff70ca8d4342fd1e003c319b455b3bd8797a524470ada2a` | 0 |
| src/ui/fonts/inter_bold_48.c | 477264 | `8f262bd976dddec9c9fc69fb6cbedad692ef7fb05ebc10219aecbbf743214621` | 0 |
| src/ui/fonts/inter_medium_20.c | 109924 | `6d2067839ae61ff2ceb6c4b85da0025bc8baffe5462486e46bf555412769c08e` | 0 |
| src/ui/fonts/inter_medium_32.c | 218261 | `9445298cfc9ce4141e95c867e65aaf87a5cd2a5c6d6ae71ffae4b0689c8f9fe3` | 0 |
| src/ui/fonts/inter_regular_24.c | 130640 | `0f898381eda14ad4bf04eb3d1eca09bae336e85b0c35565ca06a719653ef0ac4` | 0 |
| src/ui/fonts/inter_regular_32.c | 195082 | `14680f1a8e90933a0d6d84e0e8760548cc3a456392c5703a3dc9de8053f1fd18` | 0 |
| src/ui/fonts/inter_regular_48.c | 416631 | `fa6169cb2efdf02dd8ba3dc4642001d1e5efcc24ede28723902003fc653c97d1` | 0 |
| src/ui/fonts/lvgl.h | 391 | `11c17c628828fa80cf4d76e36e738c309ee0e5bd18344dd8175625733c54ac68` | 0 |
| src/ui/fonts/lvgl_font_compat.c | 3435 | `67a8045562eb177d9798515529acd8c3927cd7045953c9960e8b7c35a1c991c2` | 0 |
| src/ui/fonts/monogram_16.c | 16168 | `a0e5970175aaeabbac7299cadbb545920af1f31d076539c44d0ff0bc4e7649a3` | 0 |
| src/ui/fonts/monogram_16.h | 158 | `9c1f589005022ab443d2e0320d282e4aa4c5799b3d255fab19a8df68d2d4c426` | 0 |
| src/ui/fonts/monogram_16_bootloader.c | 4840 | `5de1f46de5c48efdb1ee97ddde36b48ab68c1dd84ed87d92795c461a71c77fc4` | 0 |
| src/ui/fonts/monogram_16_bootloader.h | 191 | `be9c3f187d51c4c9d06de25ef871450fec51b85ee964da350ec7babc30f64d67` | 0 |
| src/ui/fonts/password_12.c | 1405 | `3e9db0e36887259c555fe1ba6393ef9efa4f66c8f7bcb9daca4d13f66fbb724e` | 0 |
| src/ui/fonts/password_12.h | 198 | `c52f920e705997665f8d6a6a14cf4071f8953dae7f047ee8781bf40b29898369` | 0 |
| src/ui/fonts/password_9.c | 1388 | `b089160d8076d8b1b0fec785e8ad9e17870aaaebd543a44ce40598a0f9cda800` | 0 |
| src/ui/fonts/password_9.h | 154 | `90f8f69a18d7dc70b40620af8974468d44b61f899f6db6139ba61f0f4676910b` | 0 |
| src/ui/fonts/regular_11.c | 32527 | `7b364b0fc185ca3f17222133fea1ce2ea7551077cdabdeb1e9a404f7f9f1d4d5` | 0 |
| src/ui/fonts/regular_11.h | 154 | `0a98c23bac34f471d61acf4fa92a2c837e07806433ca95aa131eb5086c6b8835` | 0 |
| src/ui/fonts/regular_12.c | 33621 | `061359ab0984d07b83e698f7cec0082d786731378f288b383fd8710f418a946f` | 0 |
| src/ui/fonts/regular_12.h | 154 | `c284235a85a0a20cbe2546d488d6588be37e6df1b84e6d780d293f646813cb9a` | 0 |
| src/ui/fonts/regular_9.c | 31381 | `7aaab51be31de788729c9fe46ec4024079fe1bbf7fb5f389c064af8e0eb91a31` | 0 |
| src/ui/fonts/regular_9.h | 150 | `98f7215d5be8c70c3cc3aa8e97184a5f391201367c8b73d7a3ccc56b1f528af3` | 0 |
| src/ui/fonts/regular_9_bootloader.c | 15876 | `5453ccee1557b14014c4b4a7ab57004ab4b814d98f454bd04756ae80a7b2dae2` | 0 |
| src/ui/fonts/regular_9_bootloader.h | 183 | `e1d321850785b1cf43e041776fb84f961f042c34baf1809870e1a716ad1483e6` | 0 |
| src/ui/fonts/regular_fonts.h | 197 | `8a8e025aa12cff224593361e93ac0b80822f17945e297ba5271c0cbbbff12580` | 0 |
| src/ui/graphics/graphics.c | 700 | `04b7f519cfb183a24fe900af85577a43332d093b5602cab775604fe2979e2920` | 0 |
| src/ui/graphics/graphics.h | 496 | `a4ce7700e842555679eb3e4413370cefa48cd2a27861e272f5e0c0bd64fbba96` | 0 |
| src/ui/oled/oled.c | 4379 | `ed7a0ba91c16163d3b5b8cd5dbba05d155c6cc8f2a46d812775324ab03a88757` | 0 |
| src/ui/oled/oled.h | 2770 | `11bc1ea771b107fc399ab5830fc6a542d1b85f8f41dad91abe2d870bcf2ec96c` | 0 |
| src/ui/oled/oled_writer.c | 1290 | `1e49807ebed8391f58f225bc0e3ddbc5bc47a8be969e00ffb18f8aea69c96840` | 0 |
| src/ui/oled/oled_writer.h | 436 | `484da60c1c4ace43f60680ab6067265cb3201962065648c3475b8a2f04be65c4` | 0 |
| src/ui/oled/sh1107.c | 4742 | `4cdbdd49fb69f9a9ae925988c4bbfc477e61fd884492347a09375e665e1de17c` | 0 |
| src/ui/oled/sh1107.h | 424 | `6f11af7cd69de4fccf04a5ca441b9d39c7b4c40f06bc9937ec17283af768348c` | 0 |
| src/ui/oled/ssd1312.c | 4806 | `c229caef4b0b9f99872bdf2b6015d38a180a85f9aa248521c490262ca2fb1173` | 0 |
| src/ui/oled/ssd1312.h | 412 | `7e80fa18a1ff73103d7420dc2f8e028b1746d879739f49dbcc264c27821e6b9a` | 0 |
| src/ui/screen_process.c | 2920 | `c797a0a0dd7f8a7519bcc53fcefb344d5b5fb78baf2691d3c40e655197e9107a` | 0 |
| src/ui/screen_process.h | 1324 | `4925324ae565ea56f3b245de7e65211ba042e42d3ca1f08f9959f59a26302bbf` | 0 |
| src/ui/screen_saver.c | 1605 | `e5d01795a1d6c770a03cd378030fb5badf2394bd018ed5b839dd4913f299ef7e` | 0 |
| src/ui/screen_saver.h | 841 | `6d9596bf239ce5933c80ceaaf9ea6f1e8072a6abb18ced3780aa21d32ac4628f` | 0 |
| src/ui/screen_stack.c | 2027 | `197e7ea15e96db7fd131ea244c960a3d4832517ebd3f0a3d79d3a64af3042241` | 0 |
| src/ui/screen_stack.h | 541 | `15906232878e5958c681a35ed055844d98b3dd1aac15978929c8736e47fcb6ae` | 0 |
| src/ui/ugui/ugui.c | 24444 | `220bfa84f9ce74facbe56797bb218cb57d22c4bf009f083cf8a3dc5cd03a695f` | 0 |
| src/ui/ugui/ugui.h | 5912 | `d6faaeecf2aa46263906f5ac5a062b10e74583c75a783dd0f3ebee5cc98627d0` | 0 |
| src/ui/ui_util.c | 8629 | `9de60147f2cb3098e19bfff7bca0b9d88c5aa3a48e1f004ea14f57d02dd4aae4` | 0 |
| src/ui/ui_util.h | 5096 | `c27d10d4029d2bb1093a8a9c119157e89d60f49a3d3b9c78c7f896525767a2f2` | 0 |
| src/usb/class/hid/hid.c | 11109 | `bcd4ce1b19d1124edb7e01ef42f03e770287cf5d1657bc6d20775a084f958019` | 0 |
| src/usb/class/hid/hid.h | 4109 | `577de80520fb227d0c59d54cbee8b7e2a433255b9d57b63e02de85666d087e0f` | 0 |
| src/usb/class/hid/hww/hid_hww.c | 4754 | `6386782800379810d5b871a51d656181425832582fe7186513a0d7cd894bc042` | 0 |
| src/usb/class/hid/hww/hid_hww.h | 1709 | `c55cc67135f87e9364a8b27a1cbc8c9c1c1c532c1f483357194be370fb74fb3c` | 0 |
| src/usb/class/hid/u2f/hid_u2f.c | 5262 | `ce8506310c076ae0cb615c00b78afab8d9958f9cbc5de15cfc7e7bd32ab55cb5` | 0 |
| src/usb/class/hid/u2f/hid_u2f.h | 1623 | `bcec43c5c70c6eefbbdc8d1e6005860562c9af74c9bda31084b76fd16266ec5d` | 0 |
| src/usb/class/usb_desc.h | 7046 | `5065da9afd04d585483cb4bb706a6ecfd53e3504c5a96c757959f36385d9c377` | 0 |
| src/usb/class/usb_desc_bitbox02plus.h | 5016 | `4538dd98aad944ad1a79ef1004234c299475cb6fe215ad3f4bc62b10a294172b` | 0 |
| src/usb/class/usb_desc_common.h | 6509 | `f81e45537c09af04b33ff8a5705458630940f4ab89805dad0b68b2f5567ea801` | 0 |
| src/usb/class/usb_size.h | 166 | `f9ec0deac44a546890d03fd364d6f7c30337cf3af0bf10b8dfd544210082621d` | 0 |
| src/usb/class/usb_u2f_desc.h | 3758 | `6d7dd70956c39337cceb388e23a971840d5d4dd1e6aac0907fb2184b52fa1b50` | 0 |
| src/usb/u2f/u2f.h | 3133 | `d76b09a8fb63da8ecf6b6490b165c20005247b9b1a0c391070c60e030a42b63e` | 0 |
| src/usb/u2f/u2f_hid.h | 2982 | `66976af1f1a767ae9c7e4632d530cfbe0e7849e4acdeb2c13d020dede7ecee9c` | 0 |
| src/usb/u2f/u2f_keys.h | 2313 | `a162f73d950ca857744d864a07e27d90dd9f78c0be9ddc86114a2d1ae22ff97b` | 0 |
| src/usb/usb.c | 3090 | `0d427e3fb7ab2dbba2b65367e70ae6d2017d9c8ff3191109467c9edb7890564e` | 0 |
| src/usb/usb.h | 275 | `f40df9cad0283326621b13dae6dd0027f43acb95ce640f28c7e6914a8d2fa809` | 0 |
| src/usb/usb_frame.c | 5540 | `92d3fe3c443ca9989db2f96c976a931517c41394342bd98f314d1d3c215c78b0` | 0 |
| src/usb/usb_frame.h | 4220 | `b4e0030db88b0911f7ee8a8ffa623a6bd470b0eb543eb7b4422ce6b507d3737d` | 0 |
| src/usb/usb_packet.c | 3034 | `a08a57316ff2a59ced1b13b2518bfc12ba116b19feede5d5e147e73a8fab2db1` | 0 |
| src/usb/usb_packet.h | 865 | `7d2d02d5d55c31764bd99c5585730cbbf2baf6442fcd63ccae826284baee801a` | 0 |
| src/usb/usb_processing.c | 13698 | `e62fb4705df80476c55490f83bd3889603916eca52be3a6cd3a80ca7794e4645` | 0 |
| src/usb/usb_processing.h | 2167 | `b13ab589a15524572845e28b92af5bcd1757e9bad4fa92d7e74d5a75c1fe1e27` | 0 |
| src/util.c | 3410 | `c89f4e11e0a50684fd7986a85a7d84749b53f7870b6e89c7d88326f2c3192452` | 0 |
| src/util.h | 5262 | `8bfcd192ef4b5709bdc647646e9e595c2aefd6dbcd94fa79a84c13161992183b` | 0 |
