# Post-quantum cryptography review: matrix-js-sdk @ 61b08bd037a3

*One-page brief* · Reviewed: 2026-11-24 10:44 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: Matrix.org Foundation — public repository (passive review)

Source: https://github.com/matrix-org/matrix-js-sdk/tree/61b08bd037a3b987f267e2e8ac47002c75d59d85

**Post-quantum maturity:** Level 0 of 4 — no post-quantum cryptography. **Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

**Findings:** Critical 0 · High 2 · Medium 3 · Low 1 · Info 1

**Quantum timeline (Mosca: x + y − z):** Key establishment 10 + 5 − 8 = 7 → too late

## What matters most

1. **High** · markdown-it 14.3.2 is affected by GHSA-gfr2-rv44-r23c (CVE-2026-111758) (QSI-2026-48184)\
   What to do: Upgrade to a fixed version (14.3.3, 15.0.3).
2. **High** · zod 4.6.5 is affected by GHSA-mrhx-c7xc-m3w5 (CVE-2023-54404) (QSI-2026-48187)\
   What to do: Upgrade to a fixed version (4.6.6).
3. **Medium** · Quantum-vulnerable ECDH: channel key exchange (TLS, Noise, handshakes) (1 file(s)) (QSI-2026-48182) · *preliminary*\
   What to do: Move the handshake to a hybrid key exchange (X25519MLKEM768 in TLS 1.3; a hybrid KEM in Noise-based protocols).
4. **Medium** · glob 13.0.6 is affected by GHSA-3g3m-2fjr-6pw4 (CVE-2026-118773) (QSI-2026-48183)\
   What to do: Upgrade to a fixed version (14.0.2).

2 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · channel key exchange (TLS, Noise, handshakes) | ECDH | Move the handshake to a hybrid key exchange (X25519MLKEM768 in TLS 1.3; a hybrid KEM in Noise-based protocols) |

## Known vulnerable components

Advisories for the versions in use: 5; each needs checking against the code.

---

Static review of source code and manifests; files analysed: 240. No requests were sent to the owner's systems.

Full report, content SHA-256: `3dd170854bf1954aa80ce093e4b55d2c9d6de64a400e2a729027a4f928c729d1`

Full report signature (report.sig.json): Ed25519 key, then the ML-DSA-65 one where it co-signs, SHA-256 fingerprints `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e · ML-DSA-65 dbd4e297b3213d1d7577a565e76de14cc5ad0e409f1dc68291c67266fc95066a`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.