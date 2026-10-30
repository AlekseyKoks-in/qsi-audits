# Post-quantum cryptography review: zebra @ 147a6a8bf7d3

*One-page brief* · Reviewed: 2026-10-29 23:49 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: Zcash Foundation — public repository (passive review)

Source: https://github.com/ZcashFoundation/zebra/tree/147a6a8bf7d3b1427a9c0557f284d5bfa7b0e522

**Post-quantum maturity:** Level 0 of 4 — no post-quantum cryptography. **Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

**Findings:** Critical 0 · High 2 · Medium 13 · Low 5 · Info 6

**Quantum timeline (Mosca: x + y − z):** Key establishment 10 + 5 − 8 = 7 → too late; Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **High** · quinn-proto 0.11.16 is affected by RUSTSEC-2026-0340 (QSI-2026-07371)\
   What to do: Upgrade to a fixed version (0.11.18).
2. **High** · quinn-proto 0.11.16 is affected by RUSTSEC-2026-0341 (QSI-2026-07372)\
   What to do: Upgrade to a fixed version (0.11.17).
3. **Medium** · Quantum-vulnerable Ed25519 key (Ed25519) in SECURITY.md (QSI-2026-07350)\
   What to do: Inventory and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it..
4. **Medium** · opentelemetry_sdk 0.31.0 is affected by GHSA-w9wp-h8wv-79jx (CVE-2026-48504) (QSI-2026-07367)\
   What to do: Upgrade to a fixed version (0.32.1).

16 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · threshold signing and MPC protocols | Pedersen commitment | Track post-quantum threshold signatures (NIST IR 8214C) and keep the protocol layer ready to swap the… |
| **Medium** · transaction and message signing | Halo 2 (IPA), Ed25519, RedDSA | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum… |
| **Medium** · role not determined | Halo 2 (IPA), Sinsemilla, RedDSA, X25519 … | Classify each usage, record data lifetimes, and plan migration to a post-quantum algorithm; introduce an… |

## Known vulnerable components

Advisories for the versions in use: 10; unlikely to apply to this build: 1 (a Cargo feature that is off, affected functions not named in the code, or a platform that is not built); to review: 9.

Analyst review: 0 confirmed, 0 not applicable, 1 dismissed as false positives. (QSI review, 2026-10-23)

---

Static review of source code and manifests; files analysed: 439. No requests were sent to the owner's systems.

Full report, content SHA-256: `91cfb3dd01b634fae7dd5a8e161479a5e242739f2957bd218e9a221f11e5df4c`

Full report signature (report.sig.json): Ed25519 key, SHA-256 fingerprint `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.