# Post-quantum cryptography review: trustwallet-wallet-core @ adf80f8bac98

*One-page brief* · Reviewed: 2026-11-24 13:03 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: Trust Wallet — public repository (passive review)

Source: https://github.com/trustwallet/wallet-core/tree/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9

**Post-quantum maturity:** Level 0 of 4 — no post-quantum cryptography. **Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

**Findings:** Critical 0 · High 0 · Medium 11 · Low 0 · Info 14 (of them advisories unlikely to apply: 5)

**Quantum timeline (Mosca: x + y − z):** Key establishment 10 + 5 − 8 = 7 → too late; Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **Medium** · Transaction signing for 43 chain(s) relies on elliptic-curve signatures (QSI-2026-50586) · *confirmed by the analyst*\
   What to do: Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains…
2. **Medium** · Quantum-vulnerable ECDSA: transaction and message signing (84 file(s)) (QSI-2026-50576) · *confirmed by the analyst*\
   What to do: Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains…
3. **Medium** · Quantum-vulnerable Ed25519: transaction and message signing (38 file(s)) (QSI-2026-50577) · *confirmed by the analyst*\
   What to do: Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains…
4. **Medium** · Quantum-vulnerable Schnorr (BIP-340): transaction and message signing (16 file(s)) (QSI-2026-50579) · *confirmed by the analyst*\
   What to do: Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains…

7 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · transaction and message signing | ECDSA, Ed25519, Schnorr (BIP-340), BLS12-381 … | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum… |
| **Medium** · authentication and identity (certificates, tokens, device attestation) | ECDSA | Keep credentials short-lived and plan ML-DSA certificates, tokens and keys as the ecosystem supports them |
| **Medium** · role not determined | Ed25519, ECDSA, Schnorr (BIP-340), X25519 … | Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205)… |

## Known vulnerable components

Advisories for the versions in use: 5; unlikely to apply to this build: 5 (no call path to the affected code, a module only tests use, functions not named in the code, a Cargo feature that is off or a platform not built); to review: 0.

Analyst review: 13 confirmed, 12 not applicable, 0 dismissed as false positives. (QSI review, 2026-10-28)

---

Static review of source code and manifests; files analysed: 1695. No requests were sent to the owner's systems.

Full report, content SHA-256: `5a8431b1429d457c7a449832f386a33123ab0d76e14a27c700135a7243b1b8c5`

Full report signature (report.sig.json): Ed25519 key, then the ML-DSA-65 one where it co-signs, SHA-256 fingerprints `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e · ML-DSA-65 dbd4e297b3213d1d7577a565e76de14cc5ad0e409f1dc68291c67266fc95066a`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.