# Post-quantum cryptography review: zcash-android-wallet-sdk @ a95780ac00e0

*One-page brief* · Reviewed: 2026-10-28 13:02 UTC · Risk profile: Small technology company · Client: Electric Coin Company (Zcash) — public repository (passive review)

Source: https://github.com/zcash/zcash-android-wallet-sdk/tree/a95780ac00e0198c111c6e701126e6688f64a12a

**Post-quantum maturity:** Level 0 of 4 — no post-quantum cryptography. **Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

**Findings:** Critical 0 · High 0 · Medium 6 · Low 21 · Info 6

**Quantum timeline (Mosca: x + y − z):** Key establishment 5 + 3 − 12 = -4 → time available

## What matters most

1. **Medium** · SHA-1 used in backend-lib/src/main/java/cash/z/ecc/android/sdk/internal/ext/FileExt.kt (QSI-2026-05179) · *confirmed by the analyst*\
   What to do: Replace with SHA-256/SHA-3 (or Argon2/bcrypt for passwords) where security-relevant.
2. **Medium** · block-buffer 0.10.4 is affected by GHSA-qwgh-2vcv-g2f7 (QSI-2026-05184)\
   What to do: Upgrade to a fixed version (none published yet; see the advisory for mitigations).
3. **Medium** · block-buffer 0.11.0-rc.3 is affected by GHSA-qwgh-2vcv-g2f7 (QSI-2026-05185)\
   What to do: Upgrade to a fixed version (none published yet; see the advisory for mitigations).
4. **Medium** · rsa 0.9.10 is affected by RUSTSEC-2023-0071 (CVE-2023-49092) (QSI-2026-05189)\
   What to do: Upgrade to a fixed version (none published yet; see the advisory for mitigations).
5. **Medium** · rustls 0.23.43 is affected by GHSA-2mjx-qc3c-rqvc (RUSTSEC-2026-0285) (QSI-2026-05190)\
   What to do: Upgrade to a fixed version (0.23.45).
6. **Medium** · rustls 0.23.43 is affected by GHSA-c8m5-c952-6cm4 (RUSTSEC-2026-0346) (QSI-2026-05191)\
   What to do: Upgrade to a fixed version (0.23.46, 0.24.0-dev.2).

21 more in the full report.

## Known vulnerable components

Advisories for the versions in use: 26; unlikely to apply to this build: 16 (a Cargo feature that is off, affected functions not named in the code, or a platform that is not built); to review: 10.

Analyst review: 1 confirmed, 0 not applicable, 0 dismissed as false positives. (QSI review, 2026-10-23)

---

Static review of source code and manifests; files analysed: 350. No requests were sent to the owner's systems.

Full report, content SHA-256: `d2c9af625f49db5cb717298783cbe2869e143e524920ee5efa91cd94399bd0e6`

Full report signature (report.sig.json): Ed25519 key, SHA-256 fingerprint `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.