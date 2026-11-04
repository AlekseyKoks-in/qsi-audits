# Post-quantum cryptography review: metamask-extension @ d2db7ee9a19b

*One-page brief* · Reviewed: 2026-11-04 19:02 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: MetaMask (Consensys) — public repository (passive review)

Source: https://github.com/MetaMask/metamask-extension/tree/d2db7ee9a19b0322105618521370ab690911209f

**Post-quantum maturity:** Level 0 of 4 — no post-quantum cryptography. **Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

**Findings:** Critical 0 · High 0 · Medium 5 · Low 0 · Info 2

**Quantum timeline (Mosca: x + y − z):** Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **Medium** · Quantum-vulnerable ECDSA: transaction and message signing (1 file(s)) (QSI-2026-12190) · *preliminary*\
   What to do: Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains…
2. **Medium** · Quantum-vulnerable ECDSA: role not determined (10 file(s)) (QSI-2026-12189) · *preliminary*\
   What to do: Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form…
3. **Medium** · @hono/node-server 2.1.1 is affected by GHSA-rmxm-3fg6-px4f (CVE-2026-118663) (QSI-2026-12194)\
   What to do: Upgrade to a fixed version (2.1.3).
4. **Medium** · Non-cryptographic RNG near security-sensitive identifiers in app/scripts/sidepanel/background.ts (QSI-2026-12191) · *preliminary*\
   What to do: Use a CSPRNG (secrets, crypto.getRandomValues, crypto/rand).

1 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · transaction and message signing | ECDSA | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum… |
| **Medium** · role not determined | ECDSA | Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205)… |

## Known vulnerable components

Advisories for the versions in use: 1; each needs checking against the code.

---

Static review of source code and manifests; files analysed: 4870. No requests were sent to the owner's systems.

Full report, content SHA-256: `4574607d892a03af609dda8b51e06cab924466835209a93a9524129d671008ad`

Full report signature (report.sig.json): Ed25519 key, SHA-256 fingerprint `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.