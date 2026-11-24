# Post-quantum cryptography review: zingolib @ 81d799775f11

*One-page brief* · Reviewed: 2026-11-24 11:42 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: Zingo Labs — public repository (passive review)

Source: https://github.com/zingolabs/zingolib/tree/81d799775f11e882896e8710e8af12d6d4d29a41

**Post-quantum maturity:** Level 3 of 4 — hybrid protection in a critical path. **Next step:** Cover the remaining classical critical roles and plan when the classical half can be dropped.

**Findings:** Critical 0 · High 3 · Medium 6 · Low 34 · Info 14 (of them advisories unlikely to apply: 18)

**Quantum timeline (Mosca: x + y − z):** Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **High** · pulldown-cmark 0.13.4 is affected by RUSTSEC-2026-0414 (QSI-2026-49818)\
   What to do: Upgrade to a fixed version (0.13.5).
2. **High** · rustls-webpki 0.101.7 is affected by GHSA-82j2-j2ch-gfr8 (CVE-2026-93599, RUSTSEC-2026-0104) (QSI-2026-49830)\
   What to do: Upgrade to a fixed version (0.103.13, 0.104.0-alpha.7).
3. **Medium** · Quantum-vulnerable Pedersen commitment: threshold signing and MPC protocols (2 file(s)) (QSI-2026-49800) · *preliminary*\
   What to do: Track post-quantum threshold signatures (NIST IR 8214C) and keep the protocol layer ready to swap the signature scheme; record which keys…
4. **Medium** · Quantum-vulnerable ECDSA: transaction and message signing (1 file(s)) (QSI-2026-49801) · *preliminary*\
   What to do: Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains…

39 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · threshold signing and MPC protocols | Pedersen commitment | Track post-quantum threshold signatures (NIST IR 8214C) and keep the protocol layer ready to swap the… |
| **Medium** · transaction and message signing | ECDSA | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum… |

## Known vulnerable components

Advisories for the versions in use: 43; unlikely to apply to this build: 18 (no call path to the affected code, a module only tests use, functions not named in the code, a Cargo feature that is off or a platform not built); to review: 25.

---

Static review of source code and manifests; files analysed: 204. No requests were sent to the owner's systems.

Full report, content SHA-256: `3d51efc8de34d864c8046d6d92c4e5b009a292f9e1a1bfa3ab3a698895f4645e`

Full report signature (report.sig.json): Ed25519 key, then the ML-DSA-65 one where it co-signs, SHA-256 fingerprints `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e · ML-DSA-65 dbd4e297b3213d1d7577a565e76de14cc5ad0e409f1dc68291c67266fc95066a`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.