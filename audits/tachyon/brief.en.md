# Post-quantum cryptography review: tachyon @ 6cdaebccf147

*One-page brief* · Reviewed: 2026-11-24 11:26 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: Tachyon (Zcash) — public repository (passive review)

Source: https://github.com/tachyon-zcash/tachyon/tree/6cdaebccf147c5a013d212f9d7302924a9570626

**Post-quantum maturity:** Level 0 of 4 — no post-quantum cryptography. **Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

**Findings:** Critical 0 · High 0 · Medium 3 · Low 10 · Info 1 (of them advisories unlikely to apply: 8)

**Quantum timeline (Mosca: x + y − z):** Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **Medium** · Quantum-vulnerable Pedersen commitment: threshold signing and MPC protocols (1 file(s)) (QSI-2026-49589) · *preliminary*\
   What to do: Track post-quantum threshold signatures (NIST IR 8214C) and keep the protocol layer ready to swap the signature scheme; record which keys…
2. **Medium** · Quantum-vulnerable RedDSA: role not determined (6 file(s)) (QSI-2026-49587) · *preliminary*\
   What to do: Classify each usage, record data lifetimes, and plan migration to a post-quantum algorithm; introduce an abstraction layer for…
3. **Medium** · Quantum-vulnerable RedDSA: authentication and identity (certificates, tokens, device attestation)… (QSI-2026-49588) · *preliminary*\
   What to do: Keep credentials short-lived and plan ML-DSA certificates, tokens and keys as the ecosystem supports them.
4. **Low** · heapless 0.7.17 is affected by RUSTSEC-2026-0580 (no severity rating) (QSI-2026-49598) · *preliminary*\
   What to do: Triage the advisory; upgrade to a fixed version (0.9.4) if it applies.

9 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · threshold signing and MPC protocols | Pedersen commitment | Track post-quantum threshold signatures (NIST IR 8214C) and keep the protocol layer ready to swap the… |
| **Medium** · authentication and identity (certificates, tokens, device attestation) | RedDSA | Keep credentials short-lived and plan ML-DSA certificates, tokens and keys as the ecosystem supports them |
| **Medium** · role not determined | RedDSA | Classify each usage, record data lifetimes, and plan migration to a post-quantum algorithm; introduce an… |

## Known vulnerable components

Advisories for the versions in use: 10; unlikely to apply to this build: 8 (no call path to the affected code, a module only tests use, functions not named in the code, a Cargo feature that is off or a platform not built); to review: 2.

---

Static review of source code and manifests; files analysed: 57. No requests were sent to the owner's systems.

Full report, content SHA-256: `d2582758173de8cfbdbd330e9c2fa474974d00acd862a78e5003fd9874e6dd55`

Full report signature (report.sig.json): Ed25519 key, then the ML-DSA-65 one where it co-signs, SHA-256 fingerprints `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e · ML-DSA-65 dbd4e297b3213d1d7577a565e76de14cc5ad0e409f1dc68291c67266fc95066a`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.