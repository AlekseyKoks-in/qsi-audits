# Post-quantum cryptography review: scroll @ 3046bbd18a6a

*One-page brief* · Reviewed: 2026-11-07 18:39 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: scroll — public repository (passive review)

Source: https://github.com/scroll-tech/scroll/tree/3046bbd18a6a05bf29dd3ffef7b5676203201050

**Post-quantum maturity:** Level 4 of 4 — post-quantum by default in the critical paths. **Next step:** Keep the inventory current and review new code paths before release.

**Findings:** Critical 1 · High 14 · Medium 19 · Low 43 · Info 102

**Quantum timeline (Mosca: x + y − z):** Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **Critical** · github.com/gin-contrib/cors v1.5.0 is affected by GHSA-869c-j7wc-8jqv (CVE-2019-25211, GO-2024-2955) (QSI-2026-25386)\
   What to do: Upgrade to a fixed version (1.6.0).
2. **High** · TLS certificate verification disabled in bridge-history-api/cmd/api/app/app.go (QSI-2026-25289)\
   What to do: Remove the override; use a proper CA bundle or pinning.
3. **High** · github.com/docker/cli v25.0.4-0.20240305161310-2bf4225ad269+incompatible is affected by… (QSI-2026-25391)\
   What to do: Upgrade to a fixed version (29.2.0).
4. **High** · github.com/containerd/containerd v1.7.12 is affected by GHSA-pwhc-rpq9-4c8w (CVE-2024-25621… (QSI-2026-25453)\
   What to do: Upgrade to a fixed version (1.7.29).

73 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · transaction and message signing | ECDSA | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum… |
| **Medium** · authentication and identity (certificates, tokens, device attestation) | ECDSA | Keep credentials short-lived and plan ML-DSA certificates, tokens and keys as the ecosystem supports them |
| **Medium** · role not determined | ECDSA | Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205)… |

## Known vulnerable components

Advisories for the versions in use: 120; unlikely to apply to this build: 74 (a Cargo feature that is off, affected functions not named in the code, or a platform that is not built); to review: 46.

---

Static review of source code and manifests; files analysed: 387. No requests were sent to the owner's systems.

Full report, content SHA-256: `4fb555f1aacf1a15553dbb12fde83d11c84ae195fc3f8b64fd9a8ac90625d10a`

Full report signature (report.sig.json): Ed25519 key, SHA-256 fingerprint `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.