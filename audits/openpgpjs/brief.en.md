# Post-quantum cryptography review: openpgpjs @ 8bc35df48879

*One-page brief* · Reviewed: 2026-10-28 12:44 UTC · Risk profile: Security software vendor · Client: OpenPGP.js project — public repository (passive review)

Source: https://github.com/openpgpjs/openpgpjs/tree/8bc35df4887933a3b2661e3741b33ba5f347b935

**Post-quantum maturity:** Level 2 of 4 — post-quantum in use outside the critical paths. **Next step:** Extend post-quantum protection to the critical roles that stay classical, starting with what can be recorded today (wrapped keys, channel key exchange).

**Findings:** Critical 0 · High 0 · Medium 7 · Low 1 · Info 1

**Quantum timeline (Mosca: x + y − z):** Key establishment 10 + 3 − 8 = 5 → too late; Signatures 5 + 3 − 8 = 0 → tight

## What matters most

1. **Medium** · Quantum-vulnerable X25519: key wrapping and data encryption at rest (5 file(s)) (QSI-2026-04759) · *preliminary*\
   What to do: Wrap keys with ML-KEM or a hybrid KEM (X25519 + ML-KEM-768) and re-wrap the stored keys; data that may already have been copied needs its…
2. **Medium** · Quantum-vulnerable ECDH: key wrapping and data encryption at rest (1 file(s)) (QSI-2026-04764) · *preliminary*\
   What to do: Wrap keys with ML-KEM or a hybrid KEM (X25519 + ML-KEM-768) and re-wrap the stored keys; data that may already have been copied needs its…
3. **Medium** · Quantum-vulnerable ECDH: role not determined (2 file(s)) (QSI-2026-04762) · *preliminary*\
   What to do: Classify each usage, record data lifetimes, and plan migration to Hybrid key establishment with ML-KEM (FIPS 203), e.g. X25519MLKEM768 in…
4. **Medium** · Quantum-vulnerable X25519: role not determined (5 file(s)) (QSI-2026-04763) · *preliminary*\
   What to do: Classify each usage, record data lifetimes, and plan migration to Hybrid key establishment with ML-KEM (FIPS 203), e.g. X25519MLKEM768 in…

4 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · key wrapping and data encryption at rest | X25519, ECDH | Wrap keys with ML-KEM or a hybrid KEM (X25519 + ML-KEM-768) and re-wrap the stored keys; data that may… |
| **Medium** · role not determined | ECDSA, X25519, ECDH, RSA | Classify each usage, record data lifetimes, and plan migration to Hybrid key establishment with ML-KEM (FIPS… |

---

Static review of source code and manifests; files analysed: 108. No requests were sent to the owner's systems.

Full report, content SHA-256: `b2ce41a779ab83da67c60c3d95217832c3b36f0255aef76330dcb58b2cfe65da`

Full report signature (report.sig.json): Ed25519 key, SHA-256 fingerprint `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.