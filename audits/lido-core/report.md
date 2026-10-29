# Отчёт об аудите безопасности и постквантовой готовности

**Проект:** lido-core @ 2bd532298d85 · Lido — публичный репозиторий (пассивная проверка)
| | |
|---|---|
| Организация | QSI |
| Дата отчёта | 2026-10-29 05:26 UTC |
| Версия отчёта | 1 |
| Запуск аудита | 8abdf060-c96a-4135-963c-b3e114a0a16e (Документальный аудит) |
| Версия анализатора | qsi-engine 1.2.0 |
| Профиль риска | Финансовая организация |
| SHA-256 содержимого | `c266fde0a890e83c5e80ded8062b5964727a2b971ca6b6d0d6a81227ffa65cca` |
| Ключ подписи (Ed25519, отпечаток SHA-256; подпись — отдельный файл report.sig.json) | `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e` |
> Отчёт содержит результаты автоматизированного и документального анализа в указанных границах. Он не является юридическим заключением, сертификацией или подтверждением соответствия какому-либо стандарту.

## 1. Резюме для руководства

- Критическая: **5**
- Высокая: **25**
- Средняя: **27**
- Низкая: **12**
- Информационная: **7**

- Подтверждённая техническая уязвимость: 0
- Известная уязвимая версия компонента: 46
- Подтверждённая ошибка конфигурации: 0
- Потенциальный криптографический риск: 9
- Долгосрочный постквантовый риск: 5
- Рекомендация по улучшению: 15
- Недостаточность данных: 1

Неравенство Моски (x + y > z): x = 10, y = 5, z = 8 → при этом сценарии миграция завершится слишком поздно. _z — плановое допущение профиля риска, а не прогноз. Публично известного криптографически значимого квантового компьютера сегодня не существует._

**Постквантовая зрелость: Уровень 0 из 4 — постквантовой криптографии нет.** Следующий шаг: Проведите инвентаризацию: где классическая криптография с открытым ключом защищает долгоживущие данные и ключи, и выберите первую миграцию — обычно гибридный обмен ключами TLS и обёрнутые ключи.

## 2. Область и границы проверки

Режим: Документальный аудит

Репозиторий: <https://github.com/lidofinance/core> @ `2bd532298d85cdf520169fdc0c5fb0cc9baf03c3` — ссылки в доказательствах открывают строки на этом коммите.

267 файлов, всего 2531440 байт, редактирований: 16; список SHA-256 по файлам — в приложении C.

## 3. Методология

| Область | Статус | Количество | Примеры |
|---|---|---|---|
| source_code | проверено | 147 | .solcover.js: 19 lines scanned with 16 rule patterns and 123 registry patterns; commitlint.config.ts: 1 lines scanned with 16 rule patterns and 123 registry patterns; eslint.config.mjs: 68 lines scanned with 16 rule patterns and 123 registry patterns |
| smart_contracts | проверено | 116 | contracts/0.4.24/Lido.sol: built-in Solidity pattern checks; contracts/0.4.24/StETH.sol: built-in Solidity pattern checks; contracts/0.4.24/lib/StakeLimitUtils.sol: built-in Solidity pattern checks |
| slither | не проверено | 116 | slither is not installed on the server (pip install slither-analyzer + solc) |
| secrets | проверено | 8 | contracts/0.4.24/nos/NodeOperatorsRegistry.sol: 3 redacted value(s) not reported (comments, test modules, fixture declarations, placeholders, values the source annotates as published, or hex values not bound to a secret name); contracts/0.4.24/template/LidoTemplate.sol: 4 redacted value(s) not reported (comments, test modules, fixture declarations, placeholders, values the source annotates as published, or hex values not bound to a secret name); contracts/0.8.25/vaults/VaultHub.sol: 1 redacted value(s) not reported (comments, test modules, fixture declarations, placeholders, values the source annotates as published, or hex values not bound to a secret name) |
| dependencies | проверено | 4 | package.json: 66 dependencies parsed (58 pinned); poetry.lock: 50 dependencies parsed (50 pinned); pyproject.toml: 1 dependencies parsed (0 pinned) |
| tls_key_exchange_groups | Недостаточность данных | 50 | poetry.lock line 9: not in the algorithm registry, not assessed: ["dev"]; poetry.lock line 21: not in the algorithm registry, not assessed: ["dev"]; poetry.lock line 163: not in the algorithm registry, not assessed: ["dev"] |
| tls_configuration | проверено | 1 | poetry.lock: openssl TLS directives parsed |
| osv_advisories | проверено | 1 | 1000 pinned packages queried at OSV.dev; 44 affected (23 of them only in development or build dependencies) |
| osv_advisories | Недостаточность данных | 1 | npm/axios@1.17.0: 22 advisories at OSV.dev, the first 20 are listed as findings; see OSV.dev for the rest |

_Длинные списки здесь сгруппированы; полный список по файлам — в JSON-версии отчёта, подписанной тем же ключом._

## 4. Проверенные и непроверенные активы

- slither — не проверено: 116 (примеры: slither is not installed on the server (pip install slither-analyzer + solc))
- tls_key_exchange_groups — Недостаточность данных: 50 (примеры: poetry.lock line 9: not in the algorithm registry, not assessed: ["dev"]; poetry.lock line 21: not in the algorithm registry, not assessed: ["dev"]; poetry.lock line 163: not in the algorithm registry, not assessed: ["dev"])
- osv_advisories — Недостаточность данных: 1 (примеры: npm/axios@1.17.0: 22 advisories at OSV.dev, the first 20 are listed as findings; see OSV.dev for the rest)

## 5. Краткое описание архитектуры

Static review of the source tree lido-core at 2bd532298d85cdf520169fdc0c5fb0cc9baf03c3. 267 files analysed; of 966 files, 579 are test, fuzzing, benchmark or example code and were left out, 120 are not read by any analyzer, 0 exceed the per-file limit and 0 did not fit the total limit. No requests were sent to the owner's systems.

## 6. Общая оценка состояния безопасности

- Ориентировочный индекс состояния: **0** / 100 — _Рассчитан по находкам в области проверки (подтверждённые и потенциальные проблемы, взвешенные по серьёзности). Ориентировочный; не сравним между аудитами с разной областью._
- Доля квантово-уязвимых элементов инвентаризации: 10.1%

## 7. Подробное описание находок

### QSI-2026-06310 — @openzeppelin/contracts 3.4.0 затронут GHSA-fg47-3c2x-m2wr (CVE-2021-39167)

- Серьёзность: **Критическая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/@openzeppelin/contracts@3.4.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 05:26 UTC
- Балл приоритета: 56.3 / 100
- CVSS v3.1: 10.0 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H`)

OSV.dev сообщает GHSA-fg47-3c2x-m2wr (CVE-2021-39167) для пакета npm @openzeppelin/contracts версии 3.4.0: TimelockController vulnerability in OpenZeppelin Contracts. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-fg47-3c2x-m2wr
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-fg47-3c2x-m2wr](https://osv.dev/vulnerability/GHSA-fg47-3c2x-m2wr) · manifest · SHA-256 86eb53dbf7f2f383bea068a3275c14665b036b3f07e4a8678f285bc72a5a5bf2_

```
{"id": "GHSA-fg47-3c2x-m2wr", "aliases": ["CVE-2021-39167"], "modified": "2026-07-08T06:29:37.864167374Z", "summary": "TimelockController vulnerability in OpenZeppelin Contracts ", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (3.4.2, 4.3.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06316 — babel-traverse 6.26.0 затронут GHSA-67hx-6x53-jw92 (CVE-2023-45133)

- Серьёзность: **Критическая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/babel-traverse@6.26.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 05:26 UTC
- Балл приоритета: 42.2 / 100
- CVSS v3.1: 9.3 (`CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H`)

OSV.dev сообщает GHSA-67hx-6x53-jw92 (CVE-2023-45133) для пакета npm babel-traverse версии 6.26.0: Babel vulnerable to arbitrary code execution when compiling specifically crafted malicious code. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-67hx-6x53-jw92
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-67hx-6x53-jw92](https://osv.dev/vulnerability/GHSA-67hx-6x53-jw92) · line 3860 · SHA-256 16deafe8a82a19a1da77ffa3a401198bb44013849d3199210d59703b275ac8ef_

```
{"id": "GHSA-67hx-6x53-jw92", "aliases": ["CVE-2023-45133"], "modified": "2026-09-10T03:50:03.372029556Z", "summary": "Babel vulnerable to arbitrary code execution when compiling specifically crafted malicious code", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (пока не выпущена; меры смягчения — в бюллетене).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06334 — crypto-js 3.3.0 затронут GHSA-rg76-677x-56q9 (CVE-2026-71851)

- Серьёзность: **Критическая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/crypto-js@3.3.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 05:26 UTC
- Балл приоритета: 42.2 / 100
- CVSS v3.1: 9.0 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H`)

OSV.dev сообщает GHSA-rg76-677x-56q9 (CVE-2026-71851) для пакета npm crypto-js версии 3.3.0: crypto-js: Insufficient Entropy in Cryptographic Secret Generation via Vulnerable CryptoJS Dependency Chain. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-rg76-677x-56q9
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-rg76-677x-56q9](https://osv.dev/vulnerability/GHSA-rg76-677x-56q9) · line 4895 · SHA-256 45ef5e2c85f8298a81a897c421678b61711a1259852c9f1dbc85acadfed4319b_

```
{"id": "GHSA-rg76-677x-56q9", "aliases": ["CVE-2026-71851"], "modified": "2026-08-07T19:10:56.177489Z", "summary": "crypto-js: Insufficient Entropy in Cryptographic Secret Generation via Vulnerable CryptoJS Dependency Chain", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (4.0.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06335 — crypto-js 3.3.0 затронут GHSA-xwcq-pm8m-c4vf (CVE-2023-46233)

- Серьёзность: **Критическая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/crypto-js@3.3.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 05:26 UTC
- Балл приоритета: 42.2 / 100
- CVSS v3.1: 9.1 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N`)

OSV.dev сообщает GHSA-xwcq-pm8m-c4vf (CVE-2023-46233) для пакета npm crypto-js версии 3.3.0: crypto-js PBKDF2 1,000 times weaker than specified in 1993 and 1.3M times weaker than current standard. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-xwcq-pm8m-c4vf
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-xwcq-pm8m-c4vf](https://osv.dev/vulnerability/GHSA-xwcq-pm8m-c4vf) · line 4895 · SHA-256 ae191f4cba25690e02746ff5b9880f65d1d3647459773db918723c96e120fe53_

```
{"id": "GHSA-xwcq-pm8m-c4vf", "aliases": ["CVE-2023-46233"], "modified": "2026-09-10T03:49:58.831533491Z", "summary": "crypto-js PBKDF2 1,000 times weaker than specified in 1993 and 1.3M times weaker than current standard", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (4.2.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06337 — form-data 2.3.3 затронут GHSA-fjxv-7rqg-78g4 (CVE-2025-7783)

- Серьёзность: **Критическая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/form-data@2.3.3`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 05:26 UTC
- Балл приоритета: 42.2 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-fjxv-7rqg-78g4 (CVE-2025-7783) для пакета npm form-data версии 2.3.3: form-data uses unsafe random function in form-data for choosing boundary. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-fjxv-7rqg-78g4
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-fjxv-7rqg-78g4](https://osv.dev/vulnerability/GHSA-fjxv-7rqg-78g4) · line 6440 · SHA-256 200dcd18c0390a88f15584c7e7ac24e130dcb5b2add9e4c07c40ed5e3f8671d9_

```
{"id": "GHSA-fjxv-7rqg-78g4", "aliases": ["CVE-2025-7783"], "modified": "2026-09-10T03:50:57.924154051Z", "summary": "form-data uses unsafe random function in form-data for choosing boundary", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (2.5.4, 3.0.4, 4.0.4).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06309 — @openzeppelin/contracts 3.4.0 затронут GHSA-88g8-f5mf-f5rj (CVE-2021-46320, CVE-2022-39384, GHSA-9c22-pwxw-p6hx)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/@openzeppelin/contracts@3.4.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 05:26 UTC
- Балл приоритета: 52.3 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N`)

