# Post-quantum cryptography review: libwally-core @ 374df231d054

*One-page brief* · Reviewed: 2026-10-29 19:57 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: Blockstream (libwally) — public repository (passive review)

Source: https://github.com/ElementsProject/libwally-core/tree/374df231d05410a31d605b31c1cc5256581381d7

**Post-quantum maturity:** Level 0 of 4 — no post-quantum cryptography. **Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

**Findings:** Critical 0 · High 0 · Medium 5 · Low 0 · Info 1

**Quantum timeline (Mosca: x + y − z):** Key establishment 10 + 5 − 8 = 7 → too late; Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **Medium** · Quantum-vulnerable RSA key (4096-bit) in SECURITY.md (QSI-2026-06685)\
   What to do: Inventory and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it..
2. **Medium** · Quantum-vulnerable ECDSA: transaction and message signing (36 file(s)) (QSI-2026-06686) · *confirmed by the analyst*\
   What to do: Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains…
3. **Medium** · Quantum-vulnerable Schnorr (BIP-340): transaction and message signing (5 file(s)) (QSI-2026-06688) · *confirmed by the analyst*\
   What to do: Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains…
4. **Medium** · Quantum-vulnerable ECDSA: role not determined (2 file(s)) (QSI-2026-06687) · *confirmed by the analyst*\
   What to do: Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form…

1 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · transaction and message signing | ECDSA, Schnorr (BIP-340) | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum… |
| **Medium** · role not determined | ECDSA, Schnorr (BIP-340) | Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205)… |

Analyst review: 4 confirmed, 1 not applicable, 0 dismissed as false positives. (QSI review, 2026-10-29)

---

Static review of source code and manifests; files analysed: 249. No requests were sent to the owner's systems.

Full report, content SHA-256: `df90bccaf38bd16d1d242f2278bdcc891e053d3d16dabc0f7ffb293761a8cc6c`

Full report signature (report.sig.json): Ed25519 key, SHA-256 fingerprint `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.