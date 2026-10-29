# Отчёт об аудите безопасности и постквантовой готовности

**Проект:** bitwarden-sdk @ 25b6c8c3860a · Bitwarden — публичный репозиторий (пассивная проверка)
| | |
|---|---|
| Организация | QSI |
| Дата отчёта | 2026-10-28 18:19 UTC |
| Версия отчёта | 1 |
| Запуск аудита | 3299dddc-14ef-48e1-91a2-a864b03ce4d0 (Документальный аудит) |
| Версия анализатора | qsi-engine 1.2.0 |
| Профиль риска | Разработчик ПО безопасности |
| SHA-256 содержимого | `1e4739b3d4d55d63452098b66dfb2f91cf88d4f8816147acca500b5289e09586` |
| Ключ подписи (Ed25519, отпечаток SHA-256; подпись — отдельный файл report.sig.json) | `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e` |
> Отчёт содержит результаты автоматизированного и документального анализа в указанных границах. Он не является юридическим заключением, сертификацией или подтверждением соответствия какому-либо стандарту.

## 1. Резюме для руководства

- Критическая: **0**
- Высокая: **0**
- Средняя: **7**
- Низкая: **11**
- Информационная: **11**

- Подтверждённая техническая уязвимость: 0
- Известная уязвимая версия компонента: 13
- Подтверждённая ошибка конфигурации: 0
- Потенциальный криптографический риск: 0
- Долгосрочный постквантовый риск: 7
- Рекомендация по улучшению: 9
- Недостаточность данных: 0

Неравенство Моски (x + y > z): x = 10, y = 3, z = 8 → при этом сценарии миграция завершится слишком поздно. _z — плановое допущение профиля риска, а не прогноз. Публично известного криптографически значимого квантового компьютера сегодня не существует._

**Постквантовая зрелость: Уровень 2 из 4 — постквантовое используется вне критичных путей.** Следующий шаг: Распространите постквантовую защиту на критичные роли, которые остаются классическими, начиная с того, что можно записать уже сегодня (обёрнутые ключи, обмен ключами в канале).

## 2. Область и границы проверки

Режим: Документальный аудит

Репозиторий: <https://github.com/bitwarden/sdk-internal> @ `25b6c8c3860af5165ac1428c4c825ede7caa55de` — ссылки в доказательствах открывают строки на этом коммите.

1625 файлов, всего 8532057 байт, редактирований: 131; список SHA-256 по файлам — в приложении C.

## 3. Методология

| Область | Статус | Количество | Примеры |
|---|---|---|---|
| dependencies | проверено | 66 | Cargo.lock: 661 dependencies parsed (661 pinned); Cargo.toml: 115 dependencies parsed (61 pinned); crates/bitwarden-access-token/Cargo.toml: 6 dependencies parsed (0 pinned) |
| source_code | проверено | 1558 | crates/bitwarden-access-token/src/consts.rs: 4 lines scanned with 16 rule patterns and 122 registry patterns; crates/bitwarden-access-token/src/kind.rs: 64 lines scanned with 16 rule patterns and 122 registry patterns; 32 lines in #[cfg(test)] modules ignored; crates/bitwarden-access-token/src/lib.rs: 13 lines scanned with 16 rule patterns and 122 registry patterns |
| tls_code | проверено | 3 | crates/bitwarden-api-base/src/client.rs: TLS key-exchange settings read; crates/bitwarden-uniffi/kotlin/sdk/build.gradle: TLS key-exchange settings read; crates/bitwarden-uniffi/src/android_support.rs: TLS key-exchange settings read |
| secrets | проверено | 55 | crates/bitwarden-auth/src/login/api/request/login_api_request.rs: value(s) at line(s) 118 (mock_fields), 160 (mock_fields), 180 (mock_fields), 273 (mock_fields), 311 (mock_fields), 351 (mock_fields) are declared inside a fixture and treated as test data, although the file itself is not test code; crates/bitwarden-auth/src/login/api/request/login_api_request.rs: 7 redacted value(s) not reported (comments, test modules, fixture declarations, placeholders, values the source annotates as published, or hex values not bound to a secret name); crates/bitwarden-auth/src/login/api/send_login_request.rs: value(s) at line(s) 132 (MockLoginFields) are declared inside a fixture and treated as test data, although the file itself is not test code |
| keys | проверено | 9 | crates/bitwarden-crypto/src/enc_string/asymmetric.rs: private key block at line 335 is test data (test code); crates/bitwarden-crypto/src/keys/public_key_encryption.rs: private key block at line 347 is test data (test code); crates/bitwarden-exporters/src/cxf/ssh.rs: private key block at line 116 is test data (test code) |
| certificates_and_keys | проверено | 8 | crates/bitwarden-crypto/src/enc_string/asymmetric.rs: certificates/keys parsed; crates/bitwarden-crypto/src/keys/public_key_encryption.rs: certificates/keys parsed; crates/bitwarden-exporters/src/cxf/ssh.rs: certificates/keys parsed |
| osv_advisories | проверено | 1 | 903 pinned packages queried at OSV.dev; 23 affected (5 of them only in development or build dependencies) |

_Длинные списки здесь сгруппированы; полный список по файлам — в JSON-версии отчёта, подписанной тем же ключом._

## 4. Проверенные и непроверенные активы

- Нет

## 5. Краткое описание архитектуры

Static review of the source tree bitwarden-sdk at 25b6c8c3860af5165ac1428c4c825ede7caa55de. 1625 files analysed; of 2037 files, 255 are test, fuzzing, benchmark or example code and were left out, 157 are not read by any analyzer, 0 exceed the per-file limit and 0 did not fit the total limit. No requests were sent to the owner's systems.

## 6. Общая оценка состояния безопасности

- Ориентировочный индекс состояния: **77** / 100 — _Рассчитан по находкам в области проверки (подтверждённые и потенциальные проблемы, взвешенные по серьёзности). Ориентировочный; не сравним между аудитами с разной областью._
- Доля квантово-уязвимых элементов инвентаризации: 10.1%

## 7. Подробное описание находок

### QSI-2026-05805 — rsa 0.10.0-rc.18 затронут RUSTSEC-2023-0071 (CVE-2023-49092)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:crates.io/rsa@0.10.0-rc.18`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:19 UTC
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

### QSI-2026-05806 — rustls 0.23.45 затронут GHSA-c8m5-c952-6cm4 (RUSTSEC-2026-0346)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:crates.io/rustls@0.23.45`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:19 UTC
- Балл приоритета: 44.3 / 100
- CVSS v3.1: 4.0 (`CVSS:3.1/AV:L/AC:H/PR:H/UI:R/S:U/C:H/I:N/A:N`)

OSV.dev сообщает GHSA-c8m5-c952-6cm4 (RUSTSEC-2026-0346) для пакета crates.io rustls версии 0.23.45: Rustls: Session Debug formatting exposes TLS master secrets and resumption PSKs. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-c8m5-c952-6cm4
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-c8m5-c952-6cm4](https://osv.dev/vulnerability/GHSA-c8m5-c952-6cm4) · manifest · SHA-256 b8f49a7948da20f17a5b61070e9e354a2a3e38b5743f8f41c9b2f3d2a264b002_

```
{"id": "GHSA-c8m5-c952-6cm4", "aliases": ["RUSTSEC-2026-0346"], "modified": "2026-10-27T16:15:05.354395696Z", "summary": "Rustls: Session Debug formatting exposes TLS master secrets and resumption PSKs", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:L/AC:H/PR:H/UI:R/S:U/C:H/I:N/A:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.23.46, 0.24.0-dev.2).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05789 — TLS без постквантового обмена ключами: rustls с криптопровайдером ring

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `tls-code:rustls`
- Источник данных: Cargo.toml
- Метод обнаружения: Статическое чтение настроек TLS-библиотек в коде и манифестах: криптопровайдер, списки групп и кривых, GODEBUG.
- Анализатор: tls_code 1.2.0 · 2026-10-28 18:19 UTC
- Балл приоритета: 38.1 / 100
- CVSS v3.1: неприменимо

rustls с криптопровайдером ring в Cargo.toml:127: настроенный обмен ключами (ring) не содержит гибридной группы ML-KEM, например X25519MLKEM768 (RFC 10024), поэтому рукопожатие не может её согласовать.

**Возможные последствия.** Трафик, защищённый только классическим ECDHE, может быть записан сегодня и расшифрован после появления CRQC (harvest now, decrypt later). Актуально, если данные должны оставаться конфиденциальными много лет.

**Шаги воспроизведения.**

```
Откройте Cargo.toml:127 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [Cargo.toml](https://github.com/bitwarden/sdk-internal/blob/25b6c8c3860af5165ac1428c4c825ede7caa55de/Cargo.toml#L127) · line 127 · SHA-256 0880f8fd37df57f72244f0fa3a7f0c77b4542c1f60c22fdd9396885476c444e5_

```
  126 | rsa = "0.10.0-rc.17"
  127 | rustls = { version = "0.23.27", default-features = false, features = [
  128 |     "std",
```

_file_excerpt · [crates/bitwarden-api-base/src/client.rs](https://github.com/bitwarden/sdk-internal/blob/25b6c8c3860af5165ac1428c4c825ede7caa55de/crates/bitwarden-api-base/src/client.rs#L17) · line 17 · SHA-256 1ba9e054cc665efd719a831cebc60ff479fbdaf919561845d3735d82f1d5a805_

```
   16 |     {
   17 |         let _ = rustls::crypto::ring::default_provider().install_default();
   18 | 
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Прочитаны только код и манифесты: развёрнутые версии библиотек и настройки вне кода (окружение, флаги запуска) не определялись.

**Рекомендация.** Соберите rustls с провайдером aws-lc-rs (rustls::crypto::aws_lc_rs) и функцией prefer-post-quantum, которая ставит X25519MLKEM768 первым.

**Повторная проверка.** Подключитесь клиентом, предлагающим X25519MLKEM768 (openssl s_client -groups X25519MLKEM768 с OpenSSL 3.5+ или клиент на Go 1.24+), и проверьте согласованную группу.

### QSI-2026-05790 — Квантово-уязвимый RSA: обёртка ключей и шифрование хранимых данных (3 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `source-code:RSA:key_wrapping`
- Источник данных: crates/bitwarden-crypto/src/enc_string/asymmetric.rs
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-28 18:19 UTC
- Балл приоритета: 38.0 / 100
- CVSS v3.1: неприменимо

6 упоминаний RSA в 3 файл(ах), например crates/bitwarden-crypto/src/enc_string/asymmetric.rs:5. Роль по путям, именам функций и соседнему коду: обёртка ключей и шифрование хранимых данных. Ключи или данные, зашифрованные на эти открытые ключи, хранятся: кто скопирует их сейчас, расшифрует, когда появится CRQC («собери сейчас — расшифруй потом»).

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте crates/bitwarden-crypto/src/enc_string/asymmetric.rs:5 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [crates/bitwarden-crypto/src/enc_string/asymmetric.rs](https://github.com/bitwarden/sdk-internal/blob/25b6c8c3860af5165ac1428c4c825ede7caa55de/crates/bitwarden-crypto/src/enc_string/asymmetric.rs#L5) · line 5 · SHA-256 0899ffe94bf3265999761475ac346ac703206b9a0e23a9334294c023605431a8_

```
    4 | pub use internal::UnsignedSharedKey;
    5 | use rsa::Oaep;
    6 | use serde::Deserialize;
```

_file_excerpt · [crates/bitwarden-crypto/src/keys/public_key_encryption.rs](https://github.com/bitwarden/sdk-internal/blob/25b6c8c3860af5165ac1428c4c825ede7caa55de/crates/bitwarden-crypto/src/keys/public_key_encryption.rs#L92) · line 92 · SHA-256 76e238cd7a05acc62562de93770ef1b85d5282970c95c32797ffc60f5e8ab22f_

```
   91 |             inner: RawPublicKey::RsaOaepSha1(
   92 |                 RsaPublicKey::from_public_key_der(der.as_ref())
   93 |                     .map_err(|_| CryptoError::InvalidKey)?,
```

_file_excerpt · [crates/bitwarden-crypto/src/keys/public_key_encryption.rs](https://github.com/bitwarden/sdk-internal/blob/25b6c8c3860af5165ac1428c4c825ede7caa55de/crates/bitwarden-crypto/src/keys/public_key_encryption.rs#L213) · line 213 · SHA-256 b8db2bd24c7f18936e5b15cf516715a98e6e438ec602013cfc95398be780226c_

```
  212 |                 inner: RawPrivateKey::RsaOaepSha1(Box::pin(
  213 |                     RsaPrivateKey::new(rng, 2048).expect("failed to generate a key"),
  214 |                 )),
```

_file_excerpt · [crates/bitwarden-crypto/src/keys/public_key_encryption.rs](https://github.com/bitwarden/sdk-internal/blob/25b6c8c3860af5165ac1428c4c825ede7caa55de/crates/bitwarden-crypto/src/keys/public_key_encryption.rs#L256) · line 256 · SHA-256 3ac268cbd1a64d99e9da0ef771fd1fdca27725e49aa183151dad1f004c46031b_

```
  255 |             inner: RawPrivateKey::RsaOaepSha1(Box::pin(
  256 |                 RsaPrivateKey::from_pkcs8_der(der.as_ref()).map_err(|_| CryptoError::InvalidKey)?,
  257 |             )),
```

_file_excerpt · [crates/bitwarden-wasm-internal/src/pure_crypto.rs](https://github.com/bitwarden/sdk-internal/blob/25b6c8c3860af5165ac1428c4c825ede7caa55de/crates/bitwarden-wasm-internal/src/pure_crypto.rs#L335) · line 335 · SHA-256 7a34c79dc0e806bee3d30ee9f0682ac26daf519521459424fa257824d0f4ff75_

```
  334 |         let _span = tracing::info_span!("PureCrypto::rsa_decrypt_data").entered();
  335 |         let private_key = [REDACTED]
  336 |             .map_err(|_| RsaError::KeyParse)?;
```

_file_excerpt · [crates/bitwarden-wasm-internal/src/pure_crypto.rs](https://github.com/bitwarden/sdk-internal/blob/25b6c8c3860af5165ac1428c4c825ede7caa55de/crates/bitwarden-wasm-internal/src/pure_crypto.rs#L347) · line 347 · SHA-256 5fd90b377332de535692152c80d7eee3e1396fdb82d06f528a752e3b72c46545_

```
  346 |         let _span = tracing::info_span!("PureCrypto::rsa_encrypt_data").entered();
  347 |         let public_key = RsaPublicKey::from_public_key_der(public_key.as_slice())
  348 |             .map_err(|_| RsaError::KeyParse)?;
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Оборачивайте ключи ML-KEM или гибридным KEM (X25519 + ML-KEM-768) и переоберните хранимые ключи; для данных, которые уже могли скопировать, нужна отдельная оценка.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-05791 — Квантово-уязвимый RSA: роль не определена (2 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `source-code:RSA:general`
- Источник данных: crates/bitwarden-crypto/src/rsa.rs
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-28 18:19 UTC
- Балл приоритета: 35.3 / 100
- CVSS v3.1: неприменимо

2 упоминаний RSA в 2 файл(ах), например crates/bitwarden-crypto/src/rsa.rs:28. Роль по путям, именам функций и соседнему коду: роль не определена. По коду не видно, что защищают ключи; приоритет определит проверка.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте crates/bitwarden-crypto/src/rsa.rs:28 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [crates/bitwarden-crypto/src/rsa.rs](https://github.com/bitwarden/sdk-internal/blob/25b6c8c3860af5165ac1428c4c825ede7caa55de/crates/bitwarden-crypto/src/rsa.rs#L28) · line 28 · SHA-256 e2591525b753408aa77369f2928cb8381ef52f605f867462ade361e466fd34e1_

```
   27 |     let bits = 2048;
   28 |     let priv_key = RsaPrivateKey::new(&mut rng, bits).expect("failed to generate a key");
   29 |     let pub_key = RsaPublicKey::from(&priv_key);
```

_file_excerpt · [crates/bitwarden-importers/src/importers/onepassword/access/rsa.rs](https://github.com/bitwarden/sdk-internal/blob/25b6c8c3860af5165ac1428c4c825ede7caa55de/crates/bitwarden-importers/src/importers/onepassword/access/rsa.rs#L32) · line 32 · SHA-256 dc6a624da7ef99a393acfb779b400ff31d3c97335ec3af97d381a0689be997ae_

```
   31 | 
   32 |         let key = RsaPrivateKey::from_components(
   33 |             uint(&jwk.n)?,
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Классифицируйте каждое использование, зафиксируйте сроки жизни данных и запланируйте миграцию на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема; введите уровень абстракции для криптогибкости.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-05794 — Квантово-уязвимый ECDH: роль не определена (1 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `source-code:ECDH:general`
- Источник данных: crates/bitwarden-importers/src/importers/keeper/crypto/types.rs
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-28 18:19 UTC
- Балл приоритета: 35.3 / 100
- CVSS v3.1: неприменимо

1 упоминаний ECDH в 1 файл(ах), например crates/bitwarden-importers/src/importers/keeper/crypto/types.rs:515. Роль по путям, именам функций и соседнему коду: роль не определена. По коду не видно, что защищают ключи; приоритет определит проверка.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте crates/bitwarden-importers/src/importers/keeper/crypto/types.rs:515 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [crates/bitwarden-importers/src/importers/keeper/crypto/types.rs](https://github.com/bitwarden/sdk-internal/blob/25b6c8c3860af5165ac1428c4c825ede7caa55de/crates/bitwarden-importers/src/importers/keeper/crypto/types.rs#L515) · line 515 · SHA-256 5bf86ad6175b0cad4987bbbc9f5c27c2cd75216a931f7a98506ab02332ad6daa_

```
  514 | fn derive_ecdh_key(public: &PublicKey, secret: [REDACTED] -> KeeperAesKey {
  515 |     let shared = p256::ecdh::diffie_hellman(secret.to_nonzero_scalar(), public.as_affine());
  516 |     let hash = Sha256::digest(shared.raw_secret_bytes());
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Классифицируйте каждое использование, зафиксируйте сроки жизни данных и запланируйте миграцию на Гибридное установление ключей с ML-KEM (FIPS 203), например X25519MLKEM768 в TLS 1.3 или mlkem768x25519-sha256 в SSH; введите уровень абстракции для криптогибкости.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-05798 — block-buffer 0.10.4 затронут GHSA-qwgh-2vcv-g2f7

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/block-buffer@0.10.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:19 UTC
- Балл приоритета: 33.2 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-qwgh-2vcv-g2f7 для пакета crates.io block-buffer версии 0.10.4: block_buffer: panic corrupts inline buffer position. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-qwgh-2vcv-g2f7
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-qwgh-2vcv-g2f7](https://osv.dev/vulnerability/GHSA-qwgh-2vcv-g2f7) · manifest · SHA-256 ac22c9ee6301d8c1e4b09ca6951303d71527ccba2df30c96af92531d8efbb71e_

```
{"id": "GHSA-qwgh-2vcv-g2f7", "aliases": [], "modified": "2026-08-19T19:30:06.686866977Z", "summary": "block_buffer: panic corrupts inline buffer position", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:L/VI:L/VA:N/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (пока не выпущена; меры смягчения — в бюллетене).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05808 — rustls 0.23.45 затронут GHSA-vp88-798v-h67f (RUSTSEC-2026-0347)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:crates.io/rustls@0.23.45`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:19 UTC
- Балл приоритета: 39.3 / 100
- CVSS v3.1: 2.3 (`CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:U/C:L/I:N/A:N`)

OSV.dev сообщает GHSA-vp88-798v-h67f (RUSTSEC-2026-0347) для пакета crates.io rustls версии 0.23.45: rustls: ECH rejection can expose buffered application data to authenticated outer server before `ech_required` alert. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-vp88-798v-h67f
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-vp88-798v-h67f](https://osv.dev/vulnerability/GHSA-vp88-798v-h67f) · manifest · SHA-256 6c11041073dc3349e6541cf75d2505c69feda70953a329069e7cd16afc72863a_

```
{"id": "GHSA-vp88-798v-h67f", "aliases": ["RUSTSEC-2026-0347"], "modified": "2026-10-27T16:15:05.336685240Z", "summary": "rustls: ECH rejection can expose buffered application data to authenticated outer server before `ech_required` alert", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:U/C:L/I:N/A:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.23.46, 0.24.0-dev.2).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05809 — rustls 0.23.45 затронут GHSA-w44r-93j7-qv28 (RUSTSEC-2026-0349)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:crates.io/rustls@0.23.45`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:19 UTC
- Балл приоритета: 39.3 / 100
- CVSS v3.1: 3.7 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N`)

OSV.dev сообщает GHSA-w44r-93j7-qv28 (RUSTSEC-2026-0349) для пакета crates.io rustls версии 0.23.45: rustls: An unauthenticated ServerHello poisons the per-name key-exchange record, so later ClientHellos carry only a classical X25519 share. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-w44r-93j7-qv28
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-w44r-93j7-qv28](https://osv.dev/vulnerability/GHSA-w44r-93j7-qv28) · manifest · SHA-256 b623bcfe2c8c4d8706ab88fdde828cce35c31267db92f075982196f3c127f7ad_

```
{"id": "GHSA-w44r-93j7-qv28", "aliases": ["RUSTSEC-2026-0349"], "modified": "2026-10-27T16:15:05.340347056Z", "summary": "rustls: An unauthenticated ServerHello poisons the per-name key-exchange record, so later ClientHellos carry only a classical X25519 share", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.23.46, 0.24.0-dev.2).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05792 — Квантово-уязвимый Ed25519: аутентификация и идентификация (сертификаты, токены, аттестация устройств) (2 файл(ов))

- Серьёзность: **Низкая** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `source-code:Ed25519:authentication`
- Источник данных: crates/bitwarden-crypto/src/signing/cose.rs
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-28 18:19 UTC
- Балл приоритета: 28.3 / 100
- CVSS v3.1: неприменимо

7 упоминаний Ed25519 в 2 файл(ах), например crates/bitwarden-crypto/src/signing/cose.rs:70. Роль по путям, именам функций и соседнему коду: аутентификация и идентификация (сертификаты, токены, аттестация устройств). Краткоживущая аутентификация безопасна до появления CRQC; долгоживущим идентификаторам (аттестация устройств, ключи УЦ и SSH) план нужен раньше.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте crates/bitwarden-crypto/src/signing/cose.rs:70 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [crates/bitwarden-crypto/src/signing/cose.rs](https://github.com/bitwarden/sdk-internal/blob/25b6c8c3860af5165ac1428c4c825ede7caa55de/crates/bitwarden-crypto/src/signing/cose.rs#L70) · line 70 · SHA-256 5c0bee6e1713db2b0059d4defb2610144afa1856c6c1c177a7b1c95ee27f3200_

```
   69 | /// Helper function to parse a ed25519 signing key from a `CoseKey`.
   70 | pub(super) fn ed25519_signing_key(
   71 |     cose_key: &CoseKey,
```

_file_excerpt · [crates/bitwarden-crypto/src/signing/cose.rs](https://github.com/bitwarden/sdk-internal/blob/25b6c8c3860af5165ac1428c4c825ede7caa55de/crates/bitwarden-crypto/src/signing/cose.rs#L72) · line 72 · SHA-256 285d84c23973ec782cdea6724fb4dfe218290b21954d58737c9a48ec7e2f7e9e_

```
   71 |     cose_key: &CoseKey,
   72 | ) -> Result<ed25519_dalek::SigningKey, EncodingError> {
   73 |     // https://www.rfc-editor.org/rfc/rfc9053.html#name-octet-key-pair
```

_file_excerpt · [crates/bitwarden-crypto/src/signing/cose.rs](https://github.com/bitwarden/sdk-internal/blob/25b6c8c3860af5165ac1428c4c825ede7caa55de/crates/bitwarden-crypto/src/signing/cose.rs#L77) · line 77 · SHA-256 4f17f289beeff793941d2c3d0f33c08024482e615646c55218342eefabe71be0_

```
   76 |     if crv == EllipticCurve::Ed25519.to_i64().into() {
   77 |         Ok(ed25519_dalek::SigningKey::from_bytes(
   78 |             d.try_into()
```

_file_excerpt · [crates/bitwarden-ssh/src/export.rs](https://github.com/bitwarden/sdk-internal/blob/25b6c8c3860af5165ac1428c4c825ede7caa55de/crates/bitwarden-ssh/src/export.rs#L18) · line 18 · SHA-256 7db480ce7746bcf246737f107492d4c66d0ccfa9af2fce7371d2cc88f8b8b5ef_

```
   17 |         ssh_key::private::KeypairData::Ed25519(keypair) => {
   18 |             let sk: ed25519_dalek::SigningKey = keypair
   19 |                 .try_into()
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Делайте учётные данные краткоживущими и планируйте сертификаты, токены и ключи ML-DSA по мере поддержки в экосистеме.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-05793 — Квантово-уязвимый Ed25519: роль не определена (2 файл(ов))

- Серьёзность: **Низкая** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `source-code:Ed25519:general`
- Источник данных: crates/bitwarden-crypto/src/signing/signing_key.rs
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-28 18:19 UTC
- Балл приоритета: 28.3 / 100
- CVSS v3.1: неприменимо

10 упоминаний Ed25519 в 2 файл(ах), например crates/bitwarden-crypto/src/signing/signing_key.rs:10. Роль по путям, именам функций и соседнему коду: роль не определена. По коду не видно, что защищают ключи; приоритет определит проверка.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте crates/bitwarden-crypto/src/signing/signing_key.rs:10 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [crates/bitwarden-crypto/src/signing/signing_key.rs](https://github.com/bitwarden/sdk-internal/blob/25b6c8c3860af5165ac1428c4c825ede7caa55de/crates/bitwarden-crypto/src/signing/signing_key.rs#L10) · line 10 · SHA-256 f2f09e006050d809a158ac85059f520685fe484fc7e94536cb92bfe31e31d386_

```
    9 | };
   10 | use ed25519_dalek::Signer;
   11 | use hybrid_array::Array;
```

_file_excerpt · [crates/bitwarden-crypto/src/signing/signing_key.rs](https://github.com/bitwarden/sdk-internal/blob/25b6c8c3860af5165ac1428c4c825ede7caa55de/crates/bitwarden-crypto/src/signing/signing_key.rs#L16) · line 16 · SHA-256 e2df29428dceca3ed430d1f07bbd8efbfa47ab22f62988389286f4a1a0a05efe_

```
   15 | use super::{
   16 |     SignatureAlgorithm, ed25519_signing_key, key_id, mldsa_seed,
   17 |     verifying_key::{RawVerifyingKey, VerifyingKey},
```

_file_excerpt · [crates/bitwarden-crypto/src/signing/signing_key.rs](https://github.com/bitwarden/sdk-internal/blob/25b6c8c3860af5165ac1428c4c825ede7caa55de/crates/bitwarden-crypto/src/signing/signing_key.rs#L33) · line 33 · SHA-256 675866739e2cafe8197fbfc13b390c617944503e166ac310acaac9d414deffa9_

```
   32 | enum RawSigningKey {
   33 |     Ed25519(Pin<Box<ed25519_dalek::SigningKey>>),
   34 |     MlDsa44 {
```

_file_excerpt · [crates/bitwarden-crypto/src/signing/verifying_key.rs](https://github.com/bitwarden/sdk-internal/blob/25b6c8c3860af5165ac1428c4c825ede7caa55de/crates/bitwarden-crypto/src/signing/verifying_key.rs#L16) · line 16 · SHA-256 e6162ac0d4b2c81e929440f30b0b36cea5915cb2fc13f2bdec90a58ad413aeda_

```
   15 | 
   16 | use super::{SignatureAlgorithm, ed25519_verifying_key, key_id, mldsa44_verifying_key};
   17 | use crate::{
```

_file_excerpt · [crates/bitwarden-crypto/src/signing/verifying_key.rs](https://github.com/bitwarden/sdk-internal/blob/25b6c8c3860af5165ac1428c4c825ede7caa55de/crates/bitwarden-crypto/src/signing/verifying_key.rs#L28) · line 28 · SHA-256 7f4e13ff9dca95efd97b2e20875fe99cb539e4f315929e8ffe851a57c641771d_

```
   27 | pub(super) enum RawVerifyingKey {
   28 |     Ed25519(ed25519_dalek::VerifyingKey),
   29 |     MlDsa44(Box<ml_dsa::VerifyingKey<MlDsa44>>),
```

_file_excerpt · [crates/bitwarden-crypto/src/signing/verifying_key.rs](https://github.com/bitwarden/sdk-internal/blob/25b6c8c3860af5165ac1428c4c825ede7caa55de/crates/bitwarden-crypto/src/signing/verifying_key.rs#L67) · line 67 · SHA-256 b561f9eac4635daf17ca07af1fc9c83429619b6b7b9279df9e847e980fbb8847_

```
   66 |             RawVerifyingKey::Ed25519(key) => {
   67 |                 let sig = ed25519_dalek::Signature::from_bytes(
   68 |                     signature
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Классифицируйте каждое использование, зафиксируйте сроки жизни данных и запланируйте миграцию на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема; введите уровень абстракции для криптогибкости.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-05795 — Квантово-уязвимый RSA: аутентификация и идентификация (сертификаты, токены, аттестация устройств) (2 файл(ов))

- Серьёзность: **Низкая** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `source-code:RSA:authentication`
- Источник данных: crates/bitwarden-ssh/src/export.rs
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-28 18:19 UTC
- Балл приоритета: 28.3 / 100
- CVSS v3.1: неприменимо

2 упоминаний RSA в 2 файл(ах), например crates/bitwarden-ssh/src/export.rs:2. Роль по путям, именам функций и соседнему коду: аутентификация и идентификация (сертификаты, токены, аттестация устройств). Краткоживущая аутентификация безопасна до появления CRQC; долгоживущим идентификаторам (аттестация устройств, ключи УЦ и SSH) план нужен раньше.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте crates/bitwarden-ssh/src/export.rs:2 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [crates/bitwarden-ssh/src/export.rs](https://github.com/bitwarden/sdk-internal/blob/25b6c8c3860af5165ac1428c4c825ede7caa55de/crates/bitwarden-ssh/src/export.rs#L2) · line 2 · SHA-256 8b081d564977f2083ef6900c06228879ab8b09317147cfcc0f6e7434eb0adbe7_

```
    1 | use pkcs8::EncodePrivateKey;
    2 | use rsa::RsaPrivateKey;
    3 | use ssh_key::{EcdsaCurve, PrivateKey};
```

_file_excerpt · [crates/bitwarden-ssh/src/import.rs](https://github.com/bitwarden/sdk-internal/blob/25b6c8c3860af5165ac1428c4c825ede7caa55de/crates/bitwarden-ssh/src/import.rs#L132) · line 132 · SHA-256 4abe091c851e90ff549e7aae899143e25994fc74eb913acc900c1e045ad65f62_

```
  131 |         rsa::pkcs1::ALGORITHM_OID => {
  132 |             let private_key: [REDACTED] = private_key_info
  133 |                 .try_into()
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Делайте учётные данные краткоживущими и планируйте сертификаты, токены и ключи ML-DSA по мере поддержки в экосистеме.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-05800 — crypto-bigint 0.5.5 затронут RUSTSEC-2026-0387 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/crypto-bigint@0.5.5`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:19 UTC
- Балл приоритета: 20.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0387 для пакета crates.io crypto-bigint версии 0.5.5: Multiple timing variability issues in operations intended to be constant-time. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0387
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0387](https://osv.dev/vulnerability/RUSTSEC-2026-0387) · manifest · SHA-256 90c1f0cc3ccb6bb642d968797b426e8af0e7976cb2c08c7f8deb3d57ddb784c2_

```
{"id": "RUSTSEC-2026-0387", "aliases": [], "modified": "2026-10-24T03:45:02.365137418Z", "summary": "Multiple timing variability issues in operations intended to be constant-time", "severity": null, "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.7.6).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05801 — crypto-bigint 0.7.5 затронут RUSTSEC-2026-0387 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/crypto-bigint@0.7.5`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:19 UTC
- Балл приоритета: 20.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0387 для пакета crates.io crypto-bigint версии 0.7.5: Multiple timing variability issues in operations intended to be constant-time. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0387
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0387](https://osv.dev/vulnerability/RUSTSEC-2026-0387) · manifest · SHA-256 90c1f0cc3ccb6bb642d968797b426e8af0e7976cb2c08c7f8deb3d57ddb784c2_

```
{"id": "RUSTSEC-2026-0387", "aliases": [], "modified": "2026-10-24T03:45:02.365137418Z", "summary": "Multiple timing variability issues in operations intended to be constant-time", "severity": null, "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.7.6).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05802 — ctutils 0.4.2 затронут RUSTSEC-2026-0385 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/ctutils@0.4.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:19 UTC
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

### QSI-2026-05810 — rustls-webpki 0.103.15 затронут RUSTSEC-2026-0382 (CVE-2026-111943) (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/rustls-webpki@0.103.15`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:19 UTC
- Балл приоритета: 20.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0382 (CVE-2026-111943) для пакета crates.io rustls-webpki версии 0.103.15: Certificate verification may accept distrusted intermediates. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0382
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0382](https://osv.dev/vulnerability/RUSTSEC-2026-0382) · manifest · SHA-256 9111e73d752392534752d5ea5c9da4ec9a422a29c088531d446d16b27a016fa8_

```
{"id": "RUSTSEC-2026-0382", "aliases": ["CVE-2026-111943", "GO-2026-6809", "RUSTSEC-2026-0381", "RUSTSEC-2026-0383"], "modified": "2026-10-21T00:55:56.763143468Z", "summary": "Certificate verification may accept distrusted intermediates", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.103.16, 0.104.0-alpha.8).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05815 — webpki-root-certs 1.0.9 затронут RUSTSEC-2026-0383 (CVE-2026-111943) (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/webpki-root-certs@1.0.9`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:19 UTC
- Балл приоритета: 20.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0383 (CVE-2026-111943) для пакета crates.io webpki-root-certs версии 1.0.9: Bundled root certificates allow trust in distrusted emSign intermediates. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0383
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0383](https://osv.dev/vulnerability/RUSTSEC-2026-0383) · manifest · SHA-256 5020317ed72c7e0cbf2d22efcc385ee146b42c336ffbeb3bf453e64cec1e9d3d_

```
{"id": "RUSTSEC-2026-0383", "aliases": ["CVE-2026-111943", "GO-2026-6809", "RUSTSEC-2026-0381", "RUSTSEC-2026-0382"], "modified": "2026-10-21T06:30:02.691648061Z", "summary": "Bundled root certificates allow trust in distrusted emSign intermediates", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.26.11, 1.0.10).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05816 — webpki-roots 1.0.9 затронут RUSTSEC-2026-0381 (CVE-2026-111943) (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/webpki-roots@1.0.9`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:19 UTC
- Балл приоритета: 20.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0381 (CVE-2026-111943) для пакета crates.io webpki-roots версии 1.0.9: Bundled root certificates allow trust in distrusted emSign intermediates. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0381
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0381](https://osv.dev/vulnerability/RUSTSEC-2026-0381) · manifest · SHA-256 a97aff76592b60902cd4b16acc1ea2e7be27cd23fb1cd59575028f4953d51114_

```
{"id": "RUSTSEC-2026-0381", "aliases": ["CVE-2026-111943", "GO-2026-6809", "RUSTSEC-2026-0382", "RUSTSEC-2026-0383"], "modified": "2026-10-21T06:30:02.818201920Z", "summary": "Bundled root certificates allow trust in distrusted emSign intermediates", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.26.11, 1.0.10).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05807 — rustls 0.23.45 затронут GHSA-h2v8-394m-p7vv (RUSTSEC-2026-0348)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/rustls@0.23.45`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:19 UTC
- Балл приоритета: 30.0 / 100
- CVSS v3.1: 3.7 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:N/A:L`)

OSV.dev сообщает GHSA-h2v8-394m-p7vv (RUSTSEC-2026-0348) для пакета crates.io rustls версии 0.23.45: Rustls: Brotli certificate decompression can allocate an attacker-controlled amount of memory up to 1 GiB before authentication. Затронутый код находится за флагом Cargo `brotli`, выключенным по умолчанию; ни один проверенный манифест его не включает — бюллетень не применим, если флаг не включает другая зависимость.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-h2v8-394m-p7vv
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-h2v8-394m-p7vv](https://osv.dev/vulnerability/GHSA-h2v8-394m-p7vv) · manifest · SHA-256 ef730867cc8cb815c91955194f5da4ea1c0131c459ebef7b69607dc8c2b7b925_

```
{"id": "GHSA-h2v8-394m-p7vv", "aliases": ["RUSTSEC-2026-0348"], "modified": "2026-10-27T16:15:05.337819489Z", "summary": "Rustls: Brotli certificate decompression can allocate an attacker-controlled amount of memory up to 1 GiB before authentication.", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:N/A:L"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.23.46, 0.24.0-dev.2).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05812 — tokio 1.53.1 затронут RUSTSEC-2026-0386 (без оценки серьёзности)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/tokio@1.53.1`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:19 UTC
- Балл приоритета: 17.8 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0386 для пакета crates.io tokio версии 1.53.1: `AsyncFd::new` and related constructors violate I/O safety. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Ни одна из затронутых функций (tokio::io::unix::AsyncFd::new, tokio::io::unix::AsyncFd::try_new, tokio::io::unix::AsyncFd::try_with_interest, tokio::io::unix::AsyncFd::with_interest) не упоминается в проверенном коде: бюллетень не применим, если они не вызываются косвенно (через трейты, макросы, другие зависимости).

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0386
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0386](https://osv.dev/vulnerability/RUSTSEC-2026-0386) · manifest · SHA-256 1ebb594fd9923dc03209b41738d3f9cf8f324941e8844709473c643cd247e8b6_

```
{"id": "RUSTSEC-2026-0386", "aliases": [], "modified": "2026-10-23T14:45:03.847864944Z", "summary": "`AsyncFd::new` and related constructors violate I/O safety", "severity": null, "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (1.51.6, 1.53.3).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05817 — 13 бюллетеней в 5 пакет(ах) npm, нужных только для разработки или сборки

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependencies:npm:non-runtime`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch по точным версиям; область применения — из devDependencies, флагов dev в package-lock.json, разделов importers в pnpm, графа Cargo.lock от таблиц Cargo.toml и — для yarn.lock, который область не записывает вовсе — графа файла блокировки, пройденного от package.json. Если рабочее требование в файле блокировки разрешить не удалось, файл остаётся без классификации, чтобы пакет не был отложен в сторону по ошибке.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:19 UTC
- Балл приоритета: 15.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает 13 бюллетеней (7 с оценкой high или critical) для 5 пакет(ов) npm, которые подтягивают только инструменты разработки или сборки (package-lock.json): например, basic-ftp@5.3.1 [dev]: GHSA-c475-qrg2-pj4r; brace-expansion@5.0.8 [dev]: GHSA-6j4f-fj2g-mc7p, GHSA-q2hr-2g5m-vwhr, GHSA-qhr7-859c-m2p7, GHSA-rgw5-rvv9-x895; follow-redirects@1.16.0 [dev]: GHSA-8r9p-f939-6h3c, GHSA-q3jh-wrc6-jgq8; ip-address@10.3.1 [dev]: GHSA-2vr4-cq9g-pvrc, GHSA-h3mg-xc3c-68pw, GHSA-j6r3-76f7-8jcv, GHSA-rpw4-54j3-4h4q, GHSA-rxp7-6hxx-x8q5; shell-quote@1.9.0 [dev]: GHSA-pqg4-j6r4-53mv. Манифесты помечают их так (devDependencies, "dev": true в package-lock.json, [dev-dependencies]/[build-dependencies] через граф Cargo.lock), поэтому в поставляемый продукт они не входят.

**Возможные последствия.** Пользователей продукта они не затрагивают. Они могут влиять на машины разработчиков и CI (цепочка поставки): скомпрометированный или уязвимый инструмент способен изменить сборку.

**Шаги воспроизведения.**

```
Найдите пакеты из доказательства на https://osv.dev и проверьте их область применения в package-lock.json.
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev (npm)](https://osv.dev/) · package-lock.json · SHA-256 74ffc41c5a7c24e37c9f2447df9b62ad53930117d1126efe56865d39ee9b321c_

```
basic-ftp@5.3.1 [dev]: GHSA-c475-qrg2-pj4r
brace-expansion@5.0.8 [dev]: GHSA-6j4f-fj2g-mc7p, GHSA-q2hr-2g5m-vwhr, GHSA-qhr7-859c-m2p7, GHSA-rgw5-rvv9-x895
follow-redirects@1.16.0 [dev]: GHSA-8r9p-f939-6h3c, GHSA-q3jh-wrc6-jgq8
ip-address@10.3.1 [dev]: GHSA-2vr4-cq9g-pvrc, GHSA-h3mg-xc3c-68pw, GHSA-j6r3-76f7-8jcv, GHSA-rpw4-54j3-4h4q, GHSA-rxp7-6hxx-x8q5
shell-quote@1.9.0 [dev]: GHSA-pqg4-j6r4-53mv
```

**Ограничения проверки.** Данные получены от OSV.dev в зафиксированное время. Области применения взяты из манифестов; собственные build-зависимости крейтов реестра в Cargo.lock не различимы, поэтому множество runtime может оказаться больше реального, но не меньше.

**Рекомендация.** Обновите инструменты в рамках планового обслуживания; в первую очередь пакеты, которые выполняются в CI с секретами или создают релизные артефакты.

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05796 — basic-toml 0.1.10: информационный бюллетень RUSTSEC-2026-0374 (unmaintained)

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/basic-toml@0.1.10`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:19 UTC
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

### QSI-2026-05797 — bincode 1.3.3: информационный бюллетень RUSTSEC-2025-0141 (unmaintained)

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/bincode@1.3.3`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:19 UTC
- Балл приоритета: 11.6 / 100
- CVSS v3.1: неприменимо

OSV.dev отмечает RUSTSEC-2025-0141 для пакета crates.io bincode версии 1.3.3 как информационный (unmaintained): Bincode is unmaintained. Уязвимости в нём нет; неподдерживаемый пакет не получит исправлений будущих уязвимостей.

**Возможные последствия.** Известной уязвимости нет. Исправления безопасности в будущем могут не выйти.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2025-0141
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2025-0141](https://osv.dev/vulnerability/RUSTSEC-2025-0141) · manifest · SHA-256 532525d6fd3f2cb4701cae8133e80ff6557554f82b919c38fb8a089b03cf57f5_

```
{"id": "RUSTSEC-2025-0141", "aliases": [], "modified": "2026-01-16T11:07:28.867553Z", "summary": "Bincode is unmaintained", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные получены от OSV.dev в зафиксированное время.

**Рекомендация.** Запланируйте переход на поддерживаемую альтернативу или зафиксируйте решение оставить пакет.

**Повторная проверка.** Повторите сканирование зависимостей после изменения.

### QSI-2026-05799 — buf_redux 0.8.4: информационный бюллетень RUSTSEC-2023-0028 (unmaintained)

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/buf_redux@0.8.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:19 UTC
- Балл приоритета: 11.6 / 100
- CVSS v3.1: неприменимо

OSV.dev отмечает RUSTSEC-2023-0028 для пакета crates.io buf_redux версии 0.8.4 как информационный (unmaintained): buf_redux is Unmaintained. Уязвимости в нём нет; неподдерживаемый пакет не получит исправлений будущих уязвимостей.

**Возможные последствия.** Известной уязвимости нет. Исправления безопасности в будущем могут не выйти.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2023-0028
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2023-0028](https://osv.dev/vulnerability/RUSTSEC-2023-0028) · manifest · SHA-256 48538b296813b8bfb0d98dd5507f8bcde0ed4ee03765e3f52ba4d56c7fb37649_

```
{"id": "RUSTSEC-2023-0028", "aliases": [], "modified": "2023-03-24T15:42:41Z", "summary": "buf_redux is Unmaintained", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные получены от OSV.dev в зафиксированное время.

**Рекомендация.** Запланируйте переход на поддерживаемую альтернативу или зафиксируйте решение оставить пакет.

**Повторная проверка.** Повторите сканирование зависимостей после изменения.

### QSI-2026-05803 — fxhash 0.2.1: информационный бюллетень RUSTSEC-2025-0057 (unmaintained)

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/fxhash@0.2.1`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:19 UTC
- Балл приоритета: 11.6 / 100
- CVSS v3.1: неприменимо

OSV.dev отмечает RUSTSEC-2025-0057 для пакета crates.io fxhash версии 0.2.1 как информационный (unmaintained): fxhash - no longer maintained. Уязвимости в нём нет; неподдерживаемый пакет не получит исправлений будущих уязвимостей.

**Возможные последствия.** Известной уязвимости нет. Исправления безопасности в будущем могут не выйти.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2025-0057
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2025-0057](https://osv.dev/vulnerability/RUSTSEC-2025-0057) · manifest · SHA-256 c45d3d45f6cc6072f9f3ea781a96fb14cfe9cb6b704b66765b32d3eb712a646e_

```
{"id": "RUSTSEC-2025-0057", "aliases": [], "modified": "2025-09-05T19:09:01Z", "summary": "fxhash - no longer maintained", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные получены от OSV.dev в зафиксированное время.

**Рекомендация.** Запланируйте переход на поддерживаемую альтернативу или зафиксируйте решение оставить пакет.

**Повторная проверка.** Повторите сканирование зависимостей после изменения.

### QSI-2026-05804 — multipart 0.18.0: информационный бюллетень RUSTSEC-2023-0050 (unmaintained)

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/multipart@0.18.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:19 UTC
- Балл приоритета: 11.6 / 100
- CVSS v3.1: неприменимо

OSV.dev отмечает RUSTSEC-2023-0050 для пакета crates.io multipart версии 0.18.0 как информационный (unmaintained): multipart is Unmaintained. Уязвимости в нём нет; неподдерживаемый пакет не получит исправлений будущих уязвимостей.

**Возможные последствия.** Известной уязвимости нет. Исправления безопасности в будущем могут не выйти.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2023-0050
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2023-0050](https://osv.dev/vulnerability/RUSTSEC-2023-0050) · manifest · SHA-256 c1d0680d4f7bf0ee8ffd004252d2ee5a8d437f36ff62d04322e9ecc7f5611db9_

```
{"id": "RUSTSEC-2023-0050", "aliases": [], "modified": "2023-08-18T20:38:40Z", "summary": "multipart is Unmaintained", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные получены от OSV.dev в зафиксированное время.

**Рекомендация.** Запланируйте переход на поддерживаемую альтернативу или зафиксируйте решение оставить пакет.

**Повторная проверка.** Повторите сканирование зависимостей после изменения.

### QSI-2026-05811 — safemem 0.3.3: информационный бюллетень RUSTSEC-2023-0081 (unmaintained)

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/safemem@0.3.3`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:19 UTC
- Балл приоритета: 11.6 / 100
- CVSS v3.1: неприменимо

OSV.dev отмечает RUSTSEC-2023-0081 для пакета crates.io safemem версии 0.3.3 как информационный (unmaintained): safemem is unmaintained. Уязвимости в нём нет; неподдерживаемый пакет не получит исправлений будущих уязвимостей.

**Возможные последствия.** Известной уязвимости нет. Исправления безопасности в будущем могут не выйти.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2023-0081
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2023-0081](https://osv.dev/vulnerability/RUSTSEC-2023-0081) · manifest · SHA-256 0aa325e672dc4e57cb8b3c852ef75dcfabd897920b78292cd744e7350f009b70_

```
{"id": "RUSTSEC-2023-0081", "aliases": [], "modified": "2024-03-04T18:47:07Z", "summary": "safemem is unmaintained", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные получены от OSV.dev в зафиксированное время.

**Рекомендация.** Запланируйте переход на поддерживаемую альтернативу или зафиксируйте решение оставить пакет.

**Повторная проверка.** Повторите сканирование зависимостей после изменения.

### QSI-2026-05813 — twoway 0.1.8: информационный бюллетень RUSTSEC-2021-0146 (unmaintained)

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/twoway@0.1.8`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:19 UTC
- Балл приоритета: 11.6 / 100
- CVSS v3.1: неприменимо

OSV.dev отмечает RUSTSEC-2021-0146 для пакета crates.io twoway версии 0.1.8 как информационный (unmaintained): Crate `twoway` deprecated by the author. Уязвимости в нём нет; неподдерживаемый пакет не получит исправлений будущих уязвимостей.

**Возможные последствия.** Известной уязвимости нет. Исправления безопасности в будущем могут не выйти.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2021-0146
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2021-0146](https://osv.dev/vulnerability/RUSTSEC-2021-0146) · manifest · SHA-256 776f95d918d1a37b3a270ce8e1a97785b3bb1db62923e580de9cb25f8b943cbb_

```
{"id": "RUSTSEC-2021-0146", "aliases": [], "modified": "2023-02-09T03:11:29Z", "summary": "Crate `twoway` deprecated by the author", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные получены от OSV.dev в зафиксированное время.

**Рекомендация.** Запланируйте переход на поддерживаемую альтернативу или зафиксируйте решение оставить пакет.

**Повторная проверка.** Повторите сканирование зависимостей после изменения.

### QSI-2026-05814 — unsafe-libyaml 0.2.11: информационный бюллетень RUSTSEC-2024-0449 (unmaintained)

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/unsafe-libyaml@0.2.11`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:19 UTC
- Балл приоритета: 11.6 / 100
- CVSS v3.1: неприменимо

OSV.dev отмечает RUSTSEC-2024-0449 для пакета crates.io unsafe-libyaml версии 0.2.11 как информационный (unmaintained): unsafe-libyaml is unmaintained. Уязвимости в нём нет; неподдерживаемый пакет не получит исправлений будущих уязвимостей.

**Возможные последствия.** Известной уязвимости нет. Исправления безопасности в будущем могут не выйти.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2024-0449
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2024-0449](https://osv.dev/vulnerability/RUSTSEC-2024-0449) · manifest · SHA-256 26d102e813573cb2577fa623e28e26359b004df953372bdda3fd7cf447bb3d4b_

```
{"id": "RUSTSEC-2024-0449", "aliases": [], "modified": "2026-10-12T11:45:02.518189315Z", "summary": "unsafe-libyaml is unmaintained", "severity": null, "declared_in_manifest": false}
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

### Постквантовая зрелость: Уровень 2 из 4 — постквантовое используется вне критичных путей

- Используется: ML-DSA — crates/bitwarden-crypto/src/signing/cose.rs
- Используется: ML-DSA — crates/bitwarden-crypto/src/signing/signing_key.rs
- Используется: ML-DSA — crates/bitwarden-crypto/src/signing/verifying_key.rs
- Постквантовая библиотека объявлена в зависимостях
- Только классика — обмен ключами в канале (TLS, Noise, рукопожатия): TLS (classical groups) (2 файл(ов))
- Только классика — обёртка ключей и шифрование хранимых данных: RSA (3 файл(ов))

**Следующий шаг:** Распространите постквантовую защиту на критичные роли, которые остаются классическими, начиная с того, что можно записать уже сегодня (обёрнутые ключи, обмен ключами в канале).

_Уровни: 0 — нет; 1 — есть, но не подключено; 2 — используется вне критичных путей; 3 — гибрид в критичном пути; 4 — постквантовое по умолчанию в критичных путях (корень доверия, обёртка ключей, обмен ключами в канале). Оценка по коду и манифестам._

### Что делают квантово-уязвимые алгоритмы

| Роль | Алгоритмы (файлы) | ID | Первый шаг |
|---|---|---|---|
| **обёртка ключей и шифрование хранимых данных** | RSA (3) | QSI-2026-05790 | Оборачивайте ключи ML-KEM или гибридным KEM (X25519 + ML-KEM-768) и переоберните хранимые ключи; для данных, которые уже могли скопировать, нужна отдельная оценка |
| **обмен ключами в канале (TLS, Noise, рукопожатия)** | TLS ECDHE (2) | QSI-2026-05789 | Переведите рукопожатие на гибридный обмен ключами (X25519MLKEM768 в TLS 1.3; гибридный KEM в протоколах на основе Noise) |
| **аутентификация и идентификация (сертификаты, токены, аттестация устройств)** | Ed25519 (2), RSA (2) | QSI-2026-05792, QSI-2026-05795 | Делайте учётные данные краткоживущими и планируйте сертификаты, токены и ключи ML-DSA по мере поддержки в экосистеме |
| **роль не определена** | Ed25519 (2), RSA (2), ECDH (1) | QSI-2026-05791, QSI-2026-05793, QSI-2026-05794 | Классифицируйте каждое использование, зафиксируйте сроки жизни данных и запланируйте миграцию на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема; введите уровень абстракции для криптогибкости |

_Роль определяется по путям файлов, именам функций и коду вокруг совпадений; проверка её подтверждает. Сначала — ключи корня доверия и обёрнутые ключи: их трудно заменить или можно записать уже сегодня._
Анкета готовности для проекта не заполнялась.

### Квантовые алгоритмы, значимые для этой инвентаризации

| Квантовый алгоритм | Действие | Модель атаки | Алгоритмы из инвентаризации (строк) | Что это значит для аудита |
|---|---|---|---|---|
| Алгоритм Шора — факторизация | взламывает | Q1 | RSA (7) | Взламывает RSA при любой длине ключа: более длинный модуль лишь полиномиально повышает стоимость. Планируйте переход на ML-KEM (или гибрид) для установления ключей и ML-DSA / SLH-DSA для подписей; начинайте с ключей, защищающих данные, которые должны оставаться конфиденциальными годами («собери сейчас — расшифруй потом»), и с долгоживущих подписей. |
| Алгоритм Шора — дискретный логарифм на эллиптических кривых | взламывает | Q1 | ECDH (1), Ed25519 (4) | Ключи на эллиптических кривых, по оценкам, падут раньше ключей RSA сопоставимой классической стойкости. В блокчейнах первыми под угрозой монеты, чей открытый ключ уже опубликован (повторно используемые адреса, выходы pay-to-public-key и Taproot); планируйте переход на постквантовые подписи и до этого избегайте повторного использования ключей. |
| Алгоритм Гровера — поиск ключа и прообразов | ослабляет (более длинные ключи восстанавливают запас) | Q1 | AES-256 (25), Argon2 (2), ChaCha20-Poly1305 (5), HKDF (7), HMAC (13), SHA-2 (17) | Не взлом. Ключи 256 бит (AES-256, ChaCha20) сохраняют хороший запас; AES-128 соответствует категории 1 NIST, но некоторые регуляторы требуют 256-битных ключей в квантово-устойчивых системах (см. запись AES-128). Для долгоживущих данных предпочитайте 256-битные ключи; 256-битные хеши для стойкости к прообразам менять не нужно. |
| Брассар–Хойер–Тапп — поиск коллизий | ослабляет (более длинные ключи восстанавливают запас) | Q1 | SHA-2 (17) | 256-битные хеши (SHA-256, SHA3-256) остаются достаточными по стойкости к коллизиям; 160-битные хеши слабы уже классически (коллизии SHA-1 практичны). Где нужны категории NIST 4–5, используйте хеши на 384/512 бит. |
| Алгоритм Саймона — суперпозиционные атаки на симметричные конструкции | только при суперпозиционных запросах | Q2 | GCM mode (2) | Для обычного применения AES-GCM или CBC-MAC действий не требуется — модель атаки неприменима. Зафиксируйте это как допущение модели; для конструкций типа Even–Mansour см. офлайн-вариант. |
| Квантовое решетчатое просеивание | учтено в стандартных параметрах | Q1 | ML-DSA (3) | Для ML-KEM и ML-DSA в стандартных наборах параметров ничего менять не нужно. Заявление 2024 года о полиномиальном квантовом алгоритме для LWE отозвано после обнаружения ошибки (см. заявления). |

_Действие: взламывает — алгоритм нужно заменить; ослабляет — более длинные ключи или выходы восстанавливают запас; учтено в стандартных параметрах — при стандартных наборах действий не требуется; только при суперпозиционных запросах — к обычному применению неприменимо._


## 9. Ограничения и допущения

- Отчёт содержит результаты автоматизированного и документального анализа в указанных границах. Он не является юридическим заключением, сертификацией или подтверждением соответствия какому-либо стандарту.
- z — плановое допущение профиля риска, а не прогноз. Публично известного криптографически значимого квантового компьютера сегодня не существует.

## 10. План устранения проблем / Приоритеты на 30, 60 и 90 дней

### 30 дн.

| Приоритет | ID | Действие | Тип | Условие закрытия |
|---|---|---|---|---|
| P2 | QSI-2026-05805 | Обновите rsa до исправленной версии (пока не выпущена; меры смягчения — в бюллетене). | устранение первопричины | Сканирование зависимостей больше не сообщает RUSTSEC-2023-0071 (CVE-2023-49092). |
| P2 | QSI-2026-05806 | Обновите rustls до исправленной версии (0.23.46, 0.24.0-dev.2). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-c8m5-c952-6cm4 (RUSTSEC-2026-0346). |
| P2 | QSI-2026-05798 | Обновите block-buffer до исправленной версии (пока не выпущена; меры смягчения — в бюллетене). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-qwgh-2vcv-g2f7. |
| P2 | QSI-2026-05808 | Обновите rustls до исправленной версии (0.23.46, 0.24.0-dev.2). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-vp88-798v-h67f (RUSTSEC-2026-0347). |
| P2 | QSI-2026-05809 | Обновите rustls до исправленной версии (0.23.46, 0.24.0-dev.2). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-w44r-93j7-qv28 (RUSTSEC-2026-0349). |
| P2 | QSI-2026-05807 | Обновите rustls до исправленной версии (0.23.46, 0.24.0-dev.2). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-h2v8-394m-p7vv (RUSTSEC-2026-0348). |
### 60 дн.

| Приоритет | ID | Действие | Тип | Условие закрытия |
|---|---|---|---|---|
| P2 | QSI-2026-05789 | Соберите rustls с провайдером aws-lc-rs (rustls::crypto::aws_lc_rs) и функцией prefer-post-quantum, которая ставит X25519MLKEM768 первым. | устранение первопричины | PQ-клиент согласует X25519MLKEM768. |
| P3 | QSI-2026-05800 | Разберите RUSTSEC-2026-0387; при необходимости обновите crypto-bigint до исправленной версии (0.7.6). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0387 или результат разбора записан. |
| P3 | QSI-2026-05801 | Разберите RUSTSEC-2026-0387; при необходимости обновите crypto-bigint до исправленной версии (0.7.6). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0387 или результат разбора записан. |
| P3 | QSI-2026-05802 | Разберите RUSTSEC-2026-0385; при необходимости обновите ctutils до исправленной версии (0.4.4). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0385 или результат разбора записан. |
| P3 | QSI-2026-05810 | Разберите RUSTSEC-2026-0382 (CVE-2026-111943); при необходимости обновите rustls-webpki до исправленной версии (0.103.16, 0.104.0-alpha.8). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0382 (CVE-2026-111943) или результат разбора записан. |
| P3 | QSI-2026-05815 | Разберите RUSTSEC-2026-0383 (CVE-2026-111943); при необходимости обновите webpki-root-certs до исправленной версии (0.26.11, 1.0.10). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0383 (CVE-2026-111943) или результат разбора записан. |
| P3 | QSI-2026-05816 | Разберите RUSTSEC-2026-0381 (CVE-2026-111943); при необходимости обновите webpki-roots до исправленной версии (0.26.11, 1.0.10). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0381 (CVE-2026-111943) или результат разбора записан. |
| P3 | QSI-2026-05812 | Разберите RUSTSEC-2026-0386; при необходимости обновите tokio до исправленной версии (1.51.6, 1.53.3). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0386 или результат разбора записан. |
### 90 дн.

| Приоритет | ID | Действие | Тип | Условие закрытия |
|---|---|---|---|---|
| P3 | QSI-2026-05790 | Внесите использования RSA в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-05791 | Внесите использования RSA в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-05794 | Внесите использования ECDH в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-05792 | Внесите использования Ed25519 в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-05793 | Внесите использования Ed25519 в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-05795 | Внесите использования RSA в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P4 | QSI-2026-05790 | Запланируйте миграцию RSA на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема или гибридной схемы. |
| P4 | QSI-2026-05791 | Запланируйте миграцию RSA на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема или гибридной схемы. |
| P4 | QSI-2026-05794 | Запланируйте миграцию ECDH на Гибридное установление ключей с ML-KEM (FIPS 203), например X25519MLKEM768 в TLS 1.3 или mlkem768x25519-sha256 в SSH (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование Гибридное установление ключей с ML-KEM (FIPS 203), например X25519MLKEM768 в TLS 1.3 или mlkem768x25519-sha256 в SSH или гибридной схемы. |
| P4 | QSI-2026-05792 | Запланируйте миграцию Ed25519 на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема или гибридной схемы. |
| P4 | QSI-2026-05793 | Запланируйте миграцию Ed25519 на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема или гибридной схемы. |
| P4 | QSI-2026-05795 | Запланируйте миграцию RSA на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема или гибридной схемы. |
| P4 | QSI-2026-05817 | Обновите зависимости разработки и сборки из доказательства. | устранение первопричины | Сканирование не сообщает бюллетеней для пакетов инструментов, либо оставшиеся зафиксированы. |
| P4 | QSI-2026-05796 | Замените basic-toml поддерживаемой альтернативой или зафиксируйте, почему он остаётся. | устранение первопричины | basic-toml заменён или решение зафиксировано. |
| P4 | QSI-2026-05797 | Замените bincode поддерживаемой альтернативой или зафиксируйте, почему он остаётся. | устранение первопричины | bincode заменён или решение зафиксировано. |
| P4 | QSI-2026-05799 | Замените buf_redux поддерживаемой альтернативой или зафиксируйте, почему он остаётся. | устранение первопричины | buf_redux заменён или решение зафиксировано. |
| P4 | QSI-2026-05803 | Замените fxhash поддерживаемой альтернативой или зафиксируйте, почему он остаётся. | устранение первопричины | fxhash заменён или решение зафиксировано. |
| P4 | QSI-2026-05804 | Замените multipart поддерживаемой альтернативой или зафиксируйте, почему он остаётся. | устранение первопричины | multipart заменён или решение зафиксировано. |
| P4 | QSI-2026-05811 | Замените safemem поддерживаемой альтернативой или зафиксируйте, почему он остаётся. | устранение первопричины | safemem заменён или решение зафиксировано. |
| P4 | QSI-2026-05813 | Замените twoway поддерживаемой альтернативой или зафиксируйте, почему он остаётся. | устранение первопричины | twoway заменён или решение зафиксировано. |
| P4 | QSI-2026-05814 | Замените unsafe-libyaml поддерживаемой альтернативой или зафиксируйте, почему он остаётся. | устранение первопричины | unsafe-libyaml заменён или решение зафиксировано. |

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

1. A. Becker, L. Ducas, N. Gama, T. Laarhoven — New directions in nearest neighbor searching with applications to lattice sieving (SODA 2016; IACR ePrint 2015/1128) — IACR ePrint. <https://eprint.iacr.org/2015/1128> (peer-reviewed article: classical sieving in 2^{0.292n + o(n)})
2. A. Chailloux, J. Loyer — Lattice sieving via quantum random walks (ASIACRYPT 2021; IACR ePrint 2021/570) — IACR ePrint. <https://eprint.iacr.org/2021/570> (peer-reviewed article: 2^{0.2570d + o(d)}, previously 2^{0.2653d + o(d)} (Laarhoven))
3. A. Chailloux, M. Naya-Plasencia, A. Schrottenloher — An Efficient Quantum Collision Search Algorithm and Implications on Symmetric Cryptography (ASIACRYPT 2017; IACR ePrint 2017/847) — IACR ePrint. <https://eprint.iacr.org/2017/847> (peer-reviewed article: Õ(2^{2n/5}) time, O(n) qubits, Õ(2^{n/5}) classical memory)
4. C. Chevignard, P.-A. Fouque, A. Schrottenloher — Reducing the Number of Qubits in Quantum Discrete Logarithms on Elliptic Curves (IACR ePrint 2026/280) — IACR ePrint. <https://eprint.iacr.org/2026/280> (revision of a EUROCRYPT 2026 paper: 3.12n + o(n) qubits; for n = 256, 1193 qubits and 22 runs of 2^38.98 Toffoli gates)
5. C. Gidney — How to factor 2048 bit RSA integers with less than a million noisy qubits (arXiv:2505.15917) — arXiv. <https://arxiv.org/abs/2505.15917> (preprint (2025-05-21): < 1 million noisy qubits, < 1 week, 0.1% gate error, 1 µs surface-code cycle)
6. C. Gidney, M. Ekerå — How to factor 2048 bit RSA integers in 8 hours using 20 million noisy qubits (Quantum 5, 433) — Quantum. <https://doi.org/10.22331/q-2021-04-15-433> (peer-reviewed article (2021): 10^-3 gate error, 1 µs cycle, 10 µs reaction time)
7. C. Zalka — Grover's quantum searching algorithm is optimal (Phys. Rev. A 60, 2746, 1999; arXiv:quant-ph/9711070) — APS. <https://doi.org/10.1103/PhysRevA.60.2746> (peer-reviewed article: optimal for any success probability; parallel search gains no more than splitting the space)
8. CRYSTALS-Kyber — Algorithm Specifications and Supporting Documentation (round 3, 2021-08-04) — CRYSTALS team. <https://pq-crystals.org/kyber/data/kyber-specification-round3-20210804.pdf> (NIST round-3 submission: core-SVP cost 2^{0.292β} classical, 2^{0.265β} quantum; Kyber768 166 quantum bits)
9. Common Vulnerability Scoring System v3.1: Specification Document — FIRST. <https://www.first.org/cvss/v3.1/specification-document> (final)
10. D. J. Bernstein — Cost analysis of hash collisions: Will quantum computers make SHARCS obsolete? (2009) — cr.yp.to. <https://cr.yp.to/hash/collisioncost-20090823.pdf> (paper dated 2009-08-23)
11. D. Litinski — How to compute a 256-bit elliptic curve private key with only 50 million Toffoli gates (arXiv:2306.08585) — arXiv. <https://arxiv.org/abs/2306.08585> (preprint (2023-06-14): 6000 modules × 1152 physical qubits, one key per 10 minutes under its architecture assumptions)
12. D. R. Simon — On the Power of Quantum Computation (SIAM J. Comput. 26, 1997) — SIAM. <https://doi.org/10.1137/S0097539796298637> (peer-reviewed article)
13. FIPS 203 — Module-Lattice-Based Key-Encapsulation Mechanism Standard (ML-KEM) — NIST. <https://csrc.nist.gov/pubs/fips/203/final> (final (August 2024))
14. FIPS 204 — Module-Lattice-Based Digital Signature Standard (ML-DSA) — NIST. <https://csrc.nist.gov/pubs/fips/204/final> (final (August 2024))
15. FIPS 205 — Stateless Hash-Based Digital Signature Standard (SLH-DSA) — NIST. <https://csrc.nist.gov/pubs/fips/205/final> (final (August 2024))
16. G. Brassard, P. Høyer, A. Tapp — Quantum Algorithm for the Collision Problem (LATIN '98; arXiv:quant-ph/9705002) — Springer / arXiv. <https://arxiv.org/abs/quant-ph/9705002> (peer-reviewed article: collisions of r-to-one functions in O((N/r)^{1/3}) expected evaluations)
17. H. Kuwakado, M. Morii — Quantum distinguisher between the 3-round Feistel cipher and the random permutation (IEEE ISIT 2010) — IEEE. <https://ieeexplore.ieee.org/document/5513654> (peer-reviewed conference paper)
18. IANA — Transport Layer Security (TLS) Parameters (Supported Groups, SignatureScheme, Cipher Suites) — IANA. <https://www.iana.org/assignments/tls-parameters/> (living registry (checked 2026-10-13); 'Recommended' column Y/N/D)
19. J. Proos, C. Zalka — Shor's discrete logarithm quantum algorithm for elliptic curves (Quantum Inf. Comput. 3(4), 2003; arXiv:quant-ph/0301141) — Quantum Information & Computation. <https://doi.org/10.26421/QIC3.4-3> (peer-reviewed article)
20. L. K. Grover — A fast quantum mechanical algorithm for database search (STOC 1996) — ACM. <https://doi.org/10.1145/237814.237866> (peer-reviewed article)
21. M. Amy et al. — Estimating the cost of generic quantum pre-image attacks on SHA-2 and SHA-3 (SAC 2016; arXiv:1603.09383) — Springer / arXiv. <https://arxiv.org/abs/1603.09383> (peer-reviewed article: SHA-256 about 2^153.8 surface-code cycles on 2^12.6 logical qubits; SHA3-256 about 2^146.5 cycles on 2^20)
22. M. Cain et al. — Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits (arXiv:2603.28627) — arXiv. <https://arxiv.org/abs/2603.28627> (preprint (2026-03-30): P-256 in a few days with 26,000 physical neutral-atom qubits; RSA-2048 one to two orders of magnitude longer)
23. M. Kaplan, G. Leurent, A. Leverrier, M. Naya-Plasencia — Breaking Symmetric Cryptosystems using Quantum Period Finding (CRYPTO 2016; arXiv:1602.05973) — Springer / arXiv. <https://arxiv.org/abs/1602.05973> (peer-reviewed article: superposition-query forgeries on CBC-MAC, PMAC, GMAC, GCM, OCB)
24. M. Mosca — Cybersecurity in an Era with Quantum Computers: Will We Be Ready? (IEEE Security & Privacy, 2018) — IEEE. <https://doi.org/10.1109/MSP.2018.3761723> (peer-reviewed article; source of the x + y > z migration inequality)
25. M. Roetteler, M. Naehrig, K. Svore, K. Lauter — Quantum resource estimates for computing elliptic curve discrete logarithms (ASIACRYPT 2017) — IACR / arXiv. <https://arxiv.org/abs/1706.06752> (peer-reviewed article: at most 9n + 2⌈log2 n⌉ + 10 qubits and 448 n^3 log2 n + 4090 n^3 Toffoli gates)
26. NIST IR 8547 — Transition to Post-Quantum Cryptography Standards — NIST. <https://csrc.nist.gov/pubs/ir/8547/ipd> (initial public draft (November 2024); proposes deprecating quantum-vulnerable public-key algorithms after 2030 and disallowing them after 2035 — dates may change in the final version)
27. NIST — Post-Quantum Cryptography Standardization: Evaluation Criteria, Security (Call for Proposals, Section 4.A.5) — NIST. <https://csrc.nist.gov/Projects/Post-Quantum-Cryptography/Post-Quantum-Cryptography-Standardization/Evaluation-Criteria/Security-(Evaluation-Criteria)> (security categories: AES-128 key search 2^170/MAXDEPTH quantum gates, AES-192 2^233/MAXDEPTH, AES-256 2^298/MAXDEPTH; MAXDEPTH 2^40–2^96)
28. OSV advisory GHSA-c8m5-c952-6cm4 — OSV.dev. <https://osv.dev/vulnerability/GHSA-c8m5-c952-6cm4> (modified 2026-10-27T16:15:05.354395696Z)
29. OSV advisory GHSA-h2v8-394m-p7vv — OSV.dev. <https://osv.dev/vulnerability/GHSA-h2v8-394m-p7vv> (modified 2026-10-27T16:15:05.337819489Z)
30. OSV advisory GHSA-qwgh-2vcv-g2f7 — OSV.dev. <https://osv.dev/vulnerability/GHSA-qwgh-2vcv-g2f7> (modified 2026-08-19T19:30:06.686866977Z)
31. OSV advisory GHSA-vp88-798v-h67f — OSV.dev. <https://osv.dev/vulnerability/GHSA-vp88-798v-h67f> (modified 2026-10-27T16:15:05.336685240Z)
32. OSV advisory GHSA-w44r-93j7-qv28 — OSV.dev. <https://osv.dev/vulnerability/GHSA-w44r-93j7-qv28> (modified 2026-10-27T16:15:05.340347056Z)
33. OSV advisory RUSTSEC-2021-0146 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2021-0146> (modified 2023-02-09T03:11:29Z)
34. OSV advisory RUSTSEC-2023-0028 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2023-0028> (modified 2023-03-24T15:42:41Z)
35. OSV advisory RUSTSEC-2023-0050 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2023-0050> (modified 2023-08-18T20:38:40Z)
36. OSV advisory RUSTSEC-2023-0071 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2023-0071> (modified 2026-09-14T09:45:02.996132556Z)
37. OSV advisory RUSTSEC-2023-0081 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2023-0081> (modified 2024-03-04T18:47:07Z)
38. OSV advisory RUSTSEC-2024-0449 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2024-0449> (modified 2026-10-12T11:45:02.518189315Z)
39. OSV advisory RUSTSEC-2025-0057 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2025-0057> (modified 2025-09-05T19:09:01Z)
40. OSV advisory RUSTSEC-2025-0141 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2025-0141> (modified 2026-01-16T11:07:28.867553Z)
41. OSV advisory RUSTSEC-2026-0374 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0374> (modified 2026-10-20T11:15:37.076409305Z)
42. OSV advisory RUSTSEC-2026-0381 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0381> (modified 2026-10-21T06:30:02.818201920Z)
43. OSV advisory RUSTSEC-2026-0382 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0382> (modified 2026-10-21T00:55:56.763143468Z)
44. OSV advisory RUSTSEC-2026-0383 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0383> (modified 2026-10-21T06:30:02.691648061Z)
45. OSV advisory RUSTSEC-2026-0385 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0385> (modified 2026-10-23T08:30:02.389575143Z)
46. OSV advisory RUSTSEC-2026-0386 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0386> (modified 2026-10-23T14:45:03.847864944Z)
47. OSV advisory RUSTSEC-2026-0387 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0387> (modified 2026-10-24T03:45:02.365137418Z)
48. OSV.dev — open-source vulnerability database and API — Open Source Security Foundation. <https://osv.dev/> (the database QSI queries for each exactly pinned version; every advisory id in a finding resolves at https://osv.dev/vulnerability/<id>)
49. P. W. Shor — Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms on a Quantum Computer (SIAM J. Comput., 1997) — SIAM. <https://doi.org/10.1137/S0097539795293172> (peer-reviewed article)
50. R. Babbush et al. — Securing Elliptic Curve Cryptocurrencies against Quantum Vulnerabilities: Resource Estimates and Mitigations (arXiv:2603.28846) — arXiv. <https://arxiv.org/abs/2603.28846> (preprint (2026-03-30, v2 2026-04-15): 256-bit ECDLP with < 1200 logical qubits and < 90 M Toffoli gates (or < 1450 and < 70 M); < 500,000 physical qubits at 10^-3 error, minutes)
51. RFC 10024 — Hybrid ECDHE-MLKEM key agreement for TLS 1.3 (X25519MLKEM768, SecP256r1MLKEM768, SecP384r1MLKEM1024) — IETF. <https://www.rfc-editor.org/rfc/rfc10024> (standards track; checked 2026-10-13)
52. S. Jaques, M. Naehrig, M. Roetteler, F. Virdia — Implementing Grover oracles for quantum key search on AES and LowMC (EUROCRYPT 2020; arXiv:1910.01700) — Springer / arXiv. <https://arxiv.org/abs/1910.01700> (peer-reviewed article: lower cost estimates for the AES key searches that define the NIST categories)

## Приложения: Криптографическая инвентаризация

| Алгоритм | Параметр | Библиотека | Квантовый статус | Классический статус | Количество | Мест | Примеры |
|---|---|---|---|---|---|---|---|
| AES-256 | AES-256 |  | сниженный запас (Гровер), одобрен | допустимо | 25 | 25 | crates/bitwarden-core/src/key_management/crypto/reinit_user_crypto.rs:122; crates/bitwarden-core/src/key_management/crypto_client.rs:292; crates/bitwarden-crypto/src/cose/symmetric.rs:17 |
| Argon2 |  |  | сниженный запас (Гровер), одобрен | допустимо | 2 | 2 | crates/bitwarden-crypto/src/safe/password_protected_key_envelope.rs:303; crates/bitwarden-uniffi/kotlin/app/src/main/java/com/bitwarden/myapplication/MainActivity.kt:228 |
| ChaCha20-Poly1305 | ChaCha20-Poly1305 |  | сниженный запас (Гровер), одобрен | допустимо | 4 | 4 | crates/bitwarden-crypto/src/cose/symmetric.rs:23; crates/bitwarden-crypto/src/hazmat/symmetric_encryption/mod.rs:35; crates/bitwarden-ipc/src/crypto_provider/noise/handshake.rs:38 |
| ChaCha20-Poly1305 |  |  | сниженный запас (Гровер), одобрен | допустимо | 1 | 1 | crates/bitwarden-crypto/src/hazmat/symmetric_encryption/xchacha20.rs |
| HKDF |  |  | сниженный запас (Гровер), одобрен | допустимо | 7 | 7 | crates/bitwarden-crypto/src/fingerprint.rs:19; crates/bitwarden-crypto/src/keys/shareable_key.rs:9; crates/bitwarden-crypto/src/keys/utils.rs:7 |
| HMAC | HMAC-SHA-256 |  | сниженный запас (Гровер), одобрен | допустимо | 3 | 3 | crates/bitwarden-crypto/src/hazmat/symmetric_encryption/aes256_cbc_hmac_sha256_ae.rs:12; crates/bitwarden-crypto/src/hazmat/symmetric_encryption/aes256_cbc_hmac_sha256_aead.rs:14; crates/bitwarden-vault/src/totp.rs:20 |
| HMAC |  |  | сниженный запас (Гровер), одобрен | допустимо | 8 | 8 | crates/bitwarden-crypto/src/hazmat/symmetric_encryption/aes256_cbc_hmac_sha256_ae.rs:7; crates/bitwarden-crypto/src/hazmat/symmetric_encryption/aes256_cbc_hmac_sha256_aead.rs:7; crates/bitwarden-crypto/src/keys/shareable_key.rs:3 |
| HMAC | HMAC-SHA-1 |  | сниженный запас (Гровер), одобрен | устаревающий | 1 | 1 | crates/bitwarden-vault/src/totp.rs:19 |
| HMAC | HMAC-SHA-512 |  | сниженный запас (Гровер), одобрен | допустимо | 1 | 1 | crates/bitwarden-vault/src/totp.rs:21 |
| SHA-2 | SHA-512 |  | сниженный запас (Гровер), одобрен | допустимо | 1 | 1 | crates/bitwarden-vault/src/totp.rs:21 |
| SHA-2 | SHA-256 |  | Гровер: допустимо по NIST, ниже рекомендаций ECCG/ANSSI | допустимо | 16 | 16 | crates/bitwarden-crypto/src/cose/thumbprint.rs:87; crates/bitwarden-crypto/src/enc_string/asymmetric.rs:294; crates/bitwarden-crypto/src/fingerprint.rs:19 |
| CBC mode |  |  | н/п | допустимо | 4 | 4 | crates/bitwarden-crypto/src/hazmat/symmetric_encryption/aes256_cbc.rs; crates/bitwarden-crypto/src/hazmat/symmetric_encryption/aes256_cbc_hmac_sha256_ae.rs; crates/bitwarden-crypto/src/hazmat/symmetric_encryption/aes256_cbc_hmac_sha256_aead.rs |
| Crypto library | 0.10.0-rc.18 | rsa (RustCrypto rsa) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.13.2 | p256 (RustCrypto elliptic curves) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.14.0 | p256 (RustCrypto elliptic curves) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.14.0 | p384 (RustCrypto elliptic curves) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.16.9 | ecdsa (python-ecdsa) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.17.0 | ecdsa (python-ecdsa) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.17.14 | ring (ring (Rust)) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.23.45 | rustls (rustls) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.6.0-rc.8 | argon2 (Argon2 bindings) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 3.0.0 | ed25519-dalek (ed25519-dalek) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 4.1.3 | curve25519-dalek (ed25519-dalek) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 5.0.0 | curve25519-dalek (ed25519-dalek) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.10.0-rc.17 | rsa (RustCrypto rsa) | н/п | допустимо | 1 | 1 | Cargo.toml |
| Crypto library | 0.23.27 | rustls (rustls) | н/п | допустимо | 1 | 1 | Cargo.toml |
| Crypto library | 3.0.0-pre.7 | ed25519-dalek (ed25519-dalek) | н/п | допустимо | 1 | 1 | Cargo.toml |
| Crypto library | workspace | rustls (rustls) | н/п | допустимо | 1 | 1 | crates/bitwarden-api-base/Cargo.toml |
| Crypto library | =0.6.0-rc.8 | argon2 (Argon2 bindings) | н/п | допустимо | 1 | 1 | crates/bitwarden-crypto/Cargo.toml |
| Crypto library | workspace | ed25519-dalek (ed25519-dalek) | н/п | допустимо | 2 | 2 | crates/bitwarden-crypto/Cargo.toml; crates/bitwarden-ssh/Cargo.toml |
| Crypto library | workspace | rsa (RustCrypto rsa) | н/п | допустимо | 4 | 4 | crates/bitwarden-crypto/Cargo.toml; crates/bitwarden-importers/Cargo.toml; crates/bitwarden-ssh/Cargo.toml |
| Crypto library | >=0.13.2, <0.14 | p256 (RustCrypto elliptic curves) | н/п | допустимо | 1 | 1 | crates/bitwarden-fido/Cargo.toml |
| Crypto library | =0.14.0 | p256 (RustCrypto elliptic curves) | н/п | допустимо | 1 | 1 | crates/bitwarden-importers/Cargo.toml |
| Crypto library | 0.14.0-rc.9 | p384 (RustCrypto elliptic curves) | н/п | допустимо | 1 | 1 | crates/bitwarden-ssh/Cargo.toml |
| Crypto library | 0.14.0-rc.9 | p256 (RustCrypto elliptic curves) | н/п | допустимо | 1 | 1 | crates/bitwarden-ssh/Cargo.toml |
| GCM mode |  |  | н/п | допустимо | 2 | 2 | crates/bitwarden-crypto/src/hazmat/symmetric_encryption/aes_gcm.rs; crates/bitwarden-crypto/src/hazmat/symmetric_encryption/xaes_256_gcm.rs |
| ML-DSA |  |  | постквантовый | допустимо | 3 | 3 | crates/bitwarden-crypto/src/signing/cose.rs:7; crates/bitwarden-crypto/src/signing/signing_key.rs:12; crates/bitwarden-crypto/src/signing/verifying_key.rs:14 |
| PQC library | 0.1.1 | ml-dsa (RustCrypto post-quantum crates) | постквантовый | допустимо | 1 | 1 | Cargo.lock |
| PQC library | 0.1.0-rc.8 | ml-dsa (RustCrypto post-quantum crates) | постквантовый | допустимо | 1 | 1 | crates/bitwarden-crypto/Cargo.toml |
| ECDH |  |  | уязвим (Шор) | допустимо | 1 | 1 | crates/bitwarden-importers/src/importers/keeper/crypto/types.rs:515 |
| Ed25519 | Ed25519 |  | уязвим (Шор) | допустимо | 4 | 4 | crates/bitwarden-crypto/src/signing/cose.rs:70; crates/bitwarden-crypto/src/signing/signing_key.rs:10; crates/bitwarden-crypto/src/signing/verifying_key.rs:16 |
| RSA |  |  | уязвим (Шор) | допустимо | 7 | 7 | crates/bitwarden-crypto/src/enc_string/asymmetric.rs:5; crates/bitwarden-crypto/src/keys/public_key_encryption.rs:92; crates/bitwarden-crypto/src/rsa.rs:28 |

_Длинные списки здесь сгруппированы; полный список по файлам — в JSON-версии отчёта, подписанной тем же ключом._

## Приложения: Входные файлы

| Файл | Размер | SHA-256 | Маскирования |
|---|---|---|---|
| Cargo.lock | 188038 | `4d6655c6e8702d9b55b7445e9951bdfb854c1fe7703f800b1f1f15c13b6243c6` | 0 |
| Cargo.toml | 13450 | `458d82836a443814986bd34d2ac9b76d4c4c93044c7c2c442ec938b780dfc0c7` | 0 |
| crates/bitwarden-access-token/Cargo.toml | 666 | `1232f216e6943d4c628c3be66596eeaecee8f46a0e1a69464482cbc21d0937ad` | 0 |
| crates/bitwarden-access-token/src/consts.rs | 154 | `3e72f1067db1ae0a4dcd16d6bd0db196e6bc38662c4f0a1c70c1cb54ba05c669` | 0 |
| crates/bitwarden-access-token/src/kind.rs | 1952 | `a36b8431603bbf46e6ad7883f6b118b3bc583d1c95cb93f69d704e14bdd0b166` | 0 |
| crates/bitwarden-access-token/src/lib.rs | 334 | `b176a9ed3fcf937a2c5a014dcd3efc26f019506087ba1003571d449529a4dccf` | 0 |
| crates/bitwarden-access-token/src/secrets.rs | 2210 | `b35838a3b7dd6ee241bf177fc592d8bef98103322ebe2d9f8e8bd5b1cf89eb9c` | 0 |
| crates/bitwarden-access-token/src/token.rs | 12352 | `300b923e5988308122cc43739dc4700f5c6549d75767e349cbbbe1c0190a0679` | 0 |
| crates/bitwarden-access-token-crypto/Cargo.toml | 820 | `32a1c893c425b552822a428d6d55519564285fc916250a225426e8b9f189820b` | 0 |
| crates/bitwarden-access-token-crypto/src/error.rs | 555 | `379994cb68ea75e999e37736e53f09fad06b93beb2688d3b4e92da44b548e656` | 0 |
| crates/bitwarden-access-token-crypto/src/key.rs | 2741 | `6ddcf4909428c01f0c0501cf3429c92ab01a52083a1c6f1940849c8ab4153110` | 0 |
| crates/bitwarden-access-token-crypto/src/lib.rs | 310 | `e18c96eb10f8bd1e436239ed3a79e941f057b7fe9f6ab1fc8dcdcd9d6a7c0edb` | 0 |
| crates/bitwarden-access-token-crypto/src/material.rs | 2245 | `70bacab3f9b099d15a07bfc7e3eed7b2b7b59148074468adc74a60a11ea726e7` | 0 |
| crates/bitwarden-access-token-crypto/src/purpose.rs | 1188 | `3ffa4e4b9e42cec62ed0316c935b396c72c1337cfa40faafd4f234084d2d086e` | 0 |
| crates/bitwarden-access-token-crypto/src/seed.rs | 2160 | `fc40037bc578bf1cb9dfba2e3e727eb1b1bd9a970c3be2644fc55c3af47fb2be` | 0 |
| crates/bitwarden-api-api/Cargo.toml | 839 | `5f60a3e668f135ce7d1a7bc8c4be34923f2f7ab69eee519d153c032f722d2fdb` | 0 |
| crates/bitwarden-api-api/src/apis/access_policies_api.rs | 14994 | `25e051836ee4323cea0b77113edc43dc69203520d768a89f595ccea34894b4e7` | 0 |
| crates/bitwarden-api-api/src/apis/access_requests_api.rs | 7758 | `b51fd9afcfe7b91ae9f3c7f33a751a23486e07e4f77b92ea4a283fb0118af3ab` | 0 |
| crates/bitwarden-api-api/src/apis/access_rules_api.rs | 7387 | `e9e56416549740e9741f53e51e7f17784a3538210ba51811dec68b4e2359b842` | 0 |
| crates/bitwarden-api-api/src/apis/account_billing_v_next_api.rs | 13231 | `5478149ccb81a14630244b65c7d4134fe0eff1f87e14e611a492444f58e3cb79` | 0 |
| crates/bitwarden-api-api/src/apis/accounts_api.rs | 32983 | `82489b0b32d2eaa4b8b8b03ba2d34694f9252689510a2fbb870eaa0043cc92e0` | 0 |
| crates/bitwarden-api-api/src/apis/accounts_billing_api.rs | 4237 | `0137f267b0143ccd35bc354fe63f98f62a56878827dd802dd11f4b7af71b1464` | 0 |
| crates/bitwarden-api-api/src/apis/accounts_key_management_api.rs | 10876 | `f4fa5f8052952b5768795b6110b11ad3a013cb05fe3a64df0e8495f035b3d15e` | 0 |
| crates/bitwarden-api-api/src/apis/audit_api.rs | 8866 | `0c56709e031a3144a8d8b1aa383e9514ad19d6cc88f9ec9eac3e33b389d240a0` | 0 |
| crates/bitwarden-api-api/src/apis/auth_requests_api.rs | 8031 | `4cd3e4b790af4e79d349134a66277328f9f07ba0540ea8645d827c8403dc794a` | 0 |
| crates/bitwarden-api-api/src/apis/cipher_lease_api.rs | 4084 | `78ada026bb080745b5335e16387afa32bc60238840b2a6f6eac097a9dffa4642` | 0 |
| crates/bitwarden-api-api/src/apis/ciphers_api.rs | 50427 | `ebc1215b1ef2b696e327e2efb3f6c56ba2db36473f817590b0d259911b0060d7` | 0 |
| crates/bitwarden-api-api/src/apis/collections_api.rs | 14992 | `04ed284ed2415030ec4d973b61377bd74d2331a2c3671b17a32d45dfe4858dd4` | 0 |
| crates/bitwarden-api-api/src/apis/config_api.rs | 1806 | `d37d3536df8f5ee82ddbc443a9c6d736dd87ec57af09a209f3efd7f405eb2ae4` | 0 |
| crates/bitwarden-api-api/src/apis/counts_api.rs | 4091 | `d1f7ff926beaea10d879cc4a295cc174adfa95e8342a94ec5e8d99215e3c9702` | 0 |
| crates/bitwarden-api-api/src/apis/devices_api.rs | 14725 | `baa0561004b24d410c63c678b7467f88d76dbace35855f587713d78aaad3a452` | 0 |
| crates/bitwarden-api-api/src/apis/emergency_access_api.rs | 17777 | `7d903abeb04bd3523a8ea3390a9e7040c1c6222a8c4ea0a246186e9909deba14` | 0 |
| crates/bitwarden-api-api/src/apis/events_api.rs | 18623 | `f1a69150512d4f176e521e3fe493555a4ff01433d64c80c04ff5a2d496adad9c` | 0 |
| crates/bitwarden-api-api/src/apis/folders_api.rs | 7108 | `c2e21fe891911a0d63f73bb1361681a280f5a7a09593e480b01ee3f6d37fbf19` | 0 |
| crates/bitwarden-api-api/src/apis/groups_api.rs | 11350 | `ff745a4b7826c7f2d69384edf810d4af9fa0cf9a0e318964473759523c4b7e57` | 0 |
| crates/bitwarden-api-api/src/apis/hibp_api.rs | 1987 | `fde68c001c947f363c2bcfd69d160c2dafbf8a63eace0fc454b1e3740f91751b` | 0 |
| crates/bitwarden-api-api/src/apis/import_ciphers_api.rs | 3556 | `2ff739be344592b91bd9710430ba3b95e4f2dc3a60481ce03a31a2b84e41fde9` | 0 |
| crates/bitwarden-api-api/src/apis/info_api.rs | 1748 | `6dc7d3d6e7e8fc2752d7a48a1d4a9be25bcb60e544ed343de869fa55cc35e137` | 0 |
| crates/bitwarden-api-api/src/apis/installations_api.rs | 2960 | `d519272bd42fadfa9c19d86f84f97a05ff7faefb83c805c73a72e8d3b6456b85` | 0 |
| crates/bitwarden-api-api/src/apis/leases_api.rs | 5645 | `ca951f5ef1639a30bbc48ab67342f8d24c70a74db6b41621edb60ed1ddd9a9d0` | 0 |
| crates/bitwarden-api-api/src/apis/licenses_api.rs | 3526 | `59d9b8373bdee8fe6a2dc6e03ddd1dda3a6a0d2da6ad097bd6d0764a3bbb648e` | 0 |
| crates/bitwarden-api-api/src/apis/mod.rs | 56272 | `fd173c24409f5b1cfc34d29d9b1e04ec2f84f384ceb38d5c9ebc15a4a4426ef3` | 0 |
| crates/bitwarden-api-api/src/apis/notifications_api.rs | 4647 | `11c796cd5c01c9178709312e9b85701b4af47b81a2b440d7ab713dee8f21f7a6` | 0 |
| crates/bitwarden-api-api/src/apis/organization_auth_requests_api.rs | 6145 | `1cc320b5bd8371b96d514dd0709b83047e4e6d1b51bee9f81c4b9535ef06b019` | 0 |
| crates/bitwarden-api-api/src/apis/organization_billing_api.rs | 8071 | `b9fb9aed89ec1f56051c26d86c108a210bb4a065585b6f643c1cb3d6c5265154` | 0 |
| crates/bitwarden-api-api/src/apis/organization_billing_v_next_api.rs | 14736 | `0598e826f32391ec8c825c3d24dce7d4343d912c723924f9fbe8cdff49a368c7` | 0 |
| crates/bitwarden-api-api/src/apis/organization_connections_api.rs | 6593 | `790fa8b2ef98fee732e7fa067f871ebc56573521c755cf6a42c34eb11d1a2983` | 0 |
| crates/bitwarden-api-api/src/apis/organization_domain_api.rs | 8528 | `74af5dcdc87e452c635990163d2193236f0065ea8ac9701066f701fd199ded04` | 0 |
| crates/bitwarden-api-api/src/apis/organization_export_api.rs | 2015 | `f7e3180af67570b536dd9f57c73bd39d2266ac4213ab788358b4840c2589d17a` | 0 |
| crates/bitwarden-api-api/src/apis/organization_integration_api.rs | 6003 | `94993c4e5187b44ad2321bac365a9f70bb705c602bf49711c5be230ae16065dd` | 0 |
| crates/bitwarden-api-api/src/apis/organization_integration_configuration_api.rs | 7152 | `b31d2437f55069e5bea4c0c019dc008fe3a05ab96f002776b86246354a1bc029` | 0 |
| crates/bitwarden-api-api/src/apis/organization_invite_links_api.rs | 12349 | `176f62f60faa56075e1b33e834874e6a317f1c4c2f17ab007616e1590b524c72` | 0 |
| crates/bitwarden-api-api/src/apis/organization_reports_api.rs | 18511 | `9bd6e3a1de829ca280601dd9206a4a1209715ec1bb09318d94db3aa12dd7586e` | 0 |
| crates/bitwarden-api-api/src/apis/organization_sponsorships_api.rs | 12972 | `9f69cd5eda377f9ff7127973c29699ef9577e161766747be11b47a473a3d17e2` | 0 |
| crates/bitwarden-api-api/src/apis/organization_subscriptions_api.rs | 5309 | `a6441cd528fe43eb39860eb9a5ae01c740e5057a2f514e19db26baf1e411e7ea` | 0 |
| crates/bitwarden-api-api/src/apis/organization_users_api.rs | 45279 | `acc511cbfd2dcc13eda49841a39923d136c9561b163c3145ec43a62b333a0b94` | 0 |
| crates/bitwarden-api-api/src/apis/organization_users_keys_api.rs | 5826 | `1c806716c9d8fd6c33c1327102cd0a3d647f6b4fcfb81bf88013285e40419657` | 0 |
| crates/bitwarden-api-api/src/apis/organizations_api.rs | 32008 | `ec453a13d360c42f33f049afeecce1fd63039524aa5cdffc3a3ec437d97bc00c` | 0 |
| crates/bitwarden-api-api/src/apis/pam_access_connector_rotation_attempts_api.rs | 8344 | `5cf57ef36d81466fc5b8ed6f1d8cc6fc50ac3d0d5743c81f5d205032472a8fa1` | 0 |
| crates/bitwarden-api-api/src/apis/pam_access_connector_rotation_configs_api.rs | 11101 | `00215505cb0a6402003df0d11dae97b652a9ac3507e778ebfd54e678425b27fd` | 0 |
| crates/bitwarden-api-api/src/apis/pam_access_connector_rotation_jobs_api.rs | 4840 | `8525a014554da8ffb8dda1635c3ce7e3193aef4b767895e6f30946fb1d307f54` | 0 |
| crates/bitwarden-api-api/src/apis/pam_access_connector_rotation_target_systems_api.rs | 7650 | `8c96d524079b388453eb4d0f995290d6a9c3d8c9c1e671f9204bb18c044b249d` | 0 |
| crates/bitwarden-api-api/src/apis/pam_access_connectors_api.rs | 11293 | `5ddc2f863a45b7b58b63afcde63a328dea331d5716b74afe232913dbc841465e` | 0 |
| crates/bitwarden-api-api/src/apis/plans_api.rs | 2495 | `ddbe0111d48f00a1901f65f3ca394797709a21eacfbfaed58efc3261de4a75f0` | 0 |
| crates/bitwarden-api-api/src/apis/policies_api.rs | 6936 | `89e16dc7ebb0d31d770fa1024dd7fbc7ad7a70fc2f7af5631979c083da97cba9` | 0 |
| crates/bitwarden-api-api/src/apis/preview_invoice_api.rs | 8069 | `15f1a4e391d47108f0f030aa39d9ea934b91eb7ee39194f592030c0a390e96b3` | 0 |
| crates/bitwarden-api-api/src/apis/projects_api.rs | 6252 | `aac218a63798c3d3e6d0c6caac84543f217a53c0f7be33c5b2bb1318dbe4bf47` | 0 |
| crates/bitwarden-api-api/src/apis/provider_billing_api.rs | 3952 | `c40f1ca32ff30387112f13780601fbec7bb084b6bb330b38dbaeb2a67471c3b7` | 0 |
| crates/bitwarden-api-api/src/apis/provider_billing_v_next_api.rs | 8343 | `5e7636cd9618729686a5e41d2bcd8ef4cd61bc0827aa786563c7012841ca821c` | 0 |
| crates/bitwarden-api-api/src/apis/provider_clients_api.rs | 5934 | `8914a2043fc5b8647306d2edb871f24fd53cc34c439270bbcca4d1a9d3b36e84` | 0 |
| crates/bitwarden-api-api/src/apis/provider_organizations_api.rs | 5702 | `3ff1cff07f97f174a9ef8150fbbe45d8bcd1aef53fd7de93beccc9b17bae1449` | 0 |
| crates/bitwarden-api-api/src/apis/provider_users_api.rs | 15007 | `d92dae9762b86ce19d4151dae2f632f8611573748928251cdf8efd515dd94b17` | 0 |
| crates/bitwarden-api-api/src/apis/providers_api.rs | 6493 | `dc4e021782ef8ddc0c7dd4e531b57fdf25c254ef9b6faff1dc908419634c5045` | 0 |
| crates/bitwarden-api-api/src/apis/push_api.rs | 6006 | `0e4935f8ca6d350f9114d9279025f9d367785a53fedf0b7d664d07d35acb4931` | 0 |
| crates/bitwarden-api-api/src/apis/reports_api.rs | 7566 | `90eaad53eb98b8e39d98ce8bf7ac8ff20b495e1d58b6268db6bed447a9b4cf7b` | 0 |
| crates/bitwarden-api-api/src/apis/request_sm_access_api.rs | 2230 | `cbbc19d6297aa17cffcfa1c5c709d49494e884bd6042d64542bda60a6b658b59` | 0 |
| crates/bitwarden-api-api/src/apis/secret_versions_api.rs | 6283 | `694ceec13c97a723fc51ccdcf9e8d1422effd736e3d7d7751bbf7fb9e3dce98c` | 0 |
| crates/bitwarden-api-api/src/apis/secrets_api.rs | 9548 | `74d910f6feb9433ace5a166084e4a7d8f6299666f1328b8e268d61cc9684dcd8` | 0 |
| crates/bitwarden-api-api/src/apis/secrets_manager_events_api.rs | 2984 | `1f48dc2535f862d7572623f04e4ec5ff08f6915ad4b47b0d4bbc673088dbccce` | 0 |
| crates/bitwarden-api-api/src/apis/secrets_manager_porting_api.rs | 3217 | `b44d71d1ec7c8755601095e0560b1dae0610707f0a33c90cc20618cc4989cfcf` | 0 |
| crates/bitwarden-api-api/src/apis/security_task_api.rs | 6747 | `b64d512d595b73a315324dc71fdf9fe3bc0810cc1fae7765bb0ef4b4d97ed824` | 0 |
| crates/bitwarden-api-api/src/apis/self_hosted_account_billing_v_next_api.rs | 2254 | `7beb98619fef6f1c4d8c000a3b9d5dae708eea2bd82d8b73459b82af5cb32619` | 0 |
| crates/bitwarden-api-api/src/apis/self_hosted_organization_billing_v_next_api.rs | 2177 | `8074aa50accb63d845d3ff24b074d20c583ff8badc74cec3cc14403fbd9399b7` | 0 |
| crates/bitwarden-api-api/src/apis/self_hosted_organization_licenses_api.rs | 5250 | `0fc3c55f3843bc2afaec2a00aa34d3707569674dc720ba978b940da5d7c88667` | 0 |
| crates/bitwarden-api-api/src/apis/self_hosted_organization_sponsorships_api.rs | 5877 | `639d78082862a06d6f2be7297cdc9fcfc3ac2e97c5b5976ecaa3eaf5af53089a` | 0 |
| crates/bitwarden-api-api/src/apis/sends_api.rs | 12905 | `f58e027a2335283775495d2ca9f605d7bf00a945e170fb8f1e5f62aca30b08f2` | 0 |
| crates/bitwarden-api-api/src/apis/service_accounts_api.rs | 10297 | `0dd575cba1f0ed90e27ac25b41f3a92acbb4daf49cf6f6430b518b2e9ccad1a2` | 0 |
| crates/bitwarden-api-api/src/apis/settings_api.rs | 3144 | `b0d1d022c6016f6a21306ce0f31288a6e62de0c8fe2ca2585ad0b7e7df95760d` | 0 |
| crates/bitwarden-api-api/src/apis/slack_integration_api.rs | 3255 | `880d1b1a15508dd6ef4d9187cc90a23fdb4cc8b0d4c8005b1f02435bb617cd98` | 0 |
| crates/bitwarden-api-api/src/apis/sso_cookie_vendor_api.rs | 1808 | `096210376d597184f249a33c17eebf8fbfb99edfdc4b1ed07482824a65b2463a` | 0 |
| crates/bitwarden-api-api/src/apis/stripe_api.rs | 3599 | `4548a5df6f41789806119e88ab91ba9c67751df8d90a74635af942e19b529752` | 0 |
| crates/bitwarden-api-api/src/apis/sync_api.rs | 2085 | `f9a16e0669f91906a6e7d8624448c4d12fc3432b589889a19a60bf0ed81d2c08` | 0 |
| crates/bitwarden-api-api/src/apis/teams_integration_api.rs | 5222 | `1ab435db5bcd7c593541f78d32f5bcfdaccf53b9d6504b0f8fe76beba9fd6bbf` | 0 |
| crates/bitwarden-api-api/src/apis/trash_api.rs | 4315 | `becd20628f6a879cd6d91b8b51969a87f038e512a6f9abd770ff766eee777ffa` | 0 |
| crates/bitwarden-api-api/src/apis/two_factor_api.rs | 27883 | `988fa4d1b7b664bdafc892df9a8897f8dc477ce1ba6599731d7e2a32d2c942fe` | 0 |
| crates/bitwarden-api-api/src/apis/user_subscriptions_api.rs | 6717 | `3b59cb9fdbe1be600017e964ff9116741268e4f56b8fb11bd0e3696e04902191` | 0 |
| crates/bitwarden-api-api/src/apis/users_api.rs | 2864 | `f5d35e4d821eea56fb98468de65edb70c6032774b9a6dc418558ad32050e44b2` | 0 |
| crates/bitwarden-api-api/src/apis/web_authn_api.rs | 7558 | `8385c97149f0025888a454a5332a20831ce7488e0d4bfa3ccd06eacccce6fcc7` | 0 |
| crates/bitwarden-api-api/src/lib.rs | 403 | `5ba8a4fbb91deec0ab29a266a43817d2552c61d1c926791c60008d24846f396b` | 0 |
| crates/bitwarden-api-api/src/models/accept_organization_invite_link_request_model.rs | 1124 | `fa196bf0eb0dad232ca4e083feb06fe086f3faa01edc7c73353f319736cedd2e` | 0 |
| crates/bitwarden-api-api/src/models/access_approval_mode.rs | 2842 | `38b8f4b35cff87c42955c646b0c1b23b10e0acdf1de6553810201e39d174cdf9` | 0 |
| crates/bitwarden-api-api/src/models/access_audit_event_response_model.rs | 7708 | `9a842fc3fc416ab83ecbea2484e498313d5528ba163ef2cccc900b304f9423c1` | 0 |
| crates/bitwarden-api-api/src/models/access_audit_event_response_model_list_response_model.rs | 1246 | `53c4c9b0b4cd452d26f5c636739edf0ea0a18c66ac9b09030189ef9f029dd215` | 0 |
| crates/bitwarden-api-api/src/models/access_audit_item_response_model.rs | 2265 | `4e907a80af5a1b796187f2f9268fb4d6cfe4489146ab49dc01d0871a7973478a` | 0 |
| crates/bitwarden-api-api/src/models/access_audit_item_response_model_list_response_model.rs | 1241 | `e061fad190b76be9867b74118e0e3c4b85ca90463c135514362dc28aa4acdc4d` | 0 |
| crates/bitwarden-api-api/src/models/access_decider_kind.rs | 2258 | `dffff10028723ff6d598defdc7033cc547b2f1dc3556a79f37ca9ac5f712f8a6` | 0 |
| crates/bitwarden-api-api/src/models/access_decision_request_model.rs | 1253 | `d5fd6b5aa1234bd52135466371a3b6a3674ffa8b08a84dcd5066f707a3eeb1f6` | 0 |
| crates/bitwarden-api-api/src/models/access_decision_verdict.rs | 2296 | `d382a6f0fac983c97688b700f0ad751bd3257db4dfde931cd7715da297bb8bdb` | 0 |
| crates/bitwarden-api-api/src/models/access_lease_extension_request_model.rs | 1564 | `5a01f6586e36242eb25e32786f29dcda598c883c1fe44bb0f6962714eb08d570` | 0 |
| crates/bitwarden-api-api/src/models/access_lease_response_model.rs | 4819 | `119ef397e26291c1ccd85fbd79842ca95ef7477ee463c9c474576a091cfa7544` | 0 |
| crates/bitwarden-api-api/src/models/access_lease_response_model_list_response_model.rs | 1221 | `3c9a8db2a7d20effad679278032db64b09434088f67a98b16668a338f4e21e77` | 0 |
| crates/bitwarden-api-api/src/models/access_lease_revoke_request_model.rs | 968 | `bd51bd15cda5e22cb09c7b54c49e89ca4a70ef7a8999751a3255da08d174ab93` | 0 |
| crates/bitwarden-api-api/src/models/access_lease_status.rs | 2412 | `796745dc73dbd6dde3fa5419c1ffad404f1833722f22064c7d3b68ecead8c581` | 0 |
| crates/bitwarden-api-api/src/models/access_policy_request.rs | 858 | `031cb2273ae92b67158fe40286935a907131b6dc8b18816177c41120bfafcdb2` | 0 |
| crates/bitwarden-api-api/src/models/access_pre_check_response_model.rs | 3691 | `6531c4cf8d4e541bb07897973611ca192e63285e81581eea205e79e8df6a05bb` | 0 |
| crates/bitwarden-api-api/src/models/access_request_create_request_model.rs | 2720 | `0f1ae062b33dd195d03d24dd2dcf88ae4e9225d36573e35d9202966dbcf48ff5` | 0 |
| crates/bitwarden-api-api/src/models/access_request_decision_response_model.rs | 4024 | `fd1efc3818b5765ba4187bc10e96a572c65add8c4060b4c2ea17e177b580e8f4` | 0 |
| crates/bitwarden-api-api/src/models/access_request_details_response_model.rs | 6984 | `69afff67849e04a086ba753959cad63e9473fa8dd65be27f691fc19207ce91fb` | 0 |
| crates/bitwarden-api-api/src/models/access_request_details_response_model_list_response_model.rs | 1266 | `71d51fb9d8ec53de9f9f0b3d1a48c557cc253e90b129b3720f2cfbc8b0c0ab6a` | 0 |
| crates/bitwarden-api-api/src/models/access_request_result_response_model.rs | 1385 | `aedb3c0311902079a9e18afac55512022767779265720f6d01eac78e1cf13f95` | 0 |
| crates/bitwarden-api-api/src/models/access_request_revoke_request_model.rs | 1070 | `1c2cba17f3b42a92b541766c7d32edf77865c618f7c3856ad1da545bbe4db1af` | 0 |
| crates/bitwarden-api-api/src/models/access_request_status.rs | 2519 | `14002d4ee6c94ddf9a03fd99874b10871cccf1371a23efd9cf03fcf363c8ef88` | 0 |
| crates/bitwarden-api-api/src/models/access_rule_request_model.rs | 4373 | `c7bdbe67764cd05812ca9f2c17ece583cdac5f162dd279767cc0bc32486cc298` | 0 |
| crates/bitwarden-api-api/src/models/access_rule_response_model.rs | 5269 | `109b2c399fe652067bca360d28e0b1f09f2bb67c7d06eb4fb7d7773b0e117fff` | 0 |
| crates/bitwarden-api-api/src/models/access_rule_response_model_list_response_model.rs | 1216 | `62838e8684447ff3d34861d3bd2a4617db291a11ce51315fd44d95b02fb70243` | 0 |
| crates/bitwarden-api-api/src/models/access_token_create_request_model.rs | 1143 | `0d5dcc48192f0bdbc1a4417b75024d9edfab3df9ac7867670c44fd7b260a2a50` | 0 |
| crates/bitwarden-api-api/src/models/access_token_creation_response_model.rs | 1870 | `8c2f64fa38e03fc72c06db8bd0b6e6d2ede36e72203a1b901adee2ae036a78cc` | 0 |
| crates/bitwarden-api-api/src/models/access_token_response_model.rs | 1817 | `3d1999621d3a417dae7775a7bcb36ce790bc4ffa89ffcf4032ca6c3b4b0eb058` | 0 |
| crates/bitwarden-api-api/src/models/access_token_response_model_list_response_model.rs | 1347 | `7f7d8bc3a43f6e1a73a0e71c5ee64a34b67e4da338f96c3a86c865cc86aaeadc` | 0 |
| crates/bitwarden-api-api/src/models/account_data_request_model.rs | 1137 | `fdd7bffa95e7c159baea37510e7a0955a69203b8d6479acdcf9f2f217f78d336` | 0 |
| crates/bitwarden-api-api/src/models/account_keys_request_model.rs | 1848 | `74cee8e4f6502a7bdbf0ddbe9a9666925ff6efde1335baf6f1aa4afd080df84f` | 0 |
| crates/bitwarden-api-api/src/models/add_existing_organization_request_body.rs | 841 | `8726316e6bddc5c88835043223b4a6818f09d456efcde1b2d45914b3457f3693` | 0 |
| crates/bitwarden-api-api/src/models/add_organization_report_request_model.rs | 1838 | `1401b5bf28e9fe9b61d876b87836d9d061104cbdf409b1f924a025439fedf80f` | 0 |
| crates/bitwarden-api-api/src/models/admin_auth_request_update_request_model.rs | 962 | `cc4ed55bb8c857f369083122619f0bf2656ad1061829725db51d411cf1e086b4` | 0 |
| crates/bitwarden-api-api/src/models/algorithm.rs | 2899 | `d561c6ffc9daf5a28f448b33656be3ed66fb73a3024c2b1ec05f0b1046409258` | 0 |
| crates/bitwarden-api-api/src/models/api_key_response_model.rs | 1092 | `5ca81765e5b9c8258e307d40d4cc581aff673d43210ebe3b590c93f9e6c0a667` | 0 |
| crates/bitwarden-api-api/src/models/assertion_options.rs | 2181 | `3d29d975f41b7d2605654ea1da2f9196a85942f77210abc3347c668d21daae79` | 0 |
| crates/bitwarden-api-api/src/models/assertion_response.rs | 1819 | `2e595f472f8ccdbb6c2c8d68dbc05e3ba6c760ec3659740624923bdb4981cdaf` | 0 |
| crates/bitwarden-api-api/src/models/assign_access_connector_target_request_model.rs | 1317 | `d50e3451f6f9eac7c92248b0de8d4583b70aea3b2f1f1c3626a3e0abb71677be` | 0 |
| crates/bitwarden-api-api/src/models/attachment_request_model.rs | 1583 | `2dbaa64db8ecf99d711ba5146570a79d1d3acdfed116f678d718fdaa515c425f` | 0 |
| crates/bitwarden-api-api/src/models/attachment_response_model.rs | 1678 | `f0dc96cf6cf42108c017807e29e5c4722488c6e24842f7f30c31d0cc21f06fe8` | 0 |
| crates/bitwarden-api-api/src/models/attachment_upload_data_response_model.rs | 1835 | `eb11d5059c1d0874cf87960488ede6ad941a1f18e08dce5458b3e899a7e53b8b` | 0 |
| crates/bitwarden-api-api/src/models/attestation_conveyance_preference.rs | 1327 | `765356f64153bb3f833dcd39e2c84d44c1f9413b9b74a0612c0a12ec9ae1854a` | 0 |
| crates/bitwarden-api-api/src/models/attestation_response.rs | 1408 | `c631bf23162ff780d401408b56555821c367c68033f2b51a13c30513419609e5` | 0 |
| crates/bitwarden-api-api/src/models/attestation_statement_format_identifier.rs | 1654 | `a034ccc5eabe6375ffd51ebe3448638c05e4944395a9134187a1f963ead743c3` | 0 |
| crates/bitwarden-api-api/src/models/auth_request_create_request_model.rs | 1283 | `d8fdaf56a71663fa721fb42bffd10afadf805937edfd7fdf3dfa1344069aa094` | 0 |
| crates/bitwarden-api-api/src/models/auth_request_response_model.rs | 3421 | `ecb4292a5cdf713a8fa55d4efaadf0f674ab7127053551e705e6982ae55b5f03` | 0 |
| crates/bitwarden-api-api/src/models/auth_request_response_model_list_response_model.rs | 1347 | `6a58bc70eb72208e9cbbc358516cefe146534acd5326ad4c9ddd2dc562720dc4` | 0 |
| crates/bitwarden-api-api/src/models/auth_request_type.rs | 2378 | `0d12d99160c0eb3a734a0242c3cd0b5117b11e5af3bee188004a98c21cd5a02e` | 0 |
| crates/bitwarden-api-api/src/models/auth_request_update_request_model.rs | 1250 | `e4f17a0f65b87c69d395cb17a76ad6a21487b9f28f165acd3a286fe344107d73` | 0 |
| crates/bitwarden-api-api/src/models/auth_type.rs | 2343 | `25f0ff7dd0b1dcf07f2ef353da0296a75c4a29cafb14cacc869c80dbef9a9063` | 0 |
| crates/bitwarden-api-api/src/models/authentication_extensions_client_inputs.rs | 2327 | `832d590a5e0a25af1ae7546c2c4dca2dd598f6eef5a5e00c64ee3a9b747209be` | 0 |
| crates/bitwarden-api-api/src/models/authentication_extensions_client_outputs.rs | 2204 | `ae838d06788bff76b31cccf6a23bc0580cfbf8d395211aefad363c8b9099a8e9` | 0 |
| crates/bitwarden-api-api/src/models/authentication_extensions_large_blob_inputs.rs | 1324 | `e022a7e8c1223c07aebb122e326f73d1be2732dfcbeca0097a0759e55fac728d` | 0 |
| crates/bitwarden-api-api/src/models/authentication_extensions_large_blob_outputs.rs | 1324 | `b335d32d487ba5753b99aa8d57ec7eda84d76e91352398d67617145d40abb3a1` | 0 |
| crates/bitwarden-api-api/src/models/authentication_extensions_prf_inputs.rs | 1083 | `a94ca44d5502752bfcabdc20e32287bf2ebb2c9cb8b01a684cea6203c4128515` | 0 |
| crates/bitwarden-api-api/src/models/authentication_extensions_prf_outputs.rs | 991 | `6f6004ffa0837f129fad604b47d71504c274d6e6a350018dec855fc017eba6ca` | 0 |
| crates/bitwarden-api-api/src/models/authentication_extensions_prf_values.rs | 1188 | `86a05c02aa7d035babede462d1ff84c0c65211fa2d4a98d984bc71a4bc6b8453` | 0 |
| crates/bitwarden-api-api/src/models/authenticator_assertion_raw_response.rs | 1906 | `cc14b886b0cfb0c08311c2e478350b577fbdb830c5636bed14d8f36d252ec228` | 0 |
| crates/bitwarden-api-api/src/models/authenticator_attachment.rs | 1135 | `9288295f8650969c74283d8ac493c2cc77ccbe2b53ab265f52883f28d96f4cc4` | 0 |
| crates/bitwarden-api-api/src/models/authenticator_attestation_raw_response.rs | 1898 | `69041299c03b0c840599b152d62e7636b0c74b121c054eabb14d321dce156d6a` | 0 |
| crates/bitwarden-api-api/src/models/authenticator_selection.rs | 1517 | `3a3fb4b89e8b765208a4fee2e90de36e5b5d480aba9783f038736a2e75278637` | 0 |
| crates/bitwarden-api-api/src/models/authenticator_transport.rs | 1446 | `1467fca07fb4fcc0d07ed196a8c4c5da7166588501fac7835b976a20b7494511` | 0 |
| crates/bitwarden-api-api/src/models/base_secret_response_model.rs | 2189 | `5a83e0511173c59a7ef5731617d5c6668e8875d1b529800ca1f74b4c8e82207a` | 0 |
| crates/bitwarden-api-api/src/models/base_secret_response_model_list_response_model.rs | 1341 | `7ec65bed519d1232031ed15e51bd9927d58b9019c6216ffcaef5029769f2aacd` | 0 |
| crates/bitwarden-api-api/src/models/billing_address_request.rs | 1673 | `0edecc57d64323a11e99a7c888ee59c7a2b1ce31e3d23aa36eeaf83fca16dca4` | 0 |
| crates/bitwarden-api-api/src/models/billing_address_selections.rs | 1125 | `9236d9ae8c1f3fa945fb55307e11a6fb65149b2f8f47f69469dcc2b27c812fba` | 0 |
| crates/bitwarden-api-api/src/models/billing_customer_discount.rs | 4066 | `3326ab9498d2f0b0d624adcd875e582b4c04d46f8b627beefa32c7257cb387bb` | 0 |
| crates/bitwarden-api-api/src/models/billing_history_response_model.rs | 1174 | `d5f752f5edbc971b3bdf3a06b5999adf30f89ff57340819acdea6db3b5a3fc6c` | 0 |
| crates/bitwarden-api-api/src/models/billing_invoice.rs | 1520 | `f6187aca2fcfa2b4a955c0222a8a5ec482de9034c7279a8a3de42315dbcbac63` | 0 |
| crates/bitwarden-api-api/src/models/billing_subscription.rs | 3249 | `22672b8d7cd32813468dafcd867200cd505babf3c3fa735f616b3ae4aa1b0b3c` | 0 |
| crates/bitwarden-api-api/src/models/billing_subscription_item.rs | 1952 | `d52416dd4480cf0d6fdfdd0527af703bd0af16d352205adadc6559bcd3a53468` | 0 |
| crates/bitwarden-api-api/src/models/billing_subscription_upcoming_invoice.rs | 934 | `c0785e752f00776dbf48837318216b536bce1baeac1e40b68e3b7276192340b2` | 0 |
| crates/bitwarden-api-api/src/models/billing_transaction.rs | 2141 | `3c828ffe4b71bc46e31d666689d149ffc9a61a9d16570123997a9fcd942987ee` | 0 |
| crates/bitwarden-api-api/src/models/bit_pay_credit_request.rs | 767 | `f03da4efead7e64da41c01f994a52d0fe46cbc4037a19b910f9f99b54ad2e771` | 0 |
| crates/bitwarden-api-api/src/models/bitwarden_discount_type.rs | 2437 | `3119eee204766f8b49e597213e1c3d0b56627128831a5e8d34a1de6ce1fca7bb` | 0 |
| crates/bitwarden-api-api/src/models/bulk_collection_access_request_model.rs | 1223 | `1e7cbf1e9eea53b0693ee323b6c2922da0b13aa6ff37f4f576f2bbccdf5cfa96` | 0 |
| crates/bitwarden-api-api/src/models/bulk_create_security_tasks_request_model.rs | 777 | `07e87ed85a18a6dcdb25fa3b8b73c60c588cef47a2a35e329eba9f1fd5ed9fe6` | 0 |
| crates/bitwarden-api-api/src/models/bulk_delete_response_model.rs | 1034 | `3a96386c4810f4e448fe1a2a749acf3c25f8ee55dbe6565c04a4e8374f730674` | 0 |
| crates/bitwarden-api-api/src/models/bulk_delete_response_model_list_response_model.rs | 1341 | `66601ba1f760f4a109df41f486e18fd74bda22668a4b18491472319a2b289e67` | 0 |
| crates/bitwarden-api-api/src/models/bulk_deny_admin_auth_request_request_model.rs | 720 | `75bb83df4e0a20dbf2c4ded475ac82c844e6419975bf9fec073c045a71406b17` | 0 |
| crates/bitwarden-api-api/src/models/change_kdf_request_model.rs | 1446 | `80b1c21f28e765a97d7f2e2c756289b4be44f2d16e8b947f813b51f3ebc985d9` | 0 |
| crates/bitwarden-api-api/src/models/change_plan_frequency_request.rs | 693 | `ede7b3b0424858215eb541b149534cf3279d937ac13fd76d1040e98741e93020` | 0 |
| crates/bitwarden-api-api/src/models/checkout_billing_address_request.rs | 1009 | `13de9f6a451634848e0c0421343575df91e0c53c1bd45a4be9b59b45c4d16fef` | 0 |
| crates/bitwarden-api-api/src/models/cipher_access_state_response_model.rs | 3133 | `24b501541c966484f9eda4fafa4f141dd3b1265be702617bb697711567aec264` | 0 |
| crates/bitwarden-api-api/src/models/cipher_attachment_model.rs | 861 | `b92fe2198cf0d9b875bbb48e58cefb6fe983d53d75397aa7dc7883156ebc5c5a` | 0 |
| crates/bitwarden-api-api/src/models/cipher_bank_account_model.rs | 2487 | `64fc23495dd4a4025134e02c6526060b492cfbbfe50b7af774ead087fb7fe38e` | 0 |
| crates/bitwarden-api-api/src/models/cipher_bulk_archive_request_model.rs | 657 | `c9840151c1a43eaaa2658fc2a3d770dc4e171ecd87dd950f5380b664ac9d418a` | 0 |
| crates/bitwarden-api-api/src/models/cipher_bulk_delete_request_model.rs | 879 | `d797a92af875c64313787570aeef6c2408ea549d6534f73551d1a98c56e52906` | 0 |
| crates/bitwarden-api-api/src/models/cipher_bulk_move_request_model.rs | 847 | `2dac822c3d3246d97b77cc041c1219b386a182d77bcd885fcc03c654a90fa29e` | 0 |
| crates/bitwarden-api-api/src/models/cipher_bulk_restore_request_model.rs | 887 | `a02d6b1922ec999dbc18841f04ed8aa284400debc6c27cba1ec83eb14df30fbc` | 0 |
| crates/bitwarden-api-api/src/models/cipher_bulk_share_request_model.rs | 915 | `1934cd882e71e5d4dd724b3f7f3b62c781b6bbd0241b7c8ba7925547dcd582c8` | 0 |
| crates/bitwarden-api-api/src/models/cipher_bulk_unarchive_request_model.rs | 665 | `54328ce13004b6b55d9f81bfc40216eb26b722b1aa91ac4a9ad156a254b1e1c7` | 0 |
| crates/bitwarden-api-api/src/models/cipher_bulk_update_collections_request_model.rs | 1565 | `980e7badb98ecfa18693851ada4b667cdff42b363d77d3f5b2b1412a01ed4153` | 0 |
| crates/bitwarden-api-api/src/models/cipher_card_model.rs | 1623 | `c5ab6b794f0690bda1f418cfebca971f7d44e557f16952e40b439e13e4651d4e` | 0 |
| crates/bitwarden-api-api/src/models/cipher_collections_request_model.rs | 702 | `8ba0e5bd8d80fd80609bc2a599c8da09d8b3f073fcab0ce751ef48a2a75c2e5c` | 0 |
| crates/bitwarden-api-api/src/models/cipher_create_request_model.rs | 936 | `5d459d552d67d48c162e44da169adc37bb6b400e86cf103ff5dad8def0cc0191` | 0 |
| crates/bitwarden-api-api/src/models/cipher_details_response_model.rs | 7363 | `f7cef05b72b8f0aad720ce4a31067980c801710d4d138fa9507dab8257579c9d` | 0 |
| crates/bitwarden-api-api/src/models/cipher_details_response_model_list_response_model.rs | 1359 | `877bde831f452b11fb5a9cf81b9b85d162f2a3de83f026199f11a0e9f4aebd7e` | 0 |
| crates/bitwarden-api-api/src/models/cipher_drivers_license_model.rs | 2792 | `3ce72f52aa4ec37af8fd0f9452e2ac6a96643db7f13b96235192364d5a5ac725` | 0 |
| crates/bitwarden-api-api/src/models/cipher_fido2_credential_model.rs | 3014 | `11dbe60735596b2c3fb2a3e41f7a4d048bc5acc4e1ed05b14a7e6db57084c009` | 0 |
| crates/bitwarden-api-api/src/models/cipher_field_model.rs | 1235 | `ec56712e6d893cbc43bc95a2d818732300b78458ea5dc0762a52c4343a8819ff` | 0 |
| crates/bitwarden-api-api/src/models/cipher_identity_model.rs | 3847 | `a3db38e10523ba453826f4afa3d67c4f2b5b0e672eade0a5f00e8c040dfe2984` | 0 |
| crates/bitwarden-api-api/src/models/cipher_login_model.rs | 2118 | `bb22f4876c79e813c2d7bf6b33db368fa759f5f7e8370bb63c8c424c1ff4bf43` | 0 |
| crates/bitwarden-api-api/src/models/cipher_login_uri_model.rs | 1060 | `8479b240c3132c60e39e536bdd54cd26e539d98e1ccb36380a78bdb23b4eecd8` | 0 |
| crates/bitwarden-api-api/src/models/cipher_mini_details_response_model.rs | 6188 | `b748f38bd2e84c25d4505c9eb1b3232bdaed05706667c5c2a0d8539233ec5054` | 0 |
| crates/bitwarden-api-api/src/models/cipher_mini_details_response_model_list_response_model.rs | 1383 | `a3edbe64b331bc6e06683ee481feceb34a9c94be74cee1f81afa84e303a7cfbe` | 0 |
| crates/bitwarden-api-api/src/models/cipher_mini_response_model.rs | 7102 | `bdfbfa1af40ca1563bb8c918aabd4a932fc1b8e962d28a24a9e13742b9d46241` | 0 |
| crates/bitwarden-api-api/src/models/cipher_mini_response_model_list_response_model.rs | 1341 | `3ab581e6bd39dc56f13a1957f2f0637385ac1eff1576f3f3e8c46a6ceeeda2db` | 0 |
| crates/bitwarden-api-api/src/models/cipher_partial_request_model.rs | 925 | `6f4d7ab54b5053a3d7762ed7c9933f3df37ae8b5efb991f921beb98630c555ac` | 0 |
| crates/bitwarden-api-api/src/models/cipher_passport_model.rs | 3168 | `7bc470daf84dd01d74633a61d2c050a7401033c4034eb2e60743fb51756ded42` | 0 |
| crates/bitwarden-api-api/src/models/cipher_password_history_model.rs | 819 | `f8cc927c6e71f3d4160752287b74188d72b829f14f5928851c02eb5476481c2b` | 0 |
| crates/bitwarden-api-api/src/models/cipher_permissions_response_model.rs | 929 | `825e6b76b64d98b62ff0c5568e6495d354816dc4cf2137f5841d673e4701ecb7` | 0 |
| crates/bitwarden-api-api/src/models/cipher_reprompt_type.rs | 2260 | `15ac60d806aa68085bcca53cad65bfcea09c94be7d470711d04b5f27b0c9dc54` | 0 |
| crates/bitwarden-api-api/src/models/cipher_request_model.rs | 6656 | `7deca83ef54cf2ac9ab7ef3a47a8ed407c18fd23350ea7eb3c9cf819f28f7b4b` | 0 |
| crates/bitwarden-api-api/src/models/cipher_response_model.rs | 7117 | `afb53cf7ce9d5305b226aed73926d2f62228936fee3142619ea288a03417d301` | 0 |
| crates/bitwarden-api-api/src/models/cipher_response_model_list_response_model.rs | 1317 | `127e6a9a11e244f6f639c860ee3f3a9e49125ec7685fc1bb72a57e424c952e81` | 0 |
| crates/bitwarden-api-api/src/models/cipher_secure_note_model.rs | 707 | `366c8c389327da79522871cc5c741081a96a300e6e934c71ac3983efb5628ffb` | 0 |
| crates/bitwarden-api-api/src/models/cipher_share_request_model.rs | 895 | `347d02e23ceff22e38f0d6a19293d08d9c8631a90120ad158a6ce5e5824040e6` | 0 |
| crates/bitwarden-api-api/src/models/cipher_ssh_key_model.rs | 1122 | `4b12ef4e5b774259e30e2ff260988f654f6eec4ba7a34e9310f5fe443fb9c9ad` | 0 |
| crates/bitwarden-api-api/src/models/cipher_type.rs | 2655 | `210dd65e3b07e4aa1cacbf048b9ea7c597ce3d08c2a8b63faf6a384f5eaa58fa` | 0 |
| crates/bitwarden-api-api/src/models/cipher_with_id_request_model.rs | 6776 | `b5a2e336138f5cd3a9b9bd3484c3f68eeb1d6fb7440fa8282a9332ad636effb4` | 0 |
| crates/bitwarden-api-api/src/models/claimable_rotation_job_response_model.rs | 2232 | `ae1f9fc7034a1e2c88bb9cc8edc109ba4d2f80ed7d69363bebebe7c15bee857b` | 0 |
| crates/bitwarden-api-api/src/models/claimable_rotation_job_response_model_list_response_model.rs | 1266 | `55083a0dd5d741bb1a29d4a4af18669c99b32951b06fa1ca77ae6ca73388c3f9` | 0 |
| crates/bitwarden-api-api/src/models/client_type.rs | 2430 | `08f57a1a1106d46aad50019dfd04fa8fa19d3ac30d8af961e1a81c4a8b4cfba2` | 0 |
| crates/bitwarden-api-api/src/models/collection.rs | 3689 | `91227104917be11fb03378ab2a8a28f73b60c497c36d26f38414383572f33d68` | 0 |
| crates/bitwarden-api-api/src/models/collection_access_details_response_model.rs | 3832 | `0663186f83ca8dd546951e8a64577e29dde1791888316d096a91fdd63dc85281` | 0 |
| crates/bitwarden-api-api/src/models/collection_access_details_response_model_list_response_model.rs | 1419 | `17c2ef540c57c0b13f98f402902cfa870e61b9da9873859a37de3913980a781f` | 0 |
| crates/bitwarden-api-api/src/models/collection_bulk_delete_request_model.rs | 669 | `bf08edc4bfc312fc4125767321d0cc55a505810c5494222d45b3ef38f0c44fa1` | 0 |
| crates/bitwarden-api-api/src/models/collection_details_response_model.rs | 3196 | `2e68a3fdd906e0af50bc44363a76ca78d7ce6e1272b25c939371d250833133c7` | 0 |
| crates/bitwarden-api-api/src/models/collection_details_response_model_list_response_model.rs | 1383 | `cab7c1930f4f8df197406e1bf08daaecfaecef5e5f39887402a71f7ad1bb342c` | 0 |
| crates/bitwarden-api-api/src/models/collection_response_model.rs | 1902 | `cc2889797c0ab5f974b234a855bc8add4ca4b04faba191c32248f1685f9ac729` | 0 |
| crates/bitwarden-api-api/src/models/collection_response_model_list_response_model.rs | 1341 | `13b17097e01b4caecd5cd3bacd7f4ff11f3ed3efe23713876722c0d3c37a0b41` | 0 |
| crates/bitwarden-api-api/src/models/collection_type.rs | 2530 | `f7e140a3ab48b7258a878c765c7368713c40c9a3f0958267448d3ea7b9ae7785` | 0 |
| crates/bitwarden-api-api/src/models/collection_with_id_request_model.rs | 1421 | `c287e4ed876b78dceccc3cc0edd4b3b6347b20517c8bc920d7b3047b9d4929e1` | 0 |
| crates/bitwarden-api-api/src/models/common_unlock_data_request_model.rs | 2175 | `0e803c044bc859a3842c3f355d6459cfbe72940f2e7b465d57c5758390a835ab` | 0 |
| crates/bitwarden-api-api/src/models/communication_bootstrap_settings.rs | 1353 | `445f01d74e7ee67c6b5da3536f41ab2fd3ebadf7c3e30cd01a3cadb7fee739ab` | 0 |
| crates/bitwarden-api-api/src/models/communication_settings.rs | 742 | `8cafaa882414f120dbdde0e93c4970d122d34515c7bc52bab72bc1cc03fc7b5f` | 0 |
| crates/bitwarden-api-api/src/models/config_response_model.rs | 2422 | `1670ab06d05022667158b000bda8a52284a856242274d92e0b8b8473350dc48f` | 0 |
| crates/bitwarden-api-api/src/models/confirm_organization_invite_link_request_model.rs | 1800 | `27f4536e361e8304e526fe4a421be6752386bf057708640b8aafe90fbe614032` | 0 |
| crates/bitwarden-api-api/src/models/create_client_organization_request_body.rs | 1671 | `88d2873d801d1b3ae64b9df7169fc1d9877b2a754924fba84d6e428232b41f3b` | 0 |
| crates/bitwarden-api-api/src/models/create_collection_request_model.rs | 1284 | `51f189d38a01665c3c9ce38b2c2cf4b4c5218ca051b9ac68678eccc095f518d7` | 0 |
| crates/bitwarden-api-api/src/models/create_organization_invite_link_request_model.rs | 1366 | `9b5e192933361d6f85bd3e8a68e9f59e437cb6ecb622634407df028179a986ba` | 0 |
| crates/bitwarden-api-api/src/models/create_premium_checkout_session_request.rs | 688 | `2e3ea08ae389b4d6628c1999f721b7c637f8ee54f437f80e4bc34b9c5e9a4513` | 0 |
| crates/bitwarden-api-api/src/models/create_rotation_config_request_model.rs | 2186 | `3f02e6beccaa6da376f8a0ee48f2b18e6caea06429bda00e89693c261713b6fd` | 0 |
| crates/bitwarden-api-api/src/models/credential_create_options.rs | 3099 | `4a2da225054a6528a3c5f79dc5d8688714c68b0fb5d575c1a30c782572826ef5` | 0 |
| crates/bitwarden-api-api/src/models/credential_properties_output.rs | 941 | `9c5044bf0b3ebd50a625c4e3376a278f61bb45216e44b8d6605a57b8485f0288` | 0 |
| crates/bitwarden-api-api/src/models/credential_protection_policy.rs | 1545 | `1cc370759feee55472e3850c15a08cc5bbe8af9e97febde5268a612b71c01a36` | 0 |
| crates/bitwarden-api-api/src/models/delete_attachment_response_model.rs | 1423 | `0f27c3ad82938a0794ce28785e64d1b6fe3d9e2b28eae1e09154b10dbb1d4432` | 0 |
| crates/bitwarden-api-api/src/models/delete_recover_request_model.rs | 633 | `2c24eca78492ae3ea2902270c29496d51281cb27fd4e7b5b4b3a8a611c45e1c6` | 0 |
| crates/bitwarden-api-api/src/models/device_auth_request_response_model.rs | 2797 | `ab6e51994d72578c796267e70500999b8186439f387006be47653c0953d0dfeb` | 0 |
| crates/bitwarden-api-api/src/models/device_auth_request_response_model_list_response_model.rs | 1383 | `74dc7917aa1a3c17dca60679caa77883630e4a83d67cc192e48458e50db126ed` | 0 |
| crates/bitwarden-api-api/src/models/device_keys_request_model.rs | 1091 | `5087033589af5c1f94a86dca2e506edd6e02278efa260bc42b031a99e240c65a` | 0 |
| crates/bitwarden-api-api/src/models/device_keys_update_request_model.rs | 926 | `afe0e974acbe6d24121180fb3213405d626c81b7437922f8e879b3cf66231d4d` | 0 |
| crates/bitwarden-api-api/src/models/device_request_model.rs | 1076 | `280e6b522746a2f172ef840baa74afc6cfe3ee12ba5fb1c9aec2e5d84edf17e8` | 0 |
| crates/bitwarden-api-api/src/models/device_response_model.rs | 2471 | `2980ddc413930134fcfbc4f3b6146abfd0e9f6968f4359e207e885817c68e14a` | 0 |
| crates/bitwarden-api-api/src/models/device_token_request_model.rs | 715 | `77de8520a9d3df446deb1a590b4a9b96d9dcb11f3ffdb37b06ab010d4a1192bf` | 0 |
| crates/bitwarden-api-api/src/models/device_type.rs | 4587 | `e76a5f1b273d5fca6d720bf1547091a6b55419c20e9181978cd74bde1592c12f` | 0 |
| crates/bitwarden-api-api/src/models/device_verification_request_model.rs | 836 | `6c56f2f3edf85bfb45b881151bd8f791c056f7a40e630a4c414abbe687209bcc` | 0 |
| crates/bitwarden-api-api/src/models/device_verification_response_model.rs | 1338 | `00c159a7b5285715ea19b15d97f9fbc57391fbab75a47e2681f68a1672aafd18` | 0 |
| crates/bitwarden-api-api/src/models/domains_response_model.rs | 1216 | `d8aa4103f189d849740f24bb36dda524d9143d31145de9916faeb9c324daea21` | 0 |
| crates/bitwarden-api-api/src/models/drop_password_health_report_application_request.rs | 1144 | `882ba991077d42a13565e0286b9d0b7a32ff283c4869f5cd963103614040eee8` | 0 |
| crates/bitwarden-api-api/src/models/email_request_model.rs | 2309 | `46a6c5f7476bad344b056eeccfbb7bd41d136929056e399e6321a2751aacf917` | 0 |
| crates/bitwarden-api-api/src/models/email_token_request_model.rs | 1452 | `75c6439b7881bbdab11b000103dd2fd8a98500970e513348283406679f4f0ba1` | 0 |
| crates/bitwarden-api-api/src/models/emergency_access_accept_request_model.rs | 665 | `de2faf5fe721070a2dd72bca748d0efda8c920d1215888b90ef38f32bca5bbbf` | 0 |
| crates/bitwarden-api-api/src/models/emergency_access_grantee_details_response_model.rs | 2287 | `776da65836cfd68c767445bc21e54e46ab46c88bde7035c13b9302064f8a45bb` | 0 |
| crates/bitwarden-api-api/src/models/emergency_access_grantee_details_response_model_list_response_model.rs | 1455 | `92c1878e3d114d659a4aa79fc72cb3aa4d8e0659add58d59ac8d552f89c5ebd1` | 0 |
| crates/bitwarden-api-api/src/models/emergency_access_grantor_details_response_model.rs | 2287 | `3e2e4823b5664d50442bddbec6e6f7e8e467e4aebad0dd0f6e498908dc907ba8` | 0 |
| crates/bitwarden-api-api/src/models/emergency_access_grantor_details_response_model_list_response_model.rs | 1455 | `a16bd9cae4e4f125ca011ab94d590f63ae2eb7881e9b542b2f8be4a21e4e8e4b` | 0 |
| crates/bitwarden-api-api/src/models/emergency_access_invite_request_model.rs | 1007 | `b1113bd0f8f2462cc3691d0c2ceab460a6822e0792c15f0f958eb7c6f28ee154` | 0 |
| crates/bitwarden-api-api/src/models/emergency_access_key_data_response_model.rs | 1652 | `2b0cb6ee362b7254b8bc8e6496287100ce5702c5b6e078386d7aec6dfb6d8f9d` | 0 |
| crates/bitwarden-api-api/src/models/emergency_access_password_request_model.rs | 1493 | `99232354562938fb7ee05674c99b8df5df9845d245a47d6c3e19ec10b070d325` | 0 |
| crates/bitwarden-api-api/src/models/emergency_access_status_type.rs | 2657 | `a82c9bd9f9dfced758aa2c73b7d08bcea3e827603a788f0174c8e3fcba62cf4f` | 0 |
| crates/bitwarden-api-api/src/models/emergency_access_takeover_response_model.rs | 1902 | `ba6072a7316733282858fec6c2a8c457a1f7c57abc3f1ec76fe834a1dbb21c3e` | 0 |
| crates/bitwarden-api-api/src/models/emergency_access_type.rs | 2273 | `c12f5e374e9c8f4f109aa2b213507fa7373aca509268d81e3b2e8e03d47ab20d` | 0 |
| crates/bitwarden-api-api/src/models/emergency_access_update_request_model.rs | 1099 | `e1a3f6890a5de491020fa24181aca69b802317dc0a1934bad661cb219889dafe` | 0 |
| crates/bitwarden-api-api/src/models/emergency_access_view_response_model.rs | 1172 | `3c4394179443a1ba5bef5b4ec3a80384a468591dbbb2978e1489867c80320b2c` | 0 |
| crates/bitwarden-api-api/src/models/emergency_access_with_id_request_model.rs | 1205 | `f52e07f905d7e436f072966652b8842c8e62c4ce9f059deec6b8311c2f5c3a1a` | 0 |
| crates/bitwarden-api-api/src/models/environment_config_response_model.rs | 1834 | `2b16db0e422b3b6705393fdcff2b8df62d819090b40814025e56e991e80c6ef7` | 0 |
| crates/bitwarden-api-api/src/models/error_response_model.rs | 1845 | `88b8c25132d62c730c38667de533d794c7ea27344f2bdd7f327b49d9ab13634f` | 0 |
| crates/bitwarden-api-api/src/models/event_response_model.rs | 5453 | `0a6a9443a6ac40b25875e81211a28ccf5ae1191ad27dc33361b0479a247737bd` | 0 |
| crates/bitwarden-api-api/src/models/event_response_model_list_response_model.rs | 1311 | `1d1e14c53e837341cbd8641a66f4044b8c29ab6c1d0e9a2a97522fc78892bc11` | 0 |
| crates/bitwarden-api-api/src/models/event_system_user.rs | 2622 | `c1102a7a8181df3121bd195f324cfaecdafadcacfa406db62a0824363a6e6667` | 0 |
| crates/bitwarden-api-api/src/models/event_type.rs | 25388 | `ccaac57c9150f60f33c85a3cc451fc11abde9510ea1a28d1e1265c0a5ab4328a` | 0 |
| crates/bitwarden-api-api/src/models/fido2_user.rs | 1164 | `939057435005ba9ca80c9d141311967eec8044fe8b6107ab2ab505f0e1f01479` | 0 |
| crates/bitwarden-api-api/src/models/field_type.rs | 2288 | `4df02e3ca2fd754a8688128bbce59e2904e7a7b1323db6ea60bfb5a259e657b6` | 0 |
| crates/bitwarden-api-api/src/models/file_upload_type.rs | 2207 | `6166785f9c13d8b46d00ca002216cb7c3b0eaa42916c6e920dd7fe91b3e1f0dd` | 0 |
| crates/bitwarden-api-api/src/models/folder_bulk_delete_request_model.rs | 653 | `7637bf8615dfd3b168c6f590d22730c22e6df25379f2c166e0c8bb8464db00bc` | 0 |
| crates/bitwarden-api-api/src/models/folder_request_model.rs | 600 | `558a76d1708eedef8ae433a16e9fbe0ffb356313b86887b0c924ca09dddf8a51` | 0 |
| crates/bitwarden-api-api/src/models/folder_response_model.rs | 1219 | `0f9f7e8752c2aefccdf4cf7304b8f3c7f1deef5e888c1e5920eccb3cd121f61b` | 0 |
| crates/bitwarden-api-api/src/models/folder_response_model_list_response_model.rs | 1317 | `9f5d4008ed5eea8e7de7006e12ac1efb5a33301ffdcfd852ce27e33089ea0bb7` | 0 |
| crates/bitwarden-api-api/src/models/folder_with_id_request_model.rs | 749 | `c52e8125235edc9e2527bfa68bff677e591d36d9643320e008318757e59da14b` | 0 |
| crates/bitwarden-api-api/src/models/gateway_type.rs | 2559 | `b6c658b03f5e99605b0701977d64f4eadb02352e2df54836788faad5c14888cb` | 0 |
| crates/bitwarden-api-api/src/models/get_organization_invite_link_policies_request_model.rs | 921 | `1727e563d8a77fb240828a1880edcebdb9c97c62872ba415c157171fb818efbc` | 0 |
| crates/bitwarden-api-api/src/models/get_organization_invite_link_status_request_model.rs | 913 | `b27bd20c017285f3c36c9b60a132b38b14622aad263dde81e6ad8e29aabe4f20` | 0 |
| crates/bitwarden-api-api/src/models/get_organization_invite_request_model.rs | 850 | `5036092567c50e68b619a4a9a2a3881a10db9954245fce65d8455717ced9f1e4` | 0 |
| crates/bitwarden-api-api/src/models/get_secrets_request_model.rs | 629 | `01795b9e6a13f47926e17b5fa567e4630099d70d51e4e6458922e8c4f9a59ec8` | 0 |
| crates/bitwarden-api-api/src/models/global_domains.rs | 1050 | `1acd2cc40f407077204335577c25a82b1fba20746b5ef4057b76652652d09f26` | 0 |
| crates/bitwarden-api-api/src/models/global_equivalent_domains_type.rs | 9425 | `a885148d1841bfa01be8d22700bf43a5ef0062b0bda3777ed0ccfcde3924f700` | 0 |
| crates/bitwarden-api-api/src/models/granted_access_policy_request.rs | 886 | `ca8597ee0743cd4669b4dc4336a233caac12b51a372eec36425970742ed8f92b` | 0 |
| crates/bitwarden-api-api/src/models/granted_project_access_policy_permission_details_response_model.rs | 1312 | `aa53a18c195b086fa40b1a6d3b832bdb0e166e8405681081d9ae43ddf639823e` | 0 |
| crates/bitwarden-api-api/src/models/granted_project_access_policy_response_model.rs | 1586 | `09e711ebcafa60b1022bd65f42fc8347114498d47e6cce6c46ce3c15c90de686` | 0 |
| crates/bitwarden-api-api/src/models/group_access_policy_response_model.rs | 1705 | `a55b87144924178cba148e61f666506deb37aecb1910b09b4bc8e515c3e834b2` | 0 |
| crates/bitwarden-api-api/src/models/group_bulk_request_model.rs | 625 | `88648d59614bea04ad360ba38efcf262f5708229df50636a9880cfdacb0a1e62` | 0 |
| crates/bitwarden-api-api/src/models/group_details_response_model.rs | 1688 | `9a9b2c55f54ff5c446a5582acd22dcb0a399db421ca7d874de29f823742709ff` | 0 |
| crates/bitwarden-api-api/src/models/group_details_response_model_list_response_model.rs | 1353 | `e2aeb25f9f242e0d83c8dcc0115730af949c6f60d575a5068b7b4ce4dc85905b` | 0 |
| crates/bitwarden-api-api/src/models/group_request_model.rs | 1036 | `8ca06ea02fe88cb1a3df8d3e2a64a1a169051f24a453667e30b06e7147adf200` | 0 |
| crates/bitwarden-api-api/src/models/group_response_model.rs | 1424 | `394fd49db86ad482719773273329af06badcd69a4ba401a5aaa10161d0564117` | 0 |
| crates/bitwarden-api-api/src/models/group_response_model_list_response_model.rs | 1311 | `ad166b9c5f00cab3e938bbc877fafab6b1b1dc8098ee9dc2582fb7a08eee4ba3` | 0 |
| crates/bitwarden-api-api/src/models/import_ciphers_request_model.rs | 1235 | `511977113f7db7b429ff028c25fe9defee1bf26429e33924b3c3e19fd2d79f35` | 0 |
| crates/bitwarden-api-api/src/models/import_organization_ciphers_request_model.rs | 1795 | `7795ae74daf79278938e737d487ff732b7219a156c412644f0bb534c6a28ba1e` | 0 |
| crates/bitwarden-api-api/src/models/inner_project_export_response_model.rs | 883 | `1eaeeb0019e320ec3d4e435fcf56d25533da8bdf0e6a5f5fa553a4475fed6cea` | 0 |
| crates/bitwarden-api-api/src/models/inner_project_import_request_model.rs | 734 | `3c5a788ca51856bbb3684d738c69a3c8bb52a624bedbc81e62dfc417c17ad264` | 0 |
| crates/bitwarden-api-api/src/models/inner_secret_export_response_model.rs | 1397 | `2989b513a31adb6398f575d28ce69f7a9eb745e4aa1676f63a187a219bdb5b80` | 0 |
| crates/bitwarden-api-api/src/models/inner_secret_import_request_model.rs | 1161 | `e927854e4bb55bef433b2473b3fa8818a31215f0d0f88dc68605218c48b833c5` | 0 |
| crates/bitwarden-api-api/src/models/installation_request_model.rs | 629 | `16ef4b67b2a2af6099bf52cd5125de3b988587d221e9115fbbf51d7190f7e975` | 0 |
| crates/bitwarden-api-api/src/models/installation_response_model.rs | 1185 | `7030cb086622f2c892d7e212bfb6e361edd56763b6e155e6734534605cf5cbcd` | 0 |
| crates/bitwarden-api-api/src/models/int32_int32_key_value_pair.rs | 845 | `b867f8a79067be201ec33d03986a252e69ae96393d2cb79064e2cf9aa9e04c5c` | 0 |
| crates/bitwarden-api-api/src/models/integration_type.rs | 2618 | `99dd008d860f1cbae2b5b581fe1fa5d914e95b568b1dd2ad08991de16a078f18` | 0 |
| crates/bitwarden-api-api/src/models/invoice_preview.rs | 2644 | `99839adf6a6330727ad844c24f7424e01fb860f2d1bd165ecc7db6144e8c0dd9` | 0 |
| crates/bitwarden-api-api/src/models/invoice_preview_discount.rs | 1320 | `7d75fc35242dad397b5ab2103e309efd7b5f2861e2dfb08784723fbe50dc392b` | 0 |
| crates/bitwarden-api-api/src/models/invoice_preview_item.rs | 1090 | `7a4ab3c9da3727882418cd45238b3d2957720bc274b7de455f5f6e0e4f29e9b6` | 0 |
| crates/bitwarden-api-api/src/models/json_element_push_send_request_model.rs | 2093 | `278398056cace0e828be849329bab24b31ac0904355ed0582ee6f1b6ce8179c4` | 0 |
| crates/bitwarden-api-api/src/models/kdf_request_model.rs | 1141 | `bc818110268678572223cca09fd53780a9811f35955f76822fcc035b66bccd7b` | 0 |
| crates/bitwarden-api-api/src/models/kdf_type.rs | 2153 | `3d38a2218ce17c44eb32f80efdbfd2b20348d7353e3faf87d829ac6a709120b0` | 0 |
| crates/bitwarden-api-api/src/models/key_connector_confirmation_details_response_model.rs | 1027 | `5d0fc464c847c26604ca798d7d52b505a27888352dc49cbbe36d4eb42eea6bb1` | 0 |
| crates/bitwarden-api-api/src/models/key_connector_enrollment_request_model.rs | 878 | `fc1651e0bdc08cfda788c2d2cf47bce0fdbbb983bd98cebe4d8b2c6638c238a5` | 0 |
| crates/bitwarden-api-api/src/models/key_model.rs | 969 | `9b32cad5c51ddb8d5fb9029e42104265a1ef1bab3e126e5acc37d9530e2f28cb` | 0 |
| crates/bitwarden-api-api/src/models/key_pair_request_body.rs | 830 | `198a1f480c853a229844722587f32e2a4e3bcf20a9cc9cf6b5234507b45bf207` | 0 |
| crates/bitwarden-api-api/src/models/key_regeneration_request_model.rs | 1030 | `013d6b78106d756ddfd87c8c023e133bde1edde10a9177110b60ccf677dd9fd1` | 0 |
| crates/bitwarden-api-api/src/models/key_rotation_data_response_model.rs | 1914 | `5ee0a78a2653049433f42ae2490f17739a4af6ece5c39f51ba0fdd5503073048` | 0 |
| crates/bitwarden-api-api/src/models/keys_request_model.rs | 1418 | `66aa2b7ea1a64c8107a10a6ba2a6e47b0674a8dc1f54239b56fd765be0119f8a` | 0 |
| crates/bitwarden-api-api/src/models/keys_response_model.rs | 1595 | `2054eae238b1a3af0fba0a1974577ab7894ad5495183ec769655960e55bdf30a` | 0 |
| crates/bitwarden-api-api/src/models/large_blob_support.rs | 1089 | `dccee8d79e3a5616eabec84beb52f634e6aa7d8df6e9132f9ca0cde4823f03c8` | 0 |
| crates/bitwarden-api-api/src/models/license_type.rs | 2181 | `9fef93fd9cc652423c511d924ff94dc381c9c476dd118b9a7a13009585ab27ba` | 0 |
| crates/bitwarden-api-api/src/models/master_password_authentication_data_request_model.rs | 1655 | `c2c9765f32f9342e47e90f6e34c80a548025e8b9061310f8df18f102e6f1e528` | 0 |
| crates/bitwarden-api-api/src/models/master_password_policy_response_model.rs | 2199 | `b94f327bfc0dc10cf14e0b4d4d8f188d1a9a47a24836fd4b75753432436b6e73` | 0 |
| crates/bitwarden-api-api/src/models/master_password_unlock_and_authentication_data_model.rs | 2673 | `1ad11ff43d7d40aef5bd5c25a654a8be01370fe203d2bd49527a5a66f0ff3aaa` | 0 |
| crates/bitwarden-api-api/src/models/master_password_unlock_data_request_model.rs | 1746 | `5f50fb74afe02335b8b51dc7708e54541e487c66e1d1248758b5d0b256b57682` | 0 |
| crates/bitwarden-api-api/src/models/master_password_unlock_kdf_response_model.rs | 1225 | `d35be301995ec47f17f20120a781bcad1f7c44c21632148dc894753812ff6b41` | 0 |
| crates/bitwarden-api-api/src/models/master_password_unlock_response_model.rs | 1505 | `f80d02c125a3ea700525cd81a5fbf9e684f4f210a14672d9466e13b56cb4593b` | 0 |
| crates/bitwarden-api-api/src/models/member_access_detail_report_response_model.rs | 3420 | `965176c24326eb05a952db852063ab807e62ecdfe57b395c957fe8890c82947a` | 0 |
| crates/bitwarden-api-api/src/models/member_cipher_details_response_model.rs | 1637 | `a50267de7faa1a5f7af4ef63975f2febb62473708bbc0c0e7e501be2b3a31112` | 0 |
| crates/bitwarden-api-api/src/models/member_decryption_type.rs | 2463 | `4ce452c27cb44b5c3a267be5efb10a83a3d6860f43353a964ebc6e75728089d7` | 0 |
| crates/bitwarden-api-api/src/models/minimal_billing_address_request.rs | 809 | `3fa0c876aefe2b339b1251b4016db25d98e482b5916c2e92634b570c896db620` | 0 |
| crates/bitwarden-api-api/src/models/minimal_tokenized_payment_method_request.rs | 773 | `898b72674b5f8acacf718f61548660aaa01107d6f0541dd3c311e7eda2b8313a` | 0 |
| crates/bitwarden-api-api/src/models/mod.rs | 82886 | `129052ebd77f9fd002754aef5d163af53090426f264bc7813890ffc4a81688cd` | 0 |
| crates/bitwarden-api-api/src/models/non_tokenized_payment_method_request.rs | 664 | `8db41d5623ada72be035d8dc8f129d2b958bb0c0b7ad18f16fd26bf06cbd94a7` | 0 |
| crates/bitwarden-api-api/src/models/notification_response_model.rs | 2156 | `8b0e109a8fe99cca861889deb25ebd819e4b92a0baf57a2befed05d8fae778c0` | 0 |
| crates/bitwarden-api-api/src/models/notification_response_model_list_response_model.rs | 1353 | `37e5be889ee8eb9faf2ad914e8b0e46fffd491e443ce5dd40dc22ccedb5abbc8` | 0 |
| crates/bitwarden-api-api/src/models/open_id_connect_redirect_behavior.rs | 2431 | `05053459709001ac6282a9409b32dbf0924cd7ec7427c7582eab03e63d3fc631` | 0 |
| crates/bitwarden-api-api/src/models/optional_cipher_details_response_model.rs | 1175 | `cf9e3f6e527619ea93c280948f89b756def42e598cd3ed0967dec268f597c6c6` | 0 |
| crates/bitwarden-api-api/src/models/organization.rs | 23807 | `e5d888d07c0af122417ec8bfccd6993021b4f7014d4eadaa00cd7dde6d75861b` | 0 |
| crates/bitwarden-api-api/src/models/organization_api_key_information.rs | 1160 | `5c9dba0f69befeb041585fab9a8f4e1b0c6656c4a8a925d2b16d6c4d6cb5b0fe` | 0 |
| crates/bitwarden-api-api/src/models/organization_api_key_information_list_response_model.rs | 1377 | `84cc82cf74f6998a8986fd632cc4503d1815bc259e93b95d3160bc26c00c4326` | 0 |
| crates/bitwarden-api-api/src/models/organization_api_key_request_model.rs | 1564 | `c3ca162c68e51fe79f70920f7f41f33dbd143a99f11a3f2091ce67a2ca496821` | 0 |
| crates/bitwarden-api-api/src/models/organization_api_key_type.rs | 2401 | `6d279cb8fcd884d7e9d1cfe947c91117564b4f37f224ffaee72889d1aedd5b27` | 0 |
| crates/bitwarden-api-api/src/models/organization_auth_request_update_many_request_model.rs | 1090 | `8759e71d70e6f9398952c802ef1f551e4d6c32022a1b380b66400b09d3b1af5e` | 0 |
| crates/bitwarden-api-api/src/models/organization_auto_enroll_status_response_model.rs | 1168 | `4a41c968eb732775e6c7f17b8fa0347db5d8d056164a8814445e95f84d0c280c` | 0 |
| crates/bitwarden-api-api/src/models/organization_collection_management_update_request_model.rs | 1683 | `f3a60811a37ed866f80c7a07896f2b2564261179f10226d876c9af662168b289` | 0 |
| crates/bitwarden-api-api/src/models/organization_connection_request_model.rs | 1380 | `9ac10a3db7bfc1b8792389776b32ed6b2105d6318469edffb0deaeb57a23b808` | 0 |
| crates/bitwarden-api-api/src/models/organization_connection_response_model.rs | 1521 | `0e392c04dce8886cd9d21a611a7c1d6f35464fe653f2a89d90c8b68518973e1d` | 0 |
| crates/bitwarden-api-api/src/models/organization_connection_type.rs | 2400 | `74cf35b558e78506fb0ba9938250bd0d6f42244bdb39c5c074a48144490cc775` | 0 |
| crates/bitwarden-api-api/src/models/organization_counts_response_model.rs | 1332 | `a023b0c2e69a69f6a7ec500f7f2e99f74563132063e5f94dfe7f60d2b8347e20` | 0 |
| crates/bitwarden-api-api/src/models/organization_create_request_model.rs | 6439 | `42c5a5a247c4f23f5ef568fbbf55881e211b5ac0734ea746dc280086b35d3369` | 0 |
| crates/bitwarden-api-api/src/models/organization_domain_mini_response_model.rs | 2134 | `97e3661c9d4f4d1189d96f181230497f0b00406a78fbd116b582811296f5882d` | 0 |
| crates/bitwarden-api-api/src/models/organization_domain_mini_response_model_list_response_model.rs | 1276 | `6671cb09ab60c5ee570d1a8ec56c63ad0bc5f574271a15850a306c6ad35684c0` | 0 |
| crates/bitwarden-api-api/src/models/organization_domain_request_model.rs | 681 | `7f83f198d171a437bf66df5167f1c31d192749ad251302c9b8b72e653a7294f8` | 0 |
| crates/bitwarden-api-api/src/models/organization_domain_response_model.rs | 2474 | `da00d65fd7bca4514bca9a86abefae17e9f3406c211de3bfc1339be8e2bd99a1` | 0 |
| crates/bitwarden-api-api/src/models/organization_domain_response_model_list_response_model.rs | 1389 | `141be0cb488591fcb88efe1588b01220cbe29a135383e28c7efa989ca2ee0e14` | 0 |
| crates/bitwarden-api-api/src/models/organization_domain_sso_details_request_model.rs | 693 | `d0f55d7114f2c7cd1c9f43acec8384ac741ac9266f4f8b442d82b490ad6e1fef` | 0 |
| crates/bitwarden-api-api/src/models/organization_integration_configuration_request_model.rs | 1424 | `05db274cce94f3d14cbffb6d037b4d0eab4b228a504e68323840f79d9665109d` | 0 |
| crates/bitwarden-api-api/src/models/organization_integration_configuration_response_model.rs | 1949 | `7955f6820d41c1f42f4128c928394360b3a8eef743fd906bfcf4cad8b9c3c069` | 0 |
| crates/bitwarden-api-api/src/models/organization_integration_request_model.rs | 992 | `49eb1e624300aa1e57a7d74d9b1a82b43580d38f666d6d5ae779c30b8e5b1621` | 0 |
| crates/bitwarden-api-api/src/models/organization_integration_response_model.rs | 1522 | `20cdc284458eb014a8b707b7f4a83d98f5cfc979b180ffa6e6d13f0870197860` | 0 |
| crates/bitwarden-api-api/src/models/organization_integration_status.rs | 2688 | `9ccd1a417651a3f65e6b5b5f80a7600cc488a91c0784964d341be1ed755db3f6` | 0 |
| crates/bitwarden-api-api/src/models/organization_invite_link_response_model.rs | 2136 | `5c4b0e02acd5e11acec7ca9f785aa41dc796a1863f9c05a5ef86fc8cc1bb1113` | 0 |
| crates/bitwarden-api-api/src/models/organization_invite_link_sso_response_model.rs | 1158 | `b1eecc8470a8087535633ee7794865f3a96d0ecd730d24e6c6c02527aaebcf24` | 0 |
| crates/bitwarden-api-api/src/models/organization_invite_link_status_response_model.rs | 1846 | `b5a7e2159d7abc6c45f50c0db531c01c2eb978119d6b1be8c9f116b490dce9bd` | 0 |
| crates/bitwarden-api-api/src/models/organization_invite_link_validate_email_domain_request_model.rs | 1066 | `2b95b66cd436d330a512d926127e8e33663c6bd5315f12546927af1fdfe16a9c` | 0 |
| crates/bitwarden-api-api/src/models/organization_invite_link_validate_email_domain_response_model.rs | 837 | `50c77fabb80f44736999d292fb4148ecd9e966166647c23f8da0b0decfed0e0c` | 0 |
| crates/bitwarden-api-api/src/models/organization_invite_response_model.rs | 733 | `0306ca371cb6426d06dd222703bdfbf030ea58a2199c71b1f47a8b30307c960a` | 0 |
| crates/bitwarden-api-api/src/models/organization_keys_request_model.rs | 870 | `b612a2027418b5dcbad7e1c88e250e9d1cc5eed11e2a6ff035dc158de7ad2c03` | 0 |
| crates/bitwarden-api-api/src/models/organization_keys_response_model.rs | 1136 | `b2cd9da4e47ea2a987518927dcc5e662bc27eb3597165897b2f84446d547abe1` | 0 |
| crates/bitwarden-api-api/src/models/organization_license.rs | 10999 | `760e2a51c3dd70fb27350ee0e982f9fc920041ca4d4556c04c499c1f74d015b4` | 0 |
| crates/bitwarden-api-api/src/models/organization_no_payment_create_request.rs | 6076 | `323f337105ff0bb0da21c6149adbc890b2c5820233ada8966f6d759d220a1b71` | 0 |
| crates/bitwarden-api-api/src/models/organization_password_reset_key_data_response_model.rs | 1468 | `3dd497791f8bf89845050be77e2fa839943c08e535180f4ba09494f2c5a0d648` | 0 |
| crates/bitwarden-api-api/src/models/organization_private_key_response_model.rs | 967 | `003fbf441e820b91e71e6073014822185e7304a996c12783a9106ab93c049420` | 0 |
| crates/bitwarden-api-api/src/models/organization_public_key_response_model.rs | 959 | `562f5d7dc7937267e96d47c54124889e4ddd7022edeab8e8a9bfbf34d22263c7` | 0 |
| crates/bitwarden-api-api/src/models/organization_report_file_response_model.rs | 1310 | `32e72a2f0950649084e134d03eaa8ea43a06c1c04755756ef2eaaed3b030155b` | 0 |
| crates/bitwarden-api-api/src/models/organization_report_metrics.rs | 3675 | `a2fb9dad55a7c164285a415a007fdd18bfca160d50739d12481e5882c2fac150` | 0 |
| crates/bitwarden-api-api/src/models/organization_report_response_model.rs | 2883 | `76691e340b5caa20199e1d76eaf5e4d8215854f09585fd9d2477d702ef706df6` | 0 |
| crates/bitwarden-api-api/src/models/organization_report_summary_data_response.rs | 1225 | `d99756d597c035161a023f3b4e1f95f45aca45b9c83ac68bde58b3dffb49592a` | 0 |
| crates/bitwarden-api-api/src/models/organization_response_model.rs | 11922 | `f590bc6a2dcd7f2c7d8bfd1082340f1ef30ba02ed3772358c9a2b024436cf21f` | 0 |
| crates/bitwarden-api-api/src/models/organization_seat_request_model.rs | 687 | `7fecf2e89486e05144e35437ae47c769c0daf929446d1e9918c5e844a1b0c80f` | 0 |
| crates/bitwarden-api-api/src/models/organization_sponsorship_create_request_model.rs | 1613 | `fa17bd0edc34afd5ba25d5207afccedcbaa70557fd7705b6da9963c306c94cfa` | 0 |
| crates/bitwarden-api-api/src/models/organization_sponsorship_invites_response_model.rs | 2991 | `cc6d461b83c22c159489f1914af626b53ab26c899014add680db4423636db3b6` | 0 |
| crates/bitwarden-api-api/src/models/organization_sponsorship_invites_response_model_list_response_model.rs | 1465 | `75729a2f46cb6b40e742767dcfcc56c98379e13eaaf5d130cd345d1d998225ca` | 0 |
| crates/bitwarden-api-api/src/models/organization_sponsorship_redeem_request_model.rs | 1068 | `3a58e1a6b844b47621fae871417e7927e7cdac90a6d25f89e6361f3238d208a8` | 0 |
| crates/bitwarden-api-api/src/models/organization_sponsorship_request_model.rs | 2135 | `e9f5c9ad84e75fac5ced121624df18b3c8a7842f23ef7fb1aed72284f63945e4` | 0 |
| crates/bitwarden-api-api/src/models/organization_sponsorship_response_model.rs | 2609 | `a3948267e099aa5446cb353cbd6bcb7a477c8516a182963a027c846019bb7e4f` | 0 |
| crates/bitwarden-api-api/src/models/organization_sponsorship_sync_request_model.rs | 1370 | `bb7a6b2037fe0ccb6022e9c972170bce9eaa11320c74a8d75fe442ef4c3b150d` | 0 |
| crates/bitwarden-api-api/src/models/organization_sponsorship_sync_response_model.rs | 879 | `f27926ae7b6cb0dadedfdd79a5e1b9523748006fb5a04cbfeac526b8c86de8f8` | 0 |
| crates/bitwarden-api-api/src/models/organization_sso_request_model.rs | 1065 | `f87eeca8b208277747e3100494ef0bb16c1b3b61303bd969e4d92cd62e93070f` | 0 |
| crates/bitwarden-api-api/src/models/organization_sso_response_model.rs | 1501 | `6b661299f9702fc4cde027d0b9a671f2eaacd5e8a5e83a5f3d19f40b61c6b692` | 0 |
| crates/bitwarden-api-api/src/models/organization_status_type.rs | 2398 | `85d62dbe07e4fa4d3d0b11dd36a6ee8d4f6090d8605b487a9285ed689c2fa955` | 0 |
| crates/bitwarden-api-api/src/models/organization_subscription_plan_change_request.rs | 886 | `983f808e5c7f09a6fca225ea90b8c1be1c3f13b253e42fb57cc3011a6546e5e1` | 0 |
| crates/bitwarden-api-api/src/models/organization_subscription_purchase_request.rs | 1620 | `73051f82e8da19736e798d95970cfd4283e50c23f9a8c232cb63f215801a46bb` | 0 |
| crates/bitwarden-api-api/src/models/organization_subscription_response_model.rs | 15792 | `7751d14cb15d0321d67de0d891d20e72c0884222f8593302de6717eb38ea20ca` | 0 |
| crates/bitwarden-api-api/src/models/organization_subscription_update_request.rs | 1104 | `a8e7d2c83dce7d0f2e6ee1bf3371298637d8fa69867d72fae95d3a173498a479` | 0 |
| crates/bitwarden-api-api/src/models/organization_subscription_update_request_model.rs | 988 | `418c1395d19f5b893314397e54c85f37d5fa973fceff38225b86839956aa590c` | 0 |
| crates/bitwarden-api-api/src/models/organization_update_request_model.rs | 1153 | `5c168688480bdde052067b6804e5302e2a27047d1bff349193fc1eb24e9620ba` | 0 |
| crates/bitwarden-api-api/src/models/organization_upgrade_request_model.rs | 3005 | `1fc7a18a539854ae7c5fb82695ed8404c20e93c3764922787b852b4abaa5fb1b` | 0 |
| crates/bitwarden-api-api/src/models/organization_user.rs | 6440 | `17bbf6e948d7dae1eb289e7630d315b5610d39efdaaf0d2a94370cd808817712` | 0 |
| crates/bitwarden-api-api/src/models/organization_user_accept_init_request_model.rs | 1226 | `917690639ea221dd843acfc7c46597c1658a90859b58c05263158dbc398238b8` | 0 |
| crates/bitwarden-api-api/src/models/organization_user_accept_request_model.rs | 913 | `e7d72cbadfd6e00eeea12a8c168eb6d7a11d86d8dc74c3e9cdc03ecaf9952114` | 0 |
| crates/bitwarden-api-api/src/models/organization_user_account_recovery_request_model.rs | 1412 | `6f0c51a3944b3b9d8e670845eaae0785926622f0d59371e84b5d1aad64238e96` | 0 |
| crates/bitwarden-api-api/src/models/organization_user_bulk_confirm_request_model.rs | 1083 | `61ab27f990e3c144165a4e2749b56f74f808d0499b7a415436a8ff82632a756c` | 0 |
| crates/bitwarden-api-api/src/models/organization_user_bulk_confirm_request_model_entry.rs | 785 | `ff7e847c56834728d85500904fcc1378d231a769450833216236c4648cd3c90e` | 0 |
| crates/bitwarden-api-api/src/models/organization_user_bulk_request_model.rs | 951 | `6686170168d5427418640a1a9306fca8f37ce28fac6f814a5aa5bb816315efc7` | 0 |
| crates/bitwarden-api-api/src/models/organization_user_bulk_response_model.rs | 1074 | `e81581829ae3bbbce50437fdb79e4a6c075316cdda551c16a6d91ccc0c4f2a85` | 0 |
| crates/bitwarden-api-api/src/models/organization_user_bulk_response_model_list_response_model.rs | 1401 | `acd72b946b8b776c1352a90ad4c04d6b88c4ebecabcdff2e2e96a0fbbf3c179a` | 0 |
| crates/bitwarden-api-api/src/models/organization_user_confirm_request_model.rs | 945 | `ed83dfa584eb26ccb108276affd0508be8bcc3a452b66b7cf1794bf3d77e65c1` | 0 |
| crates/bitwarden-api-api/src/models/organization_user_details_response_model.rs | 4230 | `f7b10374d05ca6f228283370a757afddbc479ffbdba883995dce60530ab47423` | 0 |
| crates/bitwarden-api-api/src/models/organization_user_invite_request_model.rs | 1757 | `76ff4d36b52c248ff5889de00ef955c0798763dab36f19b77678cb37b1201a2d` | 0 |
| crates/bitwarden-api-api/src/models/organization_user_pending_auto_confirm_response_model.rs | 1194 | `f0ff763cbfd5503d6bbebcf9ca22385e071a526c515511f321e201532840ab0f` | 0 |
| crates/bitwarden-api-api/src/models/organization_user_pending_auto_confirm_response_model_list_response_model.rs | 1489 | `8f3d86d39d9b91cb8f4f2dbb7458bcf9656787c6a05e798cf730a7874d0ef644` | 0 |
| crates/bitwarden-api-api/src/models/organization_user_pending_v2_upgrade_response_model.rs | 1974 | `7bcfa73a9636f98bb43c3e0100b1b925dee940c7dcc128c9123b214d850ff950` | 0 |
| crates/bitwarden-api-api/src/models/organization_user_pending_v2_upgrade_response_model_list_response_model.rs | 1326 | `2c43b95e1ec3966f93d223686719ddf475963a801d3a06839bf618c091420d41` | 0 |
| crates/bitwarden-api-api/src/models/organization_user_public_key_response_model.rs | 1241 | `223f5520b3ef5adf3b3e27b0bdeb8d6fe73382c3aacf44b43dadc48cc14308a2` | 0 |
| crates/bitwarden-api-api/src/models/organization_user_public_key_response_model_list_response_model.rs | 1431 | `0730cabf1170307aa4fbca0a319c2bd12fe298298ec83bd017e8e6e0ae9f57fc` | 0 |
| crates/bitwarden-api-api/src/models/organization_user_reset_password_details_response_model.rs | 2502 | `be6fd51ce1f609c656ec1f043f733508524f12145370e2f12715c00d3f0cc6b2` | 0 |
| crates/bitwarden-api-api/src/models/organization_user_reset_password_details_response_model_list_response_model.rs | 1501 | `1fa47ac33e52cf1bda693c785eaa186be6a213a4e883ed201b0adb4a236ede8a` | 0 |
| crates/bitwarden-api-api/src/models/organization_user_reset_password_enrollment_request_model.rs | 1109 | `bdb8d73f8349e63686ce8a4f529882c7caf8c12e105761cd577d8e33f76f46e5` | 0 |
| crates/bitwarden-api-api/src/models/organization_user_reset_password_request_model.rs | 1963 | `a4de9d0efa10715d4581031745ef73e996eaa55a427c2890e8933ca67c644008` | 0 |
| crates/bitwarden-api-api/src/models/organization_user_restore_request.rs | 928 | `cfa5906cd7a454ce0628533968ff201b572d52d6c8f58a341ee0b954d7eab36c` | 0 |
| crates/bitwarden-api-api/src/models/organization_user_status_type.rs | 3001 | `5800b9700f3fbef755796738ae11012c86dbd9300e0f664574e6105474c23ba6` | 0 |
| crates/bitwarden-api-api/src/models/organization_user_status_type_new.rs | 2964 | `cd17583b07d1178f4fc4496a9f8c7d61acd6aa744d54c515e2974b04c0beb01a` | 0 |
| crates/bitwarden-api-api/src/models/organization_user_type.rs | 2423 | `b2eff9ad9ac5391ade311a057a6a39de6f30a1b634590a104e63238e6e983f65` | 0 |
| crates/bitwarden-api-api/src/models/organization_user_update_request_model.rs | 2412 | `5333fb043c208da423d71540ac333af02777a9c34f18d01a493888ed8298e801` | 0 |
| crates/bitwarden-api-api/src/models/organization_user_user_details_response_model.rs | 5441 | `be97b5f25cb099e94ab170ecf3a2920178a16da812f978670bdc6276a6ba74e5` | 0 |
| crates/bitwarden-api-api/src/models/organization_user_user_details_response_model_list_response_model.rs | 1443 | `0e4e3ab308809069029f89180bf0be15ecc2e477b5222f16e0bff314e2c6d83a` | 0 |
| crates/bitwarden-api-api/src/models/organization_user_user_mini_details_response_model.rs | 1880 | `780f2822b9f8a506a8252d1ba372230611353de1f3ff044db74aa18812b2ca4d` | 0 |
| crates/bitwarden-api-api/src/models/organization_user_user_mini_details_response_model_list_response_model.rs | 1471 | `1dbc97c48bb3787918c4f0c1bf28c0225af5d5d4da37a02229b9064f50525169` | 0 |
| crates/bitwarden-api-api/src/models/organization_user_v2_upgrade_request_model.rs | 2069 | `b928c206c6217dedde7dfe20d22d49dc377de4e25b1b6ac7f54e08fdbf536960` | 0 |
| crates/bitwarden-api-api/src/models/organization_user_v2_upgrades_request_model.rs | 1284 | `526720c7f7b8b2b7b698a6eb9e9d4d44a917c9507978762dd2cfbf870f34b439` | 0 |
| crates/bitwarden-api-api/src/models/organization_verify_delete_recover_request_model.rs | 705 | `605dbcb4d0bfa4a5640bdbc8817ef584cf69bbfcbfcd30a0d9b9110cf1de473c` | 0 |
| crates/bitwarden-api-api/src/models/other_device_keys_update_request_model.rs | 1085 | `c52c643f4bf30a17af3172f31cb67bb047642295cd79938f6997fa5cb0b534df` | 0 |
| crates/bitwarden-api-api/src/models/pam_access_connector_detail_response_model.rs | 4844 | `72b2c0590abb63880d9fe1b5a2841dc9e5d46872d25f49852c056ebbe553db36` | 0 |
| crates/bitwarden-api-api/src/models/pam_access_connector_response_model.rs | 3945 | `728f91903ca642fa98de2f42f5832104a0bab17009c44e05a4be45fa2d448a55` | 0 |
| crates/bitwarden-api-api/src/models/pam_access_connector_response_model_list_response_model.rs | 1256 | `3f754b15ce7d38f15fd0d9c677d9c4d8b81a2d29531c589c6de3c934cb2314b7` | 0 |
| crates/bitwarden-api-api/src/models/pam_access_connector_status.rs | 2350 | `57729a581b4ad9abc3b25f997b469cafa816738b346604062afca4849fa1ca61` | 0 |
| crates/bitwarden-api-api/src/models/pam_rotation_attempt_response_model.rs | 3301 | `ea8da62a716204650d903fa1ca510e2467774a004b31d70f8c55f5599653d396` | 0 |
| crates/bitwarden-api-api/src/models/pam_rotation_attempt_status.rs | 2515 | `5b1cf49e3f775f5d8451a22c989c3b7f3cb55532a8f07c8b1172e263e5ffdc32` | 0 |
| crates/bitwarden-api-api/src/models/pam_rotation_config_detail_response_model.rs | 5812 | `ac33689f87b311a150f3f16e930eaef6bd7f847f35c621de2f3dac3992b30cc9` | 0 |
| crates/bitwarden-api-api/src/models/pam_rotation_config_response_model.rs | 5467 | `461e433ed0c5f7d9ef22be09612843ae66dfc7e18656687526d418cc3915f911` | 0 |
| crates/bitwarden-api-api/src/models/pam_rotation_config_response_model_list_response_model.rs | 1251 | `cb812817248b839c140c20d0ac373530c6209f22a65dce084ab4ef1d9ef62092` | 0 |
| crates/bitwarden-api-api/src/models/pam_rotation_job_response_model.rs | 3424 | `4d2fd544c9feb69f79cf54f2420d7be06c2f26f86c4f16f283b99a746f1b64a8` | 0 |
| crates/bitwarden-api-api/src/models/pam_rotation_job_status.rs | 2532 | `80865cb2146e4fd133c62fc9e63bc8fa796a698849d70e1d198fa23d92de708a` | 0 |
| crates/bitwarden-api-api/src/models/pam_rotation_source.rs | 2350 | `ba69e03303611032cb896c5be93aef50d1dc3e1b3e863ec91b2a8075e4fccc7e` | 0 |
| crates/bitwarden-api-api/src/models/pam_rotation_sync_state.rs | 2440 | `2f14398c252b86e4fb0c4ac2f9d5590f76fa6249b3281568911db8c4137e81e7` | 0 |
| crates/bitwarden-api-api/src/models/pam_session_termination_outcome.rs | 2514 | `692eaa535b03323151bab36749230411927d1a672c4273bf4c2dbb5fb2be393c` | 0 |
| crates/bitwarden-api-api/src/models/pam_target_system_method.rs | 2313 | `905b50742674e4c256c800e7aeb7ec6d984486fdc13b4b1b624577456a96d82c` | 0 |
| crates/bitwarden-api-api/src/models/pam_target_system_response_model.rs | 2692 | `edd7a64fa4e195f41d0ad58d7afd7e3c003d93712895fbbe463e7a29cf09e72d` | 0 |
| crates/bitwarden-api-api/src/models/pam_target_system_response_model_list_response_model.rs | 1241 | `409af96dcb4d4b537a3c7d239b30e8121ad079e040026c509abfeb507accc320` | 0 |
| crates/bitwarden-api-api/src/models/pam_target_system_status.rs | 2396 | `7b573976ad9b12abcd649e7429d514217c63beb630641bbd2ef45fac3fed56d5` | 0 |
| crates/bitwarden-api-api/src/models/passkey_directory_response_model.rs | 1303 | `1f2b63b986fba139f866e906f5bed6be4e80de94432432d430e9976f32da8e76` | 0 |
| crates/bitwarden-api-api/src/models/passkey_key_data_response_model.rs | 1270 | `12601dcd0df83c43d1605daa6d909dff76f23f3a62f9c88b63a436c5fcafd948` | 0 |
| crates/bitwarden-api-api/src/models/password_health_report_application.rs | 1476 | `b451a25e3c5ca1244cffaa85cf5ebfd13aa6516c39027f2aac128fdb44728985` | 0 |
| crates/bitwarden-api-api/src/models/password_health_report_application_model.rs | 949 | `3ab05dad984f6fcfaf7ff8414401d879c3dc5ec3be9d0959fde7528fb7f3d6a0` | 0 |
| crates/bitwarden-api-api/src/models/password_hint_request_model.rs | 629 | `e6a5bcebc0d56715c7fde98fe20d42dab2561d574dbb06eda1ed5e3e1862499c` | 0 |
| crates/bitwarden-api-api/src/models/password_manager_invoice_items.rs | 1231 | `40a17eb1292f164d64df8535b803b820427effe844f49400287e739b36aa2062` | 0 |
| crates/bitwarden-api-api/src/models/password_manager_plan_features_response_model.rs | 5232 | `5b310b4856045842f556e5cd7893b3e3c0aa882612265077c081000e236ef969` | 0 |
| crates/bitwarden-api-api/src/models/password_manager_purchase_selections.rs | 1031 | `4bb98325c11cecf41e6150a403571e7a0223c5efe333ac594ecfa11958575bd7` | 0 |
| crates/bitwarden-api-api/src/models/password_manager_selections.rs | 1134 | `51a9753df65452325d70de5739be6173e84a9650e2b59b3031767bda60e66e2a` | 0 |
| crates/bitwarden-api-api/src/models/password_manager_update_selections.rs | 969 | `5cd06320411986eb6d25ea71d451f9b344c9bb4503124ffa3dbb66228d58052b` | 0 |
| crates/bitwarden-api-api/src/models/password_request_model.rs | 1838 | `f7f796e8cca2033374f8d414e3e96f1191ff6769c91bf67e89b1bc30bd0d5a96` | 0 |
| crates/bitwarden-api-api/src/models/payment_method_type.rs | 2713 | `add0cf8ee82bc4a3a8e0c55cdf4b59f4792d00e185986dfebae2fedc304b2a10` | 0 |
| crates/bitwarden-api-api/src/models/payment_response_model.rs | 1380 | `3d83ad8efd264e77b788181844ca666caa4b03d9aad498d6fa91f93331895302` | 0 |
| crates/bitwarden-api-api/src/models/pending_annual_upgrade_response_model.rs | 1743 | `4410d9c2da3291d6cf99a945e711bd9456be0a907bc892fe70e4aa88999d7a44` | 0 |
| crates/bitwarden-api-api/src/models/pending_auth_request.rs | 865 | `f3f4cfb09be113093441cd490bcf0c754dbb243174c09ba064387960d53db1e1` | 0 |
| crates/bitwarden-api-api/src/models/pending_auth_request_response_model.rs | 3672 | `6be026cdc3ca0ef9dc65ea7603707028b182481b54037b23bff2e824b1e16f2e` | 0 |
| crates/bitwarden-api-api/src/models/pending_auth_request_response_model_list_response_model.rs | 1389 | `b839b52717e8b48b1fa82b977a8c84d856a0c188497ae724658dba83b59c8753` | 0 |
| crates/bitwarden-api-api/src/models/pending_organization_auth_request_response_model.rs | 2864 | `638fbd2857129cc989b68e82c5879b0d2105a674e67567cc9a47a23be970ce8f` | 0 |
| crates/bitwarden-api-api/src/models/pending_organization_auth_request_response_model_list_response_model.rs | 1465 | `be27ce4eefde471b0c34506159ce8ebbab5a280c864000b564dfcf758eec14f0` | 0 |
| crates/bitwarden-api-api/src/models/pending_subscription_change.rs | 937 | `f1a0562f7351bc5ae1874b5876f9031fcdebeb38fabed9bee524d189a2a551ec` | 0 |
| crates/bitwarden-api-api/src/models/people_access_policies_request_model.rs | 1149 | `5b33c43555e4f787a161715fb8cac5bfa4325500a66c708b363d6963ef6df546` | 0 |
| crates/bitwarden-api-api/src/models/permissions.rs | 3300 | `019e0b9804658abc7404831b07a45a153480dc5241637353002ed649d796832d` | 0 |
| crates/bitwarden-api-api/src/models/plan_cadence_type.rs | 2234 | `5965de5dafe46c660b685dc0804859ac6606be1844ce6bb5478a24a6165c8d25` | 0 |
| crates/bitwarden-api-api/src/models/plan_response_model.rs | 6550 | `0de1e03edd0e28df0c7e28750e240232e9705904303078a056e1ef78cd703b14` | 0 |
| crates/bitwarden-api-api/src/models/plan_response_model_list_response_model.rs | 1305 | `b030522f643c477c8f02733819d1f42c21d300e6a030cf76ea9820fe31e96ffb` | 0 |
| crates/bitwarden-api-api/src/models/plan_sponsorship_type.rs | 2261 | `a363f5a155d7e370441db240d051e02e77143091f83082f47f918c5a70d50c5e` | 0 |
| crates/bitwarden-api-api/src/models/plan_tier_type.rs | 2352 | `480ed010c2f8499eb22fd8dbf8cf376b6fbdc4ef169a44f1042ced2e4cbdf5e3` | 0 |
| crates/bitwarden-api-api/src/models/plan_type.rs | 4442 | `d1bf7fb0800bec16e80037d4a9932809fb7307285c9d94ffabfa5d53c6ed9c09` | 0 |
| crates/bitwarden-api-api/src/models/policy_request_model.rs | 849 | `069c191d53ac63286d4da4cd11de70a2bee501b5fd8bbd1c4f97a6280e319998` | 0 |
| crates/bitwarden-api-api/src/models/policy_response_model.rs | 1817 | `063b1ea6983ccaf1ebfe2eb9be9edc2466faafb737bbb112641e8777c540f297` | 0 |
| crates/bitwarden-api-api/src/models/policy_response_model_list_response_model.rs | 1317 | `508fe6993b1c7620c599e8cf72388e679329357bc57fd7f4abc9f0129bf45737` | 0 |
| crates/bitwarden-api-api/src/models/policy_status_response_model.rs | 1773 | `fcdb7fa1d2df7071acec72f1e2693a3cf45497a7cde3363ce762dff48fd732d7` | 0 |
| crates/bitwarden-api-api/src/models/policy_status_response_model_list_response_model.rs | 1353 | `ee1a6e88af46a6861034297de3bca9817fa020a164df312490742c9ad6b83a18` | 0 |
| crates/bitwarden-api-api/src/models/policy_type.rs | 4631 | `f2a0c5aa6fc031d79942fc133d7d4ab68b42d0121ca4b5d71665e5b9290e28bb` | 0 |
| crates/bitwarden-api-api/src/models/potential_grantee_response_model.rs | 1836 | `3a7531f5d30dd6e835ae79dcfcd6beb1d82931e55d5b451a825be79a52d8d399` | 0 |
| crates/bitwarden-api-api/src/models/potential_grantee_response_model_list_response_model.rs | 1377 | `9f1ad73437720548e93b0df3ea571f3ec0f9e09ee476217321fd351897519874` | 0 |
| crates/bitwarden-api-api/src/models/pre_validate_sponsorship_response_model.rs | 1320 | `1bfed22e647e0692ed3e2574b0a0eff8759bbea9a9f2de9726285444a801e5e6` | 0 |
| crates/bitwarden-api-api/src/models/premium_cloud_hosted_subscription_request.rs | 2076 | `2740d47f71f15267d36d783f87d46b4415899eac836e0e646bdbe55194117099` | 0 |
| crates/bitwarden-api-api/src/models/preview_organization_plan_change_request.rs | 1137 | `8f54d91d715aa2f728ad614b14b26af2909cf6321ccdae2b7e30ec4bc6ba7d0c` | 0 |
| crates/bitwarden-api-api/src/models/preview_organization_subscription_plan_change_tax_request.rs | 1130 | `7e94f1a64f627b92593f0aaf1ea122ecbb1a80794899e12c96329b8826c3b6d3` | 0 |
| crates/bitwarden-api-api/src/models/preview_organization_subscription_purchase_request.rs | 1091 | `024fc9705e59409dd71f629248b46fd657334b92642efc2ad08e270d71042917` | 0 |
| crates/bitwarden-api-api/src/models/preview_organization_subscription_purchase_tax_request.rs | 1142 | `6f969706e573ab12d579670c8e38209406240f694652935905564ab55fa04f58` | 0 |
| crates/bitwarden-api-api/src/models/preview_organization_subscription_update_tax_request.rs | 863 | `e7e2e57edbc2bff3f42d145a61d3fd8db5b63285403efb5a72350f7448bed2e4` | 0 |
| crates/bitwarden-api-api/src/models/preview_premium_subscription_purchase_tax_request.rs | 1243 | `e5fcddf286a3ebdf05ed82a2a7f42c958790f8747baa9e165cc76e5b3c1cb46d` | 0 |
| crates/bitwarden-api-api/src/models/preview_premium_upgrade_proration_request.rs | 1093 | `dcc758ac3835cfe04ab9bb7aecbcb2ec1786664cb76b185124de0619ac586d0b` | 0 |
| crates/bitwarden-api-api/src/models/priority.rs | 2373 | `d2693e35a9ac2061223c76f5664b3c27bbc3b6930c74852a72fd52c0803b56ca` | 0 |
| crates/bitwarden-api-api/src/models/private_keys_response_model.rs | 2226 | `1d18a0eee83d09cc284e8004dc87f6d346871fed01179e70970fbf68608f85c9` | 0 |
| crates/bitwarden-api-api/src/models/privileged_controls_invoice_items.rs | 993 | `9ce8d366018502d668a4ab8284ced5ce8fe473b01cf0c9a072999d8407717c57` | 0 |
| crates/bitwarden-api-api/src/models/product_tier_type.rs | 2470 | `305cf610985c79e2d9850e1621a0a0d9a6b4d619a5150cc751bbb5bf273417fe` | 0 |
| crates/bitwarden-api-api/src/models/profile_organization_response_model.rs | 14984 | `bd779621edcfebafa236982557cabfa4178f9ab5d07bbe4c566256ab47276940` | 0 |
| crates/bitwarden-api-api/src/models/profile_organization_response_model_list_response_model.rs | 1395 | `014dcdfefcfb94b11a5c9e8b521e9f8b3874418df611f0145b45e2d9a9531573` | 0 |
| crates/bitwarden-api-api/src/models/profile_provider_organization_response_model.rs | 12956 | `0ec32701a1be5b4b995d54ee1afea23d898f1ba210b2746fe4e720874e35dc03` | 0 |
| crates/bitwarden-api-api/src/models/profile_provider_response_model.rs | 2811 | `ae53a5c53f2792bc824dcb381218b1ad7212408266638682dcadec49aaa589ab` | 0 |
| crates/bitwarden-api-api/src/models/profile_response_model.rs | 5312 | `8f91b6058bb46d6cb41502ef651590266db0951274a74c73600ad05ccdd9b0b1` | 0 |
| crates/bitwarden-api-api/src/models/project_counts_response_model.rs | 1304 | `6ce7bad79f4d44500309a9aef9cb3e57dd83f27bc2433586685d7775e077f920` | 0 |
| crates/bitwarden-api-api/src/models/project_create_request_model.rs | 628 | `62d4201fa5d8495ecf3f6ee41d3548cb777d0c6bb78ef19e9dc3434d4e134787` | 0 |
| crates/bitwarden-api-api/src/models/project_people_access_policies_response_model.rs | 1329 | `e453feb4a0ff6eb2ec9436337810a34c43ddece6025aa262d0f5fa9c7761e91d` | 0 |
| crates/bitwarden-api-api/src/models/project_response_model.rs | 1987 | `a74702a93af1ca2a2434a303828b44c5fe4fd90fda4086254ffeb5e1248fbcd5` | 0 |
| crates/bitwarden-api-api/src/models/project_response_model_list_response_model.rs | 1323 | `198d2f07b497d06836702de74bccbb8c1c550dc3193d77c3ccccbe5f6fedbc33` | 0 |
| crates/bitwarden-api-api/src/models/project_service_accounts_access_policies_request_model.rs | 1008 | `b593773c4dd7b1e36f6cb367cee55c1c44455e61b1f34c06fe37588571edf10d` | 0 |
| crates/bitwarden-api-api/src/models/project_service_accounts_access_policies_response_model.rs | 1153 | `7589a9c96014e9d9dc7ebbd5e3ec53a42f7a26935abd298af7fec3684b1c3048` | 0 |
| crates/bitwarden-api-api/src/models/project_update_request_model.rs | 628 | `e81a3206974f624363bf98f053d00cd734271a31107dbf17c726c5177492ef40` | 0 |
| crates/bitwarden-api-api/src/models/protected_device_response_model.rs | 2093 | `830326df311978aaab4d52fe139bfde58635f7a288b26f2deb28012890bcb92c` | 0 |
| crates/bitwarden-api-api/src/models/provider_organization_add_request_model.rs | 845 | `aac8714e40e5166c03e5fe669c1e7fc6406f64f59fe6f678b8645bf63133a461` | 0 |
| crates/bitwarden-api-api/src/models/provider_organization_create_request_model.rs | 1131 | `ca8477715e49fff2d108ba477bd5b1007d35f3a8a91cf408e1782a6b473930a0` | 0 |
| crates/bitwarden-api-api/src/models/provider_organization_organization_details_response_model.rs | 3297 | `af08d654362e47aca0b25253f2e23ed1f8cbe8accba553158ac355e2d80772bd` | 0 |
| crates/bitwarden-api-api/src/models/provider_organization_organization_details_response_model_list_response_model.rs | 1519 | `626ef325635b90d0471be0fbc1dad8e33c8580ec6c3f57c8f8d62c94e367e311` | 0 |
| crates/bitwarden-api-api/src/models/provider_organization_response_model.rs | 3000 | `92d050f4846871ef616c77aae01ee1c6ab665fde94096e13c7854f150419fd60` | 0 |
| crates/bitwarden-api-api/src/models/provider_response_model.rs | 2935 | `b141246a4c758f00d68ac097925a1a0c4d1052628fe884149d89c7335715c34e` | 0 |
| crates/bitwarden-api-api/src/models/provider_setup_request_model.rs | 1738 | `235818f2d581443427ed35a3b84416265d5ec028f190f403aa611aeae3fe4d56` | 0 |
| crates/bitwarden-api-api/src/models/provider_status_type.rs | 2349 | `f1053836df4b43773149a3330e59f8c88d0f9041baf9441cae69a8c37939ff3c` | 0 |
| crates/bitwarden-api-api/src/models/provider_type.rs | 2270 | `2eb0a24b5d256c477b689589a9ea6490f3c97cbe47b3a5da31b220ed512130eb` | 0 |
| crates/bitwarden-api-api/src/models/provider_update_request_model.rs | 1001 | `82286f5644e19c1e0c670750c728044596ce2702ff6cf91b45e910104291212b` | 0 |
| crates/bitwarden-api-api/src/models/provider_user_accept_request_model.rs | 653 | `91538a8cc8ce786d78b22a451b42a895762937984f99d7a5dc0e71a6d349b159` | 0 |
| crates/bitwarden-api-api/src/models/provider_user_bulk_confirm_request_model.rs | 777 | `6fdbc356c2242ec5e5533068a2870ba630893489f16e9d0948d5cc75b34d4e85` | 0 |
| crates/bitwarden-api-api/src/models/provider_user_bulk_confirm_request_model_entry.rs | 769 | `5a29c63ba8b1f0830b943af577a97568c2e95e1a209e71a5c3b5a73cac5db154` | 0 |
| crates/bitwarden-api-api/src/models/provider_user_bulk_request_model.rs | 653 | `fc95b7a425a44033c8e3b57e21f1f3d552d616c5e0cf1f6edef5ae4a9e0f8cb9` | 0 |
| crates/bitwarden-api-api/src/models/provider_user_bulk_response_model.rs | 1058 | `87303b39e310707e9129cab6c1db933d5923c8f5a6f5826b92d8df0010af4703` | 0 |
| crates/bitwarden-api-api/src/models/provider_user_bulk_response_model_list_response_model.rs | 1377 | `bb03159811bd98114817712de12d822e7336b1c0097b3877fb29860f59bc6755` | 0 |
| crates/bitwarden-api-api/src/models/provider_user_confirm_request_model.rs | 647 | `23ae1c639cdafba41c79cf3e406fa6f552632d1daaf76c7995b86bea9780cbd7` | 0 |
| crates/bitwarden-api-api/src/models/provider_user_invite_request_model.rs | 823 | `0b7abf27132ae40f6b205784b3acf97eb8ee0dfd66c8164a59116b301625534c` | 0 |
| crates/bitwarden-api-api/src/models/provider_user_public_key_response_model.rs | 1225 | `8d3d5a2f33ff207ac9e33819ecb2d1c0a72cd388bcc3d91f5b382529236f6d40` | 0 |
| crates/bitwarden-api-api/src/models/provider_user_public_key_response_model_list_response_model.rs | 1407 | `ba8e1c97d9c3acf341eecf292acf43ac992edfdbdaa70cbf132f21ca599748a1` | 0 |
| crates/bitwarden-api-api/src/models/provider_user_response_model.rs | 1667 | `21800f7dd8ab226795d28ab6d603a2f660854875bd7e9b2dd878d1b7d599d131` | 0 |
| crates/bitwarden-api-api/src/models/provider_user_status_type.rs | 2407 | `fc9cfb27401d30067c40ea91bcb84aa23a26059048f678d509f246b34f39efeb` | 0 |
| crates/bitwarden-api-api/src/models/provider_user_type.rs | 2279 | `e684a35777d582a246e18cfc8a6a9167ca6b58a3f30ac75333722355e50cf0a7` | 0 |
| crates/bitwarden-api-api/src/models/provider_user_update_request_model.rs | 692 | `fa8f0a05c80022ee4a7beb0037569a33e27b41e841c794fd4ab6b5a739ef6577` | 0 |
| crates/bitwarden-api-api/src/models/provider_user_user_details_response_model.rs | 2057 | `20a4ab9163f8a21f43626ae04e7a96ebe7dd36720361c21d4b00cea8282de1fc` | 0 |
| crates/bitwarden-api-api/src/models/provider_user_user_details_response_model_list_response_model.rs | 1419 | `79f251586bad75c796ec56ee9f3bc9f6a7a2f79a5aa8e906947e1108e2083165` | 0 |
| crates/bitwarden-api-api/src/models/provider_verify_delete_recover_request_model.rs | 689 | `7a66dff6230402a576d1eaa6886aa7fcc2b16340ed3782f65ecf6f8ae6a94032` | 0 |
| crates/bitwarden-api-api/src/models/pub_key_cred_param.rs | 861 | `c155511a3ead8c88692e6d5b79a1a783441dfff9c1635b376d44bf1656b29676` | 0 |
| crates/bitwarden-api-api/src/models/public_key_credential_descriptor.rs | 1298 | `501616e0d127e640cf23d891e598547a912854762b58f760bb5aa2e110844e19` | 0 |
| crates/bitwarden-api-api/src/models/public_key_credential_hint.rs | 1241 | `c820e7c59c0067330c4c4fb42103855d1a4ef83bd774dd6ddb0923f1fca6a1f9` | 0 |
| crates/bitwarden-api-api/src/models/public_key_credential_rp_entity.rs | 1034 | `8f83053f683046a7dd148b5887d5de668f8aa268d0ad1274fd573fb38a2cf811` | 0 |
| crates/bitwarden-api-api/src/models/public_key_credential_type.rs | 1116 | `8bbf9993405248cfc8402b45a17a369441414e3154f2af2eeb6f37bb43639a3f` | 0 |
| crates/bitwarden-api-api/src/models/public_key_encryption_key_pair_request_model.rs | 1174 | `1a0e35a183b2f96e269db9d6bd401c42055a9661c7ad6abb3ecc699615f619a8` | 0 |
| crates/bitwarden-api-api/src/models/public_key_encryption_key_pair_response_model.rs | 1357 | `f49c151006b32cb152135395556954f0dc62294803a9f291467f039c6351ddd7` | 0 |
| crates/bitwarden-api-api/src/models/public_keys_response_model.rs | 1842 | `365ab646b7abf7cde904179babf1be3e68b7aa93acacb5896b95a4d4dcb701da` | 0 |
| crates/bitwarden-api-api/src/models/purchasable_proration.rs | 1225 | `d7871d1b771ddeef7a98ba897603dce19f3f047eded390a2adb954556263637e` | 0 |
| crates/bitwarden-api-api/src/models/purchase_selections.rs | 1592 | `46f250d307f55d4b5eb52c9c5e224cc43499e19890f1abf06a88f3f4718efffb` | 0 |
| crates/bitwarden-api-api/src/models/push_device_request_model.rs | 606 | `e75f4474b72ffd49640dbdeb2e471591dd2c31d07d3ceafbe7ede85d3d5db04b` | 0 |
| crates/bitwarden-api-api/src/models/push_registration_request_model.rs | 1673 | `772cafb25088ac2217da13699469190bd0bf8bcd7fd45a35c5cb173a3707d41c` | 0 |
| crates/bitwarden-api-api/src/models/push_settings.rs | 947 | `7b4d13ac63b1636a5431e1438e5e3e2224f6ce9accdd24e71ad3826f8d26b2e7` | 0 |
| crates/bitwarden-api-api/src/models/push_technology_type.rs | 2269 | `c50f2ee1083fcbb5c9545530914ebc0e55097aa7b24d99074cb4a2703e7ccf4c` | 0 |
| crates/bitwarden-api-api/src/models/push_type.rs | 5255 | `b44f8212fb4c50b802ef14e9179e1175c1408a6fe30f8846810625aa035af103` | 0 |
| crates/bitwarden-api-api/src/models/push_update_request_model.rs | 886 | `3904e0eb6af0dd2a3b43df5435a249bfea838ec5d51141402d51126d50bddbac` | 0 |
| crates/bitwarden-api-api/src/models/refresh_organization_invite_link_request_model.rs | 1116 | `4e79c37660f6d538ac6480a37b2d6db417eefb48e7cfbf844b528edcd6ad0bc3` | 0 |
| crates/bitwarden-api-api/src/models/register_access_connector_request_model.rs | 2814 | `8c1e15e0bbb719045f9c35fd51a2ac9132816113e2a0a75bfd6e49bc4789446f` | 0 |
| crates/bitwarden-api-api/src/models/register_access_connector_response_model.rs | 3200 | `3342d88945ae8b424a1e06430c3675abcf6fe39d9a3258addf9f51dc35949e5c` | 0 |
| crates/bitwarden-api-api/src/models/register_target_system_request_model.rs | 1080 | `79003c28a2a6fde3eb0fb4f30bd4d5060a3a5f31ce70676b4b7d78573b35a26e` | 0 |
| crates/bitwarden-api-api/src/models/report_file.rs | 1353 | `cb3e1dc47348bf05776528aa95424667480b2bfa218891d44da0bf05d5b5199e` | 0 |
| crates/bitwarden-api-api/src/models/report_rotation_failed_request_model.rs | 2316 | `2d23244f3b5f5c12070b8a4a2981f604a2d67ebd68d780b0c5058338d70c9d8e` | 0 |
| crates/bitwarden-api-api/src/models/report_rotation_succeeded_request_model.rs | 1017 | `6122f1c3e0a0e1dc8f653a911cc53cfd0efe5f474022efb8cc884c33047d7617` | 0 |
| crates/bitwarden-api-api/src/models/request_sm_access_request_model.rs | 861 | `7e74e1a456781b4ff1633e01896c7a0912741aae4fe311bb9923d64fefab9206` | 0 |
| crates/bitwarden-api-api/src/models/resident_key_requirement.rs | 1226 | `410c25646c190ca295d5fd49498042fada327cee2cd804e3e59e0ca60b68ca5a` | 0 |
| crates/bitwarden-api-api/src/models/restart_subscription_request.rs | 1078 | `3d7d0c60234c96944e97d22eb30c957a481b2c01dd48e1b68a7466ce9650c4db` | 0 |
| crates/bitwarden-api-api/src/models/restore_secret_version_request_model.rs | 692 | `ac03ad0ac086d67642a12de37797e1da1a08185ee01484b6d23370d1ffdc82b8` | 0 |
| crates/bitwarden-api-api/src/models/revocation_reason.rs | 2835 | `f02ae0d8cba7d58d39dba112422642ced3c85a65b5f27bbebed9dc60a189614a` | 0 |
| crates/bitwarden-api-api/src/models/revoke_access_tokens_request.rs | 641 | `1c1bb6d3409b12c9e5180821e6fb7a6a7e47b006e57ca9f6f654ebde98baef05` | 0 |
| crates/bitwarden-api-api/src/models/rotate_user_account_keys_and_data_request_model.rs | 1826 | `8d925f0d166fca49ca9bbe34842b0a029929daa3ed2a5b9e67906acf4569dbaf` | 0 |
| crates/bitwarden-api-api/src/models/rotate_user_keys_request_model.rs | 1915 | `b532ac38e3d7621e385d1d746328d0c258da4c584541526359e07226e0a11cd7` | 0 |
| crates/bitwarden-api-api/src/models/rotation_cipher_response_model.rs | 2549 | `308f8fb25d449eda8f669efe47a211e95590e83907309b15c5a06621bdab6671` | 0 |
| crates/bitwarden-api-api/src/models/rotation_claim_response_model.rs | 3930 | `aacdfb37d4fa18864d38bd7eed99e4eef26110155f95976deb589488d4c1910d` | 0 |
| crates/bitwarden-api-api/src/models/rule_bypassable_ciphers_response_model.rs | 1684 | `faa7e18ff3263782e4e8a4b2d021a1146a142e62c00ae2293a70a52eb705c2ea` | 0 |
| crates/bitwarden-api-api/src/models/saml2_binding_type.rs | 2266 | `37aa70f5285b96a49547a24bd375ecf73fd067cefd62e5eb9fbc12e5c27cbb2c` | 0 |
| crates/bitwarden-api-api/src/models/saml2_name_id_format.rs | 3011 | `b505c679251094fa891f1f04a32884b8890e1624ba3b9a0794dc95b5a5d1edd1` | 0 |
| crates/bitwarden-api-api/src/models/saml2_signing_behavior.rs | 2447 | `96fcff828b1abe464b112327fd2c1fd1a7fcc4534c15017513d0ab1d67a877ef` | 0 |
| crates/bitwarden-api-api/src/models/save_policy_request.rs | 923 | `c757264b5676d8e44ed33e86e7696dd6de9c541e06ffa4281691c671dd52e600` | 0 |
| crates/bitwarden-api-api/src/models/secret_access_policies_requests_model.rs | 1567 | `29ec7abf687b9ab85dc05cfaa2b8d38a704043e27b42b50c75815f6e2500119a` | 0 |
| crates/bitwarden-api-api/src/models/secret_access_policies_response_model.rs | 1628 | `cfa11ce2179b68a6033e3540546174dc726bd5a5c73e42b5af755149ca5c3593` | 0 |
| crates/bitwarden-api-api/src/models/secret_create_request_model.rs | 1338 | `aba60af87f52c0cb2c30fc2ec401829dab817a181f1ddac90eee89cd12bac5cd` | 0 |
| crates/bitwarden-api-api/src/models/secret_response_inner_project.rs | 863 | `fc7976f95c9327d3beb47acb4b6813cee9e8fb918c55ac7826ce285e8b00d0d0` | 0 |
| crates/bitwarden-api-api/src/models/secret_response_model.rs | 2515 | `d91f13581b858687c806ad2a71c41f98527661c42d33729655f9476814ef77df` | 0 |
| crates/bitwarden-api-api/src/models/secret_update_request_model.rs | 1541 | `f0e4e7b2578183f653445f58a7b21f2c54bc86f61c4c4838bf676bc6fd1879d7` | 0 |
| crates/bitwarden-api-api/src/models/secret_verification_request_model.rs | 1363 | `793adde20b793763cf285234ee09e178e725f71d291e3b7a476ca30503e393f5` | 0 |
| crates/bitwarden-api-api/src/models/secret_version_response_model.rs | 2476 | `65282051456a09ba83cf3ab69a731461cbc277f94fd45ecdd480dfe7fbe4d340` | 0 |
| crates/bitwarden-api-api/src/models/secret_version_response_model_list_response_model.rs | 1231 | `85c588606d4950a949e88db54493411a9dcc1bdb7cda32b66b2ea7819a9160d8` | 0 |
| crates/bitwarden-api-api/src/models/secret_with_projects_inner_project.rs | 879 | `e594f0b65a806527d25a6a8cb5d631e6a2e2326fc4186ca5451595d2c8378c3f` | 0 |
| crates/bitwarden-api-api/src/models/secret_with_projects_list_response_model.rs | 1214 | `361a87cfb857e5795c50e0fd3ba3b7d488ec086029d162c6f88adafdb86b5270` | 0 |
| crates/bitwarden-api-api/src/models/secrets_manager_invoice_items.rs | 1261 | `46e58449aa81dea7b04f8ee14a3bb69d91b43fd117075f910aa303a917abb835` | 0 |
| crates/bitwarden-api-api/src/models/secrets_manager_plan_features_response_model.rs | 4343 | `b591bc6f4da988fd27da8dcb03476099c639f08d9d92629cd50700df405782b9` | 0 |
| crates/bitwarden-api-api/src/models/secrets_manager_purchase_selections.rs | 1096 | `e2fc216c685255df2bd50593cd0e393d1f87a3574825d195596eea2a68869f53` | 0 |
| crates/bitwarden-api-api/src/models/secrets_manager_selections.rs | 1168 | `85d87bea8b9f4c4432ee1abd5649c789a3ec54ce3256fd01ddc765b4ef3fc62e` | 0 |
| crates/bitwarden-api-api/src/models/secrets_manager_subscribe_request_model.rs | 1004 | `4cce07e8f4d951bfd5b96dbb3489e0ff72e8bbe6cf34b1b844fcabec29a026e7` | 0 |
| crates/bitwarden-api-api/src/models/secrets_manager_subscription_update_request_model.rs | 1514 | `6f758e3c767265900975be0b9a3df471b79dc227419a93e8cc1fa45d7af00d8c` | 0 |
| crates/bitwarden-api-api/src/models/secrets_manager_update_selections.rs | 999 | `12174b39558cbbf98c9a74d9480a14957527d60f8c286e11dc278c965f97fd78` | 0 |
| crates/bitwarden-api-api/src/models/secrets_sync_response_model.rs | 1151 | `7af9325767ed62187a88adeb9540037dd9cbdebd11ee8f154d028a4c88181ef6` | 0 |
| crates/bitwarden-api-api/src/models/secrets_with_projects_inner_secret.rs | 2038 | `0fa2856f4518eec1fc2f76f57f808f329345bc88118a9453dc3195bf0ce5c410` | 0 |
| crates/bitwarden-api-api/src/models/secure_note_type.rs | 2140 | `5a38b5ecdd0a2d8c8d75c25f65707cbaff513462ec4f2edb5b42ea18d5494377` | 0 |
| crates/bitwarden-api-api/src/models/security_state_model.rs | 837 | `711a43436cb03bfa281d4ef89a38999e8212cd9f2bddb3b2828b94029cc954c9` | 0 |
| crates/bitwarden-api-api/src/models/security_task_create_request.rs | 939 | `8f8846c2f335039caf98054015800910b7d8ef50ae599a4dc283c27562a5bef2` | 0 |
| crates/bitwarden-api-api/src/models/security_task_metrics_response_model.rs | 1132 | `c2330561407520addcde83da4cbbba8ceaeaf50e68f3814c7847b40e7b9316ee` | 0 |
| crates/bitwarden-api-api/src/models/security_task_status.rs | 2275 | `7fe5192f8f5bd2011745833ec8b1ba335112db1682bb4b50fa86f4b91407a7af` | 0 |
| crates/bitwarden-api-api/src/models/security_task_type.rs | 2226 | `48444d96f6f551d045049e1e575170a53e5b40a054225f81362f108a02b6bfc0` | 0 |
| crates/bitwarden-api-api/src/models/security_tasks_response_model.rs | 2085 | `9b1d4444743b210cc2b52e4febdb61c29281c69fa993364fa231f8d7142b6cd4` | 0 |
| crates/bitwarden-api-api/src/models/security_tasks_response_model_list_response_model.rs | 1359 | `83967303289eb168f653e11c6edd62d0c43c1e09c48489a33eadb4ae5d2316c0` | 0 |
| crates/bitwarden-api-api/src/models/selection_read_only_request_model.rs | 1234 | `98f86dc5c2d57b267fe9a19e333ee6863090ac2fbb7794e39b03f716e4a68ea5` | 0 |
| crates/bitwarden-api-api/src/models/selection_read_only_response_model.rs | 1279 | `261e01c736e876c2f38b8d68fe08f097a4c15cde343d51053eada858e978b31c` | 0 |
| crates/bitwarden-api-api/src/models/self_hosted_organization_license_request_model.rs | 1027 | `4586d0eba172dce4602005f81f5fd3cecc073dae05a436f34c34df07b5ef7f5d` | 0 |
| crates/bitwarden-api-api/src/models/send_access_response_model.rs | 2916 | `64318782ca7547a74b87ac419878ff839f500810a9bec16ec6d8182e6d73b18e` | 0 |
| crates/bitwarden-api-api/src/models/send_data_model.rs | 1108 | `a39ae32d614e2c18c079fc347474a8452e057a7f39914c3676d842f2cbd22e41` | 0 |
| crates/bitwarden-api-api/src/models/send_encryption_type.rs | 2172 | `9ec4aa19ff5f13349fd0a72f67b201d77044c598ce8db8ae5f12d062a32a62c1` | 0 |
| crates/bitwarden-api-api/src/models/send_file_download_data_response_model.rs | 1032 | `15f64ec1cc2bcfdee6dc7515121c84030a35b01bf3874867064c05da687bad6d` | 0 |
| crates/bitwarden-api-api/src/models/send_file_model.rs | 1185 | `0c27efc9e33182e827c0c8d432634a6f6f3edfc24ab8c7ca6ee3734b799c0592` | 0 |
| crates/bitwarden-api-api/src/models/send_file_upload_data_response_model.rs | 1351 | `42ada555ccedce686b5950a8a10ea8ab0baf6e1aedb5aea05e9a6120667c759a` | 0 |
| crates/bitwarden-api-api/src/models/send_item_metadata_model.rs | 633 | `7b06f8d95f2cd91c9d4324939f76031b0a7779e8b939afac3f9cb2711d63e4db` | 0 |
| crates/bitwarden-api-api/src/models/send_request_model.rs | 4889 | `6c7310a977dc097378c35f1e3f7033c045efe70f5c388da389d6318350e3548e` | 0 |
| crates/bitwarden-api-api/src/models/send_response_model.rs | 5741 | `a5c5f8ecc2f57c8c163edb75d182d39e063aa0054b4576825297a6f259c9de15` | 0 |
| crates/bitwarden-api-api/src/models/send_response_model_list_response_model.rs | 1186 | `e16d72339f08d3b86fa8089aa059c650716bb4e9865c04c103a66690737c146e` | 0 |
| crates/bitwarden-api-api/src/models/send_text_model.rs | 851 | `ca7a627659115d14b185ea3c096f6f135fa878b8b5fd918f83d3b45fba02899b` | 0 |
| crates/bitwarden-api-api/src/models/send_type.rs | 2186 | `527e63759d1a6009afcf59a0d1705d373715465b8eaade2154640bb3b79f5de5` | 0 |
| crates/bitwarden-api-api/src/models/send_with_id_request_model.rs | 5141 | `d1e4d7f00e22dcd8595a108dd4b8745410ed73f83df3da17a3e5ec3677a77aac` | 0 |
| crates/bitwarden-api-api/src/models/server_config_response_model.rs | 859 | `6355a93df97d6ee380b2014ee7307744e4db1ffe9a4b760ac0bcb01da46df200` | 0 |
| crates/bitwarden-api-api/src/models/server_settings_response_model.rs | 1338 | `c446f4b3c51919cc0a614cc7f2f32f425be9ee7fa73d9c32705ff9c836950174` | 0 |
| crates/bitwarden-api-api/src/models/service_account_access_policy_response_model.rs | 1586 | `99df3373728b3099b6417a2cb647d2ac0b23fb328adad9ca4a6923bfc9bc5afa` | 0 |
| crates/bitwarden-api-api/src/models/service_account_counts_response_model.rs | 1324 | `0337ccf5bf84bde11801cbe17688ed6e4e9cff0122792ece40981242d0096803` | 0 |
| crates/bitwarden-api-api/src/models/service_account_create_request_model.rs | 656 | `c68440dd376a00d5dc52bce0f99e1e24f35dd780c50b19fd7ebff4ecec4c95cd` | 0 |
| crates/bitwarden-api-api/src/models/service_account_granted_policies_permission_details_response_model.rs | 1184 | `494205b1f9d483337dff94b7d740486645f7cf1350ee5ac559602e5d6cd4aac3` | 0 |
| crates/bitwarden-api-api/src/models/service_account_granted_policies_request_model.rs | 961 | `6a68dd5513b7e2b28d2f56d64b9d4971c326b1443a160064bb73a0d50a47f2d3` | 0 |
| crates/bitwarden-api-api/src/models/service_account_people_access_policies_response_model.rs | 1357 | `2fd770d8c0df0e1e5f98f75d1724ff80073a4a69c2411a140cf076199c023336` | 0 |
| crates/bitwarden-api-api/src/models/service_account_response_model.rs | 1673 | `4bb3f76fd3bcf64f168523821b68c1afdf908e7b8b5810a02498ef8984c8c79c` | 0 |
| crates/bitwarden-api-api/src/models/service_account_secrets_details_response_model.rs | 1945 | `b375c30c3e63b2bfbde80c0899f7589a4a5e90e646882f2e2e44448d0e519962` | 0 |
| crates/bitwarden-api-api/src/models/service_account_secrets_details_response_model_list_response_model.rs | 1449 | `8acffab36cafd05b326f765cde29bd2fbb8313be62ed1a9c9dad8f89872767ad` | 0 |
| crates/bitwarden-api-api/src/models/service_account_update_request_model.rs | 656 | `9157a63dbd2f846545f82a9eb31c28f076372467c8e725fb3034793bc12c19bb` | 0 |
| crates/bitwarden-api-api/src/models/set_initial_password_request_model.rs | 3105 | `fe20db6bec428f9c91867d99d1bb702d34778b40b5db596e724ba4e077e2a281` | 0 |
| crates/bitwarden-api-api/src/models/set_key_connector_key_request_model.rs | 2892 | `2a1616b0d105d8d0909efc7d29e77b70d5ebb6647e5a183ee4c1e0e04cb430ac` | 0 |
| crates/bitwarden-api-api/src/models/set_user_key_id_request_model.rs | 714 | `c8050f7cf8ca7e9d6e53d354cdc2543eeb4259ea923c63cbdd1bf9286321ba0f` | 0 |
| crates/bitwarden-api-api/src/models/set_verify_devices_request_model.rs | 1497 | `83e9c6d7980853f559a282a7026c27e1904425a7e3a0e6b758402ec0a03c2d1a` | 0 |
| crates/bitwarden-api-api/src/models/setup_business_unit_request_body.rs | 1122 | `f3a63300a01ffeb5d8c01d544c955104277d7d0b067c7b3b3d5e6687a78dbcd3` | 0 |
| crates/bitwarden-api-api/src/models/signature_key_pair_request_model.rs | 1127 | `73b95bb30319164a767b7ece2bfde0f65165b7dd83241f0255d7f2497fdc87fe` | 0 |
| crates/bitwarden-api-api/src/models/signature_key_pair_response_model.rs | 1113 | `bb1b13ce822fee294fd151be7a46c6c81397b32142ee98f7fa0a9f7d527c5c7a` | 0 |
| crates/bitwarden-api-api/src/models/sm_export_response_model.rs | 1159 | `570f3439950e8e56132b8257bf08ef71a199c7753e79c8423571874367244292` | 0 |
| crates/bitwarden-api-api/src/models/sm_import_request_model.rs | 974 | `8cf01edfec7c1f58a4f255f1e6c90bbb29bd10c1dd33b880646739d6a7173653` | 0 |
| crates/bitwarden-api-api/src/models/sso_configuration_data.rs | 8839 | `78217ffbc2fe3eb7da96b250822e7d64f614fc9f0d76c05fb1f09f9ea7b4c85c` | 0 |
| crates/bitwarden-api-api/src/models/sso_configuration_data_request.rs | 8538 | `771b42da54bca1cf94eccaff21b847d75fe4f4a6fea63e58921971a80b9b0a43` | 0 |
| crates/bitwarden-api-api/src/models/sso_type.rs | 2144 | `ae482c6e94058b28323ddf7dc95a834aaaf41d0243bf568819316dafe5911b35` | 0 |
| crates/bitwarden-api-api/src/models/sso_urls.rs | 1755 | `2218ab689babb27c172594b8732bc3c40f159a5a7ba64da58a33ff12665501e5` | 0 |
| crates/bitwarden-api-api/src/models/storage.rs | 1057 | `4c50cb9b279a4ca89733616530825eede9e1885abe2b920df56242274258bf73` | 0 |
| crates/bitwarden-api-api/src/models/storage_request_model.rs | 700 | `d8d4cfd230b34a6d3d5b5b8f149b2331fc897a18b0a040fe6d715d4430851039` | 0 |
| crates/bitwarden-api-api/src/models/storage_update_request.rs | 1195 | `044e6c691ff3976dd981d9633fcc60e8045585664e28463922ce17cb685c055d` | 0 |
| crates/bitwarden-api-api/src/models/string_authentication_extensions_prf_values_key_value_pair.rs | 1007 | `c6629ddedbf55884f589467a7e8df285afc07899a001f5d34a9adb16bcdc0511` | 0 |
| crates/bitwarden-api-api/src/models/submit_cipher_update_request_model.rs | 1276 | `32a811e04491676a59e9836914033afdb2e8bce3b75e8dfaa42c566d15a1bacc` | 0 |
| crates/bitwarden-api-api/src/models/subscription_cancellation_request_model.rs | 961 | `3a606e994a3a4f48271efddd9abd5a581364827ec18330b97f42c144b466ec36` | 0 |
| crates/bitwarden-api-api/src/models/subscription_preview.rs | 2098 | `f751bd3c7b08ce2aa16696b586b20974ec258144718bb7044f03158a8070285d` | 0 |
| crates/bitwarden-api-api/src/models/subscription_response_model.rs | 1520 | `c4a415b2cc2bae3d262e42198e446198dddb8df513408db75cbc253150373f50` | 0 |
| crates/bitwarden-api-api/src/models/sync_response_model.rs | 2896 | `65a40c8388c51b056fb56af8e507baa2a0edf94142f8869738b82ff6cec79170` | 0 |
| crates/bitwarden-api-api/src/models/tax_id_request.rs | 669 | `9eac50c6a9fd1a614596480c8cc381b5637c1b3c68d150cee2ac3e17eb331120` | 0 |
| crates/bitwarden-api-api/src/models/tax_id_selection.rs | 853 | `4e95cc793d6f8d93f7e9f8887288c6edf5ab7babcdc5934cd083b1f1852a680b` | 0 |
| crates/bitwarden-api-api/src/models/teams_channel_response_model.rs | 1131 | `4d63e737277e8f6824be7caefc2b5360ea83c386429d39b9bf3314954baf3a55` | 0 |
| crates/bitwarden-api-api/src/models/teams_channel_response_model_list_response_model.rs | 1226 | `ea17e7f71ec8f6303757ea1f845599c967436b0b7bcd8edcf7d86d2f669c8b16` | 0 |
| crates/bitwarden-api-api/src/models/tokenized_payment_method_request.rs | 1026 | `3d913a6cbb922ace5d9765958cf7adc3f93660265c83fac47c7836ed7037b9af` | 0 |
| crates/bitwarden-api-api/src/models/transaction_type.rs | 2502 | `e76ccaabdb7dc24202b47122fa4c2d8a7a7542e9df59c85f6934f97e12d5b391` | 0 |
| crates/bitwarden-api-api/src/models/trusted_device_key_data_response_model.rs | 1294 | `6c674187c3bd44129aa99f0c68b922bac388c2f8e073135a45e66ebf1563881b` | 0 |
| crates/bitwarden-api-api/src/models/two_factor_authenticator_delete_request_model.rs | 1417 | `13f248b3394bb273ea5c13d28ddf7dcc670687cfc45f013a5d47f325e9eabbf9` | 0 |
| crates/bitwarden-api-api/src/models/two_factor_authenticator_details.rs | 1237 | `1bb2d5340434f664d08e49abdf2cc8105099bcfc722b1ba3c7e11f1cc538ab50` | 0 |
| crates/bitwarden-api-api/src/models/two_factor_authenticator_response_model.rs | 1737 | `4a50e9f6cbf5c2a1190288328bbd0a786f053ec26b370df1adcd7d8c921697b3` | 0 |
| crates/bitwarden-api-api/src/models/two_factor_authenticator_update_request_model.rs | 1730 | `ce6ec60f89fc81ae0a9c75dbb0e3621b5281a9f784a8810dafd8c3b5b2c32d05` | 0 |
| crates/bitwarden-api-api/src/models/two_factor_authenticator_update_response_model.rs | 1233 | `a1b75e339cfecd43da7a06da6ec5dcb5d6922355d8cb2f16024669c05cee017c` | 0 |
| crates/bitwarden-api-api/src/models/two_factor_duo_delete_request_model.rs | 1143 | `c8ba7fc8197a270e3e9a066db1fa8738eece4d674b43a479e80668afbcc6545d` | 0 |
| crates/bitwarden-api-api/src/models/two_factor_duo_details.rs | 1839 | `3dd7584402a8fd4ad50f6871508c21b9649ef7c5ad84c490542bd08bbda06782` | 0 |
| crates/bitwarden-api-api/src/models/two_factor_duo_response_model.rs | 1620 | `0218523c09789fd05c4fa218288a3ff119c4e11a75a5104c8993fdcff97af5e8` | 0 |
| crates/bitwarden-api-api/src/models/two_factor_duo_update_request_model.rs | 1367 | `24b8ef77f572eb2653ab653e537b798921e6629331972a3297c992970d6a7192` | 0 |
| crates/bitwarden-api-api/src/models/two_factor_duo_update_response_model.rs | 1107 | `6829dd79a264355730a11f028a3f9112a6e51daca5af76d5bae19919680b50e0` | 0 |
| crates/bitwarden-api-api/src/models/two_factor_email_delete_request_model.rs | 1157 | `240a394598c3924fe56cb68384b3484fcab7c69ac7c78bbd920239d3dcd63b39` | 0 |
| crates/bitwarden-api-api/src/models/two_factor_email_details.rs | 1199 | `1107627bf8d57092a1545610007e30da5c7702f410e5bef48e4cfad6dfe2326d` | 0 |
| crates/bitwarden-api-api/src/models/two_factor_email_login_request_model.rs | 2394 | `1c80f2834257b0083c10a41576e9a60026d5ead36958dbf4b55dee4dbe471e1c` | 0 |
| crates/bitwarden-api-api/src/models/two_factor_email_response_model.rs | 1650 | `3cc21f76bcccb39bc398bf796a1e0e449c86c7ee2b2b4a0e88bd0d62589c0e2f` | 0 |
| crates/bitwarden-api-api/src/models/two_factor_email_setup_request_model.rs | 1535 | `4cce85d68803ab3604b3dc9391ebb442f35dd2e50b122eaca8f338ff6fe64743` | 0 |
| crates/bitwarden-api-api/src/models/two_factor_email_update_request_model.rs | 1658 | `9578f061f781c3db2e02c0bc37650d3813a31420e33391a60099488f9e3a6954` | 0 |
| crates/bitwarden-api-api/src/models/two_factor_email_update_response_model.rs | 1133 | `8407ed26a69862293c7ced3c1a0210f4f3748a8c9fd9d044c5fc5e3670a9275a` | 0 |
| crates/bitwarden-api-api/src/models/two_factor_organization_duo_delete_request_model.rs | 1221 | `61f844608b36878cc116878a61660f85adfd8ec19dec12cacaf452d81551fb66` | 0 |
| crates/bitwarden-api-api/src/models/two_factor_organization_duo_response_model.rs | 1696 | `60a868f16f080d3d8107acc6d6ecc3a1466d7811a0844b9278cdff1f6b5bc164` | 0 |
| crates/bitwarden-api-api/src/models/two_factor_organization_duo_update_response_model.rs | 1183 | `9f6d2f446195d1adbac267ff66836d032307dfd9946c1828b8997e639a7017ef` | 0 |
| crates/bitwarden-api-api/src/models/two_factor_provider_response_model.rs | 1131 | `afb12c107fa50d313977677acc356675a57edee508657345df364baab1e4ab52` | 0 |
| crates/bitwarden-api-api/src/models/two_factor_provider_response_model_list_response_model.rs | 1383 | `fae1b152ae4e0505482edef658b8904dd2f2639f8c51a56dec9ed8c4f4f67917` | 0 |
| crates/bitwarden-api-api/src/models/two_factor_provider_type.rs | 2886 | `2ffb2f119524aebc1a62666664d46575de357e69dbc601652a138b7fcb5dff82` | 0 |
| crates/bitwarden-api-api/src/models/two_factor_recover_response_model.rs | 917 | `0312503da5c41cddaa3a46e00eda2d347ba265545e1e44eb0b250c22459aeb6e` | 0 |
| crates/bitwarden-api-api/src/models/two_factor_web_authn_delete_all_request_model.rs | 1203 | `744c0dea316a792306a9a00a2430aa54e6eaea8221813150c151a4336ca86681` | 0 |
| crates/bitwarden-api-api/src/models/two_factor_web_authn_delete_request_model.rs | 1066 | `4b7059e3003fa1ee0d21b8f9ad98f517061d58f04cecdfbbedb2bfab67e767b6` | 0 |
| crates/bitwarden-api-api/src/models/two_factor_web_authn_delete_response_model.rs | 1619 | `fc65e0048c86c6da9ebb5fc80af73569ad9d411a53d3ac731474ebccc11bcb21` | 0 |
| crates/bitwarden-api-api/src/models/two_factor_web_authn_details.rs | 1237 | `6d779af9856de96fa953e8997ac768b24676459acc9dde48e687ec997f18d185` | 0 |
| crates/bitwarden-api-api/src/models/two_factor_web_authn_response_model.rs | 1688 | `4a2f5e37ffd36767fcb574fe2fbfa0b60dc735496baf0f42a23f2cef22dd2e93` | 0 |
| crates/bitwarden-api-api/src/models/two_factor_web_authn_update_request_model.rs | 1527 | `6c21e7646f0ed36ed2630512ad80f446d6c272e9a295aeefd05ef8dc1240ca15` | 0 |
| crates/bitwarden-api-api/src/models/two_factor_web_authn_update_response_model.rs | 1175 | `cf3e801fbed5adb3641c54e8243337738c538f8961c2cc5923620062590eadf3` | 0 |
| crates/bitwarden-api-api/src/models/two_factor_yubi_key_delete_request_model.rs | 1171 | `8ef698184ebe3e2e96d66b05f55bd9327b12b84965e06fdae9a4a9f5c704e529` | 0 |
| crates/bitwarden-api-api/src/models/two_factor_yubi_key_details.rs | 2032 | `eba3dfa7c50996f627259d9108bb903b8f9f75fb629c171fba9e69f114b8a8ce` | 0 |
| crates/bitwarden-api-api/src/models/two_factor_yubi_key_response_model.rs | 1676 | `3829b4745ce179f7444e2160fa25552252386093b7b2b5bd4604a40fae2a4f8f` | 0 |
| crates/bitwarden-api-api/src/models/two_factor_yubi_key_update_request_model.rs | 1924 | `cb8cb9c665489c8741fe0a32a92f96d8259fcb3202cfba8cd14c83d3d62d6372` | 0 |
| crates/bitwarden-api-api/src/models/two_factor_yubi_key_update_response_model.rs | 1163 | `09fc85af6794054b3e86742fb784b3ec23b2d92d146680efd618b8f1cf6e9d6d` | 0 |
| crates/bitwarden-api-api/src/models/unauthenticated_secret_verification_request_model.rs | 1526 | `5be59568a1d9a3a7a93ac71a1820a385734f0e5ff1b496f7882ebbc12b79fb22` | 0 |
| crates/bitwarden-api-api/src/models/unlock_data_request_model.rs | 2530 | `66ce4c6121e14da5ad07d5fa7bcd0d16e0e025cc74350388b1ffa310f5aa7dd9` | 0 |
| crates/bitwarden-api-api/src/models/unlock_method.rs | 2288 | `68d96f911d73be9e937e1fb9a12318fc403ec55cda32c763fb93bb6a5fb58596` | 0 |
| crates/bitwarden-api-api/src/models/unlock_method_request_model.rs | 1297 | `693cecf219a1e15065cabe38088970028eeaf3f49bf85a233b50b87947f97524` | 0 |
| crates/bitwarden-api-api/src/models/untrust_devices_request_model.rs | 665 | `8861563bb71d37068c088a2159536cd3d868bb972b44ca8a1809b30b84919eee` | 0 |
| crates/bitwarden-api-api/src/models/update_avatar_request_model.rs | 727 | `3fbb1111e0e78006aeb6fe73de29c5fdb0b7b0eb7f9beb541579d7f190f6b488` | 0 |
| crates/bitwarden-api-api/src/models/update_client_organization_request_body.rs | 831 | `7238fb8845e0f1c664b1da0e406b4b3bec62b899f7341cb6e701b9d0028934f1` | 0 |
| crates/bitwarden-api-api/src/models/update_collection_request_model.rs | 1357 | `2dee219b1ff787550133cd230805eee1edb01bfab0c118aa7c453c5591881c5b` | 0 |
| crates/bitwarden-api-api/src/models/update_devices_trust_request_model.rs | 1860 | `f0f314af865bd3eb8f97f866dc7080d939240524cc29433c0836377690f38884` | 0 |
| crates/bitwarden-api-api/src/models/update_domains_request_model.rs | 1105 | `16c115198773020bbbf7bf8667278e3aa86c0c4c4ec101454963b4f1bd88e620` | 0 |
| crates/bitwarden-api-api/src/models/update_invite_support_confirm_request_model.rs | 1104 | `9211a0e127624d05a4575075fe8e69fcd0e336ecaec8c0d354d279dfae991c7c` | 0 |
| crates/bitwarden-api-api/src/models/update_organization_invite_link_request_model.rs | 834 | `950334f37f2f13b6b86cb11cee0ca2c119e9df755c95f742b9cbfb13438a0dc9` | 0 |
| crates/bitwarden-api-api/src/models/update_organization_report_application_data_request_model.rs | 872 | `787874c94ed360fa258c8643ab3585aea3e5fa14888a7302c580cc72b110905c` | 0 |
| crates/bitwarden-api-api/src/models/update_organization_report_summary_request_model.rs | 1039 | `9a58946e06f82cb03ea11e49952f52698424f07a7f4da110f35d2f5b78c6c155` | 0 |
| crates/bitwarden-api-api/src/models/update_organization_report_v2_request_model.rs | 1403 | `b602da123a5fd5a62615782f0b4af0600700fa7e8ed630a58495be1444287023` | 0 |
| crates/bitwarden-api-api/src/models/update_profile_request_model.rs | 953 | `c1c3bf1eb1b6af0831b34c27c6a64869f58189c5de370a2a873fb2f7e470cfdc` | 0 |
| crates/bitwarden-api-api/src/models/update_rotation_config_request_model.rs | 1925 | `910f4c511b8693999d63f6a79830bed53dee5b06ff66b72d7498837672000107` | 0 |
| crates/bitwarden-api-api/src/models/update_target_system_request_model.rs | 1356 | `f68afe5a3caf3794e5b5fd34ed4791aea3203bc8f9bd15a1c5dd45e45727412a` | 0 |
| crates/bitwarden-api-api/src/models/update_tde_offboarding_password_request_model.rs | 1744 | `018a7af4aced1de3cc1b9475c30545936686d57e0174e9c9c4cef45c328c781b` | 0 |
| crates/bitwarden-api-api/src/models/update_temp_password_request_model.rs | 1704 | `386a8e5f166b804acc15779bebe399944428e05dbcc36b35b0b054676b29e81a` | 0 |
| crates/bitwarden-api-api/src/models/upgrade_premium_to_organization_request.rs | 1899 | `b0dfa5168e663cf7dbfedb60ad17eef8d0e294b1b14b24d75ed853bd7ddff78a` | 0 |
| crates/bitwarden-api-api/src/models/uri_match_type.rs | 2513 | `7954488a901ffd15d9ed2d0de2f8c6cc0d3897b9d8df6812295c2bbb06755a61` | 0 |
| crates/bitwarden-api-api/src/models/user_access_policy_response_model.rs | 1761 | `4311d470ee445739f29196ebfad35e7422709ac6ec801f3e339cdc970bb0f2cb` | 0 |
| crates/bitwarden-api-api/src/models/user_decryption_response_model.rs | 1604 | `d3ab53f25df34ca1fa2b10ce4d8d4af3746b2efce92b42839fb555372e312942` | 0 |
| crates/bitwarden-api-api/src/models/user_key_response_model.rs | 1088 | `3a737d35fc7277e952eef696d7e7de7150dde718a649693da18eb101a121dae6` | 0 |
| crates/bitwarden-api-api/src/models/user_license.rs | 3209 | `a9790e2d66cece9a00768365b6177c93d6102214ca412592ce3886600a7fd39e` | 0 |
| crates/bitwarden-api-api/src/models/user_verification_requirement.rs | 1246 | `29e31e066d72683ef0a81a83eff8809302ceb7b97a91ca063b331dcaeba192aa` | 0 |
| crates/bitwarden-api-api/src/models/v2_upgrade_token_request_model.rs | 1296 | `e82573305982e1c75f489991fce5c212ef2c7608ab26968e6652484b6f93886f` | 0 |
| crates/bitwarden-api-api/src/models/v2_upgrade_token_response_model.rs | 934 | `ceea02537cc353bbf9818b633be0606a6244c0ff7ac871b92a4d083dcad7f4d8` | 0 |
| crates/bitwarden-api-api/src/models/verified_organization_domain_sso_detail_response_model.rs | 1485 | `e1094a7dba855abf9baa37f46c59a779ce3f26fde81ff2ea22895c5b1efc7fe0` | 0 |
| crates/bitwarden-api-api/src/models/verified_organization_domain_sso_details_response_model.rs | 1277 | `8a4223372b1d577ae08c66e92a3efba889f421d18ce1afd483cfb3fcc4686d6c` | 0 |
| crates/bitwarden-api-api/src/models/verify_delete_recover_request_model.rs | 758 | `21a58b3d0cd1357f158874955d9435588ed7d5c59d253a29ba1ad939b4559e3e` | 0 |
| crates/bitwarden-api-api/src/models/verify_email_request_model.rs | 726 | `9b9cebb1829b2318fde1284101a01a1c4202364650edff39757afc231b9fb584` | 0 |
| crates/bitwarden-api-api/src/models/verify_otp_request_model.rs | 607 | `db6c1314040b1385a7b396e1ea6ec0e43e8f969cb16708a3a8809d9acfe66b69` | 0 |
| crates/bitwarden-api-api/src/models/web_authn_credential_create_options_response_model.rs | 1121 | `cafa003df4c08bdf1bd598632d24dd3977f4b225c8a94ad4b4a3ca6312ca1354` | 0 |
| crates/bitwarden-api-api/src/models/web_authn_credential_response_model.rs | 1724 | `07e4f57c4914ed203c43afba3280cb4cffbbf183e249c7d0b505abb91d6c3b0d` | 0 |
| crates/bitwarden-api-api/src/models/web_authn_credential_response_model_list_response_model.rs | 1389 | `09c3dd399cfce7a392a6a69ac8a63fe84eb495de662c96dccf9f83e71e8ccc02` | 0 |
| crates/bitwarden-api-api/src/models/web_authn_login_assertion_options_response_model.rs | 1099 | `49b8aa757f40ca044d61abaaf3d5e54d7fbd6c136a71b86442791a3a1faa509d` | 0 |
| crates/bitwarden-api-api/src/models/web_authn_login_credential_create_request_model.rs | 1939 | `c0d9fffeaf409aed40518a7b4058d311bb03da340c6c8b51700623ccfdf87b70` | 0 |
| crates/bitwarden-api-api/src/models/web_authn_login_credential_update_request_model.rs | 1543 | `97f215bacc2b0c534bd07e33fde0ed0e6fda3609e6ff75b8e95f206616799475` | 0 |
| crates/bitwarden-api-api/src/models/web_authn_login_rotate_key_request_model.rs | 1056 | `63632adc11af481a719b7e280b0e3d0072feef1802ca3b40b0895c2b4990e481` | 0 |
| crates/bitwarden-api-api/src/models/web_authn_prf_decryption_option.rs | 1422 | `113beeb51f14f42966911ce1d22fbcce21f845b6968fbeea57bae3a91551c581` | 0 |
| crates/bitwarden-api-api/src/models/web_authn_prf_status.rs | 2351 | `a1c9dc149075ecdaf4a0a1eb19ff7e9d4c665e7e97edf08acc6cef8e8b824220` | 0 |
| crates/bitwarden-api-api/src/models/web_push_auth_request_model.rs | 871 | `cc9f14e5fb1f3f2521a0135fadf46abcfac6753390a6c362994c0903eb121b04` | 0 |
| crates/bitwarden-api-api/src/models/wrapped_account_cryptographic_state_request_model.rs | 1507 | `b784d78103d97aa85e457b8f02711cc739bb08749ead5381ec5845e1f279d5c9` | 0 |
| crates/bitwarden-api-base/Cargo.toml | 1156 | `6a0f54a03c44ee6844ba4a0c377b31a0b91ef9be85c59a5c6bdae1b88294dbf4` | 0 |
| crates/bitwarden-api-base/src/client.rs | 1507 | `f2e95da5e93d33bbef3c205f77ee8e9a00500d9fc73643eda176f7f31da6aa75` | 0 |
| crates/bitwarden-api-base/src/configuration.rs | 861 | `adf6367231a32237a51e42a8ab23178b776468305490c1795f42768f67c1a417` | 0 |
| crates/bitwarden-api-base/src/error.rs | 2644 | `e8935ffccc518e569cfb27179b15c65cf66a6288df26a060e22fca600efd2964` | 0 |
| crates/bitwarden-api-base/src/lib.rs | 538 | `1aa799400b63fd132e4555d182052f0769edba35af148de661cb6b91f7606a4b` | 0 |
| crates/bitwarden-api-base/src/request.rs | 2304 | `580c44d86e2663d744429468b3b8215afa8d38c78a9d26a8c98daad7e2cb6a70` | 0 |
| crates/bitwarden-api-base/src/status_code_serializer.rs | 1337 | `8f9bb4085e96ee4cfb6d410c2b74d33201ab0c26fb405524071eb5dc1abd6426` | 0 |
| crates/bitwarden-api-base/src/uniffi_support.rs | 293 | `fe596eb3a171bccb8edf6f6d5d07ddcc982267a898437042911f4e330cc28c77` | 0 |
| crates/bitwarden-api-base/src/util.rs | 2568 | `4dbff49aba26bd3c1e71fde0f94bc13541250538711432a35505da4c64fa4024` | 0 |
| crates/bitwarden-api-identity/Cargo.toml | 853 | `e57933f8a3f8ecd8320f7233e7f3a56b73ad696217d7fe07ef10bd5998fe65b6` | 0 |
| crates/bitwarden-api-identity/src/apis/accounts_api.rs | 7490 | `479acfc29d99f108be1aa272ac2dd4cdff58df5a62f08c817b2af84480dd2e3a` | 0 |
| crates/bitwarden-api-identity/src/apis/info_api.rs | 1647 | `8875a63cb10e612914f03df3c88665fc3c5fb59f9fc110ea469130fdd84ecb5f` | 0 |
| crates/bitwarden-api-identity/src/apis/mod.rs | 2358 | `c4f8e397e4db378769487b4587de0648c75617eb6113360de4cc55c5b07d476a` | 0 |
| crates/bitwarden-api-identity/src/apis/sso_api.rs | 5095 | `00a71108aaf0748f02e126e40fb32d7dcd47bd5996f7e20b2b837b21a861585a` | 0 |
| crates/bitwarden-api-identity/src/lib.rs | 403 | `5ba8a4fbb91deec0ab29a266a43817d2552c61d1c926791c60008d24846f396b` | 0 |
| crates/bitwarden-api-identity/src/models/account_keys_request_model.rs | 1840 | `7bcdcc8242c505d968cf73fa38b2961a479bbb871035c649986023f22409151c` | 0 |
| crates/bitwarden-api-identity/src/models/assertion_options.rs | 2173 | `5f1093e482b042bd2a07474c90bf03bb95aef85ba07c460a008d56ca4327e408` | 0 |
| crates/bitwarden-api-identity/src/models/authentication_extensions_client_inputs.rs | 2319 | `1b880ca24fd4a9c42f1b405e74f7278d1965ee7c1ec8bc659267052830d3bfaa` | 0 |
| crates/bitwarden-api-identity/src/models/authentication_extensions_large_blob_inputs.rs | 1316 | `858945ac3bb3949bc85f198e7487c7aaea77cb96e75b565a01d85939dc1fbab3` | 0 |
| crates/bitwarden-api-identity/src/models/authentication_extensions_prf_inputs.rs | 1075 | `07d558a2f93794f460fc0a6545e45ae5e204fa78b539e6bb8802cb750062717c` | 0 |
| crates/bitwarden-api-identity/src/models/authentication_extensions_prf_values.rs | 1180 | `9bb8ec36238a64c1dd332a748774dae9c7a7cea016a200962c8773c79bc1b900` | 0 |
| crates/bitwarden-api-identity/src/models/authenticator_transport.rs | 1438 | `2c16ddedb7fcd6c58a7e337292111065c6c13ecce67a89718af3ef494a9228e5` | 0 |
| crates/bitwarden-api-identity/src/models/credential_protection_policy.rs | 1537 | `abe3f0c577dd9150ad473c62a7efd9d692b71de69a8e030429de01f538669fbc` | 0 |
| crates/bitwarden-api-identity/src/models/kdf_request_model.rs | 1133 | `529788c9cc302ed8b538090e410f7ba804461c57736aea799e13ea92716984b4` | 0 |
| crates/bitwarden-api-identity/src/models/kdf_settings.rs | 1117 | `b8c3f8a29de9930b80d694119ba2e9a88bafa423b1b37e2e1355178bf132f9b8` | 0 |
| crates/bitwarden-api-identity/src/models/kdf_type.rs | 2145 | `27e4befb7bef83adaba76efd2bdc40953a7025a144ada8c76671aeb1a9e7e76a` | 0 |
| crates/bitwarden-api-identity/src/models/keys_request_model.rs | 1240 | `b616fc9a971d7a93998932bab80fa0e89fce6671d03f47d134b034c0cc24d653` | 0 |
| crates/bitwarden-api-identity/src/models/large_blob_support.rs | 1081 | `216ab03f063ba2ef68ec83b513ecee5dc5a7e49bf7266a698114e29128493e25` | 0 |
| crates/bitwarden-api-identity/src/models/master_password_authentication_data_request_model.rs | 1168 | `c76cf38c99b45807aa1cdd4c792caa903b8597d69d4ece0bdeed20b68aba7cc0` | 0 |
| crates/bitwarden-api-identity/src/models/master_password_unlock_data_request_model.rs | 1287 | `1abe9f8ee510861a064229768f50d23adad63984f83522f961ca09b4b5669553` | 0 |
| crates/bitwarden-api-identity/src/models/mod.rs | 4130 | `2c3cc676a58bbb5159c874545cc5c92ca33b2f2e77becbefe5b6130b87f47adf` | 0 |
| crates/bitwarden-api-identity/src/models/open_org_invite_request_model.rs | 810 | `57e096601ce0d2be79c4ec402af3018869a8c027c12cdc041eb4bd5548f87e3a` | 0 |
| crates/bitwarden-api-identity/src/models/password_prelogin_request_model.rs | 637 | `5c14e14b271be62a33be3b89f5baf9da0f890de09045afbefc9a6a4bbdf342d2` | 0 |
| crates/bitwarden-api-identity/src/models/password_prelogin_response_model.rs | 1701 | `a541a247017cb52bd10fd8bf219263c8ef48f7b94378edfddd86443f223faa7b` | 0 |
| crates/bitwarden-api-identity/src/models/product_tier_type.rs | 2462 | `39528d94e4fbaa91bd39550406d4d308a9ac0d709e94c7cdefae6220091d05e2` | 0 |
| crates/bitwarden-api-identity/src/models/product_type.rs | 2333 | `dd27bc28eaacd7f4e21027aa1a2d4557f0d6987624dfbf534a16023aa88629e5` | 0 |
| crates/bitwarden-api-identity/src/models/public_key_credential_descriptor.rs | 1290 | `3528c7a69fc29831446db26addde2418944e9872d0de991f4be78736e03ab22f` | 0 |
| crates/bitwarden-api-identity/src/models/public_key_credential_hint.rs | 1233 | `28c18de6eaac217314f8562f576652e58efba3f1da1f93425d6f4304f369ad8a` | 0 |
| crates/bitwarden-api-identity/src/models/public_key_credential_type.rs | 1108 | `4abbeed3dd58750eec0d004ccbf50c7756fb9a37848108c0f076b0a5e965127c` | 0 |
| crates/bitwarden-api-identity/src/models/public_key_encryption_key_pair_request_model.rs | 1166 | `06d415fef97b5dd380c53acd669da236de9584973318a7424cd25eb8ba10a71c` | 0 |
| crates/bitwarden-api-identity/src/models/register_finish_request_model.rs | 5662 | `ae9ab8dc6ce860a6af239b97efb99953e616a25e859ab330d0b4c9124fcc5c2d` | 0 |
| crates/bitwarden-api-identity/src/models/register_finish_response_model.rs | 709 | `21c2400ef9ab345c6924f1a3383c9b537d998c9bee07879dcaa143723b23abd5` | 0 |
| crates/bitwarden-api-identity/src/models/register_send_verification_email_request_model.rs | 1607 | `a2467c93e8d2c9aa2ee47f82ca0217abc8d37da406f9289af03322565eb44f4d` | 0 |
| crates/bitwarden-api-identity/src/models/register_start_open_org_invite_request_model.rs | 1100 | `605e8ab06685d39ee1341778c16690e37a6de17d4ced498393dfc88057a321c6` | 0 |
| crates/bitwarden-api-identity/src/models/register_verification_email_clicked_request_model.rs | 973 | `a6158b6ff4dd6b3ff6cfa2d84904c3c6a8aa00ff76ad13c50b39a683b49fcdd8` | 0 |
| crates/bitwarden-api-identity/src/models/security_state_model.rs | 829 | `8c9ab3a444aea88e5e4a48faab82bf6db99e5ed99e037b61af44210aa9b14046` | 0 |
| crates/bitwarden-api-identity/src/models/signature_key_pair_request_model.rs | 1119 | `572812d73963429ff1aa50a8e0d2057aef937f4dad29df216eed964ec1d25d2d` | 0 |
| crates/bitwarden-api-identity/src/models/string_authentication_extensions_prf_values_key_value_pair.rs | 999 | `ada27074550fbd09ebf0a24a202957a63bd68252d8ae1f46a357411387514658` | 0 |
| crates/bitwarden-api-identity/src/models/trial_send_verification_email_request_model.rs | 2579 | `2211d7c752ebacd1952729dca91e1300364e0b258d3103fb0983b65c450d3e74` | 0 |
| crates/bitwarden-api-identity/src/models/user_verification_requirement.rs | 1238 | `dea004053071499c02cc5011a5f23f5c619a44d2cf0844c37bccfcb9f59f10e6` | 0 |
| crates/bitwarden-api-identity/src/models/web_authn_login_assertion_options_response_model.rs | 1091 | `72f0664dba8d4a3d41fafab7c6196393e13cc96bd3d822ac2e599c3a44d7c717` | 0 |
| crates/bitwarden-api-key-connector/Cargo.toml | 723 | `ec984980c8aecb62fb824d31345a5c93656fb3f86ab1af8b7bdd6b9efa1565d2` | 0 |
| crates/bitwarden-api-key-connector/src/apis/mod.rs | 1849 | `65aa99d572a9a0d05e2a2760ffe37e22ff337422082c6d762787a614e5a4ec6b` | 0 |
| crates/bitwarden-api-key-connector/src/apis/user_keys_api.rs | 5311 | `2835c524e64d8579529901155f7d78428a86bcf8f55d30e8db27260e978682bb` | 0 |
| crates/bitwarden-api-key-connector/src/lib.rs | 86 | `360388c5261f64fbe76b6d1951d3c705d53af23c23636e6a9ed17d8b3555797c` | 0 |
| crates/bitwarden-api-key-connector/src/models/mod.rs | 65 | `111abd0fd07d5f90175441aec75f8b1a6dfbab9435f410f0134ea455218a00ad` | 0 |
| crates/bitwarden-api-key-connector/src/models/user_key_request_model.rs | 209 | `f6b93566894fca8eccc2c99c9ca299f23325f751fada641300ea5957454740e8` | 0 |
| crates/bitwarden-api-key-connector/src/models/user_key_response_model.rs | 207 | `93bda19f4a8f71f36acb4c0499856b248bc52b6425056b3f6b22df83c56af0d9` | 0 |
| crates/bitwarden-auth/Cargo.toml | 2242 | `df6da4d60ec3aba25fd556f5c1275de33a1b9601da6332f9a65f574d1e9ec6c6` | 0 |
| crates/bitwarden-auth/src/api/enums/grant_type.rs | 714 | `252357c76db45c7f8890d9c65d201e3697bd44e3d0553926523e01e99c7c860a` | 0 |
| crates/bitwarden-auth/src/api/enums/mod.rs | 229 | `67d74ca3318a46be51860c28c43d865afef194ae15aba61581a319ffa7a82a97` | 0 |
| crates/bitwarden-auth/src/api/enums/scope.rs | 1403 | `d3a680b932c43c074d71952685fd22f31e8320b6b004f9c587b1bce1db68b244` | 0 |
| crates/bitwarden-auth/src/api/enums/two_factor_provider.rs | 522 | `cbe15b0b2c54b6c1cc7ecb6d2d288a5a0dce661059fd1c0ea5120ae2916c417e` | 0 |
| crates/bitwarden-auth/src/api/mod.rs | 176 | `130f7124857ff67e228fd51ce391da5284ad98bb264e49e8c75b0e11b9bc4f7a` | 0 |
| crates/bitwarden-auth/src/api/request/mod.rs | 235 | `32a55b6731749752876efeddc08b44a684cb997f703879be982982cb5852d41f` | 0 |
| crates/bitwarden-auth/src/api/response/mod.rs | 235 | `0f21b5faaae6e7cfb70374215dcc288e09fa8be92b6d99918b0e8bc1419a3e75` | 0 |
| crates/bitwarden-auth/src/auth_client.rs | 2201 | `a9d6e90ab80260a0ef6a780ede69664069f76dbd98a102bd37a5c6ddb027b153` | 0 |
| crates/bitwarden-auth/src/lib.rs | 365 | `c994af12d5e12e58062e6d43ce11c86208bd47cbf40326c66215adae41d6090b` | 0 |
| crates/bitwarden-auth/src/login/api/mod.rs | 432 | `d7d07300db5bd203f27d29d4e3331e0b3255da92f672909d37ee5099dac26478` | 0 |
| crates/bitwarden-auth/src/login/api/request/login_api_request.rs | 12723 | `eb439372b0d2de51abe6fdaf514f9913d39946370d124b30646a739f5203f24e` | 7 |
| crates/bitwarden-auth/src/login/api/request/mod.rs | 479 | `8aa4853d687064b16a95e78e23c9b4b63d58ba304d1d515dcfdd8193ba8a58f7` | 0 |
| crates/bitwarden-auth/src/login/api/response/key_connector_user_decryption_option_api_response.rs | 488 | `e8aa5b355950976a8cdccf317ab6457aa63a86c7a2acea3b64faed76b4b43cff` | 0 |
| crates/bitwarden-auth/src/login/api/response/login_error_api_response.rs | 18077 | `06f061117fa4d8dfe0e718a1005129344a0894136de08d0bb3040ab10667a873` | 0 |
| crates/bitwarden-auth/src/login/api/response/login_success_api_response.rs | 4343 | `438a45d40c1948a50f72287bac75ebc30ca0efb5b2d3257fea0c03a83caaa203` | 0 |
| crates/bitwarden-auth/src/login/api/response/mod.rs | 1169 | `94862e1c10a70649dc6d0a0f78d8b39075c9143c23b8416bb04e27caa8c7ec9a` | 0 |
| crates/bitwarden-auth/src/login/api/response/trusted_device_user_decryption_option_api_response.rs | 1437 | `931e205e1ac8369ed9e8dd5af669e1425388c1f36c78b744b746cbad90c79d76` | 0 |
| crates/bitwarden-auth/src/login/api/response/user_decryption_options_api_response.rs | 1590 | `bd83f286815ba17a718886cff6c125dac2cf6277ab689585a24c2fab55df269b` | 0 |
| crates/bitwarden-auth/src/login/api/response/webauthn_prf_user_decryption_option_api_response.rs | 1086 | `50092dcdb2cd756ca83f013c5653905236e82022b87312583e8cdbec93365378` | 0 |
| crates/bitwarden-auth/src/login/api/send_login_request.rs | 17861 | `d42d766bcbfbb810643b94bfb433ed61429f4411ebd7ec4e241cece68c89788d` | 1 |
| crates/bitwarden-auth/src/login/login_client.rs | 2812 | `1b167c989093bbcda697ab4af3b57b559dcd84cc318f8fc371246db06114c827` | 0 |
| crates/bitwarden-auth/src/login/login_via_password/login_via_password_impl.rs | 27698 | `abe69eb48b1653b196e2a645e6956fe1adf4faf0ef1572b3bcd3d67020c458b5` | 0 |
| crates/bitwarden-auth/src/login/login_via_password/mod.rs | 3432 | `ce7c17c51b6f7b95eadf5bb02846bbe84e4c663885b2fe50dac6f94406e46695` | 1 |
| crates/bitwarden-auth/src/login/login_via_password/password_login_api_request.rs | 10208 | `cfc1bef4adfdff76541c1106de65e994db19cf67837dcbbad8a1959eb2d8024a` | 0 |
| crates/bitwarden-auth/src/login/login_via_password/password_login_error.rs | 15444 | `e6c6204463f93336a555622f3a7682fc323b8a9ff8b1036569aa9ba3df8b921d` | 0 |
| crates/bitwarden-auth/src/login/login_via_password/password_login_request.rs | 796 | `4278b5a31ee93c36ca7b5cbc7dd324cca062fef553b81ea605f8a60b6d5c3b36` | 0 |
| crates/bitwarden-auth/src/login/login_via_password/password_prelogin.rs | 10502 | `8f81b89ea75c972972c1c09aea62508ca3568ed40875473ce4103910d7bf2766` | 0 |
| crates/bitwarden-auth/src/login/login_via_password/password_prelogin_response.rs | 6186 | `b426e471cf887dfcee868c6ecfb09ba4c6e4bd2785f07ce99aef5c6dd956ead5` | 0 |
| crates/bitwarden-auth/src/login/mod.rs | 417 | `cf0d229b6f9facb92f775a958fbf9a8117b89b76c3e1b8110ee2fc5819435359` | 0 |
| crates/bitwarden-auth/src/login/models/key_connector_user_decryption_option.rs | 1167 | `15ff05444f25d080eb520c621eb062a83fbdfedcfb6028033097e8d4385d28c2` | 0 |
| crates/bitwarden-auth/src/login/models/login_device_request.rs | 1360 | `ccd3fa1424d9073973c02aa02cac6ae5c02799f76301acf70c223ab63020decd` | 0 |
| crates/bitwarden-auth/src/login/models/login_request.rs | 746 | `151b70a73c9e74e7bd0b6e66b477a6b3bcfd503b2e082616efa67ba6c2b949cb` | 0 |
| crates/bitwarden-auth/src/login/models/login_response.rs | 615 | `c6fe90209bf726e387223c47677a8524324152e75ed2468e22fb31669f560957` | 0 |
| crates/bitwarden-auth/src/login/models/login_success_response.rs | 5110 | `fc569b64714dcd1dbfc54fbce45973e3cc00088db8c6bdff4ae60e0ce3a6c4ae` | 0 |
| crates/bitwarden-auth/src/login/models/mod.rs | 808 | `6265966f0efb23550fdc1ed728ee2a603e8b72ac523d93d0003c24c7e42d12c7` | 0 |
| crates/bitwarden-auth/src/login/models/trusted_device_user_decryption_option.rs | 3435 | `95d87cef31ed923c39517b475e2cb82b78df9a9ca35167bed682dd53f3f61fd0` | 0 |
| crates/bitwarden-auth/src/login/models/user_decryption_options_response.rs | 20101 | `f616de21e7706d5766a2a288d7d5b0922550ce8bf6440a2afda51d0a0f6afe66` | 0 |
| crates/bitwarden-auth/src/login/models/webauthn_prf_user_decryption_option.rs | 3666 | `c5123241846644a392dc1f617861a7c2861acfdc65d639cd282ec20a395c0402` | 2 |
| crates/bitwarden-auth/src/registration/mod.rs | 1158 | `0071ee5e0c4cb08288760fba1114581eaac78b955f68ffd97cee5d76c9f6eae3` | 0 |
| crates/bitwarden-auth/src/registration/open_org_invite_crypto/client.rs | 3598 | `68fe93690bdc662bd005c7617794a40008592daf56e95b206f5d473f9fd260f4` | 1 |
| crates/bitwarden-auth/src/registration/open_org_invite_crypto/data_v1.rs | 978 | `aeaf23fd5708141dee343e818b319f873c270ed40843f0e2bd099f61e4edb1b4` | 0 |
| crates/bitwarden-auth/src/registration/open_org_invite_crypto/mod.rs | 649 | `b1e2420df15409edb1ebad213074c076763a9caa3066149cad6fda8ca18d796b` | 0 |
| crates/bitwarden-auth/src/registration/open_org_invite_crypto/open_org_invite.rs | 7865 | `4f0f19d436e2875ba0a1e8b668181d13294c14b8a04f3ecec461686364812753` | 1 |
| crates/bitwarden-auth/src/registration/open_org_invite_crypto/serialization.rs | 7284 | `df163328c1ecab666d2297b856d49ff6be863c5b70e6fd62c39a566d572a0e8c` | 1 |
| crates/bitwarden-auth/src/registration/post_keys_for_jit_password_registration.rs | 19884 | `9424866aeddd9f3c52c327f0a715c037e3946824dacaf1032e1b201e5e666e24` | 4 |
| crates/bitwarden-auth/src/registration/post_keys_for_key_connector_registration.rs | 11609 | `a5daf7dc31cbca73b9e7b6b384d706b1137af726eedad1d6cf702ca5c4add031` | 0 |
| crates/bitwarden-auth/src/registration/post_keys_for_tde_registration.rs | 18849 | `55b60c5a208d995b80b0cdaed3197bf8152724a7a8a1337abc9f4980321ba6a0` | 0 |
| crates/bitwarden-auth/src/registration/post_keys_for_user_password_registration.rs | 21257 | `820e387aa8ecc65bea1fc0cafc80ad85081e332b8ba896c545a905a3a6e6dc52` | 3 |
| crates/bitwarden-auth/src/registration/registration_client.rs | 1411 | `e52bd3d063501bf83cef4f3854dc6bc78ee97cce2b56e79f6e41b683cbd59ad9` | 0 |
| crates/bitwarden-auth/src/send_access/access_token_request.rs | 14602 | `58d49d9cd0512c799f7e99e828334393d2e667945ec3b2bde111df835b95ff9a` | 0 |
| crates/bitwarden-auth/src/send_access/access_token_response.rs | 3371 | `d3bf10759da26a17591225d36aa9a6010d6ad528b2c078627d3b02e760e59dd4` | 0 |
| crates/bitwarden-auth/src/send_access/api/mod.rs | 504 | `52f26bee95db98c81a21e5dd7b31d5503c2de2cc510c1d2a985ca9452ff005b2` | 0 |
| crates/bitwarden-auth/src/send_access/api/token_api_error_response.rs | 36970 | `b9861207def88c2c490b3ef60a8f47675a45f26288c18f60728a13945f4250b7` | 0 |
| crates/bitwarden-auth/src/send_access/api/token_api_success_response.rs | 766 | `6404cb8de9ae1677fc5cad7fd69f939e8a9c21e4d8e7ec6f00c8d14a7f079a6b` | 0 |
| crates/bitwarden-auth/src/send_access/api/token_request_payload.rs | 8145 | `162aebeb1bf80c82eeea33e993a217051da68329c81de58aac1507ab52b39b18` | 0 |
| crates/bitwarden-auth/src/send_access/client.rs | 37759 | `72e39694484431b6076a589a826c09f73c433bb063b46525fad4c34654a5dc17` | 0 |
| crates/bitwarden-auth/src/send_access/mod.rs | 1189 | `3ceb06c87addb83af201eeca29ac079c1acd72078320f09073ef316d1a1e139c` | 0 |
| crates/bitwarden-auth/src/token_management/middleware.rs | 11281 | `4a806682ff839b7c3350075ca5c9c5acffa9534035a0d83213d17248bc3f41be` | 0 |
| crates/bitwarden-auth/src/token_management/mod.rs | 347 | `97c4b7d655cb9dfeaa9ba7c8d71a9a01fcc2ecd2c25d96a5243ddcd6e4861f71` | 0 |
| crates/bitwarden-auth/src/token_management/password_manager_token_handler.rs | 11557 | `d026f054541b232de6e49972bf90b936a8e872a249d7b1ebf8cb88415a77f833` | 1 |
| crates/bitwarden-auth/src/token_management/secrets_manager_token_handler.rs | 11415 | `de16f0f07e0dae8a411deb0f1f4eb9517dbaa13ea21e7af10ae5bb1770c09def` | 0 |
| crates/bitwarden-cli/Cargo.toml | 498 | `66c97e2ce1868f4fdeb02a1733de3aa7bd2e514bad2e6df117478b50b25ee006` | 0 |
| crates/bitwarden-cli/src/color.rs | 1043 | `2655e75de1e9c36bbbeca6eedbb878c118f112af0fe5740493e71c3c84b39858` | 0 |
| crates/bitwarden-cli/src/lib.rs | 459 | `16079cf64dd705e347cb175b6be003ed4e1ddb25a8d3a81c1d25dc50a78c20e9` | 0 |
| crates/bitwarden-collections/Cargo.toml | 1262 | `3604d7c284f8076ca26e6f72c680048d5eecbcd7196bc00fd993cfdf034c8708` | 0 |
| crates/bitwarden-collections/src/collection.rs | 13380 | `86019700aaa46de8c814b04db4464538978aaaaed514cd05ccc5cc8f8f5e800b` | 0 |
| crates/bitwarden-collections/src/collection_client.rs | 10460 | `64dd8a2e89b5e6c8c88da11be3632e74ccde628da27927b50ab06b79a3770801` | 0 |
| crates/bitwarden-collections/src/error.rs | 946 | `e7fb5d10d7a8ebaf89ad51d0c5d634741533e6521af60f7328000901a4f57a1a` | 0 |
| crates/bitwarden-collections/src/lib.rs | 821 | `451629dcb8c720c864c68b675ff24f9552c194b39362ab9d0a67e1e031b73e09` | 0 |
| crates/bitwarden-collections/src/tree.rs | 9744 | `718b6685a2cf5ec755c08e705118f5749cd84c35184b74f9a14d54ac10e3c242` | 0 |
| crates/bitwarden-collections/src/uniffi_support.rs | 65 | `b866e5045c0bf91493e1c750b2ceba7744afa61f7171f70159c3034c743e7714` | 0 |
| crates/bitwarden-core/Cargo.toml | 4414 | `da8ecb28e2920fabd7c532cda9563e113159afd98e3b7f00de1b22cabb278e88` | 0 |
| crates/bitwarden-core/src/auth/access_token.rs | 4518 | `8c53619397f7c8ebda9f6e57790546955e7e97c94f52eaf4a951a8d4894134a6` | 1 |
| crates/bitwarden-core/src/auth/api/mod.rs | 49 | `765b715c9b5d375e588edac715ccad98ec2c7a8643d351794e9a84b0f03b4e51` | 0 |
| crates/bitwarden-core/src/auth/api/request/access_token_request.rs | 907 | `d1987f7d9aeb99ecec05e79c18f6a03a95dd07133c1c837d7a6916e74d07b493` | 0 |
| crates/bitwarden-core/src/auth/api/request/api_token_request.rs | 1219 | `cb16d58207f9093f1f296c3b98824b948641a81555ef61bb8e7cb817c75ea22a` | 0 |
| crates/bitwarden-core/src/auth/api/request/auth_request_token_request.rs | 1629 | `87deac295ad848d4c775a752300ff2e0291288db0c24fe9b78d9541e2c78a866` | 0 |
| crates/bitwarden-core/src/auth/api/request/mod.rs | 1454 | `8a70a359daedd6bcd954ca4276ccda75eaca4088f5a4133d183e3d62b7115806` | 0 |
| crates/bitwarden-core/src/auth/api/request/password_token_request.rs | 2054 | `4fbc1ebb7c79ba9923e13e9ab0fb49a5e8a0b2d8adf9b91ebb0bd81124e3ddee` | 0 |
| crates/bitwarden-core/src/auth/api/request/renew_token_request.rs | 758 | `0a81e82ff838abeb374a39e545e614ba314b5ed43029d83b73ff0d69defee7ea` | 0 |
| crates/bitwarden-core/src/auth/api/response/identity_payload_response.rs | 356 | `7861b5ace359909c7f4d3612ff8a4627bd7d78f3be1a35ebfffe0cfcd4051846` | 0 |
| crates/bitwarden-core/src/auth/api/response/identity_refresh_response.rs | 313 | `89c21756eb341e210026e9bdcbf0b754e7dbff5f40ebfc34ff9ef64c95022e43` | 0 |
| crates/bitwarden-core/src/auth/api/response/identity_success_response.rs | 2996 | `2f92e64e948b2ec03f1367c5122fe1af2e422a1da3e1d257ad7e6ba38124f438` | 0 |
| crates/bitwarden-core/src/auth/api/response/identity_token_fail_response.rs | 971 | `6b2c1ac113d608e593eded0413fb19621d7dc9f6da23f7b7f8f6a048a5f5b3c6` | 0 |
| crates/bitwarden-core/src/auth/api/response/identity_token_response.rs | 2427 | `67f0093716ac9f74cbb22148732f9251d087fb3817f4babae0fa5ca789a06caf` | 0 |
| crates/bitwarden-core/src/auth/api/response/identity_two_factor_response.rs | 1092 | `05689fc57432c00fd615b6748b70f07c0f78fb3d3fbbc8abea7d508356fcd2e4` | 0 |
| crates/bitwarden-core/src/auth/api/response/mod.rs | 621 | `9b609b84eec44f028f135423cec3acbff8f36f085532deb07bd178d5b1b3f6ef` | 0 |
| crates/bitwarden-core/src/auth/api/response/two_factor_provider_data/authenticator.rs | 269 | `987faf3212074481d56e81221f34eba8f7d0cf2a3bf7a0dfa599da3a04073b40` | 0 |
| crates/bitwarden-core/src/auth/api/response/two_factor_provider_data/duo.rs | 372 | `ef16607a9ccd8ded5dde53e3437666054c0e0ddfb2d8b6866958f322e4322661` | 0 |
| crates/bitwarden-core/src/auth/api/response/two_factor_provider_data/email.rs | 315 | `4caef2b25305d4f11fa365ea3bf5a0ae0ed17ad7e162977de2ae98c0ef752377` | 0 |
| crates/bitwarden-core/src/auth/api/response/two_factor_provider_data/mod.rs | 132 | `c40ca1fe09e2d3b856d527cbd5a8ae8e4005c01cec0747895b3207f6cb0a4c70` | 0 |
| crates/bitwarden-core/src/auth/api/response/two_factor_provider_data/organization_duo.rs | 384 | `a90df4aa912f623fdc0bc73140e0af6e22170e230ea3d8b4b4d9c3ca9565a890` | 0 |
| crates/bitwarden-core/src/auth/api/response/two_factor_provider_data/remember.rs | 264 | `fea698f22e8b0d9536200923e5b9c3582df877de23999f2131c6f5f7a2096c4f` | 0 |
| crates/bitwarden-core/src/auth/api/response/two_factor_provider_data/web_authn.rs | 264 | `2b0302e3ef9e522c9b54b732159e68c8e6ce0cc17c9a4d271c3878f67833e5b9` | 0 |
| crates/bitwarden-core/src/auth/api/response/two_factor_provider_data/yubi_key.rs | 311 | `2d6780aebd576ce4bce2a7dc6ff50719faebce9e349c4551beae7cfb98c7c87d` | 0 |
| crates/bitwarden-core/src/auth/api/response/two_factor_providers.rs | 1748 | `7fff79d03cdb3c4a2c3c54f53d320958874083fd5001c5a65aaf8699822238ff` | 0 |
| crates/bitwarden-core/src/auth/api/response/user_decryption_options_response.rs | 716 | `1f830820b2b09dc9f37de489a0200ac5b470df8893c2546e5d9c9534e2295d41` | 0 |
| crates/bitwarden-core/src/auth/auth_client.rs | 7434 | `2f6b6cddced6edf62eeb852ab25c3e26490d0a8a7e162f5ef133c88cf9ee6856` | 0 |
| crates/bitwarden-core/src/auth/auth_request.rs | 13979 | `ad8629df10dea566429709dd65d054cbf1b8d02d08cdbf40a9eaad8108809c08` | 3 |
| crates/bitwarden-core/src/auth/auth_tokens.rs | 8273 | `01ceaeeab97eb895b41c824943e645107c9c2c7a901a9035db83434c66472189` | 0 |
| crates/bitwarden-core/src/auth/jwt_token.rs | 5641 | `1b06bc5c3069132021f08d9e169c9819cd23e4e186784384b2643bfd6c5e5c2c` | 0 |
| crates/bitwarden-core/src/auth/key_connector.rs | 1154 | `86ec60e78d55b15e46d242911f9998c1e806a67d18bc2cf8255a151b1ffdf216` | 0 |
| crates/bitwarden-core/src/auth/login/access_token.rs | 6470 | `2a69dff04dc21a2c438509f56599b3788542ace416cc56e45d4e79558b45071c` | 0 |
| crates/bitwarden-core/src/auth/login/api_key.rs | 3934 | `21204109477889a6d188d1f74bc48ca7703435e27abb0ca4df9898d0f5cfe05b` | 0 |
| crates/bitwarden-core/src/auth/login/auth_request.rs | 4370 | `1483ae6482d7dfcb2cad26fb848e41988d717b9740a9313f197842ccb8309fff` | 0 |
| crates/bitwarden-core/src/auth/login/mod.rs | 2343 | `00314cedcad7d82c96ef91b48a5b03db4b38b3b3430b774dee2e028dbcc6712b` | 0 |
| crates/bitwarden-core/src/auth/login/password.rs | 5440 | `cfcb3058e09630a38040ac19b1f8f5de17b6c0b4cf735e286f18244aa3dfe954` | 0 |
| crates/bitwarden-core/src/auth/login/prelogin.rs | 1715 | `c4256d09efc9a8c0e78926afe68454508a68156c25ebe6f1083fa573cf77b12d` | 0 |
| crates/bitwarden-core/src/auth/login/response/mod.rs | 43 | `9ba4e31648f914ffe2257fcff09f1c0b30f789da2d71419343b53f4a36d647c1` | 0 |
| crates/bitwarden-core/src/auth/login/response/two_factor/authenticator.rs | 491 | `173f00df0a330227a4d98dad98e6b594ead8e1500496593670e1c25af510f399` | 0 |
| crates/bitwarden-core/src/auth/login/response/two_factor/duo.rs | 883 | `fb27b8aa2d5381bb4fbc0349aa65a23760a8fbda6ac85c3f37236a7b661bcb2e` | 0 |
| crates/bitwarden-core/src/auth/login/response/two_factor/email.rs | 512 | `b5b0fcfc1884efb2c4c0e219af41e57c00718bf1a0ea042aec30ba2b7d516825` | 0 |
| crates/bitwarden-core/src/auth/login/response/two_factor/mod.rs | 266 | `586075cee6b8b1eb85a07f4acdf0d4141f9b5b39f9ae78a7d98983fcd548fbfa` | 0 |
| crates/bitwarden-core/src/auth/login/response/two_factor/remember.rs | 442 | `610615f19e0180beefcec694c40c573eb967e43fd80a6a3276e9fa363ab1e438` | 0 |
| crates/bitwarden-core/src/auth/login/response/two_factor/two_factor_providers.rs | 1478 | `0d6a220538f01e1364938bcbd26d3f4f0f3d20a9cb47c57d6403541590c6c896` | 0 |
| crates/bitwarden-core/src/auth/login/response/two_factor/web_authn.rs | 444 | `a2aa7f1b56b7482b62ac1d61c9214b4a5825c1ae1aa25be67e93a2177e01eb8b` | 0 |
| crates/bitwarden-core/src/auth/login/response/two_factor/yubi_key.rs | 543 | `7f875f45555a3605df9e70e7521c9a5d14d280ab4653e61a4ecc49590d4e00d0` | 0 |
| crates/bitwarden-core/src/auth/login/two_factor.rs | 2427 | `12b1c10d486d8360fc2320a211463bdf3a2b0a8033c134b8c9aa496ab3b43135` | 0 |
| crates/bitwarden-core/src/auth/mod.rs | 2026 | `dfb2b59c31e8d53a39f971f45bbe8046e3a48bc5fec0a42bd7b7f068b6406dc4` | 0 |
| crates/bitwarden-core/src/auth/password/mod.rs | 1255 | `c4f3388a319b6512802fc91dc9c75c29ec555cafebb07e35386e1b271decae46` | 1 |
| crates/bitwarden-core/src/auth/password/policy.rs | 4983 | `43cb072016b11a565d4bc7da0e848887c061d3c4bd73723dbaa4d21362ccd534` | 7 |
| crates/bitwarden-core/src/auth/password/strength.rs | 2105 | `d3b83cb05ef74fdf69ac57f62b5c5d46a269dce1e7c728a89d22df4aa9d71988` | 1 |
| crates/bitwarden-core/src/auth/password/validate.rs | 7322 | `7ea028cd1ac0a7ef65ffb2e30f7face923ddfe53dfe7930ba96d09002ebb385e` | 5 |
| crates/bitwarden-core/src/auth/pin.rs | 7671 | `0e4d78f775daeb3402cb81dd5de91ae2b82fb7f52ebdfca490e07cd67179ca3c` | 2 |
| crates/bitwarden-core/src/auth/register.rs | 1427 | `bfe92d0e92d320f0ecc37e1095505fc4105b9afe7fc665d21f6d9b64c31c005b` | 0 |
| crates/bitwarden-core/src/auth/renew.rs | 3259 | `f94b41092919202051055e4f41b62d36e3c9d3f3844d9df62e06fc9d1b908ae7` | 0 |
| crates/bitwarden-core/src/auth/tde.rs | 2470 | `9ed78ae457109554a3192b9fba6b3d4b4816e2ef7469f01bb5714bb9963254d6` | 0 |
| crates/bitwarden-core/src/client/builder.rs | 12802 | `f206d78c0fc4baf2ab9c6ef3ccf927b0402464f3d7dfca93ce7f6711281e8974` | 0 |
| crates/bitwarden-core/src/client/client.rs | 2306 | `ebf9cb05acb35bbf183df550dbffeec8eef906b0e55f32c7bfed60a46af0e73c` | 0 |
| crates/bitwarden-core/src/client/client_settings.rs | 9174 | `07939aaaa62e23937f4b1f33a984659416b6194bd8a81380774615ac7231cb1e` | 0 |
| crates/bitwarden-core/src/client/encryption_settings.rs | 5098 | `72761805f792aca211407ba7846308697d1e7e55de705668935ea69c0928ae9a` | 0 |
| crates/bitwarden-core/src/client/flags.rs | 2307 | `48628b6077034c4ec51870b78319719df594a789577c859dfc832aa2a2f3e450` | 0 |
| crates/bitwarden-core/src/client/flags_client.rs | 9538 | `b78bbd0169f36d12f265cd5ca421b221d52387c1dc2a3b2f176b69c96afb4fd6` | 0 |
| crates/bitwarden-core/src/client/from_client_part.rs | 4017 | `6bbfe6a5f552779a9ff6163a46e727db25fed6f6a0f7545b34b995be067ace3d` | 0 |
| crates/bitwarden-core/src/client/gov_mode.rs | 2452 | `edfeaf19f35a98aae7fbccd6c80901373cca0d44788c6a3d8f0db01bbbbb4d47` | 0 |
| crates/bitwarden-core/src/client/internal.rs | 21356 | `c09a43cbc97e7f680d98bb4710a4a119928e3740cf09504d812b2f1701180058` | 1 |
| crates/bitwarden-core/src/client/login_method.rs | 988 | `78625fdfa2d22dc4b65252e91d81c7bfbaac25592ef51c2a755bb97d1bea34e2` | 0 |
| crates/bitwarden-core/src/client/mod.rs | 1355 | `74963f645af64ec4d894aa8d458627c1be322aa68eec906505317e06795d4edb` | 0 |
| crates/bitwarden-core/src/client/persisted_state.rs | 2941 | `a2f5865ceb724712bc2c2c68bd3cdcaf6ccba9e1a410772e81f47dc5d410f9c1` | 0 |
| crates/bitwarden-core/src/client/rehydration.rs | 11397 | `3d1f3327bdc0b44d3ae680781c2ae7b39d911a9384b13631b052debbc3b2a174` | 0 |
| crates/bitwarden-core/src/client/tracing_middleware.rs | 3586 | `2f4af2b0baf1508437869c59d97a2faf3537c99701cf30df14d8020ee5949328` | 0 |
| crates/bitwarden-core/src/error.rs | 1428 | `26d7be2a34da4648dc909a23714e723411bdaefd1c4b5ffecbc4dc7e03b07b0d` | 0 |
| crates/bitwarden-core/src/global/global_client.rs | 2246 | `4331d2438af61724967cbe576056a2ba369e6cdb2bbe1fa6cbb25f9fc9000172` | 0 |
| crates/bitwarden-core/src/global/global_internal_client.rs | 1169 | `9b11700473f2e86736e55e7e5a11a01a9c28cd6f66dbb538dbf94d20b174cce5` | 0 |
| crates/bitwarden-core/src/global/mod.rs | 593 | `cae81da99a1d8a85aa26d8ac7cbf6394c6c60f940df0207bb7e7c7f6c72f67ad` | 0 |
| crates/bitwarden-core/src/ids.rs | 97 | `c4925f6907736da6cc2ca39bcda9bf948e53de4e0c3bc4597e27b603368c3f1f` | 0 |
| crates/bitwarden-core/src/key_management/account_cryptographic_state.rs | 58534 | `77795297d17e8f9cf253441ffbc0e07e7267e341479d8460c82485092a9d2417` | 0 |
| crates/bitwarden-core/src/key_management/crypto/reinit_user_crypto.rs | 26308 | `609851e2f65de545c8336206611df57d35b5ce3133ea3bfc6a68c66abcb8e439` | 0 |
| crates/bitwarden-core/src/key_management/crypto.rs | 101488 | `20416920c85baecf2244d821717e08922171e04ee9526276edd3d22df927d65e` | 8 |
| crates/bitwarden-core/src/key_management/crypto_client.rs | 18652 | `0baded531d71a70a021d02ee1a71791932af3f043172e611c30ac4474ba47929` | 0 |
| crates/bitwarden-core/src/key_management/local_user_data_key.rs | 7977 | `6a334335503b85fe81da34f310b7d5f002af180bb0d808f9458a12b6e5c6ba87` | 0 |
| crates/bitwarden-core/src/key_management/local_user_data_key_state.rs | 14626 | `12967eafd0f908024f9975cefb235f5e7586f35b92754d567868081b4ded03f9` | 0 |
| crates/bitwarden-core/src/key_management/master_password.rs | 24792 | `41d75dccce38fec35011d43278a8e4e5a6df019edd8a9aabb07f8c31aa493e2d` | 0 |
| crates/bitwarden-core/src/key_management/mod.rs | 5018 | `99c3f0e4a5e2752dbc1deb6db7d15e842adcc3cbc59c9f374a58eba9a1846d05` | 0 |
| crates/bitwarden-core/src/key_management/pin_lock_system.rs | 45362 | `0185d9b13adc3b4c7bd9c9e5cc69cb11151a30cc18080d237ce5b09da6c582d2` | 0 |
| crates/bitwarden-core/src/key_management/security_state.rs | 9462 | `5781fd4d8922e3c38dc108a35af0cebe51012f92a33373566ac90b7e69e497e4` | 0 |
| crates/bitwarden-core/src/key_management/state_bridge.rs | 5928 | `971ab8cbe1d4e5c130b5dfd6a1ac1627f888a869188b7f850e1413c61513f9d7` | 0 |
| crates/bitwarden-core/src/key_management/user_decryption.rs | 1575 | `926f68d1ea8cc24b6212a5bc7d81711db20f55f966998681a8a4461b5aae39dc` | 0 |
| crates/bitwarden-core/src/key_management/v2_encrypted_migrations_grace_period_start.rs | 1259 | `0c99ca312d78c0dc2c2de65552862c7e8e6a7c709617fa3fb1332f907b1138d8` | 0 |
| crates/bitwarden-core/src/key_management/v2_upgrade_token.rs | 16246 | `d38c1a259591cefcbe264b468e8ddc9261eebff7a4331a2e16bbac6bf01f7a0d` | 0 |
| crates/bitwarden-core/src/key_management/wasm_unlock_state.rs | 2594 | `62a9180d08abc159c2ad1418434cc5cdf442543ccd5d3027c69382fee5c0587e` | 0 |
| crates/bitwarden-core/src/key_management/webauthn_prf.rs | 6668 | `d4a662d2d2b708b0efe462b9a04fc759e019e671a5c20af7e6ee39f571ec7d21` | 0 |
| crates/bitwarden-core/src/lib.rs | 1023 | `d82a009fa811a825a8ac8106f0327b75b794a81a39436008b90c897be32b1bed` | 0 |
| crates/bitwarden-core/src/mobile/client_kdf.rs | 752 | `411074ba5188b1f9d112d57795739a308be30eb01fd97c26c74e4de05df34d72` | 0 |
| crates/bitwarden-core/src/mobile/kdf.rs | 399 | `2b7cc0ebf48c760bd3e964ca0fef71eff98c2c78918b8fe98030519ef6d2847d` | 0 |
| crates/bitwarden-core/src/mobile/mod.rs | 211 | `f1e81185e80a49abbbd1324af6985e4074fc8d2da1ceca0a8420808e49e64b0f` | 0 |
| crates/bitwarden-core/src/platform/generate_fingerprint.rs | 4140 | `6a25bd8a3dd0d26c255ecec694366549ddbe858004fc5ba95f7e6a88ae50adc4` | 1 |
| crates/bitwarden-core/src/platform/get_user_api_key.rs | 3619 | `c13355461652944bc066af639a6e3c24264ae40028050069b5e2aaaaddc1b665` | 0 |
| crates/bitwarden-core/src/platform/mod.rs | 610 | `38cb09fe8dc32809b1b196c593989154e7280db23f239ee54a4aa5ca4de862fb` | 0 |
| crates/bitwarden-core/src/platform/platform_client.rs | 1507 | `39af6acab2c2df22a09f575c09e673164069dc2d7ff91781ed99de3398504c78` | 0 |
| crates/bitwarden-core/src/platform/secret_verification_request.rs | 698 | `99525ca9be034eadfb8618e94013995c4fd874c771daddac29e5db2b2fa5dc50` | 0 |
| crates/bitwarden-core/src/platform/state_client.rs | 2140 | `e442eccb4294a94d4bc64a3bdf64523911558d17aa620c98666fe4173e55d772` | 0 |
| crates/bitwarden-core/src/secrets_manager/mod.rs | 154 | `b1fea8dd66227f3c052fec0d42ead1abecc288c80e6ef095d73ef4b51e995ecc` | 0 |
| crates/bitwarden-core/src/secrets_manager/state.rs | 2492 | `b7f415d6f4a6c792fe12e4bb5402e40b89c66e8eec55d8acf61c4c14b26a388b` | 0 |
| crates/bitwarden-core/src/uniffi_support.rs | 1358 | `2c69120714e208f01522f17dbe7fdaaf7f0607173cb383b1417bb96b7fdac1c2` | 0 |
| crates/bitwarden-core-macro/Cargo.toml | 556 | `032ee465afc3323bf207b1db817745a1c6e74cd2212464da19d24ac4eaaa5225` | 0 |
| crates/bitwarden-core-macro/src/lib.rs | 4855 | `ccf9ad1802b9916d8c370ddf05c773a8961021c341136cc58ce9fb0fbbecaddb` | 0 |
| crates/bitwarden-crypto/Cargo.toml | 3547 | `e32c5c2f39d895df9674e4121ef4dc9144938ba63595d11dee1f88217d483129` | 0 |
| crates/bitwarden-crypto/src/content_format.rs | 10131 | `f424a349a9bc487529deed883ac4bf97fa2d8470082e0eaaf6a7e1b14442e033` | 0 |
| crates/bitwarden-crypto/src/cose/mod.rs | 14303 | `41013fba25241d8acca009b1f03820ad901dd7dfbf36d1d545fc04200f230ead` | 0 |
| crates/bitwarden-crypto/src/cose/symmetric.rs | 60193 | `11daa5831402b64f2c0155950f8f61a3c2ebc226b549723490f15f1fb7e6530a` | 0 |
| crates/bitwarden-crypto/src/cose/thumbprint.rs | 6364 | `5f50c687ce02231a39be67fc0b5e2b36f1d15662203570d3cd4ae570e7e9b050` | 0 |
| crates/bitwarden-crypto/src/enc_string/asymmetric.rs | 17106 | `2458b9a452ba5257bee3196c9a2ad46a6d2fc06db2f2558e40e9bc1b01b409f1` | 1 |
| crates/bitwarden-crypto/src/enc_string/mod.rs | 3102 | `bd1d93bfd896edd1f098d50b00eb106ed53f01110e0b0954a953120a3d1c99a9` | 0 |
| crates/bitwarden-crypto/src/enc_string/symmetric.rs | 41917 | `abb92e98f0d723a726b580b93a42db501f876497bbd38687b5f2b4ba1c997a31` | 0 |
| crates/bitwarden-crypto/src/error.rs | 5141 | `27b87d65503f270dc0035d291322bc6e57a9a199a4f74e61d30842bf941edc7a` | 0 |
| crates/bitwarden-crypto/src/fingerprint.rs | 4155 | `df55d76d9a47c7fd71e8998b75d7a75562e961aa5cf791ca7c2b04a2497d6abc` | 0 |
| crates/bitwarden-crypto/src/hazmat/mod.rs | 265 | `a0ed53f6cbcb4439d2b2d24237edc81181b3626e76b1c6aee103f2846d95c9b2` | 0 |
| crates/bitwarden-crypto/src/hazmat/symmetric_encryption/aes256_cbc.rs | 4190 | `4bbfd9f842e12edb54b2ee4cc986ac42149b614ce1affc351d91043e88d297ab` | 0 |
| crates/bitwarden-crypto/src/hazmat/symmetric_encryption/aes256_cbc_hmac_sha256_ae.rs | 7757 | `7f324ac1897d48f4936ba0c57c12bfb315aae93f2b6696a0e3643922ed650c3e` | 0 |
| crates/bitwarden-crypto/src/hazmat/symmetric_encryption/aes256_cbc_hmac_sha256_aead.rs | 13049 | `0bad2bb078c8d9c50ffb2f5f464c2fd3b06e4dce8c295cc5b5c886e1e15a07ba` | 0 |
| crates/bitwarden-crypto/src/hazmat/symmetric_encryption/aes_gcm.rs | 7277 | `9f613ff754d0e6151ce2fcff664ce39b27b753811afb3f86da1a1dc278f92b32` | 0 |
| crates/bitwarden-crypto/src/hazmat/symmetric_encryption/mod.rs | 3383 | `f9f7528fc94856a202ff8f6a56426dfd2c0021843db89331d1b89bbde8e86a7b` | 0 |
| crates/bitwarden-crypto/src/hazmat/symmetric_encryption/xaes_256_gcm.rs | 7851 | `34c124fcb3a79812e39baf9724c64b9737617dc9f67883d8ed8a452c7e3f540e` | 0 |
| crates/bitwarden-crypto/src/hazmat/symmetric_encryption/xchacha20.rs | 7628 | `a3d65c92d0d806d9d01bf077c21bffa6456e3529cf619b65e5e44c00caa8f590` | 0 |
| crates/bitwarden-crypto/src/keys/device_key.rs | 7302 | `ebe351591a70d6801e52d1d3fec10c04c1defacaebd00991678bbf238dbb73e0` | 0 |
| crates/bitwarden-crypto/src/keys/kdf.rs | 8502 | `fc7b3f23d20b12226e7210575c98266e66cbe14bdb3bff8b520c44081bc21b85` | 0 |
| crates/bitwarden-crypto/src/keys/key_connector_key.rs | 12733 | `2c347bcb356b10779d8e31f722dbb3d7fdbf6664e76edd15015b86ecca758bb7` | 0 |
| crates/bitwarden-crypto/src/keys/key_encryptable.rs | 4237 | `1db9d67d68639f0ef69b4523499bb14e6538a181bef679dc6ca9e3c576c49160` | 0 |
| crates/bitwarden-crypto/src/keys/key_id.rs | 7182 | `36ea618949a9710a97a75dd074a2ee74f51afc252e90135e306a13ddb70ea333` | 0 |
| crates/bitwarden-crypto/src/keys/master_key.rs | 14332 | `64fffc73bd62ad6c954c93da38740e4e17c2106220ef9be68e15937fe74ffb38` | 3 |
| crates/bitwarden-crypto/src/keys/mod.rs | 1425 | `808d2df4a8fefa2c91125e52bf27af7b134b18fe27029e99aedbe82dcb862cf9` | 0 |
| crates/bitwarden-crypto/src/keys/pin_key.rs | 1913 | `50481c2e1e60f051f560868c661f5e1f14a10f27130631823a7e77d8143850c3` | 0 |
| crates/bitwarden-crypto/src/keys/prf.rs | 2002 | `324bbb1d7594b52cace72d75e7c3745e95d06410985269b6752992250d726515` | 0 |
| crates/bitwarden-crypto/src/keys/public_key_encryption.rs | 24419 | `1704487950b07675b6b2f1839aa082c5fdb657ad4d57e5555eb14914965c1aa2` | 1 |
| crates/bitwarden-crypto/src/keys/rotateable_key_set.rs | 8190 | `2c822a3d70bd874aeb0f64b17b8dc8275784e04812da1b2d860d9283f7c91e2c` | 0 |
| crates/bitwarden-crypto/src/keys/shareable_key.rs | 1999 | `688d4e3b661b9ac1eaac46d69694a6e66e930485cdae93da149df4cf8a04c8da` | 0 |
| crates/bitwarden-crypto/src/keys/signed_public_key.rs | 7793 | `03d58e91bb7f35c2fe785a5648780776360382bb971e1daf41c3dc0f038be2fd` | 0 |
| crates/bitwarden-crypto/src/keys/symmetric_crypto_key.rs | 55418 | `54b99010250372a45c4d5472c10e7411726fb1c0be541c1e28b35a0a663be277` | 0 |
| crates/bitwarden-crypto/src/keys/user_key.rs | 471 | `66310f8f12d3f1e02cddd566f0df1cfa97178986cbaa7d5ff2367e46f469ba32` | 0 |
| crates/bitwarden-crypto/src/keys/utils.rs | 7578 | `77f37a90b1388c7a142041a292eca95071474ab7f2c9e06d71369241739a63f6` | 0 |
| crates/bitwarden-crypto/src/lib.rs | 1750 | `c6a6363132bf94b46ff1dd356c73867cfbb080618ee4f8d44690647f4dce8060` | 0 |
| crates/bitwarden-crypto/src/rsa.rs | 2413 | `9ad610028bf0dbc2dafa8bf0f9341d43fe0032385a7e5e6218d6dd2f94341f7b` | 0 |
| crates/bitwarden-crypto/src/safe/data_envelope.rs | 34969 | `4cb3d46ef14ca958d189067049d9c9983f5ef8a91ea4f9b5ee76d5c9a48a9efe` | 0 |
| crates/bitwarden-crypto/src/safe/helpers.rs | 8781 | `eaf845b329afc7144f31d7fde9ebc7ad7777b3c0b936bf9ff76eac3d75709edc` | 0 |
| crates/bitwarden-crypto/src/safe/high_entropy_secret.rs | 11275 | `a975eb83c844edd0665f6bfe670d5a802df861ba07d6bec25044757800df6fc9` | 0 |
| crates/bitwarden-crypto/src/safe/key_hierarchy/content_encryption_key.rs | 3573 | `f4753c275086f91a5b201f7d9cbd078ea4c3228442cc2d7d701ff382714cd4da` | 0 |
| crates/bitwarden-crypto/src/safe/key_hierarchy/key_encryption_key.rs | 3699 | `bd2f03795cb042e28a5b7bb5e1a58b3c8ec6f1d97514d418ddd789e38e0713ae` | 0 |
| crates/bitwarden-crypto/src/safe/key_hierarchy/mod.rs | 157 | `227654c36ffe669ed4cff327c174d062efd90d39e851e2b1dbd1a6b4651db684` | 0 |
| crates/bitwarden-crypto/src/safe/mod.rs | 4319 | `70ad0f25765bdd484bce91d806771b704a657c8ebdf21f016f6ab6fa68d0552c` | 0 |
| crates/bitwarden-crypto/src/safe/password_protected_key_envelope.rs | 50202 | `be7b48839d6b6875e0c92ee0fd6599429fc68a91c770d9be4bf225df1795a02a` | 10 |
| crates/bitwarden-crypto/src/safe/secret_protected_key_envelope.rs | 41179 | `19df402afdd45dafc6140863f59476ffe5f8d849f64d2eaf1dddaabcce7aeb66` | 0 |
| crates/bitwarden-crypto/src/safe/symmetric_key_envelope.rs | 21372 | `19ced80a5239fd770c8e18dbec46fa81b481d1eb1ddd3106c8e84e04acc96392` | 0 |
| crates/bitwarden-crypto/src/signing/cose.rs | 6650 | `6563e381a3b09ab3053066665333a151f7d67532eb8a1471c984198af56656a9` | 0 |
| crates/bitwarden-crypto/src/signing/message.rs | 4217 | `ccd037f8266b20337dde40fb10875732e80a810e0f6f8ac6f01ee4a2cd4d5dda` | 0 |
| crates/bitwarden-crypto/src/signing/mod.rs | 5056 | `1e43cce378003459a2f9372da3243d9549866a5a451c3bd7c170d82fa3f5d615` | 0 |
| crates/bitwarden-crypto/src/signing/namespace.rs | 1894 | `5fa03f7d5708bed96b997bc4d56e99da0578ce997582c003d7ed3aeff9839649` | 0 |
| crates/bitwarden-crypto/src/signing/signature.rs | 11288 | `e7f8e6d4e653380784381cc6679d9522394d5830f0d7125da98d1f3b61bb52a8` | 0 |
| crates/bitwarden-crypto/src/signing/signed_object.rs | 10990 | `f919cd50540dc2d02c3e7773e9b4646e0bdc7e7036f761f5e8e6643b5a88a71a` | 0 |
| crates/bitwarden-crypto/src/signing/signing_key.rs | 23425 | `94a830bfd05b14dbb4feb1135fda84ee8312a5dc28661117e8e15e206a1d1292` | 0 |
| crates/bitwarden-crypto/src/signing/verifying_key.rs | 13185 | `8202ab50d63cb84ba6676827335edf2f69d82b747db1c79bc971b945e9bc3461` | 0 |
| crates/bitwarden-crypto/src/store/backend/implementation/basic.rs | 1353 | `57072aa35fab388e9bc2cdcb6a5ca233fd3f98d31d9d633e54d2cdcacaff5d44` | 0 |
| crates/bitwarden-crypto/src/store/backend/implementation/mod.rs | 754 | `25ab1ee3d4bc5798c3f69e085650b01e2ce9972205a6bc6a34b3a5e38f2759c4` | 0 |
| crates/bitwarden-crypto/src/store/backend/mod.rs | 1411 | `253a984a8a7bcfa31f52173238857f071e8cdd3ea11cff0771a57bd502eb9f07` | 0 |
| crates/bitwarden-crypto/src/store/cipher_suite.rs | 3066 | `2ff918838d2f67c4485568aaedf258a2fc46f5ece09c549909167ca9db0a2a47` | 0 |
| crates/bitwarden-crypto/src/store/context.rs | 51392 | `0997514df485f9ee63def0fa385220ab7f15d3b70490f125f974e73b7b9e4326` | 0 |
| crates/bitwarden-crypto/src/store/mod.rs | 19446 | `4e664e970fb1c825e87be4240a9271ef62ef2e53727f9d87db6d22926e14ab80` | 0 |
| crates/bitwarden-crypto/src/stream/aes256_cbc_hmac_legacy_stream.rs | 28225 | `6418b8f866772ef166ceb23f09aa3343b85d35883dbb5cd7bff912b7ded2afb2` | 0 |
| crates/bitwarden-crypto/src/stream/large_memory_buffer.rs | 4156 | `a852a22a7438d9a1809f2d2fb363ceb8d4410f7daeb99471012517c900724b03` | 0 |
| crates/bitwarden-crypto/src/stream/mod.rs | 5719 | `6a7a36a4e48c4d1170456074aaa579e8f48f4630ad6a78a11c68056f90e3a7b7` | 0 |
| crates/bitwarden-crypto/src/stream/streaming_attachment_cipher.rs | 26147 | `b7a62e51a4bcafade43967bceda4e2d2e38321644f60907ba70844467925545c` | 0 |
| crates/bitwarden-crypto/src/traits/decryptable.rs | 4921 | `a604757f37d80025d4d7d4e8c35c080ace5afd52705c2007b5dd8c296f755872` | 0 |
| crates/bitwarden-crypto/src/traits/encryptable.rs | 12627 | `d8751f85752bbc28e1bf7a081ce5dd5147ebbbcf94fbaddd179cf3e715d1a75c` | 0 |
| crates/bitwarden-crypto/src/traits/keyslot_ids.rs | 5573 | `8927f791b1e9ce63a3254fb238d77c1fa7c41519f5c0a9685e7487432d4e4d1d` | 0 |
| crates/bitwarden-crypto/src/traits/mod.rs | 1210 | `cdd341ad3397e96ec4144c2dfc7f58bb35ce601a6fde3518111a6316beb0b6f5` | 0 |
| crates/bitwarden-crypto/src/uniffi_support.rs | 2624 | `2d263e79ab74585a0ee83fc7da12d77e15f5b4f8d0bed350ae950e9806c7e1e7` | 0 |
| crates/bitwarden-crypto/src/util.rs | 4398 | `1a33be9168a329241c7743f598527e4e32a38c5dafd19bc2813028b0735cd84e` | 0 |
| crates/bitwarden-crypto/src/wordlist.rs | 116678 | `822f3044c50b3569ee1f0abffbed258de339371190011299774416fa30bca8da` | 0 |
| crates/bitwarden-crypto-cipher-suite/Cargo.toml | 924 | `0b0f83b5385be2a9774a5f95dced5debeb9576eeee7a0deade2665c49c59aeb5` | 0 |
| crates/bitwarden-crypto-cipher-suite/src/cipher_suite_client.rs | 3520 | `fc02e1ce4f5bb2153e5424dac6973ac63422353e5fdf0adc42a6431607e98e7c` | 0 |
| crates/bitwarden-crypto-cipher-suite/src/lib.rs | 149 | `f46f9526e93b1c1d61ff83d3f16bd27401217696421761593cb27d3fd501443d` | 0 |
| crates/bitwarden-crypto-sync-handler/Cargo.toml | 1582 | `83c537055a7ff53ef96e16bbcce990a6f30744dc4de5184336580c70a8154deb` | 0 |
| crates/bitwarden-crypto-sync-handler/src/crypto_sync_handler.rs | 22541 | `2f0533455f3b2efd80ba6fa1f4b1390168c5737227b55210eb30cf1ef48c9859` | 0 |
| crates/bitwarden-crypto-sync-handler/src/lib.rs | 436 | `126254245532907fa380a9ce091a74ecaaa3e784d8b62cb15d451195c9bbab45` | 0 |
| crates/bitwarden-emergency-access/Cargo.toml | 1614 | `a374bcbf614d8bf648437c75ffa2499d1b91d83c37bcb1e7ffe9af485e45f9af` | 0 |
| crates/bitwarden-emergency-access/src/accept.rs | 2683 | `02c4ea15a1fcd8836ce7bd5b14a9a75049a569c106f4f2f19ab97475f66ddeca` | 0 |
| crates/bitwarden-emergency-access/src/approve.rs | 1997 | `1e9527d6527309199643c37fff77e2e17592f4d2d33061bd6ed6022471ababd7` | 0 |
| crates/bitwarden-emergency-access/src/confirm.rs | 5823 | `cd8caf1c9e88ed98fe4c91a208c49b8e90be847cff0d820f13cc67f737f0d75a` | 0 |
| crates/bitwarden-emergency-access/src/delete.rs | 1962 | `f0762b7b2563f1d90599708c5adb73daec54398b1e13a9f4b0a9118f94c5d38b` | 0 |
| crates/bitwarden-emergency-access/src/emergency_access.rs | 5935 | `d3f2b7fb2a56695b56a904d4e52ceafc251a3cfbf8bc4e88426860c3415f827f` | 0 |
| crates/bitwarden-emergency-access/src/emergency_access_client.rs | 1036 | `45fc0fa2a9b2fdb20ea79ec439ba0ee6fa4248ed0f31d97327333bec2d969d91` | 0 |
| crates/bitwarden-emergency-access/src/get.rs | 3626 | `f40fa36879ba3352147e8943e7b5cf74906fc936cc5ff5b8de51e3173d501b92` | 0 |
| crates/bitwarden-emergency-access/src/get_grantor_policies.rs | 6313 | `c764600657670858f46b33652990a8772c2edebb426f99ad150b0648c6f02b8e` | 0 |
| crates/bitwarden-emergency-access/src/initiate.rs | 2058 | `5ab1ab1f57e02cf3da9e38557d9c4e4b4ab12e3de180937b1b5c24c9160fe007` | 0 |
| crates/bitwarden-emergency-access/src/invite.rs | 3170 | `90a1981b5b74b2db1b9e0c5960504d00f4beae0e6d923cf16b9367358b0b0c7b` | 0 |
| crates/bitwarden-emergency-access/src/lib.rs | 1304 | `8222d844c0e08a0470f46464b0444c06a84f6c692c530541782417613aa7087d` | 0 |
| crates/bitwarden-emergency-access/src/list_granted.rs | 4877 | `0292af3dc8388a328120060a0d51880786b405a0d48d5b8d32249a393e1ecf93` | 0 |
| crates/bitwarden-emergency-access/src/list_trusted.rs | 5910 | `350418af37e076b15070a73130c0756a849d94c20c4e3c986ef37254ab312fad` | 0 |
| crates/bitwarden-emergency-access/src/reinvite.rs | 2023 | `c1a85492bc5c66e3ae2241a561df03beca55c6be1b4a44a9dd292f7029b91827` | 0 |
| crates/bitwarden-emergency-access/src/reject.rs | 1958 | `d63f2720000450b4b2d4cddec6d1b9d05960299bd2653eb2e277cf6ef2a81194` | 0 |
| crates/bitwarden-emergency-access/src/takeover.rs | 16055 | `271b930de2a764796382b0e9683e7fc2828dfb6923acbcfd2cebbf5f118cca3a` | 0 |
| crates/bitwarden-emergency-access/src/update.rs | 3110 | `134ccfdc244634f4f28429a65f3496fc423eb76fd7a0c7b96b79034fcc1fc9c3` | 0 |
| crates/bitwarden-emergency-access/src/view_vault_items.rs | 11534 | `5ce49bc0257864bbea985f933d0bd498d8ca3f6bf67f40897e510d098d97f68a` | 0 |
| crates/bitwarden-encoding/Cargo.toml | 1053 | `d8ce5ce8db1a032d3088287df3a66645022383b5a6671fbc6fe7b165d44e4516` | 0 |
| crates/bitwarden-encoding/src/b64.rs | 7023 | `6cb8d826228d3075d8b784ff8f8ef4ed62ae6e9d17154573958d25b7e9623fa0` | 0 |
| crates/bitwarden-encoding/src/b64url.rs | 6702 | `ee619a6881e95c4fe7e373d3e98bc00a0a5d1eac90d1aa854df7ecd121c36109` | 0 |
| crates/bitwarden-encoding/src/chunked.rs | 3019 | `bc20e57bcd2097156af6d9102766705c19061ad71dc52048dae94553bd60cf88` | 0 |
| crates/bitwarden-encoding/src/lib.rs | 312 | `850ea859586665f6d5b04d0f5008b3dd5aca125f3560a10b7e2282bd3bb10bb0` | 0 |
| crates/bitwarden-encoding/src/serde.rs | 832 | `2a2d386eb6053070987c9675759033e4bf3ea02b2077260ac41cef3a8d4def8d` | 0 |
| crates/bitwarden-encoding/src/uniffi_support.rs | 397 | `f95e1a38e2d6d2276bbebc573d794cd9cbfcfaa7cb9ce8ddcd673683aa8a8e96` | 0 |
| crates/bitwarden-error/.cargo/config | 68 | `9ff2ef513df9e780376850768592b6fffda0a564450146f0a776523b1aaa58c5` | 0 |
| crates/bitwarden-error/Cargo.toml | 826 | `9ac38271eda82e407ebbfb66c39370431f05396745c9626c94a0d7007e0ceb8d` | 0 |
| crates/bitwarden-error/src/flat_error.rs | 92 | `bdf30d33be8ed36648593a4264d6629d75ac5c18e422846e8d51e1615bea5a92` | 0 |
| crates/bitwarden-error/src/lib.rs | 586 | `8c984a49e6f07798554743394f015ee18add536d70b4a0c0e8c9b36be8b5460d` | 0 |
| crates/bitwarden-error/src/wasm.rs | 1022 | `75f7147676321789adc0482f877e69bc4eb6b99da0921b791e9ba4ade10c9d2e` | 0 |
| crates/bitwarden-error-macro/Cargo.toml | 725 | `cb06746edbf4c727e495aa9fded3face1cec3d4a75e707ffbe891d3982fb467b` | 0 |
| crates/bitwarden-error-macro/src/args.rs | 588 | `19c2c6229989c9e30e7f40fab47c95d8b25b65b2680ed38bb7d9108e2f8d8ce7` | 0 |
| crates/bitwarden-error-macro/src/attribute.rs | 1533 | `e21c9d6d3d252083c71c37d6899b5b9fe1c159cd5cd50418a903937acf70e4fd` | 0 |
| crates/bitwarden-error-macro/src/basic/attribute.rs | 2192 | `42bdafc731f862248c274876b978e5dba147021bcb65ce952ac20af51ec3fbde` | 0 |
| crates/bitwarden-error-macro/src/basic/mod.rs | 19 | `aa4a5db2b669a6351d9b614ec311c219243dddf5500435874831fdc2f29bb0e4` | 0 |
| crates/bitwarden-error-macro/src/flat/attribute.rs | 4367 | `7138deda7e0b8964befd9f9f22fde320643577cd13104c2a78dee33343dc6bc1` | 0 |
| crates/bitwarden-error-macro/src/flat/mod.rs | 19 | `aa4a5db2b669a6351d9b614ec311c219243dddf5500435874831fdc2f29bb0e4` | 0 |
| crates/bitwarden-error-macro/src/full/attribute.rs | 671 | `f322e2e7dc64350e6990422ae52190180ae4cfeaeb848fe2deeb6042f5b2589d` | 0 |
| crates/bitwarden-error-macro/src/full/mod.rs | 19 | `aa4a5db2b669a6351d9b614ec311c219243dddf5500435874831fdc2f29bb0e4` | 0 |
| crates/bitwarden-error-macro/src/lib.rs | 2972 | `eeea5d637931e31fbef7f776b28a694561e8a3e98074bf9e9323fbd9aa4cc682` | 0 |
| crates/bitwarden-exporters/Cargo.toml | 1653 | `71ac53a0deda7294a018fb9a32513cbe1d1476d37a6fd289fc882bc5ef36e6a1` | 0 |
| crates/bitwarden-exporters/src/csv.rs | 9155 | `7ea33cdc450c6004abcef8d6e57acac12455ea258960a2d91365f167f253543c` | 0 |
| crates/bitwarden-exporters/src/cxf/api_key.rs | 5688 | `81326af20301889e350e8bc420c6ffef83676bfdec686dae98591e180a30fc83` | 0 |
| crates/bitwarden-exporters/src/cxf/card.rs | 9144 | `9f0eee628ea39efa9a04d896d21ac59c174bee1441b833b6a42dd06c217cac61` | 0 |
| crates/bitwarden-exporters/src/cxf/editable_field.rs | 16649 | `a78c46378de2eb189a8f64d91514214d4fc564713426270cc3bf723d0e87bcc1` | 0 |
| crates/bitwarden-exporters/src/cxf/error.rs | 232 | `09a738113cf8bbf6c82b0b86196372a8430eda59976d47843b496768f09f3a3f` | 0 |
| crates/bitwarden-exporters/src/cxf/export.rs | 14488 | `7e2da9e3474f51b8b297c74bb4175cbdd93e5e7f19cb1be7f9ed8f67f3462f77` | 0 |
| crates/bitwarden-exporters/src/cxf/identity.rs | 38635 | `ff1d7b8ed4834474203c46a48a8a1e24b691d13b089803dacd79b259035e8cc7` | 0 |
| crates/bitwarden-exporters/src/cxf/import.rs | 48658 | `342c620bad7fc77e406066e797061c0d6de8b44d8f8e887770b5030884ce2d56` | 0 |
| crates/bitwarden-exporters/src/cxf/login.rs | 22463 | `f798fb6ad4ca0508f163965b5bd97c0f6edbcd0a2f08d471aaa50c291a4be551` | 0 |
| crates/bitwarden-exporters/src/cxf/mod.rs | 512 | `d1969bc1d03ce922fdbfbceccc41720a645766502deda05e5327fa32b22a9449` | 0 |
| crates/bitwarden-exporters/src/cxf/note.rs | 3784 | `2af9dc638459c5c5070660777bbb76e55bc89dab57e7f922274c034b866cd35a` | 0 |
| crates/bitwarden-exporters/src/cxf/ssh.rs | 6460 | `41f4971ed2f336cb420176f1b9b292271138002eac8c38244364c6860930d1f0` | 3 |
| crates/bitwarden-exporters/src/cxf/wifi.rs | 7119 | `1d6ad9c7676116e1b67f0d9d210efe4a0a189198dcdad7e110a77594071afb60` | 0 |
| crates/bitwarden-exporters/src/encrypted_json.rs | 9939 | `543be0f48148aed949d5e44db722b40a2ad281fcc9f839c016d6b463c1bc374d` | 0 |
| crates/bitwarden-exporters/src/error.rs | 846 | `6d8b78dfa39bab42ede8b83db44b52f64f49e6550d7e7674b2d15888ce15ffc3` | 0 |
| crates/bitwarden-exporters/src/export.rs | 6897 | `8729ef84f064876fd8f99d04982f92e22858b7f262aacf1d5f6102fe41fac3d4` | 0 |
| crates/bitwarden-exporters/src/exporter_client.rs | 2825 | `3f1a34cb7a76f7da246f7240137f459a71949ffb4601a422790069ff269d3f80` | 0 |
| crates/bitwarden-exporters/src/json.rs | 37563 | `ff2d8ed97291374c6e775ce62ca72eff284111a865128e71ea767cf2f0224dc7` | 2 |
| crates/bitwarden-exporters/src/lib.rs | 26101 | `148240d36e53ceb80cc0d56437186a63394cd59887b55224bcb005c2a982165d` | 0 |
| crates/bitwarden-exporters/src/models.rs | 13606 | `ae0a41ebea3f5f455e8b3c46570a9b0710450931c152c28957fd74a55e6d1a5f` | 0 |
| crates/bitwarden-exporters/src/uniffi_support.rs | 65 | `b866e5045c0bf91493e1c750b2ceba7744afa61f7171f70159c3034c743e7714` | 0 |
| crates/bitwarden-ffi/Cargo.toml | 961 | `f12f5e9471af2306bc9d8af9423b3bcdfcdcf263124a0129ee1ec1c9d226bf87` | 0 |
| crates/bitwarden-ffi/src/lib.rs | 768 | `3857270f4529ea41164950d28a7e096ce537db7e3bdc50b189e306c20a598fbb` | 0 |
| crates/bitwarden-ffi/src/wire.rs | 5189 | `ec561ce1afff8c7bf300463d22d692c3894f2808487c050221cdff13d46faa56` | 0 |
| crates/bitwarden-ffi/src/wire_macros.rs | 5262 | `406fc43874cac9868496d7b8b97288bcabd71b2368d9a3bd87f25275fb9391e6` | 0 |
| crates/bitwarden-ffi-macro/Cargo.toml | 555 | `eda6a775351e3f27ff0433c1f377e92acc23adf460deeec64c31422af6e67e73` | 0 |
| crates/bitwarden-ffi-macro/src/attrs.rs | 2728 | `f96ef52c63deafc541ec685fa486a5357edc78c7e6db3b5819b3a606aa61a601` | 0 |
| crates/bitwarden-ffi-macro/src/lib.rs | 4861 | `1cb9a8f9135eac0cbce718f57f9fc83760b5647ee826e8ac6606042b8f693757` | 0 |
| crates/bitwarden-ffi-macro/src/wasm_export.rs | 14748 | `d14ed3b6b8bcb42194158a111b393cf2e06e8c8f2c1fe863aea9661b6b4170bc` | 0 |
| crates/bitwarden-ffi-macro/src/wasm_import.rs | 5088 | `9c6d8adaab17b30b818e9e6c1a5bf19cdc0a79a353412b4292c2d428db1f2f4c` | 0 |
| crates/bitwarden-ffi-macro/src/wasm_object.rs | 3154 | `ab44a62b2f220458ae47058f85a733e8666fd0bc3073c37e22bcc6f1ae37160c` | 0 |
| crates/bitwarden-ffi-macro/src/wasm_record.rs | 4231 | `8848f4c34244bee5932d156009021718efad3162c47616b0ff6d5263c403f09d` | 0 |
| crates/bitwarden-fido/Cargo.toml | 1405 | `2b27ab1a52e5bc4b64040d6b6dec65d4f4acd239d6180fa34b0005a2352a776b` | 0 |
| crates/bitwarden-fido/src/authenticator.rs | 31589 | `b313f865aa31c1f6f85dfc3017efb9f1a1b811acbf42b1e6cb15bcf9fe464ad4` | 0 |
| crates/bitwarden-fido/src/client.rs | 5535 | `18339fd07599fd537e667fdb15c2552e655d7b6cb3f05bcb0c6be92a33ac2038` | 0 |
| crates/bitwarden-fido/src/client_fido.rs | 2321 | `0d3a4cc6d8e74d28a1a1f245eb41f0f39275d5646fa136223ef5c04e0d9a24d3` | 0 |
| crates/bitwarden-fido/src/crypto.rs | 4149 | `73f924cd1cd08b9a0340d251d9798707bd9d3dacdd1a0387d96234913516b9ba` | 0 |
| crates/bitwarden-fido/src/device_auth_key.rs | 32571 | `ce7a028f0188d1360dc98c0ee3ef5669ff965b0bdd34966f74e1d74c1c45394e` | 0 |
| crates/bitwarden-fido/src/lib.rs | 10979 | `ef78581d56e9e4927caf122d495081072c4dc2f42837a7399c47b0aa8d2adf9e` | 0 |
| crates/bitwarden-fido/src/traits.rs | 2121 | `7217ad569e71cacb136d81e24a644cdf567780380af67a9a151ec45fab7d27b2` | 0 |
| crates/bitwarden-fido/src/types.rs | 41169 | `ca2706352865299d80d290821a9c4a4d191cdd1cb35c2d991cf530016950d964` | 0 |
| crates/bitwarden-fido/src/uniffi_support.rs | 164 | `37ea90629d3729662641c313485015440e657bfa3f09b439b9397e8704dab908` | 0 |
| crates/bitwarden-generators/Cargo.toml | 1256 | `14e1f8fb4e0544386e9805d4689424ad56f40885f4f69e0514a0942d2b12afe1` | 0 |
| crates/bitwarden-generators/src/generator_client.rs | 4318 | `fc1714bbea147802653ee7d873d9840b5dc25481698c2dbff1e61e5092a00d3e` | 0 |
| crates/bitwarden-generators/src/lib.rs | 786 | `ca617a26dbb2f1c72c5301d1130fa859da29587e04dad756eb05e298897b2c0a` | 0 |
| crates/bitwarden-generators/src/passphrase.rs | 8215 | `ea3455b6321effa01768d28328141db05ee410a2517da08438928c378104043c` | 0 |
| crates/bitwarden-generators/src/password.rs | 30781 | `c0848274a80ffb3752bc54ed2b8080e60928017d3de76a3e61996799b2d47926` | 0 |
| crates/bitwarden-generators/src/passwordrules.rs | 18777 | `1ef61943e416c6b310455fede73c882f1ed2acf53b94637c4ca2e499ba1c0da9` | 0 |
| crates/bitwarden-generators/src/username.rs | 9312 | `ccd1349efc679af4a104e981b1d9a127789dcc408bd0d2d4edf6a8cbd8337ff0` | 0 |
| crates/bitwarden-generators/src/username_forwarders/addyio.rs | 5357 | `dca6bda8a71f7b8b58f97526ce6fc0e7f5eaa25891d31b645bdcb661f69991db` | 0 |
| crates/bitwarden-generators/src/username_forwarders/duckduckgo.rs | 3066 | `b3cdbe60be91a6cbd7103fa1ad146d97b0bce7544b93f5d643d1bf9c4d4c5a88` | 0 |
| crates/bitwarden-generators/src/username_forwarders/fastmail.rs | 6866 | `02f5ae3e3672eb418a25a397484f352948e47d085eed8d7c4010f3f19e6d4a66` | 0 |
| crates/bitwarden-generators/src/username_forwarders/firefox.rs | 5427 | `2ce6a5c64be31044e9a0667f7b18d1db63e957a8d778d6eff768bde28a443759` | 0 |
| crates/bitwarden-generators/src/username_forwarders/forwardemail.rs | 6707 | `26fc2f1de0ae4e9a333442542d34912b2a68f12d20eaa4456e8c1185a950fbc3` | 0 |
| crates/bitwarden-generators/src/username_forwarders/mod.rs | 625 | `1cb25f6000588cd4145820ec7b84116c632c3d5bade2557e693fd707fe3aba92` | 0 |
| crates/bitwarden-generators/src/username_forwarders/simplelogin.rs | 3991 | `901b71f1303b9ede825ed129a494a11898601c2734d90a017669e52476046eec` | 0 |
| crates/bitwarden-generators/src/util.rs | 495 | `bdec44c689c85f2baf414ee8a53c0b5ef5cd49f2cb0f852e050225d45439206b` | 0 |
| crates/bitwarden-importers/Cargo.toml | 2683 | `c1a566d095f91c07247e1d9905fcfdbb1883a5b1159dec564903d84061cca41b` | 0 |
| crates/bitwarden-importers/src/error.rs | 1987 | `48939709d6a5f42d49ad15d87b709e544b2a88f57f966afa3ebc54ca2f952875` | 0 |
| crates/bitwarden-importers/src/import.rs | 2229 | `44a4bf4ae86e5ef129168465551d8bc9f55e2dc51953b85340e3e096ed7c9558` | 0 |
| crates/bitwarden-importers/src/importer_client.rs | 3751 | `b5075066f87ac2839a434a112de006084207f1c8c784e37fd4f8b440712109f1` | 0 |
| crates/bitwarden-importers/src/importers/kdbx.rs | 18906 | `b0f947e1fb46ce52ba05d4b83e327d92041ca43227a5f35a974e891544407729` | 0 |
| crates/bitwarden-importers/src/importers/keeper/crypto/error.rs | 1304 | `e53974fffb11f41524bf4adc1b6d96e3689d78666d4f8be11ff1dd4d54f9d425` | 0 |
| crates/bitwarden-importers/src/importers/keeper/crypto/mod.rs | 1276 | `518d2573d54a7ff017bdf67a8e927591aa7da84486b84f40c3379f8de5e5fa2c` | 0 |
| crates/bitwarden-importers/src/importers/keeper/crypto/types.rs | 35235 | `87db9ef4a5eaf0ca4d1f9e21ad728b591ea21e173a1cdcdb86b65e9eed926455` | 2 |
| crates/bitwarden-importers/src/importers/keeper/crypto/utils.rs | 5042 | `68b04dca40c1446bbb16ae19a583d2ad226f459a9b7577cf72981526103448be` | 0 |
| crates/bitwarden-importers/src/importers/keeper/mod.rs | 791 | `cf9340d45213321c419afc9ef148ad24cff9420eb551107b75a090bbb4c5b958` | 0 |
| crates/bitwarden-importers/src/importers/mod.rs | 237 | `762e46354209d358c46a81f3a3e0e3765028a69c507e7dafcdd06f568da39998` | 0 |
| crates/bitwarden-importers/src/importers/onepassword/access/account_key.rs | 6925 | `0294c934b55c0333ec4016f2527f8f1d26a6844962e72f8dcce88387fb757eea` | 0 |
| crates/bitwarden-importers/src/importers/onepassword/access/client.rs | 27280 | `24f47ed71146919af659d5ba776503221a55352c1fd437f745babad03270b688` | 0 |
| crates/bitwarden-importers/src/importers/onepassword/access/credentials.rs | 1249 | `a5db36d98747e77c1d372075c84da76c2aaa607c5158a11feff6f658e4e40a42` | 0 |
| crates/bitwarden-importers/src/importers/onepassword/access/device.rs | 7004 | `b92218b10483248d700319bbc42a05c517f0fd4dd61be679c9adf0ebedcc466e` | 0 |
| crates/bitwarden-importers/src/importers/onepassword/access/error.rs | 2610 | `02080d783bb463e8da3eb7285ca52d86f731dbe829576f6725c2848a71bd8e45` | 0 |
| crates/bitwarden-importers/src/importers/onepassword/access/identity.rs | 2447 | `7337400e1edf33c8bf59c659898b4e26a85d1b98f46e2d1eeba5ec54fd0fe58b` | 0 |
| crates/bitwarden-importers/src/importers/onepassword/access/kdf.rs | 9720 | `efb80861043868f6373858c165d9760b16127a3420856d724c34321b8f10167e` | 0 |
| crates/bitwarden-importers/src/importers/onepassword/access/keychain.rs | 12437 | `ae0b75f16e9dca8d8b71deb5b7dbccf465cbd2a395bdf8c6a85c81c3ed24a5a0` | 0 |
| crates/bitwarden-importers/src/importers/onepassword/access/login.rs | 17762 | `50290182a23ad2cffc65edb34dfac6b8341584032462c9efbac0531a8274789e` | 1 |
| crates/bitwarden-importers/src/importers/onepassword/access/mac.rs | 5409 | `f8cf86df0bb1f7fb5992e6455824e09de2624c9be106226cc93708d044f0edc8` | 0 |
| crates/bitwarden-importers/src/importers/onepassword/access/mod.rs | 845 | `a34b6fb9e7c1ce2930b60a481f32374ee84915f58828257936066743aca566ae` | 0 |
| crates/bitwarden-importers/src/importers/onepassword/access/model.rs | 5738 | `b7bf8e11292bda5b4db427854b93af0fffc8ee7fd8ff963a5f05134a1501cc10` | 0 |
| crates/bitwarden-importers/src/importers/onepassword/access/opdata.rs | 9002 | `67dc0293468fcdaf9051baee5ebfab7edb5eef78af4614e7898e73a09422bcb3` | 4 |
| crates/bitwarden-importers/src/importers/onepassword/access/replay.rs | 4873 | `75a0c91d5c5010767f0a19baf34064c5e5af8a8638f1dd0e73ae834f89b9aa86` | 0 |
| crates/bitwarden-importers/src/importers/onepassword/access/rest.rs | 15544 | `aaecd46cd17ea99c927e923608a82cdf9dfe7670bd7a3c9a0b9f0f3ccb8954cf` | 0 |
| crates/bitwarden-importers/src/importers/onepassword/access/rsa.rs | 4866 | `2ede253b33a47cbadb95443b3330ecc634ed5581ee2bd7b839752f60c96656b4` | 0 |
| crates/bitwarden-importers/src/importers/onepassword/access/session.rs | 386 | `34531b5424c248e19943c8a447966039065eb3d7985fe1fb2b1ead665d742d6e` | 0 |
| crates/bitwarden-importers/src/importers/onepassword/access/sign_in.rs | 5902 | `5c8811a73ec8320ef199a0c2d0e670783d4cfae5ff0a771ecd4197480ccb69c0` | 0 |
| crates/bitwarden-importers/src/importers/onepassword/access/srp.rs | 25187 | `ffea4b1abe928a15581fa6689036d13163647e979ba0d60864e0f1749d4df2da` | 1 |
| crates/bitwarden-importers/src/importers/onepassword/access/two_factor.rs | 7949 | `74bab6863ee9d5ac6fa4bd8d0cf7d19bcc027e1a678dffc50c245a6ae0cfee0f` | 0 |
| crates/bitwarden-importers/src/importers/onepassword/access/wire.rs | 9887 | `78a25f8fe9717855ca7e6389d25dd55d783ec3f6f6097097ab156b6678812e89` | 0 |
| crates/bitwarden-importers/src/importers/onepassword/convert/card.rs | 2076 | `f4e573723cbeb41afbc65cb344385668852113a4c9beda92a06406c36f4911ae` | 0 |
| crates/bitwarden-importers/src/importers/onepassword/convert/claimed.rs | 2583 | `89dc18fb3d935583d7b7a57cba0625fb12add1d7f7f00797b9130010d8d41167` | 0 |
| crates/bitwarden-importers/src/importers/onepassword/convert/credential.rs | 3286 | `720470143ecd160830237dffa8612bf627fd9a8eb4a8fcec420fc774374e3e73` | 0 |
| crates/bitwarden-importers/src/importers/onepassword/convert/field.rs | 5784 | `9c4b092a7dfbeb5f1c957421c5157ca9d61527bca5e197d4d2d3c33f8597806e` | 0 |
| crates/bitwarden-importers/src/importers/onepassword/convert/identity.rs | 2129 | `facd71d8c7ff6e25ac18ba863702ecba788a07425784abd4d6ec83ba0d9ae97c` | 0 |
| crates/bitwarden-importers/src/importers/onepassword/convert/login.rs | 2632 | `7254ac289b7decb42ca49d0b95bacac3c45c8c5e6e33a7ac00db325636d56d34` | 0 |
| crates/bitwarden-importers/src/importers/onepassword/convert/mod.rs | 6576 | `652b7a974839ea4a49ae4a1bc54b972e3c7863feadf3ea47e98ba3c7b0510086` | 0 |
| crates/bitwarden-importers/src/importers/onepassword/convert/ssh_key.rs | 1899 | `4bc97a9fda2726a4191af943ca54c704a70c1bc257e582c01c0b761d8083eed3` | 0 |
| crates/bitwarden-importers/src/importers/onepassword/convert/value.rs | 1991 | `9581e6a12e57bc285906038dc8b76389c00838f29a72568574515a76a0005029` | 0 |
| crates/bitwarden-importers/src/importers/onepassword/mod.rs | 2000 | `b67d22b137beb507e763fdb133995e201d41d6cf9c4101c95e0dd64cc5f5564a` | 0 |
| crates/bitwarden-importers/src/lib.rs | 4278 | `11cc6a8bd01253ef875d59c82bb5771a4fe777cca495537eaf769b862b84ca0d` | 0 |
| crates/bitwarden-importers/src/pipeline.rs | 24593 | `36457f301fbe2f8ece0977ad9936a028de8dbac15315cb2f001be0d815378f36` | 0 |
| crates/bitwarden-importers/src/uniffi_support.rs | 65 | `b866e5045c0bf91493e1c750b2ceba7744afa61f7171f70159c3034c743e7714` | 0 |
| crates/bitwarden-importers/src/wasm.rs | 2786 | `9fe1f715d22390bfb324fe1eb1423b6e2d69cba73f04ba4f111d5a176cad8890` | 0 |
| crates/bitwarden-ipc/Cargo.toml | 1590 | `19c5b4ffe98c9494bbde0c86a3ddf8bed960e3c59b93066f6ab1093df2209c26` | 0 |
| crates/bitwarden-ipc/src/constants.rs | 54 | `3cd28b0891526d9a36fd9532a5de38b6044111b3d4bf71e557394e9f243c0ce9` | 0 |
| crates/bitwarden-ipc/src/crypto_provider/mod.rs | 15 | `126f8d7ae1083befb08ca3021f77dcee91a1dd388a31a6009a6b6ca93c6dd481` | 0 |
| crates/bitwarden-ipc/src/crypto_provider/noise/crypto_provider.rs | 19704 | `92d1d0aff318d3978d716377ac507f3a9a6497aa80908771c6192cf7c82994ce` | 0 |
| crates/bitwarden-ipc/src/crypto_provider/noise/handshake.rs | 7415 | `684a639443e8a42b95c3cec0e1f439c13ea085abed0fafc20197d05928420df8` | 0 |
| crates/bitwarden-ipc/src/crypto_provider/noise/mod.rs | 3036 | `89303eb55984266b635acc78a15f8e8b3c3ed89be7ede841a4077291c663ff45` | 0 |
| crates/bitwarden-ipc/src/crypto_provider/noise/transport_state.rs | 12096 | `7ffd87aa6325be50cd0604948d136f5bbf19c4eb2bc0ef74b414de39e3c69940` | 0 |
| crates/bitwarden-ipc/src/discover/mod.rs | 1255 | `b5a49ebb0162d580a44ec770f215bb86ef7f7a18ae69c8309f39dfb0892ad83f` | 0 |
| crates/bitwarden-ipc/src/endpoint.rs | 5352 | `583de2f45297ec26262553fbcb5415bc02fe8afc8e73a3b78f427cb8f36ce4ef` | 0 |
| crates/bitwarden-ipc/src/error.rs | 5225 | `fbaee2b46bcbd3e2d5d50f3baebffdd0bf8523d380df499858c52eceed6196f2` | 0 |
| crates/bitwarden-ipc/src/ipc_client.rs | 58175 | `9e89cd3976f81919ab613fa0720fe2cf8d87930798bad31ea3cd916f043d2e93` | 0 |
| crates/bitwarden-ipc/src/ipc_client_ext.rs | 6221 | `c65ecb30190731ea340ffa68f1befb8810d452ef19b8314ce7c26c32dd4d1fb4` | 0 |
| crates/bitwarden-ipc/src/ipc_client_trait.rs | 2062 | `c9443953b2e49a4d4b44eb736ef1fc13a6426dd6b8a487f00e62371a86c25e6d` | 0 |
| crates/bitwarden-ipc/src/lib.rs | 1768 | `69b781e63d7ba5c35e5030cddcb31e3ca2953827af62954443e608f253eb13d7` | 0 |
| crates/bitwarden-ipc/src/message.rs | 4391 | `c43089604c8212c27f288439f161a061626362ecc1730be775145e7f56f912ea` | 0 |
| crates/bitwarden-ipc/src/rpc/error.rs | 773 | `f41c4e6ddea61dbcd34a72ebc13057473a019287a3b189743a681daf08a0ecdc` | 0 |
| crates/bitwarden-ipc/src/rpc/exec/error.rs | 248 | `8993ddee95ca4af7850959c47d29417e645aafd0b289ca140f4b9b5e75fd3bf7` | 0 |
| crates/bitwarden-ipc/src/rpc/exec/handler.rs | 3687 | `c3e9a284a75f91626e7e408a816231bca7a6dcf896c5a3d4311e499301e3060c` | 0 |
| crates/bitwarden-ipc/src/rpc/exec/handler_registry.rs | 4226 | `4fdb166a8668ef45d3ca135a3239660df27131a6996bfd1a53d7e4a6986384d9` | 0 |
| crates/bitwarden-ipc/src/rpc/exec/mod.rs | 43 | `50427b46988c75858b6a508d958d089160686dd26dab2388b5c49eeeab3ee02a` | 0 |
| crates/bitwarden-ipc/src/rpc/mod.rs | 147 | `e238bae4b7f3d5b10937e8cabcf47ea7e2c64ddbaedbb4279d7848f24943cfc5` | 0 |
| crates/bitwarden-ipc/src/rpc/request.rs | 389 | `b76af95bfc3d0e5547c8bda893ce767dc576c01fb642866dbf9469b8d2addcb9` | 0 |
| crates/bitwarden-ipc/src/rpc/request_message.rs | 2558 | `39801109ee0864ccf4d7f257159105ce674662261fe822243e1ae4c979fd6fe3` | 0 |
| crates/bitwarden-ipc/src/rpc/response_message.rs | 859 | `4e01e3a2173dcb7054eb2a81316b59e4f8ae59430a76e03a2eb7a5bcd365f446` | 0 |
| crates/bitwarden-ipc/src/serde_utils.rs | 643 | `866e9f69c1967acce61e66e44cd007b7fee259fb48ee3efff3bd185b5f542fef` | 0 |
| crates/bitwarden-ipc/src/traits/communication_backend.rs | 10374 | `ab88bab0c27c5d4c21da8c9da9e391ba942a060f1c6b94b74e84555064c6996a` | 0 |
| crates/bitwarden-ipc/src/traits/crypto_provider.rs | 3614 | `f8e887b23b156fc1e09a6ea2713b53ce21bfe40a205c20c75a823420682157a3` | 0 |
| crates/bitwarden-ipc/src/traits/mod.rs | 623 | `5f8c96df487df2aa083b7d719675ab3234f4989324fefebde0fd4241544af0a4` | 0 |
| crates/bitwarden-ipc/src/traits/session_repository.rs | 2298 | `f71599f54a79d42eaa67d7c9a4d38fb481e99df74fcd56d70442f787e0d76666` | 0 |
| crates/bitwarden-ipc/src/wasm/communication_backend.rs | 8456 | `7136a61b5a64f9626b578037b58e570856a881ff1dd1515e5c07158d87585b0a` | 0 |
| crates/bitwarden-ipc/src/wasm/discover.rs | 1122 | `87cdb0c1d6f354272cb6b291677f709d76484a32b89f1d3503f34e122db469cc` | 0 |
| crates/bitwarden-ipc/src/wasm/generic_session_repository.rs | 2800 | `dd6b3f8e77109a826a1c7ad40b422caf8c5262b845dcf8c93f0f026ca8c6e5f4` | 0 |
| crates/bitwarden-ipc/src/wasm/ipc_client.rs | 4546 | `0bbd5483e05a52f277656689048c0b2bedf79e588ebcd33cc46204ac6425c6ba` | 0 |
| crates/bitwarden-ipc/src/wasm/js_session_repository.rs | 3578 | `0934d1046fb78efd72a2a5f0045cd472b9497eb56f16037dbaa71edaa7b82c9e` | 0 |
| crates/bitwarden-ipc/src/wasm/message.rs | 1925 | `294c0742fa5dc889482b3b02113cdd252aaa4f84227fde09ef93a46d5e489c3a` | 0 |
| crates/bitwarden-ipc/src/wasm/mod.rs | 301 | `f7f18cc18d73d682cd29e232a7b30b0d5626e233ba34bc1bb041318be9e084d1` | 0 |
| crates/bitwarden-logging/Cargo.toml | 1041 | `459deb04073324c0b152541e6b6f09a095c0957bd9998e5267083002b2f1ac99` | 0 |
| crates/bitwarden-logging/src/circular_buffer.rs | 4919 | `63a9849fc7fcb1ca3c5c354b62f914ccf609a5677f405fc3622aa1e25c5007ce` | 0 |
| crates/bitwarden-logging/src/config.rs | 807 | `b2f0308d585dd0964f6800996482a344f62d4a66b22c4429ffaa8b7b6ee21f34` | 0 |
| crates/bitwarden-logging/src/event.rs | 2817 | `b0f6db2c72ba0d5b5a82e9233066e946b477cd85874c11cb583e4b3d5a572fed` | 0 |
| crates/bitwarden-logging/src/global.rs | 5134 | `cca04647b210d0e40abba7917aa90f8d87a3d04aadee8e46f4974353f11194f7` | 0 |
| crates/bitwarden-logging/src/layer.rs | 5795 | `0ee55712ccefe643a40a0a6538fffe0c660532037c5f6300e6f57a1fc963281b` | 0 |
| crates/bitwarden-logging/src/lib.rs | 497 | `f9c5b3f446fa14e23b323a880270baa277f751aa904a9eaa6f545d259c481c65` | 0 |
| crates/bitwarden-logging/src/visitor.rs | 3799 | `25e41ad32cf440aa3973eebf27a57626c8a3c246560974ce70a9b669656118d9` | 0 |
| crates/bitwarden-logging-macro/Cargo.toml | 559 | `3a4ddae882bee5cfcddfba2650c16884d0e6b343fc69cd92f6bbae43a54d02ba` | 0 |
| crates/bitwarden-logging-macro/src/lib.rs | 2312 | `d9cca57b4de697e44dfca63b3d17bd0e13e75ab7e019b341fea9b57d01fc466f` | 0 |
| crates/bitwarden-managed-settings/Cargo.toml | 1081 | `44995f00aea0ef4a091aa55af12095f379852b81f3fb791212d24617d475b0b4` | 0 |
| crates/bitwarden-managed-settings/src/lib.rs | 214 | `c6798cf6d040dba3d36b26497e3b7f7706fb490be1212c82b30cafb87cf899ed` | 0 |
| crates/bitwarden-managed-settings/src/managed_settings_client.rs | 7049 | `92c7ac189fb10abb7c6efce7d50991cafb94b88475af11aa6db98837dc0949f3` | 0 |
| crates/bitwarden-managed-settings-types/Cargo.toml | 1105 | `7562ca7ecfcd8de95c17d41d1f072dcf33c1e9ee9c589b870936ac9186d70dc3` | 0 |
| crates/bitwarden-managed-settings-types/src/lib.rs | 171 | `1433dcd33e235d8eb36b7bec59766faf9932601a52d0f0d9aa6229aa72c4d210` | 0 |
| crates/bitwarden-managed-settings-types/src/profile.rs | 5263 | `cbea477c99b4082a5bc4540b37f90022df2386910557ae2af5c39cb7c5035a6b` | 0 |
| crates/bitwarden-member-administration/Cargo.toml | 1067 | `20a1ebf0581eb3c8e636810bdbd3e10e8c0d1675039341705ffe6ce3582698f4` | 0 |
| crates/bitwarden-member-administration/src/lib.rs | 356 | `8b497ca1b6b7e6c8b9833e7e6aed6adfca0aded02f1074078e8239403aacb290` | 0 |
| crates/bitwarden-member-administration/src/organization_user_bulk_response.rs | 2292 | `2fc5fe57ca46b5ea42568f82becc0350e41b18d2c096b2ae5e204f1211969b80` | 0 |
| crates/bitwarden-member-administration/src/organization_users_management_client.rs | 4425 | `d35cf2410d8ffd31539bf98ec4ce0bcb3bf6f0b06c1aa8c03ef8652fa4f39d0e` | 0 |
| crates/bitwarden-organization-crypto/Cargo.toml | 1164 | `722bbf1d648b5f478626604357ceb1ee7f5d1823277a1f0710a678863d64d9ab` | 0 |
| crates/bitwarden-organization-crypto/src/invite.rs | 39601 | `c003bc8ecad6d2c56ba6a9aa987ffa9e70575eb91da8036e3751c507c4f3e527` | 0 |
| crates/bitwarden-organization-crypto/src/lib.rs | 96 | `fecd43be4f9d43b48ef2af3fb2bc381482886bbbb2fade99d8d67a0a2f0be996` | 0 |
| crates/bitwarden-organization-crypto/src/wasm.rs | 3136 | `232c7198ab744670bea90548b783875e5de258ac3a2e8bcde614e4c026404e60` | 0 |
| crates/bitwarden-organization-domains/Cargo.toml | 1152 | `30a487a3f0b79ddc6179307220b2b76e5d9ad0c32831fa8269d1e47e8b4aa72b` | 0 |
| crates/bitwarden-organization-domains/src/lib.rs | 203 | `263abb99bc44d895b2775e962b813fc58b4d9e220e4c3dc531b222a81bb1ae51` | 0 |
| crates/bitwarden-organization-domains/src/organization_domains_client.rs | 6109 | `e7886d418912caccfe7d30bba0ee1596ab3f7db44df1c82755d4752a0e882037` | 0 |
| crates/bitwarden-organization-invite-link/Cargo.toml | 1636 | `606873ae99ebfe3c06f44ea867cc5fc9892801ce8c7de5dfca3d7f1bb5a6dbf9` | 0 |
| crates/bitwarden-organization-invite-link/src/error.rs | 13026 | `3d96750f2279aea5bd9b97b5c40cf3fcb4dc54c2194731f1696d727c7ee6f5e7` | 0 |
| crates/bitwarden-organization-invite-link/src/invite_link_admin_client.rs | 34101 | `bc646e8fa67bd1519cd610c329d311eb0ebacc9e028cd62d1f8c2c84ec0a323a` | 0 |
| crates/bitwarden-organization-invite-link/src/invite_link_client.rs | 8997 | `c7832f68ae10c56893b5116be12c33eeb8cbd2491e4ba3508c44738e4d9695f6` | 0 |
| crates/bitwarden-organization-invite-link/src/invite_link_user_client.rs | 25375 | `5b667a838059f0f48bfcc282cf538afa6ff6846ef0f129d06708f21f72d94857` | 0 |
| crates/bitwarden-organization-invite-link/src/lib.rs | 590 | `32d6037df4e0df3c5a97b4a5c24fe69a6c0c50807343df7bbc91039b9b96565a` | 0 |
| crates/bitwarden-organization-invite-link/src/organization_invite_link.rs | 6181 | `d683b438d3c4902afa7d2b304b735c6b06dead5775d05d6400c54a51b0c51e76` | 0 |
| crates/bitwarden-organization-invite-link/src/validation_problem.rs | 5398 | `002f43b11801cd60c99d0def7587bf16dbdde8389e07d2e13ce377ee40da8d93` | 0 |
| crates/bitwarden-organizations/Cargo.toml | 1200 | `741b56172e48bbe450bb378df250d9596a2d420ccb868674e241af1f85373646` | 0 |
| crates/bitwarden-organizations/src/lib.rs | 647 | `9bd0f3e09c5400345c98232b7d4a6f7f1a2814b2c054c94647aa39bb83c454fa` | 0 |
| crates/bitwarden-organizations/src/organizations_client.rs | 3790 | `d4b1b34a1f3722fa2398528410cacd8cef73da8c5aee9cae2d092edcca5def2c` | 0 |
| crates/bitwarden-organizations/src/profile.rs | 19202 | `5cd3e835e07d1cd8eded8183dd8be2c8dbd444d37752b1119b86c8dce3c4e6a0` | 0 |
| crates/bitwarden-organizations/src/types.rs | 4546 | `d8e9194a6b6fd8d5d11d6ab95e5f2cbb611333a9f9f34f8da905342bec02c7c9` | 0 |
| crates/bitwarden-organizations/src/uniffi_support.rs | 164 | `37ea90629d3729662641c313485015440e657bfa3f09b439b9397e8704dab908` | 0 |
| crates/bitwarden-pm/Cargo.toml | 3734 | `92c705c99ad7bd412825b9c27a2e1ad026b2befbc1333a149b6422d1811f7f3f` | 0 |
| crates/bitwarden-pm/src/builder.rs | 3664 | `210ae49fc654a5129efcb976aad7eb6f74926a8a22e0bee762a9b0050a342af1` | 0 |
| crates/bitwarden-pm/src/commercial.rs | 722 | `64770b9bca2ae1e5ef9389c6a627866a72236d20b62fc5c5d80e450e46848b13` | 0 |
| crates/bitwarden-pm/src/debug.rs | 1647 | `1f973cd41e50c61484e1add544c5242593d49565520917dad13debc7ba616eb9` | 0 |
| crates/bitwarden-pm/src/lib.rs | 11948 | `f9a812b5dc9ecb0d770e9b743c11b8a720a1167fa441a3d749769557a5a1041e` | 0 |
| crates/bitwarden-pm/src/migrations.rs | 2357 | `82ca20ce84ba363b6603bb2ec7f9a6f8c1547cf5531dd921b277ddebc8eda84c` | 0 |
| crates/bitwarden-policies/Cargo.toml | 1605 | `2103b4b3b5d6debd9eca214992d79a8a4e9a97c4aed351c1a70a83e8e24d54a2` | 0 |
| crates/bitwarden-policies/src/lib.rs | 1090 | `1db041ba714e70919df75c529ad73f14acff00cfa4e0feed24dc95cb02ac4384` | 0 |
| crates/bitwarden-policies/src/models.rs | 7725 | `44e376fd12586966987e26215f61447172856aa269888554494c351da0d429ff` | 0 |
| crates/bitwarden-policies/src/policies/activate_autofill.rs | 409 | `fb2eb488c30302679853f150a884c303d5ef4898695e1bfbba4b1493af7c9932` | 0 |
| crates/bitwarden-policies/src/policies/automatic_app_log_in.rs | 1739 | `232cf136ef5f0662e215dd8c6affb1a49a30a4b4024860588e5b42a5dd3abdf0` | 0 |
| crates/bitwarden-policies/src/policies/automatic_user_confirmation.rs | 582 | `6615fa70868d39dd2f97ebdf0cc27255ba1dabc1aabec0d4a80c0e20a8ce1b52` | 0 |
| crates/bitwarden-policies/src/policies/autotype_default_setting.rs | 440 | `acebf17a9d9049bd1f8db9fd76f271e06f4599821068a84b42233ab49a287936` | 0 |
| crates/bitwarden-policies/src/policies/block_claimed_domain_account_creation.rs | 497 | `51e1862a59748b69b8b73cceb2453538969a5621be5e508c179e8427ec71772d` | 0 |
| crates/bitwarden-policies/src/policies/disable_personal_vault_export.rs | 461 | `7ab18fe2747469a41bf9912940f3603425e8d09d3d707d75d5fc339c992d0a46` | 0 |
| crates/bitwarden-policies/src/policies/disable_send.rs | 384 | `60fc625a3118056154f30ad6317332c535f24682979675454f123616fafa63b9` | 0 |
| crates/bitwarden-policies/src/policies/fill_assist.rs | 1808 | `2e72388c2ea7d36aeb71a5c052f0820f7a95d832e1f157071b50bbbedf2e0786` | 0 |
| crates/bitwarden-policies/src/policies/free_families_sponsorship.rs | 572 | `a45c872ea2648d1447b0fff09bd909f221959a050c71b178178e2f6cba1d9a49` | 0 |
| crates/bitwarden-policies/src/policies/master_password.rs | 6543 | `aa63665365a7b4dda675f8e4123b87b4f9b71dcd24dc003ae0c2e7c00d39121d` | 0 |
| crates/bitwarden-policies/src/policies/maximum_vault_timeout.rs | 3630 | `e96bb6d74190807d710a8a08ec77000fb02c06d407d19097dcb00152b0a05498` | 0 |
| crates/bitwarden-policies/src/policies/mod.rs | 1763 | `6def6ed0887de2d5e230a2797ba98d2dd07691d693cbb4a983b5ed9c548080be` | 0 |
| crates/bitwarden-policies/src/policies/organization_data_ownership.rs | 1886 | `e61b61ce1449fa3b259236396dd7b4dc9b28a9038fa0d9db2828fc07b8445839` | 0 |
| crates/bitwarden-policies/src/policies/organization_user_notification.rs | 2524 | `a7d4615db7d2c626db762c0a5bbab2db9973e2b276230853e8bdf0d3bb2cd3fb` | 0 |
| crates/bitwarden-policies/src/policies/password_generator.rs | 4372 | `f48691b72ef4ab11232663ed9e03f9ebd552a7db7b872923f07dd37cc7fcf45b` | 0 |
| crates/bitwarden-policies/src/policies/remove_unlock_with_pin.rs | 553 | `91b6b5a40909f2d9cc864aef90c3ba90059121a1cf8d229b2e550b4abb9cee2b` | 0 |
| crates/bitwarden-policies/src/policies/require_sso.rs | 390 | `88c62f3363c537908dfc6721d9a5680ef4170cc4ff36312f717b0cc2067ff4ee` | 0 |
| crates/bitwarden-policies/src/policies/reset_password.rs | 1852 | `4bbd14f74b4ef8c88ec705fc989c0bed94c3b104fc6528c6042f219615d5bd2e` | 0 |
| crates/bitwarden-policies/src/policies/restricted_item_types.rs | 552 | `45372f97b7e9e875f257a68d6d0ae208d1eb4a97018f3928e8f2dc24d7d26d2d` | 0 |
| crates/bitwarden-policies/src/policies/send_controls.rs | 389 | `49471127b38c381ddfb98bf460ec47a9816e0efb413f647b0225a6fee336ce04` | 0 |
| crates/bitwarden-policies/src/policies/send_options.rs | 1536 | `9c863eec8c69e794df0bb34877f8988bb88461c77ac6c2d9fb0a01f593d1fded` | 0 |
| crates/bitwarden-policies/src/policies/single_org.rs | 383 | `d82765b3e171e515e17d61305f16a6d7c170cd221777acfe4587d430b910fe90` | 0 |
| crates/bitwarden-policies/src/policies/two_factor_authentication.rs | 445 | `d19327dde97e6e78780046d2971ce6b42063715f63bcc8452bd0211bb6579060` | 0 |
| crates/bitwarden-policies/src/policies/uri_match_defaults.rs | 410 | `5cc5dd48c51f3a2befb8d0f6c7ff29b264e278e0ac204f4cb186cddea6db9fb4` | 0 |
| crates/bitwarden-policies/src/policy.rs | 4267 | `0cf850d7e586124525c3876ef3161d454a53867b07f4d28bc1365ebcae2ae26e` | 0 |
| crates/bitwarden-policies/src/policy_client.rs | 23851 | `226c7781256625ffb5dfddb64014ffa813921b31a2282cba37948451c146bee4` | 0 |
| crates/bitwarden-policies/src/policy_definition.rs | 22915 | `859218826a43181c10ed33a6a0ea45e1358d0c08b2e918f61fb251de3785c7e5` | 0 |
| crates/bitwarden-policies/src/policy_sync_handler.rs | 5839 | `0936aa2e7c63015e9d00ac4d1b7e5c493da9ec607a91032792177ee90e41ad26` | 0 |
| crates/bitwarden-policies/src/policy_type.rs | 9789 | `02b5155b7dabffe73336e5d8045eda13854307fa3c9f55831af27328e13e4e87` | 0 |
| crates/bitwarden-policies/src/uniffi_support.rs | 164 | `37ea90629d3729662641c313485015440e657bfa3f09b439b9397e8704dab908` | 0 |
| crates/bitwarden-random/Cargo.toml | 1850 | `ca5c2ab8ff868593c655f59e30a0052aa8570ad092c78bbec92df7ee55a55d5c` | 0 |
| crates/bitwarden-random/src/ffi.rs | 5275 | `ff778896f7b49d6256cb5e67b41c16b8c937ffd925db39cba8e397fce206fcaf` | 0 |
| crates/bitwarden-random/src/lib.rs | 3522 | `63826c46bf52886eafe07152faddab10b37c3762645fe03fe9b9037b125adbf9` | 0 |
| crates/bitwarden-random/src/seeded.rs | 3223 | `9963717e67327b2e313ca6ab7039376d0559cc3acad15c84aae0000fce0e4705` | 0 |
| crates/bitwarden-random/src/snow_resolver.rs | 1105 | `aa7488bc6d62953355960298c906da763a0a273fce00e8117cae755bb95e67a0` | 0 |
| crates/bitwarden-send/Cargo.toml | 2020 | `1f1517762e82ec7a8a6eeeeb2181d12ca128fd330f42f22964706508c79a0496` | 0 |
| crates/bitwarden-send/src/access.rs | 45972 | `cdf44d40abb50d36f0b699e139d91786d69c3fe67500e64944f2a5e4d6515f11` | 0 |
| crates/bitwarden-send/src/create.rs | 11124 | `d46762fee466a129a7f3d8a4883c8dd0dd120ac87fe11abcf446b7fcf1b31c0c` | 0 |
| crates/bitwarden-send/src/create_file_send.rs | 36070 | `f2127ee903a5d7d13f12e643370a805e3a69056f469e30a3c7fb1aa157a8c0a3` | 0 |
| crates/bitwarden-send/src/delete.rs | 18766 | `662f24571f2158dda58796862599a38e188a997c52d6ca8b6ee581d7cc458843` | 0 |
| crates/bitwarden-send/src/edit.rs | 30588 | `39d4a11bdd37675fd6046b1b4f970fcc44ca1be6dd4d92b8200249bf18429287` | 0 |
| crates/bitwarden-send/src/error.rs | 732 | `05eca8a3ff13312c965b2a826f117891239afb1bbd9148607267cec238bb8c1e` | 0 |
| crates/bitwarden-send/src/fetch.rs | 7824 | `a644f84e7674d1e7017ad1567c6ceebcdc65dba8643744f531e1be633e22a7dc` | 0 |
| crates/bitwarden-send/src/get_list.rs | 9030 | `4d86ded9232965209dd488630596121e316eebab77d306b90f4cdee8ae9bdab9` | 0 |
| crates/bitwarden-send/src/lib.rs | 1528 | `d384715c24bce9d630beedcba8a4cfdef8ecae95dd0a7f20cb8651b819d0ee28` | 0 |
| crates/bitwarden-send/src/receive_client.rs | 16009 | `09073047250da0ca310592abce891e7bfcbb8081dc8790b92206fdc7e20a0ada` | 0 |
| crates/bitwarden-send/src/remove_password.rs | 7073 | `1c880ad74abd5c2e83004075c7c3acc68abe785f2a0f9a91e9b11f3a06fb93d8` | 0 |
| crates/bitwarden-send/src/rotate.rs | 4089 | `0cf33811227ebdf0f938d417eb0ce3e0ea16ca39c1140c6093b25e05c9157ee8` | 0 |
| crates/bitwarden-send/src/send.rs | 60314 | `7453e319315b79ee9260c4b7ae64e2494692ca215df60a681e871f438e469f1b` | 1 |
| crates/bitwarden-send/src/send_client.rs | 4922 | `2cd51909342612c2af1baf31ef5d0ef1e75324b1d5a6b1a77fea89f6cdcb57fa` | 0 |
| crates/bitwarden-send/src/send_sync_handler.rs | 8863 | `8b301e8fb8403a00c4cf9a260aa967186730bf8ed436721d28e23daf9276d6ae` | 0 |
| crates/bitwarden-send/src/uniffi_support.rs | 164 | `37ea90629d3729662641c313485015440e657bfa3f09b439b9397e8704dab908` | 0 |
| crates/bitwarden-sensitive-value/Cargo.toml | 880 | `603e932462b5adca7a073f69e63643267084b090ec4cc3a844e87c7e065696bc` | 0 |
| crates/bitwarden-sensitive-value/src/lib.rs | 319 | `f3283a4150b1d901665835d33f3f414cd0f293a8fd5dc09cbbb4771aef7d646e` | 0 |
| crates/bitwarden-sensitive-value/src/sensitive.rs | 5001 | `bb28f9b2eee123d62ae756459b86509c22ef7ef48b8b722f1357f65dcd8ebe51` | 0 |
| crates/bitwarden-sensitive-value/src/sensitive_slice.rs | 2266 | `c4f885a1e4c98e249a9a7ed591a1a4363df1a806a742d273a3220b8f82f25529` | 0 |
| crates/bitwarden-sensitive-value/src/sensitive_string.rs | 6784 | `2a2e968872f85960dc457b58a8d9fe11e524c7b9a43dd554da3f2e3aac800ab2` | 0 |
| crates/bitwarden-sensitive-value/src/types.rs | 714 | `080101739ed8838790cd0dbc559c0606d71b0f3fb14f3a41c5accbfa301827c1` | 0 |
| crates/bitwarden-server-communication-config/Cargo.toml | 1431 | `4e02802e389efb49294c21ce02fb7078a82ef7758098b17d4a2e71dab36e1f63` | 0 |
| crates/bitwarden-server-communication-config/src/client.rs | 54884 | `e6ba5320c15a63db56fd9c8257d759784a1b32b7c136af43ac12f0bf02e9091f` | 0 |
| crates/bitwarden-server-communication-config/src/config.rs | 12064 | `981b3aeaad68afcd5a3d1fec70f4748df84da09dccd47974f0e1dc6231248d31` | 0 |
| crates/bitwarden-server-communication-config/src/cookie_provider.rs | 6523 | `3f644ba7cb9a7e2f3a1c4dc6507d3a7e065e44e94f10b9feec38430dace2b6cc` | 0 |
| crates/bitwarden-server-communication-config/src/lib.rs | 1078 | `6953a6ce76ae12459ef16f1d472cdc1653dd744b89505a6ca42866a9a2e6c86e` | 0 |
| crates/bitwarden-server-communication-config/src/middleware.rs | 10866 | `096ebace3e2477e9379f1b16b6a35dd139588980d418f14b5f0f2d4e485227b7` | 0 |
| crates/bitwarden-server-communication-config/src/platform_api.rs | 3149 | `95aec2664277ea786800ebf814f45b660095a5088defd6c745eaeb065283f059` | 0 |
| crates/bitwarden-server-communication-config/src/repository.rs | 7466 | `25024efbf2c6b879126c66fcc4dd1351b970f0b2a0915f45f4b5c326c027fd61` | 0 |
| crates/bitwarden-server-communication-config/src/wasm/client.rs | 6703 | `818ef33c5d72fd92ca968ec8f8d413c014f81d09947c21883c8ddc835fd3485c` | 0 |
| crates/bitwarden-server-communication-config/src/wasm/js_platform_api.rs | 3411 | `9ce994573868eed217562a1ebcddaca590a9d97a297218cc63a382cc3bebada4` | 0 |
| crates/bitwarden-server-communication-config/src/wasm/js_repository.rs | 3951 | `ddeb9ef2b835c41182f3f92a814972e2344e6920f72a56243a6e8dee453a409d` | 0 |
| crates/bitwarden-server-communication-config/src/wasm/mod.rs | 183 | `61cd18228af76cd7ba8dbeb4c3955a2d62865e07792b1292876f58da30132d1c` | 0 |
| crates/bitwarden-shared-unlock/Cargo.toml | 1995 | `69c14456e654c9a26abd9f58ca7c506de3f73f858db1b164c86820ba4d4c1c40` | 0 |
| crates/bitwarden-shared-unlock/src/active_peers.rs | 3363 | `4a5fc2f989aa029e65d19fad95d1ad3971af55d62e27d760045ba10f1bf0bd4e` | 0 |
| crates/bitwarden-shared-unlock/src/drivers.rs | 2404 | `359a56e356e8fcd83a245b81ddeee2b443cf3d42ed3848700c0e827b82739577` | 0 |
| crates/bitwarden-shared-unlock/src/lib.rs | 10373 | `ef57112c41061c1b58ca2d14b0bb59f747cc8904770857fd3bbccb1bb3e690da` | 0 |
| crates/bitwarden-shared-unlock/src/message.rs | 4298 | `ea2049a488a39206481f6f07d4d11587e4576d9a53b3d98b9d3dfa3ee8e0b24b` | 0 |
| crates/bitwarden-shared-unlock/src/peer.rs | 22039 | `d810f2c1efb7ad957472b3396b1a999617a38cd350f3702c966585155bf3fc4a` | 0 |
| crates/bitwarden-shared-unlock/src/timing.rs | 1258 | `643c7a380bae749a7d563abf53961c5aa4dd0e2db3eefad34d6009a91cbfdbd5` | 0 |
| crates/bitwarden-shared-unlock/src/wasm/biometrics.rs | 11581 | `42bdd9d95423df8331e738c7362e88c75cd1e0bb55f86eb25e2fab42ed86c876` | 0 |
| crates/bitwarden-shared-unlock/src/wasm/drivers.rs | 8593 | `a994f85179457ec6affa1954614198c184469869114e7cfe11ad1b2307cce7bd` | 0 |
| crates/bitwarden-shared-unlock/src/wasm/mod.rs | 114 | `7911a7197948c66077358e4bf9a9c41cf8799e9e19b3b333bddb7bca6212545a` | 0 |
| crates/bitwarden-shared-unlock/src/wasm/peer.rs | 1743 | `f4c1445a52045e41c0f23e77133680502ac1ea614322cb5f6a68a198d358e37b` | 0 |
| crates/bitwarden-ssh/Cargo.toml | 1685 | `e02c67172e53373e4b2eb4c51507133e19414d4489859ca835d1a064c0c05723` | 0 |
| crates/bitwarden-ssh/src/error.rs | 804 | `8a58ef2ef394307a752346444ab7a4091dac252d6112484e258e7d8abfcc9c02` | 0 |
| crates/bitwarden-ssh/src/export.rs | 6703 | `a8bba069ef561e8ef6653f90fdf10698245e08e91ff0d71ec904098b97d14f1c` | 0 |
| crates/bitwarden-ssh/src/generator.rs | 5223 | `bf74a5389fea4973e1187c74bfd59ccc715ddfbf60fd63e8fbf1b3bfe8ccb0f9` | 0 |
| crates/bitwarden-ssh/src/import.rs | 17480 | `da110e2c92bbded49d34542cb234efe9ff822f92a0d6ecaef2a1db272d0eff30` | 0 |
| crates/bitwarden-ssh/src/lib.rs | 1182 | `3cf3e6ed630fc332698b352da278dc2dace3d1e122cb44ceeae2a515432b5b81` | 0 |
| crates/bitwarden-state/Cargo.toml | 1770 | `dc68532b3bae9b46be860129c0fc038061472e8dc635bfa9c2a793cf36dcac31` | 0 |
| crates/bitwarden-state/src/any_map.rs | 2454 | `8930d52088364a80e0fe0fccb6ae70815619c0c10b40e48cc8c427826555a38b` | 0 |
| crates/bitwarden-state/src/debug.rs | 11756 | `93b5b4b9670f1393c464cce39970c19e8cedd59be4841e192474581311964c41` | 0 |
| crates/bitwarden-state/src/lib.rs | 848 | `f049c4f3a9f2ed02fcdeef2c4c80ec1e5de215a94b81db68379da7bc5ba6692b` | 0 |
| crates/bitwarden-state/src/persist.rs | 497 | `2036e5e98cec1b7f4fcd51aac929822303f4e209bfdc4979b258763e113e01f6` | 0 |
| crates/bitwarden-state/src/registry.rs | 15096 | `b2f3b17113519b3ed0e7820f4ae2bf70395d749b5dbf7fd06cab95bf1731257a` | 0 |
| crates/bitwarden-state/src/repository.rs | 8961 | `a03e4ec546e50504b5d766dd9ed702a3588506f95fa7dd1264a13c4494d71fee` | 0 |
| crates/bitwarden-state/src/sdk_managed/configuration.rs | 848 | `179e304c9ece02aa637d277bc66a4ff1b9c509ba53ced24fa3b6ce3b6306134c` | 0 |
| crates/bitwarden-state/src/sdk_managed/indexed_db.rs | 7100 | `6e011ad2f13e429993ef6584e0487201ad1d1406cceab4c3947d81312861d499` | 0 |
| crates/bitwarden-state/src/sdk_managed/memory.rs | 10428 | `ea2ad18fb9a6b70f0d0b4f2b7e47997f550c621bca8be673d1c8131672c84af3` | 0 |
| crates/bitwarden-state/src/sdk_managed/mod.rs | 10312 | `668f3000f3b94eb000ebd1779732e295c78461998e3e1dec966a17c538235663` | 0 |
| crates/bitwarden-state/src/sdk_managed/sqlite.rs | 18392 | `61f5726638d1c9b7bb6f19197401119df3b04671e0db3a06ff737988bbf22ce6` | 0 |
| crates/bitwarden-state/src/settings/key.rs | 1925 | `2902ad98191c4c4e2eb03b28027f1bbe5f9269cee6ec122b1edfda790933d54c` | 0 |
| crates/bitwarden-state/src/settings/mod.rs | 1333 | `8fe95b7ad9ced0349e21461d7118c6ac8db26db127d9a5554622aa4f05f3d98a` | 0 |
| crates/bitwarden-state/src/settings/setting.rs | 3246 | `b8ef68f3b04c360eba40628df5eecd114ec9c400ca4e8c8531ccb0a780ee6927` | 0 |
| crates/bitwarden-state-bridge-macro/Cargo.toml | 543 | `195f41984c083b9803fc43233215fe1475ebf3c8d1db504c7918a7e71d7be999` | 0 |
| crates/bitwarden-state-bridge-macro/src/lib.rs | 14114 | `34b8bed944b04796f67c5e651e406c3bc169e0bc1425492d65d1ebb9f8666f3b` | 0 |
| crates/bitwarden-sync/Cargo.toml | 1078 | `3e86caa17916e691d589a7c3e97e60f41a3a88e3c78683cdb4635d570ed0cb7c` | 0 |
| crates/bitwarden-sync/src/handler.rs | 2565 | `f2691449fb48491c9714f1372aa23bd13a0643e2d6f66ccf5d7aae78fefb431c` | 0 |
| crates/bitwarden-sync/src/lib.rs | 238 | `a72b4b0c369856691ea5a2eddcb72fcbdc9be1e01994d476c0aba78e1ecfaf3e` | 0 |
| crates/bitwarden-sync/src/registry.rs | 3144 | `6363c86605898405fb66af44cbef3da8f7aa4e425bc32104cb91b2b0f46ad1b7` | 0 |
| crates/bitwarden-sync/src/state.rs | 291 | `081b1cc4002031cef590c3ea8a6864074a47db0a67f67762f3894a7b4338370f` | 0 |
| crates/bitwarden-sync/src/sync_client.rs | 22258 | `2d53f56af0dfbebdb3d16c2da460b685b0bd44c1de233610e4e4b4924865c49a` | 0 |
| crates/bitwarden-test-macro/Cargo.toml | 556 | `9e2b370d936be51ce8be4f9d501fb175c7f5b02f7b915dd4ed773d71555dd4c7` | 0 |
| crates/bitwarden-test-macro/src/lib.rs | 2462 | `e64cc6f4344761f9afbbb23403448f90ccb1c5c805d626f8bd547a2113fcd65a` | 0 |
| crates/bitwarden-threading/Cargo.toml | 1418 | `a7f965edc4d5e3df37dd9a7a1f586296d947c87d1622b4bc825c71f25dded21f` | 0 |
| crates/bitwarden-threading/src/cancellation_token.rs | 2435 | `456586caf9c2e84a325de1784a85677dab665261ea7a1440ebe7a61eb653afda` | 0 |
| crates/bitwarden-threading/src/lib.rs | 861 | `4fcb882a028a72d13671569c327c480fc6069da60e3b9e4ef716ef001b6febe3` | 0 |
| crates/bitwarden-threading/src/thread_bound_runner.rs | 8479 | `20935c56eedb1b073f6c2f0e1b88a3cde620d2bc55681a8f05e5aca7b3531493` | 0 |
| crates/bitwarden-threading/src/time.rs | 2998 | `54c0149d8a21424bddd251180b568dc62d691c236afbfeeca519ea4ecb89490b` | 0 |
| crates/bitwarden-uniffi/Cargo.toml | 3168 | `bc06b6c12642591f7da81648e566c08c4d53c579a547dbc7a7f261a8ff5e4efe` | 0 |
| crates/bitwarden-uniffi/kotlin/app/build.gradle | 2565 | `0ef5bbeeb889ae70aca9cdc66da2786b85269190136a9f2a43e254954125238e` | 0 |
| crates/bitwarden-uniffi/kotlin/app/src/main/java/com/bitwarden/myapplication/Biometrics.kt | 5643 | `e55f84f7e8d4379c85d69500fc6470d2c5810dd6ce1a330824e15e3045fd7626` | 0 |
| crates/bitwarden-uniffi/kotlin/app/src/main/java/com/bitwarden/myapplication/MainActivity.kt | 19226 | `bb3d0ab195857676ff3ec85d0f935035817e31065fd4a39f3af947cd2f21c0f3` | 1 |
| crates/bitwarden-uniffi/kotlin/app/src/main/java/com/bitwarden/myapplication/ui/theme/Color.kt | 292 | `c70e2770f6e1f8508850123705281b79d8bb80cbe19c3694ce93efacb75898fd` | 0 |
| crates/bitwarden-uniffi/kotlin/app/src/main/java/com/bitwarden/myapplication/ui/theme/Theme.kt | 2203 | `30967651f1cb618782db81051fd1a72f59df7499114de46cd7649b872a498abd` | 0 |
| crates/bitwarden-uniffi/kotlin/app/src/main/java/com/bitwarden/myapplication/ui/theme/Type.kt | 997 | `f362724a62fde2a25b8d84011e80c7bee958f321af5256dd462e3ab1459a7e87` | 0 |
| crates/bitwarden-uniffi/kotlin/build.gradle | 448 | `e57080d90816f662501e92404ab56849813523059574f76b195fd0815d0fe4c5` | 0 |
| crates/bitwarden-uniffi/kotlin/sdk/build.gradle | 5357 | `6ad8644d8840008fc97625ac603948d6b877f4f20dbb3dbad017d1dc375560f3` | 0 |
| crates/bitwarden-uniffi/kotlin/settings.gradle | 347 | `d471d7fcb2164327c547c5423a80bc7e47a13e0e288d5664121bf178ab5c22b2` | 0 |
| crates/bitwarden-uniffi/src/android_support.rs | 4041 | `3207ddd10eb5ba3ad3435d0778597917ec82d4b4ea2107b32088562be571d4b8` | 0 |
| crates/bitwarden-uniffi/src/auth/login.rs | 1785 | `ecc4906d76c3c1b7c616ed415cd146f23fea19e7fd574e3c995b8cf3232952b4` | 0 |
| crates/bitwarden-uniffi/src/auth/mod.rs | 5790 | `9c50b9ee53e3b6a62b9555866d2675cbbd41aa0d5841da461003678512f85a62` | 0 |
| crates/bitwarden-uniffi/src/auth/registration.rs | 2579 | `96d152be627ea4874b7bd92ee10c1b231158a657dba16d385eadbdf1b2d58714` | 0 |
| crates/bitwarden-uniffi/src/crypto.rs | 5889 | `2f59be698cd00ffa71189c4523275887dc4cd2d1ecb494a97c13d661345eb570` | 0 |
| crates/bitwarden-uniffi/src/debug.rs | 1646 | `bded941d321d0be0c8bf63d336405dfa8fea4b135c393d56f17579b24751d245` | 0 |
| crates/bitwarden-uniffi/src/error.rs | 5326 | `5fb7f61a24c06ba30acbc5cab8b3e52afe0f026acbd2194d757a4204e6b864bb` | 0 |
| crates/bitwarden-uniffi/src/lib.rs | 13596 | `bbe5d123e98f0ac0c6f0adae279de3319aa1a4e5f202fa4c9711ba5875bc2a26` | 0 |
| crates/bitwarden-uniffi/src/log_callback.rs | 2791 | `e4f362666858caaebaae6aa7f39f0b1de27497c2779b3d750a617d65b9008db8` | 0 |
| crates/bitwarden-uniffi/src/managed_settings.rs | 1318 | `67f7ed27435153203801e6cb56f73e9fbf4cf1fd847dc2d0fef1bd7552f0fc82` | 0 |
| crates/bitwarden-uniffi/src/platform/fido2/device_auth_key.rs | 11894 | `1e16aee3be9b09d2cfea30da4aca1874722e93b62254678a28e43c4d1e01d463` | 0 |
| crates/bitwarden-uniffi/src/platform/fido2/mod.rs | 12755 | `c953239a5cb9ac5ae27f826ae61a1f98c59572a4bb3e484d2231adf85be0b2b6` | 0 |
| crates/bitwarden-uniffi/src/platform/mod.rs | 2408 | `1450b537def64b031690f05a8a622c2c5d68a58da2724c3c21ae21ecf80ca335` | 0 |
| crates/bitwarden-uniffi/src/platform/repository.rs | 6420 | `71fc1186d71221a0a267484198e19f300253a23ca500036731420ff62ec51e41` | 0 |
| crates/bitwarden-uniffi/src/platform/server_communication_config.rs | 5751 | `c25a2e5cf9b39e20ae5ad8d4a2851da23a69ba17827af810a2e918fb5d312e95` | 0 |
| crates/bitwarden-uniffi/src/policies.rs | 783 | `da595fc41d33750309e0bd8f36d95a776b9c953b4d304b779cf9495b21b41d77` | 0 |
| crates/bitwarden-uniffi/src/tools/mod.rs | 5698 | `f0e0b282aa25d9a32af222dc1c0543c6ae2d3a090dda97a2b1ff7d5f1c15d245` | 0 |
| crates/bitwarden-uniffi/src/tools/sends.rs | 1714 | `0a0889446add0c215f0024395ace9438a59b65dc8dc7db8067329c948c7b46f9` | 0 |
| crates/bitwarden-uniffi/src/tools/ssh.rs | 683 | `6aac33d6de095d7fce89553e8d500074c460708e94ef9c6c9f28c53a5d90f84c` | 0 |
| crates/bitwarden-uniffi/src/uniffi_support.rs | 511 | `aec3f77601f1e9c29b528b7dfac536ce309a049f811f7e019770bd4a6122cf4c` | 0 |
| crates/bitwarden-uniffi/src/vault/attachments.rs | 1724 | `43033f3868870c2a15aeb998982e63795609d333330ab4bb93a90286da26612c` | 0 |
| crates/bitwarden-uniffi/src/vault/ciphers.rs | 2057 | `de695bc80ea9e4c8dd91afdb8a89a3201b0758add7942f6ae27dda3f775ab4f9` | 0 |
| crates/bitwarden-uniffi/src/vault/collections.rs | 3455 | `dbf4f972acafbe06a46966def04354c3c3c2994259c6c7d65e2157b97549d58a` | 0 |
| crates/bitwarden-uniffi/src/vault/folders.rs | 733 | `d87c52fc423352be39167e0354278c5bf902786dafa5d14b030c906cf2565249` | 0 |
| crates/bitwarden-uniffi/src/vault/mod.rs | 1898 | `f0e8a86a66e1d68bd76c136dc0a6c865a933bd7fb9090c4ee4ab59207027455c` | 0 |
| crates/bitwarden-uniffi/src/vault/password_history.rs | 621 | `22735e2f38b385e1910f4f82d22037f885269c785235ce9453f43c9135333efc` | 0 |
| crates/bitwarden-uniffi/swift/Package.swift | 1323 | `958e904d5a776ff07513f741c4c9bb6ea5f0e9f76ad0d7eda4cf62075cbb63cc` | 0 |
| crates/bitwarden-uniffi/swift/Sources/BitwardenSdkSupport/NaiveDateFormatter.swift | 911 | `157610fe70ca53028be7cebd4f74292e4c64d28caf67b12ebf17d11013bed9ae` | 0 |
| crates/bitwarden-uniffi/swift/iOS/App/Biometrics.swift | 2845 | `cf24e5ca07866dfdcfcb25d69612d723b4f18a634d21d114f1ae3aaa5d64826f` | 0 |
| crates/bitwarden-uniffi/swift/iOS/App/ContentView.swift | 18211 | `d4a7f76a422d003c0989a9a381a605a738c0ef1460021b53cdbd3fe95af239ca` | 1 |
| crates/bitwarden-uniffi/swift/iOS/App/testApp.swift | 210 | `e35356fab5d1743f6a322e3cd611b797ee1495ed104c2f11c235a44facc61921` | 0 |
| crates/bitwarden-uniffi-error/Cargo.toml | 458 | `2f2ab50d2692902f931369596b17bf9503babee1b057ec704a4cd929bd61498d` | 0 |
| crates/bitwarden-uniffi-error/src/lib.rs | 1601 | `624e01c9d72ba7a5fb3888a68e032cdeb6bf0f5be822a527bbc1116b7b97aa4a` | 0 |
| crates/bitwarden-unlock/Cargo.toml | 1323 | `74d0ae3d414d6e12dc0cbf4d1b39c7b4bfbac8d7da80843aeb6cec289aedeebd` | 0 |
| crates/bitwarden-unlock/src/lib.rs | 318 | `4e1f3c08704ba71de7971ac106d87656d0e355f5625a634bdaa95e7712f15b8b` | 0 |
| crates/bitwarden-unlock/src/session_key.rs | 3299 | `fa1eefc631abe0bfa656caf2671412f866b5292545b5118e8815e7eb7ccdbd95` | 0 |
| crates/bitwarden-unlock/src/unlock_client.rs | 18049 | `7066de62b8185b400f7f21ee891b78b72c351da13e9a296ca25934ed09acbf81` | 0 |
| crates/bitwarden-user-crypto-management/Cargo.toml | 2027 | `07c6dc40fddf6affbd4341125752dbfb3abc14a43988f1b3afcf303b5a4368bc` | 0 |
| crates/bitwarden-user-crypto-management/src/change_kdf.rs | 9085 | `818a157e21e14c3cbd5be56cd7d9b9cbb8550b5bd091b68f7ec5c28af65b709f` | 0 |
| crates/bitwarden-user-crypto-management/src/key_connector_migration.rs | 14000 | `10a6bdd81adeb9ed7b0698abb3671002dd36bb7a1dc755eb210bf43740f4cd63` | 0 |
| crates/bitwarden-user-crypto-management/src/key_id_backfill.rs | 10712 | `e9219406c78b6f11309d94fa16fc0f9503e04bab5283d785258c953e3315412b` | 0 |
| crates/bitwarden-user-crypto-management/src/key_rotation/crypto.rs | 15933 | `cd9b0c075024a55ee31ccd5017c506c44a2c33c6695b6c260a99b8e8db843412` | 0 |
| crates/bitwarden-user-crypto-management/src/key_rotation/data.rs | 27892 | `9ee2cbed03f9c4f424263a8be1cad5d008e49f652845b46c2e249d6527f8c402` | 0 |
| crates/bitwarden-user-crypto-management/src/key_rotation/mod.rs | 5061 | `f9adc0a636f27ea9c91eb214c238cb76c195598f26b9db0992b68e096212bb24` | 0 |
| crates/bitwarden-user-crypto-management/src/key_rotation/partial_rotateable_keyset.rs | 7352 | `d42020839bafc532277de7f487c0d924346d9fbb206243c38cdc84004a30675c` | 0 |
| crates/bitwarden-user-crypto-management/src/key_rotation/password_change_and_rotate_user_keys.rs | 14946 | `cdeea61471dbfc30ae0bbc9885ce2411647c705ade00152868f8a9c10f667195` | 8 |
| crates/bitwarden-user-crypto-management/src/key_rotation/rotate_user_keys.rs | 42145 | `a25dbaec9dace7b5df36cb34c875dc3d788dd32d113c61ea584fd4a3c9dc9fce` | 10 |
| crates/bitwarden-user-crypto-management/src/key_rotation/rotation_context.rs | 23220 | `0f76564bff8a4cf8efde44e2b0eeae3c49ff08b1203dcdb1f489cd9ccb260f32` | 0 |
| crates/bitwarden-user-crypto-management/src/key_rotation/sync.rs | 32692 | `53ca071708327dfffa09158b2d5b7614d78cf668e04a9a7450969755ec991a52` | 0 |
| crates/bitwarden-user-crypto-management/src/key_rotation/unlock.rs | 39110 | `27755e459a444c5b095c1aa0c5459588299448773282a03c43851545ab00dd55` | 3 |
| crates/bitwarden-user-crypto-management/src/key_rotation/unlock_method.rs | 13595 | `b570efbd37b95ed41e87ba8c0a4f12ba60fd33fe41dd008a8106042a95f4f4cd` | 2 |
| crates/bitwarden-user-crypto-management/src/lib.rs | 663 | `fbeac55dc17831a95f1cf63950c3605df0875a8a342bbb351aaeb8bbe1234283` | 0 |
| crates/bitwarden-user-crypto-management/src/pin_settings/mod.rs | 74 | `1373c219bae4849ddaef9886c049a32d4e48cacf7ac666200fb34704bda656d0` | 0 |
| crates/bitwarden-user-crypto-management/src/pin_settings/pin_settings_client.rs | 2804 | `ab75e53a3e930f8b3a3414566988c5ce2517ca921ac4a7e6338dd47caa34895f` | 0 |
| crates/bitwarden-user-crypto-management/src/public_key_encryption_key_pair_regeneration/mod.rs | 4823 | `3b3b005b7a1063b00e70a340e23881e0b56e3b59176c1b657b3a54f7630e3a0b` | 0 |
| crates/bitwarden-user-crypto-management/src/public_key_encryption_key_pair_regeneration/regenerate.rs | 11427 | `03920cb91279bedf559dd01b3e4f625759d9bc5a80b989bf7f25553d38fdd5c1` | 0 |
| crates/bitwarden-user-crypto-management/src/public_key_encryption_key_pair_regeneration/should_regenerate.rs | 32028 | `f9d5703205e0b28797e10f26ccf0f78e5dc92409cc933568f4b0fafcd9c9cf0c` | 0 |
| crates/bitwarden-user-crypto-management/src/user_crypto_management_client.rs | 984 | `b5325b4b0db9d5d68c0035dbfabd9bb2357732920f28dfb07650246264b991d3` | 0 |
| crates/bitwarden-user-crypto-management/src/v2_migration_permission.rs | 7473 | `834167f6b7029126ab4ddc5ab4b8b5be3ef9093177ae2940a94762fccd93f707` | 0 |
| crates/bitwarden-uuid/Cargo.toml | 651 | `92704d49adcaf04f5ee77f6a66e256bde294fa4259b92b0665f2f0bc5f276af5` | 0 |
| crates/bitwarden-uuid/src/lib.rs | 84 | `3527b88f621708640d95043723f25db7a13535528fcd03551ec3505eae1b6f76` | 0 |
| crates/bitwarden-uuid-macro/Cargo.toml | 500 | `63cb9881ab5efd5cd9e6435bb07ccfcae5e9f70d113b79986c4e2b6451717d60` | 0 |
| crates/bitwarden-uuid-macro/src/lib.rs | 2636 | `943ccd6e7984e9f21ba2b1d2b336b2a2209844b0b58b79f728c239664d494293` | 0 |
| crates/bitwarden-vault/Cargo.toml | 2610 | `18b3a5e61f59b50807a1048fc33313581ac56ea6214713a21f0de583a2eef9a9` | 0 |
| crates/bitwarden-vault/src/cipher/attachment.rs | 20507 | `184b7f52f8580bf9bf2fb21c5f4830282d3fab708c051fb59060b1360d99e430` | 0 |
| crates/bitwarden-vault/src/cipher/attachment_client/admin/delete.rs | 3449 | `0030ca5bc52a106c244bc15a99ad3b3112c06d269b821cd93ba1d7aef8117544` | 0 |
| crates/bitwarden-vault/src/cipher/attachment_client/admin/download_url.rs | 6135 | `955a5bb592caaf13cbfff732dd80eaf305dbb42d4d43fbbe24687b6fc52e3a98` | 0 |
| crates/bitwarden-vault/src/cipher/attachment_client/admin/mod.rs | 453 | `3763441340e94bc34fa762f2fb607b8ae03763cd1ccb9a1173973cf0632df405` | 0 |
| crates/bitwarden-vault/src/cipher/attachment_client/create.rs | 20620 | `d2360ee668b0c4a98815366c49362a833308281a9a83771e7996f997b2ff46d8` | 0 |
| crates/bitwarden-vault/src/cipher/attachment_client/delete.rs | 7229 | `eb0e4956ce71f371456287318ace22dc39fc3525992901bf5a276911b8f8640c` | 0 |
| crates/bitwarden-vault/src/cipher/attachment_client/download_url.rs | 17706 | `0cc49e79de4aa4b07f713013a8471c93a03dc1af7caca1472fd6d64e505e998a` | 0 |
| crates/bitwarden-vault/src/cipher/attachment_client/mod.rs | 3965 | `2853943804ac8968982f1561fd74d4f6e207ffee539091f1181a8c48bd5fe792` | 0 |
| crates/bitwarden-vault/src/cipher/attachment_client/renew.rs | 4565 | `8c550f1abc042ad04598ecc5a5f9ad08f74a624de820fa71da683c9e1b20046c` | 0 |
| crates/bitwarden-vault/src/cipher/attachment_client/upgrade.rs | 32654 | `b597d53ccd831a04ecaff21ef989fa46946b2982b85da3c7756f1f9353289f8b` | 0 |
| crates/bitwarden-vault/src/cipher/bank_account.rs | 17259 | `e9e6f98ca8cfd4f0f71ff0e3ff47f4ce10b1c584a7c5af2c45f372680e3c5ae7` | 0 |
| crates/bitwarden-vault/src/cipher/blob/conversions/bank_account.rs | 2123 | `be15e0d0aa20109449f24e04e3fd539207bb3b709864d83aaa0559562c97abe6` | 0 |
| crates/bitwarden-vault/src/cipher/blob/conversions/card.rs | 1484 | `44e008a5e04966ee94ad064ee54a40b1cdfe46d7be4e881c89a6d1f72539e1cb` | 0 |
| crates/bitwarden-vault/src/cipher/blob/conversions/drivers_license.rs | 3452 | `1acffba7bd6856ae6f5f124765dbf97c7889cd971374fc883046b598f2d1e73e` | 0 |
| crates/bitwarden-vault/src/cipher/blob/conversions/identity.rs | 2423 | `e1a31811103c1932bb91f3f68ea54b274d35977a900f5cc73dcbba06c5cfb0ec` | 0 |
| crates/bitwarden-vault/src/cipher/blob/conversions/login.rs | 11320 | `200db5adfc32066f45abcef5f40e04be77428009e364893aff985a4480eebee7` | 1 |
| crates/bitwarden-vault/src/cipher/blob/conversions/mod.rs | 13321 | `eb985e3e8406b39b2c7ee0d0899a98d65d320d0de6f2bfd1b4f28119ab43e377` | 0 |
| crates/bitwarden-vault/src/cipher/blob/conversions/passport.rs | 3712 | `c52be25bd78a6f8eb35f0c2bbaa2f7d9e4c523700a0d4f2a47aace7ff050c577` | 0 |
| crates/bitwarden-vault/src/cipher/blob/conversions/secure_note.rs | 2322 | `ab738ba9410af2d363d94000cf444856c7cfd28c549d924c8ae0a638a5fbfabb` | 1 |
| crates/bitwarden-vault/src/cipher/blob/conversions/ssh_key.rs | 693 | `c1747ca82ea200fb072fd76ba5ee740f3d4b7deff7664a0ca8b5654f79f68312` | 1 |
| crates/bitwarden-vault/src/cipher/blob/encryption.rs | 27423 | `80538b17850e9d9068eae53ca933832d4f8891f6c3d42ae650afbb2326f88f5c` | 1 |
| crates/bitwarden-vault/src/cipher/blob/mod.rs | 1936 | `1b1563aa90a15611493b83c113789a780afda54ff7559f2f85a79ff95a988891` | 0 |
| crates/bitwarden-vault/src/cipher/blob/sealed.rs | 8516 | `a7bde33c0e112b40c4f331c46896d9ac6305c1b1fc8f8f5a0f070bb5338af0cf` | 0 |
| crates/bitwarden-vault/src/cipher/blob/v1.rs | 25317 | `2a93e693ad642fd21afb590ab2054c41e873f152543be5b27e37dbc06d154d89` | 2 |
| crates/bitwarden-vault/src/cipher/card.rs | 10689 | `246ff8f4ffadc8d3d3c0cef3e4db04c76bfc0f5951700f7afb1ff08d7161bbb9` | 0 |
| crates/bitwarden-vault/src/cipher/cipher.rs | 176387 | `70d0a3fe6af95978b97ceea966ab500e46130e586bd7fd17d81c05863c60680c` | 1 |
| crates/bitwarden-vault/src/cipher/cipher_client/admin/create.rs | 8581 | `19495ff543cd38c8e823aa3efb107e0b433fb32ad0d01a49d0365578211de880` | 0 |
| crates/bitwarden-vault/src/cipher/cipher_client/admin/delete.rs | 6994 | `b49c798124f8a9514ded377a951a11f553e3daba5cabc8ff1adc94cf36ad852e` | 0 |
| crates/bitwarden-vault/src/cipher/cipher_client/admin/edit.rs | 16426 | `2aab29fea9ef3310fd68329e397e3a436d0abcc7964227bb222fd0be54da4f29` | 0 |
| crates/bitwarden-vault/src/cipher/cipher_client/admin/get.rs | 19521 | `d89e16bdeb2f0d5c68717abd4e5fdad104304249b0948076defdb52aa1eafcb7` | 0 |
| crates/bitwarden-vault/src/cipher/cipher_client/admin/mod.rs | 1264 | `463e05d3e0aa6da56e06789b89d55b617ba6cd9405c437bc0273180b4ccb6771` | 0 |
| crates/bitwarden-vault/src/cipher/cipher_client/admin/restore.rs | 11602 | `3461cf4e9f00d3cc66b2831a495c75e3d56d28f9528501019fe202707229d682` | 0 |
| crates/bitwarden-vault/src/cipher/cipher_client/bulk_update_collections.rs | 9213 | `c4adac2c4e8f8444faf9c49183c3152a57fff41d89d0543affad0221481d07f9` | 0 |
| crates/bitwarden-vault/src/cipher/cipher_client/create.rs | 16315 | `5e19d851bf22fd2ec9a5e91efb55d633bb84f6466d9eb2940cddc57e11bf8933` | 0 |
| crates/bitwarden-vault/src/cipher/cipher_client/delete.rs | 11026 | `8c1dac34d839e31c3b45f31648af96f1408c90ce85f28875058f1be37ff08dbf` | 0 |
| crates/bitwarden-vault/src/cipher/cipher_client/delete_attachment.rs | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| crates/bitwarden-vault/src/cipher/cipher_client/edit.rs | 52525 | `0658a227fa6d928dd4a4fcdafcd2bd47062d56d10d5c80f6d7bb98b89fba8626` | 1 |
| crates/bitwarden-vault/src/cipher/cipher_client/get.rs | 4510 | `b782df39e8a3c7d577cde91b7fa697a970032993d2595fb577c03ef512930b85` | 0 |
| crates/bitwarden-vault/src/cipher/cipher_client/mod.rs | 40477 | `201bead51b16ec84ee1132dc680e3728eba2b34709899d9d040d3e1215bce6a7` | 0 |
| crates/bitwarden-vault/src/cipher/cipher_client/move_many.rs | 6886 | `b53a0853bcad04cb1064fe007e440d73075c8d80930eb27783f47c51a0fc39e3` | 0 |
| crates/bitwarden-vault/src/cipher/cipher_client/restore.rs | 19894 | `67ad277f03a2dcbfadad1e8654ae1d8baecfad7e56c4d3d5c05ba59c3f155823` | 0 |
| crates/bitwarden-vault/src/cipher/cipher_client/share_cipher.rs | 51781 | `c0326e74ea5b8a34bc8b246aabb9e2132679d899de0373b4496b2f7e433f173e` | 2 |
| crates/bitwarden-vault/src/cipher/cipher_permissions.rs | 780 | `b543e616d754320d5d4f0aec60be35c6a2dc365322bd5c50402a5b93364c7360` | 0 |
| crates/bitwarden-vault/src/cipher/cipher_view_type.rs | 4541 | `c848ea85d22cc5ed186953731ff162cddfa63315da5b193da6b2f854617007c7` | 0 |
| crates/bitwarden-vault/src/cipher/drivers_license.rs | 17812 | `a7d75a49fc1ca635ded8dfe9c7eed2edda9e867caaa36c582098e917cfc06ae1` | 0 |
| crates/bitwarden-vault/src/cipher/field.rs | 8343 | `50542f7bfbf99df9c88f265567fe01725a5296135585bc75414ac2327bb942b5` | 0 |
| crates/bitwarden-vault/src/cipher/identity.rs | 15308 | `449d88e6f6c9a61608539ad8f8a5e78c68ddd216ba607890a8f9d529784be8af` | 0 |
| crates/bitwarden-vault/src/cipher/linked_id.rs | 3122 | `1e43606a1ee5f5e804bd59da3f320c100a2405727eea2110efcf8242c60fa3ec` | 0 |
| crates/bitwarden-vault/src/cipher/local_data.rs | 1691 | `b3d652c7b2cba1c49c47a581a4edee61ae0621cedc4414d10ad8bebf96746f31` | 0 |
| crates/bitwarden-vault/src/cipher/login.rs | 32479 | `87af284ed426c8cf78dd0403df89262422f97e39c432bc47ba2ab0ec85a2d3ae` | 0 |
| crates/bitwarden-vault/src/cipher/mod.rs | 2161 | `b0337aea113218e861b0e2cd03c4d44fca54b167e59825773b557ba663b4fe95` | 0 |
| crates/bitwarden-vault/src/cipher/passport.rs | 19358 | `d64e681ed32f148be3d637281723856f28d9bcc3dbd631e6acba3a260fa01869` | 0 |
| crates/bitwarden-vault/src/cipher/secure_note.rs | 6924 | `aeb1b6e54b37605c299a4acd4ba4fbbc9a4d146154db819de4069d5be66640e3` | 0 |
| crates/bitwarden-vault/src/cipher/ssh_key.rs | 12456 | `55dc7fc3b9863ffb6e60fc0fb107a90389b3215911cf5b681bdae28f8d030ae1` | 2 |
| crates/bitwarden-vault/src/cipher_risk/cipher_risk_client.rs | 19566 | `b9a328588bb94761cba27d36c0cd5e60eeeca669d32afd6b8f7ea8a966b52e5a` | 8 |
| crates/bitwarden-vault/src/cipher_risk/hibp.rs | 5888 | `8d8715c45a72e325bfc45b0dbe26cdcd3e0ab8121a921c98b4ff0d163f05f659` | 1 |
| crates/bitwarden-vault/src/cipher_risk/mod.rs | 231 | `82c8c75465914d4872fba3a0526e7d59fca2f4b4ba4eb7faa02d07efc6601878` | 0 |
| crates/bitwarden-vault/src/cipher_risk/password_strength.rs | 2872 | `1fc3c742e0b051ed4f2924c4de4d80811177f45a0c87c2edfa603adac50f0931` | 0 |
| crates/bitwarden-vault/src/cipher_risk/types.rs | 3721 | `9307aa87853f3dfedd42d18d9d6c38bf19af9e43f7ebf6ab0cfe5103e3f4a948` | 0 |
| crates/bitwarden-vault/src/domain.rs | 697 | `4da13aa850335c5a22b7dc444863aef0bd5cfd5dedf073b2c48a3d46b5b817c5` | 0 |
| crates/bitwarden-vault/src/error.rs | 1466 | `4edb0acb799503a171d95b8c18500a807924fe7c09136bfe89a111b3b1b77a22` | 0 |
| crates/bitwarden-vault/src/folder/create.rs | 5517 | `eda59ff480103d5f5c5fe88dadea3221d0407725d6b29f88f12171b1d2d4feb5` | 0 |
| crates/bitwarden-vault/src/folder/edit.rs | 6345 | `006343c0223fa53ab5d56df1331681659a8e4b3de824c34ccc80c3be93a1c281` | 0 |
| crates/bitwarden-vault/src/folder/folder_client.rs | 1430 | `fbf994bced1fb16223b7cde68858ea16ff6a6d3466fcdf214de8ac714eb3b851` | 0 |
| crates/bitwarden-vault/src/folder/folder_models.rs | 2892 | `2ba4b7bcad74d833979f80db600950bbcd8ebfd3aedbb482575df753198e6ccd` | 0 |
| crates/bitwarden-vault/src/folder/folder_sync_handler.rs | 3918 | `ea8179a0624818a4cbcb0fd69833cc079bff399c69f4939bbef201550bd8231d` | 0 |
| crates/bitwarden-vault/src/folder/get_list.rs | 4651 | `20ad2fa312df256522137209f145e2f28d6f5d72958f6f8d799e46c2731f3cc3` | 0 |
| crates/bitwarden-vault/src/folder/mod.rs | 386 | `be158451a6c658b30112b88f3bd78e723e8c3111b8a4c02b8bf7561d3abf84f7` | 0 |
| crates/bitwarden-vault/src/lib.rs | 781 | `a16cffe0aa449299dd5644ff0e989d23a62129029009798ee388017e3c879a03` | 0 |
| crates/bitwarden-vault/src/password_history.rs | 3304 | `8196cc8229dfce5541724c49936bc98b50e509703199f8f19dacc617caa754a6` | 0 |
| crates/bitwarden-vault/src/password_history_client.rs | 850 | `b407ea7214fbf72bd83d30f9db23d293b64fc86a0dc2226a56ad2b55dec178a3` | 0 |
| crates/bitwarden-vault/src/totp.rs | 25803 | `8571a94439f25dc58a7db64f1a407d8779e79a35df10086c7e28724f8e71e98f` | 0 |
| crates/bitwarden-vault/src/totp_client.rs | 1509 | `9222861ebbe9f4f75c62fa21f69db1e9e4fd2f4a7afb4d13b08788c1514b26ea` | 0 |
| crates/bitwarden-vault/src/uniffi_support.rs | 359 | `e7f7723bb161a71cd93e85d2d2ce7db7be68f8042e7db9fb3710b5c6896a0d09` | 0 |
| crates/bitwarden-vault/src/vault_client.rs | 1960 | `828075ae6663706d21bdb861a16107daf8ccd2b96a6ad8e5d56b42a02f2a381c` | 0 |
| crates/bitwarden-wasm-internal/Cargo.toml | 4241 | `7db07d4d14e14e37cfbf00a8bf0f775df38eda4bef06cb395082ef85e5a6b4db` | 0 |
| crates/bitwarden-wasm-internal/bitwarden_license/npm/index.js | 267 | `b97116717386bb3311641e56b9442380c373e3d072f6efee4b83a3656646c72f` | 0 |
| crates/bitwarden-wasm-internal/bitwarden_license/npm/package-lock.json | 1813 | `2ac751beb43dc6d76ab9bf054c6e56333947310465414a4ebaf4e2bf6660df45` | 0 |
| crates/bitwarden-wasm-internal/bitwarden_license/npm/package.json | 993 | `43fbdc37fb1fd73ba72efc55d657c99c320a9175c6424cbead9105048baccfae` | 0 |
| crates/bitwarden-wasm-internal/build.rs | 1853 | `5d1ace6b8ed67b77cc1e5df5b50d9e5b9f66b3d49d43e34d7528fe7ced862e62` | 0 |
| crates/bitwarden-wasm-internal/npm/index.js | 267 | `b97116717386bb3311641e56b9442380c373e3d072f6efee4b83a3656646c72f` | 0 |
| crates/bitwarden-wasm-internal/npm/package-lock.json | 1746 | `5eb78605c45613ebd0fd640b2bba6ad2447308b48d07168adc41a8170333dab2` | 0 |
| crates/bitwarden-wasm-internal/npm/package.json | 937 | `d0991cb3c972894f8eb5d6e14da10e331e8297aa8fa92e78b8986d5a11596c8b` | 0 |
| crates/bitwarden-wasm-internal/src/client.rs | 6749 | `040ba33bb9344ca6ef357daeb49172ddf04585cb367678cd2acc1b1457cca072` | 0 |
| crates/bitwarden-wasm-internal/src/custom_types.rs | 885 | `7c9c09e8b99b2ad632976039292988e722aef0f33b8453de56e97734ea140f64` | 0 |
| crates/bitwarden-wasm-internal/src/flight_recorder.rs | 1686 | `b702babaf7984654de558ce4d242882de7a8ead3522fca577755327075e9f3bb` | 0 |
| crates/bitwarden-wasm-internal/src/init.rs | 2826 | `eb675bd0ab83030719c33e7be3259dbb02b50d4b708a8ed3aeb8250dad9b227d` | 0 |
| crates/bitwarden-wasm-internal/src/lib.rs | 690 | `51a46c5f87e8131c6bbc4e9e6feb903fd74caee36545c4b28309ed63f85457e6` | 0 |
| crates/bitwarden-wasm-internal/src/platform/mod.rs | 1469 | `a35e2c4a1e4efc9b67a1cd9fe4263887d3726be690855697f7b9082c77225c52` | 0 |
| crates/bitwarden-wasm-internal/src/platform/repository.rs | 12438 | `b0f0628813f83d807bdc506c139415edf98a3462d84b9b3e1d8f1ac2834ea16f` | 0 |
| crates/bitwarden-wasm-internal/src/platform/token_provider.rs | 1305 | `5f33c58a226028829350397f58be68f2d50c0dfbdf74ee36d59ef72c173eb3d5` | 0 |
| crates/bitwarden-wasm-internal/src/pure_crypto.rs | 26116 | `5f947b051d9c16c4cb631d4d1e4914410034b6e9389bdd31f837554490bb9693` | 3 |
| crates/bitwarden-wasm-internal/src/ssh.rs | 1420 | `40ce148a6643a9793359dcc36a6f8668d8c9b3e4d98fd6a655d37c1b78e74cc4` | 0 |
| crates/bw/Cargo.toml | 1627 | `a55473cac0903896f014573498204b41a1494e49855acf2bd984dff5199e2df6` | 0 |
| crates/bw/src/admin_console/mod.rs | 2242 | `70a53accf4836210e905f48e34ab455c5c575238f6c1e4355c3709dc7105b66d` | 0 |
| crates/bw/src/auth/login.rs | 3685 | `ab1d5629fd4a639eaa959434f6aee2959157ee12e340fa6dc88c7d658d6a0426` | 0 |
| crates/bw/src/auth/mod.rs | 1793 | `992d9e806549e554eafcddc32ed778f876b2fd378be59120a63ad099dd0a9b3e` | 0 |
| crates/bw/src/client_state.rs | 8526 | `1ce734b3cae3662f6f8deb00e2706cecedfb2452846cc1231e9d492a2df93c5e` | 0 |
| crates/bw/src/command/create.rs | 1363 | `93d2c0f4cf9e8fae6752fb0656008493ee2fae1199b1795ea3db4987a67dbbb6` | 0 |
| crates/bw/src/command/delete.rs | 573 | `ace7197f5a375f82d9467f8a91596fd06e5bffef8a705f799bffa286b203ee5a` | 0 |
| crates/bw/src/command/edit.rs | 555 | `d4a28994419329039eae52be1e24b6458aae240db085c26480f7525ee93e24a2` | 0 |
| crates/bw/src/command/get.rs | 2218 | `1939dcef4ac124ae5541c7729e4d210dc6b45b04a0a6b283829f9414256904f7` | 0 |
| crates/bw/src/command/list.rs | 808 | `4f1322f20529d873b465201ffd06c62a0e0dc44d08cd4801ed416e72cb410488` | 0 |
| crates/bw/src/command/mod.rs | 5972 | `66bc0c435e7f46594dc1927948dd3d55c11b46c9f673a9d71f25d92750d7f29b` | 0 |
| crates/bw/src/dirt/mod.rs | 90 | `059e9a21e19b19d8371a600daea02718b9f2cbbce09978e3ef73c3ce0dc7af8a` | 0 |
| crates/bw/src/key_management/lock.rs | 578 | `6c3c5e518109d772701c4cb7559f8f7b83fde9dff81f7de286baef0839abd74d` | 0 |
| crates/bw/src/key_management/mod.rs | 585 | `1349155f844136f032cd4c3f32c1b90e0a677ba70dde47f361c73ea5c19b8513` | 0 |
| crates/bw/src/main.rs | 9986 | `5cb2e1be6c73fc6b206537ba34f848a12faa3c02b9ad394b4ff190ea67c5e049` | 0 |
| crates/bw/src/platform/appdata.rs | 2082 | `ff23de6e0e6a04c2daed27107f69d08d566abb824e3b7c05baa1bce753eb3a71` | 0 |
| crates/bw/src/platform/completion.rs | 875 | `eccaf05118a2e0798bb8cf3ec49b7a2dbd28e29e173fb8708d1c19fd5b759546` | 0 |
| crates/bw/src/platform/config.rs | 13259 | `18d6329518cbaa6e2322849da5c2be972380c859fff6050de2d87847f3ab6008` | 0 |
| crates/bw/src/platform/encode.rs | 467 | `1a723f1463386fab23f7b4ec0d8046cf30f98fae8aacb212dc7f56ba0b1a262e` | 0 |
| crates/bw/src/platform/mod.rs | 555 | `05c664b7032dcc59362a6dfcf3053c372c3ea33bb8fd24010f2b92c7fb7487ac` | 0 |
| crates/bw/src/platform/serve.rs | 409 | `9dd3b071eb6606f8d97ae173609283ab713703d97b467d148094a91f02e9a13e` | 0 |
| crates/bw/src/platform/status.rs | 5738 | `52ded1eb96f855eab15c4a40e56dfba42010bb06c936ff8dc6f1574bfb564089` | 0 |
| crates/bw/src/platform/sync.rs | 1639 | `7f2b390eb6f96aefa0be376e1596f82e1d9747cf14a807021b7dd21783a5abf3` | 0 |
| crates/bw/src/render.rs | 3189 | `3b42071836e0feb51a93cb5bea9f12dfc14c8abbf5d027880819d7baba24c767` | 0 |
| crates/bw/src/tools/file_output.rs | 12682 | `ccd95346077ab4f9a56cc321eb67886152ae8c0db44b4372aa35128148fa5718` | 0 |
| crates/bw/src/tools/mod.rs | 8696 | `c57c101e0f68f5e5220a401a305c2d9916e48ca5dc44f67f00249bcde871b814` | 0 |
| crates/bw/src/tools/receive.rs | 36558 | `031115cf1684d667205e993ffe9733e848aff942a6fc58a7f9d4202596c54da3` | 0 |
| crates/bw/src/tools/send.rs | 82218 | `c08e581bb74fcaf299a166e9fafe6f60e4452c78d9bb7505866e417c005a615d` | 0 |
| crates/bw/src/tools/send_access_token_cache.rs | 8695 | `1cdbdf450f1d9277674d9fbb2610735c17fe7e6c581aa2f35d0efd7400cb9d92` | 1 |
| crates/bw/src/vault/mod.rs | 4897 | `6db9267a0296f7eaa3ac698449e4df874b899f9434c8228157440c5cf9815106` | 0 |
| crates/uniffi-bindgen/Cargo.toml | 544 | `660b3773db040aaaa303c0996e75ee10d91c4887ad98cebca43d512c32b77d07` | 0 |
| crates/uniffi-bindgen/uniffi-bindgen.rs | 48 | `55a5501b6239f6f219489db85de7ead6d2bf0c927f4fa1cfd674779e33d59c31` | 0 |
| crates/wasm-bindgen-cli-runner/Cargo.toml | 543 | `4cf06a111d25c6fd087ec74e26a36c9ec7bf367dad37ac639abee24fd7bb08fa` | 0 |
| crates/wasm-bindgen-cli-runner/wasm-bindgen-runner.rs | 276 | `5cb7f3feee7c1d728d6a13798ec96941b85bd9340f7cf2568632276479cfb4eb` | 0 |
| crates/wasm-bindgen-cli-runner/wasm-bindgen-test-runner.rs | 288 | `197d1fcfd8dcaf8ffb4b574aa1f66e0e2bde05790dca3cc928281804d0d41d1c` | 0 |
| package-lock.json | 89567 | `d1198053f89c6e36e3f59506e60ea55fe02e1620af2933c0b475de7057e9c33e` | 0 |
| package.json | 1021 | `33ffb5b3e61118435d220c7469ff87ebe277bce55983e537154ab98f2fab46eb` | 0 |
