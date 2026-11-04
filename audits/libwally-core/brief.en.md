# Post-quantum cryptography review: libwally-core @ 374df231d054

*One-page brief* · Reviewed: 2026-11-04 18:56 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: Blockstream (libwally) — public repository (passive review)

Source: https://github.com/ElementsProject/libwally-core/tree/374df231d05410a31d605b31c1cc5256581381d7

**Post-quantum maturity:** Level 0 of 4 — no post-quantum cryptography. **Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

**Findings:** Critical 0 · High 0 · Medium 7 · Low 0 · Info 1

**Quantum timeline (Mosca: x + y − z):** Key establishment 10 + 5 − 8 = 7 → too late; Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **Medium** · Quantum-vulnerable RSA key (4096-bit) in SECURITY.md (QSI-2026-12082)\
   What to do: Inventory and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it..
2. **Medium** · Quantum-vulnerable ECDH: key wrapping and data encryption at rest (2 file(s)) (QSI-2026-12085) · *confirmed by the analyst*\
   What to do: Wrap keys with ML-KEM or a hybrid KEM (X25519 + ML-KEM-768) and re-wrap the stored keys; data that may already have been copied needs its…
3. **Medium** · Quantum-vulnerable ECDSA: transaction and message signing (37 file(s)) (QSI-2026-12087) · *confirmed by the analyst*\
   What to do: Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains…
4. **Medium** · Quantum-vulnerable Schnorr (BIP-340): transaction and message signing (7 file(s)) (QSI-2026-12088) · *confirmed by the analyst*\
   What to do: Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains…

3 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · key wrapping and data encryption at rest | ECDH | Wrap keys with ML-KEM or a hybrid KEM (X25519 + ML-KEM-768) and re-wrap the stored keys; data that may… |
| **Medium** · transaction and message signing | ECDSA, Schnorr (BIP-340) | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum… |
| **Medium** · role not determined | ECDH, ECDSA, Schnorr (BIP-340) | Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205)… |

Analyst review: 6 confirmed, 1 not applicable, 0 dismissed as false positives. (QSI review, 2026-10-29)

---

Static review of source code and manifests; files analysed: 249. No requests were sent to the owner's systems.

Full report, content SHA-256: `c5113cb67ef52870716f434261cef10b8348209e2f0bfb7ed78e283dc233aa13`

Full report signature (report.sig.json): Ed25519 key, SHA-256 fingerprint `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.