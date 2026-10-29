# Post-quantum cryptography review: rabby @ 663c0e80e9f6

*One-page brief* · Reviewed: 2026-10-28 18:13 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: Rabby Wallet (DeBank) — public repository (passive review)

Source: https://github.com/RabbyHub/Rabby/tree/663c0e80e9f6139cbb87932ddea909e1e4a382f1

**Post-quantum maturity:** Level 0 of 4 — no post-quantum cryptography. **Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

**Findings:** Critical 2 · High 74 · Medium 78 · Low 3 · Info 3

**Quantum timeline (Mosca: x + y − z):** Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **Critical** · @openzeppelin/contracts 3.4.1-solc-0.7-2 is affected by GHSA-fg47-3c2x-m2wr (CVE-2021-39167) (QSI-2026-05639)\
   What to do: Upgrade to a fixed version (3.4.2, 4.3.1).
2. **Critical** · @openzeppelin/contracts 3.4.2-solc-0.7 is affected by GHSA-fg47-3c2x-m2wr (CVE-2021-39167) (QSI-2026-05643)\
   What to do: Upgrade to a fixed version (3.4.2, 4.3.1).
3. **High** · fflate 0.8.2 is affected by GHSA-px8p-9vwx-vf98 (CVE-2026-45820) (QSI-2026-05625)\
   What to do: Upgrade to a fixed version (0.4.9, 0.5.4, 0.6.11, 0.7.5, 0.8.3).
4. **High** · lodash 4.17.21 is affected by GHSA-r5fr-rjxr-66jc (CVE-2026-4800) (QSI-2026-05627)\
   What to do: Upgrade to a fixed version (4.18.0).

153 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · transaction and message signing | ECDSA | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum… |
| **Medium** · role not determined | ECDSA | Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205)… |

## Known vulnerable components

Advisories for the versions in use: 154; each needs checking against the code.

---

Static review of source code and manifests; files analysed: 1694. No requests were sent to the owner's systems.

Full report, content SHA-256: `cd71a6408082cfedd9f571cc9cd9d48a53b708d27b8a87e76466454bfa56cbf9`

Full report signature (report.sig.json): Ed25519 key, SHA-256 fingerprint `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.