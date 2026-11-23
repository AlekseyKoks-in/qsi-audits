# Post-quantum cryptography review: scroll @ 3046bbd18a6a

*One-page brief* · Reviewed: 2026-11-23 13:10 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: scroll — public repository (passive review)

Source: https://github.com/scroll-tech/scroll/tree/3046bbd18a6a05bf29dd3ffef7b5676203201050

**Post-quantum maturity:** Level 4 of 4 — post-quantum by default in the critical paths. **Next step:** Keep the inventory current and review new code paths before release.

**Findings:** Critical 3 · High 35 · Medium 40 · Low 58 · Info 142

**Quantum timeline (Mosca: x + y − z):** Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **Critical** · github.com/gin-contrib/cors v1.5.0 is affected by GHSA-869c-j7wc-8jqv (CVE-2019-25211, GO-2024-2955) (QSI-2026-43424)\
   What to do: Upgrade to a fixed version (1.6.0).
2. **Critical** · proxy-addr 2.0.7 is affected by GHSA-jqcg-44mw-7w3h (CVE-2026-90711) (QSI-2026-43568)\
   What to do: Upgrade to a fixed version (2.0.8).
3. **Critical** · underscore 1.9.1 is affected by GHSA-cf4h-3jhx-xvhq (CVE-2021-23358) (QSI-2026-43588)\
   What to do: Upgrade to a fixed version (1.12.1).
4. **High** · TLS certificate verification disabled in bridge-history-api/cmd/api/app/app.go (QSI-2026-43319)\
   What to do: Remove the override; use a proper CA bundle or pinning.

132 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · transaction and message signing | ECDSA | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum… |
| **Medium** · authentication and identity (certificates, tokens, device attestation) | ECDSA | Keep credentials short-lived and plan ML-DSA certificates, tokens and keys as the ecosystem supports them |
| **Medium** · role not determined | ECDSA | Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205)… |

## Known vulnerable components

Advisories for the versions in use: 216; unlikely to apply to this build: 110 (a Cargo feature that is off, affected functions not named in the code, or a platform that is not built); to review: 106.

---

Static review of source code and manifests; files analysed: 389. No requests were sent to the owner's systems.

Full report, content SHA-256: `dc1fe0629d33bc2e69b7d2e32ad7d8b931deea4de933dbe0ad6f687453612b15`

Full report signature (report.sig.json): Ed25519 key, then the ML-DSA-65 one where it co-signs, SHA-256 fingerprints `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e · ML-DSA-65 dbd4e297b3213d1d7577a565e76de14cc5ad0e409f1dc68291c67266fc95066a`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.