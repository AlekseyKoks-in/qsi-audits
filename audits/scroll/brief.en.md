# Post-quantum cryptography review: scroll @ 3046bbd18a6a

*One-page brief* · Reviewed: 2026-11-04 19:23 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: Scroll — public repository (passive review)

Source: https://github.com/scroll-tech/scroll/tree/3046bbd18a6a05bf29dd3ffef7b5676203201050

**Post-quantum maturity:** Level 0 of 4 — no post-quantum cryptography. **Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

**Findings:** Critical 8 · High 17 · Medium 24 · Low 43 · Info 79

**Quantum timeline (Mosca: x + y − z):** Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **Critical** · github.com/gin-contrib/cors v1.5.0 is affected by GHSA-869c-j7wc-8jqv (CVE-2019-25211, GO-2024-2955) (QSI-2026-12737)\
   What to do: Upgrade to a fixed version (1.6.0).
2. **Critical** · golang.org/x/crypto v0.32.0 is affected by GHSA-5cgq-3rg8-m6cv (CVE-2026-42508) (QSI-2026-12756)\
   What to do: Upgrade to a fixed version (0.52.0).
3. **Critical** · golang.org/x/crypto v0.32.0 is affected by GHSA-89gr-r52h-f8rx (CVE-2026-39831) (QSI-2026-12758)\
   What to do: Upgrade to a fixed version (0.52.0).
4. **Critical** · golang.org/x/crypto v0.32.0 is affected by GHSA-f5wc-c3c7-36mc (CVE-2026-39832) (QSI-2026-12760)\
   What to do: Upgrade to a fixed version (0.52.0).

88 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · transaction and message signing | ECDSA | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum… |
| **Medium** · authentication and identity (certificates, tokens, device attestation) | ECDSA | Keep credentials short-lived and plan ML-DSA certificates, tokens and keys as the ecosystem supports them |
| **Medium** · role not determined | ECDSA | Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205)… |

## Known vulnerable components

Advisories for the versions in use: 113; unlikely to apply to this build: 51 (a Cargo feature that is off, affected functions not named in the code, or a platform that is not built); to review: 62.

---

Static review of source code and manifests; files analysed: 387. No requests were sent to the owner's systems.

Full report, content SHA-256: `4897e726a15e304768c5ebf2af71de58f62cb3bb57cf67be7e269af631545ec2`

Full report signature (report.sig.json): Ed25519 key, SHA-256 fingerprint `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.