# Post-quantum cryptography review: foundry @ 7f0a409a5c20

*One-page brief* · Reviewed: 2026-10-28 12:26 UTC · Risk profile: Security software vendor · Client: Foundry (Paradigm) — public repository (passive review)

Source: https://github.com/foundry-rs/foundry/tree/7f0a409a5c2016f16cb2e8618a750cc04e13977c

**Post-quantum maturity:** Level 4 of 4 — post-quantum by default in the critical paths. **Next step:** Keep the inventory current and review new code paths before release.

**Findings:** Critical 0 · High 2 · Medium 3 · Low 10 · Info 3

**Quantum timeline (Mosca: x + y − z):** Key establishment 10 + 3 − 8 = 5 → too late; Signatures 5 + 3 − 8 = 0 → tight

## What matters most

1. **High** · quick-xml 0.39.4 is affected by RUSTSEC-2026-0194 (QSI-2026-04469)\
   What to do: Upgrade to a fixed version (0.41.0).
2. **High** · quick-xml 0.39.4 is affected by RUSTSEC-2026-0195 (QSI-2026-04470)\
   What to do: Upgrade to a fixed version (0.41.0).
3. **Medium** · TLS without a post-quantum key exchange: rustls with the ring crypto provider (QSI-2026-04456) · *preliminary*\
   What to do: Build rustls with the aws-lc-rs provider (rustls::crypto::aws_lc_rs) and the prefer-post-quantum feature, which puts X25519MLKEM768 first.
4. **Medium** · block-buffer 0.9.0 is affected by GHSA-qwgh-2vcv-g2f7 (QSI-2026-04462)\
   What to do: Upgrade to a fixed version (none published yet; see the advisory for mitigations).

11 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · channel key exchange (TLS, Noise, handshakes) | TLS ECDHE | Move the handshake to a hybrid key exchange (X25519MLKEM768 in TLS 1.3; a hybrid KEM in Noise-based protocols) |
| **Low** · transaction and message signing | ECDSA, BLS12-381 | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum… |
| **Low** · authentication and identity (certificates, tokens, device attestation) | ECDSA | Keep credentials short-lived and plan ML-DSA certificates, tokens and keys as the ecosystem supports them |
| **Low** · role not determined | BLS12-381, ECDSA | Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205)… |

## Known vulnerable components

Advisories for the versions in use: 7; each needs checking against the code.

---

Static review of source code and manifests; files analysed: 761. No requests were sent to the owner's systems.

Full report, content SHA-256: `37dc71482c0ac19cdfddf6850b40a433a909c798e26a1f8725c5dfb354258319`

Full report signature (report.sig.json): Ed25519 key, SHA-256 fingerprint `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.