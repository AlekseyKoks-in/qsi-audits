# Отчёт об аудите безопасности и постквантовой готовности

**Проект:** zingolib @ 81d799775f11 · Zingo Labs — публичный репозиторий (пассивная проверка)
| | |
|---|---|
| Организация | QSI |
| Дата отчёта | 2026-10-29 23:55 UTC |
| Версия отчёта | 1 |
| Запуск аудита | e29b9ffc-fd97-4146-8d14-272920d5611f (Документальный аудит) |
| Версия анализатора | qsi-engine 1.2.0 |
| Профиль риска | Криптобиржа, кастодиан или кошелёк |
| SHA-256 содержимого | `b483913c63ed4f898763dd5a8af350e3d6f7242566bb78c10722ddaaaaa3ce49` |
| Ключ подписи (Ed25519, отпечаток SHA-256; подпись — отдельный файл report.sig.json) | `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e` |
> Отчёт содержит результаты автоматизированного и документального анализа в указанных границах. Он не является юридическим заключением, сертификацией или подтверждением соответствия какому-либо стандарту.

## 1. Резюме для руководства

- Критическая: **0**
- Высокая: **2**
- Средняя: **8**
- Низкая: **31**
- Информационная: **11**

- Подтверждённая техническая уязвимость: 0
- Известная уязвимая версия компонента: 41
- Подтверждённая ошибка конфигурации: 0
- Потенциальный криптографический риск: 0
- Долгосрочный постквантовый риск: 2
- Рекомендация по улучшению: 9
- Недостаточность данных: 0

Неравенство Моски (x + y > z): x = 10, y = 5, z = 8 → при этом сценарии миграция завершится слишком поздно. _z — плановое допущение профиля риска, а не прогноз. Публично известного криптографически значимого квантового компьютера сегодня не существует._

**Постквантовая зрелость: Уровень 4 из 4 — постквантовое по умолчанию в критичных путях.** Следующий шаг: Поддерживайте инвентарь в актуальном состоянии и проверяйте новые пути кода перед выпуском.

## 2. Область и границы проверки

Режим: Документальный аудит

Репозиторий: <https://github.com/zingolabs/zingolib> @ `81d799775f11e882896e8710e8af12d6d4d29a41` — ссылки в доказательствах открывают строки на этом коммите.

205 файлов, всего 4410510 байт, редактирований: 0; список SHA-256 по файлам — в приложении C.

## 3. Методология

| Область | Статус | Количество | Примеры |
|---|---|---|---|
| dependencies | проверено | 19 | Cargo.lock: 964 dependencies parsed (964 pinned); Cargo.toml: 79 dependencies parsed (7 pinned); bindings/pin/package.json: 0 dependencies parsed (0 pinned) |
| source_code | проверено | 185 | bindings/android/build.gradle.kts: 171 lines scanned with 16 rule patterns and 128 registry patterns; bindings/android/settings.gradle.kts: 16 lines scanned with 16 rule patterns and 128 registry patterns; bindings/pin/bin/fetch_binding_layer.mjs: 30 lines scanned with 16 rule patterns and 128 registry patterns |
| tls_code | проверено | 5 | tools/workbench/src/lib.rs: TLS key-exchange settings read; zingo-netutils/src/crypto.rs: TLS key-exchange settings read; zingo-netutils/src/lib.rs: TLS key-exchange settings read |
| osv_advisories | проверено | 1 | 970 pinned packages queried at OSV.dev; 30 affected (1 of them only in development or build dependencies) |

_Длинные списки здесь сгруппированы; полный список по файлам — в JSON-версии отчёта, подписанной тем же ключом._

## 4. Проверенные и непроверенные активы

- Нет

## 5. Краткое описание архитектуры

Static review of the source tree zingolib at 81d799775f11e882896e8710e8af12d6d4d29a41. 205 files analysed; of 550 files, 131 are test, fuzzing, benchmark or example code and were left out, 214 are not read by any analyzer, 0 exceed the per-file limit and 0 did not fit the total limit. Files no analyzer reads include: .agents/claude.md, .config/nextest.toml, .dupes-ignore.toml, .editorconfig, .env.testing-artifacts. 65 files in build-output or dependency-cache directories (.git, .hg, .venv, __pycache__, build, dist, node_modules, target, vendor, venv) were not read. 4 files come from directories a .gitmodules pins and are read as shipped source rather than skipped as a dependency cache: docs/adr (4). No requests were sent to the owner's systems.

## 6. Общая оценка состояния безопасности

- Ориентировочный индекс состояния: **15** / 100 — _Рассчитан по находкам в области проверки (подтверждённые и потенциальные проблемы, взвешенные по серьёзности). Ориентировочный; не сравним между аудитами с разной областью._
- Доля квантово-уязвимых элементов инвентаризации: 3.5%

## 7. Подробное описание находок

### QSI-2026-07465 — pulldown-cmark 0.13.4 затронут RUSTSEC-2026-0414

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/pulldown-cmark@0.13.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:55 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает RUSTSEC-2026-0414 для пакета crates.io pulldown-cmark версии 0.13.4: Exponential event growth with `ENABLE_WIKILINKS`. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0414
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0414](https://osv.dev/vulnerability/RUSTSEC-2026-0414) · manifest · SHA-256 343be7fb95a60e6a1948d8a825851b2de50cac880d8b07346f31d8519aaffa63_

```
{"id": "RUSTSEC-2026-0414", "aliases": [], "modified": "2026-10-28T09:00:02.341043798Z", "summary": "Exponential event growth with `ENABLE_WIKILINKS`", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.13.5).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-07475 — rustls-webpki 0.101.7 затронут GHSA-82j2-j2ch-gfr8 (CVE-2026-93599, RUSTSEC-2026-0104)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/rustls-webpki@0.101.7`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:55 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-82j2-j2ch-gfr8 (CVE-2026-93599, RUSTSEC-2026-0104) для пакета crates.io rustls-webpki версии 0.101.7: rustls-webpki: Denial of service via panic on malformed CRL BIT STRING. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-82j2-j2ch-gfr8
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-82j2-j2ch-gfr8](https://osv.dev/vulnerability/GHSA-82j2-j2ch-gfr8) · manifest · SHA-256 a2f685e85eb5c808cb9d2de44620be02b2f87b43da592ad8769d4abeedddf3f4_

```
{"id": "GHSA-82j2-j2ch-gfr8", "aliases": ["CVE-2026-93599", "RUSTSEC-2026-0104"], "modified": "2026-09-19T03:55:33.412079637Z", "summary": "rustls-webpki: Denial of service via panic on malformed CRL BIT STRING", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.103.13, 0.104.0-alpha.7).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-07467 — rustls 0.21.12 затронут GHSA-c8m5-c952-6cm4 (RUSTSEC-2026-0346)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:crates.io/rustls@0.21.12`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:55 UTC
- Балл приоритета: 44.2 / 100
- CVSS v3.1: 4.0 (`CVSS:3.1/AV:L/AC:H/PR:H/UI:R/S:U/C:H/I:N/A:N`)

OSV.dev сообщает GHSA-c8m5-c952-6cm4 (RUSTSEC-2026-0346) для пакета crates.io rustls версии 0.21.12: Rustls: Session Debug formatting exposes TLS master secrets and resumption PSKs. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

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

### QSI-2026-07470 — rustls 0.23.43 затронут GHSA-2mjx-qc3c-rqvc (RUSTSEC-2026-0285)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:crates.io/rustls@0.23.43`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:55 UTC
- Балл приоритета: 44.2 / 100
- CVSS v3.1: 5.3 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N`)

OSV.dev сообщает GHSA-2mjx-qc3c-rqvc (RUSTSEC-2026-0285) для пакета crates.io rustls версии 0.23.43: Rustls: TLS 1.3 handshake messages incorrectly accepted across encryption level boundaries. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-2mjx-qc3c-rqvc
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-2mjx-qc3c-rqvc](https://osv.dev/vulnerability/GHSA-2mjx-qc3c-rqvc) · manifest · SHA-256 2eb1b68fbcd85e31dc42c55fbc2a260702f6c3eba28f968b13b8aeb647b6e134_

```
{"id": "GHSA-2mjx-qc3c-rqvc", "aliases": ["RUSTSEC-2026-0285"], "modified": "2026-10-27T15:30:05.509305490Z", "summary": "Rustls: TLS 1.3 handshake messages incorrectly accepted across encryption level boundaries", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.23.45).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-07471 — rustls 0.23.43 затронут GHSA-c8m5-c952-6cm4 (RUSTSEC-2026-0346)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:crates.io/rustls@0.23.43`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:55 UTC
- Балл приоритета: 44.2 / 100
- CVSS v3.1: 4.0 (`CVSS:3.1/AV:L/AC:H/PR:H/UI:R/S:U/C:H/I:N/A:N`)

OSV.dev сообщает GHSA-c8m5-c952-6cm4 (RUSTSEC-2026-0346) для пакета crates.io rustls версии 0.23.43: Rustls: Session Debug formatting exposes TLS master secrets and resumption PSKs. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

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

### QSI-2026-07449 — Квантово-уязвимый Pedersen commitment: пороговая подпись и протоколы MPC (2 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `source-code:Pedersen commitment:threshold_mpc`
- Источник данных: pepper-sync/src/scan/transactions.rs
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-29 23:55 UTC
- Балл приоритета: 35.6 / 100
- CVSS v3.1: неприменимо

7 упоминаний Pedersen commitment в 2 файл(ах), например pepper-sync/src/scan/transactions.rs:51. Роль по путям, именам функций и соседнему коду: пороговая подпись и протоколы MPC. Paillier, обязательства Педерсена и доказательства на дискретном логарифме внутри пороговых ECDSA и EdDSA ломаются алгоритмом Шора; постквантовая пороговая схема — это смена протокола, а не параметра.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте pepper-sync/src/scan/transactions.rs:51 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [pepper-sync/src/scan/transactions.rs](https://github.com/zingolabs/zingolib/blob/81d799775f11e882896e8710e8af12d6d4d29a41/pepper-sync/src/scan/transactions.rs#L51) · line 51 · SHA-256 409d382bdc6c2d5140bad1c9c6066561c0f2e563877a332af95d5399516930f6_

```
   50 | 
   51 |     fn value_commitment(&self) -> D::ValueCommitment;
   52 | }
