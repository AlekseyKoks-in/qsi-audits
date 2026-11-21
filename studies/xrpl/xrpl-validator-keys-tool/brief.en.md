# Post-quantum cryptography review: xrpl-validator-keys-tool @ 4c0fb75eec96

*One-page brief* · Reviewed: 2026-11-21 10:24 UTC · Risk profile: Web3 project · Client: Ripple — public repository (passive review)

Source: https://github.com/ripple/validator-keys-tool/tree/4c0fb75eec9601c711645998c904507e87e910ae

**Post-quantum maturity:** Level 0 of 4 — no post-quantum cryptography. **Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

**Findings:** Critical 0 · High 0 · Medium 2 · Low 0 · Info 0

**Quantum timeline (Mosca: x + y − z):** Signatures 10 + 5 − 12 = 3 → too late

## What matters most

1. **Medium** · Quantum-vulnerable ECDSA: role not determined (1 file(s)) (QSI-2026-34934) · *preliminary*\
   What to do: Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form…
2. **Medium** · Quantum-vulnerable Ed25519: role not determined (1 file(s)) (QSI-2026-34935) · *preliminary*\
   What to do: Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form…

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · role not determined | ECDSA, Ed25519 | Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205)… |

---

Static review of source code and manifests; files analysed: 4. No requests were sent to the owner's systems.

Full report, content SHA-256: `b85785e63f890a58ff95dd6422534423caf8411033ded5511e5803a9181a099c`

Full report signature (report.sig.json): Ed25519 key, then the ML-DSA-65 one where it co-signs, SHA-256 fingerprints `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e · ML-DSA-65 dbd4e297b3213d1d7577a565e76de14cc5ad0e409f1dc68291c67266fc95066a`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.