# Post-quantum cryptography review: cairo @ 68a61f6c6251

*One-page brief* · Reviewed: 2026-10-30 22:40 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: StarkWare — public repository (passive review)

Source: https://github.com/starkware-libs/cairo/tree/68a61f6c6251900e0080e09c812ffaeb37fd358e

**Post-quantum maturity:** Level 0 of 4 — no post-quantum cryptography. **Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

**Findings:** Critical 2 · High 4 · Medium 6 · Low 10 · Info 4

**Quantum timeline (Mosca: x + y − z):** Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **Critical** · zip 0.6.6 is affected by GHSA-m665-v7pm-7grj (CVE-2026-115905) (QSI-2026-08258)\
   What to do: Upgrade to a fixed version (9.0.5).
2. **Critical** · zip 0.6.6 is affected by RUSTSEC-2026-0369 (QSI-2026-08261)\
   What to do: Upgrade to a fixed version (9.0.0).
3. **High** · pulldown-cmark 0.13.4 is affected by RUSTSEC-2026-0414 (QSI-2026-08245)\
   What to do: Upgrade to a fixed version (0.13.5).
4. **High** · quinn-proto 0.11.17 is affected by RUSTSEC-2026-0340 (QSI-2026-08247)\
   What to do: Upgrade to a fixed version (0.11.18).

18 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · threshold signing and MPC protocols | Pedersen commitment | Track post-quantum threshold signatures (NIST IR 8214C) and keep the protocol layer ready to swap the… |
| **Medium** · transaction and message signing | ECDSA | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum… |
| **Medium** · role not determined | ECDSA | Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205)… |

## Known vulnerable components

Advisories for the versions in use: 20; unlikely to apply to this build: 2 (a Cargo feature that is off, affected functions not named in the code, or a platform that is not built); to review: 18.

---

Static review of source code and manifests; files analysed: 567. No requests were sent to the owner's systems.

Full report, content SHA-256: `0cede3410ee055ef6b93e3929d0ef3eaf01d8d91a4c591065d7bd91e370d0a45`

Full report signature (report.sig.json): Ed25519 key, SHA-256 fingerprint `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.