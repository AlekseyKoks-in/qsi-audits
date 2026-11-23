# Post-quantum cryptography review: noir @ 5c98fecd3fe6

*One-page brief* · Reviewed: 2026-11-23 12:50 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: Aztec / Noir — public repository (passive review)

Source: https://github.com/noir-lang/noir/tree/5c98fecd3fe6c51bd9e3a605cafe412d25ae8915

**Post-quantum maturity:** Level 0 of 4 — no post-quantum cryptography. **Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

**Findings:** Critical 0 · High 12 · Medium 20 · Low 8 · Info 4

**Quantum timeline (Mosca: x + y − z):** Key establishment 10 + 5 − 8 = 7 → too late; Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **High** · quick-xml 0.26.0 is affected by RUSTSEC-2026-0194 (QSI-2026-42402)\
   What to do: Upgrade to a fixed version (0.41.0).
2. **High** · quick-xml 0.26.0 is affected by RUSTSEC-2026-0195 (QSI-2026-42403)\
   What to do: Upgrade to a fixed version (0.41.0).
3. **High** · @fastify/busboy 2.1.1 is affected by GHSA-x8mw-p69m-v3mx (CVE-2026-19481) (QSI-2026-42408)\
   What to do: Upgrade to a fixed version (3.2.1).
4. **High** · brace-expansion 5.0.8 is affected by GHSA-6j4f-fj2g-mc7p (CVE-2026-102276) (QSI-2026-42410)\
   What to do: Upgrade to a fixed version (1.1.19, 2.1.5, 3.0.7, 5.0.10).

36 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · threshold signing and MPC protocols | Pedersen commitment | Track post-quantum threshold signatures (NIST IR 8214C) and keep the protocol layer ready to swap the… |
| **Medium** · role not determined | BLS12-381, ECDSA, Pedersen hash | Classify each usage, record data lifetimes, and plan migration to a post-quantum algorithm; introduce an… |

## Known vulnerable components

Advisories for the versions in use: 36; unlikely to apply to this build: 2 (a Cargo feature that is off, affected functions not named in the code, or a platform that is not built); to review: 34.

---

Static review of source code and manifests; files analysed: 782. No requests were sent to the owner's systems.

Full report, content SHA-256: `de1f3a625a8efad1595565943d70e067f88481fb35499051ce74f2358042ee98`

Full report signature (report.sig.json): Ed25519 key, then the ML-DSA-65 one where it co-signs, SHA-256 fingerprints `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e · ML-DSA-65 dbd4e297b3213d1d7577a565e76de14cc5ad0e409f1dc68291c67266fc95066a`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.