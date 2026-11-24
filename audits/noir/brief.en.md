# Post-quantum cryptography review: noir @ 5c98fecd3fe6

*One-page brief* · Reviewed: 2026-11-24 10:57 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: Aztec / Noir — public repository (passive review)

Source: https://github.com/noir-lang/noir/tree/5c98fecd3fe6c51bd9e3a605cafe412d25ae8915

**Post-quantum maturity:** Level 0 of 4 — no post-quantum cryptography. **Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

**Findings:** Critical 0 · High 12 · Medium 20 · Low 8 · Info 4 (of them advisories unlikely to apply: 2)

**Quantum timeline (Mosca: x + y − z):** Key establishment 10 + 5 − 8 = 7 → too late; Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **High** · quick-xml 0.26.0 is affected by RUSTSEC-2026-0194 (QSI-2026-48342)\
   What to do: Upgrade to a fixed version (0.41.0).
2. **High** · @fastify/busboy 2.1.1 is affected by GHSA-x8mw-p69m-v3mx (CVE-2026-19481) (QSI-2026-48348)\
   What to do: Upgrade to a fixed version (3.2.1).
3. **High** · brace-expansion 5.0.8 is affected by GHSA-6j4f-fj2g-mc7p (CVE-2026-102276) (QSI-2026-48350)\
   What to do: Upgrade to a fixed version (1.1.19, 2.1.5, 3.0.7, 5.0.10).
4. **High** · lodash-es 4.17.21 is affected by GHSA-r5fr-rjxr-66jc (CVE-2026-4800) (QSI-2026-48355)\
   What to do: Upgrade to a fixed version (4.18.0).

36 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · threshold signing and MPC protocols | Pedersen commitment | Track post-quantum threshold signatures (NIST IR 8214C) and keep the protocol layer ready to swap the… |
| **Medium** · role not determined | BLS12-381, ECDSA, Pedersen hash | Classify each usage, record data lifetimes, and plan migration to a post-quantum algorithm; introduce an… |

## Known vulnerable components

Advisories for the versions in use: 36; unlikely to apply to this build: 2 (no call path to the affected code, a module only tests use, functions not named in the code, a Cargo feature that is off or a platform not built); to review: 34.

---

Static review of source code and manifests; files analysed: 782. No requests were sent to the owner's systems.

Full report, content SHA-256: `e2e218b5fa99d8d4137c6a849354e1ff5621b4d388681cca577051a34960a94c`

Full report signature (report.sig.json): Ed25519 key, then the ML-DSA-65 one where it co-signs, SHA-256 fingerprints `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e · ML-DSA-65 dbd4e297b3213d1d7577a565e76de14cc5ad0e409f1dc68291c67266fc95066a`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.