# Post-quantum cryptography review: jade @ a59d14c2b397

*One-page brief* · Reviewed: 2026-10-29 19:59 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: Blockstream (Jade) — public repository (passive review)

Source: https://github.com/Blockstream/Jade/tree/a59d14c2b39715060e6721a309a7d49bedd3ee5b

**Post-quantum maturity:** Level 0 of 4 — no post-quantum cryptography. **Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

**Findings:** Critical 0 · High 5 · Medium 16 · Low 0 · Info 2

**Quantum timeline (Mosca: x + y − z):** Key establishment 10 + 5 − 8 = 7 → too late; Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **High** · Private key material present in release/scripts/dev_fw_signing_key_A.pem (QSI-2026-06703)\
   What to do: Treat the key as compromised: rotate it, revoke associated certificates, remove it from version history and store keys in a secrets…
2. **High** · Private key material present in release/scripts/dev_fw_signing_key_B.pem (QSI-2026-06704)\
   What to do: Treat the key as compromised: rotate it, revoke associated certificates, remove it from version history and store keys in a secrets…
3. **High** · Private key material present in release/scripts/dev_fw_signing_key_C.pem (QSI-2026-06705)\
   What to do: Treat the key as compromised: rotate it, revoke associated certificates, remove it from version history and store keys in a secrets…
4. **High** · Private key material present in tools/fakeprod_attest.pem (QSI-2026-06710)\
   What to do: Treat the key as compromised: rotate it, revoke associated certificates, remove it from version history and store keys in a secrets…

17 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · firmware and boot verification (root of trust) | ECDSA | Plan a hybrid firmware signature (the classical one plus ML-DSA or SLH-DSA, both required) and the path to… |
| **Medium** · transaction and message signing | ECDSA, Schnorr (BIP-340) | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum… |
| **Medium** · authentication and identity (certificates, tokens, device attestation) | ECDSA, RSA | Keep credentials short-lived and plan ML-DSA certificates, tokens and keys as the ecosystem supports them |
| **Medium** · role not determined | ECDSA, Schnorr (BIP-340) | Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205)… |

---

Static review of source code and manifests; files analysed: 737. No requests were sent to the owner's systems.

Full report, content SHA-256: `f4b140a68a457febeea7aae793751c45b1001460fce55b495d23af538ad63b92`

Full report signature (report.sig.json): Ed25519 key, SHA-256 fingerprint `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.