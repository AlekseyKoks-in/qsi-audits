# Post-quantum cryptography review: stellar-core @ 362dbc5184c5

*One-page brief* · Reviewed: 2026-11-24 12:49 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: Stellar Development Foundation — public repository (passive review)

Source: https://github.com/stellar/stellar-core/tree/362dbc5184c5fdc0d6e898f3046639dc5e2a4f32

**Post-quantum maturity:** Level 1 of 4 — post-quantum code present, not wired. **Next step:** Wire the existing post-quantum primitive into a critical path (key wrapping or the channel) behind a hybrid construction, and test interoperability.

**Findings:** Critical 0 · High 0 · Medium 22 · Low 36 · Info 9 (of them advisories unlikely to apply: 2)

**Quantum timeline (Mosca: x + y − z):** Key establishment 10 + 5 − 8 = 7 → too late; Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **Medium** · Quantum-vulnerable Ed25519: transaction and message signing (13 file(s)) (QSI-2026-50465) · *preliminary*\
   What to do: Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains…
2. **Medium** · Quantum-vulnerable ECDSA: transaction and message signing (8 file(s)) (QSI-2026-50468) · *preliminary*\
   What to do: Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains…
3. **Medium** · Quantum-vulnerable X25519: role not determined (9 file(s)) (QSI-2026-50463) · *preliminary*\
   What to do: Classify each usage, record data lifetimes, and plan migration to Hybrid key establishment with ML-KEM (FIPS 203), e.g. X25519MLKEM768 in…
4. **Medium** · Quantum-vulnerable Ed25519: role not determined (36 file(s)) (QSI-2026-50464) · *preliminary*\
   What to do: Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form…

54 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · transaction and message signing | Ed25519, ECDSA | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum… |
| **Medium** · authentication and identity (certificates, tokens, device attestation) | Ed25519 | Keep credentials short-lived and plan ML-DSA certificates, tokens and keys as the ecosystem supports them |
| **Medium** · role not determined | Ed25519, ECDSA, BLS12-381, X25519 | Classify each usage, record data lifetimes, and plan migration to Hybrid key establishment with ML-KEM (FIPS… |

## Known vulnerable components

Advisories for the versions in use: 50; unlikely to apply to this build: 2 (no call path to the affected code, a module only tests use, functions not named in the code, a Cargo feature that is off or a platform not built); to review: 48.

Analyst review: 0 confirmed, 0 not applicable, 1 dismissed as false positives. (QSI review, 2026-11-24)

---

Static review of source code and manifests; files analysed: 3401. No requests were sent to the owner's systems.

Full report, content SHA-256: `f9281f5842a7a0e108f6c1ab8f0b7da0d65c121ee2b7bb5827b79143a43701e5`

Full report signature (report.sig.json): Ed25519 key, then the ML-DSA-65 one where it co-signs, SHA-256 fingerprints `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e · ML-DSA-65 dbd4e297b3213d1d7577a565e76de14cc5ad0e409f1dc68291c67266fc95066a`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.