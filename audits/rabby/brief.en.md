# Post-quantum cryptography review: rabby @ 663c0e80e9f6

*One-page brief* · Reviewed: 2026-11-17 18:49 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: Rabby Wallet (DeBank) — public repository (passive review)

Source: https://github.com/RabbyHub/Rabby/tree/663c0e80e9f6139cbb87932ddea909e1e4a382f1

**Post-quantum maturity:** Level 0 of 4 — no post-quantum cryptography. **Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

**Findings:** Critical 7 · High 167 · Medium 160 · Low 13 · Info 3

**Quantum timeline (Mosca: x + y − z):** Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **Critical** · @openzeppelin/contracts 3.4.1-solc-0.7-2 is affected by GHSA-fg47-3c2x-m2wr (CVE-2021-39167) (QSI-2026-27541)\
   What to do: Upgrade to a fixed version (3.4.2, 4.3.1).
2. **Critical** · @openzeppelin/contracts 3.4.2-solc-0.7 is affected by GHSA-fg47-3c2x-m2wr (CVE-2021-39167) (QSI-2026-27545)\
   What to do: Upgrade to a fixed version (3.4.2, 4.3.1).
3. **Critical** · elliptic 6.5.4 is affected by GHSA-vjh7-7g9h-fjfh (QSI-2026-27715)\
   What to do: Upgrade to a fixed version (6.6.1).
4. **Critical** · elliptic 6.5.7 is affected by GHSA-vjh7-7g9h-fjfh (QSI-2026-27718)\
   What to do: Upgrade to a fixed version (6.6.1).

343 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · transaction and message signing | ECDSA | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum… |
| **Medium** · role not determined | ECDSA | Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205)… |

## Known vulnerable components

Advisories for the versions in use: 344; each needs checking against the code.

---

Static review of source code and manifests; files analysed: 1694. No requests were sent to the owner's systems.

Full report, content SHA-256: `0d3818447ade0de153f5c097e5f2041bcbe1354c6f042e46eef0d6a8d7faf9fd`

Full report signature (report.sig.json): Ed25519 key, then the ML-DSA-65 one where it co-signs, SHA-256 fingerprints `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e · ML-DSA-65 dbd4e297b3213d1d7577a565e76de14cc5ad0e409f1dc68291c67266fc95066a`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.