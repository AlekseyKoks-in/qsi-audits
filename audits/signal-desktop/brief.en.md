# Post-quantum cryptography review: signal-desktop @ 17502b9d1a9e

*One-page brief* · Reviewed: 2026-11-04 19:27 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: Signal Messenger — public repository (passive review)

Source: https://github.com/signalapp/Signal-Desktop/tree/17502b9d1a9e34af689f31508c4ac4ccee5b5cb7

**Post-quantum maturity:** Level 1 of 4 — post-quantum code present, not wired. **Next step:** Wire the existing post-quantum primitive into a critical path (key wrapping or the channel) behind a hybrid construction, and test interoperability.

**Findings:** Critical 1 · High 6 · Medium 3 · Low 0 · Info 1

## What matters most

1. **Critical** · @storybook/core 8.6.18 is affected by GHSA-f2ph-cmg5-wxc8 (CVE-2026-114125) (QSI-2026-12828)\
   What to do: Upgrade to a fixed version (8.6.19).
2. **High** · zod 4.3.6 is affected by GHSA-mrhx-c7xc-m3w5 (CVE-2023-54404) (QSI-2026-12821)\
   What to do: Upgrade to a fixed version (4.6.6).
3. **High** · Possible hard-coded secret in ts/state/smart/fun/giphy.preload.ts (QSI-2026-12820) · *preliminary*\
   What to do: Move secrets to a secrets manager/environment; rotate the exposed values.
4. **High** · undici 6.29.0 is affected by GHSA-2m5v-pch6-74hx (CVE-2026-109383) (QSI-2026-12823)\
   What to do: Upgrade to a fixed version (6.29.1, 7.30.1, 8.12.2).
5. **High** · undici 6.29.0 is affected by GHSA-qrxm-fqhp-jwvm (CVE-2026-87018) (QSI-2026-12826)\
   What to do: Upgrade to a fixed version (6.29.1, 7.30.1, 8.12.2).
6. **High** · undici 6.29.0 is affected by GHSA-xjj6-f33q-929c (CVE-2026-109869) (QSI-2026-12827)\
   What to do: Upgrade to a fixed version (6.29.1, 7.30.1, 8.12.2).

4 more in the full report.

## Known vulnerable components

Advisories for the versions in use: 9; each needs checking against the code.

---

Static review of source code and manifests; files analysed: 2202. No requests were sent to the owner's systems.

Full report, content SHA-256: `ac7b6c0c129e043eb4d1f4e7e84808016014c6d36c2007a6f6d604f27c19565c`

Full report signature (report.sig.json): Ed25519 key, SHA-256 fingerprint `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.