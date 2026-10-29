# Два дефекта, из-за которых аудит возвращал чистый результат / Two defects that returned a clean result

Найдено и закрыто 2026-10-29. Оба относятся к одному классу и к самому опасному виду отказа: **не ошибка, а
тишина.** Инструмент не падал, не предупреждал и не писал в отчёт, что чего-то не прочитал — он возвращал
аккуратную, подписанную, маленькую инвентаризацию. Для грантодателя и для клиента такой результат читается как
«здесь чисто».

---

## 1. Обходчик молча переопределял объявленную область аудита

**Что было.** В `backend/app/cli.py` множество `REPO_SKIP_DIRS` содержало `vendor`, и проверка стояла **до**
счётчика `stats["seen"]`. То есть файлы под `vendor/` не попадали ни в разбор, ни в число пропущенных, ни в одну
строку отчёта.

**Как это проявилось.** У `selfcustody/krux` — аппаратного биткоин-кошелька — в области аудита **прямо указан**
`vendor/embit`. Подмодуль подтянулся, каталог был на месте, 153 файла лежали в дереве. Обходчик их не прочитал.
Аудит вернул:

| | строк инвентаризации | ломает Шор | находок | файлов |
|---|---|---|---|---|
| до | 13 | **1** | 3 | 103 |
| после | **98** | **64** | 47 | 257 |

Одна строка ECDSA у аппаратного кошелька для биткоина. Ровно тот же вид результата, который на `Blockstream/Jade`
уже однажды оказался ложным (7 строк вместо 93) — но там причиной был поверхностный клон, а здесь список
пропускаемых каталогов, то есть **код сканера переопределял решение оператора**.

**Почему `embit` дал такой прирост.** `vendor/embit` вкладывает в себя **ещё один** подмодуль — `secp256k1-zkp`
от Blockstream. Поэтому реальная цепочка подписи Krux лежит на два уровня вглубь от его собственного дерева:
`src/krux/key.py` → `vendor/embit/src/embit/` → `vendor/embit/secp256k1/secp256k1-zkp/`. 53 строки ECDSA,
7 Schnorr (BIP-340), 4 Pedersen commitment.

**Чем закрыто.** Правило: **каталог, закреплённый в `.gitmodules`, — это поставляемый исходный код, а не кеш
зависимостей.** Проект выбрал этот коммит, и его содержимое попадает в прошивку, которую устанавливает
пользователь. Новая функция `pinned_dirs(root)` читает корневой `.gitmodules` и выводит такие каталоги из-под
действия и `REPO_SKIP_DIRS`, и `vendored_path()`.

Почему не просто убрать `vendor` из списка: у Go `vendor/` — настоящий воспроизводимый кеш, и
`vendor/github.com/x/y.go` должен оставаться пропущенным. Различает их не имя каталога, а то, закреплён ли он
коммитом.

Своё тестовое дерево у подмодуля остаётся исключённым: аудит сообщает о том, что поставляется.

**И второе, не менее важное: теперь пропущенное считается.** `stats["skipped_dirs"]` попадает в описание аудита:
«N файлов в каталогах сборки или кешах зависимостей не прочитаны». Отчёт, который не говорит, от чего отказался,
позволяет принять скудный результат за чистый.

> [!note] Поправка, сделанная до публикации
> Первая версия увеличивала `stats["pinned"]` на этапе отбора кандидатов, и подписанный отчёт утверждал, что
> «288 файлов прочитаны», когда прочитано было 257 — ошибка на 31 в документе, который несёт подпись. Теперь
> счёт идёт по фактически разобранным файлам.

**Проверка по всему портфелю, чтобы в обороте не оказалось двух видов цифр.** Из 49 целей аудита 16 объявляют
подмодули, и только 3 объявляют подмодуль под пропускаемым каталогом: `krux` и два прогона `trezor-firmware`.
**Ни одна опубликованная цифра не была неверной**, потому что область аудита Trezor
(`crypto core/embed/sec core/embed/projects/bootloader common/protob`) и так не включала `vendor/` — его исключала
кампания, а не обходчик. Но это означает, что цитируемые 111/73/7 у Trezor его **недооценивают**: под `vendor/`
лежат настоящие реализации ML-DSA и SPHINCS+. Они измерены отдельным комплектом `trezor-vendored-crypto`, а не
правкой цифр, уже процитированных в живой заявке.

