# Post-quantum cryptography review: zebra @ 147a6a8bf7d3

*One-page brief* · Reviewed: 2026-10-28 13:04 UTC · Risk profile: Small technology company · Client: Zcash Foundation — public repository (passive review)

Source: https://github.com/ZcashFoundation/zebra/tree/147a6a8bf7d3b1427a9c0557f284d5bfa7b0e522

**Post-quantum maturity:** Level 0 of 4 — no post-quantum cryptography. **Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

**Findings:** Critical 0 · High 2 · Medium 2 · Low 9 · Info 6

**Quantum timeline (Mosca: x + y − z):** Key establishment 5 + 3 − 12 = -4 → time available; Signatures 5 + 3 − 12 = -4 → time available

## What matters most

1. **High** · quinn-proto 0.11.16 is affected by RUSTSEC-2026-0340 (QSI-2026-05258)\
   What to do: Upgrade to a fixed version (0.11.18).
2. **High** · quinn-proto 0.11.16 is affected by RUSTSEC-2026-0341 (QSI-2026-05259)\
   What to do: Upgrade to a fixed version (0.11.17).
3. **Medium** · opentelemetry_sdk 0.31.0 is affected by GHSA-w9wp-h8wv-79jx (CVE-2026-48504) (QSI-2026-05254)\
   What to do: Upgrade to a fixed version (0.32.1).
4. **Medium** · block-buffer 0.10.4 is affected by GHSA-qwgh-2vcv-g2f7 (QSI-2026-05252)\
   What to do: Upgrade to a fixed version (none published yet; see the advisory for mitigations).

9 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Low** · transaction and message signing | Ed25519 | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum… |
| **Low** · role not determined | X25519, BLS12-381, ECDSA | Classify each usage, record data lifetimes, and plan migration to Hybrid key establishment with ML-KEM (FIPS… |

## Known vulnerable components

Advisories for the versions in use: 9; unlikely to apply to this build: 1 (a Cargo feature that is off, affected functions not named in the code, or a platform that is not built); to review: 8.

Analyst review: 0 confirmed, 0 not applicable, 1 dismissed as false positives. (QSI review, 2026-10-23)

---

Static review of source code and manifests; files analysed: 439. No requests were sent to the owner's systems.

Full report, content SHA-256: `ee7b94a59f12e7f13dc01adc6ec7e927c84e349194b3f02b357fd6092000614f`

Full report signature (report.sig.json): Ed25519 key, SHA-256 fingerprint `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.