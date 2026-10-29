# Post-quantum cryptography review: matrix-js-sdk @ 61b08bd037a3

*One-page brief* · Reviewed: 2026-10-28 18:22 UTC · Risk profile: Security software vendor · Client: Matrix.org Foundation — public repository (passive review)

Source: https://github.com/matrix-org/matrix-js-sdk/tree/61b08bd037a3b987f267e2e8ac47002c75d59d85

**Post-quantum maturity:** Level 0 of 4 — no post-quantum cryptography. **Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

**Findings:** Critical 0 · High 2 · Medium 1 · Low 1 · Info 1

**Quantum timeline (Mosca: x + y − z):** Key establishment 10 + 3 − 8 = 5 → too late

## What matters most

1. **High** · markdown-it 14.3.2 is affected by GHSA-gfr2-rv44-r23c (CVE-2026-111758) (QSI-2026-05835)\
   What to do: Upgrade to a fixed version (14.3.3, 15.0.3).
2. **High** · zod 4.6.5 is affected by GHSA-mrhx-c7xc-m3w5 (CVE-2023-54404) (QSI-2026-05837)\
   What to do: Upgrade to a fixed version (4.6.6).
3. **Medium** · Quantum-vulnerable ECDH: channel key exchange (TLS, Noise, handshakes) (1 file(s)) (QSI-2026-05834) · *preliminary*\
   What to do: Move the handshake to a hybrid key exchange (X25519MLKEM768 in TLS 1.3; a hybrid KEM in Noise-based protocols).
4. **Low** · markdown-it 14.3.2 is affected by GHSA-vfgh-jcmw-g37q (CVE-2026-111766) (QSI-2026-05836)\
   What to do: Upgrade to a fixed version (14.3.3, 15.0.3).

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · channel key exchange (TLS, Noise, handshakes) | ECDH | Move the handshake to a hybrid key exchange (X25519MLKEM768 in TLS 1.3; a hybrid KEM in Noise-based protocols) |

## Known vulnerable components

Advisories for the versions in use: 3; each needs checking against the code.

---

Static review of source code and manifests; files analysed: 240. No requests were sent to the owner's systems.

Full report, content SHA-256: `6b99f797316754f231b4b06db6d193f9d0893a7f657f49253d76cbd060ebaeb3`

Full report signature (report.sig.json): Ed25519 key, SHA-256 fingerprint `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.