Закреплено тестом `test_a_submodule_the_tree_pins_is_shipped_source_not_a_dependency_cache`.

---

## 2. Референсная реализация стандарта может ни разу не назвать его имя

**Что было.** Аудит трёх примитивов, закреплённых Trezor под `vendor/`, прочитал **123 файла референсной
реализации SPHINCS+ и дал ноль строк SLH-DSA.** При этом *место вызова* в загрузочном заголовке Trezor
находилось — то есть инвентаризация могла назвать SLH-DSA в корне доверия и промолчать о реализации под ним.

**Причина.** `sphincs/sphincsplus` называет себя `SPX_*` и `spx_ctx` и объявляет `CRYPTO_ALGNAME "SPHINCS+"`.
Слов «SLH-DSA» и `slh_dsa` в нём нет вообще. Существующие шаблоны покрывали liboqs, BouncyCastle, noble, OpenSSL
`EVP_PKEY_SLH_DSA`, Rust `slh_dsa::`, путь включения `sphincsplus/ref/*.h` и литералы наборов параметров — то
есть **все способы вызвать**, но ни одного способа реализовать. Это тот же пробел, что был найден на HKDF в
`rustls`, только на поколение стандартов позже.

**Чем закрыто.** Добавлен шаблон в `pqc.yaml` под `slh-dsa`:

```
CRYPTO_ALGNAME\s+"SPHINCS\+"|\bspx_ctx\b|\bSPX_(?:N|D|BYTES|SK_BYTES|PK_BYTES|TREE_HEIGHT|FULL_HEIGHT|WOTS_\w+|FORS_\w+|ADDR_TYPE_\w+)\b|\b(?:fors_sign|fors_pk_from_sig|wots_pk_from_sig|wots_gen_sk)\b
```

**Имена макросов перечислены, а не взяты как `SPX_\w+`, намеренно: `SPX` — это ещё и биржевой индекс.** Тест
закрепляет пять промахов (`const symbol = "SPX";`, `SPX_TIMEOUT_MS`, `struct spx_device`) рядом с пятью
попаданиями из референсного дерева.

**ML-DSA не потребовал ничего:** `mldsa-native` пишет `mldsa_native.h` и `MLDSA44_PUBLICKEY_SIZE`, и до этих
шаблонов уже доставали существующие. Именно поэтому тот же аудит нашёл 8 строк ML-DSA и ни одной SLH-DSA — что и
было сигналом, что дело в шаблонах, а не в дереве.

**Измерение влияния на портфель.** Кодовый поиск GitHub по 42 уникальным репозиториям аудита: **ни один не
содержит кода SPHINCS+ в собственном дереве** (поиск индексирует файлы репозитория, но не его подмодули — а
случай подмодуля уже перечислен по `.gitmodules` всех целей). Значит, новые шаблоны не меняют ни один
опубликованный комплект.

---

## 3. Правило «закреплено = поставляется» дважды перегнуло, и оба раза урок один

Для прошивки закреплённый подмодуль — действительно поставляемый код. Для закреплённого **тестового** дерева —
нет.

* **`lidofinance/core`** закрепляет `foundry/lib/forge-std`. Подтягивание добавило 9 строк Keccak-256 и
  **4 находки `SOL-FLOATING-PRAGMA` про тестовую обвязку Foundry, а не про контракты Lido.**
* **`wycheproof`** — корпус тестовых векторов Google, закреплённый у `trezor-firmware` и `rustcrypto-rsa`. Чтение
  его как поставляемого кода инвентаризировало бы каждый алгоритм, на который кто-либо когда-либо написал вектор.

Оба имени добавлены в `TEST_DIRS` (`forge-std`, `ds-test`, `wycheproof`), а не в список vendored, — так
`--include-tests` при необходимости до них всё ещё достаёт. **Перечислены по именам намеренно:** правило «всё под
`lib/`» исключило бы `lib/solidity-utils` у `aave-v3-origin`, а это код, который поставляется.

