# Post-quantum cryptography review: monero @ 3fd0f88c20f5

*One-page brief* · Reviewed: 2026-10-29 23:26 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: Monero — public repository (passive review)

Source: https://github.com/monero-project/monero/tree/3fd0f88c20f559839cafb20911cb13cb45eba7bd

**Post-quantum maturity:** Level 0 of 4 — no post-quantum cryptography. **Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

**Findings:** Critical 0 · High 1 · Medium 41 · Low 2 · Info 1

**Quantum timeline (Mosca: x + y − z):** Key establishment 10 + 5 − 8 = 7 → too late; Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **High** · Possible hard-coded secret in utils/python-rpc/framework/wallet.py (QSI-2026-07254) · *preliminary*\
   What to do: Move secrets to a secrets manager/environment; rotate the exposed values.
2. **Medium** · Transaction signing for 1 chain(s) relies on elliptic-curve signatures (QSI-2026-07256)\
   What to do: Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains…
3. **Medium** · Quantum-vulnerable Ed25519 key (Ed25519) in utils/gpg_keys/0xfffc0000.asc (QSI-2026-07220)\
   What to do: Inventory and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it..
4. **Medium** · Quantum-vulnerable RSA key (4096-bit) in utils/gpg_keys/SNeedlewoods.asc (QSI-2026-07221)\
   What to do: Inventory and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it..

40 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · channel key exchange (TLS, Noise, handshakes) | RSA | Move the handshake to a hybrid key exchange (X25519MLKEM768 in TLS 1.3; a hybrid KEM in Noise-based protocols) |
| **Medium** · transaction and message signing | Ed25519 | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum… |
| **Medium** · role not determined | Ed25519, ECDH, X25519 | Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205)… |

## Known vulnerable components

Advisories for the versions in use: 3; unlikely to apply to this build: 1 (a Cargo feature that is off, affected functions not named in the code, or a platform that is not built); to review: 2.

---

Static review of source code and manifests; files analysed: 1117. No requests were sent to the owner's systems.

Full report, content SHA-256: `baf67d98f79b2d660cf6851c2ab260cc1d832d4825056049a72d778f6eb5536e`

Full report signature (report.sig.json): Ed25519 key, SHA-256 fingerprint `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.