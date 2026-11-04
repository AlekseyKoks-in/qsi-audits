# Post-quantum cryptography review: zodl-android @ 229dd3bff749

*One-page brief* · Reviewed: 2026-11-04 19:47 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: Zodl (ex-Zashi, ECC) — public repository (passive review)

Source: https://github.com/zodl-inc/zodl-android/tree/229dd3bff7490ea90ca4d7d79f3c539d71976f66

**Post-quantum maturity:** Level 0 of 4 — no post-quantum cryptography. **Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

**Findings:** Critical 0 · High 0 · Medium 1 · Low 0 · Info 2

**Quantum timeline (Mosca: x + y − z):** Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **Medium** · Quantum-vulnerable RedDSA: transaction and message signing (3 file(s)) (QSI-2026-13081) · *preliminary*\
   What to do: Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains…

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · transaction and message signing | RedDSA | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum… |

---

Static review of source code and manifests; files analysed: 1609. No requests were sent to the owner's systems.

Full report, content SHA-256: `03b45dcd48862e675a425236dcd5fa3016b0ab65367cb7ad3a0de2690086f32b`

Full report signature (report.sig.json): Ed25519 key, SHA-256 fingerprint `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.