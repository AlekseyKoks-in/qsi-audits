# Post-quantum cryptography review: agave @ 7700cb3128c1

*One-page brief* · Reviewed: 2026-11-17 18:44 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: Anza (Solana) — public repository (passive review)

Source: https://github.com/anza-xyz/agave/tree/7700cb3128c1f19820de67b81aa45d18f73d2ac0

**Post-quantum maturity:** Level 0 of 4 — no post-quantum cryptography. **Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

**Findings:** Critical 3 · High 99 · Medium 103 · Low 59 · Info 41

**Quantum timeline (Mosca: x + y − z):** Key establishment 10 + 5 − 8 = 7 → too late; Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **Critical** · loader-utils 2.0.2 is affected by GHSA-76p3-8jx3-jpfq (CVE-2022-37601) (QSI-2026-27404)\
   What to do: Upgrade to a fixed version (1.4.1, 2.0.3).
2. **Critical** · proxy-addr 2.0.7 is affected by GHSA-jqcg-44mw-7w3h (CVE-2026-90711) (QSI-2026-27448)\
   What to do: Upgrade to a fixed version (2.0.8).
3. **Critical** · websocket-driver 0.7.4 is affected by GHSA-xv26-6w52-cph6 (CVE-2026-54466) (QSI-2026-27505)\
   What to do: Upgrade to a fixed version (0.7.5).
4. **High** · quinn-proto 0.10.6 is affected by GHSA-4w2j-m93h-cj5j (CVE-2026-25800, RUSTSEC-2026-0185) (QSI-2026-27270)\
   What to do: Upgrade to a fixed version (0.11.15).

260 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · key wrapping and data encryption at rest | ElGamal | Wrap keys with ML-KEM or a hybrid KEM (X25519 + ML-KEM-768) and re-wrap the stored keys; data that may… |
| **Medium** · channel key exchange (TLS, Noise, handshakes) | TLS ECDHE | Move the handshake to a hybrid key exchange (X25519MLKEM768 in TLS 1.3; a hybrid KEM in Noise-based protocols) |
| **Medium** · threshold signing and MPC protocols | Pedersen commitment | Track post-quantum threshold signatures (NIST IR 8214C) and keep the protocol layer ready to swap the… |
| **Medium** · transaction and message signing | Ed25519, ECDSA, BN254 (alt_bn128) | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum… |

## Known vulnerable components

Advisories for the versions in use: 267; unlikely to apply to this build: 24 (a Cargo feature that is off, affected functions not named in the code, or a platform that is not built); to review: 243.

---

Static review of source code and manifests; files analysed: 1287. No requests were sent to the owner's systems.

Full report, content SHA-256: `d51a5b6711ab5cfa745288825d028076f2f7e569c0a5a602efa6751a4f3d1fc6`

Full report signature (report.sig.json): Ed25519 key, then the ML-DSA-65 one where it co-signs, SHA-256 fingerprints `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e · ML-DSA-65 dbd4e297b3213d1d7577a565e76de14cc5ad0e409f1dc68291c67266fc95066a`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.