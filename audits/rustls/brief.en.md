# Post-quantum cryptography review: rustls @ 84bf9eaa9857

*One-page brief* · Reviewed: 2026-11-23 13:06 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: rustls project — public repository (passive review)

Source: https://github.com/rustls/rustls/tree/84bf9eaa9857d7114609f7e5d0ae1f0fd3cd9f77

**Post-quantum maturity:** Level 3 of 4 — hybrid protection in a critical path. **Next step:** Cover the remaining classical critical roles and plan when the classical half can be dropped.

**Findings:** Critical 0 · High 6 · Medium 9 · Low 12 · Info 5

**Quantum timeline (Mosca: x + y − z):** Key establishment 10 + 5 − 8 = 7 → too late; Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **High** · Private key material present in bogo/keys/ecdsa_p256_key.pem (QSI-2026-43275)\
   What to do: Treat the key as compromised: rotate it, revoke associated certificates, remove it from version history and store keys in a secrets…
2. **High** · Private key material present in bogo/keys/ecdsa_p384_key.pem (QSI-2026-43280)\
   What to do: Treat the key as compromised: rotate it, revoke associated certificates, remove it from version history and store keys in a secrets…
3. **High** · Private key material present in bogo/keys/key.pem (QSI-2026-43281)\
   What to do: Treat the key as compromised: rotate it, revoke associated certificates, remove it from version history and store keys in a secrets…
4. **High** · Private key material present in bogo/keys/rsa_1024_key.pem (QSI-2026-43287)\
   What to do: Treat the key as compromised: rotate it, revoke associated certificates, remove it from version history and store keys in a secrets…

23 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · key wrapping and data encryption at rest | RSA | Wrap keys with ML-KEM or a hybrid KEM (X25519 + ML-KEM-768) and re-wrap the stored keys; data that may… |
| **Medium** · channel key exchange (TLS, Noise, handshakes) | RSA, X25519 | Move the handshake to a hybrid key exchange (X25519MLKEM768 in TLS 1.3; a hybrid KEM in Noise-based protocols) |
| **Medium** · role not determined | ECDSA, Ed25519 | Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205)… |

## Known vulnerable components

Advisories for the versions in use: 2; unlikely to apply to this build: 1 (a Cargo feature that is off, affected functions not named in the code, or a platform that is not built); to review: 1.

---

Static review of source code and manifests; files analysed: 137. No requests were sent to the owner's systems.

Full report, content SHA-256: `536ef4981d43332fb99de432eed2019652d91ce70c60918a0dd8d542e0bf44d4`

Full report signature (report.sig.json): Ed25519 key, then the ML-DSA-65 one where it co-signs, SHA-256 fingerprints `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e · ML-DSA-65 dbd4e297b3213d1d7577a565e76de14cc5ad0e409f1dc68291c67266fc95066a`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.