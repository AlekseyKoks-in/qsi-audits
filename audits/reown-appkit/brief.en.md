# Post-quantum cryptography review: reown-appkit @ 8f9f39f1dfe0

*One-page brief* · Reviewed: 2026-10-28 18:40 UTC · Risk profile: Web3 project · Client: Reown (ex-WalletConnect) — public repository (passive review)

Source: https://github.com/reown-com/appkit/tree/8f9f39f1dfe0a21bb619dd9a33b6d7500523298b

**Post-quantum maturity:** Level 0 of 4 — no post-quantum cryptography. **Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

**Findings:** Critical 9 · High 33 · Medium 54 · Low 5 · Info 2

**Quantum timeline (Mosca: x + y − z):** Signatures 10 + 5 − 12 = 3 → too late

## What matters most

1. **Critical** · storybook 9.0.15 is affected by GHSA-f2ph-cmg5-wxc8 (CVE-2026-114125) (QSI-2026-05990)\
   What to do: Upgrade to a fixed version (10.6.2, 11.0.0-alpha.6, 8.6.19, 9.1.21).
2. **Critical** · next 15.5.9 is affected by GHSA-2464-fhr4-w9xw (QSI-2026-06013)\
   What to do: Upgrade to a fixed version (15.5.28, 16.4.1).
3. **Critical** · next 15.5.9 is affected by GHSA-2xp9-vwfh-vxw4 (QSI-2026-06016)\
   What to do: Upgrade to a fixed version (15.5.24, 16.3.3).
4. **Critical** · next-auth 5.0.0-beta.29 is affected by GHSA-7rqj-j65f-68wh (CVE-2026-73420) (QSI-2026-06034)\
   What to do: Upgrade to a fixed version (4.24.15, 5.0.0-beta.32).

97 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · transaction and message signing | ECDSA | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum… |
| **Medium** · role not determined | ECDSA | Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205)… |

## Known vulnerable components

Advisories for the versions in use: 99; each needs checking against the code.

---

Static review of source code and manifests; files analysed: 1249. No requests were sent to the owner's systems.

Full report, content SHA-256: `9a4a12ceaaf420315869a8bf23c8b27c9c28ae606706d313eac55d1ed8f78f46`

Full report signature (report.sig.json): Ed25519 key, SHA-256 fingerprint `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.