# Кто уже начал постквантовую миграцию, а кто нет / Who has already begun the post-quantum migration

Измерено 2026-10-28 по 33 уникальным подписанным аудитам (англоязычные повторы исключены, иначе семь
репозиториев считались бы дважды). Каждая цифра воспроизводится из `report.json` соответствующего комплекта;
подписи проверяются, расхождений с собой нет.

**Почему этого отчёта не существовало до сегодня.** Инвентаризация с самого начала различала статусы `pqc` и
`hybrid` — уже постквантовые строки, — но ни одна сводка их не показывала: все сводки считали уязвимое. Пробел
обнаружился при сборке табличного представления, когда сумма по столбцам не сошлась с числом строк. Это и есть
более продаваемая половина продукта: не «всё сломано», а **кто начал, в каком файле и на какой строке, и кто не
начал**.

---

## Итог

**8 из 33 аудированных кодовых баз содержат постквантовую криптографию. 25 содержат криптографию, уязвимую к
Шору, и ни одной постквантовой строки.**

| репозиторий | PQ | Шор | строк | что именно |
|---|---|---|---|---|
| `openpgpjs` | 8 | 35 | 65 | ML-DSA-65 ×3, ML-KEM-768 ×3, библиотека ×2 |
| `trezor-firmware` | 7 | 73 | 111 | ML-DSA ×6 (в т.ч. ML-DSA-44), SLH-DSA ×1 |
| `bitwarden-sdk` | 5 | 12 | 119 | ML-DSA ×3, библиотека ×2 |
| `rage` | 3 | 13 | 43 | библиотека ×3 |
| `coinbase-cb-mpc` | 2 | **88** | 103 | ML-KEM-768 ×2 |
| `signal-desktop` | 2 | 0 | 22 | ML-KEM ×2 |
| `foundry` | 1 | 16 | 100 | X25519MLKEM768 (гибрид) |
| `rustls` | 1 | 29 | 103 | X25519MLKEM768 (гибрид) |

По портфелю: **ML-DSA 12 строк, ML-KEM 7, объявленных PQC-библиотек 7, X25519MLKEM768 2, SLH-DSA 1.**

---

## Четыре вывода, которых не видно из одного репозитория

### 1. Из трёх MPC-библиотек кастодианов постквантовый примитив есть только у одной — и он не подключён

| библиотека | строк | Шор | доля | PQ |
|---|---|---|---|---|
| `coinbase-cb-mpc` | 103 | 88 | 85 % | **ML-KEM-768, реализован** |
| `fireblocks-mpc-lib` | 89 | 87 | **98 %** | нет |
| `bitgo-mpc` | 91 | 66 | 73 % | нет |

У Coinbase это `include-internal/cbmpc/internal/crypto/mlkem768.h` и `src/cbmpc/crypto/mlkem768.cpp` —
`mlkem768_pub_key_t` и `mlkem768_prv_key_t` с `encapsulate` и `decapsulate`. **Но подключают его только его же
`.cpp`, `CMakeLists.txt` и `tests/unit/crypto/test_mlkem768.cpp`.** Путь publicly verifiable encryption, которым
шифруются резервные копии долей ключа, его не использует.

Это важно, потому что именно PVE — самая срочная экспозиция во всём срезе: зашифрованные доли **хранятся**, то
есть снятая сегодня копия становится открытым текстом, когда появится CRQC, и никакая последующая миграция этого
не отменит. У Coinbase нужный для этого KEM **уже построен и не соединён с местом, где он нужен** — это работа по
подключению, а не исследовательская задача. У Fireblocks и BitGo и примитива нет.

### 2. Два ведущих аппаратных кошелька разошлись

| | строк | Шор | PQ |
|---|---|---|---|
| `trezor-firmware` | 111 | 73 | **7** |
| `bitbox02-firmware` | 81 | 36 | **0** |

У Trezor это не декларация в манифесте, а работающий код: модуль `core/embed/sec/mldsa44/`, аттестация MCU на
ML-DSA (`core/embed/sec/mcu_attestation/`), **SLH-DSA в `core/embed/sec/image/boot_header.c:30` — то есть в самом
корне доверия**, и поставляемый сертификат X.509 с открытым ключом **ML-DSA-44**
(`core/embed/sec/secret/unix/certs/T3W1.der`, «T3W1 Trezor Safe»). Корень доверия Trezor несёт обе схемы
одновременно: Ed25519 на строке 81 того же файла и SLH-DSA на строке 30. Это переход в середине, а не
нетронутое состояние.

