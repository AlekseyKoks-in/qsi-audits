# Post-quantum cryptography review: zcash-android-wallet-sdk @ a95780ac00e0

*One-page brief* · Reviewed: 2026-11-23 13:28 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: Electric Coin Company (Zcash) — public repository (passive review)

Source: https://github.com/zcash/zcash-android-wallet-sdk/tree/a95780ac00e0198c111c6e701126e6688f64a12a

**Post-quantum maturity:** Level 0 of 4 — no post-quantum cryptography. **Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

**Findings:** Critical 0 · High 0 · Medium 6 · Low 31 · Info 8

**Quantum timeline (Mosca: x + y − z):** Key establishment 10 + 5 − 8 = 7 → too late; Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **Medium** · Quantum-vulnerable RSA key (2048-bit) in responsible_disclosure.md (QSI-2026-43766)\
   What to do: Inventory and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it..
2. **Medium** · SHA-1 used in backend-lib/src/main/java/cash/z/ecc/android/sdk/internal/ext/FileExt.kt (QSI-2026-43764) · *confirmed by the analyst*\
   What to do: Replace with SHA-256/SHA-3 (or Argon2/bcrypt for passwords) where security-relevant.
3. **Medium** · Quantum-vulnerable RedDSA: transaction and message signing (5 file(s)) (QSI-2026-43765) · *preliminary*\
   What to do: Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains…
4. **Medium** · rsa 0.9.10 is affected by RUSTSEC-2023-0071 (CVE-2023-49092) (QSI-2026-43785)\
   What to do: Upgrade to a fixed version (0.10.0).

33 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · transaction and message signing | RedDSA | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum… |

## Known vulnerable components

Advisories for the versions in use: 35; unlikely to apply to this build: 25 (a Cargo feature that is off, affected functions not named in the code, or a platform that is not built); to review: 10.

Analyst review: 1 confirmed, 0 not applicable, 0 dismissed as false positives. (QSI review, 2026-10-23)

---

Static review of source code and manifests; files analysed: 350. No requests were sent to the owner's systems.

Full report, content SHA-256: `52fd61e7e75141f6f28c3dc1599e0b41ea8f5b28e3272d60d0df25ccae0b76fd`

Full report signature (report.sig.json): Ed25519 key, then the ML-DSA-65 one where it co-signs, SHA-256 fingerprints `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e · ML-DSA-65 dbd4e297b3213d1d7577a565e76de14cc5ad0e409f1dc68291c67266fc95066a`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.