```

_file_excerpt · [pepper-sync/src/scan/transactions.rs](https://github.com/zingolabs/zingolib/blob/81d799775f11e882896e8710e8af12d6d4d29a41/pepper-sync/src/scan/transactions.rs#L59) · line 59 · SHA-256 24d1d5ac2c08de69150089fcb84211eb9aa85803fe034c46c738764521f7262c_

```
   58 | 
   59 |     fn value_commitment(&self) -> <OrchardDomain as Domain>::ValueCommitment {
   60 |         self.cv_net().clone()
```

_file_excerpt · [pepper-sync/src/scan/transactions.rs](https://github.com/zingolabs/zingolib/blob/81d799775f11e882896e8710e8af12d6d4d29a41/pepper-sync/src/scan/transactions.rs#L69) · line 69 · SHA-256 81d93edd8517873aa4686c7258bbbeff2c9965c4a5b87761dcfcb1130d62c4b1_

```
   68 | 
   69 |     fn value_commitment(&self) -> <IronwoodDomain as Domain>::ValueCommitment {
   70 |         self.cv_net().clone()
```

_file_excerpt · [zingolib/src/wallet/utils.rs](https://github.com/zingolabs/zingolib/blob/81d799775f11e882896e8710e8af12d6d4d29a41/zingolib/src/wallet/utils.rs#L122) · line 122 · SHA-256 2707de40479b753d39f7461e82d4a25ed7cb396560849e8e9d814d5897a8d8fb_

```
  121 |         alpha: jubjub::Fr,
  122 |         rcv: sapling_value::ValueCommitTrapdoor,
  123 |         anchor: jubjub::Fq,
```

_file_excerpt · [zingolib/src/wallet/utils.rs](https://github.com/zingolabs/zingolib/blob/81d799775f11e882896e8710e8af12d6d4d29a41/zingolib/src/wallet/utils.rs#L160) · line 160 · SHA-256 59f54835e4ded0aa21021c517a84089caac6930596077cea78796e72dc88bdf8_

```
  159 |         value: sapling_value::NoteValue,
  160 |         rcv: sapling_value::ValueCommitTrapdoor,
  161 |     ) -> sapling_circuit::Output {
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Отслеживайте постквантовые пороговые подписи (NIST IR 8214C) и держите слой протоколов готовым к замене схемы подписи; зафиксируйте, сколько должны жить ключи и доли.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-07450 — Квантово-уязвимый ECDSA: подпись транзакций и сообщений (1 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `source-code:ECDSA:transaction_signing`
- Источник данных: zingolib/src/wallet/keys/legacy/extended_transparent.rs
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-29 23:55 UTC
- Балл приоритета: 35.6 / 100
- CVSS v3.1: неприменимо

2 упоминаний ECDSA в 1 файл(ах), например zingolib/src/wallet/keys/legacy/extended_transparent.rs:50. Роль по путям, именам функций и соседнему коду: подпись транзакций и сообщений. CRQC восстанавливает закрытый ключ по уже известному открытому (в блокчейне после первой траты, при повторном использовании адреса): средствам и подтверждениям под этими ключами нужен путь миграции.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте zingolib/src/wallet/keys/legacy/extended_transparent.rs:50 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [zingolib/src/wallet/keys/legacy/extended_transparent.rs](https://github.com/zingolabs/zingolib/blob/81d799775f11e882896e8710e8af12d6d4d29a41/zingolib/src/wallet/keys/legacy/extended_transparent.rs#L50) · line 50 · SHA-256 023976ff01c852e69536cca81fad78d6b07d62ff52288dd8f98119e4ac4d0f9b_

```
   49 | 
   50 |     const INVALID: &'static str = "legacy transparent secret key is not a valid secp256k1 scalar";
   51 | 
```

_file_excerpt · [zingolib/src/wallet/keys/legacy/extended_transparent.rs](https://github.com/zingolabs/zingolib/blob/81d799775f11e882896e8710e8af12d6d4d29a41/zingolib/src/wallet/keys/legacy/extended_transparent.rs#L83) · line 83 · SHA-256 124d40d49edcc5b14380dc7b4f61b667dd341bf43732ba96ed595fe71e0b3b68_

```
   82 |     const INVALID: &'static str =
   83 |         "legacy transparent public key is not a compressed secp256k1 point";
   84 | 
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Следите за постквантовыми планами каждой сети, не используйте открытые ключи повторно и держите подписание готовым к постквантовым схемам по мере их принятия сетями.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-07453 — block-buffer 0.9.0 затронут GHSA-qwgh-2vcv-g2f7

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/block-buffer@0.9.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:55 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-qwgh-2vcv-g2f7 для пакета crates.io block-buffer версии 0.9.0: block_buffer: panic corrupts inline buffer position. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

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

### QSI-2026-07454 — block-buffer 0.10.4 затронут GHSA-qwgh-2vcv-g2f7

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/block-buffer@0.10.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:55 UTC
- Балл приоритета: 33.1 / 100
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

### QSI-2026-07466 — rsa 0.9.10 затронут RUSTSEC-2023-0071 (CVE-2023-49092)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/rsa@0.9.10`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:55 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: 5.9 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:N/A:N`)

OSV.dev сообщает RUSTSEC-2023-0071 (CVE-2023-49092) для пакета crates.io rsa версии 0.9.10: Marvin Attack: potential key recovery through timing sidechannels. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2023-0071
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2023-0071](https://osv.dev/vulnerability/RUSTSEC-2023-0071) · manifest · SHA-256 6fcc27a80e8a30342b68a229087947db7a952d0facf3cc8d6edbd7abfd150c53_

```
{"id": "RUSTSEC-2023-0071", "aliases": ["CVE-2023-49092", "GHSA-4grx-2x9w-596c", "GHSA-c38w-74pg-36hr"], "modified": "2026-09-14T09:45:02.996132556Z", "summary": "Marvin Attack: potential key recovery through timing sidechannels", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:N/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (пока не выпущена; меры смягчения — в бюллетене).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-07468 — rustls 0.21.12 затронут GHSA-h2v8-394m-p7vv

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:crates.io/rustls@0.21.12`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:55 UTC
- Балл приоритета: 39.2 / 100
- CVSS v3.1: 3.7 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:N/A:L`)

OSV.dev сообщает GHSA-h2v8-394m-p7vv для пакета crates.io rustls версии 0.21.12: Rustls: Brotli certificate decompression can allocate an attacker-controlled amount of memory up to 1 GiB before authentication. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

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

### QSI-2026-07469 — rustls 0.21.12 затронут GHSA-w44r-93j7-qv28 (RUSTSEC-2026-0349)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:crates.io/rustls@0.21.12`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:55 UTC
- Балл приоритета: 39.2 / 100
- CVSS v3.1: 3.7 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N`)

OSV.dev сообщает GHSA-w44r-93j7-qv28 (RUSTSEC-2026-0349) для пакета crates.io rustls версии 0.21.12: rustls: An unauthenticated ServerHello poisons the per-name key-exchange record, so later ClientHellos carry only a classical X25519 share. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

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

### QSI-2026-07473 — rustls 0.23.43 затронут GHSA-w44r-93j7-qv28 (RUSTSEC-2026-0349)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:crates.io/rustls@0.23.43`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:55 UTC
- Балл приоритета: 39.2 / 100
- CVSS v3.1: 3.7 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N`)

OSV.dev сообщает GHSA-w44r-93j7-qv28 (RUSTSEC-2026-0349) для пакета crates.io rustls версии 0.23.43: rustls: An unauthenticated ServerHello poisons the per-name key-exchange record, so later ClientHellos carry only a classical X25519 share. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

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

### QSI-2026-07476 — rustls-webpki 0.101.7 затронут GHSA-965h-392x-2mh5 (CVE-2026-93600, RUSTSEC-2026-0098)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/rustls-webpki@0.101.7`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:55 UTC
- Балл приоритета: 29.4 / 100
- CVSS v3.1: 2.2 (`CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:U/C:N/I:L/A:N`)

OSV.dev сообщает GHSA-965h-392x-2mh5 (CVE-2026-93600, RUSTSEC-2026-0098) для пакета crates.io rustls-webpki версии 0.101.7: webpki: Name constraints for URI names were incorrectly accepted. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-965h-392x-2mh5
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-965h-392x-2mh5](https://osv.dev/vulnerability/GHSA-965h-392x-2mh5) · manifest · SHA-256 7dfbf39859f726382fb5bacff8569cd96b6823e01f426668833099ff6d756657_

```
{"id": "GHSA-965h-392x-2mh5", "aliases": ["CVE-2026-93600", "RUSTSEC-2026-0098"], "modified": "2026-09-19T03:55:32.245575348Z", "summary": "webpki: Name constraints for URI names were incorrectly accepted", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:U/C:N/I:L/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.103.12, 0.104.0-alpha.6).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-07477 — rustls-webpki 0.101.7 затронут GHSA-xgp8-3hg3-c2mh (CVE-2026-93601, RUSTSEC-2026-0099)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/rustls-webpki@0.101.7`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:55 UTC
- Балл приоритета: 29.4 / 100
- CVSS v3.1: 2.2 (`CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:U/C:N/I:L/A:N`)

OSV.dev сообщает GHSA-xgp8-3hg3-c2mh (CVE-2026-93601, RUSTSEC-2026-0099) для пакета crates.io rustls-webpki версии 0.101.7: webpki: Name constraints were accepted for certificates asserting a wildcard name. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-xgp8-3hg3-c2mh
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-xgp8-3hg3-c2mh](https://osv.dev/vulnerability/GHSA-xgp8-3hg3-c2mh) · manifest · SHA-256 c068ea92e7b545b187eef89198d9b7ef2f675512c425f0664366565735f890b6_

```
{"id": "GHSA-xgp8-3hg3-c2mh", "aliases": ["CVE-2026-93601", "RUSTSEC-2026-0099"], "modified": "2026-09-19T03:55:49.146112754Z", "summary": "webpki: Name constraints were accepted for certificates asserting a wildcard name", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:U/C:N/I:L/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.103.12, 0.104.0-alpha.6).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-07455 — crypto-bigint 0.5.5 затронут RUSTSEC-2026-0387 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/crypto-bigint@0.5.5`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:55 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0387 для пакета crates.io crypto-bigint версии 0.5.5: Multiple timing variability issues in operations intended to be constant-time. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

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

### QSI-2026-07456 — ctutils 0.4.3 затронут RUSTSEC-2026-0385 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/ctutils@0.4.3`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:55 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0385 для пакета crates.io ctutils версии 0.4.3: Non-constant-time mask generation and `u128` comparisons. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

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

### QSI-2026-07458 — h2 0.3.27 затронут RUSTSEC-2026-0258 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/h2@0.3.27`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:55 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0258 для пакета crates.io h2 версии 0.3.27: h2 unbounded empty DATA frames. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0258
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0258](https://osv.dev/vulnerability/RUSTSEC-2026-0258) · manifest · SHA-256 d8694780e4da4b8ee995c62dbd89ea4aef9579bf2c51b2a4b677a2231b8d4edc_

```
{"id": "RUSTSEC-2026-0258", "aliases": ["GHSA-q83h-524g-xf6h"], "modified": "2026-10-12T18:00:10.934581734Z", "summary": "h2 unbounded empty DATA frames", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.4.16).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-07459 — h2 0.4.15 затронут RUSTSEC-2026-0258 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/h2@0.4.15`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:55 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0258 для пакета crates.io h2 версии 0.4.15: h2 unbounded empty DATA frames. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0258
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0258](https://osv.dev/vulnerability/RUSTSEC-2026-0258) · manifest · SHA-256 d8694780e4da4b8ee995c62dbd89ea4aef9579bf2c51b2a4b677a2231b8d4edc_

```
{"id": "RUSTSEC-2026-0258", "aliases": ["GHSA-q83h-524g-xf6h"], "modified": "2026-10-12T18:00:10.934581734Z", "summary": "h2 unbounded empty DATA frames", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.4.16).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-07461 — libcrux-kem 0.0.9 затронут RUSTSEC-2026-0330 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/libcrux-kem@0.0.9`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:55 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0330 для пакета crates.io libcrux-kem версии 0.0.9: Hybrid Encapsulation from Seed Panics on Short Seed. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Проверенный код не упоминает затронутые функции (libcrux_kem::PublicKey::encapsulate_derand); libcrux-kem приходит через другие зависимости, которые могут их вызывать.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0330
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0330](https://osv.dev/vulnerability/RUSTSEC-2026-0330) · manifest · SHA-256 cdf7c6ad5bb4674c9f7444fd7acd0e77e02cb826ee0a8fa27d1ab17ed4781c9b_

```
{"id": "RUSTSEC-2026-0330", "aliases": [], "modified": "2026-10-07T08:30:02.862241231Z", "summary": "Hybrid Encapsulation from Seed Panics on Short Seed", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:L/AC:L/AT:P/PR:H/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.0.10).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-07462 — libcrux-kem 0.0.9 затронут RUSTSEC-2026-0331 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/libcrux-kem@0.0.9`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:55 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0331 для пакета crates.io libcrux-kem версии 0.0.9: Panic on Decoding Short Hybrid Keys. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Проверенный код не упоминает затронутые функции (libcrux_kem::PrivateKey::decode, libcrux_kem::PublicKey::decode); libcrux-kem приходит через другие зависимости, которые могут их вызывать.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0331
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0331](https://osv.dev/vulnerability/RUSTSEC-2026-0331) · manifest · SHA-256 300dc3afabe412104fa3172250d8fe302eb1838b7665eeb35a4ac1e61673f61c_

```
{"id": "RUSTSEC-2026-0331", "aliases": [], "modified": "2026-10-07T08:30:02.870588917Z", "summary": "Panic on Decoding Short Hybrid Keys", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.0.10).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-07478 — rustls-webpki 0.101.7 затронут RUSTSEC-2026-0382 (CVE-2026-111943) (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/rustls-webpki@0.101.7`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:55 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0382 (CVE-2026-111943) для пакета crates.io rustls-webpki версии 0.101.7: Certificate verification may accept distrusted intermediates. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0382
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0382](https://osv.dev/vulnerability/RUSTSEC-2026-0382) · manifest · SHA-256 4c972eb1d77abf0d1c39f2b402c5fea32a5dacf7dbbeac638e7549ce780805d1_

```
{"id": "RUSTSEC-2026-0382", "aliases": ["BIT-golang-2026-111943", "CVE-2026-111943", "GO-2026-6809", "RUSTSEC-2026-0381", "RUSTSEC-2026-0383"], "modified": "2026-10-29T10:55:54.096394276Z", "summary": "Certificate verification may accept distrusted intermediates", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.103.16, 0.104.0-alpha.8).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-07479 — rustls-webpki 0.103.13 затронут RUSTSEC-2026-0382 (CVE-2026-111943) (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/rustls-webpki@0.103.13`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:55 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0382 (CVE-2026-111943) для пакета crates.io rustls-webpki версии 0.103.13: Certificate verification may accept distrusted intermediates. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0382
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0382](https://osv.dev/vulnerability/RUSTSEC-2026-0382) · manifest · SHA-256 4c972eb1d77abf0d1c39f2b402c5fea32a5dacf7dbbeac638e7549ce780805d1_

```
{"id": "RUSTSEC-2026-0382", "aliases": ["BIT-golang-2026-111943", "CVE-2026-111943", "GO-2026-6809", "RUSTSEC-2026-0381", "RUSTSEC-2026-0383"], "modified": "2026-10-29T10:55:54.096394276Z", "summary": "Certificate verification may accept distrusted intermediates", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.103.16, 0.104.0-alpha.8).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-07482 — webpki-root-certs 1.0.9 затронут RUSTSEC-2026-0383 (CVE-2026-111943) (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/webpki-root-certs@1.0.9`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:55 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0383 (CVE-2026-111943) для пакета crates.io webpki-root-certs версии 1.0.9: Bundled root certificates allow trust in distrusted emSign intermediates. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0383
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0383](https://osv.dev/vulnerability/RUSTSEC-2026-0383) · manifest · SHA-256 42d7c64046711e787b8b00e03aacfbe617175f84da228dc8a3413bd6c9dc27aa_

```
{"id": "RUSTSEC-2026-0383", "aliases": ["BIT-golang-2026-111943", "CVE-2026-111943", "GO-2026-6809", "RUSTSEC-2026-0381", "RUSTSEC-2026-0382"], "modified": "2026-10-29T10:55:54.096394276Z", "summary": "Bundled root certificates allow trust in distrusted emSign intermediates", "severity": null, "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.26.11, 1.0.10).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-07483 — webpki-roots 0.24.0 затронут RUSTSEC-2026-0381 (CVE-2026-111943) (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/webpki-roots@0.24.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:55 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0381 (CVE-2026-111943) для пакета crates.io webpki-roots версии 0.24.0: Bundled root certificates allow trust in distrusted emSign intermediates. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0381
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0381](https://osv.dev/vulnerability/RUSTSEC-2026-0381) · manifest · SHA-256 fe0730fa87c619c62bf0bee198d2f7f275186863690454c8ae7e45848f4db031_

```
{"id": "RUSTSEC-2026-0381", "aliases": ["BIT-golang-2026-111943", "CVE-2026-111943", "GO-2026-6809", "RUSTSEC-2026-0382", "RUSTSEC-2026-0383"], "modified": "2026-10-29T10:55:54.096394276Z", "summary": "Bundled root certificates allow trust in distrusted emSign intermediates", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.26.11, 1.0.10).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-07484 — webpki-roots 0.25.4 затронут RUSTSEC-2026-0381 (CVE-2026-111943) (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/webpki-roots@0.25.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:55 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0381 (CVE-2026-111943) для пакета crates.io webpki-roots версии 0.25.4: Bundled root certificates allow trust in distrusted emSign intermediates. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0381
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0381](https://osv.dev/vulnerability/RUSTSEC-2026-0381) · manifest · SHA-256 fe0730fa87c619c62bf0bee198d2f7f275186863690454c8ae7e45848f4db031_

```
{"id": "RUSTSEC-2026-0381", "aliases": ["BIT-golang-2026-111943", "CVE-2026-111943", "GO-2026-6809", "RUSTSEC-2026-0382", "RUSTSEC-2026-0383"], "modified": "2026-10-29T10:55:54.096394276Z", "summary": "Bundled root certificates allow trust in distrusted emSign intermediates", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.26.11, 1.0.10).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-07485 — webpki-roots 1.0.9 затронут RUSTSEC-2026-0381 (CVE-2026-111943) (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/webpki-roots@1.0.9`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:55 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0381 (CVE-2026-111943) для пакета crates.io webpki-roots версии 1.0.9: Bundled root certificates allow trust in distrusted emSign intermediates. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0381
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0381](https://osv.dev/vulnerability/RUSTSEC-2026-0381) · manifest · SHA-256 fe0730fa87c619c62bf0bee198d2f7f275186863690454c8ae7e45848f4db031_

```
{"id": "RUSTSEC-2026-0381", "aliases": ["BIT-golang-2026-111943", "CVE-2026-111943", "GO-2026-6809", "RUSTSEC-2026-0382", "RUSTSEC-2026-0383"], "modified": "2026-10-29T10:55:54.096394276Z", "summary": "Bundled root certificates allow trust in distrusted emSign intermediates", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.26.11, 1.0.10).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-07486 — zstd 0.14.2 затронут RUSTSEC-2026-0391 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/zstd@0.14.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:55 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0391 для пакета crates.io zstd версии 0.14.2: Data from an abandoned stream leaks into the next stream on a reused context. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Проверенный код не упоминает затронутые функции (zstd::stream::raw::Decoder::with_context, zstd::stream::raw::Encoder::with_context); zstd приходит через другие зависимости, которые могут их вызывать.

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

### QSI-2026-07487 — zstd-safe 8.1.0 затронут RUSTSEC-2026-0395 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/zstd-safe@8.1.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:55 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0395 для пакета crates.io zstd-safe версии 8.1.0: Use-after-free with `CParameter::StableInBuffer`. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Проверенный код не упоминает затронутые функции (zstd_safe::CCtx::set_parameter); zstd-safe приходит через другие зависимости, которые могут их вызывать.

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

### QSI-2026-07488 — zstd-safe 8.1.0 затронут RUSTSEC-2026-0396 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/zstd-safe@8.1.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:55 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0396 для пакета crates.io zstd-safe версии 8.1.0: `Seekable` reads a NULL or out-of-bounds seek table. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Проверенный код не упоминает затронутые функции (zstd_safe::seekable::SeekTable::frame_decompressed_size, zstd_safe::seekable::Seekable::decompress, zstd_safe::seekable::Seekable::decompress_frame, zstd_safe::seekable::Seekable::frame_decompressed_size, zstd_safe::seekable::Seekable::offset_to_frame_index); zstd-safe приходит через другие зависимости, которые могут их вызывать.

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

### QSI-2026-07489 — zstd-safe 8.1.0 затронут RUSTSEC-2026-0397 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/zstd-safe@8.1.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:55 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0397 для пакета crates.io zstd-safe версии 8.1.0: `OutBuffer::around_pos` exposes uninitialized memory. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Проверенный код не упоминает затронутые функции (zstd_safe::OutBuffer::around_pos); zstd-safe приходит через другие зависимости, которые могут их вызывать.

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

### QSI-2026-07490 — zstd-safe 8.1.0 затронут RUSTSEC-2026-0398 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/zstd-safe@8.1.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:55 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0398 для пакета crates.io zstd-safe версии 8.1.0: `Seekable::decompress` sets a `Vec` length beyond its capacity for offsets past the end. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Проверенный код не упоминает затронутые функции (zstd_safe::seekable::AdvancedSeekable::decompress, zstd_safe::seekable::Seekable::decompress); zstd-safe приходит через другие зависимости, которые могут их вызывать.

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

### QSI-2026-07491 — zstd-safe 8.1.0 затронут RUSTSEC-2026-0399 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/zstd-safe@8.1.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:55 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0399 для пакета crates.io zstd-safe версии 8.1.0: Use-after-free through `init_using_cdict` and `init_using_ddict`. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Проверенный код не упоминает затронутые функции (zstd_safe::CCtx::init_using_cdict, zstd_safe::DCtx::init_using_ddict); zstd-safe приходит через другие зависимости, которые могут их вызывать.

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

### QSI-2026-07492 — zstd-safe 8.1.0 затронут RUSTSEC-2026-0400 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/zstd-safe@8.1.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:55 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0400 для пакета crates.io zstd-safe версии 8.1.0: Use-after-free of a dictionary after a one-shot call on a context with an open stream. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Проверенный код не упоминает затронутые функции (zstd_safe::DCtx::decompress, zstd_safe::DCtx::decompress_using_ddict, zstd_safe::DCtx::decompress_using_dict); zstd-safe приходит через другие зависимости, которые могут их вызывать.

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

### QSI-2026-07493 — zstd-safe 8.1.0 затронут RUSTSEC-2026-0401 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/zstd-safe@8.1.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:55 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0401 для пакета crates.io zstd-safe версии 8.1.0: Out-of-bounds read in `train_from_buffer` when sample sizes overflow. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Проверенный код не упоминает затронутые функции (zstd_safe::train_from_buffer); zstd-safe приходит через другие зависимости, которые могут их вызывать.

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

### QSI-2026-07494 — zstd-safe 8.1.0 затронут RUSTSEC-2026-0402 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/zstd-safe@8.1.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:55 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0402 для пакета crates.io zstd-safe версии 8.1.0: Heap buffer overflow in `CCtx::try_clone` on a multithreaded context. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Проверенный код не упоминает затронутые функции (zstd_safe::CCtx::try_clone); zstd-safe приходит через другие зависимости, которые могут их вызывать.

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

### QSI-2026-07495 — zstd-safe 8.1.0 затронут RUSTSEC-2026-0403 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/zstd-safe@8.1.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:55 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0403 для пакета crates.io zstd-safe версии 8.1.0: Uninitialized memory exposed when streaming decompression of a legacy frame fails. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Проверенный код не упоминает затронутые функции (zstd_safe::DCtx::decompress_stream); zstd-safe приходит через другие зависимости, которые могут их вызывать.

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

### QSI-2026-07496 — zstd-safe 8.1.0 затронут RUSTSEC-2026-0404 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/zstd-safe@8.1.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:55 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0404 для пакета crates.io zstd-safe версии 8.1.0: Double free in `DCtx::try_clone`. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Проверенный код не упоминает затронутые функции (zstd_safe::DCtx::try_clone); zstd-safe приходит через другие зависимости, которые могут их вызывать.

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

### QSI-2026-07497 — zstd-safe 8.1.0 затронут RUSTSEC-2026-0405 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/zstd-safe@8.1.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:55 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0405 для пакета crates.io zstd-safe версии 8.1.0: Out-of-bounds read with an out-of-range `InBuffer::pos`. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Проверенный код не упоминает затронутые функции (zstd_safe::seekable::SeekableCStream::compress_stream); zstd-safe приходит через другие зависимости, которые могут их вызывать.

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

### QSI-2026-07498 — zstd-safe 8.1.0 затронут RUSTSEC-2026-0406 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/zstd-safe@8.1.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:55 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0406 для пакета crates.io zstd-safe версии 8.1.0: Use-after-free when changing a multithreaded context with an unfinished frame. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Проверенный код не упоминает затронутые функции (zstd_safe::CCtx::disable_dictionary, zstd_safe::CCtx::init, zstd_safe::CCtx::load_dictionary, zstd_safe::CCtx::ref_cdict, zstd_safe::CCtx::ref_prefix, zstd_safe::CCtx::reset …); zstd-safe приходит через другие зависимости, которые могут их вызывать.

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

### QSI-2026-07499 — zstd-sys 2.1.1+zstd.1.5.7 затронут RUSTSEC-2026-0410 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/zstd-sys@2.1.1+zstd.1.5.7`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:55 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0410 для пакета crates.io zstd-sys версии 2.1.1+zstd.1.5.7: WebAssembly allocator shim corrupts memory on allocation failure. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Бюллетень не называет затронутых функций, поэтому достижимость не определена. Касается только целевых платформ wasm32.

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

### QSI-2026-07472 — rustls 0.23.43 затронут GHSA-h2v8-394m-p7vv (RUSTSEC-2026-0348)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/rustls@0.23.43`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:55 UTC
- Балл приоритета: 29.9 / 100
- CVSS v3.1: 3.7 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:N/A:L`)

OSV.dev сообщает GHSA-h2v8-394m-p7vv (RUSTSEC-2026-0348) для пакета crates.io rustls версии 0.23.43: Rustls: Brotli certificate decompression can allocate an attacker-controlled amount of memory up to 1 GiB before authentication. Затронутый код находится за флагом Cargo `brotli`, выключенным по умолчанию; ни один проверенный манифест его не включает — бюллетень не применим, если флаг не включает другая зависимость.

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

### QSI-2026-07460 — json 0.12.4: информационный бюллетень RUSTSEC-2022-0081 (unmaintained)

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `dependency:crates.io/json@0.12.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:55 UTC
- Балл приоритета: 19.8 / 100
- CVSS v3.1: неприменимо

OSV.dev отмечает RUSTSEC-2022-0081 для пакета crates.io json версии 0.12.4 как информационный (unmaintained): json is unmaintained. Уязвимости в нём нет; неподдерживаемый пакет не получит исправлений будущих уязвимостей.

**Возможные последствия.** Известной уязвимости нет. Исправления безопасности в будущем могут не выйти.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2022-0081
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2022-0081](https://osv.dev/vulnerability/RUSTSEC-2022-0081) · manifest · SHA-256 170faf33f171c78abb49dbab7d9b9ebdf4897294fc8ad906f15a805818da1f7e_

```
{"id": "RUSTSEC-2022-0081", "aliases": [], "modified": "2023-08-25T17:52:15Z", "summary": "json is unmaintained", "severity": null, "declared_in_manifest": true}
```

**Ограничения проверки.** Данные получены от OSV.dev в зафиксированное время.

**Рекомендация.** Запланируйте переход на поддерживаемую альтернативу или зафиксируйте решение оставить пакет.

**Повторная проверка.** Повторите сканирование зависимостей после изменения.

### QSI-2026-07474 — rustls-pemfile 1.0.4: информационный бюллетень RUSTSEC-2025-0134 (unmaintained)

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `dependency:crates.io/rustls-pemfile@1.0.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:55 UTC
- Балл приоритета: 19.8 / 100
- CVSS v3.1: неприменимо

OSV.dev отмечает RUSTSEC-2025-0134 для пакета crates.io rustls-pemfile версии 1.0.4 как информационный (unmaintained): rustls-pemfile is unmaintained. Уязвимости в нём нет; неподдерживаемый пакет не получит исправлений будущих уязвимостей.

**Возможные последствия.** Известной уязвимости нет. Исправления безопасности в будущем могут не выйти.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2025-0134
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2025-0134](https://osv.dev/vulnerability/RUSTSEC-2025-0134) · manifest · SHA-256 3ae993a0c7d366086e5824ab9c7ec628e9d859b903e834854c0f3d2f0be64ccd_

```
{"id": "RUSTSEC-2025-0134", "aliases": [], "modified": "2025-12-05T19:07:59.622592Z", "summary": "rustls-pemfile is unmaintained", "severity": null, "declared_in_manifest": true}
```

**Ограничения проверки.** Данные получены от OSV.dev в зафиксированное время.

**Рекомендация.** Запланируйте переход на поддерживаемую альтернативу или зафиксируйте решение оставить пакет.

**Повторная проверка.** Повторите сканирование зависимостей после изменения.

### QSI-2026-07480 — tokio 1.53.1 затронут RUSTSEC-2026-0386 (без оценки серьёзности)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/tokio@1.53.1`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:55 UTC
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

### QSI-2026-07500 — 1 бюллетеней в 1 пакет(ах) crates.io, нужных только для разработки или сборки

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependencies:crates.io:non-runtime`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch по точным версиям; область применения — из devDependencies, флагов dev в package-lock.json, разделов importers в pnpm, графа Cargo.lock от таблиц Cargo.toml и — для yarn.lock, который область не записывает вовсе — графа файла блокировки, пройденного от package.json. Если рабочее требование в файле блокировки разрешить не удалось, файл остаётся без классификации, чтобы пакет не был отложен в сторону по ошибке.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:55 UTC
- Балл приоритета: 15.5 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает 1 бюллетеней (0 с оценкой high или critical) для 1 пакет(ов) crates.io, которые подтягивают только инструменты разработки или сборки (Cargo.lock): например, rustls-pemfile@2.2.0 [dev]: RUSTSEC-2025-0134. Манифесты помечают их так (devDependencies, "dev": true в package-lock.json, [dev-dependencies]/[build-dependencies] через граф Cargo.lock), поэтому в поставляемый продукт они не входят.

**Возможные последствия.** Пользователей продукта они не затрагивают. Они могут влиять на машины разработчиков и CI (цепочка поставки): скомпрометированный или уязвимый инструмент способен изменить сборку.

**Шаги воспроизведения.**

```
Найдите пакеты из доказательства на https://osv.dev и проверьте их область применения в Cargo.lock.
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev (crates.io)](https://osv.dev/) · Cargo.lock · SHA-256 14125f07fac0bed362d76dd69cb36dfcb49644a33f3c1f61f53ec9d6b89f73c0_

```
rustls-pemfile@2.2.0 [dev]: RUSTSEC-2025-0134
```

**Ограничения проверки.** Данные получены от OSV.dev в зафиксированное время. Области применения взяты из манифестов; собственные build-зависимости крейтов реестра в Cargo.lock не различимы, поэтому множество runtime может оказаться больше реального, но не меньше.

**Рекомендация.** Обновите инструменты в рамках планового обслуживания; в первую очередь пакеты, которые выполняются в CI с секретами или создают релизные артефакты.

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-07451 — basic-toml 0.1.10: информационный бюллетень RUSTSEC-2026-0374 (unmaintained)

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/basic-toml@0.1.10`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:55 UTC
- Балл приоритета: 11.8 / 100
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

### QSI-2026-07452 — bincode 1.3.3: информационный бюллетень RUSTSEC-2025-0141 (unmaintained)

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/bincode@1.3.3`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:55 UTC
- Балл приоритета: 11.8 / 100
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

### QSI-2026-07457 — derivative 2.2.0: информационный бюллетень RUSTSEC-2024-0388 (unmaintained)

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/derivative@2.2.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:55 UTC
- Балл приоритета: 11.8 / 100
- CVSS v3.1: неприменимо

OSV.dev отмечает RUSTSEC-2024-0388 для пакета crates.io derivative версии 2.2.0 как информационный (unmaintained): `derivative` is unmaintained; consider using an alternative. Уязвимости в нём нет; неподдерживаемый пакет не получит исправлений будущих уязвимостей.

**Возможные последствия.** Известной уязвимости нет. Исправления безопасности в будущем могут не выйти.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2024-0388
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2024-0388](https://osv.dev/vulnerability/RUSTSEC-2024-0388) · manifest · SHA-256 3438f6c3cab3309fb6388762a19097619076b18baff08e3e9ab34fa969478d55_

```
{"id": "RUSTSEC-2024-0388", "aliases": [], "modified": "2024-11-10T13:34:40Z", "summary": "`derivative` is unmaintained; consider using an alternative", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные получены от OSV.dev в зафиксированное время.

**Рекомендация.** Запланируйте переход на поддерживаемую альтернативу или зафиксируйте решение оставить пакет.

**Повторная проверка.** Повторите сканирование зависимостей после изменения.

### QSI-2026-07463 — paste 1.0.15: информационный бюллетень RUSTSEC-2024-0436 (unmaintained)

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/paste@1.0.15`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:55 UTC
- Балл приоритета: 11.8 / 100
- CVSS v3.1: неприменимо

OSV.dev отмечает RUSTSEC-2024-0436 для пакета crates.io paste версии 1.0.15 как информационный (unmaintained): paste - no longer maintained. Уязвимости в нём нет; неподдерживаемый пакет не получит исправлений будущих уязвимостей.

**Возможные последствия.** Известной уязвимости нет. Исправления безопасности в будущем могут не выйти.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2024-0436
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2024-0436](https://osv.dev/vulnerability/RUSTSEC-2024-0436) · manifest · SHA-256 ea867adb8ba26c96c3779becf55b3de25d46f37f23ab55131e09c98a8b0b9975_

```
{"id": "RUSTSEC-2024-0436", "aliases": [], "modified": "2026-01-27T22:03:15.694766Z", "summary": "paste - no longer maintained", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные получены от OSV.dev в зафиксированное время.

**Рекомендация.** Запланируйте переход на поддерживаемую альтернативу или зафиксируйте решение оставить пакет.

**Повторная проверка.** Повторите сканирование зависимостей после изменения.

### QSI-2026-07464 — proc-macro-error2 2.0.1: информационный бюллетень RUSTSEC-2026-0173 (unmaintained)

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/proc-macro-error2@2.0.1`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:55 UTC
- Балл приоритета: 11.8 / 100
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

### QSI-2026-07481 — unsafe-libyaml 0.2.11: информационный бюллетень RUSTSEC-2024-0449 (unmaintained)

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/unsafe-libyaml@0.2.11`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:55 UTC
- Балл приоритета: 11.8 / 100
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

### Постквантовая зрелость: Уровень 4 из 4 — постквантовое по умолчанию в критичных путях

- Гибрид — обмен ключами в канале (TLS, Noise, рукопожатия): Cargo.toml (классическая группа + X25519MLKEM768)
- Гибрид — обмен ключами в канале (TLS, Noise, рукопожатия): zingo-netutils/src/crypto.rs (классическая группа + X25519MLKEM768)
- Используется: X25519MLKEM768 — Cargo.toml
- Используется: X25519MLKEM768 — zingo-netutils/src/crypto.rs
- Постквантовая библиотека объявлена в зависимостях

**Следующий шаг:** Поддерживайте инвентарь в актуальном состоянии и проверяйте новые пути кода перед выпуском.

_Уровни: 0 — нет; 1 — есть, но не подключено; 2 — используется вне критичных путей; 3 — гибрид в критичном пути; 4 — постквантовое по умолчанию в критичных путях (корень доверия, обёртка ключей, обмен ключами в канале). Оценка по коду и манифестам._

### Что делают квантово-уязвимые алгоритмы

| Роль | Алгоритмы (файлы) | ID | Первый шаг |
|---|---|---|---|
| **пороговая подпись и протоколы MPC** | Pedersen commitment (2) | QSI-2026-07449 | Отслеживайте постквантовые пороговые подписи (NIST IR 8214C) и держите слой протоколов готовым к замене схемы подписи; зафиксируйте, сколько должны жить ключи и доли |
| **подпись транзакций и сообщений** | ECDSA (1) | QSI-2026-07450 | Следите за постквантовыми планами каждой сети, не используйте открытые ключи повторно и держите подписание готовым к постквантовым схемам по мере их принятия сетями |

_Роль определяется по путям файлов, именам функций и коду вокруг совпадений; проверка её подтверждает. Сначала — ключи корня доверия и обёрнутые ключи: их трудно заменить или можно записать уже сегодня._
Анкета готовности для проекта не заполнялась.

### Квантовые алгоритмы, значимые для этой инвентаризации

| Квантовый алгоритм | Действие | Модель атаки | Алгоритмы из инвентаризации (строк) | Что это значит для аудита |
|---|---|---|---|---|
| Алгоритм Шора — дискретный логарифм на эллиптических кривых | взламывает | Q1 | ECDSA (1), Pedersen commitment (2), X25519MLKEM768 (2) | Ключи на эллиптических кривых, по оценкам, падут раньше ключей RSA сопоставимой классической стойкости. В блокчейнах первыми под угрозой монеты, чей открытый ключ уже опубликован (повторно используемые адреса, выходы pay-to-public-key и Taproot); планируйте переход на постквантовые подписи и до этого избегайте повторного использования ключей. |
| Алгоритм Гровера — поиск ключа и прообразов | ослабляет (более длинные ключи восстанавливают запас) | Q1 | SHA-2 (1) | Не взлом. Ключи 256 бит (AES-256, ChaCha20) сохраняют хороший запас; AES-128 соответствует категории 1 NIST, но некоторые регуляторы требуют 256-битных ключей в квантово-устойчивых системах (см. запись AES-128). Для долгоживущих данных предпочитайте 256-битные ключи; 256-битные хеши для стойкости к прообразам менять не нужно. |
| Брассар–Хойер–Тапп — поиск коллизий | ослабляет (более длинные ключи восстанавливают запас) | Q1 | SHA-2 (1) | 256-битные хеши (SHA-256, SHA3-256) остаются достаточными по стойкости к коллизиям; 160-битные хеши слабы уже классически (коллизии SHA-1 практичны). Где нужны категории NIST 4–5, используйте хеши на 384/512 бит. |
| Квантовое решетчатое просеивание | учтено в стандартных параметрах | Q1 | X25519MLKEM768 (2) | Для ML-KEM и ML-DSA в стандартных наборах параметров ничего менять не нужно. Заявление 2024 года о полиномиальном квантовом алгоритме для LWE отозвано после обнаружения ошибки (см. заявления). |

_Действие: взламывает — алгоритм нужно заменить; ослабляет — более длинные ключи или выходы восстанавливают запас; учтено в стандартных параметрах — при стандартных наборах действий не требуется; только при суперпозиционных запросах — к обычному применению неприменимо._


## 9. Ограничения и допущения

- Отчёт содержит результаты автоматизированного и документального анализа в указанных границах. Он не является юридическим заключением, сертификацией или подтверждением соответствия какому-либо стандарту.
- z — плановое допущение профиля риска, а не прогноз. Публично известного криптографически значимого квантового компьютера сегодня не существует.

## 10. План устранения проблем / Приоритеты на 30, 60 и 90 дней

### 30 дн.

| Приоритет | ID | Действие | Тип | Условие закрытия |
|---|---|---|---|---|
| P2 | QSI-2026-07465 | Обновите pulldown-cmark до исправленной версии (0.13.5). | устранение первопричины | Сканирование зависимостей больше не сообщает RUSTSEC-2026-0414. |
| P2 | QSI-2026-07475 | Обновите rustls-webpki до исправленной версии (0.103.13, 0.104.0-alpha.7). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-82j2-j2ch-gfr8 (CVE-2026-93599, RUSTSEC-2026-0104). |
| P2 | QSI-2026-07467 | Обновите rustls до исправленной версии (0.23.46, 0.24.0-dev.2). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-c8m5-c952-6cm4 (RUSTSEC-2026-0346). |
| P2 | QSI-2026-07470 | Обновите rustls до исправленной версии (0.23.45). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-2mjx-qc3c-rqvc (RUSTSEC-2026-0285). |
| P2 | QSI-2026-07471 | Обновите rustls до исправленной версии (0.23.46, 0.24.0-dev.2). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-c8m5-c952-6cm4 (RUSTSEC-2026-0346). |
| P2 | QSI-2026-07453 | Обновите block-buffer до исправленной версии (пока не выпущена; меры смягчения — в бюллетене). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-qwgh-2vcv-g2f7. |
| P2 | QSI-2026-07454 | Обновите block-buffer до исправленной версии (пока не выпущена; меры смягчения — в бюллетене). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-qwgh-2vcv-g2f7. |
| P2 | QSI-2026-07466 | Обновите rsa до исправленной версии (пока не выпущена; меры смягчения — в бюллетене). | устранение первопричины | Сканирование зависимостей больше не сообщает RUSTSEC-2023-0071 (CVE-2023-49092). |
| P2 | QSI-2026-07468 | Обновите rustls до исправленной версии (0.23.46, 0.24.0-dev.2). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-h2v8-394m-p7vv. |
| P2 | QSI-2026-07469 | Обновите rustls до исправленной версии (0.23.46, 0.24.0-dev.2). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-w44r-93j7-qv28 (RUSTSEC-2026-0349). |
| P2 | QSI-2026-07473 | Обновите rustls до исправленной версии (0.23.46, 0.24.0-dev.2). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-w44r-93j7-qv28 (RUSTSEC-2026-0349). |
| P2 | QSI-2026-07476 | Обновите rustls-webpki до исправленной версии (0.103.12, 0.104.0-alpha.6). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-965h-392x-2mh5 (CVE-2026-93600, RUSTSEC-2026-0098). |
| P2 | QSI-2026-07477 | Обновите rustls-webpki до исправленной версии (0.103.12, 0.104.0-alpha.6). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-xgp8-3hg3-c2mh (CVE-2026-93601, RUSTSEC-2026-0099). |
| P2 | QSI-2026-07472 | Обновите rustls до исправленной версии (0.23.46, 0.24.0-dev.2). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-h2v8-394m-p7vv (RUSTSEC-2026-0348). |
### 60 дн.

| Приоритет | ID | Действие | Тип | Условие закрытия |
|---|---|---|---|---|
| P3 | QSI-2026-07455 | Разберите RUSTSEC-2026-0387; при необходимости обновите crypto-bigint до исправленной версии (0.7.6). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0387 или результат разбора записан. |
| P3 | QSI-2026-07456 | Разберите RUSTSEC-2026-0385; при необходимости обновите ctutils до исправленной версии (0.4.4). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0385 или результат разбора записан. |
| P3 | QSI-2026-07458 | Разберите RUSTSEC-2026-0258; при необходимости обновите h2 до исправленной версии (0.4.16). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0258 или результат разбора записан. |
| P3 | QSI-2026-07459 | Разберите RUSTSEC-2026-0258; при необходимости обновите h2 до исправленной версии (0.4.16). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0258 или результат разбора записан. |
| P3 | QSI-2026-07461 | Разберите RUSTSEC-2026-0330; при необходимости обновите libcrux-kem до исправленной версии (0.0.10). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0330 или результат разбора записан. |
| P3 | QSI-2026-07462 | Разберите RUSTSEC-2026-0331; при необходимости обновите libcrux-kem до исправленной версии (0.0.10). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0331 или результат разбора записан. |
| P3 | QSI-2026-07478 | Разберите RUSTSEC-2026-0382 (CVE-2026-111943); при необходимости обновите rustls-webpki до исправленной версии (0.103.16, 0.104.0-alpha.8). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0382 (CVE-2026-111943) или результат разбора записан. |
| P3 | QSI-2026-07479 | Разберите RUSTSEC-2026-0382 (CVE-2026-111943); при необходимости обновите rustls-webpki до исправленной версии (0.103.16, 0.104.0-alpha.8). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0382 (CVE-2026-111943) или результат разбора записан. |
| P3 | QSI-2026-07482 | Разберите RUSTSEC-2026-0383 (CVE-2026-111943); при необходимости обновите webpki-root-certs до исправленной версии (0.26.11, 1.0.10). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0383 (CVE-2026-111943) или результат разбора записан. |
| P3 | QSI-2026-07483 | Разберите RUSTSEC-2026-0381 (CVE-2026-111943); при необходимости обновите webpki-roots до исправленной версии (0.26.11, 1.0.10). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0381 (CVE-2026-111943) или результат разбора записан. |
| P3 | QSI-2026-07484 | Разберите RUSTSEC-2026-0381 (CVE-2026-111943); при необходимости обновите webpki-roots до исправленной версии (0.26.11, 1.0.10). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0381 (CVE-2026-111943) или результат разбора записан. |
| P3 | QSI-2026-07485 | Разберите RUSTSEC-2026-0381 (CVE-2026-111943); при необходимости обновите webpki-roots до исправленной версии (0.26.11, 1.0.10). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0381 (CVE-2026-111943) или результат разбора записан. |
| P3 | QSI-2026-07486 | Разберите RUSTSEC-2026-0391; при необходимости обновите zstd до исправленной версии (0.14.3). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0391 или результат разбора записан. |
| P3 | QSI-2026-07487 | Разберите RUSTSEC-2026-0395; при необходимости обновите zstd-safe до исправленной версии (8.2.0). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0395 или результат разбора записан. |
| P3 | QSI-2026-07488 | Разберите RUSTSEC-2026-0396; при необходимости обновите zstd-safe до исправленной версии (8.2.0). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0396 или результат разбора записан. |
| P3 | QSI-2026-07489 | Разберите RUSTSEC-2026-0397; при необходимости обновите zstd-safe до исправленной версии (8.2.0). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0397 или результат разбора записан. |
| P3 | QSI-2026-07490 | Разберите RUSTSEC-2026-0398; при необходимости обновите zstd-safe до исправленной версии (8.2.0). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0398 или результат разбора записан. |
| P3 | QSI-2026-07491 | Разберите RUSTSEC-2026-0399; при необходимости обновите zstd-safe до исправленной версии (8.2.0). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0399 или результат разбора записан. |
| P3 | QSI-2026-07492 | Разберите RUSTSEC-2026-0400; при необходимости обновите zstd-safe до исправленной версии (8.2.0). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0400 или результат разбора записан. |
| P3 | QSI-2026-07493 | Разберите RUSTSEC-2026-0401; при необходимости обновите zstd-safe до исправленной версии (8.2.0). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0401 или результат разбора записан. |
| P3 | QSI-2026-07494 | Разберите RUSTSEC-2026-0402; при необходимости обновите zstd-safe до исправленной версии (8.2.0). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0402 или результат разбора записан. |
| P3 | QSI-2026-07495 | Разберите RUSTSEC-2026-0403; при необходимости обновите zstd-safe до исправленной версии (8.2.0). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0403 или результат разбора записан. |
| P3 | QSI-2026-07496 | Разберите RUSTSEC-2026-0404; при необходимости обновите zstd-safe до исправленной версии (8.2.0). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0404 или результат разбора записан. |
| P3 | QSI-2026-07497 | Разберите RUSTSEC-2026-0405; при необходимости обновите zstd-safe до исправленной версии (8.2.0). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0405 или результат разбора записан. |
| P3 | QSI-2026-07498 | Разберите RUSTSEC-2026-0406; при необходимости обновите zstd-safe до исправленной версии (8.2.0). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0406 или результат разбора записан. |
| P3 | QSI-2026-07499 | Разберите RUSTSEC-2026-0410; при необходимости обновите zstd-sys до исправленной версии (2.1.2). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0410 или результат разбора записан. |
| P3 | QSI-2026-07480 | Разберите RUSTSEC-2026-0386; при необходимости обновите tokio до исправленной версии (1.51.6, 1.53.3). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0386 или результат разбора записан. |
### 90 дн.

| Приоритет | ID | Действие | Тип | Условие закрытия |
|---|---|---|---|---|
| P3 | QSI-2026-07449 | Внесите использования Pedersen commitment в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-07450 | Внесите использования ECDSA в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P4 | QSI-2026-07449 | Запланируйте миграцию Pedersen commitment на  (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование  или гибридной схемы. |
| P4 | QSI-2026-07450 | Запланируйте миграцию ECDSA на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема или гибридной схемы. |
| P4 | QSI-2026-07460 | Замените json поддерживаемой альтернативой или зафиксируйте, почему он остаётся. | устранение первопричины | json заменён или решение зафиксировано. |
| P4 | QSI-2026-07474 | Замените rustls-pemfile поддерживаемой альтернативой или зафиксируйте, почему он остаётся. | устранение первопричины | rustls-pemfile заменён или решение зафиксировано. |
| P4 | QSI-2026-07500 | Обновите зависимости разработки и сборки из доказательства. | устранение первопричины | Сканирование не сообщает бюллетеней для пакетов инструментов, либо оставшиеся зафиксированы. |
| P4 | QSI-2026-07451 | Замените basic-toml поддерживаемой альтернативой или зафиксируйте, почему он остаётся. | устранение первопричины | basic-toml заменён или решение зафиксировано. |
| P4 | QSI-2026-07452 | Замените bincode поддерживаемой альтернативой или зафиксируйте, почему он остаётся. | устранение первопричины | bincode заменён или решение зафиксировано. |
| P4 | QSI-2026-07457 | Замените derivative поддерживаемой альтернативой или зафиксируйте, почему он остаётся. | устранение первопричины | derivative заменён или решение зафиксировано. |
| P4 | QSI-2026-07463 | Замените paste поддерживаемой альтернативой или зафиксируйте, почему он остаётся. | устранение первопричины | paste заменён или решение зафиксировано. |
| P4 | QSI-2026-07464 | Замените proc-macro-error2 поддерживаемой альтернативой или зафиксируйте, почему он остаётся. | устранение первопричины | proc-macro-error2 заменён или решение зафиксировано. |
| P4 | QSI-2026-07481 | Замените unsafe-libyaml поддерживаемой альтернативой или зафиксируйте, почему он остаётся. | устранение первопричины | unsafe-libyaml заменён или решение зафиксировано. |

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
5. C. Zalka — Grover's quantum searching algorithm is optimal (Phys. Rev. A 60, 2746, 1999; arXiv:quant-ph/9711070) — APS. <https://doi.org/10.1103/PhysRevA.60.2746> (peer-reviewed article: optimal for any success probability; parallel search gains no more than splitting the space)
6. CRYSTALS-Kyber — Algorithm Specifications and Supporting Documentation (round 3, 2021-08-04) — CRYSTALS team. <https://pq-crystals.org/kyber/data/kyber-specification-round3-20210804.pdf> (NIST round-3 submission: core-SVP cost 2^{0.292β} classical, 2^{0.265β} quantum; Kyber768 166 quantum bits)
7. Common Vulnerability Scoring System v3.1: Specification Document — FIRST. <https://www.first.org/cvss/v3.1/specification-document> (final)
8. D. J. Bernstein — Cost analysis of hash collisions: Will quantum computers make SHARCS obsolete? (2009) — cr.yp.to. <https://cr.yp.to/hash/collisioncost-20090823.pdf> (paper dated 2009-08-23)
9. D. Litinski — How to compute a 256-bit elliptic curve private key with only 50 million Toffoli gates (arXiv:2306.08585) — arXiv. <https://arxiv.org/abs/2306.08585> (preprint (2023-06-14): 6000 modules × 1152 physical qubits, one key per 10 minutes under its architecture assumptions)
10. FIPS 203 — Module-Lattice-Based Key-Encapsulation Mechanism Standard (ML-KEM) — NIST. <https://csrc.nist.gov/pubs/fips/203/final> (final (August 2024))
11. FIPS 204 — Module-Lattice-Based Digital Signature Standard (ML-DSA) — NIST. <https://csrc.nist.gov/pubs/fips/204/final> (final (August 2024))
12. FIPS 205 — Stateless Hash-Based Digital Signature Standard (SLH-DSA) — NIST. <https://csrc.nist.gov/pubs/fips/205/final> (final (August 2024))
13. G. Brassard, P. Høyer, A. Tapp — Quantum Algorithm for the Collision Problem (LATIN '98; arXiv:quant-ph/9705002) — Springer / arXiv. <https://arxiv.org/abs/quant-ph/9705002> (peer-reviewed article: collisions of r-to-one functions in O((N/r)^{1/3}) expected evaluations)
14. J. Proos, C. Zalka — Shor's discrete logarithm quantum algorithm for elliptic curves (Quantum Inf. Comput. 3(4), 2003; arXiv:quant-ph/0301141) — Quantum Information & Computation. <https://doi.org/10.26421/QIC3.4-3> (peer-reviewed article)
15. L. K. Grover — A fast quantum mechanical algorithm for database search (STOC 1996) — ACM. <https://doi.org/10.1145/237814.237866> (peer-reviewed article)
16. M. Amy et al. — Estimating the cost of generic quantum pre-image attacks on SHA-2 and SHA-3 (SAC 2016; arXiv:1603.09383) — Springer / arXiv. <https://arxiv.org/abs/1603.09383> (peer-reviewed article: SHA-256 about 2^153.8 surface-code cycles on 2^12.6 logical qubits; SHA3-256 about 2^146.5 cycles on 2^20)
17. M. Cain et al. — Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits (arXiv:2603.28627) — arXiv. <https://arxiv.org/abs/2603.28627> (preprint (2026-03-30): P-256 in a few days with 26,000 physical neutral-atom qubits; RSA-2048 one to two orders of magnitude longer)
18. M. Mosca — Cybersecurity in an Era with Quantum Computers: Will We Be Ready? (IEEE Security & Privacy, 2018) — IEEE. <https://doi.org/10.1109/MSP.2018.3761723> (peer-reviewed article; source of the x + y > z migration inequality)
19. M. Roetteler, M. Naehrig, K. Svore, K. Lauter — Quantum resource estimates for computing elliptic curve discrete logarithms (ASIACRYPT 2017) — IACR / arXiv. <https://arxiv.org/abs/1706.06752> (peer-reviewed article: at most 9n + 2⌈log2 n⌉ + 10 qubits and 448 n^3 log2 n + 4090 n^3 Toffoli gates)
20. NIST IR 8547 — Transition to Post-Quantum Cryptography Standards — NIST. <https://csrc.nist.gov/pubs/ir/8547/ipd> (initial public draft (November 2024); proposes deprecating quantum-vulnerable public-key algorithms after 2030 and disallowing them after 2035 — dates may change in the final version)
21. NIST — Post-Quantum Cryptography Standardization: Evaluation Criteria, Security (Call for Proposals, Section 4.A.5) — NIST. <https://csrc.nist.gov/Projects/Post-Quantum-Cryptography/Post-Quantum-Cryptography-Standardization/Evaluation-Criteria/Security-(Evaluation-Criteria)> (security categories: AES-128 key search 2^170/MAXDEPTH quantum gates, AES-192 2^233/MAXDEPTH, AES-256 2^298/MAXDEPTH; MAXDEPTH 2^40–2^96)
22. OSV advisory GHSA-2mjx-qc3c-rqvc — OSV.dev. <https://osv.dev/vulnerability/GHSA-2mjx-qc3c-rqvc> (modified 2026-10-27T15:30:05.509305490Z)
23. OSV advisory GHSA-82j2-j2ch-gfr8 — OSV.dev. <https://osv.dev/vulnerability/GHSA-82j2-j2ch-gfr8> (modified 2026-09-19T03:55:33.412079637Z)
24. OSV advisory GHSA-965h-392x-2mh5 — OSV.dev. <https://osv.dev/vulnerability/GHSA-965h-392x-2mh5> (modified 2026-09-19T03:55:32.245575348Z)
25. OSV advisory GHSA-c8m5-c952-6cm4 — OSV.dev. <https://osv.dev/vulnerability/GHSA-c8m5-c952-6cm4> (modified 2026-10-27T16:15:05.354395696Z)
26. OSV advisory GHSA-h2v8-394m-p7vv — OSV.dev. <https://osv.dev/vulnerability/GHSA-h2v8-394m-p7vv> (modified 2026-10-27T16:15:05.337819489Z)
27. OSV advisory GHSA-qwgh-2vcv-g2f7 — OSV.dev. <https://osv.dev/vulnerability/GHSA-qwgh-2vcv-g2f7> (modified 2026-08-19T19:30:06.686866977Z)
28. OSV advisory GHSA-w44r-93j7-qv28 — OSV.dev. <https://osv.dev/vulnerability/GHSA-w44r-93j7-qv28> (modified 2026-10-27T16:15:05.340347056Z)
29. OSV advisory GHSA-xgp8-3hg3-c2mh — OSV.dev. <https://osv.dev/vulnerability/GHSA-xgp8-3hg3-c2mh> (modified 2026-09-19T03:55:49.146112754Z)
30. OSV advisory RUSTSEC-2022-0081 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2022-0081> (modified 2023-08-25T17:52:15Z)
31. OSV advisory RUSTSEC-2023-0071 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2023-0071> (modified 2026-09-14T09:45:02.996132556Z)
32. OSV advisory RUSTSEC-2024-0388 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2024-0388> (modified 2024-11-10T13:34:40Z)
33. OSV advisory RUSTSEC-2024-0436 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2024-0436> (modified 2026-01-27T22:03:15.694766Z)
34. OSV advisory RUSTSEC-2024-0449 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2024-0449> (modified 2026-10-12T11:45:02.518189315Z)
35. OSV advisory RUSTSEC-2025-0134 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2025-0134> (modified 2025-12-05T19:07:59.622592Z)
36. OSV advisory RUSTSEC-2025-0141 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2025-0141> (modified 2026-01-16T11:07:28.867553Z)
37. OSV advisory RUSTSEC-2026-0173 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0173> (modified 2026-06-07T21:00:04.318567692Z)
38. OSV advisory RUSTSEC-2026-0258 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0258> (modified 2026-10-12T18:00:10.934581734Z)
39. OSV advisory RUSTSEC-2026-0330 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0330> (modified 2026-10-07T08:30:02.862241231Z)
40. OSV advisory RUSTSEC-2026-0331 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0331> (modified 2026-10-07T08:30:02.870588917Z)
41. OSV advisory RUSTSEC-2026-0374 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0374> (modified 2026-10-20T11:15:37.076409305Z)
42. OSV advisory RUSTSEC-2026-0381 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0381> (modified 2026-10-29T10:55:54.096394276Z)
43. OSV advisory RUSTSEC-2026-0382 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0382> (modified 2026-10-29T10:55:54.096394276Z)
44. OSV advisory RUSTSEC-2026-0383 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0383> (modified 2026-10-29T10:55:54.096394276Z)
45. OSV advisory RUSTSEC-2026-0385 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0385> (modified 2026-10-23T08:30:02.389575143Z)
46. OSV advisory RUSTSEC-2026-0386 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0386> (modified 2026-10-23T14:45:03.847864944Z)
47. OSV advisory RUSTSEC-2026-0387 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0387> (modified 2026-10-24T03:45:02.365137418Z)
48. OSV advisory RUSTSEC-2026-0391 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0391> (modified 2026-10-26T14:00:04.269245609Z)
49. OSV advisory RUSTSEC-2026-0395 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0395> (modified 2026-10-26T14:00:06.388344282Z)
50. OSV advisory RUSTSEC-2026-0396 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0396> (modified 2026-10-26T14:00:05.789682118Z)
51. OSV advisory RUSTSEC-2026-0397 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0397> (modified 2026-10-26T14:00:05.089587004Z)
52. OSV advisory RUSTSEC-2026-0398 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0398> (modified 2026-10-26T14:00:05.092082939Z)
53. OSV advisory RUSTSEC-2026-0399 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0399> (modified 2026-10-26T14:00:05.792431051Z)
54. OSV advisory RUSTSEC-2026-0400 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0400> (modified 2026-10-26T14:00:05.692077560Z)
55. OSV advisory RUSTSEC-2026-0401 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0401> (modified 2026-10-26T14:00:04.231502512Z)
56. OSV advisory RUSTSEC-2026-0402 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0402> (modified 2026-10-26T14:00:05.685817733Z)
57. OSV advisory RUSTSEC-2026-0403 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0403> (modified 2026-10-26T14:00:05.787441176Z)
58. OSV advisory RUSTSEC-2026-0404 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0404> (modified 2026-10-26T14:00:05.092817237Z)
59. OSV advisory RUSTSEC-2026-0405 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0405> (modified 2026-10-26T14:00:05.680942523Z)
60. OSV advisory RUSTSEC-2026-0406 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0406> (modified 2026-10-26T14:00:05.095427051Z)
61. OSV advisory RUSTSEC-2026-0410 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0410> (modified 2026-10-26T14:00:05.788985783Z)
62. OSV advisory RUSTSEC-2026-0414 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0414> (modified 2026-10-28T09:00:02.341043798Z)
63. OSV.dev — open-source vulnerability database and API — Open Source Security Foundation. <https://osv.dev/> (the database QSI queries for each exactly pinned version; every advisory id in a finding resolves at https://osv.dev/vulnerability/<id>)
64. P. W. Shor — Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms on a Quantum Computer (SIAM J. Comput., 1997) — SIAM. <https://doi.org/10.1137/S0097539795293172> (peer-reviewed article)
65. R. Babbush et al. — Securing Elliptic Curve Cryptocurrencies against Quantum Vulnerabilities: Resource Estimates and Mitigations (arXiv:2603.28846) — arXiv. <https://arxiv.org/abs/2603.28846> (preprint (2026-03-30, v2 2026-04-15): 256-bit ECDLP with < 1200 logical qubits and < 90 M Toffoli gates (or < 1450 and < 70 M); < 500,000 physical qubits at 10^-3 error, minutes)
66. S. Jaques, M. Naehrig, M. Roetteler, F. Virdia — Implementing Grover oracles for quantum key search on AES and LowMC (EUROCRYPT 2020; arXiv:1910.01700) — Springer / arXiv. <https://arxiv.org/abs/1910.01700> (peer-reviewed article: lower cost estimates for the AES key searches that define the NIST categories)

## Приложения: Криптографическая инвентаризация

| Алгоритм | Параметр | Библиотека | Квантовый статус | Классический статус | Количество | Мест | Примеры |
|---|---|---|---|---|---|---|---|
| SHA-2 | SHA-256 |  | Гровер: допустимо по NIST, ниже рекомендаций ECCG/ANSSI | допустимо | 1 | 1 | bindings/pin/lib/registry.mjs:57 |
| X25519MLKEM768 |  |  | гибрид | допустимо | 2 | 2 | Cargo.toml:155; zingo-netutils/src/crypto.rs:25 |
| Crypto library | 0.11.0 | zcash_protocol (Zcash protocol crates) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.11.1 | jubjub (jubjub) | н/п | допустимо | 2 | 2 | Cargo.lock; Cargo.toml |
| Crypto library | 0.13.0 | group (jubjub) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.13.1 | ff (jubjub) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.13.1 | p384 (RustCrypto elliptic curves) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.13.2 | p256 (RustCrypto elliptic curves) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.13.4 | k256 (RustCrypto elliptic curves) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.14.0 | group (jubjub) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.14.0 | ff (jubjub) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.15.0 | bellman (bellman) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.16.0 | orchard (Zcash protocol crates) | н/п | допустимо | 2 | 2 | Cargo.lock; Cargo.toml |
| Crypto library | 0.16.9 | ecdsa (python-ecdsa) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.17.0 | zcash_keys (Zcash protocol crates) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.17.14 | ring (ring (Rust)) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.2.0 | halo2_poseidon (halo2 (Zcash)) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.2.0 | sinsemilla (sinsemilla) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.2.1 | zcash_spec (Zcash protocol crates) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.21.12 | rustls (rustls) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.23.43 | rustls (rustls) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.25.0 | zcash_client_backend (Zcash protocol crates) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.27.0 | secp256k1 (secp256k1 bindings) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.3.0 | zip32 (Zcash protocol crates) | н/п | допустимо | 2 | 2 | Cargo.lock; Cargo.toml |
| Crypto library | 0.31.0 | zcash_proofs (Zcash protocol crates) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.31.0 | zcash_primitives (Zcash protocol crates) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.33.1 | secp256k1 (secp256k1 bindings) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.4.0 | halo2_proofs (halo2 (Zcash)) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.5.1 | zcash_note_encryption (Zcash protocol crates) | н/п | допустимо | 2 | 2 | Cargo.lock; Cargo.toml |
| Crypto library | 0.6.0 | halo2_gadgets (halo2 (Zcash)) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.6.0 | pasta_curves (pasta_curves (Pallas/Vesta)) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.6.1 | reddsa (reddsa) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.9.0 | sapling-crypto (Zcash protocol crates) | н/п | допустимо | 2 | 2 | Cargo.lock; Cargo.toml |
| Crypto library | 0.9.0 | bls12_381 (jubjub) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.9.0 | redjubjub (reddsa) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.9.10 | rsa (RustCrypto rsa) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 2.0.1 | x25519-dalek (ed25519-dalek) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 2.2.0 | ed25519-dalek (ed25519-dalek) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 4.1.3 | curve25519-dalek (ed25519-dalek) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.23.40 | rustls (rustls) | н/п | допустимо | 1 | 1 | Cargo.toml |
| Crypto library | =0.11.0 | zcash_protocol (Zcash protocol crates) | н/п | допустимо | 1 | 1 | Cargo.toml |
| Crypto library | =0.17.0 | zcash_keys (Zcash protocol crates) | н/п | допустимо | 1 | 1 | Cargo.toml |
| Crypto library | =0.25.0 | zcash_client_backend (Zcash protocol crates) | н/п | допустимо | 1 | 1 | Cargo.toml |
| Crypto library | =0.31.0 | zcash_primitives (Zcash protocol crates) | н/п | допустимо | 1 | 1 | Cargo.toml |
| Crypto library | =0.31.0 | zcash_proofs (Zcash protocol crates) | н/п | допустимо | 1 | 1 | Cargo.toml |
| Crypto library | workspace | jubjub (jubjub) | н/п | допустимо | 2 | 2 | pepper-sync/Cargo.toml; zingolib/Cargo.toml |
| Crypto library | workspace | zcash_protocol (Zcash protocol crates) | н/п | допустимо | 6 | 6 | pepper-sync/Cargo.toml; zingo-cli/Cargo.toml; zingo-ffi/lib/Cargo.toml |
| Crypto library | workspace | zcash_keys (Zcash protocol crates) | н/п | допустимо | 5 | 5 | pepper-sync/Cargo.toml; zingo-cli/Cargo.toml; zingo-ffi/lib/Cargo.toml |
| Crypto library | workspace | orchard (Zcash protocol crates) | н/п | допустимо | 2 | 2 | pepper-sync/Cargo.toml; zingolib/Cargo.toml |
| Crypto library | workspace | zcash_note_encryption (Zcash protocol crates) | н/п | допустимо | 1 | 1 | pepper-sync/Cargo.toml |
| Crypto library | workspace | sapling-crypto (Zcash protocol crates) | н/п | допустимо | 2 | 2 | pepper-sync/Cargo.toml; zingolib/Cargo.toml |
| Crypto library | workspace | zcash_client_backend (Zcash protocol crates) | н/п | допустимо | 4 | 4 | pepper-sync/Cargo.toml; zingo-cli/Cargo.toml; zingo-ffi/lib/Cargo.toml |
| Crypto library | workspace | zip32 (Zcash protocol crates) | н/п | допустимо | 4 | 4 | pepper-sync/Cargo.toml; zingo-cli/Cargo.toml; zingo-ffi/lib/Cargo.toml |
| Crypto library | workspace | zcash_primitives (Zcash protocol crates) | н/п | допустимо | 2 | 2 | pepper-sync/Cargo.toml; zingolib/Cargo.toml |
| Crypto library | workspace | rustls (rustls) | н/п | допустимо | 1 | 1 | zingo-netutils/Cargo.toml |
| Crypto library | 0.23 | rustls (rustls) | н/п | допустимо | 1 | 1 | zingo-netutils/webpki-verifier-shim/Cargo.toml |
| Crypto library | workspace | zcash_proofs (Zcash protocol crates) | н/п | допустимо | 1 | 1 | zingolib/Cargo.toml |
| PQC library | 0.1.1 | ml-dsa (RustCrypto post-quantum crates) | постквантовый | допустимо | 1 | 1 | Cargo.lock |
| ECDSA | secp256k1 |  | уязвим (Шор) | допустимо | 1 | 1 | zingolib/src/wallet/keys/legacy/extended_transparent.rs:50 |
| Pedersen commitment |  |  | уязвим (Шор) | допустимо | 2 | 2 | pepper-sync/src/scan/transactions.rs:51; zingolib/src/wallet/utils.rs:122 |

_Длинные списки здесь сгруппированы; полный список по файлам — в JSON-версии отчёта, подписанной тем же ключом._

## Приложения: Входные файлы

| Файл | Размер | SHA-256 | Маскирования |
|---|---|---|---|
| Cargo.lock | 269057 | `fac8e0d6c1a50c97243571fd26211ab19303a882a7fa54ae3d952894f53b7473` | 0 |
| Cargo.toml | 6510 | `53590c97f0183db8eab7c94382ab367e4a92cb2fb4dad339a167efa9e3bb8028` | 0 |
| bindings/android/build.gradle.kts | 5535 | `cdcf1671bd315ea49e0cb9d1e7a8c63cd9a9347fdda53be331ae11755848de93` | 0 |
| bindings/android/settings.gradle.kts | 258 | `46b810b2fed48a8c7f6e87dd454b50e1c19d180743390679eaedb683b96efaf9` | 0 |
| bindings/pin/bin/fetch_binding_layer.mjs | 921 | `196946f5b9729dbdfe8350f4c3452d278ebb809fa6b3cf5476fa36e78f700854` | 0 |
| bindings/pin/bin/pin_binding_layer.mjs | 1322 | `7d1f4ffae98ee8e17cc854dfff7e262a4a9fe3cd722618fb7784beb85dea22d3` | 0 |
| bindings/pin/lib/bundle_messages.mjs | 5057 | `bdd242a3f59c78d160ab5399b5071039c5a2e0efb24258be1cb5d66801574bf1` | 0 |
| bindings/pin/lib/bundle_pin.mjs | 5104 | `be2d7aeebf6d38fe445d591e65ff5a7354d31b58c74c46b65f9eaa33bf6b089f` | 0 |
| bindings/pin/lib/disk.mjs | 1106 | `269b036f85a2737b5bbe7c0337c73a62690a33c681fcbf8346775730303064f1` | 0 |
| bindings/pin/lib/fetch_binding_layer.mjs | 4079 | `e21e6386676a83582b6a684e8f7f0b36a3a0aef810faa63b1c337bd3b12336b6` | 0 |
| bindings/pin/lib/maven_repository.mjs | 2538 | `16eae3774c0cb74435936272b4cbaa081cba7439cb4ce1f765827fb06ccf457c` | 0 |
| bindings/pin/lib/pin_file.mjs | 586 | `910e010aa6710abfb05d1fe3e45d7e1a12ebe3a7e2da29d314dccd3f76b34c40` | 0 |
| bindings/pin/lib/registry.mjs | 2734 | `8839e5d9674b8300c64ff2b6153bd48bb9484236ab2ddf0ed226f407473cc168` | 0 |
| bindings/pin/lib/swift_package.mjs | 1390 | `cff1d7c7d858e552bfb9c457293ebd8eac000d37f5db34674bb33257cbcd67fc` | 0 |
| bindings/pin/lib/tar_archive.mjs | 5433 | `8c2270e86b07f0024c345f8d4369db4bd76cab0daee444eac7ce65e3e45de6be` | 0 |
| bindings/pin/package.json | 616 | `e6623b934f833a59eb835eb19f88a36f64c865d1330d34f76fc711ada0e8d8c1` | 0 |
| bindings/swift/Package.swift | 904 | `ebd25d8956995a134b21c316301c5d04c70c3108b58eeca94d9679fe01ae8392` | 0 |
| pepper-sync/Cargo.toml | 1912 | `cb854fe9df00292257d10f8bec91894560d603df354c613e0b671944db6e295f` | 0 |
| pepper-sync/src/client.rs | 26541 | `ffafbcb9ee59a433fa979e5b31244deb9d7bcdf3d127ab1c6c73efcccda53919` | 0 |
| pepper-sync/src/client/fetch.rs | 13058 | `c30f95535e1815f02268d85f39f0e02fbc2136bda5c300b64279e4a531c51b06` | 0 |
| pepper-sync/src/config.rs | 8825 | `6fbd2c35791ae409403ebbcd698d8926e8c48fe37b7831db62c1ef7e0948edfa` | 0 |
| pepper-sync/src/error.rs | 43243 | `268c148cf6240b73465bc234ab7b70790a7a7e10c5be09885deb1a6b4622635c` | 0 |
| pepper-sync/src/keys.rs | 9595 | `8cba355b5f15a818ba9b8a6458c95e1749751af5eba0286e00a2af293bd8f099` | 0 |
| pepper-sync/src/keys/transparent.rs | 4843 | `c647c160651c24fcfe8c85a5ea357f460471ee2a76181d77dcc8ab67a28ec26f` | 0 |
| pepper-sync/src/lib.rs | 9742 | `62a7c86cab30449a186e351fe499091299b8b83c7bc1eb334c66181696022071` | 0 |
| pepper-sync/src/mocks.rs | 11631 | `ac5fceb8f9ccb984088999203953aac63099bda9f1f454e92b9038c89746df30` | 0 |
| pepper-sync/src/scan.rs | 12962 | `ed077f1a52419fcec4d2c630e2353b3ef73d2744534891b3d4a8bd75272e671e` | 0 |
| pepper-sync/src/scan/compact_blocks.rs | 51957 | `4b415108604477312f486b2b9fbc0becab5c33390e413039b62cf843bca56bfb` | 0 |
| pepper-sync/src/scan/compact_blocks/runners.rs | 22694 | `69aecdf74b0895fbdbbfe07f7d5da8fcba20f5722787474c9d181ceb8f03c1c4` | 0 |
| pepper-sync/src/scan/task.rs | 57518 | `4e443ebb418234b15719737b7b945e29a0923a4f60621d5886115eefb9800ae6` | 0 |
| pepper-sync/src/scan/transactions.rs | 28456 | `259906c37470febc5de66d131f0cb0eb469bfcbdc87945570b0489c9a976a484` | 0 |
| pepper-sync/src/shardtree_ext.rs | 6591 | `d73b1dc74bd7019d9bc5b5ff59c5556882ea68ee75dfcebbcf45bbbeba1abf93` | 0 |
| pepper-sync/src/sync.rs | 288020 | `82fbcee650c61cbf2017ddbec067993d11856c54fa1ff4175d9a76b256a45d5f` | 0 |
| pepper-sync/src/sync/spend.rs | 20359 | `81837dcbd331997aa8339fdcb20e9da26df8e760efd0a533e39d4e8a8a53f2be` | 0 |
| pepper-sync/src/sync/state.rs | 90087 | `a1d8cb17703f6c175b30a1c082dca289797829d665e5376bbd79413368a56767` | 0 |
| pepper-sync/src/sync/transparent.rs | 12252 | `b4025cd498775af74d112ad17dec9c703f95ca70dd83290cf5afe42a2bb64de6` | 0 |
| pepper-sync/src/sync/truncate.rs | 24480 | `51fa30b089eff01597a16f3ca42e64c11113d2688993ce87062a6df2dc574053` | 0 |
| pepper-sync/src/utils.rs | 2191 | `94143291b729fcac1647fb525d12b3e8ad40c1626cb5306893e66ce1041ddc27` | 0 |
| pepper-sync/src/utils/block.rs | 3679 | `51042b9fe274e4ee01a6ab7f1ab9d8c055eacad1119840257e7290392e86e445` | 0 |
| pepper-sync/src/utils/transaction.rs | 3206 | `ae89558d436f0208ac5fb0e44e8bdbeaa17d7aa3845f691d4e994f8680806d59` | 0 |
| pepper-sync/src/wallet.rs | 70447 | `7e1c52143c5408f0babde71d5874073fadbd17b82785c3b1667a37c40db53fad` | 0 |
| pepper-sync/src/wallet/serialization.rs | 76004 | `c9f30245e50308609a4d0acef40881358f22a07adf90faf05d954e69ada6afcd` | 0 |
| pepper-sync/src/wallet/traits.rs | 22939 | `335291bac4b8980e3ef0b0dde28dba1196e8a257c2ee0cf608e18795f96b07a0` | 0 |
| pepper-sync/src/witness.rs | 32790 | `bbf1574e8a09542f6d51bba014842a75cad8314b37d976510ec8e081eef80a13` | 0 |
| rust-toolchain.toml | 68 | `f0d38d5646454eb43314992e5014e5573def564955811be9f450ce8a72760e99` | 0 |
| tools/workbench/Cargo.lock | 5989 | `8b03f73d12ed89ed28111b2e424726179f2b94a79a3d499ce18372d9a1834c6b` | 0 |
| tools/workbench/Cargo.toml | 924 | `1ae94a3d4c4793094221d394c0ecf1c6fbbb0963b9ad76d49f5f7ebe1ab5e242` | 0 |
| tools/workbench/src/bin/binding-changelog.rs | 104 | `1e9a539347ba364b231b920e65e03011fb90e30d8245f31f3528b95f9b0450b0` | 0 |
| tools/workbench/src/bin/binding-manifest.rs | 102 | `6765d145caa8bcb93395676a81c88fd961f93d4be24a3d829bb11589d408db14` | 0 |
| tools/workbench/src/bin/binding-publish.rs | 100 | `f736043b2c8c24ae6bdc5b731aa6afbf42a43566dde9be984609c0277bfecd3c` | 0 |
| tools/workbench/src/bin/birth-trial.rs | 17200 | `ca56e4b52abe845d3c533ec706a036eb0f78dd6f2ecd0df1e309669e8245e588` | 0 |
| tools/workbench/src/bin/build-binding-layer.rs | 93852 | `77167d578a5f65f7092e1b2af513555598981ce167614a0fbb3f2f7626624607` | 0 |
| tools/workbench/src/bin/bundle-nym-proxy.rs | 4708 | `fd176b6d7114debf2b3e7f5f39a33494024a5326b57bf7f9a491113120d93826` | 0 |
| tools/workbench/src/bin/cancel-closed-pr-runs.rs | 807 | `8fd6d3088fb3fdf5240a73a750ec6a286dfc3da4e73dca52e3ab4fcd822bdbf1` | 0 |
| tools/workbench/src/bin/dupes-gate.rs | 90 | `b2454538e136ce2a1d83bbeed8462f59e0ca9da6cd764eadba1db9256ff3de2e` | 0 |
| tools/workbench/src/bin/exclusion-audit.rs | 16507 | `d09fd7b47f7882708125db69603f96027f9b6e4859bb844ab4b9a8ca92fa6d96` | 0 |
| tools/workbench/src/bin/exit-census.rs | 4222 | `28c959a59f132ee51e66ca89ac786c3752554b6067e3ca24b22d437a9e47cccf` | 0 |
| tools/workbench/src/bin/feature-sweep.rs | 7492 | `aa6a483bd3f799037c03c85a62786f9b27161e88402a701016340c3e1df28dc3` | 0 |
| tools/workbench/src/bin/get-rust-version.rs | 571 | `3712d3713716d584082bb666e1382b59cf63097be91324bd01b2b0fd10b81294` | 0 |
| tools/workbench/src/bin/prune-cache-families.rs | 315 | `5c7b92524774aa205748ce294bd199ce6baafe06d0ab6f6d224324e2bc8f79dc` | 0 |
| tools/workbench/src/bin/run-cli.rs | 8287 | `2a4fa5bed9b27e1e0f1e8d7166bbdc174c9f4e0b7abbb37e79fbc09f4a4c0ce3` | 0 |
| tools/workbench/src/bin/sweep-teardown.rs | 6631 | `3740feb9ce55d96a0b1c27eb7983c613a59fb96b815ab9b342cf7882bee833e5` | 0 |
| tools/workbench/src/bin/sync-ab.rs | 52578 | `30ed268df725d5300a0eea3cc68057eb3b13e03ddb8adeee29c7ca8a2eda3d76` | 0 |
| tools/workbench/src/bin/test-summary.rs | 18212 | `2afcfeeb0aa8ac4fd3e6c1e4a9c6fb07bd8ea7586fb024c22786887f5a27d20a` | 0 |
| tools/workbench/src/binding_changelog.rs | 27395 | `c087210c68e6e6184413b79f8e0856f79f3d9ec54f623b2db6ee50c1863c79a9` | 0 |
| tools/workbench/src/binding_layer.rs | 47525 | `54346ca14ae2d378538c50082d7e26e310a1fb59d82fabe92344c672af59838e` | 0 |
| tools/workbench/src/binding_manifest.rs | 41318 | `56b8056db6f9f36f3d3e91147f5c01306ae3039cdf73a365b03f5082afa11901` | 0 |
| tools/workbench/src/binding_publish.rs | 46304 | `aa24c49631b0d0f4a920b2db09c6c1f6a338a0a2545bca48554b53c65d1f7aef` | 0 |
| tools/workbench/src/cache_families.rs | 11455 | `cc50eb1613a9f89abe21eefab62b4a3bc1870916b98a4766ebc16903f7e14ff3` | 0 |
| tools/workbench/src/closed_pr_runs.rs | 3181 | `410c59133ff3149389526de0720130f0833482a8d8098c0ebf6a6be5f7278bd5` | 0 |
| tools/workbench/src/dupes_gate.rs | 20814 | `009f21c019e3114447c95800b77d6abab317cad1ba3acb052697a8ee555e6608` | 0 |
| tools/workbench/src/lib.rs | 32893 | `867152be257373bd5e9fd4d5c806ee0e59de2877656368c1c712036bb9fa2340` | 0 |
| tools/workbench/src/nextest_ceilings.rs | 17162 | `ed4f196bc7d0ff031de51a590a819236c3cd7edbf68555b93862c5017afb8369` | 0 |
| tools/workbench/src/orasust.rs | 11433 | `9edad0dba4a8803c41bf2256b1801c09b4d85b3d90963784d5a44265ceffd48d` | 0 |
| tools/workbench/src/panic_strategy.rs | 12201 | `4db6af7faf6adf89e8099dfac420fc530ccf365e1e2815fbc6f2439821d1b225` | 0 |
| tools/workbench/src/runner_labels.rs | 6773 | `ae571ee6528eb0061856d6fda659b5c924e9c64e252c19107a3228af96e6f161` | 0 |
| tools/workbench/src/session.rs | 804 | `692c78bfaaba4dfe204e775d7f8a103dd3e57b5da859ac08c253af55b1599ae9` | 0 |
| zingo-cli/Cargo.toml | 3550 | `7afab8c0e5c4e65a4ee096835d8087fd3ae9c59211586afb3f7ae96599d1339b` | 0 |
| zingo-cli/src/commands.rs | 128654 | `5a9a667d8972fbf08cd03d2c1662f8f525d8d15baf1660525c4ded96552b9545` | 0 |
| zingo-cli/src/commands/error.rs | 2309 | `1af580b0e98dd06d952f53d0d65646a0553675e0d2e8647b121489f22c4c66d8` | 0 |
| zingo-cli/src/commands/utils.rs | 18392 | `0cef416249cd1c89e1eda7fdadc8c3f02312ce543538433778f353722efc84e9` | 0 |
| zingo-cli/src/examples.rs | 3320 | `ca2dac2b82f5d69151ee6414314ac2ecc1dd952c64ff01e887a1921b1739fefb` | 0 |
| zingo-cli/src/lib.rs | 68138 | `f81f944fe001703ec95d6de5367f060bd81733676c7cf4608efbb3a13a1bddd1` | 0 |
| zingo-cli/src/main.rs | 2215 | `5a8c098d4c55b61280791b9e7ceb1c8692a4ad8da70ac04ab7a5656363fe8912` | 0 |
| zingo-cli/src/version.rs | 196 | `a14997d447841b89e86f8a3ca590ca472c3dcc5c2dee6a7a8a998324816075b2` | 0 |
| zingo-ffi/lib/Cargo.toml | 1555 | `2e4b5a336c030f625d7ffa37de14743cda674618fbbb36e9856ba2dca50809dd` | 0 |
| zingo-ffi/lib/src/lib.rs | 160142 | `0757d7edd0073242e36c6f519ec531c28d0869a11e21ba863594664e66f9173e` | 0 |
| zingo-ffi/lib/src/private_migration_drivers.rs | 14136 | `8b57773701f758845c587fff8b7465bf643869b09217f98b3781f9516feeef79` | 0 |
| zingo-ffi/uniffi-bindgen/Cargo.toml | 497 | `ae1827830f913e24838e2c780f0bd67edaf9aa127a584272acf22b27d723f52c` | 0 |
| zingo-ffi/uniffi-bindgen/src/bin/zingo-uniffi-bindgen.rs | 73 | `26cfd7ef272f10db8f0abe94ffb23ecfba65785c55577435be87bc91534ae109` | 0 |
| zingo-memo/Cargo.toml | 510 | `2e0a967e54bf1a12d8eece1e07aa4e7bb242547645d2469e8e554e9d5050250c` | 0 |
| zingo-memo/src/lib.rs | 24679 | `7d21ef7a5065fefebd4d980e1ee12cd3bb700e20e954cc5c56008d8c6f87b7e0` | 0 |
| zingo-net-diag/Cargo.toml | 1367 | `6d458b06bc3f3b254ea8a7f6fd3d09e3f6c43facc0349ca48011ca8a6b71b73f` | 0 |
| zingo-net-diag/src/lib.rs | 12792 | `1f43c7fe33c3c78cb1e5e52978bd8193c4198a9d3cb9be3154e7dc763659d6c2` | 0 |
| zingo-netutils/Cargo.toml | 7204 | `068590c5c29b8abb74d68296db44019686ab0030384af687879b89db2f67f880` | 0 |
| zingo-netutils/nym-proxy-ffi/Cargo.toml | 1478 | `b7c0f29815de3daba9ddb9857dfa446e3c5b70f0941c13245b867901092019cc` | 0 |
| zingo-netutils/nym-proxy-ffi/src/debug_log.rs | 1205 | `9412804b4ff7a9319fc0d8b83f2ffba4a67c8a26559fe5d5865d50b4f642f1f3` | 0 |
| zingo-netutils/nym-proxy-ffi/src/lib.rs | 52384 | `a869e35b7affec221ed36e54f66833a22cdbbf49255716235c988d680a5b8704` | 0 |
| zingo-netutils/src/arm_race.rs | 15584 | `732e37bba90b36ca46a9ab81606850b83de8ae11b6471821085e98ec52288835` | 0 |
| zingo-netutils/src/bin/nym-proxy.rs | 9536 | `92a7edaa963f195b1289cd658e4424b23f5f1e6241b112b4ba7485616a1e7169` | 0 |
| zingo-netutils/src/conduit.rs | 6800 | `86b17f70eb30846b7239b3982ed2738da59f979adfe048d473567713151edc33` | 0 |
| zingo-netutils/src/crypto.rs | 1327 | `53d4da233ecfec4bf7655cb5dbdf9b7d13a4c324417820f644a8f66e4aa9c726` | 0 |
| zingo-netutils/src/default_indexer.rs | 1314 | `3448c44060958ba0edff6b766a8ad0276792f0f707376e1c8c23a9d167c8c074` | 0 |
| zingo-netutils/src/error.rs | 4995 | `4c08d5217b929e434b82b0e8dba78e885ce3b52cab6cbcac6d211001cbf70ae0` | 0 |
| zingo-netutils/src/exit.rs | 14923 | `9427ef906ba1c3c25a1db4b34e51fc3d9642af03f6551997f62769f564564ea0` | 0 |
| zingo-netutils/src/globally_public.rs | 6105 | `550ab26e7b7dc8ca62ecd8478f8f44b6f44025014be6d01719a1a24c7a9943cc` | 0 |
| zingo-netutils/src/lib.rs | 41384 | `b1fd42806f601f0976b79ad55da16c4b9b74f792659bc4911106cca06268cd38` | 0 |
| zingo-netutils/src/mixnet_connect.rs | 2347 | `ee29dc1fe24a81d5f5e1f0d15de830db7b1c1b423724a36a8be2412657049d5c` | 0 |
| zingo-netutils/src/nym_proxy.rs | 46801 | `1c3426cfd779f5e2e5ec82905ed6db7f64b8a4522343e67beffaf555a84be20e` | 0 |
| zingo-netutils/src/nym_proxy/closed_input_channel.rs | 3486 | `4977f9933c266fecbe954f2dc79e9bb2d3bd6663814a698d37f0e94cefcb9ed8` | 0 |
| zingo-netutils/src/provider.rs | 4282 | `4bd6246a9176cbb1c6e66a98214f73a999cea143acfaaf5f3511945a07ed057f` | 0 |
| zingo-netutils/src/sentinel.rs | 5852 | `b3d853aaf96db87803197419c380f4d955313e4b0ecd4b022e97d7aca216c1fd` | 0 |
| zingo-netutils/src/socks5_fetch.rs | 10957 | `75cc50e0cb795b279496ed33d2101022077900ea075c08320d000a000c93d0a9` | 0 |
| zingo-netutils/src/socks5_transmit.rs | 32741 | `23a821b28bf89514ed7d0cc6e99a6d5a45d98059e2fcb1c47ce690ad504d381b` | 0 |
| zingo-netutils/src/time.rs | 17371 | `d66d0d2601e220db5166a4005c891c9a4f660381d422291e83f75a4162752a9d` | 0 |
| zingo-netutils/webpki-verifier-shim/Cargo.toml | 810 | `470bacd633625299e12d7d8e5dcbcb372f949ca786e47fff7659662005533df0` | 0 |
| zingo-netutils/webpki-verifier-shim/src/lib.rs | 4970 | `b9d9737f96ec96d04b4115196c1e9382809c876b1bd3682620c31d25e1d9432d` | 0 |
| zingo-price/Cargo.toml | 1591 | `acdd168ec89f5ef282c666f0d1e8a2ec585c6c89591f93182fae54958bba9af4` | 0 |
| zingo-price/src/lib.rs | 46162 | `e15ab6331af723ca068139f047f93b7f1db234a1551a9c84a604d39ad3d4a31d` | 0 |
| zingo-status/Cargo.toml | 475 | `530a6054e2a6b49ece605ef3811f03847e3a5e35220655e0a825a716d644f6d8` | 0 |
| zingo-status/src/confirmation_status.rs | 18966 | `6352e8d2c24745ea29c1c22aefd3de572310ec179ca23e8ec642e0bdf8a744b5` | 0 |
| zingo-status/src/lib.rs | 131 | `7116bf9fc6946bf3a1a7ac6297a8574629d1ddf0a1f34cb5c1f949f6294246cd` | 0 |
| zingolib/Cargo.toml | 4633 | `9b911a4a96949da4b1d7508f2d0b6bbc6d45658207362836ae67dce133f9e4c2` | 0 |
| zingolib/build.rs | 6034 | `6e03692bfa9739ba09a3e2fc366e31069898515bdf98e67fd15a27b7428199d7` | 0 |
| zingolib/short_commit.rs | 404 | `b85e23877779e79c51c56483346cf26e6b7bb3817dec89323c241f7afaf543ee` | 0 |
| zingolib/src/config.rs | 32049 | `973efe5bf2e2e74b26d77dfe33c477c823d66e677c7b5e54b89efd6b41f9a78c` | 0 |
| zingolib/src/connectivity.rs | 7392 | `0bb58b2aee4a21f39a64a55b6c46337af02980fdf60a44214ad7790f02af4e67` | 0 |
| zingolib/src/data.rs | 6399 | `ef8ded0f6af8a9bba084f353003f1110792818f1a47e7045a69af72c05f5fd6d` | 0 |
| zingolib/src/data/proposal.rs | 7057 | `9d2484cce68e77192881199eeb0981c8d1935f8c48155e8e22d8382353ab572a` | 0 |
| zingolib/src/destination.rs | 1702 | `6187b9d4d4c75023e70bdb39c89a0dc3df3b6157dc14f7d62a1d46735152f3ff` | 0 |
| zingolib/src/lib.rs | 2743 | `81740b427c900fcc0f78cd5ee804b5ec6084b2e2ce268d20a6313baa98ee0929` | 0 |
| zingolib/src/lightclient.rs | 44281 | `67b2ca378b351ab5210991283732f151d12dba61d8dac499be5cd2abaf87c367` | 0 |
| zingolib/src/lightclient/darkside.rs | 7739 | `11b05f6f719b8533229ce3053f5758134c78a3609b0b4aa03419f6aa91bbaa6c` | 0 |
| zingolib/src/lightclient/error.rs | 9274 | `218d26d9a728abc456103066197f1b1fcff0de53dd5420005a91748c45e14f4e` | 0 |
| zingolib/src/lightclient/indexer_history.rs | 10447 | `3a214c6366b40f970815bc3179d3bd96fe62edc03650fbdfae8e4bcbc6048cce` | 0 |
| zingolib/src/lightclient/migrate.rs | 230129 | `6747506998d65b7313927f0b849ddd9758635195e09a6b0d739ff97265aa3f3a` | 0 |
| zingolib/src/lightclient/migrate/transmission_grpc.rs | 2464 | `4b1fc8668c65ad9ab64afcf81384ac11717621243c0d6a21143aadabcdcfb99e` | 0 |
| zingolib/src/lightclient/migrate/transmission_route.rs | 3540 | `e7270671ca5029f5d7a5a47389ba6e4322551cbe058ead09c81ef1bc5c4a3ff5` | 0 |
| zingolib/src/lightclient/mixnet.rs | 104009 | `a705fba1b7033e2ebf32e250a40dc33f3d6fba9cb1010b9c34bb29cc2f4b12db` | 0 |
| zingolib/src/lightclient/offline.rs | 9861 | `e8c6ee1e299e23398f66bb4e31f6ac508d1f10c0e66bd402d5d996588533d1a9` | 0 |
| zingolib/src/lightclient/propose.rs | 90209 | `fe7ae699c4a3f8a54e7e235054ce43a41a38a6c78be0dda75dbf4e3c39d742a9` | 0 |
| zingolib/src/lightclient/save.rs | 6884 | `49064ec1bd8df041c85ce7bf62f650206a5d4ae109c61cc549442bc118a55330` | 0 |
| zingolib/src/lightclient/send.rs | 72495 | `5c104f08a6f7bc74a04ffa0dec0baf418f2571a9714a0e8d9618a50bd6955fa5` | 0 |
| zingolib/src/lightclient/sync.rs | 27239 | `433e4f17d8bb1e2269b0d40a014b655cfeca15fb6b049c3a999ac4f1c5529155` | 0 |
| zingolib/src/lightclient/transmit.rs | 21620 | `d184e1c25740b40a89ededa39f235ede62ca5c7b5adfb8432daa7604b9430c44` | 0 |
| zingolib/src/mixnet.rs | 7559 | `875f84c8af9c6340680702ee1b4b67db3dec300512af29236436a575ce5d82df` | 0 |
| zingolib/src/mixnet/acquire.rs | 17035 | `451a1ced6d94746d7f786a5fab5ea46958fbcdb499db28c40de96cc63c55b62c` | 0 |
| zingolib/src/mixnet/driver.rs | 17703 | `1a2c3a14b1cd1bb4cb72406bbdb522a930b4ad076f1320025719598f48774a39` | 0 |
| zingolib/src/mixnet/mode.rs | 28376 | `a7d257d091223c151fa9541d0ab4a4108e5712944b5ae83d084214122784ad1f` | 0 |
| zingolib/src/mixnet/pools.rs | 20546 | `14221916607a8ba9d110baf9ad63e94573eb7c2f04cdd1f304802c879b044ad5` | 0 |
| zingolib/src/mixnet/probe.rs | 14497 | `2dd2e20dc9599da3d5ce78e769be80e44d2604fedfda1803bae35f52e9ecd9f0` | 0 |
| zingolib/src/mixnet/provision.rs | 8830 | `8cc0149073416f4c571e51058b816309ef44273b904134c8ca3065e465a5e759` | 0 |
| zingolib/src/mixnet/roles.rs | 3262 | `180726f0c2626cabdd0a1a3776983be38372bc97d6bc31cc762525ed060ec9c2` | 0 |
| zingolib/src/mixnet/route.rs | 12149 | `661573e5eac4dcfcfa94719362565361524ff82484f41fd4e5866ef5eb06dee1` | 0 |
| zingolib/src/mixnet/speed.rs | 13226 | `88449c6f75cfcc6c2000d87fb8c23232df8f5dfae98cf216f907e6180152f029` | 0 |
| zingolib/src/mixnet/supervisor.rs | 68926 | `6424d562d3a32c6212274c84f63ae9e4086027609682365b2bb060d4ee0ea45b` | 0 |
| zingolib/src/mocks.rs | 25636 | `69c32dee7effe0a074861a1e35a70a4eac4b2627ca5a72237017115da5a9f773` | 0 |
| zingolib/src/netutils.rs | 1892 | `9c1645ef9329ba39250973dcb5c3a287d87c8f6ac0ecc327ea6bd26cc0b19afa` | 0 |
| zingolib/src/perspective.rs | 17526 | `68bb1a77eb931bf6210643dea8324f4f23cb768cb90f66e07bbf50e667c12bec` | 0 |
| zingolib/src/perspective/finsight.rs | 3536 | `b1e9abde77d4fb4a988307c2c6889412831c2fa6dc14ad0efd933917a022fe3e` | 0 |
| zingolib/src/perspective/sync_progress.rs | 16167 | `f37222e8a3582427e5518571801f25b1a02521dfa70b7be0c1ca75e8cdd5f6a1` | 0 |
| zingolib/src/perspective/value_transfer.rs | 9794 | `bd2018277b1e783beec1d720520e7659276c9150e3b45964dd74dab63194b768` | 0 |
| zingolib/src/sync.rs | 1440 | `f1db0a5ea4eb43821dab262703683656ede4b6b80e14c44c540c7efad87520fa` | 0 |
| zingolib/src/testutils.rs | 23519 | `8f8403a2837ea3ec54c4127a4b9cfc45f6c773fb3de973307ad5d622cc8c5640` | 0 |
| zingolib/src/utils.rs | 758 | `bd3d11ed9172991c77bff15db8dbf3ef08f1e704b948de9d475f71c88e47a50e` | 0 |
| zingolib/src/utils/conversion.rs | 1041 | `35cfbd9dbde9c20b64c6c7cbf8091fa667b0ad857c2c558cc9ef866d5b525734` | 0 |
| zingolib/src/utils/error.rs | 1119 | `98247988272803cf18a834be0ba64e88bb3b61ac956c4122ae7dc234f21cfc93` | 0 |
| zingolib/src/wallet.rs | 23383 | `5be198adcfeef9bbf2591b693e25dbbe331d04e6950b0a95e29230b5223eecf3` | 0 |
| zingolib/src/wallet/balance.rs | 25423 | `b988800a21df2d94e05cbd5094995dd88306049d093dbdd1e6e5a9d4b67f37c0` | 0 |
| zingolib/src/wallet/disk.rs | 40693 | `d5c7b53f357e33542ca84a74487e411d50aeaefdb2029c12f155b245b9fea24f` | 0 |
| zingolib/src/wallet/error.rs | 14639 | `97a8e4797daea80b6020f07b18b4b25bb957af3c3f5592f0638743a1f067243d` | 0 |
| zingolib/src/wallet/expiry.rs | 2990 | `9d61d2f5b112025c0b222f5086f3065d35876e2a6cfdd22353e9b96b93def32b` | 0 |
| zingolib/src/wallet/keys.rs | 32419 | `58a86aaab239a06a5d9b1ec2fe493c892c503bd7908864220b3ff171ffad596a` | 0 |
| zingolib/src/wallet/keys/legacy.rs | 15247 | `e15f9b3ffdb3f22737086c11765db8032e9b66acf1c50c1ea26db93eaf3d7fae` | 0 |
| zingolib/src/wallet/keys/legacy/extended_transparent.rs | 9788 | `c18e56a265bc99d75f5eb79cd90e5d15436afb786584bf4622cfb3af521fede7` | 0 |
| zingolib/src/wallet/keys/unified.rs | 16779 | `10b188df25208c9a0fa25ef697e3f85649fc64fcac5b128a85d633d2c24b68b8` | 0 |
| zingolib/src/wallet/legacy.rs | 47135 | `b62b1298d59ecd1675f9bb3f5041a768fc05e0de051ce41eb31c513e79bce55f` | 0 |
| zingolib/src/wallet/locks.rs | 2231 | `6847e34f54ef72be7ca09b757d707df1b356f15e73da056b50407d1f590667df` | 0 |
| zingolib/src/wallet/migration.rs | 9964 | `48493b259118c4eb9e12485c46e154d985b32ab927c826c91e2decd2b566839f` | 0 |
| zingolib/src/wallet/migration/immediate.rs | 16735 | `7ea6a3e1508f03142bf34df9c7c664b509740318520d03ad2d17f29a3fac8a3b` | 0 |
| zingolib/src/wallet/migration/params.rs | 8714 | `70551a1ba528ad0c098de19a373563a91fc61b56916a07f2dfd21651111fda10` | 0 |
| zingolib/src/wallet/migration/parts.rs | 55458 | `004117d5aafc450d9a4c4469037c2cc77b860600b17b1507231b3368d493ee7c` | 0 |
| zingolib/src/wallet/migration/quantize.rs | 5853 | `d6b01c0ae6318a95106d5a23097a9ba952adf0cf5e4451def21d5b983dbb3606` | 0 |
| zingolib/src/wallet/migration/reconcile.rs | 38949 | `b096cfb755b539cbac399d57586f3065cd79c24656dfd192d097e0c5b14f29ed` | 0 |
| zingolib/src/wallet/migration/schedule.rs | 70399 | `18e62d4f50d6d09121d139452ced31a2452fb67a61b675a2f683d92d382f310e` | 0 |
| zingolib/src/wallet/migration/split.rs | 57989 | `f806beadec15ed682576aff22a336ab623bf69067cca087fcb32a417397e07f6` | 0 |
| zingolib/src/wallet/migration/store.rs | 34624 | `7997abb8136933f23ca28ef1975d717d352ac3982e53ecafc27d9892b78c3f19` | 0 |
| zingolib/src/wallet/migration/transmission.rs | 2830 | `e9cd2167896c6ada513466e89f37f05a067d66e762166b99bc1b10b9dcf7534f` | 0 |
| zingolib/src/wallet/note_selection.rs | 13420 | `f999bbe8adf797b3f582e3fa448a047685ebccfadbe739da6104e1f69401361a` | 0 |
| zingolib/src/wallet/output.rs | 21897 | `94842f9e8278f7f202810c93042f79465cfaf7eb87b94a2895807a2a5e253b20` | 0 |
| zingolib/src/wallet/output/query.rs | 5993 | `fc565576eab13dbb642acb9bc70c4fd43d8ee8744bba5924be1cd99e26ce344e` | 0 |
| zingolib/src/wallet/propose.rs | 23739 | `133de2fa44bf99ab28b4cf56338c8a5fa42127fbd9168181679ea7442e5b53d2` | 0 |
| zingolib/src/wallet/send.rs | 24467 | `e77583dfa7c1bc83728056338580991c1ba740bd56bb737519ce9979b8d2657e` | 0 |
| zingolib/src/wallet/summary.rs | 31830 | `1ab0f52f257a6a52dea889b91b31ee6c7851b2b411b3488614b030934545faaf` | 0 |
| zingolib/src/wallet/summary/data.rs | 26368 | `b95e8e3cafe3f51e398996fffe6ea75b71c48e2f8a2c4e65368955c1fccffe5e` | 0 |
| zingolib/src/wallet/sync.rs | 10743 | `c4f8a725caa3b51f9b97be0bb9258cc9685c53705dfb861899eb332216f0ba7b` | 0 |
| zingolib/src/wallet/traits.rs | 1555 | `ed5ae03fb7f21d77e0a16fa996e92b395034cbb02911d0eb282d6c65229aaeff` | 0 |
| zingolib/src/wallet/transaction.rs | 11413 | `cf130bfefe3fe658e76b84d5670d5991d8bd176c11c989d65b6c6002b84a173e` | 0 |
| zingolib/src/wallet/transparent.rs | 22236 | `abffb82b3977e5f8584191e8a3cd698c8fd4738ee5cff3c340fb12b3e5ebf4f4` | 0 |
| zingolib/src/wallet/utils.rs | 8119 | `3bbd271a52e5dd297ba6b99ed0ec1e5f0e141797f51d5942293e67813fddea07` | 0 |
| zingolib/src/wallet/zcb_traits.rs | 47499 | `44f65fc5b82c6b926a4938232e06d94b6908c5e76fbf86c65636744b90677bd3` | 0 |
| docs/adr/tools/workbench/Cargo.lock | 153 | `8cecd3765ca005ee9a5a1563a656bdfc8342854daafa01b1bb3cbf2bc7de9d80` | 0 |
| docs/adr/tools/workbench/Cargo.toml | 262 | `17e98a2e156107998e089666d4e4a7dcb10da280aa39fb93167f5a223c645657` | 0 |
| docs/adr/tools/workbench/src/bin/check-records.rs | 1018 | `fde5ac25fe9434efe94575d7b7f6181704dcbae59e131db75da9a1f15fe88375` | 0 |
| docs/adr/tools/workbench/src/lib.rs | 13520 | `7c126f77e40447ac84161d44ff9355f0cc72be66368e86fcf2422d0939a9767c` | 0 |
