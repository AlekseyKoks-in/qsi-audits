# Post-quantum cryptography review: fabric-lib-go @ f8b4f4a833e4

*One-page brief* · Reviewed: 2026-11-24 12:38 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: Hyperledger Fabric (LF Decentralized Trust) — public repository (passive review)

Source: https://github.com/hyperledger/fabric-lib-go/tree/f8b4f4a833e4140a4d006fc2e0a46823952b5f1c

**Post-quantum maturity:** Level 0 of 4 — no post-quantum cryptography. **Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

**Findings:** Critical 0 · High 0 · Medium 3 · Low 0 · Info 9 (of them advisories unlikely to apply: 8)

**Quantum timeline (Mosca: x + y − z):** Key establishment 10 + 5 − 8 = 7 → too late; Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **Medium** · Quantum-vulnerable ECDSA: role not determined (10 file(s)) (QSI-2026-50419) · *preliminary*\
   What to do: Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form…
2. **Medium** · Quantum-vulnerable Ed25519: role not determined (6 file(s)) (QSI-2026-50420) · *preliminary*\
   What to do: Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form…
3. **Medium** · Quantum-vulnerable RSA: role not determined (6 file(s)) (QSI-2026-50421) · *preliminary*\
   What to do: Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form…

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · role not determined | ECDSA, Ed25519, RSA | Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205)… |

## Known vulnerable components

Advisories for the versions in use: 8; unlikely to apply to this build: 8 (no call path to the affected code, a module only tests use, functions not named in the code, a Cargo feature that is off or a platform not built); to review: 0.

---

Static review of source code and manifests; files analysed: 67. No requests were sent to the owner's systems.

Full report, content SHA-256: `984e17ce13c776af60b66152eeba8360455c2444552d42cef727c77044fd1213`

Full report signature (report.sig.json): Ed25519 key, then the ML-DSA-65 one where it co-signs, SHA-256 fingerprints `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e · ML-DSA-65 dbd4e297b3213d1d7577a565e76de14cc5ad0e409f1dc68291c67266fc95066a`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.