# Post-quantum cryptography review: lightwalletd @ 4abfe9cd7b9b

*One-page brief* · Reviewed: 2026-11-24 17:17 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: Electric Coin Company (Zcash) — public repository (passive review)

Source: https://github.com/zcash/lightwalletd/tree/4abfe9cd7b9b13f6093df59911639d1d9195dc09

**Post-quantum maturity:** Level 3 of 4 — hybrid protection in a critical path. **Next step:** Pin the toolchain version and set the TLS groups in the code (X25519MLKEM768 first): the hybrid key exchange found rests on a default the code does not show, and a toolchain or library change would change it.

**Findings:** Critical 0 · High 0 · Medium 2 · Low 5 · Info 6 (of them advisories unlikely to apply: 5)

**Quantum timeline (Mosca: x + y − z):** Key establishment 10 + 5 − 8 = 7 → too late; Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **Medium** · Quantum-vulnerable RSA key in certificate (lightwalletd.testnet.local) (QSI-2026-50694)\
   What to do: Track in the PQC inventory; prefer short certificate lifetimes; follow CA/Browser Forum and NIST PQC transition guidance for ML-DSA…
2. **Medium** · Quantum-vulnerable RSA: role not determined (1 file(s)) (QSI-2026-50692) · *preliminary*\
   What to do: Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form…
3. **Low** · golang.org/x/net v0.58.0 is affected by GO-2026-6603 (CVE-2026-78659) (no severity rating) (QSI-2026-50698) · *preliminary*\
   What to do: Triage the advisory; upgrade to a fixed version (0.60.0) if it applies.

4 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · role not determined | RSA | Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205)… |

## Known vulnerable components

Advisories for the versions in use: 10; unlikely to apply to this build: 5 (no call path to the affected code, a module only tests use, functions not named in the code, a Cargo feature that is off or a platform not built); to review: 5.

Analyst review: 0 confirmed, 1 not applicable, 0 dismissed as false positives. (QSI review, 2026-10-23)

---

Static review of source code and manifests; files analysed: 34. No requests were sent to the owner's systems.

Full report, content SHA-256: `e0fa5bd5f70ded1e7ed3914849cc00e96a6d73b4d67bc2dec65f011f6123e970`

Full report signature (report.sig.json): Ed25519 key, then the ML-DSA-65 one where it co-signs, SHA-256 fingerprints `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e · ML-DSA-65 dbd4e297b3213d1d7577a565e76de14cc5ad0e409f1dc68291c67266fc95066a`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.