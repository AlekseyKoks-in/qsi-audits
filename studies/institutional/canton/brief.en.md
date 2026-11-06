# Post-quantum cryptography review: canton @ 4eab7a047040

*One-page brief* · Reviewed: 2026-11-06 15:24 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: Digital Asset (Canton) — public repository (passive review)

Source: https://github.com/digital-asset/canton/tree/4eab7a047040bb61798b66abde794c8cb27f7746

**Post-quantum maturity:** Level 2 of 4 — post-quantum in use outside the critical paths. **Next step:** Extend post-quantum protection to the critical roles that stay classical, starting with what can be recorded today (wrapped keys, channel key exchange).

**Findings:** Critical 0 · High 4 · Medium 9 · Low 4 · Info 0

**Quantum timeline (Mosca: x + y − z):** Key establishment 10 + 5 − 8 = 7 → too late; Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **High** · Private key material present in performance/src/main/console/tls/participant.pem (QSI-2026-19406)\
   What to do: Treat the key as compromised: rotate it, revoke associated certificates, remove it from version history and store keys in a secrets…
2. **High** · Private key material present in performance/src/main/console/tls/synchronizer.pem (QSI-2026-19410)\
   What to do: Treat the key as compromised: rotate it, revoke associated certificates, remove it from version history and store keys in a secrets…
3. **High** · Certificate has expired (localhost) (QSI-2026-19403)\
   What to do: Renew the certificate and automate renewal (e.g. ACME) with expiry monitoring.
4. **High** · Certificate has expired (localhost) (QSI-2026-19407)\
   What to do: Renew the certificate and automate renewal (e.g. ACME) with expiry monitoring.

13 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · key wrapping and data encryption at rest | ECDH | Wrap keys with ML-KEM or a hybrid KEM (X25519 + ML-KEM-768) and re-wrap the stored keys; data that may… |
| **Medium** · transaction and message signing | ECDSA, Ed25519, RSA | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum… |
| **Medium** · authentication and identity (certificates, tokens, device attestation) | RSA, ECDSA, Ed25519 | Keep credentials short-lived and plan ML-DSA certificates, tokens and keys as the ecosystem supports them |
| **Medium** · role not determined | ECDSA, RSA | Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205)… |

---

Static review of source code and manifests; files analysed: 3314. No requests were sent to the owner's systems.

Full report, content SHA-256: `efbd8a018afeed64113c4427d45e8d0033b998dc55ff0d735a440be80e9c9cb1`

Full report signature (report.sig.json): Ed25519 key, SHA-256 fingerprint `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.