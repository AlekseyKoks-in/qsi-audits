# Post-quantum cryptography review: hyperledger-fabric @ 13ef9e5ee594

*One-page brief* · Reviewed: 2026-11-06 10:32 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: Hyperledger Fabric (LF Decentralized Trust) — public repository (passive review)

Source: https://github.com/hyperledger/fabric/tree/13ef9e5ee59466b152c8fe65b3a095234de671f7

**Post-quantum maturity:** Level 4 of 4 — post-quantum by default in the critical paths. **Next step:** Keep the inventory current and review new code paths before release.

**Findings:** Critical 0 · High 1 · Medium 7 · Low 3 · Info 18

**Quantum timeline (Mosca: x + y − z):** Key establishment 10 + 5 − 8 = 7 → too late; Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **High** · google.golang.org/grpc v1.83.1 is affected by GHSA-2v4p-qf9q-27wj (CVE-2026-84445, GO-2026-6443) (QSI-2026-17550)\
   What to do: Upgrade to a fixed version (1.82.2, 1.83.2, 1.84.0-dev.0.20260825144003-d5a41119e0e3, 1.85.0-dev.0.20260825072537-93e31b48545e).
2. **Medium** · Quantum-vulnerable ECDSA: transaction and message signing (1 file(s)) (QSI-2026-17522) · *preliminary*\
   What to do: Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains…
3. **Medium** · Quantum-vulnerable Ed25519: transaction and message signing (1 file(s)) (QSI-2026-17523) · *preliminary*\
   What to do: Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains…
4. **Medium** · Quantum-vulnerable ECDSA: role not determined (8 file(s)) (QSI-2026-17524) · *preliminary*\
   What to do: Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form…

7 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · transaction and message signing | ECDSA, Ed25519 | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum… |
| **Medium** · authentication and identity (certificates, tokens, device attestation) | ECDSA | Keep credentials short-lived and plan ML-DSA certificates, tokens and keys as the ecosystem supports them |
| **Medium** · role not determined | ECDSA, ECDH, Ed25519 | Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205)… |

## Known vulnerable components

Advisories for the versions in use: 20; unlikely to apply to this build: 18 (a Cargo feature that is off, affected functions not named in the code, or a platform that is not built); to review: 2.

---

Static review of source code and manifests; files analysed: 814. No requests were sent to the owner's systems.

Full report, content SHA-256: `c6d8ad0dc0ae1f4057b7a287b056a05648ac2555beac30700886e6ad50e9e186`

Full report signature (report.sig.json): Ed25519 key, SHA-256 fingerprint `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.