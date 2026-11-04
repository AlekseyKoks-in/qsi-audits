# Post-quantum cryptography review: pasta-curves @ e3c0f0246f56

*One-page brief* · Reviewed: 2026-11-04 19:12 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: Electric Coin Company (Zcash) — public repository (passive review)

Source: https://github.com/zcash/pasta_curves/tree/e3c0f0246f56d351f1a94ff0a74c8d201dbf87d9

**Post-quantum maturity:** Level 0 of 4 — no post-quantum cryptography. **Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

**Findings:** Critical 0 · High 0 · Medium 1 · Low 0 · Info 1

**Quantum timeline (Mosca: x + y − z):** Key establishment 10 + 5 − 8 = 7 → too late

## What matters most

1. **Medium** · Quantum-vulnerable Pasta curves (Pallas/Vesta): role not determined (4 file(s)) (QSI-2026-12277) · *preliminary*\
   What to do: Classify each usage, record data lifetimes, and plan migration to a post-quantum algorithm; introduce an abstraction layer for…

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · role not determined | Pasta curves (Pallas/Vesta) | Classify each usage, record data lifetimes, and plan migration to a post-quantum algorithm; introduce an… |

---

Static review of source code and manifests; files analysed: 35. No requests were sent to the owner's systems.

Full report, content SHA-256: `02f97d2a63b9de6a907d16415561dfff45827aee3f298143449459019b8ae1cc`

Full report signature (report.sig.json): Ed25519 key, SHA-256 fingerprint `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.