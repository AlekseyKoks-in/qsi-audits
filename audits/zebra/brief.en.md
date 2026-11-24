# Post-quantum cryptography review: zebra @ 147a6a8bf7d3

*One-page brief* · Reviewed: 2026-11-24 11:41 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: Zcash Foundation — public repository (passive review)

Source: https://github.com/ZcashFoundation/zebra/tree/147a6a8bf7d3b1427a9c0557f284d5bfa7b0e522

**Post-quantum maturity:** Level 0 of 4 — no post-quantum cryptography. **Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

**Findings:** Critical 0 · High 2 · Medium 14 · Low 11 · Info 8 (of them advisories unlikely to apply: 2)

**Quantum timeline (Mosca: x + y − z):** Key establishment 10 + 5 − 8 = 7 → too late; Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **High** · quinn-proto 0.11.16 is affected by RUSTSEC-2026-0340 (QSI-2026-49789)\
   What to do: Upgrade to a fixed version (0.11.18).
2. **Medium** · Quantum-vulnerable Ed25519 key (Ed25519) in SECURITY.md (QSI-2026-49765)\
   What to do: Inventory and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it..
3. **Medium** · Quantum-vulnerable Sinsemilla: key wrapping and data encryption at rest (1 file(s)) (QSI-2026-49770) · *preliminary*\
   What to do: Wrap keys with ML-KEM or a hybrid KEM (X25519 + ML-KEM-768) and re-wrap the stored keys; data that may already have been copied needs its…
4. **Medium** · Quantum-vulnerable Pedersen commitment: threshold signing and MPC protocols (12 file(s)) (QSI-2026-49767) · *preliminary*\
   What to do: Track post-quantum threshold signatures (NIST IR 8214C) and keep the protocol layer ready to swap the signature scheme; record which keys…

23 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · key wrapping and data encryption at rest | Sinsemilla | Wrap keys with ML-KEM or a hybrid KEM (X25519 + ML-KEM-768) and re-wrap the stored keys; data that may… |
| **Medium** · threshold signing and MPC protocols | Pedersen commitment | Track post-quantum threshold signatures (NIST IR 8214C) and keep the protocol layer ready to swap the… |
| **Medium** · transaction and message signing | Ed25519, Halo 2 (IPA), RedDSA | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum… |
| **Medium** · role not determined | Halo 2 (IPA), RedDSA, Sinsemilla, X25519 … | Classify each usage, record data lifetimes, and plan migration to a post-quantum algorithm; introduce an… |

## Known vulnerable components

Advisories for the versions in use: 15; unlikely to apply to this build: 2 (no call path to the affected code, a module only tests use, functions not named in the code, a Cargo feature that is off or a platform not built); to review: 13.

Analyst review: 0 confirmed, 0 not applicable, 0 dismissed as false positives. (QSI review, 2026-10-23)

---

Static review of source code and manifests; files analysed: 437. No requests were sent to the owner's systems.

Full report, content SHA-256: `90199a527c8c6652c5e50afdb3cc8c73fc7c8a8bbc01a2488c3b1f5d82f5a446`

Full report signature (report.sig.json): Ed25519 key, then the ML-DSA-65 one where it co-signs, SHA-256 fingerprints `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e · ML-DSA-65 dbd4e297b3213d1d7577a565e76de14cc5ad0e409f1dc68291c67266fc95066a`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.