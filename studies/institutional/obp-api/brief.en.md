# Post-quantum cryptography review: obp-api @ 6a4a13ef079f

*One-page brief* · Reviewed: 2026-11-24 12:00 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: TESOBE (Open Bank Project) — public repository (passive review)

Source: https://github.com/OpenBankProject/OBP-API/tree/6a4a13ef079fa33707f4ee3dba1e600570ed34b4

**Post-quantum maturity:** Level 0 of 4 — no post-quantum cryptography. **Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

**Findings:** Critical 0 · High 8 · Medium 12 · Low 5 · Info 7

**Quantum timeline (Mosca: x + y − z):** Key establishment 10 + 5 − 8 = 7 → too late; Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **High** · org.postgresql:postgresql 42.7.11 is affected by GHSA-j92g-9f8w-j867 (CVE-2026-54291) (QSI-2026-49955)\
   What to do: Upgrade to a fixed version (42.7.12).
2. **High** · org.xerial.snappy:snappy-java 1.1.10.4 is affected by GHSA-gwq9-9ffj-mvrv (CVE-2026-93451) (QSI-2026-49956)\
   What to do: Upgrade to a fixed version (1.1.10.9).
3. **High** · org.jsoup:jsoup 1.18.3 is affected by GHSA-65r4-943x-97jj (CVE-2026-75140) (QSI-2026-49960)\
   What to do: Upgrade to a fixed version (1.23.2).
4. **High** · com.rabbitmq:amqp-client 5.22.0 is affected by GHSA-68mj-5wr7-6fgg (CVE-2026-69219) (QSI-2026-49964)\
   What to do: Upgrade to a fixed version (5.33.1).

21 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · authentication and identity (certificates, tokens, device attestation) | RSA | Keep credentials short-lived and plan ML-DSA certificates, tokens and keys as the ecosystem supports them |
| **Medium** · role not determined | RSA | Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205)… |

## Known vulnerable components

Advisories for the versions in use: 19; each needs checking against the code.

Analyst review: 0 confirmed, 4 not applicable, 7 dismissed as false positives. (QSI review, 2026-11-24)

---

Static review of source code and manifests; files analysed: 1190. No requests were sent to the owner's systems.

Full report, content SHA-256: `e5a7852ac0bd2a437c9b86ce887fe8f140790ffa617ff73ab1a470aa832d1c60`

Full report signature (report.sig.json): Ed25519 key, then the ML-DSA-65 one where it co-signs, SHA-256 fingerprints `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e · ML-DSA-65 dbd4e297b3213d1d7577a565e76de14cc5ad0e409f1dc68291c67266fc95066a`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.