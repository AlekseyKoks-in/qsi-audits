# Отчёт об аудите безопасности и постквантовой готовности

**Проект:** rustcrypto-rsa @ f96c4b5d629a · RustCrypto project — публичный репозиторий (пассивная проверка)
| | |
|---|---|
| Организация | QSI |
| Дата отчёта | 2026-10-28 12:51 UTC |
| Версия отчёта | 1 |
| Запуск аудита | 1acd22ab-77cd-485d-86c8-d51734a5ccfe (Документальный аудит) |
| Версия анализатора | qsi-engine 1.2.0 |
| Профиль риска | Разработчик ПО безопасности |
| SHA-256 содержимого | `c0d439a694ce1e368fd2f36235910d4b8fb8e439d2c8ee8f0b7a317d4baa0ae1` |
| Ключ подписи (Ed25519, отпечаток SHA-256; подпись — отдельный файл report.sig.json) | `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e` |
> Отчёт содержит результаты автоматизированного и документального анализа в указанных границах. Он не является юридическим заключением, сертификацией или подтверждением соответствия какому-либо стандарту.

## 1. Резюме для руководства

- Критическая: **0**
- Высокая: **0**
- Средняя: **1**
- Низкая: **2**
- Информационная: **1**

- Подтверждённая техническая уязвимость: 0
- Известная уязвимая версия компонента: 2
- Подтверждённая ошибка конфигурации: 0
- Потенциальный криптографический риск: 0
- Долгосрочный постквантовый риск: 1
- Рекомендация по улучшению: 0
- Недостаточность данных: 1

Неравенство Моски (x + y > z): x = 10, y = 3, z = 8 → при этом сценарии миграция завершится слишком поздно. _z — плановое допущение профиля риска, а не прогноз. Публично известного криптографически значимого квантового компьютера сегодня не существует._

**Постквантовая зрелость: Уровень 0 из 4 — постквантовой криптографии нет.** Следующий шаг: Проведите инвентаризацию: где классическая криптография с открытым ключом защищает долгоживущие данные и ключи, и выберите первую миграцию — обычно гибридный обмен ключами TLS и обёрнутые ключи.

## 2. Область и границы проверки

Режим: Документальный аудит

Репозиторий: <https://github.com/RustCrypto/RSA> @ `f96c4b5d629a0aeb6f680294debfd38ec8a81f68` — ссылки в доказательствах открывают строки на этом коммите.

35 файлов, всего 300818 байт, редактирований: 5; список SHA-256 по файлам — в приложении C.

## 3. Методология

| Область | Статус | Количество | Примеры |
|---|---|---|---|
| dependencies | проверено | 3 | Cargo.lock: 120 dependencies parsed (120 pinned); Cargo.toml: 28 dependencies parsed (0 pinned); marvin-toolkit/Cargo.toml: 3 dependencies parsed (0 pinned) |
| source_code | проверено | 32 | src/algorithms/generate.rs: 187 lines scanned with 16 rule patterns and 122 registry patterns; 50 lines in #[cfg(test)] modules ignored; src/algorithms/mgf.rs: 78 lines scanned with 16 rule patterns and 122 registry patterns; src/algorithms/oaep.rs: 262 lines scanned with 16 rule patterns and 122 registry patterns |
| keys | ошибка (не проверено) | 1 | src/key.rs line 1134: public key could not be parsed (ValueError) |
| certificates_and_keys | проверено | 5 | src/key.rs: certificates/keys parsed; src/lib.rs: certificates/keys parsed; src/oaep.rs: certificates/keys parsed |
| keys | проверено | 5 | src/lib.rs: the key block at line 139 sits in a documentation comment, where it is the worked example of the crate's own API; src/oaep.rs: private key block at line 339 is test data (test code); src/pkcs1v15.rs: private key block at line 304 is test data (test code) |
| osv_advisories | проверено | 1 | 120 pinned packages queried at OSV.dev; 2 affected |

_Длинные списки здесь сгруппированы; полный список по файлам — в JSON-версии отчёта, подписанной тем же ключом._

## 4. Проверенные и непроверенные активы

- keys — ошибка (не проверено): src/key.rs line 1134: public key could not be parsed (ValueError)

