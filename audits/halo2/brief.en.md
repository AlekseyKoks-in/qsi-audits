# Post-quantum cryptography review: halo2 @ 3442dd33754a

*One-page brief* · Reviewed: 2026-10-29 23:45 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: Electric Coin Company (Zcash) — public repository (passive review)

Source: https://github.com/zcash/halo2/tree/3442dd33754ae0d44b8970e5a4eea79b0c3360bf

**Post-quantum maturity:** Level 0 of 4 — no post-quantum cryptography. **Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

**Findings:** Critical 0 · High 0 · Medium 2 · Low 0 · Info 3

**Quantum timeline (Mosca: x + y − z):** Key establishment 10 + 5 − 8 = 7 → too late

## What matters most

1. **Medium** · Quantum-vulnerable Halo 2 (IPA): role not determined (34 file(s)) (QSI-2026-07294) · *preliminary*\
   What to do: Classify each usage, record data lifetimes, and plan migration to a post-quantum algorithm; introduce an abstraction layer for…
2. **Medium** · Quantum-vulnerable Sinsemilla: role not determined (9 file(s)) (QSI-2026-07295) · *preliminary*\
   What to do: Classify each usage, record data lifetimes, and plan migration to a post-quantum algorithm; introduce an abstraction layer for…

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · role not determined | Halo 2 (IPA), Sinsemilla | Classify each usage, record data lifetimes, and plan migration to a post-quantum algorithm; introduce an… |

---

Static review of source code and manifests; files analysed: 100. No requests were sent to the owner's systems.

Full report, content SHA-256: `78926dc2f6ba69925f7b5b54cd0fde297409fa72872eddb930be8eaf5f1f29da`

Full report signature (report.sig.json): Ed25519 key, SHA-256 fingerprint `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.