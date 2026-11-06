# Post-quantum cryptography review: noir @ 5c98fecd3fe6

*One-page brief* · Reviewed: 2026-11-06 13:41 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: Aztec / Noir — public repository (passive review)

Source: https://github.com/noir-lang/noir/tree/5c98fecd3fe6c51bd9e3a605cafe412d25ae8915

**Post-quantum maturity:** Level 0 of 4 — no post-quantum cryptography. **Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

**Findings:** Critical 0 · High 2 · Medium 4 · Low 3 · Info 3

**Quantum timeline (Mosca: x + y − z):** Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **High** · quick-xml 0.26.0 is affected by RUSTSEC-2026-0194 (QSI-2026-18417)\
   What to do: Upgrade to a fixed version (0.41.0).
2. **High** · quick-xml 0.26.0 is affected by RUSTSEC-2026-0195 (QSI-2026-18418)\
   What to do: Upgrade to a fixed version (0.41.0).
3. **Medium** · Quantum-vulnerable Pedersen commitment: threshold signing and MPC protocols (2 file(s)) (QSI-2026-18411) · *preliminary*\
   What to do: Track post-quantum threshold signatures (NIST IR 8214C) and keep the protocol layer ready to swap the signature scheme; record which keys…
4. **Medium** · Quantum-vulnerable BLS12-381: role not determined (2 file(s)) (QSI-2026-18409) · *preliminary*\
   What to do: Classify each usage, record data lifetimes, and plan migration to a post-quantum algorithm; introduce an abstraction layer for…

5 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · threshold signing and MPC protocols | Pedersen commitment | Track post-quantum threshold signatures (NIST IR 8214C) and keep the protocol layer ready to swap the… |
| **Medium** · role not determined | BLS12-381, ECDSA | Classify each usage, record data lifetimes, and plan migration to a post-quantum algorithm; introduce an… |

## Known vulnerable components

Advisories for the versions in use: 6; unlikely to apply to this build: 1 (a Cargo feature that is off, affected functions not named in the code, or a platform that is not built); to review: 5.

---

Static review of source code and manifests; files analysed: 783. No requests were sent to the owner's systems.

Full report, content SHA-256: `9579118b1ed736fecdaf1a116a0bf103b1ec5c13ba363a84361fbc9f45c88115`

Full report signature (report.sig.json): Ed25519 key, SHA-256 fingerprint `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.