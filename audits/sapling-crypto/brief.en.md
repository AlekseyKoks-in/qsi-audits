# Post-quantum cryptography review: sapling-crypto @ 88a7946b4a30

*One-page brief* · Reviewed: 2026-10-29 23:02 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: Electric Coin Company (Zcash) — public repository (passive review)

Source: https://github.com/zcash/sapling-crypto/tree/88a7946b4a3066787776e11f0a502654167e022d

**Post-quantum maturity:** Level 0 of 4 — no post-quantum cryptography. **Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

**Findings:** Critical 0 · High 0 · Medium 4 · Low 2 · Info 3

**Quantum timeline (Mosca: x + y − z):** Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **Medium** · Quantum-vulnerable Pedersen commitment: threshold signing and MPC protocols (19 file(s)) (QSI-2026-06993) · *preliminary*\
   What to do: Track post-quantum threshold signatures (NIST IR 8214C) and keep the protocol layer ready to swap the signature scheme; record which keys…
2. **Medium** · Quantum-vulnerable BLS12-381: threshold signing and MPC protocols (1 file(s)) (QSI-2026-06996) · *preliminary*\
   What to do: Track post-quantum threshold signatures (NIST IR 8214C) and keep the protocol layer ready to swap the signature scheme; record which keys…
3. **Medium** · Quantum-vulnerable RedDSA: role not determined (2 file(s)) (QSI-2026-06994) · *preliminary*\
   What to do: Classify each usage, record data lifetimes, and plan migration to a post-quantum algorithm; introduce an abstraction layer for…
4. **Medium** · Quantum-vulnerable BLS12-381: role not determined (13 file(s)) (QSI-2026-06995) · *preliminary*\
   What to do: Classify each usage, record data lifetimes, and plan migration to a post-quantum algorithm; introduce an abstraction layer for…

2 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · threshold signing and MPC protocols | Pedersen commitment, BLS12-381 | Track post-quantum threshold signatures (NIST IR 8214C) and keep the protocol layer ready to swap the… |
| **Medium** · role not determined | BLS12-381, RedDSA | Classify each usage, record data lifetimes, and plan migration to a post-quantum algorithm; introduce an… |

## Known vulnerable components

Advisories for the versions in use: 2; each needs checking against the code.

---

Static review of source code and manifests; files analysed: 37. No requests were sent to the owner's systems.

Full report, content SHA-256: `121c19c60c0efe8d69737aefe8bbd6df5eb0867316cb975e81ab39f95de3b3c2`

Full report signature (report.sig.json): Ed25519 key, SHA-256 fingerprint `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.