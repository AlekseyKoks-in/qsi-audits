# Post-quantum cryptography review: hyperledger-fabric @ 13ef9e5ee594

*One-page brief* · Reviewed: 2026-11-24 17:25 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: Hyperledger Fabric (LF Decentralized Trust) — public repository (passive review)

Source: https://github.com/hyperledger/fabric/tree/13ef9e5ee59466b152c8fe65b3a095234de671f7

**Post-quantum maturity:** Level 3 of 4 — hybrid protection in a critical path. **Next step:** Pin the toolchain version and set the TLS groups in the code (X25519MLKEM768 first): the hybrid key exchange found rests on a default the code does not show, and a toolchain or library change would change it.

**Findings:** Critical 0 · High 0 · Medium 7 · Low 7 · Info 16 (of them advisories unlikely to apply: 16)

**Quantum timeline (Mosca: x + y − z):** Key establishment 10 + 5 − 8 = 7 → too late; Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **Medium** · Quantum-vulnerable ECDSA: transaction and message signing (1 file(s)) (QSI-2026-50980) · *preliminary*\
   What to do: Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains…
2. **Medium** · Quantum-vulnerable Ed25519: transaction and message signing (1 file(s)) (QSI-2026-50981) · *preliminary*\
   What to do: Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains…
3. **Medium** · Quantum-vulnerable ECDSA: authentication and identity (certificates, tokens, device attestation)… (QSI-2026-50982) · *preliminary*\
   What to do: Keep credentials short-lived and plan ML-DSA certificates, tokens and keys as the ecosystem supports them.
4. **Medium** · Quantum-vulnerable ECDSA: role not determined (7 file(s)) (QSI-2026-50983) · *preliminary*\
   What to do: Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form…

10 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · transaction and message signing | ECDSA, Ed25519 | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum… |
| **Medium** · authentication and identity (certificates, tokens, device attestation) | ECDSA | Keep credentials short-lived and plan ML-DSA certificates, tokens and keys as the ecosystem supports them |
| **Medium** · role not determined | ECDSA, ECDH, Ed25519 | Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205)… |

## Known vulnerable components

Advisories for the versions in use: 21; unlikely to apply to this build: 16 (no call path to the affected code, a module only tests use, functions not named in the code, a Cargo feature that is off or a platform not built); to review: 5.

---

Static review of source code and manifests; files analysed: 813. No requests were sent to the owner's systems.

Full report, content SHA-256: `57d4712c4ea496b59b47089d4e312745c731ae6bbb963a54636265041952a410`

Full report signature (report.sig.json): Ed25519 key, then the ML-DSA-65 one where it co-signs, SHA-256 fingerprints `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e · ML-DSA-65 dbd4e297b3213d1d7577a565e76de14cc5ad0e409f1dc68291c67266fc95066a`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.