# Триаж биткоин-среза портфеля / Triage of the Bitcoin custody slice — 2026-10-28

Шесть кодовых баз: прошивки Trezor и BitBox02, ядро кошелька Trust Wallet и MPC-библиотеки Coinbase, Fireblocks,
BitGo. **75 находок разобраны, 0 оставлены без решения.** Решения лежат в
`quantumwebhunter/campaigns/triage/<репозиторий>.yml` и попадают в подписанный комплект, поэтому проверить их
может любой, кто откроет отчёт.

## Итог

| | |
|---|---|
| находок разобрано | **75** |
| `confirmed` | **57** |
| `not_applicable` (severity → info) | **18** |
| `false_positive` (снято со счёта) | **0** |
| без решения | **0** |
| подписи комплектов | 42 проверено, 0 сбоев |
| шлюз согласованности | 42 комплекта, 0 расхождений с самими собой |

| комплект | находок | medium после | info после |
|---|---|---|---|
| `trezor-firmware-en` | 11 | 11 | 0 |
| `bitbox02-firmware-en` | 15 | 9 | 6 |
| `trustwallet-wallet-core-en` | 24 | 9 | 15 |
| `coinbase-cb-mpc-en` | 9 | 9 | 0 |
| `fireblocks-mpc-lib-en` | 7 | 7 | 0 |
| `bitgo-mpc-en` | 9 | 8 | 1 |

**Ноль ложных срабатываний — и это не удача, а следствие предмета.** На портфеле ранее было измерено, что 9 из 11
«высоких» оказались ложными (память проекта `qsi-key-detector-false-positives`), но те находки были эвристикой поиска секретов.
Здесь предмет другой: наличие асимметричного алгоритма в коде — проверяемый факт, а не догадка. Поэтому
инвентаризацию можно подавать как есть, а числа находок — только после такого разбора.

## Что дал триаж: три отклонения с проверяемым обоснованием

**`block-buffer` GHSA-qwgh-2vcv-g2f7 → `not_applicable` в обоих репозиториях.** Это та самая уязвимость, которая
повторяется в шести репозиториях Zcash, в Monero, в BitBox и в Trust Wallet, то есть главный пример в пользу
сводной инвентаризации. Условие адвизори: паника должна быть *перехвачена*, а испорченный буфер — использован
снова. В Trust Wallet поиск `catch_unwind` даёт **ноль** вхождений, а через C-FFI паника пробрасывается. В BitBox
из 30 вхождений 26 лежат в `external/vendor/`, а четыре под `src/` — целиком тестовый код
(`#[cfg(test)]` в `bitbox-executor`, тесты с `TestingHal` в `hww.rs` и `async_usb.rs`, интеграционный тест
`bitbox-secp256k1/tests/context.rs`); в `no_std`-сборке на Cortex-M `catch_unwind` недоступен вовсе.

**`anyhow` RUSTSEC-2026-0190 → `not_applicable`.** В BitBox попадает единственным путём
`anyhow ← prost-derive ← prost ← bitbox-proto`, а `prost-derive` — proc-macro, то есть исполняется генератором
кода при сборке и в образ прошивки не линкуется. В Trust Wallet приходит через `move-core-types`, и
`Error::downcast_mut` не вызывается нигде.

**`keccak` GHSA-3288-p39f-rqpv, `time` RUSTSEC-2026-0009, `rand` GHSA-cq8v-f236-94qc → `not_applicable`**, каждое
с конкретной причиной: ARMv8-ассемблерный бэкенд за выключенной фичей `asm`; функции разбора RFC 2822, которые не
вызываются; и необходимость кастомного глобального логгера, которого нет.

## Что дал триаж в обратную сторону: повышение severity

**`crypto-bigint` RUSTSEC-2026-0387 («множественные расхождения по времени в операциях, задуманных как
константные») — `confirmed`, low/без рейтинга → medium, в обоих репозиториях.** Но подтверждения означают разное,
и это главный аргумент за то, что триаж нужен по каждому репозиторию отдельно:

* **Trust Wallet:** `rust/tw_keypair/Cargo.toml` объявляет `k256` и `p256` **жёсткими, не опциональными**
  зависимостями с фичей `ecdsa`; обе тянут `elliptic-curve`, тот — `crypto-bigint 0.5.1`. Достижимо из обоих
  корней workspace, значит из каждого из 43 чейнов, который подписывает. Прятаться за фичей тут не за что.
