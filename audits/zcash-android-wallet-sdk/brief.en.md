# Post-quantum cryptography review: zcash-android-wallet-sdk @ a95780ac00e0

*One-page brief* · Reviewed: 2026-10-31 00:24 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: Electric Coin Company (Zcash) — public repository (passive review)

Source: https://github.com/zcash/zcash-android-wallet-sdk/tree/a95780ac00e0198c111c6e701126e6688f64a12a

**Post-quantum maturity:** Level 0 of 4 — no post-quantum cryptography. **Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

**Findings:** Critical 0 · High 0 · Medium 6 · Low 20 · Info 6

**Quantum timeline (Mosca: x + y − z):** Key establishment 10 + 5 − 8 = 7 → too late; Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **Medium** · Quantum-vulnerable RSA key (2048-bit) in responsible_disclosure.md (QSI-2026-09492)\
   What to do: Inventory and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it..
2. **Medium** · SHA-1 used in backend-lib/src/main/java/cash/z/ecc/android/sdk/internal/ext/FileExt.kt (QSI-2026-09490) · *confirmed by the analyst*\
   What to do: Replace with SHA-256/SHA-3 (or Argon2/bcrypt for passwords) where security-relevant.
3. **Medium** · Quantum-vulnerable RedDSA: authentication and identity (certificates, tokens, device attestation)… (QSI-2026-09491) · *preliminary*\
   What to do: Keep credentials short-lived and plan ML-DSA certificates, tokens and keys as the ecosystem supports them.
4. **Medium** · rsa 0.9.10 is affected by RUSTSEC-2023-0071 (CVE-2023-49092) (QSI-2026-09499)\
   What to do: Upgrade to a fixed version (none published yet; see the advisory for mitigations).

22 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · authentication and identity (certificates, tokens, device attestation) | RedDSA | Keep credentials short-lived and plan ML-DSA certificates, tokens and keys as the ecosystem supports them |

## Known vulnerable components

Advisories for the versions in use: 24; unlikely to apply to this build: 16 (a Cargo feature that is off, affected functions not named in the code, or a platform that is not built); to review: 8.

Analyst review: 1 confirmed, 0 not applicable, 0 dismissed as false positives. (QSI review, 2026-10-23)

---

Static review of source code and manifests; files analysed: 350. No requests were sent to the owner's systems.

Full report, content SHA-256: `ce90a169f94c05a032c889b746edd3f3afaf0360b549e3c77acfe50f8cef58fc`

Full report signature (report.sig.json): Ed25519 key, SHA-256 fingerprint `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.