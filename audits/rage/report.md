# Отчёт об аудите безопасности и постквантовой готовности

**Проект:** rage @ b5b68c4f4f7e · str4d (rage / age encryption) — публичный репозиторий (пассивная проверка)
| | |
|---|---|
| Организация | QSI |
| Дата отчёта | 2026-10-28 12:48 UTC |
| Версия отчёта | 1 |
| Запуск аудита | 5a56c499-e3a2-4c96-9fd8-9e480d717111 (Документальный аудит) |
| Версия анализатора | qsi-engine 1.2.0 |
| Профиль риска | Разработчик ПО безопасности |
| SHA-256 содержимого | `ccf0d5cdc01d4ae253800f38b6649385c95e635670a1525a81a7ba2dd7702868` |
| Ключ подписи (Ed25519, отпечаток SHA-256; подпись — отдельный файл report.sig.json) | `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e` |
> Отчёт содержит результаты автоматизированного и документального анализа в указанных границах. Он не является юридическим заключением, сертификацией или подтверждением соответствия какому-либо стандарту.

## 1. Резюме для руководства

- Критическая: **1**
- Высокая: **1**
- Средняя: **3**
- Низкая: **18**
- Информационная: **3**

- Подтверждённая техническая уязвимость: 0
- Известная уязвимая версия компонента: 20
- Подтверждённая ошибка конфигурации: 0
- Потенциальный криптографический риск: 0
- Долгосрочный постквантовый риск: 3
- Рекомендация по улучшению: 3
- Недостаточность данных: 0

Неравенство Моски (x + y > z): x = 10, y = 3, z = 8 → при этом сценарии миграция завершится слишком поздно. _z — плановое допущение профиля риска, а не прогноз. Публично известного криптографически значимого квантового компьютера сегодня не существует._

**Постквантовая зрелость: Уровень 1 из 4 — постквантовый код есть, но не подключён.** Следующий шаг: Подключите имеющийся постквантовый примитив к критичному пути (обёртка ключей или канал) в гибридной схеме и проверьте совместимость.

## 2. Область и границы проверки

Режим: Документальный аудит

Репозиторий: <https://github.com/str4d/rage> @ `b5b68c4f4f7ea5c368bc060f6fe0237549c3a13f` — ссылки в доказательствах открывают строки на этом коммите.

54 файлов, всего 639435 байт, редактирований: 10; список SHA-256 по файлам — в приложении C.

## 3. Методология

| Область | Статус | Количество | Примеры |
|---|---|---|---|
| dependencies | проверено | 6 | Cargo.lock: 382 dependencies parsed (382 pinned); Cargo.toml: 31 dependencies parsed (0 pinned); age/Cargo.toml: 51 dependencies parsed (1 pinned) |
| source_code | проверено | 47 | age/src/cli_common/error.rs: 116 lines scanned with 16 rule patterns and 122 registry patterns; age/src/cli_common/file_io.rs: 471 lines scanned with 16 rule patterns and 122 registry patterns; 38 lines in #[cfg(test)] modules ignored; age/src/cli_common/identities.rs: 273 lines scanned with 16 rule patterns and 122 registry patterns |
| keys | проверено | 10 | age/src/ssh/identity.rs: the marker at line 333 is a PEM header without key material (a literal in code that parses or writes PEM, or a documentation placeholder); age/src/ssh/identity.rs: the marker at line 366 is a PEM header without key material (a literal in code that parses or writes PEM, or a documentation placeholder); age/src/ssh/identity.rs: private key block at line 398 is test data (test code) |
| certificates_and_keys | проверено | 1 | age/src/ssh/identity.rs: certificates/keys parsed |
| osv_advisories | проверено | 1 | 382 pinned packages queried at OSV.dev; 12 affected (3 of them only in development or build dependencies) |

_Длинные списки здесь сгруппированы; полный список по файлам — в JSON-версии отчёта, подписанной тем же ключом._

## 4. Проверенные и непроверенные активы

- Нет

## 5. Краткое описание архитектуры

Static review of the source tree rage at b5b68c4f4f7ea5c368bc060f6fe0237549c3a13f. 54 files analysed; of 320 files, 219 are test, fuzzing, benchmark or example code and were left out, 47 are not read by any analyzer, 0 exceed the per-file limit and 0 did not fit the total limit. No requests were sent to the owner's systems.

## 6. Общая оценка состояния безопасности

- Ориентировочный индекс состояния: **43** / 100 — _Рассчитан по находкам в области проверки (подтверждённые и потенциальные проблемы, взвешенные по серьёзности). Ориентировочный; не сравним между аудитами с разной областью._
- Доля квантово-уязвимых элементов инвентаризации: 30.2%

## 7. Подробное описание находок

### QSI-2026-04937 — zip 8.6.0 затронут RUSTSEC-2026-0369

