# Отчёт об аудите безопасности и постквантовой готовности

**Проект:** rust-secp256k1 @ fe8b3bec962f · rust-secp256k1 — публичный репозиторий (пассивная проверка)
| | |
|---|---|
| Организация | QSI |
| Дата отчёта | 2026-10-29 19:56 UTC |
| Версия отчёта | 1 |
| Запуск аудита | 9a8057aa-62c4-49fc-8047-f988a32f7a64 (Документальный аудит) |
| Версия анализатора | qsi-engine 1.2.0 |
| Профиль риска | Криптобиржа, кастодиан или кошелёк |
| SHA-256 содержимого | `0383ea7ca33a559a1937e9fb54875aaf90e0e5036351bd80f34861433622d557` |
| Ключ подписи (Ed25519, отпечаток SHA-256; подпись — отдельный файл report.sig.json) | `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e` |
> Отчёт содержит результаты автоматизированного и документального анализа в указанных границах. Он не является юридическим заключением, сертификацией или подтверждением соответствия какому-либо стандарту.

## 1. Резюме для руководства

- Критическая: **0**
- Высокая: **0**
- Средняя: **3**
- Низкая: **0**
- Информационная: **0**

- Подтверждённая техническая уязвимость: 0
- Известная уязвимая версия компонента: 0
- Подтверждённая ошибка конфигурации: 0
- Потенциальный криптографический риск: 0
- Долгосрочный постквантовый риск: 3
- Рекомендация по улучшению: 0
- Недостаточность данных: 0

Неравенство Моски (x + y > z): x = 10, y = 5, z = 8 → при этом сценарии миграция завершится слишком поздно. _z — плановое допущение профиля риска, а не прогноз. Публично известного криптографически значимого квантового компьютера сегодня не существует._

**Постквантовая зрелость: Уровень 0 из 4 — постквантовой криптографии нет.** Следующий шаг: Проведите инвентаризацию: где классическая криптография с открытым ключом защищает долгоживущие данные и ключи, и выберите первую миграцию — обычно гибридный обмен ключами TLS и обёрнутые ключи.

## 2. Область и границы проверки

Режим: Документальный аудит

Репозиторий: <https://github.com/rust-bitcoin/rust-secp256k1> @ `fe8b3bec962fc2c7052501de397fde58ef7142d1` — ссылки в доказательствах открывают строки на этом коммите.

118 файлов, всего 4018256 байт, редактирований: 39; список SHA-256 по файлам — в приложении C.

## 3. Методология

| Область | Статус | Количество | Примеры |
|---|---|---|---|
| dependencies | проверено | 2 | Cargo.toml: 11 dependencies parsed (0 pinned); secp256k1-sys/Cargo.toml: 2 dependencies parsed (0 pinned) |
| source_code | проверено | 116 | secp256k1-sys/build.rs: 68 lines scanned with 16 rule patterns and 123 registry patterns; secp256k1-sys/depend/check_uint128_t.c: 16 lines scanned with 16 rule patterns and 123 registry patterns; secp256k1-sys/depend/secp256k1/contrib/lax_der_parsing.c: 150 lines scanned with 16 rule patterns and 123 registry patterns |
| secrets | проверено | 7 | src/ellswift.rs: 2 redacted value(s) not reported (comments, test modules, fixture declarations, placeholders, values the source annotates as published, or hex values not bound to a secret name); src/key/mod.rs: value(s) at line(s) 2162 (test_keypair_deserialize_serde) are declared inside a fixture and treated as test data, although the file itself is not test code; src/key/mod.rs: 3 redacted value(s) not reported (comments, test modules, fixture declarations, placeholders, values the source annotates as published, or hex values not bound to a secret name) |
| osv_advisories | не проверено | 1 | no exactly pinned versions to query |

_Длинные списки здесь сгруппированы; полный список по файлам — в JSON-версии отчёта, подписанной тем же ключом._

## 4. Проверенные и непроверенные активы

- osv_advisories — не проверено: no exactly pinned versions to query

## 5. Краткое описание архитектуры

Static review of the source tree rust-secp256k1 at fe8b3bec962fc2c7052501de397fde58ef7142d1. 118 files analysed; of 248 files, 46 are test, fuzzing, benchmark or example code and were left out, 84 are not read by any analyzer, 0 exceed the per-file limit and 0 did not fit the total limit. 30 files in build-output or dependency-cache directories (.git, .hg, .venv, __pycache__, build, dist, node_modules, target, vendor, venv) were not read. No requests were sent to the owner's systems.

## 6. Общая оценка состояния безопасности

- Ориентировочный индекс состояния: **100** / 100 — _Рассчитан по находкам в области проверки (подтверждённые и потенциальные проблемы, взвешенные по серьёзности). Ориентировочный; не сравним между аудитами с разной областью._
- Доля квантово-уязвимых элементов инвентаризации: 100.0%

## 7. Подробное описание находок

### QSI-2026-06682 — Квантово-уязвимый ECDSA: подпись транзакций и сообщений (23 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `source-code:ECDSA:transaction_signing`
- Источник данных: secp256k1-sys/build.rs
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-29 19:56 UTC
- Балл приоритета: 35.6 / 100
- CVSS v3.1: неприменимо

