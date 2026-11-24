# Post-quantum cryptography review: ethers-js @ 3ea4c226dd0b

*One-page brief* · Reviewed: 2026-11-24 10:27 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: ethers.js project — public repository (passive review)

Source: https://github.com/ethers-io/ethers.js/tree/3ea4c226dd0b3a074abf90748de9d11192027f4f

**Post-quantum maturity:** Level 0 of 4 — no post-quantum cryptography. **Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

**Findings:** Critical 0 · High 0 · Medium 3 · Low 0 · Info 4

**Quantum timeline (Mosca: x + y − z):** Key establishment 10 + 5 − 8 = 7 → too late; Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **Medium** · Quantum-vulnerable ECDSA: transaction and message signing (26 file(s)) (QSI-2026-47807) · *preliminary*\
   What to do: Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains…
2. **Medium** · Quantum-vulnerable ECDH: role not determined (3 file(s)) (QSI-2026-47808) · *preliminary*\
   What to do: Classify each usage, record data lifetimes, and plan migration to Hybrid key establishment with ML-KEM (FIPS 203), e.g. X25519MLKEM768 in…
3. **Medium** · Quantum-vulnerable ECDSA: role not determined (3 file(s)) (QSI-2026-47813) · *preliminary*\
   What to do: Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form…

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · transaction and message signing | ECDSA | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum… |
| **Medium** · role not determined | ECDH, ECDSA | Classify each usage, record data lifetimes, and plan migration to Hybrid key establishment with ML-KEM (FIPS… |

Analyst review: 0 confirmed, 2 not applicable, 12 dismissed as false positives. (QSI review, 2026-10-27)

---

Static review of source code and manifests; files analysed: 759. No requests were sent to the owner's systems.

Full report, content SHA-256: `981b7e7ba91a53174e5aaf5c88b285da2b0d4862ba50f00abfb1ea16574cbd6d`

Full report signature (report.sig.json): Ed25519 key, then the ML-DSA-65 one where it co-signs, SHA-256 fingerprints `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e · ML-DSA-65 dbd4e297b3213d1d7577a565e76de14cc5ad0e409f1dc68291c67266fc95066a`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.