# Post-quantum cryptography review: orchard @ 616a669df8c9

*One-page brief* · Reviewed: 2026-10-29 23:44 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: Electric Coin Company (Zcash) — public repository (passive review)

Source: https://github.com/zcash/orchard/tree/616a669df8c9a59c33d47064d3ce04b25d026b2e

**Post-quantum maturity:** Level 0 of 4 — no post-quantum cryptography. **Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

**Findings:** Critical 0 · High 0 · Medium 6 · Low 4 · Info 6

**Quantum timeline (Mosca: x + y − z):** Key establishment 10 + 5 − 8 = 7 → too late; Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **Medium** · Quantum-vulnerable Pedersen commitment: threshold signing and MPC protocols (14 file(s)) (QSI-2026-07278) · *preliminary*\
   What to do: Track post-quantum threshold signatures (NIST IR 8214C) and keep the protocol layer ready to swap the signature scheme; record which keys…
2. **Medium** · Quantum-vulnerable Halo 2 (IPA): role not determined (16 file(s)) (QSI-2026-07279) · *preliminary*\
   What to do: Classify each usage, record data lifetimes, and plan migration to a post-quantum algorithm; introduce an abstraction layer for…
3. **Medium** · Quantum-vulnerable RedDSA: role not determined (1 file(s)) (QSI-2026-07280) · *preliminary*\
   What to do: Classify each usage, record data lifetimes, and plan migration to a post-quantum algorithm; introduce an abstraction layer for…
4. **Medium** · Quantum-vulnerable Sinsemilla: role not determined (9 file(s)) (QSI-2026-07281) · *preliminary*\
   What to do: Classify each usage, record data lifetimes, and plan migration to a post-quantum algorithm; introduce an abstraction layer for…

6 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · threshold signing and MPC protocols | Pedersen commitment | Track post-quantum threshold signatures (NIST IR 8214C) and keep the protocol layer ready to swap the… |
| **Medium** · authentication and identity (certificates, tokens, device attestation) | RedDSA | Keep credentials short-lived and plan ML-DSA certificates, tokens and keys as the ecosystem supports them |
| **Medium** · role not determined | Halo 2 (IPA), Sinsemilla, RedDSA | Classify each usage, record data lifetimes, and plan migration to a post-quantum algorithm; introduce an… |

## Known vulnerable components

Advisories for the versions in use: 5; unlikely to apply to this build: 1 (a Cargo feature that is off, affected functions not named in the code, or a platform that is not built); to review: 4.

---

Static review of source code and manifests; files analysed: 49. No requests were sent to the owner's systems.

Full report, content SHA-256: `638cc4f1f581e5f8f4b801f9303b6938cf0c446fb09c5fc6e07d71953fd31043`

Full report signature (report.sig.json): Ed25519 key, SHA-256 fingerprint `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.