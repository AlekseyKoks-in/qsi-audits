# Post-quantum cryptography review: xrpl-rippled-quantum @ 816e5b65bd95

*One-page brief* · Reviewed: 2026-11-21 10:20 UTC · Risk profile: Web3 project · Client: XRPL Foundation — public repository (passive review)

Source: https://github.com/XRPLF/rippled/tree/816e5b65bd956a6a27e85d8722af03f488a5a2b2

**Post-quantum maturity:** Level 2 of 4 — post-quantum in use outside the critical paths. **Next step:** Extend post-quantum protection to the critical roles that stay classical, starting with what can be recorded today (wrapped keys, channel key exchange).

**Findings:** Critical 0 · High 0 · Medium 5 · Low 2 · Info 0

**Quantum timeline (Mosca: x + y − z):** Key establishment 5 + 5 − 12 = -2 → tight; Signatures 10 + 5 − 12 = 3 → too late

## What matters most

1. **Medium** · Quantum-vulnerable ECDSA: transaction and message signing (5 file(s)) (QSI-2026-34896) · *preliminary*\
   What to do: Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains…
2. **Medium** · Quantum-vulnerable Ed25519: transaction and message signing (3 file(s)) (QSI-2026-34898) · *preliminary*\
   What to do: Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains…
3. **Medium** · Quantum-vulnerable ECDSA: role not determined (15 file(s)) (QSI-2026-34893) · *preliminary*\
   What to do: Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form…
4. **Medium** · Quantum-vulnerable Ed25519: role not determined (4 file(s)) (QSI-2026-34894) · *preliminary*\
   What to do: Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form…

3 more in the full report.

## What the quantum-vulnerable cryptography protects

| Role | Algorithms | What to do |
|---|---|---|
| **Medium** · transaction and message signing | ECDSA, Ed25519 | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum… |
| **Medium** · authentication and identity (certificates, tokens, device attestation) | ECDSA | Keep credentials short-lived and plan ML-DSA certificates, tokens and keys as the ecosystem supports them |
| **Medium** · role not determined | ECDSA, Ed25519, EC-ElGamal, RSA | Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205)… |

---

Static review of source code and manifests; files analysed: 1258. No requests were sent to the owner's systems.

Full report, content SHA-256: `522d76c66777c5c945523d7ce86ab74b2ac4dcab4c460f5e90d23a774224d168`

Full report signature (report.sig.json): Ed25519 key, then the ML-DSA-65 one where it co-signs, SHA-256 fingerprints `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e · ML-DSA-65 dbd4e297b3213d1d7577a565e76de14cc5ad0e409f1dc68291c67266fc95066a`. bundle.sig.json lists the SHA-256 of every file in this bundle and is signed too; verify-bundle checks it offline.

Preliminary findings need confirmation in the code; the full report gives the evidence, the limits of each check and how to re-test.