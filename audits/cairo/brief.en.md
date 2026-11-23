# Post-quantum cryptography review: cairo @ 68a61f6c6251

*One-page brief* · Reviewed: 2026-11-23 12:18 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: StarkWare — public repository (passive review)

Source: https://github.com/starkware-libs/cairo/tree/68a61f6c6251900e0080e09c812ffaeb37fd358e

**Post-quantum maturity:** Level 0 of 4 — no post-quantum cryptography. **Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

**Findings:** Critical 2 · High 6 · Medium 8 · Low 23 · Info 4

**Quantum timeline (Mosca: x + y − z):** Key establishment 10 + 5 − 8 = 7 → too late; Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **Critical** · zip 0.6.6 is affected by GHSA-m665-v7pm-7grj (CVE-2026-115905, RUSTSEC-2026-0548) (QSI-2026-41827)\
   What to do: Upgrade to a fixed version (9.0.5).
2. **Critical** · zip 0.6.6 is affected by RUSTSEC-2026-0369 (QSI-2026-41830)\
   What to do: Upgrade to a fixed version (9.0.0).
3. **High** · pulldown-cmark 0.13.4 is affected by RUSTSEC-2026-0414 (QSI-2026-41809)\
   What to do: Upgrade to a fixed version (0.13.5).
4. **High** · pulldown-cmark 0.13.4 is affected by RUSTSEC-2026-0433 (QSI-2026-41810)\
   What to do: Upgrade to a fixed version (0.13.6).

35 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · threshold signing and MPC protocols | Pedersen hash | Track post-quantum threshold signatures (NIST IR 8214C) and keep the protocol layer ready to swap the… |
| **Medium** · transaction and message signing | ECDSA, Pedersen hash | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum… |
| **Medium** · role not determined | ECDSA, Pedersen hash | Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205)… |

## Known vulnerable components

Advisories for the versions in use: 35; unlikely to apply to this build: 6 (a Cargo feature that is off, affected functions not named in the code, or a platform that is not built); to review: 29.

---

Static review of source code and manifests; files analysed: 673. No requests were sent to the owner's systems.

Full report, content SHA-256: `6ac8c818e12805e9f179534b85530d2327e1d3952fae7ccaa9861b02a2f0c560`

Full report signature (report.sig.json): Ed25519 key, then the ML-DSA-65 one where it co-signs, SHA-256 fingerprints `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e · ML-DSA-65 dbd4e297b3213d1d7577a565e76de14cc5ad0e409f1dc68291c67266fc95066a`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.