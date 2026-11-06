# Post-quantum cryptography review: zcash-swift-wallet-sdk @ 4895ee058da9

*One-page brief* · Reviewed: 2026-11-06 14:13 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: Electric Coin Company (Zcash) — public repository (passive review)

Source: https://github.com/zcash/zcash-swift-wallet-sdk/tree/4895ee058da99971057cceb80f36b8909656a8a9

**Post-quantum maturity:** Level 0 of 4 — no post-quantum cryptography. **Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

**Findings:** Critical 0 · High 0 · Medium 7 · Low 20 · Info 4

**Quantum timeline (Mosca: x + y − z):** Key establishment 10 + 5 − 8 = 7 → too late; Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **Medium** · Quantum-vulnerable RSA key (2048-bit) in responsible_disclosure.md (QSI-2026-19144)\
   What to do: Inventory and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it..
2. **Medium** · Quantum-vulnerable RedDSA: transaction and message signing (1 file(s)) (QSI-2026-19143) · *preliminary*\
   What to do: Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains…
3. **Medium** · rsa 0.9.10 is affected by RUSTSEC-2023-0071 (CVE-2023-49092) (QSI-2026-19152)\
   What to do: Upgrade to a fixed version (none published yet; see the advisory for mitigations).
4. **Medium** · rustls 0.23.42 is affected by GHSA-2mjx-qc3c-rqvc (RUSTSEC-2026-0285) (QSI-2026-19153)\
   What to do: Upgrade to a fixed version (0.23.45).

23 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · transaction and message signing | RedDSA | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum… |

## Known vulnerable components

Advisories for the versions in use: 25; unlikely to apply to this build: 16 (a Cargo feature that is off, affected functions not named in the code, or a platform that is not built); to review: 9.

---

Static review of source code and manifests; files analysed: 205. No requests were sent to the owner's systems.

Full report, content SHA-256: `2d8b5fd188ac91539032dfc0c992994a3714083bf24b5b2cae09bf32785b8e32`

Full report signature (report.sig.json): Ed25519 key, SHA-256 fingerprint `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.