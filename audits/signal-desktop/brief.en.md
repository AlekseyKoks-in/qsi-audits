# Post-quantum cryptography review: signal-desktop @ 17502b9d1a9e

*One-page brief* · Reviewed: 2026-11-24 11:25 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: Signal Messenger — public repository (passive review)

Source: https://github.com/signalapp/Signal-Desktop/tree/17502b9d1a9e34af689f31508c4ac4ccee5b5cb7

**Post-quantum maturity:** Level 2 of 4 — post-quantum in use outside the critical paths. **Next step:** Extend post-quantum protection to the critical roles that stay classical, starting with what can be recorded today (wrapped keys, channel key exchange).

**Findings:** Critical 1 · High 17 · Medium 18 · Low 3 · Info 2

**Quantum timeline (Mosca: x + y − z):** Key establishment 10 + 5 − 8 = 7 → too late

## What matters most

1. **Critical** · @storybook/core 8.6.18 is affected by GHSA-f2ph-cmg5-wxc8 (CVE-2026-114125) (QSI-2026-49527)\
   What to do: Upgrade to a fixed version (8.6.19).
2. **High** · zod 4.3.6 is affected by GHSA-mrhx-c7xc-m3w5 (CVE-2023-54404) (QSI-2026-49520)\
   What to do: Upgrade to a fixed version (4.6.6).
3. **High** · uuid 13.0.0 is affected by GHSA-w5hq-g745-h8pq (CVE-2026-41907, CVE-2026-41988) (QSI-2026-49555)\
   What to do: Upgrade to a fixed version (11.1.1, 12.0.1, 13.0.1).
4. **High** · zod 3.25.76 is affected by GHSA-mrhx-c7xc-m3w5 (CVE-2023-54404) (QSI-2026-49556)\
   What to do: Upgrade to a fixed version (4.6.6).

35 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · key wrapping and data encryption at rest | X25519 | Wrap keys with ML-KEM or a hybrid KEM (X25519 + ML-KEM-768) and re-wrap the stored keys; data that may… |
| **Medium** · role not determined | X25519 | Classify each usage, record data lifetimes, and plan migration to Hybrid key establishment with ML-KEM (FIPS… |

## Known vulnerable components

Advisories for the versions in use: 37; each needs checking against the code.

Analyst review: 0 confirmed, 1 not applicable, 0 dismissed as false positives. (QSI review, 2026-11-24)

---

Static review of source code and manifests; files analysed: 2198. No requests were sent to the owner's systems.

Full report, content SHA-256: `435c1ba319928a3ce0b0c42b8cd1309a9cec47966f4a876a8e0d40d465da3f63`

Full report signature (report.sig.json): Ed25519 key, then the ML-DSA-65 one where it co-signs, SHA-256 fingerprints `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e · ML-DSA-65 dbd4e297b3213d1d7577a565e76de14cc5ad0e409f1dc68291c67266fc95066a`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.