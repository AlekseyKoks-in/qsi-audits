# Post-quantum cryptography review: embit @ 2b375a33bd89

*One-page brief* · Reviewed: 2026-11-06 14:41 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: embit (SeedSigner, Krux) — public repository (passive review)

Source: https://github.com/diybitcoinhardware/embit/tree/2b375a33bd8926caec7e53d7cfd41b165d196566

**Post-quantum maturity:** Level 0 of 4 — no post-quantum cryptography. **Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

**Findings:** Critical 0 · High 1 · Medium 6 · Low 0 · Info 1

**Quantum timeline (Mosca: x + y − z):** Key establishment 10 + 5 − 8 = 7 → too late; Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **High** · Non-cryptographic generator next to key or seed generation in src/embit/util/key.py (QSI-2026-19301) · *preliminary*\
   What to do: Use the platform CSPRNG (secrets, os.urandom, crypto.getRandomValues, crypto/rand, SecureRandom, OsRng) or a hardware TRNG for every key…
2. **Medium** · Quantum-vulnerable ECDSA: transaction and message signing (31 file(s)) (QSI-2026-19294) · *confirmed by the analyst*\
   What to do: Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains…
3. **Medium** · Quantum-vulnerable Pedersen commitment: threshold signing and MPC protocols (4 file(s)) (QSI-2026-19296) · *confirmed by the analyst*\
   What to do: Track post-quantum threshold signatures (NIST IR 8214C) and keep the protocol layer ready to swap the signature scheme; record which keys…
4. **Medium** · Quantum-vulnerable Schnorr (BIP-340): transaction and message signing (7 file(s)) (QSI-2026-19299) · *confirmed by the analyst*\
   What to do: Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains…

3 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · threshold signing and MPC protocols | Pedersen commitment | Track post-quantum threshold signatures (NIST IR 8214C) and keep the protocol layer ready to swap the… |
| **Medium** · transaction and message signing | ECDSA, Schnorr (BIP-340) | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum… |
| **Medium** · role not determined | ECDH, ECDSA, Schnorr (BIP-340) | Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205)… |

Analyst review: 4 confirmed, 1 not applicable, 1 dismissed as false positives. (QSI review, 2026-10-29)

---

Static review of source code and manifests; files analysed: 140. No requests were sent to the owner's systems.

Full report, content SHA-256: `975014859df9799ae59da5cc65b2b30339130f43b00e8d160ae659839b707716`

Full report signature (report.sig.json): Ed25519 key, SHA-256 fingerprint `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.