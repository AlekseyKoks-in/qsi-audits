# Post-quantum cryptography review: scroll @ 3046bbd18a6a

*One-page brief* · Reviewed: 2026-11-24 17:22 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: scroll — public repository (passive review)

Source: https://github.com/scroll-tech/scroll/tree/3046bbd18a6a05bf29dd3ffef7b5676203201050

**Post-quantum maturity:** Level 3 of 4 — hybrid protection in a critical path. **Next step:** Pin the toolchain version and set the TLS groups in the code (X25519MLKEM768 first): the hybrid key exchange found rests on a default the code does not show, and a toolchain or library change would change it.

**Findings:** Critical 5 · High 26 · Medium 33 · Low 65 · Info 142 (of them advisories unlikely to apply: 110)

**Quantum timeline (Mosca: x + y − z):** Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **Critical** · github.com/gin-contrib/cors v1.5.0 is affected by GHSA-869c-j7wc-8jqv (CVE-2019-25211, GO-2024-2955) (QSI-2026-50810)\
   What to do: Upgrade to a fixed version (1.6.0).
2. **Critical** · golang.org/x/crypto v0.32.0 is affected by GHSA-f5wc-c3c7-36mc (CVE-2026-39832, GO-2026-5006) (QSI-2026-50834)\
   What to do: Upgrade to a fixed version (0.52.0).
3. **Critical** · proxy-addr 2.0.7 is affected by GHSA-jqcg-44mw-7w3h (CVE-2026-90711) (QSI-2026-50951)\
   What to do: Upgrade to a fixed version (2.0.8).
4. **Critical** · underscore 1.9.1 is affected by GHSA-cf4h-3jhx-xvhq (CVE-2021-23358) (QSI-2026-50971)\
   What to do: Upgrade to a fixed version (1.12.1).

125 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · transaction and message signing | ECDSA | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum… |
| **Medium** · authentication and identity (certificates, tokens, device attestation) | ECDSA | Keep credentials short-lived and plan ML-DSA certificates, tokens and keys as the ecosystem supports them |
| **Medium** · role not determined | ECDSA | Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205)… |

## Known vulnerable components

Advisories for the versions in use: 213; unlikely to apply to this build: 110 (no call path to the affected code, a module only tests use, functions not named in the code, a Cargo feature that is off or a platform not built); to review: 103.

Analyst review: 0 confirmed, 0 not applicable, 4 dismissed as false positives. (QSI review, 2026-11-24)

---

Static review of source code and manifests; files analysed: 385. No requests were sent to the owner's systems.

Full report, content SHA-256: `b66307f2b2bc454e65fcd895e9d042e915ba094dcaa747a4b18b64c10d95f7ed`

Full report signature (report.sig.json): Ed25519 key, then the ML-DSA-65 one where it co-signs, SHA-256 fingerprints `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e · ML-DSA-65 dbd4e297b3213d1d7577a565e76de14cc5ad0e409f1dc68291c67266fc95066a`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.