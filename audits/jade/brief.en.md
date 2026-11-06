# Post-quantum cryptography review: jade @ a59d14c2b397

*One-page brief* · Reviewed: 2026-11-06 14:36 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: Blockstream (Jade) — public repository (passive review)

Source: https://github.com/Blockstream/Jade/tree/a59d14c2b39715060e6721a309a7d49bedd3ee5b

**Post-quantum maturity:** Level 0 of 4 — no post-quantum cryptography. **Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

**Findings:** Critical 0 · High 2 · Medium 18 · Low 0 · Info 2

**Quantum timeline (Mosca: x + y − z):** Key establishment 10 + 5 − 8 = 7 → too late; Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **High** · Private key material present in tools/fakeprod_attest.pem (QSI-2026-19276)\
   What to do: Treat the key as compromised: rotate it, revoke associated certificates, remove it from version history and store keys in a secrets…
2. **High** · Private key material present in tools/fakeprod_v2.pem (QSI-2026-19277)\
   What to do: Treat the key as compromised: rotate it, revoke associated certificates, remove it from version history and store keys in a secrets…
3. **Medium** · Quantum-vulnerable RSA key (4096-bit) in SECURITY.md (QSI-2026-19260)\
   What to do: Inventory and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it..
4. **Medium** · Quantum-vulnerable RSA key (3072-bit) in release/scripts/dev_fw_pub_key_A.pub (QSI-2026-19269)\
   What to do: Inventory and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it..

16 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · firmware and boot verification (root of trust) | ECDSA | Plan a hybrid firmware signature (the classical one plus ML-DSA or SLH-DSA, both required) and the path to… |
| **Medium** · key wrapping and data encryption at rest | ECDH | Wrap keys with ML-KEM or a hybrid KEM (X25519 + ML-KEM-768) and re-wrap the stored keys; data that may… |
| **Medium** · transaction and message signing | ECDSA, Schnorr (BIP-340) | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum… |
| **Medium** · authentication and identity (certificates, tokens, device attestation) | ECDSA, RSA | Keep credentials short-lived and plan ML-DSA certificates, tokens and keys as the ecosystem supports them |

---

Static review of source code and manifests; files analysed: 733. No requests were sent to the owner's systems.

Full report, content SHA-256: `447dc63401d0c7203a75e0ba46ce8b54a460db98875c7a3393d656c9fc082ca4`

Full report signature (report.sig.json): Ed25519 key, SHA-256 fingerprint `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.