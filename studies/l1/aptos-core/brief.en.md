# Post-quantum cryptography review: aptos-core @ 81d89f428fe8

*One-page brief* · Reviewed: 2026-11-06 16:20 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: Aptos Labs — public repository (passive review)

Source: https://github.com/aptos-labs/aptos-core/tree/81d89f428fe8e4b69d53b4916993e9a930afc37c

**Post-quantum maturity:** Level 2 of 4 — post-quantum in use outside the critical paths. **Next step:** Extend post-quantum protection to the critical roles that stay classical, starting with what can be recorded today (wrapped keys, channel key exchange).

**Findings:** Critical 0 · High 0 · Medium 9 · Low 0 · Info 0

**Quantum timeline (Mosca: x + y − z):** Key establishment 10 + 5 − 8 = 7 → too late; Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **Medium** · Quantum-vulnerable BLS12-381: transaction and message signing (2 file(s)) (QSI-2026-19659) · *preliminary*\
   What to do: Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains…
2. **Medium** · Quantum-vulnerable Ed25519: transaction and message signing (10 file(s)) (QSI-2026-19660) · *preliminary*\
   What to do: Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains…
3. **Medium** · Quantum-vulnerable X25519: channel key exchange (TLS, Noise, handshakes) (2 file(s)) (QSI-2026-19662) · *preliminary*\
   What to do: Move the handshake to a hybrid key exchange (X25519MLKEM768 in TLS 1.3; a hybrid KEM in Noise-based protocols).
4. **Medium** · Quantum-vulnerable ECDSA: transaction and message signing (3 file(s)) (QSI-2026-19663) · *preliminary*\
   What to do: Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains…

5 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · channel key exchange (TLS, Noise, handshakes) | X25519 | Move the handshake to a hybrid key exchange (X25519MLKEM768 in TLS 1.3; a hybrid KEM in Noise-based protocols) |
| **Medium** · transaction and message signing | Ed25519, ECDSA, BLS12-381, BN254 (alt_bn128) | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum… |
| **Medium** · role not determined | BN254 (alt_bn128), Ed25519, X25519, RSA | Classify each usage, record data lifetimes, and plan migration to Hybrid key establishment with ML-KEM (FIPS… |

---

Static review of source code and manifests; files analysed: 336. No requests were sent to the owner's systems.

Full report, content SHA-256: `496bbf2c0ceaa6407d995b8152ee8fd44f8f95ed1f641fbd08068a5bb313751f`

Full report signature (report.sig.json): Ed25519 key, SHA-256 fingerprint `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.