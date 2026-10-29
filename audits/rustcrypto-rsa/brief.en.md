# Post-quantum cryptography review: rustcrypto-rsa @ f96c4b5d629a

*One-page brief* · Reviewed: 2026-10-28 12:51 UTC · Risk profile: Security software vendor · Client: RustCrypto project — public repository (passive review)

Source: https://github.com/RustCrypto/RSA/tree/f96c4b5d629a0aeb6f680294debfd38ec8a81f68

**Post-quantum maturity:** Level 0 of 4 — no post-quantum cryptography. **Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

**Findings:** Critical 0 · High 0 · Medium 1 · Low 2 · Info 1

**Quantum timeline (Mosca: x + y − z):** Key establishment 10 + 3 − 8 = 5 → too late

## What matters most

1. **Medium** · Quantum-vulnerable RSA: role not determined (5 file(s)) (QSI-2026-05056) · *preliminary*\
   What to do: Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form…
2. **Low** · crypto-bigint 0.7.5 is affected by RUSTSEC-2026-0387 (no severity rating) (QSI-2026-05058) · *preliminary*\
   What to do: Triage the advisory; upgrade to a fixed version (0.7.6) if it applies.
3. **Low** · ctutils 0.4.2 is affected by RUSTSEC-2026-0385 (no severity rating) (QSI-2026-05059) · *preliminary*\
   What to do: Triage the advisory; upgrade to a fixed version (0.4.4) if it applies.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · role not determined | RSA | Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205)… |

## Known vulnerable components

Advisories for the versions in use: 2; each needs checking against the code.

---

Static review of source code and manifests; files analysed: 35. No requests were sent to the owner's systems.

Full report, content SHA-256: `c0d439a694ce1e368fd2f36235910d4b8fb8e439d2c8ee8f0b7a317d4baa0ae1`

Full report signature (report.sig.json): Ed25519 key, SHA-256 fingerprint `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.