# Cryptographic inventories of open-source code, signed and reproducible

51 audit bundles over **43 codebases**: a machine-readable inventory of every cryptographic
primitive the scanner found, what it is used for, and what a quantum computer does to it. Across those codebases
**2,798 inventory rows**, of which **1,346 fall to Shor's algorithm** and **27 are already
post-quantum**, from **27,469 parsed files**.

Every bundle is pinned to an upstream commit, carries an Ed25519 signature and a CycloneDX CBOM, and was produced
before anyone paid for it. The point of publishing them is that you do not have to believe any of the numbers
above.

## Check it yourself

No dependencies, no network, nothing to install:

```
python3 verify.py --self-test     # test the verifier before trusting what it says
python3 verify.py                 # verify all 51 bundles
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
The three zeros are the interesting part and are not a statement about what those wallets can do: `bdk` delegates
signing to `rust-bitcoin` and `rust-secp256k1`, `seedsigner` to a hash-locked `embit` release, and
`rust-bitcoin` holds taproot types while the Schnorr signatures live in `rust-secp256k1`. **Readiness for a
consensus change cannot be read off a single repository** — which is the same defect that once made a Bitcoin
signer measure 13 inventory rows instead of 98. Presence of a primitive is necessary and not sufficient: P2MR
also needs address encoding, descriptors and PSBT support. The full argument, with the primary quotations, is in
`reports/BIP-360-361-READINESS-2026-10-29.md`.

## Layout

```
PUBLIC-KEY.pem     the one key that signed every bundle
verify.py          standalone verifier
readiness.py       BIP-360 / BIP-361 readiness, measured from the bundles
audits/<name>/     report.json · report.md · report.html · report.pdf · cbom.cdx.json
                   report.sarif.json · bundle.sig.json · report.sig.json · public_key.pem
                   brief.en.md · brief.ru.md (+ pdf)
reports/           the write-ups: re-audits, triage, adoption survey, scope-and-recall study,
                   and the BIP-360/361 readiness analysis
