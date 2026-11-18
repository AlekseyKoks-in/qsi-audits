# Post-quantum cryptography review: arc-node @ 6e764023ee65

*One-page brief* · Reviewed: 2026-11-17 21:51 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: Circle (Arc) — public repository (passive review)

Source: https://github.com/circlefin/arc-node/tree/6e764023ee6515fe70573e123ed2db912a7207b4

**Post-quantum maturity:** Level 2 of 4 — post-quantum in use outside the critical paths. **Next step:** Extend post-quantum protection to the critical roles that stay classical, starting with what can be recorded today (wrapped keys, channel key exchange).

**Findings:** Critical 0 · High 21 · Medium 23 · Low 64 · Info 64

**Quantum timeline (Mosca: x + y − z):** Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **High** · rmcp 1.4.0 is affected by GHSA-33f5-2c5q-wgwj (CVE-2026-63127) (QSI-2026-28840)\
   What to do: Upgrade to a fixed version (2.0.0).
2. **High** · rmcp 1.4.0 is affected by GHSA-9pj6-vhgr-3mwh (CVE-2026-63128) (QSI-2026-28842)\
   What to do: Upgrade to a fixed version (2.0.0).
3. **High** · Possible hard-coded secret in… (QSI-2026-28734) · *preliminary*\
   What to do: Move secrets to a secrets manager/environment; rotate the exposed values.
4. **High** · hickory-proto 0.25.2 is affected by GHSA-3v94-mw7p-v465 (CVE-2026-123607, RUSTSEC-2026-0118) (QSI-2026-28793)\
   What to do: Upgrade to a fixed version (0.26.0-beta.1).

104 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · transaction and message signing | ECDSA, Ed25519 | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum… |
| **Medium** · role not determined | Ed25519, ECDSA | Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205)… |

## Known vulnerable components

Advisories for the versions in use: 85; unlikely to apply to this build: 24 (a Cargo feature that is off, affected functions not named in the code, or a platform that is not built); to review: 61.

---

Static review of source code and manifests; files analysed: 1135. No requests were sent to the owner's systems.

Full report, content SHA-256: `3326e45c1fd7911e313c12296b6a9399477f80b3e8af924d6b0bdb913f888d2c`

Full report signature (report.sig.json): Ed25519 key, then the ML-DSA-65 one where it co-signs, SHA-256 fingerprints `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e · ML-DSA-65 dbd4e297b3213d1d7577a565e76de14cc5ad0e409f1dc68291c67266fc95066a`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.