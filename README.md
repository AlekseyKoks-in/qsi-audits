# Cryptographic inventories of open-source code, signed and reproducible

60 audit bundles over **52 codebases**: a machine-readable inventory of every cryptographic
primitive the scanner found, what it is used for, and what a quantum computer does to it. Across those codebases
**3,745 inventory rows**, of which **1,708 fall to Shor's algorithm**, **28 are post-quantum** and
**4 are hybrid** (post-quantum combined with classical), from **30,771 parsed files**. Those last two
are kept apart on purpose: write-ups of mine dated before 2026-10-30 quote a single "29 post-quantum" that was
28+4-style addition of the two, which is why one number appeared in two different places.

### What those rows rest on

A single "inventory rows" total mixes evidence of very different strength, so here it is split. This is the one
table to read before quoting any other number in this repository.

| what the row rests on | rows | Shor-breakable |
|---|---:|---:|
| a line of source code | 1,987 | 1,243 |
| name of a dependency in a manifest | 911 | 0 |
| name of a source file (low confidence) | 384 | 180 |
| a deployed smart contract | 126 | 3 |
| OpenPGP key committed to the repository | 117 | 117 |
| a certificate or key file | 112 | 59 |
| the chain a wallet supports | 105 | 105 |
| other | 3 | 1 |

Two things in that table are worth saying out loud rather than leaving for a careful reader to notice.

**180 of the 1,708 Shor-breakable rows rest on the name of a source file**, not on a line of
code. That signal exists because `trezor-firmware/crypto/pbkdf2.c` *defines* PBKDF2 instead of calling it, so no
call-site pattern reaches it and the inventory missed it entirely — a file named after an algorithm is the project
telling you what is in it. It is still weaker evidence than a call, the reports mark it `confidence: low`, and a
headline figure silently promotes it to the same standing as the rest. Now it does not.

**117 rows are cryptography the projects did not write**: OpenPGP primary keys and subkeys committed to the
repositories — maintainers' release-signing keys, in `bitbox02-firmware`, `jade`, `libwally-core`, `monero`, `zcash-android-wallet-sdk`, `zcash-swift-wallet-sdk`, `zebra`. They belong in an
inventory, because a quantum computer forges a release signature as readily as a transaction one, but a reader who
saw only the Shor total would take them for implemented cryptography. Every one carries `usage: OpenPGP primary
key` or `OpenPGP subkey`, so one filter removes them from any figure here.

The 911 manifest rows carry no quantum status at all —
a dependency's name is not an algorithm — which is why they add to the row count and nothing to the Shor count.

Every bundle is pinned to an upstream commit, carries an Ed25519 signature and a CycloneDX CBOM, and was produced
before anyone paid for it. The point of publishing them is that you do not have to believe any of the numbers
above.

## Check it yourself

No dependencies, no network, nothing to install:

```
python3 verify.py --self-test     # test the verifier before trusting what it says
python3 verify.py                 # verify all 60 bundles
python3 verify.py audits/secp256k1
```

`verify.py` re-hashes every file named in each signature, verifies the Ed25519 signature over the signed payload,
and checks that the key which signed each bundle is the one in `PUBLIC-KEY.pem` at the root — so substituting a
key in one bundle does not go unnoticed. Ed25519 is implemented twice in that file, once self-contained and once
through the `cryptography` package when it is installed, and **both must agree**; `--self-test` demonstrates that
a real signature passes, that the two implementations agree, and that flipping a single byte of the payload, the
signature or a file is caught.

Signing key `5b3cf9c9bd0fa544`, fingerprint
`5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e`.

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

Schnorr/BIP-340 primitives are present in 7 of the 10 self-custody codebases, and **exactly 1 of
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
own code arriving as the benchmarks left — and measure **693 and 448** now that `bitbox02-firmware` is
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
Shor-breakable to **197 and 104**. 44 of the added rows are committed OpenPGP keys rather than
implemented cryptography, which the breakdown above separates, so the honest statement of the improvement is
136 → 153 rows of cryptography this project actually contains.

**`krux` is still left at its earlier bundle**, and the reason is narrower than a size limit. Re-read at full
depth it yields 248 inventory rows — but **230 of them come from `firmware/MaixPy` and 11 from `src/krux`**, with
1,677 files still not fitting. That is a 23% sample of the tree whose composition depends on the order files are
visited, presented as an inventory of a hardware wallet. The 98-row bundle published here covers Krux's own code
and the `embit` it pins, within the budget, and answers the question a reader actually has. The full run is kept
as evidence rather than published as a measurement.

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

