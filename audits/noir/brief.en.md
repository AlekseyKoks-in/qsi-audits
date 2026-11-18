# Post-quantum cryptography review: noir @ 5c98fecd3fe6

*One-page brief* · Reviewed: 2026-11-17 18:36 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: Aztec / Noir — public repository (passive review)

Source: https://github.com/noir-lang/noir/tree/5c98fecd3fe6c51bd9e3a605cafe412d25ae8915

**Post-quantum maturity:** Level 0 of 4 — no post-quantum cryptography. **Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

**Findings:** Critical 2 · High 54 · Medium 61 · Low 15 · Info 4

**Quantum timeline (Mosca: x + y − z):** Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **Critical** · tinypool 1.1.1 is affected by GHSA-5gmw-xhrv-c9v3 (CVE-2026-104848) (QSI-2026-27098)\
   What to do: Upgrade to a fixed version (2.1.1).
2. **Critical** · tinypool 1.1.1 is affected by GHSA-85c8-ppgw-ccpr (CVE-2026-104849) (QSI-2026-27099)\
   What to do: Upgrade to a fixed version (2.1.2).
3. **High** · quick-xml 0.26.0 is affected by RUSTSEC-2026-0194 (QSI-2026-27034)\
   What to do: Upgrade to a fixed version (0.41.0).
4. **High** · quick-xml 0.26.0 is affected by RUSTSEC-2026-0195 (QSI-2026-27035)\
   What to do: Upgrade to a fixed version (0.41.0).

128 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · threshold signing and MPC protocols | Pedersen commitment | Track post-quantum threshold signatures (NIST IR 8214C) and keep the protocol layer ready to swap the… |
| **Medium** · role not determined | BLS12-381, ECDSA | Classify each usage, record data lifetimes, and plan migration to a post-quantum algorithm; introduce an… |

## Known vulnerable components

Advisories for the versions in use: 129; unlikely to apply to this build: 2 (a Cargo feature that is off, affected functions not named in the code, or a platform that is not built); to review: 127.

---

Static review of source code and manifests; files analysed: 783. No requests were sent to the owner's systems.

Full report, content SHA-256: `71c9e6610c9f497aca033e9d472373545a13a16d695dcb82012c49a01b7b5d01`

Full report signature (report.sig.json): Ed25519 key, then the ML-DSA-65 one where it co-signs, SHA-256 fingerprints `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e · ML-DSA-65 dbd4e297b3213d1d7577a565e76de14cc5ad0e409f1dc68291c67266fc95066a`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.