# Post-quantum cryptography review: fabric-lib-go @ f8b4f4a833e4

*One-page brief* · Reviewed: 2026-11-06 10:15 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: Hyperledger Fabric (LF Decentralized Trust) — public repository (passive review)

Source: https://github.com/hyperledger/fabric-lib-go/tree/f8b4f4a833e4140a4d006fc2e0a46823952b5f1c

**Post-quantum maturity:** Level 0 of 4 — no post-quantum cryptography. **Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

**Findings:** Critical 0 · High 1 · Medium 3 · Low 0 · Info 7

**Quantum timeline (Mosca: x + y − z):** Key establishment 10 + 5 − 8 = 7 → too late; Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **High** · google.golang.org/grpc v1.83.1 is affected by GHSA-2v4p-qf9q-27wj (CVE-2026-84445, GO-2026-6443) (QSI-2026-17514)\
   What to do: Upgrade to a fixed version (1.82.2, 1.83.2, 1.84.0-dev.0.20260825144003-d5a41119e0e3, 1.85.0-dev.0.20260825072537-93e31b48545e).
2. **Medium** · Quantum-vulnerable ECDSA: role not determined (10 file(s)) (QSI-2026-17511) · *preliminary*\
   What to do: Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form…
3. **Medium** · Quantum-vulnerable Ed25519: role not determined (6 file(s)) (QSI-2026-17512) · *preliminary*\
   What to do: Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form…
4. **Medium** · Quantum-vulnerable RSA: role not determined (6 file(s)) (QSI-2026-17513) · *preliminary*\
   What to do: Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form…

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · role not determined | ECDSA, Ed25519, RSA | Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205)… |

## Known vulnerable components

Advisories for the versions in use: 8; unlikely to apply to this build: 7 (a Cargo feature that is off, affected functions not named in the code, or a platform that is not built); to review: 1.

---

Static review of source code and manifests; files analysed: 67. No requests were sent to the owner's systems.

Full report, content SHA-256: `967ff3502b91c3f489ae4dc96bfd80d7f227c73a45038ab60ffb4c654876bd06`

Full report signature (report.sig.json): Ed25519 key, SHA-256 fingerprint `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.