### 3. Гибридный обмен ключами дошёл до TLS и ни до одного кошелька

`X25519MLKEM768` — ровно та гибридная конструкция, которую рекомендуют для «собери сейчас, расшифруй потом», —
присутствует в `rustls` и в `foundry` (через ту же библиотеку TLS). **В аудированных кошельках, SDK и
MPC-библиотеках её нет ни разу.** При этом обмен ключами — именно то место, где ретроспективный риск реален:
подпись можно сменить потом, а записанный сегодня сеанс расшифруют позже.

### 4. Крупнейший разрыв в портфеле

| репозиторий | Шор | строк | доля | PQ |
|---|---|---|---|---|
| `trustwallet-wallet-core` | **254** | 355 | 72 % | 0 |
| `agave` (валидатор Solana) | 103 | 189 | 55 % | 0 |
| `fireblocks-mpc-lib` | 87 | 89 | 98 % | 0 |
| `bitgo-mpc` | 66 | 91 | 73 % | 0 |
| `bitbox02-firmware` | 36 | 81 | 44 % | 0 |

---

## Чего этот отчёт не утверждает

Эти оговорки не формальность: без них отчёт утверждал бы о вендорах то, что данными не подкреплено.

* **Отсутствие строки — это отсутствие в аудированной области, а не доказательство, что вендор ничего не делает.**
  Каждый аудит ограничен областью и зафиксированным коммитом; работа могла идти в другой ветке, в другом
  репозитории или в закрытом коде.
* **`signal-desktop` с нулём строк Шора — почти наверняка граница области, а не постквантовая готовность.**
  Криптография Signal живёт в нативных библиотеках за пределами TypeScript-дерева. Читать как «в разобранных
  файлах не найдено».
* **Строки «PQC library» — это объявления зависимостей**, а не доказательство использования. У `rage` все три
  строки такие, то есть библиотека подключена; вызовы не прослеживались.
* **Это не криптографический разбор** ни одной из реализаций: инвентаризация говорит, что примитив присутствует и
  где, а не что он применён корректно.
* Срез — шесть репозиториев Zcash и `monero` постквантовых строк не содержат; для Zcash это ожидаемо, поскольку
  соответствующая работа идёт в Epoch и Tachyon, то есть вне аудированных деревьев.

---

## Дополнение 2026-10-29: исправленные знаменатели и то, что Trezor действительно закрепляет

Сам вывод не изменился — изменились два основания, и прежние цифры выше сохранены как есть, чтобы видно было, что
именно сдвинулось.

**1. Знаменатель был 33, стал 43.** В портфель добавились `bitcoin-core/secp256k1`, `SeedSigner`, `Krux` и ещё
ряд комплектов. Корректная формулировка теперь: **8 из 43 аудированных кодовых баз содержат постквантовую
криптографию, 33 содержат уязвимую к Шору и ни одной постквантовой, 2 не содержат ни того ни другого**
(`lottery-demo` и `zodl-android` — у обоих криптография за пределами аудированной области). Доля «начавших» при
этом **упала с 24 % до 19 %**, и это не ухудшение состояния отрасли, а следствие того, что добавленные
репозитории — библиотеки подписи, где постквантового кода нет вовсе.

**2. Цифры BitBox02 были занижены.** Перепись подмодулей (см. [[SCOPE-AND-RECALL-2026-10-29]]) показала, что
`bitbox02-firmware` закрепляет `secp256k1-zkp` внутри своего Rust-крейта и этот подмодуль ни разу не доходил до
сканера. Исправлено: **136 строк, 90 ломает Шор** вместо 81 / 36. Постквантовых строк по-прежнему **ноль**, то
есть вывод №2 выше — расхождение Trezor и BitBox02 — не только сохраняется, но усиливается: у BitBox02 теперь
в 2,5 раза больше известной экспозиции и ровно столько же постквантового кода, сколько было.

**3. Trezor закрепляет не заголовок, а полные референсные реализации — и до 2026-10-29 инвентаризация их не
видела.** Область основного аудита Trezor покрывает места вызова (`core/embed/sec`), а реализации лежат
подмодулями под `vendor/`, вне этой области. Отдельный комплект `trezor-vendored-crypto` их читает:
**142 строки, 38 ломает Шор, 102 постквантовых — ML-DSA 8 и SLH-DSA 94.**