- Серьёзность: **Критическая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:crates.io/zip@8.6.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 12:48 UTC
- Балл приоритета: 54.3 / 100
- CVSS v3.1: 9.1 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H`)

OSV.dev сообщает RUSTSEC-2026-0369 для пакета crates.io zip версии 8.6.0: ZipStreamReader::extract() and ZipArchive::extract() apply Unix permissions through symlinks without confining the target. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0369
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0369](https://osv.dev/vulnerability/RUSTSEC-2026-0369) · manifest · SHA-256 9aef5f045615f47bcb38c8fa6cc96616234dcdc509a2b8225bfe413eddd70e04_

```
{"id": "RUSTSEC-2026-0369", "aliases": ["GHSA-4684-h2q9-2vcp"], "modified": "2026-10-16T23:30:02.387698467Z", "summary": "ZipStreamReader::extract() and ZipArchive::extract() apply Unix permissions through symlinks without confining the target", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (9.0.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-04935 — zip 8.6.0 затронут RUSTSEC-2026-0367

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:crates.io/zip@8.6.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 12:48 UTC
- Балл приоритета: 50.3 / 100
- CVSS v3.1: 7.3 (`CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H`)

OSV.dev сообщает RUSTSEC-2026-0367 для пакета crates.io zip версии 8.6.0: Insecure Preservation of SUID/SGID Bits during ZIP Extraction Leading to Potential Privilege Escalation. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0367
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0367](https://osv.dev/vulnerability/RUSTSEC-2026-0367) · manifest · SHA-256 15f1d3dcd40074f7815d474465495a74632c16549a413ab89f8ddf2c2b88fbb5_

```
{"id": "RUSTSEC-2026-0367", "aliases": ["GHSA-vv5m-jxxh-4627"], "modified": "2026-10-16T23:30:02.392172556Z", "summary": " Insecure Preservation of SUID/SGID Bits during ZIP Extraction Leading to Potential Privilege Escalation", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (9.0.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-04934 — rsa 0.10.0-rc.18 затронут RUSTSEC-2023-0071 (CVE-2023-49092)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:crates.io/rsa@0.10.0-rc.18`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 12:48 UTC
- Балл приоритета: 44.3 / 100
- CVSS v3.1: 5.9 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:N/A:N`)

OSV.dev сообщает RUSTSEC-2023-0071 (CVE-2023-49092) для пакета crates.io rsa версии 0.10.0-rc.18: Marvin Attack: potential key recovery through timing sidechannels. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2023-0071
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2023-0071](https://osv.dev/vulnerability/RUSTSEC-2023-0071) · manifest · SHA-256 0db94e1eb8892ff3c781df371743247db7a773258576ae414ad6431dd6e38cbc_

```
{"id": "RUSTSEC-2023-0071", "aliases": ["CVE-2023-49092", "GHSA-4grx-2x9w-596c", "GHSA-c38w-74pg-36hr"], "modified": "2026-09-14T09:45:02.996132556Z", "summary": "Marvin Attack: potential key recovery through timing sidechannels", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:N/A:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (пока не выпущена; меры смягчения — в бюллетене).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-04928 — Квантово-уязвимый X25519: обёртка ключей и шифрование хранимых данных (3 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `source-code:X25519:key_wrapping`
- Источник данных: age/src/native/x25519.rs
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-28 12:48 UTC
- Балл приоритета: 38.0 / 100
- CVSS v3.1: неприменимо

9 упоминаний X25519 в 3 файл(ах), например age/src/native/x25519.rs:16. Роль по путям, именам функций и соседнему коду: обёртка ключей и шифрование хранимых данных. Ключи или данные, зашифрованные на эти открытые ключи, хранятся: кто скопирует их сейчас, расшифрует, когда появится CRQC («собери сейчас — расшифруй потом»).

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте age/src/native/x25519.rs:16 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [age/src/native/x25519.rs](https://github.com/str4d/rage/blob/b5b68c4f4f7ea5c368bc060f6fe0237549c3a13f/age/src/native/x25519.rs#L16) · line 16 · SHA-256 05df6829be49cabd10d88d6036ce76d2ba7040e231172dca53924a0750b6570f_

```
   15 | use subtle::ConstantTimeEq;
   16 | use x25519_dalek::{EphemeralSecret, PublicKey, StaticSecret};
   17 | use zeroize::Zeroize;
```

_file_excerpt · [age/src/ssh/identity.rs](https://github.com/str4d/rage/blob/b5b68c4f4f7ea5c368bc060f6fe0237549c3a13f/age/src/ssh/identity.rs#L20) · line 20 · SHA-256 1ee07b7a7c8bc78c730da898a54e4637f245085669e2241423890dd326877b88_

```
   19 | use std::io;
   20 | use x25519_dalek::{PublicKey as X25519PublicKey, StaticSecret};
   21 | use zeroize::Zeroize;
```

_file_excerpt · [age/src/ssh/identity.rs](https://github.com/str4d/rage/blob/b5b68c4f4f7ea5c368bc060f6fe0237549c3a13f/age/src/ssh/identity.rs#L103) · line 103 · SHA-256 87ba13f8a1497fd71ed3922f4e03c558c1286a2a000a6bcef5cc9ce029e2c31c_

```
  102 |                 }
  103 |                 if stanza.body.len() != crate::x25519::ENCRYPTED_FILE_KEY_BYTES {
  104 |                     return Some(Err(DecryptError::InvalidHeader));
```

_file_excerpt · [age/src/ssh/identity.rs](https://github.com/str4d/rage/blob/b5b68c4f4f7ea5c368bc060f6fe0237549c3a13f/age/src/ssh/identity.rs#L108) · line 108 · SHA-256 0be5d59c2834e0cc9449d59da2a0d0ef4d12c1baafef72fc5be3f97c0be8471b_

```
  107 |                 let epk =
  108 |                     base64_arg::<_, { crate::x25519::EPK_LEN_BYTES }, 33>(stanza.args.get(1)?)?
  109 |                         .into();
```

_file_excerpt · [age/src/ssh/recipient.rs](https://github.com/str4d/rage/blob/b5b68c4f4f7ea5c368bc060f6fe0237549c3a13f/age/src/ssh/recipient.rs#L24) · line 24 · SHA-256 6abe103c9a43a94a19a02b55300b17593e658208804bda30ec6d4a8f8935c00a_

```
   23 | use sha2::Sha256;
   24 | use x25519_dalek::{EphemeralSecret, PublicKey as X25519PublicKey, StaticSecret};
   25 | 
```

_file_excerpt · [age/src/ssh/recipient.rs](https://github.com/str4d/rage/blob/b5b68c4f4f7ea5c368bc060f6fe0237549c3a13f/age/src/ssh/recipient.rs#L181) · line 181 · SHA-256 900291691f762d6c9ce5739d76737af6565a43944e9e9595ede307ce1202091b_

```
  180 |             Recipient::SshEd25519(ssh_key, ed25519_pk) => {
  181 |                 let pk: X25519PublicKey = ed25519_pk.to_montgomery().to_bytes().into();
  182 | 
```

_file_excerpt · [age/src/ssh/recipient.rs](https://github.com/str4d/rage/blob/b5b68c4f4f7ea5c368bc060f6fe0237549c3a13f/age/src/ssh/recipient.rs#L184) · line 184 · SHA-256 a3dd61d18bb5abc2d5d5ecda2460b8425e0990823960a38a07f6f02254910caf_

```
  183 |                 let esk = EphemeralSecret::random_from_rng(&mut rng);
  184 |                 let epk: X25519PublicKey = (&esk).into();
  185 | 
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Оборачивайте ключи ML-KEM или гибридным KEM (X25519 + ML-KEM-768) и переоберните хранимые ключи; для данных, которые уже могли скопировать, нужна отдельная оценка.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-04927 — Квантово-уязвимый X25519: роль не определена (6 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `source-code:X25519:general`
- Источник данных: age/src/cli_common/recipients.rs
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-28 12:48 UTC
- Балл приоритета: 35.3 / 100
- CVSS v3.1: неприменимо

10 упоминаний X25519 в 6 файл(ах), например age/src/cli_common/recipients.rs:5. Роль по путям, именам функций и соседнему коду: роль не определена. По коду не видно, что защищают ключи; приоритет определит проверка.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте age/src/cli_common/recipients.rs:5 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [age/src/cli_common/recipients.rs](https://github.com/str4d/rage/blob/b5b68c4f4f7ea5c368bc060f6fe0237549c3a13f/age/src/cli_common/recipients.rs#L5) · line 5 · SHA-256 949c4c42018679fc2651bed9e0f1f3b1745770fe5a7fb8e36b731e989e25846d_

```
    4 | use super::{ReadError, identities::parse_identity_files};
    5 | use crate::{Recipient, identity::RecipientsAccumulator, tag, tagpq, util::LimitedReader, x25519};
    6 | 
```

_file_excerpt · [age/src/cli_common/recipients.rs](https://github.com/str4d/rage/blob/b5b68c4f4f7ea5c368bc060f6fe0237549c3a13f/age/src/cli_common/recipients.rs#L59) · line 59 · SHA-256 67e9a05a95b80abd2572165233020bf982389af48ab6e32fc58921fbabd4bd0c_

```
   58 | ) -> Result<(), ReadError> {
   59 |     if let Ok(pk) = s.parse::<x25519::Recipient>() {
   60 |         recipients.push(Box::new(pk));
```

_file_excerpt · [age/src/identity.rs](https://github.com/str4d/rage/blob/b5b68c4f4f7ea5c368bc060f6fe0237549c3a13f/age/src/identity.rs#L10) · line 10 · SHA-256 90fb4d93d25a26413a6a2e13c88d3522480c3fe8ad04bd9a4714789f9afefbad_

```
    9 |     Callbacks, DecryptError, EncryptError, IdentityFileConvertError, NoCallbacks,
   10 |     util::LimitedReader, x25519,
   11 | };
```

_file_excerpt · [age/src/identity.rs](https://github.com/str4d/rage/blob/b5b68c4f4f7ea5c368bc060f6fe0237549c3a13f/age/src/identity.rs#L25) · line 25 · SHA-256 36e6ff8be827a3d1ca9c83b6bea9f135da0c2e3134d6065b0db4a549b1a84b24_

```
   24 |     /// The standard age identity type.
   25 |     Native(x25519::Identity),
   26 |     /// A plugin-compatible identity.
```

_file_excerpt · [age/src/identity.rs](https://github.com/str4d/rage/blob/b5b68c4f4f7ea5c368bc060f6fe0237549c3a13f/age/src/identity.rs#L92) · line 92 · SHA-256 5dbfb3ab6c2704e8c45630f92fe5b306c65e38bd00cda43237b0113c8a40e8e5_

```
   91 | 
   92 |             match line.parse::<x25519::Identity>() {
   93 |                 Ok(identity) => {
```

_file_excerpt · [age/src/lib.rs](https://github.com/str4d/rage/blob/b5b68c4f4f7ea5c368bc060f6fe0237549c3a13f/age/src/lib.rs#L259) · line 259 · SHA-256 97aa08d50fd46207d19c0dbcece4d115dab63ea31e056bc595a5f0d1de4dc1d0_

```
  258 | pub use native::tagpq;
  259 | pub use native::x25519;
  260 | 
```

_file_excerpt · [age/src/native.rs](https://github.com/str4d/rage/blob/b5b68c4f4f7ea5c368bc060f6fe0237549c3a13f/age/src/native.rs#L9) · line 9 · SHA-256 05ec1745e4a1eddf7f1b06b954c98bdc480a6ed460e540bdf7f35b369715f3e3_

```
    8 | pub mod tagpq;
    9 | pub mod x25519;
   10 | 
```

_file_excerpt · [rage/build.rs](https://github.com/str4d/rage/blob/b5b68c4f4f7ea5c368bc060f6fe0237549c3a13f/rage/build.rs#L258) · line 258 · SHA-256 99ac994fe5cd88e6869eb03bccd9531e1423147477843660c83708e8f60cdab2_

```
  257 |                     .paragraph(fl!("man-rage-recipients-and-identities"))
  258 |                     .subheading(fl!("man-rage-native-x25519-keys-heading"))
  259 |                     .paragraph(fl!(
```

_file_excerpt · [rage/build.rs](https://github.com/str4d/rage/blob/b5b68c4f4f7ea5c368bc060f6fe0237549c3a13f/rage/build.rs#L260) · line 260 · SHA-256 b74d073343a9a1960ff582b2292f1366a84e5fd86311591a7ba8e0e30cf6307d_

```
  259 |                     .paragraph(fl!(
  260 |                         "man-rage-native-x25519-keys",
  261 |                         example_age_recipient = "age1gde3ncmahlqd9gg50tanl99r960llztrhfapnmx853s4tjum03uqfssgdh",
```

_file_excerpt · [rage/src/bin/rage-keygen/main.rs](https://github.com/str4d/rage/blob/b5b68c4f4f7ea5c368bc060f6fe0237549c3a13f/rage/src/bin/rage-keygen/main.rs#L57) · line 57 · SHA-256 d3f1ab0f99eee13a2589f6865cb86ef7e63c343058c209297f0b40cba1267813_

```
   56 | fn generate(mut output: file_io::OutputWriter) -> io::Result<()> {
   57 |     let sk = age::x25519::Identity::generate();
   58 |     let pk = sk.to_public();
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Классифицируйте каждое использование, зафиксируйте сроки жизни данных и запланируйте миграцию на Гибридное установление ключей с ML-KEM (FIPS 203), например X25519MLKEM768 в TLS 1.3 или mlkem768x25519-sha256 в SSH; введите уровень абстракции для криптогибкости.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-04929 — Квантово-уязвимый RSA: аутентификация и идентификация (сертификаты, токены, аттестация устройств) (3 файл(ов))

- Серьёзность: **Низкая** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `source-code:RSA:authentication`
- Источник данных: age/src/ssh/identity.rs
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-28 12:48 UTC
- Балл приоритета: 28.3 / 100
- CVSS v3.1: неприменимо

9 упоминаний RSA в 3 файл(ах), например age/src/ssh/identity.rs:38. Роль по путям, именам функций и соседнему коду: аутентификация и идентификация (сертификаты, токены, аттестация устройств). Краткоживущая аутентификация безопасна до появления CRQC; долгоживущим идентификаторам (аттестация устройств, ключи УЦ и SSH) план нужен раньше.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте age/src/ssh/identity.rs:38 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [age/src/ssh/identity.rs](https://github.com/str4d/rage/blob/b5b68c4f4f7ea5c368bc060f6fe0237549c3a13f/age/src/ssh/identity.rs#L38) · line 38 · SHA-256 de035e6101f0cc8f4ddb886275317cee992d29d5439c38800bf9838042a88fbd_

```
   37 |     /// An ssh-rsa private key.
   38 |     SshRsa(Vec<u8>, Box<rsa::RsaPrivateKey>),
   39 |     /// An ssh-ed25519 key pair.
```

_file_excerpt · [age/src/ssh/recipient.rs](https://github.com/str4d/rage/blob/b5b68c4f4f7ea5c368bc060f6fe0237549c3a13f/age/src/ssh/recipient.rs#L42) · line 42 · SHA-256 479bf142c9167d7508156b2bb610dc3f5f7b0340b5df42a781aca3cdf0e5ab43_

```
   41 |     /// An ssh-rsa public key.
   42 |     SshRsa(Vec<u8>, rsa::RsaPublicKey),
   43 |     /// An ssh-ed25519 public key.
```

_file_excerpt · [age/src/ssh/recipient.rs](https://github.com/str4d/rage/blob/b5b68c4f4f7ea5c368bc060f6fe0237549c3a13f/age/src/ssh/recipient.rs#L77) · line 77 · SHA-256 6951b047acbed0bc3e239453ac347280898f4087616b23546fd33c6aada0285a_

```
   76 |     fn from_str(s: &str) -> Result<Self, Self::Err> {
   77 |         match ssh_recipient(rsa::RsaPublicKey::MAX_SIZE)(s) {
   78 |             Ok((_, ParsedRecipient::Supported(pk))) => Ok(pk),
```

_file_excerpt · [age/src/ssh/recipient.rs](https://github.com/str4d/rage/blob/b5b68c4f4f7ea5c368bc060f6fe0237549c3a13f/age/src/ssh/recipient.rs#L124) · line 124 · SHA-256 bff2dfed80a0d3876ae441e29798cd20bba3594c349b887486d2c80a81d28b78_

```
  123 |             | Identity::Encrypted(EncryptedKey { ssh_key, .. }) => {
  124 |                 match read_ssh::rsa_pubkey(rsa::RsaPublicKey::MAX_SIZE)(&ssh_key) {
  125 |                     Ok((_, pk)) => {
```

_file_excerpt · [age/src/ssh.rs](https://github.com/str4d/rage/blob/b5b68c4f4f7ea5c368bc060f6fe0237549c3a13f/age/src/ssh.rs#L346) · line 346 · SHA-256 7e3785d0dbcd802591dcf43f3e19518c5a11074bbe503579789d417cce71a346_

```
  345 |     /// - [OpenSSH serialization code](https://github.com/openssh/openssh-portable/blob/4103a3ec7c68493dbc4f0994a229507e943a86d3/sshkey.c#L3187-L3198)
  346 |     fn openssh_rsa_privkey(input: &[u8]) -> IResult<&[u8], rsa::RsaPrivateKey> {
  347 |         delimited(
```

_file_excerpt · [age/src/ssh.rs](https://github.com/str4d/rage/blob/b5b68c4f4f7ea5c368bc060f6fe0237549c3a13f/age/src/ssh.rs#L351) · line 351 · SHA-256 4053b2391fbea71b39dd399191ef97f6307a2fb093522f2d6f7ac1d7eda26864_

```
  350 |                 (mpint, mpint, mpint, mpint, mpint, mpint),
  351 |                 |(n, e, d, _iqmp, p, q)| rsa::RsaPrivateKey::from_components(n, e, d, vec![p, q]),
  352 |             ),
```

_file_excerpt · [age/src/ssh.rs](https://github.com/str4d/rage/blob/b5b68c4f4f7ea5c368bc060f6fe0237549c3a13f/age/src/ssh.rs#L506) · line 506 · SHA-256 7e7e503abedc0514c33f3905e22bdec016c5f8f737be09dd7bee1c7ea3e02b2e_

```
  505 |         max_size: usize,
  506 |     ) -> impl Fn(&[u8]) -> IResult<&[u8], Option<rsa::RsaPublicKey>> {
  507 |         move |input| {
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Делайте учётные данные краткоживущими и планируйте сертификаты, токены и ключи ML-DSA по мере поддержки в экосистеме.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-04931 — crypto-bigint 0.7.5 затронут RUSTSEC-2026-0387 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/crypto-bigint@0.7.5`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 12:48 UTC
- Балл приоритета: 20.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0387 для пакета crates.io crypto-bigint версии 0.7.5: Multiple timing variability issues in operations intended to be constant-time. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0387
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0387](https://osv.dev/vulnerability/RUSTSEC-2026-0387) · manifest · SHA-256 eab63427da988e95becf061fd8169abcb9634f743aeeb7567dfa2ba2667b05a5_

```
{"id": "RUSTSEC-2026-0387", "aliases": [], "modified": "2026-10-24T03:45:02.365137418Z", "summary": "Multiple timing variability issues in operations intended to be constant-time", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.7.6).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-04932 — ctutils 0.4.2 затронут RUSTSEC-2026-0385 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/ctutils@0.4.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 12:48 UTC
- Балл приоритета: 20.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0385 для пакета crates.io ctutils версии 0.4.2: Non-constant-time mask generation and `u128` comparisons. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0385
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0385](https://osv.dev/vulnerability/RUSTSEC-2026-0385) · manifest · SHA-256 200470326c8a5ad19deb3639dff41d33749b1153097b6b87ef95e4beec747848_

```
{"id": "RUSTSEC-2026-0385", "aliases": [], "modified": "2026-10-23T08:30:02.389575143Z", "summary": "Non-constant-time mask generation and `u128` comparisons", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.4.4).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-04936 — zip 8.6.0 затронут RUSTSEC-2026-0368 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/zip@8.6.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 12:48 UTC
- Балл приоритета: 20.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0368 для пакета crates.io zip версии 8.6.0: zip: `ZipArchive::extract` creates symbolic links whose attacker-controlled targets are outside the destination directory. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0368
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0368](https://osv.dev/vulnerability/RUSTSEC-2026-0368) · manifest · SHA-256 5290c9a29df3d85ab102844569d01115b101b377c4c3e6ad6ff25e6c67e65a22_

```
{"id": "RUSTSEC-2026-0368", "aliases": ["GHSA-4v9h-p7m9-rh26"], "modified": "2026-10-16T23:30:02.383750571Z", "summary": "zip: `ZipArchive::extract` creates symbolic links whose attacker-controlled targets are outside the destination directory", "severity": null, "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (9.0.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-04938 — zstd 0.13.3 затронут RUSTSEC-2026-0391 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/zstd@0.13.3`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 12:48 UTC
- Балл приоритета: 20.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0391 для пакета crates.io zstd версии 0.13.3: Data from an abandoned stream leaks into the next stream on a reused context. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Проверенный код не упоминает затронутые функции (zstd::stream::raw::Decoder::with_context, zstd::stream::raw::Encoder::with_context); zstd приходит через другие зависимости, которые могут их вызывать.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0391
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0391](https://osv.dev/vulnerability/RUSTSEC-2026-0391) · manifest · SHA-256 c5a6274e5a4cfb8793fcf3f343ddadadd6d41a200d24a392d8f363faa59b0e78_

```
{"id": "RUSTSEC-2026-0391", "aliases": [], "modified": "2026-10-26T14:00:04.269245609Z", "summary": "Data from an abandoned stream leaks into the next stream on a reused context", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.14.3).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-04939 — zstd-safe 7.2.4 затронут RUSTSEC-2026-0395 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/zstd-safe@7.2.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 12:48 UTC
- Балл приоритета: 20.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0395 для пакета crates.io zstd-safe версии 7.2.4: Use-after-free with `CParameter::StableInBuffer`. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Проверенный код не упоминает затронутые функции (zstd_safe::CCtx::set_parameter); zstd-safe приходит через другие зависимости, которые могут их вызывать.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0395
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0395](https://osv.dev/vulnerability/RUSTSEC-2026-0395) · manifest · SHA-256 cf314e3df3f714ad17083f648e4d6822839805759c13c152cf2b2edcfbba9cdb_

```
{"id": "RUSTSEC-2026-0395", "aliases": [], "modified": "2026-10-26T14:00:06.388344282Z", "summary": "Use-after-free with `CParameter::StableInBuffer`", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (8.2.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-04940 — zstd-safe 7.2.4 затронут RUSTSEC-2026-0396 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/zstd-safe@7.2.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 12:48 UTC
- Балл приоритета: 20.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0396 для пакета crates.io zstd-safe версии 7.2.4: `Seekable` reads a NULL or out-of-bounds seek table. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Проверенный код не упоминает затронутые функции (zstd_safe::seekable::SeekTable::frame_decompressed_size, zstd_safe::seekable::Seekable::decompress, zstd_safe::seekable::Seekable::decompress_frame, zstd_safe::seekable::Seekable::frame_decompressed_size, zstd_safe::seekable::Seekable::offset_to_frame_index); zstd-safe приходит через другие зависимости, которые могут их вызывать.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0396
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0396](https://osv.dev/vulnerability/RUSTSEC-2026-0396) · manifest · SHA-256 46019c3c1c8cc1772c03fcccbfa90a2b7502cdb744481795fef991bd88bf8e23_

```
{"id": "RUSTSEC-2026-0396", "aliases": [], "modified": "2026-10-26T14:00:05.789682118Z", "summary": "`Seekable` reads a NULL or out-of-bounds seek table", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (8.2.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-04941 — zstd-safe 7.2.4 затронут RUSTSEC-2026-0397 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/zstd-safe@7.2.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 12:48 UTC
- Балл приоритета: 20.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0397 для пакета crates.io zstd-safe версии 7.2.4: `OutBuffer::around_pos` exposes uninitialized memory. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Проверенный код не упоминает затронутые функции (zstd_safe::OutBuffer::around_pos); zstd-safe приходит через другие зависимости, которые могут их вызывать.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0397
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0397](https://osv.dev/vulnerability/RUSTSEC-2026-0397) · manifest · SHA-256 e1cc2d6a8e69a560eb15d719dcb988b36e18b940b8913145ec52a73efd0b9fcc_

```
{"id": "RUSTSEC-2026-0397", "aliases": [], "modified": "2026-10-26T14:00:05.089587004Z", "summary": "`OutBuffer::around_pos` exposes uninitialized memory", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (8.2.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-04942 — zstd-safe 7.2.4 затронут RUSTSEC-2026-0398 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/zstd-safe@7.2.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 12:48 UTC
- Балл приоритета: 20.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0398 для пакета crates.io zstd-safe версии 7.2.4: `Seekable::decompress` sets a `Vec` length beyond its capacity for offsets past the end. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Проверенный код не упоминает затронутые функции (zstd_safe::seekable::AdvancedSeekable::decompress, zstd_safe::seekable::Seekable::decompress); zstd-safe приходит через другие зависимости, которые могут их вызывать.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0398
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0398](https://osv.dev/vulnerability/RUSTSEC-2026-0398) · manifest · SHA-256 01887ac4409fe66647c178d3ac91c674dafafb9134960f58c0f4ffcaa080acda_

```
{"id": "RUSTSEC-2026-0398", "aliases": [], "modified": "2026-10-26T14:00:05.092082939Z", "summary": "`Seekable::decompress` sets a `Vec` length beyond its capacity for offsets past the end", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (8.2.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-04943 — zstd-safe 7.2.4 затронут RUSTSEC-2026-0399 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/zstd-safe@7.2.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 12:48 UTC
- Балл приоритета: 20.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0399 для пакета crates.io zstd-safe версии 7.2.4: Use-after-free through `init_using_cdict` and `init_using_ddict`. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Проверенный код не упоминает затронутые функции (zstd_safe::CCtx::init_using_cdict, zstd_safe::DCtx::init_using_ddict); zstd-safe приходит через другие зависимости, которые могут их вызывать.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0399
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0399](https://osv.dev/vulnerability/RUSTSEC-2026-0399) · manifest · SHA-256 dde7c9d1fcd35a89a4e462b7b42373ae75187190ebfffa3876d9e2bba20e386a_

```
{"id": "RUSTSEC-2026-0399", "aliases": [], "modified": "2026-10-26T14:00:05.792431051Z", "summary": "Use-after-free through `init_using_cdict` and `init_using_ddict`", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (8.2.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-04944 — zstd-safe 7.2.4 затронут RUSTSEC-2026-0400 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/zstd-safe@7.2.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 12:48 UTC
- Балл приоритета: 20.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0400 для пакета crates.io zstd-safe версии 7.2.4: Use-after-free of a dictionary after a one-shot call on a context with an open stream. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Проверенный код не упоминает затронутые функции (zstd_safe::DCtx::decompress, zstd_safe::DCtx::decompress_using_ddict, zstd_safe::DCtx::decompress_using_dict); zstd-safe приходит через другие зависимости, которые могут их вызывать.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0400
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0400](https://osv.dev/vulnerability/RUSTSEC-2026-0400) · manifest · SHA-256 12a31cd97694259b60fd13de0204d4257a30facebdbf5eb19bc091d2b54c85f6_

```
{"id": "RUSTSEC-2026-0400", "aliases": [], "modified": "2026-10-26T14:00:05.692077560Z", "summary": "Use-after-free of a dictionary after a one-shot call on a context with an open stream", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (8.2.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-04945 — zstd-safe 7.2.4 затронут RUSTSEC-2026-0401 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/zstd-safe@7.2.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 12:48 UTC
- Балл приоритета: 20.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0401 для пакета crates.io zstd-safe версии 7.2.4: Out-of-bounds read in `train_from_buffer` when sample sizes overflow. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Проверенный код не упоминает затронутые функции (zstd_safe::train_from_buffer); zstd-safe приходит через другие зависимости, которые могут их вызывать.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0401
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0401](https://osv.dev/vulnerability/RUSTSEC-2026-0401) · manifest · SHA-256 8f606743a027e187f8815975be52f1a4018a22a8d8cacc5d66407f974573c3a0_

```
{"id": "RUSTSEC-2026-0401", "aliases": [], "modified": "2026-10-26T14:00:04.231502512Z", "summary": "Out-of-bounds read in `train_from_buffer` when sample sizes overflow", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (8.2.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-04946 — zstd-safe 7.2.4 затронут RUSTSEC-2026-0402 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/zstd-safe@7.2.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 12:48 UTC
- Балл приоритета: 20.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0402 для пакета crates.io zstd-safe версии 7.2.4: Heap buffer overflow in `CCtx::try_clone` on a multithreaded context. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Проверенный код не упоминает затронутые функции (zstd_safe::CCtx::try_clone); zstd-safe приходит через другие зависимости, которые могут их вызывать.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0402
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0402](https://osv.dev/vulnerability/RUSTSEC-2026-0402) · manifest · SHA-256 1659ee65665b5ae755a87f2715370efa327fc3064514c61888dd4fa3a3f32642_

```
{"id": "RUSTSEC-2026-0402", "aliases": [], "modified": "2026-10-26T14:00:05.685817733Z", "summary": "Heap buffer overflow in `CCtx::try_clone` on a multithreaded context", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (8.2.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-04947 — zstd-safe 7.2.4 затронут RUSTSEC-2026-0403 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/zstd-safe@7.2.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 12:48 UTC
- Балл приоритета: 20.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0403 для пакета crates.io zstd-safe версии 7.2.4: Uninitialized memory exposed when streaming decompression of a legacy frame fails. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Проверенный код не упоминает затронутые функции (zstd_safe::DCtx::decompress_stream); zstd-safe приходит через другие зависимости, которые могут их вызывать.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0403
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0403](https://osv.dev/vulnerability/RUSTSEC-2026-0403) · manifest · SHA-256 b1d1701270f636af5d21f2b55cbd122bcd0df90ce4dce6793aa9263b377caddb_

```
{"id": "RUSTSEC-2026-0403", "aliases": [], "modified": "2026-10-26T14:00:05.787441176Z", "summary": "Uninitialized memory exposed when streaming decompression of a legacy frame fails", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (8.2.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-04948 — zstd-safe 7.2.4 затронут RUSTSEC-2026-0404 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/zstd-safe@7.2.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 12:48 UTC
- Балл приоритета: 20.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0404 для пакета crates.io zstd-safe версии 7.2.4: Double free in `DCtx::try_clone`. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Проверенный код не упоминает затронутые функции (zstd_safe::DCtx::try_clone); zstd-safe приходит через другие зависимости, которые могут их вызывать.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0404
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0404](https://osv.dev/vulnerability/RUSTSEC-2026-0404) · manifest · SHA-256 7c25f3932e55150f3788cd8fcee7738d3c905758f825a562b19f78d7e041b0b2_

```
{"id": "RUSTSEC-2026-0404", "aliases": [], "modified": "2026-10-26T14:00:05.092817237Z", "summary": "Double free in `DCtx::try_clone`", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (8.2.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-04949 — zstd-safe 7.2.4 затронут RUSTSEC-2026-0405 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/zstd-safe@7.2.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 12:48 UTC
- Балл приоритета: 20.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0405 для пакета crates.io zstd-safe версии 7.2.4: Out-of-bounds read with an out-of-range `InBuffer::pos`. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Проверенный код не упоминает затронутые функции (zstd_safe::seekable::SeekableCStream::compress_stream); zstd-safe приходит через другие зависимости, которые могут их вызывать.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0405
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0405](https://osv.dev/vulnerability/RUSTSEC-2026-0405) · manifest · SHA-256 aa7a0dd1f301f7767bcd2d2a354fda77b1e2ed887669efac9bdd2bc66db5be81_

```
{"id": "RUSTSEC-2026-0405", "aliases": [], "modified": "2026-10-26T14:00:05.680942523Z", "summary": "Out-of-bounds read with an out-of-range `InBuffer::pos`", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (8.2.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-04950 — zstd-safe 7.2.4 затронут RUSTSEC-2026-0406 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/zstd-safe@7.2.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 12:48 UTC
- Балл приоритета: 20.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0406 для пакета crates.io zstd-safe версии 7.2.4: Use-after-free when changing a multithreaded context with an unfinished frame. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Проверенный код не упоминает затронутые функции (zstd_safe::CCtx::disable_dictionary, zstd_safe::CCtx::init, zstd_safe::CCtx::load_dictionary, zstd_safe::CCtx::ref_cdict, zstd_safe::CCtx::ref_prefix, zstd_safe::CCtx::reset …); zstd-safe приходит через другие зависимости, которые могут их вызывать.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0406
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0406](https://osv.dev/vulnerability/RUSTSEC-2026-0406) · manifest · SHA-256 deca0b7103bdc0c3ed051bcdb0dbd3d63e215fecdbdba6a7f24f9fb8c2e93ecd_

```
{"id": "RUSTSEC-2026-0406", "aliases": [], "modified": "2026-10-26T14:00:05.095427051Z", "summary": "Use-after-free when changing a multithreaded context with an unfinished frame", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (8.2.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-04951 — zstd-sys 2.0.16+zstd.1.5.7 затронут RUSTSEC-2026-0410 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/zstd-sys@2.0.16+zstd.1.5.7`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 12:48 UTC
- Балл приоритета: 20.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0410 для пакета crates.io zstd-sys версии 2.0.16+zstd.1.5.7: WebAssembly allocator shim corrupts memory on allocation failure. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Бюллетень не называет затронутых функций, поэтому достижимость не определена. Касается только целевых платформ wasm32.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0410
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0410](https://osv.dev/vulnerability/RUSTSEC-2026-0410) · manifest · SHA-256 1e892df4ce7c9911f01547e4a80d1fb3ea5a27b8c1c89c0514917e08bbf3bdc5_

```
{"id": "RUSTSEC-2026-0410", "aliases": [], "modified": "2026-10-26T14:00:05.788985783Z", "summary": "WebAssembly allocator shim corrupts memory on allocation failure", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (2.1.2).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-04952 — 4 бюллетеней в 3 пакет(ах) crates.io, нужных только для разработки или сборки

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependencies:crates.io:non-runtime`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch по точным версиям; область применения — из devDependencies, флагов dev в package-lock.json, разделов importers в pnpm, графа Cargo.lock от таблиц Cargo.toml и — для yarn.lock, который область не записывает вовсе — графа файла блокировки, пройденного от package.json. Если рабочее требование в файле блокировки разрешить не удалось, файл остаётся без классификации, чтобы пакет не был отложен в сторону по ошибке.
- Анализатор: dependencies 1.2.0 · 2026-10-28 12:48 UTC
- Балл приоритета: 15.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает 4 бюллетеней (2 с оценкой high или critical) для 3 пакет(ов) crates.io, которые подтягивают только инструменты разработки или сборки (Cargo.lock): например, pprof@0.13.0 [dev]: GHSA-gw5w-5j7f-jmjj; quick-xml@0.26.0 [dev]: RUSTSEC-2026-0194, RUSTSEC-2026-0195; tokio@1.52.3 [dev]: RUSTSEC-2026-0386. Манифесты помечают их так (devDependencies, "dev": true в package-lock.json, [dev-dependencies]/[build-dependencies] через граф Cargo.lock), поэтому в поставляемый продукт они не входят.

**Возможные последствия.** Пользователей продукта они не затрагивают. Они могут влиять на машины разработчиков и CI (цепочка поставки): скомпрометированный или уязвимый инструмент способен изменить сборку.

**Шаги воспроизведения.**

```
Найдите пакеты из доказательства на https://osv.dev и проверьте их область применения в Cargo.lock.
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev (crates.io)](https://osv.dev/) · Cargo.lock · SHA-256 9d9b06d343ab87c0c3691f419ae25b559874c19803ae3bbe7fd1c99ca4493185_

```
pprof@0.13.0 [dev]: GHSA-gw5w-5j7f-jmjj
quick-xml@0.26.0 [dev]: RUSTSEC-2026-0194, RUSTSEC-2026-0195
tokio@1.52.3 [dev]: RUSTSEC-2026-0386
```

**Ограничения проверки.** Данные получены от OSV.dev в зафиксированное время. Области применения взяты из манифестов; собственные build-зависимости крейтов реестра в Cargo.lock не различимы, поэтому множество runtime может оказаться больше реального, но не меньше.

**Рекомендация.** Обновите инструменты в рамках планового обслуживания; в первую очередь пакеты, которые выполняются в CI с секретами или создают релизные артефакты.

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-04930 — basic-toml 0.1.10: информационный бюллетень RUSTSEC-2026-0374 (unmaintained)

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/basic-toml@0.1.10`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 12:48 UTC
- Балл приоритета: 11.6 / 100
- CVSS v3.1: неприменимо

OSV.dev отмечает RUSTSEC-2026-0374 для пакета crates.io basic-toml версии 0.1.10 как информационный (unmaintained): `basic-toml` is unmaintained. Уязвимости в нём нет; неподдерживаемый пакет не получит исправлений будущих уязвимостей.

**Возможные последствия.** Известной уязвимости нет. Исправления безопасности в будущем могут не выйти.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0374
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0374](https://osv.dev/vulnerability/RUSTSEC-2026-0374) · manifest · SHA-256 5043412c341a3842fb5b4d44f2440bd25fa5620f52d2ed3398ec617b542ae0db_

```
{"id": "RUSTSEC-2026-0374", "aliases": [], "modified": "2026-10-20T11:15:37.076409305Z", "summary": "`basic-toml` is unmaintained", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные получены от OSV.dev в зафиксированное время.

**Рекомендация.** Запланируйте переход на поддерживаемую альтернативу или зафиксируйте решение оставить пакет.

**Повторная проверка.** Повторите сканирование зависимостей после изменения.

### QSI-2026-04933 — proc-macro-error2 2.0.1: информационный бюллетень RUSTSEC-2026-0173 (unmaintained)

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/proc-macro-error2@2.0.1`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 12:48 UTC
- Балл приоритета: 11.6 / 100
- CVSS v3.1: неприменимо

OSV.dev отмечает RUSTSEC-2026-0173 для пакета crates.io proc-macro-error2 версии 2.0.1 как информационный (unmaintained): proc-macro-error2 is unmaintained. Уязвимости в нём нет; неподдерживаемый пакет не получит исправлений будущих уязвимостей.

**Возможные последствия.** Известной уязвимости нет. Исправления безопасности в будущем могут не выйти.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0173
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0173](https://osv.dev/vulnerability/RUSTSEC-2026-0173) · manifest · SHA-256 0ecc182141bd9effc6d35bc24dc20c57e6473fb3877ad59a5fbdb1cd55b56528_

```
{"id": "RUSTSEC-2026-0173", "aliases": [], "modified": "2026-06-07T21:00:04.318567692Z", "summary": "proc-macro-error2 is unmaintained", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные получены от OSV.dev в зафиксированное время.

**Рекомендация.** Запланируйте переход на поддерживаемую альтернативу или зафиксируйте решение оставить пакет.

**Повторная проверка.** Повторите сканирование зависимостей после изменения.


## 8. Постквантовая оценка

| | Обмен ключами (x — сколько данные должны оставаться конфиденциальными; «собери сейчас, расшифруй потом») | Подписи (x — сколько подписи и ключи должны оставаться доверенными) |
|---|---|---|
| Срок жизни данных/ключей x | 10 | 5 |
| Время миграции y | 3 | 3 |
| Принятое число лет до CRQC z | 8 (early) | 8 |
| x + y − z | 5 → при этом сценарии миграция завершится слишком поздно | 0 → запас минимален |
#### Откуда взято z

Усреднённая оценка экспертов, что CRQC появится в пределах горизонта, из ежегодного опроса, который публикует автор этого неравенства. Это оценки вероятности, а не предсказание даты.

| В пределах | Вероятность | Формулировка отчёта |
|---|---|---|
| 5 лет | ~15% | усреднённая оценка |
| 10 лет | 28-49% | вполне возможно |
| 15 лет | 51-70% | вероятно |

**Почему выбран этот сценарий (early, z = 8):** Внутри 10-летнего горизонта, которому опрос даёт 28-49% («вполне возможно»), и согласуется с оценкой BSI в 15 лет, которая «может сократиться до 10 или меньше». Для данных с десятилетиями конфиденциальности, где ошибка дорога.
_Допущения планирования: x для обмена ключами, x для подписей, y — значения по умолчанию профиля риска «Разработчик ПО безопасности», а не данные клиента; с фактическими сроками клиента вывод может измениться._

### Постквантовая зрелость: Уровень 1 из 4 — постквантовый код есть, но не подключён

- Постквантовая библиотека объявлена в зависимостях
- Только классика — обёртка ключей и шифрование хранимых данных: X25519 (3 файл(ов))

**Следующий шаг:** Подключите имеющийся постквантовый примитив к критичному пути (обёртка ключей или канал) в гибридной схеме и проверьте совместимость.

_Уровни: 0 — нет; 1 — есть, но не подключено; 2 — используется вне критичных путей; 3 — гибрид в критичном пути; 4 — постквантовое по умолчанию в критичных путях (корень доверия, обёртка ключей, обмен ключами в канале). Оценка по коду и манифестам._

### Что делают квантово-уязвимые алгоритмы

| Роль | Алгоритмы (файлы) | ID | Первый шаг |
|---|---|---|---|
| **обёртка ключей и шифрование хранимых данных** | X25519 (3) | QSI-2026-04928 | Оборачивайте ключи ML-KEM или гибридным KEM (X25519 + ML-KEM-768) и переоберните хранимые ключи; для данных, которые уже могли скопировать, нужна отдельная оценка |
| **аутентификация и идентификация (сертификаты, токены, аттестация устройств)** | RSA (3) | QSI-2026-04929 | Делайте учётные данные краткоживущими и планируйте сертификаты, токены и ключи ML-DSA по мере поддержки в экосистеме |
| **роль не определена** | X25519 (6) | QSI-2026-04927 | Классифицируйте каждое использование, зафиксируйте сроки жизни данных и запланируйте миграцию на Гибридное установление ключей с ML-KEM (FIPS 203), например X25519MLKEM768 в TLS 1.3 или mlkem768x25519-sha256 в SSH; введите уровень абстракции для криптогибкости |

_Роль определяется по путям файлов, именам функций и коду вокруг совпадений; проверка её подтверждает. Сначала — ключи корня доверия и обёрнутые ключи: их трудно заменить или можно записать уже сегодня._
Анкета готовности для проекта не заполнялась.

### Квантовые алгоритмы, значимые для этой инвентаризации

| Квантовый алгоритм | Действие | Модель атаки | Алгоритмы из инвентаризации (строк) | Что это значит для аудита |
|---|---|---|---|---|
| Алгоритм Шора — факторизация | взламывает | Q1 | RSA (3) | Взламывает RSA при любой длине ключа: более длинный модуль лишь полиномиально повышает стоимость. Планируйте переход на ML-KEM (или гибрид) для установления ключей и ML-DSA / SLH-DSA для подписей; начинайте с ключей, защищающих данные, которые должны оставаться конфиденциальными годами («собери сейчас — расшифруй потом»), и с долгоживущих подписей. |
| Алгоритм Шора — дискретный логарифм на эллиптических кривых | взламывает | Q1 | X25519 (10) | Ключи на эллиптических кривых, по оценкам, падут раньше ключей RSA сопоставимой классической стойкости. В блокчейнах первыми под угрозой монеты, чей открытый ключ уже опубликован (повторно используемые адреса, выходы pay-to-public-key и Taproot); планируйте переход на постквантовые подписи и до этого избегайте повторного использования ключей. |
| Алгоритм Гровера — поиск ключа и прообразов | ослабляет (более длинные ключи восстанавливают запас) | Q1 | AES-256 (1), ChaCha20-Poly1305 (2), HKDF (2), HMAC (4), SHA-2 (6), scrypt (1) | Не взлом. Ключи 256 бит (AES-256, ChaCha20) сохраняют хороший запас; AES-128 соответствует категории 1 NIST, но некоторые регуляторы требуют 256-битных ключей в квантово-устойчивых системах (см. запись AES-128). Для долгоживущих данных предпочитайте 256-битные ключи; 256-битные хеши для стойкости к прообразам менять не нужно. |
| Брассар–Хойер–Тапп — поиск коллизий | ослабляет (более длинные ключи восстанавливают запас) | Q1 | SHA-2 (6) | 256-битные хеши (SHA-256, SHA3-256) остаются достаточными по стойкости к коллизиям; 160-битные хеши слабы уже классически (коллизии SHA-1 практичны). Где нужны категории NIST 4–5, используйте хеши на 384/512 бит. |

_Действие: взламывает — алгоритм нужно заменить; ослабляет — более длинные ключи или выходы восстанавливают запас; учтено в стандартных параметрах — при стандартных наборах действий не требуется; только при суперпозиционных запросах — к обычному применению неприменимо._


## 9. Ограничения и допущения

- Отчёт содержит результаты автоматизированного и документального анализа в указанных границах. Он не является юридическим заключением, сертификацией или подтверждением соответствия какому-либо стандарту.
- z — плановое допущение профиля риска, а не прогноз. Публично известного криптографически значимого квантового компьютера сегодня не существует.

## 10. План устранения проблем / Приоритеты на 30, 60 и 90 дней

### 30 дн.

| Приоритет | ID | Действие | Тип | Условие закрытия |
|---|---|---|---|---|
| P2 | QSI-2026-04937 | Обновите zip до исправленной версии (9.0.0). | устранение первопричины | Сканирование зависимостей больше не сообщает RUSTSEC-2026-0369. |
| P2 | QSI-2026-04935 | Обновите zip до исправленной версии (9.0.0). | устранение первопричины | Сканирование зависимостей больше не сообщает RUSTSEC-2026-0367. |
| P2 | QSI-2026-04934 | Обновите rsa до исправленной версии (пока не выпущена; меры смягчения — в бюллетене). | устранение первопричины | Сканирование зависимостей больше не сообщает RUSTSEC-2023-0071 (CVE-2023-49092). |
### 60 дн.

| Приоритет | ID | Действие | Тип | Условие закрытия |
|---|---|---|---|---|
| P3 | QSI-2026-04931 | Разберите RUSTSEC-2026-0387; при необходимости обновите crypto-bigint до исправленной версии (0.7.6). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0387 или результат разбора записан. |
| P3 | QSI-2026-04932 | Разберите RUSTSEC-2026-0385; при необходимости обновите ctutils до исправленной версии (0.4.4). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0385 или результат разбора записан. |
| P3 | QSI-2026-04936 | Разберите RUSTSEC-2026-0368; при необходимости обновите zip до исправленной версии (9.0.0). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0368 или результат разбора записан. |
| P3 | QSI-2026-04938 | Разберите RUSTSEC-2026-0391; при необходимости обновите zstd до исправленной версии (0.14.3). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0391 или результат разбора записан. |
| P3 | QSI-2026-04939 | Разберите RUSTSEC-2026-0395; при необходимости обновите zstd-safe до исправленной версии (8.2.0). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0395 или результат разбора записан. |
| P3 | QSI-2026-04940 | Разберите RUSTSEC-2026-0396; при необходимости обновите zstd-safe до исправленной версии (8.2.0). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0396 или результат разбора записан. |
| P3 | QSI-2026-04941 | Разберите RUSTSEC-2026-0397; при необходимости обновите zstd-safe до исправленной версии (8.2.0). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0397 или результат разбора записан. |
| P3 | QSI-2026-04942 | Разберите RUSTSEC-2026-0398; при необходимости обновите zstd-safe до исправленной версии (8.2.0). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0398 или результат разбора записан. |
| P3 | QSI-2026-04943 | Разберите RUSTSEC-2026-0399; при необходимости обновите zstd-safe до исправленной версии (8.2.0). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0399 или результат разбора записан. |
| P3 | QSI-2026-04944 | Разберите RUSTSEC-2026-0400; при необходимости обновите zstd-safe до исправленной версии (8.2.0). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0400 или результат разбора записан. |
| P3 | QSI-2026-04945 | Разберите RUSTSEC-2026-0401; при необходимости обновите zstd-safe до исправленной версии (8.2.0). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0401 или результат разбора записан. |
| P3 | QSI-2026-04946 | Разберите RUSTSEC-2026-0402; при необходимости обновите zstd-safe до исправленной версии (8.2.0). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0402 или результат разбора записан. |
| P3 | QSI-2026-04947 | Разберите RUSTSEC-2026-0403; при необходимости обновите zstd-safe до исправленной версии (8.2.0). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0403 или результат разбора записан. |
| P3 | QSI-2026-04948 | Разберите RUSTSEC-2026-0404; при необходимости обновите zstd-safe до исправленной версии (8.2.0). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0404 или результат разбора записан. |
| P3 | QSI-2026-04949 | Разберите RUSTSEC-2026-0405; при необходимости обновите zstd-safe до исправленной версии (8.2.0). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0405 или результат разбора записан. |
| P3 | QSI-2026-04950 | Разберите RUSTSEC-2026-0406; при необходимости обновите zstd-safe до исправленной версии (8.2.0). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0406 или результат разбора записан. |
| P3 | QSI-2026-04951 | Разберите RUSTSEC-2026-0410; при необходимости обновите zstd-sys до исправленной версии (2.1.2). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0410 или результат разбора записан. |
### 90 дн.

| Приоритет | ID | Действие | Тип | Условие закрытия |
|---|---|---|---|---|
| P3 | QSI-2026-04928 | Внесите использования X25519 в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-04927 | Внесите использования X25519 в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-04929 | Внесите использования RSA в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P4 | QSI-2026-04928 | Запланируйте миграцию X25519 на Гибридное установление ключей с ML-KEM (FIPS 203), например X25519MLKEM768 в TLS 1.3 или mlkem768x25519-sha256 в SSH (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование Гибридное установление ключей с ML-KEM (FIPS 203), например X25519MLKEM768 в TLS 1.3 или mlkem768x25519-sha256 в SSH или гибридной схемы. |
| P4 | QSI-2026-04927 | Запланируйте миграцию X25519 на Гибридное установление ключей с ML-KEM (FIPS 203), например X25519MLKEM768 в TLS 1.3 или mlkem768x25519-sha256 в SSH (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование Гибридное установление ключей с ML-KEM (FIPS 203), например X25519MLKEM768 в TLS 1.3 или mlkem768x25519-sha256 в SSH или гибридной схемы. |
| P4 | QSI-2026-04929 | Запланируйте миграцию RSA на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема или гибридной схемы. |
| P4 | QSI-2026-04952 | Обновите зависимости разработки и сборки из доказательства. | устранение первопричины | Сканирование не сообщает бюллетеней для пакетов инструментов, либо оставшиеся зафиксированы. |
| P4 | QSI-2026-04930 | Замените basic-toml поддерживаемой альтернативой или зафиксируйте, почему он остаётся. | устранение первопричины | basic-toml заменён или решение зафиксировано. |
| P4 | QSI-2026-04933 | Замените proc-macro-error2 поддерживаемой альтернативой или зафиксируйте, почему он остаётся. | устранение первопричины | proc-macro-error2 заменён или решение зафиксировано. |

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

1. A. Chailloux, M. Naya-Plasencia, A. Schrottenloher — An Efficient Quantum Collision Search Algorithm and Implications on Symmetric Cryptography (ASIACRYPT 2017; IACR ePrint 2017/847) — IACR ePrint. <https://eprint.iacr.org/2017/847> (peer-reviewed article: Õ(2^{2n/5}) time, O(n) qubits, Õ(2^{n/5}) classical memory)
2. C. Chevignard, P.-A. Fouque, A. Schrottenloher — Reducing the Number of Qubits in Quantum Discrete Logarithms on Elliptic Curves (IACR ePrint 2026/280) — IACR ePrint. <https://eprint.iacr.org/2026/280> (revision of a EUROCRYPT 2026 paper: 3.12n + o(n) qubits; for n = 256, 1193 qubits and 22 runs of 2^38.98 Toffoli gates)
3. C. Gidney — How to factor 2048 bit RSA integers with less than a million noisy qubits (arXiv:2505.15917) — arXiv. <https://arxiv.org/abs/2505.15917> (preprint (2025-05-21): < 1 million noisy qubits, < 1 week, 0.1% gate error, 1 µs surface-code cycle)
4. C. Gidney, M. Ekerå — How to factor 2048 bit RSA integers in 8 hours using 20 million noisy qubits (Quantum 5, 433) — Quantum. <https://doi.org/10.22331/q-2021-04-15-433> (peer-reviewed article (2021): 10^-3 gate error, 1 µs cycle, 10 µs reaction time)
5. C. Zalka — Grover's quantum searching algorithm is optimal (Phys. Rev. A 60, 2746, 1999; arXiv:quant-ph/9711070) — APS. <https://doi.org/10.1103/PhysRevA.60.2746> (peer-reviewed article: optimal for any success probability; parallel search gains no more than splitting the space)
6. Common Vulnerability Scoring System v3.1: Specification Document — FIRST. <https://www.first.org/cvss/v3.1/specification-document> (final)
7. D. J. Bernstein — Cost analysis of hash collisions: Will quantum computers make SHARCS obsolete? (2009) — cr.yp.to. <https://cr.yp.to/hash/collisioncost-20090823.pdf> (paper dated 2009-08-23)
8. D. Litinski — How to compute a 256-bit elliptic curve private key with only 50 million Toffoli gates (arXiv:2306.08585) — arXiv. <https://arxiv.org/abs/2306.08585> (preprint (2023-06-14): 6000 modules × 1152 physical qubits, one key per 10 minutes under its architecture assumptions)
9. FIPS 203 — Module-Lattice-Based Key-Encapsulation Mechanism Standard (ML-KEM) — NIST. <https://csrc.nist.gov/pubs/fips/203/final> (final (August 2024))
10. FIPS 204 — Module-Lattice-Based Digital Signature Standard (ML-DSA) — NIST. <https://csrc.nist.gov/pubs/fips/204/final> (final (August 2024))
11. FIPS 205 — Stateless Hash-Based Digital Signature Standard (SLH-DSA) — NIST. <https://csrc.nist.gov/pubs/fips/205/final> (final (August 2024))
12. G. Brassard, P. Høyer, A. Tapp — Quantum Algorithm for the Collision Problem (LATIN '98; arXiv:quant-ph/9705002) — Springer / arXiv. <https://arxiv.org/abs/quant-ph/9705002> (peer-reviewed article: collisions of r-to-one functions in O((N/r)^{1/3}) expected evaluations)
13. J. Proos, C. Zalka — Shor's discrete logarithm quantum algorithm for elliptic curves (Quantum Inf. Comput. 3(4), 2003; arXiv:quant-ph/0301141) — Quantum Information & Computation. <https://doi.org/10.26421/QIC3.4-3> (peer-reviewed article)
14. L. K. Grover — A fast quantum mechanical algorithm for database search (STOC 1996) — ACM. <https://doi.org/10.1145/237814.237866> (peer-reviewed article)
15. M. Amy et al. — Estimating the cost of generic quantum pre-image attacks on SHA-2 and SHA-3 (SAC 2016; arXiv:1603.09383) — Springer / arXiv. <https://arxiv.org/abs/1603.09383> (peer-reviewed article: SHA-256 about 2^153.8 surface-code cycles on 2^12.6 logical qubits; SHA3-256 about 2^146.5 cycles on 2^20)
16. M. Cain et al. — Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits (arXiv:2603.28627) — arXiv. <https://arxiv.org/abs/2603.28627> (preprint (2026-03-30): P-256 in a few days with 26,000 physical neutral-atom qubits; RSA-2048 one to two orders of magnitude longer)
17. M. Mosca — Cybersecurity in an Era with Quantum Computers: Will We Be Ready? (IEEE Security & Privacy, 2018) — IEEE. <https://doi.org/10.1109/MSP.2018.3761723> (peer-reviewed article; source of the x + y > z migration inequality)
18. M. Roetteler, M. Naehrig, K. Svore, K. Lauter — Quantum resource estimates for computing elliptic curve discrete logarithms (ASIACRYPT 2017) — IACR / arXiv. <https://arxiv.org/abs/1706.06752> (peer-reviewed article: at most 9n + 2⌈log2 n⌉ + 10 qubits and 448 n^3 log2 n + 4090 n^3 Toffoli gates)
19. NIST IR 8547 — Transition to Post-Quantum Cryptography Standards — NIST. <https://csrc.nist.gov/pubs/ir/8547/ipd> (initial public draft (November 2024); proposes deprecating quantum-vulnerable public-key algorithms after 2030 and disallowing them after 2035 — dates may change in the final version)
20. NIST — Post-Quantum Cryptography Standardization: Evaluation Criteria, Security (Call for Proposals, Section 4.A.5) — NIST. <https://csrc.nist.gov/Projects/Post-Quantum-Cryptography/Post-Quantum-Cryptography-Standardization/Evaluation-Criteria/Security-(Evaluation-Criteria)> (security categories: AES-128 key search 2^170/MAXDEPTH quantum gates, AES-192 2^233/MAXDEPTH, AES-256 2^298/MAXDEPTH; MAXDEPTH 2^40–2^96)
21. OSV advisory RUSTSEC-2023-0071 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2023-0071> (modified 2026-09-14T09:45:02.996132556Z)
22. OSV advisory RUSTSEC-2026-0173 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0173> (modified 2026-06-07T21:00:04.318567692Z)
23. OSV advisory RUSTSEC-2026-0367 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0367> (modified 2026-10-16T23:30:02.392172556Z)
24. OSV advisory RUSTSEC-2026-0368 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0368> (modified 2026-10-16T23:30:02.383750571Z)
25. OSV advisory RUSTSEC-2026-0369 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0369> (modified 2026-10-16T23:30:02.387698467Z)
26. OSV advisory RUSTSEC-2026-0374 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0374> (modified 2026-10-20T11:15:37.076409305Z)
27. OSV advisory RUSTSEC-2026-0385 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0385> (modified 2026-10-23T08:30:02.389575143Z)
28. OSV advisory RUSTSEC-2026-0387 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0387> (modified 2026-10-24T03:45:02.365137418Z)
29. OSV advisory RUSTSEC-2026-0391 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0391> (modified 2026-10-26T14:00:04.269245609Z)
30. OSV advisory RUSTSEC-2026-0395 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0395> (modified 2026-10-26T14:00:06.388344282Z)
31. OSV advisory RUSTSEC-2026-0396 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0396> (modified 2026-10-26T14:00:05.789682118Z)
32. OSV advisory RUSTSEC-2026-0397 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0397> (modified 2026-10-26T14:00:05.089587004Z)
33. OSV advisory RUSTSEC-2026-0398 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0398> (modified 2026-10-26T14:00:05.092082939Z)
34. OSV advisory RUSTSEC-2026-0399 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0399> (modified 2026-10-26T14:00:05.792431051Z)
35. OSV advisory RUSTSEC-2026-0400 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0400> (modified 2026-10-26T14:00:05.692077560Z)
36. OSV advisory RUSTSEC-2026-0401 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0401> (modified 2026-10-26T14:00:04.231502512Z)
37. OSV advisory RUSTSEC-2026-0402 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0402> (modified 2026-10-26T14:00:05.685817733Z)
38. OSV advisory RUSTSEC-2026-0403 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0403> (modified 2026-10-26T14:00:05.787441176Z)
39. OSV advisory RUSTSEC-2026-0404 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0404> (modified 2026-10-26T14:00:05.092817237Z)
40. OSV advisory RUSTSEC-2026-0405 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0405> (modified 2026-10-26T14:00:05.680942523Z)
41. OSV advisory RUSTSEC-2026-0406 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0406> (modified 2026-10-26T14:00:05.095427051Z)
42. OSV advisory RUSTSEC-2026-0410 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0410> (modified 2026-10-26T14:00:05.788985783Z)
43. OSV.dev — open-source vulnerability database and API — Open Source Security Foundation. <https://osv.dev/> (the database QSI queries for each exactly pinned version; every advisory id in a finding resolves at https://osv.dev/vulnerability/<id>)
44. P. W. Shor — Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms on a Quantum Computer (SIAM J. Comput., 1997) — SIAM. <https://doi.org/10.1137/S0097539795293172> (peer-reviewed article)
45. R. Babbush et al. — Securing Elliptic Curve Cryptocurrencies against Quantum Vulnerabilities: Resource Estimates and Mitigations (arXiv:2603.28846) — arXiv. <https://arxiv.org/abs/2603.28846> (preprint (2026-03-30, v2 2026-04-15): 256-bit ECDLP with < 1200 logical qubits and < 90 M Toffoli gates (or < 1450 and < 70 M); < 500,000 physical qubits at 10^-3 error, minutes)
46. S. Jaques, M. Naehrig, M. Roetteler, F. Virdia — Implementing Grover oracles for quantum key search on AES and LowMC (EUROCRYPT 2020; arXiv:1910.01700) — Springer / arXiv. <https://arxiv.org/abs/1910.01700> (peer-reviewed article: lower cost estimates for the AES key searches that define the NIST categories)

## Приложения: Криптографическая инвентаризация

| Алгоритм | Параметр | Библиотека | Квантовый статус | Классический статус | Количество | Мест | Примеры |
|---|---|---|---|---|---|---|---|
| AES-256 | AES-256 |  | сниженный запас (Гровер), одобрен | допустимо | 1 | 1 | age/src/ssh.rs:11 |
| ChaCha20-Poly1305 | ChaCha20-Poly1305 |  | сниженный запас (Гровер), одобрен | допустимо | 2 | 2 | age-core/src/primitives.rs:7; age/src/primitives/stream.rs:5 |
| HKDF |  |  | сниженный запас (Гровер), одобрен | допустимо | 2 | 2 | age-core/src/primitives.rs:10; age/src/native.rs:3 |
| HMAC |  |  | сниженный запас (Гровер), одобрен | допустимо | 4 | 4 | age/src/error.rs:422; age/src/format.rs:10; age/src/keys.rs:13 |
| SHA-2 | SHA-512 |  | сниженный запас (Гровер), одобрен | допустимо | 1 | 1 | age/src/ssh/identity.rs:114 |
| scrypt |  |  | сниженный запас (Гровер), одобрен | допустимо | 1 | 1 | age/src/native/scrypt.rs |
| SHA-2 | SHA-256 |  | Гровер: допустимо по NIST, ниже рекомендаций ECCG/ANSSI | допустимо | 5 | 5 | age-core/src/primitives.rs:11; age/src/native.rs:12; age/src/primitives.rs:9 |
| Crypto library | 0.10.0-rc.18 | rsa (RustCrypto rsa) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.14.0 | p384 (RustCrypto elliptic curves) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.14.0 | p256 (RustCrypto elliptic curves) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 3.0.0 | x25519-dalek (ed25519-dalek) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 5.0.0 | curve25519-dalek (ed25519-dalek) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.14 | p256 (RustCrypto elliptic curves) | н/п | допустимо | 1 | 1 | Cargo.toml |
| Crypto library | 3 | x25519-dalek (ed25519-dalek) | н/п | допустимо | 1 | 1 | Cargo.toml |
| Crypto library | 5 | curve25519-dalek (ed25519-dalek) | н/п | допустимо | 1 | 1 | age/Cargo.toml |
| Crypto library | =0.10.0-rc.18 | rsa (RustCrypto rsa) | н/п | допустимо | 1 | 1 | age/Cargo.toml |
| Crypto library | workspace | x25519-dalek (ed25519-dalek) | н/п | допустимо | 1 | 1 | age/Cargo.toml |
| Crypto library | workspace | p256 (RustCrypto elliptic curves) | н/п | допустимо | 1 | 1 | age/Cargo.toml |
| PQC library | 0.3.2 | ml-kem (RustCrypto post-quantum crates) | постквантовый | допустимо | 1 | 1 | Cargo.lock |
| PQC library | 0.3 | ml-kem (RustCrypto post-quantum crates) | постквантовый | допустимо | 1 | 1 | Cargo.toml |
| PQC library | workspace | ml-kem (RustCrypto post-quantum crates) | постквантовый | допустимо | 1 | 1 | age/Cargo.toml |
| RSA |  |  | уязвим (Шор) | допустимо | 3 | 3 | age/src/ssh.rs:346; age/src/ssh/identity.rs:38; age/src/ssh/recipient.rs:42 |
| X25519 | X25519 |  | уязвим (Шор) | допустимо | 10 | 10 | age/src/cli_common/recipients.rs:5; age/src/identity.rs:10; age/src/lib.rs:259 |

_Длинные списки здесь сгруппированы; полный список по файлам — в JSON-версии отчёта, подписанной тем же ключом._

## Приложения: Входные файлы

| Файл | Размер | SHA-256 | Маскирования |
|---|---|---|---|
| Cargo.lock | 92546 | `b0a8b4ae058e50916e3361dc6cd03096b85e2d674bfa4c38605ff9cf4fa8b2b4` | 0 |
| Cargo.toml | 1878 | `14f9f3586ef4fc0472b2febc8fd6e7a83a9b873111603dfac91fc5db82a526b9` | 0 |
| age/Cargo.toml | 3823 | `f59a2e0ae1fefb72ea8c2ce2f8ef0ba0c454bbe44623f8fa3fed83be98351eae` | 0 |
| age/src/cli_common/error.rs | 4175 | `0e0fbf78aa6e463d95d48cfff7681e00e02416629b50296a26d7652bfde0714b` | 0 |
| age/src/cli_common/file_io.rs | 14652 | `bbaca202b0e53c06383044fae0b9a77b9ba25b2d083ee4909316dec7fa7fe935` | 0 |
| age/src/cli_common/identities.rs | 10491 | `c44e9d10994a1dc367b297bd383b5dd16c9cbc70381a0ed8ad68590cec6ec4eb` | 0 |
| age/src/cli_common/recipients.rs | 7460 | `af2b6d7dd5958b91e56c35ddb3df73b9bde23b5cab9118e4d2ab719816d8bcee` | 0 |
| age/src/cli_common.rs | 7061 | `57342ad0f1c66c229e3f1a5d6a4cc912a2f03a2555fb7adb928587512dc94abf` | 0 |
| age/src/encrypted.rs | 12851 | `5ef85a2adcd03fe152ffd63b2ff54b1cbbf695b5f40bb408fbff5eceb0c11511` | 0 |
| age/src/error.rs | 14929 | `c9d995dd74c0f006880db674ca7614effe7c6478d9c535c84c96ed975f95e34e` | 0 |
| age/src/format.rs | 15406 | `7ec7c540d75c971a42d92bb792b6fd063936da1e0565fb990afe58a3110e92cc` | 0 |
| age/src/i18n.rs | 3126 | `222a9dc2b20353f0abdea7c027ca37dc43181828fc243c19abff13c75b49f50b` | 0 |
| age/src/identity.rs | 13125 | `8be708188c5e0f9efa1f3aca44a943060147a23b4ced3a32d4d716d588fbbf02` | 0 |
| age/src/keys.rs | 1060 | `8f85881ed09cdb112f63d1898ba73b03f2168628219071cda9ce45509723e9ca` | 0 |
| age/src/lib.rs | 16555 | `fa1f17a56d7ac3ff7b8ccc2472aa21f261d0c2ea53946498e9537e0ab6a074dc` | 0 |
| age/src/native/scrypt.rs | 9832 | `318f9280dccc2b6cb37476e61d2794ae0872c52d0d0f3169c3f8aa7a62585fee` | 0 |
| age/src/native/tag.rs | 4011 | `3770810dd6b1cadaef1ec7170a0a93a6acf4ddf0822c4ac832b60f8682ae54d0` | 0 |
| age/src/native/tagpq.rs | 5547 | `9d90ce9be62eac475d5b5aac4a7942f14dcd98d89324412b87f00ecd590e5c1e` | 0 |
| age/src/native/x25519.rs | 9769 | `16e457867be81be4d998264e8cc9695b7a95660865e758a79e3501100846f9f5` | 0 |
| age/src/native.rs | 586 | `881b02385f188b684cc7f08f33984810dcad7fc318d3f5a8ab6d7439b516e0b5` | 0 |
| age/src/plugin.rs | 30248 | `818aa0e8547da106758d5ffe6340f4beee2e3d6a5378ae45bce693673956874b` | 0 |
| age/src/primitives/armor.rs | 56516 | `7f15ff4e83b42db3115660699b876cc4f0f2f72ebfd5922a724ba9c431e8d144` | 0 |
| age/src/primitives/stream.rs | 37309 | `36adc28b386b2ac2da32a05ba5734c2bda79f78ea02bb4cc4769ef82cb938160` | 0 |
| age/src/primitives.rs | 1946 | `6021de5b7a9d4e2981acb8e407fe47ffad0ae9743e66e1f9677304a98b3b7602` | 0 |
| age/src/protocol.rs | 20760 | `0a12690ac6a62e378fbdfd1a39a719652281ecd459976e86ed3254113bdb19c9` | 0 |
| age/src/simple.rs | 3711 | `2fe61c492a99c6ae005827f94e2427e39ba790a4a0a441e6cd4e9e0119fce39b` | 0 |
| age/src/ssh/identity.rs | 17051 | `9c359ba9b72af1c5dfee9cd33998b397b37f613d95ca4ba9fa9837d8f7d37fb7` | 10 |
| age/src/ssh/recipient.rs | 11869 | `4dfb6714f29babd5be9d0a876e33a7edbecd8d978fe2c7111a4fcb7ad91cb339` | 0 |
| age/src/ssh.rs | 21595 | `2dd1be76df20f7ed8cf9ae837709b179ceae4440f9ccc3413ff28446cbab1b1e` | 0 |
| age/src/util.rs | 7382 | `3fc97ed2e41fc66a500f1b6dfe735067b4571849c50c62b750133fc16f0a426d` | 0 |
| age-core/Cargo.toml | 1136 | `2b0085aa074e4bf57df14804cc8084cb8e954221e139831007fa3172e8656555` | 0 |
| age-core/src/format.rs | 23539 | `23243cfcee402c9ef98a48d379820e5e48f692fd7b3fb94258af8966cf6794fc` | 0 |
| age-core/src/io.rs | 1837 | `9b1f2abc58869ba97570a9872dac1290a516f6973a4ed35d5fb9cae81f1e1a16` | 0 |
| age-core/src/lib.rs | 637 | `ba12bc5f109d8ac6c02ebb600b7be1eceae0db0079dfa0ef2e4a42e36f1cfd0b` | 0 |
| age-core/src/plugin.rs | 16638 | `4b4b0044cb00768d06b44c2c3d33c3e83ec10d4f785a1bf544ff2cac620e3d36` | 0 |
| age-core/src/primitives.rs | 7708 | `da24f571051d8402bae0ac831ef063c109495d51f413e39c1f747145204f22c8` | 0 |
| age-plugin/Cargo.toml | 714 | `3bce93b36f895d38b176e99bb79db1136afb1e875cae05b7b0d79d63408a19d9` | 0 |
| age-plugin/src/identity.rs | 13232 | `ff6fcfb2a197252884fbde58122d7db683b12d15e4d8361caa202dbd9ac04646` | 0 |
| age-plugin/src/lib.rs | 13527 | `ffb47c8a11de7f4a16a6ee98a18e51b3367b0ccba7be4a7c3aa29baae67613d9` | 0 |
| age-plugin/src/recipient.rs | 18380 | `a54a5f3b568061b727e18357ed58092a9a8719eb27edad5416abd1c1d1914e4b` | 0 |
| rage/Cargo.toml | 7242 | `6a60cee957389d26a3e1857c8744d7cb9767308907c387218af57df01fe086ca` | 0 |
| rage/build.rs | 18663 | `55db85f9f5e07cdc650b647e80f184bde2536567f61eb1c6dccdae7ac8475def` | 0 |
| rage/src/bin/rage/cli.rs | 4975 | `6512b6393befa588a4ebb6d2bc74fe4d8b529856e5ce10fcac9bf7fc952bfebd` | 0 |
| rage/src/bin/rage/error.rs | 7870 | `48202c62c13a2872db57406bcd5655a64993a7147433dc30b3bc8c38ec4a27aa` | 0 |
| rage/src/bin/rage/i18n.rs | 1153 | `58c49a58536dfb4a774c2460f1b1cee59a26e25a02748466a79e65361e684168` | 0 |
| rage/src/bin/rage/main.rs | 13463 | `a9b47927305d861144d27350c4c6326f80f8b2349299ae2dd49d22561c83cf34` | 0 |
| rage/src/bin/rage-keygen/cli.rs | 1406 | `57c88bf1a56945d3253fa3375c792310dcbb50212a60f9a88fb27b4d06a06b99` | 0 |
| rage/src/bin/rage-keygen/error.rs | 1664 | `9739f49266273caf85e9706d83a9233f5dd1bf7259a1a4b8b6d6318870756c1c` | 0 |
| rage/src/bin/rage-keygen/main.rs | 2261 | `88b956d279fb1ab6d05dd77e531e784c0cfee0a2544dc8a8779e8cdc10a9e9e4` | 0 |
| rage/src/bin/rage-mount/cli.rs | 1874 | `ed1a1231968858b07589b5d1c45100ae5c689bad471f2787743bf2d59f385f91` | 0 |
| rage/src/bin/rage-mount/main.rs | 6869 | `9960e58d911a32de66fc88a275f01eeaf508c166dec75c37efc89ac8e5781e99` | 0 |
| rage/src/bin/rage-mount/tar.rs | 8807 | `20f0abc60f10761781bf63d1d4bb37ee8cacfc3ae6e84adbfc351a8a34323581` | 0 |
| rage/src/bin/rage-mount/zip.rs | 8504 | `c75a37ae0dcd036a61de13cf7055988ca48a70fe862a00401a958c5fce6ef449` | 0 |
| rust-toolchain.toml | 66 | `7235c5519f78c24d56b8af9e5cf7c37732e67935f6898a091a8df47ca370a2a1` | 0 |