Проверено на цели, о которой я не думал: у `bitcoin-core/secp256k1` есть собственный каталог `src/wycheproof/`.
Исключены 5 файлов, 4 из них и раньше отсекались по именам `*_test.json`/`*_test.h`, а новым оказался ровно один —
`WYCHEPROOF_COPYING`, файл лицензии. Инвентаризация не изменилась: 38 строк из 38 ломает Шор. `lido-core` вернулся
к исходным 267 файлам и 69 строкам.

## 4. Перепись: у 23 подмодулей в области аудита файлы не доходили до сканера

Дефект Jade как совокупность, а не как случай. Скрипт `scratchpad/submodule_census.py` сравнивает объявленные в
`.gitmodules` пути каждой цели с путями, которые её собственный комплект называет разобранными; подмодуль вне
объявленной области считается ожидаемо отсутствующим и в дефект не записывается.

**Первый прогон 2026-10-29 дал 23 отсутствующих — и из них 5 оказались правильным поведением,** потому что
закреплённые тестовые обвязки и корпусы векторов на тот момент ещё не были классифицированы (см. раздел 3).
Сама перепись сообщала о собственной корректной работе как о дефекте, и опубликованное число 23 было по этой
причине неверным. Исправленная перепись теперь спрашивает у кода, должен ли подмодуль быть исключён, прежде чем
называть его пропущенным.

**Состояние после всех правок: 15 подмодулей в области разобраны, 63 правомерно отсутствуют как вне области,
5 исключены по замыслу (тест/vendored), и 14 находятся в области и ОТСУТСТВУЮТ — все четырнадцать в одном
`nitro`.** Два настоящих дефекта были коммерчески
живыми, потому что их цифры процитированы в заявках, и оба исправлены:

| комплект | отсутствовавший подмодуль | было | стало |
|---|---|---|---|
| `bitbox02-firmware` | `src/rust/bitbox-secp256k1/depend/secp256k1-zkp` | 81 строка / 36 Шора / 589 файлов | **136 / 90 / 721** |
| `libwally-core` | `src/secp256k1` | 26 строк / 6 Шора / 122 файла | **81 / 60 / 254** |

У BitBox02 экспозиция Шора оказалась **в 2,5 раза** больше, у libwally — **в 10 раз**. Русский и англоязычный
прогоны BitBox02 совпали до строки, то есть двуязычный шлюз это пережил.

**Почему `nitro` оставлен, а не доделан.** Его сохранённый комплект разобрал 1 038 файлов и все они — код самой
Arbitrum (`nitro-reth`, `crates`, `arbnode`, `arbos`, `cmd`, `bold`, …). Отсутствующие 14 подмодулей это чужие
проекты: `go-ethereum`, `brotli`, `wasmer`, `openzeppelin-contracts`, спецификационный набор тестов WASM и
примеры программ на rust/c/bf для него. То есть комплект и так отвечает на вопрос «что в коде Arbitrum», а
«подтянуть всё» означало бы влить ~5 000 файлов апстримного geth в инвентаризацию Arbitrum и назвать это её
экспозицией. Правильное решение — явная область, как у `trezor-firmware`, и отдельный аудит geth, если он кому-то
понадобится; к живым заявкам `nitro` отношения не имеет, поэтому это отложено, а не сделано наспех.

`aave-v3-origin/lib/solidity-utils` и `scroll/scroll-contracts` были настоящими дефектами и исправлены:
**aave-v3-origin 19 строк → 89, 225 файлов → 645, 23 находки → 58; scroll 30 строк → 78, 224 файла → 387,
73 находки → 115.** Первая — библиотека BGD, которую импортируют контракты Aave, вторая — собственные контракты
Scroll, выделенные во второй репозиторий; обе действительно поставляются, поэтому обе в области.

> [!warning] Итоговые цифры портфеля — это нижняя граница
> Пока перепись не чиста, суммы по портфелю следует называть границей снизу, и так и писать во внешних текстах.
> На 2026-10-29: **51 подписанный комплект, 43 кодовые базы, 2 798 строк инвентаризации, 1 346 ломает Шор,
> 29 постквантовых.** Срез самостоятельного хранения из десяти репозиториев: **629 строк, 440 Шора (70 %), 7
> постквантовых — все у Trezor.**

