# Post-quantum cryptography review: rs-soroban-env @ 0c99950e9612

*One-page brief* · Reviewed: 2026-11-06 16:05 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: Stellar Development Foundation — public repository (passive review)

Source: https://github.com/stellar/rs-soroban-env/tree/0c99950e96128beba3319aa96b116646ce974e69

**Post-quantum maturity:** Level 2 of 4 — post-quantum in use outside the critical paths. **Next step:** Extend post-quantum protection to the critical roles that stay classical, starting with what can be recorded today (wrapped keys, channel key exchange).

**Findings:** Critical 0 · High 0 · Medium 10 · Low 6 · Info 2

**Quantum timeline (Mosca: x + y − z):** Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **Medium** · Quantum-vulnerable Ed25519: transaction and message signing (2 file(s)) (QSI-2026-19557) · *preliminary*\
   What to do: Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains…
2. **Medium** · Quantum-vulnerable ECDSA: transaction and message signing (2 file(s)) (QSI-2026-19561) · *preliminary*\
   What to do: Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains…
3. **Medium** · Quantum-vulnerable Ed25519: role not determined (9 file(s)) (QSI-2026-19558) · *preliminary*\
   What to do: Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form…
4. **Medium** · Quantum-vulnerable BLS12-381: role not determined (5 file(s)) (QSI-2026-19559) · *preliminary*\
   What to do: Classify each usage, record data lifetimes, and plan migration to a post-quantum algorithm; introduce an abstraction layer for…

12 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · transaction and message signing | ECDSA, Ed25519 | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum… |
| **Medium** · authentication and identity (certificates, tokens, device attestation) | Ed25519 | Keep credentials short-lived and plan ML-DSA certificates, tokens and keys as the ecosystem supports them |
| **Medium** · role not determined | Ed25519, ECDSA, BLS12-381, BN254 (alt_bn128) | Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205)… |

## Known vulnerable components

Advisories for the versions in use: 9; unlikely to apply to this build: 2 (a Cargo feature that is off, affected functions not named in the code, or a platform that is not built); to review: 7.

---

Static review of source code and manifests; files analysed: 256. No requests were sent to the owner's systems.

Full report, content SHA-256: `9b85f3462552f82353205b89d9274711efee1e99748e272a6e7abd94e0172d1e`

Full report signature (report.sig.json): Ed25519 key, SHA-256 fingerprint `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.