OSV.dev сообщает GHSA-88g8-f5mf-f5rj (CVE-2021-46320, CVE-2022-39384, GHSA-9c22-pwxw-p6hx) для пакета npm @openzeppelin/contracts версии 3.4.0: Improper Initialization in OpenZeppelin. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-88g8-f5mf-f5rj
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-88g8-f5mf-f5rj](https://osv.dev/vulnerability/GHSA-88g8-f5mf-f5rj) · manifest · SHA-256 996bac0e638469194a1b75976040bcee2010b168f1eb320290c0278f3b315376_

```
{"id": "GHSA-88g8-f5mf-f5rj", "aliases": ["CVE-2021-46320", "CVE-2022-39384", "GHSA-9c22-pwxw-p6hx"], "modified": "2026-07-16T03:56:17.546633851Z", "summary": "Improper Initialization in OpenZeppelin", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (4.4.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06339 — glob 10.4.5 затронут GHSA-5j98-mcp5-4vw2 (CVE-2025-64756)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/glob@10.4.5`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 05:26 UTC
- Балл приоритета: 52.3 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H`)

OSV.dev сообщает GHSA-5j98-mcp5-4vw2 (CVE-2025-64756) для пакета npm glob версии 10.4.5: glob CLI: Command injection via -c/--cmd executes matches with shell:true. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-5j98-mcp5-4vw2
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-5j98-mcp5-4vw2](https://osv.dev/vulnerability/GHSA-5j98-mcp5-4vw2) · line 6758 · SHA-256 884949ec1d5b0afc49c5012a13d4ca725389d36fedb5f13b4b032100d7b7bda4_

```
{"id": "GHSA-5j98-mcp5-4vw2", "aliases": ["CVE-2025-64756"], "modified": "2026-09-10T03:50:30.568830409Z", "summary": "glob CLI: Command injection via -c/--cmd executes matches with shell:true", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (10.5.0, 11.1.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06317 — base-x 3.0.10 затронут GHSA-xq7p-g2vc-g82p (CVE-2025-27611)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/base-x@3.0.10`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 05:26 UTC
- Балл приоритета: 39.2 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-xq7p-g2vc-g82p (CVE-2025-27611) для пакета npm base-x версии 3.0.10: Homograph attack allows Unicode lookalike characters to bypass validation. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-xq7p-g2vc-g82p
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-xq7p-g2vc-g82p](https://osv.dev/vulnerability/GHSA-xq7p-g2vc-g82p) · line 3924 · SHA-256 adfe81a5ece5d60980882038b464f57071b5092ad5a6c69e4d69044756f04c0e_

```
{"id": "GHSA-xq7p-g2vc-g82p", "aliases": ["CVE-2025-27611"], "modified": "2025-05-01T13:30:57Z", "summary": "Homograph attack allows Unicode lookalike characters to bypass validation.", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (3.0.11, 4.0.1, 5.0.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06321 — brace-expansion 2.0.1 затронут GHSA-6j4f-fj2g-mc7p (CVE-2026-102276)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/brace-expansion@2.0.1`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 05:26 UTC
- Балл приоритета: 39.2 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-6j4f-fj2g-mc7p (CVE-2026-102276) для пакета npm brace-expansion версии 2.0.1: brace-expansion: DoS via uncontrolled recursion in parseCommaParts causing stack exhaustion. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-6j4f-fj2g-mc7p
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-6j4f-fj2g-mc7p](https://osv.dev/vulnerability/GHSA-6j4f-fj2g-mc7p) · line 4053 · SHA-256 cf933227a5523b6f51c16be2051db199cf5f5331c14d818f4a5f89484522a199_

```
{"id": "GHSA-6j4f-fj2g-mc7p", "aliases": ["CVE-2026-102276"], "modified": "2026-09-30T00:00:03.836613572Z", "summary": "brace-expansion: DoS via uncontrolled recursion in parseCommaParts causing stack exhaustion", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.1.19, 2.1.5, 3.0.7, 5.0.10).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06323 — brace-expansion 2.0.1 затронут GHSA-mh99-v99m-4gvg (CVE-2026-14257)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/brace-expansion@2.0.1`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 05:26 UTC
- Балл приоритета: 39.2 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-mh99-v99m-4gvg (CVE-2026-14257) для пакета npm brace-expansion версии 2.0.1: brace-expansion: DoS via unbounded expansion length causing an out-of-memory process crash. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-mh99-v99m-4gvg
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-mh99-v99m-4gvg](https://osv.dev/vulnerability/GHSA-mh99-v99m-4gvg) · line 4053 · SHA-256 d3117282a2602bb20fb4abcbba05bbf2452002d7fcdb74af027e5332394cda52_

```
{"id": "GHSA-mh99-v99m-4gvg", "aliases": ["CVE-2026-14257"], "modified": "2026-09-10T03:50:12.282849322Z", "summary": "brace-expansion: DoS via unbounded expansion length causing an out-of-memory process crash", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.1.17, 2.1.3, 3.0.3, 5.0.8).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06325 — brace-expansion 2.0.1 затронут GHSA-qhr7-859c-m2p7 (CVE-2026-102278)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/brace-expansion@2.0.1`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 05:26 UTC
- Балл приоритета: 39.2 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-qhr7-859c-m2p7 (CVE-2026-102278) для пакета npm brace-expansion версии 2.0.1: brace-expansion: DoS via uncontrolled recursion on nested brace groups causing stack exhaustion. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-qhr7-859c-m2p7
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-qhr7-859c-m2p7](https://osv.dev/vulnerability/GHSA-qhr7-859c-m2p7) · line 4053 · SHA-256 275e692c3e2352812e486e115c46ddfbc08d41860e0602c22f5e55a57cd20be1_

```
{"id": "GHSA-qhr7-859c-m2p7", "aliases": ["CVE-2026-102278"], "modified": "2026-09-30T00:00:04.402763332Z", "summary": "brace-expansion: DoS via uncontrolled recursion on nested brace groups causing stack exhaustion", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.1.20, 2.1.6, 3.0.8, 5.0.11).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06326 — brace-expansion 2.0.1 затронут GHSA-rgw5-rvv9-x895 (CVE-2026-69152)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/brace-expansion@2.0.1`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 05:26 UTC
- Балл приоритета: 39.2 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-rgw5-rvv9-x895 (CVE-2026-69152) для пакета npm brace-expansion версии 2.0.1: brace-expansion: DoS via unbounded intermediate arrays, bypassing the CVE-2026-14257 mitigation. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-rgw5-rvv9-x895
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-rgw5-rvv9-x895](https://osv.dev/vulnerability/GHSA-rgw5-rvv9-x895) · line 4053 · SHA-256 ca241c0fa4e3f0d01fcb36167c9abb890f5b550ae235da27e144275f8621c589_

```
{"id": "GHSA-rgw5-rvv9-x895", "aliases": ["CVE-2026-69152"], "modified": "2026-09-10T03:51:14.535270857Z", "summary": "brace-expansion: DoS via unbounded intermediate arrays, bypassing the CVE-2026-14257 mitigation", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.1.18, 2.1.4, 3.0.6, 5.0.9).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06328 — browserslist 3.2.8 затронут GHSA-73wf-gq98-2v4g (CVE-2026-73088)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/browserslist@3.2.8`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 05:26 UTC
- Балл приоритета: 39.2 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-73wf-gq98-2v4g (CVE-2026-73088) для пакета npm browserslist версии 3.2.8: Browserslist: Uncaught crash / prototype write via untrusted browserslist-stats.json custom stats (normalizeStats). Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-73wf-gq98-2v4g
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-73wf-gq98-2v4g](https://osv.dev/vulnerability/GHSA-73wf-gq98-2v4g) · line 4106 · SHA-256 2112289ce3a004c38a13bf02ac58d42f49e6f4eaa4422aae00cbd798fc8fa039_

```
{"id": "GHSA-73wf-gq98-2v4g", "aliases": ["CVE-2026-73088"], "modified": "2026-09-10T03:51:15.295037659Z", "summary": "Browserslist: Uncaught crash / prototype write via untrusted browserslist-stats.json custom stats (normalizeStats)", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (4.28.7).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06329 — browserslist 3.2.8 затронут GHSA-c83g-rgw3-j3cx (CVE-2026-73089)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/browserslist@3.2.8`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 05:26 UTC
- Балл приоритета: 39.2 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-c83g-rgw3-j3cx (CVE-2026-73089) для пакета npm browserslist версии 3.2.8: Browserslist: Unbounded memory growth (no cache eviction) via distinct query results, leading to eventual OOM. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-c83g-rgw3-j3cx
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-c83g-rgw3-j3cx](https://osv.dev/vulnerability/GHSA-c83g-rgw3-j3cx) · line 4106 · SHA-256 8ee3bc1907ee3700bea8977475c5e16b814cf1559a2bcf1f4bf806e615205237_

```
{"id": "GHSA-c83g-rgw3-j3cx", "aliases": ["CVE-2026-73089"], "modified": "2026-09-10T03:50:54.622936829Z", "summary": "Browserslist: Unbounded memory growth (no cache eviction) via distinct query results, leading to eventual OOM", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (4.28.7).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06330 — browserslist 4.24.4 затронут GHSA-73wf-gq98-2v4g (CVE-2026-73088)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/browserslist@4.24.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 05:26 UTC
- Балл приоритета: 39.2 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-73wf-gq98-2v4g (CVE-2026-73088) для пакета npm browserslist версии 4.24.4: Browserslist: Uncaught crash / prototype write via untrusted browserslist-stats.json custom stats (normalizeStats). Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-73wf-gq98-2v4g
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-73wf-gq98-2v4g](https://osv.dev/vulnerability/GHSA-73wf-gq98-2v4g) · line 4118 · SHA-256 2112289ce3a004c38a13bf02ac58d42f49e6f4eaa4422aae00cbd798fc8fa039_

```
{"id": "GHSA-73wf-gq98-2v4g", "aliases": ["CVE-2026-73088"], "modified": "2026-09-10T03:51:15.295037659Z", "summary": "Browserslist: Uncaught crash / prototype write via untrusted browserslist-stats.json custom stats (normalizeStats)", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (4.28.7).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06331 — browserslist 4.24.4 затронут GHSA-c83g-rgw3-j3cx (CVE-2026-73089)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/browserslist@4.24.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 05:26 UTC
- Балл приоритета: 39.2 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-c83g-rgw3-j3cx (CVE-2026-73089) для пакета npm browserslist версии 4.24.4: Browserslist: Unbounded memory growth (no cache eviction) via distinct query results, leading to eventual OOM. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-c83g-rgw3-j3cx
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-c83g-rgw3-j3cx](https://osv.dev/vulnerability/GHSA-c83g-rgw3-j3cx) · line 4118 · SHA-256 8ee3bc1907ee3700bea8977475c5e16b814cf1559a2bcf1f4bf806e615205237_

```
{"id": "GHSA-c83g-rgw3-j3cx", "aliases": ["CVE-2026-73089"], "modified": "2026-09-10T03:50:54.622936829Z", "summary": "Browserslist: Unbounded memory growth (no cache eviction) via distinct query results, leading to eventual OOM", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (4.28.7).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06332 — browserslist 4.24.5 затронут GHSA-73wf-gq98-2v4g (CVE-2026-73088)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/browserslist@4.24.5`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 05:26 UTC
- Балл приоритета: 39.2 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-73wf-gq98-2v4g (CVE-2026-73088) для пакета npm browserslist версии 4.24.5: Browserslist: Uncaught crash / prototype write via untrusted browserslist-stats.json custom stats (normalizeStats). Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-73wf-gq98-2v4g
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-73wf-gq98-2v4g](https://osv.dev/vulnerability/GHSA-73wf-gq98-2v4g) · line 4132 · SHA-256 2112289ce3a004c38a13bf02ac58d42f49e6f4eaa4422aae00cbd798fc8fa039_

```
{"id": "GHSA-73wf-gq98-2v4g", "aliases": ["CVE-2026-73088"], "modified": "2026-09-10T03:51:15.295037659Z", "summary": "Browserslist: Uncaught crash / prototype write via untrusted browserslist-stats.json custom stats (normalizeStats)", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (4.28.7).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06333 — browserslist 4.24.5 затронут GHSA-c83g-rgw3-j3cx (CVE-2026-73089)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/browserslist@4.24.5`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 05:26 UTC
- Балл приоритета: 39.2 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-c83g-rgw3-j3cx (CVE-2026-73089) для пакета npm browserslist версии 4.24.5: Browserslist: Unbounded memory growth (no cache eviction) via distinct query results, leading to eventual OOM. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-c83g-rgw3-j3cx
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-c83g-rgw3-j3cx](https://osv.dev/vulnerability/GHSA-c83g-rgw3-j3cx) · line 4132 · SHA-256 8ee3bc1907ee3700bea8977475c5e16b814cf1559a2bcf1f4bf806e615205237_

```
{"id": "GHSA-c83g-rgw3-j3cx", "aliases": ["CVE-2026-73089"], "modified": "2026-09-10T03:50:54.622936829Z", "summary": "Browserslist: Unbounded memory growth (no cache eviction) via distinct query results, leading to eventual OOM", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (4.28.7).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06338 — form-data 2.3.3 затронут GHSA-hmw2-7cc7-3qxx (CVE-2026-12143)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/form-data@2.3.3`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 05:26 UTC
- Балл приоритета: 39.2 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N`)

OSV.dev сообщает GHSA-hmw2-7cc7-3qxx (CVE-2026-12143) для пакета npm form-data версии 2.3.3: form-data: CRLF injection in form-data via unescaped multipart field names and filenames. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-hmw2-7cc7-3qxx
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-hmw2-7cc7-3qxx](https://osv.dev/vulnerability/GHSA-hmw2-7cc7-3qxx) · line 6440 · SHA-256 64b88e5adc882b4c0f6f6fe0a51634707e810628ea92673780b5017357695e14_

```
{"id": "GHSA-hmw2-7cc7-3qxx", "aliases": ["CVE-2026-12143"], "modified": "2026-09-10T03:50:49.785679067Z", "summary": "form-data: CRLF injection in form-data via unescaped multipart field names and filenames", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N"}, {"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (2.5.6, 3.0.5, 4.0.6).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06342 — ip-address 9.0.5 затронут GHSA-mwp4-54f8-5fhr (CVE-2026-69192)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/ip-address@9.0.5`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 05:26 UTC
- Балл приоритета: 39.2 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-mwp4-54f8-5fhr (CVE-2026-69192) для пакета npm ip-address версии 9.0.5: ip-address: Address4 decodes leading-zero octets as decimal while resolvers decode them as octal, allowing SSRF and trust-boundary bypass. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-mwp4-54f8-5fhr
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-mwp4-54f8-5fhr](https://osv.dev/vulnerability/GHSA-mwp4-54f8-5fhr) · line 7537 · SHA-256 c806462494712890cdd6af18d5f8c78a0e74fc09a95f719a902a673d49919138_

```
{"id": "GHSA-mwp4-54f8-5fhr", "aliases": ["CVE-2026-69192"], "modified": "2026-09-10T03:51:14.478555296Z", "summary": "ip-address: Address4 decodes leading-zero octets as decimal while resolvers decode them as octal, allowing SSRF and trust-boundary bypass", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:N/VA:N/SC:H/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (10.3.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06346 — json5 0.5.1 затронут GHSA-9c47-m6qq-7p4h (CVE-2022-46175)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/json5@0.5.1`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 05:26 UTC
- Балл приоритета: 39.2 / 100
- CVSS v3.1: 7.1 (`CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:L/A:H`)

OSV.dev сообщает GHSA-9c47-m6qq-7p4h (CVE-2022-46175) для пакета npm json5 версии 0.5.1: Prototype Pollution in JSON5 via Parse Method. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-9c47-m6qq-7p4h
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-9c47-m6qq-7p4h](https://osv.dev/vulnerability/GHSA-9c47-m6qq-7p4h) · line 8204 · SHA-256 69d5be41912ef346bff847de93316cfe1437d11c75f6767d69321d599b281989_

```
{"id": "GHSA-9c47-m6qq-7p4h", "aliases": ["CVE-2022-46175"], "modified": "2026-09-10T03:49:56.250129993Z", "summary": "Prototype Pollution in JSON5 via Parse Method", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:L/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.0.2, 2.2.2).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06348 — lodash 4.17.21 затронут GHSA-r5fr-rjxr-66jc (CVE-2026-4800)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/lodash@4.17.21`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 05:26 UTC
- Балл приоритета: 39.2 / 100
- CVSS v3.1: 8.1 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H`)

OSV.dev сообщает GHSA-r5fr-rjxr-66jc (CVE-2026-4800) для пакета npm lodash версии 4.17.21: lodash vulnerable to Code Injection via `_.template` imports key names. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-r5fr-rjxr-66jc
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-r5fr-rjxr-66jc](https://osv.dev/vulnerability/GHSA-r5fr-rjxr-66jc) · line 8713 · SHA-256 30a32ee3a99869b8f1266d8d87dff3946cc5ec16e4a57567776608ebc1c57530_

```
{"id": "GHSA-r5fr-rjxr-66jc", "aliases": ["CVE-2026-4800"], "modified": "2026-10-17T02:56:15.633068434Z", "summary": "lodash vulnerable to Code Injection via `_.template` imports key names", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (4.18.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06350 — minimatch 9.0.5 затронут GHSA-23c5-xmqv-rm74 (CVE-2026-27904)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/minimatch@9.0.5`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 05:26 UTC
- Балл приоритета: 39.2 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-23c5-xmqv-rm74 (CVE-2026-27904) для пакета npm minimatch версии 9.0.5: minimatch ReDoS: nested *() extglobs generate catastrophically backtracking regular expressions. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-23c5-xmqv-rm74
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-23c5-xmqv-rm74](https://osv.dev/vulnerability/GHSA-23c5-xmqv-rm74) · line 9036 · SHA-256 f25d4148233e76d337e4c8e1f77365b5ed08f4f131db657f142d4e41e5938cc8_

```
{"id": "GHSA-23c5-xmqv-rm74", "aliases": ["CVE-2026-27904"], "modified": "2026-09-10T03:50:59.274637421Z", "summary": "minimatch ReDoS: nested *() extglobs generate catastrophically backtracking regular expressions", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (10.2.3, 3.1.4, 4.2.5, 5.1.8, 6.2.2).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06351 — minimatch 9.0.5 затронут GHSA-3ppc-4f35-3m26 (CVE-2026-26996)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/minimatch@9.0.5`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 05:26 UTC
- Балл приоритета: 39.2 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-3ppc-4f35-3m26 (CVE-2026-26996) для пакета npm minimatch версии 9.0.5: minimatch has a ReDoS via repeated wildcards with non-matching literal in pattern. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-3ppc-4f35-3m26
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-3ppc-4f35-3m26](https://osv.dev/vulnerability/GHSA-3ppc-4f35-3m26) · line 9036 · SHA-256 7894decfdb9401924dfb1c0193887a6fd01ea775ac42078a4ec0aa0bb5583313_

```
{"id": "GHSA-3ppc-4f35-3m26", "aliases": ["CVE-2026-26996"], "modified": "2026-09-10T03:50:33.812431744Z", "summary": "minimatch has a ReDoS via repeated wildcards with non-matching literal in pattern", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (10.2.1, 3.1.3, 4.2.4, 5.1.7, 6.2.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06352 — minimatch 9.0.5 затронут GHSA-7r86-cg39-jmmj (CVE-2026-27903)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/minimatch@9.0.5`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 05:26 UTC
- Балл приоритета: 39.2 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-7r86-cg39-jmmj (CVE-2026-27903) для пакета npm minimatch версии 9.0.5: minimatch has ReDoS: matchOne() combinatorial backtracking via multiple non-adjacent GLOBSTAR segments. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-7r86-cg39-jmmj
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-7r86-cg39-jmmj](https://osv.dev/vulnerability/GHSA-7r86-cg39-jmmj) · line 9036 · SHA-256 54f5b8f4a3d673e969a7611b462e7ce231023fad3786124a18e7a6fd44d41be3_

```
{"id": "GHSA-7r86-cg39-jmmj", "aliases": ["CVE-2026-27903"], "modified": "2026-09-10T03:50:34.376990726Z", "summary": "minimatch has ReDoS: matchOne() combinatorial backtracking via multiple non-adjacent GLOBSTAR segments", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (10.2.3, 3.1.3, 4.2.5, 5.1.8, 6.2.2).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06353 — node-fetch 1.7.3 затронут GHSA-r683-j2x4-v87g (CVE-2022-0235)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/node-fetch@1.7.3`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 05:26 UTC
- Балл приоритета: 39.2 / 100
- CVSS v3.1: 8.8 (`CVSS:3.0/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H`)

OSV.dev сообщает GHSA-r683-j2x4-v87g (CVE-2022-0235) для пакета npm node-fetch версии 1.7.3: node-fetch forwards secure headers to untrusted sites. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-r683-j2x4-v87g
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-r683-j2x4-v87g](https://osv.dev/vulnerability/GHSA-r683-j2x4-v87g) · line 9294 · SHA-256 ffdb73eb723f433cb75a6bf12f9f12801bacfd1a2d67752b0fdb5af52efccafd_

```
{"id": "GHSA-r683-j2x4-v87g", "aliases": ["CVE-2022-0235"], "modified": "2023-11-08T04:07:30.211593Z", "summary": "node-fetch forwards secure headers to untrusted sites", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.0/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (2.6.7, 3.1.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06281 — initialize() без модификатора initializer в contracts/0.4.24/Lido.sol

- Серьёзность: **Высокая** · Классификация: Потенциальный криптографический риск · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `contract:contracts/0.4.24/Lido.sol`
- Источник данных: contracts/0.4.24/Lido.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-29 05:26 UTC
- Балл приоритета: 36.1 / 100
- CVSS v3.1: неприменимо

Функция initialize в строка 276 не имеет защиты initializer/onlyInitializing. (см. SWC-118)

**Возможные последствия.** В обновляемых прокси кто угодно может (пере)инициализировать контракт и стать владельцем.

**Шаги воспроизведения.**

```
Откройте строка 276 в предоставленном файле contracts/0.4.24/Lido.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [contracts/0.4.24/Lido.sol](https://github.com/lidofinance/core/blob/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3/contracts/0.4.24/Lido.sol#L276) · line 276 · SHA-256 d58bc402a0d6c6e329e8cc825bfa0962f991fdfcec167aec5a6796220984c63c_

```
  274 |      * @dev The contract's balance must be non-zero to mint initial shares of stETH
  275 |      */
  276 |     function initialize(address _lidoLocator, address _eip712StETH, uint256 _depositsReserveTarget) public payable onlyInit {
  277 |         _bootstrapInitialHolder(); // stone in the elevator
  278 | 
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте OpenZeppelin Initializable (модификатор initializer) и отключите инициализаторы в конструкторе реализации.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-06283 — initialize() без модификатора initializer в contracts/0.4.24/nos/NodeOperatorsRegistry.sol

- Серьёзность: **Высокая** · Классификация: Потенциальный криптографический риск · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `contract:contracts/0.4.24/nos/NodeOperatorsRegistry.sol`
- Источник данных: contracts/0.4.24/nos/NodeOperatorsRegistry.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-29 05:26 UTC
- Балл приоритета: 36.1 / 100
- CVSS v3.1: неприменимо

Функция initialize в строка 219 не имеет защиты initializer/onlyInitializing. (см. SWC-118)

**Возможные последствия.** В обновляемых прокси кто угодно может (пере)инициализировать контракт и стать владельцем.

**Шаги воспроизведения.**

```
Откройте строка 219 в предоставленном файле contracts/0.4.24/nos/NodeOperatorsRegistry.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [contracts/0.4.24/nos/NodeOperatorsRegistry.sol](https://github.com/lidofinance/core/blob/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3/contracts/0.4.24/nos/NodeOperatorsRegistry.sol#L219) · line 219 · SHA-256 4100b3b42fb08b9468abd9aa5a6b302faed9cd0a57cc58786259ba67b96d3454_

```
  217 |     // METHODS
  218 |     //
  219 |     function initialize(
  220 |         address _locator,
  221 |         bytes32 _type,
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте OpenZeppelin Initializable (модификатор initializer) и отключите инициализаторы в конструкторе реализации.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-06289 — initialize() без модификатора initializer в contracts/0.8.9/oracle/AccountingOracle.sol

- Серьёзность: **Высокая** · Классификация: Потенциальный криптографический риск · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `contract:contracts/0.8.9/oracle/AccountingOracle.sol`
- Источник данных: contracts/0.8.9/oracle/AccountingOracle.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-29 05:26 UTC
- Балл приоритета: 36.1 / 100
- CVSS v3.1: неприменимо

Функция initialize в строка 128 не имеет защиты initializer/onlyInitializing. (см. SWC-118)

**Возможные последствия.** В обновляемых прокси кто угодно может (пере)инициализировать контракт и стать владельцем.

**Шаги воспроизведения.**

```
Откройте строка 128 в предоставленном файле contracts/0.8.9/oracle/AccountingOracle.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [contracts/0.8.9/oracle/AccountingOracle.sol](https://github.com/lidofinance/core/blob/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3/contracts/0.8.9/oracle/AccountingOracle.sol#L128) · line 128 · SHA-256 b8d556bf9c13c8d31567e9e72c63f38e078d768a41cffe740e43808508dfd432_

```
  126 |     }
  127 | 
  128 |     function initialize(
  129 |         address admin,
  130 |         address consensusContract,
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте OpenZeppelin Initializable (модификатор initializer) и отключите инициализаторы в конструкторе реализации.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-06290 — initialize() без модификатора initializer в contracts/0.8.9/oracle/ValidatorsExitBusOracle.sol

- Серьёзность: **Высокая** · Классификация: Потенциальный криптографический риск · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `contract:contracts/0.8.9/oracle/ValidatorsExitBusOracle.sol`
- Источник данных: contracts/0.8.9/oracle/ValidatorsExitBusOracle.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-29 05:26 UTC
- Балл приоритета: 36.1 / 100
- CVSS v3.1: неприменимо

Функция initialize в строка 57 не имеет защиты initializer/onlyInitializing. (см. SWC-118)

**Возможные последствия.** В обновляемых прокси кто угодно может (пере)инициализировать контракт и стать владельцем.

**Шаги воспроизведения.**

```
Откройте строка 57 в предоставленном файле contracts/0.8.9/oracle/ValidatorsExitBusOracle.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [contracts/0.8.9/oracle/ValidatorsExitBusOracle.sol](https://github.com/lidofinance/core/blob/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3/contracts/0.8.9/oracle/ValidatorsExitBusOracle.sol#L57) · line 57 · SHA-256 6d7e79109c4d547ec756f0fea4c85b0cac33078b6f1f22d70aab05bb20a5b616_

```
   55 |     {}
   56 | 
   57 |     function initialize(
   58 |         address admin,
   59 |         address consensusContract,
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте OpenZeppelin Initializable (модификатор initializer) и отключите инициализаторы в конструкторе реализации.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-06308 — @openzeppelin/contracts 3.4.0 затронут GHSA-7grf-83vw-6f5x (CVE-2022-35915)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/@openzeppelin/contracts@3.4.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 05:26 UTC
- Балл приоритета: 46.3 / 100
- CVSS v3.1: 5.3 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L`)

OSV.dev сообщает GHSA-7grf-83vw-6f5x (CVE-2022-35915) для пакета npm @openzeppelin/contracts версии 3.4.0: OpenZeppelin Contracts ERC165Checker unbounded gas consumption. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-7grf-83vw-6f5x
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-7grf-83vw-6f5x](https://osv.dev/vulnerability/GHSA-7grf-83vw-6f5x) · manifest · SHA-256 ffee1bb6ddbfa8b9508b54da394ec3feb5c2fa941801a23b0fd7ac68f12044c9_

```
{"id": "GHSA-7grf-83vw-6f5x", "aliases": ["CVE-2022-35915"], "modified": "2023-11-08T04:09:52.370855Z", "summary": "OpenZeppelin Contracts ERC165Checker unbounded gas consumption", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (4.7.2).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06311 — @openzeppelin/contracts 3.4.0 затронут GHSA-mx2q-35m2-x2rh (CVE-2023-30541)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/@openzeppelin/contracts@3.4.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 05:26 UTC
- Балл приоритета: 46.3 / 100
- CVSS v3.1: 5.3 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L`)

OSV.dev сообщает GHSA-mx2q-35m2-x2rh (CVE-2023-30541) для пакета npm @openzeppelin/contracts версии 3.4.0: OpenZeppelin Contracts TransparentUpgradeableProxy clashing selector calls may not be delegated. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-mx2q-35m2-x2rh
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-mx2q-35m2-x2rh](https://osv.dev/vulnerability/GHSA-mx2q-35m2-x2rh) · manifest · SHA-256 9938c96d508f58617efcda784b16cc41209d560903b9f3dcf596d4fa32319fd1_

```
{"id": "GHSA-mx2q-35m2-x2rh", "aliases": ["CVE-2023-30541"], "modified": "2026-09-10T03:50:01.099654307Z", "summary": "OpenZeppelin Contracts TransparentUpgradeableProxy clashing selector calls may not be delegated", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (4.8.3).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06312 — openzeppelin-solidity 2.0.0 затронут GHSA-7grf-83vw-6f5x (CVE-2022-35915)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/openzeppelin-solidity@2.0.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 05:26 UTC
- Балл приоритета: 46.3 / 100
- CVSS v3.1: 5.3 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L`)

OSV.dev сообщает GHSA-7grf-83vw-6f5x (CVE-2022-35915) для пакета npm openzeppelin-solidity версии 2.0.0: OpenZeppelin Contracts ERC165Checker unbounded gas consumption. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-7grf-83vw-6f5x
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-7grf-83vw-6f5x](https://osv.dev/vulnerability/GHSA-7grf-83vw-6f5x) · manifest · SHA-256 ffee1bb6ddbfa8b9508b54da394ec3feb5c2fa941801a23b0fd7ac68f12044c9_

```
{"id": "GHSA-7grf-83vw-6f5x", "aliases": ["CVE-2022-35915"], "modified": "2023-11-08T04:09:52.370855Z", "summary": "OpenZeppelin Contracts ERC165Checker unbounded gas consumption", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (пока не выпущена; меры смягчения — в бюллетене).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06313 — setuptools 78.1.1 затронут GHSA-h35f-9h28-mq5c (CVE-2026-59890, PYSEC-2026-3447)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:PyPI/setuptools@78.1.1`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 05:26 UTC
- Балл приоритета: 46.3 / 100
- CVSS v3.1: 6.1 (`CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:L/A:N`)

OSV.dev сообщает GHSA-h35f-9h28-mq5c (CVE-2026-59890, PYSEC-2026-3447) для пакета PyPI setuptools версии 78.1.1: setuptools: MANIFEST.in exclusion bypass in sdist via Unicode normalization collision (NFC/NFD) on macOS APFS/HFS+. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-h35f-9h28-mq5c
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-h35f-9h28-mq5c](https://osv.dev/vulnerability/GHSA-h35f-9h28-mq5c) · manifest · SHA-256 1166784dc7e5b42d06ff0612777d5403986f90db8c0f417fe00e4619e77bbcd0_

```
{"id": "GHSA-h35f-9h28-mq5c", "aliases": ["BIT-setuptools-2026-59890", "CVE-2026-59890", "PYSEC-2026-3447"], "modified": "2026-09-10T03:50:52.323347787Z", "summary": "setuptools: MANIFEST.in exclusion bypass in sdist via Unicode normalization collision (NFC/NFD) on macOS APFS/HFS+", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:L/A:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (83.0.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06282 — Solidity < 0.8 без встроенных проверок переполнения (0.4.24) в 7 файл(ах)

- Серьёзность: **Средняя** · Классификация: Потенциальный криптографический риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `solidity:compiler:0.4.24`
- Источник данных: contracts/0.4.24/lib/StakeLimitUtils.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-29 05:26 UTC
- Балл приоритета: 43.0 / 100
- CVSS v3.1: неприменимо

pragma 0.4.24 в 7 файл(ах), впервые в contracts/0.4.24/lib/StakeLimitUtils.sol:5; использование SafeMath: no. При SafeMath серьёзность снижена до низкой: проверки есть в коде. (см. SWC-101)

**Возможные последствия.** Переполнение арифметики может исказить балансы там, где его не охраняет проверка в духе SafeMath.

**Шаги воспроизведения.**

```
Откройте contracts/0.4.24/lib/StakeLimitUtils.sol:5 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [contracts/0.4.24/lib/StakeLimitUtils.sol](https://github.com/lidofinance/core/blob/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3/contracts/0.4.24/lib/StakeLimitUtils.sol#L5) · line 5 · SHA-256 57abb8ce724ed1595b4b5c5099e24ae0d7d46684bbabd946477dd8fadbbaa8a4_

```
    3 | 
    4 | /* See contracts/COMPILERS.md */
    5 | pragma solidity 0.4.24;
    6 | 
    7 | import {UnstructuredStorage} from "@aragon/os/contracts/common/UnstructuredStorage.sol";
```

_file_excerpt · [contracts/0.4.24/template/IETHRegistrarController.sol](https://github.com/lidofinance/core/blob/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3/contracts/0.4.24/template/IETHRegistrarController.sol#L5) · line 5 · SHA-256 9ab23f5e110d6c9952e20a5a03c218c4e193faff24d522e297766ef6307e0923_

```
    3 | // SPDX-License-Identifier: GPL-3.0
    4 | 
    5 | pragma solidity 0.4.24;
    6 | 
    7 | interface IETHRegistrarController {
```

_file_excerpt · [contracts/0.4.24/template/IInterfaceResolver.sol](https://github.com/lidofinance/core/blob/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3/contracts/0.4.24/template/IInterfaceResolver.sol#L5) · line 5 · SHA-256 64dc856fb7a5a422b2e4f73ac9572737a2e0479dde8cca5b049345eb8afe47f2_

```
    3 | // SPDX-License-Identifier: GPL-3.0
    4 | 
    5 | pragma solidity 0.4.24;
    6 | 
    7 | interface IInterfaceResolver {
```

_file_excerpt · [contracts/0.4.24/template/Imports.sol](https://github.com/lidofinance/core/blob/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3/contracts/0.4.24/template/Imports.sol#L5) · line 5 · SHA-256 ce21d85aaaf14996c1cd9fbdf0a43838712f36412629f1527ae3d1ce941d64a5_

```
    3 | // SPDX-License-Identifier: GPL-3.0
    4 | 
    5 | pragma solidity 0.4.24;
    6 | 
    7 | import "@aragon/id/contracts/FIFSResolvingRegistrar.sol";
```

_file_excerpt · [contracts/0.4.24/template/LidoTemplate.sol](https://github.com/lidofinance/core/blob/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3/contracts/0.4.24/template/LidoTemplate.sol#L5) · line 5 · SHA-256 389f37393ef0122bfaaa8809e587293894efa99a2a91f5eb95063fc50c3d83b2_

```
    3 | // SPDX-License-Identifier: GPL-3.0
    4 | 
    5 | pragma solidity 0.4.24;
    6 | 
    7 | import {APMRegistryFactory} from "@aragon/os/contracts/factory/APMRegistryFactory.sol";
```

_file_excerpt · [contracts/0.4.24/utils/UnstructuredStorageExt.sol](https://github.com/lidofinance/core/blob/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3/contracts/0.4.24/utils/UnstructuredStorageExt.sol#L7) · line 7 · SHA-256 670c8f1478bbf4587715d9be4324d7f7684d49f68404ba2f39f77b716473ac54_

```
    5 | // See contracts/COMPILERS.md
    6 | // solhint-disable-next-line
    7 | pragma solidity 0.4.24;
    8 | 
    9 | 
```

_file_excerpt · [contracts/0.4.24/utils/Versioned.sol](https://github.com/lidofinance/core/blob/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3/contracts/0.4.24/utils/Versioned.sol#L3) · line 3 · SHA-256 9edf3c046928a76a50b9a95f55a9cba91b8f2397d5e618b63baa60de0d08cb13_

```
    1 | // SPDX-FileCopyrightText: 2023 Lido <info@lido.fi>
    2 | // SPDX-License-Identifier: GPL-3.0
    3 | pragma solidity 0.4.24;
    4 | 
    5 | import "@aragon/os/contracts/common/UnstructuredStorage.sol";
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Перейдите на Solidity ≥ 0.8 или последовательно используйте SafeMath.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-06285 — Solidity < 0.8 без встроенных проверок переполнения (0.6.11) в 1 файл(ах)

- Серьёзность: **Средняя** · Классификация: Потенциальный криптографический риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `solidity:compiler:0.6.11`
- Источник данных: contracts/0.6.11/deposit_contract.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-29 05:26 UTC
- Балл приоритета: 43.0 / 100
- CVSS v3.1: неприменимо

pragma 0.6.11 в 1 файл(ах), впервые в contracts/0.6.11/deposit_contract.sol:12; использование SafeMath: no. При SafeMath серьёзность снижена до низкой: проверки есть в коде. (см. SWC-101)

**Возможные последствия.** Переполнение арифметики может исказить балансы там, где его не охраняет проверка в духе SafeMath.

**Шаги воспроизведения.**

```
Откройте contracts/0.6.11/deposit_contract.sol:12 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [contracts/0.6.11/deposit_contract.sol](https://github.com/lidofinance/core/blob/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3/contracts/0.6.11/deposit_contract.sol#L12) · line 12 · SHA-256 df96a7324c50113cc5a9a726b2cfde3112e1f77d03daefe28f54ef2580a92ba9_

```
   10 | // SPDX-License-Identifier: CC0-1.0
   11 | 
   12 | pragma solidity 0.6.11;
   13 | 
   14 | // This interface is designed to be compatible with the Vyper version.
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Перейдите на Solidity ≥ 0.8 или последовательно используйте SafeMath.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-06286 — Solidity < 0.8 без встроенных проверок переполнения (0.6.12) в 1 файл(ах)

- Серьёзность: **Средняя** · Классификация: Потенциальный криптографический риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `solidity:compiler:0.6.12`
- Источник данных: contracts/0.6.12/interfaces/IStETH.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-29 05:26 UTC
- Балл приоритета: 43.0 / 100
- CVSS v3.1: неприменимо

pragma 0.6.12 в 1 файл(ах), впервые в contracts/0.6.12/interfaces/IStETH.sol:5; использование SafeMath: no. При SafeMath серьёзность снижена до низкой: проверки есть в коде. (см. SWC-101)

**Возможные последствия.** Переполнение арифметики может исказить балансы там, где его не охраняет проверка в духе SafeMath.

**Шаги воспроизведения.**

```
Откройте contracts/0.6.12/interfaces/IStETH.sol:5 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [contracts/0.6.12/interfaces/IStETH.sol](https://github.com/lidofinance/core/blob/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3/contracts/0.6.12/interfaces/IStETH.sol#L5) · line 5 · SHA-256 6953edd42eb95a1428ca3bf35c8a0b18fadb2af40cd5b19e3d0d44bbcb2b0239_

```
    3 | // SPDX-License-Identifier: GPL-3.0
    4 | 
    5 | pragma solidity 0.6.12; // latest available for using OZ
    6 | 
    7 | import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Перейдите на Solidity ≥ 0.8 или последовательно используйте SafeMath.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-06300 — Прямое использование ecrecover в contracts/common/lib/ECDSA.sol

- Серьёзность: **Средняя** · Классификация: Потенциальный криптографический риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `contract:contracts/common/lib/ECDSA.sol`
- Источник данных: contracts/common/lib/ECDSA.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-29 05:26 UTC
- Балл приоритета: 43.0 / 100
- CVSS v3.1: неприменимо

ecrecover в строка 40. (см. SWC-117/SWC-121)

**Возможные последствия.** Без проверок s-значения/нулевого адреса и nonce подписи могут быть изменяемыми или повторно используемыми. ecrecover основан на secp256k1 ECDSA (долгосрочно квантово-уязвим).

**Шаги воспроизведения.**

```
Откройте строка 40 в предоставленном файле contracts/common/lib/ECDSA.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [contracts/common/lib/ECDSA.sol](https://github.com/lidofinance/core/blob/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3/contracts/common/lib/ECDSA.sol#L40) · line 40 · SHA-256 83607227e296c689cb5b8094db2a2b14f5919036e6a07f97c4ca8bcce1ab15ea_

```
   38 | 
   39 |         // If the signature is valid (and not malleable), return the signer address
   40 |         address signer = ecrecover(hash, v, r, s);
   41 |         require(signer != address(0), "ECDSA: invalid signature");
   42 | 
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте OpenZeppelin ECDSA.recover с разделением доменов EIP-712 и nonce.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-06299 — Квантово-уязвимый ECDSA: подпись транзакций и сообщений (2 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `source-code:ECDSA:transaction_signing`
- Источник данных: contracts/common/lib/ECDSA.sol
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-29 05:26 UTC
- Балл приоритета: 39.6 / 100
- CVSS v3.1: неприменимо

2 упоминаний ECDSA в 2 файл(ах), например contracts/common/lib/ECDSA.sol:40. Роль по путям, именам функций и соседнему коду: подпись транзакций и сообщений. CRQC восстанавливает закрытый ключ по уже известному открытому (в блокчейне после первой траты, при повторном использовании адреса): средствам и подтверждениям под этими ключами нужен путь миграции.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте contracts/common/lib/ECDSA.sol:40 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [contracts/common/lib/ECDSA.sol](https://github.com/lidofinance/core/blob/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3/contracts/common/lib/ECDSA.sol#L40) · line 40 · SHA-256 83607227e296c689cb5b8094db2a2b14f5919036e6a07f97c4ca8bcce1ab15ea_

```
   38 | 
   39 |         // If the signature is valid (and not malleable), return the signer address
   40 |         address signer = ecrecover(hash, v, r, s);
   41 |         require(signer != address(0), "ECDSA: invalid signature");
   42 | 
```

_file_excerpt · [lib/eips/eip712.ts](https://github.com/lidofinance/core/blob/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3/lib/eips/eip712.ts#L41) · line 41 · SHA-256 57777a832a8ab6c54cd9be147ec73148b86c007e3b79c84951d9450045e1b22b_

```
   40 | 
   41 |   return signer.signTypedData(domain, types, permit).then((signature) => Signature.from(signature));
   42 | }
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Следите за постквантовыми планами каждой сети, не используйте открытые ключи повторно и держите подписание готовым к постквантовым схемам по мере их принятия сетями.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-06305 — Квантово-уязвимый ECDSA: роль не определена (1 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `source-code:ECDSA:general`
- Источник данных: lib/ec.ts
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-29 05:26 UTC
- Балл приоритета: 38.2 / 100
- CVSS v3.1: неприменимо

1 упоминаний ECDSA в 1 файл(ах), например lib/ec.ts:10. Роль по путям, именам функций и соседнему коду: роль не определена. По коду не видно, что защищают ключи; приоритет определит проверка.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте lib/ec.ts:10 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [lib/ec.ts](https://github.com/lidofinance/core/blob/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3/lib/ec.ts#L10) · line 10 · SHA-256 58b1fe5be584f1efb1e1914b4b01c0bd083c87538ae53d4817a214df9e4ab02d_

```
    9 | export function recover(messageHash: string, { v, r, s }: ECDSASignature) {
   10 |   const pubKey = ecrecover(Buffer.from(de0x(messageHash), "hex"), v, Buffer.from(r), Buffer.from(s));
   11 |   return toChecksumAddress(bufferToHex(pubToAddress(pubKey)));
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Классифицируйте каждое использование, зафиксируйте сроки жизни данных и запланируйте миграцию на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема; введите уровень абстракции для криптогибкости.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-06306 — Квантово-уязвимый BLS12-381: роль не определена (2 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `source-code:BLS12-381:general`
- Источник данных: lib/pdg.ts
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-29 05:26 UTC
- Балл приоритета: 38.2 / 100
- CVSS v3.1: неприменимо

4 упоминаний BLS12-381 в 2 файл(ах), например lib/pdg.ts:8. Роль по путям, именам функций и соседнему коду: роль не определена. По коду не видно, что защищают ключи; приоритет определит проверка.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте lib/pdg.ts:8 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [lib/pdg.ts](https://github.com/lidofinance/core/blob/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3/lib/pdg.ts#L8) · line 8 · SHA-256 66930079176ab32be697b7ee8c11d415ef4bc001470e72520f5f92ee259f5d6f_

```
    7 | import {
    8 |   BLS12_381,
    9 |   PredepositGuarantee,
```

_file_excerpt · [lib/pdg.ts](https://github.com/lidofinance/core/blob/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3/lib/pdg.ts#L71) · line 71 · SHA-256 7485cb9a1f58e84b9dde46c24f46c882a6142f25956b5e8b9342411f2c6b29c5_

```
   70 |   options = {} as GeneratePredepositOptions,
   71 | ): Promise<{ deposit: IStakingVault.DepositStruct; depositY: BLS12_381.DepositYStruct }> => {
   72 |   const { overrideAmount = ether("1"), depositDomain, pubkeyFlipBitmask, signatureFlipBitmask } = options;
```

_file_excerpt · [lib/protocol/helpers/vaults.ts](https://github.com/lidofinance/core/blob/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3/lib/protocol/helpers/vaults.ts#L23) · line 23 · SHA-256 9375a0e9d6aa327d4ab84c3c3a49ad3f27fdd59749ce652b31bd00a349412f14_

```
   22 | } from "typechain-types";
   23 | import { BLS12_381 } from "typechain-types/contracts/0.8.25/vaults/predeposit_guarantee/PredepositGuarantee";
   24 | 
```

_file_excerpt · [lib/protocol/helpers/vaults.ts](https://github.com/lidofinance/core/blob/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3/lib/protocol/helpers/vaults.ts#L616) · line 616 · SHA-256 5d6285f98dd015a4f1490800d95877021b2c607dfdae60b598513266e6fac602_

```
  615 |   deposit: IStakingVault.DepositStruct;
  616 |   depositY: BLS12_381.DepositYStruct;
  617 | }> => {
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Классифицируйте каждое использование, зафиксируйте сроки жизни данных и запланируйте миграцию на постквантовый алгоритм; введите уровень абстракции для криптогибкости.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-06287 — Криптография на спариваниях в контракте: BLS12-381 (contracts/0.8.25/CLValidatorVerifier.sol)

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `contract:contracts/0.8.25/CLValidatorVerifier.sol`
- Источник данных: contracts/0.8.25/CLValidatorVerifier.sol
- Метод обнаружения: Сопоставление шаблонов реестра с учётом комментариев.
- Анализатор: solidity 1.2.0 · 2026-10-29 05:26 UTC
- Балл приоритета: 34.7 / 100
- CVSS v3.1: неприменимо

contracts/0.8.25/CLValidatorVerifier.sol использует BLS12-381 (впервые в строка 8): эллиптические кривые со спариванием (прекомпилы alt_bn128 0x06–0x08 или BLS12-381 0x0b–0x11) и/или верификатор доказательств на спариваниях.

**Возможные последствия.** Они опираются на дискретный логарифм в группах эллиптических кривых, который алгоритм Шора решает на CRQC; доказательства или агрегированные подписи, принимаемые контрактом, тогда можно будет подделать. Сегодня не эксплуатируется.

**Шаги воспроизведения.**

```
Откройте строка 8 в предоставленном файле contracts/0.8.25/CLValidatorVerifier.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [contracts/0.8.25/CLValidatorVerifier.sol](https://github.com/lidofinance/core/blob/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3/contracts/0.8.25/CLValidatorVerifier.sol#L8) · line 8 · SHA-256 a11357c978519d6852673f72922d0ce2f6f6a5705c42eb3b08d902d142db93b2_

```
    6 | import {GIndex, pack, concat} from "contracts/common/lib/GIndex.sol";
    7 | import {SSZ} from "contracts/common/lib/SSZ.sol";
    8 | import {BLS12_381} from "contracts/common/lib/BLS.sol";
    9 | import {BeaconRootData, ValidatorWitness} from "contracts/common/interfaces/ValidatorWitness.sol";
   10 | 
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Обнаружение по шаблонам; используемую схему следует подтвердить по исходному коду верификатора.

**Рекомендация.** Внесите контракт в PQC-инвентаризацию и предусмотрите путь обновления (обновляемый верификатор, системы доказательств/подписи на хешах или решётках по мере их зрелости).

**Повторная проверка.** Повторите аудит после обновления верификатора.

### QSI-2026-06298 — Криптография на спариваниях в контракте: BLS12-381 (contracts/common/lib/BLS.sol)

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `contract:contracts/common/lib/BLS.sol`
- Источник данных: contracts/common/lib/BLS.sol
- Метод обнаружения: Сопоставление шаблонов реестра с учётом комментариев.
- Анализатор: solidity 1.2.0 · 2026-10-29 05:26 UTC
- Балл приоритета: 34.7 / 100
- CVSS v3.1: неприменимо

contracts/common/lib/BLS.sol использует BLS12-381 (впервые в строка 17): эллиптические кривые со спариванием (прекомпилы alt_bn128 0x06–0x08 или BLS12-381 0x0b–0x11) и/или верификатор доказательств на спариваниях.

**Возможные последствия.** Они опираются на дискретный логарифм в группах эллиптических кривых, который алгоритм Шора решает на CRQC; доказательства или агрегированные подписи, принимаемые контрактом, тогда можно будет подделать. Сегодня не эксплуатируется.

**Шаги воспроизведения.**

```
Откройте строка 17 в предоставленном файле contracts/common/lib/BLS.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [contracts/common/lib/BLS.sol](https://github.com/lidofinance/core/blob/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3/contracts/common/lib/BLS.sol#L17) · line 17 · SHA-256 8d7f4d005115cfe7831462f946a46d4f3335c1be5ce3c7c7bd3fca4b1083e6a7_

```
   15 |  */
   16 | // solhint-disable contract-name-capwords
   17 | library BLS12_381 {
   18 |     /*´:°•.°+.*•´.*:˚.°*.˚•´.°:°•.°•.*•´.*:˚.°*.˚•´.°:°•.°+.*•´.*:*/
   19 |     /*                          STRUCTS                           */
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Обнаружение по шаблонам; используемую схему следует подтвердить по исходному коду верификатора.

**Рекомендация.** Внесите контракт в PQC-инвентаризацию и предусмотрите путь обновления (обновляемый верификатор, системы доказательств/подписи на хешах или решётках по мере их зрелости).

**Повторная проверка.** Повторите аудит после обновления верификатора.

### QSI-2026-06315 — @babel/runtime 7.26.0 затронут GHSA-968p-4wvh-cqc8 (CVE-2025-27789)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/@babel/runtime@7.26.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 05:26 UTC
- Балл приоритета: 34.7 / 100
- CVSS v3.1: 6.2 (`CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-968p-4wvh-cqc8 (CVE-2025-27789) для пакета npm @babel/runtime версии 7.26.0: Babel has inefficient RegExp complexity in generated code with .replace when transpiling named capturing groups. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-968p-4wvh-cqc8
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-968p-4wvh-cqc8](https://osv.dev/vulnerability/GHSA-968p-4wvh-cqc8) · line 274 · SHA-256 7bc3174869552dd66bd418f9e04c71cb361db3e4d72f4664a1168cc739088da3_

```
{"id": "GHSA-968p-4wvh-cqc8", "aliases": ["CVE-2025-27789"], "modified": "2026-09-10T03:50:22.971593530Z", "summary": "Babel has inefficient RegExp complexity in generated code with .replace when transpiling named capturing groups", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (7.26.10, 8.0.0-alpha.17).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06318 — bn.js 4.12.1 затронут GHSA-378v-28hj-76wf (CVE-2026-2739)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/bn.js@4.12.1`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 05:26 UTC
- Балл приоритета: 34.7 / 100
- CVSS v3.1: 5.3 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L`)

OSV.dev сообщает GHSA-378v-28hj-76wf (CVE-2026-2739) для пакета npm bn.js версии 4.12.1: bn.js affected by an infinite loop. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-378v-28hj-76wf
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-378v-28hj-76wf](https://osv.dev/vulnerability/GHSA-378v-28hj-76wf) · line 4013 · SHA-256 a665b25e3f33b25353c831a6837c7c5e42986347b4df0bcf386ba3f03432bad3_

```
{"id": "GHSA-378v-28hj-76wf", "aliases": ["CVE-2026-2739"], "modified": "2026-09-10T03:50:33.815513385Z", "summary": "bn.js affected by an infinite loop", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L"}, {"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:N/E:P"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (4.12.3, 5.2.3).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06319 — bn.js 5.2.1 затронут GHSA-378v-28hj-76wf (CVE-2026-2739)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/bn.js@5.2.1`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 05:26 UTC
- Балл приоритета: 34.7 / 100
- CVSS v3.1: 5.3 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L`)

OSV.dev сообщает GHSA-378v-28hj-76wf (CVE-2026-2739) для пакета npm bn.js версии 5.2.1: bn.js affected by an infinite loop. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-378v-28hj-76wf
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-378v-28hj-76wf](https://osv.dev/vulnerability/GHSA-378v-28hj-76wf) · line 4020 · SHA-256 a665b25e3f33b25353c831a6837c7c5e42986347b4df0bcf386ba3f03432bad3_

```
{"id": "GHSA-378v-28hj-76wf", "aliases": ["CVE-2026-2739"], "modified": "2026-09-10T03:50:33.815513385Z", "summary": "bn.js affected by an infinite loop", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L"}, {"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:N/E:P"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (4.12.3, 5.2.3).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06320 — brace-expansion 2.0.1 затронут GHSA-3jxr-9vmj-r5cp (CVE-2026-13149)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/brace-expansion@2.0.1`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 05:26 UTC
- Балл приоритета: 34.7 / 100
- CVSS v3.1: 5.3 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L`)

OSV.dev сообщает GHSA-3jxr-9vmj-r5cp (CVE-2026-13149) для пакета npm brace-expansion версии 2.0.1: brace-expansion: DoS via exponential-time expansion of consecutive non-expanding {} groups. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-3jxr-9vmj-r5cp
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-3jxr-9vmj-r5cp](https://osv.dev/vulnerability/GHSA-3jxr-9vmj-r5cp) · line 4053 · SHA-256 12323a5cbb663a6ca957402ae997f8497a271e2b326429662e8243d69d0c9d09_

```
{"id": "GHSA-3jxr-9vmj-r5cp", "aliases": ["CVE-2026-13149"], "modified": "2026-09-10T03:51:10.092354944Z", "summary": "brace-expansion: DoS via exponential-time expansion of consecutive non-expanding {} groups", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L"}, {"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:P/S:N/AU:Y/R:U/V:D/RE:M/U:Amber"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.1.16, 2.1.2, 5.0.7).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06322 — brace-expansion 2.0.1 затронут GHSA-f886-m6hf-6m8v (CVE-2026-33750)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/brace-expansion@2.0.1`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 05:26 UTC
- Балл приоритета: 34.7 / 100
- CVSS v3.1: 6.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-f886-m6hf-6m8v (CVE-2026-33750) для пакета npm brace-expansion версии 2.0.1: brace-expansion: Zero-step sequence causes process hang and memory exhaustion. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-f886-m6hf-6m8v
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-f886-m6hf-6m8v](https://osv.dev/vulnerability/GHSA-f886-m6hf-6m8v) · line 4053 · SHA-256 946af967067c5a463e46f3d442313e467b2536f8004876dead0dee1cfeb5711d_

```
{"id": "GHSA-f886-m6hf-6m8v", "aliases": ["CVE-2026-33750"], "modified": "2026-09-10T03:51:00.342356761Z", "summary": "brace-expansion: Zero-step sequence causes process hang and memory exhaustion", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:N/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.1.13, 2.0.3, 3.0.2, 5.0.5).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06324 — brace-expansion 2.0.1 затронут GHSA-q2hr-2g5m-vwhr (CVE-2026-102277)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/brace-expansion@2.0.1`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 05:26 UTC
- Балл приоритета: 34.7 / 100
- CVSS v3.1: 5.3 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L`)

OSV.dev сообщает GHSA-q2hr-2g5m-vwhr (CVE-2026-102277) для пакета npm brace-expansion версии 2.0.1: brace-expansion: Quadratic-time expansion of the `{a},b}` rewrite causes CPU denial of service. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-q2hr-2g5m-vwhr
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-q2hr-2g5m-vwhr](https://osv.dev/vulnerability/GHSA-q2hr-2g5m-vwhr) · line 4053 · SHA-256 798c3854b19c9033c4e4ebcc2656a9cbdd2e1551dfba1a6307865066fff2c348_

```
{"id": "GHSA-q2hr-2g5m-vwhr", "aliases": ["CVE-2026-102277"], "modified": "2026-09-30T00:00:03.849541183Z", "summary": "brace-expansion: Quadratic-time expansion of the `{a},b}` rewrite causes CPU denial of service", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.1.21, 2.1.7, 3.0.9, 5.0.12).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06336 — elliptic 6.6.1 затронут GHSA-848j-6mx2-7j84 (CVE-2025-14505)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/elliptic@6.6.1`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 05:26 UTC
- Балл приоритета: 34.7 / 100
- CVSS v3.1: 5.6 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:L/A:L`)

OSV.dev сообщает GHSA-848j-6mx2-7j84 (CVE-2025-14505) для пакета npm elliptic версии 6.6.1: Elliptic Uses a Cryptographic Primitive with a Risky Implementation. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-848j-6mx2-7j84
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-848j-6mx2-7j84](https://osv.dev/vulnerability/GHSA-848j-6mx2-7j84) · line 5236 · SHA-256 c877c7b2da4802b65cb44f7fbd020c526da526417b59a4c119d33db038c1eaa2_

```
{"id": "GHSA-848j-6mx2-7j84", "aliases": ["CVE-2025-14505"], "modified": "2026-09-10T03:50:32.794069999Z", "summary": "Elliptic Uses a Cryptographic Primitive with a Risky Implementation", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:L/A:L"}, {"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:L/VI:L/VA:L/SC:N/SI:N/SA:N/E:P"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (пока не выпущена; меры смягчения — в бюллетене).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06340 — ip-address 9.0.5 затронут GHSA-h3mg-xc3c-68pw (CVE-2026-101911)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/ip-address@9.0.5`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 05:26 UTC
- Балл приоритета: 34.7 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-h3mg-xc3c-68pw (CVE-2026-101911) для пакета npm ip-address версии 9.0.5: ip-address: Address6 builds a parse diagnostic proportional to the input with no length bound, allowing a single long string to stall or crash the process. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-h3mg-xc3c-68pw
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-h3mg-xc3c-68pw](https://osv.dev/vulnerability/GHSA-h3mg-xc3c-68pw) · line 7537 · SHA-256 084104e164917fcb371e479d007af8b749882c861c64fcacd02041d6e2826f13_

```
{"id": "GHSA-h3mg-xc3c-68pw", "aliases": ["CVE-2026-101911"], "modified": "2026-09-30T00:00:04.407982988Z", "summary": "ip-address: Address6 builds a parse diagnostic proportional to the input with no length bound, allowing a single long string to stall or crash the process", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (10.7.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06341 — ip-address 9.0.5 затронут GHSA-j6r3-76f7-8jcv (CVE-2026-101912)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/ip-address@9.0.5`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 05:26 UTC
- Балл приоритета: 34.7 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-j6r3-76f7-8jcv (CVE-2026-101912) для пакета npm ip-address версии 9.0.5: ip-address: isInSubnet() and isHostInSubnet() compare addresses of different families as if they shared an address space, allowing an allowlist check to admit an address outside its range. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-j6r3-76f7-8jcv
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-j6r3-76f7-8jcv](https://osv.dev/vulnerability/GHSA-j6r3-76f7-8jcv) · line 7537 · SHA-256 b9f0b89bd954b0b0d9c1b4d78cdd26b719df1b9c13c106e6d87c1add480a2db7_

```
{"id": "GHSA-j6r3-76f7-8jcv", "aliases": ["CVE-2026-101912"], "modified": "2026-09-30T00:00:03.843448355Z", "summary": "ip-address: isInSubnet() and isHostInSubnet() compare addresses of different families as if they shared an address space, allowing an allowlist check to admit an address outside its range", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (10.7.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06343 — ip-address 9.0.5 затронут GHSA-rpw4-54j3-4h4q (CVE-2026-101913)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/ip-address@9.0.5`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 05:26 UTC
- Балл приоритета: 34.7 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-rpw4-54j3-4h4q (CVE-2026-101913) для пакета npm ip-address версии 9.0.5: ip-address: Address6.isLinkLocal() recognizes fe80::/64 rather than fe80::/10, allowing SSRF and trust-boundary bypass to on-link hosts. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-rpw4-54j3-4h4q
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-rpw4-54j3-4h4q](https://osv.dev/vulnerability/GHSA-rpw4-54j3-4h4q) · line 7537 · SHA-256 dc0bdf91e8de82dfc03986ef28acb52ed28cd0fe6e1c47fb73ddb402120d2d37_

```
{"id": "GHSA-rpw4-54j3-4h4q", "aliases": ["CVE-2026-101913"], "modified": "2026-09-28T21:00:05.359993143Z", "summary": "ip-address: Address6.isLinkLocal() recognizes fe80::/64 rather than fe80::/10, allowing SSRF and trust-boundary bypass to on-link hosts", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:L/VI:N/VA:N/SC:L/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (10.5.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06344 — ip-address 9.0.5 затронут GHSA-rxp7-6hxx-x8q5 (CVE-2026-111997)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/ip-address@9.0.5`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 05:26 UTC
- Балл приоритета: 34.7 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-rxp7-6hxx-x8q5 (CVE-2026-111997) для пакета npm ip-address версии 9.0.5: ip-address: Address6 matches a zone identifier in quadratic time ahead of its length limit, allowing a single long string to stall the process. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-rxp7-6hxx-x8q5
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-rxp7-6hxx-x8q5](https://osv.dev/vulnerability/GHSA-rxp7-6hxx-x8q5) · line 7537 · SHA-256 7dc8c20c8ae73d58d9b3ae97df00f6c5b5020d9aba1bf5eaa5bb382651e4fb20_

```
{"id": "GHSA-rxp7-6hxx-x8q5", "aliases": ["CVE-2026-111997"], "modified": "2026-10-22T16:30:30.129356757Z", "summary": "ip-address: Address6 matches a zone identifier in quadratic time ahead of its length limit, allowing a single long string to stall the process", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (10.7.4).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06345 — ip-address 9.0.5 затронут GHSA-v2v4-37r5-5v8g (CVE-2026-42338)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/ip-address@9.0.5`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 05:26 UTC
- Балл приоритета: 34.7 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-v2v4-37r5-5v8g (CVE-2026-42338) для пакета npm ip-address версии 9.0.5: ip-address has XSS in Address6 HTML-emitting methods. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-v2v4-37r5-5v8g
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-v2v4-37r5-5v8g](https://osv.dev/vulnerability/GHSA-v2v4-37r5-5v8g) · line 7537 · SHA-256 ec61fd0b64c02fcf0d991a9d6915e610a3e57e5f2c1e10e1b5495f8c6bf33e96_

```
{"id": "GHSA-v2v4-37r5-5v8g", "aliases": ["CVE-2026-42338"], "modified": "2026-09-10T03:50:47.603301077Z", "summary": "ip-address has XSS in Address6 HTML-emitting methods", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:L/VI:L/VA:N/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (10.1.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06347 — lodash 4.17.21 затронут GHSA-f23m-r3pf-42rh (CVE-2026-2950)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/lodash@4.17.21`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 05:26 UTC
- Балл приоритета: 34.7 / 100
- CVSS v3.1: 6.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:L`)

OSV.dev сообщает GHSA-f23m-r3pf-42rh (CVE-2026-2950) для пакета npm lodash версии 4.17.21: lodash vulnerable to Prototype Pollution via array path bypass in `_.unset` and `_.omit`. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-f23m-r3pf-42rh
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-f23m-r3pf-42rh](https://osv.dev/vulnerability/GHSA-f23m-r3pf-42rh) · line 8713 · SHA-256 f829d185af0521d1d9cdfb871e40105d15b0e8c3935c5f1c334af62ee9969ac6_

```
{"id": "GHSA-f23m-r3pf-42rh", "aliases": ["CVE-2026-2950"], "modified": "2026-10-17T02:56:13.084362346Z", "summary": "lodash vulnerable to Prototype Pollution via array path bypass in `_.unset` and `_.omit`", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:L"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (4.18.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06349 — lodash 4.17.21 затронут GHSA-xxjr-mmjv-4gpg (CVE-2025-13465)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/lodash@4.17.21`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 05:26 UTC
- Балл приоритета: 34.7 / 100
- CVSS v3.1: 6.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:L`)

OSV.dev сообщает GHSA-xxjr-mmjv-4gpg (CVE-2025-13465) для пакета npm lodash версии 4.17.21: Lodash has Prototype Pollution Vulnerability in `_.unset` and `_.omit` functions. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-xxjr-mmjv-4gpg
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-xxjr-mmjv-4gpg](https://osv.dev/vulnerability/GHSA-xxjr-mmjv-4gpg) · line 8713 · SHA-256 6f467919d9390f8e5f27ab05d05afeeb4c85df7ad2f81f04c1087e2ce75e96d7_

```
{"id": "GHSA-xxjr-mmjv-4gpg", "aliases": ["CVE-2025-13465"], "modified": "2026-10-17T02:55:54.229635593Z", "summary": "Lodash has Prototype Pollution Vulnerability in `_.unset` and `_.omit` functions", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:L"}, {"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:L/VA:L/SC:H/SI:H/SA:H/E:P"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (4.17.23).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06314 — setuptools 78.1.1 затронут GHSA-xmj3-9gf7-h52w

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:PyPI/setuptools@78.1.1`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 05:26 UTC
- Балл приоритета: 41.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-xmj3-9gf7-h52w для пакета PyPI setuptools версии 78.1.1: setuptools: Windows path escape via namespace_packages.txt during legacy wheel installation  Description. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-xmj3-9gf7-h52w
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-xmj3-9gf7-h52w](https://osv.dev/vulnerability/GHSA-xmj3-9gf7-h52w) · manifest · SHA-256 44a6682e9f91141fddf72661e8dee5d4e7d036a4cef5a380ef28d84b2f40c18f_

```
{"id": "GHSA-xmj3-9gf7-h52w", "aliases": [], "modified": "2026-10-23T22:00:03.739009766Z", "summary": "setuptools: Windows path escape via namespace_packages.txt during legacy wheel installation  Description", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:L/AC:H/AT:P/PR:L/UI:A/VC:N/VI:L/VA:L/SC:N/SI:N/SA:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (84.1.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06280 — Solidity < 0.8 без встроенных проверок переполнения (0.4.24) в 3 файл(ах)

- Серьёзность: **Низкая** · Классификация: Потенциальный криптографический риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `solidity:compiler:0.4.24`
- Источник данных: contracts/0.4.24/Lido.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-29 05:26 UTC
- Балл приоритета: 38.8 / 100
- CVSS v3.1: неприменимо

pragma 0.4.24 в 3 файл(ах), впервые в contracts/0.4.24/Lido.sol:5; использование SafeMath: yes. При SafeMath серьёзность снижена до низкой: проверки есть в коде. (см. SWC-101)

**Возможные последствия.** Переполнение арифметики может исказить балансы там, где его не охраняет проверка в духе SafeMath.

**Шаги воспроизведения.**

```
Откройте contracts/0.4.24/Lido.sol:5 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [contracts/0.4.24/Lido.sol](https://github.com/lidofinance/core/blob/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3/contracts/0.4.24/Lido.sol#L5) · line 5 · SHA-256 1a4dfc768395ba0b8d160472b523ad9efa5b93fd50d403f9d2ee1b86dd2f3db5_

```
    3 | 
    4 | /* See contracts/COMPILERS.md */
    5 | pragma solidity 0.4.24;
    6 | 
    7 | import {AragonApp, UnstructuredStorage} from "@aragon/os/contracts/apps/AragonApp.sol";
```

_file_excerpt · [contracts/0.4.24/StETH.sol](https://github.com/lidofinance/core/blob/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3/contracts/0.4.24/StETH.sol#L5) · line 5 · SHA-256 8b8575106d9a59657b97cbccd6b96ed95d2c36275471ee048f75c8eedf891bec_

```
    3 | 
    4 | /* See contracts/COMPILERS.md */
    5 | pragma solidity 0.4.24;
    6 | 
    7 | import {IERC20} from "openzeppelin-solidity/contracts/token/ERC20/IERC20.sol";
```

_file_excerpt · [contracts/0.4.24/nos/NodeOperatorsRegistry.sol](https://github.com/lidofinance/core/blob/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3/contracts/0.4.24/nos/NodeOperatorsRegistry.sol#L5) · line 5 · SHA-256 bfe8e1892929cd46cd361204531c9a6dc6f7f615a4f67f869d9122c31c5a4d56_

```
    3 | 
    4 | // See contracts/COMPILERS.md
    5 | pragma solidity 0.4.24;
    6 | 
    7 | import {AragonApp} from "@aragon/os/contracts/apps/AragonApp.sol";
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Перейдите на Solidity ≥ 0.8 или последовательно используйте SafeMath.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-06288 — Плавающая версия компилятора (>=0.8.0) в 4 файл(ах)

- Серьёзность: **Низкая** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `solidity:pragma:>=0.8.0`
- Источник данных: contracts/0.8.25/vaults/interfaces/IPinnedBeaconProxy.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-29 05:26 UTC
- Балл приоритета: 38.4 / 100
- CVSS v3.1: неприменимо

pragma >=0.8.0 в 4 файл(ах), впервые в contracts/0.8.25/vaults/interfaces/IPinnedBeaconProxy.sol:6. (см. SWC-103)

**Возможные последствия.** Контракты могут быть развёрнуты непроверенной версией компилятора. Фактический компилятор задаёт конфигурация сборки, которую эта проверка не читает.

**Шаги воспроизведения.**

```
Откройте contracts/0.8.25/vaults/interfaces/IPinnedBeaconProxy.sol:6 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [contracts/0.8.25/vaults/interfaces/IPinnedBeaconProxy.sol](https://github.com/lidofinance/core/blob/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3/contracts/0.8.25/vaults/interfaces/IPinnedBeaconProxy.sol#L6) · line 6 · SHA-256 6f531844245a6c032de39d91a78752de3f969b49361c058cb38500e1b53fa683_

```
    4 | // See contracts/COMPILERS.md
    5 | // solhint-disable-next-line lido/fixed-compiler-version
    6 | pragma solidity >=0.8.0;
    7 | 
    8 | /**
```

_file_excerpt · [contracts/0.8.25/vaults/interfaces/IPredepositGuarantee.sol](https://github.com/lidofinance/core/blob/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3/contracts/0.8.25/vaults/interfaces/IPredepositGuarantee.sol#L6) · line 6 · SHA-256 0cb55bcd817c0b7090d28a383a8a0bead64b5d8ecdd7197b1e8cab988fef3e07_

```
    4 | // See contracts/COMPILERS.md
    5 | // solhint-disable-next-line lido/fixed-compiler-version
    6 | pragma solidity >=0.8.0;
    7 | 
    8 | import {IStakingVault} from "./IStakingVault.sol";
```

_file_excerpt · [contracts/0.8.25/vaults/interfaces/IStakingVault.sol](https://github.com/lidofinance/core/blob/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3/contracts/0.8.25/vaults/interfaces/IStakingVault.sol#L6) · line 6 · SHA-256 34d88607dbab71ee232debf33df5d14e7044c83f9d94a9562445f2af012681bb_

```
    4 | // See contracts/COMPILERS.md
    5 | // solhint-disable-next-line lido/fixed-compiler-version
    6 | pragma solidity >=0.8.0;
    7 | 
    8 | import {IDepositContract} from "contracts/common/interfaces/IDepositContract.sol";
```

_file_excerpt · [contracts/common/interfaces/ILido.sol](https://github.com/lidofinance/core/blob/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3/contracts/common/interfaces/ILido.sol#L6) · line 6 · SHA-256 745dfe167069f25713b3f93353f872e1ca5f59ace2140ef39f8d5b5c034edfe5_

```
    4 | // See contracts/COMPILERS.md
    5 | // solhint-disable-next-line lido/fixed-compiler-version
    6 | pragma solidity >=0.8.0;
    7 | 
    8 | import {IERC20} from "@openzeppelin/contracts-v4.4/token/ERC20/IERC20.sol";
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Зафиксируйте версию компилятора, использованную при тестировании.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-06292 — Плавающая версия компилятора (>=0.4.24 <0.9.0) в 16 файл(ах)

- Серьёзность: **Низкая** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `solidity:pragma:>=0.4.24 <0.9.0`
- Источник данных: contracts/common/interfaces/IBurner.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-29 05:26 UTC
- Балл приоритета: 38.4 / 100
- CVSS v3.1: неприменимо

pragma >=0.4.24 <0.9.0 в 16 файл(ах), впервые в contracts/common/interfaces/IBurner.sol:6. (см. SWC-103)

**Возможные последствия.** Контракты могут быть развёрнуты непроверенной версией компилятора. Фактический компилятор задаёт конфигурация сборки, которую эта проверка не читает.

**Шаги воспроизведения.**

```
Откройте contracts/common/interfaces/IBurner.sol:6 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [contracts/common/interfaces/IBurner.sol](https://github.com/lidofinance/core/blob/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3/contracts/common/interfaces/IBurner.sol#L6) · line 6 · SHA-256 372d226cba7aa73df8f44aaae6ad353a5aba3a5ca55dc622e6e58a0b3b97022b_

```
    4 | // See contracts/COMPILERS.md
    5 | // solhint-disable-next-line
    6 | pragma solidity >=0.4.24 <0.9.0;
    7 | 
    8 | 
```

_file_excerpt · [contracts/common/interfaces/ICircuitBreaker.sol](https://github.com/lidofinance/core/blob/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3/contracts/common/interfaces/ICircuitBreaker.sol#L6) · line 6 · SHA-256 771ca4260272e693f119f524ade937d5dce82b3b3cc2d0e447add83385930eca_

```
    4 | // See contracts/COMPILERS.md
    5 | // solhint-disable-next-line
    6 | pragma solidity >=0.4.24 <0.9.0;
    7 | 
    8 | // https://github.com/lidofinance/circuit-breaker/blob/b4b2fbc921b3191560a3fc62d502d4bb98ad99e1/src/CircuitBreaker.sol
```

_file_excerpt · [contracts/common/interfaces/IEIP712StETH.sol](https://github.com/lidofinance/core/blob/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3/contracts/common/interfaces/IEIP712StETH.sol#L6) · line 6 · SHA-256 b57600745763ee76b8ad333d88ebd7bd09ed295e1b162aef24e931212e890460_

```
    4 | // See contracts/COMPILERS.md
    5 | // solhint-disable-next-line
    6 | pragma solidity >=0.4.24 <0.9.0;
    7 | 
    8 | /**
```

_file_excerpt · [contracts/common/interfaces/IGateSeal.sol](https://github.com/lidofinance/core/blob/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3/contracts/common/interfaces/IGateSeal.sol#L6) · line 6 · SHA-256 f5d1323025c1b4524b7c2e5f44e5c85564a16b6d2f72fd5d39b3bacae2db230c_

```
    4 | // See contracts/COMPILERS.md
    5 | // solhint-disable-next-line
    6 | pragma solidity >=0.4.24 <0.9.0;
    7 | 
    8 | // https://github.com/lidofinance/gate-seals/blob/main/contracts/GateSeal.vy
```

_file_excerpt · [contracts/common/interfaces/IGateSealFactory.sol](https://github.com/lidofinance/core/blob/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3/contracts/common/interfaces/IGateSealFactory.sol#L6) · line 6 · SHA-256 da411dd5561bc4c7c389328804612ee10b838ae190adfdcc26d9090e92f24a50_

```
    4 | // See contracts/COMPILERS.md
    5 | // solhint-disable-next-line
    6 | pragma solidity >=0.4.24 <0.9.0;
    7 | 
    8 | // https://github.com/lidofinance/gate-seals/blob/main/contracts/GateSealFactory.vy
```

_file_excerpt · [contracts/common/interfaces/ILidoLocator.sol](https://github.com/lidofinance/core/blob/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3/contracts/common/interfaces/ILidoLocator.sol#L6) · line 6 · SHA-256 8cda5c666b215be1a04f25d6668c634caf71337a7fa49c038edf617961ae9747_

```
    4 | // See contracts/COMPILERS.md
    5 | // solhint-disable-next-line lido/fixed-compiler-version
    6 | pragma solidity >=0.4.24 <0.9.0;
    7 | 
    8 | interface ILidoLocator {
```

_file_excerpt · [contracts/common/interfaces/IPausableUntil.sol](https://github.com/lidofinance/core/blob/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3/contracts/common/interfaces/IPausableUntil.sol#L6) · line 6 · SHA-256 b11c93b20da40a3ed28b86478c952595ddfb1bdb5925d8c07956f8b66903c924_

```
    4 | // See contracts/COMPILERS.md
    5 | // solhint-disable-next-line
    6 | pragma solidity >=0.4.24 <0.9.0;
    7 | 
    8 | /// @title  IPausableUntil
```

_file_excerpt · [contracts/common/lib/ECDSA.sol](https://github.com/lidofinance/core/blob/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3/contracts/common/lib/ECDSA.sol#L9) · line 9 · SHA-256 010cde526c2547b97897bb771b35c24e01d3b78c6733a3fcba1d71ef396cb717_

```
    7 | /* See contracts/COMPILERS.md */
    8 | // solhint-disable-next-line
    9 | pragma solidity >=0.4.24 <0.9.0;
   10 | 
   11 | 
```

_file_excerpt · [contracts/common/lib/Math256.sol](https://github.com/lidofinance/core/blob/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3/contracts/common/lib/Math256.sol#L8) · line 8 · SHA-256 f00b7b0492004183b3953ea494b302843de279ede54e202350d13a0f46d6a71c_

```
    6 | // See contracts/COMPILERS.md
    7 | // solhint-disable-next-line
    8 | pragma solidity >=0.4.24 <0.9.0;
    9 | 
   10 | library Math256 {
```

_file_excerpt · [contracts/common/lib/MemUtils.sol](https://github.com/lidofinance/core/blob/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3/contracts/common/lib/MemUtils.sol#L6) · line 6 · SHA-256 c15725824fab4faee10c4f3f1892a30c57571eff9d13dcd6c5c4a1233e68bb25_

```
    4 | /* See contracts/COMPILERS.md */
    5 | // solhint-disable-next-line lido/fixed-compiler-version
    6 | pragma solidity >=0.4.24 <0.9.0;
    7 | 
    8 | 
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Зафиксируйте версию компилятора, использованную при тестировании.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-06293 — Плавающая версия компилятора (>=0.5.0) в 7 файл(ах)

- Серьёзность: **Низкая** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `solidity:pragma:>=0.5.0`
- Источник данных: contracts/common/interfaces/IDepositContract.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-29 05:26 UTC
- Балл приоритета: 38.4 / 100
- CVSS v3.1: неприменимо

pragma >=0.5.0 в 7 файл(ах), впервые в contracts/common/interfaces/IDepositContract.sol:6. (см. SWC-103)

**Возможные последствия.** Контракты могут быть развёрнуты непроверенной версией компилятора. Фактический компилятор задаёт конфигурация сборки, которую эта проверка не читает.

**Шаги воспроизведения.**

```
Откройте contracts/common/interfaces/IDepositContract.sol:6 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [contracts/common/interfaces/IDepositContract.sol](https://github.com/lidofinance/core/blob/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3/contracts/common/interfaces/IDepositContract.sol#L6) · line 6 · SHA-256 34335c600067d334e770032e86d51a5f69c969ae424ebc353687d5c6c0986184_

```
    4 | // See contracts/COMPILERS.md
    5 | // solhint-disable-next-line lido/fixed-compiler-version
    6 | pragma solidity >=0.5.0;
    7 | 
    8 | interface IDepositContract {
```

_file_excerpt · [contracts/common/interfaces/IHashConsensus.sol](https://github.com/lidofinance/core/blob/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3/contracts/common/interfaces/IHashConsensus.sol#L6) · line 6 · SHA-256 5c54f4f58f92a937ed671a6040a017bc85987939211980b27fca053e2c96af97_

```
    4 | // See contracts/COMPILERS.md
    5 | // solhint-disable-next-line lido/fixed-compiler-version
    6 | pragma solidity >=0.5.0;
    7 | 
    8 | 
```

_file_excerpt · [contracts/common/interfaces/ILazyOracle.sol](https://github.com/lidofinance/core/blob/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3/contracts/common/interfaces/ILazyOracle.sol#L6) · line 6 · SHA-256 14f903c44fc99c3f829ce4b8c3d7764aee663b50ecfee33eac9025eb474dd04e_

```
    4 | // See contracts/COMPILERS.md
    5 | // solhint-disable-next-line lido/fixed-compiler-version
    6 | pragma solidity >=0.5.0;
    7 | 
    8 | /**
```

_file_excerpt · [contracts/common/interfaces/IStakingModule.sol](https://github.com/lidofinance/core/blob/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3/contracts/common/interfaces/IStakingModule.sol#L6) · line 6 · SHA-256 f6e3ea2dcb2955427b30641368ee998b067967aede2b795f142be54d38740ba1_

```
    4 | // See contracts/COMPILERS.md
    5 | // solhint-disable-next-line lido/fixed-compiler-version
    6 | pragma solidity >=0.5.0;
    7 | 
    8 | /// @title Lido's Staking Module interface
```

_file_excerpt · [contracts/common/interfaces/IVaultHub.sol](https://github.com/lidofinance/core/blob/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3/contracts/common/interfaces/IVaultHub.sol#L6) · line 6 · SHA-256 5c54f4f58f92a937ed671a6040a017bc85987939211980b27fca053e2c96af97_

```
    4 | // See contracts/COMPILERS.md
    5 | // solhint-disable-next-line lido/fixed-compiler-version
    6 | pragma solidity >=0.5.0;
    7 | 
    8 | 
```

_file_excerpt · [contracts/common/interfaces/IWithdrawalQueue.sol](https://github.com/lidofinance/core/blob/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3/contracts/common/interfaces/IWithdrawalQueue.sol#L6) · line 6 · SHA-256 56789afd50d1c20b7a6f9fcd56a8dac300246dc4824bd4a8ccb0726a49afc5e2_

```
    4 | // See contracts/COMPILERS.md
    5 | // solhint-disable-next-line lido/fixed-compiler-version
    6 | pragma solidity >=0.5.0;
    7 | 
    8 | interface IWithdrawalQueue {
```

_file_excerpt · [contracts/common/interfaces/ReportValues.sol](https://github.com/lidofinance/core/blob/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3/contracts/common/interfaces/ReportValues.sol#L6) · line 6 · SHA-256 a97bc72ec1ad2e92164aad9701f235d7dc3c9d1e3cc827edc9062e62b91e268e_

```
    4 | // See contracts/COMPILERS.md
    5 | // solhint-disable-next-line lido/fixed-compiler-version
    6 | pragma solidity >=0.5.0;
    7 | 
    8 | struct ReportValues {
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Зафиксируйте версию компилятора, использованную при тестировании.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-06294 — Плавающая версия компилятора (>=0.4.24) в 3 файл(ах)

- Серьёзность: **Низкая** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `solidity:pragma:>=0.4.24`
- Источник данных: contracts/common/interfaces/IOracleReportSanityChecker.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-29 05:26 UTC
- Балл приоритета: 38.4 / 100
- CVSS v3.1: неприменимо

pragma >=0.4.24 в 3 файл(ах), впервые в contracts/common/interfaces/IOracleReportSanityChecker.sol:6. (см. SWC-103)

**Возможные последствия.** Контракты могут быть развёрнуты непроверенной версией компилятора. Фактический компилятор задаёт конфигурация сборки, которую эта проверка не читает.

**Шаги воспроизведения.**

```
Откройте contracts/common/interfaces/IOracleReportSanityChecker.sol:6 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [contracts/common/interfaces/IOracleReportSanityChecker.sol](https://github.com/lidofinance/core/blob/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3/contracts/common/interfaces/IOracleReportSanityChecker.sol#L6) · line 6 · SHA-256 e526e96fbbac1f3d604b4c5f7067a574869d9e1c63fd8ba15658b0d2d7d769e1_

```
    4 | // See contracts/COMPILERS.md
    5 | // solhint-disable-next-line lido/fixed-compiler-version
    6 | pragma solidity >=0.4.24;
    7 | 
    8 | interface IOracleReportSanityChecker {
```

_file_excerpt · [contracts/common/interfaces/IOssifiableProxy.sol](https://github.com/lidofinance/core/blob/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3/contracts/common/interfaces/IOssifiableProxy.sol#L5) · line 5 · SHA-256 59d1ed32994e4553d0ec3ef5cb0bfc35eb8fe665ce6f33a006369915a91fe13c_

```
    3 | // See contracts/COMPILERS.md
    4 | // solhint-disable-next-line lido/fixed-compiler-version
    5 | pragma solidity >=0.4.24;
    6 | 
    7 | interface IOssifiableProxy {
```

_file_excerpt · [contracts/common/interfaces/IVersioned.sol](https://github.com/lidofinance/core/blob/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3/contracts/common/interfaces/IVersioned.sol#L6) · line 6 · SHA-256 0660dff824d611316b9ecb6d8c871f27b94ff111970e9825082004b69c743649_

```
    4 | // See contracts/COMPILERS.md
    5 | // solhint-disable-next-line
    6 | pragma solidity >=0.4.24;
    7 | 
    8 | interface IVersioned {
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Зафиксируйте версию компилятора, использованную при тестировании.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-06295 — Плавающая версия компилятора (>=0.8.9 <0.9.0) в 4 файл(ах)

- Серьёзность: **Низкая** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `solidity:pragma:>=0.8.9 <0.9.0`
- Источник данных: contracts/common/interfaces/IStakingModuleV2.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-29 05:26 UTC
- Балл приоритета: 38.4 / 100
- CVSS v3.1: неприменимо

pragma >=0.8.9 <0.9.0 в 4 файл(ах), впервые в contracts/common/interfaces/IStakingModuleV2.sol:5. (см. SWC-103)

**Возможные последствия.** Контракты могут быть развёрнуты непроверенной версией компилятора. Фактический компилятор задаёт конфигурация сборки, которую эта проверка не читает.

**Шаги воспроизведения.**

```
Откройте contracts/common/interfaces/IStakingModuleV2.sol:5 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [contracts/common/interfaces/IStakingModuleV2.sol](https://github.com/lidofinance/core/blob/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3/contracts/common/interfaces/IStakingModuleV2.sol#L5) · line 5 · SHA-256 82fa4964aa927215b3d4c21add37350e352a666bc20b5b72b8f8a8a7cbc1ce3c_

```
    3 | 
    4 | // solhint-disable-next-line lido/fixed-compiler-version
    5 | pragma solidity >=0.8.9 <0.9.0;
    6 | 
    7 | interface IStakingModuleV2 {
```

_file_excerpt · [contracts/common/lib/Bytes32String.sol](https://github.com/lidofinance/core/blob/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3/contracts/common/lib/Bytes32String.sol#L3) · line 3 · SHA-256 3ebb0b3e60226fbdfab751ceab640b81ab31c979875f401d0892d3851e07b986_

```
    1 | // SPDX-License-Identifier: GPL-3.0
    2 | // solhint-disable-next-line lido/fixed-compiler-version
    3 | pragma solidity >=0.8.9 <0.9.0;
    4 | 
    5 | /**
```

_file_excerpt · [contracts/common/lib/TriggerableWithdrawals.sol](https://github.com/lidofinance/core/blob/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3/contracts/common/lib/TriggerableWithdrawals.sol#L6) · line 6 · SHA-256 a59e67acffaf9a1c05c982609d0750e97aaae2dc5dff6a895d411b1a7d40c6d0_

```
    4 | /* See contracts/COMPILERS.md */
    5 | // solhint-disable-next-line lido/fixed-compiler-version
    6 | pragma solidity >=0.8.9 <0.9.0;
    7 | 
    8 | /**
```

_file_excerpt · [contracts/common/lib/WithdrawalCredentials.sol](https://github.com/lidofinance/core/blob/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3/contracts/common/lib/WithdrawalCredentials.sol#L3) · line 3 · SHA-256 3ebb0b3e60226fbdfab751ceab640b81ab31c979875f401d0892d3851e07b986_

```
    1 | // SPDX-License-Identifier: GPL-3.0
    2 | // solhint-disable-next-line lido/fixed-compiler-version
    3 | pragma solidity >=0.8.9 <0.9.0;
    4 | 
    5 | /**
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Зафиксируйте версию компилятора, использованную при тестировании.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-06296 — Плавающая версия компилятора (>=0.8.9) в 2 файл(ах)

- Серьёзность: **Низкая** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `solidity:pragma:>=0.8.9`
- Источник данных: contracts/common/interfaces/TopUpWitness.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-29 05:26 UTC
- Балл приоритета: 38.4 / 100
- CVSS v3.1: неприменимо

pragma >=0.8.9 в 2 файл(ах), впервые в contracts/common/interfaces/TopUpWitness.sol:5. (см. SWC-103)

**Возможные последствия.** Контракты могут быть развёрнуты непроверенной версией компилятора. Фактический компилятор задаёт конфигурация сборки, которую эта проверка не читает.

**Шаги воспроизведения.**

```
Откройте contracts/common/interfaces/TopUpWitness.sol:5 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [contracts/common/interfaces/TopUpWitness.sol](https://github.com/lidofinance/core/blob/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3/contracts/common/interfaces/TopUpWitness.sol#L5) · line 5 · SHA-256 1432a42e978675992f39892dcaaac81066f0152f0bfa7aa953c93b300e4fa298_

```
    3 | 
    4 | // solhint-disable-next-line
    5 | pragma solidity >=0.8.9;
    6 | 
    7 | import {BeaconRootData, ValidatorWitness} from "contracts/common/interfaces/ValidatorWitness.sol";
```

_file_excerpt · [contracts/common/interfaces/ValidatorWitness.sol](https://github.com/lidofinance/core/blob/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3/contracts/common/interfaces/ValidatorWitness.sol#L5) · line 5 · SHA-256 5c9ce9896e50e31e0c8e359927db66c2d0ee7f98e621cdb554d11e466d7a7ce6_

```
    3 | 
    4 | // solhint-disable-next-line
    5 | pragma solidity >=0.8.9;
    6 | 
    7 | struct BeaconRootData {
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Зафиксируйте версию компилятора, использованную при тестировании.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-06297 — Плавающая версия компилятора (^0.8.25) в 9 файл(ах)

- Серьёзность: **Низкая** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `solidity:pragma:^0.8.25`
- Источник данных: contracts/common/lib/BLS.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-29 05:26 UTC
- Балл приоритета: 38.4 / 100
- CVSS v3.1: неприменимо

pragma ^0.8.25 в 9 файл(ах), впервые в contracts/common/lib/BLS.sol:5. (см. SWC-103)

**Возможные последствия.** Контракты могут быть развёрнуты непроверенной версией компилятора. Фактический компилятор задаёт конфигурация сборки, которую эта проверка не читает.

**Шаги воспроизведения.**

```
Откройте contracts/common/lib/BLS.sol:5 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [contracts/common/lib/BLS.sol](https://github.com/lidofinance/core/blob/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3/contracts/common/lib/BLS.sol#L5) · line 5 · SHA-256 35bab40d6ec5974db96ff716e2771f1bba2ed5c379d7a67fd30950540ec0f053_

```
    3 | // See contracts/COMPILERS.md
    4 | // solhint-disable-next-line lido/fixed-compiler-version
    5 | pragma solidity ^0.8.25;
    6 | 
    7 | import {SSZ} from "./SSZ.sol";
```

_file_excerpt · [contracts/common/lib/BeaconTypes.sol](https://github.com/lidofinance/core/blob/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3/contracts/common/lib/BeaconTypes.sol#L6) · line 6 · SHA-256 0fac5ed3b93bfbcb621b47c1c577e9cfdfe6f6ea6403449552040db7c3538565_

```
    4 | // See contracts/COMPILERS.md
    5 | // solhint-disable-next-line lido/fixed-compiler-version
    6 | pragma solidity ^0.8.25;
    7 | 
    8 | struct Validator {
```

_file_excerpt · [contracts/common/lib/GIndex.sol](https://github.com/lidofinance/core/blob/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3/contracts/common/lib/GIndex.sol#L11) · line 11 · SHA-256 ce38a11d793ecddd6a1911180050d9d9f1b19d11aa0eae10e55e194ba399a99d_

```
    9 | // See contracts/COMPILERS.md
   10 | // solhint-disable-next-line lido/fixed-compiler-version
   11 | pragma solidity ^0.8.25;
   12 | 
   13 | type GIndex is bytes32;
```

_file_excerpt · [contracts/common/lib/SSZ.sol](https://github.com/lidofinance/core/blob/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3/contracts/common/lib/SSZ.sol#L11) · line 11 · SHA-256 dad15ec1b5bac83ac71ebad55ccdc4ee6c3cad9c8899f3286f517ea849ad3675_

```
    9 | // See contracts/COMPILERS.md
   10 | // solhint-disable-next-line lido/fixed-compiler-version
   11 | pragma solidity ^0.8.25;
   12 | 
   13 | import {BeaconBlockHeader, Validator} from "./BeaconTypes.sol";
```

_file_excerpt · [contracts/upgrade/interfaces/IDualGovernance.sol](https://github.com/lidofinance/core/blob/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3/contracts/upgrade/interfaces/IDualGovernance.sol#L6) · line 6 · SHA-256 59cde1081a21fd205bfe1dc58050c3547e77a921718c580940389f51b1975a40_

```
    4 | // See contracts/COMPILERS.md
    5 | // solhint-disable-next-line lido/fixed-compiler-version
    6 | pragma solidity ^0.8.25;
    7 | 
    8 | /// @notice Represents an external call to a specific address with an optional ETH transfer.
```

_file_excerpt · [contracts/upgrade/interfaces/ITimelock.sol](https://github.com/lidofinance/core/blob/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3/contracts/upgrade/interfaces/ITimelock.sol#L6) · line 6 · SHA-256 5266a254447d2501e469fbd615c718d3c7f12b9e04e7aacf94455cf3200d6ca4_

```
    4 | // See contracts/COMPILERS.md
    5 | // solhint-disable-next-line lido/fixed-compiler-version
    6 | pragma solidity ^0.8.25;
    7 | 
    8 | type Duration is uint32;
```

_file_excerpt · [contracts/upgrade/interfaces/IUpgradeConfig.sol](https://github.com/lidofinance/core/blob/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3/contracts/upgrade/interfaces/IUpgradeConfig.sol#L6) · line 6 · SHA-256 f7bbf70cda6fc44716d84bcdc88d421a81ab1631b94659770058911aaf6d29bd_

```
    4 | // See contracts/COMPILERS.md
    5 | // solhint-disable-next-line lido/fixed-compiler-version
    6 | pragma solidity ^0.8.25;
    7 | 
    8 | import {GlobalConfig, CoreUpgradeConfig, CuratedModuleConfig, CSMUpgradeConfig} from "../UpgradeTypes.sol";
```

_file_excerpt · [contracts/upgrade/interfaces/IUpgradeTemplate.sol](https://github.com/lidofinance/core/blob/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3/contracts/upgrade/interfaces/IUpgradeTemplate.sol#L6) · line 6 · SHA-256 8b3d463fedcae84e75cb79a60299492b96097e195b6c77793a74c26932452c37_

```
    4 | // See contracts/COMPILERS.md
    5 | // solhint-disable-next-line lido/fixed-compiler-version
    6 | pragma solidity ^0.8.25;
    7 | 
    8 | interface IUpgradeTemplate {
```

_file_excerpt · [contracts/upgrade/utils/OmnibusBase.sol](https://github.com/lidofinance/core/blob/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3/contracts/upgrade/utils/OmnibusBase.sol#L5) · line 5 · SHA-256 fed483bbd5cec12170e82026181f2df207134c8275daf8a0b4e9640a584aad0d_

```
    3 | // See contracts/COMPILERS.md
    4 | // solhint-disable-next-line lido/fixed-compiler-version
    5 | pragma solidity ^0.8.25;
    6 | 
    7 | import {IForwarder} from "../interfaces/IForwarder.sol";
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Зафиксируйте версию компилятора, использованную при тестировании.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-06301 — Плавающая версия компилятора (^0.8.9) в 2 файл(ах)

- Серьёзность: **Низкая** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `solidity:pragma:^0.8.9`
- Источник данных: contracts/common/lib/UnstructuredStorage.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-29 05:26 UTC
- Балл приоритета: 38.4 / 100
- CVSS v3.1: неприменимо

pragma ^0.8.9 в 2 файл(ах), впервые в contracts/common/lib/UnstructuredStorage.sol:5. (см. SWC-103)

**Возможные последствия.** Контракты могут быть развёрнуты непроверенной версией компилятора. Фактический компилятор задаёт конфигурация сборки, которую эта проверка не читает.

**Шаги воспроизведения.**

```
Откройте contracts/common/lib/UnstructuredStorage.sol:5 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [contracts/common/lib/UnstructuredStorage.sol](https://github.com/lidofinance/core/blob/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3/contracts/common/lib/UnstructuredStorage.sol#L5) · line 5 · SHA-256 4ffc7bb8e91f891665d3ee3d74452c57a1c08ea51a86c347cf03b431c9abfa46_

```
    3 | 
    4 | // solhint-disable-next-line lido/fixed-compiler-version
    5 | pragma solidity ^0.8.9;
    6 | 
    7 | library UnstructuredStorage {
```

_file_excerpt · [contracts/common/utils/PausableUntil.sol](https://github.com/lidofinance/core/blob/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3/contracts/common/utils/PausableUntil.sol#L4) · line 4 · SHA-256 9e8734160ad7f76e92b283253f551142792108b4e60f68302abdc72e6a1cfcf2_

```
    2 | // SPDX-License-Identifier: GPL-3.0
    3 | // solhint-disable-next-line lido/fixed-compiler-version
    4 | pragma solidity ^0.8.9;
    5 | 
    6 | import {UnstructuredStorage} from "contracts/common/lib/UnstructuredStorage.sol";
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Зафиксируйте версию компилятора, использованную при тестировании.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-06302 — Плавающая версия компилятора (^0.8.20) в 6 файл(ах)

- Серьёзность: **Низкая** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `solidity:pragma:^0.8.20`
- Источник данных: contracts/openzeppelin/5.2/upgradeable/access/AccessControlUpgradeable.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-29 05:26 UTC
- Балл приоритета: 38.4 / 100
- CVSS v3.1: неприменимо

pragma ^0.8.20 в 6 файл(ах), впервые в contracts/openzeppelin/5.2/upgradeable/access/AccessControlUpgradeable.sol:4. (см. SWC-103)

**Возможные последствия.** Контракты могут быть развёрнуты непроверенной версией компилятора. Фактический компилятор задаёт конфигурация сборки, которую эта проверка не читает.

**Шаги воспроизведения.**

```
Откройте contracts/openzeppelin/5.2/upgradeable/access/AccessControlUpgradeable.sol:4 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [contracts/openzeppelin/5.2/upgradeable/access/AccessControlUpgradeable.sol](https://github.com/lidofinance/core/blob/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3/contracts/openzeppelin/5.2/upgradeable/access/AccessControlUpgradeable.sol#L4) · line 4 · SHA-256 c91c7637d5b12637701a0ae1cfe3520baeb4ff5be7deffb00fab10c387d34135_

```
    2 | // OpenZeppelin Contracts (last updated v5.0.0) (access/AccessControl.sol)
    3 | 
    4 | pragma solidity ^0.8.20;
    5 | 
    6 | import {IAccessControl} from "@openzeppelin/contracts-v5.2/access/IAccessControl.sol";
```

_file_excerpt · [contracts/openzeppelin/5.2/upgradeable/access/Ownable2StepUpgradeable.sol](https://github.com/lidofinance/core/blob/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3/contracts/openzeppelin/5.2/upgradeable/access/Ownable2StepUpgradeable.sol#L4) · line 4 · SHA-256 9039fba09f8df5cefb332d1e317b3aad6b2ba7b8ced29a77b66686e10d70cb92_

```
    2 | // OpenZeppelin Contracts (last updated v5.1.0) (access/Ownable2Step.sol)
    3 | 
    4 | pragma solidity ^0.8.20;
    5 | 
    6 | import {OwnableUpgradeable} from "./OwnableUpgradeable.sol";
```

_file_excerpt · [contracts/openzeppelin/5.2/upgradeable/access/OwnableUpgradeable.sol](https://github.com/lidofinance/core/blob/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3/contracts/openzeppelin/5.2/upgradeable/access/OwnableUpgradeable.sol#L4) · line 4 · SHA-256 010e5f1ec1c98ca5555f498ffaac5efbb31f3dc629e3d2423eb6352420c6fd11_

```
    2 | // OpenZeppelin Contracts (last updated v5.0.0) (access/Ownable.sol)
    3 | 
    4 | pragma solidity ^0.8.20;
    5 | 
    6 | import {ContextUpgradeable} from "../utils/ContextUpgradeable.sol";
```

_file_excerpt · [contracts/openzeppelin/5.2/upgradeable/access/extensions/AccessControlEnumerableUpgradeable.sol](https://github.com/lidofinance/core/blob/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3/contracts/openzeppelin/5.2/upgradeable/access/extensions/AccessControlEnumerableUpgradeable.sol#L4) · line 4 · SHA-256 5759405eb212aba45f5f43e3031619415c18606ec276f213984da352fe8cf5cd_

```
    2 | // OpenZeppelin Contracts (last updated v5.1.0) (access/extensions/AccessControlEnumerable.sol)
    3 | 
    4 | pragma solidity ^0.8.20;
    5 | 
    6 | import {IAccessControlEnumerable} from "@openzeppelin/contracts-v5.2/access/extensions/IAccessControlEnumerable.sol";
```

_file_excerpt · [contracts/openzeppelin/5.2/upgradeable/utils/ContextUpgradeable.sol](https://github.com/lidofinance/core/blob/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3/contracts/openzeppelin/5.2/upgradeable/utils/ContextUpgradeable.sol#L4) · line 4 · SHA-256 6db5b22f01feb64db43eb6bad64f302d28db2b05927eaef06e52f2e8f50b8b04_

```
    2 | // OpenZeppelin Contracts (last updated v5.0.1) (utils/Context.sol)
    3 | 
    4 | pragma solidity ^0.8.20;
    5 | import {Initializable} from "../proxy/utils/Initializable.sol";
    6 | 
```

_file_excerpt · [contracts/openzeppelin/5.2/upgradeable/utils/introspection/ERC165Upgradeable.sol](https://github.com/lidofinance/core/blob/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3/contracts/openzeppelin/5.2/upgradeable/utils/introspection/ERC165Upgradeable.sol#L4) · line 4 · SHA-256 87a3921b0c1cbe1cfa71feb0bd0343897bf5e8ec0a76d7a1bd1e7867e91b1454_

```
    2 | // OpenZeppelin Contracts (last updated v5.1.0) (utils/introspection/ERC165.sol)
    3 | 
    4 | pragma solidity ^0.8.20;
    5 | 
    6 | import {IERC165} from "@openzeppelin/contracts-v5.2/utils/introspection/IERC165.sol";
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Зафиксируйте версию компилятора, использованную при тестировании.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-06327 — brace-expansion 2.0.1 затронут GHSA-v6h2-p8h4-qcjw (CVE-2025-5889)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/brace-expansion@2.0.1`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 05:26 UTC
- Балл приоритета: 31.0 / 100
- CVSS v3.1: 3.1 (`CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:N/I:N/A:L`)

OSV.dev сообщает GHSA-v6h2-p8h4-qcjw (CVE-2025-5889) для пакета npm brace-expansion версии 2.0.1: brace-expansion Regular Expression Denial of Service vulnerability. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-v6h2-p8h4-qcjw
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-v6h2-p8h4-qcjw](https://osv.dev/vulnerability/GHSA-v6h2-p8h4-qcjw) · line 4053 · SHA-256 42c39c639c9e9e145377b48bdc291881110c55d6a328c02fc67ae8798aaf1553_

```
{"id": "GHSA-v6h2-p8h4-qcjw", "aliases": ["CVE-2025-5889"], "modified": "2026-09-10T03:50:25.501161917Z", "summary": "brace-expansion Regular Expression Denial of Service vulnerability", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:N/I:N/A:L"}, {"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:H/AT:N/PR:L/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.1.12, 2.0.2, 3.0.1, 4.0.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06284 — Привилегированные административные функции в contracts/0.4.24/template/LidoTemplate.sol: setOwner, deployLidoAPM, cancelAndTransferDomain, createStdAragonRepos, createRepos, newDAO, issueTokens, finalizeDAO

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:contracts/0.4.24/template/LidoTemplate.sol`
- Источник данных: contracts/0.4.24/template/LidoTemplate.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-29 05:26 UTC
- Балл приоритета: 38.5 / 100
- CVSS v3.1: неприменимо

Функции, защищённые модификаторами владельца/ролей: setOwner, deployLidoAPM, cancelAndTransferDomain, createStdAragonRepos, createRepos, newDAO, issueTokens, finalizeDAO. (см. —)

**Возможные последствия.** Риск централизации: компрометация ключа администратора компрометирует протокол.

**Шаги воспроизведения.**

```
Откройте contract в предоставленном файле contracts/0.4.24/template/LidoTemplate.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [contracts/0.4.24/template/LidoTemplate.sol](https://github.com/lidofinance/core/blob/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3/contracts/0.4.24/template/LidoTemplate.sol) · multiple · SHA-256 736dfd3723fafc3fb804b10442f6ac83a92856381c910c5d630f0cc2f78750c7_

```
Privileged functions: setOwner, deployLidoAPM, cancelAndTransferDomain, createStdAragonRepos, createRepos, newDAO, issueTokens, finalizeDAO
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте мультиподпись/таймлок для ролей администратора и документируйте их.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-06291 — Привилегированные административные функции в contracts/0.8.9/proxy/OssifiableProxy.sol: proxy__ossify, proxy__changeAdmin, proxy__upgradeTo, proxy__upgradeToAndCall

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:contracts/0.8.9/proxy/OssifiableProxy.sol`
- Источник данных: contracts/0.8.9/proxy/OssifiableProxy.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-29 05:26 UTC
- Балл приоритета: 38.5 / 100
- CVSS v3.1: неприменимо

Функции, защищённые модификаторами владельца/ролей: proxy__ossify, proxy__changeAdmin, proxy__upgradeTo, proxy__upgradeToAndCall. (см. —)

**Возможные последствия.** Риск централизации: компрометация ключа администратора компрометирует протокол.

**Шаги воспроизведения.**

```
Откройте contract в предоставленном файле contracts/0.8.9/proxy/OssifiableProxy.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [contracts/0.8.9/proxy/OssifiableProxy.sol](https://github.com/lidofinance/core/blob/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3/contracts/0.8.9/proxy/OssifiableProxy.sol) · multiple · SHA-256 23b3c3709c3f27454f728b31a23f89ea3e5df629ba7a4d071bea128a839cb7c3_

```
Privileged functions: proxy__ossify, proxy__changeAdmin, proxy__upgradeTo, proxy__upgradeToAndCall
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте мультиподпись/таймлок для ролей администратора и документируйте их.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-06303 — Привилегированные административные функции в contracts/openzeppelin/5.2/upgradeable/access/Ownable2StepUpgradeable.sol: transferOwnership

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:contracts/openzeppelin/5.2/upgradeable/access/Ownable2StepUpgradeable.sol`
- Источник данных: contracts/openzeppelin/5.2/upgradeable/access/Ownable2StepUpgradeable.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-29 05:26 UTC
- Балл приоритета: 38.5 / 100
- CVSS v3.1: неприменимо

Функции, защищённые модификаторами владельца/ролей: transferOwnership. (см. —)

**Возможные последствия.** Риск централизации: компрометация ключа администратора компрометирует протокол.

**Шаги воспроизведения.**

```
Откройте contract в предоставленном файле contracts/openzeppelin/5.2/upgradeable/access/Ownable2StepUpgradeable.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [contracts/openzeppelin/5.2/upgradeable/access/Ownable2StepUpgradeable.sol](https://github.com/lidofinance/core/blob/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3/contracts/openzeppelin/5.2/upgradeable/access/Ownable2StepUpgradeable.sol) · multiple · SHA-256 3ef6a6924988649e26a7e42a450b6976f80844a318d3ab2418fc99e4bae2bcee_

```
Privileged functions: transferOwnership
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте мультиподпись/таймлок для ролей администратора и документируйте их.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-06304 — Привилегированные административные функции в contracts/openzeppelin/5.2/upgradeable/access/OwnableUpgradeable.sol: renounceOwnership, transferOwnership

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:contracts/openzeppelin/5.2/upgradeable/access/OwnableUpgradeable.sol`
- Источник данных: contracts/openzeppelin/5.2/upgradeable/access/OwnableUpgradeable.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-29 05:26 UTC
- Балл приоритета: 38.5 / 100
- CVSS v3.1: неприменимо

Функции, защищённые модификаторами владельца/ролей: renounceOwnership, transferOwnership. (см. —)

**Возможные последствия.** Риск централизации: компрометация ключа администратора компрометирует протокол.

**Шаги воспроизведения.**

```
Откройте contract в предоставленном файле contracts/openzeppelin/5.2/upgradeable/access/OwnableUpgradeable.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [contracts/openzeppelin/5.2/upgradeable/access/OwnableUpgradeable.sol](https://github.com/lidofinance/core/blob/2bd532298d85cdf520169fdc0c5fb0cc9baf03c3/contracts/openzeppelin/5.2/upgradeable/access/OwnableUpgradeable.sol) · multiple · SHA-256 c9178db25d8ef1b1a83ff9fe952090d86c1ef54a1f84a5a67cc0aac7fdd62bd6_

```
Privileged functions: renounceOwnership, transferOwnership
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте мультиподпись/таймлок для ролей администратора и документируйте их.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-06354 — 13 бюллетеней в 4 пакет(ах) PyPI, нужных только для разработки или сборки

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependencies:PyPI:non-runtime`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch по точным версиям; область применения — из devDependencies, флагов dev в package-lock.json, разделов importers в pnpm, графа Cargo.lock от таблиц Cargo.toml и — для yarn.lock, который область не записывает вовсе — графа файла блокировки, пройденного от package.json. Если рабочее требование в файле блокировки разрешить не удалось, файл остаётся без классификации, чтобы пакет не был отложен в сторону по ошибке.
- Анализатор: dependencies 1.2.0 · 2026-10-29 05:26 UTC
- Балл приоритета: 17.1 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает 13 бюллетеней (7 с оценкой high или critical) для 4 пакет(ов) PyPI, которые подтягивают только инструменты разработки или сборки (poetry.lock): например, aiohttp@3.14.3 [dev]: GHSA-2g87-pp6c-29x5, GHSA-494j-54xm-rwp3, GHSA-5wr8-gcqf-gqf3, GHSA-6cjc-53gc-5rqm, GHSA-9xw5-w5jj-pvcg, GHSA-f9xw-jh8m-3mwq, GHSA-gx76-c99x-2c96, GHSA-pqxq-w44r-73xw; certifi@2024.8.30 [dev]: GHSA-6q48-6c7w-9gw2; urllib3@2.7.0 [dev]: GHSA-8988-9cw3-xx77, GHSA-gh4c-6fx4-qh6g, GHSA-vxq7-64xx-v4gw; web3@6.20.3 [dev]: GHSA-5hr4-253g-cpx2. Манифесты помечают их так (devDependencies, "dev": true в package-lock.json, [dev-dependencies]/[build-dependencies] через граф Cargo.lock), поэтому в поставляемый продукт они не входят.

**Возможные последствия.** Пользователей продукта они не затрагивают. Они могут влиять на машины разработчиков и CI (цепочка поставки): скомпрометированный или уязвимый инструмент способен изменить сборку.

**Шаги воспроизведения.**

```
Найдите пакеты из доказательства на https://osv.dev и проверьте их область применения в poetry.lock.
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev (PyPI)](https://osv.dev/) · poetry.lock · SHA-256 1e6cb78244d9c788246d0d92f307231ed76b7e434e54196f9f27070bebe40240_

```
aiohttp@3.14.3 [dev]: GHSA-2g87-pp6c-29x5, GHSA-494j-54xm-rwp3, GHSA-5wr8-gcqf-gqf3, GHSA-6cjc-53gc-5rqm, GHSA-9xw5-w5jj-pvcg, GHSA-f9xw-jh8m-3mwq, GHSA-gx76-c99x-2c96, GHSA-pqxq-w44r-73xw
certifi@2024.8.30 [dev]: GHSA-6q48-6c7w-9gw2
urllib3@2.7.0 [dev]: GHSA-8988-9cw3-xx77, GHSA-gh4c-6fx4-qh6g, GHSA-vxq7-64xx-v4gw
web3@6.20.3 [dev]: GHSA-5hr4-253g-cpx2
```

**Ограничения проверки.** Данные получены от OSV.dev в зафиксированное время. Области применения взяты из манифестов; собственные build-зависимости крейтов реестра в Cargo.lock не различимы, поэтому множество runtime может оказаться больше реального, но не меньше.

**Рекомендация.** Обновите инструменты в рамках планового обслуживания; в первую очередь пакеты, которые выполняются в CI с секретами или создают релизные артефакты.

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06355 — 60 бюллетеней в 19 пакет(ах) npm, нужных только для разработки или сборки

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependencies:npm:non-runtime`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch по точным версиям; область применения — из devDependencies, флагов dev в package-lock.json, разделов importers в pnpm, графа Cargo.lock от таблиц Cargo.toml и — для yarn.lock, который область не записывает вовсе — графа файла блокировки, пройденного от package.json. Если рабочее требование в файле блокировки разрешить не удалось, файл остаётся без классификации, чтобы пакет не был отложен в сторону по ошибке.
- Анализатор: dependencies 1.2.0 · 2026-10-29 05:26 UTC
- Балл приоритета: 17.1 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает 60 бюллетеней (30 с оценкой high или critical) для 19 пакет(ов) npm, которые подтягивают только инструменты разработки или сборки (yarn.lock): например, @eslint/plugin-kit@0.3.1 [dev]: GHSA-xffm-g5w8-qvg7; @fastify/busboy@2.1.1 [dev]: GHSA-gxm5-99cw-xjw9, GHSA-x8mw-p69m-v3mx; @humanfs/node@0.16.6 [dev]: GHSA-p498-v437-472g; @isaacs/brace-expansion@5.0.0 [dev]: GHSA-7h2j-956f-4vf2; adm-zip@0.4.16 [dev]: GHSA-7q85-xj36-vmfc, GHSA-8238-w5pm-2374, GHSA-c6fg-446q-cg94, GHSA-j5f4-cc29-5x44, GHSA-p634-w6r4-rjp2, GHSA-rcw4-f5rp-g42v, GHSA-xcpc-8h2w-3j85. Манифесты помечают их так (devDependencies, "dev": true в package-lock.json, [dev-dependencies]/[build-dependencies] через граф Cargo.lock), поэтому в поставляемый продукт они не входят.

**Возможные последствия.** Пользователей продукта они не затрагивают. Они могут влиять на машины разработчиков и CI (цепочка поставки): скомпрометированный или уязвимый инструмент способен изменить сборку.

**Шаги воспроизведения.**

```
Найдите пакеты из доказательства на https://osv.dev и проверьте их область применения в yarn.lock.
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev (npm)](https://osv.dev/) · yarn.lock · SHA-256 942cac280c5d4ce8c339d7bf24bf290ad9752d0a0c30f3589569e182a35ccccd_

```
@eslint/plugin-kit@0.3.1 [dev]: GHSA-xffm-g5w8-qvg7
@fastify/busboy@2.1.1 [dev]: GHSA-gxm5-99cw-xjw9, GHSA-x8mw-p69m-v3mx
@humanfs/node@0.16.6 [dev]: GHSA-p498-v437-472g
@isaacs/brace-expansion@5.0.0 [dev]: GHSA-7h2j-956f-4vf2
adm-zip@0.4.16 [dev]: GHSA-7q85-xj36-vmfc, GHSA-8238-w5pm-2374, GHSA-c6fg-446q-cg94, GHSA-j5f4-cc29-5x44, GHSA-p634-w6r4-rjp2, GHSA-rcw4-f5rp-g42v, GHSA-xcpc-8h2w-3j85
ajv@8.17.1 [dev]: GHSA-2g4f-4pwh-qvx6
axios@1.17.0 [dev]: GHSA-3pq3-5fj3-cg6v, GHSA-42h9-826w-cgv3, GHSA-44g4-m2mj-wpvx, GHSA-4hqw-qxg8-jxx2, GHSA-542g-h47m-68v8, GHSA-7q8q-rj6j-mhjq, GHSA-9fr6-4gfg-395g, GHSA-c29m-xwm3-cm6r, GHSA-f4gw-2p7v-4548, GHSA-gcfj-64vw-6mp9, GHSA-hcpx-6fm6-wx23, GHSA-j8rh-479h-cp32, GHSA-jqh4-m9w3-8hp9, GHSA-m8m8-qj5v-23w3, GHSA-mghh-pgcx-3jjj, GHSA-mmx7-hfxf-jppx, GHSA-mwf2-3pr3-8698, GHSA-pmv8-rq9r-6j72, GHSA-r4gj-5m52-g5wh, GHSA-vh66-26gq-q6x8
bn.js@4.11.6 [dev]: GHSA-378v-28hj-76wf
cookie@0.4.2 [dev]: GHSA-pxg6-pf52-xh8x
diff@4.0.2 [dev]: GHSA-73rr-hh4g-fpgx
diff@5.2.0 [dev]: GHSA-73rr-hh4g-fpgx
fast-uri@3.1.8 [dev]: GHSA-333x-w4r6-6crp, GHSA-w74x-v6f9-j3xg, GHSA-wjr9-j795-jxcr, GHSA-xhq7-xmqj-769h
follow-redirects@1.16.0 [dev]: GHSA-8r9p-f939-6h3c, GHSA-q3jh-wrc6-jgq8
form-data@4.0.5 [dev]: GHSA-hmw2-7cc7-3qxx
handlebars@4.7.9 [dev]: GHSA-8r5x-fm3f-whwj, GHSA-p8wg-vrv2-v86f, GHSA-xw65-4hp5-5hc7
immutable@4.3.8 [dev]: GHSA-v56q-mh7h-f735, GHSA-xvcm-6775-5m9r
js-yaml@4.1.0 [dev]: GHSA-2883-xcg3-v3hh, GHSA-52cp-r559-cp3m, GHSA-5p4m-2wfm-xmqj, GHSA-h67p-54hq-rp68, GHSA-mh29-5h37-fv8m
minimatch@10.1.1 [dev]: GHSA-23c5-xmqv-rm74, GHSA-3ppc-4f35-3m26, GHSA-7r86-cg39-jmmj
minimatch@5.1.6 [dev]: GHSA-23c5-xmqv-rm74, GHSA-3ppc-4f35-3m26, GHSA-7r86-cg39-jmmj
```

**Ограничения проверки.** Данные получены от OSV.dev в зафиксированное время. Области применения взяты из манифестов; собственные build-зависимости крейтов реестра в Cargo.lock не различимы, поэтому множество runtime может оказаться больше реального, но не меньше.

**Рекомендация.** Обновите инструменты в рамках планового обслуживания; в первую очередь пакеты, которые выполняются в CI с секретами или создают релизные артефакты.

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06307 — Не обнаружено криптобиблиотек с поддержкой PQC

- Серьёзность: **Информационная** · Классификация: Недостаточность данных · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependencies`
- Источник данных: dependency manifests
- Метод обнаружения: Сопоставление названий зависимостей.
- Анализатор: dependencies 1.2.0 · 2026-10-29 05:26 UTC
- Балл приоритета: 14.5 / 100
- CVSS v3.1: неприменимо

В 4 манифестах зависимостей QSI нашёл криптобиблиотеки (@noble/curves, @noble/hashes, @noble/secp256k1, crypto-js, elliptic, ethers, pycryptodome, secp256k1, tweetnacl, web3), но ни одной из списка поддерживающих PQC.

**Возможные последствия.** Только индикатор готовности: поддержка PQC может обеспечиваться платформой (OpenSSL, ОС, облачный KMS), а не зависимостями приложения.

**Шаги воспроизведения.**

```
Изучите перечисленные в доказательстве манифесты.
```

**Подтверждающие доказательства.**

_dependency · package.json, poetry.lock, pyproject.toml, yarn.lock · SHA-256 7bee3fe7eaee47f3666a17867737321314890e06b76c64557ac6283c87d176ca_

```
Crypto libraries: @noble/curves, @noble/hashes, @noble/secp256k1, crypto-js, elliptic, ethers, pycryptodome, secp256k1, tweetnacl, web3
```

**Ограничения проверки.** Отсутствие доказательств не является доказательством отсутствия: системные библиотеки и транзитивные зависимости могут не указываться.

**Рекомендация.** Определите источник поддержки PQC (TLS-терминатор, KMS/HSM, обновление библиотек).

**Повторная проверка.** Повторите сканирование после обновлений.


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
_Допущения планирования: x для обмена ключами, x для подписей, y — значения по умолчанию профиля риска «Финансовая организация», а не данные клиента; с фактическими сроками клиента вывод может измениться._

### Постквантовая зрелость: Уровень 0 из 4 — постквантовой криптографии нет


**Следующий шаг:** Проведите инвентаризацию: где классическая криптография с открытым ключом защищает долгоживущие данные и ключи, и выберите первую миграцию — обычно гибридный обмен ключами TLS и обёрнутые ключи.

_Уровни: 0 — нет; 1 — есть, но не подключено; 2 — используется вне критичных путей; 3 — гибрид в критичном пути; 4 — постквантовое по умолчанию в критичных путях (корень доверия, обёртка ключей, обмен ключами в канале). Оценка по коду и манифестам._

### Что делают квантово-уязвимые алгоритмы

| Роль | Алгоритмы (файлы) | ID | Первый шаг |
|---|---|---|---|
| **подпись транзакций и сообщений** | ECDSA (2) | QSI-2026-06299 | Следите за постквантовыми планами каждой сети, не используйте открытые ключи повторно и держите подписание готовым к постквантовым схемам по мере их принятия сетями |
| **роль не определена** | BLS12-381 (2), ECDSA (1) | QSI-2026-06305, QSI-2026-06306 | Классифицируйте каждое использование, зафиксируйте сроки жизни данных и запланируйте миграцию на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема; введите уровень абстракции для криптогибкости |

_Роль определяется по путям файлов, именам функций и коду вокруг совпадений; проверка её подтверждает. Сначала — ключи корня доверия и обёрнутые ключи: их трудно заменить или можно записать уже сегодня._
Анкета готовности для проекта не заполнялась.

### Квантовые алгоритмы, значимые для этой инвентаризации

| Квантовый алгоритм | Действие | Модель атаки | Алгоритмы из инвентаризации (строк) | Что это значит для аудита |
|---|---|---|---|---|
| Алгоритм Шора — дискретный логарифм в конечных полях | взламывает | Q1 | BLS12-381 (4) | Взламывает Диффи–Хеллмана в конечных полях и DSA при любом размере. Переводите установление ключей на ML-KEM (на переходный период — гибрид с X25519 или ECDH), подписи — на ML-DSA или SLH-DSA. |
| Алгоритм Шора — дискретный логарифм на эллиптических кривых | взламывает | Q1 | BLS12-381 (4), ECDSA (3) | Ключи на эллиптических кривых, по оценкам, падут раньше ключей RSA сопоставимой классической стойкости. В блокчейнах первыми под угрозой монеты, чей открытый ключ уже опубликован (повторно используемые адреса, выходы pay-to-public-key и Taproot); планируйте переход на постквантовые подписи и до этого избегайте повторного использования ключей. |
| Алгоритм Гровера — поиск ключа и прообразов | ослабляет (более длинные ключи восстанавливают запас) | Q1 | Keccak-256 (35) | Не взлом. Ключи 256 бит (AES-256, ChaCha20) сохраняют хороший запас; AES-128 соответствует категории 1 NIST, но некоторые регуляторы требуют 256-битных ключей в квантово-устойчивых системах (см. запись AES-128). Для долгоживущих данных предпочитайте 256-битные ключи; 256-битные хеши для стойкости к прообразам менять не нужно. |
| Брассар–Хойер–Тапп — поиск коллизий | ослабляет (более длинные ключи восстанавливают запас) | Q1 | Keccak-256 (35) | 256-битные хеши (SHA-256, SHA3-256) остаются достаточными по стойкости к коллизиям; 160-битные хеши слабы уже классически (коллизии SHA-1 практичны). Где нужны категории NIST 4–5, используйте хеши на 384/512 бит. |

_Действие: взламывает — алгоритм нужно заменить; ослабляет — более длинные ключи или выходы восстанавливают запас; учтено в стандартных параметрах — при стандартных наборах действий не требуется; только при суперпозиционных запросах — к обычному применению неприменимо._


## 9. Ограничения и допущения

- Отчёт содержит результаты автоматизированного и документального анализа в указанных границах. Он не является юридическим заключением, сертификацией или подтверждением соответствия какому-либо стандарту.
- z — плановое допущение профиля риска, а не прогноз. Публично известного криптографически значимого квантового компьютера сегодня не существует.
- slither: 116 (примеры: slither is not installed on the server (pip install slither-analyzer + solc))
- tls_key_exchange_groups: 50 (примеры: poetry.lock line 9: not in the algorithm registry, not assessed: ["dev"]; poetry.lock line 21: not in the algorithm registry, not assessed: ["dev"]; poetry.lock line 163: not in the algorithm registry, not assessed: ["dev"])
- osv_advisories: 1 (примеры: npm/axios@1.17.0: 22 advisories at OSV.dev, the first 20 are listed as findings; see OSV.dev for the rest)

## 10. План устранения проблем / Приоритеты на 30, 60 и 90 дней

### 30 дн.

| Приоритет | ID | Действие | Тип | Условие закрытия |
|---|---|---|---|---|
| P1 | QSI-2026-06281 | Используйте OpenZeppelin Initializable (модификатор initializer) и отключите инициализаторы в конструкторе реализации. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P1 | QSI-2026-06283 | Используйте OpenZeppelin Initializable (модификатор initializer) и отключите инициализаторы в конструкторе реализации. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P1 | QSI-2026-06289 | Используйте OpenZeppelin Initializable (модификатор initializer) и отключите инициализаторы в конструкторе реализации. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P1 | QSI-2026-06290 | Используйте OpenZeppelin Initializable (модификатор initializer) и отключите инициализаторы в конструкторе реализации. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P2 | QSI-2026-06310 | Обновите @openzeppelin/contracts до исправленной версии (3.4.2, 4.3.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-fg47-3c2x-m2wr (CVE-2021-39167). |
| P2 | QSI-2026-06316 | Обновите babel-traverse до исправленной версии (пока не выпущена; меры смягчения — в бюллетене). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-67hx-6x53-jw92 (CVE-2023-45133). |
| P2 | QSI-2026-06334 | Обновите crypto-js до исправленной версии (4.0.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-rg76-677x-56q9 (CVE-2026-71851). |
| P2 | QSI-2026-06335 | Обновите crypto-js до исправленной версии (4.2.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-xwcq-pm8m-c4vf (CVE-2023-46233). |
| P2 | QSI-2026-06337 | Обновите form-data до исправленной версии (2.5.4, 3.0.4, 4.0.4). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-fjxv-7rqg-78g4 (CVE-2025-7783). |
| P2 | QSI-2026-06309 | Обновите @openzeppelin/contracts до исправленной версии (4.4.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-88g8-f5mf-f5rj (CVE-2021-46320, CVE-2022-39384, GHSA-9c22-pwxw-p6hx). |
| P2 | QSI-2026-06339 | Обновите glob до исправленной версии (10.5.0, 11.1.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-5j98-mcp5-4vw2 (CVE-2025-64756). |
| P2 | QSI-2026-06317 | Обновите base-x до исправленной версии (3.0.11, 4.0.1, 5.0.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-xq7p-g2vc-g82p (CVE-2025-27611). |
| P2 | QSI-2026-06321 | Обновите brace-expansion до исправленной версии (1.1.19, 2.1.5, 3.0.7, 5.0.10). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-6j4f-fj2g-mc7p (CVE-2026-102276). |
| P2 | QSI-2026-06323 | Обновите brace-expansion до исправленной версии (1.1.17, 2.1.3, 3.0.3, 5.0.8). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-mh99-v99m-4gvg (CVE-2026-14257). |
| P2 | QSI-2026-06325 | Обновите brace-expansion до исправленной версии (1.1.20, 2.1.6, 3.0.8, 5.0.11). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-qhr7-859c-m2p7 (CVE-2026-102278). |
| P2 | QSI-2026-06326 | Обновите brace-expansion до исправленной версии (1.1.18, 2.1.4, 3.0.6, 5.0.9). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-rgw5-rvv9-x895 (CVE-2026-69152). |
| P2 | QSI-2026-06328 | Обновите browserslist до исправленной версии (4.28.7). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-73wf-gq98-2v4g (CVE-2026-73088). |
| P2 | QSI-2026-06329 | Обновите browserslist до исправленной версии (4.28.7). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-c83g-rgw3-j3cx (CVE-2026-73089). |
| P2 | QSI-2026-06330 | Обновите browserslist до исправленной версии (4.28.7). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-73wf-gq98-2v4g (CVE-2026-73088). |
| P2 | QSI-2026-06331 | Обновите browserslist до исправленной версии (4.28.7). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-c83g-rgw3-j3cx (CVE-2026-73089). |
| P2 | QSI-2026-06332 | Обновите browserslist до исправленной версии (4.28.7). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-73wf-gq98-2v4g (CVE-2026-73088). |
| P2 | QSI-2026-06333 | Обновите browserslist до исправленной версии (4.28.7). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-c83g-rgw3-j3cx (CVE-2026-73089). |
| P2 | QSI-2026-06338 | Обновите form-data до исправленной версии (2.5.6, 3.0.5, 4.0.6). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-hmw2-7cc7-3qxx (CVE-2026-12143). |
| P2 | QSI-2026-06342 | Обновите ip-address до исправленной версии (10.3.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-mwp4-54f8-5fhr (CVE-2026-69192). |
| P2 | QSI-2026-06346 | Обновите json5 до исправленной версии (1.0.2, 2.2.2). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-9c47-m6qq-7p4h (CVE-2022-46175). |
| P2 | QSI-2026-06348 | Обновите lodash до исправленной версии (4.18.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-r5fr-rjxr-66jc (CVE-2026-4800). |
| P2 | QSI-2026-06350 | Обновите minimatch до исправленной версии (10.2.3, 3.1.4, 4.2.5, 5.1.8, 6.2.2). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-23c5-xmqv-rm74 (CVE-2026-27904). |
| P2 | QSI-2026-06351 | Обновите minimatch до исправленной версии (10.2.1, 3.1.3, 4.2.4, 5.1.7, 6.2.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-3ppc-4f35-3m26 (CVE-2026-26996). |
| P2 | QSI-2026-06352 | Обновите minimatch до исправленной версии (10.2.3, 3.1.3, 4.2.5, 5.1.8, 6.2.2). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-7r86-cg39-jmmj (CVE-2026-27903). |
| P2 | QSI-2026-06353 | Обновите node-fetch до исправленной версии (2.6.7, 3.1.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-r683-j2x4-v87g (CVE-2022-0235). |
| P2 | QSI-2026-06308 | Обновите @openzeppelin/contracts до исправленной версии (4.7.2). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-7grf-83vw-6f5x (CVE-2022-35915). |
| P2 | QSI-2026-06311 | Обновите @openzeppelin/contracts до исправленной версии (4.8.3). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-mx2q-35m2-x2rh (CVE-2023-30541). |
| P2 | QSI-2026-06312 | Обновите openzeppelin-solidity до исправленной версии (пока не выпущена; меры смягчения — в бюллетене). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-7grf-83vw-6f5x (CVE-2022-35915). |
| P2 | QSI-2026-06313 | Обновите setuptools до исправленной версии (83.0.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-h35f-9h28-mq5c (CVE-2026-59890, PYSEC-2026-3447). |
| P2 | QSI-2026-06315 | Обновите @babel/runtime до исправленной версии (7.26.10, 8.0.0-alpha.17). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-968p-4wvh-cqc8 (CVE-2025-27789). |
| P2 | QSI-2026-06318 | Обновите bn.js до исправленной версии (4.12.3, 5.2.3). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-378v-28hj-76wf (CVE-2026-2739). |
| P2 | QSI-2026-06319 | Обновите bn.js до исправленной версии (4.12.3, 5.2.3). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-378v-28hj-76wf (CVE-2026-2739). |
| P2 | QSI-2026-06320 | Обновите brace-expansion до исправленной версии (1.1.16, 2.1.2, 5.0.7). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-3jxr-9vmj-r5cp (CVE-2026-13149). |
| P2 | QSI-2026-06322 | Обновите brace-expansion до исправленной версии (1.1.13, 2.0.3, 3.0.2, 5.0.5). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-f886-m6hf-6m8v (CVE-2026-33750). |
| P2 | QSI-2026-06324 | Обновите brace-expansion до исправленной версии (1.1.21, 2.1.7, 3.0.9, 5.0.12). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-q2hr-2g5m-vwhr (CVE-2026-102277). |
| P2 | QSI-2026-06336 | Обновите elliptic до исправленной версии (пока не выпущена; меры смягчения — в бюллетене). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-848j-6mx2-7j84 (CVE-2025-14505). |
| P2 | QSI-2026-06340 | Обновите ip-address до исправленной версии (10.7.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-h3mg-xc3c-68pw (CVE-2026-101911). |
| P2 | QSI-2026-06341 | Обновите ip-address до исправленной версии (10.7.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-j6r3-76f7-8jcv (CVE-2026-101912). |
| P2 | QSI-2026-06343 | Обновите ip-address до исправленной версии (10.5.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-rpw4-54j3-4h4q (CVE-2026-101913). |
| P2 | QSI-2026-06344 | Обновите ip-address до исправленной версии (10.7.4). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-rxp7-6hxx-x8q5 (CVE-2026-111997). |
| P2 | QSI-2026-06345 | Обновите ip-address до исправленной версии (10.1.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-v2v4-37r5-5v8g (CVE-2026-42338). |
| P2 | QSI-2026-06347 | Обновите lodash до исправленной версии (4.18.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-f23m-r3pf-42rh (CVE-2026-2950). |
| P2 | QSI-2026-06349 | Обновите lodash до исправленной версии (4.17.23). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-xxjr-mmjv-4gpg (CVE-2025-13465). |
| P2 | QSI-2026-06314 | Обновите setuptools до исправленной версии (84.1.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-xmj3-9gf7-h52w. |
| P2 | QSI-2026-06327 | Обновите brace-expansion до исправленной версии (1.1.12, 2.0.2, 3.0.1, 4.0.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-v6h2-p8h4-qcjw (CVE-2025-5889). |
### 60 дн.

| Приоритет | ID | Действие | Тип | Условие закрытия |
|---|---|---|---|---|
| P2 | QSI-2026-06282 | Перейдите на Solidity ≥ 0.8 или последовательно используйте SafeMath. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P2 | QSI-2026-06285 | Перейдите на Solidity ≥ 0.8 или последовательно используйте SafeMath. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P2 | QSI-2026-06286 | Перейдите на Solidity ≥ 0.8 или последовательно используйте SafeMath. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P2 | QSI-2026-06300 | Используйте OpenZeppelin ECDSA.recover с разделением доменов EIP-712 и nonce. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
### 90 дн.

| Приоритет | ID | Действие | Тип | Условие закрытия |
|---|---|---|---|---|
| P3 | QSI-2026-06299 | Внесите использования ECDSA в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-06305 | Внесите использования ECDSA в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-06306 | Внесите использования BLS12-381 в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-06287 | Внесите использования ? в contract:contracts/0.8.25/CLValidatorVerifier.sol в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-06298 | Внесите использования ? в contract:contracts/common/lib/BLS.sol в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-06280 | Перейдите на Solidity ≥ 0.8 или последовательно используйте SafeMath. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P3 | QSI-2026-06288 | Зафиксируйте версию компилятора, использованную при тестировании. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P3 | QSI-2026-06292 | Зафиксируйте версию компилятора, использованную при тестировании. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P3 | QSI-2026-06293 | Зафиксируйте версию компилятора, использованную при тестировании. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P3 | QSI-2026-06294 | Зафиксируйте версию компилятора, использованную при тестировании. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P3 | QSI-2026-06295 | Зафиксируйте версию компилятора, использованную при тестировании. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P3 | QSI-2026-06296 | Зафиксируйте версию компилятора, использованную при тестировании. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P3 | QSI-2026-06297 | Зафиксируйте версию компилятора, использованную при тестировании. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P3 | QSI-2026-06301 | Зафиксируйте версию компилятора, использованную при тестировании. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P3 | QSI-2026-06302 | Зафиксируйте версию компилятора, использованную при тестировании. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-06299 | Запланируйте миграцию ECDSA на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема или гибридной схемы. |
| P4 | QSI-2026-06305 | Запланируйте миграцию ECDSA на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема или гибридной схемы. |
| P4 | QSI-2026-06306 | Запланируйте миграцию BLS12-381 на  (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование  или гибридной схемы. |
| P4 | QSI-2026-06287 | Запланируйте миграцию ? на ? (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ? или гибридной схемы. |
| P4 | QSI-2026-06298 | Запланируйте миграцию ? на ? (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ? или гибридной схемы. |
| P4 | QSI-2026-06284 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-06291 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-06303 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-06304 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-06354 | Обновите зависимости разработки и сборки из доказательства. | устранение первопричины | Сканирование не сообщает бюллетеней для пакетов инструментов, либо оставшиеся зафиксированы. |
| P4 | QSI-2026-06355 | Обновите зависимости разработки и сборки из доказательства. | устранение первопричины | Сканирование не сообщает бюллетеней для пакетов инструментов, либо оставшиеся зафиксированы. |

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
3. C. Gidney, M. Ekerå — How to factor 2048 bit RSA integers in 8 hours using 20 million noisy qubits (Quantum 5, 433) — Quantum. <https://doi.org/10.22331/q-2021-04-15-433> (peer-reviewed article (2021): 10^-3 gate error, 1 µs cycle, 10 µs reaction time)
4. C. Zalka — Grover's quantum searching algorithm is optimal (Phys. Rev. A 60, 2746, 1999; arXiv:quant-ph/9711070) — APS. <https://doi.org/10.1103/PhysRevA.60.2746> (peer-reviewed article: optimal for any success probability; parallel search gains no more than splitting the space)
5. Common Vulnerability Scoring System v3.1: Specification Document — FIRST. <https://www.first.org/cvss/v3.1/specification-document> (final)
6. D. J. Bernstein — Cost analysis of hash collisions: Will quantum computers make SHARCS obsolete? (2009) — cr.yp.to. <https://cr.yp.to/hash/collisioncost-20090823.pdf> (paper dated 2009-08-23)
7. D. Litinski — How to compute a 256-bit elliptic curve private key with only 50 million Toffoli gates (arXiv:2306.08585) — arXiv. <https://arxiv.org/abs/2306.08585> (preprint (2023-06-14): 6000 modules × 1152 physical qubits, one key per 10 minutes under its architecture assumptions)
8. EIP-197 — Precompiled contract for optimal ate pairing check on alt_bn128 (0x08) — Ethereum. <https://eips.ethereum.org/EIPS/eip-197> (final)
9. EIP-2537 — Precompile for BLS12-381 curve operations (0x0b–0x11) — Ethereum. <https://eips.ethereum.org/EIPS/eip-2537> (final)
10. FIPS 203 — Module-Lattice-Based Key-Encapsulation Mechanism Standard (ML-KEM) — NIST. <https://csrc.nist.gov/pubs/fips/203/final> (final (August 2024))
11. FIPS 204 — Module-Lattice-Based Digital Signature Standard (ML-DSA) — NIST. <https://csrc.nist.gov/pubs/fips/204/final> (final (August 2024))
12. FIPS 205 — Stateless Hash-Based Digital Signature Standard (SLH-DSA) — NIST. <https://csrc.nist.gov/pubs/fips/205/final> (final (August 2024))
13. G. Brassard, P. Høyer, A. Tapp — Quantum Algorithm for the Collision Problem (LATIN '98; arXiv:quant-ph/9705002) — Springer / arXiv. <https://arxiv.org/abs/quant-ph/9705002> (peer-reviewed article: collisions of r-to-one functions in O((N/r)^{1/3}) expected evaluations)
14. J. Groth — On the Size of Pairing-based Non-interactive Arguments (EUROCRYPT 2016) — IACR. <https://eprint.iacr.org/2016/260> (peer-reviewed article)
15. J. Proos, C. Zalka — Shor's discrete logarithm quantum algorithm for elliptic curves (Quantum Inf. Comput. 3(4), 2003; arXiv:quant-ph/0301141) — Quantum Information & Computation. <https://doi.org/10.26421/QIC3.4-3> (peer-reviewed article)
16. L. K. Grover — A fast quantum mechanical algorithm for database search (STOC 1996) — ACM. <https://doi.org/10.1145/237814.237866> (peer-reviewed article)
17. M. Amy et al. — Estimating the cost of generic quantum pre-image attacks on SHA-2 and SHA-3 (SAC 2016; arXiv:1603.09383) — Springer / arXiv. <https://arxiv.org/abs/1603.09383> (peer-reviewed article: SHA-256 about 2^153.8 surface-code cycles on 2^12.6 logical qubits; SHA3-256 about 2^146.5 cycles on 2^20)
18. M. Cain et al. — Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits (arXiv:2603.28627) — arXiv. <https://arxiv.org/abs/2603.28627> (preprint (2026-03-30): P-256 in a few days with 26,000 physical neutral-atom qubits; RSA-2048 one to two orders of magnitude longer)
19. M. Ekerå, J. Gärtner — A high-level comparison of state-of-the-art quantum algorithms for breaking asymmetric cryptography (arXiv:2405.14381) — arXiv. <https://arxiv.org/abs/2405.14381> (preprint (2024-05-23): Regev-style algorithms show no overall advantage yet for cryptographic RSA and finite-field sizes)
20. M. Mosca — Cybersecurity in an Era with Quantum Computers: Will We Be Ready? (IEEE Security & Privacy, 2018) — IEEE. <https://doi.org/10.1109/MSP.2018.3761723> (peer-reviewed article; source of the x + y > z migration inequality)
21. M. Roetteler, M. Naehrig, K. Svore, K. Lauter — Quantum resource estimates for computing elliptic curve discrete logarithms (ASIACRYPT 2017) — IACR / arXiv. <https://arxiv.org/abs/1706.06752> (peer-reviewed article: at most 9n + 2⌈log2 n⌉ + 10 qubits and 448 n^3 log2 n + 4090 n^3 Toffoli gates)
22. NIST IR 8547 — Transition to Post-Quantum Cryptography Standards — NIST. <https://csrc.nist.gov/pubs/ir/8547/ipd> (initial public draft (November 2024); proposes deprecating quantum-vulnerable public-key algorithms after 2030 and disallowing them after 2035 — dates may change in the final version)
23. NIST — Post-Quantum Cryptography Standardization: Evaluation Criteria, Security (Call for Proposals, Section 4.A.5) — NIST. <https://csrc.nist.gov/Projects/Post-Quantum-Cryptography/Post-Quantum-Cryptography-Standardization/Evaluation-Criteria/Security-(Evaluation-Criteria)> (security categories: AES-128 key search 2^170/MAXDEPTH quantum gates, AES-192 2^233/MAXDEPTH, AES-256 2^298/MAXDEPTH; MAXDEPTH 2^40–2^96)
24. OSV advisory GHSA-23c5-xmqv-rm74 — OSV.dev. <https://osv.dev/vulnerability/GHSA-23c5-xmqv-rm74> (modified 2026-09-10T03:50:59.274637421Z)
25. OSV advisory GHSA-378v-28hj-76wf — OSV.dev. <https://osv.dev/vulnerability/GHSA-378v-28hj-76wf> (modified 2026-09-10T03:50:33.815513385Z)
26. OSV advisory GHSA-3jxr-9vmj-r5cp — OSV.dev. <https://osv.dev/vulnerability/GHSA-3jxr-9vmj-r5cp> (modified 2026-09-10T03:51:10.092354944Z)
27. OSV advisory GHSA-3ppc-4f35-3m26 — OSV.dev. <https://osv.dev/vulnerability/GHSA-3ppc-4f35-3m26> (modified 2026-09-10T03:50:33.812431744Z)
28. OSV advisory GHSA-5j98-mcp5-4vw2 — OSV.dev. <https://osv.dev/vulnerability/GHSA-5j98-mcp5-4vw2> (modified 2026-09-10T03:50:30.568830409Z)
29. OSV advisory GHSA-67hx-6x53-jw92 — OSV.dev. <https://osv.dev/vulnerability/GHSA-67hx-6x53-jw92> (modified 2026-09-10T03:50:03.372029556Z)
30. OSV advisory GHSA-6j4f-fj2g-mc7p — OSV.dev. <https://osv.dev/vulnerability/GHSA-6j4f-fj2g-mc7p> (modified 2026-09-30T00:00:03.836613572Z)
31. OSV advisory GHSA-73wf-gq98-2v4g — OSV.dev. <https://osv.dev/vulnerability/GHSA-73wf-gq98-2v4g> (modified 2026-09-10T03:51:15.295037659Z)
32. OSV advisory GHSA-7grf-83vw-6f5x — OSV.dev. <https://osv.dev/vulnerability/GHSA-7grf-83vw-6f5x> (modified 2023-11-08T04:09:52.370855Z)
33. OSV advisory GHSA-7r86-cg39-jmmj — OSV.dev. <https://osv.dev/vulnerability/GHSA-7r86-cg39-jmmj> (modified 2026-09-10T03:50:34.376990726Z)
34. OSV advisory GHSA-848j-6mx2-7j84 — OSV.dev. <https://osv.dev/vulnerability/GHSA-848j-6mx2-7j84> (modified 2026-09-10T03:50:32.794069999Z)
35. OSV advisory GHSA-88g8-f5mf-f5rj — OSV.dev. <https://osv.dev/vulnerability/GHSA-88g8-f5mf-f5rj> (modified 2026-07-16T03:56:17.546633851Z)
36. OSV advisory GHSA-968p-4wvh-cqc8 — OSV.dev. <https://osv.dev/vulnerability/GHSA-968p-4wvh-cqc8> (modified 2026-09-10T03:50:22.971593530Z)
37. OSV advisory GHSA-9c47-m6qq-7p4h — OSV.dev. <https://osv.dev/vulnerability/GHSA-9c47-m6qq-7p4h> (modified 2026-09-10T03:49:56.250129993Z)
38. OSV advisory GHSA-c83g-rgw3-j3cx — OSV.dev. <https://osv.dev/vulnerability/GHSA-c83g-rgw3-j3cx> (modified 2026-09-10T03:50:54.622936829Z)
39. OSV advisory GHSA-f23m-r3pf-42rh — OSV.dev. <https://osv.dev/vulnerability/GHSA-f23m-r3pf-42rh> (modified 2026-10-17T02:56:13.084362346Z)
40. OSV advisory GHSA-f886-m6hf-6m8v — OSV.dev. <https://osv.dev/vulnerability/GHSA-f886-m6hf-6m8v> (modified 2026-09-10T03:51:00.342356761Z)
41. OSV advisory GHSA-fg47-3c2x-m2wr — OSV.dev. <https://osv.dev/vulnerability/GHSA-fg47-3c2x-m2wr> (modified 2026-07-08T06:29:37.864167374Z)
42. OSV advisory GHSA-fjxv-7rqg-78g4 — OSV.dev. <https://osv.dev/vulnerability/GHSA-fjxv-7rqg-78g4> (modified 2026-09-10T03:50:57.924154051Z)
43. OSV advisory GHSA-h35f-9h28-mq5c — OSV.dev. <https://osv.dev/vulnerability/GHSA-h35f-9h28-mq5c> (modified 2026-09-10T03:50:52.323347787Z)
44. OSV advisory GHSA-h3mg-xc3c-68pw — OSV.dev. <https://osv.dev/vulnerability/GHSA-h3mg-xc3c-68pw> (modified 2026-09-30T00:00:04.407982988Z)
45. OSV advisory GHSA-hmw2-7cc7-3qxx — OSV.dev. <https://osv.dev/vulnerability/GHSA-hmw2-7cc7-3qxx> (modified 2026-09-10T03:50:49.785679067Z)
46. OSV advisory GHSA-j6r3-76f7-8jcv — OSV.dev. <https://osv.dev/vulnerability/GHSA-j6r3-76f7-8jcv> (modified 2026-09-30T00:00:03.843448355Z)
47. OSV advisory GHSA-mh99-v99m-4gvg — OSV.dev. <https://osv.dev/vulnerability/GHSA-mh99-v99m-4gvg> (modified 2026-09-10T03:50:12.282849322Z)
48. OSV advisory GHSA-mwp4-54f8-5fhr — OSV.dev. <https://osv.dev/vulnerability/GHSA-mwp4-54f8-5fhr> (modified 2026-09-10T03:51:14.478555296Z)
49. OSV advisory GHSA-mx2q-35m2-x2rh — OSV.dev. <https://osv.dev/vulnerability/GHSA-mx2q-35m2-x2rh> (modified 2026-09-10T03:50:01.099654307Z)
50. OSV advisory GHSA-q2hr-2g5m-vwhr — OSV.dev. <https://osv.dev/vulnerability/GHSA-q2hr-2g5m-vwhr> (modified 2026-09-30T00:00:03.849541183Z)
51. OSV advisory GHSA-qhr7-859c-m2p7 — OSV.dev. <https://osv.dev/vulnerability/GHSA-qhr7-859c-m2p7> (modified 2026-09-30T00:00:04.402763332Z)
52. OSV advisory GHSA-r5fr-rjxr-66jc — OSV.dev. <https://osv.dev/vulnerability/GHSA-r5fr-rjxr-66jc> (modified 2026-10-17T02:56:15.633068434Z)
53. OSV advisory GHSA-r683-j2x4-v87g — OSV.dev. <https://osv.dev/vulnerability/GHSA-r683-j2x4-v87g> (modified 2023-11-08T04:07:30.211593Z)
54. OSV advisory GHSA-rg76-677x-56q9 — OSV.dev. <https://osv.dev/vulnerability/GHSA-rg76-677x-56q9> (modified 2026-08-07T19:10:56.177489Z)
55. OSV advisory GHSA-rgw5-rvv9-x895 — OSV.dev. <https://osv.dev/vulnerability/GHSA-rgw5-rvv9-x895> (modified 2026-09-10T03:51:14.535270857Z)
56. OSV advisory GHSA-rpw4-54j3-4h4q — OSV.dev. <https://osv.dev/vulnerability/GHSA-rpw4-54j3-4h4q> (modified 2026-09-28T21:00:05.359993143Z)
57. OSV advisory GHSA-rxp7-6hxx-x8q5 — OSV.dev. <https://osv.dev/vulnerability/GHSA-rxp7-6hxx-x8q5> (modified 2026-10-22T16:30:30.129356757Z)
58. OSV advisory GHSA-v2v4-37r5-5v8g — OSV.dev. <https://osv.dev/vulnerability/GHSA-v2v4-37r5-5v8g> (modified 2026-09-10T03:50:47.603301077Z)
59. OSV advisory GHSA-v6h2-p8h4-qcjw — OSV.dev. <https://osv.dev/vulnerability/GHSA-v6h2-p8h4-qcjw> (modified 2026-09-10T03:50:25.501161917Z)
60. OSV advisory GHSA-xmj3-9gf7-h52w — OSV.dev. <https://osv.dev/vulnerability/GHSA-xmj3-9gf7-h52w> (modified 2026-10-23T22:00:03.739009766Z)
61. OSV advisory GHSA-xq7p-g2vc-g82p — OSV.dev. <https://osv.dev/vulnerability/GHSA-xq7p-g2vc-g82p> (modified 2025-05-01T13:30:57Z)
62. OSV advisory GHSA-xwcq-pm8m-c4vf — OSV.dev. <https://osv.dev/vulnerability/GHSA-xwcq-pm8m-c4vf> (modified 2026-09-10T03:49:58.831533491Z)
63. OSV advisory GHSA-xxjr-mmjv-4gpg — OSV.dev. <https://osv.dev/vulnerability/GHSA-xxjr-mmjv-4gpg> (modified 2026-10-17T02:55:54.229635593Z)
64. OSV.dev — open-source vulnerability database and API — Open Source Security Foundation. <https://osv.dev/> (the database QSI queries for each exactly pinned version; every advisory id in a finding resolves at https://osv.dev/vulnerability/<id>)
65. P. W. Shor — Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms on a Quantum Computer (SIAM J. Comput., 1997) — SIAM. <https://doi.org/10.1137/S0097539795293172> (peer-reviewed article)
66. R. Babbush et al. — Securing Elliptic Curve Cryptocurrencies against Quantum Vulnerabilities: Resource Estimates and Mitigations (arXiv:2603.28846) — arXiv. <https://arxiv.org/abs/2603.28846> (preprint (2026-03-30, v2 2026-04-15): 256-bit ECDLP with < 1200 logical qubits and < 90 M Toffoli gates (or < 1450 and < 70 M); < 500,000 physical qubits at 10^-3 error, minutes)
67. S. Jaques, M. Naehrig, M. Roetteler, F. Virdia — Implementing Grover oracles for quantum key search on AES and LowMC (EUROCRYPT 2020; arXiv:1910.01700) — Springer / arXiv. <https://arxiv.org/abs/1910.01700> (peer-reviewed article: lower cost estimates for the AES key searches that define the NIST categories)
68. Smart Contract Weakness Classification (SWC) Registry — SWC community (no longer actively maintained). <https://swcregistry.io/> (historic reference; still widely cited)

## Приложения: Криптографическая инвентаризация

| Алгоритм | Параметр | Библиотека | Квантовый статус | Классический статус | Количество | Мест | Примеры |
|---|---|---|---|---|---|---|---|
| Keccak-256 | Keccak-256 |  | Гровер: допустимо по NIST, ниже рекомендаций ECCG/ANSSI | допустимо | 35 | 35 | contracts/0.4.24/nos/NodeOperatorsRegistry.sol:360; contracts/0.4.24/template/LidoTemplate.sol:183; contracts/0.8.25/consolidation/ConsolidationBus.sol:166 |
| Crypto library | 6.14.4 | ethers (ethers.js) | н/п | допустимо | 2 | 2 | package.json; yarn.lock:6046 |
| Crypto library | 3.20.0 | pycryptodome (PyCryptodome) | н/п | допустимо | 1 | 1 | poetry.lock |
| Crypto library | 6.20.3 | web3 (web3) | н/п | допустимо | 1 | 1 | poetry.lock |
| Crypto library | 4.0.4 | secp256k1 (secp256k1 bindings) | н/п | допустимо | 1 | 1 | yarn.lock:10758 |
| Crypto library | 0.14.5 | tweetnacl (TweetNaCl) | н/п | допустимо | 1 | 1 | yarn.lock:12026 |
| Crypto library | 1.0.3 | tweetnacl (TweetNaCl) | н/п | допустимо | 1 | 1 | yarn.lock:12033 |
| Crypto library | 0.16.0 | web3 (web3) | н/п | допустимо | 1 | 1 | yarn.lock:12500 |
| Crypto library | 0.18.4 | web3 (web3) | н/п | допустимо | 1 | 1 | yarn.lock:12512 |
| Crypto library | 0.20.7 | web3 (web3) | н/п | допустимо | 1 | 1 | yarn.lock:12525 |
| Crypto library | 1.2.0 | @noble/curves (noble-curves) | н/п | допустимо | 1 | 1 | yarn.lock:1480 |
| Crypto library | 1.4.2 | @noble/curves (noble-curves) | н/п | допустимо | 1 | 1 | yarn.lock:1489 |
| Crypto library | 1.8.1 | @noble/curves (noble-curves) | н/п | допустимо | 1 | 1 | yarn.lock:1498 |
| Crypto library | 1.9.2 | @noble/curves (noble-curves) | н/п | допустимо | 1 | 1 | yarn.lock:1507 |
| Crypto library | 1.8.2 | @noble/curves (noble-curves) | н/п | допустимо | 1 | 1 | yarn.lock:1516 |
| Crypto library | 1.2.0 | @noble/hashes (noble-hashes) | н/п | допустимо | 1 | 1 | yarn.lock:1525 |
| Crypto library | 1.3.2 | @noble/hashes (noble-hashes) | н/п | допустимо | 1 | 1 | yarn.lock:1532 |
| Crypto library | 1.4.0 | @noble/hashes (noble-hashes) | н/п | допустимо | 1 | 1 | yarn.lock:1539 |
| Crypto library | 1.7.1 | @noble/hashes (noble-hashes) | н/п | допустимо | 1 | 1 | yarn.lock:1546 |
| Crypto library | 1.7.2 | @noble/hashes (noble-hashes) | н/п | допустимо | 1 | 1 | yarn.lock:1553 |
| Crypto library | 1.8.0 | @noble/hashes (noble-hashes) | н/п | допустимо | 1 | 1 | yarn.lock:1560 |
| Crypto library | 1.7.1 | @noble/secp256k1 (noble-curves) | н/п | допустимо | 1 | 1 | yarn.lock:1567 |
| Crypto library | 1.7.2 | @noble/secp256k1 (noble-curves) | н/п | допустимо | 1 | 1 | yarn.lock:1574 |
| Crypto library | 3.3.0 | crypto-js (crypto-js) | н/п | допустимо | 1 | 1 | yarn.lock:4895 |
| Crypto library | 6.6.1 | elliptic (elliptic (Node)) | н/п | допустимо | 1 | 1 | yarn.lock:5236 |
| Crypto library | 5.8.0 | ethers (ethers.js) | н/п | допустимо | 1 | 1 | yarn.lock:6061 |
| Crypto library | 6.13.6 | ethers (ethers.js) | н/п | допустимо | 1 | 1 | yarn.lock:6099 |
| BLS12-381 |  |  | уязвим (Шор) | допустимо | 4 | 4 | contracts/0.8.25/CLValidatorVerifier.sol:8; contracts/common/lib/BLS.sol:17; lib/pdg.ts:8 |
| ECDSA | secp256k1 (ecrecover) |  | уязвим (Шор) | допустимо | 1 | 1 | contracts/common/lib/ECDSA.sol:40 |
| ECDSA |  |  | уязвим (Шор) | допустимо | 2 | 2 | lib/ec.ts:10; lib/eips/eip712.ts:41 |

_Длинные списки здесь сгруппированы; полный список по файлам — в JSON-версии отчёта, подписанной тем же ключом._

## Приложения: Входные файлы

| Файл | Размер | SHA-256 | Маскирования |
|---|---|---|---|
| .solcover.js | 694 | `3eb2bc0a01de9c9d5b2bc0a25e0dd9de65e6fca3c2fa63790e400aa751d0565d` | 0 |
| commitlint.config.ts | 67 | `eda2b3989c752320cce88af66b8d488ca4c6f8c417fcd3b9f4e8fd54fbda9284` | 0 |
| contracts/0.4.24/Lido.sol | 70838 | `3bf84b96fb155af2290e6b26bc0138de356442a9abe3ea0f5274497f9fbffc10` | 0 |
| contracts/0.4.24/StETH.sol | 23702 | `63ebed0e205b602fe2e427bb09c111479f98253bd02f96ac052b38202d3713bd` | 0 |
| contracts/0.4.24/lib/StakeLimitUtils.sol | 10421 | `97b006a62f169eefe66279e2827ba5d5663fd74042602a5337a73509468503e3` | 0 |
| contracts/0.4.24/nos/NodeOperatorsRegistry.sol | 75983 | `fd4c08c4e22c066f427acadbfd951ed4441da3ca7821caa78b891f823bd01037` | 3 |
| contracts/0.4.24/template/IETHRegistrarController.sol | 812 | `a52940d09532e7e7ec573e1db0fadbc2e13f8c1b6f8ae0b159ce08737bd586a2` | 0 |
| contracts/0.4.24/template/IInterfaceResolver.sol | 247 | `6ebcaa4a7623dd24b61b524651a4e9ca01c63fc0b561595c74971a3dbeb88869` | 0 |
| contracts/0.4.24/template/Imports.sol | 323 | `52a806178846e721917f44c3fa86e768e456f01e95fca077b833dcdff78764b7` | 0 |
| contracts/0.4.24/template/LidoTemplate.sol | 29621 | `29b3231006cc46cb55921152dbe96f417fde797f5d69c8d70ca15f0c42da29ca` | 4 |
| contracts/0.4.24/utils/UnstructuredStorageExt.sol | 2391 | `11dbb51c4885d38eee1fdd632a45f79223647785ee80c0877a1d7123d7a3aea6` | 0 |
| contracts/0.4.24/utils/Versioned.sol | 1845 | `73804e634f20285f9ed1c323e3c56833048f893d1afe6219afd689076e58dedf` | 0 |
| contracts/0.6.11/deposit_contract.sol | 9425 | `2a8db249155e8502e1132f14410b8d7b2a924512723ed07a08167477d8f8c073` | 0 |
| contracts/0.6.12/interfaces/IStETH.sol | 498 | `3c96c6250a67eca83d5f89c1e7a08b27f3168ec744ca3745df4ace687df6b6b2` | 0 |
| contracts/0.8.25/CLValidatorVerifier.sol | 4816 | `d6e89f6975e4fa02f758bf461a98ac2d689296b5c92d03ffd4e43a22d0b3d7ed` | 0 |
| contracts/0.8.25/consolidation/ConsolidationBus.sol | 15480 | `362741ab332ba2be2ad030c9e34534bf7bff0ed408ae8374ca67cba3ff115b88` | 0 |
| contracts/0.8.25/consolidation/ConsolidationGateway.sol | 15339 | `86eee98160b1b24c84a7ebf37cc053aa09cea7a4b78f43d5c12651e4ca923426` | 0 |
| contracts/0.8.25/consolidation/ConsolidationMigrator.sol | 14868 | `cea8ed0280ba02439456fe00cfea8762670770b83e7dff7146c31dc4cce19263` | 0 |
| contracts/0.8.25/lib/BeaconChainDepositor.sol | 6296 | `b4afeac2e4dab53d2b6d1cebcf41bfc670eb1ea069cb1d5bc0e07f1932bf9fe0` | 0 |
| contracts/0.8.25/sr/ISRBase.sol | 3910 | `63466ac2f70f94c6b1045c628a7b677975aad56b95d7b8634758e97bdbebeb64` | 0 |
| contracts/0.8.25/sr/SRLib.sol | 47235 | `2a53ec2d183f3c3d8b6257f18dc7143e8afbc8d3d2f8a48bd0e5e0580b5b47ab` | 0 |
| contracts/0.8.25/sr/SRStorage.sol | 2842 | `62e922f76a1db7756684d73db3151a02f6d8f0de51fac27922f0a4095ceb9d95` | 0 |
| contracts/0.8.25/sr/SRTypes.sol | 13237 | `22c28be7ceaf6ed841f18fc19296372ab246b1cfecc87902d49ee1670ed4aed6` | 0 |
| contracts/0.8.25/sr/SRUtils.sol | 3608 | `1f59e455e510e5eb9c19bdf64dd7357c3e4a8c445c5baaa2f3691ecb7115d295` | 0 |
| contracts/0.8.25/sr/StakingRouter.sol | 55709 | `4d5b83fc73736db6755ebbb58811ed499c3e6de622cce11a3ad8548800a34155` | 0 |
| contracts/0.8.25/utils/Confirmable2Addresses.sol | 1006 | `1a4bdfbdb2dfe7ef3dd47571325a590abcc53a7001edafd85d990913a13333e8` | 0 |
| contracts/0.8.25/utils/Confirmations.sol | 9638 | `7db1b26aff6ecdfad6fdf16ebe1f8076ef8106688b1313f73ba7610975d107aa` | 0 |
| contracts/0.8.25/utils/PausableUntilWithRoles.sol | 2269 | `70dec91c2b4c322dce02f1f2ce5dbbb578249b92bb97fa484c9fad62e1a53495` | 0 |
| contracts/0.8.25/vaults/VaultHub.sol | 79517 | `d9aa5d6ac42bc9c5b83b2c80fe96a81649e5b0f7b92e29b0b805eb6197e6f3e7` | 1 |
| contracts/0.8.25/vaults/dashboard/Permissions.sol | 14666 | `85d9b2b3f32da5465ff435e94437de8f1115bc6ffada5492d5b3f11a132a0e0f` | 0 |
| contracts/0.8.25/vaults/interfaces/IPinnedBeaconProxy.sol | 402 | `cdd548cdea22eb318efd3a59cec7d164f257453a91c4b54d1467454e1de0da68` | 0 |
| contracts/0.8.25/vaults/interfaces/IPredepositGuarantee.sol | 2514 | `121d88c8332021e4d163c807c4edef5d6b4744832ec1d9498259d62cd2af9d87` | 0 |
| contracts/0.8.25/vaults/interfaces/IStakingVault.sol | 2977 | `3a812ce040da103a50824cf1ad35823a655e9bb1920f8d8c8219d290ee0c7cc6` | 0 |
| contracts/0.8.25/vaults/interfaces/IVaultFactory.sol | 246 | `f8d1c9fb1df9fcaacb5cab5efdbaf6e149e066813eb77a44eb7274548dc32198` | 0 |
| contracts/0.8.25/vaults/lib/PinnedBeaconUtils.sol | 1721 | `c75bfba1086f02282f846e5d5c16c68b21dab7f8147688d076c90e14a9b2661f` | 0 |
| contracts/0.8.25/vaults/lib/RecoverTokens.sol | 1746 | `6eeb52f252dd0ebf4c6a05a9fd77cca897d56676d1229710efaf512a2ab806d0` | 0 |
| contracts/0.8.25/vaults/predeposit_guarantee/MeIfNobodyElse.sol | 892 | `75a0f4eca6feecacb57250c91127e0ff71d04d13b4a15d1e9772ac3845685cac` | 0 |
| contracts/0.8.9/Accounting.sol | 24101 | `dc0609ab76e462be8b28806cc768f22bdd61f24f23d45baef5ec3b1457bf659f` | 0 |
| contracts/0.8.9/TriggerableWithdrawalsGateway.sol | 12231 | `22a41b19c7b44b6e6a86ead5ba942ddab36e9ca44f2586040375a82eb9dad55a` | 0 |
| contracts/0.8.9/WithdrawalQueueBase.sol | 28146 | `68d8919f89198c3d39272b2259a3144bf87a4aa48c570624b025fd86da47d2bb` | 0 |
| contracts/0.8.9/WithdrawalVaultEIP7685.sol | 4718 | `e7dad85a284b7c07038bff8e936fb677a79b1fa9d2e8b9d628d3a107d9b79489` | 0 |
| contracts/0.8.9/interfaces/IERC4906.sol | 1066 | `a61a64cdb68aa429ad4ef10cc508b8735a8241acedcbf7d4850a283047b4deb6` | 0 |
| contracts/0.8.9/interfaces/IPostTokenRebaseReceiver.sol | 662 | `4a30d88b2ab684c9030f0755a2d8d21beacb94614865f9f9b52577d2e2970611` | 0 |
| contracts/0.8.9/interfaces/ISecondOpinionOracle.sol | 1118 | `596cb7b854a0a77a1ef9690f2eb6af7f0625d4fbca676ced7d0a1b96b2a22508` | 0 |
| contracts/0.8.9/interfaces/ITokenRatePusher.sol | 519 | `9013b385ae4b330e011929ea5bebb6d6e61164fce8c5ec81a0dad480c30c20fa` | 0 |
| contracts/0.8.9/interfaces/ITokenRatePusherWithArgs.sol | 1928 | `a2eefece47109d497938a9a71015d24fc83101d33ce1f46dc2a247426b32e48d` | 0 |
| contracts/0.8.9/lib/ExitLimitUtils.sol | 4676 | `6f6bb8bec3c3eee6690d71b1b5d494c66a746d468f789dbb9883d6eefe4b927b` | 0 |
| contracts/0.8.9/lib/UnstructuredRefStorage.sol | 553 | `83b045f33e8f28351cbbe2e14f872526d02f95a6000728291ae436112d04423f` | 0 |
| contracts/0.8.9/lib/UnstructuredStorage.sol | 1199 | `955bfcb0bf265db114248bdabeabebc39bddb3fbb756e2448f6aed59f1994f56` | 0 |
| contracts/0.8.9/oracle/AccountingOracle.sol | 38878 | `bac9aa7db51322470e6bd38550c7d72c408051a82f79ddf7f4b5ba7ffe29bc40` | 0 |
| contracts/0.8.9/oracle/BaseOracle.sol | 16706 | `3579ab8bef4d4d3a16789cde52e60e478b4cea75a4ddc601cf9e74ea56effd9c` | 0 |
| contracts/0.8.9/oracle/HashConsensus.sol | 43873 | `517874ab586ec9859281b62081980a0ea98e4ad1eaf04642f246995078017b29` | 0 |
| contracts/0.8.9/oracle/ValidatorsExitBus.sol | 46084 | `8cffe1fe5577ebb0ddd1a1d4e2e7454b82f780216648e538f69021278d7cb920` | 0 |
| contracts/0.8.9/oracle/ValidatorsExitBusOracle.sol | 11205 | `c986fc00f6aeb44c73e1a4e6b5261da6da4125b125a8b5a08e32a40ea6de6ecf` | 0 |
| contracts/0.8.9/proxy/OssifiableProxy.sol | 3516 | `3fb48bc4a40c887dd581178d05316745c1b1c393a8e64787ef2a7075f1e7ce6d` | 0 |
| contracts/0.8.9/utils/DummyEmptyContract.sol | 278 | `edf59d17c1eb25e3de3c6922e6fd9d8cd88d9903d49c37afad7088788c338580` | 0 |
| contracts/0.8.9/utils/PausableUntil.sol | 3156 | `afd11f5950050bbc8e9fad3cbea2a5bdbcc23048128c30f335a12b48084c8594` | 0 |
| contracts/0.8.9/utils/Versioned.sol | 2430 | `7f9ba0a2368d7531447a80e80ae28406964acf51ca0de8bfa985620e226340a8` | 0 |
| contracts/common/interfaces/IBurner.sol | 1329 | `1747753535963f43c83b9d072cf05acae8b46d11e73a0d24455b56ded35c5170` | 0 |
| contracts/common/interfaces/ICircuitBreaker.sol | 531 | `741d8845a1f696dda4d1d6111f8bd457beee6bbe523a40626bbe0675252d618d` | 0 |
| contracts/common/interfaces/IDepositContract.sol | 536 | `d7b36c2de36cfc68a3fa0812add4e9c55879188a08317166a0ab0f63baaffc63` | 0 |
| contracts/common/interfaces/IEIP712StETH.sol | 1621 | `449180685b8dc86d2ed43eeb92c375938e5d3b17b41ccce011f79bb0f5807a61` | 0 |
| contracts/common/interfaces/IGateSeal.sol | 466 | `6ae2cd5968636651e97dcb99f2d8d476d0e4d0251a6cbdde53d5bf94c5aa4e8b` | 0 |
| contracts/common/interfaces/IGateSealFactory.sol | 540 | `3d7359e7d6b091f4fc300383bf39e06c16e0fd14606b1ac308ac694f1ad55b59` | 0 |
| contracts/common/interfaces/IHashConsensus.sol | 755 | `014793d5760909e6a82baed6e142ea7e512d81daffe10d5bac27b05a79313182` | 0 |
| contracts/common/interfaces/ILazyOracle.sol | 521 | `9249d6a81c7d44c062acd1ffb1ce8a38c07999d0bc8be913697e8cb9e4fa1df8` | 0 |
| contracts/common/interfaces/ILido.sol | 2818 | `083ac5688804237329e50e4c966cae6b782bd9000f092a9740ddb738f234ea2a` | 0 |
| contracts/common/interfaces/ILidoLocator.sol | 2732 | `cc65faee8789012cbb58c0073c770bddb37c9a7fc2594ff2e200fc7894a2dc7a` | 0 |
| contracts/common/interfaces/IOracleReportSanityChecker.sol | 1599 | `3329ace700baa6a521da6bcea2f0b4013deba1f8a7b9833fc50e1683b6f1bcfd` | 0 |
| contracts/common/interfaces/IOssifiableProxy.sol | 564 | `717bf674a2d98e46523610f97c74e27b9521582e8f8cb55b285b10b8c3b875fe` | 0 |
| contracts/common/interfaces/IPausableUntil.sol | 601 | `0377e3ac9ff2d6be41f4b8f40eee7cfd452ce6de760f9b9145fdb38b94902de3` | 0 |
| contracts/common/interfaces/IStakingModule.sol | 13120 | `4a98e89e763d19b45cb1ea422cec1c554fbd43c9f39c6bcc7a18aad64d46e193` | 0 |
| contracts/common/interfaces/IStakingModuleV2.sol | 1511 | `eacc19c668dd2ad94c7c0cffc5957181b8bf1ed2321c14c34c9845ea054a64ce` | 0 |
| contracts/common/interfaces/IVaultHub.sol | 456 | `d50dab7c4bb078c078a6f16aefaebfaa3ae44715aeba44dc42d57e894454ee70` | 0 |
| contracts/common/interfaces/IVersioned.sol | 321 | `1cd7edd080482e1f3dc191ae56cd99be90fbdc3b71750c1652a81d57e871bc68` | 0 |
| contracts/common/interfaces/IWithdrawalQueue.sol | 450 | `b59b2fe9e01bb1be2e0b286b972afe2cafd2ee7210a96f4c1703c17a7777fb1c` | 0 |
| contracts/common/interfaces/ReportValues.sol | 1189 | `faed77fa80f76b04d39bed32df19e44ed55ed047724dbc26c54bb7ecd9034862` | 0 |
| contracts/common/interfaces/TopUpWitness.sol | 482 | `34135d561e4d8c3f1585cdbc15d20f568e36bb37db6c8d4444a8d0cd48cef44d` | 0 |
| contracts/common/interfaces/ValidatorWitness.sol | 673 | `8fd24cfab7402233029756e52e59198b0d9cbf0a42e5c07d9fa2338ed731a5f7` | 0 |
| contracts/common/lib/BLS.sol | 27412 | `0187cc6a6b1aaa833317695d88795db431fa237452213e8c3872a0f444dceb7c` | 0 |
| contracts/common/lib/BeaconTypes.sol | 583 | `9591e9af1a4fd398db86267f3589e763f9eb2016bf29e26cfa50988cf73a10c3` | 0 |
| contracts/common/lib/Bytes32String.sol | 1430 | `636dcd8b3f4959176ad044df3d9c55611ff939b13f0bfeb1070c827f6d46ed50` | 0 |
| contracts/common/lib/ECDSA.sol | 2925 | `9bf07e0a958e4eb956e22214d4a37537527f20966b325d1954a32f99c8945ab4` | 0 |
| contracts/common/lib/GIndex.sol | 3363 | `2653bd4ba89c349f3db36f21a8afc6a24e0e233816d9b608f46d048feb601d1f` | 0 |
| contracts/common/lib/Math256.sol | 1537 | `028e9b0c87fea3ec6fd5aac9e7a5724a18b4a175d5ab70159f24428dd28ea6b6` | 0 |
| contracts/common/lib/MemUtils.sol | 2604 | `dc4f389cfd1ae1b4dd5fe908432159103544ece1ca9f694093f64def5db7acca` | 0 |
| contracts/common/lib/MinFirstAllocationStrategy.sol | 5647 | `90aae2101a74b1aec03470da771f673dc4310ae415e31391d81c589403166b9c` | 0 |
| contracts/common/lib/SSZ.sol | 9809 | `91ef497b972bbee0fe89043034e6bd62fa0c1059f22874d4826bc6164a22009b` | 0 |
| contracts/common/lib/SignatureUtils.sol | 2600 | `b3d93a1bcd82ea289ce7b8dde4b50e98e6719b26a3271f50f9766d650b143c7d` | 0 |
| contracts/common/lib/TriggerableWithdrawals.sol | 7998 | `ad2b6f0f4378b2717c323c0a6b340aed86211366cb195ec68fd537144d4815ac` | 0 |
| contracts/common/lib/UnstructuredStorage.sol | 1254 | `ca4ad93eedff40de12fdd50a88ef608650139a5543fd160dab61cad4d3c03160` | 0 |
| contracts/common/lib/WithdrawalCredentials.sol | 1709 | `cf5e77be0c5d522d853d19a4c5284e53fa0fb149a9902f77648a8f6d5584636c` | 0 |
| contracts/common/utils/PausableUntil.sol | 3364 | `f27405a7f52a15f7e1b10a73ae57ed69fe6514aaba821415e5584458546cf255` | 0 |
| contracts/openzeppelin/5.2/upgradeable/access/AccessControlUpgradeable.sol | 8234 | `d32578f73ad0a24f65d8208033226cc5567a9df2a57fabadf644f6e4e7f172a4` | 1 |
| contracts/openzeppelin/5.2/upgradeable/access/Ownable2StepUpgradeable.sol | 3432 | `de8bb1febdcb330afa3046809f8c62df233f7615acf71641330f1b10a98652aa` | 1 |
| contracts/openzeppelin/5.2/upgradeable/access/OwnableUpgradeable.sol | 4033 | `e566e534ad84f7b18a490f07d6faf597b4c9ba5f34d3efc006944d5ec4ed517d` | 0 |
| contracts/openzeppelin/5.2/upgradeable/access/extensions/AccessControlEnumerableUpgradeable.sol | 4748 | `b6b854fdb69cfe58d7494f6cfc1920a68b504c32e97f6028b6d62a844bc17426` | 1 |
| contracts/openzeppelin/5.2/upgradeable/utils/ContextUpgradeable.sol | 1194 | `a08e16324da33a9d666dc07a22ae58031c242a3869f6808e55b4b82fc70cb209` | 0 |
| contracts/openzeppelin/5.2/upgradeable/utils/introspection/ERC165Upgradeable.sol | 1189 | `76f4b4b6f5d8de71b0b29d90f2b277b88b2c45898340b20b278b9e9ed5074f77` | 0 |
| contracts/upgrade/EDFUpgradeConfig.sol | 11461 | `d7e6d4598eb94595ca99814bef5fb325fc21e123758c2470822849117ee853a9` | 0 |
| contracts/upgrade/EDFUpgradeTemplate.sol | 16822 | `606e2ea7b0afe3accad730915c458da6c40a2cdc6e9a96db9694cb1046dc5b4f` | 0 |
| contracts/upgrade/EDFUpgradeTypes.sol | 3066 | `4b111d4a1764bf8b88b547fa7ad5578431208725e24b0160cf4fa1ce96a913ce` | 0 |
| contracts/upgrade/EDFUpgradeVoteScript.sol | 6627 | `2979daf72e940565f1b9c8abb048bb87b61f5d93bab7a446a537b47091e0f9a1` | 0 |
| contracts/upgrade/UpgradeConfig.sol | 23308 | `4012b572647a483f201f047da03ada1419bac507028fe206a9fc558da2ec04f4` | 0 |
| contracts/upgrade/UpgradeTemplate.sol | 41420 | `e1a316bdeda9a8790cb1bb36b2245bec36db4807fce7a541477d1cc749c8fe64` | 0 |
| contracts/upgrade/UpgradeTemporaryAdmin.sol | 5908 | `9854df9743b2356f30ceabc9decf7bba84b060c8c3c40c704ace82299a875cb1` | 0 |
| contracts/upgrade/UpgradeTypes.sol | 16001 | `0f9e9a720d8712c0b54424d5ab1204cf4b414cd768bf64d0c7924acef22ef636` | 0 |
| contracts/upgrade/UpgradeVoteScript.sol | 38181 | `f90360322277764e49f2943d0c63d756fe4de8004ad8695376eff03fa84f28fb` | 0 |
| contracts/upgrade/interfaces/IDualGovernance.sol | 1625 | `cf24028f4efc2ddbb61841951d9f1719b605b23a6233d78a4cdcafbca338ac76` | 0 |
| contracts/upgrade/interfaces/IForwarder.sol | 334 | `ec9ca4a866435aec84fa4ca3dc816c46f332a166ec723450b3c82726366c1fdf` | 0 |
| contracts/upgrade/interfaces/IOracleReportSanityChecker_preV3.sol | 3870 | `8491e79239f840e48e86ee78973ec6ea6f428836ad6fb15c4e6e44a9b736e06b` | 0 |
| contracts/upgrade/interfaces/IOracleReportSanityChecker_preV4.sol | 1001 | `e6f1eebef4d55c3dbffd39bd6d48eef00cf2a9cd5e918ee2048de3866091cdb8` | 0 |
| contracts/upgrade/interfaces/ITimelock.sol | 1162 | `7325aa5bc0e07df9e08b462ee317200cd886b2342ba692e7ead3cf02b59adfd8` | 0 |
| contracts/upgrade/interfaces/IUpgradeConfig.sol | 909 | `aa54e14e56a9671973195d896857aec8657da41ea404c911bc99f58d9acfcadf` | 0 |
| contracts/upgrade/interfaces/IUpgradeTemplate.sol | 354 | `6282bfde4448a8d95ec11d56dd98599342d39de9258db9f275824ef743d8456b` | 0 |
| contracts/upgrade/interfaces/IVoting.sol | 888 | `2ee30a8e06421d3d5860dde1e5fd6bbc6f89f608bc462cf47131e83be8cd5e06` | 0 |
| contracts/upgrade/utils/CallScriptBuilder.sol | 1504 | `360bbbc8e103db84b0b51ddf32a999505c6f09188830437658ca0991f2a160a2` | 0 |
| contracts/upgrade/utils/OmnibusBase.sol | 6065 | `cc90638544abe5365e9846e1e476eb3c02cf3ee0a6281c7684446a6a989fe0b3` | 0 |
| eslint.config.mjs | 2149 | `8e3d51dfab007829d44f46958cef89783422f0e355d825139774ad7030f13b3a` | 0 |
| globals.d.ts | 4330 | `a2a6c4b08f34f9dff798fb5614649b26eeeae4cd91ba47af703b4fb17027c2fe` | 0 |
| hardhat.config.ts | 7283 | `d88a3e927cea86a783f08f6505e910a1f11693c4ba1c1e2653f429ee840bae4c` | 0 |
| hardhat.helpers.ts | 1447 | `89412e4079f62341ab07f207486d090dc22a42e5e81655de25fe13a7ade6bd08` | 0 |
| lib/account.ts | 2493 | `00bd4ad3f9afc13522eaf1139aa4e7a1e7155241166f9498d8332af425590a92` | 0 |
| lib/address.ts | 293 | `dd0092a3a15b0cc0833cf2e4428669292f5cc098e30a7fff63d8ec870fbc2a2f` | 0 |
| lib/artifacts.ts | 714 | `8299f787d5b765bc28c9d60dfcf40b22f4d8cdd207918e71901b47fa3023d2e4` | 0 |
| lib/bigint-math.ts | 277 | `17195c888fa4607120deb9653d6b4b1624e18eef989ee236e552c59ae26438e9` | 0 |
| lib/bytes.ts | 292 | `a3462239703ab65c727a869874276834baecc2ee43f0cee3626eeb3c9afe97db` | 0 |
| lib/config-schemas.ts | 35855 | `c82facf384ee95f1e4e354e0499a8a606a15cbd6ad1d50c5e88877a78342544e` | 0 |
| lib/console.ts | 2791 | `1f839add41f66065e270f4ba2bd015959da91d67b70f081006d69cda9365040b` | 0 |
| lib/constants.ts | 3455 | `2c5d14323f50b437d6b69f95d8ea4f7d8ebe332a7dd4ce7ea93a9388bbc165e6` | 0 |
| lib/contract.ts | 3982 | `273767f4cd77685f2ff6ff9d65e923b9048864b0bdf6047beee9b2be22d48a82` | 0 |
| lib/deploy.ts | 10140 | `65653813eb06e85db7017e86482559f537897ea35575c845b4ee6c609600309c` | 0 |
| lib/deposit.ts | 4465 | `a265047f6eb1137379d406479abfa8903c9dfc301e3ae57cab74630c4ee21938` | 0 |
| lib/dsm.ts | 3315 | `db8d463f2423956dca53c2db023395d9f18a33dfe9b5c051208a5575bdb652e2` | 0 |
| lib/ec.ts | 546 | `154d165895eafdad4c62cbc9e0dd637ed8224c06a80d2e3c1b3f21056882c18c` | 0 |
| lib/eips/eip4788.ts | 1106 | `1221278718eb5623d7450bef216c3cd5c8ac98c62328fc2726a4410775219809` | 0 |
| lib/eips/eip7002.ts | 3480 | `cf18430e02ce825b3ec19e8ba0d855ce17fc9e197a33dd400479a7c068cee16c` | 0 |
| lib/eips/eip712.ts | 1247 | `53ea90ee23f76ac005553b82f81b903fa1a13e65bfe753243131c54f9646352e` | 0 |
| lib/eips/eip7251.ts | 1816 | `8d2cfc9f66704d4999453ea4377cf22c76c20309f73fbae1d486876d4321db87` | 0 |
| lib/eips/index.ts | 107 | `6b04ddf22683f0401e8d4db881aff79252b86a9b30256af1d48652cb0df21109` | 0 |
| lib/ens.ts | 2034 | `997e325f4c904a59703fae759b297a6c112063db7020fbb9e367985ff2761182` | 0 |
| lib/event.ts | 3183 | `9ab0b25df1ab4040138f6f5ccc0098d8ad0e65e1c75301452c7ba44ead6328fe` | 0 |
| lib/explorer.ts | 1085 | `36ed46f8a069d9fb5c878f3d475bfa5cd52bbfda77899bfc73cfd3a51c755290` | 0 |
| lib/index.ts | 805 | `e0635d5932153c1a852fa4ea05d30acd1a4cc7ae484fb814ad9d481eb645dd95` | 0 |
| lib/keccak.ts | 126 | `fec96f2444bd54d13fc48a233c740629860a344aa43e881085d46d661206a7c3` | 0 |
| lib/log.ts | 7017 | `665ddd4c758281f97bd8f234cb9efb801d8e535c4a3037ecaff94317c8779c1a` | 0 |
| lib/network.ts | 478 | `7c4bd6de4ec677b12c329c206e8d95f7a641caefc5f856913b44b79e6ccf1d0f` | 0 |
| lib/nor.ts | 6003 | `157ef75f969d96850119dd152cde76cf716e40e2d3a8ccea5098a9500118a2cd` | 0 |
| lib/oracle.ts | 9162 | `21b88b51a802b7d6e65d44a1919f32e25f150b2220b4d38db202091d631702f5` | 0 |
| lib/pdg.ts | 10734 | `19be37c418e814ce84a8e09335b8a56f7cd19cf888036194b4dc5d249e56a28b` | 0 |
| lib/promise.ts | 1684 | `0fe746672e3a5118cd2714051780c838815774933f3196dae0c73b158ffc2270` | 0 |
| lib/protocol/context.ts | 3412 | `bc9c97893caccbe8483156d5aad13a476a9a3e69e43e425892d8a6e482ee93e8` | 0 |
| lib/protocol/discover.ts | 11935 | `bf89b2f7c3e146aa8b9299b9c7dda8814670a1d3149f155874392ff8dc7043c3` | 0 |
| lib/protocol/helpers/accounting.ts | 43472 | `a6c15dc8d51502467b20240d4913850a3ff20ec28710b5abc16ddb0675f25bb3` | 0 |
| lib/protocol/helpers/cmv2.ts | 20858 | `84154f6ab4e6b65a90e0accf76290be8039f402565c387beb146aae437d0bc2d` | 0 |
| lib/protocol/helpers/consolidation.ts | 7026 | `b30515be8317c5e02fef46548992a147feb32ebb838804abba5cef4e71ebe69b` | 0 |
| lib/protocol/helpers/dsm.ts | 2868 | `31690dde4df12bdfb1098929824942d603dddf5a45e3bae58ddf98a624a4433b` | 0 |
| lib/protocol/helpers/edf.ts | 2618 | `935eddbc318401849f81555890ccfeca1f32ad63ed05ab08853c159768787eba` | 0 |
| lib/protocol/helpers/index.ts | 2576 | `f404e5b710a4cc4042c385031530344e4b114004ecd8ff4162b927fcf3f20d10` | 0 |
| lib/protocol/helpers/nor-sdvt.ts | 13830 | `7c2e945df03e31e661da005b9605ba836b764c6790e99f81479200bdf822f280` | 0 |
| lib/protocol/helpers/operatorGrid.ts | 3980 | `b9dd2a377bad966c706a832634efb32e4abae191b1a4c49825552a216693f42e` | 0 |
| lib/protocol/helpers/pdg.ts | 893 | `b6dfda592fa19da93d79f7a4a4c2fcd8468fa2a68798244659d31604d89b0523` | 0 |
| lib/protocol/helpers/sanity-checker.ts | 3576 | `2792b84755e88af23b2468d33ffed2b5e1c042422833ea88ed9de348a2843aff` | 0 |
| lib/protocol/helpers/share-rate.ts | 3983 | `21a15f23959162c4b23d2377663511161ff6a2dda84b1c982eafc3412c180b9c` | 0 |
| lib/protocol/helpers/staking-module.ts | 1291 | `035e8b7df7d81c0c72d44da7e6f6c24a68dd6caefb030405e359f22ac7af4afc` | 0 |
| lib/protocol/helpers/staking.ts | 22663 | `35c54dc3a53d0a88abe6460c7b1d14ef2f333f85f84224be9cda385b38f26821` | 0 |
| lib/protocol/helpers/topup.ts | 9989 | `e3107012548e684913eb439a5cd1fd612eb734e875a2a89ba25524430965f867` | 0 |
| lib/protocol/helpers/vaults.ts | 25421 | `bc3c3f8a0977984c5d4f5addcb6a8656efea53f7523634cb5162df620c7c50d6` | 0 |
| lib/protocol/helpers/withdrawal.ts | 3064 | `bd76894995e3df9a08e7db9809ca46c1b03f291390c8e426d3941fb5bb3d0bd6` | 0 |
| lib/protocol/index.ts | 196 | `9a76fb95ba2a252a4c38d0f02a908854bb8ade5c628bcf299067caaa4506b4a8` | 0 |
| lib/protocol/mainnet.ts | 349 | `f1ce96e30cf6f9c1ef6115a18f4c1e61189cf73d122c95aae382161f4eb66dbb` | 0 |
| lib/protocol/networks.ts | 6834 | `afbff4a71df886ce4170c64c2b6c86f0baf711951ef16ba72daf59259999df70` | 0 |
| lib/protocol/provision.ts | 3527 | `f05ff39256e0fc589a622063abdd084751ee9cf4e126f1c275de0c9dd6dead00` | 0 |
| lib/protocol/types.ts | 7419 | `4cf999a22bd65958ea01f3f34f2c643c4454ff37f7a5e683793f7667419dd687` | 0 |
| lib/provider.ts | 1325 | `a5511869145cb4a967db8b9c6ee1c6417eb9cc88eff3fefc00794ff2a9f034e7` | 0 |
| lib/proxy.ts | 783 | `f20763cc7c9d03e78f9c05bfbd5ca0f71d303e2fc79139e2ff815a7cae304e97` | 0 |
| lib/scratch.ts | 3638 | `8c9404e7e65420497803a5fd48eb70862a1f0671ef37f7dd99ef7135284d2381` | 0 |
| lib/signing-keys.ts | 2476 | `10a99cd5c9b240e8bcb3879d5ff1caa92a3e37c59e4e6d38127578b8354a50cb` | 0 |
| lib/state-file.ts | 13590 | `3ff8fb8d261aeb4bdb3f4467b3488a43503daf8fe9e4de8b88903cb674a4e5cc` | 0 |
| lib/storage.ts | 1615 | `82e124245a0b2ff6183c2d1dd92dedf96354dc3e0b8915445d41ee4274cece9d` | 0 |
| lib/string.ts | 1157 | `77f773cd7123d6613b5f23a88452b086eece41c62bf2445a4f9587925bf7f6a2` | 0 |
| lib/time.ts | 2299 | `7ff0193a693d5aa07de71bef8242cd4aa69a38c4e72510847276d98e59d49798` | 0 |
| lib/top-ups.ts | 962 | `e7f3e2c8c7112d3614b509221f044df5b2ad74a8f5033913e576e91510f9e9c9` | 0 |
| lib/units.ts | 377 | `e72aabf57c4e2a1044144fc4a0cdd1f2a9af578685df421a3eb6f0ddedda402f` | 0 |
| lib/wc.ts | 1028 | `c16d44c09096c97b7c3090c3a61f5bbefa358eb580f444cdfddfa798a6210068` | 0 |
| package.json | 6791 | `e714df7b4ff13932cfc3f431b62eff6aba032deeaf759e3307e466fc06eaac1e` | 0 |
| poetry.lock | 242918 | `128104f06088106ef01bd0043fd7228de6e6d5959f93bc1fca0da296cbef12e1` | 4 |
| pyproject.toml | 456 | `53340d428b9c07503771d876d67c575bea70d6fb6bf64fdf624dc52b5da678ab` | 0 |
| scripts/archive/srv3-hoodi/steps/0100-deploy-wv-impl.ts | 1722 | `588e0746b9c4472ce1bfa728cef57f0d0a46827279a4999b77b8fb0596c8dd49` | 0 |
| scripts/archive/srv3-hoodi/steps/1000-voting-wv-impl.ts | 2912 | `66c6327b63966e60fac5c77ff5b0fb76148a305c7b1237653f409b06da208cd3` | 0 |
| scripts/archive/srv3-hoodi-upd1/steps/0911-upd1-deploy.ts | 11156 | `7b9a0ad864ea64c76d41b6b165c4c0819294f9e97127e629170cbe64ceb4e25c` | 0 |
| scripts/archive/srv3-hoodi-upd1/steps/0911-upd1-voting.ts | 15604 | `d5db690e1fef454d35635bd8146aa61da4c77bbb6dc3ac5909416112e998b78a` | 0 |
| scripts/archive/srv3-hoodi-upd2/steps/0911-upd2-deploy.ts | 6204 | `dbacf0abd5d9bde557c54f53e9a1a0218d766665ab4909d988a38ebfe745905f` | 0 |
| scripts/archive/srv3-hoodi-upd2/steps/0911-upd2-voting.ts | 5278 | `6966b6a509de843170ff832abcf82334333ad3ca70e0e9dd00d985955b1a90e9` | 0 |
| scripts/archive/srv3-hoodi-upd3/steps/0911-upd3-deploy.ts | 1041 | `7222f1ed89731879da706ceb47303f4071736a0893ad8d4943329db7ed4904fc` | 0 |
| scripts/archive/srv3-hoodi-upd3/steps/0911-upd3-voting.ts | 3395 | `f4860a03a3397b9ccdf7437e95e8d29339646f9c66d5ed05e4647a7e4e291fbe` | 0 |
| scripts/archive/srv3-hoodi-upd4/steps/0911-upd4-deploy.ts | 2657 | `a08bc92abdbccc5426e09cf539c579d273161d3a3e93d9676b748e490438ce42` | 0 |
| scripts/archive/srv3-hoodi-upd4/steps/0911-upd4-voting.ts | 3388 | `8c1966e631921c772a6e820e280d3235f1aa071459c39a28ee32670becd0503c` | 0 |
| scripts/archive/stVaults-3.02/steps/0100-deploy-v3-02-implementations.ts | 3074 | `02db201409b39fab5d8378fa7262845fac6f1c021f73e85cb02d28e70793d7cf` | 0 |
| scripts/archive/stVaults-3.02/steps/0100-mock-upgrade-to-v3-02.ts | 1145 | `cb9d7b1879f53f3b0edded0b08b218b002dcbe7638d079325a60387621fbaf5f` | 0 |
| scripts/archive/stvaults/steps/0000-check-env.ts | 995 | `ffe4c89615ffbbda610225fdb230ac24981dac3268424efa30e908149d2bbd8f` | 0 |
| scripts/archive/stvaults/steps/0100-deploy-v3-contracts.ts | 13791 | `f8d3e02c37170c62e832eea8ce9b9013148c530150c339b00cfc6abef916968f` | 0 |
| scripts/archive/stvaults/steps/0200-deploy-v3-upgrading-contracts.ts | 3372 | `d460adcc4bdd82ebf71f5cf41042dd0f2b4baf6d09f495a31936e2c5e73fc340` | 0 |
| scripts/archive/stvaults/steps/0300-deploy-v3-vote-script.ts | 769 | `c3cd09b7b276d584978231161e5acd1698e7990ea6168727f8d158dd1191a4bb` | 0 |
| scripts/archive/stvaults/steps/0500-mock-v3-aragon-voting.ts | 266 | `4e5acf083acbeafe7ab2e8d55ee6954cd831b1a67995df59084e7cf0c3879cca` | 0 |
| scripts/archive/stvaults/steps/x0000-deploy-locator.ts | 2508 | `fe1b16ea0fd31def21684b4ab0bd50fc3a2259950846266dde1bb33e59bcc053` | 0 |
| scripts/archive/stvaults-hoodi/upgrade/steps/0100-upgrade-hoodi-to-v3-rc2.ts | 5401 | `e26ad32c3ea17e16219d9765f2cfb8c44610f986bab7797c9041c6db454cd114` | 0 |
| scripts/archive/stvaults-hoodi/upgrade/steps/0100-upgrade-hoodi-to-v3-rc3.ts | 4691 | `2ba3c284e9877c302d7b2a12516e659b05a13d0d378a8f6259db482031516ce2` | 0 |
| scripts/archive/stvaults-hoodi/upgrade/steps/0100-upgrade-hoodi-to-v3-rc4.ts | 2277 | `2f35314e80f40e549ef29559980a72b99cc0b2acf4e4449c01d0a64140f930c2` | 0 |
| scripts/archive/stvaults-hoodi/upgrade/steps/0100-upgrade-hoodi-to-v3-rc5.ts | 4506 | `056c93e5eb0cb77506447e21280385a3d10caf29456786fed87879cc6e00b1aa` | 0 |
| scripts/archive/stvaults-hoodi/upgrade/steps/xxxx-update-lazy-oracle.ts | 437 | `da44d7af225c991565c6a6389f82b43a16c1f5654f82de95f595abf911bdc20d` | 0 |
| scripts/scratch/scratch-deploy.ts | 278 | `3ced7f3a139dc3ec82d0d53069867e48e85a0bd0c96b19834a34bf3787285ec9` | 0 |
| scripts/scratch/steps/0000-populate-deploy-artifact-from-env.ts | 2846 | `c867d117578e9246313b4c4e62bc63d3f234a46463de9d73b801970b422edab9` | 0 |
| scripts/scratch/steps/0010-deploy-deposit-contract.ts | 725 | `eecb99a08f318734c4443203d5bce0d0be9b645b59042230aff52278c95a203c` | 0 |
| scripts/scratch/steps/0020-deploy-aragon-env.ts | 5676 | `05b079f1cc5af75b9d8f92caaca7163c56aedb972dd0cf7ca5b278cb0e792cf8` | 0 |
| scripts/scratch/steps/0030-deploy-template-and-app-bases.ts | 1593 | `334bcfa966ff01138ef9a00e20964b2e65c6e9738c481846079b68e86afdbc04` | 0 |
| scripts/scratch/steps/0040-register-ens-domain.ts | 2096 | `8382f91ac4b6cce3c47e7667a495e651fab46b268d569342848702ec28bc9b90` | 0 |
| scripts/scratch/steps/0050-deploy-apm.ts | 2457 | `0a883f405ec7d54fa0b10276765c91efe980669d31aba4d4b0dac04bb1ed8ed9` | 0 |
| scripts/scratch/steps/0060-create-app-repos.ts | 1498 | `24713547854b171aee291a0880d96a096a926cd296c7761fe16d5d833350defd` | 0 |
| scripts/scratch/steps/0070-deploy-dao.ts | 9054 | `c097c9d0f69db569adb98bf9d1d468cc219873e47ad925fbe242fdc96b6298b4` | 0 |
| scripts/scratch/steps/0080-issue-tokens.ts | 2588 | `79dad12d4588dff012121e61d5f245d817759ccf0d5118e062b986dd454a5457` | 0 |
| scripts/scratch/steps/0083-deploy-core.ts | 20178 | `8046854b7e59911f06fdd0f13c313be2888ffc202db1bdc583df671c84fa7954` | 0 |
| scripts/scratch/steps/0085-deploy-vaults.ts | 5360 | `e81d047d918e99dba311dce8fd0c83c36e89b17664df3b921bdd91fb740ee482` | 0 |
| scripts/scratch/steps/0090-upgrade-locator.ts | 2235 | `4d7453823cea2008a54567e4fcea58f6f5f2a522aff18bda430e274ada9a4656` | 0 |
| scripts/scratch/steps/0100-deploy-circuit-breaker.ts | 4841 | `aad150130abc26a6aeae1eb19a05c47396946c680fb7129aa3b16deaeaf1f0e4` | 0 |
| scripts/scratch/steps/0101-deploy-easytrack.ts | 945 | `cab07b779a186322859fae6ea696eea43aa183300f3c2eeba1a1704625789dc6` | 0 |
| scripts/scratch/steps/0102-deploy-execution-delegation-framework.ts | 383 | `bf31d3e8e7963203922166817ee77a663831e673051e312c1ec7cda8f70bd949` | 0 |
| scripts/scratch/steps/0110-finalize-dao.ts | 667 | `8db6c71f3899a072ea004f0f474a7821d3409c9c8c6df5c25d384e1a984595d7` | 0 |
| scripts/scratch/steps/0120-post-locator-initializers.ts | 2297 | `288f2bb86eba7ccd9ef6559aebbe2eeddfde5077198cd3b470d2f6d21cab383b` | 0 |
| scripts/scratch/steps/0130-grant-roles.ts | 4953 | `3a9cd49c66a498269bc8866d714f960f1aebea3d036708a52e8529e4789a2d80` | 0 |
| scripts/scratch/steps/0135-deploy-staking-modules.ts | 340 | `b5758b28833d0da075bf4ffef5fb2d7930d2aeb3da853bfa77d3a887a958ab89` | 0 |
| scripts/scratch/steps/0140-plug-staking-modules.ts | 14739 | `795f1fa2281d2f8804f444b4b4755db6785c740a0cde45fd882ed1c0fada3cd4` | 0 |
| scripts/scratch/steps/0150-transfer-roles.ts | 4047 | `db39ae7006e77af9c4cdee48e15a7be6ba26d3bb38d44d0d8114111f3e00e054` | 0 |
| scripts/tooling/steps/0000-check-env.ts | 995 | `ffe4c89615ffbbda610225fdb230ac24981dac3268424efa30e908149d2bbd8f` | 0 |
| scripts/tooling/steps/0100-deploy-alerting-harness.ts | 767 | `fa1fa81fb360bc635a7c1ded27408c6f20b2fda03de4a6e83b1068225631652a` | 0 |
| scripts/upgrade/steps/0000-check-env.ts | 906 | `026f581d4df8916d2d5e5f81c449429f74d2bf81523db623f8b6dc19b202958b` | 0 |
| scripts/upgrade/steps/0100-deploy-base-contracts.ts | 15271 | `7e82c778d82c8e45e49f271de902cffa444133112a6cf16ca734ac6c19a3086f` | 0 |
| scripts/upgrade/steps/0135-deploy-staking-modules.ts | 629 | `b3cd83849f194cdbc885c8dc08e3bc47683d2779e4f0a22aaa0d50b72dae55f6` | 0 |
| scripts/upgrade/steps/0200-deploy-upgrade-template.ts | 10329 | `7517ce3d5a564d03bb8c0ab0b495f5e166b3407a53db03823c670e3fe5718d9e` | 0 |
| scripts/upgrade/steps/0300-deploy-upgrade-vote-script.ts | 1242 | `dcff048f2932c6c83564f61ab3b2d424d7857d8afb19a8a749468293342923b7` | 0 |
| scripts/upgrade/steps/0500-mock-dg-voting.ts | 266 | `4e5acf083acbeafe7ab2e8d55ee6954cd831b1a67995df59084e7cf0c3879cca` | 0 |
| scripts/upgrade/steps/0500-mock-upgrade.ts | 4265 | `fb2fe77fafc61cb4171832cc129cb7564c5f4bc3b6c9c14c857b246fd1c254c7` | 0 |
| scripts/upgrade/steps/0910-edf-deploy-delegation-contracts.ts | 545 | `7d35cefad1f8f43f9e54c988d9e43083c44d1204ec1cfa4c67410e0a0d617cc2` | 0 |
| scripts/upgrade/steps/0910-edf-prepare-protocol-delegation-contracts.ts | 567 | `a44587fe65d570186b668525068512925fb2a875a6ea0e1170b6e75855c13239` | 0 |
| scripts/upgrade/steps/0911-edf-deploy.ts | 3871 | `69a18dc479f487ef991103ec383d05e5a802e06084f6183c0666c49db89620f5` | 0 |
| scripts/upgrade/steps/0912-edf-deploy-upgrade-template.ts | 6607 | `3c5451d1d398b9502b36e7503112ef805de6b8b7babd98d7ae0de606f1c614fa` | 0 |
| scripts/upgrade/steps/0913-edf-deploy-upgrade-vote-script.ts | 1288 | `db59b1fbaff385097d4a78875ec18d71298a69106db19c1e7a583cd0758d48d3` | 0 |
| scripts/upgrade/steps/1000-mock-voting.ts | 202 | `d7a5d908d98fed9eca8c29d00e28a237fe69036347d9d1b339b3df7f5e15eab2` | 0 |
| scripts/utils/edf-upgrade.ts | 17503 | `da9bbd3f124728feddc9af1657609e2fc371c0c8b0082b78fec6b78aef03c9ee` | 0 |
| scripts/utils/execution-delegation-framework.ts | 7323 | `fed3d2e514d45c9b2c3f7b1e5989dc180829ea0c9d08464d9ae02b4264e378ab` | 0 |
| scripts/utils/migrate.ts | 770 | `a5fb5bf67b2d0288cf38f1dd9d0d1b0fd71b08593528fa289cd3e7f3ecf74317` | 0 |
| scripts/utils/mine.ts | 454 | `b097f7493fe679bc79b7fd1903f3bf5b261abdfedbe802dd4702a3c9774b1368` | 0 |
| scripts/utils/omnibus.ts | 1221 | `334f228eb1c1ede9f4a54e87cea4a4c8a4cdf6bf1de1a4c8b1bd0d2d20038bfd` | 0 |
| scripts/utils/scratch.ts | 4483 | `d452a241fe698a8f4b8504d88a908c0212b23af4b4f3302a857fd376880557a1` | 0 |
| scripts/utils/staking-modules.ts | 17712 | `48cceac159f3e00ff59895b5575d0b59aff7ae3c927d488874037df53d2981d3` | 0 |
| scripts/utils/upgrade.ts | 19850 | `5c7402eccd7c600700e3220a55a91cf04e00e41c06cf1cbb2d48b352bcbeae91` | 0 |
| tasks/check-interfaces.ts | 17984 | `f4c78baf340bf324fac7c43c7f1ca7735da97a2918070b5f40f08d98a9bf0798` | 0 |
| tasks/compile.ts | 754 | `05e1c32c540ed5ab8cf1c39be92ee7a4195e0ea33b44f504852151b167271be9` | 0 |
| tasks/extract-abis.ts | 1804 | `8d5d41d3ef4f7b1e124b01bf80e5a7bb472fcc4f12907e400cfa7649b27dfc32` | 0 |
| tasks/index.ts | 234 | `b96b185424c77774d8d4b84106cbe6f09827b36724749606a1fade33bbc1b1f2` | 0 |
| tasks/lint-solidity.ts | 6069 | `ae53223b46a2f814eeb20b28c5b2036f33a514e3a5168eda05585bcf92d190e0` | 0 |
| tasks/logger.ts | 5529 | `91534c55aeadb3a3a134ca3d236af8f4108f88c4d71958ac8acec3c3866c2018` | 0 |
| tasks/overrides.ts | 1512 | `c0a18bcf445ff30c79b3862dd4b53a681a4e1866bfdab47046f4e7e61742f96f` | 0 |
| tasks/protocol-get-addresses.ts | 289 | `350aaa02cfecc993cde30c1006c573b76083e1f6b016546999e3aa0c9f4396e9` | 0 |
| tasks/validate-configs.ts | 13745 | `65a766cc81801e82c973b1afc67ebd69badb802c28cffd21ad0a54957df38166` | 0 |
| tasks/verify-contracts.ts | 3881 | `af94fe3c186d98dee294f58511e2ede898d2e1ea07f823d70438e60b7dde580d` | 0 |
| yarn.lock | 477869 | `dbf868f03eba5f710b37105fbe6df78de28706dc3e89f3bc21956f711d933f14` | 1 |