**Что это значит для уже отправленного письма в Galaxy.** Письмо от 2026-10-28 называет «830 строк, 604 ломает
Шор» по шести базам, включая BitBox02. По исправленным комплектам эти шесть дают **885 строк и 658 Шора**.
Утверждение письма не было ложным — оно занижало, причём в сторону собственного аргумента, и письмо прямо
называет цифры инвентаризацией на зафиксированных коммитах. Но воспроизвести 830/604 из текущих комплектов уже
нельзя, поэтому прежние значения сохранены в `_before-2026-10-29/` и при ответе Galaxy цифры следует назвать
исправленными, объяснив, чем именно.

## Что из этого продаётся

Структурная находка, которой нет ни в одном отчёте по одному репозиторию: **одна и та же криптография лежит в
трёх разных местах, и аудит, не идущий по закреплению, объявляет подписывающее устройство чистым.**

| устройство | где лежит его криптография | строк | Шор |
|---|---|---|---|
| `Blockstream/Jade` | исходники libwally внесены в дерево | 93 | 66 |
| `selfcustody/krux` | `embit` как git-подмодуль, а в нём ещё `secp256k1-zkp` | 98 | 64 |
| `BitBoxSwiss/bitbox02-firmware` | `secp256k1-zkp` подмодулем внутри своего Rust-крейта | 136 | 90 |
| `SeedSigner/seedsigner` | `embit==0.8.0` релизом с PyPI с замком по хешу | 7 | **1** |

Строка SeedSigner **верна**. Экспозиция реальна, её просто нет в том репозитории, который кто-либо стал бы
аудировать — и это лучшая практика по цепочке поставок (пин с хешем), которая одновременно делает экспозицию
невидимой для обычного аудита.

Все три в итоге сводятся к `bitcoin-core/secp256k1`: **38 строк инвентаризации, Шор ломает все 38, постквантового
кода нет.**

---

# ENGLISH

Found and closed on 2026-10-29. Both belong to the same class and to the most dangerous kind of failure: **not an
error, but silence.** The tool did not crash, did not warn, and did not record in the report that it had declined
to read anything — it returned a tidy, signed, small inventory. To a funder or a client, that reads as "this is
clean".

## 1. The walker silently overrode the declared audit scope

`REPO_SKIP_DIRS` in `backend/app/cli.py` contained `vendor`, and the check ran **before** `stats["seen"]` was
incremented — so files under `vendor/` reached neither the analysis, nor the skipped count, nor any line of the
report.

`selfcustody/krux` is a Bitcoin hardware wallet whose audit scope **explicitly named** `vendor/embit`. The
submodule materialised, the directory was there, 153 files sat in the tree, and the walker read none of them. The
audit returned **13 inventory rows and a single ECDSA row**. Following the pin gives **98 rows and 64
Shor-breakable** (3 → 47 findings, 103 → 257 files). This is the same shape of result that
`Blockstream/Jade` once produced falsely (7 rows instead of 93) — but there the cause was a shallow clone, and
here it was the scanner's own skip list **overriding the operator's decision**.

The size of the jump is explained by nesting: `vendor/embit` pins **another** submodule, Blockstream's
`secp256k1-zkp`, so Krux's real signing chain sits two levels below its own tree —
`src/krux/key.py` → `vendor/embit/src/embit/` → `vendor/embit/secp256k1/secp256k1-zkp/`, giving 53 ECDSA rows,
7 Schnorr (BIP-340) and 4 Pedersen commitment.

**The rule now: a directory a `.gitmodules` pins is shipped source, not a dependency cache.** The project chose
that commit and its contents ship in the firmware a user installs. `pinned_dirs(root)` reads the root
`.gitmodules` and exempts those subtrees from both `REPO_SKIP_DIRS` and `vendored_path()`. Deleting `vendor` from
the list wholesale would be wrong: Go's `vendor/` is a genuinely reproducible cache and
`vendor/github.com/x/y.go` must stay excluded. What separates them is not the directory's name but whether a
commit pins it. A pinned submodule's own test tree stays excluded, because the audit reports what ships.

