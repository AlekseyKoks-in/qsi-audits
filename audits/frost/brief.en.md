# Post-quantum cryptography review: frost @ 0966bd1529aa

*One-page brief* · Reviewed: 2026-10-29 23:04 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: Zcash Foundation — public repository (passive review)

Source: https://github.com/ZcashFoundation/frost/tree/0966bd1529aa062ad3b621af99e277f976b1c0f0

**Post-quantum maturity:** Level 0 of 4 — no post-quantum cryptography. **Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

**Findings:** Critical 0 · High 0 · Medium 4 · Low 3 · Info 2

**Quantum timeline (Mosca: x + y − z):** Key establishment 10 + 5 − 8 = 7 → too late; Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **Medium** · No hybrid post-quantum key exchange configured (book/src/zcash/server.md) (QSI-2026-07007)\
   What to do: With OpenSSL ≥ 3.5 (or BoringSSL/rustls with ML-KEM), add X25519MLKEM768 ahead of X25519 in the groups list after interoperability testing.
2. **Medium** · Quantum-vulnerable FROST: threshold signing and MPC protocols (27 file(s)) (QSI-2026-07008) · *preliminary*\
   What to do: Track post-quantum threshold signatures (NIST IR 8214C) and keep the protocol layer ready to swap the signature scheme; record which keys…
3. **Medium** · Quantum-vulnerable ECDSA: threshold signing and MPC protocols (2 file(s)) (QSI-2026-07009) · *preliminary*\
   What to do: Track post-quantum threshold signatures (NIST IR 8214C) and keep the protocol layer ready to swap the signature scheme; record which keys…
4. **Medium** · Quantum-vulnerable ECDSA: role not determined (1 file(s)) (QSI-2026-07010) · *preliminary*\
   What to do: Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form…

3 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · threshold signing and MPC protocols | FROST, ECDSA | Track post-quantum threshold signatures (NIST IR 8214C) and keep the protocol layer ready to swap the… |
| **Medium** · role not determined | ECDSA | Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205)… |

## Known vulnerable components

Advisories for the versions in use: 4; unlikely to apply to this build: 1 (a Cargo feature that is off, affected functions not named in the code, or a platform that is not built); to review: 3.

---

Static review of source code and manifests; files analysed: 61. No requests were sent to the owner's systems.

Full report, content SHA-256: `3b0ed30a05821c2b696f385188fa6f97f309e120180a06949bb6210af7e79a0e`

Full report signature (report.sig.json): Ed25519 key, SHA-256 fingerprint `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.