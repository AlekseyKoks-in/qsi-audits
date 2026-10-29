# Post-quantum cryptography review: librustzcash @ 8672a4b2d60f

*One-page brief* · Reviewed: 2026-10-28 12:28 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: Electric Coin Company (Zcash) — public repository (passive review)

Source: https://github.com/zcash/librustzcash/tree/8672a4b2d60f432664780e6a4e85f49a36805a2a

**Post-quantum maturity:** Level 0 of 4 — no post-quantum cryptography. **Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

**Findings:** Critical 0 · High 2 · Medium 10 · Low 32 · Info 7

**Quantum timeline (Mosca: x + y − z):** Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **High** · rustls-webpki 0.101.7 is affected by GHSA-82j2-j2ch-gfr8 (CVE-2026-93599, RUSTSEC-2026-0104) (QSI-2026-04498)\
   What to do: Upgrade to a fixed version (0.103.13, 0.104.0-alpha.7).
2. **High** · rustls-webpki 0.103.3 is affected by GHSA-82j2-j2ch-gfr8 (CVE-2026-93599, RUSTSEC-2026-0104) (QSI-2026-04502)\
   What to do: Upgrade to a fixed version (0.103.13, 0.104.0-alpha.7).
3. **Medium** · serde_with 3.16.0 is affected by GHSA-7gcf-g7xr-8hxj (QSI-2026-04507)\
   What to do: Upgrade to a fixed version (3.21.0).
4. **Medium** · Quantum-vulnerable ECDSA: transaction and message signing (15 file(s)) (QSI-2026-04471) · *preliminary*\
   What to do: Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains…

40 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · transaction and message signing | ECDSA, BLS12-381 | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum… |

## Known vulnerable components

Advisories for the versions in use: 43; unlikely to apply to this build: 14 (a Cargo feature that is off, affected functions not named in the code, or a platform that is not built); to review: 29.

---

Static review of source code and manifests; files analysed: 333. No requests were sent to the owner's systems.

Full report, content SHA-256: `81ab30c80d5b748a201294a9babfd1a7209fb108ef54f431fd522308b135270a`

Full report signature (report.sig.json): Ed25519 key, SHA-256 fingerprint `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.