**And everything skipped is now counted**, and said in the audit description: "N files in build-output or
dependency-cache directories were not read." A report that does not say what it declined to read lets a thin
result pass for a clean one.

*A correction made before publishing:* the first version counted `stats["pinned"]` at shortlist time, and the
signed report then claimed 288 files were read when 257 were — wrong by 31 in a document that carries a
signature. It now counts what was actually analysed.

**Portfolio check,** so a detection change does not leave two kinds of figure in circulation: of 49 audit
targets, 16 declare submodules and only 3 declare one under a skipped directory — `krux` and the two
`trezor-firmware` runs. **No published figure was wrong**, because Trezor's campaign scope never included
`vendor/` at all: the campaign excluded it, not the walker. That does mean Trezor's cited 111/73/7 *understates*
it — `vendor/` holds the real ML-DSA and SPHINCS+ implementations, measured as a separate
`trezor-vendored-crypto` bundle rather than by editing numbers already quoted in a live application.

## 2. A standard's reference implementation may never write the standard's name

Auditing the three primitives Trezor pins under `vendor/` read **123 files of the SPHINCS+ reference
implementation and produced zero SLH-DSA rows**, while the *call site* in Trezor's boot header was found — so the
inventory could name SLH-DSA in the root of trust and stay silent about the implementation beneath it.

`sphincs/sphincsplus` calls itself `SPX_*` and `spx_ctx` and declares `CRYPTO_ALGNAME "SPHINCS+"`; the words
"SLH-DSA" and `slh_dsa` appear nowhere in it. The existing patterns covered liboqs, BouncyCastle, noble, OpenSSL
`EVP_PKEY_SLH_DSA`, Rust `slh_dsa::`, the include path `sphincsplus/ref/*.h` and the parameter-set literals —
every way of *calling* it and no way of *implementing* it. That is the same blind spot found on HKDF in `rustls`,
one generation of standards later.

The macro names in the new pattern are **enumerated rather than matched as `SPX_\w+` on purpose: a bare SPX is
also a stock index**, and the test pins five near misses beside five positives from the reference tree. ML-DSA
needed nothing, because `mldsa-native` writes `mldsa_native.h` and `MLDSA44_PUBLICKEY_SIZE`, which the existing
patterns already reach — which is exactly why the same audit found 8 ML-DSA rows and no SLH-DSA, and why the
patterns rather than the tree were the suspect.