`test-submodule-scope.sh` is its test suite, 11 cases, and two of them are not synthetic: it clones `embit` the
way CI clones — shallow, no submodules — and requires the tool to catch the empty `secp256k1-zkp`, then
materialises the submodules and requires it to pass.

## Layout

```
PUBLIC-KEY.pem     the one key that signed every bundle
verify.py          standalone verifier
readiness.py       BIP-360 / BIP-361 readiness, measured from the bundles
submodule-scope.py are your pinned submodules populated, and did your tools read them?
test-submodule-scope.sh  its tests, including two against a real repository
audits/<name>/     report.json · report.md · report.html · report.pdf · cbom.cdx.json
                   report.sarif.json · bundle.sig.json · report.sig.json · public_key.pem
                   brief.en.md · brief.ru.md (+ pdf)
reports/           the write-ups: re-audits, triage, adoption survey, scope-and-recall study,
                   and the BIP-360/361 readiness analysis
```

`audits/` holds 60 directories but **52 distinct codebases**: 7 of them
(`bitbox02-firmware-en`, `bitgo-mpc-en`, `coinbase-cb-mpc-en`, `fireblocks-mpc-lib-en`, `librustzcash-en`, `trezor-firmware-en`, `trustwallet-wallet-core-en`) are English renderings of an audit also present in Russian, and
`trezor-vendored-crypto` is a sub-audit of a vendored directory inside `trezor-firmware`. Totals on this page
exclude all 8 so nothing is counted twice.

## The Bitcoin self-custody slice

Ten codebases, **693 inventory rows, 448 Shor-breakable**. This is the slice cited in grant
applications, so it is here in full.

| codebase | upstream | commit | files | inventory rows | Shor-breakable | post-quantum |
|---|---|---|---:|---:|---:|---:|
| `bitbox02-firmware` | BitBox (Shift Crypto) | `ae548ef4e40f` | 2645 | 197 | 104 | 0 |
| `jade` | Blockstream (Jade) | `a59d14c2b397` | 737 | 110 | 74 | 0 |
| `trezor-firmware` | SatoshiLabs (Trezor) | `72489948b3c4` | 411 | 111 | 73 | 7 |
| `krux` | Krux (selfcustody) | `9b3a4314a205` | 257 | 98 | 64 | 0 |
| `libwally-core` | Blockstream (libwally) | `374df231d054` | 249 | 77 | 56 | 0 |
| `rust-secp256k1` | rust-secp256k1 | `fe8b3bec962f` | 118 | 32 | 32 | 0 |
| `secp256k1` | Bitcoin Core (libsecp256k1) | `1b4181f93f7a` | 90 | 32 | 32 | 0 |
| `rust-bitcoin` | rust-bitcoin | `f127ba2ae14e` | 125 | 28 | 11 | 0 |
| `bdk` | Bitcoin Dev Kit | `f2528da88b10` | 45 | 1 | 1 | 0 |
| `seedsigner` | SeedSigner | `ada81cde050e` | 74 | 7 | 1 | 0 |

Two things this slice shows that no single-repository audit does. **The same cryptography lives in three
different places**: Jade vendors libwally's C source in-tree, Krux pins `embit` as a git submodule, and
SeedSigner pins the same `embit` as a hash-locked PyPI release — so an audit that does not follow the pin reports
a Bitcoin signer as clean. And **the three most-recommended hardware signers have diverged**: Trezor ships
working post-quantum code, including SLH-DSA in its boot header beside Ed25519, while BitBox02 and Jade ship
none.

## Everything, by inventory size

