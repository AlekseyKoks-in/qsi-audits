# Post-quantum cryptography review: bitwarden-sdk @ 25b6c8c3860a

*One-page brief* · Reviewed: 2026-11-24 10:21 UTC · Risk profile: Security software vendor · Client: Bitwarden — public repository (passive review)

Source: https://github.com/bitwarden/sdk-internal/tree/25b6c8c3860af5165ac1428c4c825ede7caa55de

**Post-quantum maturity:** Level 2 of 4 — post-quantum in use outside the critical paths. **Next step:** Extend post-quantum protection to the critical roles that stay classical, starting with what can be recorded today (wrapped keys, channel key exchange).

**Findings:** Critical 0 · High 0 · Medium 6 · Low 14 · Info 12 (of them advisories unlikely to apply: 3)

**Quantum timeline (Mosca: x + y − z):** Key establishment 10 + 3 − 8 = 5 → too late; Signatures 5 + 3 − 8 = 0 → tight

## What matters most

1. **Medium** · TLS without a post-quantum key exchange: rustls with the ring crypto provider (QSI-2026-47699) · *preliminary*\
   What to do: Build rustls with the aws-lc-rs provider (rustls::crypto::aws_lc_rs) and the prefer-post-quantum feature, which puts X25519MLKEM768 first.
2. **Medium** · Quantum-vulnerable RSA: key wrapping and data encryption at rest (4 file(s)) (QSI-2026-47700) · *preliminary*\
   What to do: Wrap keys with ML-KEM or a hybrid KEM (X25519 + ML-KEM-768) and re-wrap the stored keys; data that may already have been copied needs its…
3. **Medium** · Quantum-vulnerable ECDH: key wrapping and data encryption at rest (1 file(s)) (QSI-2026-47704) · *preliminary*\
   What to do: Wrap keys with ML-KEM or a hybrid KEM (X25519 + ML-KEM-768) and re-wrap the stored keys; data that may already have been copied needs its…
4. **Medium** · Quantum-vulnerable RSA: role not determined (1 file(s)) (QSI-2026-47701) · *preliminary*\
   What to do: Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form…

16 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · key wrapping and data encryption at rest | RSA, ECDH | Wrap keys with ML-KEM or a hybrid KEM (X25519 + ML-KEM-768) and re-wrap the stored keys; data that may… |
| **Medium** · channel key exchange (TLS, Noise, handshakes) | TLS ECDHE | Move the handshake to a hybrid key exchange (X25519MLKEM768 in TLS 1.3; a hybrid KEM in Noise-based protocols) |
| **Low** · authentication and identity (certificates, tokens, device attestation) | Ed25519, RSA | Keep credentials short-lived and plan ML-DSA certificates, tokens and keys as the ecosystem supports them |
| **Medium** · role not determined | Ed25519, RSA | Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205)… |

## Known vulnerable components

Advisories for the versions in use: 15; unlikely to apply to this build: 3 (no call path to the affected code, a module only tests use, functions not named in the code, a Cargo feature that is off or a platform not built); to review: 12.

---

Static review of source code and manifests; files analysed: 1625. No requests were sent to the owner's systems.

Full report, content SHA-256: `7630cd30bc753a33011a316a0ce2cd9c6816f67470146cebed43bf8616295be1`

Full report signature (report.sig.json): Ed25519 key, then the ML-DSA-65 one where it co-signs, SHA-256 fingerprints `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e · ML-DSA-65 dbd4e297b3213d1d7577a565e76de14cc5ad0e409f1dc68291c67266fc95066a`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.