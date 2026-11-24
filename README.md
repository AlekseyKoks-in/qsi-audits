# Cryptographic inventories of open-source code, signed and reproducible

61 audit bundles over **53 codebases**: a machine-readable inventory of every cryptographic
primitive the scanner found, what it is used for, and what a quantum computer does to it. Across those codebases
**4,045 inventory rows**, of which **1,991 fall to Shor's algorithm**, **28 are post-quantum** and
**13 are hybrid** (post-quantum combined with classical), from **30,744 parsed files**. Those last two
are kept apart on purpose: write-ups of mine dated before 2026-10-30 quote a single "29 post-quantum" that was
28+13-style addition of the two, which is why one number appeared in two different places.

### What those rows rest on

A single "inventory rows" total mixes evidence of very different strength, so here it is split. This is the one
table to read before quoting any other number in this repository.

| what the row rests on | rows | Shor-breakable |
|---|---:|---:|
| a line of source code | 2,286 | 1,494 |
| name of a dependency in a manifest | 869 | 0 |
| name of a source file (low confidence) | 348 | 155 |
| a deployed smart contract | 121 | 3 |
| OpenPGP key committed to the repository | 119 | 119 |
| the chain a wallet supports | 114 | 114 |
| a certificate or key file | 101 | 53 |
| other | 87 | 53 |

Two things in that table are worth saying out loud rather than leaving for a careful reader to notice.

**155 of the 1,991 Shor-breakable rows rest on the name of a source file**, not on a line of
code. That signal exists because `trezor-firmware/crypto/pbkdf2.c` *defines* PBKDF2 instead of calling it, so no
call-site pattern reaches it and the inventory missed it entirely — a file named after an algorithm is the project
telling you what is in it. It is still weaker evidence than a call, the reports mark it `confidence: low`, and a
headline figure silently promotes it to the same standing as the rest. Now it does not.

**119 rows are cryptography the projects did not write**: OpenPGP primary keys and subkeys committed to the
repositories — maintainers' release-signing keys, in `bitbox02-firmware`, `jade`, `libwally-core`, `monero`, `seedsigner`, `zcash-android-wallet-sdk`, `zcash-swift-wallet-sdk`, `zebra`. They belong in an
inventory, because a quantum computer forges a release signature as readily as a transaction one, but a reader who
saw only the Shor total would take them for implemented cryptography. Every one carries `usage: OpenPGP primary
key` or `OpenPGP subkey`, so one filter removes them from any figure here.

The 869 manifest rows carry no quantum status at all —
a dependency's name is not an algorithm — which is why they add to the row count and nothing to the Shor count.

Every bundle is pinned to an upstream commit, carries an Ed25519 signature and a CycloneDX CBOM, and was produced
before anyone paid for it. The point of publishing them is that you do not have to believe any of the numbers
above.

## Check it yourself

No dependencies, no network, nothing to install:

```
python3 verify.py --self-test     # test the verifier before trusting what it says
python3 verify.py                 # verify all 61 bundles
python3 verify.py audits/secp256k1
```

`verify.py` re-hashes every file named in each signature, verifies the Ed25519 signature over the signed payload,
and checks that the key which signed each bundle is the one in `PUBLIC-KEY.pem` at the root — so substituting a
key in one bundle does not go unnoticed. Ed25519 is implemented twice in that file, once self-contained and once
through the `cryptography` package when it is installed, and **both must agree**; `--self-test` demonstrates that
a real signature passes, that the two implementations agree, and that flipping a single byte of the payload, the
signature or a file is caught.

Bundles signed from 13 November 2026 on also carry a post-quantum co-signature: ML-DSA-65 (FIPS 204) over the same
payload, with the payload's schema as the context string, by a key the Ed25519-signed payload names (`pq_key_id`).
`verify.py` checks it as well, again twice where it can: with an ML-DSA-65 verifier written into the file (pure
Python, no dependencies) and with `cryptography` 48 or later when that is installed with OpenSSL 3.5. A payload that
names a key whose signature is missing, a signature for another context, a key other than the named one or a
`public_key_mldsa.pem` that differs from it all fail. `--self-test` runs the built-in verifier on five of NIST's own
ML-DSA-65 test vectors from the ACVP server (`mldsa65-kat.json`: one valid signature, and ones with a modified
`z`, hint, commitment and message), and the full set of NIST's ML-DSA-65 verification vectors (30) gives the
expected answer. Since the re-issue of 22 November (below) every bundle here carries it except `audits/lottery-demo` and `audits/nitro`,
signed before it existed, which pass on Ed25519 as before. The publisher ML-DSA-65 key is
`PUBLIC-KEY-MLDSA.pem` at the root, and a bundle co-signed by any other key fails.

On Windows, Git for Windows turns LF into CRLF on checkout by default (`core.autocrlf`). The signatures are over
the exact bytes, so this repository's `.gitattributes` switches that off for every file; a clone made before it
existed, or with the setting forced, has CRLF line endings, and `verify.py` then names the cause instead of
reporting a bare hash mismatch. Clone again, or `git clone -c core.autocrlf=false`.

Signing key `5b3cf9c9bd0fa544`, fingerprint
`5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e`; ML-DSA-65 key `dbd4e297b3213d1d`, fingerprint
`dbd4e297b3213d1d7577a565e76de14cc5ad0e409f1dc68291c67266fc95066a`.

## What BIP-360 and BIP-361 require of wallet code, and what is actually there

Read from `bitcoin/bips` on 2026-10-29 rather than from secondary write-ups, which disagree even about the name.
**BIP-360 is now titled Pay-to-Merkle-Root (P2MR)**, version 0.12.1, Status: Draft: P2TR with the key-path spend
removed, defending against long exposure only, and saying in terms that post-quantum signatures are not in it and
are deferred to "a separate proposal … upon further research" that is not yet written. **BIP-361, Post Quantum
Migration and Legacy Signature Sunset** (Draft, Informational, assigned 2026-02-11) "follows the implementation
of any post-quantum (PQ) output type", and at its Phase A non-upgraded wallets "can no longer receive from any
other wallets".

Both therefore turn on wallets being upgraded, and neither says what that means in code. `readiness.py` answers
the part that is measurable from these bundles:

```
python3 readiness.py          # the self-custody slice
python3 readiness.py --all    # every audited codebase
python3 readiness.py --json
```

Schnorr/BIP-340 primitives are present in 8 of the 10 self-custody codebases, and **exactly 1 of
the ten holds any post-quantum primitive** — Trezor, with ML-DSA and SLH-DSA, the latter in its boot header beside Ed25519.
The zeros are the interesting part and are not a statement about what those wallets can do. `seedsigner`
delegates to a hash-locked `embit` release; `rust-bitcoin` holds taproot types while the Schnorr signatures live
in `rust-secp256k1`; and **`bdk` is not a wallet at all** — at the audited commit `bitcoindevkit/bdk` is the
chain and indexer layer, with no wallet, keys, signer or descriptor crate in the tree. The wallet is the separate
repository `bitcoindevkit/bdk_wallet`, audited here as `bdk-wallet` on 2026-10-29: 10 inventory rows, 7 of them
ECDSA, named in `src/wallet/signer.rs`, `src/keys/mod.rs` and the descriptor modules — and no Schnorr there
either, so for BDK the signing primitive sits two repositories away from the wallet.

**The same question, asked of SeedSigner, produced the sharpest number in this repository.** Its own tree is 7
inventory rows with 1 Shor-breakable, which is correct — and its signing path is `embit`, pinned as
`embit==0.8.0` with a sha256 hash lock in `requirements.txt`, verified at the audited commit. `embit` is audited
here too, at `2b375a33bd89`: **77 inventory rows, 55 of them Shor-breakable**, including its own
pinned `secp256k1-zkp` submodule, and **7 Schnorr (BIP-340) rows** — so SeedSigner does hold taproot primitives,
one repository away. **1 versus 55 is the cost of auditing the repository with the wallet's name on it.**
`readiness.py` now resolves each zero to the audited destination and prints its measured figures, so the chain
`bdk` → `bdk_wallet` → `rust-secp256k1` and `seedsigner` → `embit` is traceable rather than asserted.

**An earlier version of this page said `bdk` "delegates signing to rust-bitcoin and rust-secp256k1".** That was
the right direction attached to the wrong repository, and it was corrected by auditing the wallet rather than by
rewording the sentence. It is recorded here because a page arguing that thin results deserve suspicion has no
business hiding one of its own. **Readiness for a consensus change cannot be read off a single repository** — which is the same defect that once made a Bitcoin
signer measure 13 inventory rows instead of 98. Presence of a primitive is necessary and not sufficient: P2MR
also needs address encoding, descriptors and PSBT support. The full argument, with the primary quotations, is in
`reports/BIP-360-361-READINESS-2026-10-29.md`.

## Correction, 2026-10-29: benchmark files were counted as deployed exposure

Triaging `embit` surfaced a defect in the runner, not in any audited project. The test-and-example filter checked
*directories* for benchmark patterns but had **no rule for benchmark file names**, and C and Rust put `bench.h`
and `bench_sign.c` directly in `src/` — which is exactly what libsecp256k1 and secp256k1-zkp do. Across the
portfolio **61 inventory rows in nine codebases came from `bench*` files**: a timing harness counted as shipped
cryptography. The rule is fixed, deliberately strict past the whole word so `benchmarking_utils.rs` stays
production code, and covered by eleven new tests.

Five codebases were re-audited at their original commits with their analyst decisions preserved:

| codebase | rows before | after | Shor before | after | why |
|---|---:|---:|---:|---:|---|
| `secp256k1` | 38 | **32** | 38 | **32** | six `bench*.c` rows removed |
| `rust-secp256k1` | 36 | **32** | 36 | **32** | four removed |
| `libwally-core` | 81 | **77** | 60 | **56** | four removed |
| `embit` | 89 | **77** | 67 | **55** | twelve removed |
| `jade` | 93 | **110** | 66 | **74** | fourteen removed, and 183 of Jade's own bootloader, pinserver and tools files read for the first time |

**`bitcoin-core/secp256k1` is therefore 32 of 32, not 38 of 38.** The ratio and the argument are untouched —
still every row, still zero post-quantum — and the count is smaller and truer. Figures quoted in letters and
write-ups dated before 2026-10-29 use the earlier numbers, including a ten-codebase slice of 629 rows and 440
Shor-breakable. The same ten measured 632 and 434 after the benchmark fix — the small net difference being Jade's
own code arriving as the benchmarks left — then 695 and 448 once `bitbox02-firmware` was
read to 2,645 files instead of 721. Every letter that quotes 629/440 carries a link to this
repository, so the figure is checkable here; it moved upward each time, and the reason for each move is in this
section.