| codebase | upstream | commit | files | inventory rows | Shor-breakable | post-quantum |
|---|---|---|---:|---:|---:|---:|
| `trustwallet-wallet-core` | Trust Wallet | `adf80f8bac98` | 1695 | 355 | 254 | 0 |
| `bitbox02-firmware` | BitBox (Shift Crypto) | `ae548ef4e40f` | 2645 | 197 | 104 | 0 |
| `agave` | Anza (Solana) | `7700cb3128c1` | 1293 | 189 | 103 | 0 |
| `librustzcash` | Electric Coin Company (Zcash) | `8672a4b2d60f` | 333 | 156 | 23 | 0 |
| `zebra` | Zcash Foundation | `147a6a8bf7d3` | 439 | 148 | 65 | 0 |
| `bitwarden-sdk` | Bitwarden | `25b6c8c3860a` | 1625 | 119 | 12 | 5 |
| `monero` | Monero | `3fd0f88c20f5` | 1117 | 116 | 79 | 0 |
| `trezor-firmware` | SatoshiLabs (Trezor) | `72489948b3c4` | 411 | 111 | 73 | 7 |
| `jade` | Blockstream (Jade) | `a59d14c2b397` | 737 | 110 | 74 | 0 |
| `nitro` | Offchain Labs (Arbitrum) | `ccc5c828d9ea` | 1038 | 108 | 13 | 0 |
| `coinbase-cb-mpc` | Coinbase | `0b716706f998` | 174 | 103 | 88 | 2 |
| `rustls` | rustls project | `84bf9eaa9857` | 137 | 103 | 29 | 0 |
| `ethers-js` | ethers.js project | `3ea4c226dd0b` | 759 | 100 | 29 | 0 |
| `foundry` | Foundry (Paradigm) | `7f0a409a5c20` | 761 | 100 | 16 | 0 |
| `krux` | Krux (selfcustody) | `9b3a4314a205` | 257 | 98 | 64 | 0 |
| `bitgo-mpc` | BitGo | `3c892fd6a388` | 271 | 91 | 66 | 0 |
| `aave-v3-origin` | Aave DAO | `8305565ae342` | 645 | 89 | 2 | 0 |
| `fireblocks-mpc-lib` | Fireblocks | `00ae08b7f1bd` | 123 | 89 | 87 | 0 |
| `zingolib` | Zingo Labs | `81d799775f11` | 205 | 86 | 3 | 1 |
| `scroll` | Scroll | `3046bbd18a6a` | 387 | 78 | 7 | 0 |
| `embit` | embit (SeedSigner, Krux) | `2b375a33bd89` | 142 | 77 | 55 | 0 |
| `libwally-core` | Blockstream (libwally) | `374df231d054` | 249 | 77 | 56 | 0 |
| `halo2` | Electric Coin Company (Zcash) | `3442dd33754a` | 100 | 73 | 45 | 0 |
| `noir` | Aztec / Noir | `5c98fecd3fe6` | 783 | 72 | 9 | 0 |
| `lido-core` | Lido | `2bd532298d85` | 267 | 69 | 7 | 0 |
| `orchard` | Electric Coin Company (Zcash) | `616a669df8c9` | 49 | 69 | 41 | 0 |
| `rabby` | Rabby Wallet (DeBank) | `663c0e80e9f6` | 1694 | 66 | 29 | 0 |
| `reown-appkit` | Reown (ex-WalletConnect) | `8f9f39f1dfe0` | 1249 | 66 | 16 | 0 |
| `openpgpjs` | OpenPGP.js project | `8bc35df48879` | 108 | 65 | 35 | 8 |
| `frost` | Zcash Foundation | `0966bd1529aa` | 61 | 59 | 33 | 0 |
| `sapling-crypto` | Electric Coin Company (Zcash) | `88a7946b4a30` | 37 | 57 | 36 | 0 |
| `metamask-extension` | MetaMask (Consensys) | `d2db7ee9a19b` | 4873 | 50 | 12 | 0 |
| `zcash-android-wallet-sdk` | Electric Coin Company (Zcash) | `a95780ac00e0` | 350 | 46 | 2 | 0 |
| `zcash-swift-wallet-sdk` | Electric Coin Company (Zcash) | `4895ee058da9` | 205 | 45 | 2 | 0 |
| `rage` | str4d (rage / age encryption) | `b5b68c4f4f7e` | 54 | 43 | 13 | 3 |
| `safe-smart-account` | Safe | `247b8ce3bdbf` | 77 | 33 | 5 | 0 |
| `rust-secp256k1` | rust-secp256k1 | `fe8b3bec962f` | 118 | 32 | 32 | 0 |
| `secp256k1` | Bitcoin Core (libsecp256k1) | `1b4181f93f7a` | 90 | 32 | 32 | 0 |
| `tachyon` | Tachyon (Zcash) | `6cdaebccf147` | 58 | 29 | 10 | 0 |
| `rust-bitcoin` | rust-bitcoin | `f127ba2ae14e` | 125 | 28 | 11 | 0 |
| `signal-desktop` | Signal Messenger | `17502b9d1a9e` | 2202 | 22 | 0 | 2 |
| `cairo` | StarkWare | `68a61f6c6251` | 567 | 18 | 10 | 0 |
| `reddsa` | Zcash Foundation | `04e973bcf8d4` | 15 | 12 | 4 | 0 |
| `rustcrypto-rsa` | RustCrypto project | `f96c4b5d629a` | 35 | 11 | 6 | 0 |
| `bdk-wallet` | Bitcoin Dev Kit (bdk_wallet) | `09c677305139` | 28 | 10 | 7 | 0 |
| `sigstore-js` | Sigstore project | `769a53d87132` | 180 | 10 | 3 | 0 |
| `lightwalletd` | Electric Coin Company (Zcash) | `4abfe9cd7b9b` | 34 | 8 | 3 | 0 |
| `seedsigner` | SeedSigner | `ada81cde050e` | 74 | 7 | 1 | 0 |
| `matrix-js-sdk` | Matrix.org Foundation | `61b08bd037a3` | 240 | 6 | 1 | 0 |
| `zodl-android` | Zodl (ex-Zashi, ECC) | `229dd3bff749` | 1609 | 5 | 0 | 0 |
| `bdk` | Bitcoin Dev Kit | `f2528da88b10` | 45 | 1 | 1 | 0 |
| `lottery-demo` | Демо-клиент | — | 1 | 1 | 0 | 0 |

