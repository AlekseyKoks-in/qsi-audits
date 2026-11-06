# Post-quantum cryptography review: seedsigner @ ada81cde050e

*One-page brief* · Reviewed: 2026-11-06 13:57 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: SeedSigner — public repository (passive review)

Source: https://github.com/SeedSigner/seedsigner/tree/ada81cde050e46c19cb6e3fa73872b73955a138c

**Post-quantum maturity:** Level 0 of 4 — no post-quantum cryptography. **Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

**Findings:** Critical 0 · High 2 · Medium 2 · Low 0 · Info 0

**Quantum timeline (Mosca: x + y − z):** Key establishment 10 + 5 − 8 = 7 → too late; Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **High** · Non-cryptographic generator next to key or seed generation in src/seedsigner/views/seed_views.py (QSI-2026-18989) · *preliminary*\
   What to do: Use the platform CSPRNG (secrets, os.urandom, crypto.getRandomValues, crypto/rand, SecureRandom, OsRng) or a hardware TRNG for every key…
2. **High** · Non-cryptographic generator next to key or seed generation in tools/mnemonic.py (QSI-2026-18990) · *preliminary*\
   What to do: Use the platform CSPRNG (secrets, os.urandom, crypto.getRandomValues, crypto/rand, SecureRandom, OsRng) or a hardware TRNG for every key…
3. **Medium** · Quantum-vulnerable RSA key (3072-bit) in seedsigner_pubkey.gpg (QSI-2026-18987)\
   What to do: Inventory and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it..
4. **Medium** · Quantum-vulnerable ECDSA: transaction and message signing (1 file(s)) (QSI-2026-18988) · *confirmed by the analyst*\
   What to do: Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains…

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · transaction and message signing | ECDSA | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum… |

Analyst review: 1 confirmed, 0 not applicable, 0 dismissed as false positives. (QSI review, 2026-10-29)

---

Static review of source code and manifests; files analysed: 76. No requests were sent to the owner's systems.

Full report, content SHA-256: `01996796bcafb8fce4023132d4bba49a64437dd673f115989e79cf74109bfa43`

Full report signature (report.sig.json): Ed25519 key, SHA-256 fingerprint `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.