**The byte-budget defect described in earlier versions of this file is now fixed.** It read: when the limit
binds, the order of dropping must prefer the project's own tree, and the report must name what it dropped.
`krux` and `bitbox02-firmware` pin large vendored dependencies — MaixPy, lvgl, optiga-trust-m, cryptoauthlib — and
with those materialised the tree exceeded the runner's total-size limit, dropping **1,749 and 556 files
respectively**, among them the projects' own source: `src/boot.py` and `src/krux/auto_shutdown.py` for Krux,
`src/rust/bitbox-aes` for BitBox02. Both halves are now done: the budget is spent on the project's own tree before
the directories a `.gitmodules` pins, the report names the files that did not fit and the ones no analyzer reads,
and it attributes the files it did read to the submodules they came from. When a project's own source is dropped
the description says so as an explicit warning rather than leaving a reader to infer it from a count.

**`bitbox02-firmware` is therefore re-audited here**, at the same commit as before. It reads
2,645 files where it previously read 721 — of 8,952 files in the tree, after setting
aside test, fuzzing, benchmark and example code and the files no analyzer reads, that is 84% of what
could be read — and the 518 that still did not fit are named in the report and are every one of them
`optiga-trust-m`'s vendored mbedtls headers. The bundle goes from 136 rows and 90
Shor-breakable to **202 and 113**. 44 of the added rows are committed OpenPGP keys rather than
implemented cryptography, which the breakdown above separates, so the honest statement of the improvement is
136 → 158 rows of cryptography this project actually contains.

**`krux` is still left at its earlier bundle**, and the reason is narrower than a size limit. Re-read at full
depth it yields 248 inventory rows — but **230 of them come from `firmware/MaixPy` and 11 from `src/krux`**, with
1,677 files still not fitting. That is a 23% sample of the tree whose composition depends on the order files are
visited, presented as an inventory of a hardware wallet. The 99-row bundle published here covers Krux's own code
and the `embit` it pins, within the budget, and answers the question a reader actually has. The full run is kept
as evidence rather than published as a measurement.

## Re-measure, 2026-11-05: every bundle again, with the current engine

Every bundle published here except `nitro` was re-audited on 5 November at its recorded commit, tree, language
and analyst decisions, with the engine as it stands after the corrections of 2 to 5 November. `nitro` keeps its
earlier bundle: its scope was never recorded, and the reconstructed one parses 1,036 files where the published
bundle parsed 1,038, so a re-run would be a different measurement presented as a correction. The portfolio now
holds **3,982 inventory rows, 1,944 Shor-breakable**, and the ten-codebase Bitcoin slice
**808 and 555** (695 and 448 before). `bitcoin-core/secp256k1` has **39 Shor-breakable rows of 40**: its ECDH
module was not recognised before. Most of the movement is the scanner learning words it lacked — ECDH on secp256k1,
BIP-340 in Rust and C, Ed25519 implementations — and some is false rows leaving. Every codebase that moved:

| codebase | rows before | after | Shor before | after | why |
|---|---:|---:|---:|---:|---|
| `agave` | 200 | **212** | 103 | **115** | references to Solana's Ed25519 verify program (`ed25519_program::id()`) |
| `bdk-wallet` | 10 | **14** | 7 | **11** | BIP-340 rows added; one test helper (`persist_test_utils.rs`) no longer counted |
| `bitbox02-firmware` | 199 | **202** | 104 | **113** | ECDH/BIP-340 rows added; false rows removed: `i2c_ecc.c` as ECDSA, LVGL `lv_os_none.c` as JWS "none" |
| `bitgo-mpc` | 91 | **93** | 66 | **68** | pattern corrections of 2026-11-02 to 2026-11-05 (ECDH/BIP-340/Ed25519 vocabulary, Jubjub traits, benchmarks) |
| `bitwarden-sdk` | 119 | **120** | 12 | **13** | pattern corrections of 2026-11-02 to 2026-11-05 (ECDH/BIP-340/Ed25519 vocabulary, Jubjub traits, benchmarks) |
| `coinbase-cb-mpc` | 103 | **108** | 88 | **93** | ECDSA/ECDH call sites; the one file fewer is a file no analyzer reads; second pass: `base_ecc_secp256k1.h` no longer an ECDSA row by file name alone (tree 182 → 181 files) |
| `embit` | 77 | **87** | 55 | **64** | ECDH and BIP-340 rows of its secp256k1-zkp and Python key code |
| `ethers-js` | 100 | **114** | 29 | **43** | pattern corrections of 2026-11-02 to 2026-11-05 (ECDH/BIP-340/Ed25519 vocabulary, Jubjub traits, benchmarks) |
| `foundry` | 103 | **100** | 16 | **17** | pattern corrections of 2026-11-02 to 2026-11-05 (ECDH/BIP-340/Ed25519 vocabulary, Jubjub traits, benchmarks) |
| `frost` | 59 | **57** | 33 | **33** | pattern corrections of 2026-11-02 to 2026-11-05 (ECDH/BIP-340/Ed25519 vocabulary, Jubjub traits, benchmarks) |
| `halo2` | 74 | **63** | 46 | **45** | `halo2_gadgets/src/ecc.rs` no longer read as ECDSA; generic field/group traits no longer Jubjub |
| `jade` | 110 | **144** | 74 | **107** | the libwally-core it pins, as above |
| `krux` | 98 | **99** | 64 | **64** | eleven `bench*.c` rows of the vendored secp256k1-zkp removed; ECDH and BIP-340 rows added |
| `librustzcash` | 156 | **147** | 23 | **26** | pattern corrections of 2026-11-02 to 2026-11-05 (ECDH/BIP-340/Ed25519 vocabulary, Jubjub traits, benchmarks) |
| `libwally-core` | 77 | **103** | 56 | **81** | the C++ wrapper `wally.hpp` and `wally_crypto.h` declarations: ECDH, ECDSA, BIP-340 |
| `monero` | 116 | **137** | 79 | **99** | the Ed25519 implementation in `external/supercop` now recognised; second pass: XSalsa20-Poly1305 (libsodium header) and AES-CFB key wrapping in `gen_ssl_cert.cpp` |
| `noir` | 73 | **71** | 9 | **9** | pattern corrections of 2026-11-02 to 2026-11-05 (ECDH/BIP-340/Ed25519 vocabulary, Jubjub traits, benchmarks) |
| `openpgpjs` | 65 | **64** | 35 | **32** | `ecc_kem.js` no longer ECDSA, `ecc_dsa.js` no longer classical DSA; second pass: Twofish (`cipher/twofish.js`) and CFB mode |
| `orchard` | 70 | **66** | 42 | **42** | pattern corrections of 2026-11-02 to 2026-11-05 (ECDH/BIP-340/Ed25519 vocabulary, Jubjub traits, benchmarks) |
| `pasta-curves` | 9 | **5** | 5 | **5** | pattern corrections of 2026-11-02 to 2026-11-05 (ECDH/BIP-340/Ed25519 vocabulary, Jubjub traits, benchmarks) |
| `rage` | 45 | **43** | 13 | **13** | pattern corrections of 2026-11-02 to 2026-11-05 (ECDH/BIP-340/Ed25519 vocabulary, Jubjub traits, benchmarks) |
| `reddsa` | 12 | **9** | 4 | **4** | pattern corrections of 2026-11-02 to 2026-11-05 (ECDH/BIP-340/Ed25519 vocabulary, Jubjub traits, benchmarks) |
| `rust-bitcoin` | 28 | **48** | 11 | **25** | BIP-340 (`XOnlyPublicKey`, taproot) and ECDSA call sites now recognised |
| `rust-secp256k1` | 32 | **49** | 32 | **48** | ECDH and BIP-340 forms of the Rust bindings now recognised (`XOnlyPublicKey`, `sign_schnorr*`) |
| `sapling-crypto` | 58 | **53** | 37 | **36** | `circuit/ecc.rs` no longer read as ECDSA; generic traits no longer Jubjub |
| `scroll` | 92 | **89** | 7 | **7** | pattern corrections of 2026-11-02 to 2026-11-05 (ECDH/BIP-340/Ed25519 vocabulary, Jubjub traits, benchmarks) |
| `secp256k1` | 32 | **40** | 32 | **39** | ECDH module (`secp256k1_ecdh`, ElligatorSwift XDH) now recognised |
| `seedsigner` | 7 | **9** | 1 | **3** | whole tree read: the release-signing OpenPGP key and BIP-340 rows (tree 166 → 373 files) |
| `tachyon` | 29 | **25** | 10 | **10** | pattern corrections of 2026-11-02 to 2026-11-05 (ECDH/BIP-340/Ed25519 vocabulary, Jubjub traits, benchmarks) |
| `trezor-firmware` | 111 | **113** | 73 | **74** | one ECDH row (`zkp_ecdsa.c`); the one file fewer is a file no analyzer reads (tree 888 → 887 files) |
| `trustwallet-wallet-core` | 355 | **396** | 254 | **294** | BIP-340 (Babylon), Ed25519 variants (Cardano, Waves) and ECDSA call sites now recognised (tree 2,105 → 2,104 files) |
| `zcash-android-wallet-sdk` | 51 | **48** | 7 | **7** | pattern corrections of 2026-11-02 to 2026-11-05 (ECDH/BIP-340/Ed25519 vocabulary, Jubjub traits, benchmarks) |
| `zcash-swift-wallet-sdk` | 46 | **43** | 3 | **3** | pattern corrections of 2026-11-02 to 2026-11-05 (ECDH/BIP-340/Ed25519 vocabulary, Jubjub traits, benchmarks) |
| `zebra` | 148 | **146** | 65 | **68** | pattern corrections of 2026-11-02 to 2026-11-05 (ECDH/BIP-340/Ed25519 vocabulary, Jubjub traits, benchmarks) |
| `zingolib` | 86 | **82** | 3 | **3** | pattern corrections of 2026-11-02 to 2026-11-05 (ECDH/BIP-340/Ed25519 vocabulary, Jubjub traits, benchmarks) |

Where the tree changed, the reason is in the row. The English twins (`*-en`) now face the same tree as their base
bundle, which for `bitbox02-firmware-en` and `trezor-firmware-en` means the whole tree instead of an older, smaller
one. The before-state of every bundle is kept, with the logs of this run, so each row above can be traced.

