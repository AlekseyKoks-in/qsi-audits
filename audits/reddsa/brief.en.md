# Post-quantum cryptography review: reddsa @ 04e973bcf8d4

*One-page brief* · Reviewed: 2026-10-29 23:42 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: Zcash Foundation — public repository (passive review)

Source: https://github.com/ZcashFoundation/reddsa/tree/04e973bcf8d46819db055ebd0d44304c24a156a4

**Post-quantum maturity:** Level 0 of 4 — no post-quantum cryptography. **Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

**Findings:** Critical 0 · High 0 · Medium 2 · Low 0 · Info 2

**Quantum timeline (Mosca: x + y − z):** Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **Medium** · Quantum-vulnerable FROST: threshold signing and MPC protocols (1 file(s)) (QSI-2026-07275) · *preliminary*\
   What to do: Track post-quantum threshold signatures (NIST IR 8214C) and keep the protocol layer ready to swap the signature scheme; record which keys…
2. **Medium** · Quantum-vulnerable RedDSA: role not determined (3 file(s)) (QSI-2026-07274) · *preliminary*\
   What to do: Classify each usage, record data lifetimes, and plan migration to a post-quantum algorithm; introduce an abstraction layer for…

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · threshold signing and MPC protocols | FROST | Track post-quantum threshold signatures (NIST IR 8214C) and keep the protocol layer ready to swap the… |
| **Medium** · role not determined | RedDSA | Classify each usage, record data lifetimes, and plan migration to a post-quantum algorithm; introduce an… |

---

Static review of source code and manifests; files analysed: 15. No requests were sent to the owner's systems.

Full report, content SHA-256: `d9243f8dfd3941e5e6a92db037b26c39dbdc1672e3532e89daa13c24c6b57733`

Full report signature (report.sig.json): Ed25519 key, SHA-256 fingerprint `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.