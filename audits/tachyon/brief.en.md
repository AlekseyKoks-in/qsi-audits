# Post-quantum cryptography review: tachyon @ 6cdaebccf147

*One-page brief* · Reviewed: 2026-10-29 23:54 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: Tachyon (Zcash) — public repository (passive review)

Source: https://github.com/tachyon-zcash/tachyon/tree/6cdaebccf147c5a013d212f9d7302924a9570626

**Post-quantum maturity:** Level 0 of 4 — no post-quantum cryptography. **Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

**Findings:** Critical 0 · High 0 · Medium 4 · Low 1 · Info 2

**Quantum timeline (Mosca: x + y − z):** Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **Medium** · Quantum-vulnerable Pedersen commitment: threshold signing and MPC protocols (1 file(s)) (QSI-2026-07445) · *preliminary*\
   What to do: Track post-quantum threshold signatures (NIST IR 8214C) and keep the protocol layer ready to swap the signature scheme; record which keys…
2. **Medium** · Quantum-vulnerable RedDSA: role not determined (6 file(s)) (QSI-2026-07443) · *preliminary*\
   What to do: Classify each usage, record data lifetimes, and plan migration to a post-quantum algorithm; introduce an abstraction layer for…
3. **Medium** · Quantum-vulnerable RedDSA: authentication and identity (certificates, tokens, device attestation)… (QSI-2026-07444) · *preliminary*\
   What to do: Keep credentials short-lived and plan ML-DSA certificates, tokens and keys as the ecosystem supports them.
4. **Medium** · Non-cryptographic RNG near security-sensitive identifiers in book/mermaid.min.js (QSI-2026-07442) · *preliminary*\
   What to do: Use a CSPRNG (secrets, crypto.getRandomValues, crypto/rand).

1 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · threshold signing and MPC protocols | Pedersen commitment | Track post-quantum threshold signatures (NIST IR 8214C) and keep the protocol layer ready to swap the… |
| **Medium** · authentication and identity (certificates, tokens, device attestation) | RedDSA | Keep credentials short-lived and plan ML-DSA certificates, tokens and keys as the ecosystem supports them |
| **Medium** · role not determined | RedDSA | Classify each usage, record data lifetimes, and plan migration to a post-quantum algorithm; introduce an… |

## Known vulnerable components

Advisories for the versions in use: 1; each needs checking against the code.

---

Static review of source code and manifests; files analysed: 58. No requests were sent to the owner's systems.

Full report, content SHA-256: `b4a5fab2bdec6a0f10dffb9b2bac126760c1defa80e6e0498eabf8830d661237`

Full report signature (report.sig.json): Ed25519 key, SHA-256 fingerprint `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.