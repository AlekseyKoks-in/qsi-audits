# Post-quantum cryptography review: metamask-extension @ d2db7ee9a19b

*One-page brief* · Reviewed: 2026-11-23 12:44 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: MetaMask (Consensys) — public repository (passive review)

Source: https://github.com/MetaMask/metamask-extension/tree/d2db7ee9a19b0322105618521370ab690911209f

**Post-quantum maturity:** Level 0 of 4 — no post-quantum cryptography. **Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

**Findings:** Critical 1 · High 32 · Medium 56 · Low 11 · Info 2

**Quantum timeline (Mosca: x + y − z):** Key establishment 10 + 5 − 8 = 7 → too late; Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **Critical** · bitcoinjs-lib 7.0.1 is affected by GHSA-8vv3-6qpc-gpw6 (CVE-2026-107846) (QSI-2026-42267)\
   What to do: Upgrade to a fixed version (5.2.1, 6.1.8, 7.0.2).
2. **High** · nanoid 2.1.11 is affected by GHSA-xwg4-73v4-xw9w (CVE-2026-73086) (QSI-2026-42323)\
   What to do: Upgrade to a fixed version (3.3.12, 5.1.11).
3. **High** · postcss 7.0.39 is affected by GHSA-6g55-p6wh-862q (CVE-2026-45623) (QSI-2026-42324)\
   What to do: Upgrade to a fixed version (8.5.12).
4. **High** · postcss 7.0.39 is affected by GHSA-r28c-9q8g-f849 (CVE-2026-73646) (QSI-2026-42328)\
   What to do: Upgrade to a fixed version (8.5.18).

96 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · transaction and message signing | ECDSA | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum… |
| **Medium** · role not determined | ECDSA, ECDH | Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205)… |

## Known vulnerable components

Advisories for the versions in use: 94; each needs checking against the code.

---

Static review of source code and manifests; files analysed: 4870. No requests were sent to the owner's systems.

Full report, content SHA-256: `b0a22dca7397a1b5d36312851dbbe7eb91a4c84595f609898d15e02ca6516893`

Full report signature (report.sig.json): Ed25519 key, then the ML-DSA-65 one where it co-signs, SHA-256 fingerprints `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e · ML-DSA-65 dbd4e297b3213d1d7577a565e76de14cc5ad0e409f1dc68291c67266fc95066a`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.