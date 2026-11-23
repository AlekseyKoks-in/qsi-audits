# Post-quantum cryptography review: zebra @ 147a6a8bf7d3

*One-page brief* · Reviewed: 2026-11-23 13:31 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: Zcash Foundation — public repository (passive review)

Source: https://github.com/ZcashFoundation/zebra/tree/147a6a8bf7d3b1427a9c0557f284d5bfa7b0e522

**Post-quantum maturity:** Level 0 of 4 — no post-quantum cryptography. **Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

**Findings:** Critical 0 · High 2 · Medium 14 · Low 11 · Info 8

**Quantum timeline (Mosca: x + y − z):** Key establishment 10 + 5 − 8 = 7 → too late; Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **High** · quinn-proto 0.11.16 is affected by RUSTSEC-2026-0340 (QSI-2026-43877)\
   What to do: Upgrade to a fixed version (0.11.18).
2. **High** · quinn-proto 0.11.16 is affected by RUSTSEC-2026-0341 (QSI-2026-43878)\
   What to do: Upgrade to a fixed version (0.11.17).
3. **Medium** · Quantum-vulnerable Ed25519 key (Ed25519) in SECURITY.md (QSI-2026-43853)\
   What to do: Inventory and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it..
4. **Medium** · opentelemetry_sdk 0.31.0 is affected by GHSA-w9wp-h8wv-79jx (CVE-2026-48504) (QSI-2026-43873)\
   What to do: Upgrade to a fixed version (0.32.1).

23 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · key wrapping and data encryption at rest | Sinsemilla | Wrap keys with ML-KEM or a hybrid KEM (X25519 + ML-KEM-768) and re-wrap the stored keys; data that may… |
| **Medium** · threshold signing and MPC protocols | Pedersen commitment | Track post-quantum threshold signatures (NIST IR 8214C) and keep the protocol layer ready to swap the… |
| **Medium** · transaction and message signing | Ed25519, Halo 2 (IPA), RedDSA | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum… |
| **Medium** · role not determined | Halo 2 (IPA), RedDSA, Sinsemilla, X25519 … | Classify each usage, record data lifetimes, and plan migration to a post-quantum algorithm; introduce an… |

## Known vulnerable components

Advisories for the versions in use: 15; unlikely to apply to this build: 2 (a Cargo feature that is off, affected functions not named in the code, or a platform that is not built); to review: 13.

Analyst review: 0 confirmed, 0 not applicable, 0 dismissed as false positives. (QSI review, 2026-10-23)

---

Static review of source code and manifests; files analysed: 437. No requests were sent to the owner's systems.

Full report, content SHA-256: `d088edbaa8e8ba8d3edd5c5c4ce91861160386bbd322a7e8a7cc5a02b044dc5b`

Full report signature (report.sig.json): Ed25519 key, then the ML-DSA-65 one where it co-signs, SHA-256 fingerprints `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e · ML-DSA-65 dbd4e297b3213d1d7577a565e76de14cc5ad0e409f1dc68291c67266fc95066a`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.