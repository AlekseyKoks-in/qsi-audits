# Post-quantum cryptography review: trezor-vendored-crypto @ 72489948b3c4

*One-page brief* · Reviewed: 2026-11-06 14:40 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: Trezor (vendored primitives) — public repository (passive review)

Source: https://github.com/trezor/trezor-firmware/tree/72489948b3c44a37598de9da658be28e4fabb4ae

**Post-quantum maturity:** Level 1 of 4 — post-quantum code present, not wired. **Next step:** Wire the existing post-quantum primitive into a critical path (key wrapping or the channel) behind a hybrid construction, and test interoperability.

**Findings:** Critical 0 · High 0 · Medium 4 · Low 0 · Info 0

**Quantum timeline (Mosca: x + y − z):** Key establishment 10 + 5 − 8 = 7 → too late; Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **Medium** · Quantum-vulnerable ECDSA: transaction and message signing (21 file(s)) (QSI-2026-19291) · *confirmed by the analyst*\
   What to do: Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains…
2. **Medium** · Quantum-vulnerable Schnorr (BIP-340): transaction and message signing (3 file(s)) (QSI-2026-19293) · *confirmed by the analyst*\
   What to do: Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains…
3. **Medium** · Quantum-vulnerable Ed25519: role not determined (5 file(s)) (QSI-2026-19290) · *confirmed by the analyst*\
   What to do: Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form…
4. **Medium** · Quantum-vulnerable ECDH: role not determined (4 file(s)) (QSI-2026-19292) · *confirmed by the analyst*\
   What to do: Classify each usage, record data lifetimes, and plan migration to Hybrid key establishment with ML-KEM (FIPS 203), e.g. X25519MLKEM768 in…

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · transaction and message signing | ECDSA, Schnorr (BIP-340) | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum… |
| **Medium** · role not determined | Ed25519, ECDH | Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205)… |

Analyst review: 4 confirmed, 0 not applicable, 0 dismissed as false positives. (QSI review, 2026-10-29)

---

Static review of source code and manifests; files analysed: 505. No requests were sent to the owner's systems.

Full report, content SHA-256: `61dd2de82e4d564b1a3f4c220a2b6a15bf0407f3722f3b05d874bae599441e13`

Full report signature (report.sig.json): Ed25519 key, SHA-256 fingerprint `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.