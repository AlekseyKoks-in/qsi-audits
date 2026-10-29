# Post-quantum cryptography review: scroll @ 3046bbd18a6a

*One-page brief* · Reviewed: 2026-10-29 06:18 UTC · Risk profile: Web3 project · Client: Scroll — public repository (passive review)

Source: https://github.com/scroll-tech/scroll/tree/3046bbd18a6a05bf29dd3ffef7b5676203201050

**Post-quantum maturity:** Level 0 of 4 — no post-quantum cryptography. **Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

**Findings:** Critical 1 · High 9 · Medium 13 · Low 35 · Info 57

**Quantum timeline (Mosca: x + y − z):** Signatures 10 + 5 − 12 = 3 → too late

## What matters most

1. **Critical** · github.com/gin-contrib/cors v1.5.0 is affected by GHSA-869c-j7wc-8jqv (CVE-2019-25211, GO-2024-2955) (QSI-2026-06635)\
   What to do: Upgrade to a fixed version (1.6.0).
2. **High** · TLS certificate verification disabled in bridge-history-api/cmd/api/app/app.go (QSI-2026-06538)\
   What to do: Remove the override; use a proper CA bundle or pinning.
3. **High** · github.com/btcsuite/btcd v0.20.1-beta is affected by GHSA-27vh-h6mc-q6g8 (CVE-2024-38365… (QSI-2026-06636)\
   What to do: Upgrade to a fixed version (0.24.2-beta.rc1).
4. **High** · Possible reentrancy (external call before state update) in… (QSI-2026-06547) · *preliminary*\
   What to do: Apply checks-effects-interactions and/or ReentrancyGuard.

54 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · transaction and message signing | ECDSA | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum… |
| **Medium** · authentication and identity (certificates, tokens, device attestation) | ECDSA | Keep credentials short-lived and plan ML-DSA certificates, tokens and keys as the ecosystem supports them |
| **Medium** · role not determined | ECDSA | Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205)… |

## Known vulnerable components

Advisories for the versions in use: 57; unlikely to apply to this build: 29 (a Cargo feature that is off, affected functions not named in the code, or a platform that is not built); to review: 28.

---

Static review of source code and manifests; files analysed: 387. No requests were sent to the owner's systems.

Full report, content SHA-256: `bfe57c31bc57c669da6e4a7cee997a8bd19fd26d0a62a5decfc2255b7452d9bb`

Full report signature (report.sig.json): Ed25519 key, SHA-256 fingerprint `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.