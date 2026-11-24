# Post-quantum cryptography review: rage @ b5b68c4f4f7e

*One-page brief* · Reviewed: 2026-11-24 11:04 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: str4d (rage / age encryption) — public repository (passive review)

Source: https://github.com/str4d/rage/tree/b5b68c4f4f7ea5c368bc060f6fe0237549c3a13f

**Post-quantum maturity:** Level 1 of 4 — post-quantum code present, not wired. **Next step:** Wire the existing post-quantum primitive into a critical path (key wrapping or the channel) behind a hybrid construction, and test interoperability.

**Findings:** Critical 2 · High 4 · Medium 5 · Low 18 · Info 5 (of them advisories unlikely to apply: 14)

**Quantum timeline (Mosca: x + y − z):** Key establishment 10 + 5 − 8 = 7 → too late; Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **Critical** · zip 8.6.0 is affected by GHSA-m665-v7pm-7grj (CVE-2026-115905, RUSTSEC-2026-0548) (QSI-2026-48769)\
   What to do: Upgrade to a fixed version (9.0.5).
2. **Medium** · Quantum-vulnerable X25519: key wrapping and data encryption at rest (4 file(s)) (QSI-2026-48756) · *preliminary*\
   What to do: Wrap keys with ML-KEM or a hybrid KEM (X25519 + ML-KEM-768) and re-wrap the stored keys; data that may already have been copied needs its…
3. **Medium** · Quantum-vulnerable X25519: role not determined (5 file(s)) (QSI-2026-48755) · *preliminary*\
   What to do: Classify each usage, record data lifetimes, and plan migration to Hybrid key establishment with ML-KEM (FIPS 203), e.g. X25519MLKEM768 in…
4. **Medium** · Quantum-vulnerable RSA: authentication and identity (certificates, tokens, device attestation) (3… (QSI-2026-48757) · *preliminary*\
   What to do: Keep credentials short-lived and plan ML-DSA certificates, tokens and keys as the ecosystem supports them.

25 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · key wrapping and data encryption at rest | X25519 | Wrap keys with ML-KEM or a hybrid KEM (X25519 + ML-KEM-768) and re-wrap the stored keys; data that may… |
| **Medium** · authentication and identity (certificates, tokens, device attestation) | RSA | Keep credentials short-lived and plan ML-DSA certificates, tokens and keys as the ecosystem supports them |
| **Medium** · role not determined | X25519 | Classify each usage, record data lifetimes, and plan migration to Hybrid key establishment with ML-KEM (FIPS… |

## Known vulnerable components

Advisories for the versions in use: 26; unlikely to apply to this build: 14 (no call path to the affected code, a module only tests use, functions not named in the code, a Cargo feature that is off or a platform not built); to review: 12.

---

Static review of source code and manifests; files analysed: 54. No requests were sent to the owner's systems.

Full report, content SHA-256: `4d39e37a98b4854df837d800c91a60ccad168a087cc70c077773fbb46b903334`

Full report signature (report.sig.json): Ed25519 key, then the ML-DSA-65 one where it co-signs, SHA-256 fingerprints `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e · ML-DSA-65 dbd4e297b3213d1d7577a565e76de14cc5ad0e409f1dc68291c67266fc95066a`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.