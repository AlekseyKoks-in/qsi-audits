# Post-quantum cryptography review: agave @ 7700cb3128c1

*One-page brief* · Reviewed: 2026-11-06 21:55 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: Anza (Solana) — public repository (passive review)

Source: https://github.com/anza-xyz/agave/tree/7700cb3128c1f19820de67b81aa45d18f73d2ac0

**Post-quantum maturity:** Level 0 of 4 — no post-quantum cryptography. **Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

**Findings:** Critical 0 · High 15 · Medium 34 · Low 34 · Info 28

**Quantum timeline (Mosca: x + y − z):** Key establishment 10 + 5 − 8 = 7 → too late; Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **High** · openssl 0.10.64 is affected by GHSA-8c75-8mhr-p7r9 (CVE-2026-41678) (QSI-2026-23142)\
   What to do: Upgrade to a fixed version (0.10.78).
2. **High** · openssl 0.10.64 is affected by GHSA-ghm9-cr32-g9qj (CVE-2026-41681) (QSI-2026-23143)\
   What to do: Upgrade to a fixed version (0.10.78).
3. **High** · openssl 0.10.64 is affected by GHSA-hppc-g8h3-xhp3 (CVE-2026-41898) (QSI-2026-23144)\
   What to do: Upgrade to a fixed version (0.10.78).
4. **High** · openssl 0.10.64 is affected by GHSA-pqf5-4pqq-29f5 (CVE-2026-41676) (QSI-2026-23146)\
   What to do: Upgrade to a fixed version (0.10.78).

79 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · key wrapping and data encryption at rest | ElGamal | Wrap keys with ML-KEM or a hybrid KEM (X25519 + ML-KEM-768) and re-wrap the stored keys; data that may… |
| **Medium** · channel key exchange (TLS, Noise, handshakes) | TLS ECDHE | Move the handshake to a hybrid key exchange (X25519MLKEM768 in TLS 1.3; a hybrid KEM in Noise-based protocols) |
| **Medium** · threshold signing and MPC protocols | Pedersen commitment | Track post-quantum threshold signatures (NIST IR 8214C) and keep the protocol layer ready to swap the… |
| **Medium** · transaction and message signing | Ed25519, ECDSA, BN254 (alt_bn128) | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum… |

## Known vulnerable components

Advisories for the versions in use: 78; unlikely to apply to this build: 16 (a Cargo feature that is off, affected functions not named in the code, or a platform that is not built); to review: 62.

---

Static review of source code and manifests; files analysed: 1293. No requests were sent to the owner's systems.

Full report, content SHA-256: `e07562da5ad4c4b8b1047070bd3490f9b610f804916abf0a0891cd02f3545648`

Full report signature (report.sig.json): Ed25519 key, SHA-256 fingerprint `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.