**Impact measured:** GitHub code search across all 42 unique audited repositories found **none carrying SPHINCS+
code in its own tree** (code search indexes a repository's own files, not its submodules — and the submodule case
was already enumerated from every target's `.gitmodules`). So the new patterns change no published bundle.

## 3. The rule overreached twice, and both corrections are one lesson

"Pinned means shipped" is true for firmware and false for a pinned *test* tree. `lidofinance/core` pins
`foundry/lib/forge-std`, and materialising it added nine Keccak-256 rows and **four `SOL-FLOATING-PRAGMA`
findings about Foundry's test harness rather than about Lido's contracts**. Google's `wycheproof` vector corpus,
pinned by `trezor-firmware` and `rustcrypto-rsa`, would have inventoried every algorithm anyone ever wrote a
vector for. Both names now sit in `TEST_DIRS` (`forge-std`, `ds-test`, `wycheproof`) rather than in the vendored
list, so `--include-tests` can still reach them — and they are **named one by one on purpose**, because a blanket
`lib/` rule would have excluded `aave-v3-origin`'s `lib/solidity-utils`, which does ship.

It then proved itself on a target I had not considered: `bitcoin-core/secp256k1` keeps its own `src/wycheproof/`
vectors. Five files are excluded, four of which already were by their `*_test.json`/`*_test.h` names, so exactly
one is new — `WYCHEPROOF_COPYING`, a licence file — and the inventory is unchanged at 38 of 38 Shor-breakable.
`lido-core` returned to its original 267 files and 69 rows.

## 4. The census: 23 in-scope submodules never reached the scanner

The Jade defect as a population rather than an anecdote. `scratchpad/submodule_census.py` compares each target's
declared `.gitmodules` paths against the paths its own bundle says it parsed, treating a submodule outside the
declared scope as an expected absence rather than a defect.

**The first run on 2026-10-29 reported 23 absences, and 5 of those turned out to be correct behaviour**, because
pinned test harnesses and vector corpora had not yet been classified (section 3). The census was reporting its own
correct work as a defect, which is why the published figure of 23 was wrong; it now asks the code whether a
submodule is supposed to be excluded before calling it missing.

**State after every fix: 15 in-scope submodules parsed, 63 correctly absent as out of scope, 5 excluded by design
(test or vendored), and 14 in scope and ABSENT — every one of the fourteen in `nitro`.** The two genuine defects that were
commercially live, because their figures are quoted in applications, are both fixed:
`bitbox02-firmware` was missing `src/rust/bitbox-secp256k1/depend/secp256k1-zkp` and went from
**81 rows / 36 Shor-breakable / 589 files to 136 / 90 / 721**; `libwally-core` was missing `src/secp256k1` and
went from **26 / 6 / 122 to 81 / 60 / 254**. That is 2.5× more Shor exposure for BitBox02 and **ten times** for
libwally. The Russian and English BitBox02 runs reproduce each other to the row, so the bilingual gate survived
the change. **Why `nitro` is deferred rather than finished.** Its stored bundle parsed 1,038 files and every one of them is
Arbitrum's own code (`nitro-reth`, `crates`, `arbnode`, `arbos`, `cmd`, `bold`, …). The 14 absent submodules are
other people's projects: `go-ethereum`, `brotli`, `wasmer`, `openzeppelin-contracts`, the WASM specification test
suite and the rust/c/bf sample programs written for it. So the bundle already answers "what is in Arbitrum's
code", and materialising everything would pour some 5,000 files of upstream geth into Arbitrum's inventory and
call it Arbitrum's exposure. The right answer is an explicit scope, as `trezor-firmware` has, plus a separate
audit of geth if anyone wants one — and since `nitro` bears on no live application, that is deferred deliberately
rather than done in a hurry.

`aave-v3-origin/lib/solidity-utils` and `scroll/scroll-contracts` were genuine defects and are fixed:
**aave-v3-origin 19 rows → 89, 225 files → 645, 23 findings → 58; scroll 30 rows → 78, 224 files → 387, 73
findings → 115.** The first is BGD's library, which Aave's contracts import; the second is Scroll's own contracts
split into a second repository. Both genuinely ship, so both belong in scope.

**So portfolio totals are a floor until that census is clean, and outward-facing prose should say so.** As of
2026-10-29: **51 signed bundles, 43 codebases, 2,798 inventory rows, 1,346 Shor-breakable, 29 post-quantum.** The
ten-repository self-custody slice: **629 rows, 440 Shor-breakable (70%), 7 post-quantum, all of them Trezor's.**

**What this means for the Galaxy letter already sent.** The letter of 2026-10-28 states "830 inventory rows, 604
breakable by Shor's algorithm" across six codebases including BitBox02. On the corrected bundles those six give
**885 rows and 658 Shor-breakable**. Nothing the letter claimed was false — it understated, in the direction of
its own argument, and it describes its figures as inventory at pinned commits. But 830/604 can no longer be
reproduced from the current bundles, so the previous reports are kept in `_before-2026-10-29/` and any reply to
Galaxy should give the corrected figures and say what changed.

## What of this is saleable

The structural finding, which no single-repository report contains: **the same cryptography lives in three
different places, and an audit that does not follow the pin declares a signing device clean.** Jade vendors
libwally's C source in-tree (93 rows, 66 Shor-breakable). Krux pins `embit` as a git submodule which nests
`secp256k1-zkp` again (98, 64). BitBox02 pins `secp256k1-zkp` inside its own Rust crate (136, 90). SeedSigner
pins `embit==0.8.0` as a hash-locked PyPI release, so its row reads 7
and **is correct** — the exposure is real and simply is not in the repository anyone would audit, which is to say
that excellent supply-chain practice is also what makes the exposure invisible to an ordinary audit. All three
reduce to `bitcoin-core/secp256k1`: **38 inventory rows, 38 of them Shor-breakable, no post-quantum code.**