A second pass the same day, after the scanner's vocabulary was compared with the rule sets of three other open
scanners (Go and cloudflare/circl APIs, BouncyCastle classes, NaCl secretbox, NTRU/SABER/Twofish/Serpent/RC2/
Whirlpool entries, common MD5/SHA-1/DES spellings), re-audited all 60 bundles again. 56 did not move; the four that
did are `coinbase-cb-mpc` and its twin (one false row gone), `monero` and `openpgpjs` (two real rows each), as
the table states.

## Third pass, 2026-11-06: constants, toolchain defaults, test vectors

All 60 bundles again, after three engine changes. (1) An implementation is now recognised by the standard constants
it has to contain — a curve's prime and order, a hash's round constants — whatever its functions are called; this
adds real rows to every codebase that carries its own secp256k1, SHA-2 or Ed25519 code (`libwally-core`, `jade`,
`krux`, `embit`, `rust-secp256k1`, `rust-bitcoin`, `ethers-js` and others). (2) A Go `tls.Config` that leaves
`CurvePreferences` unset is inventoried as the hybrid X25519MLKEM768 that Go 1.24+ offers by default (`lightwalletd`,
`scroll`), at low confidence because the file does not show the Go version. (3) libsecp256k1's test vectors and test
helpers (`vectors.h`, `testutil.h`, `testrand*.h`) are test code; the first run of this pass counted them as
implementations and was corrected before publication. Totals moved from 3,924 / 1,899 to **3,988 / 1,946**,
hybrid rows from 12 to **14**. `nitro` again keeps its published bundle (different tree). Before-states and
logs are in the archive of this run.

## Re-audit, 2026-11-17: dependency advisories past the first 1,000 packages

Until 12 November the dependency check sent OSV.dev at most the first 1,000 pinned packages of a codebase, and its
coverage line said "1000 pinned packages queried" without saying that more existed. The limit is now 5,000, and
anything beyond it is named in the coverage as not checked. 9 bundles in `audits/` were re-audited on
17 November at their recorded commit, tree, language and analyst decisions; each now queries every package it pins
and carries the ML-DSA-65 co-signature.

| codebase | packages queried before | after | affected before | after | advisory findings before | after | all findings before | after |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `agave` | 1,000 | **1,970** | 60 | **133** | 55 | **240** | 111 | **305** |
| `foundry` | 1,000 | **1,566** | 8 | **26** | 2 | **4** | 19 | **53** |
| `lido-core` | 1,000 | **1,365** | 45 | **72** | 47 | **77** | 78 | **108** |
| `metamask-extension` | 1,000 | **4,643** | 10 | **56** | 1 | **96** | 7 | **104** |
| `noir` | 1,000 | **3,708** | 8 | **84** | 3 | **125** | 12 | **136** |
| `rabby` | 1,000 | **2,477** | 21 | **86** | 152 | **344** | 159 | **350** |
| `reown-appkit` | 1,000 | **3,535** | 32 | **108** | 101 | **395** | 105 | **400** |
| `scroll` | 1,000 | **2,634** | 47 | **173** | 63 | **134** | 179 | **279** |
| `signal-desktop` | 1,000 | **2,291** | 6 | **23** | 9 | **39** | 11 | **41** |

Advisory findings (`DEP-KNOWN-ADVISORY`: a pinned version that an OSV.dev advisory names) went from 433 to
**1,454** across them. All findings moved for a second reason as well: a re-audit runs the current engine, so it
includes rules added since a bundle was published (payment crediting, TON contracts and TON Connect sign-in,
stablecoin integrations). The inventory, which is what the totals on this page count, did not move except in
`metamask-extension`: one ECDH row, its `eciesjs` import (ECIES on secp256k1) in
`app/scripts/controllers/qr-sync/key-manager.ts`, recognised since JavaScript ECIES libraries were added to the
registry on 8 November, which moved the totals from 3,988 / 1,946 to
**3,989 / 1,947**; the other eight inventories are identical row for row. `agave` parses six files fewer:
the minified KaTeX bundles under `docs/static/katex/`, third-party code that the scanner sets aside since
12 November, none of which held a row. A lookup that fails on the network is now retried, three attempts, and if
it still fails the coverage says so and why; the first run of this re-audit lost the lookups of three bundles to
transient DNS failures, which is how the retry came to exist, and those three were run again. The same re-audit replaced `arc-node`, one bundle published in both studies (`studies/institutional/arc-node`, `studies/l1/arc-node`), which hit the same limit: packages queried 1,000 → **1,993**, advisory findings 30 → **37**, and the 37 own-code rows and 12 Shor-breakable the studies quote were left as they were (the correction of 19 November, below, moves them). `python3 verify.py studies/institutional/arc-node` checks it.

Still stopping at 1,000 packages, as their coverage lines say: `audits/nitro`. `nitro` keeps its published bundle
for the reason given above (its scope was never recorded, so a re-run would face a different tree).

## Correction, 2026-11-18: NIST's post-quantum signature API is not Ed25519

NIST's post-quantum standardisation adopted the NaCl/SUPERCOP API for every submission, so `crypto_sign_keypair` and
`crypto_sign_seed_keypair` name Ed25519 in libsodium, TweetNaCl and ref10, and SPHINCS+ or ML-DSA in a reference
implementation. The scanner read all of them as Ed25519, and in `trezor-vendored-crypto` that put 5
Shor-breakable Ed25519 rows into exactly the post-quantum code: `vendor/sphincsplus/ref/api.h`, `sign.c` and
`PQCgenKAT_sign.c`, and `vendor/mldsa-native/mldsa/mldsa_native.h` and `mldsa_native.c`. Such a match is now not Ed25519
when the file shows a post-quantum signature scheme — in its path, as the NIST API's `CRYPTO_ALGNAME`, or as the
scheme's own identifiers (`SPX_`, `MLD_`, `PQCLEAN_`) — and names neither Ed25519 nor libsodium or TweetNaCl. The
upper-case `CRYPTO_BYTES` is no signal, because SUPERCOP's ref10 Ed25519 defines it too. Measured on every file of the
portfolio whose Ed25519 row came from these names (11 files in 4 bundles): the five post-quantum files lose the row and
keep their ML-DSA and SLH-DSA rows; TweetNaCl in `libnunchuk`, ref10 in `monero` and libsodium in `stellar-core` keep
theirs.

`trezor-vendored-crypto` was re-audited at its recorded commit and scope, on the same tree: **143 inventory rows,
36 Shor-breakable** (148 and 41 before), its 102 post-quantum rows unchanged. Every version
of it published here carried the same five rows, so the 38 Shor-breakable rows that
[reports/PQ-ADOPTION-2026-10-28.md](reports/PQ-ADOPTION-2026-10-28.md) quotes for it were 33. The sub-audit
is outside the totals on this page, which therefore do not move.

The same day, a source file that is a table of test vectors (Wycheproof, FIPS 186-4) became test code when its name,
its own description and its body agree. Measured on the 579 analysed files with a test word in their name that 112
bundles' audited commits still serve, it changes no bundle published here.

## Correction, 2026-11-19: test-support files the path rules missed

Five kinds of test-support file were read as shipped code. Each was checked upstream at the audited commit before a
rule was written for it:

- Soroban's `testutils.rs`, `builtin_contracts/testutils.rs` and `e2e_testutils.rs`, which soroban-env-host compiles
  only under `#[cfg(any(test, feature = "testutils"))]` — in `rs-soroban-env` and in the four protocol versions that
  `stellar-core` vendors;
- arc-node's `pq_test_vectors.rs`, gated the same way behind `test-utils`, and the tool that generates them;
- `*_unittest.*` files, and NIST's `PQCgenKAT_*.c` known-answer-test generators;
- the cheat codes for symbolic tests with Halmos that OpenZeppelin pins beside forge-std, whose `SymTest.sol` derives
  a cheat-code address with Keccak-256 as forge-std does;
- Certora Prover harnesses under `certora/` (symbolic lending pools, dummy tokens, transfer-strategy harnesses),
  which the prover checks the contracts against and which are never deployed.

Measured with the old and new rules over every analysed input of the 130 bundles kept here: 183 files become test
code, carrying 30 inventory rows, in 12 bundles. The bundles published here that moved were re-audited at their
recorded commit and scope, each on the same tree:

| bundle | rows before | after | Shor before | after | own-code rows before | after | own Shor before | after |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `audits/aave-v3-origin` | 89 | **85** | 2 | **1** | 61 | **57** | 2 | **1** |
| `audits/safe-smart-account` | 33 | **30** | 5 | **3** | 13 | **10** | 5 | **3** |
| `studies/l1/arc-node` | 194 | **188** | 14 | **14** | 37 | **34** | 12 | **12** |
| `studies/l1/rs-soroban-env` | 76 | **73** | 38 | **36** | 58 | **55** | 38 | **36** |
| `studies/l1/stellar-core` | 419 | **408** | 176 | **169** | 186 | **175** | 143 | **136** |

The two in `audits/` move the totals on this page from 3,989 / 1,947 to
**3,982 / 1,944**. The studies quote own-code rows: Stellar's 58 + 186 (38 + 143 Shor-breakable) are now
**55 + 175** (36 + 136), and Arc's 37 (12) are **34** (12): its three
SLH-DSA rows from the test-vector generator are gone, and the SLH-DSA verification precompile the study names
remains. Both study reports carry a dated note. `zingolib` and `trezor-vendored-crypto` each had one such file with no
row in it, so their bundles stand.

Findings moved too. Harness code no longer produces them (`SOL-ADMIN-FUNCTIONS`, `SOL-FLOATING-PRAGMA` and
`SOL-ECRECOVER` in the Certora and Halmos harnesses), and a re-audit runs the current engine: `aave-v3-origin` gains
four findings from Solidity rules added since 6 November — `SOL-ORACLE-STALE` for `AaveOracle` and the two UI data
providers, which read `latestAnswer()` without a freshness check, and `SOL-ERC20-UNSAFE-CALL` for one `approve`
outside SafeERC20 — each preliminary, and each read against the source before publication. That reading found two
more false findings, now fixed: `require(feed.latestAnswer() > 0, ...)`, which Aave runs before storing a feed, reads
no price. The two Stellar bundles also carry advisory data as of 19 November (unrated and informational advisories).

## Re-issue, 2026-11-22: every bundle again, and whose code a finding is in

Every bundle published here that has an upstream commit, 59 in `audits/` and 20 in `studies/`, was
re-audited at its recorded commit, tree, language, risk profile and analyst decisions, with engine 1.16.2, and
each now carries the ML-DSA-65 co-signature. `audits/nitro` keeps its published bundle: its scope was never recorded, and the whole tree is a different measurement (5,714 parsed files where the published bundle parsed 1,038); `audits/lottery-demo` keeps its published bundle: it has no upstream repository. Before publication every re-issued bundle was compared
with the one it replaces, input by input, inventory row by row and finding by finding, and passed `bundle-qa`, the
quality gate added on 22 November. The comparison was run first on 22 November with engine 1.16.1; what it found
wrong in the engine was fixed, as 1.16.2, and every bundle was re-issued again on 23 November: those are the bundles
published. Every bundle, before and after, is in [reports/REISSUE-2026-11-22.md](reports/REISSUE-2026-11-22.md).

