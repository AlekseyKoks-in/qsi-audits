# Post-quantum cryptography review: safe-smart-account @ 247b8ce3bdbf

*One-page brief* · Reviewed: 2026-10-28 12:53 UTC · Risk profile: Financial institution · Client: Safe — public repository (passive review)

Source: https://github.com/safe-global/safe-smart-account/tree/247b8ce3bdbf204a120e77f5b369d137424ddc58

**Post-quantum maturity:** Level 0 of 4 — no post-quantum cryptography. **Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

**Findings:** Critical 0 · High 0 · Medium 3 · Low 3 · Info 2

**Quantum timeline (Mosca: x + y − z):** Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **Medium** · Raw ecrecover usage in certora/harnesses/SafeHarness.sol (QSI-2026-05092) · *preliminary*\
   What to do: Use OpenZeppelin ECDSA.recover with EIP-712 domain separation and nonces.
2. **Medium** · Unchecked low-level call in certora/harnesses/SafeHarness.sol (QSI-2026-05093) · *preliminary*\
   What to do: Check the boolean return value or use OpenZeppelin Address.sendValue / functionCall.
3. **Medium** · Quantum-vulnerable ECDSA: transaction and message signing (3 file(s)) (QSI-2026-05091) · *preliminary*\
   What to do: Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains…
4. **Low** · Floating pragma (>=0.7.0 <0.9.0) in 50 file(s) (QSI-2026-05094)\
   What to do: Pin the compiler version used in testing.

2 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · transaction and message signing | ECDSA | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum… |

---

Static review of source code and manifests; files analysed: 77. No requests were sent to the owner's systems.

Full report, content SHA-256: `0da61727ced613d6767f96b37828d8b962f93bc2e81d7a8c2e0fab5270116a40`

Full report signature (report.sig.json): Ed25519 key, SHA-256 fingerprint `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.