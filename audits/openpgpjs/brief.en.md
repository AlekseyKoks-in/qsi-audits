# Post-quantum cryptography review: openpgpjs @ 8bc35df48879

*One-page brief* · Reviewed: 2026-11-24 10:58 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: OpenPGP.js project — public repository (passive review)

Source: https://github.com/openpgpjs/openpgpjs/tree/8bc35df4887933a3b2661e3741b33ba5f347b935

**Post-quantum maturity:** Level 2 of 4 — post-quantum in use outside the critical paths. **Next step:** Extend post-quantum protection to the critical roles that stay classical, starting with what can be recorded today (wrapped keys, channel key exchange).

**Findings:** Critical 0 · High 0 · Medium 8 · Low 0 · Info 3

**Quantum timeline (Mosca: x + y − z):** Key establishment 10 + 5 − 8 = 7 → too late; Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **Medium** · Quantum-vulnerable X25519: key wrapping and data encryption at rest (7 file(s)) (QSI-2026-48377) · *preliminary*\
   What to do: Wrap keys with ML-KEM or a hybrid KEM (X25519 + ML-KEM-768) and re-wrap the stored keys; data that may already have been copied needs its…
2. **Medium** · Quantum-vulnerable ECDH: key wrapping and data encryption at rest (2 file(s)) (QSI-2026-48380) · *preliminary*\
   What to do: Wrap keys with ML-KEM or a hybrid KEM (X25519 + ML-KEM-768) and re-wrap the stored keys; data that may already have been copied needs its…
3. **Medium** · Quantum-vulnerable ECDSA: role not determined (7 file(s)) (QSI-2026-48376) · *preliminary*\
   What to do: Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form…
4. **Medium** · Quantum-vulnerable ECDH: role not determined (1 file(s)) (QSI-2026-48383) · *preliminary*\
   What to do: Classify each usage, record data lifetimes, and plan migration to Hybrid key establishment with ML-KEM (FIPS 203), e.g. X25519MLKEM768 in…

4 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · key wrapping and data encryption at rest | X25519, ECDH | Wrap keys with ML-KEM or a hybrid KEM (X25519 + ML-KEM-768) and re-wrap the stored keys; data that may… |
| **Medium** · role not determined | ECDSA, X25519, ECDH, RSA | Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205)… |

Analyst review: 0 confirmed, 2 not applicable, 0 dismissed as false positives. (QSI review, 2026-11-22)

---

Static review of source code and manifests; files analysed: 108. No requests were sent to the owner's systems.

Full report, content SHA-256: `bfc10baaa4b3b1bb81fccdfcddd80392fb183f0ceb0a395c1b1b76cf204593a7`

Full report signature (report.sig.json): Ed25519 key, then the ML-DSA-65 one where it co-signs, SHA-256 fingerprints `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e · ML-DSA-65 dbd4e297b3213d1d7577a565e76de14cc5ad0e409f1dc68291c67266fc95066a`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.