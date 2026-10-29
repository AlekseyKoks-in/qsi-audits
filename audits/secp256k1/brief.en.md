# Post-quantum cryptography review: secp256k1 @ 1b4181f93f7a

*One-page brief* · Reviewed: 2026-10-29 19:55 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: Bitcoin Core (libsecp256k1) — public repository (passive review)

Source: https://github.com/bitcoin-core/secp256k1/tree/1b4181f93f7a53639223ced4c347d0d0d2c2ff9c

**Post-quantum maturity:** Level 0 of 4 — no post-quantum cryptography. **Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

**Findings:** Critical 0 · High 0 · Medium 3 · Low 0 · Info 0

**Quantum timeline (Mosca: x + y − z):** Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **Medium** · Quantum-vulnerable ECDSA: transaction and message signing (10 file(s)) (QSI-2026-06680) · *confirmed by the analyst*\
   What to do: Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains…
2. **Medium** · Quantum-vulnerable Schnorr (BIP-340): transaction and message signing (3 file(s)) (QSI-2026-06681) · *confirmed by the analyst*\
   What to do: Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains…
3. **Medium** · Quantum-vulnerable ECDSA: role not determined (13 file(s)) (QSI-2026-06679) · *confirmed by the analyst*\
   What to do: Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form…

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · transaction and message signing | ECDSA, Schnorr (BIP-340) | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum… |
| **Medium** · role not determined | ECDSA | Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205)… |

Analyst review: 3 confirmed, 0 not applicable, 0 dismissed as false positives. (QSI review, 2026-10-29)

---

Static review of source code and manifests; files analysed: 90. No requests were sent to the owner's systems.

Full report, content SHA-256: `56f80d0b643240472a5275315c67519ccec002d816ceb4d16c80c8c585d6670a`

Full report signature (report.sig.json): Ed25519 key, SHA-256 fingerprint `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.