**The inventory** moves from 3,982 / 1,944 to **4,065 / 2,000**, post-quantum rows stay at 28 and hybrid rows at 14 (`openpgpjs` −2, `signal-desktop` +2), and the
Bitcoin slice from 808 / 555 to **823 / 570**. What moved it:

- a Solidity contract that verifies a signature through a library (OpenZeppelin's `ECDSA.recover` and
  `SignatureChecker`, `P256`, `WebAuthn`, `RSA.pkcs1Sha256`) now has a row, where only the `ecrecover` precompile was
  read before;
- a line that one pattern files under a parameter set (ECDSA on P-256) is no longer counted a second time as a bare
  ECDSA row because a broader pattern of the same entry matched it too;
- Cairo is read, PKCS#11 key types and mechanisms are recognised, Starknet's and Sapling's Pedersen is a hash rather
  than a commitment, EC-ElGamal and Falcon have rows of their own, and libsignal-client's key records and key
  agreement are Curve25519, of which Signal Desktop had no row at all;
- files that are not shipped code are set aside: Foundry tests (`*.t.sol`), minified bundles, a documentation
  generator's search index.

| codebase | rows before | after | Shor before | after | own-code rows before | after | why |
|---|---:|---:|---:|---:|---:|---:|---|
| `aave-v3-origin` | 85 | **95** | 1 | **11** | 57 | **28** | OpenZeppelin's `ECDSA.recover` and `SignatureChecker` in `AToken`, `DebtTokenBase` and `BaseDelegation` (permit and delegation by signature) and in the OpenZeppelin it pins |
| `bitbox02-firmware` | 202 | **206** | 113 | **117** | 91 | **89** | PKCS#11 mechanisms in cryptoauthlib's PKCS#11 layer (ECDSA, ECDH, finite-field DH, MQV); two duplicate bare ECDSA rows gone |
| `bitgo-mpc` | 93 | **97** | 68 | **71** | 88 | **92** | Ed25519 in the EdDSA and RedPallas MPS utilities and in the MPCv2 EdDSA module; PBKDF2 with 200,000 iterations |
| `cairo` | 38 | **61** | 14 | **25** | 33 | **54** | the Cairo files of the core library are read; Starknet's Pedersen is a hash, not a commitment; two cryptographic crates in `Cargo.lock` (tree 563 → 673 files) |
| `embit` | 87 | **89** | 64 | **66** | 44 | **44** | Pedersen commitments of secp256k1-zkp's range proofs |
| `ethers-js` | 114 | **116** | 43 | **43** | 110 | **112** | PBKDF2 of the 2014 presale wallet format in `json-crowdsale`, kept at info by an analyst decision |
| `fireblocks-mpc-lib` | 90 | **91** | 88 | **89** | 90 | **91** | a Pedersen commitment in the range proofs |
| `foundry` | 100 | **100** | 17 | **18** | 78 | **78** | ECDSA on secp256k1 in the Tempo session policy; Foundry's template tests (`*.t.sol`) set aside (tree 760 → 757 files) |
| `jade` | 144 | **149** | 107 | **112** | 33 | **33** | Pedersen commitments of the libwally-core and secp256k1-zkp it carries (generator, range proofs) |
| `krux` | 99 | **101** | 64 | **66** | 11 | **14** | Pedersen commitments of the secp256k1-zkp range proofs in the embit it pins |
| `librustzcash` | 147 | **144** | 26 | **23** | 35 | **32** | three duplicate bare ECDSA rows gone (PCZT signer, transparent builder and signer) |
| `libwally-core` | 103 | **108** | 81 | **86** | 45 | **46** | Pedersen commitments (Elements' generator and range proofs) |
| `lido-core` | 69 | **70** | 7 | **8** | 42 | **43** | an OpenZeppelin signature-library call in `SignatureUtils.sol` |
| `metamask-extension` | 51 | **53** | 13 | **13** | 17 | **17** | two cryptographic libraries in `yarn.lock` the registry now knows |
| `noir` | 71 | **68** | 9 | **7** | 44 | **41** | Pedersen hash in the CLI's build script; the documentation search index set aside (tree 783 → 782 files) |
| `openpgpjs` | 64 | **62** | 32 | **32** | 58 | **56** | ML-KEM and ML-DSA were each counted twice in `noble_post_quantum.ts`, with the parameter set and without it: post-quantum rows 8 → 6 |
| `rabby` | 66 | **72** | 29 | **30** | 34 | **38** | the sample keystore `wallet.json` is read (key, scrypt, AES-128-CTR) and two cryptographic libraries (tree 1,694 → 1,695 files) |
| `reown-appkit` | 67 | **71** | 16 | **20** | 19 | **23** | ECDSA in the browser-extension and laboratory apps |
| `rust-bitcoin` | 48 | **47** | 25 | **24** | 43 | **42** | one duplicate bare ECDSA row gone |
| `sapling-crypto` | 53 | **56** | 36 | **39** | 37 | **40** | Sapling's Pedersen is a hash, not a commitment: seven hash rows where there were four commitment rows |
| `scroll` | 89 | **98** | 7 | **12** | 56 | **60** | the test keystore and Web3Signer key configuration under `common/testcontainers`, which the path rules do not yet treat as test support (key files are read since 20 November); ECDSA in the relayer and its transaction signer; a signature-library call in `L2WstETHToken.sol`; a cryptographic Go module (tree 387 → 389 files) |
| `signal-desktop` | 22 | **29** | 0 | **5** | 20 | **27** | libsignal-client's Curve25519 identity and pre-keys, X25519 agreement and Kyber pre-keys: X25519 in five files (`ts/Curve.node.ts`, the protocol store, message sending and receiving, pre-key lookup), ML-KEM in two |
| `trustwallet-wallet-core` | 396 | **398** | 294 | **293** | 348 | **295** | ECDSA on the STARK curve (StarkEx keys) and three cryptographic crates; three duplicate bare ECDSA rows gone |

**Whose code** a row is in moved as well. A submodule that another project's submodule pins (OpenZeppelin under
`lib/solidity-utils` in `aave-v3-origin`) and a known library copied into the tree (`trezor-crypto/` in
`trustwallet-wallet-core`) count as third-party code now. That changes own-code figures, not the totals above.

**The findings** of the deduplicated codebases move from 2,526 to **2,316**, the critical and high
ones from 706 to **537**, for four reasons.

