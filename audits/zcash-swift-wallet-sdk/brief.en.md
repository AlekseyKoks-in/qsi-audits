# Post-quantum cryptography review: zcash-swift-wallet-sdk @ 4895ee058da9

*One-page brief* · Reviewed: 2026-10-28 13:03 UTC · Risk profile: Small technology company · Client: Electric Coin Company (Zcash) — public repository (passive review)

Source: https://github.com/zcash/zcash-swift-wallet-sdk/tree/4895ee058da99971057cceb80f36b8909656a8a9

**Post-quantum maturity:** Level 0 of 4 — no post-quantum cryptography. **Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

**Findings:** Critical 0 · High 0 · Medium 7 · Low 21 · Info 4

**Quantum timeline (Mosca: x + y − z):** Key establishment 5 + 3 − 12 = -4 → time available

## What matters most

1. **Medium** · block-buffer 0.10.4 is affected by GHSA-qwgh-2vcv-g2f7 (QSI-2026-05216)\
   What to do: Upgrade to a fixed version (none published yet; see the advisory for mitigations).
2. **Medium** · block-buffer 0.11.0-rc.3 is affected by GHSA-qwgh-2vcv-g2f7 (QSI-2026-05217)\
   What to do: Upgrade to a fixed version (none published yet; see the advisory for mitigations).
3. **Medium** · rsa 0.9.10 is affected by RUSTSEC-2023-0071 (CVE-2023-49092) (QSI-2026-05222)\
   What to do: Upgrade to a fixed version (none published yet; see the advisory for mitigations).
4. **Medium** · rustls 0.23.42 is affected by GHSA-2mjx-qc3c-rqvc (RUSTSEC-2026-0285) (QSI-2026-05223)\
   What to do: Upgrade to a fixed version (0.23.45).
5. **Medium** · rustls 0.23.42 is affected by GHSA-c8m5-c952-6cm4 (RUSTSEC-2026-0346) (QSI-2026-05224)\
   What to do: Upgrade to a fixed version (0.23.46, 0.24.0-dev.2).
6. **Medium** · serde_with 3.17.0 is affected by GHSA-7gcf-g7xr-8hxj (QSI-2026-05227)\
   What to do: Upgrade to a fixed version (3.21.0).

22 more in the full report.

## Known vulnerable components

Advisories for the versions in use: 27; unlikely to apply to this build: 16 (a Cargo feature that is off, affected functions not named in the code, or a platform that is not built); to review: 11.

---

Static review of source code and manifests; files analysed: 205. No requests were sent to the owner's systems.

Full report, content SHA-256: `3f9395ecdc760e1d1fbe874a5b0e9954a776e0a678451db32e9a30253ad81a7f`

Full report signature (report.sig.json): Ed25519 key, SHA-256 fingerprint `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.