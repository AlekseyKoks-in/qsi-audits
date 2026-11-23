# Post-quantum cryptography review: reown-appkit @ 8f9f39f1dfe0

*One-page brief* · Reviewed: 2026-11-23 13:02 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: Reown (ex-WalletConnect) — public repository (passive review)

Source: https://github.com/reown-com/appkit/tree/8f9f39f1dfe0a21bb619dd9a33b6d7500523298b

**Post-quantum maturity:** Level 0 of 4 — no post-quantum cryptography. **Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

**Findings:** Critical 20 · High 135 · Medium 199 · Low 42 · Info 2

**Quantum timeline (Mosca: x + y − z):** Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **Critical** · bitcoinjs-lib 6.1.7 is affected by GHSA-8vv3-6qpc-gpw6 (CVE-2026-107846) (QSI-2026-42857)\
   What to do: Upgrade to a fixed version (5.2.1, 6.1.8, 7.0.2).
2. **Critical** · storybook 9.0.15 is affected by GHSA-f2ph-cmg5-wxc8 (CVE-2026-114125) (QSI-2026-42862)\
   What to do: Upgrade to a fixed version (10.6.2, 11.0.0-alpha.6, 8.6.19, 9.1.21).
3. **Critical** · bitcoinjs-lib 7.0.0-rc.0 is affected by GHSA-8vv3-6qpc-gpw6 (CVE-2026-107846) (QSI-2026-42885)\
   What to do: Upgrade to a fixed version (5.2.1, 6.1.8, 7.0.2).
4. **Critical** · next 15.5.9 is affected by GHSA-2464-fhr4-w9xw (QSI-2026-42886)\
   What to do: Upgrade to a fixed version (15.5.28, 16.4.1).

392 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · transaction and message signing | ECDSA | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum… |
| **Medium** · role not determined | ECDSA | Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205)… |

## Known vulnerable components

Advisories for the versions in use: 393; each needs checking against the code.

---

Static review of source code and manifests; files analysed: 1249. No requests were sent to the owner's systems.

Full report, content SHA-256: `714c38e1c9fb8f7a1bf6109db39ac33e7f24dab7dd2171641b331c64e8b17c40`

Full report signature (report.sig.json): Ed25519 key, then the ML-DSA-65 one where it co-signs, SHA-256 fingerprints `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e · ML-DSA-65 dbd4e297b3213d1d7577a565e76de14cc5ad0e409f1dc68291c67266fc95066a`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.