```

`audits/` holds 51 directories but **43 distinct codebases**: 7 of them
(`bitbox02-firmware-en`, `bitgo-mpc-en`, `coinbase-cb-mpc-en`, `fireblocks-mpc-lib-en`, `librustzcash-en`, `trezor-firmware-en`, `trustwallet-wallet-core-en`) are English renderings of an audit also present in Russian, and
`trezor-vendored-crypto` is a sub-audit of a vendored directory inside `trezor-firmware`. Totals on this page
exclude all 8 so nothing is counted twice.

## The Bitcoin self-custody slice

Ten codebases, **629 inventory rows, 440 Shor-breakable**. This is the slice cited in grant
applications, so it is here in full.

| codebase | upstream | commit | files | inventory rows | Shor-breakable | post-quantum |
|---|---|---|---:|---:|---:|---:|
| `bitbox02-firmware` | BitBox (Shift Crypto) | `ae548ef4e40f` | 721 | 136 | 90 | 0 |
| `trezor-firmware` | SatoshiLabs (Trezor) | `72489948b3c4` | 411 | 111 | 73 | 7 |
| `jade` | Blockstream (Jade) | `a59d14c2b397` | 568 | 93 | 66 | 0 |
| `krux` | Krux (selfcustody) | `9b3a4314a205` | 257 | 98 | 64 | 0 |
| `libwally-core` | Blockstream (libwally) | `374df231d054` | 254 | 81 | 60 | 0 |
| `secp256k1` | Bitcoin Core (libsecp256k1) | `1b4181f93f7a` | 99 | 38 | 38 | 0 |
| `rust-secp256k1` | rust-secp256k1 | `fe8b3bec962f` | 127 | 36 | 36 | 0 |
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
| `agave` | Anza (Solana) | `7700cb3128c1` | 1293 | 189 | 103 | 0 |
| `bitbox02-firmware` | BitBox (Shift Crypto) | `ae548ef4e40f` | 721 | 136 | 90 | 0 |
| `bitwarden-sdk` | Bitwarden | `25b6c8c3860a` | 1625 | 119 | 12 | 5 |
| `trezor-firmware` | SatoshiLabs (Trezor) | `72489948b3c4` | 411 | 111 | 73 | 7 |
| `nitro` | Offchain Labs (Arbitrum) | `ccc5c828d9ea` | 1038 | 108 | 13 | 0 |
| `coinbase-cb-mpc` | Coinbase | `0b716706f998` | 174 | 103 | 88 | 2 |
| `rustls` | rustls project | `84bf9eaa9857` | 137 | 103 | 29 | 0 |
| `ethers-js` | ethers.js project | `3ea4c226dd0b` | 759 | 100 | 29 | 0 |
| `foundry` | Foundry (Paradigm) | `7f0a409a5c20` | 761 | 100 | 16 | 0 |
| `krux` | Krux (selfcustody) | `9b3a4314a205` | 257 | 98 | 64 | 0 |
| `jade` | Blockstream (Jade) | `a59d14c2b397` | 568 | 93 | 66 | 0 |
| `bitgo-mpc` | BitGo | `3c892fd6a388` | 271 | 91 | 66 | 0 |
| `aave-v3-origin` | Aave DAO | `8305565ae342` | 645 | 89 | 2 | 0 |
| `fireblocks-mpc-lib` | Fireblocks | `00ae08b7f1bd` | 123 | 89 | 87 | 0 |
| `libwally-core` | Blockstream (libwally) | `374df231d054` | 254 | 81 | 60 | 0 |
| `scroll` | Scroll | `3046bbd18a6a` | 387 | 78 | 7 | 0 |
| `lido-core` | Lido | `2bd532298d85` | 267 | 69 | 7 | 0 |
| `rabby` | Rabby Wallet (DeBank) | `663c0e80e9f6` | 1694 | 66 | 29 | 0 |
| `reown-appkit` | Reown (ex-WalletConnect) | `8f9f39f1dfe0` | 1249 | 66 | 16 | 0 |
| `openpgpjs` | OpenPGP.js project | `8bc35df48879` | 108 | 65 | 35 | 8 |
| `metamask-extension` | MetaMask (Consensys) | `d2db7ee9a19b` | 4873 | 50 | 12 | 0 |
| `librustzcash` | Electric Coin Company (Zcash) | `8672a4b2d60f` | 333 | 46 | 19 | 0 |
| `rage` | str4d (rage / age encryption) | `b5b68c4f4f7e` | 54 | 43 | 13 | 3 |
| `noir` | Aztec / Noir | `5c98fecd3fe6` | 783 | 39 | 9 | 0 |
| `secp256k1` | Bitcoin Core (libsecp256k1) | `1b4181f93f7a` | 99 | 38 | 38 | 0 |
| `rust-secp256k1` | rust-secp256k1 | `fe8b3bec962f` | 127 | 36 | 36 | 0 |
| `monero` | Monero | `3fd0f88c20f5` | 580 | 34 | 14 | 0 |
| `safe-smart-account` | Safe | `247b8ce3bdbf` | 77 | 33 | 5 | 0 |
| `rust-bitcoin` | rust-bitcoin | `f127ba2ae14e` | 125 | 28 | 11 | 0 |
| `zebra` | Zcash Foundation | `147a6a8bf7d3` | 439 | 27 | 14 | 0 |
| `signal-desktop` | Signal Messenger | `17502b9d1a9e` | 2202 | 22 | 0 | 2 |
| `cairo` | StarkWare | `68a61f6c6251` | 567 | 18 | 10 | 0 |
| `zcash-android-wallet-sdk` | Electric Coin Company (Zcash) | `a95780ac00e0` | 350 | 14 | 2 | 0 |
| `zcash-swift-wallet-sdk` | Electric Coin Company (Zcash) | `4895ee058da9` | 205 | 12 | 2 | 0 |
| `rustcrypto-rsa` | RustCrypto project | `f96c4b5d629a` | 35 | 11 | 6 | 0 |
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
cryptography lives in one; materialised, it is 93 rows and 66 Shor-breakable. Krux measured 13 rows and a single
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

51 подписанных комплектов аудита по **43 кодовым базам**: машиночитаемая инвентаризация
криптографических примитивов — какой алгоритм, где, для чего, и что с ним делает квантовый компьютер. Всего
**2,798 строк инвентаризации**, из них **1,346 ломает алгоритм Шора**, и **27 уже
постквантовых**; разобрано **27,469 файлов**.

Каждый комплект привязан к коммиту апстрима, несёт подпись Ed25519 и CBOM в формате CycloneDX и сделан до того,
как кто-либо за это заплатил. Смысл публикации в том, что ни одной цифре выше верить не нужно.

**Проверка:** `python3 verify.py --self-test`, затем `python3 verify.py`. Зависимостей нет, сети не требуется.
Проверяльщик заново считает хеши всех файлов, перечисленных в подписи, проверяет подпись Ed25519 над подписанным
payload и сверяет ключ каждого комплекта с `PUBLIC-KEY.pem` в корне. Ed25519 реализован в нём дважды —
самостоятельно и через пакет `cryptography`, если тот установлен, — и **обе реализации должны совпасть**.
Самопроверка показывает, что настоящая подпись проходит, реализации согласны, а перевёрнутый байт payload,
подписи или файла обнаруживается.

В `audits/` 51 каталогов, но **43 разных кодовых баз**: 7 из них — англоязычные
версии тех же аудитов, а `trezor-vendored-crypto` — подаудит вложенного каталога внутри `trezor-firmware`. В
итогах они исключены, иначе портфель считал бы себя дважды.

**Срез самостоятельного хранения биткоина:** десять кодовых баз, **629 строк, 440 ломает Шор**. Та же
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
