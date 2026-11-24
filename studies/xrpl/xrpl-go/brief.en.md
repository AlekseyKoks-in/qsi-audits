# Post-quantum cryptography review: xrpl-go @ 23275f007b47

*One-page brief* · Reviewed: 2026-11-24 12:23 UTC · Risk profile: Web3 project · Client: XRPL Foundation — public repository (passive review)

Source: https://github.com/XRPLF/xrpl-go/tree/23275f007b4758e82809f51d1e4ec3c5efb2fbe0

**Post-quantum maturity:** Level 0 of 4 — no post-quantum cryptography. **Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

**Findings:** Critical 0 · High 0 · Medium 4 · Low 4 · Info 3 (of them advisories unlikely to apply: 1)

**Quantum timeline (Mosca: x + y − z):** Key establishment 5 + 5 − 12 = -2 → tight; Signatures 10 + 5 − 12 = 3 → too late

## What matters most

1. **Medium** · Quantum-vulnerable ECDSA: transaction and message signing (9 file(s)) (QSI-2026-50278) · *preliminary*\
   What to do: Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains…
2. **Medium** · Quantum-vulnerable Pedersen commitment: threshold signing and MPC protocols (5 file(s)) (QSI-2026-50280) · *preliminary*\
   What to do: Track post-quantum threshold signatures (NIST IR 8214C) and keep the protocol layer ready to swap the signature scheme; record which keys…
3. **Medium** · Quantum-vulnerable ECDSA: role not determined (6 file(s)) (QSI-2026-50279) · *preliminary*\
   What to do: Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form…
4. **Medium** · Quantum-vulnerable Ed25519: role not determined (1 file(s)) (QSI-2026-50283) · *preliminary*\
   What to do: Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form…

4 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Low** · key wrapping and data encryption at rest | EC-ElGamal, ElGamal | Wrap keys with ML-KEM or a hybrid KEM (X25519 + ML-KEM-768) and re-wrap the stored keys; data that may… |
| **Medium** · threshold signing and MPC protocols | Pedersen commitment | Track post-quantum threshold signatures (NIST IR 8214C) and keep the protocol layer ready to swap the… |
| **Medium** · transaction and message signing | ECDSA | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum… |
| **Medium** · role not determined | ECDSA, EC-ElGamal, Ed25519 | Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205)… |

## Known vulnerable components

Advisories for the versions in use: 2; unlikely to apply to this build: 1 (no call path to the affected code, a module only tests use, functions not named in the code, a Cargo feature that is off or a platform not built); to review: 1.

---

Static review of source code and manifests; files analysed: 514. No requests were sent to the owner's systems.

Full report, content SHA-256: `f9db4079968b71a485ee3267c4405c7e7d0a37423da25741100e5100741b87e8`

Full report signature (report.sig.json): Ed25519 key, then the ML-DSA-65 one where it co-signs, SHA-256 fingerprints `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e · ML-DSA-65 dbd4e297b3213d1d7577a565e76de14cc5ad0e409f1dc68291c67266fc95066a`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.