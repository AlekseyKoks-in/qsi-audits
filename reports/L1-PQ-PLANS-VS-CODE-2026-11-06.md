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

## Correction, 2026-11-19

The own-code figures for Stellar and Arc in the table above counted test-support code as shipped. soroban-env-host
compiles `testutils.rs`, `builtin_contracts/testutils.rs` and `e2e_testutils.rs` only under
`#[cfg(any(test, feature = "testutils"))]`, and arc-node's precompiles gate `pq_test_vectors.rs` behind `test-utils`
and build its generator as a separate tool. Re-audited at the same commits, on the same trees, the bundles in
`studies/l1/` now give: Stellar **55 + 175** own-code rows (was 58 + 186) and **36 + 136** Shor-breakable (was 38 + 143);
Arc **34** own-code rows (was 37) and **12** Shor-breakable (unchanged). Arc's three removed rows were the SLH-DSA rows of
its test-vector generator; the SLH-DSA verification precompile cited above is unaffected, and no other cell of the table
changes. The README's dated section of the same day gives the measurement.

## Re-issue, 2026-11-22

Every bundle of this study was re-audited on 23 November at its recorded commit, tree and analyst decisions with engine 1.16.2, and is now co-signed with ML-DSA-65 (`python3 verify.py studies/l1/*`). Figures of the table that move: `go-algorand` **97** own-code rows and **27** Shor-breakable (was 93 and 26), post-quantum rows **6** (was 3): Falcon-512 is now recognised in `crypto/falconWrapper.go`, the generated codec and `cmd/algokey`, beside the state-proof keys already counted, and Ed25519 in the p2p peer identity; `aptos-core` **79** own-code rows and **55** Shor-breakable (was 82 and 58): rows counted twice are gone (bare ECDSA rows beside the secp256r1 ones, a second Ed25519 row of the signing traits) and BLS12-381 is read from the code rather than from file names; `rs-soroban-env` **50** own-code rows and **31** Shor-breakable (was 55 and 36): a line that names its curve (ECDSA on secp256k1 or P-256, in `crypto/mod.rs` and the cost runners) was also counted as a bare ECDSA row; `stellar-core` **155** own-code rows and **116** Shor-breakable (was 175 and 136): the same double count, in the four protocol versions of Soroban it vendors (`src/rust/soroban/p21` to `p24`). Solana's row reads 115 Shor-breakable of 212 rows since the re-measure of 6 November (four ElGamal rows of confidential transfers), unchanged by this re-issue. No verifier, account type or consensus key named above changes.

*QSI — quantum-readiness inventory of cryptography. Contact: alekseykoksin@gmail.com.*
