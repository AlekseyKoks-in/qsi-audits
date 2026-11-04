# Post-quantum cryptography review: lido-core @ 2bd532298d85

*One-page brief* · Reviewed: 2026-11-04 18:57 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: Lido — public repository (passive review)

Source: https://github.com/lidofinance/core/tree/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3

**Post-quantum maturity:** Level 0 of 4 — no post-quantum cryptography. **Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

**Findings:** Critical 5 · High 26 · Medium 28 · Low 12 · Info 7

**Quantum timeline (Mosca: x + y − z):** Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **Critical** · @openzeppelin/contracts 3.4.0 is affected by GHSA-fg47-3c2x-m2wr (CVE-2021-39167) (QSI-2026-12121)\
   What to do: Upgrade to a fixed version (3.4.2, 4.3.1).
2. **Critical** · babel-traverse 6.26.0 is affected by GHSA-67hx-6x53-jw92 (CVE-2023-45133) (QSI-2026-12127)\
   What to do: Upgrade to a fixed version (none published yet; see the advisory for mitigations).
3. **Critical** · crypto-js 3.3.0 is affected by GHSA-rg76-677x-56q9 (CVE-2026-71851) (QSI-2026-12145)\
   What to do: Upgrade to a fixed version (4.0.0).
4. **Critical** · crypto-js 3.3.0 is affected by GHSA-xwcq-pm8m-c4vf (CVE-2023-46233) (QSI-2026-12146)\
   What to do: Upgrade to a fixed version (4.2.0).

67 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · transaction and message signing | ECDSA | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum… |
| **Medium** · role not determined | BLS12-381, ECDSA | Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205)… |

## Known vulnerable components

Advisories for the versions in use: 47; each needs checking against the code.

---

Static review of source code and manifests; files analysed: 267. No requests were sent to the owner's systems.

Full report, content SHA-256: `f46bf3d63c32c5a0d4fa4432f9eed9ee7d601c840b1c9185e9171cf86cc18391`

Full report signature (report.sig.json): Ed25519 key, SHA-256 fingerprint `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.