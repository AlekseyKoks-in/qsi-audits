# Security & Post-Quantum Readiness Audit Report

**Project:** xrpl-go @ 23275f007b47 · XRPL Foundation — public repository (passive review)
| | |
|---|---|
| Organization | QSI |
| Report date | 2026-11-24 12:23 UTC |
| Report version | 1 |
| Audit run | d0ec19fe-029d-4de5-b315-e8a92baf2623 (Document audit) |
| Analyzer engine | qsi-engine 1.20.0 |
| Risk profile | Web3 project |
| Content SHA-256 | `f9db4079968b71a485ee3267c4405c7e7d0a37423da25741100e5100741b87e8` |
| Signature key (Ed25519 SHA-256 fingerprint, then the ML-DSA-65 one where it co-signs; the signature is the separate file report.sig.json) | `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e · ML-DSA-65 dbd4e297b3213d1d7577a565e76de14cc5ad0e409f1dc68291c67266fc95066a` |
> This report presents automated and documented analysis results for the stated scope. It is not a legal opinion, a certification or an attestation of compliance with any standard.

## 1. Executive summary

- Critical: **0**
- High: **0**
- Medium: **4**
- Low: **4**
- Info: **3**

- Confirmed technical vulnerability: 0
- Known vulnerable component: 2
- Confirmed configuration error: 0
- Potential cryptographic risk: 0
- Long-term post-quantum risk: 7
- Improvement recommendation: 1
- Insufficient data: 1

Mosca's inequality (x + y > z): x = 5, y = 5, z = 12 → tight margin. _z is a planning assumption chosen per risk profile, not a prediction. A cryptographically relevant quantum computer is not publicly known to exist today._

**Post-quantum maturity: Level 0 of 4 — no post-quantum cryptography.** Next step: Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

## 2. Scope and boundaries

Mode: Document audit

Repository: <https://github.com/XRPLF/xrpl-go> @ `23275f007b4758e82809f51d1e4ec3c5efb2fbe0` — evidence links open the lines at this commit.

514 files, 20335888 bytes in total, 0 redaction(s); the per-file SHA-256 list is in appendix C.

## 3. Methodology

| Area | Status | Count | Examples |
|---|---|---|---|
| source_code | checked | 508 | .agents/skills/xrpl-standards/scripts/extract-spec.py: 316 lines scanned with 17 rule patterns and 340 registry patterns; .agents/skills/xrpl-standards/scripts/sync-xls-standards.py: 381 lines scanned with 17 rule patterns and 340 registry patterns; address-codec/address.go: 73 lines scanned with 17 rule patterns and 340 registry patterns |
| dependencies | checked | 4 | confidential/go.mod: 17 dependencies parsed (17 pinned); docs/package.json: 12 dependencies parsed (0 pinned); docs/yarn.lock: 1205 dependencies parsed (1205 pinned) |
| entropy | checked | 1 | random-number generation: 508 code files read with 42 macro definitions from the tree; 0 ineffective guard(s), 0 weak random-bytes provider(s), 0 weak key-generation site(s) |
| crediting | checked | 1 | payment crediting: 120 file(s) read incoming transfers on TON, the XRP Ledger (Xaman sign requests included), Tron or an EVM chain, 0 credit from a Tron or EVM node, 0 from fetched Solana transactions; 0 lead(s). A wait for confirmations or finality is recognised by its words, not traced; reorganisations and duplicate crediting are not checked |
| key_storage | checked | 1 | key settings with a fallback in the code: 0; decryption fallbacks: 0; derived nonces: 0; key columns: 0 (a KMS, HSM or vault service is used); author warnings: 0 |
| govulncheck | checked | 1 | govulncheck@v1.9.0 with the Go vulnerability database of 2026-11-23: 2 of 2 Go module(s) scanned from their product packages |
| osv_advisories | checked | 1 | 1225 pinned packages queried at OSV.dev; 3 affected (1 of them only in development or build dependencies) |

_Long lists are grouped here; the full per-file list is in the JSON report, signed with the same key._

## 4. Assets examined and not examined

- None

## 5. Architecture overview

Static review of the source tree xrpl-go at 23275f007b4758e82809f51d1e4ec3c5efb2fbe0. 514 files analysed; of 1442 files, 584 are test, fuzzing, benchmark or example code and were left out, 342 are not read by any analyzer, 2 exceed the per-file limit and 0 did not fit the total limit. Files no analyzer reads include: .agents/skills/address-pr-comments/SKILL.md, .agents/skills/go-concurrency/AGENTS.md, .agents/skills/go-concurrency/SKILL.md, .agents/skills/go-concurrency/rules/_sections.md, .agents/skills/go-concurrency/rules/_template.md. 30 files in build-output or dependency-cache directories (.git, .hg, .venv, __pycache__, build, dist, node_modules, target, vendor, venv) were not read. No requests were sent to the owner's systems.

## 6. Overall security posture

- Indicative posture index: **99** / 100 — _Derived from findings in scope (confirmed and potential issues weighted by severity). Indicative only; not comparable across differently scoped audits._
- Quantum-vulnerable share of inventory: 76.9%

## 7. Detailed findings

### QSI-2026-50278 — Quantum-vulnerable ECDSA: transaction and message signing (9 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:ECDSA:transaction_signing`
- Data source: address-codec/codec.go
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.20.0 · 2026-11-24 12:23 UTC
- Priority score: 33.0 / 100
- CVSS v3.1: not applicable

