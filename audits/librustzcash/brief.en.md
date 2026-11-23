# Post-quantum cryptography review: librustzcash @ 8672a4b2d60f

*One-page brief* · Reviewed: 2026-11-23 12:35 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: Electric Coin Company (Zcash) — public repository (passive review)

Source: https://github.com/zcash/librustzcash/tree/8672a4b2d60f432664780e6a4e85f49a36805a2a

**Post-quantum maturity:** Level 0 of 4 — no post-quantum cryptography. **Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

**Findings:** Critical 0 · High 2 · Medium 10 · Low 35 · Info 10

**Quantum timeline (Mosca: x + y − z):** Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **High** · rustls-webpki 0.101.7 is affected by GHSA-82j2-j2ch-gfr8 (CVE-2026-93599, RUSTSEC-2026-0104) (QSI-2026-42090)\
   What to do: Upgrade to a fixed version (0.103.13, 0.104.0-alpha.7).
2. **High** · rustls-webpki 0.103.3 is affected by GHSA-82j2-j2ch-gfr8 (CVE-2026-93599, RUSTSEC-2026-0104) (QSI-2026-42094)\
   What to do: Upgrade to a fixed version (0.103.13, 0.104.0-alpha.7).
3. **Medium** · serde_with 3.16.0 is affected by GHSA-7gcf-g7xr-8hxj (QSI-2026-42099)\
   What to do: Upgrade to a fixed version (3.21.0).
4. **Medium** · Quantum-vulnerable Pedersen commitment: threshold signing and MPC protocols (4 file(s)) (QSI-2026-42058) · *preliminary*\
   What to do: Track post-quantum threshold signatures (NIST IR 8214C) and keep the protocol layer ready to swap the signature scheme; record which keys…

43 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · threshold signing and MPC protocols | Pedersen commitment | Track post-quantum threshold signatures (NIST IR 8214C) and keep the protocol layer ready to swap the… |
| **Medium** · transaction and message signing | ECDSA, BLS12-381 | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum… |

## Known vulnerable components

Advisories for the versions in use: 45; unlikely to apply to this build: 15 (a Cargo feature that is off, affected functions not named in the code, or a platform that is not built); to review: 30.

---

Static review of source code and manifests; files analysed: 333. No requests were sent to the owner's systems.

Full report, content SHA-256: `1a261486a4fc9c4d6cf51703116da0016cda44ad98004e8e633da9caffdf3aa9`

Full report signature (report.sig.json): Ed25519 key, then the ML-DSA-65 one where it co-signs, SHA-256 fingerprints `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e · ML-DSA-65 dbd4e297b3213d1d7577a565e76de14cc5ad0e409f1dc68291c67266fc95066a`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.