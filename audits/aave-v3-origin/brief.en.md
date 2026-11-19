# Post-quantum cryptography review: aave-v3-origin @ 8305565ae342

*One-page brief* · Reviewed: 2026-11-19 17:39 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: Aave DAO — public repository (passive review)

Source: https://github.com/aave-dao/aave-v3-origin/tree/8305565ae342f1773c42cd2e4593f175fe5968a0

**Post-quantum maturity:** Level 0 of 4 — no post-quantum cryptography. **Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

**Findings:** Critical 0 · High 9 · Medium 6 · Low 12 · Info 28

**Quantum timeline (Mosca: x + y − z):** Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **High** · delegatecall usage in src/contracts/dependencies/openzeppelin/contracts/Address.sol (QSI-2026-32489) · *preliminary*\
   What to do: Restrict delegatecall targets to trusted, immutable implementations.
2. **High** · delegatecall usage in… (QSI-2026-32491) · *preliminary*\
   What to do: Restrict delegatecall targets to trusted, immutable implementations.
3. **High** · initialize() without initializer modifier in… (QSI-2026-32492) · *preliminary*\
   What to do: Use OpenZeppelin Initializable (initializer modifier) and disable initializers in the implementation constructor.
4. **High** · delegatecall usage in… (QSI-2026-32493) · *preliminary*\
   What to do: Restrict delegatecall targets to trusted, immutable implementations.

23 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · transaction and message signing | ECDSA | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum… |

---

Static review of source code and manifests; files analysed: 569. No requests were sent to the owner's systems.

Full report, content SHA-256: `bb41ff4a30c95a7fb927bcfd2ccf40e3f60d0c46c9ac924d9eaf1390a2136636`

Full report signature (report.sig.json): Ed25519 key, then the ML-DSA-65 one where it co-signs, SHA-256 fingerprints `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e · ML-DSA-65 dbd4e297b3213d1d7577a565e76de14cc5ad0e409f1dc68291c67266fc95066a`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.