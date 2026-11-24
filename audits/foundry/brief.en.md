# Post-quantum cryptography review: foundry @ 7f0a409a5c20

*One-page brief* · Reviewed: 2026-11-24 12:34 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: Foundry (Paradigm) — public repository (passive review)

Source: https://github.com/foundry-rs/foundry/tree/7f0a409a5c2016f16cb2e8618a750cc04e13977c

**Post-quantum maturity:** Level 4 of 4 — post-quantum by default in the critical paths. **Next step:** Keep the inventory current and review new code paths before release.

**Findings:** Critical 1 · High 2 · Medium 7 · Low 34 · Info 8 (of them advisories unlikely to apply: 26)

**Quantum timeline (Mosca: x + y − z):** Key establishment 10 + 5 − 8 = 7 → too late; Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **Critical** · zip 9.0.4 is affected by GHSA-m665-v7pm-7grj (CVE-2026-115905, RUSTSEC-2026-0548) (QSI-2026-50355)\
   What to do: Upgrade to a fixed version (9.0.5).
2. **High** · quick-xml 0.39.4 is affected by RUSTSEC-2026-0194 (QSI-2026-50350)\
   What to do: Upgrade to a fixed version (0.41.0).
3. **Medium** · TLS without a post-quantum key exchange: rustls with the ring crypto provider (QSI-2026-50336) · *preliminary*\
   What to do: Build rustls with the aws-lc-rs provider (rustls::crypto::aws_lc_rs) and the prefer-post-quantum feature, which puts X25519MLKEM768 first.
4. **Medium** · Quantum-vulnerable ECDSA: transaction and message signing (11 file(s)) (QSI-2026-50334) · *preliminary*\
   What to do: Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains…

40 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · channel key exchange (TLS, Noise, handshakes) | TLS ECDHE | Move the handshake to a hybrid key exchange (X25519MLKEM768 in TLS 1.3; a hybrid KEM in Noise-based protocols) |
| **Medium** · transaction and message signing | ECDSA, BLS12-381, Ed25519 | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum… |
| **Medium** · authentication and identity (certificates, tokens, device attestation) | ECDSA | Keep credentials short-lived and plan ML-DSA certificates, tokens and keys as the ecosystem supports them |
| **Medium** · role not determined | BLS12-381 | Classify each usage, record data lifetimes, and plan migration to a post-quantum algorithm; introduce an… |

## Known vulnerable components

Advisories for the versions in use: 38; unlikely to apply to this build: 26 (no call path to the affected code, a module only tests use, functions not named in the code, a Cargo feature that is off or a platform not built); to review: 12.

Analyst review: 0 confirmed, 1 not applicable, 0 dismissed as false positives. (QSI review, 2026-11-24)

---

Static review of source code and manifests; files analysed: 757. No requests were sent to the owner's systems.

Full report, content SHA-256: `388938333456bbc986f2bdcf457bedeaebb5c39bc975833e222eac35f494966a`

Full report signature (report.sig.json): Ed25519 key, then the ML-DSA-65 one where it co-signs, SHA-256 fingerprints `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e · ML-DSA-65 dbd4e297b3213d1d7577a565e76de14cc5ad0e409f1dc68291c67266fc95066a`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.