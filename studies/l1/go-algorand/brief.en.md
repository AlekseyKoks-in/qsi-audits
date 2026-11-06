# Post-quantum cryptography review: go-algorand @ e46aea5466a1

*One-page brief* · Reviewed: 2026-11-06 16:16 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: Algorand Foundation — public repository (passive review)

Source: https://github.com/algorand/go-algorand/tree/e46aea5466a1152af6e08f83555ed16cfcd89f49

**Post-quantum maturity:** Level 2 of 4 — post-quantum in use outside the critical paths. **Next step:** Extend post-quantum protection to the critical roles that stay classical, starting with what can be recorded today (wrapped keys, channel key exchange).

**Findings:** Critical 0 · High 1 · Medium 11 · Low 3 · Info 7

**Quantum timeline (Mosca: x + y − z):** Key establishment 10 + 5 − 8 = 7 → too late; Signatures 10 + 5 − 8 = 7 → too late

## What matters most

1. **High** · Possible hard-coded secret in logging/telemetryConfig.go (QSI-2026-19631) · *preliminary*\
   What to do: Move secrets to a secrets manager/environment; rotate the exposed values.
2. **Medium** · Quantum-vulnerable RSA key (2048-bit) in installer/rpm/RPM-GPG-KEY-Algorand (QSI-2026-19630)\
   What to do: Inventory and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it..
3. **Medium** · github.com/labstack/echo/v4 v4.16.1 is affected by GHSA-246p-cpwv-v3jq (CVE-2026-118653… (QSI-2026-19635)\
   What to do: Upgrade to a fixed version (none published yet; see the advisory for mitigations).
4. **Medium** · github.com/labstack/echo/v4 v4.16.1 is affected by GHSA-99jh-6h7p-pp36 (CVE-2026-118651… (QSI-2026-19636)\
   What to do: Upgrade to a fixed version (none published yet; see the advisory for mitigations).

11 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · key wrapping and data encryption at rest | X25519 | Wrap keys with ML-KEM or a hybrid KEM (X25519 + ML-KEM-768) and re-wrap the stored keys; data that may… |
| **Medium** · transaction and message signing | ECDSA | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum… |
| **Medium** · role not determined | Ed25519, X25519, ECDH, RSA | Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205)… |

## Known vulnerable components

Advisories for the versions in use: 14; unlikely to apply to this build: 7 (a Cargo feature that is off, affected functions not named in the code, or a platform that is not built); to review: 7.

---

Static review of source code and manifests; files analysed: 1160. No requests were sent to the owner's systems.

Full report, content SHA-256: `6d145d52c9c066144e055074447ebfbd4d0fe3daaa4654cbf36de67ea6eb5165`

Full report signature (report.sig.json): Ed25519 key, SHA-256 fingerprint `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.