51 упоминаний ECDSA в 23 файл(ах), например secp256k1-sys/build.rs:20. Роль по путям, именам функций и соседнему коду: подпись транзакций и сообщений. CRQC восстанавливает закрытый ключ по уже известному открытому (в блокчейне после первой траты, при повторном использовании адреса): средствам и подтверждениям под этими ключами нужен путь миграции.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте secp256k1-sys/build.rs:20 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [secp256k1-sys/build.rs](https://github.com/rust-bitcoin/rust-secp256k1/blob/fe8b3bec962fc2c7052501de397fde58ef7142d1/secp256k1-sys/build.rs#L20) · line 20 · SHA-256 a5f2d41826e68b84e6cc0e9f6c66bb2d8df138b21870fab304ea5baa3f0cf9c8_

```
   19 |     base_config
   20 |         .include("depend/secp256k1/")
   21 |         .include("depend/secp256k1/include")
```

_file_excerpt · [secp256k1-sys/build.rs](https://github.com/rust-bitcoin/rust-secp256k1/blob/fe8b3bec962fc2c7052501de397fde58ef7142d1/secp256k1-sys/build.rs#L21) · line 21 · SHA-256 4199c21bcb627930afb8759ea12971929ddaeea49d540dec5f3120dd9275a26f_

```
   20 |         .include("depend/secp256k1/")
   21 |         .include("depend/secp256k1/include")
   22 |         .include("depend/secp256k1/src")
```

_file_excerpt · [secp256k1-sys/build.rs](https://github.com/rust-bitcoin/rust-secp256k1/blob/fe8b3bec962fc2c7052501de397fde58ef7142d1/secp256k1-sys/build.rs#L22) · line 22 · SHA-256 92465db9e22b0cd0df7d8585a8505b1318dcb874a3c6015e59d2af2c13a254f7_

```
   21 |         .include("depend/secp256k1/include")
   22 |         .include("depend/secp256k1/src")
   23 |         .flag_if_supported("-Wno-unused-function") // some ecmult stuff is defined but not used upstream
```

_file_excerpt · [secp256k1-sys/depend/secp256k1/contrib/lax_der_parsing.h](https://github.com/rust-bitcoin/rust-secp256k1/blob/fe8b3bec962fc2c7052501de397fde58ef7142d1/secp256k1-sys/depend/secp256k1/contrib/lax_der_parsing.h#L57) · line 57 · SHA-256 25af7e242d92af0d3c46ae8d8a48030e247c4bfdeba65068030e64eb4c88c912_

```
   56 |    files (such as tests.c) without the need to set an explicit -I flag,
   57 |    which would be necessary to locate secp256k1.h. */
   58 | #ifndef SECP256K1_H
```

_file_excerpt · [secp256k1-sys/depend/secp256k1/contrib/lax_der_parsing.h](https://github.com/rust-bitcoin/rust-secp256k1/blob/fe8b3bec962fc2c7052501de397fde58ef7142d1/secp256k1-sys/depend/secp256k1/contrib/lax_der_parsing.h#L59) · line 59 · SHA-256 4c35a81e99a7eaf5ea7315346f3b8cacb0832f7c4a3b1a3d003ff0bd3b6a82c1_

```
   58 | #ifndef SECP256K1_H
   59 | #include <secp256k1.h>
   60 | #endif
```

_file_excerpt · [secp256k1-sys/depend/secp256k1/contrib/lax_der_privatekey_parsing.h](https://github.com/rust-bitcoin/rust-secp256k1/blob/fe8b3bec962fc2c7052501de397fde58ef7142d1/secp256k1-sys/depend/secp256k1/contrib/lax_der_privatekey_parsing.h#L34) · line 34 · SHA-256 163cac24f6b60e798317e2383fb603da718e728035262dc9759d7cf3fbd47b4f_

```
   33 |    files (such as tests.c) without the need to set an explicit -I flag,
   34 |    which would be necessary to locate secp256k1.h. */
   35 | #ifndef SECP256K1_H
```

_file_excerpt · [secp256k1-sys/depend/secp256k1/contrib/lax_der_privatekey_parsing.h](https://github.com/rust-bitcoin/rust-secp256k1/blob/fe8b3bec962fc2c7052501de397fde58ef7142d1/secp256k1-sys/depend/secp256k1/contrib/lax_der_privatekey_parsing.h#L36) · line 36 · SHA-256 2741d1869779ddac4f151ac1740c338ba299b2bed7b98a38e6042acb62fca350_

```
   35 | #ifndef SECP256K1_H
   36 | #include <secp256k1.h>
   37 | #endif
```

_file_excerpt · [secp256k1-sys/depend/secp256k1/include/secp256k1_ecdh.h](https://github.com/rust-bitcoin/rust-secp256k1/blob/fe8b3bec962fc2c7052501de397fde58ef7142d1/secp256k1-sys/depend/secp256k1/include/secp256k1_ecdh.h#L4) · line 4 · SHA-256 1b629d577e7d70d59383b1579315be3bf12eeca54bf16ca67903eecec13b55a4_

```
    3 | 
    4 | #include "secp256k1.h"
    5 | 
```

_file_excerpt · [secp256k1-sys/depend/secp256k1/include/secp256k1_ellswift.h](https://github.com/rust-bitcoin/rust-secp256k1/blob/fe8b3bec962fc2c7052501de397fde58ef7142d1/secp256k1-sys/depend/secp256k1/include/secp256k1_ellswift.h#L4) · line 4 · SHA-256 1b629d577e7d70d59383b1579315be3bf12eeca54bf16ca67903eecec13b55a4_

```
    3 | 
    4 | #include "secp256k1.h"
    5 | 
```

_file_excerpt · [secp256k1-sys/depend/secp256k1/include/secp256k1_extrakeys.h](https://github.com/rust-bitcoin/rust-secp256k1/blob/fe8b3bec962fc2c7052501de397fde58ef7142d1/secp256k1-sys/depend/secp256k1/include/secp256k1_extrakeys.h#L4) · line 4 · SHA-256 1b629d577e7d70d59383b1579315be3bf12eeca54bf16ca67903eecec13b55a4_

```
    3 | 
    4 | #include "secp256k1.h"
    5 | 
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Следите за постквантовыми планами каждой сети, не используйте открытые ключи повторно и держите подписание готовым к постквантовым схемам по мере их принятия сетями.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-06683 — Квантово-уязвимый Schnorr (BIP-340): подпись транзакций и сообщений (2 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `source-code:Schnorr (BIP-340):transaction_signing`
- Источник данных: secp256k1-sys/src/lib.rs
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-29 19:56 UTC
- Балл приоритета: 35.6 / 100
- CVSS v3.1: неприменимо

9 упоминаний Schnorr (BIP-340) в 2 файл(ах), например secp256k1-sys/src/lib.rs:1073. Роль по путям, именам функций и соседнему коду: подпись транзакций и сообщений. CRQC восстанавливает закрытый ключ по уже известному открытому (в блокчейне после первой траты, при повторном использовании адреса): средствам и подтверждениям под этими ключами нужен путь миграции.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте secp256k1-sys/src/lib.rs:1073 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [secp256k1-sys/src/lib.rs](https://github.com/rust-bitcoin/rust-secp256k1/blob/fe8b3bec962fc2c7052501de397fde58ef7142d1/secp256k1-sys/src/lib.rs#L1073) · line 1073 · SHA-256 efacee2282622bd9afdbd4d21fba13b4ae52c3b7950fd46c6eaad7f2833d7b66_

```
 1072 |     )]
 1073 |     pub fn secp256k1_schnorrsig_sign(
 1074 |         cx: *const Context,
```

_file_excerpt · [secp256k1-sys/src/lib.rs](https://github.com/rust-bitcoin/rust-secp256k1/blob/fe8b3bec962fc2c7052501de397fde58ef7142d1/secp256k1-sys/src/lib.rs#L1086) · line 1086 · SHA-256 7155b9ee61a6b3b7a19c9ac3b631ad3edddee83c1b261e3bb09f225c048c9e9d_

```
 1085 |     )]
 1086 |     pub fn secp256k1_schnorrsig_sign_custom(
 1087 |         cx: *const Context,
```

_file_excerpt · [secp256k1-sys/src/lib.rs](https://github.com/rust-bitcoin/rust-secp256k1/blob/fe8b3bec962fc2c7052501de397fde58ef7142d1/secp256k1-sys/src/lib.rs#L1099) · line 1099 · SHA-256 c0c60e7da096f64bf928a080f61201ddc6e99b91eb09cbad8df405a0f2587182_

```
 1098 |     )]
 1099 |     pub fn secp256k1_schnorrsig_verify(
 1100 |         cx: *const Context,
```

_file_excerpt · [src/schnorr.rs](https://github.com/rust-bitcoin/rust-secp256k1/blob/fe8b3bec962fc2c7052501de397fde58ef7142d1/src/schnorr.rs#L119) · line 119 · SHA-256 b0ac4aa5cec5e41d8282163f25ae8852222c94224505fe06a05e79b8e0e43c6f_

```
  118 |             |secp: &Secp256k1<crate::AllPreallocated>| {
  119 |                 ffi::secp256k1_schnorrsig_sign_custom(
  120 |                     secp.ctx.as_ptr(),
```

_file_excerpt · [src/schnorr.rs](https://github.com/rust-bitcoin/rust-secp256k1/blob/fe8b3bec962fc2c7052501de397fde58ef7142d1/src/schnorr.rs#L167) · line 167 · SHA-256 3c8d77857e39e275e2dbfcd82048329024ab19596a4d5f0aeac8ee8c576d00d8_

```
  166 |             |secp: &Secp256k1<crate::AllPreallocated>| {
  167 |                 ffi::secp256k1_schnorrsig_verify(
  168 |                     secp.ctx.as_ptr(),
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Следите за постквантовыми планами каждой сети, не используйте открытые ключи повторно и держите подписание готовым к постквантовым схемам по мере их принятия сетями.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-06684 — Квантово-уязвимый ECDSA: роль не определена (2 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `source-code:ECDSA:general`
- Источник данных: src/lib.rs
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-29 19:56 UTC
- Балл приоритета: 34.2 / 100
- CVSS v3.1: неприменимо

3 упоминаний ECDSA в 2 файл(ах), например src/lib.rs:362. Роль по путям, именам функций и соседнему коду: роль не определена. По коду не видно, что защищают ключи; приоритет определит проверка.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте src/lib.rs:362 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [src/lib.rs](https://github.com/rust-bitcoin/rust-secp256k1/blob/fe8b3bec962fc2c7052501de397fde58ef7142d1/src/lib.rs#L362) · line 362 · SHA-256 ffad46a775c24c96bcfcbea7698aa07d993b31975376d7e818d1f3c45d00c042_

```
  361 |     fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
  362 |         write!(f, "<secp256k1 context {:?}, {}>", self.ctx, C::DESCRIPTION)
  363 |     }
```

_file_excerpt · [src/lib.rs](https://github.com/rust-bitcoin/rust-secp256k1/blob/fe8b3bec962fc2c7052501de397fde58ef7142d1/src/lib.rs#L416) · line 416 · SHA-256 f7ed24bd3aef909915629692e58bc72335aab84d369d315f1446ff5438803c34_

```
  415 |     #[cfg(feature = "rand")]
  416 |     #[deprecated(since = "0.32.0", note = "use secp256k1::generate_keypair instead")]
  417 |     pub fn generate_keypair<R: rand::Rng + ?Sized>(
```

_file_excerpt · [src/scalar.rs](https://github.com/rust-bitcoin/rust-secp256k1/blob/fe8b3bec962fc2c7052501de397fde58ef7142d1/src/scalar.rs#L151) · line 151 · SHA-256 d1c2f06aed006e6ebf628ab453e342b3fd91780c66badcc37598269148d8a562_

```
  150 |     fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
  151 |         fmt::Display::fmt("the value is not a member of secp256k1 field", f)
  152 |     }
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Классифицируйте каждое использование, зафиксируйте сроки жизни данных и запланируйте миграцию на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема; введите уровень абстракции для криптогибкости.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.


## 8. Постквантовая оценка

| | Обмен ключами (x — сколько данные должны оставаться конфиденциальными; «собери сейчас, расшифруй потом») | Подписи (x — сколько подписи и ключи должны оставаться доверенными) |
|---|---|---|
| Срок жизни данных/ключей x | 10 | 10 |
| Время миграции y | 5 | 5 |
| Принятое число лет до CRQC z | 8 (early) | 8 |
| x + y − z | 7 → при этом сценарии миграция завершится слишком поздно | 7 → при этом сценарии миграция завершится слишком поздно |
#### Откуда взято z

Усреднённая оценка экспертов, что CRQC появится в пределах горизонта, из ежегодного опроса, который публикует автор этого неравенства. Это оценки вероятности, а не предсказание даты.

| В пределах | Вероятность | Формулировка отчёта |
|---|---|---|
| 5 лет | ~15% | усреднённая оценка |
| 10 лет | 28-49% | вполне возможно |
| 15 лет | 51-70% | вероятно |

**Почему выбран этот сценарий (early, z = 8):** Внутри 10-летнего горизонта, которому опрос даёт 28-49% («вполне возможно»), и согласуется с оценкой BSI в 15 лет, которая «может сократиться до 10 или меньше». Для данных с десятилетиями конфиденциальности, где ошибка дорога.
_Допущения планирования: x для обмена ключами, x для подписей, y — значения по умолчанию профиля риска «Криптобиржа, кастодиан или кошелёк», а не данные клиента; с фактическими сроками клиента вывод может измениться._

### Постквантовая зрелость: Уровень 0 из 4 — постквантовой криптографии нет


**Следующий шаг:** Проведите инвентаризацию: где классическая криптография с открытым ключом защищает долгоживущие данные и ключи, и выберите первую миграцию — обычно гибридный обмен ключами TLS и обёрнутые ключи.

_Уровни: 0 — нет; 1 — есть, но не подключено; 2 — используется вне критичных путей; 3 — гибрид в критичном пути; 4 — постквантовое по умолчанию в критичных путях (корень доверия, обёртка ключей, обмен ключами в канале). Оценка по коду и манифестам._

### Что делают квантово-уязвимые алгоритмы

| Роль | Алгоритмы (файлы) | ID | Первый шаг |
|---|---|---|---|
| **подпись транзакций и сообщений** | ECDSA (23), Schnorr (BIP-340) (2) | QSI-2026-06682, QSI-2026-06683 | Следите за постквантовыми планами каждой сети, не используйте открытые ключи повторно и держите подписание готовым к постквантовым схемам по мере их принятия сетями |
| **роль не определена** | ECDSA (2) | QSI-2026-06684 | Классифицируйте каждое использование, зафиксируйте сроки жизни данных и запланируйте миграцию на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема; введите уровень абстракции для криптогибкости |

_Роль определяется по путям файлов, именам функций и коду вокруг совпадений; проверка её подтверждает. Сначала — ключи корня доверия и обёрнутые ключи: их трудно заменить или можно записать уже сегодня._
Анкета готовности для проекта не заполнялась.

### Квантовые алгоритмы, значимые для этой инвентаризации

| Квантовый алгоритм | Действие | Модель атаки | Алгоритмы из инвентаризации (строк) | Что это значит для аудита |
|---|---|---|---|---|
| Алгоритм Шора — дискретный логарифм на эллиптических кривых | взламывает | Q1 | ECDH (2), ECDSA (27), Schnorr (BIP-340) (3) | Ключи на эллиптических кривых, по оценкам, падут раньше ключей RSA сопоставимой классической стойкости. В блокчейнах первыми под угрозой монеты, чей открытый ключ уже опубликован (повторно используемые адреса, выходы pay-to-public-key и Taproot); планируйте переход на постквантовые подписи и до этого избегайте повторного использования ключей. |

_Действие: взламывает — алгоритм нужно заменить; ослабляет — более длинные ключи или выходы восстанавливают запас; учтено в стандартных параметрах — при стандартных наборах действий не требуется; только при суперпозиционных запросах — к обычному применению неприменимо._


## 9. Ограничения и допущения

- Отчёт содержит результаты автоматизированного и документального анализа в указанных границах. Он не является юридическим заключением, сертификацией или подтверждением соответствия какому-либо стандарту.
- z — плановое допущение профиля риска, а не прогноз. Публично известного криптографически значимого квантового компьютера сегодня не существует.
- osv_advisories: no exactly pinned versions to query

## 10. План устранения проблем / Приоритеты на 30, 60 и 90 дней

### 30 дн.

| Приоритет | ID | Действие | Тип | Условие закрытия |
|---|---|---|---|---|
### 60 дн.

| Приоритет | ID | Действие | Тип | Условие закрытия |
|---|---|---|---|---|
### 90 дн.

| Приоритет | ID | Действие | Тип | Условие закрытия |
|---|---|---|---|---|
| P3 | QSI-2026-06682 | Внесите использования ECDSA в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-06683 | Внесите использования Schnorr (BIP-340) в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-06684 | Внесите использования ECDSA в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P4 | QSI-2026-06682 | Запланируйте миграцию ECDSA на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема или гибридной схемы. |
| P4 | QSI-2026-06683 | Запланируйте миграцию Schnorr (BIP-340) на  (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование  или гибридной схемы. |
| P4 | QSI-2026-06684 | Запланируйте миграцию ECDSA на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема или гибридной схемы. |

## 11. Использованные инструменты

- blockchain 1.0.0
- certificates 1.1.0
- chain_map 1.0.0
- configs 1.1.0
- dependencies 1.2.0
- inventory_document 1.1.0
- solidity 1.2.0
- source_code 1.3.0
- tls_code 1.1.0
- tls_live 1.0.0
- qsi-engine 1.2.0
- OSV.dev API v1

## 12. Источники и нормативные документы

1. C. Chevignard, P.-A. Fouque, A. Schrottenloher — Reducing the Number of Qubits in Quantum Discrete Logarithms on Elliptic Curves (IACR ePrint 2026/280) — IACR ePrint. <https://eprint.iacr.org/2026/280> (revision of a EUROCRYPT 2026 paper: 3.12n + o(n) qubits; for n = 256, 1193 qubits and 22 runs of 2^38.98 Toffoli gates)
2. Common Vulnerability Scoring System v3.1: Specification Document — FIRST. <https://www.first.org/cvss/v3.1/specification-document> (final)
3. D. Litinski — How to compute a 256-bit elliptic curve private key with only 50 million Toffoli gates (arXiv:2306.08585) — arXiv. <https://arxiv.org/abs/2306.08585> (preprint (2023-06-14): 6000 modules × 1152 physical qubits, one key per 10 minutes under its architecture assumptions)
4. FIPS 203 — Module-Lattice-Based Key-Encapsulation Mechanism Standard (ML-KEM) — NIST. <https://csrc.nist.gov/pubs/fips/203/final> (final (August 2024))
5. FIPS 204 — Module-Lattice-Based Digital Signature Standard (ML-DSA) — NIST. <https://csrc.nist.gov/pubs/fips/204/final> (final (August 2024))
6. FIPS 205 — Stateless Hash-Based Digital Signature Standard (SLH-DSA) — NIST. <https://csrc.nist.gov/pubs/fips/205/final> (final (August 2024))
7. J. Proos, C. Zalka — Shor's discrete logarithm quantum algorithm for elliptic curves (Quantum Inf. Comput. 3(4), 2003; arXiv:quant-ph/0301141) — Quantum Information & Computation. <https://doi.org/10.26421/QIC3.4-3> (peer-reviewed article)
8. M. Cain et al. — Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits (arXiv:2603.28627) — arXiv. <https://arxiv.org/abs/2603.28627> (preprint (2026-03-30): P-256 in a few days with 26,000 physical neutral-atom qubits; RSA-2048 one to two orders of magnitude longer)
9. M. Mosca — Cybersecurity in an Era with Quantum Computers: Will We Be Ready? (IEEE Security & Privacy, 2018) — IEEE. <https://doi.org/10.1109/MSP.2018.3761723> (peer-reviewed article; source of the x + y > z migration inequality)
10. M. Roetteler, M. Naehrig, K. Svore, K. Lauter — Quantum resource estimates for computing elliptic curve discrete logarithms (ASIACRYPT 2017) — IACR / arXiv. <https://arxiv.org/abs/1706.06752> (peer-reviewed article: at most 9n + 2⌈log2 n⌉ + 10 qubits and 448 n^3 log2 n + 4090 n^3 Toffoli gates)
11. NIST IR 8547 — Transition to Post-Quantum Cryptography Standards — NIST. <https://csrc.nist.gov/pubs/ir/8547/ipd> (initial public draft (November 2024); proposes deprecating quantum-vulnerable public-key algorithms after 2030 and disallowing them after 2035 — dates may change in the final version)
12. P. W. Shor — Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms on a Quantum Computer (SIAM J. Comput., 1997) — SIAM. <https://doi.org/10.1137/S0097539795293172> (peer-reviewed article)
13. R. Babbush et al. — Securing Elliptic Curve Cryptocurrencies against Quantum Vulnerabilities: Resource Estimates and Mitigations (arXiv:2603.28846) — arXiv. <https://arxiv.org/abs/2603.28846> (preprint (2026-03-30, v2 2026-04-15): 256-bit ECDLP with < 1200 logical qubits and < 90 M Toffoli gates (or < 1450 and < 70 M); < 500,000 physical qubits at 10^-3 error, minutes)

## Приложения: Криптографическая инвентаризация

| Алгоритм | Параметр | Библиотека | Квантовый статус | Классический статус | Количество | Мест | Примеры |
|---|---|---|---|---|---|---|---|
| ECDH |  |  | уязвим (Шор) | допустимо | 2 | 2 | secp256k1-sys/depend/secp256k1/include/secp256k1_ecdh.h; src/ecdh.rs |
| ECDSA | secp256k1 |  | уязвим (Шор) | допустимо | 21 | 21 | secp256k1-sys/build.rs:20; secp256k1-sys/depend/secp256k1/contrib/lax_der_parsing.h:57; secp256k1-sys/depend/secp256k1/contrib/lax_der_privatekey_parsing.h:34 |
| ECDSA |  |  | уязвим (Шор) | допустимо | 6 | 6 | secp256k1-sys/depend/secp256k1/src/ecdsa.h; secp256k1-sys/depend/secp256k1/src/ecdsa_impl.h; secp256k1-sys/src/lib.rs:271 |
| Schnorr (BIP-340) |  |  | уязвим (Шор) | допустимо | 3 | 3 | secp256k1-sys/depend/secp256k1/include/secp256k1_schnorrsig.h; secp256k1-sys/src/lib.rs:1073; src/schnorr.rs:119 |

_Длинные списки здесь сгруппированы; полный список по файлам — в JSON-версии отчёта, подписанной тем же ключом._

## Приложения: Входные файлы

| Файл | Размер | SHA-256 | Маскирования |
|---|---|---|---|
| Cargo.toml | 3184 | `f1840f6dfb58f6ca1bc442f730c97893c96648fbc84ca860cf4d31fb0c8e386e` | 0 |
| secp256k1-sys/Cargo.toml | 1619 | `ff4c6efd6aeaf4f76348f7b2f3ad7477f62657998825eb07dc13745e6c4348ee` | 0 |
| secp256k1-sys/build.rs | 2705 | `f28218d715a210ccf4a02a72a8b10ba1bc32e55aab62de87c620c071616e15c4` | 0 |
| secp256k1-sys/depend/check_uint128_t.c | 248 | `c20d2a8c6f6991595840a78f0e72eb0b32cce41209e62d30599c238fd21d5f47` | 0 |
| secp256k1-sys/depend/secp256k1/contrib/lax_der_parsing.c | 3855 | `d59c736417fbed06df5db4f476caf5643b55ecc5c950596ee3b80462dfb52859` | 0 |
| secp256k1-sys/depend/secp256k1/contrib/lax_der_parsing.h | 4290 | `9e3f5c6282938e3e141e911381ec6aebb321ad5a6d03b1e9e7a921548b6b51cc` | 0 |
| secp256k1-sys/depend/secp256k1/contrib/lax_der_privatekey_parsing.c | 5182 | `c729549dd004b2631c72ddd9083b370886de6bfde0f06fad01eddafdc8da27bb` | 0 |
| secp256k1-sys/depend/secp256k1/contrib/lax_der_privatekey_parsing.h | 4056 | `270578950fc61f0875a252f809a718a9a414754e17fc070846d577113e11e3e6` | 0 |
| secp256k1-sys/depend/secp256k1/include/secp256k1.h | 43026 | `d39c553b7903dfaec2c0947e33ed33eafbdfa09b3ef4a59fd4eb32ac959f370f` | 0 |
| secp256k1-sys/depend/secp256k1/include/secp256k1_ecdh.h | 2710 | `24a629250a48ff976ddff7c56f0b4e3ce47ea49b97105accc2e41a4b5eaa017a` | 0 |
| secp256k1-sys/depend/secp256k1/include/secp256k1_ellswift.h | 9397 | `05e4a55ae2d4610f8f832472824bc7c6dd9a96e347e9f956a5320b39b6f7a24a` | 0 |
| secp256k1-sys/depend/secp256k1/include/secp256k1_extrakeys.h | 11490 | `6d168046d730b7a69f50e7793bf4254f6cb56c22002a3249836b41c6ea907a30` | 0 |
| secp256k1-sys/depend/secp256k1/include/secp256k1_musig.h | 29265 | `4fc94ae766ba1edb13003431948183fece6328ba682a3bea9496998184b219c6` | 0 |
| secp256k1-sys/depend/secp256k1/include/secp256k1_preallocated.h | 6306 | `6ca991814860e7448cc67d8501a39b9327fba65a5501bf79951d3ac861e79a4a` | 0 |
| secp256k1-sys/depend/secp256k1/include/secp256k1_recovery.h | 4922 | `f87789710c856ee08d6f04fa0809343cbdb508a9045580cf91ffe4aaf717be82` | 0 |
| secp256k1-sys/depend/secp256k1/include/secp256k1_schnorrsig.h | 8487 | `d76fff4bac7c0214df645179031dfe75d56df83c17bcdf646d0aa189251f20d7` | 0 |
| secp256k1-sys/depend/secp256k1/src/assumptions.h | 4677 | `cbad7817c315f29783e2fa21f6477888b20a262672f674bc94c5858d3309806e` | 0 |
| secp256k1-sys/depend/secp256k1/src/checkmem.h | 4640 | `338d267031b23e83133614ed1ad23e68480ba9f837c497155c326d08322d3c16` | 0 |
| secp256k1-sys/depend/secp256k1/src/ecdsa.h | 1344 | `011f5744a12548a5c333e6ea3a3d0e43b7f90a698955f7452e948b552abb19c1` | 0 |
| secp256k1-sys/depend/secp256k1/src/ecdsa_impl.h | 11302 | `c6f44808c93278a1bd42aea9c6cc66bafc2df90ad4b09bf25ace1efa0965b112` | 0 |
| secp256k1-sys/depend/secp256k1/src/eckey.h | 1323 | `b1f23329bb6abe30e52f335975ba7617564ad10dccd580a894ffd0bef965e461` | 0 |
| secp256k1-sys/depend/secp256k1/src/eckey_impl.h | 3843 | `5f73e180882c209f28352612dd996136abdb102e93d9e3f8e2478888db20e46e` | 0 |
| secp256k1-sys/depend/secp256k1/src/ecmult.h | 2819 | `1aedbc9abb1bce054768b366f886c40e0ac0cf535b4deb0859cf858c692419bf` | 0 |
| secp256k1-sys/depend/secp256k1/src/ecmult_compute_table.h | 1153 | `7f8b7cb544b64c46f2d9744c5fdecf5115a0ee898f3be86c1ab666567e6661a9` | 0 |
| secp256k1-sys/depend/secp256k1/src/ecmult_compute_table_impl.h | 2143 | `a3427b408943cfc6c1a4edefb9e9ee565f8cffe3728fe9e2396e7ff4163b2eca` | 0 |
| secp256k1-sys/depend/secp256k1/src/ecmult_const.h | 1454 | `6b4c471e779bc5c6eeb6014250bfb582e4713437208c1d8d8024cef6dce148e0` | 0 |
| secp256k1-sys/depend/secp256k1/src/ecmult_const_impl.h | 20379 | `8838775cdd25cf65e253dc226e9ef0573a8c8cf58efb0c1e8a8fda4fbb9f9434` | 0 |
| secp256k1-sys/depend/secp256k1/src/ecmult_gen.h | 5528 | `02b5f57bbcd49da5dd3cb385e326ceef3eebdca190dfe6ec5d439417691501dc` | 0 |
| secp256k1-sys/depend/secp256k1/src/ecmult_gen_compute_table.h | 702 | `7dbc14514dbc0228998a73078865ce5bb1913c56f9ae1ec28be25511d41f018d` | 0 |
| secp256k1-sys/depend/secp256k1/src/ecmult_gen_compute_table_impl.h | 5015 | `08fe63e5adbb6e67a55fb66fc2d14554c8643db49c60e9d279eea57708551c90` | 0 |
| secp256k1-sys/depend/secp256k1/src/ecmult_gen_impl.h | 17227 | `77fc665701acc1aaae6b61a73c4a05431be6a673f93c31d77bd77e9c9bcb8918` | 0 |
| secp256k1-sys/depend/secp256k1/src/ecmult_impl.h | 36899 | `aabc88f8acaaf07b5e931e58535a5e15af86f30cc128c18b6c49714f548010f8` | 0 |
| secp256k1-sys/depend/secp256k1/src/field.h | 16635 | `1a4ad5e0a6047cea3d54d573093756e4484d24e5d62e70a6a4bf941c529125ac` | 0 |
| secp256k1-sys/depend/secp256k1/src/field_10x26.h | 2358 | `47f9d068809137d2ffb9119bf1cfea3280e0aeb11978feea0ac7802be37a0107` | 0 |
| secp256k1-sys/depend/secp256k1/src/field_10x26_impl.h | 53112 | `02550b9ca48ded198f3aa8db9d8c6eee0bb6be585d82caa93f1413e382582c21` | 0 |
| secp256k1-sys/depend/secp256k1/src/field_5x52.h | 2400 | `9b6ab1a6c79b776d4b082ee127ce471f355e255bf5108effb599a96b9029ff70` | 0 |
| secp256k1-sys/depend/secp256k1/src/field_5x52_impl.h | 20326 | `2e3d35fcffced09bb6ac898760af75fcf26c6cb4260e1a89c2340fc516788fc5` | 0 |
| secp256k1-sys/depend/secp256k1/src/field_5x52_int128_impl.h | 12391 | `59ed9576d6deb63c100b26019a33d24c230a7d136b956f67133e6877208530eb` | 0 |
| secp256k1-sys/depend/secp256k1/src/field_impl.h | 16223 | `0afd349a2cbe8f9846c4c9651f09c982fb16334eea6ff8cca1971a87cf810ae1` | 0 |
| secp256k1-sys/depend/secp256k1/src/group.h | 13118 | `ba3b2da5ab27366dd92b636e7d8dca9249c2db923c4239d7189dd958c6734761` | 0 |
| secp256k1-sys/depend/secp256k1/src/group_impl.h | 38781 | `8aefc6d6eeab3d16aa83ab3355596b2dcf04c921ede1f4e2b09f825dd2cb6d32` | 0 |
| secp256k1-sys/depend/secp256k1/src/hash.h | 2196 | `2a78cc73f4ecf25179f859c7778e0c9eb2d7a4ac03e2c13d8fd3480fa0bebd00` | 0 |
| secp256k1-sys/depend/secp256k1/src/hash_impl.h | 14582 | `d152eb1b1578edab2ecf3ada77aa185ea52020c1bdcbc9eb4c393fdd8295a77e` | 0 |
| secp256k1-sys/depend/secp256k1/src/hsort.h | 1705 | `bd108b51741b926781cb0a3ff2a054b61db2296f09857dfb2150fd661ace6cf1` | 0 |
| secp256k1-sys/depend/secp256k1/src/hsort_impl.h | 5038 | `6a794299c0fa53600b8bce5c4c463586cdbd204fe2eaad469e3eb9c12a9c4d67` | 0 |
| secp256k1-sys/depend/secp256k1/src/int128.h | 4012 | `8435767d08876d419b3b743dd5ae31b07e0b74218df1be45462ea487015d84d2` | 0 |
| secp256k1-sys/depend/secp256k1/src/int128_impl.h | 376 | `5683c02dfc495639da259d80624711c1c449bbaee6186729e399e713a28b4719` | 0 |
| secp256k1-sys/depend/secp256k1/src/int128_native.h | 601 | `c28a470a02e1fd799f2cf8228ffe1731b3e0d2be191978355697a235e26a6805` | 0 |
| secp256k1-sys/depend/secp256k1/src/int128_native_impl.h | 3271 | `3c1cbd5272d9b62783acd262d5807aee79d6d386f4aba888eaf906512c82d4e4` | 0 |
| secp256k1-sys/depend/secp256k1/src/int128_struct.h | 259 | `b8eed83cae0de920af460eefdb26d796862a8dd36759869db76a72db262c2984` | 0 |
| secp256k1-sys/depend/secp256k1/src/int128_struct_impl.h | 8434 | `1c09fafe1861c7ce5e524a92e561afd6f1525dec86b154d7abb39d09d033431c` | 0 |
| secp256k1-sys/depend/secp256k1/src/modinv32.h | 1995 | `cc7da45d20d976a9753a7926a04fb694a151b35329d8d1ebbd008febddf9ad8c` | 0 |
| secp256k1-sys/depend/secp256k1/src/modinv32_impl.h | 34692 | `248a5c185fdd1b34c22e8d0f12d1c3d80211aa37bb83178fde22abef062c988d` | 0 |
| secp256k1-sys/depend/secp256k1/src/modinv64.h | 2099 | `db15aae18793d2bd401f9e9de5d8b22c513787f85aec694e8b367b9e0cb69efc` | 0 |
| secp256k1-sys/depend/secp256k1/src/modinv64_impl.h | 40233 | `8cbe489cf14cbbd8fe916ad91d02ac99d37bb442f9f29b9efeff737821909707` | 0 |
| secp256k1-sys/depend/secp256k1/src/modules/ecdh/main_impl.h | 2822 | `53241d7caec889c4f41c4ee71cda197214ff31caf20459425a6af86d48c07b40` | 0 |
| secp256k1-sys/depend/secp256k1/src/modules/ellswift/main_impl.h | 28694 | `bed144aea3f7559f294e57d9e3062386d1c12de7ebf48a5d0ccebde9aece2736` | 0 |
| secp256k1-sys/depend/secp256k1/src/modules/extrakeys/main_impl.h | 11241 | `27b18e35f1200c70329123c9dc6bc2ae54de2ea15f7f7671a80fb1cdb2a02b30` | 0 |
| secp256k1-sys/depend/secp256k1/src/modules/musig/keyagg.h | 1408 | `079c5b03c77422b29a33294aea99b9c26c22fb53e89a1d7152afe0d05a68eed3` | 0 |
| secp256k1-sys/depend/secp256k1/src/modules/musig/keyagg_impl.h | 12327 | `05b8ee77127f75455ab1e169579a9e86f43fcaafc0cb7182b60b44449695be5e` | 0 |
| secp256k1-sys/depend/secp256k1/src/modules/musig/main_impl.h | 426 | `9ec7e6082aa496353466769bb9f7705c32caf8d060b0c92815cb37f6c4265654` | 0 |
| secp256k1-sys/depend/secp256k1/src/modules/musig/session.h | 941 | `c12f5ec3df77df5ad3f4fcdfe99c8545c574825680c333c12e086238696ce0e2` | 0 |
| secp256k1-sys/depend/secp256k1/src/modules/musig/session_impl.h | 34842 | `168e7cc3ac954ef9927711879f1cc44c788521057402695c723c14509047bb46` | 0 |
| secp256k1-sys/depend/secp256k1/src/modules/musig/vectors.h | 37797 | `c7cd9dc3804d864d17e43c5b00335a405a3bc4a30861838ac4599a213231e132` | 0 |
| secp256k1-sys/depend/secp256k1/src/modules/recovery/main_impl.h | 6985 | `197bdb189d471cfb9123cab1b1beb5118e89985e4688d00781fd554aa6fa3c09` | 0 |
| secp256k1-sys/depend/secp256k1/src/modules/schnorrsig/main_impl.h | 11292 | `b55b1d634b9bcac79c10278b2d1407cc0bcad13c813bc65ff0deccd6f117adb1` | 0 |
| secp256k1-sys/depend/secp256k1/src/precompute_ecmult.c | 4134 | `eab942df74b984eb0cb55b924344391a399bb07472886501b19776e955478950` | 0 |
| secp256k1-sys/depend/secp256k1/src/precompute_ecmult_gen.c | 3939 | `77e375055b057465e20bb0bc703f46203c16cb41b98ce76856b53b88a6116fc1` | 0 |
| secp256k1-sys/depend/secp256k1/src/precomputed_ecmult.c | 2409228 | `44c8513c966cd6f49ecc57a5a623dbb2e9f17d70fa09039fce0738d2de515c79` | 0 |
| secp256k1-sys/depend/secp256k1/src/precomputed_ecmult.h | 1665 | `cee6422b15bd9fe22fd5306613cf2cabd690490bebe3afd794bc8961e92191e5` | 0 |
| secp256k1-sys/depend/secp256k1/src/precomputed_ecmult_gen.c | 259735 | `feefab4d4c735d9fd3e76271eeeda476e9859022e5c845bd8a3f83947cf38385` | 0 |
| secp256k1-sys/depend/secp256k1/src/precomputed_ecmult_gen.h | 1013 | `c045bde13bd99de253b19351959d1c0411f0398a53c15e5c2e20a5a0f05f1e9f` | 0 |
| secp256k1-sys/depend/secp256k1/src/scalar.h | 6075 | `d3561ecba79556e0d7d2a3f0cf93398bd1f2353441cb0abdd9f8fc49ad67c04b` | 0 |
| secp256k1-sys/depend/secp256k1/src/scalar_4x64.h | 811 | `1f7e75c03494ed55e6466b84507e3f240ad5616bc85a8e1f9f46daaa3150fd35` | 0 |
| secp256k1-sys/depend/secp256k1/src/scalar_4x64_impl.h | 35169 | `183eaa00def71b4b240eda3354968de160b8908b4a891399d75622e593969924` | 0 |
| secp256k1-sys/depend/secp256k1/src/scalar_8x32.h | 735 | `9f77522d7fd95caf61693492fc2883800722f2978f64fcf04420a3daec0d13e2` | 0 |
| secp256k1-sys/depend/secp256k1/src/scalar_8x32_impl.h | 30216 | `4ef4a71103799cf6192dbcd6e49da527ec022abb5380147cda44761e66d906f7` | 0 |
| secp256k1-sys/depend/secp256k1/src/scalar_impl.h | 12744 | `c4c79e9d73303c958128906625a1c96fe35e06fcd7a2c0dea282c827088bc4c3` | 0 |
| secp256k1-sys/depend/secp256k1/src/scalar_low.h | 1145 | `4138194717181b6227fc03529f1e5fe54789515f0d3ee83b5c258b28fdb2fd92` | 0 |
| secp256k1-sys/depend/secp256k1/src/scalar_low_impl.h | 6411 | `570e203ca151e15563312a753715780b01d23a5a1f171c5511f71af38b818ab8` | 0 |
| secp256k1-sys/depend/secp256k1/src/scratch.h | 2182 | `aa9c7b6d2e1e68d17dd2e70d282bd0227302bae7aa7396062da205429009c967` | 0 |
| secp256k1-sys/depend/secp256k1/src/scratch_impl.h | 2867 | `02c34bdf19ebcaf23d24b0b6d4b9aae31809d3edec285386bddbef3cf7b2ea7d` | 0 |
| secp256k1-sys/depend/secp256k1/src/secp256k1.c | 30671 | `39e452b52a252c9389ae99ecd26489f34122018ad053b566ebf213ad874af476` | 0 |
| secp256k1-sys/depend/secp256k1/src/selftest.h | 1351 | `cca836fd26cb12b60a66ad808c9e89bd42a45c3220626def81437f7fbae6f97f` | 0 |
| secp256k1-sys/depend/secp256k1/src/testrand.h | 1886 | `b1708cdab67d44311b97af6f77c719f6dfc03d8c53e5e686bc1d9fd967a49687` | 0 |
| secp256k1-sys/depend/secp256k1/src/testrand_impl.h | 5805 | `5303c670a157d2857c1f5de4567f73d04b2f5a37434eae1fcaabe00597dab57a` | 0 |
| secp256k1-sys/depend/secp256k1/src/testutil.h | 4603 | `a2f705686ab565024949f5a4018ccb978b4c9e0eb11fec58a771b17467009654` | 0 |
| secp256k1-sys/depend/secp256k1/src/util.h | 14727 | `224fda59fc8ed42d1b259dfef2ecdf130a3e4c126cced79d0d1362521518153d` | 0 |
| secp256k1-sys/depend/secp256k1/src/util_local_visibility.h | 402 | `d47d4a58f40157ab2a298151f366c5ebec8f7a1e7aaba88e36b530b1c01584ca` | 0 |
| secp256k1-sys/depend/secp256k1/tools/symbol-check.py | 2426 | `fc152ef1c87a7c0c1d6487fe3f451068f42efe3c1a7205571404226c2a364f2b` | 0 |
| secp256k1-sys/depend/secp256k1/tools/wycheproof_utils.py | 427 | `9f2c2368953eeb3c9b7c3b31a807cde76b3106df93fbb975993638d5eb1a1e8a` | 0 |
| secp256k1-sys/src/lib.rs | 70718 | `415aae64b2c5f2f51644db0273decde6dedf092e159d583810f1bd439f759d73` | 0 |
| secp256k1-sys/src/macros.rs | 3221 | `5cc2d18ba578ab1bd5f24cda2e5d04bec238e0ac5d615845b5f49f13aed86719` | 0 |
| secp256k1-sys/src/recovery.rs | 7321 | `0b3128bbdb9d7b6896d23fa70a495644627b22fbcbcea2013bfc12d5cab49882` | 0 |
| secp256k1-sys/src/types.rs | 3312 | `5d51de698119d62dae9f7402b415080a4bb3efcf3105cf1d11881fa48474e2d7` | 0 |
| secp256k1-sys/wasm/wasm-sysroot/stdio.h | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| secp256k1-sys/wasm/wasm-sysroot/stdlib.h | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| secp256k1-sys/wasm/wasm-sysroot/string.h | 236 | `fbfdac6ad0b66450c634081c5270b724179fd2b5dd615275489b3c22d275268f` | 0 |
| secp256k1-sys/wasm/wasm.c | 710 | `804c35ac2746282ad01c6bf1bf331ff4bb17843f14750308580575215caaeb6e` | 0 |
| src/constants.rs | 2446 | `b731982fed3921dd7b391c5185cfb80a9bac3519147fe760fe9af10d012e3b56` | 0 |
| src/context/internal_nostd.rs | 6529 | `6a41454cde81eb9f37b40f7f35977575766c89d3a275ad616f689178424045d7` | 0 |
| src/context/internal_std.rs | 3291 | `ace7fc791d4ecab0d3e171ae20f3e377f23b6eb0a5ea8cf700bd99382db15a57` | 0 |
| src/context/mod.rs | 16342 | `8c2ad10e9f9a1a23a9ea56ebabaa4e7c5a12c41bf739addff45a1b394ae3b1b2` | 0 |
| src/context/spinlock.rs | 7872 | `0f63af558b09bcc4a563853efa343628c3de044e86a6aa1fe9f412904f1f0d39` | 0 |
| src/ecdh.rs | 8625 | `b7a382d0fbefc1944aecab86e5fa62e1fcb07d16ab97b89a1c5352357428009c` | 0 |
| src/ecdsa/mod.rs | 19911 | `c2501fabd9e06440ba379326e1179f0a1501d86b6c8025278e081bfc7e703599` | 0 |
| src/ecdsa/recovery.rs | 16666 | `acec0d5ab6859c999ddcf8b441a6e5014022e9e91b310443f4be9d7f0654fe01` | 0 |
| src/ecdsa/serialized_signature.rs | 9043 | `f7083c232563eed68b246c14d7b4329152b41a1ab5cad21053cf7d80a19cfd5e` | 0 |
| src/ellswift.rs | 46614 | `0f8263f7a08819e9cee525235766c818379d5005ff04a7e7b9be3e48b88b7518` | 2 |
| src/key/mod.rs | 75790 | `811fd2982f101aa42c8157f37db01cb4b4e13850686cdb596319e20b761c8e15` | 3 |
| src/key/secret.rs | 11958 | `df49878912b209974289c9d479c12ab2b19c1a6d0638539ad5dd62d1401936ed` | 0 |
| src/lib.rs | 42297 | `41069109679af98f2c060205d76170ecba86ad5f26ad30c4894d1b751b09d6a9` | 3 |
| src/macros.rs | 4164 | `31ece8ad2fa96786df7cc5498e455f454dee353c6a0383c2a282f87a034d0b7b` | 0 |
| src/musig.rs | 69169 | `a22fd3466a745b4fad5e685c04a0cda15648102fc580db8b29eb1be41414cf60` | 0 |
| src/scalar.rs | 5109 | `59603163ac5b2947abbbe913d83a8950713a87afaad29aa929c821e5fc0d21ec` | 0 |
| src/schnorr.rs | 31606 | `259030c32d226d4f1ef6ccbe7426f0f86874ec494aed531855f743140af02a25` | 28 |
| src/secret.rs | 7120 | `b9f4f2ee7314d6ba80e8ecc1d50b3a9050671acc2e2649109e7831db5977f8ab` | 3 |
| src/serde_util.rs | 3017 | `a3c07e7486b54c50e5fbd1c47391cd84f3debfbad051036ee5e42de920620d9e` | 0 |
