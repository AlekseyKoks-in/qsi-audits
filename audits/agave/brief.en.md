# Post-quantum cryptography review: agave @ 7700cb3128c1

*One-page brief* · Reviewed: 2026-11-23 11:59 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: Anza (Solana) — public repository (passive review)

Source: https://github.com/anza-xyz/agave/tree/7700cb3128c1f19820de67b81aa45d18f73d2ac0

**Post-quantum maturity:** Level 0 of 4 — no post-quantum cryptography. **Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

**Findings:** Critical 0 · High 4 · Medium 27 · Low 40 · Info 42

**Quantum timeline (Mosca: x + y − z):** Key establishment 10 + 5 − 8 = 7 → too late; Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **High** · quinn-proto 0.10.6 is affected by GHSA-4w2j-m93h-cj5j (CVE-2026-25800, RUSTSEC-2026-0185) (QSI-2026-41515)\
   What to do: Upgrade to a fixed version (0.11.15).
2. **High** · quinn-proto 0.10.6 is affected by GHSA-6xvm-j4wr-6v98 (CVE-2026-31812, RUSTSEC-2026-0037) (QSI-2026-41516)\
   What to do: Upgrade to a fixed version (0.11.14).
3. **High** · tar 0.4.40 is affected by GHSA-gchp-q4r4-x4ff (CVE-2026-33055, RUSTSEC-2026-0068) (QSI-2026-41542)\
   What to do: Upgrade to a fixed version (0.4.45).
4. **High** · rustls-webpki 0.101.7 is affected by GHSA-82j2-j2ch-gfr8 (CVE-2026-93599, RUSTSEC-2026-0104) (QSI-2026-41533)\
   What to do: Upgrade to a fixed version (0.103.13, 0.104.0-alpha.7).

67 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · key wrapping and data encryption at rest | ElGamal | Wrap keys with ML-KEM or a hybrid KEM (X25519 + ML-KEM-768) and re-wrap the stored keys; data that may… |
| **Medium** · channel key exchange (TLS, Noise, handshakes) | TLS ECDHE | Move the handshake to a hybrid key exchange (X25519MLKEM768 in TLS 1.3; a hybrid KEM in Noise-based protocols) |
| **Medium** · threshold signing and MPC protocols | Pedersen commitment | Track post-quantum threshold signatures (NIST IR 8214C) and keep the protocol layer ready to swap the… |
| **Medium** · transaction and message signing | Ed25519, ECDSA, BN254 (alt_bn128) | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum… |

## Known vulnerable components

Advisories for the versions in use: 74; unlikely to apply to this build: 24 (a Cargo feature that is off, affected functions not named in the code, or a platform that is not built); to review: 50.

---

Static review of source code and manifests; files analysed: 1287. No requests were sent to the owner's systems.

Full report, content SHA-256: `f3d925a29d13b905d3036bec8ac7fab77ac833154d356c756864459a222df2f1`

Full report signature (report.sig.json): Ed25519 key, then the ML-DSA-65 one where it co-signs, SHA-256 fingerprints `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e · ML-DSA-65 dbd4e297b3213d1d7577a565e76de14cc5ad0e409f1dc68291c67266fc95066a`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.