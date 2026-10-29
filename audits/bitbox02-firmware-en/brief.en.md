# Post-quantum cryptography review: bitbox02-firmware-en @ ae548ef4e40f

*One-page brief* · Reviewed: 2026-10-29 05:31 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: BitBox (Shift Crypto) — public repository (passive review)

Source: https://github.com/BitBoxSwiss/bitbox02-firmware/tree/ae548ef4e40f548a17542ba457f138db4fa0069d

**Post-quantum maturity:** Level 0 of 4 — no post-quantum cryptography. **Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

**Findings:** Critical 0 · High 0 · Medium 11 · Low 0 · Info 6

**Quantum timeline (Mosca: x + y − z):** Key establishment 10 + 5 − 8 = 7 → too late; Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **Medium** · Transaction signing for 3 chain(s) relies on elliptic-curve signatures (QSI-2026-06382) · *confirmed by the analyst*\
   What to do: Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains…
2. **Medium** · Quantum-vulnerable ECDSA: firmware and boot verification (root of trust) (3 file(s)) (QSI-2026-06373) · *confirmed by the analyst*\
   What to do: Plan a hybrid firmware signature (the classical one plus ML-DSA or SLH-DSA, both required) and the path to ship the new keys in a…
3. **Medium** · Quantum-vulnerable X25519: key wrapping and data encryption at rest (1 file(s)) (QSI-2026-06379) · *confirmed by the analyst*\
   What to do: Wrap keys with ML-KEM or a hybrid KEM (X25519 + ML-KEM-768) and re-wrap the stored keys; data that may already have been copied needs its…
4. **Medium** · Quantum-vulnerable X25519: channel key exchange (TLS, Noise, handshakes) (3 file(s)) (QSI-2026-06375) · *confirmed by the analyst*\
   What to do: Move the handshake to a hybrid key exchange (X25519MLKEM768 in TLS 1.3; a hybrid KEM in Noise-based protocols).

7 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · firmware and boot verification (root of trust) | ECDSA | Plan a hybrid firmware signature (the classical one plus ML-DSA or SLH-DSA, both required) and the path to… |
| **Medium** · key wrapping and data encryption at rest | X25519 | Wrap keys with ML-KEM or a hybrid KEM (X25519 + ML-KEM-768) and re-wrap the stored keys; data that may… |
| **Medium** · channel key exchange (TLS, Noise, handshakes) | X25519 | Move the handshake to a hybrid key exchange (X25519MLKEM768 in TLS 1.3; a hybrid KEM in Noise-based protocols) |
| **Medium** · transaction and message signing | ECDSA, Schnorr (BIP-340), Ed25519 | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum… |

## Known vulnerable components

Advisories for the versions in use: 4; unlikely to apply to this build: 4 (a Cargo feature that is off, affected functions not named in the code, or a platform that is not built); to review: 0.

Analyst review: 12 confirmed, 5 not applicable, 0 dismissed as false positives. (QSI review, 2026-10-28)

---

Static review of source code and manifests; files analysed: 721. No requests were sent to the owner's systems.

Full report, content SHA-256: `0f265adc21c8c990d44fbf098fcee7eebde1b04c28396bf07b7094b1e54e848b`

Full report signature (report.sig.json): Ed25519 key, SHA-256 fingerprint `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.