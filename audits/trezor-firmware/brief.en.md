# Post-quantum cryptography review: trezor-firmware @ 72489948b3c4

*One-page brief* · Reviewed: 2026-10-29 05:57 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: SatoshiLabs (Trezor) — public repository (passive review)

Source: https://github.com/trezor/trezor-firmware/tree/72489948b3c44a37598de9da658be28e4fabb4ae

**Post-quantum maturity:** Level 3 of 4 — hybrid protection in a critical path. **Next step:** Cover the remaining classical critical roles and plan when the classical half can be dropped.

**Findings:** Critical 0 · High 0 · Medium 11 · Low 0 · Info 0

**Quantum timeline (Mosca: x + y − z):** Key establishment 10 + 5 − 8 = 7 → too late; Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **Medium** · Transaction signing for 11 chain(s) relies on elliptic-curve signatures (QSI-2026-06455) · *confirmed by the analyst*\
   What to do: Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains…
2. **Medium** · Quantum-vulnerable Ed25519: firmware and boot verification (root of trust) (2 file(s)) (QSI-2026-06445) · *confirmed by the analyst*\
   What to do: Plan a hybrid firmware signature (the classical one plus ML-DSA or SLH-DSA, both required) and the path to ship the new keys in a…
3. **Medium** · Quantum-vulnerable X25519: channel key exchange (TLS, Noise, handshakes) (3 file(s)) (QSI-2026-06447) · *confirmed by the analyst*\
   What to do: Move the handshake to a hybrid key exchange (X25519MLKEM768 in TLS 1.3; a hybrid KEM in Noise-based protocols).
4. **Medium** · Quantum-vulnerable ECDSA: transaction and message signing (4 file(s)) (QSI-2026-06448) · *confirmed by the analyst*\
   What to do: Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains…

7 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · firmware and boot verification (root of trust) | Ed25519 | Plan a hybrid firmware signature (the classical one plus ML-DSA or SLH-DSA, both required) and the path to… |
| **Medium** · channel key exchange (TLS, Noise, handshakes) | X25519 | Move the handshake to a hybrid key exchange (X25519MLKEM768 in TLS 1.3; a hybrid KEM in Noise-based protocols) |
| **Medium** · transaction and message signing | ECDSA, Ed25519, Schnorr (BIP-340) | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum… |
| **Medium** · authentication and identity (certificates, tokens, device attestation) | ECDSA | Keep credentials short-lived and plan ML-DSA certificates, tokens and keys as the ecosystem supports them |

Analyst review: 11 confirmed, 0 not applicable, 0 dismissed as false positives. (QSI review, 2026-10-28)

---

Static review of source code and manifests; files analysed: 411. No requests were sent to the owner's systems.

Full report, content SHA-256: `2f06e710722b156693133d030295730454268f4b264bec15de9be2d6b01e7502`

Full report signature (report.sig.json): Ed25519 key, SHA-256 fingerprint `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.