> [!warning] 94 — самая легко искажаемая цифра во всём портфеле
> Это по одной строке на файл **полной** апстримной реализации SPHINCS+: четыре бэкенда (`ref/`, `haraka-aesni/`,
> `sha2-avx2/`, `shake-a64/`, `shake-avx2/`) и 18 заголовков наборов параметров. Микроконтроллер Trezor не может
> исполнять код AVX2 или AArch64 вообще, а сборка компилирует ровно один набор параметров. Честная формулировка —
> **«Trezor закрепляет целиком референсную реализацию SPHINCS+ и собирает из неё одну конфигурацию»**, и это
> гораздо более веское свидетельство реальной работы, чем подключённый заголовок. Кроме того **17 из 94 строк —
> это инстанцирование на Haraka, которое FIPS 205 не стандартизовал** (в стандарт вошли SHA2 и SHAKE), то есть
> это допстандартный SPHINCS+, а не SLH-DSA в строгом смысле.
>
> Поэтому `trezor-vendored-crypto` **намеренно не входит** в знаменатель «43 кодовые базы»: это тот же
> репозиторий на том же коммите, и счёт его отдельной базой превратил бы одну миграцию в две.

**Почему эти 94 строки раньше не находились** — детектор искал все способы *вызвать* SLH-DSA и ни одного способа
её *реализовать*: референсная реализация называет себя `SPX_*` и `spx_ctx` и ни разу не пишет имени стандарта.
Разбор — в [[SCOPE-AND-RECALL-2026-10-29]].

**Итоговые суммы по портфелю на 2026-10-29 — нижняя граница, а не измерение:** 51 подписанный комплект,
43 кодовые базы, 2 798 строк инвентаризации, 1 346 ломает Шор, 29 постквантовых. Перепись подмодулей чиста
везде, кроме `nitro`, чьи четырнадцать неподтянутых подмодулей — чужие проекты, отложенные осознанно.

---

# ENGLISH

Measured 2026-10-28 across 33 unique signed audits (the English re-runs are excluded, or seven repositories would
count twice). Every figure reproduces from the relevant bundle's `report.json`; signatures verify and no bundle
disagrees with itself.

**Why this report did not exist until today.** The inventory has always distinguished `pqc` and `hybrid` rows —
cryptography that is already post-quantum — but no summary ever showed them: every summary counted what was
vulnerable. The gap surfaced while building a table view, when the column sums stopped matching the row count.
This is the more saleable half of the product: not "everything is broken" but **who has started, at which file and
line, and who has not**.

**8 of 33 audited codebases contain post-quantum cryptography. 25 contain Shor-breakable cryptography and none at
all.** Across the portfolio: ML-DSA 12 rows, ML-KEM 7, declared PQC libraries 7, X25519MLKEM768 2, SLH-DSA 1.

**Of the three custodian MPC libraries, only one has a post-quantum primitive, and it is not wired in.**
`coinbase-cb-mpc` implements ML-KEM-768 (`mlkem768.h`, `mlkem768.cpp`: `encapsulate`, `decapsulate`) but the only
files including it are its own `.cpp`, its `CMakeLists.txt` and `tests/unit/crypto/test_mlkem768.cpp` — the
publicly verifiable encryption path that wraps key-share backups does not use it. That path is the most urgent
exposure in the whole slice, because the ciphertexts are *stored*: a copy taken today becomes plaintext once a
CRQC exists and no later migration undoes it. So the KEM Coinbase needs for it is already built and not yet
connected — a wiring job, not a research problem. `fireblocks-mpc-lib` (87 of 89 rows Shor-breakable, 98%) and
`bitgo-mpc` (66 of 91) have no post-quantum primitive at all.

**The two leading hardware wallets have diverged.** `trezor-firmware` carries 7 post-quantum rows and they are
working code, not manifest declarations: an ML-DSA-44 module at `core/embed/sec/mldsa44/`, MCU attestation using
ML-DSA, **SLH-DSA in `core/embed/sec/image/boot_header.c:30` — in the root of trust itself** — and a shipped X.509
certificate with an ML-DSA-44 public key. Its boot header carries both schemes at once: Ed25519 at line 81 and
SLH-DSA at line 30, a migration in progress rather than an untouched one. `bitbox02-firmware` has zero.

