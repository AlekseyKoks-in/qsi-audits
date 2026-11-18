# Post-quantum cryptography review: signal-desktop @ 17502b9d1a9e

*One-page brief* · Reviewed: 2026-11-17 18:53 UTC · Risk profile: Crypto exchange, custodian or wallet · Client: Signal Messenger — public repository (passive review)

Source: https://github.com/signalapp/Signal-Desktop/tree/17502b9d1a9e34af689f31508c4ac4ccee5b5cb7

**Post-quantum maturity:** Level 1 of 4 — post-quantum code present, not wired. **Next step:** Wire the existing post-quantum primitive into a critical path (key wrapping or the channel) behind a hybrid construction, and test interoperability.

**Findings:** Critical 1 · High 20 · Medium 16 · Low 3 · Info 1

## What matters most

1. **Critical** · @storybook/core 8.6.18 is affected by GHSA-f2ph-cmg5-wxc8 (CVE-2026-114125) (QSI-2026-27882)\
   What to do: Upgrade to a fixed version (8.6.19).
2. **High** · zod 4.3.6 is affected by GHSA-mrhx-c7xc-m3w5 (CVE-2023-54404) (QSI-2026-27874)\
   What to do: Upgrade to a fixed version (4.6.6).
3. **High** · uuid 13.0.0 is affected by GHSA-w5hq-g745-h8pq (CVE-2026-41907, CVE-2026-41988) (QSI-2026-27911)\
   What to do: Upgrade to a fixed version (11.1.1, 12.0.1, 13.0.1).
4. **High** · zod 3.25.76 is affected by GHSA-mrhx-c7xc-m3w5 (CVE-2023-54404) (QSI-2026-27912)\
   What to do: Upgrade to a fixed version (4.6.6).
5. **High** · Possible hard-coded secret in ts/state/smart/fun/giphy.preload.ts (QSI-2026-27873) · *preliminary*\
   What to do: Move secrets to a secrets manager/environment; rotate the exposed values.
6. **High** · picomatch 2.3.2 is affected by GHSA-fc5q-39xc-vjpf (CVE-2026-112366) (QSI-2026-27875)\
   What to do: Upgrade to a fixed version (none published yet; see the advisory for mitigations).

34 more in the full report.

## Known vulnerable components

Advisories for the versions in use: 39; each needs checking against the code.

---

Static review of source code and manifests; files analysed: 2202. No requests were sent to the owner's systems.

Full report, content SHA-256: `324a9363abafe07bc91b90bbea83b9ef66f96b1ea98624f2dffda606fd2db881`

Full report signature (report.sig.json): Ed25519 key, then the ML-DSA-65 one where it co-signs, SHA-256 fingerprints `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e · ML-DSA-65 dbd4e297b3213d1d7577a565e76de14cc5ad0e409f1dc68291c67266fc95066a`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.