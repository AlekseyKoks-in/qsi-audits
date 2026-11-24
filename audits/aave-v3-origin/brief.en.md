# Post-quantum cryptography review: aave-v3-origin @ 8305565ae342

*One-page brief* · Reviewed: 2026-11-24 09:50 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: Aave DAO — public repository (passive review)

Source: https://github.com/aave-dao/aave-v3-origin/tree/8305565ae342f1773c42cd2e4593f175fe5968a0

**Post-quantum maturity:** Level 0 of 4 — no post-quantum cryptography. **Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

**Findings:** Critical 0 · High 0 · Medium 5 · Low 10 · Info 31

**Quantum timeline (Mosca: x + y − z):** Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **Medium** · Chainlink price used without a freshness check (latestAnswer()) in… (QSI-2026-47362) · *preliminary*\
   What to do: Read updatedAt from latestRoundData and reject answers older than the feed's heartbeat; reject non-positive answers; on rollups consult…
2. **Medium** · Chainlink price used without a freshness check (latestAnswer()) in… (QSI-2026-47363) · *preliminary*\
   What to do: Read updatedAt from latestRoundData and reject answers older than the feed's heartbeat; reject non-positive answers; on rollups consult…
3. **Medium** · Chainlink price used without a freshness check (latestAnswer()) in src/contracts/misc/AaveOracle.sol (QSI-2026-47365) · *preliminary*\
   What to do: Read updatedAt from latestRoundData and reject answers older than the feed's heartbeat; reject non-positive answers; on rollups consult…
4. **Medium** · Quantum-vulnerable ECDSA: transaction and message signing (11 file(s)) (QSI-2026-47368) · *preliminary*\
   What to do: Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains…

11 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · transaction and message signing | ECDSA | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum… |

---

Static review of source code and manifests; files analysed: 569. No requests were sent to the owner's systems.

Full report, content SHA-256: `162d6d677d1293856676a9f6a8786be872e3aadfaf1869ffd2b52df9aa912bac`

Full report signature (report.sig.json): Ed25519 key, then the ML-DSA-65 one where it co-signs, SHA-256 fingerprints `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e · ML-DSA-65 dbd4e297b3213d1d7577a565e76de14cc5ad0e409f1dc68291c67266fc95066a`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.