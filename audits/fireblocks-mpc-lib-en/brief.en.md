# Post-quantum cryptography review: fireblocks-mpc-lib-en @ 00ae08b7f1bd

*One-page brief* · Reviewed: 2026-11-06 13:14 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: Fireblocks — public repository (passive review)

Source: https://github.com/fireblocks/mpc-lib/tree/00ae08b7f1bdbb887aedece384aca2f942aae432

**Post-quantum maturity:** Level 0 of 4 — no post-quantum cryptography. **Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

**Findings:** Critical 0 · High 0 · Medium 7 · Low 0 · Info 0

**Quantum timeline (Mosca: x + y − z):** Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **Medium** · Quantum-vulnerable Paillier: threshold signing and MPC protocols (30 file(s)) (QSI-2026-18011) · *confirmed by the analyst*\
   What to do: Track post-quantum threshold signatures (NIST IR 8214C) and keep the protocol layer ready to swap the signature scheme; record which keys…
2. **Medium** · Quantum-vulnerable Pedersen commitment: threshold signing and MPC protocols (8 file(s)) (QSI-2026-18012) · *confirmed by the analyst*\
   What to do: Track post-quantum threshold signatures (NIST IR 8214C) and keep the protocol layer ready to swap the signature scheme; record which keys…
3. **Medium** · Quantum-vulnerable Threshold ECDSA: threshold signing and MPC protocols (7 file(s)) (QSI-2026-18013) · *confirmed by the analyst*\
   What to do: Track post-quantum threshold signatures (NIST IR 8214C) and keep the protocol layer ready to swap the signature scheme; record which keys…
4. **Medium** · Quantum-vulnerable FROST: threshold signing and MPC protocols (7 file(s)) (QSI-2026-18014) · *confirmed by the analyst*\
   What to do: Track post-quantum threshold signatures (NIST IR 8214C) and keep the protocol layer ready to swap the signature scheme; record which keys…

3 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · threshold signing and MPC protocols | Paillier, Pedersen commitment, FROST, Threshold ECDSA … | Track post-quantum threshold signatures (NIST IR 8214C) and keep the protocol layer ready to swap the… |
| **Medium** · role not determined | Ed25519 | Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205)… |

Analyst review: 7 confirmed, 0 not applicable, 0 dismissed as false positives. (QSI review, 2026-10-28)

---

Static review of source code and manifests; files analysed: 123. No requests were sent to the owner's systems.

Full report, content SHA-256: `23fbd77d28cfee88fe35b18ec32795741bb197e17d217cbdef227c02036a02e3`

Full report signature (report.sig.json): Ed25519 key, SHA-256 fingerprint `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.