* **BitBox02:** `src/rust/util/Cargo.toml:17` берёт `p256` как **опциональную** зависимость, а `lib.rs` закрывает
  её `#[cfg(feature = "p256")]`. Фича включается ровно в одном месте — в блоке `app-u2f` в
  `bitbox02-rust-c/Cargo.toml`. Путь реален и секрето-зависим (`util/src/p256.rs` экспортирует `rust_p256_sign`,
  вызывающий `SigningKey::sign_prehash`), но это **подписи U2F/FIDO на P-256, а не биткоиновые ключи** — те идут
  через `bitbox-secp256k1`/libsecp256k1, которого адвизори не касается. В Bitcoin-only прошивке этого кода нет.

То есть одна уязвимость, один диапазон версий, одно решение — **и совершенно разный радиус поражения.** Эксплойт
не демонстрирован ни там, ни там; модель атаки требует локальных измерений времени, что для аппаратного кошелька
ровно та угроза, против которой он и существует. Исправление есть — `crypto-bigint 0.7.6`, но для Trust Wallet это
ломающее обновление через `elliptic-curve`, и сначала должны сдвинуться `k256`/`p256`.

## Главная ценность: раскрытые роли

48 находок `CODE-QV-ASYMMETRIC` — это и есть продукт, но часть приходила с пометкой «роль не определена», а план
миграции упорядочивается именно по тому, что защищает ключ. Раскрыто по исходникам, с указанием функции:

| было | стало |
|---|---|
| Trezor, `crypto/bip32.c:702` | внутри `hdnode_get_shared_key`: ECDH на приватном ключе BIP-32 узла против публичного ключа партнёра; сессионные ключи функций идентичности, не траты |
| Trezor, `crypto/bip32.c:485` | внутри `hdnode_fill_public_key`, диспетчер по вариантам кривых — слой вывода публичных ключей, а не отдельное использование |
| Trezor, `crypto/ecdsa.c` и ещё 7 файлов | реализация ECDSA; **но `crypto/setup.py` и `crypto/tools/bip39bruteforce.c` — сборочный скрипт и демо-утилита, на устройство не попадают** |
| BitBox, `src/pukcc/pukcc.c:181` | `pukcc_ecdsa_verify` — аппаратная проверка подписи на ATSAM; корень доверия загрузчика, проверка публичными ключами |
| BitBox, `bitboxsync.rs:11` | обёртывание ключей при хранении, то есть «собери сейчас, расшифруй потом» |
| BitGo, `opengpgUtils.ts` | не подпись, а **хранение**: OpenPGP шифрует доли ключей TSS и доказательства к ним (`verifyShareProof`, `getBitgoGpgPubKey`) |
| BitGo, `encrypt-rsa-browser.ts` | RSA-OAEP/SHA-256 через WebCrypto на публичный ключ сервера торговой сети |
| Fireblocks, `ed25519_algebra.{h,c}` | слой арифметики под пороговым EdDSA — та же экспозиция, что у пороговых строк, а не дополнительная |
| Coinbase, `base_rsa.cpp:96` | `rsa_pub_key_t` с `encrypt_raw` (RSA_NO_PADDING), `verify_pkcs1`, `EVP_RSA_gen`; подключается `base_pki.h` и `base_paillier.h` — слой PKI под PVE и модульной арифметикой Paillier |

## Две оговорки, записанные в решения намеренно

**Доказательство слабее вывода — у Coinbase.** Строка «Threshold ECDSA» верна по назначению библиотеки, но
**привязана к объявлениям пространств имён и закрывающим скобкам**, а не к криптографическим операциям.
Содержательные доказательства для этого класса лежат в строках Paillier (`base_paillier.h`,
`static constexpr int bit_size = 2048`) и Pedersen (`zk_pedersen.cpp` с реальной генерацией параметров через
`BN_generate_prime_ex`). Это записано в заметке вместе с замечанием, что детектору следовало бы якориться на
функциях протокола.

**Педерсен нельзя описывать как раскрытие сумм.** Взлом дискретного логарифма отнимает у обязательства
**связывание**, а не скрытность: оно совершенно скрывающее, и значения из него не достать даже квантово.
Экспозиция здесь — подделываемость внутри доказательств, то есть будущая стойкость, а не раскрытие прошлого. Та же
ошибка подстерегала в Monero, где раскрытие прошлого идёт не через Педерсена, а через секрет ECDH, которым сумма
шифруется получателю. Формулировка заперта в текстах решений, чтобы не всплыла снова.

**И одна находка, которую нельзя убрать.** SHA-1 у Trust Wallet (`CODE-WEAK-HASH-API`) торчит через публичный
`TWHash`, а `src/Bitcoin/OpCodes.h` ссылается на него потому, что **в Bitcoin Script есть `OP_SHA1`**. Библиотека,
собирающая и исполняющая скрипты, обязана уметь его считать: это требование уровня консенсуса, а не выбор
библиотеки. Решение — `confirmed` с указанием, что правильное действие здесь не удаление, а документирование
назначения и запрет на новые вызовы для целей целостности.