## 5. Краткое описание архитектуры

Static review of the source tree rustcrypto-rsa at f96c4b5d629a0aeb6f680294debfd38ec8a81f68. 35 files analysed; of 75 files, 23 are test, fuzzing, benchmark or example code and were left out, 17 are not read by any analyzer, 0 exceed the per-file limit and 0 did not fit the total limit. No requests were sent to the owner's systems.

## 6. Общая оценка состояния безопасности

- Ориентировочный индекс состояния: **98** / 100 — _Рассчитан по находкам в области проверки (подтверждённые и потенциальные проблемы, взвешенные по серьёзности). Ориентировочный; не сравним между аудитами с разной областью._
- Доля квантово-уязвимых элементов инвентаризации: 54.5%

## 7. Подробное описание находок

### QSI-2026-05056 — Квантово-уязвимый RSA: роль не определена (5 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `source-code:RSA:general`
- Источник данных: src/encoding.rs
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-28 12:51 UTC
- Балл приоритета: 35.3 / 100
- CVSS v3.1: неприменимо

8 упоминаний RSA в 5 файл(ах), например src/encoding.rs:68. Роль по путям, именам функций и соседнему коду: роль не определена. По коду не видно, что защищают ключи; приоритет определит проверка.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте src/encoding.rs:68 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [src/encoding.rs](https://github.com/RustCrypto/RSA/blob/f96c4b5d629a0aeb6f680294debfd38ec8a81f68/src/encoding.rs#L68) · line 68 · SHA-256 848496bd7c37c63103d96a76766750a0c93994941a9810bfd3804b1d855e2f05_

```
   67 | 
   68 |         RsaPrivateKey::from_components(n, e, d, primes).map_err(|_| KeyMalformed)
   69 |     }
```

_file_excerpt · [src/encoding.rs](https://github.com/RustCrypto/RSA/blob/f96c4b5d629a0aeb6f680294debfd38ec8a81f68/src/encoding.rs#L88) · line 88 · SHA-256 51040fadaa40d8aefffe667c170da4266984b8003fe2220dcf044ffd55ab4c03_

```
   87 | 
   88 |         RsaPublicKey::new(n, e).map_err(|_| KeyMalformed)
   89 |     }
```

_file_excerpt · [src/key.rs](https://github.com/RustCrypto/RSA/blob/f96c4b5d629a0aeb6f680294debfd38ec8a81f68/src/key.rs#L338) · line 338 · SHA-256 b400f8009b313e186171f142d7584b0f639b5a05524e78b44461a94f2104c7ca_

```
  337 |         let components = generate_multi_prime_key_with_exp(rng, 2, bit_size, exp)?;
  338 |         RsaPrivateKey::from_components(
  339 |             components.n.get(),
```

_file_excerpt · [src/key.rs](https://github.com/RustCrypto/RSA/blob/f96c4b5d629a0aeb6f680294debfd38ec8a81f68/src/key.rs#L364) · line 364 · SHA-256 6202abba500461e188a8f64092e4524b2f6dfb3202a0694dc57bad41e0fe4ecc_

```
  363 |         let components = generate_multi_prime_key_with_exp(rng, 2, bit_size, exp)?;
  364 |         RsaPrivateKey::from_components(
  365 |             components.n.get(),
```

_file_excerpt · [src/pkcs1v15/signing_key.rs](https://github.com/RustCrypto/RSA/blob/f96c4b5d629a0aeb6f680294debfd38ec8a81f68/src/pkcs1v15/signing_key.rs#L60) · line 60 · SHA-256 b0263c77cb240628bb2f31d489438c088a47a65609d04db1b81f99208ac3d2b4_

```
   59 |         Ok(Self {
   60 |             inner: RsaPrivateKey::new(rng, bit_size)?,
   61 |             prefix: pkcs1v15_generate_prefix::<D>(),
```

_file_excerpt · [src/pkcs1v15/signing_key.rs](https://github.com/RustCrypto/RSA/blob/f96c4b5d629a0aeb6f680294debfd38ec8a81f68/src/pkcs1v15/signing_key.rs#L89) · line 89 · SHA-256 96efd77715170f81d71a18c7c23d8db777764f09d7bfbc345825c9e3cf46a90a_

```
   88 |         Ok(Self {
   89 |             inner: RsaPrivateKey::new(rng, bit_size)?,
   90 |             prefix: Vec::new(),
```

_file_excerpt · [src/pss/blinded_signing_key.rs](https://github.com/RustCrypto/RSA/blob/f96c4b5d629a0aeb6f680294debfd38ec8a81f68/src/pss/blinded_signing_key.rs#L80) · line 80 · SHA-256 129f3a710601ea4cfcdb8113049c8c1f093d9e451247404aac20c41f11d9efdd_

```
   79 |         Ok(Self {
   80 |             inner: RsaPrivateKey::new(rng, bit_size)?,
   81 |             salt_len,
```

_file_excerpt · [src/pss/signing_key.rs](https://github.com/RustCrypto/RSA/blob/f96c4b5d629a0aeb6f680294debfd38ec8a81f68/src/pss/signing_key.rs#L85) · line 85 · SHA-256 00c09dc98ca719774e6d1850f1e06364da42e2119ba5c17415b5e09cb961ae53_

```
   84 |         Ok(Self {
   85 |             inner: RsaPrivateKey::new(rng, bit_size)?,
   86 |             salt_len,
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Классифицируйте каждое использование, зафиксируйте сроки жизни данных и запланируйте миграцию на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема; введите уровень абстракции для криптогибкости.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-05058 — crypto-bigint 0.7.5 затронут RUSTSEC-2026-0387 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/crypto-bigint@0.7.5`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 12:51 UTC
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

### QSI-2026-05059 — ctutils 0.4.2 затронут RUSTSEC-2026-0385 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/ctutils@0.4.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 12:51 UTC
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

### QSI-2026-05057 — Не обнаружено криптобиблиотек с поддержкой PQC

- Серьёзность: **Информационная** · Классификация: Недостаточность данных · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependencies`
- Источник данных: dependency manifests
- Метод обнаружения: Сопоставление названий зависимостей.
- Анализатор: dependencies 1.2.0 · 2026-10-28 12:51 UTC
- Балл приоритета: 13.5 / 100
- CVSS v3.1: неприменимо

В 3 манифестах зависимостей QSI нашёл криптобиблиотеки (rsa), но ни одной из списка поддерживающих PQC.

**Возможные последствия.** Только индикатор готовности: поддержка PQC может обеспечиваться платформой (OpenSSL, ОС, облачный KMS), а не зависимостями приложения.

**Шаги воспроизведения.**

```
Изучите перечисленные в доказательстве манифесты.
```

**Подтверждающие доказательства.**

_dependency · Cargo.lock, Cargo.toml, marvin-toolkit/Cargo.toml · SHA-256 bceb41c8a05bf5308ccf41f3394d1edb11551672e62af9fdef4204d525b694bf_

```
Crypto libraries: rsa
```

**Ограничения проверки.** Отсутствие доказательств не является доказательством отсутствия: системные библиотеки и транзитивные зависимости могут не указываться.

**Рекомендация.** Определите источник поддержки PQC (TLS-терминатор, KMS/HSM, обновление библиотек).

**Повторная проверка.** Повторите сканирование после обновлений.


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

### Постквантовая зрелость: Уровень 0 из 4 — постквантовой криптографии нет


**Следующий шаг:** Проведите инвентаризацию: где классическая криптография с открытым ключом защищает долгоживущие данные и ключи, и выберите первую миграцию — обычно гибридный обмен ключами TLS и обёрнутые ключи.

_Уровни: 0 — нет; 1 — есть, но не подключено; 2 — используется вне критичных путей; 3 — гибрид в критичном пути; 4 — постквантовое по умолчанию в критичных путях (корень доверия, обёртка ключей, обмен ключами в канале). Оценка по коду и манифестам._

### Что делают квантово-уязвимые алгоритмы

| Роль | Алгоритмы (файлы) | ID | Первый шаг |
|---|---|---|---|
| **роль не определена** | RSA (5) | QSI-2026-05056 | Классифицируйте каждое использование, зафиксируйте сроки жизни данных и запланируйте миграцию на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема; введите уровень абстракции для криптогибкости |

_Роль определяется по путям файлов, именам функций и коду вокруг совпадений; проверка её подтверждает. Сначала — ключи корня доверия и обёрнутые ключи: их трудно заменить или можно записать уже сегодня._
Анкета готовности для проекта не заполнялась.

### Квантовые алгоритмы, значимые для этой инвентаризации

| Квантовый алгоритм | Действие | Модель атаки | Алгоритмы из инвентаризации (строк) | Что это значит для аудита |
|---|---|---|---|---|
| Алгоритм Шора — факторизация | взламывает | Q1 | RSA (6) | Взламывает RSA при любой длине ключа: более длинный модуль лишь полиномиально повышает стоимость. Планируйте переход на ML-KEM (или гибрид) для установления ключей и ML-DSA / SLH-DSA для подписей; начинайте с ключей, защищающих данные, которые должны оставаться конфиденциальными годами («собери сейчас — расшифруй потом»), и с долгоживущих подписей. |
| Алгоритм Гровера — поиск ключа и прообразов | ослабляет (более длинные ключи восстанавливают запас) | Q1 | SHA-2 (4) | Не взлом. Ключи 256 бит (AES-256, ChaCha20) сохраняют хороший запас; AES-128 соответствует категории 1 NIST, но некоторые регуляторы требуют 256-битных ключей в квантово-устойчивых системах (см. запись AES-128). Для долгоживущих данных предпочитайте 256-битные ключи; 256-битные хеши для стойкости к прообразам менять не нужно. |
| Брассар–Хойер–Тапп — поиск коллизий | ослабляет (более длинные ключи восстанавливают запас) | Q1 | SHA-2 (4) | 256-битные хеши (SHA-256, SHA3-256) остаются достаточными по стойкости к коллизиям; 160-битные хеши слабы уже классически (коллизии SHA-1 практичны). Где нужны категории NIST 4–5, используйте хеши на 384/512 бит. |

_Действие: взламывает — алгоритм нужно заменить; ослабляет — более длинные ключи или выходы восстанавливают запас; учтено в стандартных параметрах — при стандартных наборах действий не требуется; только при суперпозиционных запросах — к обычному применению неприменимо._


## 9. Ограничения и допущения

- Отчёт содержит результаты автоматизированного и документального анализа в указанных границах. Он не является юридическим заключением, сертификацией или подтверждением соответствия какому-либо стандарту.
- z — плановое допущение профиля риска, а не прогноз. Публично известного криптографически значимого квантового компьютера сегодня не существует.
- keys: src/key.rs line 1134: public key could not be parsed (ValueError)

## 10. План устранения проблем / Приоритеты на 30, 60 и 90 дней

### 30 дн.

| Приоритет | ID | Действие | Тип | Условие закрытия |
|---|---|---|---|---|
### 60 дн.

| Приоритет | ID | Действие | Тип | Условие закрытия |
|---|---|---|---|---|
| P3 | QSI-2026-05058 | Разберите RUSTSEC-2026-0387; при необходимости обновите crypto-bigint до исправленной версии (0.7.6). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0387 или результат разбора записан. |
| P3 | QSI-2026-05059 | Разберите RUSTSEC-2026-0385; при необходимости обновите ctutils до исправленной версии (0.4.4). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0385 или результат разбора записан. |
### 90 дн.

| Приоритет | ID | Действие | Тип | Условие закрытия |
|---|---|---|---|---|
| P3 | QSI-2026-05056 | Внесите использования RSA в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P4 | QSI-2026-05056 | Запланируйте миграцию RSA на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема или гибридной схемы. |

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
2. C. Gidney — How to factor 2048 bit RSA integers with less than a million noisy qubits (arXiv:2505.15917) — arXiv. <https://arxiv.org/abs/2505.15917> (preprint (2025-05-21): < 1 million noisy qubits, < 1 week, 0.1% gate error, 1 µs surface-code cycle)
3. C. Gidney, M. Ekerå — How to factor 2048 bit RSA integers in 8 hours using 20 million noisy qubits (Quantum 5, 433) — Quantum. <https://doi.org/10.22331/q-2021-04-15-433> (peer-reviewed article (2021): 10^-3 gate error, 1 µs cycle, 10 µs reaction time)
4. C. Zalka — Grover's quantum searching algorithm is optimal (Phys. Rev. A 60, 2746, 1999; arXiv:quant-ph/9711070) — APS. <https://doi.org/10.1103/PhysRevA.60.2746> (peer-reviewed article: optimal for any success probability; parallel search gains no more than splitting the space)
5. Common Vulnerability Scoring System v3.1: Specification Document — FIRST. <https://www.first.org/cvss/v3.1/specification-document> (final)
6. D. J. Bernstein — Cost analysis of hash collisions: Will quantum computers make SHARCS obsolete? (2009) — cr.yp.to. <https://cr.yp.to/hash/collisioncost-20090823.pdf> (paper dated 2009-08-23)
7. FIPS 203 — Module-Lattice-Based Key-Encapsulation Mechanism Standard (ML-KEM) — NIST. <https://csrc.nist.gov/pubs/fips/203/final> (final (August 2024))
8. FIPS 204 — Module-Lattice-Based Digital Signature Standard (ML-DSA) — NIST. <https://csrc.nist.gov/pubs/fips/204/final> (final (August 2024))
9. FIPS 205 — Stateless Hash-Based Digital Signature Standard (SLH-DSA) — NIST. <https://csrc.nist.gov/pubs/fips/205/final> (final (August 2024))
10. G. Brassard, P. Høyer, A. Tapp — Quantum Algorithm for the Collision Problem (LATIN '98; arXiv:quant-ph/9705002) — Springer / arXiv. <https://arxiv.org/abs/quant-ph/9705002> (peer-reviewed article: collisions of r-to-one functions in O((N/r)^{1/3}) expected evaluations)
11. L. K. Grover — A fast quantum mechanical algorithm for database search (STOC 1996) — ACM. <https://doi.org/10.1145/237814.237866> (peer-reviewed article)
12. M. Amy et al. — Estimating the cost of generic quantum pre-image attacks on SHA-2 and SHA-3 (SAC 2016; arXiv:1603.09383) — Springer / arXiv. <https://arxiv.org/abs/1603.09383> (peer-reviewed article: SHA-256 about 2^153.8 surface-code cycles on 2^12.6 logical qubits; SHA3-256 about 2^146.5 cycles on 2^20)
13. M. Cain et al. — Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits (arXiv:2603.28627) — arXiv. <https://arxiv.org/abs/2603.28627> (preprint (2026-03-30): P-256 in a few days with 26,000 physical neutral-atom qubits; RSA-2048 one to two orders of magnitude longer)
14. M. Mosca — Cybersecurity in an Era with Quantum Computers: Will We Be Ready? (IEEE Security & Privacy, 2018) — IEEE. <https://doi.org/10.1109/MSP.2018.3761723> (peer-reviewed article; source of the x + y > z migration inequality)
15. NIST IR 8547 — Transition to Post-Quantum Cryptography Standards — NIST. <https://csrc.nist.gov/pubs/ir/8547/ipd> (initial public draft (November 2024); proposes deprecating quantum-vulnerable public-key algorithms after 2030 and disallowing them after 2035 — dates may change in the final version)
16. NIST — Post-Quantum Cryptography Standardization: Evaluation Criteria, Security (Call for Proposals, Section 4.A.5) — NIST. <https://csrc.nist.gov/Projects/Post-Quantum-Cryptography/Post-Quantum-Cryptography-Standardization/Evaluation-Criteria/Security-(Evaluation-Criteria)> (security categories: AES-128 key search 2^170/MAXDEPTH quantum gates, AES-192 2^233/MAXDEPTH, AES-256 2^298/MAXDEPTH; MAXDEPTH 2^40–2^96)
17. OSV advisory RUSTSEC-2026-0385 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0385> (modified 2026-10-23T08:30:02.389575143Z)
18. OSV advisory RUSTSEC-2026-0387 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0387> (modified 2026-10-24T03:45:02.365137418Z)
19. P. W. Shor — Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms on a Quantum Computer (SIAM J. Comput., 1997) — SIAM. <https://doi.org/10.1137/S0097539795293172> (peer-reviewed article)
20. S. Jaques, M. Naehrig, M. Roetteler, F. Virdia — Implementing Grover oracles for quantum key search on AES and LowMC (EUROCRYPT 2020; arXiv:1910.01700) — Springer / arXiv. <https://arxiv.org/abs/1910.01700> (peer-reviewed article: lower cost estimates for the AES key searches that define the NIST categories)

## Приложения: Криптографическая инвентаризация

| Алгоритм | Параметр | Библиотека | Расположение | Квантовый статус | Классический статус |
|---|---|---|---|---|---|
| SHA-2 | SHA-384 |  | src/pkcs1v15.rs:267 | сниженный запас (Гровер), одобрен | допустимо |
| SHA-2 | SHA-512 |  | src/pkcs1v15.rs:272 | сниженный запас (Гровер), одобрен | допустимо |
| SHA-2 | SHA-224 |  | src/pkcs1v15.rs:257 | Гровер: допустимо по NIST, ниже рекомендаций ECCG/ANSSI | устаревающий |
| SHA-2 | SHA-256 |  | src/pkcs1v15.rs:262 | Гровер: допустимо по NIST, ниже рекомендаций ECCG/ANSSI | допустимо |
| Crypto library | 0.9 | rsa (RustCrypto rsa) | marvin-toolkit/Cargo.toml | н/п | допустимо |
| RSA |  |  | src/algorithms/rsa.rs | уязвим (Шор) | допустимо |
| RSA |  |  | src/encoding.rs:68 | уязвим (Шор) | допустимо |
| RSA |  |  | src/key.rs:338 | уязвим (Шор) | допустимо |
| RSA |  |  | src/pkcs1v15/signing_key.rs:60 | уязвим (Шор) | допустимо |
| RSA |  |  | src/pss/blinded_signing_key.rs:80 | уязвим (Шор) | допустимо |
| RSA |  |  | src/pss/signing_key.rs:85 | уязвим (Шор) | допустимо |

## Приложения: Входные файлы

| Файл | Размер | SHA-256 | Маскирования |
|---|---|---|---|
| Cargo.lock | 28075 | `be3f101d792bbf2d833588100d067b54a3b53ea3a5a41461a696cd7cedb95fc8` | 0 |
| Cargo.toml | 3861 | `23b63ed294721e4771e71976af4f7306040807589ebbcb338c36eb56d1f66e20` | 0 |
| marvin-toolkit/Cargo.toml | 349 | `cb34ab4bd9ebd619db29da7dda6c1f48485836d15e8726673ba77ecc0c096bd4` | 0 |
| src/algorithms/generate.rs | 6418 | `9d4cf485bac61795cf5c96b78fea6af45ba842ea4d574dad5a4b7274191bd7d7` | 0 |
| src/algorithms/mgf.rs | 2099 | `7b337420ea5a96d9b0805e83725f6d7a7a585f03f210fcb46335c9f32ba57dd2` | 0 |
| src/algorithms/oaep.rs | 7712 | `f1b4e5f78672699465f4b91754b3cf1edd10521875c086000b0c67e27bb1fa01` | 0 |
| src/algorithms/pad.rs | 6901 | `ec20420686a242a804254cb9abd721c0a9339d1974ea6bbcbe9cfff806db2d55` | 0 |
| src/algorithms/pkcs1v15.rs | 9714 | `ffb0687c4a3a1e905dc2a59a2d70ad9ed7a82194a33277fb44a3cfa41c7d1ca4` | 0 |
| src/algorithms/pss.rs | 12066 | `e93c2e09331a441b711424675f8bc082dca18a296884b4ede067b2fb2f04f346` | 0 |
| src/algorithms/rsa.rs | 20225 | `6a455b19f5e3e25d4bdf70ec67c41678d8017fb192cb450347037cdd981ca6e8` | 0 |
| src/algorithms.rs | 968 | `d0849f47ed22ea07afb79e8cf4f1bfa6351a47f373cdb9c0d475fe33a4d4de62` | 0 |
| src/dummy_rng.rs | 608 | `aee7479544785b17942fd4800b5be942ab6313de28d9ee4f94bedd0b1f93900e` | 0 |
| src/encoding.rs | 8547 | `39ec4b355f95e45bf6822d9b4a9ab1d43d1c4b730b3c54dd5db993e8f222213e` | 0 |
| src/errors.rs | 3964 | `59eefe23b283cbdce1a2475a28be787cfe4c22aad8573adff0bc928e9dba2d3a` | 0 |
| src/hazmat.rs | 728 | `34143d40260f8da56f15d2e890acada46f02ca364dda52a1f8655643461da5f4` | 0 |
| src/key.rs | 51894 | `eeb1e8704e8643c049561837a8da28d4528513f23642f1ee3199201519049527` | 0 |
| src/lib.rs | 4832 | `b595e73a382c529d557c7ef2930828893be0d87a2f27936db5c636e06eae5728` | 1 |
| src/oaep/decrypting_key.rs | 3889 | `f9db7a3f0ec97476a1fe8ff6bceb53cf6d35bc19d82b09da91ec775cae323be9` | 0 |
| src/oaep/encrypting_key.rs | 3247 | `bb3e1352f26a56d32f0fe8ddefd54bd27bc3f5038ee4cf0609c2f0c353f6b648` | 0 |
| src/oaep.rs | 22195 | `d33b87a40ebbc0cd87b9d08f4c7d7195e1a109a8136b232c035afd22f98f63cf` | 1 |
| src/pkcs1v15/decrypting_key.rs | 2502 | `73da01e7ce18211e64f009408dfe27298377324518378ac4a0f41eb24b161258` | 0 |
| src/pkcs1v15/encrypting_key.rs | 1840 | `9dbe51d300b4026a8a97d861951bba43814c1d2aaa605b9f358e181faefcd771` | 0 |
| src/pkcs1v15/signature.rs | 2804 | `63a6870f765ac243f4c4f783596e42221bfae495406cba59dd33bf093d87c73d` | 0 |
| src/pkcs1v15/signing_key.rs | 9365 | `8cdeedb6de0749c22bd6e0bf0c07270b3bed15dde1d5c1477950579a20bbe2bf` | 0 |
| src/pkcs1v15/verifying_key.rs | 6643 | `c943c41c048c3cb0dab70bfc15b50c680577a0752cd71166197d044e33e9c781` | 0 |
| src/pkcs1v15.rs | 24525 | `560937820974e813a41eb96d0bbe49c6f4cebf838ad0795932945244edb6ebb5` | 1 |
| src/pss/blinded_signing_key.rs | 8466 | `05cb7d0e84ec7fcd64c5f091828214908d202cf47d6ca2b54c0e508c77c46cb6` | 0 |
| src/pss/signature.rs | 2780 | `543d2554a49c39b3325b6bc0493197ec9fe2c33b5ded180754b04065e48ed1fa` | 0 |
| src/pss/signing_key.rs | 9085 | `95cd495708093fa3747eda26bf0e0009e48f5a2feb46cf0c2a94203e2f2fe52f` | 0 |
| src/pss/verifying_key.rs | 6658 | `e023a2216d8e6acfb9ae104e325e7f5cd9fad1e7dbc3261e9eb2ea4dfe5cf7e2` | 0 |
| src/pss.rs | 21764 | `88537e9df026e7c4a3d343c6cd1d4dbfa4d34e035e10c411b8745f64b068f40e` | 2 |
| src/traits/encryption.rs | 1271 | `595a850d43cbf636953b4bded972558f8ee74882123e0b19128d0449c10778e2` | 0 |
| src/traits/keys.rs | 2908 | `b2d0fd9f8cc187b3fd9f96fb5c4251ee37daeabe7af6a8f37cf72c0870f4e588` | 0 |
| src/traits/padding.rs | 1634 | `1e524d6c95b7502918c32a7ca77bd83dbda1f458ba9c4976ea8a4c27ad0e105a` | 0 |
| src/traits.rs | 281 | `fdf9a94e6dc1bfe6881aa16075d05428e62ac7071a5d48127c566ddb609932f2` | 0 |
