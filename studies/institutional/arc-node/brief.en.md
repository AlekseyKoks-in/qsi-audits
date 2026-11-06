# Post-quantum cryptography review: arc-node @ 6e764023ee65

*One-page brief* · Reviewed: 2026-11-06 15:31 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: Circle (Arc) — public repository (passive review)

Source: https://github.com/circlefin/arc-node/tree/6e764023ee6515fe70573e123ed2db912a7207b4

**Post-quantum maturity:** Level 2 of 4 — post-quantum in use outside the critical paths. **Next step:** Extend post-quantum protection to the critical roles that stay classical, starting with what can be recorded today (wrapped keys, channel key exchange).

**Findings:** Critical 0 · High 17 · Medium 20 · Low 31 · Info 61

**Quantum timeline (Mosca: x + y − z):** Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **High** · rmcp 1.4.0 is affected by GHSA-33f5-2c5q-wgwj (CVE-2026-63127) (QSI-2026-19526)\
   What to do: Upgrade to a fixed version (2.0.0).
2. **High** · rmcp 1.4.0 is affected by GHSA-9pj6-vhgr-3mwh (CVE-2026-63128) (QSI-2026-19528)\
   What to do: Upgrade to a fixed version (2.0.0).
3. **High** · Possible hard-coded secret in… (QSI-2026-19441) · *preliminary*\
   What to do: Move secrets to a secrets manager/environment; rotate the exposed values.
4. **High** · hickory-proto 0.25.2 is affected by GHSA-3v94-mw7p-v465 (RUSTSEC-2026-0118) (QSI-2026-19499)\
   What to do: Upgrade to a fixed version (0.26.0-beta.1).

64 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · transaction and message signing | ECDSA, Ed25519 | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum… |
| **Medium** · role not determined | Ed25519, ECDSA | Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205)… |

## Known vulnerable components

Advisories for the versions in use: 45; unlikely to apply to this build: 4 (a Cargo feature that is off, affected functions not named in the code, or a platform that is not built); to review: 41.

---

Static review of source code and manifests; files analysed: 1135. No requests were sent to the owner's systems.

Full report, content SHA-256: `2cb1f259975c8af684ffa81af50b3a9c029ff2d5a6375299ede323d6502412cd`

Full report signature (report.sig.json): Ed25519 key, SHA-256 fingerprint `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.