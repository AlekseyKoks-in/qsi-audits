# Post-quantum cryptography review: rustls @ 84bf9eaa9857

*One-page brief* · Reviewed: 2026-10-29 23:20 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: rustls project — public repository (passive review)

Source: https://github.com/rustls/rustls/tree/84bf9eaa9857d7114609f7e5d0ae1f0fd3cd9f77

**Post-quantum maturity:** Level 4 of 4 — post-quantum by default in the critical paths. **Next step:** Keep the inventory current and review new code paths before release.

**Findings:** Critical 0 · High 6 · Medium 8 · Low 11 · Info 6

**Quantum timeline (Mosca: x + y − z):** Key establishment 10 + 5 − 8 = 7 → too late; Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **High** · Private key material present in bogo/keys/ecdsa_p256_key.pem (QSI-2026-07183)\
   What to do: Treat the key as compromised: rotate it, revoke associated certificates, remove it from version history and store keys in a secrets…
2. **High** · Private key material present in bogo/keys/ecdsa_p384_key.pem (QSI-2026-07188)\
   What to do: Treat the key as compromised: rotate it, revoke associated certificates, remove it from version history and store keys in a secrets…
3. **High** · Private key material present in bogo/keys/key.pem (QSI-2026-07189)\
   What to do: Treat the key as compromised: rotate it, revoke associated certificates, remove it from version history and store keys in a secrets…
4. **High** · Private key material present in bogo/keys/rsa_1024_key.pem (QSI-2026-07195)\
   What to do: Treat the key as compromised: rotate it, revoke associated certificates, remove it from version history and store keys in a secrets…

21 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · channel key exchange (TLS, Noise, handshakes) | RSA, X25519 | Move the handshake to a hybrid key exchange (X25519MLKEM768 in TLS 1.3; a hybrid KEM in Noise-based protocols) |
| **Medium** · role not determined | ECDSA, Ed25519 | Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205)… |

## Known vulnerable components

Advisories for the versions in use: 1; each needs checking against the code.

---

Static review of source code and manifests; files analysed: 137. No requests were sent to the owner's systems.

Full report, content SHA-256: `210849db2029e7259b751c529067f4e6383788b3f466265134aa340884f0bfb1`

Full report signature (report.sig.json): Ed25519 key, SHA-256 fingerprint `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.