1. A finding whose every source lies in bundled third-party code (a vendored directory, a known library inside a
   dependency directory, a submodule another project's submodule pins) is informational and titled "In bundled
   third-party code": 38 findings.
2. Advisories on packages that only development or build tooling pulls in, a documentation site's included, are one
   informational `DEP-ADVISORY-DEV` finding per ecosystem; `agave`'s Docusaurus site alone held 194. Advisory findings
   move from 1,595 to **1,297**, with advisory data as of 23 November.
3. False findings were fixed in the engine first. All 9 high-severity "unprotected initializer" findings
   are gone: one was an internal library function in Aave's `ReserveLogic`, which no outside caller can reach and an
   earlier engine already passed over, and the comparison exposed the rest (Lido's Aragon `onlyInit` and contract
   versions, Scroll's owner-only predeploys, the OpenZeppelin 2.x proxies Aave vendors). It also exposed delegatecalls
   whose target no caller chooses (Aave), an example key from a manual page in `rage`, OBP-API's example tokens, which
   all expired between 2016 and 2022, and the placeholders of its configuration template, a counter
   nonce in Aptos's Noise implementation read as a fixed one, and an ECDSA signer in OpenPGP.js read as an Ed25519 one.
   Fixes made since a bundle's engine apply as well, such as Java's one-block `RSA/ECB/OAEP…` transform, which is not
   the ECB mode of a block cipher (OBP-API).
4. 74 findings are new, and none of them is critical or high: 19 post-quantum findings for the rows
   added above; 50 dependency findings from OSV.dev's data of 23 November, 32 of them advisories
   without a severity rating, which stay low or informational until triaged, and most of the rest informational
   notices; and 5 from rules added since a bundle's engine, each with an analyst decision (below). The
   other rules added since then (payment crediting, ERC-4626 inflation and more) run on every bundle now and report
   nothing new in these codebases.

Three analyst decisions were added, each with its reason in the report: ethers.js's `json-crowdsale` derives its key
with PBKDF2 at 2,000 iterations because the 2014 presale wallet format fixes that count, and ethers.js only decrypts
such wallets (`not_applicable`); OpenPGP.js's Ed25519 `sign()` takes the public key as an argument, but `decryptKey`
validates a key's parameters before the key can sign (`not_applicable`); and Rabby's `wallet.json` is a sample keystore
committed with its test set-up (`not_applicable`). The decision files as committed on 2 November carry severities
that their notes state and the published bundles did not, and the re-issue applies them: Krux's ECB formats in
`kef.py` are medium rather than high, crypto-bigint's timing advisory (RUSTSEC-2026-0387) in `bitbox02-firmware` and
`trustwallet-wallet-core` is medium rather than low, and the ECDSA finding of undetermined role in `libwally-core` and
`secp256k1` is informational. `embit`'s decisions of 29 October, signed in its bundle, had no file the runner could
read and were restored from the evidence archive.

**The studies** quote own-code rows. Every study bundle whose own-code or post-quantum figures moved:

| bundle | own-code rows before | after | own Shor before | after | post-quantum before | after | why |
|---|---:|---:|---:|---:|---:|---:|---|
| `studies/institutional/canton` | 74 | **73** | 35 | **35** | 2 | **2** | a false `IDEA` row in a CI script (`scripts/ci/todo_refs.py`) is gone |
| `studies/institutional/corda` | 23 | **22** | 16 | **15** | 0 | **0** | one ECDSA row in `DefaultCryptoService.kt` was counted twice, with its curve and without it |
| `studies/l1/aptos-core` | 82 | **79** | 58 | **55** | 4 | **4** | rows counted twice are gone (bare ECDSA rows beside the secp256r1 ones, a second Ed25519 row of the signing traits) and BLS12-381 is read from the code rather than from file names |
| `studies/l1/go-algorand` | 93 | **97** | 26 | **27** | 3 | **6** | Falcon-512 is now recognised in `crypto/falconWrapper.go`, the generated codec and `cmd/algokey`, beside the state-proof keys already counted, and Ed25519 in the p2p peer identity |
| `studies/l1/rs-soroban-env` | 55 | **50** | 36 | **31** | 6 | **6** | a line that names its curve (ECDSA on secp256k1 or P-256, in `crypto/mod.rs` and the cost runners) was also counted as a bare ECDSA row |
| `studies/l1/stellar-core` | 175 | **155** | 136 | **116** | 1 | **1** | the same double count, in the four protocol versions of Soroban it vendors (`src/rust/soroban/p21` to `p24`) |

The three study reports carry a dated note. The bundles as they were, the logs of both runs and both comparisons are
kept with this run.

## Re-issue, 2026-11-24: which advisories reach the code, and key storage

Every bundle published here that has an upstream commit, 59 in `audits/` and 20 in `studies/`, was
re-audited on 24 November at its recorded commit, tree, language, risk profile and analyst decisions, with engine 1.20.0;
`audits/lottery-demo` and `audits/nitro` keep their published bundles, for the reasons given under 22 November. The comparison prompted engine 1.20.1, with which `trezor-firmware`, `trustwallet-wallet-core` and `go-algorand` ran again (with the English bundles of `trezor-firmware` and `trustwallet-wallet-core`): it reports Go modules that hold only tests or samples as nothing to scan rather than as a failed scan, and retries a scan with cgo when a cgo wrapper's types are missing. Every re-issued
bundle was compared with the one it replaces, input by input, row by row and finding by
finding, and passed `bundle-qa`; each, before and after, is in
[reports/REISSUE-2026-11-24.md](reports/REISSUE-2026-11-24.md). What the engine gained since 1.16.2:

- **Whether a dependency advisory reaches the code.** Every advisory finding now carries a verdict. For Go, govulncheck
  builds the call graph from the product's own packages, tests and tools left out, through every dependency to the
  functions the Go vulnerability database names: a traced call keeps the advisory's severity with high confidence, and
  no call path makes it informational. It runs on every tree that holds a Go module, and the reports of 9 codebases,
  the studies included, record its result: 44 advisories with a traced call, 120 without one. Elsewhere the
  check is by imports and names: a module only tests use, affected
  functions the code does not name, a Cargo feature that is off or a platform not built make an advisory unlikely to
  apply, and a package that only other dependencies bring in stays open for review, marked as such, because without a
  call graph it can be neither confirmed nor set aside. Of 1,802 advisory findings, with OSV.dev's data of 24 November,
  295 are marked unlikely to apply. Each brief now lists first the code's own findings and the advisories whose affected functions the code
  names or calls, one row per package.
- **Key storage in backends** (`KEYMGMT-*`: a key with a fallback value in code or configuration, decryption that falls
  back to a constant key, a nonce derived from data, private keys in a database column the service decrypts without a
  KMS, an author's warning on key code), **Solana crediting** (a payment read from a failed transaction, a token
  payment without its mint) and **Go's `Sum`** on a fresh hasher, which hashes nothing. In the codebases here, which are wallets, libraries and nodes rather than the backends these rules were written for, they report one finding: Corda's node keeps the private keys of its confidential identities in its database unencrypted (`node_our_key_pairs`) and signs with them there, which the analyst decision confirms at medium.
- **Test support the path rules missed**: BoringSSL's BoGo suite (`bogo/`), test-container helpers
  (`testcontainers/`) and Storybook (`.storybook/`); and seven false-finding shapes found when every high finding of the
  portfolio was read against its source on 23 November: a C declaration of `random`, a value that repeats its own
  name, a header name, a Kotlin `$CONST` template, an SMT-LIB keyword compared with a token, a register-field
  `#define`, and a `verify=False` that belongs to no HTTP client.

**The inventory** moves from 4,065 / 2,000 to **4,045 / 1,991**, post-quantum rows stay at 28 and hybrid rows move from 14 to **13** (`rustls` −1), and the
Bitcoin slice stays at 823 / 570. Every codebase whose inventory moved:

| codebase | rows before | after | Shor before | after | own-code rows before | after | why |
|---|---:|---:|---:|---:|---:|---:|---|
| `rustls` | 111 | **97** | 29 | **22** | 88 | **87** | BoringSSL's test suite (BoGo) under `bogo/` is test code: its runner, key files and certificates (tree 137 → 120 files) |
| `scroll` | 98 | **93** | 12 | **10** | 60 | **55** | the test-container helpers under `common/testcontainers/` are test support, which the section of 22 November said the path rules did not yet treat as such: the test keystore and the Web3Signer key configuration (tree 389 → 385 files) |
| `signal-desktop` | 29 | **28** | 5 | **5** | 27 | **26** | Storybook's configuration under `.storybook/` is test code: a SHA-256 row in its test runner (tree 2,202 → 2,198 files) |

**The findings** of the deduplicated codebases move from 2,316 to **2,278**, the critical and high ones from
537 to **508**: 28 to **2** in the code itself and 509 to **506** advisories. Across the codebases
and the studies 21 more findings carry an analyst decision, from the decision files written on 23 and
24 November after the high findings without one were read against their source; each decision states its reason in
the report. In the study bundles the critical and high findings move from 48 to **24** by the same
decisions and fixes (Canton's and Corda's test certificates and keys, OBP-API's documentation examples, the SQLite that
stellar-core vendors). Every codebase whose critical and high findings moved:

| codebase | critical + high before | after | why |
|---|---:|---:|---|
| `bitbox02-firmware` | 11 | **9** | a register-field `#define` in the vendored SAMD51 headers was read as ECB mode, and the `verify=False` of the version script's own GPG check as disabled TLS: both shapes are fixed in the engine |
| `embit` | 1 | **0** | `ECKey.generate()` in `util/key.py`, Bitcoin Core's test-framework key code, draws the secret with Python's `random`; nothing in embit calls it, so the decision records it as a latent hazard at low |
| `foundry` | 5 | **3** | Anvil's `--mnemonic-seed-unsafe` derives the test accounts of a local development node from a seed the user passes (`not_applicable`), and an SMT-LIB keyword compared with a token in the symbolic solver was read as a secret: a shape fixed in the engine |
| `jade` | 2 | **0** | the keys of Jade's "fakeprod" mode under `tools/`, committed on purpose for development builds (`not_applicable`) |
| `krux` | 1 | **0** | Krux never calls the vendored copy of embit's `util/key.py` (`not_applicable`; the finding is embit's) |
| `lido-core` | 44 | **43** | `lib/pdg.ts` is a Hardhat test helper whose BLS keys come from the public test mnemonic (`not_applicable`) |
| `metamask-extension` | 33 | **32** | a crediting finding in Storybook's test data: `.storybook/` is test code |
| `rabby` | 171 | **170** | the Google Analytics 4 API secret in `src/utils/ga4.ts`, which ships in every copy of the extension and opens nothing (`not_applicable`) |
| `reown-appkit` | 155 | **154** | the fund-wallet view preselects a token from a list keyed by contract address; nothing there credits a payment (`not_applicable`) |
| `rustls` | 6 | **0** | the BoGo test keys and certificates, now test code |
| `scroll` | 38 | **31** | three Solidity findings in the cross-domain messengers are the detector reading a messenger's purpose as a defect (`false_positive`, each with the guard that makes it safe), and govulncheck decides the Go advisories: a traced call raises two to critical, no call path lowers others to informational |
| `seedsigner` | 2 | **0** | the decoy words of the "Verify Word" quiz are not key generation (`false_positive`), and `tools/mnemonic.py` is a developer helper outside the device image (`not_applicable`) |
| `signal-desktop` | 19 | **18** | the Giphy API key of the GIF picker, a client key that ships with the app by design (`not_applicable`) |
| `sigstore-js` | 10 | **9** | the certificate in `DEMO.md` is an example of the CLI's output, a ten-minute Fulcio certificate long expired (`false_positive`) |

**The studies** quote own-code rows, and no study bundle's own-code or post-quantum figures moved, so the three study reports stand as written. The bundles as they were and the logs of this run are kept with it.

## Institutional ledgers and bank-facing platforms

A separate study, kept out of the totals above: Canton, Arc, Hyperledger Fabric and Besu, Corda and the Open Bank
Project, seven signed bundles in `studies/institutional/`. Canton already signs with ML-DSA-65 and Arc verifies
SLH-DSA, but none of the seven encrypts with ML-KEM in its own code; Fabric gets hybrid TLS only from the Go
toolchain's default. See [reports/INSTITUTIONAL-LEDGERS-2026-11-06.md](reports/INSTITUTIONAL-LEDGERS-2026-11-06.md).

A second study compares five layer-1 networks' announced post-quantum plans with their code (Algorand, Aptos,
Stellar, Arc, Solana; bundles in `studies/l1/`): Falcon, SLH-DSA and ML-DSA verifiers and opt-in accounts exist, and
every consensus key set is still classical. See [reports/L1-PQ-PLANS-VS-CODE-2026-11-06.md](reports/L1-PQ-PLANS-VS-CODE-2026-11-06.md).