---

# ENGLISH

Six codebases — Trezor and BitBox02 firmware, Trust Wallet's wallet core, and the MPC libraries of Coinbase,
Fireblocks and BitGo. **75 findings triaged, none left undecided**: **57 confirmed, 18 not applicable (severity
dropped to info), 0 false positives.** Decisions live in `campaigns/triage/<repo>.yml` and travel inside the
signed bundle, so anyone opening a report can check them. 42 bundles verify; the consistency gate reports 42
bundles and 0 disagreeing with themselves.

**Zero false positives is a property of the subject, not luck.** The portfolio previously measured 9 of 11 "high"
findings as false, but those were secret-detection heuristics. Here the claim is that an asymmetric algorithm is
present in the code at a named line, which is checkable. So the inventory can be quoted as it stands, and finding
counts only after a review like this one.

**Three dismissals with verifiable reasons.** `block-buffer` GHSA-qwgh-2vcv-g2f7 — the advisory that recurs in six
Zcash repositories, Monero, BitBox and Trust Wallet — is `not_applicable` in both, because it needs a panic to be
*caught* and the corrupted buffer reused: Trust Wallet has zero `catch_unwind` occurrences and propagates across
its C FFI, and in BitBox 26 of 30 occurrences are vendored third-party code while the 4 under `src/` are all
tests, in a `no_std` Cortex-M build where `catch_unwind` does not exist. `anyhow` RUSTSEC-2026-0190 reaches BitBox
only through the proc-macro `prost-derive`, so it runs in the code generator and is never linked into the
firmware. `keccak`, `time` and `rand` each fall to a specific unreached feature or function.

**One raise, which is triage working in the other direction.** `crypto-bigint` RUSTSEC-2026-0387 (timing
variability in operations intended to be constant-time) goes from low/unrated to **medium, confirmed, in both
repositories** — but the two confirmations mean different things, which is the case for per-repository triage. In
Trust Wallet `tw_keypair` declares `k256` and `p256` as hard, non-optional dependencies, so it sits in the signing
path of all 43 chains. In BitBox it reaches the firmware only through `util`'s optional `p256` feature, switched
on by the `app-u2f` build, and `util/src/p256.rs` exports `rust_p256_sign` — so it covers **FIDO credentials, not
bitcoin spending keys** (those go through libsecp256k1, untouched by this advisory) and is absent from a
Bitcoin-only firmware. Same advisory, same version range, same decision, materially different blast radius. No
exploit is demonstrated either way; the fix is crypto-bigint 0.7.6, a breaking upgrade through `elliptic-curve`.

**The main value is resolved roles**, since a migration plan is ordered by what a key protects: Trezor's
`bip32.c:702` is `hdnode_get_shared_key` (ECDH session keys for identity features, not spending); `bip32.c:485` is
`hdnode_fill_public_key`'s per-curve dispatch (a derivation layer, not extra exposure); two of the eight ECDSA
anchors are a build script and a demo tool that never ship; BitBox's `pukcc.c:181` is `pukcc_ecdsa_verify`, the
bootloader's hardware signature check; BitGo's `opengpgUtils.ts` is storage, not signing — OpenPGP wrapping of TSS
key shares, so harvest-now-decrypt-later and fixable today with a hybrid KEM; `encrypt-rsa-browser.ts` is
RSA-OAEP/SHA-256 via WebCrypto; Fireblocks' `ed25519_algebra.{h,c}` is the arithmetic layer under threshold EdDSA;
Coinbase's `base_rsa.cpp` is the PKI layer under publicly verifiable encryption and Paillier's modulus arithmetic.

**Two caveats recorded on purpose.** Coinbase's "Threshold ECDSA" row is right by the library's purpose but
anchored on namespace declarations rather than cryptographic operations — the substantive evidence for that class
is in the Paillier row (`base_paillier.h`, `bit_size = 2048`) and the Pedersen row (`zk_pedersen.cpp`, real
parameter generation). And a Pedersen commitment must never be described as leaking amounts: breaking the discrete
log costs it *binding*, not hiding, since it is perfectly hiding. The retroactive-disclosure path in a private
chain runs through ECDH-derived secrets instead, as in Monero. **And one finding that cannot be removed:** Trust
Wallet's SHA-1 is exposed through the public `TWHash` API and referenced from `src/Bitcoin/OpCodes.h` because
Bitcoin Script defines `OP_SHA1` — a consensus-level requirement, so the right disposition is documentation and a
ban on new integrity callers, not deletion.
