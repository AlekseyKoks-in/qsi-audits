# Post-quantum cryptography review: sigstore-js @ 769a53d87132

*One-page brief* · Reviewed: 2026-11-23 13:16 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: Sigstore project — public repository (passive review)

Source: https://github.com/sigstore/sigstore-js/tree/769a53d8713248a8bf49edfc2a5d1955b0dcc24d

**Post-quantum maturity:** Level 0 of 4 — no post-quantum cryptography. **Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

**Findings:** Critical 1 · High 9 · Medium 15 · Low 2 · Info 2

**Quantum timeline (Mosca: x + y − z):** Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **Critical** · proxy-addr 2.0.7 is affected by GHSA-jqcg-44mw-7w3h (CVE-2026-90711) (QSI-2026-43670)\
   What to do: Upgrade to a fixed version (2.0.8).
2. **High** · Private key material present in packages/cli/src/signer.ts (QSI-2026-43648)\
   What to do: Treat the key as compromised: rotate it, revoke associated certificates, remove it from version history and store keys in a secrets…
3. **High** · Certificate has expired ((empty)) (QSI-2026-43646)\
   What to do: Renew the certificate and automate renewal (e.g. ACME) with expiry monitoring.
4. **High** · brace-expansion 5.0.9 is affected by GHSA-6j4f-fj2g-mc7p (CVE-2026-102276) (QSI-2026-43652)\
   What to do: Upgrade to a fixed version (1.1.19, 2.1.5, 3.0.7, 5.0.10).

23 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · role not determined | ECDSA | Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205)… |

## Known vulnerable components

Advisories for the versions in use: 22; each needs checking against the code.

---

Static review of source code and manifests; files analysed: 180. No requests were sent to the owner's systems.

Full report, content SHA-256: `a5a4680f90889063630ae364d3bf304903749f7b1b18cbc74f26d97c07a06c7d`

Full report signature (report.sig.json): Ed25519 key, then the ML-DSA-65 one where it co-signs, SHA-256 fingerprints `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e · ML-DSA-65 dbd4e297b3213d1d7577a565e76de14cc5ad0e409f1dc68291c67266fc95066a`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.