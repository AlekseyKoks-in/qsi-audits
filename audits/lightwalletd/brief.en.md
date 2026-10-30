# Post-quantum cryptography review: lightwalletd @ 4abfe9cd7b9b

*One-page brief* · Reviewed: 2026-10-29 23:10 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: Electric Coin Company (Zcash) — public repository (passive review)

Source: https://github.com/zcash/lightwalletd/tree/4abfe9cd7b9b13f6093df59911639d1d9195dc09

**Post-quantum maturity:** Level 0 of 4 — no post-quantum cryptography. **Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

**Findings:** Critical 0 · High 0 · Medium 2 · Low 8 · Info 4

**Quantum timeline (Mosca: x + y − z):** Key establishment 10 + 5 − 8 = 7 → too late; Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **Medium** · Quantum-vulnerable RSA key in certificate (lightwalletd.testnet.local) (QSI-2026-07097)\
   What to do: Track in the PQC inventory; prefer short certificate lifetimes; follow CA/Browser Forum and NIST PQC transition guidance for ML-DSA…
2. **Medium** · Quantum-vulnerable RSA: role not determined (1 file(s)) (QSI-2026-07095) · *preliminary*\
   What to do: Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form…
3. **Low** · golang.org/x/crypto v0.55.0 is affected by GO-2026-5932 (no severity rating) (QSI-2026-07099) · *preliminary*\
   What to do: Triage the advisory; upgrade to a fixed version (none published yet; see the advisory for mitigations) if it applies.
4. **Low** · golang.org/x/crypto v0.55.0 is affected by GO-2026-6354 (CVE-2026-78662) (no severity rating) (QSI-2026-07100) · *preliminary*\
   What to do: Triage the advisory; upgrade to a fixed version (0.56.0) if it applies.

6 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · role not determined | RSA | Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205)… |

## Known vulnerable components

Advisories for the versions in use: 10; unlikely to apply to this build: 2 (a Cargo feature that is off, affected functions not named in the code, or a platform that is not built); to review: 8.

Analyst review: 0 confirmed, 1 not applicable, 0 dismissed as false positives. (QSI review, 2026-10-23)

---

Static review of source code and manifests; files analysed: 34. No requests were sent to the owner's systems.

Full report, content SHA-256: `ee01be5a6a668e45f80173febb444271441656e5c2f98f8ad60408f1e35ec330`

Full report signature (report.sig.json): Ed25519 key, SHA-256 fingerprint `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.