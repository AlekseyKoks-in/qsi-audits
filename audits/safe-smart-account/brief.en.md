# Post-quantum cryptography review: safe-smart-account @ 247b8ce3bdbf

*One-page brief* · Reviewed: 2026-11-23 13:07 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: Safe — public repository (passive review)

Source: https://github.com/safe-global/safe-smart-account/tree/247b8ce3bdbf204a120e77f5b369d137424ddc58

**Post-quantum maturity:** Level 0 of 4 — no post-quantum cryptography. **Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

**Findings:** Critical 0 · High 0 · Medium 1 · Low 3 · Info 2

**Quantum timeline (Mosca: x + y − z):** Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **Medium** · Quantum-vulnerable ECDSA: transaction and message signing (2 file(s)) (QSI-2026-43301) · *preliminary*\
   What to do: Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains…
2. **Low** · Floating pragma (>=0.7.0 <0.9.0) in 50 file(s) (QSI-2026-43300)\
   What to do: Pin the compiler version used in testing.
3. **Low** · Floating pragma (>=0.5.0 <0.9.0) in 1 file(s) (QSI-2026-43302)\
   What to do: Pin the compiler version used in testing.
4. **Low** · Floating pragma (>=0.7.4 <0.9.0) in 1 file(s) (QSI-2026-43303)\
   What to do: Pin the compiler version used in testing.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · transaction and message signing | ECDSA | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum… |

---

Static review of source code and manifests; files analysed: 74. No requests were sent to the owner's systems.

Full report, content SHA-256: `3bddc30255c4b700b5d0c66e064c05a011eea8c2e28607ab9a692aea5be00b1c`

Full report signature (report.sig.json): Ed25519 key, then the ML-DSA-65 one where it co-signs, SHA-256 fingerprints `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e · ML-DSA-65 dbd4e297b3213d1d7577a565e76de14cc5ad0e409f1dc68291c67266fc95066a`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.