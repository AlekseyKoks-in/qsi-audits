# Post-quantum cryptography review: lido-core @ 2bd532298d85

*One-page brief* · Reviewed: 2026-11-24 10:42 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: Lido — public repository (passive review)

Source: https://github.com/lidofinance/core/tree/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3

**Post-quantum maturity:** Level 0 of 4 — no post-quantum cryptography. **Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

**Findings:** Critical 5 · High 38 · Medium 36 · Low 17 · Info 8

**Quantum timeline (Mosca: x + y − z):** Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **Critical** · @openzeppelin/contracts 3.4.0 is affected by GHSA-fg47-3c2x-m2wr (CVE-2021-39167) (QSI-2026-48092)\
   What to do: Upgrade to a fixed version (3.4.2, 4.3.1).
2. **Critical** · babel-traverse 6.26.0 is affected by GHSA-67hx-6x53-jw92 (CVE-2023-45133) (QSI-2026-48098)\
   What to do: Upgrade to a fixed version (none published yet; see the advisory for mitigations).
3. **Critical** · crypto-js 3.3.0 is affected by GHSA-rg76-677x-56q9 (CVE-2026-71851) (QSI-2026-48116)\
   What to do: Upgrade to a fixed version (4.0.0).
4. **Critical** · form-data 2.3.3 is affected by GHSA-fjxv-7rqg-78g4 (CVE-2025-7783) (QSI-2026-48119)\
   What to do: Upgrade to a fixed version (2.5.4, 3.0.4, 4.0.4).

92 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · transaction and message signing | ECDSA | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum… |
| **Medium** · role not determined | BLS12-381, ECDSA | Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205)… |

## Known vulnerable components

Advisories for the versions in use: 77; each needs checking against the code.

Analyst review: 0 confirmed, 1 not applicable, 0 dismissed as false positives. (QSI review, 2026-11-24)

---

Static review of source code and manifests; files analysed: 267. No requests were sent to the owner's systems.

Full report, content SHA-256: `9e0fb2adf6e3bded9ad5f1a7f223f120ec1bd9a5e3de14afe740286ec6de4084`

Full report signature (report.sig.json): Ed25519 key, then the ML-DSA-65 one where it co-signs, SHA-256 fingerprints `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e · ML-DSA-65 dbd4e297b3213d1d7577a565e76de14cc5ad0e409f1dc68291c67266fc95066a`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.