A third study reads the XRP Ledger stack for XRPL-Standards discussion 295, which proposes ML-DSA-44 under a
`Quantum` amendment: rippled (`develop` and `xrplf/quantum`), xrpl.js, xrpl-py, xrpl4j, xrpl-go, validator-keys-tool
and Ledger's XRP app, eight bundles in `studies/xrpl/`, each also co-signed with ML-DSA-65 (`python3 verify.py
studies/xrpl/*`). 241 inventory rows, 190 Shor-breakable; the 13 post-quantum rows are all on rippled's
`xrplf/quantum` branch. Two things the proposal does not cover yet: Confidential MPT balances (XLS-0096) sit on the
ledger as EC-ElGamal ciphertexts on secp256k1, readable by whoever first breaks the key with a quantum computer, and
validator-keys-tool has no post-quantum key type. See [reports/XRPL-PQ-INVENTORY-2026-11-21.md](reports/XRPL-PQ-INVENTORY-2026-11-21.md).

## A federal mandate now describes this method

OMB **M-26-15** of 24 June 2026 asks agencies to build "a dynamic, continuously updated inventory of all
cryptographic assets" using "Software Composition Analysis (SCA) to analyze Software Bills of Materials (SBOMs),
Static/Dynamic Application Security Testing (SAST/DAST) to find cryptographic functions in code, and network
scanners to detect protocols and cipher suites", feeding "a central Cryptographic Bill of Materials (CBOM)".
These bundles use two of those three methods and **declare the third**: live network probing is listed under
`not_checked` in every report, because each audit runs offline. Every bundle carries a CycloneDX `cbom.cdx.json`
— while noting that the *minimum elements* of a CBOM are still unpublished, due from CISA and NIST around
19 March 2027, so nobody can claim conformance to them yet.

The memorandum's algorithm table names seven quantum-vulnerable algorithms and then adds "Other non-PQC
Asymmetric Algorithms". Measured here, **40% of the 1,991 Shor-breakable rows fall only under
that catch-all**, across 18 distinct algorithms, the largest being Ed25519 — which the memorandum never
names. A tool built from the seven named algorithms finds RSA and ECDSA and misses the cryptography modern
systems are actually built from. The full mapping, and the one gap this exercise found in my own registry (MQV,
the seventh named algorithm, which had no entry), are in
[reports/FEDERAL-CBOM-2026-10-30.md](reports/FEDERAL-CBOM-2026-10-30.md) (also
[in English](reports/FEDERAL-CBOM-2026-10-30.en.md)).

On 27 October 2026 NIST published **IR 8547 in final form**, stricter than its 2024 draft: ECDSA, EdDSA, RSA and
Diffie-Hellman are now deprecated after 2030 at every key size, not only at 112 bits. Measured here, that puts a
2030 milestone on **342 rows the draft left alone until 2035** — standard Ed25519, P-256, P-384, RSA-3072
and up — and says nothing at all about the 473 secp256k1 rows, a curve NIST never approved; with the
535 rows in families no NIST standard covers, about half of the exposure here (1,008 of 1,991 rows) sits outside NIST's dates.
The split is section 3 of the same report.

## A check any project can run: does your scanner have a word for this cryptography?

An inventory can fail in a way that looks exactly like a clean result. Not a crash and not a parse error: the
scanner opens every file, recognises nothing, and reports that the code holds no quantum-vulnerable cryptography.

That happened here, on the worst possible target. `zcash/orchard` — the protocol whose Balance property rests
entirely on discrete logarithms in the Pallas group — measured **one inventory row (AES-256) and zero
Shor-breakable rows**. The registry had no entry for Sinsemilla, RedDSA, Halo 2 or Poseidon, so there was no word
in the vocabulary for any of it. With four entries added the same commit measures 69 rows and 41.

`zk-vocabulary.py` is the generalisable half, carrying that vocabulary and nothing else of this project. No
dependencies, no network, no `git`.

```
python3 zk-vocabulary.py --repo /path/to/checkout     # what is actually in this tree
python3 zk-vocabulary.py --against results.sarif      # ...and what your scanner failed to report
python3 zk-vocabulary.py --self-test                  # check the patterns before trusting their silence
```

It is careful about two things that a grep is not. It says **what** a quantum adversary breaks: for a commitment
that is *binding*, not hiding — a Pedersen commitment hides amounts information-theoretically, so committed values
stay secret against any computer, while a quantum adversary can open one to a different value, which is forged
supply rather than lost privacy. For a proof system it is *soundness*: accepted proofs of false statements. And it
reports **Poseidon as not Shor-breakable**, because its hardness is not group hardness; filing it under Shor would
overstate the risk as badly as missing Sinsemilla understated it.

Exit status 1 when the tree holds a primitive your tool did not report. `test-zk-vocabulary.sh` runs 14 cases,
four against freshly cloned real repositories, including the one that matters: fed the literal output this
scanner produced for `zcash/orchard` — `["AES-256"]` — it names all five primitives that were missed.

The defects behind every figure in this file, with the before-state archived, are in
[reports/FIXES-2026-10-30.md](reports/FIXES-2026-10-30.md) (also
[in English](reports/FIXES-2026-10-30.en.md)).

## A check any project can run: do your pinned submodules reach your tools?

`submodule-scope.py` is the generalisable half of the defect described above, written so it has nothing to do
with this repository or its scanner. No dependencies, no network, no `git` subprocess — it parses `.gitmodules`
itself, so it works on an exported tree too. Exit status 0 when nothing is wrong and 1 when something is.

```
python3 submodule-scope.py                           # are the pinned submodules even populated?
python3 submodule-scope.py --against results.sarif   # and did your tool actually read them?
python3 submodule-scope.py --against parsed.txt --scope src include
python3 submodule-scope.py --json
```

It catches two silent failures, both of which make a security tool report a clean result for code it never
opened. **A shallow clone leaves submodules empty** — `git clone --depth 1` without `--recurse-submodules` gives
you empty directories, a scanner finds nothing in them and says nothing about it, and CI is where this happens
because CI is where shallow clones live. **And a skip list can override a declared scope**: a scanner whose
directory-skip list contains `vendor` will skip `vendor/embit` even when the scope named it, and if it skips
before counting, the report never mentions what it declined. The first cost this project a reading of 7
inventory rows instead of 93; the second, 13 instead of 98.

`--against` takes a SARIF file, a JSON array or object with a `files`/`inputs` list, or one path per line — so
it works with whatever your tool already emits. In GitHub Actions:

```yaml
- uses: actions/checkout@v4
  with:
    submodules: recursive          # without this the next step tells you why it matters
- run: python3 submodule-scope.py
# after your scanner has run:
- run: python3 submodule-scope.py --against results.sarif
```

One exception, which the first published version got wrong: a submodule the project declares `update = none`
is one git itself leaves out of a default checkout — `git clone --recurse-submodules` skips it — so an empty one
is reported but is not a failure. Until 2026-11-02 the tool called SeedSigner's `seedsigner-screenshots` EMPTY
and would have failed CI for a checkout that was exactly as its maintainers intended. Only the empty case is
excused: once such a submodule is checked out, it gets the same checks as any other.

`test-submodule-scope.sh` is its test suite, 19 cases, and six of them are not synthetic. Two clone `embit` the
way CI clones — shallow, no submodules — and require the tool to catch the empty `secp256k1-zkp`, then
materialise the submodules and require it to pass. Four build a superproject with real git, offline, and hold
the tool to what git actually does with `update = none`.

## Layout

```
PUBLIC-KEY.pem     the one key that signed every bundle
PUBLIC-KEY-MLDSA.pem  the ML-DSA-65 key of the post-quantum co-signatures (from 13 November 2026)
verify.py          standalone verifier (Ed25519 and ML-DSA-65)
mldsa65-kat.json   NIST ACVP test vectors for verify.py --self-test
readiness.py       BIP-360 / BIP-361 readiness, measured from the bundles
submodule-scope.py are your pinned submodules populated, and did your tools read them?
test-submodule-scope.sh  its tests, including two against a real repository and four against git
audits/<name>/     report.json · report.md · report.html · report.pdf · cbom.cdx.json
                   report.sarif.json · bundle.sig.json · report.sig.json · public_key.pem
                   (+ public_key_mldsa.pem where co-signed)
                   brief.en.md · brief.ru.md (+ pdf)
studies/<study>/<name>/  bundles of the separate studies (institutional, l1, xrpl), same layout,
                   kept out of the totals on this page
reports/           the write-ups: re-audits, triage, adoption survey, scope-and-recall study,
                   the BIP-360/361 readiness analysis and the studies
```

`audits/` holds 61 directories but **53 distinct codebases**: 7 of them
(`bitbox02-firmware-en`, `bitgo-mpc-en`, `coinbase-cb-mpc-en`, `fireblocks-mpc-lib-en`, `librustzcash-en`, `trezor-firmware-en`, `trustwallet-wallet-core-en`) are English renderings of an audit also present in Russian, and
`trezor-vendored-crypto` is a sub-audit of a vendored directory inside `trezor-firmware`. Totals on this page
exclude all 8 so nothing is counted twice.

## The Bitcoin self-custody slice

Ten codebases, **823 inventory rows, 570 Shor-breakable**. This is the slice cited in grant
applications, so it is here in full.

| codebase | upstream | commit | files | inventory rows | Shor-breakable | post-quantum |
|---|---|---|---:|---:|---:|---:|
| `bitbox02-firmware` | BitBox (Shift Crypto) | `ae548ef4e40f` | 2645 | 206 | 117 | 0 |
| `jade` | Blockstream (Jade) | `a59d14c2b397` | 733 | 149 | 112 | 0 |
| `libwally-core` | Blockstream (libwally) | `374df231d054` | 245 | 108 | 86 | 0 |
| `trezor-firmware` | SatoshiLabs (Trezor) | `72489948b3c4` | 411 | 113 | 74 | 7 |
| `krux` | Krux (selfcustody) | `9b3a4314a205` | 244 | 101 | 66 | 0 |
| `rust-secp256k1` | rust-secp256k1 | `fe8b3bec962f` | 114 | 49 | 48 | 0 |
| `secp256k1` | Bitcoin Core (libsecp256k1) | `1b4181f93f7a` | 85 | 40 | 39 | 0 |
| `rust-bitcoin` | rust-bitcoin | `f127ba2ae14e` | 125 | 47 | 24 | 0 |
| `seedsigner` | SeedSigner | `ada81cde050e` | 76 | 9 | 3 | 0 |
| `bdk` | Bitcoin Dev Kit | `f2528da88b10` | 44 | 1 | 1 | 0 |

Two things this slice shows that no single-repository audit does. **The same cryptography lives in three
different places**: Jade vendors libwally's C source in-tree, Krux pins `embit` as a git submodule, and
SeedSigner pins the same `embit` as a hash-locked PyPI release — so an audit that does not follow the pin reports
a Bitcoin signer as clean. And **the three most-recommended hardware signers have diverged**: Trezor ships
working post-quantum code, including SLH-DSA in its boot header beside Ed25519, while BitBox02 and Jade ship
none.

## Everything, by inventory size

| codebase | upstream | commit | files | inventory rows | Shor-breakable | post-quantum |
|---|---|---|---:|---:|---:|---:|
| `trustwallet-wallet-core` | Trust Wallet | `adf80f8bac98` | 1695 | 398 | 293 | 0 |
| `agave` | Anza (Solana) | `7700cb3128c1` | 1287 | 212 | 115 | 0 |
| `bitbox02-firmware` | BitBox (Shift Crypto) | `ae548ef4e40f` | 2645 | 206 | 117 | 0 |
| `jade` | Blockstream (Jade) | `a59d14c2b397` | 733 | 149 | 112 | 0 |
| `zebra` | Zcash Foundation | `147a6a8bf7d3` | 437 | 146 | 68 | 0 |
| `librustzcash` | Electric Coin Company (Zcash) | `8672a4b2d60f` | 333 | 144 | 23 | 0 |
| `monero` | Monero | `3fd0f88c20f5` | 1117 | 137 | 99 | 0 |
| `bitwarden-sdk` | Bitwarden | `25b6c8c3860a` | 1625 | 120 | 13 | 5 |
| `ethers-js` | ethers.js project | `3ea4c226dd0b` | 759 | 116 | 43 | 0 |
| `trezor-firmware` | SatoshiLabs (Trezor) | `72489948b3c4` | 411 | 113 | 74 | 7 |
| `coinbase-cb-mpc` | Coinbase | `0b716706f998` | 174 | 108 | 93 | 2 |
| `libwally-core` | Blockstream (libwally) | `374df231d054` | 245 | 108 | 86 | 0 |
| `nitro` | Offchain Labs (Arbitrum) | `ccc5c828d9ea` | 1038 | 108 | 13 | 0 |
| `krux` | Krux (selfcustody) | `9b3a4314a205` | 244 | 101 | 66 | 0 |
| `foundry` | Foundry (Paradigm) | `7f0a409a5c20` | 757 | 100 | 18 | 0 |
| `bitgo-mpc` | BitGo | `3c892fd6a388` | 271 | 97 | 71 | 0 |
| `rustls` | rustls project | `84bf9eaa9857` | 120 | 97 | 22 | 0 |
| `aave-v3-origin` | Aave DAO | `8305565ae342` | 569 | 95 | 11 | 0 |
| `scroll` | scroll | `3046bbd18a6a` | 385 | 93 | 10 | 0 |
| `fireblocks-mpc-lib` | Fireblocks | `00ae08b7f1bd` | 123 | 91 | 89 | 0 |
| `embit` | embit (SeedSigner, Krux) | `2b375a33bd89` | 140 | 89 | 66 | 0 |
| `zingolib` | Zingo Labs | `81d799775f11` | 204 | 82 | 3 | 1 |
| `rabby` | Rabby Wallet (DeBank) | `663c0e80e9f6` | 1695 | 72 | 30 | 0 |
| `reown-appkit` | Reown (ex-WalletConnect) | `8f9f39f1dfe0` | 1246 | 71 | 20 | 0 |
| `lido-core` | Lido | `2bd532298d85` | 267 | 70 | 8 | 0 |
| `noir` | Aztec / Noir | `5c98fecd3fe6` | 782 | 68 | 7 | 0 |
| `orchard` | Electric Coin Company (Zcash) | `616a669df8c9` | 49 | 66 | 42 | 0 |
| `halo2` | Electric Coin Company (Zcash) | `3442dd33754a` | 100 | 63 | 45 | 0 |
| `openpgpjs` | OpenPGP.js project | `8bc35df48879` | 108 | 62 | 32 | 6 |
| `cairo` | StarkWare | `68a61f6c6251` | 673 | 61 | 25 | 0 |
| `frost` | Zcash Foundation | `0966bd1529aa` | 61 | 57 | 33 | 0 |
| `sapling-crypto` | Electric Coin Company (Zcash) | `88a7946b4a30` | 37 | 56 | 39 | 0 |
| `metamask-extension` | MetaMask (Consensys) | `d2db7ee9a19b` | 4856 | 53 | 13 | 0 |
| `rust-secp256k1` | rust-secp256k1 | `fe8b3bec962f` | 114 | 49 | 48 | 0 |
| `zcash-android-wallet-sdk` | Electric Coin Company (Zcash) | `a95780ac00e0` | 350 | 48 | 7 | 0 |
| `rust-bitcoin` | rust-bitcoin | `f127ba2ae14e` | 125 | 47 | 24 | 0 |
| `rage` | str4d (rage / age encryption) | `b5b68c4f4f7e` | 54 | 43 | 13 | 3 |
| `zcash-swift-wallet-sdk` | Electric Coin Company (Zcash) | `4895ee058da9` | 205 | 43 | 3 | 0 |
| `secp256k1` | Bitcoin Core (libsecp256k1) | `1b4181f93f7a` | 85 | 40 | 39 | 0 |
| `safe-smart-account` | Safe | `247b8ce3bdbf` | 74 | 30 | 3 | 0 |
| `signal-desktop` | Signal Messenger | `17502b9d1a9e` | 2198 | 28 | 5 | 4 |
| `tachyon` | Tachyon (Zcash) | `6cdaebccf147` | 57 | 25 | 10 | 0 |
| `bdk-wallet` | Bitcoin Dev Kit (bdk_wallet) | `09c677305139` | 27 | 14 | 11 | 0 |
| `rustcrypto-rsa` | RustCrypto project | `f96c4b5d629a` | 35 | 11 | 6 | 0 |
| `sigstore-js` | Sigstore project | `769a53d87132` | 180 | 10 | 3 | 0 |
| `lightwalletd` | Electric Coin Company (Zcash) | `4abfe9cd7b9b` | 34 | 9 | 3 | 0 |
| `reddsa` | Zcash Foundation | `04e973bcf8d4` | 15 | 9 | 4 | 0 |
| `seedsigner` | SeedSigner | `ada81cde050e` | 76 | 9 | 3 | 0 |
| `zodl-android` | Zodl (ex-Zashi, ECC) | `229dd3bff749` | 1609 | 8 | 3 | 0 |
| `matrix-js-sdk` | Matrix.org Foundation | `61b08bd037a3` | 240 | 6 | 1 | 0 |
| `pasta-curves` | Electric Coin Company (Zcash) | `e3c0f0246f56` | 35 | 5 | 5 | 0 |
| `bdk` | Bitcoin Dev Kit | `f2528da88b10` | 44 | 1 | 1 | 0 |
| `lottery-demo` | Демо-клиент | — | 1 | 1 | 0 | 0 |

One row has no commit and that is not an omission: `lottery-demo` is a single-file demonstration audit of a
529-byte `Lottery.sol` with no upstream repository, kept here because the portfolio totals quoted elsewhere
include it. It is the only entry in this repository that is not an audit of real upstream code.

## What this is not

- **Not a cryptographic review** of any implementation, and not a claim that any of these projects is weak.
- **Not a vulnerability report.** An inventory says a primitive is present and where, not that it is used
  wrongly. Where a finding is a defect rather than an inventory row, the report says which.
- **Not a full reachability analysis.** Since 24 November a dependency advisory in Go code is traced by govulncheck
  from the product's packages to the affected functions; elsewhere it is judged by imports and names, and one that
  cannot be settled that way stays open for review and says so. A finding in the audited code itself is not traced to
  an entry point.
- **Not a migration implementation.** Signature schemes change by consensus and by maintainers, not by a scanner.

## Known limits, and mistakes of mine that these numbers survived

Stated here rather than left for you to find.

**The tool is AI-assisted; the decisions are not.** The scanner proposes candidate rows and every one is decided
against the real source by hand before anything ships — most recently 75 findings across six codebases, each with
a written decision and its reason, 57 confirmed and 18 not applicable. The reports carry their own measured
false-positive history, including a case where **9 of 11 "high" findings proved false and were retracted**.

**Two failures of method, caught by measurement and now pinned by tests.** Blockstream Jade first measured 7
inventory rows and no secp256k1 at all, because a shallow clone leaves git submodules empty and all of Jade's
cryptography lives in one; materialised, it is 110 rows and 74 Shor-breakable. Krux measured 13 rows and a single
ECDSA row, because the scanner's own directory-skip list silently overrode the audit scope that named
`vendor/embit`, and did so before counting anything, so the report never mentioned what it had declined; read
correctly, Krux is 101 rows and 66 Shor-breakable. A census then compared every stored audit's declared
`.gitmodules` paths against the files its own signed bundle says it parsed and found **18 in-scope submodules
that had never reached the scanner at all**. Both rules are now enforced by the runner and pinned by tests.

**Any portfolio total here is a floor,** not a ceiling: at least one audited repository still has unmaterialised
submodules and has not been re-run.

**Key material is never stored.** Where a secret-like string is found, the report records the file, the line, a
SHA-256 of the line and the fact of the match — the value is replaced with `[REDACTED BY QSI]`. You can see this
in `audits/rustls/report.md`, where the findings point at the project's own BoGo test-suite key files: the PEM
header is shown, the key bytes are not, and the report states that the value was not retained.

## Licence

`verify.py` and the repository's own tooling: MIT. The reports may be read, redistributed and quoted freely; if
you quote a figure, please quote the commit beside it, because the figure belongs to that commit.

## Contact

Open an issue here, or reach me as `AlekseyKoks-in`. If you maintain one of these projects and a row looks wrong,
that is the most useful message I can get — the two corrections above both began as a number that looked wrong.

---

# По-русски

Подписанные комплекты аудита (61) по **53 кодовым базам**: машиночитаемая инвентаризация
криптографических примитивов — какой алгоритм, где, для чего, и что с ним делает квантовый компьютер. Всего
**4 045 строк инвентаризации**, из них **1 991 ломает алгоритм Шора**, и **28 уже
постквантовых**; разобрано **30 744 файлов**.

Каждый комплект привязан к коммиту апстрима, несёт подпись Ed25519 и CBOM в формате CycloneDX и сделан до того,
как кто-либо за это заплатил. Смысл публикации в том, что ни одной цифре выше верить не нужно.

**Проверка:** `python3 verify.py --self-test`, затем `python3 verify.py`. Зависимостей нет, сети не требуется.
Проверяльщик заново считает хеши всех файлов, перечисленных в подписи, проверяет подпись Ed25519 над подписанным
payload и сверяет ключ каждого комплекта с `PUBLIC-KEY.pem` в корне. Ed25519 реализован в нём дважды —
самостоятельно и через пакет `cryptography`, если тот установлен, — и **обе реализации должны совпасть**.
Самопроверка показывает, что настоящая подпись проходит, реализации согласны, а перевёрнутый байт payload,
подписи или файла обнаруживается.

**Постквантовая соподпись.** Комплекты, подписанные с 13 ноября 2026 года, несут и подпись ML-DSA-65 (FIPS 204)
над тем же payload; `verify.py` проверяет её встроенной реализацией на чистом Python (сверена со всеми 30 векторами
NIST для ML-DSA-65) и сверяет ключ с `PUBLIC-KEY-MLDSA.pem` в корне (`dbd4e297b3213d1d`). После перевыпуска 22 ноября
соподписаны все комплекты, кроме `audits/lottery-demo` и `audits/nitro`: они подписаны до появления соподписи. Проверка зависимостей по OSV.dev до 12 ноября брала
не больше 1000 закреплённых пакетов и не говорила об остальных; теперь до 5000, остаток назван в покрытии. Находок
по бюллетеням в этих комплектах стало 1 454 вместо 433; инвентаризация не изменилась, кроме одной
строки ECDH в `metamask-extension` (импорт `eciesjs`): итог стал таким — строк 3 989, по Шору
1 947 (было 3 988 и 1 946). Тем же переаудитом заменён `arc-node` — один комплект в обоих исследованиях: пакетов 1 000 → 1 993, находок по бюллетеням 30 → 37; 37 строк своего кода и 12 по Шору, которые цитируют исследования, тогда не изменились (их меняет поправка 19 ноября). На прежнем пределе остаётся: `audits/nitro`.

**Перевыпуск 24 ноября.** Все комплекты с апстримом, 59 в `audits/` и 20 в `studies/`,
переаудированы 24 ноября движком 1.20.0 на записанных коммите, дереве, языке, профиле риска и решениях аналитика;
`audits/lottery-demo` и `audits/nitro` сохраняют опубликованные комплекты (причины — в абзаце о 22–23 ноября ниже). Сверка дала движок 1.20.1, им ещё раз прогнаны `trezor-firmware`, `trustwallet-wallet-core` и `go-algorand` (и английские версии `trezor-firmware` и `trustwallet-wallet-core`): Go-модули, где только тесты или примеры, теперь «сканировать нечего», а не сбой, а скан повторяется с cgo, когда не хватает типов обёртки cgo. Каждый сверен с
прежним и прошёл `bundle-qa`; до и после — в
[reports/REISSUE-2026-11-24.md](reports/REISSUE-2026-11-24.md). Новое: у каждого бюллетеня зависимости есть вердикт
достижимости — для Go граф вызовов govulncheck от пакетов продукта (результат записан в отчётах 9 кодовых баз:
вызов прослежен у 44, нет вызова у 120), для прочих экосистем — по импортам и именам; маловероятными помечены 295 из
1 802. Правила хранения ключей (`KEYMGMT-*`), зачисления на Solana и `Sum` в Go нашли одну находку: узел Corda хранит закрытые ключи конфиденциальных идентичностей в своей базе без шифрования (`node_our_key_pairs`) и подписывает ими там же — решение аналитика подтверждает её со средней важностью. Тестовым
кодом теперь считаются набор BoGo (`bogo/`), помощники testcontainers и Storybook. Итог портфеля: **строк 4 045,
по Шору 1 991** (было 4 065 и 2 000), постквантовых по-прежнему 28, гибридных 13 (было 14); срез биткоина — по-прежнему 823 и 570. Находок
2 278 вместо 2 316, критических и высоких 508 вместо 537: ещё 21 находок получили решение
аналитика после чтения исходников, ложные формы исправлены в движке, а govulncheck поднимает бюллетень с прослеженным
вызовом и опускает до информационного тот, до которого вызов не доходит. Таблицы — в английском разделе.

**Перевыпуск 22–23 ноября.** Все комплекты с апстримом, 59 в `audits/` и 20 в `studies/`,
переаудированы 23 ноября на записанных коммите, дереве, языке, профиле риска и решениях аналитика движком 1.16.2; все
соподписаны ML-DSA-65. `audits/nitro` сохраняет опубликованный комплект: область аудита не была записана, а всё дерево — другое измерение (5 714 разобранных файлов вместо 1 038); `audits/lottery-demo` сохраняет опубликованный комплект: у него нет апстрима. Каждый перевыпущенный комплект сверен с прежним по входам, строкам и находкам и
прошёл `bundle-qa`; ошибки движка, найденные сверкой (первый прогон — движок 1.16.1), исправлены до публикуемого прогона;
каждый комплект до и после — в [reports/REISSUE-2026-11-22.md](reports/REISSUE-2026-11-22.md). Итог портфеля: **строк 4 065, по Шору 2 000** (было 3 982 и 1 944), постквантовых и гибридных по-прежнему 28 и 14 (`openpgpjs` −2, `signal-desktop` +2);
срез биткоина — 823 и 570 (было 808 и 555).
Строки прибавили вызовы библиотек подписи в Solidity, чтение Cairo, PKCS#11, EC-ElGamal, Falcon и словарь libsignal;
убавили дубли «ECDSA без кривой» рядом с «ECDSA P-256» и файлы, которые не являются поставляемым кодом. Находок
2 316 вместо 2 526, критических и высоких 537 вместо 706: находки в стороннем коде
дерева стали информационными (38), бюллетени пакетов только для разработки и сборки сведены в одну находку
на экосистему, ложные находки исправлены в движке (все 9 «незащищённых инициализаторов»,
delegatecall без выбора цели вызывающим, пример ключа из man-страницы rage, истёкшие примерные JWT и шаблон настроек
OBP-API, nonce со счётчиком в Noise у Aptos, ECDSA, принятая за Ed25519, в OpenPGP.js), а правила, добавленные после
выпуска комплекта, теперь применены к нему. Добавлены три решения аналитика (ethers.js, OpenPGP.js, Rabby), а
серьёзности, записанные в файлах решений, теперь действуют: ECB у Krux — средняя вместо высокой, бюллетень
crypto-bigint у BitBox02 и Trust Wallet Core — средняя вместо низкой. Таблицы — в английском разделе.

**Поправка 19 ноября.** Тестовый код, который не ловили правила по путям: `testutils.rs` и `e2e_testutils.rs` в
Soroban (собираются только для тестов), генератор PQ-векторов arc-node, `*_unittest.*`, генераторы KAT от NIST, обвязка
Halmos и Certora. Измерено по всем разобранным файлам 130 комплектов: 183 файла, 30 строк, 12 комплектов. Итог
портфеля: **строк 3 982, по Шору 1 944** (было 3 989 и 1 947). В исследованиях: строк своего
кода у Stellar 55 + 175 вместо 58 + 186 (по Шору 36 + 136 вместо 38 + 143), у Arc
34 вместо 37 (по Шору 12).

**Поправка 18 ноября.** NIST взял для постквантовых подписей API NaCl, поэтому `crypto_sign_keypair` в эталонных
SPHINCS+ и ML-DSA сканер читал как Ed25519: в `trezor-vendored-crypto` было 5 ложных строк Ed25519, ломаемых
Шором, — во всех опубликованных версиях (из 38 строк по Шору в отчёте от 28 октября настоящих
33). После переаудита: строк 143, по Шору 36 (было 148 и 41); подаудит в
итоги не входит. Тем же днём таблицы тестовых векторов (Wycheproof, FIPS 186-4) стали тестовым кодом; опубликованные
комплекты это не меняет.

Каталогов в `audits/` — 61, а разных кодовых баз — **53**: 7 из них — англоязычные
версии тех же аудитов, а `trezor-vendored-crypto` — подаудит вложенного каталога внутри `trezor-firmware`. В
итогах они исключены, иначе портфель считал бы себя дважды.

**Срез самостоятельного хранения биткоина:** десять кодовых баз, **823 строки, 570 ломает Шор**. Та же
криптография лежит в трёх разных местах — Jade вносит исходники libwally в своё дерево, Krux подключает `embit`
как git-подмодуль, SeedSigner — тот же `embit` как релиз с PyPI с замком по хешу, — поэтому аудит, не прошедший
по закреплению, объявляет биткоин-подписанта чистым. И три самых рекомендуемых аппаратных кошелька разошлись: у
Trezor постквантовый код работает, включая SLH-DSA в загрузочном заголовке рядом с Ed25519, у BitBox02 и Jade —
ничего.

**XRP Ledger (21 ноября), отдельное исследование вне итогов.** Для обсуждения №295 в XRPL-Standards (ML-DSA-44 под
поправкой `Quantum`) прочитан стек XRP Ledger: rippled (`develop` и `xrplf/quantum`), xrpl.js, xrpl-py, xrpl4j,
xrpl-go, validator-keys-tool и приложение XRP для Ledger — восемь комплектов в `studies/xrpl/`, все с соподписью
ML-DSA-65 (`python3 verify.py studies/xrpl/*`). Строк 241, по Шору 190; все 13 постквантовых — в ветке
`xrplf/quantum` rippled. Чего предложение пока не охватывает: остатки конфиденциальных MPT (XLS-0096) лежат в реестре
как шифротексты EC-ElGamal на secp256k1, и их прочтёт тот, кто первым взломает ключ квантовым компьютером; в
validator-keys-tool нет постквантового типа ключа. Подробно — [reports/XRPL-PQ-INVENTORY-2026-11-21.md](reports/XRPL-PQ-INVENTORY-2026-11-21.md).

**Чем это не является:** не криптографический разбор реализаций и не утверждение, что эти проекты слабы; не отчёт
об уязвимостях — инвентаризация говорит, что примитив присутствует и где, а не что он применён неверно; не полный
анализ достижимости (с 24 ноября бюллетени Go проверяет граф вызовов govulncheck, прочие — импорты и имена, а находки в
самом коде до точки входа не прослеживаются); не реализация миграции.

**Честно об ограничениях.** Инструмент построен при значительной помощи ИИ, но решения принимаются вручную:
сканер предлагает строки-кандидаты, каждая разбирается по реальным исходникам до публикации — в последней партии
75 находок по шести базам, по каждой письменное решение с причиной, 57 подтверждено, 18 неприменимо. Отчёты сами
указывают измеренную историю ложных срабатываний, включая случай, когда **9 из 11 «высоких» оказались ложными и
были отозваны**. Два провала метода, найденные измерением и закрытые тестами: Jade сначала дал 7 строк и ни одного
secp256k1 (поверхностный клон оставляет подмодули пустыми) — после подтягивания 110 строк и 74 Шора; Krux дал 13
строк и одну ECDSA, потому что список пропускаемых каталогов молча переопределил объявленную область с
`vendor/embit`, — прочитанный правильно, 101 строка и 66. Затем перепись сравнила у каждого аудита пути из
`.gitmodules` с файлами, которые его подписанный комплект называет разобранными, и нашла **18 подмодулей в области
аудита, которые до сканера вообще не доходили**. Любая суммарная цифра здесь — **нижняя граница**.

**Ключевой материал не сохраняется.** Там, где найдена строка, похожая на секрет, отчёт фиксирует файл, строку,
SHA-256 строки и сам факт совпадения, а значение заменено на `[REDACTED BY QSI]`. Это видно в
`audits/rustls/report.md`: находки указывают на тестовые ключи самого проекта из набора BoGo — показан заголовок
PEM, байты ключа нет, и отчёт прямо говорит, что значение не сохранялось.

**Лицензия:** `verify.py` и собственный инструментарий — MIT; отчёты можно свободно читать, распространять и
цитировать. Если цитируете цифру, приводите рядом коммит: цифра принадлежит коммиту.

**Связь:** issue в этом репозитории или `AlekseyKoks-in`. Если вы мейнтейнер одного из этих проектов и строка
выглядит неверной — это самое полезное сообщение, какое может прийти: оба исправления выше начались с цифры,
которая выглядела неправильно.