**Hybrid key exchange has reached TLS and no wallet.** `X25519MLKEM768`, the construction recommended against
harvest-now-decrypt-later, appears in `rustls` and `foundry` and in none of the audited wallets, SDKs or MPC
libraries — even though key exchange is exactly where the retroactive risk is real: a signature can be replaced
later, a session recorded today is decrypted later.

**The largest single gap** is `trustwallet-wallet-core`: 254 Shor-breakable rows of 355, and no post-quantum
cryptography.

**What this report does not claim.** An absent row means absent *in the audited scope at a pinned commit*, not
that a vendor has done nothing — work may sit in another branch, repository or closed source. `signal-desktop`'s
zero Shor rows is almost certainly a scope boundary rather than readiness, since Signal's cryptography lives in
native libraries outside the TypeScript tree. "PQC library" rows are dependency declarations, not evidence of
use — all three of `rage`'s are. And this is not a cryptographic review of any implementation: the inventory says
a primitive is present and where, not that it is used correctly. The six Zcash repositories and `monero` contain
no post-quantum rows, which for Zcash is expected, since that work lives in Epoch and Tachyon rather than in the
audited trees.

---

## Addendum 2026-10-29: corrected denominators, and what Trezor actually pins

The conclusion is unchanged; two of its foundations are not. The figures above are left as they were so that what
moved is visible.

**The denominator was 33 and is now 43.** `bitcoin-core/secp256k1`, SeedSigner, Krux and several other bundles
joined the portfolio. The correct statement is now **8 of 43 audited codebases contain post-quantum
cryptography, 33 contain Shor-breakable cryptography and none at all, and 2 contain neither** (`lottery-demo` and
`zodl-android`, both of whose cryptography sits outside the audited scope). The "already started" share therefore
**falls from 24% to 19%** — not because the industry moved backwards, but because the repositories added are
signing libraries, which contain no post-quantum code at all.

**BitBox02's figures were understated.** The submodule census (see [[SCOPE-AND-RECALL-2026-10-29]]) found that
`bitbox02-firmware` pins `secp256k1-zkp` inside its own Rust crate and that the submodule had never reached the
scanner. Corrected: **136 rows, 90 Shor-breakable**, against 81 and 36 before. Post-quantum rows remain **zero**,
so the second finding above — the Trezor/BitBox02 divergence — not only survives but strengthens: BitBox02 now has
two and a half times the known exposure and exactly as much post-quantum code as before, which is none.

**Trezor pins whole reference implementations, not headers — and until 2026-10-29 the inventory could not see
them.** The main Trezor audit's scope covers the call sites in `core/embed/sec`; the implementations are
submodules under `vendor/`, outside it. A separate `trezor-vendored-crypto` bundle reads them: **142 rows, 38
Shor-breakable, 102 post-quantum — ML-DSA 8 and SLH-DSA 94.**

**94 is the most misquotable number in the portfolio.** It is one row per file of the *complete* upstream SPHINCS+
implementation: four backends (`ref/`, `haraka-aesni/`, `sha2-avx2/`, `shake-a64/`, `shake-avx2/`) and 18
parameter-set headers. A Trezor's microcontroller cannot execute the AVX2 or AArch64 code at all, and the build
compiles exactly one parameter set. The honest claim is **"Trezor pins the whole SPHINCS+ reference
implementation and compiles one configuration from it"** — far stronger evidence of real work than an imported
header. And **17 of the 94 rows are the Haraka instantiation, which FIPS 205 did not standardise** (it covers the
SHA2 and SHAKE instantiations), so those are pre-standard SPHINCS+ rather than SLH-DSA proper. For the same
reason `trezor-vendored-crypto` is **deliberately excluded** from the 43-codebase denominator: it is the same
repository at the same commit, and counting it separately would turn one migration into two.

**Why those 94 rows were invisible before:** the detector covered every way of *calling* SLH-DSA and no way of
*implementing* it, because the reference implementation calls itself `SPX_*` and `spx_ctx` and never writes the
standard's name. Full account in [[SCOPE-AND-RECALL-2026-10-29]].

**Portfolio totals as of 2026-10-29:** 51 signed bundles, 43 codebases, 2,798 inventory rows, 1,346
Shor-breakable, 29 post-quantum. The submodule census is clean except for `nitro`, whose fourteen unmaterialised
submodules are all upstream projects and are deferred deliberately.
