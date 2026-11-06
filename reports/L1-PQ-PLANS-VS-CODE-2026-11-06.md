# Layer-1 post-quantum plans versus the code (2026-11-06)

Five layer-1 networks have announced post-quantum plans. This report checks what their own repositories contain at
a pinned commit. Every post-quantum line cited below was opened and read; the totals come from QSI's signed bundles in
`studies/l1/<name>/`, verifiable offline with `python3 verify.py studies/l1/*`.

| Network | Repository @ commit | Own-code rows | Shor-breakable | Post-quantum in the code | Still classical |
|---|---|---:|---:|---|---|
| Algorand | `go-algorand` @ `e46aea5` | 93 | 26 | **Falcon** state-proof keys (`crypto/merklesignature`, `stateproof/signer.go`); AVM `falcon_verify` opcode, Falcon-512 and Falcon-1024 (`data/transactions/logic/opcodes.go:860`) | Accounts, consensus votes and VRF sortition (Ed25519, `crypto/vrf.go`) |
| Aptos | `aptos-core` @ `81d89f4` (scoped: crypto, types, framework, keyless) | 82 | 58 | **SLH-DSA-SHA2-128s** account keys (`crates/aptos-crypto/src/slh_dsa_sha2_128s/`) behind an on-chain feature flag (`types/src/on_chain_config/aptos_features.rs:170`) | Default accounts Ed25519, validator BLS12-381, keyless Groth16 on BN254, noise X25519 |
| Stellar | `rs-soroban-env` @ `0c99950`, `stellar-core` @ `362dbc5` | 58 + 186 | 38 + 143 | **ML-DSA** host function in Soroban (`soroban-env-host/src/crypto/ml_dsa.rs:21`) | Account signers and SCP consensus Ed25519; overlay peer authentication X25519 |
| Arc (Circle) | `arc-node` @ `6e76402` | 37 | 12 | **SLH-DSA** verification precompile (`crates/pq-precompile/src/lib.rs:22`) | Consensus votes and proposals Ed25519 (`crates/types/src/signing.rs:21`) |
| Solana | `agave` (portfolio bundle) | — | 111 of 208 rows | none in the validator client | Accounts and votes Ed25519 |

## What the code says

**Signatures are moving first, and only as an option.** Every network that has started has added a post-quantum
*verifier* or an *opt-in account type*: Falcon on Algorand, SLH-DSA on Aptos and Arc, ML-DSA in Soroban. None has
replaced its consensus signatures. Validators and default accounts sign with Ed25519 or BLS12-381 on all five. That
is the right order for user funds, because an opt-in account is protected the day it is created. It leaves the
consensus key set as the part an attacker with a quantum computer would forge.

**Algorand is the furthest along, in two places.** State proofs, the mechanism that lets other chains verify
Algorand's history, are signed with Falcon keys today, and smart contracts can verify Falcon signatures natively.
Its consensus sortition still depends on an Ed25519-based VRF.

**Aptos has the most complete account path.** SLH-DSA keys sit in the core crypto crate and in the transaction
authenticator, behind an on-chain feature flag. Note for anyone auditing it: `gh api repos/aptos-labs/aptos-core/commits/HEAD`
resolves to a 2024 commit without this code (a ref named `HEAD`). Our first run used it and reported no post-quantum
code. Resolve the default branch instead.

**Encryption is absent everywhere.** No repository here negotiates ML-KEM in its own peer-to-peer layer. Peer
traffic on public chains is mostly public data, so this matters less than it does for the permissioned ledgers in
[INSTITUTIONAL-LEDGERS-2026-11-06.md](INSTITUTIONAL-LEDGERS-2026-11-06.md).

## Method and limits

Static review of each tree at the commit shown, with test, benchmark, fuzzing and example code excluded, and
vendored code reported apart from the project's own code. aptos-core was reviewed on the five paths named, not the
whole monorepo. A verifier in the code does not mean it is enabled on mainnet: feature flags and protocol versions
decide that, and this report does not claim activation.

*QSI — quantum-readiness inventory of cryptography. Contact: alekseykoksin@gmail.com.*
