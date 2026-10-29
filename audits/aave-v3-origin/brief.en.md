# Post-quantum cryptography review: aave-v3-origin @ 8305565ae342

*One-page brief* · Reviewed: 2026-10-29 06:16 UTC · Risk profile: Financial institution · Client: Aave DAO — public repository (passive review)

Source: https://github.com/aave-dao/aave-v3-origin/tree/8305565ae342f1773c42cd2e4593f175fe5968a0

**Post-quantum maturity:** Level 0 of 4 — no post-quantum cryptography. **Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

**Findings:** Critical 0 · High 9 · Medium 3 · Low 14 · Info 32

**Quantum timeline (Mosca: x + y − z):** Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **High** · delegatecall usage in… (QSI-2026-06514) · *preliminary*\
   What to do: Restrict delegatecall targets to trusted, immutable implementations.
2. **High** · delegatecall usage in src/contracts/dependencies/openzeppelin/contracts/Address.sol (QSI-2026-06520) · *preliminary*\
   What to do: Restrict delegatecall targets to trusted, immutable implementations.
3. **High** · delegatecall usage in… (QSI-2026-06522) · *preliminary*\
   What to do: Restrict delegatecall targets to trusted, immutable implementations.
4. **High** · initialize() without initializer modifier in… (QSI-2026-06523) · *preliminary*\
   What to do: Use OpenZeppelin Initializable (initializer modifier) and disable initializers in the implementation constructor.

22 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · transaction and message signing | ECDSA | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum… |

---

Static review of source code and manifests; files analysed: 645. No requests were sent to the owner's systems.

Full report, content SHA-256: `e7d4254918ac124d044234875cf5eaf0ca41e8942ad34749fce947e2c8940dca`

Full report signature (report.sig.json): Ed25519 key, SHA-256 fingerprint `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.