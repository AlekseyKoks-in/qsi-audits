# Post-quantum cryptography review: jade @ a59d14c2b397

*One-page brief* · Reviewed: 2026-11-24 10:32 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: Blockstream (Jade) — public repository (passive review)

Source: https://github.com/Blockstream/Jade/tree/a59d14c2b39715060e6721a309a7d49bedd3ee5b

**Post-quantum maturity:** Level 0 of 4 — no post-quantum cryptography. **Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

**Findings:** Critical 0 · High 0 · Medium 16 · Low 0 · Info 7

**Quantum timeline (Mosca: x + y − z):** Key establishment 10 + 5 − 8 = 7 → too late; Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **Medium** · Quantum-vulnerable RSA key (4096-bit) in SECURITY.md (QSI-2026-47908)\
   What to do: Inventory and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it..
2. **Medium** · Quantum-vulnerable RSA key (3072-bit) in release/scripts/dev_fw_pub_key_A.pub (QSI-2026-47917)\
   What to do: Inventory and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it..
3. **Medium** · Quantum-vulnerable RSA key (3072-bit) in release/scripts/dev_fw_pub_key_B.pub (QSI-2026-47918)\
   What to do: Inventory and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it..
4. **Medium** · Quantum-vulnerable RSA key (3072-bit) in release/scripts/dev_fw_pub_key_C.pub (QSI-2026-47919)\
   What to do: Inventory and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it..

12 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · firmware and boot verification (root of trust) | ECDSA | Plan a hybrid firmware signature (the classical one plus ML-DSA or SLH-DSA, both required) and the path to… |
| **Medium** · key wrapping and data encryption at rest | ECDH | Wrap keys with ML-KEM or a hybrid KEM (X25519 + ML-KEM-768) and re-wrap the stored keys; data that may… |
| **Medium** · transaction and message signing | ECDSA, Schnorr (BIP-340) | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum… |
| **Medium** · authentication and identity (certificates, tokens, device attestation) | ECDSA, RSA | Keep credentials short-lived and plan ML-DSA certificates, tokens and keys as the ecosystem supports them |

Analyst review: 0 confirmed, 2 not applicable, 0 dismissed as false positives. (QSI review, 2026-11-24)

---

Static review of source code and manifests; files analysed: 733. No requests were sent to the owner's systems.

Full report, content SHA-256: `4c5e367731b15a2c72e3213604ac020a32b9015371aa1ae02eb1bed679f97cd3`

Full report signature (report.sig.json): Ed25519 key, then the ML-DSA-65 one where it co-signs, SHA-256 fingerprints `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e · ML-DSA-65 dbd4e297b3213d1d7577a565e76de14cc5ad0e409f1dc68291c67266fc95066a`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.