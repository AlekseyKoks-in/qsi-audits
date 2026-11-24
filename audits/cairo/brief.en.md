# Post-quantum cryptography review: cairo @ 68a61f6c6251

*One-page brief* · Reviewed: 2026-11-24 10:24 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: StarkWare — public repository (passive review)

Source: https://github.com/starkware-libs/cairo/tree/68a61f6c6251900e0080e09c812ffaeb37fd358e

**Post-quantum maturity:** Level 0 of 4 — no post-quantum cryptography. **Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

**Findings:** Critical 2 · High 6 · Medium 8 · Low 23 · Info 4 (of them advisories unlikely to apply: 6)

**Quantum timeline (Mosca: x + y − z):** Key establishment 10 + 5 − 8 = 7 → too late; Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **Critical** · zip 0.6.6 is affected by GHSA-m665-v7pm-7grj (CVE-2026-115905, RUSTSEC-2026-0548) (QSI-2026-47769)\
   What to do: Upgrade to a fixed version (9.0.5).
2. **High** · pulldown-cmark 0.13.4 is affected by RUSTSEC-2026-0414 (QSI-2026-47751)\
   What to do: Upgrade to a fixed version (0.13.5).
3. **High** · quinn-proto 0.11.17 is affected by RUSTSEC-2026-0340 (QSI-2026-47754)\
   What to do: Upgrade to a fixed version (0.11.18).
4. **Medium** · Quantum-vulnerable Pedersen hash: threshold signing and MPC protocols (5 file(s)) (QSI-2026-47733) · *preliminary*\
   What to do: Track post-quantum threshold signatures (NIST IR 8214C) and keep the protocol layer ready to swap the signature scheme; record which keys…

35 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · threshold signing and MPC protocols | Pedersen hash | Track post-quantum threshold signatures (NIST IR 8214C) and keep the protocol layer ready to swap the… |
| **Medium** · transaction and message signing | ECDSA, Pedersen hash | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum… |
| **Medium** · role not determined | ECDSA, Pedersen hash | Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205)… |

## Known vulnerable components

Advisories for the versions in use: 35; unlikely to apply to this build: 6 (no call path to the affected code, a module only tests use, functions not named in the code, a Cargo feature that is off or a platform not built); to review: 29.

---

Static review of source code and manifests; files analysed: 673. No requests were sent to the owner's systems.

Full report, content SHA-256: `f32c78529fc8a47d1bbeed6b9bbf2f644aa2a3707f09e683d718ecca56e79994`

Full report signature (report.sig.json): Ed25519 key, then the ML-DSA-65 one where it co-signs, SHA-256 fingerprints `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e · ML-DSA-65 dbd4e297b3213d1d7577a565e76de14cc5ad0e409f1dc68291c67266fc95066a`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.