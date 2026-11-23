# Post-quantum cryptography review: corda @ 80033580ecfd

*One-page brief* · Reviewed: 2026-11-23 13:44 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: R3 — public repository (passive review)

Source: https://github.com/corda/corda/tree/80033580ecfd66a22ab5e9cf5a1319d1111ade92

**Post-quantum maturity:** Level 0 of 4 — no post-quantum cryptography. **Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

**Findings:** Critical 0 · High 3 · Medium 6 · Low 1 · Info 0

**Quantum timeline (Mosca: x + y − z):** Key establishment 10 + 5 − 8 = 7 → too late; Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **High** · Certificate has expired (Corda Node Root CA) (QSI-2026-43972)\
   What to do: Renew the certificate and automate renewal (e.g. ACME) with expiry monitoring.
2. **High** · Possible hard-coded secret in core/src/main/kotlin/net/corda/core/CordaOID.kt (QSI-2026-43974) · *preliminary*\
   What to do: Move secrets to a secrets manager/environment; rotate the exposed values.
3. **High** · Possible hard-coded secret in… (QSI-2026-43981) · *preliminary*\
   What to do: Move secrets to a secrets manager/environment; rotate the exposed values.
4. **Medium** · Quantum-vulnerable ECDSA: transaction and message signing (1 file(s)) (QSI-2026-43978) · *preliminary*\
   What to do: Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains…

6 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · transaction and message signing | ECDSA | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum… |
| **Medium** · authentication and identity (certificates, tokens, device attestation) | ECDSA, Ed25519 | Keep credentials short-lived and plan ML-DSA certificates, tokens and keys as the ecosystem supports them |
| **Medium** · role not determined | ECDSA, RSA, Ed25519 | Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205)… |

---

Static review of source code and manifests; files analysed: 1117. No requests were sent to the owner's systems.

Full report, content SHA-256: `fd8dc48777a644a94728c1767e9ca2a0929e1aefdb2820ea6910253638bfa2ae`

Full report signature (report.sig.json): Ed25519 key, then the ML-DSA-65 one where it co-signs, SHA-256 fingerprints `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e · ML-DSA-65 dbd4e297b3213d1d7577a565e76de14cc5ad0e409f1dc68291c67266fc95066a`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.