One row has no commit and that is not an omission: `lottery-demo` is a single-file demonstration audit of a
529-byte `Lottery.sol` with no upstream repository, kept here because the portfolio totals quoted elsewhere
include it. It is the only entry in this repository that is not an audit of real upstream code.

## What this is not

- **Not a cryptographic review** of any implementation, and not a claim that any of these projects is weak.
- **Not a vulnerability report.** An inventory says a primitive is present and where, not that it is used
  wrongly. Where a finding is a defect rather than an inventory row, the report says which.
- **Not reachability analysis.** Where it cannot be established that an affected code path is reached, the report
  says so instead of implying it.
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
correctly, Krux is 98 rows and 64 Shor-breakable. A census then compared every stored audit's declared
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

60 подписанных комплектов аудита по **52 кодовым базам**: машиночитаемая инвентаризация
криптографических примитивов — какой алгоритм, где, для чего, и что с ним делает квантовый компьютер. Всего
**3,745 строк инвентаризации**, из них **1,708 ломает алгоритм Шора**, и **28 уже
постквантовых**; разобрано **30,771 файлов**.

Каждый комплект привязан к коммиту апстрима, несёт подпись Ed25519 и CBOM в формате CycloneDX и сделан до того,
как кто-либо за это заплатил. Смысл публикации в том, что ни одной цифре выше верить не нужно.

**Проверка:** `python3 verify.py --self-test`, затем `python3 verify.py`. Зависимостей нет, сети не требуется.
Проверяльщик заново считает хеши всех файлов, перечисленных в подписи, проверяет подпись Ed25519 над подписанным
payload и сверяет ключ каждого комплекта с `PUBLIC-KEY.pem` в корне. Ed25519 реализован в нём дважды —
самостоятельно и через пакет `cryptography`, если тот установлен, — и **обе реализации должны совпасть**.
Самопроверка показывает, что настоящая подпись проходит, реализации согласны, а перевёрнутый байт payload,
подписи или файла обнаруживается.

В `audits/` 60 каталогов, но **52 разных кодовых баз**: 7 из них — англоязычные
версии тех же аудитов, а `trezor-vendored-crypto` — подаудит вложенного каталога внутри `trezor-firmware`. В
итогах они исключены, иначе портфель считал бы себя дважды.

**Срез самостоятельного хранения биткоина:** десять кодовых баз, **693 строк, 448 ломает Шор**. Та же
криптография лежит в трёх разных местах — Jade вносит исходники libwally в своё дерево, Krux подключает `embit`
как git-подмодуль, SeedSigner — тот же `embit` как релиз с PyPI с замком по хешу, — поэтому аудит, не прошедший
по закреплению, объявляет биткоин-подписанта чистым. И три самых рекомендуемых аппаратных кошелька разошлись: у
Trezor постквантовый код работает, включая SLH-DSA в загрузочном заголовке рядом с Ed25519, у BitBox02 и Jade —
ничего.

**Чем это не является:** не криптографический разбор реализаций и не утверждение, что эти проекты слабы; не отчёт
об уязвимостях — инвентаризация говорит, что примитив присутствует и где, а не что он применён неверно; не анализ
достижимости; не реализация миграции.

**Честно об ограничениях.** Инструмент построен при значительной помощи ИИ, но решения принимаются вручную:
сканер предлагает строки-кандидаты, каждая разбирается по реальным исходникам до публикации — в последней партии
75 находок по шести базам, по каждой письменное решение с причиной, 57 подтверждено, 18 неприменимо. Отчёты сами
указывают измеренную историю ложных срабатываний, включая случай, когда **9 из 11 «высоких» оказались ложными и
были отозваны**. Два провала метода, найденные измерением и закрытые тестами: Jade сначала дал 7 строк и ни одного
secp256k1 (поверхностный клон оставляет подмодули пустыми) — после подтягивания 93 строки и 66 Шора; Krux дал 13
строк и одну ECDSA, потому что список пропускаемых каталогов молча переопределил объявленную область с
`vendor/embit`, — прочитанный правильно, 98 строк и 64. Затем перепись сравнила у каждого аудита пути из
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
