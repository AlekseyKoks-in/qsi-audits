# Post-quantum cryptography review: trustwallet-wallet-core @ adf80f8bac98

*One-page brief* · Reviewed: 2026-11-06 14:09 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: Trust Wallet — public repository (passive review)

Source: https://github.com/trustwallet/wallet-core/tree/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9

**Post-quantum maturity:** Level 0 of 4 — no post-quantum cryptography. **Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

**Findings:** Critical 0 · High 0 · Medium 10 · Low 1 · Info 13

**Quantum timeline (Mosca: x + y − z):** Key establishment 10 + 5 − 8 = 7 → too late; Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **Medium** · Transaction signing for 43 chain(s) relies on elliptic-curve signatures (QSI-2026-19073) · *confirmed by the analyst*\
   What to do: Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains…
2. **Medium** · Quantum-vulnerable ECDSA: transaction and message signing (84 file(s)) (QSI-2026-19063) · *confirmed by the analyst*\
   What to do: Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains…
3. **Medium** · Quantum-vulnerable Ed25519: transaction and message signing (38 file(s)) (QSI-2026-19064) · *confirmed by the analyst*\
   What to do: Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains…
4. **Medium** · Quantum-vulnerable Schnorr (BIP-340): transaction and message signing (16 file(s)) (QSI-2026-19066) · *confirmed by the analyst*\
   What to do: Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains…

7 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · transaction and message signing | ECDSA, Ed25519, Schnorr (BIP-340), BLS12-381 … | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum… |
| **Medium** · authentication and identity (certificates, tokens, device attestation) | ECDSA | Keep credentials short-lived and plan ML-DSA certificates, tokens and keys as the ecosystem supports them |
| **Medium** · role not determined | Ed25519, ECDSA, Schnorr (BIP-340), X25519 … | Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205)… |

## Known vulnerable components

Advisories for the versions in use: 5; unlikely to apply to this build: 5 (a Cargo feature that is off, affected functions not named in the code, or a platform that is not built); to review: 0.

Analyst review: 13 confirmed, 11 not applicable, 0 dismissed as false positives. (QSI review, 2026-10-28)

---

Static review of source code and manifests; files analysed: 1695. No requests were sent to the owner's systems.

Full report, content SHA-256: `2b0df45a41718a581b21ec11a27880093808631567d7c06798e7cbd85821adbd`

Full report signature (report.sig.json): Ed25519 key, SHA-256 fingerprint `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.