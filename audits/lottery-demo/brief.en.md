# Post-quantum cryptography review: lottery-demo

*One-page brief* · Reviewed: 2026-10-21 18:06 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: Демо-клиент

**Post-quantum maturity:** Level 0 of 4 — no post-quantum cryptography. **Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

**Findings:** Critical 0 · High 3 · Medium 1 · Low 0 · Info 1

## What matters most

1. **High** · tx.origin used for authorization in Lottery.sol (QSI-2026-00254)\
   What to do: Use msg.sender for authorization.
2. **High** · Slither: arbitrary-send-eth in Lottery.sol (QSI-2026-00255) · *preliminary*\
   What to do: Review the Slither detector documentation for 'arbitrary-send-eth' and fix or justify.
3. **High** · Slither: weak-prng in Lottery.sol (QSI-2026-00256) · *preliminary*\
   What to do: Review the Slither detector documentation for 'weak-prng' and fix or justify.
4. **Medium** · Slither: tx-origin in Lottery.sol (QSI-2026-00257) · *preliminary*\
   What to do: Review the Slither detector documentation for 'tx-origin' and fix or justify.

---

Static review of source code and manifests; files analysed: 1. No requests were sent to the owner's systems.

Full report, content SHA-256: `73de6bbc6c9edcedd4634eb26480047a3070d69b3c2421b669a4a8148817a2c0`

Full report signature (report.sig.json): Ed25519 key, SHA-256 fingerprint `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.