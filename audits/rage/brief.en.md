# Post-quantum cryptography review: rage @ b5b68c4f4f7e

*One-page brief* · Reviewed: 2026-10-28 12:48 UTC · Risk profile: Security software vendor · Client: str4d (rage / age encryption) — public repository (passive review)

Source: https://github.com/str4d/rage/tree/b5b68c4f4f7ea5c368bc060f6fe0237549c3a13f

**Post-quantum maturity:** Level 1 of 4 — post-quantum code present, not wired. **Next step:** Wire the existing post-quantum primitive into a critical path (key wrapping or the channel) behind a hybrid construction, and test interoperability.

**Findings:** Critical 1 · High 1 · Medium 3 · Low 18 · Info 3

**Quantum timeline (Mosca: x + y − z):** Key establishment 10 + 3 − 8 = 5 → too late; Signatures 5 + 3 − 8 = 0 → tight

## What matters most

1. **Critical** · zip 8.6.0 is affected by RUSTSEC-2026-0369 (QSI-2026-04937)\
   What to do: Upgrade to a fixed version (9.0.0).
2. **High** · zip 8.6.0 is affected by RUSTSEC-2026-0367 (QSI-2026-04935)\
   What to do: Upgrade to a fixed version (9.0.0).
3. **Medium** · rsa 0.10.0-rc.18 is affected by RUSTSEC-2023-0071 (CVE-2023-49092) (QSI-2026-04934)\
   What to do: Upgrade to a fixed version (none published yet; see the advisory for mitigations).
4. **Medium** · Quantum-vulnerable X25519: key wrapping and data encryption at rest (3 file(s)) (QSI-2026-04928) · *preliminary*\
   What to do: Wrap keys with ML-KEM or a hybrid KEM (X25519 + ML-KEM-768) and re-wrap the stored keys; data that may already have been copied needs its…

19 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · key wrapping and data encryption at rest | X25519 | Wrap keys with ML-KEM or a hybrid KEM (X25519 + ML-KEM-768) and re-wrap the stored keys; data that may… |
| **Low** · authentication and identity (certificates, tokens, device attestation) | RSA | Keep credentials short-lived and plan ML-DSA certificates, tokens and keys as the ecosystem supports them |
| **Medium** · role not determined | X25519 | Classify each usage, record data lifetimes, and plan migration to Hybrid key establishment with ML-KEM (FIPS… |

## Known vulnerable components

Advisories for the versions in use: 20; unlikely to apply to this build: 13 (a Cargo feature that is off, affected functions not named in the code, or a platform that is not built); to review: 7.

---

Static review of source code and manifests; files analysed: 54. No requests were sent to the owner's systems.

Full report, content SHA-256: `ccf0d5cdc01d4ae253800f38b6649385c95e635670a1525a81a7ba2dd7702868`

Full report signature (report.sig.json): Ed25519 key, SHA-256 fingerprint `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.