59 reference(s) to ECDSA across 9 file(s), e.g. address-codec/codec.go:126. Role, judged from paths, function names and nearby code: transaction and message signing. A CRQC derives the private key from a public key that is already known (on chain after the first spend, in reused addresses): funds and approvals controlled by these keys need a migration path.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open address-codec/codec.go:126 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [address-codec/codec.go](https://github.com/XRPLF/xrpl-go/blob/23275f007b4758e82809f51d1e4ec3c5efb2fbe0/address-codec/codec.go#L126) · line 126 · SHA-256 9bc5d0aa806c8b7391b599a260c9e56f46090c76a9d52a8a7e78e7172555ca54_

```
  125 | 		return Encode(entropy, ed25519.FamilySeedPrefix(), FamilySeedLength)
  126 | 	} else if secp256k1 := crypto.SECP256K1(); encodingType == secp256k1 {
  127 | 		return Encode(entropy, secp256k1.FamilySeedPrefix(), FamilySeedLength)
```

_file_excerpt · [address-codec/codec.go](https://github.com/XRPLF/xrpl-go/blob/23275f007b4758e82809f51d1e4ec3c5efb2fbe0/address-codec/codec.go#L127) · line 127 · SHA-256 c4ceb8f6d3e305178d3c847cb421dbd4f065eea18226a20779066dfe0e488ee9_

```
  126 | 	} else if secp256k1 := crypto.SECP256K1(); encodingType == secp256k1 {
  127 | 		return Encode(entropy, secp256k1.FamilySeedPrefix(), FamilySeedLength)
  128 | 	}
```

_file_excerpt · [address-codec/codec.go](https://github.com/XRPLF/xrpl-go/blob/23275f007b4758e82809f51d1e4ec3c5efb2fbe0/address-codec/codec.go#L154) · line 154 · SHA-256 ab1c233801236a49dbea03b9047719cff3d41e8f4a4838fabbca097974e63114_

```
  153 | 
  154 | 	secp256k1 := crypto.SECP256K1()
  155 | 	secp256k1Prefix := secp256k1.FamilySeedPrefix()
```

_file_excerpt · [address-codec/errors.go](https://github.com/XRPLF/xrpl-go/blob/23275f007b4758e82809f51d1e4ec3c5efb2fbe0/address-codec/errors.go#L20) · line 20 · SHA-256 d89d949df4633af81826f12e285b4cdb228fafe7fbd13734a44106b00203d9fa_

```
   19 | 	// ErrInvalidEncodingType indicates that a seed encoding type is neither ed25519 nor secp256k1.
   20 | 	ErrInvalidEncodingType = errors.New("encoding type must be `ed25519` or `secp256k1`")
   21 | 	// ErrInvalidXAddress indicates an invalid x-address.
```

_file_excerpt · [confidential/builder/clawback.go](https://github.com/XRPLF/xrpl-go/blob/23275f007b4758e82809f51d1e4ec3c5efb2fbe0/confidential/builder/clawback.go#L48) · line 48 · SHA-256 16165aec80cde5ffbf39794faf5722ca0e9632b5619690214c16c452b8de54d6_

```
   47 | 	IssuanceID    string
   48 | 	IssuerPrivKey string              // Non-zero secp256k1 scalar below the curve order, also used to decrypt the holder balance
   49 | 	BalanceRange  elgamal.AmountRange // Inclusive bounds for decrypting the holder's balance
```

_file_excerpt · [confidential/builder/clawback.go](https://github.com/XRPLF/xrpl-go/blob/23275f007b4758e82809f51d1e4ec3c5efb2fbe0/confidential/builder/clawback.go#L57) · line 57 · SHA-256 d1f022a96d0454978cc8ae9c6b7b27497518f1bfe3357b638840abe7fb4f3892_

```
   56 | 	Amount           uint64 // The holder's complete confidential balance, which a clawback removes in full
   57 | 	IssuerPubKey     string // Valid 33-byte compressed secp256k1 point from MPTokenIssuance.IssuerEncryptionKey
   58 | 	IssuerCiphertext string // Two valid compressed secp256k1 points from the holder MPToken's IssuerEncryptedBalance
```

_file_excerpt · [confidential/builder/clawback.go](https://github.com/XRPLF/xrpl-go/blob/23275f007b4758e82809f51d1e4ec3c5efb2fbe0/confidential/builder/clawback.go#L58) · line 58 · SHA-256 588bb6fc61ab7ffe8d035129cf942afc074cb370e8f9a1d81aa4713205a39333_

```
   57 | 	IssuerPubKey     string // Valid 33-byte compressed secp256k1 point from MPTokenIssuance.IssuerEncryptionKey
   58 | 	IssuerCiphertext string // Two valid compressed secp256k1 points from the holder MPToken's IssuerEncryptedBalance
   59 | }
```

_file_excerpt · [confidential/builder/errors.go](https://github.com/XRPLF/xrpl-go/blob/23275f007b4758e82809f51d1e4ec3c5efb2fbe0/confidential/builder/errors.go#L75) · line 75 · SHA-256 68c15f0cdce6059201a7ba9126b09ba557d6aba07afdac0fdd8ca4c968ca90bf_

```
   74 | 	ErrInvalidIssuanceID  = errors.New("builder: issuance ID must be exactly 48 hex characters")
   75 | 	ErrInvalidPrivKey     = errors.New("builder: private key must be a non-zero secp256k1 scalar")
   76 | 	ErrInvalidPubKey      = errors.New("builder: public key must be a valid 33-byte compressed secp256k1 point")
```

_file_excerpt · [confidential/builder/errors.go](https://github.com/XRPLF/xrpl-go/blob/23275f007b4758e82809f51d1e4ec3c5efb2fbe0/confidential/builder/errors.go#L76) · line 76 · SHA-256 ca6b77796fa4ad617c5757d3ff35989cae8f7e096c958573e15ad31de20a1e71_

```
   75 | 	ErrInvalidPrivKey     = errors.New("builder: private key must be a non-zero secp256k1 scalar")
   76 | 	ErrInvalidPubKey      = errors.New("builder: public key must be a valid 33-byte compressed secp256k1 point")
   77 | 	ErrInvalidCiphertext  = errors.New("builder: ciphertext must contain two valid compressed secp256k1 points")
```

_file_excerpt · [confidential/builder/errors.go](https://github.com/XRPLF/xrpl-go/blob/23275f007b4758e82809f51d1e4ec3c5efb2fbe0/confidential/builder/errors.go#L77) · line 77 · SHA-256 4ac7262241b0580f4008e9fb18a719900502ef5a1cbd1bf3a1e1769fc358d86e_

```
   76 | 	ErrInvalidPubKey      = errors.New("builder: public key must be a valid 33-byte compressed secp256k1 point")
   77 | 	ErrInvalidCiphertext  = errors.New("builder: ciphertext must contain two valid compressed secp256k1 points")
   78 | 	ErrInvalidTransaction = errors.New("builder: prepared transaction is invalid")
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains adopt them.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-50280 — Quantum-vulnerable Pedersen commitment: threshold signing and MPC protocols (5 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:Pedersen commitment:threshold_mpc`
- Data source: confidential/commitment/commitment.go
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.20.0 · 2026-11-24 12:23 UTC
- Priority score: 33.0 / 100
- CVSS v3.1: not applicable

9 reference(s) to Pedersen commitment across 5 file(s), e.g. confidential/commitment/commitment.go:24. Role, judged from paths, function names and nearby code: threshold signing and MPC protocols. Paillier, Pedersen commitments and the discrete-logarithm proofs inside threshold ECDSA and EdDSA protocols all fall to Shor's algorithm; a post-quantum threshold scheme is a protocol change, not a parameter change.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open confidential/commitment/commitment.go:24 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [confidential/commitment/commitment.go](https://github.com/XRPLF/xrpl-go/blob/23275f007b4758e82809f51d1e4ec3c5efb2fbe0/confidential/commitment/commitment.go#L24) · line 24 · SHA-256 f54b52aa677de09d10cc1bbcc2ce76a178971c5ed99e91796c8a949c108011f1_

```
   23 | 
   24 | 	c, err := mptcrypto.PedersenCommitment(amount, bf)
   25 | 	if err != nil {
```

_file_excerpt · [confidential/deps/include/secp256k1_mpt.h](https://github.com/XRPLF/xrpl-go/blob/23275f007b4758e82809f51d1e4ec3c5efb2fbe0/confidential/deps/include/secp256k1_mpt.h#L231) · line 231 · SHA-256 d14025fc0f9047dce1e628444687577a59ac742a045f92182192614f0caf0e69_

```
  230 | int
  231 | secp256k1_mpt_pedersen_commit(
  232 |     secp256k1_context const* ctx,
```

_file_excerpt · [confidential/deps/include/utility/mpt_utility.h](https://github.com/XRPLF/xrpl-go/blob/23275f007b4758e82809f51d1e4ec3c5efb2fbe0/confidential/deps/include/utility/mpt_utility.h#L54) · line 54 · SHA-256 e92263be3776aafe4d9bcfe1246553afc691e09d4dfcd504c1478e903b5b903a_

```
   53 | {
   54 |     uint8_t pedersen_commitment[kMPT_PEDERSEN_COMMIT_SIZE];
   55 |     uint64_t amount;
```

_file_excerpt · [confidential/deps/include/utility/mpt_utility.h](https://github.com/XRPLF/xrpl-go/blob/23275f007b4758e82809f51d1e4ec3c5efb2fbe0/confidential/deps/include/utility/mpt_utility.h#L225) · line 225 · SHA-256 ee42899e04fd6668b6a7f270ecc73cd9b6b72c34ee1f8a26a9c452bf418793d1_

```
  224 | int
  225 | mpt_get_pedersen_commitment(
  226 |     uint64_t amount,
```

_file_excerpt · [confidential/mptcrypto/mptcrypto_cgo.go](https://github.com/XRPLF/xrpl-go/blob/23275f007b4758e82809f51d1e4ec3c5efb2fbe0/confidential/mptcrypto/mptcrypto_cgo.go#L59) · line 59 · SHA-256 41b2df3db91254f1d9f7dfc7c77d83ec9b9fa33229dc01e96593d423c277137c_

```
   58 | 	for i, b := range p.Commitment {
   59 | 		c.pedersen_commitment[i] = C.uint8_t(b)
   60 | 	}
```

_file_excerpt · [confidential/mptcrypto/mptcrypto_cgo.go](https://github.com/XRPLF/xrpl-go/blob/23275f007b4758e82809f51d1e4ec3c5efb2fbe0/confidential/mptcrypto/mptcrypto_cgo.go#L214) · line 214 · SHA-256 86d1d864c9d1e9f6dee855cc31509f3d89ce57041d2de2001db2d89011ee1d5f_

```
  213 | // PedersenCommitment computes a Pedersen commitment for the given amount and blinding factor.
  214 | func PedersenCommitment(amount uint64, bf BlindingFactor) (commitment Commitment, err error) {
  215 | 	ret := C.mpt_get_pedersen_commitment(
```

_file_excerpt · [confidential/mptcrypto/mptcrypto_cgo.go](https://github.com/XRPLF/xrpl-go/blob/23275f007b4758e82809f51d1e4ec3c5efb2fbe0/confidential/mptcrypto/mptcrypto_cgo.go#L215) · line 215 · SHA-256 fcafb6f2ef2a6d25241093b7ed53f3330b91b12c3b79bbd7a170dbbdfd667a43_

```
  214 | func PedersenCommitment(amount uint64, bf BlindingFactor) (commitment Commitment, err error) {
  215 | 	ret := C.mpt_get_pedersen_commitment(
  216 | 		C.uint64_t(amount),
```

_file_excerpt · [confidential/mptcrypto/mptcrypto_nocgo.go](https://github.com/XRPLF/xrpl-go/blob/23275f007b4758e82809f51d1e4ec3c5efb2fbe0/confidential/mptcrypto/mptcrypto_nocgo.go#L61) · line 61 · SHA-256 f04cb102f8718cea1e869bccdc919fcc19c34734b6c5c9927e6bbdf5a3db9ac8_

```
   60 | // PedersenCommitment computes a Pedersen commitment for the given amount and blinding factor.
   61 | func PedersenCommitment(amount uint64, bf BlindingFactor) (commitment Commitment, err error) {
   62 | 	return commitment, ErrCgoRequired
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Track post-quantum threshold signatures (NIST IR 8214C) and keep the protocol layer ready to swap the signature scheme; record which keys and shares must stay valid for how long.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-50279 — Quantum-vulnerable ECDSA: role not determined (6 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:ECDSA:general`
- Data source: confidential/builder/convert.go
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.20.0 · 2026-11-24 12:23 UTC
- Priority score: 31.7 / 100
- CVSS v3.1: not applicable

10 reference(s) to ECDSA across 6 file(s), e.g. confidential/builder/convert.go:20. Role, judged from paths, function names and nearby code: role not determined. The code does not show what the keys protect; review decides the priority.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open confidential/builder/convert.go:20 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [confidential/builder/convert.go](https://github.com/XRPLF/xrpl-go/blob/23275f007b4758e82809f51d1e4ec3c5efb2fbe0/confidential/builder/convert.go#L20) · line 20 · SHA-256 4327d096246962d2ec77bd842717af72f6af534475025f6195ac5a8992df20fa_

```
   19 | 	Amount        uint64
   20 | 	HolderPrivKey string // Non-zero secp256k1 scalar below the curve order. Required only for first-time key registration.
   21 | 	HolderPubKey  string // Valid 33-byte compressed secp256k1 point
```

_file_excerpt · [confidential/builder/convert.go](https://github.com/XRPLF/xrpl-go/blob/23275f007b4758e82809f51d1e4ec3c5efb2fbe0/confidential/builder/convert.go#L21) · line 21 · SHA-256 057dbfdb49eea5eab58ded98e71fbbff7eb4bad06fcc438f99ca3f7b5210d9ab_

```
   20 | 	HolderPrivKey string // Non-zero secp256k1 scalar below the curve order. Required only for first-time key registration.
   21 | 	HolderPubKey  string // Valid 33-byte compressed secp256k1 point
   22 | }
```

_file_excerpt · [confidential/builder/convert_back.go](https://github.com/XRPLF/xrpl-go/blob/23275f007b4758e82809f51d1e4ec3c5efb2fbe0/confidential/builder/convert_back.go#L22) · line 22 · SHA-256 763b867dda0f548f8d48ebd7ea815df931fae241d62ad810b4e0456859295088_

```
   21 | 	Amount        uint64
   22 | 	HolderPrivKey string              // Non-zero secp256k1 scalar below the curve order, also used to decrypt balance from ledger
   23 | 	HolderPubKey  string              // Valid 33-byte compressed secp256k1 point
```

_file_excerpt · [confidential/builder/convert_back.go](https://github.com/XRPLF/xrpl-go/blob/23275f007b4758e82809f51d1e4ec3c5efb2fbe0/confidential/builder/convert_back.go#L23) · line 23 · SHA-256 fafd6ede0bcea7794b4768f4a1a7154f46db85ae14aeebf3068eaa71d404c555_

```
   22 | 	HolderPrivKey string              // Non-zero secp256k1 scalar below the curve order, also used to decrypt balance from ledger
   23 | 	HolderPubKey  string              // Valid 33-byte compressed secp256k1 point
   24 | 	BalanceRange  elgamal.AmountRange // Inclusive balance decryption bounds
```

_file_excerpt · [confidential/builder/keys.go](https://github.com/XRPLF/xrpl-go/blob/23275f007b4758e82809f51d1e4ec3c5efb2fbe0/confidential/builder/keys.go#L8) · line 8 · SHA-256 f7469875cd46ee1c0a9129acdd1f199f5e53aca84e9295d66bd96551cf3a86c1_

```
    7 | 	"github.com/Peersyst/xrpl-go/pkg/mptsizes"
    8 | 	"github.com/decred/dcrd/dcrec/secp256k1/v4"
    9 | )
```

_file_excerpt · [confidential/builder/keys.go](https://github.com/XRPLF/xrpl-go/blob/23275f007b4758e82809f51d1e4ec3c5efb2fbe0/confidential/builder/keys.go#L26) · line 26 · SHA-256 6b38f9681931df7a49ce8940b2d9edf7b91a04311c968890d2eae11fd92c769b_

```
   25 | 	}
   26 | 	var scalar secp256k1.ModNScalar
   27 | 	return !scalar.SetByteSlice(keyBytes) && !scalar.IsZero()
```

_file_excerpt · [confidential/builder/send.go](https://github.com/XRPLF/xrpl-go/blob/23275f007b4758e82809f51d1e4ec3c5efb2fbe0/confidential/builder/send.go#L25) · line 25 · SHA-256 192eba53ce061226401ceb955c7b1c7d11b34a768dc57d087184bb5c79697e65_

```
   24 | 	Amount         uint64
   25 | 	SenderPrivKey  string              // Non-zero secp256k1 scalar below the curve order, also used to decrypt balance from ledger
   26 | 	SenderPubKey   string              // Valid 33-byte compressed secp256k1 point
```

_file_excerpt · [confidential/builder/send.go](https://github.com/XRPLF/xrpl-go/blob/23275f007b4758e82809f51d1e4ec3c5efb2fbe0/confidential/builder/send.go#L26) · line 26 · SHA-256 0c6920ef40759f88afcd8030d4835436fea4babe0157fc21543258cafc47b1d6_

```
   25 | 	SenderPrivKey  string              // Non-zero secp256k1 scalar below the curve order, also used to decrypt balance from ledger
   26 | 	SenderPubKey   string              // Valid 33-byte compressed secp256k1 point
   27 | 	BalanceRange   elgamal.AmountRange // Inclusive balance decryption bounds
```

_file_excerpt · [confidential/deps/include/bsgs_dlp.h](https://github.com/XRPLF/xrpl-go/blob/23275f007b4758e82809f51d1e4ec3c5efb2fbe0/confidential/deps/include/bsgs_dlp.h#L4) · line 4 · SHA-256 6ae49dbad550ee9170b9a1c84d53854a668eb7a6abb2a367131b21923186705a_

```
    3 | 
    4 | #include <secp256k1.h>
    5 | #include <stddef.h>
```

_file_excerpt · [confidential/deps/include/utility/mpt_utility.h](https://github.com/XRPLF/xrpl-go/blob/23275f007b4758e82809f51d1e4ec3c5efb2fbe0/confidential/deps/include/utility/mpt_utility.h#L5) · line 5 · SHA-256 308d3e70f8eba79c098cdc39235abd5d05a95f5718c61c02060e9faf7543c0cb_

```
    4 | #include <mpt_protocol.h>
    5 | #include <secp256k1.h>
    6 | #include <secp256k1_mpt.h>
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it; introduce an abstraction layer for crypto-agility.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-50283 — Quantum-vulnerable Ed25519: role not determined (1 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:Ed25519:general`
- Data source: pkg/crypto/ed25519.go
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.20.0 · 2026-11-24 12:23 UTC
- Priority score: 31.7 / 100
- CVSS v3.1: not applicable

8 reference(s) to Ed25519 across 1 file(s), e.g. pkg/crypto/ed25519.go:18. Role, judged from paths, function names and nearby code: role not determined. The code does not show what the keys protect; review decides the priority.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open pkg/crypto/ed25519.go:18 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [pkg/crypto/ed25519.go](https://github.com/XRPLF/xrpl-go/blob/23275f007b4758e82809f51d1e4ec3c5efb2fbe0/pkg/crypto/ed25519.go#L18) · line 18 · SHA-256 1f98d51e99284557ce33e668ccbb78a2c5126713035edb189b1e08aedba3e65e_

```
   17 | 	// XRPL Ed25519 keys are encoded as the ED prefix byte followed by the seed or public key bytes.
   18 | 	ed25519PrivateKeyLength = 1 + ed25519.SeedSize
   19 | 	ed25519PublicKeyLength  = 1 + ed25519.PublicKeySize
```

_file_excerpt · [pkg/crypto/ed25519.go](https://github.com/XRPLF/xrpl-go/blob/23275f007b4758e82809f51d1e4ec3c5efb2fbe0/pkg/crypto/ed25519.go#L19) · line 19 · SHA-256 1e20780bccfd9e56e122ead5198350c3e8972a0148ae91dfd22dfec2728cea20_

```
   18 | 	ed25519PrivateKeyLength = 1 + ed25519.SeedSize
   19 | 	ed25519PublicKeyLength  = 1 + ed25519.PublicKeySize
   20 | )
```

_file_excerpt · [pkg/crypto/ed25519.go](https://github.com/XRPLF/xrpl-go/blob/23275f007b4758e82809f51d1e4ec3c5efb2fbe0/pkg/crypto/ed25519.go#L55) · line 55 · SHA-256 ae1e34e2a4abe47d123d054b41d6744d0c24145bacf08217410ef4a21a242d09_

```
   54 | 	rawPriv := Sha512Half(decodedSeed)
   55 | 	pubKey, privKey, err := ed25519.GenerateKey(bytes.NewBuffer(rawPriv))
   56 | 	if err != nil {
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it; introduce an abstraction layer for crypto-agility.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-50286 — github.com/gorilla/websocket v1.5.3 is affected by GO-2026-6278 (no severity rating)

- Severity: **Low** · Classification: Known vulnerable component · Confidence: High · _preliminary — requires further verification_
- Affected asset: `dependency:Go/github.com/gorilla/websocket@v1.5.3`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.20.0 · 2026-11-24 12:23 UTC
- Priority score: 30.6 / 100
- CVSS v3.1: not applicable

OSV.dev reports GO-2026-6278 for Go package github.com/gorilla/websocket at version v1.5.3: Gorilla WebSocket Uses Cryptographically Weak PRNG for WebSocket Mask Key in github.com/gorilla/websocket. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. govulncheck traced a call from the product code to the affected code: github.com/Peersyst/xrpl-go/xrpl/websocket.Connection.Connect → … → github.com/gorilla/websocket.Dialer.DialContext.

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-6278
```

**Evidence.**

_tool_output · [OSV.dev GO-2026-6278](https://osv.dev/vulnerability/GO-2026-6278) · line 16 · SHA-256 b256e646804db265695055ae8cfbaf2aff7c9b104af4ea0fce0ccd6cb16153e7_

```
{"id": "GO-2026-6278", "aliases": ["GHSA-w67g-5rqw-f597"], "modified": "2026-11-23T20:30:10.450913632Z", "summary": "Gorilla WebSocket Uses Cryptographically Weak PRNG for WebSocket Mask Key in github.com/gorilla/websocket", "severity": null, "declared_in_manifest": true}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability was decided by govulncheck@v1.9.0 with the Go vulnerability database of 2026-11-23: a call graph from the product's packages (tests, examples and benchmarks left out) through every dependency to the affected functions. Calls through reflection, unsafe pointers or assembly are not followed.

**Recommendation.** Triage the advisory; upgrade to a fixed version (1.5.1, 1.5.4-0.20240701034025-d67f41855da4) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-50281 — Quantum-vulnerable EC-ElGamal: key wrapping and data encryption at rest (4 file(s))

- Severity: **Low** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:EC-ElGamal:key_wrapping`
- Data source: confidential/deps/include/bsgs_dlp.h
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.20.0 · 2026-11-24 12:23 UTC
- Priority score: 27.9 / 100
- CVSS v3.1: not applicable

42 reference(s) to EC-ElGamal across 4 file(s), e.g. confidential/deps/include/bsgs_dlp.h:103. Role, judged from paths, function names and nearby code: key wrapping and data encryption at rest. Keys or data encrypted to these public keys are stored: anyone who copies them now decrypts them once a CRQC exists (harvest now, decrypt later).

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open confidential/deps/include/bsgs_dlp.h:103 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [confidential/deps/include/bsgs_dlp.h](https://github.com/XRPLF/xrpl-go/blob/23275f007b4758e82809f51d1e4ec3c5efb2fbe0/confidential/deps/include/bsgs_dlp.h#L103) · line 103 · SHA-256 76da87080a7a52d874491def066eff308f11dcede2e03e79eb8fbd19e1534b84_

```
  102 | /** Opaque BSGS context. Allocated by secp256k1_elgamal_bsgs_ctx_create(). */
  103 | typedef struct secp256k1_elgamal_bsgs_ctx secp256k1_elgamal_bsgs_ctx;
  104 | 
```

_file_excerpt · [confidential/deps/include/bsgs_dlp.h](https://github.com/XRPLF/xrpl-go/blob/23275f007b4758e82809f51d1e4ec3c5efb2fbe0/confidential/deps/include/bsgs_dlp.h#L126) · line 126 · SHA-256 d3c705268bbc4df51139a5150c7960186a8330f67551a950b0217e0921706918_

```
  125 |  */
  126 | secp256k1_elgamal_bsgs_ctx*
  127 | secp256k1_elgamal_bsgs_ctx_create(
```

_file_excerpt · [confidential/deps/include/bsgs_dlp.h](https://github.com/XRPLF/xrpl-go/blob/23275f007b4758e82809f51d1e4ec3c5efb2fbe0/confidential/deps/include/bsgs_dlp.h#L127) · line 127 · SHA-256 42ef5c453a6078b884e511b06ab95d12f10c85f95c816c329fcfe4208a129e2f_

```
  126 | secp256k1_elgamal_bsgs_ctx*
  127 | secp256k1_elgamal_bsgs_ctx_create(
  128 |     secp256k1_context const* ctx,
```

_file_excerpt · [confidential/deps/include/secp256k1_mpt.h](https://github.com/XRPLF/xrpl-go/blob/23275f007b4758e82809f51d1e4ec3c5efb2fbe0/confidential/deps/include/secp256k1_mpt.h#L16) · line 16 · SHA-256 2fe0678af4d255c60ea8a39b55985920c55d42ba3f09a6a4eb9f1088aa6016e5_

```
   15 | SECP256K1_API int
   16 | secp256k1_elgamal_generate_keypair(
   17 |     secp256k1_context const* ctx,
```

_file_excerpt · [confidential/deps/include/secp256k1_mpt.h](https://github.com/XRPLF/xrpl-go/blob/23275f007b4758e82809f51d1e4ec3c5efb2fbe0/confidential/deps/include/secp256k1_mpt.h#L25) · line 25 · SHA-256 63dcf3257792647745aa579ef40515991d9fda1c6563bd0852fcdcc8a02aa26d_

```
   24 | SECP256K1_API int
   25 | secp256k1_elgamal_encrypt(
   26 |     secp256k1_context const* ctx,
```

_file_excerpt · [confidential/deps/include/secp256k1_mpt.h](https://github.com/XRPLF/xrpl-go/blob/23275f007b4758e82809f51d1e4ec3c5efb2fbe0/confidential/deps/include/secp256k1_mpt.h#L81) · line 81 · SHA-256 7e99b4824505c236da1bb6cec3edf4058e961a306631ff354a1c6d17eed1e46c_

```
   80 | SECP256K1_API int
   81 | secp256k1_elgamal_decrypt(
   82 |     secp256k1_context const* ctx,
```

_file_excerpt · [confidential/deps/include/utility/mpt_utility.h](https://github.com/XRPLF/xrpl-go/blob/23275f007b4758e82809f51d1e4ec3c5efb2fbe0/confidential/deps/include/utility/mpt_utility.h#L6) · line 6 · SHA-256 31b23b8e25347065ae1b0df04ac9a810f029339be06924c2abbb02726460beba_

```
    5 | #include <secp256k1.h>
    6 | #include <secp256k1_mpt.h>
    7 | #include <stdbool.h>
```

_file_excerpt · [confidential/deps/include/utility/mpt_utility.h](https://github.com/XRPLF/xrpl-go/blob/23275f007b4758e82809f51d1e4ec3c5efb2fbe0/confidential/deps/include/utility/mpt_utility.h#L122) · line 122 · SHA-256 9740eecce46c517029e0cbc8e163fb4345b73e8798085af4ee7e0b5c422e70a5_

```
  121 | bool
  122 | mpt_make_ec_pair(
  123 |     uint8_t const buffer[kMPT_ELGAMAL_TOTAL_SIZE],
```

_file_excerpt · [confidential/deps/include/utility/mpt_utility.h](https://github.com/XRPLF/xrpl-go/blob/23275f007b4758e82809f51d1e4ec3c5efb2fbe0/confidential/deps/include/utility/mpt_utility.h#L135) · line 135 · SHA-256 3cebed8006bfaa4e2c2bad9e0b48e524a8dcb6e5fbb6524b17355a626adeced1_

```
  134 | bool
  135 | mpt_serialize_ec_pair(
  136 |     secp256k1_pubkey const* in1,
```

_file_excerpt · [confidential/mptcrypto/mptcrypto_cgo.go](https://github.com/XRPLF/xrpl-go/blob/23275f007b4758e82809f51d1e4ec3c5efb2fbe0/confidential/mptcrypto/mptcrypto_cgo.go#L78) · line 78 · SHA-256 afd1056df0dcc4f3c718ab16201b5fcd9219fd28cff5d3cb9d74f9d3e567743d_

```
   77 | func GenerateKeypair() (privkey PrivateKey, pubkey PublicKey, err error) {
   78 | 	ret := C.mpt_generate_keypair(
   79 | 		uint8Ptr(&privkey[0]),
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Wrap keys with ML-KEM or a hybrid KEM (X25519 + ML-KEM-768) and re-wrap the stored keys; data that may already have been copied needs its own assessment.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-50284 — Quantum-vulnerable ElGamal: key wrapping and data encryption at rest (1 file(s))

- Severity: **Low** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:ElGamal:key_wrapping`
- Data source: xrpl/transaction/errors.go
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.20.0 · 2026-11-24 12:23 UTC
- Priority score: 27.9 / 100
- CVSS v3.1: not applicable

3 reference(s) to ElGamal across 1 file(s), e.g. xrpl/transaction/errors.go:727. Role, judged from paths, function names and nearby code: key wrapping and data encryption at rest. Keys or data encrypted to these public keys are stored: anyone who copies them now decrypts them once a CRQC exists (harvest now, decrypt later).

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open xrpl/transaction/errors.go:727 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [xrpl/transaction/errors.go](https://github.com/XRPLF/xrpl-go/blob/23275f007b4758e82809f51d1e4ec3c5efb2fbe0/xrpl/transaction/errors.go#L727) · line 727 · SHA-256 d8796bbecee0d907e89217418caa2f0289d32a2ad154ec25dbfa39dddecc66b3_

```
  726 | 	// ErrConfidentialConvertInvalidCiphertext is returned when a convert ciphertext is not valid.
  727 | 	ErrConfidentialConvertInvalidCiphertext = errors.New("confidential MPT convert: encrypted amounts must be valid 66-byte ElGamal ciphertexts with two compressed secp256k1 points")
  728 | 	// ErrConfidentialConvertBackInvalidAmount is returned when MPTAmount is outside the valid non-zero protocol range.
```

_file_excerpt · [xrpl/transaction/errors.go](https://github.com/XRPLF/xrpl-go/blob/23275f007b4758e82809f51d1e4ec3c5efb2fbe0/xrpl/transaction/errors.go#L733) · line 733 · SHA-256 aa65dea9e38c8802f20c03ee283d0d380ee87a99689f83d5b89348a199a0c47e_

```
  732 | 	// ErrConfidentialConvertBackInvalidCiphertext is returned when a ciphertext field is not valid on a convert back.
  733 | 	ErrConfidentialConvertBackInvalidCiphertext = errors.New("confidential MPT convert back: encrypted amounts must be valid 66-byte ElGamal ciphertexts with two compressed secp256k1 points")
  734 | 	// ErrConfidentialConvertBackInvalidCommitment is returned when BalanceCommitment is not valid on a convert back.
```

_file_excerpt · [xrpl/transaction/errors.go](https://github.com/XRPLF/xrpl-go/blob/23275f007b4758e82809f51d1e4ec3c5efb2fbe0/xrpl/transaction/errors.go#L746) · line 746 · SHA-256 986b375ed7a8a5ceed5edceb2605cc9e8bdde2aaf5f8e5144505598497c003e9_

```
  745 | 	// ErrConfidentialSendInvalidCiphertext is returned when a send ciphertext is not valid.
  746 | 	ErrConfidentialSendInvalidCiphertext = errors.New("confidential MPT send: encrypted amounts must be valid 66-byte ElGamal ciphertexts with two compressed secp256k1 points")
  747 | 	// ErrConfidentialSendInvalidCommitment is returned when a send commitment is not valid.
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Wrap keys with ML-KEM or a hybrid KEM (X25519 + ML-KEM-768) and re-wrap the stored keys; data that may already have been copied needs its own assessment.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-50282 — Quantum-vulnerable EC-ElGamal: role not determined (1 file(s))

- Severity: **Low** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:EC-ElGamal:general`
- Data source: confidential/mptcrypto/sizes_cgo.go
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.20.0 · 2026-11-24 12:23 UTC
- Priority score: 25.2 / 100
- CVSS v3.1: not applicable

1 reference(s) to EC-ElGamal across 1 file(s), e.g. confidential/mptcrypto/sizes_cgo.go:6. Role, judged from paths, function names and nearby code: role not determined. The code does not show what the keys protect; review decides the priority.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open confidential/mptcrypto/sizes_cgo.go:6 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [confidential/mptcrypto/sizes_cgo.go](https://github.com/XRPLF/xrpl-go/blob/23275f007b4758e82809f51d1e4ec3c5efb2fbe0/confidential/mptcrypto/sizes_cgo.go#L6) · line 6 · SHA-256 fefef0cb743ce6f93572f57ad9e759f21e40c32b91cbd8f4e2346288f9a9b0da_

```
    5 | /*
    6 | #include <secp256k1_mpt.h>
    7 | */
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Classify each usage, record data lifetimes, and plan migration to NIST's post-quantum standards cover key encapsulation and signatures; none covers additively homomorphic encryption. Treat amounts encrypted this way as eventually public, and limit what a design must store on-ledger; lattice-based homomorphic schemes are the research direction; introduce an abstraction layer for crypto-agility.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-50287 — golang.org/x/crypto v0.56.0 is affected by GO-2026-5932 (no severity rating)

- Severity: **Info** · Classification: Known vulnerable component · Confidence: Low · _preliminary — requires further verification_
- Affected asset: `dependency:Go/golang.org/x/crypto@v0.56.0`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch API lookup of the exact declared version.
- Analyzer: dependencies 1.20.0 · 2026-11-24 12:23 UTC
- Priority score: 15.3 / 100
- CVSS v3.1: not applicable

OSV.dev reports GO-2026-5932 for Go package golang.org/x/crypto at version v0.56.0: The golang.org/x/crypto/openpgp package is unmaintained, unsafe by design, and has known security issues. The advisory carries neither a CVSS vector nor a database severity, so QSI rates it low and preliminary until it is triaged. The product's build includes golang.org/x/crypto, but govulncheck found none of its affected packages imported: the advisory does not apply to the shipped code.

**Potential impact.** Unknown without triage: read the advisory and check whether the affected code is reachable in your build.

**Reproduction steps.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-5932
```

**Evidence.**

_tool_output · [OSV.dev GO-2026-5932](https://osv.dev/vulnerability/GO-2026-5932) · line 24 · SHA-256 7567598e736f75fe8f2c913606229875f197cdfc5e798ba52e2dfa3ab75088b4_

```
{"id": "GO-2026-5932", "aliases": [], "modified": "2026-11-02T22:15:06.677088389Z", "summary": "The golang.org/x/crypto/openpgp package is unmaintained, unsafe by design, and has known security issues", "severity": null, "declared_in_manifest": false}
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. The advisory has no severity rating. Reachability was decided by govulncheck@v1.9.0 with the Go vulnerability database of 2026-11-23: a call graph from the product's packages (tests, examples and benchmarks left out) through every dependency to the affected functions. Calls through reflection, unsafe pointers or assembly are not followed.

**Recommendation.** Triage the advisory; upgrade to a fixed version (0.58.1-0.20261009181718-2f1f834330b2) if it applies.

**Retest procedure.** Re-run the dependency scan after upgrading.

### QSI-2026-50288 — 1 advisories in 1 development or build-only npm package(s)

- Severity: **Info** · Classification: Improvement recommendation · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `dependencies:npm:non-runtime`
- Data source: OSV.dev
- Detection method: OSV.dev querybatch lookup of exact versions; scope from devDependencies, package-lock.json dev flags, pnpm importers sections, the Cargo.lock graph rooted at the Cargo.toml tables, and — for yarn.lock, which records no scope — the lock graph walked from package.json. Where a runtime requirement cannot be resolved in a lock, that lock is left unclassified rather than risking a package being set aside wrongly.
- Analyzer: dependencies 1.20.0 · 2026-11-24 12:23 UTC
- Priority score: 13.7 / 100
- CVSS v3.1: not applicable

OSV.dev lists 1 advisories (1 rated high or critical) for 1 npm package(s) that only development or build tooling pulls in (docs/yarn.lock): e.g. webpack-dev-middleware@7.4.5 [build]: GHSA-g84c-rxfj-3j2c. The manifests mark them as such (devDependencies, "dev": true in package-lock.json, pnpm importers sections, [dev-dependencies]/[build-dependencies] reached through Cargo.lock, or — for yarn.lock, which records no scope at all — package.json reached through the lock graph), so they are not part of what ships.

**Potential impact.** They do not reach users of the product. They can affect developer machines and CI (supply chain): a compromised or vulnerable tool can tamper with builds.

**Reproduction steps.**

```
Look the packages listed in the evidence up at https://osv.dev and check their scope in docs/yarn.lock.
```

**Evidence.**

_tool_output · [OSV.dev (npm)](https://osv.dev/) · docs/yarn.lock · SHA-256 e2bb24b4b5673e9a965d954ffa6e935cfba8b1931912b67356d5d535169f4886_

```
webpack-dev-middleware@7.4.5 [build]: GHSA-g84c-rxfj-3j2c
```

**Limitations of the check.** Advisory data comes from OSV.dev at the recorded time. Scopes come from the manifests; a registry crate's own build dependencies cannot be told apart in Cargo.lock, so the runtime set may be larger than reality, never smaller.

**Recommendation.** Update the tooling during routine maintenance; prioritise packages that run in CI with secrets or that produce release artefacts.

**Retest procedure.** Re-run the dependency scan after updating.

### QSI-2026-50285 — No post-quantum capable cryptographic library detected

- Severity: **Info** · Classification: Insufficient data · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `dependencies`
- Data source: dependency manifests
- Detection method: Dependency name matching.
- Analyzer: dependencies 1.20.0 · 2026-11-24 12:23 UTC
- Priority score: 12.2 / 100
- CVSS v3.1: not applicable

Across 4 dependency manifests, QSI found crypto libraries (@noble/hashes, github.com/Peersyst/xrpl-go, golang.org/x/crypto) but none from its PQC-capable list.

**Potential impact.** Readiness indicator only: PQC support may come from the platform (OpenSSL, OS, cloud KMS) rather than application dependencies.

**Reproduction steps.**

```
Review the dependency manifests listed in the evidence.
```

**Evidence.**

_dependency · confidential/go.mod, docs/package.json, docs/yarn.lock, go.mod · SHA-256 a42f2c23f3e4eb47a022e0667d1d02bd3ad402bcf79bc7959083602fa9ba59db_

```
Crypto libraries: @noble/hashes, github.com/Peersyst/xrpl-go, golang.org/x/crypto
```

**Limitations of the check.** Absence of evidence is not evidence of absence: system libraries and transitive dependencies may not be listed.

**Recommendation.** Confirm where PQC support will come from (TLS terminator, KMS/HSM, library upgrade).

**Retest procedure.** Re-scan after upgrades.


## 8. Post-quantum assessment

| | Key establishment (x = how long data must stay confidential; harvest now, decrypt later) | Signatures (x = how long signatures/keys must stay trusted) |
|---|---|---|
| Data/key lifetime x | 5 | 10 |
| Migration time y | 5 | 5 |
| Assumed years to CRQC z | 12 (central) | 12 |
| x + y − z | -2 → tight margin | 3 → migration would finish too late under this scenario |
#### Where z comes from

Averaged expert likelihood that a CRQC exists within each horizon, from the annual survey published by the author of this inequality. Likelihood estimates, not predictions of a date.

| Within | Likelihood | The report's wording |
|---|---|---|
| 5 years | ~15% | averaged estimate |
| 10 years | 28-49% | quite possible |
| 15 years | 51-70% | likely |

**Why this scenario (central, z = 12):** Between the 10-year band (28-49%) and the 15-year band (51-70%): roughly where the experts' averaged likelihood crosses one half. More than half of the respondents (13 of 26) already put the likelihood at 50% or more for some horizon.
_Planning assumptions: x for key establishment, x for signatures, y are the defaults of the risk profile “Web3 project”, not the client's figures; with the client's actual lifetimes the verdict can change._

### Post-quantum maturity: Level 0 of 4 — no post-quantum cryptography

- Classical only — key wrapping and data encryption at rest: EC-ElGamal, ElGamal (5 file(s))
- Classical only — threshold signing and MPC protocols: Pedersen commitment (5 file(s))

**Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

_Levels: 0 none; 1 present, not wired; 2 in use outside the critical paths; 3 hybrid in a critical path; 4 post-quantum by default in the critical paths (root of trust, key wrapping, channel key exchange). Judged from code and manifests._

### What the quantum-vulnerable algorithms do

| Role | Algorithms (files) | ID | First step |
|---|---|---|---|
| **key wrapping and data encryption at rest** | EC-ElGamal (4), ElGamal (1) | QSI-2026-50281, QSI-2026-50284 | Wrap keys with ML-KEM or a hybrid KEM (X25519 + ML-KEM-768) and re-wrap the stored keys; data that may already have been copied needs its own assessment |
| **threshold signing and MPC protocols** | Pedersen commitment (5) | QSI-2026-50280 | Track post-quantum threshold signatures (NIST IR 8214C) and keep the protocol layer ready to swap the signature scheme; record which keys and shares must stay valid for how long |
| **transaction and message signing** | ECDSA (9) | QSI-2026-50278 | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains adopt them |
| **role not determined** | ECDSA (6), EC-ElGamal (1), Ed25519 (1) | QSI-2026-50279, QSI-2026-50282, QSI-2026-50283 | Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it; introduce an abstraction layer for crypto-agility |

_Roles are judged from file paths, function names and the code around each match; review confirms them. Root-of-trust keys and wrapped keys come first: they are hard to replace or can be recorded today._
No readiness questionnaire was completed for this project.

### Quantum algorithms relevant to this inventory

| Quantum algorithm | Effect | Attack model | Inventoried algorithms (rows) | What it means for this audit |
|---|---|---|---|---|
| Shor's algorithm — discrete logarithms in finite fields | breaks | Q1 | ElGamal (2) | Breaks finite-field Diffie–Hellman and DSA at every size. Move key establishment to ML-KEM (hybrid with X25519 or ECDH during the transition) and signatures to ML-DSA or SLH-DSA. |
| Shor's algorithm — elliptic-curve discrete logarithms | breaks | Q1 | EC-ElGamal (5), ECDSA (16), Ed25519 (2), Pedersen commitment (5) | Elliptic-curve keys are expected to fall before RSA keys of comparable classical strength. On blockchains, coins whose public key is already on chain (reused addresses, pay-to-public-key and Taproot outputs) are exposed first; plan the move to post-quantum signatures and avoid key reuse in the meantime. |
| Grover's algorithm — key search and preimages | weakens (larger keys restore the margin) | Q1 | RIPEMD-160 (1), SHA-2 (4) | Not a break. 256-bit keys (AES-256, ChaCha20) keep a comfortable margin; AES-128 meets NIST category 1, while some authorities ask for 256-bit keys in quantum-resistant contexts (see the AES-128 entry). Prefer 256-bit keys for long-lived data; 256-bit hashes need no change for preimage resistance. |
| Brassard–Høyer–Tapp — collision search | weakens (larger keys restore the margin) | Q1 | RIPEMD-160 (1), SHA-2 (4) | 256-bit hashes (SHA-256, SHA3-256) remain adequate for collision resistance; 160-bit hashes are already weak classically (SHA-1 collisions are practical). Use 384/512-bit hashes where NIST categories 4–5 are required. |

_Effects: breaks — replace the algorithm; weakens — larger keys or outputs restore the margin; included in standard parameters — no action at standard parameter sets; only with superposition queries — not applicable to ordinary deployments._


## 9. Limitations and assumptions

- This report presents automated and documented analysis results for the stated scope. It is not a legal opinion, a certification or an attestation of compliance with any standard.
- z is a planning assumption chosen per risk profile, not a prediction. A cryptographically relevant quantum computer is not publicly known to exist today.

## 10. Remediation plan / Priorities for 30, 60 and 90 days

### 30 days

| Priority | ID | Action | Type | Closure criteria |
|---|---|---|---|---|
### 60 days

| Priority | ID | Action | Type | Closure criteria |
|---|---|---|---|---|
| P3 | QSI-2026-50286 | Triage GO-2026-6278; upgrade github.com/gorilla/websocket to a fixed version (1.5.1, 1.5.4-0.20240701034025-d67f41855da4) if it applies. | root-cause fix | Dependency scan no longer reports GO-2026-6278, or the triage is recorded. |
| P3 | QSI-2026-50287 | Triage GO-2026-5932; upgrade golang.org/x/crypto to a fixed version (0.58.1-0.20261009181718-2f1f834330b2) if it applies. | root-cause fix | Dependency scan no longer reports GO-2026-5932, or the triage is recorded. |
### 90 days

| Priority | ID | Action | Type | Closure criteria |
|---|---|---|---|---|
| P3 | QSI-2026-50278 | Add ECDSA usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-50280 | Add Pedersen commitment usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-50279 | Add ECDSA usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-50283 | Add Ed25519 usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-50281 | Add EC-ElGamal usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-50284 | Add ElGamal usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-50282 | Add EC-ElGamal usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P4 | QSI-2026-50278 | Plan migration of ECDSA to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-50280 | Plan migration of Pedersen commitment to  (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows  or a hybrid scheme in use. |
| P4 | QSI-2026-50279 | Plan migration of ECDSA to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-50283 | Plan migration of Ed25519 to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-50281 | Plan migration of EC-ElGamal to NIST's post-quantum standards cover key encapsulation and signatures; none covers additively homomorphic encryption. Treat amounts encrypted this way as eventually public, and limit what a design must store on-ledger; lattice-based homomorphic schemes are the research direction (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows NIST's post-quantum standards cover key encapsulation and signatures; none covers additively homomorphic encryption. Treat amounts encrypted this way as eventually public, and limit what a design must store on-ledger; lattice-based homomorphic schemes are the research direction or a hybrid scheme in use. |
| P4 | QSI-2026-50284 | Plan migration of ElGamal to Hybrid key establishment with ML-KEM (FIPS 203), e.g. X25519MLKEM768 in TLS 1.3 or mlkem768x25519-sha256 in SSH (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows Hybrid key establishment with ML-KEM (FIPS 203), e.g. X25519MLKEM768 in TLS 1.3 or mlkem768x25519-sha256 in SSH or a hybrid scheme in use. |
| P4 | QSI-2026-50282 | Plan migration of EC-ElGamal to NIST's post-quantum standards cover key encapsulation and signatures; none covers additively homomorphic encryption. Treat amounts encrypted this way as eventually public, and limit what a design must store on-ledger; lattice-based homomorphic schemes are the research direction (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows NIST's post-quantum standards cover key encapsulation and signatures; none covers additively homomorphic encryption. Treat amounts encrypted this way as eventually public, and limit what a design must store on-ledger; lattice-based homomorphic schemes are the research direction or a hybrid scheme in use. |
| P4 | QSI-2026-50288 | Update the development and build dependencies listed in the evidence. | root-cause fix | The dependency scan reports no advisories for tooling packages, or the remaining ones are recorded. |

## 11. Tools used

- blockchain 1.0.0
- certificates 1.2.0
- chain_map 1.0.0
- configs 1.1.0
- crediting 1.4.0
- dependencies 1.6.0
- hndl 1.0.0
- inventory_document 1.1.0
- key_storage 1.0.0
- mpc 1.0.0
- solidity 1.8.1
- source_code 1.11.0
- tls_code 1.1.0
- tls_live 1.0.0
- ton_contracts 1.0.0
- validator_keys 1.2.0
- wallet_login 1.0.0
- qsi-engine 1.20.0
- OSV.dev API v1

## 12. Sources and normative documents

1. A. Chailloux, M. Naya-Plasencia, A. Schrottenloher — An Efficient Quantum Collision Search Algorithm and Implications on Symmetric Cryptography (ASIACRYPT 2017; IACR ePrint 2017/847) — IACR ePrint. <https://eprint.iacr.org/2017/847> (peer-reviewed article: Õ(2^{2n/5}) time, O(n) qubits, Õ(2^{n/5}) classical memory)
2. C. Chevignard, P.-A. Fouque, A. Schrottenloher — Reducing the Number of Qubits in Quantum Discrete Logarithms on Elliptic Curves (IACR ePrint 2026/280) — IACR ePrint. <https://eprint.iacr.org/2026/280> (revision of a EUROCRYPT 2026 paper: 3.12n + o(n) qubits; for n = 256, 1193 qubits and 22 runs of 2^38.98 Toffoli gates)
3. C. Gidney, M. Ekerå — How to factor 2048 bit RSA integers in 8 hours using 20 million noisy qubits (Quantum 5, 433) — Quantum. <https://doi.org/10.22331/q-2021-04-15-433> (peer-reviewed article (2021): 10^-3 gate error, 1 µs cycle, 10 µs reaction time)
4. C. Zalka — Grover's quantum searching algorithm is optimal (Phys. Rev. A 60, 2746, 1999; arXiv:quant-ph/9711070) — APS. <https://doi.org/10.1103/PhysRevA.60.2746> (peer-reviewed article: optimal for any success probability; parallel search gains no more than splitting the space)
5. Common Vulnerability Scoring System v3.1: Specification Document — FIRST. <https://www.first.org/cvss/v3.1/specification-document> (final)
6. D. J. Bernstein — Cost analysis of hash collisions: Will quantum computers make SHARCS obsolete? (2009) — cr.yp.to. <https://cr.yp.to/hash/collisioncost-20090823.pdf> (paper dated 2009-08-23)
7. D. Litinski — How to compute a 256-bit elliptic curve private key with only 50 million Toffoli gates (arXiv:2306.08585) — arXiv. <https://arxiv.org/abs/2306.08585> (preprint (2023-06-14): 6000 modules × 1152 physical qubits, one key per 10 minutes under its architecture assumptions)
8. FIPS 203 — Module-Lattice-Based Key-Encapsulation Mechanism Standard (ML-KEM) — NIST. <https://csrc.nist.gov/pubs/fips/203/final> (final (August 2024))
9. FIPS 204 — Module-Lattice-Based Digital Signature Standard (ML-DSA) — NIST. <https://csrc.nist.gov/pubs/fips/204/final> (final (August 2024))
10. FIPS 205 — Stateless Hash-Based Digital Signature Standard (SLH-DSA) — NIST. <https://csrc.nist.gov/pubs/fips/205/final> (final (August 2024))
11. G. Brassard, P. Høyer, A. Tapp — Quantum Algorithm for the Collision Problem (LATIN '98; arXiv:quant-ph/9705002) — Springer / arXiv. <https://arxiv.org/abs/quant-ph/9705002> (peer-reviewed article: collisions of r-to-one functions in O((N/r)^{1/3}) expected evaluations)
12. J. Proos, C. Zalka — Shor's discrete logarithm quantum algorithm for elliptic curves (Quantum Inf. Comput. 3(4), 2003; arXiv:quant-ph/0301141) — Quantum Information & Computation. <https://doi.org/10.26421/QIC3.4-3> (peer-reviewed article)
13. L. K. Grover — A fast quantum mechanical algorithm for database search (STOC 1996) — ACM. <https://doi.org/10.1145/237814.237866> (peer-reviewed article)
14. M. Amy et al. — Estimating the cost of generic quantum pre-image attacks on SHA-2 and SHA-3 (SAC 2016; arXiv:1603.09383) — Springer / arXiv. <https://arxiv.org/abs/1603.09383> (peer-reviewed article: SHA-256 about 2^153.8 surface-code cycles on 2^12.6 logical qubits; SHA3-256 about 2^146.5 cycles on 2^20)
15. M. Cain et al. — Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits (arXiv:2603.28627) — arXiv. <https://arxiv.org/abs/2603.28627> (preprint (2026-03-30): P-256 in a few days with 26,000 physical neutral-atom qubits; RSA-2048 one to two orders of magnitude longer)
16. M. Ekerå, J. Gärtner — A high-level comparison of state-of-the-art quantum algorithms for breaking asymmetric cryptography (arXiv:2405.14381) — arXiv. <https://arxiv.org/abs/2405.14381> (preprint (2024-05-23): Regev-style algorithms show no overall advantage yet for cryptographic RSA and finite-field sizes)
17. M. Mosca — Cybersecurity in an Era with Quantum Computers: Will We Be Ready? (IEEE Security & Privacy, 2018) — IEEE. <https://doi.org/10.1109/MSP.2018.3761723> (peer-reviewed article; source of the x + y > z migration inequality)
18. M. Roetteler, M. Naehrig, K. Svore, K. Lauter — Quantum resource estimates for computing elliptic curve discrete logarithms (ASIACRYPT 2017) — IACR / arXiv. <https://arxiv.org/abs/1706.06752> (peer-reviewed article: at most 9n + 2⌈log2 n⌉ + 10 qubits and 448 n^3 log2 n + 4090 n^3 Toffoli gates)
19. NIST IR 8547 — Transition to Post-Quantum Cryptography Standards — NIST. <https://csrc.nist.gov/pubs/ir/8547/final> (final (2026-10-27; the initial public draft of November 2024 is obsoleted). Tables 2 and 4: ECDSA, EdDSA and RSA signatures, finite-field and elliptic-curve DH and MQV, and RSA key establishment are deprecated after 2030 and disallowed after 2035 at every key size — the draft deprecated only the 112-bit level. A composite (hybrid) key establishment stays FIPS 140-validatable while one input comes from an approved scheme. Repeats the federal deadlines of OMB M-26-15: post-quantum key establishment by 2030-12-31 and signatures by 2031-12-31 for high value assets and high impact systems)
20. NIST — Post-Quantum Cryptography Standardization: Evaluation Criteria, Security (Call for Proposals, Section 4.A.5) — NIST. <https://csrc.nist.gov/Projects/Post-Quantum-Cryptography/Post-Quantum-Cryptography-Standardization/Evaluation-Criteria/Security-(Evaluation-Criteria)> (security categories: AES-128 key search 2^170/MAXDEPTH quantum gates, AES-192 2^233/MAXDEPTH, AES-256 2^298/MAXDEPTH; MAXDEPTH 2^40–2^96)
21. OSV advisory GO-2026-5932 — OSV.dev. <https://osv.dev/vulnerability/GO-2026-5932> (modified 2026-11-02T22:15:06.677088389Z)
22. OSV advisory GO-2026-6278 — OSV.dev. <https://osv.dev/vulnerability/GO-2026-6278> (modified 2026-11-23T20:30:10.450913632Z)
23. OSV.dev — open-source vulnerability database and API — Open Source Security Foundation. <https://osv.dev/> (the database QSI queries for each exactly pinned version; every advisory id in a finding resolves at https://osv.dev/vulnerability/<id>)
24. P. W. Shor — Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms on a Quantum Computer (SIAM J. Comput., 1997) — SIAM. <https://doi.org/10.1137/S0097539795293172> (peer-reviewed article)
25. R. Babbush et al. — Securing Elliptic Curve Cryptocurrencies against Quantum Vulnerabilities: Resource Estimates and Mitigations (arXiv:2603.28846) — arXiv. <https://arxiv.org/abs/2603.28846> (preprint (2026-03-30, v2 2026-04-15): 256-bit ECDLP with < 1200 logical qubits and < 90 M Toffoli gates (or < 1450 and < 70 M); < 500,000 physical qubits at 10^-3 error, minutes)
26. S. Jaques, M. Naehrig, M. Roetteler, F. Virdia — Implementing Grover oracles for quantum key search on AES and LowMC (EUROCRYPT 2020; arXiv:1910.01700) — Springer / arXiv. <https://arxiv.org/abs/1910.01700> (peer-reviewed article: lower cost estimates for the AES key searches that define the NIST categories)

## Appendices: Cryptographic inventory

By origin: dependency manifests 4 (0 Shor-breakable) · own code 26 (21 Shor-breakable) · third-party code in the tree 9 (9 Shor-breakable).

| Algorithm | Parameter | Library | Quantum status | Classical status | Count | Locations | Examples |
|---|---|---|---|---|---|---|---|
| RIPEMD-160 | RIPEMD-160 |  | weak classically | legacy | 1 | 1 | address-codec/sha256.go:15 |
| SHA-2 | SHA-512 |  | reduced margin (Grover), approved | acceptable | 2 | 2 | pkg/crypto/secp256k1.go:5; pkg/crypto/sha512.go:3 |
| SHA-2 | SHA-256 |  | Grover: acceptable to NIST, below ECCG/ANSSI guidance | acceptable | 2 | 2 | address-codec/base58check.go:4; address-codec/sha256.go:4 |
| Crypto library | v0.56.0 | golang.org/x/crypto (Go x/crypto) | n/a | acceptable | 2 | 2 | confidential/go.mod:24; go.mod:28 |
| Crypto library | v0.3.1 | github.com/Peersyst/xrpl-go (xrpl-go) | n/a | acceptable | 1 | 1 | confidential/go.mod:6 |
| Crypto library | 1.4.0 | @noble/hashes (noble-hashes) | n/a | acceptable | 1 | 1 | docs/yarn.lock:2428 |
| EC-ElGamal |  |  | vulnerable (Shor) | acceptable | 5 | 5 | confidential/deps/include/bsgs_dlp.h:103; confidential/deps/include/secp256k1_mpt.h:16; confidential/deps/include/utility/mpt_utility.h:6 |
| ECDSA | secp256k1 |  | vulnerable (Shor) | acceptable | 14 | 14 | address-codec/codec.go:126; address-codec/errors.go:20; confidential/builder/clawback.go:48 |
| ECDSA |  |  | vulnerable (Shor) | acceptable | 2 | 2 | confidential/deps/include/secp256k1.h:74; pkg/crypto/secp256k1.go:151 |
| Ed25519 | Ed25519 |  | vulnerable (Shor) | acceptable | 2 | 2 | pkg/crypto/ed25519.go:18; pkg/crypto/ed25519.go:55 |
| ElGamal |  |  | vulnerable (Shor) | deprecated | 2 | 2 | confidential/elgamal/elgamal.go; xrpl/transaction/errors.go:727 |
| Pedersen commitment |  |  | vulnerable (Shor) | acceptable | 5 | 5 | confidential/commitment/commitment.go:24; confidential/deps/include/secp256k1_mpt.h:231; confidential/deps/include/utility/mpt_utility.h:54 |

_Long lists are grouped here; the full per-file list is in the JSON report, signed with the same key._

## Appendices: Input files

| File | Size | SHA-256 | Redactions |
|---|---|---|---|
| .agents/skills/xrpl-standards/scripts/extract-spec.py | 10162 | `89b3484d2818fd0d6fcd00097a1b16276a5985c8cc2a66d10b4f3ab21ec8d735` | 0 |
| .agents/skills/xrpl-standards/scripts/sync-xls-standards.py | 10999 | `26d5648d3df84755b8d93b8c7967dd63b4d1f6eb254f6ec60a0151959ab44a0c` | 0 |
| address-codec/address.go | 3068 | `ca0ccb1b013c272f25da07e573d4110df9c92463784fb45288d3bba0cb503770` | 0 |
| address-codec/alphabet.go | 1838 | `7f2fab355c421b74ccaf1d396a0f0c7de89ec791c647df0c65f0c965171c7177` | 0 |
| address-codec/alphabet_gen.go | 1431 | `5316f0ef166ab5aa1494b566a0fab6cb87b19517b48d07a651c0cb96d732c201` | 0 |
| address-codec/base58.go | 3335 | `de807e1cddd02c86f138f79c960e5140f2fe7f7c4c87e797899a700e583bdfac` | 0 |
| address-codec/base58check.go | 2230 | `7a7775bd02159d13dfc23e62176e44f495da00d328c8323d676f703813ef2211` | 0 |
| address-codec/codec.go | 7210 | `b643c629721c48ad7413759441b96fdff8310b0cf4b20ac354bf7782d1bead29` | 0 |
| address-codec/errors.go | 2513 | `2b300f6a738ff7b033f2dd29dd4fdc66255778100bb23fcca9d0de2d0c295fda` | 0 |
| address-codec/interfaces/crypto.go | 363 | `b3d18cf79107f105e419fc732927aff1f96ea9249726a20ee7c30e3b6e9304f1` | 0 |
| address-codec/sha256.go | 439 | `c8660008f6f07216ca98d538eb82d5d68e4dd1194492118401b19866ec514749` | 0 |
| address-codec/x_codec.go | 4598 | `ce6f5ad701de6d6096aba4a7890a6266ee0b432445fc73b2befecf6a15f57d40` | 0 |
| binary-codec/codec.go | 9438 | `a35fb1f306db8c6ffc31534aba5d6783d5eb84379a3ea3b18b4e3a8064b75778` | 0 |
| binary-codec/definitions/definitions.go | 4304 | `50893c59fd59afe71e1d445f7b903d9499718c071c6d538397673bfbe1e9f1ef` | 0 |
| binary-codec/definitions/errors.go | 1115 | `5108bc933e7b1717136dd472bac79f4b377f73ad6316e33ddb83b8c21d0fefb5` | 0 |
| binary-codec/definitions/field_instance.go | 1105 | `6a56120d4ae574f1ece5d8d9b7ca06d572a8212dc71609aaf3bf1d28ccf08730` | 0 |
| binary-codec/definitions/helpers.go | 5786 | `04e72ede01dce1080038c39af948b6daea4ecb554b8b583ad78c10e106b5d022` | 0 |
| binary-codec/definitions/init.go | 56 | `a010e71453c300515df92e4af2d38a7c20d537de364b7893436c542ecd0c96a9` | 0 |
| binary-codec/errors.go | 1916 | `d3dbefc3a995858687c4671ba9a3cded130c17c0e08c6b5080ba44a39d54186b` | 0 |
| binary-codec/ledger_data.go | 2371 | `5815f91d399245760989c136ade3d01504b15a9902b1bb3951c53fbd78602be8` | 0 |
| binary-codec/quality.go | 3816 | `3351e131871a197abb673780fdcbeb6171cb9caa421bf8862b78889c38afcc11` | 0 |
| binary-codec/serdes/binary_parser.go | 4318 | `3fe3c2c62eee0d22dd4b79e53d8ac644b58fe7bdc8e92875205df79c09f243d6` | 0 |
| binary-codec/serdes/binary_serializer.go | 2012 | `18333b091ed5d8f60e16d597451a852f39c72f01e1479b69ac89f0dc91e5eb3b` | 0 |
| binary-codec/serdes/field_id_codec.go | 2570 | `4b349f2b4829c6a1627f4e9f5195ad741c76d60c1d902515fd764790852025b6` | 0 |
| binary-codec/serdes/interfaces/definitions.go | 646 | `a2cee2a45b378dfcef6a8cac20d29f7b125e67914d38fc043f2e5e866d8cb8dd` | 0 |
| binary-codec/serdes/interfaces/field_id_codec.go | 225 | `27a46e4b7f7007dca1cc41e47b9babbca8718eb91faff2723c994c2b12fc4693` | 0 |
| binary-codec/types/account_id.go | 2373 | `a7549a2d6428a24b8ae6be2db27d19a22ff9a2cf8b2fc4e81dfb602030c438e4` | 0 |
| binary-codec/types/amount.go | 22953 | `1c73cd1a7caf3aaf82536928aa0210c73395565f6a05556d378eecdc7615ac17` | 0 |
| binary-codec/types/blob.go | 1496 | `6c35fde7f8e9af6e7aa02f01ede3ee1007f14cdc79b76a02b3cf28b116abcf08` | 0 |
| binary-codec/types/currency.go | 2167 | `63b515b33e7bd3366bb3a4d92c7431303e021eba1f02d6db4c6d5c8f029c611e` | 0 |
| binary-codec/types/errors.go | 2558 | `1a89ce1193440a31f48356adbb1b086f0a9367acedcc2b022d2829d820e68c11` | 0 |
| binary-codec/types/hash.go | 2461 | `e88f350792cf7916e73ecbb092c3098f0b6773fb363178022e241be5c2dc41ef` | 0 |
| binary-codec/types/hash128.go | 251 | `69da5ac258b3c1f7fda99e32be2d982080052e3dc2b02f9030b78e67d826004c` | 0 |
| binary-codec/types/hash160.go | 251 | `a2bfb5ca332a40c4e9d4c0fa53a642fc5d42e495ed95763b2759f689838fe340` | 0 |
| binary-codec/types/hash192.go | 320 | `deb2ffcc191af6e05a9576712e4d6e0ecbbd46e811e1916dcd33dcd74e17144b` | 0 |
| binary-codec/types/hash256.go | 323 | `8f898ad50ba1981ee62f391b533ed74e1b5020a96e9faa70c93a801b835436df` | 0 |
| binary-codec/types/int32.go | 3685 | `0cc079b05cf553969fd77fe6817d4a1c49f5ba1234ae5df90543a6e90315ec13` | 0 |
| binary-codec/types/interfaces/binary_parser.go | 500 | `cbbb5e1f8f870865693029138dd170abd3862cc445730e3f49363a44f8c8b2ba` | 0 |
| binary-codec/types/interfaces/binary_serializer.go | 439 | `ed3d7a1b615b0cd6f9dfc711e8bd6b0065f71b4efee64db05f1707c39889e74d` | 0 |
| binary-codec/types/iou_value.go | 4899 | `f0c2c3e7c29cbc9b6ac241d0e2629659a396c96fafbd21b1050b3e2a54b6bf18` | 0 |
| binary-codec/types/issue.go | 7098 | `c893a4fa31a7570cd5a20e4879e51549814033dcc160a1687966ebcd9797b4fd` | 0 |
| binary-codec/types/pathset.go | 8105 | `a70e88713ff770549445f764880e12af7fc28892525500337644a54157b0b198` | 0 |
| binary-codec/types/permission_value.go | 2311 | `5de9d776a144e2c83e6058cea4a0423177b4759b5e439e5b9e8b8f874faaee30` | 0 |
| binary-codec/types/serialized_type.go | 1902 | `099e41c1f272c7809259ec250ed3f06ae6534723261b83c364c8072be4376af6` | 0 |
| binary-codec/types/st_array.go | 2592 | `0fc832f80710a03a3d320f606f818e48e69f6ab547ca2cfa0cd21637fd611b22` | 0 |
| binary-codec/types/st_number.go | 8777 | `826df6f93f2f28a8781f80ca31e4c5dd337b867568c61f74b0a30daca4ac2c36` | 0 |
| binary-codec/types/st_object.go | 9881 | `b255109d550fd801bfb5995c4cd1741cdc9d4f3d45d61c1de2f6887f06689961` | 0 |
| binary-codec/types/uint16.go | 2487 | `a8e7d037d4399bf0ae9187c4af3b5cd3d5c369abe9364bb0bbc779fde28bb9b4` | 0 |
| binary-codec/types/uint32.go | 1186 | `fbb4542b6bbb2adc76cb3cc7d66149cbb8329a04c513d357d0b0552d9ba90072` | 0 |
| binary-codec/types/uint64.go | 2794 | `601cc5e04d1bf85c5e443b6779388dab992ce9c7a06c0ccc1cb099b54e248eb5` | 0 |
| binary-codec/types/uint8.go | 2225 | `5956fd31907c2730f86ef01dcefb84fd790cf8033e7aa6e9870a5aba384b35f1` | 0 |
| binary-codec/types/vector256.go | 3085 | `a993f1de44c5943bd3e9e53e3d968910929f3c43fe0886670744edee9391cf29` | 0 |
| binary-codec/types/xchain_bridge.go | 3289 | `8818dfa539fad069f3047cf4e0902151c0a21ca741836b85a5af2613b7b6839e` | 0 |
| confidential/builder/balance.go | 3695 | `7ff53c66697ff844d28297e0bae4c3f08f774e4a3533ba4038b06b3a588992ef` | 0 |
| confidential/builder/batch.go | 17391 | `07175342d42df0f8b2ab1bd8e3a770b5ba0f9dc032c453fb614ebdb8d8aaa675` | 0 |
| confidential/builder/batch_operations.go | 13733 | `df51dfcb2f1e74c2dd90a506584c47128a6d4d739e346dd9e28a550d2f4f72a2` | 0 |
| confidential/builder/batch_state.go | 11271 | `a1f61ca327a6995287837023de51500ef6c08278435d73fa9c5db82e1cc2b456` | 0 |
| confidential/builder/clawback.go | 7624 | `5ca708dce64db266364208111cc3c7b48bfa1fb7cd4e5889ed9e552f0a15e3d0` | 0 |
| confidential/builder/convert.go | 6557 | `921ce76e2cfb9ef029cf50ade88d7f1cde14a761018f7b6670e1040bf7245708` | 0 |
| confidential/builder/convert_back.go | 7600 | `bba1381f25a1ea74cc6be9844d36174c9d8bc66d9938349fdeb339ff2f95e837` | 0 |
| confidential/builder/errors.go | 6033 | `77dce0e6141ffc343940a1ae6350298ff62c3bf5bb72fb9a191bce89359d22f4` | 0 |
| confidential/builder/keys.go | 1228 | `990263992b3448b01973887545df1e944210f5d8c92606257e38391bf3ce3db9` | 0 |
| confidential/builder/ledgerfields.go | 2423 | `6b566aac9bd6dd2588811975ed50d472e2939b2c152d83d1932baa7c53a58c6d` | 0 |
| confidential/builder/merge_inbox.go | 2894 | `d8706e95739afe057fbbefa70de52aa6bf716b93ec6287337ca5aaed952496e6` | 0 |
| confidential/builder/preflight.go | 18151 | `7dfb1143401eaa94ffc4054460e0f46b9fdfd3ccf08ea772fd73b4ab6f97087c` | 0 |
| confidential/builder/querier.go | 11227 | `73ce257dca21e271dd7ca5256f77699eba355d374aa22d878e3e65c67456134a` | 0 |
| confidential/builder/send.go | 9556 | `fe2b61ce2f63a5271c7dfffd6213b9f1c1d789e04d0dd19e481f5a281837803e` | 0 |
| confidential/builder/tx_options.go | 5719 | `bc1fad501f715669743dc3178d2d0475a8914326a3572bf207acd031837a9928` | 0 |
| confidential/builder/validation.go | 3988 | `17abb823eff20d8e01b954450e23a47730360d1d4b9c8ac06d6746231d759348` | 0 |
| confidential/commitment/commitment.go | 965 | `7252d21d8260865315f72acd461d0a5242052e0926cea49b2f7da011f9ac39be` | 0 |
| confidential/commitment/errors.go | 394 | `3de5a3d2532a3a3e0e16d9e3bba6472751311ea2f685aa87dc30a08ffdab3a3b` | 0 |
| confidential/deps/include/bsgs_dlp.h | 7739 | `99308b5a6685a4d7dc919e23b29752d476a422784ffa44f2bea3a1f9cf1dfad3` | 0 |
| confidential/deps/include/mpt_protocol.h | 1300 | `341b4dd4c9ac01d45bcbce7d5de4c9354773eb83ee5caf6a54bc8065f92dadc5` | 0 |
| confidential/deps/include/secp256k1.h | 42403 | `328da0a2e0433e9cdcfae1fbde894d50a17c349e366e03f3f99fe8558ebd9af9` | 0 |
| confidential/deps/include/secp256k1_mpt.h | 16209 | `ee1a061db0bae3c1b9259aee21a989ff2a5df3e15f5267eb8f54ff6eba054a03` | 0 |
| confidential/deps/include/utility/mpt_utility.h | 18927 | `909a063bb3643ceef2ffdc988fc112a4b99d46e32223b865dd58302ffe413fc3` | 0 |
| confidential/deps/libs/darwin-amd64/libcrypto.a | 9163648 | `119d5f6bbb5e9af6744de4d74285739ac995421853163266147a2b8f0b2e9e9f` | 0 |
| confidential/deps/libs/darwin-arm64/libcrypto.a | 8927336 | `8912dac8f995dc5e99074468a06d6a40b6b2f8bf7d2dbfd0e56283476ac5924b` | 0 |
| confidential/elgamal/elgamal.go | 6207 | `55af2dcb32d75448cb2faab53d599e883cdcf49203fbc7a56d81b15935f081b0` | 0 |
| confidential/elgamal/errors.go | 1522 | `747dc5f6ed0a2b2e0b59a49548a5aa19104df858412fcbc6d382c67ffe895d69` | 0 |
| confidential/go.mod | 912 | `660fa1ddd869f0b82e1aafee44e8319ec45c10c77dd08eeb1da05baa316ef404` | 0 |
| confidential/integration/doc.go | 355 | `8e2005c7957562808049513c24b444f00917cd24f3719cc4f70464f3e39809c2` | 0 |
| confidential/mptcrypto/errors.go | 827 | `16ab957b77d42ebf9f1eb13b0b5e2416d065434f1139ed32dee34926bdeae4c5` | 0 |
| confidential/mptcrypto/mptcrypto_cgo.go | 17531 | `5daffa0c8fbc4f93825e6481447650b2bfda6ddcf703ff240a1ed035bcb57a01` | 0 |
| confidential/mptcrypto/mptcrypto_nocgo.go | 7402 | `6274e87c038e2fa27aadf60f1080269d2dfe76d7b64c7ceadb0fa1fc0a79bd75` | 0 |
| confidential/mptcrypto/sizes_cgo.go | 2350 | `27fde8ff86f67e9cf9cbaa6a976e75607760a2e0c60ce0666d6ae321075b330b` | 0 |
| confidential/mptcrypto/types.go | 1468 | `9681e7276672419d80099ae7ef8f9f0d8808aa5f19b7ca8e91b581c90c9fc0bd` | 0 |
| confidential/proof/clawback.go | 3483 | `7bc905f0394d14cfc5baaf3f2c776a64bbab777b9ae3ee572e43dd2f54e3f063` | 0 |
| confidential/proof/context.go | 3907 | `c1778efcd917958343c861d42cde13b48ec6de1012cea0de69ccb6040026bd25` | 0 |
| confidential/proof/convert.go | 2663 | `d88c052baaf17bb47ae4191bbb536e3f26451b44c8f1692da732f10b1b256d44` | 0 |
| confidential/proof/convert_back.go | 3353 | `b8fbe7010e338b7d62d0aa61aed699bd2b4349feabaa71c0239dd241462a6966` | 0 |
| confidential/proof/errors.go | 2128 | `5c9a32f4c1a64ffe5d0779318b162d5042687e32d5427cb32003c2b123d5acf4` | 0 |
| confidential/proof/helpers.go | 2460 | `d58467e42df86843e520985719df57c566a5800b103618520d23a04b99167f87` | 0 |
| confidential/proof/send.go | 5791 | `33ed47118cd7f3e52dcd124293f161447b23bdbe7595a2a1a639fda89409d2c3` | 0 |
| confidential/proof/types.go | 480 | `07a4b1dd491553de1e7093e9977fd4701169090c947532ae258ef521bc03c5d3` | 0 |
| confidential/proof/verify.go | 2510 | `86e714717f71e9f295333a6b3059a0b951b4c451b1f9af5150bfc020b043df3e` | 0 |
| docs/docusaurus.config.ts | 4559 | `cd38ae66bb6583c19242d14790e40a0c1acb0607f7283ca56359bcbb11e30ea2` | 0 |
| docs/package.json | 1487 | `b2fb1930bd2911b3414a1421781a2e23fe05e56b86d2d31de1b12cc15630790d` | 0 |
| docs/sidebars.ts | 2482 | `15eab4aa5eda275e768ed7e24952c62ab6f23b7d27ba9ed7dabb877ba0522b04` | 0 |
| docs/sidebarsChangelog.ts | 438 | `186e1d24db2b3b720d013a30005c01d48d3ba42c5a205b2fa31397c8e0687738` | 0 |
| docs/src/components/HeroSection/index.tsx | 762 | `794fd412149a0f28135c57a9be3a2694fb713eaddd120be19b0adba327238e54` | 0 |
| docs/src/components/HomepageFeatures/index.tsx | 1923 | `c5a5106aaf4ebaaa1a440650a3e6567afd2f6e62249fd974e107d40719619e75` | 0 |
| docs/src/components/LinkButton/index.tsx | 457 | `7c7cd48eabdbc7279722fdc60da4140f00df7997665d065d0326ec97d331d357` | 0 |
| docs/src/pages/index.tsx | 1062 | `ff824c9fb9ae4c1e3e6b8d7c1cafde8bb3cd7793a8a831ce4ee138c10f1e1f8e` | 0 |
| docs/src/theme/SearchBar.tsx | 383 | `7c5fa368dfaa927658d9b71e34c8894dc8e7527b364175606e9b7a36e28a4c60` | 0 |
| docs/src/theme/sidebar/sidebarLabelGenerator.ts | 1894 | `05343e2de54053115faabbe884073cd12ef8a17f2aed4384402a11291a513d40` | 0 |
| docs/yarn.lock | 450679 | `aa4f072a8e127952946db4d3523bcc8cae8023cdaa147e1fbf6c02589f9e3c16` | 0 |
| go.mod | 905 | `3bbfa87cbb538b9cfa639e3b15c8de1847d9beda92e4a8409c5e362ebf7c5091` | 0 |
| keypairs/crypto.go | 2241 | `02c2b8d5128163f25e29d9b42768b32226fca6514de5b8bee68f0a837e71e47b` | 0 |
| keypairs/errors.go | 1346 | `b9dad719958a774973fc207eed61d7c13ad27b4411ffa5ea9e818c42719cca71` | 0 |
| keypairs/interfaces/crypto.go | 554 | `9c7a175e0d4f5b8d2df4db177acb7ac94d259cf5fe1a33414dfe54cce4a1eb1c` | 0 |
| keypairs/interfaces/random.go | 189 | `7997445ef325f85129a0e3509b7c1ec14cb853a54b3af6608dafd70c714a3758` | 0 |
| keypairs/keypairs.go | 4540 | `def432fed3c778e4dff44f2cf97f135088ad5787f51aad4f2fb9d8cf0cb2be85` | 0 |
| pkg/big-decimal/big_decimal.go | 4622 | `c57df309667bbc28e4239129361673b0bcec8b61f7def53ea10da9ba2f105ce0` | 0 |
| pkg/big-decimal/errors.go | 547 | `dbcee6f0be6c5c83d44717a5f9f5750aac8ab019e742fdb834328943bad77860` | 0 |
| pkg/crypto/ed25519.go | 3096 | `e62d5cbbd0eff17fbf6f5602cd25f496af467a1e3b7ce5ae07408b5d69b456dc` | 0 |
| pkg/crypto/errors.go | 829 | `f3eb8213f9411732b47a6e483ade97960589418803a142091d9087efa2e3a5bc` | 0 |
| pkg/crypto/secp256k1.go | 5884 | `51e07c32b8f4c75e2261de90e40b238819d59c7899ee6f2551e356e302bd4352` | 0 |
| pkg/crypto/sha512.go | 190 | `b427118e844c121f956a1b34615b2e1d842616eae2d7c9333b2c08f720aa325b` | 0 |
| pkg/crypto/types.go | 192 | `efb37413089f166d18d69f5315d6d2905c60445726d4de3b41a6acac3f8abb83` | 0 |
| pkg/decodehook/hook.go | 1379 | `20c142cda83ec26921d08e1e398ddba2be4928c930299ba9fc984e569eb1d4be` | 0 |
| pkg/hexutil/errors.go | 195 | `4714c199278b66ff2d06ed360c3384e8e067cab37b14db8b3c7058a3f286f5bb` | 0 |
| pkg/hexutil/hexutil.go | 685 | `9261f523fedd8f29b388b2344fdf6054a53a82842026c86fedb7d738bdf72b88` | 0 |
| pkg/map_utils/map_utils.go | 278 | `ce0ac0689010745852baa0f6e7d3d0dbbbc8ecf7ba5b506fdd1f5ab350ab0b9a` | 0 |
| pkg/mptsizes/mptsizes.go | 1843 | `15bee7cfc497499ffabd8f450f83424bd17ea007be3742552b4e68393b723a52` | 0 |
| pkg/random/main.go | 803 | `0af6c49b1196dcd836bc7186943aef35b4f6cb2ba5d47d237c26d69beefd8ba4` | 0 |
| pkg/typecheck/typecheck.go | 5307 | `ecd5f8800cc64c6d1b17472fb04546aedd5b25e7eafdfd0ff9ca1ce047a29d08` | 0 |
| xrpl/common/constants.go | 767 | `79907f10675b71c14efb5f2908526c7bb2e5371c4060460f65bb0bcfa584f4e6` | 0 |
| xrpl/common/interfaces.go | 559 | `d696b47ac2b6d898270ae40fabc2019d8bcc9f234e94d241d2dc5a2b6e8b7483` | 0 |
| xrpl/common/network_timing.go | 184 | `01c44db789302d325429a4dde6bf431926de58971560f34321c2c6240d871c6b` | 0 |
| xrpl/common/network_timing_localnet.go | 190 | `0949011f060a7aff95e14c6167e8da88d157d3d953ec24979de9c52f4569fec7` | 0 |
| xrpl/currency/drops.go | 5564 | `52839a0e83debf252b24e13d9496b1b0fe8b55007acef498474725a8c87463e9` | 0 |
| xrpl/currency/errors.go | 2071 | `6a5c5f2b7090443bf12c9959c435b6ec2d5a079d44db32867188d77e1bee833a` | 0 |
| xrpl/currency/native.go | 2895 | `8b14c9eaa3a8b44f48f03785d589a71f4d07accd16f0b45a02e3ac159998c3de` | 0 |
| xrpl/currency/non-standard.go | 2006 | `1cedb3d3dc14e7ca12eb78e6433e4e92a71042450741d894de4f4527e30b32e9` | 0 |
| xrpl/currency/rat.go | 731 | `ddec5ba12a5d5bbf45f0ef6179f76ed313c849b922fc430077555cd0b0a40a35` | 0 |
| xrpl/errors.go | 1088 | `dbdad993f4a8ddf086f87936797789aa524ea765382f930a5a7fe623f448c1fa` | 0 |
| xrpl/faucet/constants.go | 199 | `67a19b0aa21ba9a0430edb583b3f5f3211ea2d8493492d2c4119a08ab310421f` | 0 |
| xrpl/faucet/devnet.go | 1933 | `6588522906f4d15aa8f4e4ce1734029494c6106bfde26e3ddfa1514a95b8c2e5` | 0 |
| xrpl/faucet/errors.go | 1261 | `366c425499ee1e65caf0ebb68aee29cfe94020605a16998a08ea43e418a22419` | 0 |
| xrpl/faucet/testnet.go | 1885 | `99701eaca95c0fdd78dd877de89fea751d220bf7e9bb597ccfc5d41605890846` | 0 |
| xrpl/flag/flag.go | 844 | `d4d646227dc8d71eed58a86c1c97b96349a85092e97826c391cfb4e6e184db1d` | 0 |
| xrpl/hash/constants.go | 731 | `d4e70e047fd955f849a4c964cbe91801f70d974472e5e51cd621c7a34fa7cb94` | 0 |
| xrpl/hash/errors.go | 991 | `11c3ff51ccacacc47a717e9a4605a8f59e4a717821c53dcba30dabcec18b7899` | 0 |
| xrpl/hash/ledger.go | 7080 | `abd151dd6c479fa0af148cbee242cbe9fe437fbd8b91820dca5adcea60e3d4ec` | 0 |
| xrpl/hash/tx.go | 2315 | `da4fd1beee128bcb4562b70bbcfc9eb693e65cb80abcee9c6dede5ea5c2af927` | 0 |
| xrpl/interfaces/crypto.go | 278 | `a17884728cdb7b0f3d01c4ee7250e7ee88d8b0894b23d98e16901244310edf74` | 0 |
| xrpl/internal/client/account_delete.go | 1676 | `0f9565a492967820103d01a3c220242de6cd4746f27129dad4cc8ada70190c44` | 0 |
| xrpl/internal/client/address.go | 3934 | `76feead4dfd350ea07352be833988547db3a79f210bdc4655ff7c4f05b146b7c` | 0 |
| xrpl/internal/client/errors.go | 12196 | `35e01e6bf81bbefea0791d81717ee0f3be673fd4c3b29b2d075f8e35f6368225` | 0 |
| xrpl/internal/client/fee.go | 2318 | `a9a5fa2280fd52ec43dfebf01d86187f076554f92c653d6a7c1e97bbc4ea4fb2` | 0 |
| xrpl/internal/client/fee_calculation.go | 8824 | `f96d65cd69651068693a48c7a57a56503b12babed8a740cddd976b84d871a243` | 0 |
| xrpl/internal/client/finality.go | 6501 | `cb7694c775d037f582aa3a05286a2d39f07be8bd78bbfbd7655393df727812c0` | 0 |
| xrpl/internal/client/finality_hooks.go | 1821 | `76bf9062b27ff6265867eebfcc6187ad528d0811c7b99872fcaf5f37ef1c4df6` | 0 |
| xrpl/internal/client/network.go | 7863 | `b57f2c2f6e87416e3e99df6523430e656e8dbabd1bb45029a6bacfb87149d779` | 0 |
| xrpl/internal/client/query.go | 1861 | `f86561fcefb0d0f1acae95f956ed8d1691ec6864d680463990141c49862bb137` | 0 |
| xrpl/internal/client/query_helpers.go | 2547 | `ff1ecc3c9d7d9c839f040b85e5f20220539466d70c2050bc9bdecd817ec70f5b` | 0 |
| xrpl/internal/client/sponsorship.go | 8370 | `6929dffdb75c8bd5fbd435280e2befa30ec27a71069282bd0ae3fe3f67c5d3dd` | 0 |
| xrpl/internal/client/transaction.go | 11604 | `fb22e0b73dbc2dfe4013ed41d06c91ffacbc15f8e0a2bcc9d63326b21fd2f603` | 0 |
| xrpl/internal/client/transaction_map.go | 422 | `c67d027905c8e3cdf780cf50af11a2506c65206c2f48db694428d0815d61b257` | 0 |
| xrpl/internal/clientconfig/insecure_scheme.go | 1794 | `5d96ced0e1bd510371b58651243213df1b7896544b32832d8c48ac0473f01c38` | 0 |
| xrpl/internal/clientconfig/redact.go | 634 | `90266b1b7e1384d51a26d36eb5a4cbf2f3f6c76b54adff5a9e5a38c8453d04ac` | 0 |
| xrpl/internal/decimal/decimal.go | 3554 | `88dedb2b28a81d3efc27ebfa30d32ba2eaa9187ea600b12e7bfe5043053f3e77` | 0 |
| xrpl/ledger-entry-types/account_root.go | 10774 | `12422bac86f99ead97dc42d7964e0de16a1cec0588659d96421f733f48ca0d85` | 0 |
| xrpl/ledger-entry-types/amendments.go | 3312 | `f00c59af103c8b759f82aebec185d0904c8d88e1f53cd6d52099221e8c5e7ceb` | 0 |
| xrpl/ledger-entry-types/amm.go | 6567 | `6707f8e297a8a12dfba686a6f39d8cc6cd384b5cab654761f7bc7321c8161ae4` | 0 |
| xrpl/ledger-entry-types/asset.go | 1262 | `084ea536653acea99615811f6d8ec13959d0f2675a3469e044a5b9ea7497392b` | 0 |
| xrpl/ledger-entry-types/bridge.go | 3556 | `4ac0ce2250e5c4d67e53363796cdcdb6b06d450f0aa78ac453f8232dc49eb7c7` | 0 |
| xrpl/ledger-entry-types/check.go | 3659 | `d668ce5206d279bfc8cacdbf91e5a7b1359588193fada3af5224c168aaf3f1eb` | 0 |
| xrpl/ledger-entry-types/credential.go | 2710 | `fab7afb21b53b95e096842dd5ff91747258adab4761de14a321a63aaf9491807` | 0 |
| xrpl/ledger-entry-types/delegate.go | 2239 | `b15bf7fd4105aceb9f4c0117ad36dd5198122a5cd0635ea7b5692b541de98c17` | 0 |
| xrpl/ledger-entry-types/deposit_preauth.go | 2710 | `dad1c19798a9ad21019c5adc868b286bec5106204e39aa14d96f3bedc3072ee9` | 0 |
| xrpl/ledger-entry-types/did.go | 2505 | `24881d3c3950dc67ebb74bd5b3c28341971eab50a5d05ecf6408a9e30f91adf1` | 0 |
| xrpl/ledger-entry-types/directory_node.go | 5221 | `151b26069b0aaf1cf5e28a4108d3d9131755295b9d320c54ef388c0819276bab` | 0 |
| xrpl/ledger-entry-types/errors.go | 1612 | `f9aac6660b80c069a6d3c28369ec2735e89471b2b0fa37a67dfcdf0dd5eef7d1` | 0 |
| xrpl/ledger-entry-types/escrow.go | 5136 | `e337de945a86f0c0d808612e66ea8df44bd6bfe69153f8b9ca3d482b6f0fbfa3` | 0 |
| xrpl/ledger-entry-types/fee_settings.go | 2084 | `120073f19f40be6d7b8d4394b82d21524c90e62095cece610b46910aa2e70c02` | 0 |
| xrpl/ledger-entry-types/ledger_hashes.go | 3435 | `c6ea2a2d2182c84f6a7ddd6a36946c2b0a77349a4fdb877ce96646dc6bf68486` | 0 |
| xrpl/ledger-entry-types/ledger_object.go | 4471 | `d234608676fbc0f40d394fa5249f3a7280b6e2499568854e605d1d35940e6572` | 0 |
| xrpl/ledger-entry-types/loan.go | 5848 | `b3f81604f2e20693a0e3cb77ea7dad43bffa83c2d74a6cee04c763f5f280edc2` | 0 |
| xrpl/ledger-entry-types/loan_broker.go | 3737 | `964d8cec7a472546d52e758dccd61e1c1ba3bb0fdfa456da3cee600ee7d65160` | 0 |
| xrpl/ledger-entry-types/mptoken.go | 3848 | `0c214736f93ba3184dd65ef929acbeb5003606330da85b6a01e3d199f1a3ed82` | 0 |
| xrpl/ledger-entry-types/mptoken_issuance.go | 8254 | `ef8b215b838017dc280605d3818a63288182a29764bea56b9f73aa0a3533c44a` | 0 |
| xrpl/ledger-entry-types/negative_unl.go | 3083 | `968cfb300c5bda0668a2d1eb523ba044bd5039ca3cfb8bbc70494fe14b77315b` | 0 |
| xrpl/ledger-entry-types/nftoken_offer.go | 3629 | `10524bca389a663d45120f7985a9f0d1d1bd12aec1efea51a498aa7e0d28ffd7` | 0 |
| xrpl/ledger-entry-types/nftoken_page.go | 2677 | `6e2101c2580e03454e0eacedf7dba01d064d36adf71a859d356975d9e984f817` | 0 |
| xrpl/ledger-entry-types/offer.go | 5815 | `31a184ca0852670e1edd101da0659305dfa5dabf196df7e27470e1ac7300f6a5` | 0 |
| xrpl/ledger-entry-types/oracle.go | 7145 | `f917b87271fbfe183f395df480d8a1de9ee824fa9d49efc69e73e6591ea9fcab` | 0 |
| xrpl/ledger-entry-types/pay_channel.go | 4566 | `22fd3af720b0766845fe07fa6183b46cad6d3d767610cf9325400f3fc4fe97e3` | 0 |
| xrpl/ledger-entry-types/permissioned_domain.go | 3269 | `67337c0bc435bbbd8dffdcb7ec74569e96b974fc40efd576bcfc23911329232d` | 0 |
| xrpl/ledger-entry-types/ripple_state.go | 7276 | `b6f53d6a5ecb733c562d294f7be2af024b22e62ce7ec64ad55d475833e61a4cf` | 0 |
| xrpl/ledger-entry-types/signer_list.go | 4965 | `4e75f3b76235e0aebc5ff41c629b165a667fdb29fabb2a77597d270bea11eeb8` | 0 |
| xrpl/ledger-entry-types/sponsorship.go | 1726 | `180c18e008943454d070fba32ed257bcb29627f00d08e895943c575704da94af` | 0 |
| xrpl/ledger-entry-types/ticket.go | 1757 | `067bd7192ba3fd5889e1c637b65fc836c1079efa59bb0b6a24ae3fde22252ac6` | 0 |
| xrpl/ledger-entry-types/vault.go | 3804 | `6601d10588cddb1cc7bfc4aa6c5f78e03e73ce0a51c4ba217365893670ed3886` | 0 |
| xrpl/ledger-entry-types/xchain_owned_claim_id.go | 5191 | `deebe63986cbefb1a1b70d38704048f9644947c9ab1546ddd25d98cdea1df0a2` | 0 |
| xrpl/ledger-entry-types/xchain_owned_create_account_claim_id.go | 4171 | `45bf510981a67ba7fd8ed7d68328ff08b061f81fbef03b5c0cd97796709fce4b` | 0 |
| xrpl/multisign.go | 6426 | `2d03c7a38acc3c83fdf2bdef783d42f1b6acd9fccf238fe46d53ed2cb15640ea` | 0 |
| xrpl/queries/account/channels.go | 2297 | `5395b5c2ab709ede88cbc9e92ac888f596bf915a0850dc89d16ce2231d8a396e` | 0 |
| xrpl/queries/account/currencies.go | 1626 | `88b256d6446b7aa3f8c5707df5382e467364e8abd7e9ef156a55a6903954c81c` | 0 |
| xrpl/queries/account/errors.go | 169 | `1f2e0a0dc6d3e829a19c2a8d3a4deb8a9380004a62244c3e3b41524c2575140b` | 0 |
| xrpl/queries/account/gateway_balances.go | 3306 | `05af47a633a25864bbfaebdd7ffdb0feca4434c0dac7652a8641234c220371fb` | 0 |
| xrpl/queries/account/info.go | 2120 | `258421518e3c14839da8d3835e08d95cb5038814798c544166f05e46822d4040` | 0 |
| xrpl/queries/account/lines.go | 2307 | `29a5443968a4d934371ba8613a5f8cc2888d2bf0e0636746bd82c10bb0ea5d66` | 0 |
| xrpl/queries/account/nfts.go | 2096 | `c25c1a0cb6dc608c8b6f3949683616834f09dfd3e42d0bbf9a29d91600f7d166` | 0 |
| xrpl/queries/account/no_ripple_check.go | 1941 | `443f66b4f92fe2cc97a4330710259911ab6436b46cb67d3eb0e54e4792cd6ebb` | 0 |
| xrpl/queries/account/objects.go | 3662 | `c092f5363bb03c86a8cda3e9e22b4e7b86a447e18b7f06bf9cac121670d17a76` | 0 |
| xrpl/queries/account/offers.go | 1916 | `47a5e6a0986686932e4ae2a4d9e8b1dd75d1760a0a53b88e41551539a476956c` | 0 |
| xrpl/queries/account/transactions.go | 2903 | `e978583823f7159fc589a3819e4f8232d5616d24bb2a30e22a4ddf0bc1bbb2ef` | 0 |
| xrpl/queries/account/types/channel_result.go | 1201 | `c9549943cfdefb37609c0598d506a6cc7d96108fb77d522344cede8f73149482` | 0 |
| xrpl/queries/account/types/errors.go | 250 | `284c3d0bc23efb1b6efef1b52e4684425950e9d70c2ed39bb4b57bff2dffb507` | 0 |
| xrpl/queries/account/types/nft.go | 912 | `88da0560ceb9431c4323a488a460bb1d875e5aaf21546590398c9e52f2d0cd41` | 0 |
| xrpl/queries/account/types/offer_result.go | 606 | `c3b0da9162fb093694fa9297628e3116b891f6df2e7665a8c610870e4e4e46c9` | 0 |
| xrpl/queries/account/types/queue_data.go | 674 | `fd9c42c5c3ae79d8915c989c52135338f2749978d80feb486cb1152162153ef0` | 0 |
| xrpl/queries/account/types/queue_transaction.go | 667 | `20388d62384f6cb724668291093d0796a73816ee58a7ff2d9a0239e1e276ce64` | 0 |
| xrpl/queries/account/types/trust_line.go | 894 | `73d3cb817cb745d0111c3357b0cb2ae9f154362b4494d0496a8aba6f021d4ada` | 0 |
| xrpl/queries/account/v1/channels.go | 2421 | `61466f95344782e60fcbd14fb8eda6f76822da474d0c6f0fb10e4ecc8399657a` | 0 |
| xrpl/queries/account/v1/currencies.go | 1877 | `92d35f71aa7a1de1fa8e12f8b62dcbab2c2c8abe34db4578bbf172ff322f9b6d` | 0 |
| xrpl/queries/account/v1/info.go | 2082 | `7ef0f6220c761f694f601e188f14c9a13cfd045206619673de5ab7dec73b7486` | 0 |
| xrpl/queries/account/v1/lines.go | 2296 | `59a8405adc9d36f361a45c13e584887a30f1a3d40156960c724f9619cf48a0cb` | 0 |
| xrpl/queries/account/v1/nfts.go | 2096 | `71c3778a95f10f0437f3915d4a9c387ac069133f05d76ad1c52ded8f32535bc6` | 0 |
| xrpl/queries/account/v1/no_ripple_check.go | 2023 | `4cfad2dfbd63c48702825fdf07df4b3f671199105547c18e042e8a7fc0737582` | 0 |
| xrpl/queries/account/v1/objects.go | 3407 | `50ef23357f6ae69359952342af90677474c43b7781d6bcbdfb1203fd16f9b555` | 0 |
| xrpl/queries/account/v1/offers.go | 1999 | `aa30cebf166548c0587376021c3dd4dbb7954628fbe012956ce21933180a30cc` | 0 |
| xrpl/queries/account/v1/transactions.go | 2686 | `0a118460f3df0a5080d15fb9c14a7ef1549e01514bc2c02d55b9568f8ef46957` | 0 |
| xrpl/queries/account/v1/types/account_data.go | 337 | `4271d822ccf3c49312c84d32db432c16c0d207de96356cb3dff083774a16e8d9` | 0 |
| xrpl/queries/amm/amm_info.go | 6985 | `8bf222c72e25e24ef7f0e52aa2290ae511a4836634d185165c5de24f630805cd` | 0 |
| xrpl/queries/amm/errors.go | 277 | `e4b1d3c61550d519c5501272c97cfdaeeb0ae35c5244118579382e7d22a7fdc2` | 0 |
| xrpl/queries/channel/v1/verify.go | 1570 | `6db65ccece93a8201433d537aa4656ac90d0db5d981337d940000b57e23a324c` | 0 |
| xrpl/queries/channel/verify.go | 1554 | `6f56af25d77e87e8951264ccf17824d44722caf6e36397b3acb837437abdd306` | 0 |
| xrpl/queries/clio/account_sponsoring.go | 2175 | `11cbde50b8fee4edf3bd22361fafe3eb173a9802ab99ef80584844cd5bf8916e` | 0 |
| xrpl/queries/clio/nft_history.go | 2584 | `150257a464c7df4e1f46fca22b3408e06738076e4249bd5a5b0eaf63d3575992` | 0 |
| xrpl/queries/clio/nft_info.go | 1878 | `674f768d5e0ccc56e408ccfb367f2636896a1be734cfffbd3faaf6d58a94fa8a` | 0 |
| xrpl/queries/clio/nfts_by_issuer.go | 1865 | `d75d6aa93c5c7483e6e0ae66f00db8eaee8bc6a19ebeaf61f4cdfe8575b0f6e9` | 0 |
| xrpl/queries/clio/types/ledger.go | 1474 | `d8202788ef0f2eef0017f9df0ca2988c5eeb19a4f4143e93f13d1eb6d6e557da` | 0 |
| xrpl/queries/clio/types/nft.go | 1069 | `64475f71984cd59842c91192f9aa72f7f89ad23d9ef2a5de9cb58a39af217cba` | 0 |
| xrpl/queries/clio/types/server.go | 2968 | `6b357369a97554b37125c1b17329e96951d0c3330a38d6c2b62ba45764e9be26` | 0 |
| xrpl/queries/clio/v1/nft_history.go | 2561 | `bfcdd99982e4515cf1423fcb802282a61e14fa2d6f3dac1ce6795c9c7d23dedc` | 0 |
| xrpl/queries/clio/v1/nft_info.go | 1889 | `b0fc1a46a028033ac4e7747f313add32a5321c2c56446095bf59a8dc2b7d9476` | 0 |
| xrpl/queries/common/errors.go | 247 | `d998d476f3f922719ef0bd1e381bd9bee811745f4a5e6af9a43d0f7ffec9faa1` | 0 |
| xrpl/queries/common/ledger.go | 2026 | `ad69fcfac475f89dc3c8b14372afec43aeebd3a824cdcd3699ce975eced6666c` | 0 |
| xrpl/queries/common/request.go | 521 | `ade9758fadb1fc679e29ebe77f0f572a512ac6215333d2fd0992323eed981146` | 0 |
| xrpl/queries/ledger/ledger.go | 3155 | `fa335b1ec7dbf9313fe9f5192d8d412c95efaed06d159422784ab9f6d92994e0` | 0 |
| xrpl/queries/ledger/ledger_closed.go | 1224 | `b57034c096d59024651d9e4472cc2bcdc93697693482cb770ba8efa8d1d985d1` | 0 |
| xrpl/queries/ledger/ledger_current.go | 1197 | `b381217157f18ef1f0d992038feb629f3be542c25e2a1a855c4ff7c004b2f3a2` | 0 |
| xrpl/queries/ledger/ledger_data.go | 1878 | `ff87e6a6703d5be287cca7e3c18931802a10fb4950f34fd5797a28927f7adfd4` | 0 |
| xrpl/queries/ledger/ledger_entry.go | 8362 | `db88adc032de4439c0bd6798253004b4399707f8731dac529305892f974624c5` | 0 |
| xrpl/queries/ledger/ledger_entry_selectors.go | 7041 | `3d8f334286168c78453fafd99eecca78dc56c8fbee713980bbdef8dffdec8f53` | 0 |
| xrpl/queries/ledger/types/ledger.go | 2177 | `5b0ffe5937dd6199f8e94150291404c81ea0f0c06016954d05d66ba1c0c8f18e` | 0 |
| xrpl/queries/ledger/types/state.go | 432 | `81bf5b30d0f864b725f81fcd8a831e8b6b1f4367ed695533ad988a48583fd212` | 0 |
| xrpl/queries/ledger/v1/ledger.go | 3324 | `36ac87a76bb3f40ac67e6c6f386c4a92e9a88399e6528b92f52b6f00fc6ed67c` | 0 |
| xrpl/queries/ledger/v1/ledger_closed.go | 1288 | `9b9ad5a4fff0ac6f1a584ab14a5e0b05ba0bc51d3386d084d4f404899e9b043a` | 0 |
| xrpl/queries/ledger/v1/ledger_current.go | 1265 | `06cfe3b1f10531289693fa79028f5d692cc6ee6edee9cf623a6d5222ae0a02c2` | 0 |
| xrpl/queries/ledger/v1/ledger_data.go | 1608 | `caf9e5c205ba0b3d19e23e894d2879227a712c6a69541db93fdb6561817ea276` | 0 |
| xrpl/queries/ledger/v1/types/ledger.go | 2218 | `8f36f60d0c4bdd408c4fe5f394526e72d4f1eccd2f279b3dd767f5387416e747` | 0 |
| xrpl/queries/ledger/v1/types/state.go | 429 | `d54b8c34a9ff1beed40b1417ed23dd64fa21f6ad817c1dd9361856c6b9bafa16` | 0 |
| xrpl/queries/nft/nftoken_buy_offers.go | 1910 | `98aa4eccf2d046fcd72b32e85fa3621ad72b87d32941dc3f3d865de6ba6c14fc` | 0 |
| xrpl/queries/nft/nftoken_sell_offers.go | 1900 | `3d1d034418c0576b5a7832174f1f3f171dd7f63e971b87a76b4f3888269351ee` | 0 |
| xrpl/queries/nft/types/nftoken_offer.go | 602 | `0a2651ad4dfc8ade181d53491bb5676b6b5b40342d9efdf35ce9508f109024c6` | 0 |
| xrpl/queries/nft/v1/nftoken_buy_offers.go | 1968 | `1cac0aac02f2def06e4f57e53d7b0e5440c078aebb8921ae2b4d14e540ea0459` | 0 |
| xrpl/queries/nft/v1/nftoken_sell_offers.go | 1901 | `6245efd2c557da1e7543ef0e8183567a6f34697dbcb8c54a7434585b498151d2` | 0 |
| xrpl/queries/oracle/get_aggregate_price.go | 2892 | `9422ac218eed543782892667d4938b83285df890c96fe2d1d9e3cd00e74cb474` | 0 |
| xrpl/queries/oracle/types/oracle.go | 248 | `37614eaa7ff9fccd3d84790e008a883cbcff986cb0920e53d103c0a9360b595d` | 0 |
| xrpl/queries/oracle/types/set.go | 378 | `76dedce5830202e9583ba9a3bc7b7ff88545590c708391d1bbea9050d43f80a6` | 0 |
| xrpl/queries/path/book_offers.go | 2205 | `d35c4132d97890240d95d5f6bbc581536dce6b191f17552d402a870b1580e51d` | 0 |
| xrpl/queries/path/deposit_authorized.go | 2102 | `38d6fd64eac86cd311d7b3fc7ab1456c9047477db38eb316629dfd6924e49f91` | 0 |
| xrpl/queries/path/path_find.go | 4376 | `64349dc617f2dd1cbd066daec629b9ce7188807d31f957f44f9ba300ed3013a8` | 0 |
| xrpl/queries/path/ripple_path_find.go | 2632 | `ed55bd6d79def20724177287b60984e992bef83eb6a562af36d035798a26e8f9` | 0 |
| xrpl/queries/path/types/book_offer.go | 2620 | `8e536937a04a4322f60205cd85224de6788e1a44391f51c87bdf73199d7ce615` | 0 |
| xrpl/queries/path/types/path.go | 987 | `1c86fc43bdb0b4659fc3459e8fdceb0aa4294e7db461ed905842f9dcd3078037` | 0 |
| xrpl/queries/path/types/ripple_path.go | 332 | `c6ed59f6d80b922846b6320319bf15cf5e8aee2e536f9190dd3e700a34db2cf3` | 0 |
| xrpl/queries/path/v1/book_offers.go | 2207 | `f87b522b16b2748197d780c11254b24e8b018d9149b21e610cd345b7c52c0544` | 0 |
| xrpl/queries/path/v1/deposit_authorized.go | 2231 | `531b273e22c854fb39532ecbce7688856e5f75597d2a9a6c3354968278b95a66` | 0 |
| xrpl/queries/path/v1/path_find.go | 4267 | `78d58c5c58eea56c6b75a847204e326b6a4cbbe251c4459f2d5ebc8bd4b201ed` | 0 |
| xrpl/queries/path/v1/ripple_path_find.go | 2845 | `7e201b5552ea0248c99d913da6421650725a07535456a6f1986a199259d41afa` | 0 |
| xrpl/queries/server/errors.go | 967 | `674be510c3792aeb37f21a65f888e0e003be0dee5df426c94435ed2ef56407c6` | 0 |
| xrpl/queries/server/feature.go | 2748 | `bb29eebff81c695089ce04255a8a7036d69cdd9902cc02a8d60439e7d035ac13` | 0 |
| xrpl/queries/server/fee.go | 1751 | `19eaea674bbf1221fb9eb65d842821ba2d70020a27e4143f3c52925522f98fe0` | 0 |
| xrpl/queries/server/manifest.go | 1833 | `698c40d376e331917fb95f4e305750595614611e854c40722ba9297a21085b4b` | 0 |
| xrpl/queries/server/server_definitions.go | 10706 | `9874354219fbb689d145f2fa7f164552ed4fd94caae2ca64bf08c34ab30633f5` | 0 |
| xrpl/queries/server/server_info.go | 1231 | `c360d2d6ab17815ce48676bdda74df92a9a7866e361e52a19306412b93426790` | 0 |
| xrpl/queries/server/server_state.go | 1464 | `1a81c0f83efd1517253623ecdb92e8fc40aa794c5dc4cd2b10933bece2cadbfb` | 0 |
| xrpl/queries/server/types/feature.go | 291 | `814fd8321322d0388bf6cb62dee7f309cd5b1a9cbb8715ce550c966faf1881b7` | 0 |
| xrpl/queries/server/types/fee_drops.go | 441 | `1018665417ba32f7e15ac90d87f05afa057a685cddcf9f16609a6494c41d1417` | 0 |
| xrpl/queries/server/types/fee_levels.go | 462 | `1ff7dfea7d8a4926712e33653d0a34a0de7598d73d91ea5d2c936f2a7d13a660` | 0 |
| xrpl/queries/server/types/job.go | 380 | `9dd53ba8878f7ab351226cb97f1630c48246f300797de69c912cb88a0f8a0342` | 0 |
| xrpl/queries/server/types/ledger.go | 593 | `bb5ea257d1285a66dd8855ad41ea6989bec99dafb49ecf77218f8cc16fae60d2` | 0 |
| xrpl/queries/server/types/port.go | 305 | `d03a2bb8e1f93c7ae306de8344414a4ca002711d432eda44f91626ec3dd85b6e` | 0 |
| xrpl/queries/server/types/server.go | 8721 | `4e81c61ddfbf13d8e3b46fba6eb3f5ce035b1afeec18a1c107b204a08bbd05f6` | 0 |
| xrpl/queries/server/types/state_accounting.go | 590 | `4ba1b4e56126712adfc95c4efe1be0478707c640895376c18efcd5f0f278df43` | 0 |
| xrpl/queries/subscription/subscribe.go | 2686 | `098ffe1baf35a8842e37ebab879d05fd2bbdf3a844446142c70cbf2fef641b61` | 0 |
| xrpl/queries/subscription/types/book_changes.go | 3331 | `ee901c5e084287ae5f013991f85da952af1c3d4c32419a65901dfacec20f4162` | 0 |
| xrpl/queries/subscription/types/consensus.go | 537 | `25dde77a3119632be6c86ffd99d82b53ffa9b139375a6bd13b46ab558e07953f` | 0 |
| xrpl/queries/subscription/types/ledger.go | 2241 | `e40ec7a5da852e53ca759f0cd9ef1ca2de17531e625488aebdf2d7a0ac0cdc18` | 0 |
| xrpl/queries/subscription/types/order_book.go | 2586 | `7b3345c940face52c4144c227c61091e766d6b770853a05587eaecd28d69be65` | 0 |
| xrpl/queries/subscription/types/peer.go | 2215 | `6ec8e57c53b80ad0327fd84e40b5aa37cd93762350b01335b928e97e096520cd` | 0 |
| xrpl/queries/subscription/types/transaction.go | 2067 | `ebaeac434b9149804cf4f5f233036de2f268c656e1025fc3c830393cc2d35cca` | 0 |
| xrpl/queries/subscription/types/type.go | 735 | `00eec4c3f4c7874dc479ab48cebf62005baaf4b644fc68ce36eabb57a766556d` | 0 |
| xrpl/queries/subscription/types/validation.go | 3761 | `ceebdeb261d4c1105e5e9414542823fbf055eb3f47254bbd48e341aaa0203cc6` | 0 |
| xrpl/queries/subscription/unsubscribe.go | 1804 | `75387dddad23e223b781ab17e268e7818cd8e5dc94326dea09e6ad3313f036c3` | 0 |
| xrpl/queries/subscription/v1/subscribe.go | 2725 | `543e1edef7e58651c1c1a6b3f931561c66c14cda397fd6af4ff6edcbfee327c4` | 0 |
| xrpl/queries/subscription/v1/types/book_changes.go | 3378 | `115872659e506314931899c32920eaa0e1839f7fa27358a2fd9b26654f7b0049` | 0 |
| xrpl/queries/subscription/v1/types/consensus.go | 549 | `57e42135a3a0b2ff9456b69b4ea37a6d0cf5b8a05f4072d1f93a1acf049ce65f` | 0 |
| xrpl/queries/subscription/v1/types/ledger.go | 2166 | `902e219ac8358b85971cf29ada17e01babdb607ba105677ff2c3dbe9f9517385` | 0 |
| xrpl/queries/subscription/v1/types/order_book.go | 2252 | `fa7eee1b997df1c4c498c7460b8a735eec5497925086053c5c5631e99990f28b` | 0 |
| xrpl/queries/subscription/v1/types/peer.go | 2214 | `97814ebe2d9a5f5a62002b5a9c429a2d997f213456945a9961a547eb242af7d0` | 0 |
| xrpl/queries/subscription/v1/types/transaction.go | 1883 | `56d318343c7bc1520ebb76b44ce3b4dcbe824e323e92b0322a9d996ccd8ea371` | 0 |
| xrpl/queries/subscription/v1/types/type.go | 536 | `2b8066e80007e6921b03e68074411a1ce8d0d8284b7e4d4dccd3270c2583980d` | 0 |
| xrpl/queries/subscription/v1/types/validation.go | 3685 | `b5c406b5956313245b552bc58e392d6b2373e3b7a19b79f2eed0bccf1954635a` | 0 |
| xrpl/queries/subscription/v1/unsubscribe.go | 1740 | `8f2b841625341786446a271f5d3847df872da45308210938e2043c6198f9de16` | 0 |
| xrpl/queries/transactions/errors.go | 1826 | `765755f778fadc350e61a9d055591f5b43efdeb8453f76d40ef2afc338b05d69` | 0 |
| xrpl/queries/transactions/simulate.go | 6425 | `d3a5d6ad349ddbd679e3b518d1c92f7448396c5647870c09adf579ddd631a63e` | 0 |
| xrpl/queries/transactions/submit.go | 2633 | `65b71b4d0ad45746cf1ddb53a2e0cb385525fbc4d873c409d92b7166a05c5e57` | 0 |
| xrpl/queries/transactions/submit_multisigned.go | 1840 | `32bcc8f93ba10270d2aa57b4abe11d95dcb66241ecb08a2b349ffe7f71e93e77` | 0 |
| xrpl/queries/transactions/transaction_entry.go | 1445 | `c09ff79e778a85c993f823aaeed47f648e794807598df7605815c19183e138ef` | 0 |
| xrpl/queries/transactions/tx_request.go | 1902 | `55704a46420f761aaf2cc8c10f23d45a4d43304e78dae3121046ad7ebb8e465f` | 0 |
| xrpl/queries/transactions/v1/errors.go | 154 | `5641e0dd9a0c81970c65eda340217efe6557527edfd88a25ea0a98b78765ff50` | 0 |
| xrpl/queries/transactions/v1/submit.go | 2445 | `cb7fc49096492871b4d8ad24eb461c0e9fd38663c0b52f2ddc191fcd188f7020` | 0 |
| xrpl/queries/transactions/v1/submit_multisigned.go | 1867 | `4fe17a3cf951c994d8c3a83df69aa02d4a56cef13da6db2d138e2613c56d281f` | 0 |
| xrpl/queries/transactions/v1/transaction_entry.go | 1269 | `441c4113541c9af6805b3725af3fe572d9b1e2fede94ac16bcb3d65758497c67` | 0 |
| xrpl/queries/transactions/v1/tx_request.go | 1953 | `9341397169c6e0711f60f08a465b4a18800f7b2074d7fb2d580c938fffe37070` | 0 |
| xrpl/queries/utility/ping.go | 1232 | `1dad4551debeb2ca38bcb8ea2db964250dc8c25be32d0e309bcc4af9c4d53b79` | 0 |
| xrpl/queries/utility/random.go | 1204 | `769b8467ef8dca54d3c19e8b7ad1c1cc93ea65a0b486c97842b456de2b5ccab2` | 0 |
| xrpl/queries/utility/v1/ping.go | 1218 | `672f807632760e2b869f8605368c5efc534a8b0fb58a536ba812d6c63ef02b2f` | 0 |
| xrpl/queries/utility/v1/random.go | 1199 | `975cd676c2e32d3a95fe5561c3b0063865e28cdb82ab1736a84672077c5035e5` | 0 |
| xrpl/queries/vault/errors.go | 1093 | `52af086e9eb7446e65a50ca23821d222086ce8fb4bc533e54bcfb5dfca379786` | 0 |
| xrpl/queries/vault/vault_info.go | 7806 | `4b948ffab10f91a55534c53eeaf0bf3e776d202f965c51ebe723da2a0d6ba54a` | 0 |
| xrpl/queries/version/api.go | 343 | `608ef98e8d11b3c2ce77bb61f521897ccc10f1cde3cdb7661a9c43fe3b04deec` | 0 |
| xrpl/rpc/client.go | 15833 | `286621e95c5840b57782dce424fe10dd79b532efd71125ea41fb3cbb23e40a1a` | 0 |
| xrpl/rpc/config.go | 5495 | `8dc29fcfaee56bced9a9cf3250d29b6742ef69f064b27526a8fc73c4b9ba23ab` | 0 |
| xrpl/rpc/errors.go | 14993 | `46fb726d187693f88aa901089075109ebb5dcf1256769d7a49eb035aeba71ae9` | 0 |
| xrpl/rpc/helpers.go | 9751 | `e05d287f9d2f40fa79aef9477d042c8792aaf376bc3637b2baeb243fb6f4ab70` | 0 |
| xrpl/rpc/network_identity.go | 4322 | `85c0c757a2cbae3b200ab1e2c72773b22a76145ea2762cbaef2b49f6d41c53a7` | 0 |
| xrpl/rpc/queries.go | 16021 | `5ad3d516fc31a8b328c997c156ddef97941a39dc1195e8a06146f6a775b73bbc` | 0 |
| xrpl/rpc/request.go | 553 | `cb2ca6e79aeef4a07f720a6fe85cf332e84f49fdfd878336b399d43ba2b335cf` | 0 |
| xrpl/rpc/response.go | 1351 | `01fe4d9a444046b1ccc1d84b4e023ec5f1b388863bcf745f8f9573d427e41d42` | 0 |
| xrpl/rpc/sponsorship.go | 1330 | `c8392eb638be2405684175f15c6abd7572f0d5533248339e433e6672ed3d72c3` | 0 |
| xrpl/rpc/transport_security.go | 5910 | `2629646affb804296ab8572a337ad52639dc639f49e8a59595ae7bf23184410e` | 0 |
| xrpl/rpc/types/client_options.go | 826 | `95a16b1176cbbeb21f3d22d6ad5a560af521765e374af1b7c76dadbe1da283a7` | 0 |
| xrpl/time/conversion.go | 2574 | `f154a7d11c0e816d2dedf2ddfddbddc56fa8d9317717a62fec43ca2629ac8673` | 0 |
| xrpl/transaction/account_delete.go | 2615 | `d146fec8c464f2e6bc4681189e176541d17b547eb6c52b28d2bf060614b5d553` | 0 |
| xrpl/transaction/account_set.go | 15778 | `55f295ef076be20ae37646091c2a1e3e0dcbe938abc702f616668f61a9b1e256` | 0 |
| xrpl/transaction/amm_bid.go | 4750 | `c27867e311251214107a42fb22d8f3f66ce4d6c2337ae900f3590ae7c3738961` | 0 |
| xrpl/transaction/amm_clawback.go | 3748 | `c27c89b4c57a557f155f0effeb1cc22fb3cccc77664c4eab7246eccb90d84e63` | 0 |
| xrpl/transaction/amm_common.go | 882 | `8e62c549228feb6ae33f509dce5953f6b8f2eb176ea5fbd9114376d5a569b083` | 0 |
| xrpl/transaction/amm_create.go | 2505 | `0b82e0dd2385daeca2a8aa7582499499b0d5ccd29fe8942e39b6564c48d3e6d5` | 0 |
| xrpl/transaction/amm_delete.go | 2320 | `517f37ac3ef956d18147efbbf578768369539dcdeda525ddf40e59d18acc01f5` | 0 |
| xrpl/transaction/amm_deposit.go | 5176 | `c0f84aa1936dfd7a3fc0b27dd38decec83770a68d1e5a75493817afada802df0` | 0 |
| xrpl/transaction/amm_vote.go | 2287 | `9254e15d351bedb132f0db86e0c996d7c3c8136af40468ed011823c18c7e3ca7` | 0 |
| xrpl/transaction/amm_withdraw.go | 5068 | `10ee36ad43875b716d764a1f145bd3c856086fcbac3c51e1c0d8fe4365b35b18` | 0 |
| xrpl/transaction/balance_changes.go | 8778 | `218bbb0e176ae16d6b281559a14ad2e0cdb6e8756f38fe6e3e3300def9d0db56` | 0 |
| xrpl/transaction/batch.go | 4327 | `e9f5751e22883a6836e15dfdec64dfbcb0691b9c6eb2f69ac085d6b9c889f0d2` | 0 |
| xrpl/transaction/check_cancel.go | 1503 | `3b14e76ff05e3d5f1aae1fd717b3020e2f7827964fc225dc882a1072f75ba5e3` | 0 |
| xrpl/transaction/check_cash.go | 3030 | `2f570bfd975cdf7c8ee8519578d8770bfd5aaeeef55f9881167ea2b83c799022` | 0 |
| xrpl/transaction/check_create.go | 3048 | `732b392672e5e65ea9a771f0030f0243182b30b5dd8307c1db902c09a0e3832b` | 0 |
| xrpl/transaction/clawback.go | 4059 | `9e5161e6df7bcad073596bb834c0dafab642a4f02b8670f3a612751852d33df5` | 0 |
| xrpl/transaction/confidential_mpt_clawback.go | 2985 | `7ef13464e61ebd9df2c11e868f19f77c7153cb33455c731ceff76c9904d1155b` | 0 |
| xrpl/transaction/confidential_mpt_constants.go | 2142 | `9fd56224f5cb289ed1b93e51c88ca0fc3c529e608d21d64af4395e4174f41491` | 0 |
| xrpl/transaction/confidential_mpt_convert.go | 5140 | `6e3738fe622d85edf54cd476496dae225e8b1d967abf157f7390bd6e46dc020f` | 0 |
| xrpl/transaction/confidential_mpt_convert_back.go | 4646 | `2e8d9be72f8315763da4ecdd8a49c96c2cc0deafa869a532af2d0a01b5d0ce4a` | 0 |
| xrpl/transaction/confidential_mpt_merge_inbox.go | 1847 | `d30c4ef1c4168982d978c302522a5f960861aca45b452f2cec068cfe0d50adb2` | 0 |
| xrpl/transaction/confidential_mpt_send.go | 6099 | `2f4ce6ff4901d94fb159cbcf605795757f0c257e6b103ff542b04e08c64d5644` | 0 |
| xrpl/transaction/credential_accept.go | 1600 | `416207914dd5c92682199067055fdc14e1c5abde02e2ff27bf86ca60e7b72349` | 0 |
| xrpl/transaction/credential_create.go | 2788 | `7f97f44977322f6ecbbef61e065f998a366d4e557367fe35fcddae7dfc10765c` | 0 |
| xrpl/transaction/credential_delete.go | 2053 | `1050c2b6b57ee77d05a68077a1ba1b2137ec49909980a632304c72463260b823` | 0 |
| xrpl/transaction/delegate_set.go | 4818 | `99b3483d1f17a4676b5aac462604a988a952fab215335b55ec0fe3b29663d7f0` | 0 |
| xrpl/transaction/deposit_preauth.go | 4303 | `40fafd0f8ca5c525dbd02744b2930b695bdcfcd33a4ba29be6c2e67a85966356` | 0 |
| xrpl/transaction/did_delete.go | 903 | `bd312e6e4623e0d1a8822a4476752bd55ef8009bb3a762522eb2fa07024668ec` | 0 |
| xrpl/transaction/did_set.go | 1539 | `11c69196097eee22a678ca8a3a22e2cd7a6e58a65c6080e791cb859278c03d24` | 0 |
| xrpl/transaction/errors.go | 66837 | `283dddbc64e9f873fe554ff4d782a8bd5d38cf879d3e7bc76e975da52f733fba` | 0 |
| xrpl/transaction/escrow_cancel.go | 1584 | `c130cd84e21778f92f4a1a9bc8f3b009eeed4fc9e4f09a180c9c272f06f7efaa` | 0 |
| xrpl/transaction/escrow_create.go | 4397 | `f466933817c4ba462a997673a360278ecb1fbfa5ba0f5fd959c6c2861fb9fbe4` | 0 |
| xrpl/transaction/escrow_finish.go | 3068 | `9816ddf6a3bd1eea1fc7991907d4632a687ea709532831bbf0da93bdca56a553` | 0 |
| xrpl/transaction/flat_tx.go | 2625 | `e297195a9d3f6586aba3ec441d875f832562bde33819ee6e0c417866676870f4` | 0 |
| xrpl/transaction/integration/errors.go | 260 | `465441393e9e22bd357cef9afdc8b411549f08971ce54d583cd3fe1d8b4f1880` | 0 |
| xrpl/transaction/loan_broker_cover_clawback.go | 3112 | `49c670bbe3eea4da0918057f423196a175d2c8646c8e6ade0cbc28555d6379ec` | 0 |
| xrpl/transaction/loan_broker_cover_deposit.go | 1863 | `7e9707efd739d900b27aa78b402693195902114fb2a929c704c6cc833a3dc693` | 0 |
| xrpl/transaction/loan_broker_cover_withdraw.go | 2964 | `1ce04f30b67b4ce3dfd1392003d42a25715c9430e0a7e4554f9277469411c841` | 0 |
| xrpl/transaction/loan_broker_delete.go | 1371 | `9be45752db625fa0a6207922f22c0aa97798e562810e5b4121b3f95c8ea27201` | 0 |
| xrpl/transaction/loan_broker_set.go | 5479 | `883df98a0dcde31a088160d0b161741677cd9ca090c4c76e7a4ec9357278518f` | 0 |
| xrpl/transaction/loan_delete.go | 1238 | `eb7684cd25efe5c719cc2b7e64d827377ce10427a55867daed29ff3c6d368b9e` | 0 |
| xrpl/transaction/loan_manage.go | 2328 | `10e9986e7e1d067fde6ebffe0667b78adf84791f705cb2fb404e4b672429633f` | 0 |
| xrpl/transaction/loan_pay.go | 2998 | `c9ead561ba772cf80a6a4e23802ae0304747a08e0396772e4fe3e42c1c01b6bf` | 0 |
| xrpl/transaction/loan_set.go | 10218 | `98ab27d707bcec24f035a898fdf32db28e78ce1d989483e2f0160e99770d8401` | 0 |
| xrpl/transaction/metadata.go | 2665 | `8a2cdf7c09d87796e80d277d1aa5c216b61b5bad9e77b219d5ed90d2dd374b3b` | 0 |
| xrpl/transaction/metadata_builder.go | 3412 | `3f76c2c49010f7b70bbf3744c50c442c0b983b2b33c45be7054ac7b17cce2d84` | 0 |
| xrpl/transaction/mptoken_authorize.go | 2916 | `ea4c20ba6f8d7e4fa0503a342b0bd11084bc09400e0e2a0f9517ce6f0ca58995` | 0 |
| xrpl/transaction/mptoken_issuance_create.go | 10841 | `dbe278ca4f60f1af76d0bab7f76a3d499387135ee82376851f4c9eb266be95ea` | 0 |
| xrpl/transaction/mptoken_issuance_destroy.go | 1609 | `acf52426194c134a9d08c2be1e28bc36bdfd8e463d8eebdc55653a68381efb81` | 0 |
| xrpl/transaction/mptoken_issuance_set.go | 9654 | `f25dfae9814c2df2464aff490fcf7abffb7e01c941d6e215b5200b2ee274ce42` | 0 |
| xrpl/transaction/nftoken_accept_offer.go | 3560 | `76b5c7da740fe0da2493a07a3186ccd06decce93b0c18e2c39681dc00d2d0195` | 0 |
| xrpl/transaction/nftoken_burn.go | 2383 | `10d3fddb3f8691cf0668ba14c2f41377800a07e8dd345232ab9695d67226c58f` | 0 |
| xrpl/transaction/nftoken_cancel_offer.go | 2019 | `fa208f4b88654257e55b4821eb004faec5f5e03836113fc875beaf499fd3ce86` | 0 |
| xrpl/transaction/nftoken_create_offer.go | 5048 | `b5024b954d05420172facb2a688e9b5dfebeb8f32e2dffa28612f055d7df0e22` | 0 |
| xrpl/transaction/nftoken_mint.go | 8363 | `8fccdca9e61df298f2b06159d3453830ff4b1db2f959466a116c90741ef5d2d9` | 0 |
| xrpl/transaction/nftoken_modify.go | 3159 | `7843f6b60903ea9e9b2c6456d0314ca6b51b572b5cc6bdb4655ca84d5779aae2` | 0 |
| xrpl/transaction/offer_cancel.go | 1206 | `9589c03b8a4ad6c2e814807b67b5ddec215b1d1624aa2245d96bcfe63f976af3` | 0 |
| xrpl/transaction/offer_create.go | 4987 | `fda2cd51ca05f026b99caf1162153b9120d6c09742aa8f2f390957dc5babc42a` | 0 |
| xrpl/transaction/oracle_delete.go | 898 | `878d56d957821d8981088dfb90eb4514d7fa9d813f443b7363e13410b9fbd81e` | 0 |
| xrpl/transaction/oracle_set.go | 4407 | `782a5e72b0dbc86df755e9855ab18cde2d72f866471d738f948aa3ee4fc37dce` | 0 |
| xrpl/transaction/path_step.go | 732 | `0a96266120eb4b27079ba5e4d89ddd0fe5e051ed36e66fcb38dff9aa2a63dae1` | 0 |
| xrpl/transaction/payment.go | 9190 | `b5fd1d50e1ca68e2d7b3b086b5cdbf75b032049a96fad566038ee2e556163fa2` | 0 |
| xrpl/transaction/payment_channel_claim.go | 7256 | `78cd3ff54bc8c5ac057c5f5272ba5db6f73341b3735c2c157f9723d7e2b256a0` | 0 |
| xrpl/transaction/payment_channel_create.go | 3448 | `ac2cc3e5abf279242a7b6afba1a86db11c66edd054955c5010d74694551f0027` | 0 |
| xrpl/transaction/payment_channel_fund.go | 2572 | `aca60af99ac1be225cae124323a0322ac404ce84bd90fce28f7b92e36ed04d10` | 0 |
| xrpl/transaction/permissioned_domain_delete.go | 1417 | `5c17de938bf6564ad2d07911eca05b5aad8075adde094c4cf16551e4cb74d7c4` | 0 |
| xrpl/transaction/permissioned_domain_set.go | 1840 | `b73fe8785e24386db3318d67fd3550305312956ad043f4d301fc67f3c3bf4e19` | 0 |
| xrpl/transaction/results.go | 21929 | `625d5ef756a131442cb68d380a361a1a0d15b43b23387f16cbc138c714a26c7a` | 0 |
| xrpl/transaction/set_regular_key.go | 2149 | `64c0c5eda16db48632953778eeb3a6f0b6fbcf9a3cd2d62b8e96649978d825e9` | 0 |
| xrpl/transaction/signer_list_set.go | 5422 | `29f0f0431236a1b4b24a21fbc423d96d795596517dc44c669644a5fc6c7a6d60` | 0 |
| xrpl/transaction/sponsor.go | 9049 | `a1634c7797522aa71a8c8368fa2030cc17442ab12262fc4406cb094687661994` | 0 |
| xrpl/transaction/sponsorship_set.go | 7175 | `123d94002135bebfc25b2dedc58c6e09cb24be5675364bdeea88cd105dd88c2e` | 0 |
| xrpl/transaction/sponsorship_transfer.go | 3707 | `180d2506f40815e399e6c97d57999811a769591a29462fff7ac6087298f500ed` | 0 |
| xrpl/transaction/ticket_create.go | 1813 | `c2f61b605e8b9c4d31a59d796a7520ff30e817f2e0443efa6aee60ce628d44a5` | 0 |
| xrpl/transaction/trust_set.go | 4744 | `4ce74b614dc2a18adeaf5a06b673f54ec8f5f89dc1fa722a9b2aaf6f03fd4b4b` | 0 |
| xrpl/transaction/tx.go | 9544 | `de802cd1f01ab80984d6b169ad1213c62c213f28d93cc0260eb52a025b6284d3` | 0 |
| xrpl/transaction/tx_type.go | 6197 | `e1a4857cdaecf84ff0c0922c85bddd28f0bf4359b3d2e46258324d1f6689e6e0` | 0 |
| xrpl/transaction/types/address.go | 274 | `a3db39cb84bbc6159457dc58fb8c9cba7e541fc2e73536513395a80e326f7bf5` | 0 |
| xrpl/transaction/types/asset_scale.go | 196 | `d4e615fb410db974b3d23d41d61b448c308fe924a2f305990c5117dff6030eed` | 0 |
| xrpl/transaction/types/authorize_credential.go | 808 | `a27f070cee853921b4bed4b4d07acacb72ab3cca7388fd249bffa158a6f1b6bf` | 0 |
| xrpl/transaction/types/authorize_credential_list.go | 1063 | `7cee0714fc4392ace748da3d616fb6e6b3e8329f38fd38adf90199e4a7eb6e63` | 0 |
| xrpl/transaction/types/authorize_credentials.go | 1313 | `be64e8cf1d79b5d3e6f30f82ce80f6cfa150ba4251eb72081d166fdcaf7c58bc` | 0 |
| xrpl/transaction/types/batch_id.go | 127 | `d0d9ea78afe3501eb5fb5d192fda83457da890edbd2f3b3c6bc3dce3c7040787` | 0 |
| xrpl/transaction/types/batch_signer.go | 1798 | `6c90dfce8a865dbf81aae622f23e80baf82450f7ed587aa4ebceef837ab0e36c` | 0 |
| xrpl/transaction/types/cover_rate.go | 435 | `7b59d3644dfbc8bd30611e66860933f612b18270fff5778d87c8ac4f3f754e58` | 0 |
| xrpl/transaction/types/credential.go | 567 | `cb30a5e4cb85b362be5b7842c209380eaf3896dfa5b7c7d74383957841d8f784` | 0 |
| xrpl/transaction/types/credential_ids.go | 1119 | `79d910ec564f94d6152cd37b8c66be828eb8da3de27d7d30aa19948cd0ff72c5` | 0 |
| xrpl/transaction/types/credential_type.go | 1058 | `9946b7c6ea702440a02b235187a48fe3d18a55c5b980b4c6edd8682f15e02e31` | 0 |
| xrpl/transaction/types/currency_amount.go | 7022 | `f515d2ce70e1ff12231c5c73b4a03cd215d86dfcaabf88bc07c0c92581f8e51e` | 0 |
| xrpl/transaction/types/data.go | 351 | `0c4bb355bb1544cb65ee9a792f90571c94d882e686bd53ffee578c95c8be0c2a` | 0 |
| xrpl/transaction/types/destination_tag.go | 219 | `db3f670d83f6ea04d583552bd84e642fb25a64615d570c81d5233e040a50d5eb` | 0 |
| xrpl/transaction/types/domain.go | 228 | `d128f12779e94dd1b8d46226be97acde1002f2a5fbff252bef62e2c8b6db4113` | 0 |
| xrpl/transaction/types/domain_id.go | 143 | `2672b8ff897ef67d63b3f178be168b9f05f77f8c82f78fb1fa063bc3d4523814` | 0 |
| xrpl/transaction/types/email_hash.go | 265 | `3d437ccf7ec456fc585f2d35135059696a5c28016454b36f9679b9f1feeb3c6c` | 0 |
| xrpl/transaction/types/encryption_key.go | 231 | `d27bbc3f5ef3f7dc6fc4d7c1a6e229e742550ea276d98908fbd696fd63506b64` | 0 |
| xrpl/transaction/types/errors.go | 9847 | `15eed09743e69ab3e56a126c1037307258e9db2043ab076f5371d8cff415eabe` | 0 |
| xrpl/transaction/types/expiration.go | 194 | `e7d0649398bcf6c7f63b6ea3003db15aaf134ca2c2da19936bf7fcb03fa33f00` | 0 |
| xrpl/transaction/types/flags.go | 773 | `878b3c572432d6159fab8ec67d90058c9d32823607b98fde06a65b6244bcb116` | 0 |
| xrpl/transaction/types/grace_period.go | 383 | `8e3fd63041464f430920bdb86f7a7785f3cca5b040e51a5166059acda6e0a13d` | 0 |
| xrpl/transaction/types/hash128.go | 239 | `9b01a94fe00ece073f8575a41fcb1cd25eff6ded3a51f9111195205deb722522` | 0 |
| xrpl/transaction/types/hash192.go | 239 | `550360200c9cfd05f45cfb5a43ad8be007bc207e9e16c4db1be6810c7d19d0ea` | 0 |
| xrpl/transaction/types/hash256.go | 239 | `aeea2668eb5e395820879426e828c3bd9418e18470013fd03251af724e916e4f` | 0 |
| xrpl/transaction/types/hex_blob.go | 261 | `f3477ba47d2a1380b69eef233e28a6c2b6ae300f20d2bae5b9dc065538a4b700` | 0 |
| xrpl/transaction/types/holder.go | 280 | `1a1c39241559f869197d599f41978af1d7eb8f80fbb060d2679d3fc0b95cd37e` | 0 |
| xrpl/transaction/types/immutable_flags.go | 170 | `b7829879a353dfaa5e5af35bb37d2a2ee7c8ff5197f10902e9c0831e16d4b206` | 0 |
| xrpl/transaction/types/interest_rate.go | 411 | `293f2b416f8f185c0e5822a8009a55710b1d43d1f5d311379c3bcb044b32dc06` | 0 |
| xrpl/transaction/types/issued_currency.go | 487 | `6a2a39f85b798e27326c3711ba8613575c09000b7b041cd83625baec4c7fdab7` | 0 |
| xrpl/transaction/types/loan_broker_id.go | 383 | `7dbd82692b370f3ce2571b6a9f5897748ae423e3c77fab100c3d9072bc0bee79` | 0 |
| xrpl/transaction/types/memo.go | 1006 | `da02ddd9ff5dcda588abb89e0f45a5aca5329003bae5a5e03bbd7c97a1cfa035` | 0 |
| xrpl/transaction/types/message_key.go | 189 | `b141e680f36120f1672adbc163489863386355e541a0918219c9391af4c19b39` | 0 |
| xrpl/transaction/types/mpt_amount.go | 1934 | `5b5fb6e983332563a7f2ca57726fa88830ea84292fe4189356b88bf37ad0dfb7` | 0 |
| xrpl/transaction/types/mpt_issuance_id.go | 157 | `75a6e9fe7c0a2d685d2855921e1600ee4339662dfa65dd6a300a2d1b5901aebc` | 0 |
| xrpl/transaction/types/mptoken_metadata.go | 15719 | `82f39b462e197b27beaa7db13bb2873c5ffe69bd315bf7b927be54b3257f1888` | 0 |
| xrpl/transaction/types/nftoken.go | 189 | `95b940ad020bfbda814a32575c373b062592bb7e4ecd83985475bfb06a4f5795` | 0 |
| xrpl/transaction/types/nftoken_id.go | 250 | `2552a90d867e49f51d35cfc9a32fb38755fd0f02d5ff65f8fd9f353e12553e0f` | 0 |
| xrpl/transaction/types/nftoken_minter.go | 308 | `b178bc0109b8ad2c32af5b9513b372f44e1878f948b86942646d21ae1085790d` | 0 |
| xrpl/transaction/types/nftoken_uri.go | 259 | `7dda76f9070b768a6e0520636be13c5012eb8aae895eabf5c2d6970d441ddabe` | 0 |
| xrpl/transaction/types/offer_id.go | 128 | `602bf1c2b35e2fb1df38e642b6f5624c0d188186e29585107e443f8450f22c87` | 0 |
| xrpl/transaction/types/owner_count.go | 358 | `ab5762034cf200630ec6b0e165cbf33b22abe3912db1605ab3380afa30663901` | 0 |
| xrpl/transaction/types/payment_interval.go | 405 | `bbda4c6985a489bb287d8c2ac00b95777e48b6202bd4e20136355ef1bf362306` | 0 |
| xrpl/transaction/types/payment_total.go | 364 | `997deb97422e6a8338c5804c0e69820a5b0edb5ad42857e78c2f248898d3df85` | 0 |
| xrpl/transaction/types/permission.go | 1082 | `ed5c75a13faf9e13b6a537a3f82e9d408dccb767e29d4b54425e61896991b364` | 0 |
| xrpl/transaction/types/previous_payment_due_date.go | 374 | `7d99cd32477ba484cdba4349a602aaa54dc3355493a75bac7770f845304a7a29` | 0 |
| xrpl/transaction/types/raw_tx.go | 2371 | `d912db8220b27c7e4ddbe3292af6689583ebb9e8cbbc9475ac91e4ed423b448d` | 0 |
| xrpl/transaction/types/signer.go | 1117 | `c41ebe5b507defe2369f82d83457de225dad6267b9dafba7324d2c93a926ddf8` | 0 |
| xrpl/transaction/types/sponsor_signature.go | 1318 | `f54dd6ce5f0afd33868406c1e4f095833b17670ea54e4f25595b6f38e057039e` | 0 |
| xrpl/transaction/types/ticksize.go | 413 | `190cda28e9d0dd32c456a04402f45d2c6283adf695986171681423c69db6cc42` | 0 |
| xrpl/transaction/types/transfer_fee.go | 186 | `989f634c26e0e68dd2697d18df991a04e608c043a89e4174b108dc7c917b43a0` | 0 |
| xrpl/transaction/types/transfer_rate.go | 406 | `efe4710416b17a69b7f011f0c0e8fde7985244ce016e0d02d85ff201cae30c91` | 0 |
| xrpl/transaction/types/vault_kind.go | 336 | `24c9faf400d4f1004af965632a93736c0618aae70ca24abacc06d8aa5794761d` | 0 |
| xrpl/transaction/types/vault_withdrawal_policy.go | 451 | `01253cd60c712b5fd69d84c70c7f7afa120968457f7a27ca72079654fbd41523` | 0 |
| xrpl/transaction/types/wallet_locator.go | 314 | `c0b3ce9ce571395ca3c67655d60ac7e7b3d142383ad0db8ce2a5e33db95c482b` | 0 |
| xrpl/transaction/types/wallet_size.go | 267 | `fd3bb92f099aabac30d152849ffa873ec1616f173078e083e5ab7e8db48f77ff` | 0 |
| xrpl/transaction/types/xchain_bridge.go | 2039 | `2f0989b630a2fe376f59f8fb0d9330554c074712fb626b9f8e8222a3e06e1f25` | 0 |
| xrpl/transaction/types/xrpl_number.go | 415 | `d48166a6e9f78c6fb9afd52fea00547d53ba815454a5519836ead8a2121a4b38` | 0 |
| xrpl/transaction/validations_commons.go | 4009 | `b5fd92e592efb8e02dd5531d5018be82eaa7f8f20a7d22ddb0dfeb16f628fbcb` | 0 |
| xrpl/transaction/validations_confidential_objects.go | 4307 | `68acfb8bd5ed2a00f1260e0ee19639173989034d4fef44f2714a9e8e536316bd` | 0 |
| xrpl/transaction/validations_xrpl_objects.go | 11205 | `e98bdf80c82dadee99daa3e54b2be6af32af58b78fec18670691b3e406a2ab29` | 0 |
| xrpl/transaction/vault_clawback.go | 2716 | `c595089697979f2083546e44dc8de8d9adc61979a56f7ea4f958427823045994` | 0 |
| xrpl/transaction/vault_create.go | 6792 | `a46c2b2726a7562430dacf06048d97242ce3114744cc5c9ac274a7d45bbde874` | 0 |
| xrpl/transaction/vault_delete.go | 1927 | `b5c9b82d79955e695e714b8396b2cab6fae9161027511fc614404105e18e9815` | 0 |
| xrpl/transaction/vault_deposit.go | 1620 | `412e29dc6c5648acb74308e312fb18fcef8f874488ef0233414c521587581b1a` | 0 |
| xrpl/transaction/vault_set.go | 2656 | `f24cc1a9ad072d2547c84de8a2246d9b502ecdf68075bc31643cecfbb3e9f749` | 0 |
| xrpl/transaction/vault_withdraw.go | 2674 | `f11f0161532166a550b36a1aca9ef2c2dc8ff6fae2fc171906e64c95466b99b2` | 0 |
| xrpl/transaction/xchain_account_create_commit.go | 2789 | `056b10a694c2e7fb1b97de91bf2c2a4fce521fe10c46a52f3094e4a578a6b881` | 0 |
| xrpl/transaction/xchain_add_account_create_attestation.go | 5766 | `6adb6f9308d27d3a849aa892ed71f13ae394359da556df5a4d9d0177f4bd1603` | 0 |
| xrpl/transaction/xchain_add_claim_attestation.go | 6141 | `a012790b75390d8c5f37ac52cdd169fe03272c8c1113214d51c527eccfc60e30` | 0 |
| xrpl/transaction/xchain_claim.go | 3559 | `5fa4385518e20e42a56a6c071734b6714ee40221a7fc88fb0abf4e839662a20a` | 0 |
| xrpl/transaction/xchain_commit.go | 3053 | `b4ea0ac15b89fe27c0204b8863d610d7fe21d0b4a45ad309142d2e3bb326633c` | 0 |
| xrpl/transaction/xchain_create_bridge.go | 2994 | `fb1fef84c03608913a6b514ab35bef3360af460df7a99dd268e4d9e91f196bce` | 0 |
| xrpl/transaction/xchain_create_claim_id.go | 2678 | `9a259785791d8cc7620ad3c64c8fc90c18dd85b8d2d47c9b4ba63b520c95eb09` | 0 |
| xrpl/transaction/xchain_modify_bridge.go | 3113 | `64ad5170cc16f1bb2533369c00bd39d20b8fda101e6275ba6b0a2010fddc1387` | 0 |
| xrpl/wallet/authorize_channel.go | 897 | `8e499a298307b8bd07860df56f589d7b0c066ac4edab9b3d3d880d6019066faf` | 0 |
| xrpl/wallet/batch.go | 5414 | `e2cdc28ec7101e134387989113a376b1bfcedf4b697048259a69616137af9f59` | 0 |
| xrpl/wallet/counterparty_signer.go | 7470 | `a84604b5d33ece10f22b0607613f5e7c770aea1357ed6058c7a77439d8d18c15` | 0 |
| xrpl/wallet/errors.go | 4065 | `b98db341481bc67b81db786c6911ea9691a668de71eb49b7910046cb4e8cda3f` | 0 |
| xrpl/wallet/sponsor_signer.go | 10150 | `f04a62c2a778d2969cb82a9b4954b45b756395f62b082b6bddf689acb833490c` | 0 |
| xrpl/wallet/types/batch_account.go | 544 | `8ceb965e8a89a625e14bfb3714bd18f4821aae362bdf302a939ca90f3113e2fe` | 0 |
| xrpl/wallet/types/batch_signable.go | 4212 | `63bb1675a310154359627d37946f36ef77c1d070d2f3bb698d68d5bdb24aac39` | 0 |
| xrpl/wallet/types/errors.go | 2226 | `fa0422f31a67abeaab3e716d95ae1cb0e5c3c25dac7ecbe57f7e671edeba8bf9` | 0 |
| xrpl/wallet/wallet.go | 8537 | `8f808f72c4aa608f9b36cfb347c4f167c35ad962d3573a45c78fd14ee94995d6` | 0 |
| xrpl/websocket/client.go | 39962 | `07ed0330212cf410c407c8878486117ded94c08c9ee1f6beac3389144ad53dde` | 0 |
| xrpl/websocket/config.go | 4576 | `b70492447684811e4b9e3ff07ff1ad495b187a442bb26637de575888430b59bf` | 0 |
| xrpl/websocket/connection.go | 9885 | `c05e48e5d4ef110a58db7567ec98ef66a60c054460d30db268b8b5ba1518ffdb` | 0 |
| xrpl/websocket/errors.go | 15415 | `3c7949fa9321fc21dc9636bee64435dcca519fe27e1347f99e13859ec7e16272` | 0 |
| xrpl/websocket/interfaces/request.go | 332 | `50edc3858e55a9cb56499978b7c94b079de1373f5b224d358be8bf245d2d7da1` | 0 |
| xrpl/websocket/network_identity.go | 4259 | `c1962b7b53c05d9ce0dbc1974db7cf210f7e6ddbfa727c03c6ff3bc51effe967` | 0 |
| xrpl/websocket/queries.go | 16000 | `cbec536b85d2964a228d62230dfb262e472258ee9da64146f9c0c1020e6a95ff` | 0 |
| xrpl/websocket/response.go | 1736 | `fed30591c5ec4ed4c427e6b854e01831b64d0e50d49b39955004ea9497b13c99` | 0 |
| xrpl/websocket/sponsorship.go | 1356 | `7905477da93ab9705d5bd59181fe39f5b4e884b78a66626f75747cf35a15e289` | 0 |
| xrpl/websocket/streams.go | 8257 | `28fffb946b2ec328fec5dfe14f0a9ab93050e3d223ba8da246218c42b2433142` | 0 |
| xrpl/websocket/subscription.go | 891 | `38960bf2acf7ddeac364f69b56e7bf80924193736686a2cc4c4ed06936b4c18a` | 0 |
| xrpl/websocket/types/client_options.go | 733 | `0f5e9ee914f786c87b10642ddfe7f21e9f1114019e1601d3c1c6c87959eabb71` | 0 |
| xrpl/websocket/types/message.go | 788 | `835676b893107c5478ee19855d1b4a3e6ad54e5f5b4448d7d98012a762a4902c` | 0 |
